# HIOC Installation

## Document Ownership

This document owns installation, configuration, dependencies, deployment, upgrade, validation, and rollback instructions.

It should not contain roadmap, architecture rationale, release history, or dashboard design. For release packaging workflow, see [RELEASE.md](RELEASE.md). For project direction, see [HIOC_MASTER_PLAN.md](HIOC_MASTER_PLAN.md).

## Repository and Runtime Layout

The authoritative source checkout is:

```text
/home/jazofv1/hioc-release-source
```

The deployed production runtime is:

```text
/home/jazofv1/hioc
```

Git operations, development, validation, release preparation, and release execution originate from the authoritative source checkout. The production runtime contains persistent runtime state and installer-managed changes and must not be treated as a clean development checkout.

The deployed runtime is not the normal location for Git development or upgrade operations. Do not use direct `git pull` operations inside `/home/jazofv1/hioc` as the standard production upgrade method. Use the supported release workflow from the authoritative source checkout or a validated release package.

For governance, see [HIOC_MASTER_PLAN.md](HIOC_MASTER_PLAN.md). For release packaging and workflow, see [RELEASE.md](RELEASE.md). The accepted architecture decision is recorded in [../DECISIONS.md](../DECISIONS.md#adr-0013-development-checkout-and-production-runtime-have-separate-roles).

## Pi4

```bash
git clone https://github.com/jorgeazofeifa-creator/hioc.git /home/jazofv1/hioc-release-source
cd /home/jazofv1/hioc-release-source
bash release/validate.sh
bash release/install.sh pi4
/home/jazofv1/hioc/pi4/bin/hioc-validate-mqtt.py
```

The Pi4 release installer invokes `pi4/install_pi4.sh` and installs to `/home/jazofv1/hioc` by default. It requires `rsync`, `crontab`, `flock`, `python3`, and the existing Pi4 toolkit configuration. Set `HIOC_INSTALL_DIR` or `PI4_TOOLS_DIR` only when intentionally using nondefault paths.

The installer uses the existing Pi4 toolkit configuration at:

```text
/home/jazofv1/pi4-tools/config/toolkit.conf
```

It adds cron entries for:

- incident engine every minute
- history engine every five minutes
- Living Inventory engine every 30 minutes
- platform status publisher daily at 03:17

Optional Living Inventory settings can be added to `/home/jazofv1/hioc/config/hioc.conf`:

```text
HIOC_INVENTORY_SCAN_SUBNET=""
HIOC_INVENTORY_ACTIVE_DISCOVERY="off"
HIOC_INVENTORY_PING_COUNT="1"
HIOC_INVENTORY_PING_TIMEOUT_SEC="1"
HIOC_INVENTORY_STALE_AFTER_SEC="900"
HIOC_INVENTORY_OFFLINE_AFTER_SEC="3600"
HIOC_INVENTORY_SNMP_COMMUNITY=""
HIOC_INVENTORY_INTEGRATION_DIR=""
HIOC_INVENTORY_DHCP_LEASE_FILES="/etc/pihole/dhcp.leases,/var/lib/misc/dnsmasq.leases,/var/lib/dhcp/dhcpd.leases"
HIOC_INVENTORY_KNOWN_INFRASTRUCTURE_FILE="/home/jazofv1/hioc/config/inventory/known_infrastructure.json"
```

Leave `HIOC_INVENTORY_ACTIVE_DISCOVERY` set to `off` for the currently approved passive discovery mode from host facts, default route, neighbor table, DHCP leases, integration hint files, and optional known infrastructure definitions.

`HIOC_INVENTORY_DHCP_LEASE_FILES` is an ordered, comma-separated list of local lease files. HIOC reads these files passively and reports whether records were found or the sources were empty, missing, unreadable, malformed, affected by an I/O error, or only partially usable. A lease is assignment metadata and does not prove reachability or refresh a device's positive-observation timestamp.

If Pi-hole's lease file exists but the HIOC service account cannot read it, grant only that account read access and verify it explicitly. For example, run the following manually with the actual service account substituted for `hioc-user`:

```bash
sudo setfacl -m u:hioc-user:r-- /etc/pihole/dhcp.leases
sudo -u hioc-user test -r /etc/pihole/dhcp.leases
```

HIOC does not change lease-file ownership or permissions during installation. Package upgrades or file replacement can remove a file ACL, so re-run validation after Pi-hole upgrades. If ACL persistence is required, manage it through the host's approved system policy rather than broadening the file's permissions.

Active-discovery configuration may exist, but operational use is governed by [HIOC_MASTER_PLAN.md](HIOC_MASTER_PLAN.md) and should not be enabled until the planned Phase 7B Safe Active Discovery work is explicitly approved.

To enrich inventory with operator-owned infrastructure metadata, create `/home/jazofv1/hioc/config/inventory/known_infrastructure.json`:

```json
{
  "devices": [
    {
      "id": "gateway",
      "name": "Internet Gateway",
      "ip": "192.168.1.1",
      "mac": "aa:bb:cc:dd:ee:ff",
      "role": "Network Equipment",
      "type": "gateway",
      "vendor": "Huawei",
      "model": "Gateway",
      "location": "Network closet",
      "enabled": true
    }
  ]
}
```

The file is optional. A missing default file does not fail inventory. Set `HIOC_INVENTORY_KNOWN_INFRASTRUCTURE_FILE=""` to disable this source explicitly.

## Home Assistant

From the Home Assistant terminal after deploying or copying the validated Home Assistant files:

```bash
cd /config/hioc
bash homeassistant/install_ha.sh
bash homeassistant/validate_ha.sh
ha core check
ha core restart
```

## Release Install

From the authoritative source checkout:

```bash
cd /home/jazofv1/hioc-release-source
bash release/validate.sh
bash release/install.sh
```

For an upgrade:

```bash
cd /home/jazofv1/hioc-release-source
bash release/validate.sh
bash release/upgrade.sh
/home/jazofv1/hioc/pi4/bin/hioc-validate-mqtt.py
```

The final command performs bounded, read-only validation of the deployed
retained Incident Engine MQTT contract using the existing toolkit and HIOC
configuration. Preserve its output and exit status as post-install or
post-upgrade evidence. See [MQTT.md](MQTT.md#operational-validation) for
preconditions, checked topics, and PASS, FAIL, and INCOMPLETE semantics.

The upgrade preserves the existing `state`, `history`, `logs`, and `backups` directories. Before copying the validated release, it records the replaceable installation content, including configuration, under a timestamped directory in `/home/jazofv1/hioc/backups`.

Use the latest recorded upgrade backup for rollback:

```bash
cd /home/jazofv1/hioc-release-source
bash release/rollback.sh
```

To select a specific validated backup, pass its path:

```bash
cd /home/jazofv1/hioc-release-source
bash release/rollback.sh /home/jazofv1/hioc/backups/release-upgrade-YYYYMMDD-HHMMSS
```

The same release commands may be run from a validated versioned release package. Do not use direct Git updates inside `/home/jazofv1/hioc` as the standard production upgrade path.

Then enable notifications:

```text
input_boolean.hioc_incident_notifications
```

The Home Assistant installer copies packages into `/config/packages` and dashboard YAML into `/config/dashboards`.

## Rollback

On Pi4:

```bash
bash ~/hioc/pi4/uninstall_pi4.sh
```

On Home Assistant, remove:

```text
/config/packages/hioc_incident_center.yaml
/config/packages/hioc_predictive_analytics.yaml
/config/packages/hioc_living_inventory.yaml
/config/packages/hioc_platform.yaml
/config/dashboards/living_inventory.yaml
/config/dashboards/hioc_dashboard_v2.yaml
```

Then run:

```bash
ha core check
ha core restart
```
