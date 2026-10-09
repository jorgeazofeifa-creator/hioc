"""Current deployment preparation with immutable historical authority."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import unittest
from test_pe4_ha_public_projection_deploy import D,ROOT
P=ROOT/D.RECORD
R=json.loads(P.read_bytes());S=json.loads((ROOT/D.SCHEMA).read_bytes())
def git(*args):return subprocess.check_output(["git",*args],cwd=ROOT)
def normalized(path):return (ROOT/path).read_bytes().replace(b"\r\n",b"\n")
def blob(raw):return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

class DeploymentPreparationTests(unittest.TestCase):
    def test_canonical_closed_record_and_schema(self):
        self.assertEqual(P.read_bytes(),D.canonical(R));self.assertEqual((ROOT/D.SCHEMA).read_bytes(),D.canonical(S))
        D.check_closed(R,S)
        self.assertEqual(S,{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"PE-4 public projection deployment preparation",**D.closed_schema(R)})
    def test_every_leaf_and_nested_object_rejects_drift(self):
        def walk(value,schema):
            if type(value) is dict:
                with self.assertRaises(D.Failure):D.check_closed(dict(value,unreviewed=True),schema)
                for k,v in value.items():walk(v,schema["properties"][k])
            elif type(value) is list:
                with self.assertRaises(D.Failure):D.check_closed(value+[None],schema)
                for v,c in zip(value,schema["prefixItems"]):walk(v,c)
            else:
                with self.assertRaises(D.Failure):D.check_closed({"unreviewed":True},schema)
        walk(R,S)
    def test_starting_commit_parent_and_subject(self):
        self.assertEqual(R["starting_head"],D.PARENT)
        self.assertEqual(git("show","-s","--format=%s",D.PARENT).decode().strip(),"PE-4: close public projection POSIX validation")
        self.assertEqual(git("rev-parse",D.PARENT+"^").decode().strip(),D.IMPLEMENTATION)
        self.assertEqual(R["commit_subject"],D.SUBJECT)
    def test_all_current_artifact_bindings(self):
        self.assertEqual(len(R["artifacts"]),len({a["path"] for a in R["artifacts"]}))
        for item in R["artifacts"]:
            raw=normalized(item["path"]);self.assertEqual(D.sha(raw),item["sha256"]);self.assertEqual(blob(raw),item["git_blob"])
    def test_historical_authority_stays_exact(self):
        for item in R["historical_authority"]:
            raw=git("show",item["commit"]+":"+item["path"])
            self.assertEqual(D.sha(raw),item["sha256"]);self.assertEqual(blob(raw),item["git_blob"])
            if not item["historical_only"]:self.assertEqual(normalized(item["path"]),raw)
    def test_runtime_source_and_private_protection(self):
        for path,digest in (*D.SET,*D.PRIVATE.items()):
            old=git("show",D.IMPLEMENTATION+":"+path)
            self.assertEqual(normalized(path),old);self.assertEqual(D.sha(old),digest)
        self.assertEqual(git("diff","--name-only",D.PARENT,"--","pi4","pi4-tools","release","homeassistant","requirements-pe4.lock"),b"")
    def test_predeployment_baseline_is_required_and_not_claimed_observed(self):
        self.assertTrue(R["PREDEPLOYMENT_BASELINE_VALIDATION_REQUIRED"])
        self.assertEqual(R["predeployment_pi3_baseline_validation"],"NOT_STARTED/REQUIRED_BEFORE_DEPLOYMENT")
        candidate=R["baseline_engine_candidate"]
        self.assertEqual(D.sha(git("show",candidate["commit"]+":"+D.SET[2][0])),D.OLD_ENGINE)
        self.assertFalse(candidate["production_observed"]);self.assertEqual(R["engine_mode_policy"],"PRESERVE_SEPARATELY_REVIEWED_BASELINE")
    def test_exact_set_order_and_ownership_policy(self):
        self.assertEqual(R["DEPLOYMENT_SET"],[p for p,_ in D.SET]);self.assertEqual(R["DEPLOYMENT_ORDER"],R["DEPLOYMENT_SET"])
        self.assertEqual(R["additive_file_mode"],"0644");self.assertEqual(R["owner"],"jazofv1");self.assertEqual(R["group"],"jazofv1")
        self.assertEqual(R["INVENTORY_CRON_EXACT"],D.INVENTORY);self.assertEqual(R["ASSOCIATION_CRON_EXACT"],D.ASSOCIATION);self.assertEqual(R["PLATFORM_CRON_EXACT"],D.PLATFORM)
    def test_no_production_or_network_activity_claims(self):
        self.assertTrue(all(value is False for value in R["codex_activity"].values()))
        for key in ("FORCED_INVENTORY_RUN_ALLOWED","MQTT_DURING_DEPLOYMENT","HA_DURING_DEPLOYMENT","CREDENTIAL_DURING_DEPLOYMENT","ADAPTER_DURING_DEPLOYMENT","NEW_SCHEDULER","SYSTEMD","GENERIC_INSTALLER_ALLOWED"):
            self.assertFalse(R[key])
        self.assertEqual(R["posix_validation_provenance"],"OPERATOR_SUPPLIED");self.assertFalse(R["codex_observed_posix_validation"])
    def test_master_current_stage_and_separate_handoffs(self):
        text=(ROOT/"docs/HIOC_MASTER_PLAN.md").read_text(encoding="utf8")
        current=text.split("## Current Objective",1)[1].split("### Historical",1)[0]
        self.assertTrue(current.lstrip().startswith("**PE-4 Home Assistant Association Public Projection Deployment Preparation**"))
        for phrase in ("PASS/CLOSED","NOT STARTED / PREPARED FOR SEPARATE AUTHORIZATION","Production Execution NOT STARTED","Deployment Preparation commit ONLY","STOP and independent source review","REQUIRED BEFORE DEPLOYMENT","PE-4 NOT COMPLETE"):
            self.assertIn(phrase,current)
    def test_document_freezes_failure_execution_and_proof_limits(self):
        text=normalized(R["document"]).decode()
        for phrase in ("OPERATOR_SUPPLIED","not a claim that production currently matches","EXCLUSIVE NONBLOCKING","UNKNOWN_AFTER_ATTEMPT","NO REPLACE","NOT AUTHORIZED YET","SEPARATE FUTURE ACCEPTANCE GATE","Local files or metadata alone cannot prove MQTT","one-shot","same filesystem"):
            self.assertIn(phrase.replace("NO REPLACE","NOREPLACE"),text)
    def test_all_changes_have_current_bindings_and_no_historical_rewrites(self):
        paths=set(git("diff","--name-only",D.PARENT).decode().splitlines())
        allowed={item["path"] for item in R["artifacts"]}|{D.RECORD,D.SCHEMA}
        self.assertTrue(paths<=allowed)
        for path in paths:
            self.assertTrue(path.startswith(("governance/pe4/pe4-ha-association-public-projection-deployment-preparation","docs/","tools/hioc-pe4-ha-public-projection-","tests/")))

if __name__=="__main__":unittest.main()
