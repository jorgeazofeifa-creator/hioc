import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "hioc-python313-validate.ps1"
POLICY = ROOT / "docs" / "PYTHON_RUNTIME_COMPATIBILITY.md"
SUPPORT = ROOT / "governance" / "python-runtime-support.json"
GITATTRIBUTES = ROOT / ".gitattributes"


class Python313OperatorCheckpointTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = SCRIPT.read_text(encoding="utf-8")
        cls.policy = POLICY.read_text(encoding="utf-8")
        cls.support = json.loads(SUPPORT.read_text(encoding="utf-8"))

    def test_explicit_parameters_and_self_identity(self):
        for name in ("Repo", "GovernanceCommit"):
            self.assertIn(f"[string]${name}", self.script)
        self.assertIn("tools/hioc-python313-validate.ps1", self.script)
        self.assertIn("PYTHON_CHECKPOINT_SCRIPT_IDENTITY_MISMATCH", self.script)
        self.assertIn("$Head -ne $GovernanceCommit -or $Origin -ne $GovernanceCommit", self.script)
        self.assertNotIn("C:\\Users\\", self.script)

    def test_pending_support_state_is_required_and_not_modified(self):
        self.assertEqual(self.support["windows_operator"]["status"], "validation_pending")
        self.assertIsNone(self.support["windows_operator"]["validated_patch"])
        self.assertIn("$Support.windows_operator.status -cne 'validation_pending'", self.script)
        self.assertIn("PYTHON_SUPPORT_STATE_NOT_PENDING", self.script)
        self.assertNotIn("Set-Content", self.script)
        self.assertNotIn("Add-Content", self.script)

    def test_official_install_manager_and_runtime_line_are_exact(self):
        self.assertIn("$InstallerPackageId = '9NQ7512CXL7T'", self.script)
        self.assertIn("--source msstore", self.script)
        self.assertIn("install $ExpectedMajorMinor", self.script)
        self.assertIn("$ExpectedMajorMinor = '3.13'", self.script)
        for forbidden in ("conda", "choco", "chocolatey", "scoop"):
            self.assertNotIn(forbidden, self.script.lower())

    def test_runtime_probe_is_execution_based_and_cpython_exact(self):
        self.assertIn("platform.python_implementation()", self.script)
        self.assertIn("platform.python_version()", self.script)
        self.assertIn("^CPython\\|3\\.13\\.[0-9]+$", self.script)
        self.assertIn("$PythonPrefix = @('-3.13')", self.script)
        self.assertIn("PYTHON_MANAGER_AUTOMATIC_INSTALL", self.script)
        self.assertIn("PYLAUNCHER_ALLOW_INSTALL", self.script)

    def test_required_validation_matrix_is_run_with_governed_runtime(self):
        for marker in (
            "unittest', 'discover', '-s', 'tests'",
            "tests.test_python_runtime_compatibility",
            "tests.test_pe3_action1_runbook",
            "test_manufacturer_*.py",
            "-m compileall",
        ):
            self.assertIn(marker, self.script)
        self.assertIn("PYTHONPYCACHEPREFIX", self.script)
        self.assertIn("FINAL_REPOSITORY_STATE_FAILED", self.script)
        self.assertGreaterEqual(self.script.count(".Ran -le 0"), 4)

    def test_evidence_is_sanitized_and_complete(self):
        for field in (
            "RESULT=PASS", "PYTHON_IMPLEMENTATION=", "PYTHON_VERSION=",
            "PYTHON_RESOLVER=py -3.13",
            "SUPPORT_STATE_BEFORE_VALIDATION=validation_pending",
            "FULL_SUITE_TESTS=", "FULL_SUITE_SKIPS=",
            "PYTHON_POLICY_TESTS=PASS:", "ACTION1_GOVERNANCE_TESTS=PASS:",
            "MANUFACTURER_TESTS=PASS:", "PYTHON_COMPILATION=PASS",
            "REPOSITORY_HEAD=", "WORKING_TREE_CLEAN=TRUE",
            "PROMOTE_TO_SUPPORTED=TRUE", "ROLLBACK_RECOMMENDED=FALSE",
        ):
            self.assertIn(field, self.script)
        self.assertNotIn("$_.Exception", self.script)
        self.assertNotIn("ScriptStackTrace", self.script)

    def test_no_action1_action2_or_production_logic(self):
        lower = self.script.lower()
        for forbidden in (
            "hioc-pe3-action1.ps1", "hioc-validate-manufacturer.py",
            "ssh ", "scp ", "rsync ", "192.168.100.252", "action 2",
            "manufacturer.json", "manufacturer_status.json",
        ):
            self.assertNotIn(forbidden, lower)
        self.assertNotRegex(self.script, r"(?m)^\s*exit(?:\s|$)")

    def test_policy_records_identity_and_short_invocation(self):
        self.assertIn(
            "tools/hioc-python313-validate.ps1 text eol=lf",
            GITATTRIBUTES.read_text(encoding="utf-8").splitlines(),
        )
        sha = hashlib.sha256(SCRIPT.read_bytes()).hexdigest()
        blob_tool = shutil.which("git")
        self.assertIsNotNone(blob_tool)
        blob = subprocess.run(
            [blob_tool, "-C", str(ROOT), "hash-object", "--path=tools/hioc-python313-validate.ps1", "--", str(SCRIPT)],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        self.assertIn(f"PYTHON313_CHECKPOINT_SHA256={sha}", self.policy)
        self.assertIn(f"PYTHON313_CHECKPOINT_GIT_BLOB={blob}", self.policy)
        self.assertIn("& $CheckpointScript -Repo $Repo -GovernanceCommit $GovernanceCommit", self.policy)

    def test_powershell_51_parse(self):
        shell = shutil.which("powershell.exe") or shutil.which("powershell")
        if not shell:
            self.skipTest("Windows PowerShell unavailable")
        command = (
            "$text=Get-Content -Raw -LiteralPath $env:HIOC_TEST_PY313_SCRIPT;"
            "$tokens=$null;$errors=$null;"
            "[System.Management.Automation.Language.Parser]::ParseInput($text,[ref]$tokens,[ref]$errors)|Out-Null;"
            "if($errors.Count){$errors.Message;exit 1}"
        )
        env = dict(os.environ)
        env["HIOC_TEST_PY313_SCRIPT"] = str(SCRIPT)
        result = subprocess.run([shell, "-NoProfile", "-Command", command], env=env,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
