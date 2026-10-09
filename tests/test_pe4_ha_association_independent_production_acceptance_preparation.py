"""Repository-only preparation checks: never inspect production."""
import copy,hashlib,json,subprocess,unittest
from pathlib import Path
from test_pe4_ha_association_deployment_closure import validate,canonical
ROOT=Path(__file__).resolve().parents[1]
BASE='369134ff77d062ba0aeebc3db98e04662f2f6fed'
P=ROOT/'governance/pe4/pe4-ha-association-independent-production-acceptance-preparation.json'
R=json.loads(P.read_bytes());S=json.loads(P.with_suffix('.schema.json').read_bytes())
class PreparationTests(unittest.TestCase):
 def reject(self,path,value):
  bad=copy.deepcopy(R);node=bad
  for key in path[:-1]:node=node[key]
  node[path[-1]]=value
  with self.assertRaises(ValueError):validate(bad,S)
 def test_canonical_closed_pair(self):
  validate(R,S);self.assertEqual(P.read_bytes(),canonical(R));self.assertEqual(P.with_suffix('.schema.json').read_bytes(),canonical(S))
 def test_all_nested_objects_closed(self):
  def visit(v,s):
   if isinstance(v,dict):
    bad=dict(v,unexpected=True)
    with self.assertRaises(ValueError):validate(bad,s)
    for k in v:visit(v[k],s['properties'][k])
   elif isinstance(v,list):
    for x,y in zip(v,s['prefixItems']):visit(x,y)
  visit(R,S)
 def test_missing_top_properties(self):
  for k in R:
   bad=copy.deepcopy(R);del bad[k]
   with self.assertRaises(ValueError):validate(bad,S)
 def test_predecessor_authority(self):
  self.assertEqual(R['starting_commit'],BASE)
  for args,value in [(('rev-parse',BASE+'^'),R['parent']),(('show','-s','--format=%s',BASE),R['subject'])]:self.assertEqual(subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip(),value)
 def test_existing_definitions_sufficient_no_new_main(self):
  a=R['architecture'];self.assertTrue(a['existing_tools_sufficient']);self.assertFalse(a['new_tool_required']);self.assertIsNone(a['new_tool']);self.assertTrue(a['cli_mains_prohibited'])
 def test_sync_provenance_and_exact_authority(self):
  e=R['source_synchronization_evidence'];self.assertEqual(e['provenance'],'OPERATOR_SUPPLIED_PRODUCTION_EVIDENCE');self.assertFalse(e['codex_observed']);fields=dict(x.split('=',1) for x in e['exact_report_text'].splitlines() if x);self.assertEqual(fields,e['report']);self.assertEqual(fields['HEAD_AFTER'],BASE);self.assertEqual(fields['SOURCE_SYNCHRONIZATION_RETURN_CODE'],'0');self.reject(['source_synchronization_evidence','codex_observed'],True)
 def test_snapshot_not_permanent_constant(self):
  self.assertIn('NOT_PERMANENT_ARCHITECTURAL_CONSTANTS',R['checkpoint_snapshot']['scope']);self.assertFalse(R['checkpoint_snapshot']['fresh_ha_probe'])
 def test_durable_capture_outside_production(self):
  e=R['evidence'];self.assertIn('AppData',e['location']);self.assertNotIn('/tmp',e['location']);self.assertEqual(e['files'],['validation.json','manifest.json']);self.assertEqual(e['max_report_bytes'],4096);self.assertIn('MANIFEST_LAST',e['publication']);self.assertIn('NO_AUTOMATIC_DELETION',e['retention'])
 def test_report_privacy_closed_allowlist(self):
  e=R['evidence'];s=e['report_schema'];self.assertEqual(set(e['allowed_fields']),set(s['properties']));self.assertFalse(s['additionalProperties']);self.assertEqual(set(s['required']),set(s['properties']))
  for private in ['token','device_id','entity_id','mac','raw_state','credential','household_name']:self.assertNotIn(private,s['properties'])
 def test_master_prepared_not_executed(self):
  text=(ROOT/'docs/HIOC_MASTER_PLAN.md').read_text(encoding='utf8');self.assertIn('Independent Production Acceptance Preparation | PASS/CLOSED',text);self.assertIn('Acceptance execution: **NOT STARTED / PREPARED FOR SEPARATE AUTHORIZATION**',text)
 def test_source_implementation_unchanged(self):
  for p in subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'pi4','pi4-tools','tools','governance'],cwd=ROOT,text=True).splitlines():
   before=subprocess.check_output(['git','show',BASE+':'+p],cwd=ROOT);current=(ROOT/p).read_bytes().replace(b'\r\n',b'\n')
   if p=='pi4/bin/hioc-inventory-engine.py':
    implementation=json.loads((ROOT/'governance/pe4/pe4-ha-association-public-projection-implementation.json').read_bytes())
    self.assertEqual(before,subprocess.check_output(['git','show',implementation['starting_commit']+':'+p],cwd=ROOT))
    bound=next(i for i in implementation['implementation_artifacts'] if i['path']==p)
    self.assertEqual(hashlib.sha256(current).hexdigest(),bound['sha256'])
   else:self.assertEqual(before,current)
 def test_document_boundary(self):
  text=(ROOT/'docs/PE4_HOME_ASSISTANT_ASSOCIATION_INDEPENDENT_PRODUCTION_ACCEPTANCE_PREPARATION.md').read_text(encoding='utf8')
  for phrase in ['No HA network','UNAVAILABLE','RECORDED','UNKNOWN','No new tool','manifest LAST','STOP','historical snapshot']:self.assertIn(phrase,text)
for path,item in R['sources'].items():
 def check(self,path=path,item=item):
  raw=subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT);self.assertEqual(hashlib.sha256(raw).hexdigest(),item['sha256']);self.assertEqual(subprocess.check_output(['git','rev-parse',BASE+':'+path],cwd=ROOT,text=True).strip(),item['git_blob']);self.reject(['sources',path,'sha256'],'0'*64)
 setattr(PreparationTests,'test_bound_'+path.replace('/','_').replace('.','_').replace('-','_'),check)
for k,v in R['negative_evidence_by_codex'].items():
 def check(self,k=k):self.assertIs(R['negative_evidence_by_codex'][k],False);self.reject(['negative_evidence_by_codex',k],True)
 setattr(PreparationTests,'test_codex_no_'+k,check)
for k,v in R['lifecycle'].items():
 def check(self,k=k,v=v):self.assertEqual(R['lifecycle'][k],v);self.reject(['lifecycle',k],'UNAUTHORIZED')
 setattr(PreparationTests,'test_lifecycle_'+k,check)
for k,v in R['historical'].items():
 def check(self,k=k,v=v):self.assertEqual(R['historical'][k],v);self.reject(['historical',k],'RECREATED')
 setattr(PreparationTests,'test_historical_'+k,check)
if __name__=='__main__':unittest.main()
