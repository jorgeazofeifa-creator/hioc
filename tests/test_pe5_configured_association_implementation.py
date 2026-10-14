"""PE-5.3 controlled repository fixtures. POSIX sync/metadata/flock are injected on Windows."""
import ast
import copy
import hashlib
import importlib.util
import io
import json
import os
import socket
import stat
import subprocess
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import timedelta
from functools import lru_cache
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
from hioc import configured_association as m
from hioc import configured_association_store as storage
from hioc.configured_association_schemas import schemas
from test_pe5_local_service_association import snapshot, device, service, NOW, OWNER, SERVICE, SECOND_OWNER, SECOND_MAC
BASE="72e878f9c0c8f5d3fe6357979e045943f3cf9d34"
RECORD="governance/pe5/pe5-configured-association-implementation.json"
SCHEMA=RECORD.replace(".json",".schema.json")

def git(*args):return subprocess.check_output(["git","--no-optional-locks",*args],cwd=ROOT,env=dict(os.environ,GIT_OPTIONAL_LOCKS="0"),stderr=subprocess.PIPE)
def raw(p):return (ROOT/p).read_bytes().replace(b"\r\n",b"\n")
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def closed(v):
    if type(v) is dict:return dict(type="object",additionalProperties=False,required=sorted(v),properties={k:closed(x) for k,x in sorted(v.items())})
    if type(v) is list:return dict(type="array",minItems=len(v),maxItems=len(v),prefixItems=[closed(x) for x in v],items=False)
    return dict(const=v)
def schema_for(r):return {"$schema":"https://json-schema.org/draft/2020-12/schema","title":"PE-5.3 configured relationship repository implementation",**closed(r)}
def require(v,msg):
    if not v:raise ValueError(msg)

def validate_implementation(r,s,identities=True):
    require(s==schema_for(r),"exact implementation schema")
    require(r["predecessor_commit"]==BASE and r["checkpoint"]=="PE-5.3" and r["status"]=="COMPLETE_REPOSITORY_IMPLEMENTATION","authority")
    require(r["next_checkpoint"]=="PE-5.4 - PI3 Release Source Synchronization","sequence")
    frozen=json.loads(git("show",BASE+":governance/pe5/pe5-atomic-durability-contract-correction.json"))
    require(r["contract_sha256"]==sha(m.canonical(frozen["contract"])),"frozen authority")
    require(schemas()=={k:frozen[k] for k in ("input_schema","output_schema","metadata_schema")},"runtime schemas")
    require(all(v is False for v in r["production_activity"].values()) and r["recurring_activated"] is False,"production authority")
    require(r["deployment_requirements"]["language_floor"]=="CPython 3.10" and r["deployment_requirements"]["owner"]=="jazofv1" and r["deployment_requirements"]["activation"]=="DISABLED_THROUGH_PE5_5" and r["deployment_requirements"]["source_provisioned"] is False,"disabled deployment")
    require(len(r["required_existing_dependencies"])==8 and all(i in r["protected"] for i in r["required_existing_dependencies"]),"dependency authority")
    require(len(r["checklist"])==46 and {x["label"] for x in r["checklist"]}==set(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")+["A"+x for x in "ABCDEFGHIJKLMNOPQRST"]),"coverage")
    if r.get("defect_correction"):
        c=r["defect_correction"]
        require(c["baseline_commit"]=="348f9787ae0ab364570a2ba07ada9527fc8db0e2" and c["checkpoint"]=="PE-5.6","correction authority")
        require(c["retry_performed"] is False and c["corrected_production_deployment_established"] is False,"production remains unknown")
        require(c["changed_payload_sources"]==["pi4/lib/hioc/configured_association_store.py"],"bounded payload")
    if r.get("production_validation"):
        c=r["production_validation"]
        require(c["classification"]==("HISTORICAL_INTENTIONALLY_PRESERVED" if r.get("scheduler_activation") else "CURRENT") and c["checkpoint"]=="PE-5.6" and c["status"]=="COMPLETE/PASS","closure authority")
        require(c["evidence_authority"]=="OPERATOR_SUPPLIED" and c["implementation_commit"]=="4990c62afbce22a804229f3cb8329986741067a6","evidence scope")
        require(c["next_checkpoint"]=="PE-5.7 - Conditional Execution Activation" and c["pe5_7_started"] is False and c["scheduler_active"] is False and c["recurring_execution_accepted"] is False,"closed bounded execution only")
        require(c["corrected_initialization"]["execution_count"]==1 and c["bounded_composer"]["execution_count"]==1 and c["bounded_composer"]["accepted_count"]==1 and c["bounded_composer"]["rejected_count"]==0,"bounded observations")
        require(c["configured_branch"]["association"]["relationship_id"]==m.relationship_id(c["configured_branch"]["association"]),"observed relationship identity")
        require(all(v["failures"]==v["errors"]==0 for v in c["validation"]["results"].values()),"required validation")
    if r.get("scheduler_activation"):
        a=r["scheduler_activation"]
        require(a["classification"]=="CURRENT" and a["checkpoint"]=="PE-5.7" and a["status"]=="COMPLETE/PASS","activation closure authority")
        require(a["evidence_authority"]=="OPERATOR_SUPPLIED" and a["predecessor_closure_commit"]=="21ca5f676bb96d376b3a6f098decfecfe3c6ea49","activation predecessor")
        require(a["next_checkpoint"]=="PE-5.8 - Operational Evidence and Independent Production Acceptance" and a["recurring_execution_active"] is True and a["pe5_8_started"] is False and a["natural_cycle_evidence_established"] is False and a["recurring_operational_acceptance_established"] is False,"activation versus operational acceptance")
        e=a["activation"];post=a["post_activation"]
        require(e["marker_count"]==e["entry_count"]==post["marker_count"]==post["entry_count"]==1 and post["unexpected_pe5_entry_count"]==0,"single accepted cron entry")
        require(e["schedule"]=="2,17,32,47 * * * *" and e["command"]=="/usr/bin/python3 /home/jazofv1/hioc/pi4/bin/hioc-compose-service-associations.py","frozen execution model")
        require(e["after_sha256"]==post["crontab_sha256"] and e["composer_executed_manually"] is False and e["installer_executed"] is False and e["mqtt_accessed"] is False,"bounded activation evidence")
    if identities:
        scope=set(r["authorized_paths"])
        require(scope=={i["path"] for i in r["artifacts"]}|{RECORD,SCHEMA},"scope")
        changed=set(git("diff","--name-only",BASE).decode().splitlines())|set(git("ls-files","--others","--exclude-standard").decode().splitlines())
        require(changed==scope,"unexpected path")
        for i in r["artifacts"]:
            b=raw(i["path"]);require((sha(b),blob(b))==(i["sha256"],i["git_blob"]),"implementation identity: "+i["path"])
        for i in r["protected"]:
            b=git("show",BASE+":"+i["path"])
            require(b==raw(i["path"]) and (sha(b),blob(b))==(i["sha256"],i["git_blob"]),"immutable predecessor: "+i["path"])
        for item in r["payload"]:
            b=raw(item["source"]);require((sha(b),blob(b))==(item["sha256"],item["git_blob"]),"payload binding")
            require(item["owner"]=="jazofv1" and item["destination"].startswith("/home/jazofv1/hioc/"),"payload ownership")
    return r

@lru_cache(maxsize=1)
def implementation_successor():
    b,sb=raw(RECORD),raw(SCHEMA);r,s=json.loads(b),json.loads(sb)
    require(b==m.canonical(r) and sb==m.canonical(s),"canonical implementation")
    return validate_implementation(r,s)

def implementation_binding(path):
    item=next((x for x in implementation_successor()["artifacts"] if x["path"]==path),None)
    if item:require((sha(raw(path)),blob(raw(path)))==(item["sha256"],item["git_blob"]),"current implementation binding")
    return item

def assert_implementation_sequence(text):
    implementation_binding("docs/HIOC_MASTER_PLAN.md")
    section=text.split("## Next Planned Task",1)[1].split("### Historical",1)[0]
    if implementation_successor().get("scheduler_activation"):
        require(section.strip().startswith("### PE-5.8 - Operational Evidence and Independent Production Acceptance"),"next operational evidence checkpoint")
        require("PE5_7_STATUS=COMPLETE/PASS" in section and "RECURRING_EXECUTION_ACTIVE=TRUE" in section and "PE5_8_STARTED=FALSE" in section and "Separate authorization is required for PE-5.8" in section,"activation closure sequence")
        return
    if implementation_successor().get("production_validation"):
        require(section.strip().startswith("### PE-5.7 - Conditional Execution Activation"),"next activation checkpoint only")
        require("PE5_6_STATUS=COMPLETE/PASS" in section and "PE5_7_STARTED=FALSE" in section and "RECURRING_EXECUTION_ACTIVE=FALSE" in section and "Separate authorization is required for PE-5.7" in section,"bounded closure sequence")
        return
    if implementation_successor().get("defect_correction"):
        require(section.strip().startswith("### PE-5.6 - Bounded Mapping and Storage Production Validation"),"current corrected checkpoint")
        require("PE5_6_STATUS=BLOCKED_PENDING_CORRECTED_DEPLOYMENT_AND_SEPARATE_RETRY" in section and "PE5_7_STARTED=FALSE" in section,"no validation closure or activation")
        return
    require(section.strip().startswith("### PE-5.4 - PI3 Release Source Synchronization"),"current next task")
    require("PE5_3_STATUS=COMPLETE_REPOSITORY_IMPLEMENTATION" in section and "PE5_4_STARTED=FALSE" in section and "Separate authorization is required" in section,"lifecycle gate")


def source(rows=None, revision=1):
    row=dict(mapping_id="map_"+"1"*32,endpoint_id="me_"+"2"*32,device_id=OWNER,service_id=None)
    return dict(schema_version="1.0",source_id="operator_mqtt_v1",revision=revision,mappings=[row] if rows is None else rows)

class FakePosix(storage.PosixFS):
    """Actual temporary-file read/write/fsync/replace. Directory sync and POSIX
    metadata/flock are simulated, not native crash/ownership/locking evidence."""
    def __init__(self):
        self.overrides={};self.fds={};self.trace=[];self.fault=None;self.busy=False
        self.after_replace=None;self.before_open=None
    def info(self,s,path,directory=False):
        v={k:getattr(s,k) for k in ("st_dev","st_ino","st_size","st_mtime_ns","st_ctime_ns","st_mode","st_uid","st_gid","st_nlink")}
        v.update(st_mode=(stat.S_IFDIR|0o700) if directory else (s.st_mode & ~0o777)|0o600,st_uid=1000,st_gid=1000)
        v.update(self.overrides.get(str(path),{}))
        return SimpleNamespace(**v)
    def directory(self,path):
        path=Path(path)
        if path.is_symlink() or not path.is_dir():raise OSError("unsafe synthetic directory")
        return path
    def child_directory(self,d,name):
        p=d/name
        if p.is_symlink():raise OSError("unsafe synthetic symlink")
        if not p.exists():raise FileNotFoundError(str(p))
        if not p.is_dir():raise NotADirectoryError(str(p))
        return p
    def mkdir(self,d,name):
        self.trace.append("BOOTSTRAP_MKDIR")
        if self.fault=="BOOTSTRAP_MKDIR":raise OSError("synthetic mkdir failure")
        (d/name).mkdir(mode=0o700)
    def statdir(self,path):return self.info(path.stat(),path,True)
    def close_dir(self,fd):pass
    def statat(self,d,name):
        p=d/name;return self.info(p.lstat(),p)
    def openat(self,d,name,flags,mode=0o600):
        p=d/name
        if self.before_open:self.before_open(p)
        fd=os.open(p,flags|os.O_BINARY,mode);self.fds[fd]=p;return fd
    def fstat(self,fd):
        value=self.info(os.fstat(fd),self.fds[fd])
        # Windows path stat exposes creation time while fstat exposes change time.
        # This injected POSIX fixture uses one consistent synthetic ctime.
        if os.name=="nt":value.st_ctime_ns=self.fds[fd].lstat().st_ctime_ns
        return value
    def chmod(self,fd):pass
    def sync(self,fd,phase):
        self.trace.append(phase)
        if phase==self.fault:raise OSError("synthetic EIO")
        os.fsync(fd)
    def syncdir(self,fd,phase):
        self.trace.append(phase)
        if phase==self.fault:raise OSError("synthetic EIO")
    def replace(self,d,before,after,phase):
        self.trace.append(phase)
        if phase==self.fault:raise OSError("synthetic EIO")
        os.replace(d/before,d/after)
        if self.after_replace:self.after_replace(phase,d/after)
    def unlink(self,d,name):os.unlink(d/name)
    def flock(self,fd,unlock=False):
        if unlock:self.busy=False;return
        if self.busy:raise BlockingIOError()
        self.busy=True

class Fixture:
    def __init__(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        for p in ["config/enrichment","state/enrichment/service_associations","state/inventory"]:(self.root/p).mkdir(parents=True)
        self.fs=FakePosix();self.store=storage.Store(self.root,owner_uid=1000,fs=self.fs)
        (self.root/storage.INVENTORY).write_bytes(m.canonical(snapshot()))
    def close(self):self.tmp.cleanup()
    def install(self,value=None):
        return self.store.install_source(source() if value is None else value,approved=True,initialize=True)
    def primary(self,domain):return self.root/storage.DOMAINS[domain][0]
    def meta(self,domain):return json.loads((self.root/storage.DOMAINS[domain][1]).read_bytes())

class ConfiguredResolutionTests(unittest.TestCase):
    def assert_code(self,code,call):
        with self.assertRaises(m.AssociationError) as caught:call()
        self.assertEqual(caught.exception.code,code)
    def test_frozen_schemas_exact(self):
        r=json.loads(git("show",BASE+":governance/pe5/pe5-atomic-durability-contract-correction.json"))
        self.assertEqual(schemas(),{k:r[k] for k in schemas()})
    def test_valid_configured_opaque_strong_owner_private_provenance(self):
        inv=snapshot();before=copy.deepcopy(inv);r=m.compose(inv,source(),NOW)
        self.assertEqual(inv,before);a=r["configured"]["associations"][0]
        self.assertEqual(a["device_id"],OWNER);self.assertEqual(a["source_kind"],"configured_mqtt")
        self.assertEqual(a["source_revision"],1);self.assertEqual(a["source_sha256"],m.digest(source()))
        self.assertEqual(a["rule_id"],"declared_endpoint_device_v1");m.validate_handoff(r,inv,source(),NOW)
    def test_preserves_exact_local_foundation(self):
        r=m.compose(snapshot(),source(),NOW)
        self.assertEqual(r["local"],m.local.resolve_service_associations(snapshot(),NOW,2100))
    def test_relationship_id_exact_domain_and_revision_invariance(self):
        x=source()["mappings"][0]
        expected="mqra_"+hashlib.sha256(json.dumps(["configured_mqtt_v1","operator_mqtt_v1",x["endpoint_id"],x["device_id"],None,"endpoint_to_device"],separators=(",",":")).encode()).hexdigest()
        self.assertEqual(m.relationship_id(x),expected)
        self.assertEqual(m.compose(snapshot(),source(revision=2),NOW)["configured"]["associations"][0]["relationship_id"],expected)
    def test_deterministic_multirow_sorting_and_fan_in(self):
        rows=[dict(source()["mappings"][0],mapping_id="map_"+format(i,"032x"),endpoint_id="me_"+format(i,"032x")) for i in range(1,9)]
        a=m.compose(snapshot(),source(rows),NOW);b=m.compose(snapshot(),source(rows[::-1]),NOW)
        self.assertEqual([x["relationship_id"] for x in a["configured"]["associations"]],[x["relationship_id"] for x in b["configured"]["associations"]])
        self.assertEqual(len(a["configured"]["associations"]),8)
    def test_explicit_empty_source_is_known_empty(self):
        r=m.compose(snapshot(),source([]),NOW);self.assertEqual(r["configured"]["state"],"VALID");self.assertEqual(r["configured"]["candidate_count"],0)
    def test_absent_or_invalid_source_keeps_independent_local(self):
        for value,code in [(None,"SOURCE_ABSENT"),({}, "SOURCE_SCHEMA_INVALID")]:
            r=m.compose(snapshot(),value,NOW);self.assertEqual(r["state"],"VALID");self.assertIsNotNone(r["local"])
            self.assertEqual(r["configured"]["error_code"],code);self.assertEqual(r["changes"],m.no_changes())
    def test_source_revision_integer_bounds_and_no_bool(self):
        for rev in [True,0,-1,9007199254740992,1.5,"1"]:
            with self.subTest(revision=rev):self.assert_code("SOURCE_SCHEMA_INVALID",lambda:m.validate_source(source(revision=rev)))
    def test_closed_source_rejects_secrets_topics_authority_fields(self):
        for field in ["password","token","topic","client_id","ip","mac","health","observed_at","source_kind","url"]:
            value=source();value["mappings"][0][field]="forbidden"
            with self.subTest(field=field):self.assert_code("SOURCE_SCHEMA_INVALID",lambda:m.validate_source(value))
    def test_unknown_schema_and_identifiers(self):
        for field in ["mapping_id","endpoint_id","device_id","service_id"]:
            value=source();value["mappings"][0][field]="name-or-address"
            with self.subTest(field=field):self.assert_code("SOURCE_SCHEMA_INVALID",lambda:m.validate_source(value))
        value=source();value["schema_version"]="2.0";self.assert_code("SOURCE_SCHEMA_INVALID",lambda:m.validate_source(value))
    def test_duplicate_rows_ids_and_endpoints(self):
        x=source()["mappings"][0]
        for rows in [[x,x],[x,dict(x,endpoint_id="me_"+"3"*32)],[x,dict(x,mapping_id="map_"+"3"*32)]]:
            with self.subTest(rows=rows):self.assert_code("SOURCE_DUPLICATE",lambda:m.validate_source(source(rows)))
    def test_conflicting_endpoint_rejects_whole_source(self):
        x=source()["mappings"][0];rows=[x,dict(x,mapping_id="map_"+"3"*32,device_id=SECOND_OWNER)]
        self.assert_code("SOURCE_CONFLICT",lambda:m.validate_source(source(rows)))
        self.assertEqual(m.compose(snapshot(),source(rows),NOW)["configured"]["candidate_count"],0)
    def test_strict_json_duplicate_keys_nan_encoding_and_size(self):
        for data in [b'{"a":1,"a":2}',b'{"a":NaN}',b'\xff',b"{",b'{"a":Infinity}']:
            with self.subTest(data=data):self.assert_code("SOURCE_SCHEMA_INVALID",lambda:m.strict_json(data,262144))
        self.assert_code("SOURCE_SCHEMA_INVALID",lambda:m.strict_json(b" "*262145,262144))
    def test_source_array_bound(self):
        x=source()["mappings"][0];rows=[dict(x,mapping_id="map_"+format(i,"032x"),endpoint_id="me_"+format(i,"032x")) for i in range(4097)]
        self.assert_code("SOURCE_SCHEMA_INVALID",lambda:m.validate_source(source(rows)))
    def test_device_rejections(self):
        cases=[
            (snapshot(devices=[]),"MISSING_DEVICE"),
            (snapshot(devices=[dict(device(),mac="")]),"WEAK_DEVICE"),
            (snapshot(devices=[device(),device()]),"AMBIGUOUS_DEVICE"),
            (snapshot(devices=[device(),device(device_id=SECOND_OWNER)]),"MAC_COLLISION"),
            (snapshot(devices=[device(mac=SECOND_MAC,device_id=OWNER)]),"DEVICE_ID_MISMATCH")]
        for inv,code in cases:
            with self.subTest(code=code):
                r=m.compose(inv,source(),NOW);self.assertEqual(r["configured"]["associations"],[])
                self.assertEqual(r["configured"]["rejections"],[dict(mapping_id=source()["mappings"][0]["mapping_id"],code=code)])
    def test_service_reference_rejections_and_acceptance(self):
        x=source()["mappings"][0];x["service_id"]=SERVICE
        cases=[(snapshot(services=[]),"MISSING_SERVICE"),(snapshot(services=[service(),service()]),"AMBIGUOUS_SERVICE"),
               (snapshot(services=[service(owner=SECOND_OWNER)],devices=[device(),device(SECOND_MAC)]),"SERVICE_OWNER_MISMATCH")]
        for inv,code in cases:
            with self.subTest(code=code):self.assertEqual(m.compose(inv,source([x]),NOW)["configured"]["rejections"][0]["code"],code)
        self.assertEqual(len(m.compose(snapshot(),source([x]),NOW)["configured"]["associations"]),1)
    def test_inventory_clock_freshness_and_deadline(self):
        now=m.local._time(NOW,"CLOCK_INVALID")
        r=m.compose(snapshot(),source(),NOW);self.assertEqual(m.local._time(r["valid_until"],"CLOCK_INVALID")-now,timedelta(seconds=1200))
        for offset,code in [(1,"INVENTORY_FUTURE"),(-2100,"INVENTORY_STALE"),(-2101,"INVENTORY_STALE")]:
            inv=snapshot();inv["updated"]=m.local._time_text(now+timedelta(seconds=offset))
            with self.subTest(offset=offset):
                x=m.compose(inv,source(),NOW);self.assertEqual(x["state"],"UNAVAILABLE");self.assertEqual(x["configured"]["error_code"],code);self.assertEqual(x["valid_until"],x["evaluated_at"])
        self.assert_code("CLOCK_INVALID",lambda:m.compose(snapshot(),source(),"invalid"))
    def test_backward_clock_does_not_publish(self):
        prior=m.compose(snapshot(),source(),NOW)
        self.assert_code("CLOCK_INVALID",lambda:m.compose(snapshot(),source(),"2026-10-12T11:59:59Z",prior))
    def test_revision_rollback_equal_changed_and_equal_identical(self):
        anchor={"sha256":m.digest(source()),"source_revision":1}
        m.check_revision(source(),[anchor]);m.check_revision(source(revision=2),[anchor])
        value=source();value["mappings"]=[]
        self.assert_code("SOURCE_REVISION_CONFLICT",lambda:m.check_revision(value,[anchor]))
        self.assert_code("SOURCE_REVISION_ROLLBACK",lambda:m.check_revision(source(),[dict(anchor,source_revision=2)]))
    def test_handoff_expiry_input_change_source_change(self):
        r=m.compose(snapshot(),source(),NOW)
        self.assert_code("PRIOR_STATE_INVALID",lambda:m.validate_handoff(r,snapshot(),source(),r["valid_until"]))
        inv=snapshot();inv["summary"]={"changed":True}
        self.assert_code("INVENTORY_INVALID",lambda:m.validate_handoff(r,inv,source(),NOW))
        self.assert_code("SOURCE_CHANGED",lambda:m.validate_handoff(r,snapshot(),source(revision=2),NOW))
    def test_output_semantic_corruption_is_rejected(self):
        for mutate in [
            lambda x:x["configured"]["associations"][0].update(relationship_id="mqra_"+"0"*64),
            lambda x:x["configured"].update(candidate_count=2),
            lambda x:x["configured"]["associations"][0].update(source_revision=2),
            lambda x:x.update(valid_until=x["evaluated_at"]),
            lambda x:x["local"].update(max_snapshot_age_seconds=1),
            lambda x:x["changes"].update(added_count=1)]:
            x=m.compose(snapshot(),source(),NOW);mutate(x)
            with self.subTest(mutation=mutate):self.assert_code("PRIOR_STATE_INVALID",lambda:m.validate_envelope(x))
    def test_current_comparison_and_unavailable_do_not_fabricate_removals(self):
        prior=m.compose(snapshot(),source(),NOW);x=m.compose(snapshot(),source(),NOW,prior)
        self.assertTrue(x["changes"]["baseline"]);self.assertEqual(x["changes"]["removed_count"],0)
        x=m.compose(snapshot(),None,NOW,prior);self.assertFalse(x["changes"]["baseline"])
    def test_bounded_change_fields_checked(self):
        r=m.compose(snapshot(),source(),NOW);r["changes"]=dict(baseline=True,added=["mqra_"+format(i,"064x") for i in range(64)],removed=[],added_count=70,removed_count=0,truncated=True)
        m.validate_envelope(r)
        r["changes"]["truncated"]=False;self.assert_code("PRIOR_STATE_INVALID",lambda:m.validate_envelope(r))
    def test_network_subprocess_and_input_authority_untouched(self):
        inv=snapshot();before=copy.deepcopy(inv)
        with patch.object(socket,"socket",side_effect=AssertionError("network")),patch.object(subprocess,"run",side_effect=AssertionError("process")):
            r=m.compose(inv,source(),NOW)
        self.assertEqual(inv,before)
        text=json.dumps(r["configured"])
        for field in ["health_status","role_suggestion","metadata_quality","192.0.2.1","synthetic label","02:00:00"]:self.assertNotIn(field,text)

class PersistenceTests(unittest.TestCase):
    def setUp(self):self.f=Fixture();self.addCleanup(self.f.close)
    def assert_error(self,call,code=None,phase=None):
        with self.assertRaises(m.AssociationError) as caught:call()
        if code:self.assertEqual(caught.exception.code,code)
        if phase:self.assertEqual(caught.exception.phase,phase)
        return caught.exception
    def test_approval_and_explicit_initialization_required(self):
        self.assert_error(lambda:self.f.store.install_source(source()),"WRITE_FAILED","OPERATOR_APPROVAL_REQUIRED")
        self.assert_error(lambda:self.f.store.install_source(source(),approved=True),"WRITE_FAILED","RECOVERY_REQUIRED")
        self.f.install();self.assertEqual(self.f.meta(storage.SOURCE)["state"],"CONFIRMED")
    def test_source_output_separation_and_confirmed_handoff(self):
        self.f.install();before=self.f.primary(storage.SOURCE).read_bytes();r=self.f.store.composer(NOW)
        self.assertEqual(self.f.primary(storage.SOURCE).read_bytes(),before)
        self.assertEqual(self.f.meta(storage.OUTPUT)["confirmed"]["sha256"],m.digest(r))
        self.assertEqual(self.f.store.read_handoff(NOW),r)
    def test_source_absence_valid_local_private_output(self):
        r=self.f.store.composer(NOW)
        self.assertEqual(r["configured"]["error_code"],"SOURCE_ABSENT")
        self.assertIsNotNone(self.f.store.read_handoff(NOW)["local"])
    def test_exact_atomic_order_and_one_primary_replace(self):
        self.f.install();self.f.fs.trace=[];self.f.store.composer(NOW);t=self.f.fs.trace
        self.assertLess(t.index("PENDING_PARENT"),t.index("PRIMARY_FILE"))
        self.assertLess(t.index("PRIMARY_FILE"),t.index("PRIMARY_REPLACE"))
        self.assertLess(t.index("PRIMARY_REPLACE"),t.index("PRIMARY_PARENT"))
        self.assertLess(t.index("PRIMARY_PARENT"),t.index("CONFIRMATION_REPLACE"))
        self.assertEqual(t.count("PRIMARY_REPLACE"),1)
    def test_pre_replace_failures_preserve_old_and_clean_owned_temp(self):
        self.f.install();self.f.store.composer(NOW);old=self.f.primary(storage.OUTPUT).read_bytes()
        for phase in ["PENDING_FILE","PENDING_REPLACE","PENDING_PARENT","PRIMARY_FILE","PRIMARY_REPLACE"]:
            with self.subTest(phase=phase):
                # Restore a separately recertified fixture after each pending failure.
                self.f.fs.fault=phase
                self.assert_error(lambda:self.f.store.composer(NOW),"WRITE_FAILED","PRE_REPLACEMENT_FAILURE")
                self.assertEqual(self.f.primary(storage.OUTPUT).read_bytes(),old)
                self.assertFalse(list(self.f.primary(storage.OUTPUT).parent.glob(".hioc-*.tmp")))
                self.f.fs.fault=None;self.f.store.recertify(storage.OUTPUT,NOW,True)
    def test_post_replace_parent_failure_indeterminate_no_rollback(self):
        self.f.install();old=self.f.store.composer(NOW);old_bytes=self.f.primary(storage.OUTPUT).read_bytes()
        self.f.fs.fault="PRIMARY_PARENT";self.f.fs.trace=[]
        later=m.local._time_text(m.local._time(NOW,"CLOCK_INVALID")+timedelta(seconds=1))
        self.assert_error(lambda:self.f.store.composer(later),"WRITE_FAILED","INDETERMINATE_DURABILITY")
        self.assertNotEqual(self.f.primary(storage.OUTPUT).read_bytes(),old_bytes)
        meta=self.f.meta(storage.OUTPUT);self.assertEqual(meta["state"],"PENDING");self.assertEqual(meta["confirmed"]["sha256"],m.digest(old))
        self.assertEqual(self.f.fs.trace.count("PRIMARY_REPLACE"),1);self.assertNotIn("CONFIRMATION_REPLACE",self.f.fs.trace)
        self.assert_error(lambda:self.f.store.read_handoff(later),"WRITE_FAILED","RECOVERY_REQUIRED")
        self.f.fs.fault=None;self.assert_error(lambda:self.f.store.composer(later),"PRIOR_STATE_INVALID","RECOVERY_REQUIRED")
    def test_explicit_candidate_recovery_no_primary_replace_or_time_refresh(self):
        self.f.install();self.f.store.composer(NOW);self.f.fs.fault="PRIMARY_PARENT"
        self.assert_error(lambda:self.f.store.composer(NOW));before=self.f.primary(storage.OUTPUT).read_bytes()
        self.f.fs.fault=None;self.f.fs.trace=[]
        self.f.store.recertify(storage.OUTPUT,NOW,True)
        self.assertEqual(self.f.primary(storage.OUTPUT).read_bytes(),before)
        self.assertNotIn("PRIMARY_REPLACE",self.f.fs.trace);self.assertEqual(self.f.meta(storage.OUTPUT)["state"],"CONFIRMED")
    def test_recovery_approval_expiry_and_unmatched_bytes_stop(self):
        self.f.install();self.f.store.composer(NOW)
        self.assert_error(lambda:self.f.store.recertify(storage.OUTPUT,NOW,False),"WRITE_FAILED","OPERATOR_APPROVAL_REQUIRED")
        self.assert_error(lambda:self.f.store.recertify(storage.OUTPUT,"2026-10-12T12:21:00Z",True),"PRIOR_STATE_INVALID")
        value=json.loads(self.f.primary(storage.OUTPUT).read_bytes());value["evaluated_at"]="2026-10-12T12:00:01Z"
        self.f.primary(storage.OUTPUT).write_bytes(m.canonical(value))
        self.assert_error(lambda:self.f.store.recertify(storage.OUTPUT,NOW,True))
    def test_confirmation_metadata_failure_does_not_report_success(self):
        self.f.install();self.f.store.composer(NOW)
        for phase in ["CONFIRMATION_FILE","CONFIRMATION_REPLACE","CONFIRMATION_PARENT"]:
            with self.subTest(phase=phase):
                self.f.fs.fault=phase;self.assert_error(lambda:self.f.store.composer(NOW),"WRITE_FAILED","CONFIRMATION_METADATA_UNCONFIRMED")
                self.f.fs.fault=None;self.f.store.recertify(storage.OUTPUT,NOW,True)
    def test_confirmation_surviving_witness_requires_anchor_resync(self):
        self.f.install();self.f.fs.fault="CONFIRMATION_PARENT"
        self.assert_error(lambda:self.f.store.composer(NOW),"WRITE_FAILED","CONFIRMATION_METADATA_UNCONFIRMED")
        self.assertEqual(self.f.meta(storage.OUTPUT)["state"],"CONFIRMED")
        self.f.fs.fault=storage.OUTPUT+"_ANCHOR_PARENT";self.f.fs.trace=[]
        self.assert_error(lambda:self.f.store.composer(NOW));self.assertNotIn("PRIMARY_REPLACE",self.f.fs.trace)
    def test_missing_malformed_metadata_blocks_no_adoption(self):
        self.f.install();self.f.store.composer(NOW);p=self.f.root/storage.DOMAINS[storage.OUTPUT][1]
        for data in [b"{",b'{"duplicate":1,"duplicate":2}',b" "*8193]:
            with self.subTest(data=data[:20]):
                p.write_bytes(data);self.assert_error(lambda:self.f.store.composer(NOW),"PRIOR_STATE_INVALID")
        p.unlink();self.assert_error(lambda:self.f.store.composer(NOW),"PRIOR_STATE_INVALID")
    def test_wrong_domain_digest_pending_state_block(self):
        self.f.install();self.f.store.composer(NOW);p=self.f.root/storage.DOMAINS[storage.OUTPUT][1];saved=p.read_bytes()
        for mutate in [lambda x:x.update(domain=storage.SOURCE),lambda x:x["confirmed"].update(sha256="0"*64),
                       lambda x:x.update(state="PENDING",candidate=x["confirmed"])]:
            x=json.loads(saved);mutate(x);p.write_bytes(m.canonical(x));self.assert_error(lambda:self.f.store.composer(NOW))
        p.write_bytes(saved)
    def test_corrupt_output_requires_explicit_fresh_recomputation(self):
        self.f.install();self.f.store.composer(NOW);self.f.primary(storage.OUTPUT).write_bytes(b"corrupt")
        self.assert_error(lambda:self.f.store.composer(NOW),"PRIOR_STATE_INVALID")
        r=self.f.store.composer(NOW,recovery=True,approved=True);self.assertEqual(self.f.store.read_handoff(NOW),r)
    def test_source_pending_does_not_block_independent_local_branch(self):
        self.f.install();self.f.fs.fault="PRIMARY_PARENT"
        self.assert_error(lambda:self.f.store.install_source(source(revision=2),approved=True),"WRITE_FAILED","INDETERMINATE_DURABILITY")
        self.f.fs.fault=None
        r=self.f.store.composer(NOW);self.assertEqual(r["configured"]["error_code"],"WRITE_FAILED")
        self.assertIsNotNone(self.f.store.read_handoff(NOW)["local"])
    def test_confirmed_source_anchor_is_independent_of_unusable_output(self):
        self.f.install();self.f.store.composer(NOW)
        self.f.primary(storage.OUTPUT).write_bytes(b"corrupt output")
        self.f.store.install_source(source(revision=2),approved=True)
        current,anchor,unused=self.f.store.confirmed(storage.SOURCE)
        self.assertEqual(current["revision"],2)
        self.assert_error(lambda:self.f.store.composer(NOW),"PRIOR_STATE_INVALID","RECOVERY_REQUIRED")
    def test_fresh_source_recovery_preserves_available_confirmed_output_revision_anchor(self):
        self.f.install();old_primary=self.f.primary(storage.SOURCE).read_bytes()
        old_meta=(self.f.root/storage.DOMAINS[storage.SOURCE][1]).read_bytes()
        self.f.store.install_source(source(revision=2),approved=True);self.f.store.composer(NOW)
        # Explicit synthetic replay of an older source/witness, not a production action.
        self.f.primary(storage.SOURCE).write_bytes(old_primary)
        (self.f.root/storage.DOMAINS[storage.SOURCE][1]).write_bytes(old_meta)
        candidate=source([],revision=2)
        self.assert_error(lambda:self.f.store.install_source(candidate,approved=True,recovery=True,initialize=True),"SOURCE_REVISION_CONFLICT")
    def test_recovery_preserves_pending_output_candidate_revision_floor(self):
        self.f.install();self.f.store.composer(NOW)
        old_primary=self.f.primary(storage.SOURCE).read_bytes()
        old_meta=(self.f.root/storage.DOMAINS[storage.SOURCE][1]).read_bytes()
        self.f.store.install_source(source(revision=2),approved=True)
        self.f.fs.fault="PRIMARY_PARENT";self.assert_error(lambda:self.f.store.composer(NOW))
        self.f.fs.fault=None
        self.f.primary(storage.SOURCE).write_bytes(old_primary)
        (self.f.root/storage.DOMAINS[storage.SOURCE][1]).write_bytes(old_meta)
        self.assert_error(lambda:self.f.store.install_source(source([],revision=2),approved=True,recovery=True,initialize=True),"SOURCE_REVISION_ROLLBACK")
        self.f.store.install_source(source([],revision=3),approved=True,recovery=True,initialize=True)
    def test_source_revision_anchors_and_pending_floor(self):
        self.f.install();self.f.store.composer(NOW)
        self.f.store.install_source(source(revision=2),approved=True)
        self.assert_error(lambda:self.f.store.install_source(source(),approved=True),"SOURCE_REVISION_ROLLBACK")
        self.f.fs.fault="PRIMARY_PARENT"
        self.assert_error(lambda:self.f.store.install_source(source(revision=3),approved=True))
        self.f.fs.fault=None
        self.assert_error(lambda:self.f.store.install_source(source(revision=2),approved=True,recovery=True,initialize=True),"SOURCE_REVISION_ROLLBACK")
        self.f.store.install_source(source(revision=4),approved=True,recovery=True,initialize=True)
    def test_unsafe_mode_uid_type_and_hardlink_source(self):
        self.f.install();p=self.f.primary(storage.SOURCE)
        for override in [dict(st_uid=1001),dict(st_mode=stat.S_IFREG|0o644),dict(st_mode=stat.S_IFLNK|0o600),dict(st_mode=stat.S_IFIFO|0o600),dict(st_nlink=2)]:
            self.f.fs.overrides[str(p)]=override
            with self.subTest(override=override):self.assertEqual(self.f.store.composer(NOW)["configured"]["error_code"],"SOURCE_METADATA_INVALID")
        self.f.fs.overrides={}
    def test_unsafe_directory_fails_before_primary_replacement(self):
        self.f.install();self.f.fs.overrides[str(self.f.primary(storage.OUTPUT).parent)]={"st_mode":stat.S_IFDIR|0o755}
        self.assert_error(lambda:self.f.store.composer(NOW));self.assertNotIn("PRIMARY_REPLACE",self.f.fs.trace[self.f.fs.trace.index("CONFIRMATION_PARENT")+1:])
    def test_overlap_nonblocking_no_output_replace(self):
        self.f.fs.busy=True;self.assert_error(lambda:self.f.store.composer(NOW),"OVERLAP_SKIPPED")
        self.assertFalse(self.f.primary(storage.OUTPUT).exists())
    def test_read_race_and_source_changed_before_output_replace(self):
        self.f.install()
        def mutate(phase,path):
            if phase=="PENDING_REPLACE" and path==self.f.root/storage.DOMAINS[storage.OUTPUT][1]:
                self.f.primary(storage.SOURCE).write_bytes(m.canonical(source(revision=2)))
        self.f.fs.after_replace=mutate
        self.assert_error(lambda:self.f.store.composer(NOW),"SOURCE_CHANGED","PRE_REPLACEMENT_FAILURE")
        self.assertFalse(self.f.primary(storage.OUTPUT).exists())
    def test_inventory_change_before_output_replace(self):
        self.f.install()
        def mutate(phase,path):
            if phase=="PENDING_REPLACE":
                inv=snapshot();inv["summary"]={"changed":True};(self.f.root/storage.INVENTORY).write_bytes(m.canonical(inv))
        self.f.fs.after_replace=mutate
        self.assert_error(lambda:self.f.store.composer(NOW),"INVENTORY_INVALID","PRE_REPLACEMENT_FAILURE")
    def test_invalid_input_changes_still_abort_unavailable_publication(self):
        for target,code in [(storage.INVENTORY,"INVENTORY_INVALID"),(storage.DOMAINS[storage.SOURCE][0],"SOURCE_CHANGED")]:
            with self.subTest(target=target):
                f=Fixture()
                try:
                    f.install();(f.root/target).write_bytes(b"invalid")
                    def mutate(phase,path):
                        if phase=="PENDING_REPLACE":(f.root/target).write_bytes(b"still invalid")
                    f.fs.after_replace=mutate
                    with self.assertRaises(m.AssociationError) as caught:f.store.composer(NOW)
                    self.assertEqual(caught.exception.code,code)
                    self.assertFalse(f.primary(storage.OUTPUT).exists())
                finally:f.close()
    def test_recovery_parent_fsync_failure_retains_pending(self):
        self.f.install();self.f.store.composer(NOW);self.f.fs.fault="PRIMARY_PARENT"
        self.assert_error(lambda:self.f.store.composer(NOW))
        self.f.fs.fault="RECOVERY_PRIMARY_PARENT"
        self.assert_error(lambda:self.f.store.recertify(storage.OUTPUT,NOW,True),"WRITE_FAILED","RECOVERY_REQUIRED")
        self.assertEqual(self.f.meta(storage.OUTPUT)["state"],"PENDING")
    def test_explicit_recovery_never_replaces_unsafe_primary_or_metadata(self):
        self.f.install()
        for relative in storage.DOMAINS[storage.SOURCE]:
            p=self.f.root/relative
            self.f.fs.overrides[str(p)]={"st_mode":stat.S_IFLNK|0o600}
            with self.subTest(relative=relative):
                self.assert_error(lambda:self.f.store.install_source(source(revision=2),approved=True,recovery=True,initialize=True),"SOURCE_METADATA_INVALID")
            self.f.fs.overrides={}
    def test_no_stale_temp_or_hidden_payload_lkg_consumed(self):
        self.f.install();p=self.f.primary(storage.OUTPUT).parent/".hioc-crash.tmp";p.write_bytes(b"not authority")
        self.f.store.composer(NOW);self.assertEqual(p.read_bytes(),b"not authority")
        self.assertEqual(set(x.name for x in p.parent.iterdir()),{".lock",".hioc-crash.tmp","current.json","current.durability.json"})
    def test_missing_inventory_whole_unavailable_nonfabricated(self):
        (self.f.root/storage.INVENTORY).unlink();self.f.install()
        r=self.f.store.composer(NOW);self.assertEqual(r["state"],"UNAVAILABLE");self.assertIsNone(r["local"])
        self.assertEqual(r["valid_until"],r["evaluated_at"]);self.assert_error(lambda:self.f.store.read_handoff(NOW))


class InitialInfrastructureTests(unittest.TestCase):
    def setUp(self):
        self.f=Fixture()
        # Existing config/state bases; all three approved private dirs absent.
        (self.f.root/"config/enrichment").rmdir()
        (self.f.root/"state/enrichment/service_associations").rmdir()
        (self.f.root/"state/enrichment").rmdir()
    def tearDown(self):self.f.close()
    def failure(self,call,code=None):
        with self.assertRaises(m.AssociationError) as caught:call()
        if code:self.assertEqual(caught.exception.code,code)
        self.assertFalse(self.f.primary(storage.SOURCE).exists())
        return caught.exception
    def test_posix_bootstrap_uses_anchored_no_follow_exact_mode_syscalls(self):
        fs=object.__new__(storage.PosixFS)
        with patch.object(storage.os,"O_DIRECTORY",0x10000,create=True),patch.object(storage.os,"O_NOFOLLOW",0x20000,create=True),patch.object(storage.os,"open",return_value=17) as opened,patch.object(storage.os,"mkdir") as made:
            self.assertEqual(fs.child_directory(12,"enrichment"),17)
            opened.assert_called_once_with("enrichment",storage.os.O_RDONLY|0x10000|0x20000,dir_fd=12)
            fs.mkdir(12,"enrichment");made.assert_called_once_with("enrichment",0o700,dir_fd=12)
    def test_concurrent_mkdir_accepts_only_safe_existing_winner(self):
        original=self.f.fs.mkdir
        def winner(d,name):
            original(d,name)
            raise FileExistsError()
        self.f.fs.mkdir=winner;self.f.install()
        self.assertEqual(self.f.meta(storage.SOURCE)["state"],"CONFIRMED")
    def test_ancestor_replacement_before_creation_fails_closed(self):
        original=self.f.fs.child_directory
        def replaced(d,name):
            value=original(d,name)
            if name=="config":self.f.fs.overrides[str(self.f.root)]={"st_ino":0}
            return value
        self.f.fs.child_directory=replaced
        self.failure(self.f.install,"SOURCE_CHANGED")
        self.assertNotIn("BOOTSTRAP_MKDIR",self.f.fs.trace)
    def test_clean_initial_install_all_directories_and_confirmed_sidecar(self):
        self.assertEqual(self.f.install(),"CONFIRMED_DURABLE_CURRENT")
        for p in ("config/enrichment","state/enrichment","state/enrichment/service_associations"):
            info=self.f.fs.statdir(self.f.root/p)
            self.assertEqual(stat.S_IMODE(info.st_mode),0o700);self.assertEqual(info.st_uid,1000)
        self.assertEqual(self.f.meta(storage.SOURCE)["state"],"CONFIRMED")
        self.assertTrue((self.f.root/storage.LOCK).is_file())
        self.assertEqual(stat.S_IMODE(self.f.fs.statat(self.f.primary(storage.SOURCE).parent,self.f.primary(storage.SOURCE).name).st_mode),0o600)
        self.assertEqual(self.f.fs.trace.count("PRIMARY_REPLACE"),1)
    def test_missing_without_initialization_is_not_contention(self):
        e=self.failure(lambda:self.f.store.install_source(source(),approved=True),"WRITE_FAILED")
        self.assertEqual(e.phase,"LOCK_UNAVAILABLE");self.assertNotIn("BOOTSTRAP_MKDIR",self.f.fs.trace)
    def test_missing_without_approval_does_not_create(self):
        self.failure(lambda:self.f.store.install_source(source(),initialize=True),"WRITE_FAILED")
        self.assertNotIn("BOOTSTRAP_MKDIR",self.f.fs.trace)
    def test_composer_cannot_bootstrap(self):
        self.failure(lambda:self.f.store.composer(NOW),"WRITE_FAILED")
        self.assertNotIn("BOOTSTRAP_MKDIR",self.f.fs.trace)
    def test_recovery_paths_cannot_bootstrap(self):
        for call in [lambda:self.f.store.install_source(source(),approved=True,initialize=True,recovery=True),
                     lambda:self.f.store.composer(NOW,recovery=True,approved=True),
                     lambda:self.f.store.recertify(storage.SOURCE,NOW,True)]:
            self.failure(call);self.assertNotIn("BOOTSTRAP_MKDIR",self.f.fs.trace)
    def test_wrong_existing_private_modes_and_owners_not_repaired(self):
        for p in ("config/enrichment","state/enrichment","state/enrichment/service_associations"):
            (self.f.root/p).mkdir(parents=True,exist_ok=True)
        for relative in ("config/enrichment","state/enrichment","state/enrichment/service_associations"):
            for override in ({"st_mode":stat.S_IFDIR|0o755},{"st_uid":1001}):
                self.f.fs.overrides[str(self.f.root/relative)]=override
                self.failure(self.f.install,"SOURCE_METADATA_INVALID")
                self.assertEqual(self.f.fs.overrides[str(self.f.root/relative)],override)
                self.f.fs.overrides={}
    def test_unsafe_base_directory_fails(self):
        for p in ("config","state"):
            for override in ({"st_mode":stat.S_IFDIR|0o777},{"st_uid":1001}):
                self.f.fs.overrides[str(self.f.root/p)]=override
                self.failure(self.f.install,"SOURCE_METADATA_INVALID")
                self.f.fs.overrides={}
    def test_non_directory_and_symlink_rejected(self):
        p=self.f.root/"config/enrichment";p.write_bytes(b"unchanged")
        self.failure(self.f.install);self.assertEqual(p.read_bytes(),b"unchanged")
        p.unlink()
        # Inject a symlink identity in the syscall model without Windows privilege.
        p.mkdir();self.f.fs.overrides[str(p)]={"st_mode":stat.S_IFLNK|0o700}
        self.failure(self.f.install,"SOURCE_METADATA_INVALID")
    def test_mkdir_and_directory_fsync_failure_prevent_primary(self):
        for phase in ("BOOTSTRAP_MKDIR","BOOTSTRAP_CHILD","BOOTSTRAP_PARENT"):
            self.f.fs.fault=phase
            e=self.failure(self.f.install,"WRITE_FAILED")
            self.assertEqual(e.phase,"INITIALIZATION_INFRASTRUCTURE_FAILED")
            self.assertNotIn("PRIMARY_REPLACE",self.f.fs.trace)
        self.f.fs.fault=None;self.f.install()
    def test_path_replacement_detected_before_source_primary(self):
        self.f.install();original=self.f.primary(storage.SOURCE).read_bytes()
        def change(phase,path):
            if phase=="PENDING_REPLACE":
                self.f.fs.overrides[str(self.f.root/"config/enrichment")]={"st_ino":0}
        self.f.fs.after_replace=change
        with self.assertRaises(m.AssociationError) as caught:
            self.f.store.install_source(source(revision=2),approved=True,initialize=True)
        self.assertEqual(caught.exception.code,"SOURCE_CHANGED")
        self.assertEqual(self.f.primary(storage.SOURCE).read_bytes(),original)
    def test_contending_lock_still_overlap(self):
        self.f.install();self.f.fs.busy=True
        with self.assertRaises(m.AssociationError) as caught:self.f.install()
        self.assertEqual(caught.exception.code,"OVERLAP_SKIPPED")
    def test_repeated_operation_does_not_recreate_or_repair(self):
        self.f.install();self.f.fs.trace=[]
        self.f.store.install_source(source(revision=2),approved=True)
        self.assertNotIn("BOOTSTRAP_MKDIR",self.f.fs.trace)
        self.f.fs.overrides[str(self.f.root/"config/enrichment")]={"st_mode":stat.S_IFDIR|0o755}
        with self.assertRaises(m.AssociationError):self.f.store.install_source(source(revision=3),approved=True)
    def test_preexisting_bases_are_required_no_generic_recursive_creation(self):
        (self.f.root/"config").rmdir()
        self.failure(self.f.install,"WRITE_FAILED");self.assertFalse((self.f.root/"config").exists())
    def test_malformed_candidate_does_not_bootstrap(self):
        bad=source();bad["revision"]=0
        self.failure(lambda:self.f.store.install_source(bad,approved=True,initialize=True))
        self.assertNotIn("BOOTSTRAP_MKDIR",self.f.fs.trace)

class EntrypointAndGovernanceTests(unittest.TestCase):
    def load(self,name):
        p=ROOT/"pi4/bin"/name
        spec=importlib.util.spec_from_file_location(name,p);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
    def test_composer_safe_counts_without_private_labels(self):
        f=Fixture();self.addCleanup(f.close);f.install();module=self.load("hioc-compose-service-associations.py")
        with patch.object(module,"datetime") as dt,redirect_stdout(io.StringIO()) as out:
            dt.now.return_value=m.local._time(NOW,"CLOCK_INVALID");self.assertEqual(module.main([],lambda:f.store),0)
        self.assertIn("ACCEPTED_COUNT=1",out.getvalue());self.assertNotIn(OWNER,out.getvalue())
    def test_argument_errors_do_not_echo_secrets_or_allow_root_override(self):
        for name in ["hioc-compose-service-associations.py","hioc-install-mqtt-mappings.py"]:
            module=self.load(name)
            with redirect_stdout(io.StringIO()) as out:
                self.assertEqual(module.main(["--root","secret-value"],lambda:None),1)
            self.assertNotIn("secret-value",out.getvalue())
    def test_dirfd_capability_gap_fails_closed_before_filesystem_use(self):
        with patch.object(storage.os,"name","posix"),patch.object(storage.os,"O_NOFOLLOW",0,create=True),patch.object(storage.os,"O_DIRECTORY",0,create=True),patch.object(storage.os,"supports_dir_fd",set()):
            with self.assertRaises(m.AssociationError) as caught:storage.PosixFS()
        self.assertEqual(caught.exception.phase,"POSIX_CAPABILITY_UNAVAILABLE")
    def test_native_posix_capability_not_claimed_on_windows(self):
        if os.name=="nt":
            with self.assertRaises(m.AssociationError):storage.PosixFS()
    def test_disabled_cron_exact_cadence_and_no_activation(self):
        text=raw("deploy/pe5-service-associations.cron.disabled").decode()
        self.assertTrue(all(not line or line.startswith("#") for line in text.splitlines()))
        self.assertIn("2,17,32,47 * * * *",text)
    def test_static_no_network_shell_credentials_public_mutation(self):
        paths=["pi4/lib/hioc/configured_association.py","pi4/lib/hioc/configured_association_store.py","pi4/lib/hioc/configured_association_schemas.py","pi4/bin/hioc-compose-service-associations.py","pi4/bin/hioc-install-mqtt-mappings.py"]
        forbidden={"socket","subprocess","requests","http","urllib","paho","paramiko","mqtt","home_assistant","dotenv"}
        for p in paths:
            tree=ast.parse(raw(p))
            for n in ast.walk(tree):
                if isinstance(n,ast.Import):
                    self.assertFalse(any(a.name.split(".")[0] in forbidden for a in n.names),p)
                if isinstance(n,ast.ImportFrom):self.assertNotIn((n.module or "").split(".")[0],forbidden,p)
            self.assertNotIn("os.environ",raw(p).decode())
    def test_exact_implementation_contract_scope_and_payload(self):implementation_successor()
    def test_implementation_sequence_pe54_not_started(self):assert_implementation_sequence(raw("docs/HIOC_MASTER_PLAN.md").decode())
    def test_reject_mismatched_schema_or_production_authority(self):
        r=copy.deepcopy(implementation_successor());r["production_activity"]["production_access"]=True
        with self.assertRaises(ValueError):validate_implementation(r,schema_for(r),False)
        r=implementation_successor();s=schema_for(r);s["additionalProperties"]=True
        with self.assertRaises(ValueError):validate_implementation(r,s,False)
    def test_checklist_complete_and_protected_previous_contract(self):
        r=implementation_successor();self.assertEqual(len(r["checklist"]),46);self.assertGreater(len(r["protected"]),223)

if __name__=="__main__":unittest.main()
