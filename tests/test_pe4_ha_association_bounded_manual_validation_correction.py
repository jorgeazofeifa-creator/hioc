"""Synthetic correction/protected-surface tests; immutable adapter is never executed."""
import ast,contextlib,copy,hashlib,importlib.util,json,stat,subprocess,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
def module(path,name):
 spec=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
M=module('tools/hioc-pe4-ha-association-manual-validate.py','corrected_manual')
D=module('tools/hioc-pe4-ha-association-deploy.py','frozen_deployment')
A=module('pi4/lib/hioc/home_assistant_association.py','frozen_adapter_definitions')
C=module('pi4/lib/hioc/core/compatibility.py','frozen_compatibility_definitions')
RECORD=ROOT/M.CORRECTION
R=json.loads(RECORD.read_bytes());S=json.loads(RECORD.with_suffix('.schema.json').read_bytes());CL=json.loads((ROOT/M.CLOSURE).read_bytes())
class FakeFS:
 def __init__(self):
  self.data={x['path']:(ROOT/x['path']).read_bytes().replace(b'\r\n',b'\n') for x in CL['dependencies']+CL['deployed_targets']}
  self.modes={x['path']:int(x.get('mode','0644'),8) if x.get('mode')!='NO_SPECIAL_OR_GROUP_WORLD_WRITE' else 0o644 for x in CL['dependencies']+CL['deployed_targets']}
  prior=b'HIOC_HOME=/home/jazofv1/hioc\n';candidate=D.endpoint_config(prior)
  intent={'version':1,'source_commit':M.DEPLOYED,'created_files':[x['path'] for x in CL['deployed_targets']],'created_directories':[],'lock_created':True,'endpoint_added':True,'config_mode':'0600','prior_sha256':M.sha(prior),'candidate_sha256':M.sha(candidate),'targets':{x['path']:x['sha256'] for x in CL['deployed_targets']}}
  raw=D.canonical(intent)
  self.data.update({D.CONFIG:candidate,D.LOCK:b'',D.TX+'/intent.json':raw,D.TX+'/config-prior':prior,D.TX+'/config-candidate':candidate,D.TX+'/committed.json':D.canonical({'status':'COMMITTED','source_commit':M.DEPLOYED,'intent_sha256':M.sha(raw)}),'state/inventory/inventory.json':b'SYNTHETIC_PRIVATE_INVENTORY','pi4/bin/hioc-platform-status.py':b'SYNTHETIC_PLATFORM'})
  self.modes.update({p:0o600 for p in self.data if p not in self.modes});self.directories={D.ASSOCIATIONS};self.uid=self.gid=1000
 def read(self,path,mode=None):
  if path not in self.data:return None
  if mode is not None:M.require(self.modes[path]==mode)
  return self.data[path]
 def info(self,path):
  return SimpleNamespace(st_mode=(stat.S_IFDIR|0o700) if path in self.directories else stat.S_IFREG|self.modes[path],st_uid=1000,st_gid=1000,st_nlink=1)
 def check_directory(self,path,mode=None):return path==D.TX or path in self.directories
 def parents(self,path):return D.NativeFS.parents(self,path)
class FakeActive:
 def lstat(self):return SimpleNamespace(st_mode=stat.S_IFLNK|0o777,st_uid=1000,st_gid=1000)
 def resolve(self):return D.ENVIRONMENT
class FakeHome:
 def __truediv__(self,path):return FakeActive()
def protected(fs,include_inventory=True,runtime_error=False,cron_error=False):
 original=M.sha
 def digest(b):return CL['platform_status_sha256'] if b==b'SYNTHETIC_PLATFORM' else original(b)
 with contextlib.ExitStack() as stack:
  stack.enter_context(patch.object(M,'sha',side_effect=digest));stack.enter_context(patch.object(M,'HOME',FakeHome()))
  stack.enter_context(patch.object(M.os,'readlink',return_value='environments/cpython311-websockets16.1.1-lock-v1'))
  stack.enter_context(patch.object(M,'runtime_probe',side_effect=M.Stop if runtime_error else lambda d:None))
  stack.enter_context(patch.object(M,'scheduler',side_effect=M.Stop if cron_error else lambda:CL['existing_platform_cron'].encode()))
  stack.enter_context(patch.object(M.os,'walk',side_effect=AssertionError('whole tree traversal forbidden')))
  return M.protected_snapshot(fs,CL,D,include_inventory=include_inventory)
class CorrectionTests(unittest.TestCase):
 def test_canonical_closed_correction_record(self):
  M.schema_validate(R,S);self.assertEqual(RECORD.read_bytes(),M.canonical(R));self.assertEqual(RECORD.with_suffix('.schema.json').read_bytes(),M.canonical(S))
 def test_policy_extra_or_changed_properties_rejected(self):
  for key,value in [('unexpected',True),('protected_surface_policy',{}),('second_adapter_execution_authorized',True)]:
   bad=copy.deepcopy(R);bad[key]=value
   with self.assertRaises(M.Stop):M.schema_validate(bad,S)
 def test_historical_raw_report_exact_operator_request(self):
  h=R['historical_evidence']['report']
  expected=dict(RESULT='PASS',ERROR_CODE='NONE',FAILURE_STAGE='NONE',COMPATIBILITY_STATUS='COMPATIBLE',OBSERVED_HA_VERSION='2026.9.4',ASSOCIATED_COUNT='25',REVIEW_ONLY_COUNT='170',REJECTED_COUNT='26',UNMATCHED_COUNT='8',HISTORICAL_BINDING_COUNT='0',STATE_PUBLISHED='TRUE',LAST_KNOWN_GOOD_PRESERVED='FALSE')
  self.assertEqual({k:h[k] for k in M.FIELDS},expected)
  old_extra=tuple('PRODUCTION_FILES_UNCHANGED' if k=='PROTECTED_PRODUCTION_SURFACES_UNCHANGED' else k for k in M.EXTRA)
  self.assertEqual(R['historical_evidence']['exact_report_text'],'\n'.join(k+'='+h[k] for k in old_extra+M.FIELDS)+'\n')
 def test_historical_fail_and_adapter_pass_distinct(self):
  h=R['historical_evidence']['report'];self.assertEqual((h['PRODUCTION_FILES_UNCHANGED'],h['OVERALL_VALIDATION'],h['RESULT']),('FALSE','FAIL','PASS'));self.assertEqual(h['ADAPTER_EXECUTION_COUNT'],'1');self.assertEqual(h['ADAPTER_RETURN_CODE'],'0');self.assertEqual(h['OBSERVED_HA_VERSION'],'2026.9.4')
 def test_diagnostics_inconclusive_and_directory_not_cause(self):
  self.assertEqual(R['diagnostics'][0]['result'],'INCONCLUSIVE');self.assertFalse(R['diagnostics'][1]['directory_timestamps_in_original_equality']);self.assertFalse(R['diagnostics'][1]['direct_cause_established']);self.assertFalse(R['diagnostics'][2]['original_mismatch_cause_proved']);self.assertEqual(R['diagnostics'][2]['current_file_count'],22)
 def test_no_adapter_defect_or_second_execution_authority(self):
  self.assertFalse(R['adapter_defect_established']);self.assertFalse(R['second_adapter_execution_authorized']);self.assertFalse(R['automatic_retry']);self.assertEqual(R['post_run_reconciliation'],'NOT_PERFORMED')
 def test_prior_preparation_and_closure_bytes_immutable(self):
  for key in ('preparation','preparation_schema','deployment_closure','deployment_closure_schema'):
   x=R[key];raw=subprocess.check_output(['git','show',M.BASE+':'+x['path']],cwd=ROOT);self.assertEqual(raw,(ROOT/x['path']).read_bytes().replace(b'\r\n',b'\n'));self.assertEqual(M.sha(raw),x['sha256'])
 def test_corrected_wrapper_and_reconciler_identity(self):
  for key in ('corrected_wrapper','reconciliation_tool'):
   x=R[key];b=subprocess.check_output(['git','show','d767ad429ae0573ffb1411ccb787795063ef647c:'+x['path']],cwd=ROOT) if key=='reconciliation_tool' else (ROOT/x['path']).read_bytes().replace(b'\r\n',b'\n');self.assertEqual(M.sha(b),x['sha256']);self.assertEqual(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),x['git_blob'])
 def test_immutable_deployed_source_identity(self):
  for key in ('module','entrypoint','compatibility','deployment_helper'):
   x=R['sources'][key];raw=subprocess.check_output(['git','show',M.DEPLOYED+':'+x['path']],cwd=ROOT);self.assertEqual(raw,(ROOT/x['path']).read_bytes().replace(b'\r\n',b'\n'));self.assertEqual(M.sha(raw),x['sha256'])
 def test_explicit_protected_contract_no_global_walk(self):
  p=R['protected_surface_policy'];self.assertFalse(p['whole_tree_walk']);self.assertFalse(p['ad_hoc_exclusion_list']);self.assertEqual((len(p['five_dependencies']),len(p['six_runtime_governance'])),(5,6));self.assertEqual(len(p['deployed_adapter_entrypoint_compatibility']),3)
  source=(ROOT/'tools/hioc-pe4-ha-association-manual-validate.py').read_text(encoding='utf8');self.assertNotIn('production_snapshot(',source);self.assertNotIn('os.walk(',source);self.assertIn('PROTECTED_PRODUCTION_SURFACES_UNCHANGED',source)
 def test_unrelated_state_history_log_churn_ignored(self):
  fs=FakeFS();before=protected(fs)
  for path in ('history/host.csv','logs/engine.log','state/events/events.json','state/incidents/active.json','state/forecast.json','state/statistics.json','state/inventory/independent-output.json'):fs.data[path]=b'churn';fs.modes[path]=0o600
  self.assertEqual(before,protected(fs))
 def test_changed_adapter_fails(self):self.bad_file('pi4/lib/hioc/home_assistant_association.py')
 def test_changed_entrypoint_fails(self):self.bad_file('pi4/bin/hioc-home-assistant-association.py')
 def test_changed_compatibility_module_fails(self):self.bad_file('pi4/lib/hioc/core/compatibility.py')
 def test_changed_dependency_fails(self):
  for x in CL['dependencies']:self.bad_file(x['path'])
 def test_changed_runtime_governance_fails(self):
  for x in CL['deployed_targets']:
   if x['classification']=='C_RUNTIME_GOVERNANCE':self.bad_file(x['path'])
 def test_changed_config_fails(self):self.bad_file(D.CONFIG)
 def test_changed_platform_status_fails(self):self.bad_file('pi4/bin/hioc-platform-status.py')
 def test_changed_journal_fails(self):
  for name in M.JOURNAL_FILES:self.bad_file(D.TX+'/'+name)
 def bad_file(self,path):
  fs=FakeFS();fs.data[path]=b'changed'
  with self.assertRaises((M.Stop,D.Failure,ValueError)):protected(fs)
 def test_execution_time_inventory_kept_separate(self):
  fs=FakeFS();before=protected(fs);before_reconcile=protected(fs,False);fs.data['state/inventory/inventory.json']=b'normal current inventory change'
  self.assertNotEqual(before,protected(fs));self.assertEqual(before_reconcile,protected(fs,False));self.assertEqual(R['historical_evidence']['report']['CANONICAL_INVENTORY_UNCHANGED'],'TRUE')
 def test_cron_or_scheduler_drift_fails(self):
  with self.assertRaises(M.Stop):protected(FakeFS(),cron_error=True)
  raw=CL['existing_platform_cron'].encode()+b'\n';self.assertEqual(M.validate_cron(raw),raw)
  for value in (raw.replace(b'17 3',b'18 3'),raw+b'* * * * * /home/jazofv1/hioc/pi4/bin/hioc-home-assistant-association.py\n',raw+raw):
   with self.assertRaises(M.Stop):M.validate_cron(value)
 def test_runtime_identity_drift_fails(self):
  with self.assertRaises(M.Stop):protected(FakeFS(),runtime_error=True)
 def test_directory_and_lock_security_remain_protected(self):
  fs=FakeFS();fs.modes[D.LOCK]=0o644
  with self.assertRaises((M.Stop,D.Failure)):protected(fs)
 def test_source_call_analysis_only_governed_writers(self):
  tree=ast.parse((ROOT/'pi4/lib/hioc/home_assistant_association.py').read_bytes())
  runtime=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='Runtime');text=ast.unparse(runtime)
  self.assertIn("StateStore(HOME / 'state/platform')",text);self.assertIn("update_status(self.store, self.registry, {'ha_core': observation}",text);self.assertNotIn('write_json(',text)
  fs=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='PosixFS');start=next(n for n in fs.body if isinstance(n,ast.FunctionDef) and n.name=='start');self.assertIn("'associations'",ast.unparse(start))
  self.assertFalse(R['source_write_scope_analysis']['additional_adapter_write_target_found'])
 def test_corrected_wrapper_real_authority_blocks_second_run(self):
  source=(ROOT/'tools/hioc-pe4-ha-association-manual-validate.py').read_text(encoding='utf8');gate=source.index("require(record['second_adapter_execution_authorized'] is True)");invoke=source.index('rc,raw=invoke_once(');self.assertLess(gate,invoke);self.assertFalse(R['second_adapter_execution_authorized'])
 def test_current_lifecycle_reconciliation_objective(self):
  text=(ROOT/'docs/HIOC_MASTER_PLAN.md').read_text(encoding='utf8');current=text.split('## Current Objective',1)[1].split('### Future Compatibility',1)[0];self.assertIn('**PE-4 Home Assistant Association Adapter Durable Post-Run Reconciliation**',current);self.assertIn('PI3 source synchronization to the evidence-authority correction commit',current)
  for name,state in [('Bounded Manual Production Validation','ATTEMPTED / REVIEW REQUIRED'),('Bounded Validation Scope Correction','PASS/CLOSED'),('Durable Post-Run Reconciliation','PREPARED FOR SEPARATE AUTHORIZATION')]:self.assertIn('| PE-4 Home Assistant Association Adapter '+name+' | '+state+' |',text)
 def test_source_sync_and_reconciliation_separate(self):
  self.assertEqual(R['operator_sequence'][:3],['SOURCE_SYNC_ONLY_THEN_STOP','INDEPENDENT_SOURCE_SYNC_REVIEW','SEPARATELY_AUTHORIZE_READ_ONLY_RECONCILIATION']);self.assertEqual(R['next_operator_action'],'PI3 SOURCE SYNCHRONIZATION TO CORRECTION COMMIT')
 def test_codex_negative_evidence_all_false(self):self.assertTrue(all(v is False for v in R['negative_evidence_by_codex'].values()))
if __name__=='__main__':unittest.main()
