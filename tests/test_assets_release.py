import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AssetReleaseTests(unittest.TestCase):
    def test_installer_deploys_asset_tools_without_schedule(self):
        script = (ROOT / "pi4" / "install_pi4.sh").read_text(encoding="utf-8")
        self.assertIn('chmod +x "$INSTALL_DIR/pi4/bin/hioc-assets.py"', script)
        self.assertIn('chmod +x "$INSTALL_DIR/pi4/bin/hioc-validate-assets.py"', script)
        self.assertIn('chmod 0700 "$INSTALL_DIR/backups/assets"', script)
        for marker in ("CRON_ASSET", "hioc-assets.lock $INSTALL_DIR", "hioc-assets.py\""):
            self.assertNotIn(marker, "\n".join(line for line in script.splitlines() if "CRON_" in line))

    def test_runtime_validation_is_conditional_and_read_only(self):
        script = (ROOT / "pi4" / "validate_pi4.sh").read_text(encoding="utf-8")
        self.assertIn("hioc-validate-assets.py", script)
        self.assertNotIn("hioc-assets.py initialize", script)

    def test_upgrade_preserves_state_and_backups(self):
        script = (ROOT / "release" / "upgrade.sh").read_text(encoding="utf-8")
        self.assertGreaterEqual(script.count("--exclude state"), 2)
        self.assertGreaterEqual(script.count("--exclude backups"), 2)
        self.assertNotIn("--delete", script)

    def test_rollback_does_not_delete_asset_state_or_backups(self):
        script = (ROOT / "release" / "rollback.sh").read_text(encoding="utf-8")
        self.assertNotIn("--delete", script)
        self.assertNotIn("rm ", script)

    def test_prohibited_runtime_files_do_not_import_assets(self):
        for relative in ("pi4/lib/hioc/inventory.py", "pi4/lib/hioc/enrichment.py", "pi4/bin/hioc-inventory-engine.py"):
            self.assertNotIn("hioc.assets", (ROOT / relative).read_text(encoding="utf-8"))


if __name__ == "__main__": unittest.main()
