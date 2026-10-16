"""PE-6 declarative design, immutable predecessors and current-binding tests. No runtime classifier."""
import ast,copy,hashlib,json,os,subprocess
from functools import lru_cache
from pathlib import Path
from unittest.mock import patch
import unittest
ROOT=Path(__file__).resolve().parents[1]
BASE="d6f9d3c6bd07b16fc515ae531b6aa0a3e9188221"
RECORD="governance/pe6/pe6-classification-contract-design.json"
SCHEMA=RECORD.replace(".json",".schema.json")
DOCUMENT="docs/PE6_CLASSIFICATION_CONTRACT_DESIGN.md"
PE5_RECORD="governance/pe5/pe5-configured-association-implementation.json"
PE5_SCHEMA=PE5_RECORD.replace(".json",".schema.json")
def git(*a):return subprocess.check_output(["git","--no-optional-locks",*a],cwd=ROOT,env=dict(os.environ,GIT_OPTIONAL_LOCKS="0"),stderr=subprocess.PIPE)
def raw(p):return (ROOT/p).read_bytes().replace(b"\r\n",b"\n")
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def canonical(v):return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True).encode()+b"\n"
def require(value,reason):
    if not value:raise ValueError(reason)
def closed(v):
    if type(v)is dict:return dict(type="object",additionalProperties=False,required=sorted(v),properties={k:closed(x) for k,x in sorted(v.items())})
    if type(v)is list:return dict(type="array",minItems=len(v),maxItems=len(v),prefixItems=[closed(x) for x in v],items=False)
    return dict(const=v)
def schema_for(r):return {"$schema":"https://json-schema.org/draft/2020-12/schema","title":"PE-6 authoritative contract design and execution roadmap",**closed(r)}
@lru_cache(maxsize=None)
def baseline_bytes(p):return git("show",BASE+":"+p)
@lru_cache(maxsize=1)
def accepted_pe5_implementation():
    """Validate PE-5 at its actual immutable closure, never against PE-6 documentation."""
    import test_pe5_configured_association_implementation as prior
    require(raw(PE5_RECORD)==baseline_bytes(PE5_RECORD) and raw(PE5_SCHEMA)==baseline_bytes(PE5_SCHEMA),"accepted PE5 governance immutable")
    record,schema=json.loads(baseline_bytes(PE5_RECORD)),json.loads(baseline_bytes(PE5_SCHEMA))
    original_git=prior.git
    def accepted_git(*a):
        if a==("diff","--name-only",prior.BASE):return git("diff","--name-only",prior.BASE,BASE)
        if a==("ls-files","--others","--exclude-standard"):return b""
        return original_git(*a)
    with patch.dict(prior.__dict__,raw=baseline_bytes,git=accepted_git):
        return prior.validate_implementation(record,schema)
def validate_design(r,s,identities=True):
    require(s==schema_for(r),"exact design schema")
    require(r["schema_version"]==1 and r["baseline_commit"]==BASE and r["checkpoint"]=="PE-6.0" and r["status"]=="COMPLETE_CONTRACT_DESIGN","design authority")
    require(r["pe5_status"]=="COMPLETE" and r["pe6_status"]=="DESIGN_COMPLETE_RUNTIME_NOT_IMPLEMENTED","phase distinction")
    require(all(r[k] is False for k in ["runtime_implementation_authorized","runtime_implemented","production_authorized","production_access","production_mutation","later_checkpoint_started"]),"design-only access boundary")
    require([x["number"] for x in r["requirements"]]==list(range(1,19)) and r["authorization"]["section_count"]==18,"complete user requirements")
    require(len(r["capability_inventory"])==24 and {x["classification"] for x in r["capability_inventory"]}=={"IMPLEMENTED_AND_VALIDATED","IMPLEMENTED_BUT_UNVERIFIED","DESIGNED_NOT_IMPLEMENTED","PLANNED","HISTORICAL_OR_SUPERSEDED","UNKNOWN"},"actual capability classifications")
    require([x["id"] for x in r["decisions"]]==["D%02d"%i for i in range(1,21)] and all(x["existing_authority"] and x["alternatives"] and x["proposal"] and x["rationale"] and x["compatibility"] and x["required_evidence"] and x["operator_approval"] and x["disposition"]=="PROPOSED_FOR_SEPARATE_IMPLEMENTATION_AUTHORIZATION" for x in r["decisions"]),"twenty evidenced proposals")
    c=r["classification_contract"]
    require(c["public_role_is_confirmation"] is False and c["asset_schema_extension"] is False and c["physical_asset_classification_supported"] is False and c["existing_operator_values_never_overwritten"] is True and c["explicit_unknown_is_not_absence"] is True,"operator and Asset authority")
    require(c["operator_role_source"]=="APPROVED_ORIGINAL_KNOWN_CONFIG_WITH_UNIQUE_STRONG_MAC_BINDING_ONLY","confirmation source")
    role=r["role_suggestion_contract"];rules=role["rules"]
    require(len(rules)==7 and len({x["id"] for x in rules})==7 and all(x["confidence"]=="low" and x["authority"]=="UNCONFIRMED_SUGGESTION" and x["scope"]=="technical_role_hypothesis_not_physical_asset_purpose" and x["correlation_policy"] for x in rules),"bounded unconfirmed rule catalog")
    require(role["automatic_confidence"]=="low" and role["numeric_confidence"] is False and "never boost" in rules[0]["correlation_policy"],"no correlated confidence escalation")
    require(all(x["source"] in ["PE1_ACTIVE_HOSTNAME","PE5_CONFIRMED_LOCAL_RELATIONSHIP"] for x in rules),"allowed rule evidence")
    require({"manufacturer_alone","port_alone","MQTT_edge_alone","HA_association_or_domain_alone","IP_or_subnet","raw_Asset_notes_or_purpose","public_role_as_operator_proof","historical_or_expired_hostname"}<=set(role["excluded_sources"]),"prohibited inference sources")
    q=r["metadata_quality_contract"]
    require(q["summary_values"]==["unknown","incomplete","documented","conflicted"] and len(q["dimensions"])==8 and len({x["name"] for x in q["dimensions"]})==8,"separated quality dimensions")
    require(q["numerical_score"] is False and q["notes_required"] is False and q["quality_is_health"] is False and q["quality_is_availability"] is False,"quality not health score")
    o=r["output_semantics"]
    require(o["status"]=="PROPOSED_NOT_IMPLEMENTED" and o["private_only"] is True and o["storage"]=="STATELESS_IN_MEMORY_ONLY" and all(o[k] is False for k in ["persistent_store_required","recurring_execution_required","inventory_hook","public_projection_authorized"]),"stateless private proposal")
    require(o["no_output_file"] is True and o["no_last_known_good"] is True and o["no_new_scheduler"] is True and o["no_new_producer_execution"] is True,"no hidden persistence or execution")
    require(len(r["input_contract"])==7 and [x["kind"] for x in r["input_contract"]]==["inventory","assets","known_operator_role","hostname","manufacturer","home_assistant_summary","pe5_handoff"] and r["input_contract"][0]["required"] is True and all(x["required"] is False for x in r["input_contract"][1:]),"required versus optional source scope")
    require(len(r["required_implementation_fixtures"])==30,"implementation validation matrix")
    require([x["checkpoint"] for x in r["execution_roadmap"]]==["PE-6."+str(i) for i in range(6)],"minimal explicit execution order")
    for i,x in enumerate(r["execution_roadmap"]):
        require(x["dependencies"]==["PE-5.9" if i==0 else "PE-6."+str(i-1)] and x["successor"]==("PE-7" if i==5 else "PE-6."+str(i+1)),"roadmap predecessor/successor")
        require(all(x[k] for k in ["objective","scope","inputs","outputs","access","allowed_changes","tests","acceptance","operator_action","stop_conditions"]),"complete checkpoint contract")
        require(x["status"]==("COMPLETE_CONTRACT_DESIGN" if i==0 else "PLANNED_ONLY_NOT_AUTHORIZED"),"no later checkpoint authorization")
    require(r["next_checkpoint"]=="PE-6.1 - Private classification implementation and comprehensive repository validation" and r["unresolved_decisions"]["design_blockers"]==[],"next gate and design blockers")
    require(all(x["status"]=="UNKNOWN_NOT_OBSERVED" and x["resolved_before"] for x in r["unresolved_decisions"]["operational_facts"]),"no fabricated production facts")
    pe5=json.loads(baseline_bytes(PE5_RECORD))
    require(r["private_handoff"]["accepted_pe5"]==pe5["final_closure"]["private_handoff"] and r["private_handoff"]["pe5_record_sha256"]==sha(baseline_bytes(PE5_RECORD)) and r["private_handoff"]["pe5_schema_sha256"]==sha(baseline_bytes(PE5_SCHEMA)),"immutable complete PE5 handoff")
    require(r["deferred_work"]==pe5["final_closure"]["deferred_work"],"later phases remain deferred")
    shape=r["proposed_output_schema"]
    require(shape["additionalProperties"] is False and shape["properties"]["schema_version"]["const"]=="1.0" and shape["properties"]["rule_version"]["const"]=="pe6-role-v1" and shape["properties"]["devices"]["items"]["additionalProperties"] is False,"private closed output shape")
    fields=set(shape["properties"]["devices"]["items"]["properties"])
    require("role_suggestion" in fields and "metadata_quality" in fields and not fields & {"ip","mac","role","type","health","health_status","expected_availability","notes","physical_location","purpose"},"no protected/raw output fields")
    require(r["validation"]["full_suite_required"] is False and "full native suite for source implementation" in r["validation"]["full_suite_authority"],"implementation versus design test policy")
    require(all(v["failures"]==v["errors"]==0 for v in r["validation"]["baseline_results"].values()),"accepted baseline validation")
    if identities:
        require(len(r["authorized_paths"])==21 and sorted(r["authorized_paths"])==r["authorized_paths"] and set(r["authorized_paths"])=={x["path"] for x in r["artifacts"]}|{RECORD,SCHEMA},"finite successor path map")
        changed=set(git("diff","--name-only",BASE).decode().splitlines())|set(git("ls-files","--others","--exclude-standard").decode().splitlines())
        require(changed==set(r["authorized_paths"]),"unexpected design path")
        for x in r["artifacts"]:
            b=raw(x["path"]);require((sha(b),blob(b))==(x["sha256"],x["git_blob"]),"current PE6 artifact identity: "+x["path"])
        for x in r["protected"]:
            b=baseline_bytes(x["path"]);require(raw(x["path"])==b and (sha(b),blob(b))==(x["sha256"],x["git_blob"]),"immutable predecessor object: "+x["path"])
        doc=raw(DOCUMENT).decode();original=doc.split("~~~text\n",1)[1].rsplit("\n~~~",1)[0]
        require(sha(original.encode())==r["authorization"]["normalized_text_sha256"],"verbatim user authorization")
        require(raw(PE5_RECORD)==baseline_bytes(PE5_RECORD) and raw(PE5_SCHEMA)==baseline_bytes(PE5_SCHEMA),"PE5 accepted package byte preservation")
    return r
@lru_cache(maxsize=1)
def design_successor():
    if (ROOT/"governance/pe6/pe6-classification-implementation.json").exists():
        from test_pe6_classification_implementation import accepted_design
        return accepted_design()
    b,s=raw(RECORD),raw(SCHEMA);r,sc=json.loads(b),json.loads(s)
    require(b==canonical(r) and s==canonical(sc),"canonical PE6 design")
    return validate_design(r,sc)
def design_binding(path):
    if (ROOT/"governance/pe6/pe6-classification-implementation.json").exists():
        from test_pe6_classification_implementation import implementation_binding
        item=implementation_binding(path)
        if item is not None:return item
    item=next((x for x in design_successor()["artifacts"] if x["path"]==path),None)
    if item:require((sha(raw(path)),blob(raw(path)))==(item["sha256"],item["git_blob"]),"PE6 current binding")
    return item
def assert_pe6_sequence(text):
    if (ROOT/"governance/pe6/pe6-classification-implementation.json").exists():
        from test_pe6_classification_implementation import assert_implementation_sequence
        return assert_implementation_sequence(text)
    design_binding("docs/HIOC_MASTER_PLAN.md")
    section=text.split("## Next Planned Task",1)[1].split("### Historical",1)[0]
    require(section.strip().startswith("### PE-6.1 - Private classification implementation and comprehensive repository validation"),"current PE6 next checkpoint")
    require("PE5_STATUS=COMPLETE" in section and "PE6_0_STATUS=COMPLETE_CONTRACT_DESIGN" in section and "PE6_RUNTIME_IMPLEMENTED=FALSE" in section and "Separate authorization is required for PE-6.1" in section,"design versus implementation sequence")
class PE6DesignTests(unittest.TestCase):
    def candidate(self):return copy.deepcopy(design_successor())
    def check(self,r):return validate_design(r,schema_for(r),identities=False)
    def test_closed_canonical_current_contract_and_twenty_one_paths(self):
        r=design_successor();self.assertEqual(len(r["authorized_paths"]),21);self.assertEqual(len(r["decisions"]),20)
    def test_all_original_user_sections_preserved(self):
        r=design_successor();self.assertEqual([x["number"] for x in r["requirements"]],list(range(1,19)))
    def test_reject_missing_requirement(self):
        r=self.candidate();r["requirements"].pop()
        with self.assertRaisesRegex(ValueError,"complete user requirements"):self.check(r)
    def test_reject_unjustified_or_implicitly_approved_decision(self):
        for key,value in [("rationale",""),("disposition","ALREADY_IMPLEMENTED")]:
            r=self.candidate();r["decisions"][0][key]=value
            with self.assertRaisesRegex(ValueError,"twenty evidenced proposals"):self.check(r)
    def test_reject_runtime_or_production_authority(self):
        for key in ["runtime_implementation_authorized","runtime_implemented","production_authorized","production_access","production_mutation","later_checkpoint_started"]:
            r=self.candidate();r[key]=True
            with self.assertRaisesRegex(ValueError,"design-only access boundary"):self.check(r)
    def test_asset_schema1_remains_closed_without_operator_role(self):
        from hioc import assets
        self.assertEqual(assets.SCHEMA_VERSION,"1.0");self.assertEqual(assets.OPERATOR_FIELDS,("friendly_name","physical_location","purpose","notes"))
        self.assertNotIn("operator_role",assets.RECORD_KEYS)
    def test_reject_public_role_confirmation_or_asset_extension(self):
        for key in ["public_role_is_confirmation","asset_schema_extension","physical_asset_classification_supported"]:
            r=self.candidate();r["classification_contract"][key]=True
            with self.assertRaisesRegex(ValueError,"operator and Asset authority"):self.check(r)
    def test_reject_numeric_or_correlated_confidence_escalation(self):
        r=self.candidate();r["role_suggestion_contract"]["rules"][0]["confidence"]="high"
        with self.assertRaisesRegex(ValueError,"bounded unconfirmed rule catalog"):self.check(r)
        r=self.candidate();r["role_suggestion_contract"]["numeric_confidence"]=True
        with self.assertRaisesRegex(ValueError,"no correlated confidence escalation"):self.check(r)
    def test_mqtt_ha_manufacturer_and_ports_are_not_role_authority(self):
        r=self.candidate();r["role_suggestion_contract"]["rules"][0]["source"]="MQTT_EDGE"
        with self.assertRaisesRegex(ValueError,"allowed rule evidence"):self.check(r)
    def test_quality_keeps_dimensions_and_never_becomes_health(self):
        r=self.candidate();r["metadata_quality_contract"]["quality_is_health"]=True
        with self.assertRaisesRegex(ValueError,"quality not health score"):self.check(r)
    def test_reject_persistence_schedule_or_inventory_hook(self):
        for key in ["persistent_store_required","recurring_execution_required","inventory_hook","public_projection_authorized"]:
            r=self.candidate();r["output_semantics"][key]=True
            with self.assertRaisesRegex(ValueError,"stateless private proposal"):self.check(r)
    def test_reject_pe5_confirmation_weakening(self):
        r=self.candidate();r["private_handoff"]["accepted_pe5"]["configured_valid_requires_confirmed_source"]=False
        with self.assertRaisesRegex(ValueError,"immutable complete PE5 handoff"):self.check(r)
    def test_frozen_pe5_schema_and_runtime_objects_unchanged(self):
        r=design_successor();self.assertEqual(raw(PE5_RECORD),baseline_bytes(PE5_RECORD));self.assertEqual(raw(PE5_SCHEMA),baseline_bytes(PE5_SCHEMA))
        for x in r["protected"]:
            if x["path"].startswith(("pi4/","deploy/","homeassistant/","governance/pe5/")):self.assertEqual(raw(x["path"]),baseline_bytes(x["path"]))
    def test_historical_pe5_acceptance_uses_exact_closure(self):
        self.assertEqual(accepted_pe5_implementation(),json.loads(baseline_bytes(PE5_RECORD)))
    def test_current_master_plan_and_legacy_binding_consumers(self):
        assert_pe6_sequence(raw("docs/HIOC_MASTER_PLAN.md").decode())
        from test_pe4_documentation_consistency_correction import current_artifacts,current_binding
        mapping={x["path"]:x for x in current_artifacts()}
        for x in design_successor()["artifacts"]:
            self.assertEqual(mapping[x["path"]],design_binding(x["path"]));self.assertEqual(current_binding(x["path"]),design_binding(x["path"]))
        from test_pe4_ha_association_public_projection_test_binding_correction import closure_artifact_bindings
        closure=closure_artifact_bindings()
        for x in design_successor()["artifacts"]:self.assertEqual(closure[x["path"]],design_binding(x["path"]))
        old=next(x for x in accepted_pe5_implementation()["artifacts"] if x["path"]=="docs/DATA_MODEL.md")
        self.assertNotEqual(old["sha256"],closure["docs/DATA_MODEL.md"]["sha256"])
        self.assertEqual(sha(baseline_bytes("docs/DATA_MODEL.md")),old["sha256"])
    def test_reject_protected_or_raw_output_field(self):
        r=self.candidate();r["proposed_output_schema"]["properties"]["devices"]["items"]["properties"]["health_status"]={"type":"string"}
        with self.assertRaisesRegex(ValueError,"no protected/raw output fields"):self.check(r)
    def test_declarative_output_schema_fixture_not_classifier_execution(self):
        from test_pe5_mapping_contract_design import check_shape
        r=design_successor();shape=r["proposed_output_schema"]
        example=dict(schema_version="1.0",rule_version="pe6-role-v1",state="UNAVAILABLE",evaluated_at="2026-10-14T00:00:00Z",valid_until=None,inputs=[],devices=[],summary=dict(device_count=0,suggestion_count=0,conflicted_count=0,unavailable_source_count=0))
        check_shape(example,shape)
        for key,value in [("schema_version","2.0"),("secret","SYNTHETIC_NOT_A_CREDENTIAL")]:
            bad=copy.deepcopy(example);bad[key]=value
            with self.assertRaises(ValueError):check_shape(bad,shape)
    def test_reject_unresolved_design_blocker_or_fabricated_production_fact(self):
        r=self.candidate();r["unresolved_decisions"]["design_blockers"]=["unknown"]
        with self.assertRaisesRegex(ValueError,"next gate and design blockers"):self.check(r)
        r=self.candidate();r["unresolved_decisions"]["operational_facts"][0]["status"]="OBSERVED"
        with self.assertRaisesRegex(ValueError,"no fabricated production facts"):self.check(r)
    def test_roadmap_preserves_source_deploy_execution_and_pe7_boundaries(self):
        r=self.candidate();r["execution_roadmap"][3]["successor"]="PE-7"
        with self.assertRaisesRegex(ValueError,"roadmap predecessor/successor"):self.check(r)
    def test_original_test_classes_and_historical_validator_bodies_preserved(self):
        p="tests/test_pe5_configured_association_implementation.py";before,after=ast.parse(baseline_bytes(p)),ast.parse(raw(p))
        classes=lambda t:{x.name:ast.dump(x,include_attributes=False) for x in t.body if isinstance(x,ast.ClassDef)}
        self.assertEqual(classes(before),classes(after))
        funcs=lambda t:{x.name:x for x in t.body if isinstance(x,ast.FunctionDef)}
        old,new=funcs(before),funcs(after)
        for name,fn in old.items():
            if name not in ["implementation_successor","implementation_binding","assert_implementation_sequence"]:self.assertEqual(ast.dump(fn,include_attributes=False),ast.dump(new[name],include_attributes=False))
            else:
                bodies=[ast.dump(x,include_attributes=False) for x in new[name].body]
                self.assertTrue(all(ast.dump(x,include_attributes=False) in bodies for x in fn.body),name)
if __name__=="__main__":unittest.main()
