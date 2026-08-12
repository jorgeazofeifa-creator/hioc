import os
import pathlib
import re
import shutil
import subprocess
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
RUNBOOK = ROOT / "docs" / "PE3_MANUFACTURER_PRODUCTION_RUNBOOK.md"


class PE3Action5CBootstrapContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.runbook = RUNBOOK.read_text(encoding="utf-8")
        section = cls.runbook.split("#### Action 5C-A", 1)[1]
        cls.action5c_a, remainder = section.split("#### Action 5C-B", 1)
        cls.action5c_b = remainder.split("## Action 6", 1)[0]
        cls.block = re.search(r"```bash\n(.*?)```", cls.action5c_a, re.DOTALL).group(1)

    def test_bootstrap_is_inline_and_targets_the_canonical_script(self):
        self.assertIn("hioc_pe3_action5c_a_sync()", self.block)
        self.assertIn("tools/hioc-pe3-action5c-revalidate.sh", self.block)
        self.assertIn("da47aa4a3d0346432332fc42f4111a956fd8e1bd", self.block)
        self.assertNotIn("bash \"$SCRIPT\"", self.block)

    def test_scope_excludes_runtime_staging_backup_and_later_actions(self):
        for forbidden in (
            "/home/jazofv1/hioc\n", "release/upgrade.sh", "release/rollback.sh",
            "release/validate.sh", "validate_pi4.sh", "backups/",
            "manufacturer-db.json", "MANUFACTURER_DB_PATH", "ACTION5=COMPLETE",
            "ACTION6", "Action 6", "hioc-pe3-action5c-revalidate.sh --",
        ):
            self.assertNotIn(forbidden, self.block)

    def test_order_enforces_clean_fast_forward_then_script_identity(self):
        positions = [
            self.block.index("status --porcelain"),
            self.block.index("fetch origin"),
            self.block.index("rev-parse origin/main"),
            self.block.index("merge-base --is-ancestor HEAD origin/main"),
            self.block.index("merge --ff-only origin/main"),
            self.block.index("POST_SYNC_HEAD_MISMATCH"),
            self.block.index("ACTION5C_SCRIPT_MISSING"),
            self.block.index("ACTION5C_SCRIPT_GIT_IDENTITY_MISMATCH"),
            self.block.index("ACTION5C_SCRIPT_WORKTREE_IDENTITY_MISMATCH"),
        ]
        self.assertEqual(positions, sorted(positions))

    def test_failure_contract_is_complete(self):
        for code in (
            "WRONG_TARGET", "SOURCE_REPOSITORY_MISSING", "WRONG_BRANCH",
            "SOURCE_REPOSITORY_DIRTY", "ACTIVE_GIT_OPERATION", "GIT_FETCH_FAILED",
            "GOVERNANCE_COMMIT_MISMATCH", "NON_FAST_FORWARD_SOURCE",
            "FAST_FORWARD_FAILED", "POST_SYNC_HEAD_MISMATCH",
            "POST_SYNC_REPOSITORY_DIRTY", "ACTION5C_SCRIPT_MISSING",
            "ACTION5C_SCRIPT_NOT_REGULAR",
            "ACTION5C_SCRIPT_GIT_IDENTITY_MISMATCH",
            "ACTION5C_SCRIPT_WORKTREE_IDENTITY_MISMATCH",
        ):
            self.assertIn(code, self.block)
        for stage in ("TARGET_SYNCHRONIZATION", "SCRIPT_AVAILABILITY", "SCRIPT_IDENTITY"):
            self.assertIn(stage, self.block)
        for marker in ("RESULT=INPUT_OR_PRECONDITION_ERROR", "ERROR_CODE=%s", "FAILURE_STAGE=%s"):
            self.assertIn(marker, self.block)

    def test_pass_contract_is_exact_and_unique(self):
        markers = (
            "TARGET_IDENTITY=PASS", "REPOSITORY_PRECONDITION=PASS",
            "REPOSITORY_SYNCHRONIZATION=PASS", "SYNCHRONIZED_HEAD_IDENTITY=PASS",
            "ACTION5C_SCRIPT_AVAILABILITY=PASS", "ACTION5C_SCRIPT_IDENTITY=PASS",
            "ACTION5C_A=COMPLETE", "RESULT=PASS",
        )
        for marker in markers:
            self.assertEqual(self.block.count(marker), 1)

    def test_parent_shell_survives_failure_and_later_steps_do_not_run(self):
        shell = os.environ.get("HIOC_TEST_SHELL") or shutil.which("bash")
        if not shell:
            self.skipTest("Bash is required")
        result = subprocess.run(
            [shell, "-c", self.block + "\nprintf 'PARENT_SHELL_ALIVE=TRUE\\n'"],
            text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("RESULT=INPUT_OR_PRECONDITION_ERROR", result.stdout)
        self.assertIn("PARENT_SHELL_ALIVE=TRUE", result.stdout)
        self.assertNotIn("REPOSITORY_SYNCHRONIZATION=PASS", result.stdout)
        self.assertNotRegex(self.block, r"(?m)^\s*(?:set\s+-[^\n]*e|exit(?:\s|$))")

    def test_action5c_b_requires_review_and_separate_authorization(self):
        self.assertIn("reviewed Action 5C-A PASS and separate authorization", self.action5c_b)
        self.assertIn("No Action 5C-B invocation is prepared", self.action5c_b)
        self.assertIn("/home/jazofv1/hioc/backups/release-upgrade-20260812-133550", self.action5c_b)
        self.assertNotRegex(self.action5c_b, r"```bash")

    def test_governance_rule_covers_read_only_scripts(self):
        operations = (ROOT / "docs" / "OPERATIONS.md").read_text(encoding="utf-8")
        decisions = (ROOT / "DECISIONS.md").read_text(encoding="utf-8")
        self.assertIn("This applies equally to read-only closure and\nrevalidation scripts", operations)
        self.assertIn("including scripts whose eventual operation is\nread-only", decisions)


if __name__ == "__main__":
    unittest.main()
