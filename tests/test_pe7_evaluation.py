"""Qualified-source fixtures with explicit synthetic timings, never production policy."""
import copy
from datetime import timedelta
import unittest
import uuid
from hioc import availability as a
from hioc.availability_contract import PolicyError, digest, timestamp, time_text

ID = 'dev_0123456789abcdef'
TS = '2026-10-21T00:00:00.000000Z'
EPOCH = '1a1416eefec8448a898fdb27a8409a43'


def at(seconds):
    return time_text(timestamp(TS)+timedelta(seconds=seconds))


def profile():
    return dict(schema_version='1.0', profile_id='synthetic_only', revision=1,
        enabled_sources=['synthetic_connectivity'], source_definitions={'synthetic_connectivity': dict(
            source_id='synthetic_connectivity', kind='ha', expected_report_seconds=10, allowed_jitter_seconds=2,
            max_age_seconds=20, positive_meanings=['connected'], negative_meanings=['disconnected'],
            physical_device_authority=True, mapping_revision=1, mapping_sha256='a'*64)},
        evaluation_interval_seconds=5, negative_confirmations=2, recovery_confirmations=2,
        grace_seconds=12, reminder_interval_seconds=None)


def policy(expected=True, revision=1):
    return dict(asset_id=ID, store_epoch=EPOCH, revision=revision, expected_availability=expected,
                infrastructure_device=None, infrastructure_type=None)


def observation(seconds=0, kind='NEGATIVE', *, source='synthetic_connectivity', epoch=EPOCH):
    definition = profile()['source_definitions']['synthetic_connectivity']
    return dict(schema_version='1.0', source_id=source, source_kind='ha', asset_id=ID, device_id=ID,
        source_epoch=epoch, sample_id=digest([epoch, source, seconds, kind]), observed_at=at(seconds),
        collected_at=at(seconds), collection_status='SUCCESS', completeness='COMPLETE', evidence_kind=kind,
        scope='DEVICE', authority_ref=digest([source, 1, definition['mapping_sha256']]),
        valid_until=at(seconds+20), reason_code='SYNTHETIC_ONLY', source_sha256=digest([seconds, kind]))


class EvaluationTests(unittest.TestCase):
    def evaluate(self, seconds, kind='NEGATIVE', prior=None, **kwargs):
        return a.evaluate(policy(), 'strong', profile(), [observation(seconds, kind)], prior, at(seconds), **kwargs)

    def test_count_and_grace_are_both_required(self):
        first = self.evaluate(0)
        self.assertEqual(first['availability_state'], 'DEGRADED')
        second = self.evaluate(10, prior=first['state'])
        self.assertEqual(second['state']['negative_count'], 2)
        self.assertEqual(second['availability_state'], 'DEGRADED')
        # Elapsed grace with the same still-fresh report does not add a sample.
        third = a.evaluate(policy(), 'strong', profile(), [observation(10)], second['state'], at(12))
        self.assertEqual(third['state']['negative_count'], 2)
        self.assertEqual(third['availability_state'], 'OFFLINE')

    def test_repeated_snapshot_never_confirms(self):
        state = None
        for second in (0, 5, 10, 15):
            result = a.evaluate(policy(), 'strong', profile(), [observation()], state, at(second))
            state = result['state']
            self.assertEqual(state['negative_count'], 1)
            self.assertNotEqual(result['availability_state'], 'OFFLINE')

    def test_positive_recovery_needs_distinct_reports(self):
        first = self.evaluate(0, 'POSITIVE', case_open=True)
        self.assertEqual(first['availability_state'], 'RECOVERING')
        repeated = a.evaluate(policy(), 'strong', profile(), [observation(0, 'POSITIVE')], first['state'], at(5), case_open=True)
        self.assertEqual(repeated['availability_state'], 'RECOVERING')
        second = self.evaluate(10, 'POSITIVE', repeated['state'], case_open=True)
        self.assertEqual(second['availability_state'], 'AVAILABLE')

    def test_missing_failed_incomplete_unknown_do_not_outage_or_recover(self):
        for change in ({'collection_status': 'FAILED'}, {'collection_status': 'UNAVAILABLE'},
                       {'completeness': 'INCOMPLETE'}, {'evidence_kind': 'UNKNOWN'}):
            row = observation(); row.update(change)
            result = a.evaluate(policy(), 'strong', profile(), [row], None, at(0), case_open=True)
            self.assertEqual(result['availability_state'], 'UNKNOWN')
        self.assertEqual(a.evaluate(policy(), 'strong', profile(), [], None, TS)['availability_state'], 'UNKNOWN')

    def test_exclusive_freshness_boundary(self):
        result = a.evaluate(policy(), 'strong', profile(), [observation()], None, at(20))
        self.assertEqual(result['availability_state'], 'STALE')

    def test_clock_future_reversal_and_out_of_order(self):
        self.assertEqual(a.evaluate(policy(), 'strong', profile(), [observation(1)], None, TS)['availability_state'], 'UNKNOWN')
        first = self.evaluate(10)
        self.assertEqual(a.evaluate(policy(), 'strong', profile(), [observation()], first['state'], at(11))['reason_code'], 'SOURCE_OUT_OF_ORDER')
        self.assertEqual(a.evaluate(policy(), 'strong', profile(), [observation()], first['state'], TS)['reason_code'], 'CLOCK_REVERSED')

    def test_source_restart_resets_confirmation(self):
        first = self.evaluate(0)
        row = observation(15, epoch=uuid.uuid4().hex)
        result = a.evaluate(policy(), 'strong', profile(), [row], first['state'], at(15))
        self.assertEqual(result['state']['negative_count'], 1)
        self.assertNotEqual(result['availability_state'], 'OFFLINE')

    def test_infrastructure_edits_rebind_without_evidence_reset(self):
        first = self.evaluate(0)
        current = policy(revision=2); current.update(infrastructure_device=True, infrastructure_type='router_gateway')
        second = a.evaluate(current, 'strong', profile(), [observation(15)], first['state'], at(15))
        self.assertEqual(second['availability_state'], 'OFFLINE')
        self.assertEqual(second['state']['applied_policy_revision'], 2)

    def test_off_and_null_are_not_monitored_but_distinct_policy(self):
        for expected in (False, None):
            result = a.evaluate(policy(expected), 'strong', profile(), [observation()], None, TS)
            self.assertEqual(result['availability_state'], 'NOT_MONITORED')
            self.assertIs(policy(expected)['expected_availability'], expected)

    def test_unsafe_identity_and_missing_profile_are_unknown(self):
        for identity in ('weak', 'conflicted', 'orphan', 'absent'):
            self.assertEqual(a.evaluate(policy(), identity, profile(), [observation()], None, TS)['reason_code'], 'UNKNOWN_IDENTITY')
        self.assertEqual(a.evaluate(policy(), 'strong', None, [], None, TS)['availability_state'], 'UNKNOWN')

    def test_entity_state_and_no_physical_authority_cannot_outage(self):
        for scope, physical in (('ENTITY', True), ('DEVICE', False)):
            p = profile(); p['source_definitions']['synthetic_connectivity']['physical_device_authority'] = physical
            row = observation(); row['scope'] = scope
            self.assertEqual(a.evaluate(policy(), 'strong', p, [row], None, TS)['availability_state'], 'DEGRADED')

    def test_fresh_physical_conflict_is_explicit(self):
        p = profile(); second = copy.deepcopy(p['source_definitions']['synthetic_connectivity'])
        second['source_id'] = 'other_connectivity'
        p['source_definitions']['other_connectivity'] = second
        p['enabled_sources'] = sorted(p['source_definitions'])
        rows = [observation(kind='POSITIVE'), observation(source='other_connectivity')]
        self.assertEqual(a.evaluate(policy(), 'strong', p, rows, None, TS)['reason_code'], 'SOURCE_CONFLICT')

    def test_closed_profile_and_observation_validation(self):
        for field, value in (('negative_confirmations', 1), ('recovery_confirmations', True),
                             ('grace_seconds', 1), ('reminder_interval_seconds', 10), ('extra', 1)):
            bad = profile(); bad[field] = value
            with self.assertRaises(PolicyError): a.validate_profile(bad)
        bad = observation(); bad['extra'] = 'private'
        with self.assertRaises(PolicyError): a.validate_observation(bad)


if __name__ == '__main__': unittest.main()
