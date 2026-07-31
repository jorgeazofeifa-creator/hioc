import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from canonical_address_validation import (
    REQUIRED_BOOLEAN_INVARIANTS,
    evaluate,
    find_qualifying_candidates,
)


MAC = "aa:bb:cc:dd:ee:ff"


def inventory(ip, sources=None):
    return {"devices": [{
        "id": "dev_stable",
        "mac": MAC,
        "ip": ip,
        "sources": sources or ["arp_table", "dhcp_leases"],
    }]}


LEASES = [{"mac": MAC, "ip": "192.168.1.20", "expiry": 2000}]
STALE = [{"mac": MAC, "ip": "192.168.1.10", "state": "STALE"}]
VALID_INVARIANTS = {name: True for name in REQUIRED_BOOLEAN_INVARIANTS}


class CanonicalAddressValidationTests(unittest.TestCase):
    def test_pass_when_active_dhcp_wins_qualifying_case(self):
        report = evaluate(
            inventory("192.168.1.20"), LEASES, STALE, VALID_INVARIANTS, now_epoch=1000
        )
        self.assertEqual(report["result"], "PASS")
        self.assertFalse(report["rollback_recommended"])

    def test_fail_when_stale_ipv4_still_wins_qualifying_case(self):
        report = evaluate(
            inventory("192.168.1.10"), LEASES, STALE, VALID_INVARIANTS, now_epoch=1000
        )
        self.assertEqual(report["result"], "FAIL")
        self.assertTrue(report["rollback_recommended"])

    def test_no_candidate_is_successful_non_rollback_outcome(self):
        report = evaluate(
            inventory("192.168.1.20"), LEASES, [], VALID_INVARIANTS, now_epoch=1000
        )
        self.assertEqual(report["result"], "NO_QUALIFYING_CANDIDATE")
        self.assertFalse(report["rollback_recommended"])

    def test_ipv6_link_local_stale_neighbor_is_ineligible(self):
        neighbors = [{"mac": MAC, "ip": "fe80::1", "state": "STALE"}]
        candidates, _ = find_qualifying_candidates(inventory("192.168.1.20"), LEASES, neighbors, 1000)
        self.assertEqual(candidates, [])

    def test_configured_integration_excludes_candidate(self):
        observed = inventory("192.168.1.30", ["arp_table", "dhcp_leases", "integration:controller"])
        candidates, exclusions = find_qualifying_candidates(observed, LEASES, STALE, 1000)
        self.assertEqual(candidates, [])
        self.assertIn("higher_ranked_source", exclusions[0]["exclusion_reasons"])

    def test_local_and_gateway_sources_exclude_candidates(self):
        for source in ("local_host", "gateway"):
            with self.subTest(source=source):
                candidates, exclusions = find_qualifying_candidates(
                    inventory("192.168.1.30", ["arp_table", "dhcp_leases", source]),
                    LEASES,
                    STALE,
                    1000,
                )
                self.assertEqual(candidates, [])
                self.assertIn("higher_ranked_source", exclusions[0]["exclusion_reasons"])

    def test_reachable_and_permanent_neighbors_exclude_candidates(self):
        for state in ("REACHABLE", "PERMANENT"):
            with self.subTest(state=state):
                neighbors = STALE + [{"mac": MAC, "ip": "192.168.1.30", "state": state}]
                candidates, exclusions = find_qualifying_candidates(
                    inventory("192.168.1.30"), LEASES, neighbors, 1000
                )
                self.assertEqual(candidates, [])
                self.assertIn("higher_ranked_neighbor", exclusions[0]["exclusion_reasons"])

    def test_historical_canonical_must_match_stale_candidate_when_supplied(self):
        historical = inventory("192.168.1.99")
        candidates, exclusions = find_qualifying_candidates(
            inventory("192.168.1.20"), LEASES, STALE, 1000, historical
        )
        self.assertEqual(candidates, [])
        self.assertIn("historical_canonical_not_stale_candidate", exclusions[0]["exclusion_reasons"])

    def test_expired_and_invalid_dhcp_addresses_are_ineligible(self):
        leases = [
            {"mac": MAC, "ip": "192.168.1.20", "expiry": 999},
            {"mac": MAC, "ip": "not-an-ip", "expiry": 2000},
        ]
        report = evaluate(
            inventory("192.168.1.10"), leases, STALE, VALID_INVARIANTS, now_epoch=1000
        )
        self.assertEqual(report["result"], "NO_QUALIFYING_CANDIDATE")

    def test_zero_diagnostic_metadata_does_not_fail_no_candidate(self):
        invariants = {**VALID_INVARIANTS, "_unrelated_canonical_change_count": 0}
        report = evaluate(
            inventory("192.168.1.20"), LEASES, [], invariants, now_epoch=1000
        )
        self.assertEqual(report["result"], "NO_QUALIFYING_CANDIDATE")
        self.assertFalse(report["rollback_recommended"])
        self.assertEqual(report["diagnostic_metadata"], {"_unrelated_canonical_change_count": 0})

    def test_all_supported_diagnostic_value_types_are_informational(self):
        metadata = {
            "_zero": 0,
            "_positive": 151,
            "_unknown": None,
            "_note": "unchanged",
        }
        report = evaluate(
            inventory("192.168.1.20"),
            LEASES,
            [],
            {**VALID_INVARIANTS, **metadata},
            now_epoch=1000,
        )
        self.assertEqual(report["result"], "NO_QUALIFYING_CANDIDATE")
        self.assertEqual(report["diagnostic_metadata"], metadata)

    def test_failed_required_invariant_is_the_only_failed_invariant(self):
        invariants = {**VALID_INVARIANTS, "artifact_identity": False, "_count": 0}
        report = evaluate(inventory("192.168.1.20"), LEASES, [], invariants, now_epoch=1000)
        self.assertEqual(report["result"], "FAIL")
        self.assertEqual(report["failed_invariants"], ["artifact_identity"])
        self.assertEqual(report["invariant_input_errors"], [])
        self.assertTrue(report["rollback_recommended"])

    def test_missing_required_invariant_is_explicit_input_failure(self):
        invariants = dict(VALID_INVARIANTS)
        invariants.pop("artifact_identity")
        report = evaluate(inventory("192.168.1.20"), LEASES, [], invariants, now_epoch=1000)
        self.assertEqual(report["result"], "FAIL")
        self.assertEqual(report["failed_invariants"], [])
        self.assertIn("missing required Boolean invariant: artifact_identity", report["invariant_input_errors"])

    def test_integer_zero_is_not_boolean_false(self):
        invariants = {**VALID_INVARIANTS, "artifact_identity": 0}
        report = evaluate(inventory("192.168.1.20"), LEASES, [], invariants, now_epoch=1000)
        self.assertEqual(report["result"], "FAIL")
        self.assertEqual(report["failed_invariants"], [])
        self.assertIn("required invariant must be Boolean: artifact_identity", report["invariant_input_errors"])

    def test_integer_one_is_not_boolean_true(self):
        invariants = {**VALID_INVARIANTS, "artifact_identity": 1}
        report = evaluate(inventory("192.168.1.20"), LEASES, [], invariants, now_epoch=1000)
        self.assertEqual(report["result"], "FAIL")
        self.assertIn("required invariant must be Boolean: artifact_identity", report["invariant_input_errors"])

    def test_unexpected_public_key_is_explicit_input_failure(self):
        invariants = {**VALID_INVARIANTS, "device_count": 151}
        report = evaluate(inventory("192.168.1.20"), LEASES, [], invariants, now_epoch=1000)
        self.assertEqual(report["result"], "FAIL")
        self.assertIn(
            "unexpected non-diagnostic invariant key: device_count",
            report["invariant_input_errors"],
        )


if __name__ == "__main__":
    unittest.main()
