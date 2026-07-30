import datetime as dt
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "homeassistant" / "dashboards" / "hioc_dashboard_v2.yaml"
FRESHNESS_SECONDS = 12 * 60
FUTURE_TOLERANCE_SECONDS = 2 * 60


def operational_health(raw, now):
    if raw in (None, "", "unknown", "unavailable"):
        return "Unknown"
    try:
        stamp = dt.datetime.strptime(raw, "%Y-%m-%d %H:%M:%S")
    except (TypeError, ValueError):
        return "Unknown"
    age = (now - stamp).total_seconds()
    if age < -FUTURE_TOLERANCE_SECONDS:
        return "Unknown"
    if age <= FRESHNESS_SECONDS:
        return "Healthy"
    return "Stale"


def forecast_health(trend):
    return "Watch" if trend == "rising" else "Favorable" if trend in {"stable", "falling"} else "Unknown"


class MqttDashboardHealthTests(unittest.TestCase):
    def test_operational_and_forecast_scenarios_are_independent(self):
        now = dt.datetime(2026, 7, 29, 22, 30, 0)
        fresh = "2026-07-29 22:25:00"
        stale = "2026-07-29 22:00:00"
        self.assertEqual((operational_health(fresh, now), forecast_health("stable")), ("Healthy", "Favorable"))
        self.assertEqual((operational_health(fresh, now), forecast_health("rising")), ("Healthy", "Watch"))
        self.assertEqual((operational_health(stale, now), forecast_health("stable")), ("Stale", "Favorable"))
        for raw in ("unknown", "unavailable", "not-a-time", "2026-07-29 23:00:00"):
            self.assertNotEqual(operational_health(raw, now), "Healthy")

    def test_dashboard_exposes_separate_truths_and_threshold(self):
        source = DASHBOARD.read_text(encoding="utf-8")
        self.assertIn("title: MQTT Operational Health", source)
        self.assertIn("title: MQTT Forecast Trend", source)
        self.assertIn("age <= 720", source)
        self.assertIn("age >= -120", source)
        self.assertIn("Historical failure count:", source)
        self.assertNotIn("Meaning: MQTT trend is not rising.", source)
        self.assertNotIn("MQTT forecast trend is not rising.", source)


if __name__ == "__main__":
    unittest.main()
