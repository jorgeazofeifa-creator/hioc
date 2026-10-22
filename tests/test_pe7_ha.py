"""HA API-contract fixtures; installed HA capability remains a later P requirement."""
import asyncio
import json
import contextvars
import copy
import importlib.util
from pathlib import Path
from types import SimpleNamespace as NS
import unittest
from unittest.mock import Mock
import test_pe7_evaluation as fixtures

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('hioc_operator_fixture', ROOT/'homeassistant/custom_components/hioc_operator/__init__.py')
bridge = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(bridge)


class Connection:
    def __init__(self, user):
        self.user = user; self.refresh_token_id = 'test_token'; self.remote = '127.0.0.1'
        self.send_message = self._send
    def _send(self, _): pass
    def _connect_closed_error(self, _): pass


class HAIdentityTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.user = NS(id='test_operator', is_active=True, is_admin=True, system_generated=False)
        self.token = NS(user=self.user, token_type='normal', expire_at=200)
        async def user(_): return self.user
        self.auth = NS(async_get_user=user, async_get_refresh_token=Mock(side_effect=lambda _: self.token),
                       async_validate_refresh_token=Mock())
        self.hass = NS(auth=self.auth)
        self.context = contextvars.ContextVar('fixture_connection', default=None)
        self.connection = Connection(self.user); self.context.set(self.connection)
        self.call = NS(context=NS(user_id=self.user.id, parent_id=None, id='test_context'), data={})

    async def verify(self):
        return await bridge.verified_actor(self.hass, self.call, ['test_operator'], self.context, now=100)

    async def test_actual_context_connection_and_provider_checked(self):
        self.assertEqual(await self.verify(), ('test_operator', 'test_context'))
        self.auth.async_validate_refresh_token.assert_called_once_with(self.token, '127.0.0.1')

    async def test_null_system_deactivated_nonadmin_and_unknown_user_denied(self):
        for field, value in (('is_active', False), ('is_admin', False), ('system_generated', True)):
            original = getattr(self.user, field); setattr(self.user, field, value)
            with self.assertRaises(bridge.BridgeError): await self.verify()
            setattr(self.user, field, original)
        self.call.context.user_id = None
        with self.assertRaises(bridge.BridgeError): await self.verify()
        self.auth.async_validate_refresh_token.assert_not_called()

    async def test_rest_automation_parent_mismatched_and_closed_connections_denied(self):
        self.context.set(None)
        with self.assertRaises(bridge.BridgeError): await self.verify()
        self.context.set(self.connection); self.call.context.parent_id = 'automation'
        with self.assertRaises(bridge.BridgeError): await self.verify()
        self.call.context.parent_id = None; self.connection.user = NS(id='different')
        with self.assertRaises(bridge.BridgeError): await self.verify()
        self.connection.user = self.user; self.connection.send_message = self.connection._connect_closed_error
        with self.assertRaises(bridge.BridgeError): await self.verify()

    async def test_removed_expired_wrong_user_and_nonlogin_tokens_denied(self):
        for token in (None, NS(user=self.user, token_type='normal', expire_at=100),
                      NS(user=self.user, token_type='long_lived_access_token', expire_at=None),
                      NS(user=NS(id='other'), token_type='normal', expire_at=200)):
            self.token = token
            with self.assertRaises(bridge.BridgeError): await self.verify()

    async def test_provider_revocation_and_missing_capability_fail_closed(self):
        self.auth.async_validate_refresh_token.side_effect = RuntimeError('test provider revoked')
        with self.assertRaises(RuntimeError): await self.verify()
        del self.auth.async_validate_refresh_token
        with self.assertRaises(AttributeError): await self.verify()

    async def test_payload_cannot_forge_operator_or_private_fields(self):
        for key in ('actor_id', 'user_id', 'is_admin', 'notes', 'path', 'shell'):
            with self.assertRaises(bridge.BridgeError):
                bridge.validate_payload('get', {'asset_id':fixtures.ID, key:'forged'})


class MemoryReceipts:
    def __init__(self): self.value = None
    async def async_load(self): return copy.deepcopy(self.value)
    async def async_save(self, value): self.value = copy.deepcopy(value)


class ReceiverTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.storage = MemoryReceipts(); self.calls = []
        async def notify(value): self.calls.append(value)
        self.receiver = bridge.NotificationReceiver(self.storage, notify, lambda: True, lambda: fixtures.timestamp(fixtures.TS))
        self.event = dict(schema_version='1.0', event_id='a'*64, incident_id='b'*64, event_kind='OUTAGE_STARTED',
                          severity='warning', occurred_at=fixtures.TS, policy_revision=1, asset_id_digest='c'*64)
        self.receiver.projection = dict(schema_version='1.0', evaluated_at=fixtures.TS, valid_until=fixtures.at(100),
            status='VALID', total_case_count=1, omitted_case_count=0, cases=[dict(incident_id='b'*64,
                asset_id_digest='c'*64, episode=1, lifecycle='active', availability_state='OFFLINE',
                suppression_reason=None, severity='warning', policy_revision=1, profile_revision=1,
                detected_at=fixtures.TS, updated_at=fixtures.TS)])

    async def test_durable_dedup_survives_receiver_restart(self):
        self.assertEqual(await self.receiver.accept(self.event), 'TRANSPORT_ACCEPTED')
        fresh = bridge.NotificationReceiver(self.storage, self.receiver.notify, lambda: True,
                                             lambda: fixtures.timestamp(fixtures.TS))
        fresh.projection = self.receiver.projection
        self.assertEqual(await fresh.accept(self.event), 'DUPLICATE')
        self.assertEqual(len(self.calls), 1)

    async def test_failed_notification_remains_unknown_without_retry(self):
        async def failing(value): self.calls.append(value); raise TimeoutError('private')
        self.receiver.notify = failing
        self.assertEqual(await self.receiver.accept(self.event), 'DELIVERY_UNKNOWN')
        self.assertEqual(await self.receiver.accept(self.event), 'DUPLICATE')
        self.assertEqual(len(self.calls), 1)

    async def test_missing_expired_truncated_summary_cannot_authorize_delivery(self):
        for change in ({'omitted_case_count':1}, {'valid_until':fixtures.TS}, {'extra':'private'}):
            original = copy.deepcopy(self.receiver.projection)
            self.receiver.projection.update(change)
            with self.assertRaises(bridge.BridgeError): await self.receiver.accept(self.event)
            self.receiver.projection = original
        self.receiver.projection = None
        with self.assertRaises(bridge.BridgeError): await self.receiver.accept(self.event)
        self.assertEqual(self.calls, [])

    async def test_gate_off_and_private_extra_event_field_denied(self):
        self.receiver.enabled = lambda: False
        with self.assertRaises(bridge.BridgeError): await self.receiver.accept(self.event)
        self.receiver.enabled = lambda: True
        self.event['notes'] = 'private'
        with self.assertRaises(bridge.BridgeError): await self.receiver.accept(self.event)
        self.assertEqual(self.calls, [])


if __name__ == '__main__': unittest.main()


class ObservationRoleTests(unittest.TestCase):
    def settings(self):
        mapping=dict(source_id='synthetic_connectivity',asset_id=fixtures.ID,ha_device_id='opaque_device',
            entity_id='sensor.synthetic_connectivity',mapping_revision=1,scope='DEVICE',report_semantics_verified=True)
        profile=fixtures.profile();profile['source_definitions']['synthetic_connectivity']['mapping_sha256']=bridge.sha(mapping)
        association={'associations':[dict(hioc_device_id=fixtures.ID,status='ASSOCIATED_STRONG_MAC',association_basis='unique_mac',
            ha_device_id='opaque_device',entities=[{'entity_id':mapping['entity_id']}])]} 
        return dict(enabled=True,transport={},source_epoch=fixtures.EPOCH,profiles={fixtures.ID:profile},mappings=[mapping],
            association=association,association_sha256=bridge.sha(association),association_deadline=fixtures.at(100))

    def test_actual_allowlisted_report_time_normalizes_into_backend_contract(self):
        from hioc.availability import validate_observation, evaluate
        from hioc.availability_protocol import ObservationProtocol,ObservationTrust,sign
        from hioc.availability_contract import canonical,digest
        import uuid
        settings=self.settings();calls=[]
        def get(key):
            calls.append(key);return NS(state='connected',last_reported=fixtures.timestamp(fixtures.TS))
        rows=bridge.collect_selected_observations(get,settings,fixtures.TS)
        self.assertEqual(calls,['sensor.synthetic_connectivity']);validate_observation(rows[0])
        self.assertNotIn('sensor.synthetic_connectivity',json.dumps(rows));self.assertNotIn('connected',json.dumps(rows))
        self.assertEqual(evaluate(fixtures.policy(),'strong',settings['profiles'][fixtures.ID],rows,None,fixtures.TS)['availability_state'],'AVAILABLE')
        issuer=uuid.uuid4().hex;key=b's'*32;peer='a'*64;sink=Mock()
        trust=ObservationTrust(issuer,'observation_only',key,peer,{fixtures.ID:frozenset(['synthetic_connectivity'])},True)
        protocol=ObservationProtocol(sink,lambda *_:trust,lambda _:settings['profiles'][fixtures.ID],lambda _:'strong',lambda:fixtures.timestamp(fixtures.TS))
        payload={'observations':rows}
        assertion=dict(issuer=issuer,key_id='observation_only',audience='hioc.pe7.observation',request_id=uuid.uuid4().hex,
            issued_at=fixtures.TS,expires_at=fixtures.at(30),method='POST',path='/pe7/v1/observations',payload_sha256=digest(payload))
        envelope=sign(assertion,payload,key)
        answer=protocol.handle('/pe7/v1/observations',canonical(envelope),peer)
        self.assertEqual(answer['result'],'observations_received');sink.commit.assert_called_once_with(rows)
        self.assertEqual(protocol.handle('/pe7/v1/policy/update',canonical(envelope),peer)['result'],'error')
        assertion['request_id']=uuid.uuid4().hex;assertion['audience']='hioc.pe7.asset'
        self.assertEqual(protocol.handle('/pe7/v1/observations',canonical(sign(assertion,payload,key)),peer)['result'],'error')

    def test_membership_staleness_and_no_report_time_do_not_invent_physical_evidence(self):
        settings=self.settings(); calls=[]
        settings['association']['associations'][0]['entities']=[]
        settings['association_sha256']=bridge.sha(settings['association'])
        rows=bridge.collect_selected_observations(lambda key:calls.append(key),settings,fixtures.TS)
        self.assertEqual(calls,[]);self.assertEqual(rows[0]['evidence_kind'],'UNKNOWN')
        settings=self.settings()
        with self.assertRaises(bridge.BridgeError):bridge.collect_selected_observations(lambda _:None,settings,fixtures.at(100))
        rows=bridge.collect_selected_observations(lambda _:NS(state='connected'),settings,fixtures.TS)
        self.assertEqual(rows[0]['evidence_kind'],'UNKNOWN')

    def test_unknown_switch_state_and_ordinary_entity_negative_are_not_device_outages(self):
        settings=self.settings()
        for meaning in ('unknown','unavailable','off'):
            rows=bridge.collect_selected_observations(lambda _:NS(state=meaning,last_reported=fixtures.timestamp(fixtures.TS)),settings,fixtures.TS)
            self.assertEqual(rows[0]['evidence_kind'],'UNKNOWN')

    def _reserved_mapping_cannot_create_outage(self, meaning):
        from hioc.availability import validate_profile, evaluate
        from hioc.availability_incidents import empty_state, apply_evaluation
        for mapping_field in ('negative_meanings', 'positive_meanings'):
            with self.subTest(meaning=meaning, mapping_field=mapping_field):
                settings = self.settings()
                profile = settings['profiles'][fixtures.ID]
                profile['source_definitions']['synthetic_connectivity'][mapping_field] = [meaning]
                validate_profile(profile)
                prior, incidents = None, empty_state()
                for second in (0, 5, 15, 25):
                    now = fixtures.at(second)
                    rows = bridge.collect_selected_observations(
                        lambda _: NS(state=meaning, last_reported=fixtures.timestamp(now)), settings, now)
                    self.assertEqual(rows[0]['evidence_kind'], 'UNKNOWN')
                    result = evaluate(fixtures.policy(), 'strong', profile, rows, prior, now)
                    prior = result['state']
                    self.assertEqual(prior['negative_count'], 0)
                    self.assertEqual(prior['positive_count'], 0)
                    self.assertEqual(result['availability_state'], 'UNKNOWN')
                    incidents = apply_evaluation(incidents, fixtures.policy(), result)
                    self.assertFalse(incidents['cases'])
                    self.assertFalse(incidents['outbox'])

    def test_reserved_unknown_mapping_cannot_create_outage(self):
        self._reserved_mapping_cannot_create_outage('unknown')

    def test_reserved_unavailable_mapping_cannot_create_outage(self):
        self._reserved_mapping_cannot_create_outage('unavailable')

    def test_genuine_mappings_preserve_evaluation_and_outage_events(self):
        from hioc.availability import validate_profile, evaluate
        from hioc.availability_incidents import empty_state, apply_evaluation
        for meaning, kind, expected in (('connected', 'POSITIVE', 'AVAILABLE'),
                                         ('disconnected', 'NEGATIVE', 'OFFLINE')):
            with self.subTest(meaning=meaning):
                settings = self.settings()
                profile = settings['profiles'][fixtures.ID]
                validate_profile(profile)
                prior, incidents = None, empty_state()
                for second in (0, 15):
                    now = fixtures.at(second)
                    rows = bridge.collect_selected_observations(
                        lambda _: NS(state=meaning, last_reported=fixtures.timestamp(now)), settings, now)
                    self.assertEqual(rows[0]['evidence_kind'], kind)
                    result = evaluate(fixtures.policy(), 'strong', profile, rows, prior, now)
                    prior = result['state']
                    incidents = apply_evaluation(incidents, fixtures.policy(), result)
                self.assertEqual(result['availability_state'], expected)
                events = [row['event']['event_kind'] for row in incidents['outbox'].values()]
                self.assertEqual(events, ['OUTAGE_STARTED'] if kind == 'NEGATIVE' else [])



class AssertionFreshnessTests(unittest.TestCase):
    def test_executor_queue_cannot_extend_verified_actor_authorization(self):
        import tempfile,uuid
        from pathlib import Path
        from datetime import datetime,timedelta,timezone
        from unittest.mock import patch
        class Clock(datetime):
            offset=0
            @classmethod
            def now(cls,tz=None):return cls(2026,10,21,tzinfo=timezone.utc)+timedelta(seconds=cls.offset)
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);root.chmod(0o700)
            key=root/'key';key.write_bytes(b'q'*32);key.chmod(0o600)
            client=bridge.Client.__new__(bridge.Client)
            client.config={'issuer':uuid.uuid4().hex,'key_id':'synthetic_key'};client.key_path=key
            client.exchange=Mock(return_value={'fixture':'admitted'})
            with patch.object(bridge,'datetime',Clock):
                Clock.offset=29
                client.request('get',{'asset_id':fixtures.ID},'actor','context',fixtures.TS)
                envelope=json.loads(client.exchange.call_args.args[1])
                self.assertEqual(envelope['assertion']['issued_at'],fixtures.TS)
                self.assertEqual(envelope['assertion']['expires_at'],fixtures.at(30))
                self.assertEqual(set(envelope['payload']),{'asset_id'})
                client.exchange.reset_mock()
                for offset in (30,31,-1):
                    Clock.offset=offset
                    with self.assertRaises(bridge.BridgeError):client.request('get',{'asset_id':fixtures.ID},'actor','context',fixtures.TS)
                client.exchange.assert_not_called()
