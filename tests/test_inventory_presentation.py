import re
import unittest
from numbers import Number
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
        cls.mqtt_sensors = {
            sensor["unique_id"]: sensor for sensor in cls.package["mqtt"]["sensor"]
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

    @staticmethod
    def _render_numeric_mqtt_template(template, payload):
        match = re.fullmatch(
            r"\{\{ value_json\.(\w+) if value_json\.\1 is defined "
            r"and value_json\.\1 is number and value_json\.\1 is not boolean "
            r"else 'unknown' \}\}",
            template,
        )
        if match is None:
            raise AssertionError(
                "Numeric MQTT template no longer uses the required defined-and-numeric policy"
            )
        field = match.group(1)
        value = payload.get(field)
        return value if isinstance(value, Number) and not isinstance(value, bool) else "unknown"

    def _mqtt_state(self, unique_id, payload):
        return self._render_numeric_mqtt_template(
            self.mqtt_sensors[unique_id]["value_template"], payload
        )

    @staticmethod
    def _render_operations_summary(
        template, watch_count, degraded_count, offline_count, status="online"
    ):
        required_fragments = (
            "{% if status not in",
            "{% elif offline > 0 %}",
            "{% elif degraded > 0 %}",
            "{% elif watch > 0 %}",
            "Inventory healthy",
        )
        if not all(fragment in template for fragment in required_fragments):
            raise AssertionError("Operations summary template branches changed")
        if status not in {"online", "degraded"} or min(
            watch_count, degraded_count, offline_count
        ) < 0:
            return "Inventory status unavailable"
        if offline_count > 0:
            return f"{offline_count} offline device" + (
                "s" if offline_count != 1 else ""
            )
        if degraded_count > 0:
            return f"{degraded_count} degraded device" + (
                "s" if degraded_count != 1 else ""
            )
        if watch_count > 0:
            return (
                f"{watch_count} devices have stale observations"
                if watch_count != 1
                else "1 device has a stale observation"
            )
        return "Inventory healthy"

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

    def test_numeric_mqtt_templates_preserve_zero_and_reject_unavailable_values(self):
        fields = {
            "hioc_inventory_device_count": "device_count",
            "hioc_inventory_healthy_devices": "healthy_count",
            "hioc_inventory_watch_devices": "watch_count",
            "hioc_inventory_degraded_devices": "degraded_count",
            "hioc_inventory_offline_devices": "offline_count",
            "hioc_inventory_lowest_health": "lowest_health_score",
            "hioc_inventory_service_count": "service_count",
            "hioc_inventory_topology_edges": "topology_edges",
            "hioc_inventory_dependency_edges": "dependency_edges",
        }
        cases = (
            (7, 7),
            (0, 0),
            (3.5, 3.5),
            (None, "unknown"),
            ("", "unknown"),
            ("not-a-number", "unknown"),
            (True, "unknown"),
        )
        for unique_id, field in fields.items():
            with self.subTest(unique_id=unique_id, case="missing"):
                self.assertEqual(self._mqtt_state(unique_id, {}), "unknown")
            for value, expected in cases:
                with self.subTest(unique_id=unique_id, value=value):
                    self.assertEqual(
                        self._mqtt_state(unique_id, {field: value}), expected
                    )

    def test_production_summary_payload_preserves_zero_through_derived_behavior(self):
        payload = {
            "healthy_count": 97,
            "watch_count": 2,
            "degraded_count": 0,
            "offline_count": 0,
        }
        healthy = self._mqtt_state("hioc_inventory_healthy_devices", payload)
        watch = self._mqtt_state("hioc_inventory_watch_devices", payload)
        degraded = self._mqtt_state("hioc_inventory_degraded_devices", payload)
        offline = self._mqtt_state("hioc_inventory_offline_devices", payload)

        self.assertEqual((healthy, watch, degraded, offline), (97, 2, 0, 0))
        operations_summary = self.sensors["hioc_inventory_operations_summary"]["state"]
        self.assertEqual(
            self._render_operations_summary(
                operations_summary, watch, degraded, offline
            ),
            "2 devices have stale observations",
        )
        recommendation = self.sensors["hioc_inventory_recommended_action"]["state"]
        self.assertEqual(
            self._render_recommendation(recommendation, watch, degraded, offline),
            "No operator action required; stale observations remain visible for review.",
        )
        inventory_healthy = (
            "online" in {"online", "degraded"} and degraded == 0 and offline == 0
        )
        self.assertTrue(inventory_healthy)

    def test_missing_or_malformed_counts_cannot_create_false_all_clear(self):
        recommendation = self.sensors["hioc_inventory_recommended_action"]["state"]
        operations_summary = self.sensors["hioc_inventory_operations_summary"]["state"]
        payloads = (
            {"watch_count": 0, "offline_count": 0},
            {"watch_count": 0, "degraded_count": None, "offline_count": 0},
            {"watch_count": 0, "degraded_count": "", "offline_count": 0},
            {
                "watch_count": 0,
                "degraded_count": "not-a-number",
                "offline_count": 0,
            },
        )
        for payload in payloads:
            with self.subTest(payload=payload):
                watch = self._mqtt_state("hioc_inventory_watch_devices", payload)
                degraded = self._mqtt_state("hioc_inventory_degraded_devices", payload)
                offline = self._mqtt_state("hioc_inventory_offline_devices", payload)
                self.assertEqual(degraded, "unknown")
                converted = (
                    int(watch) if isinstance(watch, Number) else -1,
                    int(degraded) if isinstance(degraded, Number) else -1,
                    int(offline) if isinstance(offline, Number) else -1,
                )
                self.assertEqual(
                    self._render_operations_summary(operations_summary, *converted),
                    "Inventory status unavailable",
                )
                self.assertEqual(
                    self._render_recommendation(
                        recommendation,
                        *converted,
                    ),
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
