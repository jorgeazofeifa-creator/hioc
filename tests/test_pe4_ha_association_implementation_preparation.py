"""Repository-only preparation invariants; no adapter, secret or production execution."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import unittest

from tests.test_pe4_0c_association_contract import validate_schema

ROOT = Path(__file__).resolve().parents[1]
BASE = "9bdf8bdfb990c4cedb821f79c5e2306b868a92fa"
RECORD_PATH = ROOT / "governance/pe4/pe4-ha-association-adapter-implementation-preparation.json"
SCHEMA_PATH = RECORD_PATH.with_name("pe4-ha-association-adapter-implementation-preparation.schema.json")
RECORD = json.loads(RECORD_PATH.read_text(encoding="utf-8"))
SCHEMA = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
LIFE = json.loads((ROOT / RECORD["lifecycle_algorithm"]["authority"]).read_text(encoding="utf-8"))
CONTRACT = json.loads((ROOT / "governance/pe4/pe4-0c-association-contract.json").read_text(encoding="utf-8"))


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


class ImplementationPreparationTests(unittest.TestCase):
    def test_closed_schema_and_canonical_json(self):
        for path in (RECORD_PATH, SCHEMA_PATH):
            value = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(path.read_text(encoding="utf-8"), json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n")
        validate_schema(RECORD, SCHEMA)
        for changes in ({"token": "synthetic-not-a-credential"}, {"runtime_adapter": "IMPLEMENTED"}, {"association_state_schema_version": "1.0"}, {"next_checkpoint": "Implementation"}):
            invalid = copy.deepcopy(RECORD); invalid.update(changes)
            with self.assertRaises(ValueError): validate_schema(invalid, SCHEMA)
        for key in RECORD:
            invalid = copy.deepcopy(RECORD); del invalid[key]
            with self.subTest(missing=key):
                with self.assertRaises(ValueError): validate_schema(invalid, SCHEMA)

    def test_authorities_and_schema_bindings(self):
        self.assertEqual(RECORD["baseline_commit"], BASE)
        for key in ("pe4_0b2b", "pe4_0c", "pe4_0c1", "lifecycle_state"):
            self.assertEqual(RECORD[key], "PASS_CLOSED")
        self.assertEqual(RECORD["status"], "PREPARED_FOR_SEPARATE_IMPLEMENTATION")
        self.assertEqual(RECORD["association_state_schema_version"], LIFE["state_schema_version"])
        self.assertEqual(RECORD["association_state_schema_path"], LIFE["state_schema_path"])
        raw = (ROOT / RECORD["association_state_schema_path"]).read_text(encoding="utf-8").encode()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), RECORD["association_state_schema_sha256"])
        self.assertEqual(CONTRACT["lifecycle_state"], "PASS_CLOSED")
        self.assertEqual(LIFE["lifecycle_state"], "PASS_CLOSED")

    def test_reviewed_baseline_source_identities(self):
        bindings = RECORD["source_review"]["bindings"]
        self.assertGreaterEqual(len(bindings), 50)
        for path, binding in bindings.items():
            with self.subTest(path=path):
                raw = git("show", BASE + ":" + path)
                self.assertEqual(hashlib.sha256(raw).hexdigest(), binding["sha256"])
                self.assertEqual(git("rev-parse", BASE + ":" + path).decode().strip(), binding["git_blob"])
        for path in ("pi4/lib/hioc/inventory.py", "pi4/bin/hioc-inventory-engine.py", "pi4/lib/hioc/core/state.py", "pi4/lib/hioc/core/compatibility.py", "tools/hioc-pe4-ha-auth-capability.py", "tools/hioc-pe4-ha-registry-discovery.py"):
            expected = bindings[path]["git_blob"]
            if path == "pi4/bin/hioc-inventory-engine.py":
                # Frozen predecessor remains checked above; current consumer is now governed.
                implementation=json.loads((ROOT/"governance/pe4/pe4-ha-association-public-projection-implementation.json").read_bytes())
                expected=next(i['git_blob'] for i in implementation['implementation_artifacts'] if i['path']==path)
            self.assertEqual(git("hash-object", "--path=" + path, path).decode().strip(), expected)

    def test_production_paths_runtime_and_no_tools_import(self):
        self.assertEqual(RECORD["module_path"], "pi4/lib/hioc/home_assistant_association.py")
        self.assertEqual(RECORD["entrypoint_path"], "pi4/bin/hioc-home-assistant-association.py")
        for key in ("module_path", "entrypoint_path"):
            # Absence belongs to the frozen preparation baseline, not the current tree.
            self.assertEqual(git("ls-tree","-r","--name-only",BASE,"--",RECORD[key]),b"")
            implementation=json.loads((ROOT/"governance/pe4/pe4-ha-association-runtime-validation-correction.json").read_bytes())
            binding=next(v for v in implementation["sources"].values() if v["path"]==RECORD[key])
            self.assertEqual(hashlib.sha256((ROOT/RECORD[key]).read_bytes()).hexdigest(),binding["sha256"])
        runtime = RECORD["runtime"]
        self.assertEqual(runtime["active"], "/home/jazofv1/hioc/runtime/pe4/active")
        self.assertEqual((runtime["python_version"], runtime["websockets_version"]), ("3.11.2", "16.1.1"))
        self.assertEqual(runtime["flags"], ["-I", "-B"])
        self.assertEqual(runtime["tools_import"], "PROHIBITED")
        self.assertEqual(runtime["mutation"], "PROHIBITED")

    def test_canonical_input_cannot_promote_identity_or_failed_read(self):
        source = RECORD["canonical_inventory"]
        self.assertEqual(source["path"], "state/inventory/inventory.json")
        self.assertEqual(source["stable_id_field"], "devices[].id")
        self.assertEqual(source["canonical_mac_field"], "devices[].mac")
        self.assertEqual(source["schema_version"], "1.0")
        self.assertEqual(source["max_bytes"], 16 * 1024 * 1024)
        self.assertEqual(source["max_age_seconds"], 3 * RECORD["scheduler"]["cadence_seconds"])
        self.assertIn("FAILURE_NOT_DISAPPEARANCE", source["absent_or_invalid"])
        self.assertIn("NO_LAST_WINS", source["duplicate_mac"])
        self.assertIn("READ_ONLY", source["authority"])
        self.assertEqual(RECORD["generic_integration_ingestion"], "PROHIBITED")
        self.assertEqual(RECORD["identity_engine"], CONTRACT["identity_engine"])

    def test_dedicated_lock_and_deadlock_safe_order(self):
        lock = RECORD["lock"]
        self.assertEqual(lock["path"], "state/inventory/associations/.home_assistant.lock")
        self.assertNotEqual(lock["path"], RECORD["compatibility"]["writer_lock"])
        self.assertEqual((lock["owner"], lock["group"], lock["mode"]), ("jazofv1", "jazofv1", "0600"))
        self.assertEqual(lock["directory_mode"], "0700")
        self.assertEqual(lock["acquisition_timeout_seconds"], 0)
        self.assertTrue(lock["network_span"])
        order = lock["ordering"]
        self.assertEqual(order[0], "ASSOCIATION_LOCK")
        self.assertLess(order.index("ASSOCIATION_COMMIT"), order.index("COMPATIBILITY_LOCK_THROUGH_UPDATE_STATUS"))
        self.assertIn("NO_INVENTORY_OR_COMPATIBILITY_LOCK_HELD_DURING_NETWORK", lock["other_lock_rule"])
        self.assertIn("NEVER_UNLINK_LOCK", lock["release"])

    def test_publication_transaction_retains_prior_and_recovers(self):
        writer = RECORD["state_writer"]
        self.assertFalse(writer["generic_state_writer_sufficient"])
        self.assertEqual(RECORD["private_state_path"], LIFE["private_state_path"])
        self.assertEqual(writer["file_mode"], "0600")
        for invariant in ("FILE_FLUSH_FSYNC", "FD_REREAD_HASH_AND_METADATA", "ATOMIC_REPLACE", "ASSOCIATION_DIRECTORY_FSYNC", "DURABLE_COMMITTED_MARKER"):
            self.assertIn(invariant, writer["durability"])
        self.assertIn("RESTORE_EXACT_PRIOR", writer["failure_before_commit"])
        self.assertIn("UNCOMMITTED_INTENT_RESTORE_PRIOR", writer["recovery"])
        self.assertIn("COMPLETED_RECOVERY_NEVER_RESTORES_PRIOR", writer["cleanup"])
        self.assertIn("NO_FALSE_PRESERVATION_CLAIM", writer["unverifiable_recovery"])
        self.assertIn("NOT_FAILED_CYCLE", writer["post_commit_error"])

    def test_credential_security_and_separate_prerequisite(self):
        credential = RECORD["credential"]
        self.assertEqual(credential["storage_path"], "/etc/hioc/credentials/home_assistant.token")
        self.assertEqual((credential["owner"], credential["group"], credential["mode"]), ("root", "jazofv1", "0640"))
        self.assertFalse(credential["provisioned_now"])
        for key in ("argv", "normal_environment", "ordinary_config", "state_evidence_logs_mqtt_exception_echo"):
            self.assertEqual(credential[key], "PROHIBITED")
        self.assertEqual(credential["max_file_bytes"], credential["max_token_bytes"] + 1)
        self.assertIn("AT_MOST_ONE_FINAL_LF", credential["newline_policy"])
        self.assertEqual(credential["empty_token"], "REJECT")
        self.assertIn("NO_FALLBACK", credential["deletion"])
        self.assertEqual(RECORD["next_checkpoint"], "PE-4 Home Assistant Runtime Credential Provisioning")
        self.assertEqual(RECORD["required_prerequisite"]["name"], RECORD["next_checkpoint"])
        self.assertEqual(RECORD["required_prerequisite"]["status"], "NOT_STARTED")
        self.assertNotIn("token_value", credential)

    def test_all_required_commands_and_relationship_incomplete_reconciled(self):
        expected = ["config/device_registry/list", "config/entity_registry/list", "config/area_registry/list", "config_entries/get"]
        self.assertEqual(RECORD["transport"]["commands"], expected)
        self.assertEqual(RECORD["transport"]["command_ids"], [1, 2, 3, 4])
        self.assertEqual(RECORD["transport"]["structural_cores"], CONTRACT["structural_cores"])
        state_schema = json.loads((ROOT / RECORD["association_state_schema_path"]).read_text())
        props = state_schema["properties"]["associations"]["items"]["properties"]
        self.assertEqual(set(RECORD["private_metadata_projection"]["ha_metadata"]), set(props["ha_metadata"]["properties"]))
        self.assertEqual(set(RECORD["private_metadata_projection"]["entity"]), set(props["entities"]["items"]["properties"]))
        self.assertEqual(RECORD["transport"]["retries"], 0)
        self.assertEqual(RECORD["transport"]["total_network_seconds"], 90)
        self.assertIn("ALL_FOUR_SUCCESS", RECORD["transport"]["required_commands"])
        self.assertIn("SUCCESSFUL_SNAPSHOT_ONLY", RECORD["relationships"]["incomplete"])
        self.assertEqual(RECORD["relationships"]["command_failure"], "FAIL_WHOLE_CYCLE_NOT_INCOMPLETE")

    def test_single_ha_producer_matches_actual_registry(self):
        registry = json.loads((ROOT / "governance/compatibility-contracts.json").read_text())
        dep = next(d for d in registry["dependencies"] if d["dependency_id"] == "ha_core")
        compat = RECORD["compatibility"]
        self.assertEqual(compat["required_capabilities"], dep["required_capabilities"])
        self.assertEqual(dep["optional_capabilities"], [])
        self.assertIn("SOLE_RECURRING_HA_PRODUCER_FULL_SIX", compat["ownership"])
        self.assertIn("NO_PARTIAL", compat["merge_policy"])
        self.assertIn("NO_EXACT_HA_VERSION_GATE", compat["version_policy"])
        self.assertTrue(compat["no_adapter_mqtt"])

    def test_history_lifecycle_scope_and_scheduler(self):
        lifecycle = RECORD["lifecycle_algorithm"]
        self.assertEqual(lifecycle["history_max_records"], LIFE["history_policy"]["max_records"])
        self.assertFalse(lifecycle["history_eviction"])
        self.assertFalse(lifecycle["historical_projection"])
        self.assertFalse(lifecycle["liveness_authority"])
        self.assertEqual(lifecycle["failed_cycle"], "ENTIRE_PRIOR_STATE_UNCHANGED")
        self.assertEqual(RECORD["public_projection"]["disposition"], "DEFERRED")
        self.assertEqual(RECORD["public_projection"]["checkpoint"], "PE-4 Home Assistant Association Public Projection")
        self.assertEqual(RECORD["scheduler"]["cron_cadence"], "5,35 * * * *")
        self.assertIn("NEXT_SCHEDULED", RECORD["scheduler"]["retry"])
        self.assertEqual(len(RECORD["first_implementation_scope"]), 21)

    def test_failure_coverage_and_truthful_commit_boundary(self):
        self.assertEqual(set(RECORD["failure_model"]), set(RECORD["result_contract"]["failure_stages"]))
        self.assertEqual(len(RECORD["failure_model"]), 17)
        for failure, model in RECORD["failure_model"].items():
            self.assertIn("PRESERVE_ENTIRE", model["last_known_good"])
            self.assertIs(type(model["credential_could_be_acquired"]), bool)
            self.assertIs(type(model["network_could_have_occurred"]), bool)
            self.assertIs(type(model["candidate_could_exist"]), bool)
        self.assertFalse(RECORD["failure_model"]["LOCK_ACQUISITION"]["network_could_have_occurred"])
        self.assertTrue(RECORD["failure_model"]["CANONICAL_INVENTORY_INPUT"]["network_could_have_occurred"])
        self.assertIn("PASS_WITH_WARNING", RECORD["result_contract"]["results"])
        self.assertIn("LAST_KNOWN_GOOD_PRESERVED", RECORD["result_contract"]["fields"])

    def test_current_lifecycle_and_preserved_roadmap(self):
        text = (ROOT / "docs/HIOC_MASTER_PLAN.md").read_text(encoding="utf-8")
        current = text.split("# Implementation Status", 1)[1].split("# Historical Operator Preparation Chronology", 1)[0]
        for row in ("| PE-4.0B.2b | PASS/CLOSED |", "| PE-4.0C | PASS/CLOSED |", "| PE-4.0C.1 Association Lifecycle Clarification | PASS/CLOSED |", "| PE-4 Home Assistant Association Adapter Implementation Preparation | PASS/CLOSED |", "| PE-4 Home Assistant Runtime Credential Provisioning | PASS/CLOSED |", "| PE-4 Home Assistant Association Adapter Implementation | PASS/CLOSED, corrected before deployment |", "| PE-4 | NOT COMPLETE |", "| Phase 7A | ACTIVE |", "| Rollback | NOT PERFORMED |"):
            self.assertIn(row, current)
        self.assertTrue(current.split("## Next Planned Task", 1)[1].strip().startswith("### PE-4 Home Assistant Association Public Projection"))
        self.assertIn("Compatibility Diagnostics UX", text)
        for key, value in {"runtime_adapter":"NOT_IMPLEMENTED", "deployment":"NOT_STARTED", "production_execution":"NOT_STARTED", "rollback":"NOT_PERFORMED"}.items():
            self.assertEqual(RECORD[key], value)
        self.assertTrue(RECORD["no_production_action"])


if __name__ == "__main__":
    unittest.main()
