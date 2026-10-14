"""Repository-only contract tests and synthetic durability model, not PE-5.3 runtime."""
import copy
import hashlib
import json
import os
import subprocess
import tempfile
import unittest
from functools import lru_cache
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE="0c9c40d42c829c280341e73e475aac2ff4abf897"
RECORD="governance/pe5/pe5-atomic-durability-contract-correction.json"
SCHEMA=RECORD.replace(".json",".schema.json")
OLD="governance/pe5/pe5-mapping-contract-design.json"
ALLOWED=["execution.failure","handoff.validity","persistence.atomic","persistence.backup_recovery","persistence.corruption","persistence.history","persistence.lkg","persistence.restart","persistence.retention","schemas_semantics.atomic_input","schemas_semantics.deployment","schemas_semantics.source_install","schemas_semantics.source_state","source.revision","source.update"]

def git(*args):
    return subprocess.check_output(["git","--no-optional-locks",*args],cwd=ROOT,env=dict(os.environ,GIT_OPTIONAL_LOCKS="0"),stderr=subprocess.PIPE)
def raw(p):return (ROOT/p).read_bytes().replace(b"\r\n",b"\n")
def canonical(x):return (json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False)+"\n").encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def require(x,m):
    if not x:raise ValueError(m)
def closed(v):
    if type(v) is dict:return dict(type="object",additionalProperties=False,required=sorted(v),properties={k:closed(x) for k,x in sorted(v.items())})
    if type(v) is list:return dict(type="array",minItems=len(v),maxItems=len(v),prefixItems=[closed(x) for x in v],items=False)
    return dict(const=v)
def schema_for(r):
    return {"$schema":"https://json-schema.org/draft/2020-12/schema","title":"PE-5.2 atomic durability failure contract correction",**closed(r)}
def leaves(v,p=""):
    out={}
    for k,x in v.items():
        q=(p+"."+k).lstrip(".")
        if type(x) is dict:out.update(leaves(x,q))
        else:out[q]=x
    return out
def metadata_schema():
    variants=[]
    for domain in ("CONFIGURED_MAPPING_SOURCE","GENERATED_RELATIONSHIP_OUTPUT"):
        revision={"type":"integer","minimum":1,"maximum":9007199254740991}
        if domain=="GENERATED_RELATIONSHIP_OUTPUT":revision={"anyOf":[revision,{"type":"null"}]}
        descriptor=dict(type="object",additionalProperties=False,required=["sha256","source_revision"],properties=dict(sha256={"type":"string","pattern":"^[0-9a-f]{64}$"},source_revision=revision))
        optional={"anyOf":[descriptor,{"type":"null"}]}
        for state in ("PENDING","CONFIRMED"):
            props=dict(schema_version={"const":"1.0"},domain={"const":domain},transaction_id={"type":"string","pattern":"^dur_[0-9a-f]{32}$"},state={"const":state},confirmed=optional if state=="PENDING" else descriptor,candidate=descriptor if state=="PENDING" else {"type":"null"})
            variants.append(dict(type="object",additionalProperties=False,required=sorted(props),properties=props))
    return {"$schema":"https://json-schema.org/draft/2020-12/schema","title":"Private primary durability witness, canonical bytes bounded to 8192", "anyOf":variants}
def validate_correction(r,s,identities=True):
    require(s==schema_for(r),"exact typed correction schema")
    require(r["predecessor_commit"]==BASE and r["status"]=="COMPLETE_ATOMIC_DURABILITY_CONTRACT_CORRECTION","correction authority")
    original=json.loads(git("show",BASE+":"+OLD))
    a,b=leaves(original["contract"]),leaves(r["contract"])
    changed={p for p in a if a[p]!=b.get(p)}
    require(changed==set(ALLOWED) and r["allowed_contract_changes"]==ALLOWED,"unrelated contract changed")
    require(set(r["contract"])==set(original["contract"])|{"atomic_durability"},"contract scope")
    require(r["input_schema"]==original["input_schema"] and r["output_schema"]==original["output_schema"],"primary schemas changed")
    require(r["metadata_schema"]==metadata_schema(),"metadata scope")
    require(all(x is False for x in r["activity"].values()),"runtime/production scope")
    d=r["contract"]["atomic_durability"];p=d["post_primary_parent_failure"]
    require(p["state"]=="INDETERMINATE_DURABILITY" and p["fail_closed"] is True,"durability failure")
    require(all(p[k] is False for k in ("prior_physical_presence_guaranteed","new_durable_commit_claimed","automatic_rollback","second_primary_replace_as_rollback","confirmation_write_allowed")),"false guarantee/rollback")
    require(d["pre_replacement"]["prior_path_unchanged"] is True and d["pre_replacement"]["temp_authoritative"] is False,"pre-replace")
    require("PENDING.confirmed" in p["logical_lkg"] and "No primary os.replace" in d["explicit_recovery"],"recovery")
    require(d["primary_sequence"]==["validate_inputs_and_confirmed_anchor","durable_pending_barrier","write_exclusive_primary_temp","fsync_primary_temp","replace_primary_once","fsync_primary_parent","publish_confirmed_metadata","fsync_confirmation_metadata_parent"],"write ordering")
    require(r["historical_stop"]["result"]=="STOP_PE5_3_ATOMIC_FAILURE_CONTRACT_CONTRADICTION" and r["historical_stop"]["synthetic_tests_passed"]==1,"STOP preservation")
    if identities:
        scope=set(r["authorized_paths"])
        require(len(scope)==10 and scope=={i["path"] for i in r["artifacts"]}|{RECORD,SCHEMA},"scope")
        changed=set(git("diff","--name-only",BASE).decode().splitlines())|set(git("ls-files","--others","--exclude-standard").decode().splitlines())
        require(changed==scope,"unexpected path")
        for i in r["artifacts"]:
            b=raw(i["path"]);require((sha(b),blob(b))==(i["sha256"],i["git_blob"]),"correction binding: "+i["path"])
        for i in r["protected"]:
            b=git("show",BASE+":"+i["path"]);require(raw(i["path"])==b and (sha(b),blob(b))==(i["sha256"],i["git_blob"]),"immutable artifact: "+i["path"])
    return r
@lru_cache(maxsize=1)
def correction():
    b,sb=raw(RECORD),raw(SCHEMA);r,s=json.loads(b),json.loads(sb)
    require(b==canonical(r) and sb==canonical(s),"canonical correction")
    return validate_correction(r,s)
def durability_binding(path):
    i=next((x for x in correction()["artifacts"] if x["path"]==path),None)
    if i:require((sha(raw(path)),blob(raw(path)))==(i["sha256"],i["git_blob"]),"durability binding")
    return i

class SyntheticPersistence:
    """Test-only model. Real file fsync/replace; directory-sync outcomes injected.
    Does not validate POSIX crash behavior, permissions, flock or runtime schemas.
    """
    def __init__(self,root):
        self.primary=Path(root)/"primary.json";self.meta=Path(root)/"durability.json"
        self.trace=[];self.replacements=0
        self.old=canonical(dict(revision=1,value="prior",evaluated_at="unchanged"))
        self.new=canonical(dict(revision=2,value="candidate",evaluated_at="unchanged"))
        self.primary.write_bytes(self.old)
        self.meta.write_bytes(canonical(self.witness("CONFIRMED",self.descriptor(self.old),None)))
    def descriptor(self,b):
        x=json.loads(b)
        require(set(x)=={"revision","value","evaluated_at"} and type(x["revision"]) is int and x["revision"]>0,"synthetic primary shape")
        return dict(sha256=sha(b),source_revision=x["revision"])
    def witness(self,state,confirmed,candidate):
        return dict(schema_version="1.0",domain="CONFIGURED_MAPPING_SOURCE",transaction_id="dur_"+"1"*32,state=state,confirmed=confirmed,candidate=candidate)
    def read_meta(self):
        from test_pe5_mapping_contract_design import check_shape
        b=self.meta.read_bytes();require(len(b)<=8192,"metadata bound")
        m=json.loads(b);check_shape(m,metadata_schema())
        require(m["domain"]=="CONFIGURED_MAPPING_SOURCE","domain")
        return m
    def step(self,name,fault):
        self.trace.append(name)
        if name==fault:raise OSError("synthetic EIO at "+name)
    def atomic_meta(self,m,phase,fault):
        tmp=self.meta.with_suffix(".tmp")
        try:
            self.step(phase+"_write",fault)
            with tmp.open("xb") as f:
                f.write(canonical(m));f.flush();os.fsync(f.fileno())
            self.step(phase+"_replace",fault);os.replace(tmp,self.meta)
            self.step(phase+"_parent",fault)
        finally:
            if tmp.exists():tmp.unlink()
    def confirmed_anchor(self):
        m=self.read_meta()
        require(m["state"]=="CONFIRMED" and m["confirmed"]==self.descriptor(self.primary.read_bytes()),"unconfirmed primary")
        return m["confirmed"]
    def publish(self,fault=None):
        tmp=self.primary.with_suffix(".tmp");phase="PRE_REPLACEMENT_FAILURE"
        try:
            old=self.confirmed_anchor()
            # Trusted surviving CONFIRMED must be resynced before starting another attempt.
            self.step("anchor_file",fault)
            with self.primary.open("r+b") as f:os.fsync(f.fileno())
            self.step("anchor_parent",fault)
            with self.meta.open("r+b") as f:os.fsync(f.fileno())
            self.step("anchor_metadata_parent",fault)
            self.atomic_meta(self.witness("PENDING",old,self.descriptor(self.new)),"pending",fault)
            self.step("primary_write",fault)
            with tmp.open("xb") as f:
                f.write(self.new);f.flush();self.step("primary_fsync",fault);os.fsync(f.fileno())
            self.step("primary_replace",fault)
            os.replace(tmp,self.primary);self.replacements+=1
            phase="INDETERMINATE_DURABILITY";self.step("primary_parent",fault)
            phase="CONFIRMATION_METADATA_UNCONFIRMED"
            self.atomic_meta(self.witness("CONFIRMED",self.descriptor(self.new),None),"confirmation",fault)
            return "CONFIRMED_DURABLE_CURRENT"
        except (OSError,ValueError):return phase
        finally:
            if tmp.exists():tmp.unlink()
    def consume(self):
        try:self.confirmed_anchor();return True
        except (OSError,ValueError,KeyError):return False
    def recover(self,fault=None):
        m=self.read_meta();b=self.primary.read_bytes();d=self.descriptor(b)
        require(d==m["candidate"] or d==m["confirmed"],"unrecorded primary")
        self.step("recovery_file",fault)
        with self.primary.open("r+b") as f:os.fsync(f.fileno())
        self.step("recovery_parent",fault)
        self.atomic_meta(self.witness("CONFIRMED",d,None),"recovery_confirmation",fault)
        return "CONFIRMED_DURABLE_CURRENT"

class AtomicDurabilityCorrectionTests(unittest.TestCase):
    def test_complete_exact_successor(self):correction()
    def test_no_unrelated_contract_changes(self):
        r=copy.deepcopy(correction());r["contract"]["execution"]["cadence_seconds"]=1
        with self.assertRaises(ValueError):validate_correction(r,schema_for(r),False)
    def test_primary_schemas_unchanged(self):
        old=json.loads(git("show",BASE+":"+OLD))
        self.assertEqual(correction()["input_schema"],old["input_schema"]);self.assertEqual(correction()["output_schema"],old["output_schema"])
    def test_no_identity_or_transport_authority_changes(self):
        old=json.loads(git("show",BASE+":"+OLD))["contract"];new=correction()["contract"]
        for section in ("mqtt","relationships","premise"):self.assertEqual(new[section],old[section])
        self.assertFalse(new["persistence"]["lkg_required"])
    def test_source_uncertainty_preserves_independent_local_branch(self):
        c=correction()["contract"]
        self.assertIn("independently valid local branch",c["handoff"]["validity"])
        self.assertIn("output itself is confirmed",c["handoff"]["validity"])
        self.assertIn("affected primary domain",c["atomic_durability"]["scope"])
        old=json.loads(git("show",BASE+":"+OLD))["contract"]
        self.assertEqual(c["source"]["failure"],old["source"]["failure"])
    def test_runtime_and_historical_artifacts_immutable(self):
        self.assertGreater(len(correction()["protected"]),220)
        self.assertFalse(any(correction()["activity"].values()))
    def test_metadata_closed_private_bounded(self):
        from test_pe5_mapping_contract_design import check_shape
        m=dict(schema_version="1.0",domain="CONFIGURED_MAPPING_SOURCE",transaction_id="dur_"+"a"*32,state="PENDING",confirmed=None,candidate=dict(sha256="b"*64,source_revision=1))
        check_shape(m,metadata_schema())
        for key in ("topic","ip","mac","health","password","payload","evaluated_at"):
            bad=dict(m,**{key:"forbidden"})
            with self.subTest(key=key),self.assertRaises(ValueError):check_shape(bad,metadata_schema())
        for key,value in (("state","INDETERMINATE"),("domain","PUBLIC"),("transaction_id","guess")):
            bad=dict(m,**{key:value})
            with self.subTest(key=key),self.assertRaises(ValueError):check_shape(bad,metadata_schema())
    def test_metadata_descriptors_revision_rules(self):
        from test_pe5_mapping_contract_design import check_shape
        m=dict(schema_version="1.0",domain="CONFIGURED_MAPPING_SOURCE",transaction_id="dur_"+"a"*32,state="CONFIRMED",confirmed=dict(sha256="b"*64,source_revision=None),candidate=None)
        with self.assertRaises(ValueError):check_shape(m,metadata_schema())
        m["domain"]="GENERATED_RELATIONSHIP_OUTPUT";check_shape(m,metadata_schema())
        m["confirmed"]["source_revision"]=True
        with self.assertRaises(ValueError):check_shape(m,metadata_schema())
    def model(self):return tempfile.TemporaryDirectory()
    def test_before_replace_failures_preserve_prior(self):
        for fault in ("primary_write","primary_fsync","primary_replace","pending_write","pending_replace","pending_parent"):
            with self.subTest(fault=fault),self.model() as root:
                f=SyntheticPersistence(root);self.assertEqual(f.publish(fault),"PRE_REPLACEMENT_FAILURE")
                self.assertEqual(f.primary.read_bytes(),f.old);self.assertEqual(f.replacements,0)
                self.assertEqual(f.read_meta()["confirmed"],f.descriptor(f.old))
                self.assertFalse(f.primary.with_suffix(".tmp").exists())
    def test_success_confirms_candidate_in_exact_order(self):
        with self.model() as root:
            f=SyntheticPersistence(root);self.assertEqual(f.publish(),"CONFIRMED_DURABLE_CURRENT")
            self.assertEqual(f.primary.read_bytes(),f.new);self.assertTrue(f.consume());self.assertEqual(f.replacements,1)
            self.assertLess(f.trace.index("pending_parent"),f.trace.index("primary_replace"))
            self.assertLess(f.trace.index("primary_parent"),f.trace.index("confirmation_write"))
            self.assertEqual(f.trace[-1],"confirmation_parent")
    def test_original_fault_fixture_old_file_physically_gone(self):
        with self.model() as root:
            f=SyntheticPersistence(root);self.assertEqual(f.publish("primary_parent"),"INDETERMINATE_DURABILITY")
            self.assertEqual(f.primary.read_bytes(),f.new);self.assertNotEqual(f.primary.read_bytes(),f.old)
            self.assertFalse(f.consume());self.assertEqual(f.replacements,1)
            self.assertNotIn("confirmation_write",f.trace)
            self.assertEqual(f.read_meta()["state"],"PENDING")
            self.assertEqual(f.read_meta()["confirmed"],f.descriptor(f.old))
    def test_indeterminate_next_invocation_blocks_no_rollback(self):
        with self.model() as root:
            f=SyntheticPersistence(root);f.publish("primary_parent");before=f.primary.read_bytes()
            self.assertEqual(f.publish(),"PRE_REPLACEMENT_FAILURE");self.assertEqual(f.replacements,1)
            self.assertEqual(f.primary.read_bytes(),before);self.assertFalse(f.consume())
    def test_candidate_recertification_no_primary_replace_or_time_refresh(self):
        with self.model() as root:
            f=SyntheticPersistence(root);f.publish("primary_parent");before=f.primary.read_bytes()
            self.assertEqual(f.recover(),"CONFIRMED_DURABLE_CURRENT");self.assertTrue(f.consume())
            self.assertEqual(f.primary.read_bytes(),before);self.assertEqual(f.replacements,1)
    def test_prior_recertification_after_pre_replace_failure(self):
        with self.model() as root:
            f=SyntheticPersistence(root);f.publish("primary_replace")
            f.recover();self.assertEqual(f.primary.read_bytes(),f.old);self.assertEqual(f.replacements,0)
    def test_recovery_failed_parent_stays_pending(self):
        with self.model() as root:
            f=SyntheticPersistence(root);f.publish("primary_parent")
            with self.assertRaises(OSError):f.recover("recovery_parent")
            self.assertEqual(f.read_meta()["state"],"PENDING");self.assertFalse(f.consume())
    def test_recovery_unmatched_or_missing_primary_stops(self):
        for missing in (True,False):
            with self.subTest(missing=missing),self.model() as root:
                f=SyntheticPersistence(root);f.publish("primary_parent")
                if missing:f.primary.unlink()
                else:f.primary.write_bytes(canonical(dict(revision=3,value="unrecorded",evaluated_at="unchanged")))
                with self.assertRaises((OSError,ValueError)):f.recover()
                self.assertEqual(f.read_meta()["state"],"PENDING")
    def test_confirmation_failure_does_not_claim_full_success(self):
        for fault in ("confirmation_write","confirmation_replace","confirmation_parent"):
            with self.subTest(fault=fault),self.model() as root:
                f=SyntheticPersistence(root);self.assertEqual(f.publish(fault),"CONFIRMATION_METADATA_UNCONFIRMED")
                self.assertEqual(f.primary.read_bytes(),f.new);self.assertEqual(f.replacements,1)
                if fault!="confirmation_parent":self.assertFalse(f.consume())
                else:
                    self.assertTrue(f.consume())
                    # Witness proves prior primary fsync, not its own parent fsync.
                    self.assertLess(f.trace.index("primary_parent"),f.trace.index("confirmation_replace"))
                    self.assertEqual(f.publish("anchor_parent"),"PRE_REPLACEMENT_FAILURE")
                    self.assertEqual(f.replacements,1)
    def test_missing_malformed_wrong_domain_metadata_fails_closed(self):
        for fault in ("absent","malformed","domain","digest","oversized"):
            with self.subTest(fault=fault),self.model() as root:
                f=SyntheticPersistence(root)
                if fault=="absent":f.meta.unlink()
                elif fault=="malformed":f.meta.write_bytes(b"invalid")
                elif fault=="oversized":f.meta.write_bytes(b" "*8193)
                else:
                    m=f.read_meta()
                    if fault=="domain":m["domain"]="GENERATED_RELATIONSHIP_OUTPUT"
                    else:m["confirmed"]["sha256"]="0"*64
                    f.meta.write_bytes(canonical(m))
                self.assertFalse(f.consume());self.assertEqual(f.publish(),"PRE_REPLACEMENT_FAILURE");self.assertEqual(f.replacements,0)
    def test_contract_rejects_false_physical_guarantee(self):
        r=copy.deepcopy(correction());r["contract"]["atomic_durability"]["post_primary_parent_failure"]["prior_physical_presence_guaranteed"]=True
        with self.assertRaises(ValueError):validate_correction(r,schema_for(r),False)
    def test_contract_rejects_automatic_rollback(self):
        r=copy.deepcopy(correction());r["contract"]["atomic_durability"]["post_primary_parent_failure"]["automatic_rollback"]=True
        with self.assertRaises(ValueError):validate_correction(r,schema_for(r),False)
    def test_historical_stop_preserved(self):
        self.assertEqual(correction()["historical_stop"]["synthetic_tests_passed"],1)
        self.assertIn("precedes implementation",correction()["contract"]["atomic_durability"]["stop_evidence"])

if __name__=="__main__":unittest.main()
