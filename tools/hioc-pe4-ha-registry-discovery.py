#!/usr/bin/env python3
"""PE-4.0B.2b: bounded, memory-only capability-first HA registry discovery.

No execution is authorized by repository preparation. No raw payload is logged,
written, or included in an exception. This standalone artifact leaves 2a intact.
"""
from __future__ import annotations

import asyncio
import getpass
import hashlib
import importlib
import inspect
import json
import logging
import math
import os
import re
import secrets
import socket
import stat
import subprocess
import sys
import time
import warnings

CORE_TAG = "2026.8.1"
COMMANDS = (
    "config/device_registry/list", "config/entity_registry/list",
    "config/area_registry/list", "config_entries/get",
)
REGISTRIES = ("device", "entity", "area", "config_entry")
CONNECT_TIMEOUT = 5.0
RECEIVE_TIMEOUT = 15.0
TOTAL_BUDGET = 90.0
CLOSE_TIMEOUT = 2.0
MAX_MESSAGE = 16 * 1024 * 1024
MAX_RECORDS = dict(zip(REGISTRIES, (4096, 65536, 2048, 4096)))
MAX_NAMESPACES = 128
MAX_FIELDS = 128
MAX_FIELD_NAMES = 256
MAX_DEPTH = 32
MAX_STRING = 1024
MAX_EVIDENCE = 256 * 1024
MAX_WARNINGS = 16
# Only these literals may escape the sanitizer. Other namespaces are counted.
SAFE_NAMESPACES = frozenset({"mac", "bluetooth", "zigbee", "zwave", "upnp",
                             "mqtt", "hue", "esphome", "zha", "zwave_js"})
ERROR_CODES = frozenset({
    "WRONG_TARGET", "WRONG_OPERATOR", "UNSUPPORTED_HA_DEPLOYMENT",
    "UNSUPPORTED_INTERFACE", "AUTHENTICATION_UNAVAILABLE", "AUTHENTICATION_FAILED",
    "INSUFFICIENT_READ_SCOPE", "UNEXPECTED_SCHEMA", "PRIVACY_CONTRACT_VIOLATION",
    "DISCOVERY_OUTPUT_UNSAFE", "EVIDENCE_PUBLICATION_FAILED", "UNEXPECTED_ERROR",
})
STAGES = frozenset({"TARGET_IDENTITY", "HA_DEPLOYMENT_DISCOVERY", "AUTHENTICATION",
                    "INTERFACE_DISCOVERY", "SCHEMA_DISCOVERY", "PRIVACY_VALIDATION",
                    "EVIDENCE_PUBLICATION", "COMPLETE"})
WARNING_CODES = frozenset({"UNKNOWN_FIELDS", "UNPUBLISHED_NAMESPACES",
                           "RELATIONSHIP_SNAPSHOT_INCOMPLETE", "CLASSIFICATION_NOT_DERIVED"})
TYPES = frozenset({"null", "string", "boolean", "integer", "number", "array", "object"})


def field_contract(strings="", nullable="", arrays="", objects="", booleans="", numbers="", integers=""):
    result = {}
    for names, kinds in ((strings, {"string"}), (nullable, {"string", "null"}),
                         (arrays, {"array"}), (objects, {"object"}),
                         (booleans, {"boolean"}), (numbers, {"integer", "number"}),
                         (integers, {"integer"})):
        result.update({name: frozenset(kinds) for name in names.split()})
    return result


FIELDS = {
    "device": field_contract(
        strings="id config_entry_id primary_config_entry",
        nullable="area_id configuration_url config_subentry_id disabled_by entry_type hw_version manufacturer model model_id name_by_user name serial_number sw_version via_device_id",
        arrays="config_entries connections identifiers labels", objects="config_entries_subentries",
        numbers="created_at modified_at"),
    "entity": field_contract(
        strings="entity_id id platform unique_id",
        nullable="area_id config_entry_id config_subentry_id device_id disabled_by entity_category hidden_by icon name original_name translation_key",
        arrays="labels", objects="categories options", booleans="has_entity_name",
        numbers="created_at modified_at"),
    "area": field_contract(strings="area_id name", nullable="floor_id humidity_entity_id icon picture temperature_entity_id",
                            arrays="aliases labels", numbers="created_at modified_at"),
    "config_entry": field_contract(strings="entry_id domain title source state",
        nullable="disabled_by reason error_reason_translation_key",
        objects="supported_subentry_types", booleans="supports_options supports_remove_device supports_unload supports_reconfigure pref_disable_new_entities pref_disable_polling",
        numbers="created_at modified_at", integers="num_subentries"),
}
FIELDS["config_entry"]["error_reason_translation_placeholders"] = frozenset({"object", "null"})
CORE = {
    "device": {"id", "config_entry_id", "connections", "identifiers", "area_id", "disabled_by", "via_device_id"},
    "entity": {"entity_id", "platform", "device_id", "area_id", "config_entry_id", "disabled_by"},
    "area": {"area_id"}, "config_entry": {"entry_id", "domain"},
}
ID_FIELD = dict(zip(REGISTRIES, ("id", "entity_id", "area_id", "entry_id")))
RELATIONS = {
    "device": {"area_id": "area", "via_device_id": "device", "config_entry_id": "config_entry"},
    "entity": {"area_id": "area", "device_id": "device", "config_entry_id": "config_entry"},
    "area": {}, "config_entry": {},
}
COUNT_KEYS = frozenset({"records", "disabled", "unknown_fields", "unknown_null", "unknown_string",
    "unknown_boolean", "unknown_integer", "unknown_number", "unknown_array", "unknown_object",
    "with_device", "without_device", "with_area", "with_config_entry", "via_device",
    "connections_zero", "connections_one", "connections_multiple", "mac_zero", "mac_one", "mac_multiple",
    "mac_entries", "mac_canonical", "mac_normalization_required", "mac_invalid", "mac_duplicate_entries",
    "mac_collision_values", "mac_conflicting_devices", "identifier_collision_values",
    "connection_collision_values", "unpublished_namespaces", "dangling_relationships",
    "template_platform", "group_domain", "scene_domain", "automation_domain"})


class Failure(Exception):
    def __init__(self, code, stage):
        if code not in ERROR_CODES or stage not in STAGES:
            code, stage = "UNEXPECTED_ERROR", "PRIVACY_VALIDATION"
        self.code, self.stage = code, stage
        self.compatibility = None
        super().__init__(code)


def reject(stage="SCHEMA_DISCOVERY", code="UNEXPECTED_SCHEMA"):
    raise Failure(code, stage)


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode("ascii")


def kind(value):
    return {type(None): "null", str: "string", bool: "boolean", int: "integer",
            float: "number", list: "array", dict: "object"}.get(type(value), "unsafe")


def strict_message(raw):
    if type(raw) is not str:
        reject()
    try:
        if len(raw.encode("utf-8")) > MAX_MESSAGE:
            reject()
    except (UnicodeError, MemoryError):
        reject()
    # Bound nesting before the decoder allocates nested containers.
    depth = 0
    quoted = escaped = False
    for char in raw:
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
        elif char in "[{":
            depth += 1
            if depth > MAX_DEPTH:
                reject()
        elif char in "]}":
            depth -= 1
    def pairs(items):
        obj = {}
        for key, value in items:
            if key in obj:
                reject()
            obj[key] = value
        return obj
    def finite_float(text):
        value = float(text)
        if not math.isfinite(value):
            reject()
        return value
    try:
        value = json.loads(raw, object_pairs_hook=pairs, parse_constant=lambda _: reject(), parse_float=finite_float)
    except (ValueError, RecursionError, MemoryError, OverflowError):
        reject()
    if type(value) is not dict:
        reject()
    return value


def checked_result(raw, command_id):
    msg = strict_message(raw)
    if (type(msg.get("id")) is not int or msg["id"] != command_id
            or msg.get("type") != "result" or type(msg.get("success")) is not bool):
        reject("INTERFACE_DISCOVERY")
    if msg["success"]:
        if set(msg) != {"id", "type", "success", "result"}:
            reject("INTERFACE_DISCOVERY")
        return msg["result"]
    if set(msg) != {"id", "type", "success", "error"} or type(msg["error"]) is not dict:
        reject("INTERFACE_DISCOVERY")
    error = msg["error"]
    if type(error.get("code")) is not str or type(error.get("message")) is not str:
        reject("INTERFACE_DISCOVERY")
    code = {"unauthorized": "INSUFFICIENT_READ_SCOPE", "not_allowed": "INSUFFICIENT_READ_SCOPE",
            "unknown_command": "UNSUPPORTED_INTERFACE"}.get(error["code"], "UNEXPECTED_SCHEMA")
    reject("INTERFACE_DISCOVERY", code)


def private_text(value, nullable=False):
    if nullable and value is None:
        return
    if type(value) is not str or not value or len(value) > MAX_STRING:
        reject()


def normalize_mac(value):
    if not (re.fullmatch(r"[0-9a-fA-F]{12}", value)
            or re.fullmatch(r"(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}", value)
            or re.fullmatch(r"(?:[0-9a-fA-F]{2}-){5}[0-9a-fA-F]{2}", value)
            or re.fullmatch(r"[0-9a-fA-F]{4}(?:\.[0-9a-fA-F]{4}){2}", value)):
        return None
    compact = re.sub(r"[:.\-]", "", value)
    if not re.fullmatch(r"[0-9a-fA-F]{12}", compact):
        return None
    return compact.lower()


class Reducer:
    """Retains only private relation/identity indexes, never whole raw records.

    Index keys are NOT hashed, serialized, logged, or included in fingerprint.
    They are discarded when report construction completes or invocation fails.
    """
    def __init__(self):
        self.observations = {}
        self.ids = {}
        self.links = []
        self.namespace_union = set()
        self.field_union = set()

    def consume(self, registry, records):
        if registry in self.observations or type(records) is not list or len(records) > MAX_RECORDS[registry]:
            reject()
        counts = {key: 0 for key in COUNT_KEYS}
        inventory = {}
        names = {"connection": set(), "identifier": set()}
        identities = set()
        collision_maps = {"mac": {}, "connection": {}, "identifier": {}}
        for row in records:
            if type(row) is not dict or len(row) > MAX_FIELDS or not CORE[registry].issubset(row):
                reject()
            for name, value in row.items():
                if type(name) is not str or len(name) > MAX_STRING:
                    reject()
                self.field_union.add(name)
                if len(self.field_union) > MAX_FIELD_NAMES:
                    reject()
                value_kind = kind(value)
                if value_kind == "unsafe" or (value_kind == "number" and not math.isfinite(value)):
                    reject()
                if name not in FIELDS[registry]:
                    counts["unknown_fields"] += 1
                    counts["unknown_" + value_kind] += 1
                    continue
                if value_kind not in FIELDS[registry][name]:
                    reject()
                item = inventory.setdefault(name, {"types": set(), "present": 0})
                item["types"].add(value_kind)
                item["present"] += 1
            identity = row[ID_FIELD[registry]]
            private_text(identity)
            if identity in identities:
                reject()
            identities.add(identity)
            counts["records"] += 1
            if row.get("disabled_by") is not None:
                counts["disabled"] += 1
            for field, target in RELATIONS[registry].items():
                ref = row[field]
                private_text(ref, nullable=True)
                if ref is not None:
                    self.links.append((registry, target, ref))
                    if field == "via_device_id":
                        counts["via_device"] += 1
                    else:
                        counts[{"device_id": "with_device", "area_id": "with_area",
                                "config_entry_id": "with_config_entry"}[field]] += 1
            if registry == "entity":
                private_text(row["platform"])
                counts["without_device"] += row["device_id"] is None
                counts["template_platform"] += row["platform"] == "template"
                for domain in ("group", "scene", "automation"):
                    counts[domain + "_domain"] += identity.startswith(domain + ".")
            if registry == "config_entry":
                private_text(row["domain"])
            if registry != "device":
                continue
            macs = []
            for field, category in (("connections", "connection"), ("identifiers", "identifier")):
                entries = row[field]
                if len(entries) > MAX_FIELDS:
                    reject()
                if field == "connections":
                    counts["connections_" + ("zero" if not entries else "one" if len(entries) == 1 else "multiple")] += 1
                seen = set()
                for pair in entries:
                    if type(pair) is not list or len(pair) != 2:
                        reject()
                    namespace, value = pair
                    private_text(namespace)
                    private_text(value)
                    self.namespace_union.add(namespace)
                    if len(self.namespace_union) > MAX_NAMESPACES:
                        reject()
                    if namespace in SAFE_NAMESPACES:
                        names[category].add(namespace)
                    else:
                        counts["unpublished_namespaces"] += 1
                    key = (namespace, value)
                    if key in seen:
                        reject()
                    seen.add(key)
                    collision_maps[category].setdefault(key, set()).add(identity)
                    if category == "connection" and namespace == "mac":
                        counts["mac_entries"] += 1
                        norm = normalize_mac(value)
                        if norm is None:
                            counts["mac_invalid"] += 1
                        else:
                            counts["mac_canonical" if re.fullmatch(r"(?:[0-9a-f]{2}:){5}[0-9a-f]{2}", value)
                                   else "mac_normalization_required"] += 1
                            collision_maps["mac"].setdefault(norm, set()).add(identity)
                            macs.append(norm)
            counts["mac_duplicate_entries"] += len(macs) - len(set(macs))
            nmac = sum(1 for pair in row["connections"] if pair[0] == "mac")
            counts["mac_" + ("zero" if not nmac else "one" if nmac == 1 else "multiple")] += 1
        for category, index in collision_maps.items():
            colliding = [owners for owners in index.values() if len(owners) > 1]
            counts[category + "_collision_values"] = len(colliding)
            if category == "mac":
                counts["mac_conflicting_devices"] = len(set().union(*colliding)) if colliding else 0
        self.ids[registry] = identities
        self.observations[registry] = {
            "counts": counts,
            "fields": {name: {"types": sorted(data["types"]), "optional": data["present"] < len(records)}
                       for name, data in sorted(inventory.items())},
            "namespaces": {name: sorted(values) for name, values in names.items()},
        }

    def finish(self):
        if set(self.observations) != set(REGISTRIES):
            reject()
        for registry, target, ref in self.links:
            if ref not in self.ids[target]:
                self.observations[registry]["counts"]["dangling_relationships"] += 1
        warnings_list = {"CLASSIFICATION_NOT_DERIVED"}
        for observation in self.observations.values():
            for count, warning in (("unknown_fields", "UNKNOWN_FIELDS"),
                                   ("unpublished_namespaces", "UNPUBLISHED_NAMESPACES"),
                                   ("dangling_relationships", "RELATIONSHIP_SNAPSHOT_INCOMPLETE")):
                if observation["counts"][count]:
                    warnings_list.add(warning)
        # Known field/type/observed optionality only. No namespace, count, or value.
        structure = {r: self.observations[r]["fields"] for r in REGISTRIES}
        report = base_report()
        report.update(registries=self.observations,
                      structure_fingerprint=hashlib.sha256(canonical(structure)).hexdigest(),
                      warnings=sorted(warnings_list))
        self.ids.clear()
        self.links.clear()
        self.namespace_union.clear()
        self.field_union.clear()
        validate_report(report)
        return report


def sanitized_version(value):
    if type(value) is not str or len(value) > 32 or not re.fullmatch(r"[0-9]{4}\.[0-9]{1,2}\.[0-9]{1,3}(?:(?:a|b|rc|\.dev)[0-9]{1,8})?", value):
        reject("HA_DEPLOYMENT_DISCOVERY", "UNEXPECTED_SCHEMA")
    return value


def compatibility_metadata(observed=None, failed=None, dependency="ha_core", status=None):
    if status is None:
        status = "INCOMPATIBLE" if failed else "COMPATIBILITY_UNKNOWN" if observed is None else "COMPATIBLE" if observed == CORE_TAG else "COMPATIBLE_UPDATED"
    return {"dependency_id": dependency, "status": status, "observed_version": observed,
            "compatibility_baseline": CORE_TAG if dependency == "ha_core" else None,
            "failed_capability": failed, "likely_update_compatibility_break": False}


def dependency_reject(dependency, capability, status="INCOMPATIBLE", code="UNSUPPORTED_INTERFACE", stage="INTERFACE_DISCOVERY"):
    error = Failure(code, stage)
    error.compatibility = compatibility_metadata(failed=capability, dependency=dependency, status=status)
    raise error


def base_report(code="NONE", stage="COMPLETE"):
    return {"schema_version": "1.1", "result": "PASS" if code == "NONE" else "FAIL",
            "target_classification": "APPROVED_PI3_TO_PI5_HA",
            "interface_classification": "CAPABILITY_FIRST_SOURCE_BASELINE_WEBSOCKET",
            "deployment_classification": "REMOTE_HA_ENDPOINT_ONLY",
            "core_source_reference": CORE_TAG,
            "INSTANCE_REFERENCE_METHOD": "OPERATOR_LOGICAL_LABEL", "INSTANCE_REFERENCE": "PI5_HA",
            "classification_limit": "PHYSICAL_HELPER_INTEGRATION_VIRTUAL_CLOUD_NOT_DERIVED",
            "registries": {}, "structure_fingerprint": None, "warnings": [],
            "privacy_validation": "PASS", "ERROR_CODE": code, "FAILURE_STAGE": stage,
            "compatibility": compatibility_metadata(status="COMPATIBILITY_UNKNOWN")}


def validate_report(report):
    """Structural allowlists first; textual defenses apply only to approved literals.

    Caller data cannot choose report keys, field names, namespaces, or warnings.
    Raw nested values are never legal evidence values.
    """
    def unsafe():
        reject("PRIVACY_VALIDATION", "DISCOVERY_OUTPUT_UNSAFE")
    base = base_report()
    if type(report) is not dict or set(report) != set(base):
        unsafe()
    varying = {"result", "registries", "structure_fingerprint", "warnings", "ERROR_CODE", "FAILURE_STAGE", "compatibility"}
    for key in set(base) - varying:
        if report[key] != base[key] or type(report[key]) is not str:
            unsafe()
    meta = report["compatibility"]
    if type(meta) is not dict or set(meta) != set(compatibility_metadata()):
        unsafe()
    if meta["dependency_id"] not in {"ha_core", "pe4_python", "pe4_websockets", "iproute"}:
        unsafe()
    if meta["status"] not in {"COMPATIBLE", "COMPATIBLE_UPDATED", "COMPATIBILITY_UNKNOWN", "INCOMPATIBLE", "TRUST_ANCHOR_CHANGED", "DEPENDENCY_UNAVAILABLE"}:
        unsafe()
    if meta["observed_version"] is not None:
        try:
            sanitized_version(meta["observed_version"])
        except Failure:
            unsafe()
    expected_baseline = CORE_TAG if meta["dependency_id"] == "ha_core" else None
    if meta["compatibility_baseline"] != expected_baseline or meta["likely_update_compatibility_break"] is not False:
        unsafe()
    if meta["failed_capability"] not in {None, "authentication", "device_registry", "entity_registry", "area_registry", "config_entries", "runtime_identity", "import_api", "address_output", "version_metadata", "transport"}:
        unsafe()
    code, stage = report["ERROR_CODE"], report["FAILURE_STAGE"]
    if type(code) is not str or type(stage) is not str or code not in ERROR_CODES | {"NONE"} or stage not in STAGES:
        unsafe()
    if report["result"] != ("PASS" if code == "NONE" else "FAIL"):
        unsafe()
    if (code == "NONE") != (stage == "COMPLETE"):
        unsafe()
    ws = report["warnings"]
    if type(ws) is not list or len(ws) > MAX_WARNINGS or any(type(v) is not str or v not in WARNING_CODES for v in ws):
        unsafe()
    if len(ws) != len(set(ws)):
        unsafe()
    regs = report["registries"]
    if type(regs) is not dict or set(regs) != (set(REGISTRIES) if code == "NONE" else set()):
        unsafe()
    for registry, obs in regs.items():
        if type(obs) is not dict or set(obs) != {"counts", "fields", "namespaces"}:
            unsafe()
        counts, fields, namespaces = obs["counts"], obs["fields"], obs["namespaces"]
        if type(counts) is not dict or set(counts) != COUNT_KEYS:
            unsafe()
        if any(type(n) is not int or not 0 <= n <= MAX_RECORDS[registry] * MAX_FIELDS * 3 for n in counts.values()):
            unsafe()
        if counts["records"] > MAX_RECORDS[registry]:
            unsafe()
        if type(fields) is not dict or not set(fields).issubset(FIELDS[registry]):
            unsafe()
        for name, inv in fields.items():
            if type(inv) is not dict or set(inv) != {"types", "optional"} or type(inv["optional"]) is not bool:
                unsafe()
            if type(inv["types"]) is not list or not inv["types"] or any(type(t) is not str or t not in FIELDS[registry][name] for t in inv["types"]):
                unsafe()
            if len(inv["types"]) != len(set(inv["types"])):
                unsafe()
        if type(namespaces) is not dict or set(namespaces) != {"connection", "identifier"}:
            unsafe()
        for values in namespaces.values():
            if type(values) is not list or len(values) > MAX_NAMESPACES or any(type(n) is not str or n not in SAFE_NAMESPACES for n in values):
                unsafe()
            if len(values) != len(set(values)):
                unsafe()
    fingerprint = report["structure_fingerprint"]
    if code == "NONE":
        structure = {r: regs[r]["fields"] for r in REGISTRIES}
        if type(fingerprint) is not str or fingerprint != hashlib.sha256(canonical(structure)).hexdigest():
            unsafe()
    elif fingerprint is not None:
        unsafe()
    payload = canonical(report)
    if len(payload) > MAX_EVIDENCE:
        unsafe()
    # Every free string above is enumerated. Defend approved schema tokens too.
    for registry in regs:
        for token in list(regs[registry]["fields"]) + sum(list(regs[registry]["namespaces"].values()), []):
            if not re.fullmatch(r"[a-z][a-z0-9_]{0,63}", token):
                unsafe()
    return payload


def time_left(deadline, cap, stage):
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        dependency_reject("ha_core", "transport", "DEPENDENCY_UNAVAILABLE", stage=stage)
    return min(remaining, cap)


async def bounded(factory, deadline, cap, stage, aborter=lambda: None):
    # Check before creating a coroutine/task. Abort the transport before
    # cancellation, including stalled sends (websockets discourages cancelling
    # send on an open connection). No retry and no new network cleanup budget.
    timeout = time_left(deadline, cap, stage)
    async def invoke():
        try:
            return await factory()
        except (Failure, asyncio.CancelledError):
            raise
        except Exception as exc:
            if any(getattr(getattr(exc, side, None), "code", None) == 1009 for side in ("rcvd", "sent")):
                reject("SCHEMA_DISCOVERY", "UNEXPECTED_SCHEMA")
            # The normal post-close receive is the only allowed closed result.
            if (getattr(getattr(exc, "rcvd", None), "code", None) in {1000, 1001}
                    and getattr(getattr(exc, "sent", None), "code", None) in {1000, 1001}):
                raise
            if isinstance(exc, OSError) or type(exc).__module__.startswith("websockets") or getattr(exc, "rcvd", None) is not None:
                dependency_reject("ha_core", "transport", "DEPENDENCY_UNAVAILABLE", stage=stage)
            dependency_reject("ha_core", "transport", "COMPATIBILITY_UNKNOWN", code="UNEXPECTED_ERROR", stage=stage)
    task = asyncio.create_task(invoke())
    try:
        done, _ = await asyncio.wait({task}, timeout=timeout)
        if task not in done:
            dependency_reject("ha_core", "transport", "DEPENDENCY_UNAVAILABLE", stage=stage)
        return await task
    finally:
        if not task.done():
            aborter()
            task.cancel()
            # The pinned websockets/asyncio operations cooperate after abort.
            # Only task reaping receives a finite grace, never more networking.
            done, _ = await asyncio.wait({task}, timeout=CLOSE_TIMEOUT)
            if task not in done:
                dependency_reject("ha_core", "transport", "DEPENDENCY_UNAVAILABLE", stage=stage)
        if task.done() and not task.cancelled():
            task.exception()


def abort(ws):
    transport = getattr(ws, "transport", None)
    if transport is not None:
        transport.abort()


async def close_bounded(ws, deadline):
    try:
        await bounded(ws.close, deadline, CLOSE_TIMEOUT, "INTERFACE_DISCOVERY", lambda: abort(ws))
    except BaseException:
        abort(ws)
        raise


async def exchange(ws, token, deadline):
    reducer = Reducer()
    observed = None
    capability = "version_metadata"
    try:
        greeting = strict_message(await bounded(ws.recv, deadline, RECEIVE_TIMEOUT, "AUTHENTICATION", lambda: abort(ws)))
        if not {"type", "ha_version"}.issubset(greeting) or greeting["type"] != "auth_required":
            reject("AUTHENTICATION")
        observed = sanitized_version(greeting["ha_version"])
        capability = "authentication"
        await bounded(lambda: ws.send(json.dumps({"type": "auth", "access_token": token})), deadline, RECEIVE_TIMEOUT, "AUTHENTICATION", lambda: abort(ws))
        token = None
        auth = strict_message(await bounded(ws.recv, deadline, RECEIVE_TIMEOUT, "AUTHENTICATION", lambda: abort(ws)))
        if auth.get("type") == "auth_invalid":
            reject("AUTHENTICATION", "AUTHENTICATION_FAILED")
        if not {"type", "ha_version"}.issubset(auth) or auth["type"] != "auth_ok" or sanitized_version(auth["ha_version"]) != observed:
            reject("AUTHENTICATION")
        for command_id, (registry, command) in enumerate(zip(REGISTRIES, COMMANDS), 1):
            capability = {"device": "device_registry", "entity": "entity_registry", "area": "area_registry", "config_entry": "config_entries"}[registry]
            await bounded(lambda: ws.send(json.dumps({"id": command_id, "type": command})), deadline, RECEIVE_TIMEOUT, "INTERFACE_DISCOVERY", lambda: abort(ws))
            raw = await bounded(ws.recv, deadline, RECEIVE_TIMEOUT, "INTERFACE_DISCOVERY", lambda: abort(ws))
            records = checked_result(raw, command_id)
            raw = None
            reducer.consume(registry, records)
            records = None
        # One close, no fifth command/poll. Drain only already queued responses
        # after the closing handshake; a normal ConnectionClosedOK is the end.
        await close_bounded(ws, deadline)
        try:
            await bounded(ws.recv, deadline, CLOSE_TIMEOUT, "INTERFACE_DISCOVERY", lambda: abort(ws))
        except Exception as exc:
            if not (getattr(getattr(exc, "rcvd", None), "code", None) in {1000, 1001}
                    and getattr(getattr(exc, "sent", None), "code", None) in {1000, 1001}):
                raise
        else:
            reject("INTERFACE_DISCOVERY")
        report = reducer.finish()
        report["compatibility"] = compatibility_metadata(observed)
        validate_report(report)
        return report
    except Failure as error:
        prior_status = error.compatibility["status"] if error.compatibility else None
        failed = "transport" if prior_status == "DEPENDENCY_UNAVAILABLE" else capability
        error.compatibility = compatibility_metadata(observed, failed, status=prior_status)
        raise
    finally:
        token = None
        reducer.ids.clear()
        reducer.links.clear()
        abort(ws)


async def discover(token, module=None):
    module = module or importlib.import_module("websockets")
    if getattr(module, "__version__", None) != "16.1.1":
        dependency_reject("pe4_websockets", "import_api", "TRUST_ANCHOR_CHANGED")
    connect = getattr(module, "connect", None)
    if not inspect.isclass(connect) or not callable(getattr(connect, "process_redirect", None)):
        dependency_reject("pe4_websockets", "import_api")
    class NoRedirect(connect):
        def process_redirect(self, exc):
            return exc
    deadline = time.monotonic() + TOTAL_BUDGET
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    ws = None
    try:
        await bounded(lambda: asyncio.get_running_loop().sock_connect(sock, ("192.168.100.251", 8123)), deadline, CONNECT_TIMEOUT, "INTERFACE_DISCOVERY", sock.close)
        # Numeric AF_INET tuple and preconnected socket: no getaddrinfo/DNS.
        logger = logging.Logger("hioc_discovery_silent", level=logging.CRITICAL + 1)
        ws = await bounded(lambda: NoRedirect(
            "ws://192.168.100.251:8123/api/websocket", sock=sock, proxy=None,
            open_timeout=time_left(deadline, CONNECT_TIMEOUT, "INTERFACE_DISCOVERY"),
            close_timeout=CLOSE_TIMEOUT, max_size=MAX_MESSAGE, max_queue=1,
            compression=None, ping_interval=None, logger=logger),
            deadline, CONNECT_TIMEOUT, "INTERFACE_DISCOVERY", sock.close)
        return await exchange(ws, token, deadline)
    except Failure:
        raise
    except Exception as exc:
        if any(getattr(getattr(exc, side, None), "code", None) == 1009 for side in ("rcvd", "sent")):
            reject("SCHEMA_DISCOVERY", "UNEXPECTED_SCHEMA")
        reject("INTERFACE_DISCOVERY", "UNSUPPORTED_INTERFACE")
    finally:
        token = None
        if ws is not None:
            abort(ws)
        sock.close()


def preflight(argv):
    if argv or os.name != "posix" or socket.gethostname() != "nutandpihole":
        reject("TARGET_IDENTITY", "WRONG_TARGET")
    import pwd
    if pwd.getpwuid(os.geteuid()).pw_name != "jazofv1":
        reject("TARGET_IDENTITY", "WRONG_OPERATOR")
    try:
        addresses = subprocess.run(["/usr/sbin/ip", "-o", "-4", "addr", "show"],
            capture_output=True, text=True, timeout=2, stdin=subprocess.DEVNULL, check=True).stdout
    except (OSError, subprocess.SubprocessError):
        dependency_reject("iproute", "address_output", "DEPENDENCY_UNAVAILABLE")
    if not re.search(r"\binet 192\.168\.100\.252/", addresses):
        reject("TARGET_IDENTITY", "WRONG_TARGET")
    environment = "/home/jazofv1/hioc/runtime/pe4/environments/cpython311-websockets16.1.1-lock-v1"
    if sys.version_info[:3] != (3, 11, 2) or os.path.realpath(sys.prefix) != environment:
        dependency_reject("pe4_python", "runtime_identity", "TRUST_ANCHOR_CHANGED")
    if not sys.flags.isolated or not sys.flags.dont_write_bytecode:
        reject("INTERFACE_DISCOVERY", "UNSUPPORTED_INTERFACE")
    if any(os.environ.get(k, "").strip() for k in os.environ if k.lower() in {"http_proxy", "https_proxy", "all_proxy", "no_proxy"}):
        reject("INTERFACE_DISCOVERY", "UNSUPPORTED_INTERFACE")
    try:
        module = importlib.import_module("websockets")
    except Exception:
        dependency_reject("pe4_websockets", "import_api", "DEPENDENCY_UNAVAILABLE")
    if (module.__version__ != "16.1.1" or not os.path.realpath(module.__file__).startswith(environment + "/lib/python3.11/site-packages/websockets/")):
        dependency_reject("pe4_websockets", "import_api", "TRUST_ANCHOR_CHANGED")
    if not sys.stdin.isatty() or not sys.stderr.isatty():
        reject("AUTHENTICATION", "AUTHENTICATION_UNAVAILABLE")


def acquire_token(prompt=None):
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", getpass.GetPassWarning)
            token = (prompt or getpass.getpass)("Home Assistant access token: ")
    except (getpass.GetPassWarning, EOFError, OSError, KeyboardInterrupt):
        reject("AUTHENTICATION", "AUTHENTICATION_UNAVAILABLE")
    if type(token) is not str or not token or len(token) > 8192 or "\n" in token or "\r" in token:
        reject("AUTHENTICATION", "AUTHENTICATION_UNAVAILABLE")
    return token


def publish_files(directory_fd, report, ops=os, guard=lambda: None):
    """Private directory fd; hard-link publish is atomic and refuses overwrite.

    Result is linked last, after durable report publication. No rename/replace.
    On interruption only our unpublished temporary name is removed.
    """
    payload = validate_report(report)
    directory_info = ops.fstat(directory_fd)
    if (not stat.S_ISDIR(directory_info.st_mode)
            or stat.S_IMODE(directory_info.st_mode) != 0o700
            or directory_info.st_uid != ops.geteuid()):
        reject("EVIDENCE_PUBLICATION", "EVIDENCE_PUBLICATION_FAILED")
    result = (f'RESULT={report["result"]}\nERROR_CODE={report["ERROR_CODE"]}\n'
              f'FAILURE_STAGE={report["FAILURE_STAGE"]}\nPRIVACY_VALIDATION=PASS\n').encode("ascii")
    for name, data in (("discovery-report.json", payload), ("discovery-result.txt", result)):
        temporary = ".publish-" + secrets.token_hex(8)
        fd = None
        created = False
        linked_result = False
        try:
            guard()
            fd = ops.open(temporary, ops.O_WRONLY | ops.O_CREAT | ops.O_EXCL | ops.O_NOFOLLOW,
                          0o600, dir_fd=directory_fd)
            created = True
            ops.fchmod(fd, 0o600)
            metadata = ops.fstat(fd)
            if not stat.S_ISREG(metadata.st_mode) or stat.S_IMODE(metadata.st_mode) != 0o600 or metadata.st_uid != ops.geteuid() or metadata.st_gid != ops.getegid():
                reject("EVIDENCE_PUBLICATION", "EVIDENCE_PUBLICATION_FAILED")
            view = memoryview(data)
            while view:
                n = ops.write(fd, view)
                if n <= 0:
                    raise OSError("write failed")
                view = view[n:]
            ops.fsync(fd)
            ops.close(fd)
            fd = None
            guard()
            ops.link(temporary, name, src_dir_fd=directory_fd, dst_dir_fd=directory_fd, follow_symlinks=False)
            linked_result = name == "discovery-result.txt"
            ops.unlink(temporary, dir_fd=directory_fd)
            created = False
            ops.fsync(directory_fd)
            guard()
        except BaseException:
            # Withdraw our completion marker if its durability could not be
            # confirmed. Never remove an existing/colliding evidence name.
            if linked_result:
                ops.unlink(name, dir_fd=directory_fd)
                ops.fsync(directory_fd)
            raise
        finally:
            if fd is not None:
                ops.close(fd)
            if created:
                ops.unlink(temporary, dir_fd=directory_fd)


def publish(report):
    validate_report(report)
    parent = fd = None
    try:
        parent = os.open("/tmp", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        parent_info = os.fstat(parent)
        named_parent = os.stat("/tmp", follow_symlinks=False)
        if ((parent_info.st_dev, parent_info.st_ino) != (named_parent.st_dev, named_parent.st_ino)
                or parent_info.st_uid != 0 or parent_info.st_gid != 0
                or stat.S_IMODE(parent_info.st_mode) != 0o1777):
            reject("EVIDENCE_PUBLICATION", "EVIDENCE_PUBLICATION_FAILED")
        # One name, one mkdir; collision stops without alternate-name adoption.
        name = "hioc-pe4-ha-discovery-" + secrets.token_hex(4)
        os.mkdir(name, 0o700, dir_fd=parent)
        fd = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent)
        info = os.fstat(fd)
        named = os.stat(name, dir_fd=parent, follow_symlinks=False)
        if ((info.st_dev, info.st_ino) != (named.st_dev, named.st_ino)
                or info.st_uid != os.geteuid() or info.st_gid != os.getegid()
                or stat.S_IMODE(info.st_mode) != 0o700):
            reject("EVIDENCE_PUBLICATION", "EVIDENCE_PUBLICATION_FAILED")
        os.fsync(fd)
        os.fsync(parent)
        def guard():
            final = os.stat(name, dir_fd=parent, follow_symlinks=False)
            descriptor = os.fstat(fd)
            identity = lambda i: (i.st_dev, i.st_ino, i.st_uid, i.st_gid, i.st_mode)
            if identity(final) != identity(info) or identity(descriptor) != identity(info):
                reject("EVIDENCE_PUBLICATION", "EVIDENCE_PUBLICATION_FAILED")
        publish_files(fd, report, guard=guard)
    except (OSError, Failure):
        reject("EVIDENCE_PUBLICATION", "EVIDENCE_PUBLICATION_FAILED")
    finally:
        if fd is not None:
            os.close(fd)
        if parent is not None:
            os.close(parent)


def record_compatibility(report):
    if os.name != "posix":
        return None  # Windows synthetic tests never touch production state.
    from pathlib import Path
    source_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(source_root / "pi4" / "lib"))
    try:
        from hioc.core.compatibility import refresh_status, observation_from_ha
        from hioc.core.state import StateStore
        from hioc.runtime import now_iso
        home = Path("/home/jazofv1/hioc")
        meta = report.get("compatibility", {})
        dependency = meta.get("dependency_id", "ha_core")
        if dependency == "ha_core":
            observation = observation_from_ha(report)
        else:
            capability_sets = {"pe4_python": {"interpreter_start": None, "runtime_api": False},
                "pe4_websockets": {"import_api": False, "bounded_connect": None},
                "iproute": {"address_route_neighbor": False, "socket_columns": None}}
            observation = {"available": meta.get("status") != "DEPENDENCY_UNAVAILABLE",
                "identity_matches": False if meta.get("status") == "TRUST_ANCHOR_CHANGED" else None,
                "capabilities": capability_sets[dependency]}
        return refresh_status(StateStore(home / "state" / "platform"), source_root,
            {dependency: observation}, now_iso(), source_root)
    finally:
        sys.path.pop(0)


def run(argv=None, output=print):
    token = None
    ready = False
    publishing = False
    try:
        preflight(sys.argv[1:] if argv is None else argv)
        ready = True
        token = acquire_token()
        report = asyncio.run(discover(token))
        token = None
        publishing = True
        publish(report)
        try:
            record_compatibility(report)
        except Exception:
            output("Compatibility state unavailable; sanitized discovery evidence remains authoritative.")
        output("RESULT=PASS\nERROR_CODE=NONE\nFAILURE_STAGE=COMPLETE\nPRIVACY_VALIDATION=PASS")
        return 0
    except Failure as exc:
        if ready and not publishing:
            try:
                failure_report = base_report(exc.code, exc.stage)
                if exc.compatibility is not None:
                    failure_report["compatibility"] = exc.compatibility
                publish(failure_report)
                try:
                    record_compatibility(failure_report)
                except Exception:
                    output("Compatibility state unavailable; sanitized failure evidence remains authoritative.")
            except (OSError, Failure):
                exc = Failure("EVIDENCE_PUBLICATION_FAILED", "EVIDENCE_PUBLICATION")
        output(f"RESULT=FAIL\nERROR_CODE={exc.code}\nFAILURE_STAGE={exc.stage}")
        if exc.compatibility is not None:
            meta = exc.compatibility
            output(f"Compatibility issue: {meta['dependency_id']}; {meta['status']}; version={meta['observed_version'] or 'unknown'}; capability={meta['failed_capability']}. Review the dependency contract. No update cause is established.")
        return 1
    except (KeyboardInterrupt, asyncio.CancelledError):
        # Publication cleans only invocation-owned unpublished temporary files;
        # an interruption never initiates a second publication attempt.
        output("RESULT=FAIL\nERROR_CODE=UNEXPECTED_ERROR\nFAILURE_STAGE=INTERFACE_DISCOVERY")
        return 130
    except Exception:
        output("RESULT=FAIL\nERROR_CODE=UNEXPECTED_ERROR\nFAILURE_STAGE=INTERFACE_DISCOVERY")
        return 1
    finally:
        token = None


if __name__ == "__main__":
    raise SystemExit(run())
