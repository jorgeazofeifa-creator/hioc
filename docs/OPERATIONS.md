# HIOC Operations

## PE-3 manufacturer dataset conflicts

The offline PE-3 builder may report an aggregate nonzero conflict count for
official assignment keys with multiple normalized organization variants. Such
keys remain in the private database as non-selectable conflict metadata without
organization values. `conflicting_assignment` is an unknown manufacturer result,
not an operational fault, and prevents fallback to a shorter prefix. Operators
must never manually select or patch a winner. IEEE source and generated database
artifacts remain local and outside Git and releases.

## PE-3 production deployment procedure

Production deployment is not an ad hoc shell session. Follow
[PE3_MANUFACTURER_PRODUCTION_RUNBOOK.md](PE3_MANUFACTURER_PRODUCTION_RUNBOOK.md)
one action at a time and return sanitized output after every action. The
supported final dataset path is
`/home/jazofv1/hioc/data/manufacturer/versions/local-ieee-ra--2026-08-11-r1/`.
Never transfer IEEE source CSVs, copy code manually into the runtime, overwrite
an immutable dataset version, silently replace a different configured path, or
interpret conflict/unknown counts as operational failure.

Action 1 accepts the retained external workspace only as an explicit Windows
operator variable. After repository support promotion, it resolves the governed
Windows line in the order `py -3.13`, `python3`, then `python`; fallbacks must
execute as CPython 3.13. No usable interpreter yields `PYTHON3_NOT_FOUND`; a
usable incompatible interpreter yields `PYTHON_VERSION_UNSUPPORTED`.
Database/manifest selection is based on both frozen SHA-256 values, adjacency,
regular-file/reparse-point checks, and frozen sizes. Multiple identical matches
are selected lexically only after validation; zero matches fail with
`VALIDATED_BUILD_PAIR_NOT_FOUND`. No raw registry value or Windows user path is
printed.

The current support state is `validation_pending`, so Action 1 stops with
`PYTHON_RUNTIME_SUPPORT_PENDING` before discovery. The separate Windows Python
3.13 Installation & Compatibility Validation checkpoint must install an
official runtime, record its patch, run the full suite and focused tests, and
commit the support promotion. Action 1 disables Python Install Manager automatic
installation during probes. See
[PYTHON_RUNTIME_COMPATIBILITY.md](PYTHON_RUNTIME_COMPATIBILITY.md).

The separate installation/validation action is the repository-controlled
`tools/hioc-python313-validate.ps1`. It verifies its own approved Git identity,
installs through the official WinGet Python Install Manager package, uses
`pymanager` for non-launching management/list operations and the sole explicit
`pymanager install 3.13` mutation, then runs the governed validation matrix with
`py -3.13`. Automatic runtime installation is disabled before any launcher
probe. Native manager stderr is captured and judged with its actual exit code,
so informational stderr with exit zero is not a failure and nonzero exit is.
An existing 3.14 runtime neither satisfies nor blocks the 3.13 checkpoint. It
returns sanitized evidence. It does not execute Action 1 or modify the support
manifest. Evidence review and support promotion remain a later checkpoint.

The official manager is present. An informal `py --help` diagnostic installed
CPython 3.14.7 through automatic default-runtime behavior; classify this as
`PYTHON_OPERATOR_DIAGNOSTIC_SIDE_EFFECT — UNINTENDED_DEFAULT_RUNTIME_INSTALL`,
not HIOC support or production state. Do not remove it in this checkpoint. The
safe manager dry run observed CPython 3.13.15 as the current candidate, while
the governed line remains floating 3.13.x and installation/validation remains
pending.

Action 1 is implemented only by the repository-controlled Windows PowerShell
script `tools/hioc-pe3-action1.ps1`; its source must never be reproduced through
chat. The runbook freezes the script SHA-256 and Git blob identity and provides
only the direct invocation model. Before artifact checks, the script verifies
the approved main/origin commit, its own path and Git identity, repository
cleanliness, and implementation ancestry. A script mismatch reports
`ACTION1_SCRIPT_IDENTITY_MISMATCH`.

Expected precondition and validation failures print a sanitized `RESULT` and
`ERROR_CODE`, then return from the script function. Unexpected exceptions are
caught as `ACTION1_UNEXPECTED_ERROR` with only a bounded `FAILURE_STAGE`. The
script contains no host-level `exit`, so the interactive PowerShell prompt
remains available for evidence capture.

## PE-3.1 manufacturer enrichment boundary

PE-3.1 executable tooling is repository implemented but not deployed. A future operator
obtains IEEE source files independently, records their SHA-256 values, and runs
an offline builder into an immutable local version directory under
`data/manufacturer/versions/`. HIOC never downloads, bundles, or redistributes
registry data. `MANUFACTURER_DB_PATH` is empty by default and a configured value
selects one local normalized database; its manifest is the fixed adjacent
`manufacturer-db.manifest.json`.

The future manually invoked `hioc-generate-manufacturer.py` reads completed
inventory and writes only private manufacturer sidecars. It has no schedule or
inventory hook. Install, upgrade, and rollback preserve local databases,
configuration, and sidecars. Production commands are deliberately deferred.
The binding operational, failure, locking, and rollback behavior is
[PE3_MANUFACTURER_EXECUTABLE_CONTRACT.md](PE3_MANUFACTURER_EXECUTABLE_CONTRACT.md).
The future standalone manufacturer validator is strictly read-only and acquires
no lock. Published database versions require no reader lock because the builder
atomically publishes a complete immutable directory. Runtime sidecar validation
observes independently loaded files and reports inconsistencies without repair.
Only the offline builder and manual generator own manufacturer-specific locks.

## Document Ownership

This is the authoritative operational and runtime reference. It defines how current components run, what they produce, and how operators validate and recover them. The current deployed-system overview is in [SYSTEM_REFERENCE.md](SYSTEM_REFERENCE.md); deployment mechanics are in [DEPLOYMENT.md](DEPLOYMENT.md).

## Runtime Health Principle

HIOC runtime is cron-driven, using short-lived jobs protected by `flock`. A healthy deployment should not be expected to show persistent HIOC processes. Health is determined through cron availability, expected entries, fresh status artifacts, successful scheduled output, logs, generated state, and safe manual execution when required.

The confirmed trigger is the `jazofv1` user crontab. Every listed command uses `flock -n`: if another live execution owns the lock, the new invocation exits instead of waiting. A lock-path file may remain after a run; its presence alone does not mean a job is stuck because the lock is held by a live file descriptor.

## Deployed PE-1 Operational Boundary

PE-1 is **complete and production validated**. Its private production sidecars
are `state/inventory/enrichment.json` and
`state/inventory/enrichment_status.json`. PE-1 runs inside the existing
Inventory Engine schedule and lock, adds no cron job or network acquisition,
and publishes neither artifact over MQTT.

Enrichment failure is isolated from
authoritative inventory generation: public inventory remains valid, the last
valid enrichment envelope remains untouched, and a sanitized local status
records the PE-1 failure without changing device health or creating an
incident. Detailed schema, permissions, validation, evidence, and rollback
requirements are in
[PE1_HOSTNAME_ENRICHMENT_SPEC.md](PE1_HOSTNAME_ENRICHMENT_SPEC.md). Corrected
production validation reported status `online`, 153 records, 83 candidates, 82
selected candidates, and zero conflicts. Missing optional source types,
historical candidates, or conflicts are not failures. The public inventory and
all existing consumer, identity, canonical-address, health, liveness, incident,
topology, and service-ownership contracts remained protected.

## Deployed PE-2.1 Operational Boundary

PE-2.0 and the PE-2.1 implementation design are approved; PE-2.1 is implemented,
repository validated, deployed, and production validated.
The local artifacts are
`state/inventory/assets.json` and
`state/inventory/assets_status.json`. A dedicated local CLI—not manual JSON,
MQTT, Home Assistant, dashboards, or an API—will own validated edits under
`/tmp/hioc-assets.lock`, create a validated timestamped backup before each
mutation, and write atomically with restrictive modes. It will read current
inventory only for stable-ID/orphan context and will never mutate or block the
Inventory Engine. The complete contract is in
[PE2_ASSET_FOUNDATION_SPEC.md](PE2_ASSET_FOUNDATION_SPEC.md).

Asset data will remain local and deny-by-default. Missing, empty, or orphaned
Asset metadata will not affect health, liveness, incidents, or any public
consumer. Governed production deployment/validation is prepared in
`tools/hioc-pe2-production-validate.sh`; it must be invoked only through the
approved target/repository bootstrap after its governance commit is pushed.
Preparation does not authorize Codex access, deployment, or production action.
The initial deployment completed, but its validator stopped on a repository-mode
versus runtime-mode contract defect before synthetic validation. The deployed
implementation remains in place with approved restrictive modes. Corrected
validation must use `--revalidate-existing-deployment`; that mode never invokes
`release/upgrade.sh` and produces a new protected evidence directory.

Incident protection for this revalidation is a positive contract, not live-file
digest equality. `tools/validate_pe2_incident_contract.py` validates JSON and
required shape, absence of Asset metadata and synthetic values, and structural
Asset-to-incident isolation. Normal lifecycle, title, telemetry, history, or
summary movement is operational drift. Uncertainty is `VALIDATION_FAIL` with
rollback false; rollback requires a deterministic PE-2-caused regression.

One-time PE-2 residue cleanup uses the committed six-entry manifest and
`tools/hioc-pe2-clean-synthetic-backups.py`. Run validation-only first, then
delete only after every entry passes basename, containment, regular-file,
non-symlink, ownership/mode, SHA-256, JSON, authoritative schema, and synthetic-
only checks. Wildcard, timestamp-range, and discovered-backup deletion are
prohibited. Current state, the backup root, and every unlisted operator backup
are outside scope. Cleanup and final revalidation are separate actions.

Final validation reported deployed-and-validated status, passing Asset and
protected invariants, passing privacy and performance, complete current-run
synthetic cleanup, and incident operational drift without causal PE-2 regression.
No rollback occurred or was required. Evidence is retained at the sanitized
reference `/tmp/hioc-pe2-production-validation-CtZ4WHUN`.

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
- **Outputs/status/logs:** The governed probe publishes legacy MQTT network
  state and inventory. Production validation at approved commit
  `e06539d9bece040d721b9912213559cc54f1610d` confirmed retained PI5 online
  state and Pi5 inventory identity at the configured address.
- **Recovery:** Inspect gateway, DNS, Internet, MQTT, configuration, and current telemetry before a manual run.
- **Validation:** Cron present and network latency/loss/DNS/MQTT observations
  update as expected. On 2026-07-30 the Git blob, Linux worktree, and deployed
  target matched; syntax, owner, group, mode, connectivity, publication,
  inventory, and incident recovery passed. Backup
  `hioc-network-probe.sh.20260730T203740.backup` was created; rollback was not
  required.

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

Canonical IPv4 is the inventory engine's deterministic representative address
for one reconciled MAC-backed identity. It is not complete address history and
does not prove reachability, health, or online status. Strong current or
configured evidence may outrank DHCP; active DHCP outranks `STALE` neighbor
evidence for the same MAC; `FAILED` and `INCOMPLETE` cannot become preferred
operational addresses. Equal evidence uses explicit lease, observation, and
numeric-address tie-breaks rather than collection order. Static devices remain
supported. Production investigation compares DHCP leases, `ip neigh`, the
canonical inventory record, stable ID, sources, and health fields without
treating a lease as a liveness check. See the
[Canonical Address Selection Hardening Evidence Report](CANONICAL_ADDRESS_HARDENING_EVIDENCE.md).

Canonical-address production validation must admit only same-MAC active DHCP
IPv4 versus different `STALE` neighbor IPv4 cases and must exclude local-host,
gateway, configured-integration, `REACHABLE`, and `PERMANENT` evidence. IPv6
and non-canonical address classes cannot qualify. `NO_QUALIFYING_CANDIDATE`
means the deployment and general invariants may pass without a current direct
reproduction; it is not failure and does not justify rollback. Only a
qualifying stale IPv4 that still wins, or an independent deployment/invariant
failure, is `FAIL`.

When retired-address DHCP evidence is found, inspect configured
`HIOC_INVENTORY_DHCP_LEASE_FILES`, readable lease rows and expiry values,
non-secret Pi-hole/dnsmasq reservation definitions, DHCP logs, and neighbor
evidence before classifying or changing it. Evidence collection must not alter
DHCP or network configuration.

The revised validator invariant document has a strict schema. Required Boolean
keys are `artifact_identity`, `unique_mac_identity`,
`inventory_count_consistent`, `health_and_liveness_fields_present`,
`stable_identity_fields_present`, and
`bounded_unrelated_canonical_changes`. All must exist and be JSON Booleans.
Only required `false` values fail an invariant. Keys beginning with `_` are
diagnostic metadata and may contain zero, counts, null, or strings without
affecting the outcome. Missing or mistyped required keys and unexpected
non-underscore keys are explicit input failures.

Production closure passed with strict-validator result
`NO_QUALIFYING_CANDIDATE`: all six Boolean invariants passed, diagnostic counts
were preserved separately, inventory remained at 151 devices, and one
unrelated canonical-address change remained within the bounded invariant.
Comparator source and runtime matched Git-derived SHA-256
`35f36916399331a6e1129f7a49ba86933960eca8e94d6b30c80e9be3d7cd75b8`.
No rollback was recommended or performed. The unexpired `.152` old lease and
its lack of renewal during the bounded 60-second observation remain separate
DHCP cleanup evidence; `.251` had stronger current `REACHABLE` and configured
integration evidence.

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

## Git-Governed Deployment Artifact Identity

The authoritative bytes of a Git-governed deployment artifact are the raw Git
blob at the exact approved commit and repository-relative path. Editor buffers,
temporary copies, uncommitted or platform-normalized worktrees, generated
intermediates, and pre-commit versions are never authoritative.

Use `tools/git_artifact_manifest.py APPROVED_FULL_COMMIT PATH
--compare-worktree` to derive identity. Record the full commit, path, Git blob
ID, Git-derived SHA-256, byte length, mode, and worktree comparison together.
The deterministic output has no timestamp and never accepts a supplied
checksum.

Network-probe deployment uses
`pi4-tools/deploy-network-probe.sh APPROVED_FULL_COMMIT
pi4-tools/scripts/hioc-network-probe.sh`. Synchronization is a separate
prerequisite. The helper requires a clean checkout at the exact full commit, a
tracked executable blob, byte-equal source, valid Bash syntax, a successful
timestamped backup, and byte-equal deployed target. It reports blob, worktree,
and deployed checksums plus the backup path. Do not add an
`EXPECTED_SOURCE_SHA` constant to operator instructions.

All deployment evidence must be regenerated after the final commit and push
from the exact `origin/main` Git object. No pre-commit checksum may appear in
operator instructions, and no manually transcribed checksum may be the sole
artifact identity. An Evidence Report must include approved commit, path, blob
ID, Git-derived SHA-256, worktree comparison, deployed checksum, and
source-to-target byte identity. Repository PASS is prohibited until this
post-push evidence is regenerated.

Deployment correctness and downstream incident recovery are separate
validation domains:

- **PASS:** deterministic deployment and downstream recovery both validated.
- **PARTIAL PASS:** deployment validated while recovery was delayed or
  inconclusive and requires separate downstream-state follow-up.
- **FAIL:** deterministic deployment validation failed.

Delayed recovery, stale presentation, retained state awaiting replacement, or
debounce/polling delay is not by itself a rollback reason. Do not roll back a
byte-identical, valid deployment solely because bounded incident observation
did not converge. The operator procedure captures and validates the helper's
actual timestamped backup and prints, but never automatically executes, a
rollback command reserved for justified deterministic failure.

## Operations Acceptance Standard

The permanent actionable release checklist is in [HIOC_MASTER_PLAN.md](HIOC_MASTER_PLAN.md#operations-acceptance-standard). Operations documentation must allow an operator to answer what exists, why, how it runs, how it is validated, and how it is recovered without rediscovering the system through SSH.
