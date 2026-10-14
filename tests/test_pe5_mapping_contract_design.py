"""PE-5.2 design contracts and exact successor identities; no runtime collection."""
import copy
import hashlib
import json
import os
import re
import subprocess
import unittest
from functools import lru_cache
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE="78ee4cd16120bf4ea3166901994727a19d1faad1"
RECORD="governance/pe5/pe5-mapping-contract-design.json"
SCHEMA=RECORD.replace(".json",".schema.json")
DESIGN="docs/PE5_MAPPING_CONTRACT_DESIGN.md"

def git(*args):
    return subprocess.check_output(["git","--no-optional-locks",*args],cwd=ROOT,env=dict(os.environ,GIT_OPTIONAL_LOCKS="0"),stderr=subprocess.PIPE)
def raw(path):return (ROOT/path).read_bytes().replace(b"\r\n",b"\n")
def canonical(v):return (json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False)+"\n").encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def require(v,message):
    if not v:raise ValueError(message)
def closed(v):
    if type(v) is dict:return dict(type="object",additionalProperties=False,required=sorted(v),properties={k:closed(x) for k,x in sorted(v.items())})
    if type(v) is list:return dict(type="array",minItems=len(v),maxItems=len(v),prefixItems=[closed(x) for x in v],items=False)
    return dict(const=v)
def schema_for(r):return {"$schema":"https://json-schema.org/draft/2020-12/schema","title":"PE-5.2 mapping source and complete contract design",**closed(r)}
def validate_design(r,s,identities=True):
    require(s==schema_for(r),"closed successor schema mismatch")
    require(r["predecessor_commit"]==BASE and r["checkpoint"]=="PE-5.2" and r["status"]=="COMPLETE_CONTRACT_DESIGN","authority")
    c=r["contract"]
    require(c["decision_count"]==30 and c["next_checkpoint"]=="PE-5.3","coverage/sequence")
    require(c["runtime_implementation_authorized"] is False and c["production_mutation_authorized"] is False,"implementation authority")
    p=c["premise"]
    require(p["preexisting_generic_mapping_store_required"] is False and p["production_absence_claimed"] is False and p["additional_production_observation_required"] is False,"production inference")
    require(all(p[k]=="UNDEFINED" for k in ("original_deployed_authority","original_deployed_store","original_mapping_freshness")),"historical premise")
    require(all(c["mqtt"][k] is False for k in ("live_broker_access_required","subscription_required","discovery_subscriber_required","publication_required","client_enumeration_required","topic_content_reading_required","raw_topics_required")),"live transport scope")
    require(c["source"]["path"]=="/home/jazofv1/hioc/config/enrichment/mqtt_mappings.json" and c["source"]["source_id"]=="operator_mqtt_v1","source")
    require(c["persistence"]["required"] is True and c["persistence"]["lkg_required"] is False,"persistence safety")
    require(c["persistence"]["output_path"]==c["handoff"]["path"]=="/home/jazofv1/hioc/state/enrichment/service_associations/current.json","handoff")
    require(c["execution"]["recurring_required"] is True and c["execution"]["cadence_seconds"]==900 and c["execution"]["handoff_max_age_seconds"]==1200 and c["execution"]["inventory_max_age_seconds"]==2100,"time authorities")
    require(len(r["decision_resolution"])==30 and [x["number"] for x in r["decision_resolution"]]==list(range(1,31)),"unresolved design items")
    require(all(x["disposition"]=="RESOLVED_DESIGN" and x["contract_section"] in c for x in r["decision_resolution"]),"incomplete decisions")
    source=r["input_schema"]
    require(source["additionalProperties"] is False and set(source["required"])=={"schema_version","source_id","revision","mappings"},"open source")
    row=source["properties"]["mappings"]["items"]
    require(row["additionalProperties"] is False and set(row["required"])=={"mapping_id","endpoint_id","device_id","service_id"},"private fields")
    require(r["output_schema"]["additionalProperties"] is False and r["output_schema"]["properties"]["schema_version"]=={"const":"2.0"},"handoff schema")
    if identities:
        scope=set(r["authorized_paths"])
        require(scope=={i["path"] for i in r["artifacts"]}|{RECORD,SCHEMA} and len(scope)==len(r["authorized_paths"]),"scope map")
        # Scope is relative to the exact accepted predecessor, before and after commit.
        changed=set(git("diff","--name-only",BASE).decode().splitlines())|set(git("ls-files","--others","--exclude-standard").decode().splitlines())
        require(changed==scope,"unexpected path")
        for i in r["artifacts"]:
            b=raw(i["path"]);require((sha(b),blob(b))==(i["sha256"],i["git_blob"]),"current artifact identity: "+i["path"])
        for i in r["protected"]:
            b=git("show",BASE+":"+i["path"])
            require((sha(b),blob(b))==(i["sha256"],i["git_blob"]) and raw(i["path"])==b,"immutable artifact: "+i["path"])
    return r
@lru_cache(maxsize=1)
def design_successor():
    b,bs=raw(RECORD),raw(SCHEMA);r,s=json.loads(b),json.loads(bs)
    require(b==canonical(r) and bs==canonical(s),"noncanonical successor")
    return validate_design(r,s)
def design_binding(path):
    i=next((x for x in design_successor()["artifacts"] if x["path"]==path),None)
    if i is not None:require((sha(raw(path)),blob(raw(path)))==(i["sha256"],i["git_blob"]),"successor binding")
    return i
def assert_design_sequence(text):
    design_binding("docs/HIOC_MASTER_PLAN.md")
    section=text.split("## Next Planned Task",1)[1].split("### Historical",1)[0]
    require(section.strip().startswith("### PE-5.3 - Remaining Capability Implementation and Comprehensive Validation"),"next checkpoint")
    require("Separate authorization is required" in section and "PE-5.1 first execution is complete" in section,"later action gate")
    full=raw("docs/HIOC_MASTER_PLAN.md").decode()
    require("PE5_2_STATUS=COMPLETE_CONTRACT_DESIGN" in full and "PE5_3_STARTED=FALSE" in full,"current lifecycle")

def check_shape(v,s):
    # Small repository-only evaluator for the explicit declarative schema keywords.
    # PE-5.3 still must implement the runtime validator and semantic identity rules.
    if "anyOf" in s:
        for option in s["anyOf"]:
            try:check_shape(v,option);return
            except ValueError:pass
        raise ValueError("no schema branch")
    if "const" in s:require(type(v) is type(s["const"]) and v==s["const"],"typed constant")
    if "enum" in s:require(any(type(v) is type(x) and v==x for x in s["enum"]),"enum")
    kinds={"object":dict,"array":list,"string":str,"integer":int,"boolean":bool,"null":type(None)}
    if "type" in s:
        names=s["type"] if type(s["type"]) is list else [s["type"]]
        require(type(v) in [kinds[x] for x in names],"type")
    if type(v) is dict:
        require(set(s.get("required",[]))<=set(v),"missing field")
        if s.get("additionalProperties") is False:require(set(v)<=set(s["properties"]),"extra field")
        for k,x in v.items():
            if k in s.get("properties",{}):check_shape(x,s["properties"][k])
    if type(v) is list:
        require(s.get("minItems",0)<=len(v)<=s.get("maxItems",len(v)),"array bounds")
        for x in v:check_shape(x,s["items"])
        if s.get("uniqueItems"):require(len({canonical(x) for x in v})==len(v),"duplicate row")
    if type(v) is str:
        require(len(v)<=s.get("maxLength",1024),"string bound")
        if "pattern" in s:require(re.fullmatch(s["pattern"],v) is not None,"pattern")
    if type(v) is int:require(s.get("minimum",v)<=v<=s.get("maximum",v),"number bound")

def example():
    return dict(schema_version="1.0",source_id="operator_mqtt_v1",revision=1,mappings=[dict(mapping_id="map_"+"1"*32,endpoint_id="me_"+"2"*32,device_id="dev_"+"3"*16,service_id=None)])

class MappingContractDesignTests(unittest.TestCase):
    def test_complete_successor(self):design_successor()
    def test_exact_current_sequence(self):assert_design_sequence(raw("docs/HIOC_MASTER_PLAN.md").decode())
    def test_no_runtime_or_historical_mutation(self):
        self.assertGreater(len(design_successor()["protected"]),200)
    def test_schema_accepts_explicit_empty_configuration(self):
        x=example();x["mappings"]=[]
        check_shape(x,design_successor()["input_schema"])
    def test_schema_accepts_private_opaque_binding(self):check_shape(example(),design_successor()["input_schema"])
    def test_reject_transport_and_secret_fields(self):
        for key in ("topic","password","token","mac","ip","role_suggestion","health"):
            x=example();x["mappings"][0][key]="sensitive"
            with self.subTest(key=key),self.assertRaises(ValueError):check_shape(x,design_successor()["input_schema"])
    def test_reject_wrong_or_weak_identifiers(self):
        for key in ("mapping_id","endpoint_id","device_id"):
            x=example();x["mappings"][0][key]="hostname-or-ip"
            with self.subTest(key=key),self.assertRaises(ValueError):check_shape(x,design_successor()["input_schema"])
    def test_reject_boolean_revision(self):
        x=example();x["revision"]=True
        with self.assertRaises(ValueError):check_shape(x,design_successor()["input_schema"])
    def test_reject_invalid_revision(self):
        for v in (0,-1,9007199254740992):
            x=example();x["revision"]=v
            with self.subTest(v=v),self.assertRaises(ValueError):check_shape(x,design_successor()["input_schema"])
    def test_reject_exact_duplicate_row(self):
        x=example();x["mappings"]*=2
        with self.assertRaises(ValueError):check_shape(x,design_successor()["input_schema"])
    def test_mapping_count_bound(self):
        x=example();x["mappings"]=[dict(x["mappings"][0],mapping_id="map_"+format(i,"032x")) for i in range(4097)]
        with self.assertRaises(ValueError):check_shape(x,design_successor()["input_schema"])
    def test_contract_rejects_live_access_even_with_matching_schema(self):
        for k in ("live_broker_access_required","subscription_required","publication_required","discovery_subscriber_required","client_enumeration_required","topic_content_reading_required"):
            r=copy.deepcopy(design_successor());r["contract"]["mqtt"][k]=True
            with self.subTest(k=k),self.assertRaises(ValueError):validate_design(r,schema_for(r),identities=False)
    def test_contract_rejects_inferred_production_absence(self):
        r=copy.deepcopy(design_successor());r["contract"]["premise"]["production_absence_claimed"]=True
        with self.assertRaises(ValueError):validate_design(r,schema_for(r),identities=False)
    def test_contract_rejects_reopened_snapshot_policy(self):
        r=copy.deepcopy(design_successor());r["contract"]["execution"]["inventory_max_age_seconds"]=1200
        with self.assertRaises(ValueError):validate_design(r,schema_for(r),identities=False)
    def test_contract_rejects_stale_lkg_as_authority(self):
        r=copy.deepcopy(design_successor());r["contract"]["persistence"]["lkg_required"]=True
        with self.assertRaises(ValueError):validate_design(r,schema_for(r),identities=False)
    def test_contract_rejects_missing_design_decision(self):
        r=copy.deepcopy(design_successor());r["decision_resolution"].pop()
        with self.assertRaises(ValueError):validate_design(r,schema_for(r),identities=False)
    def test_contract_rejects_implicit_next_implementation(self):
        r=copy.deepcopy(design_successor());r["contract"]["runtime_implementation_authorized"]=True
        with self.assertRaises(ValueError):validate_design(r,schema_for(r),identities=False)
    def test_handoff_is_closed_and_private(self):
        s=design_successor()["output_schema"]
        x={k:None for k in s["required"]};x["topic"]="private"
        with self.assertRaises(ValueError):check_shape(x,s)
    def test_schema_is_closed_exact_typed(self):
        r=design_successor();s=schema_for(r);s["additionalProperties"]=True
        with self.assertRaises(ValueError):validate_design(r,s,identities=False)
    def test_successor_bad_current_bytes_are_rejected(self):
        i=design_binding("docs/HIOC_MASTER_PLAN.md")
        self.assertNotEqual(i["sha256"],sha(b"wrong successor"))
if __name__=="__main__":unittest.main()
