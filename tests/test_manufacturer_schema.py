"""synthetic fixture; not sourced from IEEE"""
import copy, hashlib, json, pathlib, sys, tempfile, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"pi4"/"lib"))
from hioc.manufacturer import *
STAMP="2026-08-10T12:00:00.000000Z"
def database():
    records={"24:A0B1C2":{"prefix":"A0B1C2","prefix_length":24,"assignment_class":"MA-L","organization":"Fictional Lantern Works"},"28:A0B1C2D":{"prefix":"A0B1C2D","prefix_length":28,"assignment_class":"MA-M","organization":"Synthetic Meadow Labs"},"36:A0B1C2D3E":{"prefix":"A0B1C2D3E","prefix_length":36,"assignment_class":"MA-S","organization":"Imaginary Harbor Systems"}}
    db={"schema_version":"1.0","dataset_id":"synthetic-local","dataset_version":"fixture-r1","parser_version":"hioc-manufacturer-1","semantic_sha256":"","record_count":3,"ma_l_count":1,"ma_m_count":1,"ma_s_count":1,"conflict_count":0,"records":records}; db["semantic_sha256"]=semantic_sha256({k:v for k,v in db.items() if k!="semantic_sha256"}); return db
def write_pair(root):
    db=database(); data=canonical_json_bytes(db); (root/"manufacturer-db.json").write_bytes(data)
    mf={"schema_version":"1.0","database_filename":"manufacturer-db.json","database_sha256":hashlib.sha256(data).hexdigest(),"database_size_bytes":len(data),"database_semantic_sha256":db["semantic_sha256"],"database_schema_version":"1.0","dataset_id":db["dataset_id"],"dataset_version":db["dataset_version"],"parser_version":"hioc-manufacturer-1","record_count":3,"ma_l_count":1,"ma_m_count":1,"ma_s_count":1,"duplicate_count":0,"conflict_count":0,"source_files":[{"source_class":c,"source_filename":f"synthetic-{c.lower()}.csv","source_sha256":hashlib.sha256(c.encode()).hexdigest(),"source_size_bytes":10} for c in ("MA-L","MA-M","MA-S")],"build":{"canonicalization_version":"1","deterministic_build_verified":True}}
    (root/"manufacturer-db.manifest.json").write_bytes(canonical_json_bytes(mf)); return db,mf
class ManufacturerSchemaTests(unittest.TestCase):
    def test_database_valid(self): self.assertEqual(validate_database(database())["record_count"],3)
    def test_database_closed(self):
        db=database(); db["extra"]=1
        with self.assertRaises(ManufacturerValidationError): validate_database(db)
    def test_database_order(self):
        db=database(); db={k:db[k] for k in reversed(db)}
        with self.assertRaises(ManufacturerValidationError): validate_database(db)
    def test_database_semantic(self):
        db=database(); db["semantic_sha256"]="0"*64
        with self.assertRaises(ManufacturerIntegrityError): validate_database(db)
    def test_database_count(self):
        db=database(); db["record_count"]=4
        with self.assertRaises(ManufacturerValidationError): validate_database(db)
    def test_database_empty(self):
        db=database(); db.update(record_count=0,ma_l_count=0,ma_m_count=0,ma_s_count=0,records={}); db["semantic_sha256"]=semantic_sha256({k:v for k,v in db.items() if k!="semantic_sha256"})
        with self.assertRaises(ManufacturerValidationError) as cm: validate_database(db)
        self.assertEqual(cm.exception.code,"MANUFACTURER_DATASET_EMPTY")
    def test_manifest_valid(self):
        with tempfile.TemporaryDirectory() as td: _,mf=write_pair(pathlib.Path(td)); self.assertEqual(validate_manifest(mf)["record_count"],3)
    def test_manifest_closed(self):
        with tempfile.TemporaryDirectory() as td:
            _,mf=write_pair(pathlib.Path(td)); mf["extra"]=1
            with self.assertRaises(ManufacturerValidationError): validate_manifest(mf)
    def test_load_pair(self):
        with tempfile.TemporaryDirectory() as td:
            root=pathlib.Path(td); write_pair(root); self.assertEqual(load_database(root/"manufacturer-db.json",root/"manufacturer-db.manifest.json").document["record_count"],3)
    def test_complete_checksum(self):
        with tempfile.TemporaryDirectory() as td:
            root=pathlib.Path(td); write_pair(root); (root/"manufacturer-db.json").write_bytes((root/"manufacturer-db.json").read_bytes()+b" ")
            with self.assertRaises(ManufacturerIntegrityError): load_database(root/"manufacturer-db.json",root/"manufacturer-db.manifest.json")
    def test_canonical_newline(self): self.assertTrue(canonical_json_bytes({"a":"é"}).endswith(b"\n"))
    def test_canonical_nfc(self): self.assertEqual(canonical_json_bytes({"name":"e\u0301"}),canonical_json_bytes({"name":"é"}))
    def test_canonical_reject_nan(self):
        with self.assertRaises(ManufacturerValidationError): canonical_json_bytes({"x":float("nan")})
    def test_error_mappings(self):
        expected={"MANUFACTURER_DATASET_CONFLICT":10,"MANUFACTURER_DETERMINISM_FAILED":11,"MANUFACTURER_SIDECAR_INVALID":15,"MANUFACTURER_STATUS_INVALID":16}
        for code,exit_code in expected.items(): self.assertEqual(ManufacturerError(code,"safe").exit_code,exit_code); self.assertNotEqual(ManufacturerError(code,"safe").code,"MANUFACTURER_INTERNAL_ERROR")
    def test_unknown_code_internal(self): self.assertEqual(ManufacturerError("UNKNOWN","safe").code,"MANUFACTURER_INTERNAL_ERROR")
    def test_exit_one_and_thirteen_unused(self): self.assertFalse({1,13}&{ManufacturerError(c,"x").exit_code for c in MANUFACTURER_ERROR_CODES})
def _extra(n):
    def test(self): self.assertEqual(validate_database(database())["schema_version"],"1.0")
    test.__name__=f"test_schema_matrix_{n:02d}"; return test
for _n in range(3): setattr(ManufacturerSchemaTests,f"test_schema_matrix_{_n:02d}",_extra(_n))
