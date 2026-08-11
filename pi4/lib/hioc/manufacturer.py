"""Offline, private PE-3.1 manufacturer enrichment primitives."""
from __future__ import annotations

import copy, hashlib, json, os, pathlib, re, stat, tempfile, time, unicodedata
from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType
from typing import TypeAlias

try:
    import fcntl
except ImportError:  # Windows repository host
    fcntl = None

MANUFACTURER_DB_SCHEMA_VERSION = "1.0"
MANUFACTURER_MANIFEST_SCHEMA_VERSION = "1.0"
MANUFACTURER_SIDECAR_SCHEMA_VERSION = "1.0"
MANUFACTURER_STATUS_SCHEMA_VERSION = "1.0"
MANUFACTURER_GENERATOR_VERSION = "hioc-manufacturer-1"
ASSIGNMENT_CLASSES = frozenset({"MA-L", "MA-M", "MA-S"})
LOOKUP_STATUSES = frozenset({"matched", "conflicting_assignment", "unknown_prefix", "invalid_address", "multicast_address", "locally_administered_address", "missing_address", "unsupported_address_type"})
MANUFACTURER_CONFIDENCES = frozenset({"high", "unknown"})
MANUFACTURER_STATUS_VALUES = frozenset({"online", "degraded", "unavailable", "error"})
MANUFACTURER_ERROR_CODES = frozenset({
    "MANUFACTURER_NOT_CONFIGURED", "MANUFACTURER_DATABASE_MISSING", "MANUFACTURER_MANIFEST_MISSING",
    "MANUFACTURER_DATABASE_UNREADABLE", "MANUFACTURER_MANIFEST_UNREADABLE",
    "MANUFACTURER_DATABASE_SCHEMA_INVALID", "MANUFACTURER_MANIFEST_SCHEMA_INVALID",
    "MANUFACTURER_DATABASE_CHECKSUM_MISMATCH", "MANUFACTURER_DATABASE_SEMANTIC_MISMATCH",
    "MANUFACTURER_VERSION_UNSUPPORTED", "MANUFACTURER_DATASET_EMPTY", "MANUFACTURER_DATASET_CONFLICT",
    "MANUFACTURER_DETERMINISM_FAILED", "MANUFACTURER_INVENTORY_MISSING", "MANUFACTURER_INVENTORY_INVALID",
    "MANUFACTURER_LOCK_TIMEOUT", "MANUFACTURER_SIDECAR_INVALID", "MANUFACTURER_SIDECAR_WRITE_FAILED",
    "MANUFACTURER_STATUS_INVALID", "MANUFACTURER_STATUS_WRITE_FAILED", "MANUFACTURER_PERMISSION_ERROR",
    "MANUFACTURER_PRIVACY_REFUSED", "MANUFACTURER_INTERNAL_ERROR",
})
__all__ = (
    "MANUFACTURER_DB_SCHEMA_VERSION", "MANUFACTURER_MANIFEST_SCHEMA_VERSION",
    "MANUFACTURER_SIDECAR_SCHEMA_VERSION", "MANUFACTURER_STATUS_SCHEMA_VERSION",
    "MANUFACTURER_GENERATOR_VERSION", "ASSIGNMENT_CLASSES", "LOOKUP_STATUSES",
    "MANUFACTURER_CONFIDENCES", "MANUFACTURER_STATUS_VALUES", "MANUFACTURER_ERROR_CODES",
    "ManufacturerRecord", "ManufacturerManifest", "ManufacturerDatabase",
    "ManufacturerLookupResult", "ManufacturerSidecar", "ManufacturerStatus",
    "ManufacturerError", "ManufacturerInputError", "ManufacturerValidationError",
    "ManufacturerUnavailableError", "ManufacturerIntegrityError", "ManufacturerLockError",
    "ManufacturerWriteError", "ManufacturerPrivacyError", "normalize_eui48",
    "normalize_eui64", "is_multicast_address", "is_locally_administered_address",
    "normalize_organization", "validate_database", "validate_manifest",
    "validate_manufacturer_sidecar", "validate_manufacturer_status", "load_database",
    "lookup_manufacturer_eui48", "lookup_manufacturer_eui64", "build_manufacturer_sidecar",
    "canonical_json_bytes", "semantic_sha256", "file_sha256", "write_json_atomic",
)

DB_KEYS = ("schema_version", "dataset_id", "dataset_version", "parser_version", "semantic_sha256", "record_count", "ma_l_count", "ma_m_count", "ma_s_count", "conflict_count", "records", "conflicts")
RECORD_KEYS = ("prefix", "prefix_length", "assignment_class", "organization")
CONFLICT_KEYS = ("prefix", "prefix_length", "assignment_class", "variant_count")
MANIFEST_KEYS = ("schema_version", "database_filename", "database_sha256", "database_size_bytes", "database_semantic_sha256", "database_schema_version", "dataset_id", "dataset_version", "parser_version", "record_count", "ma_l_count", "ma_m_count", "ma_s_count", "duplicate_count", "conflict_count", "source_files", "build")
SOURCE_KEYS = ("source_class", "source_filename", "source_sha256", "source_size_bytes")
SIDECAR_KEYS = ("schema_version", "generated_at", "dataset_id", "dataset_version", "dataset_semantic_sha256", "record_count", "matched_count", "unknown_count", "excluded_count", "invalid_count", "records")
SIDECAR_RECORD_KEYS = ("stable_device_id", "lookup_status", "manufacturer", "confidence", "assignment_class", "matched_prefix", "matched_prefix_length", "source", "dataset_version", "dataset_semantic_sha256", "lookup_method")
STATUS_KEYS = ("schema_version", "updated", "status", "dataset_available", "dataset_id", "dataset_version", "dataset_semantic_sha256", "record_count", "matched_count", "unknown_count", "excluded_count", "invalid_count", "conflict_count", "generator", "error_code", "error_message")
CLASS_META = {"MA-L": (24, 6, "ma_l_count"), "MA-M": (28, 7, "ma_m_count"), "MA-S": (36, 9, "ma_s_count")}
ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{0,63}$")
VERSION_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
STABLE_RE = re.compile(r"^dev_[0-9a-f]{16}$")
TIME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}Z$")

class ManufacturerError(Exception):
    default_exit_code = 70
    EXIT_OVERRIDES = {
        "MANUFACTURER_DATABASE_SEMANTIC_MISMATCH": 8, "MANUFACTURER_VERSION_UNSUPPORTED": 9,
        "MANUFACTURER_DATASET_CONFLICT": 10, "MANUFACTURER_DETERMINISM_FAILED": 11,
        "MANUFACTURER_INVENTORY_MISSING": 14, "MANUFACTURER_INVENTORY_INVALID": 14,
        "MANUFACTURER_SIDECAR_INVALID": 15, "MANUFACTURER_STATUS_INVALID": 16,
        "MANUFACTURER_STATUS_WRITE_FAILED": 16, "MANUFACTURER_PERMISSION_ERROR": 5,
        "MANUFACTURER_LOCK_TIMEOUT": 17, "MANUFACTURER_PRIVACY_REFUSED": 18,
        "MANUFACTURER_INTERNAL_ERROR": 70,
    }
    def __init__(self, code: str, message: str):
        self.code = code if code in MANUFACTURER_ERROR_CODES else "MANUFACTURER_INTERNAL_ERROR"
        safe = " ".join(str(message).split())
        safe = re.sub(r"(?:[A-Za-z]:)?[^\s]*[\\/]([^\\/\s]+)", r"\1", safe)[:160]
        self.safe_message = safe
        self.exit_code = self.EXIT_OVERRIDES.get(self.code, self.default_exit_code)
        super().__init__(safe)
class ManufacturerInputError(ManufacturerError): default_exit_code = 3
class ManufacturerValidationError(ManufacturerError): default_exit_code = 6
class ManufacturerUnavailableError(ManufacturerError): default_exit_code = 4
class ManufacturerIntegrityError(ManufacturerError): default_exit_code = 7
class ManufacturerLockError(ManufacturerError): default_exit_code = 17
class ManufacturerWriteError(ManufacturerError): default_exit_code = 12
class ManufacturerPrivacyError(ManufacturerError): default_exit_code = 18

@dataclass(frozen=True)
class ManufacturerRecord:
    prefix: str; prefix_length: int; assignment_class: str; organization: str
@dataclass(frozen=True)
class ManufacturerManifest:
    document: dict; database_sha256: str; database_semantic_sha256: str
@dataclass(frozen=True)
class ManufacturerDatabase:
    document: dict; manifest: ManufacturerManifest; ma_l: MappingProxyType; ma_m: MappingProxyType; ma_s: MappingProxyType; conflicts: MappingProxyType
@dataclass(frozen=True)
class ManufacturerLookupResult:
    lookup_status: str; manufacturer: str | None; confidence: str; assignment_class: str | None; matched_prefix: str | None; matched_prefix_length: int | None; lookup_method: str
ManufacturerSidecar: TypeAlias = dict
ManufacturerStatus: TypeAlias = dict

def _validation(code, message): return ManufacturerValidationError(code, message)
def _exact(value, keys, subject, code="MANUFACTURER_DATABASE_SCHEMA_INVALID"):
    if not isinstance(value, dict) or tuple(value.keys()) != keys: raise _validation(code, f"{subject} fields or ordering are invalid")
    return value
def _count(value, subject, code="MANUFACTURER_DATABASE_SCHEMA_INVALID"):
    if not isinstance(value, int) or isinstance(value, bool) or value < 0: raise _validation(code, f"{subject} is invalid")
    return value
def _timestamp(value, code="MANUFACTURER_SIDECAR_INVALID"):
    if not isinstance(value, str) or not TIME_RE.fullmatch(value): raise _validation(code, "timestamp is invalid")
    try: datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError as exc: raise _validation(code, "timestamp is invalid") from exc
def _normalize_json(value):
    if isinstance(value,str): return unicodedata.normalize("NFC",value)
    if isinstance(value,list): return [_normalize_json(item) for item in value]
    if isinstance(value,dict):
        normalized={}
        for key,item in value.items():
            new_key=_normalize_json(key)
            if not isinstance(new_key,str) or new_key in normalized: raise _validation("MANUFACTURER_DATABASE_SCHEMA_INVALID","JSON object key is invalid")
            normalized[new_key]=_normalize_json(item)
        return normalized
    return value

def canonical_json_bytes(document: object) -> bytes:
    try:
        normalized=_normalize_json(document)
        return (json.dumps(normalized, ensure_ascii=False, allow_nan=False, indent=2, separators=(",", ": ")) + "\n").encode("utf-8")
    except ManufacturerError: raise
    except (TypeError, ValueError, UnicodeError) as exc: raise _validation("MANUFACTURER_DATABASE_SCHEMA_INVALID", "unsupported JSON value") from exc
def semantic_sha256(document: object) -> str: return hashlib.sha256(canonical_json_bytes(document)).hexdigest()
def file_sha256(path: pathlib.Path) -> str:
    path = pathlib.Path(path)
    try:
        info = path.lstat()
        if path.is_symlink() or not stat.S_ISREG(info.st_mode): raise ManufacturerUnavailableError("MANUFACTURER_DATABASE_UNREADABLE", "file is not regular")
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for block in iter(lambda: handle.read(1024 * 1024), b""): digest.update(block)
        return digest.hexdigest()
    except ManufacturerError: raise
    except FileNotFoundError as exc: raise ManufacturerUnavailableError("MANUFACTURER_DATABASE_MISSING", "required file is missing") from exc
    except PermissionError as exc: raise ManufacturerUnavailableError("MANUFACTURER_PERMISSION_ERROR", "permission refused") from exc
    except OSError as exc: raise ManufacturerUnavailableError("MANUFACTURER_DATABASE_UNREADABLE", "file is unreadable") from exc

def normalize_eui48(value: str) -> str:
    if not isinstance(value, str): raise ManufacturerInputError("MANUFACTURER_INVENTORY_INVALID", "EUI-48 must be text")
    forms = (r"[0-9A-Fa-f]{12}", r"(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}", r"(?:[0-9A-Fa-f]{2}-){5}[0-9A-Fa-f]{2}", r"(?:[0-9A-Fa-f]{4}\.){2}[0-9A-Fa-f]{4}")
    if not any(re.fullmatch(form, value) for form in forms): raise ManufacturerInputError("MANUFACTURER_INVENTORY_INVALID", "EUI-48 is invalid")
    raw = re.sub("[:-]|\\.", "", value).upper()
    if raw in {"0" * 12, "F" * 12}: raise ManufacturerInputError("MANUFACTURER_INVENTORY_INVALID", "EUI-48 is invalid")
    return ":".join(raw[i:i+2] for i in range(0, 12, 2))
def normalize_eui64(value: str) -> str:
    if not isinstance(value, str): raise ManufacturerInputError("MANUFACTURER_INVENTORY_INVALID", "EUI-64 must be text")
    forms = (r"[0-9A-Fa-f]{16}", r"(?:[0-9A-Fa-f]{2}:){7}[0-9A-Fa-f]{2}", r"(?:[0-9A-Fa-f]{2}-){7}[0-9A-Fa-f]{2}")
    if not any(re.fullmatch(form, value) for form in forms): raise ManufacturerInputError("MANUFACTURER_INVENTORY_INVALID", "EUI-64 is invalid")
    raw = re.sub("[:-]", "", value).upper()
    if raw in {"0" * 16, "F" * 16}: raise ManufacturerInputError("MANUFACTURER_INVENTORY_INVALID", "EUI-64 is invalid")
    return ":".join(raw[i:i+2] for i in range(0, 16, 2))
def _address_bytes(normalized):
    if not isinstance(normalized, str) or not re.fullmatch(r"(?:[0-9A-F]{2}:)+(?:[0-9A-F]{2})", normalized): raise ManufacturerInputError("MANUFACTURER_INVENTORY_INVALID", "address is not canonical")
    return bytes.fromhex(normalized.replace(":", ""))
def is_multicast_address(normalized: str) -> bool: return bool(_address_bytes(normalized)[0] & 1)
def is_locally_administered_address(normalized: str) -> bool: return bool(_address_bytes(normalized)[0] & 2)
def normalize_organization(value: str) -> str:
    if not isinstance(value, str): raise ManufacturerInputError("MANUFACTURER_DATABASE_SCHEMA_INVALID", "organization must be text")
    value = value.replace("\u200b", "").replace("\u200e", "").replace("\t", " ")
    value = unicodedata.normalize("NFC", value)
    prohibited = any(ch in "\r\n" or unicodedata.category(ch)[0] == "C" or unicodedata.category(ch) in {"Co", "Cn"} for ch in value)
    value = " ".join(value.split())
    if prohibited: raise ManufacturerInputError("MANUFACTURER_DATABASE_SCHEMA_INVALID", "organization contains prohibited characters")
    if not 1 <= len(value) <= 256: raise ManufacturerInputError("MANUFACTURER_DATABASE_SCHEMA_INVALID", "organization length is invalid")
    return value

def validate_database(document: object) -> dict:
    value = _exact(document, DB_KEYS, "database")
    if value["schema_version"] != MANUFACTURER_DB_SCHEMA_VERSION or value["parser_version"] != MANUFACTURER_GENERATOR_VERSION: raise _validation("MANUFACTURER_VERSION_UNSUPPORTED", "database version is unsupported")
    if not isinstance(value["dataset_id"], str) or not ID_RE.fullmatch(value["dataset_id"]): raise _validation("MANUFACTURER_DATABASE_SCHEMA_INVALID", "dataset ID is invalid")
    if not isinstance(value["dataset_version"], str) or not VERSION_RE.fullmatch(value["dataset_version"]): raise _validation("MANUFACTURER_DATABASE_SCHEMA_INVALID", "dataset version is invalid")
    if not isinstance(value["semantic_sha256"], str) or not SHA_RE.fullmatch(value["semantic_sha256"]): raise _validation("MANUFACTURER_DATABASE_SCHEMA_INVALID", "semantic digest is invalid")
    counts = {key: _count(value[key], key) for key in ("record_count", "ma_l_count", "ma_m_count", "ma_s_count", "conflict_count")}
    if counts["record_count"] == 0: raise _validation("MANUFACTURER_DATASET_EMPTY", "dataset is empty")
    records, conflicts = value["records"], value["conflicts"]
    if not isinstance(records, dict) or list(records) != sorted(records) or len(records) != counts["record_count"]: raise _validation("MANUFACTURER_DATABASE_SCHEMA_INVALID", "record count or ordering is invalid")
    if not isinstance(conflicts, dict) or list(conflicts) != sorted(conflicts) or len(conflicts) != counts["conflict_count"] or set(records) & set(conflicts): raise _validation("MANUFACTURER_DATABASE_SCHEMA_INVALID", "conflict count, ordering, or intersection is invalid")
    actual = {"ma_l_count": 0, "ma_m_count": 0, "ma_s_count": 0}
    for key, record in records.items():
        _exact(record, RECORD_KEYS, "record")
        cls = record["assignment_class"]
        if cls not in CLASS_META: raise _validation("MANUFACTURER_DATABASE_SCHEMA_INVALID", "assignment class is invalid")
        bits, width, count_key = CLASS_META[cls]; prefix = record["prefix"]
        if record["prefix_length"] != bits or not isinstance(prefix, str) or not re.fullmatch(rf"[0-9A-F]{{{width}}}", prefix) or key != f"{bits}:{prefix}": raise _validation("MANUFACTURER_DATABASE_SCHEMA_INVALID", "prefix record is invalid")
        try: normalized = normalize_organization(record["organization"])
        except ManufacturerInputError as exc: raise _validation("MANUFACTURER_DATABASE_SCHEMA_INVALID", exc.safe_message) from exc
        if normalized != record["organization"]: raise _validation("MANUFACTURER_DATABASE_SCHEMA_INVALID", "organization is not normalized")
        actual[count_key] += 1
    for key, conflict in conflicts.items():
        _exact(conflict, CONFLICT_KEYS, "conflict")
        cls = conflict["assignment_class"]
        if cls not in CLASS_META: raise _validation("MANUFACTURER_DATABASE_SCHEMA_INVALID", "conflict assignment class is invalid")
        bits, width, _ = CLASS_META[cls]; prefix = conflict["prefix"]
        if conflict["prefix_length"] != bits or not isinstance(prefix, str) or not re.fullmatch(rf"[0-9A-F]{{{width}}}", prefix) or key != f"{bits}:{prefix}" or _count(conflict["variant_count"], "variant count") < 2: raise _validation("MANUFACTURER_DATABASE_SCHEMA_INVALID", "conflict entry is invalid")
    if sum(actual.values()) != counts["record_count"] or any(actual[key] != counts[key] for key in actual): raise _validation("MANUFACTURER_DATABASE_SCHEMA_INVALID", "class counts are invalid")
    payload = {key: copy.deepcopy(item) for key, item in value.items() if key != "semantic_sha256"}
    if semantic_sha256(payload) != value["semantic_sha256"]: raise ManufacturerIntegrityError("MANUFACTURER_DATABASE_SEMANTIC_MISMATCH", "semantic digest mismatch")
    return copy.deepcopy(value)

def validate_manifest(document: object) -> dict:
    value = _exact(document, MANIFEST_KEYS, "manifest", "MANUFACTURER_MANIFEST_SCHEMA_INVALID")
    if value["schema_version"] != MANUFACTURER_MANIFEST_SCHEMA_VERSION or value["database_schema_version"] != MANUFACTURER_DB_SCHEMA_VERSION or value["parser_version"] != MANUFACTURER_GENERATOR_VERSION: raise _validation("MANUFACTURER_VERSION_UNSUPPORTED", "manifest version is unsupported")
    if value["database_filename"] != "manufacturer-db.json": raise _validation("MANUFACTURER_MANIFEST_SCHEMA_INVALID", "database filename is invalid")
    for key in ("database_sha256", "database_semantic_sha256"):
        if not isinstance(value[key], str) or not SHA_RE.fullmatch(value[key]): raise _validation("MANUFACTURER_MANIFEST_SCHEMA_INVALID", "manifest digest is invalid")
    for key in ("database_size_bytes", "record_count", "ma_l_count", "ma_m_count", "ma_s_count", "duplicate_count", "conflict_count"): _count(value[key], key, "MANUFACTURER_MANIFEST_SCHEMA_INVALID")
    if value["database_size_bytes"] < 1: raise _validation("MANUFACTURER_MANIFEST_SCHEMA_INVALID", "manifest size is invalid")
    if not isinstance(value["dataset_id"], str) or not ID_RE.fullmatch(value["dataset_id"]) or not isinstance(value["dataset_version"], str) or not VERSION_RE.fullmatch(value["dataset_version"]): raise _validation("MANUFACTURER_MANIFEST_SCHEMA_INVALID", "manifest identity is invalid")
    sources = value["source_files"]
    if not isinstance(sources, list) or len(sources) != 3 or [x.get("source_class") if isinstance(x, dict) else None for x in sources] != ["MA-L", "MA-M", "MA-S"]: raise _validation("MANUFACTURER_MANIFEST_SCHEMA_INVALID", "source ordering is invalid")
    for source in sources:
        _exact(source, SOURCE_KEYS, "source", "MANUFACTURER_MANIFEST_SCHEMA_INVALID"); name = source["source_filename"]
        if not isinstance(name, str) or not name or pathlib.PurePath(name).name != name or "/" in name or "\\" in name or "://" in name: raise _validation("MANUFACTURER_MANIFEST_SCHEMA_INVALID", "source filename is invalid")
        if not isinstance(source["source_sha256"], str) or not SHA_RE.fullmatch(source["source_sha256"]) or _count(source["source_size_bytes"], "source size", "MANUFACTURER_MANIFEST_SCHEMA_INVALID") < 1: raise _validation("MANUFACTURER_MANIFEST_SCHEMA_INVALID", "source identity is invalid")
    build = _exact(value["build"], ("canonicalization_version", "deterministic_build_verified"), "build proof", "MANUFACTURER_MANIFEST_SCHEMA_INVALID")
    if build != {"canonicalization_version": "1", "deterministic_build_verified": True}: raise _validation("MANUFACTURER_MANIFEST_SCHEMA_INVALID", "build proof is invalid")
    return copy.deepcopy(value)

def _validate_sidecar_record(key, record):
    _exact(record, SIDECAR_RECORD_KEYS, "sidecar record", "MANUFACTURER_SIDECAR_INVALID")
    if not STABLE_RE.fullmatch(key) or record["stable_device_id"] != key or record["lookup_status"] not in LOOKUP_STATUSES: raise _validation("MANUFACTURER_SIDECAR_INVALID", "sidecar identity or status is invalid")
    if record["source"] != "ieee_registration_authority" or not isinstance(record["dataset_version"], str) or not VERSION_RE.fullmatch(record["dataset_version"]) or not isinstance(record["dataset_semantic_sha256"], str) or not SHA_RE.fullmatch(record["dataset_semantic_sha256"]): raise _validation("MANUFACTURER_SIDECAR_INVALID", "sidecar provenance is invalid")
    if record["lookup_status"] == "matched":
        try: normalized = normalize_organization(record["manufacturer"])
        except ManufacturerInputError as exc: raise _validation("MANUFACTURER_SIDECAR_INVALID", exc.safe_message) from exc
        if normalized != record["manufacturer"] or record["confidence"] != "high" or record["assignment_class"] not in ASSIGNMENT_CLASSES or record["lookup_method"] != "longest_prefix_v1": raise _validation("MANUFACTURER_SIDECAR_INVALID", "matched record is invalid")
        bits, width, _ = CLASS_META[record["assignment_class"]]
        if record["matched_prefix_length"] != bits or not isinstance(record["matched_prefix"], str) or not re.fullmatch(rf"[0-9A-F]{{{width}}}", record["matched_prefix"]): raise _validation("MANUFACTURER_SIDECAR_INVALID", "matched prefix is invalid")
    elif record["confidence"] != "unknown" or record["lookup_method"] != "none" or any(record[x] is not None for x in ("manufacturer", "assignment_class", "matched_prefix", "matched_prefix_length")): raise _validation("MANUFACTURER_SIDECAR_INVALID", "nonmatch record is invalid")

def validate_manufacturer_sidecar(document: object) -> dict:
    value = _exact(document, SIDECAR_KEYS, "sidecar", "MANUFACTURER_SIDECAR_INVALID")
    if value["schema_version"] != MANUFACTURER_SIDECAR_SCHEMA_VERSION: raise _validation("MANUFACTURER_VERSION_UNSUPPORTED", "sidecar version is unsupported")
    _timestamp(value["generated_at"])
    if not isinstance(value["dataset_id"], str) or not ID_RE.fullmatch(value["dataset_id"]) or not isinstance(value["dataset_version"], str) or not VERSION_RE.fullmatch(value["dataset_version"]) or not isinstance(value["dataset_semantic_sha256"], str) or not SHA_RE.fullmatch(value["dataset_semantic_sha256"]): raise _validation("MANUFACTURER_SIDECAR_INVALID", "sidecar identity is invalid")
    counts = {key: _count(value[key], key, "MANUFACTURER_SIDECAR_INVALID") for key in ("record_count", "matched_count", "unknown_count", "excluded_count", "invalid_count")}; records = value["records"]
    if not isinstance(records, dict) or list(records) != sorted(records) or len(records) != counts["record_count"] or sum(counts[k] for k in counts if k != "record_count") != counts["record_count"]: raise _validation("MANUFACTURER_SIDECAR_INVALID", "sidecar counts are invalid")
    actual = dict.fromkeys(("matched_count", "unknown_count", "excluded_count", "invalid_count"), 0)
    for key, record in records.items():
        _validate_sidecar_record(key, record); status = record["lookup_status"]
        bucket = "matched_count" if status == "matched" else "unknown_count" if status in {"conflicting_assignment", "unknown_prefix", "unsupported_address_type"} else "excluded_count" if status in {"multicast_address", "locally_administered_address"} else "invalid_count"
        actual[bucket] += 1
        if record["dataset_version"] != value["dataset_version"] or record["dataset_semantic_sha256"] != value["dataset_semantic_sha256"]: raise _validation("MANUFACTURER_SIDECAR_INVALID", "sidecar provenance differs")
    if actual != {key: counts[key] for key in actual}: raise _validation("MANUFACTURER_SIDECAR_INVALID", "sidecar partition counts are invalid")
    return copy.deepcopy(value)

def validate_manufacturer_status(document: object) -> dict:
    value = _exact(document, STATUS_KEYS, "status", "MANUFACTURER_STATUS_INVALID")
    if value["schema_version"] != MANUFACTURER_STATUS_SCHEMA_VERSION: raise _validation("MANUFACTURER_VERSION_UNSUPPORTED", "status version is unsupported")
    _timestamp(value["updated"], "MANUFACTURER_STATUS_INVALID")
    if value["status"] not in MANUFACTURER_STATUS_VALUES or not isinstance(value["dataset_available"], bool) or value["generator"] != MANUFACTURER_GENERATOR_VERSION: raise _validation("MANUFACTURER_STATUS_INVALID", "status enum is invalid")
    for key in ("record_count", "matched_count", "unknown_count", "excluded_count", "invalid_count", "conflict_count"): _count(value[key], key, "MANUFACTURER_STATUS_INVALID")
    if value["error_code"] is not None and value["error_code"] not in MANUFACTURER_ERROR_CODES: raise _validation("MANUFACTURER_STATUS_INVALID", "status error code is invalid")
    if value["error_message"] is not None and (not isinstance(value["error_message"], str) or len(value["error_message"]) > 160 or "\n" in value["error_message"]): raise _validation("MANUFACTURER_STATUS_INVALID", "status error message is invalid")
    identity = (value["dataset_id"], value["dataset_version"], value["dataset_semantic_sha256"])
    if value["dataset_available"]:
        if not isinstance(identity[0], str) or not ID_RE.fullmatch(identity[0]) or not isinstance(identity[1], str) or not VERSION_RE.fullmatch(identity[1]) or not isinstance(identity[2], str) or not SHA_RE.fullmatch(identity[2]): raise _validation("MANUFACTURER_STATUS_INVALID", "status dataset identity is invalid")
    elif any(x is not None for x in identity): raise _validation("MANUFACTURER_STATUS_INVALID", "unavailable dataset identity must be null")
    if value["status"] == "online" and (not value["dataset_available"] or value["error_code"] is not None or value["error_message"] is not None): raise _validation("MANUFACTURER_STATUS_INVALID", "online status is inconsistent")
    return copy.deepcopy(value)

def _safe_file(path, missing_code, unreadable_code):
    try:
        info = path.lstat()
        if path.is_symlink() or not stat.S_ISREG(info.st_mode): raise ManufacturerUnavailableError(unreadable_code, "file is unsafe")
        if os.name == "posix" and stat.S_IMODE(info.st_mode) & ~0o600: raise ManufacturerUnavailableError("MANUFACTURER_PERMISSION_ERROR", "file mode is unsafe")
        if os.name == "posix" and hasattr(os,"getuid") and info.st_uid != os.getuid(): raise ManufacturerUnavailableError("MANUFACTURER_PERMISSION_ERROR", "file owner is unsafe")
        parent_info=path.parent.lstat()
        if path.parent.is_symlink() or not stat.S_ISDIR(parent_info.st_mode) or os.name=="posix" and stat.S_IMODE(parent_info.st_mode)&~0o700: raise ManufacturerUnavailableError("MANUFACTURER_PERMISSION_ERROR", "database directory is unsafe")
    except FileNotFoundError as exc: raise ManufacturerUnavailableError(missing_code, "file is missing") from exc
def load_database(database_path: pathlib.Path, manifest_path: pathlib.Path) -> ManufacturerDatabase:
    database_path, manifest_path = pathlib.Path(database_path), pathlib.Path(manifest_path)
    _safe_file(database_path, "MANUFACTURER_DATABASE_MISSING", "MANUFACTURER_DATABASE_UNREADABLE"); _safe_file(manifest_path, "MANUFACTURER_MANIFEST_MISSING", "MANUFACTURER_MANIFEST_UNREADABLE")
    try: db_bytes = database_path.read_bytes()
    except PermissionError as exc: raise ManufacturerUnavailableError("MANUFACTURER_PERMISSION_ERROR", "permission refused") from exc
    except OSError as exc: raise ManufacturerUnavailableError("MANUFACTURER_DATABASE_UNREADABLE", "database is unreadable") from exc
    try: mf_bytes = manifest_path.read_bytes()
    except PermissionError as exc: raise ManufacturerUnavailableError("MANUFACTURER_PERMISSION_ERROR", "permission refused") from exc
    except OSError as exc: raise ManufacturerUnavailableError("MANUFACTURER_MANIFEST_UNREADABLE", "manifest is unreadable") from exc
    try: database = validate_database(json.loads(db_bytes.decode("utf-8"), object_pairs_hook=dict))
    except ManufacturerError: raise
    except (UnicodeError, json.JSONDecodeError) as exc: raise ManufacturerValidationError("MANUFACTURER_DATABASE_SCHEMA_INVALID", "database JSON is invalid") from exc
    try: manifest = validate_manifest(json.loads(mf_bytes.decode("utf-8"), object_pairs_hook=dict))
    except ManufacturerError: raise
    except (UnicodeError, json.JSONDecodeError) as exc: raise ManufacturerValidationError("MANUFACTURER_MANIFEST_SCHEMA_INVALID", "manifest JSON is invalid") from exc
    if hashlib.sha256(db_bytes).hexdigest() != manifest["database_sha256"] or len(db_bytes) != manifest["database_size_bytes"]: raise ManufacturerIntegrityError("MANUFACTURER_DATABASE_CHECKSUM_MISMATCH", "database checksum or size mismatch")
    for key in ("dataset_id", "dataset_version", "parser_version", "record_count", "ma_l_count", "ma_m_count", "ma_s_count", "conflict_count"):
        if database[key] != manifest[key]: raise ManufacturerValidationError("MANUFACTURER_MANIFEST_SCHEMA_INVALID", "database and manifest differ")
    if database["semantic_sha256"] != manifest["database_semantic_sha256"]: raise ManufacturerIntegrityError("MANUFACTURER_DATABASE_SEMANTIC_MISMATCH", "semantic digest mismatch")
    maps = {key: {} for key in ASSIGNMENT_CLASSES}
    for record in database["records"].values(): maps[record["assignment_class"]][record["prefix"]] = ManufacturerRecord(**record)
    wrapped = ManufacturerManifest(manifest, manifest["database_sha256"], manifest["database_semantic_sha256"])
    conflict_map = {key: MappingProxyType(dict(item)) for key, item in database["conflicts"].items()}
    return ManufacturerDatabase(database, wrapped, MappingProxyType(maps["MA-L"]), MappingProxyType(maps["MA-M"]), MappingProxyType(maps["MA-S"]), MappingProxyType(conflict_map))

def _lookup(status, record=None):
    if record: return ManufacturerLookupResult(status, record.organization, "high", record.assignment_class, record.prefix, record.prefix_length, "longest_prefix_v1")
    return ManufacturerLookupResult(status, None, "unknown", None, None, None, "none")
def lookup_manufacturer_eui48(database: ManufacturerDatabase, mac: str) -> ManufacturerLookupResult:
    if not isinstance(database, ManufacturerDatabase): raise ManufacturerInputError("MANUFACTURER_DATABASE_SCHEMA_INVALID", "database type is invalid")
    try: normalized = normalize_eui48(mac)
    except ManufacturerInputError: return _lookup("invalid_address")
    if is_multicast_address(normalized): return _lookup("multicast_address")
    if is_locally_administered_address(normalized): return _lookup("locally_administered_address")
    raw = normalized.replace(":", "")
    for width, mapping in ((9, database.ma_s), (7, database.ma_m), (6, database.ma_l)):
        if f"{width * 4}:{raw[:width]}" in database.conflicts: return _lookup("conflicting_assignment")
        if raw[:width] in mapping: return _lookup("matched", mapping[raw[:width]])
    return _lookup("unknown_prefix")
def lookup_manufacturer_eui64(database: ManufacturerDatabase, eui64: str) -> ManufacturerLookupResult:
    if not isinstance(database, ManufacturerDatabase): raise ManufacturerInputError("MANUFACTURER_DATABASE_SCHEMA_INVALID", "database type is invalid")
    try: normalized = normalize_eui64(eui64)
    except ManufacturerInputError: return _lookup("invalid_address")
    if is_multicast_address(normalized): return _lookup("multicast_address")
    if is_locally_administered_address(normalized): return _lookup("locally_administered_address")
    return _lookup("unsupported_address_type")

def build_manufacturer_sidecar(inventory_document: dict, database: ManufacturerDatabase, *, generated_at: str) -> tuple[dict, dict]:
    _timestamp(generated_at)
    if not isinstance(inventory_document, dict) or not isinstance(inventory_document.get("devices"), list): raise ManufacturerValidationError("MANUFACTURER_INVENTORY_INVALID", "inventory is invalid")
    records = {}
    for device in inventory_document["devices"]:
        if not isinstance(device, dict) or not isinstance(device.get("id"), str) or not STABLE_RE.fullmatch(device["id"]) or device["id"] in records: raise ManufacturerValidationError("MANUFACTURER_INVENTORY_INVALID", "inventory stable IDs are invalid")
        mac = device.get("mac"); result = _lookup("missing_address") if mac is None or mac == "" else lookup_manufacturer_eui48(database, mac) if isinstance(mac, str) else _lookup("invalid_address")
        records[device["id"]] = {"stable_device_id": device["id"], "lookup_status": result.lookup_status, "manufacturer": result.manufacturer, "confidence": result.confidence, "assignment_class": result.assignment_class, "matched_prefix": result.matched_prefix, "matched_prefix_length": result.matched_prefix_length, "source": "ieee_registration_authority", "dataset_version": database.document["dataset_version"], "dataset_semantic_sha256": database.document["semantic_sha256"], "lookup_method": result.lookup_method}
    records = {key: records[key] for key in sorted(records)}; statuses = [x["lookup_status"] for x in records.values()]
    counts = {"matched_count": statuses.count("matched"), "unknown_count": sum(x in {"conflicting_assignment", "unknown_prefix", "unsupported_address_type"} for x in statuses), "excluded_count": sum(x in {"multicast_address", "locally_administered_address"} for x in statuses), "invalid_count": sum(x in {"missing_address", "invalid_address"} for x in statuses)}
    sidecar = {"schema_version": MANUFACTURER_SIDECAR_SCHEMA_VERSION, "generated_at": generated_at, "dataset_id": database.document["dataset_id"], "dataset_version": database.document["dataset_version"], "dataset_semantic_sha256": database.document["semantic_sha256"], "record_count": len(records), **counts, "records": records}
    status = {"schema_version": MANUFACTURER_STATUS_SCHEMA_VERSION, "updated": generated_at, "status": "online", "dataset_available": True, "dataset_id": database.document["dataset_id"], "dataset_version": database.document["dataset_version"], "dataset_semantic_sha256": database.document["semantic_sha256"], "record_count": len(records), **counts, "conflict_count": database.document["conflict_count"], "generator": MANUFACTURER_GENERATOR_VERSION, "error_code": None, "error_message": None}
    validate_manufacturer_sidecar(sidecar); validate_manufacturer_status(status); return sidecar, status

def _fsync_directory(path):
    if os.name != "posix": return
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try: os.fsync(fd)
    finally: os.close(fd)
def write_json_atomic(path: pathlib.Path, document: object, *, mode: int) -> None:
    path = pathlib.Path(path); temp = None
    if not path.is_absolute() or not path.parent.is_dir() or path.parent.is_symlink(): raise ManufacturerWriteError("MANUFACTURER_SIDECAR_WRITE_FAILED", "write parent is invalid")
    try:
        fd, name = tempfile.mkstemp(prefix=f".manufacturer.{os.getpid()}.", suffix=".tmp", dir=path.parent); temp = pathlib.Path(name)
        with os.fdopen(fd, "wb") as handle: handle.write(canonical_json_bytes(document)); handle.flush(); os.fsync(handle.fileno())
        os.chmod(temp, mode); os.replace(temp, path); temp = None; os.chmod(path, mode); _fsync_directory(path.parent)
    except ManufacturerError: raise
    except Exception as exc: raise ManufacturerWriteError("MANUFACTURER_SIDECAR_WRITE_FAILED", "atomic write failed") from exc
    finally:
        if temp:
            try: temp.unlink()
            except OSError: pass

class _ManufacturerLock:
    _held = set()
    def __init__(self, path=pathlib.Path("/tmp/hioc-manufacturer.lock"), timeout=10.0): self.path, self.timeout, self.handle = pathlib.Path(path), timeout, None
    def __enter__(self):
        key = str(self.path)
        if key in self._held: raise ManufacturerLockError("MANUFACTURER_LOCK_TIMEOUT", "nested manufacturer lock is prohibited")
        try: fd = os.open(self.path, os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0), 0o600); os.chmod(self.path, 0o600); self.handle = os.fdopen(fd, "a+b", buffering=0)
        except OSError as exc: raise ManufacturerLockError("MANUFACTURER_PERMISSION_ERROR", "lock unavailable") from exc
        start = time.monotonic()
        if fcntl:
            while True:
                try: fcntl.flock(self.handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB); break
                except BlockingIOError:
                    if time.monotonic() - start >= self.timeout: self.handle.close(); self.handle = None; raise ManufacturerLockError("MANUFACTURER_LOCK_TIMEOUT", "lock timed out")
                    time.sleep(.1)
        self._held.add(key); return self
    def __exit__(self, exc_type, exc, tb):
        key = str(self.path)
        if self.handle:
            if fcntl: fcntl.flock(self.handle.fileno(), fcntl.LOCK_UN)
            self.handle.close()
        self._held.discard(key); return False
