import hashlib
from typing import Optional


def capability_id(device_id: str, capability: str) -> str:
    return "cap_" + hashlib.sha1(f"{device_id}:{capability}".encode()).hexdigest()[:16]


class CapabilityRegistry:
    def __init__(self):
        self._items = {}

    def add(self, device_id: str, capability: str, source: str, status: str = "present", metadata: Optional[dict] = None) -> None:
        item = {
            "id": capability_id(device_id, capability),
            "device_id": device_id,
            "capability": capability,
            "source": source,
            "status": status,
            "metadata": metadata or {},
        }
        self._items[item["id"]] = item

    def infer_from_device(self, device: dict) -> None:
        role_map = {
            "gateway": "Gateway",
            "collector": "Collector",
            "dns": "DNS",
            "dhcp": "DHCP",
            "home_assistant": "Home Assistant",
            "wireless_infrastructure": "Wireless Infrastructure",
            "switch": "Switch",
            "linux_host": "Linux Host",
        }
        for role in device.get("roles", []):
            capability = role_map.get(role)
            if capability:
                self.add(device["id"], capability, "role")
        firmware = device.get("firmware")
        if isinstance(firmware, dict) and firmware:
            self.add(device["id"], "Firmware", "inventory", metadata=firmware)

    def infer_from_service(self, service: dict) -> None:
        service_map = {
            "mqtt": "MQTT",
            "dns": "DNS",
            "dhcp": "DHCP",
            "ups": "UPS",
            "ssh": "SSH",
            "scheduler": "Scheduler",
        }
        capability = service_map.get(service.get("type"))
        if capability and service.get("device_id"):
            self.add(service["device_id"], capability, service.get("source", "service"), service.get("status", "present"), {"service_id": service.get("id")})

    def all(self) -> list[dict]:
        return sorted(self._items.values(), key=lambda item: (item["device_id"], item["capability"]))
