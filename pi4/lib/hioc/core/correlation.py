import hashlib

from .monitoring import is_operationally_monitored


def stable_id(key: str) -> str:
    return hashlib.sha1(key.encode()).hexdigest()


def severity_rank(severity: str) -> int:
    return {"critical": 4, "major": 3, "warning": 2, "info": 1}.get(severity, 0)


def num(value, default=0.0):
    try:
        return float(str(value).strip())
    except Exception:
        return default


def build_telemetry_signals(telemetry: dict, config: dict) -> list[dict]:
    signals = []

    def add(name, system, severity, reason, value, affected, root_hint="", confidence=75):
        signals.append({
            "name": name,
            "system": system,
            "severity": severity,
            "reason": reason,
            "value": value,
            "affected": affected,
            "root_hint": root_hint or system,
            "confidence": confidence,
            "source": "telemetry",
        })

    gateway_status = telemetry.get("gateway_status", "online")
    gateway_latency = num(telemetry.get("gateway_latency_ms"))
    packet_loss = num(telemetry.get("packet_loss_percent"))
    internet_latency = num(telemetry.get("internet_latency_ms"))
    internet_health = telemetry.get("internet_health", "healthy")
    dns_latency = num(telemetry.get("dns_latency_ms"))
    mqtt_publish = num(telemetry.get("mqtt_publish_ms"))
    pi5_status = telemetry.get("pi5_status", "online")
    pi4_temp = num(telemetry.get("pi4_temperature_c"))

    if gateway_status != "online":
        add("gateway_offline", "Gateway", "critical", "Gateway is unreachable from the Pi4 probe", gateway_status, ["Gateway", "LAN", "Internet", "DNS", "MQTT", "Home Assistant"], "Local gateway or LAN path", 94)
    elif gateway_latency >= num(config.get("HIOC_MAJOR_GATEWAY_LATENCY_MS", 100)):
        add("gateway_latency", "Gateway", "major", f"Gateway latency is {gateway_latency} ms", f"{gateway_latency} ms", ["Gateway", "LAN", "DNS"], "Local gateway or LAN path", 88)
    elif gateway_latency >= num(config.get("HIOC_WARN_GATEWAY_LATENCY_MS", 20)):
        add("gateway_latency", "Gateway", "warning", f"Gateway latency is {gateway_latency} ms", f"{gateway_latency} ms", ["Gateway", "LAN"], "Local gateway or LAN path", 78)

    gateway_healthy = gateway_status == "online" and gateway_latency < num(config.get("HIOC_WARN_GATEWAY_LATENCY_MS", 20))

    if packet_loss >= num(config.get("HIOC_MAJOR_PACKET_LOSS_PERCENT", 10)):
        add("packet_loss", "Internet", "major", f"Packet loss is {packet_loss}%", f"{packet_loss}%", ["Internet", "DNS", "MQTT", "Cloud services"], "ISP or upstream routing" if gateway_healthy else "Network path", 92 if gateway_healthy else 82)
    elif packet_loss >= num(config.get("HIOC_WARN_PACKET_LOSS_PERCENT", 1)):
        add("packet_loss", "Internet", "warning", f"Packet loss is {packet_loss}%", f"{packet_loss}%", ["Internet"], "ISP or upstream routing" if gateway_healthy else "Network path", 84 if gateway_healthy else 72)

    if internet_latency >= num(config.get("HIOC_MAJOR_INTERNET_LATENCY_MS", 250)):
        add("internet_latency", "Internet", "major", f"Average internet latency is {internet_latency} ms", f"{internet_latency} ms", ["Internet", "Cloud services"], "ISP or upstream routing" if gateway_healthy else "Network path", 88 if gateway_healthy else 76)
    elif internet_latency >= num(config.get("HIOC_WARN_INTERNET_LATENCY_MS", 120)):
        add("internet_latency", "Internet", "warning", f"Average internet latency is {internet_latency} ms", f"{internet_latency} ms", ["Internet"], "ISP or upstream routing" if gateway_healthy else "Network path", 80 if gateway_healthy else 70)

    if internet_health == "critical":
        add("internet_health", "Internet", "critical", "Probe reports internet health as critical", internet_health, ["Internet", "DNS", "MQTT"], "Internet reachability", 86)
    elif internet_health == "degraded":
        add("internet_health", "Internet", "warning", "Probe reports internet health as degraded", internet_health, ["Internet"], "Internet reachability", 74)

    if dns_latency >= num(config.get("HIOC_MAJOR_DNS_LATENCY_MS", 500)):
        add("dns_latency", "DNS", "major", f"Local DNS latency is {dns_latency} ms", f"{dns_latency} ms", ["DNS", "Pi-hole", "Internet"], "DNS resolver path", 86)
    elif dns_latency >= num(config.get("HIOC_WARN_DNS_LATENCY_MS", 100)):
        add("dns_latency", "DNS", "warning", f"Local DNS latency is {dns_latency} ms", f"{dns_latency} ms", ["DNS", "Pi-hole"], "DNS resolver path", 76)

    if mqtt_publish >= num(config.get("HIOC_MAJOR_MQTT_PUBLISH_MS", 2000)):
        add("mqtt_publish", "MQTT", "major", f"MQTT publish duration is {mqtt_publish} ms", f"{mqtt_publish} ms", ["MQTT", "Telemetry", "Home Assistant"], "MQTT broker or Home Assistant host load", 82)
    elif mqtt_publish >= num(config.get("HIOC_WARN_MQTT_PUBLISH_MS", 500)):
        add("mqtt_publish", "MQTT", "warning", f"MQTT publish duration is {mqtt_publish} ms", f"{mqtt_publish} ms", ["MQTT", "Telemetry"], "MQTT broker or Home Assistant host load", 72)

    if pi5_status != "online":
        add("pi5_offline", "Pi5", "critical", "Pi5 / Home Assistant host is unreachable from Pi4", pi5_status, ["Home Assistant", "Dashboard", "Automations"], "Pi5 power, network, or HA host failure", 95)

    if pi4_temp >= num(config.get("HIOC_MAJOR_PI4_TEMP_C", 75)):
        add("pi4_temperature", "Pi4", "major", f"Pi4 temperature is {pi4_temp}C", f"{pi4_temp}C", ["Pi4", "Pi-hole", "NUT", "Probe"], "Pi4 thermal headroom reduced", 90)
    elif pi4_temp >= num(config.get("HIOC_WARN_PI4_TEMP_C", 65)):
        add("pi4_temperature", "Pi4", "warning", f"Pi4 temperature is {pi4_temp}C", f"{pi4_temp}C", ["Pi4"], "Pi4 thermal headroom reduced", 76)

    return signals


def build_inventory_signals(inventory: dict) -> list[dict]:
    signals = []
    devices = inventory.get("devices", []) if isinstance(inventory, dict) else []
    services = inventory.get("services", []) if isinstance(inventory, dict) else []
    service_by_device = {}
    for service in services:
        service_by_device.setdefault(service.get("device_id"), []).append(service)

    for device in devices:
        if not is_operationally_monitored(device):
            continue
        status = device.get("health_status")
        if status not in ("degraded", "offline"):
            continue
        severity = "critical" if status == "offline" and ("gateway" in device.get("roles", []) or "collector" in device.get("roles", [])) else "major" if status == "offline" else "warning"
        name = device.get("display_name") or device.get("hostname") or device.get("ip") or device.get("id", "unknown device")
        affected = [name]
        for service in service_by_device.get(device.get("id"), []):
            affected.append(service.get("name", service.get("type", "service")))
        signals.append({
            "name": f"inventory_{status}",
            "system": name,
            "severity": severity,
            "reason": f"{name} inventory health is {status}: {', '.join(device.get('health_reasons', [])) or 'health score threshold'}",
            "value": str(device.get("health_score", "unknown")),
            "affected": sorted(set(affected)),
            "root_hint": name,
            "confidence": 88 if status == "offline" else 74,
            "source": "inventory",
            "device_id": device.get("id"),
        })
    return signals


def build_event_signals(events: list[dict]) -> list[dict]:
    signals = []
    for event in events[:20]:
        event_type = event.get("type")
        if event_type in ("DeviceDiscovered", "InventoryChanged", "TopologyChanged"):
            signals.append({
                "name": event_type,
                "system": "HIOC",
                "severity": "info",
                "reason": f"Internal event {event_type} from {event.get('source', 'unknown')}",
                "value": event.get("id", ""),
                "affected": ["Inventory"],
                "root_hint": "Inventory change",
                "confidence": 40,
                "source": "event",
            })
    return signals


def affected_from_graph(root_device_id: str, inventory: dict) -> list[str]:
    if not root_device_id:
        return []
    devices = {device.get("id"): device for device in inventory.get("devices", [])}
    services = {service.get("id"): service for service in inventory.get("services", [])}
    affected = []
    for edge in inventory.get("topology", {}).get("edges", []):
        if edge.get("parent_id") == root_device_id and edge.get("child_id") in devices:
            affected.append(devices[edge["child_id"]].get("display_name", edge["child_id"]))
    for edge in inventory.get("dependencies", {}).get("edges", []):
        if edge.get("from_id") == root_device_id and edge.get("to_id") in services:
            affected.append(services[edge["to_id"]].get("name", edge["to_id"]))
    return sorted(set(affected))


def correlate(signals: list[dict], inventory: dict = None) -> dict:
    actionable = [signal for signal in signals if severity_rank(signal.get("severity", "info")) >= 2]
    if not actionable:
        return {}
    inventory = inventory or {}
    names = {signal["name"] for signal in actionable}
    severity = max((signal["severity"] for signal in actionable), key=severity_rank)
    evidence = [f"{signal['system']}: {signal['reason']}" for signal in actionable]
    affected = sorted(set(item for signal in actionable for item in signal.get("affected", [])))
    confidence = min(100, round(sum(signal.get("confidence", 60) for signal in actionable) / len(actionable)))

    if "gateway_offline" in names or "gateway_latency" in names:
        key = "network_path_degradation"
        title = "Network path degradation"
        system = "Gateway"
        root = "Local gateway or LAN path"
        recommendation = "Check gateway, AP/switch path, cabling, and local network load."
        confidence = max(confidence, 90)
    elif {"packet_loss", "internet_latency", "internet_health"} & names:
        key = "internet_degradation_isp_likely"
        title = "Internet degradation"
        system = "Internet"
        root = "ISP or upstream routing"
        recommendation = "Gateway and local services should be checked first, then compare external targets and ISP path."
        confidence = max(confidence, 86)
    elif "dns_latency" in names:
        key = "dns_degradation"
        title = "DNS degradation"
        system = "DNS"
        root = "Pi-hole, upstream DNS, or resolver latency"
        recommendation = "Check Pi-hole FTL, upstream resolver, and Pi4 resource load."
        confidence = max(confidence, 82)
    elif "mqtt_publish" in names:
        key = "mqtt_degradation"
        title = "MQTT telemetry degradation"
        system = "MQTT"
        root = "MQTT broker or Home Assistant host load"
        recommendation = "Check Mosquitto broker status, HA host load, and MQTT client pressure."
        confidence = max(confidence, 78)
    elif "pi5_offline" in names:
        key = "home_assistant_host_unreachable"
        title = "Home Assistant host unreachable"
        system = "Pi5"
        root = "Pi5 power, network, or HA host failure"
        recommendation = "Check Pi5 power, network link, and Home Assistant host status."
        confidence = max(confidence, 95)
    elif "pi4_temperature" in names:
        key = "pi4_thermal_degradation"
        title = "Pi4 thermal warning"
        system = "Pi4"
        root = "Pi4 thermal headroom reduced"
        recommendation = "Check Pi4 cooling, case airflow, and CPU load."
        confidence = max(confidence, 88)
    else:
        primary = max(actionable, key=lambda signal: severity_rank(signal.get("severity", "info")))
        root_device_id = primary.get("device_id", "")
        graph_affected = affected_from_graph(root_device_id, inventory)
        affected = sorted(set(affected + graph_affected))
        key = f"inventory_{stable_id(primary.get('root_hint', primary['system']))[:12]}"
        title = f"{primary['system']} health degradation"
        system = primary["system"]
        root = primary.get("root_hint", primary["system"])
        recommendation = "Review inventory health reasons, device power/network state, and dependent services."
        confidence = max(confidence, 80 if graph_affected else 70)

    return {
        "id": stable_id(key),
        "key": key,
        "status": "active",
        "phase": "detected",
        "severity": severity,
        "system": system,
        "title": title,
        "root_cause": root,
        "confidence_percent": int(confidence),
        "reason": "; ".join(evidence),
        "impact": f"Affected systems: {', '.join(affected)}" if affected else "Affected systems are being evaluated",
        "affected": affected,
        "recommendation": recommendation,
        "current_value": actionable[0].get("value", ""),
        "evidence": evidence,
        "signals": actionable,
    }


def lifecycle_phase(occurrences: int, confirm_cycles: int) -> str:
    if occurrences <= 1:
        return "detected"
    if occurrences < confirm_cycles:
        return "confirmed"
    return "active"

