"""PE-4 private association adapter. Importing this module performs no I/O.

Production paths and authority are fixed. Injected interfaces are for synthetic
validation; the entrypoint exposes no fixture, credential or recovery arguments.
"""
import asyncio
import collections
import contextlib
import errno
import hashlib
import json
import logging
import os
from pathlib import Path
import re
import socket
import stat
import struct
import sys
import time
from datetime import datetime, timezone

HOME = Path("/home/jazofv1/hioc")
ENVIRONMENT = HOME / "runtime/pe4/environments/cpython311-websockets16.1.1-lock-v1"
INTERPRETER = HOME / "runtime/pe4/active/bin/python"
ENDPOINT = "ws://192.168.100.251:8123/api/websocket"
STATE = "state/inventory/associations/home_assistant.json"
LOCK = "state/inventory/associations/.home_assistant.lock"
SCHEMA_PATH = "governance/pe4/pe4-home-assistant-association-state-v1.1.schema.json"
SCHEMA_SHA = "5cd060ffd0a7a2e0a2b3e61da50ec8e5a418f4251df7305f713c10701b0e6a5d"
CLOSURE_PATH = "governance/pe4/pe4-ha-runtime-credential-provisioning-closure.json"
CLOSURE_SHA = "ae1aa575799576d7bdbd64670a516fdc1e38cb6c2b5b6fb816211e69987dde18"
COMMANDS = ("config/device_registry/list", "config/entity_registry/list",
            "config/area_registry/list", "config_entries/get")
CAPABILITIES = ("version_metadata", "authentication", "device_registry",
                "entity_registry", "area_registry", "config_entries")
LIMIT = 16 * 1024 * 1024


class Failure(Exception):
    def __init__(self, stage, preserved="UNKNOWN"):
        self.stage, self.preserved = stage, preserved
        super().__init__(stage)


def require(condition, stage):
    if not condition:
        raise Failure(stage)


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True, allow_nan=False) + "\n").encode("utf-8")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def instant(value):
    require(type(value) is str, "CANDIDATE_STATE_VALIDATION")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        require(parsed.utcoffset() is not None, "CANDIDATE_STATE_VALIDATION")
        return parsed.astimezone(timezone.utc)
    except (ValueError, OverflowError):
        raise Failure("CANDIDATE_STATE_VALIDATION") from None


def strict_json(raw, stage, registry=False):
    require(type(raw) in (bytes, str), stage)
    require(len(raw if type(raw) is bytes else raw.encode("utf-8")) <= LIMIT, stage)
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, stage)
            result[key] = value
        return result
    def nonfinite(_):
        raise Failure(stage)
    try:
        value = json.loads(raw, object_pairs_hook=pairs, parse_constant=nonfinite)
    except (ValueError, UnicodeError, RecursionError):
        raise Failure(stage) from None
    names = set()
    def walk(item, depth):
        require(depth <= 32, stage)
        if type(item) is dict:
            if registry:
                require(len(item) <= 128, stage)
                names.update(item)
                require(len(names) <= 256, stage)
            for key, child in item.items():
                if registry: require(len(key) <= 1024, stage)
                walk(child, depth + 1)
        elif type(item) is list:
            for child in item: walk(child, depth + 1)
        elif type(item) is str and registry:
            require(len(item) <= 1024, stage)
        elif type(item) is float:
            import math
            require(math.isfinite(item), stage)
    walk(value, 0)
    return value


KEYWORDS = {"$id", "$schema", "title", "type", "const", "enum", "anyOf",
            "properties", "required", "additionalProperties", "items", "minItems",
            "maxItems", "uniqueItems", "minimum", "maximum", "minLength", "maxLength", "pattern"}


def check_schema_contract(schema):
    require(type(schema) is dict and not set(schema) - KEYWORDS, "CONTRACT_VALIDATION")
    for child in schema.get("properties", {}).values(): check_schema_contract(child)
    for child in schema.get("anyOf", []): check_schema_contract(child)
    if "items" in schema: check_schema_contract(schema["items"])
    if "pattern" in schema:
        try: re.compile(schema["pattern"])
        except re.error: raise Failure("CONTRACT_VALIDATION") from None


def validate_schema(value, schema):
    stage = "CANDIDATE_STATE_VALIDATION"
    types = {"object": dict, "array": list, "string": str, "integer": int,
             "boolean": bool, "null": type(None), "number": (int, float)}
    if "type" in schema:
        kind = schema["type"]
        require(kind in types and (type(value) in types[kind] if kind == "number"
                                  else type(value) is types[kind]), stage)
    if "const" in schema:
        require(type(value) is type(schema["const"]) and value == schema["const"], stage)
    if "enum" in schema:
        require(any(type(value) is type(v) and value == v for v in schema["enum"]), stage)
    if "anyOf" in schema:
        valid = False
        for branch in schema["anyOf"]:
            try: validate_schema(value, branch); valid = True; break
            except Failure: pass
        require(valid, stage)
    if type(value) is dict:
        props = schema.get("properties", {})
        require(set(schema.get("required", [])) <= value.keys(), stage)
        if schema.get("additionalProperties") is False:
            require(not value.keys() - props.keys(), stage)
        for key, child in value.items():
            if key in props: validate_schema(child, props[key])
    elif type(value) is list:
        require(schema.get("minItems", 0) <= len(value) <= schema.get("maxItems", LIMIT), stage)
        if schema.get("uniqueItems"):
            require(len({encoded(v) for v in value}) == len(value), stage)
        if "items" in schema:
            for child in value: validate_schema(child, schema["items"])
    elif type(value) is str:
        require(schema.get("minLength", 0) <= len(value) <= schema.get("maxLength", LIMIT), stage)
        if "pattern" in schema: require(re.search(schema["pattern"], value) is not None, stage)
    elif type(value) in (int, float):
        require(schema.get("minimum", -float("inf")) <= value <= schema.get("maximum", float("inf")), stage)


def episode(record):
    return record["ha_device_id"], record["hioc_device_id"], instant(record["last_confirmed_at"])


def validate_privacy(value):
    """Schema is the field allowlist; values must not carry raw network identities."""
    if type(value) is str:
        require(not any(ord(c) < 32 or ord(c) == 127 for c in value) and
                not re.search(r"(?i)(?:https?://|[0-9a-f]{2}(?::[0-9a-f]{2}){5}|(?:[0-9]{1,3}\.){3}[0-9]{1,3}|\b[a-z0-9-]+\.(?:local|lan|home)\b)", value), "CANDIDATE_STATE_VALIDATION")
    elif type(value) is dict:
        for child in value.values(): validate_privacy(child)
    elif type(value) is list:
        for child in value: validate_privacy(child)


def validate_state(state, schema, prior=None):
    validate_schema(state, schema)
    validate_privacy(state)
    stage = "CANDIDATE_STATE_VALIDATION"
    updated = instant(state["updated_at"])
    owners, firsts, active_ha, active_hioc, episodes = {}, {}, set(), set(), set()
    entity_ids, registry_ids = set(), set()
    for record in state["associations"] + state["binding_history"]:
        ha, hioc = record["ha_device_id"], record["hioc_device_id"]
        require(ha not in owners or owners[ha] == hioc, stage); owners[ha] = hioc
        first, last = instant(record["first_associated_at"]), instant(record["last_confirmed_at"])
        pair = ha, hioc
        require(pair not in firsts or firsts[pair] == first, stage); firsts[pair] = first
        require(first <= last, stage)
        if "retired_at" in record:
            require(last < instant(record["retired_at"]) <= updated, stage)
            require(episode(record) not in episodes, stage); episodes.add(episode(record))
        else:
            require(last == updated and ha not in active_ha and hioc not in active_hioc, stage)
            active_ha.add(ha); active_hioc.add(hioc)
            config_ids = [entry["entry_id"] for entry in record.get("config_entries", [])]
            require(len(config_ids) == len(set(config_ids)), stage)
            for entity in record.get("entities", []):
                require(entity["registry_id"] not in registry_ids and entity["entity_id"] not in entity_ids, stage)
                registry_ids.add(entity["registry_id"]); entity_ids.add(entity["entity_id"])
    summary = state["summary"]
    require(summary["associated_devices"] == len(state["associations"]), stage)
    require(summary["historical_bindings"] == len(state["binding_history"]), stage)
    require(summary["entity_memberships"] == sum(len(a.get("entities", [])) for a in state["associations"]), stage)
    diagnostics = {d["reason"]: d["count"] for d in state["diagnostics"]}
    require(len(diagnostics) == len(state["diagnostics"]), stage)
    for name, prefix in (("review_only", "REVIEW_ONLY_"), ("rejected", "REJECT_")):
        require(summary[name] == sum(n for reason, n in diagnostics.items() if reason.startswith(prefix)), stage)
    require(summary["unmatched"] == diagnostics.get("UNMATCHED_STRONG_EVIDENCE", 0), stage)
    if prior is not None:
        require(updated > instant(prior["updated_at"]), stage)
        current_history = {episode(h): h for h in state["binding_history"]}
        for h in prior["binding_history"]: require(current_history.get(episode(h)) == h, stage)
        pairs = {(a["ha_device_id"], a["hioc_device_id"]) for a in state["associations"]}
        for old in prior["associations"]:
            pair = old["ha_device_id"], old["hioc_device_id"]
            if pair not in pairs: require(episode(old) in current_history, stage)
        for old in prior["associations"] + prior["binding_history"]:
            pair = old["ha_device_id"], old["hioc_device_id"]
            require(owners.get(pair[0]) == pair[1] and firsts.get(pair) == instant(old["first_associated_at"]), stage)


def normalize_mac(value):
    require(type(value) is str, "CANONICAL_INVENTORY_INPUT")
    value = value.strip().lower().replace("-", ":")
    return value if re.fullmatch(r"[0-9a-f]{2}(?::[0-9a-f]{2}){5}", value) else None


def validate_inventory(raw, now):
    stage = "CANONICAL_INVENTORY_INPUT"
    value = strict_json(raw, stage)
    require(type(value) is dict and {"schema_version", "updated", "devices", "services", "topology", "dependencies", "summary"} <= value.keys(), stage)
    require(value["schema_version"] == "1.0" and type(value["updated"]) is str and
            all(type(value[key]) is kind for key, kind in (("devices", list), ("services", list),
                ("topology", dict), ("dependencies", dict), ("summary", dict))) and
            len(value["devices"]) <= 65536, stage)
    try: age = (now - instant(value["updated"])).total_seconds()
    except Failure: raise Failure(stage) from None
    require(-60 <= age <= 5400, stage)
    ids, index = {}, collections.defaultdict(set)
    for device in value["devices"]:
        require(type(device) is dict and type(device.get("id")) is str and re.fullmatch(r"dev_[0-9a-f]{16}", device["id"]), stage)
        require(device["id"] not in ids, stage)
        mac = device.get("mac")
        if mac not in (None, ""):
            require(type(mac) is str, stage)
            mac = normalize_mac(mac); require(mac is not None, stage)
            index[mac].add(device["id"])
        ids[device["id"]] = mac
    return ids, index


def credential_value(raw):
    stage = "CREDENTIAL_ACQUISITION"
    require(type(raw) is bytes and 2 <= len(raw) <= 4097 and raw.endswith(b"\n"), stage)
    value = raw[:-1]
    require(1 <= len(value) <= 4096 and all(0x21 <= c <= 0x7e for c in value), stage)
    return value.decode("ascii")


def registry_cores(registries):
    stage = "REGISTRY_SCHEMA"
    specifications = ((4096, {"id": str, "connections": list}, ("id",)),
                      (65536, {"id": str, "entity_id": str, "platform": str, "device_id": (str, type(None))}, ("id", "entity_id")),
                      (2048, {"area_id": str, "name": str}, ("area_id",)),
                      (4096, {"entry_id": str, "domain": str}, ("entry_id",)))
    require(type(registries) is list and len(registries) == 4, stage)
    namespaces, fields = set(), set()
    for records, (limit, core, keys) in zip(registries, specifications):
        require(type(records) is list and len(records) <= limit, stage)
        unique = {key: set() for key in keys}
        for record in records:
            require(type(record) is dict and len(record) <= 128, stage)
            fields.update(record); require(len(fields) <= 256, stage)
            for key, kinds in core.items():
                require(key in record and type(record[key]) in (kinds if type(kinds) is tuple else (kinds,)), stage)
            for key in keys:
                require(record[key] and record[key] not in unique[key], stage); unique[key].add(record[key])
            if "connections" in core:
                # The pinned 2b model bounds the union of both pair namespaces.
                # Optional identifiers remain supporting-only and are never indexed.
                for field in ("connections", "identifiers"):
                    if field not in record: continue
                    require(type(record[field]) is list, stage)
                    for pair in record[field]:
                        require(type(pair) is list and len(pair) == 2 and
                                all(type(v) is str and (field == "connections" or 0 < len(v) <= 1024) for v in pair), stage)
                        namespaces.add(pair[0]); require(len(namespaces) <= 128, stage)
    return registries


def mac_outcomes(devices, hioc_index):
    parsed, reverse = {}, collections.defaultdict(set)
    for device in devices:
        macs, invalid = set(), False
        for namespace, value in device["connections"]:
            if namespace == "mac":
                mac = normalize_mac(value)
                if mac is None: invalid = True
                else: macs.add(mac); reverse[mac].add(device["id"])
        parsed[device["id"]] = macs, invalid
    outcomes, targets = {}, {}
    for ha, (macs, invalid) in parsed.items():
        if invalid: reason = "REJECT_INVALID_MAC"
        elif not macs: reason = "REVIEW_ONLY_NO_MAC"
        elif len(macs) != 1: reason = "REVIEW_ONLY_MULTIPLE_MAC"
        else:
            mac = next(iter(macs)); matches = hioc_index.get(mac, set())
            if len(reverse[mac]) != 1: reason = "REJECT_HA_MAC_COLLISION"
            elif len(matches) > 1: reason = "REJECT_HIOC_MAC_AMBIGUITY"
            elif not matches: reason = "UNMATCHED_STRONG_EVIDENCE"
            else: reason = "ASSOCIATED_STRONG_MAC"; targets[ha] = next(iter(matches))
        outcomes[ha] = reason
    return outcomes, targets


def private_relationships(device, registries, property_schema):
    devices, entities, areas, entries = registries
    area_by = {a["area_id"]: a for a in areas}; entry_by = {e["entry_id"]: e for e in entries}
    device_ids = {d["id"] for d in devices}
    result, incomplete, configs = {}, False, set()
    def safe(value, schema):
        try:
            validate_schema(value, schema)
            validate_privacy(value)
            def text_ok(v):
                if type(v) is str:
                    return not any(ord(c) < 32 or ord(c) == 127 for c in v) and not re.search(r"(?i)(?:https?://|[0-9a-f]{2}(?::[0-9a-f]{2}){5}|(?:[0-9]{1,3}\.){3}[0-9]{1,3})", v)
                if type(v) is dict: return all(text_ok(x) for x in v.values())
                if type(v) is list: return all(text_ok(x) for x in v)
                return True
            return text_ok(value)
        except Failure: return False
    def optional(source, key, target, schema, resolves=None):
        nonlocal incomplete
        if key not in source: return
        value = source[key]
        if safe(value, schema) and (value is None or resolves is None or value in resolves): target[key] = value
        else: incomplete = True
    safe_entries = {key: value for key, value in entry_by.items() if safe({"entry_id": key, "domain": value["domain"]}, property_schema["config_entries"]["items"])}
    metadata = {}
    for key, schema in property_schema["ha_metadata"]["properties"].items():
        optional(device, key, metadata, schema, device_ids if key == "via_device_id" else None)
    if metadata: result["ha_metadata"] = metadata
    if device.get("area_id") is not None:
        area = area_by.get(device["area_id"]) if type(device["area_id"]) is str else None
        candidate = {"area_id": area["area_id"]} if area else None
        if candidate is not None and safe(candidate, property_schema["area_candidate"]):
            area_properties = property_schema["area_candidate"]["anyOf"][0]["properties"]
            optional(area, "name", candidate, area_properties["name"])
            result["area_candidate"] = candidate
        else: incomplete = True
    def config_ref(value):
        nonlocal incomplete
        if value is None: return
        if type(value) is str and value in safe_entries: configs.add(value)
        else: incomplete = True
    if "config_entry_id" in device: config_ref(device["config_entry_id"])
    if "config_entries" in device:
        if type(device["config_entries"]) is list:
            for value in device["config_entries"]: config_ref(value)
        else: incomplete = True
    members = []; entity_schema = property_schema["entities"]["items"]
    for entity in entities:
        if entity["device_id"] != device["id"]: continue
        member = {"registry_id": entity["id"], "entity_id": entity["entity_id"], "platform": entity["platform"]}
        for key in ("area_id", "config_entry_id", "disabled_by", "entity_category"):
            optional(entity, key, member, entity_schema["properties"][key], area_by if key == "area_id" else safe_entries if key == "config_entry_id" else None)
        if "config_entry_id" in entity: config_ref(entity["config_entry_id"])
        if safe(member, entity_schema): members.append(member)
        else: incomplete = True
    if members: result["entities"] = sorted(members, key=lambda e: (e["registry_id"], e["entity_id"]))
    projected = []; config_schema = property_schema["config_entries"]["items"]
    for entry_id in sorted(configs):
        entry = entry_by[entry_id]; member = {"entry_id": entry_id, "domain": entry["domain"]}
        for key in ("state", "disabled_by"): optional(entry, key, member, config_schema["properties"][key])
        if safe(member, config_schema): projected.append(member)
        else: incomplete = True
    if projected: result["config_entries"] = projected
    result["relationship_status"] = "INCOMPLETE" if incomplete else "COMPLETE"
    return result


def reconcile(prior, registries, inventory, timestamp, version, schema):
    registry_cores(registries)
    devices, entities, _, _ = registries
    ids, index = inventory
    by_ha = {d["id"]: d for d in devices}
    raw, targets = mac_outcomes(devices, index); outcomes = dict(raw)
    old_active = prior["associations"] if prior else []
    old_history = prior["binding_history"] if prior else []
    old = old_active + old_history
    owners = {a["ha_device_id"]: a["hioc_device_id"] for a in old}
    sources = {a["hioc_device_id"]: a for a in old_active}
    current, rotations, used = [], set(), set()
    for ha in sorted(targets):
        hioc = targets[ha]
        if ha in owners and owners[ha] != hioc:
            outcomes[ha] = "REJECT_PRIOR_BINDING_CONFLICT"; continue
        source = sources.get(hioc)
        if source is None and ha not in owners:
            historical = [a for a in old_history if a["hioc_device_id"] == hioc]
            if historical:
                latest = max(instant(a["last_confirmed_at"]) for a in historical)
                latest_records = [a for a in historical if instant(a["last_confirmed_at"]) == latest]
                if len({a["ha_device_id"] for a in latest_records}) != 1:
                    outcomes[ha] = "REJECT_PRIOR_BINDING_CONFLICT"; continue
                source = latest_records[0]
        if source and source["ha_device_id"] != ha and source["ha_device_id"] in by_ha:
            outcomes[ha] = "REJECT_PRIOR_BINDING_CONFLICT"; continue
        if hioc in used:
            outcomes[ha] = "REJECT_PRIOR_BINDING_CONFLICT"; continue
        known = [a for a in old if a["ha_device_id"] == ha and a["hioc_device_id"] == hioc]
        first = min((a["first_associated_at"] for a in known), key=instant) if known else timestamp
        if source and source["ha_device_id"] != ha and not known: rotations.add(source["ha_device_id"])
        association = dict(hioc_device_id=hioc, ha_device_id=ha, association_basis="unique_mac",
                           status="ASSOCIATED_STRONG_MAC", first_associated_at=first,
                           last_confirmed_at=timestamp, observed_ha_version=version, contract_version="1.0")
        association.update(private_relationships(by_ha[ha], registries, schema["properties"]["associations"]["items"]["properties"]))
        current.append(association); used.add(hioc)
    history = [dict(h) for h in old_history]; existing = {episode(h) for h in history}; added = 0
    pairs = {(a["ha_device_id"], a["hioc_device_id"]) for a in current}
    for old_record in old_active:
        ha, hioc = old_record["ha_device_id"], old_record["hioc_device_id"]
        if (ha, hioc) in pairs: continue
        if ha in rotations: reason = "HA_DEVICE_RECREATED"
        elif ha not in by_ha: reason = "HA_DEVICE_ABSENT"
        elif raw[ha] == "REJECT_INVALID_MAC": reason = "HA_DEVICE_INVALID_MAC"
        elif raw[ha] == "REVIEW_ONLY_NO_MAC": reason = "HA_DEVICE_NO_MAC"
        elif raw[ha] == "REVIEW_ONLY_MULTIPLE_MAC": reason = "HA_DEVICE_MULTIPLE_MAC"
        elif raw[ha] == "REJECT_HA_MAC_COLLISION": reason = "HA_DEVICE_MAC_COLLISION"
        elif hioc not in ids: reason = "HIOC_DEVICE_ABSENT"
        elif raw[ha] == "REJECT_HIOC_MAC_AMBIGUITY": reason = "HIOC_MAC_AMBIGUITY"
        else: reason = "HIOC_CANONICAL_MAC_NO_LONGER_MATCHES"
        historical = {key: old_record[key] for key in ("hioc_device_id", "ha_device_id", "first_associated_at", "last_confirmed_at")}
        historical.update(retired_at=timestamp, retirement_reason=reason)
        if episode(historical) not in existing:
            history.append(historical); existing.add(episode(historical)); added += 1
    require(len(history) <= 4096, "BINDING_HISTORY_CAPACITY")
    counts = collections.Counter(outcomes.values())
    strong_ids = {a["ha_device_id"] for a in current}
    orphans = sum(e["device_id"] not in strong_ids for e in entities)
    if orphans: counts["ENTITY_WITHOUT_DEVICE_IDENTITY"] = orphans
    if added: counts["PRIOR_BINDING_RETIRED"] = added
    if rotations: counts["HA_DEVICE_ID_RECREATED"] = len(rotations)
    state = dict(schema_version="1.1", updated_at=timestamp, instance_reference="PI5_HA",
                 observed_ha_version=version, contract_version="1.0",
                 associations=sorted(current, key=lambda a: (a["hioc_device_id"], a["ha_device_id"])),
                 binding_history=sorted(history, key=episode),
                 diagnostics=[dict(reason=r, count=n) for r, n in sorted(counts.items())],
                 summary=dict(associated_devices=len(current), entity_memberships=sum(len(a.get("entities", [])) for a in current),
                              review_only=sum(n for r, n in counts.items() if r.startswith("REVIEW_ONLY_")),
                              rejected=sum(n for r, n in counts.items() if r.startswith("REJECT_")),
                              unmatched=counts["UNMATCHED_STRONG_EVIDENCE"], historical_bindings=len(history)))
    validate_state(state, schema, prior)
    require(len(encoded(state)) <= LIMIT, "CANDIDATE_STATE_VALIDATION")
    return state


# The current closure supplies this descriptor/ACL boundary; it is runtime-owned.
HOST = "nutandpihole"
OPERATOR = "jazofv1"
FINAL_NAME = "home_assistant.token"
MAX_FILE = 4097

def credential_require(condition, _code):
    require(condition, "CREDENTIAL_ACQUISITION")

def effective_readers(users, groups, user, group):
    """NSS enumeration plus lookups; primary membership is not in gr_mem."""
    credential_require(len({u.pw_name for u in users}) == len(users), "ACCOUNT_LOOKUP_INVALID")
    credential_require(len({u.pw_uid for u in users}) == len(users), "ACCOUNT_LOOKUP_INVALID")
    credential_require(len({g.gr_name for g in groups}) == len(groups), "ACCOUNT_LOOKUP_INVALID")
    credential_require(sum(g.gr_gid == group.gr_gid for g in groups) == 1, "ACCOUNT_LOOKUP_INVALID")
    credential_require(sum(u == user for u in users) == 1 and sum(g == group for g in groups) == 1, "ACCOUNT_LOOKUP_INVALID")
    credential_require(user.pw_name == OPERATOR and user.pw_uid > 0 and group.gr_name == OPERATOR and group.gr_gid > 0, "ACCOUNT_LOOKUP_INVALID")
    credential_require(len(group.gr_mem) == len(set(group.gr_mem)), "ACCOUNT_LOOKUP_INVALID")
    by_name = {u.pw_name: u for u in users}
    credential_require(all(name in by_name for name in group.gr_mem), "ACCOUNT_LOOKUP_INVALID")
    readers = {u.pw_name for u in users if u.pw_gid == group.gr_gid}
    readers.update(group.gr_mem)
    credential_require(OPERATOR in readers, "GROUP_READER_INVALID")
    credential_require(all(name == OPERATOR or by_name[name].pw_uid == 0 for name in readers), "GROUP_READER_INVALID")
    return group.gr_gid


def identities(mode):
    credential_require(sys.platform == "linux", "LINUX_REQUIRED")
    credential_require(os.uname().nodename == HOST, "HOST_INVALID")
    import pwd
    import grp
    try:
        user = pwd.getpwnam(OPERATOR)
        group = grp.getgrnam(OPERATOR)
        users, groups = pwd.getpwall(), grp.getgrall()
        root = pwd.getpwuid(0)
        credential_require(root.pw_name == "root" and root.pw_uid == 0 and sum(u == root for u in users) == 1, "ACCOUNT_LOOKUP_INVALID")
        gid = effective_readers(users, groups, user, group)
        members = set(group.gr_mem) | {u.pw_name for u in users if u.pw_gid == gid}
        for member in members:
            looked_up = pwd.getpwnam(member)
            credential_require(looked_up.pw_name == member and sum(u == looked_up for u in users) == 1, "ACCOUNT_LOOKUP_INVALID")
        credential_require(pwd.getpwuid(user.pw_uid) == user and grp.getgrgid(gid) == group, "ACCOUNT_LOOKUP_INVALID")
    except (KeyError, OSError):
        raise Failure("ACCOUNT_LOOKUP_INVALID") from None
    if mode == "root":
        credential_require(os.geteuid() == 0 and os.getuid() == 0, "ROOT_REQUIRED")
    else:
        credential_require(os.geteuid() == user.pw_uid and os.getuid() == user.pw_uid, "OPERATOR_REQUIRED")
        credential_require(gid in {os.getegid(), *os.getgroups()}, "OPERATOR_GROUP_INVALID")
    return gid


def fingerprint(info):
    return (info.st_dev, info.st_ino, info.st_mode, info.st_uid, info.st_gid,
            info.st_nlink, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


class NativeFS:
    """Descriptor-relative Linux credential operations; imports perform no I/O."""
    security_stage = "CREDENTIAL_ACQUISITION"
    def open_root(self):
        return os.open("/", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)

    def open_dir(self, parent, name):
        return os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=parent)

    def open_file(self, parent, name):
        return os.open(name, os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=parent)

    def fstat(self, fd):
        return os.fstat(fd)

    def lstat(self, parent, name):
        return os.stat(name, dir_fd=parent, follow_symlinks=False)

    def read(self, fd, size):
        return os.read(fd, size)

    def close(self, fd):
        os.close(fd)

    def acl(self, fd, directory=False):
        for attr in (["system.posix_acl_access", "system.posix_acl_default"] if directory else ["system.posix_acl_access"]):
            try:
                raw = os.getxattr(fd, attr)
            except OSError as exc:
                # ENODATA is an authoritative absent ACL; ENOTSUP/EPERM etc fail.
                require(exc.errno == errno.ENODATA, self.security_stage)
                continue
            require(attr.endswith("access"), self.security_stage)
            require(len(raw) == 28 and struct.unpack("<I", raw[:4])[0] == 2, self.security_stage)
            entries = [struct.unpack("<HHI", raw[i:i+8]) for i in range(4, 28, 8)]
            mode = stat.S_IMODE(self.fstat(fd).st_mode)
            expected = [(1, (mode >> 6) & 7, 0xffffffff), (4, (mode >> 3) & 7, 0xffffffff), (32, mode & 7, 0xffffffff)]
            require(entries == expected, self.security_stage)


def check_directory(fs, fd, gid=None):
    info = fs.fstat(fd)
    mode = stat.S_IMODE(info.st_mode)
    credential_require(stat.S_ISDIR(info.st_mode) and info.st_uid == 0 and not (mode & 0o7022), "DIRECTORY_INVALID")
    if gid is not None:
        credential_require(info.st_gid == gid and mode == 0o750, "DIRECTORY_INVALID")
    fs.acl(fd, True)
    return info


def bound_name(fs, parent, name, fd):
    require(fingerprint(fs.lstat(parent, name)) == fingerprint(fs.fstat(fd)),
            getattr(fs, "security_stage", "CREDENTIAL_ACQUISITION"))


def open_hierarchy(fs, gid):
    fds = []
    try:
        fd = fs.open_root(); fds.append(fd); check_directory(fs, fd)
        for name in ("etc", "hioc", "credentials"):
            parent = fd
            fd = fs.open_dir(parent, name); fds.append(fd)
            check_directory(fs, fd, gid if name != "etc" else None)
            bound_name(fs, parent, name, fd)
        return fds
    except BaseException:
        for fd in reversed(fds): fs.close(fd)
        raise


def recheck_hierarchy(fs, fds, gid):
    for index, fd in enumerate(fds):
        check_directory(fs, fd, gid if index >= 2 else None)
        if index:
            bound_name(fs, fds[index-1], ("etc", "hioc", "credentials")[index-1], fd)


def read_credential(fs, parent, gid, name=FINAL_NAME, expected=None):
    # lstat before open rejects FIFO/device/directory without opening it.
    initial = fs.lstat(parent, name)
    credential_require(stat.S_ISREG(initial.st_mode) and initial.st_nlink == 1, "FILE_INVALID")
    fd = fs.open_file(parent, name)
    data = None
    try:
        before = fs.fstat(fd)
        credential_require(fingerprint(initial) == fingerprint(before), "NAME_BINDING_CHANGED")
        credential_require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "FILE_INVALID")
        credential_require(before.st_uid == 0 and before.st_gid == gid and stat.S_IMODE(before.st_mode) == 0o640, "FILE_SECURITY_INVALID")
        credential_require(2 <= before.st_size <= MAX_FILE, "CONTENT_INVALID")
        fs.acl(fd)
        data = fs.read(fd, MAX_FILE + 1)  # one bounded logical read; short reads fail.
        credential_require(len(data) == before.st_size, "READ_INCOMPLETE")
        credential_require(fingerprint(before) == fingerprint(fs.fstat(fd)), "FILE_CHANGED")
        bound_name(fs, parent, name, fd)
        credential_value(data)
        credential_require(expected is None or data == expected, "CONTENT_CHANGED")
        return credential_value(data)
    finally:
        data = None
        fs.close(fd)




class PosixFS(NativeFS):
    """Pinned state storage; its security errors never originate from credentials."""
    security_stage = "STATE_PUBLICATION"
    def __init__(self, uid, gid):
        self.uid, self.gid = uid, gid
        self.chain = []
        self.parent = None
        self.lock_fd = None

    def security(self, fd, directory=False, mode=0o600, links=1, owner=None):
        info = self.fstat(fd)
        require((stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode)) and
                info.st_uid == (self.uid if owner is None else owner) and info.st_gid == self.gid and
                stat.S_IMODE(info.st_mode) == mode and (directory or info.st_nlink == links), "STATE_PUBLICATION")
        self.acl(fd, directory)
        return info

    def start(self):
        fd = self.open_root(); self.chain.append((None, None, fd))
        for name in ("home", "jazofv1", "hioc", "state", "inventory", "associations"):
            parent = fd
            if name == "associations":
                try: os.mkdir(name, 0o700, dir_fd=parent); os.fsync(parent)
                except FileExistsError: pass
            fd = self.open_dir(parent, name); self.chain.append((parent, name, fd))
        self.parent = fd
        self.guard()

    def guard(self):
        for parent, name, fd in self.chain:
            info = self.fstat(fd)
            require(stat.S_ISDIR(info.st_mode) and info.st_uid in (0, self.uid) and
                    not stat.S_IMODE(info.st_mode) & 0o022, "STATE_PUBLICATION")
            self.acl(fd, True)
            if parent is not None:
                named = self.lstat(parent, name)
                require((info.st_dev, info.st_ino, info.st_mode, info.st_uid, info.st_gid) ==
                        (named.st_dev, named.st_ino, named.st_mode, named.st_uid, named.st_gid), "STATE_PUBLICATION")
        self.security(self.parent, True, 0o700)
        if self.lock_fd is not None:
            self.security(self.lock_fd)
            bound_name(self, self.parent, ".home_assistant.lock", self.lock_fd)

    def finish(self):
        for _, _, fd in reversed(self.chain): self.close(fd)
        self.chain.clear()

    def file(self, parent, name, limit=LIMIT, links=1, private=True):
        before = self.lstat(parent, name)
        require(stat.S_ISREG(before.st_mode) and before.st_nlink == links, "STATE_PUBLICATION")
        fd = self.open_file(parent, name)
        try:
            info = self.fstat(fd)
            require(fingerprint(info) == fingerprint(before), "STATE_PUBLICATION")
            if private: self.security(fd, links=links)
            else:
                require(info.st_uid == self.uid and not stat.S_IMODE(info.st_mode) & 0o022, "STATE_PUBLICATION")
                self.acl(fd)
            require(0 <= info.st_size <= limit, "STATE_PUBLICATION")
            data = self.read(fd, limit + 1)
            require(len(data) == info.st_size and fingerprint(info) == fingerprint(self.fstat(fd)) and
                    fingerprint(info) == fingerprint(self.lstat(parent, name)), "STATE_PUBLICATION")
            return data, info
        finally: self.close(fd)

    def write(self, parent, name, data):
        self.guard()
        fd = os.open(name, os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC,
                     0o600, dir_fd=parent)
        try:
            self.security(fd)
            offset = 0
            while offset < len(data):
                written = os.write(fd, data[offset:])
                require(written > 0, "STATE_PUBLICATION"); offset += written
            os.fsync(fd)
            os.lseek(fd, 0, os.SEEK_SET)
            require(os.read(fd, len(data) + 1) == data, "STATE_PUBLICATION")
            self.security(fd)
            bound_name(self, parent, name, fd)
        finally: self.close(fd)

    def names(self, parent): return os.listdir(parent)
    def sync(self, fd): self.guard(); os.fsync(fd)
    def mkdir(self, parent, name):
        self.guard(); os.mkdir(name, 0o700, dir_fd=parent)
    def link(self, src, name, dst, target):
        self.guard(); os.link(name, target, src_dir_fd=src, dst_dir_fd=dst, follow_symlinks=False)
    def replace(self, src, name, dst, target):
        self.guard(); os.replace(name, target, src_dir_fd=src, dst_dir_fd=dst)
    def unlink(self, parent, name, expected):
        self.guard()
        actual = self.lstat(parent, name)
        require((actual.st_dev, actual.st_ino) == (expected.st_dev, expected.st_ino) and stat.S_ISREG(actual.st_mode), "STATE_PUBLICATION")
        os.unlink(name, dir_fd=parent)
    def rmdir(self, parent, name, fd):
        self.guard(); bound_name(self, parent, name, fd)
        self.security(fd, True, 0o700); os.rmdir(name, dir_fd=parent)

    @contextlib.contextmanager
    def lock(self):
        import fcntl
        fd, locked, entered = None, False, False
        try:
            self.guard()
            fd = os.open(".home_assistant.lock", os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC,
                         0o600, dir_fd=self.parent)
            self.security(fd); bound_name(self, self.parent, ".home_assistant.lock", fd)
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB); locked = True
            self.lock_fd = fd
            self.guard()
            entered = True
            yield
        except (OSError, Failure):
            if not entered: raise Failure("LOCK_ACQUISITION") from None
            raise
        finally:
            try:
                if locked:
                    try:
                        if entered: self.guard()
                    finally:
                        self.lock_fd = None
                        fcntl.flock(fd, fcntl.LOCK_UN)
            finally:
                if fd is not None: self.close(fd)


def read_prior(fs, schema):
    # Only absence at the initial no-follow name probe is a first baseline.
    # Disappearance after that probe is a coherence failure, never an empty reset.
    try: fs.lstat(fs.parent, "home_assistant.json")
    except FileNotFoundError: return None, None, None
    except (OSError, Failure): raise Failure("PRIOR_STATE_VALIDATION") from None
    try: raw, info = fs.file(fs.parent, "home_assistant.json")
    except (OSError, Failure): raise Failure("PRIOR_STATE_VALIDATION") from None
    try:
        value = strict_json(raw, "PRIOR_STATE_VALIDATION")
        validate_state(value, schema)
    except Failure: raise Failure("PRIOR_STATE_VALIDATION") from None
    return value, raw, info


INTENT_KEYS = {"transaction_id", "final_basename", "prior_present", "prior_length", "candidate_length", "prior_sha256", "candidate_sha256"}
MARKER_KEYS = {"transaction_id", "intent_sha256", "candidate_sha256"}
NAMESPACE = re.compile(r"\.home_assistant\.(txn|done)-([0-9a-f]{32})$")


class Publication:
    """Hardlinked prior, durable intent and commit marker, cleanup-only done name."""
    def __init__(self, fs, schema): self.fs, self.schema = fs, schema

    def verify_bytes(self, raw):
        value = strict_json(raw, "STATE_PUBLICATION")
        validate_state(value, self.schema)
        return value

    def inspect(self, name):
        fs = self.fs; match = NAMESPACE.fullmatch(name)
        require(match is not None, "STATE_PUBLICATION")
        fd = fs.open_dir(fs.parent, name)
        try:
            fs.security(fd, True, 0o700); bound_name(fs, fs.parent, name, fd)
            names = set(fs.names(fd))
            require(names <= {"candidate.json", "prior.json", "intent.json", "committed.json"}, "STATE_PUBLICATION")
            # Done is intentionally cleanup-only, including partially removed metadata.
            if match[1] == "done": return fd, None, None, names
            require("intent.json" in names, "STATE_PUBLICATION")
            intent_raw, _ = fs.file(fd, "intent.json", 4096)
            intent = strict_json(intent_raw, "STATE_PUBLICATION")
            require(type(intent) is dict and set(intent) == INTENT_KEYS and intent["transaction_id"] == match[2] and
                    intent["final_basename"] == "home_assistant.json" and type(intent["prior_present"]) is bool, "STATE_PUBLICATION")
            for key in ("prior_length", "candidate_length"):
                require(type(intent[key]) is int and 0 <= intent[key] <= LIMIT, "STATE_PUBLICATION")
            require(type(intent["candidate_sha256"]) is str and re.fullmatch(r"[0-9a-f]{64}", intent["candidate_sha256"]), "STATE_PUBLICATION")
            require((intent["prior_present"] and type(intent["prior_sha256"]) is str and re.fullmatch(r"[0-9a-f]{64}", intent["prior_sha256"])) or
                    (not intent["prior_present"] and intent["prior_sha256"] is None and intent["prior_length"] == 0), "STATE_PUBLICATION")
            require(("prior.json" in names) == intent["prior_present"], "STATE_PUBLICATION")
            if intent["prior_present"]:
                # Before replacement two links; afterwards only backup remains.
                info = fs.lstat(fd, "prior.json"); require(info.st_nlink in (1, 2), "STATE_PUBLICATION")
                raw, _ = fs.file(fd, "prior.json", links=info.st_nlink)
                require(len(raw) == intent["prior_length"] and digest(raw) == intent["prior_sha256"], "STATE_PUBLICATION")
                self.verify_bytes(raw)
            marker = None
            if "committed.json" in names:
                marker_raw, _ = fs.file(fd, "committed.json", 4096)
                marker = strict_json(marker_raw, "STATE_PUBLICATION")
                require(type(marker) is dict and set(marker) == MARKER_KEYS and marker ==
                        dict(transaction_id=match[2], intent_sha256=digest(intent_raw), candidate_sha256=intent["candidate_sha256"]), "STATE_PUBLICATION")
            return fd, intent, marker, names
        except BaseException:
            fs.close(fd); raise

    def cleanup(self, name, fd):
        fs = self.fs
        names = fs.names(fd)
        require(set(names) <= {"candidate.json", "prior.json", "intent.json", "committed.json"}, "STATE_PUBLICATION")
        pinned = []
        for child in names:
            info = fs.lstat(fd, child)
            raw, _ = fs.file(fd, child, links=info.st_nlink)
            require(info.st_nlink in (1, 2) and (info.st_nlink == 1 or child == "prior.json"), "STATE_PUBLICATION")
            pinned.append((child, info))
        for child, info in pinned: fs.unlink(fd, child, info)
        fs.sync(fd); fs.rmdir(fs.parent, name, fd); fs.sync(fs.parent)

    def to_done(self, name, fd):
        fs = self.fs; done = name.replace(".txn-", ".done-")
        require(done not in fs.names(fs.parent), "STATE_PUBLICATION")
        bound_name(fs, fs.parent, name, fd)
        fs.replace(fs.parent, name, fs.parent, done); fs.sync(fs.parent)
        self.cleanup(done, fd)

    def restore(self, fd, intent):
        fs = self.fs
        if "committed.json" in fs.names(fd):
            info = fs.lstat(fd, "committed.json"); fs.file(fd, "committed.json", 4096)
            fs.unlink(fd, "committed.json", info)
        fs.sync(fd)  # marker must be durably invalid before restoration.
        if intent["prior_present"]:
            info = fs.lstat(fd, "prior.json")
            raw, _ = fs.file(fd, "prior.json", links=info.st_nlink)
            require(len(raw) == intent["prior_length"] and digest(raw) == intent["prior_sha256"], "STATE_PUBLICATION")
            try: current = fs.lstat(fs.parent, "home_assistant.json")
            except FileNotFoundError: current = None
            if current is None or (current.st_dev, current.st_ino) != (info.st_dev, info.st_ino):
                # Keep the backup link until restoration is verified and cleanup completes.
                if "candidate.json" in fs.names(fd):
                    fs.unlink(fd, "candidate.json", fs.lstat(fd, "candidate.json"))
                fs.link(fd, "prior.json", fd, "candidate.json")
                fs.replace(fd, "candidate.json", fs.parent, "home_assistant.json")
            fs.sync(fs.parent)
            restored, actual = fs.file(fs.parent, "home_assistant.json", links=2)
            require(restored == raw and (actual.st_dev, actual.st_ino) == (info.st_dev, info.st_ino), "STATE_PUBLICATION")
        else:
            try:
                info = fs.lstat(fs.parent, "home_assistant.json")
                raw, _ = fs.file(fs.parent, "home_assistant.json")
                require(digest(raw) == intent["candidate_sha256"], "STATE_PUBLICATION")
                fs.unlink(fs.parent, "home_assistant.json", info)
            except FileNotFoundError: pass
            fs.sync(fs.parent)
            try: fs.lstat(fs.parent, "home_assistant.json")
            except FileNotFoundError: pass
            else: raise Failure("STATE_PUBLICATION")

    def recovery(self):
        fs = self.fs; pending = []
        for name in fs.names(fs.parent):
            if name.startswith((".home_assistant.txn-", ".home_assistant.done-")):
                require(NAMESPACE.fullmatch(name), "STATE_PUBLICATION"); pending.append(name)
        txns = [n for n in pending if ".txn-" in n]
        require(len(txns) <= 1, "STATE_PUBLICATION")
        # Reject the entire set before cleanup if any namespace is malformed.
        opened = []
        try:
            for name in sorted(pending): opened.append((name, *self.inspect(name)))
            for name, fd, intent, marker, _ in opened:
                if ".done-" in name: self.cleanup(name, fd); continue
                if marker:
                    raw, _ = fs.file(fs.parent, "home_assistant.json")
                    require(len(raw) == intent["candidate_length"] and digest(raw) == intent["candidate_sha256"], "STATE_PUBLICATION")
                    self.verify_bytes(raw); fs.sync(fs.parent); fs.sync(fd)
                    self.to_done(name, fd)
                else:
                    self.restore(fd, intent); self.to_done(name, fd)
        except (OSError, Failure): raise Failure("STATE_PUBLICATION", "UNKNOWN") from None
        finally:
            for _, fd, *_ in opened: fs.close(fd)

    def publish(self, candidate, prior_raw, prior_info, recheck):
        fs = self.fs; data = encoded(candidate); self.verify_bytes(data)
        transaction_id = os.urandom(16).hex(); name = ".home_assistant.txn-" + transaction_id
        intent = dict(transaction_id=transaction_id, final_basename="home_assistant.json",
                      prior_present=prior_raw is not None, prior_length=len(prior_raw) if prior_raw is not None else 0,
                      candidate_length=len(data), prior_sha256=digest(prior_raw) if prior_raw is not None else None,
                      candidate_sha256=digest(data))
        fd = None; prepared = False; committed = False; linked = False
        try:
            fs.mkdir(fs.parent, name); fd = fs.open_dir(fs.parent, name)
            fs.security(fd, True, 0o700); bound_name(fs, fs.parent, name, fd)
            fs.write(fd, "candidate.json", data)
            if prior_raw is not None:
                raw, info = fs.file(fs.parent, "home_assistant.json")
                require(raw == prior_raw and (info.st_dev, info.st_ino) == (prior_info.st_dev, prior_info.st_ino), "STATE_PUBLICATION")
                fs.link(fs.parent, "home_assistant.json", fd, "prior.json"); linked = True
                backup, info = fs.file(fd, "prior.json", links=2)
                require(backup == prior_raw and (info.st_dev, info.st_ino) == (prior_info.st_dev, prior_info.st_ino), "STATE_PUBLICATION")
            else:
                try: fs.lstat(fs.parent, "home_assistant.json")
                except FileNotFoundError: pass
                else: raise Failure("STATE_PUBLICATION")
            fs.write(fd, "intent.json", encoded(intent)); fs.sync(fd); fs.sync(fs.parent); prepared = True
            staged, _ = fs.file(fd, "candidate.json"); require(staged == data, "STATE_PUBLICATION")
            self.verify_bytes(staged); fs.guard(); bound_name(fs, fs.parent, name, fd)
            if prior_raw is not None:
                raw, info = fs.file(fs.parent, "home_assistant.json", links=2)
                require(raw == prior_raw and (info.st_dev, info.st_ino) == (prior_info.st_dev, prior_info.st_ino), "STATE_PUBLICATION")
            else:
                try: fs.lstat(fs.parent, "home_assistant.json")
                except FileNotFoundError: pass
                else: raise Failure("STATE_PUBLICATION")
            recheck()
            fs.replace(fd, "candidate.json", fs.parent, "home_assistant.json")
            final, _ = fs.file(fs.parent, "home_assistant.json")
            require(final == data, "STATE_PUBLICATION"); self.verify_bytes(final); fs.sync(fs.parent)
            marker = dict(transaction_id=transaction_id, intent_sha256=digest(encoded(intent)), candidate_sha256=digest(data))
            fs.write(fd, "committed.json", encoded(marker))
            actual, _ = fs.file(fd, "committed.json", 4096); require(actual == encoded(marker), "STATE_PUBLICATION")
            fs.sync(fd); committed = True
            try: self.to_done(name, fd)
            except (OSError, Failure): return "TRANSACTION_CLEANUP_FAILED"
            return None
        except BaseException as error:
            if committed: return "TRANSACTION_CLEANUP_FAILED"
            try:
                if prepared:
                    self.restore(fd, intent); self.to_done(name, fd)
                elif fd is not None:
                    # No final replacement is possible before durable intent.
                    self.cleanup(name, fd)
                if prior_raw is None:
                    try: fs.lstat(fs.parent, "home_assistant.json")
                    except FileNotFoundError: pass
                    else: raise Failure("STATE_PUBLICATION")
                else:
                    actual, info = fs.file(fs.parent, "home_assistant.json")
                    require(actual == prior_raw and (info.st_dev, info.st_ino) == (prior_info.st_dev, prior_info.st_ino), "STATE_PUBLICATION")
                fs.sync(fs.parent)
            except BaseException: raise Failure("STATE_PUBLICATION", "UNKNOWN") from None
            stage = error.stage if isinstance(error, Failure) and error.stage == "CANONICAL_INVENTORY_INPUT" else "STATE_PUBLICATION"
            raise Failure(stage, "TRUE") from None
        finally:
            if fd is not None: fs.close(fd)


async def bounded(factory, deadline, cap, stage, aborter):
    remaining = min(cap, deadline - time.monotonic())
    require(remaining > 0, stage)
    async def invoke():
        return await factory()
    task = asyncio.create_task(invoke())
    try:
        done, _ = await asyncio.wait({task}, timeout=remaining)
        require(task in done, stage)
        return await task
    finally:
        if not task.done():
            aborter(); task.cancel()
            done, _ = await asyncio.wait({task}, timeout=2)
            require(task in done, stage)
        if task.done() and not task.cancelled(): task.exception()


def abort_transport(ws):
    transport = getattr(ws, "transport", None)
    if transport is not None: transport.abort()


def normal_close(error):
    return all(getattr(getattr(error, side, None), "code", None) in (1000, 1001) for side in ("rcvd", "sent"))


async def exchange(ws, token, observation, deadline):
    from .core.compatibility import safe_version
    stage, capability = "HA_AUTHENTICATION", "version_metadata"
    registries, version = [], None
    async def receive():
        return strict_json(await bounded(ws.recv, deadline, 15, stage, lambda: abort_transport(ws)), stage, True)
    try:
        greeting = await receive()
        require(type(greeting) is dict and greeting.get("type") == "auth_required", stage)
        version = safe_version(greeting.get("ha_version"))
        require(version is not None, stage)
        observation["observed_version"] = version; observation["capabilities"][capability] = True
        capability = "authentication"
        message = json.dumps({"type": "auth", "access_token": token})
        try: await bounded(lambda: ws.send(message), deadline, 15, stage, lambda: abort_transport(ws))
        finally: message = None; token = None
        auth = await receive()
        require(type(auth) is dict and auth.get("type") == "auth_ok" and safe_version(auth.get("ha_version")) == version, stage)
        observation["capabilities"][capability] = True
        for command_id, command in enumerate(COMMANDS, 1):
            stage, capability = "REQUIRED_REGISTRY_COMMAND", CAPABILITIES[command_id + 1]
            await bounded(lambda: ws.send(json.dumps({"id": command_id, "type": command})), deadline, 15, stage, lambda: abort_transport(ws))
            result = await receive()
            require(type(result) is dict and set(result) == {"id", "type", "success", "result"} and
                    type(result.get("id")) is int and result["id"] == command_id and result.get("type") == "result" and
                    result.get("success") is True, stage)
            registries.append(result["result"])
            # Validate the real structural core as each capability is observed.
            stage = "REGISTRY_SCHEMA"
            padded = registries + [[] for _ in range(4 - len(registries))]
            registry_cores(padded)
            observation["capabilities"][capability] = True
        stage = "REQUIRED_REGISTRY_COMMAND"
        await bounded(ws.close, deadline, 2, stage, lambda: abort_transport(ws))
        try:
            await bounded(ws.recv, deadline, 2, stage, lambda: abort_transport(ws))
        except Exception as error:
            if not normal_close(error): raise
        else: raise Failure(stage)  # Any fifth/replayed envelope is prohibited.
        return registries, version
    except Failure:
        observation["capabilities"][capability] = False
        raise
    except BaseException:
        observation["available"] = False
        raise Failure(stage) from None
    finally:
        token = None; abort_transport(ws)


async def network(token, observation, connector=None, socket_factory=socket.socket):
    if connector is None:
        from websockets.asyncio.client import connect
        connector = connect
    class NoRedirect(connector):
        def process_redirect(self, error): return error
    deadline = time.monotonic() + 90
    sock, ws = None, None
    try:
        sock = socket_factory(socket.AF_INET, socket.SOCK_STREAM); sock.setblocking(False)
        await bounded(lambda: asyncio.get_running_loop().sock_connect(sock, ("192.168.100.251", 8123)), deadline, 5, "HA_CONNECTION", sock.close)
        logger = logging.Logger("hioc_ha_silent", logging.CRITICAL + 1)
        ws = await bounded(lambda: NoRedirect(ENDPOINT, sock=sock, proxy=None, compression=None,
                           ping_interval=None, max_queue=1, max_size=LIMIT, logger=logger,
                           open_timeout=min(5, deadline - time.monotonic()), close_timeout=2),
                           deadline, 5, "HA_CONNECTION", sock.close)
        observation["available"] = True
        return await exchange(ws, token, observation, deadline)
    except Failure:
        if ws is None: observation["available"] = False
        raise
    except BaseException:
        observation["available"] = False
        raise Failure("HA_CONNECTION") from None
    finally:
        token = None
        if ws is not None: abort_transport(ws)
        if sock is not None: sock.close()


class Runtime:
    """Production adapter dependencies; no command-line overrides."""
    def __init__(self):
        self.uid = self.gid = None
        self.registry = self.store = None
        self.schema = None

    def now(self): return datetime.now(timezone.utc)

    def target(self):
        from .core.config import ConfigService
        require(sys.platform == "linux" and os.name == "posix" and socket.gethostname() == HOST, "TARGET_VALIDATION")
        require(not any(key.lower() in {"hioc_home", "hioc_ha_endpoint", "http_proxy", "https_proxy", "all_proxy", "no_proxy"} for key in os.environ), "TARGET_VALIDATION")
        import pwd
        user = pwd.getpwnam(OPERATOR)
        require(os.getuid() == os.geteuid() == user.pw_uid and user.pw_uid > 0, "TARGET_VALIDATION")
        config = ConfigService().load()
        require(config.get("HIOC_HOME") == str(HOME) and config.get("HIOC_HA_ENDPOINT") == ENDPOINT, "TARGET_VALIDATION")
        # Credential-free local address inspection, no DNS and no subprocess secret.
        import subprocess
        result = subprocess.run(["/usr/sbin/ip", "-o", "-4", "addr", "show"], stdin=subprocess.DEVNULL,
                                capture_output=True, timeout=2, check=False)
        require(result.returncode == 0 and len(result.stdout) <= 65536 and
                re.search(rb"\binet 192\.168\.100\.252/", result.stdout), "TARGET_VALIDATION")
        self.uid = user.pw_uid

    def runtime(self):
        import platform
        import sysconfig
        import importlib.util
        import importlib.metadata
        require(sys.implementation.name == "cpython" and sys.version_info[:3] == (3, 11, 2) and
                platform.machine() == "aarch64" and sysconfig.get_config_var("SOABI") == "cpython-311-aarch64-linux-gnu" and
                sys.flags.isolated and sys.flags.dont_write_bytecode and Path(sys.prefix).resolve() == ENVIRONMENT and
                Path(sys.executable).absolute() == INTERPRETER, "RUNTIME_VALIDATION")
        site = ENVIRONMENT / "lib/python3.11/site-packages"
        require(not list(site.glob("*.pth")) and "sitecustomize" not in sys.modules and "usercustomize" not in sys.modules, "RUNTIME_VALIDATION")
        spec = importlib.util.find_spec("websockets")
        require(spec is not None and spec.origin is not None and Path(spec.origin).resolve() == site / "websockets/__init__.py", "RUNTIME_VALIDATION")
        for item in sys.path:
            resolved = Path(item).resolve()
            require(resolved == Path("/usr/lib/python311.zip") or resolved == Path("/usr/lib/python3.11") or
                    resolved == Path("/usr/lib/python3.11/lib-dynload") or resolved == site or
                    resolved == HOME / "pi4/lib", "RUNTIME_VALIDATION")
        distributions = {d.metadata["Name"].lower().replace("_", "-"): d.version for d in importlib.metadata.distributions(path=[str(site)])}
        require(distributions.get("websockets") == "16.1.1" and set(distributions) <= {"websockets", "pip", "setuptools"}, "RUNTIME_VALIDATION")
        import websockets
        require(websockets.__version__ == "16.1.1" and Path(websockets.__file__).resolve() == site / "websockets/__init__.py", "RUNTIME_VALIDATION")
        self.gid = identities("operator")

    def filesystem(self): return PosixFS(self.uid, self.gid)

    def home_file(self, fs, relative, limit=LIMIT):
        home_fd = fs.chain[3][2]; parts = relative.split("/"); opened = []
        try:
            parent = home_fd
            for part in parts[:-1]:
                fd = fs.open_dir(parent, part); opened.append((parent, part, fd))
                info = fs.fstat(fd)
                require(stat.S_ISDIR(info.st_mode) and info.st_uid in (0, self.uid) and not stat.S_IMODE(info.st_mode) & 0o022, "CONTRACT_VALIDATION")
                fs.acl(fd, True); bound_name(fs, parent, part, fd); parent = fd
            raw, _ = fs.file(parent, parts[-1], limit, private=False)
            for parent, part, fd in opened: bound_name(fs, parent, part, fd)
            fs.guard(); return raw
        finally:
            for _, _, fd in reversed(opened): fs.close(fd)

    def contracts(self, fs):
        from .core.compatibility import load_registry
        from .core.state import StateStore
        raw = self.home_file(fs, SCHEMA_PATH)
        require(digest(raw) == SCHEMA_SHA, "CONTRACT_VALIDATION")
        schema = strict_json(raw, "CONTRACT_VALIDATION"); check_schema_contract(schema)
        closure = self.home_file(fs, CLOSURE_PATH)
        require(digest(closure) == CLOSURE_SHA, "CONTRACT_VALIDATION")
        # Bind all frozen authority bytes, including the historical preparation.
        authorities = {
            "governance/pe4/pe4-0c-association-contract.json": "a48ec696c7e596dde68e252366f84ea46dfa7076a9b1aaff419a993742ed9a58",
            "governance/pe4/pe4-0c1-association-lifecycle-clarification.json": "de53307023af7c663878aa9e6212d27cf9023c372c69224bf4b186642c11fb0e",
            "governance/pe4/pe4-ha-association-adapter-implementation-preparation.json": "e014ce6a7b70db26f9d643318d93b8da9e6050afedbd09fe73e86e0efbd14d0b"}
        for path, expected in authorities.items(): require(digest(self.home_file(fs, path)) == expected, "CONTRACT_VALIDATION")
        compatibility_raw = self.home_file(fs, "governance/compatibility-contracts.json")
        require(digest(compatibility_raw) == "83493cacfef10ff85e936bcacbee215797c745e3fa6edff1954c3cc1f3c82227", "CONTRACT_VALIDATION")
        self.registry = load_registry(HOME / "governance/compatibility-contracts.json")
        require(strict_json(compatibility_raw, "CONTRACT_VALIDATION") == self.registry, "CONTRACT_VALIDATION")
        dependency = next(d for d in self.registry["dependencies"] if d["dependency_id"] == "ha_core")
        require(dependency["required_capabilities"] == list(CAPABILITIES), "CONTRACT_VALIDATION")
        self.store = StateStore(HOME / "state/platform")
        self.schema = schema
        return schema

    def inventory(self, fs):
        fs.guard()
        raw, _ = fs.file(fs.chain[-2][2], "inventory.json", private=False)
        return raw, validate_inventory(raw, self.now())

    def credential(self):
        fs = NativeFS(); fds = open_hierarchy(fs, self.gid)
        try:
            token = read_credential(fs, fds[-1], self.gid)
            recheck_hierarchy(fs, fds, self.gid)
            return token
        finally:
            for fd in reversed(fds): fs.close(fd)

    def observe(self, token, observation):
        # Closing this loop never waits indefinitely for cancelled foreign tasks.
        loop = asyncio.new_event_loop()
        loop.set_debug(False)
        loop.set_exception_handler(lambda _loop, _context: None)
        try: return loop.run_until_complete(network(token, observation))
        finally:
            token = None
            loop.close()

    def assessment(self, observation, timestamp):
        from .core.compatibility import assess
        dependency = next(d for d in self.registry["dependencies"] if d["dependency_id"] == "ha_core")
        previous_payload = self.store.read_json("compatibility.json", {})
        previous = next((d for d in previous_payload.get("dependencies", []) if d.get("dependency_id") == "ha_core"), {})
        return assess(dependency, observation, previous, timestamp)["status"]

    def report(self, observation, timestamp):
        from .core.compatibility import update_status
        update_status(self.store, self.registry, {"ha_core": observation}, timestamp)


RESULT_FIELDS = ("RESULT", "ERROR_CODE", "FAILURE_STAGE", "COMPATIBILITY_STATUS", "OBSERVED_HA_VERSION",
                 "ASSOCIATED_COUNT", "REVIEW_ONLY_COUNT", "REJECTED_COUNT", "UNMATCHED_COUNT", "HISTORICAL_BINDING_COUNT",
                 "STATE_PUBLISHED", "LAST_KNOWN_GOOD_PRESERVED")
STAGES = {"TARGET_VALIDATION", "RUNTIME_VALIDATION", "LOCK_ACQUISITION", "CONTRACT_VALIDATION", "PRIOR_STATE_VALIDATION",
          "CANONICAL_INVENTORY_INPUT", "CREDENTIAL_ACQUISITION", "HA_CONNECTION", "HA_AUTHENTICATION",
          "REQUIRED_REGISTRY_COMMAND", "REGISTRY_SCHEMA", "COMPATIBILITY", "ASSOCIATION_EVALUATION",
          "BINDING_HISTORY_CAPACITY", "CANDIDATE_STATE_VALIDATION", "STATE_PUBLICATION", "UNEXPECTED_INTERNAL"}


def result_fields(state=None, observation=None, status="UNKNOWN", error=None, warning=None, published=False, preserved="UNKNOWN"):
    from .core.compatibility import safe_version, STATES
    observation = observation or {}
    stage = error.stage if isinstance(error, Failure) and error.stage in STAGES else "UNEXPECTED_INTERNAL" if error else "NONE"
    code = "BINDING_HISTORY_CAPACITY_EXCEEDED" if stage == "BINDING_HISTORY_CAPACITY" else stage + "_FAILED" if error else warning or "NONE"
    require(warning in (None, "TRANSACTION_CLEANUP_FAILED", "COMPATIBILITY_REPORTING_FAILED"), "UNEXPECTED_INTERNAL")
    fields = dict(RESULT="FAIL" if error else "PASS_WITH_WARNING" if warning else "PASS", ERROR_CODE=code,
                  FAILURE_STAGE=stage, COMPATIBILITY_STATUS=status if status in STATES else "UNKNOWN",
                  OBSERVED_HA_VERSION=safe_version(observation.get("observed_version")) or "UNKNOWN",
                  STATE_PUBLISHED="TRUE" if published else "FALSE", LAST_KNOWN_GOOD_PRESERVED=preserved if preserved in ("TRUE", "FALSE", "UNKNOWN") else "UNKNOWN")
    for key, summary_key in (("ASSOCIATED_COUNT", "associated_devices"), ("REVIEW_ONLY_COUNT", "review_only"),
                             ("REJECTED_COUNT", "rejected"), ("UNMATCHED_COUNT", "unmatched"), ("HISTORICAL_BINDING_COUNT", "historical_bindings")):
        count = state["summary"][summary_key] if state else None
        fields[key] = str(count) if type(count) is int and 0 <= count <= (4096 if key == "HISTORICAL_BINDING_COUNT" else 65536) else "UNKNOWN"
    text = "\n".join(key + "=" + fields[key] for key in RESULT_FIELDS) + "\n"
    require(len(text.encode("ascii")) <= 4096 and len(text.splitlines()) <= 16, "UNEXPECTED_INTERNAL")
    return text


def run_cycle(runtime=None):
    runtime = runtime or Runtime()
    fs = None; prior = raw_prior = prior_info = candidate = None
    prior_valid = observed = published = False
    observation = {"capabilities": {capability: None for capability in CAPABILITIES}}
    status, warning, preserved = "UNKNOWN", None, "UNKNOWN"
    stage = "TARGET_VALIDATION"
    error = None
    def action(selected, call):
        nonlocal stage
        stage = selected
        try: return call()
        except Failure as failure:
            if failure.stage in STAGES and (selected in {"STATE_PUBLICATION", "ASSOCIATION_EVALUATION", "HA_CONNECTION"}): raise
            raise Failure(selected, failure.preserved) from None
    try:
        action("TARGET_VALIDATION", runtime.target)
        action("RUNTIME_VALIDATION", runtime.runtime)
        fs = runtime.filesystem()
        action("LOCK_ACQUISITION", fs.start)
        with fs.lock():
            try:
                schema = action("CONTRACT_VALIDATION", lambda: runtime.contracts(fs))
                writer = Publication(fs, schema)
                action("STATE_PUBLICATION", writer.recovery)
                prior, raw_prior, prior_info = action("PRIOR_STATE_VALIDATION", lambda: read_prior(fs, schema))
                prior_valid = True; preserved = "TRUE"
                raw_inventory, inventory = action("CANONICAL_INVENTORY_INPUT", lambda: runtime.inventory(fs))
                inventory_sha = digest(raw_inventory)
                token = action("CREDENTIAL_ACQUISITION", runtime.credential)
                try:
                    observed = True
                    registries, version = action("HA_CONNECTION", lambda: runtime.observe(token, observation))
                finally: token = None
                timestamp = runtime.now().isoformat().replace("+00:00", "Z")
                status = action("COMPATIBILITY", lambda: runtime.assessment(observation, timestamp))
                from .core.compatibility import GOOD
                require(status in GOOD, "COMPATIBILITY")
                candidate = action("ASSOCIATION_EVALUATION", lambda: reconcile(prior, registries, inventory, timestamp, version, schema))
                action("CANDIDATE_STATE_VALIDATION", lambda: validate_state(candidate, schema, prior))
                def recheck():
                    refreshed, _ = action("CANONICAL_INVENTORY_INPUT", lambda: runtime.inventory(fs))
                    require(refreshed == raw_inventory and digest(refreshed) == inventory_sha, "CANONICAL_INVENTORY_INPUT")
                warning = action("STATE_PUBLICATION", lambda: writer.publish(candidate, raw_prior, prior_info, recheck))
                published = True; preserved = "FALSE"
                try: runtime.report(observation, timestamp)
                except BaseException:
                    if warning is None: warning = "COMPATIBILITY_REPORTING_FAILED"
            except BaseException as failure:
                error = failure if isinstance(failure, Failure) else Failure(stage)
                preserved = error.preserved if error.stage == "STATE_PUBLICATION" else preserved
                if prior_valid and error.stage != "STATE_PUBLICATION":
                    try:
                        if raw_prior is None:
                            try: fs.lstat(fs.parent, "home_assistant.json")
                            except FileNotFoundError: pass
                            else: raise Failure("STATE_PUBLICATION")
                        else:
                            actual, info = fs.file(fs.parent, "home_assistant.json")
                            require(actual == raw_prior and (info.st_dev, info.st_ino) == (prior_info.st_dev, prior_info.st_ino), "STATE_PUBLICATION")
                    except BaseException: preserved = "UNKNOWN"
                if observed:
                    try:
                        timestamp = runtime.now().isoformat().replace("+00:00", "Z")
                        status = runtime.assessment(observation, timestamp)
                        runtime.report(observation, timestamp)
                    except BaseException: pass
    except BaseException as failure:
        if published:
            if warning is None: warning = "TRANSACTION_CLEANUP_FAILED"
        else: error = failure if isinstance(failure, Failure) else Failure(stage)
    finally:
        if fs is not None:
            try: fs.finish()
            except BaseException:
                if published and warning is None: warning = "TRANSACTION_CLEANUP_FAILED"
                elif not published: preserved = "UNKNOWN"
    return result_fields(candidate if published else prior if prior_valid else None, observation, status,
                         error, warning, published, preserved)


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if args:
        sys.stdout.write(result_fields(error=Failure("TARGET_VALIDATION"))); return 1
    alarm = None
    if sys.platform == "linux":
        import signal
        def timeout(_signum, _frame): raise Failure("UNEXPECTED_INTERNAL")
        alarm = signal.signal(signal.SIGALRM, timeout)
        signal.setitimer(signal.ITIMER_REAL, 180)
    try: text = run_cycle()
    except BaseException: text = result_fields(error=Failure("UNEXPECTED_INTERNAL"))
    finally:
        if alarm is not None:
            signal.setitimer(signal.ITIMER_REAL, 0); signal.signal(signal.SIGALRM, alarm)
    sys.stdout.write(text)
    return 1 if text.startswith("RESULT=FAIL\n") else 0
