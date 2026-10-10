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

CORRECTION_COMMIT = '30010c54d3f3078a9b07dada36dfe8dd4db2f6e5'
CLOSURE_RECORD = 'governance/pe4/pe4-ha-association-public-projection-deployment-closure.json'
CLOSURE_SCHEMA = CLOSURE_RECORD.replace('.json','.schema.json')
CLOSURE_DOCUMENT = 'docs/PE4_HOME_ASSISTANT_ASSOCIATION_PUBLIC_PROJECTION_DEPLOYMENT_CLOSURE.md'
CLOSURE_TEST = 'tests/test_pe4_ha_association_public_projection_deployment_closure.py'
CORRECTION_HELPER = 'tests/test_pe4_ha_association_public_projection_test_binding_correction.py'
CLOSURE_PATHS = tuple(sorted((
 MASTER, CLOSURE_DOCUMENT, CLOSURE_RECORD, CLOSURE_SCHEMA, CLOSURE_TEST,
 'tests/test_pe4_ha_association_public_projection.py',
 'tests/test_pe4_ha_association_public_projection_posix_source_validation_closure.py',
 CORRECTION_HELPER,
)))
CORRECTION_ARTIFACTS = (
 'docs/PE4_HOME_ASSISTANT_ASSOCIATION_PUBLIC_PROJECTION_TEST_BINDING_CORRECTION.md',
 RECORD, RECORD.replace('.json','.schema.json'), CORRECTION_HELPER,
)
CLOSURE_HEADING = '## Public Projection production closure and PE-4 completion — 2026-10-09'

def correction_artifact_sources():
 return [dict(path=path,commit=CORRECTION_COMMIT,
              sha256=sha(git('show',CORRECTION_COMMIT+':'+path)),
              git_blob=blob(git('show',CORRECTION_COMMIT+':'+path)))
         for path in CORRECTION_ARTIFACTS]

def correction_prerequisite(record):
 return dict(artifact_sources=correction_artifact_sources(),
             binding_exception_paths=record['binding_exception_paths'],
             current_lifecycle_test_bindings=record['current_lifecycle_test_bindings'],
             immutable_historical_authorities=record['immutable_historical_authorities'],
             byte_authority={'canonical_json_authority':'GIT_STAGE_0_BYTES',
                             'worktree_observation':'CRLF_TO_LF_EQUIVALENCE_ONLY'})

def closure_master_section(text):
 if text.count(CLOSURE_HEADING)!=1:
  raise ValueError('exact current closure heading missing or duplicated')
 section=text.split(CLOSURE_HEADING,1)[1].split('\n## ',1)[0]
 for phrase in ('PUBLIC_PROJECTION=PASS/CLOSED','PE4=PASS/CLOSED','OPERATOR_SUPPLIED',
                'Phase 7A ACTIVE','PE-5 NOT_STARTED',
                '014a901a56ebc613b2235ad434ae124024ae6e01e8e1960ce98e7df6709e9944'):
  if phrase not in section:
   raise ValueError('current closure section evidence missing')
 return section

def validate_closure_successor(record=None,schema=None,correction=None):
 raw=current_index(CLOSURE_RECORD);schema_raw=current_index(CLOSURE_SCHEMA)
 actual=json.loads(raw);actual_schema=json.loads(schema_raw)
 if raw!=canonical(actual) or schema_raw!=canonical(actual_schema):
  raise ValueError('noncanonical closure stage-0 authority')
 record=actual if record is None else record
 schema=actual_schema if schema is None else schema
 validate(record,schema)
 accepted=json.loads(git('show',CORRECTION_COMMIT+':'+RECORD))
 correction=accepted if correction is None else correction
 if correction!=accepted:
  raise ValueError('original correction authority changed')
 for path in (RECORD,RECORD.replace('.json','.schema.json')):
  if current_index(path)!=git('show',CORRECTION_COMMIT+':'+path):
   raise ValueError('immutable correction record or schema changed')
 if (record['predecessor_commit'],record['predecessor_parent'],record['predecessor_subject']) != (
    CORRECTION_COMMIT,PREDECESSOR,'PE-4: correct historical lifecycle test bindings'):
  raise ValueError('closure immediate predecessor mismatch')
 if record['binding_correction_commit']!=CORRECTION_COMMIT or record['binding_correction_status']!='PASS_CLOSED':
  raise ValueError('closure binding correction authority mismatch')
 if record['binding_correction_prerequisite']!=correction_prerequisite(accepted):
  raise ValueError('exact correction prerequisite mismatch')
 if accepted['binding_exception_paths']!=list(EXCEPTIONS):
  raise ValueError('exact four-path boundary')
 for item in accepted['current_lifecycle_test_bindings']:
  identity(current_index(item['path']),item,'current_')
 sources=record['sources']
 if len(sources)!=101 or sources[-4:]!=correction_artifact_sources():
  raise ValueError('missing historical or correction source bindings')
 for item in sources:
  expected_commit=CORRECTION_COMMIT if item in sources[-4:] else PREDECESSOR
  if item['commit']!=expected_commit:
   raise ValueError('historical source authority refreshed')
  identity(git('show',item['commit']+':'+item['path']),item)
 for item in record['protected_sources']:
  old=git('show',PREDECESSOR+':'+item['path']);identity(old,item)
  if normalized(item['path'])!=old:
   raise ValueError('protected source changed')
 expected_paths=sorted(set(CLOSURE_PATHS)-{CLOSURE_RECORD,CLOSURE_SCHEMA})
 if [item['path'] for item in record['artifacts']]!=expected_paths:
  raise ValueError('exact closure artifact boundary')
 changed=set(git('diff','--name-only',CORRECTION_COMMIT).decode().splitlines())
 changed.update(git('ls-files','--others','--exclude-standard').decode().splitlines())
 if changed!=set(CLOSURE_PATHS):
  raise ValueError('unexplained closure changed path')
 for item in record['artifacts']:
  identity(current_index(item['path']),item)
 checkpoint=[i for i in record['pe4_completion_audit']['prerequisites']
             if i['checkpoint']=='Historical vs Current Lifecycle Test-Binding Correction']
 if checkpoint!=[dict(authority=RECORD,authority_commit=CORRECTION_COMMIT,
                      checkpoint='Historical vs Current Lifecycle Test-Binding Correction',
                      classification='MANDATORY_PREREQUISITE',current_status='PASS/CLOSED',
                      evidence='IMMUTABLE_REPOSITORY_FACT',prior_status='PASS/CLOSED')]:
  raise ValueError('missing accepted correction completion prerequisite')
 pe4=[i for i in record['pe4_completion_audit']['prerequisites'] if i['checkpoint']=='PE-4']
 if len(pe4)!=1 or pe4[0]['evidence']!='DERIVED_CURRENT_CLOSURE_EVALUATION' or pe4[0]['prior_status']!='NOT COMPLETE':
  raise ValueError('candidate completion misclassified as immutable fact')
 if record['production_evidence_provenance']!='OPERATOR_SUPPLIED' or record['codex_production_observation'] is not False or any(record['codex_activity'].values()):
  raise ValueError('unsupported production observation')
 for key in ('source_sync','independent_source_review','corrected_baseline','baseline_receipt',
             'deployment','installed_review','pre_slot','natural_cycle','mqtt_acceptance'):
  if record[key]['provenance']!='OPERATOR_SUPPLIED':
   raise ValueError('wrong production evidence provenance')
 original_baseline=json.loads(git('show',PREDECESSOR+':governance/pe4/pe4-ha-association-public-projection-deployment-baseline-correction.json'))
 if record['baseline_attempt_1']!=original_baseline['baseline_attempt_1'] or record['law']!=original_baseline['law'] or record['preserved_runtime']!=original_baseline['preserved_runtime']:
  raise ValueError('immutable baseline evidence changed')
 if record['correction_commit']!=PREDECESSOR or record['corrected_baseline']['correction_commit']!=PREDECESSOR or record['source_sync']['result']['SOURCE_COMMIT']!=PREDECESSOR or record['independent_source_review']['commit']!=PREDECESSOR:
  raise ValueError('historical production authority refreshed')
 for field in ('SOURCE_COMMIT','DEPLOYMENT_PREPARATION_COMMIT'):
  if record['deployment']['sanitized_result'][field]!=PREDECESSOR:
   raise ValueError('historical deployment authority refreshed')
 closure_master_section(current_index(MASTER).decode('utf8'))
 return record

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
 closure=validate_closure_successor(correction=record)
 current={item['path']:item for item in closure['artifacts']}
 for item in record['artifacts']:
  identity(git('show',CORRECTION_COMMIT+':'+item['path']),item)
  identity(current_index(item['path']),current.get(item['path'],item))
 return record
def successor():
 record_raw=current_index(RECORD)
 schema_raw=current_index(RECORD.replace('.json','.schema.json'))
 record=json.loads(record_raw);schema=json.loads(schema_raw)
 if record_raw!=canonical(record) or schema_raw!=canonical(schema):
  raise ValueError('noncanonical successor')
 return validate_successor(record,schema)
def closure_artifact_bindings():
 record=successor();closure=validate_closure_successor(correction=record)
 bindings={item['path']:item for item in record['artifacts']}
 bindings.update({item['path']:item for item in closure['artifacts']})
 return bindings
# Existing historical consumers retain the same validated authority entry point.
current_artifact_bindings = closure_artifact_bindings

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
 def test_correction_snapshot_and_current_closure_have_separate_authority(self):
  text=git('show',CORRECTION_COMMIT+':'+MASTER).decode('utf8')
  section=text.split('## Historical/current lifecycle test-binding correction',1)[1].split('\n## ',1)[0]
  for phrase in ('Correction: PASS/CLOSED','Public Projection closure: NOT CLOSED','PE-4: NOT COMPLETE','Phase 7A: ACTIVE','PE-5: NOT STARTED','OPERATOR_SUPPLIED / CLOSURE DRAFT NOT YET ACCEPTED'):
   self.assertIn(phrase,section)
  current=validate_closure_successor()
  self.assertEqual(current['binding_correction_commit'],CORRECTION_COMMIT)
  self.assertIn('PUBLIC_PROJECTION=PASS/CLOSED',closure_master_section(current_index(MASTER).decode('utf8')))
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

# The correction checkpoint remains immutable; a closure continuation has its own authority.
CLOSURE_NEGATIVES = {
 'wrong_immediate_predecessor':(('predecessor_commit',),PREDECESSOR),
 'wrong_binding_correction_commit':(('binding_correction_commit',),PREDECESSOR),
 'wrong_binding_correction_status':(('binding_correction_status',),'NOT_CLOSED'),
 'wrong_correction_artifact_sha':(('binding_correction_prerequisite','artifact_sources',0,'sha256'),'0'*64),
 'wrong_correction_artifact_blob':(('binding_correction_prerequisite','artifact_sources',0,'git_blob'),'0'*40),
 'stale_current_artifact_identity':(('artifacts',0,'sha256'),'0'*64),
 'old_unvalidated_overlay_binding':(('artifacts',0,'git_blob'),'0'*40),
 'historical_artifact_refreshed':(('sources',0,'commit'),CORRECTION_COMMIT),
 'runtime_binding_exception':(('binding_correction_prerequisite','binding_exception_paths',0),'pi4/bin/hioc-inventory-engine.py'),
 'wrong_production_provenance':(('production_evidence_provenance',),'CODEX_OBSERVED'),
 'wrong_current_completion_provenance':(('pe4_completion_audit','prerequisites',63,'evidence'),'IMMUTABLE_REPOSITORY_FACT'),
 'wrong_byte_authority':(('binding_correction_prerequisite','byte_authority','canonical_json_authority'),'RAW_WINDOWS_WORKTREE'),
}
for name,(path,value) in CLOSURE_NEGATIVES.items():
 def test(self,path=path,value=value):
  bad=copy.deepcopy(json.loads(current_index(CLOSURE_RECORD)));parent=bad
  for key in path[:-1]:parent=parent[key]
  parent[path[-1]]=value
  with self.assertRaises(ValueError):validate_closure_successor(bad)
 setattr(TestBindingCorrectionTests,'test_closure_reject_'+name,test)

def reject_missing_closure_prerequisite(self):
 bad=copy.deepcopy(json.loads(current_index(CLOSURE_RECORD)));del bad['binding_correction_prerequisite']
 with self.assertRaises(ValueError):validate_closure_successor(bad)

def reject_fifth_closure_exception(self):
 bad=copy.deepcopy(json.loads(current_index(CLOSURE_RECORD)))
 bad['binding_correction_prerequisite']['binding_exception_paths'].append('tests/test_extra.py')
 with self.assertRaises(ValueError):validate_closure_successor(bad)

def reject_historical_section_as_current(self):
 text=current_index(MASTER).decode('utf8')
 wrong=text.replace(CLOSURE_HEADING,'## Historical closure evidence')
 with self.assertRaises(ValueError):closure_master_section(wrong)
 section=closure_master_section(text)
 wrong=text.replace(section,'\nUNACCEPTED WITHOUT CURRENT EVIDENCE\n',1)
 wrong+='\n## Historical closure evidence\n'+section
 with self.assertRaises(ValueError):closure_master_section(wrong)

TestBindingCorrectionTests.test_closure_reject_missing_prerequisite=reject_missing_closure_prerequisite
TestBindingCorrectionTests.test_closure_reject_fifth_exception=reject_fifth_closure_exception
TestBindingCorrectionTests.test_closure_reject_historical_section_as_current=reject_historical_section_as_current

if __name__=='__main__':unittest.main()
