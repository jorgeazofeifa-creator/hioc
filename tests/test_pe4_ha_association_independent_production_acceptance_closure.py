"""Repository-only sanitized closure assertions; never inspect retained evidence or execute acceptance."""
import copy,hashlib,json,subprocess,unittest
from pathlib import Path
from test_pe4_ha_association_deployment_closure import validate,canonical
ROOT=Path(__file__).resolve().parents[1]
BASE='400f157e1815a0960fba38ac1a92b93a7dda37eb'
P=ROOT/'governance/pe4/pe4-ha-association-independent-production-acceptance-closure.json'
R=json.loads(P.read_bytes());S=json.loads(P.with_suffix('.schema.json').read_bytes())
class AcceptanceClosureTests(unittest.TestCase):
 def test_canonical_closed_record(self):
  validate(R,S);self.assertEqual(P.read_bytes(),canonical(R));self.assertEqual(P.with_suffix('.schema.json').read_bytes(),canonical(S));self.assertEqual(R['status'],'PASS_CLOSED')
 def test_closed_schema_rejects_every_extra_and_changed_leaf(self):
  def visit(v,s):
   if type(v)==dict:
    bad=copy.deepcopy(v);bad['unreviewed_private_field']=True
    with self.assertRaises(ValueError):validate(bad,s)
    for k,x in v.items():visit(x,s['properties'][k])
   elif type(v)==list:
    with self.assertRaises(ValueError):validate(v+[None],s)
    for x,n in zip(v,s['prefixItems']):visit(x,n)
   else:
    with self.assertRaises(ValueError):validate(None,s)
  visit(R,S)
 def test_predecessor_authority(self):
  self.assertEqual(R['closure_predecessor'],BASE);self.assertEqual(subprocess.check_output(['git','show','-s','--format=%s',BASE],cwd=ROOT).decode().strip(),R['predecessor_subject']);self.assertEqual(subprocess.check_output(['git','rev-parse',BASE+'^'],cwd=ROOT).decode().strip(),R['predecessor_parent'])
 def test_all_eight_bound_git_identities(self):
  self.assertEqual(len(R['sources']),8)
  for item in R['sources']:
   self.assertEqual(item['commit'],BASE);raw=subprocess.check_output(['git','show',BASE+':'+item['path']],cwd=ROOT)
   self.assertEqual(hashlib.sha256(raw).hexdigest(),item['sha256']);self.assertEqual(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),item['git_blob'])
   if item['path']!='docs/HIOC_MASTER_PLAN.md':self.assertEqual((ROOT/item['path']).read_bytes().replace(b'\r\n',b'\n'),raw)
 def test_attempt_one_exact_historical_record(self):
  old=json.loads(subprocess.check_output(['git','show',BASE+':governance/pe4/pe4-ha-association-independent-production-acceptance-operator-path.json'],cwd=ROOT));self.assertEqual(R['attempt_1'],old['attempt_1']);self.assertEqual(R['original_ephemeral_evidence_limitation'],old['original_ephemeral_evidence_limitation']);self.assertEqual(R['attempt_1']['capture_result'],'FAIL');self.assertFalse(R['attempt_1']['evidence_recreated'])
 def test_attempt_two_execution_operator_provenance(self):
  a=R['attempt_2'];self.assertEqual(a['execution_provenance'],'OPERATOR_SUPPLIED_WINDOWS_AND_PRODUCTION_EXECUTION_EVIDENCE');self.assertFalse(a['codex_observed']);self.assertEqual((a['status'],a['operator_result'],a['acceptance_result'],a['error_code'],a['failure_stage']),('PASS','PASS','PASS','NONE','NONE'));self.assertEqual(a['remote_return_code'],0);self.assertIn('IMPLIES',a['remote_return_code_basis']);self.assertFalse(a['automatic_retry'])
 def test_attempt_two_review_operator_provenance(self):
  a=R['attempt_2'];self.assertEqual(a['review_provenance'],'OPERATOR_SUPPLIED_WINDOWS_EVIDENCE_REVIEW');self.assertEqual(a['evidence_review'],'PASS');self.assertFalse(a['review_pi3_access']);self.assertFalse(a['review_production_mutation']);self.assertFalse(a['evidence_directory_accessed_by_codex'])
 def test_exact_run_and_file_metadata(self):
  a=R['attempt_2'];self.assertEqual(a['source_commit'],BASE);self.assertEqual(a['run_id'],'20261007T220653-46cef5aace9e');self.assertEqual(a['run_directory_count'],1);self.assertEqual(a['file_names'],['manifest.json','validation.json']);self.assertEqual(a['validation_bytes'],560);self.assertEqual(a['manifest_bytes'],194);self.assertEqual(a['validation_sha256'],'b6dc423c243dba496dfb2f22918cafc8ee2e61566a2baac5a6bc67d5522f826f');self.assertEqual(a['manifest_sha256'],'14bfbb72b19082b565c0258efde2ae956cc7d00fe2da3b492be2ca376c7f0943')
 def test_manifest_binding(self):
  a=R['attempt_2'];self.assertEqual(a['manifest_source_commit'],BASE);self.assertEqual(a['manifest_validation_bytes'],a['validation_bytes']);self.assertEqual(a['manifest_validation_sha256'],a['validation_sha256']);self.assertEqual(a['manifest_binding'],'PASS')
 def test_all_eight_acceptance_gates(self):
  gates=R['attempt_2']['gates'];self.assertEqual(set(gates),{'DEPLOYMENT','RUNTIME','PRIVATE_STATE','COMPATIBILITY','INVENTORY','CRON_SCHEDULER','PROTECTED_SURFACES_UNCHANGED','CHECKPOINT_COUNTS_AGREE'});self.assertTrue(all(x=='PASS' for x in gates.values()))
 def test_prohibited_actions_false(self):
  self.assertTrue(all(x is False for x in R['attempt_2']['activity'].values()));self.assertTrue(all(x is False for x in R['negative_evidence_by_codex'].values()));self.assertTrue(all(x is False for x in R['source_synchronization']['actions'].values()))
 def test_reported_owners_and_protected_acls(self):
  a=R['attempt_2']['security']
  for k in ['run_owner','validation_owner','manifest_owner']:self.assertEqual(a[k],'AzureAD'+chr(92)+'JorgeAzofeifaCastill')
  for k in ['run_acl_protected','validation_acl_protected','manifest_acl_protected']:self.assertIs(a[k],True)
 def test_historical_limitation_not_erased(self):
  a=R['original_ephemeral_evidence_limitation'];self.assertFalse(a['present']);self.assertEqual((a['revalidation'],a['limitation'],a['disappearance_cause']),('UNAVAILABLE','RECORDED','UNKNOWN'));self.assertFalse(a['execution_time_comparison_recreated']);self.assertFalse(a['historical_evidence_recreated']);self.assertEqual(R['attempt_2']['original_ephemeral_evidence_revalidation'],'UNAVAILABLE')
 def test_source_sync_chain_and_changeset(self):
  a=R['source_synchronization'];self.assertEqual(a['provenance'],'OPERATOR_SUPPLIED');self.assertEqual(a['successor_commit_count'],2);self.assertEqual(a['changeset_count'],14);self.assertEqual(subprocess.check_output(['git','rev-parse',BASE+'^^'],cwd=ROOT).decode().strip(),a['head_before']);self.assertEqual(len(subprocess.check_output(['git','diff','--name-only',a['head_before'],BASE],cwd=ROOT).decode().splitlines()),14);self.assertEqual((a['head_after'],a['origin_main_after']),(BASE,BASE));self.assertEqual((a['result'],a['return_code']),('PASS',0));self.assertEqual((a['ahead'],a['behind']),(0,0))
 def test_prerequisites_pass(self):
  for k in ['preparation','capture_correction','operator_path_integration']:self.assertEqual(R['prerequisites'][k],'PASS_CLOSED')
  self.assertEqual(R['prerequisites']['native_windows_durability'],'PASS');self.assertEqual(R['prerequisites']['separate_durable_evidence_review'],'PASS')
 def test_acceptance_closed_scheduler_not_started(self):
  a=R['lifecycle'];self.assertEqual((a['attempt_1'],a['attempt_2'],a['independent_production_acceptance']),('FAIL_DURABLE_CAPTURE','PASS','PASS_CLOSED'));self.assertEqual(a['scheduler'],'NOT_STARTED');self.assertFalse(a['second_adapter_execution_authorized'])
 def test_pe4_phase_projection_rollback_preserved(self):
  a=R['lifecycle'];self.assertEqual((a['pe4'],a['phase7a'],a['projection'],a['rollback']),('NOT_COMPLETE','ACTIVE','DEFERRED','NOT_PERFORMED'))
 def test_no_raw_evidence_committed(self):
  self.assertFalse(R['attempt_2']['raw_evidence_committed']);self.assertEqual(R['privacy'],'SANITIZED_OPERATOR_SUPPLIED_METADATA_AND_HASH_IDENTITIES_ONLY_NO_RAW_EVIDENCE')
  for name in ['validation.json','manifest.json']:self.assertNotIn(name,[Path(x).name for x in subprocess.check_output(['git','ls-files','governance/pe4'],cwd=ROOT).decode().splitlines()])
 def test_master_authoritative_table(self):
  s=(ROOT/'docs/HIOC_MASTER_PLAN.md').read_text(encoding='utf8');t=s.split('Authoritative Current PE-4 Lifecycle',1)[1].split('### Completed',1)[0]
  for name,state in [('Independent Production Acceptance Attempt 1','FAIL / DURABLE CAPTURE'),('Independent Production Acceptance Attempt 2','PASS'),('PE-4 Home Assistant Association Adapter Independent Production Acceptance','PASS/CLOSED'),('PE-4 Home Assistant Association Adapter Scheduler Deployment','PASS/CLOSED')]:self.assertIn('| '+name+' | '+state+' |',t)
 def test_master_current_objective_and_next_checkpoint(self):
  s=(ROOT/'docs/HIOC_MASTER_PLAN.md').read_text(encoding='utf8');c=s.split('## Current Objective',1)[1];self.assertTrue(c.lstrip().startswith('**PE-4 Home Assistant Association Public Projection Deployment Baseline Correction**'));n=s.split('## Next Planned Task',1)[1];self.assertTrue(n.lstrip().startswith('### PE-4 Home Assistant Association Public Projection'));self.assertIn('NOT STARTED',n);self.assertEqual(R['next_objective_status'],'NOT_STARTED');self.assertTrue(R['future_execution_requires_separate_authorization'])
 def test_closure_document_boundary(self):
  s=(ROOT/'docs/PE4_HOME_ASSISTANT_ASSOCIATION_INDEPENDENT_PRODUCTION_ACCEPTANCE_CLOSURE.md').read_text(encoding='utf8');self.assertIn('Codex did not observe execution',s);self.assertIn('Scheduler Deployment NOT STARTED',s);self.assertIn('No scheduler implementation',s);self.assertIn('stdout durably unavailable',s)
if __name__=='__main__':unittest.main()
