#!/usr/bin/env python3
import sys
from pathlib import Path

HIOC_HOME = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(HIOC_HOME / "pi4" / "lib"))

from hioc.config import load_config
from hioc.core.events import EventBus
from hioc.core.schemas import INVENTORY_SCHEMA, INVENTORY_SUMMARY_SCHEMA
from hioc.core.state import StateStore
from hioc.inventory import discover_inventory
from hioc.mqtt import MqttClient
from hioc.runtime import load_json, save_json, setup_logger, now_iso


def main() -> int:
    config = load_config()
    home = Path(config.get("HIOC_HOME", str(HIOC_HOME)))
    state_dir = home / "state" / "inventory"
    log = setup_logger(home / "logs", "hioc-inventory-engine")
    inventory_file = state_dir / "inventory.json"
    devices_file = state_dir / "devices.json"
    services_file = state_dir / "services.json"
    topology_file = state_dir / "topology.json"
    dependencies_file = state_dir / "dependencies.json"
    summary_file = state_dir / "summary.json"
    status_file = state_dir / "status.json"
    event_store = StateStore(home / "state" / "events")
    event_bus = EventBus(event_store, "inventory", int(config.get("HIOC_EVENT_RETENTION", "500")))
    previous = load_json(inventory_file, {"devices": []})
    try:
        inventory = discover_inventory(config, previous)
        store = StateStore(state_dir)
        capabilities = inventory.pop("_capabilities", [])
        store.write_json("inventory.json", inventory, INVENTORY_SCHEMA)
        store.write_json("devices.json", inventory["devices"])
        store.write_json("services.json", inventory["services"])
        store.write_json("capabilities.json", capabilities)
        store.write_json("topology.json", inventory["topology"])
        store.write_json("dependencies.json", inventory["dependencies"])
        store.write_json("summary.json", inventory["summary"], INVENTORY_SUMMARY_SCHEMA)
        status = {"status": "online", "updated": now_iso(), "device_count": inventory["summary"]["device_count"], "schema_version": inventory["schema_version"]}
        save_json(status_file, status)
        previous_ids = {device.get("id") for device in previous.get("devices", [])}
        current_ids = {device.get("id") for device in inventory["devices"]}
        for device in inventory["devices"]:
            if device.get("id") not in previous_ids:
                event_bus.publish("DeviceDiscovered", inventory["updated"], {"device_id": device["id"], "display_name": device.get("display_name", ""), "ip": device.get("ip", ""), "mac": device.get("mac", "")})
        if current_ids != previous_ids or inventory["summary"] != previous.get("summary"):
            event_bus.publish("InventoryChanged", inventory["updated"], {"device_count": inventory["summary"]["device_count"], "service_count": inventory["summary"]["service_count"], "capability_count": len(capabilities)})
        if inventory["topology"] != previous.get("topology"):
            event_bus.publish("TopologyChanged", inventory["updated"], {"topology_edges": inventory["summary"]["topology_edges"]})
        base = config.get("HIOC_BASE_TOPIC", "home/infrastructure/hioc")
        payloads = {
            f"{base}/inventory": inventory,
            f"{base}/inventory/devices": inventory["devices"],
            f"{base}/inventory/services": inventory["services"],
            f"{base}/inventory/topology": inventory["topology"],
            f"{base}/inventory/dependencies": inventory["dependencies"],
            f"{base}/inventory/summary": inventory["summary"],
            f"{base}/inventory/status": status,
        }
        try:
            with MqttClient(config) as mqtt:
                for topic, payload in payloads.items():
                    mqtt.publish(topic, payload)
        except Exception as exc:
            log.error("inventory discovered but MQTT publish failed: %s", exc)
            status["status"] = "degraded"
            status["publish_errors"] = [str(exc)]
            save_json(status_file, status)
            return 0
        log.info("inventory updated devices=%s services=%s", inventory["summary"]["device_count"], inventory["summary"]["service_count"])
        return 0
    except Exception as exc:
        log.exception("inventory engine failed")
        save_json(status_file, {"status": "error", "updated": now_iso(), "error": str(exc)})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
