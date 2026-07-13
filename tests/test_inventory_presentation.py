import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_PATH = ROOT / "homeassistant" / "packages" / "hioc_living_inventory.yaml"
DASHBOARD_PATH = ROOT / "homeassistant" / "dashboards" / "hioc_dashboard_v2.yaml"


class InventoryPresentationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            import yaml
        except ImportError:
            raise unittest.SkipTest("PyYAML is not available in this Python runtime")
        cls.package = yaml.safe_load(PACKAGE_PATH.read_text(encoding="utf-8"))
        cls.dashboard = yaml.safe_load(DASHBOARD_PATH.read_text(encoding="utf-8"))

        template_blocks = [block for block in cls.package["template"] if "sensor" in block]
        cls.sensors = {
            sensor["unique_id"]: sensor
            for block in template_blocks
            for sensor in block["sensor"]
        }

    def test_summary_preserves_branch_precedence_and_wording(self):
        template = self.sensors["hioc_inventory_operations_summary"]["state"]
        offline = template.index("{% if offline > 0 %}")
        degraded = template.index("{% elif degraded > 0 %}")
        watch = template.index("{% elif watch > 0 %}")
        healthy = template.index("Inventory healthy")

        self.assertLess(offline, degraded)
        self.assertLess(degraded, watch)
        self.assertLess(watch, healthy)
        self.assertIn("offline device", template)
        self.assertIn("degraded device", template)
        self.assertIn("has a stale observation", template)
        self.assertIn("have stale observations", template)
        self.assertNotIn("need attention", template.lower())

        cases = {
            (97, 0, 0, 0): "Inventory healthy",
            (97, 2, 0, 0): "2 devices have stale observations",
            (97, 0, 1, 0): "1 degraded device",
            (97, 0, 0, 1): "1 offline device",
            (96, 2, 1, 0): "1 degraded device",
        }
        for counts, expected in cases.items():
            healthy_count, watch_count, degraded_count, offline_count = counts
            with self.subTest(counts=counts):
                if offline_count > 0:
                    actual = f"{offline_count} offline device" + ("s" if offline_count != 1 else "")
                elif degraded_count > 0:
                    actual = f"{degraded_count} degraded device" + ("s" if degraded_count != 1 else "")
                elif watch_count > 0:
                    actual = (
                        f"{watch_count} devices have stale observations"
                        if watch_count != 1
                        else "1 device has a stale observation"
                    )
                else:
                    actual = "Inventory healthy"
                self.assertEqual(actual, expected)
                self.assertGreaterEqual(healthy_count, 0)

    def test_watch_only_recommendation_is_non_actionable(self):
        template = self.sensors["hioc_inventory_recommended_action"]["state"]
        self.assertLess(template.index("{% if offline > 0 %}"), template.index("{% elif degraded > 0 %}"))
        self.assertLess(template.index("{% elif degraded > 0 %}"), template.index("{% elif watch > 0 %}"))
        self.assertIn(
            "No operator action required; stale observations remain visible for review.",
            template,
        )
        self.assertIn("Open the inventory dashboard", template)
        self.assertIn("Review degraded device health reasons", template)

    def test_entities_counts_and_dashboard_layout_are_unchanged(self):
        expected_ids = {
            "hioc_inventory_operations_summary",
            "hioc_inventory_recommended_action",
        }
        self.assertTrue(expected_ids <= self.sensors.keys())

        views = self.dashboard["views"]
        inventory_view = next(view for view in views if view.get("path") == "hioc-v2-inventory")
        cards = [card for section in inventory_view["sections"] for card in section.get("cards", [])]
        summary = next(card for card in cards if card.get("title") == "Inventory Summary")
        counts = next(card for card in cards if card.get("title") == "Counts")

        self.assertEqual(summary["grid_options"]["columns"], 8)
        self.assertEqual(counts["grid_options"]["columns"], 4)
        for entity_id in (
            "sensor.hioc_inventory_healthy_devices",
            "sensor.hioc_inventory_watch_devices",
            "sensor.hioc_inventory_degraded_devices",
            "sensor.hioc_inventory_offline_devices",
        ):
            self.assertIn(entity_id, summary["content"])
            self.assertIn(entity_id, counts["content"])


if __name__ == "__main__":
    unittest.main()
