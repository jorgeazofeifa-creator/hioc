import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DASHBOARDS = (
    ROOT / "homeassistant" / "dashboards" / "living_inventory.yaml",
    ROOT / "homeassistant" / "dashboards" / "hioc_dashboard_v2.yaml",
)


class WatchDevicePresentationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            import yaml
        except ImportError:
            raise unittest.SkipTest("PyYAML is not available in this Python runtime")

        cls.cards = {}
        for path in DASHBOARDS:
            dashboard = yaml.safe_load(path.read_text(encoding="utf-8"))
            cards = [
                card
                for view in dashboard["views"]
                for section in view.get("sections", [])
                for card in section.get("cards", [])
            ]
            cls.cards[path.name] = next(card for card in cards if card.get("title") == "Watch Devices")

    def test_independently_scoped_watch_templates_remain_equivalent(self):
        contents = [card["content"] for card in self.cards.values()]
        self.assertEqual(contents[0], contents[1])

    @staticmethod
    def _watch_devices(devices):
        watch = sorted(
            (device for device in devices if device.get("health_status") == "watch"),
            key=lambda device: device.get("display_name", ""),
        )
        known_age = sorted(
            (device for device in watch if isinstance(device.get("observation_age_seconds"), (int, float))),
            key=lambda device: device["observation_age_seconds"],
            reverse=True,
        )
        unknown_age = [device for device in watch if not isinstance(device.get("observation_age_seconds"), (int, float))]
        return known_age + unknown_age

    @staticmethod
    def _age(age):
        if not isinstance(age, (int, float)):
            return "unknown"
        if age >= 86400:
            return f"{age // 86400:.0f}d {(age % 86400) // 3600:.0f}h"
        if age >= 3600:
            return f"{age // 3600:.0f}h {(age % 3600) // 60:.0f}m"
        if age >= 60:
            return f"{age // 60:.0f}m"
        return "<1m"

    def test_both_inventory_dashboards_use_authoritative_device_attributes(self):
        required = (
            "state_attr('sensor.hioc_inventory_devices', 'devices')",
            "selectattr('health_status', 'equalto', 'watch')",
            "sort(attribute='display_name')",
            "sort(attribute='observation_age_seconds', reverse=true)",
            "display_name",
            "hostname",
            "ip",
            "mac",
            "observation_status",
            "observation_age_seconds",
            "sources",
            "health_reasons",
        )
        for name, card in self.cards.items():
            with self.subTest(dashboard=name):
                self.assertEqual(card["type"], "markdown")
                for fragment in required:
                    self.assertIn(fragment, card["content"])

    def test_zero_watch_devices_has_concise_empty_state(self):
        devices = [{"display_name": "Healthy", "health_status": "healthy"}]
        self.assertEqual(self._watch_devices(devices), [])
        for card in self.cards.values():
            self.assertIn("No watch devices", card["content"])

    def test_one_watch_device_exposes_all_requested_fields(self):
        device = {
            "display_name": "Phone",
            "hostname": "phone-one",
            "ip": "192.0.2.10",
            "mac": "aa:bb:cc:dd:ee:ff",
            "health_status": "watch",
            "observation_status": "stale",
            "observation_age_seconds": 3720,
            "sources": ["arp_table", "dhcp_leases"],
            "health_reasons": ["last seen is stale"],
        }
        self.assertEqual(self._watch_devices([device]), [device])
        self.assertEqual(self._age(device["observation_age_seconds"]), "1h 2m")

    def test_multiple_watch_devices_are_ordered_oldest_observation_first(self):
        devices = [
            {"display_name": "Newest", "health_status": "watch", "observation_age_seconds": 60},
            {"display_name": "Unknown", "health_status": "watch", "observation_age_seconds": None},
            {"display_name": "Oldest", "health_status": "watch", "observation_age_seconds": 90000},
            {"display_name": "Middle", "health_status": "watch", "observation_age_seconds": 3600},
        ]
        ordered = self._watch_devices(devices)
        self.assertEqual([device["display_name"] for device in ordered], ["Oldest", "Middle", "Newest", "Unknown"])
        self.assertEqual(self._age(ordered[0]["observation_age_seconds"]), "1d 1h")
        self.assertEqual(self._age(ordered[-1]["observation_age_seconds"]), "unknown")

    def test_equal_ages_have_stable_display_name_secondary_order(self):
        devices = [
            {"display_name": "Zulu", "health_status": "watch", "observation_age_seconds": 300},
            {"display_name": "Alpha", "health_status": "watch", "observation_age_seconds": 300},
        ]
        self.assertEqual(
            [device["display_name"] for device in self._watch_devices(devices)],
            ["Alpha", "Zulu"],
        )

    def test_malformed_optional_lists_render_unknown_instead_of_mapping_keys(self):
        for card in self.cards.values():
            content = card["content"]
            self.assertIn("sources is not mapping", content)
            self.assertIn("reasons is not mapping", content)
            self.assertIn("else %}Unknown{% endif %}", content)
            self.assertIn("age is not boolean", content)
            self.assertIn("device.get('ip') is string", content)
            self.assertIn("device.get('mac') is string", content)
            self.assertIn("device.get('observation_status') is string", content)

    def test_missing_hostname_is_optional(self):
        device = {"display_name": "Unnamed client", "health_status": "watch", "observation_age_seconds": 120}
        self.assertNotIn("hostname", device)
        self.assertEqual(self._watch_devices([device]), [device])
        for card in self.cards.values():
            self.assertIn("{% if device.get('hostname') is string and device.get('hostname') %}", card["content"])

    def test_mixed_health_inventory_only_presents_watch_devices(self):
        devices = [
            {"display_name": "Healthy", "health_status": "healthy", "observation_age_seconds": 10},
            {"display_name": "Watch", "health_status": "watch", "observation_age_seconds": 20},
            {"display_name": "Degraded", "health_status": "degraded", "observation_age_seconds": 30},
            {"display_name": "Offline", "health_status": "offline", "observation_age_seconds": 40},
        ]
        self.assertEqual([device["display_name"] for device in self._watch_devices(devices)], ["Watch"])


if __name__ == "__main__":
    unittest.main()
