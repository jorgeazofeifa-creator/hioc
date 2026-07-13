from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ReleaseScriptTests(unittest.TestCase):
    def test_upgrade_invokes_non_executable_installer_through_bash(self):
        upgrade_script = (ROOT / "release" / "upgrade.sh").read_text(encoding="utf-8")

        self.assertIn('bash "$INSTALL_DIR/pi4/install_pi4.sh"', upgrade_script)
        self.assertNotIn('\n"$INSTALL_DIR/pi4/install_pi4.sh"', upgrade_script)


if __name__ == "__main__":
    unittest.main()
