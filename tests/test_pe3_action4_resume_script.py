import os
import hashlib
import pathlib
import shutil
import subprocess
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "hioc-pe3-action4-resume-permissions.sh"


class PE3Action4ResumeScriptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = SCRIPT.read_text(encoding="utf-8")

    def test_frozen_paths_and_artifact_identity(self):
        for value in (
            "/home/jazofv1/hioc-release-source",
            "/tmp/hioc-pe3-dataset-transfer-PJ5qPbRS",
            "8652642", "1338", "53581",
            "81f147cc57768c5797c4ad73a8c0369001bbdcbfe1548e71d3702c8c7f81e0e1",
            "10c8097c0a4ec6e8cc4cd3dc61afc7f368057f4ef4b6534df9f6dd31634a4ac4",
        ):
            self.assertIn(value, self.text)

    def test_documented_script_sha256_and_git_blob(self):
        runbook = (ROOT / "docs" / "PE3_MANUFACTURER_PRODUCTION_RUNBOOK.md").read_text(encoding="utf-8")
        digest = hashlib.sha256(SCRIPT.read_bytes()).hexdigest()
        self.assertEqual(digest, "31561b166d9d272c18767789e56dc126a107f7ce42b21ac93f81d37737e003a6")
        self.assertIn(digest, runbook)
        git = shutil.which("git")
        if git:
            result = subprocess.run(
                [git, "hash-object", "--path=tools/hioc-pe3-action4-resume-permissions.sh", str(SCRIPT)],
                cwd=ROOT, text=True, capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), "0602d9f460bf127bac4be953686fad1c0700c14e")
        self.assertIn("0602d9f460bf127bac4be953686fad1c0700c14e", runbook)

    def test_source_and_script_identity_are_governed(self):
        for token in (
            "branch --show-current", "rev-parse HEAD", "rev-parse origin/main",
            "status --porcelain", "merge-base --is-ancestor", "diff --quiet",
            'rev-parse "$GOVERNANCE_COMMIT:$SCRIPT_PATH"', "hash-object --path=",
            "ACTION4_SCRIPT_IDENTITY_MISMATCH",
        ):
            self.assertIn(token, self.text)

    def test_prechecks_precede_chmod_and_only_exact_targets_are_eligible(self):
        pre = self.text.index("verify_stage_before_normalization()")
        exact = self.text.index("exact_stage_entries ||", pre)
        owner = self.text.index('regular_owned_file "$DB"', pre)
        size = self.text.index("STAGING_SIZE_DRIFT", pre)
        digest = self.text.index("STAGING_HASH_DRIFT", pre)
        mode = self.text.index("UNSUPPORTED_PRE_NORMALIZATION_MODE", pre)
        chmod = self.text.index('chmod 0600 -- "$DB"')
        self.assertLess(exact, owner)
        self.assertLess(owner, size)
        self.assertLess(size, digest)
        self.assertLess(digest, mode)
        self.assertLess(mode, chmod)
        self.assertIn('chmod 0600 -- "$DB"', self.text)
        self.assertIn('chmod 0600 -- "$MF"', self.text)
        self.assertNotRegex(self.text, r"chmod\s+(?:-R|--recursive)")

    def test_0600_is_noop_0644_is_normalized_and_other_modes_fail(self):
        self.assertIn('if [ "$(stat -c %a "$DB" 2>/dev/null)" = 644 ]', self.text)
        self.assertIn('if [ "$(stat -c %a "$MF" 2>/dev/null)" = 644 ]', self.text)
        self.assertIn('[ "$mode" = 600 ] || [ "$mode" = 644 ]', self.text)
        self.assertIn("UNSUPPORTED_PRE_NORMALIZATION_MODE", self.text)

    def test_post_normalization_rechecks_every_invariant(self):
        start = self.text.index("verify_stage_after_normalization()")
        end = self.text.index("validate_manufacturer()", start)
        post = self.text[start:end]
        for token in (
            "stage_directory_valid", "exact_stage_entries", 'regular_owned_file "$DB"',
            'regular_owned_file "$MF"', 'stat -c %a "$DB"', 'stat -c %a "$MF"',
            'stat -c %s "$DB"', 'stat -c %s "$MF"', 'sha256sum "$DB"',
            'sha256sum "$MF"', "POST_NORMALIZATION_IDENTITY=PASS",
        ):
            self.assertIn(token, post)

    def test_failure_codes_cover_required_stages(self):
        for code in (
            "SOURCE_IDENTITY_DRIFT", "STAGING_IDENTITY_DRIFT",
            "UNSUPPORTED_PRE_NORMALIZATION_MODE", "STAGING_CHMOD_FAILED",
            "POST_NORMALIZATION_OWNER_OR_TYPE_DRIFT", "MANUFACTURER_VALIDATOR_FAILED",
            "MANUFACTURER_PRIVACY_CHECK_FAILED", "MANUFACTURER_RECORD_COUNT_MISMATCH",
        ):
            self.assertIn(code, self.text)

    def test_validator_contract_is_explicit_and_read_only(self):
        self.assertIn('d.get("result")=="PASS"', self.text)
        self.assertIn('d.get("privacy_safe") is True', self.text)
        self.assertIn('d.get("record_count")==int(sys.argv[2])', self.text)
        self.assertIn("hioc-validate-manufacturer.py", self.text)
        self.assertNotIn("hioc-generate-manufacturer.py", self.text)
        self.assertNotIn("release/upgrade.sh", self.text)
        for forbidden in ("ssh ", "scp ", "rsync ", "Action 5", "systemctl", "install "):
            self.assertNotIn(forbidden, self.text)

    def test_pass_evidence_has_each_distinct_barrier(self):
        for marker in (
            "SOURCE_IDENTITY_RECHECK=PASS", "STAGING_IDENTITY_RECHECK=PASS",
            "STAGING_PERMISSION_NORMALIZATION=PASS", "POST_NORMALIZATION_IDENTITY=PASS",
            "MANUFACTURER_VALIDATION=PASS", "ACTION4=COMPLETE", "RESULT=PASS",
        ):
            self.assertEqual(self.text.count(marker), 1)

    def test_parent_shell_survives_harmless_failure_and_later_stages_do_not_run(self):
        shell = os.environ.get("HIOC_TEST_SHELL") or shutil.which("bash")
        if not shell:
            self.skipTest("Bash is required")
        invocation = (
            f'"{pathlib.Path(shell).as_posix()}" "{SCRIPT.as_posix()}" --governance-commit '
            f"{'0' * 40}; printf 'PARENT_SHELL_ALIVE=TRUE\\n'"
        )
        result = subprocess.run([shell, "-c", invocation], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("RESULT=INPUT_OR_PRECONDITION_ERROR", result.stdout)
        self.assertIn("PARENT_SHELL_ALIVE=TRUE", result.stdout)
        self.assertNotIn("STAGING_PERMISSION_NORMALIZATION=PASS", result.stdout)
        self.assertNotIn("MANUFACTURER_VALIDATION=PASS", result.stdout)
        self.assertNotRegex(self.text, r"(?m)^\s*(?:set -e|exit(?:\s|$))")


if __name__ == "__main__":
    unittest.main()
