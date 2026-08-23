import pathlib
import re
import os
import shutil
import subprocess
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
RUNBOOK = ROOT / "docs" / "PE3_MANUFACTURER_PRODUCTION_RUNBOOK.md"
MASTER = ROOT / "docs" / "HIOC_MASTER_PLAN.md"
ACTION4_SCRIPT = ROOT / "tools" / "hioc-pe3-action4-resume-permissions.sh"
ACTION5_SCRIPT = ROOT / "tools" / "hioc-pe3-action5-deploy.sh"


class PE3ProductionRunbookSequencingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.runbook = RUNBOOK.read_text(encoding="utf-8")
        cls.master = MASTER.read_text(encoding="utf-8")
        cls.action3 = cls.runbook.split("## Action 3", 1)[1].split("## Action 4", 1)[0]
        cls.action4 = cls.runbook.split("## Action 4", 1)[1].split("## Action 5", 1)[0]
        cls.resume = cls.action4.split("### Action 4A", 1)[1]
        cls.resume_blocks = re.findall(r"```bash\n(.*?)```", cls.resume, re.DOTALL)
        cls.resume_block = cls.resume_blocks[0]
        cls.action4b_block = cls.resume_blocks[1]
        cls.resume_script = ACTION4_SCRIPT.read_text(encoding="utf-8")
        cls.action5 = cls.runbook.split("## Action 5", 1)[1].split("## Action 6", 1)[0]
        cls.action5_script = ACTION5_SCRIPT.read_text(encoding="utf-8")

    def test_action3_is_staging_only(self):
        self.assertIn("STAGING_VERIFICATION=PASS", self.action3)
        self.assertNotIn("IMPLEMENTATION_COMMIT=", self.action3)
        self.assertNotIn("hioc-validate-manufacturer.py", self.action3)
        self.assertNotIn("git -C", self.action3)

    def test_action4_synchronizes_before_identity_and_validator(self):
        fetch = self.action4.index('git -C "$SOURCE" fetch origin')
        synchronize = self.action4.index('git -C "$SOURCE" merge --ff-only origin/main')
        commit = self.action4.index('cat-file -e "$IMPLEMENTATION_COMMIT^{commit}"')
        identity = self.action4.index('diff --quiet "$IMPLEMENTATION_COMMIT"')
        validator = self.action4.index("hioc-validate-manufacturer.py")
        self.assertLess(fetch, synchronize)
        self.assertLess(synchronize, commit)
        self.assertLess(commit, identity)
        self.assertLess(identity, validator)

    def test_operator_failures_preserve_interactive_shell(self):
        for action in (self.action3, self.action4):
            block = re.search(r"```bash\n(.*?)```", action, re.DOTALL).group(1)
            self.assertNotIn("set -e", block)
            self.assertNotRegex(block, r"(?m)^\s*exit(?:\s|$)")
            self.assertIn("RESULT=INPUT_OR_PRECONDITION_ERROR", block)
            self.assertIn("ERROR_CODE=%s", block)
            self.assertIn("FAILURE_STAGE=%s", block)
            self.assertRegex(block, r"hioc_pe3_action[34]\(\)")

    def test_accepted_staging_evidence_and_resume_point_are_preserved(self):
        for marker in (
            "/tmp/hioc-pe3-dataset-transfer-PJ5qPbRS",
            "target identity\nPASS",
            "owner/mode PASS",
            "regular/non-symlink checks\nPASS",
            "byte sizes PASS",
            "SHA-256 identities PASS",
            "Do not repeat it for this deployment unless staging changes",
        ):
            self.assertIn(marker, self.action3)
        self.assertIn("STOPPED — REPOSITORY-SEQUENCING PRECONDITION", self.action3)
        self.assertIn("restart point is Action 4", self.master)

    def test_action4_cannot_deploy(self):
        self.assertIn("required barrier before Action 5 can deploy code", self.action4)
        for forbidden in ("release/upgrade.sh", "HIOC_INSTALL_DIR", "CODE_DEPLOYMENT=PASS"):
            self.assertNotIn(forbidden, self.action4)
        self.assertIn("IMPLEMENTATION_VALIDATION=PASS", self.action4)
        self.assertIn("STAGING_REVALIDATION=PASS", self.action4)
        self.assertIn("RESULT=VALIDATION_FAIL", self.action4)
        self.assertIn("validation_fail MANUFACTURER_VALIDATION_FAILED", self.action4)

    def test_permission_normalization_is_identity_gated_and_exact(self):
        action = self.resume_script
        owner = action.index('regular_owned_file "$DB"')
        size = action.index('STAGING_SIZE_DRIFT')
        digest = action.index('STAGING_HASH_DRIFT')
        mode_gate = action.index('UNSUPPORTED_PRE_NORMALIZATION_MODE')
        chmod = action.index('chmod 0600 -- "$DB"')
        post_mode = action.index('POST_NORMALIZATION_MODE_DRIFT')
        unchanged = action.index('POST_NORMALIZATION_HASH_DRIFT')
        validator = action.index('validate_manufacturer || return 1')
        self.assertLess(owner, size)
        self.assertLess(size, digest)
        self.assertLess(digest, mode_gate)
        self.assertLess(mode_gate, chmod)
        self.assertLess(chmod, post_mode)
        self.assertLess(post_mode, unchanged)
        self.assertLess(unchanged, validator)
        self.assertIn('manufacturer-db.json,manufacturer-db.manifest.json', action)
        self.assertNotRegex(action, r"chmod\s+(?:-R|--recursive)")
        self.assertEqual(action.count('chmod 0600 -- "$DB"'), 1)
        self.assertEqual(action.count('chmod 0600 -- "$MF"'), 1)

    def test_permission_contract_and_resume_are_fail_closed(self):
        implementation = (ROOT / "pi4" / "lib" / "hioc" / "manufacturer.py").read_text(encoding="utf-8")
        validator = (ROOT / "pi4" / "bin" / "hioc-validate-manufacturer.py").read_text(encoding="utf-8")
        self.assertIn("stat.S_IMODE(info.st_mode) & ~0o600", implementation)
        self.assertIn("permission_mode_is_valid(stat.S_IMODE(path.stat().st_mode),artifact_class)", validator)
        self.assertIn('artifact_class == "private_manufacturer"', validator)
        self.assertIn('artifact_class == "inventory_input"', validator)
        self.assertIn('mode" = 600 ] || [ "$mode" = 644', self.resume_script)
        for marker in ("STAGING_EXTRA_OR_MISSING_ENTRY", "STAGING_OWNER_OR_TYPE_DRIFT",
                       "STAGING_SIZE_DRIFT", "STAGING_HASH_DRIFT",
                       "UNSUPPORTED_PRE_NORMALIZATION_MODE"):
            self.assertIn(marker, self.resume_script)
        self.assertIn("ACTION4=COMPLETE", self.resume_script)
        self.assertNotIn("release/upgrade.sh", self.resume)

    def test_resume_is_repository_controlled(self):
        self.assertIn("tools/hioc-pe3-action4-resume-permissions.sh", self.resume)
        self.assertIn('SCRIPT_REL=tools/hioc-pe3-action4-resume-permissions.sh', self.resume)
        self.assertIn('bash /home/jazofv1/hioc-release-source/tools/hioc-pe3-action4-resume-permissions.sh', self.action4b_block)
        self.assertNotIn("hioc_pe3_action4_resume_permissions()", self.resume)

    def test_action4a_synchronizes_and_stops_after_identity(self):
        action = self.resume_block
        clean = action.index('status --porcelain')
        fetch = action.index('fetch origin')
        ancestry = action.index('merge-base --is-ancestor HEAD origin/main')
        fast_forward = action.index('merge --ff-only origin/main')
        post = action.index('POST_SYNC_HEAD_MISMATCH')
        present = action.index('ACTION4_RESUME_SCRIPT_MISSING')
        commit_blob = action.index('ACTION4_SCRIPT_GIT_IDENTITY_MISMATCH')
        worktree_blob = action.index('ACTION4_SCRIPT_WORKTREE_IDENTITY_MISMATCH')
        complete = action.index('ACTION4A=COMPLETE')
        self.assertLess(clean, fetch)
        self.assertLess(fetch, ancestry)
        self.assertLess(ancestry, fast_forward)
        self.assertLess(fast_forward, post)
        self.assertLess(post, present)
        self.assertLess(present, commit_blob)
        self.assertLess(commit_blob, worktree_blob)
        self.assertLess(worktree_blob, complete)
        self.assertNotIn('bash "$SCRIPT"', action)
        self.assertNotIn("hioc-validate-manufacturer.py", action)
        self.assertNotIn("chmod", action)

    def test_resume_sync_fails_closed_and_preserves_staging(self):
        action = self.resume_block
        for code in (
            "SOURCE_REPOSITORY_DIRTY", "ACTIVE_GIT_OPERATION",
            "NON_FAST_FORWARD_SOURCE", "FAST_FORWARD_FAILED",
            "ACTION4_RESUME_SCRIPT_MISSING", "ACTION4_SCRIPT_GIT_IDENTITY_MISMATCH",
            "ACTION4_SCRIPT_WORKTREE_IDENTITY_MISMATCH",
        ):
            self.assertIn(code, action)
        self.assertNotIn("/tmp/hioc-pe3-dataset-transfer-PJ5qPbRS", action)
        self.assertNotIn("chmod", action)
        for forbidden in ("reset", "--force", "stash", "release/upgrade.sh", "Action 5"):
            self.assertNotIn(forbidden, action)

    def test_resume_prerequisite_preserves_parent_shell(self):
        shell = os.environ.get("HIOC_TEST_SHELL") or shutil.which("bash")
        if not shell:
            self.skipTest("Bash is required")
        result = subprocess.run(
            [shell, "-c", self.resume_block + "\nprintf 'PARENT_SHELL_ALIVE=TRUE\\n'"],
            text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("RESULT=INPUT_OR_PRECONDITION_ERROR", result.stdout)
        self.assertIn("PARENT_SHELL_ALIVE=TRUE", result.stdout)
        self.assertNotIn("TARGET_SYNCHRONIZATION=PASS", result.stdout)
        self.assertNotRegex(action := self.resume_block, r"(?m)^\s*(?:set -e|exit(?:\s|$))")

    def test_action4a_pass_contract_is_closed_and_action4b_is_separate(self):
        for marker in (
            "TARGET_IDENTITY=PASS", "REPOSITORY_PRECONDITION=PASS",
            "REPOSITORY_SYNCHRONIZATION=PASS", "SYNCHRONIZED_HEAD_IDENTITY=PASS",
            "ACTION4_RESUME_SCRIPT_AVAILABILITY=PASS",
            "ACTION4_RESUME_SCRIPT_IDENTITY=PASS", "ACTION4A=COMPLETE",
            "RESULT=PASS",
        ):
            self.assertEqual(self.resume_block.count(marker), 1)
        self.assertIn("requires separate authorization", self.resume)
        self.assertIn("ACTION4=COMPLETE", self.resume_script)
        self.assertNotIn("ACTION4=COMPLETE", self.resume_block)
        self.assertNotIn("release/upgrade.sh", self.action4b_block)

    def test_action3_and_action4_bash_parse(self):
        shell = os.environ.get("HIOC_TEST_SHELL") or shutil.which("bash")
        if not shell:
            self.skipTest("Bash is required")
        for action in (self.action3, self.action4):
            for block in re.findall(r"```bash\n(.*?)```", action, re.DOTALL):
                result = subprocess.run(
                    [shell, "-n"], input=block, text=True, capture_output=True
                )
                self.assertEqual(result.returncode, 0, result.stderr)
        result = subprocess.run(
            [shell, "-n", str(ACTION4_SCRIPT)], text=True, capture_output=True
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_action5_is_governed_and_does_not_chain_action6(self):
        self.assertIn("tools/hioc-pe3-action5-deploy.sh", self.action5)
        self.assertNotIn("set -euo pipefail", self.action5)
        self.assertIn("ACTION5=COMPLETE", self.action5_script)
        self.assertNotIn("ACTION6", self.action5_script)
        self.assertNotIn("manufacturer-db.json", self.action5_script)

    def test_action5_bash_parses(self):
        shell = os.environ.get("HIOC_TEST_SHELL") or shutil.which("bash")
        if not shell:
            self.skipTest("Bash is required")
        result = subprocess.run([shell, "-n", str(ACTION5_SCRIPT)], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
