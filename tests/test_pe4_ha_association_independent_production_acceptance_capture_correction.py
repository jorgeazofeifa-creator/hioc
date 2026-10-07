"""Synthetic local reports only; never recover Attempt 1 or inspect evidence paths."""
import copy,hashlib,importlib.util,json,subprocess,unittest
from pathlib import Path
from test_pe4_ha_association_deployment_closure import validate,canonical
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'governance/pe4/pe4-ha-association-independent-production-acceptance-capture-correction.json'
R=json.loads(P.read_bytes()) if P.exists() else None
S=json.loads(P.with_suffix('.schema.json').read_bytes()) if P.exists() else None
spec=importlib.util.spec_from_file_location('local_capture',ROOT/'tools/hioc-pe4-ha-association-acceptance-capture.py');M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
COMMIT='a'*40
def synthetic():
 return dict({**{k:'PASS' for k in M.GATES},**{k:False for k in M.ACTIVITY}},TARGET='PI3 NUT&PIHOLE',SOURCE_COMMIT=COMMIT,MODE='READ_ONLY',ORIGINAL_EPHEMERAL_EVIDENCE_REVALIDATION='UNAVAILABLE',ORIGINAL_EPHEMERAL_EVIDENCE_LIMITATION='RECORDED',RESULT='PASS',FAILURE_STAGE='NONE')
class CaptureTests(unittest.TestCase):
 def reject(self,raw,rc=0):
  with self.assertRaises(M.CaptureFailure):M.validate_received(raw,COMMIT,rc)
 def test_python_original_identity_preserved(self):
  raw=M.canonical(synthetic());self.assertIs(M.validate_received(raw,COMMIT,0),raw)
 def test_powershell_51_mismatch_proven(self):
  raw=M.canonical(synthetic())
  script="$v=ConvertFrom-Json -InputObject ([Console]::In.ReadToEnd());$o=[ordered]@{};foreach($k in ($v.PSObject.Properties.Name | Sort-Object)){$o[$k]=$v.$k};[Console]::Write((ConvertTo-Json -InputObject $o -Compress)+[char]10)"
  result=subprocess.run(['powershell.exe','-NoProfile','-Command',script],input=raw,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  self.assertEqual(result.returncode,0);self.assertEqual(len(raw),560);self.assertEqual(len(result.stdout),565)
  i=next(i for i,(a,b) in enumerate(zip(raw,result.stdout)) if a!=b);self.assertEqual(i,550);self.assertEqual(raw[i:i+1],b'&');self.assertEqual(result.stdout[i:i+6],b'\\u0026');self.assertEqual(json.loads(result.stdout),synthetic());self.assertEqual(result.stdout,raw.replace(b'&',b'\\u0026'));self.reject(result.stdout)
 def test_malformed_json(self):self.reject(b'{\n')
 def test_duplicate_key(self):
  raw=M.canonical(synthetic());self.reject(raw.replace(b'{',b'{"TARGET":"PI3 NUT&PIHOLE",',1))
 def test_non_ascii(self):self.reject(M.canonical(synthetic()).replace(b'PIHOLE',b'PIHOL\xff'))
 def test_crlf(self):self.reject(M.canonical(synthetic()).replace(b'\n',b'\r\n'))
 def test_missing_lf(self):self.reject(M.canonical(synthetic())[:-1])
 def test_oversize(self):self.reject(b' '*4096+b'\n')
 def test_extra_private_field(self):
  v=synthetic();v['token']='synthetic';self.reject(M.canonical(v))
 def test_missing_field(self):
  v=synthetic();del v['TARGET'];self.reject(M.canonical(v))
 def test_pass_unknown(self):
  v=synthetic();v['RUNTIME']='UNKNOWN';self.reject(M.canonical(v))
 def test_pass_failure_stage(self):
  v=synthetic();v['FAILURE_STAGE']='CAPTURE';self.reject(M.canonical(v))
 def test_fail_none(self):
  v=synthetic();v['RESULT']='FAIL';self.reject(M.canonical(v),1)
 def test_return_code_mismatch(self):self.reject(M.canonical(synthetic()),1)
 def test_valid_failure_original_bytes(self):
  v=synthetic();v.update(RESULT='FAIL',FAILURE_STAGE='PRIVATE_STATE',PRIVATE_STATE='FAIL');raw=M.canonical(v);self.assertIs(M.validate_received(raw,COMMIT,2),raw)
 def test_nonfinite(self):self.reject(M.canonical(synthetic()).replace(b'false',b'NaN',1))
 def test_noncanonical_whitespace(self):self.reject(M.canonical(synthetic()).replace(b':',b': ',1))
 def test_false_integer_rejected(self):
  v=synthetic();v['ADAPTER_EXECUTED']=0;self.reject(M.canonical(v))
 def test_publish_original_manifest_last_no_evidence_io(self):
  events=[];files={};raw=M.canonical(synthetic())
  class Node:
   def __init__(self,name,parent=None):self.name=name;self.parent=parent
   def exists(self):return False
   def mkdir(self):events.append('mkdir')
   def __truediv__(self,name):return Node(name,self)
   def read_bytes(self):return files[self.name]
  directory=Node('20261007T000000-0123456789ab',Node(COMMIT))
  def write(p,v):self.assertNotIn(p.name,files);files[p.name]=v;events.append(p.name)
  M.publish_original(raw,COMMIT,0,directory,security=lambda p:None,sync=lambda p:events.append('sync'),write=write,protect=lambda p:events.append('protect'))
  self.assertIs(files['validation.json'],raw);self.assertLess(events.index('validation.json'),events.index('manifest.json'));manifest=json.loads(files['manifest.json']);self.assertEqual(manifest['validation_sha256'],hashlib.sha256(raw).hexdigest());self.assertEqual(manifest['validation_bytes'],560)
 def test_existing_directory_no_overwrite(self):
  class Node:
   name='20261007T000000-0123456789ab';parent=type('Parent',(),{'name':COMMIT})()
   def exists(self):return True
  with self.assertRaises(M.CaptureFailure):M.publish_original(M.canonical(synthetic()),COMMIT,0,Node())
 def test_old_authority_cannot_capture(self):
  v=synthetic();v['SOURCE_COMMIT']=M.BASE
  class Node:
   name='20261007T144645-b79becafb543';parent=type('Parent',(),{'name':M.BASE})()
   def exists(self):return False
  with self.assertRaises(M.CaptureFailure):M.publish_original(M.canonical(v),M.BASE,0,Node())
 def test_extra_trailing_lf_rejected(self):self.reject(M.canonical(synthetic())+b'\n')
 def test_bad_target_and_stage(self):
  for key,value in [('TARGET','OTHER'),('FAILURE_STAGE','PRIVATE_RAW_VALUE')]:
   v=synthetic();v[key]=value;self.reject(M.canonical(v))
 def test_boolean_return_code_rejected(self):self.reject(M.canonical(synthetic()),False)
 def test_flush_failure_prevents_manifest(self):
  events=[]
  class Node:
   def __init__(self,name,parent=None):self.name=name;self.parent=parent
   def exists(self):return False
   def mkdir(self):pass
   def __truediv__(self,name):return Node(name,self)
  def fail(_):raise M.CaptureFailure()
  directory=Node('20261007T000000-0123456789ab',Node(COMMIT))
  with self.assertRaises(M.CaptureFailure):M.publish_original(M.canonical(synthetic()),COMMIT,0,directory,security=lambda p:None,sync=fail,write=lambda p,v:events.append(p.name),protect=lambda p:None)
  self.assertEqual(events,['validation.json'])
 def test_closed_schema_rejects_false_acceptance_claim(self):
  bad=copy.deepcopy(R);bad['attempt_1']['capture_result']='PASS'
  with self.assertRaises(ValueError):validate(bad,S)
  bad=copy.deepcopy(R);bad['attempt_1']['evidence_recreated']=True
  with self.assertRaises(ValueError):validate(bad,S)
 def test_canonical_closed_governance(self):
  validate(R,S);self.assertEqual(P.read_bytes(),canonical(R));self.assertEqual(P.with_suffix('.schema.json').read_bytes(),canonical(S))
 def test_helper_identity_bound(self):
  self.assertEqual(hashlib.sha256(subprocess.check_output(['git','show','27377b95658010bf35c2b1fab8009de3d6f24bb6:'+R['workstation_helper']['path']],cwd=ROOT)).hexdigest(),R['workstation_helper']['sha256'])
 def test_attempt_one_remains_lost(self):
  a=R['attempt_1'];self.assertFalse(a['raw_stdout_durably_available']);self.assertFalse(a['evidence_recreated']);self.assertEqual(a['raw_stdout_revalidation'],'UNAVAILABLE');self.assertEqual(a['capture_result'],'FAIL')
 def test_no_remote_or_inspection_engine(self):
  source=(ROOT/R['workstation_helper']['path']).read_text(encoding='utf8');self.assertNotIn("['ssh'",source.lower());self.assertNotIn('socket',source);self.assertNotIn('/home/jazofv1/hioc',source);self.assertNotIn('manual-reconcile',source)
 def test_master_attempt_and_no_closure(self):
  text=(ROOT/'docs/HIOC_MASTER_PLAN.md').read_text(encoding='utf8');self.assertIn('FAIL / DURABLE CAPTURE',text);self.assertIn('Independent Production Acceptance | PASS/CLOSED |',text)
for gate in M.GATES:
 def check(self,gate=gate):
  v=synthetic();v[gate]='INVALID';self.reject(M.canonical(v))
 setattr(CaptureTests,'test_invalid_gate_'+gate.lower(),check)
for action in M.ACTIVITY:
 def check(self,action=action):
  v=synthetic();v[action]=True;self.reject(M.canonical(v))
 setattr(CaptureTests,'test_forbidden_'+action.lower(),check)
if __name__=='__main__':unittest.main()
