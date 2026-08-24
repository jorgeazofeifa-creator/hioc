import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
RUNBOOK = ROOT / "docs" / "PE3_MANUFACTURER_PRODUCTION_RUNBOOK.md"
MASTER = ROOT / "docs" / "HIOC_MASTER_PLAN.md"
CONTRACT = ROOT / "docs" / "PE3_MANUFACTURER_EXECUTABLE_CONTRACT.md"
DOCUMENTS = (
    ROOT / "DECISIONS.md",
    ROOT / "docs" / "CHANGELOG.md",
    ROOT / "docs" / "DEPLOYMENT.md",
    MASTER,
    ROOT / "docs" / "OPERATIONS.md",
    CONTRACT,
    RUNBOOK,
    ROOT / "docs" / "RELEASE.md",
)


class PE3Action10GovernanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.runbook = RUNBOOK.read_text(encoding="utf-8")
        cls.action10 = cls.runbook.split(
            "## Action 10 — Administrative no-op closure", 1
        )[1].split("## Result taxonomy", 1)[0]
        cls.action10_flat = " ".join(cls.action10.split())

    def test_case_c_and_disposition_are_governed(self):
        for path in DOCUMENTS:
            text = path.read_text(encoding="utf-8")
            self.assertIn("NOOP_ALREADY_ABSENT", text, path)
        self.assertIn("CASE C — ACTION 10 ADMINISTRATIVE NO-OP CLOSURE", self.runbook)

    def test_no_pi3_action_or_evidence_input(self):
        for forbidden in (
            "```bash", "rm --", "rmdir --", "set -e", "set -u",
            "set -o pipefail", "set -euo pipefail", "jq ",
        ):
            self.assertNotIn(forbidden, self.action10)
        self.assertIn("are not Action 10 inputs", self.action10_flat)
        self.assertIn("No PI3 access", self.action10_flat)
        self.assertIn("Action 10 Evidence Report", self.action10_flat)

    def test_staging_is_non_authoritative_and_never_recreated(self):
        for value in (
            "installed immutable database/manifest plus active configuration",
            "No PI3 access", "deletion", "recreation", "retransmission",
        ):
            self.assertIn(value, self.action10_flat)
        self.assertNotIn("REMOVED_VALID_STAGING", self.action10)

    def test_completion_remains_repository_governed(self):
        self.assertIn("Action 10 remains **NOT COMPLETE**", self.action10)
        for value in ("committed", "pushed", "cleanly\nverified"):
            self.assertIn(value, self.action10)
        self.assertIn("separate repository-only completion record", self.action10)

    def test_active_ledger_has_no_stale_action9_or_deletion_contract(self):
        ledger = self.runbook.split("## Operator action ledger", 1)[1]
        self.assertIn("Invocation-owned evidence only", ledger)
        self.assertIn("administrative `NOOP_ALREADY_ABSENT` closure", ledger)
        for stale in (
            "no-op timing writes", "required threshold failure",
            "transfer cleanup PASS", "Exact temporary deletion",
        ):
            self.assertNotIn(stale, ledger)

    def test_no_action10_tool_exists(self):
        self.assertFalse(any((ROOT / "tools").glob("*action10*")))


if __name__ == "__main__":
    unittest.main()
