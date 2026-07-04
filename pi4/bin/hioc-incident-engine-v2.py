#!/usr/bin/env python3
import hashlib
import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path

HIOC_HOME = Path(os.environ.get("HIOC_HOME", "/home/jazofv1/hioc"))
PI4_TOOLS_HOME = Path(os.environ.get("PI4_TOOLS_HOME", "/home/jazofv1/pi4-tools"))
CONFIG_FILE = HIOC_HOME / "config" / "hioc.conf"
TOOLKIT_CONFIG = PI4_TOOLS_HOME / "config" / "toolkit.conf"
STATE_DIR = HIOC_HOME / "state" / "incidents"
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
    "HIOC_HISTORY_LIMIT": "100",
    "HIOC_RECOVERY_CONFIRM_CYCLES": "2",
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


def mqtt_pub(topic, payload):
    c = cfg()
    cmd = ["mosquitto_pub", "-h", c.get("MQTT_HOST", "localhost"), "-p", c.get("MQTT_PORT", "1883"), "-t", topic, "-m", payload, "-r"]
    if c.get("MQTT_USER"):
        cmd += ["-u", c.get("MQTT_USER", "")]
    if c.get("MQTT_PASSWORD"):
        cmd += ["-P", c.get("MQTT_PASSWORD", "")]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)


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


def stable_id(key):
    return hashlib.sha1(key.encode()).hexdigest()


def severity_rank(sev):
    return {"critical": 4, "major": 3, "warning": 2, "info": 1}.get(sev, 0)


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


def build_signals(t):
    c = cfg()
    signals = []

    def add(name, system, severity, reason, value, affected):
        signals.append({"name": name, "system": system, "severity": severity, "reason": reason, "value": value, "affected": affected})

    if t["gateway_status"] != "online":
        add("gateway_offline", "Gateway", "critical", "Gateway is unreachable from the Pi4 probe", t["gateway_status"], ["Gateway", "LAN", "Internet", "DNS", "MQTT", "Home Assistant"])
    elif t["gateway_latency_ms"] >= num(c["HIOC_MAJOR_GATEWAY_LATENCY_MS"]):
        add("gateway_latency", "Gateway", "major", f"Gateway latency is {t['gateway_latency_ms']} ms", f"{t['gateway_latency_ms']} ms", ["Gateway", "LAN", "DNS"])
    elif t["gateway_latency_ms"] >= num(c["HIOC_WARN_GATEWAY_LATENCY_MS"]):
        add("gateway_latency", "Gateway", "warning", f"Gateway latency is {t['gateway_latency_ms']} ms", f"{t['gateway_latency_ms']} ms", ["Gateway", "LAN"])

    if t["packet_loss_percent"] >= num(c["HIOC_MAJOR_PACKET_LOSS_PERCENT"]):
        add("packet_loss", "Internet", "major", f"Packet loss is {t['packet_loss_percent']}%", f"{t['packet_loss_percent']}%", ["Internet", "DNS", "MQTT", "Cloud services"])
    elif t["packet_loss_percent"] >= num(c["HIOC_WARN_PACKET_LOSS_PERCENT"]):
        add("packet_loss", "Internet", "warning", f"Packet loss is {t['packet_loss_percent']}%", f"{t['packet_loss_percent']}%", ["Internet"])

    if t["internet_latency_ms"] >= num(c["HIOC_MAJOR_INTERNET_LATENCY_MS"]):
        add("internet_latency", "Internet", "major", f"Average internet latency is {t['internet_latency_ms']} ms", f"{t['internet_latency_ms']} ms", ["Internet", "Cloud services"])
    elif t["internet_latency_ms"] >= num(c["HIOC_WARN_INTERNET_LATENCY_MS"]):
        add("internet_latency", "Internet", "warning", f"Average internet latency is {t['internet_latency_ms']} ms", f"{t['internet_latency_ms']} ms", ["Internet"])

    if t["internet_health"] == "critical":
        add("internet_health", "Internet", "critical", "Probe reports internet health as critical", t["internet_health"], ["Internet", "DNS", "MQTT"])
    elif t["internet_health"] == "degraded":
        add("internet_health", "Internet", "warning", "Probe reports internet health as degraded", t["internet_health"], ["Internet"])

    if t["dns_latency_ms"] >= num(c["HIOC_MAJOR_DNS_LATENCY_MS"]):
        add("dns_latency", "DNS", "major", f"Local DNS latency is {t['dns_latency_ms']} ms", f"{t['dns_latency_ms']} ms", ["DNS", "Pi-hole", "Internet"])
    elif t["dns_latency_ms"] >= num(c["HIOC_WARN_DNS_LATENCY_MS"]):
        add("dns_latency", "DNS", "warning", f"Local DNS latency is {t['dns_latency_ms']} ms", f"{t['dns_latency_ms']} ms", ["DNS", "Pi-hole"])

    if t["mqtt_publish_ms"] >= num(c["HIOC_MAJOR_MQTT_PUBLISH_MS"]):
        add("mqtt_publish", "MQTT", "major", f"MQTT publish duration is {t['mqtt_publish_ms']} ms", f"{t['mqtt_publish_ms']} ms", ["MQTT", "Telemetry", "Home Assistant"])
    elif t["mqtt_publish_ms"] >= num(c["HIOC_WARN_MQTT_PUBLISH_MS"]):
        add("mqtt_publish", "MQTT", "warning", f"MQTT publish duration is {t['mqtt_publish_ms']} ms", f"{t['mqtt_publish_ms']} ms", ["MQTT", "Telemetry"])

    if t["pi5_status"] != "online":
        add("pi5_offline", "Pi5", "critical", "Pi5 / Home Assistant host is unreachable from Pi4", t["pi5_status"], ["Home Assistant", "Dashboard", "Automations"])

    if t["pi4_temperature_c"] >= num(c["HIOC_MAJOR_PI4_TEMP_C"]):
        add("pi4_temperature", "Pi4", "major", f"Pi4 temperature is {t['pi4_temperature_c']}C", f"{t['pi4_temperature_c']}C", ["Pi4", "Pi-hole", "NUT", "Probe"])
    elif t["pi4_temperature_c"] >= num(c["HIOC_WARN_PI4_TEMP_C"]):
        add("pi4_temperature", "Pi4", "warning", f"Pi4 temperature is {t['pi4_temperature_c']}C", f"{t['pi4_temperature_c']}C", ["Pi4"])

    return signals


def correlate(signals, t):
    if not signals:
        return None
    names = {s["name"] for s in signals}
    systems = {s["system"] for s in signals}
    severity = max((s["severity"] for s in signals), key=severity_rank)
    affected = sorted(set(a for s in signals for a in s["affected"]))
    evidence = [f"{s['system']}: {s['reason']}" for s in signals]

    gateway_healthy = t["gateway_status"] == "online" and t["gateway_latency_ms"] < num(cfg()["HIOC_WARN_GATEWAY_LATENCY_MS"])

    if "gateway_offline" in names or "gateway_latency" in names:
        key = "network_path_degradation"
        title = "Network path degradation"
        system = "Gateway"
        root = "Local gateway or LAN path"
        confidence = 92
        recommendation = "Check Huawei gateway, Orbi AP path, cabling, and local network load."
    elif {"packet_loss", "internet_latency"} & names and gateway_healthy:
        key = "internet_degradation_isp_likely"
        title = "Internet degradation"
        system = "Internet"
        root = "ISP or upstream routing"
        confidence = 94 if "packet_loss" in names else 88
        recommendation = "Gateway is healthy. Monitor ISP path, compare external targets, and run a speed test if it persists."
    elif "dns_latency" in names and not ({"packet_loss", "internet_latency"} & names):
        key = "dns_degradation"
        title = "DNS degradation"
        system = "DNS"
        root = "Pi-hole, upstream DNS, or resolver latency"
        confidence = 86
        recommendation = "Check Pi-hole FTL, upstream resolver, and Pi4 resource load."
    elif "mqtt_publish" in names and len(names) == 1:
        key = "mqtt_degradation"
        title = "MQTT telemetry degradation"
        system = "MQTT"
        root = "MQTT broker or Home Assistant host load"
        confidence = 82
        recommendation = "Check Mosquitto broker status, HA host CPU/memory, and MQTT client load."
    elif "pi5_offline" in names:
        key = "home_assistant_host_unreachable"
        title = "Home Assistant host unreachable"
        system = "Pi5"
        root = "Pi5 power, network, or HA host failure"
        confidence = 95
        recommendation = "Check Pi5 power, network link, and Home Assistant host status."
    elif "pi4_temperature" in names:
        key = "pi4_thermal_degradation"
        title = "Pi4 thermal warning"
        system = "Pi4"
        root = "Pi4 thermal headroom reduced"
        confidence = 90
        recommendation = "Check Pi4 cooling, case airflow, and CPU load."
    else:
        key = "infrastructure_degradation"
        title = "Infrastructure degradation"
        system = sorted(systems)[0]
        root = "Multiple infrastructure signals"
        confidence = 75
        recommendation = "Review the evidence list and open Diagnostics for the affected subsystem."

    return {
        "id": stable_id(key),
        "key": key,
        "status": "active",
        "phase": "active",
        "severity": severity,
        "system": system,
        "title": title,
        "root_cause": root,
        "confidence_percent": confidence,
        "reason": "; ".join(evidence),
        "impact": f"Affected systems: {', '.join(affected)}",
        "affected": affected,
        "recommendation": recommendation,
        "current_value": signals[0]["value"],
        "evidence": evidence,
        "telemetry": t,
    }


def publish_all(base):
    for topic, path in {
        f"{base}/incidents/active": ACTIVE_FILE,
        f"{base}/incidents/history": HISTORY_FILE,
        f"{base}/incidents/summary": SUMMARY_FILE,
        f"{base}/timeline/history": TIMELINE_FILE,
        f"{base}/timeline/latest": LATEST_EVENT_FILE,
        f"{base}/status/detail": STATUS_FILE,
    }.items():
        if path.exists():
            mqtt_pub(topic, path.read_text())
    mqtt_pub(f"{base}/status", "online")


def main():
    c = cfg()
    base = c.get("HIOC_BASE_TOPIC", "home/infrastructure/hioc")
    limit = int(c.get("HIOC_HISTORY_LIMIT", "100"))
    recovery_cycles = int(c.get("HIOC_RECOVERY_CONFIRM_CYCLES", "2"))
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    t = read_telemetry()
    signals = build_signals(t)
    candidate = correlate(signals, t)
    active = load_json(ACTIVE_FILE, {"status": "none"})
    history = load_json(HISTORY_FILE, [])
    timestamp = now_iso()

    if candidate:
        candidate.update({"started": active.get("started", timestamp) if active.get("key") == candidate["key"] and active.get("status") == "active" else timestamp,
                          "updated": timestamp,
                          "started_epoch": active.get("started_epoch", int(time.time())) if active.get("key") == candidate["key"] and active.get("status") == "active" else int(time.time()),
                          "updated_epoch": int(time.time()),
                          "occurrences": active.get("occurrences", 0) + 1 if active.get("key") == candidate["key"] and active.get("status") == "active" else 1,
                          "recovery_confirmations": 0})
        if not (active.get("status") == "active" and active.get("key") == candidate["key"]):
            if active.get("status") == "active":
                active["status"] = "superseded"
                active["phase"] = "archived"
                active["resolved"] = timestamp
                active["duration_seconds"] = int(time.time()) - int(active.get("started_epoch", int(time.time())))
                history = [active] + history
            add_timeline({"timestamp": timestamp, "severity": candidate["severity"], "system": candidate["system"], "title": candidate["title"], "message": candidate["reason"], "incident_id": candidate["id"], "root_cause": candidate["root_cause"], "confidence_percent": candidate["confidence_percent"]})
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
                active["duration_seconds"] = int(time.time()) - int(active.get("started_epoch", int(time.time())))
                history = [active] + history
                add_timeline({"timestamp": timestamp, "severity": "info", "system": active.get("system", "HIOC"), "title": "Incident resolved", "message": f"{active.get('title', 'Incident')} recovered after {active['duration_seconds']}s", "incident_id": active.get("id", ""), "root_cause": active.get("root_cause", "unknown"), "confidence_percent": active.get("confidence_percent", 0)})
                active = {"status": "none", "phase": "idle", "severity": "info", "system": "HIOC", "title": "No active incident", "summary": "All monitored systems are within thresholds", "updated": timestamp, "telemetry": t}
            save_json(ACTIVE_FILE, active)
        else:
            save_json(ACTIVE_FILE, {"status": "none", "phase": "idle", "severity": "info", "system": "HIOC", "title": "No active incident", "summary": "All monitored systems are within thresholds", "updated": timestamp, "telemetry": t})

    history = history[:limit]
    save_json(HISTORY_FILE, history)
    current = load_json(ACTIVE_FILE, {})
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
    }
    save_json(SUMMARY_FILE, summary)
    save_json(STATUS_FILE, {"status": "online", "version": "1.2.0", "updated": timestamp})
    publish_all(base)


if __name__ == "__main__":
    main()
