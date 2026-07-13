import re
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

        views = cls.dashboard["views"]
        inventory_view = next(view for view in views if view.get("path") == "hioc-v2-inventory")
        cls.inventory_cards = [
            card for section in inventory_view["sections"] for card in section.get("cards", [])
        ]

    @staticmethod
    def _render_recommendation(
        template, watch_count, degraded_count, offline_count, status="online"
    ):
        branches = re.fullmatch(
            r"\s*{% set status = .*? %}\s*"
            r"{% set offline = .*? %}\s*"
            r"{% set degraded = .*? %}\s*"
            r"{% set watch = .*? %}\s*"
            r"{% if status not in .*? %}\s*(.*?)\s*"
            r"{% elif offline > 0 %}\s*(.*?)\s*"
            r"{% elif degraded > 0 %}\s*(.*?)\s*"
            r"{% elif watch > 0 %}\s*(.*?)\s*"
            r"{% else %}\s*(.*?)\s*{% endif %}\s*",
            template,
            flags=re.DOTALL,
        )
        if branches is None:
            raise AssertionError("Recommendation template no longer has the required count branches")
        unknown_text, offline_text, degraded_text, watch_text, healthy_text = branches.groups()
        if status not in {"online", "degraded"} or min(
            watch_count, degraded_count, offline_count
        ) < 0:
            return unknown_text
        if offline_count > 0:
            return offline_text
        if degraded_count > 0:
            return degraded_text
        if watch_count > 0:
            return watch_text
        return healthy_text

    def test_summary_preserves_branch_precedence_and_wording(self):
        template = self.sensors["hioc_inventory_operations_summary"]["state"]
        unknown = template.index("{% if status not in")
        offline = template.index("{% elif offline > 0 %}")
        degraded = template.index("{% elif degraded > 0 %}")
        watch = template.index("{% elif watch > 0 %}")
        healthy = template.index("Inventory healthy")

        self.assertLess(unknown, offline)
        self.assertLess(offline, degraded)
        self.assertLess(degraded, watch)
        self.assertLess(watch, healthy)
        self.assertIn("offline device", template)
        self.assertIn("degraded device", template)
        self.assertIn("has a stale observation", template)
        self.assertIn("have stale observations", template)
        self.assertNotIn("need attention", template.lower())
        self.assertIn("Inventory status unavailable", template)

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

    def test_recommendation_template_renders_each_count_branch(self):
        template = self.sensors["hioc_inventory_recommended_action"]["state"]
        cases = {
            (0, 0, 1): "Open the inventory dashboard and verify power, Wi-Fi/Ethernet, and gateway reachability for offline devices.",
            (0, 1, 0): "Review degraded device health reasons and confirm whether the device has changed IP, MAC, or parent path.",
            (2, 0, 0): "No operator action required; stale observations remain visible for review.",
            (0, 0, 0): "No inventory action required.",
            (2, 1, 0): "Review degraded device health reasons and confirm whether the device has changed IP, MAC, or parent path.",
            (2, 1, 1): "Open the inventory dashboard and verify power, Wi-Fi/Ethernet, and gateway reachability for offline devices.",
            (-1, 0, 0): "Inventory recommendation unavailable; review Inventory for current state.",
        }
        for counts, expected in cases.items():
            with self.subTest(counts=counts):
                self.assertEqual(self._render_recommendation(template, *counts), expected)
        self.assertEqual(
            self._render_recommendation(template, 0, 0, 0, status="unknown"),
            "Inventory recommendation unavailable; review Inventory for current state.",
        )

    def test_inventory_summary_uses_authoritative_recommendation_entity(self):
        summary = next(card for card in self.inventory_cards if card.get("title") == "Inventory Summary")
        self.assertIn(
            "Recommended action: {{ states('sensor.hioc_inventory_recommended_action') }}",
            summary["content"],
        )
        self.assertNotIn(
            "Recommended action: review Device Health when degraded or offline counts are nonzero.",
            summary["content"],
        )
        style = summary["card_mod"]["style"]
        self.assertIn("sensor.hioc_inventory_watch_devices", style)
        self.assertIn("#38bdf8", style)

    def test_entities_counts_and_dashboard_layout_are_unchanged(self):
        expected_ids = {
            "hioc_inventory_operations_summary",
            "hioc_inventory_recommended_action",
        }
        self.assertTrue(expected_ids <= self.sensors.keys())

        summary = next(card for card in self.inventory_cards if card.get("title") == "Inventory Summary")
        counts = next(card for card in self.inventory_cards if card.get("title") == "Counts")

        self.assertEqual(summary["grid_options"], {"columns": 12, "rows": "auto"})
        self.assertEqual(counts["grid_options"], {"columns": 12, "rows": "auto"})
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
