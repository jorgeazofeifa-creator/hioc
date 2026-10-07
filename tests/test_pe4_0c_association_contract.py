"""Frozen architecture only: synthetic fixtures, no production adapter or network."""
import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "governance/pe4/pe4-0c-association-contract.json"
CONTRACT = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
STATE_SCHEMA = json.loads((ROOT / CONTRACT["state_schema"]).read_text(encoding="utf-8"))
CONTRACT_SCHEMA = json.loads((ROOT / "governance/pe4/pe4-0c-association-contract.schema.json").read_text(encoding="utf-8"))
TS = "2026-10-06T12:00:00Z"

def validate_schema(value, schema, root=None):
    """Independent executor for every JSON Schema keyword in this one fixture.

    Kept test-only: the standalone client uses its own stricter final validator.
    Unknown keywords fail the test rather than silently weakening validation.
    """
    root = root or schema
    allowed = {'$schema','$id','$defs','$ref','title','type','const','enum','properties',
               'additionalProperties','required','items','minItems','maxItems','uniqueItems',
               'minimum','maximum','minLength','maxLength','pattern','anyOf','allOf','if','then','else'}
    if set(schema)-allowed: raise AssertionError('unhandled schema keyword')
    if '$ref' in schema:
        target=root
        for part in schema['$ref'].removeprefix('#/').split('/'): target=target[part]
        validate_schema(value,target,root)
    if 'const' in schema and (type(value) is not type(schema['const']) or value != schema['const']): raise ValueError()
    if 'enum' in schema and not any(type(value) is type(x) and value==x for x in schema['enum']): raise ValueError()
    if 'anyOf' in schema:
        for branch in schema['anyOf']:
            try: validate_schema(value,branch,root); break
            except ValueError: pass
        else: raise ValueError()
    for branch in schema.get('allOf',[]): validate_schema(value,branch,root)
    if 'if' in schema:
        try: validate_schema(value,schema['if'],root); branch='then'
        except ValueError: branch='else'
        if branch in schema: validate_schema(value,schema[branch],root)
    types={'object':dict,'array':list,'string':str,'boolean':bool,'integer':int,'null':type(None)}
    if 'type' in schema and type(value) is not types[schema['type']]: raise ValueError()
    if type(value) is dict:
        props=schema.get('properties',{})
        if not set(schema.get('required',[])).issubset(value): raise ValueError()
        if schema.get('additionalProperties') is False and set(value)-set(props): raise ValueError()
        for key,item in value.items():
            if key in props: validate_schema(item,props[key],root)
    if type(value) is list:
        if len(value)<schema.get('minItems',0) or len(value)>schema.get('maxItems',10**9): raise ValueError()
        if schema.get('uniqueItems') and len({json.dumps(x,sort_keys=True) for x in value})!=len(value): raise ValueError()
        if 'items' in schema:
            for item in value: validate_schema(item,schema['items'],root)
    if type(value) is int:
        if value<schema.get('minimum',-10**30) or value>schema.get('maximum',10**30): raise ValueError()
    if type(value) is str:
        if len(value)<schema.get('minLength',0) or len(value)>schema.get('maxLength',10**9): raise ValueError()
        if 'pattern' in schema and not re.search(schema['pattern'],value): raise ValueError()


def reference_decision(devices, selected, hioc, prior=None):
    """Test-only decision table for contract reasoning, not runtime implementation."""
    prior = prior or {}
    parsed = {}
    for device in devices:
        if not isinstance(device.get("id"), str) or not device["id"]:
            return "REJECT_STRUCTURAL_CONTRACT"
        pairs = device.get("connections")
        if not isinstance(pairs, list) or any(not isinstance(p, list) or len(p) != 2 or any(not isinstance(x, str) for x in p) for p in pairs):
            return "REJECT_STRUCTURAL_CONTRACT"
        if device["id"] in parsed:
            return "REJECT_STRUCTURAL_CONTRACT"
        macs, invalid = set(), False
        for namespace, value in pairs:
            if namespace != "mac":
                continue
            normalized = value.strip().lower().replace("-", ":")
            if not re.fullmatch(r"[0-9a-f]{2}(?::[0-9a-f]{2}){5}", normalized):
                invalid = True
            else:
                macs.add(normalized)
        parsed[device["id"]] = (macs, invalid)
    macs, invalid = parsed[selected]
    if invalid:
        return "REJECT_INVALID_MAC"
    if not macs:
        return "REVIEW_ONLY_NO_MAC"
    if len(macs) != 1:
        return "REVIEW_ONLY_MULTIPLE_MAC"
    mac = next(iter(macs))
    if sum(mac in values for values, _ in parsed.values()) != 1:
        return "REJECT_HA_MAC_COLLISION"
    matches = [d["id"] for d in hioc if d.get("mac") == mac]
    if len(matches) > 1:
        return "REJECT_HIOC_MAC_AMBIGUITY"
    if not matches:
        return "UNMATCHED_STRONG_EVIDENCE"
    target = matches[0]
    if (selected in prior and prior[selected] != target) or any(ha != selected and bound == target for ha, bound in prior.items()):
        return "REJECT_PRIOR_BINDING_CONFLICT"
    return "ASSOCIATED_STRONG_MAC"


def fixture():
    return {"schema_version": "1.0", "updated_at": TS, "instance_reference": "PI5_HA",
            "observed_ha_version": "2026.9.4", "contract_version": "1.0",
            "associations": [{"hioc_device_id": "dev_0123456789abcdef", "ha_device_id": "synthetic-device",
                              "association_basis": "unique_mac", "status": "ASSOCIATED_STRONG_MAC",
                              "first_associated_at": TS, "last_confirmed_at": TS,
                              "observed_ha_version": "2026.9.4", "contract_version": "1.0",
                              "relationship_status": "COMPLETE"}],
            "summary": {"associated_devices": 1, "entity_memberships": 0, "review_only": 0, "rejected": 0, "unmatched": 0},
            "diagnostics": []}


class AssociationContractTests(unittest.TestCase):
    def test_canonical_artifacts_and_contract_schema(self):
        for path in (CONTRACT_PATH, ROOT / CONTRACT["state_schema"], ROOT / "governance/pe4/pe4-0c-association-contract.schema.json"):
            value = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(path.read_text(encoding="utf-8"), json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n")
        validate_schema(CONTRACT, CONTRACT_SCHEMA)
        for key, value in (("creates_hioc_identity", True), ("lifecycle_state", "NOT_STARTED"), ("source_structure_fingerprint", "wrong")):
            bad = copy.deepcopy(CONTRACT); bad[key] = value
            with self.assertRaises(ValueError): validate_schema(bad, CONTRACT_SCHEMA)

    def test_authoritative_evidence_bindings(self):
        self.assertEqual(CONTRACT["record_type"], "PE4_0C_ASSOCIATION_CONTRACT")
        self.assertEqual(CONTRACT["lifecycle_state"], "PASS_CLOSED")
        self.assertEqual(CONTRACT["status"], "FROZEN")
        self.assertEqual(CONTRACT["source_structure_fingerprint"], "fef567f29e545e1b7c03b4a8c585f0b03b6ea8b588c5502acb5ce51e809d9b1d")
        self.assertEqual(CONTRACT["source_2b_report_sha256"], "322e237404c3c721be782e9ce2dbc4ceb1e63b8374af00b6fe75a940624d2ded")
        closure = json.loads((ROOT / CONTRACT["source_2b_closure"]).read_text())
        self.assertEqual(hashlib.sha256((ROOT / CONTRACT["source_2b_closure"]).read_text().encode()).hexdigest(), CONTRACT["source_2b_closure_sha256"])
        self.assertEqual(closure["evidence_report_sha256"], CONTRACT["source_2b_report_sha256"])
        self.assertEqual(closure["evidence_result_sha256"], CONTRACT["source_2b_result_sha256"])
        self.assertEqual(CONTRACT["observed_ha_core_version"], "2026.9.4")
        self.assertEqual(CONTRACT["core_source_baseline"], "2026.8.1")
        self.assertEqual(CONTRACT["observed_compatibility"], "COMPATIBLE_UPDATED")
        self.assertIsNone(CONTRACT["failed_capability"])
        self.assertFalse(CONTRACT["likely_update_compatibility_break"])

    def test_identity_is_hioc_only_and_no_observation_mutation(self):
        self.assertEqual(CONTRACT["identity_engine"], "HIOC_ONLY")
        self.assertEqual(CONTRACT["generic_integration_inventory_ingestion"], "PROHIBITED")
        for key in ("creates_hioc_identity", "changes_hioc_stable_id", "changes_hioc_mac", "changes_hioc_canonical_ip", "changes_liveness", "changes_health", "changes_incidents", "changes_asset_fields"):
            self.assertIs(CONTRACT[key], False)
        for key in ("weak_ip_promotion", "generic_source_provenance_append", "entity_presence_proves_availability", "ha_absence_reduces_hioc_confidence", "count_coverage_is_one_to_one"):
            self.assertFalse(CONTRACT["observation_boundary"][key])
        self.assertTrue(CONTRACT["observation_boundary"]["dedicated_post_identity_layer"])
        self.assertEqual(CONTRACT["private_state_path"], "state/inventory/associations/home_assistant.json")

    def test_exact_uniqueness_and_rejection_policies(self):
        rules = CONTRACT["mac_rules"]
        for key in ("distinct_valid_mac_count", "ha_device_count_per_mac", "hioc_device_count_per_mac"):
            self.assertEqual(rules[key], 1)
        for key, outcome in (("multiple_mac", "REVIEW_ONLY_MULTIPLE_MAC"), ("invalid_mac", "REJECT_INVALID_MAC"), ("ha_collision", "REJECT_HA_MAC_COLLISION"), ("hioc_ambiguity", "REJECT_HIOC_MAC_AMBIGUITY"), ("no_mac", "REVIEW_ONLY_NO_MAC"), ("unmatched", "UNMATCHED_STRONG_EVIDENCE")):
            self.assertEqual(rules[key], outcome)
            self.assertIn(outcome, CONTRACT["association_outcomes"])
        self.assertFalse(rules["merge_hioc_duplicates"])
        self.assertEqual(rules["collision_tiebreakers"], "PROHIBITED")
        self.assertEqual(CONTRACT["prior_binding"]["conflict"], "REJECT_PRIOR_BINDING_CONFLICT")
        self.assertFalse(CONTRACT["prior_binding"]["silent_move"])
        self.assertTrue(CONTRACT["prior_binding"]["retain_previous_known_good"])

    def test_synthetic_decision_table(self):
        mac = "02:00:00:00:00:01"; second = "02:00:00:00:00:02"
        device = {"id": "a", "connections": [["mac", mac]]}
        hioc = [{"id": "existing", "mac": mac}]
        cases = [([device], hioc, {}, "ASSOCIATED_STRONG_MAC"),
                 ([{"id": "a", "connections": []}], hioc, {}, "REVIEW_ONLY_NO_MAC"),
                 ([{"id": "a", "connections": [["mac", "bad"]]}], hioc, {}, "REJECT_INVALID_MAC"),
                 ([{"id": "a", "connections": [["mac", mac], ["mac", "bad"]]}], hioc, {}, "REJECT_INVALID_MAC"),
                 ([{"id": "a", "connections": [["mac", mac], ["mac", second]]}], hioc, {}, "REVIEW_ONLY_MULTIPLE_MAC"),
                 ([device, {"id": "b", "connections": [["mac", mac.upper()]]}], hioc, {}, "REJECT_HA_MAC_COLLISION"),
                 ([device], hioc + [{"id": "other", "mac": mac}], {}, "REJECT_HIOC_MAC_AMBIGUITY"),
                 ([device], [], {}, "UNMATCHED_STRONG_EVIDENCE"),
                 ([device], hioc, {"a": "other"}, "REJECT_PRIOR_BINDING_CONFLICT"),
                 ([device], hioc, {"b": "existing"}, "REJECT_PRIOR_BINDING_CONFLICT"),
                 ([{"id": "a", "connections": [["mac", mac, "extra"]]}], hioc, {}, "REJECT_STRUCTURAL_CONTRACT"),
                 ([{"id": "a", "connections": [["bluetooth", mac], ["upnp", "same-name"]]}], hioc, {}, "REVIEW_ONLY_NO_MAC"),
                 ([{"id": "a", "connections": [["mac", mac], ["mac", mac.replace(":", "-")]]}], hioc, {}, "ASSOCIATED_STRONG_MAC")]
        for devices, inventory, prior, outcome in cases:
            with self.subTest(outcome=outcome):
                untouched = copy.deepcopy((devices, inventory, prior))
                self.assertEqual(reference_decision(devices, "a", inventory, prior), outcome)
                self.assertEqual((devices, inventory, prior), untouched)
        self.assertEqual(reference_decision(list(reversed(cases[5][0])), "a", hioc), "REJECT_HA_MAC_COLLISION")

    def test_namespace_and_extraction_authority(self):
        ns = CONTRACT["namespace_authority"]
        self.assertIn("ONLY_STRONG_NAMESPACE", ns["connections"]["mac"])
        for key in ("bluetooth", "upnp"):
            self.assertIn("SUPPORTING_PRIVATE_ONLY", ns["connections"][key])
        self.assertEqual(set(ns["identifiers"]), {"hue", "mqtt", "upnp", "zwave_js"})
        self.assertTrue(all("SUPPORTING_PRIVATE_ONLY" in value for value in ns["identifiers"].values()))
        self.assertIn("NO_IDENTITY_AUTHORITY", ns["unknown"])
        for key in ("ha_ip_identity_extraction", "ha_hostname_identity_extraction"):
            self.assertEqual(CONTRACT["authority"][key], "NOT_AUTHORIZED")
        self.assertEqual(CONTRACT["authority"]["serial_number"], "NOT_RETAINED_NOT_IDENTITY")
        self.assertEqual(CONTRACT["authority"]["configuration_url"], "NOT_RETAINED_NOT_PARSED_NOT_LOGGED_NOT_PUBLISHED")

    def test_entity_relationships_and_asset_precedence(self):
        self.assertEqual(CONTRACT["entity_membership"]["path"], "entity.device_id -> strongly associated HA device -> HIOC device")
        self.assertEqual(CONTRACT["entity_membership"]["without_device"], "ENTITY_WITHOUT_DEVICE_IDENTITY")
        self.assertFalse(CONTRACT["entity_membership"]["independent_matching"])
        self.assertEqual(CONTRACT["entity_membership"]["unique_id_retention"], "NOT_RETAINED")
        self.assertEqual(CONTRACT["authority"]["precedence"][0], "OPERATOR_ASSET_METADATA")
        self.assertTrue({"friendly_name", "physical_location", "purpose", "notes", "owner", "criticality", "expected_availability"} <= set(CONTRACT["authority"]["asset_fields_never_overwritten"]))
        self.assertFalse(CONTRACT["authority"]["metadata_is_identity"])

    def test_no_fuzzy_or_heuristic_matching(self):
        self.assertTrue({"LEVENSHTEIN_STRING_SIMILARITY", "SUBSTRING_NAME_MATCHING", "MANUFACTURER_MODEL_SCORING", "AREA_SCORING", "ENTITY_COUNT_SCORING", "INTEGRATION_DOMAIN_SCORING", "WEIGHTED_CONFIDENCE_PERCENTAGES", "ENTITY_ID", "UNIQUE_ID"} <= set(CONTRACT["prohibited_automatic_matching"]))

    def test_additive_compatibility_and_last_known_good(self):
        policy = CONTRACT["schema_evolution"]
        self.assertIn("NOT_CONSUMED_NOT_RETAINED_NOT_IDENTITY", policy["unknown_fields"])
        self.assertIn("NO_AUTHORITY", policy["unknown_namespaces"])
        self.assertFalse(policy["universal_future_ha_compatibility"])
        self.assertFalse(CONTRACT["snapshot"]["cross_registry_atomicity"])
        self.assertIn("NO_FABRICATED_LINK", CONTRACT["snapshot"]["dangling_reference"])
        transaction = CONTRACT["transactional_state"]
        self.assertEqual(transaction["replace"], "ATOMIC_ONLY_COMPLETELY_VALIDATED_CANDIDATE")
        self.assertEqual(set(transaction["retain_last_known_good_on"]), {"TRANSPORT_FAILURE", "AUTHENTICATION_FAILURE", "SCHEMA_INCOMPATIBILITY", "REQUIRED_COMMAND_FAILURE", "COMPATIBILITY_FAILURE", "STATE_PUBLICATION_FAILURE"})

    def test_valid_private_state(self):
        state = fixture(); validate_schema(state, STATE_SCHEMA)
        state["associations"][0].update(ha_metadata={"name": "synthetic", "disabled_by": None},
            entities=[{"registry_id": "synthetic", "entity_id": "sensor.synthetic", "platform": "test"}],
            config_entries=[{"entry_id": "synthetic", "domain": "test"}], area_candidate={"area_id": "synthetic", "name": "synthetic"})
        validate_schema(state, STATE_SCHEMA)
        state = fixture(); state["associations"] = []; state["summary"]["associated_devices"] = 0
        validate_schema(state, STATE_SCHEMA)

    def test_private_state_rejects_identity_and_leaks(self):
        for key in CONTRACT["private_prohibited_fields"]:
            for location in ("root", "association", "metadata"):
                state = fixture()
                target = state if location == "root" else state["associations"][0]
                if location == "metadata": target = target.setdefault("ha_metadata", {})
                target[key] = "synthetic"
                with self.subTest(field=key, location=location):
                    with self.assertRaises(ValueError): validate_schema(state, STATE_SCHEMA)
        for key in ("unique_id", "mac", "configuration_url"):
            state = fixture(); state["associations"][0]["entities"] = [{"registry_id": "synthetic", "entity_id": "sensor.synthetic", "platform": "test", key: "synthetic"}]
            with self.assertRaises(ValueError): validate_schema(state, STATE_SCHEMA)

    def test_state_bounds_types_and_status(self):
        for key, value in (("instance_reference", "other"), ("updated_at", "not-a-time"), ("schema_version", "2.0"), ("diagnostics", [{"reason": "unknown", "count": 1}])):
            state = fixture(); state[key] = value
            with self.assertRaises(ValueError): validate_schema(state, STATE_SCHEMA)
        for key, value in (("hioc_device_id", "raw-ha-id"), ("status", "REVIEW_ONLY_NO_MAC"), ("association_basis", "name"), ("ha_device_id", "x" * 257)):
            state = fixture(); state["associations"][0][key] = value
            with self.assertRaises(ValueError): validate_schema(state, STATE_SCHEMA)
        state = fixture(); state["associations"] *= 4097
        with self.assertRaises(ValueError): validate_schema(state, STATE_SCHEMA)
        state = fixture(); state["summary"]["associated_devices"] = True
        with self.assertRaises(ValueError): validate_schema(state, STATE_SCHEMA)

    def test_public_projection_is_separate_and_safe(self):
        self.assertEqual(set(CONTRACT["public_projection_allowlist"]), {"associated", "association_basis", "entity_count", "integration_domains", "has_area_candidate"})
        self.assertTrue({"raw_ha_mac", "ha_device_id", "entity_registry_id", "entity_id", "unique_id", "config_entry_id", "device_name", "area_name", "config_entry_title", "serial_number", "configuration_url"} <= set(CONTRACT["public_prohibited_fields"]))
        self.assertFalse(set(CONTRACT["public_projection_allowlist"]) & set(CONTRACT["public_prohibited_fields"]))
        association_properties = STATE_SCHEMA["properties"]["associations"]["items"]["properties"]
        self.assertFalse({"mac", "ip", "hostname"} & set(association_properties))

    def test_snapshot_constraints_and_current_roadmap(self):
        counts = CONTRACT["production_observation"]["registries"]
        for key, value in {"total":229, "mac_zero":169, "mac_one":58, "mac_multiple":2, "mac_entries":62, "mac_canonical":54, "mac_invalid":8, "mac_collision_values":9, "mac_conflicting_devices":18}.items():
            self.assertEqual(counts["device_registry"]["counts"][key], value)
        self.assertEqual(counts["entity_registry"]["counts"]["with_device"], 2241)
        self.assertEqual(counts["entity_registry"]["counts"]["without_device"], 184)
        self.assertTrue(CONTRACT["production_observation"]["counts_are_snapshot_only"])
        master = (ROOT / "docs/HIOC_MASTER_PLAN.md").read_text(encoding="utf-8")
        current = master.split("# Implementation Status", 1)[1].split("# Historical Operator Preparation Chronology", 1)[0]
        self.assertIn("| PE-4.0C | PASS/CLOSED |", current)
        self.assertTrue(current.split("## Next Planned Task", 1)[1].strip().startswith("### PE-4 Home Assistant Association Adapter Bounded Manual Production Validation"))
        self.assertIn("Compatibility Diagnostics UX", master)
        self.assertEqual(CONTRACT["runtime_adapter"], "NOT_IMPLEMENTED")
        self.assertEqual(CONTRACT["next_checkpoint_state"], "NOT_STARTED")


if __name__ == "__main__":
    unittest.main()
