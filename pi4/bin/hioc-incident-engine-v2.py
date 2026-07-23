#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

HIOC_HOME = Path(os.environ.get("HIOC_HOME", "/home/jazofv1/hioc"))
PI4_TOOLS_HOME = Path(os.environ.get("PI4_TOOLS_HOME", "/home/jazofv1/pi4-tools"))
sys.path.insert(0, str(HIOC_HOME / "pi4" / "lib"))

from hioc.core.correlation import build_event_signals, build_inventory_signals, build_telemetry_signals, correlate as core_correlate, lifecycle_phase
from hioc.core.events import EventBus
from hioc.core.incident_review import build_history_stats, compact_recent_incidents, enrich_history, recent_incident_reviews
from hioc.core.state import StateStore
from hioc.mqtt import MqttClient

CONFIG_FILE = HIOC_HOME / "config" / "hioc.conf"
TOOLKIT_CONFIG = PI4_TOOLS_HOME / "config" / "toolkit.conf"
STATE_DIR = HIOC_HOME / "state" / "incidents"
INVENTORY_FILE = HIOC_HOME / "state" / "inventory" / "inventory.json"
EVENTS_FILE = HIOC_HOME / "state" / "events" / "events.json"
LOG_DIR = HIOC_HOME / "logs"
ACTIVE_FILE = STATE_DIR / "active.json"
HISTORY_FILE = STATE_DIR / "history.json"
SUMMARY_FILE = STATE_DIR / "summary.json"
TIMELINE_FILE = STATE_DIR / "timeline.json"
LATEST_EVENT_FILE = STATE_DIR / "latest_event.json"
STATUS_FILE = HIOC_HOME / "state" / "incident_engine_status.json"

DEFAULTS = {
    "HIOC_BASE_TOPIC": "home/infrastructure/hioc",
    "HIOC_LEGACY_BASE_TOPIC": "home/infrastructure/pi4",
    "MQTT_HOST": "localhost",
    "MQTT_PORT": "1883",
    "HIOC_HISTORY_LIMIT": "100",
    "HIOC_RECOVERY_CONFIRM_CYCLES": "2",
    "HIOC_INCIDENT_CONFIRM_CYCLES": "3",
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


def now_iso():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def read_shell_config(path: Path):
    out = {}
    if not path.exists():
        return out
    for raw in path.read_text(errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        out[key.strip()] = value.strip().strip('"').strip("'")
    return out


def cfg():
    c = dict(DEFAULTS)
    c.update(read_shell_config(TOOLKIT_CONFIG))
    c.update(read_shell_config(CONFIG_FILE))
    return c


def run(cmd, timeout=4):
    try:
        return subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL, timeout=timeout).strip()
    except Exception:
        return ""


def mqtt_read(topic, fallback="unknown"):
    c = cfg()
    cmd = ["timeout", "4", "mosquitto_sub", "-h", c.get("MQTT_HOST", "localhost"), "-p", c.get("MQTT_PORT", "1883"), "-C", "1", "-t", topic]
    if c.get("MQTT_USER"):
        cmd += ["-u", c.get("MQTT_USER", "")]
    if c.get("MQTT_PASSWORD"):
        cmd += ["-P", c.get("MQTT_PASSWORD", "")]
    value = run(cmd, timeout=5)
    return value if value != "" else fallback


def num(value, default=0.0):
    try:
        return float(str(value).strip())
    except Exception:
        return default


def load_json(path, fallback):
    try:
        if path.exists():
            return json.loads(path.read_text())
    except Exception:
        pass
    return fallback


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))


def add_timeline(event):
    limit = int(cfg().get("HIOC_HISTORY_LIMIT", "100"))
    timeline = load_json(TIMELINE_FILE, [])
    timeline = [event] + timeline
    save_json(TIMELINE_FILE, timeline[:limit])
    save_json(LATEST_EVENT_FILE, event)


def read_telemetry():
    c = cfg()
    legacy = c.get("HIOC_LEGACY_BASE_TOPIC", c.get("MQTT_BASE_TOPIC", "home/infrastructure/pi4"))
    temp_raw = run(["vcgencmd", "measure_temp"])
    return {
        "internet_latency_ms": num(mqtt_read(f"{legacy}/network/average_internet_latency_ms", 0)),
        "packet_loss_percent": num(mqtt_read(f"{legacy}/network/average_packet_loss_percent", 0)),
        "jitter_ms": num(mqtt_read(f"{legacy}/network/internet_jitter_ms", 0)),
        "gateway_latency_ms": num(mqtt_read(f"{legacy}/network/gateway_latency_ms", 0)),
        "dns_latency_ms": num(mqtt_read(f"{legacy}/network/dns_latency_local_ms", 0)),
        "mqtt_publish_ms": num(mqtt_read(f"{legacy}/network/mqtt_publish_duration_ms", 0)),
        "internet_health": mqtt_read(f"{legacy}/network/internet_health", "healthy"),
        "gateway_status": mqtt_read(f"{legacy}/network/gateway_status", "online"),
        "pi5_status": mqtt_read(f"{legacy}/network/pi5_status", "online"),
        "pi4_temperature_c": num(temp_raw.replace("temp=", "").replace("'C", ""), 0),
    }


def load_inventory():
    return load_json(INVENTORY_FILE, {"devices": [], "services": [], "topology": {"edges": []}, "dependencies": {"edges": []}, "summary": {}})


def load_events():
    return load_json(EVENTS_FILE, [])


def publish_event(event_bus, event_type, timestamp, payload):
    try:
        event_bus.publish(event_type, timestamp, payload)
    except Exception:
        pass


def _publication_error(phase, topic, completed, exc, context=""):
    detail = f"{context}: " if context else ""
    return RuntimeError(
        f"phase={phase} topic={topic or 'none'} completed={completed}: "
        f"{type(exc).__name__}: {detail}{exc}"
    )


def publish_all(base, config):
    publication_files = (
        (f"{base}/incidents/active", ACTIVE_FILE),
        (f"{base}/incidents/history", HISTORY_FILE),
        (f"{base}/incidents/summary", SUMMARY_FILE),
        (f"{base}/timeline/history", TIMELINE_FILE),
        (f"{base}/timeline/latest", LATEST_EVENT_FILE),
        (f"{base}/status/detail", STATUS_FILE),
    )
    payloads = []
    for topic, path in publication_files:
        if not path.exists():
            continue
        try:
            payload = path.read_text(encoding="utf-8")
            json.loads(payload)
        except Exception as exc:
            raise _publication_error("preflight", topic, 0, exc, f"path={path}") from exc
        payloads.append((topic, payload))
    payloads.append((f"{base}/status", "online"))

    completed = []
    current_topic = None
    entered = False
    try:
        with MqttClient(config, client_id="hioc-incident-engine") as mqtt:
            entered = True
            for current_topic, payload in payloads:
                try:
                    mqtt.publish(current_topic, payload, retain=True)
                except Exception as exc:
                    raise _publication_error("publish", current_topic, len(completed), exc) from exc
                completed.append(current_topic)
    except RuntimeError as exc:
        if str(exc).startswith("phase=publish "):
            raise
        phase = "cleanup" if entered else "connect"
        raise _publication_error(phase, current_topic, len(completed), exc) from exc
    except Exception as exc:
        phase = "cleanup" if entered else "connect"
        raise _publication_error(phase, current_topic, len(completed), exc) from exc
    return completed


def main():
    c = cfg()
    base = c.get("HIOC_BASE_TOPIC", "home/infrastructure/hioc")
    limit = int(c.get("HIOC_HISTORY_LIMIT", "100"))
    recovery_cycles = int(c.get("HIOC_RECOVERY_CONFIRM_CYCLES", "2"))
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    t = read_telemetry()
    inventory = load_inventory()
    events = load_events()
    signals = []
    signals.extend(build_telemetry_signals(t, c))
    signals.extend(build_inventory_signals(inventory))
    signals.extend(build_event_signals(events))
    candidate = core_correlate(signals, inventory)
    active = load_json(ACTIVE_FILE, {"status": "none"})
    history = load_json(HISTORY_FILE, [])
    timestamp = now_iso()
    event_bus = EventBus(StateStore(HIOC_HOME / "state" / "events"), "incident", int(c.get("HIOC_EVENT_RETENTION", "500")))

    if candidate:
        same_active = active.get("key") == candidate["key"] and active.get("status") == "active"
        occurrences = active.get("occurrences", 0) + 1 if same_active else 1
        phase = lifecycle_phase(occurrences, int(c.get("HIOC_INCIDENT_CONFIRM_CYCLES", "3")))
        candidate.update({"started": active.get("started", timestamp) if same_active else timestamp,
                          "updated": timestamp,
                          "started_epoch": active.get("started_epoch", int(time.time())) if same_active else int(time.time()),
                          "updated_epoch": int(time.time()),
                          "occurrences": occurrences,
                          "phase": phase,
                          "lifecycle": phase,
                          "recovery_confirmations": 0,
                          "telemetry": t})
        if not (active.get("status") == "active" and active.get("key") == candidate["key"]):
            if active.get("status") == "active":
                active["status"] = "superseded"
                active["phase"] = "archived"
                active["resolved"] = timestamp
                active["duration_seconds"] = int(time.time()) - int(active.get("started_epoch", int(time.time())))
                active["end_time"] = timestamp
                history = [active] + history
                publish_event(event_bus, "IncidentSuperseded", timestamp, {"incident_id": active.get("id", ""), "root_cause": active.get("root_cause", ""), "duration_seconds": active.get("duration_seconds", 0)})
            add_timeline({"timestamp": timestamp, "severity": candidate["severity"], "system": candidate["system"], "title": candidate["title"], "message": candidate["reason"], "incident_id": candidate["id"], "root_cause": candidate["root_cause"], "confidence_percent": candidate["confidence_percent"]})
            publish_event(event_bus, "IncidentDetected", timestamp, {"incident_id": candidate["id"], "root_cause": candidate["root_cause"], "confidence_percent": candidate["confidence_percent"], "affected": candidate.get("affected", [])})
        elif active.get("phase") != phase:
            publish_event(event_bus, "IncidentLifecycleChanged", timestamp, {"incident_id": candidate["id"], "phase": phase, "root_cause": candidate["root_cause"]})
        save_json(ACTIVE_FILE, candidate)
    else:
        if active.get("status") == "active":
            confirmations = int(active.get("recovery_confirmations", 0)) + 1
            active["recovery_confirmations"] = confirmations
            active["phase"] = "recovering"
            active["updated"] = timestamp
            if confirmations >= recovery_cycles:
                active["status"] = "resolved"
                active["phase"] = "resolved"
                active["resolved"] = timestamp
                active["end_time"] = timestamp
                active["duration_seconds"] = int(time.time()) - int(active.get("started_epoch", int(time.time())))
                history = [active] + history
                add_timeline({"timestamp": timestamp, "severity": "info", "system": active.get("system", "HIOC"), "title": "Incident resolved", "message": f"{active.get('title', 'Incident')} recovered after {active['duration_seconds']}s", "incident_id": active.get("id", ""), "root_cause": active.get("root_cause", "unknown"), "confidence_percent": active.get("confidence_percent", 0)})
                publish_event(event_bus, "IncidentResolved", timestamp, {"incident_id": active.get("id", ""), "root_cause": active.get("root_cause", "unknown"), "confidence_percent": active.get("confidence_percent", 0), "duration_seconds": active.get("duration_seconds", 0), "affected": active.get("affected", [])})
                active = {"status": "none", "phase": "idle", "severity": "info", "system": "HIOC", "title": "No active incident", "summary": "All monitored systems are within thresholds", "updated": timestamp, "telemetry": t}
            save_json(ACTIVE_FILE, active)
        else:
            save_json(ACTIVE_FILE, {"status": "none", "phase": "idle", "severity": "info", "system": "HIOC", "title": "No active incident", "summary": "All monitored systems are within thresholds", "updated": timestamp, "telemetry": t})

    timeline = load_json(TIMELINE_FILE, [])
    history = enrich_history(history[:limit], timeline)
    save_json(HISTORY_FILE, history)
    current = load_json(ACTIVE_FILE, {})
    history_stats = build_history_stats(history)
    recent_incidents = compact_recent_incidents(history)
    recent_reviews = recent_incident_reviews(history)
    latest_review = history[0].get("review", {}) if history else {}
    summary = {
        "updated": timestamp,
        "engine_version": "1.2.0",
        "active_status": current.get("status", "none"),
        "active_phase": current.get("phase", "idle"),
        "active_title": current.get("title", "No active incident"),
        "active_severity": current.get("severity", "info"),
        "active_system": current.get("system", "HIOC"),
        "root_cause": current.get("root_cause", "none"),
        "confidence_percent": current.get("confidence_percent", 0),
        "history_count": len(history),
        "signals_detected": len(signals),
        "correlation_engine": "2.0.0",
        "events_consumed": len(events),
        "history_stats": history_stats,
        "recent_incidents": recent_incidents,
        "recent_incident_reviews": recent_reviews,
        "latest_incident_review": latest_review,
    }
    save_json(SUMMARY_FILE, summary)
    save_json(STATUS_FILE, {"status": "online", "version": "1.2.0", "updated": timestamp})
    try:
        publish_all(base, c)
    except Exception as exc:
        print(f"incident MQTT publication failed {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
