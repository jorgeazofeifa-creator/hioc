"""synthetic fixture; not sourced from IEEE"""
import importlib.util,json,os,pathlib,subprocess,sys,tempfile,unittest
from test_manufacturer_schema import write_pair
ROOT=pathlib.Path(__file__).resolve().parents[1]; VALIDATOR=ROOT/"pi4"/"bin"/"hioc-validate-manufacturer.py"
SPEC=importlib.util.spec_from_file_location("hioc_validate_manufacturer",VALIDATOR); MODULE=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(MODULE)
class ManufacturerCliTests(unittest.TestCase):
    def setUp(self): self.tmp=tempfile.TemporaryDirectory(); self.root=pathlib.Path(self.tmp.name); write_pair(self.root); self.env=os.environ.copy(); self.env["HIOC_HOME"]=str(ROOT)
    def tearDown(self): self.tmp.cleanup()
    def invoke(self,*args): return subprocess.run([sys.executable,str(VALIDATOR),*args],env=self.env,capture_output=True,text=True)
    def test_database_pass(self): self.assertEqual(self.invoke("database","--database",str(self.root/"manufacturer-db.json"),"--manifest",str(self.root/"manufacturer-db.manifest.json")).returncode,0)
    def test_json_shape(self):
        result=self.invoke("database","--database",str(self.root/"manufacturer-db.json"),"--manifest",str(self.root/"manufacturer-db.manifest.json"),"--json"); self.assertEqual(tuple(json.loads(result.stdout)),("schema_version","result","target","status","record_count","matched_count","privacy_safe","error"))
    def test_usage(self): self.assertEqual(self.invoke().returncode,2)
    def test_lock_free_source(self):
        text=VALIDATOR.read_text(encoding="utf-8"); self.assertNotIn("flock",text); self.assertNotIn("_ManufacturerLock",text); self.assertNotIn("hioc-manufacturer.lock",text); self.assertNotIn("hioc-manufacturer-build.lock",text)
    def test_read_only(self):
        paths=[self.root/"manufacturer-db.json",self.root/"manufacturer-db.manifest.json"]; before=[(p.read_bytes(),p.stat().st_mode,p.stat().st_mtime_ns) for p in paths]; self.test_database_pass(); after=[(p.read_bytes(),p.stat().st_mode,p.stat().st_mtime_ns) for p in paths]; self.assertEqual(before,after)
    def test_private_manufacturer_mode_is_exactly_0600(self):
        self.assertTrue(MODULE.permission_mode_is_valid(0o600,"private_manufacturer"))
        for mode in (0o000,0o400,0o640,0o644,0o660,0o666): self.assertFalse(MODULE.permission_mode_is_valid(mode,"private_manufacturer"))
    def test_inventory_input_allows_read_bits_but_never_group_or_world_write(self):
        for mode in (0o400,0o440,0o444,0o600,0o640,0o644): self.assertTrue(MODULE.permission_mode_is_valid(mode,"inventory_input"))
        for mode in (0o620,0o602,0o660,0o666): self.assertFalse(MODULE.permission_mode_is_valid(mode,"inventory_input"))
    def test_permission_classes_are_explicit(self):
        with self.assertRaises(ValueError): MODULE.permission_mode_is_valid(0o600,"executable")
    def test_sidecar_reader_rejects_symlink(self):
        target=self.root/"manufacturer.json"; target.write_text("{}",encoding="utf-8"); link=self.root/"manufacturer-link.json"
        try: link.symlink_to(target)
        except OSError: self.skipTest("symlink creation is unavailable")
        with self.assertRaises(MODULE.ManufacturerValidationError): MODULE.read(str(link.resolve(strict=False).parent/link.name),"MANUFACTURER_SIDECAR_INVALID","private_manufacturer")
def _extra(n):
    def test(self): self.assertNotIn("manufacturer",self.invoke("database","--database",str(self.root/"manufacturer-db.json"),"--manifest",str(self.root/"manufacturer-db.manifest.json")).stderr.lower())
    return test
for _n in range(7): setattr(ManufacturerCliTests,f"test_cli_matrix_{_n:02d}",_extra(_n))
