"""Synthetic compatibility code installation; never import/execute production tools."""
import ast,copy,hashlib,json,subprocess,unittest
from pathlib import Path
from unittest.mock import patch
from tests.test_pe4_ha_association_adapter_deployment_preparation import D,R,ROOT,COMMIT,SyntheticFS,manifest
COMP='pi4/lib/hioc/core/compatibility.py'
BASE='84635cb88380c590d2adfb655c37afd2118c629f'
class ProductionDependencyTests(unittest.TestCase):
 def setUp(self):self.fs=SyntheticFS();self.m=manifest();self.item=next(i for i in self.m['deploy'] if i['path']==COMP)
 def expect_failure(self,code,call):
  with self.assertRaises(D.Failure) as caught:call()
  self.assertEqual(caught.exception.code,code)
 def test_exact_five_existing_and_nine_additive_sets(self):
  expected={'pi4/lib/hioc/__init__.py','pi4/lib/hioc/core/__init__.py','pi4/lib/hioc/core/config.py','pi4/lib/hioc/core/state.py','pi4/lib/hioc/core/schemas.py'}
  old=json.loads(subprocess.check_output(['git','show',BASE+':'+D.RECORD],cwd=ROOT))
  self.assertEqual(D.DEPENDENCIES,expected);self.assertEqual({i['path'] for i in self.m['dependencies']},expected);self.assertEqual(len(self.m['deploy']),9)
  self.assertEqual({i['path'] for i in self.m['deploy']},{i['path'] for i in old['deployment_files']}|{COMP})
  self.assertEqual(R['runtime_governance'],old['runtime_governance']);self.assertEqual(self.item['classification'],'A_NEW_FILE_TO_DEPLOY');self.assertEqual(self.item['policy'],D.ADDITIVE_POLICY)
  self.assertEqual((self.item['owner'],self.item['group'],self.item['mode']),('jazofv1','jazofv1','0644'))
 def test_absent_compatibility_installed_exactly(self):
  self.assertNotIn(COMP,self.fs.files);D.deploy(self.fs,self.m,COMMIT);self.assertEqual(self.fs.files[COMP],self.item['bytes']);self.assertEqual(self.fs.modes[COMP],0o644)
 def test_exact_compatibility_preserved(self):
  self.fs.files[COMP]=self.item['bytes'];self.fs.modes[COMP]=0o644;D.deploy(self.fs,self.m,COMMIT);self.assertNotIn('add:'+COMP,self.fs.mutations)
 def test_different_compatibility_fails_before_intent(self):
  self.fs.files[COMP]=b'synthetic differing code';self.fs.modes[COMP]=0o644;self.expect_failure('DESTINATION_CONFLICT',lambda:D.deploy(self.fs,self.m,COMMIT));self.assertEqual(self.fs.mutations,[]);self.assertNotIn(D.TX+'/intent.json',self.fs.files)
 def test_unsafe_compatibility_fails_before_intent(self):
  for mode in (0o600,0o666,0o4755):
   fs=SyntheticFS();fs.files[COMP]=self.item['bytes'];fs.modes[COMP]=mode;self.expect_failure('UNSAFE_OBJECT',lambda:D.deploy(fs,self.m,COMMIT));self.assertEqual(fs.mutations,[])
  fs=SyntheticFS();fs.unsafe.add(COMP);self.expect_failure('UNSAFE_OBJECT',lambda:D.deploy(fs,self.m,COMMIT));self.assertEqual(fs.mutations,[])
 def test_compatibility_in_durable_intent_and_created_files(self):
  def fault(point):
   if point=='PREPARED':raise RuntimeError('synthetic interruption')
  with self.assertRaises(RuntimeError):D.deploy(self.fs,self.m,COMMIT,fault)
  intent=json.loads(self.fs.files[D.TX+'/intent.json']);self.assertIn(COMP,intent['created_files']);self.assertEqual(intent['targets'][COMP],self.item['sha256']);self.assertEqual(D.transaction_state(self.fs,self.m,COMMIT),'PREPARED');self.assertNotIn(COMP,self.fs.files)
 def test_interruption_before_after_compatibility_publication_resumes(self):
  for after in (False,True):
   with self.subTest(after=after):
    fs=SyntheticFS();original=fs.add
    def add(path,raw,mode):
     if path==COMP:
      if after:original(path,raw,mode)
      raise RuntimeError('synthetic publication interruption')
     return original(path,raw,mode)
    with patch.object(fs,'add',side_effect=add),self.assertRaises(RuntimeError):D.deploy(fs,self.m,COMMIT)
    self.assertEqual(D.transaction_state(fs,self.m,COMMIT),'PREPARED');self.assertEqual(COMP in fs.files,after)
    D.deploy(fs,self.m,COMMIT);self.assertEqual(D.transaction_state(fs,self.m,COMMIT),'COMMITTED');self.assertEqual(fs.files[COMP],self.item['bytes']);self.assertEqual(fs.mutations.count('add:'+COMP),1)
 def test_committed_rerun_never_rewrites_compatibility(self):
  D.deploy(self.fs,self.m,COMMIT);before=list(self.fs.mutations);D.deploy(self.fs,self.m,COMMIT);self.assertEqual(self.fs.mutations,before);self.assertEqual(self.fs.mutations.count('add:'+COMP),1)
 def test_all_five_existing_missing_or_different_fail_before_intent(self):
  for item in self.m['dependencies']:
   for present in (False,True):
    with self.subTest(path=item['path'],present=present):
     fs=SyntheticFS()
     if present:fs.files[item['path']]=b'synthetic byte drift'
     else:del fs.files[item['path']]
     self.expect_failure('DEPENDENCY_DRIFT',lambda:D.deploy(fs,self.m,COMMIT));self.assertEqual(fs.mutations,[]);self.assertNotIn(D.TX+'/intent.json',fs.files)
 def test_platform_cron_state_and_inventory_preserved(self):
  preserved={'pi4/bin/hioc-platform-status.py':b'synthetic pre-compatibility executable','state/platform/compatibility.json':b'synthetic private compatibility history','state/inventory/inventory.json':b'synthetic inventory','operator-crontab':b'17 3 * * * existing platform job'}
  self.fs.files.update(preserved)
  for path in preserved:self.fs.modes[path]=0o644
  D.deploy(self.fs,self.m,COMMIT)
  for path,raw in preserved.items():self.assertEqual(self.fs.files[path],raw)
  self.assertNotIn('pi4/bin/hioc-platform-status.py',{i['path'] for i in self.m['deploy']})
 def test_compatibility_uses_existing_atomic_add_publication(self):
  with patch.object(self.fs,'add',wraps=self.fs.add) as add:D.deploy(self.fs,self.m,COMMIT)
  add.assert_any_call(COMP,self.item['bytes'],0o644)
  tree=ast.parse((ROOT/'tools/hioc-pe4-ha-association-deploy.py').read_bytes());native=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='NativeFS');method=next(n for n in native.body if isinstance(n,ast.FunctionDef) and n.name=='add')
  calls=[n for n in ast.walk(method) if isinstance(n,ast.Call)];rename=next(n for n in calls if isinstance(n.func,ast.Name) and n.func.id=='rename');self.assertEqual(rename.args[-1].value,1)
 def test_direct_import_and_consumed_call_closure_no_new_dependency(self):
  adapter=ast.parse((ROOT/'pi4/lib/hioc/home_assistant_association.py').read_bytes());self.assertEqual({n.module for n in ast.walk(adapter) if isinstance(n,ast.ImportFrom) and n.level},{'core.config','core.compatibility','core.state'})
  state=ast.parse((ROOT/'pi4/lib/hioc/core/state.py').read_bytes());self.assertEqual({n.module for n in ast.walk(state) if isinstance(n,ast.ImportFrom) and n.level},{'schemas'})
  tree=ast.parse(subprocess.check_output(['git','show','HEAD:'+COMP],cwd=ROOT));self.assertFalse(any(isinstance(n,ast.ImportFrom) and n.level for n in tree.body));functions={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)};seen=set();todo=['safe_version','load_registry','assess','update_status']
  while todo:
   name=todo.pop()
   if name in seen:continue
   seen.add(name)
   for n in ast.walk(functions[name]):
    if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in functions:todo.append(n.func.id)
   self.assertFalse(any(isinstance(n,ast.ImportFrom) and n.level for n in ast.walk(functions[name])))
  self.assertNotIn('mqtt_observation',seen);self.assertNotIn('refresh_status',seen)
  helper=ast.parse((ROOT/'tools/hioc-pe4-ha-association-deploy.py').read_bytes())
  for n in ast.walk(helper):
   if isinstance(n,ast.ImportFrom):self.assertFalse((n.module or '').startswith('hioc'))
   if isinstance(n,ast.Call) and isinstance(n.func,ast.Name):self.assertNotIn(n.func.id,{'refresh_status','update_status','mqtt_observation','run_cycle'})
 def test_closed_canonical_correction_and_current_source_identities(self):
  base=ROOT/'governance/pe4/pe4-ha-association-production-dependency-correction';record=json.loads(base.with_suffix('.json').read_bytes());schema=json.loads(base.with_suffix('.schema.json').read_bytes())
  def validate(value,node):
   if 'const' in node:self.assertIs(type(value),type(node['const']));self.assertEqual(value,node['const']);return
   if node['type']=='object':
    self.assertFalse(node['additionalProperties']);self.assertEqual(set(value),set(node['required']));self.assertEqual(set(value),set(node['properties']))
    for key,child in node['properties'].items():validate(value[key],child)
   else:
    self.assertFalse(node['items']);self.assertEqual(len(value),node['minItems']);self.assertEqual(len(value),node['maxItems'])
    for item,child in zip(value,node['prefixItems']):validate(item,child)
  validate(record,schema)
  for changes in ({'production_mutation':True},{'extra':True}):
   bad=copy.deepcopy(record);bad.update(changes)
   with self.assertRaises(AssertionError):validate(bad,schema)
  for suffix in ('.json','.schema.json'):
   raw=base.with_suffix(suffix).read_bytes();self.assertEqual(raw,D.canonical(json.loads(raw)))
  for item in record['sources'].values():
   raw=(ROOT/item['path']).read_bytes().replace(b'\r\n',b'\n');self.assertEqual(D.sha(raw),item['sha256']);self.assertEqual(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),item['git_blob'])
  self.assertEqual(record['starting_commit'],D.BASELINE);self.assertEqual(R['helper'],record['sources']['deployment_helper']);self.assertFalse(record['runtime_contract_consumption']);self.assertFalse(record['production_platform_status_deployment'])
 def test_historical_platform_and_source_tree_writer_evidence(self):
  introduction='8187114c7233be82b188f0fc03b93a022787e7bb';raw=subprocess.check_output(['git','show',introduction+'^:pi4/bin/hioc-platform-status.py'],cwd=ROOT);self.assertEqual(D.sha(raw),'b65464e722bf9a4da0004ecf3bb05e4105f345a87c62405ce92d97c6298b2af8')
  tree=ast.parse(raw);self.assertFalse(any(isinstance(n,ast.ImportFrom) and 'compatibility' in (n.module or '') for n in ast.walk(tree)))
  self.assertEqual(D.sha(subprocess.check_output(['git','show','HEAD:pi4/bin/hioc-platform-status.py'],cwd=ROOT)),'55f75b7945b02f5d23759cf277b0e008a407d9d71e51a9c12b40a3cd1855c733')
  writer=ast.parse((ROOT/'tools/hioc-pe4-ha-registry-discovery.py').read_bytes());method=next(n for n in writer.body if isinstance(n,ast.FunctionDef) and n.name=='record_compatibility');imports={n.module for n in ast.walk(method) if isinstance(n,ast.ImportFrom)};self.assertIn('hioc.core.compatibility',imports);self.assertIn('hioc.core.state',imports)
  calls={n.func.id for n in ast.walk(method) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name)};self.assertIn('StateStore',calls);self.assertIn('refresh_status',calls)
if __name__=='__main__':unittest.main()
