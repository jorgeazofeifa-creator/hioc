"""Anchored recovery fixtures; historical digest is explicitly mocked, never reconstructed."""
import contextlib
import copy
import hashlib
import importlib.util
import inspect
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import test_pe73_successor_delivery as prior

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('prepared_recovery_tests',ROOT/'tools/pe73_successor_prepared_recovery.py')
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)

class PreparedRecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):prior.SuccessorTests.setUpClass()
    def setUp(self):self.make_fixture()
    def make_fixture(self):
        self.case=prior.SuccessorTests('test_exact_thirteen_source_pins_and_three_deltas');self.case.setUp();self.case.prepare()
        self.w,self.d,self.fs,self.base,self.ops=self.case.w,self.case.d,self.case.fs,self.case.base,self.case.ops
        self.base.write_new('backups/.pe73-delivery.lock',b'')
        inventory={x:'EXCLUDE' for x in self.d.CRON};inventory['7 * * * * unrelated-job']='PRESERVE'
        provider=self.w.WindowConsumers(self.ops,self.case.original,list(self.d.CRON),inventory)
        self.c=provider.bind(self.fs,self.case.source)
        self.coordinator=self.w.MaintenanceCoordinator(provider,lambda:self.case.source)
        self.anchor_raw=self.fs.read(r.TX+'/journal.json')
        self.real_sha=r.sha
        # Only this canonical fixture journal is mapped to the operator-supplied
        # immutable digest. All source/backup/stage/claim hashing remains real.
        self.sha_patch=patch.object(r,'sha',side_effect=lambda b:r.JOURNAL_SHA if b==self.anchor_raw else self.real_sha(b));self.sha_patch.start()
        self.core_sha_patch=patch.object(self.d,'sha',side_effect=lambda b:r.JOURNAL_SHA if b==self.anchor_raw else self.real_sha(b));self.core_sha_patch.start()
        self.entries_patch=patch.object(r,'_entries',side_effect=self.entries);self.entries_patch.start()
        self.tx_uid,self.tx_gid,self.tx_mode=1000,1000,0o700
    def close_fixture(self):
        self.entries_patch.stop();self.core_sha_patch.stop();self.sha_patch.stop();self.case.tearDown()
    def tearDown(self):self.close_fixture()
    def entries(self,fs,d):
        r.require(fs.transaction_present(),'RECOVERY_TRANSACTION_MISSING')
        r.require((self.tx_uid,self.tx_gid,self.tx_mode)==(1000,1000,0o700),'RECOVERY_TRANSACTION_OWNER_OR_MODE')
        p=self.base.path(r.TX);info=p.stat()
        return {x.name for x in p.iterdir()},{'st_dev':info.st_dev,'st_ino':info.st_ino,'st_uid':1000,'st_gid':1000,'mode':0o700,'type':'DIRECTORY'}
    def proof(self):return r._validate(self.w,self.coordinator)
    def binding(self):return self.w,self.case.m,self.coordinator,self.proof(),{'commit':'SYNTHETIC','tree':'SYNTHETIC'}
    def run_recovery(self):
        with patch.object(r,'_native_binding',side_effect=self.binding),contextlib.redirect_stdout(io.StringIO()) as out:
            result=r.run_prepared_recovery()
        return result,out.getvalue()
    def alter_journal(self,change):
        value=self.c._journal();change(value);raw=self.d.canonical(value)
        self.base.path(r.TX+'/journal.json').write_bytes(raw);self.anchor_raw=raw
    def test_exact_anchor_validation_is_read_only(self):
        before={p.name:p.read_bytes() for p in self.base.path(r.TX).iterdir()}
        proof=self.proof();self.assertEqual(proof['journal_sha256'],r.JOURNAL_SHA);self.assertEqual(proof['entry_count'],27)
        self.assertEqual(before,{p.name:p.read_bytes() for p in self.base.path(r.TX).iterdir()});self.assertEqual(self.ops.calls,[])
    def test_real_unmatched_digest_is_rejected(self):
        with patch.object(r,'sha',side_effect=self.real_sha),self.assertRaisesRegex(ValueError,'RECOVERY_JOURNAL_ANCHOR_MISMATCH'):self.proof()
    def test_incorrect_journal_hash_is_rejected(self):
        self.base.path(r.TX+'/journal.json').write_bytes(self.anchor_raw+b' ')
        with self.assertRaisesRegex(ValueError,'RECOVERY_JOURNAL_ANCHOR_MISMATCH'):self.proof()
    def test_each_staged_payload_and_each_backup_is_checked(self):
        for kind in ['stage-','backup-']:
            for i in range(13):
                p=self.base.path(r.TX+'/'+kind+str(i));original=p.read_bytes();p.write_bytes(original+b'X')
                try:
                    with self.subTest(kind=kind,index=i),self.assertRaisesRegex(ValueError,'RECOVERY_(STAGE|BACKUP)_DRIFT'):self.proof()
                finally:p.write_bytes(original)
    def test_runtime_drift_is_rejected(self):
        p=self.base.path(self.d.ORDER[0]);p.write_bytes(p.read_bytes()+b'X')
        with self.assertRaises(Exception):self.proof()
    def test_scheduler_drift_is_rejected(self):
        self.ops.raw+=b'9 * * * * unauthorized\n'
        with self.assertRaises(self.d.Failure):self.proof()
    def test_active_and_incomplete_processes_are_rejected(self):
        self.ops.active=[{'pid':3,'start_ticks':10,'command_sha256':'a'*64}]
        with self.assertRaisesRegex(ValueError,'KNOWN_CONSUMERS_NOT_DRAINED'):self.proof()
        self.ops.active=[];self.ops.complete=False
        with self.assertRaisesRegex(ValueError,'KNOWN_CONSUMERS_NOT_DRAINED'):self.proof()
    def test_wrong_phase_pending_installation_restoration_and_authority_rejected(self):
        original=self.anchor_raw
        changes=[lambda v:v.update(state='COMMITTED'),lambda v:v.update(pending=self.d.ORDER[0]),
                 lambda v:v.update(installed={self.d.ORDER[0]:v['baseline'][self.d.ORDER[0]]}),
                 lambda v:v.update(restored={self.d.ORDER[0]:v['baseline'][self.d.ORDER[0]]}),
                 lambda v:v.update(commit_authorization='UNEXPECTED_COMMIT'),
                 lambda v:v.update(rollback_authorization='UNEXPECTED_ROLLBACK'),
                 lambda v:v.update(window={'phase':'EXCLUDED'})]
        for change in changes:
            self.base.path(r.TX+'/journal.json').write_bytes(original);self.anchor_raw=original
            self.alter_journal(change)
            with self.subTest(change=changes.index(change)),self.assertRaises(Exception):self.proof()
        self.base.path(r.TX+'/journal.json').write_bytes(original);self.anchor_raw=original
    def test_unexpected_artifacts_and_prior_claim_are_rejected(self):
        for name in ['journal-next','window-crontab-original','unexpected','prepared-recovery-claim.json']:
            p=self.base.path(r.TX+'/'+name);p.write_bytes(b'X')
            try:
                with self.subTest(name=name),self.assertRaisesRegex(ValueError,'RECOVERY_UNEXPECTED_ARTIFACTS'):self.proof()
            finally:p.unlink()
    def test_transaction_owner_and_mode_are_required(self):
        for uid,gid,mode in [(0,1000,0o700),(1000,0,0o700),(1000,1000,0o755)]:
            self.tx_uid,self.tx_gid,self.tx_mode=uid,gid,mode
            with self.assertRaises(ValueError):self.proof()
        self.tx_uid,self.tx_gid,self.tx_mode=1000,1000,0o700
    def test_all_transaction_file_owners_modes_and_hardlinks_are_checked(self):
        import os
        target=r.TX+'/stage-0'
        self.base.modes[target]=0o644
        with self.assertRaises(self.d.Failure):self.proof()
        self.base.modes[target]=0o600;self.base.uids[target]=0
        with self.assertRaises(self.d.Failure):self.proof()
        self.base.uids[target]=1000
        link=self.base.root/'hardlink-test';os.link(self.base.path(target),link)
        try:
            with self.assertRaises(self.d.Failure):self.proof()
        finally:link.unlink()
    def test_existing_shared_mutex_is_required(self):
        self.base.path('backups/.pe73-delivery.lock').unlink()
        with self.assertRaisesRegex(ValueError,'RECOVERY_EXISTING_MUTEX_MISSING'):self.proof()
    def test_read_only_public_receipt_grants_no_execution(self):
        before={p.name:p.read_bytes() for p in self.base.path(r.TX).iterdir()}
        with patch.object(r,'_native_binding',side_effect=self.binding):result=r.inspect_prepared_recovery()
        self.assertFalse(result['native_execution_authorized']);self.assertFalse(result['production_mutated'])
        self.assertEqual(before,{p.name:p.read_bytes() for p in self.base.path(r.TX).iterdir()})
    def test_correct_continuation_never_prepares_or_fabricates_window(self):
        before={p.name:self.base.snapshot(r.TX+'/'+p.name,0o600) for p in self.base.path(r.TX).iterdir()}
        unchanged={p:self.fs.snapshot(p,self.d.MODES[p]) for p in self.case.source if p not in self.case.m['changed_paths']}
        actions=[];real=self.coordinator.execute
        def tracked(action,authorization):actions.append(action);return real(action,authorization)
        with patch.object(self.coordinator,'execute',side_effect=tracked),patch.object(self.c,'prepare',side_effect=AssertionError('REPREPARE_FORBIDDEN')):
            result,out=self.run_recovery()
        self.assertTrue(result['RESULT'].startswith('PASS_'));self.assertEqual(tuple(actions),r.CONTINUATION)
        self.assertEqual(actions[0],'PRESERVE');self.assertNotIn('ATTACH',actions)
        self.assertEqual(len(self.base.publications),3);self.assertEqual(self.ops.raw,self.case.original)
        self.assertTrue(self.base.path(r.CLAIM).exists())
        for path,b in unchanged.items():self.assertEqual(self.fs.snapshot(path,self.d.MODES[path]),b)
        for name,b in before.items():
            if name!='journal.json':self.assertEqual(self.base.snapshot(r.TX+'/'+name,0o600),b)
        self.assertNotIn('PRIVATE',out)
    def test_second_invocation_never_silently_resumes(self):
        result,_=self.run_recovery();self.assertTrue(result['RESULT'].startswith('PASS_'))
        count=len(self.base.publications);calls=len(self.ops.calls)
        result,_=self.run_recovery();self.assertTrue(result['RESULT'].startswith('FAIL_STOP'))
        self.assertEqual(len(self.base.publications),count);self.assertEqual(len(self.ops.calls),calls)
    def test_claim_race_refuses_without_overwriting(self):
        original=self.base.write_new
        def write(path,raw,mode=0o600):
            if path==r.CLAIM and not self.base.path(path).exists():original(path,b'OTHER_ATTEMPT',mode)
            return original(path,raw,mode)
        with patch.object(self.base,'write_new',side_effect=write):result,_=self.run_recovery()
        self.assertTrue(result['RESULT'].startswith('FAIL_STOP'));self.assertEqual(self.base.read(r.CLAIM),b'OTHER_ATTEMPT')
        self.assertEqual(self.ops.calls,[]);self.assertEqual(self.base.publications,[])
    def test_claim_identity_drift_blocks_progress(self):
        engine=r._begin(self.w,self.coordinator)
        engine.perform_next()
        self.base.path(r.CLAIM).write_bytes(b'CHANGED')
        with self.assertRaises(ValueError):engine.perform_next()
        self.assertEqual(self.ops.calls,[]);self.assertEqual(self.base.publications,[])
    def test_process_change_after_admission_blocks_before_preserve(self):
        engine=r._begin(self.w,self.coordinator);self.ops.complete=False
        with self.assertRaises(self.d.Failure):engine.perform_next()
        self.assertIsNone(self.c._journal().get('window'));self.assertEqual(self.ops.calls,[])
        self.assertFalse(self.base.path(r.CLAIM).exists())
        with self.assertRaises(ValueError):r._begin(self.w,self.coordinator)
    def test_native_entry_points_accept_no_operator_parameters(self):
        for f in [r.inspect_prepared_recovery,r.run_prepared_recovery]:
            self.assertEqual(len(inspect.signature(f).parameters),0)
            with self.assertRaises(TypeError):f({'approved':True})
    def test_normal_and_historical_excluded_entry_behavior_preserved(self):
        with self.assertRaises(self.d.Failure):self.w._ApprovedSequence(self.coordinator)
        fresh,_=prior.s.load()
        self.assertEqual(fresh.DEPLOYMENT_SEQUENCE,('PREPARE',)+r.CONTINUATION)
        self.assertEqual(fresh.EXCLUDED_RECOVERY_JOURNAL_SHA256,'b899a8fa79bde3c6619d6abd8217d88833c414823e7888358ed7a043b766600f')
        with self.assertRaises(fresh.d.Failure):fresh.validate_excluded_resume(self.coordinator)
    def test_interruption_boundaries_stop_and_retain_new_durable_state(self):
        target=next(p for p in self.d.ORDER if p in self.case.m['changed_paths'])
        points=['WINDOW:PRESERVATION_UNCERTAIN','WINDOW:PRESERVED','WINDOW:EXCLUSION_UNCERTAIN','WINDOW:EXCLUDED',
                'WINDOW:DRAINED','WINDOW:ESTABLISHED','COMMITTING','INTENT:'+target,'AFTER_PUBLICATION:'+target,
                'COMMITTED','WINDOW:RELEASE_AUTHORIZED','WINDOW:RESTORE_UNCERTAIN','WINDOW:SCHEDULER_RESTORED','WINDOW:RELEASED']
        for index,point in enumerate(points):
            if index:self.close_fixture();self.make_fixture()
            def fault(current):
                if current==point:raise OSError('PRIVATE_PRIMARY_EXCEPTION')
            self.c.fault=fault
            result,out=self.run_recovery()
            with self.subTest(point=point):
                self.assertTrue(result['RESULT'].startswith('FAIL_STOP'));self.assertTrue(self.base.path(r.CLAIM).exists())
                self.assertFalse(result['automatic_scheduler_restoration']);self.assertFalse(result['automatic_release'])
                self.assertNotIn('PRIVATE_PRIMARY_EXCEPTION',json.dumps(result)+out)
                counts=(len(self.ops.calls),len(self.base.publications));self.run_recovery()
                self.assertEqual(counts,(len(self.ops.calls),len(self.base.publications)))
    def test_primary_and_inspection_failure_are_separate_and_sanitized(self):
        real=self.c._journal;failed=[False]
        def journal():
            if failed[0]:raise OSError('PRIVATE_INSPECTION_EXCEPTION')
            return real()
        def fault(point):
            if point=='WINDOW:PRESERVED':failed[0]=True;raise OSError('PRIVATE_PRIMARY_EXCEPTION')
        self.c.fault=fault
        with patch.object(self.c,'_journal',side_effect=journal):result,out=self.run_recovery()
        self.assertIsNotNone(result['primary_failure']);self.assertIsNotNone(result['inspection_failure'])
        self.assertNotIn('PRIVATE_',json.dumps(result)+out)
    def test_diagnostics_churn_does_not_waive_incomplete_or_active_checks(self):
        real=self.ops.processes;counter=[0]
        def processes():
            counter[0]+=1;v=real();v['limitations']=['UNCLASSIFIED_PID_'+str(counter[0]),'CACHED_MODULES_UNKNOWN'];return v
        with patch.object(self.ops,'processes',side_effect=processes):result,_=self.run_recovery()
        self.assertTrue(result['RESULT'].startswith('PASS_'));self.assertFalse(result['universal_exclusion'])

    def test_entry_construction_is_read_only_and_claim_requires_native_admission(self):
        before={p.name:p.read_bytes() for p in self.base.path(r.TX).iterdir()}
        r._begin(self.w,self.coordinator)
        self.assertEqual(before,{p.name:p.read_bytes() for p in self.base.path(r.TX).iterdir()})
        with self.assertRaises(ValueError):
            with self.c.fs.mutex():pass
        self.assertFalse(self.base.path(r.CLAIM).exists())
    def test_claim_records_original_real_admission_structure(self):
        engine=r._begin(self.w,self.coordinator);engine.perform_next()
        value=self.d.parsed(self.base.read(r.CLAIM))
        self.assertEqual(value['journal_anchor'],r.JOURNAL_SHA)
        self.assertTrue(value['admission_reference'].startswith('PE73_'))
        self.assertEqual(len(value['authorization_sha256']),64)
        self.assertEqual(value['actions'],list(r.CONTINUATION))

if __name__=='__main__':unittest.main()
