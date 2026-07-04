# HIOC Production Architecture Review

Review scope: entire repository as currently present in this workspace, assessed as a commercial monitoring platform candidate before a version 1.0 release.

No code changes are included in this review.

## Executive Assessment

HIOC has a strong operational vision and a credible early architecture: Pi4 collectors produce local state, publish retained MQTT, and Home Assistant renders the operator console. The incident model is unusually practical for a home infrastructure tool because it tries to answer cause, impact, confidence, evidence, and recommendation rather than only listing sensors.

The project is not yet version-1.0 commercial-grade. The main blockers are not product direction; they are engineering structure. Incident and history engines still duplicate configuration, MQTT, JSON, and subprocess behavior instead of using shared runtime modules. There is no formal scheduler, schema validation layer, migration framework, plugin interface, or comprehensive test harness. Home Assistant integration is useful but partly environment-specific. Long-term reliability will require stronger contracts between telemetry, state, incident correlation, inventory, dashboards, and installers.

## Scores

| Category | Score | Rationale |
|---|---:|---|
| Overall architecture | 6 | The core pattern is sound: local state, retained MQTT, HA console. The system is still script-oriented with limited internal contracts and no orchestration layer. |
| Code organization | 5 | New inventory modules improve structure, but incident/history remain monolithic scripts with repeated helpers. Shell and Python runtimes coexist without a clear boundary. |
| Maintainability | 5 | Simple files are easy to read, but duplicated config/MQTT/state handling means changes must be repeated across engines. Lack of schemas increases regression risk. |
| Extensibility | 6 | MQTT topics and state files make extension possible. Missing plugin/provider interfaces, migration strategy, and scheduler abstraction will slow growth. |
| Performance | 6 | Current home-scale workload is acceptable. Blocking MQTT reads, repeated subprocesses, CSV full reads, and large retained JSON attributes become issues as data grows. |
| Security | 5 | Active inventory is now off by default, which is good. MQTT credentials are handled through config but passed to subprocesses in older engines. No secret redaction, least-privilege docs, or TLS MQTT support. |
| Reliability | 5 | Local JSON state and retained MQTT are good reliability foundations. Atomic writes exist only in shared runtime, not all engines. Cron is simple but weak for supervision, backoff, and health. |
| Installability | 6 | Installers and validators exist and are conservative. They are still path-personalized, cron-based, and not fully idempotent across all migration scenarios. |
| Documentation | 7 | Documentation coverage is now broad: architecture, install, MQTT, HA, data model, roadmap, decisions, implementation review. It still needs operator runbooks and compatibility matrices. |
| Home Assistant integration | 6 | MQTT sensors/packages are straightforward and useful. The main dashboard references many environment-specific entities, and notification target remains hardcoded. |
| MQTT architecture | 6 | Retained JSON topics are clear and stable. Inventory now uses persistent MQTT publishing. Incident/history still shell out to `mosquitto_pub`/`mosquitto_sub`, and there is no shared topic registry or schema validation. |
| Testing | 4 | Inventory unit tests are useful. There are no incident/history unit tests, integration tests, installer tests, MQTT contract tests, or dashboard/entity compatibility tests. |
| Observability | 5 | State JSON files and basic logs exist. There is no structured logging standard, engine runtime metrics, failure counters, self-health dashboard, or traceable run IDs. |
| Scalability | 4 | Fine for a small home environment. Large inventories, long CSV history, retained full-device payloads, and Home Assistant JSON attributes may not scale cleanly. |
| Separation of concerns | 5 | Inventory has reasonable separation. Incident/history mix config, collection, correlation, state, publishing, and orchestration in single files. |

## Duplicated Logic

- Shell-style config parsing appears in incident, history, shared Python config, and shell common code.
- MQTT publishing exists in three forms: incident `mosquitto_pub`, history `mosquitto_pub`, and inventory socket MQTT client.
- MQTT reading through `mosquitto_sub` is duplicated in incident and history.
- JSON load/save helpers are duplicated, and only shared runtime uses atomic replace.
- Numeric parsing helpers exist in shell and Python forms.
- Timestamp generation is repeated.
- State directory creation is repeated across engines and installers.
- Topic names are embedded in engines, docs, and HA packages without a single topic registry.
- Health/status payload patterns are similar but not standardized.

## Oversized Modules

- `pi4/bin/hioc-incident-engine-v2.py`: combines config, MQTT I/O, telemetry collection, signal generation, correlation, incident lifecycle, file persistence, and MQTT publishing.
- `pi4/bin/hioc-history-engine.py`: combines config, MQTT reads, CSV writes, host metrics, trend calculations, forecast modeling, and publishing.
- `pi4/lib/hioc/inventory.py`: improved but already broad: discovery adapters, classification, health scoring, topology, dependencies, and orchestration live together.
- `homeassistant/dashboards/home_infrastructure_hioc_incident_center_v12.yaml`: very large and partly environment-specific, which makes maintenance and portability hard.

## Opportunities For Abstraction

- `ConfigProvider`: one canonical parser for toolkit config, HIOC config, environment overrides, defaults, and type coercion.
- `MqttBus`: one shared MQTT client for publish, subscribe/read, retained payloads, topic registry, reconnect, and error reporting.
- `StateStore`: atomic JSON read/write, schema validation, migration, locking, retention, and backup hooks.
- `Scheduler`: replace direct cron knowledge with generated job definitions, intervals, locks, and validation.
- `TelemetryProvider` interface: probe MQTT, host metrics, inventory providers, HA-exported data, SNMP, and future integrations.
- `HealthScorer` interface: common health status scoring for incidents, inventory, services, and forecast signals.
- `TopologyProvider` and `DependencyProvider`: separate raw discovery from graph construction.
- `Dashboard contract generator`: derive HA MQTT sensors and docs from topic/schema definitions.
- `Validation framework`: common validation checks with machine-readable output.

## Future Technical Debt

- Personalized default paths such as `/home/jazofv1/hioc` and `/home/jazofv1/pi4-tools`.
- Cron-only scheduling will become brittle as subsystem count grows.
- Multiple MQTT implementations will diverge.
- MQTT payload schemas are documented but not enforced.
- Retained payloads may grow without size limits.
- CSV history files will grow for a year and are read into memory for calculations.
- Legacy shell incident engine remains present and can confuse ownership.
- Dashboard files are not generated from installed entity contracts.
- No database abstraction for inventory/history as data grows.
- No migration framework for state files or HA entity changes.

## Coupling Between Subsystems

- Incident and history engines are tightly coupled to legacy Pi4 probe MQTT topics.
- HA packages are tightly coupled to exact retained topic paths.
- Dashboard YAML is coupled to many entities not installed by this repo.
- Installers assume Pi4 toolkit config exists in a specific path.
- Inventory depends on Linux command availability and Pi-oriented filesystem conventions.
- Existing incident notifications are coupled to one mobile app service name.
- History forecasts are coupled to CSV layout and hardcoded sample assumptions.

## Missing Interfaces

- No formal discovery-provider interface.
- No formal MQTT topic/schema registry.
- No state repository interface.
- No incident-rule or correlation plugin interface.
- No Home Assistant entity contract generator.
- No versioned migration interface.
- No runtime health interface shared by all engines.
- No typed data models for incidents, forecasts, inventory, services, topology, or dependencies.
- No centralized command execution policy for timeouts, logging, and redaction.

## Missing Configuration Options

- MQTT TLS, CA certificate, client certificate, and insecure-skip-verify behavior.
- MQTT client IDs per engine.
- Per-engine enable/disable flags.
- Per-engine intervals outside shell cron strings.
- Log level and log retention.
- State retention limits for inventory and timelines.
- History CSV retention enforcement.
- Notification target selection.
- Dashboard install selection.
- Active discovery allowlist/denylist.
- Maximum MQTT payload size.
- Maximum inventory device count.
- System command paths or capability detection overrides.

## Missing Validation

- JSON schema validation for all state and MQTT payloads.
- MQTT publish/read contract tests.
- Installer dry-run validation.
- HA package entity validation against expected topics.
- Dashboard dependency validation.
- Cron duplicate/migration validation.
- History CSV retention validation.
- Config value type/range validation.
- MQTT credential presence and broker connectivity validation before first run.
- Active discovery safety validation beyond subnet size.
- Shell script syntax validation in CI.

## Race Conditions And Concurrency Issues

- Cron uses `flock` for each engine, which prevents overlap per engine, but shared state writes across engines are not globally coordinated.
- Incident and history engines write JSON with direct `write_text`, not atomic temp-file replacement.
- Installer runs engines immediately after installing cron; a cron trigger at the same time could contend, though flock reduces this for engine-specific locks.
- Crontab modification is read-modify-write and can race with external crontab edits.
- HA installer overwrites package/dashboard files after backup but has no lock.
- Multiple future inventory providers writing integration hint files could race with inventory reads unless atomically written.

## Long-Running And Blocking Operations

- Incident engine performs multiple blocking `mosquitto_sub -C 1` reads with timeouts every minute.
- History engine performs multiple blocking MQTT reads every five minutes.
- History engine shells out to `bash -lc` for disk and memory metrics.
- Inventory active scan can run up to 90 seconds if enabled.
- Inventory SNMP can add per-target blocking timeouts if enabled.
- MQTT publish in incident/history shells out per topic.
- CSV history reads load up to 2016 rows per metric now, which is okay but still blocking.

## Disk Write Frequency

- Incident engine: every minute writes active incident, history, summary, status, and sometimes timeline/latest event.
- History engine: every five minutes appends network and host CSV rows and writes forecast/statistics/status.
- Inventory engine: every 30 minutes writes inventory, devices, services, topology, dependencies, summary, and status.
- Installers write backups and copied files.

Current write volume is acceptable for a Pi4, but direct full-file rewrites should be standardized through an atomic state store with retention policies.

## Memory Growth Risks

- Incident history and timeline are bounded by `HIOC_HISTORY_LIMIT`, good.
- History CSV files grow for up to documented retention but retention is not enforced in code.
- `read_csv` loads selected CSV data into memory; acceptable now, but not durable for multi-year or high-frequency data.
- Inventory retains previously seen devices indefinitely unless state is manually pruned.
- HA JSON attributes for full inventory can become large and burden HA state storage.

## MQTT Message Growth Risks

- `home/infrastructure/hioc/inventory` publishes the full inventory object.
- `inventory/devices` and `inventory/services` can grow with device count.
- HA attribute mirrors of full inventory may become large.
- Incident payloads include telemetry/evidence and can grow if correlation expands.
- No configured payload size limits, compression, chunking, or pagination.

## Five-Year Architecture Changes To Make Today

If HIOC is expected to grow for another five years, I would move it from a collection of scripts to a small, disciplined platform:

1. Create a versioned HIOC core Python package with typed models, schema validation, shared MQTT, shared state store, and shared config.
2. Replace cron strings with a managed scheduler or systemd timers generated from a declarative job registry.
3. Define a provider/plugin interface for telemetry, inventory, topology, dependencies, and incident rules.
4. Introduce a local embedded database, likely SQLite, for inventory, history, events, and migrations while continuing to publish MQTT summaries.
5. Treat MQTT as an external contract generated from schemas, not hand-coded strings.
6. Generate Home Assistant packages and docs from the MQTT/entity contract.
7. Build a validation CLI that checks config, state, MQTT broker, HA packages, dashboards, permissions, and migrations.
8. Move dashboards toward repo-owned entity contracts and separate optional environment-specific views.
9. Add structured logs, per-run status, metrics, and failure counters for every engine.
10. Establish CI tests for Python, shell, YAML, schema compatibility, and installer behavior.

## Version 2 Architecture Recommendations

Prioritized from highest to lowest impact:

1. **Create `hioc-core` shared runtime package.** Move config, MQTT, state, logging, subprocess execution, schemas, and version constants into one reusable package. This removes the biggest source of duplication and drift.
2. **Introduce typed, versioned schemas.** Define JSON schemas or typed Python models for incident, forecast, inventory, topology, dependency, and status payloads. Validate before writing state or publishing MQTT.
3. **Replace per-engine MQTT implementations with one bus.** Incident, history, and inventory should share a persistent MQTT abstraction supporting publish, subscribe/read, retained messages, TLS, credentials, reconnect, and redacted errors.
4. **Add a state store with atomic writes and migrations.** All engines should use one `StateStore` that handles temp-file replace, file locks, schema versioning, retention, and migration.
5. **Move history and inventory to SQLite.** Keep MQTT summaries, but store long-lived samples, inventory changes, events, and graph edges in a queryable local database.
6. **Create a declarative job registry.** Define engine intervals, locks, timeouts, enable flags, and validation in one place, then generate cron/systemd timer entries.
7. **Refactor incident engine into modules.** Split telemetry collection, signal rules, correlation, lifecycle, state persistence, and publishing. This is the most important engine-level maintainability fix.
8. **Refactor history engine into modules.** Split collectors, time-series store, trend calculations, forecast models, and publishing.
9. **Split inventory providers from inventory modeling.** Discovery adapters should be pluggable: local host, neighbor table, DHCP, HA integration exports, SNMP, Orbi, switches, cameras, UPS, MQTT broker, and future sources.
10. **Create a topology/dependency graph layer.** Use explicit graph models and confidence levels instead of simple edge inference embedded in inventory code.
11. **Add config validation and defaults typing.** Every config option should have type, default, allowed range, description, and validation error.
12. **Make Home Assistant integration contract-driven.** Generate packages from MQTT schemas and maintain compatibility metadata for entity IDs and unique IDs.
13. **Separate portable and environment-specific dashboards.** Ship a core dashboard that only references repo-installed entities. Keep local custom dashboards as optional examples.
14. **Make notifications configurable.** Replace the hardcoded mobile app notify service with helper-driven or documented configuration.
15. **Add observability for engines.** Publish engine duration, last success, last failure, error count, skipped runs, MQTT publish status, and state write status.
16. **Add bounded payload policies.** Define max inventory devices per MQTT payload, summaries vs details, optional pagination, and HA attribute size constraints.
17. **Add retention enforcement.** Enforce CSV/database retention, timeline length, inventory tombstone lifetime, and log rotation.
18. **Add integration and contract tests.** Test MQTT payloads, schemas, HA YAML, installers, validators, and migration behavior in CI.
19. **Add least-privilege deployment documentation.** Document required Linux permissions, optional active discovery privileges, file ownership, and secret handling.
20. **Create release packaging.** Provide versioned archives, checksums, migration notes, and rollback procedures for true v1.0/v2.0 releases.

## Release Readiness Judgment

HIOC is promising and useful as an advanced home monitoring stack, but I would not release it as commercial-grade version 1.0 yet. I would consider it a strong pre-1.0 technical preview or private beta.

The shortest credible path to v1.0 is:

1. Refactor shared runtime across all engines.
2. Add schemas and state validation.
3. Add installer/HA validation depth.
4. Remove or clearly quarantine environment-specific dashboard assumptions.
5. Add tests for incident and history behavior.
6. Add observability for engine health.

Once those are in place, the existing product direction can support a serious self-hosted monitoring platform.

