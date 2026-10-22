"""Closed status reads and engine integration: no production configuration."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest
import uuid
from unittest.mock import patch
from hioc import availability as a
from hioc.availability_contract import PolicyError,canonical,digest,strict_json
from hioc.availability_incidents import EngineState,empty_state,validate_state
from hioc.availability_protocol import Protocol,IssuerTrust,STATUS_ROUTE,sign
import test_pe7_evaluation as f
import test_pe7_assets as asset_fixtures
from test_pe7_ha import bridge

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('pe7_engine_fixture',ROOT/'pi4/bin/hioc-incident-engine-v2.py')
engine_module=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(engine_module)

class StatusTests(unittest.TestCase):
    def setUp(self):
        fixture=asset_fixtures.PolicyAssetsTests(); fixture.setUp(); self.addCleanup(fixture.doCleanups)
        self.fixture=fixture; self.service=fixture.service; self.store=fixture.storage
        current=fixture.migrate()
        self.service.mutate_policy('update',fixture.payload(current,{'expected_availability':True}),'issuer','actor',lambda:True)
        parent=fixture.home/'state/incidents'; parent.mkdir(mode=0o700)
        self.engine=EngineState(parent/'pe7.json',fixture.home/'engine.lock')
        with self.engine.transaction(): self.engine.initialize_explicitly()
        self.now=f.TS
        self.reader=a.AvailabilityReader(self.service,self.engine,lambda:self.now)

    def cycle(self, rows=None, profile=True):
        return engine_module.run_availability_cycle(self.service,self.engine,
            {f.ID:f.profile()} if profile else {}, [f.observation(kind='POSITIVE')] if rows is None else rows,
            self.now,operator_enabled=lambda:False)

    def read(self):
        value=self.reader.read(f.ID)
        self.assertEqual(bridge.validate_availability_response(copy.deepcopy(value),{'asset_id':f.ID}),value)
        return value

    def saved(self, value):
        current=self.store.load_store()
        return self.service.mutate_policy('update',self.fixture.payload(current,{'expected_availability':value}),'issuer','actor',lambda:True)

    def test_T03_positive_without_incident_has_scope_and_actual_application(self):
        self.cycle(); value=self.read()
        self.assertEqual(value['evaluation']['availability_state'],'AVAILABLE')
        self.assertEqual(value['evaluation']['evidence_scope'],'DEVICE')
        self.assertEqual(value['current_policy_revision'],value['applied_policy_revision'])
        self.assertEqual(value['policy_binding'],'CURRENT')
        with self.engine.transaction(): self.assertEqual(self.engine.read()['cases'],{})

    def test_T04_stale(self):
        self.now=f.at(20); self.cycle([f.observation(kind='POSITIVE')]); value=self.read()
        self.assertEqual(value['evaluation']['availability_state'],'STALE')
        self.assertEqual(value['evaluation']['reason_code'],'SOURCE_STALE')
        self.assertEqual(value['observations'][0]['freshness'],'STALE')

    def test_T04_missing(self):
        self.cycle([]); value=self.read()
        self.assertEqual(value['evaluation']['availability_state'],'UNKNOWN')
        self.assertEqual(value['evaluation']['reason_code'],'SOURCE_MISSING')
        self.assertEqual(value['observations'][0]['collection_status'],'ABSENT')

    def test_failed_collection(self):
        row=f.observation(); row['collection_status']='FAILED'; self.cycle([row])
        value=self.read(); self.assertEqual(value['evaluation']['reason_code'],'COLLECTION_FAILED')
        self.assertEqual(value['observations'][0]['freshness'],'UNKNOWN')

    def test_incomplete_collection(self):
        row=f.observation(); row['completeness']='INCOMPLETE'; self.cycle([row])
        self.assertEqual(self.read()['evaluation']['reason_code'],'COLLECTION_INCOMPLETE')

    def test_conflicting_sources(self):
        profile=f.profile(); first=profile['enabled_sources'][0]; second='second_source'
        profile['enabled_sources']=sorted([first,second]); profile['source_definitions'][second]=dict(profile['source_definitions'][first],source_id=second)
        rows=[f.observation(kind='POSITIVE'),f.observation(kind='NEGATIVE',source=second)]
        engine_module.run_availability_cycle(self.service,self.engine,{f.ID:profile},rows,self.now,operator_enabled=lambda:False)
        value=self.read(); self.assertEqual(value['evaluation']['reason_code'],'SOURCE_CONFLICT')
        self.assertEqual(len(value['observations']),2)

    def test_never_evaluated_requires_valid_store(self):
        value=self.read(); self.assertEqual(value['result'],'NOT_EVALUATED')
        self.assertIsNone(value['applied_policy_revision']); self.assertIsNone(value['evaluation'])

    def test_explicit_OFF(self):
        self.saved(False); self.cycle(); value=self.read()
        self.assertIs(value['expected_availability'],False)
        self.assertEqual(value['evaluation']['availability_state'],'NOT_MONITORED')
        self.assertEqual(value['observations'],[])

    def test_unset_is_not_explicit_OFF(self):
        self.saved(None); self.cycle(); value=self.read()
        self.assertIsNone(value['expected_availability']); self.assertEqual(value['policy_status'],'PRESENT')
        self.assertEqual(value['evaluation']['availability_state'],'NOT_MONITORED')

    def test_ambiguous_identity(self):
        self.service.attachment=lambda _: 'conflicted'; self.cycle()
        self.assertEqual(self.read()['evaluation']['reason_code'],'UNKNOWN_IDENTITY')

    def test_saved_revision_not_applied_until_actual_evaluation(self):
        self.cycle(); old=self.read()['applied_policy_revision']; self.saved(False); value=self.read()
        self.assertEqual(value['policy_binding'],'PENDING'); self.assertEqual(value['applied_policy_revision'],old)
        self.assertGreater(value['current_policy_revision'],old)

    def test_missing_and_corrupt_storage_are_unavailable(self):
        self.engine.path.unlink(); self.assertEqual(self.read()['result'],'UNAVAILABLE')
        self.engine.path.write_text('{}'); self.assertEqual(self.read()['result'],'UNAVAILABLE')

    def test_read_never_writes_evaluates_collects_or_contacts_network(self):
        self.cycle(); before={str(p):p.read_bytes() for p in self.fixture.home.rglob('*') if p.is_file()}
        with patch('os.replace',side_effect=AssertionError('write')), patch('os.chmod',side_effect=AssertionError('chmod')), \
             patch('hioc.availability.evaluate',side_effect=AssertionError('evaluate')), \
             patch('socket.socket',side_effect=AssertionError('network')):
            self.assertEqual(self.read()['result'],'READ')
        self.assertEqual(before,{str(p):p.read_bytes() for p in self.fixture.home.rglob('*') if p.is_file()})

    def test_missing_read_guard_is_not_created(self):
        self.store.lock_path.unlink(); self.assertEqual(self.read()['result'],'UNAVAILABLE')
        self.assertFalse(self.store.lock_path.exists())

    def test_read_does_not_extend_expiry(self):
        self.cycle(); original=self.read()['evaluation']['evaluated_at']; self.now=f.at(20); value=self.read()
        self.assertEqual(value['evaluation']['freshness'],'EXPIRED')
        self.assertEqual(value['evaluation']['evaluated_at'],original)
        self.assertEqual(value['observations'][0]['freshness'],'STALE')

    def test_policy_race_fails_closed(self):
        self.cycle(); original=self.reader._policy; calls=[]
        def racing(key):
            answer=original(key); calls.append(key)
            return answer if len(calls)==1 else (answer[0],answer[1]+1,answer[2],answer[3])
        self.reader._policy=racing
        value=self.read(); self.assertEqual(value['status_reason'],'POLICY_CHANGED_DURING_READ')
        self.assertIsNone(value['evaluation']); self.assertEqual(len(calls),2)

    def test_closed_backend_and_HA_schemas_reject_private_and_forged_data(self):
        self.cycle(); value=self.read()
        for target in ('outer','evaluation','source'):
            bad=copy.deepcopy(value)
            (bad if target=='outer' else bad['evaluation'] if target=='evaluation' else bad['observations'][0])['notes']='private'
            with self.assertRaises(PolicyError): a.validate_status(bad)
            with self.assertRaises(bridge.BridgeError): bridge.validate_availability_response(bad,{'asset_id':f.ID})
        bad=copy.deepcopy(value); bad['current_policy_revision']=True
        with self.assertRaises(PolicyError): a.validate_status(bad)

    def test_separate_read_audience_actor_acl_quota_and_sanitized_errors(self):
        issuer=uuid.uuid4().hex; secret=b'x'*32; peer='b'*64
        trust=IssuerTrust(issuer,'test_key',secret,peer,{'actor':{'availability_status':frozenset([f.ID])}},True)
        protocol=Protocol(self.service,lambda *_:trust,lambda:f.timestamp(self.now),status_reader=self.reader)
        def send(audience='hioc.pe7.availability.read',payload=None):
            payload={'asset_id':f.ID} if payload is None else payload
            assertion=dict(issuer=issuer,key_id='test_key',actor_id='actor',context_id='ctx',request_id=uuid.uuid4().hex,
                audience=audience,method='POST',path=STATUS_ROUTE,issued_at=f.TS,expires_at=f.at(30),payload_sha256=digest(payload))
            return protocol.handle(STATUS_ROUTE,canonical(sign(assertion,payload,secret)),peer)
        self.assertEqual(send('hioc.pe7.asset')['result'],'error')
        self.assertEqual(send(payload={'asset_id':f.ID,'notes':'private'})['result'],'error')
        self.assertEqual(send()['result'],'NOT_EVALUATED')
        trust.actors.clear(); self.assertEqual(send()['error_code'],'FORBIDDEN')
        trust.actors.update({'actor':{'availability_status':frozenset([f.ID])}})
        for _ in range(29): self.assertEqual(send()['result'],'NOT_EVALUATED')
        result=send(); self.assertEqual(result['error_code'],'RATE_LIMITED')
        self.assertEqual(set(result),{'schema_version','result','error_code','retryable'})

if __name__=='__main__':unittest.main()


class VersionAwareClassificationTests(unittest.TestCase):
    def value(self, actor='operator_ha', policy_only=False):
        import test_pe6_classification as previous
        value=previous.asset();value['schema_version']='2.0'
        value.update(store_epoch=f.EPOCH,store_revision=1,policy_requests=[])
        row=value['assets'][previous.OWNER]
        row.update(update_source=actor,expected_availability=True,infrastructure_device=True,infrastructure_type='network_switch')
        if policy_only:
            for key in ('friendly_name','physical_location','purpose','notes'):row[key]=None
        return value

    def test_A01_to_A05_original_value_bytes_digest_provenance_and_policy_only(self):
        import test_pe6_classification as previous
        from hioc.asset_policy import serialize
        from hioc import assets
        import hashlib
        values=[(previous.asset(),False)]+[(self.value(actor,only),only) for actor in ('operator_cli','operator_ha') for only in (False,True)]
        for value,only in values:
            with self.subTest(version=value['schema_version'],only=only):
                raw=serialize(value);inputs=previous.inputs();inputs['assets']=previous.m.snapshot(value,raw=raw)
                before=copy.deepcopy(inputs);result=previous.m.resolve_classification(inputs,previous.NOW)
                proof=next(x for x in result['inputs'] if x['kind']=='assets')
                self.assertEqual(proof['state'],'VALID');self.assertEqual(proof['sha256'],hashlib.sha256(raw).hexdigest())
                self.assertEqual(inputs,before);self.assertEqual(inputs['assets']['raw'].encode(),raw)
                row=result['devices'][0];self.assertIsNone(row['operator_role']);self.assertEqual(row['role_suggestion'],[])
                self.assertEqual(row['metadata_quality'],'incomplete' if only else 'documented')
                if value['schema_version']=='2.0':
                    self.assertEqual(inputs['assets']['value']['assets'][previous.OWNER]['update_source'],value['assets'][previous.OWNER]['update_source'])
                    with self.assertRaises(assets.AssetValidationError):assets.validate_store(value)

    def test_A06_A07_mixed_shapes_future_schema_and_receipts_reject_without_losing_other_sources(self):
        import test_pe6_classification as previous
        variants=[]
        future=self.value();future['schema_version']='3.0';variants.append(future)
        mixed=self.value();mixed['assets'][previous.OWNER]=previous.asset()['assets'][previous.OWNER];variants.append(mixed)
        extra=self.value();extra['secret']='PRIVATE_EXTRA';variants.append(extra)
        receipt=self.value();receipt['policy_requests']=[{}];variants.append(receipt)
        for value in variants:
            inputs=previous.with_host();inputs['assets']=previous.m.snapshot(value)
            result=previous.m.resolve_classification(inputs,previous.NOW)
            self.assertEqual(next(x for x in result['inputs'] if x['kind']=='assets')['state'],'INVALID')
            self.assertEqual(result['devices'][0]['role_suggestion'][0]['role'],'IoT')
            self.assertNotIn('PRIVATE_EXTRA',json.dumps(result))

    def test_native_secure_reader_consumes_original_2_0_without_projection(self):
        import tempfile,hashlib
        import test_pe6_classification as previous
        from hioc.asset_policy import serialize
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);root.chmod(0o700)
            inventory=root/'inventory.json';inventory.write_bytes(previous.m.canonical(previous.inventory()));inventory.chmod(0o600)
            path=root/'assets.json';raw=serialize(self.value());path.write_bytes(raw);path.chmod(0o600)
            lock=root/'asset.lock';lock.write_bytes(b'');lock.chmod(0o600)
            result=previous.caller.evaluate({'inventory':inventory,'assets':path},asset_lock=lock,clock=lambda:previous.NOW)
            self.assertEqual(result['devices'][0]['metadata_quality'],'documented')
            self.assertEqual(next(x for x in result['inputs'] if x['kind']=='assets')['sha256'],hashlib.sha256(raw).hexdigest())
            self.assertEqual(path.read_bytes(),raw)

class StateCapacityTests(unittest.TestCase):
    def test_oversized_state_rejected_before_replacing_readable_journal(self):
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);root.chmod(0o700)
            engine=EngineState(root/'engine.json',root/'engine.lock')
            with engine.transaction():
                engine.initialize_explicitly();before=engine.path.read_bytes();value=engine.read()
                value['legacy_active']={'status':'none','summary':'x'*16777216}
                with self.assertRaises(PolicyError) as caught:engine.write(value)
                self.assertEqual(caught.exception.code,'BUSY')
                self.assertEqual(engine.path.read_bytes(),before)
            self.assertEqual(sorted(p.name for p in root.iterdir()),['engine.json','engine.lock'])
