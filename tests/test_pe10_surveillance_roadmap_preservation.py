"""Future surveillance roadmap preservation; no collector or production execution."""
import copy,hashlib,json,os,subprocess,unittest
from functools import lru_cache
from pathlib import Path
from contextlib import contextmanager
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
PREDECESSOR='9c6784e7541beccf42192f3a1cf63269bedd8129'
ACCEPTED_ROADMAP='6f69c4dfb85924a83b59e85ef2da602fc75ec5ea'
RECORD='governance/pe4/pe10-surveillance-roadmap-preservation.json'
SCHEMA=RECORD.replace('.json','.schema.json')
MASTER='docs/HIOC_MASTER_PLAN.md'
CANDIDATE_PATHS=tuple(sorted([MASTER,RECORD,SCHEMA,'tests/test_pe10_surveillance_roadmap_preservation.py','tests/test_pe4_documentation_consistency_correction_closure.py','tests/test_pe4_ha_association_public_projection_test_binding_correction.py']))
CAPABILITY='Surveillance Reliability, Recording Integrity, and Camera Infrastructure Monitoring'
ORIGINAL_SPECIFICATION_SHA256='55b564f68e0116beeab54199659c8c8a1a601e86f2f420dcf7d903acb1191e24'
def git(*args):return subprocess.check_output(['git','--no-optional-locks',*args],cwd=ROOT,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
def digest(raw):return hashlib.sha256(raw).hexdigest()
def blob(raw):return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def canonical(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False)+'\n').encode()
def closed(v):
 if type(v) is dict:return dict(type='object',additionalProperties=False,required=sorted(v),properties={k:closed(x) for k,x in sorted(v.items())})
 if type(v) is list:return dict(type='array',minItems=len(v),maxItems=len(v),prefixItems=[closed(x) for x in v],items=False)
 return {'const':v}
def require(value,message):
 if not value:raise ValueError(message)
def current_bytes(path):return (ROOT/path).read_bytes().replace(b'\r\n',b'\n')
def _validate_historical_roadmap(record,schema):
 require(schema=={'$schema':'https://json-schema.org/draft/2020-12/schema','title':'PE-10 surveillance roadmap preservation',**closed(record)},'exact roadmap schema mismatch')
 require(record['predecessor_commit']==PREDECESSOR and record['authorized_paths']==list(CANDIDATE_PATHS),'wrong roadmap scope')
 require(record['capability']==CAPABILITY and record['capability_status']=='PLANNED_NOT_STARTED' and record['implementation_authorized'] is False,'surveillance authorization mismatch')
 require(record['architectural_home']=='PE10_APPLICATION_INTEGRATION_SERVICE_ASSURANCE' and record['checkpoint_count']==6,'wrong surveillance placement')
 require(record['lifecycle']==dict(phase7a='ACTIVE',pe4='PASS/CLOSED',public_projection='PASS/CLOSED',documentation_consistency_correction='PASS/CLOSED',pe5='NOT_STARTED') and record['pe5_start_authorized'] is False and record['current_next_task']=='UNKNOWN_NOT_YET_AUTHORIZED','current sequence changed')
 require(not git('diff','--cached','--name-only'),'staging must remain empty')
 head=git('rev-parse','HEAD').decode().strip()
 if head==PREDECESSOR:
  changed=set(git('diff','--name-only',PREDECESSOR).decode().splitlines());changed.update(git('ls-files','--others','--exclude-standard').decode().splitlines())
 else:
  require(git('rev-parse','HEAD^').decode().strip()==PREDECESSOR and not git('status','--porcelain'),'wrong committed roadmap successor')
  changed=set(git('diff','--name-only',PREDECESSOR,head).decode().splitlines())
 require(changed==set(CANDIDATE_PATHS),'unexplained roadmap mutation')
 require(not git('stash','list'),'unexpected stash')
 require({x['path'] for x in record['artifacts']}==set(CANDIDATE_PATHS)-{RECORD,SCHEMA},'incomplete current map')
 for item in record['artifacts']:
  raw=current_bytes(item['path']);require(digest(raw)==item['sha256'] and blob(raw)==item['git_blob'],'current roadmap identity mismatch')
 for item in record['historical_artifacts']:
  raw=git('show',PREDECESSOR+':'+item['path']);require(digest(raw)==item['sha256'] and blob(raw)==item['git_blob'],'historical identity mismatch')
  require(current_bytes(item['path'])==raw,'accepted package rewritten')
 old=git('show',PREDECESSOR+':'+MASTER).decode().splitlines(keepends=True);candidate=list(old)
 for ins in sorted(record['master_insertions'],key=lambda x:x['after_line'],reverse=True):
  require(digest(old[ins['after_line']-1].rstrip('\n').encode())==ins['anchor_sha256'],'roadmap insertion anchor mismatch')
  candidate[ins['after_line']:ins['after_line']]=[ins['text']+'\n']
 require(''.join(candidate).encode()==current_bytes(MASTER),'existing Master content changed')
 master=current_bytes(MASTER).decode();original=''.join(old)
 for marker in ['## Current Objective','## Next Planned Task']:
  section=master.split(marker,1)[1].split('### Historical',1)[0];prior=original.split(marker,1)[1].split('### Historical',1)[0]
  require(section==prior,'current objective or sequencing changed')
 require(master.count('#### '+CAPABILITY)==1,'duplicate surveillance capability')
 surveillance=master.split('#### '+CAPABILITY,1)[1].split('### Status Vocabulary',1)[0]
 require(surveillance.count('##### Surveillance checkpoint ')==6,'wrong bounded checkpoints')
 for phrase in record['required_surveillance_phrases']:require(phrase in surveillance,'missing surveillance requirement: '+phrase)
 require('Status: **PLANNED / NOT STARTED — IMPLEMENTATION NOT AUTHORIZED**' in surveillance,'future status missing')
 require('192.168.100.152 is obsolete historical addressing' in surveillance and 'not newly\nobserved production evidence' in surveillance,'historical context converted into current evidence')
 source=master.split('<!-- ORIGINAL_SURVEILLANCE_SPECIFICATION_BEGIN -->\n```text\n',1)[1].split('```\n<!-- ORIGINAL_SURVEILLANCE_SPECIFICATION_END -->',1)[0]
 import re
 require(digest(source.encode())==ORIGINAL_SPECIFICATION_SHA256==record['original_specification']['normalized_utf8_sha256'],'original specification not preserved verbatim')
 require([int(n) for n in re.findall(r'(?m)^={10,}\n(\d+)\. [^\n]+\n={10,}$',source)]==list(range(1,74)),'original 73-section scope changed')
 require(record['original_specification']['testing_clarification'] in master.split('# Decision Log',1)[1],'testing exception absent from decisions')
 require('Do NOT reintroduce a second go2rtc architecture without a specific future requirement.' in surveillance,'conditional go2rtc requirement lost')
 require(all(v is False for v in record['implementation_activity'].values()),'implementation authority introduced')
 return record
@contextmanager
def accepted_roadmap_context():
 original_git=git
 def accepted_bytes(path):return original_git('show',ACCEPTED_ROADMAP+':'+path)
 def accepted_git(*args):
  if args==('rev-parse','HEAD'):return (ACCEPTED_ROADMAP+'\n').encode()
  if args==('rev-parse','HEAD^'):return (PREDECESSOR+'\n').encode()
  if args in [('status','--porcelain'),('diff','--cached','--name-only'),('stash','list')]:return b''
  return original_git(*args)
 with patch.dict(globals(),git=accepted_git,current_bytes=accepted_bytes):yield

def validate_record(record,schema):
 with accepted_roadmap_context():return _validate_historical_roadmap(record,schema)

@lru_cache(maxsize=1)
def successor():
 raw=git('show',ACCEPTED_ROADMAP+':'+RECORD);schema_raw=git('show',ACCEPTED_ROADMAP+':'+SCHEMA);record=json.loads(raw);schema=json.loads(schema_raw)
 require(raw==canonical(record) and schema_raw==canonical(schema),'noncanonical roadmap contract')
 return validate_record(record,schema)
def current_binding(path):
 from test_pe5_implementation_preparation import CANDIDATE_PATHS as PE5_PATHS, current_binding as pe5_binding
 if path in PE5_PATHS:return pe5_binding(path)
 record=successor();require(path in {x['path'] for x in record['artifacts']},'path outside roadmap map')
 item=next(x for x in record['artifacts'] if x['path']==path);raw=current_bytes(path)
 require(digest(raw)==item['sha256'] and blob(raw)==item['git_blob'],'current roadmap bytes mismatch');return item
class SurveillanceRoadmapPreservationTests(unittest.TestCase):
 def test_exact_roadmap_and_bindings(self):successor()
 def test_no_sequence_or_authorization_change(self):
  r=successor();self.assertFalse(r['pe5_start_authorized']);self.assertFalse(r['implementation_authorized']);self.assertEqual(r['current_next_task'],'UNKNOWN_NOT_YET_AUTHORIZED')
 def test_existing_closure_law_preserved(self):
  import ast
  path='tests/test_pe4_documentation_consistency_correction_closure.py'
  old=ast.parse(git('show',PREDECESSOR+':'+path));new=ast.parse(current_bytes(path))
  a=next(x for x in old.body if isinstance(x,ast.FunctionDef) and x.name=='validate_closure');b=next(x for x in new.body if isinstance(x,ast.FunctionDef) and x.name=='_validate_historical_closure')
  self.assertEqual([ast.dump(x,include_attributes=False) for x in a.body],[ast.dump(x,include_attributes=False) for x in b.body])
 def test_existing_history_and_completed_packages_preserved(self):
  for item in successor()['historical_artifacts']:self.assertEqual(current_bytes(item['path']),git('show',PREDECESSOR+':'+item['path']))
 def test_six_checkpoints_and_cross_cutting_architecture(self):
  master=current_bytes(MASTER).decode();self.assertEqual(master.count('##### Surveillance checkpoint '),6)
  for phrase in ['not a second incident taxonomy','same Dashboard v2','aggregation/downsampling','DENY BY DEFAULT','No parallel surveillance engine']:self.assertIn(phrase,master)
 def test_reject_authorization_and_wrong_home(self):
  for key,value in [('implementation_authorized',True),('pe5_start_authorized',True),('architectural_home','NEW_PHASE'),('current_next_task','SURVEILLANCE_IMPLEMENTATION')]:
   bad=copy.deepcopy(successor());bad[key]=value
   with self.assertRaises(ValueError):validate_record(bad,{'$schema':'https://json-schema.org/draft/2020-12/schema','title':'PE-10 surveillance roadmap preservation',**closed(bad)})
 def test_reject_identity_and_scope_changes(self):
  bad=copy.deepcopy(successor());bad['artifacts'][0]['sha256']='0'*64
  with self.assertRaises(ValueError):validate_record(bad,{'$schema':'https://json-schema.org/draft/2020-12/schema','title':'PE-10 surveillance roadmap preservation',**closed(bad)})
  bad=copy.deepcopy(successor());bad['authorized_paths'].append('pi4/unapproved.py')
  with self.assertRaises(ValueError):validate_record(bad,{'$schema':'https://json-schema.org/draft/2020-12/schema','title':'PE-10 surveillance roadmap preservation',**closed(bad)})
 def test_reject_schema_drift(self):
  r=successor();s=json.loads(current_bytes(SCHEMA));s['additionalProperties']=True
  with self.assertRaises(ValueError):validate_record(r,s)
if __name__=='__main__':unittest.main()
