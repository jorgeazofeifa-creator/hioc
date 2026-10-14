"""Current PE-5 roadmap and immutable historical binding tests; repository only."""
import ast
import copy
import hashlib
import json
import os
import subprocess
import unittest
from functools import lru_cache
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
BASE="edb406b2243b7256c919a08a7162971265df1d08"
RECORD="governance/pe5/pe5-execution-roadmap.json"
SCHEMA=RECORD.replace(".json",".schema.json")
NUMBERS=["PE-5."+str(i) for i in range(2,10)]
NAMES=["Mapping Source Authority and Complete Contract Design","Remaining Capability Implementation and Comprehensive Validation","PI3 Release Source Synchronization","Disabled Production Deployment","Bounded Mapping and Storage Production Validation","Conditional Execution Activation","Operational Evidence and Independent Production Acceptance","Final PE-5 Closure and PE-6 Handoff"]
FIELDS={"number","name","objective","why_required","authoritative_dependency","predecessor","dependencies","inputs","outputs","established_facts","facts_resolved","types","production_access","repository_changes_allowed","production_observation_allowed","production_mutation_allowed","pi3_operator_action_required","codex_pi3_access","pi5_action","mqtt_access","credential_access","persistence_changes","scheduler_changes","inventory_engine_changes","public_inventory_changes","mqtt_publication_changes","tests_required","production_validation_required","evidence_report_required","acceptance_criteria","rollback_recovery","stop_condition","successor","conditional_disposition","authorization"}
REQUIREMENTS=["local service ownership relationships","systemd evidence","ss/listening-socket evidence","stable device binding","stable relationship identifiers","source provenance","rule provenance","configured MQTT mappings","MQTT association evidence","mapping source authority","mapping producer authority","mapping identifier semantics","mapping relationship semantics","mapping freshness","mapping expiry","duplicate handling","conflict handling","missing endpoint handling","privacy","credentials/secrets","topic leakage prevention","no identity authority","no canonical-IP authority","no liveness authority","no health authority","bounded diff","unchanged publish/subscribe behavior","persistence requirement","recurring execution decision","producer/inventory integration decision","retention decision","deployment","bounded production validation","independent acceptance","operational documentation","final PE-5 closure","PE-6 handoff readiness"]
def git(*a):return subprocess.check_output(["git","--no-optional-locks",*a],cwd=ROOT,env=dict(os.environ,GIT_OPTIONAL_LOCKS="0"),stderr=subprocess.PIPE)
def raw(p):return (ROOT/p).read_bytes().replace(b"\r\n",b"\n")
def require(v,m):
    if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def canonical(x):return (json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False)+"\n").encode()
def closed(v):
    if type(v) is dict:return dict(type="object",additionalProperties=False,required=sorted(v),properties={k:closed(x) for k,x in sorted(v.items())})
    if type(v) is list:return dict(type="array",minItems=len(v),maxItems=len(v),prefixItems=[closed(x) for x in v],items=False)
    return dict(const=v)
def schema_for(r):return {"$schema":"https://json-schema.org/draft/2020-12/schema","title":"PE-5 complete execution roadmap",**closed(r)}
@lru_cache(maxsize=None)
def historical_bytes(path):return git("show",BASE+":"+path)
def check_identity(p,b,i):
    require(sha(b)==i["sha256"] and blob(b)==i["git_blob"],"identity mismatch: "+p)
def validate_roadmap(r,s):
    require(s==schema_for(r),"exact roadmap schema mismatch")
    require(type(r["version"]) is int and r["version"]==1,"version")
    require(r["predecessor_commit"]==BASE and r["status"]=="PREPARED_FOR_ACCEPTANCE","roadmap authority")
    require(r["runtime_activity_authorized"] is False,"planning operational authority")
    require(r["current_checkpoint"]=="PE-5.2" and r["final_checkpoint"]=="PE-5.9" and r["final_successor"]=="PE-6","sequence endpoints")
    require([c["number"] for c in r["checkpoints"]]==NUMBERS,"checkpoint order/count")
    require([c["name"] for c in r["checkpoints"]]==NAMES,"checkpoint names")
    for i,c in enumerate(r["checkpoints"]):
        require(set(c)==FIELDS,"incomplete checkpoint contract")
        prev="PE-5.1" if i==0 else NUMBERS[i-1]
        nxt="PE-6" if i==7 else NUMBERS[i+1]
        require(c["predecessor"]==prev and c["dependencies"]==[prev] and c["successor"]==nxt,"dependency/successor/cycle")
        require(c["codex_pi3_access"]=="PROHIBITED" and c["pi5_action"]=="NOT_REQUIRED","remote access")
        require(c["public_inventory_changes"]==c["mqtt_publication_changes"]=="PROHIBITED","public/MQTT boundary")
        require(c["authorization"]=="PLANNED_ONLY_SEPARATE_CHECKPOINT_AUTHORIZATION_REQUIRED","implicit authorization")
        require(c["evidence_report_required"] is True and all(c[k] for k in FIELDS if k!="pi3_operator_action_required"),"missing gate")
    require([x["requirement"] for x in r["coverage"]]==REQUIREMENTS,"requirement coverage")
    for x in r["coverage"]:
        require(x["disposition"] in ["COVERED_BY_COMPLETED_PE5_1","ASSIGNED_TO_PE5_X","DEFERRED_OUTSIDE_PE5_WITH_AUTHORITY","NOT_REQUIRED_WITH_AUTHORITY"],"unassigned requirement")
        require(x["checkpoints"] and set(x["checkpoints"])<=set(NUMBERS+["PE-5.1"]),"coverage target")
    for x in r["unknown_resolution"]:
        require(x["resolved_by"] in NUMBERS,"unknown resolver")
        require(all(NUMBERS.index(n)>NUMBERS.index(x["resolved_by"]) for n in x["blocks"]),"unknown discovered too late")
    require(len(r["definition_of_done"])==14 and len(r["deferred_work"])>=17,"completion/cross-phase boundary")
    require(r["accepted_pe5_1"]==dict(source_commit="ed3a80508d101652bac89e1dcc111167670aaebc",policy_seconds=2100,execution_count=1,return_code=0,association_count=8,rejection_count=0,inventory_unchanged=True,public_inventory_unchanged=True,persistent_state_created=False),"accepted foundation changed")
    a=r["audit"]
    tracked=git("ls-tree","-r","--name-only",BASE).decode().splitlines()
    require(a["baseline"]==BASE and a["tracked_files_searched"]==len(tracked)==428 and not a["exclusions"],"audit coverage")
    require(len({x["path"] for x in a["references"]})==len(a["references"]),"duplicate audit groups")
    require(all(x["path"] in tracked and x["classification"] in ["CURRENT","HISTORICAL_INTENTIONALLY_PRESERVED","STALE_REQUIRES_UPDATE","UNRELATED_REFERENCE"] for x in a["references"]),"audit classification")
    require(a["known_static_contradictions_remaining"]==a["unexplained_pe5_references"]==0,"known unexplained contradiction")
    require(all(x.get("disposition") for x in a["contradictions"]),"unresolved contradiction")
    scope=set(r["authorized_paths"])
    require(len(scope)==len(r["authorized_paths"]) and scope=={i["path"] for i in r["artifacts"]}|{RECORD,SCHEMA},"scope/map")
    actual=set(git("diff","--name-only",BASE).decode().splitlines())|set(git("ls-files","--others","--exclude-standard").decode().splitlines())
    require(actual==scope,"unexpected mutation paths")
    for i in r["artifacts"]:check_identity(i["path"],raw(i["path"]),i)
    for key in ["protected_runtime","historical_governance"]:
        for i in r[key]:
            historical=historical_bytes(i["path"]);check_identity(i["path"],historical,i)
            require(raw(i["path"])==historical,"historical/runtime artifact changed")
    assert_roadmap_sequence(raw("docs/HIOC_MASTER_PLAN.md").decode(),binding=False)
    # Original policy validator body survives exactly under historical name.
    old=ast.parse(git("show","ed3a80508d101652bac89e1dcc111167670aaebc:tests/test_pe5_snapshot_age_policy.py"))
    new=ast.parse(raw("tests/test_pe5_snapshot_age_policy.py"))
    fn=lambda t,n:next(x for x in t.body if isinstance(x,ast.FunctionDef) and x.name==n)
    require(ast.dump(ast.Module(body=fn(old,"validate_policy_record").body,type_ignores=[]))==ast.dump(ast.Module(body=fn(new,"_validate_historical_policy").body,type_ignores=[])),"historical validator weakened")
    return r
ROADMAP_SUBJECT = "PE-5: define complete execution roadmap"

@lru_cache(maxsize=1)
def accepted_roadmap_commit():
    # Resolve the immutable accepted child, never reinterpret a later HEAD as this plan.
    commits=git("rev-list","--ancestry-path",BASE+"..HEAD").decode().splitlines()
    matches=[c for c in commits
             if git("show","-s","--format=%P",c).decode().strip()==BASE
             and git("show","-s","--format=%s",c).decode().strip()==ROADMAP_SUBJECT]
    require(len(matches)<=1,"ambiguous accepted roadmap object")
    return matches[0] if matches else None

@lru_cache(maxsize=1)
def roadmap_successor():
    accepted=accepted_roadmap_commit()
    if accepted is None:
        require(git("rev-parse","HEAD").decode().strip()==BASE,"roadmap candidate ancestry")
        b,bs=raw(RECORD),raw(SCHEMA);r,s=json.loads(b),json.loads(bs)
        require(b==canonical(r) and bs==canonical(s),"noncanonical roadmap")
        return validate_roadmap(r,s)
    original_git=git
    @lru_cache(maxsize=None)
    def accepted_bytes(path):return original_git("show",accepted+":"+path)
    def accepted_git(*args):
        if args==("diff","--name-only",BASE):
            return original_git("diff","--name-only",BASE,accepted)
        if args==("ls-files","--others","--exclude-standard"):return b""
        return original_git(*args)
    b,bs=accepted_bytes(RECORD),accepted_bytes(SCHEMA);r,s=json.loads(b),json.loads(bs)
    require(b==canonical(r) and bs==canonical(s),"noncanonical accepted roadmap")
    # The accepted planning record/schema themselves are immutable in later checkouts.
    require(raw(RECORD)==b and raw(SCHEMA)==bs,"historical roadmap package changed")
    with patch.dict(globals(),raw=accepted_bytes,git=accepted_git):
        return validate_roadmap(r,s)
def roadmap_binding(path):
    r=roadmap_successor();i=next((x for x in r["artifacts"] if x["path"]==path),None)
    if i is not None:check_identity(path,raw(path),i)
    return i
def assert_roadmap_sequence(text,binding=True):
    if binding:roadmap_binding("docs/HIOC_MASTER_PLAN.md")
    section=text.split("## Next Planned Task",1)[1].split("### Historical",1)[0]
    require(section.strip().startswith("### PE-5.2 - "+NAMES[0]),"current next checkpoint")
    require("Separate authorization is required" in section and "PE-5.1 first execution is complete" in section,"current stop boundary")
    # Existing current-sequence consumers may pass only the current-status section.
    # The complete checkpoint structure is validated from the exact bound document.
    full=raw("docs/HIOC_MASTER_PLAN.md").decode()
    roadmap=full.split("<!-- PE5_EXECUTION_ROADMAP_BEGIN -->",1)[1].split("<!-- PE5_EXECUTION_ROADMAP_END -->",1)[0]
    for n,name in zip(NUMBERS,NAMES):require("#### "+n+" - "+name in roadmap,"missing checkpoint")
    require("TOTAL_REMAINING_PE5_CHECKPOINTS=8" in roadmap and "PE5_FINAL_SUCCESSOR=PE-6" in roadmap,"phase endpoints")
    require("### PE-5 Definition of Done" in roadmap and "### UNKNOWN resolution matrix" in roadmap and "### Efficiency review" in roadmap,"roadmap gates")
class ExecutionRoadmapTests(unittest.TestCase):
    def test_current_exact_roadmap(self):roadmap_successor()
    def test_current_sequence(self):assert_roadmap_sequence(raw("docs/HIOC_MASTER_PLAN.md").decode())
    def test_existing_current_section_interface(self):
        master=raw("docs/HIOC_MASTER_PLAN.md").decode()
        current=master.split("# Implementation Status",1)[1].split("# Historical Operator Preparation Chronology",1)[0]
        assert_roadmap_sequence(current)
    def test_current_document_source_bindings_keep_historical_authority(self):
        from test_pe4_ha_association_public_projection_test_binding_correction import verify_source_binding
        for path in ['governance/pe4/pe4-ha-association-public-projection-implementation.json',
                     'governance/pe4/pe4-ha-association-public-projection-posix-source-validation-closure.json']:
            record=json.loads(raw(path))
            commit=record.get('starting_commit',record.get('closure_predecessor'))
            for item in record['sources']:
                with self.subTest(record=path,source=item['path']):
                    historical=git('show',commit+':'+item['path'])
                    verify_source_binding(item,historical,path,commit)
                    if not item['historical_only'] and roadmap_binding(item['path']) is not None:
                        with self.assertRaises(ValueError):
                            verify_source_binding(item,historical,path,commit,current_raw=b'wrong current bytes')
    def test_current_documentation_entry_points_follow_exact_successor(self):
        from test_pe4_documentation_consistency_correction import current_artifacts, current_binding
        from test_pe4_documentation_consistency_correction_closure import current_bytes
        from test_pe4_ha_association_public_projection_test_binding_correction import current_index
        mapping={i['path']:i for i in current_artifacts()}
        for item in roadmap_successor()['artifacts']:
            with self.subTest(path=item['path']):
                self.assertEqual(mapping[item['path']],item)
                self.assertEqual(current_binding(item['path']),item)
                self.assertEqual(current_bytes(item['path']),raw(item['path']))
                self.assertEqual(current_index(item['path']),raw(item['path']))
        for path,name in [('tests/test_pe4_documentation_consistency_correction.py','_validate_historical_candidate'),
                          ('tests/test_pe4_documentation_consistency_correction_closure.py','_validate_historical_closure')]:
            old=ast.parse(historical_bytes(path));new=ast.parse(raw(path))
            function=lambda tree:next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name==name)
            self.assertEqual(ast.dump(function(old)),ast.dump(function(new)))
    def test_reject_cycle_or_missing_successor(self):
        for field,value in [("successor","PE-5.2"),("dependencies",["PE-5.9"]),("predecessor","PE-6")]:
            r=copy.deepcopy(roadmap_successor());r["checkpoints"][0][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):validate_roadmap(r,schema_for(r))
    def test_reject_unknown_resolved_late(self):
        r=copy.deepcopy(roadmap_successor());r["unknown_resolution"][0]["resolved_by"]="PE-5.9"
        with self.assertRaises(ValueError):validate_roadmap(r,schema_for(r))
    def test_reject_missing_requirement(self):
        r=copy.deepcopy(roadmap_successor());r["coverage"].pop()
        with self.assertRaises(ValueError):validate_roadmap(r,schema_for(r))
    def test_reject_operation_authority(self):
        r=copy.deepcopy(roadmap_successor());r["runtime_activity_authorized"]=True
        with self.assertRaises(ValueError):validate_roadmap(r,schema_for(r))
    def test_reject_public_or_remote_authority(self):
        for field in ["public_inventory_changes","mqtt_publication_changes","codex_pi3_access"]:
            r=copy.deepcopy(roadmap_successor());r["checkpoints"][0][field]="ALLOWED"
            with self.subTest(field=field),self.assertRaises(ValueError):validate_roadmap(r,schema_for(r))
    def test_reject_stale_identity_or_open_schema(self):
        r=copy.deepcopy(roadmap_successor());r["artifacts"][0]["sha256"]="0"*64
        with self.assertRaises(ValueError):validate_roadmap(r,schema_for(r))
        s=schema_for(roadmap_successor());s["additionalProperties"]=True
        with self.assertRaises(ValueError):validate_roadmap(roadmap_successor(),s)
    def test_historical_policy_still_exact(self):
        from test_pe5_snapshot_age_policy import policy_successor
        self.assertEqual(policy_successor()["max_snapshot_age_seconds"],2100)
    def test_local_runtime_is_not_roadmap_exception(self):
        self.assertIsNone(roadmap_binding("pi4/lib/hioc/service_association.py"))
if __name__=="__main__":unittest.main()
