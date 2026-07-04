#!/usr/bin/env python3
import csv
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

HIOC_HOME = Path(os.environ.get("HIOC_HOME", "/home/jazofv1/hioc"))
CONFIG_FILE = HIOC_HOME / "config" / "hioc.conf"
TOOLKIT_CONFIG = Path(os.environ.get("PI4_TOOLKIT_CONFIG", "/home/jazofv1/pi4-tools/config/toolkit.conf"))
STATE_DIR = HIOC_HOME / "state"
HISTORY_DIR = HIOC_HOME / "history"
LOG_DIR = HIOC_HOME / "logs"
FORECAST_FILE = STATE_DIR / "forecast.json"
STATS_FILE = STATE_DIR / "statistics.json"
STATUS_FILE = STATE_DIR / "history_status.json"

DEFAULTS = {
    "HIOC_BASE_TOPIC": "home/infrastructure/hioc",
    "HIOC_LEGACY_BASE_TOPIC": "home/infrastructure/pi4",
    "HIOC_HISTORY_RETENTION_DAYS": "365",
}


def read_shell_config(path: Path) -> dict:
    data = {}
    if not path.exists():
        return data
    for raw in path.read_text(errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def cfg() -> dict:
    out = dict(DEFAULTS)
    out.update(read_shell_config(TOOLKIT_CONFIG))
    out.update(read_shell_config(CONFIG_FILE))
    return out


def run(cmd, timeout=5):
    try:
        return subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL, timeout=timeout).strip()
    except Exception:
        return ""


def mqtt_read(topic: str, fallback="unknown"):
    c = cfg()
    cmd = [
        "timeout", "4", "mosquitto_sub",
        "-h", c.get("MQTT_HOST", "localhost"),
        "-p", c.get("MQTT_PORT", "1883"),
        "-C", "1",
        "-t", topic,
    ]
    if c.get("MQTT_USER"):
        cmd.extend(["-u", c.get("MQTT_USER", "")])
    if c.get("MQTT_PASSWORD"):
        cmd.extend(["-P", c.get("MQTT_PASSWORD", "")])
    value = run(cmd, timeout=6)
    return value if value != "" else fallback


def mqtt_pub(topic: str, payload: str):
    c = cfg()
    cmd = [
        "mosquitto_pub",
        "-h", c.get("MQTT_HOST", "localhost"),
        "-p", c.get("MQTT_PORT", "1883"),
        "-t", topic,
        "-m", payload,
        "-r",
    ]
    if c.get("MQTT_USER"):
        cmd.extend(["-u", c.get("MQTT_USER", "")])
    if c.get("MQTT_PASSWORD"):
        cmd.extend(["-P", c.get("MQTT_PASSWORD", "")])
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)


def num(value, default=0.0):
    try:
        return float(str(value).strip())
    except Exception:
        return default


def append_csv(name: str, row: dict):
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    path = HISTORY_DIR / f"{name}.csv"
    exists = path.exists()
    with path.open("a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()))
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def read_csv(name: str, limit=2016):
    path = HISTORY_DIR / f"{name}.csv"
    if not path.exists():
        return []
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    return rows[-limit:]


def avg(values):
    vals = [num(v) for v in values if str(v) not in ("", "unknown", "unavailable")]
    return round(sum(vals) / len(vals), 3) if vals else 0


def slope_per_day(rows, field):
    if len(rows) < 2:
        return 0
    first = num(rows[0].get(field))
    last = num(rows[-1].get(field))
    try:
        t0 = datetime.fromisoformat(rows[0]["timestamp"])
        t1 = datetime.fromisoformat(rows[-1]["timestamp"])
        days = max((t1 - t0).total_seconds() / 86400, 1 / 288)
        return round((last - first) / days, 4)
    except Exception:
        return 0


def trend_label(slope, deadband):
    if slope > deadband:
        return "rising"
    if slope < -deadband:
        return "falling"
    return "stable"


def main():
    c = cfg()
    base = c.get("HIOC_BASE_TOPIC", "home/infrastructure/hioc")
    legacy = c.get("HIOC_LEGACY_BASE_TOPIC", c.get("MQTT_BASE_TOPIC", "home/infrastructure/pi4"))
    now = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")

    STATE_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    network = {
        "timestamp": now,
        "internet_latency_ms": num(mqtt_read(f"{legacy}/network/average_internet_latency_ms", 0)),
        "packet_loss_percent": num(mqtt_read(f"{legacy}/network/average_packet_loss_percent", 0)),
        "jitter_ms": num(mqtt_read(f"{legacy}/network/internet_jitter_ms", 0)),
        "gateway_latency_ms": num(mqtt_read(f"{legacy}/network/gateway_latency_ms", 0)),
        "dns_latency_ms": num(mqtt_read(f"{legacy}/network/dns_latency_local_ms", 0)),
        "mqtt_publish_ms": num(mqtt_read(f"{legacy}/network/mqtt_publish_duration_ms", 0)),
    }
    append_csv("network", network)

    # Local host metrics
    temp_raw = run(["vcgencmd", "measure_temp"])
    pi4_temp = num(temp_raw.replace("temp=", "").replace("'C", ""), 0)
    disk_percent = num(run(["bash", "-lc", "df -P / | awk 'NR==2 {gsub(/%/,\"\",$5); print $5}'"]), 0)
    mem_percent = num(run(["bash", "-lc", "free | awk '/Mem:/ {printf \"%.2f\", ($3/$2)*100}'"]), 0)
    host = {
        "timestamp": now,
        "pi4_temp_c": pi4_temp,
        "pi4_disk_percent": disk_percent,
        "pi4_memory_percent": mem_percent,
    }
    append_csv("host", host)

    nrows = read_csv("network")
    hrows = read_csv("host")

    latency_slope = slope_per_day(nrows, "internet_latency_ms")
    loss_slope = slope_per_day(nrows, "packet_loss_percent")
    dns_slope = slope_per_day(nrows, "dns_latency_ms")
    mqtt_slope = slope_per_day(nrows, "mqtt_publish_ms")
    disk_slope = slope_per_day(hrows, "pi4_disk_percent")
    temp_slope = slope_per_day(hrows, "pi4_temp_c")
    mem_slope = slope_per_day(hrows, "pi4_memory_percent")

    days_to_disk_full = None
    if disk_slope > 0:
        days_to_disk_full = max(0, round((90 - host["pi4_disk_percent"]) / disk_slope, 1))

    forecast = {
        "timestamp": now,
        "internet": {
            "current_latency_ms": network["internet_latency_ms"],
            "average_latency_24h_ms": avg([r.get("internet_latency_ms") for r in nrows[-288:]]),
            "average_packet_loss_24h_percent": avg([r.get("packet_loss_percent") for r in nrows[-288:]]),
            "latency_trend": trend_label(latency_slope, 5),
            "latency_change_ms_per_day": latency_slope,
            "packet_loss_trend": trend_label(loss_slope, 0.2),
        },
        "dns": {
            "current_latency_ms": network["dns_latency_ms"],
            "average_latency_24h_ms": avg([r.get("dns_latency_ms") for r in nrows[-288:]]),
            "trend": trend_label(dns_slope, 10),
            "change_ms_per_day": dns_slope,
        },
        "mqtt": {
            "current_publish_ms": network["mqtt_publish_ms"],
            "average_publish_24h_ms": avg([r.get("mqtt_publish_ms") for r in nrows[-288:]]),
            "trend": trend_label(mqtt_slope, 20),
            "change_ms_per_day": mqtt_slope,
        },
        "pi4": {
            "temperature_c": host["pi4_temp_c"],
            "temperature_trend": trend_label(temp_slope, 1),
            "temperature_change_c_per_day": temp_slope,
            "memory_percent": host["pi4_memory_percent"],
            "memory_trend": trend_label(mem_slope, 2),
            "disk_percent": host["pi4_disk_percent"],
            "disk_growth_percent_per_day": disk_slope,
            "estimated_days_to_90_percent": days_to_disk_full,
        },
    }

    statistics = {
        "timestamp": now,
        "samples": {"network": len(nrows), "host": len(hrows)},
        "network_24h": {
            "avg_latency_ms": forecast["internet"]["average_latency_24h_ms"],
            "avg_packet_loss_percent": forecast["internet"]["average_packet_loss_24h_percent"],
            "avg_dns_latency_ms": forecast["dns"]["average_latency_24h_ms"],
            "avg_mqtt_publish_ms": forecast["mqtt"]["average_publish_24h_ms"],
        },
        "host_24h": {
            "avg_pi4_temp_c": avg([r.get("pi4_temp_c") for r in hrows[-288:]]),
            "avg_pi4_memory_percent": avg([r.get("pi4_memory_percent") for r in hrows[-288:]]),
            "avg_pi4_disk_percent": avg([r.get("pi4_disk_percent") for r in hrows[-288:]]),
        },
    }

    FORECAST_FILE.write_text(json.dumps(forecast, indent=2))
    STATS_FILE.write_text(json.dumps(statistics, indent=2))
    STATUS_FILE.write_text(json.dumps({"status": "online", "updated": now}, indent=2))

    mqtt_pub(f"{base}/forecast", json.dumps(forecast))
    mqtt_pub(f"{base}/statistics", json.dumps(statistics))
    mqtt_pub(f"{base}/history/status", json.dumps({"status": "online", "updated": now}))


if __name__ == "__main__":
    main()
