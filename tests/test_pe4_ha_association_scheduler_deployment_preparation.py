"""Synthetic scheduler fixtures only. Never read or install a real crontab."""
import copy,hashlib,importlib.util,json,subprocess,sys,types,unittest
from pathlib import Path
from unittest.mock import patch
from test_pe4_ha_association_deployment_closure import validate,canonical
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'governance/pe4/pe4-ha-association-scheduler-deployment-preparation.json'
R=json.loads(P.read_bytes());S=json.loads(P.with_suffix('.schema.json').read_bytes())
spec=importlib.util.spec_from_file_location('prepared_scheduler_test',ROOT/'tools/hioc-pe4-ha-association-scheduler-deploy.py');M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
COMMIT='a'*40
PRIOR=b'# unrelated comment  \nMAILTO=""\n\n'+M.PLATFORM+b'\n0,30 * * * * /synthetic/inventory\n'
class Ops:
 def __init__(self,raw=PRIOR):self.raw=raw;self.installs=[];self.reads=0;self.rc=0;self.after=None;self.fail_install=False;self.fail_read_after=False;self.drift_at=None
 def read(self):
  self.reads+=1
  if self.fail_read_after and self.installs:raise OSError('private synthetic diagnostic')
  if self.drift_at==self.reads:return self.raw+b'# concurrent change\n'
  return self.raw
 def install(self,candidate):
  self.installs.append(candidate);self.raw=candidate if self.after is None else self.after
  if self.fail_install:raise TimeoutError('private synthetic diagnostic')
  return self.rc
class SchedulerPreparationTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.blobs={i['path']:subprocess.check_output(['git','show',M.BASE+':'+i['path']],cwd=ROOT) for i in R['sources']}
 def deploy(self,ops=None,guard=None):return M.deploy(COMMIT,ops or Ops(),guard or (lambda c:'stable'))
 def test_exact_cadence_runtime_flags_entrypoint_marker(self):
  self.assertEqual(M.MARKER,b'# HIOC_PE4_HA_ASSOCIATION');self.assertEqual(M.LINE,b'5,35 * * * * /home/jazofv1/hioc/runtime/pe4/active/bin/python -I -B /home/jazofv1/hioc/pi4/bin/hioc-home-assistant-association.py >/dev/null 2>&1');self.assertEqual(M.BLOCK,M.MARKER+b'\n'+M.LINE+b'\n')
 def test_frozen_architecture_exact_existing_authority(self):
  old=json.loads((ROOT/'governance/pe4/pe4-ha-association-adapter-implementation-preparation.json').read_bytes());self.assertEqual(R['frozen_scheduler'],old['scheduler']);self.assertFalse(R['canonical_cron']['external_overlap_lock'])
 def test_successful_actual_deployment_function(self):
  ops=Ops();report=self.deploy(ops);self.assertEqual(report['RESULT'],'PASS');self.assertEqual(report['MUTATION_STATE'],'VERIFIED_INSTALLED');self.assertEqual(ops.installs,[M.candidate_crontab(PRIOR)]);self.assertEqual(report['INSTALL_ATTEMPTS'],1)
 def test_platform_exact_preservation(self):
  candidate=M.candidate_crontab(PRIOR);self.assertEqual([x for x in candidate.split(b'\n') if b'hioc-platform-status' in x],[M.PLATFORM]);self.assertTrue(M.verify_candidate(PRIOR,candidate))
 def test_unrelated_prefix_preservation_and_no_normalization(self):
  prior=b'  # whitespace\n\nX="a b"\n'+M.PLATFORM+b'\n\n';self.assertEqual(M.candidate_crontab(prior),prior+M.BLOCK)
 def test_missing_final_lf_controlled_separator_only(self):
  prior=M.PLATFORM;self.assertEqual(M.candidate_crontab(prior),prior+b'\n'+M.BLOCK)
 def test_candidate_generation_deterministic(self):self.assertEqual(M.candidate_crontab(PRIOR),M.candidate_crontab(PRIOR))
 def reject_prior(self,raw):
  ops=Ops(raw);report=self.deploy(ops);self.assertEqual(report['RESULT'],'FAIL');self.assertEqual(report['INSTALL_ATTEMPTS'],0);self.assertEqual(ops.installs,[])
 def test_empty_crontab_rejected_no_platform_adoption(self):self.reject_prior(b'')
 def test_missing_platform_rejected(self):self.reject_prior(b'# only comments\n')
 def test_duplicate_platform_rejected(self):self.reject_prior(PRIOR+M.PLATFORM+b'\n')
 def test_changed_platform_rejected(self):self.reject_prior(PRIOR.replace(b'17 3',b'18 3'))
 def test_existing_association_canonical_rejected(self):self.reject_prior(PRIOR+M.BLOCK)
 def test_duplicate_association_rejected(self):self.reject_prior(PRIOR+M.BLOCK+M.BLOCK)
 def test_malformed_association_rejected(self):self.reject_prior(PRIOR+b'* invalid hioc-home-assistant-association.py\n')
 def test_unexpected_identity_marker_rejected(self):self.reject_prior(PRIOR+b'# HIOC_PE4_HA_ASSOCIATION altered\n')
 def test_unexpected_association_variant_rejected(self):self.reject_prior(PRIOR+b'0 * * * * /other/hioc-ha-association\n')
 def test_invalid_utf8_rejected(self):self.reject_prior(PRIOR+b'\xff\n')
 def test_crlf_rejected_without_normalizing(self):self.reject_prior(PRIOR.replace(b'\n',b'\r\n'))
 def test_nul_rejected(self):self.reject_prior(PRIOR+b'\0')
 def test_oversized_crontab_rejected(self):self.reject_prior(b' '*65537)
 def test_candidate_overflow_rejected(self):self.reject_prior(PRIOR+b'#'+b'x'*(M.LIMIT-len(PRIOR)-2)+b'\n')
 def test_pre_mutation_crontab_drift(self):
  ops=Ops();ops.drift_at=2;report=self.deploy(ops);self.assertEqual(report['ERROR_CODE'],'PRE_MUTATION_DRIFT');self.assertEqual(ops.installs,[])
 def test_pre_mutation_guard_drift(self):
  ops=Ops();calls=[]
  def guard(c):calls.append(1);return len(calls)
  report=self.deploy(ops,guard);self.assertEqual(report['RESULT'],'FAIL');self.assertEqual(ops.installs,[])
 def test_nonzero_install_even_candidate_observed_is_fail(self):
  ops=Ops();ops.rc=1;report=self.deploy(ops);self.assertEqual(report['RESULT'],'FAIL');self.assertEqual(report['MUTATION_STATE'],'CANDIDATE_OBSERVED');self.assertTrue(report['MANUAL_REVIEW_REQUIRED']);self.assertEqual(len(ops.installs),1)
 def test_nonzero_install_prior_observed_no_preservation_claim(self):
  ops=Ops();ops.rc=1;ops.after=PRIOR;report=self.deploy(ops);self.assertEqual(report['MUTATION_STATE'],'PRIOR_OBSERVED');self.assertTrue(report['MANUAL_REVIEW_REQUIRED']);self.assertEqual(report['RESULT'],'FAIL')
 def test_ambiguous_install_none_return(self):
  ops=Ops();ops.rc=None;report=self.deploy(ops);self.assertEqual(report['RESULT'],'FAIL');self.assertTrue(report['MANUAL_REVIEW_REQUIRED']);self.assertEqual(len(ops.installs),1)
 def test_install_exception_candidate_may_be_installed(self):
  ops=Ops();ops.fail_install=True;report=self.deploy(ops);self.assertEqual(report['RESULT'],'FAIL');self.assertEqual(report['MUTATION_STATE'],'CANDIDATE_OBSERVED');self.assertEqual(len(ops.installs),1)
 def test_post_reread_failure_unknown(self):
  ops=Ops();ops.fail_read_after=True;report=self.deploy(ops);self.assertEqual(report['MUTATION_STATE'],'UNKNOWN');self.assertTrue(report['MANUAL_REVIEW_REQUIRED']);self.assertEqual(len(ops.installs),1)
 def test_post_candidate_mismatch(self):
  ops=Ops();ops.after=PRIOR+b'# changed\n';report=self.deploy(ops);self.assertEqual(report['ERROR_CODE'],'POST_INSTALL_MISMATCH');self.assertEqual(report['MUTATION_STATE'],'OTHER_OBSERVED');self.assertEqual(report['RESULT'],'FAIL')
 def test_post_duplicate_association_detection(self):
  ops=Ops();ops.after=M.candidate_crontab(PRIOR)+M.BLOCK;self.assertEqual(self.deploy(ops)['RESULT'],'FAIL')
 def test_post_platform_mutation_detection(self):
  ops=Ops();ops.after=M.candidate_crontab(PRIOR).replace(b'17 3',b'18 3');self.assertEqual(self.deploy(ops)['RESULT'],'FAIL')
 def test_post_guard_drift_manual_review(self):
  ops=Ops();calls=[]
  def guard(c):calls.append(1);return 'stable' if len(calls)<3 else 'drift'
  report=self.deploy(ops,guard);self.assertEqual(report['RESULT'],'FAIL');self.assertTrue(report['MANUAL_REVIEW_REQUIRED']);self.assertEqual(len(ops.installs),1)
 def test_final_read_drift(self):
  ops=Ops();ops.drift_at=4;self.assertEqual(self.deploy(ops)['RESULT'],'FAIL');self.assertEqual(len(ops.installs),1)
 def test_no_auto_retry_rollback_or_execution_flags(self):
  ops=Ops();ops.fail_install=True;report=self.deploy(ops)
  for key in ['ADAPTER_EXECUTED','CREDENTIAL_ACCESSED','HA_NETWORK_ATTEMPTED','ASSOCIATION_STATE_MUTATED','PUBLIC_PROJECTION_EXECUTED','AUTOMATIC_RETRY','ROLLBACK_PERFORMED']:self.assertIs(report[key],False)
  self.assertEqual(len(ops.installs),1)
 def test_private_exception_not_exposed(self):
  ops=Ops();ops.fail_install=True;raw=M.canonical(self.deploy(ops));self.assertNotIn(b'private synthetic',raw);self.assertNotIn(PRIOR,raw)
  import io
  captured=io.StringIO()
  with patch.object(M.sys,'stderr',captured):
   with self.assertRaises((M.Failure,M.argparse.ArgumentError)):M.Parser(add_help=False,exit_on_error=False).parse_args(['--synthetic-private'])
  self.assertEqual(captured.getvalue(),'')
 def test_systemd_association_scheduler_rejected(self):
  with self.assertRaises(M.Failure):M.check_surfaces([('/etc/systemd/system/x.service',b'ExecStart=/home/jazofv1/hioc/pi4/bin/hioc-home-assistant-association.py')])
 def test_system_scheduler_marker_rejected(self):
  with self.assertRaises(M.Failure):M.check_surfaces([('/etc/cron.d/x',b'# HIOC_PE4_HA_ASSOCIATION')])
 def test_unrelated_scheduler_surfaces_stable(self):
  entries=[('/etc/cron.d/other',b'0 0 * * * root /synthetic\n'),('/etc/systemd/system/other.service',b'ExecStart=/bin/true')];self.assertEqual(M.check_surfaces(entries),M.check_surfaces(list(reversed(entries))))
 def test_scheduler_surface_size_and_count_bounded(self):
  for entries in [[('/etc/cron.d/x',b'x'*65537)],[(str(x),b'') for x in range(4097)]]:
   with self.assertRaises(M.Failure):M.check_surfaces(entries)
 def test_native_crontab_read_command_fixed(self):
  with patch.object(M,'read_command',return_value=PRIOR) as call:self.assertEqual(M.NativeOps().read(),PRIOR);call.assert_called_once_with(['/usr/bin/crontab','-l'])
 def test_native_install_only_crontab_stdin_no_adapter(self):
  candidate=M.candidate_crontab(PRIOR)
  with patch.object(M.subprocess,'run',return_value=types.SimpleNamespace(returncode=0)) as call:
   self.assertEqual(M.NativeOps().install(candidate),0);args,kwargs=call.call_args;self.assertEqual(args[0],['/usr/bin/crontab','-']);self.assertEqual(kwargs['input'],candidate);self.assertEqual(kwargs['stdout'],subprocess.DEVNULL);self.assertEqual(kwargs['stderr'],subprocess.DEVNULL);self.assertNotIn('shell',kwargs);self.assertEqual(kwargs['env'],M.ENV)
 def process(self,raw,rc=0,stderr=False):
  code='import sys;sys.stdout.buffer.write('+repr(raw)+');'+('sys.stderr.write("synthetic stderr");' if stderr else '')+'raise SystemExit('+str(rc)+')';return [sys.executable,'-I','-B','-c',code]
 def test_actual_local_binary_reader_and_discarded_stderr(self):self.assertEqual(M.read_command(self.process(PRIOR,stderr=True)),PRIOR)
 def test_actual_local_reader_oversize(self):
  with self.assertRaises(Exception):M.read_command(self.process(b'x'*65537))
 def test_actual_local_reader_process_failure(self):
  with self.assertRaises(Exception):M.read_command(self.process(PRIOR,1))
 def test_actual_local_reader_timeout(self):
  with patch.object(M,'TIMEOUT',.1):
   with self.assertRaises(Exception):M.read_command([sys.executable,'-I','-B','-c','import time;time.sleep(1)'])
 def target(self,**changes):
  values=dict(host='nutandpihole',user='jazofv1',uid=1000,euid=1000,gid=1000,egid=1000);values.update(changes);return M.target_gate(**values)
 def test_target_exact(self):self.target()
 def test_wrong_host_rejected(self):
  with self.assertRaises(M.Failure):self.target(host='other')
 def test_wrong_user_rejected(self):
  with self.assertRaises(M.Failure):self.target(user='root')
 def test_wrong_effective_identity_rejected(self):
  for changes in [dict(uid=0,euid=0),dict(euid=1001),dict(egid=1001)]:
   with self.assertRaises(M.Failure):self.target(**changes)
 def fake_git(self,override=None):
  override=override or {}
  def run(args,**kwargs):
   a=tuple(args[3:]);require=a in override
   if require:out=override[a]
   elif a in [('rev-parse','HEAD'),('rev-parse','origin/main')]:out=(COMMIT+'\n').encode()
   elif a==('branch','--show-current'):out=b'main\n'
   elif a==('rev-parse','HEAD^'):out=(M.BASE+'\n').encode()
   elif a==('show','-s','--format=%s','HEAD'):out=(M.SUBJECT+'\n').encode()
   elif a[0]=='status':out=b''
   elif a[:2]==('rev-parse','--git-path'):out=('nonexistent-scheduler-test-marker-'+a[2]).encode()
   elif a[0]=='rev-parse':
    path=a[1].split(':',1)[1];out=next(i['git_blob'] for i in R['sources'] if i['path']==path).encode()
   elif a[0]=='show':
    commit,path=a[1].split(':',1);out=self.blobs[path] if commit==M.BASE else (ROOT/path).read_bytes().replace(b'\r\n',b'\n')
   else:raise AssertionError(a)
   return types.SimpleNamespace(returncode=0,stdout=out)
  return run
 def gate(self,override=None):return M.source_gate(COMMIT,root=ROOT,run=self.fake_git(override))
 def test_actual_source_gate_exact_contract(self):self.assertEqual(self.gate()['starting_commit'],M.BASE)
 def test_source_commit_drift(self):
  with self.assertRaises(Exception):self.gate({('rev-parse','HEAD'):b'b'*40})
 def test_dirty_repository(self):
  with self.assertRaises(Exception):self.gate({('status','--porcelain'):b' M synthetic'})
 def test_wrong_branch(self):
  with self.assertRaises(Exception):self.gate({('branch','--show-current'):b'other'})
 def test_origin_divergence(self):
  with self.assertRaises(Exception):self.gate({('rev-parse','origin/main'):b'b'*40})
 def test_wrong_parent_or_subject(self):
  for command in [('rev-parse','HEAD^'),('show','-s','--format=%s','HEAD')]:
   with self.assertRaises(Exception):self.gate({command:b'wrong'})
 def test_entrypoint_and_module_identity_drift(self):
  for path in ['pi4/bin/hioc-home-assistant-association.py','pi4/lib/hioc/home_assistant_association.py']:
   with self.assertRaises(Exception):self.gate({('show',M.BASE+':'+path):b'changed'})
 def test_runtime_governance_identity_drift(self):
  with self.assertRaises(Exception):self.gate({('show',M.BASE+':governance/pe4/pe4-ha-runtime-credential-provisioning-closure.json'):b'changed'})
 def test_acceptance_closure_missing_or_mismatched(self):
  for value in [b'',b'{}']:
   with self.assertRaises(Exception):self.gate({('show',M.BASE+':'+M.ACCEPTANCE):value})
 def test_actual_readonly_validators_reused_without_main(self):
  calls=[];m=types.SimpleNamespace(deployment_integrity=lambda *a:calls.append('deployment'),runtime_probe=lambda *a:calls.append('runtime'));self.assertEqual(M.read_only_production_gate(m,None,None,{},lambda:'surfaces'),'surfaces');self.assertEqual(calls,['deployment','runtime'])
 def test_runtime_production_drift_stops_before_install(self):
  def fail(*a):raise M.Failure()
  m=types.SimpleNamespace(deployment_integrity=lambda *a:None,runtime_probe=fail);ops=Ops();report=self.deploy(ops,lambda c:M.read_only_production_gate(m,None,None,{},lambda:'surfaces'));self.assertEqual(report['RESULT'],'FAIL');self.assertEqual(ops.installs,[])
 def test_deployed_production_identity_drift_stops_before_install(self):
  def fail(*a):raise M.Failure()
  m=types.SimpleNamespace(deployment_integrity=fail,runtime_probe=lambda *a:None);ops=Ops();report=self.deploy(ops,lambda c:M.read_only_production_gate(m,None,None,{},lambda:'surfaces'));self.assertEqual(report['RESULT'],'FAIL');self.assertEqual(ops.installs,[])
 def test_canonical_closed_governance(self):validate(R,S);self.assertEqual(P.read_bytes(),canonical(R));self.assertEqual(P.with_suffix('.schema.json').read_bytes(),canonical(S))
 def test_all_bound_source_identities(self):
  for i in R['sources']:
   raw=self.blobs[i['path']];self.assertEqual(hashlib.sha256(raw).hexdigest(),i['sha256']);self.assertEqual(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),i['git_blob'])
   if not i['historical_only']:self.assertEqual((ROOT/i['path']).read_bytes().replace(b'\r\n',b'\n'),raw)
  self.assertEqual(hashlib.sha256((ROOT/R['deployment_tool']['path']).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),R['deployment_tool']['sha256'])
 def test_no_auth_no_systemd_boot_manual_execution(self):
  self.assertFalse(R['scheduler_installation_authorized']);self.assertTrue(all(x is False for x in R['negative_evidence_by_codex'].values()));self.assertFalse(R['execution_policy']['forced_boot_run']);self.assertFalse(R['execution_policy']['immediate_run']);self.assertFalse(R['execution_policy']['manual_second_adapter_authorized']);self.assertEqual(R['frozen_scheduler']['service_timer'],'NONE_CRON_REPOSITORY_CONVENTION')
 def test_rollback_and_concurrency_limit_explicit(self):
  self.assertIn('NOT_IMPLEMENTED',R['transaction']['rollback']);self.assertIn('NO_COMPARE_AND_SWAP',R['transaction']['concurrency']);self.assertFalse(R['transaction']['prior_crontab_persisted']);self.assertIn('EXCLUSIVE_OPERATOR',R['transaction']['concurrency'])
 def test_lifecycle_and_input_gates_preserved(self):
  self.assertEqual(R['lifecycle']['independent_production_acceptance'],'PASS_CLOSED');self.assertEqual(R['lifecycle']['scheduler_deployment'],'NOT_STARTED_PREPARED_FOR_SEPARATE_AUTHORIZATION');self.assertEqual(R['lifecycle']['pe4'],'NOT_COMPLETE');self.assertEqual(R['lifecycle']['phase7a'],'ACTIVE');self.assertEqual(R['frozen_scheduler']['startup'],'FIRST_SCHEDULED_SLOT_WITH_VALID_FRESH_CANONICAL_INVENTORY_NO_FORCED_BOOT_NETWORK_RUN')
 def test_document_selected_conventions_and_limits(self):
  text=(ROOT/'docs/PE4_HOME_ASSISTANT_ASSOCIATION_SCHEDULER_DEPLOYMENT_PREPARATION.md').read_text(encoding='utf8');self.assertIn('Generic installer is not reused',text);self.assertIn('no compare-and-swap',text);self.assertIn('may already',text);self.assertIn('No automatic rollback',text)
 def test_master_preparation_closed_execution_unauthorized(self):
  text=(ROOT/'docs/HIOC_MASTER_PLAN.md').read_text(encoding='utf8');table=text.split('Authoritative Current PE-4 Lifecycle',1)[1].split('### Completed',1)[0]
  self.assertIn('| PE-4 Home Assistant Association Adapter Scheduler Deployment Preparation | PASS/CLOSED |',table);self.assertIn('| PE-4 Home Assistant Association Adapter Scheduler Deployment | NOT STARTED / PREPARED FOR SEPARATE AUTHORIZATION |',table);self.assertIn('PI3 source synchronization to the scheduler preparation commit ONLY',text.split('## Current Objective',1)[1])
 def test_schema_closed_rejects_unauthorized_activity(self):
  bad=copy.deepcopy(R);bad['scheduler_installation_authorized']=True
  with self.assertRaises(ValueError):validate(bad,S)
  bad=copy.deepcopy(R);bad['lifecycle']['pe4']='COMPLETE'
  with self.assertRaises(ValueError):validate(bad,S)
  bad=copy.deepcopy(R);bad['private_extra']='synthetic'
  with self.assertRaises(ValueError):validate(bad,S)
 def test_actual_native_ops_deployment_integration(self):
  candidate=M.candidate_crontab(PRIOR)
  for rc in [0,1]:
   with patch.object(M,'read_command',side_effect=[PRIOR,PRIOR,candidate]+([candidate] if rc==0 else [])),patch.object(M.subprocess,'run',return_value=types.SimpleNamespace(returncode=rc)) as install:
    report=M.deploy(COMMIT,M.NativeOps(),lambda c:'stable');self.assertEqual(report['RESULT'],'PASS' if rc==0 else 'FAIL');self.assertEqual(install.call_count,1);self.assertEqual(install.call_args.args[0],['/usr/bin/crontab','-'])
 def test_unrelated_platform_comment_preserved(self):
  prior=b'# hioc-platform-status note unchanged  '+b'\n'+PRIOR;candidate=M.candidate_crontab(prior);self.assertEqual(candidate,prior+M.BLOCK);self.assertTrue(M.verify_candidate(prior,candidate))


class SurfaceFilesystemTests(unittest.TestCase):
 def fixture(self):
  import contextlib,stat
  class FS:
   uid=1000
   def __init__(self):
    self.data={'etc/crontab':b'# unrelated cron\n','etc/cron.d':None,'etc/cron.d/unrelated':b'0 * * * * root /safe/job\n','etc/systemd/system':None,'etc/systemd/system/unrelated.service':b'[Service]\nExecStart=/safe/job\n','etc/systemd/system/link.service':b'/safe/unrelated.service'}
    self.links={'etc/systemd/system/link.service'};self.opened=[];self.reads=[];self.block=None
   def info(self,p):
    if p not in self.data:return None
    raw=self.data[p];kind=stat.S_IFLNK if p in self.links else stat.S_IFDIR if raw is None else stat.S_IFREG
    return types.SimpleNamespace(st_uid=0,st_gid=0,st_mode=kind|(0o777 if p in self.links else 0o755 if raw is None else 0o644),st_dev=1,st_ino=list(self.data).index(p)+1,st_nlink=1,st_size=len(raw or b''))
   @contextlib.contextmanager
   def directory(self,p):
    if p==self.block:raise OSError('synthetic redirected ancestor')
    self.opened.append(p);yield p
   def read(self,p):self.reads.append(p);return self.data[p]
   def names(self,p):return (x[len(p)+1:] for x in self.data if x.startswith(p+'/') and '/' not in x[len(p)+1:])
   def readlink(self,name,dir_fd):return self.data[dir_fd+'/'+name].decode()
  return FS()
 def scan(self,fs):return M.NativeOps().surfaces(fs,fs.names,fs.readlink)
 def test_actual_scanner_normal_files_and_symlink_target_without_following(self):
  fs=self.fixture();result=self.scan(fs);self.assertEqual(len(result),64);self.assertNotIn('etc/systemd/system/link.service',fs.reads);self.assertTrue(fs.opened)
 def test_actual_scanner_rejects_association_content_name_and_symlink_target(self):
  for variant in ('content','name','target'):
   with self.subTest(variant=variant):
    fs=self.fixture()
    if variant=='content':fs.data['etc/crontab']=M.LINE
    elif variant=='name':fs.data['etc/systemd/system/hioc-ha-association.service']=b'safe'
    else:fs.data['etc/systemd/system/link.service']=b'/unsafe/hioc-home-assistant-association.py'
    with self.assertRaises(M.Failure):self.scan(fs)
 def test_actual_scanner_rejects_redirected_root(self):
  fs=self.fixture();fs.links.add('etc/cron.d')
  with self.assertRaises(M.Failure):self.scan(fs)
 def test_actual_scanner_rejects_oversized_file(self):
  fs=self.fixture();fs.data['etc/crontab']=b'x'*(M.LIMIT+1)
  with self.assertRaises(M.Failure):self.scan(fs)
 def test_actual_scanner_rejects_object_count_overflow(self):
  fs=self.fixture()
  for n in range(4096):fs.data['etc/cron.d/job'+str(n)]=b'safe'
  with self.assertRaises(M.Failure):self.scan(fs)
 def test_actual_scanner_security_failure_stops_before_install(self):
  fs=self.fixture();fs.block='etc/systemd/system';ops=Ops();report=M.deploy(COMMIT,ops,lambda c:self.scan(fs));self.assertEqual(report['RESULT'],'FAIL');self.assertEqual(ops.installs,[])

if __name__=='__main__':unittest.main()
