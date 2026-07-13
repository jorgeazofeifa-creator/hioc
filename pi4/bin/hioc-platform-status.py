#!/usr/bin/env python3
import sys
from pathlib import Path

HIOC_HOME = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(HIOC_HOME / "pi4" / "lib"))

from hioc.config import load_config
from hioc.core.state import StateStore
from hioc.core.version import read_version_manifest
from hioc.mqtt import MqttClient
from hioc.runtime import now_iso, setup_logger


def main() -> int:
    config = load_config()
    home = Path(config.get("HIOC_HOME", str(HIOC_HOME)))
    log = setup_logger(home / "logs", "hioc-platform-status")
    store = StateStore(home / "state" / "platform")
    timestamp = now_iso()
    try:
        version = read_version_manifest(home / "VERSION.yaml")
        version_payload = {
            "status": "online",
            "updated": timestamp,
            "versions": version,
        }
        status_payload = {
            "status": "online",
            "updated": timestamp,
            "hioc_version": version["hioc_version"],
            "core": version["core"],
            "correlation_engine": version["correlation_engine"],
            "dashboard": version["dashboard"],
            "schema": version["schema"],
            "mqtt_api": version["mqtt_api"],
            "build": version["build"],
        }
        store.write_json("version.json", version_payload)
        store.write_json("status.json", status_payload)
        base = config.get("HIOC_BASE_TOPIC", "home/infrastructure/hioc")
        try:
            with MqttClient(config, client_id="hioc-platform-status") as mqtt:
                mqtt.publish(f"{base}/platform/version", version_payload)
                mqtt.publish(f"{base}/platform/status", status_payload)
        except Exception as exc:
            status_payload["status"] = "degraded"
            status_payload["publish_error"] = str(exc)
            store.write_json("status.json", status_payload)
            log.error("platform status MQTT publish failed: %s", exc)
            return 0
        log.info(
            "platform status updated hioc_version=%s build=%s",
            version["hioc_version"],
            version["build"],
        )
        return 0
    except Exception as exc:
        store.write_json("status.json", {"status": "error", "updated": timestamp, "error": str(exc)})
        log.exception("platform status failed")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
