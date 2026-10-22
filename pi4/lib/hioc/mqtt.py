import json
import socket
import struct
import ipaddress
import time
from datetime import datetime, timezone


class MqttPublishError(RuntimeError):
    def __init__(self, message, capability=None):
        self.capability = capability
        super().__init__(message)


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
        response = bytearray()
        while len(response) < 4:
            chunk = self.sock.recv(4 - len(response))
            if not chunk:
                raise ConnectionError("MQTT CONNACK connection closed before completion")
            response.extend(chunk)
        if response[0] != 0x20 or response[1] != 0x02 or response[2] != 0x00 or response[3] != 0x00:
            raise MqttPublishError("MQTT CONNACK does not satisfy the transport contract", "connack")

    def publish(self, topic: str, payload, retain: bool = True) -> None:
        if self.sock is None:
            raise MqttPublishError("MQTT client is not connected", "publish")
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


class BoundedNotificationTransport:
    """Opt-in PE-7 QoS1 single attempt. Existing telemetry methods are unchanged.

    Numeric broker address is required to avoid unbounded DNS at the dispatch
    boundary. PUBACK proves broker acceptance only, not recipient delivery.
    No reconnect, library retry, offline queue, retained notification or new secret.
    """
    deadline_aware = True
    automatic_retries = False
    offline_queue = False

    def __init__(self, config, topic, *, socket_factory=socket.socket,
                 clock=lambda: datetime.now(timezone.utc), monotonic=time.monotonic):
        self.config, self.topic = config, topic
        self.socket_factory, self.clock, self.monotonic = socket_factory, clock, monotonic
        self.address = ipaddress.ip_address(config['MQTT_HOST'])
        if not self.address.is_private or self.address.is_unspecified:
            raise MqttPublishError('PE-7 broker address is not approved', 'bounded')
        if not isinstance(topic, str) or not topic or any(c in topic for c in '+#\x00'):
            raise MqttPublishError('PE-7 notification topic is invalid', 'bounded')

    def send_once(self, event, *, deadline, timeout):
        end = datetime.strptime(deadline, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)
        remaining = min((end-self.clock()).total_seconds(), timeout, 5)
        if remaining <= 0:
            return 'FAILED_NOT_SUBMITTED'
        monotonic_end = self.monotonic() + remaining
        sock, publish_started = None, False
        def budget():
            left = min((end-self.clock()).total_seconds(), monotonic_end-self.monotonic())
            if left <= 0:
                raise TimeoutError()
            sock.settimeout(left)
        def receive(count):
            result = bytearray()
            while len(result) < count:
                budget()
                part = sock.recv(count-len(result))
                if not part:
                    raise ConnectionError()
                result.extend(part)
            return bytes(result)
        try:
            family = socket.AF_INET6 if self.address.version == 6 else socket.AF_INET
            sock = self.socket_factory(family, socket.SOCK_STREAM)
            budget()
            sock.connect((str(self.address), int(self.config['MQTT_PORT'])))
            flags = 0x02
            payload = _field('hioc-pe7-notify-' + event['event_id'][:16])
            if self.config.get('MQTT_USER'):
                flags |= 0x80
                payload += _field(self.config['MQTT_USER'])
            if self.config.get('MQTT_PASSWORD'):
                flags |= 0x40
                payload += _field(self.config['MQTT_PASSWORD'])
            variable = _field('MQTT') + bytes([4, flags]) + struct.pack('!H', 10)
            budget()
            sock.sendall(bytes([0x10]) + _encode_remaining_length(len(variable)+len(payload)) + variable + payload)
            if receive(4) != b'\x20\x02\x00\x00':
                return 'FAILED_NOT_SUBMITTED'
            body = _field(self.topic) + b'\x00\x01' + json.dumps(event, sort_keys=True, separators=(',', ':')).encode('utf-8')
            budget()
            publish_started = True
            sock.sendall(bytes([0x32]) + _encode_remaining_length(len(body)) + body)
            return 'TRANSPORT_ACCEPTED' if receive(4) == b'\x40\x02\x00\x01' else 'DELIVERY_UNKNOWN'
        except Exception:
            return 'DELIVERY_UNKNOWN' if publish_started else 'FAILED_NOT_SUBMITTED'
        finally:
            if sock is not None:
                sock.close()

