import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "pi4" / "lib"))

from hioc.inventory import (
    build_dependencies,
    build_topology,
    classify_device,
    enrich_services,
    health_score,
    inventory_class,
    merge_records,
    normalize_mac,
    operator_role,
    scan_subnet,
    stable_device_id,
)


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

    def test_subnet_scan_is_disabled_for_safe_inventory(self):
        self.assertEqual(scan_subnet("192.168.1.0/24", 1, 1), {})

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
