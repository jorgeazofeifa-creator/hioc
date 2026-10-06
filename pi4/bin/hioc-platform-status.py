#!/usr/bin/env python3
import sys
from pathlib import Path

HIOC_HOME = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(HIOC_HOME / "pi4" / "lib"))

from hioc.core.compatibility import refresh_status, summary_fields, python_observation, summarize, mqtt_observation
from hioc.config import load_config
from hioc.core.state import StateStore
from hioc.core.version import read_version_manifest
from hioc.mqtt import MqttClient
from hioc.runtime import now_iso, setup_logger


def compatibility_status(store, home, observations, timestamp, log):
    try:
        return refresh_status(store, home, observations, timestamp, HIOC_HOME)
    except Exception:
        payload = summarize([], timestamp)
        payload['summary'] = "Compatibility registry or state unavailable; no update cause established."
        log.warning("%s", payload['summary'])
        # Preserve last-known-good authoritative state on framework failure.
        return payload


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
        compatibility = compatibility_status(store, home, {"system_python": python_observation(
            ".".join(map(str, sys.version_info[:3])), sys.implementation.name.replace("cpython", "CPython"))}, timestamp, log)
        status_payload["compatibility"] = summary_fields(compatibility)
        for entry in compatibility["dependencies"]:
            if entry["status"] in {"INCOMPATIBLE", "TRUST_ANCHOR_CHANGED", "DEPENDENCY_UNAVAILABLE", "COMPATIBILITY_DEGRADED"}:
                log.warning("%s", entry["diagnostic"])
        store.write_json("version.json", version_payload)
        store.write_json("status.json", status_payload)
        base = config.get("HIOC_BASE_TOPIC", "home/infrastructure/hioc")
        try:
            with MqttClient(config, client_id="hioc-platform-status") as mqtt:
                # A successful local QoS 0 write proves publication capability,
                # not broker delivery. Do not record success before that write.
                mqtt.publish(f"{base}/platform/version", version_payload)
                compatibility = compatibility_status(store, home, {"mqtt_transport": mqtt_observation()}, timestamp, log)
                status_payload["compatibility"] = summary_fields(compatibility)
                mqtt.publish(f"{base}/platform/compatibility", compatibility)
                mqtt.publish(f"{base}/platform/status", status_payload)
        except Exception as exc:
            status_payload["status"] = "degraded"
            status_payload["publish_error"] = "MQTT publication unavailable; see compatibility status"
            compatibility = compatibility_status(store, home, {"mqtt_transport": mqtt_observation(exc)}, timestamp, log)
            status_payload["compatibility"] = summary_fields(compatibility)
            store.write_json("status.json", status_payload)
            log.error("%s", next((e["diagnostic"] for e in compatibility["dependencies"] if e["dependency_id"] == "mqtt_transport"), "MQTT publication unavailable; compatibility evidence could not be persisted."))
            return 0
        store.write_json("status.json", status_payload)
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
