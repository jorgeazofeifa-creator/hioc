import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "pi4" / "lib"))

from hioc.inventory import (
    build_dependencies,
    build_inventory_summary,
    build_topology,
    classify_device,
    dhcp_lease_discovery,
    dhcp_lease_paths,
    dhcp_lease_source_results,
    dhcp_leases,
    enrich_services,
    health_score,
    inventory_summary_lists,
    inventory_class,
    observation_freshness,
    append_known_infrastructure,
    discover_inventory,
    integration_inventory,
    known_infrastructure,
    merge_records,
    neighbor_table,
    normalize_mac,
    operator_role,
    resolve_configured_parent_ids,
    scan_subnet,
    stable_device_id,
)
from hioc.core.monitoring import is_operationally_monitored


class InventoryModelTests(unittest.TestCase):
    def test_mac_normalization_accepts_colon_and_dash_formats(self):
        self.assertEqual(normalize_mac("AA-BB-CC-DD-EE-FF"), "aa:bb:cc:dd:ee:ff")
        self.assertEqual(normalize_mac("aa:bb:cc:dd:ee:ff"), "aa:bb:cc:dd:ee:ff")
        self.assertEqual(normalize_mac("not-a-mac"), "")

    def test_stable_device_id_prefers_mac_then_ip(self):
        with_mac = stable_device_id({"mac": "aa:bb:cc:dd:ee:ff", "ip": "192.168.1.20"})
        same_mac_new_ip = stable_device_id({"mac": "aa:bb:cc:dd:ee:ff", "ip": "192.168.1.21"})
        by_ip = stable_device_id({"ip": "192.168.1.20"})
        self.assertEqual(with_mac, same_mac_new_ip)
        self.assertNotEqual(with_mac, by_ip)

    def test_health_score_marks_stale_and_offline_devices(self):
        healthy = health_score({"last_seen_epoch": 1000, "reachable": True, "mac": "aa:bb:cc:dd:ee:ff"}, 1010, 60, 120)
        stale = health_score({"last_seen_epoch": 900, "reachable": True, "mac": "aa:bb:cc:dd:ee:ff"}, 1010, 60, 120)
        offline = health_score({"last_seen_epoch": 800, "reachable": False, "mac": "aa:bb:cc:dd:ee:ff"}, 1010, 60, 120)
        self.assertEqual(healthy[1], "healthy")
        self.assertEqual(stale[1], "watch")
        self.assertEqual(offline[1], "offline")

    def test_health_score_only_forces_offline_for_never_observed_records(self):
        legacy_missing_timestamp = health_score({"mac": "aa:bb:cc:dd:ee:ff"}, 1010, 60, 120)
        never_observed = health_score({"mac": "aa:bb:cc:dd:ee:ff", "_never_observed": True}, 1010, 60, 120)

        self.assertEqual(legacy_missing_timestamp[1], "degraded")
        self.assertEqual(never_observed[1], "offline")

    def test_merge_records_preserves_previous_unseen_devices(self):
        config = {"HIOC_INVENTORY_STALE_AFTER_SEC": "60", "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120"}
        previous = {
            "devices": [
                {
                    "id": stable_device_id({"mac": "aa:bb:cc:dd:ee:ff"}),
                    "mac": "aa:bb:cc:dd:ee:ff",
                    "display_name": "sensor-one",
                    "last_seen_epoch": 100,
                    "first_seen": "earlier",
                }
            ]
        }
        devices = merge_records([{"ip": "192.168.1.2", "mac": "11:22:33:44:55:66", "reachable": True}], previous, "now", 130, config)
        ids = {device["id"] for device in devices}
        self.assertIn(stable_device_id({"mac": "aa:bb:cc:dd:ee:ff"}), ids)
        self.assertIn(stable_device_id({"mac": "11:22:33:44:55:66"}), ids)

    def test_same_run_weak_ip_identity_reconciles_into_mac_identity(self):
        config = {"HIOC_INVENTORY_STALE_AFTER_SEC": "60", "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120"}
        devices = merge_records([
            {"ip": "192.168.100.219", "source": "arp_table", "vendor": "Weak metadata", "reachable": False},
            {"ip": "192.168.100.219", "mac": "0e:38:76:1a:e3:ba", "source": "dhcp_leases", "reachable": True},
        ], {"devices": []}, "2026-07-12T22:26:48-06:00", 1000, config)

        self.assertEqual(len(devices), 1)
        self.assertEqual(devices[0]["id"], stable_device_id({"mac": "0e:38:76:1a:e3:ba"}))
        self.assertEqual(devices[0]["vendor"], "Weak metadata")
        self.assertNotIn("reachable", devices[0])
        self.assertEqual(devices[0]["health_status"], "healthy")
        self.assertIn("arp_table", devices[0]["source"])
        self.assertIn("dhcp_leases", devices[0]["source"])
        self.assertEqual(devices[0]["sources"], ["arp_table", "dhcp_leases"])

    def test_retained_weak_ip_identity_reconciles_into_current_mac_identity(self):
        config = {"HIOC_INVENTORY_STALE_AFTER_SEC": "60", "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120"}
        previous = {"devices": [
            {
                "id": stable_device_id({"ip": "192.168.100.219"}),
                "ip": "192.168.100.219",
                "mac": "",
                "first_seen": "2026-07-01T08:00:00-06:00",
                "last_seen": "2026-07-01T09:00:00-06:00",
                "last_seen_epoch": 100,
                "source": "arp_table",
                "vendor": "Retained metadata",
            },
            {
                "id": stable_device_id({"mac": "0e:38:76:1a:e3:ba"}),
                "ip": "192.168.100.219",
                "mac": "0e:38:76:1a:e3:ba",
                "first_seen": "2026-07-10T08:00:00-06:00",
                "last_seen": "2026-07-11T09:00:00-06:00",
                "last_seen_epoch": 900,
                "source": "dhcp_leases",
            },
        ]}
        devices = merge_records([
            {"ip": "192.168.100.219", "mac": "0e:38:76:1a:e3:ba", "source": "dhcp_leases", "reachable": True},
        ], previous, "2026-07-12T22:26:48-06:00", 1000, config)

        self.assertEqual(len(devices), 1)
        self.assertEqual(devices[0]["id"], stable_device_id({"mac": "0e:38:76:1a:e3:ba"}))
        self.assertNotEqual(devices[0]["id"], stable_device_id({"ip": "192.168.100.219"}))
        self.assertEqual(devices[0]["first_seen"], "2026-07-01T08:00:00-06:00")
        self.assertEqual(devices[0]["last_seen"], "2026-07-11T09:00:00-06:00")
        self.assertEqual(devices[0]["last_seen_epoch"], 900)
        self.assertEqual(devices[0]["vendor"], "Retained metadata")
        self.assertNotIn("reachable", devices[0])
        self.assertIn("arp_table", devices[0]["source"])
        self.assertIn("dhcp_leases", devices[0]["source"])
        self.assertEqual(devices[0]["sources"], ["arp_table", "dhcp_leases"])

    def test_current_weak_ip_identity_reconciles_into_retained_mac_identity(self):
        config = {"HIOC_INVENTORY_STALE_AFTER_SEC": "60", "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120"}
        weak_id = stable_device_id({"ip": "192.168.100.219"})
        strong_id = stable_device_id({"mac": "0e:38:76:1a:e3:ba"})
        previous = {"devices": [{
            "id": strong_id,
            "ip": "192.168.100.219",
            "mac": "0e:38:76:1a:e3:ba",
            "name": "Retained Device",
            "vendor": "Retained Vendor",
            "role": "IoT",
            "firmware": "1.2.3",
            "interface": "eth0",
            "interfaces": [{"interface": "eth0", "ip": "192.168.100.219"}],
            "first_seen": "2026-07-02T08:00:00-06:00",
            "last_seen": "2026-07-11T09:00:00-06:00",
            "last_seen_epoch": 900,
            "source": "integration:retained",
            "last_seen_source": "integration:retained",
        }]}
        devices = merge_records([{
            "ip": "192.168.100.219",
            "mac": "",
            "name": "192.168.100.219",
            "vendor": "",
            "source": "arp_table",
            "last_seen_source": "arp_table",
        }], previous, "2026-07-12T23:21:19-06:00", 1000, config)

        self.assertEqual(len(devices), 1)
        self.assertEqual(devices[0]["id"], strong_id)
        self.assertNotEqual(devices[0]["id"], weak_id)
        self.assertEqual(devices[0]["mac"], "0e:38:76:1a:e3:ba")
        self.assertEqual(devices[0]["display_name"], "Retained Device")
        self.assertEqual(devices[0]["vendor"], "Retained Vendor")
        self.assertEqual(devices[0]["role"], "IoT")
        self.assertEqual(devices[0]["firmware"], "1.2.3")
        self.assertEqual(devices[0]["interface"], "eth0")
        self.assertEqual(devices[0]["interfaces"], [{"interface": "eth0", "ip": "192.168.100.219"}])
        self.assertEqual(devices[0]["first_seen"], "2026-07-02T08:00:00-06:00")
        self.assertEqual(devices[0]["last_seen"], "2026-07-12T23:21:19-06:00")
        self.assertEqual(devices[0]["last_seen_epoch"], 1000)
        self.assertEqual(devices[0]["last_seen_source"], "arp_table")
        self.assertEqual(devices[0]["sources"], ["arp_table", "integration:retained"])

    def test_current_weak_consumes_retained_weak_and_strong_identities(self):
        config = {"HIOC_INVENTORY_STALE_AFTER_SEC": "60", "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120"}
        weak_id = stable_device_id({"ip": "192.168.100.219"})
        strong_id = stable_device_id({"mac": "0e:38:76:1a:e3:ba"})
        previous = {"devices": [
            {
                "id": weak_id,
                "ip": "192.168.100.219",
                "mac": "",
                "first_seen": "2026-07-01T08:00:00-06:00",
                "source": "previous_weak",
            },
            {
                "id": strong_id,
                "ip": "192.168.100.219",
                "mac": "0e:38:76:1a:e3:ba",
                "first_seen": "2026-07-02T08:00:00-06:00",
                "source": "previous_strong",
            },
        ]}
        devices = merge_records([{
            "ip": "192.168.100.219",
            "source": "arp_table",
            "last_seen_source": "arp_table",
        }], previous, "2026-07-12T23:21:19-06:00", 1000, config)

        self.assertEqual(len(devices), 1)
        self.assertEqual(devices[0]["id"], strong_id)
        self.assertEqual(devices[0]["first_seen"], "2026-07-01T08:00:00-06:00")
        self.assertEqual(devices[0]["sources"], ["arp_table", "previous_strong", "previous_weak"])

    def test_failed_neighbor_line_produces_no_device(self):
        lines = (
            "192.168.100.138 dev eth0 FAILED",
            "192.168.100.138 dev eth0 lladdr 0e:38:76:1a:e3:ba FAILED",
        )
        for line in lines:
            with self.subTest(line=line), self.assertLogs("hioc-inventory-engine", level="DEBUG") as logs, \
                    patch("hioc.inventory.run_command", return_value=(0, line, "")):
                self.assertEqual(neighbor_table(), {})
            diagnostic = " ".join(logs.output)
            self.assertIn("ip=192.168.100.138", diagnostic)
            self.assertIn("interface=eth0", diagnostic)
            self.assertIn("state=FAILED", diagnostic)

    def test_incomplete_neighbor_line_produces_no_device(self):
        with patch("hioc.inventory.run_command", return_value=(0, "192.168.100.58 dev eth0 INCOMPLETE", "")):
            self.assertEqual(neighbor_table(), {})

    def test_none_and_unknown_macless_neighbor_lines_produce_no_device(self):
        for line in ("192.168.100.57 dev eth0 NONE", "192.168.100.58 dev eth0 UNKNOWN"):
            with self.subTest(line=line), patch("hioc.inventory.run_command", return_value=(0, line, "")):
                self.assertEqual(neighbor_table(), {})

    def test_mac_backed_durable_neighbor_states_remain_accepted(self):
        mac = "0e:38:76:1a:e3:ba"
        for state in ("REACHABLE", "STALE", "DELAY", "PROBE", "PERMANENT"):
            line = f"192.168.100.219 dev eth0 lladdr {mac} {state}"
            with self.subTest(state=state), patch("hioc.inventory.run_command", return_value=(0, line, "")):
                self.assertEqual(neighbor_table()["192.168.100.219"]["mac"], mac)

    def test_complete_arp_fallback_entry_remains_accepted(self):
        commands = [
            (1, "", "ip unavailable"),
            (0, "? (192.168.100.219) at 0e:38:76:1a:e3:ba [ether] on eth0", ""),
        ]
        with patch("hioc.inventory.run_command", side_effect=commands):
            self.assertEqual(neighbor_table()["192.168.100.219"]["mac"], "0e:38:76:1a:e3:ba")

    def test_incomplete_arp_fallback_entry_is_rejected(self):
        commands = [
            (1, "", "ip unavailable"),
            (0, "? (192.168.100.58) at <incomplete> on eth0", ""),
        ]
        with patch("hioc.inventory.run_command", side_effect=commands):
            self.assertEqual(neighbor_table(), {})

    def test_repeated_failed_neighbor_never_enters_inventory(self):
        config = {"HIOC_INVENTORY_STALE_AFTER_SEC": "60", "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120"}
        previous = {"devices": []}
        for epoch in (1000, 1060, 1120):
            with patch("hioc.inventory.run_command", return_value=(0, "192.168.100.138 dev eth0 FAILED", "")):
                current = list(neighbor_table().values())
            devices = merge_records(current, previous, f"run-{epoch}", epoch, config)
            self.assertEqual(devices, [])
            previous = {"devices": devices}

    def test_failed_neighbor_does_not_refresh_retained_strong_identity(self):
        config = {"HIOC_INVENTORY_STALE_AFTER_SEC": "60", "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120"}
        strong_id = stable_device_id({"mac": "0e:38:76:1a:e3:ba"})
        previous = {"devices": [{
            "id": strong_id,
            "ip": "192.168.100.219",
            "mac": "0e:38:76:1a:e3:ba",
            "first_seen": "2026-07-02T08:00:00-06:00",
            "last_seen": "2026-07-12T22:36:11-06:00",
            "last_seen_epoch": 900,
            "source": "arp_table",
        }]}
        with patch("hioc.inventory.run_command", return_value=(0, "192.168.100.219 dev eth0 FAILED", "")):
            current = list(neighbor_table().values())
        devices = merge_records(current, previous, "2026-07-12T23:21:19-06:00", 1000, config)

        self.assertEqual(current, [])
        self.assertEqual(len(devices), 1)
        self.assertEqual(devices[0]["id"], strong_id)
        self.assertEqual(devices[0]["mac"], "0e:38:76:1a:e3:ba")
        self.assertEqual(devices[0]["last_seen"], "2026-07-12T22:36:11-06:00")
        self.assertEqual(devices[0]["last_seen_epoch"], 900)
        self.assertEqual(devices[0]["health_status"], "watch")
        self.assertEqual(devices[0]["status"], "stale")
        self.assertEqual(devices[0]["observation_status"], "stale")

        aged = merge_records([], {"devices": devices}, "2026-07-12T23:23:19-06:00", 1100, config)
        self.assertEqual(aged[0]["id"], strong_id)
        self.assertEqual(aged[0]["last_seen_epoch"], 900)
        self.assertEqual(aged[0]["health_status"], "watch")
        self.assertEqual(aged[0]["status"], "unknown")
        self.assertEqual(aged[0]["observation_status"], "expired")
        self.assertFalse(aged[0]["operationally_monitored"])
        self.assertIn("operational availability unknown", aged[0]["health_reasons"][0])

    def test_operational_monitoring_policy_is_conservative_and_centralized(self):
        monitored = (
            {"inventory_class": "infrastructure", "source": "arp_table"},
            {"inventory_class": "client", "source": "known_infrastructure"},
            {"inventory_class": "client", "source": "integration:home_assistant"},
            {"inventory_class": "client", "source": "gateway"},
            {"inventory_class": "client", "source": "local_host"},
            {"inventory_class": "client", "source": "future_source"},
            {"inventory_class": "client", "source": "arp_table", "operationally_monitored": True},
        )
        unmonitored = (
            {"inventory_class": "client", "source": "arp_table"},
            {"inventory_class": "client", "source": "dhcp_leases"},
            {"inventory_class": "client", "sources": ["arp_table", "dhcp_leases"]},
        )

        for record in monitored:
            with self.subTest(record=record):
                self.assertTrue(is_operationally_monitored(record))
        for record in unmonitored:
            with self.subTest(record=record):
                self.assertFalse(is_operationally_monitored(record))

    def test_monitoring_policy_does_not_depend_on_device_identity_fields(self):
        passive = {"inventory_class": "client", "source": "arp_table"}
        identities = (
            {},
            {"ip": "10.0.0.10"},
            {"mac": "aa:bb:cc:dd:ee:ff"},
            {"hostname": "arbitrary-client"},
            {"name": "Arbitrary Client"},
        )
        for identity in identities:
            with self.subTest(identity=identity):
                self.assertFalse(is_operationally_monitored({**passive, **identity}))

    def test_observation_freshness_allowed_values_and_ages_are_deterministic(self):
        cases = (
            ({"last_seen_epoch": 950}, ("recent", 50)),
            ({"last_seen_epoch": 900}, ("stale", 100)),
            ({"last_seen_epoch": 800}, ("expired", 200)),
            ({"_never_observed": True}, ("unobserved", None)),
            ({}, ("unknown", None)),
        )
        for record, expected in cases:
            with self.subTest(record=record):
                self.assertEqual(observation_freshness(record, 1000, 60, 120), expected)

    def test_recent_arp_only_client_remains_visible_and_recent(self):
        config = {"HIOC_INVENTORY_STALE_AFTER_SEC": "60", "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120"}
        devices = merge_records([{
            "ip": "10.0.0.20",
            "mac": "11:22:33:44:55:66",
            "source": "arp_table",
            "roles": ["endpoint"],
            "role": "Unknown",
        }], {"devices": []}, "now", 1000, config)

        self.assertEqual(len(devices), 1)
        self.assertEqual(devices[0]["observation_status"], "recent")
        self.assertEqual(devices[0]["observation_age_seconds"], 0)
        self.assertEqual(devices[0]["health_status"], "healthy")
        self.assertEqual(devices[0]["status"], "online")
        self.assertFalse(devices[0]["operationally_monitored"])

    def test_dhcp_only_client_is_assignment_metadata_but_not_positive_observation(self):
        config = {"HIOC_INVENTORY_STALE_AFTER_SEC": "60", "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120"}
        devices = merge_records([{
            "ip": "192.168.100.224",
            "mac": "64:b5:c6:c1:c5:09",
            "source": "dhcp_leases",
            "_positive_observation": False,
            "roles": ["endpoint"],
            "role": "Unknown",
        }], {"devices": []}, "now", 1000, config)

        self.assertEqual(devices[0]["observation_status"], "unknown")
        self.assertNotIn("last_seen", devices[0])
        self.assertNotIn("last_seen_epoch", devices[0])
        self.assertEqual(devices[0]["health_status"], "watch")
        self.assertEqual(devices[0]["status"], "unknown")
        self.assertFalse(devices[0]["operationally_monitored"])
        self.assertIn("operational availability unknown", devices[0]["health_reasons"][0])

    def test_infrastructure_and_known_assets_keep_strict_age_health(self):
        config = {"HIOC_INVENTORY_STALE_AFTER_SEC": "60", "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120"}
        records = (
            {"id": "server", "mac": "aa:bb:cc:dd:ee:01", "role": "Server", "source": "arp_table"},
            {"id": "known", "mac": "aa:bb:cc:dd:ee:02", "role": "IoT", "source": "known_infrastructure"},
        )
        for record in records:
            previous = {"devices": [{**record, "last_seen": "earlier", "last_seen_epoch": 100}]}
            with self.subTest(record=record):
                device = merge_records([], previous, "now", 1000, config)[0]
                self.assertTrue(device["operationally_monitored"])
                self.assertEqual(device["observation_status"], "expired")
                self.assertEqual(device["health_status"], "degraded")
                self.assertEqual(device["status"], "degraded")
                self.assertIn("not seen within offline threshold", device["health_reasons"])

    def test_legacy_macless_arp_only_record_is_removed(self):
        config = {"HIOC_INVENTORY_STALE_AFTER_SEC": "60", "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120"}
        previous = {"devices": [{
            "id": stable_device_id({"ip": "192.168.100.138"}),
            "ip": "192.168.100.138",
            "mac": "",
            "last_seen_epoch": 100,
            "source": "arp_table",
            "sources": ["arp_table"],
        }]}

        self.assertEqual(merge_records([], previous, "now", 1000, config), [])

    def test_macless_retained_integration_and_known_records_are_preserved(self):
        config = {"HIOC_INVENTORY_STALE_AFTER_SEC": "60", "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120"}
        for source in ("integration:test", "known_infrastructure"):
            ip = "192.168.100.80" if source.startswith("integration") else "192.168.100.81"
            previous = {"devices": [{
                "id": stable_device_id({"ip": ip}),
                "ip": ip,
                "mac": "",
                "last_seen_epoch": 100,
                "source": source,
            }]}
            with self.subTest(source=source):
                devices = merge_records([], previous, "now", 1000, config)
                self.assertEqual(len(devices), 1)
                self.assertEqual(devices[0]["id"], stable_device_id({"ip": ip}))

    def test_macless_retained_mixed_provenance_is_preserved(self):
        config = {"HIOC_INVENTORY_STALE_AFTER_SEC": "60", "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120"}
        previous = {"devices": [{
            "id": stable_device_id({"ip": "192.168.100.82"}),
            "ip": "192.168.100.82",
            "mac": "",
            "last_seen_epoch": 100,
            "source": "arp_table, integration:test",
            "sources": ["arp_table", "integration:test"],
        }]}

        self.assertEqual(len(merge_records([], previous, "now", 1000, config)), 1)

    def test_macless_gateway_and_local_host_records_are_preserved(self):
        config = {"HIOC_INVENTORY_STALE_AFTER_SEC": "60", "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120"}
        previous = {"devices": [
            {"id": "gateway", "ip": "192.168.100.1", "mac": "", "source": "gateway", "last_seen_epoch": 100},
            {"id": "local", "ip": "192.168.100.252", "mac": "", "source": "local_host", "type": "local_host", "last_seen_epoch": 100},
        ]}

        devices = merge_records([], previous, "now", 1000, config)

        self.assertEqual({device["id"] for device in devices}, {"gateway", "local"})

    def test_current_weak_does_not_reconcile_with_conflicting_retained_macs(self):
        config = {"HIOC_INVENTORY_STALE_AFTER_SEC": "60", "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120"}
        previous = {"devices": [
            {"id": "retained-conflict", "ip": "192.168.100.52", "mac": "aa:bb:cc:dd:ee:01"},
            {"id": "retained-conflict", "ip": "192.168.100.52", "mac": "aa:bb:cc:dd:ee:02"},
        ]}
        with self.assertLogs("hioc-inventory-engine", level="WARNING") as logs:
            devices = merge_records([
                {"ip": "192.168.100.52", "source": "arp_table", "last_seen_source": "arp_table"},
            ], previous, "2026-07-12T23:21:19-06:00", 1000, config)

        self.assertEqual(len(devices), 3)
        self.assertIn("multiple_retained_mac_identities", " ".join(logs.output))

    def test_multiple_current_weak_identities_do_not_reconcile_to_retained_strong(self):
        config = {"HIOC_INVENTORY_STALE_AFTER_SEC": "60", "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120"}
        previous = {"devices": [{
            "id": stable_device_id({"mac": "aa:bb:cc:dd:ee:55"}),
            "ip": "192.168.100.55",
            "mac": "aa:bb:cc:dd:ee:55",
        }]}
        with self.assertLogs("hioc-inventory-engine", level="WARNING") as logs:
            devices = merge_records([
                {"ip": "192.168.100.55", "source": "arp_table", "_merge_key": "weak-a"},
                {"ip": "192.168.100.55", "source": "integration:weak", "_merge_key": "weak-b"},
            ], previous, "2026-07-12T23:21:19-06:00", 1000, config)

        self.assertEqual(len(devices), 3)
        self.assertIn("multiple_current_weak_identities", " ".join(logs.output))

    def test_current_weak_without_retained_strong_remains_ip_identity(self):
        config = {"HIOC_INVENTORY_STALE_AFTER_SEC": "60", "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120"}
        devices = merge_records([
            {"ip": "192.168.100.53", "source": "arp_table", "last_seen_source": "arp_table"},
        ], {"devices": []}, "2026-07-12T23:21:19-06:00", 1000, config)

        self.assertEqual(len(devices), 1)
        self.assertEqual(devices[0]["id"], stable_device_id({"ip": "192.168.100.53"}))
        self.assertEqual(devices[0]["mac"], "")

    def test_conflicting_current_and_retained_macs_remain_separate(self):
        config = {"HIOC_INVENTORY_STALE_AFTER_SEC": "60", "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120"}
        current_mac = "aa:bb:cc:dd:ee:01"
        retained_mac = "aa:bb:cc:dd:ee:02"
        previous = {"devices": [{
            "id": stable_device_id({"mac": retained_mac}),
            "ip": "192.168.100.54",
            "mac": retained_mac,
        }]}
        with self.assertLogs("hioc-inventory-engine", level="WARNING") as logs:
            devices = merge_records([
                {"ip": "192.168.100.54", "source": "arp_table"},
                {"ip": "192.168.100.54", "mac": current_mac, "source": "integration:current"},
            ], previous, "2026-07-12T23:21:19-06:00", 1000, config)

        self.assertEqual(len(devices), 2)
        self.assertEqual({device["mac"] for device in devices}, {current_mac, retained_mac})
        self.assertIn("conflicting_current_and_retained_macs", " ".join(logs.output))

    def test_different_mac_identities_on_same_ip_are_not_merged(self):
        config = {"HIOC_INVENTORY_STALE_AFTER_SEC": "60", "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120"}
        with self.assertLogs("hioc-inventory-engine", level="WARNING") as logs:
            devices = merge_records([
                {"ip": "192.168.100.50", "mac": "aa:bb:cc:dd:ee:01", "source": "arp_table"},
                {"ip": "192.168.100.50", "mac": "aa:bb:cc:dd:ee:02", "source": "dhcp_leases"},
            ], {"devices": []}, "2026-07-12T22:26:48-06:00", 1000, config)

        self.assertEqual(len(devices), 2)
        self.assertIn("multiple_mac_identities", " ".join(logs.output))

    def test_weak_identity_remains_separate_when_multiple_strong_macs_claim_ip(self):
        config = {"HIOC_INVENTORY_STALE_AFTER_SEC": "60", "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120"}
        with self.assertLogs("hioc-inventory-engine", level="WARNING"):
            devices = merge_records([
                {"ip": "192.168.100.51", "source": "arp_table"},
                {"ip": "192.168.100.51", "mac": "aa:bb:cc:dd:ee:01", "source": "dhcp_leases"},
                {"ip": "192.168.100.51", "mac": "aa:bb:cc:dd:ee:02", "source": "integration:test"},
            ], {"devices": []}, "2026-07-12T22:26:48-06:00", 1000, config)

        self.assertEqual(len(devices), 3)

    def test_reconciliation_preserves_known_infrastructure_enrichment(self):
        config = {"HIOC_INVENTORY_STALE_AFTER_SEC": "60", "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120"}
        observed = [
            {"ip": "192.168.100.60", "source": "arp_table"},
            {"ip": "192.168.100.60", "mac": "aa:bb:cc:dd:ee:60", "source": "dhcp_leases", "role": "Unknown"},
        ]
        known = [{
            "mac": "aa:bb:cc:dd:ee:60",
            "name": "Known Device",
            "role": "Network Equipment",
            "source": "known_infrastructure",
            "_observed": False,
            "_known_metadata_fields": ["name", "role"],
        }]
        devices = merge_records(append_known_infrastructure(observed, known), {"devices": []}, "2026-07-12T22:26:48-06:00", 1000, config)

        self.assertEqual(len(devices), 1)
        self.assertEqual(devices[0]["display_name"], "Known Device")
        self.assertEqual(devices[0]["role"], "Network Equipment")
        self.assertIn("known_infrastructure", devices[0]["source"])

    def test_retained_non_arp_weak_identity_without_strong_replacement_is_preserved(self):
        config = {"HIOC_INVENTORY_STALE_AFTER_SEC": "60", "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120"}
        weak_id = stable_device_id({"ip": "192.168.100.70"})
        previous = {"devices": [{
            "id": weak_id,
            "ip": "192.168.100.70",
            "mac": "",
            "first_seen": "2026-07-01T08:00:00-06:00",
            "last_seen_epoch": 100,
            "source": "integration:test",
        }]}
        devices = merge_records([
            {"ip": "192.168.100.71", "mac": "aa:bb:cc:dd:ee:71", "source": "arp_table"},
        ], previous, "2026-07-12T22:26:48-06:00", 1000, config)

        self.assertIn(weak_id, {device["id"] for device in devices})
        self.assertEqual(len(devices), 2)

    def test_production_shaped_weak_identities_reconcile(self):
        config = {"HIOC_INVENTORY_STALE_AFTER_SEC": "60", "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120"}
        cases = (
            ("192.168.100.219", "0e:38:76:1a:e3:ba"),
            ("192.168.100.140", "aa:bb:cc:dd:ee:40"),
            ("192.168.100.182", "aa:bb:cc:dd:ee:82"),
        )
        for ip, mac in cases:
            with self.subTest(ip=ip):
                previous = {"devices": [{
                    "id": stable_device_id({"ip": ip}),
                    "ip": ip,
                    "mac": "",
                    "first_seen": "2026-07-01T08:00:00-06:00",
                    "last_seen_epoch": 100,
                    "source": "arp_table",
                }]}
                devices = merge_records([
                    {"ip": ip, "mac": mac, "source": "dhcp_leases", "reachable": True},
                ], previous, "2026-07-12T22:26:48-06:00", 1000, config)

                self.assertEqual(len(devices), 1)
                self.assertEqual(devices[0]["id"], stable_device_id({"mac": mac}))

    def test_topology_links_children_to_gateway(self):
        gateway = {"id": "gateway", "ip": "192.168.1.1"}
        collector = {"id": "collector", "ip": "192.168.1.2"}
        endpoint = {"id": "endpoint", "ip": "192.168.1.10"}
        topology = build_topology([gateway, collector, endpoint], "192.168.1.1", "collector")
        self.assertEqual(topology["root_id"], "gateway")
        self.assertIn({"parent_id": "gateway", "child_id": "endpoint", "relationship": "network_parent"}, topology["edges"])

    def test_topology_uses_single_intermediate_infrastructure_device(self):
        gateway = {"id": "gateway", "ip": "192.168.1.1"}
        collector = {"id": "collector", "ip": "192.168.1.2"}
        satellite = {"id": "orbi-satellite", "ip": "192.168.1.3", "roles": ["wireless_infrastructure"]}
        endpoint = {"id": "endpoint", "ip": "192.168.1.10", "roles": ["endpoint"]}
        topology = build_topology([gateway, collector, satellite, endpoint], "192.168.1.1", "collector")
        self.assertIn({"parent_id": "gateway", "child_id": "orbi-satellite", "relationship": "network_parent"}, topology["edges"])
        self.assertIn({"parent_id": "orbi-satellite", "child_id": "endpoint", "relationship": "network_parent"}, topology["edges"])

    def test_topology_uses_integration_parent_hints(self):
        gateway = {"id": "gateway", "ip": "192.168.1.1"}
        switch = {"id": "switch", "ip": "192.168.1.4", "mac": "11:22:33:44:55:66", "roles": ["switch"]}
        endpoint = {"id": "endpoint", "ip": "192.168.1.20", "parent_mac": "11:22:33:44:55:66", "roles": ["endpoint"]}
        topology = build_topology([gateway, switch, endpoint], "192.168.1.1", "")
        self.assertIn({"parent_id": "switch", "child_id": "endpoint", "relationship": "network_parent"}, topology["edges"])

    def test_classification_detects_infrastructure_names(self):
        primary, roles = classify_device({"hostname": "orbi-satellite-office", "ip": "192.168.1.3"}, "192.168.1.1", set())
        self.assertEqual(primary, "network_infrastructure")
        self.assertIn("wireless_infrastructure", roles)
        self.assertEqual(operator_role({}, roles), "Network Equipment")
        self.assertEqual(inventory_class("Network Equipment"), "infrastructure")

    def test_gateway_is_network_equipment_infrastructure(self):
        primary, roles = classify_device({"name": "Default Gateway", "ip": "192.168.1.1"}, "192.168.1.1", set())

        self.assertEqual(primary, "gateway")
        self.assertIn("gateway", roles)
        self.assertEqual(operator_role({}, roles), "Network Equipment")
        self.assertEqual(inventory_class("Network Equipment"), "infrastructure")

    def test_local_pihole_host_is_core_infrastructure(self):
        primary, roles = classify_device({"hostname": "nutandpihole", "ip": "192.168.1.252"}, "192.168.1.1", {"192.168.1.252"})

        self.assertEqual(primary, "collector")
        self.assertIn("collector", roles)
        self.assertIn("dns", roles)
        self.assertEqual(operator_role({}, roles), "Core Infrastructure")
        self.assertEqual(inventory_class("Core Infrastructure"), "infrastructure")

    def test_classification_detects_client_roles(self):
        _, roles = classify_device({"hostname": "living-room-tv", "ip": "192.168.1.40"}, "192.168.1.1", set())
        self.assertIn("media", roles)
        self.assertEqual(operator_role({}, roles), "Media")
        self.assertEqual(inventory_class("Media"), "client")

    def test_merge_records_adds_operator_inventory_fields(self):
        config = {"HIOC_INVENTORY_STALE_AFTER_SEC": "60", "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120"}
        devices = merge_records([
            {
                "ip": "192.168.1.3",
                "mac": "11:22:33:44:55:66",
                "hostname": "orbi-satellite-office",
                "roles": ["wireless_infrastructure"],
                "role": "Network Equipment",
                "inventory_class": "infrastructure",
                "source": "neighbor_table",
            }
        ], {"devices": []}, "now", 100, config)

        self.assertEqual(devices[0]["name"], "orbi-satellite-office")
        self.assertEqual(devices[0]["role"], "Network Equipment")
        self.assertEqual(devices[0]["inventory_class"], "infrastructure")
        self.assertEqual(devices[0]["status"], "online")
        self.assertEqual(devices[0]["health"], "healthy")

    def test_missing_known_infrastructure_file_is_nonfatal(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "known_infrastructure.json"
            records = known_infrastructure({"HIOC_INVENTORY_KNOWN_INFRASTRUCTURE_FILE": str(missing)})

        self.assertEqual(records, [])

    def test_empty_known_infrastructure_config_disables_loading(self):
        records = known_infrastructure({"HIOC_INVENTORY_KNOWN_INFRASTRUCTURE_FILE": ""})

        self.assertEqual(records, [])

    def test_valid_known_infrastructure_definition_creates_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "known_infrastructure.json"
            path.write_text('{"devices":[{"id":"gateway","name":"Huawei Gateway","ip":"192.168.1.1","mac":"aa-bb-cc-dd-ee-ff","role":"Network Equipment","type":"gateway","vendor":"Huawei","enabled":true}]}')
            records = known_infrastructure({"HIOC_INVENTORY_KNOWN_INFRASTRUCTURE_FILE": str(path)})

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["mac"], "aa:bb:cc:dd:ee:ff")
        self.assertEqual(records[0]["source"], "known_infrastructure")
        self.assertFalse(records[0]["_observed"])

    def test_known_infrastructure_mac_match_enriches_existing_passive_device(self):
        config = {"HIOC_INVENTORY_STALE_AFTER_SEC": "60", "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120"}
        observed = [{"ip": "192.168.1.2", "mac": "aa:bb:cc:dd:ee:ff", "source": "arp_table", "roles": ["endpoint"], "role": "Unknown", "inventory_class": "client"}]
        known = [{"mac": "aa:bb:cc:dd:ee:ff", "name": "Office Switch", "role": "Network Equipment", "source": "known_infrastructure", "_observed": False, "_known_metadata_fields": ["name", "role"]}]

        devices = merge_records(append_known_infrastructure(observed, known), {"devices": []}, "now", 100, config)

        self.assertEqual(len(devices), 1)
        self.assertEqual(devices[0]["display_name"], "Office Switch")
        self.assertEqual(devices[0]["role"], "Network Equipment")
        self.assertEqual(devices[0]["inventory_class"], "infrastructure")
        self.assertEqual(devices[0]["status"], "online")
        self.assertIn("arp_table", devices[0]["source"])
        self.assertIn("known_infrastructure", devices[0]["source"])

    def test_known_metadata_does_not_override_observed_runtime_identity_with_empty_values(self):
        config = {"HIOC_INVENTORY_STALE_AFTER_SEC": "60", "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120"}
        observed = [{"ip": "192.168.1.2", "mac": "aa:bb:cc:dd:ee:ff", "hostname": "observed-host", "source": "dhcp_leases"}]
        known = [{"mac": "aa:bb:cc:dd:ee:ff", "name": "Preferred Name", "source": "known_infrastructure", "_observed": False, "_known_metadata_fields": ["name"]}]

        devices = merge_records(append_known_infrastructure(observed, known), {"devices": []}, "now", 100, config)

        self.assertEqual(devices[0]["hostname"], "observed-host")
        self.assertEqual(devices[0]["display_name"], "Preferred Name")
        self.assertNotIn("last_seen", devices[0])
        self.assertEqual(devices[0]["observation_status"], "unknown")

    def test_invalid_known_infrastructure_records_are_rejected_partially(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "known_infrastructure.json"
            path.write_text('{"devices":[{"name":"Bad MAC","mac":"not-a-mac"},{"name":"UPS","role":"Core Infrastructure"}]}')
            records = known_infrastructure({"HIOC_INVENTORY_KNOWN_INFRASTRUCTURE_FILE": str(path)})

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["name"], "UPS")

    def test_duplicate_known_identifiers_keep_first_valid_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "known_infrastructure.json"
            path.write_text('{"devices":[{"id":"switch","name":"Switch A","mac":"aa:bb:cc:dd:ee:ff"},{"id":"switch","name":"Switch B","mac":"11:22:33:44:55:66"},{"id":"ap","name":"AP","mac":"aa:bb:cc:dd:ee:ff"}]}')
            records = known_infrastructure({"HIOC_INVENTORY_KNOWN_INFRASTRUCTURE_FILE": str(path)})

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["name"], "Switch A")

    def test_disabled_known_definition_is_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "known_infrastructure.json"
            path.write_text('{"devices":[{"name":"Disabled UPS","role":"Core Infrastructure","enabled":false}]}')
            records = known_infrastructure({"HIOC_INVENTORY_KNOWN_INFRASTRUCTURE_FILE": str(path)})

        self.assertEqual(records, [])

    def test_conflicting_known_identifiers_do_not_collapse_unrelated_devices(self):
        observed = [{"ip": "192.168.1.20", "mac": "aa:bb:cc:dd:ee:ff", "source": "arp_table"}]
        known = [{"ip": "192.168.1.20", "mac": "11:22:33:44:55:66", "name": "Wrong Device", "source": "known_infrastructure", "_observed": False, "_known_metadata_fields": ["name"]}]

        records = append_known_infrastructure(observed, known)

        self.assertEqual(records, observed)

    def test_known_parent_alias_is_resolved_for_topology_hints(self):
        parent = {"id": "dev_parent", "_configured_id": "switch"}
        child = {"id": "dev_child", "parent_id": "switch"}

        resolve_configured_parent_ids([parent, child])

        self.assertEqual(child["parent_id"], "dev_parent")

    def test_configured_never_observed_device_is_offline_without_last_seen(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "known_infrastructure.json"
            path.write_text('{"devices":[{"id":"ups","name":"UPS","role":"Core Infrastructure","type":"network_device"}]}')
            config = {
                "HIOC_HOME": tmp,
                "HIOC_INVENTORY_KNOWN_INFRASTRUCTURE_FILE": str(path),
                "HIOC_INVENTORY_STALE_AFTER_SEC": "60",
                "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120",
                "HIOC_INVENTORY_ACTIVE_DISCOVERY": "off",
            }
            with patch("hioc.inventory.local_ipv4_addresses", return_value=[]), \
                 patch("hioc.inventory.default_gateway", return_value={}), \
                 patch("hioc.inventory.neighbor_table", return_value={}), \
                 patch("hioc.inventory.systemd_services", return_value={}), \
                 patch("hioc.inventory.listening_services", return_value=[]), \
                 patch("hioc.inventory.package_version", return_value=""):
                inventory = discover_inventory(config, {"devices": []})

        device = next(item for item in inventory["devices"] if item["display_name"] == "UPS")
        self.assertEqual(device["health_status"], "offline")
        self.assertEqual(device["status"], "offline")
        self.assertNotIn("last_seen", device)
        self.assertNotIn("last_seen_epoch", device)
        self.assertFalse(any(key.startswith("_") for key in device))

    def test_known_parent_alias_flows_through_discovery_topology(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "known_infrastructure.json"
            path.write_text('{"devices":[{"id":"gateway","name":"Gateway","ip":"192.168.1.1","role":"Network Equipment"},{"id":"switch","name":"Switch","role":"Network Equipment","parent_id":"gateway"}]}')
            config = {
                "HIOC_HOME": tmp,
                "HIOC_INVENTORY_KNOWN_INFRASTRUCTURE_FILE": str(path),
                "HIOC_INVENTORY_STALE_AFTER_SEC": "60",
                "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120",
                "HIOC_INVENTORY_ACTIVE_DISCOVERY": "off",
            }
            with patch("hioc.inventory.local_ipv4_addresses", return_value=[]), \
                 patch("hioc.inventory.default_gateway", return_value={}), \
                 patch("hioc.inventory.neighbor_table", return_value={}), \
                 patch("hioc.inventory.systemd_services", return_value={}), \
                 patch("hioc.inventory.listening_services", return_value=[]), \
                 patch("hioc.inventory.package_version", return_value=""):
                inventory = discover_inventory(config, {"devices": []})

        devices = {item["display_name"]: item for item in inventory["devices"]}
        gateway_id = devices["Gateway"]["id"]
        switch_id = devices["Switch"]["id"]
        self.assertIn({"parent_id": gateway_id, "child_id": switch_id, "relationship": "network_parent"}, inventory["topology"]["edges"])
        self.assertFalse(any(any(key.startswith("_") for key in device) for device in inventory["devices"]))

    def test_local_services_keep_pre_enrichment_collector_ownership(self):
        collector_mac = "b8:27:eb:70:ab:df"
        client_mac = "bc:dd:c2:0d:f7:77"
        collector_id = stable_device_id({"mac": collector_mac})
        client_id = stable_device_id({"mac": client_mac})
        local_addresses = [
            {"interface": "eth0", "cidr": "192.168.100.252/24", "ip": "192.168.100.252", "mac": collector_mac},
            {"interface": "docker0", "cidr": "172.17.0.1/16", "ip": "172.17.0.1", "mac": "02:42:63:a7:ca:d9"},
        ]
        neighbor = {"192.168.100.105": {"ip": "192.168.100.105", "mac": client_mac, "source": "arp_table", "last_seen_source": "arp_table"}}
        systemd = {
            "pihole-FTL": {"status": "active"},
            "cron": {"status": "active"},
            "ssh": {"status": "active"},
            "nut-monitor": {"status": "active"},
            "nut-server": {"status": "active"},
        }
        sockets = [
            {"port": 53, "status": "listening"},
            {"port": 67, "status": "listening"},
        ]

        with tempfile.TemporaryDirectory() as tmp:
            known_path = Path(tmp) / "known_infrastructure.json"
            known_path.write_text(json.dumps({"devices": [{
                "name": "Pi3 - NUT and Pi-hole",
                "hostname": "nutandpihole",
                "ip": "192.168.100.252",
                "mac": collector_mac,
                "role": "Core Infrastructure",
                "type": "server",
                "vendor": "Raspberry Pi",
                "model": "Raspberry Pi 3",
                "notes": "Collector metadata",
            }]}))
            config = {
                "HIOC_HOME": tmp,
                "HIOC_INVENTORY_KNOWN_INFRASTRUCTURE_FILE": str(known_path),
                "HIOC_INVENTORY_STALE_AFTER_SEC": "60",
                "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120",
                "HIOC_INVENTORY_ACTIVE_DISCOVERY": "off",
            }
            with patch("hioc.inventory.local_ipv4_addresses", return_value=local_addresses), \
                 patch("hioc.inventory.socket.gethostname", return_value="nutandpihole"), \
                 patch("hioc.inventory.default_gateway", return_value={}), \
                 patch("hioc.inventory.neighbor_table", return_value=neighbor), \
                 patch("hioc.inventory.dhcp_lease_discovery", return_value=({}, "dhcp_leases_unavailable")), \
                 patch("hioc.inventory.integration_inventory", return_value={}), \
                 patch("hioc.inventory.systemd_services", return_value=systemd), \
                 patch("hioc.inventory.listening_services", return_value=sockets), \
                 patch("hioc.inventory.package_version", return_value=""):
                inventory = discover_inventory(config, {"devices": []})

        devices = {device["id"]: device for device in inventory["devices"]}
        collector = devices[collector_id]
        client = devices[client_id]
        self.assertNotEqual(collector_id, client_id)
        self.assertEqual(collector["type"], "local_host")
        self.assertEqual(collector["ip"], "192.168.100.252")
        self.assertEqual(collector["mac"], collector_mac)
        self.assertEqual(collector["interfaces"], local_addresses)
        self.assertEqual(collector["hostname"], "nutandpihole")
        self.assertTrue(collector["reachable"])
        self.assertIn("local_host", collector["sources"])
        self.assertEqual(collector["display_name"], "Pi3 - NUT and Pi-hole")
        self.assertEqual(collector["role"], "Core Infrastructure")
        self.assertEqual(collector["vendor"], "Raspberry Pi")
        self.assertEqual(collector["model"], "Raspberry Pi 3")
        self.assertEqual(collector["notes"], "Collector metadata")
        self.assertEqual(client["ip"], "192.168.100.105")
        self.assertTrue(inventory["services"])
        self.assertEqual({service["device_id"] for service in inventory["services"]}, {collector_id})
        self.assertEqual({service["host"] for service in inventory["services"]}, {"Pi3 - NUT and Pi-hole"})
        service_ids = {service["id"] for service in inventory["services"]}
        self.assertTrue(any(edge["to_id"] in service_ids for edge in inventory["dependencies"]["edges"]))

    def test_missing_canonical_local_device_omits_local_services_without_fallback(self):
        local_address = {"interface": "eth0", "cidr": "192.168.1.2/24", "ip": "192.168.1.2", "mac": "aa:bb:cc:dd:ee:01"}
        unrelated = {
            "id": stable_device_id({"mac": "aa:bb:cc:dd:ee:02"}),
            "ip": "192.168.1.50",
            "mac": "aa:bb:cc:dd:ee:02",
            "type": "endpoint",
            "display_name": "Unrelated endpoint",
            "health_status": "healthy",
            "roles": ["endpoint"],
        }
        config = {
            "HIOC_HOME": "/nonexistent",
            "HIOC_INVENTORY_KNOWN_INFRASTRUCTURE_FILE": "",
            "HIOC_INVENTORY_STALE_AFTER_SEC": "60",
            "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120",
            "HIOC_INVENTORY_ACTIVE_DISCOVERY": "off",
        }
        with patch("hioc.inventory.local_ipv4_addresses", return_value=[local_address]), \
             patch("hioc.inventory.default_gateway", return_value={}), \
             patch("hioc.inventory.neighbor_table", return_value={}), \
             patch("hioc.inventory.dhcp_lease_discovery", return_value=({}, "dhcp_leases_unavailable")), \
             patch("hioc.inventory.integration_inventory", return_value={}), \
             patch("hioc.inventory.merge_records", return_value=[unrelated]), \
             patch("hioc.inventory.systemd_services") as systemd, \
             patch("hioc.inventory.listening_services") as sockets, \
             patch("hioc.inventory.package_version", return_value=""), \
             self.assertLogs("hioc-inventory-engine", level="ERROR") as logs:
            inventory = discover_inventory(config, {"devices": []})

        self.assertEqual(inventory["services"], [])
        systemd.assert_not_called()
        sockets.assert_not_called()
        self.assertIn("canonical local device id", " ".join(logs.output))
        self.assertIn(stable_device_id(local_address), " ".join(logs.output))

    def test_interface_order_changes_identity_selection_but_not_local_service_ownership(self):
        physical = {"interface": "eth0", "cidr": "192.168.1.2/24", "ip": "192.168.1.2", "mac": "aa:bb:cc:dd:ee:01"}
        bridge = {"interface": "docker0", "cidr": "172.17.0.1/16", "ip": "172.17.0.1", "mac": "02:42:ac:11:00:01"}
        endpoint_mac = "aa:bb:cc:dd:ee:99"
        endpoint_id = stable_device_id({"mac": endpoint_mac})
        config = {
            "HIOC_HOME": "/nonexistent",
            "HIOC_INVENTORY_KNOWN_INFRASTRUCTURE_FILE": "",
            "HIOC_INVENTORY_STALE_AFTER_SEC": "60",
            "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120",
            "HIOC_INVENTORY_ACTIVE_DISCOVERY": "off",
        }

        for addresses in ([physical, bridge], [bridge, physical]):
            with self.subTest(first_interface=addresses[0]["interface"]), \
                 patch("hioc.inventory.local_ipv4_addresses", return_value=addresses), \
                 patch("hioc.inventory.default_gateway", return_value={}), \
                 patch("hioc.inventory.neighbor_table", return_value={"192.168.1.99": {"ip": "192.168.1.99", "mac": endpoint_mac, "source": "arp_table"}}), \
                 patch("hioc.inventory.dhcp_lease_discovery", return_value=({}, "dhcp_leases_unavailable")), \
                 patch("hioc.inventory.integration_inventory", return_value={}), \
                 patch("hioc.inventory.systemd_services", return_value={"cron": {"status": "active"}}), \
                 patch("hioc.inventory.listening_services", return_value=[]), \
                 patch("hioc.inventory.package_version", return_value=""):
                inventory = discover_inventory(config, {"devices": []})

            canonical_id = stable_device_id(addresses[0])
            self.assertEqual({service["device_id"] for service in inventory["services"]}, {canonical_id})
            self.assertNotIn(endpoint_id, {service["device_id"] for service in inventory["services"]})

    def test_existing_integration_hint_behavior_remains_compatible(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "integrations"
            root.mkdir()
            (root / "orbi.json").write_text('{"devices":[{"name":"Orbi Satellite","ip":"192.168.1.3","mac":"aa:bb:cc:dd:ee:ff","parent_ip":"192.168.1.1"}]}')
            devices = integration_inventory({"HIOC_INVENTORY_INTEGRATION_DIR": str(root)}, Path(tmp))

        self.assertEqual(devices["aa:bb:cc:dd:ee:ff"]["source"], "integration:orbi")
        self.assertEqual(devices["aa:bb:cc:dd:ee:ff"]["parent_ip"], "192.168.1.1")

    def test_subnet_scan_is_disabled_for_safe_inventory(self):
        self.assertEqual(scan_subnet("192.168.1.0/24", 1, 1), {})

    def test_dhcp_lease_parsing_when_file_is_present(self):
        with tempfile.TemporaryDirectory() as tmp:
            lease_file = Path(tmp) / "dhcp.leases"
            lease_file.write_text("1780000000 aa:bb:cc:dd:ee:ff 192.168.1.50 phone-one 01:aa:bb:cc:dd:ee:ff\n")

            leases = dhcp_leases([lease_file])
            discovered, status = dhcp_lease_discovery({"HIOC_INVENTORY_DHCP_LEASE_FILES": str(lease_file)})

        lease = leases["aa:bb:cc:dd:ee:ff"]
        self.assertEqual(lease["hostname"], "phone-one")
        self.assertEqual(lease["source"], "dhcp_leases")
        self.assertEqual(lease["lease_expires_epoch"], 1780000000)
        self.assertEqual(lease["dhcp_client_id"], "01:aa:bb:cc:dd:ee:ff")
        self.assertEqual(lease["dhcp_lease_source"], str(lease_file))
        self.assertFalse(lease["_positive_observation"])
        self.assertEqual(discovered["aa:bb:cc:dd:ee:ff"]["ip"], "192.168.1.50")
        self.assertEqual(status, "dhcp_leases_found")

    def test_dhcp_lease_missing_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "missing.leases"
            discovered, status = dhcp_lease_discovery({"HIOC_INVENTORY_DHCP_LEASE_FILES": str(missing)})

        self.assertEqual(discovered, {})
        self.assertEqual(status, "dhcp_leases_missing")

    def test_dhcp_lease_source_statuses_distinguish_empty_unreadable_and_io_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            lease_file = Path(tmp) / "dhcp.leases"
            lease_file.write_text("")
            self.assertEqual(dhcp_lease_discovery({"HIOC_INVENTORY_DHCP_LEASE_FILES": str(lease_file)})[1], "dhcp_leases_empty")
            with patch.object(Path, "read_text", side_effect=PermissionError("denied")):
                results = dhcp_lease_source_results([lease_file])
                discovered, status = dhcp_lease_discovery({"HIOC_INVENTORY_DHCP_LEASE_FILES": str(lease_file)})
            self.assertEqual(results[0].status, "unreadable")
            self.assertEqual(discovered, {})
            self.assertEqual(status, "dhcp_leases_unreadable")
            with patch.object(Path, "read_text", side_effect=OSError("I/O failure")):
                discovered, status = dhcp_lease_discovery({"HIOC_INVENTORY_DHCP_LEASE_FILES": str(lease_file)})
            self.assertEqual(discovered, {})
            self.assertEqual(status, "dhcp_leases_io_error")

    def test_dhcp_lease_parser_rejects_invalid_fields_and_reports_malformed(self):
        invalid_lines = (
            "not-an-expiry aa:bb:cc:dd:ee:ff 192.168.1.2 host",
            "-1 aa:bb:cc:dd:ee:ff 192.168.1.2 host",
            "100 not-a-mac 192.168.1.2 host",
            "100 aa:bb:cc:dd:ee:ff not-an-ip host",
            "too short",
        )
        with tempfile.TemporaryDirectory() as tmp:
            lease_file = Path(tmp) / "dhcp.leases"
            lease_file.write_text("\n".join(invalid_lines))
            with self.assertLogs("hioc-inventory-engine", level="WARNING") as logs:
                discovered, status = dhcp_lease_discovery({"HIOC_INVENTORY_DHCP_LEASE_FILES": str(lease_file)})
        self.assertEqual(discovered, {})
        self.assertEqual(status, "dhcp_leases_malformed")
        self.assertEqual(len(logs.output), len(invalid_lines))
        self.assertNotIn("not-a-mac 192.168.1.2", " ".join(logs.output))

    def test_dhcp_lease_parser_reports_partial_and_preserves_placeholder_and_infinite_lease(self):
        with tempfile.TemporaryDirectory() as tmp:
            lease_file = Path(tmp) / "dhcp.leases"
            lease_file.write_text(
                "0 aa:bb:cc:dd:ee:01 192.168.1.10 * *\n"
                "malformed line\n"
            )
            with self.assertLogs("hioc-inventory-engine", level="WARNING"):
                discovered, status = dhcp_lease_discovery({"HIOC_INVENTORY_DHCP_LEASE_FILES": str(lease_file)})
        lease = discovered["aa:bb:cc:dd:ee:01"]
        self.assertEqual(status, "dhcp_leases_partial")
        self.assertEqual(lease["lease_expires_epoch"], 0)
        self.assertEqual(lease["hostname"], "")
        self.assertEqual(lease["dhcp_client_id"], "")

    def test_dhcp_lease_duplicates_and_conflicting_macs_are_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            lease_file = Path(tmp) / "dhcp.leases"
            lease_file.write_text(
                "100 aa:bb:cc:dd:ee:01 192.168.1.10 first *\n"
                "200 aa:bb:cc:dd:ee:01 192.168.1.10 latest *\n"
                "300 aa:bb:cc:dd:ee:02 192.168.1.10 other *\n"
            )
            discovered, status = dhcp_lease_discovery({"HIOC_INVENTORY_DHCP_LEASE_FILES": str(lease_file)})
        self.assertEqual(status, "dhcp_leases_found")
        self.assertEqual(len(discovered), 2)
        self.assertEqual(discovered["aa:bb:cc:dd:ee:01"]["hostname"], "latest")
        devices = merge_records(list(discovered.values()), {"devices": []}, "now", 1000, {"HIOC_INVENTORY_STALE_AFTER_SEC": "60", "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120"})
        self.assertEqual({device["mac"] for device in devices}, {"aa:bb:cc:dd:ee:01", "aa:bb:cc:dd:ee:02"})

    def test_multiple_dhcp_lease_paths_merge_valid_sources_and_report_partial_failures(self):
        with tempfile.TemporaryDirectory() as tmp:
            valid = Path(tmp) / "valid.leases"
            malformed = Path(tmp) / "malformed.leases"
            valid.write_text("100 aa:bb:cc:dd:ee:01 192.168.1.10 host *\n")
            malformed.write_text("bad line\n")
            config = {"HIOC_INVENTORY_DHCP_LEASE_FILES": f"{valid},{malformed}"}
            self.assertEqual([str(path) for path in dhcp_lease_paths(config)], [str(valid), str(malformed)])
            with self.assertLogs("hioc-inventory-engine", level="WARNING"):
                discovered, status = dhcp_lease_discovery(config)
        self.assertEqual(set(discovered), {"aa:bb:cc:dd:ee:01"})
        self.assertEqual(status, "dhcp_leases_partial")

    def test_dhcp_merge_fills_missing_metadata_without_overwriting_stronger_observation(self):
        config = {"HIOC_INVENTORY_STALE_AFTER_SEC": "60", "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120"}
        mac = "aa:bb:cc:dd:ee:01"
        dhcp = {
            "ip": "192.168.1.20",
            "mac": mac,
            "hostname": "lease-name",
            "lease_expires_epoch": 2000,
            "dhcp_client_id": "client-id",
            "dhcp_lease_source": "/lease/file",
            "source": "dhcp_leases",
            "last_seen_source": "/lease/file",
            "_positive_observation": False,
            "roles": ["endpoint"],
            "type": "endpoint",
        }
        arp = {"ip": "192.168.1.20", "mac": mac, "hostname": "", "source": "arp_table", "last_seen_source": "arp_table", "roles": ["endpoint"]}
        devices = merge_records([arp, dhcp], {"devices": []}, "now", 1000, config)
        self.assertEqual(devices[0]["hostname"], "lease-name")
        self.assertEqual(devices[0]["last_seen_epoch"], 1000)
        self.assertEqual(devices[0]["last_seen_source"], "arp_table")
        self.assertEqual(devices[0]["lease_expires_epoch"], 2000)
        self.assertIn("dhcp_leases", devices[0]["sources"])

        arp["hostname"] = "strong-name"
        devices = merge_records([arp, {**dhcp, "hostname": "weak-name"}], {"devices": []}, "now", 1000, config)
        self.assertEqual(devices[0]["hostname"], "strong-name")

    def test_dhcp_does_not_refresh_retained_positive_observation(self):
        config = {"HIOC_INVENTORY_STALE_AFTER_SEC": "60", "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120"}
        mac = "aa:bb:cc:dd:ee:01"
        previous = {"devices": [{
            "id": stable_device_id({"mac": mac}),
            "ip": "192.168.1.20",
            "mac": mac,
            "reachable": True,
            "source": "arp_table",
            "sources": ["arp_table"],
            "last_seen": "earlier",
            "last_seen_epoch": 800,
        }]}
        dhcp = {
            "ip": "192.168.1.20",
            "mac": mac,
            "hostname": "weak-name",
            "lease_expires_epoch": 2000,
            "source": "dhcp_leases",
            "_positive_observation": False,
        }
        devices = merge_records([dhcp], previous, "now", 1000, config)
        device = devices[0]
        self.assertEqual(device["last_seen"], "earlier")
        self.assertEqual(device["last_seen_epoch"], 800)
        self.assertNotEqual(device["observation_status"], "recent")

    def test_current_local_identity_remains_authoritative_over_dhcp_assignment(self):
        config = {"HIOC_INVENTORY_STALE_AFTER_SEC": "60", "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120"}
        mac = "aa:bb:cc:dd:ee:01"
        local = {
            "ip": "192.168.1.20",
            "mac": mac,
            "hostname": "authoritative-name",
            "name": "Operator Name",
            "interfaces": [{"interface": "eth0", "ip": "192.168.1.20"}],
            "reachable": True,
            "type": "local_host",
            "roles": ["collector"],
            "role": "Core Infrastructure",
            "source": "local_host",
        }
        dhcp = {
            "ip": "192.168.1.99",
            "mac": mac,
            "hostname": "weak-name",
            "lease_expires_epoch": 2000,
            "source": "dhcp_leases",
        }
        device = merge_records([local, dhcp], {"devices": []}, "now", 1000, config)[0]
        self.assertEqual(device["ip"], "192.168.1.20")
        self.assertEqual(device["hostname"], "authoritative-name")
        self.assertEqual(device["name"], "Operator Name")
        self.assertEqual(device["interfaces"], local["interfaces"])
        self.assertTrue(device["reachable"])
        self.assertEqual(device["type"], "local_host")
        self.assertEqual(device["lease_expires_epoch"], 2000)

    def test_missing_optional_device_fields_do_not_break_dashboard_payloads(self):
        infrastructure, _ = inventory_summary_lists([
            {
                "display_name": "Default Gateway",
                "inventory_class": "infrastructure",
                "health_status": "healthy",
            }
        ], [])

        self.assertEqual(infrastructure[0]["name"], "Default Gateway")
        self.assertEqual(infrastructure[0]["ip"], "")
        self.assertEqual(infrastructure[0]["mac"], "")
        self.assertEqual(infrastructure[0]["vendor"], "")
        self.assertEqual(infrastructure[0]["source"], "")

    def test_summary_counts_are_never_none(self):
        summary = build_inventory_summary(
            devices=[
                {"inventory_class": "infrastructure", "health_status": "healthy", "health_score": 100},
                {"inventory_class": "client", "health_status": "watch", "health_score": 80},
            ],
            services=[{"name": "Pi-hole FTL", "host": "Pi4", "type": "dns", "status": "active"}],
            topology={"edges": []},
            dependencies={"edges": []},
            now="now",
            discovery_sources=["local_host", "gateway", "arp_table", "dhcp_leases_unavailable"],
            discovery_limited=True,
            discovery_limit_reason="limited",
        )

        for key in ("infrastructure_count", "client_count", "network_client_count", "service_count", "healthy_count", "watch_count", "degraded_count", "offline_count"):
            self.assertIsNotNone(summary[key])
        self.assertEqual(summary["infrastructure_count"], 1)
        self.assertEqual(summary["client_count"], 1)
        self.assertEqual(summary["discovery_sources"][-1], "dhcp_leases_unavailable")

    def test_dependencies_include_core_services(self):
        devices = [{"id": "collector", "health_status": "healthy"}, {"id": "endpoint", "health_status": "healthy"}]
        services = [{"id": "svc_dns", "type": "dns"}, {"id": "svc_mqtt", "type": "mqtt"}]
        dependencies = build_dependencies(devices, services)
        edge_types = {edge["type"] for edge in dependencies["edges"]}
        self.assertIn("depends_on_dns", edge_types)
        self.assertIn("depends_on_mqtt", edge_types)

    def test_services_are_enriched_with_host_and_dependencies(self):
        devices = [{"id": "collector", "display_name": "Pi4"}]
        services = [{"id": "svc_mqtt", "name": "MQTT listener", "type": "mqtt", "device_id": "collector", "status": "listening"}]
        dependencies = {"edges": [{"from_id": "svc_mqtt", "to_id": "svc_dns", "type": "depends_on_dns"}]}
        enriched = enrich_services(services, devices, dependencies)

        self.assertEqual(enriched[0]["host"], "Pi4")
        self.assertEqual(enriched[0]["dependency"], "depends_on_dns")


if __name__ == "__main__":
    unittest.main()
