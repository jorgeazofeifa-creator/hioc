"""Repository-only authority tests and synthetic durable reconciliation; no live execution."""
import ast,contextlib,copy,hashlib,io,json,subprocess,sys,unittest
from types import SimpleNamespace
from unittest.mock import patch
from test_pe4_ha_association_bounded_manual_validation_correction import ROOT,R,M,D,A,C,CL,module
from test_pe4_ha_association_manual_reconciliation import H,state,PrivateFS,CompatFS,compat_payload
N=module('tools/hioc-pe4-ha-association-manual-reconcile.py','successor_reconciler_definitions')
Q=json.loads((ROOT/N.AUTHORITY).read_bytes());S=json.loads((ROOT/N.AUTHORITY.replace('.json','.schema.json')).read_bytes())
SOURCE=(ROOT/'tools/hioc-pe4-ha-association-manual-reconcile.py').read_text(encoding='utf8')
def git_input(args):
    return subprocess.check_output(['git',*args[1:]],cwd=ROOT)
def report():
    v={k:'UNKNOWN' for k in N.REPORT_FIELDS};v.update(N.KNOWN_LIMITATION);v.update({k:'FALSE' for k in N.NO_ACTIVITY});v.update(TARGET='PI3 NUT&PIHOLE',FAILURE_STAGE='TARGET',RECONCILIATION='FAIL');return v
class EvidenceAuthorityTests(unittest.TestCase):
 def test_canonical_closed_record_and_schema(self):
  M.schema_validate(Q,S)
  for path,obj in ((N.AUTHORITY,Q),(N.AUTHORITY.replace('.json','.schema.json'),S)):self.assertEqual((ROOT/path).read_bytes(),M.canonical(obj))
 def test_record_rejects_extra_and_changed_authorization(self):
  for key,value in [('raw',True),('second_adapter_execution_authorized',True),('adapter_rerun',True),('historical_evidence_recreated',True),('original_ephemeral_directory_present',True),('matching_ephemeral_directories',1)]:
   q=copy.deepcopy(Q);q[key]=value
   with self.assertRaises(M.Stop):M.schema_validate(q,S)
 def test_predecessor_record_and_schema_frozen(self):
  for key in ('predecessor_record','predecessor_schema'):
   item=Q[key];raw=subprocess.check_output(['git','show',N.BASE+':'+item['path']],cwd=ROOT)
   self.assertEqual(raw,(ROOT/item['path']).read_bytes());self.assertEqual(M.sha(raw),item['sha256']);self.assertEqual(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),item['git_blob'])
 def test_exact_committed_report_authority(self):
  with patch.object(N,'SOURCE',ROOT),patch.object(N,'command',side_effect=git_input):self.assertEqual(N.validate_committed_report(M,R),H)
 def test_arbitrary_or_changed_historical_report_rejected(self):
  for key,value in [('RESULT','FAIL'),('OVERALL_VALIDATION','PASS'),('PRODUCTION_FILES_UNCHANGED','TRUE'),('ADAPTER_EXECUTION_COUNT','2'),('CONFIG_UNCHANGED','FALSE'),('CANONICAL_INVENTORY_UNCHANGED','FALSE'),('OBSERVED_HA_VERSION','2026.9.5')]:
   q=copy.deepcopy(R);q['historical_evidence']['report'][key]=value
   with patch.object(N,'SOURCE',ROOT),patch.object(N,'command',side_effect=git_input):
    with self.assertRaises((M.Stop,N.Stop)):N.validate_committed_report(M,q)
 def test_record_hash_drift_rejected(self):
  with patch.object(N,'SOURCE',ROOT),patch.object(N,'command',return_value=b'{}'):
   with self.assertRaises(N.Stop):N.validate_committed_report(M,R)
 def test_schema_hash_drift_rejected(self):
  def altered(args):return b'{}' if args[-1].endswith('.schema.json') else git_input(args)
  with patch.object(N,'SOURCE',ROOT),patch.object(N,'command',side_effect=altered):
   with self.assertRaises(N.Stop):N.validate_committed_report(M,R)
 def gate(self,override=None):
  def response(args):
   a=args[1:]
   if a[0]=='show' and ':' in a[-1]:return (ROOT/a[-1].split(':',1)[1]).read_bytes()
   values={('branch','--show-current'):'main',('rev-parse','HEAD'):'a'*40,('rev-parse','origin/main'):'a'*40,('rev-parse','HEAD^'):N.BASE,('rev-list','--left-right','--count','HEAD...origin/main'):'0\t0',('show','-s','--format=%s','HEAD'):'PE-4: correct reconciliation evidence authority',('status','--porcelain','--untracked-files=all'):''}
   if a[:2]==['rev-parse','--git-path']:return ('nonexistent-operation-check/'+a[-1]).encode()
   return (override.get(tuple(a),values.get(tuple(a),'')) if override else values.get(tuple(a),'')).encode()
  with patch.object(N,'SOURCE',ROOT),patch.object(N,'command',side_effect=response):N.source_gate('a'*40)
 def test_successor_source_gate_exact_main_parent_subject_clean(self):self.gate()
 def test_successor_source_gate_rejects_wrong_parent(self):
  with self.assertRaises(N.Stop):self.gate({('rev-parse','HEAD^'):'b'*40})
 def test_successor_source_gate_rejects_wrong_subject(self):
  with self.assertRaises(N.Stop):self.gate({('show','-s','--format=%s','HEAD'):'unapproved'})
 def test_successor_source_gate_rejects_dirty_or_wrong_origin(self):
  for override in ({('status','--porcelain','--untracked-files=all'):'?? stray'}, {('rev-parse','origin/main'):'b'*40}):
   with self.assertRaises(N.Stop):self.gate(override)
 def test_source_authority_checks_frozen_deployment_and_tool(self):
  def response(args):
   if args[1]=='rev-parse' and args[2].startswith('a'*40):return (Q['reconciliation_tool']['git_blob']+'\n').encode()
   return git_input(args)
  with patch.object(N,'SOURCE',ROOT),patch.object(N,'command',side_effect=response):self.assertEqual(N.source_authority(M,'a'*40),(CL,R))
 def test_source_authority_rejects_successor_tool_blob_drift(self):
  def response(args):return b'0'*40 if args[1]=='rev-parse' and args[2].startswith('a'*40) else git_input(args)
  with patch.object(N,'SOURCE',ROOT),patch.object(N,'command',side_effect=response):
   with self.assertRaises(N.Stop):N.source_authority(M,'a'*40)
 def test_missing_ephemeral_fact_and_zero_matching_recorded(self):
  self.assertFalse(Q['original_ephemeral_directory_present']);self.assertEqual(Q['matching_ephemeral_directories'],0);self.assertEqual(Q['missing_evidence_fact'],'EPHEMERAL_EVIDENCE_DIRECTORY_CURRENTLY_ABSENT');self.assertEqual(Q['disappearance_cause'],'NOT_ESTABLISHED_NO_INFERENCE')
 def test_operator_attempt_and_diagnostic_provenance(self):
  a=Q['attempt_1'];self.assertEqual(a['provenance'],'OPERATOR_SUPPLIED_PRODUCTION_EVIDENCE');self.assertEqual(a['invocations'],1);self.assertEqual(a['outer_return_code'],1);self.assertFalse(a['durable_checks_reached']);self.assertEqual(a['report']['FAILURE_STAGE'],'HISTORICAL_EVIDENCE');self.assertEqual(a['report']['CURRENT_PRIVATE_STATE_VALIDATION'],'UNKNOWN');self.assertEqual(Q['diagnostics']['presence_report']['MATCHING_EVIDENCE_DIRECTORY_COUNT'],'0')
 def test_no_original_artifact_hash_claim(self):self.assertEqual(Q['original_artifact_identities'],'NOT_INDEPENDENTLY_RECORDED_BEFORE_LOSS_NOT_CLAIMED')
 def test_three_authority_classes_separate(self):self.assertEqual(len(Q['evidence_classes']),3);self.assertEqual(Q['original_artifact_revalidation'],'UNAVAILABLE');self.assertEqual(Q['durable_state_reconciliation'],'NOT_PERFORMED_UNDER_SUCCESSOR_AUTHORITY')
 def test_no_ephemeral_argument_reader_or_creator(self):
  for token in ('evidence_input','--evidence-directory','/tmp/hioc-pe4','tempfile','mkdir','write_bytes','write_text','unlink','rmtree','os.open'):self.assertNotIn(token,SOURCE)
 def test_no_prohibited_calls(self):
  calls=[ast.unparse(n.func) for n in ast.walk(ast.parse(SOURCE)) if isinstance(n,ast.Call)]
  for token in ('invoke_once','run_cycle','read_credential','connect','socket.socket','StateStore','write_json','update_status','recovery','deploy','unlink','mkdir','os.replace','write_evidence','Popen','prerequisites'):
   self.assertFalse(any(x==token or x.endswith('.'+token) for x in calls),token)
 def test_no_whole_tree_or_inventory_recreation(self):
  self.assertNotIn('walk(',SOURCE);self.assertNotIn('rglob(',SOURCE);self.assertIn('include_inventory=False',SOURCE);self.assertTrue(Q['no_execution_time_inventory_recreation'])
 def test_protected_surface_contract_unchanged(self):self.assertEqual(Q['protected_surface_policy'],R['protected_surface_policy']);self.assertEqual(len(CL['dependencies']),5);self.assertEqual(len(CL['deployed_targets']),9)
 def test_current_private_counts_and_version(self):
  with patch.object(M,'namespace',return_value=(True,True)):self.assertTrue(N.private_state(PrivateFS(),D,M,A,H))
 def test_current_private_count_drift_rejected(self):
  for key in ('associated_devices','review_only','rejected','unmatched','historical_bindings'):
   v=state();v['summary'][key]+=1
   with patch.object(M,'namespace',return_value=(True,True)):
    with self.assertRaises((N.Stop,A.Failure)):N.private_state(PrivateFS(v),D,M,A,H)
 def test_current_private_version_drift_rejected(self):
  v=state();v['observed_ha_version']='2026.9.5'
  with patch.object(M,'namespace',return_value=(True,True)):
   with self.assertRaises((N.Stop,A.Failure)):N.private_state(PrivateFS(v),D,M,A,H)
 def test_current_private_transaction_or_absence_rejected(self):
  for value in ((True,False),(False,True)):
   with patch.object(M,'namespace',return_value=value):
    with self.assertRaises(N.Stop):N.private_state(PrivateFS(),D,M,A,H)
 def test_current_compatibility_semantics(self):
  with patch.object(N,'SOURCE',ROOT):self.assertTrue(N.compatibility_state(CompatFS(),M,C,H))
 def test_current_compatibility_drift_rejected(self):
  for key,value in [('status','INCOMPATIBLE'),('observed_version','2026.9.5'),('failed_capability','authentication')]:
   v=compat_payload();next(e for e in v['dependencies'] if e['dependency_id']=='ha_core')[key]=value
   with patch.object(N,'SOURCE',ROOT):
    with self.assertRaises(N.Stop):N.compatibility_state(CompatFS(v),M,C,H)
 def test_current_compatibility_capability_and_summary_drift_rejected(self):
  for kind in ('capability','summary'):
   v=compat_payload()
   if kind=='capability':next(e for e in v['dependencies'] if e['dependency_id']=='ha_core')['capabilities']['authentication']=False
   else:v['dependency_count']+=1
   with patch.object(N,'SOURCE',ROOT):
    with self.assertRaises((N.Stop,M.Stop)):N.compatibility_state(CompatFS(v),M,C,H)
 def test_current_protected_stability_and_no_inventory(self):
  with patch.object(M,'protected_snapshot',return_value={'safe':1}) as snap,patch.object(N,'private_state'),patch.object(N,'compatibility_state'):
   self.assertTrue(N.reconcile_checks(M,D,PrivateFS(),CL,H,A,C));self.assertEqual(snap.call_count,2);self.assertTrue(all(c.kwargs['include_inventory'] is False for c in snap.call_args_list))
 def test_current_protected_drift_rejected(self):
  with patch.object(M,'protected_snapshot',side_effect=[{'safe':1},{'safe':2}]),patch.object(N,'private_state'),patch.object(N,'compatibility_state'):
   with self.assertRaises(N.Stop):N.reconcile_checks(M,D,PrivateFS(),CL,H,A,C)
 def test_known_loss_cannot_be_unknown_even_on_failure(self):
  for k in N.KNOWN_LIMITATION:
   v=report();v[k]='UNKNOWN'
   with self.assertRaises(N.Stop):N.report_text(v)
 def test_success_requires_all_gates_and_limitation(self):
  v=report();v.update(N.SUCCESS,SOURCE_EVIDENCE_AUTHORITY_COMMIT='a'*40,RECONCILIATION='PASS');self.assertIn('RECONCILIATION=PASS',N.report_text(v))
  for k in N.SUCCESS:
   bad=dict(v);bad[k]='UNKNOWN'
   with self.assertRaises(N.Stop):N.report_text(bad)
 def test_no_activity_cannot_be_true(self):
  for k in N.NO_ACTIVITY:
   v=report();v[k]='TRUE'
   with self.assertRaises(N.Stop):N.report_text(v)
 def test_finite_sanitized_report(self):
  v=report();self.assertEqual(len(N.report_text(v).splitlines()),30)
  for k in N.REPORT_FIELDS:
   bad=dict(v);bad[k]='private household identifier'
   with self.assertRaises(N.Stop):N.report_text(bad)
 def test_durability_rule_documented_and_closed(self):
  self.assertEqual(len(Q['future_evidence_durability_rule']['alternatives']),3)
  for path in ('docs/HIOC_MASTER_PLAN.md','docs/OPERATIONS.md','DECISIONS.md','docs/PE4_HOME_ASSISTANT_ASSOCIATION_RECONCILIATION_EVIDENCE_AUTHORITY_CORRECTION.md'):
   t=(ROOT/path).read_text(encoding='utf8');self.assertIn('Closure-critical evidence must not rely solely on ephemeral /tmp storage',t);self.assertIn('Hashes and metadata cannot recover lost bytes',t)
 def test_lifecycle_no_second_execution_or_acceptance(self):
  self.assertEqual(Q['lifecycle']['second_adapter_execution'],'NOT_AUTHORIZED');self.assertEqual(Q['lifecycle']['independent_production_acceptance'],'NOT_STARTED');self.assertEqual(Q['lifecycle']['pe4'],'NOT_COMPLETE');self.assertFalse(Q['second_adapter_execution_authorized'])
 def test_future_block_separate_review_only_without_ephemeral_argument(self):
  t=(ROOT/'docs/PE4_HOME_ASSISTANT_ASSOCIATION_RECONCILIATION_EVIDENCE_AUTHORITY_CORRECTION.md').read_text(encoding='utf8');b=t.split('```sh',1)[1].split('```',1)[0]
  self.assertIn('FOR REVIEW ONLY - DO NOT RUN WITHOUT SEPARATE AUTHORIZATION',t);self.assertIn('--approved-evidence-authority-commit',b);self.assertIn('-I -B -S',b)
  for token in ('--evidence-directory','git pull','git fetch','manual-validate.py','set -','pipefail','exit','exec ','logout'):self.assertNotIn(token,b)
class SyntheticSuccessorFlowTests(unittest.TestCase):
 def flow(self,broken=None,args=None):
  class FS:
   def read(self,path,*args):
    if path==A.STATE:return A.encoded(state())
    if path==A.SCHEMA_PATH:return (ROOT/A.SCHEMA_PATH).read_bytes()
    if path=='state/platform/compatibility.json':return M.canonical(compat_payload())
    return (ROOT/'governance/compatibility-contracts.json').read_bytes()
  d=SimpleNamespace(NativeFS=lambda *a:FS())
  def load(path,name):return M if 'manual-validate' in str(path) else C if 'compatibility.py' in str(path) else d if 'deploy.py' in str(path) else A
  captured=io.StringIO()
  with contextlib.ExitStack() as stack:
   stack.enter_context(patch.dict(sys.modules,{'pwd':SimpleNamespace(getpwnam=lambda n:SimpleNamespace(pw_uid=1000)),'grp':SimpleNamespace(getgrnam=lambda n:SimpleNamespace(gr_gid=1000))}))
   stack.enter_context(patch.object(N.sys,'platform','linux'));stack.enter_context(patch.object(N.os,'environ',N.ENV))
   for name in ('getuid','geteuid','getgid','getegid'):stack.enter_context(patch.object(N.os,name,lambda:1000,create=True))
   stack.enter_context(patch.object(N.socket,'gethostname',return_value='nutandpihole'));stack.enter_context(patch.object(N,'SOURCE',ROOT));stack.enter_context(patch.object(N,'module',side_effect=load));stack.enter_context(patch.object(N,'source_gate'));stack.enter_context(patch.object(N,'source_authority',return_value=(CL,R)));stack.enter_context(patch.object(N,'command',side_effect=git_input));stack.enter_context(patch.object(M,'namespace',return_value=(True,True)))
   stack.enter_context(patch.object(M,'protected_snapshot',return_value={'safe':1}))
   for target,name in ((M,'invoke_once'),(M,'write_evidence'),(A,'run_cycle'),(A,'main'),(C,'update_status')):stack.enter_context(patch.object(target,name,side_effect=AssertionError('prohibited')))
   if broken:stack.enter_context(patch.object(N,broken,side_effect=N.Stop))
   with contextlib.redirect_stdout(captured):rc=N.main(args or ['--approved-evidence-authority-commit','a'*40])
  return rc,dict(line.split('=',1) for line in captured.getvalue().splitlines())
 def test_success_preserves_history_with_mandatory_limitation(self):
  rc,v=self.flow();self.assertEqual(rc,0);self.assertEqual(v['RECONCILIATION'],'PASS');self.assertEqual(v['HISTORICAL_WRAPPER_OVERALL_VALIDATION'],'FAIL');self.assertEqual(v['HISTORICAL_PRODUCTION_FILES_UNCHANGED'],'FALSE');self.assertEqual(v['HISTORICAL_ADAPTER_EXECUTION_COUNT'],'1');self.assertEqual(v['ORIGINAL_EPHEMERAL_EVIDENCE_LIMITATION'],'RECORDED');self.assertTrue(all(v[k]=='FALSE' for k in N.NO_ACTIVITY))
 def test_historical_gate_failure_known_loss_still_explicit(self):
  rc,v=self.flow('validate_committed_report');self.assertEqual(rc,1);self.assertEqual(v['FAILURE_STAGE'],'HISTORICAL_EVIDENCE');self.assertEqual(v['ORIGINAL_EPHEMERAL_EVIDENCE_REVALIDATION'],'UNAVAILABLE')
 def test_current_private_failure_safe(self):
  rc,v=self.flow('private_state');self.assertEqual(rc,1);self.assertEqual(v['FAILURE_STAGE'],'PRIVATE_STATE');self.assertEqual(v['ORIGINAL_EPHEMERAL_EVIDENCE_LIMITATION'],'RECORDED')
 def test_arbitrary_report_and_old_evidence_arguments_rejected(self):
  for args in (['--report','{}'],['--approved-correction-commit','a'*40,'--evidence-directory','/tmp/old']):
   rc,v=self.flow(args=args);self.assertEqual(rc,1);self.assertEqual(v['FAILURE_STAGE'],'TARGET')
if __name__=='__main__':unittest.main()
