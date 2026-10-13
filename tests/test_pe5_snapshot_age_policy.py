"""Approved policy governance and synthetic boundary tests; no production."""
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

ROOT = Path(__file__).resolve().parents[1]
BASE = "eda8c9930d7f7fbf09bcc08b252bef05b385cf7e"
RECORD = "governance/pe5/pe5-snapshot-age-policy-selection.json"
SCHEMA = RECORD.replace(".json", ".schema.json")
POLICY_PATHS = (
    "docs/HIOC_MASTER_PLAN.md",
    "docs/PASSIVE_ENRICHMENT_ARCHITECTURE.md",
    "docs/PE5_LOCAL_SERVICE_ASSOCIATION_IMPLEMENTATION.md",
    RECORD, SCHEMA,
    "tests/test_pe5_service_association_caller.py",
    "tests/test_pe4_ha_association_public_projection_test_binding_correction.py",
    "tests/test_pe5_snapshot_age_policy.py",
)

def git(*args):
    return subprocess.check_output(["git", "--no-optional-locks", *args], cwd=ROOT,
                                  env=dict(os.environ, GIT_OPTIONAL_LOCKS="0"), stderr=subprocess.PIPE)

def raw(path):
    return (ROOT/path).read_bytes().replace(b"\r\n", b"\n")

def sha(value): return hashlib.sha256(value).hexdigest()
def blob(value): return hashlib.sha1(b"blob "+str(len(value)).encode()+b"\0"+value).hexdigest()
def canonical(value): return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)+"\n").encode()
def require(value, message):
    if not value: raise ValueError(message)

def closed(value):
    if type(value) is dict:
        return dict(type="object", additionalProperties=False, required=sorted(value),
                    properties={k:closed(v) for k,v in sorted(value.items())})
    if type(value) is list:
        return dict(type="array", minItems=len(value), maxItems=len(value),
                    prefixItems=[closed(v) for v in value], items=False)
    return dict(const=value)

def schema_for(record):
    return {"$schema":"https://json-schema.org/draft/2020-12/schema",
            "title":"PE-5.1 approved snapshot-age policy selection", **closed(record)}

def validate_policy_record(record, schema):
    require(schema == schema_for(record), "exact policy schema mismatch")
    require(record["predecessor_commit"] == BASE and record["authorized_paths"] == list(POLICY_PATHS), "policy scope changed")
    require(record["max_snapshot_age_seconds"] == 2100 and type(record["max_snapshot_age_seconds"]) is int, "approved value changed")
    require(record["snapshot_age_policy_status"] == "SELECTED_CANDIDATE_PENDING_COMMIT", "policy status changed")
    require(record["policy_basis"] == "EXPLICIT_OPERATIONAL_POLICY_INFORMED_BY_PRODUCTION_EVIDENCE", "policy basis changed")
    require(record["scheduled_cadence_seconds"] == 1800 and record["tolerance_seconds"] == 300, "tolerance changed")
    require(record["measured_worst_case_bound"] is False and record["future_cycle_guarantee"] is False, "observation overstated")
    require(record["policy_default"] is None and record["private_state_requirement"] == "DEFERRED_NOT_REQUIRED_FOR_OFFLINE_CALLER", "caller expanded")
    require(all(value is False for value in record["forbidden_activity"].values()), "operational scope expanded")
    require(record["current_next_task"] == "CONCISE_INDEPENDENT_CANDIDATE_ACCEPTANCE", "next checkpoint changed")
    require(record["operator_evidence"] == OPERATOR_EVIDENCE, "operator evidence changed")
    require(not git("diff","--cached","--name-only") and not git("stash","list"), "index or stash changed")
    head = git("rev-parse","HEAD").decode().strip()
    if head == BASE:
        require(git("rev-parse","origin/main").decode().strip() == BASE, "tracking changed")
        changes = set(git("diff","--name-only").decode().splitlines()) | set(git("ls-files","--others","--exclude-standard").decode().splitlines())
    else:
        require(git("rev-parse","HEAD^").decode().strip() == BASE and not git("status","--porcelain"), "wrong committed policy")
        changes = set(git("diff","--name-only",BASE,head).decode().splitlines())
    require(changes == set(POLICY_PATHS), "unexpected policy mutation")
    require({i["path"] for i in record["artifacts"]} == set(POLICY_PATHS)-{RECORD,SCHEMA}
            and len(record["artifacts"]) == len(POLICY_PATHS)-2, "incomplete policy map")
    for item in record["artifacts"]:
        value = raw(item["path"])
        require(sha(value) == item["sha256"] and blob(value) == item["git_blob"], "policy identity mismatch")
    for item in record["protected_artifacts"]:
        value = git("show",BASE+":"+item["path"])
        require(sha(value) == item["sha256"] and blob(value) == item["git_blob"]
                and raw(item["path"]) == value, "historical or runtime artifact changed")
    import difflib
    for path, changes in record["document_edits"].items():
        old = git("show",BASE+":"+path).decode().splitlines(keepends=True)
        new = raw(path).decode().splitlines(keepends=True)
        require(list(difflib.unified_diff(old,new)) == changes, "unrelated document edit")
    old = ast.parse(git("show",BASE+":tests/test_pe5_service_association_caller.py"))
    new = ast.parse(raw("tests/test_pe5_service_association_caller.py"))
    get = lambda tree,name:next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name == name)
    require([ast.dump(n) for n in get(old,"validate_caller_record").body] ==
            [ast.dump(n) for n in get(new,"_validate_historical_caller").body], "historical caller validator weakened")
    for path in record["document_edits"]:
        text = raw(path).decode()
        current = text.split("<!-- PE5_1_CURRENT_POLICY_BEGIN -->",1)[1].split("<!-- PE5_1_CURRENT_POLICY_END -->",1)[0]
        for marker in ["PE5_1_MAX_SNAPSHOT_AGE_SECONDS=2100", "SELECTED_CANDIDATE_PENDING_COMMIT", "NOT AUTHORIZED"]:
            require(marker in current, "current policy missing")
        require("UNKNOWN_REQUIRED_BEFORE_OPERATIONAL_USE" not in current, "current policy still unknown")
    # Historical observation identity is linked to existing immutable deployment authority.
    authority = json.loads(git("show",BASE+":governance/pe4/pe4-ha-association-public-projection-deployment-baseline-correction.json"))
    require(authority["backport"]["sha256"] == OPERATOR_EVIDENCE["production_engine_sha256"], "engine historical authority mismatch")
    require(authority["preserved_runtime"]["pi4/lib/hioc/inventory.py"]["sha256"] ==
            OPERATOR_EVIDENCE["production_inventory_sha256"], "inventory historical authority mismatch")
    payload = git("show",BASE+":"+authority["backport"]["path"])
    require(sha(payload) == OPERATOR_EVIDENCE["production_engine_sha256"], "engine payload mismatch")
    return record

OPERATOR_EVIDENCE = {
    "provenance":"OPERATOR_SUPPLIED",
    "source_sync_commit":BASE, "source_sync_independent_acceptance":"PASS",
    "production_engine_sha256":"5c12a368d8db7b045348cf201331c5e24390fbfe715fe399a4afef79fa594ca0",
    "production_inventory_sha256":"df1dc4e2de7d8d77b54acdcb3f340281ead6cc03d74a73ad59b2864b03564503",
    "cron_schedule":"*/30 * * * *", "cron_active":True, "canonical_command_match":True,
    "timezone":"America/Costa_Rica", "ntp_enabled":True, "ntp_synchronized":True,
    "natural_refresh_count":2, "previous_snapshot_age_seconds":[1801.594635,1800.903011],
    "new_snapshot_age_seconds":[6.096861,5.739757],
    "engine_duration_bounds_seconds":[[1.24,6.36],[0.6,5.776]],
    "final_capture_summary_available":False, "capture_termination_cause":"UNKNOWN",
    "whole_failure_history_proven":False,
}

@lru_cache(maxsize=1)
def policy_successor():
    record_raw, schema_raw = raw(RECORD), raw(SCHEMA)
    record, schema = json.loads(record_raw), json.loads(schema_raw)
    require(record_raw == canonical(record) and schema_raw == canonical(schema), "noncanonical policy")
    return validate_policy_record(record,schema)

def policy_current_binding(path):
    item = next((i for i in policy_successor()["artifacts"] if i["path"] == path),None)
    require(item is not None, "outside policy map")
    value=raw(path)
    require(sha(value) == item["sha256"] and blob(value) == item["git_blob"], "current policy identity mismatch")
    return item

def assert_policy_sequence(text):
    policy_current_binding("docs/HIOC_MASTER_PLAN.md")
    section=text.split("## Next Planned Task",1)[1].split("### Historical",1)[0]
    require(section.strip().startswith("### PE-5.1 snapshot-age policy"), "policy next task missing")
    require("CONCISE_INDEPENDENT_CANDIDATE_ACCEPTANCE" in section and "NOT AUTHORIZED" in section, "policy stop gate missing")

class SnapshotAgePolicyTests(unittest.TestCase):
    def test_exact_current_governance(self): policy_successor()
    def test_documents_agree_current_not_unknown(self):
        record=policy_successor()
        self.assertEqual(record["max_snapshot_age_seconds"],2100)
        assert_policy_sequence(raw("docs/HIOC_MASTER_PLAN.md").decode())
    def test_historical_unknown_and_validator_preserved(self):
        from test_pe5_service_association_caller import caller_successor
        self.assertEqual(caller_successor()["snapshot_age_policy"],"UNKNOWN_REQUIRED_BEFORE_OPERATIONAL_USE")
        self.assertEqual(raw("governance/pe5/pe5-service-association-caller-integration.json"),
                         git("show",BASE+":governance/pe5/pe5-service-association-caller-integration.json"))
    def test_reject_changed_value_or_status(self):
        for field,value in [("max_snapshot_age_seconds",2101),("max_snapshot_age_seconds",True),
                            ("snapshot_age_policy_status","UNKNOWN_REQUIRED_BEFORE_OPERATIONAL_USE"),
                            ("measured_worst_case_bound",True),("policy_default",2100)]:
            record=copy.deepcopy(policy_successor());record[field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):validate_policy_record(record,schema_for(record))
    def test_reject_runtime_authority_expansion(self):
        for field in policy_successor()["forbidden_activity"]:
            record=copy.deepcopy(policy_successor());record["forbidden_activity"][field]=True
            with self.subTest(field=field),self.assertRaises(ValueError):validate_policy_record(record,schema_for(record))
    def test_reject_stale_identity_and_open_schema(self):
        record=copy.deepcopy(policy_successor());record["artifacts"][0]["sha256"]="0"*64
        with self.assertRaises(ValueError):validate_policy_record(record,schema_for(record))
        schema=schema_for(policy_successor());schema["additionalProperties"]=True
        with self.assertRaises(ValueError):validate_policy_record(policy_successor(),schema)
    def test_reject_unapproved_binding(self):
        with self.assertRaises(ValueError):policy_current_binding("pi4/lib/hioc/service_association.py")
    def test_approved_inclusive_boundary(self):
        from hioc.service_association import resolve_service_associations
        from test_pe5_local_service_association import snapshot
        self.assertEqual(resolve_service_associations(snapshot(),"2026-10-12T12:35:00Z",2100)["association_count"],1)
    def test_microsecond_and_whole_second_excess_rejected(self):
        from hioc.service_association import resolve_service_associations, ServiceAssociationError
        from test_pe5_local_service_association import snapshot
        for timestamp in ["2026-10-12T12:35:00.000001Z","2026-10-12T12:35:01Z"]:
            with self.subTest(timestamp=timestamp),self.assertRaises(ServiceAssociationError) as caught:
                resolve_service_associations(snapshot(),timestamp,2100)
            self.assertEqual(str(caught.exception),"SNAPSHOT_STALE")
    def test_future_still_rejected(self):
        from hioc.service_association import resolve_service_associations, ServiceAssociationError
        from test_pe5_local_service_association import snapshot
        with self.assertRaises(ServiceAssociationError) as caught:
            resolve_service_associations(snapshot(),"2026-10-12T11:59:59.999999Z",2100)
        self.assertEqual(str(caught.exception),"SNAPSHOT_FUTURE")
    def test_explicit_arbitrary_threshold_remains_supported(self):
        from hioc.service_association import resolve_service_associations, ServiceAssociationError
        from test_pe5_local_service_association import snapshot, NOW
        self.assertEqual(resolve_service_associations(snapshot(),NOW,0)["association_count"],1)
        self.assertEqual(resolve_service_associations(snapshot(),"2026-10-12T12:01:00Z",60)["association_count"],1)
        with self.assertRaises(ServiceAssociationError):resolve_service_associations(snapshot(),"2026-10-12T12:01:00Z",59)
    def test_runtime_and_caller_bytes_unchanged(self):
        for path in ["pi4/lib/hioc/service_association.py","pi4/bin/hioc-resolve-local-services.py",
                     "pi4/bin/hioc-inventory-engine.py","pi4/lib/hioc/inventory.py","pi4/install_pi4.sh"]:
            self.assertEqual(raw(path),git("show",BASE+":"+path),path)

if __name__ == "__main__": unittest.main()
