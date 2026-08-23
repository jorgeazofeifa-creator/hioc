import hashlib
import os
import pathlib
import re
import shutil
import subprocess
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "hioc-pe3-action8-generate.sh"
RUNBOOK = ROOT / "docs" / "PE3_MANUFACTURER_PRODUCTION_RUNBOOK.md"
MASTER_PLAN = ROOT / "docs" / "HIOC_MASTER_PLAN.md"
DECISIONS = ROOT / "DECISIONS.md"


class PE3Action8GenerationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = SCRIPT.read_text(encoding="utf-8")
        cls.runbook = RUNBOOK.read_text(encoding="utf-8")
        cls.action8 = cls.runbook.split("## Action 8", 1)[1].split("## Action 9", 1)[0]
        cls.action8_flat = " ".join(cls.action8.split())
        cls.bootstrap = cls.action8.split("```bash", 1)[1].split("```", 1)[0]

    def test_unsafe_inline_action8_is_retired(self):
        self.assertIn("ACTION 8 OPERATOR-SAFETY AND EVIDENCE CONTRACT DEFECT", self.action8_flat)
        self.assertNotIn("```bash\nset -euo pipefail", self.action8)
        self.assertNotIn("| tee \"$EVIDENCE_DIR", self.action8)
        self.assertNotIn("hioc-pe3-production-validation-XXXXXXXX", self.action8)

    def test_bootstrap_is_frozen_and_separate(self):
        self.assertIn("hioc_pe3_action8_bootstrap_sync()", self.bootstrap)
        self.assertIn("b8c38607325acaf6ab3a02878c834e05e54bea56", self.bootstrap)
        self.assertNotIn("91360c1f83c890dd340a9a6390bf462cb0f95731", self.bootstrap)
        self.assertIn("ACTION8_BOOTSTRAP=COMPLETE", self.bootstrap)
        self.assertIn("GOVERNANCE_COMMIT=${1:-}", self.bootstrap)
        self.assertIn('[ "$#" -eq 1 ]', self.bootstrap)
        self.assertIn("<operator-approved-full-40-hex-governance-commit>", self.bootstrap)
        self.assertNotRegex(self.bootstrap, r"GOVERNANCE_COMMIT=[0-9a-f]{40}")
        self.assertNotIn('bash "$SCRIPT"', self.bootstrap)
        for forbidden in (
            "/home/jazofv1/hioc/config", "hioc-pe3-dataset-transfer",
            "manufacturer.json", "manufacturer_status.json", "ACTION9",
            "systemctl", "release/upgrade.sh",
        ):
            self.assertNotIn(forbidden, self.bootstrap)

    def test_superseded_blob_is_retained_only_as_historical_evidence_or_test_sentinel(self):
        old_blob = "91360c1f83c890dd340a9a6390bf462cb0f95731"
        self.assertNotIn(old_blob, self.bootstrap)
        self.assertIn(old_blob, MASTER_PLAN.read_text(encoding="utf-8"))
        self.assertIn(old_blob, DECISIONS.read_text(encoding="utf-8"))
        self.assertIn("historical", DECISIONS.read_text(encoding="utf-8").lower())

    def test_bootstrap_operator_safety_and_pass_contract(self):
        self.assertIn("set +x", self.bootstrap)
        self.assertNotRegex(self.bootstrap, r"(?m)^\s*(?:set\s+-[^\n]*e|exit(?:\s|$))")
        for marker in (
            "TARGET_IDENTITY=PASS", "REPOSITORY_PRECONDITION=PASS",
            "REPOSITORY_SYNCHRONIZATION=PASS", "SYNCHRONIZED_HEAD_IDENTITY=PASS",
            "ACTION8_SCRIPT_AVAILABILITY=PASS", "ACTION8_SCRIPT_IDENTITY=PASS",
            "ACTION8_BOOTSTRAP=COMPLETE", "RESULT=PASS",
        ):
            self.assertIn(marker, self.bootstrap)
        for marker in ("ERROR_CODE=%s", "FAILURE_STAGE=%s", "ROLLBACK_RECOMMENDED=FALSE"):
            self.assertIn(marker, self.bootstrap)

    def test_bootstrap_input_and_failure_mappings(self):
        self.assertIn("'^[0-9a-f]{40}$'", self.bootstrap)
        self.assertLess(self.bootstrap.index("INVALID_GOVERNANCE_COMMIT"), self.bootstrap.index("hostname -s"))
        self.assertLess(self.bootstrap.index("INVALID_GOVERNANCE_COMMIT"), self.bootstrap.index("fetch origin"))
        mappings = {
            "WRONG_TARGET": "TARGET_SYNCHRONIZATION",
            "SOURCE_REPOSITORY_MISSING": "REPOSITORY_PRECONDITION",
            "WRONG_BRANCH": "REPOSITORY_PRECONDITION",
            "SOURCE_REPOSITORY_DIRTY": "REPOSITORY_PRECONDITION",
            "ACTIVE_GIT_OPERATION": "REPOSITORY_PRECONDITION",
            "GIT_FETCH_FAILED": "REPOSITORY_SYNCHRONIZATION",
            "GOVERNANCE_COMMIT_MISMATCH": "REPOSITORY_SYNCHRONIZATION",
            "NON_FAST_FORWARD_SOURCE": "REPOSITORY_SYNCHRONIZATION",
            "FAST_FORWARD_FAILED": "REPOSITORY_SYNCHRONIZATION",
            "POST_SYNC_HEAD_MISMATCH": "SYNCHRONIZED_HEAD_IDENTITY",
            "POST_SYNC_REPOSITORY_DIRTY": "SYNCHRONIZED_HEAD_IDENTITY",
            "ACTION8_SCRIPT_MISSING": "SCRIPT_AVAILABILITY",
            "ACTION8_SCRIPT_NOT_REGULAR": "SCRIPT_AVAILABILITY",
            "ACTION8_SCRIPT_GIT_IDENTITY_MISMATCH": "SCRIPT_IDENTITY",
            "ACTION8_SCRIPT_WORKTREE_IDENTITY_MISMATCH": "SCRIPT_IDENTITY",
        }
        for code, stage in mappings.items():
            self.assertRegex(self.bootstrap, rf"fail {code} {stage}")

    def test_bootstrap_exact_synchronization_and_identity_barriers(self):
        barriers = (
            'branch --show-current 2>/dev/null)" = main',
            'status --porcelain 2>/dev/null)',
            'fetch origin',
            'rev-parse origin/main 2>/dev/null)" = "$GOVERNANCE_COMMIT"',
            'merge-base --is-ancestor HEAD "$GOVERNANCE_COMMIT"',
            'merge --ff-only origin/main',
            'rev-parse HEAD 2>/dev/null)" = "$GOVERNANCE_COMMIT"',
            '[ ! -L "$SCRIPT" ]', '[ -e "$SCRIPT" ]', '[ -f "$SCRIPT" ]',
            'rev-parse "$GOVERNANCE_COMMIT:$SCRIPT_REL"',
            'hash-object --path="$SCRIPT_REL" "$SCRIPT"',
            'diff --quiet -- "$SCRIPT_REL"',
        )
        for barrier in barriers:
            self.assertIn(barrier, self.bootstrap)
        self.assertLess(self.bootstrap.index("fetch origin"), self.bootstrap.index("merge --ff-only"))
        self.assertLess(self.bootstrap.index("merge --ff-only"), self.bootstrap.index("POST_SYNC_HEAD_MISMATCH"))
        self.assertLess(self.bootstrap.index("POST_SYNC_REPOSITORY_DIRTY"), self.bootstrap.index("ACTION8_SCRIPT_MISSING"))

    def test_invalid_bootstrap_input_preserves_parent_shell(self):
        shell = os.environ.get("HIOC_TEST_SHELL") or shutil.which("bash")
        if not shell:
            self.skipTest("Bash is required")
        body = self.bootstrap.rsplit("hioc_pe3_action8_bootstrap_sync", 1)[0]
        invalid_args = (
            "", "invalid", "d47eb6e", "D47EB6E272E75E2209591693E819F62423F7DC70",
            "main", "v1.0.0", "d47eb6e272e75e2209591693e819f62423f7dc70 extra",
        )
        for args in invalid_args:
            command = body + f"hioc_pe3_action8_bootstrap_sync {args}; printf 'PARENT_SHELL_ALIVE=TRUE\\n'"
            result = subprocess.run([shell, "-c", command], text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("ERROR_CODE=INVALID_GOVERNANCE_COMMIT", result.stdout)
            self.assertIn("FAILURE_STAGE=INPUT_VALIDATION", result.stdout)
            self.assertIn("ROLLBACK_RECOMMENDED=FALSE", result.stdout)
            self.assertIn("PARENT_SHELL_ALIVE=TRUE", result.stdout)
            self.assertNotIn("TARGET_IDENTITY=PASS", result.stdout)
            self.assertNotIn("REPOSITORY_SYNCHRONIZATION=PASS", result.stdout)

    def test_exact_identity_contract(self):
        self.assertIn('"$(id -un 2>/dev/null)" = jazofv1', self.script)
        self.assertIn('"$(id -gn 2>/dev/null)" = jazofv1', self.script)
        for value in (
            "local-ieee-ra--2026-08-11-r1", "8652642", "1338",
            "81f147cc57768c5797c4ad73a8c0369001bbdcbfe1548e71d3702c8c7f81e0e1",
            "10c8097c0a4ec6e8cc4cd3dc61afc7f368057f4ef4b6534df9f6dd31634a4ac4",
            "53581",
        ):
            self.assertIn(value, self.script)
        for rel in (
            "hioc-pe3-action8-generate.sh", "hioc-generate-manufacturer.py",
            "hioc-validate-manufacturer.py", "manufacturer.py",
        ):
            self.assertIn(rel, self.script)

    def test_pass_and_failure_contracts(self):
        for marker in (
            "TARGET_IDENTITY=PASS", "SOURCE_IDENTITY=PASS", "RUNTIME_IDENTITY=PASS",
            "EVIDENCE_PRECONDITION=PASS", "CONFIGURATION_IDENTITY=PASS",
            "DATASET_IDENTITY=PASS", "DATASET_VALIDATION=PASS",
            "INVENTORY_IDENTITY=PASS", "OUTPUT_PRECONDITION=PASS",
            "PROTECTED_PRE_STATE=PASS", "MANUFACTURER_GENERATION=PASS",
            "MANUFACTURER_ARTIFACT_IDENTITY=PASS",
            "MANUFACTURER_ARTIFACT_VALIDATION=PASS",
            "PROTECTED_POST_GENERATION=PASS", "EVIDENCE_PUBLICATION=PASS",
            "EVIDENCE_REPORT=PASS", "EVIDENCE_DIR=%s", "ACTION8=COMPLETE",
            "RESULT=PASS", "ROLLBACK_RECOMMENDED=FALSE",
        ):
            self.assertIn(marker, self.script)
        for marker in ("ERROR_CODE=%s", "FAILURE_STAGE=%s", "ROLLBACK_RECOMMENDED=%s"):
            self.assertIn(marker, self.script)
        ordered = (
            "TARGET_IDENTITY=PASS", "SOURCE_IDENTITY=PASS", "RUNTIME_IDENTITY=PASS",
            "CONFIGURATION_IDENTITY=PASS", "DATASET_IDENTITY=PASS",
            "DATASET_VALIDATION=PASS", "INVENTORY_IDENTITY=PASS",
            "OUTPUT_PRECONDITION=PASS", "EVIDENCE_PRECONDITION=PASS",
            "PROTECTED_PRE_STATE=PASS", "MANUFACTURER_GENERATION=PASS",
            "MANUFACTURER_ARTIFACT_IDENTITY=PASS",
            "MANUFACTURER_ARTIFACT_VALIDATION=PASS",
            "PROTECTED_POST_GENERATION=PASS", "EVIDENCE_PUBLICATION=PASS",
            "EVIDENCE_REPORT=PASS", "ACTION8=COMPLETE", "RESULT=PASS",
        )
        for marker in ordered:
            self.assertIn(marker.split("=", 1)[0], self.action8)
        main_body = self.script.split("main() {", 1)[1].split("action8_entry() {", 1)[0]
        phases = (
            "verify_target_source_runtime", "verify_configuration_dataset_inventory",
            "verify_output_prestate", "prepare_evidence_directory",
            "write_protected_snapshot", "run_generation", "validate_and_publish_evidence",
        )
        positions = [main_body.index(phase) for phase in phases]
        self.assertEqual(positions, sorted(positions))
        self.assertIn(
            "EVIDENCE_PUBLICATION=PASS\\nEVIDENCE_REPORT=PASS\\nEVIDENCE_DIR=%s\\n"
            "ACTION8=COMPLETE\\nRESULT=PASS\\nROLLBACK_RECOMMENDED=FALSE\\n",
            self.script,
        )

    def test_mutation_and_protection_boundaries(self):
        self.assertIn('subprocess.Popen([sys.executable, str(generator), "--home", str(home), "--json"])', self.script)
        self.assertIn("manufacturer.json", self.script)
        self.assertIn("manufacturer_status.json", self.script)
        self.assertIn("generation-result.json", self.script)
        self.assertIn("generation-performance.txt", self.script)
        self.assertIn("CONFIG_SHA_BEFORE", self.script)
        self.assertNotIn("TRANSPORT_SHA_BEFORE", self.script)
        self.assertNotIn("TRANSPORT_STAGING_INVALID", self.script)
        self.assertNotIn("TRANSPORT_STAGING_CHANGED", self.script)
        for forbidden in ("systemctl", "crontab", "release/upgrade.sh", "ACTION9", "rm -r"):
            self.assertNotIn(forbidden, self.script)

    def test_private_atomic_evidence_and_artifact_validation(self):
        self.assertIn("/tmp/hioc-pe3-action8-XXXXXXXX", self.script)
        self.assertIn("EVIDENCE_DIR_CREATED=TRUE", self.script)
        self.assertIn('owned_mode_directory "$EVIDENCE_DIR" 700', self.script)
        self.assertNotIn("/tmp/hioc-pe3-production-validation-", self.script)
        self.assertNotIn("--evidence-dir", self.script)
        self.assertNotIn("hioc-pe3-action5-", self.script)
        self.assertNotIn("hioc-pe3-action5c-", self.script)
        self.assertIn("EVIDENCE_DIRECTORY_CREATE_FAILED EVIDENCE_PREPARATION FALSE", self.script)
        self.assertIn("EVIDENCE_PRE_DIRECTORY_CREATE_FAILED EVIDENCE_PREPARATION FALSE", self.script)
        self.assertIn('EVIDENCE_DIR=%s\\n\' "$EVIDENCE_DIR"', self.script)
        self.assertLess(
            self.script.index("verify_output_prestate || return 1"),
            self.script.index("prepare_evidence_directory || return 1"),
        )
        self.assertLess(
            self.script.index("prepare_evidence_directory || return 1"),
            self.script.index("run_generation || return 1"),
        )
        self.assertIn(".action8-result.XXXXXXXX", self.script)
        self.assertIn(".action8-performance.XXXXXXXX", self.script)
        self.assertIn('mv -fT -- "$TEMP_RESULT"', self.script)
        self.assertLess(
            self.script.index('mv -fT -- "$TEMP_PERFORMANCE"'),
            self.script.index('mv -fT -- "$TEMP_RESULT"'),
        )
        self.assertIn('[ "$(dirname -- "$EVIDENCE_DIR")" = /tmp ]', self.script)
        self.assertIn('sync -f "$EVIDENCE_DIR"', self.script)
        self.assertIn("validate_sidecar", self.script)
        self.assertIn("MANUFACTURER_TEMP_ARTIFACT_PRESENT", self.script)
        self.assertNotIn("| tee", self.script)

    def test_generator_failure_publishes_private_structured_evidence(self):
        for marker in (
            ".action8-stderr.XXXXXXXX", ".action8-failure.XXXXXXXX",
            "generation-failure.json", "GENERATOR_FAILURE_EVIDENCE=PASS",
            "GENERATOR_FAILURE_EVIDENCE_PUBLICATION_FAILED",
            '"observed_exit_code"', '"generator_error_code"',
            '"generator_launch_status"', '"GENERATOR_INVOCATION_FAILED"',
            '"stdout_structured_failure"', '"stderr_present"',
            '"manufacturer_sidecar"', '"manufacturer_status"',
            '"output_mutation"', '"rollback_recommended"',
        ):
            self.assertIn(marker, self.script)
        self.assertLess(
            self.script.index('mv -fT -- "$TEMP_PERFORMANCE"'),
            self.script.index('mv -fT -- "$TEMP_FAILURE"'),
        )
        self.assertIn("generation-failure.json", self.action8_flat)

    def test_generator_failure_raw_captures_are_private_and_removed(self):
        self.assertIn('2> "$TEMP_STDERR"', self.script)
        self.assertIn('rm -- "$TEMP_RESULT" "$TEMP_STDERR" "$TEMP_STARTED"', self.script)
        self.assertLess(
            self.script.index('rm -- "$TEMP_RESULT" "$TEMP_STDERR" "$TEMP_STARTED"'),
            self.script.index('mv -fT -- "$TEMP_FAILURE"'),
        )
        self.assertNotIn('cat "$TEMP_RESULT"', self.script)
        self.assertNotIn('cat "$TEMP_STDERR"', self.script)
        self.assertNotIn('printf "$TEMP_RESULT"', self.script)
        self.assertNotIn('printf "$TEMP_STDERR"', self.script)
        self.assertIn('path.stat().st_size > 65536', self.script)

    def test_generator_failure_privacy_is_allowlisted(self):
        self.assertIn("allowed_codes = {", self.script)
        self.assertNotIn('"generator_error_message"', self.script)
        self.assertNotIn('"stderr"', self.script)
        self.assertNotIn('"stdout"', self.script)
        self.assertIn('"generator_diagnostic"', self.script)

    def test_generator_failure_rollback_tracks_output_mutation(self):
        self.assertIn('rollback = sidecar_mutated or unsafe_output_state', self.script)
        self.assertIn('"STATUS_ONLY" if status_mutated else "NONE"', self.script)
        self.assertIn('raise SystemExit(10 if generator_failure and rollback else 0 if generator_failure else 12 if rollback else 11)', self.script)
        self.assertIn('10) FAILURE_KIND=GENERATOR; FAILURE_ROLLBACK=TRUE', self.script)
        self.assertRegex(
            self.script,
            r"fail_action8 VALIDATION_FAIL MANUFACTURER_GENERATOR_FAILED "
            r'MANUFACTURER_GENERATION "\$FAILURE_ROLLBACK"',
        )

    def test_generator_failure_does_not_publish_success_markers(self):
        failure_branch = self.script.split('if [ "$generation_rc" -ne 0 ]; then', 1)[1].split("fi", 1)[0]
        self.assertNotIn("MANUFACTURER_GENERATION=PASS", failure_branch)
        self.assertNotIn("generation-result.json", failure_branch)
        self.assertNotIn("ACTION8=COMPLETE", failure_branch)

    def test_generator_failure_embedded_python_compiles(self):
        function = self.script.split("publish_generator_failure_evidence() {", 1)[1]
        program = function.split("<<'PY'\n", 1)[1].split("\nPY\n", 1)[0]
        compile(program, "action8-generator-failure-evidence", "exec")

    def test_generator_failure_malformed_or_unexpected_diagnostic_is_unavailable(self):
        self.assertIn("except (OSError, UnicodeError, json.JSONDecodeError):", self.script)
        self.assertIn('value.get("result") != "FAIL"', self.script)
        self.assertIn('error.get("code") not in allowed_codes', self.script)
        self.assertIn('"generator_diagnostic": "RECOGNIZED" if diagnostic_code else "UNAVAILABLE"', self.script)

    def test_generator_failure_status_is_bounded_and_attributed(self):
        self.assertIn("def status_error(path):", self.script)
        self.assertIn('value.get("status") not in {"degraded", "unavailable", "error"}', self.script)
        self.assertIn("status_code = status_error(status)", self.script)
        self.assertIn("diagnostic_code = stdout_code or status_code", self.script)

    def test_generator_failure_evidence_permissions_are_private(self):
        self.assertIn('chmod 0600 "$TEMP_FAILURE"', self.script)
        self.assertIn('owned_mode_file "$TEMP_FAILURE" 600', self.script)
        self.assertIn('owned_mode_directory "$EVIDENCE_DIR" 700', self.script)

    def test_generator_failure_cleanup_uncertainty_fails_closed(self):
        cleanup = 'rm -- "$TEMP_RESULT" "$TEMP_STDERR" "$TEMP_STARTED" >/dev/null 2>&1 || { FAILURE_ROLLBACK=TRUE; return 20; }'
        self.assertIn(cleanup, self.script)
        self.assertIn("GENERATOR_FAILURE_EVIDENCE_PUBLICATION_FAILED", self.script)
        self.assertIn("EVIDENCE_PUBLICATION", self.script)

    def test_generator_failure_result_last_is_distinct_from_success_result(self):
        self.assertLess(
            self.script.index('mv -fT -- "$TEMP_PERFORMANCE" "$EVIDENCE_DIR/generation-performance.txt"'),
            self.script.index('mv -fT -- "$TEMP_FAILURE" "$EVIDENCE_DIR/generation-failure.json"'),
        )
        self.assertIn('mv -fT -- "$TEMP_RESULT" "$EVIDENCE_DIR/generation-result.json"', self.script)
        self.assertNotEqual("generation-failure.json", "generation-result.json")

    def test_generation_performance_uses_governed_python_not_external_time(self):
        self.assertNotIn("/usr/bin/time", self.script)
        self.assertIn("time.perf_counter()", self.script)
        self.assertIn("resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss", self.script)
        self.assertIn("manufacturer_generation_measurement_status", self.script)
        self.assertIn("subprocess.Popen", self.script)

    def test_generator_launch_status_is_confirmed_only_after_child_creation(self):
        self.assertNotIn('"generator_started"', self.script)
        self.assertIn('"generator_launch_status": "CONFIRMED" if launch_confirmed else "UNCONFIRMED"', self.script)
        self.assertLess(self.script.index("subprocess.Popen"), self.script.index('started.write_text("TRUE\\n"'))
        self.assertIn("GENERATOR_INVOCATION_FAILED", self.script)
        self.assertIn("MANUFACTURER_INVOCATION", self.script)

    def test_performance_launcher_embedded_python_compiles(self):
        function = self.script.split("run_generation() {", 1)[1]
        program = function.split('2> "$TEMP_STDERR"\n', 1)[1].split("\nPY\n", 1)[0]
        compile(program, "action8-performance-launcher", "exec")

    def test_transport_staging_absence_is_accepted_after_installation_and_activation(self):
        self.assertNotIn("/tmp/hioc-pe3-dataset-transfer-", self.script)
        self.assertNotIn("TRANSPORT_STAGE", self.script)
        self.assertIn("CONFIGURATION_IDENTITY=PASS", self.script)
        self.assertIn("DATASET_IDENTITY=PASS", self.script)

    def test_present_transport_staging_is_not_consumed_recreated_or_cleaned(self):
        for forbidden in ("TRANSPORT_STAGE", "dataset-transfer", "scp ", "rsync ", "mkdir", "rmdir"):
            self.assertNotIn(forbidden, self.script)
        self.assertNotRegex(self.script, r"(?m)^\s*rm\s+-r")

    def test_child_script_failure_preserves_parent_shell(self):
        shell = os.environ.get("HIOC_TEST_SHELL") or shutil.which("bash")
        if not shell:
            self.skipTest("Bash is required")
        path = str(SCRIPT).replace("\\", "/")
        if re.match(r"^[A-Za-z]:/", path):
            path = "/" + path[0].lower() + path[2:]
        result = subprocess.run(
            [shell, "-c", f". '{path}'; printf 'PARENT_SHELL_ALIVE=TRUE\\n'"],
            text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("ERROR_CODE=INVALID_ARGUMENTS", result.stdout)
        self.assertIn("PARENT_SHELL_ALIVE=TRUE", result.stdout)
        self.assertNotRegex(self.script, r"(?m)^\s*(?:set\s+-[^\n]*e|exit(?:\s|$))")

    def test_operator_supplied_evidence_directory_is_rejected(self):
        shell = os.environ.get("HIOC_TEST_SHELL") or shutil.which("bash")
        if not shell:
            self.skipTest("Bash is required")
        path = str(SCRIPT).replace("\\", "/")
        if re.match(r"^[A-Za-z]:/", path):
            path = "/" + path[0].lower() + path[2:]
        result = subprocess.run(
            [shell, path, "--governance-commit", "0" * 40,
             "--evidence-dir", "/tmp/hioc-pe3-action5c-anything"],
            text=True, capture_output=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ERROR_CODE=INVALID_ARGUMENTS", result.stdout)
        self.assertIn("FAILURE_STAGE=INPUT_VALIDATION", result.stdout)
        self.assertNotIn("TARGET_IDENTITY=PASS", result.stdout)

    def test_bootstrap_blob_matches_unchanged_diagnostic_retention_wrapper(self):
        committed_bootstrap_blob = re.search(r"SCRIPT_BLOB=([0-9a-f]{40})", self.bootstrap).group(1)
        current_blob = subprocess.run(
            ["git", "hash-object", str(SCRIPT)], cwd=ROOT,
            text=True, capture_output=True, check=True,
        ).stdout.strip()
        self.assertEqual(current_blob, committed_bootstrap_blob)
        self.assertEqual(current_blob, "b8c38607325acaf6ab3a02878c834e05e54bea56")
        self.assertEqual(
            hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),
            "e42aa964ba822176e9b354ccbf9a726623361f236455bd16b5c29a301de2cb5a",
        )


if __name__ == "__main__":
    unittest.main()
