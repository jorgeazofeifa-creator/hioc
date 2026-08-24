import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs" / "PE4_HOME_ASSISTANT_ACCESS_PRIVACY_CONTRACT.md"
MASTER = ROOT / "docs" / "HIOC_MASTER_PLAN.md"


class PE4AccessPrivacyContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = CONTRACT.read_text(encoding="utf-8")
        cls.master = MASTER.read_text(encoding="utf-8")

    def require(self, *values):
        for value in values:
            self.assertIn(value, self.contract)

    def test_status_and_supported_interface_gate(self):
        self.assertIn("PE-4.0A is **COMPLETE in repository governance**", self.master)
        self.assertIn("PE-4.0B live/schema discovery", self.master)
        self.require("SUPPORTED FOR 2a ROOT ONLY", "UNSUPPORTED_INTERFACE", "must not fall back to internals")

    def test_read_only_and_mutation_prohibitions(self):
        self.require(
            "Home Assistant service calls",
            "registry writes",
            "token creation/deletion",
            "database mutation",
            "`.storage` mutation",
            "restart/reboot",
            "integration reload",
            "HIOC inventory/Asset/manufacturer/incident mutation",
        )

    def test_identity_and_asset_authority_are_protected(self):
        self.require(
            "HIOC remains authoritative for stable device ID, MAC identity, and canonical IP",
            "Operator-managed Asset knowledge remains the highest",
            "authority for descriptive fields",
            "cannot overwrite an Asset field",
            "REJECT AS INDEPENDENT IDENTITY",
        )

    def test_sensitive_values_are_excluded(self):
        self.require(
            "raw MAC or IP addresses",
            "entity IDs",
            "unique IDs",
            "device/area/room/person/user names",
            "secrets, tokens, credentials",
            "Raw data never enters Git",
        )

    def test_mac_and_live_state_boundaries(self):
        self.require(
            "without printing a MAC",
            "raw MACs do not\nenter discovery evidence",
            "Live entity state and availability are discarded",
            "no PE-4 identity",
        )

    def test_bounded_private_evidence(self):
        self.require(
            "one bounded invocation",
            "no\npolling loop",
            "invocation-owned private directory",
            "rejects symlinks",
            "result-last publication",
            "contains no raw registry record",
        )

    def test_fail_closed_contract(self):
        self.require(
            "UNEXPECTED_SCHEMA",
            "PRIVACY_CONTRACT_VIOLATION",
            "DISCOVERY_OUTPUT_UNSAFE",
            "EVIDENCE_PUBLICATION_FAILED",
            "Every failure emits a bounded\nsanitized result when safe, stops",
            "automatic rollback",
        )

    def test_credentials_are_not_invented_or_persisted(self):
        self.require(
            "never committed, echoed, logged, printed",
            "operator-provided HA access/bearer token",
            "Token generation remains outside",
            "non-command-line invocation method",
        )


if __name__ == "__main__":
    unittest.main()
