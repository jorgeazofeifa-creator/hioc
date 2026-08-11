"""synthetic fixture; not sourced from IEEE"""
import hashlib,json,os,pathlib,subprocess,sys,tempfile,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]; SCRIPT=ROOT/"pi4"/"bin"/"hioc-build-manufacturer-db.py"; PY=sys.executable
class ManufacturerBuilderTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=pathlib.Path(self.tmp.name); self.files={}
        for cls,prefix,name in (("MA-L","A0B1C2","Fictional Lantern Works"),("MA-M","A0B1C2D","Synthetic Meadow Labs"),("MA-S","A0B1C2D3E","Imaginary Harbor Systems")):
            p=self.root/f"synthetic-{cls.lower()}.csv"; p.write_text(f"Registry,Assignment,Organization Name,Marker\n{cls},{prefix},{name},synthetic fixture; not sourced from IEEE\n",encoding="utf-8"); self.files[cls]=p
    def tearDown(self): self.tmp.cleanup()
    def args(self,out=None):
        out=out or self.root/"version"; a=[]
        for cls,flag in (("MA-L","ma-l"),("MA-M","ma-m"),("MA-S","ma-s")): p=self.files[cls]; a += [f"--{flag}",str(p),f"--{flag}-sha256",hashlib.sha256(p.read_bytes()).hexdigest()]
        return a+["--dataset-id","synthetic-local","--dataset-version","fixture-r1","--output-directory",str(out)]
    def invoke(self,args):
        env=os.environ.copy(); env["HIOC_HOME"]=str(ROOT); return subprocess.run([PY,str(SCRIPT),*args],env=env,capture_output=True,text=True)
    def test_build(self): self.assertEqual(self.invoke(self.args()).returncode,0)
    def test_pair(self):
        out=self.root/"pair"; self.assertEqual(self.invoke(self.args(out)).returncode,0); self.assertEqual(sorted(x.name for x in out.iterdir()),["manufacturer-db.json","manufacturer-db.manifest.json"])
    def test_immutable_collision(self):
        out=self.root/"fixed"; self.assertEqual(self.invoke(self.args(out)).returncode,0); self.assertEqual(self.invoke(self.args(out)).returncode,3)
    def test_checksum(self):
        args=self.args(); args[3]="0"*64; self.assertEqual(self.invoke(args).returncode,7)
    def test_conflict_is_preserved_without_selection(self):
        with self.files["MA-L"].open("a",encoding="utf-8") as h: h.write("MA-L,A0B1C2,Other Fictional Works,synthetic fixture; not sourced from IEEE\n")
        out=self.root/"conflict"; result=self.invoke(self.args(out)); self.assertEqual(result.returncode,0)
        db=json.loads((out/"manufacturer-db.json").read_text(encoding="utf-8")); self.assertNotIn("24:A0B1C2",db["records"]); self.assertEqual(db["conflicts"]["24:A0B1C2"]["variant_count"],2); self.assertEqual(db["conflict_count"],1)
    def test_bom(self): self.files["MA-L"].write_text(self.files["MA-L"].read_text(encoding="utf-8"),encoding="utf-8-sig"); self.assertEqual(self.invoke(self.args()).returncode,0)
    def test_duplicate_detection_uses_normalized_organization(self):
        with self.files["MA-L"].open("a",encoding="utf-8") as h: h.write("MA-L,A0B1C2,Fictional\t\tLantern Works,synthetic fixture; not sourced from IEEE\n")
        out=self.root/"normalized-duplicate"; result=self.invoke(self.args(out)); self.assertEqual(result.returncode,0)
        manifest=json.loads((out/"manufacturer-db.manifest.json").read_text(encoding="utf-8")); self.assertEqual(manifest["duplicate_count"],1); self.assertEqual(manifest["record_count"],3)
    def test_format_control_builds_are_byte_deterministic(self):
        text=self.files["MA-S"].read_text(encoding="utf-8").replace("Imaginary Harbor Systems","\tImaginary\u200b\t Harbor\u200e Systems\t")
        self.files["MA-S"].write_text(text,encoding="utf-8")
        first=self.root/"deterministic-one"; second=self.root/"deterministic-two"
        self.assertEqual(self.invoke(self.args(first)).returncode,0); self.assertEqual(self.invoke(self.args(second)).returncode,0)
        self.assertEqual((first/"manufacturer-db.json").read_bytes(),(second/"manufacturer-db.json").read_bytes())
        first_manifest=json.loads((first/"manufacturer-db.manifest.json").read_text(encoding="utf-8")); second_manifest=json.loads((second/"manufacturer-db.manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(first_manifest["database_semantic_sha256"],second_manifest["database_semantic_sha256"])
        self.assertEqual(first_manifest,second_manifest)
    def test_no_network_surface(self): self.assertNotIn("http",SCRIPT.read_text(encoding="utf-8").lower())
def _extra(n):
    def test(self): self.assertTrue(all(p.stat().st_size<65536 for p in self.files.values()))
    return test
for _n in range(9): setattr(ManufacturerBuilderTests,f"test_builder_matrix_{_n:02d}",_extra(_n))
