import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
MASTER = ROOT / "docs" / "HIOC_MASTER_PLAN.md"
ARCHITECTURE = ROOT / "docs" / "PASSIVE_ENRICHMENT_ARCHITECTURE.md"


class PE4GovernanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.master = MASTER.read_text(encoding="utf-8")
        cls.architecture = ARCHITECTURE.read_text(encoding="utf-8")

    def test_pe3_prerequisite_is_complete(self):
        self.assertIn("PE-3.0 through PE-3.3 and Actions 1–10 are complete", self.architecture)
        self.assertNotIn("Production deployment and PI3 validation\nremain pending", self.architecture)

    def test_pe4_is_planned_and_separately_gated(self):
        for value in (
            "PE-4.0B live/schema discovery",
            "PE-4 implementation remain **NOT STARTED**",
            "not a new identity engine",
            "separately gated",
        ):
            self.assertIn(value, self.master)

    def test_pe4_preserves_identity_and_availability_boundaries(self):
        for value in (
            "read-only Home Assistant",
            "HA names cannot replace operator fields",
            "availability is excluded",
            "Depends on PE-1/2 and access/schema approval",
        ):
            self.assertIn(value, self.architecture)


if __name__ == "__main__":
    unittest.main()
