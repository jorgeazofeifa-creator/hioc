# HIOC System Reference Manual

## PE-3 manufacturer conflict reference

The private manufacturer database has disjoint `records` and `conflicts`
mappings. Records are selectable assignments; conflicts contain only canonical
prefix metadata and `variant_count`, never organization variants. Lookup checks
conflicts before records at 36, 28, then 24 bits. A conflict returns
`conflicting_assignment`, manufacturer null, confidence unknown, and blocks
shorter-prefix fallback. Sidecar unknown counts include this status.

## PE-3 production boundary

The validated production-intended identity is dataset `local-ieee-ra`, version
`2026-08-11-r1`, with 53,581 selectable records and 2 conflict keys. Deployment
uses only its normalized database and adjacent manifest; raw source CSVs are not
production dependencies. The exact supported version directory includes both
identity components as `local-ieee-ra--2026-08-11-r1`. PE-3.3 is design-frozen
but neither deployed nor production validated.

## Python runtime boundary

The Python language floor is CPython 3.10, while tested and supported claims are
separate. CPython 3.12.13 has historical full-suite evidence. Windows CPython
3.13.x is supported for the operator workstation, with validated patch evidence
3.13.15. The exact managed interpreter is resolved through `pymanager` and
executed directly by PowerShell. Production uses the
distribution-managed `python3`, but its exact version remains unverified. The
authoritative policy and machine-readable support-state relationship are in
[PYTHON_RUNTIME_COMPATIBILITY.md](PYTHON_RUNTIME_COMPATIBILITY.md).

## Purpose and Authority

This is the authoritative current-state reference for what HIOC is today. The [Master Plan](HIOC_MASTER_PLAN.md) explains how HIOC is built and evolves. [OPERATIONS.md](OPERATIONS.md) owns detailed runtime procedures.

Evidence labels used here:

- **Known and verified:** supplied operator production evidence.
- **Repository-derived:** established by tracked code or documentation.
- **Requires production verification:** not proven by repository or supplied evidence.
- **Planned future state:** roadmap only, not implemented.

## Current Runtime Topology

```text
Clients
  |-- DHCP/DNS --> PI3 NUT&PIHOLE (192.168.100.252)
  |                  |-- Pi-hole FTL
  |                  |-- DHCP and DNS
  |                  |-- Unbound (127.0.0.1:5335)
  |                  |-- NUT
  |                  `-- HIOC cron-driven runtime
  |-- routed access --> Gateway/router (192.168.100.1)
  `-- Home Assistant --> PI5 (192.168.100.251)
                         |-- DNS dependency on PI3
                         `-- consumes configured MQTT/NUT/HIOC data
```

MQTT relationships are repository-supported, but broker host, authentication, and exact production placement are environment-managed and not recorded here. StrongVPN is abandoned; absence of `tun0` is expected. Historical duplicate policy-routing rules are cleanup candidates outside this checkpoint.

## Directory Structure

| Path | Responsibility | Evidence |
| --- | --- | --- |
| Windows repository | Development, tests, docs, Git commits | Known and verified |
| `/home/jazofv1/hioc-release-source` | Git-managed release source and release execution | Known and verified |
| `/home/jazofv1/hioc` | Non-Git deployed runtime | Known and verified |
| `/home/jazofv1/hioc/pi4/bin` | Deployed HIOC engine executables | Repository-derived |
| `/home/jazofv1/hioc/config` | Runtime HIOC configuration | Repository-derived |
| `/home/jazofv1/hioc/state` | Runtime-generated JSON state | Repository-derived |
| `/home/jazofv1/hioc/history` | Runtime-generated CSV history | Repository-derived |
| `/home/jazofv1/hioc/logs` | Runtime logs | Known and verified |
| `/home/jazofv1/hioc/backups` | Installer and release-upgrade backups | Repository-derived |
| `/home/jazofv1/pi4-tools` | External Pi4 toolkit | Known and verified |
| `/home/jazofv1/pi4-tools/scripts` | Mixed boundary: governed HIOC network probe plus remaining external scheduled toolkit scripts | Network probe repository source established; remaining intake pending |

The source repository additionally contains `pi4`, `homeassistant`, `release`, `docs`, and `tests`. Runtime-generated state and logs do not belong in Git.

## Data Flow

| Producer | Flow | Result |
| --- | --- | --- |
| External network probe | Network observations -> legacy MQTT | Inputs for history and incidents |
| Inventory engine | Host, route, neighbor, DHCP, integration, known infrastructure -> reconciliation | Inventory JSON, events, retained MQTT |
| History engine | MQTT/local metrics -> CSV/statistics/forecast | History state and retained MQTT |
| Incident Engine v2 | Telemetry + inventory + events -> correlation/lifecycle | Incident/timeline state and retained MQTT |
| Platform status | `VERSION.yaml` + runtime status -> platform JSON | Local and retained platform state |
| PI4 health publisher | Toolkit health -> MQTT | Legacy health inputs; exact external producer contract requires verification |

## Scheduled Jobs

The canonical production crontab has ten jobs: Daily Maintenance, Resource Monitor, UPS Monitor, DNS Watchdog, PI4 MQTT Health Publisher, HIOC Network Probe, History Engine, Inventory Engine, Platform Status, and Incident Engine v2. All are short-lived `flock -n` jobs. See the exact table and per-job contracts in [OPERATIONS.md](OPERATIONS.md#canonical-schedule).

## Persistent Supporting Services

| Service/port | Meaning | Evidence |
| --- | --- | --- |
| cron | Schedules HIOC and toolkit jobs | Known and verified |
| `22/tcp` | SSH | Confirmed production observation |
| `53` | Pi-hole DNS | Confirmed production observation |
| `80`, `443` | Pi-hole web interfaces | Confirmed production observation; protocol/interface details require verification |
| `3493/tcp` | NUT `upsd` | Confirmed production observation |
| `127.0.0.1:5335` | Unbound local listener | Known and verified |
| `8091` | Z-Wave JS UI, not HIOC | Known and verified |
| Pi-hole FTL | Pi-hole service | Known and verified |
| NUT | UPS monitoring support | Known and verified |
| MQTT broker | HIOC dependency where configured | Placement/port requires production verification |

HIOC engines are scheduled jobs, not persistent HIOC systemd services or Docker containers. No HIOC dashboard or API port was verified during the July 29 validation.

## JSON State Artifacts

| Artifact | Producer/purpose | Known schema/freshness | Consumers/validation |
| --- | --- | --- | --- |
| `state/history_status.json` | History Engine health | `status`, `updated`; fresh relative to 5-minute schedule | Operational checks; consumer beyond engine publication not asserted |
| `state/incident_engine_status.json` | Incident Engine v2 health | `status`, `version`, `updated`; fresh relative to 1-minute schedule | Incident status publication and operational checks |
| `state/forecast.json` | History Engine forecasts | Structured forecast document; 5-minute producer interval | MQTT/Home Assistant predictive views |
| `state/statistics.json` | History Engine statistics | Structured statistics document; 5-minute producer interval | MQTT/Home Assistant predictive views |
| `state/inventory/*.json` | Inventory Engine canonical inventory and projections | Inventory schema plus projection documents; 30-minute producer interval | MQTT, Home Assistant, incident correlation, validator |
| `state/inventory/enrichment.json` | PE-1 private hostname evidence envelope | Closed schema `1.0`; generated with inventory; production validated | Local validation only; not published to MQTT or consumer contracts |
| `state/inventory/enrichment_status.json` | PE-1 local generation status | Closed schema `1.0`; production status `online` | Local operational validation only |
| `state/incidents/*.json` | Incident Engine lifecycle, history, summary, timeline | Current incident contracts in DATA_MODEL/MQTT; 1-minute producer interval | MQTT, Home Assistant, operator review |
| `state/platform/version.json` | Platform Status version | Version manifest projection; daily producer interval | MQTT and validator |
| `state/platform/status.json` | Platform Status health | `status`, `updated`, optional publish/error fields; daily producer interval | MQTT and validator |
| `state/events/events.json` | Core event bus | Internal event collection | Inventory/incident processing and validator |

Exact freshness alert thresholds are not yet formally baselined; validation compares timestamps to the documented schedule and current operational context.

## Logs

| Log | Producer/use |
| --- | --- |
| `logs/hioc-inventory-engine.log` | Inventory Engine recurring results and errors |
| `logs/hioc-platform-status.log` | Platform Status results and errors |
| `logs/hioc.log` | Shared shell/common HIOC logging |

Log retention is not established by repository evidence. Historical errors may remain after recovery. July 4-12 Platform Status logging failures are retained evidence; later successful entries establish recovery.

## Configuration

- `/home/jazofv1/hioc/config/hioc.conf`: deployed HIOC configuration, created from `pi4/config/hioc.conf.example` if absent.
- `/home/jazofv1/pi4-tools/config/toolkit.conf`: external toolkit and MQTT configuration dependency.
- `/home/jazofv1/hioc/config/inventory/known_infrastructure.json`: optional operator-managed inventory metadata.
- `VERSION.yaml`: authoritative release/version manifest.
- `/etc/pihole/dhcp.leases`: default Pi-hole DHCP lease input.

External Pi-hole, Unbound, NUT, router, and Home Assistant configuration paths are production-managed and require production verification. Secrets are intentionally omitted.

## Operational Dependencies and Health Model

See [NETWORK_FOUNDATION.md](NETWORK_FOUNDATION.md) for network dependencies. Current health separates observation, staleness, degradation, offline, incident, process, service, capacity, and freshness concepts. DHCP assignment is not liveness. Process-up status is not sufficient for service health. Capacity health is architecturally required but DHCP capacity monitoring remains planned. See [INCIDENT_MODEL.md](INCIDENT_MODEL.md).

## Recovery Summary

1. Validate cron and expected entries.
2. Inspect lock ownership without deleting lock paths blindly.
3. Inspect fresh state and valid JSON.
4. Inspect current logs while preserving historical evidence.
5. Run a safe one-time job only when side effects and overlap are controlled.
6. Validate deployed files with supported validators.
7. Use [DEPLOYMENT.md](DEPLOYMENT.md), [RELEASE.md](RELEASE.md), and [RECOVERY_BASELINE.md](RECOVERY_BASELINE.md) for deployment or recovery.

## Verification Register

### Known and verified

PI3/PI5/gateway addresses, current DHCP pool, ten cron entries, non-Git runtime model, listed logs/status files, July 29 deployment PASS, HIOC short-lived execution model, Unbound local listener, and port `8091` as Z-Wave JS UI rather than HIOC.

### Repository-derived

HIOC engine outputs, MQTT contracts, installer/validator behavior, configuration defaults, state schemas, and release/rollback boundaries.

### Requires production verification

External Pi4 toolkit script output contracts, log routing for every cron command, expected runtimes, log retention, broker placement and port, exact Pi-hole/Unbound/NUT configuration paths, and any HIOC dashboard endpoint.

### Current enrichment and planned future state

The Observation -> Enrichment -> Asset information model is authoritative.
PE-1 and PE-2.1 are production validated. DHCP Service Health & Capacity Monitoring, Safe Active
Discovery,
retention/archival policy, asset-centric digital twin, and later
topology/dependency intelligence. Canonical-address hardening is complete and
production validated; PE-0 is design approved and PE-1 is complete and
production validated. Its two private Enrichment sidecars are current runtime
state. Corrected production validation
reported `online`, 153 records, 83 candidates, 82 selected candidates, and zero
conflicts without changing public inventory or consumer contracts. PE-2.0 is
design and implementation design approved. PE-2.1 now provides deployed private
`assets.json`, `assets_status.json`, and the local Asset CLI/validator and is
production validated. Asset presentation/publication remains future work.

PE-3.0 architecture is approved and the PE-3.1 executable contract is frozen in
[PE3_MANUFACTURER_EXECUTABLE_CONTRACT.md](PE3_MANUFACTURER_EXECUTABLE_CONTRACT.md).
The repository-implemented runtime uses a locally transformed, checksum-verified database and a
manually invoked separate generator for private manufacturer sidecars. Local
acquisition/transformation is approved; registry content cannot enter Git or
releases. PE-3.2 externally validated the production-intended dataset and
manifest; neither is committed or deployed. No production manufacturer sidecar,
schedule, public projection, or consumer exists. PE-3.3 is design approved;
Production Actions 1 and 2 completed and Action 3 staging evidence is preserved.
Action 4 is stopped at bounded staged-file permission normalization pending the
approved repository-controlled resume. No dataset installation, sidecar
generation, deployment, or PI3 production validation has occurred.
