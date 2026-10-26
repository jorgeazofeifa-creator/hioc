"""Focused maintenance-window tests, real Windows temporary fixture bytes only."""
import copy
import contextlib
import os
import shutil
import subprocess
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import test_pe73_pi3_delivery as prior

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("pe73_window_tests", ROOT/"tools/pe73_maintenance_window.py")
w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
d = w.d

class Ops:
    def __init__(self, raw):
        self.raw, self.boot_id, self.clock = raw, "BOOT_ID_1", 1000
        self.active, self.complete, self.calls = [], True, []
        self.fail_install = False
    def now(self): return self.clock
    def live_gate(self): pass  # Explicit synthetic native-acceptance stand-in.
    def scheduler(self): return self.raw
    def install_scheduler(self, raw, expected):
        d.require(d.sha(self.raw)==expected,"SCHEDULER_CONFLICT")
        self.calls.append(raw)
        if self.fail_install: raise OSError("synthetic uncertain effect")
        self.raw=raw
    def processes(self):
        return {"boot_id": self.boot_id,"observed_at":self.clock,"known_active":copy.deepcopy(self.active),
            "inspection_complete":self.complete,"limitations":["CACHED_MODULES_UNKNOWN"],"universal_exclusion":False}

class WindowTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix="hioc-pe73-window-test-")
        self.fs=prior.FixtureFS(Path(self.temp.name))
        self.raw=("# preserved comment\n"+"\n".join(d.CRON)+"\n7 * * * * unrelated-job\n").encode()
        self.ops=Ops(self.raw);self.count=0
        self.inventory={x:"EXCLUDE" for x in d.CRON};self.inventory["7 * * * * unrelated-job"]="PRESERVE"
        self.provider=w.WindowConsumers(self.ops,self.raw,list(d.CRON),self.inventory)
        self.c=self.provider.bind(self.fs,prior.SOURCE)
        before=d.preflight(self.fs,prior.SOURCE,self.provider)
        self.c.prepare("PREPARE_WINDOW",d.sha(d.canonical(before)))
    def tearDown(self): self.temp.cleanup()
    def grant(self, action):
        self.count+=1
        return {"action":action,"reference":"WINDOW_AUTH_"+str(self.count),
            "journal_sha256":d.sha(d.canonical(self.c._journal())),"scheduler_sha256":d.sha(self.ops.raw),
            "operator":"OPERATOR_JORGE","session":self.provider.session,"boot_id":self.ops.boot_id,
            "expires_at":self.ops.clock+600,"exclusive_responsibility":True,"risks_acknowledged":list(w.RISKS)}
    def step(self, action): return self.provider.progress(action,self.grant(action))
    def establish(self):
        for action in ("PRESERVE","EXCLUDE","DRAIN","ESTABLISH"): self.step(action)
    def runtime(self,action):
        g=self.grant(action);self.provider.authorize_runtime(g)
        return getattr(self.c,action.lower())(g["reference"],g["journal_sha256"])
    def test_original_inventory_rejects_unclassified_entry(self):
        bad=dict(self.inventory);del bad["7 * * * * unrelated-job"]
        with self.assertRaises(d.Failure):w.WindowConsumers(self.ops,self.raw,list(d.CRON),bad)
    def test_missing_approved_job_rejected(self):
        with self.assertRaises(d.Failure):w.WindowConsumers(self.ops,self.raw,list(d.CRON)[:-1],self.inventory)
    def test_exact_preservation_and_exclusion(self):
        self.step("PRESERVE");self.assertEqual(self.fs.read(w.BACKUP),self.raw)
        self.step("EXCLUDE");self.assertEqual(self.ops.raw,b"# preserved comment\n7 * * * * unrelated-job\n")
        for line in d.CRON:self.assertNotIn(line.encode(),self.ops.raw)
    def test_scheduler_conflict_preserves_unexpected_bytes(self):
        self.step("PRESERVE");self.ops.raw+=b"9 * * * * surprise\n";raw=self.ops.raw
        with self.assertRaises(d.Failure):self.step("EXCLUDE")
        self.assertEqual(self.ops.raw,raw);self.assertFalse(self.ops.calls)
    def test_uncertain_exclusion_not_retried(self):
        self.step("PRESERVE");self.ops.fail_install=True
        with self.assertRaises(OSError):self.step("EXCLUDE")
        self.assertEqual(self.c._journal()["window"]["phase"],"EXCLUSION_UNCERTAIN")
        with self.assertRaises(d.Failure):self.step("EXCLUDE")
        self.assertEqual(len(self.ops.calls),1)
    def test_known_active_consumer_blocks_drain(self):
        self.step("PRESERVE");self.step("EXCLUDE")
        self.ops.active=[{"pid":123,"start_ticks":44,"command_sha256":"a"*64}]
        with self.assertRaises(d.Failure):self.step("DRAIN")
    def test_incomplete_inspection_blocks_drain(self):
        self.step("PRESERVE");self.step("EXCLUDE");self.ops.complete=False
        with self.assertRaises(d.Failure):self.step("DRAIN")
    def test_invalid_authorization_fields_and_risk_acknowledgement(self):
        for key,value in [("exclusive_responsibility",False),("risks_acknowledged",[]),("expires_at",self.ops.clock),
                          ("boot_id","OTHER"),("session","OLD"),("journal_sha256","0"*64),("scheduler_sha256","0"*64)]:
            with self.subTest(key=key):
                g=self.grant("PRESERVE");g[key]=value
                with self.assertRaises(d.Failure):self.provider.progress("PRESERVE",g)
    def test_unknown_action_rejected(self):
        with self.assertRaises(d.Failure):self.provider.progress("CHMOD",self.grant("PRESERVE"))
    def test_duplicate_operation_rejected(self):
        g=self.grant("PRESERVE");self.provider.progress("PRESERVE",g)
        with self.assertRaises(d.Failure):self.provider.progress("PRESERVE",g)
    def test_manual_control_truthful(self):
        self.establish();receipt=self.provider.inspect()
        self.assertFalse(receipt["universal_exclusion"]);self.assertEqual(receipt["manual_launch_control"],"PROCEDURAL_ONLY")
        self.assertIn("CACHED_MODULES_UNKNOWN",receipt["process_observation"]["limitations"])
    def test_commit_requires_separate_bound_grant(self):
        self.establish()
        with self.assertRaises(d.Failure):self.c.commit("UNAPPROVED",d.sha(d.canonical(self.c._journal())))
        self.assertFalse(self.fs.publications)
    def test_known_process_arriving_after_drain_blocks_commit(self):
        self.establish();self.ops.active=[{"pid":123,"start_ticks":44,"command_sha256":"a"*64}]
        with self.assertRaises(d.Failure):self.runtime("COMMIT")
        self.assertFalse(self.fs.publications)
    def test_commit_and_exact_release(self):
        self.establish();self.assertEqual(self.runtime("COMMIT")["state"],"COMMITTED")
        self.assertEqual(self.ops.raw,self.provider.reduced)
        for action in ("AUTHORIZE_RELEASE","RESTORE_SCHEDULER","RELEASE"):self.step(action)
        self.assertEqual(self.ops.raw,self.raw);self.assertEqual(self.provider.inspect()["phase"],"RELEASED")
        self.fs.assert_unrelated(self)
    def test_fresh_recovery_requires_attach_and_drain(self):
        self.establish();self.runtime("COMMIT");self.provider=w.WindowConsumers(self.ops,self.raw,list(d.CRON),self.inventory)
        self.c=self.provider.bind(self.fs,prior.SOURCE)
        with self.assertRaises(d.Failure):self.provider.assert_active()
        self.step("ATTACH")
        with self.assertRaises(d.Failure):self.step("AUTHORIZE_RELEASE")
        self.step("DRAIN");self.step("AUTHORIZE_RELEASE")
    def test_reboot_invalidates_old_session(self):
        self.establish();self.ops.boot_id="BOOT_ID_2"
        with self.assertRaises(d.Failure):self.runtime("COMMIT")
        self.assertFalse(self.fs.publications)
    def test_deadline_never_releases_scheduler(self):
        self.establish();self.ops.clock+=601
        with self.assertRaises(d.Failure):self.provider.assert_active()
        self.assertEqual(self.ops.raw,self.provider.reduced)
    def test_target_drift_blocks_publication(self):
        self.establish();p=next(iter(prior.BASE));self.fs.path(p).write_bytes(b"drift")
        with self.assertRaises(d.Failure):self.runtime("COMMIT")
        self.assertFalse(self.fs.publications)
    def test_partial_publication_and_lost_effect_no_release(self):
        self.establish();self.fs.fail=lambda point:point=="PUBLISH:"+d.ORDER[2]
        with self.assertRaises(OSError):self.runtime("COMMIT")
        v=self.c._journal();self.assertEqual(v["state"],"COMMITTING");self.assertEqual(v["pending"],d.ORDER[2])
        with self.assertRaises(d.Failure):self.step("AUTHORIZE_RELEASE")
        self.assertEqual(self.ops.raw,self.provider.reduced)
    def test_separately_authorized_rollback_and_restore(self):
        self.establish();self.runtime("COMMIT")
        self.assertEqual(self.runtime("ROLLBACK")["state"],"ROLLED_BACK")
        for action in ("AUTHORIZE_RELEASE","RESTORE_SCHEDULER","RELEASE"):self.step(action)
        for p,raw in prior.BASE.items():self.assertEqual(self.fs.read(p,d.MODES[p]),raw)
    def test_interrupted_rollback_blocks_release(self):
        self.establish();self.runtime("COMMIT")
        self.fs.fail=lambda point:point=="PUBLISH:"+next(reversed(prior.BASE))
        with self.assertRaises(OSError):self.runtime("ROLLBACK")
        self.assertEqual(self.c._journal()["state"],"ROLLING_BACK")
        with self.assertRaises(d.Failure):self.step("AUTHORIZE_RELEASE")
    def test_unauthorized_restore_and_release(self):
        self.establish()
        for action in ("RESTORE_SCHEDULER","RELEASE"):
            with self.assertRaises(d.Failure):self.step(action)
        self.assertEqual(self.ops.raw,self.provider.reduced)
    def test_corrupt_backup_rejected(self):
        self.step("PRESERVE");self.fs.path(w.BACKUP).write_bytes(b"corrupt")
        with self.assertRaises(d.Failure):self.c._journal()
    def test_unknown_core_field_still_rejected(self):
        self.establish();v=self.c._journal();v["invented"]=True;self.fs.journal(v)
        with self.assertRaises(d.Failure):self.c._journal()
    def test_core_installed_provenance_still_rejected(self):
        self.establish();self.runtime("COMMIT");v=self.c._journal();v["installed"][d.ORDER[0]]["sha256"]="0"*64;self.fs.journal(v)
        with self.assertRaises(d.Failure):self.c._journal()
    def test_phase_label_cannot_replace_authorization_history(self):
        self.establish();self.runtime("COMMIT");v=self.c._journal()
        v["window"]["phase"]="RELEASE_AUTHORIZED"
        v["window"]["release_runtime_sha256"]="a"*64
        self.fs.journal(v)
        with self.assertRaises(d.Failure):self.c._journal()
    def test_release_rechecks_source_identity(self):
        self.establish();self.runtime("COMMIT")
        self.c.source=dict(self.c.source);self.c.source[d.ORDER[0]]=b"corrupt"
        with self.assertRaises(d.Failure):self.step("AUTHORIZE_RELEASE")
        self.assertEqual(self.ops.raw,self.provider.reduced)
    def test_uncertain_scheduler_restore_never_retries_or_releases(self):
        self.establish();self.runtime("COMMIT");self.step("AUTHORIZE_RELEASE")
        self.ops.fail_install=True
        with self.assertRaises(OSError):self.step("RESTORE_SCHEDULER")
        self.assertEqual(self.c._journal()["window"]["phase"],"RESTORE_UNCERTAIN")
        count=len(self.ops.calls)
        for a in ("RESTORE_SCHEDULER","RELEASE","ATTACH"):
            with self.assertRaises(d.Failure):self.step(a)
        self.assertEqual(len(self.ops.calls),count)
    def test_operator_change_requires_new_explicit_disposition(self):
        self.establish();g=self.grant("DRAIN");g["operator"]="OTHER_OPERATOR"
        with self.assertRaises(d.Failure):self.provider.progress("DRAIN",g)
    def test_runtime_grant_is_bound_and_consumed(self):
        self.establish();g=self.grant("COMMIT");self.provider.authorize_runtime(g)
        with self.assertRaises(d.Failure):self.c.commit("OTHER_REFERENCE",g["journal_sha256"])
        with self.assertRaises(d.Failure):self.c.commit(g["reference"],g["journal_sha256"])
        self.assertFalse(self.fs.publications)
    def test_native_prepare_gate_precedes_any_preparation_effect(self):
        before=self.fs.read(d.TX+"/journal.json")
        with patch.object(self.ops,"live_gate",side_effect=d.Failure("NATIVE_WINDOW_ACCEPTANCE_REQUIRED")):
            with self.assertRaisesRegex(d.Failure,"NATIVE_WINDOW_ACCEPTANCE_REQUIRED"):
                self.c.prepare("PREPARE_AGAIN", "0"*64)
        self.assertEqual(self.fs.read(d.TX+"/journal.json"),before)
    def test_native_process_parser_reports_known_identity_without_private_arguments(self):
        proc=Path(self.temp.name)/"synthetic-proc";entry=proc/"1234567";entry.mkdir(parents=True)
        (entry/"cmdline").write_bytes(b"python3\0/home/jazofv1/hioc/pi4/bin/hioc-assets.py\0private_argument\0")
        fields=["S"]+["0"]*18+["2345"]
        (entry/"stat").write_text("1234567 (python with spaces) "+" ".join(fields))
        original=Path;native=w.NativeOps.__new__(w.NativeOps);native.boot_id="BOOT_ID_1";native.now=lambda:1000
        with patch.object(w,"Path",side_effect=lambda x:proc if x=="/proc" else original(x)):
            receipt=native.processes()
        self.assertEqual(receipt["known_active"][0]["start_ticks"],2345)
        self.assertTrue(receipt["inspection_complete"]);self.assertFalse(receipt["universal_exclusion"])
        self.assertNotIn("private_argument",json.dumps(receipt))
    def test_gated_native_scheduler_uses_single_fixed_argv_and_verifies(self):
        native=w.NativeOps.__new__(w.NativeOps);current=[self.raw]
        native.scheduler=lambda:current[0]
        def install(argv,**kwargs):
            self.assertEqual(argv,["/usr/bin/crontab","-"]);self.assertNotIn("shell",kwargs)
            current[0]=kwargs["input"]
            return type("Result",(),{"returncode":0})()
        with patch.object(native,"scheduler_gate"),patch.object(native,"live_gate"),patch.object(w.subprocess,"run",side_effect=install) as call:
            native.install_scheduler(b"# synthetic replacement\n",d.sha(self.raw))
        self.assertEqual(call.call_count,1)
    def test_native_mutation_gates_unconditionally_refuse(self):
        native=w.NativeOps.__new__(w.NativeOps)
        with self.assertRaisesRegex(d.Failure,"NATIVE_WINDOW_ACCEPTANCE_REQUIRED"):native.live_gate()
        with self.assertRaisesRegex(d.Failure,"NATIVE_SCHEDULER_NOT_QUALIFIED"):native.install_scheduler(b"x","0"*64)
    def test_native_gate_blocks_before_any_fixture_effect(self):
        with patch.object(self.ops,"live_gate",side_effect=d.Failure("NATIVE_WINDOW_ACCEPTANCE_REQUIRED")):
            with self.assertRaises(d.Failure):self.step("PRESERVE")
        self.assertNotIn("window",self.c._journal());self.assertFalse(self.ops.calls)


class RelativeInvocationTests(unittest.TestCase):
    def observe(self, argv, cwd="/home/jazofv1/hioc/pi4/bin", cwd_error=None,
                stat_change=False, cwd_change=False, command_change=False):
        with tempfile.TemporaryDirectory(prefix="hioc-pe73-process-test-") as name:
            proc=Path(name)/"proc";entry=proc/"1234567";entry.mkdir(parents=True)
            raw=b"\0".join(x.encode() for x in argv)+b"\0"
            (entry/"cmdline").write_bytes(raw)
            def stat_value(start):return "1234567 (python with spaces) "+" ".join(["S"]+["0"]*18+[str(start)])
            (entry/"stat").write_text(stat_value(2345))
            native=w.NativeOps.__new__(w.NativeOps);native.boot_id="BOOT_ID_1";native.now=lambda:1000
            original_path=Path;original_read=Path.read_text;read_count=[0];cwd_reads=[0]
            def stat_read(path,*args,**kwargs):
                if path==entry/"stat":
                    read_count[0]+=1
                    if stat_change and read_count[0]>1:return stat_value(2346)
                return original_read(path,*args,**kwargs)
            def readlink(path):
                self.assertEqual(Path(path),entry/"cwd")
                cwd_reads[0]+=1
                if cwd_error:raise cwd_error
                if cwd_change and cwd_reads[0]>1:return "/changed/cwd"
                if command_change:(entry/"cmdline").write_bytes(b"python3\0other.py\0")
                return cwd
            with patch.object(w,"Path",side_effect=lambda x:proc if x=="/proc" else original_path(x)), \
                    patch.object(w.os,"readlink",side_effect=readlink),patch.object(Path,"read_text",stat_read):
                evidence=native.processes()
            observer=type("ObservedOps",(),{"boot_id":"BOOT_ID_1","processes":lambda self:evidence,"now":lambda self:1000})()
            provider=w.WindowConsumers.__new__(w.WindowConsumers);provider.ops=observer
            return evidence,provider
    def blocked(self, argv, **kwargs):
        evidence,provider=self.observe(argv,**kwargs)
        with self.assertRaises(w.d.Failure):provider._processes()
        self.assertFalse(evidence["universal_exclusion"])
        return evidence
    def test_original_relative_asset_invocation_blocks_actual_drain(self):
        evidence=self.blocked(["python3","hioc-assets.py","list"])
        self.assertEqual(evidence["known_active"][0]["start_ticks"],2345)

    def test_absolute_invocation_blocks_actual_drain(self):
        self.blocked(["python3","/home/jazofv1/hioc/pi4/bin/hioc-assets.py","list"])
    def test_dot_relative_invocation_blocks_actual_drain(self):
        self.blocked(["python3","./hioc-assets.py","list"])
    def test_relative_classification_cli_blocks_actual_drain(self):
        self.blocked(["python3","hioc-classify-metadata.py"])
    def test_python_options_preceding_script(self):
        for flags in (["-I","-S","-B"],["-ISB"],["-X","dev","-W","ignore"],
                      ["-Xutf8=1","-Wignore"],["--check-hash-based-pycs","always"],["--"]):
            with self.subTest(flags=flags):self.blocked(["/usr/bin/python3.11",*flags,"hioc-assets.py","list"])
    def test_module_invocation_blocks_actual_drain(self):
        self.blocked(["python3","-I","-m","hioc.classification"])
    def test_direct_relative_script_blocks_actual_drain(self):
        self.blocked(["./hioc-assets.py","list"])
    def test_unrelated_python_script_allows_valid_known_process_drain(self):
        evidence,provider=self.observe(["python3","unrelated.py","hioc-assets.py"],cwd_error=AssertionError("cwd must not be requested"))
        self.assertTrue(evidence["inspection_complete"])
        self.assertEqual(provider._processes()["known_active"],[])
        self.assertIn("UNCLASSIFIED_PID_1234567",evidence["limitations"])
    def test_python_option_arguments_are_not_scripts(self):
        evidence,provider=self.observe(["python3","-W","hioc-assets.py","unrelated.py"])
        self.assertTrue(evidence["inspection_complete"]);provider._processes()
    def test_command_text_is_not_shell_parsed_or_executed(self):
        evidence,provider=self.observe(["python3","-c","print('hioc-assets.py')"])
        self.assertTrue(evidence["inspection_complete"]);provider._processes()
    def test_missing_cwd_blocks_drain(self):
        e=self.blocked(["python3","hioc-assets.py"],cwd_error=FileNotFoundError())
        self.assertFalse(e["inspection_complete"])
    def test_unreadable_cwd_blocks_drain(self):
        e=self.blocked(["python3","hioc-assets.py"],cwd_error=PermissionError())
        self.assertFalse(e["inspection_complete"])
    def test_start_identity_change_blocks_drain(self):
        e=self.blocked(["python3","hioc-assets.py"],stat_change=True)
        self.assertFalse(e["inspection_complete"])
    def test_cwd_change_blocks_drain(self):
        e=self.blocked(["python3","hioc-assets.py"],cwd_change=True)
        self.assertFalse(e["inspection_complete"])
    def test_command_change_blocks_drain(self):
        e=self.blocked(["python3","hioc-assets.py"],command_change=True)
        self.assertFalse(e["inspection_complete"])
    def test_process_exit_during_cwd_inspection_blocks_until_fresh_scan(self):
        e=self.blocked(["python3","hioc-assets.py"],cwd_error=ProcessLookupError())
        self.assertFalse(e["inspection_complete"])
    def test_ambiguous_script_resolution_blocks_drain(self):
        for script,cwd in (("../bin/hioc-assets.py",w.RUNTIME_BIN),("hioc-assets.py","/unverified/alias"),
                           ("hioc-assets.py",w.RUNTIME_BIN+" (deleted)"),("hioc-assets.py","relative/cwd")):
            with self.subTest(script=script,cwd=cwd):
                self.assertFalse(self.blocked(["python3",script],cwd=cwd)["inspection_complete"])
    def test_ambiguous_python_options_cannot_hide_known_script(self):
        e=self.blocked(["python3","--unverified-option","hioc-assets.py"])
        self.assertFalse(e["inspection_complete"])
    def test_empty_process_scan_allows_fresh_known_process_drain(self):
        with tempfile.TemporaryDirectory(prefix="hioc-pe73-empty-proc-") as directory:
            original=Path;native=w.NativeOps.__new__(w.NativeOps);native.boot_id="BOOT_ID_1";native.now=lambda:1000
            with patch.object(w,"Path",side_effect=lambda x:original(directory) if x=="/proc" else original(x)):
                evidence=native.processes()
        ops=type("ObservedOps",(),{"boot_id":"BOOT_ID_1","processes":lambda self:evidence,"now":lambda self:1000})()
        provider=w.WindowConsumers.__new__(w.WindowConsumers);provider.ops=ops
        self.assertTrue(provider._processes()["inspection_complete"])
        self.assertFalse(evidence["universal_exclusion"])
    def test_known_inventory_names_are_existing_hioc_entry_points(self):
        for name in w.ENTRY_NAMES:self.assertTrue((ROOT/"pi4/bin"/name).is_file(),name)


class ControllerIdentityBindingTests(unittest.TestCase):
    def test_provider_pin_matches_corrected_controller_bytes(self):
        self.assertEqual(w.PIN,d.sha((ROOT/"tools/hioc-pe73-pi3-delivery.py").read_bytes()))
        self.assertFalse(hasattr(w.d,"QUALIFICATION_CHECKOUT"))
        self.assertEqual(w.d.RELEASE,"51398bab4e2293b578b2cdac2d0740c3738cab2f")

    def test_provider_refuses_mismatched_controller_before_import(self):
        spec=importlib.util.spec_from_file_location("pe73_wrong_controller_pin",ROOT/"tools/pe73_maintenance_window.py")
        module=importlib.util.module_from_spec(spec)
        with patch.object(Path,"read_bytes",return_value=b"tampered controller"):
            with self.assertRaisesRegex(RuntimeError,"ACCEPTED_CONTROLLER_CHANGED"):
                spec.loader.exec_module(module)



class PublicationStableIntegrationTests(unittest.TestCase):
    """Real isolated Git objects and actual provider/controller coupling; no PI3."""
    PAYLOAD = "51398bab4e2293b578b2cdac2d0740c3738cab2f"
    PUBLISHED = "302a4e3f34f53fffb8299771d31c115e052b5400"
    ORIGIN = "https://github.com/jorgeazofeifa-creator/hioc.git"
    TOOL_PATHS = ("tools/hioc-pe73-pi3-delivery.py", "tools/pe73_maintenance_window.py")
    real_run = staticmethod(subprocess.run)

    @classmethod
    def setUpClass(cls):
        cls.git_executable = shutil.which("git")
        if cls.git_executable is None:
            raise RuntimeError("Git required for repository-integrity integration tests")
        cls.cache_temp = tempfile.TemporaryDirectory(prefix="hioc-pe73-object-cache-")
        cls.addClassCleanup(cls.cache_temp.cleanup)
        cls.cache = Path(cls.cache_temp.name)/"cache.git"
        cls.run_git(ROOT, "clone", "--bare", "--local", "--no-hardlinks", "--quiet", str(ROOT), str(cls.cache))

    @classmethod
    def environment(cls):
        # Windows transport only: do not inherit Git directory/object overrides or
        # user/system hooks, signing, credential helpers or global configuration.
        env = {k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
        env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
                   GIT_TERMINAL_PROMPT="0")
        return env

    @classmethod
    def run_git(cls, root, *args, data=None):
        result = cls.real_run([cls.git_executable, "--no-optional-locks", "--no-replace-objects", *args],
            cwd=root, input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            timeout=40, env=cls.environment())
        if result.returncode:
            raise AssertionError("Isolated fixture Git operation failed: "+repr(args))
        return result.stdout

    @classmethod
    def configure(cls, root):
        cls.run_git(root,"config","core.autocrlf","false")
        cls.run_git(root,"config","user.name","HIOC Synthetic Fixture")
        cls.run_git(root,"config","user.email","fixture@example.invalid")
        cls.run_git(root,"config","commit.gpgsign","false")
        hooks=root/".git"/"fixture-empty-hooks";hooks.mkdir()
        cls.run_git(root,"config","core.hooksPath",str(hooks))

    @contextlib.contextmanager
    def repository(self, revision=PUBLISHED, empty=False):
        with tempfile.TemporaryDirectory(prefix="hioc-pe73-repository-") as directory:
            root=Path(directory)/"source"
            if empty:
                root.mkdir();self.run_git(root,"init","--quiet")
                self.configure(root)
                self.run_git(root,"remote","add","origin",self.ORIGIN)
                self.run_git(root,"commit","--allow-empty","--quiet","-m","Isolated unrelated fixture")
            else:
                self.run_git(Path(directory),"clone","--local","--no-hardlinks","--no-checkout","--quiet",str(self.cache),str(root))
                self.configure(root)
                self.run_git(root,"remote","set-url","origin",self.ORIGIN)
                self.run_git(root,"checkout","--quiet","--detach",revision)
            canonical=Path(self.run_git(root,"rev-parse","--show-toplevel").decode().strip())
            self.assertTrue(canonical.samefile(root))  # Resolve Windows short-path aliases in this fixture only.
            root=canonical
            self.assertNotEqual(root.resolve(),ROOT.resolve())
            yield root

    def provider(self, root=ROOT):
        spec=importlib.util.spec_from_file_location("pe73_isolated_provider",root/"tools/pe73_maintenance_window.py")
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        return module

    def gate(self, root, module=None, cwd=None):
        module=module or self.provider()
        calls=[]
        def transport(argv,**kwargs):
            # Only adapt the Linux fixed executable/environment to Windows. Git
            # computes every HEAD, root, status, ancestry and object result itself.
            self.assertEqual(argv[0],"/usr/bin/git")
            self.assertEqual(argv[1:3],["--no-optional-locks","--no-replace-objects"])
            calls.append(argv[3:]);kwargs["env"]=self.environment()
            return self.real_run([self.git_executable,*argv[1:]],**kwargs)
        with patch.object(module.d.subprocess,"run",side_effect=transport):
            source=module.d.source_gate((cwd or root).as_posix())
        self.assertEqual(source,prior.SOURCE)
        reads=[a[1] for a in calls if a[0]=="show"]
        self.assertEqual(sorted(reads),sorted(self.PAYLOAD+":"+p for p in prior.SOURCE))
        self.assertEqual(module.PIN,module.d.sha((Path(module.__file__).parent/"hioc-pe73-pi3-delivery.py").read_bytes()))
        return module,source

    def publish_fixture_tools(self, root):
        before={p:(ROOT/p).read_bytes() for p in self.TOOL_PATHS}
        for p,raw in before.items():(root/p).write_bytes(raw)
        self.run_git(root,"add","--",*self.TOOL_PATHS)
        self.run_git(root,"commit","--quiet","-m","Synthetic qualification tooling publication")
        return before

    def test_original_payload_checkout_uses_original_objects_with_corrected_provider(self):
        with self.repository(self.PAYLOAD) as root:self.gate(root)

    def test_current_published_qualification_checkout_uses_original_objects(self):
        with self.repository() as root:self.gate(root)

    def test_successive_real_publications_need_no_source_or_allowlist_edit(self):
        with self.repository() as root:
            before=self.publish_fixture_tools(root)
            module=self.provider(root)
            self.assertFalse(hasattr(module.d,"QUALIFICATION_CHECKOUT"))
            for step in range(2):
                head=self.run_git(root,"rev-parse","HEAD").decode().strip()
                self.assertNotIn(head,(self.PUBLISHED,self.PAYLOAD))
                self.assertNotIn(head,before[self.TOOL_PATHS[0]].decode())
                self.gate(root,module)
                self.assertEqual({p:(root/p).read_bytes() for p in before},before)
                if step==0:self.run_git(root,"commit","--allow-empty","--quiet","-m","Synthetic later qualification evidence")

    def test_dirty_tracked_and_untracked_repositories_are_rejected(self):
        module=self.provider()
        with self.repository() as root:
            tracked=root/".gitattributes";saved=tracked.read_bytes();tracked.write_bytes(saved+b"\n# fixture dirt\n")
            with self.assertRaisesRegex(module.d.Failure,"SOURCE_DIRTY"):self.gate(root,module)
            tracked.write_bytes(saved)
            (root/"unexpected-fixture.txt").write_bytes(b"untracked fixture")
            with self.assertRaisesRegex(module.d.Failure,"SOURCE_DIRTY"):self.gate(root,module)

    def test_wrong_source_location_and_origin_are_rejected(self):
        module=self.provider()
        with self.repository() as root:
            with self.assertRaisesRegex(module.d.Failure,"SOURCE_ROOT_MISMATCH"):self.gate(root,module,cwd=root/"tools")
            self.run_git(root,"remote","set-url","origin","https://example.invalid/unapproved.git")
            with self.assertRaisesRegex(module.d.Failure,"SOURCE_REMOTE_MISMATCH"):self.gate(root,module)

    def test_missing_payload_commit_is_rejected(self):
        module=self.provider()
        with self.repository(empty=True) as root:
            with self.assertRaisesRegex(module.d.Failure,"SOURCE_INVALID"):self.gate(root,module)

    def test_unrelated_commit_is_rejected_even_when_payload_objects_are_present(self):
        module=self.provider()
        with self.repository() as root:
            tree=self.run_git(root,"mktree",data=b"").decode().strip()
            unrelated=self.run_git(root,"commit-tree",tree,data=b"Unrelated fixture history\n").decode().strip()
            self.run_git(root,"checkout","--quiet","--detach",unrelated)
            with self.assertRaisesRegex(module.d.Failure,"SOURCE_HISTORY_MISMATCH"):self.gate(root,module)

    def test_corrupted_payload_blob_is_rejected_in_unshared_fixture_object_store(self):
        module=self.provider()
        with self.repository() as root:
            oid=module.d.MANIFEST[0]["git_blob"]
            obj=root/".git"/"objects"/oid[:2]/oid[2:];obj.parent.mkdir(exist_ok=True)
            if obj.exists():self.assertEqual(obj.stat().st_nlink,1)
            obj.write_bytes(b"corrupt synthetic loose Git object")
            with self.assertRaisesRegex(module.d.Failure,"SOURCE_INVALID"):self.gate(root,module)

    def test_wrong_payload_sha_or_blob_pin_rejects_real_git_objects(self):
        module=self.provider()
        with self.repository() as root:
            for field,value in (("sha256","0"*64),("git_blob","0"*40)):
                manifest=copy.deepcopy(module.d.MANIFEST);manifest[0][field]=value
                with self.subTest(field=field),patch.object(module.d,"MANIFEST",manifest):
                    with self.assertRaisesRegex(module.d.Failure,"SOURCE_IDENTITY_MISMATCH"):self.gate(root,module)

    def test_provider_detects_changed_controller_in_otherwise_valid_published_repository(self):
        trusted=self.provider()
        with self.repository() as root:
            self.publish_fixture_tools(root)
            target=root/self.TOOL_PATHS[0];target.write_bytes(target.read_bytes()+b"\n# unapproved tooling change\n")
            self.run_git(root,"add","--",self.TOOL_PATHS[0]);self.run_git(root,"commit","--quiet","-m","Unapproved synthetic controller change")
            self.gate(root,trusted)  # Repository integrity is deliberately NOT code approval.
            with self.assertRaisesRegex(RuntimeError,"ACCEPTED_CONTROLLER_CHANGED"):self.provider(root)

    def test_valid_published_repository_never_authorizes_native_mutation(self):
        with self.repository() as root,tempfile.TemporaryDirectory(prefix="hioc-pe73-blocked-runtime-") as directory:
            self.publish_fixture_tools(root);module,source=self.gate(root,self.provider(root))
            fs=prior.FixtureFS(Path(directory))
            raw=("\n".join(module.d.CRON)+"\n").encode();inventory={x:"EXCLUDE" for x in module.d.CRON}
            # Exercise actual unconditional native methods on Windows; no gate is
            # replaced. __new__ avoids only the Linux target-observation constructor.
            ops=module.NativeOps.__new__(module.NativeOps)
            provider=module.WindowConsumers(ops,raw,list(module.d.CRON),inventory)
            controller=provider.bind(fs,source)
            before={p.relative_to(fs.root).as_posix():p.read_bytes() for p in fs.root.rglob("*") if p.is_file()}
            with patch.object(module.subprocess,"run",side_effect=AssertionError("Unexpected native command")):
                for action in ("prepare","commit","rollback"):
                    with self.subTest(action=action),self.assertRaisesRegex(module.d.Failure,"NATIVE_WINDOW_ACCEPTANCE_REQUIRED"):
                        getattr(controller,action)("SYNTHETIC_NOT_NATIVE_APPROVAL","0"*64)
                for action in ("PRESERVE","RELEASE"):
                    with self.subTest(action=action),self.assertRaisesRegex(module.d.Failure,"NATIVE_WINDOW_ACCEPTANCE_REQUIRED"):
                        provider.progress(action,{"approved":True})
                with self.assertRaisesRegex(module.d.Failure,"NATIVE_WINDOW_ACCEPTANCE_REQUIRED"):
                    provider.authorize_runtime({"action":"COMMIT","approved":True})
                with self.assertRaisesRegex(module.d.Failure,"NATIVE_SCHEDULER_NOT_QUALIFIED"):
                    ops.install_scheduler(raw,"0"*64)
            self.assertEqual(before,{p.relative_to(fs.root).as_posix():p.read_bytes() for p in fs.root.rglob("*") if p.is_file()})
            self.assertFalse(fs.publications)

    def test_real_repository_source_keeps_journal_and_window_authorization_boundaries(self):
        with self.repository() as root,tempfile.TemporaryDirectory(prefix="hioc-pe73-journal-integration-") as directory:
            module,source=self.gate(root)
            fs=prior.FixtureFS(Path(directory));raw=("\n".join(module.d.CRON)+"\n").encode()
            # Explicit synthetic Ops, as in the existing transaction tests. This
            # does not qualify or override the actual NativeOps gates tested above.
            ops=Ops(raw);provider=module.WindowConsumers(ops,raw,list(module.d.CRON),{x:"EXCLUDE" for x in module.d.CRON})
            controller=provider.bind(fs,source);before=module.d.preflight(fs,source,provider)
            controller.prepare("PREPARE_GIT_INTEGRATION_FIXTURE",module.d.sha(module.d.canonical(before)))
            journal=controller._journal();self.assertEqual(journal["release"],self.PAYLOAD)
            with self.assertRaisesRegex(module.d.Failure,"WINDOW_AUTHORIZATION_INVALID"):
                provider.authorize_runtime({"action":"COMMIT"})
            for field,value in (("release",self.PUBLISHED),("checkout_authorized",True)):
                bad=copy.deepcopy(journal);bad[field]=value;fs.journal(bad)
                with self.assertRaises(module.d.Failure):controller._journal()
                fs.journal(journal)
            self.assertEqual(controller._journal()["release"],self.PAYLOAD)
            self.assertFalse(fs.publications)


if __name__=="__main__":unittest.main()
