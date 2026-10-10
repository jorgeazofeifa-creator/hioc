from test_pe4_ha_association_public_projection_test_binding_correction import closure_artifact_bindings, verify_source_binding
"""Repository-only sanitized operator-evidence closure; no runtime execution."""
import copy,hashlib,json,re,subprocess,unittest
from pathlib import Path
from test_pe4_ha_association_deployment_closure import validate,canonical
ROOT=Path(__file__).resolve().parents[1]
BASE='c762745b428b28518cf4415f7399ff2cacb70c66'
P=ROOT/'governance/pe4/pe4-ha-association-public-projection-posix-source-validation-closure.json'
R=json.loads(P.read_bytes());S=json.loads(P.with_suffix('.schema.json').read_bytes())
GATES=['SOURCE_IMPLEMENTATION_IDENTITY','PRIVATE_ADAPTER_IDENTITY','PRIVATE_SCHEMA_IDENTITY','POSIX_PATH_SECURITY','ASSOCIATION_LOCK_SECURITY','SHARED_LOCK_ACQUISITION','TRANSACTION_NAMESPACE','PRIVATE_STATE_COPY','PRIVATE_STATE_SCHEMA','PRIVATE_STATE_SEMANTICS','PUBLIC_CONTRACT','PUBLIC_CANDIDATE_DERIVATION','CURRENT_INVENTORY_INTERSECTION']
FLAGS=['PUBLIC_OUTPUT_WRITTEN','MQTT_PUBLISHED','HA_NETWORK_ATTEMPTED','CREDENTIAL_ACCESSED','ADAPTER_EXECUTED','CRONTAB_MUTATED','PRODUCTION_MUTATED']
EXPECTED={k:('CLEAN' if k=='TRANSACTION_NAMESPACE' else 'PASS') for k in GATES}
EXPECTED.update(TARGET='PI3 NUT&PIHOLE',SOURCE_COMMIT=BASE,MODE='READ_ONLY_SOURCE_VALIDATION',PRIOR_PUBLIC_PROJECTION_PRESENT='FALSE',PUBLIC_PROJECTION_ALREADY_PRESENT='FALSE',RESULT='PASS',ERROR_CODE='NONE',STOP_REQUIRED='TRUE')
EXPECTED.update({k:'FALSE' for k in FLAGS})

def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)

class PosixSourceValidationClosureTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.blobs={i['path']:git('show',BASE+':'+i['path']) for i in R['sources']}
 def test_exact_predecessor_parent_subject_and_source_commit(self):
  self.assertEqual(R['closure_predecessor'],BASE);self.assertEqual(git('show','-s','--format=%s',BASE).decode().strip(),R['predecessor_subject']);self.assertEqual(git('rev-parse',BASE+'^').decode().strip(),R['predecessor_parent']);self.assertEqual(R['validator']['source_commit'],BASE)
 def test_closed_canonical_family(self):
  validate(R,S);self.assertEqual(P.read_bytes(),canonical(R));self.assertEqual(P.with_suffix('.schema.json').read_bytes(),canonical(S))
 def test_every_nested_object_and_leaf_rejects_unknown_content(self):
  def visit(v,s):
   if type(v) is dict:
    with self.assertRaises(ValueError):validate(dict(v,unreviewed=True),s)
    for k,x in v.items():visit(x,s['properties'][k])
   elif type(v) is list:
    with self.assertRaises(ValueError):validate(v+[None],s)
    for x,n in zip(v,s['prefixItems']):visit(x,n)
   else:
    with self.assertRaises(ValueError):validate(None,s)
  visit(R,S)
 def test_exact_sanitized_output_and_all_thirteen_gates(self):
  fields=R['validator']['sanitized_result'];self.assertEqual(fields,EXPECTED);self.assertEqual(len(GATES),13)
  exact=''.join(k+'='+v+'\n' for k,v in fields.items())
  # Output order is frozen separately to preserve the actual validator representation.
  exact=''.join(k+'='+fields[k]+'\n' for k in R['validator']['output_key_order'])
  self.assertEqual(R['validator']['exact_sanitized_output'],exact)
  self.assertEqual(dict(line.split('=',1) for line in exact.splitlines()),EXPECTED)
 def test_operator_provenance_single_execution_no_codex_observation(self):
  self.assertEqual(R['evidence_provenance'],'OPERATOR_SUPPLIED');self.assertFalse(R['codex_observed']);self.assertEqual(R['validator']['execution_count'],1);self.assertTrue(R['validator']['authorized_operator_execution']);self.assertFalse(R['validator']['reexecution_authorized_by_closure']);self.assertTrue(all(v is False for v in R['codex_activity'].values()))
 def test_supplied_source_review_and_scoped_activity(self):
  a=R['source_review'];self.assertEqual(a['provenance'],'OPERATOR_SUPPLIED');self.assertEqual(a['host'],'nutandpihole');self.assertEqual(a['user'],'jazofv1');self.assertEqual(a['head'],BASE);self.assertEqual(a['origin_main'],BASE);self.assertEqual(a['parent'],R['predecessor_parent']);self.assertEqual(a['subject'],R['predecessor_subject']);self.assertEqual((a['ahead'],a['behind']),(0,0));self.assertTrue(a['worktree_clean']);self.assertFalse(a['active_git_operation']);self.assertEqual(a['implementation_changeset_count'],18);self.assertTrue(all(v is False for v in a['review_activity'].values()));self.assertEqual(a['review_activity_scope'],'INDEPENDENT_REVIEW_ONLY_NOT_VALIDATOR_OR_NATURAL_CYCLES')
 def test_supplied_crontab_hash_and_counts_without_mutation(self):
  a=R['source_review'];self.assertEqual(a['crontab_sha256'],'8f900f4679aa861b02e781a61927683db5900ddfe159d78c3831a1595ae7fe71');self.assertEqual((a['association_marker_count'],a['association_job_count'],a['inventory_job_count']),(1,1,1))
 def test_predeployment_public_namespace_baseline_time_scope(self):
  a=R['predeployment_public_namespace'];self.assertFalse(a['prior_present']);self.assertFalse(a['current_present']);self.assertEqual(a['scope'],'CURRENT_PRODUCTION_INVENTORY_AT_OPERATOR_VALIDATION_TIME_ONLY');self.assertFalse(a['additional_production_state_inferred'])
 def test_all_immutable_implementation_and_private_bindings(self):
  required={'governance/pe4/pe4-ha-association-public-projection-implementation.json','governance/pe4/pe4-ha-association-public-projection-implementation.schema.json','governance/pe4/pe4-home-assistant-public-projection.schema.json','pi4/lib/hioc/home_assistant_public_projection.py','pi4/bin/hioc-inventory-engine.py','tools/hioc-pe4-ha-public-projection-source-validate.py','tests/test_pe4_ha_association_public_projection.py','tests/test_pe4_ha_public_projection_source_validate.py','docs/PE4_HOME_ASSISTANT_ASSOCIATION_PUBLIC_PROJECTION_IMPLEMENTATION.md','docs/HIOC_MASTER_PLAN.md','pi4/lib/hioc/home_assistant_association.py','governance/pe4/pe4-home-assistant-association-state-v1.1.schema.json'}
  self.assertTrue(required<={i['path'] for i in R['sources']})
  for i in R['sources']:
   raw=self.blobs[i['path']];self.assertEqual(i['commit'],BASE);self.assertEqual(hashlib.sha256(raw).hexdigest(),i['sha256']);self.assertEqual(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),i['git_blob'])
   verify_source_binding(i,raw,'governance/pe4/pe4-ha-association-public-projection-posix-source-validation-closure.json',BASE)
  expected={'pi4/lib/hioc/home_assistant_association.py':'9a9be5812f3481146de7546875320eb6adec65ca5a2b3230ff5fec378892c7c1','governance/pe4/pe4-home-assistant-association-state-v1.1.schema.json':'5cd060ffd0a7a2e0a2b3e61da50ec8e5a418f4251df7305f713c10701b0e6a5d'}
  for path,sha in expected.items():self.assertEqual(hashlib.sha256(self.blobs[path]).hexdigest(),sha)
 def test_all_current_closure_artifact_bindings(self):
  self.assertEqual(len(R['closure_artifacts']),6)
  for i in R['closure_artifacts']:
   raw=git('show','6bfb689fc9e49de5d7ae17267f2b389e13f0bc1e:'+i['path']);self.assertEqual(hashlib.sha256(raw).hexdigest(),i['sha256']);self.assertEqual(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),i['git_blob'])
   prep=json.loads((ROOT/'governance/pe4/pe4-ha-association-public-projection-deployment-baseline-correction.json').read_bytes());current={a['path']:a for a in prep['artifacts']};current.update(closure_artifact_bindings());now=(ROOT/i['path']).read_bytes().replace(b'\r\n',b'\n');self.assertEqual(hashlib.sha256(now).hexdigest(),current.get(i['path'],i)['sha256'])
 def test_no_runtime_deployment_scheduler_or_private_authority_changes(self):
  self.assertEqual(git('diff','--name-only',BASE,'6bfb689fc9e49de5d7ae17267f2b389e13f0bc1e','--','pi4','pi4-tools','tools','release','homeassistant','requirements-pe4.lock'),b'')
  paths=git('diff','--name-only',BASE,'6bfb689fc9e49de5d7ae17267f2b389e13f0bc1e').decode().splitlines();allowed={i['path'] for i in R['closure_artifacts']}|{str(P.relative_to(ROOT)).replace('\\','/'),str(P.with_suffix('.schema.json').relative_to(ROOT)).replace('\\','/')};self.assertTrue(set(paths)<=allowed)
 def test_privacy_no_raw_state_identifiers_or_credentials(self):
  forbidden={'device_id','hioc_device_id','ha_device_id','entity_id','registry_id','config_entry_id','area_name','mac','ip_address','token','credential_data','raw_inventory','raw_state','raw_crontab','raw_stdout','raw_stderr','integration_domains'}
  def walk(v):
   if type(v) is dict:
    self.assertFalse(forbidden&set(v))
    for x in v.values():walk(x)
   elif type(v) is list:
    for x in v:walk(x)
  walk(R)
  text=canonical(R).decode();self.assertIsNone(re.search(r'dev_[0-9a-f]{16}|(?:[0-9a-f]{2}:){5}[0-9a-f]{2}|(?:[0-9]{1,3}\.){3}[0-9]{1,3}',text));self.assertNotIn('sensor.',text);self.assertNotIn('Bearer ',text)
 def test_exact_current_lifecycle_and_next_preparation_gate(self):
  expected=dict(preparation='PASS_CLOSED',source_implementation='IMPLEMENTED',windows_synthetic_validation='PASS',pi3_posix_source_validation='PASS_CLOSED',public_projection_deployment='NOT_STARTED',public_projection_production_execution='NOT_STARTED',scheduler_deployment='PASS_CLOSED',recurring_association_scheduler='ACTIVE_AUTHORIZED',inventory_scheduler='ACTIVE',manual_second_adapter_execution='NOT_AUTHORIZED_NOT_PERFORMED',pe4='NOT_COMPLETE',phase7a='ACTIVE',pe5='NOT_STARTED',rollback='NOT_PERFORMED')
  self.assertEqual(R['lifecycle'],expected);self.assertEqual(R['next_checkpoint'],'PUBLIC_PROJECTION_DEPLOYMENT_PREPARATION');self.assertTrue(R['next_checkpoint_requires_separate_authorization']);self.assertFalse(R['deployment_authorized_by_closure'])
 def test_master_current_table_objective_next_and_sync_only(self):
  text=subprocess.check_output(['git','show','c7db29f795909d7926e36c02f1166034bcebb8b0:docs/HIOC_MASTER_PLAN.md'],cwd=ROOT).decode('utf8');table=text.split('## Authoritative Current PE-4 Lifecycle',1)[1].split('### Completed',1)[0]
  self.assertIn('| PE-4 Home Assistant Association Public Projection PI3 POSIX Source Validation | PASS/CLOSED |',table)
  current=text.split('## Current Objective',1)[1].split('### Historical',1)[0];self.assertTrue(current.lstrip().startswith('**PE-4 Home Assistant Association Public Projection Deployment Baseline Correction**'));self.assertIn('OPERATOR_SUPPLIED',current)
  next_task=text.split('## Next Planned Task',1)[1].split('### Historical',1)[0];self.assertTrue(next_task.lstrip().startswith('### PE-4 Home Assistant Association Public Projection Corrected Pre-Deployment PI3 Baseline Validation'));self.assertIn('NOT STARTED / REQUIRED BEFORE DEPLOYMENT',next_task)
  for section in [current,next_task]:
   for phrase in ['Baseline Correction commit ONLY','STOP and independent source review','PE-4 NOT COMPLETE']:self.assertIn(phrase,section)
 def test_document_explains_proof_limits_and_operator_evidence(self):
  text=(ROOT/'docs/PE4_HOME_ASSISTANT_ASSOCIATION_PUBLIC_PROJECTION_POSIX_SOURCE_VALIDATION_CLOSURE.md').read_text(encoding='utf8')
  for phrase in ['OPERATOR_SUPPLIED','Codex did not observe','in memory only','at validation time','does not prove','Deployment NOT STARTED','Production Execution NOT STARTED','PE-4 NOT COMPLETE','STOP']:self.assertIn(phrase,text)
  for limitation in R['does_not_prove']:self.assertIn(limitation,text)

# Every supplied sanitized field is independently protected against altered evidence.
for name,expected in EXPECTED.items():
 def test(self,name=name,expected=expected):
  bad=copy.deepcopy(R);bad['validator']['sanitized_result'][name]='UNREVIEWED'
  with self.assertRaises(ValueError):validate(bad,S)
  self.assertEqual(R['validator']['sanitized_result'][name],expected)
 setattr(PosixSourceValidationClosureTests,'test_exact_operator_field_'+name.lower(),test)

if __name__=='__main__':unittest.main()
