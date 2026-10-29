"""Focused successor adapter checks; real temporary bytes, explicit synthetic POSIX metadata."""
import ast
import contextlib
import copy
import hashlib
import importlib.util
import inspect
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('successor_under_test', ROOT/'tools/pe73_successor_delivery.py')
s = importlib.util.module_from_spec(spec);spec.loader.exec_module(s)

def git(*a):
    return subprocess.check_output(['git','--no-optional-locks',*a],cwd=ROOT)

class SuccessorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = {}
        cls.w, cls.m = s.load()
        for item in cls.m['artifacts']:
            cls.source[item['path']] = git('show',s.RELEASE+':'+item['path'])
        cls.old = {x['path']:git('cat-file','blob',git('rev-parse',cls.m['prior_release']+':'+x['path']).decode().strip()) for x in cls.m['artifacts']}

    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='pe73-successor-synthetic-')
        self.w,self.m=s.load();self.d=self.w.d
        # Reuse the accepted fixture implementation in a private test namespace.
        fspec=importlib.util.spec_from_file_location('successor_isolated_fixture',ROOT/'tests/test_pe73_pi3_delivery.py')
        f=importlib.util.module_from_spec(fspec);fspec.loader.exec_module(f)
        f.d=self.d;f.BASE=self.old
        self.base=f.FixtureFS(Path(self.temp.name))
        self.base.path(s.HISTORICAL_TX).mkdir()
        self.base.write_new(s.HISTORICAL_TX+'/journal.json',b'HISTORICAL_FIXTURE_NOT_A_NATIVE_VALIDATION')
        self.history=self.base.snapshot(s.HISTORICAL_TX+'/journal.json',0o600)
        self.fs=s.GuardedFS(self.base,self.w,self.m,self.history)
        class Ops:
            boot_id='BOOT_SYNTHETIC';clock=1000;active=[];complete=True
            def now(o):return o.clock
            def live_gate(o):pass  # Explicit synthetic admission seam, never native.
            def scheduler(o):return o.raw
            def install_scheduler(o,raw,expected):
                self.d.require(self.d.sha(o.raw)==expected,'SCHEDULER_CONFLICT');o.calls.append(raw)
                if o.fail:raise OSError('PRIVATE_SYNTHETIC')
                o.raw=raw
            def processes(o):return {'boot_id':o.boot_id,'observed_at':o.clock,'known_active':copy.deepcopy(o.active),'inspection_complete':o.complete,'limitations':['CACHED_MODULES_UNKNOWN'],'universal_exclusion':False}
        self.ops=Ops();self.ops.fail=False;self.ops.calls=[]
        self.ops.raw=('\n'.join(self.d.CRON)+'\n7 * * * * unrelated-job\n').encode()
        self.original=self.ops.raw
        inventory={x:'EXCLUDE' for x in self.d.CRON};inventory['7 * * * * unrelated-job']='PRESERVE'
        self.p=self.w.WindowConsumers(self.ops,self.original,list(self.d.CRON),inventory)
        self.c=self.p.bind(self.fs,self.source);self.count=0

    def tearDown(self):
        self.assertEqual(self.base.read(s.HISTORICAL_TX+'/journal.json'),b'HISTORICAL_FIXTURE_NOT_A_NATIVE_VALIDATION')
        self.base.assert_unrelated(self)
        self.temp.cleanup()

    def grant(self,action):
        self.count+=1
        return {'action':action,'reference':'SUCCESSOR_SYNTHETIC_'+str(self.count),'journal_sha256':self.d.sha(self.d.canonical(self.c._journal())),'scheduler_sha256':self.d.sha(self.ops.raw),'operator':'SYNTHETIC_OPERATOR','session':self.p.session,'boot_id':self.ops.boot_id,'expires_at':self.ops.clock+600,'exclusive_responsibility':True,'risks_acknowledged':list(self.w.RISKS)}
    def prepare(self):
        value=self.d.preflight(self.fs,self.source,self.p)
        return self.c.prepare('SUCCESSOR_SYNTHETIC_PREPARE',self.d.sha(self.d.canonical(value)))
    def establish(self):
        self.prepare()
        for action in ['PRESERVE','EXCLUDE','DRAIN','ESTABLISH']:self.p.progress(action,self.grant(action))
    def runtime(self,action):
        grant=self.grant(action);self.p.authorize_runtime(grant)
        return getattr(self.c,action.lower())(grant['reference'],grant['journal_sha256'])

    def test_exact_thirteen_source_pins_and_three_deltas(self):
        self.d.check_sources(self.source)
        self.assertEqual(len(self.m['artifacts']),13);self.assertEqual(len(self.m['changed_paths']),3)
        self.assertEqual(self.m['changed_paths'],sorted(p for p in self.old if self.old[p]!=self.source[p]))
    def test_every_wrong_source_object_rejected(self):
        for path in self.source:
            with self.subTest(path=path),self.assertRaises(self.d.Failure):self.d.check_sources(dict(self.source,**{path:self.source[path]+b' '}))
    def test_original_modules_are_isolated(self):
        old,_=s.load(successor=False)
        self.assertNotEqual(old.d.TX,self.d.TX);self.assertEqual(old.d.RELEASE,self.m['prior_release'])
        self.assertEqual(self.d.RELEASE,s.RELEASE)
    def test_original_algorithms_and_scheduler_source_are_preserved(self):
        old,_=s.load(successor=False)
        for obj in ['Controller','NativeFS','NativeConsumers','source_gate','check_sources','preflight']:
            left,right=getattr(old.d,obj),getattr(self.d,obj)
            if inspect.isclass(left):
                first=dict(inspect.getmembers(left,inspect.isfunction));second=dict(inspect.getmembers(right,inspect.isfunction))
                self.assertEqual(set(first),set(second))
                for name in first:self.assertEqual(inspect.getsource(first[name]),inspect.getsource(second[name]))
            else:self.assertEqual(inspect.getsource(left),inspect.getsource(right))
        operation=(inspect.getsource(self.w.NativeOps.scheduler)+'\n'+inspect.getsource(self.w.NativeOps.install_scheduler)).encode()
        self.assertEqual(self.d.sha(operation),self.w.SCHEDULER_OPERATION_PIN)
        self.assertEqual(self.w.PIN,self.m['controller_sha256'])
    def test_thirteen_backups_and_only_three_live_replacements(self):
        before={p:self.fs.snapshot(p,self.d.MODES[p]) for p in self.source}
        self.establish();self.runtime('COMMIT')
        self.assertEqual(set(self.base.publications),set(self.m['changed_paths']))
        self.assertEqual(self.c._journal()['state'],'COMMITTED')
        for i,p in enumerate(self.d.ORDER):
            self.assertEqual(self.fs.read(self.d.TX+'/backup-'+str(i)),self.old[p])
            self.assertEqual(self.fs.read(p,self.d.MODES[p]),self.source[p])
            if p not in self.m['changed_paths']:self.assertEqual(self.fs.snapshot(p,self.d.MODES[p]),before[p])
    def test_explicit_rollback_restores_only_three_and_original_bytes(self):
        self.establish();self.runtime('COMMIT');self.runtime('ROLLBACK')
        self.assertEqual(self.c._journal()['state'],'ROLLED_BACK')
        self.assertEqual(len(self.base.publications),6)
        for p in self.source:self.assertEqual(self.fs.read(p,self.d.MODES[p]),self.old[p])
    def test_release_restores_exact_scheduler(self):
        self.establish();self.runtime('COMMIT')
        for a in ['AUTHORIZE_RELEASE','RESTORE_SCHEDULER','RELEASE']:self.p.progress(a,self.grant(a))
        self.assertEqual(self.ops.raw,self.original);self.assertEqual(self.c._journal()['window']['phase'],'RELEASED')
    def test_no_unfenced_commit(self):
        self.prepare()
        with self.assertRaises(Exception):self.runtime('COMMIT')
        self.assertEqual(self.base.publications,[])
    def test_active_consumer_blocks_drain(self):
        self.prepare()
        for a in ['PRESERVE','EXCLUDE']:self.p.progress(a,self.grant(a))
        self.ops.active=[{'pid':99,'start_ticks':1,'command_sha256':'a'*64}]
        with self.assertRaises(self.d.Failure):self.p.progress('DRAIN',self.grant('DRAIN'))
        self.assertEqual(self.base.publications,[])
    def test_incomplete_process_visibility_blocks_drain(self):
        self.prepare()
        for a in ['PRESERVE','EXCLUDE']:self.p.progress(a,self.grant(a))
        self.ops.complete=False
        with self.assertRaises(self.d.Failure):self.p.progress('DRAIN',self.grant('DRAIN'))
    def test_native_fallback_still_refuses(self):
        with self.assertRaises(self.d.Failure):self.d.NativeConsumers().assert_active()
    def test_boot_change_blocks_operation(self):
        self.establish();grant=self.grant('COMMIT');self.ops.boot_id='DIFFERENT_BOOT'
        with self.assertRaises(self.d.Failure):self.p.authorize_runtime(grant)
    def test_scheduler_drift_blocks_operation(self):
        self.establish();self.ops.raw+=b'9 * * * * unexpected\n'
        with self.assertRaises(self.d.Failure):self.runtime('COMMIT')
    def test_backup_drift_blocks_all_publication(self):
        self.establish();self.base.path(self.d.TX+'/backup-0').write_bytes(b'WRONG')
        with self.assertRaises(self.d.Failure):self.runtime('COMMIT')
        self.assertEqual(self.base.publications,[])
    def test_stage_drift_blocks_all_publication(self):
        self.establish();self.base.path(self.d.TX+'/stage-0').write_bytes(b'WRONG')
        with self.assertRaises(self.d.Failure):self.runtime('COMMIT')
        self.assertEqual(self.base.publications,[])
    def test_changed_mode_owner_and_hardlink_refuse(self):
        path=self.m['changed_paths'][0]
        for attr,value in [('modes',0o777),('uids',0),('gids',0)]:
            table=getattr(self.base,attr);old=table.get(path);table[path]=value
            with self.assertRaises(self.d.Failure):self.prepare()
            if old is None:table.pop(path)
            else:table[path]=old
    def test_historical_journal_identity_drift_blocks_new_writes(self):
        path=s.HISTORICAL_TX+'/journal.json';original=self.history
        snapshot=self.base.snapshot
        with patch.object(self.base,'snapshot',side_effect=lambda p,mode=None:dict(original,sha256='0'*64) if p==path else snapshot(p,mode)):
            with self.assertRaisesRegex(ValueError,'PREDECESSOR_JOURNAL_DRIFT'):self.fs.mkdir_tx()
    def test_no_reuse_of_existing_successor_transaction(self):
        self.prepare()
        with self.assertRaises(self.d.Failure):self.prepare()
    def test_unchanged_file_publication_is_identity_checked(self):
        p=next(iter(self.fs.unchanged));before=self.fs.snapshot(p,self.d.MODES[p])
        with self.assertRaisesRegex(ValueError,'UNCHANGED_ARTIFACT_DRIFT'):self.fs.publish(p,b'BAD',before,self.d.MODES[p])
        self.assertEqual(self.base.publications,[])
    def test_unrelated_publication_and_removal_refused(self):
        with self.assertRaises(ValueError):self.fs.publish('unrelated.txt',b'BAD',{},0o600)
        with self.assertRaises(ValueError):self.fs.remove_installed('unrelated.txt',{},0o600)
        with self.assertRaises(ValueError):self.fs.write_new(s.HISTORICAL_TX+'/overwrite',b'BAD')
    def test_interrupted_publication_is_pending_and_not_retried(self):
        self.establish();target=next(p for p in self.d.ORDER if p in self.m['changed_paths'])
        def fault(point):
            if point=='AFTER_PUBLICATION:'+target:raise OSError('PRIVATE_SYNTHETIC')
        self.c.fault=fault
        with self.assertRaises(OSError):self.runtime('COMMIT')
        value=self.c._journal();self.assertEqual(value['state'],'COMMITTING');self.assertEqual(value['pending'],target)
        count=len(self.base.publications)
        with self.assertRaises(Exception):self.runtime('COMMIT')
        self.assertEqual(len(self.base.publications),count);self.assertNotEqual(self.ops.raw,self.original)
    def test_uncertain_scheduler_restoration_is_not_retried_or_released(self):
        self.establish();self.runtime('COMMIT');self.p.progress('AUTHORIZE_RELEASE',self.grant('AUTHORIZE_RELEASE'));self.ops.fail=True
        with self.assertRaises(OSError):self.p.progress('RESTORE_SCHEDULER',self.grant('RESTORE_SCHEDULER'))
        count=len(self.ops.calls)
        with self.assertRaises(self.d.Failure):self.p.progress('RESTORE_SCHEDULER',self.grant('RESTORE_SCHEDULER'))
        self.assertEqual(len(self.ops.calls),count);self.assertEqual(self.c._journal()['window']['phase'],'RESTORE_UNCERTAIN')
    def test_tool_and_manifest_tampering_rejected_before_execution(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);(root/'governance/pe7').mkdir(parents=True)
            (root/'governance/pe7/pe73-successor-delivery.json').write_bytes(b'{}')
            with self.assertRaisesRegex(ValueError,'SUCCESSOR_MANIFEST_IDENTITY'):s.load(root)
    def test_source_gate_checks_released_payload_and_clean_origin(self):
        def run(argv,**kwargs):
            a=argv[3:];out=b'';status=0
            if a==['rev-parse','--verify','HEAD^{commit}']:out=b'a'*40
            elif a==['rev-parse','--show-toplevel']:out=str(self.d.SOURCE).encode()
            elif a==['remote','get-url','origin']:out=b'https://github.com/jorgeazofeifa-creator/hioc.git'
            elif a==['status','--porcelain=v1','--untracked-files=all']:out=b''
            elif a==['rev-parse','--verify',s.RELEASE+'^{commit}']:out=s.RELEASE.encode()
            elif a[:2]==['merge-base','--is-ancestor']:pass
            elif a[0]=='show':out=self.source[a[1].split(':',1)[1]]
            elif a[0]=='rev-parse':out=next(x['git_blob'].encode() for x in self.m['artifacts'] if x['path']==a[1].split(':',1)[1])
            else:raise AssertionError(a)
            return type('Result',(),{'returncode':status,'stdout':out})()
        with patch.object(self.d.subprocess,'run',side_effect=run):self.assertEqual(self.d.source_gate(),self.source)
        def dirty(argv,**kwargs):
            r=run(argv,**kwargs)
            if argv[3:]==['status','--porcelain=v1','--untracked-files=all']:r.stdout=b' M dirty'
            return r
        with patch.object(self.d.subprocess,'run',side_effect=dirty),self.assertRaises(self.d.Failure):self.d.source_gate()
    def test_native_inspection_does_not_grant_execution(self):
        text=inspect.getsource(s.native_assessment)
        for forbidden in ['.prepare(','.commit(','.rollback(','.install_scheduler(','.mutex(','.perform_next(']:self.assertNotIn(forbidden,text)
        self.assertIn("'native_execution_authorized': False",text)

    def test_predecessor_uses_original_strict_committed_released_validation(self):
        import test_pe73_maintenance_window as historical_fixture
        case=historical_fixture.WindowTests('test_manual_control_truthful')
        case.setUp()
        try:
            case.establish();case.runtime('COMMIT')
            for action in ['AUTHORIZE_RELEASE','RESTORE_SCHEDULER','RELEASE']:case.step(action)
            historical,_=s.load(successor=False)
            with patch.object(historical.d,'source_gate',return_value=historical_fixture.prior.SOURCE):
                observed=s.predecessor(case.fs,historical)
                self.assertTrue(observed['exists'])
                value=case.c._journal();value['window']['phase']='SCHEDULER_RESTORED'
                case.fs.journal(value)
                with self.assertRaises(Exception):s.predecessor(case.fs,historical)
        finally:case.tearDown()
    def test_real_hardlink_blocks_prepare(self):
        import os
        path=self.m['changed_paths'][0];link=self.base.root/'temporary-test-hardlink'
        os.link(self.base.path(path),link)
        try:
            with self.assertRaises(self.d.Failure):self.prepare()
        finally:link.unlink()
    def test_native_admission_cannot_be_replaced_by_json(self):
        ops=self.w.NativeOps.__new__(self.w.NativeOps)
        ops._admission={'approved':True}
        with self.assertRaises(self.d.Failure):ops.live_gate()
    def test_changed_provider_refuses_before_execution(self):
        import shutil
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);(root/'tools').mkdir();(root/'governance/pe7').mkdir(parents=True)
            shutil.copyfile(ROOT/'governance/pe7/pe73-successor-delivery.json',root/'governance/pe7/pe73-successor-delivery.json')
            shutil.copyfile(ROOT/'tools/hioc-pe73-pi3-delivery.py',root/'tools/hioc-pe73-pi3-delivery.py')
            (root/'tools/pe73_maintenance_window.py').write_bytes(b'raise RuntimeError("MUST_NOT_RUN")')
            with self.assertRaisesRegex(ValueError,'TOOL_SOURCE_IDENTITY'):s.load(root)

    def test_existing_whole_process_sequence_installs_three_and_releases(self):
        coordinator=self.w.MaintenanceCoordinator(self.p,lambda:self.source)
        sequence=self.w._ApprovedSequence(coordinator)
        for expected in self.w.DEPLOYMENT_SEQUENCE:
            action,_=sequence.perform_next();self.assertEqual(action,expected)
        self.assertEqual(self.c._journal()['state'],'COMMITTED')
        self.assertEqual(self.c._journal()['window']['phase'],'RELEASED')
        self.assertEqual(self.ops.raw,self.original)
        self.assertEqual(set(self.base.publications),set(self.m['changed_paths']))
    def test_sequence_context_change_stops_without_restoration(self):
        coordinator=self.w.MaintenanceCoordinator(self.p,lambda:self.source)
        sequence=self.w._ApprovedSequence(coordinator)
        for _ in range(5):sequence.perform_next()
        self.ops.active=[{'pid':99,'start_ticks':2,'command_sha256':'a'*64}]
        with self.assertRaises(self.d.Failure):sequence.perform_next()
        self.assertTrue(sequence.stopped)
        self.assertEqual(self.base.publications,[])
        self.assertNotEqual(self.ops.raw,self.original)
        with self.assertRaises(self.d.Failure):sequence.perform_next()
    def test_sequence_expiry_stops_without_retry(self):
        coordinator=self.w.MaintenanceCoordinator(self.p,lambda:self.source)
        sequence=self.w._ApprovedSequence(coordinator)
        for _ in range(3):sequence.perform_next()
        self.ops.clock+=4000
        with self.assertRaises(self.d.Failure):sequence.perform_next()
        self.assertNotEqual(self.ops.raw,self.original)
        self.assertEqual(self.base.publications,[])

if __name__=='__main__':unittest.main()
