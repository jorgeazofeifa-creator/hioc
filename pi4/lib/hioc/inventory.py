import hashlib
import ipaddress
import json
import os
import re
import socket
import time
from pathlib import Path

from .runtime import run_command, now_iso
from .core.capabilities import CapabilityRegistry
from .core.drivers import DriverRegistry, DriverResult


MAC_RE = re.compile(r"^[0-9a-f]{2}(:[0-9a-f]{2}){5}$")


def normalize_mac(value: str) -> str:
    mac = str(value or "").strip().lower().replace("-", ":")
    return mac if MAC_RE.match(mac) else ""


def stable_device_id(record: dict) -> str:
    key = record.get("mac") or record.get("ip") or record.get("hostname") or record.get("name") or "unknown"
    return "dev_" + hashlib.sha1(str(key).lower().encode()).hexdigest()[:16]


def read_os_release(path: Path = Path("/etc/os-release")) -> dict:
    values = {}
    if not path.exists():
        return values
    for raw in path.read_text(errors="ignore").splitlines():
        if "=" not in raw:
            continue
        key, value = raw.split("=", 1)
        values[key.lower()] = value.strip().strip('"')
    return values


def local_ipv4_addresses() -> list[dict]:
    code, out, _ = run_command(["ip", "-o", "-4", "addr", "show"], timeout=4)
    addresses = []
    if code != 0:
        return addresses
    for line in out.splitlines():
        parts = line.split()
        if len(parts) < 4:
            continue
        interface = parts[1]
        cidr = parts[3]
        if cidr.startswith("127."):
            continue
        mac = ""
        _, mac_out, _ = run_command(["cat", f"/sys/class/net/{interface}/address"], timeout=2)
        addresses.append({"interface": interface, "cidr": cidr, "ip": cidr.split("/", 1)[0], "mac": normalize_mac(mac_out)})
    return addresses


def default_gateway() -> dict:
    code, out, _ = run_command(["ip", "route", "show", "default"], timeout=4)
    if code != 0 or not out:
        return {}
    parts = out.split()
    data = {}
    if "via" in parts:
        data["ip"] = parts[parts.index("via") + 1]
    if "dev" in parts:
        data["interface"] = parts[parts.index("dev") + 1]
    return data


def neighbor_table() -> dict:
    code, out, _ = run_command(["ip", "neigh", "show"], timeout=4)
    neighbors = {}
    if code != 0:
        code, out, _ = run_command(["arp", "-an"], timeout=4)
    for line in out.splitlines():
        ip_match = re.search(r"(\d+\.\d+\.\d+\.\d+)", line)
        mac_match = re.search(r"([0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}", line)
        if not ip_match:
            continue
        ip = ip_match.group(1)
        mac = normalize_mac(mac_match.group(0)) if mac_match else ""
        if ip:
            neighbors[ip] = {"ip": ip, "mac": mac, "source": "neighbor_table", "last_seen_source": "neighbor_table"}
    return neighbors


def dhcp_leases() -> dict:
    paths = [
        Path("/etc/pihole/dhcp.leases"),
        Path("/var/lib/misc/dnsmasq.leases"),
        Path("/var/lib/dhcp/dhcpd.leases"),
    ]
    devices = {}
    for path in paths:
        if not path.exists():
            continue
        for raw in path.read_text(errors="ignore").splitlines():
            parts = raw.split()
            if len(parts) < 3:
                continue
            if normalize_mac(parts[1]):
                hostname = parts[3] if len(parts) >= 4 and parts[3] != "*" else ""
                devices[parts[2]] = {
                    "ip": parts[2],
                    "mac": normalize_mac(parts[1]),
                    "hostname": hostname,
                    "source": path.name,
                    "last_seen_source": path.name,
                }
    return devices


def integration_inventory(config: dict, state_dir: Path) -> dict:
    configured = config.get("HIOC_INVENTORY_INTEGRATION_DIR", "")
    root = Path(configured) if configured else state_dir / "inventory" / "integrations"
    devices = {}
    if not root.exists() or not root.is_dir():
        return devices
    for path in sorted(root.glob("*.json")):
        try:
            payload = json.loads(path.read_text())
        except Exception:
            continue
        if isinstance(payload, dict):
            records = payload.get("devices", [])
        elif isinstance(payload, list):
            records = payload
        else:
            records = []
        for item in records:
            if not isinstance(item, dict):
                continue
            record = dict(item)
            record["mac"] = normalize_mac(record.get("mac", ""))
            if record.get("parent_mac"):
                record["parent_mac"] = normalize_mac(record.get("parent_mac", ""))
            key = record.get("mac") or record.get("ip") or record.get("hostname") or record.get("name")
            if key:
                record.setdefault("source", f"integration:{path.stem}")
                record.setdefault("last_seen_source", f"integration:{path.stem}")
                devices[str(key)] = record
    return devices


def reverse_dns(ip: str) -> str:
    try:
        name = socket.gethostbyaddr(ip)[0]
        return name.rstrip(".")
    except Exception:
        return ""


def ping_reachable(ip: str, count: int, timeout_sec: int) -> bool:
    code, _, _ = run_command(["ping", "-c", str(count), "-W", str(timeout_sec), ip], timeout=max(3, count * timeout_sec + 2))
    return code == 0


def scan_subnet(cidr: str, count: int, timeout_sec: int) -> dict:
    if not cidr:
        return {}
    try:
        network = ipaddress.ip_network(cidr, strict=False)
    except ValueError:
        return {}
    if network.num_addresses > 1024:
        return {}
    devices = {}
    code, out, _ = run_command(["nmap", "-sn", str(network)], timeout=90)
    if code == 0:
        current_ip = ""
        current_name = ""
        for line in out.splitlines():
            host = re.search(r"Nmap scan report for (?:([^\s]+) )?\(?(\d+\.\d+\.\d+\.\d+)\)?", line)
            mac = re.search(r"MAC Address: ([0-9A-Fa-f:]{17})(?: \((.+)\))?", line)
            if host:
                current_name = host.group(1) or ""
                current_ip = host.group(2)
                devices[current_ip] = {"ip": current_ip, "hostname": current_name if current_name != current_ip else "", "source": "nmap", "last_seen_source": "nmap"}
            elif mac and current_ip:
                devices[current_ip]["mac"] = normalize_mac(mac.group(1))
                devices[current_ip]["vendor"] = mac.group(2) or ""
        return devices
    for host in network.hosts():
        ip = str(host)
        if ping_reachable(ip, count, timeout_sec):
            devices[ip] = {"ip": ip, "source": "ping_sweep", "last_seen_source": "ping_sweep"}
    return devices


def systemd_services() -> dict:
    code, out, _ = run_command(["systemctl", "list-units", "--type=service", "--all", "--no-pager", "--plain"], timeout=8)
    services = {}
    if code != 0:
        return services
    for line in out.splitlines():
        parts = line.split()
        if len(parts) < 4 or not parts[0].endswith(".service"):
            continue
        name = parts[0].replace(".service", "")
        state = parts[2]
        services[name] = {"name": name, "status": state, "manager": "systemd"}
    return services


def listening_services() -> list[dict]:
    code, out, _ = run_command(["ss", "-ltnup"], timeout=6)
    services = []
    if code != 0:
        return services
    for line in out.splitlines()[1:]:
        parts = line.split()
        if len(parts) < 5:
            continue
        local = parts[4]
        proc = parts[-1] if len(parts) > 5 else ""
        port = local.rsplit(":", 1)[-1] if ":" in local else ""
        if port.isdigit():
            services.append({"port": int(port), "protocol": parts[0].lower(), "process": proc, "status": "listening"})
    return services


def package_version(package: str) -> str:
    code, out, _ = run_command(["dpkg-query", "-W", "-f=${Version}", package], timeout=4)
    return out if code == 0 else ""


def snmp_firmware(ip: str, community: str) -> dict:
    if not community:
        return {}
    code, out, _ = run_command(["snmpget", "-v2c", "-c", community, "-Oqv", ip, "1.3.6.1.2.1.1.1.0"], timeout=4)
    if code != 0 or not out:
        return {}
    return {"sys_descr": out.strip().strip('"')}


class PassiveNetworkDriver:
    name = "passive_network"

    def discover(self, config: dict) -> DriverResult:
        devices = list(neighbor_table().values()) + list(dhcp_leases().values())
        state_root = Path(config.get("HIOC_HOME", "/home/jazofv1/hioc")) / "state"
        devices.extend(integration_inventory(config, state_root).values())
        return DriverResult(name=self.name, devices=devices)


class ActiveNetworkDriver:
    name = "active_network"

    def discover(self, config: dict) -> DriverResult:
        devices = list(scan_subnet(config.get("HIOC_INVENTORY_SCAN_SUBNET", ""), int(config.get("HIOC_INVENTORY_PING_COUNT", "1")), int(config.get("HIOC_INVENTORY_PING_TIMEOUT_SEC", "1"))).values())
        return DriverResult(name=self.name, devices=devices)


class LocalServiceDriver:
    name = "local_services"

    def __init__(self, local_device_id: str):
        self.local_device_id = local_device_id

    def discover(self, config: dict) -> DriverResult:
        services = build_services(self.local_device_id, systemd_services(), listening_services())
        return DriverResult(name=self.name, services=services)


def classify_device(record: dict, gateway_ip: str, local_ips: set[str]) -> tuple[str, list[str]]:
    ip = record.get("ip", "")
    hostname = (record.get("hostname") or record.get("name") or "").lower()
    vendor = (record.get("vendor") or "").lower()
    model = (record.get("model") or "").lower()
    combined = " ".join([hostname, vendor, model])
    roles = []
    if ip == gateway_ip:
        roles.append("gateway")
    if ip in local_ips:
        roles.append("collector")
    if "pi" in hostname or "raspberry" in hostname:
        roles.append("linux_host")
    if "homeassistant" in hostname or "haos" in hostname:
        roles.append("home_assistant")
    if "pihole" in hostname or "pi-hole" in hostname:
        roles.extend(["dns", "dhcp"])
    if any(token in combined for token in ("orbi", "satellite", "mesh", "access-point", "access point", "ap-")):
        roles.append("wireless_infrastructure")
    if any(token in combined for token in ("switch", "netgear gs", "unifi usw", "tp-link sg", "managed-switch")):
        roles.append("switch")
    if not roles:
        roles.append("endpoint")
    primary = "gateway" if "gateway" in roles else "collector" if "collector" in roles else "network_infrastructure" if {"wireless_infrastructure", "switch"} & set(roles) else "home_assistant" if "home_assistant" in roles else "endpoint"
    return primary, sorted(set(roles))


def health_score(record: dict, now_epoch: int, stale_after: int, offline_after: int) -> tuple[int, str, list[str]]:
    reasons = []
    score = 100
    last_seen = int(record.get("last_seen_epoch") or 0)
    age = now_epoch - last_seen if last_seen else offline_after + 1
    if age > offline_after:
        score -= 55
        reasons.append("not seen within offline threshold")
    elif age > stale_after:
        score -= 25
        reasons.append("last seen is stale")
    if record.get("reachable") is False:
        score -= 35
        reasons.append("ping check failed")
    if not record.get("mac") and record.get("type") != "local_host":
        score -= 5
        reasons.append("MAC address not observed")
    score = max(0, min(100, score))
    if score >= 90:
        status = "healthy"
    elif score >= 70:
        status = "watch"
    elif score >= 40:
        status = "degraded"
    else:
        status = "offline"
    return score, status, reasons


def merge_records(records: list[dict], previous: dict, now: str, now_epoch: int, config: dict) -> list[dict]:
    by_key = {}
    for record in records:
        key = normalize_mac(record.get("mac", "")) or record.get("ip") or record.get("hostname")
        if not key:
            continue
        existing = by_key.setdefault(key, {})
        existing.update({k: v for k, v in record.items() if v not in ("", None, [])})
    prev_by_id = {item.get("id"): item for item in previous.get("devices", []) if item.get("id")}
    stale_after = int(config.get("HIOC_INVENTORY_STALE_AFTER_SEC", "900"))
    offline_after = int(config.get("HIOC_INVENTORY_OFFLINE_AFTER_SEC", "3600"))
    devices = []
    for record in by_key.values():
        record["mac"] = normalize_mac(record.get("mac", ""))
        record["id"] = stable_device_id(record)
        prev = prev_by_id.get(record["id"], {})
        record["first_seen"] = prev.get("first_seen", now)
        record["last_seen"] = now
        record["last_seen_epoch"] = now_epoch
        record["display_name"] = record.get("hostname") or record.get("name") or record.get("ip") or record["id"]
        score, status, reasons = health_score(record, now_epoch, stale_after, offline_after)
        record["health_score"] = score
        record["health_status"] = status
        record["health_reasons"] = reasons
        devices.append(record)
    seen_ids = {d["id"] for d in devices}
    for old in previous.get("devices", []):
        if old.get("id") not in seen_ids:
            record = dict(old)
            score, status, reasons = health_score(record, now_epoch, stale_after, offline_after)
            record["health_score"] = score
            record["health_status"] = status
            record["health_reasons"] = reasons
            devices.append(record)
    return sorted(devices, key=lambda item: (item.get("type", ""), item.get("display_name", "")))


def build_services(local_device_id: str, systemd: dict, sockets: list[dict]) -> list[dict]:
    interesting = {
        "mosquitto": "mqtt",
        "pihole-FTL": "dns",
        "pihole-FTL.service": "dns",
        "dnsmasq": "dhcp",
        "nut-server": "ups",
        "nut-monitor": "ups",
        "ssh": "ssh",
        "cron": "scheduler",
    }
    services = []
    for name, service_type in interesting.items():
        unit = systemd.get(name.replace(".service", ""))
        if unit:
            services.append({"id": f"svc_{service_type}_{hashlib.sha1(name.encode()).hexdigest()[:8]}", "name": name, "type": service_type, "device_id": local_device_id, "status": unit["status"], "source": "systemd"})
    for item in sockets:
        if item["port"] == 1883:
            services.append({"id": "svc_mqtt_listener", "name": "MQTT listener", "type": "mqtt", "device_id": local_device_id, "status": item["status"], "port": item["port"], "source": "ss"})
        elif item["port"] in (53, 67):
            services.append({"id": f"svc_network_{item['port']}", "name": f"Network service port {item['port']}", "type": "dns" if item["port"] == 53 else "dhcp", "device_id": local_device_id, "status": item["status"], "port": item["port"], "source": "ss"})
    unique = {}
    for service in services:
        unique[service["id"]] = service
    return sorted(unique.values(), key=lambda item: item["id"])


def _device_lookup(devices: list[dict]) -> tuple[dict, dict, dict]:
    by_id = {device.get("id"): device for device in devices if device.get("id")}
    by_mac = {device.get("mac"): device for device in devices if device.get("mac")}
    by_ip = {device.get("ip"): device for device in devices if device.get("ip")}
    return by_id, by_mac, by_ip


def _hinted_parent_id(device: dict, by_id: dict, by_mac: dict, by_ip: dict) -> str:
    for field, lookup in (("parent_id", by_id), ("parent_device_id", by_id), ("parent_mac", by_mac), ("uplink_mac", by_mac), ("parent_ip", by_ip), ("uplink_ip", by_ip)):
        value = device.get(field)
        if value in lookup and lookup[value].get("id") != device.get("id"):
            return lookup[value]["id"]
    return ""


def build_topology(devices: list[dict], gateway_ip: str, local_device_id: str) -> dict:
    gateway_id = next((d["id"] for d in devices if d.get("ip") == gateway_ip), "")
    by_id, by_mac, by_ip = _device_lookup(devices)
    infrastructure_roles = {"wireless_infrastructure", "switch"}
    infrastructure = [
        device for device in devices
        if infrastructure_roles & set(device.get("roles", [])) and device.get("id") not in (gateway_id, local_device_id)
    ]
    edges = []
    for device in devices:
        if device["id"] == gateway_id:
            continue
        hinted_parent = _hinted_parent_id(device, by_id, by_mac, by_ip)
        if hinted_parent:
            parent = hinted_parent
        elif device in infrastructure:
            parent = gateway_id or local_device_id
        elif len(infrastructure) == 1 and device["id"] not in (gateway_id, local_device_id):
            parent = infrastructure[0]["id"]
        else:
            parent = gateway_id or local_device_id
        if device["id"] != parent:
            device["parent_id"] = parent
            edges.append({"parent_id": parent, "child_id": device["id"], "relationship": "network_parent"})
    return {"root_id": gateway_id or local_device_id, "edges": edges}


def build_dependencies(devices: list[dict], services: list[dict]) -> dict:
    edges = []
    service_by_type = {}
    for service in services:
        service_by_type.setdefault(service["type"], service["id"])
    for device in devices:
        if device.get("health_status") == "offline":
            continue
        for service_type in ("dns", "dhcp", "mqtt"):
            if service_type in service_by_type and service_by_type[service_type] != device["id"]:
                edges.append({"from_id": device["id"], "to_id": service_by_type[service_type], "type": f"depends_on_{service_type}"})
    for service in services:
        if service["type"] == "mqtt" and "dns" in service_by_type:
            edges.append({"from_id": service["id"], "to_id": service_by_type["dns"], "type": "depends_on_dns"})
    return {"edges": edges}


def discover_inventory(config: dict, previous: dict) -> dict:
    now = now_iso()
    now_epoch = int(time.time())
    local_addresses = local_ipv4_addresses()
    local_ips = {item["ip"] for item in local_addresses}
    gateway = default_gateway()
    gateway_ip = gateway.get("ip", "")
    active_discovery = str(config.get("HIOC_INVENTORY_ACTIVE_DISCOVERY", "off")).lower() in ("1", "true", "yes", "on", "enabled")
    records = []
    hostname = socket.gethostname()
    os_release = read_os_release()
    kernel = os.uname().release if hasattr(os, "uname") else ""
    local_mac = next((item["mac"] for item in local_addresses if item.get("mac")), "")
    local_ip = next((item["ip"] for item in local_addresses), "")
    records.append({
        "type": "local_host",
        "name": hostname,
        "hostname": hostname,
        "ip": local_ip,
        "mac": local_mac,
        "interfaces": local_addresses,
        "firmware": {
            "os": os_release.get("pretty_name", ""),
            "kernel": kernel,
            "mosquitto": package_version("mosquitto"),
            "pihole": package_version("pihole-FTL"),
        },
        "reachable": True,
        "source": "local_host",
        "last_seen_source": "local_host",
    })
    if gateway_ip:
        records.append({"type": "network_device", "name": "Default Gateway", "ip": gateway_ip, "interface": gateway.get("interface", ""), "source": "default_route", "last_seen_source": "default_route"})
    state_root = Path(config.get("HIOC_HOME", "/home/jazofv1/hioc")) / "state"
    registry = DriverRegistry()
    registry.register(PassiveNetworkDriver())
    if active_discovery:
        registry.register(ActiveNetworkDriver())
    for result in registry.run(config):
        records.extend(result.devices)
    count = int(config.get("HIOC_INVENTORY_PING_COUNT", "1"))
    timeout = int(config.get("HIOC_INVENTORY_PING_TIMEOUT_SEC", "1"))
    community = config.get("HIOC_INVENTORY_SNMP_COMMUNITY", "")
    enriched = []
    for record in records:
        if record.get("ip"):
            if active_discovery:
                record.setdefault("hostname", reverse_dns(record["ip"]))
            if active_discovery and record["ip"] not in local_ips:
                record["reachable"] = ping_reachable(record["ip"], count, timeout)
            if active_discovery:
                firmware = snmp_firmware(record["ip"], community)
                if firmware:
                    record["firmware"] = firmware
        primary_type, roles = classify_device(record, gateway_ip, local_ips)
        if "gateway" in roles:
            record["type"] = "gateway"
        elif "collector" in roles:
            record["type"] = record.get("type") or "collector"
        else:
            record["type"] = record.get("type") or primary_type
        record["roles"] = roles
        enriched.append(record)
    devices = merge_records(enriched, previous, now, now_epoch, config)
    local_device_id = next((d["id"] for d in devices if d.get("type") == "local_host"), devices[0]["id"] if devices else "")
    service_registry = DriverRegistry()
    service_registry.register(LocalServiceDriver(local_device_id))
    services = []
    for result in service_registry.run(config):
        services.extend(result.services)
    topology = build_topology(devices, gateway_ip, local_device_id)
    dependencies = build_dependencies(devices, services)
    capabilities = CapabilityRegistry()
    for device in devices:
        capabilities.infer_from_device(device)
    for service in services:
        capabilities.infer_from_service(service)
    capability_list = capabilities.all()
    summary = {
        "updated": now,
        "device_count": len(devices),
        "healthy_count": len([d for d in devices if d.get("health_status") == "healthy"]),
        "watch_count": len([d for d in devices if d.get("health_status") == "watch"]),
        "degraded_count": len([d for d in devices if d.get("health_status") == "degraded"]),
        "offline_count": len([d for d in devices if d.get("health_status") == "offline"]),
        "service_count": len(services),
        "topology_edges": len(topology["edges"]),
        "dependency_edges": len(dependencies["edges"]),
        "lowest_health_score": min([d.get("health_score", 0) for d in devices], default=0),
    }
    return {
        "schema_version": "1.0",
        "updated": now,
        "devices": devices,
        "services": services,
        "_capabilities": capability_list,
        "topology": topology,
        "dependencies": dependencies,
        "summary": summary,
    }
