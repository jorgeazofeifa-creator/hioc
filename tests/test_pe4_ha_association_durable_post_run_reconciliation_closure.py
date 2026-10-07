"""Repository-only closure tests; supplied PI3 evidence is never collected or executed here."""
import copy,hashlib,importlib.util,json,subprocess,unittest
from pathlib import Path
from test_pe4_ha_association_deployment_closure import validate,canonical
ROOT=Path(__file__).resolve().parents[1]
BASE='96150db5e28b065a587ae09ce0522ef6bd66f3be'
PARENT='d767ad429ae0573ffb1411ccb787795063ef647c'
SUBJECT='PE-4: correct reconciliation evidence authority'
NEXT='PE-4 Home Assistant Association Adapter Independent Production Acceptance'
RECORD=ROOT/'governance/pe4/pe4-ha-association-durable-post-run-reconciliation-closure.json'
SCHEMA=RECORD.with_suffix('.schema.json')
R=json.loads(RECORD.read_bytes());S=json.loads(SCHEMA.read_bytes())
AUTHORITY=ROOT/'governance/pe4/pe4-ha-association-reconciliation-evidence-authority-correction.json'
Q=json.loads(AUTHORITY.read_bytes())
def definitions():
 spec=importlib.util.spec_from_file_location('closure_report_definitions',ROOT/'tools/hioc-pe4-ha-association-manual-reconcile.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
N=definitions()
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def evidence_text(value):return '\n'.join(k+'='+v for k,v in value.items())+'\n'
class DurableReconciliationClosureTests(unittest.TestCase):
 def reject(self,path,value):
  bad=copy.deepcopy(R);target=bad
  for key in path[:-1]:target=target[key]
  target[path[-1]]=value
  with self.assertRaises(ValueError):validate(bad,S)
 def test_canonical_json_closed_schema_pair(self):
  validate(R,S);self.assertEqual(RECORD.read_bytes(),canonical(R));self.assertEqual(SCHEMA.read_bytes(),canonical(S));self.assertEqual(S['$id'],SCHEMA.name);self.assertEqual(R['status'],'PASS_CLOSED');self.assertEqual(R['schema_version'],'1.0');self.assertEqual(R['record_type'],'PE4_HA_ASSOCIATION_DURABLE_POST_RUN_RECONCILIATION_CLOSURE')
 def test_every_object_rejects_extra_properties(self):
  def visit(value,node):
   if isinstance(value,dict):
    bad=copy.deepcopy(value);bad['unreviewed_extra']=True
    with self.assertRaises(ValueError):validate(bad,node)
    for key,child in node['properties'].items():visit(value[key],child)
   elif isinstance(value,list):
    for item,child in zip(value,node['prefixItems']):visit(item,child)
  visit(R,S)
 def test_missing_required_property_rejected(self):
  for key in R:
   bad=copy.deepcopy(R);del bad[key]
   with self.assertRaises(ValueError):validate(bad,S)
 def test_exact_source_commit_parent_subject(self):
  self.assertEqual(R['starting_commit'],BASE);self.assertEqual(R['predecessor_parent'],PARENT);self.assertEqual(R['predecessor_subject'],SUBJECT)
  self.assertEqual(git('rev-parse',BASE+'^').decode().strip(),PARENT);self.assertEqual(git('show','-s','--format=%s',BASE).decode().strip(),SUBJECT)
  for key in ('starting_commit','predecessor_parent','predecessor_subject'):self.reject([key],'unapproved')
 def test_exact_predecessor_changeset(self):self.assertEqual(R['predecessor_changeset_count'],21);self.assertEqual(len(git('diff-tree','--no-commit-id','--name-only','-r',BASE).splitlines()),21)
 def test_source_identities_bound_to_predecessor_and_current_bytes(self):
  for name,item in R['sources'].items():
   raw=git('show',BASE+':'+item['path']);self.assertEqual(raw,(ROOT/item['path']).read_bytes().replace(b'\r\n',b'\n'));self.assertEqual(hashlib.sha256(raw).hexdigest(),item['sha256']);self.assertEqual(git('rev-parse',BASE+':'+item['path']).decode().strip(),item['git_blob']);self.reject(['sources',name,'sha256'],'0'*64);self.reject(['sources',name,'git_blob'],'0'*40)
 def test_all_predecessor_governance_files_immutable(self):
  for path in git('ls-tree','-r','--name-only',BASE,'governance').decode().splitlines():self.assertEqual(git('show',BASE+':'+path),(ROOT/path).read_bytes().replace(b'\r\n',b'\n'))
 def test_source_synchronization_evidence_exact_and_consistent(self):
  e=R['source_synchronization_evidence'];r=e['report'];self.assertEqual(dict(line.split('=',1) for line in e['exact_report_text'].splitlines()),r);self.assertEqual(e['return_code'],0)
  for key in ('EXPECTED_TARGET','FETCHED_ORIGIN_MAIN','HEAD_AFTER','ORIGIN_MAIN_AFTER'):self.assertEqual(r[key],BASE)
  for key in ('EXPECTED_PREDECESSOR','HEAD_BEFORE'):self.assertEqual(r[key],PARENT)
  for key in ('TARGET_PARENT_VALIDATION','TARGET_SUBJECT_VALIDATION','TARGET_CHANGESET_VALIDATION','SOURCE_IDENTITY_VALIDATION','RESULT','SOURCE_SYNCHRONIZATION'):self.assertEqual(r[key],'PASS')
  self.assertEqual(r['EXPECTED_SUBJECT'],SUBJECT);self.assertEqual(r['AHEAD'],r['BEHIND']);self.assertEqual(r['AHEAD'],'0');self.assertEqual(r['WORKTREE_CLEAN'],'TRUE');self.assertEqual(r['CHANGESET_COUNT'],'21');self.assertEqual(r['SOURCE_SYNCHRONIZATION_RETURN_CODE'],'0')
  for key,field in [('evidence_authority_record','EVIDENCE_AUTHORITY_RECORD_SHA256'),('evidence_authority_schema','EVIDENCE_AUTHORITY_SCHEMA_SHA256'),('corrected_reconciler','CORRECTED_RECONCILER_SHA256'),('adapter','ADAPTER_SHA256'),('entrypoint','ENTRYPOINT_SHA256'),('compatibility_module','COMPATIBILITY_MODULE_SHA256'),('deployment_closure','DEPLOYMENT_CLOSURE_SHA256')]:self.assertEqual(r[field],R['sources'][key]['sha256'])
  for key in ('ADAPTER_EXECUTED_BY_THIS_ACTION','SECOND_ADAPTER_EXECUTION_AUTHORIZED','RECONCILER_EXECUTED_BY_THIS_ACTION','HA_NETWORK_ATTEMPTED_BY_THIS_ACTION','CREDENTIAL_ACCESSED_BY_THIS_ACTION','PRODUCTION_MUTATED_BY_THIS_ACTION'):self.assertEqual(r[key],'FALSE')
 def test_independent_source_review_is_supplied_history(self):
  e=R['independent_source_review'];self.assertEqual(e['reviewed_commit'],BASE);self.assertEqual(e['reviewed_parent'],PARENT);self.assertEqual(e['reviewed_subject'],SUBJECT);self.assertEqual(e['provenance'],'USER_SUPPLIED_REVIEW_HISTORY');self.assertFalse(e['codex_observed']);self.assertTrue(e['separate_durable_reconciliation_authorized'])
 def test_operator_provenance_cannot_be_codex_observed(self):
  for name in ('source_synchronization_evidence','durable_reconciliation_evidence'):
   self.assertEqual(R[name]['label'],'OPERATOR_SUPPLIED_PRODUCTION_EVIDENCE');self.assertEqual(R[name]['provenance'],'OPERATOR_SUPPLIED');self.reject([name,'provenance'],'CODEX_OBSERVED')
  self.assertEqual(R['operator_evidence_provenance'],'OPERATOR_SUPPLIED');self.reject(['operator_evidence_provenance'],'CODEX_OBSERVED')
 def test_exact_finite_reconciliation_pass_report_matches_predecessor_contract(self):
  e=R['durable_reconciliation_evidence'];r=e['report'];self.assertEqual(set(r),set(N.REPORT_FIELDS));self.assertEqual(N.report_text(r)+'RECONCILIATION_RETURN_CODE=0\n',e['exact_report_text']);self.assertEqual(dict(line.split('=',1) for line in e['exact_report_text'].splitlines()),dict(r,RECONCILIATION_RETURN_CODE='0'));self.assertEqual(r['SOURCE_EVIDENCE_AUTHORITY_COMMIT'],BASE);self.assertEqual(e['invocations_under_successor_authority'],1);self.assertEqual(e['return_code'],0)
 def test_return_code_integer_zero_not_boolean(self):
  for name in ('source_synchronization_evidence','durable_reconciliation_evidence'):
   self.assertIs(type(R[name]['return_code']),int)
   for value in (1,False):self.reject([name,'return_code'],value)
 def test_historical_live_report_exactly_frozen(self):
  old=json.loads(git('show',PARENT+':'+R['sources']['historical_scope_record']['path']));e=R['historical_live_execution'];self.assertEqual(e['report'],old['historical_evidence']['report']);self.assertEqual(e['invocations'],1);self.assertEqual(e['wrapper_return_code'],1);self.assertFalse(e['historical_evidence_rewritten']);self.assertEqual(e['report']['MANUAL_REVIEW_REQUIRED'],'TRUE')
  r=R['durable_reconciliation_evidence']['report']
  for new,oldkey in [('HISTORICAL_ADAPTER_RESULT','RESULT'),('HISTORICAL_WRAPPER_OVERALL_VALIDATION','OVERALL_VALIDATION'),('HISTORICAL_PRODUCTION_FILES_UNCHANGED','PRODUCTION_FILES_UNCHANGED'),('HISTORICAL_ADAPTER_EXECUTION_COUNT','ADAPTER_EXECUTION_COUNT'),('HISTORICAL_EXECUTION_TIME_CONFIG_PRESERVED','CONFIG_UNCHANGED'),('HISTORICAL_EXECUTION_TIME_INVENTORY_PRESERVED','CANONICAL_INVENTORY_UNCHANGED')]:self.assertEqual(r[new],e['report'][oldkey])
 def test_failed_first_reconciliation_preserved(self):
  self.assertEqual(R['historical_reconciliation_attempt_1'],Q['attempt_1']);self.assertEqual(R['historical_reconciliation_attempt_1']['report']['RECONCILIATION'],'FAIL');self.assertEqual(R['historical_reconciliation_attempt_1']['report']['FAILURE_STAGE'],'HISTORICAL_EVIDENCE');self.assertFalse(R['historical_reconciliation_attempt_1']['durable_checks_reached'])
 def test_missing_artifact_limitation_and_unknown_cause_retained(self):
  e=R['original_ephemeral_evidence'];self.assertEqual(e['directory'],Q['original_ephemeral_directory']);self.assertFalse(e['present']);self.assertEqual(e['matching_directories'],0);self.assertEqual(e['revalidation'],'UNAVAILABLE');self.assertEqual(e['limitation'],'RECORDED');self.assertEqual(e['disappearance_cause'],'UNKNOWN');self.assertEqual(e['unavailable_checks'],Q['evidence_limitation']);self.assertFalse(e['historical_evidence_recreated']);self.assertEqual(e['original_artifact_identities'],'NOT_INDEPENDENTLY_RECORDED_BEFORE_LOSS_NOT_CLAIMED')
 def test_three_evidence_classes_remain_separate(self):
  self.assertEqual(R['evidence_authority_model'],{'historical_report':'COMMITTED_OPERATOR_SUPPLIED_REPORT','original_ephemeral_artifacts':'UNAVAILABLE_FOR_REVALIDATION','durable_current_production':'OPERATOR_SUPPLIED_RECONCILIATION_PASS'})
 def test_corrected_bounded_manual_closure_contract_explicit(self):
  c=R['manual_validation_closure_contract']
  for key in ('historical_adapter_pass','historical_wrapper_fail_preserved','historical_global_false_preserved','one_adapter_invocation_only','historical_execution_time_config_inventory_true_preserved','corrected_durable_report_matches_predecessor_contract','protected_production_surfaces_unchanged','current_durable_validation_gates_pass','missing_original_artifact_limitation_retained'):self.assertIs(c[key],True);self.reject(['manual_validation_closure_contract',key],False)
  for key in ('execution_time_comparison_recreated','original_artifact_bytes_revalidated','independent_production_acceptance_performed'):self.assertIs(c[key],False);self.reject(['manual_validation_closure_contract',key],True)
 def test_protected_contract_and_durable_checks_preserved(self):self.assertEqual(R['protected_surface_policy'],Q['protected_surface_policy']);self.assertEqual(R['durable_checks'],Q['durable_checks']);self.assertEqual(R['future_evidence_durability_rule'],Q['future_evidence_durability_rule'])
 def test_no_implementation_or_runtime_contract_changes(self):
  for key in ('runtime_implementation_modified','reconciler_modified','runtime_contract_consumption','closure_record_deployed','second_adapter_execution_authorized'):self.assertIs(R[key],False);self.reject([key],True)
 def test_codex_negative_evidence_all_false(self):
  for key,value in R['negative_evidence_by_codex'].items():self.assertIs(value,False);self.reject(['negative_evidence_by_codex',key],True)
 def test_next_project_objective_exact_and_not_started(self):self.assertEqual(R['next_task'],NEXT);self.assertEqual(R['lifecycle']['independent_production_acceptance'],'NOT_STARTED');self.reject(['next_task'],'Scheduler Deployment')
 def test_master_current_lifecycle_objective_and_history(self):
  s=(ROOT/'docs/HIOC_MASTER_PLAN.md').read_text(encoding='utf8');current=s.split('## Current Objective',1)[1].split('### Future Compatibility Diagnostics UX Checkpoint',1)[0];self.assertIn('**'+NEXT+'**',current);self.assertIn('### '+NEXT,current);self.assertIn('PI3 source synchronization to the durable reconciliation closure commit',current);self.assertNotIn('PREPARED FOR SEPARATE AUTHORIZATION',current)
  table=s.split('## Authoritative Current PE-4 Lifecycle',1)[1].split('### Completed',1)[0]
  for name in ('Bounded Manual Production Validation','Durable Post-Run Reconciliation'):self.assertIn('| PE-4 Home Assistant Association Adapter '+name+' | PASS/CLOSED |',table)
  for row in ('| Historical Wrapper | FAIL / MANUAL REVIEW REQUIRED |','| Post-Run Reconciliation Attempt 1 | FAIL / HISTORICAL_EVIDENCE |','| Second Adapter Execution | NOT AUTHORIZED |'):self.assertIn(row,table)
  self.assertIn('Active Discovery remains postponed',current);self.assertIn('Phase 7A Passive Living Inventory ACTIVE',current)
 def test_original_master_chronology_immutable(self):
  old=git('show',BASE+':docs/HIOC_MASTER_PLAN.md').decode();now=(ROOT/'docs/HIOC_MASTER_PLAN.md').read_text(encoding='utf8');self.assertEqual(old.split('# Historical Checkpoint Chronology',1)[1].split('# Implementation Status',1)[0],now.split('# Historical Checkpoint Chronology',1)[1].split('# Implementation Status',1)[0])
 def test_focused_document_provenance_limits_and_next_checkpoint(self):
  text=(ROOT/'docs/PE4_HOME_ASSISTANT_ASSOCIATION_DURABLE_POST_RUN_RECONCILIATION_CLOSURE.md').read_text(encoding='utf8')
  for value in ('OPERATOR_SUPPLIED_PRODUCTION_EVIDENCE','PRODUCTION_FILES_UNCHANGED=FALSE','PROTECTED_PRODUCTION_SURFACES_UNCHANGED=TRUE','UNAVAILABLE','RECORDED','Disappearance cause UNKNOWN','original bytes','FULL_ORIGINAL_ARTIFACT_REVALIDATION','ZERO_EVIDENCE_GAPS',NEXT):self.assertIn(value,text)
  self.assertIn('Closure-critical evidence must not rely solely on ephemeral /tmp storage',text)
 def test_final_repository_validation_provenance_and_counts(self):
  e=R['repository_validation_evidence']
  self.assertEqual(e['approved_test_corrections']['count'],2);self.assertEqual(len(e['approved_test_corrections']['paths']),2);self.assertFalse(e['approved_test_corrections']['runtime_implementation_modified'])
  for name,total in [('related_ha_closure_tests',463),('negative_in_memory_checks',9)]:
   self.assertEqual(e[name]['provenance'],'CODEX_OBSERVED_REPOSITORY_VALIDATION');self.assertEqual(e[name]['total'],total);self.assertEqual(e[name]['passed'],total);self.reject(['repository_validation_evidence',name,'passed'],0)
  for name in ('action_e_standard_user','full_regression'):
   self.assertEqual(e[name]['provenance'],'OPERATOR_SUPPLIED_WINDOWS_VALIDATION_EVIDENCE');self.assertFalse(e[name]['codex_executed']);self.reject(['repository_validation_evidence',name,'codex_executed'],True)
  f=e['full_regression'];self.assertEqual(f['total'],f['passed']+f['skipped']);self.assertEqual((f['total'],f['passed'],f['failed'],f['errors'],f['skipped']),(1868,1821,0,0,47));self.reject(['repository_validation_evidence','full_regression','failed'],1)
  self.assertEqual(e['action_e_standard_user']['tests'],26)
# One independent closed-schema rejection test for each finite result field.
EXPECTED={'TARGET':'PI3 NUT&PIHOLE','SOURCE_EVIDENCE_AUTHORITY_COMMIT':BASE,**N.SUCCESS,**{k:'FALSE' for k in N.NO_ACTIVITY},'RECONCILIATION':'PASS'}
for field,expected in EXPECTED.items():
 def check(self,field=field,expected=expected):
  self.assertEqual(R['durable_reconciliation_evidence']['report'][field],expected)
  changed={'FAIL':'PASS','FALSE':'TRUE','TRUE':'FALSE','UNAVAILABLE':'PASS','RECORDED':'ZERO_EVIDENCE_GAPS','PASS':'FAIL'}.get(expected,'UNAPPROVED')
  self.reject(['durable_reconciliation_evidence','report',field],changed)
 setattr(DurableReconciliationClosureTests,'test_required_report_'+field.lower(),check)
LIFECYCLE={'durable_post_run_reconciliation':'PASS_CLOSED','bounded_manual_validation':'PASS_CLOSED','first_live_adapter_invocation':'COMPLETED_ONCE_ADAPTER_PASS','historical_wrapper':'FAIL_MANUAL_REVIEW_REQUIRED','post_run_reconciliation_attempt_1':'FAIL_HISTORICAL_EVIDENCE','independent_production_acceptance':'NOT_STARTED','scheduler_deployment':'NOT_STARTED','public_projection':'DEFERRED','pe4':'NOT_COMPLETE','phase7a':'ACTIVE','rollback':'NOT_PERFORMED','second_adapter_execution':'NOT_AUTHORIZED'}
for field,expected in LIFECYCLE.items():
 def check(self,field=field,expected=expected):self.assertEqual(R['lifecycle'][field],expected);self.reject(['lifecycle',field],'UNAUTHORIZED_CHANGED_STATE')
 setattr(DurableReconciliationClosureTests,'test_required_lifecycle_'+field,check)
if __name__=='__main__':unittest.main()
