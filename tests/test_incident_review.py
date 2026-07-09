import sys
import unittest
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "pi4" / "lib"))

from hioc.core.incident_review import (
    build_history_stats,
    build_incident_report,
    compact_recent_incidents,
    enrich_history,
    recent_incident_reviews,
)


class IncidentReviewTests(unittest.TestCase):
    def sample_incident(self):
        return {
            "id": "incident-1",
            "status": "resolved",
            "phase": "resolved",
            "title": "Internet degradation",
            "severity": "warning",
            "started": "2026-07-09T02:14:11-06:00",
            "resolved": "2026-07-09T02:20:43-06:00",
            "duration_seconds": 392,
            "root_cause": "ISP or upstream routing",
            "confidence_percent": 97,
            "affected": ["Internet", "DNS", "MQTT"],
            "impact": "Affected systems: Internet, DNS, MQTT",
            "evidence": ["Internet: Packet loss is 7%", "DNS: Local DNS latency is 340 ms"],
            "recommendation": "Compare external targets and ISP path.",
            "signals": [{"source": "telemetry", "system": "DNS"}],
        }

    def test_build_incident_report_contains_operator_fields(self):
        report = build_incident_report(self.sample_incident(), [
            {"timestamp": "2026-07-09T02:14:11-06:00", "message": "Internet latency exceeded threshold.", "incident_id": "incident-1"},
            {"timestamp": "2026-07-09T02:20:43-06:00", "message": "Incident resolved.", "incident_id": "incident-1"},
        ])

        self.assertEqual(report["title"], "Internet degradation")
        self.assertEqual(report["duration"], "6 minutes 32 seconds")
        self.assertEqual(report["recovery_type"], "automatic")
        self.assertIn("DNS", report["affected_services"])
        self.assertEqual(len(report["timeline"]), 4)

    def test_history_stats_are_derived_from_existing_records(self):
        history = enrich_history([self.sample_incident()], [])
        stats = build_history_stats(history, datetime.fromisoformat("2026-07-09T12:00:00-06:00"))

        self.assertEqual(stats["today"], 1)
        self.assertEqual(stats["last_7_days"], 1)
        self.assertEqual(stats["last_30_days"], 1)
        self.assertEqual(stats["automatic_recoveries"], 1)
        self.assertEqual(stats["manual_intervention_required"], 0)
        self.assertEqual(stats["average_duration"], "6 minutes 32 seconds")
        self.assertEqual(stats["longest_incident"], "6 minutes 32 seconds")

    def test_compact_recent_incidents_uses_reviews(self):
        history = enrich_history([self.sample_incident()], [])
        recent = compact_recent_incidents(history)

        self.assertEqual(recent[0]["title"], "Internet degradation")
        self.assertEqual(recent[0]["status"], "Resolved")
        self.assertEqual(recent[0]["duration"], "6 minutes 32 seconds")

    def test_recent_incident_reviews_include_full_review(self):
        history = enrich_history([self.sample_incident()], [])
        reviews = recent_incident_reviews(history)

        self.assertEqual(reviews[0]["incident_id"], "incident-1")
        self.assertIn("impact_summary", reviews[0])
        self.assertIn("recommended_action", reviews[0])


if __name__ == "__main__":
    unittest.main()
