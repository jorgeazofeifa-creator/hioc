"""Additive lifecycle governance; pure synthetic references, no runtime adapter."""
import copy
from datetime import datetime
import hashlib
import json
from pathlib import Path
import unittest

from tests.test_pe4_0c_association_contract import validate_schema, fixture, reference_decision

ROOT = Path(__file__).resolve().parents[1]
RECORD_PATH = ROOT / "governance/pe4/pe4-0c1-association-lifecycle-clarification.json"
RECORD = json.loads(RECORD_PATH.read_text(encoding="utf-8"))
SCHEMA = json.loads((ROOT / RECORD["state_schema_path"]).read_text(encoding="utf-8"))
T0 = "2026-10-06T10:00:00Z"
T1 = "2026-10-06T11:00:00Z"
T2 = "2026-10-06T12:00:00Z"
T3 = "2026-10-06T13:00:00Z"
T4 = "2026-10-06T14:00:00Z"
T5 = "2026-10-06T15:00:00Z"
A = "dev_0123456789abcdef"
B = "dev_1111111111111111"
MAC = "02:00:00:00:00:01"
OTHER_MAC = "02:00:00:00:00:02"


def date(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def episode_key(record):
    return record["ha_device_id"], record["hioc_device_id"], date(record["last_confirmed_at"])


def validate_semantics(state):
    """Test-only cross-record rules that JSON Schema cannot express by key."""
    validate_schema(state, SCHEMA)
    owners, active_ha, active_hioc, episodes = {}, set(), set(), set()
    for active in state["associations"]:
        ha, hioc = active["ha_device_id"], active["hioc_device_id"]
        if ha in active_ha or hioc in active_hioc:
            raise ValueError("active cardinality")
        active_ha.add(ha); active_hioc.add(hioc)
        if not date(active["first_associated_at"]) <= date(active["last_confirmed_at"]) == date(state["updated_at"]):
            raise ValueError("active timestamps")
        owners[ha] = hioc
    for historical in state["binding_history"]:
        key = episode_key(historical)
        if key in episodes:
            raise ValueError("duplicate episode")
        episodes.add(key)
        ha, hioc = historical["ha_device_id"], historical["hioc_device_id"]
        if ha in owners and owners[ha] != hioc:
            raise ValueError("historical target changed")
        owners[ha] = hioc
        if not date(historical["first_associated_at"]) <= date(historical["last_confirmed_at"]) < date(historical["retired_at"]) <= date(state["updated_at"]):
            raise ValueError("history timestamps")
    pair_first = {}
    for record in state["associations"] + state["binding_history"]:
        pair = (record["ha_device_id"], record["hioc_device_id"])
        first = date(record["first_associated_at"])
        if pair in pair_first and pair_first[pair] != first:
            raise ValueError("inconsistent exact-pair first timestamp")
        pair_first[pair] = first
    for active in state["associations"]:
        first_times = [active["first_associated_at"]] + [h["first_associated_at"] for h in state["binding_history"] if (h["ha_device_id"], h["hioc_device_id"]) == (active["ha_device_id"], active["hioc_device_id"])]
        if active["first_associated_at"] != min(first_times, key=date):
            raise ValueError("pair first timestamp changed")
    summary = state["summary"]
    if summary["associated_devices"] != len(state["associations"]) or summary["historical_bindings"] != len(state["binding_history"]) or summary["entity_memberships"] != sum(len(a.get("entities", [])) for a in state["associations"]):
        raise ValueError("summary counts")
    reasons = [item["reason"] for item in state["diagnostics"]]
    if len(reasons) != len(set(reasons)):
        raise ValueError("diagnostic duplicate reason")


def prior_state():
    state = fixture()
    state["schema_version"] = "1.1"
    state["associations"][0]["ha_device_id"] = "old"
    state["associations"][0]["first_associated_at"] = T0
    state["binding_history"] = []
    state["summary"]["historical_bindings"] = 0
    return state


def dev(ha="old", mac=MAC):
    return {"id": ha, "connections": [["mac", mac]]}


def reference_cycle(prior, devices, inventory, timestamp=T3, failure=None, incomplete=False):
    """Pure lifecycle table fixture, deliberately not a transport or state writer."""
    untouched = copy.deepcopy(prior)
    if failure:
        return untouched, failure
    try:
        validate_semantics(prior)
        if date(timestamp) <= date(prior["updated_at"]):
            raise ValueError("cycle clock")
        by_ha = {d["id"]: d for d in devices}
        by_hioc = {d["id"]: d for d in inventory}
        if len(by_hioc) != len(inventory) or len(by_ha) != len(devices):
            raise ValueError("duplicate input keys")
        owners = {a["ha_device_id"]: a["hioc_device_id"] for a in prior["associations"] + prior["binding_history"]}
        prior_active = {a["hioc_device_id"]: a for a in prior["associations"]}
        raw_outcomes = {d["id"]: reference_decision(devices, d["id"], inventory) for d in devices}
        outcomes, current, rotations = dict(raw_outcomes), [], set()
        for d in sorted(devices, key=lambda value: value["id"]):
            ha = d["id"]
            if raw_outcomes[ha] != "ASSOCIATED_STRONG_MAC":
                continue
            mac = next(v.strip().lower().replace("-", ":") for ns, v in d["connections"] if ns == "mac")
            hioc = next(item["id"] for item in inventory if item.get("mac") == mac)
            if ha in owners and owners[ha] != hioc:
                outcomes[ha] = "REJECT_PRIOR_BINDING_CONFLICT"; continue
            source = prior_active.get(hioc)
            # A known exact pair reactivates; a new ID needs an absent old source.
            if source is None and ha not in owners:
                candidates = [h for h in prior["binding_history"] if h["hioc_device_id"] == hioc]
                if candidates:
                    latest = max(date(h["last_confirmed_at"]) for h in candidates)
                    candidates = [h for h in candidates if date(h["last_confirmed_at"]) == latest]
                    if len({h["ha_device_id"] for h in candidates}) != 1:
                        outcomes[ha] = "REJECT_PRIOR_BINDING_CONFLICT"; continue
                    source = candidates[0]
            if source is not None and source["ha_device_id"] != ha:
                if source["ha_device_id"] in by_ha:
                    outcomes[ha] = "REJECT_PRIOR_BINDING_CONFLICT"; continue
                rotations.add(source["ha_device_id"])
            if any(a["hioc_device_id"] == hioc for a in current):
                outcomes[ha] = "REJECT_PRIOR_BINDING_CONFLICT"; continue
            known = [a for a in prior["associations"] + prior["binding_history"] if a["ha_device_id"] == ha and a["hioc_device_id"] == hioc]
            first = min((a["first_associated_at"] for a in known), key=date) if known else timestamp
            current.append({"hioc_device_id": hioc, "ha_device_id": ha, "association_basis": "unique_mac", "status": "ASSOCIATED_STRONG_MAC", "first_associated_at": first, "last_confirmed_at": timestamp, "observed_ha_version": "2026.9.4", "contract_version": "1.0", "relationship_status": "INCOMPLETE" if incomplete else "COMPLETE"})
        history = copy.deepcopy(prior["binding_history"])
        existing = {episode_key(h): h for h in history}
        pairs = {(a["ha_device_id"], a["hioc_device_id"]) for a in current}
        added = 0
        for a in prior["associations"]:
            ha, hioc = a["ha_device_id"], a["hioc_device_id"]
            if (ha, hioc) in pairs:
                continue
            reason = None
            if ha in rotations: reason = "HA_DEVICE_RECREATED"
            elif ha not in by_ha: reason = "HA_DEVICE_ABSENT"
            elif raw_outcomes[ha] == "REJECT_INVALID_MAC": reason = "HA_DEVICE_INVALID_MAC"
            elif raw_outcomes[ha] == "REVIEW_ONLY_NO_MAC": reason = "HA_DEVICE_NO_MAC"
            elif raw_outcomes[ha] == "REVIEW_ONLY_MULTIPLE_MAC": reason = "HA_DEVICE_MULTIPLE_MAC"
            elif raw_outcomes[ha] == "REJECT_HA_MAC_COLLISION": reason = "HA_DEVICE_MAC_COLLISION"
            elif hioc not in by_hioc: reason = "HIOC_DEVICE_ABSENT"
            elif raw_outcomes[ha] == "REJECT_HIOC_MAC_AMBIGUITY": reason = "HIOC_MAC_AMBIGUITY"
            else: reason = "HIOC_CANONICAL_MAC_NO_LONGER_MATCHES"
            retired = {k: a[k] for k in ("hioc_device_id", "ha_device_id", "first_associated_at", "last_confirmed_at")}
            retired.update(retired_at=timestamp, retirement_reason=reason)
            key = episode_key(retired)
            if key not in existing:
                history.append(retired); existing[key] = retired; added += 1
        if len(history) > RECORD["history_policy"]["max_records"]:
            return untouched, "BINDING_HISTORY_CAPACITY_EXCEEDED"
        result = copy.deepcopy(prior)
        result.update(updated_at=timestamp, associations=sorted(current, key=lambda a:(a["hioc_device_id"], a["ha_device_id"])), binding_history=sorted(history, key=episode_key))
        counts = {reason: sum(value == reason for value in outcomes.values()) for reason in set(outcomes.values())}
        result["summary"] = {"associated_devices": len(current), "entity_memberships": 0, "review_only": sum(count for reason, count in counts.items() if reason.startswith("REVIEW_ONLY_")), "rejected": sum(count for reason, count in counts.items() if reason.startswith("REJECT_")), "unmatched": counts.get("UNMATCHED_STRONG_EVIDENCE", 0), "historical_bindings": len(history)}
        if added: counts["PRIOR_BINDING_RETIRED"] = added
        if rotations: counts["HA_DEVICE_ID_RECREATED"] = len(rotations)
        result["diagnostics"] = [{"reason": reason, "count": count} for reason, count in sorted(counts.items())]
        validate_semantics(result)
        return result, "PASS"
    except (ValueError, KeyError, StopIteration):
        return untouched, "CANDIDATE_VALIDATION"


class LifecycleClarificationTests(unittest.TestCase):
    def test_authority_canonical_schema_and_immutable_originals(self):
        self.assertEqual(RECORD["record_type"], "PE4_0C1_ASSOCIATION_LIFECYCLE_CLARIFICATION")
        self.assertEqual(RECORD["lifecycle_state"], "PASS_CLOSED")
        self.assertEqual(RECORD["pe4_0c"], "PASS_CLOSED")
        record_schema = json.loads((ROOT / "governance/pe4/pe4-0c1-association-lifecycle-clarification.schema.json").read_text())
        validate_schema(RECORD, record_schema)
        invalid = copy.deepcopy(RECORD); invalid["silent_rebinding"] = "ALLOWED"
        with self.assertRaises(ValueError): validate_schema(invalid, record_schema)
        for path in (RECORD_PATH, ROOT / RECORD["state_schema_path"], ROOT / "governance/pe4/pe4-0c1-association-lifecycle-clarification.schema.json"):
            value = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(path.read_text(encoding="utf-8"), json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n")
        for path_key, hash_key in (("original_0c_contract_path", "original_0c_contract_sha256"), ("original_state_schema_path", "original_state_schema_sha256"), ("state_schema_path", "state_schema_sha256")):
            self.assertEqual(hashlib.sha256((ROOT / RECORD[path_key]).read_text(encoding="utf-8").encode()).hexdigest(), RECORD[hash_key])
        self.assertEqual(RECORD["original_0c_contract_sha256"], "a48ec696c7e596dde68e252366f84ea46dfa7076a9b1aaff419a993742ed9a58")
        self.assertEqual(RECORD["original_state_schema_sha256"], "0a85d0e16f8d27f6532846e00eed843915b06ed2a3b84fd74285d931f3e6892d")

    def test_success_reconfirms_exact_pair_and_incomplete_relationships(self):
        prior = prior_state()
        for incomplete in (False, True):
            result, status = reference_cycle(prior, [dev()], [{"id":A,"mac":MAC}], incomplete=incomplete)
            self.assertEqual(status, "PASS")
            active = result["associations"][0]
            self.assertEqual(active["first_associated_at"], T0)
            self.assertEqual(active["last_confirmed_at"], T3)
            self.assertEqual(active["relationship_status"], "INCOMPLETE" if incomplete else "COMPLETE")
            self.assertEqual(result["binding_history"], [])
        self.assertEqual(prior, prior_state())

    def test_all_successful_retirement_cases(self):
        cases=[([], [{"id":A,"mac":MAC}], "HA_DEVICE_ABSENT"),
               ([{"id":"old","connections":[]}], [{"id":A,"mac":MAC}], "HA_DEVICE_NO_MAC"),
               ([dev(mac="invalid")], [{"id":A,"mac":MAC}], "HA_DEVICE_INVALID_MAC"),
               ([{"id":"old","connections":[["mac",MAC],["mac",OTHER_MAC]]}], [{"id":A,"mac":MAC}], "HA_DEVICE_MULTIPLE_MAC"),
               ([dev(),dev("duplicate")], [{"id":A,"mac":MAC}], "HA_DEVICE_MAC_COLLISION"),
               ([dev()], [], "HIOC_DEVICE_ABSENT"),
               ([dev()], [{"id":A,"mac":OTHER_MAC}], "HIOC_CANONICAL_MAC_NO_LONGER_MATCHES"),
               ([dev()], [{"id":A,"mac":MAC},{"id":B,"mac":MAC}], "HIOC_MAC_AMBIGUITY")]
        for devices, inventory, reason in cases:
            with self.subTest(reason=reason):
                result, status = reference_cycle(prior_state(), devices, inventory)
                self.assertEqual(status,"PASS")
                self.assertEqual(result["associations"],[])
                self.assertEqual(result["binding_history"][0]["retirement_reason"],reason)
                self.assertEqual(result["binding_history"][0]["last_confirmed_at"],T2)
                self.assertEqual(result["binding_history"][0]["retired_at"],T3)
                self.assertEqual(result["summary"]["historical_bindings"],1)

    def test_failure_preserves_entire_prior_state(self):
        prior=prior_state()
        for failure in RECORD["failure_classes"]:
            with self.subTest(failure=failure):
                result,status=reference_cycle(prior,[],[],failure=failure)
                self.assertEqual(status,failure)
                self.assertEqual(result,prior)
        result,status=reference_cycle(prior,[dev()],[{"id":A,"mac":MAC}],timestamp=T1)
        self.assertEqual(status,"CANDIDATE_VALIDATION")
        self.assertEqual(result,prior)

    def test_mac_change_never_silently_rebinds(self):
        result,status=reference_cycle(prior_state(),[dev(mac=OTHER_MAC)],[{"id":A,"mac":MAC},{"id":B,"mac":OTHER_MAC}])
        self.assertEqual(status,"PASS")
        self.assertEqual(result["associations"],[])
        self.assertEqual(result["binding_history"][0]["hioc_device_id"],A)
        self.assertEqual(result["binding_history"][0]["retirement_reason"],"HIOC_CANONICAL_MAC_NO_LONGER_MATCHES")
        self.assertIn({"reason":"REJECT_PRIOR_BINDING_CONFLICT","count":1},result["diagnostics"])

    def test_reactivation_same_pair_and_later_episode(self):
        retired,status=reference_cycle(prior_state(),[],[{"id":A,"mac":MAC}])
        reactivated,status=reference_cycle(retired,[dev()],[{"id":A,"mac":MAC}],T4)
        self.assertEqual(status,"PASS")
        self.assertEqual(reactivated["associations"][0]["first_associated_at"],T0)
        self.assertEqual(reactivated["associations"][0]["last_confirmed_at"],T4)
        self.assertEqual(reactivated["binding_history"],retired["binding_history"])
        again,status=reference_cycle(reactivated,[],[{"id":A,"mac":MAC}],T5)
        self.assertEqual(status,"PASS")
        self.assertEqual(len(again["binding_history"]),2)
        self.assertEqual({h["last_confirmed_at"] for h in again["binding_history"]},{T2,T4})
        different,status=reference_cycle(retired,[dev(mac=OTHER_MAC)],[{"id":B,"mac":OTHER_MAC}],T4)
        self.assertEqual(status,"PASS")
        self.assertEqual(different["associations"],[])
        self.assertIn({"reason":"REJECT_PRIOR_BINDING_CONFLICT","count":1},different["diagnostics"])

    def test_safe_recreation_new_pair_timestamp(self):
        result,status=reference_cycle(prior_state(),[dev("new")],[{"id":A,"mac":MAC}])
        self.assertEqual(status,"PASS")
        self.assertEqual(result["associations"][0]["ha_device_id"],"new")
        self.assertEqual(result["associations"][0]["hioc_device_id"],A)
        self.assertEqual(result["associations"][0]["first_associated_at"],T3)
        self.assertEqual(result["binding_history"][0]["retirement_reason"],"HA_DEVICE_RECREATED")
        self.assertIn({"reason":"HA_DEVICE_ID_RECREATED","count":1},result["diagnostics"])
        self.assertEqual(len(RECORD["recreation_conditions"]),10)

    def test_unsafe_recreation_rejected(self):
        cases=[([{"id":"old","connections":[]},dev("new")],[{"id":A,"mac":MAC}]),
               ([dev(),dev("new")],[{"id":A,"mac":MAC}]),
               ([dev("new")],[{"id":A,"mac":MAC},{"id":B,"mac":MAC}]),
               ([{"id":"new","connections":[["mac",MAC],["mac",OTHER_MAC]]}],[{"id":A,"mac":MAC}]),
               ([dev("new",mac="invalid")],[{"id":A,"mac":MAC}])]
        for devices,inventory in cases:
            result,status=reference_cycle(prior_state(),devices,inventory)
            self.assertEqual(status,"PASS")
            self.assertFalse(any(a["ha_device_id"]=="new" for a in result["associations"]))
        prior=prior_state()
        prior["binding_history"]=[{"ha_device_id":"new","hioc_device_id":B,"first_associated_at":T0,"last_confirmed_at":T0,"retired_at":T1,"retirement_reason":"HA_DEVICE_ABSENT"}]
        prior["summary"]["historical_bindings"]=1
        result,status=reference_cycle(prior,[dev("new")],[{"id":A,"mac":MAC}])
        self.assertEqual(status,"PASS")
        self.assertEqual(result["associations"],[])
        self.assertIn({"reason":"REJECT_PRIOR_BINDING_CONFLICT","count":1},result["diagnostics"])

    def test_history_is_idempotent_and_deterministic(self):
        retired,status=reference_cycle(prior_state(),[],[{"id":A,"mac":MAC}])
        again,status=reference_cycle(retired,[],[{"id":A,"mac":MAC}],T4)
        self.assertEqual(status,"PASS")
        self.assertEqual(again["binding_history"],retired["binding_history"])
        self.assertNotIn("PRIOR_BINDING_RETIRED",[d["reason"] for d in again["diagnostics"]])
        devices=[dev(),dev("ambiguous")]
        left,_=reference_cycle(prior_state(),devices,[{"id":A,"mac":MAC}])
        right,_=reference_cycle(prior_state(),list(reversed(devices)),[{"id":A,"mac":MAC}])
        self.assertEqual(left,right)

    def test_history_capacity_has_no_eviction(self):
        prior=prior_state()
        prior["binding_history"]=[{"ha_device_id":f"synthetic-{i}","hioc_device_id":A,"first_associated_at":T0,"last_confirmed_at":T0,"retired_at":T1,"retirement_reason":"HA_DEVICE_ABSENT"} for i in range(4096)]
        prior["summary"]["historical_bindings"]=4096
        validate_semantics(prior)
        result,status=reference_cycle(prior,[],[{"id":A,"mac":MAC}])
        self.assertEqual(status,"BINDING_HISTORY_CAPACITY_EXCEEDED")
        self.assertEqual(result,prior)
        self.assertFalse(RECORD["history_policy"]["automatic_eviction"])

    def test_closed_history_schema_and_invalid_semantics(self):
        state,status=reference_cycle(prior_state(),[],[{"id":A,"mac":MAC}])
        validate_semantics(state)
        for field in RECORD["history_prohibited_fields"]:
            invalid=copy.deepcopy(state);invalid["binding_history"][0][field]="synthetic"
            with self.subTest(field=field):
                with self.assertRaises(ValueError):validate_schema(invalid,SCHEMA)
        for mutate in (
            lambda s:s["summary"].update(historical_bindings=0),
            lambda s:s["binding_history"][0].update(retired_at=T0),
            lambda s:s["binding_history"][0].update(retirement_reason="arbitrary"),
            lambda s:s.update(schema_version="1.0"),
            lambda s:s["binding_history"].append({**s["binding_history"][0],"retired_at":T4}),
            lambda s:s["binding_history"].append({**s["binding_history"][0],"last_confirmed_at":"2026-10-06T12:00:00.000000Z"}),
        ):
            invalid=copy.deepcopy(state);mutate(invalid)
            with self.assertRaises(ValueError):validate_semantics(invalid)
        invalid=copy.deepcopy(state);invalid["binding_history"]*=4097
        with self.assertRaises(ValueError):validate_schema(invalid,SCHEMA)
        active=prior_state();active["binding_history"]=[{**state["binding_history"][0],"hioc_device_id":B,"retired_at":T2}];active["summary"]["historical_bindings"]=1
        with self.assertRaises(ValueError):validate_semantics(active)

    def test_exact_summary_and_active_only_public_projection(self):
        self.assertEqual(set(SCHEMA["properties"]["summary"]["required"]),{"associated_devices","entity_memberships","review_only","rejected","unmatched","historical_bindings"})
        self.assertEqual(RECORD["public_projection"],"CURRENT_ACTIVE_ONLY_HISTORY_NEVER_ASSOCIATED_TRUE_DEFERRED_IMPLEMENTATION")
        retired,status=reference_cycle(prior_state(),[],[{"id":A,"mac":MAC}])
        projected={a["hioc_device_id"]:True for a in retired["associations"]}
        self.assertNotIn(A,projected)
        self.assertEqual(retired["summary"]["associated_devices"],0)
        self.assertEqual(retired["summary"]["historical_bindings"],1)

    def test_no_new_authority_and_historical_preparation_boundary(self):
        self.assertEqual(RECORD["generic_integration_ingestion"],"PROHIBITED")
        for field in ("changes_hioc_identity","changes_canonical_mac","changes_canonical_ip","changes_liveness","changes_health","changes_incidents","changes_asset_fields"):
            self.assertIs(RECORD[field],False)
        self.assertEqual(RECORD["runtime_adapter"],"NOT_IMPLEMENTED")
        self.assertEqual(RECORD["production_state"],"NOT_CREATED")
        self.assertEqual(RECORD["implementation_preparation"],"NOT_STARTED")
        self.assertIn("LIKELY_SEPARATE",RECORD["credential_prerequisite"])
        master=(ROOT/"docs/HIOC_MASTER_PLAN.md").read_text(encoding="utf-8")
        current=master.split("# Implementation Status",1)[1].split("# Historical Operator Preparation Chronology",1)[0]
        self.assertIn("| PE-4.0C.1 Association Lifecycle Clarification | PASS/CLOSED |",current)
        self.assertIn("| PE-4 Home Assistant Association Adapter Implementation Preparation | PASS/CLOSED |",current)
        self.assertTrue(current.split("## Next Planned Task",1)[1].strip().startswith("### PE-4 Home Assistant Association Adapter Deployment Preparation"))
        self.assertIn("Compatibility Diagnostics UX",master)


if __name__ == "__main__":
    unittest.main()
