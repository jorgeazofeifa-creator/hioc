"""Faults/crash states through the real one-shot F executor and immutable journal."""
import copy, unittest
from unittest import mock
from tools import hioc_pe4_action_f as F
from tests.test_pe4_action_f_runtime import Memory, run, COMMIT, bindings, directory

class RecoveryTests(unittest.TestCase):
    def test_before_and_after_every_intent_confirmation_boundary(self):
        events=['PREPARED']+[op+'_'+phase for op in F.OPERATIONS for phase in ('INTENT','CONFIRMED')]+['POST_VERIFIED','RESULT','RESULT_REFERENCE','COMMITTED']
        for event in events:
            for when in ('before','after'):
                backend=Memory('write-'+when+':'+event)
                with self.subTest(event=event,when=when):
                    rc,out=run(backend)
                    self.assertEqual(rc,1);self.assertEqual(out['RESULT'],'FAIL')
                    self.assertEqual(out['RECOVERY_REQUIRED'],'TRUE')
                    self.assertEqual(out['ROLLBACK_RECOMMENDED'],'FALSE')
                    self.assertNotIn('COMPLETE',out['PUBLICATION_STATE'])
                    self.assertNotIn('private',str(out))
                    self.assertEqual(len([c for c in backend.calls if c=='write-'+when+':'+event]),1)
                    # A new invocation never adopts or retries these records.
                    mutations=set(backend.mutations)
                    rc,again=run(backend)
                    self.assertEqual(rc,1);self.assertEqual(again['ERROR_CODE'],'UNRESOLVED_TRANSACTION')
                    self.assertEqual(backend.mutations,mutations)
    def test_before_after_each_mutation_and_fsync_confirmation(self):
        for op in F.OPERATIONS:
            for phase in ('mutate-before:','mutate-after:','confirm-before:','confirm-after:'):
                backend=Memory(phase+op)
                with self.subTest(op=op,phase=phase):
                    rc,out=run(backend)
                    self.assertEqual(rc,1);self.assertEqual(out['RECOVERY_REQUIRED'],'TRUE')
                    self.assertEqual(out['ROLLBACK_RECOMMENDED'],'FALSE')
                    if phase!='mutate-before:':self.assertEqual(out['PUBLICATION_STATE'],'UNCERTAIN')
                    self.assertEqual(backend.calls.count(phase+op),1)
    def test_failures_before_allocation_have_no_publication_or_recovery(self):
        for point in ('preflight','revalidate'):
            rc,out=run(Memory(point))
            self.assertEqual(rc,1);self.assertEqual(out['PUBLICATION_STATE'],'NONE')
            self.assertEqual(out['RECOVERY_REQUIRED'],'FALSE');self.assertEqual(out['TRANSACTION_DIR'],'NONE')
    def test_allocation_failure_retains_attempt_locator(self):
        rc,out=run(Memory('allocate'))
        self.assertEqual(rc,1);self.assertIn('/transactions/f-',out['TRANSACTION_DIR'].replace('\\','/'))
        self.assertEqual(out['EVIDENCE_STATE'],'NOT_CREATED');self.assertEqual(out['EVIDENCE_DIR'],'NONE')
    def test_result_partial_write_not_confirmed(self):
        rc,out=run(Memory('write-after:RESULT'))
        self.assertEqual(rc,1);self.assertEqual(out['EVIDENCE_STATE'],'UNCONFIRMED')
        self.assertEqual(out['EVIDENCE_DIR'],'NONE')
    def test_result_reference_completion_and_close_failures_never_pass(self):
        for point in ('write-after:RESULT_REFERENCE','write-after:COMMITTED','read:result.json','names','close','postverify'):
            with self.subTest(point=point):
                rc,out=run(Memory(point))
                self.assertEqual(rc,1);self.assertEqual(out['RESULT'],'FAIL')
                self.assertEqual(out['RECOVERY_REQUIRED'],'TRUE');self.assertEqual(out['ROLLBACK_RECOMMENDED'],'FALSE')
    def test_changed_chain_or_result_is_rejected_after_commit(self):
        class Corrupt(Memory):
            def read(self,name):
                raw=super().read(name)
                if 'write-after:COMMITTED' in self.calls and name=='0000.json':return raw+b' '
                return raw
        rc,out=run(Corrupt());self.assertEqual(rc,1);self.assertEqual(out['RECOVERY_REQUIRED'],'TRUE')
    def test_no_replace_errors_no_retry_no_overwrite(self):
        for code in ('CONFLICT','UNAVAILABLE','IO_FAILED'):
            class Conflict(Memory):
                def mutate(self,op,tid):
                    self.calls.append('attempt:'+op)
                    raise F.Failure(code,op)
            backend=Conflict();rc,out=run(backend)
            self.assertEqual(rc,1);self.assertEqual(out['ERROR_CODE'],code)
            self.assertEqual(backend.calls.count('attempt:CLIENT'),1)
            self.assertFalse(backend.mutations)
    def test_native_no_replace_collision_and_unsupported_errno(self):
        for err,code in ((F.errno.EEXIST,'CONFLICT'),(F.errno.ENOSYS,'UNAVAILABLE'),(F.errno.EXDEV,'UNAVAILABLE'),(F.errno.EIO,'IO_FAILED')):
            fn=mock.Mock(return_value=-1)
            with mock.patch.object(F.H.ctypes,'CDLL',return_value=type('Lib',(),{'renameat2':fn})()),mock.patch.object(F.H.ctypes,'get_errno',return_value=err),self.assertRaises(F.H.Failure) as caught:
                F.H.noreplace(directory(),'.source','final')
            self.assertEqual(caught.exception.code,code);fn.assert_called_once()
            self.assertEqual(fn.call_args.args[-1],1)
    def test_final_collision_and_unresolved_preflight_never_allocate(self):
        for code in ('CONFLICT','UNRESOLVED_TRANSACTION','LOCK_BUSY'):
            class Rejected(Memory):
                def preflight(self,commit):raise F.Failure(code,'PRECONDITIONS')
            backend=Rejected();rc,out=run(backend)
            self.assertEqual(rc,1);self.assertFalse(backend.mutations);self.assertFalse(backend.allocated)
    def test_forbidden_resume_cleanup_rollback_and_probes_are_absent(self):
        source=(F.H.REPOSITORY/'tools/hioc_pe4_action_f.py').read_text()
        for fragment in ('os.unlink(', 'os.rmdir(', 'os.replace(', 'shutil.', 'CAPABILITY_PROBE',
                         'exact_distribution_set(', 'import websockets', 'site.main(', 'site.addsitedir(',
                         'hioc-pe4-runtime-rollback.py','hioc-pe4-runtime-preflight.py'):
            self.assertNotIn(fragment,source)

if __name__=='__main__':unittest.main()
