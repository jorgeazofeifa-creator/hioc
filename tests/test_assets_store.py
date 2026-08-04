import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "pi4" / "lib"))
from hioc.assets import (AssetLock, AssetLockTimeout, AssetRestoreError,
                         AssetRevisionConflict, AssetService, AssetStore,
                         AssetValidationError)

ID = "dev_0123456789abcdef"


class Clock:
    def __init__(self): self.n = 0
    def __call__(self, tz=None):
        self.n += 1
        return datetime(2026, 8, 3, 12, 0, 0, self.n, tzinfo=timezone.utc)


class AssetStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.home = Path(self.temp.name)
        self.store = AssetStore(self.home, Clock(), self.home / "asset.lock")
        self.service = AssetService(self.store)
        self.store.state_dir.mkdir(parents=True)
        (self.store.inventory_path).write_text(json.dumps({"devices": [{"id": ID}]}), encoding="utf-8")

    def tearDown(self): self.temp.cleanup()

    def test_initialize_create_update_noop_and_revision(self):
        self.assertEqual(self.service.initialize()["result"], "initialized")
        created = self.service.set_fields(ID, {"friendly_name": "Synthetic"})
        self.assertEqual(created["data"]["revision"], 1)
        before = self.store.store_path.read_bytes(); backups = list(self.store.backup_dir.iterdir())
        noop = self.service.set_fields(ID, {"friendly_name": "Synthetic"}, expected_revision=1)
        self.assertEqual(noop["result"], "no_change"); self.assertEqual(before, self.store.store_path.read_bytes())
        self.assertEqual(backups, list(self.store.backup_dir.iterdir()))
        updated = self.service.set_fields(ID, {"purpose": "Validation"}, expected_revision=1)
        self.assertEqual(updated["data"]["revision"], 2)

    def test_stale_revision_clear_and_remove(self):
        self.service.initialize(); self.service.set_fields(ID, {"friendly_name": "Synthetic", "purpose": "Test"})
        with self.assertRaises(AssetRevisionConflict): self.service.set_fields(ID, {"purpose": "New"}, expected_revision=9)
        clear = self.service.clear_field(ID, "purpose", 1); self.assertEqual(clear["data"]["revision"], 2)
        removed = self.service.clear_field(ID, "friendly_name", 2); self.assertEqual(removed["result"], "removed")

    def test_backups_exact_digest_and_restore(self):
        self.service.initialize(); self.service.set_fields(ID, {"friendly_name": "Synthetic"})
        original = self.store.store_path.read_bytes(); result = self.service.backup(); name = result["data"]["backup"]
        self.assertEqual((self.store.backup_dir / name).read_bytes(), original)
        self.service.set_fields(ID, {"purpose": "Changed"}, expected_revision=1)
        restored = self.service.restore(name); self.assertEqual(restored["result"], "restored")
        self.assertIsNone(self.store.load_store()["assets"][ID]["purpose"])

    def test_restore_rejects_paths_and_digest_mismatch(self):
        self.service.initialize()
        for value in ("../assets.json", str(self.store.store_path), "not-a-backup"):
            with self.assertRaises(AssetRestoreError): self.service.restore(value)
        name = self.service.backup()["data"]["backup"]
        (self.store.backup_dir / name).write_bytes(b"{}\n")
        with self.assertRaises(AssetRestoreError): self.service.restore(name)

    def test_atomic_replace_failure_preserves_store_and_temp_cleanup(self):
        self.service.initialize(); before = self.store.store_path.read_bytes()
        with mock.patch("hioc.assets.os.replace", side_effect=OSError("synthetic")):
            with self.assertRaises(Exception): self.service.set_fields(ID, {"friendly_name": "Synthetic"})
        self.assertEqual(before, self.store.store_path.read_bytes())
        self.assertEqual(list(self.store.state_dir.glob("*.tmp")), [])

    def test_nested_lock_rejected_and_released(self):
        with AssetLock(self.store.lock_path, False):
            with self.assertRaises(AssetLockTimeout):
                with AssetLock(self.store.lock_path, True): pass
        with AssetLock(self.store.lock_path, True): pass

    def test_malformed_store_is_not_repaired(self):
        self.store.store_path.write_text("{", encoding="utf-8")
        before = self.store.store_path.read_bytes()
        with self.assertRaises(AssetValidationError): self.service.set_fields(ID, {"friendly_name": "Synthetic"})
        self.assertEqual(before, self.store.store_path.read_bytes())


if __name__ == "__main__": unittest.main()
