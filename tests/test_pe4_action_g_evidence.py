import json
import unittest
from pathlib import Path


class ActionGEvidenceTests(unittest.TestCase):
    def test_strict_schema_and_required_fields(self):
        schema = json.loads(Path("governance/pe4/action-g-result.schema.json").read_text(encoding="utf-8"))
        self.assertFalse(schema["additionalProperties"])
        required = set(schema["required"])
        for field in ("current_consumer", "f_transaction_id", "f_result_sha256", "f_committed_sha256",
                      "final_environment_identity", "active_identity", "client_sha256",
                      "credential_use", "network_connection_attempted", "result"):
            self.assertIn(field, required)

    def test_schema_is_versioned_for_g(self):
        schema = json.loads(Path("governance/pe4/action-g-result.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(schema["properties"]["record_type"]["const"], "ACTION_G_RESULT")
        self.assertEqual(schema["properties"]["schema_version"]["const"], "2.0")
