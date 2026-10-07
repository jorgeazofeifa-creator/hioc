"""Durable compatibility roadmap commitments; no runtime/host execution."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MASTER = (ROOT / "docs/HIOC_MASTER_PLAN.md").read_text(encoding="utf-8")


def section(start, end):
    return MASTER.split(start, 1)[1].split(end, 1)[0]


class CompatibilityMasterPlanGovernanceTests(unittest.TestCase):
    def test_permanent_principles_and_states(self):
        text = section("## 10. Compatibility Resilience", "# Architecture")
        for anchor in ("Accept compatible external evolution", "Preserve intentional HIOC-controlled and security identities", "Standard Compatibility States", "COMPATIBLE", "COMPATIBLE_UPDATED", "COMPATIBILITY_UNKNOWN", "COMPATIBILITY_DEGRADED", "INCOMPATIBLE", "TRUST_ANCHOR_CHANGED", "DEPENDENCY_UNAVAILABLE", "Update Causality and Last-Known-Compatible History", "Subsystem Failure Isolation", "Dependency Classification"):
            with self.subTest(anchor=anchor): self.assertIn(anchor, text)
    def test_central_contracts_and_future_ux(self):
        for anchor in ("state/platform/compatibility.json", "<HIOC_BASE_TOPIC>/platform/compatibility", "### Compatibility Diagnostics UX", "#### Persistent Home Assistant Notifications", "#### Phone-Notification Integration", "existing planned phone-notification", "#### User-Visible Diagnostic Semantics", "COMPATIBILITY_RESILIENCE.md"):
            with self.subTest(anchor=anchor): self.assertIn(anchor, MASTER)
    def test_current_lifecycle_and_sequence(self):
        text = section("# Implementation Status", "# Historical Operator Preparation Chronology")
        for anchor in ("Authoritative Current PE-4 Lifecycle", "PE-4.0B.2a", "First PE-4.0B.2b live execution", "Corrected PE-4.0B.2b execution", "PE-4.0C", "Phase 7A", "Rollback", "PASS/CLOSED", "ATTEMPTED / NOT COMPLETE", "NOT STARTED", "ACTIVE", "NOT PERFORMED", "PE-4.0C Association Contract Freeze"):
            with self.subTest(anchor=anchor): self.assertIn(anchor, text)
        for obsolete in ("2a is not prepared", "repeat separate successor preparation", "no PE-3 dataset is deployed"):
            self.assertNotIn(obsolete, text)
        next_task = text.split("## Next Planned Task", 1)[1]
        self.assertTrue(next_task.strip().startswith("### PE-4 Home Assistant Association Adapter Scheduler Deployment"))
    def test_development_and_operations_acceptance(self):
        self.assertIn("External Dependency Compatibility Review", section("# Working Agreement", "# Implementation Status"))
        self.assertIn("Operational Dependency Compatibility Acceptance", section("## Operations Acceptance Standard", "# Working Agreement"))
    def test_history_and_other_roadmap_anchors(self):
        for anchor in ("/tmp/hioc-pe4-ha-discovery-22be880b", "efd3aa0cc2f5bc00a459a0c05055ac14e5a9a7ab6cc13aeeb34aa9aa616cb087", "1e11b6e512db860a8f9b2b6af1723c6aabafd75968d7fd643c891144a7a72195", "authentication frame was not sent", "zero registry commands were sent", "DHCP Service Health & Capacity Monitoring", "Expected Availability & Permanent IoT Monitoring", "Asset-Centric Evolution", "Automatic service relationships", "Failure propagation visualization", "Historical infrastructure trends", "Predictive recommendations", "Infrastructure Backup, Disaster Recovery, and Hardware Migration", "Incident-history validator hardening"):
            with self.subTest(anchor=anchor): self.assertIn(anchor, MASTER)


if __name__ == "__main__":
    unittest.main()
