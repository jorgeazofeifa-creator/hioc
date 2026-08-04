import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "pi4" / "lib"))
SPEC = importlib.util.spec_from_file_location("hioc_assets_cli", ROOT / "pi4" / "bin" / "hioc-assets.py")
CLI = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(CLI)
ID = "dev_0123456789abcdef"


class Tty(io.StringIO):
    def isatty(self): return True


class AssetCliTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.home = Path(self.temp.name)
        self.output = io.StringIO(); self.error = io.StringIO()
        self.cli = CLI.AssetCli(self.home, io.StringIO(), self.output, self.error)
        self.cli.service.store.lock_path = self.home / "lock"

    def tearDown(self): self.temp.cleanup()

    def invoke(self, args):
        code = self.cli.run(args); output = self.output.getvalue(); self.output.seek(0); self.output.truncate(0)
        return code, output

    def test_json_initialize_and_redacted_list(self):
        self.assertEqual(self.invoke(["--json", "initialize"])[0], 0)
        code, output = self.invoke(["--json", "set", "--device-id", ID, "--friendly-name", "Secret Synthetic", "--allow-orphan"])
        self.assertEqual(code, 0); self.assertNotIn("Secret Synthetic", output); self.assertNotIn(ID, output)
        code, output = self.invoke(["--json", "list"]); self.assertEqual(code, 0)
        self.assertNotIn("Secret Synthetic", output); self.assertNotIn(ID, output)

    def test_revision_conflict_and_not_found_exit_codes(self):
        self.invoke(["initialize"]); self.invoke(["set", "--device-id", ID, "--friendly-name", "Synthetic", "--allow-orphan"])
        self.assertEqual(self.invoke(["set", "--device-id", ID, "--purpose", "X", "--expected-revision", "9"])[0], 5)
        self.assertEqual(self.invoke(["show", "--device-id", "dev_ffffffffffffffff"])[0], 4)

    def test_sensitive_display_requires_tty_and_confirmation(self):
        self.invoke(["initialize"]); self.invoke(["set", "--device-id", ID, "--friendly-name", "Sensitive Synthetic", "--allow-orphan"])
        self.assertEqual(self.invoke(["show", "--device-id", ID, "--show-sensitive"])[0], 13)
        out, err = Tty(), io.StringIO(); cli = CLI.AssetCli(self.home, Tty("SHOW\n"), out, err); cli.service.store.lock_path = self.home / "lock"
        self.assertEqual(cli.run(["show", "--device-id", ID, "--show-sensitive"]), 0)
        self.assertIn("Sensitive Synthetic", out.getvalue())
        self.assertNotIn("Sensitive Synthetic", err.getvalue())

    def test_json_sensitive_refused_and_usage_is_two(self):
        self.assertEqual(self.invoke(["--json", "show", "--device-id", ID, "--show-sensitive"])[0], 13)
        self.assertEqual(self.invoke(["set", "--device-id", ID])[0], 2)


if __name__ == "__main__": unittest.main()
