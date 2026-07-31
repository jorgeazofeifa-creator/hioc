import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from canonical_address_validation import evaluate, find_qualifying_candidates


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


class CanonicalAddressValidationTests(unittest.TestCase):
    def test_pass_when_active_dhcp_wins_qualifying_case(self):
        report = evaluate(inventory("192.168.1.20"), LEASES, STALE, now_epoch=1000)
        self.assertEqual(report["result"], "PASS")
        self.assertFalse(report["rollback_recommended"])

    def test_fail_when_stale_ipv4_still_wins_qualifying_case(self):
        report = evaluate(inventory("192.168.1.10"), LEASES, STALE, now_epoch=1000)
        self.assertEqual(report["result"], "FAIL")
        self.assertTrue(report["rollback_recommended"])

    def test_no_candidate_is_successful_non_rollback_outcome(self):
        report = evaluate(inventory("192.168.1.20"), LEASES, [], now_epoch=1000)
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
        report = evaluate(inventory("192.168.1.10"), leases, STALE, now_epoch=1000)
        self.assertEqual(report["result"], "NO_QUALIFYING_CANDIDATE")

    def test_failed_general_invariant_is_fail_even_without_candidate(self):
        report = evaluate(
            inventory("192.168.1.20"), LEASES, [], {"artifact_identity": False}, now_epoch=1000
        )
        self.assertEqual(report["result"], "FAIL")
        self.assertEqual(report["failed_invariants"], ["artifact_identity"])


if __name__ == "__main__":
    unittest.main()
