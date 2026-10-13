"""Synthetic private resolver tests; never collect or access runtime state."""
import ast
import copy
import json
import os
import socket
import subprocess
import sys
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "pi4/lib"))
from hioc import service_association as module
from hioc.inventory import normalize_mac, stable_device_id

NOW = "2026-10-12T12:00:00Z"
MAC = "02:00:00:00:00:01"
OWNER = stable_device_id({"mac": MAC})
SECOND_MAC = "02:00:00:00:00:02"
SECOND_OWNER = stable_device_id({"mac": SECOND_MAC})
SERVICE = "svc_scheduler_01234567"


def device(mac=MAC, device_id=None):
    return {"id": device_id or stable_device_id({"mac": normalize_mac(mac)}), "mac": mac,
            "ip": "192.0.2.1", "first_seen": "historical", "last_seen": "unchanged",
            "health_status": "watch", "expected_availability": "operator-owned",
            "notes": "synthetic private note", "home_assistant": {"associated": True}}


def service(service_id=SERVICE, source="systemd", owner=OWNER, service_type="scheduler"):
    value = {"id": service_id, "source": source, "device_id": owner,
             "type": service_type, "name": "synthetic label", "status": "inactive"}
    if source == "ss":
        value["port"] = {"svc_mqtt_listener": 1883, "svc_network_53": 53, "svc_network_67": 67}[service_id]
    return value


def snapshot(services=None, devices=None):
    return {"schema_version": "1.0", "updated": NOW,
            "devices": [device()] if devices is None else devices,
            "services": [service()] if services is None else services,
            "topology": {"edges": []}, "dependencies": {"edges": []},
            "summary": {"service_count": 1}, "discovery_limited": False}


def resolve(value=None, evaluated=NOW, maximum=60):
    return module.resolve_service_associations(snapshot() if value is None else value, evaluated, maximum)


class LocalServiceAssociationTests(unittest.TestCase):
    def reject(self, value, code, evaluated=NOW, maximum=60):
        before = copy.deepcopy(value)
        with self.assertRaises(module.ServiceAssociationError) as caught:
            module.resolve_service_associations(value, evaluated, maximum)
        self.assertEqual(caught.exception.code, code)
        self.assertEqual(str(caught.exception), code)
        self.assertEqual(value, before)

    def rejection(self, value, code):
        before = copy.deepcopy(value)
        result = resolve(value)
        self.assertEqual(result["association_count"], 0)
        self.assertEqual(result["rejection_count"], 1)
        self.assertEqual(result["rejections"][0]["reason"], code)
        self.assertEqual(value, before)
        module.validate_service_association_envelope(result)
        return result["rejections"][0]

    def test_valid_systemd_strong_owner_existing_ids_and_provenance(self):
        result = resolve()
        self.assertEqual(result["association_count"], 1)
        self.assertEqual(result["rejection_count"], 0)
        item = result["service_associations"][0]
        self.assertEqual(item["service_id"], SERVICE)
        self.assertEqual(item["stable_device_id"], OWNER)
        self.assertEqual(item["source_type"], "systemd")
        self.assertEqual(item["association_basis"], "existing_service_ownership")
        self.assertEqual(item["confidence"], "high")
        self.assertEqual(item["collection_provenance"]["inventory_updated"], result["inventory_updated"])
        self.assertRegex(item["collection_provenance"]["inventory_snapshot_sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(result["max_snapshot_age_seconds"], 60)

    def test_multiple_services_one_owner_and_all_ss_services(self):
        observations = [service(), service("svc_ssh_00000000", service_type="ssh")]
        for sid, kind in [("svc_mqtt_listener", "mqtt"), ("svc_network_53", "dns"), ("svc_network_67", "dhcp")]:
            observations.append(service(sid, "ss", service_type=kind))
        result = resolve(snapshot(observations))
        self.assertEqual(result["association_count"], 5)
        self.assertEqual({x["stable_device_id"] for x in result["service_associations"]}, {OWNER})
        self.assertEqual({x["service_id"] for x in result["service_associations"]}, {x["id"] for x in observations})

    def test_normalized_mac_reuses_existing_identity_semantics(self):
        result = resolve(snapshot(devices=[device(" 02-00-00-00-00-01 ", OWNER)]))
        self.assertEqual(result["service_associations"][0]["stable_device_id"], OWNER)

    def test_identical_consumed_duplicates_deduplicate_without_rejection(self):
        a = service();b = dict(a, status="active", name="another synthetic label")
        result = resolve(snapshot([a, b, a]))
        self.assertEqual((result["association_count"], result["rejection_count"]), (1, 0))
        self.assertEqual(result["service_associations"][0]["service_id"], SERVICE)

    def test_repeated_and_reordered_inputs_have_identical_output_bytes(self):
        a = snapshot([service(), service("svc_ssh_00000000", owner=SECOND_OWNER, service_type="ssh")], [device(), device(SECOND_MAC)])
        b = copy.deepcopy(a);b["devices"].reverse();b["services"].reverse()
        encode = lambda v: json.dumps(v, sort_keys=True, separators=(",", ":"))
        self.assertEqual(encode(resolve(a)), encode(resolve(a)))
        self.assertEqual(encode(resolve(a)), encode(resolve(b)))

    def test_null_id_rejections_with_distinct_safe_references_are_order_independent(self):
        a = dict(service(), id="synthetic-invalid-a")
        b = dict(service(owner=SECOND_OWNER), id="synthetic-invalid-b", source="ss")
        one = snapshot([a, b], [device(), device(SECOND_MAC)])
        two = copy.deepcopy(one);two["services"].reverse();two["devices"].reverse()
        self.assertEqual(resolve(one), resolve(two))
        self.assertEqual(resolve(one)["rejection_count"], 2)
        self.assertTrue(all(item["service_id"] is None for item in resolve(one)["rejections"]))

    def test_envelope_total_results_cannot_exceed_input_record_limit(self):
        value = resolve(snapshot([service(), service("svc_ssh_00000000", owner=SECOND_OWNER, service_type="ssh")]))
        self.assertEqual((value["association_count"], value["rejection_count"]), (1, 1))
        with patch.object(module, "MAX_RECORDS", 1), self.assertRaises(module.ServiceAssociationError):
            module.validate_service_association_envelope(value)

    def test_ids_stable_across_snapshot_cycles(self):
        a = snapshot();b = snapshot();b["updated"] = "2026-10-12T12:00:01Z"
        one = resolve(a)["service_associations"][0];two = resolve(b, b["updated"])["service_associations"][0]
        self.assertEqual(one["association_id"], two["association_id"])
        self.assertNotEqual(one["collection_provenance"], two["collection_provenance"])

    def test_missing_owner(self):
        result = self.rejection(snapshot(devices=[]), "MISSING_OWNER")
        self.assertEqual(result["owner_reference"], OWNER)
        self.assertEqual(result["source_type"], "systemd")

    def test_ip_hostname_service_label_and_port_cannot_supply_identity(self):
        for hints in [{"ip": "192.0.2.1"}, {"hostname": "collector"}, {"name": "cron", "port": 1883}]:
            weak = dict(id=OWNER, **hints)
            with self.subTest(hints=hints):self.rejection(snapshot(devices=[weak]), "WEAK_OWNER")

    def test_ambiguous_duplicate_owner_id_even_identical(self):
        self.rejection(snapshot(devices=[device(), device()]), "AMBIGUOUS_OWNER")

    def test_mac_collision_rejects_instead_of_selecting_first(self):
        self.rejection(snapshot(devices=[device(), device(MAC, SECOND_OWNER)]), "OWNER_MAC_COLLISION")

    def test_malformed_mac(self):
        self.rejection(snapshot(devices=[device("not-a-mac", OWNER)]), "MALFORMED_MAC")

    def test_nonstring_mac_is_not_coerced_into_authority(self):
        value = snapshot();value["devices"][0]["mac"] = {"private": "value"}
        self.rejection(value, "MALFORMED_DEVICE")

    def test_device_id_must_match_mac_derived_existing_id(self):
        self.rejection(snapshot(devices=[device(SECOND_MAC, OWNER)]), "OWNER_ID_MISMATCH")

    def test_conflicting_service_ownership_rejects_all_same_id(self):
        a = service();b = service(owner=SECOND_OWNER)
        result = self.rejection(snapshot([a, b], [device(), device(SECOND_MAC)]), "CONFLICTING_SERVICE_ID")
        self.assertIsNone(result["owner_reference"])

    def test_conflicting_same_id_source_or_type(self):
        for field, new in [("type", "ssh"), ("source", "ss")]:
            a = service();b = dict(a);b[field] = new
            with self.subTest(field=field):self.rejection(snapshot([a, b]), "CONFLICTING_SERVICE_ID")

    def test_malformed_same_id_cannot_hide_behind_valid_duplicate(self):
        a = service();b = dict(a, port=True)
        self.rejection(snapshot([a, b]), "CONFLICTING_SERVICE_ID")

    def test_unsupported_source_and_unknown_source_not_echoed(self):
        for source in ["mqtt_discovery", "home_assistant", "scanner", "http", "snmp", "secret-token-value"]:
            with self.subTest(source=source):
                row = self.rejection(snapshot([dict(service(), source=source)]), "UNSUPPORTED_SOURCE")
                self.assertIsNone(row["source_type"])
                self.assertNotIn(source, json.dumps(row))

    def test_unsupported_service_type(self):
        self.rejection(snapshot([dict(service(), type="fingerprint")]), "UNSUPPORTED_SERVICE_TYPE")

    def test_invalid_service_id_is_null_and_never_echoed(self):
        for sid in [None, "secret-token-value", "dev_0123456789abcdef", "svc_scheduler_01234567\n", {}, 42]:
            with self.subTest(sid=sid):
                row = self.rejection(snapshot([dict(service(), id=sid)]), "INVALID_SERVICE_ID")
                self.assertIsNone(row["service_id"])
                self.assertNotIn("secret-token-value", json.dumps(row))

    def test_malformed_service_objects(self):
        for record in [None, [], "private text", 3, dict(service(), device_id=None), dict(service(), status=[]), dict(service(), port=True)]:
            with self.subTest(record=record):self.rejection(snapshot([record]), "MALFORMED_SERVICE")

    def test_service_extension_is_closed(self):
        self.rejection(snapshot([dict(service(), credential="do-not-echo")]), "UNEXPECTED_SERVICE_FIELD")

    def test_source_id_type_and_socket_port_must_agree(self):
        for record in [service("svc_mqtt_listener"), dict(service("svc_network_53", "ss", service_type="dns"), port=67), service(SERVICE, service_type="ssh")]:
            with self.subTest(record=record):self.rejection(snapshot([record]), "SOURCE_ID_TYPE_MISMATCH")

    def test_malformed_snapshot_top_level_and_schema(self):
        for value in [None, [], {}, dict(snapshot(), schema_version="2.0"), dict(snapshot(), devices={}), dict(snapshot(), services={}), dict(snapshot(), summary=[]), dict(snapshot(), topology=[])]:
            with self.subTest(value=value):self.reject(value, "SNAPSHOT_INVALID")

    def test_required_snapshot_timestamp_missing(self):
        value = snapshot();del value["updated"]
        self.reject(value, "SNAPSHOT_INVALID")

    def test_invalid_snapshot_and_evaluation_timestamps(self):
        for timestamp in ["", "yesterday", "2026-10-12", "2026-10-12T12:00:00", "2026-02-30T12:00:00Z", "2026-10-12T12:00:00+99:00"]:
            with self.subTest(timestamp=timestamp):
                self.reject(dict(snapshot(), updated=timestamp), "INVALID_SNAPSHOT_TIME")
                self.reject(snapshot(), "INVALID_EVALUATION_TIME", evaluated=timestamp)
        for timestamp in [None, 1, {}, datetime(2026, 10, 12)]:
            self.reject(snapshot(), "INVALID_EVALUATION_TIME", evaluated=timestamp)

    def test_future_and_stale_snapshots(self):
        self.reject(snapshot(), "SNAPSHOT_FUTURE", evaluated="2026-10-12T11:59:59Z")
        self.reject(snapshot(), "SNAPSHOT_STALE", evaluated="2026-10-12T12:01:01Z")

    def test_exact_age_boundary_zero_and_microsecond(self):
        self.assertEqual(resolve(maximum=0)["association_count"], 1)
        self.assertEqual(resolve(evaluated="2026-10-12T12:01:00Z")["association_count"], 1)
        self.reject(snapshot(), "SNAPSHOT_STALE", evaluated="2026-10-12T12:01:00.000001Z")

    def test_timezone_equivalence(self):
        a = resolve(evaluated="2026-10-12T06:00:00-06:00")
        self.assertEqual(a, resolve())

    def test_policy_is_required_explicit_integer_not_boolean(self):
        for maximum in [None, True, False, -1, 1.0, "60", {}, module.MAX_POLICY_INTEGER + 1]:
            with self.subTest(maximum=maximum):self.reject(snapshot(), "INVALID_MAX_SNAPSHOT_AGE", maximum=maximum)
        with self.assertRaises(TypeError):module.resolve_service_associations(snapshot(), NOW)

    def test_device_records_without_traceable_id_invalidate_whole_snapshot(self):
        for value in [None, {}, {"id": "unsafe"}, {"id": OWNER, "mac": MAC}, []]:
            if value == {"id": OWNER, "mac": MAC}:continue
            with self.subTest(value=value):self.reject(snapshot(devices=[value]), "SNAPSHOT_DEVICE_INVALID")

    def test_empty_collections_do_not_assert_health_success_or_absence(self):
        result = resolve(snapshot(services=[]))
        self.assertEqual((result["association_count"], result["rejection_count"]), (0, 0))
        self.assertEqual(result["service_associations"], [])
        text = json.dumps(result)
        for term in ["healthy", "collection_success", "service_absent", "outage", "expected_availability"]:self.assertNotIn(term, text)

    def test_inputs_all_protected_fields_unchanged_and_no_data_leaks(self):
        value = snapshot();before = copy.deepcopy(value);result = resolve(value)
        self.assertEqual(value, before)
        text = json.dumps(result)
        for term in [MAC, "192.0.2.1", "synthetic private note", "synthetic label", '"status"', '"home_assistant"', '"observed_at"']:self.assertNotIn(term, text)
        result["service_associations"][0]["collection_provenance"]["inventory_updated"] = "mutated"
        self.assertEqual(value, before)

    def test_record_and_payload_limits_fail_instead_of_truncating(self):
        self.reject(snapshot(services=[service()] * (module.MAX_RECORDS + 1)), "SNAPSHOT_LIMIT_EXCEEDED")
        self.reject(snapshot(devices=[device()] * (module.MAX_RECORDS + 1)), "SNAPSHOT_LIMIT_EXCEEDED")
        with patch.object(module, "MAX_SNAPSHOT_BYTES", 20):self.reject(snapshot(), "SNAPSHOT_LIMIT_EXCEEDED")

    def test_non_json_input_and_nan_rejected_with_safe_code(self):
        for value in [object(), float("nan"), set([1])]:
            input_value = snapshot();input_value["private"] = value
            with self.assertRaises(module.ServiceAssociationError) as caught:resolve(input_value)
            self.assertEqual(str(caught.exception), "SNAPSHOT_INVALID")

    def test_invalid_and_rejected_records_are_not_silently_dropped(self):
        value = snapshot([None, None, dict(service(), source="unsupported"), service("svc_ssh_00000000", service_type="ssh")])
        result = resolve(value)
        self.assertEqual((result["association_count"], result["rejection_count"]), (1, 3))
        self.assertTrue(all("collection_provenance" in x for x in result["rejections"]))

    def test_envelope_closed_at_every_object(self):
        result = resolve()
        paths = [(), ("service_associations", 0), ("service_associations", 0, "collection_provenance")]
        for path in paths:
            bad = copy.deepcopy(result);target = bad
            for key in path:target = target[key]
            target["secret_extension"] = "private"
            with self.subTest(path=path),self.assertRaises(module.ServiceAssociationError):module.validate_service_association_envelope(bad)
        rejected = resolve(snapshot(devices=[]))
        rejected["rejections"][0]["extra"] = "private"
        with self.assertRaises(module.ServiceAssociationError):module.validate_service_association_envelope(rejected)

    def test_envelope_count_uniqueness_provenance_and_identity_checks(self):
        value = resolve()
        mutations = [lambda b:b.update(association_count=True), lambda b:b.update(association_count=2), lambda b:b.update(schema_version="2.0"), lambda b:b["service_associations"][0].update(association_id="lsa_"+"0"*64), lambda b:b["service_associations"][0]["collection_provenance"].update(inventory_updated="2026-10-12T11:00:00Z")]
        for mutation in mutations:
            bad = copy.deepcopy(value);mutation(bad)
            with self.assertRaises(module.ServiceAssociationError):module.validate_service_association_envelope(bad)
        bad = copy.deepcopy(value);bad["service_associations"] *= 2;bad["association_count"] = 2
        with self.assertRaises(module.ServiceAssociationError):module.validate_service_association_envelope(bad)

    def test_schema_artifact_matches_pure_contract(self):
        stored = json.loads((ROOT / "governance/pe5/pe5-local-service-association-envelope.schema.json").read_bytes())
        self.assertEqual(stored, module.contract_schema())
        schema = module.contract_schema();schema["additionalProperties"] = True
        self.assertFalse(module.contract_schema()["additionalProperties"])

    def test_no_io_clock_environment_network_or_subprocess_at_resolve(self):
        class NoEnvironment:
            def __getitem__(self, key):raise AssertionError("environment read")
            def get(self, *args):raise AssertionError("environment read")
            def __iter__(self):raise AssertionError("environment read")
        class ExplicitTime:
            fromisoformat = staticmethod(datetime.fromisoformat)
            def now(*args):raise AssertionError("clock read")
            def utcnow(*args):raise AssertionError("clock read")
        expected = resolve()
        with patch.object(os, "environ", NoEnvironment()), patch("os.getenv", side_effect=AssertionError("environment")), patch("builtins.open", side_effect=AssertionError("filesystem")), patch("socket.socket", side_effect=AssertionError("network")), patch("socket.create_connection", side_effect=AssertionError("network")), patch("subprocess.run", side_effect=AssertionError("subprocess")), patch.object(module, "datetime", ExplicitTime):
            self.assertEqual(resolve(), expected)

    def test_new_module_initialization_has_no_business_io(self):
        source = (ROOT / "pi4/lib/hioc/service_association.py").read_text()
        compiled = compile(source, "service_association.py", "exec")
        namespace = {"__name__": "hioc.service_association_isolated", "__package__": "hioc"}
        with patch("builtins.open", side_effect=AssertionError("filesystem")), patch("socket.create_connection", side_effect=AssertionError("network")), patch("subprocess.run", side_effect=AssertionError("subprocess")), patch("os.getenv", side_effect=AssertionError("environment")):
            exec(compiled, namespace)
            self.assertEqual(namespace["resolve_service_associations"](snapshot(), NOW, 60), resolve())

    def test_library_imports_only_pure_dependencies_and_existing_identity_functions(self):
        tree = ast.parse((ROOT / "pi4/lib/hioc/service_association.py").read_text())
        imports = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))]
        names = {alias.name for n in imports if isinstance(n, ast.Import) for alias in n.names}
        self.assertEqual(names, {"hashlib", "json", "math", "re"})
        identity = next(n for n in imports if isinstance(n, ast.ImportFrom) and n.module == "inventory")
        self.assertEqual({x.name for x in identity.names}, {"normalize_mac", "stable_device_id"})

    def test_runtime_consumers_remain_identical_to_authorized_baseline(self):
        paths = ["pi4/bin/hioc-inventory-engine.py", "pi4/lib/hioc/inventory.py", "pi4/lib/hioc/mqtt.py", "pi4/lib/hioc/assets.py", "pi4/lib/hioc/home_assistant_association.py", "pi4/lib/hioc/home_assistant_public_projection.py", "pi4/lib/hioc/core/correlation.py", "pi4/bin/hioc-history-engine.py", "homeassistant/packages/hioc_living_inventory.yaml"]
        for path in paths:
            original = subprocess.check_output(["git", "show", "f3730ba5a8745361934ff822a9c29c16c9d0767b:" + path], cwd=ROOT)
            self.assertEqual((ROOT / path).read_bytes().replace(b"\r\n", b"\n"), original, path)


# Current implementation governance; accepted preparation stays a historical Git package.
import hashlib
from functools import lru_cache

IMPLEMENTATION_BASE = "f3730ba5a8745361934ff822a9c29c16c9d0767b"
IMPLEMENTATION_RECORD = "governance/pe5/pe5-local-service-association-implementation.json"
IMPLEMENTATION_SCHEMA = IMPLEMENTATION_RECORD.replace(".json", ".schema.json")
IMPLEMENTATION_PATHS = tuple(sorted([
    "pi4/lib/hioc/service_association.py",
    "governance/pe5/pe5-local-service-association-envelope.schema.json",
    "tests/test_pe5_local_service_association.py",
    "docs/PE5_LOCAL_SERVICE_ASSOCIATION_IMPLEMENTATION.md",
    IMPLEMENTATION_RECORD, IMPLEMENTATION_SCHEMA,
    "docs/HIOC_MASTER_PLAN.md", "docs/PASSIVE_ENRICHMENT_ARCHITECTURE.md",
    "tests/test_pe5_implementation_preparation.py",
    "tests/test_pe4_ha_association_public_projection_test_binding_correction.py",
]))
IMPLEMENTATION_LIFECYCLE = dict(phase7a="ACTIVE", pe4="PASS/CLOSED", public_projection="PASS/CLOSED",
    documentation_consistency_correction="PASS/CLOSED", pe5_preparation="COMMITTED_PREPARED_FOR_REVIEW",
    pe5_1="IMPLEMENTED_REPOSITORY_CANDIDATE", pe5="IN_PROGRESS_REPOSITORY_ONLY", surveillance="PLANNED_NOT_STARTED")
FORBIDDEN_ACTIVITY = ["production", "deployment", "runtime_integration", "collection", "persistence", "scheduler",
    "mqtt_publish", "mqtt_subscribe", "public_projection", "identity_changes", "canonical_ip_changes",
    "liveness_changes", "health_changes", "assets_changes", "incident_changes", "graph_changes", "active_discovery", "surveillance"]


def evidence_git(*args):
    return subprocess.check_output(["git", "--no-optional-locks", *args], cwd=ROOT,
        env=dict(os.environ, GIT_OPTIONAL_LOCKS="0"), stderr=subprocess.PIPE)


def evidence_bytes(path):
    return (ROOT/path).read_bytes().replace(b"\r\n", b"\n")


def evidence_digest(raw):return hashlib.sha256(raw).hexdigest()
def evidence_blob(raw):return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
def evidence_canonical(v):return (json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False)+"\n").encode()
def evidence_closed(v):
    if type(v) is dict:return dict(type="object", additionalProperties=False, required=sorted(v), properties={k:evidence_closed(x) for k,x in sorted(v.items())})
    if type(v) is list:return dict(type="array", minItems=len(v), maxItems=len(v), prefixItems=[evidence_closed(x) for x in v], items=False)
    return dict(const=v)
def evidence_schema(record):
    return {"$schema":"https://json-schema.org/draft/2020-12/schema", "title":"PE-5.1 local service association implementation", **evidence_closed(record)}
def evidence_require(value, message):
    if not value:raise ValueError(message)


def _validate_historical_implementation(record, schema):
    evidence_require(evidence_canonical(schema)==evidence_canonical(evidence_schema(record)), "exact typed implementation schema mismatch")
    evidence_require(record["predecessor_commit"]==IMPLEMENTATION_BASE and record["authorized_paths"]==list(IMPLEMENTATION_PATHS), "wrong implementation scope")
    evidence_require(record["status"]=="IMPLEMENTED_REPOSITORY_CANDIDATE" and record["lifecycle"]==IMPLEMENTATION_LIFECYCLE, "wrong implementation lifecycle")
    evidence_require(record["repository_implementation_authorized"] is True and record["runtime_integration_authorized"] is False and record["production_authorized"] is False, "implementation authority expanded")
    evidence_require(record["forbidden_activity"]==dict.fromkeys(FORBIDDEN_ACTIVITY, False), "forbidden runtime authority")
    evidence_require(record["snapshot_age_policy"]=="UNKNOWN_REQUIRED_BEFORE_OPERATIONAL_USE" and record["eligible_sources"]==["systemd", "ss"], "policy or source expansion")
    evidence_require(record["current_next_task"]=="PE5_1_IMPLEMENTATION_CANDIDATE_REVIEW", "wrong next task")
    evidence_require(record["first_checkpoint"]=="PE-5.1 - Private Local Service Association Contract and Pure Resolver", "wrong checkpoint")
    evidence_require(not evidence_git("diff", "--cached", "--name-only") and not evidence_git("stash", "list"), "staging or stash changed")
    head=evidence_git("rev-parse", "HEAD").decode().strip()
    if head==IMPLEMENTATION_BASE:
        evidence_require(evidence_git("rev-parse", "origin/main").decode().strip()==IMPLEMENTATION_BASE, "baseline tracking changed")
        changed=set(evidence_git("diff", "--name-only", IMPLEMENTATION_BASE).decode().splitlines())
        changed.update(evidence_git("ls-files", "--others", "--exclude-standard").decode().splitlines())
    else:
        evidence_require(evidence_git("rev-parse", "HEAD^").decode().strip()==IMPLEMENTATION_BASE and not evidence_git("status", "--porcelain"), "wrong committed successor")
        changed=set(evidence_git("diff", "--name-only", IMPLEMENTATION_BASE, head).decode().splitlines())
    evidence_require(changed==set(IMPLEMENTATION_PATHS), "unexpected implementation path")
    evidence_require(len(record["artifacts"])==len(IMPLEMENTATION_PATHS)-2 and {x["path"] for x in record["artifacts"]}==set(IMPLEMENTATION_PATHS)-{IMPLEMENTATION_RECORD, IMPLEMENTATION_SCHEMA}, "incomplete current map")
    for item in record["artifacts"]:
        raw=evidence_bytes(item["path"])
        evidence_require(evidence_digest(raw)==item["sha256"] and evidence_blob(raw)==item["git_blob"], "implementation artifact identity mismatch")
    for item in record["source_bindings"]+record["historical_artifacts"]:
        raw=evidence_git("show", IMPLEMENTATION_BASE+":"+item["path"])
        evidence_require(evidence_digest(raw)==item["sha256"] and evidence_blob(raw)==item["git_blob"], "historical source identity mismatch")
        if item["path"] not in IMPLEMENTATION_PATHS:evidence_require(evidence_bytes(item["path"])==raw, "immutable source changed")
    old=evidence_git("show", IMPLEMENTATION_BASE+":docs/HIOC_MASTER_PLAN.md").decode().splitlines(keepends=True);candidate=list(old)
    evidence_require(len(record["master_insertions"])==5, "unexpected master edit shape")
    for item in sorted(record["master_insertions"], key=lambda x:x["after_line"], reverse=True):
        evidence_require(evidence_digest(old[item["after_line"]-1].rstrip("\n").encode())==item["anchor_sha256"], "master anchor changed")
        candidate[item["after_line"]:item["after_line"]]=[item["text"]+"\n"]
    evidence_require("".join(candidate).encode()==evidence_bytes("docs/HIOC_MASTER_PLAN.md"), "old master content changed")
    master=evidence_bytes("docs/HIOC_MASTER_PLAN.md").decode()
    for marker in ["## Current Objective", "## Next Planned Task"]:
        section=master.split(marker,1)[1].split("### Historical",1)[0]
        for phrase in ["PE-5.1", "NOT AUTHORIZED", "Phase 7A ACTIVE", "PE-4 PASS/CLOSED", "Public Projection PASS/CLOSED", "UNKNOWN_REQUIRED_BEFORE_OPERATIONAL_USE"]:
            evidence_require(phrase in section, "current sequencing or invariant missing")
    edit=record["architecture_edit"];original=evidence_git("show", IMPLEMENTATION_BASE+":docs/PASSIVE_ENRICHMENT_ARCHITECTURE.md").decode()
    evidence_require(original.replace(edit["needle"],edit["replacement"])+edit["append"]==evidence_bytes("docs/PASSIVE_ENRICHMENT_ARCHITECTURE.md").decode(), "unrelated architecture change")
    old_prep=ast.parse(evidence_git("show", IMPLEMENTATION_BASE+":tests/test_pe5_implementation_preparation.py"));current_prep=ast.parse(evidence_bytes("tests/test_pe5_implementation_preparation.py"))
    f=lambda tree,name:next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name)
    evidence_require([ast.dump(x,include_attributes=False) for x in f(old_prep,"validate_record").body]==[ast.dump(x,include_attributes=False) for x in f(current_prep,"_validate_historical_preparation").body], "historical preparation validator weakened")
    original_master="".join(old);extract=lambda t:t.split("<!-- ORIGINAL_SURVEILLANCE_SPECIFICATION_BEGIN -->\n```text\n",1)[1].split("```\n<!-- ORIGINAL_SURVEILLANCE_SPECIFICATION_END -->",1)[0]
    evidence_require(extract(master)==extract(original_master), "original surveillance source changed")
    historical_roadmap=json.loads(evidence_git("show", IMPLEMENTATION_BASE+":governance/pe4/pe10-surveillance-roadmap-preservation.json"))
    evidence_require(historical_roadmap["original_specification"]["testing_clarification"] in master.split("# Decision Log",1)[1], "surveillance testing clarification changed")
    evidence_require(json.loads(evidence_bytes("governance/pe5/pe5-local-service-association-envelope.schema.json"))==module.contract_schema(), "private envelope schema drift")
    return record


ACCEPTED_IMPLEMENTATION = "e30e483d7e5ede1cde1f75bc25bc65ff4ec115b1"

def implementation_historical_bytes(path):
    return evidence_git("show", ACCEPTED_IMPLEMENTATION+":"+path)

def validate_implementation_record(record, schema):
    original_git = evidence_git
    def historical_git(*args):
        if args == ("rev-parse", "HEAD"):return (ACCEPTED_IMPLEMENTATION+"\n").encode()
        if args == ("rev-parse", "HEAD^"):return (IMPLEMENTATION_BASE+"\n").encode()
        if args in [("status", "--porcelain"), ("diff", "--cached", "--name-only"), ("stash", "list")]:return b""
        return original_git(*args)
    with patch.dict(globals(), evidence_git=historical_git, evidence_bytes=implementation_historical_bytes):
        return _validate_historical_implementation(record, schema)


@lru_cache(maxsize=1)
def implementation_successor():
    raw=implementation_historical_bytes(IMPLEMENTATION_RECORD);schema_raw=implementation_historical_bytes(IMPLEMENTATION_SCHEMA);r=json.loads(raw);s=json.loads(schema_raw)
    evidence_require(raw==evidence_canonical(r) and schema_raw==evidence_canonical(s), "noncanonical implementation record")
    return validate_implementation_record(r,s)


def implementation_current_binding(path):
    from test_pe5_service_association_caller import CALLER_PATHS, caller_current_binding
    if path in CALLER_PATHS:return caller_current_binding(path)
    record=implementation_successor();item=next((x for x in record["artifacts"] if x["path"]==path),None)
    evidence_require(item is not None,"path outside implementation map")
    raw=evidence_bytes(path);evidence_require(evidence_digest(raw)==item["sha256"] and evidence_blob(raw)==item["git_blob"],"current implementation identity mismatch")
    return item


def _assert_historical_implementation_sequence(text):
    implementation_current_binding("docs/HIOC_MASTER_PLAN.md")
    current=text.split("## Next Planned Task",1)[1].split("### Historical",1)[0]
    evidence_require(current.strip().startswith("### PE-5.1 private resolver"), "missing current implementation checkpoint")
    evidence_require("NOT AUTHORIZED" in current and "UNKNOWN_REQUIRED_BEFORE_OPERATIONAL_USE" in current, "runtime or policy gate absent")


def assert_implementation_sequence(text):
    from test_pe5_service_association_caller import assert_caller_sequence
    return assert_caller_sequence(text)


class LocalServiceImplementationGovernanceTests(unittest.TestCase):
    def test_exact_implementation_contract_and_bindings(self):implementation_successor()
    def test_preparation_history_closed_work_and_runtime_authority_preserved(self):
        r=implementation_successor();self.assertFalse(r["runtime_integration_authorized"]);self.assertFalse(r["production_authorized"])
        self.assertEqual(r["lifecycle"]["pe4"],"PASS/CLOSED");self.assertEqual(r["snapshot_age_policy"],"UNKNOWN_REQUIRED_BEFORE_OPERATIONAL_USE")
    def test_reject_source_scope_policy_and_authority_expansion(self):
        for field,value in [("eligible_sources",["systemd","ss","mqtt"]),("snapshot_age_policy",300),("production_authorized",True),("runtime_integration_authorized",True),("current_next_task","DEPLOY_NOW")]:
            bad=copy.deepcopy(implementation_successor());bad[field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):validate_implementation_record(bad,evidence_schema(bad))
    def test_reject_each_operational_side_effect_authority(self):
        for field in FORBIDDEN_ACTIVITY:
            bad=copy.deepcopy(implementation_successor());bad["forbidden_activity"][field]=True
            with self.subTest(field=field),self.assertRaises(ValueError):validate_implementation_record(bad,evidence_schema(bad))
    def test_reject_extra_mutation_and_stale_artifact(self):
        bad=copy.deepcopy(implementation_successor());bad["authorized_paths"].append("pi4/bin/hioc-inventory-engine.py")
        with self.assertRaises(ValueError):validate_implementation_record(bad,evidence_schema(bad))
        bad=copy.deepcopy(implementation_successor());bad["artifacts"][0]["sha256"]="0"*64
        with self.assertRaises(ValueError):validate_implementation_record(bad,evidence_schema(bad))
    def test_reject_open_or_stale_exact_schema(self):
        r=implementation_successor();s=evidence_schema(r);s["additionalProperties"]=True
        with self.assertRaises(ValueError):validate_implementation_record(r,s)


if __name__ == "__main__":
    unittest.main()
