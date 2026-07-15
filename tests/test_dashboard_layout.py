import hashlib
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_PATH = ROOT / "homeassistant" / "dashboards" / "hioc_dashboard_v2.yaml"

EXPECTED_VIEWS = [
    ("Executive", "hioc-v2-executive", "mdi:monitor-dashboard"),
    ("Operations", "hioc-v2-operations", "mdi:view-dashboard"),
    ("Diagnostics", "hioc-v2-diagnostics", "mdi:stethoscope"),
    ("Inventory", "hioc-v2-inventory", "mdi:devices"),
    ("Network", "hioc-v2-network", "mdi:web-check"),
    ("Servers", "hioc-v2-servers", "mdi:server"),
]

EXPECTED_TOP_LEVEL_CARDS = {
    "Executive": [
        "Mission Status",
        "Current Incident",
        "Affected Systems",
        "Domain Health",
        "Top Risks",
        "Latest Events",
        "Data Freshness",
    ],
    "Operations": [
        "Live Operational State",
        "Incident",
        "Inventory",
        "Internet",
        "DNS",
        "MQTT",
        "Pi4",
        "Forecast",
        "Platform",
    ],
    "Diagnostics": [
        "Incident Mission Control",
        "Recommended Action",
        "Evidence",
        "Dependency Path",
        "Timeline",
        "Latest Incident Review",
        "Live Telemetry",
        "Engine State",
    ],
    "Inventory": [
        "Inventory Summary",
        "Counts",
        "Watch Devices",
        "Inventory Explorer - Devices",
        "Inventory Explorer - Services",
    ],
    "Network": ["Network Health", "DNS Investigation", "MQTT Path", "Network Evidence"],
    "Servers": ["Pi4 Health", "Pi4 Evidence", "HIOC Engines"],
}

# Canonical structural snapshot of the operator-supplied layout with the
# approved Watch Devices card inserted in the Inventory view.
EXPECTED_LAYOUT_SHA256 = "8ec117fb6928c9bd0348d74103f6633771d1d4aa41f675335dd38b9fdcea9622"


def _card_outline(card):
    result = {
        key: card[key]
        for key in (
            "type",
            "title",
            "navigation_path",
            "view_layout",
            "columns",
            "square",
            "conditions",
        )
        if key in card
    }
    tap_action = card.get("tap_action")
    if isinstance(tap_action, dict):
        result["tap_action"] = {
            key: tap_action[key]
            for key in ("action", "navigation_path")
            if key in tap_action
        }
    if "grid_options" in card:
        result["grid_options"] = card["grid_options"]
    if isinstance(card.get("card"), dict):
        result["card"] = _card_outline(card["card"])
    if "cards" in card:
        result["cards"] = [_card_outline(child) for child in card["cards"]]
    return result


def _layout_outline(dashboard):
    result = {"title": dashboard.get("title"), "views": []}
    for view in dashboard.get("views", []):
        view_result = {
            key: view[key]
            for key in ("title", "path", "icon", "type", "max_columns", "theme", "cards")
            if key in view
        }
        view_result["sections"] = []
        for section in view.get("sections", []):
            section_result = {
                key: section[key]
                for key in ("type", "title", "column_span")
                if key in section
            }
            section_result["cards"] = [
                _card_outline(card) for card in section.get("cards", [])
            ]
            view_result["sections"].append(section_result)
        result["views"].append(view_result)
    return result


class DashboardLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            import yaml
        except ImportError as exc:
            raise unittest.SkipTest("PyYAML is not available in this Python runtime") from exc
        cls.raw = DASHBOARD_PATH.read_text(encoding="utf-8")
        cls.dashboard = yaml.safe_load(cls.raw)

    def test_view_order_paths_icons_columns_and_sections(self):
        actual = [
            (view["title"], view["path"], view["icon"])
            for view in self.dashboard["views"]
        ]
        self.assertEqual(actual, EXPECTED_VIEWS)
        for view in self.dashboard["views"]:
            self.assertEqual(view["type"], "sections")
            self.assertEqual(view["max_columns"], 4)
            self.assertEqual(view["theme"], "HIOC Operations")
            self.assertEqual(view["cards"], [])
            self.assertEqual(len(view["sections"]), 1)
            self.assertEqual(view["sections"][0]["column_span"], 4)
            self.assertEqual(
                [card.get("title") for card in view["sections"][0]["cards"]],
                EXPECTED_TOP_LEVEL_CARDS[view["title"]],
            )

    def test_complete_nested_layout_snapshot(self):
        canonical = json.dumps(
            _layout_outline(self.dashboard),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        self.assertEqual(hashlib.sha256(canonical).hexdigest(), EXPECTED_LAYOUT_SHA256)

    def test_operator_card_dimensions_are_preserved(self):
        heights = re.findall(r"min-height:\s*(\d+px)", self.raw)
        self.assertEqual(
            heights,
            [
                "315px", "315px", "280px",
                *("155px" for _ in range(7)),
                "265px", "265px", "150px",
                *("180px" for _ in range(8)),
                "310px", "310px", "250px", "250px", "210px", "310px",
                "260px", "260px", "230px", "300px", "300px", "500px", "500px",
                "260px", "260px", "260px", "210px", "330px", "330px", "330px",
            ],
        )


if __name__ == "__main__":
    unittest.main()
