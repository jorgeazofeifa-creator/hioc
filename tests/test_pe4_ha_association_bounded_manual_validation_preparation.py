"""Synthetic preparation checks only: no operator main, adapter cycle or live network."""
import ast
import contextlib
import io
import sys
from types import SimpleNamespace
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'governance/pe4/pe4-ha-association-bounded-manual-validation-preparation.json'
R=json.loads(P.read_bytes());S=json.loads(P.with_suffix('.schema.json').read_bytes())
def module(path,name):
 spec=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
M=module('tools/hioc-pe4-ha-association-manual-validate.py','synthetic_manual')
C=module('pi4/lib/hioc/core/compatibility.py','synthetic_compat')
A=module('pi4/lib/hioc/home_assistant_association.py','synthetic_validation')
DOC=(ROOT/'docs/PE4_HOME_ASSISTANT_ASSOCIATION_BOUNDED_MANUAL_VALIDATION_PREPARATION.md').read_text(encoding='utf8')
TEXT=(ROOT/'tools/hioc-pe4-ha-association-manual-validate.py').read_text(encoding='utf8')
TREE=ast.parse(TEXT)
def fields(**changes):
 r=dict(RESULT='PASS',ERROR_CODE='NONE',FAILURE_STAGE='NONE',COMPATIBILITY_STATUS='COMPATIBLE',OBSERVED_HA_VERSION='2026.8.1',ASSOCIATED_COUNT='1',REVIEW_ONLY_COUNT='0',REJECTED_COUNT='0',UNMATCHED_COUNT='0',HISTORICAL_BINDING_COUNT='0',STATE_PUBLISHED='TRUE',LAST_KNOWN_GOOD_PRESERVED='FALSE');r.update(changes);return r
def raw(r):return ('\n'.join(k+'='+r[k] for k in M.FIELDS)+'\n').encode()
def checks(**changes):
 r=dict(STATE_SCHEMA_VALIDATION='PASS',TRANSACTION_NAMESPACE_CLEAN='TRUE',CONFIG_UNCHANGED='TRUE',CANONICAL_INVENTORY_UNCHANGED='TRUE',PLATFORM_STATUS_UNCHANGED='TRUE',PLATFORM_CRON_UNCHANGED='TRUE',ASSOCIATION_SCHEDULER_PRESENT='FALSE',PROTECTED_PRODUCTION_SURFACES_UNCHANGED='TRUE',COMPATIBILITY_STATE_VALIDATION='PASS');r.update(changes);return r
class PreparationTests(unittest.TestCase):
 def reject(self,key,value):
  bad=copy.deepcopy(R);bad[key]=value
  with self.assertRaises(M.Stop):M.schema_validate(bad,S)
 def test_canonical_closed_record(self):
  M.schema_validate(R,S);self.assertEqual(P.read_bytes(),M.canonical(R));self.assertEqual(P.with_suffix('.schema.json').read_bytes(),M.canonical(S));self.assertEqual(R['status'],'PASS_CLOSED')
 def test_every_object_rejects_extra_properties(self):
  def walk(v,n):
   if isinstance(v,dict):
    bad=copy.deepcopy(v);bad['unexpected']=True
    with self.assertRaises(M.Stop):M.schema_validate(bad,n)
    for k,x in v.items():walk(x,n['properties'][k])
   elif isinstance(v,list):
    for x,child in zip(v,n['prefixItems']):walk(x,child)
  walk(R,S)
 def test_deployment_closure_exact_identity(self):
  for key in ('deployment_closure','deployment_closure_schema'):
   x=R[key];b=subprocess.check_output(['git','show',R['starting_commit']+':'+x['path']],cwd=ROOT)
   self.assertEqual(hashlib.sha256(b).hexdigest(),x['sha256']);self.assertEqual(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),x['git_blob'])
  self.reject('deployment_closure',{})
 def test_deployed_commit_and_frozen_sources_unchanged(self):
  self.assertEqual(R['deployed_source_commit'],'4912f20d8b2ff78dcdaf8b3e0f52e57d5de5e3a2');self.reject('deployed_source_commit','0'*40)
  for x in R['sources'].values():
   b=subprocess.check_output(['git','show',R['deployed_source_commit']+':'+x['path']],cwd=ROOT)
   self.assertEqual(b,(ROOT/x['path']).read_bytes().replace(b'\r\n',b'\n'));self.assertEqual(hashlib.sha256(b).hexdigest(),x['sha256'])
 def test_wrapper_and_compatibility_schema_identity(self):
  for name in ('source_only_wrapper','compatibility_status_schema'):
   x=R[name];b=subprocess.check_output(['git','show','abae01b6eb60aecb12396d8078dee719d75801b7:'+x['path']],cwd=ROOT);self.assertEqual(hashlib.sha256(b).hexdigest(),x['sha256'])
 def test_command_exact_no_application_arguments(self):
  self.assertEqual(R['adapter_command'],M.ADAPTER_COMMAND);self.assertEqual(R['adapter_arguments'],[]);self.assertEqual(M.ADAPTER_COMMAND[1:3],['-I','-B']);self.assertEqual(len(M.ADAPTER_COMMAND),4);self.reject('adapter_arguments',['--force'])
 def test_minimal_environment_and_proxy_override_boundary(self):
  self.assertEqual(R['environment'],M.ENV);self.assertEqual(set(M.ENV),{'PATH','HOME','LANG','LC_ALL'});self.assertEqual(len(R['rejected_environment_overrides_case_insensitive']),6);self.reject('environment',{'TOKEN':'secret'})
 def test_runtime_identity_frozen(self):
  x=R['runtime'];self.assertEqual((x['python'],x['architecture'],x['soabi'],x['websockets']),('3.11.2','aarch64','cpython-311-aarch64-linux-gnu','16.1.1'));self.assertFalse(x['mutation'])
 def test_exactly_one_call_no_retry(self):
  self.assertEqual(R['adapter_execution_count'],'EXACTLY_ONE');self.assertFalse(R['automatic_retry']);self.reject('automatic_retry',True)
  main=next(n for n in TREE.body if isinstance(n,ast.FunctionDef) and n.name=='main')
  calls=[n for n in ast.walk(main) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='invoke_once'];self.assertEqual(len(calls),1)
  invoke=next(n for n in TREE.body if isinstance(n,ast.FunctionDef) and n.name=='invoke_once')
  popens=[n for n in ast.walk(invoke) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='Popen'];self.assertEqual(len(popens),1)
 def test_no_scheduler_projection_ha_inventory_mutation(self):
  for k in ('scheduler_mutation','public_projection','ha_mutation','canonical_inventory_mutation'):self.assertFalse(R[k]);self.reject(k,True)
  self.assertNotIn('deploy(',TEXT);self.assertNotIn('writer.recovery(',TEXT);self.assertNotIn('runtime.credential(',TEXT)
 def test_exact_four_registry_commands_from_deployed_source(self):
  self.assertEqual(R['network']['commands'],list(A.COMMANDS));self.assertEqual(len(A.COMMANDS),4);self.reject('network',{})
 def test_network_limits_and_no_auxiliary_probes(self):
  n=R['network'];self.assertEqual((n['shared_deadline_seconds'],n['send_receive_cap_seconds'],n['adapter_alarm_seconds']),(90,15,180))
  for k in ('dns','proxy','redirect','retry','auxiliary_probes'):self.assertFalse(n[k])
 def test_exact_result_fields_from_deployed_source(self):
  self.assertEqual(R['result_fields'],list(A.RESULT_FIELDS));self.assertEqual(tuple(R['result_fields']),M.FIELDS);self.assertEqual(len(M.FIELDS),12)
 def test_pre_run_absence_and_lock_security(self):
  self.assertEqual(R['pre_run_private_state'],'ABSENT_REQUIRED');self.assertEqual(R['pre_run_absent'],['home_assistant.json','.home_assistant.txn-*','.home_assistant.done-*']);self.assertIn('0600',R['lock_security']);self.assertIn('SINGLE_LINK',R['lock_security']);self.reject('pre_run_private_state','PRESENT')
 def test_committed_and_exact_five_nine_manifests(self):
  c=json.loads((ROOT/M.CLOSURE).read_bytes());self.assertEqual(R['deployment_transaction_required'],'COMMITTED');self.assertEqual(R['five_required_dependencies'],c['dependencies']);self.assertEqual(R['nine_deployed_targets'],c['deployed_targets']);self.assertEqual((len(R['five_required_dependencies']),len(R['nine_deployed_targets'])),(5,9))
 def test_platform_and_cron_preservation(self):
  p=R['preservation'];self.assertEqual(p['platform_sha256'],'b65464e722bf9a4da0004ecf3bb05e4105f345a87c62405ce92d97c6298b2af8');self.assertTrue(p['platform_cron'].startswith('17 3 * * * flock -n'));self.assertFalse(p['platform_execution'])
 def test_config_inventory_boolean_comparisons(self):
  self.assertIn('TRANSIENT_BYTES_COMPARE_REPORT_BOOLEAN_ONLY',R['preservation']['config']);self.assertIn('CONFIG_UNCHANGED',R['evidence_report_fields']);self.assertIn('CANONICAL_INVENTORY_UNCHANGED',R['evidence_report_fields']);self.assertIn('RAM_ONLY_NO_HASHES',R['evidence']['private_comparisons'])
 def test_credential_no_reader_or_exposure(self):
  self.assertTrue(R['credential_policy']['adapter_governed_path_only']);self.assertTrue(all(v is False for k,v in R['credential_policy'].items() if k!='adapter_governed_path_only'))
  self.assertNotIn('read_credential(',TEXT);self.assertNotIn('credential-validate.py',TEXT);self.assertNotIn('.prerequisites(',TEXT)
 def test_private_evidence_allowlist(self):
  self.assertEqual(set(R['evidence_report_fields']),set(M.FIELDS+tuple('PRODUCTION_FILES_UNCHANGED' if k=='PROTECTED_PRODUCTION_SURFACES_UNCHANGED' else k for k in M.EXTRA)));self.assertEqual(R['evidence']['files'],['result.txt','validation.json','report.txt']);self.assertEqual(R['evidence']['directory_mode'],'0700');self.assertEqual(R['evidence']['file_mode'],'0600')
 def test_pass_exact_good_states_and_lkg(self):
  self.assertEqual(set(R['pass']['good_compatibility_states']),C.GOOD);self.assertEqual(M.classify(fields(),0,checks()),'PASS')
  for change in ({'STATE_PUBLISHED':'FALSE'},{'LAST_KNOWN_GOOD_PRESERVED':'TRUE'},{'ERROR_CODE':'TRANSACTION_CLEANUP_FAILED'},{'FAILURE_STAGE':'COMPATIBILITY'}):
   with self.assertRaises(M.Stop):M.classify(fields(**change),0,checks())
 def test_warning_codes_only_and_no_final_acceptance(self):
  self.assertEqual(R['pass_with_warning']['codes'],list(M.WARNINGS));self.assertFalse(R['pass_with_warning']['final_acceptance'])
  for code in M.WARNINGS:self.assertEqual(M.classify(fields(RESULT='PASS_WITH_WARNING',ERROR_CODE=code),0,checks()),'MANUAL_REVIEW_REQUIRED')
  with self.assertRaises(M.Stop):M.classify(fields(RESULT='PASS_WITH_WARNING',ERROR_CODE='NONE'),0,checks())
 def test_fail_nonzero_no_rerun(self):
  f=fields(RESULT='FAIL',ERROR_CODE='HA_AUTHENTICATION_FAILED',FAILURE_STAGE='HA_AUTHENTICATION',STATE_PUBLISHED='FALSE',LAST_KNOWN_GOOD_PRESERVED='TRUE')
  self.assertEqual(M.classify(f,1,checks()),'FAIL')
  with self.assertRaises(M.Stop):M.classify(f,0,checks())
  self.assertFalse(R['fail']['automatic_retry'])
 def test_zero_and_review_counts_are_not_invented_failures(self):
  self.assertEqual(M.classify(fields(ASSOCIATED_COUNT='0'),0,checks()),'MANUAL_REVIEW_REQUIRED')
  self.assertEqual(M.classify(fields(REVIEW_ONLY_COUNT='8',REJECTED_COUNT='3'),0,checks()),'PASS');self.assertFalse(R['counts']['arbitrary_thresholds'])
 def test_first_run_history_zero_structural_authority(self):
  self.assertEqual(R['counts']['historical_bindings_first_run'],0)
  with self.assertRaises(M.Stop):M.classify(fields(HISTORICAL_BINDING_COUNT='1'),0,checks())
 def test_all_failure_stages_documented(self):
  self.assertEqual(set(R['failure_stage_handling']),A.STAGES);self.assertEqual(set(M.STAGES),A.STAGES)
  for stage in A.STAGES:self.assertIn('| '+stage+' |',DOC)
 def test_lkg_derived_from_immutable_source(self):
  self.assertEqual(R['last_known_good']['successful_first_publication'],'FALSE');self.assertEqual(R['last_known_good']['before_prior_validation'],'UNKNOWN');self.assertIn('TRUE_IF_RESTORED',R['last_known_good']['publication_stage_failure']);self.assertIn('preserved = "FALSE"',(ROOT/'pi4/lib/hioc/home_assistant_association.py').read_text(encoding='utf8'))
 def test_separate_sync_and_execution_review_only_block(self):
  self.assertEqual(R['next_action_after_preparation'],'PI3 SOURCE SYNCHRONIZATION TO PREPARATION COMMIT');self.assertIn('INDEPENDENTLY_REVIEW_SOURCE_SYNC',R['operator_sequence']);self.assertIn('FOR REVIEW ONLY - DO NOT RUN WITHOUT SEPARATE AUTHORIZATION',DOC)
  block=DOC.split('## Complete future execution block',1)[1].split('```sh',1)[1].split('```',1)[0]
  for forbidden in ('git pull','git fetch','set -','pipefail','set -x','exit','exec ','logout'):self.assertNotIn(forbidden,block)
  self.assertIn('--approved-preparation-commit',block);self.assertIn('return_code=$?',block)
 def test_current_master_lifecycle_and_next_action(self):
  text=(ROOT/'docs/HIOC_MASTER_PLAN.md').read_text(encoding='utf8');current=text.split('## Current Objective',1)[1].split('### Future Compatibility',1)[0]
  self.assertIn('Post-Run Reconciliation',current);self.assertIn('PI3 source synchronization to the durable reconciliation closure commit',current)
  table=text.split('## Authoritative Current PE-4 Lifecycle',1)[1].split('### Completed',1)[0]
  self.assertIn('| PE-4 Home Assistant Association Adapter Bounded Manual Production Validation | PASS/CLOSED |',table)
  for name,state in (('Independent Production Acceptance','PASS/CLOSED'),('Scheduler Deployment','PASS/CLOSED')):self.assertIn('| PE-4 Home Assistant Association Adapter '+name+' | '+state+' |',table)
 def test_valid_parser_retains_exact_sanitized_result(self):
  f=fields();self.assertEqual(M.parse_result(raw(f),C),f)
 def test_parser_rejects_raw_extra_duplicate_reordered_output(self):
  good=raw(fields())
  for bad in (good+b'token=secret\n',good.replace(b'RESULT=PASS',b'RESULT=PASS\nRESULT=PASS'),b'raw registry contents',b'\n'.join(reversed(good.splitlines()))+b'\n',good[:-1]):
   with self.assertRaises((M.Stop,UnicodeError)):M.parse_result(bad,C)
 def test_parser_rejects_private_or_unbounded_values(self):
  for k,v in (('OBSERVED_HA_VERSION','192.168.1.1'),('OBSERVED_HA_VERSION','household.local'),('ASSOCIATED_COUNT','65537'),('HISTORICAL_BINDING_COUNT','4097'),('STATE_PUBLISHED','secret'),('FAILURE_STAGE','UNKNOWN_STAGE')):
   with self.assertRaises(M.Stop):M.parse_result(raw(fields(**{k:v})),C)
 def test_nonfinite_and_duplicate_json_rejected(self):
  for raw_value in (b'{"a":1,"a":2}',b'{"a":NaN}',b'{"a":Infinity}'):
   with self.assertRaises(M.Stop):M.strict(raw_value)
 def test_invariant_failure_never_passes(self):
  for key in checks():
   with self.assertRaises(M.Stop):M.classify(fields(),0,checks(**{key:'UNKNOWN'}))
  with self.assertRaises(M.Stop):M.classify(fields(),0,checks(CONFIG_UNCHANGED='FALSE'))
 def test_sanitized_evidence_files_exact_and_private_safe(self):
  report={k:'UNKNOWN' for k in M.FIELDS+M.EXTRA};report.update(fields());report.update(OVERALL_VALIDATION='PASS',TARGET='PI3 NUT&PIHOLE',DEPLOYED_SOURCE_COMMIT=M.DEPLOYED,ADAPTER_EXECUTION_COUNT='1',WRAPPER_STATUS='COMPLETE',MANUAL_REVIEW_REQUIRED='FALSE',CREDENTIAL_EXPOSED='FALSE',RAW_HA_DATA_PERSISTED='FALSE',PRIVATE_ASSOCIATION_CONTENT_EXPOSED='FALSE')
  with tempfile.TemporaryDirectory() as tmp, patch.object(M.os,'O_NOFOLLOW',getattr(M.os,'O_NOFOLLOW',0),create=True):
   M.write_evidence(Path(tmp),report,raw(fields()));self.assertEqual(set(p.name for p in Path(tmp).iterdir()),{'result.txt','validation.json','report.txt'});self.assertEqual(json.loads((Path(tmp)/'validation.json').read_bytes()),report)
  report['HOUSEHOLD']= 'private'
  with tempfile.TemporaryDirectory() as tmp:
   with self.assertRaises(M.Stop):M.write_evidence(Path(tmp),report)
 def test_compatibility_framework_semantics_preserve_unrelated_history(self):
  registry=json.loads((ROOT/'governance/compatibility-contracts.json').read_bytes());schema=json.loads((ROOT/'governance/compatibility-status.schema.json').read_bytes())
  class Store:
   def __init__(self,p):self.p=p
   def read_json(self,*a):return self.p
   def write_json(self,n,p,mode):self.p=p
  store=Store({});C._update_status(store,registry,{},'2026-10-06T10:00:00Z');before=copy.deepcopy(store.p)
  observation={'observed_version':'2026.8.1','capabilities':{k:True for k in A.CAPABILITIES}}
  C._update_status(store,registry,{'ha_core':observation},'2026-10-08T10:00:00Z');after=copy.deepcopy(store.p)
  ha=next(x for x in after['dependencies'] if x['dependency_id']=='ha_core');f=fields(COMPATIBILITY_STATUS=ha['status'])
  self.assertEqual(M.compatibility_validation(before,after,f,C,schema,registry),'PASS')
  bad=copy.deepcopy(after);next(x for x in bad['dependencies'] if x['dependency_id']=='ha_core')['observed_version']='2026.8.2'
  with self.assertRaises(M.Stop):M.compatibility_validation(before,bad,f,C,schema,registry)
 def test_unchanged_compatibility_failure_requires_review(self):
  registry=json.loads((ROOT/'governance/compatibility-contracts.json').read_bytes());schema=json.loads((ROOT/'governance/compatibility-status.schema.json').read_bytes())
  payload=C.summarize([C.assess(x,{}, {},'2026-10-06T10:00:00Z') for x in registry['dependencies']],'2026-10-06T10:00:00Z')
  self.assertEqual(M.compatibility_validation(payload,payload,fields(RESULT='FAIL'),C,schema,registry),'NOT_UPDATED_REVIEW_REQUIRED')
  with self.assertRaises(M.Stop):M.compatibility_validation(payload,payload,fields(),C,schema,registry)
 def test_precondition_names_include_all_gate_boundaries(self):
  self.assertGreaterEqual(len(R['pre_execution_stops']),13);self.assertIn('DEPLOYMENT_NOT_COMMITTED',R['pre_execution_stops']);self.assertIn('PRIVATE_STATE_OR_TRANSACTION_NAMESPACE_PRESENT',R['pre_execution_stops']);self.assertIn('MALFORMED_OUTPUT',R['post_execution_stops'])
 def test_post_checks_independent_and_output_error_not_persisted(self):
  self.assertIn("except BaseException:report['OUTPUT_VALIDATION']='FAIL'",TEXT);self.assertIn("check('CONFIG_UNCHANGED'",TEXT);self.assertIn("raw if parsed is not None else None",TEXT);self.assertIn('stderr=subprocess.DEVNULL',TEXT)
 def test_namespace_stops_before_first_run_and_never_deletes(self):
  class FS:
   def check_directory(self,*a):return True
   def read(self,*a):return b''
   def names(self,*a):return ['.home_assistant.lock','home_assistant.json']
  d=type('D',(),{'ASSOCIATIONS':'x','LOCK':'y'})
  with self.assertRaises(M.Stop):M.namespace(FS(),d,True)
  self.assertEqual(M.namespace(FS(),d),(True,True));self.assertNotIn('os.unlink',TEXT);self.assertNotIn('os.replace',TEXT)
 def test_wrapper_definition_import_safe(self):
  for n in TREE.body:
   if isinstance(n,ast.Expr):self.assertIsInstance(n.value,ast.Constant)
  self.assertEqual(R['manual_adapter_execution'],'NOT_PERFORMED');self.assertFalse(R['codex_pi3_access']);self.assertFalse(R['codex_ha_access']);self.assertFalse(R['codex_credential_access'])
class SyntheticWrapperFlowTests(unittest.TestCase):
 def run_flow(self,mode='pass'):
  # Every target/filesystem/child boundary is fake; operator main never sees production.
  c=json.loads((ROOT/M.CLOSURE).read_bytes());schema=json.loads((ROOT/A.SCHEMA_PATH).read_bytes())
  registry=json.loads((ROOT/'governance/compatibility-contracts.json').read_bytes())
  state={'schema_version':'1.1','updated_at':'2026-10-06T14:00:00Z','instance_reference':'PI5_HA','observed_ha_version':'2026.8.1','contract_version':'1.0','associations':[{'hioc_device_id':'dev_'+('a'*16),'ha_device_id':'synthetic-device','association_basis':'unique_mac','status':'ASSOCIATED_STRONG_MAC','first_associated_at':'2026-10-06T14:00:00Z','last_confirmed_at':'2026-10-06T14:00:00Z','observed_ha_version':'2026.8.1','contract_version':'1.0','relationship_status':'COMPLETE'}],'binding_history':[],'diagnostics':[],'summary':{'associated_devices':1,'entity_memberships':0,'review_only':0,'rejected':0,'unmatched':0,'historical_bindings':0}}
  A.validate_state(state,schema)
  prior=C.summarize([C.assess(x,{}, {},'2026-10-06T10:00:00Z') for x in registry['dependencies']],'2026-10-06T10:00:00Z')
  invoked=[];saved=[]
  class FS:
   def read(self,path,*args):
    if path==A.STATE:return A.encoded(state)
    if path==A.SCHEMA_PATH:return A.encoded(schema)
    if path=='governance/compatibility-contracts.json':return A.encoded(registry)
    if path=='state/platform/compatibility.json':return A.encoded(prior)
    if path=='pi4/bin/hioc-platform-status.py':return b'platform'
    return b'unchanged'
  d=SimpleNamespace(NativeFS=lambda *a:FS(),CONFIG='config/hioc.conf')
  def load(path,name):return d if 'deploy.py' in str(path) else A if 'association.py' in str(path) else C
  def invoke(on_started):
   on_started();invoked.append(1)
   if mode=='malformed':return 0,b'private raw output must not persist'
   if mode=='warning':return 0,raw(fields(RESULT='PASS_WITH_WARNING',ERROR_CODE='TRANSACTION_CLEANUP_FAILED'))
   if mode=='fail':return 1,raw(fields(RESULT='FAIL',ERROR_CODE='HA_CONNECTION_FAILED',FAILURE_STAGE='HA_CONNECTION',STATE_PUBLISHED='FALSE',LAST_KNOWN_GOOD_PRESERVED='TRUE'))
   return 0,raw(fields())
  def names(*args):return (False,True) if not invoked or mode=='fail' else (True,mode!='warning')
  def capture(directory,report,result):saved.append((copy.deepcopy(report),result))
  with tempfile.TemporaryDirectory() as tmp,contextlib.ExitStack() as stack:
   stack.enter_context(patch.dict(sys.modules,{'pwd':SimpleNamespace(getpwnam=lambda n:SimpleNamespace(pw_uid=1000)),'grp':SimpleNamespace(getgrnam=lambda n:SimpleNamespace(gr_gid=1000))}))
   stack.enter_context(patch.object(M.sys,'platform','linux'))
   stack.enter_context(patch.object(M,'SOURCE',ROOT))
   stack.enter_context(patch.object(M.os,'environ',M.ENV))
   for name in ('getuid','geteuid','getgid','getegid'):stack.enter_context(patch.object(M.os,name,lambda:1000,create=True))
   stack.enter_context(patch.object(M.socket,'gethostname',lambda:'nutandpihole'))
   stack.enter_context(patch.object(M,'command',return_value=b'inet 192.168.100.252/24'))
   stack.enter_context(patch.object(M,'source_binding',side_effect=M.Stop if mode=='precondition' else lambda x:(c,{'second_adapter_execution_authorized':True})))
   stack.enter_context(patch.object(M,'load_module',side_effect=load))
   stack.enter_context(patch.object(M,'deployment_integrity'))
   stack.enter_context(patch.object(M,'runtime_probe'))
   stack.enter_context(patch.object(M,'namespace',side_effect=names))
   stack.enter_context(patch.object(M,'scheduler',return_value=b'synthetic cron'))
   stack.enter_context(patch.object(M,'protected_snapshot',return_value={'synthetic':'RAM_ONLY'}))
   stack.enter_context(patch.object(M,'evidence_directory',return_value=Path(tmp)))
   stack.enter_context(patch.object(M,'invoke_once',side_effect=invoke))
   stack.enter_context(patch.object(M,'compatibility_validation',return_value='PASS'))
   stack.enter_context(patch.object(M,'sha',return_value=c['platform_status_sha256']))
   stack.enter_context(patch.object(M,'write_evidence',side_effect=capture))
   (Path(tmp)/'report.txt').write_text('SYNTHETIC_ONLY',encoding='ascii')
   with contextlib.redirect_stdout(io.StringIO()):rc=M.main(['--approved-preparation-commit','a'*40])
  return rc,invoked,saved[0]
 def test_precondition_failure_invokes_zero_children(self):
  rc,calls,(report,result)=self.run_flow('precondition');self.assertEqual(calls,[]);self.assertEqual(report['ADAPTER_EXECUTION_COUNT'],'0');self.assertEqual(rc,1);self.assertIsNone(result)
 def test_success_invokes_once_and_retains_only_sanitized_result(self):
  rc,calls,(report,result)=self.run_flow();self.assertEqual(len(calls),1);self.assertEqual(rc,0);self.assertEqual(report['OVERALL_VALIDATION'],'PASS');M.validate_report(report);self.assertEqual(result,raw(fields()))
 def test_warning_invokes_once_then_stops_for_review(self):
  rc,calls,(report,result)=self.run_flow('warning');self.assertEqual(len(calls),1);self.assertEqual(rc,1);self.assertEqual(report['OVERALL_VALIDATION'],'MANUAL_REVIEW_REQUIRED');self.assertEqual(report['TRANSACTION_NAMESPACE_CLEAN'],'FALSE')
 def test_fail_invokes_once_and_preserves_exact_lkg_report(self):
  rc,calls,(report,result)=self.run_flow('fail');self.assertEqual(len(calls),1);self.assertEqual(rc,1);self.assertEqual(report['RESULT'],'FAIL');self.assertEqual(report['LAST_KNOWN_GOOD_PRESERVED'],'TRUE')
 def test_malformed_output_discarded_and_independent_checks_still_run(self):
  rc,calls,(report,result)=self.run_flow('malformed');self.assertEqual(len(calls),1);self.assertEqual(rc,1);self.assertIsNone(result);self.assertEqual(report['OUTPUT_VALIDATION'],'FAIL');self.assertEqual(report['CONFIG_UNCHANGED'],'TRUE');self.assertEqual(report['CANONICAL_INVENTORY_UNCHANGED'],'TRUE');self.assertNotIn('private raw',str(report))

if __name__=='__main__':unittest.main()
