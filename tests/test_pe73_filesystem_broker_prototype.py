"""Focused nonprivileged Windows broker feasibility tests; no production access."""
import ast
import copy
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import stat
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("pe73_broker_prototype_tests", ROOT / "tools/pe73_filesystem_broker_prototype.py")
b = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(b)

class BrokerTests(unittest.TestCase):
    def setUp(self):
        self.f = b.Fixture()
    def tearDown(self):
        self.f.close()
    def request(self):
        self.f.fs.snapshot(self.f.d.ORDER[0], self.f.d.MODES[self.f.d.ORDER[0]])
        return copy.deepcopy(self.f.fs.last_request)
    def reject(self, request, token=None):
        with self.assertRaises(b.BrokerError):
            self.f.broker.exchange(b.canonical(request), object() if token is None else token)
    def stop_pending(self, path=None):
        value = self.f.prepare()
        target = path or self.f.d.ORDER[0]
        def stop(point):
            if point == "INTENT:" + target:
                raise KeyboardInterrupt()
        self.f.controller.fault = stop
        with self.assertRaises(KeyboardInterrupt):
            self.f.controller.commit("COMMIT_SYNTHETIC_BROKER", value["journal_sha256"])
        self.f.controller.fault = lambda _: None
        return self.f.controller._journal()
    def injected(self, point, operation):
        def fail(actual, request):
            if actual == point and request["operation"] == operation:
                raise OSError("private fault details must never leave the prototype")
        self.f.broker.fault = fail


    def test_only_synthetic_contents_and_identity_constants(self):
        self.f.d.check_sources(self.f.source)
        self.assertEqual(self.f.d.RELEASE, "f" * 40)
        for path, raw in self.f.source.items():
            self.assertEqual(raw, ("synthetic-candidate:" + path + "\n").encode())
        for path, raw in self.f.base.items():
            self.assertEqual(raw, ("synthetic-baseline:" + path + "\n").encode())

    def test_unlisted_absolute_traversal_and_backslash_paths(self):
        request = self.request()
        for path in ["../secret", "/home/jazofv1/hioc/pi4/lib/hioc/assets.py", "C:/private", "pi4/../secret", "pi4\\lib\\hioc\\assets.py", "config/hioc.conf"]:
            bad = copy.deepcopy(request); bad["artifact"] = path
            self.reject(bad)
            with self.assertRaises(b.BrokerError):self.f.disk.path(path)

    def test_unknown_operation_and_consumer_release_prohibited(self):
        request = self.request()
        for op in ["RELEASE_CONSUMERS", "CHMOD", "EXECUTE", "DELETE", "JOURNAL", "UNKNOWN"]:
            bad = copy.deepcopy(request); bad["operation"] = op; self.reject(bad)
        self.assertTrue(self.f.consumers.active)

    def test_closed_duplicate_nonfinite_and_malformed_request(self):
        request = self.request()
        bad = copy.deepcopy(request); bad["extra"] = 1; self.reject(bad)
        bad = copy.deepcopy(request); bad["version"] = True; self.reject(bad)
        for raw in [b'{"version":1,"version":1}', b'{"v":NaN}', b'not-json', b'\xff']:
            with self.assertRaises(b.BrokerError):self.f.broker.exchange(raw, object())

    def test_forged_transaction_and_operation_identity(self):
        request = self.request()
        for key, value in [("transaction", "forged"), ("operation_id", "../escape"), ("source_sha256", "0" * 64)]:
            bad = copy.deepcopy(request); bad[key] = value; self.reject(bad)

    def test_transaction_string_does_not_grant_authority(self):
        request = self.request()
        self.reject(request)
        with self.assertRaises(b.BrokerError):self.f.authority.verify_reply({}, request)

    def test_grant_bound_to_exact_request_and_consumed_once(self):
        request = self.request(); token = self.f.authority.issue(request)
        modified = copy.deepcopy(request); modified["operation_id"] = "a" * 32
        self.reject(modified, token)
        self.reject(request, token)

    def test_stale_context_and_boolean_expected_binding(self):
        request = self.request(); token = self.f.authority.issue(request)
        self.f.consumers.session = "different-session"
        self.reject(request, token)
        request = self.request(); request["expected"]["kind"] = True
        with self.assertRaises(b.BrokerError):self.f.authority.issue(request)

    def test_source_identity_corruption(self):
        path = self.f.d.ORDER[0]; self.f.source[path] += b"corrupt"
        with self.assertRaises(self.f.d.Failure):self.f.d.preflight(self.f.fs, self.f.source, self.f.consumers)

    def test_symlink_and_reparse_substitution_rejected(self):
        path = next(iter(self.f.base)); target = self.f.root / path
        original = Path.lstat
        with patch.object(Path, "lstat", lambda p, *a, **k: types.SimpleNamespace(st_mode=stat.S_IFLNK|0o777, st_file_attributes=0) if p == target else original(p,*a,**k)):
            with self.assertRaises(b.BrokerError):self.f.fs.snapshot(path, self.f.d.MODES[path])

    def test_unexpected_type_and_hardlink_rejected(self):
        path = next(iter(self.f.base)); target = self.f.root / path; raw = target.read_bytes()
        target.unlink(); target.mkdir()
        with self.assertRaises(b.BrokerError):self.f.fs.snapshot(path, self.f.d.MODES[path])
        target.rmdir(); target.write_bytes(raw)
        other = self.f.root / "fixture-hardlink"
        os.link(target, other)
        with self.assertRaises(b.BrokerError):self.f.fs.snapshot(path, self.f.d.MODES[path])
        other.unlink()

    def test_owner_and_mode_expectations_rejected(self):
        path = next(iter(self.f.base))
        for values in ([0, 0, self.f.d.MODES[path]], [1000, 1000, 0o777]):
            self.f.disk.metadata[path] = values
            with self.assertRaises(b.BrokerError):self.f.fs.snapshot(path, self.f.d.MODES[path])
        self.f.disk.metadata[path] = [1000, 1000, self.f.d.MODES[path]]

    def test_no_caller_root_override_or_generic_writer(self):
        with self.assertRaises(TypeError):b.Fixture(root=ROOT)
        with self.assertRaises(b.BrokerError):b.FixtureDisk(ROOT, self.f.d)
        with self.assertRaises(b.BrokerError):self.f.fs.write_new(self.f.d.ORDER[0], b"arbitrary")
        with self.assertRaises(b.BrokerError):self.f.fs.read("config/private")

    def test_publication_cannot_skip_controller_pending_order(self):
        self.stop_pending()
        path = self.f.d.ORDER[1]
        with self.assertRaises(b.BrokerError):self.f.fs.request("PUBLISH", path, expected=self.f.controller._journal()["baseline"][path])
        self.assertFalse(self.f.disk.path(path).exists())

    def test_no_publication_or_rollback_from_prepared_state(self):
        self.f.prepare(); path = self.f.d.ORDER[0]
        for op in ("PUBLISH", "RESTORE", "REMOVE"):
            with self.assertRaises(b.BrokerError):self.f.fs.request(op, path)

    def test_omitted_backup_blocks_publication(self):
        info = self.f.prepare(); path = next(iter(self.f.base)); index = self.f.d.ORDER.index(path)
        self.f.disk.path(self.f.d.TX + "/backup-" + str(index)).unlink()
        with self.assertRaises(b.BrokerError):self.f.controller.commit("COMMIT_SYNTHETIC_BROKER", info["journal_sha256"])
        self.assertEqual(self.f.controller._journal()["state"], "PREPARED")

    def test_corrupt_backup_blocks_publication(self):
        info = self.f.prepare(); path = next(iter(self.f.base)); index = self.f.d.ORDER.index(path)
        self.f.disk.path(self.f.d.TX + "/backup-" + str(index)).write_bytes(b"corrupt")
        with self.assertRaises(b.BrokerError):self.f.controller.commit("COMMIT_SYNTHETIC_BROKER", info["journal_sha256"])

    def test_stage_corruption_and_target_drift_block_commit(self):
        info = self.f.prepare(); path = self.f.d.ORDER[0]
        self.f.disk.path(self.f.d.TX + "/stage-0").write_bytes(b"corrupt")
        with self.assertRaises(b.BrokerError):self.f.controller.commit("COMMIT_SYNTHETIC_BROKER", info["journal_sha256"])
        self.f.disk.path(self.f.d.TX + "/stage-0").write_bytes(self.f.source[path])
        baseline = next(iter(self.f.base)); self.f.disk.path(baseline).write_bytes(b"drift")
        with self.assertRaises((b.BrokerError, self.f.d.Failure)):self.f.controller.commit("COMMIT_SYNTHETIC_BROKER", info["journal_sha256"])

    def test_stale_target_snapshot_rejected_with_valid_old_grant(self):
        request = self.request(); request["operation"] = "READ"; token = self.f.authority.issue(request)
        path = request["artifact"]
        if path in self.f.base:self.f.disk.path(path).write_bytes(b"drift")
        else:self.f.disk.write_new(path, b"unexpected", self.f.d.MODES[path])
        self.reject(request, token)

    def test_duplicate_mutation_after_failure_rejected_across_fresh_broker(self):
        info = self.f.prepare();self.injected("before_execution", "PUBLISH")
        with self.assertRaisesRegex(b.BrokerError, "OUTCOME_UNCONFIRMED"):
            self.f.controller.commit("COMMIT_SYNTHETIC_BROKER", info["journal_sha256"])
        request = copy.deepcopy(self.f.fs.last_request)
        self.f.reopen()
        token = self.f.authority.issue(request)
        self.reject(request, token)
        request["operation_id"] = "b" * 32
        token = self.f.authority.issue(request)
        self.reject(request, token)

    def test_lost_reply_after_publication_never_implies_success(self):
        info = self.f.prepare(); self.injected("after_success_before_reply", "PUBLISH")
        with self.assertRaisesRegex(b.BrokerError, "OUTCOME_UNCONFIRMED"):
            self.f.controller.commit("COMMIT_SYNTHETIC_BROKER", info["journal_sha256"])
        path = self.f.d.ORDER[0]
        self.assertEqual(self.f.disk.read(path, self.f.d.MODES[path]), self.f.source[path])
        self.f.reopen(); value = self.f.controller._journal()
        self.assertEqual(value["state"], "COMMITTING");self.assertEqual(value["pending"], path);self.assertFalse(value["installed"])
        self.assertFalse(self.f.controller.inspect()["live_state_established"])
        with self.assertRaises(self.f.d.Failure):self.f.controller.rollback("ROLLBACK_UNCERTAIN", self.f.controller.inspect()["journal_sha256"])
        self.assertTrue(self.f.consumers.active)

    def test_independent_fresh_inspection_after_recorded_partial_publication(self):
        info = self.f.prepare()
        def stop(point):
            if point == "INSTALLED:" + self.f.d.ORDER[2]:raise KeyboardInterrupt()
        self.f.controller.fault = stop
        with self.assertRaises(KeyboardInterrupt):self.f.controller.commit("COMMIT_SYNTHETIC_BROKER", info["journal_sha256"])
        self.f.reopen(); value = self.f.controller._journal()
        self.assertEqual(len(value["installed"]), 3);self.assertIsNone(value["pending"])
        result = self.f.controller.rollback("ROLLBACK_PARTIAL", self.f.controller.inspect()["journal_sha256"])
        self.assertEqual(result["state"], "ROLLED_BACK")

    def test_interrupted_rollback_without_reply_remains_uncertain(self):
        info = self.f.commit(); self.injected("after_success_before_reply", "RESTORE")
        with self.assertRaises(b.BrokerError):self.f.controller.rollback("ROLLBACK_SYNTHETIC_BROKER", info["journal_sha256"])
        self.f.reopen();value = self.f.controller._journal()
        self.assertEqual(value["state"], "ROLLING_BACK");self.assertIsNotNone(value["pending"])
        with self.assertRaises(self.f.d.Failure):self.f.controller.rollback("ROLLBACK_AGAIN", self.f.controller.inspect()["journal_sha256"])
        self.assertTrue(self.f.consumers.active)

    def test_recovery_read_failure_never_changes_journal_or_releases(self):
        self.f.commit(); self.f.reopen()
        before = self.f.disk.read(self.f.d.TX + "/journal.json")
        self.injected("during_recovery_inspection", "SNAPSHOT")
        with self.assertRaises(b.BrokerError):self.f.controller.inspect()
        self.assertEqual(self.f.disk.read(self.f.d.TX + "/journal.json"), before)
        self.assertTrue(self.f.consumers.active)

    def test_request_evidence_never_authorizes_or_rewrites_journal(self):
        self.f.commit(); journal = self.f.disk.read(self.f.d.TX + "/journal.json")
        for p in self.f.disk.trace_dir.iterdir():p.write_bytes(b.canonical({"phase":"COMMITTED","release":True}))
        self.f.reopen()
        self.assertEqual(self.f.controller._journal()["state"], "COMMITTED")
        self.assertEqual(self.f.disk.read(self.f.d.TX + "/journal.json"), journal)
        request = self.request();request["operation"] = "RELEASE_CONSUMERS";self.reject(request)

    def test_forged_modified_and_cross_request_reply_rejected(self):
        request = self.request()
        reply = {"version":1,"transaction":b.TRANSACTION,"operation_id":request["operation_id"],"request_sha256":b.digest(b.canonical(request)),"result":request["expected"],"synthetic_only":True}
        with self.assertRaises(b.BrokerError):self.f.authority.verify_reply(reply, request)
        token = self.f.authority.issue(request);reply = self.f.broker.exchange(b.canonical(request), token)
        reply["result"] = {}
        with self.assertRaises(b.BrokerError):self.f.authority.verify_reply(reply, request)

    def test_external_boundary_is_rechecked_not_inferred_from_journal(self):
        self.f.prepare(); self.f.consumers.active = False
        with self.assertRaises(b.BrokerError):self.f.controller.commit("COMMIT_SYNTHETIC_BROKER", self.f.controller.inspect()["journal_sha256"])
        self.assertEqual(self.f.controller._journal()["state"], "PREPARED")

    def test_adapter_has_no_local_protected_access_before_broker_execution(self):
        active = [False]
        original = self.f.disk.snapshot
        transport = self.f.fs.transport
        def guarded(path, mode=None):
            if path in self.f.d.ORDER:
                self.assertTrue(active[0], "client attempted protected snapshot")
            return original(path, mode)
        def exchange(raw, token):
            active[0] = True
            try:return transport(raw, token)
            finally:active[0] = False
        self.f.disk.snapshot = guarded
        self.f.fs.transport = exchange
        self.f.commit()

    def test_closed_result_rejects_even_sealed_invalid_snapshot(self):
        request=self.request()
        for change in ("exists_type","extra_field","bad_parents"):
            result=copy.deepcopy(self.f.fs.snapshot(request["artifact"],self.f.d.MODES[request["artifact"]]))
            if change=="exists_type":result["exists"]=1
            elif change=="extra_field":result["unexpected"]=True
            else:result["parents"]={}
            reply=self.f.authority.seal({"version":1,"transaction":b.TRANSACTION,"operation_id":request["operation_id"],"request_sha256":b.digest(b.canonical(request)),"result":result,"synthetic_only":True})
            with self.assertRaises(b.BrokerError):self.f.authority.verify_reply(reply,request)

    def test_restore_of_new_artifact_is_not_a_generic_write(self):
        path=next(p for p in self.f.d.ORDER if p not in self.f.base)
        with self.assertRaises(b.BrokerError):self.f.fs.request("RESTORE",path)
        self.assertFalse(self.f.disk.path(path).exists())

    def test_new_destination_race_is_not_overwritten(self):
        path=next(p for p in self.f.d.ORDER if p not in self.f.base)
        value=self.stop_pending(path)
        original=b.os.rename
        def raced(src,dst):
            self.f.disk.write_new(path,b"independent-race",self.f.d.MODES[path])
            return original(src,dst)
        with patch.object(b.os,"rename",raced):
            with self.assertRaises(b.BrokerError):self.f.fs.request("PUBLISH",path,expected=value["baseline"][path])
        self.assertEqual(self.f.disk.read(path,self.f.d.MODES[path]),b"independent-race")
        self.assertEqual(self.f.controller._journal()["pending"],path)

    def test_during_rollback_failure_preserves_controller_pending(self):
        info=self.f.commit();self.injected("during_rollback","RESTORE")
        with self.assertRaises(b.BrokerError):self.f.controller.rollback("ROLLBACK_DURING",info["journal_sha256"])
        self.f.reopen();value=self.f.controller._journal()
        self.assertEqual(value["state"],"ROLLING_BACK");self.assertIsNotNone(value["pending"])
        self.assertFalse(self.f.controller.inspect()["live_state_established"])
        self.assertTrue(self.f.consumers.active)

    def test_no_native_backend_privilege_network_or_engine_calls(self):
        source = (ROOT / "tools/pe73_filesystem_broker_prototype.py").read_text()
        tree = ast.parse(source)
        imports = {n.names[0].name for n in ast.walk(tree) if isinstance(n,ast.Import)}
        self.assertFalse(imports & {"subprocess","ctypes","socket"})
        for call in [n for n in ast.walk(tree) if isinstance(n,ast.Call)]:
            if isinstance(call.func, ast.Attribute) and isinstance(call.func.value,ast.Name):
                self.assertNotIn((call.func.value.id,call.func.attr),{("os","chmod"),("os","chown"),("os","system"),("os","setuid")})
        with patch.object(self.f.d,"NativeFS",side_effect=AssertionError("native called")),patch.object(self.f.d,"source_gate",side_effect=AssertionError("source gate called")):
            self.f.commit()
        with patch.object(b.os,"name","posix"):
            with self.assertRaisesRegex(b.BrokerError,"WINDOWS_FIXTURE_ONLY"):b.Fixture()

# One real full transaction supplies independently captured before/installed/restored
# observations for all13 paths; per-path assertions do not rerun the same transaction.
class ArtifactObservationsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        f=b.Fixture()
        try:
            cls.order=list(f.d.ORDER);cls.base=copy.deepcopy(f.base);cls.source=copy.deepcopy(f.source);cls.modes=copy.deepcopy(f.d.MODES)
            cls.before={p:f.fs.snapshot(p, f.d.MODES[p] if p in f.base else None) for p in f.d.ORDER}
            info=f.commit();cls.committed=copy.deepcopy(info)
            cls.installed={p:f.fs.snapshot(p,f.d.MODES[p]) for p in f.d.ORDER}
            result=f.controller.rollback("ROLLBACK_SYNTHETIC_BROKER",info["journal_sha256"])
            cls.rolled_back=copy.deepcopy(result);cls.inspected=f.controller.inspect()
            cls.restored={p:f.fs.snapshot(p,f.d.MODES[p] if p in f.base else None) for p in f.d.ORDER}
            cls.requests=copy.deepcopy(f.fs.requests)
        finally:f.close()

    def test_actual_controller_full_flow_and_operation_coverage(self):
        self.assertEqual(self.committed["state"],"COMMITTED")
        self.assertTrue(self.committed["live_state_established"])
        self.assertEqual(self.rolled_back["state"],"ROLLED_BACK")
        self.assertTrue(self.inspected["live_state_established"])
        self.assertEqual({r["operation"] for r in self.requests},b.OPERATIONS)
        self.assertEqual([r["artifact"] for r in self.requests if r["operation"]=="PUBLISH"],self.order)
        self.assertEqual([r["artifact"] for r in self.requests if r["operation"] in {"RESTORE","REMOVE"}],list(reversed(self.order)))
        self.assertEqual(len(self.base),5);self.assertEqual(len(self.source),13)

def artifact_case(path):
    def test(self):
        self.assertEqual(self.before[path]["exists"],path in self.base)
        snap=self.installed[path]
        self.assertEqual(snap["sha256"],b.digest(self.source[path]))
        self.assertEqual((snap["identity"]["st_uid"],snap["identity"]["st_gid"],snap["identity"]["mode"]),(1000,1000,self.modes[path]))
        snap=self.restored[path];self.assertEqual(snap["exists"],path in self.base)
        if path in self.base:self.assertEqual(snap["sha256"],b.digest(self.base[path]))
    return test

def fault_case(point, operation):
    def test(self):
        if operation in {"BACKUP","STAGE"}:
            self.injected(point,operation)
            with self.assertRaises(b.BrokerError):self.f.prepare()
            self.assertEqual(self.f.controller._journal()["state"],"PREPARING")
        else:
            info=self.f.prepare();self.injected(point,operation)
            with self.assertRaises(b.BrokerError):self.f.controller.commit("COMMIT_SYNTHETIC_BROKER",info["journal_sha256"])
            self.assertEqual(self.f.controller._journal()["state"],"COMMITTING")
        self.assertTrue(self.f.consumers.active)
    return test

_d,_s,_base=b.load_fixture_controller()
for i,path in enumerate(_d.ORDER):setattr(ArtifactObservationsTests,"test_artifact_%02d_%s"%(i,"replacement" if path in _base else "new"),artifact_case(path))
for i,(point,op) in enumerate([("before_execution","PUBLISH"),("after_validation_before_mutation","PUBLISH"),("during_staging","STAGE"),("during_publication","PUBLISH"),("after_mutation_before_verification","PUBLISH"),("after_success_before_reply","PUBLISH"),("during_backup","BACKUP")]):
    setattr(BrokerTests,"test_fault_%02d_%s"%(i,point),fault_case(point,op))

if __name__ == "__main__":
    unittest.main()
