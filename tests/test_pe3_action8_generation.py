import os
import pathlib
import re
import shutil
import subprocess
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "hioc-pe3-action8-generate.sh"
RUNBOOK = ROOT / "docs" / "PE3_MANUFACTURER_PRODUCTION_RUNBOOK.md"


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
        self.assertIn("91360c1f83c890dd340a9a6390bf462cb0f95731", self.bootstrap)
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
            "53581", "/tmp/hioc-pe3-dataset-transfer-PJ5qPbRS",
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
            "verify_transport_and_output_prestate", "prepare_evidence_directory",
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
        self.assertIn('python3 "$RUNTIME/$GENERATOR_REL" --home "$RUNTIME" --json', self.script)
        self.assertIn("manufacturer.json", self.script)
        self.assertIn("manufacturer_status.json", self.script)
        self.assertIn("generation-result.json", self.script)
        self.assertIn("generation-performance.txt", self.script)
        self.assertIn("CONFIG_SHA_BEFORE", self.script)
        self.assertIn("TRANSPORT_SHA_BEFORE", self.script)
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
            self.script.index("verify_transport_and_output_prestate || return 1"),
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

    def test_previous_bootstrap_blob_is_explicitly_stale(self):
        committed_bootstrap_blob = re.search(r"SCRIPT_BLOB=([0-9a-f]{40})", self.bootstrap).group(1)
        current_blob = subprocess.run(
            ["git", "hash-object", str(SCRIPT)], cwd=ROOT,
            text=True, capture_output=True, check=True,
        ).stdout.strip()
        self.assertNotEqual(current_blob, committed_bootstrap_blob)
        self.assertIn("new synchronization/script-identity bootstrap", self.action8_flat)


if __name__ == "__main__":
    unittest.main()
