"""Private, pure PE-5.1 ownership resolver. No collection, publication or state I/O."""
import hashlib
import json
import math
import re
from datetime import datetime, timezone

from .inventory import normalize_mac, stable_device_id

SCHEMA_VERSION = "1.0"
MAX_RECORDS = 4096
MAX_SNAPSHOT_BYTES = 16 * 1024 * 1024
MAX_POLICY_INTEGER = 2 ** 53 - 1
SOURCES = ("systemd", "ss")
SERVICE_TYPES = ("mqtt", "dns", "dhcp", "ups", "ssh", "scheduler")
DEVICE_PATTERN = r"^dev_[0-9a-f]{16}$"
SERVICE_PATTERN = r"^(?:svc_(?:mqtt|dns|dhcp|ups|ssh|scheduler)_[0-9a-f]{8}|svc_mqtt_listener|svc_network_(?:53|67))$"
TIMESTAMP_PATTERN = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})$"
SERVICE_FIELDS = frozenset(("id", "name", "type", "device_id", "status", "source", "port", "host", "dependency"))
REJECTION_CODES = (
    "MALFORMED_SERVICE", "UNEXPECTED_SERVICE_FIELD", "INVALID_SERVICE_ID",
    "UNSUPPORTED_SOURCE", "UNSUPPORTED_SERVICE_TYPE", "SOURCE_ID_TYPE_MISMATCH",
    "CONFLICTING_SERVICE_ID", "MISSING_OWNER", "WEAK_OWNER", "AMBIGUOUS_OWNER",
    "MALFORMED_DEVICE", "MALFORMED_MAC", "OWNER_MAC_COLLISION", "OWNER_ID_MISMATCH",
)


class ServiceAssociationError(ValueError):
    """Whole-contract failure. Messages contain only fixed safe error codes."""
    def __init__(self, code):
        self.code = code
        super().__init__(code)


def _fail(code):
    raise ServiceAssociationError(code)


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def _hash(value):
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _json_input(value, depth=0):
    if depth > 32:
        _fail("SNAPSHOT_INVALID")
    kind = type(value)
    if value is None or kind in (str, bool, int):
        return
    if kind is float and math.isfinite(value):
        return
    if kind is dict and all(type(key) is str for key in value):
        for child in value.values():
            _json_input(child, depth + 1)
        return
    if kind is list:
        for child in value:
            _json_input(child, depth + 1)
        return
    _fail("SNAPSHOT_INVALID")


def _time(value, code):
    if type(value) is not str or not re.fullmatch(TIMESTAMP_PATTERN, value):
        _fail(code)
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.astimezone(timezone.utc)
    except (ValueError, OverflowError):
        _fail(code)


def _time_text(value):
    return value.isoformat(timespec="microseconds").replace("+00:00", "Z")


def _policy(value):
    if type(value) is not int or not 0 <= value <= MAX_POLICY_INTEGER:
        _fail("INVALID_MAX_SNAPSHOT_AGE")


def _freshness(updated, evaluated, maximum):
    if updated > evaluated:
        _fail("SNAPSHOT_FUTURE")
    age = evaluated - updated
    whole_seconds = age.days * 86400 + age.seconds
    if whole_seconds > maximum or (whole_seconds == maximum and age.microseconds):
        _fail("SNAPSHOT_STALE")


def _safe_service_id(value):
    return value if type(value) is str and re.fullmatch(SERVICE_PATTERN, value) else None


def _association_id(service_id, owner, source):
    return "lsa_" + _hash([service_id, owner, source])


def _service_reason(record):
    if type(record) is not dict:
        return "MALFORMED_SERVICE"
    if set(record) - SERVICE_FIELDS:
        return "UNEXPECTED_SERVICE_FIELD"
    if _safe_service_id(record.get("id")) is None:
        return "INVALID_SERVICE_ID"
    if type(record.get("source")) is not str or record["source"] not in SOURCES:
        return "UNSUPPORTED_SOURCE"
    if type(record.get("type")) is not str or record["type"] not in SERVICE_TYPES:
        return "UNSUPPORTED_SERVICE_TYPE"
    if type(record.get("device_id")) is not str or not re.fullmatch(DEVICE_PATTERN, record["device_id"]):
        return "MALFORMED_SERVICE"
    for key in ("name", "status", "host", "dependency"):
        if key in record and (type(record[key]) is not str or len(record[key]) > 1024):
            return "MALFORMED_SERVICE"
    if "port" in record and (type(record["port"]) is not int or not 1 <= record["port"] <= 65535):
        return "MALFORMED_SERVICE"
    sid, source, service_type = record["id"], record["source"], record["type"]
    if source == "systemd":
        if not re.fullmatch(r"svc_" + service_type + r"_[0-9a-f]{8}", sid):
            return "SOURCE_ID_TYPE_MISMATCH"
    else:
        expected = {"svc_mqtt_listener": ("mqtt", 1883), "svc_network_53": ("dns", 53), "svc_network_67": ("dhcp", 67)}
        if sid not in expected or expected[sid] != (service_type, record.get("port")):
            return "SOURCE_ID_TYPE_MISMATCH"
    return None


def _owners(devices):
    by_id, by_mac = {}, {}
    for device in devices:
        if type(device) is not dict or type(device.get("id")) is not str or not re.fullmatch(DEVICE_PATTERN, device["id"]):
            # Without an identifiable device record global owner uniqueness cannot be established.
            _fail("SNAPSHOT_DEVICE_INVALID")
        by_id.setdefault(device["id"], []).append(device)
        mac = device.get("mac")
        if type(mac) is str and normalize_mac(mac):
            by_mac.setdefault(normalize_mac(mac), []).append(device)
    return by_id, by_mac


def _owner_reason(owner_id, by_id, by_mac):
    matches = by_id.get(owner_id, [])
    if not matches:
        return "MISSING_OWNER"
    if len(matches) != 1:
        return "AMBIGUOUS_OWNER"
    device = matches[0]
    raw_mac = device.get("mac", "")
    if type(raw_mac) is not str:
        return "MALFORMED_DEVICE"
    if not raw_mac.strip():
        return "WEAK_OWNER"
    mac = normalize_mac(raw_mac)
    if not mac:
        return "MALFORMED_MAC"
    if len(by_mac[mac]) != 1:
        return "OWNER_MAC_COLLISION"
    if stable_device_id({"mac": mac}) != owner_id:
        return "OWNER_ID_MISMATCH"
    return None


def _rejection_order(item):
    return (item["service_id"] or "", item["reason"], item["owner_reference"] or "", item["source_type"] or "")


def _rejection(service_id, reason, records, provenance):
    def unique_reference(field, allowed):
        values = [record.get(field) if type(record) is dict else None for record in records]
        if values and all(allowed(value) for value in values) and len(set(values)) == 1:
            return values[0]
        return None
    return {
        "service_id": service_id, "reason": reason,
        "owner_reference": unique_reference("device_id", lambda v: type(v) is str and re.fullmatch(DEVICE_PATTERN, v)),
        "source_type": unique_reference("source", lambda v: type(v) is str and v in SOURCES),
        "collection_provenance": dict(provenance),
    }


def resolve_service_associations(snapshot, evaluated_at, max_snapshot_age_seconds):
    """Return a new private envelope, or raise a safe whole-input error.

    Identical consumed service tuples deduplicate. Any same-ID disagreement in
    owner/source/type or malformed same-ID evidence rejects the entire ID group.
    Empty services produce no accepted/rejected relationship claims and do not
    establish collection success, absence, availability or health.
    """
    _policy(max_snapshot_age_seconds)
    evaluated = _time(evaluated_at, "INVALID_EVALUATION_TIME")
    if type(snapshot) is not dict:
        _fail("SNAPSHOT_INVALID")
    required = {"schema_version": str, "updated": str, "devices": list, "services": list, "topology": dict, "dependencies": dict, "summary": dict}
    if any(type(snapshot.get(key)) is not kind for key, kind in required.items()) or snapshot["schema_version"] != "1.0":
        _fail("SNAPSHOT_INVALID")
    _json_input(snapshot)
    if len(snapshot["devices"]) > MAX_RECORDS or len(snapshot["services"]) > MAX_RECORDS:
        _fail("SNAPSHOT_LIMIT_EXCEEDED")
    try:
        encoded_size = len(_canonical(snapshot).encode("utf-8"))
    except (ValueError, RecursionError):
        _fail("SNAPSHOT_INVALID")
    if encoded_size > MAX_SNAPSHOT_BYTES:
        _fail("SNAPSHOT_LIMIT_EXCEEDED")
    updated = _time(snapshot["updated"], "INVALID_SNAPSHOT_TIME")
    _freshness(updated, evaluated, max_snapshot_age_seconds)
    by_id, by_mac = _owners(snapshot["devices"])
    # Canonical snapshot provenance ignores top-level record ordering, never edits input.
    reference = dict(snapshot)
    for key in ("devices", "services"):
        reference[key] = sorted(snapshot[key], key=_canonical)
    snapshot_hash = _hash(reference)
    provenance = {"inventory_updated": _time_text(updated), "inventory_snapshot_sha256": snapshot_hash}
    groups, rejections, associations = {}, [], []
    for record in snapshot["services"]:
        sid = _safe_service_id(record.get("id")) if type(record) is dict else None
        reason = _service_reason(record)
        if sid is None:
            rejections.append(_rejection(None, reason or "INVALID_SERVICE_ID", [record], provenance))
        else:
            groups.setdefault(sid, []).append((record, reason))
    for sid in sorted(groups):
        group = groups[sid]
        tuples = {_canonical([record.get("device_id"), record.get("source"), record.get("type")]) for record, _ in group}
        invalid = {reason for _, reason in group if reason}
        if len(tuples) > 1 or (invalid and any(reason is None for _, reason in group)):
            reason = "CONFLICTING_SERVICE_ID"
        elif invalid:
            reason = sorted(invalid)[0]
        else:
            record = group[0][0]
            reason = _owner_reason(record["device_id"], by_id, by_mac)
        if reason:
            rejections.append(_rejection(sid, reason, [record for record, _ in group], provenance))
            continue
        record = group[0][0]
        associations.append({
            "association_id": _association_id(sid, record["device_id"], record["source"]),
            "service_id": sid, "stable_device_id": record["device_id"],
            "service_type": record["type"], "source_type": record["source"],
            "association_basis": "existing_service_ownership", "confidence": "high",
            "collection_provenance": dict(provenance),
        })
    associations.sort(key=lambda item: item["association_id"])
    rejections.sort(key=_rejection_order)
    result = {
        "schema_version": SCHEMA_VERSION, "inventory_updated": _time_text(updated),
        "evaluated_at": _time_text(evaluated), "max_snapshot_age_seconds": max_snapshot_age_seconds,
        "association_count": len(associations), "service_associations": associations,
        "rejection_count": len(rejections), "rejections": rejections,
    }
    validate_service_association_envelope(result)
    return result


def contract_schema():
    """Construct a fresh closed schema without reading a schema/configuration file."""
    def obj(fields):
        return {"type": "object", "additionalProperties": False, "required": sorted(fields), "properties": fields}
    text = lambda pattern: {"type": "string", "pattern": pattern}
    time_field = {"type": "string", "pattern": TIMESTAMP_PATTERN, "format": "date-time", "maxLength": 32}
    provenance = obj({"inventory_updated": dict(time_field), "inventory_snapshot_sha256": text(r"^[0-9a-f]{64}$")})
    association = obj({
        "association_id": text(r"^lsa_[0-9a-f]{64}$"), "service_id": text(SERVICE_PATTERN),
        "stable_device_id": text(DEVICE_PATTERN), "service_type": {"enum": list(SERVICE_TYPES)},
        "source_type": {"enum": list(SOURCES)}, "association_basis": {"const": "existing_service_ownership"},
        "confidence": {"const": "high"}, "collection_provenance": provenance,
    })
    rejection = obj({"service_id": {"type": ["string", "null"], "pattern": SERVICE_PATTERN}, "reason": {"enum": list(REJECTION_CODES)}, "owner_reference": {"type": ["string", "null"], "pattern": DEVICE_PATTERN}, "source_type": {"enum": [None, *SOURCES]}, "collection_provenance": provenance})
    root = obj({
        "schema_version": {"const": SCHEMA_VERSION}, "inventory_updated": dict(time_field),
        "evaluated_at": dict(time_field), "max_snapshot_age_seconds": {"type": "integer", "minimum": 0, "maximum": MAX_POLICY_INTEGER},
        "association_count": {"type": "integer", "minimum": 0, "maximum": MAX_RECORDS},
        "service_associations": {"type": "array", "maxItems": MAX_RECORDS, "uniqueItems": True, "items": association},
        "rejection_count": {"type": "integer", "minimum": 0, "maximum": MAX_RECORDS},
        "rejections": {"type": "array", "maxItems": MAX_RECORDS, "items": rejection},
    })
    return {"$schema": "https://json-schema.org/draft/2020-12/schema", "title": "PE-5.1 private local service association envelope", **root}


def _shape(value, schema):
    expected = schema.get("type")
    types = {"object": dict, "array": list, "string": str, "integer": int, "null": type(None)}
    if expected and type(value) not in [types[name] for name in ([expected] if type(expected) is str else expected)]:
        _fail("ENVELOPE_INVALID")
    if "const" in schema and (type(value) is not type(schema["const"]) or value != schema["const"]):
        _fail("ENVELOPE_INVALID")
    if "enum" in schema and value not in schema["enum"]:
        _fail("ENVELOPE_INVALID")
    if type(value) is dict:
        if set(value) != set(schema["required"]):
            _fail("ENVELOPE_INVALID")
        for key, child in schema["properties"].items():
            _shape(value[key], child)
    if type(value) is list:
        if len(value) > schema["maxItems"]:
            _fail("ENVELOPE_INVALID")
        for item in value:
            _shape(item, schema["items"])
        if schema.get("uniqueItems") and len({_canonical(item) for item in value}) != len(value):
            _fail("ENVELOPE_INVALID")
    if type(value) is str and (("pattern" in schema and not re.fullmatch(schema["pattern"], value)) or len(value) > schema.get("maxLength", 1024)):
        _fail("ENVELOPE_INVALID")
    if type(value) is int and not schema.get("minimum", value) <= value <= schema.get("maximum", value):
        _fail("ENVELOPE_INVALID")


def validate_service_association_envelope(envelope):
    """Validate closed shape plus freshness, identities, counts and uniqueness."""
    try:
        _json_input(envelope)
    except ServiceAssociationError:
        _fail("ENVELOPE_INVALID")
    _shape(envelope, contract_schema())
    updated = _time(envelope["inventory_updated"], "ENVELOPE_INVALID")
    evaluated = _time(envelope["evaluated_at"], "ENVELOPE_INVALID")
    _policy(envelope["max_snapshot_age_seconds"])
    _freshness(updated, evaluated, envelope["max_snapshot_age_seconds"])
    if envelope["association_count"] + envelope["rejection_count"] > MAX_RECORDS or envelope["association_count"] != len(envelope["service_associations"]) or envelope["rejection_count"] != len(envelope["rejections"]):
        _fail("ENVELOPE_INVALID")
    ids, rejected_ids, snapshots = set(), set(), set()
    for item in envelope["service_associations"]:
        sid = item["service_id"]
        if sid in ids or item["association_id"] != _association_id(sid, item["stable_device_id"], item["source_type"]):
            _fail("ENVELOPE_INVALID")
        probe = {"id": sid, "device_id": item["stable_device_id"], "source": item["source_type"], "type": item["service_type"]}
        if probe["source"] == "ss":
            probe["port"] = {"svc_mqtt_listener": 1883, "svc_network_53": 53, "svc_network_67": 67}.get(sid)
        if _service_reason(probe):
            _fail("ENVELOPE_INVALID")
        ids.add(sid)
        p = item["collection_provenance"]
        if p["inventory_updated"] != envelope["inventory_updated"]:
            _fail("ENVELOPE_INVALID")
        snapshots.add(p["inventory_snapshot_sha256"])
    for item in envelope["rejections"]:
        p = item["collection_provenance"]
        if p["inventory_updated"] != envelope["inventory_updated"]:
            _fail("ENVELOPE_INVALID")
        snapshots.add(p["inventory_snapshot_sha256"])
        sid = item["service_id"]
        if sid is not None:
            if sid in ids or sid in rejected_ids:
                _fail("ENVELOPE_INVALID")
            rejected_ids.add(sid)
    if len(snapshots) > 1 or envelope["service_associations"] != sorted(envelope["service_associations"], key=lambda item: item["association_id"]) or envelope["rejections"] != sorted(envelope["rejections"], key=_rejection_order):
        _fail("ENVELOPE_INVALID")
