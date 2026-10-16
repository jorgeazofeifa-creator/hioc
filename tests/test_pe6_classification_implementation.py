"""Separate immutable PE-6.0 acceptance and exact current PE-6.1 successor authority."""
import ast
import copy
import hashlib
import json
import os
import subprocess
from functools import lru_cache
from pathlib import Path
from unittest.mock import patch
import unittest
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))

ROOT=Path(__file__).resolve().parents[1]
BASE="ea4a93fba1615af1d6641c7f0683b8e912c03d72"
RECORD="governance/pe6/pe6-classification-implementation.json"
SCHEMA=RECORD.replace(".json",".schema.json")
DESIGN_RECORD="governance/pe6/pe6-classification-contract-design.json"
DESIGN_SCHEMA=DESIGN_RECORD.replace(".json",".schema.json")
DESIGN_DOCUMENT="docs/PE6_CLASSIFICATION_CONTRACT_DESIGN.md"
AUTHORIZED_PATHS=["ROADMAP.md","docs/CHANGELOG.md","docs/DATA_MODEL.md","docs/DEPLOYMENT.md","docs/HIOC_MASTER_PLAN.md","docs/HOME_ASSISTANT.md","docs/MQTT.md","docs/OPERATIONS.md","docs/PASSIVE_ENRICHMENT_ARCHITECTURE.md","docs/PE5_CONFIGURED_ASSOCIATION_IMPLEMENTATION.md","docs/PE5_IMPLEMENTATION_PREPARATION.md","docs/PE5_LOCAL_SERVICE_ASSOCIATION_IMPLEMENTATION.md","docs/PE6_CLASSIFICATION_IMPLEMENTATION.md","docs/RELEASE.md","docs/SYSTEM_REFERENCE.md","governance/pe6/pe6-classification-implementation.json","governance/pe6/pe6-classification-implementation.schema.json","pi4/bin/hioc-classify-metadata.py","pi4/lib/hioc/classification.py","pi4/lib/hioc/classification_caller.py","pi4/lib/hioc/classification_contract.py","tests/test_pe4_documentation_consistency_correction.py","tests/test_pe4_ha_association_public_projection_test_binding_correction.py","tests/test_pe5_service_association_caller.py","tests/test_pe6_classification.py","tests/test_pe6_classification_contract_design.py","tests/test_pe6_classification_implementation.py"]

def git(*args):
    return subprocess.check_output(["git","--no-optional-locks",*args],cwd=ROOT,
        env=dict(os.environ,GIT_OPTIONAL_LOCKS="0"),stderr=subprocess.PIPE)
def raw(path):return (ROOT/path).read_bytes().replace(b"\r\n",b"\n")
def sha(value):return hashlib.sha256(value).hexdigest()
def blob(value):return hashlib.sha1(b"blob "+str(len(value)).encode()+b"\0"+value).hexdigest()
def canonical(value):return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=True).encode()+b"\n"
def require(condition,reason):
    if not condition:raise ValueError(reason)
def closed(value):
    if type(value)is dict:return dict(type="object",additionalProperties=False,required=sorted(value),properties={k:closed(v) for k,v in sorted(value.items())})
    if type(value)is list:return dict(type="array",minItems=len(value),maxItems=len(value),prefixItems=[closed(v) for v in value],items=False)
    return dict(const=value)
def schema_for(value):
    return {"$schema":"https://json-schema.org/draft/2020-12/schema","title":"PE-6.1 private classification repository implementation",**closed(value)}

@lru_cache(maxsize=None)
def historical(path):return git("show",BASE+":"+path)

def validate_historical_design(record,schema):
    """Original validator/path check, replayed only against exact accepted Git objects."""
    import test_pe6_classification_contract_design as prior
    original_git=prior.git
    def accepted_git(*args):
        if args==("diff","--name-only",prior.BASE):
            return original_git("diff","--name-only",prior.BASE,BASE)
        if args==("ls-files","--others","--exclude-standard"):
            return b""  # The immutable accepted commit has no untracked namespace.
        return original_git(*args)
    with patch.dict(prior.__dict__,raw=historical,git=accepted_git):
        return prior.validate_design(record,schema)

@lru_cache(maxsize=1)
def _accepted_design():
    # Cache only validation of immutable Git objects, never current file checks.
    record,schema=json.loads(historical(DESIGN_RECORD)),json.loads(historical(DESIGN_SCHEMA))
    require(historical(DESIGN_RECORD)==canonical(record) and historical(DESIGN_SCHEMA)==canonical(schema),"canonical historical design")
    return validate_historical_design(record,schema)

def accepted_design():
    require(all(raw(path)==historical(path) for path in [DESIGN_RECORD,DESIGN_SCHEMA,DESIGN_DOCUMENT]),"immutable PE6.0 design authority")
    return copy.deepcopy(_accepted_design())

def validate_implementation(record,schema,identities=True):
    require(schema==schema_for(record),"exact implementation schema")
    require(record["baseline_commit"]==BASE and record["checkpoint"]=="PE-6.1" and record["status"]=="IMPLEMENTED_REPOSITORY_ONLY","implementation authority")
    require(record["pe5_status"]=="COMPLETE/PASS" and record["pe6_0_status"]=="COMPLETE/PASS" and record["pe6_status"]=="IN_PROGRESS_REPOSITORY_IMPLEMENTED","phase boundaries")
    require(record["repository_implementation_authorized"] is True and record["production_authorized"] is False and all(record[k] is False for k in ["production_access","production_mutation","runtime_deployment_performed","runtime_execution_performed","pe6_2_started","public_projection_added","inventory_hook_added","scheduler_added","persistence_added"]),"implementation-only boundary")
    require(record["next_checkpoint"]=="PE-6.2 - PI3 Release-Source Synchronization" and record["full_native_suite_required"] is True,"next checkpoint and mandatory full suite")
    require(record["authorized_paths"]==AUTHORIZED_PATHS and {x["path"] for x in record["artifacts"]}|{RECORD,SCHEMA}==set(AUTHORIZED_PATHS),"finite implementation scope")
    design=accepted_design()
    require(record["design_adoption"]["commit"]==BASE and record["design_adoption"]["decision_ids"]==[x["id"] for x in design["decisions"]] and record["design_adoption"]["schema_sha256"]==sha(historical(DESIGN_SCHEMA)) and record["design_adoption"]["record_sha256"]==sha(historical(DESIGN_RECORD)),"exact adopted design")
    require([x["requirement"] for x in record["fixture_coverage"]]==design["required_implementation_fixtures"] and len(record["fixture_coverage"])==30,"complete adopted fixture ledger")
    require(all(x["evidence"] and x["disposition"] in ["REPOSITORY_SYNTHETIC_VALIDATION","DEFERRED_SEPARATE_NATIVE_CHECKPOINT"] for x in record["fixture_coverage"]),"fixture evidence not fabricated")
    if not identities:return record
    changed=set(git("diff","--name-only",BASE).decode().splitlines())|set(git("ls-files","--others","--exclude-standard").decode().splitlines())
    require(changed==set(AUTHORIZED_PATHS),"unexpected implementation path")
    require(set(git("diff","--cached","--name-only",BASE).decode().splitlines())==set(AUTHORIZED_PATHS),"unexpected staged implementation path")
    entries=[row.split("\t",1) for row in git("ls-files","--stage").decode().splitlines()]
    require(all(row.split()[2]=="0" for row,path in entries),"unmerged implementation index")
    index={path:row.split()[:2] for row,path in entries}
    for item in record["artifacts"]:
        value=raw(item["path"])
        require((sha(value),blob(value))==(item["sha256"],item["git_blob"]),"current implementation artifact: "+item["path"])
        require(index.get(item["path"])==[item["mode"],blob(value)],"current staged artifact: "+item["path"])
    for path in [RECORD,SCHEMA]:
        require(index.get(path)==["100644",blob(raw(path))],"current staged governance: "+path)
    baseline=set(git("ls-tree","-r","--name-only",BASE).decode().splitlines())
    require({x["path"] for x in record["protected"]}==baseline-set(AUTHORIZED_PATHS),"complete protected baseline")
    for item in record["protected"]:
        value=historical(item["path"])
        require(raw(item["path"])==value and (sha(value),blob(value))==(item["sha256"],item["git_blob"]) and index.get(item["path"])==[item["mode"],item["git_blob"]],"protected baseline artifact: "+item["path"])
    from hioc.classification_contract import SCHEMA as output, RULES, DIMENSIONS
    require(output==design["proposed_output_schema"] and RULES==design["role_suggestion_contract"]["rules"] and DIMENSIONS==design["metadata_quality_contract"]["dimensions"],"adopted runtime constants")
    return record

def implementation_successor():
    if (ROOT/"governance/continuity/project-handoff.json").exists():
        from hioc_project_continuity import current_implementation
        return current_implementation()
    record,schema=json.loads(raw(RECORD)),json.loads(raw(SCHEMA))
    require(raw(RECORD)==canonical(record) and raw(SCHEMA)==canonical(schema),"canonical implementation")
    return validate_implementation(record,schema)

def implementation_binding(path):
    if (ROOT/"governance/continuity/project-handoff.json").exists():
        from hioc_project_continuity import current_implementation
        return next((x for x in current_implementation()["artifacts"] if x["path"]==path),None)
    item=next((x for x in implementation_successor()["artifacts"] if x["path"]==path),None)
    if item:require((sha(raw(path)),blob(raw(path)))==(item["sha256"],item["git_blob"]),"current successor identity")
    return item

def assert_implementation_sequence(text):
    implementation_binding("docs/HIOC_MASTER_PLAN.md")
    section=text.split("## Next Planned Task",1)[1].split("### Historical",1)[0]
    require(section.strip().startswith("### PE-6.2 - PI3 Release-Source Synchronization"),"current implementation successor")
    require(all(x in section for x in ["PE5_STATUS=COMPLETE","PE6_1_STATUS=COMPLETE/PASS","PE6_REPOSITORY_IMPLEMENTED=TRUE","PE6_PRODUCTION_DEPLOYED=FALSE","Separate authorization is required for PE-6.2"]),"repository versus production sequence")

class ImplementationGovernanceTests(unittest.TestCase):
    def test_current_implementation_closed_scope_identity_and_protected_objects(self):
        self.assertEqual(implementation_successor()["authorized_paths"],AUTHORIZED_PATHS)
    def test_historical_design_retains_exact_twenty_one_paths(self):
        record=accepted_design()
        self.assertEqual(len(record["authorized_paths"]),21)
        self.assertEqual(set(record["authorized_paths"]),set(git("diff","--name-only","d6f9d3c6bd07b16fc515ae531b6aa0a3e9188221",BASE).decode().splitlines()))
        for item in record["artifacts"]:
            value=historical(item["path"])
            self.assertEqual((sha(value),blob(value)),(item["sha256"],item["git_blob"]))
    def test_original_historical_validator_body_and_scope_check_unchanged(self):
        path="tests/test_pe6_classification_contract_design.py"
        def function(data):
            return next(x for x in ast.parse(data).body if isinstance(x,ast.FunctionDef) and x.name=="validate_design")
        self.assertEqual(ast.dump(function(historical(path)),include_attributes=False),ast.dump(function(raw(path)),include_attributes=False))
    def test_historical_record_identity_cannot_be_refreshed(self):
        record=copy.deepcopy(accepted_design());schema=json.loads(historical(DESIGN_SCHEMA))
        record["artifacts"][0]["sha256"]="0"*64
        with self.assertRaises(ValueError):validate_historical_design(record,schema)
        import test_pe6_classification_contract_design as prior
        with self.assertRaises(ValueError):validate_historical_design(record,prior.schema_for(record))
    def test_historical_authorization_cannot_be_expanded_for_successor(self):
        import test_pe6_classification_contract_design as prior
        record=copy.deepcopy(accepted_design());record["authorized_paths"].append("pi4/lib/hioc/classification.py")
        with self.assertRaises(ValueError):validate_historical_design(record,prior.schema_for(record))
    def test_unrelated_untracked_file_is_not_authorized(self):
        original=git
        def extra(*args):
            if args==("ls-files","--others","--exclude-standard"):
                return original(*args)+b"unrelated-private-file.txt\n"
            return original(*args)
        record=copy.deepcopy(implementation_successor())
        with patch.dict(globals(),git=extra),self.assertRaisesRegex(ValueError,"unexpected implementation path"):
            validate_implementation(record,schema_for(record))
    def test_protected_runtime_mutation_is_rejected(self):
        original=raw
        path="pi4/lib/hioc/inventory.py"
        def changed(p):return b"unauthorized" if p==path else original(p)
        record=copy.deepcopy(implementation_successor())
        with patch.dict(globals(),raw=changed),self.assertRaisesRegex(ValueError,"protected baseline artifact"):
            validate_implementation(record,schema_for(record))
    def test_current_and_historical_maps_are_independent(self):
        from test_pe6_classification_contract_design import design_successor,design_binding
        self.assertEqual(design_successor(),accepted_design())
        old=next(x for x in accepted_design()["artifacts"] if x["path"]=="docs/HIOC_MASTER_PLAN.md")
        new=implementation_binding(old["path"])
        self.assertNotEqual(old["sha256"],new["sha256"])
        self.assertEqual(design_binding(old["path"]),new)
        assert_implementation_sequence(raw(old["path"]).decode())
    def test_historical_design_source_record_schema_unchanged(self):
        for path in [DESIGN_RECORD,DESIGN_SCHEMA,DESIGN_DOCUMENT]:
            self.assertEqual(raw(path),historical(path))
    def test_original_five_file_candidate_and_asset_correction_retained(self):
        record=implementation_successor()
        self.assertEqual(len(record["preserved_candidate_paths"]),5)
        self.assertIn("return parsed, dict(kind=kind",raw("pi4/lib/hioc/classification.py").decode())
        self.assertIn("asset_path.write_bytes(serialize_store(asset()))",raw("tests/test_pe6_classification.py").decode())
        # CLI and contract constants remain byte-identical; reader correction is separately authorized.
        for item in record["preserved_candidate_unmodified"]:
            self.assertEqual(sha(raw(item["path"])),item["sha256"])
            self.assertEqual(sha((ROOT/item["path"]).read_bytes()),item["file_sha256"])
    def test_full_suite_and_no_operational_authority(self):
        record=implementation_successor()
        self.assertTrue(record["full_native_suite_required"])
        self.assertFalse(record["production_authorized"])
        self.assertFalse(record["pe6_2_started"])
        self.assertEqual(record["operational_facts"],accepted_design()["unresolved_decisions"]["operational_facts"])


    def public_entries(self):
        import test_pe6_classification_contract_design as prior
        text=raw('docs/HIOC_MASTER_PLAN.md').decode()
        return [implementation_successor,
                lambda:implementation_binding('docs/HIOC_MASTER_PLAN.md'),
                lambda:assert_implementation_sequence(text),
                lambda:prior.design_binding('docs/HIOC_MASTER_PLAN.md'),
                lambda:prior.assert_pe6_sequence(text)]

    def test_warm_public_entries_reject_new_unauthorized_path(self):
        implementation_successor();original=git
        def extra(*args):
            if args==('ls-files','--others','--exclude-standard'):
                return original(*args)+b'unauthorized-after-validation.txt\n'
            return original(*args)
        with patch.dict(globals(),git=extra):
            for entry in self.public_entries():
                with self.assertRaisesRegex(ValueError,'unexpected implementation path'):entry()

    def test_warm_public_entries_reject_protected_mutation(self):
        implementation_successor();original=raw
        def changed(path):return b'unauthorized' if path=='pi4/lib/hioc/inventory.py' else original(path)
        with patch.dict(globals(),raw=changed):
            for entry in self.public_entries():
                with self.assertRaisesRegex(ValueError,'protected baseline artifact'):entry()

    def test_warm_public_entries_revalidate_record_and_schema(self):
        implementation_successor();original=raw
        for path in (RECORD,SCHEMA):
            changed=json.loads(original(path))
            changed['unexpected_after_warmup']=True
            def replaced(name,path=path,changed=changed):return canonical(changed) if name==path else original(name)
            with self.subTest(path=path),patch.dict(globals(),raw=replaced):
                for entry in self.public_entries():
                    with self.assertRaisesRegex(ValueError,'exact implementation schema'):entry()
        implementation_successor()  # Restored fixture is independently valid.

    def test_warm_public_entries_revalidate_current_artifact(self):
        implementation_successor();original=raw
        def changed(path):return original(path)+b'\n' if path=='docs/DATA_MODEL.md' else original(path)
        with patch.dict(globals(),raw=changed):
            for entry in self.public_entries():
                with self.assertRaisesRegex(ValueError,'current implementation artifact'):entry()

    def test_warm_public_entries_revalidate_index_object_and_scope(self):
        implementation_successor();original=git
        def changed(*args):
            result=original(*args)
            if args==('ls-files','--stage'):
                rows=result.decode().splitlines()
                for i,row in enumerate(rows):
                    if row.endswith('\tdocs/DATA_MODEL.md'):
                        mode,oid,stage=row.split('\t')[0].split()
                        rows[i]=mode+' '+'0'*40+' '+stage+'\tdocs/DATA_MODEL.md'
                return ('\n'.join(rows)+'\n').encode()
            return result
        with patch.dict(globals(),git=changed):
            for entry in self.public_entries():
                with self.assertRaisesRegex(ValueError,'current staged artifact'):entry()
        def extra(*args):
            result=original(*args)
            return result+b'unauthorized-index.txt\n' if args==('diff','--cached','--name-only',BASE) else result
        with patch.dict(globals(),git=extra):
            for entry in self.public_entries():
                with self.assertRaisesRegex(ValueError,'unexpected staged implementation path'):entry()

    def test_immutable_cache_is_preserved_but_current_design_guard_is_fresh(self):
        first=_accepted_design();self.assertIs(first,_accepted_design())
        exposed=accepted_design();exposed['authorized_paths'].append('forged')
        self.assertNotIn('forged',accepted_design()['authorized_paths'])
        original=raw
        with patch.dict(globals(),raw=lambda path:b'forged' if path==DESIGN_RECORD else original(path)):
            with self.assertRaisesRegex(ValueError,'immutable PE6.0 design authority'):accepted_design()
        self.assertEqual(len(accepted_design()['authorized_paths']),21)



    def test_historical_runtime_guard_accepts_only_exact_pe61_additions(self):
        from test_pe5_service_association_caller import assert_historical_runtime_tree
        assert_historical_runtime_tree('c7db29f795909d7926e36c02f1166034bcebb8b0',['pi4','release','tools','requirements-pe4.lock'])

    def test_historical_runtime_guard_original_statements_and_classes_preserved(self):
        path='tests/test_pe5_service_association_caller.py'
        old,new=ast.parse(historical(path)),ast.parse(raw(path))
        classes=lambda tree:[ast.dump(n,include_attributes=False) for n in tree.body if isinstance(n,ast.ClassDef)]
        self.assertEqual(classes(old),classes(new))
        function=lambda tree:next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='assert_historical_runtime_tree')
        prior=[ast.dump(n,include_attributes=False) for n in function(old).body]
        current=[ast.dump(n,include_attributes=False) for n in function(new).body]
        self.assertEqual(len(current),len(prior)+1)
        self.assertEqual([n for n in current if n in prior],prior)

    def test_historical_runtime_guard_cannot_exempt_existing_baseline_file(self):
        import test_pe5_service_association_caller as prior
        original=prior.git
        def existing(*args):
            if args[:3]==('ls-tree','--name-only',BASE) and args[-1].startswith('pi4/'):
                return (args[-1]+'\n').encode()
            return original(*args)
        with patch.object(prior,'git',existing),self.assertRaisesRegex(ValueError,'existing runtime cannot be exempted'):
            prior.assert_historical_runtime_tree('c7db29f795909d7926e36c02f1166034bcebb8b0',['pi4'])


def load_tests(loader, tests, pattern):
    if (ROOT/"governance/continuity/project-handoff.json").exists():
        from hioc_project_continuity import historical_implementation_tests
        return historical_implementation_tests(loader)
    return tests

if __name__=="__main__":unittest.main()
