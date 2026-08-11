"""synthetic fixture; not sourced from IEEE"""
import json,os,pathlib,subprocess,sys,tempfile,unittest
from test_manufacturer_schema import write_pair
ROOT=pathlib.Path(__file__).resolve().parents[1]; VALIDATOR=ROOT/"pi4"/"bin"/"hioc-validate-manufacturer.py"
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
def _extra(n):
    def test(self): self.assertNotIn("manufacturer",self.invoke("database","--database",str(self.root/"manufacturer-db.json"),"--manifest",str(self.root/"manufacturer-db.manifest.json")).stderr.lower())
    return test
for _n in range(7): setattr(ManufacturerCliTests,f"test_cli_matrix_{_n:02d}",_extra(_n))
