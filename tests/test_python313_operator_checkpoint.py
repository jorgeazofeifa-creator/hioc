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
        self.assertIn("'--source', 'msstore'", self.script)
        self.assertIn("Get-Command -Name 'pymanager'", self.script)
        self.assertIn("Invoke-NativeProcess $ManagerCommand.Source @('install', $ExpectedMajorMinor)", self.script)
        self.assertNotIn('& $PythonCommand.Source install', self.script)
        self.assertNotIn("Get-Command -Name 'py' -CommandType Application -ErrorAction SilentlyContinue\nif ($null -eq $PythonCommand) { Write-CheckpointFailure 'INPUT_OR_PRECONDITION_ERROR' 'PYTHON_INSTALL_MANAGER_NOT_RESOLVABLE'", self.script)
        self.assertIn("$ExpectedMajorMinor = '3.13'", self.script)
        for forbidden in ("conda", "choco", "chocolatey", "scoop"):
            self.assertNotIn(forbidden, self.script.lower())

    def test_native_manager_stderr_is_governed_by_exit_code(self):
        helper = self.script.split("function Invoke-NativeProcess", 1)[1].split("if ([string]::IsNullOrWhiteSpace", 1)[0]
        self.assertIn("RedirectStandardOutput = $true", helper)
        self.assertIn("RedirectStandardError = $true", helper)
        self.assertIn("ExitCode = $Process.ExitCode", helper)
        self.assertIn("$StdoutTask = $Process.StandardOutput.ReadToEndAsync()", helper)
        self.assertIn("$StderrTask = $Process.StandardError.ReadToEndAsync()", helper)
        self.assertIn("Stderr = Limit-NativeOutput $StderrTask.Result", helper)
        self.assertIn("[string[]]$ArgumentList", helper)
        self.assertIn("ConvertTo-NativeArgument", helper)
        self.assertIn("Limit-NativeOutput", helper)
        self.assertIn("$Value.Length - $MaxNativeCaptureChars", self.script)
        self.assertNotIn("Substring(0, $MaxNativeCaptureChars)", self.script)
        self.assertNotIn("throw", helper.lower())
        self.assertIn("if ($Install313.ExitCode -ne 0)", self.script)
        self.assertNotIn("if (-not [string]::IsNullOrWhiteSpace($Install313.Stderr))", self.script)

    def test_manager_inspection_is_non_launching_and_existing_other_runtime_is_allowed(self):
        self.assertIn("@('list', '--one', '--format=json', '--only-managed', $ExpectedMajorMinor)", self.script)
        self.assertNotIn("py --help", self.script.lower())
        self.assertNotIn("pymanager --help", self.script.lower())
        self.assertNotIn("3.14", self.script)
        self.assertNotIn("uninstall", self.script.lower())
        self.assertLess(
            self.script.index("Get-Managed313Inventory"),
            self.script.index("Invoke-NativeProcess $ManagerCommand.Source @('install', $ExpectedMajorMinor)"),
        )

    def test_existing_313_is_reused_and_inventory_fails_closed(self):
        self.assertIn("if ($Managed313.Count -eq 0)", self.script)
        self.assertEqual(
            self.script.count("Invoke-NativeProcess $ManagerCommand.Source @('install', $ExpectedMajorMinor)"),
            1,
        )
        self.assertIn("PYTHON_MANAGED_INVENTORY_INVALID", self.script)
        self.assertIn("if ($Entries.Count -gt 1)", self.script)
        self.assertIn("catch {", self.script)
        self.assertIn("CPYTHON_313_INSTALL_VERIFICATION_FAILED", self.script)
        self.assertNotIn("uninstall", self.script.lower())

    def test_runtime_probe_is_execution_based_and_cpython_exact(self):
        self.assertIn("platform.python_implementation()", self.script)
        self.assertIn("platform.python_version()", self.script)
        self.assertIn("^CPython\\|3\\.13\\.[0-9]+$", self.script)
        self.assertIn("$PythonPrefix = @('-3.13')", self.script)
        self.assertIn("PYTHON_MANAGER_AUTOMATIC_INSTALL", self.script)
        self.assertIn("PYLAUNCHER_ALLOW_INSTALL", self.script)
        self.assertLess(
            self.script.index("SetEnvironmentVariable('PYTHON_MANAGER_AUTOMATIC_INSTALL', 'false'"),
            self.script.index("Get-Command -Name 'pymanager'"),
        )
        self.assertLess(
            self.script.index("Get-Managed313Inventory"),
            self.script.index("Get-Command -Name 'py'"),
        )
        self.assertIn("$ExactVersion = $ProbeLine.Substring('CPython|'.Length)", self.script)
        self.assertIn("$Probe = Invoke-NativeProcess $PythonCommand.Source", self.script)
        self.assertNotIn("& $PythonCommand.Source", self.script)

    def test_every_external_executable_uses_native_wrapper(self):
        self.assertNotRegex(self.script, r"(?m)^\s*&\s+\$")
        self.assertIn("function Invoke-Git", self.script)
        self.assertIn("Invoke-NativeProcess $GitCommand.Source", self.script)
        self.assertIn("Invoke-NativeProcess $Winget.Source", self.script)
        self.assertIn("Invoke-NativeProcess $ManagerCommand.Source", self.script)
        self.assertIn("Invoke-NativeProcess $PythonCommand.Source", self.script)

    def test_required_validation_matrix_is_run_with_governed_runtime(self):
        for marker in (
            "'unittest', 'discover', '-s', 'tests'",
            "tests.test_python_runtime_compatibility",
            "tests.test_pe3_action1_runbook",
            "test_manufacturer_*.py",
            "'-m', 'compileall'",
        ):
            self.assertIn(marker, self.script)
        self.assertIn("PYTHONPYCACHEPREFIX", self.script)
        self.assertIn("FINAL_REPOSITORY_STATE_FAILED", self.script)
        self.assertNotIn(".Ran -le 0", self.script)
        self.assertIn("$Result = Invoke-NativeProcess $PythonCommand.Source", self.script)
        self.assertIn("$Compilation = Invoke-NativeProcess $PythonCommand.Source", self.script)

    def test_native_exit_code_is_acceptance_and_counts_are_reporting_only(self):
        for result in ("Full", "Policy", "Action1", "Manufacturer"):
            self.assertIn(f"if (-not ${result}.Passed)", self.script)
            self.assertNotRegex(self.script, rf"if \([^\n]*\${result}\.Ran")
        self.assertIn("Passed = ($Result.ExitCode -eq 0)", self.script)
        self.assertIn("FULL_SUITE_TESTS=$($Full.Ran)", self.script)
        self.assertIn("FULL_SUITE_SKIPS=$($Full.Skipped)", self.script)

    def test_bounded_capture_preserves_success_summary_at_stream_tail(self):
        shell = shutil.which("powershell.exe") or shutil.which("powershell")
        if not shell:
            self.skipTest("Windows PowerShell unavailable")
        command = (
            "$text=Get-Content -Raw -LiteralPath $env:HIOC_TEST_PY313_SCRIPT;"
            "$tokens=$null;$errors=$null;"
            "$ast=[System.Management.Automation.Language.Parser]::ParseInput($text,[ref]$tokens,[ref]$errors);"
            "$names=@('Limit-NativeOutput','Get-NativeText','Invoke-PythonCheck');"
            "$ast.FindAll({param($n) $n -is [System.Management.Automation.Language.FunctionDefinitionAst] "
            "-and $names -contains $n.Name},$true) | ForEach-Object {Invoke-Expression $_.Extent.Text};"
            "$MaxNativeCaptureChars=1024;"
            "$raw=('x'*2048)+\"`nRan 506 tests in 14.889s`n`nOK (skipped=13)`n\";"
            "$limited=Limit-NativeOutput $raw;"
            "if($limited -notmatch 'Ran 506 tests'){exit 1};"
            "if($limited -notmatch 'OK \\(skipped=13\\)'){exit 2}"
        )
        env = dict(os.environ)
        env["HIOC_TEST_PY313_SCRIPT"] = str(SCRIPT)
        result = subprocess.run([shell, "-NoProfile", "-Command", command], env=env,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

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

    def test_native_helper_preserves_stderr_exit_status(self):
        shell = shutil.which("powershell.exe") or shutil.which("powershell")
        if not shell:
            self.skipTest("Windows PowerShell unavailable")
        command = (
            "$text=Get-Content -Raw -LiteralPath $env:HIOC_TEST_PY313_SCRIPT;"
            "$tokens=$null;$errors=$null;"
            "$ast=[System.Management.Automation.Language.Parser]::ParseInput($text,[ref]$tokens,[ref]$errors);"
            "$names=@('ConvertTo-NativeArgument','Limit-NativeOutput','Invoke-NativeProcess');"
            "$ast.FindAll({param($n) $n -is [System.Management.Automation.Language.FunctionDefinitionAst] "
            "-and $names -contains $n.Name},$true) | ForEach-Object {Invoke-Expression $_.Extent.Text};"
            "$MaxNativeCaptureChars=1048576;"
            "$ok=Invoke-NativeProcess $env:ComSpec @('/d','/c','echo informational 1>&2 & exit /b 0');"
            "$fail=Invoke-NativeProcess $env:ComSpec @('/d','/c','echo failure 1>&2 & exit /b 7');"
            "if($ok.ExitCode -ne 0 -or $ok.Stderr -notmatch 'informational'){exit 1};"
            "if($fail.ExitCode -ne 7 -or $fail.Stderr -notmatch 'failure'){exit 2}"
        )
        env = dict(os.environ)
        env["HIOC_TEST_PY313_SCRIPT"] = str(SCRIPT)
        result = subprocess.run([shell, "-NoProfile", "-Command", command], env=env,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
