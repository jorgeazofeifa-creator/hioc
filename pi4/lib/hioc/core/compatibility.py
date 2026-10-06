"""Capability-first, privacy-bounded dependency observations for platform status.

No probes are triggered by importing this module. Unknown is never a success.
Only registry-selected identifiers and numeric version tokens enter public state.
"""
import json
import ipaddress
import subprocess
import stat
import os
import time
from contextlib import contextmanager
import re
from datetime import datetime, timezone

STATES = frozenset({"COMPATIBLE", "COMPATIBLE_UPDATED", "COMPATIBILITY_UNKNOWN",
    "COMPATIBILITY_DEGRADED", "INCOMPATIBLE", "TRUST_ANCHOR_CHANGED", "DEPENDENCY_UNAVAILABLE"})
GOOD = {"COMPATIBLE", "COMPATIBLE_UPDATED", "COMPATIBILITY_DEGRADED"}
VERSION = re.compile(r"[0-9]{1,4}(?:\.[0-9]{1,4}){0,3}(?:(?:a|b|rc|\.dev)[0-9]{1,8})?\Z")


def safe_version(value):
    if type(value) is not str or len(value) > 40 or not VERSION.fullmatch(value):
        return None
    try:
        ipaddress.ip_address(value)
        return None
    except ValueError:
        return value


def load_registry(path):
    raw = path.read_bytes()
    if len(raw) > 2 * 1024 * 1024:
        raise ValueError("compatibility registry exceeds bound")
    registry = json.loads(raw)
    if registry.get("schema_version") != "1.0" or type(registry.get("dependencies")) is not list:
        raise ValueError("invalid compatibility registry")
    ids = set()
    for dep in registry["dependencies"]:
        identifier = dep["dependency_id"]
        if not re.fullmatch(r"[a-z][a-z0-9_]{0,63}", identifier) or identifier in ids:
            raise ValueError("invalid dependency identity")
        ids.add(identifier)
        if dep["dependency_class"] not in {"A", "B", "C", "D", "E"} or dep["policy"] not in {
            "capability-based", "supported-line", "intentional exact pin", "security trust anchor",
            "internal schema", "informational only"}:
            raise ValueError("invalid dependency policy")
        if not dep["required_capabilities"] or any(not re.fullmatch(r"[a-z][a-z0-9_]{0,63}", c)
                for c in dep["required_capabilities"] + dep.get("optional_capabilities", [])):
            raise ValueError("invalid capability identity")
    return registry


def _date(value):
    try:
        date = datetime.fromisoformat(value)
        return date if date.tzinfo is not None else None
    except (TypeError, ValueError):
        return None


def diagnostic(dep, status, failed, previous, observed, likely):
    name = dep["display_name"]
    component = dep["failure_isolation"]
    if status == "TRUST_ANCHOR_CHANGED":
        return f"Compatibility trust change detected: {name} identity requires governed review. {component} is isolated; the new identity has not been trusted."
    if status == "DEPENDENCY_UNAVAILABLE":
        return f"Dependency unavailable: {name}. {component} cannot use this dependency. No update cause is established."
    if status == "INCOMPATIBLE":
        if likely:
            return f"Likely update compatibility break: {name} changed from {previous} to {observed}; capability {failed} failed. {component} is isolated."
        return f"Dependency compatibility failure: {name}; capability {failed} failed. {component} is isolated. No software-version change has been established."
    if status == "COMPATIBILITY_UNKNOWN":
        return f"Compatibility unknown: {name}; required capability evidence is unavailable or stale."
    if status == "COMPATIBILITY_DEGRADED":
        return f"Compatibility degraded: {name}; optional capability {failed} failed. Required capabilities continue."
    return f"{name}: required capabilities pass; automatic continuation permitted."


def assess(dep, observation, previous, timestamp):
    observation = observation if type(observation) is dict else {}
    previous = previous if type(previous) is dict else {}
    observed = safe_version(observation.get("observed_version"))
    known = safe_version(previous.get("last_known_compatible_version"))
    capabilities = observation.get("capabilities", {})
    if type(capabilities) is not dict:
        capabilities = {}
    allowed = set(dep["required_capabilities"] + dep.get("optional_capabilities", []))
    if set(capabilities) - allowed or any(type(v) not in (bool, type(None)) for v in capabilities.values()):
        capabilities = {}
    available = observation.get("available")
    if type(available) not in (bool, type(None)):
        available = None
    failed = next((c for c in dep["required_capabilities"] if capabilities.get(c) is False), None)
    missing = any(capabilities.get(c) is None for c in dep["required_capabilities"])
    optional_failed = next((c for c in dep.get("optional_capabilities", []) if capabilities.get(c) is False), None)
    identity_ok = observation.get("identity_matches")
    frozen_drift = dep["dependency_class"] == "B" and dep.get("exact_version") and observed is not None and observed != dep["exact_version"]
    if available is False:
        status = "DEPENDENCY_UNAVAILABLE"
    elif identity_ok is False or frozen_drift:
        status = "TRUST_ANCHOR_CHANGED"
        failed = "identity"
    elif failed:
        status = "INCOMPATIBLE"
    elif dep["dependency_class"] in {"B", "C"} and identity_ok is not True:
        status = "COMPATIBILITY_UNKNOWN"
    elif missing:
        status = "COMPATIBILITY_UNKNOWN"
    elif optional_failed:
        status = "COMPATIBILITY_DEGRADED"
        failed = optional_failed
    elif observed and observed != (known or safe_version(dep.get("compatibility_baseline"))) and (known or safe_version(dep.get("compatibility_baseline"))):
        status = "COMPATIBLE_UPDATED"
    else:
        status = "COMPATIBLE"
    likely = bool(status == "INCOMPATIBLE" and known and observed and known != observed)
    if status in GOOD and observed:
        last_known, last_known_at = observed, timestamp
    else:
        last_known = known
        last_known_at = previous.get("last_known_compatible_at") if _date(previous.get("last_known_compatible_at")) else None
    problem = status not in {"COMPATIBLE", "COMPATIBLE_UPDATED"}
    first = previous.get("first_detection_time") if previous.get("status") == status and previous.get("failed_capability") == failed and safe_version(previous.get("observed_version")) == observed else None
    first = first if _date(first) else timestamp
    result = {"dependency_id": dep["dependency_id"], "display_name": dep["display_name"], "status": status,
        "updated": timestamp, "observed_version": observed, "previous_known_compatible_version": known,
        "last_known_compatible_version": last_known, "last_known_compatible_at": last_known_at,
        "compatibility_baseline": safe_version(dep.get("compatibility_baseline")), "failed_capability": failed,
        "likely_update_compatibility_break": likely, "first_detection_time": first if problem else None,
        "affected_hioc_component": dep["failure_isolation"], "recommended_action": dep["operator_remediation"],
        "capabilities": {c: capabilities.get(c) for c in sorted(allowed)}}
    result["diagnostic"] = diagnostic(dep, status, failed, known, observed, likely)
    return result


def summarize(entries, timestamp):
    counts = {s: sum(e["status"] == s for e in entries) for s in STATES}
    order = ["TRUST_ANCHOR_CHANGED", "INCOMPATIBLE", "DEPENDENCY_UNAVAILABLE", "COMPATIBILITY_DEGRADED",
             "COMPATIBILITY_UNKNOWN", "COMPATIBLE_UPDATED", "COMPATIBLE"]
    overall = next((s for s in order if counts[s]), "COMPATIBILITY_UNKNOWN")
    affected = sorted({e["affected_hioc_component"] for e in entries if e["status"] not in {"COMPATIBLE", "COMPATIBLE_UPDATED", "COMPATIBILITY_UNKNOWN"}})
    return {"schema_version": "1.0", "status": "degraded" if affected else "online", "updated": timestamp,
        "overall_compatibility": overall, "dependency_count": len(entries),
        "compatible_count": counts["COMPATIBLE"], "compatible_updated_count": counts["COMPATIBLE_UPDATED"],
        "degraded_count": counts["COMPATIBILITY_DEGRADED"], "incompatible_count": counts["INCOMPATIBLE"],
        "unknown_count": counts["COMPATIBILITY_UNKNOWN"], "trust_anchor_changed_count": counts["TRUST_ANCHOR_CHANGED"],
        "unavailable_count": counts["DEPENDENCY_UNAVAILABLE"], "affected_components": affected,
        "summary": f"{len(affected)} affected subsystem(s); {counts['COMPATIBILITY_UNKNOWN']} dependencies awaiting capability evidence.",
        "dependencies": entries}


def _update_status(store, registry, observations, timestamp, max_age_seconds=129600):
    if _date(timestamp) is None:
        raise ValueError("compatibility timestamp must have timezone")
    prior = store.read_json("compatibility.json", {})
    prior_entries = prior.get("dependencies", []) if type(prior) is dict else []
    prior_by_id = {e.get("dependency_id"): e for e in prior_entries if type(e) is dict} if type(prior_entries) is list else {}
    entries = []
    for dep in registry["dependencies"]:
        identifier = dep["dependency_id"]
        old = prior_by_id.get(identifier, {})
        if identifier in observations:
            current = assess(dep, observations[identifier], old, timestamp)
        else:
            observed_at = _date(old.get("updated"))
            age = (_date(timestamp) - observed_at).total_seconds() if observed_at else None
            # Revalidate stored values through the same sanitizer; stale current
            # observations become unknown without destroying known-good history.
            fresh = age is not None and 0 <= age <= max_age_seconds
            observation = {"observed_version": old.get("observed_version"), "capabilities": old.get("capabilities", {})} if fresh else {}
            if fresh and old.get("status") == "DEPENDENCY_UNAVAILABLE": observation["available"] = False
            if fresh and old.get("status") == "TRUST_ANCHOR_CHANGED": observation["identity_matches"] = False
            if fresh and old.get("status") in GOOD and dep["dependency_class"] in {"B", "C"}: observation["identity_matches"] = True
            current = assess(dep, observation, old, timestamp)
            current["updated"] = old.get("updated") if fresh else timestamp
            # Reading status is not a new known-compatible observation.
            current["last_known_compatible_at"] = old.get("last_known_compatible_at") if _date(old.get("last_known_compatible_at")) else None
        entries.append(current)
    payload = summarize(entries, timestamp)
    store.write_json("compatibility.json", payload, mode=0o600)
    return payload


def observation_from_ha(report):
    """Translate sanitized discovery evidence; never accept raw registry objects."""
    meta = report.get("compatibility", {}) if type(report) is dict else {}
    failed = meta.get("failed_capability")
    caps = {name: None for name in ("version_metadata", "authentication", "device_registry", "entity_registry", "area_registry", "config_entries")}
    if report.get("result") == "PASS" and meta.get("status") in {"COMPATIBLE", "COMPATIBLE_UPDATED"}:
        caps = {name: True for name in caps}
    elif meta.get("status") == "INCOMPATIBLE" and failed in caps: caps[failed] = False
    return {"observed_version": safe_version(meta.get("observed_version")), "capabilities": caps,
            "available": False if meta.get("status") == "DEPENDENCY_UNAVAILABLE" else None}


def lease_observation(statuses, observed_version=None):
    statuses = set(statuses)
    available = bool(statuses - {"missing", "unreadable", "io_error"})
    bad = bool(statuses & {"malformed", "unsupported", "partial"})
    # Empty is structurally valid but cannot prove that a format still matches.
    shape = False if bad else True if "found" in statuses else None
    return {"available": available if statuses else None, "observed_version": safe_version(observed_version),
            "capabilities": {"lease_columns": shape}}


def nut_observation(text, available=True, observed_version=None):
    # Only currently consumed status/voltage semantics; no private UPS identity.
    fields = {}
    if type(text) is str and len(text) <= 65536:
        for line in text.splitlines():
            if ': ' in line:
                key, value = line.split(': ', 1)
                fields[key] = value
    statuses = fields.get('ups.status', '').split()
    supported = {"OL", "OB", "LB", "HB", "RB", "CHRG", "DISCHRG", "BYPASS", "CAL", "OFF", "OVER", "TRIM", "BOOST", "FSD"}
    return {"available": available, "observed_version": safe_version(observed_version),
        "capabilities": {"ups_status": bool(statuses) and set(statuses) <= supported}}


def go2rtc_observation(value, available=True, observed_version=None):
    # Adapter for a future/current operator-supplied API observation; no request.
    valid = type(value) is dict and all(type(k) is str and type(v) is dict for k, v in value.items())
    return {"available": available, "observed_version": safe_version(observed_version), "capabilities": {"streams_object": valid}}


def python_observation(version, implementation="CPython", supported_line=None):
    token = safe_version(version)
    parts = token.split('.') if token else []
    valid = implementation == "CPython" and len(parts) >= 2 and all(p.isdecimal() for p in parts[:2])
    line = '.'.join(parts[:2])
    passed = valid and (line == supported_line if supported_line else tuple(map(int, parts[:2])) >= (3, 10))
    return {"available": True, "observed_version": token, "capabilities": {"cpython_line": passed}}


@contextmanager
def state_lock(store):
    path = store.path(".compatibility.lock")
    fd = os.open(path, os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0), 0o600)
    deadline = time.monotonic() + 3
    locked = False
    try:
        metadata = os.fstat(fd)
        if not stat.S_ISREG(metadata.st_mode) or (os.name != "nt" and (metadata.st_uid != os.geteuid() or stat.S_IMODE(metadata.st_mode) != 0o600)):
            raise ValueError("compatibility lock ownership unavailable")
        if metadata.st_size == 0:
            os.write(fd, b"0")
        while not locked:
            try:
                if os.name == "nt":
                    import msvcrt
                    os.lseek(fd, 0, os.SEEK_SET)
                    msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                locked = True
            except OSError:
                if time.monotonic() >= deadline:
                    raise ValueError("compatibility state lock unavailable") from None
                time.sleep(.02)
        yield
    finally:
        if locked:
            if os.name == "nt":
                import msvcrt
                os.lseek(fd, 0, os.SEEK_SET)
                msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)


def update_status(store, registry, observations, timestamp, max_age_seconds=129600):
    with state_lock(store):
        return _update_status(store, registry, observations, timestamp, max_age_seconds)


def refresh_status(store, home, observations, timestamp, source_home=None):
    path = home / "governance" / "compatibility-contracts.json"
    if not path.is_file() and source_home is not None:
        path = source_home / "governance" / "compatibility-contracts.json"
    return update_status(store, load_registry(path), observations, timestamp)


def summary_fields(payload):
    return {key: value for key, value in payload.items() if key != "dependencies"}


def isolated_runtime_observations(executable, runner=subprocess.run):
    """Local, bounded probes only; never install, repair or access a remote host."""
    probe = "import json,sys;print(json.dumps({'version':'.'.join(map(str,sys.version_info[:3])),'implementation':sys.implementation.name}))"
    try:
        process = runner([str(executable), "-I", "-B", "-S", "-c", probe],
                         capture_output=True, text=True, timeout=5, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return {"pe4_python": {"available": False, "capabilities": {"interpreter_start": None, "runtime_api": None}}}
    identity = None
    if process.returncode == 0 and len(process.stdout) <= 4096:
        try: identity = json.loads(process.stdout)
        except (ValueError, TypeError): pass
    usable = type(identity) is dict and identity.get("implementation") == "cpython" and safe_version(identity.get("version")) is not None
    version = safe_version(identity.get("version")) if usable else None
    result = {"pe4_python": {"available": True, "observed_version": version,
        "identity_matches": version == "3.11.2" if usable else None,
        "capabilities": {"interpreter_start": process.returncode == 0, "runtime_api": usable}}}
    if not usable: return result
    code = "import json,websockets;from websockets.asyncio.client import connect;print(json.dumps({'version':websockets.__version__,'api':isinstance(connect,type) and callable(getattr(connect,'process_redirect',None))}))"
    try:
        module = runner([str(executable), "-I", "-B", "-c", code], capture_output=True,
                        text=True, timeout=5, check=False)
        data = json.loads(module.stdout) if module.returncode == 0 and len(module.stdout) <= 4096 else {}
        valid = type(data) is dict and data.get("api") is True
        result["pe4_websockets"] = {"available": True, "observed_version": safe_version(data.get("version")),
            "identity_matches": data.get("version") == "16.1.1" if data else None,
            "capabilities": {"import_api": valid, "bounded_connect": valid}}
    except (OSError, subprocess.TimeoutExpired, ValueError, TypeError):
        result["pe4_websockets"] = {"available": False, "capabilities": {"import_api": None, "bounded_connect": None}}
    return result


def mqtt_observation(error=None):
    """Classify only established transport evidence; local bugs stay unknown."""
    from ..mqtt import MqttPublishError
    if error is None:
        return {"available": True, "capabilities": {"connack": True, "publish": True}}
    if isinstance(error, OSError):
        return {"available": False, "capabilities": {"connack": None, "publish": None}}
    caps={"connack": None, "publish": None}
    if isinstance(error, MqttPublishError) and error.capability in caps:
        caps[error.capability]=False
    return {"capabilities": caps}
