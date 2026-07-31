import itertools
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "pi4" / "lib"))

from hioc.inventory import merge_records, select_canonical_ip, stable_device_id


MAC = "aa:bb:cc:dd:ee:ff"
CONFIG = {
    "HIOC_INVENTORY_STALE_AFTER_SEC": "60",
    "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120",
}


def dhcp(ip, expiry=2000, **extra):
    return {
        "ip": ip,
        "mac": MAC,
        "source": "dhcp_leases",
        "lease_expires_epoch": expiry,
        "_dhcp_active": True,
        "_positive_observation": False,
        **extra,
    }


def neighbor(ip, state="STALE", **extra):
    return {
        "ip": ip,
        "mac": MAC,
        "source": "arp_table",
        "last_seen_source": "arp_table",
        "_neighbor_state": state,
        **extra,
    }


def merged(records, previous=None):
    return merge_records(records, previous or {"devices": []}, "now", 1000, CONFIG)


class CanonicalAddressSelectionTests(unittest.TestCase):
    def test_active_dhcp_beats_stale_neighbor_regression(self):
        device = merged([dhcp("192.168.100.252"), neighbor("192.168.100.105")])[0]
        self.assertEqual(device["ip"], "192.168.100.252")

    def test_active_dhcp_beats_multiple_stale_neighbors_for_every_order(self):
        records = [
            dhcp("192.168.100.252"),
            neighbor("192.168.100.105"),
            neighbor("192.168.100.106"),
        ]
        for permutation in itertools.permutations(records):
            with self.subTest(order=[item["ip"] for item in permutation]):
                self.assertEqual(merged(list(permutation))[0]["ip"], "192.168.100.252")

    def test_strong_neighbor_beats_stale_without_dhcp(self):
        records = [neighbor("192.168.1.20", "STALE"), neighbor("192.168.1.21", "REACHABLE")]
        self.assertEqual(merged(records)[0]["ip"], "192.168.1.21")

    def test_static_non_dhcp_address_remains_supported(self):
        self.assertEqual(merged([neighbor("192.168.1.40", "PERMANENT")])[0]["ip"], "192.168.1.40")

    def test_expired_dhcp_loses_to_current_neighbor(self):
        expired = dhcp("192.168.1.50", _dhcp_active=False)
        current = neighbor("192.168.1.51", "REACHABLE")
        self.assertEqual(select_canonical_ip([expired, current]), "192.168.1.51")

    def test_failed_and_incomplete_neighbors_do_not_displace_active_dhcp(self):
        for state in ("FAILED", "INCOMPLETE"):
            with self.subTest(state=state):
                self.assertEqual(
                    select_canonical_ip([dhcp("192.168.1.60"), neighbor("192.168.1.61", state)]),
                    "192.168.1.60",
                )

    def test_multiple_active_dhcp_candidates_use_expiry_then_numeric_ip(self):
        self.assertEqual(
            select_canonical_ip([dhcp("192.168.1.70", 2000), dhcp("192.168.1.71", 3000)]),
            "192.168.1.71",
        )
        self.assertEqual(
            select_canonical_ip([dhcp("192.168.1.71", 3000), dhcp("192.168.1.70", 3000)]),
            "192.168.1.70",
        )

    def test_equal_strength_and_missing_timestamps_are_deterministic(self):
        records = [neighbor("192.168.1.82"), neighbor("192.168.1.81")]
        self.assertEqual(select_canonical_ip(records), "192.168.1.81")
        self.assertEqual(select_canonical_ip(list(reversed(records))), "192.168.1.81")

    def test_duplicate_candidates_are_stable(self):
        records = [neighbor("192.168.1.90"), neighbor("192.168.1.90"), dhcp("192.168.1.91")]
        self.assertEqual(select_canonical_ip(records), "192.168.1.91")

    def test_invalid_and_noncanonical_addresses_cannot_win(self):
        invalid = [
            "not-an-ip",
            "::1",
            "0.0.0.0",
            "127.0.0.1",
            "169.254.1.1",
            "224.0.0.1",
            "255.255.255.255",
        ]
        for value in invalid:
            with self.subTest(value=value):
                self.assertEqual(select_canonical_ip([neighbor(value, "REACHABLE"), dhcp("192.168.1.100")]), "192.168.1.100")

    def test_retired_address_loses_but_identity_and_provenance_remain(self):
        device = merged([neighbor("192.168.100.105"), dhcp("192.168.100.252")])[0]
        self.assertEqual(device["ip"], "192.168.100.252")
        self.assertEqual(device["id"], stable_device_id({"mac": MAC}))
        self.assertEqual(device["mac"], MAC)
        self.assertEqual(device["sources"], ["arp_table", "dhcp_leases"])
        self.assertEqual(len(merged([neighbor("192.168.100.105"), dhcp("192.168.100.252")])), 1)

    def test_internal_candidate_state_does_not_change_serialized_schema(self):
        device = merged([neighbor("192.168.1.110", "REACHABLE")])[0]
        self.assertNotIn("_neighbor_state", device)
        self.assertNotIn("_dhcp_active", device)

    def test_canonical_selection_does_not_make_dhcp_assignment_live(self):
        previous = {"devices": [{
            "id": stable_device_id({"mac": MAC}),
            "ip": "192.168.1.119",
            "mac": MAC,
            "source": "arp_table",
            "sources": ["arp_table"],
            "last_seen": "earlier",
            "last_seen_epoch": 800,
        }]}
        device = merged([dhcp("192.168.1.120")], previous)[0]
        self.assertEqual(device["ip"], "192.168.1.120")
        self.assertEqual(device["last_seen_epoch"], 800)
        self.assertNotEqual(device["observation_status"], "recent")

    def test_local_host_evidence_remains_stronger_than_dhcp(self):
        local = {
            "ip": "192.168.1.130",
            "mac": MAC,
            "source": "local_host",
            "type": "local_host",
            "reachable": True,
        }
        self.assertEqual(merged([local, dhcp("192.168.1.131")])[0]["ip"], "192.168.1.130")


if __name__ == "__main__":
    unittest.main()
