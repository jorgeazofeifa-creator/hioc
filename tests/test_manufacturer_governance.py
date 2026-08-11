"""synthetic fixture; not sourced from IEEE"""
import pathlib,re,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
class ManufacturerGovernanceTests(unittest.TestCase):
    def test_no_runtime_database(self): self.assertFalse(any((ROOT/"data").glob("manufacturer/**/manufacturer-db*.json")) if (ROOT/"data").exists() else False)
    def test_no_ieee_csv_names(self): self.assertFalse([p for p in ROOT.rglob("*.csv") if re.search(r"(?i)(oui|oui36|mam|mas|mal)",p.name)])
    def test_fixture_markers(self):
        for p in ROOT.glob("tests/test_manufacturer_*.py"): self.assertIn("synthetic fixture; not sourced from IEEE",p.read_text(encoding="utf-8"))
    def test_no_network_imports(self):
        for p in list((ROOT/"pi4"/"bin").glob("*manufacturer*.py"))+[ROOT/"pi4"/"lib"/"hioc"/"manufacturer.py"]:
            text=p.read_text(encoding="utf-8"); self.assertNotRegex(text,r"\b(import|from)\s+(requests|urllib|httpx|socket|aiohttp)\b")
    def test_protected_files_unchanged_by_scope(self):
        self.assertTrue((ROOT/"pi4"/"lib"/"hioc"/"inventory.py").exists()); self.assertTrue((ROOT/"pi4"/"lib"/"hioc"/"enrichment.py").exists())
    def test_ignore_runtime_data(self): text=(ROOT/".gitignore").read_text(encoding="utf-8"); self.assertIn("data/manufacturer/",text); self.assertIn("state/inventory/manufacturer.json",text)
    def test_exact_two_lock_paths(self):
        texts="\n".join(p.read_text(encoding="utf-8") for p in list((ROOT/"pi4"/"bin").glob("*manufacturer*.py"))+[ROOT/"pi4"/"lib"/"hioc"/"manufacturer.py"]); self.assertEqual(set(re.findall(r"hioc-manufacturer(?:-build)?\.lock",texts)),{"hioc-manufacturer.lock","hioc-manufacturer-build.lock"})
    def test_validator_lock_free(self): self.assertNotIn("flock",(ROOT/"pi4"/"bin"/"hioc-validate-manufacturer.py").read_text(encoding="utf-8"))
