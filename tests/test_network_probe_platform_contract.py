import os
import pathlib
import shutil
import subprocess
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE = "tests.test_network_probe_governance"


class NetworkProbePlatformContractTests(unittest.TestCase):
    def run_module(self, env):
        return subprocess.run(
            [sys.executable, "-m", "unittest", MODULE],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
        )

    def test_missing_bash_is_three_visible_skips_not_errors(self):
        env = os.environ.copy()
        env.pop("HIOC_TEST_SHELL", None)
        env["PATH"] = ""
        result = self.run_module(env)
        output = result.stdout + result.stderr
        self.assertEqual(result.returncode, 0, output)
        self.assertIn("Ran 6 tests", output)
        self.assertIn("OK (skipped=3)", output)
        self.assertNotIn("ERROR", output)

    def test_available_bash_executes_all_original_assertions(self):
        shell = os.environ.get("HIOC_TEST_SHELL") or shutil.which("bash")
        if not shell:
            self.skipTest("Bash is required")
        env = os.environ.copy()
        env["HIOC_TEST_SHELL"] = shell
        result = self.run_module(env)
        output = result.stdout + result.stderr
        self.assertEqual(result.returncode, 0, output)
        self.assertIn("Ran 6 tests", output)
        self.assertIn("OK", output)
        self.assertNotIn("skipped=", output)


if __name__ == "__main__":
    unittest.main()
