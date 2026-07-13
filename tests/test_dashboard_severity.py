import json
import re
import unittest
from pathlib import Path


DASHBOARD_PATH = (
    Path(__file__).resolve().parents[1]
    / "homeassistant"
    / "dashboards"
    / "hioc_dashboard_v2.yaml"
)

AFFECTED_CARDS = {
    ("Executive", "Mission Status"): 5,
    ("Executive", "Current Incident"): 4,
    ("Executive", "Affected Systems"): 4,
    ("Executive", "Incident"): None,
    ("Executive", "Active Incident"): None,
    ("Operations", "Live Operational State"): 12,
    ("Operations", "Incident"): 3,
    ("Diagnostics", "Incident Mission Control"): 7,
    ("Diagnostics", "Recommended Action"): 5,
    ("Diagnostics", "Evidence"): 6,
}

EXPECTED_VIEWS = {
    "Executive": ("hioc-v2-executive", "sections", 4),
    "Operations": ("hioc-v2-operations", "sections", 4),
    "Diagnostics": ("hioc-v2-diagnostics", "sections", 4),
    "Inventory": ("hioc-v2-inventory", "sections", 4),
    "Network": ("hioc-v2-network", "sections", 4),
    "Servers": ("hioc-v2-servers", "sections", 4),
}

EXPECTED_NAVIGATION_PATHS = {
    ("Executive", "Mission Status"): "/lovelace/hioc-v2-diagnostics",
    ("Executive", "Current Incident"): "/lovelace/hioc-v2-diagnostics",
    ("Executive", "Affected Systems"): "/lovelace/hioc-v2-diagnostics",
    ("Executive", "Incident"): "/lovelace/hioc-v2-diagnostics",
    ("Executive", "Active Incident"): "/lovelace/hioc-v2-diagnostics",
    ("Operations", "Live Operational State"): None,
    ("Operations", "Incident"): "/lovelace/hioc-v2-diagnostics",
    ("Diagnostics", "Incident Mission Control"): None,
    ("Diagnostics", "Recommended Action"): None,
    ("Diagnostics", "Evidence"): None,
}

EXPECTED_ENTITY_IDS = {
    "sensor.hioc_core_version",
    "sensor.hioc_correlation_engine_version",
    "sensor.hioc_dashboard_version",
    "sensor.hioc_engine_status",
    "sensor.hioc_forecast_dns_trend",
    "sensor.hioc_forecast_internet_24h_average_latency",
    "sensor.hioc_forecast_internet_latency_trend",
    "sensor.hioc_forecast_mqtt_trend",
    "sensor.hioc_forecast_packet_loss_trend",
    "sensor.hioc_forecast_pi4_days_to_90_percent_disk",
    "sensor.hioc_forecast_pi4_disk_growth",
    "sensor.hioc_forecast_pi4_memory_trend",
    "sensor.hioc_forecast_pi4_temperature_trend",
    "sensor.hioc_history_engine_status",
    "sensor.hioc_incident_active",
    "sensor.hioc_incident_history_count",
    "sensor.hioc_incident_reason",
    "sensor.hioc_incident_recommendation",
    "sensor.hioc_incident_severity",
    "sensor.hioc_incident_started",
    "sensor.hioc_incident_status",
    "sensor.hioc_incident_summary",
    "sensor.hioc_incident_system",
    "sensor.hioc_incident_updated",
    "sensor.hioc_inventory_degraded_devices",
    "sensor.hioc_inventory_dependency_edges",
    "sensor.hioc_inventory_device_count",
    "sensor.hioc_inventory_devices",
    "sensor.hioc_inventory_healthy_devices",
    "sensor.hioc_inventory_offline_devices",
    "sensor.hioc_inventory_operations_summary",
    "sensor.hioc_inventory_service_count",
    "sensor.hioc_inventory_services",
    "sensor.hioc_inventory_status",
    "sensor.hioc_inventory_topology_edges",
    "sensor.hioc_inventory_watch_devices",
    "sensor.hioc_latest_timeline_event",
    "sensor.hioc_mqtt_api_version",
    "sensor.hioc_platform_status",
    "sensor.hioc_platform_version",
    "sensor.hioc_schema_version",
    "sensor.hioc_statistics_samples_host",
    "sensor.hioc_statistics_samples_network",
}


def _find_titled_cards(node, title):
    matches = []
    if isinstance(node, dict):
        if node.get("title") == title:
            matches.append(node)
        for value in node.values():
            matches.extend(_find_titled_cards(value, title))
    elif isinstance(node, list):
        for value in node:
            matches.extend(_find_titled_cards(value, title))
    return matches


def _string_values(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for value in node.values():
            yield from _string_values(value)
    elif isinstance(node, list):
        for value in node:
            yield from _string_values(value)


class DashboardSeverityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            import yaml
        except ImportError as exc:
            raise unittest.SkipTest("PyYAML is not available in this Python runtime") from exc

        cls.raw = DASHBOARD_PATH.read_text(encoding="utf-8")
        cls.dashboard = yaml.safe_load(cls.raw)
        cls.views = {view["title"]: view for view in cls.dashboard["views"]}
        cls.cards = {}
        for key in AFFECTED_CARDS:
            page, title = key
            matches = _find_titled_cards(cls.views[page], title)
            if len(matches) != 1:
                raise AssertionError(
                    f"expected one {page} / {title} card, found {len(matches)}"
                )
            cls.cards[key] = matches[0]

    def test_all_ten_cards_use_status_and_severity_mapping(self):
        self.assertEqual(10, len(self.cards))
        for key, card in self.cards.items():
            with self.subTest(card=key):
                template = json.dumps(card, sort_keys=True)
                self.assertIn("sensor.hioc_incident_status", template)
                self.assertIn("sensor.hioc_incident_severity", template)
                self.assertIn(
                    "states('sensor.hioc_incident_status') | lower | trim",
                    template,
                )
                self.assertIn(
                    "states('sensor.hioc_incident_severity') | lower | trim",
                    template,
                )
                for severity in ("warning", "major", "critical"):
                    self.assertIn(severity, template)
                self.assertIn("#64748b", template)

    def test_severity_accents_are_status_gated(self):
        for key, card in self.cards.items():
            with self.subTest(card=key):
                strings = list(_string_values(card))
                styles = [value for value in strings if "border-left:" in value]
                self.assertTrue(styles)
                for style in styles:
                    self.assertIn("incident == 'active' and severity == 'warning'", style)
                    self.assertIn("#f59e0b", style)
                    self.assertIn("incident == 'active' and severity == 'major'", style)
                    self.assertIn("var(--deep-orange-color)", style)
                    self.assertIn("incident == 'active' and severity == 'critical'", style)
                    self.assertIn("#ef4444", style)
                    self.assertIn("#64748b", style)

    def test_status_only_active_cannot_render_critical_or_red(self):
        status_only_critical = re.compile(
            r"(?:is_state\([^)]*hioc_incident_status[^)]*active[^)]*\)|"
            r"incident\s*==\s*['\"]active['\"])(?:(?!severity).){0,200}"
            r"#\s*Critical",
            re.IGNORECASE | re.DOTALL,
        )
        status_only_red = re.compile(
            r"(?:is_state\([^)]*hioc_incident_status[^)]*active[^)]*\)|"
            r"incident\s*==\s*['\"]active['\"])(?:(?!severity).){0,200}"
            r"#ef4444",
            re.IGNORECASE | re.DOTALL,
        )
        self.assertIsNone(status_only_critical.search(self.raw))
        self.assertIsNone(status_only_red.search(self.raw))
        for key, card in self.cards.items():
            with self.subTest(card=key):
                template = json.dumps(card, sort_keys=True)
                self.assertIsNone(status_only_critical.search(template))
                self.assertIsNone(status_only_red.search(template))

    def test_content_severity_is_normalized_and_status_gated(self):
        direct_mapping_cards = {
            ("Executive", "Mission Status"),
            ("Executive", "Incident"),
            ("Operations", "Live Operational State"),
            ("Operations", "Incident"),
            ("Diagnostics", "Recommended Action"),
        }
        severity_label_cards = {
            ("Executive", "Current Incident"),
            ("Executive", "Active Incident"),
            ("Diagnostics", "Incident Mission Control"),
        }

        for key in direct_mapping_cards:
            with self.subTest(card=key):
                content = self.cards[key]["content"]
                self.assertIn("incident == 'active'", content)
                for severity in ("warning", "major", "critical"):
                    self.assertIn(f"severity == '{severity}'", content)
                self.assertIn("Unknown", content)

        for key in severity_label_cards:
            with self.subTest(card=key):
                content = self.cards[key]["content"]
                self.assertIn("incident == 'active'", content)
                self.assertIn(
                    "severity in ['warning', 'major', 'critical'] else 'Unknown'",
                    content,
                )

        for key in {
            ("Executive", "Affected Systems"),
            ("Diagnostics", "Evidence"),
        }:
            with self.subTest(card=key):
                content = self.cards[key]["content"]
                self.assertNotIn("# Critical", content)
                self.assertNotIn("Severity:", content)

    def test_none_and_resolved_ignore_stale_critical_severity(self):
        for key, card in self.cards.items():
            with self.subTest(card=key):
                strings = list(_string_values(card))
                for style in (value for value in strings if "#ef4444" in value):
                    self.assertIn(
                        "incident == 'active' and severity == 'critical'", style
                    )

                if key != ("Executive", "Active Incident"):
                    template = json.dumps(card, sort_keys=True)
                    self.assertIn("none", template)
                    self.assertIn("resolved", template)

        # The Top Risks card remains hidden by its existing status-only condition.
        executive = self.views["Executive"]
        active_risk_conditions = [
            node
            for node in _find_titled_cards(executive, "Top Risks")[0]["cards"]
            if node.get("card", {}).get("title") == "Active Incident"
        ][0]["conditions"]
        self.assertEqual(
            [{"entity": "sensor.hioc_incident_status", "state": "active"}],
            active_risk_conditions,
        )

    def test_dashboard_entity_ids_are_unchanged(self):
        entity_ids = set(re.findall(r"sensor\.hioc_[a-z0-9_]+", self.raw))
        self.assertEqual(EXPECTED_ENTITY_IDS, entity_ids)

    def test_view_layouts_card_titles_and_grid_widths_are_unchanged(self):
        actual_views = {
            title: (view["path"], view["type"], view["max_columns"])
            for title, view in self.views.items()
        }
        self.assertEqual(EXPECTED_VIEWS, actual_views)

        for key, expected_columns in AFFECTED_CARDS.items():
            with self.subTest(card=key):
                card = self.cards[key]
                self.assertEqual(key[1], card["title"])
                self.assertEqual(
                    EXPECTED_NAVIGATION_PATHS[key],
                    card.get("tap_action", {}).get("navigation_path"),
                )
                if expected_columns is not None:
                    self.assertEqual(expected_columns, card["grid_options"]["columns"])


if __name__ == "__main__":
    unittest.main()
