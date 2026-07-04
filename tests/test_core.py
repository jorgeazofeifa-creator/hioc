import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "pi4" / "lib"))

from hioc.core.capabilities import CapabilityRegistry
from hioc.core.drivers import DriverRegistry, DriverResult
from hioc.core.events import EventBus
from hioc.core.schemas import EVENT_SCHEMA, SchemaError
from hioc.core.state import StateStore


class FailingDriver:
    name = "failing"

    def discover(self, config):
        raise RuntimeError("driver failed")


class WorkingDriver:
    name = "working"

    def discover(self, config):
        return DriverResult(name=self.name, devices=[{"id": "dev_1"}])


class CoreTests(unittest.TestCase):
    def test_schema_rejects_missing_required_fields(self):
        with self.assertRaises(SchemaError):
            EVENT_SCHEMA.validate({"id": "evt_1"})

    def test_state_store_writes_and_reads_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = StateStore(Path(tmp))
            store.write_json("state.json", {"status": "online"})
            self.assertEqual(store.read_json("state.json", {}), {"status": "online"})

    def test_event_bus_retains_latest_bounded_events(self):
        with tempfile.TemporaryDirectory() as tmp:
            bus = EventBus(StateStore(Path(tmp)), "test", retention=2)
            bus.publish("DeviceDiscovered", "2026-01-01T00:00:00+00:00", {"device_id": "one"})
            latest = bus.publish("InventoryChanged", "2026-01-01T00:01:00+00:00", {"device_count": 1})
            bus.publish("TopologyChanged", "2026-01-01T00:02:00+00:00", {"topology_edges": 1})
            events = bus.read_events()
            self.assertEqual(len(events), 2)
            self.assertEqual(events[1]["id"], latest["id"])

    def test_driver_registry_isolates_driver_failures(self):
        registry = DriverRegistry()
        registry.register(FailingDriver())
        registry.register(WorkingDriver())
        results = registry.run({})
        self.assertEqual(results[0].errors, ["driver failed"])
        self.assertEqual(results[1].devices, [{"id": "dev_1"}])

    def test_capability_registry_infers_roles_and_services(self):
        registry = CapabilityRegistry()
        registry.infer_from_device({"id": "dev_gateway", "roles": ["gateway"], "firmware": {"os": "Linux"}})
        registry.infer_from_service({"id": "svc_mqtt", "device_id": "dev_gateway", "type": "mqtt", "status": "active"})
        capabilities = {item["capability"] for item in registry.all()}
        self.assertIn("Gateway", capabilities)
        self.assertIn("Firmware", capabilities)
        self.assertIn("MQTT", capabilities)


if __name__ == "__main__":
    unittest.main()

