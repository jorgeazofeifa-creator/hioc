import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
MASTER = (ROOT / "docs" / "HIOC_MASTER_PLAN.md").read_text(encoding="utf-8")
CONTRACT = (ROOT / "docs" / "PE4_HOME_ASSISTANT_ACCESS_PRIVACY_CONTRACT.md").read_text(
    encoding="utf-8"
)
OPERATIONS = (ROOT / "docs" / "OPERATIONS.md").read_text(encoding="utf-8")
DECISIONS = (ROOT / "DECISIONS.md").read_text(encoding="utf-8")


class PE4PreflightGovernanceTests(unittest.TestCase):
    def test_current_checkpoint_status_is_exact(self):
        for value in (
            "PE-4.0B.1 is **COMPLETE / PASS**",
            "PE-4.0B.2, PE-4.0C, the association",
            "production deployment remain **NOT STARTED**",
            "PE-4 overall is not\ncomplete",
        ):
            self.assertIn(value, MASTER)

    def test_proven_target_and_endpoint_are_recorded(self):
        for value in (
            "`HA_TERMINAL_ADDON`",
            "interactive zsh",
            "Home Assistant OS\n18.1",
            "Core 2026.8.1",
            "Supervisor 2026.07.5",
            "`http://192.168.100.251:8123`",
            "TLS is not applicable",
            "secure non-echoing prompt",
            "no dedicated WebSocket\nclient was detected",
        ):
            self.assertIn(value, MASTER)

    def test_historical_failure_is_not_current_status(self):
        self.assertIn("`UNSUPPORTED_HA_DEPLOYMENT`", MASTER)
        self.assertIn("RECURSIVE/NONAUTHORITATIVE STATE", MASTER)
        self.assertIn("historical parser-contract failure evidence, not current status", OPERATIONS)

    def test_authenticated_discovery_has_two_stop_boundaries(self):
        for value in (
            "PE-4.0B.2a — authenticated API/capability proof",
            "PE-4.0B.2b — registry/schema discovery",
            "must not run\n   automatically after 2a",
            "Exact registry commands must not be guessed",
        ):
            self.assertIn(value, CONTRACT)

    def test_client_and_credential_decisions_fail_closed(self):
        for value in (
            "does\nnot prove that any Python WebSocket module is installed",
            "`getpass` from the controlling terminal",
            "only in\n   process memory",
            "install no package",
            "REST alone is not assumed sufficient",
        ):
            self.assertIn(value, CONTRACT)

    def test_privacy_evidence_and_authority_boundaries_remain_closed(self):
        for value in (
            "`/tmp/hioc-pe4-ha-discovery-XXXXXXXX`",
            "directory mode `0700`",
            "sanitized files\nmode `0600`",
            "result-last",
            "Raw responses stay memory-only",
            "no raw or\nredacted-raw dump",
        ):
            self.assertIn(value, CONTRACT)
        for value in (
            "No live-state identity authority",
            "`.storage` fallback",
            "database fallback",
            "adapter implementation",
            "production\nmutation",
        ):
            self.assertIn(value, OPERATIONS)

    def test_checkpoint_does_not_implement_or_authorize_discovery(self):
        self.assertIn("Neither 2a nor 2b is implemented or authorized", DECISIONS)
        self.assertNotIn("PE-4.0B.2 is COMPLETE", MASTER)


if __name__ == "__main__":
    unittest.main()
