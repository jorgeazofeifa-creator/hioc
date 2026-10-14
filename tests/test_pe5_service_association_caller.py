"""Synthetic offline caller tests; never production."""
import ast
import copy
import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from functools import lru_cache
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/"tests"),str(ROOT/"pi4/lib")]
from hioc import service_association
from test_pe5_local_service_association import snapshot, NOW, OWNER, SERVICE
SCRIPT=ROOT/"pi4/bin/hioc-resolve-local-services.py"
spec=importlib.util.spec_from_file_location("pe5_private_caller",SCRIPT)
caller=importlib.util.module_from_spec(spec);spec.loader.exec_module(caller)
BASE="e30e483d7e5ede1cde1f75bc25bc65ff4ec115b1"
RECORD="governance/pe5/pe5-service-association-caller-integration.json"
SCHEMA=RECORD.replace(".json",".schema.json")
CALLER_PATHS=tuple(["docs/HIOC_MASTER_PLAN.md","docs/PASSIVE_ENRICHMENT_ARCHITECTURE.md","docs/PE5_LOCAL_SERVICE_ASSOCIATION_IMPLEMENTATION.md","governance/pe5/pe5-service-association-caller-integration.json","governance/pe5/pe5-service-association-caller-integration.schema.json","pi4/bin/hioc-resolve-local-services.py","tests/test_pe4_documentation_consistency_correction_closure.py","tests/test_pe4_ha_association_public_projection_deployment_closure.py","tests/test_pe4_ha_association_public_projection_deployment_preparation.py","tests/test_pe4_ha_association_public_projection_test_binding_correction.py","tests/test_pe5_implementation_preparation.py","tests/test_pe5_local_service_association.py","tests/test_pe5_service_association_caller.py"])
def git(*a):return subprocess.check_output(["git","--no-optional-locks",*a],cwd=ROOT,env=dict(os.environ,GIT_OPTIONAL_LOCKS="0"),stderr=subprocess.PIPE)
def raw(p):return (ROOT/p).read_bytes().replace(b"\r\n",b"\n")
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def canonical(v):return (json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False)+"\n").encode()
def closed(v):
    if type(v) is dict:return dict(type="object",additionalProperties=False,required=sorted(v),properties={k:closed(x) for k,x in sorted(v.items())})
    if type(v) is list:return dict(type="array",minItems=len(v),maxItems=len(v),prefixItems=[closed(x) for x in v],items=False)
    return dict(const=v)
def schema_for(v):return {"$schema":"https://json-schema.org/draft/2020-12/schema","title":"PE-5.1 bounded offline caller integration",**closed(v)}
def require(v,message):
    if not v:raise ValueError(message)

def _validate_historical_caller(r,s):
    require(s==schema_for(r),"exact caller schema mismatch")
    require(r["predecessor_commit"]==BASE and r["authorized_paths"]==list(CALLER_PATHS),"wrong caller scope")
    require(r["status"]=="IMPLEMENTED_REPOSITORY_CALLER_CANDIDATE","wrong caller status")
    require(r["production_authorized"] is False and r["producer_hook_added"] is False and r["persistence_added"] is False,"operational authority")
    require(r["snapshot_age_policy"]=="UNKNOWN_REQUIRED_BEFORE_OPERATIONAL_USE" and r["policy_default"] is None,"policy invented")
    require(r["private_state_requirement"]=="DEFERRED_NOT_REQUIRED_FOR_OFFLINE_CALLER","writer expanded")
    require(r["current_next_task"]=="PE5_1_CALLER_CANDIDATE_REVIEW","wrong current task")
    require(r["lifecycle"]==dict(phase7a="ACTIVE",pe4="PASS/CLOSED",public_projection="PASS/CLOSED",pe5="IN_PROGRESS_REPOSITORY_ONLY",pe5_1="IMPLEMENTED_REPOSITORY_CANDIDATE",caller="IMPLEMENTED_REPOSITORY_CALLER_CANDIDATE",surveillance="PLANNED_NOT_STARTED"),"lifecycle changed")
    require(not git("diff","--cached","--name-only") and not git("stash","list"),"staging/stash changed")
    head=git("rev-parse","HEAD").decode().strip()
    if head==BASE:
        require(git("rev-parse","origin/main").decode().strip()==BASE,"tracking changed")
        changed=set(git("diff","--name-only").decode().splitlines())|set(git("ls-files","--others","--exclude-standard").decode().splitlines())
    else:
        require(git("rev-parse","HEAD^").decode().strip()==BASE and not git("status","--porcelain"),"wrong committed caller")
        changed=set(git("diff","--name-only",BASE,head).decode().splitlines())
    require(changed==set(CALLER_PATHS),"unexpected caller mutation")
    require(len(r["artifacts"])==len(CALLER_PATHS)-2 and {i["path"] for i in r["artifacts"]}==set(CALLER_PATHS)-{RECORD,SCHEMA},"incomplete map")
    for i in r["artifacts"]:
        b=raw(i["path"]);require(sha(b)==i["sha256"] and blob(b)==i["git_blob"],"current identity mismatch")
    for i in r["protected_artifacts"]:
        b=git("show",BASE+":"+i["path"])
        require(sha(b)==i["sha256"] and blob(b)==i["git_blob"] and raw(i["path"])==b,"immutable source changed")
    import difflib
    for p,changes in r["document_edits"].items():
        old=git("show",BASE+":"+p).decode().splitlines(keepends=True)
        now=raw(p).decode().splitlines(keepends=True)
        require(list(difflib.unified_diff(old,now))==changes,"unrelated document mutation")
    old=ast.parse(git("show",BASE+":tests/test_pe5_local_service_association.py"));now=ast.parse(raw("tests/test_pe5_local_service_association.py"))
    f=lambda t,n:next(x for x in t.body if isinstance(x,ast.FunctionDef) and x.name==n)
    require([ast.dump(x) for x in f(old,"validate_implementation_record").body]==[ast.dump(x) for x in f(now,"_validate_historical_implementation").body],"historical validator weakened")
    master=raw("docs/HIOC_MASTER_PLAN.md").decode()
    for marker in ["## Current Objective","## Next Planned Task"]:
        section=master.split(marker,1)[1].split("### Historical",1)[0]
        for phrase in ["PE-5.1","caller","NOT AUTHORIZED","UNKNOWN_REQUIRED_BEFORE_OPERATIONAL_USE","PE-4 PASS/CLOSED","Public Projection PASS/CLOSED"]:require(phrase in section,"sequence missing")
    original=git("show",BASE+":docs/HIOC_MASTER_PLAN.md").decode()
    extract=lambda t:t.split("<!-- ORIGINAL_SURVEILLANCE_SPECIFICATION_BEGIN -->\n```text\n",1)[1].split("```\n<!-- ORIGINAL_SURVEILLANCE_SPECIFICATION_END -->",1)[0]
    require(extract(master)==extract(original),"surveillance changed")
    return r

ACCEPTED_CALLER = "eda8c9930d7f7fbf09bcc08b252bef05b385cf7e"

def caller_historical_bytes(path):
    return git("show", ACCEPTED_CALLER+":"+path)

def validate_caller_record(r,s):
    original_git=git
    def historical_git(*args):
        if args == ("rev-parse","HEAD"):return (ACCEPTED_CALLER+"\n").encode()
        if args == ("rev-parse","HEAD^"):return (BASE+"\n").encode()
        if args in [("status","--porcelain"),("diff","--cached","--name-only"),("stash","list")]:return b""
        return original_git(*args)
    with patch.dict(globals(),git=historical_git,raw=caller_historical_bytes):
        return _validate_historical_caller(r,s)

@lru_cache(maxsize=1)
def caller_successor():
    rraw=caller_historical_bytes(RECORD);sraw=caller_historical_bytes(SCHEMA)
    r=json.loads(rraw);s=json.loads(sraw)
    require(rraw==canonical(r) and sraw==canonical(s),"noncanonical historical caller")
    return validate_caller_record(r,s)

def caller_current_binding(path):
    from test_pe5_execution_roadmap import roadmap_binding
    bound=roadmap_binding(path)
    if bound is not None:return bound
    from test_pe5_snapshot_age_policy import POLICY_PATHS, policy_current_binding
    if path in POLICY_PATHS:return policy_current_binding(path)
    r=caller_successor();i=next((x for x in r["artifacts"] if x["path"]==path),None)
    require(i is not None,"outside caller map")
    require(sha(raw(path))==i["sha256"] and blob(raw(path))==i["git_blob"],"caller identity mismatch")
    return i
def _assert_historical_caller_sequence(text):
    caller_current_binding("docs/HIOC_MASTER_PLAN.md")
    current=text.split("## Next Planned Task",1)[1].split("### Historical",1)[0]
    require(current.strip().startswith("### PE-5.1 caller integration"),"caller task absent")
    require("NOT AUTHORIZED" in current and "UNKNOWN_REQUIRED_BEFORE_OPERATIONAL_USE" in current,"policy gate absent")


def assert_caller_sequence(text):
    from test_pe5_snapshot_age_policy import assert_policy_sequence
    return assert_policy_sequence(text)

def assert_historical_runtime_tree(historical_commit, roots):
    # Original runtime artifacts remain immutable; only exact later additions are permitted.
    caller_current_binding("pi4/bin/hioc-resolve-local-services.py")
    approved={"pi4/lib/hioc/service_association.py","pi4/bin/hioc-resolve-local-services.py"}
    changes=set(git("diff","--name-only",historical_commit,"--",*roots).decode().splitlines())
    require(changes<=approved,"historical runtime modified outside exact additive successors")
    for p in approved:
        require(not git("ls-tree","--name-only",historical_commit,"--",p),"historical artifact cannot be exempted")
    resolver=git("show",BASE+":pi4/lib/hioc/service_association.py")
    require(raw("pi4/lib/hioc/service_association.py")==resolver,"accepted resolver changed")
    accepted=json.loads(git("show",BASE+":governance/pe5/pe5-local-service-association-implementation.json"))
    i=next(x for x in accepted["artifacts"] if x["path"]=="pi4/lib/hioc/service_association.py")
    require(sha(resolver)==i["sha256"] and blob(resolver)==i["git_blob"],"accepted additive identity mismatch")

class CallerTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.path=Path(self.temp.name)/"snapshot.json";self.value=snapshot()
        self.path.write_text(json.dumps(self.value))
    def evaluate(self,time=NOW,age=60):return caller.evaluate_file(self.path,time,age)
    def args(self):return ["--inventory-file",str(self.path),"--evaluated-at",NOW,"--max-snapshot-age-seconds","60"]
    def cli(self,args):
        out=io.StringIO();err=io.StringIO()
        with patch("sys.stdout",out),patch("sys.stderr",err):code=caller.main(args)
        return code,out.getvalue(),err.getvalue()
    def test_finalized_snapshot_matches_resolver(self):
        self.assertEqual(self.evaluate(),service_association.resolve_service_associations(self.value,NOW,60))
    def test_inventory_and_protected_fields_unchanged(self):
        before=self.path.read_bytes();value=copy.deepcopy(self.value);result=self.evaluate()
        self.assertEqual(self.path.read_bytes(),before);self.assertEqual(self.value,value)
        edge=result["service_associations"][0]
        self.assertEqual((edge["service_id"],edge["stable_device_id"]),(SERVICE,OWNER))
    def test_deterministic_complete_private_output(self):
        a=self.cli(self.args());self.assertEqual(a,self.cli(self.args()))
        self.assertEqual((a[0],a[2]),(0,""))
        service_association.validate_service_association_envelope(json.loads(a[1]))
    def test_each_required_option_absent_before_read(self):
        for name in ["--inventory-file","--evaluated-at","--max-snapshot-age-seconds"]:
            args=self.args();i=args.index(name);del args[i:i+2]
            with patch.object(caller,"evaluate_file",side_effect=AssertionError("read")):
                self.assertEqual(self.cli(args),(1,"","CALLER_ARGUMENT_INVALID\n"))
    def test_no_default_invalid_age_configuration(self):
        for value in ["","-1","1.0","true","60x","9007199254740992"]:
            args=self.args();args[-1]=value
            with self.subTest(value=value):
                code,out,err=self.cli(args);self.assertEqual((code,out),(1,""))
    def test_policy_time_invalid_before_source_open(self):
        for time,age in [(NOW,None),(NOW,True),(NOW,-1),("invalid",60)]:
            with patch.object(caller.os,"open",side_effect=AssertionError("read")):
                with self.assertRaises(service_association.ServiceAssociationError):self.evaluate(time,age)
    def test_freshness_exact_boundary_and_zero(self):
        self.assertEqual(self.evaluate(age=0)["association_count"],1)
        self.assertEqual(self.evaluate(time="2026-10-12T12:01:00Z")["association_count"],1)
    def test_stale_future_fail_without_output(self):
        for time,code in [("2026-10-12T12:01:00.000001Z","SNAPSHOT_STALE"),("2026-10-12T11:59:59Z","SNAPSHOT_FUTURE")]:
            args=self.args();args[3]=time
            self.assertEqual(self.cli(args),(1,"",code+"\n"))
    def test_corrupt_duplicate_keys_invalid_encoding(self):
        for value in [b"{",b'{"updated":"a","updated":"b"}',b"\xff"]:
            self.path.write_bytes(value)
            self.assertEqual(self.cli(self.args()),(1,"","SNAPSHOT_JSON_INVALID\n"))
    def test_missing_file_safe_error(self):
        self.path.unlink();self.assertEqual(self.cli(self.args()),(1,"","SNAPSHOT_READ_FAILED\n"))
    def test_directory_unsafe(self):
        with self.assertRaises(caller.CallerError) as e:caller.evaluate_file(self.path.parent,NOW,60)
        self.assertEqual(str(e.exception),"SNAPSHOT_FILE_UNSAFE")
    def test_symlink_unsafe_without_native_privilege_requirement(self):
        with patch.object(Path,"lstat") as observed:
            observed.return_value.st_mode=0o120777
            with self.assertRaises(caller.CallerError) as e:self.evaluate()
        self.assertEqual(str(e.exception),"SNAPSHOT_FILE_UNSAFE")
    def test_bound_prevents_truncation_promotion(self):
        with patch.object(caller,"MAX_SNAPSHOT_BYTES",10):
            with self.assertRaises(caller.CallerError) as e:self.evaluate()
        self.assertEqual(str(e.exception),"SNAPSHOT_FILE_LIMIT_EXCEEDED")
    def test_opened_version_must_agree(self):
        real=caller.os.fstat
        def fake(fd):
            from types import SimpleNamespace
            v=real(fd);return SimpleNamespace(st_mode=v.st_mode,st_dev=v.st_dev,st_ino=v.st_ino+1)
        with patch.object(caller.os,"fstat",side_effect=fake):
            with self.assertRaises(caller.CallerError) as e:self.evaluate()
        self.assertEqual(str(e.exception),"SNAPSHOT_FILE_UNSAFE")
    def test_in_place_concurrent_change_fails(self):
        real=caller.os.fstat;count=[]
        def fake(fd):
            v=real(fd);count.append(v)
            if len(count)==2:
                from types import SimpleNamespace
                return SimpleNamespace(st_size=v.st_size+1,st_mtime_ns=v.st_mtime_ns,st_ctime_ns=v.st_ctime_ns)
            return v
        with patch.object(caller.os,"fstat",side_effect=fake):
            with self.assertRaises(caller.CallerError) as e:self.evaluate()
        self.assertEqual(str(e.exception),"SNAPSHOT_FILE_CHANGED")
    def test_invalid_output_never_emitted(self):
        with patch.object(caller,"resolve_service_associations",return_value={}):
            code,out,err=self.cli(self.args())
        self.assertEqual((code,out),(1,""))
    def test_invalid_input_global_contract_no_result(self):
        self.path.write_text("{}");code,out,err=self.cli(self.args())
        self.assertEqual((code,out,err),(1,"","SNAPSHOT_INVALID\n"))
    def test_empty_does_not_assert_health_or_success(self):
        self.value["services"]=[];self.path.write_text(json.dumps(self.value));result=self.evaluate()
        self.assertEqual((result["association_count"],result["rejection_count"]),(0,0))
        for word in ["collection_success","healthy","outage","service_absent"]:self.assertNotIn(word,json.dumps(result))
    def test_unrelated_valid_service_not_corrupted_by_rejection(self):
        self.value["services"].append(None);self.path.write_text(json.dumps(self.value))
        result=self.evaluate();self.assertEqual((result["association_count"],result["rejection_count"]),(1,1))
    def test_private_no_raw_labels_addresses(self):
        out=json.dumps(self.evaluate())
        for term in ["synthetic label","192.0.2.1","02:00:00:00:00:01","health_status"]:self.assertNotIn(term,out)
    def test_no_network_subprocess_environment_state_writer(self):
        with patch("socket.socket",side_effect=AssertionError("network")),patch("subprocess.run",side_effect=AssertionError("subprocess")),patch("os.getenv",side_effect=AssertionError("environment")),patch("hioc.core.state.StateStore.write_json",side_effect=AssertionError("write")):
            self.assertEqual(self.evaluate()["association_count"],1)
    def test_restart_has_no_prior_state_or_lkg(self):
        first=self.evaluate();self.assertEqual(self.evaluate(),first)
        self.assertEqual(list(self.path.parent.iterdir()),[self.path])
    def test_runtime_producer_and_resolver_unchanged(self):
        for p in ["pi4/bin/hioc-inventory-engine.py","pi4/lib/hioc/inventory.py","pi4/lib/hioc/mqtt.py","pi4/lib/hioc/service_association.py","pi4/install_pi4.sh","pi4/lib/hioc/core/state.py"]:
            self.assertEqual(raw(p),git("show",BASE+":"+p),p)
    def test_imports_no_config_ingestion_writer(self):
        tree=ast.parse(SCRIPT.read_text())
        names={x.name for n in tree.body if isinstance(n,ast.Import) for x in n.names}
        self.assertEqual(names,{"argparse","json","os","re","stat","sys"})
        for name in ["write_json","MqttClient","load_config","discover_inventory"]:self.assertNotIn(name,SCRIPT.read_text())

class CallerGovernanceTests(unittest.TestCase):
    def test_exact_current_contract(self):caller_successor()
    def test_reject_authority_policy_writer_expansion(self):
        for field,value in [("production_authorized",True),("producer_hook_added",True),("persistence_added",True),("policy_default",60),("snapshot_age_policy",60)]:
            r=copy.deepcopy(caller_successor());r[field]=value
            with self.assertRaises(ValueError):validate_caller_record(r,schema_for(r))
    def test_reject_open_schema_stale_identity(self):
        r=caller_successor();s=schema_for(r);s["additionalProperties"]=True
        with self.assertRaises(ValueError):validate_caller_record(r,s)
        r=copy.deepcopy(r);r["artifacts"][0]["sha256"]="0"*64
        with self.assertRaises(ValueError):validate_caller_record(r,schema_for(r))
    def test_reject_out_of_scope_binding(self):
        with self.assertRaises(ValueError):caller_current_binding("pi4/bin/hioc-inventory-engine.py")
    def test_runtime_guard_rejects_existing_source_change(self):
        original=git
        def changed(*a):
            if a[:2]==("diff","--name-only"):return b"pi4/bin/hioc-inventory-engine.py\n"
            return original(*a)
        with patch.dict(globals(),git=changed),self.assertRaises(ValueError):
            assert_historical_runtime_tree("c7db29f795909d7926e36c02f1166034bcebb8b0",["pi4"])
    def test_runtime_guard_rejects_unapproved_addition(self):
        original=git
        def changed(*a):
            if a[:2]==("diff","--name-only"):return b"pi4/lib/hioc/unapproved.py\n"
            return original(*a)
        with patch.dict(globals(),git=changed),self.assertRaises(ValueError):
            assert_historical_runtime_tree("c7db29f795909d7926e36c02f1166034bcebb8b0",["pi4"])
    def test_current_sequence_history_preserved(self):
        assert_caller_sequence(raw("docs/HIOC_MASTER_PLAN.md").decode())
        self.assertEqual(caller_successor()["private_state_requirement"],"DEFERRED_NOT_REQUIRED_FOR_OFFLINE_CALLER")

if __name__=="__main__":unittest.main()
