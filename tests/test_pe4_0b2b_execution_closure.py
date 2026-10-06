"""Repository-only corrected discovery closure and immutable source bindings."""
import hashlib
import json
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "governance/pe4/pe4-0b2b-execution-closure.json"
EXPECTED = {'action_f_rerun': False,
 'action_g_rerun': False,
 'area_records': 22,
 'client_rc': 0,
 'compatibility_implementation_commit': '8187114c7233be82b188f0fc03b93a022787e7bb',
 'compatibility_status': 'COMPATIBLE_UPDATED',
 'config_entry_records': 97,
 'core_source_baseline': '2026.8.1',
 'corrected_2b_rerun_during_review': False,
 'credential_persisted': False,
 'd': 'PASS_CLOSED',
 'device_records': 229,
 'e': 'PASS_CLOSED',
 'e_handoff': 'ACCEPTED',
 'entity_records': 2425,
 'error_code': 'NONE',
 'evidence_basis': 'USER_SUPPLIED_COMPLETED_EXECUTION_AND_INDEPENDENT_READ_ONLY_REVIEW',
 'evidence_directory': '/tmp/hioc-pe4-ha-discovery-7bb82b7c',
 'evidence_report_sha256': '322e237404c3c721be782e9ce2dbc4ceb1e63b8374af00b6fe75a940624d2ded',
 'evidence_result_sha256': '685606f76aad93ede32b52c2ffa34984408d62d408185ab6141791eded478e43',
 'execution_commit': '063f3ab86c6f6c8c1ae649335856700dfeda6a22',
 'execution_hostname': 'nutandpihole',
 'execution_ipv4': '192.168.100.252',
 'execution_operator': 'jazofv1',
 'f': 'PASS_CLOSED',
 'failed_capability': None,
 'failure_stage': 'COMPLETE',
 'first_execution_error_code': 'UNSUPPORTED_HA_DEPLOYMENT',
 'first_execution_evidence_directory': '/tmp/hioc-pe4-ha-discovery-22be880b',
 'first_execution_failure_stage': 'HA_DEPLOYMENT_DISCOVERY',
 'first_execution_report_sha256': 'efd3aa0cc2f5bc00a459a0c05055ac14e5a9a7ab6cc13aeeb34aa9aa616cb087',
 'first_execution_result': 'FAIL',
 'first_execution_result_sha256': '1e11b6e512db860a8f9b2b6af1723c6aabafd75968d7fd643c891144a7a72195',
 'first_execution_superseded_by_corrected_pass': True,
 'g': 'PASS_CLOSED',
 'git_blob': '9e77993c3f6a533b3d394017d4d97e2366959797',
 'governance_synchronization_commit': '063f3ab86c6f6c8c1ae649335856700dfeda6a22',
 'independent_evidence_review': 'PASS',
 'lifecycle_state': 'PASS_CLOSED',
 'likely_update_compatibility_break': False,
 'logical_instance': 'PI5_HA',
 'observed_ha_core_version': '2026.9.4',
 'operator_block_rc': 0,
 'pe4': 'NOT_COMPLETE',
 'pe4_0b2a': 'PASS_CLOSED',
 'pe4_0b2a_rerun': False,
 'pe4_0b2b': 'PASS_CLOSED',
 'pe4_0c': 'NOT_STARTED',
 'pe4_0c_executed': False,
 'phase_7a': 'ACTIVE',
 'privacy_validation': 'PASS',
 'record_type': 'PE4_0B2B_EXECUTION_CLOSURE',
 'result': 'PASS',
 'rollback': 'NOT_PERFORMED',
 'rollback_executed': False,
 'schema_version': '1.0',
 'sha256': 'b074608e98e887767be964120e8bfad8b5f7fba5fa17d671b0a1a1704f35c1b8',
 'source_path': '/home/jazofv1/hioc-release-source/tools/hioc-pe4-ha-registry-discovery.py',
 'warnings': ['CLASSIFICATION_NOT_DERIVED', 'UNKNOWN_FIELDS', 'UNPUBLISHED_NAMESPACES']}

class CorrectedDiscoveryClosureTests(unittest.TestCase):
    def test_exact_operator_supplied_closure_fields(self):
        record = json.loads(RECORD.read_text(encoding="utf-8"))
        for key, expected in EXPECTED.items():
            with self.subTest(field=key):
                self.assertEqual(record[key], expected)
                self.assertIs(type(record[key]), type(expected))
        self.assertEqual(RECORD.read_text(encoding="utf-8").encode(), (json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n").encode())

    def test_repository_identity_bindings(self):
        record = json.loads(RECORD.read_text(encoding="utf-8"))
        def blob(path):
            return subprocess.check_output(["git", "show", "HEAD:" + path], cwd=ROOT)
        client = "tools/hioc-pe4-ha-registry-discovery.py"
        self.assertEqual(hashlib.sha256(blob(client)).hexdigest(), record["sha256"])
        self.assertEqual(subprocess.check_output(["git", "rev-parse", "HEAD:" + client], cwd=ROOT).decode().strip(), record["git_blob"])
        correction = json.loads(blob("governance/pe4/pe4-0b2b-compatibility-correction.json"))
        self.assertEqual(correction["source"]["git_blob"], record["git_blob"])
        self.assertEqual(correction["source"]["sha256"], record["sha256"])
        self.assertEqual(hashlib.sha256(blob(record["evidence_schema_path"])).hexdigest(), record["evidence_schema_sha256"])
        self.assertEqual(correction["evidence_schema"]["sha256"], record["evidence_schema_sha256"])
        self.assertEqual(correction["evidence_schema"]["version"], record["evidence_schema_version"])
        self.assertEqual(correction["first_execution"]["report_sha256"], record["first_execution_report_sha256"])
        self.assertEqual(correction["first_execution"]["result_sha256"], record["first_execution_result_sha256"])

    def test_current_roadmap_and_limited_proof(self):
        master = (ROOT / "docs/HIOC_MASTER_PLAN.md").read_text(encoding="utf-8")
        current = master.split("# Implementation Status", 1)[1].split("# Historical Operator Preparation Chronology", 1)[0]
        self.assertIn("| PE-4.0B.2b | PASS/CLOSED |", current)
        self.assertIn("| PE-4.0C | PASS/CLOSED |", current)
        self.assertTrue(current.split("## Next Planned Task", 1)[1].strip().startswith("### PE-4 Home Assistant Runtime Credential Provisioning"))
        self.assertIn("Compatibility Diagnostics UX", master)
        self.assertIn("does not prove compatibility with every future HA release", " ".join(current.split()))
        self.assertIn("operator-supplied", current)

if __name__ == "__main__":
    unittest.main()
