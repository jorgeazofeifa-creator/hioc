import os
import hashlib
import pathlib
import re
import shutil
import subprocess
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "hioc-pe3-action5-deploy.sh"
RUNBOOK = ROOT / "docs" / "PE3_MANUFACTURER_PRODUCTION_RUNBOOK.md"


class PE3Action5DeploymentContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = SCRIPT.read_text(encoding="utf-8")
        cls.runbook = RUNBOOK.read_text(encoding="utf-8")
        cls.action5 = cls.runbook.split("## Action 5", 1)[1].split("## Action 6", 1)[0]

    def test_repository_script_is_the_only_runbook_implementation(self):
        blocks = re.findall(r"```bash\n(.*?)```", self.action5, re.DOTALL)
        self.assertEqual(len(blocks), 1)
        self.assertIn("tools/hioc-pe3-action5-deploy.sh", blocks[0])
        self.assertIn("--governance-commit", blocks[0])
        self.assertNotIn("release/upgrade.sh", blocks[0])
        self.assertNotIn("set -e", blocks[0])

    def test_documented_script_identities_match(self):
        sha256 = hashlib.sha256(SCRIPT.read_bytes()).hexdigest()
        self.assertEqual(sha256, "f0d2395f5ccfbbf773da95e0fbb2ec18786e2aa03296f1085436025ace6d1b09")
        self.assertIn(sha256, self.action5)
        result = subprocess.run(
            ["git", "hash-object", "--path=tools/hioc-pe3-action5-deploy.sh", str(SCRIPT)],
            cwd=ROOT, text=True, capture_output=True, check=True,
        )
        self.assertEqual(result.stdout.strip(), "9dc26c01cd1f9b1bdbce057313d2b2ca0b92cd4c")
        self.assertIn(result.stdout.strip(), self.action5)

    def test_parent_shell_survives_harmless_failure(self):
        shell = os.environ.get("HIOC_TEST_SHELL") or shutil.which("bash")
        if not shell:
            self.skipTest("Bash is required")
        script_for_shell = str(SCRIPT).replace("\\", "/")
        if re.match(r"^[A-Za-z]:/", script_for_shell):
            script_for_shell = "/" + script_for_shell[0].lower() + script_for_shell[2:]
        result = subprocess.run(
            [shell, "-c", f". '{script_for_shell}'; printf 'PARENT_SHELL_ALIVE=TRUE\\n'"],
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("ERROR_CODE=INVALID_ARGUMENTS", result.stdout)
        self.assertIn("PARENT_SHELL_ALIVE=TRUE", result.stdout)
        self.assertNotIn("CODE_DEPLOYMENT=PASS", result.stdout)

    def test_predeployment_failures_precede_mutation(self):
        main = self.script.split("main() {", 1)[1]
        self.assertLess(main.index("verify_target_and_source || return 1"), main.index("deploy_supported_release || return 1"))
        self.assertLess(main.index("prepare_evidence_and_manifest || return 1"), main.index("deploy_supported_release || return 1"))
        self.assertLess(main.index("validate_release || return 1"), main.index("deploy_supported_release || return 1"))
        for marker in (
            "INVALID_GOVERNANCE_COMMIT", "WRONG_TARGET", "SOURCE_REPOSITORY_MISSING",
            "WRONG_BRANCH", "GOVERNANCE_COMMIT_MISMATCH", "SOURCE_REPOSITORY_DIRTY",
            "ACTIVE_GIT_OPERATION", "ACTION5_SCRIPT_IDENTITY_MISMATCH",
            "RELEASE_VALIDATION_FAILED", "BACKUP_PRECONDITION_FAILED",
        ):
            self.assertIn(marker, self.script)

    def test_failure_stages_stop_later_work(self):
        self.assertIn("validate_release || return 1", self.script)
        self.assertIn("deploy_supported_release || return 1", self.script)
        self.assertIn("validate_runtime_and_artifacts || return 1", self.script)
        self.assertIn("RUNTIME_VALIDATION_FAILED", self.script)
        self.assertIn("RUNTIME_ARTIFACT_IDENTITY_MISMATCH", self.script)
        self.assertIn("ACTION5_UNEXPECTED_ERROR", self.script)

    def test_backup_and_deployment_failure_contract(self):
        self.assertIn("RELEASE_BACKUP_CREATION_FAILED", self.script)
        self.assertIn("CODE_DEPLOYMENT_FAILED", self.script)
        deploy = self.script.index('release/upgrade.sh" >')
        runtime = self.script.index('validate_runtime_and_artifacts()')
        self.assertLess(deploy, runtime)
        self.assertIn("ROLLBACK_RECOMMENDED=%s", self.script)

    def test_dataset_configuration_and_action6_are_out_of_scope(self):
        self.assertIn('fingerprint_path "$RUNTIME/config/hioc.conf"', self.script)
        self.assertIn('fingerprint_path "$RUNTIME/data/manufacturer"', self.script)
        self.assertNotIn("manufacturer-db.json", self.script)
        self.assertNotIn("MANUFACTURER_DB_PATH=", self.script)
        self.assertNotRegex(self.script, r"(?:bash|python3) .*hioc-generate-manufacturer")
        self.assertNotIn("Action 6", self.script)
        self.assertNotIn("ACTION6", self.script)

    def test_explicit_pass_and_failure_evidence(self):
        for marker in (
            "TARGET_IDENTITY=PASS", "SOURCE_IDENTITY=PASS", "RELEASE_VALIDATION=PASS",
            "RELEASE_BACKUP=PASS", "CODE_DEPLOYMENT=PASS", "RUNTIME_VALIDATION=PASS",
            "RUNTIME_ARTIFACT_IDENTITY=PASS", "EVIDENCE_REPORT=PASS",
            "ACTION5=COMPLETE", "RESULT=PASS", "ROLLBACK_RECOMMENDED=FALSE",
        ):
            self.assertIn(marker, self.script)
        for marker in ("RESULT=%s", "ERROR_CODE=%s", "FAILURE_STAGE=%s"):
            self.assertIn(marker, self.script)

    def test_script_has_no_parent_shell_controls_or_implicit_pipeline_evidence(self):
        self.assertNotRegex(self.script, r"(?m)^\s*set\s+-[a-zA-Z]*e")
        self.assertNotRegex(self.script, r"(?m)^\s*exit(?:\s|$)")
        self.assertNotIn("| tee", self.script)


if __name__ == "__main__":
    unittest.main()
