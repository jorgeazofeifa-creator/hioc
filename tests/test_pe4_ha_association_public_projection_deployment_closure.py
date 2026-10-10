"""Repository-only closure proof; sanitized operator evidence, no native execution."""
import ast,copy,hashlib,json,re,subprocess,unittest
from pathlib import Path
from datetime import datetime
from test_pe4_ha_association_deployment_closure import validate,canonical
from test_pe4_ha_association_public_projection_test_binding_correction import current_index,validate_closure_successor,closure_master_section,CORRECTION_COMMIT
ROOT=Path(__file__).resolve().parents[1]
HISTORICAL_PRODUCTION_SOURCE='c7db29f795909d7926e36c02f1166034bcebb8b0'
CLOSURE_PREDECESSOR=CORRECTION_COMMIT
P=ROOT/'governance/pe4/pe4-ha-association-public-projection-deployment-closure.json'
R=json.loads(current_index(str(P.relative_to(ROOT)).replace('\\','/')));S=json.loads(current_index(str(P.with_suffix('.schema.json').relative_to(ROOT)).replace('\\','/')))
class PublicProjectionClosureTests(unittest.TestCase):
 def test_predecessor_exact(self):
  self.assertEqual(R['predecessor_commit'],CLOSURE_PREDECESSOR)
  for fmt,key in [('%s','predecessor_subject'),('%P','predecessor_parent')]:
   self.assertEqual(subprocess.check_output(['git','show','-s','--format='+fmt,CLOSURE_PREDECESSOR],cwd=ROOT).decode().strip(),R[key])
 def test_closed_canonical_schema(self):
  validate_closure_successor(R,S);self.assertEqual(current_index(str(P.relative_to(ROOT)).replace('\\','/')),canonical(R));self.assertEqual(current_index(str(P.with_suffix('.schema.json').relative_to(ROOT)).replace('\\','/')),canonical(S))
  def visit(v,s):
   if type(v) is dict:
    with self.assertRaises(ValueError):validate(dict(v,unreviewed=True),s)
    for k,x in v.items():visit(x,s['properties'][k])
   elif type(v) is list:
    with self.assertRaises(ValueError):validate(v+[None],s)
    for x,n in zip(v,s['prefixItems']):visit(x,n)
   else:
    with self.assertRaises(ValueError):validate({'fabricated':True},s)
  visit(R,S)
 def test_historical_sources_and_runtime_immutable(self):
  for i in R['sources']:
   raw=subprocess.check_output(['git','show',i['commit']+':'+i['path']],cwd=ROOT)
   self.assertEqual(hashlib.sha256(raw).hexdigest(),i['sha256']);self.assertEqual(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),i['git_blob'])
  for i in R['protected_sources']:
   self.assertEqual((ROOT/i['path']).read_bytes().replace(b'\r\n',b'\n'),subprocess.check_output(['git','show',HISTORICAL_PRODUCTION_SOURCE+':'+i['path']],cwd=ROOT))
  self.assertEqual(subprocess.check_output(['git','diff','--name-only',HISTORICAL_PRODUCTION_SOURCE,'--','pi4','release','tools','requirements-pe4.lock'],cwd=ROOT),b'')
 def test_specific_repository_prerequisite_closures(self):
  expected=[
   ('pe4-0b2a-execution-closure.json','lifecycle_state','PASS_CLOSED'),
   ('pe4-0b2b-execution-closure.json','lifecycle_state','PASS_CLOSED'),
   ('pe4-0c-association-contract.json','lifecycle_state','PASS_CLOSED'),
   ('pe4-0c1-association-lifecycle-clarification.json','lifecycle_state','PASS_CLOSED'),
   ('pe4-ha-runtime-credential-provisioning-closure.json','status','PASS_CLOSED'),
   ('pe4-ha-association-adapter-implementation.json','status','PASS_CLOSED'),
   ('pe4-ha-association-adapter-deployment-closure.json','status','PASS_CLOSED'),
   ('pe4-ha-association-durable-post-run-reconciliation-closure.json','status','PASS_CLOSED'),
   ('pe4-ha-association-independent-production-acceptance-closure.json','status','PASS_CLOSED'),
   ('pe4-ha-association-scheduler-deployment-closure.json','status','PASS_CLOSED'),
   ('pe4-ha-association-public-projection-preparation.json','status','PASS_CLOSED'),
   ('pe4-ha-association-public-projection-deployment-baseline-correction.json','status','PASS/CLOSED'),
   ('pe4-ha-association-public-projection-test-binding-correction.json','status','PASS_CLOSED')]
  for name,key,state in expected:
   authority=CLOSURE_PREDECESSOR if name=='pe4-ha-association-public-projection-test-binding-correction.json' else HISTORICAL_PRODUCTION_SOURCE
   raw=subprocess.check_output(['git','show',authority+':governance/pe4/'+name],cwd=ROOT)
   self.assertEqual(json.loads(raw)[key],state)
   self.assertIn('governance/pe4/'+name,[i['path'] for i in R['sources']])
  self.assertTrue(all(v is False for v in R['upgrade_authorizations'].values()))
 def test_historical_chronology_preserved(self):
  old=subprocess.check_output(['git','show',HISTORICAL_PRODUCTION_SOURCE+':docs/HIOC_MASTER_PLAN.md'],cwd=ROOT).decode()
  now=(ROOT/'docs/HIOC_MASTER_PLAN.md').read_text(encoding='utf8')
  for start,end in [('# Historical Checkpoint Chronology','# Implementation Status'),('# Historical Operator Preparation Chronology',None)]:
   a=old.split(start,1)[1];b=now.split(start,1)[1]
   if end:a=a.split(end,1)[0];b=b.split(end,1)[0]
   self.assertEqual(a,b)
 def test_no_raw_production_content(self):
  forbidden={'device_id','mac','ip_address','entity_id','ha_device_id','config_entry_id','credential_value','raw_inventory','raw_mqtt_payload','raw_private_state','receipt_bytes','MQTT_PASSWORD'}
  def walk(v):
   if type(v) is dict:
    self.assertFalse(forbidden.intersection(v))
    for x in v.values():walk(x)
   elif type(v) is list:
    for x in v:walk(x)
  walk(R)
 def test_current_artifacts_bound(self):
  expected={i['path'] for i in R['artifacts']}|{str(P.relative_to(ROOT)).replace('\\','/'),str(P.with_suffix('.schema.json').relative_to(ROOT)).replace('\\','/')}
  changed=set(subprocess.check_output(['git','diff','--name-only',CLOSURE_PREDECESSOR],cwd=ROOT).decode().splitlines())
  changed.update(subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=ROOT).decode().splitlines())
  self.assertEqual(changed,expected)
  for i in R['artifacts']:
   raw=current_index(i['path'])
   self.assertEqual(hashlib.sha256(raw).hexdigest(),i['sha256']);self.assertEqual(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),i['git_blob'])
 def test_attempt_one_exact_immutable(self):
  old=json.loads(subprocess.check_output(['git','show',HISTORICAL_PRODUCTION_SOURCE+':governance/pe4/pe4-ha-association-public-projection-deployment-baseline-correction.json'],cwd=ROOT))
  self.assertEqual(R['baseline_attempt_1'],old['baseline_attempt_1']);self.assertEqual(R['law'],old['law'])
 def test_provenance_and_scoped_actions(self):
  for k in ['source_sync','independent_source_review','corrected_baseline','baseline_receipt','deployment','installed_review','pre_slot','natural_cycle','mqtt_acceptance']:
   self.assertEqual(R[k]['provenance'],'OPERATOR_SUPPLIED')
  self.assertFalse(R['codex_production_observation']);self.assertTrue(all(v is False for v in R['codex_activity'].values()))
  self.assertFalse(R['deployment']['sanitized_result']['MQTT_PUBLISHED']);self.assertFalse(R['mqtt_acceptance']['observer_activity']['mqtt_published'])
  self.assertEqual(R['mqtt_acceptance']['result'],'PASS')
 def test_receipt_sanitized_no_reconstruction(self):
  a=R['baseline_receipt'];self.assertFalse(a['contents_committed']);self.assertFalse(a['contents_reconstructed'])
  self.assertEqual(set(a),{'provenance','status','sha256','size','uid','gid','mode','links','type','canonical_json','outer_contract','baseline_v2_contract','bytes_match_accepted_baseline','independent_sha256_match','contents_committed','contents_reconstructed'})
 def test_natural_slot_and_postdeploy_write(self):
  n=R['natural_cycle'];self.assertGreater(n['inventory_mtime_ns'],n['engine_mtime_ns'])
  inv=datetime.fromisoformat(n['inventory_updated']);cron=datetime.fromisoformat(n['cron_timestamp_utc']);status=datetime.fromisoformat(n['status_updated'])
  self.assertIn(inv.minute,(0,30));self.assertLess(cron,inv);self.assertLess(inv,status);self.assertLess((inv-cron).total_seconds(),3)
  self.assertTrue(all(v==0 and type(v)is int for v in n['contract_failures'].values()))
  self.assertEqual(n['projection_fields'],['associated','association_basis','entity_count','integration_domains','has_area_candidate'])
 def test_mqtt_source_semantics(self):
  p=ROOT/R['backport']['path'];text=p.read_text(encoding='utf8');tree=ast.parse(text)
  self.assertIn('return 0\n        log.info("inventory updated',text)
  self.assertIn('status["status"] = "degraded"',text);self.assertIn('status["publish_errors"] = [str(exc)]',text)
  topics=[n.value for n in ast.walk(tree) if isinstance(n,ast.Constant) and isinstance(n.value,str) and n.value.startswith('/inventory')]
  self.assertEqual(set(topics),{'/'+x for x in R['mqtt_source_semantics']['topics']})
  raw=subprocess.check_output(['git','show','29737ee97899bf06be09df661725c8186a7c339f:pi4/lib/hioc/mqtt.py'],cwd=ROOT).decode()
  self.assertIn('def publish(self, topic: str, payload, retain: bool = True)',raw);self.assertIn('header = 0x31 if retain else 0x30',raw)
 def test_mqtt_observation_equality_chain(self):
  a=R['mqtt_acceptance'];n=R['natural_cycle']
  self.assertEqual(a['inventory_updated'],a['broker_inventory_updated']);self.assertEqual(a['inventory_updated'],n['inventory_updated'])
  self.assertEqual(a['public_projection_count'],a['broker_public_projection_count']);self.assertEqual(a['public_projection_count'],n['public_projection_device_count'])
  self.assertEqual(a['expected_retained_topic_count'],a['observed_retained_topic_count'])
  self.assertTrue(a['observer_activity']['credential_accessed']);self.assertFalse(a['observer_activity']['credential_value_exposed'])
 def test_pe4_audit_complete_authority(self):
  a=R['pe4_completion_audit'];self.assertEqual(a['remaining_mandatory_prerequisites'],[]);self.assertTrue(a['all_required_closed'])
  old=subprocess.check_output(['git','show',HISTORICAL_PRODUCTION_SOURCE+':docs/HIOC_MASTER_PLAN.md'],cwd=ROOT).decode()
  self.assertIn('PE-4 NOT COMPLETE because its separately deferred public projection\ncheckpoint remains',old)
  prior=old.split('## Authoritative Current PE-4 Lifecycle',1)[1].split('### Completed',1)[0]
  rows=set(re.findall(r'^\| ([^|]+) \| ([^|]+) \|$',prior,re.M))-{('Checkpoint','Current state'),('---','---')}
  self.assertTrue(rows<={(i['checkpoint'],i['prior_status']) for i in a['prerequisites']})
  for i in a['prerequisites']:
   if i['classification']=='MANDATORY_PREREQUISITE':self.assertTrue('PASS' in i['current_status'] or i['current_status'] in ('ACCEPTED','COMPLETE','CORRECTED IN REPOSITORY'),i)
  self.assertIn('**PE-5 - MQTT and Passive Service Association** — not started.',old)
 def test_document_evidence_report(self):
  text=(ROOT/'docs/PE4_HOME_ASSISTANT_ASSOCIATION_PUBLIC_PROJECTION_DEPLOYMENT_CLOSURE.md').read_text(encoding='utf8')
  for x in ['Deployment Result','Intended Behavior','Invariant Checks','Production Execution Evidence','MQTT Acceptance Evidence','Warnings / Limitations','Lifecycle Result','PASS / FAIL','OPERATOR_SUPPLIED','NOT_PROVEN/CORRECT_GATE_BEHAVIOR','credential accessed TRUE','observer published FALSE','NOT_OBSERVED_BY_DESIGN']:self.assertIn(x,text)
 def test_master_current_lifecycle(self):
  t=(ROOT/'docs/HIOC_MASTER_PLAN.md').read_text(encoding='utf8');current=closure_master_section(t)
  for x in ['PUBLIC_PROJECTION=PASS/CLOSED','PE4=PASS/CLOSED','OPERATOR_SUPPLIED','Phase 7A ACTIVE','PE-5 NOT_STARTED','014a901a56ebc613b2235ad434ae124024ae6e01e8e1960ce98e7df6709e9944']:self.assertIn(x,current)
  self.assertIn('### PE-5 - MQTT and Passive Service Association',t.split('## Next Planned Task',1)[1])
  self.assertIn('NO ASSUMPTIONS. NO EXCEPTIONS.',t)
 def test_historical_master_occurrence_cannot_satisfy_current(self):
  text=(ROOT/'docs/HIOC_MASTER_PLAN.md').read_text(encoding='utf8')
  section=closure_master_section(text)
  altered=text.replace(section,'\nNO CURRENT CLOSURE EVIDENCE\n',1)+'\n## Historical closure evidence\n'+section
  with self.assertRaises(ValueError):closure_master_section(altered)

CHECKS={
'binding_correction_commit':(('binding_correction_commit',),CORRECTION_COMMIT),
'binding_correction_status':(('binding_correction_status',),'PASS_CLOSED'),
'corrected_baseline':(('corrected_baseline','result'),'PASS'),
'receipt_hash':(('baseline_receipt','sha256'),'014a901a56ebc613b2235ad434ae124024ae6e01e8e1960ce98e7df6709e9944'),
'deploy_result':(('deployment','sanitized_result','RESULT'),'PASS'),
'deploy_mutation':(('deployment','sanitized_result','MUTATION_STATE'),'VERIFIED_DEPLOYED'),
'installed':(('installed_review','sanitized_result','RESULT'),'PASS'),
'pre_slot':(('pre_slot','natural_cycle_observation'),'NOT_PROVEN'),
'pre_slot_failure':(('pre_slot','failure'),False),
'natural_pass':(('natural_cycle','result'),'PASS'),
'inventory_timestamp':(('natural_cycle','inventory_updated'),'2026-10-09T16:30:02-06:00'),
'status_timestamp':(('natural_cycle','status_updated'),'2026-10-09T16:30:03-06:00'),
'cron_observed':(('natural_cycle','natural_cron_invocation_observed'),True),
'cron_timestamp':(('natural_cycle','cron_timestamp_utc'),'2026-10-09T22:30:01.240256+00:00'),
'devices':(('natural_cycle','device_count'),186),
'projections':(('natural_cycle','public_projection_device_count'),25),
'mqtt':(('mqtt_acceptance','result'),'PASS'),
'mqtt_topics':(('mqtt_acceptance','observed_retained_topic_count'),7),
'mqtt_equality':(('mqtt_acceptance','retained_payloads_match_local_state'),'PASS'),
'mqtt_observer_published':(('mqtt_acceptance','observer_activity','mqtt_published'),False),
'mqtt_credential_accessed':(('mqtt_acceptance','observer_activity','credential_accessed'),True),
'mqtt_credential_exposed':(('mqtt_acceptance','observer_activity','credential_value_exposed'),False),
'rollback':(('lifecycle','rollback'),'NOT_PERFORMED'),
'manual_second':(('lifecycle','manual_second_adapter_execution'),'NOT_AUTHORIZED/NOT_PERFORMED'),
'phase_active':(('lifecycle','phase7a'),'ACTIVE'),
'pe5_not_started':(('lifecycle','pe5'),'NOT_STARTED'),
'pe4_closed':(('lifecycle','pe4'),'PASS/CLOSED'),
'projection_closed':(('lifecycle','public_projection'),'PASS/CLOSED')}
for name,(path,expected) in CHECKS.items():
 def test(self,path=path,expected=expected):
  v=R
  for k in path:v=v[k]
  self.assertEqual(v,expected);self.assertIs(type(v),type(expected))
  bad=copy.deepcopy(R);v=bad
  for k in path[:-1]:v=v[k]
  v[path[-1]]=None
  with self.assertRaises(ValueError):validate(bad,S)
 setattr(PublicProjectionClosureTests,'test_exact_'+name,test)
if __name__=='__main__':unittest.main()
