# HIOC Operations

## Document Ownership

This is the authoritative operational and runtime reference. It defines how current components run, what they produce, and how operators validate and recover them. The current deployed-system overview is in [SYSTEM_REFERENCE.md](SYSTEM_REFERENCE.md); deployment mechanics are in [DEPLOYMENT.md](DEPLOYMENT.md).

## Runtime Health Principle

HIOC runtime is cron-driven, using short-lived jobs protected by `flock`. A healthy deployment should not be expected to show persistent HIOC processes. Health is determined through cron availability, expected entries, fresh status artifacts, successful scheduled output, logs, generated state, and safe manual execution when required.

The confirmed trigger is the `jazofv1` user crontab. Every listed command uses `flock -n`: if another live execution owns the lock, the new invocation exits instead of waiting. A lock-path file may remain after a run; its presence alone does not mean a job is stuck because the lock is held by a live file descriptor.

## Canonical Schedule

| Component | Cron expression | Plain-language schedule | Lock |
| --- | --- | --- | --- |
| Daily Maintenance | `15 3 * * *` | Daily at 03:15 | `/tmp/daily-maintenance.lock` |
| Resource Monitor | `*/15 * * * *` | Every 15 minutes | `/tmp/resource-monitor.lock` |
| UPS Monitor | `* * * * *` | Every minute | `/tmp/ups-monitor.lock` |
| DNS Watchdog | `* * * * *` | Every minute | `/tmp/dns-watchdog.lock` |
| PI4 MQTT Health Publisher | `*/1 * * * *` | Every minute | `/tmp/pi4-mqtt-health.lock` |
| HIOC Network Probe | `*/5 * * * *` | Every 5 minutes | `/tmp/hioc-network-probe.lock` |
| HIOC History Engine | `*/5 * * * *` | Every 5 minutes | `/tmp/hioc-history-engine.lock` |
| HIOC Inventory Engine | `*/30 * * * *` | Every 30 minutes | `/tmp/hioc-inventory-engine.lock` |
| HIOC Platform Status | `17 3 * * *` | Daily at 03:17 | `/tmp/hioc-platform-status.lock` |
| HIOC Incident Engine v2 | `*/1 * * * *` | Every minute | `/tmp/hioc-incident-engine.lock` |

All expected runtimes are **Not yet formally baselined**. A future baseline should use timestamped production measurements across normal and degraded conditions and must not be guessed from cron frequency.

The confirmed crontab lines do not redirect stdout or stderr. Repository-managed Inventory and Platform Status jobs log internally to their documented files; Incident Engine v2 emits publication failures to stderr; History Engine may expose uncaught output through cron. Whether host cron mails, journals, or discards otherwise uncaptured output requires production verification. External toolkit logging also requires production verification.

## External Pi4 Toolkit Jobs

The following six scripts are confirmed production components under `/home/jazofv1/pi4-tools`. The network probe is now governed at `pi4-tools/scripts/hioc-network-probe.sh`; the other five implementations remain outside this repository pending complete source intake. Their names, paths, schedules, triggers, and locks are verified; detailed output, log, and recovery contracts require production verification.

### Daily Maintenance

- **Purpose:** External Pi4 toolkit maintenance; exact operations require production verification.
- **Schedule/trigger/lock:** `15 3 * * *`, `jazofv1` crontab, `/tmp/daily-maintenance.lock`.
- **Command:** `/home/jazofv1/pi4-tools/daily-maintenance.sh`.
- **Outputs/status/logs:** Not yet documented in this repository.
- **Recovery:** Inspect cron, lock ownership, toolkit configuration, and existing output before any manual run. Do not delete the lock path blindly.
- **Validation:** Confirm cron is active, entry exists, and production-defined maintenance evidence is current. Exact success artifact requires production verification.

### Resource Monitor

- **Purpose:** External Pi4 resource monitoring; metric and output contract requires production verification.
- **Schedule/trigger/lock:** `*/15 * * * *`, `jazofv1` crontab, `/tmp/resource-monitor.lock`.
- **Command:** `/home/jazofv1/pi4-tools/scripts/resource-monitor.sh`.
- **Outputs/status/logs:** Not yet documented in this repository.
- **Recovery:** Validate configuration and current cron/output evidence before a one-time run.
- **Validation:** Cron entry plus recent repository-external telemetry or artifact; exact artifact is TBD pending production verification.

### UPS Monitor

- **Purpose:** External UPS telemetry used by HIOC incident/history inputs; detailed UPS inventory is not documented.
- **Schedule/trigger/lock:** `* * * * *`, `jazofv1` crontab, `/tmp/ups-monitor.lock`.
- **Command:** `/home/jazofv1/pi4-tools/scripts/ups-monitor.sh`.
- **Outputs/status/logs:** Repository consumers can read toolkit UPS state and MQTT telemetry; the producer contract requires production verification.
- **Recovery:** Inspect NUT health, toolkit configuration, current telemetry, and lock ownership before manual execution.
- **Validation:** NUT reachable, cron present, and recent UPS telemetry available.

### DNS Watchdog

- **Purpose:** External DNS watchdog; corrective behavior and output contract require production verification.
- **Schedule/trigger/lock:** `* * * * *`, `jazofv1` crontab, `/tmp/dns-watchdog.lock`.
- **Command:** `/home/jazofv1/pi4-tools/scripts/dns-watchdog.sh`.
- **Outputs/status/logs:** Not yet documented in this repository.
- **Recovery:** Validate Pi-hole, Unbound, and DNS resolution before considering configuration repair or a one-time run.
- **Validation:** Cron present, DNS resolution succeeds, and any production-defined watchdog evidence is current.

### PI4 MQTT Health Publisher

- **Purpose:** Publishes Pi4 toolkit health telemetry consumed through the legacy MQTT base topic.
- **Schedule/trigger/lock:** `*/1 * * * *`, `jazofv1` crontab, `/tmp/pi4-mqtt-health.lock`.
- **Command:** `/home/jazofv1/pi4-tools/scripts/publish-mqtt-health.sh`.
- **Outputs/status/logs:** MQTT outputs are external to this repository; HIOC consumers use configured legacy topics. Exact publisher topic set requires production verification.
- **Recovery:** Validate broker connectivity and toolkit configuration without exposing credentials, then perform a safe one-time run only under operator control.
- **Validation:** Cron present and expected retained or recent toolkit health telemetry is readable.

### HIOC Network Probe

- **Purpose:** Produces network observations consumed by HIOC history and incident processing.
- **Schedule/trigger/lock:** `*/5 * * * *`, `jazofv1` crontab, `/tmp/hioc-network-probe.lock`.
- **Command:** `/home/jazofv1/pi4-tools/scripts/hioc-network-probe.sh`.
- **Outputs/status/logs:** Repository consumers read legacy MQTT network metrics; exact probe writes require production verification because the deployed script is external.
- **Recovery:** Inspect gateway, DNS, Internet, MQTT, configuration, and current telemetry before a manual run.
- **Validation:** Cron present and network latency/loss/DNS/MQTT observations update as expected.

## HIOC Repository-Managed Jobs

### HIOC History Engine

- **Purpose:** Samples legacy MQTT network metrics and local host metrics, appends history CSVs, computes forecast/statistics JSON, and publishes retained history outputs.
- **Schedule/trigger/lock:** `*/5 * * * *`, `jazofv1` crontab, `/tmp/hioc-history-engine.lock`.
- **Command:** `/home/jazofv1/hioc/pi4/bin/hioc-history-engine.py`.
- **Outputs:** `history/network.csv`, `history/host.csv`, `state/forecast.json`, `state/statistics.json`, and retained forecast/statistics/history-status MQTT topics.
- **Status/logs:** `state/history_status.json` with known fields `status` and `updated`. No dedicated repository-derived log filename; cron handling of uncaught output requires production verification.
- **Recovery:** Read-only inspect status, CSV/JSON freshness, broker/config dependencies, and cron. A manual one-time execution is supported only after confirming no live lock owner.
- **Validation:** Status `online`, timestamp fresh relative to the five-minute schedule, JSON valid, history advances, and expected MQTT data is available.

### HIOC Inventory Engine

- **Purpose:** Collects passive inventory evidence, reconciles canonical devices/services, writes inventory projections and events, and publishes retained inventory MQTT state.
- **Schedule/trigger/lock:** `*/30 * * * *`, `jazofv1` crontab, `/tmp/hioc-inventory-engine.lock`.
- **Command:** `/home/jazofv1/hioc/pi4/bin/hioc-inventory-engine.py`.
- **Outputs:** `state/inventory/inventory.json`, `devices.json`, `services.json`, `capabilities.json`, `topology.json`, `dependencies.json`, `summary.json`, `status.json`, and internal events under `state/events/events.json`.
- **Status/logs:** `state/inventory/status.json`; `logs/hioc-inventory-engine.log` from the repository logger. July 29 point-in-time logs showed successful `devices=150 services=8` updates.
- **Recovery:** Inspect status, log, source availability, config, and JSON first. Run once manually only when no execution owns the lock. Deployment repair uses supported release tooling.
- **Validation:** Cron present; status and inventory artifacts valid and fresh; expected source state truthful; current log has successful updates; deployed validator passes.

### HIOC Platform Status

- **Purpose:** Reads `VERSION.yaml`, builds platform version/status documents, writes local state, and publishes retained platform MQTT topics.
- **Schedule/trigger/lock:** `17 3 * * *`, `jazofv1` crontab, `/tmp/hioc-platform-status.lock`.
- **Command:** `/home/jazofv1/hioc/pi4/bin/hioc-platform-status.py`.
- **Outputs/status:** `state/platform/version.json` and `state/platform/status.json`; retained `platform/version` and `platform/status` MQTT topics.
- **Logs:** `logs/hioc-platform-status.log`.
- **Recovery:** Distinguish historical from current errors, validate `VERSION.yaml` and config, inspect fresh state, and run once only when safe.
- **Validation:** JSON valid, successful current log entry, version matches manifest, and status is fresh relative to the daily schedule.

The log retains July 4 through July 12 historical failures caused by `TypeError: Logger._log() got an unexpected keyword argument 'hioc_version'`. Later successful executions establish that this is resolved historical evidence, not a current failure. Do not erase the old entries.

### HIOC Incident Engine v2

- **Purpose:** Reads telemetry, inventory, and events; correlates incidents; advances lifecycle; writes incident/timeline state; and publishes the retained incident contract.
- **Schedule/trigger/lock:** `*/1 * * * *`, `jazofv1` crontab, `/tmp/hioc-incident-engine.lock`.
- **Command:** `/home/jazofv1/hioc/pi4/bin/hioc-incident-engine-v2.py`.
- **Outputs:** `state/incidents/active.json`, `history.json`, `summary.json`, `timeline.json`, `latest_event.json`, `state/incident_engine_status.json`, events, and retained incident/status MQTT topics.
- **Status/logs:** `state/incident_engine_status.json` with known fields `status`, `version`, and `updated`; shared `logs/hioc.log` is produced by shell/common runtime paths, while Python stderr handling depends on cron. No separate v2 log path is established.
- **Recovery:** Inspect incident status/state, current cron output, MQTT dependency, config, and event/inventory inputs. A required publication failure returns nonzero and must be investigated or handled through supported deployment rollback.
- **Validation:** Status `online`, version correct, timestamp fresh relative to one minute, incident JSON valid, cron entry present, and retained MQTT validator passes when broker validation is required.

## Dated Production Evidence: 2026-07-29

- `cron`: active.
- History engine: online at `2026-07-29T20:25:00-06:00`.
- Incident Engine v2: online, version `1.2.0`, at `2026-07-29T20:27:28-06:00`.
- Inventory engine: recurring successful 30-minute updates; point-in-time count 150 devices and 8 services.
- HIOC deployment validation: **PASS**.
- Port `8091` belonged to Z-Wave JS UI, not HIOC. No HIOC dashboard endpoint was confirmed.

## Safe Operational Validation

1. Confirm cron service is active and expected `jazofv1` entries are present.
2. Inspect lock ownership, not merely lock-path existence.
3. Validate current JSON and timestamps against the component interval.
4. Inspect current log tail while preserving historical evidence.
5. Check generated state and configured external dependencies.
6. Use a manual one-time run only when it will not overlap and its side effects are understood.
7. Use `pi4/validate_pi4.sh` and checkpoint-specific validators.
8. Use supported deployment or rollback for file repair; do not patch the runtime ad hoc.

## Operations Acceptance Standard

The permanent actionable release checklist is in [HIOC_MASTER_PLAN.md](HIOC_MASTER_PLAN.md#operations-acceptance-standard). Operations documentation must allow an operator to answer what exists, why, how it runs, how it is validated, and how it is recovered without rediscovering the system through SSH.
