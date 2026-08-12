import pathlib
import re
import os
import shutil
import subprocess
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
RUNBOOK = ROOT / "docs" / "PE3_MANUFACTURER_PRODUCTION_RUNBOOK.md"
MASTER = ROOT / "docs" / "HIOC_MASTER_PLAN.md"


class PE3ProductionRunbookSequencingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.runbook = RUNBOOK.read_text(encoding="utf-8")
        cls.master = MASTER.read_text(encoding="utf-8")
        cls.action3 = cls.runbook.split("## Action 3", 1)[1].split("## Action 4", 1)[0]
        cls.action4 = cls.runbook.split("## Action 4", 1)[1].split("## Action 5", 1)[0]
        cls.resume = cls.action4.split("### Action 4 resume", 1)[1]

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
        action = re.search(r"```bash\n(.*?)```", self.resume, re.DOTALL).group(1)
        owner = action.index('stat -c %U:%G "$p"')
        size = action.index('ARTIFACT_SIZE_MISMATCH')
        digest = action.index('ARTIFACT_HASH_MISMATCH')
        mode_gate = action.index('STAGING_MODE_NOT_NORMALIZABLE')
        chmod = action.index('chmod 0600 -- "$DB" "$MF"')
        post_mode = action.index('STAGING_MODE_NORMALIZATION_FAILED')
        unchanged = action.index('CONTENT_CHANGED_DURING_CHMOD')
        validator = action.index('HIOC_HOME="$SOURCE" python3')
        self.assertLess(owner, size)
        self.assertLess(size, digest)
        self.assertLess(digest, mode_gate)
        self.assertLess(mode_gate, chmod)
        self.assertLess(chmod, post_mode)
        self.assertLess(post_mode, unchanged)
        self.assertLess(unchanged, validator)
        self.assertIn('manufacturer-db.json,manufacturer-db.manifest.json', action)
        self.assertNotRegex(action, r"chmod\s+(?:-R|--recursive)")
        self.assertEqual(action.count('chmod 0600 -- "$DB" "$MF"'), 1)

    def test_permission_contract_and_resume_are_fail_closed(self):
        implementation = (ROOT / "pi4" / "lib" / "hioc" / "manufacturer.py").read_text(encoding="utf-8")
        validator = (ROOT / "pi4" / "bin" / "hioc-validate-manufacturer.py").read_text(encoding="utf-8")
        self.assertIn("stat.S_IMODE(info.st_mode) & ~0o600", implementation)
        self.assertIn("stat.S_IMODE(path.stat().st_mode)&~0o600", validator)
        self.assertIn('mode" = 600 ] || [ "$mode" = 644', self.resume)
        for marker in ("STAGING_CONTENTS_INVALID", "STAGING_FILE_IDENTITY_INVALID",
                       "ARTIFACT_SIZE_MISMATCH", "ARTIFACT_HASH_MISMATCH",
                       "STAGING_MODE_NOT_NORMALIZABLE"):
            self.assertIn(marker, self.resume)
        self.assertIn("ACTION4_RESUME=PASS", self.resume)
        self.assertNotIn("release/upgrade.sh", self.resume)

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


if __name__ == "__main__":
    unittest.main()
