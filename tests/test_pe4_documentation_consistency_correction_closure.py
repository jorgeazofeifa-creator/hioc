"""Documentation closure successor; Git evidence only, no operational authority."""
import copy
import hashlib
import json
import os
import subprocess
import unittest
from functools import lru_cache
from pathlib import Path
from contextlib import contextmanager
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
PREDECESSOR='5472a85194d105f6fb3d08ce51a4788256d8f028'
RECORD='governance/pe4/pe4-documentation-consistency-correction-closure.json'
SCHEMA=RECORD.replace('.json','.schema.json')
HISTORICAL_RECORD='governance/pe4/pe4-documentation-consistency-correction.json'
ACCEPTED_CLOSURE='9c6784e7541beccf42192f3a1cf63269bedd8129'
CANDIDATE_PATHS=tuple(sorted([
 'docs/HIOC_MASTER_PLAN.md',
 'tests/test_pe4_documentation_consistency_correction.py',
 'tests/test_pe4_ha_association_public_projection_test_binding_correction.py',
 'tests/test_compatibility_master_plan_governance.py',
 'tests/test_pe4_0b2b_execution_closure.py',
 'tests/test_pe4_0c1_association_lifecycle.py',
 'tests/test_pe4_0c_association_contract.py',
 'docs/PE4_DOCUMENTATION_CONSISTENCY_CORRECTION_CLOSURE.md',
 RECORD,SCHEMA,'tests/test_pe4_documentation_consistency_correction_closure.py']))
def git(*args):
 return subprocess.check_output(['git','--no-optional-locks',*args],cwd=ROOT,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
def digest(raw):return hashlib.sha256(raw).hexdigest()
def blob(raw):return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def canonical(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False)+'\n').encode()
def closed_schema(v):
 if type(v) is dict:return dict(type='object',additionalProperties=False,required=sorted(v),properties={k:closed_schema(x) for k,x in sorted(v.items())})
 if type(v) is list:return dict(type='array',minItems=len(v),maxItems=len(v),prefixItems=[closed_schema(x) for x in v],items=False)
 return {'const':v}
def require(value,message):
 if not value:raise ValueError(message)
def current_bytes(path):
 from test_pe5_execution_roadmap import roadmap_binding as pe5_roadmap_binding
 bound=pe5_roadmap_binding(path)
 if bound is not None:
  return (ROOT/path).read_bytes().replace(b'\r\n',b'\n')
 from test_pe5_service_association_caller import CALLER_PATHS, caller_current_binding
 if path in CALLER_PATHS:
  caller_current_binding(path)
  return (ROOT/path).read_bytes().replace(b'\r\n',b'\n')
 from test_pe5_implementation_preparation import CANDIDATE_PATHS as PE5_PATHS, current_binding as pe5_binding
 if path in PE5_PATHS:
  pe5_binding(path)
  return (ROOT/path).read_bytes().replace(b'\r\n',b'\n')
 from test_pe10_surveillance_roadmap_preservation import CANDIDATE_PATHS as ROADMAP_PATHS, current_binding as roadmap_binding
 if path in ROADMAP_PATHS:
  roadmap_binding(path)
  return (ROOT/path).read_bytes().replace(b'\r\n',b'\n')
 raw=(ROOT/path).read_bytes().replace(b'\r\n',b'\n')
 # Existing candidates stay unstaged. Committed successors use their Git object bytes.
 head=git('rev-parse','HEAD').decode().strip()
 if head!=PREDECESSOR:
  require(git('show',head+':'+path)==raw,'committed checkout mismatch')
 return raw
def _validate_historical_closure(record,schema):
 require(schema=={'$schema':'https://json-schema.org/draft/2020-12/schema','title':'PE-4 documentation consistency correction closure',**closed_schema(record)},'exact schema mismatch')
 require(record['predecessor_commit']==PREDECESSOR and record['accepted_correction_commit']==PREDECESSOR,'wrong accepted predecessor')
 require(record['status']=='PASS/CLOSED' and record['pe5_start_authorized'] is False and record['post_closure_next_task']=='UNKNOWN_NOT_YET_AUTHORIZED','closure or authorization mismatch')
 require(record['lifecycle']==dict(documentation_consistency_correction='PASS/CLOSED',pe4='PASS/CLOSED',public_projection='PASS/CLOSED',phase7a='ACTIVE',pe5='NOT_STARTED'),'lifecycle mismatch')
 require(record['authorized_paths']==list(CANDIDATE_PATHS),'wrong closure path boundary')
 head=git('rev-parse','HEAD').decode().strip()
 require(not git('diff','--cached','--name-only'),'staging must remain empty')
 if head==PREDECESSOR:
  changed=set(git('diff','--name-only',PREDECESSOR).decode().splitlines())
  changed.update(git('ls-files','--others','--exclude-standard').decode().splitlines())
 else:
  require(git('rev-parse','HEAD^').decode().strip()==PREDECESSOR,'wrong committed closure parent')
  require(not git('status','--porcelain'),'committed closure must be clean')
  changed=set(git('diff','--name-only',PREDECESSOR,head).decode().splitlines())
 require(changed==set(CANDIDATE_PATHS),'unexplained closure mutation')
 require(not git('stash','list'),'authorized stash disposition not complete')
 accepted=json.loads(git('show',PREDECESSOR+':'+HISTORICAL_RECORD))
 require(len(accepted['findings'])==49 and all(x['resolution']=='RESOLVED' for x in accepted['findings']),'accepted findings not closed')
 require(record['accepted_path_count']==33 and record['resolved_finding_count']==49,'accepted scope mismatch')
 require(record['acceptance_evidence']==dict(validation='COMPLETE',independent_review='COMPLETE',commit='COMPLETE',push='COMPLETE',independent_github_verification='COMPLETE_OPERATOR_SUPPLIED',repository_synchronization='COMPLETE',stash_disposition='COMPLETE_AUTHORIZED_DROP'),'acceptance evidence mismatch')
 for item in record['accepted_artifacts']:
  raw=git('show',PREDECESSOR+':'+item['path'])
  require(digest(raw)==item['sha256'] and blob(raw)==item['git_blob'],'accepted identity mismatch')
 require({x['path'] for x in record['accepted_artifacts']}==set(accepted['authorized_paths']),'accepted artifact map incomplete')
 for item in accepted['artifacts']:
  raw=git('show',PREDECESSOR+':'+item['path'])
  require(digest(raw)==item['sha256'] and blob(raw)==item['git_blob'],'historical correction identity mismatch')
 for path in accepted['new_artifacts'][:3]:
  require(current_bytes(path)==git('show',PREDECESSOR+':'+path),'historical correction package changed')
 require({x['path'] for x in record['artifacts']}==set(CANDIDATE_PATHS)-{RECORD,SCHEMA},'current artifact map incomplete')
 for item in record['artifacts']:
  raw=current_bytes(item['path'])
  require(digest(raw)==item['sha256'] and blob(raw)==item['git_blob'],'closure identity mismatch')
 # Exact scope already excludes every runtime/executable and all historical records.
 old=git('show',PREDECESSOR+':docs/HIOC_MASTER_PLAN.md').decode().splitlines(keepends=True);candidate=list(old)
 for op in sorted(record['master_operations'],key=lambda x:x['start_line'],reverse=True):
  start,end=op['start_line'],op['end_line']
  require(digest(''.join(old[start-1:end]).rstrip('\n').encode())==op['original_sha256'],'original Master operation mismatch')
  candidate[start-1:end]=[op['replacement']+'\n']
 require(''.join(candidate).encode()==current_bytes('docs/HIOC_MASTER_PLAN.md'),'unrelated Master text changed')
 master=current_bytes('docs/HIOC_MASTER_PLAN.md').decode()
 objective=master.split('## Current Objective',1)[1].split('### Historical',1)[0]
 next_task=master.split('## Next Planned Task',1)[1].split('### Historical',1)[0]
 require(next_task.strip().startswith('### Post-Closure Next Task — UNKNOWN / NOT YET AUTHORIZED'),'unknown next-task pointer missing')
 for section in [objective,next_task]:
  for phrase in ['Documentation Consistency Correction PASS/CLOSED',PREDECESSOR,'PE-4 PASS/CLOSED','Public Projection PASS/CLOSED','Phase 7A ACTIVE','PE-5 NOT_STARTED','PE-5 START NOT AUTHORIZED','UNKNOWN / NOT YET AUTHORIZED']:
   require(phrase in section,'current closure truth missing')
  for phrase in ['uncommitted candidate','pending validation','commit/push must close']:
   require(phrase not in section,'candidate preparation presented as current')
 require('surveillance' not in master.lower(),'surveillance roadmap added')
 require(not record['runtime_behavior_changed'] and not record['production_evidence_changed'],'operational scope changed')
 require(all(v is False for v in record['unauthorized_activity'].values()),'unauthorized activity')
 return record
@contextmanager
def accepted_closure_context():
 original_git=git
 def accepted_bytes(path):return original_git('show',ACCEPTED_CLOSURE+':'+path)
 def accepted_git(*args):
  if args==('rev-parse','HEAD'):return (ACCEPTED_CLOSURE+'\n').encode()
  if args==('rev-parse','HEAD^'):return (PREDECESSOR+'\n').encode()
  if args in [('status','--porcelain'),('diff','--cached','--name-only'),('stash','list')]:return b''
  return original_git(*args)
 with patch.dict(globals(),git=accepted_git,current_bytes=accepted_bytes):yield

def validate_closure(record,schema):
 with accepted_closure_context():return _validate_historical_closure(record,schema)

@lru_cache(maxsize=1)
def successor():
 raw=git('show',ACCEPTED_CLOSURE+':'+RECORD);schema_raw=git('show',ACCEPTED_CLOSURE+':'+SCHEMA)
 record=json.loads(raw);schema=json.loads(schema_raw)
 require(raw==canonical(record) and schema_raw==canonical(schema),'noncanonical accepted closure')
 return validate_closure(record,schema)

def current_binding(path):
 from test_pe5_execution_roadmap import roadmap_binding as pe5_roadmap_binding
 bound=pe5_roadmap_binding(path)
 if bound is not None:
  return bound
 from test_pe5_service_association_caller import CALLER_PATHS, caller_current_binding
 if path in CALLER_PATHS:return caller_current_binding(path)
 from test_pe5_implementation_preparation import CANDIDATE_PATHS as PE5_PATHS, current_binding as pe5_binding
 if path in PE5_PATHS:return pe5_binding(path)
 from test_pe10_surveillance_roadmap_preservation import CANDIDATE_PATHS as ROADMAP_PATHS, current_binding as roadmap_binding
 if path in ROADMAP_PATHS:return roadmap_binding(path)
 record=successor();accepted=json.loads(git('show',PREDECESSOR+':'+HISTORICAL_RECORD))
 entries={x['path']:x for x in accepted['artifacts']};entries.update({x['path']:x for x in record['artifacts']})
 require(path in entries,'outside exact current map');item=entries[path];raw=current_bytes(path)
 require(digest(raw)==item['sha256'] and blob(raw)==item['git_blob'],'current identity mismatch')
 return item
class DocumentationConsistencyCorrectionClosureTests(unittest.TestCase):
 def test_exact_successor_and_current_identities(self):successor()
 def test_accepted_correction_is_historical(self):
  r=successor();self.assertEqual(r['accepted_correction_commit'],PREDECESSOR)
  for path in [HISTORICAL_RECORD,HISTORICAL_RECORD.replace('.json','.schema.json'),'docs/PE4_DOCUMENTATION_CONSISTENCY_CORRECTION.md']:
   self.assertEqual(current_bytes(path),git('show',PREDECESSOR+':'+path))
 def test_unknown_next_task_and_no_pe5_authorization(self):
  r=successor();self.assertFalse(r['pe5_start_authorized']);self.assertEqual(r['post_closure_next_task'],'UNKNOWN_NOT_YET_AUTHORIZED')
 def test_historical_candidate_law_preserved(self):
  from test_pe4_documentation_consistency_correction import successor as historical
  self.assertEqual(historical()['status'],'UNCOMMITTED_CORRECTION_CANDIDATE')
 def test_reject_wrong_predecessor_and_pe5_promotion(self):
  r=successor()
  for key,value in [('accepted_correction_commit','0'*40),('pe5_start_authorized',True),('post_closure_next_task','PE5_IMPLEMENTATION')]:
   bad=copy.deepcopy(r);bad[key]=value
   with self.assertRaises(ValueError):validate_closure(bad,{'$schema':'https://json-schema.org/draft/2020-12/schema','title':'PE-4 documentation consistency correction closure',**closed_schema(bad)})
 def test_reject_mutated_identity_or_extra_path(self):
  for target in ['artifacts','accepted_artifacts']:
   bad=copy.deepcopy(successor());bad[target][0]['sha256']='0'*64
   with self.assertRaises(ValueError):validate_closure(bad,{'$schema':'https://json-schema.org/draft/2020-12/schema','title':'PE-4 documentation consistency correction closure',**closed_schema(bad)})
  bad=copy.deepcopy(successor());bad['authorized_paths'].append('pi4/unapproved.py')
  with self.assertRaises(ValueError):validate_closure(bad,{'$schema':'https://json-schema.org/draft/2020-12/schema','title':'PE-4 documentation consistency correction closure',**closed_schema(bad)})
 def test_reject_schema_drift(self):
  r=successor();s=json.loads(current_bytes(SCHEMA));s['additionalProperties']=True
  with self.assertRaises(ValueError):validate_closure(r,s)
 def test_post_commit_truth_has_no_own_sha_dependency(self):
  r=successor();self.assertNotIn('own_commit',r)
  self.assertEqual(r['status'],'PASS/CLOSED');self.assertEqual(r['accepted_correction_commit'],PREDECESSOR)
if __name__=='__main__':unittest.main()
