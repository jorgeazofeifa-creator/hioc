import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "pi4" / "lib"))

from hioc.core.correlation import (
    build_event_signals,
    build_inventory_signals,
    build_telemetry_signals,
    correlate,
    lifecycle_phase,
)
from hioc.inventory import merge_records, neighbor_table


DEFAULT_CONFIG = {
    "HIOC_WARN_INTERNET_LATENCY_MS": "120",
    "HIOC_MAJOR_INTERNET_LATENCY_MS": "250",
    "HIOC_WARN_PACKET_LOSS_PERCENT": "1",
    "HIOC_MAJOR_PACKET_LOSS_PERCENT": "10",
    "HIOC_WARN_DNS_LATENCY_MS": "100",
    "HIOC_MAJOR_DNS_LATENCY_MS": "500",
    "HIOC_WARN_GATEWAY_LATENCY_MS": "20",
    "HIOC_MAJOR_GATEWAY_LATENCY_MS": "100",
    "HIOC_WARN_MQTT_PUBLISH_MS": "500",
    "HIOC_MAJOR_MQTT_PUBLISH_MS": "2000",
    "HIOC_WARN_PI4_TEMP_C": "65",
    "HIOC_MAJOR_PI4_TEMP_C": "75",
}


class CorrelationEngineTests(unittest.TestCase):
    def test_internet_degradation_root_cause_uses_gateway_context(self):
        telemetry = {
            "gateway_status": "online",
            "gateway_latency_ms": 4,
            "packet_loss_percent": 7,
            "internet_latency_ms": 321,
            "internet_health": "degraded",
            "dns_latency_ms": 25,
            "mqtt_publish_ms": 45,
            "pi5_status": "online",
            "pi4_temperature_c": 44,
        }
        incident = correlate(build_telemetry_signals(telemetry, DEFAULT_CONFIG), {})

        self.assertEqual(incident["key"], "internet_degradation_isp_likely")
        self.assertEqual(incident["root_cause"], "ISP or upstream routing")
        self.assertGreaterEqual(incident["confidence_percent"], 86)
        self.assertIn("Internet", incident["affected"])

    def test_gateway_degradation_takes_precedence_over_downstream_symptoms(self):
        telemetry = {
            "gateway_status": "offline",
            "gateway_latency_ms": 0,
            "packet_loss_percent": 100,
            "internet_latency_ms": 0,
            "internet_health": "critical",
            "dns_latency_ms": 0,
            "mqtt_publish_ms": 0,
            "pi5_status": "online",
            "pi4_temperature_c": 44,
        }
        incident = correlate(build_telemetry_signals(telemetry, DEFAULT_CONFIG), {})

        self.assertEqual(incident["key"], "network_path_degradation")
        self.assertEqual(incident["system"], "Gateway")
        self.assertEqual(incident["severity"], "critical")
        self.assertIn("DNS", incident["affected"])

    def test_inventory_correlation_expands_affected_systems_from_graph(self):
        inventory = {
            "devices": [
                {
                    "id": "switch_1",
                    "display_name": "Office Switch",
                    "health_status": "offline",
                    "health_score": 0,
                    "health_reasons": ["not seen within offline threshold"],
                    "roles": ["switch"],
                },
                {"id": "camera_1", "display_name": "Driveway Camera", "health_status": "healthy"},
            ],
            "services": [{"id": "svc_camera", "device_id": "camera_1", "name": "Frigate Camera Stream", "type": "camera"}],
            "topology": {"edges": [{"parent_id": "switch_1", "child_id": "camera_1", "relationship": "network_parent"}]},
            "dependencies": {"edges": [{"from_id": "switch_1", "to_id": "svc_camera", "type": "depends_on_network"}]},
        }
        incident = correlate(build_inventory_signals(inventory), inventory)

        self.assertTrue(incident["key"].startswith("inventory_"))
        self.assertEqual(incident["root_cause"], "Office Switch")
        self.assertIn("Driveway Camera", incident["affected"])
        self.assertIn("Frigate Camera Stream", incident["affected"])

    def test_reconciled_identity_produces_only_one_inventory_signal(self):
        config = {"HIOC_INVENTORY_STALE_AFTER_SEC": "60", "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120"}
        previous = {"devices": [{
            "id": "dev_365fd956236f46e5",
            "ip": "192.168.100.219",
            "mac": "",
            "first_seen": "2026-07-01T08:00:00-06:00",
            "last_seen_epoch": 100,
            "source": "arp_table",
        }]}
        devices = merge_records([
            {
                "ip": "192.168.100.219",
                "mac": "0e:38:76:1a:e3:ba",
                "source": "dhcp_leases",
                "reachable": False,
            },
        ], previous, "2026-07-12T22:26:48-06:00", 1000, config)

        signals = build_inventory_signals({"devices": devices, "services": []})

        self.assertEqual(len(devices), 1)
        self.assertEqual(len(signals), 1)
        self.assertEqual(signals[0]["device_id"], devices[0]["id"])

    def test_current_weak_reconciled_to_retained_strong_cannot_duplicate_signal(self):
        config = {"HIOC_INVENTORY_STALE_AFTER_SEC": "60", "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120"}
        previous = {"devices": [{
            "id": "dev_4e3690158b11961e",
            "ip": "192.168.100.219",
            "mac": "0e:38:76:1a:e3:ba",
            "first_seen": "2026-07-01T08:00:00-06:00",
            "source": "arp_table",
        }]}
        devices = merge_records([{
            "ip": "192.168.100.219",
            "source": "arp_table",
            "last_seen_source": "arp_table",
        }], previous, "2026-07-12T23:21:19-06:00", 1000, config)
        devices[0].update({
            "health_status": "degraded",
            "health_score": 40,
            "health_reasons": ["test degraded canonical identity"],
        })

        signals = build_inventory_signals({"devices": devices, "services": []})

        self.assertEqual(len(devices), 1)
        self.assertEqual(len(signals), 1)
        self.assertEqual(signals[0]["device_id"], "dev_4e3690158b11961e")

    def test_anonymous_failed_neighbor_produces_no_inventory_signal(self):
        config = {"HIOC_INVENTORY_STALE_AFTER_SEC": "60", "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "120"}
        with patch("hioc.inventory.run_command", return_value=(0, "192.168.100.138 dev eth0 FAILED", "")):
            current = list(neighbor_table().values())
        devices = merge_records(current, {"devices": []}, "2026-07-13T10:00:00-06:00", 1000, config)

        self.assertEqual(devices, [])
        self.assertEqual(build_inventory_signals({"devices": devices, "services": []}), [])

    def test_event_signals_are_context_not_standalone_incidents(self):
        signals = build_event_signals([
            {"id": "evt_1", "type": "InventoryChanged", "source": "inventory", "payload": {}}
        ])

        self.assertEqual(correlate(signals, {}), {})

    def test_lifecycle_phase_progression(self):
        self.assertEqual(lifecycle_phase(1, 3), "detected")
        self.assertEqual(lifecycle_phase(2, 3), "confirmed")
        self.assertEqual(lifecycle_phase(3, 3), "active")


if __name__ == "__main__":
    unittest.main()
