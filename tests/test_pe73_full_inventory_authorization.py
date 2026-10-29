"""Full eligible population, real temporary stores; all identities synthetic."""
import copy,hashlib,importlib.util,json,tempfile,unittest,uuid
from datetime import timedelta
from pathlib import Path
from unittest.mock import Mock,patch
from hioc import assets
from hioc.asset_policy import PolicyService,PolicyStore
from hioc.availability_contract import canonical,digest,timestamp,time_text,PolicyError
from hioc.availability_protocol import IssuerTrust,Protocol,POPULATION_SCOPES,sign
from hioc.inventory import stable_device_id
import test_assets_schema as legacy
import test_pe5_local_service_association as inventory
R=Path(__file__).resolve().parents[1]
NOW='2026-10-12T12:00:00.000000Z'

def grants(reference='SYNTHETIC_OWNER_ACCEPTANCE'):
 return {op:{'scope':scope,'amendment':'PE73_FULL_INVENTORY_ASSET_AUTHORIZATION_V1','acceptance_reference':reference} for op,scope in POPULATION_SCOPES.items()}

def device(n):return inventory.device(mac='02:00:00:00:%02x:%02x'%(n//256,n%256))

class PopulationTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.home=Path(self.temp.name)
  self.store=PolicyStore(self.home,lock_path=self.home/'assets.lock');self.store.ensure_directories();self.store.timestamp=lambda:NOW
  self.store.inventory_context=lambda _:('available',set())
  self.before=assets.serialize_store(legacy.store());self.store.store_path.write_bytes(self.before)
  self.service=PolicyService(self.store)
  self.devices=[device(1),device(2)];self.write_inventory()
  self.service.migrate(hashlib.sha256(self.before).hexdigest(),writers_stopped=True)
  self.actor='synthetic_admin';self.issuer=uuid.uuid4().hex;self.key=bytes(range(32));self.peer='a'*64
  self.roles={self.actor:grants()};self.trust=IssuerTrust(self.issuer,'fixture',self.key,self.peer,self.roles,True)
  self.status=Mock();self.protocol=Protocol(self.service,lambda i,k:self.trust,lambda:timestamp(NOW),status_reader=self.status)
 def write_inventory(self,value=None):
  value=inventory.snapshot(devices=self.devices) if value is None else value
  self.store.inventory_path.parent.mkdir(parents=True,exist_ok=True);self.store.inventory_path.write_bytes(json.dumps(value).encode())
 def payload(self,key,operation='create'):
  value=self.store.load_store();record=value['assets'].get(key)
  return dict(asset_id=key,store_epoch=value['store_epoch'],expected_store_revision=value['store_revision'],expected_revision=record['revision'] if operation=='update' and record else None,operation_id=uuid.uuid4().hex,fields={'expected_availability':False})
 def request(self,op,key=None,payload=None,actor=None):
  key=key or self.devices[0]['id'];payload=payload or ({'asset_id':key} if op in ('get','availability_status') else self.payload(key,op))
  path='/pe7/v1/availability/status' if op=='availability_status' else '/pe7/v1/policy/'+op
  now=timestamp(NOW);a=dict(issuer=self.issuer,key_id='fixture',audience='hioc.pe7.availability.read' if op=='availability_status' else 'hioc.pe7.asset',actor_id=actor or self.actor,context_id='fixture_context',request_id=uuid.uuid4().hex,issued_at=time_text(now),expires_at=time_text(now+timedelta(seconds=30)),method='POST',path=path,payload_sha256=digest(payload))
  return path,sign(a,payload,self.key)
 def send(self,op,key=None,payload=None,actor=None):
  path,value=self.request(op,key,payload,actor);return self.protocol.handle(path,canonical(value),self.peer)
 def test_zero_store_read_and_first_explicit_creation(self):
  self.assertEqual(self.store.load_store()['asset_count'],0)
  response=self.send('get');self.assertIsNone(response['policy']['revision']);self.assertEqual(self.store.load_store()['asset_count'],0)
  self.assertEqual(self.send('create')['result'],'created');self.assertEqual(self.store.load_store()['asset_count'],1)
 def test_subsequent_and_newly_discovered_no_ACL_rebuild(self):
  frozen=copy.deepcopy(self.roles)
  self.assertEqual(self.send('create')['result'],'created')
  self.devices.append(device(3));self.write_inventory()
  for row in self.devices[1:]:self.assertEqual(self.send('create',row['id'])['result'],'created')
  self.assertEqual(self.store.load_store()['asset_count'],3);self.assertEqual(self.roles,frozen)
 def test_existing_policy_read_and_update(self):
  self.send('create');key=self.devices[0]['id'];payload=self.payload(key,'update');payload['fields']={'infrastructure_device':True,'infrastructure_type':'network_switch'}
  self.assertEqual(self.send('update',payload=payload)['result'],'updated')
  self.assertTrue(self.send('get')['policy']['infrastructure_device'])
 def test_missing_actor_denied(self):self.assertEqual(self.send('create',actor='other')['error_code'],'FORBIDDEN')
 def test_removed_grant_immediately_denied(self):
  self.roles[self.actor].pop('create');self.assertEqual(self.send('create')['error_code'],'FORBIDDEN');self.assertEqual(self.store.load_store()['asset_count'],0)
 def test_unaccepted_amendment_cannot_be_enabled(self):
  self.roles[self.actor]=grants(None);self.assertEqual(self.send('create')['error_code'],'FORBIDDEN')
 def test_disabled_issuer_denied(self):
  self.trust=IssuerTrust(self.issuer,'fixture',self.key,self.peer,self.roles,False)
  self.assertEqual(self.send('create')['error_code'],'TRUST_INVALID')
 def test_weak_identity_denied(self):
  self.devices[0]['mac']='';self.write_inventory();self.assertEqual(self.send('create')['error_code'],'FORBIDDEN')
 def test_duplicate_MAC_denied(self):
  self.devices.append(copy.deepcopy(self.devices[0]));self.write_inventory();self.assertEqual(self.send('create')['error_code'],'FORBIDDEN')
 def test_mismatched_derived_ID_denied(self):
  self.devices[0]['id']='dev_1111111111111111';self.write_inventory();self.assertEqual(self.send('create')['error_code'],'FORBIDDEN')
 def test_stale_inventory_denied(self):
  value=inventory.snapshot(devices=self.devices);value['updated']='2026-10-11T00:00:00Z';self.write_inventory(value)
  self.assertEqual(self.send('create')['error_code'],'FORBIDDEN')
 def test_future_inventory_denied(self):
  value=inventory.snapshot(devices=self.devices);value['updated']='2026-10-12T12:00:01Z';self.write_inventory(value)
  self.assertEqual(self.send('create')['error_code'],'FORBIDDEN')
 def test_orphan_creation_denied(self):self.assertEqual(self.send('create','dev_1111111111111111')['error_code'],'FORBIDDEN')
 def test_existing_create_conflict_not_overwrite(self):
  self.send('create');before=self.store.store_path.read_bytes();self.assertEqual(self.send('create')['error_code'],'REVISION_CONFLICT');self.assertEqual(self.store.store_path.read_bytes(),before)
 def test_durable_create_replay_preserved(self):
  payload=self.payload(self.devices[0]['id']);first=self.send('create',payload=payload);second=self.send('create',payload=payload)
  self.assertEqual(second['result'],'replayed');self.assertEqual(first['receipt'],second['receipt'])
 def test_transport_nonce_replay_preserved(self):
  path,envelope=self.request('get');raw=canonical(envelope);self.protocol.handle(path,raw,self.peer)
  self.assertEqual(self.protocol.handle(path,raw,self.peer)['error_code'],'REPLAY_CONFLICT')
 def test_store_revision_conflict(self):
  payload=self.payload(self.devices[1]['id']);self.send('create');self.assertEqual(self.send('create',payload=payload)['error_code'],'REVISION_CONFLICT')
 def test_store_epoch_conflict(self):
  payload=self.payload(self.devices[0]['id']);payload['store_epoch']=uuid.uuid4().hex
  self.assertEqual(self.send('create',payload=payload)['error_code'],'REVISION_CONFLICT')
 def test_read_grant_does_not_authorize_create(self):
  self.roles[self.actor]={'get':grants()['get']};self.assertEqual(self.send('get')['result'],'read');self.assertEqual(self.send('create')['error_code'],'FORBIDDEN')
 def test_create_grant_does_not_authorize_update(self):
  self.send('create');self.roles[self.actor]={'create':grants()['create']}
  self.assertEqual(self.send('update')['error_code'],'FORBIDDEN')
 def test_existing_update_scope_cannot_create_missing_asset(self):
  self.assertEqual(self.send('update')['error_code'],'FORBIDDEN')
 def test_status_requires_its_own_grant(self):
  self.send('create');self.roles[self.actor].pop('availability_status')
  self.assertEqual(self.send('availability_status')['error_code'],'FORBIDDEN');self.status.read.assert_not_called()
 def test_status_requires_existing_Asset(self):
  self.assertEqual(self.send('availability_status')['error_code'],'FORBIDDEN');self.status.read.assert_not_called()
 def test_wrong_operation_scope_denied(self):
  self.roles[self.actor]['create']['scope']='existing_assets';self.assertEqual(self.send('create')['error_code'],'TRUST_INVALID')
 def test_wildcard_and_extra_scope_keys_denied(self):
  for grant in ({'scope':'*','acceptance_reference':'FIXTURE'},{'scope':'eligible_inventory','acceptance_reference':'FIXTURE','admin':True}):
   self.roles[self.actor]['create']=grant;self.assertEqual(self.send('create')['error_code'],'TRUST_INVALID')
 def test_invalid_signature_never_reads_population(self):
  path,envelope=self.request('get');envelope['signature']='0'*64
  with patch.object(self.service,'authorize_population',side_effect=AssertionError('NO_READ')):
   self.assertEqual(self.protocol.handle(path,canonical(envelope),self.peer)['error_code'],'TRUST_INVALID')
 def test_revocation_at_writer_guard(self):
  original=self.service.mutate_policy
  def mutate(*args):self.roles.clear();return original(*args)
  with patch.object(self.service,'mutate_policy',side_effect=mutate):self.assertEqual(self.send('create')['error_code'],'FORBIDDEN')
  self.assertEqual(self.store.load_store()['asset_count'],0)
 def test_inventory_change_at_writer_guard(self):
  original=self.service.mutate_policy
  def mutate(*args):self.devices=[];self.write_inventory();return original(*args)
  with patch.object(self.service,'mutate_policy',side_effect=mutate):self.assertEqual(self.send('create')['error_code'],'FORBIDDEN')
  self.assertEqual(self.store.load_store()['asset_count'],0)
 def test_no_implicit_migration_of_zero_record_schema1(self):
  self.store.store_path.write_bytes(self.before)
  self.assertEqual(self.send('get')['error_code'],'UNSUPPORTED_SCHEMA');self.assertEqual(self.store.store_path.read_bytes(),self.before)
 def test_exact_ID_grants_remain_valid_and_bounded(self):
  self.roles[self.actor]={op:frozenset([self.devices[0]['id']]) for op in POPULATION_SCOPES}
  self.assertEqual(self.send('create')['result'],'created');self.assertEqual(self.send('get',self.devices[1]['id'])['error_code'],'FORBIDDEN')
 def test_restart_JSON_grants_persist_and_revocation_reloaded(self):
  path=self.home/'synthetic-acl.json';path.write_text(json.dumps(self.roles))
  def lookup(i,k):return IssuerTrust(self.issuer,'fixture',self.key,self.peer,json.loads(path.read_text()),True)
  self.protocol=Protocol(self.service,lookup,lambda:timestamp(NOW));self.assertEqual(self.send('create')['result'],'created')
  self.protocol=Protocol(PolicyService(self.store),lookup,lambda:timestamp(NOW));self.assertEqual(self.send('get')['result'],'read')
  path.write_text('{}');self.assertEqual(self.send('get')['error_code'],'FORBIDDEN')
 def test_mutation_quota_preserved(self):
  for i in range(11):response=self.send('create')
  self.assertEqual(response['error_code'],'RATE_LIMITED')
 def test_policy_manage_orphan_OFF_without_new_create_authority(self):
  self.send('create');key=self.devices[0]['id'];self.devices=[];self.write_inventory()
  self.assertEqual(self.send('get',key)['policy']['attachment'],'orphan')
  self.assertEqual(self.send('update',key)['result'],'no_change')
  payload=self.payload(key,'update');payload['fields']={'expected_availability':True}
  self.assertEqual(self.send('update',key,payload)['error_code'],'IDENTITY_UNSAFE')

 def test_authorized_status_reads_existing_record(self):
  from hioc.availability import AvailabilityReader
  from hioc.availability_incidents import EngineState
  self.send('create')
  self.protocol.status_reader=AvailabilityReader(self.service,EngineState(self.home/'state/incidents/pe7.json',self.home/'incidents.lock'),lambda:NOW)
  response=self.send('availability_status');self.assertIn(response['result'],('NOT_EVALUATED','UNAVAILABLE'));self.assertEqual(response['asset_id'],self.devices[0]['id'])
 def test_result_read_requires_separate_existing_grant(self):
  payload=self.payload(self.devices[0]['id']);self.send('create',payload=payload)
  request={'asset_id':payload['asset_id'],'operation_id':payload['operation_id']}
  self.assertEqual(self.send('result',payload=request)['commit_state'],'CONFIRMED')
  self.roles[self.actor].pop('result');self.assertEqual(self.send('result',payload=request)['error_code'],'FORBIDDEN')
 def test_wrong_amendment_rejected(self):
  self.roles[self.actor]['create']['amendment']='OTHER'
  self.assertEqual(self.send('create')['error_code'],'TRUST_INVALID')

class ProvisioningTests(unittest.TestCase):
 def test_population_plan_and_disabled_packet_no_ID_list(self):
  import test_pe73_ha_provision as fixture
  plan=fixture.plan();plan['actors']={'synthetic_admin':grants(None)}
  self.assertEqual(fixture.q.validate_plan(plan),plan)
  value=fixture.q.packet(plan,'a'*64,fixture.p)
  self.assertFalse(value['backend']['enabled']);self.assertEqual(value['backend']['issuer_trusts'][0]['actors'],plan['actors'])
 def test_original_contract_unchanged(self):
  raw=(R/'docs/PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION_CONTRACT.md').read_bytes()
  self.assertEqual(hashlib.sha256(raw).hexdigest(),'db8e25ba10e7038ee56a66aa12481d11c18b731a22ee4dfdc4de761031a9e14d')
