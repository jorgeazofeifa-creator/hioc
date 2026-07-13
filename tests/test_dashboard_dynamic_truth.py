import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDITED_PATHS = [
    ROOT / "homeassistant" / "dashboards" / "hioc_dashboard_v2.yaml",
    ROOT / "homeassistant" / "dashboards" / "living_inventory.yaml",
    ROOT / "homeassistant" / "dashboards" / "incident_command_card.yaml",
    ROOT / "homeassistant" / "dashboards" / "home_infrastructure_hioc_incident_center_v12.yaml",
    ROOT / "homeassistant" / "packages" / "hioc_living_inventory.yaml",
    ROOT / "homeassistant" / "packages" / "hioc_incident_center.yaml",
    ROOT / "homeassistant" / "packages" / "hioc_platform.yaml",
    ROOT / "homeassistant" / "packages" / "hioc_predictive_analytics.yaml",
]

OPERATIONAL_WORDS = re.compile(
    r"\b(?:healthy|operational|watch|warning|major|critical|degraded|offline|unknown|"
    r"recovered|affected|root cause|confidence|recommended action|service status|"
    r"platform status|active incident|no active incident|no action required|"
    r"need attention|investigate)\b",
    re.IGNORECASE,
)
IPV4 = re.compile(r"(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])")
MAC = re.compile(r"(?i)(?<![0-9a-f])(?:[0-9a-f]{2}[:-]){5}[0-9a-f]{2}(?![0-9a-f])")


def _walk_strings(node, path=(), conditional=False):
    if isinstance(node, dict):
        conditional = conditional or bool(node.get("conditions"))
        for key, value in node.items():
            yield from _walk_strings(value, path + (str(key),), conditional)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from _walk_strings(value, path + (str(index),), conditional)
    elif isinstance(node, str):
        yield path, node, conditional


class DashboardDynamicTruthTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            import yaml
        except ImportError as exc:
            raise unittest.SkipTest("PyYAML is not available in this Python runtime") from exc
        cls.raw = {path: path.read_text(encoding="utf-8") for path in AUDITED_PATHS}
        cls.yaml = {path: yaml.safe_load(text) for path, text in cls.raw.items()}

    def test_operational_conclusions_are_dynamic_or_conditionally_scoped(self):
        presentation_keys = {"content", "primary", "secondary", "state", "value_template"}
        failures = []
        for file_path, document in self.yaml.items():
            for path, value, conditional in _walk_strings(document):
                if not path or path[-1] not in presentation_keys:
                    continue
                if not OPERATIONAL_WORDS.search(value):
                    continue
                dynamic = "{{" in value or "{%" in value
                if not dynamic and not conditional:
                    failures.append(f"{file_path.name}:{'/'.join(path)}: {value!r}")
        self.assertEqual(failures, [], "Unconditional operational presentation text:\n" + "\n".join(failures))

    def test_known_hardcoded_truth_defects_do_not_recur(self):
        combined = "\n".join(self.raw.values())
        forbidden = (
            "Recommended action: review Device Health when degraded or offline counts are nonzero.",
            "Frigate stopped",
            "· Healthy",
            "need attention",
            "default('No action required')",
            'default("No action required")',
        )
        for literal in forbidden:
            with self.subTest(literal=literal):
                self.assertNotIn(literal.lower(), combined.lower())

    def test_missing_mqtt_operational_values_never_default_to_zero_or_all_clear(self):
        packages = [
            ROOT / "homeassistant" / "packages" / "hioc_living_inventory.yaml",
            ROOT / "homeassistant" / "packages" / "hioc_incident_center.yaml",
            ROOT / "homeassistant" / "packages" / "hioc_predictive_analytics.yaml",
            ROOT / "homeassistant" / "packages" / "hioc_platform.yaml",
        ]
        for path in packages:
            with self.subTest(path=path.name):
                text = self.raw[path]
                self.assertNotRegex(text, r"value_json[^\n]+default\(0(?:,\s*true)?\)")
                self.assertNotRegex(
                    text,
                    r"value_json[^\n]+default\('(?:none|info|normal|No action required)'",
                )
        inventory = self.raw[packages[0]]
        self.assertIn("Inventory status unavailable", inventory)
        self.assertIn("Inventory recommendation unavailable", inventory)

        combined = "\n".join(self.raw.values())
        self.assertNotRegex(combined, r"default\(0(?:,\s*true)?\)")
        self.assertNotRegex(combined, r"\|\s*(?:int|float)\((?:0|999)\)")

    def test_no_device_specific_addresses_are_operational_exceptions(self):
        for file_path, text in self.raw.items():
            with self.subTest(path=file_path.name):
                self.assertIsNone(IPV4.search(text))
                self.assertIsNone(MAC.search(text))
                self.assertNotRegex(
                    text,
                    r"(?i){%\s*(?:if|elif)[^%]*(?:ip|mac|hostname|device_name)\s*==",
                )

    def test_inventory_summary_delegates_recommendation_policy(self):
        dashboard = self.raw[AUDITED_PATHS[0]]
        parsed = self.yaml[AUDITED_PATHS[0]]
        inventory_view = next(
            view for view in parsed["views"] if view["path"] == "hioc-v2-inventory"
        )
        summary = next(
            card
            for section in inventory_view["sections"]
            for card in section["cards"]
            if card.get("title") == "Inventory Summary"
        )
        self.assertIn(
            "Recommended action: {{ states('sensor.hioc_inventory_recommended_action') }}",
            summary["content"],
        )
        self.assertNotIn("{% if offline", summary["content"])
        self.assertIn("sensor.hioc_inventory_recommended_action", dashboard)

    def test_forecast_health_conclusions_require_known_safe_trends(self):
        failures = []
        for file_path, document in self.yaml.items():
            for path, value, _ in _walk_strings(document):
                if "sensor.hioc_forecast_" not in value:
                    continue
                if not re.search(r"\b(?:Healthy|Operational|No Action Required)\b", value):
                    continue
                if "['stable', 'falling']" not in value and "forecast_known" not in value:
                    failures.append(f"{file_path.name}:{'/'.join(path)}")
        self.assertEqual(failures, [], "Forecast conclusions without a known-safe branch: " + repr(failures))

    def test_incident_unknowns_do_not_become_no_incident(self):
        package = self.raw[ROOT / "homeassistant" / "packages" / "hioc_incident_center.yaml"]
        command = self.raw[ROOT / "homeassistant" / "dashboards" / "incident_command_card.yaml"]
        self.assertIn("default('unknown', true)", package)
        self.assertIn("Incident state unavailable", package)
        self.assertIn("incident status is unavailable", command.lower())
        self.assertIn(
            "states('sensor.hioc_incident_status') in ['none', 'resolved']",
            command,
        )

    def test_legacy_dashboard_has_no_static_healthy_color_or_fixed_topology(self):
        legacy = self.raw[
            ROOT / "homeassistant" / "dashboards" / "home_infrastructure_hioc_incident_center_v12.yaml"
        ]
        self.assertNotRegex(legacy, r"(?m)^\s*(?:icon_color|color):\s*green\s*$")
        self.assertNotIn("v1.2.0", legacy)
        self.assertRegex(legacy, r"not\s+is_number\(score\)")
        self.assertIn("Status unknown", legacy)


if __name__ == "__main__":
    unittest.main()
