"""Repository-only declarative preparation specification, NOT a runtime implementation.
All devices/state/read conditions below are synthetic in-memory fixtures. Existing
pure adapter validators are reused; no adapter/filesystem/network entrypoint runs.
Future POSIX reader and inventory integration need separate implementation tests.
"""
import copy
import hashlib
import json
import re
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch
from hioc import home_assistant_association as private
from test_pe4_ha_association_deployment_closure import canonical, validate

ROOT = Path(__file__).resolve().parents[1]
BASE = 'debe1ae485cf6b88839f9f8f2fbb071835deda05'
PATH = ROOT / 'governance/pe4/pe4-ha-association-public-projection-preparation.json'
R = json.loads(PATH.read_bytes())
S = json.loads(PATH.with_suffix('.schema.json').read_bytes())
PRIVATE_SCHEMA = json.loads((ROOT / R['validation']['private_schema_path']).read_bytes())
PUBLIC_SCHEMA = R['public_object_schema']
STAMP = '2030-01-02T03:04:05Z'


def association(index=1, complete=True):
    return dict(hioc_device_id='dev_'+format(index, '016x'), ha_device_id='fixture_device_'+str(index),
                association_basis='unique_mac', status='ASSOCIATED_STRONG_MAC',
                first_associated_at=STAMP, last_confirmed_at=STAMP,
                observed_ha_version='synthetic-version', contract_version='1.0',
                relationship_status='COMPLETE' if complete else 'INCOMPLETE')


def state(records=None, history=None):
    records = [] if records is None else records
    history = [] if history is None else history
    return dict(schema_version='1.1', updated_at=STAMP, instance_reference='PI5_HA',
                observed_ha_version='synthetic-version', contract_version='1.0',
                associations=records, binding_history=history, diagnostics=[],
                summary=dict(associated_devices=len(records), entity_memberships=sum(len(x.get('entities', [])) for x in records),
                             historical_bindings=len(history), review_only=0, rejected=0, unmatched=0))


def devices(count=3):
    return [dict(id='dev_'+format(i, '016x'), mac='base-mac', ip='base-ip',
                 display_name='operator fixture', last_seen='base-time', reachable=True,
                 health_score=97, incidents=['base-incident'], Assets={'owner':'fixture'}) for i in range(1, count+1)]


def specification_strip(previous):
    """Test-local preparation model for both pre-discovery and pre-attachment stripping."""
    result = copy.deepcopy(previous)
    for device in result:
        device.pop('home_assistant', None)
    return result


def specification_public_check(value):
    private.validate_schema(value, PUBLIC_SCHEMA)
    private.validate_privacy(value)
    domains = value['integration_domains']
    if domains != sorted(set(domains)) or any(re.fullmatch('[0-9a-f]{12}', x) for x in domains):
        raise ValueError('unsafe or noncanonical domain')


def specification_project(current, raw):
    """Executable declarative fixture oracle only; never imported by production."""
    base = specification_strip(current)
    try:
        parsed = private.strict_json(raw, 'CANDIDATE_STATE_VALIDATION')
        private.check_schema_contract(PRIVATE_SCHEMA)
        private.validate_state(parsed, PRIVATE_SCHEMA)
        ids = [d['id'] for d in base]
        if len(set(ids)) != len(ids):
            raise ValueError('ambiguous current inventory')
        projected = {}
        for record in parsed['associations']:
            if record['hioc_device_id'] not in ids:
                continue
            obj = dict(associated=True, association_basis='strong_mac',
                       entity_count=len(record.get('entities', [])),
                       integration_domains=sorted({x['domain'] for x in record.get('config_entries', [])}),
                       has_area_candidate=isinstance(record.get('area_candidate'), dict))
            specification_public_check(obj)
            projected[record['hioc_device_id']] = obj
        # Attach only after the whole candidate projection validates.
        for device in base:
            if device['id'] in projected:
                device['home_assistant'] = projected[device['id']]
    except Exception:
        return specification_strip(current)
    return base


def specification_read_condition(**changes):
    """Truth table, not a filesystem reader; models conditions required under lock."""
    checks = dict(lock_exists=True, shared_lock_available=True, regular_file=True,
                  pinned_no_symlink=True, owner_group_mode_acl_valid=True, link_count_one=True,
                  namespace_clean_before=True, namespace_clean_after=True, size_bounded=True,
                  complete_read=True, file_fingerprint_unchanged=True,
                  parent_and_lock_binding_unchanged=True, deadline_within_budget=True)
    checks.update(changes)
    return all(checks.values())


class PreparationGovernanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.blobs = {x['path']:subprocess.check_output(['git','show',BASE+':'+x['path']],cwd=ROOT) for x in R['sources']}

    def test_canonical_record_and_schema(self):
        validate(R,S)
        self.assertEqual(PATH.read_bytes(),canonical(R))
        self.assertEqual(PATH.with_suffix('.schema.json').read_bytes(),canonical(S))

    def test_closed_every_node_rejects_broadening(self):
        def walk(v,s):
            if type(v) is dict:
                bad=copy.deepcopy(v);bad['unreviewed']=True
                with self.assertRaises(ValueError):validate(bad,s)
                for k,x in v.items():walk(x,s['properties'][k])
            elif type(v) is list:
                with self.assertRaises(ValueError):validate(v+[None],s)
                for x,n in zip(v,s['prefixItems']):walk(x,n)
            else:
                with self.assertRaises(ValueError):validate(None,s)
        walk(R,S)

    def test_exact_predecessor_authority(self):
        self.assertEqual(R['preparation_predecessor'],BASE)
        self.assertEqual(subprocess.check_output(['git','show','-s','--format=%s',BASE],cwd=ROOT).decode().strip(),R['predecessor_subject'])
        self.assertEqual(subprocess.check_output(['git','rev-parse',BASE+'^'],cwd=ROOT).decode().strip(),R['predecessor_parent'])

    def test_bound_sources_exact_git_and_immutable_runtime(self):
        self.assertEqual(len(R['sources']),103)
        for item in R['sources']:
            raw=self.blobs[item['path']]
            self.assertEqual(item['commit'],BASE)
            self.assertEqual(hashlib.sha256(raw).hexdigest(),item['sha256'])
            self.assertEqual(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),item['git_blob'])
            if not item['historical_only']:
                self.assertEqual((ROOT/item['path']).read_bytes().replace(b'\r\n',b'\n'),raw)

    def test_exact_frozen_allowlist_matches_0c(self):
        old=json.loads(self.blobs['governance/pe4/pe4-0c-association-contract.json'])
        # The bound source explicitly names all public keys and the strong basis.
        text=json.dumps(old)
        for field in R['architecture']['fields']:self.assertIn(field,text)
        self.assertIn('home_assistant.association_basis = strong_mac',self.blobs['docs/PE4_HOME_ASSISTANT_ASSOCIATION_CONTRACT.md'].decode())
        self.assertEqual(set(PUBLIC_SCHEMA['required']),set(R['architecture']['fields']))
        self.assertEqual(len(PUBLIC_SCHEMA['required']),5)
        self.assertFalse(PUBLIC_SCHEMA['additionalProperties'])

    def test_schema_bound_and_pure_module_import(self):
        self.assertEqual(private.SCHEMA_SHA,R['validation']['private_schema_sha256'])
        self.assertEqual(hashlib.sha256(self.blobs[R['validation']['private_schema_path']]).hexdigest(),private.SCHEMA_SHA)
        private.check_schema_contract(PRIVATE_SCHEMA)
        self.assertIn('Importing this module performs no I/O',self.blobs['pi4/lib/hioc/home_assistant_association.py'].decode())
        self.assertIn('from websockets.asyncio.client import connect',self.blobs['pi4/lib/hioc/home_assistant_association.py'].decode().split('async def network',1)[1])

    def test_inventory_carry_forward_requires_both_strips(self):
        self.assertIn('record = dict(old)',self.blobs['pi4/lib/hioc/inventory.py'].decode())
        self.assertIn('BEFORE_DISCOVERY',R['architecture']['recomputation'])
        self.assertIn('BEFORE_ATTACH',R['architecture']['recomputation'])

    def test_single_writer_files_before_mqtt_and_one_connection(self):
        text=self.blobs['pi4/bin/hioc-inventory-engine.py'].decode()
        self.assertEqual(R['architecture']['writer'],'pi4/bin/hioc-inventory-engine.py')
        self.assertLess(text.index('store.write_json("inventory.json"'),text.index('with MqttClient('))
        self.assertEqual(text.count('with MqttClient('),1)
        self.assertTrue(R['mqtt']['retained']);self.assertEqual(R['mqtt']['qos'],0)
        self.assertEqual(R['mqtt']['projection_topics'],['inventory','inventory/devices'])
        self.assertEqual(len(R['mqtt']['existing_topics']),7)
        self.assertFalse(R['mqtt']['new_topics'])

    def test_consumer_transports_nested_devices_without_changes(self):
        text=self.blobs['homeassistant/packages/hioc_living_inventory.yaml'].decode().split('- name: HIOC Inventory Devices',1)[1].split('- name:',1)[0]
        self.assertIn('json_attributes_topic: home/infrastructure/hioc/inventory',text)
        self.assertNotIn('json_attributes_template',text)
        self.assertFalse(R['consumers']['ha_package_change_required'])
        self.assertFalse(R['consumers']['dashboard_change_authorized'])

    def test_existing_scheduler_and_history_closure_unchanged(self):
        old=json.loads(self.blobs['governance/pe4/pe4-ha-association-scheduler-deployment-closure.json'])
        self.assertIn('5,35 * * * *',old['canonical_cron']['line'])
        self.assertEqual(R['timing']['association_schedule'],'5,35 * * * *')
        self.assertEqual(R['lifecycle']['scheduler_deployment'],'PASS_CLOSED')
        self.assertEqual(R['lifecycle']['recurring_scheduler'],'ACTIVE_AUTHORIZED')
        self.assertEqual(R['lifecycle']['manual_second_adapter_execution'],'NOT_AUTHORIZED_NOT_PERFORMED')

    def test_timing_slots_and_no_wallclock_sla(self):
        for slot in [5,35]:self.assertEqual(((30 if slot==5 else 60)-slot),25)
        self.assertEqual(R['timing']['nominal_slot_to_next_inventory_minutes'],25)
        self.assertIn('NOT_HARD_WALLCLOCK',R['timing']['expectation'])
        for key in ['new_scheduler','cascade','forced_inventory']:self.assertFalse(R['timing'][key])

    def test_lock_coherence_accounts_for_rollback_and_hardlinks(self):
        text=self.blobs['pi4/lib/hioc/home_assistant_association.py'].decode()
        self.assertIn('fcntl.LOCK_EX | fcntl.LOCK_NB',text)
        self.assertIn('links=2',text)
        self.assertIn('LOCK_SH|LOCK_NB',R['coherence']['reader_lock'])
        self.assertIn('NO_CREATE_NO_RETRY',R['coherence']['reader_lock'])
        self.assertIn('ROLLED_BACK',R['coherence']['atomic_only_rejected'])
        self.assertIn('NO_JSON_VALIDATION',R['coherence']['critical_section'])
        self.assertIn('NEXT_NATURAL_SLOT',R['coherence']['contention'])

    def test_future_install_order_inventory_only_quiescence(self):
        deploy=R['deployment']
        self.assertTrue(deploy['association_can_remain_active'])
        self.assertIn('PRIVATE_ADAPTER_SCHEMA_RUNTIME_LOCK_CONTRACT_UNCHANGED',deploy['association_condition'])
        self.assertIn('DRAIN_ALL_INVENTORY_PROCESSES',deploy['inventory_quiescence'])
        self.assertIn('INSTALL_HELPER_AND_PUBLIC_CONTRACT_BEFORE_ENGINE',deploy['order'])
        self.assertIn('INSTALL_ENGINE_LAST_VERIFY_COMPLETE_COHERENT_SET',deploy['order'])
        installer=self.blobs['pi4/install_pi4.sh'].decode()
        self.assertIn('crontab -',installer);self.assertIn('"$INSTALL_DIR/pi4/bin/hioc-inventory-engine.py"',installer)
        self.assertIn('rsync',self.blobs['release/upgrade.sh'].decode())
        self.assertIn('NOT_AUTHORIZED',deploy['generic_install_upgrade_rollback'])

    def test_current_master_lifecycle_and_separate_handoff(self):
        text=(ROOT/'docs/HIOC_MASTER_PLAN.md').read_text(encoding='utf8')
        table=text.split('## Authoritative Current PE-4 Lifecycle',1)[1].split('### Completed',1)[0]
        self.assertIn('| PE-4 Home Assistant Association Public Projection Preparation | PASS/CLOSED |',table)
        self.assertIn('| PE-4 Home Assistant Association Adapter Public Projection | NOT STARTED / PREPARED FOR SEPARATE IMPLEMENTATION |',table)
        self.assertIn('| PE-4 | NOT COMPLETE |',table)
        for marker in ['## Current Objective','## Next Planned Task']:
            section=text.split(marker,1)[1].split('### Historical',1)[0]
            self.assertIn('public projection preparation commit ONLY',section)
            self.assertIn('STOP and independent',section)
        self.assertEqual(R['unresolved_questions'],[])


class PreparationFixtureTests(unittest.TestCase):
    def project(self, records=None, history=None, current=None):
        return specification_project(devices() if current is None else current,canonical(state(records,history)))

    def test_exact_namespace_five_keys_current_active_only(self):
        result=self.project([association()])
        self.assertEqual(set(result[0]['home_assistant']),set(R['architecture']['fields']))
        self.assertTrue(result[0]['home_assistant']['associated'])
        self.assertNotIn('home_assistant',result[1])
        self.assertEqual(result[0]['home_assistant']['association_basis'],'strong_mac')
        self.assertNotIn('unique_mac',canonical(result).decode())

    def test_history_and_retired_never_project_or_create_devices(self):
        h=association(1)
        h={k:v for k,v in h.items() if k in ['hioc_device_id','ha_device_id','first_associated_at','last_confirmed_at']}
        h['first_associated_at']='2029-01-01T00:00:00Z';h['last_confirmed_at']='2029-01-01T01:00:00Z'
        h.update(retired_at='2029-01-01T02:00:00Z',retirement_reason='HA_DEVICE_ABSENT')
        self.assertEqual(self.project(history=[h]),devices())
        self.assertEqual(self.project([association(7)]),devices())

    def test_config_domains_only_unique_sorted_no_platform_fallback(self):
        a=association();a['config_entries']=[dict(entry_id='entry_'+str(i),domain=d) for i,d in enumerate(['zha','mqtt','zha'])]
        a['entities']=[dict(registry_id='registry_fixture',entity_id='sensor.fixture',platform='forbidden_platform_fallback')]
        obj=self.project([a])[0]['home_assistant']
        self.assertEqual(obj['integration_domains'],['mqtt','zha']);self.assertEqual(obj['entity_count'],1)
        self.assertNotIn('forbidden_platform_fallback',canonical(obj).decode())

    def test_complete_incomplete_safe_members_and_area_boolean(self):
        for complete in [True,False]:
            a=association(complete=complete);a['area_candidate']={'area_id':'fixture_area','name':'private room'}
            obj=self.project([a])[0]['home_assistant']
            self.assertEqual(obj,dict(associated=True,association_basis='strong_mac',entity_count=0,integration_domains=[],has_area_candidate=True))
            a['area_candidate']=None
            self.assertFalse(self.project([a])[0]['home_assistant']['has_area_candidate'])

    def test_private_relationships_names_ids_times_metadata_do_not_leak(self):
        a=association();a['ha_metadata']={'name':'private fixture name','manufacturer':'private fixture vendor'}
        a['area_candidate']={'area_id':'private_area','name':'private location'}
        a['entities']=[dict(registry_id='private_registry',entity_id='sensor.private_fixture',platform='private_platform')]
        a['config_entries']=[dict(entry_id='private_entry',domain='mqtt')]
        obj=self.project([a])[0]['home_assistant'];raw=canonical(obj).decode()
        for value in ['private','fixture_device','synthetic-version','2030-','unique_mac','COMPLETE']:
            self.assertNotIn(value,raw)
        self.assertEqual(len(obj),5)

    def test_strip_before_discovery_prevents_self_enrichment(self):
        prior=devices();prior[0]['home_assistant']={'associated':True,'entity_count':99}
        stripped=specification_strip(prior)
        self.assertEqual(stripped,devices())
        self.assertIn('home_assistant',prior[0])
        self.assertEqual(specification_project(prior,canonical(state())),devices())

    def test_recomputed_current_projection_does_not_retain_old_fields(self):
        current=devices();current[0]['home_assistant']={'arbitrary':'unsafe stale'}
        self.assertEqual(self.project([association()],current=current)[0]['home_assistant']['entity_count'],0)
        self.assertNotIn('arbitrary',self.project([association()],current=current)[0]['home_assistant'])

    def test_ordinary_inventory_authority_and_membership_unchanged(self):
        before=devices();result=self.project([association(2),association(8)],current=before)
        self.assertEqual(specification_strip(result),before)
        self.assertEqual([d['id'] for d in result],[d['id'] for d in before])
        self.assertEqual(before,devices())
        self.assertEqual(len(result),3)

    def test_synthetic_counts_varied_and_output_order_deterministic(self):
        for count in [0,1,2,4,7]:
            current=devices(count);records=[association(i) for i in range(1,count+1)]
            self.assertEqual(canonical(self.project(records,current=current)),canonical(self.project(list(reversed(records)),current=current)))
            self.assertEqual(sum('home_assistant' in d for d in self.project(records,current=current)),count)

    def test_invalid_private_snapshot_omits_entire_projection_no_partial(self):
        a=association(2);a['config_entries']=[dict(entry_id='entry',domain='deadbeefcafe')]
        self.assertEqual(self.project([association(1),a]),devices())

    def test_entity_count_and_domain_public_bounds(self):
        obj=dict(associated=True,association_basis='strong_mac',entity_count=65536,integration_domains=['a'+'b'*63],has_area_candidate=False)
        specification_public_check(obj)
        for field,value in [('entity_count',65537),('entity_count',-1),('entity_count',True),('entity_count',1.5),('integration_domains',['a'+'b'*64]),('integration_domains',['mqtt']*4097)]:
            bad=copy.deepcopy(obj);bad[field]=value
            with self.assertRaises((private.Failure,ValueError)):specification_public_check(bad)

    def test_duplicate_active_hioc_ids_rejected(self):
        a=association(2);a['hioc_device_id']=association(1)['hioc_device_id']
        self.assertEqual(self.project([association(1),a]),devices())

    def test_duplicate_current_inventory_ids_isolated(self):
        current=[devices()[0],devices()[0]]
        self.assertEqual(self.project([association()],current=current),current)

    def test_no_network_credentials_adapter_entrypoints_or_generic_ingestion(self):
        with patch.object(private,'network',side_effect=AssertionError('network')),patch.object(private,'run_cycle',side_effect=AssertionError('adapter')),patch.object(private.PosixFS,'start',side_effect=AssertionError('private FS')):
            self.assertIn('home_assistant',self.project([association()])[0])
        for key in ['GENERIC_INTEGRATION_INGESTION','HA_ACCESS','CREDENTIAL_ACCESS','MQTT_PUBLICATION','SYSTEMD','SCHEDULER_MUTATION']:
            self.assertIn(key,R['prohibited_actions'])

    def test_normal_complete_previous_and_new_snapshot_selection(self):
        previous=canonical(state([association(1)]));new=canonical(state([association(2)]))
        self.assertTrue(specification_read_condition())
        self.assertNotEqual(specification_project(devices(),previous),specification_project(devices(),new))
        # Later replacement is irrelevant after a locked coherent copy has been released.
        copied=bytes(previous);new=canonical(state())
        self.assertIn('home_assistant',specification_project(devices(),copied)[0])

    def test_duplicate_json_keys_utf8_nonfinite_oversize_isolated(self):
        for raw in [b'{"schema_version":"1.1","schema_version":"1.1"}',b'\xff',b'{"x":NaN}',b'{"x":Infinity}',b'x'*(private.LIMIT+1),b'{',b'null']:
            self.assertEqual(specification_project(devices(),raw),devices())


# Separate test cases keep each failure condition and privacy boundary visible.
def private_reject_case(path,value):
    def test(self):
        candidate=state([association()]);node=candidate
        for key in path[:-1]:node=node[key]
        node[path[-1]]=value
        current=devices();current[0]['home_assistant']={'stale':True}
        self.assertEqual(specification_project(current,canonical(candidate)),devices())
    return test

PRIVATE_REJECTS={
 'schema_version':(('schema_version',),'1.0'),
 'summary':(('summary','associated_devices'),3),
 'stable_id':(('associations',0,'hioc_device_id'),'arbitrary'),
 'status':(('associations',0,'status'),'RETIRED'),
 'basis':(('associations',0,'association_basis'),'strong_mac'),
 'unknown_private_key':(('associations',0,'unknown'),True),
 'url':(('associations',0,'ha_device_id'),'https://private.invalid/'),
 'mac':(('associations',0,'ha_device_id'),'aa:bb:cc:dd:ee:ff'),
 'ip':(('associations',0,'ha_device_id'),'192.168.2.3'),
 'hostname':(('associations',0,'ha_device_id'),'private.local'),
 'control':(('associations',0,'ha_device_id'),'private\nvalue'),
 'unsafe_domain':(('associations',0,'config_entries'),[{'entry_id':'fixture','domain':'https://private'}]),
 'entity_shape':(('associations',0,'entities'),[{'entity_id':'sensor.fixture'}]),
 'config_shape':(('associations',0,'config_entries'),[{'domain':'mqtt'}]),
 'area_shape':(('associations',0,'area_candidate'),{'name':'private'}),
 'relationship_status':(('associations',0,'relationship_status'),'UNKNOWN'),
 'time_semantics':(('associations',0,'last_confirmed_at'),'2029-01-01T00:00:00Z'),
}
for name,(path,value) in PRIVATE_REJECTS.items():
    setattr(PreparationFixtureTests,'test_private_reject_'+name,private_reject_case(path,value))


def public_reject_case(field,value):
    def test(self):
        obj=dict(associated=True,association_basis='strong_mac',entity_count=0,integration_domains=[],has_area_candidate=False)
        obj[field]=value
        with self.assertRaises((private.Failure,ValueError)):specification_public_check(obj)
    return test
PUBLIC_REJECTS={
 'false':('associated',False),'integer_boolean':('associated',1),
 'private_basis':('association_basis','unique_mac'),'other_basis':('association_basis','ip'),
 'area_id':('area_id','private'),'area_name':('area_name','private'),
 'entity_id':('entity_id','sensor.private'),'ha_id':('ha_device_id','private'),
 'config_id':('entry_id','private'),'metadata':('ha_metadata',{}),
 'relationship':('relationship_status','COMPLETE'),'timestamp':('last_confirmed_at',STAMP),
 'version':('observed_ha_version','synthetic-version'),'history':('binding_history',[]),
 'unknown':('unknown',True),'nested_area':('has_area_candidate',{'area_id':'private'}),
 'area_int':('has_area_candidate',1),'domains_unsorted':('integration_domains',['zha','mqtt']),
 'domains_duplicate':('integration_domains',['mqtt','mqtt']),
 'domain_url':('integration_domains',['https://private']),
 'domain_ip':('integration_domains',['192.168.2.3']),
 'domain_mac':('integration_domains',['aa:bb:cc:dd:ee:ff']),
 'domain_compact_mac':('integration_domains',['deadbeefcafe']),
 'domain_hostname':('integration_domains',['private.local']),
 'domain_control':('integration_domains',['mqtt\n']),
 'domain_namespace_object':('integration_domains',[{'private':'mqtt'}]),
 'entity_nonfinite':('entity_count',float('nan')),
}
for name,(field,value) in PUBLIC_REJECTS.items():
    setattr(PreparationFixtureTests,'test_public_reject_'+name,public_reject_case(field,value))


def read_reject_case(key):
    def test(self):self.assertFalse(specification_read_condition(**{key:False}))
    return test
for key in ['lock_exists','shared_lock_available','regular_file','pinned_no_symlink','owner_group_mode_acl_valid','link_count_one','namespace_clean_before','namespace_clean_after','size_bounded','complete_read','file_fingerprint_unchanged','parent_and_lock_binding_unchanged','deadline_within_budget']:
    setattr(PreparationFixtureTests,'test_read_omit_'+key,read_reject_case(key))

if __name__ == '__main__':
    unittest.main()
