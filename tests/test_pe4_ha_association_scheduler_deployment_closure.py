"""Sanitized repository-only closure tests; no production access or installer execution."""
import copy,hashlib,json,subprocess,unittest
from datetime import datetime,timedelta,timezone
from pathlib import Path
from test_pe4_ha_association_deployment_closure import validate,canonical
ROOT=Path(__file__).resolve().parents[1]
BASE='8579bb9707a1b8fd9b525b66a5156f5e96bc2429'
P=ROOT/'governance/pe4/pe4-ha-association-scheduler-deployment-closure.json'
R=json.loads(P.read_bytes());S=json.loads(P.with_suffix('.schema.json').read_bytes())
class SchedulerClosureTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.blobs={i['path']:subprocess.check_output(['git','show',BASE+':'+i['path']],cwd=ROOT) for i in R['sources']}
 def test_predecessor_exact_git_authority(self):
  self.assertEqual(R['closure_predecessor'],BASE);self.assertEqual(subprocess.check_output(['git','show','-s','--format=%s',BASE],cwd=ROOT).decode().strip(),R['predecessor_subject']);self.assertEqual(subprocess.check_output(['git','rev-parse',BASE+'^'],cwd=ROOT).decode().strip(),R['predecessor_parent'])
 def test_canonical_json_closed_schema(self):validate(R,S);self.assertEqual(P.read_bytes(),canonical(R));self.assertEqual(P.with_suffix('.schema.json').read_bytes(),canonical(S))
 def test_every_schema_leaf_closed_and_extras_rejected(self):
  def visit(v,s):
   if type(v) is dict:
    bad=copy.deepcopy(v);bad['unreviewed_private_content']=True
    with self.assertRaises(ValueError):validate(bad,s)
    for k,x in v.items():visit(x,s['properties'][k])
   elif type(v) is list:
    with self.assertRaises(ValueError):validate(v+[None],s)
    for x,n in zip(v,s['prefixItems']):visit(x,n)
   else:
    with self.assertRaises(ValueError):validate(None,s)
  visit(R,S)
 def test_all_source_git_identities_and_immutable_current_bytes(self):
  self.assertEqual(len(R['sources']),69)
  for i in R['sources']:
   raw=self.blobs[i['path']];self.assertEqual(i['commit'],BASE);self.assertEqual(hashlib.sha256(raw).hexdigest(),i['sha256']);self.assertEqual(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),i['git_blob'])
   if not i['historical_only']:self.assertEqual((ROOT/i['path']).read_bytes().replace(b'\r\n',b'\n'),raw)
 def test_preparation_frozen_model_and_canonical_cron_exact(self):
  prep=json.loads(self.blobs['governance/pe4/pe4-ha-association-scheduler-deployment-preparation.json']);self.assertEqual(prep['status'],'PASS_CLOSED');self.assertEqual(R['frozen_scheduler'],prep['frozen_scheduler']);self.assertEqual(R['canonical_cron'],prep['canonical_cron']);self.assertEqual(R['prerequisites']['scheduler_preparation'],'PASS_CLOSED')
 def test_installer_sha_matches_frozen_preparation(self):
  prep=json.loads(self.blobs['governance/pe4/pe4-ha-association-scheduler-deployment-preparation.json']);self.assertEqual(hashlib.sha256(self.blobs['tools/hioc-pe4-ha-association-scheduler-deploy.py']).hexdigest(),prep['deployment_tool']['sha256'])
 def test_canonical_marker_line_and_platform(self):
  self.assertEqual(R['canonical_cron']['marker'],'# HIOC_PE4_HA_ASSOCIATION');self.assertEqual(R['canonical_cron']['line'],'5,35 * * * * /home/jazofv1/hioc/runtime/pe4/active/bin/python -I -B /home/jazofv1/hioc/pi4/bin/hioc-home-assistant-association.py >/dev/null 2>&1');self.assertEqual(R['canonical_cron']['platform_line'],'17 3 * * * flock -n /tmp/hioc-platform-status.lock /home/jazofv1/hioc/pi4/bin/hioc-platform-status.py')
 def test_six_supplied_preinstall_hashes_match_git(self):
  expected={'docs/HIOC_MASTER_PLAN.md':'2ec69045f31869c0c699fa658953fd8588b6e501b48d1d1a8880e133e59e724b','docs/PE4_HOME_ASSISTANT_ASSOCIATION_SCHEDULER_DEPLOYMENT_PREPARATION.md':'ea760b1f8a1ee9673b29022b10eeaa0d5f606b543bc5378097b45ec2c277ac5b','governance/pe4/pe4-ha-association-scheduler-deployment-preparation.json':'2270bf964800506c73794608952d1ff6d8defa20d1a3cf01d4d23df8b0f7e624','governance/pe4/pe4-ha-association-scheduler-deployment-preparation.schema.json':'05ae7a0b3ac1c9045c2420f6bb5ca19a6fa497d7900fd48e2fc5af20c9cac2b9','tests/test_pe4_ha_association_scheduler_deployment_preparation.py':'be6df0fb6033af1d667a93e63d1dd3a8e300248239d6c3f1b3028f3ffa7e642d','tools/hioc-pe4-ha-association-scheduler-deploy.py':'a89833ee9bf9535eeab0f8567a9272e8460f473c54e05319fd887440cfb94956'}
  for p,h in expected.items():self.assertEqual(hashlib.sha256(self.blobs[p]).hexdigest(),h)
 def test_source_sync_exact_nine_file_chain(self):
  a=R['source_synchronization'];raw=subprocess.check_output(['git','diff-tree','--no-commit-id','--name-status','-r',BASE],cwd=ROOT);self.assertEqual(len(raw.splitlines()),9);self.assertEqual(hashlib.sha256(raw).hexdigest(),a['changeset_sha256']);self.assertEqual((a['head_before'],a['head_after']),('826608b40d5248c67742a17fc95a6e7612981df1',BASE));self.assertTrue(all(x is False for x in a['actions'].values()))
 def test_pre_post_review_provenance_and_scoped_flags(self):
  for key in ['preinstall_review','postinstall_review']:
   a=R[key];self.assertTrue(a['provenance'].startswith('OPERATOR_SUPPLIED'));self.assertEqual((a['head'],a['origin_main']),(BASE,BASE));self.assertEqual((a['ahead'],a['behind']),(0,0));self.assertFalse(a['active_git_operation']);self.assertTrue(all(x is False for x in a['activity'].values()))
 def test_installed_postreview_hash_equality(self):
  i=R['installation']['sanitized_result'];a=R['postinstall_review'];self.assertEqual(i['CANDIDATE_CRONTAB_SHA256'],a['current_crontab_sha256']);self.assertEqual(a['current_crontab_sha256'],a['expected_crontab_sha256'])
 def test_utc_local_exact_valid_natural_slot(self):
  a=R['first_natural_scheduled_publication'];utc=datetime.fromisoformat(a['state_updated_at'].replace('Z','+00:00'));local=utc.astimezone(timezone(timedelta(hours=-6)));self.assertEqual(local.isoformat(),a['local_state_updated_at']);self.assertEqual(local.strftime('%Y-%m-%d %H:%M'),'2026-10-07 20:35');self.assertIn(local.minute,(5,35));self.assertEqual(local.second,3)
 def test_review_flags_not_propagated_to_scheduled_cycle(self):
  a=R['first_natural_scheduled_publication'];self.assertTrue(all(v is False for k,v in a['review_activity'].items() if k!='stop_required'));self.assertNotIn('activity',a);self.assertIn('NOT_DIRECTLY_OBSERVED_NO_FALSE_REVIEW_FLAGS_PROPAGATED',a['scheduled_cycle_individual_activity']);self.assertNotIn('RESULT',a);self.assertFalse(a['process_result_reconstructed'])
 def test_immutable_attempt_one_and_original_evidence_gaps(self):
  old=json.loads(self.blobs['governance/pe4/pe4-ha-association-independent-production-acceptance-closure.json']);h=R['historical_acceptance']
  for k,v in h['attempt_1'].items():self.assertEqual(v,old['attempt_1'][k])
  self.assertEqual(h['original_ephemeral_evidence_limitation'],old['original_ephemeral_evidence_limitation']);self.assertEqual(h['attempt_1']['capture_result'],'FAIL');self.assertEqual(h['attempt_1']['inspection_semantic_result'],'PASS');self.assertFalse(h['attempt_1']['raw_stdout_durably_available']);self.assertFalse(h['attempt_1']['validation_json_published']);self.assertFalse(h['attempt_1']['manifest_json_published']);self.assertFalse(h['attempt_1']['evidence_recreated'])
 def test_only_sanitized_metadata_no_private_payload_keys(self):
  forbidden={'device_id','entity_id','registry_id','config_entry_id','area_name','mac','ip_address','token','credential_hash','raw_inventory','raw_state','raw_crontab','raw_stdout','raw_stderr'}
  def walk(v):
   if isinstance(v,dict):
    self.assertFalse(forbidden.intersection(v));[walk(x) for x in v.values()]
   elif isinstance(v,list):[walk(x) for x in v]
  walk(R);self.assertTrue(all(x is False for x in R['negative_evidence_by_codex'].values()));self.assertIn('OPERATOR_SUPPLIED_ONLY',R['production_evidence_provenance'])
 def test_schema_rejects_status_broadening_and_fabricated_result(self):
  for path,value in [(('lifecycle','pe4'),'COMPLETE'),(('lifecycle','public_projection'),'ACTIVE'),(('lifecycle','manual_second_adapter_execution'),'AUTHORIZED'),(('first_natural_scheduled_publication','adapter_result_text'),'PASS'),(('first_natural_scheduled_publication','adapter_return_code'),0), (('installation','sanitized_result','INSTALL_ATTEMPTS'),2)]:
   bad=copy.deepcopy(R);current=bad
   for k in path[:-1]:current=current[k]
   current[path[-1]]=value
   with self.assertRaises(ValueError):validate(bad,S)
 def test_master_current_closure_lifecycle_and_handoff(self):
  text=(ROOT/'docs/HIOC_MASTER_PLAN.md').read_text(encoding='utf8');table=text.split('Authoritative Current PE-4 Lifecycle',1)[1].split('### Completed',1)[0]
  for name,state in [('PE-4 Home Assistant Association Adapter Scheduler Deployment','PASS/CLOSED'),('Recurring Scheduler Operation','ACTIVE / AUTHORIZED'),('First Natural Scheduled Invocation','OBSERVED'),('First Natural Scheduled State Publication','PASS'),('Manual Second Adapter Execution','NOT AUTHORIZED / NOT PERFORMED'),('PE-4','NOT COMPLETE')]:self.assertIn('| '+name+' | '+state+' |',table)
  for marker in ['## Current Objective','## Next Planned Task']:self.assertIn('PI3 source synchronization to the scheduler deployment closure',text.split(marker,1)[1])
 def test_roadmap_projection_and_pe5_remain_deferred(self):
  self.assertIn('DEFERRED to **PE-4 Home Assistant Association Public Projection**',self.blobs['docs/HIOC_MASTER_PLAN.md'].decode());self.assertIn('NOT_COMPLETE',R['lifecycle']['pe4']);self.assertIn('PUBLIC_PROJECTION_CHECKPOINT_REMAINS',R['roadmap_basis']);self.assertEqual(R['lifecycle']['pe5'],'NOT_STARTED')
 def test_document_explicit_observation_limit_and_sync_scope(self):
  text=(ROOT/'docs/PE4_HOME_ASSISTANT_ASSOCIATION_SCHEDULER_DEPLOYMENT_CLOSURE.md').read_text(encoding='utf8');self.assertIn('NOT_OBSERVED_BY_DESIGN',text);self.assertIn('not an observed adapter RESULT PASS or rc0',text);self.assertIn('not execution by sync',text);self.assertIn('Do not run',text);self.assertIn('OPERATOR_SUPPLIED',text)

CHECKS={
'install_attempts':(('installation','sanitized_result','INSTALL_ATTEMPTS'),1),
'install_result':(('installation','sanitized_result','RESULT'),'PASS'),
'mutation_state':(('installation','sanitized_result','MUTATION_STATE'),'VERIFIED_INSTALLED'),
'prior_crontab_hash':(('installation','sanitized_result','PRIOR_CRONTAB_SHA256'),'1d71cbc5d02935f0298b3765e8576b8dceecbf6ab26965db1a1215f77753b260'),
'installed_hash':(('installation','sanitized_result','CANDIDATE_CRONTAB_SHA256'),'8f900f4679aa861b02e781a61927683db5900ddfe159d78c3831a1595ae7fe71'),
'post_marker_count':(('postinstall_review','marker_count'),1),
'post_job_count':(('postinstall_review','association_job_count'),1),
'post_platform_count':(('postinstall_review','platform_cron_count'),1),
'first_timestamp':(('first_natural_scheduled_publication','state_updated_at'),'2026-10-08T02:35:03.814281Z'),
'state_schema':(('first_natural_scheduled_publication','state_schema_validation'),'PASS'),
'ha_version':(('first_natural_scheduled_publication','observed_ha_version'),'2026.9.4'),
'associated':(('first_natural_scheduled_publication','counts','associated'),25),
'review_only':(('first_natural_scheduled_publication','counts','review_only'),170),
'rejected':(('first_natural_scheduled_publication','counts','rejected'),26),
'unmatched':(('first_natural_scheduled_publication','counts','unmatched'),8),
'history_count':(('first_natural_scheduled_publication','counts','historical_binding'),0),
'state_mode':(('first_natural_scheduled_publication','state_mode'),'0600'),
'state_links':(('first_natural_scheduled_publication','state_link_count'),1),
'transactions_count':(('first_natural_scheduled_publication','transaction_namespace_count'),0),
'transactions_clean':(('first_natural_scheduled_publication','transaction_namespace_clean'),True),
'stdout_limit':(('first_natural_scheduled_publication','adapter_result_text'),'NOT_OBSERVED_BY_DESIGN'),
'rc_limit':(('first_natural_scheduled_publication','adapter_return_code'),'NOT_OBSERVED_BY_DESIGN'),
'manual_unauthorized':(('lifecycle','manual_second_adapter_execution'),'NOT_AUTHORIZED_NOT_PERFORMED'),
'recurring_authorized':(('lifecycle','scheduler_recurring_operation'),'ACTIVE_AUTHORIZED_BY_CLOSED_SCHEDULER_CONTRACT'),
'projection_deferred':(('lifecycle','public_projection'),'DEFERRED'),
'rollback_absent':(('lifecycle','rollback'),'NOT_PERFORMED'),
'phase_active':(('lifecycle','phase7a'),'ACTIVE'),
'acceptance_closed':(('lifecycle','independent_production_acceptance'),'PASS_CLOSED'),
'scheduler_closed':(('lifecycle','scheduler_deployment'),'PASS_CLOSED'),
'first_invocation':(('first_natural_scheduled_publication','invocation'),'OBSERVED'),
'publication_pass':(('first_natural_scheduled_publication','state_publication'),'PASS'),
'no_result_recreation':(('first_natural_scheduled_publication','process_result_reconstructed'),False)}
for name,(path,expected) in CHECKS.items():
 def test(self,path=path,expected=expected):
  value=R
  for key in path:value=value[key]
  self.assertEqual(value,expected);self.assertIs(type(value),type(expected))
 setattr(SchedulerClosureTests,'test_exact_'+name,test)
if __name__=='__main__':unittest.main()
