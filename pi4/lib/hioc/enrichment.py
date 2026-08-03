import copy
import hashlib
import ipaddress
import json
import re
import unicodedata
from datetime import datetime
from pathlib import Path


SCHEMA_VERSION = "1.0"
GENERATOR = "hioc-inventory-engine"
FIELD = "hostname"
NORMALIZATION_RULE = "hostname_normalization_v1"

DEVICE_ID_RE = re.compile(r"^dev_[0-9a-f]{16}$")
CANDIDATE_ID_RE = re.compile(r"^hce_[0-9a-f]{20}$")
MAC_RE = re.compile(r"^[0-9a-f]{2}(?::[0-9a-f]{2}){5}$")
MAC_COMPACT_RE = re.compile(r"^[0-9a-f]{12}$")
DNS_LABEL_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$")
NONSTANDARD_LABEL_RE = re.compile(r"^[a-z0-9](?:[a-z0-9_-]{0,61}[a-z0-9])?$")
SAFE_INTEGRATION_RE = re.compile(r"^[a-z0-9][a-z0-9_.-]{0,63}$")

SOURCE_TYPES = {
    "configured_infrastructure",
    "trusted_integration",
    "direct_observation",
    "assignment_observation",
    "historical",
}
AUTHORITIES = {
    "configured_fact",
    "trusted_enrichment",
    "strong_observation",
    "weak_observation",
    "historical",
}
CONFIDENCES = {"authoritative", "high", "medium", "low", "unknown"}
QUALITIES = {"normal", "low", "placeholder", "invalid"}
STATES = {"active", "historical"}
CONFLICT_STATUSES = {"none", "agreement", "active_conflict", "historical_disagreement"}
EVIDENCE_STATUSES = {
    "selected",
    "selected_with_agreement",
    "selected_with_conflict",
    "no_valid_candidate",
    "no_evidence",
}
SELECTION_RULES = {
    "configured_fact",
    "trusted_integration",
    "local_host",
    "active_dhcp",
    "source_agreement",
    "historical_fallback",
    "no_valid_candidate",
}
STATUS_VALUES = {"online", "degraded", "error", "unavailable"}

AUTHORITY_RANK = {
    "configured_fact": 5,
    "trusted_enrichment": 4,
    "strong_observation": 3,
    "weak_observation": 2,
    "historical": 1,
}
CONFIDENCE_RANK = {"authoritative": 5, "high": 4, "medium": 3, "low": 2, "unknown": 1}
QUALITY_RANK = {"normal": 2, "low": 1, "placeholder": 0, "invalid": 0}
RULE_BY_AUTHORITY = {
    "configured_fact": "configured_fact",
    "trusted_enrichment": "trusted_integration",
    "strong_observation": "local_host",
    "weak_observation": "active_dhcp",
    "historical": "historical_fallback",
}

PLACEHOLDERS = {"unknown", "localhost", "localhost.localdomain"}
LOW_PATTERNS = (
    re.compile(r"^android-[a-z0-9]+$"),
    re.compile(r"^esp[_-][a-f0-9]+$"),
    re.compile(r"^desktop-[a-z0-9]+$"),
)
GENERIC_LOW_VALUES = {"android", "camera", "device", "printer", "router"}


class EnrichmentSchemaError(ValueError):
    pass


def _canonical_json(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _sha256_text(value: str, length: int) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:length]


def _parse_rfc3339(value: str) -> float:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("timestamp must be a nonempty string")
    return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()


def _safe_integration_stem(value: str) -> str:
    stem = unicodedata.normalize("NFC", str(value or "")).strip().lower()
    if SAFE_INTEGRATION_RE.fullmatch(stem):
        return stem
    return _sha256_text(stem, 12)


def _dhcp_source_id(value: str) -> str:
    normalized = str(Path(str(value or ""))).replace("\\", "/").lower()
    return f"dhcp_leases:{_sha256_text(normalized, 12)}"


def _source_descriptor(record: dict) -> dict | None:
    source = str(record.get("source", "") or "")
    enrichment_source = str(record.get("_enrichment_source", "") or "")
    hostname = record.get("hostname")
    if not isinstance(hostname, str):
        return None
    if source == "known_infrastructure" and record.get("_observed") is False:
        return {
            "source_id": "known_infrastructure",
            "source_type": "configured_infrastructure",
            "source_reference": None,
            "authority": "configured_fact",
            "confidence": "authoritative",
        }
    if enrichment_source.startswith("integration:") or source.startswith("integration:"):
        integration_source = enrichment_source if enrichment_source.startswith("integration:") else source
        stem = _safe_integration_stem(integration_source.split(":", 1)[1])
        return {
            "source_id": f"integration:{stem}",
            "source_type": "trusted_integration",
            "source_reference": stem,
            "authority": "trusted_enrichment",
            "confidence": "high",
        }
    if source == "local_host":
        return {
            "source_id": "local_host",
            "source_type": "direct_observation",
            "source_reference": None,
            "authority": "strong_observation",
            "confidence": "high",
        }
    if source == "dhcp_leases" and record.get("dhcp_lease_source"):
        source_id = _dhcp_source_id(record["dhcp_lease_source"])
        return {
            "source_id": source_id,
            "source_type": "assignment_observation",
            "source_reference": source_id.split(":", 1)[1],
            "authority": "weak_observation",
            "confidence": "medium",
        }
    return None


def _mac_placeholder(normalized: str) -> bool:
    compact = normalized.replace(":", "").replace("-", "")
    if MAC_COMPACT_RE.fullmatch(compact):
        return True
    for prefix in ("mac-", "device-"):
        if normalized.startswith(prefix) and MAC_COMPACT_RE.fullmatch(normalized[len(prefix):].replace("-", "")):
            return True
    return False


def normalize_hostname_evidence(raw_value: str) -> dict | None:
    if not isinstance(raw_value, str):
        return None
    if raw_value.strip() in ("", "*"):
        return None
    display = unicodedata.normalize("NFC", raw_value).strip().rstrip(".")
    if not display:
        return {
            "display_value": display,
            "normalized_value": "",
            "quality": "invalid",
            "selectable": False,
        }
    folded = display.casefold()
    try:
        address = ipaddress.ip_address(folded)
    except ValueError:
        address = None
    mac = folded.replace("-", ":")
    if folded in PLACEHOLDERS or address is not None or MAC_RE.fullmatch(mac) or _mac_placeholder(folded):
        return {
            "display_value": display,
            "normalized_value": folded,
            "quality": "placeholder",
            "selectable": False,
        }
    labels = display.split(".")
    ascii_labels = []
    idna_valid = True
    try:
        for label in labels:
            if not label:
                raise UnicodeError("empty label")
            ascii_labels.append(label.encode("idna").decode("ascii").lower())
    except (UnicodeError, UnicodeEncodeError):
        idna_valid = False
    normalized = ".".join(ascii_labels) if idna_valid else folded
    normal_dns = (
        idna_valid
        and 1 <= len(normalized) <= 253
        and all(len(label) <= 63 and DNS_LABEL_RE.fullmatch(label) for label in ascii_labels)
    )
    nonstandard = (
        not normal_dns
        and normalized.isascii()
        and 1 <= len(normalized) <= 253
        and all(1 <= len(label) <= 63 and NONSTANDARD_LABEL_RE.fullmatch(label) for label in normalized.split("."))
        and "_" in normalized
    )
    low = normalized in GENERIC_LOW_VALUES or any(pattern.fullmatch(normalized) for pattern in LOW_PATTERNS)
    if normal_dns:
        quality = "low" if low else "normal"
        selectable = True
    elif nonstandard:
        quality = "low"
        selectable = True
    else:
        quality = "invalid"
        selectable = False
    return {
        "display_value": display,
        "normalized_value": normalized,
        "quality": quality,
        "selectable": selectable,
    }


def _candidate_id(device_id: str, normalized: str, source_id: str, state: str) -> str:
    identity = _canonical_json((device_id, FIELD, normalized, source_id, state))
    return "hce_" + _sha256_text(identity, 20)


def _candidate_sort_key(candidate: dict) -> tuple:
    return (
        candidate["normalized_value"],
        -AUTHORITY_RANK[candidate["authority"]],
        candidate["source_id"],
        candidate["state"],
        candidate["candidate_id"],
    )


def _selection_sort_key(candidate: dict) -> tuple:
    try:
        last_available = _parse_rfc3339(candidate["last_available_at"])
    except (ValueError, OSError):
        last_available = 0
    return (
        -AUTHORITY_RANK[candidate["authority"]],
        -(1 if candidate["state"] == "active" else 0),
        -QUALITY_RANK[candidate["quality"]],
        -CONFIDENCE_RANK[candidate["confidence"]],
        -last_available,
        candidate["normalized_value"],
        candidate["source_id"],
        candidate["candidate_id"],
    )


def collect_hostname_candidates(bound_records: dict[str, list[dict]], generated_at: str) -> dict[str, list[dict]]:
    _parse_rfc3339(generated_at)
    result = {}
    for device_id in sorted(bound_records):
        if not DEVICE_ID_RE.fullmatch(device_id):
            continue
        by_identity = {}
        for record in bound_records[device_id]:
            descriptor = _source_descriptor(record)
            if descriptor is None:
                continue
            normalized = normalize_hostname_evidence(record["hostname"])
            if normalized is None:
                continue
            confidence = descriptor["confidence"]
            if normalized["quality"] in {"low", "placeholder", "invalid"}:
                confidence = "low" if normalized["quality"] != "invalid" else "unknown"
            source_id = descriptor["source_id"]
            identity = (normalized["normalized_value"], source_id)
            candidate = {
                "candidate_id": _candidate_id(device_id, normalized["normalized_value"], source_id, "active"),
                "raw_value": record["hostname"],
                "display_value": normalized["display_value"],
                "normalized_value": normalized["normalized_value"],
                "source_id": source_id,
                "source_type": descriptor["source_type"],
                "source_reference": descriptor["source_reference"],
                "authority": descriptor["authority"],
                "confidence": confidence,
                "quality": normalized["quality"],
                "selectable": normalized["selectable"],
                "observed_at": None,
                "first_available_at": generated_at,
                "last_available_at": generated_at,
                "state": "active",
                "selected": False,
                "conflict_status": "none",
                "derivation_rule": NORMALIZATION_RULE,
            }
            current = by_identity.get(identity)
            if current is None or _canonical_json(candidate) < _canonical_json(current):
                by_identity[identity] = candidate
        result[device_id] = sorted(by_identity.values(), key=_candidate_sort_key)
    return result


def _prior_hostname(prior: dict | None, device_id: str) -> dict | None:
    if not prior:
        return None
    record = prior.get("records", {}).get(device_id)
    return record.get("hostname") if isinstance(record, dict) else None


def _merge_prior_availability(candidates: list[dict], prior_hostname: dict | None) -> None:
    if not prior_hostname:
        return
    prior_candidates = prior_hostname.get("candidates", [])
    by_key = {
        (item.get("normalized_value"), item.get("source_id")): item
        for item in prior_candidates
        if isinstance(item, dict)
    }
    for candidate in candidates:
        prior = by_key.get((candidate["normalized_value"], candidate["source_id"]))
        if prior and prior.get("first_available_at"):
            candidate["first_available_at"] = prior["first_available_at"]


def _historical_candidate(prior_hostname: dict | None, device_id: str, active: list[dict]) -> dict | None:
    if not prior_hostname:
        return None
    selected_id = prior_hostname.get("selected_candidate_id")
    previous = next((item for item in prior_hostname.get("candidates", []) if item.get("candidate_id") == selected_id), None)
    if not previous or previous.get("state") != "active":
        return None
    if any(
        item["normalized_value"] == previous.get("normalized_value")
        and item["source_id"] == previous.get("source_id")
        for item in active
    ):
        return None
    historical = dict(previous)
    historical["candidate_id"] = _candidate_id(device_id, historical["normalized_value"], historical["source_id"], "historical")
    historical["source_type"] = "historical"
    historical["authority"] = "historical"
    historical["confidence"] = "low" if historical.get("selectable") else "unknown"
    historical["state"] = "historical"
    historical["selected"] = False
    historical["conflict_status"] = "none"
    return historical


def _select_hostname(candidates: list[dict]) -> dict:
    selectable = [candidate for candidate in candidates if candidate["selectable"]]
    selected = sorted(selectable, key=_selection_sort_key)[0] if selectable else None
    active_selectable = [candidate for candidate in selectable if candidate["state"] == "active"]
    active_values = {candidate["normalized_value"] for candidate in active_selectable}
    conflict = len(active_values) > 1
    active_counts = {}
    for candidate in active_selectable:
        active_counts[candidate["normalized_value"]] = active_counts.get(candidate["normalized_value"], 0) + 1
    for candidate in candidates:
        if conflict and candidate in active_selectable:
            candidate["conflict_status"] = "active_conflict"
        elif candidate["state"] == "active" and active_counts.get(candidate["normalized_value"], 0) > 1:
            candidate["conflict_status"] = "agreement"
        elif candidate["state"] == "historical" and active_values and candidate["normalized_value"] not in active_values:
            candidate["conflict_status"] = "historical_disagreement"
        else:
            candidate["conflict_status"] = "none"
        candidate["selected"] = selected is not None and candidate["candidate_id"] == selected["candidate_id"]
    if selected is None:
        evidence_status = "no_evidence" if not candidates else "no_valid_candidate"
        rule = "no_valid_candidate"
    elif conflict:
        evidence_status = "selected_with_conflict"
        rule = RULE_BY_AUTHORITY[selected["authority"]]
    elif active_counts.get(selected["normalized_value"], 0) > 1:
        evidence_status = "selected_with_agreement"
        rule = "source_agreement"
    else:
        evidence_status = "selected"
        rule = RULE_BY_AUTHORITY[selected["authority"]]
    return {
        "selected_candidate_id": selected["candidate_id"] if selected else None,
        "candidates": sorted(candidates, key=_candidate_sort_key),
        "conflict": conflict,
        "evidence_status": evidence_status,
        "selection_rule": rule,
    }


def build_hostname_envelope(
    resolved_devices: list[dict],
    candidates_by_device: dict[str, list[dict]],
    previous_envelope: dict | None,
    generated_at: str,
) -> dict:
    _parse_rfc3339(generated_at)
    records = {}
    for device in sorted(resolved_devices, key=lambda item: str(item.get("id", ""))):
        device_id = str(device.get("id", ""))
        if not DEVICE_ID_RE.fullmatch(device_id):
            raise EnrichmentSchemaError("resolved device id is invalid")
        active = [dict(item) for item in candidates_by_device.get(device_id, [])]
        prior_hostname = _prior_hostname(previous_envelope, device_id)
        _merge_prior_availability(active, prior_hostname)
        historical = _historical_candidate(prior_hostname, device_id, active)
        candidates = active + ([historical] if historical else [])
        records[device_id] = {"device_id": device_id, "hostname": _select_hostname(candidates)}
    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": generated_at,
        "generator": GENERATOR,
        "record_count": len(records),
        "candidate_count": sum(len(item["hostname"]["candidates"]) for item in records.values()),
        "conflict_count": sum(1 for item in records.values() if item["hostname"]["conflict"]),
        "records": records,
    }
    validate_hostname_envelope(payload)
    return payload


def _require_exact_keys(value: dict, expected: set[str], label: str) -> None:
    if not isinstance(value, dict):
        raise EnrichmentSchemaError(f"{label} must be an object")
    if set(value) != expected:
        raise EnrichmentSchemaError(f"{label} fields are invalid")


def _require_enum(value, allowed: set[str], label: str) -> None:
    if not isinstance(value, str) or value not in allowed:
        raise EnrichmentSchemaError(f"{label} is invalid")


def _validate_candidate(candidate: dict, device_id: str) -> None:
    fields = {
        "candidate_id", "raw_value", "display_value", "normalized_value", "source_id",
        "source_type", "source_reference", "authority", "confidence", "quality", "selectable",
        "observed_at", "first_available_at", "last_available_at", "state", "selected",
        "conflict_status", "derivation_rule",
    }
    _require_exact_keys(candidate, fields, "candidate")
    if not isinstance(candidate["candidate_id"], str) or not CANDIDATE_ID_RE.fullmatch(candidate["candidate_id"]):
        raise EnrichmentSchemaError("candidate id is invalid")
    for field in ("raw_value", "display_value", "normalized_value", "source_id"):
        if not isinstance(candidate[field], str):
            raise EnrichmentSchemaError(f"candidate {field} must be a string")
    if candidate["source_reference"] is not None and not isinstance(candidate["source_reference"], str):
        raise EnrichmentSchemaError("source reference is invalid")
    _require_enum(candidate["source_type"], SOURCE_TYPES, "source type")
    _require_enum(candidate["authority"], AUTHORITIES, "authority")
    _require_enum(candidate["confidence"], CONFIDENCES, "confidence")
    _require_enum(candidate["quality"], QUALITIES, "quality")
    _require_enum(candidate["state"], STATES, "state")
    _require_enum(candidate["conflict_status"], CONFLICT_STATUSES, "conflict status")
    if type(candidate["selectable"]) is not bool or type(candidate["selected"]) is not bool:
        raise EnrichmentSchemaError("candidate flags must be Boolean")
    if candidate["observed_at"] is not None:
        _parse_rfc3339(candidate["observed_at"])
    _parse_rfc3339(candidate["first_available_at"])
    _parse_rfc3339(candidate["last_available_at"])
    if candidate["derivation_rule"] != NORMALIZATION_RULE:
        raise EnrichmentSchemaError("derivation rule is invalid")
    expected_id = _candidate_id(device_id, candidate["normalized_value"], candidate["source_id"], candidate["state"])
    if candidate["candidate_id"] != expected_id:
        raise EnrichmentSchemaError("candidate id does not match content")


def validate_hostname_envelope(payload: dict) -> None:
    top = {"schema_version", "generated_at", "generator", "record_count", "candidate_count", "conflict_count", "records"}
    _require_exact_keys(payload, top, "enrichment")
    if payload["schema_version"] != SCHEMA_VERSION or payload["generator"] != GENERATOR:
        raise EnrichmentSchemaError("enrichment version or generator is unsupported")
    _parse_rfc3339(payload["generated_at"])
    for field in ("record_count", "candidate_count", "conflict_count"):
        if type(payload[field]) is not int or payload[field] < 0:
            raise EnrichmentSchemaError(f"{field} must be a nonnegative integer")
    if not isinstance(payload["records"], dict):
        raise EnrichmentSchemaError("records must be an object")
    if list(payload["records"]) != sorted(payload["records"]):
        raise EnrichmentSchemaError("records must be sorted")
    candidate_count = 0
    conflict_count = 0
    for device_id, record in payload["records"].items():
        if not DEVICE_ID_RE.fullmatch(device_id):
            raise EnrichmentSchemaError("device id is invalid")
        _require_exact_keys(record, {"device_id", "hostname"}, "record")
        if record["device_id"] != device_id:
            raise EnrichmentSchemaError("device id does not match key")
        hostname = record["hostname"]
        _require_exact_keys(hostname, {"selected_candidate_id", "candidates", "conflict", "evidence_status", "selection_rule"}, "hostname")
        if hostname["selected_candidate_id"] is not None and not isinstance(hostname["selected_candidate_id"], str):
            raise EnrichmentSchemaError("selected candidate id is invalid")
        if not isinstance(hostname["candidates"], list) or type(hostname["conflict"]) is not bool:
            raise EnrichmentSchemaError("hostname candidates or conflict is invalid")
        _require_enum(hostname["evidence_status"], EVIDENCE_STATUSES, "evidence status")
        _require_enum(hostname["selection_rule"], SELECTION_RULES, "selection rule")
        for candidate in hostname["candidates"]:
            _validate_candidate(candidate, device_id)
        if hostname["candidates"] != sorted(hostname["candidates"], key=_candidate_sort_key):
            raise EnrichmentSchemaError("candidates must be sorted")
        ids = [item["candidate_id"] for item in hostname["candidates"]]
        if len(ids) != len(set(ids)):
            raise EnrichmentSchemaError("candidate ids must be unique")
        selected = [item for item in hostname["candidates"] if item["selected"]]
        if len(selected) > 1 or (selected[0]["candidate_id"] if selected else None) != hostname["selected_candidate_id"]:
            raise EnrichmentSchemaError("selected candidate flags are inconsistent")
        expected = _select_hostname([dict(item) for item in hostname["candidates"]])
        if hostname != expected:
            raise EnrichmentSchemaError("hostname selection or conflict fields are inconsistent")
        candidate_count += len(hostname["candidates"])
        conflict_count += int(hostname["conflict"])
    if payload["record_count"] != len(payload["records"]):
        raise EnrichmentSchemaError("record count is inconsistent")
    if payload["candidate_count"] != candidate_count or payload["conflict_count"] != conflict_count:
        raise EnrichmentSchemaError("candidate or conflict count is inconsistent")


def load_previous_enrichment(path: Path) -> tuple[dict | None, bool]:
    if not path.exists():
        return None, False
    try:
        payload = json.loads(path.read_text())
        validate_hostname_envelope(payload)
        return payload, False
    except Exception:
        return None, True


def build_enrichment_status(
    status: str,
    updated: str,
    envelope: dict | None = None,
    error_code: str | None = None,
) -> dict:
    payload = {
        "schema_version": SCHEMA_VERSION,
        "updated": updated,
        "status": status,
        "record_count": envelope.get("record_count", 0) if envelope else 0,
        "candidate_count": envelope.get("candidate_count", 0) if envelope else 0,
        "conflict_count": envelope.get("conflict_count", 0) if envelope else 0,
        "generator": GENERATOR,
        "error_code": error_code,
    }
    validate_enrichment_status(payload)
    return payload


def validate_enrichment_status(payload: dict) -> None:
    fields = {"schema_version", "updated", "status", "record_count", "candidate_count", "conflict_count", "generator", "error_code"}
    _require_exact_keys(payload, fields, "enrichment status")
    if payload["schema_version"] != SCHEMA_VERSION or payload["generator"] != GENERATOR:
        raise EnrichmentSchemaError("status version or generator is unsupported")
    _parse_rfc3339(payload["updated"])
    _require_enum(payload["status"], STATUS_VALUES, "status")
    for field in ("record_count", "candidate_count", "conflict_count"):
        if type(payload[field]) is not int or payload[field] < 0:
            raise EnrichmentSchemaError(f"status {field} is invalid")
    if payload["error_code"] is not None:
        if not isinstance(payload["error_code"], str) or not re.fullmatch(r"[a-z0-9_]{1,64}", payload["error_code"]):
            raise EnrichmentSchemaError("status error code is invalid")
    if payload["status"] == "online" and payload["error_code"] is not None:
        raise EnrichmentSchemaError("online status cannot contain an error code")
    if payload["status"] != "online" and payload["error_code"] is None:
        raise EnrichmentSchemaError("non-online status requires an error code")
    if payload["status"] in {"error", "unavailable"} and any(
        payload[field] for field in ("record_count", "candidate_count", "conflict_count")
    ):
        raise EnrichmentSchemaError("failed or unavailable status counts must be zero")


class EnricherRegistry:
    """Small deterministic registry for later approved enrichment packages."""

    def __init__(self):
        self._entries = {}

    def register(self, name: str, source_collector, normalizer, authority, confidence, selector) -> None:
        if not re.fullmatch(r"[a-z][a-z0-9_]{0,63}", name) or name in self._entries:
            raise ValueError("enricher name is invalid or duplicated")
        self._entries[name] = (source_collector, normalizer, authority, confidence, selector)

    def run(self, context: dict) -> dict:
        output = {}
        for name, (collector, normalizer, authority, confidence, selector) in sorted(self._entries.items()):
            isolated_context = copy.deepcopy(context)
            observed = collector(isolated_context)
            normalized = normalizer(observed, isolated_context)
            output[name] = selector(normalized, authority, confidence, isolated_context)
        return output
