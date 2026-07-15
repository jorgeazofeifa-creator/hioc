import json
import hashlib
import importlib.util
import io
import logging
import sys
import tempfile
import threading
import time
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
LIFECYCLE_SCRIPT = ROOT / "pi4" / "bin" / "hioc-inventory-lifecycle.py"
ENGINE_SCRIPT = ROOT / "pi4" / "bin" / "hioc-inventory-engine.py"
sys.path.insert(0, str(ROOT / "pi4" / "lib"))

from hioc.lifecycle import (
    ACTIVE,
    ARCHIVED,
    LifecycleError,
    LifecycleProtectedError,
    LifecycleStore,
    LifecycleValidationError,
    validate_receipt_bijection,
)
from hioc.core.correlation import build_inventory_signals


def load_script(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def device(device_id="dev_client", mac="aa:bb:cc:dd:ee:01", **values):
    record = {
        "id": device_id,
        "display_name": values.pop("display_name", "Passive Client"),
        "name": "Passive Client",
        "ip": "192.0.2.10",
        "mac": mac,
        "type": "endpoint",
        "roles": ["endpoint"],
        "role": "Unknown",
        "inventory_class": "client",
        "sources": ["arp_table"],
        "source": "arp_table",
        "operationally_monitored": False,
        "health_status": "watch",
        "health_score": 75,
        "observation_status": "stale",
        "first_seen": "2026-01-01T00:00:00+00:00",
        "last_seen": "2026-01-02T00:00:00+00:00",
        "last_seen_epoch": 1767312000,
    }
    record.update(values)
    return record


def inventory(devices=None, services=None, topology=None, dependencies=None):
    devices = list(devices or [device()])
    services = list(services or [])
    topology = topology or {"root_id": "", "edges": []}
    dependencies = dependencies or {"edges": []}
    return {
        "schema_version": "1.0",
        "updated": "2026-07-14T00:00:00+00:00",
        "devices": devices,
        "services": services,
        "topology": topology,
        "dependencies": dependencies,
        "summary": {
            "updated": "2026-07-14T00:00:00+00:00",
            "device_count": len(devices),
            "infrastructure_count": 0,
            "client_count": len(devices),
            "network_client_count": len(devices),
            "healthy_count": 0,
            "watch_count": len(devices),
            "degraded_count": 0,
            "offline_count": 0,
            "service_count": len(services),
            "topology_edges": len(topology["edges"]),
            "dependency_edges": len(dependencies["edges"]),
            "lowest_health_score": 75 if devices else 0,
            "infrastructure_devices": [],
            "services": [{
                "name": service.get("name", ""), "host": service.get("host", ""),
                "type": service.get("type", ""), "status": service.get("status", ""),
                "dependency": service.get("dependency", ""),
            } for service in services],
        },
    }


class InventoryLifecycleTests(unittest.TestCase):
    def make_store(self, root, payload=None):
        state = Path(root) / "state" / "inventory"
        state.mkdir(parents=True)
        if payload is not None:
            (state / "inventory.json").write_text(json.dumps(payload), encoding="utf-8")
        return LifecycleStore(state, lock_timeout=0.1)

    @staticmethod
    def tree_snapshot(root):
        root = Path(root)
        rows = {}
        for path in sorted(root.rglob("*")):
            stat = path.stat()
            relative = str(path.relative_to(root))
            if path.is_dir():
                rows[relative] = ("dir", stat.st_mtime_ns)
            else:
                rows[relative] = ("file", stat.st_mtime_ns, stat.st_size, hashlib.sha256(path.read_bytes()).hexdigest())
        return rows

    def test_initial_migration_preserves_inventory_and_defaults_every_device_active(self):
        with tempfile.TemporaryDirectory() as tmp:
            original = inventory(
                services=[{"id": "svc_client", "name": "Client service", "type": "test", "device_id": "dev_client", "status": "known"}],
                dependencies={"edges": [{"from_id": "dev_client", "to_id": "svc_client", "type": "uses"}]},
            )
            store = self.make_store(tmp, original)
            with store.lock():
                generation = store.ensure_initialized()
            self.assertEqual(generation["inventory"], original)
            self.assertEqual(generation["lifecycle"]["records"]["dev_client"]["state"], ACTIVE)
            self.assertEqual(generation["archived"]["devices"], [])
            self.assertTrue(list((Path(tmp) / "state" / "backups").iterdir()))
            self.assertEqual(len(generation["manifest"]["transition_receipts"]), 1)

    def test_migration_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = self.make_store(tmp, inventory())
            with store.lock():
                first = store.ensure_initialized()
            before = self.tree_snapshot(store.state_dir)
            with store.lock():
                second = store.ensure_initialized()
            after = self.tree_snapshot(store.state_dir)
            self.assertEqual(first["id"], second["id"])
            self.assertEqual(before, after)
            self.assertEqual(len(store.list_generations()), 1)

    def test_corrupt_legacy_inventory_cannot_migrate_to_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = self.make_store(tmp)
            (store.state_dir / "inventory.json").write_text("{broken", encoding="utf-8")
            with store.lock(), self.assertRaises(Exception):
                store.ensure_initialized()
            self.assertFalse((store.state_dir / "CURRENT").exists())
            self.assertEqual((store.state_dir / "inventory.json").read_text(encoding="utf-8"), "{broken")

    def test_duplicate_or_missing_ids_block_migration(self):
        for records in ([device(), device()], [{"mac": "aa:bb:cc:dd:ee:02"}]):
            with self.subTest(records=records), tempfile.TemporaryDirectory() as tmp:
                store = self.make_store(tmp, inventory(records))
                with store.lock(), self.assertRaises(LifecycleValidationError):
                    store.ensure_initialized()
                self.assertFalse((store.state_dir / "CURRENT").exists())

    def test_malformed_current_catalog_and_generation_mismatch_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = self.make_store(tmp, inventory())
            with store.lock():
                generation = store.ensure_initialized()
            catalog_path = generation["root"] / "catalog.json"
            catalog = json.loads(catalog_path.read_text())
            catalog["generation_id"] = "wrong"
            catalog_path.write_text(json.dumps(catalog))
            with self.assertRaises(LifecycleValidationError):
                store.load_generation()
            self.assertEqual(json.loads((store.state_dir / "inventory.json").read_text())["devices"][0]["id"], "dev_client")

    def test_unsupported_or_malformed_schema_versions_fail_closed(self):
        for version in ("2.0", None, 1):
            with self.subTest(version=version), tempfile.TemporaryDirectory() as tmp:
                store = self.make_store(tmp, inventory())
                with store.lock():
                    generation = store.ensure_initialized()
                catalog = json.loads((generation["root"] / "catalog.json").read_text())
                catalog["schema_version"] = version
                catalog["generation_id"] = generation["id"]
                (generation["root"] / "catalog.json").write_text(json.dumps(catalog))
                with self.assertRaises(LifecycleValidationError):
                    store.load_generation()

    def test_manual_archive_excludes_active_counts_and_remains_searchable(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = self.make_store(tmp, inventory())
            with store.lock():
                store.ensure_initialized()
                generation = store.transition("dev_client", ARCHIVED, "guest device left", "tester")
            self.assertEqual(generation["inventory"]["devices"], [])
            self.assertEqual(generation["inventory"]["summary"]["device_count"], 0)
            self.assertEqual(generation["inventory"]["summary"]["watch_count"], 0)
            self.assertEqual(generation["archived"]["devices"][0]["id"], "dev_client")
            self.assertEqual(generation["inventory"]["services"], [])
            self.assertEqual(generation["inventory"]["dependencies"]["edges"], [])
            self.assertEqual(build_inventory_signals(generation["inventory"]), [])

    def test_manual_restore_preserves_identity_metadata_and_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            original = inventory()
            store = self.make_store(tmp, original)
            with store.lock():
                store.ensure_initialized()
                store.transition("dev_client", ARCHIVED, "archive", "tester")
                restored = store.transition("dev_client", ACTIVE, "return", "tester")
            current = restored["inventory"]["devices"][0]
            self.assertEqual(current["id"], "dev_client")
            self.assertEqual(current["first_seen"], original["devices"][0]["first_seen"])
            self.assertEqual(current["last_seen"], original["devices"][0]["last_seen"])

    def test_protected_assets_cannot_be_archived_and_no_force_api_exists(self):
        protected = device("dev_gateway", type="gateway", roles=["gateway"], inventory_class="infrastructure", operationally_monitored=True)
        with tempfile.TemporaryDirectory() as tmp:
            store = self.make_store(tmp, inventory([protected]))
            with store.lock():
                store.ensure_initialized()
                with self.assertRaises(LifecycleProtectedError):
                    store.transition("dev_gateway", ARCHIVED, "not allowed", "tester")
            cli = (ROOT / "pi4" / "bin" / "hioc-inventory-lifecycle.py").read_text()
            self.assertNotIn("--force", cli)

    def test_age_health_and_lease_fields_never_archive_automatically(self):
        old = device(observation_status="expired", health_status="offline", lease_expires_epoch=1)
        with tempfile.TemporaryDirectory() as tmp:
            store = self.make_store(tmp, inventory([old]))
            with store.lock():
                first = store.ensure_initialized()
                refreshed = store.apply_discovery(first["inventory"], set())
            self.assertEqual(refreshed["lifecycle"]["records"]["dev_client"]["state"], ACTIVE)

    def test_strong_positive_mac_rediscovery_restores_without_duplicate(self):
        mac = "aa:bb:cc:dd:ee:01"
        strong_id = "dev_" + hashlib.sha1(mac.encode()).hexdigest()[:16]
        with tempfile.TemporaryDirectory() as tmp:
            strong_inventory = inventory([device(strong_id, mac=mac)])
            store = self.make_store(tmp, strong_inventory)
            with store.lock():
                store.ensure_initialized()
                store.transition(strong_id, ARCHIVED, "archive", "tester")
                restored = store.apply_discovery(strong_inventory, {strong_id})
            self.assertEqual(restored["lifecycle"]["records"][strong_id]["state"], ACTIVE)
            self.assertEqual(len(restored["catalog"]["devices"]), 1)
            self.assertEqual(restored["manifest"]["operation_receipt"]["operation"], "automatic_restore")
            self.assertEqual(build_inventory_signals(restored["inventory"]), [])

    def test_dhcp_ip_hostname_and_ambiguous_evidence_do_not_restore(self):
        cases = (
            (inventory(), set()),
            (inventory([device(mac="")]), {"dev_client"}),
            (inventory([device(mac="aa:bb:cc:dd:ee:99")]), {"dev_client"}),
        )
        for discovered, positive in cases:
            with self.subTest(discovered=discovered), tempfile.TemporaryDirectory() as tmp:
                store = self.make_store(tmp, inventory())
                with store.lock():
                    store.ensure_initialized()
                    store.transition("dev_client", ARCHIVED, "archive", "tester")
                    result = store.apply_discovery(discovered, positive)
                self.assertEqual(result["lifecycle"]["records"]["dev_client"]["state"], ARCHIVED)

    def test_weak_match_to_archived_identity_does_not_create_duplicate(self):
        weak = device("dev_ip_only", mac="", display_name="Weak IP observation")
        with tempfile.TemporaryDirectory() as tmp:
            store = self.make_store(tmp, inventory())
            with store.lock():
                store.ensure_initialized()
                store.transition("dev_client", ARCHIVED, "archive", "tester")
                result = store.apply_discovery(inventory([weak]), {"dev_ip_only"})
            self.assertEqual(set(result["lifecycle"]["records"]), {"dev_client"})
            self.assertEqual(result["lifecycle"]["records"]["dev_client"]["state"], ARCHIVED)

    def test_receipt_bijection_rejects_missing_duplicate_and_unknown_receipts(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = self.make_store(tmp, inventory())
            with store.lock():
                generation = store.ensure_initialized()
            manifest = dict(generation["manifest"])
            manifest["transition_receipts"] = []
            with self.assertRaises(LifecycleValidationError):
                validate_receipt_bijection({"records": {}}, generation["lifecycle"], manifest, generation["catalog"])

    def test_receipt_segment_and_index_are_repairable_from_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = self.make_store(tmp, inventory())
            with store.lock():
                generation = store.ensure_initialized()
                segment = store._segment_path(generation["id"])
                segment.unlink()
                (store.events_dir / "lifecycle_events.json").write_text("broken")
                store.repair_after_commit(generation)
            self.assertTrue(segment.exists())
            index = json.loads((store.events_dir / "lifecycle_events.json").read_text())
            self.assertEqual(index["representation"], "immutable_receipt_segments_v1")
            self.assertEqual(index["receipt_count"], 1)
            self.assertEqual(index["generation_id"], generation["id"])
            status = store.audit_status()
            self.assertEqual(status["status"], "valid")
            self.assertEqual(status["audit_health"], "repaired")

    def test_projection_corruption_repairs_from_authoritative_generation(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = self.make_store(tmp, inventory())
            with store.lock():
                generation = store.ensure_initialized()
                (store.state_dir / "inventory.json").write_text("broken")
                store.repair_after_commit(generation)
            repaired = json.loads((store.state_dir / "inventory.json").read_text())
            self.assertEqual(repaired, generation["inventory"])

    def test_corrupt_generation_projection_regenerates_from_catalog_and_lifecycle(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = self.make_store(tmp, inventory())
            with store.lock():
                generation = store.ensure_initialized()
                (generation["root"] / "inventory.json").write_text("{broken")
                repaired = store.load_generation()
            self.assertEqual(repaired["inventory"]["devices"][0]["id"], "dev_client")
            self.assertIn("inventory.json", repaired["projection_issues"])
            with store.lock():
                store.repair_after_commit(repaired)
            self.assertEqual(json.loads((generation["root"] / "inventory.json").read_text()), repaired["inventory"])

    def test_rollback_is_a_new_audited_generation(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = self.make_store(tmp, inventory())
            with store.lock():
                initial = store.ensure_initialized()
                store.transition("dev_client", ARCHIVED, "archive", "tester")
                rolled_back = store.rollback(initial["id"])
            self.assertNotEqual(rolled_back["id"], initial["id"])
            self.assertEqual(rolled_back["lifecycle"]["records"]["dev_client"]["state"], ACTIVE)
            self.assertEqual(rolled_back["manifest"]["operation_receipt"]["operation"], "rollback")

    def test_rollback_updates_only_records_whose_state_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            original = inventory([device(), device("dev_second", mac="aa:bb:cc:dd:ee:02")])
            store = self.make_store(tmp, original)
            with store.lock():
                initial = store.ensure_initialized()
                store.transition("dev_client", ARCHIVED, "archive", "archiver")
                rolled_back = store.rollback(initial["id"], actor="rollback-operator")
            changed = rolled_back["lifecycle"]["records"]["dev_client"]
            unchanged = rolled_back["lifecycle"]["records"]["dev_second"]
            self.assertEqual(changed["changed_by"], "rollback-operator")
            self.assertNotEqual(changed["changed_at"], initial["lifecycle"]["records"]["dev_client"]["changed_at"])
            self.assertEqual(unchanged, initial["lifecycle"]["records"]["dev_second"])
            self.assertEqual(len(rolled_back["manifest"]["transition_receipts"]), 1)
            self.assertEqual(rolled_back["manifest"]["operation_receipt"]["reason"], f"rollback to {initial['id']}")

    def test_identical_and_derived_only_discovery_are_generation_noops(self):
        with tempfile.TemporaryDirectory() as tmp:
            original = inventory()
            store = self.make_store(tmp, original)
            with store.lock():
                initial = store.ensure_initialized()
            before = self.tree_snapshot(store.state_dir)
            with store.lock():
                identical = store.apply_discovery(json.loads(json.dumps(original)), set())
                derived = json.loads(json.dumps(original))
                derived["updated"] = "2026-07-14T00:30:00+00:00"
                derived["summary"]["updated"] = derived["updated"]
                derived["summary"]["watch_count"] = 999
                derived_result = store.apply_discovery(derived, set())
            after = self.tree_snapshot(store.state_dir)
            self.assertEqual(identical["id"], initial["id"])
            self.assertEqual(derived_result["id"], initial["id"])
            self.assertEqual(before, after)
            self.assertEqual(len(store.list_generations()), 1)

    def test_positive_observation_update_creates_one_incremental_audit_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            original = inventory()
            store = self.make_store(tmp, original)
            with store.lock():
                initial = store.ensure_initialized()
                changed = json.loads(json.dumps(original))
                changed["devices"][0]["last_seen"] = "2026-07-14T00:30:00+00:00"
                changed["devices"][0]["last_seen_epoch"] += 1800
                refreshed = store.apply_discovery(changed, set())
            self.assertNotEqual(refreshed["id"], initial["id"])
            self.assertEqual(len(store.list_generations()), 2)
            index = json.loads((store.events_dir / "lifecycle_events.json").read_text())
            self.assertEqual(index["receipt_count"], 2)
            self.assertLess((store.events_dir / "lifecycle_events.json").stat().st_size, 400)

    def test_read_only_cli_commands_make_zero_persistent_changes(self):
        module = load_script("hioc_lifecycle_cli", LIFECYCLE_SCRIPT)
        with tempfile.TemporaryDirectory() as tmp:
            store = self.make_store(tmp, inventory())
            with store.lock():
                store.ensure_initialized()
            for command in ("validate", "audit-status", "list-generations"):
                before = self.tree_snapshot(store.state_dir.parent)
                argv = [str(LIFECYCLE_SCRIPT), "--state-dir", str(store.state_dir), command]
                with patch.object(sys, "argv", argv), redirect_stdout(io.StringIO()):
                    self.assertEqual(module.main(), 0)
                self.assertEqual(self.tree_snapshot(store.state_dir.parent), before, command)

    def test_read_only_validate_does_not_migrate_legacy_state(self):
        module = load_script("hioc_lifecycle_cli_legacy", LIFECYCLE_SCRIPT)
        with tempfile.TemporaryDirectory() as tmp:
            store = self.make_store(tmp, inventory())
            before = self.tree_snapshot(store.state_dir.parent)
            argv = [str(LIFECYCLE_SCRIPT), "--state-dir", str(store.state_dir), "validate"]
            with patch.object(sys, "argv", argv), redirect_stdout(io.StringIO()):
                self.assertNotEqual(module.main(), 0)
            self.assertEqual(self.tree_snapshot(store.state_dir.parent), before)
            self.assertFalse((store.state_dir / "CURRENT").exists())

    def test_read_only_validate_reports_but_does_not_repair_projection(self):
        module = load_script("hioc_lifecycle_cli_projection", LIFECYCLE_SCRIPT)
        with tempfile.TemporaryDirectory() as tmp:
            store = self.make_store(tmp, inventory())
            with store.lock():
                generation = store.ensure_initialized()
            projection = generation["root"] / "inventory.json"
            projection.write_text("{broken", encoding="utf-8")
            before = self.tree_snapshot(store.state_dir.parent)
            output = io.StringIO()
            argv = [str(LIFECYCLE_SCRIPT), "--state-dir", str(store.state_dir), "validate"]
            with patch.object(sys, "argv", argv), redirect_stdout(output):
                self.assertEqual(module.main(), 0)
            self.assertIn("inventory.json", output.getvalue())
            self.assertEqual(self.tree_snapshot(store.state_dir.parent), before)
            self.assertEqual(projection.read_text(encoding="utf-8"), "{broken")

    def test_read_only_audit_status_reports_corruption_without_repair(self):
        module = load_script("hioc_lifecycle_cli_audit", LIFECYCLE_SCRIPT)
        with tempfile.TemporaryDirectory() as tmp:
            store = self.make_store(tmp, inventory())
            with store.lock():
                store.ensure_initialized()
            index = store.events_dir / "lifecycle_events.json"
            index.write_text("{broken", encoding="utf-8")
            before = self.tree_snapshot(store.state_dir.parent)
            argv = [str(LIFECYCLE_SCRIPT), "--state-dir", str(store.state_dir), "audit-status"]
            with patch.object(sys, "argv", argv), redirect_stdout(io.StringIO()):
                self.assertNotEqual(module.main(), 0)
            self.assertEqual(self.tree_snapshot(store.state_dir.parent), before)
            self.assertEqual(index.read_text(encoding="utf-8"), "{broken")

    def test_cross_generation_validation_detects_missing_receipt_and_cycle(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = self.make_store(tmp, inventory())
            with store.lock():
                store.ensure_initialized()
                archived = store.transition("dev_client", ARCHIVED, "archive", "tester")
            manifest_path = archived["root"] / "manifest.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["transition_receipts"] = []
            operation = {key: value for key, value in manifest["operation_receipt"].items() if key != "transition_hash"}
            manifest["operation_receipt"]["transition_hash"] = hashlib.sha256(json.dumps(
                {"operation": operation, "transitions": []}, sort_keys=True, separators=(",", ":")
            ).encode()).hexdigest()
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaises(LifecycleValidationError):
                store.validate_generation_chain(archived["id"])

        with tempfile.TemporaryDirectory() as tmp:
            store = self.make_store(tmp, inventory())
            with store.lock():
                generation = store.ensure_initialized()
            manifest_path = generation["root"] / "manifest.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["previous_generation_id"] = generation["id"]
            manifest["operation_receipt"]["previous_generation_id"] = generation["id"]
            operation = {key: value for key, value in manifest["operation_receipt"].items() if key != "transition_hash"}
            manifest["operation_receipt"]["transition_hash"] = hashlib.sha256(json.dumps(
                {"operation": operation, "transitions": manifest["transition_receipts"]},
                sort_keys=True, separators=(",", ":")
            ).encode()).hexdigest()
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaisesRegex(LifecycleValidationError, "cycle"):
                store.validate_generation_chain(generation["id"])

        with tempfile.TemporaryDirectory() as tmp:
            store = self.make_store(tmp, inventory())
            with store.lock():
                generation = store.ensure_initialized()
            manifest_path = generation["root"] / "manifest.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["previous_generation_id"] = "gen_missing"
            manifest["operation_receipt"]["previous_generation_id"] = "gen_missing"
            operation = {key: value for key, value in manifest["operation_receipt"].items() if key != "transition_hash"}
            manifest["operation_receipt"]["transition_hash"] = hashlib.sha256(json.dumps(
                {"operation": operation, "transitions": manifest["transition_receipts"]},
                sort_keys=True, separators=(",", ":")
            ).encode()).hexdigest()
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaisesRegex(LifecycleValidationError, "missing previous generation"):
                store.validate_generation_chain(generation["id"])

    def test_committed_chain_rejects_duplicate_extra_and_mismatched_receipts(self):
        cases = {
            "duplicate": lambda receipt: [receipt, dict(receipt)],
            "extra": lambda receipt: [receipt, {**receipt, "device_id": "dev_unknown"}],
            "mismatched_previous": lambda receipt: [{**receipt, "previous_state": ARCHIVED}],
            "mismatched_generation": lambda receipt: [{**receipt, "generation_id": "gen_wrong"}],
        }
        for name, mutate in cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                store = self.make_store(tmp, inventory())
                with store.lock():
                    store.ensure_initialized()
                    generation = store.transition("dev_client", ARCHIVED, "archive", "tester")
                manifest_path = generation["root"] / "manifest.json"
                manifest = json.loads(manifest_path.read_text())
                manifest["transition_receipts"] = mutate(dict(manifest["transition_receipts"][0]))
                operation = {key: value for key, value in manifest["operation_receipt"].items() if key != "transition_hash"}
                manifest["operation_receipt"]["transition_hash"] = hashlib.sha256(json.dumps(
                    {"operation": operation, "transitions": manifest["transition_receipts"]},
                    sort_keys=True, separators=(",", ":")
                ).encode()).hexdigest()
                manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
                with self.assertRaises(LifecycleValidationError):
                    store.validate_generation_chain(generation["id"])

    def test_rollback_refuses_to_drop_new_stable_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = self.make_store(tmp, inventory())
            with store.lock():
                initial = store.ensure_initialized()
                expanded = inventory([device(), device("dev_second", mac="aa:bb:cc:dd:ee:02")])
                store.apply_discovery(expanded, set())
                with self.assertRaises(LifecycleValidationError):
                    store.rollback(initial["id"])

    def test_prune_is_dry_run_validation_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = self.make_store(tmp, inventory())
            with store.lock():
                initial = store.ensure_initialized()
                store.transition("dev_client", ARCHIVED, "archive", "tester")
                result = store.validate_prune(initial["id"])
            self.assertTrue(result["dry_run"])
            self.assertTrue(initial["root"].exists())

    def test_internal_lock_serializes_concurrent_writers(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = self.make_store(tmp, inventory())
            errors = []
            with store.lock():
                thread = threading.Thread(target=lambda: self._capture_lock_error(store, errors))
                thread.start()
                thread.join()
            self.assertTrue(errors)
            self.assertIsInstance(errors[0], LifecycleError)

    def test_delayed_failed_mqtt_does_not_hold_lifecycle_lock_or_rollback_commit(self):
        module = load_script("hioc_inventory_engine_lock", ENGINE_SCRIPT)
        entered_publish = threading.Event()
        release_publish = threading.Event()

        class DelayedFailingMqtt:
            def __init__(self, *_args, **_kwargs):
                pass

            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def publish(self, *_args):
                entered_publish.set()
                release_publish.wait(3)
                raise RuntimeError("delayed MQTT failure")

        with tempfile.TemporaryDirectory() as tmp:
            payload = inventory()
            payload["_capabilities"] = []
            payload["_positive_device_ids"] = []
            logger = logging.getLogger("test-inventory-lock-boundary")
            result = []
            with patch.object(module, "load_config", return_value={"HIOC_HOME": tmp}), \
                    patch.object(module, "discover_inventory", return_value=payload), \
                    patch.object(module, "MqttClient", DelayedFailingMqtt), \
                    patch.object(module, "setup_logger", return_value=logger):
                thread = threading.Thread(target=lambda: result.append(module.main()))
                thread.start()
                self.assertTrue(entered_publish.wait(3))
                state = Path(tmp) / "state" / "inventory"
                with LifecycleStore(state, lock_timeout=0.25).lock():
                    pass
                release_publish.set()
                thread.join(5)
            self.assertEqual(result, [0])
            committed = LifecycleStore(Path(tmp) / "state" / "inventory").open_existing_read_only()
            self.assertEqual(committed["inventory"]["devices"][0]["id"], "dev_client")
            status = json.loads((Path(tmp) / "state" / "inventory" / "status.json").read_text())
            self.assertEqual(status["status"], "degraded")

    @staticmethod
    def _capture_lock_error(store, errors):
        try:
            with store.lock():
                pass
        except Exception as exc:
            errors.append(exc)

    def test_partial_lifecycle_state_without_current_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = self.make_store(tmp, inventory())
            store.generations_dir.mkdir()
            (store.generations_dir / "orphan").mkdir()
            with store.lock(), self.assertRaises(LifecycleValidationError):
                store.ensure_initialized()

    def test_interrupted_precommit_transaction_is_quarantined(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = self.make_store(tmp, inventory())
            stale = store.transactions_dir / "gen_interrupted"
            stale.mkdir(parents=True)
            (stale / "manifest.json").write_text("{}")
            with store.lock():
                store.ensure_initialized()
            quarantine = store.transactions_dir / "quarantine"
            self.assertTrue(any(path.name.startswith("gen_interrupted") for path in quarantine.iterdir()))


if __name__ == "__main__":
    unittest.main()
