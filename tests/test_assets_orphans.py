import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "pi4" / "lib"))
from hioc.assets import AssetService, AssetStore, AssetValidationError

ID = "dev_0123456789abcdef"


class AssetOrphanTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.home = Path(self.temp.name)
        self.store = AssetStore(self.home, lock_path=self.home / "lock"); self.service = AssetService(self.store)
        self.service.initialize()

    def tearDown(self): self.temp.cleanup()

    def test_missing_inventory_requires_allow_orphan(self):
        with self.assertRaises(AssetValidationError): self.service.set_fields(ID, {"friendly_name": "Synthetic"})
        result = self.service.set_fields(ID, {"friendly_name": "Synthetic"}, allow_orphan=True)
        self.assertEqual(result["status"], "degraded")

    def test_valid_inventory_orphan_count(self):
        self.service.set_fields(ID, {"friendly_name": "Synthetic"}, allow_orphan=True)
        self.store.inventory_path.write_text(json.dumps({"devices": []}), encoding="utf-8")
        result = self.service.list_assets()
        self.assertEqual(result["data"]["orphaned_asset_count"], 1)
        self.assertTrue(result["data"]["assets"][0]["orphaned"])

    def test_current_asset_and_malformed_inventory(self):
        self.store.inventory_path.parent.mkdir(parents=True, exist_ok=True)
        self.store.inventory_path.write_text(json.dumps({"devices": [{"id": ID}]}), encoding="utf-8")
        self.service.set_fields(ID, {"friendly_name": "Synthetic"})
        self.assertEqual(self.service.list_assets()["data"]["orphaned_asset_count"], 0)
        self.store.inventory_path.write_text("{", encoding="utf-8")
        result = self.service.list_assets(); self.assertEqual(result["data"]["inventory_context"], "invalid")
        self.assertIsNone(result["data"]["orphaned_asset_count"])
        self.assertEqual(self.service.set_fields(ID, {"purpose": "Still editable"}, expected_revision=1)["result"], "updated")

    def test_assets_never_modify_inventory(self):
        self.store.inventory_path.write_text(json.dumps({"devices": []}), encoding="utf-8")
        before = self.store.inventory_path.read_bytes()
        self.service.set_fields(ID, {"friendly_name": "Synthetic"}, allow_orphan=True)
        self.assertEqual(before, self.store.inventory_path.read_bytes())


if __name__ == "__main__": unittest.main()
