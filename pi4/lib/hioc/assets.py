"""Private PE-2.1 Asset store, transactions, and validation."""

from __future__ import annotations

import errno
import hashlib
import json
import os
import re
import stat
import tempfile
import time
import unicodedata
from contextlib import AbstractContextManager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

try:  # Production is Linux; the fallback keeps repository tests portable.
    import fcntl
except ImportError:  # pragma: no cover - Windows only
    fcntl = None


SCHEMA_VERSION = "1.0"
GENERATOR = "hioc-assets"
STORE_KEYS = ("schema_version", "updated_at", "asset_count", "assets")
RECORD_KEYS = (
    "stable_device_id", "friendly_name", "physical_location", "purpose",
    "notes", "created_at", "updated_at", "update_source", "revision",
)
STATUS_KEYS = (
    "schema_version", "updated", "status", "asset_count",
    "orphaned_asset_count", "invalid_record_count", "generator",
    "error_code", "error_message",
)
STATUS_VALUES = frozenset({"online", "degraded", "error", "unavailable"})
ERROR_CODES = frozenset({
    "STORE_MISSING", "STORE_INVALID_JSON", "STORE_SCHEMA_INVALID",
    "STORE_UNSUPPORTED_VERSION", "STORE_PERMISSION_ERROR", "LOCK_TIMEOUT",
    "INVALID_STABLE_ID", "INVALID_FIELD", "NOT_FOUND", "REVISION_CONFLICT",
    "INVENTORY_UNAVAILABLE", "INVENTORY_INVALID", "BACKUP_FAILED",
    "BACKUP_INVALID", "WRITE_FAILED", "STATUS_WRITE_FAILED",
    "RESTORE_REJECTED", "RESTORE_INVALID", "PRIVACY_REFUSED",
    "INTERNAL_ERROR",
})
FIELD_LIMITS = {
    "friendly_name": 128, "physical_location": 128, "purpose": 256,
    "notes": 1024,
}
OPERATOR_FIELDS = tuple(FIELD_LIMITS)
STABLE_ID_RE = re.compile(r"^dev_[0-9a-f]{16}$")
TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}Z$")
BACKUP_RE = re.compile(
    r"^assets-(\d{8}T\d{12}Z)-([0-9a-f]{12})\.json$"
)


class AssetError(Exception):
    exit_code = 3

    def __init__(self, code: str, message: str):
        if code not in ERROR_CODES:
            code = "INTERNAL_ERROR"
        self.code = code
        self.safe_message = " ".join(str(message).split())[:160]
        super().__init__(self.safe_message)


class AssetUsageError(AssetError):
    exit_code = 2


class AssetValidationError(AssetError):
    exit_code = 3


class AssetNotFoundError(AssetError):
    exit_code = 4


class AssetRevisionConflict(AssetError):
    exit_code = 5


class AssetLockTimeout(AssetError):
    exit_code = 6


class AssetBackupError(AssetError):
    exit_code = 7


class AssetWriteError(AssetError):
    exit_code = 8


class AssetRestoreError(AssetError):
    exit_code = 9


class AssetPrivacyError(AssetError):
    exit_code = 13


def utc_now(clock: Callable[..., datetime] = datetime.now) -> str:
    try:
        value = clock(timezone.utc)
    except TypeError:
        value = clock()
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def _require_timestamp(value: Any, field: str) -> None:
    if not isinstance(value, str) or not TIMESTAMP_RE.fullmatch(value):
        raise AssetValidationError("STORE_SCHEMA_INVALID", f"{field} must be an RFC 3339 UTC timestamp")
    try:
        datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError as exc:
        raise AssetValidationError("STORE_SCHEMA_INVALID", f"{field} timestamp is invalid") from exc


def validate_stable_id(value: str) -> str:
    if not isinstance(value, str) or not STABLE_ID_RE.fullmatch(value):
        raise AssetValidationError("INVALID_STABLE_ID", "stable device ID is invalid")
    return value


def _is_forbidden_control(char: str, allow_lf: bool = False) -> bool:
    if allow_lf and char == "\n":
        return False
    return unicodedata.category(char).startswith("C") or char in "\r\n\t\v\f\u2028\u2029"


def normalize_field(field: str, value: str | None) -> str | None:
    if field not in FIELD_LIMITS:
        raise AssetValidationError("INVALID_FIELD", "Asset field is invalid")
    if value is None:
        return None
    if not isinstance(value, str):
        raise AssetValidationError("INVALID_FIELD", "Asset field must be text")
    normalized = unicodedata.normalize("NFC", value)
    if field == "notes":
        normalized = normalized.replace("\r\n", "\n").replace("\r", "\n")
        lines = [line.rstrip() for line in normalized.split("\n")]
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
        normalized = "\n".join(lines).strip()
        if any(_is_forbidden_control(ch, allow_lf=True) for ch in normalized):
            raise AssetValidationError("INVALID_FIELD", "notes contain prohibited characters")
        if len(normalized.split("\n")) > 8:
            raise AssetValidationError("INVALID_FIELD", "notes exceed eight lines")
    else:
        normalized = normalized.strip()
        if any(_is_forbidden_control(ch) for ch in normalized):
            raise AssetValidationError("INVALID_FIELD", f"{field} contains prohibited characters")
    if not normalized:
        return None
    if len(normalized) > FIELD_LIMITS[field]:
        raise AssetValidationError("INVALID_FIELD", f"{field} exceeds its maximum length")
    return normalized


def _require_exact_keys(value: dict, keys: tuple[str, ...], subject: str) -> None:
    if tuple(value.keys()) != keys or set(value) != set(keys):
        raise AssetValidationError("STORE_SCHEMA_INVALID", f"{subject} has invalid fields or ordering")


def validate_store(value: object) -> dict:
    if not isinstance(value, dict):
        raise AssetValidationError("STORE_SCHEMA_INVALID", "Asset store must be an object")
    if value.get("schema_version") != SCHEMA_VERSION:
        code = "STORE_UNSUPPORTED_VERSION" if "schema_version" in value else "STORE_SCHEMA_INVALID"
        raise AssetValidationError(code, "Asset store schema version is unsupported")
    _require_exact_keys(value, STORE_KEYS, "Asset store")
    _require_timestamp(value["updated_at"], "updated_at")
    assets = value["assets"]
    if not isinstance(assets, dict) or not isinstance(value["asset_count"], int) or isinstance(value["asset_count"], bool):
        raise AssetValidationError("STORE_SCHEMA_INVALID", "Asset store counts or mapping are invalid")
    if value["asset_count"] != len(assets) or list(assets) != sorted(assets):
        raise AssetValidationError("STORE_SCHEMA_INVALID", "Asset count or ordering is invalid")
    for key, record in assets.items():
        validate_stable_id(key)
        if not isinstance(record, dict):
            raise AssetValidationError("STORE_SCHEMA_INVALID", "Asset record must be an object")
        _require_exact_keys(record, RECORD_KEYS, "Asset record")
        if record["stable_device_id"] != key:
            raise AssetValidationError("STORE_SCHEMA_INVALID", "Asset key and embedded ID differ")
        normalized = {field: normalize_field(field, record[field]) for field in OPERATOR_FIELDS}
        if any(normalized[field] != record[field] for field in OPERATOR_FIELDS):
            raise AssetValidationError("STORE_SCHEMA_INVALID", "Asset fields are not normalized")
        if not any(record[field] is not None for field in OPERATOR_FIELDS):
            raise AssetValidationError("STORE_SCHEMA_INVALID", "Asset record has no populated field")
        _require_timestamp(record["created_at"], "created_at")
        _require_timestamp(record["updated_at"], "updated_at")
        if record["update_source"] != "operator_cli":
            raise AssetValidationError("STORE_SCHEMA_INVALID", "Asset update source is invalid")
        if not isinstance(record["revision"], int) or isinstance(record["revision"], bool) or record["revision"] < 1:
            raise AssetValidationError("STORE_SCHEMA_INVALID", "Asset revision is invalid")
    return value


def validate_status(value: object) -> dict:
    if not isinstance(value, dict):
        raise AssetValidationError("STORE_SCHEMA_INVALID", "Asset status must be an object")
    if value.get("schema_version") != SCHEMA_VERSION:
        raise AssetValidationError("STORE_UNSUPPORTED_VERSION", "Asset status schema version is unsupported")
    _require_exact_keys(value, STATUS_KEYS, "Asset status")
    _require_timestamp(value["updated"], "updated")
    if value["status"] not in STATUS_VALUES or value["generator"] != GENERATOR:
        raise AssetValidationError("STORE_SCHEMA_INVALID", "Asset status enum or generator is invalid")
    for key in ("asset_count", "invalid_record_count"):
        if not isinstance(value[key], int) or isinstance(value[key], bool) or value[key] < 0:
            raise AssetValidationError("STORE_SCHEMA_INVALID", f"{key} is invalid")
    orphan = value["orphaned_asset_count"]
    if orphan is not None and (not isinstance(orphan, int) or isinstance(orphan, bool) or orphan < 0):
        raise AssetValidationError("STORE_SCHEMA_INVALID", "orphan count is invalid")
    error_code = value["error_code"]
    if error_code is not None and error_code not in ERROR_CODES:
        raise AssetValidationError("STORE_SCHEMA_INVALID", "status error code is invalid")
    message = value["error_message"]
    if message is not None and (not isinstance(message, str) or len(message) > 160 or "\n" in message):
        raise AssetValidationError("STORE_SCHEMA_INVALID", "status error message is invalid")
    if value["status"] == "online" and (error_code is not None or message is not None or orphan is None):
        raise AssetValidationError("STORE_SCHEMA_INVALID", "online Asset status is inconsistent")
    return value


def serialize_store(value: dict) -> bytes:
    validate_store(value)
    return (json.dumps(value, ensure_ascii=False, indent=2, separators=(",", ": ")) + "\n").encode("utf-8")


def serialize_status(value: dict) -> bytes:
    validate_status(value)
    return (json.dumps(value, ensure_ascii=False, indent=2, separators=(",", ": ")) + "\n").encode("utf-8")


def redacted_id(value: str) -> str:
    validate_stable_id(value)
    return hashlib.sha256(value.encode("ascii")).hexdigest()[:12]


def calculate_orphans(store: dict, inventory: object) -> set[str]:
    validate_store(store)
    if not isinstance(inventory, dict) or not isinstance(inventory.get("devices"), list):
        raise AssetValidationError("INVENTORY_INVALID", "inventory context is invalid")
    current = set()
    for device in inventory["devices"]:
        if not isinstance(device, dict) or "id" not in device:
            continue
        try:
            current.add(validate_stable_id(device["id"]))
        except AssetValidationError as exc:
            raise AssetValidationError("INVENTORY_INVALID", "inventory contains an invalid stable ID") from exc
    return set(store["assets"]) - current


class AssetLock(AbstractContextManager):
    _held: set[str] = set()

    def __init__(self, path: Path, shared: bool, timeout: float = 5.0):
        self.path, self.shared, self.timeout, self.handle = Path(path), shared, timeout, None

    def __enter__(self):
        key = str(self.path.resolve())
        if key in self._held:
            raise AssetLockTimeout("LOCK_TIMEOUT", "nested Asset lock is prohibited")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        flags = os.O_RDWR | os.O_CREAT
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        fd = os.open(self.path, flags, 0o600)
        os.chmod(self.path, 0o600)
        self.handle = os.fdopen(fd, "a+b", buffering=0)
        start = time.monotonic()
        if fcntl is None:  # pragma: no cover - repository-host portability
            self._held.add(key)
            return self
        operation = (fcntl.LOCK_SH if self.shared else fcntl.LOCK_EX) | fcntl.LOCK_NB
        while True:
            try:
                fcntl.flock(self.handle.fileno(), operation)
                self._held.add(key)
                return self
            except BlockingIOError:
                if time.monotonic() - start >= self.timeout:
                    self.handle.close()
                    self.handle = None
                    raise AssetLockTimeout("LOCK_TIMEOUT", "Asset lock timed out")
                time.sleep(0.05)

    def __exit__(self, exc_type, exc, tb):
        key = str(self.path.resolve())
        if self.handle is not None:
            if fcntl is not None:
                fcntl.flock(self.handle.fileno(), fcntl.LOCK_UN)
            self.handle.close()
        self._held.discard(key)
        return False


class AssetStore:
    def __init__(self, home: Path, clock: Callable[..., datetime] = datetime.now, lock_path: Path | None = None):
        self.home = Path(home)
        self.state_dir = self.home / "state" / "inventory"
        self.store_path = self.state_dir / "assets.json"
        self.status_path = self.state_dir / "assets_status.json"
        self.inventory_path = self.state_dir / "inventory.json"
        self.backup_dir = self.home / "backups" / "assets"
        self.lock_path = Path(lock_path or os.environ.get("HIOC_ASSET_LOCK", "/tmp/hioc-assets.lock"))
        self.clock = clock

    def timestamp(self) -> str:
        return utc_now(self.clock)

    def empty_store(self, timestamp: str | None = None) -> dict:
        return {"schema_version": SCHEMA_VERSION, "updated_at": timestamp or self.timestamp(), "asset_count": 0, "assets": {}}

    @staticmethod
    def _check_regular(path: Path, mode: int = 0o600) -> None:
        info = path.lstat()
        if not stat.S_ISREG(info.st_mode) or stat.S_IMODE(info.st_mode) != mode:
            raise AssetValidationError("STORE_PERMISSION_ERROR", "Asset file permissions are unsafe")
        if hasattr(os, "getuid") and os.getuid() != 0 and info.st_uid != os.getuid():
            raise AssetValidationError("STORE_PERMISSION_ERROR", "Asset file ownership is unsafe")

    def ensure_directories(self) -> None:
        self.state_dir.mkdir(parents=True, exist_ok=True, mode=0o750)
        self.backup_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
        if os.name == "posix":
            os.chmod(self.state_dir, 0o750)
            os.chmod(self.backup_dir, 0o700)

    def load_store(self, missing_ok: bool = False) -> dict | None:
        if not self.store_path.exists():
            if missing_ok:
                return None
            raise AssetValidationError("STORE_MISSING", "Asset store is not initialized")
        if os.name == "posix":
            self._check_regular(self.store_path)
        try:
            payload = json.loads(self.store_path.read_text(encoding="utf-8"), object_pairs_hook=dict)
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise AssetValidationError("STORE_INVALID_JSON", "Asset store is invalid JSON") from exc
        return validate_store(payload)

    def load_status(self) -> dict:
        if not self.status_path.exists():
            raise AssetValidationError("STORE_MISSING", "Asset status is missing")
        if os.name == "posix":
            self._check_regular(self.status_path)
        try:
            payload = json.loads(self.status_path.read_text(encoding="utf-8"), object_pairs_hook=dict)
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise AssetValidationError("STORE_INVALID_JSON", "Asset status is invalid JSON") from exc
        return validate_status(payload)

    def inventory_context(self, store: dict) -> tuple[str, set[str] | None]:
        if not self.inventory_path.exists():
            return "unavailable", None
        try:
            inventory = json.loads(self.inventory_path.read_text(encoding="utf-8"))
            return "available", calculate_orphans(store, inventory)
        except (OSError, UnicodeError, json.JSONDecodeError, AssetError):
            return "invalid", None

    @staticmethod
    def _fsync_directory(path: Path) -> None:
        if os.name != "posix":
            return
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            os.fsync(fd)
        finally:
            os.close(fd)

    def _atomic_write(self, path: Path, content: bytes, validator: Callable[[object], dict], error_code: str) -> None:
        self.ensure_directories()
        temp_path = None
        try:
            fd, name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
            temp_path = Path(name)
            with os.fdopen(fd, "wb") as handle:
                handle.write(content)
                handle.flush()
                os.fsync(handle.fileno())
            os.chmod(temp_path, 0o600)
            validator(json.loads(temp_path.read_text(encoding="utf-8"), object_pairs_hook=dict))
            os.replace(temp_path, path)
            temp_path = None
            if os.name == "posix":
                os.chmod(path, 0o600)
            self._fsync_directory(path.parent)
        except AssetError:
            raise
        except Exception as exc:
            raise AssetWriteError(error_code, "Asset atomic write failed") from exc
        finally:
            if temp_path is not None:
                try:
                    temp_path.unlink()
                except OSError:
                    pass

    def write_store(self, store: dict) -> None:
        self._atomic_write(self.store_path, serialize_store(store), validate_store, "WRITE_FAILED")

    def write_status(self, status: dict) -> None:
        self._atomic_write(self.status_path, serialize_status(status), validate_status, "STATUS_WRITE_FAILED")

    def make_status(self, store: dict | None, context: str, orphans: set[str] | None,
                    error_code: str | None = None, message: str | None = None,
                    invalid_count: int = 0) -> dict:
        if store is None:
            status = "unavailable"
        elif error_code and error_code not in {"INVENTORY_UNAVAILABLE", "INVENTORY_INVALID"}:
            status = "error"
        elif context != "available":
            status = "degraded"
            error_code = "INVENTORY_UNAVAILABLE" if context == "unavailable" else "INVENTORY_INVALID"
            message = "inventory context is unavailable" if context == "unavailable" else "inventory context is invalid"
        else:
            status, error_code, message = "online", None, None
        return {
            "schema_version": SCHEMA_VERSION, "updated": self.timestamp(), "status": status,
            "asset_count": len(store["assets"]) if store else 0,
            "orphaned_asset_count": len(orphans) if orphans is not None else None,
            "invalid_record_count": invalid_count, "generator": GENERATOR,
            "error_code": error_code, "error_message": (" ".join(message.split())[:160] if message else None),
        }

    def create_backup(self, store: dict, exact_bytes: bytes | None = None) -> str:
        self.ensure_directories()
        content = exact_bytes if exact_bytes is not None else serialize_store(store)
        try:
            validate_store(json.loads(content.decode("utf-8"), object_pairs_hook=dict))
            digest = hashlib.sha256(content).hexdigest()
            stamp = self.timestamp().replace("-", "").replace(":", "").replace(".", "")
            basename = f"assets-{stamp}-{digest[:12]}.json"
            path = self.backup_dir / basename
            if path.exists():
                if path.read_bytes() != content:
                    raise AssetBackupError("BACKUP_FAILED", "Asset backup collision")
                return basename
            self._atomic_write(path, content, validate_store, "BACKUP_FAILED")
            if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                raise AssetBackupError("BACKUP_INVALID", "Asset backup validation failed")
            return basename
        except AssetBackupError:
            raise
        except AssetError as exc:
            raise AssetBackupError("BACKUP_FAILED", "Asset backup failed") from exc
        except Exception as exc:
            raise AssetBackupError("BACKUP_FAILED", "Asset backup failed") from exc

    def load_backup(self, basename: str) -> tuple[dict, bytes]:
        if not isinstance(basename, str) or Path(basename).name != basename or not BACKUP_RE.fullmatch(basename):
            raise AssetRestoreError("RESTORE_REJECTED", "Asset backup basename is rejected")
        path = self.backup_dir / basename
        try:
            if path.is_symlink() or not path.exists() or not path.is_file():
                raise AssetRestoreError("RESTORE_REJECTED", "Asset backup is not a regular file")
            if path.resolve().parent != self.backup_dir.resolve():
                raise AssetRestoreError("RESTORE_REJECTED", "Asset backup is outside the backup root")
            if os.name == "posix":
                self._check_regular(path)
            content = path.read_bytes()
            expected = BACKUP_RE.fullmatch(basename).group(2)
            if hashlib.sha256(content).hexdigest()[:12] != expected:
                raise AssetRestoreError("RESTORE_INVALID", "Asset backup digest is invalid")
            value = json.loads(content.decode("utf-8"), object_pairs_hook=dict)
            return validate_store(value), content
        except AssetRestoreError:
            raise
        except Exception as exc:
            raise AssetRestoreError("RESTORE_INVALID", "Asset backup is invalid") from exc


class AssetService:
    def __init__(self, store: AssetStore):
        self.store = store

    @staticmethod
    def _result(command: str, result: str, status: str, data: dict) -> dict:
        return {"schema_version": SCHEMA_VERSION, "command": command, "result": result,
                "status": status, "redacted": True, "data": data, "error": None}

    def _write_status(self, store: dict) -> dict:
        context, orphans = self.store.inventory_context(store)
        status = self.store.make_status(store, context, orphans)
        self.store.write_status(status)
        return status

    def initialize(self) -> dict:
        with AssetLock(self.store.lock_path, shared=False):
            current = self.store.load_store(missing_ok=True)
            if current is not None:
                status = self._write_status(current)
                return self._result("initialize", "already_initialized", status["status"], {"asset_count": len(current["assets"]), "initialized": True})
            empty = self.store.empty_store()
            self.store.create_backup(empty)
            self.store.write_store(empty)
            status = self._write_status(empty)
            return self._result("initialize", "initialized", status["status"], {"asset_count": 0, "initialized": True})

    def list_assets(self) -> dict:
        with AssetLock(self.store.lock_path, shared=True):
            current = self.store.load_store(missing_ok=True)
            if current is None:
                return self._result("list", "listed", "unavailable", {"asset_count": 0, "orphaned_asset_count": None, "inventory_context": "unavailable", "assets": []})
            context, orphans = self.store.inventory_context(current)
            items = []
            for key, record in current["assets"].items():
                items.append({"device_id_digest": redacted_id(key), "revision": record["revision"],
                              "populated_fields": [f for f in OPERATOR_FIELDS if record[f] is not None],
                              "orphaned": (key in orphans if orphans is not None else None),
                              "created_at": record["created_at"], "updated_at": record["updated_at"]})
            return self._result("list", "listed", "online" if context == "available" else "degraded",
                                {"asset_count": len(items), "orphaned_asset_count": len(orphans) if orphans is not None else None,
                                 "inventory_context": context, "assets": items})

    def show_asset(self, device_id: str, include_values: bool = False) -> dict:
        validate_stable_id(device_id)
        with AssetLock(self.store.lock_path, shared=True):
            current = self.store.load_store()
            record = current["assets"].get(device_id)
            if record is None:
                raise AssetNotFoundError("NOT_FOUND", "Asset record was not found")
            context, orphans = self.store.inventory_context(current)
            data = {"device_id_digest": redacted_id(device_id), "revision": record["revision"],
                    "populated_fields": [f for f in OPERATOR_FIELDS if record[f] is not None],
                    "orphaned": (device_id in orphans if orphans is not None else None),
                    "created_at": record["created_at"], "updated_at": record["updated_at"]}
            if include_values:
                data["values"] = {f: record[f] for f in OPERATOR_FIELDS}
            return self._result("show", "shown", "online" if context == "available" else "degraded", data)

    def set_fields(self, device_id: str, fields: dict[str, str | None], allow_orphan: bool = False,
                   expected_revision: int | None = None) -> dict:
        validate_stable_id(device_id)
        if not fields:
            raise AssetUsageError("INVALID_FIELD", "at least one Asset field is required")
        normalized = {key: normalize_field(key, value) for key, value in fields.items()}
        with AssetLock(self.store.lock_path, shared=False):
            current = self.store.load_store(missing_ok=True)
            if current is None:
                current = self.store.empty_store()
            record = current["assets"].get(device_id)
            context, orphans = self.store.inventory_context(current)
            if record is None:
                if expected_revision is not None:
                    raise AssetRevisionConflict("REVISION_CONFLICT", "revision supplied for Asset creation")
                inventory_proves_id = context == "available" and orphans is not None
                if inventory_proves_id:
                    try:
                        inventory = json.loads(self.store.inventory_path.read_text(encoding="utf-8"))
                        ids = {d.get("id") for d in inventory.get("devices", []) if isinstance(d, dict)}
                        inventory_proves_id = device_id in ids
                    except Exception:
                        inventory_proves_id = False
                if not inventory_proves_id and not allow_orphan:
                    raise AssetValidationError("INVENTORY_UNAVAILABLE", "Asset creation requires inventory proof or allow-orphan")
                now = self.store.timestamp()
                values = {field: None for field in OPERATOR_FIELDS}
                values.update(normalized)
                if not any(value is not None for value in values.values()):
                    raise AssetValidationError("INVALID_FIELD", "new Asset requires a populated field")
                new_record = {"stable_device_id": device_id, **values, "created_at": now,
                              "updated_at": now, "update_source": "operator_cli", "revision": 1}
                result, revision = "created", 1
            else:
                if expected_revision is None or expected_revision != record["revision"]:
                    raise AssetRevisionConflict("REVISION_CONFLICT", "Asset revision conflict")
                if all(record[field] == value for field, value in normalized.items()):
                    status = self._write_status(current)
                    return self._result("set", "no_change", status["status"],
                                        {"device_id_digest": redacted_id(device_id), "revision": record["revision"],
                                         "changed_fields": [], "backup": None})
                new_record = dict(record)
                new_record.update(normalized)
                if not any(new_record[field] is not None for field in OPERATOR_FIELDS):
                    return self._remove_locked(current, device_id, record, "set", list(normalized))
                new_record["updated_at"] = self.store.timestamp()
                new_record["revision"] += 1
                result, revision = "updated", new_record["revision"]
            changed = [f for f in OPERATOR_FIELDS if (record or {}).get(f) != new_record[f]]
            updated = dict(current)
            assets = dict(current["assets"])
            assets[device_id] = new_record
            updated["assets"] = {key: assets[key] for key in sorted(assets)}
            updated["asset_count"] = len(assets)
            updated["updated_at"] = new_record["updated_at"]
            validate_store(updated)
            prior_bytes = self.store.store_path.read_bytes() if self.store.store_path.exists() else serialize_store(current)
            backup = self.store.create_backup(current, prior_bytes)
            self.store.write_store(updated)
            status = self._write_status(updated)
            return self._result("set", result, status["status"], {"device_id_digest": redacted_id(device_id),
                                "revision": revision, "changed_fields": changed, "backup": backup})

    def _remove_locked(self, current: dict, device_id: str, record: dict, command: str, changed: list[str]) -> dict:
        prior = self.store.store_path.read_bytes()
        backup = self.store.create_backup(current, prior)
        assets = dict(current["assets"])
        del assets[device_id]
        updated = {"schema_version": SCHEMA_VERSION, "updated_at": self.store.timestamp(),
                   "asset_count": len(assets), "assets": {k: assets[k] for k in sorted(assets)}}
        self.store.write_store(updated)
        status = self._write_status(updated)
        return self._result(command, "removed", status["status"], {"device_id_digest": redacted_id(device_id),
                            "revision": None, "changed_fields": changed, "backup": backup})

    def clear_field(self, device_id: str, field: str, expected_revision: int) -> dict:
        validate_stable_id(device_id)
        if field not in OPERATOR_FIELDS:
            raise AssetValidationError("INVALID_FIELD", "Asset field is invalid")
        with AssetLock(self.store.lock_path, shared=False):
            current = self.store.load_store()
            record = current["assets"].get(device_id)
            if record is None:
                raise AssetNotFoundError("NOT_FOUND", "Asset record was not found")
            if record["revision"] != expected_revision:
                raise AssetRevisionConflict("REVISION_CONFLICT", "Asset revision conflict")
            if record[field] is None:
                status = self._write_status(current)
                return self._result("clear-field", "no_change", status["status"], {"device_id_digest": redacted_id(device_id), "revision": record["revision"], "changed_fields": [], "backup": None})
            if sum(record[f] is not None for f in OPERATOR_FIELDS) == 1:
                return self._remove_locked(current, device_id, record, "clear-field", [field])
            replacement = dict(record)
            replacement[field] = None
            replacement["updated_at"] = self.store.timestamp()
            replacement["revision"] += 1
            backup = self.store.create_backup(current, self.store.store_path.read_bytes())
            updated = dict(current); assets = dict(current["assets"]); assets[device_id] = replacement
            updated.update({"updated_at": replacement["updated_at"], "assets": assets})
            self.store.write_store(updated); status = self._write_status(updated)
            return self._result("clear-field", "updated", status["status"], {"device_id_digest": redacted_id(device_id), "revision": replacement["revision"], "changed_fields": [field], "backup": backup})

    def remove(self, device_id: str, expected_revision: int) -> dict:
        validate_stable_id(device_id)
        with AssetLock(self.store.lock_path, shared=False):
            current = self.store.load_store(); record = current["assets"].get(device_id)
            if record is None:
                raise AssetNotFoundError("NOT_FOUND", "Asset record was not found")
            if record["revision"] != expected_revision:
                raise AssetRevisionConflict("REVISION_CONFLICT", "Asset revision conflict")
            return self._remove_locked(current, device_id, record, "remove", list(OPERATOR_FIELDS))

    def validate(self, refresh_status: bool = True) -> dict:
        with AssetLock(self.store.lock_path, shared=True):
            current = self.store.load_store(missing_ok=True)
            if current is None:
                if refresh_status:
                    pass
                else:
                    raise AssetValidationError("STORE_MISSING", "Asset store is not initialized")
            context, orphans = self.store.inventory_context(current) if current else ("unavailable", None)
        if refresh_status:
            with AssetLock(self.store.lock_path, shared=False):
                status = self.store.make_status(current, context, orphans)
                self.store.write_status(status)
        else:
            status = self.store.load_status()
            if current is not None and status["asset_count"] != len(current["assets"]):
                raise AssetValidationError("STORE_SCHEMA_INVALID", "Asset status count differs from store")
        if current is None:
            raise AssetValidationError("STORE_MISSING", "Asset store is not initialized")
        return self._result("validate", "valid", status["status"], {"asset_count": len(current["assets"]),
                            "orphaned_asset_count": len(orphans) if orphans is not None else None,
                            "inventory_context": context,
                            "invariants": {"store_schema": True, "status_schema": True,
                                           "stable_ids": True, "counts": True, "privacy": True}})

    def backup(self) -> dict:
        with AssetLock(self.store.lock_path, shared=False):
            current = self.store.load_store()
            basename = self.store.create_backup(current, self.store.store_path.read_bytes())
            status = self._write_status(current)
            return self._result("backup", "backed_up", status["status"], {"asset_count": len(current["assets"]), "backup": basename})

    def restore(self, basename: str) -> dict:
        candidate, _ = self.store.load_backup(basename)
        with AssetLock(self.store.lock_path, shared=False):
            current = self.store.load_store()
            pre = self.store.create_backup(current, self.store.store_path.read_bytes())
            restored = dict(candidate); restored["updated_at"] = self.store.timestamp()
            self.store.write_store(restored)
            status = self._write_status(restored)
            return self._result("restore", "restored", status["status"], {"asset_count": len(restored["assets"]), "backup": basename, "pre_restore_backup": pre})


def error_envelope(command: str, error: AssetError) -> dict:
    return {"schema_version": SCHEMA_VERSION, "command": command, "result": "error",
            "status": "error", "redacted": True, "data": {},
            "error": {"code": error.code, "message": error.safe_message}}
