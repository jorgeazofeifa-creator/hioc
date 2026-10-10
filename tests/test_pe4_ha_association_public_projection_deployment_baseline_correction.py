"""Closed correction authority; historical preparation remains immutable."""
import ast
import copy
import hashlib
import json
import subprocess
import unittest
from test_pe4_ha_public_projection_deploy import D,ROOT
R=json.loads((ROOT/D.RECORD).read_bytes())
class CorrectionTests(unittest.TestCase):
    def test_root_cause_and_original_failed_attempt_preserved(self):
        self.assertEqual(R['root_cause'],'PUBLIC_PROJECTION_DEPLOYMENT_PREPARATION_ASSUMED_UNDEPLOYED_COMPATIBILITY_ENGINE_AS_PRODUCTION_BASELINE')
        self.assertTrue(R['assumption_policy_violation']);self.assertEqual(R['root_cause_family'],'UNVERIFIED_PRODUCTION_BASELINE_PROMOTED_FROM_REPOSITORY_SOURCE_STATE')
        attempt=R['baseline_attempt_1'];self.assertEqual(attempt['provenance'],'OPERATOR_SUPPLIED');self.assertTrue(attempt['safe_failure'])
        out=attempt['output'];self.assertEqual(out['RESULT'],'FAIL');self.assertEqual(out['ERROR_CODE'],'BASELINE_MISMATCH');self.assertTrue(out['STOP_REQUIRED'])
        for key in ('ADAPTER_EXECUTED','PRODUCTION_MUTATED','CRONTAB_MUTATED','INVENTORY_LOCK_ACQUIRED','INVENTORY_ENGINE_EXECUTED','PUBLIC_PROJECTION_EXECUTED','MQTT_PUBLISHED','HA_NETWORK_ATTEMPTED','CREDENTIAL_ACCESSED'):self.assertIs(out[key],False)
    def test_original_preparation_family_bytes_unchanged(self):
        for path in ('governance/pe4/pe4-ha-association-public-projection-deployment-preparation.json','governance/pe4/pe4-ha-association-public-projection-deployment-preparation.schema.json','docs/PE4_HOME_ASSISTANT_ASSOCIATION_PUBLIC_PROJECTION_DEPLOYMENT_PREPARATION.md'):
            self.assertEqual((ROOT/path).read_bytes().replace(b'\r\n',b'\n'),subprocess.check_output(['git','show',D.PARENT+':'+path],cwd=ROOT))
    def test_exact_preserved_generation_hashes_match_history_and_are_not_targets(self):
        for path,(digest,mode) in D.PRESERVED.items():
            ref='8187114c7233be82b188f0fc03b93a022787e7bb' if path.endswith('compatibility.py') else D.PE1
            self.assertEqual(D.sha(subprocess.check_output(['git','show',ref+':'+path],cwd=ROOT)),digest)
            fact=R['preserved_runtime'][path];self.assertEqual(fact['sha256'],digest);self.assertEqual(fact['mode'],format(mode,'04o'))
            self.assertEqual(fact['provenance'],'OPERATOR_SUPPLIED');self.assertFalse(fact['deploy_target']);self.assertTrue(fact['reobserve_required'])
            self.assertNotIn(path,[p for p,_ in D.SET])
    def test_backport_hash_and_blob_are_actual_explicit_bytes(self):
        raw=(ROOT/D.PAYLOAD).read_bytes().replace(b'\r\n',b'\n');b=R['backport']
        self.assertEqual(D.sha(raw),b['sha256']);self.assertEqual(b['sha256'],D.SET[2][1]);self.assertEqual(b['path'],D.PAYLOAD)
        self.assertEqual(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),b['git_blob'])
        self.assertFalse(b['generated_during_deployment']);self.assertFalse(b['compatibility_engine_behavior_present'])
    def test_exact_three_target_set_and_source_is_backport(self):
        self.assertEqual(R['DEPLOYMENT_SET'],[p for p,_ in D.SET]);self.assertEqual(R['DEPLOYMENT_ORDER'],R['DEPLOYMENT_SET']);self.assertEqual(len(D.SET),3)
        text=(ROOT/D.TOOL).read_text();self.assertIn('source_path = PAYLOAD if path == SET[2][0] else path',text)
        self.assertNotEqual(D.SET[2][1],dict(D.CANONICAL)[D.SET[2][0]])
    def test_historical_evidence_bindings_not_production_proofs(self):
        self.assertEqual(R['runtime_classification'],D.CLASSIFICATION);self.assertEqual(R['evidence_provenance'],'OPERATOR_SUPPLIED');self.assertFalse(R['source_state_proves_production'])
        for item in R['historical_authority']:
            raw=subprocess.check_output(['git','show',item['commit']+':'+item['path']],cwd=ROOT)
            self.assertEqual(D.sha(raw),item['sha256']);self.assertEqual(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),item['git_blob'])
    def test_historical_governance_exact_explicit_no_upgrade_claims(self):
        doc=subprocess.check_output(['git','show','4912f20d8b2ff78dcdaf8b3e0f52e57d5de5e3a2:docs/PE4_HOME_ASSISTANT_ASSOCIATION_ADAPTER_DEPLOYMENT_PREPARATION.md'],cwd=ROOT).decode()
        self.assertIn('No platform-status upgrade or general compatibility-framework deployment is bundled.',doc)
        self.assertIn('without installing compatibility.py in production',doc)
        self.assertIn(D.PRESERVED['pi4/bin/hioc-platform-status.py'][0],doc)
        self.assertIn('A_NEW_FILE_TO_DEPLOY',doc)
    def test_canonical_and_private_six_files_are_immutable(self):
        self.assertEqual(len(D.CANONICAL),6)
        for path,digest in D.CANONICAL:
            raw=subprocess.check_output(['git','show',D.IMPLEMENTATION+':'+path],cwd=ROOT)
            self.assertEqual(D.sha(raw),digest);self.assertEqual((ROOT/path).read_bytes().replace(b'\r\n',b'\n'),raw)
    def test_lifecycle_no_production_gate_started_and_no_upgrade_authority(self):
        self.assertEqual(R['lifecycle']['corrected_baseline_validation'],'NOT_STARTED/PREPARED_FOR_SEPARATE_AUTHORIZATION')
        self.assertEqual(R['lifecycle']['production_execution'],'NOT_STARTED');self.assertEqual(R['lifecycle']['pe4'],'NOT_COMPLETE');self.assertEqual(R['lifecycle']['pe5'],'NOT_STARTED')
        for k in ('compatibility_runtime_deployment_authorized','platform_status_upgrade_authorized','inventory_module_upgrade_authorized','mqtt_module_upgrade_authorized'):self.assertFalse(R[k])
        self.assertTrue(all(v is False for v in R['codex_activity'].values()))
    def test_all_changed_files_have_closed_current_artifact_binding(self):
        paths=set(subprocess.check_output(['git','diff','--name-only',D.PARENT,'c7db29f795909d7926e36c02f1166034bcebb8b0'],cwd=ROOT).decode().splitlines())
        self.assertEqual(R['commit_subject'],subprocess.check_output(['git','show','-s','--format=%s','c7db29f795909d7926e36c02f1166034bcebb8b0'],cwd=ROOT).decode().strip())
        bindings={i['path']:i for i in R['artifacts']}
        self.assertTrue(paths<=set(bindings)|{D.RECORD,D.SCHEMA})
        for path,item in bindings.items():
            raw=subprocess.check_output(['git','show','c7db29f795909d7926e36c02f1166034bcebb8b0:'+path],cwd=ROOT)
            self.assertEqual(D.sha(raw),item['sha256']);self.assertEqual(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),item['git_blob'])
if __name__=='__main__':unittest.main()
