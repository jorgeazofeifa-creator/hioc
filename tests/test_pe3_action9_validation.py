import pathlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "hioc-pe3-action9-validate.sh"
COMPLETION_DOCUMENTS = (
    ROOT / "DECISIONS.md",
    ROOT / "docs" / "CHANGELOG.md",
    ROOT / "docs" / "DEPLOYMENT.md",
    ROOT / "docs" / "HIOC_MASTER_PLAN.md",
    ROOT / "docs" / "OPERATIONS.md",
    ROOT / "docs" / "PE3_MANUFACTURER_PRODUCTION_RUNBOOK.md",
    ROOT / "docs" / "RELEASE.md",
)


class PE3Action9ValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = SCRIPT.read_text(encoding="utf-8")
        cls.programs = re.findall(r"<<'PY'[^\n]*\n(.*?)\nPY", cls.text, re.S)
        cls.result_program = next(program for program in cls.programs if "expected_keys" not in program and "keys={'schema_version'" in program)
        cls.performance_program = next(program for program in cls.programs if "historical_elapsed" not in program and "elapsed > 4" in program)
        cls.protected_program = next(program for program in cls.programs if "set(protected)" in program)

    def run_evidence_program(self, program, root):
        return subprocess.run(
            [sys.executable, "-c", program, str(root)],
            text=True, capture_output=True,
        )

    def write_valid_evidence(self, root, elapsed="1.250000", rss="2048", status="MEASURED"):
        root.mkdir()
        (root / "pre").mkdir()
        result = {
            "schema_version": "1.0", "result": "PASS", "status": "online",
            "record_count": 4, "matched_count": 2, "unknown_count": 0,
            "excluded_count": 2, "invalid_count": 0, "error": None,
        }
        (root / "generation-result.json").write_text(json.dumps(result), encoding="utf-8")
        (root / "generation-performance.txt").write_text(
            f"manufacturer_generation_elapsed_seconds={elapsed} "
            f"manufacturer_generation_max_rss_kib={rss} "
            f"manufacturer_generation_measurement_status={status}\n",
            encoding="ascii",
        )
        (root / "pre" / "protected.json").write_text(
            json.dumps({"stable": [], "operational_drift": []}), encoding="utf-8"
        )
        return result

    def test_exact_interface_and_commit_validation(self):
        self.assertIn("--governance-commit", self.text)
        self.assertIn("--action8-evidence-dir", self.text)
        self.assertIn("'^[0-9a-f]{40}$'", self.text)
        self.assertIn("INVALID_ARGUMENTS", self.text)
        self.assertIn("INVALID_GOVERNANCE_COMMIT", self.text)

    def test_target_operator_and_roots(self):
        for value in ("nutandpihole", "192.168.100.252", "jazofv1", "/home/jazofv1/hioc-release-source", "/home/jazofv1/hioc"):
            self.assertIn(value, self.text)
        for code in ("WRONG_TARGET", "WRONG_OPERATOR", "SOURCE_REPOSITORY_DIRTY", "ACTIVE_GIT_OPERATION"):
            self.assertIn(code, self.text)

    def test_governed_artifact_identity(self):
        for rel in ("tools/hioc-pe3-action9-validate.sh", "tools/hioc-pe3-action8-generate.sh", "pi4/bin/hioc-validate-manufacturer.py", "pi4/lib/hioc/manufacturer.py"):
            self.assertIn(rel, self.text)
        self.assertIn('rev-parse "$GOVERNANCE_COMMIT:$rel"', self.text)
        self.assertIn('hash-object --path="$rel"', self.text)

    def test_action8_evidence_path_and_permissions(self):
        self.assertIn("/tmp/hioc-pe3-action8-*", self.text)
        self.assertIn('owned_directory "$ACTION8_EVIDENCE_DIR" 700', self.text)
        self.assertIn('owned_file "$path" 600', self.text)
        for code in ("ACTION8_EVIDENCE_PATH_INVALID", "ACTION8_EVIDENCE_DIRECTORY_UNSAFE", "ACTION8_EVIDENCE_FILE_UNSAFE"):
            self.assertIn(code, self.text)

    def test_action8_success_schema_and_failure_rejection(self):
        for value in ("generation-result.json", "generation-performance.txt", "pre/protected.json", "generation-failure.json", "ACTION8_FAILURE_EVIDENCE_PRESENT"):
            self.assertIn(value, self.text)
        self.assertIn("result.get('result')!='PASS'", self.text)
        self.assertIn("sum(counts[1:])!=counts[0]", self.text)
        self.assertIn("ACTION8_EVIDENCE_CONTENTS_INVALID", self.text)

    def test_result_validation_behavior(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary) / "evidence"
            result = self.write_valid_evidence(root)
            self.assertEqual(self.run_evidence_program(self.result_program, root).returncode, 0)
            (root / "generation-result.json").write_text("{", encoding="utf-8")
            self.assertEqual(self.run_evidence_program(self.result_program, root).returncode, 2)
            result["extra"] = True
            (root / "generation-result.json").write_text(json.dumps(result), encoding="utf-8")
            self.assertEqual(self.run_evidence_program(self.result_program, root).returncode, 2)
            result.pop("extra")
            result["record_count"] = "4"
            (root / "generation-result.json").write_text(json.dumps(result), encoding="utf-8")
            self.assertEqual(self.run_evidence_program(self.result_program, root).returncode, 3)

    def test_result_count_partition_and_non_null_error(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary) / "evidence"
            result = self.write_valid_evidence(root)
            result["record_count"] = 5
            (root / "generation-result.json").write_text(json.dumps(result), encoding="utf-8")
            self.assertEqual(self.run_evidence_program(self.result_program, root).returncode, 3)
            result["record_count"] = 4
            result["error"] = {"code": "unexpected"}
            (root / "generation-result.json").write_text(json.dumps(result), encoding="utf-8")
            self.assertEqual(self.run_evidence_program(self.result_program, root).returncode, 2)

    def test_performance_uses_action8_evidence_only(self):
        for value in ("manufacturer_generation_elapsed_seconds", "manufacturer_generation_max_rss_kib", "PERFORMANCE_MEASUREMENT_STATUS=MEASURED", "ACTION8_PERFORMANCE_ASSESSMENT=PASS"):
            self.assertIn(value, self.text)
        self.assertNotIn("/usr/bin/time", self.text)

    def test_performance_behavior_and_unvalidated_baseline(self):
        cases = (
            ("1.0", "1024", "FALSE", "FALSE"),
            ("12.467231", "1024", "TRUE", "FALSE"),
            ("1.0", "146744", "FALSE", "TRUE"),
            ("12.467231", "146744", "TRUE", "TRUE"),
        )
        for elapsed, rss, elapsed_exceeded, rss_exceeded in cases:
            with self.subTest(elapsed=elapsed, rss=rss), tempfile.TemporaryDirectory() as temporary:
                root = pathlib.Path(temporary) / "evidence"
                self.write_valid_evidence(root, elapsed=elapsed, rss=rss)
                completed = self.run_evidence_program(self.performance_program, root)
                self.assertEqual(completed.returncode, 0, completed.stderr)
                fields = completed.stdout.strip().split("\t")
                self.assertEqual(fields[2:], [elapsed_exceeded, rss_exceeded])
        self.assertIn("PERFORMANCE_BASELINE_STATUS=UNVALIDATED", self.text)
        self.assertIn("PERFORMANCE_OBSERVATION=INSUFFICIENT_BASELINE", self.text)
        self.assertIn("HISTORICAL_TARGETS_PRODUCTION_ENFORCED=FALSE", self.text)

    def test_performance_malformed_status_and_negative_values(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary) / "evidence"
            self.write_valid_evidence(root)
            path = root / "generation-performance.txt"
            path.write_text("missing-keys\n", encoding="ascii")
            self.assertEqual(self.run_evidence_program(self.performance_program, root).returncode, 4)
            self.write_valid_performance(path, "1.0", "2", "UNAVAILABLE")
            self.assertEqual(self.run_evidence_program(self.performance_program, root).returncode, 5)
            self.write_valid_performance(path, "-1", "2", "MEASURED")
            self.assertEqual(self.run_evidence_program(self.performance_program, root).returncode, 4)
            self.write_valid_performance(path, "1", "-2", "MEASURED")
            self.assertEqual(self.run_evidence_program(self.performance_program, root).returncode, 4)

    @staticmethod
    def write_valid_performance(path, elapsed, rss, status):
        path.write_text(
            f"manufacturer_generation_elapsed_seconds={elapsed} "
            f"manufacturer_generation_max_rss_kib={rss} "
            f"manufacturer_generation_measurement_status={status}\n",
            encoding="ascii",
        )

    def test_protected_snapshot_behavior(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary) / "evidence"
            self.write_valid_evidence(root)
            self.assertEqual(self.run_evidence_program(self.protected_program, root).returncode, 0)
            (root / "pre" / "protected.json").write_text(
                json.dumps({"stable": {}}), encoding="utf-8"
            )
            self.assertEqual(self.run_evidence_program(self.protected_program, root).returncode, 2)

    def test_configuration_dataset_inventory_and_artifacts(self):
        for value in ("MANUFACTURER_DB_PATH", "local-ieee-ra--2026-08-11-r1", "CONFIGURATION_SELECTION_MISMATCH", "DATASET_IDENTITY_MISMATCH", "INVENTORY_IDENTITY_INVALID", "MANUFACTURER_TEMP_ARTIFACT_PRESENT"):
            self.assertIn(value, self.text)
        self.assertIn('owned_file "$SIDE" 600', self.text)
        self.assertIn('owned_file "$STATUS" 600', self.text)
        self.assertIn('safe_owned_file "$INVENTORY"', self.text)

    def test_read_only_validator_and_privacy_contract(self):
        self.assertIn("hioc-validate-manufacturer.py", self.text)
        self.assertIn("privacy_safe", self.text)
        self.assertIn("status':'online'", self.text)
        self.assertIn("MANUFACTURER_ARTIFACT_VALIDATION=PASS", self.text)
        for forbidden in ("hioc-generate-manufacturer.py", "release/upgrade.sh", "pi4/install_pi4.sh", "systemctl", "crontab"):
            self.assertNotIn(forbidden, self.text)

    def test_protected_state_is_unchanged(self):
        for value in ("manufacturer.json", "manufacturer_status.json", "inventory.json", "hioc.conf", "manufacturer-db.json", "manufacturer-db.manifest.json", "PROTECTED_STATE_CHANGED"):
            self.assertIn(value, self.text)
        self.assertIn("if before!=after", self.text)

    def test_private_action9_evidence_and_result_last(self):
        self.assertIn("/tmp/hioc-pe3-action9-XXXXXXXX", self.text)
        self.assertIn('chmod 0700 "$EVIDENCE_DIR"', self.text)
        self.assertIn('chmod 0600 "$REPORT_TEMP"', self.text)
        self.assertIn("evidence-report.json", self.text)
        self.assertIn("action9-result.txt", self.text)
        publish = self.text.split("publish_report() {", 1)[1].split("main() {", 1)[0]
        self.assertLess(publish.index('mv -fT -- "$REPORT_TEMP"'), publish.index('mv -fT -- "$RESULT_TEMP"'))

    def test_pass_order_and_bounded_failure(self):
        ordered = (
            "TARGET_IDENTITY=PASS", "SOURCE_IDENTITY=PASS", "RUNTIME_IDENTITY=PASS",
            "ACTION8_EVIDENCE_IDENTITY=PASS", "ACTION8_RESULT_VALIDATION=PASS",
            "ACTION8_PERFORMANCE_SYNTAX=PASS", "ACTION8_PERFORMANCE_ASSESSMENT=PASS",
            "ACTION8_PROTECTED_SNAPSHOT_VALIDATION=PASS", "EVIDENCE_PREPARATION=PASS",
            "CONFIGURATION_IDENTITY=PASS", "DATASET_IDENTITY=PASS", "INVENTORY_IDENTITY=PASS",
            "MANUFACTURER_ARTIFACT_IDENTITY=PASS", "MANUFACTURER_ARTIFACT_VALIDATION=PASS",
            "PROTECTED_STATE=PASS", "EVIDENCE_REPORT=PASS", "ACTION9=COMPLETE",
        )
        success = "\n".join(line for line in self.text.splitlines() if "printf '" in line and "=PASS" in line)
        positions = [success.index(value) for value in ordered]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("EVIDENCE_REPORT=PASS\\nEVIDENCE_DIR=%s\\nACTION9=COMPLETE\\nRESULT=PASS\\nROLLBACK_RECOMMENDED=FALSE", self.text)
        for value in ("RESULT=%s", "ERROR_CODE=%s", "FAILURE_STAGE=%s", "ROLLBACK_RECOMMENDED=FALSE"):
            self.assertIn(value, self.text)
        self.assertNotIn("ACTION8_EVIDENCE_VALIDATION_FAILED", self.text)
        self.assertNotIn("FAILURE_STAGE=ACTION8_EVIDENCE_VALIDATION", self.text)
        for code, stage in (
            ("ACTION8_RESULT_SCHEMA_INVALID", "ACTION8_RESULT_VALIDATION"),
            ("ACTION8_RESULT_COUNTS_INVALID", "ACTION8_RESULT_VALIDATION"),
            ("ACTION8_PERFORMANCE_FORMAT_INVALID", "ACTION8_PERFORMANCE_SYNTAX"),
            ("ACTION8_PERFORMANCE_STATUS_INVALID", "ACTION8_PERFORMANCE_SYNTAX"),
            ("ACTION8_PROTECTED_SNAPSHOT_SCHEMA_INVALID", "ACTION8_PROTECTED_SNAPSHOT_VALIDATION"),
        ):
            self.assertIn(code, self.text)
            self.assertIn(stage, self.text)

    def test_rollback_is_always_false_and_no_later_action(self):
        self.assertNotIn("ROLLBACK_RECOMMENDED=TRUE", self.text)
        for forbidden in ("ACTION10", "hioc-pe3-action10", "TRANSPORT_STAGING", "hioc-pe3-dataset-transfer"):
            self.assertNotIn(forbidden, self.text)

    def test_evidence_report_is_bounded(self):
        for value in ("'schema_version':'1.0'", "'action':'PE-3_ACTION9'", "'governance_commit':commit", "'rollback_recommended':False", "'warnings':['PERFORMANCE_BASELINE_NOT_ESTABLISHED']"):
            self.assertIn(value, self.text)
        for forbidden in ("mac_address", "matched_prefix", "organization", "error_message", "secret"):
            self.assertNotIn(forbidden, self.text.lower())
        for value in (
            "'maximum_child_rss_kib'", "'rss_semantic':'TOTAL_PEAK_CHILD_RSS'",
            "'baseline_status':'UNVALIDATED'", "'observation':'INSUFFICIENT_BASELINE'",
            "'historical_targets_production_enforced':False",
        ):
            self.assertIn(value, self.text)

    def test_current_governance_records_action9_and_pe3_completion(self):
        for path in COMPLETION_DOCUMENTS:
            text = " ".join(path.read_text(encoding="utf-8").split())
            self.assertIn("/tmp/hioc-pe3-action9-Bb6vGrmm", text, path)
            self.assertRegex(
                text,
                r"Actions 1[–-]10.{0,30}(?:\*\*)?(?:COMPLETE|complete)(?:\*\*)?",
                path,
            )
            self.assertRegex(
                text,
                r"Action 10.{0,120}(?:\*\*)?(?:COMPLETE|complete)(?:\*\*)?",
                path,
            )
        runbook = " ".join(
            (ROOT / "docs" / "PE3_MANUFACTURER_PRODUCTION_RUNBOOK.md")
            .read_text(encoding="utf-8")
            .split()
        )
        self.assertIn("HISTORICAL_TARGETS_PRODUCTION_ENFORCED=FALSE", runbook)
        self.assertIn("Historical Action 9 corrective checkpoint", runbook)

    def test_embedded_python_compiles(self):
        self.assertEqual(len(self.programs), 5)
        for index, program in enumerate(self.programs):
            compile(program, f"action9-embedded-{index}", "exec")

    def test_no_global_strict_mode_or_shell_exit(self):
        self.assertNotRegex(self.text, r"(?m)^\s*set\s+-[^\n]*e")
        self.assertNotRegex(self.text, r"(?m)^\s*exit(?:\s|$)")

    def test_parent_shell_survives_invalid_input(self):
        shell = shutil.which("bash")
        if not shell:
            self.skipTest("Bash is required")
        result = subprocess.run([shell, "-c", f"source '{SCRIPT.as_posix()}'; printf 'PARENT_SHELL_ALIVE=TRUE\\n'"], text=True, capture_output=True)
        self.assertIn("ERROR_CODE=INVALID_ARGUMENTS", result.stdout)
        self.assertIn("PARENT_SHELL_ALIVE=TRUE", result.stdout)


if __name__ == "__main__":
    unittest.main()
