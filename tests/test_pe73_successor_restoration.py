"""Real temporary transactions; explicit synthetic POSIX/native admission seams.

Production journal/claim bytes are unavailable. Only test constants are replaced
by genuine SHA-256 digests of canonical fixture bytes; no production digest is
manufactured or mapped onto an invented capture.
"""
import ast
import contextlib
import copy
import hashlib
import importlib.util
import inspect
import io
import json
import os
from pathlib import Path
import unittest
from unittest.mock import patch
import test_pe73_successor_delivery as prior

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('restoration_under_test', ROOT/'tools/pe73_successor_restoration.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)


class RestorationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        prior.SuccessorTests.setUpClass()

    def setUp(self):
        self.case = prior.SuccessorTests('test_exact_thirteen_source_pins_and_three_deltas')
        self.case.setUp()
        self.addCleanup(self.case.tearDown)
        self.w, self.d, self.fs, self.base, self.ops = self.case.w, self.case.d, self.case.fs, self.case.base, self.case.ops
        self.p, self.c = self.case.p, self.case.c
        original_grant = self.case.grant
        def grant(action):
            value = original_grant(action)
            value['operator'] = 'UID1000_jazofv1'
            return value
        self.case.grant = grant
        self.case.establish()
        def stop(point):
            if point == 'INSTALLED:' + self.d.ORDER[4]:
                raise RuntimeError('SYNTHETIC_INITIAL_STOP')
        self.c.fault = stop
        with self.assertRaises(RuntimeError):
            self.case.runtime('COMMIT')
        self.c.fault = lambda _: None
        self.base.publications.clear()
        self.base.write_new('backups/.pe73-delivery.lock', b'')
        self.original = self.case.original
        self.co = self.w.MaintenanceCoordinator(self.p, lambda: self.case.source)
        self.prepared, _ = r._dependencies()
        raw = self.d.canonical({'version': 1, 'authority': self.prepared.AUTHORITY,
            'journal_anchor': self.prepared.JOURNAL_SHA, 'pid': 1234,
            'boot_id': 'HISTORICAL_BOOT', 'session': '1'*32, 'nonce': '2'*32,
            'actions': list(self.prepared.CONTINUATION), 'admission_reference': 'PE73_'+'a'*64,
            'authorization_sha256': 'a'*64})
        self.base.write_new(r.CLAIM, raw)
        self.claim_snapshot = self.fs.snapshot(r.CLAIM, 0o600)
        self.source = {'commit': 'a'*40, 'tree': 'b'*40}
        self.tx_owner = (1000, 1000, 0o700)
        self.stack = contextlib.ExitStack()
        self.addCleanup(self.stack.close)
        self.stack.enter_context(patch.object(r, 'JOURNAL_SHA', r.sha(self.fs.read(r.TX+'/journal.json'))))
        self.stack.enter_context(patch.object(r, 'CLAIM_SHA', r.sha(raw)))
        self.stack.enter_context(patch.object(r, 'ORIGINAL_CRON_SHA', r.sha(self.original)))
        self.stack.enter_context(patch.object(r, 'REDUCED_CRON_SHA', r.sha(self.p.reduced)))
        self.stack.enter_context(patch.object(r, '_source', side_effect=lambda _: dict(self.source)))
        self.stack.enter_context(patch.object(self.prepared, '_entries', side_effect=self.entries))
        self.recorder = r._Recorder(self.ops)
        self.ops.processes = self.recorder
        self.initial = self.c._journal()
        self.baseline = copy.deepcopy(self.initial['baseline'])

    def entries(self, fs, d):
        r.require(self.tx_owner == (1000, 1000, 0o700), 'UNSAFE_SYNTHETIC_TRANSACTION')
        path = self.base.path(r.TX)
        info = path.stat()
        return {x.name for x in path.iterdir()}, dict(st_dev=info.st_dev, st_ino=info.st_ino,
            st_uid=1000, st_gid=1000, mode=0o700, type='DIRECTORY')

    def binding(self):
        return self.w, self.case.m, self.co, self.prepared, dict(self.source), self.recorder

    def admit(self):
        return r._admit(self.w, self.co, self.prepared)

    def sequence(self):
        return r._Sequence(self.w, self.co, self.prepared, dict(self.source), self.recorder)

    def run_sequence(self):
        with patch.object(r, '_binding', side_effect=self.binding):
            return r.run_controlled_restoration()

    def inventory(self):
        return {p.relative_to(self.base.root).as_posix(): p.read_bytes()
                for p in self.base.root.rglob('*') if p.is_file()}

    def fresh(self):
        self.stack.close()
        self.case.tearDown()
        # Cleanup callbacks belong to the previous stack/case; replace their
        # bound callbacks before creating another independent synthetic fixture.
        self._cleanups.clear()
        self.setUp()

    def anchor_changed_journal(self, change):
        value = self.c._journal()
        change(value)
        raw = self.d.canonical(value)
        self.base.path(r.TX+'/journal.json').write_bytes(raw)
        self.stack.enter_context(patch.object(r, 'JOURNAL_SHA', r.sha(raw)))

    def test_read_only_admission_exact_five_prefix_thirteen_buffers(self):
        before = self.inventory()
        result = self.admit()
        self.assertEqual(len(self.initial['installed']), 5)
        self.assertEqual(result['journal_sha256'], r.JOURNAL_SHA)
        self.assertEqual(before, self.inventory())
        self.assertFalse(self.base.path(r.INTENT).exists())

    def test_public_readiness_has_no_native_authority_or_writes(self):
        before = self.inventory()
        with patch.object(r, '_binding', side_effect=self.binding), patch.object(self.fs, 'mutex', side_effect=AssertionError('LOCK')):
            result = r.inspect_restoration()
        self.assertFalse(result['native_execution_authorized'])
        self.assertFalse(result['production_mutated'])
        self.assertEqual(result['transaction_entries'], 29)
        self.assertEqual(before, self.inventory())

    def test_fixed_complete_sequence_restores_one_preserves_twelve(self):
        result = self.run_sequence()
        self.assertEqual(result['RESULT'], 'PASS_CONTROLLED_RESTORATION', result)
        self.assertEqual(self.base.publications, [self.d.ORDER[4]])
        value = self.c._journal()
        self.assertEqual((value['state'], value['window']['phase']), ('ROLLED_BACK', 'RELEASED'))
        self.assertEqual(set(value['restored']), set(self.d.ORDER[:5]))
        self.assertEqual(self.ops.raw, self.original)
        for target in self.d.ORDER:
            self.assertEqual(self.fs.read(target, self.d.MODES[target]), self.case.old[target])
            if target != self.d.ORDER[4]:
                self.assertEqual(self.fs.snapshot(target, self.d.MODES[target]), self.baseline[target])
        self.assertEqual(self.fs.snapshot(r.CLAIM, 0o600), self.claim_snapshot)
        intent = self.d.parsed(self.fs.read(r.INTENT))
        self.assertEqual(intent['actions'], list(r.ACTIONS))
        self.assertEqual(intent['source'], self.source)
        self.assertEqual(intent['journal_anchor'], r.JOURNAL_SHA)
        self.assertEqual(intent['claim_snapshot'], self.claim_snapshot)
        self.assertEqual(intent['admission_reference'], 'PE73_' + intent['authorization_sha256'])
        self.assertIsNone(self.ops._admission)
        self.assertEqual(len(self.ops.calls), 2)  # Original setup EXCLUDE + one RESTORE.

    def test_no_prepare_preserve_exclude_establish_commit_during_restoration(self):
        actions = []
        original = self.co.execute
        def execute(action, authorization):
            actions.append(action)
            return original(action, authorization)
        with patch.object(self.co, 'execute', side_effect=execute), patch.object(self.c, 'prepare', side_effect=AssertionError('PREPARE')), \
                patch.object(self.c, 'commit', side_effect=AssertionError('COMMIT')):
            result = self.run_sequence()
        self.assertEqual(result['RESULT'], 'PASS_CONTROLLED_RESTORATION', result)
        self.assertEqual(tuple(actions), r.ACTIONS)

    def test_all_twenty_six_buffer_corruptions_rejected(self):
        for prefix in ('backup-', 'stage-'):
            for i in range(13):
                path = self.base.path(r.TX+'/'+prefix+str(i))
                raw = path.read_bytes()
                path.write_bytes(raw+b'X')
                try:
                    with self.subTest(prefix=prefix, index=i), self.assertRaises(Exception):
                        self.admit()
                finally:
                    path.write_bytes(raw)
        self.assertFalse(self.base.path(r.INTENT).exists())

    def test_old_five_path_configuration_refused_before_mutation(self):
        old, _ = prior.s.load(successor=False)
        self.d.PRIOR = old.d.PRIOR
        with self.assertRaisesRegex(ValueError, 'SUCCESSOR_CONFIGURATION_REQUIRED'):
            self.admit()
        self.assertFalse(self.base.path(r.INTENT).exists())

    def test_journal_digest_claim_digest_and_claim_identity_drift(self):
        for path in (r.TX+'/journal.json', r.CLAIM):
            raw = self.base.path(path).read_bytes()
            self.base.path(path).write_bytes(raw+b' ')
            with self.subTest(path=path), self.assertRaises(Exception):
                self.admit()
            self.base.path(path).write_bytes(raw)

    def test_claim_closed_schema_and_original_authority_are_mandatory(self):
        raw = self.fs.read(r.CLAIM)
        for key, value in [('extra', True), ('actions', ['ROLLBACK']), ('journal_anchor', 'b'*64),
                           ('version', True), ('session', 'not-a-uuid'), ('admission_reference', 'BAD')]:
            item = self.d.parsed(raw)
            item[key] = value
            changed = self.d.canonical(item)
            self.base.path(r.CLAIM).write_bytes(changed)
            with patch.object(r, 'CLAIM_SHA', r.sha(changed)), self.subTest(key=key), self.assertRaises(Exception):
                self.admit()
        self.base.path(r.CLAIM).write_bytes(raw)

    def test_invalid_core_phase_pending_prefix_restoration_and_authority(self):
        changes = [lambda v: v.update(state='COMMITTED'), lambda v: v.update(pending=self.d.ORDER[5]),
            lambda v: v['installed'].pop(self.d.ORDER[0]),
            lambda v: v.update(restored={self.d.ORDER[4]:v['installed'][self.d.ORDER[4]]}),
            lambda v: v.update(rollback_authorization='UNEXPECTED_ROLLBACK'),
            lambda v: v['window'].update(phase='EXCLUDED')]
        for i, change in enumerate(changes):
            if i:
                self.fresh()
            self.anchor_changed_journal(change)
            with self.subTest(case=i), self.assertRaises(Exception):
                self.admit()
            self.assertFalse(self.base.path(r.INTENT).exists())

    def test_unexpected_tx_files_existing_intent_and_runtime_temporaries(self):
        for name in ('journal-next', 'unexpected', 'controlled-restoration-intent.json'):
            path = self.base.path(r.TX+'/'+name)
            path.write_bytes(b'partial')
            with self.subTest(name=name), self.assertRaises(ValueError):
                self.admit()
            path.unlink()
        for target in self.d.ORDER:
            path = self.base.path(str(Path(target).parent / ('.pe73-delivery-'+Path(target).name)))
            path.write_bytes(b'pending')
            with self.subTest(target=target), self.assertRaisesRegex(ValueError, 'TEMPORARY'):
                self.admit()
            path.unlink()

    def test_runtime_and_source_drift(self):
        path = self.base.path(self.d.ORDER[4])
        path.write_bytes(path.read_bytes()+b'X')
        with self.assertRaises(Exception):
            self.admit()
        self.fresh()
        self.co.source_reader = lambda: dict(self.case.source, **{self.d.ORDER[0]:b'BAD'})
        with self.assertRaises(Exception):
            self.admit()

    def test_transaction_owner_group_mode_and_existing_mutex(self):
        for identity in ((0,1000,0o700), (1000,0,0o700), (1000,1000,0o755)):
            self.tx_owner = identity
            with self.subTest(identity=identity), self.assertRaises(ValueError):
                self.admit()
        self.tx_owner = (1000,1000,0o700)
        self.base.path('backups/.pe73-delivery.lock').unlink()
        with self.assertRaisesRegex(ValueError, 'MUTEX_MISSING'):
            self.admit()

    def test_file_owner_group_mode_hardlinks_and_types(self):
        target = r.TX+'/stage-0'
        for mapping, bad in ((self.base.uids,0), (self.base.gids,0), (self.base.modes,0o644)):
            original = mapping.get(target)
            mapping[target] = bad
            with self.assertRaises(Exception):
                self.admit()
            if original is None:
                mapping.pop(target)
            else:
                mapping[target] = original
        link = self.base.root/'extra-hardlink'
        os.link(self.base.path(target), link)
        try:
            with self.assertRaises(Exception):
                self.admit()
        finally:
            link.unlink()
        original = self.base.path(target).read_bytes()
        self.base.path(target).unlink()
        self.base.path(target).mkdir()
        with self.assertRaises(Exception):
            self.admit()
        self.base.path(target).rmdir()
        self.base.path(target).write_bytes(original)

    def test_read_only_planning_and_native_attach_admission_before_intent(self):
        before = self.inventory()
        sequence = self.sequence()
        self.assertEqual(before, self.inventory())
        fs = self.c.fs
        with self.assertRaisesRegex(ValueError, 'ATTACH_ADMISSION_REQUIRED'):
            with fs.mutex():
                pass
        self.assertFalse(self.base.path(r.INTENT).exists())
        self.assertFalse(sequence.stopped)

    def test_intent_is_first_write_inside_mutex_and_admission(self):
        events = []
        original = self.base.write_new
        def write(path, raw, mode=0o600):
            events.append((path, getattr(self.ops, '_admission', None)))
            return original(path, raw, mode)
        with patch.object(self.base, 'write_new', side_effect=write):
            result = self.run_sequence()
        self.assertEqual(result['RESULT'], 'PASS_CONTROLLED_RESTORATION', result)
        self.assertEqual(events[0][0], r.INTENT)
        self.assertIs(type(events[0][1]), self.w._NativeAdmission)
        self.assertEqual(events[0][1].action, 'ATTACH')

    def test_partial_intent_or_race_stops_without_journal_change_or_retry(self):
        for partial in (False, True):
            if partial:
                self.fresh()
            original = self.base.write_new
            def write(path, raw, mode=0o600):
                if path == r.INTENT:
                    original(path, b'partial' if partial else raw, mode)
                    raise OSError('PRIVATE_SENTINEL')
                return original(path, raw, mode)
            initial = self.fs.read(r.TX+'/journal.json')
            with patch.object(self.base, 'write_new', side_effect=write):
                result = self.run_sequence()
            self.assertTrue(result['RESULT'].startswith('FAIL_'))
            self.assertEqual(self.fs.read(r.TX+'/journal.json'), initial)
            self.assertTrue(self.base.path(r.INTENT).exists())
            self.assertEqual(self.run_sequence()['failed_action'], 'READ_ONLY_ADMISSION')
            self.assertNotIn('PRIVATE_SENTINEL', json.dumps(result))

    def test_competing_mutex_is_refused_without_intent(self):
        with self.base.mutex():
            result = self.run_sequence()
        self.assertTrue(result['RESULT'].startswith('FAIL_'))
        self.assertFalse(self.base.path(r.INTENT).exists())

    def test_completed_attempt_cannot_run_again(self):
        self.assertTrue(self.run_sequence()['RESULT'].startswith('PASS_'))
        before = self.inventory()
        result = self.run_sequence()
        self.assertTrue(result['RESULT'].startswith('FAIL_'))
        self.assertEqual(before, self.inventory())

    def test_active_incomplete_stale_and_process_exception(self):
        for kind in ('active', 'incomplete', 'stale', 'exception'):
            if kind != 'active':
                self.fresh()
            if kind == 'active':
                self.ops.active = [{'pid':7,'start_ticks':2,'command_sha256':'a'*64}]
            elif kind == 'incomplete':
                self.ops.complete = False
            elif kind == 'stale':
                delegate = self.recorder.delegate
                self.recorder.delegate = lambda: dict(delegate(), observed_at=-100)
            else:
                def fail():
                    raise OSError('PRIVATE_PROCESS_SENTINEL')
                self.recorder.delegate = fail
            result = self.run_sequence()
            self.assertTrue(result['RESULT'].startswith('FAIL_'), result)
            self.assertFalse(self.base.path(r.INTENT).exists())
            self.assertNotIn('PRIVATE_PROCESS_SENTINEL', json.dumps(result))

    def test_boot_session_expiry_and_context_changes_refuse(self):
        for kind in ('boot','session','expiry','source','scheduler','journal','claim','history'):
            if kind != 'boot':
                self.fresh()
            sequence = self.sequence()
            if kind == 'boot': self.ops.boot_id = 'CHANGED_BOOT'
            if kind == 'session': self.p.session = 'changed'
            if kind == 'expiry': self.ops.clock += 3601
            if kind == 'source': self.source['commit'] = 'c'*40
            if kind == 'scheduler': self.ops.raw += b'# changed\n'
            if kind == 'journal': self.base.path(r.TX+'/journal.json').write_bytes(b'changed')
            if kind == 'claim': self.base.path(r.CLAIM).write_bytes(b'changed')
            if kind == 'history': self.base.path(prior.s.HISTORICAL_TX+'/journal.json').write_bytes(b'changed')
            with self.subTest(kind=kind), self.assertRaises(Exception):
                sequence.perform_next()
            self.assertTrue(sequence.stopped)
            self.assertFalse(self.base.path(r.INTENT).exists())
            if kind == 'history':
                self.base.path(prior.s.HISTORICAL_TX+'/journal.json').write_bytes(b'HISTORICAL_FIXTURE_NOT_A_NATIVE_VALIDATION')

    def assert_interruption(self, point):
        def fault(actual):
            if actual == point:
                raise OSError('PRIVATE_INTERRUPTION')
        self.c.fault = fault
        result = self.run_sequence()
        self.assertTrue(result['RESULT'].startswith('FAIL_'), (point,result))
        self.assertTrue(self.base.path(r.INTENT).exists())
        self.assertEqual(self.fs.snapshot(r.CLAIM,0o600),self.claim_snapshot)
        self.assertNotIn('PRIVATE_INTERRUPTION',json.dumps(result))
        before = self.inventory()
        self.assertTrue(self.run_sequence()['RESULT'].startswith('FAIL_'))
        self.assertEqual(before,self.inventory())

    def test_drain_interruption_is_separate_from_attach(self):
        count = [0]
        def fault(point):
            if point == 'WINDOW:INSTALLATION_UNCERTAIN':
                count[0] += 1
                if count[0] == 2:
                    raise OSError('DRAIN_INTERRUPTION')
        self.c.fault = fault
        result = self.run_sequence()
        self.assertEqual(result['failed_action'],'DRAIN')
        self.assertEqual(self.base.publications,[])

    def test_consumer_arrives_after_protocol_restore_stops_remaining_rollback(self):
        original = self.base.publish
        def publish(*args):
            value = original(*args)
            self.ops.active = [{'pid':17,'start_ticks':2,'command_sha256':'a'*64}]
            return value
        with patch.object(self.base,'publish',side_effect=publish):
            result = self.run_sequence()
        self.assertEqual(result['failed_action'],'ROLLBACK')
        self.assertEqual(result['primary_failure'],'KNOWN_CONSUMERS_NOT_DRAINED')
        self.assertEqual(self.c._journal()['state'],'ROLLING_BACK')
        self.assertEqual(len(self.c._journal()['restored']),1)
        self.assertEqual(self.ops.raw,self.p.reduced)
        self.assertEqual(result['process_guard']['actual_guard_observation']['known_active'][0]['pid'],17)

    def test_publication_and_journal_write_failures_preserve_uncertainty(self):
        self.base.fail = lambda p: p == 'PUBLISH:'+self.d.ORDER[4]
        result = self.run_sequence()
        self.assertEqual(result['failed_action'],'ROLLBACK')
        self.assertEqual(self.c._journal()['pending'],self.d.ORDER[4])
        self.assertEqual(self.ops.raw,self.p.reduced)
        self.fresh()
        self.base.fail = lambda p: p == r.TX+'/journal-next'
        result = self.run_sequence()
        self.assertEqual(result['failed_action'],'ATTACH')
        self.assertTrue(self.base.path(r.INTENT).exists())

    def test_baseline_verification_failure_prevents_release_authorization(self):
        original = r._restored
        with patch.object(r,'_restored',side_effect=ValueError('SYNTHETIC_BASELINE_VERIFICATION')):
            result = self.run_sequence()
        self.assertEqual(result['failed_action'],'ROLLBACK')
        self.assertEqual(self.c._journal()['window']['phase'],'RESTORATION_VERIFIED')
        self.assertEqual(self.ops.raw,self.p.reduced)

    def test_scheduler_timeout_lost_ack_and_unavailable_readback(self):
        for kind in ('timeout','lost_ack','unknown'):
            if kind != 'timeout':
                self.fresh()
            attempts = []
            def install(raw, expected):
                attempts.append(raw)
                if kind != 'timeout':
                    self.ops.raw = raw
                if kind == 'unknown':
                    self.ops.scheduler = lambda: (_ for _ in ()).throw(OSError('PRIVATE_READBACK'))
                raise TimeoutError('PRIVATE_SCHEDULER')
            self.ops.install_scheduler = install
            result = self.run_sequence()
            self.assertEqual(len(attempts),1)
            self.assertEqual(result['failed_action'],'RESTORE_SCHEDULER')
            self.assertEqual(self.c._journal()['window']['phase'],'RESTORE_UNCERTAIN')
            self.assertEqual(result['scheduler_observation_after_failure']['state'],
                {'timeout':'REDUCED','lost_ack':'ORIGINAL','unknown':'UNKNOWN'}[kind])
            self.assertNotIn('PRIVATE_',json.dumps(result))

    def test_consumer_after_scheduler_restoration_refuses_release_without_reexclusion(self):
        original = self.ops.install_scheduler
        def install(*args):
            original(*args)
            self.ops.active = [{'pid':19,'start_ticks':2,'command_sha256':'a'*64}]
        self.ops.install_scheduler = install
        result = self.run_sequence()
        self.assertEqual(result['failed_action'],'RELEASE')
        self.assertEqual(self.c._journal()['window']['phase'],'SCHEDULER_RESTORED')
        self.assertEqual(self.ops.raw,self.original)
        self.assertEqual(len(self.ops.calls),2)
        self.assertEqual(result['scheduler_observation_after_failure']['state'],'ORIGINAL')

    def test_intent_claim_buffer_history_and_source_drift_between_operations(self):
        for kind in ('intent','claim','backup','stage','history','source'):
            if kind != 'intent':
                self.fresh()
            seq = self.sequence()
            seq.perform_next()
            path = {'intent':r.INTENT,'claim':r.CLAIM,'backup':r.TX+'/backup-12',
                'stage':r.TX+'/stage-12','history':prior.s.HISTORICAL_TX+'/journal.json'}.get(kind)
            if path:
                self.base.path(path).write_bytes(b'drift')
            else:
                self.source['tree']='c'*40
            with self.subTest(kind=kind),self.assertRaises(Exception):
                seq.perform_next()
            self.assertTrue(seq.stopped)
            self.assertEqual(self.base.publications,[])
            if kind=='history':
                self.base.path(path).write_bytes(b'HISTORICAL_FIXTURE_NOT_A_NATIVE_VALIDATION')

    def test_primary_secondary_and_scheduler_failures_are_independent_sanitized(self):
        with patch.object(self.c,'_journal',side_effect=OSError('PRIVATE_JOURNAL')):
            result=r._failure(self.co,self.w,self.recorder,ValueError('PRIMARY_FAILURE'),'ROLLBACK',True)
        self.assertEqual(result['primary_failure'],'PRIMARY_FAILURE')
        self.assertEqual(result['inspection_failure'],'RESTORATION_STOPPED_OR_UNCERTAIN')
        self.assertEqual(result['scheduler_observation_after_failure']['state'],'REDUCED')
        self.assertNotIn('PRIVATE_JOURNAL',json.dumps(result))

    def test_actual_recorder_delegates_once_retains_object_and_exception(self):
        value=self.recorder.delegate()
        with patch.object(self.recorder,'delegate',return_value=value) as call:
            self.assertIs(self.recorder(),value)
            call.assert_called_once_with()
        error=OSError('PRIVATE_EXCEPTION')
        with patch.object(self.recorder,'delegate',side_effect=error) as call:
            try:
                self.recorder()
            except OSError as caught:
                self.assertIs(caught,error)
            else:
                self.fail('exception swallowed')
            call.assert_called_once_with()
        self.assertNotIn('PRIVATE_EXCEPTION',json.dumps(self.recorder.receipt(self.w)))

    def test_dependency_source_pins_and_historical_algorithms_unchanged(self):
        p,adapter=r._dependencies()
        self.assertEqual(r.sha((ROOT/'tools/pe73_successor_prepared_recovery.py').read_bytes()),r.PREPARED_SHA)
        h,m=adapter.load(successor=False)
        self.assertEqual(r.sha((ROOT/'tools/hioc-pe73-pi3-delivery.py').read_bytes()),m['controller_sha256'])
        self.assertEqual(r.sha((ROOT/'tools/pe73_maintenance_window.py').read_bytes()),m['provider_sha256'])
        self.assertEqual(inspect.getsource(h.d.Controller.rollback),inspect.getsource(self.d.Controller.rollback))
        self.assertIs(self.w.WindowController.rollback.__globals__['d'],self.d)

    def test_public_cli_only_read_only_and_entry_has_no_external_parameters(self):
        self.assertEqual(list(inspect.signature(r.run_controlled_restoration).parameters),[])
        self.assertEqual(list(inspect.signature(r.inspect_restoration).parameters),[])
        tree=ast.parse((ROOT/'tools/pe73_successor_restoration.py').read_bytes())
        main=[n for n in tree.body if isinstance(n,ast.If) and '__main__' in ast.unparse(n.test)][0]
        self.assertNotIn('run_controlled_restoration()',ast.unparse(main))
        self.assertIn("['inspect-restoration']",ast.unparse(main))

# Each interruption is a separate unittest result, not a hidden subtest total.
_INTERRUPTION_POINTS = ['WINDOW:INSTALLATION_UNCERTAIN', 'ROLLING_BACK', 'ROLLED_BACK',
    'WINDOW:RELEASE_AUTHORIZED', 'WINDOW:RESTORE_UNCERTAIN',
    'WINDOW:SCHEDULER_RESTORED', 'WINDOW:RELEASED']
_INTERRUPTION_POINTS += [prefix+path for path in prior.s.load()[0].d.ORDER[:5]
                        for prefix in ('ROLLBACK_INTENT:', 'RESTORED:')]
for _number, _point in enumerate(_INTERRUPTION_POINTS):
    def _case(self, point=_point):
        self.assert_interruption(point)
    setattr(RestorationTests, 'test_interruption_%02d' % _number, _case)


class SealedNativeContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p, cls.a = r._dependencies()
        cls.h, cls.m = cls.a.load(successor=False)

    def test_native_security_rejects_acl_unavailable_acl_symlink_and_hardlink(self):
        import errno
        import stat
        import types
        fs = object.__new__(self.h.d.NativeFS)
        info = types.SimpleNamespace(st_mode=stat.S_IFREG|0o600,st_uid=1000,st_gid=1000,st_nlink=1)
        missing = OSError(errno.ENODATA,'SYNTHETIC_NO_ACL')
        with patch.object(os,'getxattr',side_effect=missing,create=True):
            fs.security(info,False,0o600,fd=99)
        for outcome in (b'ACL', OSError(errno.EACCES,'PRIVATE_ACL')):
            with patch.object(os,'getxattr',side_effect=outcome if isinstance(outcome,Exception) else None,
                              return_value=outcome,create=True),self.assertRaises(self.h.d.Failure):
                fs.security(info,False,0o600,fd=99)
        for mode, links in ((stat.S_IFLNK|0o600,1),(stat.S_IFREG|0o600,2),(stat.S_IFREG|0o666,1)):
            info.st_mode,info.st_nlink=mode,links
            with self.subTest(mode=mode,links=links),self.assertRaises(self.h.d.Failure):
                fs.security(info,False,0o600)

    def test_original_directory_open_rejects_symlink_without_following(self):
        import errno
        fs=object.__new__(self.h.d.NativeFS)
        fs.root=Path('/home/jazofv1/hioc')
        # The first absolute-root acquisition is refused: no actual filesystem
        # access, and the native algorithm demonstrably requests O_NOFOLLOW.
        with patch.object(self.h.d.os,'O_NOFOLLOW',0x20000,create=True),patch.object(self.h.d.os,'O_DIRECTORY',0x10000,create=True),\
                patch.object(self.h.d.os,'O_CLOEXEC',0x80000,create=True),\
                patch.object(self.h.d.os,'open',side_effect=OSError(errno.ELOOP,'SYMLINK')) as opened:
            with self.assertRaises(OSError):
                with fs.directory('backups'):
                    self.fail('entered unsafe directory')
            self.assertTrue(opened.call_args.args[1]&0x20000)

    def test_source_root_provenance_is_not_an_arbitrary_checkout_allowlist(self):
        fake=type('Source',(),{'_source':staticmethod(lambda:{'commit':'a'*40,'tree':'b'*40})})
        with patch.object(r.subprocess,'run',return_value=type('Result',(),{'returncode':1})()):
            with self.assertRaisesRegex(ValueError,'SOURCE_ANCESTRY'):
                r._source(fake)
        with patch.object(r.subprocess,'run',return_value=type('Result',(),{'returncode':0})()) as called:
            self.assertEqual(r._source(fake)['commit'],'a'*40)
            self.assertIn(r.SOURCE_ANCESTOR,called.call_args.args[0])
            self.assertEqual(called.call_args.kwargs['cwd'],r.ROOT)

    def test_strict_historical_journal_does_not_require_obsolete_live_inodes(self):
        import tempfile
        spec=importlib.util.spec_from_file_location('restoration_original_fixture',ROOT/'tests/test_pe73_pi3_delivery.py')
        f=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(f)
        h,_=self.a.load(successor=False)
        f.d=h.d
        with tempfile.TemporaryDirectory(prefix='pe73-restoration-history-') as temp:
            fs=f.FixtureFS(Path(temp))
            source={x['path']:prior.git('show',h.d.RELEASE+':'+x['path']) for x in h.d.MANIFEST}
            class Ops:
                boot_id='HISTORICAL_SYNTHETIC_BOOT'
                def now(self):return 1000
                def live_gate(self):pass
                def scheduler(self):return self.raw
                def processes(self):return dict(boot_id=self.boot_id,observed_at=1000,inspection_complete=True,
                    known_active=[],universal_exclusion=False,limitations=['SYNTHETIC'])
                def install_scheduler(self,raw,expected):
                    h.require(r.sha(self.raw)==expected,'SCHEDULER_DRIFT')
                    self.raw=raw
            ops=Ops()
            ops.raw=('\n'.join(h.d.CRON)+'\n7 * * * * unrelated-job\n').encode()
            inventory={x:'EXCLUDE' if x in h.d.CRON else 'PRESERVE' for x in ops.raw.decode().splitlines()}
            provider=h.WindowConsumers(ops,ops.raw,list(h.d.CRON),inventory)
            c=provider.bind(fs,source)
            c.prepare('HISTORICAL_SYNTHETIC_PREPARE',r.sha(h.d.canonical(h.d.preflight(fs,source,provider))))
            count=[0]
            def grant(action):
                count[0]+=1
                return dict(action=action,reference='HISTORICAL_GRANT_'+str(count[0]),
                    journal_sha256=r.sha(h.d.canonical(c._journal())),scheduler_sha256=r.sha(ops.raw),
                    operator='UID1000_jazofv1',session=provider.session,boot_id=ops.boot_id,
                    expires_at=1600,exclusive_responsibility=True,risks_acknowledged=list(h.RISKS))
            for action in ('PRESERVE','EXCLUDE','DRAIN','ESTABLISH'):
                provider.progress(action,grant(action))
            g=grant('COMMIT')
            provider.authorize_runtime(g)
            c.commit(g['reference'],g['journal_sha256'])
            for action in ('AUTHORIZE_RELEASE','RESTORE_SCHEDULER','RELEASE'):
                provider.progress(action,grant(action))
            before=r._history(self.a,h,source,fs)
            target=h.d.ORDER[4]
            fs.path(target).write_bytes(fs.path(target).read_bytes()+b'changed')
            self.assertFalse(c.inspect()['live_state_established'])
            self.assertEqual(r._history(self.a,h,source,fs),before)
            fs.path(h.d.TX+'/journal.json').write_bytes(b'INVALID')
            with self.assertRaises(Exception):
                r._history(self.a,h,source,fs)


if __name__ == '__main__':
    unittest.main()
