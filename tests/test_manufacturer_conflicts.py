"""synthetic fixture; not sourced from IEEE"""
import copy, hashlib, json, os, pathlib, subprocess, sys, tempfile, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"pi4"/"lib"))
from hioc.manufacturer import *
from test_manufacturer_schema import database, write_pair, STAMP
SCRIPT=ROOT/"pi4"/"bin"/"hioc-build-manufacturer-db.py"; PY=sys.executable

def rehash(db):
    db["semantic_sha256"]=semantic_sha256({k:v for k,v in db.items() if k!="semantic_sha256"}); return db

def conflict_database(bits=36, prefix="A0B1C2D3E", cls="MA-S", variants=2):
    db=database(); key=f"{bits}:{prefix}"; record=db["records"].pop(key); count_key={"MA-L":"ma_l_count","MA-M":"ma_m_count","MA-S":"ma_s_count"}[cls]
    db["record_count"]-=1; db[count_key]-=1; db["conflict_count"]=1
    db["conflicts"]={key:{"prefix":prefix,"prefix_length":bits,"assignment_class":cls,"variant_count":variants}}
    return rehash(db)

def write_database_pair(root, db):
    _,mf=write_pair(root); data=canonical_json_bytes(db); (root/"manufacturer-db.json").write_bytes(data)
    mf.update(database_sha256=hashlib.sha256(data).hexdigest(),database_size_bytes=len(data),database_semantic_sha256=db["semantic_sha256"],record_count=db["record_count"],ma_l_count=db["ma_l_count"],ma_m_count=db["ma_m_count"],ma_s_count=db["ma_s_count"],conflict_count=db["conflict_count"])
    (root/"manufacturer-db.manifest.json").write_bytes(canonical_json_bytes(mf))

class ManufacturerConflictTests(unittest.TestCase):
    def load(self, db):
        td=tempfile.TemporaryDirectory(); self.addCleanup(td.cleanup); root=pathlib.Path(td.name); write_database_pair(root,db); return load_database(root/"manufacturer-db.json",root/"manufacturer-db.manifest.json")
    def test_conflict_schema_and_semantic_digest(self):
        db=conflict_database(); self.assertEqual(validate_database(db)["conflict_count"],1)
        changed=copy.deepcopy(db); changed["conflicts"]["36:A0B1C2D3E"]["variant_count"]=3
        with self.assertRaises(ManufacturerIntegrityError): validate_database(changed)
    def test_variant_count_below_two_rejected(self):
        db=conflict_database(variants=1); db=rehash(db)
        with self.assertRaises(ManufacturerValidationError): validate_database(db)
    def test_key_in_records_and_conflicts_rejected(self):
        db=database(); db["conflicts"]={"24:A0B1C2":{"prefix":"A0B1C2","prefix_length":24,"assignment_class":"MA-L","variant_count":2}}; db["conflict_count"]=1; db=rehash(db)
        with self.assertRaises(ManufacturerValidationError): validate_database(db)
    def test_malformed_conflict_key_rejected(self):
        db=conflict_database(); db["conflicts"]={"bad":next(iter(db["conflicts"].values()))}; db=rehash(db)
        with self.assertRaises(ManufacturerValidationError): validate_database(db)
    def test_conflict_class_and_length_must_agree(self):
        db=conflict_database(); db["conflicts"]["36:A0B1C2D3E"]["assignment_class"]="MA-L"; db=rehash(db)
        with self.assertRaises(ManufacturerValidationError): validate_database(db)
    def test_conflicted_36_blocks_shorter_fallback(self):
        result=lookup_manufacturer_eui48(self.load(conflict_database()),"A0:B1:C2:D3:E0:02")
        self.assertEqual(result.lookup_status,"conflicting_assignment"); self.assertIsNone(result.manufacturer); self.assertEqual(result.confidence,"unknown")
    def test_conflicted_28_blocks_24_fallback(self):
        result=lookup_manufacturer_eui48(self.load(conflict_database(28,"A0B1C2D","MA-M")),"A0:B1:C2:D0:00:02")
        self.assertEqual(result.lookup_status,"conflicting_assignment")
    def test_conflicted_24_returns_conflict(self):
        result=lookup_manufacturer_eui48(self.load(conflict_database(24,"A0B1C2","MA-L")),"A0:B1:C2:00:00:02")
        self.assertEqual(result.lookup_status,"conflicting_assignment")
    def test_sidecar_accepts_conflict_and_counts_unknown(self):
        db=self.load(conflict_database()); side,status=build_manufacturer_sidecar({"devices":[{"id":"dev_0000000000000001","mac":"A0:B1:C2:D3:E0:02"}]},db,generated_at=STAMP)
        record=side["records"]["dev_0000000000000001"]; self.assertEqual(record["lookup_status"],"conflicting_assignment"); self.assertIsNone(record["manufacturer"]); self.assertEqual(side["unknown_count"],1); self.assertEqual(status["conflict_count"],1)

class ManufacturerConflictBuilderTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup); self.root=pathlib.Path(self.tmp.name); self.files={}
        for cls,prefix,name in (("MA-L","A0B1C2","Fictional Lantern Works"),("MA-M","A0B1C2D","Synthetic Meadow Labs"),("MA-S","A0B1C2D3E","Imaginary Harbor Systems")):
            p=self.root/f"synthetic-{cls.lower()}.csv"; p.write_text(f"Registry,Assignment,Organization Name,Marker\n{cls},{prefix},{name},synthetic fixture; not sourced from IEEE\n",encoding="utf-8"); self.files[cls]=p
    def args(self,out):
        args=[]
        for cls,flag in (("MA-L","ma-l"),("MA-M","ma-m"),("MA-S","ma-s")):
            p=self.files[cls]; args += [f"--{flag}",str(p),f"--{flag}-sha256",hashlib.sha256(p.read_bytes()).hexdigest()]
        return args+["--dataset-id","synthetic-local","--dataset-version","fixture-r1","--output-directory",str(out),"--json"]
    def invoke(self,out):
        env=os.environ.copy(); env["HIOC_HOME"]=str(ROOT); return subprocess.run([PY,str(SCRIPT),*self.args(out)],env=env,capture_output=True,text=True)
    def add_variants(self, lines):
        with self.files["MA-L"].open("a",encoding="utf-8") as handle:
            for name in lines: handle.write(f"MA-L,A0B1C2,{name},synthetic fixture; not sourced from IEEE\n")
    def test_three_variants_emit_one_conflict(self):
        self.add_variants(["Other Fictional Works","Third Synthetic Works"]); out=self.root/"three"; self.assertEqual(self.invoke(out).returncode,0)
        db=json.loads((out/"manufacturer-db.json").read_text(encoding="utf-8")); self.assertEqual(db["conflicts"]["24:A0B1C2"]["variant_count"],3); self.assertEqual(len(db["conflicts"]),1)
    def test_exact_duplicate_plus_variant(self):
        self.add_variants(["Fictional Lantern Works","Other Fictional Works"]); out=self.root/"mixed"; result=self.invoke(out); self.assertEqual(result.returncode,0)
        envelope=json.loads(result.stdout); self.assertEqual(envelope["duplicate_count"],1); self.assertEqual(envelope["conflict_count"],1); self.assertNotIn("Works",result.stdout+result.stderr)
    def test_same_length_independent_key_remains_selectable(self):
        with self.files["MA-L"].open("a",encoding="utf-8") as handle: handle.write("MA-L,A4B5C6,Independent Synthetic Works,synthetic fixture; not sourced from IEEE\n")
        out=self.root/"independent"; self.assertEqual(self.invoke(out).returncode,0); db=json.loads((out/"manufacturer-db.json").read_text(encoding="utf-8")); self.assertIn("24:A4B5C6",db["records"]); self.assertEqual(db["conflict_count"],0)
    def test_different_length_overlap_remains_selectable(self):
        out=self.root/"overlap"; self.assertEqual(self.invoke(out).returncode,0); db=json.loads((out/"manufacturer-db.json").read_text(encoding="utf-8")); self.assertTrue(all(key in db["records"] for key in ("24:A0B1C2","28:A0B1C2D","36:A0B1C2D3E")))
    def test_variant_order_is_byte_deterministic(self):
        self.add_variants(["Other Fictional Works","Third Synthetic Works"]); one=self.root/"one"; self.assertEqual(self.invoke(one).returncode,0)
        rows=self.files["MA-L"].read_text(encoding="utf-8").splitlines(); self.files["MA-L"].write_text("\n".join([rows[0],rows[1],rows[3],rows[2]])+"\n",encoding="utf-8"); two=self.root/"two"; self.assertEqual(self.invoke(two).returncode,0)
        self.assertEqual((one/"manufacturer-db.json").read_bytes(),(two/"manufacturer-db.json").read_bytes())
        first=json.loads((one/"manufacturer-db.manifest.json").read_text(encoding="utf-8")); second=json.loads((two/"manufacturer-db.manifest.json").read_text(encoding="utf-8")); self.assertEqual(first["database_semantic_sha256"],second["database_semantic_sha256"]); self.assertEqual(first["conflict_count"],second["conflict_count"])

if __name__ == "__main__": unittest.main()
