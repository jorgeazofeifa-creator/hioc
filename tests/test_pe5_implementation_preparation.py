"""PE-5 preparation successor: repository-only governance, never runtime execution."""
import ast
import copy
import hashlib
import json
import os
import re
import subprocess
import unittest
from functools import lru_cache
from contextlib import contextmanager
from unittest.mock import patch
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PREDECESSOR='6f69c4dfb85924a83b59e85ef2da602fc75ec5ea'
ACCEPTED_PREPARATION='f3730ba5a8745361934ff822a9c29c16c9d0767b'
RECORD='governance/pe5/pe5-implementation-preparation.json'
SCHEMA=RECORD.replace('.json','.schema.json')
MASTER='docs/HIOC_MASTER_PLAN.md'
ARCHITECTURE='docs/PASSIVE_ENRICHMENT_ARCHITECTURE.md'
DOCUMENT='docs/PE5_IMPLEMENTATION_PREPARATION.md'
SELF='tests/test_pe5_implementation_preparation.py'
HISTORICAL_TEST='tests/test_pe10_surveillance_roadmap_preservation.py'
BINDING_TEST='tests/test_pe4_ha_association_public_projection_test_binding_correction.py'
CLOSURE_TEST='tests/test_pe4_documentation_consistency_correction_closure.py'
SEQUENCING_TESTS=['tests/test_compatibility_master_plan_governance.py','tests/test_pe4_0b2b_execution_closure.py','tests/test_pe4_0c_association_contract.py','tests/test_pe4_0c1_association_lifecycle.py']
CANDIDATE_PATHS=tuple(sorted([MASTER,ARCHITECTURE,DOCUMENT,RECORD,SCHEMA,SELF,HISTORICAL_TEST,BINDING_TEST,CLOSURE_TEST,*SEQUENCING_TESTS]))
DECISION='if everything related to P4-4 and everything before it is completed successfully and documented, then start with PE-5.'
FIRST='PE-5.1 - Private Local Service Association Contract and Pure Resolver'
TITLE='PE-5 implementation preparation'
ORIGINAL_SPECIFICATION_SHA256='55b564f68e0116beeab54199659c8c8a1a601e86f2f420dcf7d903acb1191e24'
FUTURE_PATHS=['pi4/lib/hioc/service_association.py','governance/pe5/pe5-local-service-association-envelope.schema.json','tests/test_pe5_local_service_association.py']
PROTECTED_FIELDS=['id','mac','ip','first_seen','last_seen','health','expected_availability','monitoring','incidents','dhcp_provenance','neighbor_observations','asset_metadata','home_assistant','public_mqtt_contract','history','retention','dependency_graph']
LIFECYCLE=dict(phase7a='ACTIVE',pe4='PASS/CLOSED',public_projection='PASS/CLOSED',documentation_consistency_correction='PASS/CLOSED',pe5_runtime='NOT_STARTED',pe5_preparation='PREPARED_FOR_REVIEW',surveillance='PLANNED_NOT_STARTED')
BOUNDARIES=['pure_resolver','finalized_inventory_only','existing_mac_backed_owner_only','reuse_inventory_identity_semantics','explicit_evaluation_time_and_age_policy','no_per_service_timestamp_fabrication','duplicate_determinism','conflicts_rejected','closed_private_output','safe_rejections','no_health_or_availability_inference','input_immutable','no_import_time_io','no_current_history_mixing','no_heuristic_dependency_authority','separate_implementation_authorization','separate_production_authorization']
ACTIVITY=['runtime_implementation','production_access','production_mutation','pi3_access','pi5_access','mqtt_connect','mqtt_publish','mqtt_subscribe','active_discovery','surveillance_implementation','new_devices','identity_changes','canonical_ip_changes','liveness_changes','health_changes','asset_changes','new_public_topics','persistence','scheduler_changes']

def git(*args):
 return subprocess.check_output(['git','--no-optional-locks',*args],cwd=ROOT,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
def digest(raw):return hashlib.sha256(raw).hexdigest()
def blob(raw):return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def canonical(value):return (json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False)+'\n').encode()
def current_bytes(path):return (ROOT/path).read_bytes().replace(b'\r\n',b'\n')
def require(value,message):
 if not value:raise ValueError(message)
def closed(value):
 if type(value) is dict:return dict(type='object',additionalProperties=False,required=sorted(value),properties={k:closed(v) for k,v in sorted(value.items())})
 if type(value) is list:return dict(type='array',minItems=len(value),maxItems=len(value),prefixItems=[closed(v) for v in value],items=False)
 return dict(const=value)
def schema_for(record):return {'$schema':'https://json-schema.org/draft/2020-12/schema','title':TITLE,**closed(record)}
def validate_identity(item,raw):
 require(set(item)=={'path','sha256','git_blob'},'identity fields changed')
 require(digest(raw)==item['sha256'] and blob(raw)==item['git_blob'],'artifact identity mismatch: '+item['path'])

def _validate_historical_preparation(record,schema):
 require(canonical(schema)==canonical(schema_for(record)),'exact typed preparation schema mismatch')
 require(record['predecessor_commit']==PREDECESSOR and record['authorized_paths']==list(CANDIDATE_PATHS),'wrong preparation scope')
 require(record['executive_decision']==DECISION,'executive decision changed')
 require(record['current_next_task']=='PE5_IMPLEMENTATION_PREPARATION' and record['pe5_selected_as_next_checkpoint'] is True,'wrong current sequence')
 require(record['preparation_authorized'] is True and record['runtime_implementation_authorized'] is False,'preparation/runtime authority conflated')
 require(record['status']=='PREPARED_FOR_REVIEW' and record['lifecycle']==LIFECYCLE,'preparation lifecycle changed')
 require(record['implementation_activity']==dict.fromkeys(ACTIVITY,False),'forbidden implementation authority')
 require(record['protected_fields']==PROTECTED_FIELDS,'protected identity or consumer field omitted')
 require(record['first_checkpoint']==FIRST and record['future_implementation_paths']==FUTURE_PATHS,'first checkpoint changed')
 require(record['first_checkpoint_boundaries']==dict.fromkeys(BOUNDARIES,True),'first checkpoint safety boundary weakened')
 require(record['eligible_first_sources']==['systemd','ss'],'new source authority introduced')
 require(record['production_facts_status']=='UNKNOWN_NOT_OBSERVED' and record['maximum_snapshot_age_seconds']=='UNKNOWN_REQUIRES_SEPARATE_EVIDENCE','production facts or freshness guessed')
 require(record['production_validation_status']=='NOT_PERFORMED_NOT_AUTHORIZED','production validation claimed')
 require(record['historical_unknown_preserved'] is True and record['completed_checkpoints_reopened']==[],'history or closure changed')
 require(not git('diff','--cached','--name-only'),'preparation candidate must remain unstaged')
 require(not git('stash','list'),'unexpected stash')
 require(git('branch','--show-current').decode().strip()=='main','wrong branch')
 head=git('rev-parse','HEAD').decode().strip()
 if head==PREDECESSOR:
  require(git('rev-parse','origin/main').decode().strip()==PREDECESSOR,'baseline tracking ref changed')
  changed=set(git('diff','--name-only',PREDECESSOR).decode().splitlines())
  changed.update(git('ls-files','--others','--exclude-standard').decode().splitlines())
 else:
  require(git('rev-parse','HEAD^').decode().strip()==PREDECESSOR and not git('status','--porcelain'),'wrong committed successor')
  changed=set(git('diff','--name-only',PREDECESSOR,head).decode().splitlines())
 require(changed==set(CANDIDATE_PATHS),'unexpected preparation mutation')
 require({x['path'] for x in record['artifacts']}==set(CANDIDATE_PATHS)-{RECORD,SCHEMA} and len(record['artifacts'])==len(CANDIDATE_PATHS)-2,'current map incomplete or duplicate')
 for item in record['artifacts']:validate_identity(item,current_bytes(item['path']))
 for item in record['source_bindings']:
  validate_identity(item,git('show',PREDECESSOR+':'+item['path']))
  if item['path'] not in CANDIDATE_PATHS:require(current_bytes(item['path'])==git('show',PREDECESSOR+':'+item['path']),'source or runtime artifact changed')
 for item in record['historical_artifacts']:
  validate_identity(item,git('show',PREDECESSOR+':'+item['path']))
  require(current_bytes(item['path'])==git('show',PREDECESSOR+':'+item['path']),'historical package rewritten')
 old=git('show',PREDECESSOR+':'+MASTER).decode().splitlines(keepends=True);candidate=list(old)
 require(len(record['master_insertions'])==6,'unexpected Master mutation shape')
 for ins in sorted(record['master_insertions'],key=lambda x:x['after_line'],reverse=True):
  require(digest(old[ins['after_line']-1].rstrip('\n').encode())==ins['anchor_sha256'],'Master insertion anchor mismatch')
  candidate[ins['after_line']:ins['after_line']]=[ins['text']+'\n']
 require(''.join(candidate).encode()==current_bytes(MASTER),'existing Master content changed')
 edit=record['architecture_gate_edit'];old_arch=git('show',PREDECESSOR+':'+ARCHITECTURE).decode()
 require(old_arch.count(edit['historical_text'])==1 and old_arch.replace(edit['historical_text'],edit['current_text']).encode()==current_bytes(ARCHITECTURE),'unrelated architecture change')
 master=current_bytes(MASTER).decode();doc=current_bytes(DOCUMENT).decode()
 for marker in ['## Current Objective','## Next Planned Task']:
  section=master.split(marker,1)[1].split('### Historical',1)[0]
  require(section.strip().startswith(('**PE-5 - MQTT and Passive Service Association: Implementation Preparation**','### PE-5 Implementation Preparation')) and 'Post-closure next task: UNKNOWN' not in section,'current UNKNOWN or missing preparation')
  for phrase in ['PE-4 PASS/CLOSED','Public Projection PASS/CLOSED','Phase 7A ACTIVE','NOT_STARTED','NOT AUTHORIZED']:
   require(phrase in section,'current lifecycle or runtime gate missing: '+phrase)
 require(DECISION in master.split('# Decision Log',1)[1] and DECISION in master.split('## Current Objective',1)[1].split('### Historical',1)[0] and DECISION in doc,'executive wording missing')
 require('UNKNOWN / NOT YET AUTHORIZED' in master.split('### Historical',1)[1],'historical UNKNOWN removed')
 source=master.split('<!-- ORIGINAL_SURVEILLANCE_SPECIFICATION_BEGIN -->\n```text\n',1)[1].split('```\n<!-- ORIGINAL_SURVEILLANCE_SPECIFICATION_END -->',1)[0]
 require(digest(source.encode())==ORIGINAL_SPECIFICATION_SHA256,'original surveillance specification changed')
 require(master.count('##### Surveillance checkpoint ')==6,'surveillance roadmap changed')
 require('Status: **PLANNED / NOT STARTED — IMPLEMENTATION NOT AUTHORIZED**' in master,'surveillance status changed')
 require([item['path'] for item in record['current_sequencing_tests']]==SEQUENCING_TESTS,'current sequencing consumer set changed')
 for item in record['current_sequencing_tests']:
  historical=git('show',PREDECESSOR+':'+item['path']).decode()
  require(historical.count(item['historical_assertion'])==1,'historical sequencing assertion missing')
  require(historical.replace(item['historical_assertion'],item['current_assertion']).encode()==current_bytes(item['path']),'unrelated current-consumer assertion changed')
 # Preserve the accepted PE-10 law body exactly; only its authority wrapper changes.
 old_test=ast.parse(git('show',PREDECESSOR+':'+HISTORICAL_TEST));new_test=ast.parse(current_bytes(HISTORICAL_TEST))
 a=next(x for x in old_test.body if isinstance(x,ast.FunctionDef) and x.name=='validate_record')
 b=next(x for x in new_test.body if isinstance(x,ast.FunctionDef) and x.name=='_validate_historical_roadmap')
 require([ast.dump(x,include_attributes=False) for x in a.body]==[ast.dump(x,include_attributes=False) for x in b.body],'historical surveillance law weakened')
 old_closure=ast.parse(git('show',PREDECESSOR+':'+CLOSURE_TEST));new_closure=ast.parse(current_bytes(CLOSURE_TEST))
 a=next(x for x in old_closure.body if isinstance(x,ast.FunctionDef) and x.name=='_validate_historical_closure')
 b=next(x for x in new_closure.body if isinstance(x,ast.FunctionDef) and x.name=='_validate_historical_closure')
 require([ast.dump(x,include_attributes=False) for x in a.body]==[ast.dump(x,include_attributes=False) for x in b.body],'historical documentation closure law weakened')
 for phrase in record['required_preparation_phrases']:require(phrase in doc,'preparation requirement absent: '+phrase)
 return record

def historical_bytes(path):
 return git('show',ACCEPTED_PREPARATION+':'+path)

@contextmanager
def accepted_preparation_context():
 original_git=git
 def accepted_git(*args):
  if args==('rev-parse','HEAD'):return (ACCEPTED_PREPARATION+'\n').encode()
  if args==('rev-parse','HEAD^'):return (PREDECESSOR+'\n').encode()
  if args in [('status','--porcelain'),('diff','--cached','--name-only'),('stash','list')]:return b''
  return original_git(*args)
 with patch.dict(globals(),git=accepted_git,current_bytes=historical_bytes):yield

def validate_record(record,schema):
 with accepted_preparation_context():return _validate_historical_preparation(record,schema)

@lru_cache(maxsize=1)
def successor():
 raw=historical_bytes(RECORD);schema_raw=historical_bytes(SCHEMA);record=json.loads(raw);schema=json.loads(schema_raw)
 require(raw==canonical(record) and schema_raw==canonical(schema),'noncanonical preparation contract')
 return validate_record(record,schema)
def current_binding(path):
 from test_pe5_service_association_caller import CALLER_PATHS, caller_current_binding
 if path in CALLER_PATHS:return caller_current_binding(path)
 from test_pe5_local_service_association import IMPLEMENTATION_PATHS, implementation_current_binding
 if path in IMPLEMENTATION_PATHS:return implementation_current_binding(path)
 record=successor();item=next((x for x in record['artifacts'] if x['path']==path),None)
 require(item is not None,'path outside preparation current map');validate_identity(item,current_bytes(path));return item

def _assert_historical_preparation_sequence(text):
 # Current sequencing follows executive authority; the accepted UNKNOWN snapshot remains immutable.
 current_binding(MASTER)
 current=text.split('## Next Planned Task',1)[1].split('### Historical',1)[0]
 require(current.strip().startswith('### PE-5 Implementation Preparation'),'current preparation pointer missing')
 require('NOT_STARTED' in current and 'NOT AUTHORIZED' in current,'runtime gate missing')
 accepted=git('show',PREDECESSOR+':'+MASTER).decode().split('## Next Planned Task',1)[1]
 require(accepted.strip().startswith('### Post-Closure Next Task — UNKNOWN / NOT YET AUTHORIZED'),'historical UNKNOWN authority changed')
 require('### Historical post-closure next-task snapshot at '+PREDECESSOR in text and '### Post-Closure Next Task — UNKNOWN / NOT YET AUTHORIZED' in text,'historical UNKNOWN snapshot removed')

def assert_current_sequence(text):
 from test_pe5_local_service_association import assert_implementation_sequence
 return assert_implementation_sequence(text)

class PE5ImplementationPreparationTests(unittest.TestCase):
 def test_exact_preparation_contract_and_current_bindings(self):successor()
 def test_historical_unknown_retained_with_current_authority(self):
  r=successor();self.assertTrue(r['historical_unknown_preserved']);self.assertEqual(r['current_next_task'],'PE5_IMPLEMENTATION_PREPARATION')
 def test_runtime_and_future_work_remain_unauthorized(self):
  r=successor();self.assertFalse(r['runtime_implementation_authorized']);self.assertTrue(all(v is False for v in r['implementation_activity'].values()))
  for path in FUTURE_PATHS:
   result=subprocess.run(['git','cat-file','-e',ACCEPTED_PREPARATION+':'+path],cwd=ROOT,capture_output=True)
   self.assertNotEqual(result.returncode,0)
 def test_completed_packages_and_source_identities_preserved(self):
  for item in successor()['historical_artifacts']:validate_identity(item,current_bytes(item['path']))
 def test_publication_mapping_and_weak_identity_not_first_stage(self):
  r=successor();self.assertEqual(r['eligible_first_sources'],['systemd','ss']);self.assertTrue(r['first_checkpoint_boundaries']['existing_mac_backed_owner_only'])
  self.assertFalse(r['implementation_activity']['mqtt_subscribe']);self.assertFalse(r['implementation_activity']['new_public_topics'])
 def test_reject_runtime_production_active_and_surveillance_authority(self):
  for key in ACTIVITY:
   bad=copy.deepcopy(successor());bad['implementation_activity'][key]=True
   with self.subTest(key=key),self.assertRaises(ValueError):validate_record(bad,schema_for(bad))
  bad=copy.deepcopy(successor());bad['runtime_implementation_authorized']=True
  with self.assertRaises(ValueError):validate_record(bad,schema_for(bad))
 def test_reject_unknown_next_task_or_reopened_checkpoint(self):
  for key,value in [('current_next_task','UNKNOWN_NOT_YET_AUTHORIZED'),('completed_checkpoints_reopened',['PE4']),('executive_decision',DECISION.replace('P4-4','PE-4'))]:
   bad=copy.deepcopy(successor());bad[key]=value
   with self.subTest(key=key),self.assertRaises(ValueError):validate_record(bad,schema_for(bad))
 def test_reject_weakened_identity_and_safety_gates(self):
  for key in BOUNDARIES:
   bad=copy.deepcopy(successor());bad['first_checkpoint_boundaries'][key]=False
   with self.subTest(key=key),self.assertRaises(ValueError):validate_record(bad,schema_for(bad))
  bad=copy.deepcopy(successor());bad['protected_fields'].remove('ip')
  with self.assertRaises(ValueError):validate_record(bad,schema_for(bad))
 def test_reject_invented_source_freshness_or_production_proof(self):
  for key,value in [('eligible_first_sources',['systemd','ss','mqtt_discovery']),('maximum_snapshot_age_seconds',300),('production_validation_status','PASS')]:
   bad=copy.deepcopy(successor());bad[key]=value
   with self.subTest(key=key),self.assertRaises(ValueError):validate_record(bad,schema_for(bad))
 def test_reject_extra_scope_and_identity_mismatch(self):
  bad=copy.deepcopy(successor());bad['authorized_paths'].append('pi4/lib/hioc/unapproved.py')
  with self.assertRaises(ValueError):validate_record(bad,schema_for(bad))
  bad=copy.deepcopy(successor());bad['artifacts'][0]['sha256']='0'*64
  with self.assertRaises(ValueError):validate_record(bad,schema_for(bad))
 def test_reject_open_or_stale_schema(self):
  r=successor();s=schema_for(r);s['additionalProperties']=True
  with self.assertRaises(ValueError):validate_record(r,s)
  s=schema_for(r);s['properties']['runtime_implementation_authorized']['const']=True
  with self.assertRaises(ValueError):validate_record(r,s)
 def test_reject_unrelated_master_mutation(self):
  from unittest.mock import patch
  reader=historical_bytes
  def altered(path):return reader(path)+b'UNRELATED CHANGE\n' if path==MASTER else reader(path)
  with patch.dict(globals(),historical_bytes=altered),self.assertRaises(ValueError):validate_record(successor(),schema_for(successor()))

if __name__=='__main__':unittest.main()
