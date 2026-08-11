"""synthetic fixture; not sourced from IEEE"""
import pathlib,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
class ManufacturerReleaseTests(unittest.TestCase):
    def test_installs_scripts(self):
        text=(ROOT/"pi4"/"install_pi4.sh").read_text(encoding="utf-8")
        for name in ("hioc-build-manufacturer-db.py","hioc-validate-manufacturer.py","hioc-generate-manufacturer.py","manufacturer.py"): self.assertIn(name,text)
    def test_modes(self):
        text=(ROOT/"pi4"/"install_pi4.sh").read_text(encoding="utf-8"); self.assertIn('chmod 0600 "$INSTALL_DIR/pi4/lib/hioc/manufacturer.py"',text); self.assertEqual(text.count("chmod 0700 \"$INSTALL_DIR/pi4/bin/hioc-"),3)
    def test_data_directory(self): self.assertIn('data/manufacturer/versions', (ROOT/"pi4"/"install_pi4.sh").read_text(encoding="utf-8"))
    def test_upgrade_preserves(self): self.assertGreaterEqual((ROOT/"release"/"upgrade.sh").read_text(encoding="utf-8").count("--exclude data/manufacturer"),2)
    def test_rollback_preserves(self): self.assertIn("--exclude data/manufacturer",(ROOT/"release"/"rollback.sh").read_text(encoding="utf-8"))
    def test_no_schedule(self):
        text="".join((ROOT/"pi4"/"install_pi4.sh").read_text(encoding="utf-8").splitlines()); self.assertNotIn("CRON_MANUFACTURER",text)
    def test_no_dataset_bundled(self): self.assertFalse(any(ROOT.glob("**/manufacturer-db.json")))
    def test_config_empty(self): self.assertIn('MANUFACTURER_DB_PATH=""',(ROOT/"pi4"/"config"/"hioc.conf.example").read_text(encoding="utf-8"))
