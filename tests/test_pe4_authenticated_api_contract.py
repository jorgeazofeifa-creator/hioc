import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTRACT = (ROOT / "docs" / "PE4_HOME_ASSISTANT_ACCESS_PRIVACY_CONTRACT.md").read_text(encoding="utf-8")
MASTER = (ROOT / "docs" / "HIOC_MASTER_PLAN.md").read_text(encoding="utf-8")


class PE4AuthenticatedAPIContractTests(unittest.TestCase):
    def require(self, *values):
        for value in values:
            self.assertIn(value, CONTRACT)

    def test_rest_contract(self):
        self.require("REST_THEN_WEBSOCKET_2A", "`GET`", "`/api/`", "Authorization: Bearer", "API running.", "HTTP 200")
        self.assertNotIn("/api/states", CONTRACT)

    def test_websocket_auth_only(self):
        self.require("/api/websocket", "`auth_required`", '"type":"auth"', "`auth_ok`", "`auth_invalid`", "Send no command")

    def test_no_registry_or_internal_fallback(self):
        self.require("NOT_SUPPORTED_BY_DOCUMENTED_REST", "NO_GENERAL_CAPABILITY_DISCOVERY_DOCUMENTED", "must not be silently elevated")
        self.require("`.storage`", "database")

    def test_bounds_and_no_continuation(self):
        self.require("5 seconds", "10 seconds", "20 seconds", "65,536 bytes", "two credential-bearing requests", "zero retries", "zero redirects")
        self.require("PE4_0B2B=NOT_STARTED", "no\npolling", "subscriptions")

    def test_credential_privacy_and_provenance(self):
        self.require("Python `getpass`", "only in process memory", "INSTANCE_REFERENCE_METHOD=OPERATOR_LOGICAL_LABEL", "`PI5_HA`")

    def test_terminal_only_and_repository_client(self):
        self.require("terminal-only", "creates no evidence directory", "repository-controlled client is required", "custom RFC6455 stack is rejected")

    def test_repository_client_is_implemented_but_not_executed(self):
        client = ROOT / "tools" / "hioc-pe4-ha-auth-capability.py"
        self.assertTrue(client.is_file())
        self.require("Repository-controlled 2a client", "has not been deployed or executed", "remains **NOT STARTED**")

    def test_client_dependency_enforces_receive_bound(self):
        source = (ROOT / "tools" / "hioc-pe4-ha-auth-capability.py").read_text(encoding="utf-8")
        self.assertIn("max_size=MAX_MESSAGE", source)
        self.assertIn('required = {"open_timeout", "close_timeout", "max_size", "proxy"}', source)
        self.assertNotIn("import websocket  #", source)
        self.assertNotIn("websocket_client_check", source)
        self.require("WEBSOCKET-CLIENT", "MESSAGE-BOUND ENFORCEMENT DEFECT",
                     "only approved path is `websockets`")

    def test_status_remains_not_started(self):
        self.assertIn("PE-4.0B.2a remains **NOT\nSTARTED**", MASTER)
        self.assertNotIn("PE-4.0B.2a is **COMPLETE", MASTER)


if __name__ == "__main__":
    unittest.main()
