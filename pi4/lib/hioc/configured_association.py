"""PE-5 configured relationships: pure local evidence, no collection or publication."""
import hashlib
import json
import math
import re
from datetime import timedelta

from . import service_association as local
from .configured_association_schemas import schemas

SOURCE_LIMIT = 262144
OUTPUT_LIMIT = 16777216
INVENTORY_POLICY = 2100
HANDOFF_SECONDS = 1200


class AssociationError(ValueError):
    """Fixed safe codes only; never echo private input."""
    def __init__(self, code, phase=None):
        self.code, self.phase = code, phase
        super().__init__(code)


def fail(code):
    raise AssociationError(code)


def canonical(value):
    try:
        return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
                           allow_nan=False) + "\n").encode("ascii")
    except (ValueError, TypeError, RecursionError, UnicodeError):
        fail("SOURCE_SCHEMA_INVALID")


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def strict_json(raw, maximum, code="SOURCE_SCHEMA_INVALID"):
    if type(raw) is not bytes or len(raw) > maximum:
        fail(code)
    def unique(pairs):
        value = {}
        for key, child in pairs:
            if key in value:
                fail(code)
            value[key] = child
        return value
    def invalid(value):
        fail(code)
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=unique, parse_constant=invalid)
        local._json_input(value)
        return value
    except AssociationError:
        raise
    except (UnicodeError, ValueError, TypeError, RecursionError):
        fail(code)


def shape(value, schema, code="SOURCE_SCHEMA_INVALID"):
    if "anyOf" in schema:
        for option in schema["anyOf"]:
            try:
                shape(value, option, code)
                return
            except AssociationError:
                pass
        fail(code)
    if "const" in schema and (type(value) is not type(schema["const"]) or value != schema["const"]):
        fail(code)
    if "enum" in schema and not any(type(value) is type(x) and value == x for x in schema["enum"]):
        fail(code)
    kinds = {"object": dict, "array": list, "string": str, "integer": int,
             "boolean": bool, "null": type(None)}
    expected = schema.get("type")
    if expected:
        names = expected if type(expected) is list else [expected]
        if type(value) not in [kinds[x] for x in names]:
            fail(code)
    if type(value) is dict:
        if not set(schema.get("required", [])) <= set(value):
            fail(code)
        if schema.get("additionalProperties") is False and set(value) != set(schema["properties"]):
            fail(code)
        for key, child in value.items():
            if key in schema.get("properties", {}):
                shape(child, schema["properties"][key], code)
    if type(value) is list:
        if not schema.get("minItems", 0) <= len(value) <= schema.get("maxItems", len(value)):
            fail(code)
        for child in value:
            shape(child, schema.get("items", {}), code)
        if schema.get("uniqueItems") and len({canonical(x) for x in value}) != len(value):
            fail(code)
    if type(value) is str:
        if len(value) > schema.get("maxLength", 1024):
            fail(code)
        if "pattern" in schema and not re.fullmatch(schema["pattern"], value):
            fail(code)
        if schema.get("format") == "date-time":
            try:
                local._time(value, code)
            except local.ServiceAssociationError:
                fail(code)
    if type(value) is int and not schema.get("minimum", value) <= value <= schema.get("maximum", value):
        fail(code)


def validate_source(value):
    if type(value) is dict and type(value.get("mappings")) is list:
        rows = value["mappings"]
        if len(rows) <= 4096 and len({canonical(x) for x in rows}) != len(rows):
            fail("SOURCE_DUPLICATE")
    shape(value, schemas()["input_schema"])
    if len(canonical(value)) > SOURCE_LIMIT:
        fail("SOURCE_SCHEMA_INVALID")
    mapping_ids, endpoints = set(), {}
    for row in value["mappings"]:
        mid, endpoint = row["mapping_id"], row["endpoint_id"]
        if mid in mapping_ids:
            fail("SOURCE_DUPLICATE")
        mapping_ids.add(mid)
        if endpoint in endpoints:
            if endpoints[endpoint] != (row["device_id"], row["service_id"]):
                fail("SOURCE_CONFLICT")
            fail("SOURCE_DUPLICATE")
        endpoints[endpoint] = (row["device_id"], row["service_id"])
    return value


def check_revision(candidate, anchors):
    validate_source(candidate)
    for anchor in anchors:
        if anchor is None or anchor["source_revision"] is None:
            continue
        revision = anchor["source_revision"]
        if candidate["revision"] < revision:
            fail("SOURCE_REVISION_ROLLBACK")
        if candidate["revision"] == revision and digest(candidate) != anchor["sha256"]:
            fail("SOURCE_REVISION_CONFLICT")


def relationship_id(row):
    values = ["configured_mqtt_v1", "operator_mqtt_v1", row["endpoint_id"], row["device_id"],
              row["service_id"], "endpoint_to_device"]
    return "mqra_" + hashlib.sha256(canonical(values)[:-1]).hexdigest()


def unavailable(code):
    return dict(state="UNAVAILABLE", source_id="operator_mqtt_v1", revision=None,
                source_sha256=None, candidate_count=0, associations=[], rejections=[], error_code=code)


def resolve_configured(source, inventory):
    validate_source(source)
    try:
        by_id, by_mac = local._owners(inventory["devices"])
    except (KeyError, TypeError, local.ServiceAssociationError):
        fail("INVENTORY_INVALID")
    owner_codes = {"MISSING_OWNER": "MISSING_DEVICE", "WEAK_OWNER": "WEAK_DEVICE",
                   "AMBIGUOUS_OWNER": "AMBIGUOUS_DEVICE", "MALFORMED_DEVICE": "WEAK_DEVICE",
                   "MALFORMED_MAC": "WEAK_DEVICE", "OWNER_MAC_COLLISION": "MAC_COLLISION",
                   "OWNER_ID_MISMATCH": "DEVICE_ID_MISMATCH"}
    services = {}
    for service in inventory["services"]:
        if type(service) is dict and type(service.get("id")) is str:
            services.setdefault(service["id"], []).append(service)
    accepted, rejected = [], []
    source_sha = digest(source)
    for row in source["mappings"]:
        reason = local._owner_reason(row["device_id"], by_id, by_mac)
        code = owner_codes.get(reason)
        if code is None and row["service_id"] is not None:
            matches = services.get(row["service_id"], [])
            if not matches:
                code = "MISSING_SERVICE"
            elif len(matches) != 1:
                code = "AMBIGUOUS_SERVICE"
            elif matches[0].get("device_id") != row["device_id"]:
                code = "SERVICE_OWNER_MISMATCH"
        if code:
            rejected.append(dict(mapping_id=row["mapping_id"], code=code))
            continue
        accepted.append(dict(row, relationship_id=relationship_id(row), direction="endpoint_to_device",
                             source_kind="configured_mqtt", source_id="operator_mqtt_v1",
                             source_revision=source["revision"], source_sha256=source_sha,
                             rule_id="declared_endpoint_device_v1"))
    return dict(state="VALID", source_id="operator_mqtt_v1", revision=source["revision"],
                source_sha256=source_sha, candidate_count=len(source["mappings"]),
                associations=sorted(accepted, key=lambda x: x["relationship_id"]),
                rejections=sorted(rejected, key=lambda x: (x["mapping_id"], x["code"])), error_code=None)


def inventory_digest(snapshot):
    reference = dict(snapshot)
    for key in ("devices", "services"):
        reference[key] = sorted(snapshot[key], key=local._canonical)
    return local._hash(reference)


def no_changes():
    return dict(baseline=False, added=[], removed=[], added_count=0, removed_count=0, truncated=False)


def compose(inventory, source, evaluated_at, prior=None, source_error=None):
    try:
        now = local._time(evaluated_at, "CLOCK_INVALID")
    except local.ServiceAssociationError:
        fail("CLOCK_INVALID")
    evaluated = local._time_text(now)
    if prior is not None:
        validate_envelope(prior)
        if now < local._time(prior["evaluated_at"], "CLOCK_INVALID"):
            fail("CLOCK_INVALID")
    result = dict(schema_version="2.0", state="UNAVAILABLE", evaluated_at=evaluated,
                  valid_until=evaluated, inventory=None, local=None,
                  configured=unavailable("INVENTORY_INVALID"), changes=no_changes())
    try:
        evidence = local.resolve_service_associations(inventory, evaluated, INVENTORY_POLICY)
        updated = local._time(evidence["inventory_updated"], "INVENTORY_INVALID")
        deadline = min(now + timedelta(seconds=HANDOFF_SECONDS), updated + timedelta(seconds=INVENTORY_POLICY))
        if deadline <= now:
            fail("INVENTORY_STALE")
    except local.ServiceAssociationError as error:
        code = {"SNAPSHOT_STALE": "INVENTORY_STALE", "SNAPSHOT_FUTURE": "INVENTORY_FUTURE"}.get(error.code, "INVENTORY_INVALID")
        result["configured"] = unavailable(code)
        validate_envelope(result)
        return result
    except AssociationError as error:
        result["configured"] = unavailable(error.code)
        validate_envelope(result)
        return result
    result.update(state="VALID", valid_until=local._time_text(deadline),
                  inventory=dict(sha256=inventory_digest(inventory), updated=local._time_text(updated)),
                  local=evidence)
    if source_error:
        result["configured"] = unavailable(source_error)
    elif source is None:
        result["configured"] = unavailable("SOURCE_ABSENT")
    else:
        try:
            result["configured"] = resolve_configured(source, inventory)
        except AssociationError as error:
            result["configured"] = unavailable(error.code)
    if prior and result["configured"]["state"] == "VALID":
        try:
            validate_handoff(prior, inventory, source, evaluated)
            previous = {x["relationship_id"] for x in prior["configured"]["associations"]}
            current = {x["relationship_id"] for x in result["configured"]["associations"]}
            added, removed = sorted(current - previous), sorted(previous - current)
            result["changes"] = dict(baseline=True, added=added[:64], removed=removed[:64],
                                    added_count=len(added), removed_count=len(removed),
                                    truncated=len(added) > 64 or len(removed) > 64)
        except AssociationError:
            pass
    validate_envelope(result)
    return result


def validate_envelope(value):
    shape(value, schemas()["output_schema"], "PRIOR_STATE_INVALID")
    if len(canonical(value)) > OUTPUT_LIMIT:
        fail("PRIOR_STATE_INVALID")
    now = local._time(value["evaluated_at"], "PRIOR_STATE_INVALID")
    deadline = local._time(value["valid_until"], "PRIOR_STATE_INVALID")
    cfg, changes = value["configured"], value["changes"]
    if cfg["state"] == "VALID":
        if cfg["revision"] is None or cfg["source_sha256"] is None or cfg["error_code"] is not None:
            fail("PRIOR_STATE_INVALID")
        if cfg["candidate_count"] != len(cfg["associations"]) + len(cfg["rejections"]):
            fail("PRIOR_STATE_INVALID")
        mids, endpoints, rids = set(), set(), set()
        for row in cfg["associations"]:
            if (row["relationship_id"] != relationship_id(row) or row["mapping_id"] in mids
                    or row["endpoint_id"] in endpoints or row["relationship_id"] in rids
                    or row["source_revision"] != cfg["revision"] or row["source_sha256"] != cfg["source_sha256"]):
                fail("PRIOR_STATE_INVALID")
            mids.add(row["mapping_id"]); endpoints.add(row["endpoint_id"]); rids.add(row["relationship_id"])
        for row in cfg["rejections"]:
            if row["mapping_id"] is None or row["mapping_id"] in mids:
                fail("PRIOR_STATE_INVALID")
            mids.add(row["mapping_id"])
        if cfg["associations"] != sorted(cfg["associations"], key=lambda x: x["relationship_id"]):
            fail("PRIOR_STATE_INVALID")
        if cfg["rejections"] != sorted(cfg["rejections"], key=lambda x: (x["mapping_id"], x["code"])):
            fail("PRIOR_STATE_INVALID")
    elif (cfg["associations"] or cfg["rejections"] or cfg["candidate_count"] or cfg["revision"] is not None
          or cfg["source_sha256"] is not None or cfg["error_code"] is None):
        fail("PRIOR_STATE_INVALID")
    if value["state"] == "UNAVAILABLE":
        if value["local"] is not None or value["inventory"] is not None or cfg["state"] != "UNAVAILABLE" or deadline != now:
            fail("PRIOR_STATE_INVALID")
    else:
        if value["inventory"] is None or not now < deadline <= now + timedelta(seconds=HANDOFF_SECONDS):
            fail("PRIOR_STATE_INVALID")
        updated = local._time(value["inventory"]["updated"], "PRIOR_STATE_INVALID")
        if updated > now or deadline > updated + timedelta(seconds=INVENTORY_POLICY):
            fail("PRIOR_STATE_INVALID")
        if value["local"] is not None:
            try:
                local.validate_service_association_envelope(value["local"])
            except local.ServiceAssociationError:
                fail("PRIOR_STATE_INVALID")
            ev = value["local"]
            if ev["max_snapshot_age_seconds"] != INVENTORY_POLICY or ev["evaluated_at"] != value["evaluated_at"] or ev["inventory_updated"] != value["inventory"]["updated"]:
                fail("PRIOR_STATE_INVALID")
            for row in ev["service_associations"] + ev["rejections"]:
                if row["collection_provenance"]["inventory_snapshot_sha256"] != value["inventory"]["sha256"]:
                    fail("PRIOR_STATE_INVALID")
    if not changes["baseline"]:
        if changes != no_changes():
            fail("PRIOR_STATE_INVALID")
    else:
        if cfg["state"] != "VALID":
            fail("PRIOR_STATE_INVALID")
        for field in ("added", "removed"):
            count = changes[field + "_count"]
            if len(changes[field]) != min(64, count) or changes[field] != sorted(changes[field]):
                fail("PRIOR_STATE_INVALID")
        if set(changes["added"]) & set(changes["removed"]) or changes["truncated"] != (changes["added_count"] > 64 or changes["removed_count"] > 64):
            fail("PRIOR_STATE_INVALID")
    return value


def validate_handoff(value, inventory, source, evaluated_at):
    validate_envelope(value)
    try:
        now = local._time(evaluated_at, "CLOCK_INVALID")
        if (value["state"] != "VALID" or now < local._time(value["evaluated_at"], "CLOCK_INVALID")
                or now >= local._time(value["valid_until"], "CLOCK_INVALID")):
            fail("PRIOR_STATE_INVALID")
        evidence = local.resolve_service_associations(inventory, value["evaluated_at"], INVENTORY_POLICY)
        if inventory_digest(inventory) != value["inventory"]["sha256"] or value["local"] != evidence:
            fail("INVENTORY_INVALID")
        if value["configured"]["state"] == "VALID":
            if source is None or value["configured"] != resolve_configured(source, inventory):
                fail("SOURCE_CHANGED")
        return value
    except local.ServiceAssociationError:
        fail("INVENTORY_INVALID")
