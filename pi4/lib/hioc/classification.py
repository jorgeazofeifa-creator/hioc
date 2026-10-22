"""Private PE-6 classification. Pure, stateless, explicitly timed; never a public role writer."""
import copy
import hashlib
import json
import re
from datetime import timedelta

from . import assets, enrichment, manufacturer
from . import service_association as local
from . import configured_association as pe5
from .inventory import KNOWN_FIELDS, OPERATOR_ROLES, normalize_mac
from .classification_contract import SCHEMA, RULES, DIMENSIONS

KINDS = ("inventory", "assets", "known_operator_role", "hostname", "manufacturer",
         "home_assistant_summary", "pe5_handoff")
LIMIT = 16 * 1024 * 1024
MAX_DEVICES = 4096
MAX_EVIDENCE = 64
POLICY = {"inventory_age_seconds": 2100, "approved_known_sha256": None,
          "manufacturer_dataset": None}
REASONS = {"VALIDATED", "ABSENT", "UNAVAILABLE", "INVALID", "STALE", "CHANGED",
           "CONFLICTED", "NOT_SUPPORTED", "INCOMPLETE", "INSUFFICIENT_EVIDENCE",
           "LIMIT_EXCEEDED"}


class ClassificationError(ValueError):
    """Fixed codes only: never propagate input or filesystem exception text."""
    def __init__(self, code):
        self.code = code if code in REASONS | {"CLOCK_INVALID", "POLICY_INVALID", "RESULT_INVALID"} else "INVALID"
        super().__init__(self.code)


def fail(code):
    raise ClassificationError(code)


def canonical(value):
    try:
        local._json_input(value)
        return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
                          allow_nan=False).encode("ascii")
    except (ValueError, TypeError, RecursionError, UnicodeError):
        fail("INVALID")


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def timestamp(value):
    # Match the accepted PE-5 aware-time grammar, without allowing fromisoformat
    # to carry an invalid offset minute (for example +01:60) into the next hour.
    if type(value) is not str or not re.fullmatch(local.TIMESTAMP_PATTERN, value):
        fail("CLOCK_INVALID")
    if value[-1] != "Z" and (int(value[-5:-3]) >= 24 or int(value[-2:]) >= 60):
        fail("CLOCK_INVALID")
    try:
        return local._time(value, "CLOCK_INVALID")
    except local.ServiceAssociationError:
        fail("CLOCK_INVALID")


def _utc_text(value):
    # Keep existing Z representation; normalize external offsets for the closed
    # output schema. Original source bytes and their digest remain untouched.
    parsed = timestamp(value)
    return value if value.endswith("Z") else local._time_text(parsed)


def snapshot(value=None, state=None, raw=None):
    """Caller captures a validated immutable copy; content proof never means durable confirmation."""
    value = copy.deepcopy(value)
    if value is not None:
        canonical(value)  # Admit only bounded-depth JSON; preserve source protocol field order.
        raw = json.dumps(value, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii") if raw is None else raw
    else:
        raw = None
    return {"state": state or ("ABSENT" if value is None else "VALID"),
            "sha256": hashlib.sha256(raw).hexdigest() if raw is not None else None,
            "value": value, "raw": raw.decode("utf8") if raw is not None else None}


def _policy(policy):
    if policy is None:
        return dict(POLICY)
    if type(policy) is not dict or set(policy) != set(POLICY):
        fail("POLICY_INVALID")
    if type(policy["inventory_age_seconds"]) is not int or policy["inventory_age_seconds"] != 2100:
        fail("POLICY_INVALID")
    known = policy["approved_known_sha256"]
    if known is not None and (type(known) is not str or not re.fullmatch("[0-9a-f]{64}", known)):
        fail("POLICY_INVALID")
    pin = policy["manufacturer_dataset"]
    if pin is not None and (type(pin) is not dict or set(pin) !=
                            {"database", "manifest", "approved_manifest_sha256"}):
        fail("POLICY_INVALID")
    return policy


def _input(kind, wrapper):
    if wrapper is None:
        wrapper = snapshot()
    if type(wrapper) is not dict or set(wrapper) != {"state", "sha256", "value", "raw"}:
        fail("INVALID")
    state, value = wrapper["state"], wrapper["value"]
    if state not in ("VALID", "ABSENT", "UNAVAILABLE", "INVALID", "STALE", "CONFLICTED"):
        fail("INVALID")
    if state != "VALID":
        if value is not None or wrapper["sha256"] is not None or wrapper["raw"] is not None:
            fail("INVALID")
        return value, dict(kind=kind, state=state, sha256=None, generated_at=None,
                           revision=None, reason_code=state)
    encoded = canonical(value)
    if len(encoded) > LIMIT:
        fail("LIMIT_EXCEEDED")
    if type(wrapper["raw"]) is not str or len(wrapper["raw"].encode("utf8")) > LIMIT:
        fail("LIMIT_EXCEEDED")
    raw = wrapper["raw"].encode("utf8")
    parsed = pe5.strict_json(raw, LIMIT)
    if hashlib.sha256(raw).hexdigest() != wrapper["sha256"] or canonical(parsed) != canonical(value):
        fail("CHANGED")
    if type(parsed) is not dict:
        fail("INVALID")
    return parsed, dict(kind=kind, state="VALID", sha256=wrapper["sha256"],
                       generated_at=None, revision=None, reason_code="VALIDATED")


def _known(value, expected, actual):
    if expected is None or expected != actual:
        fail("INSUFFICIENT_EVIDENCE")
    if set(value) != {"devices"} or type(value["devices"]) is not list:
        fail("INVALID")
    if len(value["devices"]) > MAX_DEVICES:
        fail("LIMIT_EXCEEDED")
    for row in value["devices"]:
        if type(row) is not dict or set(row) - KNOWN_FIELDS:
            fail("INVALID")
        if "enabled" in row and type(row["enabled"]) is not bool:
            fail("INVALID")
        if row.get("enabled") is False:
            continue
        if "role" in row and row["role"] not in OPERATOR_ROLES:
            fail("INVALID")
        if row.get("mac") and (type(row["mac"]) is not str or not normalize_mac(row["mac"])):
            fail("INVALID")
        for field, child in row.items():
            if field != "enabled" and child is not None and type(child) is not str:
                fail("INVALID")


def _hostname(value, inventory):
    enrichment.validate_hostname_envelope(value)
    if value["generated_at"] != inventory["updated"]:
        fail("CHANGED")
    if set(value["records"]) != {x["id"] for x in inventory["devices"]}:
        fail("CHANGED")
    for row in value["records"].values():
        if len(row["hostname"]["candidates"]) > MAX_EVIDENCE:
            fail("LIMIT_EXCEEDED")
        for candidate in row["hostname"]["candidates"]:
            if candidate["observed_at"] is not None and local._time(
                    candidate["observed_at"], "INVALID") > timestamp(inventory["updated"]):
                fail("INVALID")


def _manufacturer(value, inventory, pin):
    manufacturer.validate_manufacturer_sidecar(value)
    if pin is None:
        fail("INSUFFICIENT_EVIDENCE")
    database, unused = _input("manufacturer_database", pin["database"])
    manifest, mf_proof = _input("manufacturer_manifest", pin["manifest"])
    if database is None or manifest is None or pin["approved_manifest_sha256"] != mf_proof["sha256"]:
        fail("INSUFFICIENT_EVIDENCE")
    manufacturer.validate_database(database)
    manufacturer.validate_manifest(manifest)
    db_raw = pin["database"]["raw"].encode("utf8")
    if hashlib.sha256(db_raw).hexdigest() != manifest["database_sha256"] or len(db_raw) != manifest["database_size_bytes"] or database["semantic_sha256"] != manifest["database_semantic_sha256"]:
        fail("CHANGED")
    for key in ("dataset_id", "dataset_version", "parser_version", "record_count", "ma_l_count", "ma_m_count", "ma_s_count", "conflict_count"):
        if database[key] != manifest[key]:fail("CHANGED")
    maps = {key:{} for key in manufacturer.ASSIGNMENT_CLASSES}
    for row in database["records"].values():
        maps[row["assignment_class"]][row["prefix"]] = manufacturer.ManufacturerRecord(**row)
    db = manufacturer.ManufacturerDatabase(database, manufacturer.ManufacturerManifest(manifest,manifest["database_sha256"],manifest["database_semantic_sha256"]), maps["MA-L"], maps["MA-M"], maps["MA-S"], database["conflicts"])
    expected, unused = manufacturer.build_manufacturer_sidecar(inventory,db,generated_at=value["generated_at"])
    if value != expected:fail("CHANGED")


def _ha(value, inventory):
    ids = {x["id"] for x in inventory["devices"]}
    if set(value) - ids:
        fail("CHANGED")
    for row in value.values():
        if type(row) is not dict or set(row) != {"associated", "association_basis",
                "entity_count", "integration_domains", "has_area_candidate"}:
            fail("INVALID")
        if row["associated"] is not True or row["association_basis"] != "strong_mac" or type(row["entity_count"]) is not int or not 1 <= row["entity_count"] <= MAX_DEVICES or type(row["has_area_candidate"]) is not bool:
            fail("INVALID")
        domains = row["integration_domains"]
        if type(domains) is not list or len(domains) > 64 or any(type(x) is not str or not re.fullmatch("[a-z][a-z0-9_]{0,63}", x) for x in domains) or domains != sorted(set(domains)):
            fail("INVALID")


def _handoff(value, inventory, evaluated_at):
    if set(value) != {"output", "source", "output_confirmation", "source_confirmation"}:
        fail("INVALID")
    if value["output_confirmation"] != "CONFIRMED":
        fail("INSUFFICIENT_EVIDENCE")
    output = value["output"]
    if output["configured"]["state"] == "VALID" and value["source_confirmation"] != "CONFIRMED":
        fail("INSUFFICIENT_EVIDENCE")
    pe5.validate_handoff(output, inventory, value["source"], evaluated_at)


def _validate_source(kind, value, proof, inventory, now, policy):
    if kind == "assets":
        assets.validate_supported_store(value)
        if len(value["assets"]) > MAX_DEVICES:
            fail("LIMIT_EXCEEDED")
        if any(x["revision"] > 2**53-1 for x in value["assets"].values()):
            fail("INVALID")
    elif kind == "known_operator_role":
        _known(value, policy["approved_known_sha256"], proof["sha256"])
    elif kind == "hostname":
        _hostname(value, inventory)
        proof["generated_at"] = _utc_text(value["generated_at"])
    elif kind == "manufacturer":
        _manufacturer(value, inventory, policy["manufacturer_dataset"])
        proof["generated_at"] = _utc_text(value["generated_at"])
    elif kind == "home_assistant_summary":
        _ha(value, inventory)
    elif kind == "pe5_handoff":
        _handoff(value, inventory, now)
        proof["generated_at"] = _utc_text(value["output"]["evaluated_at"])
        proof["revision"] = value["output"]["configured"]["revision"]


def _suggestions(device_id, values, proofs, strong, conflict):
    found = {}
    if not strong:
        return []
    def add(rule, original, source, family):
        role = rule["role"]
        row = found.setdefault(role, dict(
            suggestion_id="rsug_" + digest(["pe6-role-v1", device_id, role]),
            role=role, confidence="low", rule_ids=set(), evidence_ids=set(),
            correlation_groups=set()))
        row["rule_ids"].add(rule["id"])
        row["evidence_ids"].add(digest([device_id, source, proofs[source]["sha256"], original]))
        row["correlation_groups"].add(digest(["pe6-group-v1", device_id, family]))
        if len(row["evidence_ids"]) > MAX_EVIDENCE:
            fail("LIMIT_EXCEEDED")
    hostname = values.get("hostname")
    if hostname is not None and not conflict:
        for c in hostname["records"][device_id]["hostname"]["candidates"]:
            name = c["normalized_value"]
            if c["state"] != "active" or not c["selectable"] or c["authority"] == "historical" or c["quality"] in ("invalid", "placeholder") or not name.isascii() or any(x.startswith("xn--") for x in name.split(".")):
                continue
            # Check normalization rather than trusting a forged normalized token.
            normalized = enrichment.normalize_hostname_evidence(c["raw_value"])
            if not normalized or normalized["normalized_value"] != name:
                continue
            tokens = set(re.findall("[a-z0-9]+", name.lower()))
            for rule in RULES[:-1]:
                if tokens.intersection(rule["tokens"]):
                    add(rule, c["candidate_id"], "hostname", "hostname")
    handoff = values.get("pe5_handoff")
    if handoff and handoff["output"]["local"] is not None:
        for row in handoff["output"]["local"]["service_associations"]:
            if row["stable_device_id"] == device_id and row["service_type"] in RULES[-1]["service_types"]:
                add(RULES[-1], row["association_id"], "pe5_handoff", "local_service")
    output = []
    for row in found.values():
        for field in ("rule_ids", "evidence_ids", "correlation_groups"):
            row[field] = sorted(row[field])
        output.append(row)
    return sorted(output, key=lambda x: x["suggestion_id"])


def _device(device, values, proofs, owners):
    device_id = device["id"]
    problem = local._owner_reason(device_id, *owners)
    identity = "strong" if problem is None else "ambiguous" if problem in (
        "AMBIGUOUS_OWNER", "OWNER_MAC_COLLISION") else "weak"
    strong = identity == "strong"
    host = values.get("hostname")
    conflict = bool(strong and host and host["records"][device_id]["hostname"]["conflict"])
    roles = []
    known = values.get("known_operator_role")
    if strong and known:
        roles = sorted({r["role"] for r in known["devices"] if r.get("enabled") is not False
                        and r.get("role") and normalize_mac(r.get("mac", "")) == normalize_mac(device["mac"])})
    role_conflict = len(roles) > 1
    conflict = conflict or role_conflict or bool(strong and values.get("manufacturer") and values["manufacturer"]["records"][device_id]["lookup_status"] == "conflicting_assignment")
    role = roles[0] if len(roles) == 1 else None
    evidence = digest([device_id, "known_operator_role", proofs["known_operator_role"]["sha256"], role]) if role else None
    suggestions = _suggestions(device_id, values, proofs, strong,
                               bool(host and host["records"][device_id]["hostname"]["conflict"]))
    asset_store = values.get("assets")
    record = asset_store["assets"].get(device_id) if asset_store is not None else None
    asset_state = ("unknown" if proofs["assets"]["state"] not in ("VALID", "ABSENT") else
                   "missing" if record is None else "documented" if all(record[k] is not None
                   for k in ("friendly_name", "physical_location", "purpose")) else "incomplete")
    quality = ("conflicted" if conflict else "unknown" if not strong or asset_state == "unknown"
               else "documented" if asset_state == "documented" else "incomplete")
    operator = "conflicted" if role_conflict else "explicit_unknown" if role == "Unknown" else "declared" if role else "missing" if proofs["known_operator_role"]["state"] == "ABSENT" or known is not None else "unverified"
    disposition = "unverified"
    if strong and values.get("manufacturer"):
        status = values["manufacturer"]["records"][device_id]["lookup_status"]
        disposition = ("matched" if status == "matched" else "excluded" if status in
                       ("locally_administered_address", "multicast_address") else
                       "conflicted" if status == "conflicting_assignment" else "unknown")
    available = sum(values.get(k) is not None for k in ("home_assistant_summary", "pe5_handoff"))
    relation = "available" if available == 2 else "partial" if available else "unavailable"
    provenance = "conflicted" if conflict else "verified" if all(p["state"] == "VALID" for p in proofs.values()) else "partial"
    states = [identity, asset_state, disposition, operator, "not_supported_current_schema",
              "multiple" if len(suggestions) > 1 else "single" if suggestions else "none" if strong else "unavailable",
              relation, provenance]
    kinds = ["inventory", "assets", "manufacturer", "known_operator_role", "assets",
             "hostname", "pe5_handoff", "inventory"]
    details = []
    for d, state, kind in zip(DIMENSIONS, states, kinds):
        reason = ("NOT_SUPPORTED" if state == "not_supported_current_schema" else
                  "CONFLICTED" if state == "conflicted" else
                  "INCOMPLETE" if state == "incomplete" else
                  "ABSENT" if state == "missing" else
                  "INSUFFICIENT_EVIDENCE" if state in ("weak", "unknown", "unverified", "unavailable", "none") else "VALIDATED")
        details.append(dict(name=d["name"], state=state, source_kind=kind, reason_code=reason))
    classification = ("EXPLICIT_UNKNOWN" if role == "Unknown" else "OPERATOR_DECLARED" if role
                      else "AMBIGUOUS" if role_conflict or len(suggestions) > 1
                      else "UNCONFIRMED" if suggestions else "UNKNOWN")
    return dict(stable_device_id=device_id, identity_status=identity, operator_role=role,
                operator_role_evidence=evidence, classification_status=classification,
                role_suggestion=suggestions, metadata_quality=quality,
                quality_details=sorted(details, key=lambda x: x["name"]),
                reason_codes=sorted({x["reason_code"] for x in details}))


def resolve_classification(inputs, evaluated_at, policy=None):
    """Return a private envelope. No input mutation, IO, implicit clock or environment."""
    now = timestamp(evaluated_at)
    policy = _policy(policy)
    if type(inputs) is not dict or set(inputs) - set(KINDS):
        fail("INVALID")
    values, proofs = {}, {}
    for kind in KINDS:
        try:
            value, proof = _input(kind, inputs.get(kind))
            values[kind], proofs[kind] = value, proof
        except ClassificationError as error:
            values[kind] = None
            proofs[kind] = dict(kind=kind, state="INVALID", sha256=None, generated_at=None,
                                revision=None, reason_code=error.code)
        except (ValueError, TypeError, UnicodeError, RecursionError):
            values[kind] = None
            proofs[kind] = dict(kind=kind, state="INVALID", sha256=None, generated_at=None, revision=None, reason_code="INVALID")
    deadline = None
    inv = values["inventory"]
    try:
        if inv is not None:
            if type(inv.get("devices")) is list and len(inv["devices"]) > MAX_DEVICES or type(inv.get("services")) is list and len(inv["services"]) > MAX_DEVICES:
                fail("LIMIT_EXCEEDED")
            local.resolve_service_associations(inv, evaluated_at, 2100)
            if len({d["id"] for d in inv["devices"]}) != len(inv["devices"]):
                fail("INVALID")
            updated = timestamp(inv["updated"])
            deadline = updated + timedelta(seconds=2100)
            if now < updated or now >= deadline:
                fail("STALE")
            proofs["inventory"]["generated_at"] = _utc_text(inv["updated"])
    except (local.ServiceAssociationError, ClassificationError, TypeError, KeyError) as error:
        values["inventory"] = inv = None
        code = "LIMIT_EXCEEDED" if getattr(error,"code",None) == "LIMIT_EXCEEDED" else "STALE" if deadline is not None and now >= deadline else "INVALID"
        proofs["inventory"].update(state="INVALID", reason_code=code)
    if inv is not None:
        for kind in KINDS[1:]:
            if values[kind] is None:
                continue
            try:
                _validate_source(kind, values[kind], proofs[kind], inv, evaluated_at, policy)
                if kind == "pe5_handoff":
                    deadline = min(deadline, timestamp(values[kind]["output"]["valid_until"]))
            except ClassificationError as error:
                values[kind] = None
                proofs[kind].update(state="INVALID", reason_code=error.code)
            except (ValueError, TypeError, KeyError, assets.AssetError, manufacturer.ManufacturerError):
                values[kind] = None
                proofs[kind].update(state="INVALID", reason_code="INVALID")
    devices = []
    if inv is not None:
        owners = local._owners(inv["devices"])
        try:
            devices = [_device(d, values, proofs, owners) for d in sorted(inv["devices"], key=lambda x: x["id"])]
        except ClassificationError as error:
            inv = None
            proofs["inventory"].update(state="INVALID", reason_code=error.code)
            devices = []
    state = "UNAVAILABLE" if inv is None else "VALID" if all(p["state"] == "VALID" for p in proofs.values()) else "PARTIAL"
    output = dict(schema_version="1.0", rule_version="pe6-role-v1", state=state,
                  evaluated_at=_utc_text(evaluated_at), valid_until=local._time_text(deadline) if inv is not None else None,
                  inputs=sorted(proofs.values(), key=lambda x: x["kind"]), devices=devices,
                  summary=dict(device_count=len(devices), suggestion_count=sum(len(d["role_suggestion"]) for d in devices),
                               conflicted_count=sum(d["metadata_quality"] == "conflicted" for d in devices),
                               unavailable_source_count=sum(p["state"] != "VALID" for p in proofs.values())))
    if len(canonical(output)) > LIMIT:
        fail("LIMIT_EXCEEDED")
    try:
        pe5.shape(output, SCHEMA, "RESULT_INVALID")
    except pe5.AssociationError:
        fail("RESULT_INVALID")
    return output


def validate_classification_result(result, current_inputs, evaluated_at, policy=None):
    """Every use checks current fingerprints, original derivation and a new current time."""
    try:
        pe5.shape(result, SCHEMA, "RESULT_INVALID")
        now, original = timestamp(evaluated_at), timestamp(result["evaluated_at"])
        if now < original or (result["valid_until"] is not None and now >= timestamp(result["valid_until"])):
            fail("STALE")
        expected = resolve_classification(current_inputs, result["evaluated_at"], policy)
        if canonical(result) != canonical(expected):
            fail("CHANGED")
        # Revalidate temporal source conditions at the actual use time too.
        current = resolve_classification(current_inputs, evaluated_at, policy)
        if result["state"] != "UNAVAILABLE" and current["state"] == "UNAVAILABLE":
            fail("STALE")
    except ClassificationError:
        raise
    except (ValueError, TypeError, KeyError):
        fail("RESULT_INVALID")
