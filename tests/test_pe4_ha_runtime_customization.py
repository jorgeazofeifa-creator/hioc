"""Correction governance and native observation tests use injected Linux metadata."""
import contextlib,copy,hashlib,importlib.util,json,os,stat,sys,unittest
from pathlib import Path,PurePosixPath
from types import SimpleNamespace
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'pi4/lib'))
from hioc import home_assistant_association as a
from tests.pe4_runtime_customization_fixtures import observation,failures,PTH_BYTES,SITE_BYTES
spec=importlib.util.spec_from_file_location('correction_deploy',ROOT/'tools/hioc-pe4-ha-association-deploy.py');D=importlib.util.module_from_spec(spec);spec.loader.exec_module(D)
class CorrectionTests(unittest.TestCase):
 def test_reviewed_bytes_match_independent_anchors(self):
  self.assertEqual(len(PTH_BYTES),151);self.assertEqual(hashlib.sha256(PTH_BYTES).hexdigest(),'2638ce9e2500e572a5e0de7faed6661eb569d1b696fcba07b0dd223da5f5d224')
  self.assertEqual(len(SITE_BYTES),155);self.assertEqual(hashlib.sha256(SITE_BYTES).hexdigest(),'43d81125d92376b1a69d53a71126a041cc9a18d8080e92dea0a2ae23be138b1e')
 def test_adapter_deployment_policies_are_identical(self):
  site=a.ENVIRONMENT/'lib/python3.11/site-packages'
  with patch.object(D,'SOURCE',ROOT):
   namespace=D.runtime_policy_namespace();self.assertEqual(namespace['CUSTOMIZATION_POLICY'],a.CUSTOMIZATION_POLICY)
   namespace['validate_runtime_customization'](observation(site),site)
   for name,bad in failures(site):
    with self.subTest(name=name),self.assertRaises(ValueError):namespace['validate_runtime_customization'](bad,site)
 def test_source_drift_rejected_without_loading_definitions(self):
  with patch.object(D,'SOURCE',ROOT),patch.object(D,'RUNTIME_POLICY_MODULE_SHA','0'*64),self.assertRaises(D.Failure):D.runtime_policy_namespace()
 def test_closed_canonical_record_schema_sources(self):
  base=ROOT/'governance/pe4/pe4-ha-association-runtime-validation-correction'
  record=json.loads(base.with_suffix('.json').read_bytes());schema=json.loads(base.with_suffix('.schema.json').read_bytes())
  def validate(v,n):
   if 'const' in n:self.assertIs(type(v),type(n['const']));self.assertEqual(v,n['const']);return
   if n['type']=='object':
    self.assertIs(type(v),dict);self.assertFalse(n['additionalProperties']);self.assertEqual(set(v),set(n['required']));self.assertEqual(set(v),set(n['properties']))
    for k,c in n['properties'].items():validate(v[k],c)
   else:
    self.assertIs(type(v),list);self.assertFalse(n['items']);self.assertEqual(len(v),n['minItems']);self.assertEqual(len(v),n['maxItems'])
    for x,c in zip(v,n['prefixItems']):validate(x,c)
  validate(record,schema)
  bad=copy.deepcopy(record);bad['production_failure_evidence']['provenance']='CODEX_OBSERVED'
  with self.assertRaises(AssertionError):validate(bad,schema)
  bad=copy.deepcopy(record);bad['extra']=True
  with self.assertRaises(AssertionError):validate(bad,schema)
  for suffix in ('.json','.schema.json'):
   raw=base.with_suffix(suffix).read_bytes();self.assertEqual(raw,D.canonical(json.loads(raw)))
  for item in record['sources'].values():
   raw=__import__('subprocess').check_output(['git','show','e4d5a19afecccb1584708e3da57ba3c0c4258523:'+item['path']],cwd=ROOT);self.assertEqual(D.sha(raw),item['sha256']);self.assertEqual(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),item['git_blob'])
  self.assertFalse(record['runtime_contract_consumption']);self.assertFalse(record['production_installation'])
 def file_info(self,raw,**changes):
  return SimpleNamespace(**dict(dict(st_dev=1,st_ino=2,st_mode=stat.S_IFREG|0o640,st_uid=1000,st_gid=1000,st_nlink=1,st_size=len(raw),st_mtime_ns=1,st_ctime_ns=1),**changes))
 @contextlib.contextmanager
 def file_api(self,raw,after=None):
  before=self.file_info(raw);reads=iter([raw,b''])
  pwd=SimpleNamespace(getpwuid=lambda uid:SimpleNamespace(pw_name='jazofv1'));grp=SimpleNamespace(getgrgid=lambda gid:SimpleNamespace(gr_name='jazofv1'))
  with patch.dict(sys.modules,{'pwd':pwd,'grp':grp}),patch.object(a,'runtime_directory',side_effect=lambda _:contextlib.nullcontext(10)),patch.object(a.os,'open',return_value=11),patch.object(a.os,'close'),patch.object(a.os,'read',side_effect=lambda *_:next(reads)),patch.object(a.os,'fstat',side_effect=[before,after or before]),patch.object(a.os,'stat',return_value=before),patch.object(a.os,'O_NOFOLLOW',0x20000,create=True),patch.object(a.os,'O_NONBLOCK',0x800,create=True),patch.object(a.os,'O_CLOEXEC',0x80000,create=True):yield
 def test_native_bounded_file_observation_feeds_policy(self):
  site=a.ENVIRONMENT/'lib/python3.11/site-packages';v=observation(site)
  with self.file_api(PTH_BYTES):v['pth']=a.runtime_file_observation(site/'distutils-precedence.pth')
  a.validate_runtime_customization(v,site)
 def test_native_read_rejects_metadata_drift(self):
  with self.file_api(PTH_BYTES,self.file_info(PTH_BYTES,st_ino=3)),self.assertRaises(ValueError):a.runtime_file_observation(Path('/reviewed/distutils-precedence.pth'))
 def test_native_namespace_metadata_link_collector_feeds_policy(self):
  import importlib.metadata
  class LinuxPath(PurePosixPath):
   def absolute(self):return self
   def resolve(self):return LinuxPath(a.CUSTOMIZATION_POLICY['site_target']) if str(self)==a.CUSTOMIZATION_POLICY['site_module'] else self
   def is_dir(self):return False
  site=LinuxPath('/accepted/site');good=observation(site)
  class Record(str):
   size=151;hash=SimpleNamespace(mode='sha256',value='JjjOniUA5XKl4N5_rtZmHrVp0baW_LoHsN0iPaX10iQ')
  entry=Record('distutils-precedence.pth');dist=SimpleNamespace(metadata={'Name':'setuptools'},version='66.1.1',files=[entry],locate_file=lambda _:site/entry)
  link=self.file_info(b'',st_mode=stat.S_IFLNK|0o777,st_uid=0,st_gid=0)
  pwd=SimpleNamespace(getpwuid=lambda _:SimpleNamespace(pw_name='root'));grp=SimpleNamespace(getgrgid=lambda _:SimpleNamespace(gr_name='root'))
  with patch.dict(sys.modules,{'pwd':pwd,'grp':grp,'sitecustomize':SimpleNamespace(__file__=a.CUSTOMIZATION_POLICY['site_module'])}),patch.object(a.sys,'path',[]),patch.object(a,'runtime_directory',side_effect=lambda _:contextlib.nullcontext(10)),patch.object(a.os,'listdir',return_value=['distutils-precedence.pth']),patch.object(a.os,'stat',return_value=link),patch.object(a.os,'readlink',return_value=a.CUSTOMIZATION_POLICY['site_target']),patch.object(a,'Path',LinuxPath),patch.object(importlib.metadata,'distributions',return_value=[dist]),patch.object(a,'runtime_file_observation',side_effect=[good['pth'],good['site_target']]):
   observed=a.runtime_customization_observation(site);a.validate_runtime_customization(observed,site)
 def test_bootstrap_and_child_require_same_policy_before_credential(self):
  site=D.ENVIRONMENT/'lib/python3.11/site-packages';good=observation(site)
  fake=dict(CUSTOMIZATION_POLICY=a.CUSTOMIZATION_POLICY,runtime_customization_observation=lambda _:copy.deepcopy(good),validate_runtime_customization=a.validate_runtime_customization)
  identity=dict(implementation='cpython',python='3.11.2',architecture='aarch64',soabi='cpython-311-aarch64-linux-gnu',websockets='16.1.1',prefix=str(D.ENVIRONMENT),executable=str(D.INTERPRETER),isolated=True,bytecode_disabled=True,origins_valid=True,distributions_valid=True)
  with patch.object(D,'SOURCE',ROOT),patch.object(D.subprocess,'run',return_value=SimpleNamespace(returncode=0,stdout=b'',stderr=b'')),patch.object(Path,'is_symlink',return_value=True),patch.object(Path,'resolve',return_value=D.ENVIRONMENT),patch.object(Path,'exists',return_value=True),patch.object(D,'runtime_policy_namespace',return_value=fake),patch.object(D,'command',side_effect=[json.dumps(identity).encode(),b'RESULT=PASS\nCREDENTIAL_READABLE_BY_RUNTIME_OPERATOR=TRUE\nNETWORK_CONNECTION_ATTEMPTED=FALSE\nHA_AUTHENTICATION_ATTEMPTED=FALSE\n']) as command:
   D.prerequisites();self.assertEqual(command.call_args_list[0].args[0][:3],[str(D.INTERPRETER),'-I','-B'])
   probe=command.call_args_list[0].args[0][-1];self.assertIn('validate_runtime_customization(runtime_customization_observation(site),site)',probe)
   fake['runtime_customization_observation']=lambda _:dict(good,user_loaded=True);command.reset_mock()
   with self.assertRaises(D.Failure) as caught:D.prerequisites()
   self.assertEqual(caught.exception.code,'RUNTIME_DRIFT');command.assert_not_called()
