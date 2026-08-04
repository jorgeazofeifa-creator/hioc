import hashlib
import importlib.util
import json
import os
import stat
import tempfile
import unittest
import sys
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"pi4/lib"))
SPEC = importlib.util.spec_from_file_location("pe2_cleanup", ROOT / "tools/hioc-pe2-clean-synthetic-backups.py")
M = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(M)
ID = M.RESERVED_ID


def record(device_id=ID):
    return {"stable_device_id":device_id,"friendly_name":"Synthetic","physical_location":None,
            "purpose":None,"notes":None,"created_at":"2000-01-01T00:00:00.000000Z",
            "updated_at":"2000-01-01T00:00:00.000000Z","update_source":"operator_cli","revision":1}


def store(records=None, count=None, version="1.0"):
    records=records if records is not None else {ID:record()}
    return {"schema_version":version,"updated_at":"2000-01-01T00:00:00.000000Z",
            "asset_count":len(records) if count is None else count,"assets":records}


class CleanupTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name); self.files=[]
    def tearDown(self): self.tmp.cleanup()
    def metadata(self,path): return 0o600,"jazofv1","jazofv1",path.lstat()
    def add(self,index=1,payload=None,name=None):
        name=name or f"assets-20000101T000000{index:06d}Z-{'a'*12}.json"
        path=self.root/name; raw=json.dumps(payload if payload is not None else store(),separators=(",",":")).encode(); path.write_bytes(raw)
        self.files.append((name,hashlib.sha256(raw).hexdigest())); return path
    def manifest(self,entries=None):
        path=self.root/"manifest.json"; rows=entries if entries is not None else [{"basename":n,"sha256":d} for n,d in self.files]
        path.write_text(json.dumps({"schema_version":1,"purpose":"current-run-pe2-validation-cleanup","entries":rows}),encoding="utf-8"); return path
    def execute(self,delete=True,entries=None): return M.run(self.manifest(entries),self.root,delete,self.metadata)

    def test_exact_six_file_cleanup(self):
        for i in range(6): self.add(i)
        report,rc=self.execute(); self.assertEqual((rc,report["files_validated"],report["files_deleted"]),(0,6,6)); self.assertFalse(any((self.root/n).exists() for n,_ in self.files))
    def test_one_time_manifest_is_closed_and_exact(self):
        payload=M._load_manifest(ROOT/"tools/pe2-synthetic-backup-cleanup-manifest.json")
        self.assertEqual(len(payload["entries"]),6)
        self.assertEqual(payload["entries"][0]["sha256"],"b4225a25e2c5af216a438c134501b10fb5ae23958ece1cbd5c1dcc219270c598")
        self.assertEqual(payload["entries"][-1]["sha256"],"4548c6453e76dc8adecfdb1018ee78a01092b53ae48b004547eb2afe69bac86c")
    def test_sha_mismatch_prevents_all_deletion(self):
        self.add(); self.add(2); entries=[{"basename":n,"sha256":("0"*64 if i else d)} for i,(n,d) in enumerate(self.files)]
        report,rc=self.execute(entries=entries); self.assertEqual(rc,20); self.assertTrue(all((self.root/n).exists() for n,_ in self.files))
    def test_missing_basename_prevents_all_deletion(self):
        self.add(); entries=[{"basename":"assets-20000101T000009999999Z-bbbbbbbbbbbb.json","sha256":self.files[0][1]}]
        self.assertEqual(self.execute(entries=entries)[1],20); self.assertTrue((self.root/self.files[0][0]).exists())
    def test_traversal_and_absolute_rejected(self):
        for name in ("../assets-20000101T000000000000Z-aaaaaaaaaaaa.json",str((self.root/"assets-20000101T000000000000Z-aaaaaaaaaaaa.json").resolve())):
            with self.assertRaises(M.CleanupError): M._load_manifest(self.manifest([{"basename":name,"sha256":"0"*64}]))
    def test_symlink_and_directory_rejected(self):
        target=self.add(); link=self.root/"assets-20000101T000009999999Z-bbbbbbbbbbbb.json"
        try: link.symlink_to(target)
        except OSError: self.skipTest("symlink unavailable")
        digest=hashlib.sha256(target.read_bytes()).hexdigest(); entries=[{"basename":link.name,"sha256":digest}]
        self.assertEqual(self.execute(entries=entries)[1],20)
        link.unlink(); link.mkdir(); self.assertEqual(self.execute(entries=entries)[1],20)
    def test_malformed_unsupported_and_count_mismatch_prevent_deletion(self):
        cases=[b"{",json.dumps(store(version="2.0")).encode(),json.dumps(store(count=2)).encode()]
        for raw in cases:
            self.files=[]; path=self.root/"assets-20000101T000000000001Z-aaaaaaaaaaaa.json"; path.write_bytes(raw); self.files=[(path.name,hashlib.sha256(raw).hexdigest())]
            self.assertEqual(self.execute()[1],20); self.assertTrue(path.exists()); path.unlink()
    def test_real_mixed_and_other_synthetic_id_rejected(self):
        other="dev_1111111111111111"
        for records in ({other:record(other)},{ID:record(),other:record(other)}):
            self.files=[]; path=self.add(payload=store(records)); self.assertEqual(self.execute()[1],20); self.assertTrue(path.exists()); path.unlink()
    def test_validate_only_retains_exact_candidate_and_sanitizes_output(self):
        self.add(); report,rc=self.execute(delete=False); encoded=json.dumps(report)
        self.assertEqual((rc,report["cleanup_result"],report["files_deleted"]),(0,"VALIDATED",0)); self.assertNotIn(ID,encoded); self.assertNotIn("Synthetic",encoded)
    def test_metadata_and_outside_root_rejected(self):
        self.add(); manifest=M._load_manifest(self.manifest())
        bad=lambda path:(0o644,"jazofv1","jazofv1",path.lstat())
        with self.assertRaises(M.CleanupError): M.validate_candidates(manifest,self.root,bad)
        with self.assertRaises(M.CleanupError): M.validate_candidates(manifest,self.root/"missing",self.metadata)
    def test_partial_delete_reports_exact_remaining(self):
        self.add(); self.add(2); original=Path.unlink; calls=[]
        def unlink(path):
            calls.append(path.name)
            if len(calls)==2: raise OSError("synthetic failure")
            return original(path)
        with mock.patch.object(Path,"unlink",unlink): report,rc=self.execute()
        self.assertEqual(rc,30); self.assertEqual(report["files_deleted"],1); self.assertEqual(len(report["remaining_basenames"]),1)
    def test_source_has_no_wildcard_or_recursive_deletion(self):
        text=(ROOT/"tools/hioc-pe2-clean-synthetic-backups.py").read_text(encoding="utf-8")
        for forbidden in ("glob(","rglob(","shutil.rmtree","rm -rf","assets/*"): self.assertNotIn(forbidden,text)


if __name__ == "__main__": unittest.main()
