# HIOC Installation

## Document Ownership

This document owns operator installation, configuration, upgrade, validation, and rollback commands. [DEPLOYMENT.md](DEPLOYMENT.md) owns repository-to-production boundaries and operator responsibility; [OPERATIONS.md](OPERATIONS.md) owns runtime operation and health validation.

It should not contain roadmap, architecture rationale, release history, or dashboard design. For release packaging workflow, see [RELEASE.md](RELEASE.md). For project direction, see [HIOC_MASTER_PLAN.md](HIOC_MASTER_PLAN.md).

Python prerequisite compatibility and support claims are governed by
[PYTHON_RUNTIME_COMPATIBILITY.md](PYTHON_RUNTIME_COMPATIBILITY.md). A resolved
command name is not sufficient; installation procedures must execute the
interpreter and verify its CPython implementation and governed version.

## Repository and Runtime Layout

The authoritative source checkout is:

```text
/home/jazofv1/hioc-release-source
```

The deployed production runtime is:

```text
/home/jazofv1/hioc
```

Git operations, development, source validation, release preparation, and release execution originate from the authoritative source checkout. The production runtime contains deployed files, persistent runtime state, and installer-managed changes. It is a non-Git deployment target and must not contain `.git` after the approved migration.

Do not run `git pull`, `git reset`, `git clean`, `git checkout`, or other source-management commands inside `/home/jazofv1/hioc`. Installation must not create a Git-backed runtime. Use the supported release workflow from the authoritative source checkout or a validated release package.

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

Production uses the distribution-managed CPython `python3`; do not replace the
system interpreter to match Windows. Its exact production major/minor remains
unverified and must be recorded during governed PI validation.

For Windows operator checkpoints, official CPython 3.13.x is the proposed line,
not yet supported. The approved future mechanism is the current official Python
Install Manager through the official Windows/WinGet path. WindowsApps aliases
are not installation evidence. Installation and compatibility validation are a
separate checkpoint; do not install Python as part of PE-3 Action 1.
The installation/validation checkpoint is implemented only by the governed
`tools/hioc-python313-validate.ps1` script documented in
[PYTHON_RUNTIME_COMPATIBILITY.md](PYTHON_RUNTIME_COMPATIBILITY.md). Operator
guidance invokes that file after its commit is pushed; it must not reproduce the
installation program through chat. The script produces evidence only and does
not promote support state.

For scripted management, the checkpoint uses `pymanager`, never plain `py`:
`pymanager` lists managed runtimes and explicitly installs the floating 3.13
line, while `py -3.13` executes the already-installed governed runtime.
`PYTHON_MANAGER_AUTOMATIC_INSTALL=false` is set before any runtime-launch
probe. The official manager is currently present; CPython 3.14.7 is present only
because an operator diagnostic triggered default-runtime installation and is
not HIOC-supported. It is preserved pending a separate cleanup decision and
does not prevent explicit 3.13 installation. The currently observed dry-run
candidate is 3.13.15, but no patch is pinned before successful validation.

The latest direct CPython 3.13 evidence passed 506 tests with 13 skips and exit
code 0, but it does not promote support. It exposed a checkpoint-only false
failure: parsed unittest counts had been used as an additional acceptance gate
and could be lost when bounded output retained the stream head. The governed
script now accepts test stages strictly by native exit status, retains the
trailing summary for sanitized count reporting, and still fails on every
nonzero exit. A fresh governed checkpoint PASS remains mandatory.

The checkpoint continued to report `FULL_REGRESSION_FAILED` despite a direct
508-test pass and an equivalent pass using its temporary pycache prefix. This
is now a process-wrapper forensic checkpoint, not an installation task. Do not
install, uninstall, or select another runtime. The checked-in
`tools/hioc-python313-process-diagnostic.ps1` is the sole future diagnostic and
may run only after its commit is approved and synchronized.

That diagnostic proved direct `py -3.13` and `ProcessStartInfo` execution of the
resolved App Execution Alias are not equivalent. The checkpoint no longer
launches `py`. It uses the non-installing, machine-oriented
`pymanager list --one --format=exe --only-managed 3.13` result and validates the
exact interpreter as CPython 3.13 before tests. CPython 3.14.7 cannot satisfy
that filtered selection.

After selecting that exact interpreter, the checkpoint executes Python only via
PowerShell's native invocation operator. `ProcessStartInfo` is prohibited for
the governed Python probe and validation stages because final operator evidence
proved the exact interpreter passes directly—including with the checkpoint
pycache prefix—but fails through that wrapper. This does not change installation
or support state.

The first corrected install attempt may already have installed a 3.13 runtime
before stopping at the wrapped-runtime gap in `PYTHON_PROBE`. The checkpoint
therefore inventories managed 3.13 runtimes first and reuses the manager's one
authoritative selection without reinstalling. It installs only when no 3.13 is
present and fails safely on malformed or ambiguous inventory. Exact patch and
compatibility remain unknown until the wrapped `py -3.13` probe and complete
matrix pass.

Bash is not a prerequisite for the Windows CPython 3.13 runtime itself. Three
network-probe governance tests exercise Linux/Bash artifacts and now report an
explicit `Bash is required` skip when Bash is unavailable; their platform-
neutral companion checks continue to run. Do not install Bash, WSL, Git Bash,
rsync, or PyYAML merely to alter checkpoint skip counts. Where Bash exists, the
complete original network-probe assertions remain mandatory.

Verify the non-Git runtime boundary without using Git status:

```bash
test ! -e /home/jazofv1/hioc/.git
/home/jazofv1/hioc/pi4/validate_pi4.sh
```

The first command must succeed. Runtime health and version are established by the supported validator, `VERSION.yaml`, platform state, and release evidence, not by runtime Git metadata.

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
HIOC_INVENTORY_DHCP_LEASE_FILES="/etc/pihole/dhcp.leases"
HIOC_INVENTORY_KNOWN_INFRASTRUCTURE_FILE="/home/jazofv1/hioc/config/inventory/known_infrastructure.json"
```

Leave `HIOC_INVENTORY_ACTIVE_DISCOVERY` set to `off` for the currently approved passive discovery mode from host facts, default route, neighbor table, DHCP leases, integration hint files, and optional known infrastructure definitions.

`HIOC_INVENTORY_DHCP_LEASE_FILES` is an ordered, comma-separated list of Pi-hole/dnsmasq row-format lease files. The default is `/etc/pihole/dhcp.leases`. Additional dnsmasq-format paths may be configured explicitly. An explicitly blank value disables DHCP lease acquisition; it does not restore defaults. ISC `dhcpd.leases` syntax and IPv6 lease entries are not supported by this ingestion path.

HIOC captures all configured DHCP sources once at a fixed epoch during each inventory cycle. Active finite IPv4 leases and expiry-zero infinite leases provide assignment metadata. Expired finite leases are ignored and do not prove disappearance or offline state. HIOC reports found, empty, disabled, missing, unreadable, malformed, unsupported, I/O-error, or partial source state. Incomplete or unavailable configured input marks discovery as limited while existing inventory and other discovery sources remain preserved. A lease does not prove reachability or refresh a device's positive-observation timestamp.

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
post-upgrade evidence. See [MQTT.md](MQTT.md#operational-runtime-validation) for
preconditions, checked topics, and PASS, FAIL, and INCOMPLETE semantics.

The upgrade preserves the existing `state`, `history`, `logs`, and `backups` directories. Before copying the validated release, it records replaceable installation content, including configuration, under a timestamped directory in `/home/jazofv1/hioc/backups`. Runtime `.git` is excluded from both deployment and newly created upgrade backups.

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

The same release commands may be run from a validated versioned release package. Rollback excludes `.git`, including when a historical backup contains Git metadata, so it cannot recreate a Git-backed runtime. Persistent operational directories remain protected because deployment and rollback do not use delete semantics. Do not perform direct Git updates inside `/home/jazofv1/hioc`.

Then enable notifications:

```text
input_boolean.hioc_incident_notifications
```

The Home Assistant installer copies packages into `/config/packages` and dashboard YAML into `/config/dashboards`.

## Rollback

On Pi4:

```bash
bash /home/jazofv1/hioc/pi4/uninstall_pi4.sh
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
