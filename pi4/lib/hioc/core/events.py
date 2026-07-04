import hashlib
import json
from pathlib import Path

from .schemas import EVENT_SCHEMA
from .state import StateStore


class EventBus:
    def __init__(self, store: StateStore, source: str, retention: int = 500):
        self.store = store
        self.source = source
        self.retention = retention

    def publish(self, event_type: str, timestamp: str, payload: dict) -> dict:
        basis = json.dumps({"type": event_type, "timestamp": timestamp, "source": self.source, "payload": payload}, sort_keys=True)
        event = {
            "id": "evt_" + hashlib.sha1(basis.encode()).hexdigest()[:16],
            "type": event_type,
            "timestamp": timestamp,
            "source": self.source,
            "payload": payload,
        }
        self.store.append_bounded_json_list("events.json", event, self.retention, EVENT_SCHEMA)
        self.store.write_json("latest_event.json", event, EVENT_SCHEMA)
        return event

    def read_events(self) -> list[dict]:
        events = self.store.read_json("events.json", [])
        return events if isinstance(events, list) else []

