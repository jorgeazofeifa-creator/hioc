import os
import pathlib
import re
import shutil
import subprocess
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "hioc-pe3-action7-activate.sh"
RUNBOOK = ROOT / "docs" / "PE3_MANUFACTURER_PRODUCTION_RUNBOOK.md"


class PE3Action7ActivationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = SCRIPT.read_text(encoding="utf-8")
        cls.runbook = RUNBOOK.read_text(encoding="utf-8")
        cls.action7 = cls.runbook.split("## Action 7", 1)[1].split("## Action 8", 1)[0]
        cls.action7a = cls.action7.split("### Action 7-A", 1)[1].split("### Action 7-B", 1)[0]
        cls.bootstrap = re.search(r"```bash\n(.*?)```", cls.action7a, re.DOTALL).group(1)
        cls.action7b = cls.action7.split("### Action 7-B", 1)[1]

    def test_historical_inline_procedure_is_retired(self):
        self.assertIn("ACTION 7 OPERATOR-SAFETY AND EVIDENCE CONTRACT DEFECT", self.action7)
        self.assertNotIn("EVIDENCE_DIR='/tmp/hioc-pe3-production-validation-XXXXXXXX'", self.action7)
        self.assertNotIn("CONFIG_RESULT=PASS_ACTIVATED", self.action7)

    def test_bootstrap_is_sync_and_identity_only(self):
        self.assertIn("hioc_pe3_action7_a_sync()", self.bootstrap)
        self.assertIn("tools/hioc-pe3-action7-activate.sh", self.bootstrap)
        for forbidden in (
            'bash "$SCRIPT"', "MANUFACTURER_DB_PATH", "manufacturer-db.json",
            "/home/jazofv1/hioc/config", "ACTION7=COMPLETE", "Action 8",
        ):
            self.assertNotIn(forbidden, self.bootstrap)
        for marker in (
            "TARGET_IDENTITY=PASS", "REPOSITORY_PRECONDITION=PASS",
            "REPOSITORY_SYNCHRONIZATION=PASS", "SYNCHRONIZED_HEAD_IDENTITY=PASS",
            "ACTION7_SCRIPT_AVAILABILITY=PASS", "ACTION7_SCRIPT_IDENTITY=PASS",
            "ACTION7_A=COMPLETE", "RESULT=PASS",
        ):
            self.assertEqual(self.bootstrap.count(marker), 1)

    def test_bootstrap_parent_shell_survives(self):
        shell = os.environ.get("HIOC_TEST_SHELL") or shutil.which("bash")
        if not shell:
            self.skipTest("Bash is required")
        result = subprocess.run(
            [shell, "-c", self.bootstrap + "\nprintf 'PARENT_SHELL_ALIVE=TRUE\\n'"],
            text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("RESULT=INPUT_OR_PRECONDITION_ERROR", result.stdout)
        self.assertIn("PARENT_SHELL_ALIVE=TRUE", result.stdout)
        self.assertNotRegex(self.bootstrap, r"(?m)^\s*(?:set\s+-[^\n]*e|exit(?:\s|$))")

    def test_action7b_is_short_governed_invocation(self):
        blocks = re.findall(r"```bash\n(.*?)```", self.action7b, re.DOTALL)
        self.assertEqual(len(blocks), 1)
        self.assertIn("tools/hioc-pe3-action7-activate.sh", blocks[0])
        self.assertIn("--governance-commit", blocks[0])
        self.assertNotIn("MANUFACTURER_DB_PATH", blocks[0])

    def test_exact_dataset_and_validation_contract(self):
        for value in (
            "local-ieee-ra--2026-08-11-r1", "8652642", "1338",
            "81f147cc57768c5797c4ad73a8c0369001bbdcbfe1548e71d3702c8c7f81e0e1",
            "10c8097c0a4ec6e8cc4cd3dc61afc7f368057f4ef4b6534df9f6dd31634a4ac4",
            "53581", 'd.get("privacy_safe") is True',
        ):
            self.assertIn(value, self.script)
        for marker in (
            "TARGET_IDENTITY=PASS", "SOURCE_IDENTITY=PASS", "RUNTIME_IDENTITY=PASS",
            "DATASET_IDENTITY=PASS", "DATASET_VALIDATION=PASS",
            "CONFIGURATION_PRECONDITION=PASS", "CONFIGURATION_BACKUP=PASS_CREATED",
            "CONFIGURATION_BACKUP=PASS_NOT_REQUIRED", "CONFIGURATION_ACTIVATION=PASS_NEW",
            "CONFIGURATION_ACTIVATION=PASS_NORMALIZED",
            "CONFIGURATION_ACTIVATION=PASS_ALREADY_ACTIVE", "CONFIGURATION_VALIDATION=PASS",
            "RUNTIME_DATASET_SELECTION=PASS", "POST_ACTIVATION_VALIDATION=PASS",
            "ACTION7=COMPLETE", "RESULT=PASS",
        ):
            self.assertIn(marker, self.script)

    def test_configuration_mutation_is_bounded_and_durable(self):
        self.assertEqual(self.script.count('out.append(f\'MANUFACTURER_DB_PATH="{value}"\')'), 2)
        self.assertIn('.hioc.conf.action7.XXXXXXXX', self.script)
        self.assertIn('mv -fT -- "$CONFIG_TEMP" "$CONFIG"', self.script)
        self.assertIn('sync -f "$CONFIG"', self.script)
        self.assertIn('sync -f "$CONFIG_DIR"', self.script)
        self.assertIn('sync -f "$CONFIG_TEMP"', self.script)
        self.assertIn("CONFIGURATION_DUPLICATE_KEY", self.script)
        self.assertIn("CONFIGURATION_DIFFERENT_VALUE", self.script)
        self.assertIn('bash -n "$CONFIG"', self.script)
        self.assertIn('bash -n "$CONFIG_TEMP"', self.script)
        self.assertIn("safe_owned_config", self.script)
        self.assertIn("NEEDS_MUTATION=TRUE", self.script)
        self.assertNotRegex(self.script, r"rm\s+-r[fF]?")

    def test_backup_and_rollback_contract(self):
        self.assertIn("hioc.conf.pre-pe3-action7.XXXXXXXX", self.script)
        self.assertIn('sync -f "$CONFIG_BACKUP"', self.script)
        self.assertIn("ROLLBACK_RECOMMENDED=%s", self.script)
        self.assertIn("CONFIGURATION_BACKUP_PATH=%s", self.script)
        self.assertNotIn("release/rollback.sh", self.script)
        self.assertNotRegex(
            self.script,
            r'(?:cp|install|mv)[^\n]*"\$CONFIG_BACKUP"[^\n]*"\$CONFIG"',
        )

    def test_no_other_production_domains_or_chaining(self):
        for forbidden in (
            "PI3_STAGE", "manufacturer.json", "manufacturer_status.json",
            "systemctl", "crontab", "ACTION8", "release/upgrade.sh",
        ):
            self.assertNotIn(forbidden, self.script)

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


if __name__ == "__main__":
    unittest.main()
