"""Read-only reconciliation tests use synthetic evidence and pure state validators only."""
import ast,contextlib,copy,io,json,os,stat,sys,tempfile,unittest,subprocess,types
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from test_pe4_ha_association_bounded_manual_validation_correction import ROOT,R,M,D,A,C,module
HISTORICAL_SOURCE=subprocess.check_output(['git','show','d767ad429ae0573ffb1411ccb787795063ef647c:tools/hioc-pe4-ha-association-manual-reconcile.py'],cwd=ROOT)
N=types.ModuleType('frozen_historical_reconciler');exec(compile(HISTORICAL_SOURCE,'frozen historical reconciler','exec'),N.__dict__)
# Historical synthetic fixtures only; no historical files are recreated on disk.
P=json.loads((ROOT/M.RECORD).read_bytes());H=R['historical_evidence']['report']
def evidence(h=None):
 h=H if h is None else h
 old_extra=tuple('PRODUCTION_FILES_UNCHANGED' if k=='PROTECTED_PRODUCTION_SURFACES_UNCHANGED' else k for k in M.EXTRA)
 return {'validation.json':M.canonical(h),'result.txt':('\n'.join(k+'='+h[k] for k in M.FIELDS)+'\n').encode(),'report.txt':('\n'.join(k+'='+h[k] for k in old_extra+M.FIELDS)+'\n').encode()}
def state():
 records=[]
 for i in range(25):records.append({'hioc_device_id':'dev_'+format(i,'016x'),'ha_device_id':'synthetic-'+str(i),'association_basis':'unique_mac','status':'ASSOCIATED_STRONG_MAC','first_associated_at':'2026-10-07T03:58:29Z','last_confirmed_at':'2026-10-07T03:58:29Z','observed_ha_version':'2026.9.4','contract_version':'1.0','relationship_status':'COMPLETE'})
 return {'schema_version':'1.1','updated_at':'2026-10-07T03:58:29Z','instance_reference':'PI5_HA','observed_ha_version':'2026.9.4','contract_version':'1.0','associations':records,'binding_history':[],'diagnostics':[{'reason':'REVIEW_ONLY_NO_MAC','count':170},{'reason':'REJECT_INVALID_MAC','count':26},{'reason':'UNMATCHED_STRONG_EVIDENCE','count':8}],'summary':{'associated_devices':25,'entity_memberships':0,'historical_bindings':0,'review_only':170,'rejected':26,'unmatched':8}}
class PrivateFS:
 def __init__(self,value=None):self.value=state() if value is None else value
 def read(self,path,*args):return A.encoded(self.value) if path==A.STATE else (ROOT/A.SCHEMA_PATH).read_bytes()
def compat_payload():
 reg=json.loads((ROOT/'governance/compatibility-contracts.json').read_bytes());entries=[]
 for dep in reg['dependencies']:
  observation={'observed_version':'2026.9.4','capabilities':{k:True for k in A.CAPABILITIES}} if dep['dependency_id']=='ha_core' else {}
  previous={'last_known_compatible_version':'2026.9.4'} if dep['dependency_id']=='ha_core' else {}
  entries.append(C.assess(dep,observation,previous,'2026-10-07T03:58:29Z'))
 return C.summarize(entries,'2026-10-07T03:58:29Z')
class CompatFS:
 def __init__(self,value=None):self.value=compat_payload() if value is None else value
 def read(self,path,*args):return M.canonical(self.value) if path.endswith('compatibility.json') else (ROOT/'governance/compatibility-contracts.json').read_bytes()
class ReconciliationTests(unittest.TestCase):
 def test_exact_historical_evidence_canonical_cross_file_validation(self):self.assertEqual(N.validate_historical(evidence(),M,R,P,C),H)
 def test_historical_fail_or_global_false_cannot_be_rewritten(self):
  for key,value in [('OVERALL_VALIDATION','PASS'),('PRODUCTION_FILES_UNCHANGED','TRUE'),('MANUAL_REVIEW_REQUIRED','FALSE'),('RESULT','FAIL'),('ADAPTER_EXECUTION_COUNT','2')]:
   h=copy.deepcopy(H);h[key]=value
   with self.assertRaises((N.Stop,M.Stop)):N.validate_historical(evidence(h),M,R,P,C)
 def test_historical_inventory_config_truth_cannot_be_overridden(self):
  for key in ('CANONICAL_INVENTORY_UNCHANGED','CONFIG_UNCHANGED','PLATFORM_STATUS_UNCHANGED','PLATFORM_CRON_UNCHANGED'):
   h=copy.deepcopy(H);h[key]='FALSE'
   with self.assertRaises(N.Stop):N.validate_historical(evidence(h),M,R,P,C)
 def test_unknown_extra_raw_field_rejected(self):
  h=copy.deepcopy(H);h['PRIVATE_HOUSEHOLD']='raw'
  with self.assertRaises(M.Stop):N.validate_historical(evidence(h),M,R,P,C)
 def test_canonical_and_strict_json_required(self):
  for raw in (json.dumps(H,indent=2).encode(),b'{"RESULT":"PASS","RESULT":"FAIL"}',b'{"secret":NaN}'):
   files=evidence();files['validation.json']=raw
   with self.assertRaises((N.Stop,M.Stop)):N.validate_historical(files,M,R,P,C)
 def test_result_report_mismatch_rejected(self):
  for key in ('result.txt','report.txt'):
   files=evidence();files[key]+=b'raw extra data\n'
   with self.assertRaises((N.Stop,M.Stop)):N.validate_historical(files,M,R,P,C)
 def test_file_allowlist_exact(self):
  files=evidence();files['private.json']=b'raw'
  with self.assertRaises(N.Stop):N.validate_historical(files,M,R,P,C)
 def test_directory_and_file_security_strict(self):
  directory=SimpleNamespace(st_mode=stat.S_IFDIR|0o700,st_uid=1000,st_nlink=1,st_size=0)
  file=SimpleNamespace(st_mode=stat.S_IFREG|0o600,st_uid=1000,st_nlink=1,st_size=100)
  N.object_security(directory,1000,True);N.object_security(file,1000)
  for key,value in [('st_mode',stat.S_IFREG|0o644),('st_mode',stat.S_IFLNK|0o600),('st_uid',0),('st_nlink',2),('st_size',16385)]:
   bad=copy.copy(file);setattr(bad,key,value)
   with self.assertRaises(N.Stop):N.object_security(bad,1000)
  bad=copy.copy(directory);bad.st_mode=stat.S_IFDIR|0o755
  with self.assertRaises(N.Stop):N.object_security(bad,1000,True)
 def test_evidence_path_forms_fail_before_open(self):
  for path in ('/tmp/other','/tmp/hioc-pe4-ha-association-manual-../secret','/tmp/hioc-pe4-ha-association-manual-OTHER',N.EVIDENCE+'/result.txt'):
   with patch.object(N.os,'open',side_effect=AssertionError('must reject before opening')):
    with self.assertRaises(N.Stop):N.evidence_input(path,1000)
 def test_fd_reads_no_symlink_creation_or_write_flags(self):
  tree=ast.parse(HISTORICAL_SOURCE)
  calls=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='open']
  self.assertEqual(len(calls),3)
  for call in calls:
   flags=ast.unparse(call.args[1]);self.assertIn('O_RDONLY',flags);self.assertIn('O_NOFOLLOW',flags)
   for token in ('O_CREAT','O_WRONLY','O_RDWR','O_TRUNC'):self.assertNotIn(token,flags)
 def test_private_state_valid_schema_and_historical_counts(self):
  with patch.object(M,'namespace',return_value=(True,True)):self.assertTrue(N.private_state(PrivateFS(),D,M,A,H))
 def test_private_state_schema_or_count_drift_fails(self):
  for key in ('associated_devices','review_only','rejected','unmatched','historical_bindings'):
   value=state();value['summary'][key]+=1
   with patch.object(M,'namespace',return_value=(True,True)):
    with self.assertRaises((N.Stop,A.Failure)):N.private_state(PrivateFS(value),D,M,A,H)
  value=state();value['raw_private_extra']='do not expose'
  with patch.object(M,'namespace',return_value=(True,True)):
   with self.assertRaises(A.Failure):N.private_state(PrivateFS(value),D,M,A,H)
 def test_private_state_presence_and_namespace_failures(self):
  for status in ((False,True),(True,False)):
   with patch.object(M,'namespace',return_value=status):
    with self.assertRaises(N.Stop):N.private_state(PrivateFS(),D,M,A,H)
 def test_compatibility_current_state_semantics(self):
  with patch.object(N,'SOURCE',ROOT):self.assertTrue(N.compatibility_state(CompatFS(),M,C,H))
 def test_compatibility_version_status_or_capability_drift_fails(self):
  for key,value in [('observed_version','2026.9.5'),('status','INCOMPATIBLE'),('failed_capability','authentication'),('last_known_compatible_version','2026.8.1')]:
   payload=compat_payload();next(x for x in payload['dependencies'] if x['dependency_id']=='ha_core')[key]=value
   with patch.object(N,'SOURCE',ROOT):
    with self.assertRaises(N.Stop):N.compatibility_state(CompatFS(payload),M,C,H)
 def test_current_comparison_never_recreates_inventory_history(self):
  with patch.object(M,'protected_snapshot',return_value={'protected':'RAM_ONLY'}) as snapshot,patch.object(N,'private_state',return_value=True),patch.object(N,'compatibility_state',return_value=True):
   self.assertTrue(N.reconcile_checks(M,D,PrivateFS(),{},H,A,C));self.assertEqual(snapshot.call_count,2)
   for call in snapshot.call_args_list:self.assertIs(call.kwargs['include_inventory'],False)
 def test_final_protected_snapshot_drift_fails(self):
  with patch.object(M,'protected_snapshot',side_effect=[{'safe':1},{'safe':2}]),patch.object(N,'private_state',return_value=True),patch.object(N,'compatibility_state',return_value=True):
   with self.assertRaises(N.Stop):N.reconcile_checks(M,D,PrivateFS(),{},H,A,C)
 def test_no_adapter_credential_network_or_production_writer_calls(self):
  tree=ast.parse(HISTORICAL_SOURCE);calls=[ast.unparse(n.func) for n in ast.walk(tree) if isinstance(n,ast.Call)]
  for token in ('invoke_once','run_cycle','credential','read_credential','network','connect','socket.socket','StateStore','write_json','update_status','recovery','deploy','unlink','mkdir','os.replace','write_evidence','Popen'):
   self.assertFalse(any(name==token or name.endswith('.'+token) for name in calls),token)
 def test_sanitized_report_rejects_private_values(self):
  report={k:'UNKNOWN' for k in N.REPORT_FIELDS};report.update(TARGET='PI3 NUT&PIHOLE',FAILURE_STAGE='NONE',RECONCILIATION='PASS');self.assertIn('RECONCILIATION=PASS',N.report_text(report))
  for key in ('CURRENT_PRIVATE_STATE_VALIDATION','HISTORICAL_ADAPTER_RESULT','FAILURE_STAGE'):
   bad=dict(report);bad[key]='private household identifier'
   with self.assertRaises(N.Stop):N.report_text(bad)
 def test_reconciler_stdout_only_and_no_repository_closure(self):
  text=HISTORICAL_SOURCE.decode('utf8');self.assertNotIn('write_bytes',text);self.assertNotIn('write_text',text);self.assertNotIn('tempfile',text);self.assertFalse(R['reconciliation_rules']['repository_closure_automatic'])
 def test_review_only_block_no_sync_execution_or_destructive_shell(self):
  doc=(ROOT/'docs/PE4_HOME_ASSISTANT_ASSOCIATION_BOUNDED_MANUAL_VALIDATION_CORRECTION.md').read_text(encoding='utf8');block=doc.split('```sh',1)[1].split('```',1)[0]
  self.assertIn('--evidence-directory '+N.EVIDENCE,block)
  for token in ('git pull','git fetch','manual-validate.py','set -','pipefail','exit','exec ','logout'):self.assertNotIn(token,block)
  self.assertIn('FOR REVIEW ONLY - DO NOT RUN WITHOUT SEPARATE AUTHORIZATION',doc)
class SyntheticReconciliationFlowTests(unittest.TestCase):
 def run_flow(self,broken=False):
  from test_pe4_ha_association_bounded_manual_validation_correction import CL
  class FS:
   def read(self,path,*args):
    if path==A.STATE:return A.encoded(state())
    if path==A.SCHEMA_PATH:return (ROOT/A.SCHEMA_PATH).read_bytes()
    if path=='state/platform/compatibility.json':return M.canonical(compat_payload())
    return (ROOT/'governance/compatibility-contracts.json').read_bytes()
  d=SimpleNamespace(NativeFS=lambda *a:FS())
  def load(path,name):
   return M if 'manual-validate.py' in str(path) else C if 'compatibility.py' in str(path) else d if 'deploy.py' in str(path) else A
  captured=io.StringIO();files=evidence()
  if broken:files['report.txt']+=b'INVALID_EXTRA'
  with contextlib.ExitStack() as stack:
   stack.enter_context(patch.dict(sys.modules,{'pwd':SimpleNamespace(getpwnam=lambda n:SimpleNamespace(pw_uid=1000)),'grp':SimpleNamespace(getgrnam=lambda n:SimpleNamespace(gr_gid=1000))}))
   stack.enter_context(patch.object(N.sys,'platform','linux'));stack.enter_context(patch.object(N.os,'environ',N.ENV))
   for name in ('getuid','geteuid','getgid','getegid'):stack.enter_context(patch.object(N.os,name,lambda:1000,create=True))
   stack.enter_context(patch.object(N.socket,'gethostname',return_value='nutandpihole'))
   stack.enter_context(patch.object(N,'source_gate'))
   stack.enter_context(patch.object(N,'SOURCE',ROOT));stack.enter_context(patch.object(N,'module',side_effect=load))
   stack.enter_context(patch.object(M,'source_binding',return_value=(CL,R)))
   stack.enter_context(patch.object(N,'evidence_input',return_value=files))
   stack.enter_context(patch.object(M,'protected_snapshot',return_value={'SAFE':'RAM_ONLY'}))
   stack.enter_context(patch.object(M,'namespace',return_value=(True,True)))
   for target,name in ((M,'invoke_once'),(A,'run_cycle'),(A,'main'),(C,'update_status'),(M,'write_evidence')):
    stack.enter_context(patch.object(target,name,side_effect=AssertionError('prohibited operation')))
   with contextlib.redirect_stdout(captured):rc=N.main(['--approved-correction-commit','a'*40,'--evidence-directory',N.EVIDENCE])
  return rc,dict(line.split('=',1) for line in captured.getvalue().splitlines())
 def test_read_only_success_no_adapter_writer_or_network_path(self):
  rc,r=self.run_flow();self.assertEqual(rc,0);self.assertEqual(r['RECONCILIATION'],'PASS');self.assertEqual(r['HISTORICAL_WRAPPER_OVERALL_VALIDATION'],'FAIL');self.assertEqual(r['HISTORICAL_PRODUCTION_FILES_UNCHANGED'],'FALSE');self.assertEqual(r['PROTECTED_PRODUCTION_SURFACES_UNCHANGED'],'TRUE');self.assertEqual(r['EXECUTION_TIME_COMPARISON_RECREATED'],'FALSE')
  for k in ('ADAPTER_EXECUTED_BY_RECONCILIATION','CREDENTIAL_ACCESSED_BY_RECONCILIATION','HA_NETWORK_ATTEMPTED_BY_RECONCILIATION','PRODUCTION_MUTATED_BY_RECONCILIATION','EXISTING_EVIDENCE_REWRITTEN','RAW_PRIVATE_DATA_EXPOSED'):self.assertEqual(r[k],'FALSE')
 def test_broken_evidence_fails_safely_without_private_diagnostics(self):
  rc,r=self.run_flow(True);self.assertEqual(rc,1);self.assertEqual(r['RECONCILIATION'],'FAIL');self.assertEqual(r['FAILURE_STAGE'],'HISTORICAL_EVIDENCE');self.assertNotIn('INVALID_EXTRA',str(r))

if __name__=='__main__':unittest.main()
