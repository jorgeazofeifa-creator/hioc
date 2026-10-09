"""Synthetic transaction faults; never instantiate production NativeOps."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("projection_deploy",ROOT/"tools/hioc-pe4-ha-public-projection-deploy.py")
D = importlib.util.module_from_spec(spec); spec.loader.exec_module(D)
COMMIT = "a"*40
CRON = ("# unrelated\n\n"+D.MARKER+"\n"+D.ASSOCIATION+"\n"+D.INVENTORY+"\n"+D.PLATFORM+"\n0 2 * * * echo fixture\n").encode()

class Fixture:
    def __init__(self,root,fault=None):
        self.root = Path(root); self.fault = fault; self.events = []
        self.expected_cron_sha = D.sha(CRON); self.cron = CRON; self.reads = 0; self.installs = 0
        self.held = False; self.marker = False; self.stages = {}; self.created = set()
        self.old = b"synthetic old engine"; self.baseline_value = {"crontab_sha256":D.sha(CRON)}
        self.bytes = {p:(ROOT/p).read_bytes().replace(b"\r\n",b"\n") for p,_ in D.SET}
        self.protected = {p:(ROOT/p).read_bytes() for p in D.PRIVATE}
        for path,raw in {D.SET[2][0]:self.old,**self.protected,"unrelated":b"preserve"}.items(): self.write(path,raw)
    def hit(self,key):
        self.events.append(key)
        if self.fault == key or isinstance(self.fault,set) and key in self.fault: raise D.Failure("IO_FAILED")
        if self.fault == "interrupt:"+key: raise KeyboardInterrupt()
    def write(self,path,raw):
        p = self.root/path; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(raw)
    def read(self,path):
        p = self.root/path; return p.read_bytes() if p.exists() else None
    def source(self,commit): self.hit("source"); D.require(commit==COMMIT,"SOURCE_BINDING")
    def target(self): self.hit("target"); D.require(not self.marker,"TRANSACTION_CONFLICT")
    def baseline(self,value): self.hit("baseline"); D.require(value==self.baseline_value,"BASELINE_MISMATCH"); return self.old
    def cron_read(self):
        self.reads += 1; self.hit("cron_read:"+str(self.reads))
        if self.fault == "mismatch:"+str(self.reads): return b"unknown\n"
        return self.cron
    def cron_install(self,raw):
        self.installs += 1; self.hit("cron_install:"+str(self.installs)); self.cron = raw
        assert D.ASSOCIATION.encode()+b"\n" in raw and D.PLATFORM.encode()+b"\n" in raw
    def begin(self,*_): self.marker=True; self.hit("begin")
    def intent(self,stage): self.hit("intent:"+stage)
    @contextlib.contextmanager
    def inventory_lock(self):
        self.hit("lock")
        if self.fault == "busy": raise D.Failure("BUSY")
        self.held=True
        try: yield
        finally: self.held=False; self.events.append("unlock")
    def recheck(self,*_): self.hit("recheck"); assert self.held
    def source_bytes(self,path): self.hit("source_bytes:"+path); return self.bytes[path]
    def stage(self,path,raw,baseline):
        assert self.held and D.INVENTORY.encode() not in self.cron
        self.hit("stage:"+path); self.stages[path]=raw
    def install(self,path,raw,baseline):
        assert self.held and D.INVENTORY.encode() not in self.cron
        self.hit("install:"+path); self.created.add(path); self.write(path,raw)
    def verify(self,path,raw,baseline): self.hit("verify:"+path); D.require(self.read(path)==raw,"INSTALLED_MISMATCH")
    def installed(self,*_):
        self.hit("installed"); assert self.held
        for p,raw in self.bytes.items(): D.require(self.read(p)==raw,"INSTALLED_MISMATCH")
    def rollback(self,attempted,old,baseline):
        assert self.held; self.hit("rollback")
        for p in reversed(attempted):
            if p==D.SET[2][0]: self.write(p,old)
            elif p in self.created: (self.root/p).unlink()
        self.stages.clear()
    def verify_baseline(self,*_):
        self.hit("verify_baseline"); D.require(self.read(D.SET[2][0])==self.old,"BASELINE_MISMATCH")
        for p,_ in D.SET[:2]: D.require(self.read(p) is None,"BASELINE_MISMATCH")
    def finish(self): self.hit("finish"); self.marker=False; self.stages.clear()

class DeployTests(unittest.TestCase):
    def run_fixture(self,fault=None):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        ops = Fixture(temp.name,fault)
        out = D.execute(ops,COMMIT,ops.baseline_value,True)
        self.assertFalse(ops.held)
        for p,raw in ops.protected.items(): self.assertEqual(ops.read(p),raw)
        self.assertEqual(ops.read("unrelated"),b"preserve")
        self.assertTrue(out["STOP_REQUIRED"])
        for key in D.FALSE_FIELDS: self.assertFalse(out[key])
        self.assertIn(out["ERROR_CODE"],D.CODES); self.assertIn(out["FAILURE_STAGE"],D.STAGES)
        self.assertEqual(D.canonical(json.loads(D.canonical(out))),D.canonical(out))
        return ops,out
    def test_success_order_lock_and_exact_cron(self):
        ops,out=self.run_fixture()
        self.assertEqual(out["RESULT"],"PASS"); self.assertEqual(out["INSTALL_ATTEMPTS"],3)
        self.assertEqual(ops.cron,CRON); self.assertEqual(ops.installs,2)
        self.assertFalse(ops.marker); self.assertFalse(ops.stages)
        indices=[ops.events.index("install:"+p) for p,_ in D.SET]
        self.assertEqual(indices,sorted(indices)); self.assertLess(ops.events.index("cron_install:1"),indices[0])
        self.assertLess(indices[-1],ops.events.index("installed")); self.assertLess(ops.events.index("installed"),ops.events.index("cron_install:2"))
        self.assertLess(ops.events.index("cron_install:2"),ops.events.index("unlock"))
    def test_inert_controller(self):
        with tempfile.TemporaryDirectory() as root:
            ops=Fixture(root); out=D.execute(ops,COMMIT,None)
            self.assertEqual(out["ERROR_CODE"],"AUTHORIZATION_REQUIRED"); self.assertEqual(ops.events,[])
    def test_inert_cli_without_authorization(self):
        with patch.object(D,"NativeOps",side_effect=AssertionError("native")),contextlib.redirect_stdout(io.StringIO()) as stream:
            self.assertEqual(D.main(["--baseline-report","secret-canary"]),1)
        self.assertNotIn("secret-canary",stream.getvalue()); self.assertEqual(json.loads(stream.getvalue())["ERROR_CODE"],"AUTHORIZATION_REQUIRED")
    def test_invalid_authorized_arguments_do_not_construct_native(self):
        with patch.object(D,"NativeOps",side_effect=AssertionError("native")),contextlib.redirect_stdout(io.StringIO()) as stream:
            self.assertEqual(D.main(["--deploy-authorized","secret-canary"]),1)
        self.assertNotIn("secret-canary",stream.getvalue())
    def test_busy_restores_exact_original_once(self):
        ops,out=self.run_fixture("busy")
        self.assertEqual(out["ERROR_CODE"],"BUSY"); self.assertEqual(out["FAILURE_STAGE"],"INVENTORY_DRAIN")
        self.assertEqual(ops.installs,2); self.assertEqual(ops.cron,CRON); self.assertFalse(ops.marker)
        self.assertEqual(out["INSTALL_ATTEMPTS"],0); self.assertFalse(out["ROLLBACK_PERFORMED"])
    def test_unknown_maintenance_no_rollback_or_restore_retry(self):
        for fault in ("cron_install:1","mismatch:2","cron_read:2"):
            with self.subTest(fault=fault):
                ops,out=self.run_fixture(fault)
                self.assertEqual(ops.installs,1); self.assertEqual(out["MUTATION_STATE"],"UNKNOWN_AFTER_ATTEMPT")
                self.assertFalse(out["ROLLBACK_PERFORMED"]); self.assertTrue(out["MANUAL_REVIEW_REQUIRED"])
                self.assertFalse(out["ASSOCIATION_CRON_UNCHANGED"]); self.assertFalse(out["PLATFORM_CRON_UNCHANGED"])
    def test_failed_restore_never_automatically_undoes_installed_code(self):
        for fault in ("cron_install:2","mismatch:5","cron_read:5"):
            with self.subTest(fault=fault):
                ops,out=self.run_fixture(fault)
                self.assertEqual(out["RESULT"],"FAIL"); self.assertFalse(out["ROLLBACK_PERFORMED"])
                self.assertTrue(out["MANUAL_REVIEW_REQUIRED"]); self.assertEqual(ops.installs,2)
                for p,raw in ops.bytes.items(): self.assertEqual(ops.read(p),raw)
    def test_runtime_faults_restore_only_provenance_and_exact_original(self):
        faults=["recheck","installed"]+[kind+":"+p for kind in ("stage","install","verify","source_bytes") for p,_ in D.SET]
        for fault in faults:
            with self.subTest(fault=fault):
                ops,out=self.run_fixture(fault)
                self.assertEqual(out["RESULT"],"FAIL"); self.assertEqual(ops.cron,CRON)
                self.assertEqual(ops.read(D.SET[2][0]),ops.old)
                for p,_ in D.SET[:2]: self.assertIsNone(ops.read(p))
                self.assertFalse(ops.marker); self.assertFalse(ops.stages); self.assertEqual(ops.installs,2)
    def test_interruption_leaves_marker_fresh_invocation_stops(self):
        points=["begin","intent:INVENTORY_QUIESCE","intent:INVENTORY_DRAIN","installed","intent:CRONTAB_RESTORE","intent:FINAL_VERIFY"]+["verify:"+p for p,_ in D.SET]
        for point in points:
            with self.subTest(point=point):
                ops,out=self.run_fixture("interrupt:"+point)
                self.assertEqual(out["ERROR_CODE"],"INTERRUPTED"); self.assertTrue(ops.marker)
                installs=ops.installs; ops.fault=None
                again=D.execute(ops,COMMIT,ops.baseline_value,True)
                self.assertEqual(again["ERROR_CODE"],"TRANSACTION_CONFLICT"); self.assertEqual(ops.installs,installs)
    def test_failed_rollback_cannot_claim_verified_restoration(self):
        for point in ("rollback","verify_baseline","cron_install:2","finish"):
            with self.subTest(point=point):
                ops,out=self.run_fixture({"verify:"+D.SET[2][0],point})
                self.assertTrue(out["MANUAL_REVIEW_REQUIRED"])
                self.assertEqual(out["ROLLBACK_RESULT"],"FAILED_OR_UNKNOWN")
                self.assertTrue(all(out[k] is False for k in ("PUBLIC_SCHEMA_INSTALLED","PUBLIC_HELPER_INSTALLED","INVENTORY_ENGINE_INSTALLED","DEPLOYED_SET_VERIFIED")))
                self.assertEqual(out["MUTATION_STATE"],"UNKNOWN_AFTER_ATTEMPT")
                self.assertLessEqual(ops.installs,2)
    def test_preflight_failures_do_not_mutate(self):
        for fault in ("source","target","baseline","cron_read:1"):
            with self.subTest(fault=fault):
                ops,out=self.run_fixture(fault)
                self.assertEqual(out["RESULT"],"FAIL"); self.assertEqual(ops.installs,0)
                self.assertFalse(ops.marker); self.assertEqual(ops.cron,CRON)
    def test_missing_baseline_has_no_cron_read(self):
        with tempfile.TemporaryDirectory() as root:
            ops=Fixture(root); out=D.execute(ops,COMMIT,None,True)
            self.assertEqual(out["ERROR_CODE"],"BASELINE_REQUIRED"); self.assertEqual(ops.reads,0)
    def test_source_identity_rejects_each_changed_field(self):
        good={"host":"nutandpihole","operator":"jazofv1","source":D.SOURCE,"branch":"main","head":COMMIT,"origin":COMMIT,"ahead":0,"behind":0,"clean":True,"active_operation":False,"subject":D.SUBJECT,"parent":D.PARENT,"implementation":D.IMPLEMENTATION,"tool":D.SOURCE+"/"+D.TOOL}
        D.source_authority(good,COMMIT)
        for key in good:
            with self.subTest(key=key),self.assertRaises(D.Failure): D.source_authority({**good,key:None},COMMIT)
    def test_cron_preserves_all_other_bytes(self):
        candidate=D.cron_candidate(CRON,D.sha(CRON))
        self.assertEqual(candidate,CRON.replace((D.INVENTORY+"\n").encode(),b""))
    def test_cron_rejects_duplicates_alternates_and_ambiguous_bytes(self):
        variants=[CRON.replace((s+"\n").encode(),b"") for s in (D.INVENTORY,D.ASSOCIATION,D.PLATFORM,D.MARKER)]
        variants += [CRON+(s+"\n").encode() for s in (D.INVENTORY,D.ASSOCIATION,D.PLATFORM,D.MARKER)]
        variants += [CRON.replace(b"*/30",b"*/10"),CRON.replace(b"\n",b"\r\n"),CRON[:-1],CRON+b"\0\n",CRON+b"* * * * * public-projection\n",CRON+b"* * * * * alternate hioc-inventory-engine.py\n"]
        for raw in variants:
            with self.subTest(raw=raw[-20:]),self.assertRaises(D.Failure): D.cron_candidate(raw,D.sha(raw))
    def test_no_arbitrary_exception_output(self):
        with patch.object(D,"NativeOps",side_effect=RuntimeError("private-canary")),contextlib.redirect_stdout(io.StringIO()) as stream:
            D.main(["--preparation-commit",COMMIT,"--baseline-report","/home/jazofv1/pe4-public-projection-baseline.json","--baseline-sha256","b"*64,"--deploy-authorized"])
        self.assertNotIn("private-canary",stream.getvalue())

if __name__ == "__main__": unittest.main()

class NativeSecurityTests(unittest.TestCase):
    def setUp(self):
        self.raw=(ROOT/D.SECURITY_DEPENDENCY).read_bytes().replace(b"\r\n",b"\n")
        self.cls=D.native_fs_class(self.raw)
    def test_only_accepted_read_methods_extracted(self):
        self.assertFalse(hasattr(self.cls,"replace_config")); self.assertFalse(hasattr(self.cls,"add")); self.assertFalse(hasattr(self.cls,"lock"))
        with self.assertRaises(D.Failure):D.native_fs_class(self.raw+b"\n")
    def test_security_rejects_mode_owner_link_type_and_acl(self):
        import errno,os,stat
        from types import SimpleNamespace
        good=dict(st_mode=stat.S_IFREG|0o644,st_uid=1000,st_gid=1000,st_nlink=1)
        fs=self.cls("/synthetic",1000,1000)
        def noattr(*_):raise OSError(errno.ENODATA,"fixture")
        with patch.object(os,"getxattr",side_effect=noattr,create=True),patch.object(os,"fstat",return_value=SimpleNamespace(**good)):
            fs.security(10,mode=0o644)
        for changes in ({"st_mode":stat.S_IFLNK|0o644},{"st_mode":stat.S_IFREG|0o666},{"st_uid":2000},{"st_nlink":2},{"st_mode":stat.S_IFREG|0o4644},{"st_gid":2000}):
            with self.subTest(changes=changes),patch.object(os,"getxattr",side_effect=noattr,create=True),patch.object(os,"fstat",return_value=SimpleNamespace(**(good|changes))),self.assertRaises(D.Failure):fs.security(10,mode=0o644)
        with patch.object(os,"getxattr",return_value=b"acl",create=True),patch.object(os,"fstat",return_value=SimpleNamespace(**good)),self.assertRaises(D.Failure):fs.security(10)
    def test_directory_closes_child_and_parent_once_when_child_unsafe(self):
        import os
        fs=self.cls("/synthetic",1000,1000)
        with patch.object(os,"O_DIRECTORY",0,create=True),patch.object(os,"O_NOFOLLOW",0,create=True),patch.object(os,"O_CLOEXEC",0,create=True),patch.object(os,"open",side_effect=[11,12]),patch.object(os,"close") as close,patch.object(fs,"security",side_effect=[None,D.Failure("UNSAFE_OBJECT")]):
            with self.assertRaises(D.Failure):
                with fs.directory():pass
            self.assertEqual([call.args[0] for call in close.call_args_list],[12,11])
    def test_native_mutation_requires_lock(self):
        ops=D.NativeOps.__new__(D.NativeOps);ops.lock_fd=None
        for call in (lambda:ops.stage(D.SET[0][0],b"x",{}),lambda:ops.install(D.SET[0][0],b"x",{}),lambda:ops.rollback([],b"x",{})):
            with self.assertRaises(D.Failure) as caught:call()
            self.assertEqual(caught.exception.code,"BUSY")
    def test_installed_security_verification_rejects_owner_mode_inode_and_bytes(self):
        from types import SimpleNamespace
        ops=D.NativeOps.__new__(D.NativeOps)
        path=D.SET[0][0];info=SimpleNamespace(st_uid=1000,st_gid=1000,st_mode=0o644,st_dev=1,st_ino=2,st_nlink=1)
        ops.provenance={path:D.file_identity(info)}
        class FS:
            def read(self,*_):return b"wrong"
            def info(self,*_):return info
        ops.fs=FS()
        with self.assertRaises(D.Failure):ops.verify(path,b"expected",{})
        ops.fs.read=lambda *args:b"expected"
        for key in ("uid","gid","mode","inode","links"):
            old=ops.provenance[path][key];ops.provenance[path][key]=old+1
            with self.subTest(key=key),self.assertRaises(D.Failure):ops.verify(path,b"expected",{})
            ops.provenance[path][key]=old

class BaselineNativeGateTests(unittest.TestCase):
    def fixture(self):
        import stat,subprocess
        from types import SimpleNamespace
        old=subprocess.check_output(["git","show",D.IMPLEMENTATION+"^:"+D.SET[2][0]],cwd=ROOT)
        files={D.SET[2][0]:old,"state/inventory/inventory.json":b'{"devices":[]}'}
        info=SimpleNamespace(st_uid=1000,st_gid=1000,st_mode=stat.S_IFREG|0o755,st_dev=1,st_ino=2,st_nlink=1)
        class FS:
            def read(self,path,*_):return files.get(path)
            def info(self,path):return info if path in files else None
        ops=D.NativeOps.__new__(D.NativeOps);ops.uid=ops.gid=1000;ops.commit=COMMIT;ops.fs=FS()
        ops.target=lambda:None;ops.private=lambda:{"accepted":True};ops.runtime=lambda:{"accepted":True};ops.lock_identity=lambda:{"accepted":True}
        return ops,files,info
    def test_reviewed_baseline_candidate_passes_and_is_not_a_production_claim(self):
        ops,files,_=self.fixture();receipt=ops.observe_baseline()
        self.assertEqual(receipt["engine_sha256"],D.OLD_ENGINE);self.assertEqual(receipt["engine"]["mode"],0o755)
        self.assertEqual(ops.baseline(receipt),files[D.SET[2][0]])
    def test_wrong_or_missing_engine_bytes_fail_closed(self):
        for value in (None,b"unknown",b""):
            with self.subTest(value=value):
                ops,files,_=self.fixture();files[D.SET[2][0]]=value
                with self.assertRaises(D.Failure):ops.observe_baseline()
    def test_any_preexisting_helper_or_schema_is_rejected_even_exact(self):
        for path,digest in D.SET[:2]:
            with self.subTest(path=path):
                ops,files,_=self.fixture();files[path]=(ROOT/path).read_bytes()
                with self.assertRaises(D.Failure):ops.observe_baseline()
    def test_already_public_namespace_is_rejected(self):
        for raw in (b'{"devices":[{"home_assistant":{}}]}',b'{"devices":[],"home_assistant":{}}',b'{"devices":"unknown"}'):
            ops,files,_=self.fixture();files["state/inventory/inventory.json"]=raw
            with self.subTest(raw=raw),self.assertRaises(D.Failure):ops.observe_baseline()
    def test_engine_ownership_executable_and_mode_policy(self):
        import stat
        for key,value in (("st_uid",2000),("st_gid",2000),("st_mode",stat.S_IFREG|0o644),("st_mode",stat.S_IFREG|0o777),("st_mode",stat.S_IFREG|0o4755)):
            ops,_,info=self.fixture();setattr(info,key,value)
            with self.subTest(key=key,value=value),self.assertRaises(D.Failure):ops.observe_baseline()
    def test_receipt_drift_every_field_is_rejected(self):
        ops,_,_=self.fixture();receipt=ops.observe_baseline()
        for key in receipt:
            with self.subTest(key=key),self.assertRaises(D.Failure):ops.baseline({**receipt,key:None})
    def test_wrong_production_root_rejected_before_filesystem_access(self):
        ops=D.NativeOps.__new__(D.NativeOps)
        with patch.object(Path,"resolve",return_value=Path("/synthetic-unexpected")),self.assertRaises(D.Failure):ops.target()
    def test_strict_json_rejects_duplicate_keys_constants_and_unbounded_receipt(self):
        for raw in (b'{"a":1,"a":2}',b'{"a":NaN}',b'{invalid',b'x'*(D.LIMIT+1)):
            with self.subTest(length=len(raw)),self.assertRaises(D.Failure):D.strict_json(raw)
