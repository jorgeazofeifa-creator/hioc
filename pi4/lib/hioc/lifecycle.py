import hashlib
import json
import os
import re
import shutil
import time
import uuid
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

from .core.monitoring import is_operationally_monitored
from .core.state import StateIOError, StateMalformedError, StateMissingError, StateStore, fsync_directory


SCHEMA_VERSION = "1.0"
MIGRATION_VERSION = 1
ACTIVE = "active"
ARCHIVED = "archived"
SUPPORTED_STATES = {ACTIVE, ARCHIVED}
MAC_RE = re.compile(r"^(?:[0-9a-f]{2}:){5}[0-9a-f]{2}$")


class LifecycleError(RuntimeError):
    pass


class LifecycleValidationError(LifecycleError):
    pass


class LifecycleProtectedError(LifecycleError):
    pass


def _now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _digest(payload: dict) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _generation_id() -> str:
    return f"gen_{int(time.time() * 1000)}_{uuid.uuid4().hex[:12]}"


def _mac_device_id(mac: str) -> str:
    normalized = str(mac or "").strip().lower().replace("-", ":")
    if not MAC_RE.match(normalized):
        return ""
    return "dev_" + hashlib.sha1(normalized.encode()).hexdigest()[:16]


def _validate_header(document: dict, name: str, generation_id: str | None = None) -> None:
    if not isinstance(document, dict):
        raise LifecycleValidationError(f"{name} must be an object")
    version = document.get("schema_version")
    if not isinstance(version, str) or version != SCHEMA_VERSION:
        raise LifecycleValidationError(f"{name}.schema_version unsupported or malformed: {version!r}")
    migration = document.get("migration_version")
    if not isinstance(migration, int) or isinstance(migration, bool) or migration != MIGRATION_VERSION:
        raise LifecycleValidationError(f"{name}.migration_version unsupported or malformed: {migration!r}")
    current_generation = document.get("generation_id")
    if not isinstance(current_generation, str) or not current_generation:
        raise LifecycleValidationError(f"{name}.generation_id is required")
    if generation_id is not None and current_generation != generation_id:
        raise LifecycleValidationError(f"{name}.generation_id does not match CURRENT")


def _device_ids(devices: list[dict], name: str) -> set[str]:
    ids = []
    for device in devices:
        device_id = device.get("id") if isinstance(device, dict) else None
        if not isinstance(device_id, str) or not device_id:
            raise LifecycleValidationError(f"{name} contains a device without a stable id")
        ids.append(device_id)
    if len(ids) != len(set(ids)):
        raise LifecycleValidationError(f"{name} contains duplicate stable ids")
    return set(ids)


def validate_catalog(catalog: dict, generation_id: str | None = None) -> None:
    _validate_header(catalog, "catalog", generation_id)
    for field, expected in (("devices", list), ("services", list), ("topology", dict), ("dependencies", dict)):
        if not isinstance(catalog.get(field), expected):
            raise LifecycleValidationError(f"catalog.{field} must be {expected.__name__}")
    _device_ids(catalog["devices"], "catalog.devices")


def validate_lifecycle(lifecycle: dict, catalog: dict, generation_id: str | None = None) -> None:
    _validate_header(lifecycle, "lifecycle", generation_id)
    records = lifecycle.get("records")
    if not isinstance(records, dict):
        raise LifecycleValidationError("lifecycle.records must be an object")
    catalog_ids = _device_ids(catalog["devices"], "catalog.devices")
    if set(records) != catalog_ids:
        raise LifecycleValidationError("lifecycle ids must exactly match catalog device ids")
    for device_id, record in records.items():
        if not isinstance(record, dict) or record.get("device_id") != device_id:
            raise LifecycleValidationError(f"invalid lifecycle record for {device_id}")
        if record.get("state") not in SUPPORTED_STATES:
            raise LifecycleValidationError(f"unsupported lifecycle state for {device_id}")


def lifecycle_diff(previous: dict, staged: dict) -> list[tuple[str, str | None, str]]:
    old = previous.get("records", {}) if previous else {}
    new = staged.get("records", {})
    changes = []
    for device_id in sorted(set(old) | set(new)):
        previous_state = old.get(device_id, {}).get("state")
        new_state = new.get(device_id, {}).get("state")
        if previous_state != new_state:
            if new_state not in SUPPORTED_STATES:
                raise LifecycleValidationError(f"invalid lifecycle transition for {device_id}")
            changes.append((device_id, previous_state, new_state))
    return changes


def validate_receipt_bijection(previous: dict, staged: dict, manifest: dict, catalog: dict) -> None:
    changes = lifecycle_diff(previous, staged)
    receipts = manifest.get("transition_receipts")
    if not isinstance(receipts, list):
        raise LifecycleValidationError("manifest.transition_receipts must be a list")
    actual = []
    seen = set()
    catalog_ids = _device_ids(catalog["devices"], "catalog.devices")
    for receipt in receipts:
        if not isinstance(receipt, dict):
            raise LifecycleValidationError("transition receipt must be an object")
        device_id = receipt.get("device_id")
        if device_id in seen:
            raise LifecycleValidationError(f"duplicate transition receipt for {device_id}")
        seen.add(device_id)
        if device_id not in catalog_ids:
            raise LifecycleValidationError(f"transition receipt references unknown device {device_id}")
        if receipt.get("transaction_id") != manifest.get("transaction_id") or receipt.get("generation_id") != manifest.get("generation_id"):
            raise LifecycleValidationError("receipt transaction or generation mismatch")
        actual.append((device_id, receipt.get("previous_state"), receipt.get("new_state")))
    if sorted(actual, key=lambda item: item[0]) != changes:
        raise LifecycleValidationError("lifecycle changes and transition receipts are not bijective")


def validate_committed_receipts(lifecycle: dict, manifest: dict, catalog: dict) -> None:
    receipts = manifest.get("transition_receipts")
    if not isinstance(receipts, list):
        raise LifecycleValidationError("manifest.transition_receipts must be a list")
    catalog_ids = _device_ids(catalog["devices"], "catalog.devices")
    seen = set()
    operation = manifest.get("operation_receipt")
    if not isinstance(operation, dict):
        raise LifecycleValidationError("manifest.operation_receipt must be an object")
    for field in ("transaction_id", "operation", "actor", "reason", "timestamp", "transition_hash"):
        if not isinstance(operation.get(field), str) or not operation[field]:
            raise LifecycleValidationError(f"operation receipt {field} is required")
    if operation["transaction_id"] != manifest.get("transaction_id"):
        raise LifecycleValidationError("operation receipt transaction mismatch")
    for receipt in receipts:
        device_id = receipt.get("device_id") if isinstance(receipt, dict) else None
        if device_id in seen or device_id not in catalog_ids:
            raise LifecycleValidationError("committed transition receipt is duplicate or unknown")
        seen.add(device_id)
        if receipt.get("transaction_id") != manifest.get("transaction_id") or receipt.get("generation_id") != manifest.get("generation_id"):
            raise LifecycleValidationError("committed receipt transaction or generation mismatch")
        if lifecycle["records"][device_id]["state"] != receipt.get("new_state"):
            raise LifecycleValidationError("committed receipt does not match lifecycle state")
    operation_without_hash = {key: value for key, value in operation.items() if key != "transition_hash"}
    if operation["transition_hash"] != _digest({"operation": operation_without_hash, "transitions": receipts}):
        raise LifecycleValidationError("operation transition hash mismatch")


def _projection(catalog: dict, lifecycle: dict, state: str, base_summary: dict | None = None) -> dict:
    ids = {device_id for device_id, record in lifecycle["records"].items() if record["state"] == state}
    devices = [dict(device) for device in catalog["devices"] if device["id"] in ids]
    services = [dict(service) for service in catalog["services"] if service.get("device_id") in ids]
    topology = {"root_id": catalog["topology"].get("root_id", ""), "edges": [
        dict(edge) for edge in catalog["topology"].get("edges", [])
        if edge.get("parent_id") in ids and edge.get("child_id") in ids
    ]}
    service_ids = {service.get("id") for service in services}
    allowed = ids | service_ids
    dependencies = {"edges": [
        dict(edge) for edge in catalog["dependencies"].get("edges", [])
        if edge.get("from_id") in allowed and edge.get("to_id") in allowed
    ]}
    summary = dict(base_summary or {})
    summary.update({
        "updated": catalog.get("updated", _now()),
        "device_count": len(devices),
        "infrastructure_count": sum(device.get("inventory_class") == "infrastructure" for device in devices),
        "client_count": sum(device.get("inventory_class") == "client" for device in devices),
        "network_client_count": sum(device.get("inventory_class") == "client" for device in devices),
        "healthy_count": sum(device.get("health_status") == "healthy" for device in devices),
        "watch_count": sum(device.get("health_status") == "watch" for device in devices),
        "degraded_count": sum(device.get("health_status") == "degraded" for device in devices),
        "offline_count": sum(device.get("health_status") == "offline" for device in devices),
        "service_count": len(services),
        "topology_edges": len(topology["edges"]),
        "dependency_edges": len(dependencies["edges"]),
        "lowest_health_score": min((device.get("health_score", 0) for device in devices), default=0),
        "infrastructure_devices": [{
            "name": device.get("display_name", device.get("id", "")),
            "ip": device.get("ip", ""),
            "mac": device.get("mac", ""),
            "vendor": device.get("vendor", ""),
            "role": device.get("role", "Unknown"),
            "status": device.get("status", device.get("health_status", "")),
            "health": device.get("health_status", ""),
            "health_score": device.get("health_score", 0),
            "last_seen": device.get("last_seen", ""),
            "source": device.get("source", ""),
        } for device in devices if device.get("inventory_class") == "infrastructure"],
        "services": [{
            "name": service.get("name", ""), "host": service.get("host", ""),
            "type": service.get("type", ""), "status": service.get("status", ""),
            "dependency": service.get("dependency", ""),
        } for service in services],
    })
    return {
        "schema_version": catalog.get("inventory_schema_version", "1.0"),
        "updated": catalog.get("updated", _now()),
        "devices": devices,
        "services": services,
        "topology": topology,
        "dependencies": dependencies,
        "summary": summary,
    }


def _protected(device: dict) -> bool:
    sources = {item.strip() for item in str(device.get("source", "")).split(",") if item.strip()}
    sources.update(str(item).strip() for item in device.get("sources", []) if str(item).strip())
    roles = {str(item).strip().lower() for item in device.get("roles", [])}
    return bool(
        device.get("inventory_class") == "infrastructure"
        or device.get("type") in {"collector", "gateway", "local_host"}
        or roles & {"collector", "gateway"}
        or "known_infrastructure" in sources
        or is_operationally_monitored(device)
    )


class LifecycleStore:
    def __init__(self, state_dir: Path, lock_timeout: float = 10.0):
        self.state_dir = Path(state_dir)
        self.generations_dir = self.state_dir / "generations"
        self.transactions_dir = self.state_dir / ".transactions"
        self.events_dir = self.state_dir / "events"
        self.receipts_dir = self.events_dir / "receipts"
        self.lock_path = self.state_dir / ".lifecycle.lock"
        self.lock_timeout = lock_timeout

    @contextmanager
    def lock(self):
        self.state_dir.mkdir(parents=True, exist_ok=True)
        handle = self.lock_path.open("a+")
        started = time.monotonic()
        acquired = False
        try:
            while True:
                try:
                    if os.name == "nt":
                        import msvcrt
                        handle.seek(0)
                        msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
                    else:
                        import fcntl
                        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    acquired = True
                    break
                except (BlockingIOError, OSError):
                    if time.monotonic() - started >= self.lock_timeout:
                        raise LifecycleError("inventory lifecycle lock is busy")
                    time.sleep(0.05)
            yield
        finally:
            try:
                if acquired and os.name == "nt":
                    import msvcrt
                    handle.seek(0)
                    msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
                elif acquired:
                    import fcntl
                    fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
            finally:
                handle.close()

    def _strict(self, path: Path):
        try:
            text = path.read_text(encoding="utf-8")
        except FileNotFoundError as exc:
            raise StateMissingError(path) from exc
        except OSError as exc:
            raise StateIOError(path, exc) from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise StateMalformedError(path, exc) from exc

    def current_generation_id(self) -> str:
        try:
            value = self.state_dir.joinpath("CURRENT").read_text(encoding="utf-8").strip()
        except FileNotFoundError as exc:
            raise StateMissingError(self.state_dir / "CURRENT") from exc
        except OSError as exc:
            raise StateIOError(self.state_dir / "CURRENT", exc) from exc
        if not value or Path(value).name != value:
            raise LifecycleValidationError("CURRENT contains an invalid generation id")
        return value

    def load_generation(self, generation_id: str | None = None) -> dict:
        generation_id = generation_id or self.current_generation_id()
        root = self.generations_dir / generation_id
        manifest = self._strict(root / "manifest.json")
        catalog = self._strict(root / "catalog.json")
        lifecycle = self._strict(root / "lifecycle.json")
        _validate_header(manifest, "manifest", generation_id)
        validate_catalog(catalog, generation_id)
        validate_lifecycle(lifecycle, catalog, generation_id)
        if manifest.get("catalog_sha256") != _digest(catalog) or manifest.get("lifecycle_sha256") != _digest(lifecycle):
            raise LifecycleValidationError("authoritative checksum mismatch")
        validate_committed_receipts(lifecycle, manifest, catalog)
        expected_inventory = _projection(catalog, lifecycle, ACTIVE, catalog.get("summary_template", {}))
        expected_archived = _projection(catalog, lifecycle, ARCHIVED, {})
        projection_issues = []
        try:
            inventory = self._strict(root / "inventory.json")
        except (StateMissingError, StateMalformedError, StateIOError):
            inventory = None
        try:
            archived = self._strict(root / "archived.json")
        except (StateMissingError, StateMalformedError, StateIOError):
            archived = None
        if inventory != expected_inventory:
            projection_issues.append("inventory.json")
        if archived != expected_archived:
            projection_issues.append("archived.json")
        return {
            "id": generation_id, "root": root, "manifest": manifest, "catalog": catalog,
            "lifecycle": lifecycle, "inventory": expected_inventory, "archived": expected_archived,
            "projection_issues": projection_issues,
        }

    def open_existing_read_only(self) -> dict:
        """Open and validate current authoritative state without persistent writes."""
        generation = self.load_generation()
        self.validate_generation_chain(generation["id"])
        return generation

    def validate_generation_chain(self, generation_id: str | None = None) -> dict[str, dict]:
        """Validate one ancestry chain, including cross-generation receipt bijection."""
        generation_id = generation_id or self.current_generation_id()
        loaded: dict[str, dict] = {}
        order = []
        seen = set()
        cursor = generation_id
        while cursor is not None:
            if cursor in seen:
                raise LifecycleValidationError(f"previous-generation cycle detected at {cursor}")
            seen.add(cursor)
            try:
                generation = self.load_generation(cursor)
            except StateMissingError as exc:
                raise LifecycleValidationError(f"missing previous generation: {cursor}") from exc
            loaded[cursor] = generation
            order.append(cursor)
            manifest = generation["manifest"]
            previous_id = manifest.get("previous_generation_id")
            operation_previous = manifest["operation_receipt"].get("previous_generation_id")
            if previous_id != operation_previous:
                raise LifecycleValidationError(f"operation receipt previous generation mismatch for {cursor}")
            if previous_id is not None and (not isinstance(previous_id, str) or not previous_id):
                raise LifecycleValidationError(f"invalid previous generation id for {cursor}")
            cursor = previous_id
        for current_id in order:
            current = loaded[current_id]
            previous_id = current["manifest"].get("previous_generation_id")
            previous_lifecycle = loaded[previous_id]["lifecycle"] if previous_id else {"records": {}}
            validate_receipt_bijection(previous_lifecycle, current["lifecycle"], current["manifest"], current["catalog"])
        return loaded

    def validate_all_generation_chains(self) -> dict[str, dict]:
        if not self.generations_dir.exists():
            raise LifecycleValidationError("generation directory is missing")
        loaded = {
            path.name: self.load_generation(path.name)
            for path in sorted(self.generations_dir.iterdir()) if path.is_dir()
        }
        if not loaded:
            raise LifecycleValidationError("no committed generations exist")
        for generation_id, generation in loaded.items():
            manifest = generation["manifest"]
            previous_id = manifest.get("previous_generation_id")
            if previous_id != manifest["operation_receipt"].get("previous_generation_id"):
                raise LifecycleValidationError(f"operation receipt previous generation mismatch for {generation_id}")
            if previous_id is not None and previous_id not in loaded:
                raise LifecycleValidationError(f"missing previous generation: {previous_id}")
            previous_lifecycle = loaded[previous_id]["lifecycle"] if previous_id else {"records": {}}
            validate_receipt_bijection(previous_lifecycle, generation["lifecycle"], manifest, generation["catalog"])
        validated = set()
        for generation_id in loaded:
            path = set()
            cursor = generation_id
            while cursor is not None and cursor not in validated:
                if cursor in path:
                    raise LifecycleValidationError(f"previous-generation cycle detected at {cursor}")
                path.add(cursor)
                cursor = loaded[cursor]["manifest"].get("previous_generation_id")
            validated.update(path)
        return loaded

    def _legacy_inventory(self) -> dict:
        inventory = self._strict(self.state_dir / "inventory.json")
        required = {"schema_version", "updated", "devices", "services", "topology", "dependencies", "summary"}
        if not isinstance(inventory, dict) or not required <= set(inventory):
            raise LifecycleValidationError("legacy inventory schema is invalid")
        _device_ids(inventory["devices"], "legacy inventory")
        return inventory

    def _backup_legacy(self) -> Path:
        backup_root = self.state_dir.parent / "backups"
        backup_root.mkdir(parents=True, exist_ok=True)
        target = backup_root / f"inventory-pre-lifecycle-{int(time.time())}"
        shutil.copytree(self.state_dir, target, ignore=shutil.ignore_patterns(".lifecycle.lock"))
        return target

    def _quarantine_stale_transactions(self) -> None:
        if self.transactions_dir.exists():
            quarantine = self.transactions_dir / "quarantine"
            for path in list(self.transactions_dir.iterdir()):
                if path.name == "quarantine":
                    continue
                quarantine.mkdir(parents=True, exist_ok=True)
                os.replace(path, quarantine / f"{path.name}.{int(time.time())}.stale")
        pointer_tmp = self.state_dir / "CURRENT.tmp"
        if pointer_tmp.exists():
            quarantine = self.transactions_dir / "quarantine"
            quarantine.mkdir(parents=True, exist_ok=True)
            os.replace(pointer_tmp, quarantine / f"CURRENT.tmp.{int(time.time())}.stale")

    def initialize_or_migrate(self) -> dict:
        self._quarantine_stale_transactions()
        current = self.state_dir / "CURRENT"
        if current.exists():
            generation = self.load_generation()
            self.materialize_current_if_needed(generation)
            return generation
        partial = [self.generations_dir, self.events_dir]
        if any(path.exists() and any(path.iterdir()) for path in partial):
            raise LifecycleValidationError("partial lifecycle state exists without CURRENT")
        if any((self.state_dir / name).exists() for name in ("catalog.json", "lifecycle.json", "archived.json")):
            raise LifecycleValidationError("partial lifecycle files exist without CURRENT")
        legacy_path = self.state_dir / "inventory.json"
        if not legacy_path.exists():
            other = [path for path in self.state_dir.glob("*.json") if path.name != "status.json"]
            if other:
                raise LifecycleValidationError("legacy inventory is missing while related state exists")
            legacy = {"schema_version": "1.0", "updated": _now(), "devices": [], "services": [], "topology": {"root_id": "", "edges": []}, "dependencies": {"edges": []}, "summary": {}}
        else:
            legacy = self._legacy_inventory()
            self._backup_legacy()
        records = {device["id"]: {"device_id": device["id"], "state": ACTIVE, "changed_at": legacy.get("updated", _now()), "changed_by": "migration"} for device in legacy["devices"]}
        return self.commit(legacy, records, "migration", "system", "initialize Phase 7A.8 lifecycle authority", previous=None)

    # Compatibility for internal callers; CLI read-only paths must not use this.
    def ensure_initialized(self) -> dict:
        return self.initialize_or_migrate()

    def _build_catalog(self, inventory: dict, archived_devices: list[dict] | None, generation_id: str) -> dict:
        devices = {device["id"]: dict(device) for device in archived_devices or []}
        devices.update({device["id"]: dict(device) for device in inventory["devices"]})
        return {
            "schema_version": SCHEMA_VERSION,
            "migration_version": MIGRATION_VERSION,
            "generation_id": generation_id,
            "inventory_schema_version": inventory.get("schema_version", "1.0"),
            "updated": inventory.get("updated", _now()),
            "devices": sorted(devices.values(), key=lambda item: item["id"]),
            "services": [dict(item) for item in inventory.get("services", [])],
            "topology": dict(inventory.get("topology", {"root_id": "", "edges": []})),
            "dependencies": dict(inventory.get("dependencies", {"edges": []})),
            "summary_template": dict(inventory.get("summary", {})),
        }

    @staticmethod
    def _authoritative_content(catalog: dict) -> dict:
        """Content that warrants a generation; excludes derived summary/run time."""
        return {
            "inventory_schema_version": catalog.get("inventory_schema_version", "1.0"),
            "devices": catalog.get("devices", []),
            "services": catalog.get("services", []),
            "topology": catalog.get("topology", {}),
            "dependencies": catalog.get("dependencies", {}),
        }

    def _is_noop(self, previous: dict | None, catalog: dict, records: dict) -> bool:
        return bool(
            previous
            and records == previous["lifecycle"]["records"]
            and self._authoritative_content(catalog) == self._authoritative_content(previous["catalog"])
        )

    def commit(self, inventory: dict, records: dict, operation: str, actor: str, reason: str, previous: dict | None = None, archived_devices: list[dict] | None = None) -> dict:
        generation_id = _generation_id()
        transaction_id = "txn_" + uuid.uuid4().hex
        previous_lifecycle = previous["lifecycle"] if previous else {"records": {}}
        catalog = self._build_catalog(inventory, archived_devices, generation_id)
        if previous:
            archived_ids = {device_id for device_id, record in records.items() if record["state"] == ARCHIVED}
            services = {service.get("id"): dict(service) for service in catalog["services"] if service.get("id")}
            for service in previous["catalog"]["services"]:
                if service.get("device_id") in archived_ids and service.get("id"):
                    services.setdefault(service["id"], dict(service))
            catalog["services"] = sorted(services.values(), key=lambda item: item["id"])
            topology_edges = {json.dumps(edge, sort_keys=True): dict(edge) for edge in catalog["topology"].get("edges", [])}
            for edge in previous["catalog"]["topology"].get("edges", []):
                if edge.get("parent_id") in archived_ids or edge.get("child_id") in archived_ids:
                    topology_edges.setdefault(json.dumps(edge, sort_keys=True), dict(edge))
            catalog["topology"]["edges"] = list(topology_edges.values())
            dependency_edges = {json.dumps(edge, sort_keys=True): dict(edge) for edge in catalog["dependencies"].get("edges", [])}
            for edge in previous["catalog"]["dependencies"].get("edges", []):
                if edge.get("from_id") in archived_ids or edge.get("to_id") in archived_ids:
                    dependency_edges.setdefault(json.dumps(edge, sort_keys=True), dict(edge))
            catalog["dependencies"]["edges"] = list(dependency_edges.values())
        if self._is_noop(previous, catalog, records):
            return previous
        lifecycle = {"schema_version": SCHEMA_VERSION, "migration_version": MIGRATION_VERSION, "generation_id": generation_id, "records": records}
        validate_catalog(catalog, generation_id)
        validate_lifecycle(lifecycle, catalog, generation_id)
        changes = lifecycle_diff(previous_lifecycle, lifecycle)
        receipts = [{
            "transaction_id": transaction_id, "generation_id": generation_id, "device_id": device_id,
            "previous_state": old, "new_state": new,
        } for device_id, old, new in changes]
        operation_receipt = {"transaction_id": transaction_id, "operation": operation, "actor": actor, "reason": reason, "timestamp": _now(), "previous_generation_id": previous["id"] if previous else None}
        receipt_hash = _digest({"operation": operation_receipt, "transitions": receipts})
        operation_receipt["transition_hash"] = receipt_hash
        active = _projection(catalog, lifecycle, ACTIVE, catalog["summary_template"])
        archived = _projection(catalog, lifecycle, ARCHIVED, {})
        manifest = {
            "schema_version": SCHEMA_VERSION, "migration_version": MIGRATION_VERSION, "generation_id": generation_id,
            "transaction_id": transaction_id, "previous_generation_id": previous["id"] if previous else None,
            "catalog_sha256": _digest(catalog), "lifecycle_sha256": _digest(lifecycle),
            "operation_receipt": operation_receipt, "transition_receipts": receipts,
        }
        validate_receipt_bijection(previous_lifecycle, lifecycle, manifest, catalog)
        if operation == "migration":
            original_ids = _device_ids(inventory["devices"], "legacy inventory")
            projected_ids = _device_ids(active["devices"], "migrated active inventory")
            if original_ids != projected_ids or archived["devices"]:
                raise LifecycleValidationError("migration changed active device identity or archived a record")
            original_by_id = {item["id"]: item for item in inventory["devices"]}
            projected_by_id = {item["id"]: item for item in active["devices"]}
            for device_id in original_ids:
                for field in ("first_seen", "last_seen", "last_seen_epoch", "source", "sources"):
                    if original_by_id[device_id].get(field) != projected_by_id[device_id].get(field):
                        raise LifecycleValidationError(f"migration changed {field} for {device_id}")
            for field in ("services", "topology", "dependencies"):
                if inventory[field] != active[field]:
                    raise LifecycleValidationError(f"migration changed {field}")
        self.transactions_dir.mkdir(parents=True, exist_ok=True)
        self.generations_dir.mkdir(parents=True, exist_ok=True)
        staging = self.transactions_dir / generation_id
        staging.mkdir()
        store = StateStore(staging)
        for name, payload in (("catalog.json", catalog), ("lifecycle.json", lifecycle), ("inventory.json", active), ("archived.json", archived), ("manifest.json", manifest)):
            store.write_json_durable(name, payload)
        fsync_directory(staging)
        destination = self.generations_dir / generation_id
        os.replace(staging, destination)
        fsync_directory(self.generations_dir)
        pointer_tmp = self.state_dir / "CURRENT.tmp"
        with pointer_tmp.open("w", encoding="utf-8") as handle:
            handle.write(generation_id + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(pointer_tmp, self.state_dir / "CURRENT")
        fsync_directory(self.state_dir)
        committed = self.load_generation(generation_id)
        self.materialize_after_commit(committed)
        return committed

    def _segment_path(self, generation_id: str) -> Path:
        return self.receipts_dir / f"{generation_id}.json"

    def materialize_receipt(self, generation: dict, validate_chain: bool = False) -> None:
        if validate_chain:
            self.validate_generation_chain(generation["id"])
        self.receipts_dir.mkdir(parents=True, exist_ok=True)
        segment = {"schema_version": SCHEMA_VERSION, "migration_version": MIGRATION_VERSION, "generation_id": generation["id"], "operation_receipt": generation["manifest"]["operation_receipt"], "transition_receipts": generation["manifest"]["transition_receipts"]}
        path = self._segment_path(generation["id"])
        if path.exists():
            if self._strict(path) != segment:
                raise LifecycleValidationError(f"immutable receipt segment differs for {generation['id']}")
            return
        StateStore(path.parent).write_json_durable(path.name, segment)

    def _index_document(self, generation_id: str | None = None) -> dict:
        receipts = sorted(self.receipts_dir.glob("*.json")) if self.receipts_dir.exists() else []
        return {
            "schema_version": SCHEMA_VERSION,
            "migration_version": MIGRATION_VERSION,
            "generation_id": generation_id or self.current_generation_id(),
            "representation": "immutable_receipt_segments_v1",
            "receipt_count": len(receipts),
            "receipts_path": "receipts",
        }

    def _validate_index(self, index: dict, expected_count: int | None = None) -> None:
        _validate_header(index, "lifecycle event index")
        if index.get("representation") != "immutable_receipt_segments_v1":
            raise LifecycleValidationError("lifecycle event index representation is invalid")
        if not isinstance(index.get("receipt_count"), int) or isinstance(index.get("receipt_count"), bool):
            raise LifecycleValidationError("lifecycle event index receipt_count is invalid")
        expected = expected_count if expected_count is not None else (
            len(list(self.receipts_dir.glob("*.json"))) if self.receipts_dir.exists() else 0
        )
        if index["receipt_count"] != expected:
            raise LifecycleValidationError("lifecycle event index receipt count is stale")

    def update_event_index(self, generation: dict) -> dict:
        """Atomically update the constant-size receipt-segment index after one commit."""
        index_path = self.events_dir / "lifecycle_events.json"
        if index_path.exists():
            receipt_count = len(list(self.receipts_dir.glob("*.json")))
            self._validate_index(self._strict(index_path), max(0, receipt_count - 1))
        index = self._index_document(generation["id"])
        if not index_path.exists() or self._strict(index_path) != index:
            StateStore(self.events_dir).write_json_durable("lifecycle_events.json", index)
        return index

    def rebuild_event_index(self, quarantine_corrupt: bool = False) -> dict:
        self.receipts_dir.mkdir(parents=True, exist_ok=True)
        index_path = self.events_dir / "lifecycle_events.json"
        if index_path.exists():
            try:
                existing = self._strict(index_path)
                self._validate_index(existing)
            except Exception:
                if not quarantine_corrupt:
                    raise
                quarantine = self.events_dir / "quarantine"
                quarantine.mkdir(parents=True, exist_ok=True)
                os.replace(index_path, quarantine / f"lifecycle_events.json.{int(time.time())}.corrupt")
        for path in sorted(self.receipts_dir.glob("*.json")):
            try:
                segment = self._strict(path)
                _validate_header(segment, "lifecycle receipt segment", path.stem)
                generation = self.load_generation(path.stem)
                if segment != self._receipt_segment(generation):
                    raise LifecycleValidationError(f"receipt segment mismatch for {path.stem}")
            except Exception:
                if not quarantine_corrupt:
                    raise
                quarantine = self.events_dir / "quarantine"
                quarantine.mkdir(parents=True, exist_ok=True)
                os.replace(path, quarantine / f"{path.name}.{int(time.time())}.corrupt")
        self.validate_all_generation_chains()
        index = self._index_document()
        StateStore(self.events_dir).write_json_durable("lifecycle_events.json", index)
        return index

    def repair_audit(self) -> dict:
        self.receipts_dir.mkdir(parents=True, exist_ok=True)
        quarantine = self.events_dir / "quarantine"
        generations = self.validate_all_generation_chains()
        for generation in generations.values():
            path = self._segment_path(generation["id"])
            try:
                self.materialize_receipt(generation)
            except Exception:
                quarantine.mkdir(parents=True, exist_ok=True)
                if path.exists():
                    os.replace(path, quarantine / f"{path.name}.{int(time.time())}.corrupt")
                self.materialize_receipt(generation)
        index_path = self.events_dir / "lifecycle_events.json"
        if index_path.exists():
            try:
                self._strict(index_path)
            except Exception:
                quarantine.mkdir(parents=True, exist_ok=True)
                os.replace(index_path, quarantine / f"lifecycle_events.json.{int(time.time())}.corrupt")
        return self.rebuild_event_index(quarantine_corrupt=True)

    def audit_status(self) -> dict:
        generations = self.validate_all_generation_chains()
        expected = set(generations)
        index = self._strict(self.events_dir / "lifecycle_events.json")
        self._validate_index(index)
        actual = {path.stem for path in self.receipts_dir.glob("*.json")}
        if actual != expected or index.get("generation_id") != self.current_generation_id():
            raise LifecycleValidationError("lifecycle event projection does not cover every generation")
        for generation_id in expected:
            generation = generations[generation_id]
            segment = self._strict(self._segment_path(generation_id))
            expected_segment = self._receipt_segment(generation)
            if segment != expected_segment:
                raise LifecycleValidationError(f"receipt segment mismatch for {generation_id}")
        health_path = self.events_dir / "audit_status.json"
        health = self._strict(health_path) if health_path.exists() else {"status": "unknown", "warning": "audit health status is missing"}
        return {"status": "valid", "event_generations": len(expected), "audit_health": health.get("status", "unknown"), "warning": health.get("warning", "")}

    @staticmethod
    def _receipt_segment(generation: dict) -> dict:
        return {
            "schema_version": SCHEMA_VERSION, "migration_version": MIGRATION_VERSION,
            "generation_id": generation["id"],
            "operation_receipt": generation["manifest"]["operation_receipt"],
            "transition_receipts": generation["manifest"]["transition_receipts"],
        }

    def _write_json_if_changed(self, path: Path, payload: dict | list) -> bool:
        try:
            if self._strict(path) == payload:
                return False
        except (StateMissingError, StateMalformedError, StateIOError):
            pass
        StateStore(path.parent).write_json_durable(path.name, payload)
        return True

    def _materialize_projections(self, generation: dict) -> None:
        generation_store = StateStore(generation["root"])
        for name, payload in (("inventory.json", generation["inventory"]), ("archived.json", generation["archived"])):
            self._write_json_if_changed(generation_store.path(name), payload)
        root_values = (
            ("inventory.json", generation["inventory"]), ("archived.json", generation["archived"]),
            ("devices.json", generation["inventory"]["devices"]),
            ("services.json", generation["inventory"]["services"]),
            ("topology.json", generation["inventory"]["topology"]),
            ("dependencies.json", generation["inventory"]["dependencies"]),
            ("summary.json", generation["inventory"]["summary"]),
        )
        for name, payload in root_values:
            self._write_json_if_changed(self.state_dir / name, payload)
        status_path = self.state_dir / "status.json"
        stable_status = {
            "status": "online",
            "device_count": generation["inventory"]["summary"]["device_count"],
            "schema_version": generation["inventory"]["schema_version"],
        }
        try:
            current_status = self._strict(status_path)
        except (StateMissingError, StateMalformedError, StateIOError):
            current_status = {}
        if any(current_status.get(key) != value for key, value in stable_status.items()):
            self._write_json_if_changed(status_path, {**stable_status, "updated": _now()})

    def _write_audit_health(self, status: str, warning: str) -> None:
        path = self.events_dir / "audit_status.json"
        stable = {"schema_version": SCHEMA_VERSION, "status": status, "warning": warning}
        try:
            current = self._strict(path)
            if all(current.get(key) == value for key, value in stable.items()):
                return
        except (StateMissingError, StateMalformedError, StateIOError):
            pass
        self._write_json_if_changed(path, {**stable, "updated": _now()})

    def materialize_after_commit(self, generation: dict) -> None:
        """Materialize only the newly committed audit record and current projections."""
        try:
            self.materialize_receipt(generation)
            self.update_event_index(generation)
            self._write_audit_health("healthy", "")
        except Exception:
            self.repair_audit()
            self._write_audit_health("repaired", "lifecycle audit projection was rebuilt from committed manifests")
        self._materialize_projections(generation)

    def materialize_current_if_needed(self, generation: dict | None = None) -> None:
        """Repair missing/stale projections without rewriting correct files."""
        generation = generation or self.load_generation()
        repaired = False
        try:
            if self._strict(self._segment_path(generation["id"])) != self._receipt_segment(generation):
                raise LifecycleValidationError("current receipt segment differs from committed manifest")
        except Exception:
            path = self._segment_path(generation["id"])
            if path.exists():
                quarantine = self.events_dir / "quarantine"
                quarantine.mkdir(parents=True, exist_ok=True)
                os.replace(path, quarantine / f"{path.name}.{int(time.time())}.corrupt")
            self.repair_audit()
            repaired = True
        try:
            index = self._strict(self.events_dir / "lifecycle_events.json")
            self._validate_index(index)
            if index.get("generation_id") != generation["id"]:
                raise LifecycleValidationError("lifecycle event index is stale")
        except Exception:
            self.repair_audit()
            repaired = True
        if repaired:
            self._write_audit_health("repaired", "lifecycle audit projection was rebuilt from committed manifests")
        self._materialize_projections(generation)

    # Explicit repair command compatibility.
    def repair_after_commit(self, generation: dict | None = None) -> None:
        self.materialize_current_if_needed(generation)

    def apply_discovery(self, inventory: dict, positive_ids: set[str]) -> dict:
        previous = self.load_generation()
        records = {device_id: dict(record) for device_id, record in previous["lifecycle"]["records"].items()}
        old_devices = {device["id"]: device for device in previous["catalog"]["devices"]}
        current_devices = {device["id"]: device for device in inventory["devices"]}
        archived_records = [old_devices[device_id] for device_id, record in records.items() if record["state"] == ARCHIVED and device_id in old_devices]
        weak_conflicts = set()
        for device_id, current in current_devices.items():
            if current.get("mac"):
                continue
            if any(
                (current.get("ip") and current.get("ip") == archived.get("ip"))
                or (current.get("hostname") and current.get("hostname") == archived.get("hostname"))
                for archived in archived_records
            ):
                weak_conflicts.add(device_id)
        if weak_conflicts:
            inventory = dict(inventory)
            inventory["devices"] = [item for item in inventory["devices"] if item["id"] not in weak_conflicts]
            current_devices = {device["id"]: device for device in inventory["devices"]}
        for device_id in current_devices:
            records.setdefault(device_id, {"device_id": device_id, "state": ACTIVE, "changed_at": inventory.get("updated", _now()), "changed_by": "discovery"})
        restored = []
        for device_id, record in records.items():
            if record["state"] != ARCHIVED or device_id not in positive_ids:
                continue
            current = current_devices.get(device_id)
            archived = old_devices.get(device_id)
            if (
                not current or not archived or not current.get("mac")
                or current.get("mac") != archived.get("mac")
                or _mac_device_id(current.get("mac")) != device_id
            ):
                continue
            record.update({"state": ACTIVE, "changed_at": inventory.get("updated", _now()), "changed_by": "strong_rediscovery"})
            restored.append(device_id)
        archived_devices = [old_devices[device_id] for device_id, record in records.items() if record["state"] == ARCHIVED and device_id in old_devices]
        operation = "automatic_restore" if restored else "inventory_refresh"
        reason = "strong positive MAC rediscovery" if restored else "passive inventory refresh"
        return self.commit(inventory, records, operation, "inventory-engine", reason, previous, archived_devices)

    def transition(self, device_id: str, state: str, reason: str, actor: str) -> dict:
        if state not in SUPPORTED_STATES or not reason.strip():
            raise LifecycleValidationError("valid state and nonempty reason are required")
        previous = self.load_generation()
        devices = {device["id"]: device for device in previous["catalog"]["devices"]}
        if device_id not in devices:
            raise LifecycleValidationError(f"unknown stable device id: {device_id}")
        if state == ARCHIVED and _protected(devices[device_id]):
            raise LifecycleProtectedError(f"protected asset cannot be archived: {device_id}")
        records = {key: dict(value) for key, value in previous["lifecycle"]["records"].items()}
        if records[device_id]["state"] == state:
            raise LifecycleValidationError(f"device is already {state}")
        records[device_id].update({"state": state, "changed_at": _now(), "changed_by": actor})
        active_ids = {key for key, record in records.items() if record["state"] == ACTIVE}
        catalog = previous["catalog"]
        active_inventory = _projection(catalog, {**previous["lifecycle"], "records": {key: {**value, "state": ACTIVE if key in active_ids else ARCHIVED} for key, value in records.items()}}, ACTIVE, catalog.get("summary_template", {}))
        archived_devices = [device for device in catalog["devices"] if records[device["id"]]["state"] == ARCHIVED]
        return self.commit(active_inventory, records, "archive" if state == ARCHIVED else "restore", actor, reason.strip(), previous, archived_devices)

    def rollback(self, generation_id: str, actor: str = "operator") -> dict:
        current_chain = self.validate_generation_chain()
        target_chain = self.validate_generation_chain(generation_id)
        current = current_chain[self.current_generation_id()]
        target = target_chain[generation_id]
        current_ids = set(current["lifecycle"]["records"])
        target_ids = set(target["lifecycle"]["records"])
        if current_ids != target_ids:
            raise LifecycleValidationError("rollback requires identical stable-id sets; restore the pre-migration backup for structural rollback")
        records = {key: dict(value) for key, value in target["lifecycle"]["records"].items()}
        changed_at = _now()
        for device_id, record in records.items():
            if current["lifecycle"]["records"][device_id]["state"] != record["state"]:
                record.update({"changed_at": changed_at, "changed_by": actor})
        archived_devices = [device for device in target["catalog"]["devices"] if records[device["id"]]["state"] == ARCHIVED]
        return self.commit(target["inventory"], records, "rollback", actor, f"rollback to {generation_id}", current, archived_devices)

    def list_generations(self) -> list[dict]:
        current = self.current_generation_id()
        rows = []
        for path in sorted(self.generations_dir.iterdir()):
            if not path.is_dir():
                continue
            generation = self.load_generation(path.name)
            rows.append({"generation_id": path.name, "current": path.name == current, "operation": generation["manifest"]["operation_receipt"]["operation"], "timestamp": generation["manifest"]["operation_receipt"]["timestamp"]})
        return rows

    def validate_prune(self, generation_id: str) -> dict:
        if generation_id == self.current_generation_id():
            raise LifecycleValidationError("current generation cannot be pruned")
        generation = self.validate_generation_chain(generation_id)[generation_id]
        segment = self._strict(self._segment_path(generation_id))
        expected = {"schema_version": SCHEMA_VERSION, "migration_version": MIGRATION_VERSION, "generation_id": generation_id, "operation_receipt": generation["manifest"]["operation_receipt"], "transition_receipts": generation["manifest"]["transition_receipts"]}
        if segment != expected:
            raise LifecycleValidationError("receipt segment does not match generation manifest")
        return {"generation_id": generation_id, "prunable": True, "dry_run": True}
