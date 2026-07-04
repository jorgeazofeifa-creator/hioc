# HIOC Milestone 1 Implementation Review

This review covers the Living Inventory implementation currently present in the workspace. No additional runtime code changes are included in this document.

## Repository Impact

### Files Created

- `IMPLEMENTATION_REVIEW.md`: production review requested before deployment.
- `DECISIONS.md`: architecture decision record for long-term consistency.
- `ROADMAP.md`: milestone tracking document.
- `docs/ARCHITECTURE.md`: documents runtime architecture and subsystem boundaries.
- `docs/PROJECT.md`: documents project principles and repository layout.
- `docs/MQTT.md`: documents retained MQTT topic contract.
- `docs/HOME_ASSISTANT.md`: documents HA package and dashboard integration.
- `docs/DATA_MODEL.md`: documents incident, forecast, and inventory payload structures.
- `docs/CHANGELOG.md`: documentation-level changelog.
- `pi4/lib/hioc/__init__.py`: Python package marker for shared HIOC modules.
- `pi4/lib/hioc/config.py`: shared configuration loader for HIOC and Pi4 toolkit config.
- `pi4/lib/hioc/runtime.py`: shared logging, subprocess, JSON, and timestamp helpers.
- `pi4/lib/hioc/mqtt.py`: shared retained MQTT publish helper.
- `pi4/lib/hioc/inventory.py`: Living Inventory discovery, normalization, health, topology, and dependency model.
- `pi4/bin/hioc-inventory-engine.py`: executable inventory engine.
- `homeassistant/packages/hioc_living_inventory.yaml`: HA MQTT/template entities for inventory.
- `homeassistant/dashboards/living_inventory.yaml`: HA dashboard for Living Inventory operations.
- `homeassistant/validate_ha.sh`: HA-side validation script.
- `tests/test_inventory.py`: unit tests for inventory identity, health, topology, dependencies, and retention.
- `tests/test_homeassistant_yaml.py`: HA YAML parse validation test when PyYAML is available.

### Files Modified

- `README.md`: adds summary of Living Inventory and architecture documents.
- `CHANGELOG.md`: adds Unreleased section for Living Inventory.
- `docs/INSTALL.md`: adds inventory cron behavior, optional config, HA validation, and rollback files.
- `pi4/config/hioc.conf.example`: adds inventory discovery and timing configuration.
- `pi4/install_pi4.sh`: creates inventory state directory, installs executable, adds inventory cron, runs first inventory pass.
- `pi4/uninstall_pi4.sh`: removes current incident, history, and inventory cron entries.
- `pi4/validate_pi4.sh`: validates inventory executable, cron entry, and generated JSON.
- `homeassistant/install_ha.sh`: installs dashboard YAML files and points to HA validation.

### Files Deleted

- None.

## Runtime

### New Executable

- `pi4/bin/hioc-inventory-engine.py`
  - Loads HIOC/Pi4 config.
  - Discovers devices, services, topology, and dependencies using passive sources by default.
  - Writes local JSON state under `state/inventory`.
  - Publishes retained MQTT inventory payloads.
  - Logs to `logs/hioc-inventory-engine.log`.
  - Publishes inventory topics over one persistent MQTT connection per run.
  - Returns error only for engine failures. MQTT publish failures mark status degraded in JSON and log the failure.

### New Cron Job

```text
*/30 * * * * flock -n /tmp/hioc-inventory-engine.lock $INSTALL_DIR/pi4/bin/hioc-inventory-engine.py
```

- Frequency: every 30 minutes.
- Locking: `flock` prevents overlapping runs.
- Added by: `pi4/install_pi4.sh`.
- Removed by: `pi4/uninstall_pi4.sh`.

### New MQTT Topics

- `home/infrastructure/hioc/inventory`
- `home/infrastructure/hioc/inventory/devices`
- `home/infrastructure/hioc/inventory/services`
- `home/infrastructure/hioc/inventory/topology`
- `home/infrastructure/hioc/inventory/dependencies`
- `home/infrastructure/hioc/inventory/summary`
- `home/infrastructure/hioc/inventory/status`

All are retained publications.

### New JSON Files

Created under `$HIOC_HOME/state/inventory`:

- `inventory.json`: full inventory root object.
- `devices.json`: device list.
- `services.json`: service list.
- `topology.json`: parent/child topology graph.
- `dependencies.json`: service dependency graph.
- `summary.json`: aggregate counts and health summary.
- `status.json`: engine status, schema version, update time, and publish errors when present.

### Configuration Added or Modified

Modified `pi4/config/hioc.conf.example`:

- `HIOC_INVENTORY_SCAN_SUBNET`
- `HIOC_INVENTORY_ACTIVE_DISCOVERY`
- `HIOC_INVENTORY_PING_COUNT`
- `HIOC_INVENTORY_PING_TIMEOUT_SEC`
- `HIOC_INVENTORY_STALE_AFTER_SEC`
- `HIOC_INVENTORY_OFFLINE_AFTER_SEC`
- `HIOC_INVENTORY_SNMP_COMMUNITY`
- `HIOC_INVENTORY_INTEGRATION_DIR`

Shared loader reads:

- `$PI4_TOOLS_HOME/config/toolkit.conf`
- `$HIOC_HOME/config/hioc.conf`
- environment variables starting with `HIOC_` or `MQTT_`

## Home Assistant

### Package Added

- `homeassistant/packages/hioc_living_inventory.yaml`

### Dashboard Added

- `homeassistant/dashboards/living_inventory.yaml`

### MQTT Entities Created

- `sensor.hioc_inventory_status`
- `sensor.hioc_inventory_device_count`
- `sensor.hioc_inventory_healthy_devices`
- `sensor.hioc_inventory_watch_devices`
- `sensor.hioc_inventory_degraded_devices`
- `sensor.hioc_inventory_offline_devices`
- `sensor.hioc_inventory_lowest_health`
- `sensor.hioc_inventory_service_count`
- `sensor.hioc_inventory_topology_edges`
- `sensor.hioc_inventory_dependency_edges`
- `sensor.hioc_inventory_devices`
- `sensor.hioc_inventory_services`

### Template Sensors Added

- `sensor.hioc_inventory_operations_summary`
- `sensor.hioc_inventory_recommended_action`

### Binary Sensors Added

- `binary_sensor.hioc_inventory_healthy`

### Automations Added

- None.

## Networking

### Discovery Commands

- `ip -o -4 addr show`: passive local interface read.
- `cat /sys/class/net/<interface>/address`: passive local MAC read.
- `ip route show default`: passive local route read.
- `ip neigh show`: passive neighbor table read.
- `arp -an`: passive fallback neighbor table read.
- `ping -c <count> -W <timeout> <ip>`: active reachability probe only when `HIOC_INVENTORY_ACTIVE_DISCOVERY=on`.
- `nmap -sn <subnet>`: active subnet discovery only when `HIOC_INVENTORY_ACTIVE_DISCOVERY=on`, `HIOC_INVENTORY_SCAN_SUBNET` is configured, and `nmap` exists.
- `systemctl list-units --type=service --all --no-pager --plain`: passive local service inventory.
- `ss -ltnup`: passive local listening socket inventory.
- `dpkg-query -W -f=${Version} <package>`: passive local package version read.
- `snmpget -v2c -c <community> -Oqv <ip> 1.3.6.1.2.1.1.1.0`: active SNMP firmware/system description read only when active discovery and SNMP community are configured.
- Persistent Python socket MQTT connection: active MQTT publication, one connection per run.

### Active Network Operations

#### Ping

- Frequency: every inventory run only when active discovery is enabled, currently every 30 minutes by default.
- Timeout: `HIOC_INVENTORY_PING_TIMEOUT_SEC`, default 1 second per target.
- Count: `HIOC_INVENTORY_PING_COUNT`, default 1 packet.
- Bandwidth impact: very low, one ICMP echo request/reply per observed non-local IP.
- CPU impact: low, proportional to observed device count.

#### Nmap Ping Sweep

- Frequency: every inventory run only when active discovery is enabled and `HIOC_INVENTORY_SCAN_SUBNET` is set.
- Timeout: engine command timeout is 90 seconds.
- Scope guard: subnet larger than 1024 addresses is skipped.
- Bandwidth impact: low to medium depending on subnet size.
- CPU impact: low to medium during scan.
- Deployment note: should be reviewed before enabling on constrained or sensitive networks.

#### SNMP

- Frequency: every inventory run only when active discovery is enabled and `HIOC_INVENTORY_SNMP_COMMUNITY` is configured.
- Timeout: 4 seconds per target.
- Bandwidth impact: very low per target.
- CPU impact: low, but worst-case execution grows with device count and SNMP timeouts.

#### MQTT Publish

- Frequency: every inventory run, currently every 30 minutes by default.
- Timeout: 8 seconds for MQTT connection and socket operations.
- Topics: seven retained inventory publications.
- Bandwidth impact: low to medium depending on device list size.
- CPU impact: low.

## Discovery

### Device Discovery

Devices are discovered from:

- Local Pi4 host identity and interfaces.
- Default gateway route.
- Kernel neighbor table.
- ARP fallback.
- Pi-hole/dnsmasq/dhcp lease files when available.
- Integration hint JSON files when available.
- Optional configured subnet scan only when active discovery is enabled.
- Previously observed inventory devices, retained and marked stale/offline according to thresholds.

### MAC Address Discovery

MAC addresses are obtained from:

- `/sys/class/net/<interface>/address` for local interfaces.
- `ip neigh show` or `arp -an` for neighbor devices.
- DHCP lease files for leased devices.
- `nmap -sn` output when active discovery and active scan are enabled.

### Firmware Discovery

Firmware/system version is obtained from:

- `/etc/os-release` for local OS.
- kernel release from `os.uname`.
- `dpkg-query` for local `mosquitto` and `pihole-FTL` package versions.
- optional SNMP `sysDescr` for reachable network devices when active discovery and community are configured.

### Service Detection

Services are detected from:

- `systemctl list-units` for known service units.
- `ss -ltnup` for listening ports.

Recognized service types include MQTT, DNS, DHCP, UPS, SSH, and scheduler services.

### Dependency Inference

Dependencies are inferred from service types:

- Healthy devices depend on detected DNS services.
- Healthy devices depend on detected DHCP services.
- Healthy devices depend on detected MQTT services.
- MQTT service depends on DNS when both are detected.

This is deterministic inference from local inventory, not packet-level service tracing.

### Topology Generation

Topology is generated from:

- Default gateway as root when available.
- Otherwise local collector as root.
- Integration-provided parent hints such as parent ID, parent MAC, parent IP, uplink MAC, or uplink IP.
- Intermediate infrastructure devices such as Orbi satellites, mesh nodes, access points, and switches when detected by hostname/vendor/model or integration hints.
- Endpoints attach to the single discovered intermediate infrastructure device when there is exactly one. Otherwise they attach to explicit hints or the root.

This remains an inferred topology. It can represent intermediate infrastructure when integrations provide enough hints, but it is not packet-level physical topology discovery.

## Performance

### Estimated Normal Case

- CPU usage: low, brief spikes during command execution.
- Memory usage: low, expected under 50 MB for typical home inventory.
- Disk usage: low, JSON state typically KB to low MB depending on device count.
- MQTT traffic: seven retained publishes every 30 minutes over one connection.
- Network traffic: none for discovery by default beyond local/passive reads. Ping, reverse DNS, SNMP, and nmap occur only when active discovery is enabled.
- Execution time: expected under a few seconds with passive discovery.

### Worst Case

- Worst-case discovery time can approach or exceed 90 seconds only with active discovery, configured subnet scan, plus SNMP timeouts.
- Ping fallback for up to 1024 addresses can also be slow if `nmap` is unavailable and active subnet scan is enabled.
- MQTT failure can add up to the connection timeout for one persistent connection, though local state still writes first.

## Failure Modes

### MQTT Unavailable

Inventory JSON is still written locally. Status is marked degraded with publish errors. Engine logs the failure and exits without failing the cron run.

### Pi-hole Unavailable

DHCP lease discovery from Pi-hole may be unavailable. Inventory falls back to local host facts, route, neighbor table, ARP, previous inventory state, and optional subnet scan.

### Gateway Unavailable

Default route may still identify the gateway IP, but ping reachability can fail. Gateway device health may degrade/offline based on last-seen and reachability.

### SNMP Disabled

No SNMP firmware fields are collected for network devices. Core inventory still works.

### ARP Cache Empty

Neighbor discovery returns few or no devices. Inventory falls back to leases, route, optional scan, and previous inventory.

### DHCP Leases Unavailable

Lease-based MAC/hostname discovery is skipped. Inventory falls back to neighbor table, route, optional scan, and previous inventory.

### Home Assistant Offline

MQTT retained topics still publish if broker is online. HA receives latest state when it comes back. If HA and broker are both unavailable, local JSON remains the source of truth.

## Security Review

### Credentials Used

- MQTT credentials from toolkit/HIOC config:
  - `MQTT_HOST`
  - `MQTT_PORT`
  - `MQTT_USER`
  - `MQTT_PASSWORD`
- SNMP community:
  - `HIOC_INVENTORY_SNMP_COMMUNITY`

### Shell Commands and Subprocesses

Every subprocess executed by inventory modules:

- `ip -o -4 addr show`
- `cat /sys/class/net/<interface>/address`
- `ip route show default`
- `ip neigh show`
- `arp -an`
- `ping -c <count> -W <timeout> <ip>`
- `nmap -sn <subnet>`
- `systemctl list-units --type=service --all --no-pager --plain`
- `ss -ltnup`
- `dpkg-query -W -f=${Version} mosquitto`
- `dpkg-query -W -f=${Version} pihole-FTL`
- `snmpget -v2c -c <community> -Oqv <ip> 1.3.6.1.2.1.1.1.0`
- Python socket connection to the configured MQTT broker.

### Files Written

- `$HIOC_HOME/state/inventory/inventory.json`
- `$HIOC_HOME/state/inventory/devices.json`
- `$HIOC_HOME/state/inventory/services.json`
- `$HIOC_HOME/state/inventory/topology.json`
- `$HIOC_HOME/state/inventory/dependencies.json`
- `$HIOC_HOME/state/inventory/summary.json`
- `$HIOC_HOME/state/inventory/status.json`
- `$HIOC_HOME/logs/hioc-inventory-engine.log`

Installer and validation scripts also write or copy:

- `$INSTALL_DIR` tree during install.
- `$INSTALL_DIR/config/hioc.conf` if missing.
- `$INSTALL_DIR/state/inventory`.
- `/config/packages/*.yaml` during HA install.
- `/config/dashboards/*.yaml` during HA install.
- backup files under HIOC/HA backup directories.
- current user crontab.

### External Commands

External command requirements or optional use:

- Required for existing Pi4 install: `jq`, `mosquitto_pub`, `mosquitto_sub`, `flock`, `python3`.
- Used by inventory engine when present/configured: `ip`, `cat`, `arp`, `ping`, `nmap`, `systemctl`, `ss`, `dpkg-query`, `snmpget`.

### Privileges Required

- Normal user access to run local commands and read public system files.
- Permission to read DHCP lease files if present.
- Permission to run `systemctl` and `ss`.
- Permission to update user crontab during install.
- HA installer requires write access to `/config/packages` and `/config/dashboards`.
- No root-only operation is intentionally required by the inventory engine, but some system files may be unavailable without appropriate permissions.

## Production Risks

- Low: Active subnet scanning is disabled by default.
- Medium: Active subnet scanning can increase network noise if explicitly enabled on large or sensitive networks.
- Medium: SNMP timeout per target can increase runtime when many devices do not respond.
- Medium: Topology is logical gateway-parent topology, not physical switch/AP topology.
- Medium: Dependency graph is inferred from service type, not observed client traffic.
- Medium: Home Assistant dashboard uses JSON attributes that may become large in bigger environments.
- Low: Living Inventory now uses a persistent MQTT client abstraction for all inventory topics in a run.
- Low: Missing Pi-hole leases reduce discovery richness but do not break inventory.
- Low: Missing SNMP reduces firmware data but does not break inventory.
- Low: Missing `nmap` falls back to ping sweep only when active subnet scan is configured.
- High: If `HIOC_INVENTORY_SCAN_SUBNET` is set too broadly, scan duration and traffic can become unacceptable, though the implementation skips networks larger than 1024 addresses.
- High: Current HA notification target in the existing incident package remains hardcoded outside this milestone.
- Medium: HA YAML parse test is skipped when PyYAML is unavailable in the local test runtime.
- Medium: Shell scripts were not syntax-checked with Bash in the Windows review environment because Bash was unavailable on PATH.

## Deployment Checklist

1. Review this document and confirm active discovery policy.
2. On the Pi4, confirm existing Pi4 toolkit config exists at `/home/jazofv1/pi4-tools/config/toolkit.conf`.
3. Confirm required commands are installed: `python3`, `jq`, `mosquitto_pub`, `mosquitto_sub`, and `flock`.
4. Keep `HIOC_INVENTORY_ACTIVE_DISCOVERY=off` for the initial passive deployment.
5. Decide whether to enable active subnet discovery later. Leave `HIOC_INVENTORY_SCAN_SUBNET` empty for passive-first deployment.
6. Decide whether to configure SNMP later. Leave `HIOC_INVENTORY_SNMP_COMMUNITY` empty unless network devices are intentionally configured for SNMP.
7. Run `bash pi4/install_pi4.sh` on the Pi4.
8. Run `bash pi4/validate_pi4.sh`.
9. Inspect `$HIOC_HOME/state/inventory/summary.json`.
10. Inspect `$HIOC_HOME/state/inventory/devices.json`.
11. Confirm MQTT retained topics under `home/infrastructure/hioc/inventory`.
12. On Home Assistant, run `bash homeassistant/install_ha.sh`.
13. Run `bash homeassistant/validate_ha.sh`.
14. Run `ha core check`.
15. Restart Home Assistant after validation passes.
16. Open the Living Inventory dashboard.
17. Confirm device counts, services, topology edge count, dependency edge count, and recommended action.
18. Monitor `logs/hioc-inventory-engine.log` for the first 24 hours.
19. If active scan is enabled later, verify runtime and network impact before leaving it enabled permanently.
