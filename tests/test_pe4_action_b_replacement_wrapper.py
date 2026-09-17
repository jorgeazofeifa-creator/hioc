import pathlib
import re
import shutil
import subprocess
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
WRAPPER = ROOT / "tools" / "hioc-pe4-action-b-replacement.ps1"
SOURCE = WRAPPER.read_text(encoding="utf-8")


class ActionBReplacementWrapperTests(unittest.TestCase):
    def test_single_atomic_invocation_and_single_action_b_launch_site(self):
        self.assertEqual(SOURCE.count("& {"), 1)
        self.assertEqual(SOURCE.count("$startInfo.ArgumentList.Add($Tool)"), 1)
        self.assertEqual(SOURCE.count("$process.Start()"), 1)
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
        self.assertIn("ACTION_B_REPLACEMENT=COMPLETE/PASS", SOURCE)
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
        executable = shutil.which("powershell.exe") or shutil.which("pwsh")
        if executable is None:
            self.skipTest("PowerShell is unavailable for syntax-only validation")
        escaped = str(WRAPPER).replace("'", "''")
        command = "$ErrorActionPreference='Stop';$null=[scriptblock]::Create([IO.File]::ReadAllText('" + escaped + "'))"
        completed = subprocess.run(
            [executable, "-NoProfile", "-NonInteractive", "-Command", command],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)


if __name__ == "__main__":
    unittest.main()
