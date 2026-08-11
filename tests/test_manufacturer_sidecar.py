"""synthetic fixture; not sourced from IEEE"""
import json,os,pathlib,subprocess,sys,tempfile,unittest
from test_manufacturer_schema import STAMP,write_pair
ROOT=pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"pi4"/"lib")); from hioc.manufacturer import *
class ManufacturerSidecarTests(unittest.TestCase):
    def setUp(self): self.tmp=tempfile.TemporaryDirectory(); root=pathlib.Path(self.tmp.name); write_pair(root); self.db=load_database(root/"manufacturer-db.json",root/"manufacturer-db.manifest.json")
    def tearDown(self): self.tmp.cleanup()
    def build(self): return build_manufacturer_sidecar({"devices":[{"id":"dev_0000000000000001","mac":"A0:B1:C2:D3:E0:02"},{"id":"dev_0000000000000002","mac":None},{"id":"dev_0000000000000003","mac":"A2:00:00:00:00:02"}]},self.db,generated_at=STAMP)
    def test_records_mapping(self): side,_=self.build(); self.assertIsInstance(side["records"],dict)
    def test_counts(self): side,status=self.build(); self.assertEqual((side["record_count"],side["matched_count"],side["excluded_count"],side["invalid_count"]),(3,1,1,1)); self.assertEqual(status["record_count"],3)
    def test_no_raw_mac(self): side,_=self.build(); self.assertNotIn("A0:B1",str(side))
    def test_stable_key(self): side,_=self.build(); self.assertTrue(all(k==v["stable_device_id"] for k,v in side["records"].items()))
    def test_invalid_inventory(self):
        with self.assertRaises(ManufacturerValidationError): build_manufacturer_sidecar({"devices":[{"id":"bad"}]},self.db,generated_at=STAMP)
    def test_closed_sidecar(self):
        side,_=self.build(); side["extra"]=1
        with self.assertRaises(ManufacturerValidationError) as cm: validate_manufacturer_sidecar(side)
        self.assertEqual(cm.exception.code,"MANUFACTURER_SIDECAR_INVALID")
    def test_closed_status(self):
        _,status=self.build(); status["extra"]=1
        with self.assertRaises(ManufacturerValidationError) as cm: validate_manufacturer_status(status)
        self.assertEqual(cm.exception.code,"MANUFACTURER_STATUS_INVALID")
    def test_generator_lock_precedes_database_and_inventory_reads(self):
        text=(ROOT/"pi4"/"bin"/"hioc-generate-manufacturer.py").read_text(encoding="utf-8"); lock=text.index("with _ManufacturerLock(lock_path)"); self.assertGreater(text.index("database=load_database",lock),lock); self.assertGreater(text.index("inventory.read_text",lock),lock)
    def test_generator_uses_no_other_state_lock(self):
        text=(ROOT/"pi4"/"bin"/"hioc-generate-manufacturer.py").read_text(encoding="utf-8"); self.assertNotIn("inventory.lock",text); self.assertNotIn("assets.lock",text); self.assertNotIn("enrichment.lock",text)
    def test_generator_end_to_end_and_noop(self):
        home=pathlib.Path(self.tmp.name)/"home"; state=home/"state"/"inventory"; config=home/"config"; data=home/"data"; state.mkdir(parents=True); config.mkdir(); data.mkdir(); write_pair(data)
        (state/"inventory.json").write_text(json.dumps({"devices":[{"id":"dev_0000000000000001","mac":"A0:B1:C2:D3:E0:02"}]}),encoding="utf-8"); (config/"hioc.conf").write_text(f'MANUFACTURER_DB_PATH="{data / "manufacturer-db.json"}"\n',encoding="utf-8")
        env=os.environ.copy(); env["HIOC_HOME"]=str(ROOT); script=ROOT/"pi4"/"bin"/"hioc-generate-manufacturer.py"
        args=[sys.executable,str(script),"--home",str(home)]; first=subprocess.run(args,env=env,capture_output=True,text=True); self.assertEqual(first.returncode,0,first.stderr); before=(state/"manufacturer.json").read_bytes(); second=subprocess.run(args,env=env,capture_output=True,text=True); self.assertEqual(second.returncode,0,second.stderr); self.assertEqual(before,(state/"manufacturer.json").read_bytes())
def _extra(n):
    def test(self): side,status=self.build(); self.assertEqual(status["updated"],side["generated_at"])
    return test
for _n in range(5): setattr(ManufacturerSidecarTests,f"test_sidecar_matrix_{_n:02d}",_extra(_n))
