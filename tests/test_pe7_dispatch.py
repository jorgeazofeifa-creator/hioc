"""B01..B12 deterministic real-file/native-lock dispatch fixtures."""
import copy
import hashlib
from pathlib import Path
import tempfile
import threading
import unittest
import uuid
from unittest.mock import patch
from hioc import assets
from hioc.asset_policy import PolicyStore, PolicyService
from hioc.availability import evaluate
from hioc.availability_contract import PolicyError, digest
from hioc.availability_incidents import EngineState, Dispatcher, empty_state, apply_evaluation, restart, summary, displayed
import test_pe7_evaluation as fixtures
import test_assets_schema as old


class Transport:
    deadline_aware = True
    automatic_retries = False
    offline_queue = False
    def __init__(self, callback=lambda: None): self.calls = []; self.callback = callback
    def send_once(self, event, *, deadline, timeout):
        self.calls.append((copy.deepcopy(event), deadline, timeout))
        self.callback()
        return 'TRANSPORT_ACCEPTED'


class DispatchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name); self.seconds = 0
        self.store = PolicyStore(self.home, lock_path=self.home/'assets.lock')
        self.store.timestamp = self.clock
        self.store.ensure_directories()
        self.store.inventory_context = lambda _: ('available', set())
        raw = assets.serialize_store(old.store({old.ID: old.record()}))
        self.store.store_path.write_bytes(raw)
        self.service = PolicyService(self.store, lambda _: 'strong')
        self.service.migrate(hashlib.sha256(raw).hexdigest(), writers_stopped=True)
        self.set_policy(True)
        self.engine = EngineState(self.home/'cases.json', self.home/'incident.lock')
        with self.engine.transaction():
            self.engine.initialize_explicitly()
            state = self.engine.read()
            self.epoch = state['process_epoch']
            policy = self.policy()
            first = evaluate(policy, 'strong', fixtures.profile(), [fixtures.observation(-15)], None, fixtures.at(-15))
            evaluation = evaluate(policy, 'strong', fixtures.profile(), [fixtures.observation(0)], first['state'], self.clock())
            state = apply_evaluation(state, policy, evaluation)
            self.event_id = next(iter(state['outbox']))
            self.engine.write(state)
        self.dispatch = Dispatcher(self.service, self.engine, self.clock, self.epoch, lambda: True)
        self.transport = Transport()

    def clock(self): return fixtures.at(self.seconds)
    def policy(self): return self.service.get_policy(old.ID)['policy']
    def set_policy(self, expected):
        store = self.store.load_store(); record = store['assets'][old.ID]
        self.service.mutate_policy('update', dict(asset_id=old.ID, store_epoch=store['store_epoch'],
            expected_store_revision=store['store_revision'], expected_revision=record['revision'],
            operation_id=uuid.uuid4().hex, fields={'expected_availability': expected}),
            'issuer', 'actor', lambda: True)
    def event(self):
        with self.engine.transaction(): return self.engine.read()['outbox'][self.event_id]
    def submit(self): return self.dispatch.submit(self.dispatch.claim(self.event_id), self.transport)

    def test_B01_off_commits_first_denies_new_grant(self):
        self.set_policy(False)
        with self.assertRaises(PolicyError): self.dispatch.authorize(self.event_id)
        self.assertEqual(self.transport.calls, [])

    def test_B02_committed_pre_off_grant_retains_one_bounded_attempt(self):
        grant = self.dispatch.authorize(self.event_id)
        self.set_policy(False)
        self.assertEqual(self.submit(), 'TRANSPORT_ACCEPTED')
        self.assertEqual(len(self.transport.calls), 1)
        self.assertEqual(grant['not_after'], fixtures.at(5))
        self.assertIs(self.policy()['expected_availability'], False)

    def test_B03_contention_serializes_at_guarded_fsync(self):
        at_commit, release, off_started, off_finished = (threading.Event() for _ in range(4))
        errors, grants = [], []
        def barrier(name):
            if name == 'before_authorization_commit':
                at_commit.set()
                if not release.wait(5): raise RuntimeError('fixture barrier timed out')
        self.dispatch.barrier = barrier
        def authorize():
            try: grants.append(self.dispatch.authorize(self.event_id))
            except Exception as error: errors.append(error)
        def disable():
            off_started.set()
            try: self.set_policy(False)
            except Exception as error: errors.append(error)
            finally: off_finished.set()
        authorizer = threading.Thread(target=authorize); authorizer.start()
        self.assertTrue(at_commit.wait(5))
        writer = threading.Thread(target=disable); writer.start()
        self.assertTrue(off_started.wait(5))
        # Barriers, not relative sleep timing, select authorization-first ordering.
        self.assertFalse(off_finished.is_set())
        release.set(); authorizer.join(5); writer.join(5)
        self.assertFalse(authorizer.is_alive() or writer.is_alive())
        self.assertEqual(errors, []); self.assertEqual(len(grants), 1)
        self.assertIs(self.policy()['expected_availability'], False)
        self.assertEqual(self.submit(), 'TRANSPORT_ACCEPTED')

    def test_B04_off_while_transport_in_flight_is_not_false_recovery(self):
        self.dispatch.authorize(self.event_id)
        self.transport.callback = lambda: self.set_policy(False)
        self.assertEqual(self.submit(), 'TRANSPORT_ACCEPTED')
        self.assertIs(self.policy()['expected_availability'], False)
        self.assertEqual(self.event()['event']['event_kind'], 'OUTAGE_STARTED')

    def test_B05_off_between_authorization_and_submission_expires(self):
        self.dispatch.authorize(self.event_id)
        claimed = self.dispatch.claim(self.event_id)
        self.set_policy(False); self.seconds = 6
        self.assertEqual(self.dispatch.submit(claimed, self.transport), 'EXPIRED')
        self.assertEqual(self.transport.calls, [])

    def test_B06_old_ungranted_event_cannot_be_retried_after_off(self):
        self.set_policy(False)
        for _ in range(2):
            with self.assertRaises(PolicyError): self.dispatch.authorize(self.event_id)
        self.assertEqual(self.transport.calls, [])

    def test_B07_reenable_preserves_episode_and_cancelled_event(self):
        self.set_policy(False)
        policy = self.policy()
        with self.engine.transaction():
            state = self.engine.read()
            result = evaluate(policy, 'strong', fixtures.profile(), [], None, self.clock())
            state = apply_evaluation(state, policy, result)
            self.engine.write(state)
        self.set_policy(True)
        policy = self.policy()
        with self.engine.transaction():
            state = self.engine.read()
            result = evaluate(policy, 'strong', fixtures.profile(), [], None, self.clock())
            updated = apply_evaluation(state, policy, result)
            case = next(iter(updated['cases'].values()))
            self.assertEqual(case['episode'], 1); self.assertEqual(case['lifecycle'], 'active')
            self.assertEqual(updated['outbox'][self.event_id]['state'], 'CANCELLED')
        with self.assertRaises(PolicyError): self.dispatch.authorize(self.event_id)

    def test_B08_duplicate_claim_and_copied_submission_denied(self):
        self.dispatch.authorize(self.event_id)
        claimed = self.dispatch.claim(self.event_id)
        with self.assertRaises(PolicyError): self.dispatch.claim(self.event_id)
        self.dispatch.submit(claimed, self.transport)
        with self.assertRaises(PolicyError): self.dispatch.submit(claimed, self.transport)
        self.assertEqual(len(self.transport.calls), 1)

    def test_B09_missing_revision_fails_closed(self):
        current = self.store.load_store(); del current['assets'][old.ID]['revision']
        with patch.object(self.store, 'load_store', return_value=current):
            with self.assertRaises((PolicyError, KeyError)): self.dispatch.authorize(self.event_id)
        self.assertEqual(self.transport.calls, [])

    def test_B10_failed_policy_read_never_uses_cached_on(self):
        self.policy()
        with patch.object(self.store, 'load_store', side_effect=PolicyError('COMMIT_UNKNOWN', uncertain=True)):
            with self.assertRaises(PolicyError): self.dispatch.authorize(self.event_id)
        self.assertEqual(self.transport.calls, [])

    def test_B11_restart_invalidates_prior_grants_and_inflight_is_unknown(self):
        self.dispatch.authorize(self.event_id)
        with self.engine.transaction():
            state = restart(self.engine.read()); self.engine.write(state)
        with self.assertRaises(PolicyError): self.dispatch.claim(self.event_id)
        self.assertEqual(self.event()['state'], 'EXPIRED')
        state = empty_state()
        original = self.event(); original['state'] = original['grant']['state'] = 'IN_FLIGHT'
        state['outbox'][self.event_id] = original
        self.assertEqual(restart(state)['outbox'][self.event_id]['state'], 'DELIVERY_UNKNOWN')

    def test_B12_suppression_history_and_unrelated_legacy_preserved(self):
        original = {'id': 'legacy-ups', 'status': 'active', 'severity': 'critical', 'history': ['original']}
        with self.engine.transaction(): state = self.engine.read()
        projection = summary(state, self.clock(), fixtures.at(100))
        self.assertEqual(displayed(original, projection), original)
        self.set_policy(False)
        policy = self.policy()
        with self.engine.transaction():
            result = evaluate(policy, 'strong', fixtures.profile(), [], None, self.clock())
            updated = apply_evaluation(state, policy, result)
        case = next(iter(updated['cases'].values()))
        self.assertEqual(case['suppression_reason'], 'OPERATOR_DISABLED')
        self.assertEqual(case['lifecycle'], 'active'); self.assertIsNone(case['resolved_at'])

    def test_restore_epoch_invalidates_previously_authorized_claim(self):
        self.dispatch.authorize(self.event_id)
        current = self.store.load_store(); current['store_epoch'] = uuid.uuid4().hex
        self.store.write_store(current)
        with self.assertRaises(PolicyError): self.dispatch.claim(self.event_id)

    def test_no_network_under_locks_and_no_transport_retry_on_unknown(self):
        self.dispatch.authorize(self.event_id)
        def check():
            self.assertFalse(self.engine.held)
            with assets.AssetLock(self.store.lock_path, shared=False): pass
            raise TimeoutError('private transport detail')
        self.transport.callback = check
        claimed = self.dispatch.claim(self.event_id)
        self.assertEqual(self.dispatch.submit(claimed, self.transport), 'DELIVERY_UNKNOWN')
        with self.assertRaises(PolicyError): self.dispatch.submit(claimed, self.transport)
        self.assertEqual(len(self.transport.calls), 1)


if __name__ == '__main__': unittest.main()
