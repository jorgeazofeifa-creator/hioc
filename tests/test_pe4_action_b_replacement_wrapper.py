import base64
import pathlib
import re
import shutil
import subprocess
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
WRAPPER = ROOT / "tools" / "hioc-pe4-action-b-replacement.ps1"
SOURCE = WRAPPER.read_text(encoding="utf-8")
PWSH = ROOT.parents[2] / ".cache" / "codex-runtimes" / "codex-primary-runtime" / "dependencies" / "native" / "powershell" / "pwsh.exe"
PYTHON = ROOT.parents[2] / ".cache" / "codex-runtimes" / "codex-primary-runtime" / "dependencies" / "python" / "python.exe"


class ActionBReplacementWrapperTests(unittest.TestCase):
    def test_single_atomic_invocation_and_single_action_b_launch_site(self):
        self.assertEqual(SOURCE.count("& {"), 1)
        self.assertEqual(SOURCE.count("Invoke-HIOCActionBTool -Python"), 1)
        self.assertEqual(SOURCE.count("$process.Start()"), 1)
        self.assertIn("function Invoke-HIOCPython", SOURCE)
        self.assertIn("$startInfo.ArgumentList.Add($argument)", SOURCE)
        self.assertNotIn("& $PythonPath", SOURCE)
        self.assertNotIn("& $Python -B -c", SOURCE)
        self.assertNotIn("hioc-pe4-runtime-construct.py", SOURCE)
        self.assertNotIn("Start-Sleep", SOURCE)
        self.assertNotIn("retry", SOURCE.lower().replace("not a retry mechanism", ""))

    def test_divergence_parser_requires_exactly_two_nonnegative_decimal_fields(self):
        pattern = re.compile(r"\A[ \t]*([0-9]+)[ \t]+([0-9]+)\r?\n?\Z")
        self.assertEqual(pattern.fullmatch("0\t0\r\n").groups(), ("0", "0"))
        for malformed in ("", "0", "0 0 0", "-1 0", "0 -1", "a 0", "0 a", "0\n0"):
            with self.subTest(malformed=malformed):
                self.assertIsNone(pattern.fullmatch(malformed))
        self.assertIn("$behind -ne 0 -or $ahead -ne 0", SOURCE)

    def test_precheck_is_before_the_only_launch_and_terminal_states_are_bounded(self):
        self.assertLess(SOURCE.index("Test-HIOCRepository"), SOURCE.index("$launched = $true"))
        self.assertIn("ACTION_B_REPLACEMENT=NOT_EXECUTED", SOURCE)
        self.assertIn("ACTION_B_REPLACEMENT=ATTEMPTED_NOT_COMPLETE", SOURCE)
        self.assertIn("ACTION_B_REPLACEMENT=ATTEMPTED_POSTCONDITION_FAILED", SOURCE)
        self.assertIn("ACTION_B_REPLACEMENT=COMPLETE", SOURCE)
        self.assertNotIn("REPLACEMENT_TRANSACTION=TRUE", SOURCE)
        for marker in (
            "REPLACEMENT_WRAPPER=INVOKED", "PRECHECKS=FAILED",
            "ACTION_B_LAUNCH=NOT_STARTED", "ACTION_B_TRANSACTION=NOT_STARTED",
            "ACTION_B_LAUNCH=STARTED", "ACTION_B_TRANSACTION=ATTEMPTED",
            "ACTION_B_TRANSACTION=COMPLETE",
        ):
            self.assertIn(marker, SOURCE)
        self.assertEqual(SOURCE.count("STOP_REQUIRED=TRUE"), 4)

    def test_success_requires_current_action_b_markers_and_canonical_python_validator(self):
        for marker in (
            "REMOTE_STAGING_CREATED=TRUE", "WHEEL_TRANSFERRED=TRUE",
            "LOCK_TRANSFERRED=TRUE", "REMOTE_ARTIFACT_VERIFIED=TRUE",
            "REMOTE_LOCK_VERIFIED=TRUE", "EVIDENCE_STATE=CONFIRMED",
            "ACTION_B=COMPLETE", "RESULT=PASS", "ERROR_CODE=NONE",
            "FAILURE_STAGE=COMPLETE", "ROLLBACK_RECOMMENDED=FALSE",
        ):
            self.assertIn(marker, SOURCE)
        self.assertIn("from hioc_pe4_runtime_common import is_transfer_directory", SOURCE)
        self.assertNotIn("[A-Za-z0-9_]", SOURCE)

    def test_historical_and_failed_paths_are_never_reused(self):
        self.assertIn("/tmp/hioc-pe4-artifact-transfer-7g3xp1lk", SOURCE)
        self.assertIn("/tmp/hioc-pe4-artifact-transfer-g_jrlqkl", SOURCE)
        self.assertIn("TRANSFER_DIRECTORY_REUSE_FORBIDDEN", SOURCE)
        self.assertIn("STAGING_PRESERVED=TRUE", SOURCE)

    def test_powershell_syntax_when_available(self):
        executable = str(PWSH)
        self.assertTrue(PWSH.is_file(), "managed PowerShell Core is required for syntax validation")
        escaped = str(WRAPPER).replace("'", "''")
        command = "$ErrorActionPreference='Stop';$null=[scriptblock]::Create([IO.File]::ReadAllText('" + escaped + "'))"
        completed = subprocess.run(
            [executable, "-NoProfile", "-NonInteractive", "-Command", command],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_actual_windows_powershell_argument_list_preserves_embedded_python_quotes(self):
        executable = str(PWSH)
        self.assertTrue(PWSH.is_file(), "managed PowerShell Core is required for this regression")
        start = SOURCE.index("function Invoke-HIOCPython")
        end = SOURCE.index("function Invoke-HIOCActionBTool")
        helper = SOURCE[start:end]
        code = 'import pathlib,sys;root=pathlib.Path(sys.argv[1]);print(str(root/"tools"))'
        script = helper + "\n" + (
            "$r=Invoke-HIOCPython -Python '" + str(PYTHON) + "' -Arguments @('-B','-c','" +
            code.replace("'", "''") + "','" + str(ROOT).replace("'", "''") + "') -Stage 'TEST';"
            "if($r.ExitCode -ne 0){exit 31};"
            "[Console]::Out.Write('BOUNDARY_OUTPUT='+$r.Stdout)"
        )
        encoded = base64.b64encode(script.encode("utf-16le")).decode("ascii")
        completed = subprocess.run(
            [executable, "-NoProfile", "-NonInteractive", "-EncodedCommand", encoded],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn(str(ROOT / "tools"), completed.stdout)
        self.assertNotIn("NameError", completed.stderr)


if __name__ == "__main__":
    unittest.main()
