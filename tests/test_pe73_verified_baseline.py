"""Risk-based current-baseline delivery tests; Windows fixtures, never native authority."""
import ast
import contextlib
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from hioc.assets import AssetLock

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('verified_baseline_tests',ROOT/'tools/pe73_verified_baseline.py')
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)

class BaselineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.adapter=b.adapter();w,cls.manifest=cls.adapter.load()
        refs=[release+':'+x['path'] for release in (cls.manifest['prior_release'],cls.manifest['release']) for x in cls.manifest['artifacts']]
        packed=subprocess.check_output(['git','--no-optional-locks','--no-replace-objects','cat-file','--batch'],cwd=ROOT,input=('\n'.join(refs)+'\n').encode())
        values=[];at=0
        for ref in refs:
            end=packed.index(b'\n',at);header=packed[at:end].split();assert header[1]==b'blob';size=int(header[2]);at=end+1
            values.append(packed[at:at+size]);at+=size+1
        cls.prior={x['path']:raw for x,raw in zip(cls.manifest['artifacts'],values[:13])}
        cls.source={x['path']:raw for x,raw in zip(cls.manifest['artifacts'],values[13:])}
        # Reuse the existing FixtureFS class without running its historical Git setup.
        tree=ast.parse((ROOT/'tests/test_pe73_pi3_delivery.py').read_bytes())
        node=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='FixtureFS')
        namespace=dict(d=w.d,BASE=cls.prior,Path=Path,os=os,contextlib=contextlib,AssetLock=AssetLock)
        exec(compile(ast.Module(body=[node],type_ignores=[]),'existing_FixtureFS','exec'),namespace)
        cls.FixtureFS=namespace['FixtureFS']
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='pe73-baseline-')
        self.addCleanup(self.temp.cleanup)
        self.base=self.FixtureFS(Path(self.temp.name))
        self.history={'backups/pe73-full-inventory-delivery-v1/journal.json':b'ROLLED_BACK retained',
            'backups/pe73-full-inventory-delivery-v1/prepared-recovery-claim.json':b'claim retained',
            'backups/pe73-full-inventory-delivery-v1/controlled-restoration-intent.json':b'intent retained'}
        for path,raw in self.history.items():self.base.path(path).parent.mkdir(exist_ok=True);self.base.write_new(path,raw)
        w,_=self.adapter.load();original=('\n'.join(w.d.CRON)+'\n7 * * * * unrelated-job\n').encode()
        class Ops:
            boot_id='BOOT_FIXTURE';clock=1000;active=[];complete=True;offset=0;_admission=None
            raw=original;fail_scheduler=None
            def now(o):return o.clock
            def scheduler(o):return o.raw
            def processes(o):return dict(boot_id=o.boot_id,observed_at=o.clock+o.offset,
                known_active=copy.deepcopy(o.active),inspection_complete=o.complete,
                limitations=['UNCLASSIFIED_PID_14','CACHED_MODULES_UNKNOWN'],universal_exclusion=False)
            def live_gate(o):
                a=o._admission
                b.require(a is not None and a.ops is o and a.boot_id==o.boot_id and o.clock<a.expires_at,'SYNTHETIC_ADMISSION_REQUIRED')
            def scheduler_gate(o):o.live_gate()
            def install_scheduler(o,raw,expected):
                o.scheduler_gate();b.require(b.sha(o.raw)==expected,'WINDOW_SCHEDULER_DRIFT');o.calls.append(raw)
                if o.fail_scheduler=='BEFORE':raise OSError('PRIVATE_SCHEDULER_ERROR')
                o.raw=raw
                if o.fail_scheduler=='AFTER':raise OSError('PRIVATE_SCHEDULER_ACK')
        class SessionOps(Ops):
            shared={'boot_id','clock','active','complete','offset','raw','fail_scheduler','calls'}
            def __init__(o,state):object.__setattr__(o,'state',state)
            def __getattribute__(o,name):
                if name in object.__getattribute__(o,'shared'):return object.__getattribute__(o,'state')[name]
                return object.__getattribute__(o,name)
            def __setattr__(o,name,value):
                if name in o.shared:o.state[name]=value
                else:object.__setattr__(o,name,value)
        self.SessionOps=SessionOps
        self.ops=SessionOps(dict(boot_id='BOOT_FIXTURE',clock=1000,active=[],complete=True,offset=0,raw=original,fail_scheduler=None,calls=[]))
        self.policy=b.contract();self.policy.update(original_scheduler_sha256=b.sha(original),
            reduced_scheduler_sha256=b.sha(b'7 * * * * unrelated-job\n'),scheduler_entry_count=4)
        self.patch=patch.object(b,'contract',return_value=self.policy);self.patch.start();self.addCleanup(self.patch.stop)
        self.initial=self.op(establishment=True);self.initial.establish()
    def view(self,w):
        base=self.base
        class View:
            def __getattr__(self,n):return getattr(base,n)
            def transaction_present(o):return base.path(w.d.TX).is_dir()
            def mkdir_tx(o):base.path(w.d.TX).mkdir(mode=0o700)
            def journal(o,v):
                raw=w.d.canonical(v);o.write_new(w.d.TX+'/journal-next',raw)
                os.replace(base.path(w.d.TX+'/journal-next'),base.path(w.d.TX+'/journal.json'))
                base.modes[w.d.TX+'/journal.json']=0o600
            def write_new(o,*args,**kwargs):return base.write_new(*args,**kwargs)
            def archive(o,src,dst,*,snapshot,mode):
                b.require(base.snapshot(src,mode)==snapshot and not base.path(dst).exists(),'RECOVERY_ARCHIVE_DRIFT')
                os.rename(base.path(src),base.path(dst));base.modes[dst]=mode
            def entries(o,path):return {p.name for p in base.path(path).iterdir()}
        return View()
    def op(self,**kwargs):
        w,m=self.adapter.load()
        return b.Operations(w,m,self.view(w),self.SessionOps(self.ops.state),self.source,lambda:self.source,
            tooling={'commit':'a'*40,'tree':'b'*40},**kwargs)
    def control(self):return json.loads(self.base.read(b.CONTROL))
    def recover(self,op,**kwargs):return self.op(transaction_id=op.id,recovery=True,**kwargs)
    def partial(self,point=None):
        op=self.op();point=point or 'INSTALLED:'+op.d.ORDER[4]
        def fault(p):
            if p==point:raise RuntimeError('SYNTHETIC_INTERRUPTION')
        op.co.controller.fault=fault
        with self.assertRaises(RuntimeError):op.deploy()
        return op
    def tearDown(self):
        for path,raw in self.history.items():self.assertEqual(self.base.read(path),raw)
        self.base.assert_unrelated(self)
    def test_new_attempt_after_rollback_retains_history_and_uses_new_identity(self):
        first=self.partial();recovery=self.recover(first);receipt=recovery.recover()
        self.assertEqual(receipt['state'],'ROLLED_BACK');self.assertIsNone(self.control()['active'])
        next_attempt=self.op();self.assertNotEqual(first.id,next_attempt.id)
        next_attempt.deploy();self.assertIsNone(self.control()['active'])
        self.assertEqual(self.control()['baseline']['payload_release'],self.manifest['release'])
        self.assertTrue(self.base.path(first.d.TX+'/journal.json').exists())
    def test_changed_historical_inode_and_ctime_do_not_block_current_baseline(self):
        path=self.manifest['changed_paths'][0];old=self.base.snapshot(path)
        self.base.publish(path,self.prior[path],old,old['identity']['mode'])
        self.assertNotEqual(old,self.base.snapshot(path))
        self.op()  # semantic current baseline passes; no old journal traversal.
    def test_duplicate_transaction_identity_is_rejected(self):
        op=self.partial();self.recover(op).recover()
        with self.assertRaisesRegex(ValueError,'TRANSACTION_ID_ALREADY_USED'):self.op(transaction_id=op.id)
    def test_active_transaction_blocks_new_attempt(self):
        op=self.partial()
        with self.assertRaisesRegex(ValueError,'ACTIVE_OR_UNCERTAIN_TRANSACTION'):self.op()
        self.assertEqual(self.control()['active']['id'],op.id)
    def test_content_mode_owner_hardlink_and_unsafe_id_rejected(self):
        path=self.manifest['changed_paths'][0];raw=self.base.read(path,self.base.modes[path])
        self.base.path(path).write_bytes(raw+b'X')
        with self.assertRaises(Exception):self.op()
        self.base.path(path).write_bytes(raw)
        mode=self.base.modes[path];self.base.modes[path]=0o666
        with self.assertRaises(Exception):self.op()
        self.base.modes[path]=mode;self.base.uids[path]=0
        with self.assertRaises(Exception):self.op()
        self.base.uids[path]=1000
        link=self.base.path(path+'.link');os.link(self.base.path(path),link)
        with self.assertRaises(Exception):self.op()
        link.unlink()
        with self.assertRaisesRegex(ValueError,'TRANSACTION_ID_INVALID'):self.op(transaction_id='../escape')
    def test_transaction_local_runtime_source_and_scheduler_drift_refused(self):
        op=self.op();path=self.manifest['changed_paths'][0];old=self.base.snapshot(path)
        self.base.publish(path,self.prior[path],old,old['identity']['mode'])
        with self.assertRaisesRegex(ValueError,'TRANSACTION_LOCAL_RUNTIME_DRIFT'):op.deploy()
        self.assertIsNone(self.control()['active'])
        op=self.op();op.source_reader=lambda:dict(self.source,**{path:self.source[path]+b'X'})
        with self.assertRaises(Exception):op.deploy()
        self.assertIsNone(self.control()['active'])
        op=self.op();self.ops.raw+=b'UNAUTHORIZED_CRON\n'
        with self.assertRaises(Exception):op.deploy()
        self.assertIsNone(self.control()['active'])

    def test_unauthorized_release_wrong_target_and_bad_source_rejected(self):
        w,m=self.adapter.load();bad=copy.deepcopy(m);bad['release']='f'*40
        with self.assertRaisesRegex(ValueError,'SOURCE_RELEASE_NOT_AUTHORIZED'):
            b.Operations(w,bad,self.view(w),self.SessionOps(self.ops.state),self.source,lambda:self.source,tooling={'commit':'a'*40,'tree':'b'*40})
        with self.assertRaisesRegex(ValueError,'TARGET_IDENTITY'):self.op(target=dict(b.TARGET,uid=0))
        w,m=self.adapter.load();wrong=dict(self.source);wrong[next(iter(wrong))]+=b'X'
        with self.assertRaises(Exception):b.Operations(w,m,self.view(w),self.ops,wrong,lambda:wrong,tooling={'commit':'a'*40,'tree':'b'*40})
    def test_consumers_completeness_freshness_and_exact_failure_evidence(self):
        for kind in ('active','incomplete','stale'):
            self.ops.active=[];self.ops.complete=True;self.ops.offset=0
            if kind=='active':self.ops.active=[dict(pid=19,start_ticks=2,command_sha256='c'*64)]
            if kind=='incomplete':self.ops.complete=False
            if kind=='stale':self.ops.offset=-31
            op=self.op()
            with self.assertRaises(Exception) as caught:op.deploy()
            receipt=getattr(caught.exception,'process_guard',None);self.assertIsNotNone(receipt,kind+': '+repr(caught.exception))
            self.assertEqual(receipt['failed_predicate'],{'active':'known_consumers_absent','incomplete':'inspection_completeness','stale':'observation_freshness'}[kind])
            self.ops.active=[];self.ops.complete=True;self.ops.offset=0
            op.ops.processes()
            self.assertEqual(op.recorder.receipt(op.w),receipt)
            self.assertIsNone(self.control()['active'])
    def test_boot_change_and_wrong_recovery_transaction_refused(self):
        op=self.partial()
        with self.assertRaisesRegex(ValueError,'WRONG_RECOVERY_TRANSACTION'):self.op(transaction_id='f'*32,recovery=True)
        recover=self.recover(op);old=self.ops.boot_id
        def gate():
            self.ops.boot_id='DIFFERENT_BOOT';raise ValueError('TARGET_BOOT_CHANGED')
        with patch.object(recover.ops,'live_gate',side_effect=gate),self.assertRaises(ValueError):recover.recover()
        self.ops.boot_id=old;self.assertIsNotNone(self.control()['active'])
    def test_partial_publication_without_progress_can_be_reconciled_and_rolled_back(self):
        op=self.partial('AFTER_PUBLICATION:'+self.manifest['changed_paths'][-1])
        self.assertIsNotNone(op.co.controller._journal()['pending'])
        result=self.recover(op).recover()
        self.assertEqual(result['state'],'ROLLED_BACK');self.assertIsNone(self.control()['active'])
    def test_recovery_scheduler_drift_refuses_before_private_evidence_changes(self):
        op=self.partial();directory=self.base.path(op.d.TX)
        before={p.name:p.read_bytes() for p in directory.iterdir()}
        reduced=self.ops.raw
        for unexpected in (op.original,b'UNEXPECTED_CRON\n'):
            self.ops.raw=unexpected
            with self.assertRaisesRegex(ValueError,'WINDOW_SCHEDULER_DRIFT'):self.recover(op).recover()
            self.assertEqual(before,{p.name:p.read_bytes() for p in directory.iterdir()})
        self.ops.raw=reduced
        path=op.d.TX+'/stage-4';raw=self.base.read(path);self.base.path(path).write_bytes(raw+b'X')
        with self.assertRaisesRegex(ValueError,'STAGING_DRIFT'):self.recover(op).recover()
        self.assertIsNotNone(self.control()['active'])

    def test_unknown_pending_content_refused_without_overwrite(self):
        op=self.partial('AFTER_PUBLICATION:'+self.manifest['changed_paths'][-1])
        pending=op.co.controller._journal()['pending'];self.base.path(pending).write_bytes(b'UNEXPECTED_RUNTIME')
        with self.assertRaisesRegex(ValueError,'PENDING_RUNTIME_NOT_ESTABLISHED'):self.recover(op).recover()
        self.assertEqual(self.base.read(pending,self.base.modes[pending]),b'UNEXPECTED_RUNTIME')
        self.assertIsNotNone(self.control()['active'])
    def test_interrupted_rollback_continues_recorded_reverse_prefix(self):
        op=self.partial();recover=self.recover(op)
        def stop(point):
            if point=='RESTORED:'+op.d.ORDER[4]:raise RuntimeError('STOP_ROLLBACK')
        recover.co.controller.fault=stop
        with self.assertRaises(RuntimeError):recover.recover()
        self.assertEqual(recover.co.controller._journal()['state'],'ROLLING_BACK')
        self.ops.boot_id='NEW_BOOT_FIXTURE'
        second=self.recover(op);result=second.recover()
        self.assertEqual(result['state'],'ROLLED_BACK');self.assertIsNone(self.control()['active'])
    def test_scheduler_failure_has_no_automatic_restoration_and_known_readback_recovers(self):
        op=self.op();self.ops.fail_scheduler='AFTER'
        with self.assertRaises(OSError):op.deploy()
        self.assertEqual(len(self.ops.calls),1);self.assertIsNotNone(self.control()['active'])
        self.ops.fail_scheduler=None;recover=self.recover(op);recover.reconcile_scheduler()
        result=recover.recover('RESUME_PREPARED')
        self.assertEqual(result['state'],'COMMITTED');self.assertEqual(self.ops.raw,self.initial.original)
    def test_failed_scheduler_before_exclusion_can_abort_with_no_runtime_effect(self):
        op=self.op();self.ops.fail_scheduler='BEFORE'
        with self.assertRaises(OSError):op.deploy()
        self.ops.fail_scheduler=None;recover=self.recover(op);result=recover.abort_preparation()
        self.assertEqual(result['kind'],'ABORTED_BEFORE_RUNTIME');self.assertIsNone(self.control()['active'])
        self.op()
    def test_success_promotes_only_after_verified_release(self):
        op=self.op();old=self.control()['baseline']['id'];receipt=op.deploy()
        self.assertEqual(receipt['state'],'COMMITTED');self.assertNotEqual(old,self.control()['baseline']['id'])
        self.assertEqual(self.ops.raw,self.initial.original)
        for path,raw in self.source.items():self.assertEqual(self.base.read(path,op.d.MODES[path]),raw)
    def test_partial_failure_cannot_promote_or_release(self):
        op=self.partial();old=self.control()['baseline']['id']
        with self.assertRaisesRegex(ValueError,'BASELINE_PROMOTION_REFUSED'):op.finalize()
        self.assertEqual(old,self.control()['baseline']['id']);self.assertIsNotNone(self.control()['active'])
    def test_control_drift_and_unexpected_transaction_entry_fail_closed(self):
        op=self.partial();path=op.d.TX+'/unknown';self.base.write_new(path,b'not approved')
        with self.assertRaisesRegex(ValueError,'TRANSACTION_UNEXPECTED_ENTRY'):self.recover(op)
        self.base.path(path).unlink()
        raw=self.base.read(b.CONTROL);self.base.path(b.CONTROL).write_bytes(raw+b' ')
        with self.assertRaises(Exception):self.recover(op)
    def test_backup_stage_and_current_transaction_identity_drift_refused(self):
        op=self.partial();path=op.d.TX+'/backup-4';raw=self.base.read(path);self.base.path(path).write_bytes(raw+b'X')
        with self.assertRaisesRegex(ValueError,'BACKUP_DRIFT'):self.recover(op).recover()
        self.assertIsNotNone(self.control()['active'])
    def test_promotion_control_write_interruption_preserves_exact_transition(self):
        op=self.op();publish=self.base.publish;counter=[0]
        def fail(path,*args):
            if path==b.CONTROL:
                counter[0]+=1
                if counter[0]==2:raise OSError('PROMOTION_NOT_WRITTEN')
            return publish(path,*args)
        with patch.object(self.base,'publish',side_effect=fail),self.assertRaises(OSError):op.deploy()
        self.assertEqual(op.co.controller._journal()['window']['phase'],'RELEASED')
        result=self.recover(op).recover('RELEASE')
        self.assertEqual(result['state'],'COMMITTED');self.assertIsNone(self.control()['active'])
    def test_initial_baseline_is_not_automatically_established_or_reapproved(self):
        with self.assertRaisesRegex(ValueError,'BASELINE_ALREADY_ESTABLISHED'):self.initial.establish()
        control=self.control();self.assertEqual(control['baseline']['status'],'APPROVED_VERIFIED')
        self.assertFalse(control['baseline']['compatibility']['activation_authorized'])
    def test_native_factory_refuses_windows_and_pinned_policy_intact(self):
        self.patch.stop()
        actual=b.contract();self.patch.start()
        self.assertFalse(actual['deployment_authorized']);self.assertEqual(actual['scheduler_entry_count'],12)
        with self.assertRaises(Exception):b.native()
        import marshal
        historical,_=self.adapter.load(successor=False);current,_=self.adapter.load()
        for obj,methods in [('Controller',('prepare','commit','rollback')),('NativeFS',('snapshot','publish','journal'))]:
            for name in methods:
                self.assertEqual(marshal.dumps(getattr(getattr(historical.d,obj),name).__code__),
                    marshal.dumps(getattr(getattr(current.d,obj),name).__code__))

    def test_reservation_before_private_creation_can_only_abort_exact_unchanged_state(self):
        op=self.op()
        with patch.object(op.base,'mkdir_tx',side_effect=OSError('PRIVATE_CREATE_INTERRUPTED')),self.assertRaises(OSError):op.deploy()
        self.assertFalse(self.base.path(op.d.TX).exists());self.assertIsNotNone(self.control()['active'])
        result=self.recover(op).abort_preparation()
        self.assertEqual(result['kind'],'ABORTED_BEFORE_RUNTIME');self.assertIsNone(self.control()['active'])
        self.assertEqual(self.ops.calls,[])

    def test_scheduler_restore_failure_requires_explicit_reconciliation_and_release(self):
        op=self.op();installer=self.ops.__class__.install_scheduler
        def fail_restore(ops,raw,expected):
            if raw==op.original:ops.fail_scheduler='BEFORE'
            return installer(ops,raw,expected)
        with patch.object(self.ops.__class__,'install_scheduler',fail_restore),self.assertRaises(OSError):op.deploy()
        self.assertEqual(op.co.controller._journal()['window']['phase'],'RESTORE_UNCERTAIN')
        self.assertEqual(len(self.ops.calls),2);self.ops.fail_scheduler=None
        recover=self.recover(op);recover.reconcile_scheduler()
        self.assertEqual(len(self.ops.calls),3)
        self.assertEqual(recover.recover('RELEASE')['state'],'COMMITTED')
        self.assertEqual(self.ops.raw,op.original)

    def test_promotion_temporary_is_archived_only_for_exact_authorized_transition(self):
        op=self.op();publish=self.base.publish;counter=[0]
        def fail(path,raw,before,mode):
            if path==b.CONTROL:
                counter[0]+=1
                if counter[0]==2:
                    self.base.write_new('backups/.pe73-delivery-pe73-current-baseline.json',raw)
                    raise OSError('AFTER_CONTROL_TEMPORARY')
            return publish(path,raw,before,mode)
        with patch.object(self.base,'publish',side_effect=fail),self.assertRaises(OSError):op.deploy()
        recover=self.recover(op);receipt=recover.recover('RELEASE')
        self.assertEqual(receipt['state'],'COMMITTED');self.assertIsNone(self.control()['active'])
        self.assertFalse(self.base.path('backups/.pe73-delivery-pe73-current-baseline.json').exists())
        self.assertTrue(any(p.name.startswith('archived-') for p in self.base.path(op.d.TX).iterdir()))


if __name__=='__main__':unittest.main()
