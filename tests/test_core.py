import tempfile
import unittest
from pathlib import Path
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "pi4" / "lib"))

from hioc.core.capabilities import CapabilityRegistry
from hioc.core.drivers import DriverRegistry, DriverResult
from hioc.core.events import EventBus
from hioc.core.schemas import EVENT_SCHEMA, SchemaError
from hioc.core.state import StateStore
from hioc.mqtt import MqttClient, MqttPublishError, _encode_remaining_length


class FailingDriver:
    name = "failing"

    def discover(self, config):
        raise RuntimeError("driver failed")


class WorkingDriver:
    name = "working"

    def discover(self, config):
        return DriverResult(name=self.name, devices=[{"id": "dev_1"}])


class FakeSocket:
    def __init__(self, response=b"\x20\x02\x00\x00", fail_on_send=None):
        self.response = response
        self.fail_on_send = fail_on_send
        self.send_count = 0
        self.sent = []
        self.closed = False
        self.timeout = None

    def settimeout(self, timeout):
        self.timeout = timeout

    def sendall(self, packet):
        self.send_count += 1
        if self.send_count == self.fail_on_send:
            raise OSError("socket send failed")
        self.sent.append(packet)

    def recv(self, _size):
        return self.response

    def close(self):
        self.closed = True


def decode_remaining_length(packet):
    value = 0
    multiplier = 1
    index = 1
    encoded = []
    while True:
        byte = packet[index]
        encoded.append(byte)
        index += 1
        value += (byte & 0x7F) * multiplier
        if not byte & 0x80:
            return value, index, bytes(encoded)
        multiplier *= 128


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
        self.assertEqual(results[1].devices, [{"id": "dev_1", "source": "driver:working"}])

    def test_driver_registry_validates_result_shape_and_independent_records(self):
        class ContractDriver:
            name = "future_passive"

            def discover(self, config):
                return DriverResult(
                    name=self.name,
                    devices=({"ip": "192.168.1.10"}, "invalid", {"ip": "192.168.1.11", "source": "integration:test"}),
                )

        registry = DriverRegistry()
        registry.register(ContractDriver())
        result = registry.run({})[0]

        self.assertEqual(result.devices, [
            {"ip": "192.168.1.10", "source": "driver:future_passive"},
            {"ip": "192.168.1.11", "source": "integration:test"},
        ])
        self.assertEqual(result.errors, ["driver device record 1 is not a mapping"])

    def test_driver_registry_rejects_invalid_result_and_record_collection(self):
        class InvalidResultDriver:
            name = "invalid_result"

            def discover(self, config):
                return {"devices": []}

        class InvalidCollectionDriver:
            name = "invalid_collection"

            def discover(self, config):
                return DriverResult(name=self.name, devices={"ip": "192.168.1.10"})

        registry = DriverRegistry()
        registry.register(InvalidResultDriver())
        registry.register(InvalidCollectionDriver())
        invalid_result, invalid_collection = registry.run({})

        self.assertEqual(invalid_result.devices, [])
        self.assertEqual(invalid_result.errors, ["driver returned invalid result"])
        self.assertEqual(invalid_collection.devices, [])
        self.assertEqual(invalid_collection.errors, ["driver device must be a list or tuple"])

    def test_capability_registry_infers_roles_and_services(self):
        registry = CapabilityRegistry()
        registry.infer_from_device({"id": "dev_gateway", "roles": ["gateway"], "firmware": {"os": "Linux"}})
        registry.infer_from_service({"id": "svc_mqtt", "device_id": "dev_gateway", "type": "mqtt", "status": "active"})
        capabilities = {item["capability"] for item in registry.all()}
        self.assertIn("Gateway", capabilities)
        self.assertIn("Firmware", capabilities)
        self.assertIn("MQTT", capabilities)


class MqttClientTests(unittest.TestCase):
    def test_remaining_length_encoding_covers_all_valid_widths(self):
        cases = {
            127: b"\x7f",
            128: b"\x80\x01",
            16_384: b"\x80\x80\x01",
            268_435_455: b"\xff\xff\xff\x7f",
        }
        for value, expected in cases.items():
            with self.subTest(value=value):
                self.assertEqual(_encode_remaining_length(value), expected)

    def test_publish_preserves_topic_payload_and_retain_flag(self):
        sock = FakeSocket()
        client = MqttClient({"MQTT_HOST": "broker"}, client_id="test")
        client.sock = sock
        client.publish("hioc/topic", "payload", retain=True)
        packet = sock.sent[0]
        remaining, body_start, _encoded = decode_remaining_length(packet)

        self.assertEqual(packet[0], 0x31)
        self.assertEqual(remaining, len(packet) - body_start)
        self.assertEqual(packet[body_start:body_start + 12], b"\x00\x0ahioc/topic")
        self.assertEqual(packet[body_start + 12:], b"payload")

        sock.sent.clear()
        client.publish("hioc/topic", "payload", retain=False)
        self.assertEqual(sock.sent[0][0], 0x30)

    def test_publish_serializes_mappings_with_existing_sorted_keys(self):
        sock = FakeSocket()
        client = MqttClient({"MQTT_HOST": "broker"})
        client.sock = sock
        client.publish("topic", {"z": 1, "a": 2})

        self.assertTrue(sock.sent[0].endswith(b'{"a": 2, "z": 1}'))

    def test_large_payload_packets_are_complete_and_use_three_length_bytes(self):
        for size in (131_073, 193_053, 204_800):
            with self.subTest(size=size):
                sock = FakeSocket()
                client = MqttClient({"MQTT_HOST": "broker"})
                client.sock = sock
                payload = "x" * size
                client.publish("home/infrastructure/hioc/incidents/history", payload)
                packet = sock.sent[0]
                remaining, body_start, encoded = decode_remaining_length(packet)

                self.assertEqual(len(encoded), 3)
                self.assertEqual(remaining, len(packet) - body_start)
                self.assertTrue(packet.endswith(payload.encode()))

    def test_connect_failures_and_rejections_propagate(self):
        client = MqttClient({"MQTT_HOST": "broker"})
        with patch("hioc.mqtt.socket.create_connection", side_effect=OSError("unavailable")):
            with self.assertRaisesRegex(OSError, "unavailable"):
                client.connect()

        with patch("hioc.mqtt.socket.create_connection", side_effect=TimeoutError("timed out")):
            with self.assertRaisesRegex(TimeoutError, "timed out"):
                client.connect()

        rejected = FakeSocket(response=b"\x20\x02\x00\x05")
        with patch("hioc.mqtt.socket.create_connection", return_value=rejected):
            with self.assertRaises(MqttPublishError):
                client.connect()

    def test_publish_failure_still_closes_and_clears_socket(self):
        sock = FakeSocket(fail_on_send=2)
        with patch("hioc.mqtt.socket.create_connection", return_value=sock):
            with self.assertRaisesRegex(OSError, "socket send failed"):
                with MqttClient({"MQTT_HOST": "broker"}) as client:
                    client.publish("topic", "payload")

        self.assertTrue(sock.closed)
        self.assertIsNone(client.sock)

    def test_successful_context_disconnects_and_clears_socket(self):
        sock = FakeSocket()
        with patch("hioc.mqtt.socket.create_connection", return_value=sock):
            with MqttClient({"MQTT_HOST": "broker"}) as client:
                client.publish("topic", "payload")

        self.assertTrue(sock.closed)
        self.assertIsNone(client.sock)

    def test_disconnect_send_failure_is_best_effort(self):
        sock = FakeSocket(fail_on_send=1)
        client = MqttClient({"MQTT_HOST": "broker"})
        client.sock = sock
        client.disconnect()

        self.assertTrue(sock.closed)
        self.assertIsNone(client.sock)


if __name__ == "__main__":
    unittest.main()

