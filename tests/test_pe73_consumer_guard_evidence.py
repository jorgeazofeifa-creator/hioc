"""Failure-time evidence uses actual sealed guards; no native operations or rescan."""
import copy
import json
import unittest
from unittest.mock import patch
import test_pe73_successor_delivery as prior
import test_pe73_successor_prepared_recovery as prepared

class GuardEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        prior.SuccessorTests.setUpClass()
    def setUp(self):
        self.case = prior.SuccessorTests('test_exact_thirteen_source_pins_and_three_deltas')
        self.case.setUp()
        self.addCleanup(self.case.tearDown)
        self.w, self.ops = self.case.w, self.case.ops
        self.co = self.w.MaintenanceCoordinator(self.case.p, lambda: self.case.source)
        self.rec = prior.s._Recorder(self.ops).install(self.w, self.co)
    def sample(self, **changes):
        v = dict(self.rec.delegate())
        v.update(changes)
        return v
    def reject(self, value, predicate):
        self.rec.delegate = lambda: value
        with self.assertRaisesRegex(self.w.d.Failure, 'KNOWN_CONSUMERS_NOT_DRAINED') as error:
            self.case.p._processes()
        receipt = self.rec.receipt(self.w)
        self.assertEqual(receipt['failed_predicate'], predicate)
        self.assertEqual(receipt, error.exception.process_guard)
        self.assertEqual(receipt['failure_stage'], 'WindowConsumers._processes')
        self.assertEqual(self.rec.calls, 1)
        self.assertEqual(self.ops.calls, [])
        self.assertFalse(self.case.base.publications)
        return receipt
    def test_active_known_consumer(self):
        v = self.sample(known_active=[dict(pid=17,start_ticks=2,command_sha256='a'*64)])
        receipt = self.reject(v,'known_consumers_absent')
        self.assertEqual(receipt['actual_guard_observation']['known_active'],v['known_active'])
    def test_incomplete_inspection(self):
        receipt = self.reject(self.sample(inspection_complete=False),'inspection_completeness')
        self.assertIsNone(receipt['evaluated_at'])  # Original conjunction short-circuited.
    def test_boot_mismatch(self):
        self.reject(self.sample(boot_id='OTHER_BOOT'),'boot_identity')
    def test_stale_observation(self):
        receipt = self.reject(self.sample(observed_at=self.ops.clock-31),'observation_freshness')
        self.assertEqual(receipt['observation_age_seconds'],31)
        self.assertEqual(receipt['evaluated_at'],self.ops.clock)
    def test_future_observation(self):
        receipt = self.reject(self.sample(observed_at=self.ops.clock+1),'observation_freshness')
        self.assertEqual(receipt['observation_age_seconds'],-1)
    def test_actual_failure_frozen_despite_later_clear_scan(self):
        value = self.sample(inspection_complete=False)
        receipt = self.reject(value,'inspection_completeness')
        value['inspection_complete'] = True
        self.rec.delegate = lambda: self.sample_clear
        self.sample_clear = dict(value)
        self.ops.processes()
        self.assertEqual(self.rec.receipt(self.w),receipt)
    def test_no_extra_scan_or_clock_call_success_returns_identical_object(self):
        value = self.sample()
        now = self.ops.now
        # Install wraps exactly existing calls, not additional diagnostics.
        with patch.object(self.rec,'delegate',return_value=value) as scan:
            with patch.object(self.ops,'now',wraps=now) as clock:
                self.assertIs(self.case.p._processes(),value)
        self.assertEqual(scan.call_count,1)
        self.assertEqual(clock.call_count,1)
        self.assertIsNone(self.rec.frozen)
    def test_sensitive_limitations_redacted_and_extra_fields_never_output(self):
        value = self.sample(inspection_complete=False,
            limitations=['UNCLASSIFIED_PID_42','SECRET_TOKEN=private', 'PRIVATE_ARGUMENT_TEXT'])
        receipt = self.reject(value,'inspection_completeness')
        raw = json.dumps(receipt)
        self.assertNotIn('private',raw)
        self.assertNotIn('PRIVATE_ARGUMENT_TEXT',raw)
        self.assertIn('UNCLASSIFIED_PID_42',raw)
        self.assertNotIn('BOOT_SYNTHETIC',raw)
    def test_untrusted_extra_process_fields_are_not_disclosed(self):
        value = self.sample(inspection_complete=False)
        value['argv'] = ['PRIVATE_CREDENTIAL']
        self.rec.delegate = lambda: value
        with self.assertRaises(self.w.d.Failure):
            self.case.p._processes()
        receipt = self.rec.receipt(self.w)
        self.assertIsNone(receipt['actual_guard_observation'])
        self.assertNotIn('PRIVATE_CREDENTIAL',json.dumps(receipt))
    def test_same_private_exception_propagates(self):
        error = OSError('PRIVATE_PROCESS_EXCEPTION')
        with patch.object(self.rec,'delegate',side_effect=error) as scan:
            try:
                self.case.p._processes()
            except OSError as caught:
                self.assertIs(caught,error)
            else:
                self.fail('exception swallowed')
        self.assertEqual(scan.call_count,1)
        self.assertNotIn('PRIVATE_PROCESS_EXCEPTION',json.dumps(self.rec.receipt(self.w)))
    def test_unclassified_limitations_do_not_reject_success(self):
        value = self.sample(limitations=['UNCLASSIFIED_PID_4','CACHED_MODULES_UNKNOWN'])
        self.rec.delegate = lambda: value
        self.assertIs(self.case.p._processes(),value)
        self.assertIsNone(self.rec.frozen)
    def test_prepared_admission_uses_same_recorder_and_exception(self):
        self.rec.delegate = lambda: self.value
        self.value = {
            'boot_id':self.ops.boot_id,'observed_at':self.ops.clock,
            'known_active':[],'inspection_complete':False,
            'limitations':[],'universal_exclusion':False}
        observation = self.ops.processes()
        with self.assertRaisesRegex(ValueError,'KNOWN_CONSUMERS_NOT_DRAINED') as error:
            prepared.r._record_guard(self.w,self.co,'prepared._validate', lambda: prepared.r.require(
                observation['inspection_complete'] and not observation['known_active'],
                'KNOWN_CONSUMERS_NOT_DRAINED'))
        self.assertEqual(error.exception.process_guard['failed_predicate'],'inspection_completeness')
        self.assertEqual(self.rec.calls,1)
    def test_context_freshness_rejection_retains_actual_sample(self):
        value=self.sample(observed_at=self.ops.clock-31)
        self.rec.delegate=lambda:value
        with self.assertRaisesRegex(self.w.d.Failure,'PROCESS_EVIDENCE_STALE') as error:
            self.co.context('PREPARE')
        self.assertEqual(error.exception.process_guard['failed_predicate'],'observation_freshness')
        self.assertEqual(error.exception.process_guard['action'],'PREPARE')
        self.assertEqual(self.rec.calls,1)
    def test_publication_guard_failure_evidence_survives_later_inspection(self):
        self.case.establish()
        original = self.case.base.publish
        def publish(*args):
            result=original(*args)
            self.ops.active=[dict(pid=27,start_ticks=3,command_sha256='b'*64)]
            return result
        with patch.object(self.case.base,'publish',side_effect=publish):
            with self.assertRaisesRegex(self.w.d.Failure,'KNOWN_CONSUMERS_NOT_DRAINED') as error:
                self.case.runtime('COMMIT')
        frozen=copy.deepcopy(error.exception.process_guard)
        self.ops.active=[]
        self.case.p.inspect()
        self.assertEqual(self.rec.receipt(self.w),frozen)
        self.assertEqual(frozen['actual_guard_observation']['known_active'][0]['pid'],27)
        self.assertEqual(set(self.case.c._journal()['installed']),set(self.w.d.ORDER[:5]))

    def test_scan_timestamp_is_not_misreported_as_guard_freshness_evaluation(self):
        def scan():
            return dict(boot_id=self.ops.boot_id, observed_at=self.ops.now(),
                inspection_complete=False, known_active=[], limitations=[], universal_exclusion=False)
        self.rec.delegate=scan
        with self.assertRaises(self.w.d.Failure):
            self.case.p._processes()
        self.assertIsNone(self.rec.receipt(self.w)['evaluated_at'])
    def test_recorder_installation_is_idempotent(self):
        again=prior.s._Recorder(self.ops).install(self.w,self.co)
        self.assertIs(again,self.rec)
        self.case.p._processes()
        self.assertEqual(self.rec.calls,1)
    def test_restoration_failure_keeps_exception_evidence_without_returned_binding(self):
        import test_pe73_successor_restoration as restoration
        value=self.sample(inspection_complete=False)
        self.rec.delegate=lambda:value
        try:
            self.case.p._processes()
        except self.w.d.Failure as error:
            receipt=restoration.r._failure(None,None,None,error,'READ_ONLY_ADMISSION',False)
        self.assertEqual(receipt['process_guard']['failed_predicate'],'inspection_completeness')
        self.assertEqual(receipt['primary_failure'],'KNOWN_CONSUMERS_NOT_DRAINED')

if __name__ == '__main__':
    unittest.main()
