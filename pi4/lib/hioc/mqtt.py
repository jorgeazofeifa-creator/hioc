import json
import socket
import struct


class MqttPublishError(RuntimeError):
    pass


def _encode_remaining_length(length: int) -> bytes:
    encoded = bytearray()
    while True:
        byte = length % 128
        length //= 128
        if length > 0:
            byte |= 128
        encoded.append(byte)
        if length == 0:
            return bytes(encoded)


def _field(value: str) -> bytes:
    data = str(value).encode()
    return struct.pack("!H", len(data)) + data


class MqttClient:
    """Minimal MQTT 3.1.1 publisher for retained QoS 0 telemetry."""

    def __init__(self, config: dict, client_id: str = "hioc-inventory-engine"):
        self.config = config
        self.client_id = client_id
        self.sock = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.disconnect()

    def connect(self) -> None:
        host = self.config.get("MQTT_HOST")
        if not host:
            raise MqttPublishError("MQTT_HOST is not configured")
        port = int(self.config.get("MQTT_PORT", "1883"))
        self.sock = socket.create_connection((host, port), timeout=8)
        self.sock.settimeout(8)
        flags = 0x02
        payload = _field(self.client_id)
        user = self.config.get("MQTT_USER")
        password = self.config.get("MQTT_PASSWORD")
        if user:
            flags |= 0x80
            payload += _field(user)
        if password:
            flags |= 0x40
            payload += _field(password)
        variable = _field("MQTT") + bytes([4, flags]) + struct.pack("!H", 60)
        packet = bytes([0x10]) + _encode_remaining_length(len(variable) + len(payload)) + variable + payload
        self.sock.sendall(packet)
        response = self.sock.recv(4)
        if len(response) != 4 or response[0] != 0x20 or response[1] != 0x02 or response[3] != 0x00:
            raise MqttPublishError(f"MQTT connection rejected: {response!r}")

    def publish(self, topic: str, payload, retain: bool = True) -> None:
        if self.sock is None:
            raise MqttPublishError("MQTT client is not connected")
        if isinstance(payload, (dict, list)):
            message = json.dumps(payload, sort_keys=True)
        else:
            message = str(payload)
        variable = _field(topic)
        body = message.encode()
        header = 0x31 if retain else 0x30
        packet = bytes([header]) + _encode_remaining_length(len(variable) + len(body)) + variable + body
        self.sock.sendall(packet)

    def disconnect(self) -> None:
        if self.sock is None:
            return
        try:
            self.sock.sendall(bytes([0xE0, 0x00]))
        except OSError:
            pass
        try:
            self.sock.close()
        finally:
            self.sock = None

