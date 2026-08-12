import os
import pathlib
import hashlib
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "hioc-python313-process-diagnostic.ps1"
POLICY = ROOT / "docs" / "PYTHON_RUNTIME_COMPATIBILITY.md"


class Python313ProcessDiagnosticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = SCRIPT.read_text(encoding="utf-8")

    def test_is_repository_controlled_and_sanitized(self):
        self.assertIn("[string]$Repo", self.script)
        self.assertIn("[string]$GovernanceCommit", self.script)
        self.assertIn("PROCESS_DIAGNOSTIC_SCRIPT_IDENTITY_MISMATCH", self.script)
        self.assertIn("$ActualBlob -ne $ExpectedBlob", self.script)
        self.assertNotIn("C:\\Users\\", self.script)
        self.assertNotIn("ScriptStackTrace", self.script)
        self.assertNotIn("$_.Exception", self.script)
        self.assertNotRegex(self.script, r"(?m)^\s*exit(?:\s|$)")

    def test_governed_identities_are_documented(self):
        policy = POLICY.read_text(encoding="utf-8")
        sha = hashlib.sha256(SCRIPT.read_bytes()).hexdigest()
        git = shutil.which("git")
        self.assertIsNotNone(git)
        blob = subprocess.run(
            [git, "-C", str(ROOT), "hash-object", "--path=tools/hioc-python313-process-diagnostic.ps1", "--", str(SCRIPT)],
            check=True, capture_output=True, text=True,
        ).stdout.strip()
        self.assertIn(f"PYTHON313_PROCESS_DIAGNOSTIC_SHA256={sha}", policy)
        self.assertIn(f"PYTHON313_PROCESS_DIAGNOSTIC_GIT_BLOB={blob}", policy)

    def test_compares_same_python_arguments_and_environment(self):
        self.assertIn("$RegressionArgs = @('-3.13','-m','unittest','discover','-s','tests')", self.script)
        self.assertIn("Invoke-DirectPowerShell $Python.Source $RegressionArgs", self.script)
        self.assertIn("Invoke-ProcessStartInfo $Python.Source $RegressionArgs", self.script)
        self.assertIn("PYTHONPYCACHEPREFIX", self.script)
        self.assertIn("Set-Location -LiteralPath $Repo", self.script)

    def test_reports_bounded_wrapper_internals_without_raw_test_output(self):
        self.assertIn("DIAGNOSTIC_EXECUTION=PASS", self.script)
        self.assertIn("EQUIVALENCE_RESULT=", self.script)
        self.assertNotIn("Write-Output 'RESULT=PASS'", self.script)
        for marker in (
            "WRAPPER_FULL_STARTED=", "WRAPPER_FULL_COMPLETED=", "WRAPPER_FULL_EXIT=",
            "WRAPPER_FULL_STDOUT_LENGTH=", "WRAPPER_FULL_STDERR_LENGTH=",
            "WRAPPER_FULL_STDOUT_TASK=", "WRAPPER_FULL_STDERR_TASK=",
            "WRAPPER_FULL_TESTS=", "WRAPPER_FULL_SKIPS=", "WRAPPER_FULL_SUMMARY_OK=",
            "DIRECT_FULL_EXIT=", "EXIT_CODES_MATCH=",
        ):
            self.assertIn(marker, self.script)
        self.assertNotIn("Write-Output $WrapperFull.Stdout", self.script)
        self.assertNotIn("Write-Output $WrapperFull.Stderr", self.script)

    def test_equivalence_result_passes_and_fails_closed(self):
        shell = shutil.which("powershell.exe") or shutil.which("powershell")
        if not shell:
            self.skipTest("Windows PowerShell unavailable")
        command = (
            "$text=Get-Content -Raw -LiteralPath $env:HIOC_TEST_DIAGNOSTIC;"
            "$tokens=$null;$errors=$null;"
            "$ast=[System.Management.Automation.Language.Parser]::ParseInput($text,[ref]$tokens,[ref]$errors);"
            "$fn=$ast.Find({param($n) $n -is [System.Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq 'Test-ExecutionEquivalence'},$true);"
            "Invoke-Expression $fn.Extent.Text;"
            "$ok=[pscustomobject]@{ExitCode=0;Stdout='argv'};$summary=[pscustomobject]@{Success=$true};"
            "$bad=[pscustomobject]@{ExitCode=1;Stdout='argv'};"
            "if(-not(Test-ExecutionEquivalence $ok $ok $ok $ok 'argv' $ok $ok $summary $summary)){exit 1};"
            "if(Test-ExecutionEquivalence $ok $ok $ok $ok 'argv' $ok $bad $summary $summary){exit 2}"
        )
        env = dict(os.environ)
        env["HIOC_TEST_DIAGNOSTIC"] = str(SCRIPT)
        result = subprocess.run([shell, "-NoProfile", "-Command", command], env=env,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_argv_fidelity_matrix_is_present(self):
        for value in ("path with spaces", "quote\"inside", "backslash\\before\"quote", "trailing\\", "''"):
            self.assertIn(value, self.script)
        self.assertIn("DIRECT_ARGV_MATCH=", self.script)
        self.assertIn("WRAPPER_ARGV_MATCH=", self.script)

    def test_processstartinfo_semantics_are_instrumented(self):
        for marker in (
            "UseShellExecute = $false", "CreateNoWindow = $true",
            "RedirectStandardOutput = $true", "RedirectStandardError = $true",
            "ReadToEndAsync()", "$Process.WaitForExit()", "$Process.ExitCode",
            ".GetAwaiter().GetResult()", "$Process.Dispose()",
        ):
            self.assertIn(marker, self.script)

    def test_powershell_51_parse(self):
        shell = shutil.which("powershell.exe") or shutil.which("powershell")
        if not shell:
            self.skipTest("Windows PowerShell unavailable")
        command = (
            "$text=Get-Content -Raw -LiteralPath $env:HIOC_TEST_DIAGNOSTIC;"
            "$tokens=$null;$errors=$null;"
            "[System.Management.Automation.Language.Parser]::ParseInput($text,[ref]$tokens,[ref]$errors)|Out-Null;"
            "if($errors.Count){$errors.Message;exit 1}"
        )
        env = dict(os.environ)
        env["HIOC_TEST_DIAGNOSTIC"] = str(SCRIPT)
        result = subprocess.run([shell, "-NoProfile", "-Command", command], env=env,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_real_wrapper_stream_exit_argv_repeat_and_cleanup(self):
        shell = shutil.which("powershell.exe") or shutil.which("powershell")
        if not shell:
            self.skipTest("Windows PowerShell unavailable")
        with tempfile.TemporaryDirectory(prefix="hioc wrapper path ") as temporary:
            spaced_cmd = pathlib.Path(temporary) / "native child with spaces.exe"
            shutil.copy2(os.environ["ComSpec"], spaced_cmd)
            command = (
                "$text=Get-Content -Raw -LiteralPath $env:HIOC_TEST_DIAGNOSTIC;"
                "$tokens=$null;$errors=$null;"
                "$ast=[System.Management.Automation.Language.Parser]::ParseInput($text,[ref]$tokens,[ref]$errors);"
                "$names=@('ConvertTo-NativeArgument','Limit-Output','Invoke-ProcessStartInfo');"
                "$ast.FindAll({param($n) $n -is [System.Management.Automation.Language.FunctionDefinitionAst] "
                "-and $names -contains $n.Name},$true)|ForEach-Object{Invoke-Expression $_.Extent.Text};"
                "$MaxCaptureChars=65536;"
                "$largeOut=Invoke-ProcessStartInfo $env:HIOC_TEST_PYTHON @('-c','import sys;sys.stdout.write(\"x\"*1100000)');"
                "$largeErr=Invoke-ProcessStartInfo $env:HIOC_TEST_PYTHON @('-c','import sys;sys.stderr.write(\"y\"*1100000)');"
                "$both=Invoke-ProcessStartInfo $env:HIOC_TEST_PYTHON @('-c','import sys;sys.stdout.write(\"o\"*200000);sys.stderr.write(\"e\"*200000)');"
                "$fail=Invoke-ProcessStartInfo $env:HIOC_TEST_PYTHON @('-c','raise SystemExit(7)');"
                "$argv=Invoke-ProcessStartInfo $env:HIOC_TEST_PYTHON @('-c','import json,sys;print(json.dumps(sys.argv[1:]))','path with spaces','quote\"inside','trailing\\','');"
                "if($largeOut.ExitCode-ne 0-or $largeOut.StdoutLength-ne 1100000-or $largeOut.Stdout.Length-ne 65536){exit 1};"
                "if($largeErr.ExitCode-ne 0-or $largeErr.StderrLength-ne 1100000-or $largeErr.Stderr.Length-ne 65536){exit 2};"
                "if($both.ExitCode-ne 0-or $both.StdoutLength-ne 200000-or $both.StderrLength-ne 200000){exit 3};"
                "if($fail.ExitCode-ne 7){exit 4};"
                "if($argv.Stdout.Trim()-ne '[\"path with spaces\", \"quote\\\"inside\", \"trailing\\\\\", \"\"]'){exit 5};"
                "1..3|ForEach-Object{$r=Invoke-ProcessStartInfo $env:HIOC_TEST_SPACED_CMD @('/d','/c','exit /b 0');if($r.ExitCode-ne 0){exit 6}}"
            )
            env = dict(os.environ)
            env["HIOC_TEST_DIAGNOSTIC"] = str(SCRIPT)
            env["HIOC_TEST_PYTHON"] = sys.executable
            env["HIOC_TEST_SPACED_CMD"] = str(spaced_cmd)
            result = subprocess.run([shell, "-NoProfile", "-Command", command], env=env,
                                    capture_output=True, text=True, timeout=60)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(spaced_cmd.exists())


if __name__ == "__main__":
    unittest.main()
