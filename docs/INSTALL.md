# HIOC Installation

## Document Ownership

This document owns installation, configuration, dependencies, deployment, upgrade, validation, and rollback instructions.

It should not contain roadmap, architecture rationale, release history, or dashboard design. For release packaging workflow, see [RELEASE.md](RELEASE.md). For project direction, see [HIOC_MASTER_PLAN.md](HIOC_MASTER_PLAN.md).

## Pi4

```bash
git clone https://github.com/jorgeazofeifa-creator/hioc.git ~/hioc
cd ~/hioc
bash pi4/install_pi4.sh
bash pi4/validate_pi4.sh
```

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
HIOC_INVENTORY_KNOWN_INFRASTRUCTURE_FILE="/home/jazofv1/hioc/config/inventory/known_infrastructure.json"
```

Leave `HIOC_INVENTORY_ACTIVE_DISCOVERY` set to `off` for the currently approved passive discovery mode from host facts, default route, neighbor table, DHCP leases, integration hint files, and optional known infrastructure definitions.

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

From the Home Assistant terminal after cloning or copying the repository:

```bash
cd /config/hioc
bash homeassistant/install_ha.sh
bash homeassistant/validate_ha.sh
ha core check
ha core restart
```

## Release Install

From a release package or repository checkout:

```bash
bash release/install.sh
bash release/validate.sh
```

Upgrade and rollback:

```bash
bash release/upgrade.sh
bash release/rollback.sh
```

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
