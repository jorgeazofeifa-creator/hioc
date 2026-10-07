"""Repository-only closure contracts; operator observations are never collected here."""
import copy,hashlib,json,re,subprocess,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE='4912f20d8b2ff78dcdaf8b3e0f52e57d5de5e3a2'
NEXT='PE-4 Home Assistant Association Adapter Bounded Manual Production Validation'
RECORD=ROOT/'governance/pe4/pe4-ha-association-adapter-deployment-closure.json'
R=json.loads(RECORD.read_bytes());S=json.loads(RECORD.with_suffix('.schema.json').read_bytes())
def canonical(value):return (json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False)+'\n').encode()
def validate(value,node):
 if 'const' in node:
  if type(value)!=type(node['const']) or value!=node['const']:raise ValueError('constant mismatch')
  return
 if node['type']=='object':
  if type(value)!=dict or node['additionalProperties'] is not False or set(value)!=set(node['required']) or set(value)!=set(node['properties']):raise ValueError('closed object mismatch')
  for key,child in node['properties'].items():validate(value[key],child)
 else:
  if type(value)!=list or node['items'] is not False or len(value)!=node['minItems'] or len(value)!=node['maxItems'] or len(value)!=len(node['prefixItems']):raise ValueError('closed array mismatch')
  for item,child in zip(value,node['prefixItems']):validate(item,child)
class DeploymentClosureTests(unittest.TestCase):
 def reject(self,key,value):
  bad=copy.deepcopy(R);bad[key]=value
  with self.assertRaises(ValueError):validate(bad,S)
 def test_canonical_record_and_closed_schema(self):
  validate(R,S);self.assertEqual(RECORD.read_bytes(),canonical(R));self.assertEqual(RECORD.with_suffix('.schema.json').read_bytes(),canonical(S));self.assertEqual(R['status'],'PASS_CLOSED')
 def test_additional_properties_rejected_at_every_object(self):
  def visit(value,node):
   if isinstance(value,dict):
    bad=copy.deepcopy(value);bad['unreviewed_extra']=True
    with self.assertRaises(ValueError):validate(bad,node)
    for key,child in node['properties'].items():visit(value[key],child)
   elif isinstance(value,list):
    for item,child in zip(value,node['prefixItems']):visit(item,child)
  visit(R,S)
 def test_operator_provenance_cannot_be_codex_observed(self):
  self.reject('operator_evidence_provenance','CODEX_OBSERVED')
  for name in ('deployment_evidence','static_acceptance_evidence'):
   bad=copy.deepcopy(R);bad[name]['provenance']='CODEX_OBSERVED'
   with self.assertRaises(ValueError):validate(bad,S)
   self.assertEqual(R[name]['label'],'OPERATOR_SUPPLIED_PRODUCTION_EVIDENCE')
 def test_exact_deployed_source_commit(self):self.assertEqual(R['deployed_source_commit'],BASE);self.reject('deployed_source_commit','0'*40)
 def test_deployment_result_pass_complete(self):self.assertEqual((R['deployment_result'],R['deployment_error_code']),('PASS','COMPLETE'));self.reject('deployment_result','FAIL')
 def test_transaction_committed(self):self.assertEqual(R['deployment_transaction'],'COMMITTED');self.reject('deployment_transaction','PREPARED');self.assertEqual(R['transaction_semantics'],{'NOT_STARTED':'NOT_STARTED','PREPARED':'INCOMPLETE','COMMITTED':'PASS'})
 def test_production_deployment_pass(self):self.assertEqual(R['production_deployment'],'PASS');self.reject('production_deployment','NOT_STARTED')
 def test_block_return_code_zero_not_boolean(self):self.assertIs(type(R['deployment_block_return_code']),int);self.assertEqual(R['deployment_block_return_code'],0);self.reject('deployment_block_return_code',1);self.reject('deployment_block_return_code',False)
 def test_exact_five_dependencies_nine_created_targets(self):
  prep=json.loads(subprocess.check_output(['git','show',BASE+':governance/pe4/pe4-ha-association-adapter-deployment-preparation.json'],cwd=ROOT))
  self.assertEqual((R['dependency_count'],R['dependencies_pass'],len(R['dependencies'])),(5,5,5));self.assertEqual((R['deploy_target_count'],R['deploy_targets_pass'],len(R['deployed_targets'])),(9,9,9))
  self.assertEqual({i['path'] for i in R['dependencies']},{i['path'] for i in prep['production_dependencies']});self.assertEqual({i['path'] for i in R['deployed_targets']},{i['path'] for i in prep['deployment_files']});self.assertTrue(all(i['newly_created'] and i['acceptance']=='PASS' for i in R['deployed_targets']))
  self.assertEqual((R['transaction_target_count'],R['transaction_created_file_count']),(9,9));self.reject('transaction_created_file_count',8)
 def test_static_acceptance_pass_zero_failures(self):
  self.assertEqual((R['static_acceptance'],R['static_acceptance_failure_count']),('PASS',0));self.reject('static_acceptance_failure_count',1)
  result=R['static_acceptance_evidence']['result'];self.assertEqual(result['MODE'],'READ_ONLY');self.assertEqual(result['SOURCE_HEAD'],BASE);self.assertEqual(result['FAILURE_COUNT'],0)
  for key in ('SOURCE_IDENTITY','PRODUCTION_DEPENDENCIES','DEPLOYED_TARGETS','TRANSACTION_AUTHORITY','ENDPOINT_CONFIGURATION','STATE_BOUNDARY','SCHEDULER_BOUNDARY','PLATFORM_STATUS_PRESERVATION','COMPATIBILITY_STATE_PRESERVATION','RESULT'):self.assertEqual(result[key],'PASS')
 def test_private_state_absent_before_first_run(self):
  self.assertEqual(R['pre_adapter_private_state'],'ABSENT');self.assertEqual(R['private_state_absent'],['home_assistant.json','.home_assistant.txn-*','.home_assistant.done-*']);self.assertEqual(R['association_state_publication'],'NOT_STARTED');self.assertEqual(R['association_lifecycle_execution'],'NOT_STARTED');self.assertEqual(R['ha_association_results'],'NONE_YET');self.reject('pre_adapter_private_state','PRESENT')
 def test_scheduler_not_started_absent_platform_cron_preserved(self):
  self.assertEqual(R['scheduler_deployment'],'NOT_STARTED');self.assertFalse(R['association_scheduler_present']);self.assertFalse(R['scheduler_present_before']);self.assertFalse(R['platform_cron_mutation']);self.assertEqual(R['existing_platform_cron'],'17 3 * * * flock -n /tmp/hioc-platform-status.lock /home/jazofv1/hioc/pi4/bin/hioc-platform-status.py');self.reject('association_scheduler_present',True)
 def test_platform_status_known_old_generation_preserved(self):
  self.assertEqual(R['platform_status_sha256'],'b65464e722bf9a4da0004ecf3bb05e4105f345a87c62405ce92d97c6298b2af8');self.assertEqual(R['platform_status_preservation'],'PASS');self.assertFalse(R['platform_status_deployed']);self.assertFalse(R['platform_status_executed']);self.reject('platform_status_sha256','0'*64)
 def test_compatibility_state_metadata_preserved_without_contents(self):
  self.assertEqual((R['compatibility_state_preservation'],R['compatibility_state_size'],R['compatibility_state_mtime']),('PASS',39536,'2026-10-06 12:25:11.049013060 -0600'));self.assertFalse(R['compatibility_state_contents_stored']);self.assertEqual(R['static_acceptance_evidence']['result']['COMPATIBILITY_STATE_METADATA'],'39536|2026-10-06 12:25:11.049013060 -0600');self.reject('compatibility_state_size',39537)
 def test_historical_failed_attempt_chronology(self):
  expected=[('2ef66a2d575c923c6939a4cd4d5bb2c8aab2f816','RUNTIME_DRIFT'),('e4d5a19afecccb1584708e3da57ba3c0c4258523','RUNTIME_DRIFT'),('84635cb88380c590d2adfb655c37afd2118c629f','DEPENDENCY_DRIFT')]
  self.assertEqual([(i['source_commit'],i['error_code']) for i in R['historical_failed_attempts']],expected)
  for i in R['historical_failed_attempts']:self.assertEqual((i['result'],i['deployment_transaction'],i['production_deployment']),('FAIL','NOT_STARTED','NOT_STARTED'));self.assertTrue(i['pre_intent']);self.assertFalse(i['partial_deployment'])
  self.assertEqual(R['successful_attempt'],4);self.assertTrue(R['first_attempt_to_reach_durable_intent'])
 def test_no_rollback(self):self.assertEqual(R['rollback'],'NOT_PERFORMED');self.assertTrue(all(i['rollback']=='NOT_PERFORMED' for i in R['historical_failed_attempts']));self.reject('rollback','PERFORMED')
 def test_adapter_not_executed_by_deployment_or_static_check(self):self.assertFalse(R['adapter_executed']);self.assertFalse(R['adapter_executed_by_static_acceptance']);self.reject('adapter_executed',True)
 def test_no_adapter_ha_network_authentication(self):self.assertFalse(R['ha_network_attempted']);self.assertFalse(R['ha_authentication_attempted']);self.assertFalse(R['ha_network_attempted_by_static_acceptance']);self.reject('ha_authentication_attempted',True)
 def test_next_task_exact_and_separate_authorization(self):self.assertEqual(R['next_task'],NEXT);self.assertTrue(R['first_adapter_run_requires_separate_authorization']);self.reject('next_task','PE-4 Home Assistant Association Adapter Deployment Execution')
 def test_master_authoritative_lifecycle_objective_and_next_agree(self):
  master=(ROOT/'docs/HIOC_MASTER_PLAN.md').read_text(encoding='utf-8');current=master.split('## Current Objective',1)[1].split('### Future Compatibility Diagnostics UX Checkpoint',1)[0]
  self.assertIn('**PE-4 Home Assistant Association Adapter Post-Run Reconciliation**',current);self.assertIn('### PE-4 Home Assistant Association Adapter Post-Run Reconciliation',current);self.assertNotIn('six existing',current);self.assertNotIn('eight additive',current);self.assertIn('five preserved',current);self.assertIn('nine newly created',current)
  table=master.split('Authoritative Current PE-4 Lifecycle',1)[1].split('### Completed',1)[0];self.assertIn('| PE-4 Home Assistant Association Adapter Deployment | PASS/CLOSED |',table)
  self.assertIn('| PE-4 Home Assistant Association Adapter Bounded Manual Production Validation | ATTEMPTED / REVIEW REQUIRED |',table)
  for checkpoint in ('Independent Production Acceptance','Scheduler Deployment'):self.assertIn('| PE-4 Home Assistant Association Adapter '+checkpoint+' | NOT STARTED |',table)
 def test_credential_semantics_local_validation_separate_static_check(self):
  self.assertEqual(R['credential_local_validation'],'PASS');c=R['credential_semantics'];self.assertEqual(c['deployment_file_access'],'GOVERNED_LOCAL_VALIDATOR_ONLY')
  for key in ('content_exposed_in_evidence_or_output','persisted_into_new_deployment_evidence','placed_in_argv','placed_in_environment','used_for_ha_authentication','codex_credential_access','static_acceptance_credential_access'):self.assertFalse(c[key])
  self.assertFalse(R['credential_accessed_by_static_acceptance']);self.assertFalse(R['static_acceptance_evidence']['result']['CREDENTIAL_ACCESSED_BY_THIS_CHECK'])
 def test_all_source_blobs_and_hashes_bound_to_deployed_commit(self):
  for item in R['sources'].values():
   raw=subprocess.check_output(['git','show',BASE+':'+item['path']],cwd=ROOT);self.assertEqual(hashlib.sha256(raw).hexdigest(),item['sha256']);self.assertEqual(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),item['git_blob']);self.assertEqual(raw,(ROOT/item['path']).read_bytes().replace(b'\r\n',b'\n'))
  self.assertEqual(R['source_identity_note']['supplied_text_length'],63);self.assertEqual(R['sources']['compatibility']['sha256'],'713c292c09282f3be524bc8a2090de43cf0fb78a81b3c71eed143b7a0d68e952')
 def test_endpoint_and_transaction_proofs_without_config_contents(self):
  self.assertTrue(R['transaction_endpoint_added']);self.assertEqual(R['required_endpoint'],'ws://192.168.100.251:8123/api/websocket');self.assertEqual(R['transaction_authority'],'PASS');self.assertIn('COMMITTED_MARKER_BOUND_TO_CANONICAL_INTENT_SHA256',R['transaction_proof']);self.assertIn('PRODUCTION_EQUALS_CANDIDATE',R['endpoint_proof']);self.assertFalse(R['additional_production_changes_inferred'])
 def test_evidence_scope_and_repository_closure_boundary(self):
  self.assertIsNot(R['deployment_evidence'],R['static_acceptance_evidence']);self.assertEqual(R['deployment_evidence']['result']['CREDENTIAL_LOCAL_VALIDATION'],'PASS');self.assertEqual(R['static_acceptance_evidence']['result']['MODE'],'READ_ONLY');self.assertEqual(R['lifecycle']['independent_production_acceptance'],'NOT_STARTED');self.assertFalse(R['runtime_contract_consumption']);self.assertFalse(R['closure_record_deployed']);self.assertTrue(all(v is False for v in R['negative_evidence_by_codex'].values()))
  doc=(ROOT/'docs/PE4_HOME_ASSISTANT_ASSOCIATION_ADAPTER_DEPLOYMENT_CLOSURE.md').read_text(encoding='utf-8');self.assertIn('first adapter run',doc.lower());self.assertNotIn('active/bin/python -I -B',doc)
if __name__=='__main__':unittest.main()
