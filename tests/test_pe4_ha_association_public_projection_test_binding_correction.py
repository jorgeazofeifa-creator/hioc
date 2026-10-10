"""Governed historical/current test identities; repository-only, no production access."""
import ast
import copy
import hashlib
import json
import subprocess
import unittest
from pathlib import Path
from test_pe4_ha_association_deployment_closure import canonical, validate
ROOT = Path(__file__).resolve().parents[1]
PREDECESSOR = 'c7db29f795909d7926e36c02f1166034bcebb8b0'
EDA = 'eda070d4b06ccd7f562a74e1cb6b42cb5c630d67'
IMPLEMENTATION = 'c762745b428b28518cf4415f7399ff2cacb70c66'
RECORD = 'governance/pe4/pe4-ha-association-public-projection-test-binding-correction.json'
MASTER = 'docs/HIOC_MASTER_PLAN.md'
IMPL_RECORD = 'governance/pe4/pe4-ha-association-public-projection-implementation.json'
POSIX_RECORD = 'governance/pe4/pe4-ha-association-public-projection-posix-source-validation-closure.json'
EXCEPTIONS = (
 'tests/test_pe4_ha_association_scheduler_deployment_closure.py',
 'tests/test_pe4_ha_association_implementation_preparation.py',
 'tests/test_pe4_ha_runtime_credential_provisioning.py',
 'tests/test_pe4_ha_runtime_credential_provisioning_closure.py',
)
def git(*args):
 return subprocess.check_output(['git', *args], cwd=ROOT)
def sha(raw):
 return hashlib.sha256(raw).hexdigest()
def blob(raw):
 return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def normalized(path):
 return (ROOT/path).read_bytes().replace(b'\r\n', b'\n')
def current_index(path):
 # Stage-0 bytes are the successor authority; checkout bytes are an observation.
 raw=git('show', ':'+path)
 if normalized(path) != raw:
  raise ValueError('normalized worktree differs from staged successor')
 return raw
def identity(raw, item, prefix=''):
 if sha(raw) != item[prefix+'sha256'] or blob(raw) != item[prefix+'git_blob']:
  raise ValueError('cryptographic identity mismatch')
def authority(path):
 return (IMPL_RECORD, EDA, EDA) if path == EXCEPTIONS[0] else (POSIX_RECORD, IMPLEMENTATION, IMPLEMENTATION)
def validate_successor(record, schema):
 validate(record, schema)
 if record['binding_exception_paths'] != list(EXCEPTIONS):
  raise ValueError('exact four-path boundary')
 if record['status'] != 'PASS_CLOSED' or record['closure_status'] != 'NOT_CLOSED' or record['pe4_status'] != 'NOT_COMPLETE' or record['phase_7a_status'] != 'ACTIVE' or record['pe5_status'] != 'NOT_STARTED':
  raise ValueError('unsupported lifecycle claim')
 if record['predecessor_commit'] != PREDECESSOR or any(record['codex_activity'].values()):
  raise ValueError('unsupported authority or activity')
 if [i['path'] for i in record['current_lifecycle_test_bindings']] != list(EXCEPTIONS):
  raise ValueError('exact binding boundary')
 for item in record['immutable_historical_authorities']:
  old=git('show', PREDECESSOR+':'+item['path'])
  identity(old, item)
  if normalized(item['path']) != old:
   raise ValueError('historical authority rewritten')
 for item in record['current_lifecycle_test_bindings']:
  path=item['path']; rec, commit, lifecycle=authority(path)
  if (item['historical_authority_record'], item['historical_authority_commit'], item['historical_lifecycle_authority_commit']) != (rec, commit, lifecycle):
   raise ValueError('historical authority mismatch')
  original=json.loads(git('show', PREDECESSOR+':'+rec))
  entries=[i for i in original['sources'] if i['path']==path]
  if len(entries)!=1:
   raise ValueError('path absent from original source authority')
  source=entries[0]
  if item['historical_only_original_value'] is not False or source['historical_only'] is not False:
   raise ValueError('original flag mismatch')
  if item['current_role']!='CURRENT_LIFECYCLE_TEST_IDENTITY' or item['current_runtime_authority'] is not False or item['runtime_behavior_changed'] is not False or item['production_behavior_changed'] is not False or item['historical_provenance_preserved'] is not True:
   raise ValueError('classification boundary')
  if item['historical_sha256']!=source['sha256'] or item['historical_git_blob']!=source['git_blob']:
   raise ValueError('original source identity mismatch')
  identity(git('show', commit+':'+path),item,'historical_')
  identity(git('show',lifecycle+':'+MASTER),item['historical_master_plan'])
  raw=current_index(path);identity(raw,item,'current_')
  tree=ast.parse(raw.decode('utf8'))
  literals=[n.value for n in ast.walk(tree) if isinstance(n,ast.Constant) and isinstance(n.value,str)]
  if lifecycle+':'+MASTER not in literals:
   raise ValueError('exact historical Master Plan authority missing')
  # Historical lifecycle tests must contain no evolving worktree Master Plan read.
  for node in ast.walk(tree):
   if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and node.func.attr in ('read_text','read_bytes'):
    if MASTER in ast.unparse(node.func.value):
     raise ValueError('current Master Plan used as historical authority')
 for item in record['artifacts']:
  identity(current_index(item['path']),item)
 return record
def successor():
 record_raw=current_index(RECORD)
 schema_raw=current_index(RECORD.replace('.json','.schema.json'))
 record=json.loads(record_raw);schema=json.loads(schema_raw)
 if record_raw!=canonical(record) or schema_raw!=canonical(schema):
  raise ValueError('noncanonical successor')
 return validate_successor(record,schema)
def current_artifact_bindings():
 return {item['path']:item for item in successor()['artifacts']}
def verify_source_binding(item, historical_raw, original_record, original_commit, current_raw=None, record=None):
 # Always validate the original commit, blob and digest, including historical-only sources.
 original=json.loads(git('show',PREDECESSOR+':'+original_record))
 expected_commit=original.get('starting_commit',original.get('closure_predecessor'))
 if original_commit!=expected_commit:
  raise ValueError('source authority commit mismatch')
 entries=[i for i in original['sources'] if i['path']==item['path']]
 if len(entries)!=1 or entries[0]!=item:
  raise ValueError('original source entry mismatch')
 if 'commit' in item and item['commit']!=original_commit:
  raise ValueError('source entry commit mismatch')
 identity(historical_raw,item)
 if historical_raw!=git('show',original_commit+':'+item['path']):
  raise ValueError('historical bytes mismatch')
 if item['historical_only']:
  return
 current=normalized(item['path']) if current_raw is None else current_raw.replace(b'\r\n',b'\n')
 if item['path'] not in EXCEPTIONS:
  if current!=historical_raw:
   raise ValueError('unexplained changed nonhistorical source')
  return
 accepted=successor() if record is None else validate_successor(record,json.loads(current_index(RECORD.replace('.json','.schema.json'))))
 binding=next(i for i in accepted['current_lifecycle_test_bindings'] if i['path']==item['path'])
 if (binding['historical_authority_record'],binding['historical_authority_commit'],binding['historical_sha256'],binding['historical_git_blob'])!=(original_record,original_commit,item['sha256'],item['git_blob']):
  raise ValueError('successor original identity mismatch')
 authoritative=current_index(item['path'])
 identity(authoritative,binding,'current_')
 if current!=authoritative:
  raise ValueError('current observation differs from staged successor')

class TestBindingCorrectionTests(unittest.TestCase):
 def test_closed_successor_and_exact_four_bindings(self):
  record=successor()
  self.assertEqual(len(record['current_lifecycle_test_bindings']),4)
 def test_historical_authorities_and_flags_unchanged(self):
  for rec in (IMPL_RECORD,POSIX_RECORD):
   self.assertEqual(normalized(rec),git('show',PREDECESSOR+':'+rec))
  for path in EXCEPTIONS:
   rec,commit,_=authority(path)
   item=next(i for i in json.loads(normalized(rec))['sources'] if i['path']==path)
   self.assertIs(item['historical_only'],False)
   verify_source_binding(item,git('show',commit+':'+path),rec,commit)
 def test_nonexception_changed_runtime_source_still_rejected(self):
  rec=json.loads(normalized(IMPL_RECORD))
  item=next(i for i in rec['sources'] if not i['historical_only'] and i['path'].startswith('pi4/'))
  raw=git('show',EDA+':'+item['path'])
  with self.assertRaises(ValueError):
   verify_source_binding(item,raw,IMPL_RECORD,EDA,current_raw=raw+b'\n# unexplained')
 def test_historical_only_source_still_has_immutable_identity(self):
  rec=json.loads(normalized(IMPL_RECORD))
  item=next(i for i in rec['sources'] if i['historical_only'])
  raw=git('show',EDA+':'+item['path'])
  verify_source_binding(item,raw,IMPL_RECORD,EDA,current_raw=b'different')
  with self.assertRaises(ValueError):
   verify_source_binding(item,raw+b'changed',IMPL_RECORD,EDA,current_raw=b'different')
 def test_current_master_plan_is_correction_only(self):
  text=normalized(MASTER).decode('utf8')
  section=text.split('## Historical/current lifecycle test-binding correction',1)[1].split('\n## ',1)[0]
  for phrase in ('Correction: PASS/CLOSED','Public Projection closure: NOT CLOSED','PE-4: NOT COMPLETE','Phase 7A: ACTIVE','PE-5: NOT STARTED','OPERATOR_SUPPLIED / CLOSURE DRAFT NOT YET ACCEPTED'):
   self.assertIn(phrase,section)
  self.assertNotIn('Public Projection Production Closure** - PASS/CLOSED',text)
 def test_every_nested_schema_object_is_closed(self):
  record=successor();schema=json.loads((ROOT/RECORD).with_suffix('.schema.json').read_bytes())
  def visit(value,node):
   if type(value) is dict:
    with self.assertRaises(ValueError):validate(dict(value,unreviewed=True),node)
    for k,v in value.items():visit(v,node['properties'][k])
   elif type(value) is list:
    with self.assertRaises(ValueError):validate(value+[None],node)
    for v,n in zip(value,node['prefixItems']):visit(v,n)
  visit(record,schema)

NEGATIVE_CASES = {
 'unknown_exception_path':('path','tests/test_unknown.py'),
 'docs_path_exception':('path','docs/HIOC_MASTER_PLAN.md'),
 'pi4_runtime_path_exception':('path','pi4/lib/hioc/home_assistant_association.py'),
 'tool_path_exception':('path','tools/hioc-pe4-ha-public-projection-deploy.py'),
 'release_path_exception':('path','release/payload.py'),
 'schema_path_exception':('path','governance/pe4/authority.schema.json'),
 'governance_authority_exception':('path',IMPL_RECORD),
 'path_absent_from_historical_record':('path','tests/test_absent_historical_source.py'),
 'historical_hash_mismatch':('historical_sha256','0'*64),
 'historical_blob_mismatch':('historical_git_blob','0'*40),
 'current_hash_mismatch':('current_sha256','0'*64),
 'current_blob_mismatch':('current_git_blob','0'*40),
 'historical_authority_commit_mismatch':('historical_authority_commit',PREDECESSOR),
 'historical_only_original_value_mismatch':('historical_only_original_value',True),
 'runtime_behavior_changed':('runtime_behavior_changed',True),
 'production_behavior_changed':('production_behavior_changed',True),
 'historical_provenance_not_preserved':('historical_provenance_preserved',False),
 'wildcard_exception':('path','tests/test_pe4*.py'),
 'directory_exception':('path','tests/'),
 'missing_lifecycle_authority':('historical_lifecycle_authority_commit',''),
 'current_master_as_historical_authority':('historical_lifecycle_authority_commit','HEAD'),
}
for name,(key,value) in NEGATIVE_CASES.items():
 def test(self,key=key,value=value):
  record=json.loads((ROOT/RECORD).read_bytes())
  record['current_lifecycle_test_bindings'][0][key]=value
  schema=json.loads((ROOT/RECORD).with_suffix('.schema.json').read_bytes())
  with self.assertRaises(ValueError):validate_successor(record,schema)
 setattr(TestBindingCorrectionTests,'test_reject_'+name,test)
def reject_fifth(self):
 record=json.loads((ROOT/RECORD).read_bytes());record['binding_exception_paths'].append('tests/test_extra.py')
 with self.assertRaises(ValueError):validate_successor(record,json.loads((ROOT/RECORD).with_suffix('.schema.json').read_bytes()))
def reject_claim(self):
 record=json.loads((ROOT/RECORD).read_bytes());record['pe4_status']='PASS_CLOSED'
 with self.assertRaises(ValueError):validate_successor(record,json.loads((ROOT/RECORD).with_suffix('.schema.json').read_bytes()))
TestBindingCorrectionTests.test_reject_extra_fifth_exception=reject_fifth
TestBindingCorrectionTests.test_reject_unsupported_lifecycle_claim=reject_claim
if __name__=='__main__':unittest.main()
