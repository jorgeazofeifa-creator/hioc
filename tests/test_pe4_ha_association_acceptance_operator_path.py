"""Integrated local transport and native disposable Windows evidence tests; no PI3."""
import importlib.util,json,pathlib,subprocess,sys,unittest,uuid,shutil,hashlib
from unittest.mock import patch
ROOT=pathlib.Path(__file__).resolve().parents[1]
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
C=load('capture_operator_test','tools/hioc-pe4-ha-association-acceptance-capture.py')
O=load('operator_transport_test','tools/hioc-pe4-ha-association-acceptance-operator.py')
R=load('remote_producer_test','tools/hioc-pe4-ha-association-independent-acceptance.py')
COMMIT='a'*40
class OperatorPathTests(unittest.TestCase):
 def raw(self,fail=False):
  def checks(report):
   for k in R.GATES:report[k]='PASS'
   if fail:report['PRIVATE_STATE']='FAIL';report['FAILURE_STAGE']='PRIVATE_STATE';raise ValueError('synthetic private message')
  return R.produce(COMMIT,checks=checks,gate=lambda c:None)
 def process(self,raw,rc,stderr=False):
  # Exact raw bytes and measured return code cross a real LOCAL process pipe.
  code='import sys;sys.stdout.buffer.write('+repr(raw)+');'+('sys.stderr.write("synthetic discarded stderr");' if stderr else '')+'raise SystemExit('+str(rc)+')'
  return lambda:O.transport([sys.executable,'-I','-B','-c',code])
 def invoke(self,raw,rc,publish=None):return O.execute(COMMIT,'20261007T000000-0123456789ab',self.process(raw,rc),publish or (lambda *a:None),C.validate_received)
 def test_end_to_end_pass(self):
  raw,rc=self.raw();seen=[];self.assertEqual(rc,0);self.assertEqual(self.invoke(raw,rc,lambda data,*a:seen.append(data)),0);self.assertEqual(seen,[raw])
 def test_end_to_end_fail_rc2(self):
  raw,rc=self.raw(True);seen=[];self.assertEqual(rc,2);self.assertEqual(self.invoke(raw,rc,lambda data,*a:seen.append(data)),2);self.assertEqual(seen,[raw])
 def test_stderr_discarded(self):
  raw,rc=self.raw();self.assertEqual(O.execute(COMMIT,'run',self.process(raw,rc,True),lambda *a:None,C.validate_received),0)
 def reject(self,raw,rc=0):
  with self.assertRaises(Exception):self.invoke(raw,rc)
 def test_transport_failure(self):self.reject(b'',255)
 def test_empty_stdout(self):self.reject(b'')
 def test_oversized_stdout(self):self.reject(b' '*4097)
 def test_malformed(self):self.reject(b'{\n')
 def test_wrong_commit(self):
  raw,rc=self.raw();self.reject(raw.replace(COMMIT.encode(),b'b'*40))
 def test_wrong_return_code(self):self.reject(self.raw()[0],1)
 def test_pass_rc2_mismatch(self):self.reject(self.raw()[0],2)
 def test_fail_rc0_mismatch(self):self.reject(self.raw(True)[0],0)
 def test_byte_mutation(self):self.reject(self.raw()[0].replace(b'&',b'\\u0026'))
 def test_private_extra_field(self):
  v=json.loads(self.raw()[0]);v['private_id']='synthetic';self.reject(C.canonical(v))
 def test_duplicate_key(self):self.reject(self.raw()[0].replace(b'{',b'{"MODE":"READ_ONLY",',1))
 def test_crlf(self):self.reject(self.raw()[0].replace(b'\n',b'\r\n'))
 def test_non_ascii(self):self.reject(self.raw()[0].replace(b'PIHOLE',b'PIHOL\xff'))
 def test_noncanonical(self):self.reject(self.raw()[0].replace(b':',b': ',1))
 def test_transport_timeout(self):
  with patch.object(O,'TIMEOUT',.1):
   with self.assertRaises(Exception):O.transport([sys.executable,'-I','-B','-c','import time;time.sleep(1)'])
 def test_capture_failure_no_retry(self):
  raw,rc=self.raw();calls=[]
  def receive():calls.append(1);return raw,rc
  def fail(*a):raise C.CaptureFailure()
  with self.assertRaises(C.CaptureFailure):O.execute(COMMIT,'run',receive,fail,C.validate_received)
  self.assertEqual(calls,[1])
 def test_acl_failure_no_retry(self):
  raw,rc=self.raw()
  with self.assertRaises(C.CaptureFailure):self.invoke(raw,rc,lambda *a:(_ for _ in ()).throw(C.CaptureFailure()))
 def test_native_windows_pass_fail_durability(self):
  self.assertGreaterEqual(sys.version_info[:2],(3,12));base=ROOT/('.hioc-capture-synthetic-'+uuid.uuid4().hex);parent=base/COMMIT
  self.assertEqual(base.resolve().parent,ROOT.resolve());self.assertFalse(base.exists());base.mkdir()
  try:
   C.protect_new_directory(base);C.secure_directory(base);parent=O.prepare_parent(base,COMMIT,C);C.secure_directory(parent);C.durable_directory(parent)
   for fail,run_id in [(False,'20261007T000000-0123456789ab'),(True,'20261007T000001-0123456789ac')]:
    raw,rc=self.raw(fail);directory=parent/run_id
    result=O.execute(COMMIT,run_id,self.process(raw,rc),lambda data,c,r,n:C.publish_original(data,c,r,parent/n),C.validate_received)
    self.assertEqual(result,rc);self.assertEqual((directory/'validation.json').read_bytes(),raw)
    C.secure_directory(directory/'validation.json',file=True);C.secure_directory(directory/'manifest.json',file=True)
    manifest=json.loads((directory/'manifest.json').read_bytes());self.assertEqual(manifest['validation_sha256'],hashlib.sha256(raw).hexdigest());self.assertEqual(manifest['validation_bytes'],len(raw))
    with self.assertRaises(C.CaptureFailure):C.publish_original(raw,COMMIT,rc,directory)
   # An injected unsupported flush must stop before publishing manifest.
   raw,rc=self.raw();directory=parent/'20261007T000002-0123456789ad'
   with self.assertRaises(C.CaptureFailure):C.publish_original(raw,COMMIT,rc,directory,sync=lambda _:(_ for _ in ()).throw(C.CaptureFailure()))
   self.assertTrue((directory/'validation.json').exists());self.assertFalse((directory/'manifest.json').exists())
  finally:
   self.assertEqual(base.resolve().parent,ROOT.resolve());self.assertTrue(base.name.startswith('.hioc-capture-synthetic-'));shutil.rmtree(base)
 def test_existing_run_security_rejection(self):
  class Node:
   name='20261007T000000-0123456789ab';parent=type('Parent',(),{'name':COMMIT})()
   def exists(self):return True
  with self.assertRaises(C.CaptureFailure):C.publish_original(self.raw()[0],COMMIT,0,Node())
 def test_source_binding_exact_future_contract(self):
  root=ROOT;commit=COMMIT;raw=(ROOT/'tools/hioc-pe4-ha-association-acceptance-capture.py').read_bytes().replace(b'\r\n',b'\n')
  def fake(args,**kwargs):
   command=args[3:]
   if command==['rev-parse','HEAD'] or command==['rev-parse','origin/main']:out=(commit+'\n').encode()
   elif command==['branch','--show-current']:out=b'main\n'
   elif command==['rev-parse','HEAD^']:out=(C.BASE+'\n').encode()
   elif command[:3]==['show','-s','--format=%s']:out=(C.SUBJECT+'\n').encode()
   elif command[:1]==['status']:out=b''
   elif command[:1]==['show']:out=raw
   elif command[:2]==['rev-parse','--git-path']:out=('nonexistent-synthetic-marker-'+command[2]).encode()
   else:raise AssertionError(command)
   return type('Result',(),{'returncode':0,'stdout':out})()
  with patch.object(C.subprocess,'run',fake):self.assertTrue(C.source_binding(root,commit))
 def test_governance_canonical_closed(self):
  from test_pe4_ha_association_deployment_closure import validate,canonical
  p=ROOT/'governance/pe4/pe4-ha-association-independent-production-acceptance-operator-path.json';v=json.loads(p.read_bytes());schema=json.loads(p.with_suffix('.schema.json').read_bytes());validate(v,schema);self.assertEqual(p.read_bytes(),canonical(v));self.assertEqual(p.with_suffix('.schema.json').read_bytes(),canonical(schema))
  for item in v['implementation_bindings']+v['read_only_bindings']:self.assertEqual(hashlib.sha256((ROOT/item['path']).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),item['sha256'])
 def test_attempt_one_history_exact(self):
  p=ROOT/'governance/pe4/pe4-ha-association-independent-production-acceptance-operator-path.json';v=json.loads(p.read_bytes());old=json.loads((ROOT/'governance/pe4/pe4-ha-association-independent-production-acceptance-capture-correction.json').read_bytes());self.assertEqual(v['attempt_1'],old['attempt_1']);self.assertEqual(v['original_ephemeral_evidence_limitation'],old['historical_original_limitation'])
 def test_return_code_bound_and_unexecuted(self):
  v=json.loads((ROOT/'governance/pe4/pe4-ha-association-independent-production-acceptance-operator-path.json').read_bytes());self.assertEqual((v['return_codes']['pass'],v['return_codes']['fail']),(R.PASS_RC,R.FAIL_RC));self.assertFalse(v['lifecycle']['attempt_2_authorized']);self.assertFalse(v['lifecycle']['second_adapter_execution_authorized']);self.assertTrue(all(x is False for x in v['negative_evidence_by_codex'].values()))
 def test_master_ready_not_authorized(self):
  text=(ROOT/'docs/HIOC_MASTER_PLAN.md').read_text(encoding='utf8');self.assertIn('Operator Path Integration | PASS/CLOSED',text);self.assertIn('READY FOR SEPARATE AUTHORIZATION',text);self.assertIn('NOT AUTHORIZED',text)
if __name__=='__main__':unittest.main()
