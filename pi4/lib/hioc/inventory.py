import hashlib
import ipaddress
import json
import logging
import os
import re
import socket
import time
from datetime import datetime
from pathlib import Path

from .runtime import run_command, now_iso
from .core.capabilities import CapabilityRegistry
from .core.drivers import DriverRegistry, DriverResult
from .core.monitoring import is_dhcp_assignment_only, is_operationally_monitored, record_sources as _record_sources


MAC_RE = re.compile(r"^[0-9a-f]{2}(:[0-9a-f]{2}){5}$")
KNOWN_SOURCE = "known_infrastructure"
KNOWN_FIELDS = {
    "id",
    "name",
    "hostname",
    "ip",
    "mac",
    "role",
    "type",
    "vendor",
    "model",
    "location",
    "area",
    "parent_id",
    "parent_device_id",
    "parent_mac",
    "parent_ip",
    "uplink_mac",
    "uplink_ip",
    "notes",
    "enabled",
}
KNOWN_METADATA_FIELDS = {
    "name",
    "hostname",
    "role",
    "type",
    "vendor",
    "model",
    "location",
    "area",
    "parent_id",
    "parent_device_id",
    "parent_mac",
    "parent_ip",
    "uplink_mac",
    "uplink_ip",
    "notes",
}
OPERATOR_ROLES = {
    "Core Infrastructure",
    "Network Equipment",
    "Server",
    "IoT",
    "Media",
    "Workstation",
    "Mobile",
    "Unknown",
}


LOG = logging.getLogger("hioc-inventory-engine")
NEIGHBOR_STATES = {"DELAY", "FAILED", "INCOMPLETE", "NOARP", "NONE", "PERMANENT", "PROBE", "REACHABLE", "STALE"}
DURABLE_NEIGHBOR_STATES = {"DELAY", "PERMANENT", "PROBE", "REACHABLE", "STALE"}


def normalize_mac(value: str) -> str:
    mac = str(value or "").strip().lower().replace("-", ":")
    return mac if MAC_RE.match(mac) else ""


def normalize_hostname(value: str) -> str:
    return str(value or "").strip().lower().rstrip(".")


def stable_device_id(record: dict) -> str:
    key = record.get("mac") or record.get("ip") or record.get("hostname") or record.get("_configured_id") or record.get("name") or "unknown"
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
    fallback = code != 0
    if code != 0:
        code, out, _ = run_command(["arp", "-an"], timeout=4)
        if code != 0:
            return neighbors
    for line in out.splitlines():
        ip_match = re.search(r"(\d+\.\d+\.\d+\.\d+)", line)
        mac_match = re.search(r"([0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}", line)
        if not ip_match:
            continue
        ip = ip_match.group(1)
        mac = normalize_mac(mac_match.group(0)) if mac_match else ""
        parts = line.split()
        interface = next((parts[index + 1] for index, token in enumerate(parts[:-1]) if token in ("dev", "on")), "")
        if fallback:
            if not mac:
                state = "INCOMPLETE" if "<incomplete>" in line.lower() else "UNKNOWN"
                LOG.debug("neighbor entry ignored ip=%s interface=%s state=%s reason=missing_valid_mac", ip, interface, state)
                continue
        else:
            state = next((token.upper() for token in reversed(parts) if token.upper() in NEIGHBOR_STATES), "UNKNOWN")
            if state not in DURABLE_NEIGHBOR_STATES or not mac:
                reason = "unresolved_state" if state in {"FAILED", "INCOMPLETE", "NONE"} else "missing_valid_mac" if not mac else "non_durable_state"
                LOG.debug("neighbor entry ignored ip=%s interface=%s state=%s reason=%s", ip, interface, state, reason)
                continue
        neighbors[ip] = {"ip": ip, "mac": mac, "source": "arp_table", "last_seen_source": "arp_table"}
    return neighbors


def dhcp_lease_paths(config: dict | None = None) -> list[Path]:
    configured = (config or {}).get("HIOC_INVENTORY_DHCP_LEASE_FILES", "")
    if configured:
        return [Path(item.strip()) for item in configured.split(",") if item.strip()]
    return [
        Path("/etc/pihole/dhcp.leases"),
        Path("/var/lib/misc/dnsmasq.leases"),
        Path("/var/lib/dhcp/dhcpd.leases"),
    ]


def dhcp_leases(paths: list[Path] | None = None) -> dict:
    paths = paths or dhcp_lease_paths()
    devices = {}
    for path in paths:
        if not path.exists():
            continue
        try:
            lines = path.read_text(errors="ignore").splitlines()
        except OSError:
            continue
        for raw in lines:
            parts = raw.split()
            if len(parts) < 3:
                continue
            if normalize_mac(parts[1]):
                hostname = parts[3] if len(parts) >= 4 and parts[3] != "*" else ""
                devices[parts[2]] = {
                    "ip": parts[2],
                    "mac": normalize_mac(parts[1]),
                    "hostname": hostname,
                    "source": "dhcp_leases",
                    "last_seen_source": str(path),
                }
    return devices


def dhcp_lease_discovery(config: dict) -> tuple[dict, str]:
    paths = dhcp_lease_paths(config)
    existing = [path for path in paths if path.exists()]
    if not existing:
        return {}, "dhcp_leases_unavailable"
    devices = dhcp_leases(existing)
    return devices, "dhcp_leases" if devices else "dhcp_leases_empty"


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


def known_infrastructure_path(config: dict) -> Path | None:
    raw = config.get("HIOC_INVENTORY_KNOWN_INFRASTRUCTURE_FILE")
    if raw is None:
        raw = str(Path(config.get("HIOC_HOME", "/home/jazofv1/hioc")) / "config" / "inventory" / "known_infrastructure.json")
    raw = str(raw).strip()
    if not raw:
        return None
    path = Path(raw)
    if not path.is_absolute():
        path = Path(config.get("HIOC_HOME", "/home/jazofv1/hioc")) / path
    return path


def _known_warning(message: str) -> None:
    LOG.warning("known infrastructure: %s", message)


def _valid_ip(value: str) -> bool:
    if not value:
        return True
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        return False


def _clean_known_record(raw: dict, index: int, seen_ids: set[str], seen_macs: set[str]) -> dict | None:
    if not isinstance(raw, dict):
        _known_warning(f"record {index} skipped: expected object")
        return None
    if raw.get("enabled") is False:
        return None
    unknown = sorted(set(raw) - KNOWN_FIELDS)
    if unknown:
        _known_warning(f"record {index} ignored unknown fields: {', '.join(unknown)}")
    configured_id = str(raw.get("id", "") or "").strip()
    if configured_id:
        if configured_id in seen_ids:
            _known_warning(f"record {index} id {configured_id} skipped: duplicate configured id")
            return None
        seen_ids.add(configured_id)
    record = {}
    for field in KNOWN_FIELDS - {"enabled", "id"}:
        value = raw.get(field)
        if value in ("", None, []):
            continue
        record[field] = str(value).strip() if isinstance(value, (str, int, float)) else value
    if configured_id:
        record["_configured_id"] = configured_id
    if record.get("mac"):
        mac = normalize_mac(record["mac"])
        if not mac:
            _known_warning(f"record {index} skipped: invalid MAC format")
            return None
        if mac in seen_macs:
            _known_warning(f"record {index} mac {mac} skipped: duplicate configured MAC")
            return None
        seen_macs.add(mac)
        record["mac"] = mac
    for field in ("parent_mac", "uplink_mac"):
        if record.get(field):
            mac = normalize_mac(record[field])
            if not mac:
                _known_warning(f"record {index} skipped: invalid {field} format")
                return None
            record[field] = mac
    for field in ("ip", "parent_ip", "uplink_ip"):
        if record.get(field) and not _valid_ip(record[field]):
            _known_warning(f"record {index} skipped: invalid {field}")
            return None
    if record.get("role") and record["role"] not in OPERATOR_ROLES:
        _known_warning(f"record {index} skipped: unsupported role {record['role']}")
        return None
    if not any(record.get(field) for field in ("mac", "ip", "hostname", "name", "_configured_id")):
        _known_warning(f"record {index} skipped: no usable identifier")
        return None
    record["source"] = KNOWN_SOURCE
    record["last_seen_source"] = KNOWN_SOURCE
    record["_observed"] = False
    record["_known_metadata_fields"] = sorted(field for field in KNOWN_METADATA_FIELDS if record.get(field))
    return record


def known_infrastructure(config: dict) -> list[dict]:
    path = known_infrastructure_path(config)
    if path is None:
        return []
    if not path.exists():
        return []
    try:
        text = path.read_text(errors="ignore").strip()
    except OSError as exc:
        _known_warning(f"{path} skipped: {exc}")
        return []
    if not text:
        _known_warning(f"{path} skipped: file is empty")
        return []
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        _known_warning(f"{path} skipped: invalid JSON at line {exc.lineno} column {exc.colno}")
        return []
    if not isinstance(payload, dict):
        _known_warning(f"{path} skipped: top-level JSON must be an object")
        return []
    records = payload.get("devices", [])
    if not isinstance(records, list):
        _known_warning(f"{path} skipped: devices must be a list")
        return []
    seen_ids = set()
    seen_macs = set()
    accepted = []
    for index, raw in enumerate(records):
        record = _clean_known_record(raw, index, seen_ids, seen_macs)
        if record:
            accepted.append(record)
    return accepted


def _identifier_conflicts(left: dict, right: dict) -> list[str]:
    conflicts = []
    for field in ("mac", "ip"):
        if left.get(field) and right.get(field) and left.get(field) != right.get(field):
            conflicts.append(field)
    left_host = normalize_hostname(left.get("hostname"))
    right_host = normalize_hostname(right.get("hostname"))
    if left_host and right_host and left_host != right_host:
        conflicts.append("hostname")
    return conflicts


def _matching_identifier(left: dict, right: dict) -> str:
    if left.get("mac") and left.get("mac") == right.get("mac"):
        return "mac"
    if left.get("ip") and left.get("ip") == right.get("ip"):
        return "ip"
    left_host = normalize_hostname(left.get("hostname"))
    if left_host and left_host == normalize_hostname(right.get("hostname")):
        return "hostname"
    return ""


def append_known_infrastructure(records: list[dict], known_records: list[dict]) -> list[dict]:
    accepted = list(records)
    observed = [record for record in records if record.get("_observed", True)]
    for index, record in enumerate(known_records):
        matches = []
        if record.get("mac"):
            matches = [item for item in observed if item.get("mac") == record["mac"]]
        if not matches and record.get("ip"):
            matches = [item for item in observed if item.get("ip") == record["ip"]]
        if not matches and record.get("hostname"):
            host = normalize_hostname(record["hostname"])
            matches = [item for item in observed if normalize_hostname(item.get("hostname")) == host]
        if matches:
            conflict = next((item for item in matches if _identifier_conflicts(record, item)), None)
            if conflict:
                configured_id = record.get("_configured_id", f"record {index}")
                matching = _matching_identifier(record, conflict) or "identifier"
                conflicting = ", ".join(_identifier_conflicts(record, conflict))
                _known_warning(f"{configured_id} skipped: matched by {matching} but conflicts on {conflicting}")
                continue
            record["_merge_key"] = _record_key(matches[0])
        else:
            weaker_conflict = next((item for item in observed if _matching_identifier(record, item) and _identifier_conflicts(record, item)), None)
            if weaker_conflict:
                configured_id = record.get("_configured_id", f"record {index}")
                matching = _matching_identifier(record, weaker_conflict)
                conflicting = ", ".join(_identifier_conflicts(record, weaker_conflict))
                _known_warning(f"{configured_id} skipped: matched by {matching} but conflicts on {conflicting}")
                continue
        accepted.append(record)
    return accepted


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
    return {}


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
        devices = []
        neighbors = neighbor_table()
        if neighbors:
            devices.extend(neighbors.values())
        leases, _ = dhcp_lease_discovery(config)
        devices.extend(leases.values())
        state_root = Path(config.get("HIOC_HOME", "/home/jazofv1/hioc")) / "state"
        devices.extend(integration_inventory(config, state_root).values())
        return DriverResult(name=self.name, devices=devices)


class ActiveNetworkDriver:
    name = "active_network"

    def discover(self, config: dict) -> DriverResult:
        return DriverResult(name=self.name, devices=[])


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
    if any(token in combined for token in ("ups", "apc", "eaton", "cyberpower")):
        roles.append("ups")
    if any(token in combined for token in ("camera", "cam-", "frigate", "doorbell", "printer", "thermostat", "sensor", "plug", "bulb", "matter", "zigbee", "zwave", "z-wave")):
        roles.append("iot")
    if any(token in combined for token in ("tv", "roku", "chromecast", "apple-tv", "shield", "sonos", "receiver", "media")):
        roles.append("media")
    if any(token in combined for token in ("iphone", "ipad", "pixel", "android", "galaxy", "phone", "mobile", "tablet")):
        roles.append("mobile")
    if any(token in combined for token in ("laptop", "desktop", "workstation", "macbook", "windows", "pc-")):
        roles.append("workstation")
    if any(token in combined for token in ("server", "nas", "proxmox", "docker", "ubuntu", "debian")):
        roles.append("server")
    if not roles:
        roles.append("endpoint")
    primary = "gateway" if "gateway" in roles else "collector" if "collector" in roles else "network_infrastructure" if {"wireless_infrastructure", "switch"} & set(roles) else "home_assistant" if "home_assistant" in roles else "endpoint"
    return primary, sorted(set(roles))


def operator_role(record: dict, roles: list[str]) -> str:
    role_set = set(roles)
    if "gateway" in role_set:
        return "Network Equipment"
    if role_set & {"wireless_infrastructure", "switch"}:
        return "Network Equipment"
    if role_set & {"collector", "dns", "dhcp", "mqtt", "ups"}:
        return "Core Infrastructure"
    if role_set & {"home_assistant", "server", "linux_host"}:
        return "Server"
    if "media" in role_set:
        return "Media"
    if "workstation" in role_set:
        return "Workstation"
    if "mobile" in role_set:
        return "Mobile"
    if "iot" in role_set:
        return "IoT"
    return "Unknown"


def inventory_class(role: str) -> str:
    if role in ("Core Infrastructure", "Network Equipment", "Server"):
        return "infrastructure"
    return "client"


def observation_freshness(record: dict, now_epoch: int, stale_after: int, offline_after: int) -> tuple[str, int | None]:
    last_seen = int(record.get("last_seen_epoch") or 0)
    if record.get("_never_observed"):
        return "unobserved", None
    if not last_seen:
        return "unknown", None
    age = max(0, now_epoch - last_seen)
    if age > offline_after:
        return "expired", age
    if age > stale_after:
        return "stale", age
    return "recent", age


def device_status(record: dict, health_status: str) -> str:
    if is_operationally_monitored(record):
        return "online" if health_status in ("healthy", "watch") else health_status
    observation_status = record.get("observation_status")
    if observation_status == "stale":
        return "stale"
    if observation_status in ("expired", "unknown", "unobserved") or is_dhcp_assignment_only(record):
        return "unknown"
    return "online" if health_status in ("healthy", "watch") else health_status


def health_score(record: dict, now_epoch: int, stale_after: int, offline_after: int) -> tuple[int, str, list[str]]:
    reasons = []
    score = 100
    last_seen = int(record.get("last_seen_epoch") or 0)
    if record.get("_never_observed"):
        return 0, "offline", ["not yet observed by passive discovery"]
    age = now_epoch - last_seen if last_seen else offline_after + 1
    if not is_operationally_monitored(record):
        if age > offline_after:
            return 75, "watch", ["passive observation expired; operational availability unknown"]
        if age > stale_after:
            return 75, "watch", ["last seen is stale; operational availability unknown"]
        if is_dhcp_assignment_only(record):
            return 75, "watch", ["DHCP assignment observed; operational availability unknown"]
        return score, "healthy", reasons
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


def _record_key(record: dict) -> str:
    if record.get("_merge_key"):
        return record["_merge_key"]
    return normalize_mac(record.get("mac", "")) or record.get("ip") or normalize_hostname(record.get("hostname")) or record.get("_configured_id") or record.get("name", "")


def _merge_record_values(records: list[dict]) -> dict:
    observed_records = [record for record in records if record.get("_observed", True)]
    known_records = [record for record in records if not record.get("_observed", True)]
    merged = {}
    sources = set()
    for record in observed_records + known_records:
        if record.get("source"):
            sources.add(record["source"])
        sources.update(record.get("sources", []))
    for record in observed_records:
        for key, value in record.items():
            if key.startswith("_") or value in ("", None, []):
                continue
            merged[key] = value
    for record in known_records:
        for key in ("mac", "ip", "hostname"):
            if record.get(key) and not merged.get(key):
                merged[key] = record[key]
        for key in record.get("_known_metadata_fields", []):
            value = record.get(key)
            if value not in ("", None, []):
                merged[key] = value
        if record.get("_configured_id") and not merged.get("_configured_id"):
            merged["_configured_id"] = record["_configured_id"]
    if sources:
        merged["sources"] = sorted(sources)
    merged["_observed"] = bool(observed_records)
    return merged


WEAK_IDENTITY_METADATA_FIELDS = {
    "area",
    "hostname",
    "location",
    "model",
    "name",
    "notes",
    "parent_device_id",
    "parent_id",
    "parent_ip",
    "parent_mac",
    "uplink_ip",
    "uplink_mac",
    "vendor",
}
RETAINED_STRONG_METADATA_FIELDS = WEAK_IDENTITY_METADATA_FIELDS | {
    "firmware",
    "interface",
    "interfaces",
    "role",
    "roles",
    "type",
}


def _weak_identity_metadata(record: dict) -> dict:
    metadata = {}
    for field in WEAK_IDENTITY_METADATA_FIELDS:
        value = record.get(field)
        if value in ("", None, []):
            continue
        if field == "name" and value in (record.get("ip"), record.get("id")):
            continue
        metadata[field] = value
    sources = _record_sources(record)
    if sources:
        metadata["sources"] = sorted(sources)
    metadata["_observed"] = record.get("_observed", True)
    return metadata


def _group_identities_by_ip(by_key: dict) -> dict:
    identities = {}
    for key, grouped_records in by_key.items():
        ips = {str(record.get("ip", "")).strip() for record in grouped_records if str(record.get("ip", "")).strip()}
        macs = {normalize_mac(record.get("mac", "")) for record in grouped_records}
        macs.discard("")
        for ip in ips:
            entry = identities.setdefault(ip, {"weak_keys": set(), "strong_keys": set(), "macs": set()})
            if macs:
                entry["strong_keys"].add(key)
                entry["macs"].update(macs)
            else:
                entry["weak_keys"].add(key)
    return identities


def _reconcile_current_weak_identities(by_key: dict) -> None:
    for ip, identities in _group_identities_by_ip(by_key).items():
        weak_keys = identities["weak_keys"]
        strong_keys = identities["strong_keys"]
        macs = identities["macs"]
        if len(macs) > 1 or len(strong_keys) > 1:
            LOG.warning("inventory identity reconciliation skipped ip=%s reason=multiple_mac_identities", ip)
            continue
        if not weak_keys:
            continue
        if len(weak_keys) != 1 or len(strong_keys) != 1:
            if strong_keys:
                LOG.warning("inventory identity reconciliation skipped ip=%s reason=ambiguous_weak_identity", ip)
            continue
        weak_key = next(iter(weak_keys))
        strong_key = next(iter(strong_keys))
        if weak_key == strong_key:
            continue
        weak_metadata = [_weak_identity_metadata(record) for record in by_key.pop(weak_key)]
        by_key[strong_key] = weak_metadata + by_key[strong_key]


def _current_weak_as_retained_strong(weak_records: list[dict], strong: dict) -> dict:
    weak = _merge_record_values(weak_records)
    canonical = {
        "ip": strong["ip"],
        "mac": normalize_mac(strong.get("mac", "")),
        "_observed": True,
    }
    for field in RETAINED_STRONG_METADATA_FIELDS:
        strong_value = strong.get(field)
        weak_value = weak.get(field)
        if field == "name" and strong_value in (strong.get("ip"), strong.get("id")):
            strong_value = ""
        if strong_value not in ("", None, []):
            canonical[field] = strong_value
        elif weak_value not in ("", None, []):
            canonical[field] = weak_value
    sources = _record_sources(strong) | _record_sources(weak)
    if sources:
        canonical["sources"] = sorted(sources)
    if weak.get("last_seen_source"):
        canonical["last_seen_source"] = weak["last_seen_source"]
    return canonical


def _reconcile_current_weak_with_retained_strong(by_key: dict, previous_devices: list[dict]) -> None:
    current_by_ip = _group_identities_by_ip(by_key)
    previous_by_ip = {}
    for device in previous_devices:
        ip = str(device.get("ip", "")).strip()
        if ip:
            previous_by_ip.setdefault(ip, []).append(device)
    for ip, identities in current_by_ip.items():
        weak_keys = identities["weak_keys"]
        if not weak_keys:
            continue
        retained_strong = [
            device
            for device in previous_by_ip.get(ip, [])
            if normalize_mac(device.get("mac", ""))
        ]
        retained_macs = {normalize_mac(device.get("mac", "")) for device in retained_strong}
        retained_ids = {
            device.get("id") or stable_device_id(device)
            for device in retained_strong
        }
        if identities["strong_keys"]:
            if retained_macs and retained_macs != identities["macs"]:
                LOG.warning("inventory identity reconciliation skipped ip=%s reason=conflicting_current_and_retained_macs", ip)
            continue
        if len(weak_keys) != 1:
            if retained_strong:
                LOG.warning("inventory identity reconciliation skipped ip=%s reason=multiple_current_weak_identities", ip)
            continue
        if len(retained_macs) > 1 or len(retained_ids) > 1:
            LOG.warning("inventory identity reconciliation skipped ip=%s reason=multiple_retained_mac_identities", ip)
            continue
        if not retained_strong:
            continue
        weak_key = next(iter(weak_keys))
        strong = retained_strong[0]
        strong_key = normalize_mac(strong.get("mac", ""))
        if strong_key in by_key and strong_key != weak_key:
            LOG.warning("inventory identity reconciliation skipped ip=%s reason=retained_mac_observed_at_another_ip", ip)
            continue
        canonical = _current_weak_as_retained_strong(by_key.pop(weak_key), strong)
        by_key[strong_key] = [canonical]


def _valid_first_seen(record: dict) -> tuple[float, str] | None:
    value = record.get("first_seen")
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
        return parsed.timestamp(), value
    except (ValueError, OSError):
        return None


def _earliest_first_seen(default: str, *records: dict) -> str:
    valid = [item for item in (_valid_first_seen(record) for record in records) if item]
    if valid:
        return min(valid, key=lambda item: item[0])[1]
    return next((record["first_seen"] for record in records if record.get("first_seen")), default)


def _retained_weak_reconciliations(by_key: dict, previous_devices: list[dict]) -> dict[str, dict]:
    current_by_ip = _group_identities_by_ip(by_key)
    previous_by_ip = {}
    for device in previous_devices:
        ip = str(device.get("ip", "")).strip()
        if ip:
            previous_by_ip.setdefault(ip, []).append(device)
    reconciliations = {}
    for ip, identities in current_by_ip.items():
        if len(identities["strong_keys"]) != 1 or len(identities["macs"]) != 1:
            continue
        current_mac = next(iter(identities["macs"]))
        previous = previous_by_ip.get(ip, [])
        weak = [device for device in previous if not normalize_mac(device.get("mac", ""))]
        conflicting_macs = {
            normalize_mac(device.get("mac", ""))
            for device in previous
            if normalize_mac(device.get("mac", "")) not in ("", current_mac)
        }
        if conflicting_macs:
            if weak:
                LOG.warning("inventory identity reconciliation skipped ip=%s reason=conflicting_retained_mac", ip)
            continue
        if len(weak) > 1:
            LOG.warning("inventory identity reconciliation skipped ip=%s reason=ambiguous_retained_weak_identity", ip)
            continue
        if len(weak) == 1:
            reconciliations[next(iter(identities["strong_keys"]))] = weak[0]
    return reconciliations


def _merge_retained_weak_identity(record: dict, weak: dict) -> None:
    for field, value in _weak_identity_metadata(weak).items():
        if field.startswith("_") or field in ("source", "sources"):
            continue
        if record.get(field) in ("", None, []):
            record[field] = value
    sources = _record_sources(record) | _record_sources(weak)
    if sources:
        record["sources"] = sorted(sources)


def merge_records(records: list[dict], previous: dict, now: str, now_epoch: int, config: dict) -> list[dict]:
    by_key = {}
    for record in records:
        key = _record_key(record)
        if not key:
            continue
        by_key.setdefault(key, []).append(record)
    previous_devices = previous.get("devices", [])
    _reconcile_current_weak_with_retained_strong(by_key, previous_devices)
    _reconcile_current_weak_identities(by_key)
    retained_reconciliations = _retained_weak_reconciliations(by_key, previous_devices)
    reconciled_previous_ids = {
        record.get("id") for record in retained_reconciliations.values() if record.get("id")
    }
    prev_by_id = {item.get("id"): item for item in previous_devices if item.get("id")}
    stale_after = int(config.get("HIOC_INVENTORY_STALE_AFTER_SEC", "900"))
    offline_after = int(config.get("HIOC_INVENTORY_OFFLINE_AFTER_SEC", "3600"))
    devices = []
    for key, grouped_records in by_key.items():
        record = _merge_record_values(grouped_records)
        observed = record.pop("_observed", True)
        record["mac"] = normalize_mac(record.get("mac", ""))
        record["id"] = stable_device_id(record)
        prev = prev_by_id.get(record["id"], {})
        retained_weak = retained_reconciliations.get(key, {})
        if retained_weak:
            _merge_retained_weak_identity(record, retained_weak)
        if observed:
            record["first_seen"] = _earliest_first_seen(now, prev, retained_weak)
            record["last_seen"] = now
            record["last_seen_epoch"] = now_epoch
        else:
            if prev.get("first_seen"):
                record["first_seen"] = prev["first_seen"]
            if prev.get("last_seen"):
                record["last_seen"] = prev["last_seen"]
            if prev.get("last_seen_epoch"):
                record["last_seen_epoch"] = prev["last_seen_epoch"]
            if not prev.get("last_seen_epoch"):
                record["_never_observed"] = True
        record["display_name"] = record.get("name") or record.get("hostname") or record.get("ip") or record["id"]
        record["name"] = record["display_name"]
        record.setdefault("vendor", "")
        record.setdefault("role", operator_role(record, record.get("roles", [])))
        record["inventory_class"] = inventory_class(record["role"])
        record["source"] = ", ".join(record.get("sources", [])) if record.get("sources") else record.get("source", "unknown")
        record["operationally_monitored"] = is_operationally_monitored(record)
        observation_status, observation_age = observation_freshness(record, now_epoch, stale_after, offline_after)
        record["observation_status"] = observation_status
        record["observation_age_seconds"] = observation_age
        score, status, reasons = health_score(record, now_epoch, stale_after, offline_after)
        record["health_score"] = score
        record["health_status"] = status
        record["health"] = status
        record["status"] = device_status(record, status)
        record["health_reasons"] = reasons
        devices.append(record)
    seen_ids = {d["id"] for d in devices}
    for old in previous_devices:
        if old.get("id") not in seen_ids and old.get("id") not in reconciled_previous_ids:
            if not normalize_mac(old.get("mac", "")) and _record_sources(old) == {"arp_table"}:
                LOG.debug("legacy unresolved neighbor removed ip=%s provenance=arp_table", old.get("ip", ""))
                continue
            record = dict(old)
            record.setdefault("display_name", record.get("name") or record.get("ip") or record.get("id", "unknown device"))
            record.setdefault("name", record.get("display_name", "unknown device"))
            record.setdefault("ip", "")
            record.setdefault("mac", "")
            record.setdefault("vendor", "")
            record.setdefault("source", record.get("last_seen_source", "previous_inventory"))
            record.setdefault("last_seen", "unknown")
            record.setdefault("role", operator_role(record, record.get("roles", [])))
            record.setdefault("inventory_class", inventory_class(record["role"]))
            record["operationally_monitored"] = is_operationally_monitored(record)
            observation_status, observation_age = observation_freshness(record, now_epoch, stale_after, offline_after)
            record["observation_status"] = observation_status
            record["observation_age_seconds"] = observation_age
            score, status, reasons = health_score(record, now_epoch, stale_after, offline_after)
            record["health_score"] = score
            record["health_status"] = status
            record["health"] = status
            record["status"] = device_status(record, status)
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


def resolve_configured_parent_ids(devices: list[dict]) -> None:
    by_configured_id = {
        device.get("_configured_id"): device.get("id")
        for device in devices
        if device.get("_configured_id") and device.get("id")
    }
    for device in devices:
        for field in ("parent_id", "parent_device_id"):
            value = device.get(field)
            if value in by_configured_id and by_configured_id[value] != device.get("id"):
                device[field] = by_configured_id[value]


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


def enrich_services(services: list[dict], devices: list[dict], dependencies: dict) -> list[dict]:
    devices_by_id = {device.get("id"): device for device in devices}
    dependency_by_service = {}
    for edge in dependencies.get("edges", []):
        if str(edge.get("from_id", "")).startswith("svc_"):
            dependency_by_service.setdefault(edge["from_id"], []).append(edge.get("type", "dependency"))
    enriched = []
    for service in services:
        item = dict(service)
        host = devices_by_id.get(item.get("device_id"), {})
        item["host"] = host.get("display_name") or host.get("name") or host.get("ip") or item.get("device_id", "")
        item["dependency"] = ", ".join(sorted(set(dependency_by_service.get(item.get("id"), [])))) or ""
        enriched.append(item)
    return enriched


def inventory_summary_lists(devices: list[dict], services: list[dict]) -> tuple[list[dict], list[dict]]:
    infrastructure = []
    for device in devices:
        if device.get("inventory_class") != "infrastructure":
            continue
        infrastructure.append({
            "name": device.get("display_name", device.get("id", "")),
            "ip": device.get("ip", ""),
            "mac": device.get("mac", ""),
            "vendor": device.get("vendor", ""),
            "role": device.get("role", "Unknown"),
            "status": device.get("status", device.get("health_status", "")),
            "health": device.get("health_status", ""),
            "health_score": device.get("health_score", 0),
            "last_seen": device.get("last_seen", ""),
            "source": device.get("source", ""),
        })
    service_rows = []
    for service in services:
        service_rows.append({
            "name": service.get("name", ""),
            "host": service.get("host", ""),
            "type": service.get("type", ""),
            "status": service.get("status", ""),
            "dependency": service.get("dependency", ""),
        })
    return infrastructure, service_rows


def discovery_source_status(config: dict, local_addresses: list[dict], gateway: dict) -> tuple[list[str], bool, str]:
    sources = []
    if local_addresses:
        sources.append("local_host")
    if gateway.get("ip"):
        sources.append("gateway")
    neighbors = neighbor_table()
    sources.append("arp_table" if neighbors else "arp_table_empty")
    _, lease_status = dhcp_lease_discovery(config)
    sources.append(lease_status)
    state_root = Path(config.get("HIOC_HOME", "/home/jazofv1/hioc")) / "state"
    integration_root = Path(config.get("HIOC_INVENTORY_INTEGRATION_DIR", "")) if config.get("HIOC_INVENTORY_INTEGRATION_DIR", "") else state_root / "inventory" / "integrations"
    if integration_root.exists():
        sources.append("integration_inventory")
    limited = "dhcp_leases_unavailable" in sources and not any(source == "integration_inventory" for source in sources)
    reason = "Pi-hole/dnsmasq DHCP lease files were not found; inventory is limited to local host, gateway, ARP/neigh, integrations, and prior retained devices." if limited else ""
    return sources, limited, reason


def build_inventory_summary(
    devices: list[dict],
    services: list[dict],
    topology: dict,
    dependencies: dict,
    now: str,
    discovery_sources: list[str],
    discovery_limited: bool,
    discovery_limit_reason: str,
) -> dict:
    infrastructure_count = len([d for d in devices if d.get("inventory_class") == "infrastructure"])
    client_count = len([d for d in devices if d.get("inventory_class") == "client"])
    infrastructure_devices, service_rows = inventory_summary_lists(devices, services)
    return {
        "updated": now,
        "device_count": len(devices),
        "infrastructure_count": infrastructure_count,
        "client_count": client_count,
        "network_client_count": client_count,
        "healthy_count": len([d for d in devices if d.get("health_status") == "healthy"]),
        "watch_count": len([d for d in devices if d.get("health_status") == "watch"]),
        "degraded_count": len([d for d in devices if d.get("health_status") == "degraded"]),
        "offline_count": len([d for d in devices if d.get("health_status") == "offline"]),
        "service_count": len(services),
        "topology_edges": len(topology.get("edges", [])),
        "dependency_edges": len(dependencies.get("edges", [])),
        "lowest_health_score": min([d.get("health_score", 0) for d in devices], default=0),
        "discovery_sources": discovery_sources,
        "discovery_limited": bool(discovery_limited),
        "discovery_limit_reason": discovery_limit_reason or "",
        "infrastructure_devices": infrastructure_devices,
        "services": service_rows,
    }


def discover_inventory(config: dict, previous: dict) -> dict:
    now = now_iso()
    now_epoch = int(time.time())
    local_addresses = local_ipv4_addresses()
    local_ips = {item["ip"] for item in local_addresses}
    gateway = default_gateway()
    gateway_ip = gateway.get("ip", "")
    discovery_sources, discovery_limited, discovery_limit_reason = discovery_source_status(config, local_addresses, gateway)
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
        records.append({"type": "network_device", "name": "Default Gateway", "ip": gateway_ip, "interface": gateway.get("interface", ""), "source": "gateway", "last_seen_source": "gateway"})
    state_root = Path(config.get("HIOC_HOME", "/home/jazofv1/hioc")) / "state"
    registry = DriverRegistry()
    registry.register(PassiveNetworkDriver())
    if active_discovery:
        registry.register(ActiveNetworkDriver())
    for result in registry.run(config):
        records.extend(result.devices)
    known_records = known_infrastructure(config)
    if known_records:
        discovery_sources.append(KNOWN_SOURCE)
        records = append_known_infrastructure(records, known_records)
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
        if record.get("role") in OPERATOR_ROLES:
            record["role"] = record["role"]
        else:
            record["role"] = operator_role(record, roles)
        record["inventory_class"] = inventory_class(record["role"])
        enriched.append(record)
    devices = merge_records(enriched, previous, now, now_epoch, config)
    resolve_configured_parent_ids(devices)
    local_device_id = next((d["id"] for d in devices if d.get("type") == "local_host"), devices[0]["id"] if devices else "")
    service_registry = DriverRegistry()
    service_registry.register(LocalServiceDriver(local_device_id))
    services = []
    for result in service_registry.run(config):
        services.extend(result.services)
    topology = build_topology(devices, gateway_ip, local_device_id)
    dependencies = build_dependencies(devices, services)
    services = enrich_services(services, devices, dependencies)
    capabilities = CapabilityRegistry()
    for device in devices:
        capabilities.infer_from_device(device)
    for service in services:
        capabilities.infer_from_service(service)
    capability_list = capabilities.all()
    summary = build_inventory_summary(devices, services, topology, dependencies, now, discovery_sources, discovery_limited, discovery_limit_reason)
    devices = [{key: value for key, value in device.items() if not key.startswith("_")} for device in devices]
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
