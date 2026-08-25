import importlib.util
import pathlib
import subprocess
import sys
import io
import unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))
spec = importlib.util.spec_from_file_location("pe4_action_b", TOOLS / "hioc-pe4-artifact-transfer.py")
ACTION_B = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ACTION_B)


class Runner:
    def __init__(self, fail_stage=None):
        self.calls = []
        self.fail_stage = fail_stage

    def __call__(self, command, stage, **kwargs):
        self.calls.append((command, stage, kwargs))
        if stage == self.fail_stage:
            raise ACTION_B.Failure("SIMULATED_FAILURE", stage)
        output = "/tmp/hioc-pe4-artifact-transfer-Ab12Cd34\n" if stage == "REMOTE_STAGING" else ""
        return subprocess.CompletedProcess(command, 0, output, "")


class PE4ActionBTransferTests(unittest.TestCase):
    def test_cli_is_exact_and_bounded(self):
        commit = "a" * 40
        self.assertEqual(ACTION_B.parse_cli(["--governance-commit", commit]), commit)
        for args in ([], ["--help"], ["--governance-commit", commit, "extra"], ["--wheel", "x"]):
            with self.assertRaises(ACTION_B.Failure):
                ACTION_B.parse_cli(args)

    @mock.patch.object(ACTION_B, "local_inputs", return_value=(pathlib.Path("C:/cache/wheel.whl"), pathlib.Path("C:/repo/requirements-pe4.lock")))
    def test_exact_host_options_separate_transfers_and_stop_after_evidence(self, _inputs):
        runner = Runner()
        states, remote = ACTION_B.execute("a" * 40, runner=runner,
                                          resolver=lambda name: pathlib.Path(f"C:/Windows/System32/OpenSSH/{name}.exe"))
        self.assertTrue(all(states.values()))
        self.assertEqual(remote, "/tmp/hioc-pe4-artifact-transfer-Ab12Cd34")
        flattened = [item for call, _, _ in runner.calls for item in call]
        for option in ACTION_B.SSH_OPTIONS:
            self.assertIn(option, flattened)
        self.assertNotIn("ssh", flattened)
        self.assertNotIn("scp", flattened)
        self.assertTrue(all("192.168.100.251" not in item for item in flattened))
        stages = [stage for _, stage, _ in runner.calls]
        self.assertEqual(stages, ["REMOTE_STAGING", "WHEEL_TRANSFER", "LOCK_TRANSFER",
                                  "REMOTE_ARTIFACT_IDENTITY", "REMOTE_LOCK_IDENTITY",
                                  "EVIDENCE_PUBLICATION"])
        self.assertNotIn("pip", " ".join(flattened))
        self.assertNotIn("venv", " ".join(flattened))

    @mock.patch.object(ACTION_B, "local_inputs", return_value=(pathlib.Path("C:/cache/wheel.whl"), pathlib.Path("C:/repo/requirements-pe4.lock")))
    def test_partial_transfer_failure_publishes_sanitized_state_and_preserves_directory(self, _inputs):
        runner = Runner("LOCK_TRANSFER")
        with self.assertRaises(ACTION_B.Failure) as caught:
            ACTION_B.execute("a" * 40, runner=runner, resolver=lambda name: pathlib.Path(name))
        exc = caught.exception
        self.assertTrue(exc.states["REMOTE_STAGING_CREATED"])
        self.assertTrue(exc.states["WHEEL_TRANSFERRED"])
        self.assertFalse(exc.states["LOCK_TRANSFERRED"])
        self.assertEqual(exc.remote, "/tmp/hioc-pe4-artifact-transfer-Ab12Cd34")
        self.assertEqual(runner.calls[-1][1], "FAILURE_EVIDENCE_PUBLICATION")
        evidence = runner.calls[-1][0][-1]
        self.assertIn('"wheel_transferred":true', evidence)
        self.assertIn('"lock_transferred":false', evidence)
        self.assertNotIn("SIMULATED_FAILURE\n", evidence)
        self.assertNotIn("rm ", evidence)

    def test_evidence_is_result_last_and_contains_only_bounded_state(self):
        states = {key: False for key in ACTION_B.STATE_KEYS}
        command = ACTION_B.evidence_command("/tmp/hioc-pe4-artifact-transfer-Ab12Cd34", states,
                                            "FAIL", "TRANSFER_FAILED", "WHEEL_TRANSFER")
        self.assertLess(command.index(".failure-result.tmp"), command.index("mv --"))
        self.assertIn("result.json", command)
        for forbidden in ("token", "credential", "Authorization", "manufacturer", "inventory"):
            self.assertNotIn(forbidden, command)

    def test_source_has_no_path_selected_artifact_or_lifecycle_chaining(self):
        source = (TOOLS / "hioc-pe4-artifact-transfer.py").read_text(encoding="utf-8")
        self.assertIn('("HIOC","artifacts","pe4","cache")', source)
        self.assertNotIn("--wheel", source)
        self.assertNotIn("workstation_cache_root(); wheel=cache/WHEEL_NAME", source)
        for forbidden in ("release/upgrade.sh", "systemctl", "pip install", "ACTION_C"):
            self.assertNotIn(forbidden, source)

    def test_real_subprocess_boundary_fails_closed_on_output_overflow(self):
        with self.assertRaises(ACTION_B.Failure) as caught:
            ACTION_B.run_bounded([sys.executable, "-c", "import sys;sys.stdout.write('x'*9000)"],
                                 "TEST_BOUNDARY", timeout=5, max_output=1024)
        self.assertEqual((caught.exception.code, caught.exception.stage),
                         ("COMMAND_OUTPUT_TOO_LARGE", "TEST_BOUNDARY"))

    def test_terminal_order_is_bounded_and_includes_partial_directory(self):
        states = {key: False for key in ACTION_B.STATE_KEYS}
        states["REMOTE_STAGING_CREATED"] = True
        output = io.StringIO()
        with mock.patch("sys.stdout", output):
            ACTION_B.emit(states, "FAIL", "TRANSFER_FAILED", "WHEEL_TRANSFER",
                          "/tmp/hioc-pe4-artifact-transfer-Ab12Cd34")
        lines = output.getvalue().splitlines()
        self.assertEqual(lines[-5:], ["RESULT=FAIL", "ERROR_CODE=TRANSFER_FAILED",
                                      "FAILURE_STAGE=WHEEL_TRANSFER",
                                      "ROLLBACK_RECOMMENDED=FALSE",
                                      "TRANSFER_DIRECTORY=/tmp/hioc-pe4-artifact-transfer-Ab12Cd34"])


if __name__ == "__main__":
    unittest.main()
