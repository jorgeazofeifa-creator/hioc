# HIOC MQTT Contract

## Document Ownership

This document owns MQTT topics, payload expectations, retention behavior, publishing strategy, topic hierarchy, and MQTT discovery/integration notes.

It should not contain roadmap, dashboard design, installation, or Home Assistant UI details. For payload object fields, see [DATA_MODEL.md](DATA_MODEL.md). For Home Assistant entities, see [HOME_ASSISTANT.md](HOME_ASSISTANT.md).

Default base topic:

```text
home/infrastructure/hioc
```

## Incident Topics

```text
home/infrastructure/hioc/incidents/active
home/infrastructure/hioc/incidents/history
home/infrastructure/hioc/incidents/summary
home/infrastructure/hioc/timeline/history
home/infrastructure/hioc/timeline/latest
home/infrastructure/hioc/status
home/infrastructure/hioc/status/detail
```

Correlation Engine v2 publishes through the same incident topics. The public topic names are unchanged, and existing Home Assistant sensors continue to read `status`, `severity`, `system`, `title`, `root_cause`, `confidence_percent`, `affected`, and timeline fields from the retained JSON payloads.

Completed incident history entries include a derived `review` object so operators can understand what happened after recovery. The `incidents/summary` payload also includes `history_stats`, `recent_incidents`, `recent_incident_reviews`, and `latest_incident_review` attributes for Dashboard v2. These are additive fields on existing retained topics.

The Incident Engine publishes the same ordered topic and payload set over one Core MQTT connection per run. This transport implementation does not change topic names, retained semantics, JSON structures, embedded reviews, history ordering, or status content. Authoritative local files are written before publication. A required connection or publication failure produces a nonzero Incident Engine status; earlier topics may already have been retained when a later topic fails, and the final online status is not published after such a failure.

## Forecast Topics

```text
home/infrastructure/hioc/forecast
home/infrastructure/hioc/statistics
home/infrastructure/hioc/history/status
```

## Living Inventory Topics

```text
home/infrastructure/hioc/inventory
home/infrastructure/hioc/inventory/devices
home/infrastructure/hioc/inventory/services
home/infrastructure/hioc/inventory/topology
home/infrastructure/hioc/inventory/dependencies
home/infrastructure/hioc/inventory/summary
home/infrastructure/hioc/inventory/status
```

The PE-4 public projection has accepted PI3 POSIX validation, deployment and production
acceptance: **PASS/CLOSED**, on OPERATOR_SUPPLIED evidence in the
[final closure](PE4_HOME_ASSISTANT_ASSOCIATION_PUBLIC_PROJECTION_DEPLOYMENT_CLOSURE.md).
Its five-field optional device object flows only through existing inventory and
inventory/devices payloads. No new topic or association aggregate is authorized;
retained QoS 0, one connection, local files before MQTT and failure isolation remain
unchanged. This PE-4 publication does not implement PE-5; no fresh live observation is claimed.

## Platform Topics

```text
home/infrastructure/hioc/platform/version
home/infrastructure/hioc/platform/status
```

All HIOC publications are retained so Home Assistant recovers state after restart.
The Living Inventory and Incident engines publish their topic sets over one persistent MQTT connection per run. The public topic names and JSON schemas remain unchanged.

## Operational Runtime Validation

Runtime MQTT validation proves that the deployed HIOC configuration can reach the
broker and retrieve the retained Incident Engine contract. Run the deployed
validator after an install or upgrade:

```bash
/home/jazofv1/hioc/pi4/bin/hioc-validate-mqtt.py
```

The command loads `MQTT_HOST`, `MQTT_PORT`, optional `MQTT_USER` and
`MQTT_PASSWORD`, and `HIOC_BASE_TOPIC` through HIOC's existing configuration
service. Configuration precedence remains the Pi4 toolkit configuration,
deployed HIOC configuration, and then matching process-environment overrides.
The broker is not assumed to be local, and operators do not need to discover or
reconstruct broker settings manually. Current HIOC MQTT clients do not define a
TLS configuration contract, and this validator does not introduce one.

`python3` and `mosquitto_sub` must be installed, and the configured account must
be allowed to read the retained topics. Each read has a bounded timeout. The
validator checks:

```text
<HIOC_BASE_TOPIC>/incidents/active
<HIOC_BASE_TOPIC>/incidents/history
<HIOC_BASE_TOPIC>/incidents/summary
<HIOC_BASE_TOPIC>/timeline/history
<HIOC_BASE_TOPIC>/timeline/latest
<HIOC_BASE_TOPIC>/status/detail
<HIOC_BASE_TOPIC>/status
```

JSON topics must contain a nonempty, valid UTF-8 JSON payload. The scalar status
must be `online`. Output reports each observed topic and payload byte count
without dumping payloads or credentials. Incident history also reports its
record count when it is a JSON array and whether any record contains an embedded
review.

- `PASS` and exit code `0` mean every required retained topic was read and
  validated. A legacy nonempty history without embedded review data is reported
  as a warning but does not independently fail the transport contract.
- `FAIL` and exit code `1` mean required configuration, subscriber execution,
  connectivity, payload presence, JSON, UTF-8, or scalar status validation
  failed.
- `INCOMPLETE` and exit code `2` mean at least one bounded read ended without a
  retained payload, while no stronger failure was observed.

The command is read-only: it never publishes a test payload or changes retained
state. Preserve its concise console output, exit status, topic validation
summary, history payload size, history record count, embedded-review result,
deployed commit, and overall PASS, FAIL, or INCOMPLETE result in the checkpoint
Evidence Report. Successful source deployment, source comparison, and unit tests
remain necessary, but they do not prove end-to-end retained MQTT behavior in the
deployed environment. Runtime validation is required.

## Current complete PE-5 execution roadmap

Classification: HISTORICAL_INTENTIONALLY_PRESERVED planning publication at 78ee4cd16120bf4ea3166901994727a19d1faad1; ordering remains authoritative. Current status follows PE-5.2 complete design below.

PE5_STATUS=IN_PROGRESS
PE5_1_STATUS=COMPLETE_THROUGH_ACCEPTED_FIRST_NATIVE_EXECUTION
CURRENT_PE5_CHECKPOINT=PE-5.2 - Mapping Source Authority and Complete Contract Design
PE5_FINAL_CHECKPOINT=PE-5.9 - Final PE-5 Closure and PE-6 Handoff
PE5_FINAL_SUCCESSOR=PE-6
TOTAL_REMAINING_PE5_CHECKPOINTS=8

The [Master Plan](HIOC_MASTER_PLAN.md#complete-pe-5-execution-roadmap) owns every remaining checkpoint and Definition of Done. PE-5.1 is accepted. This planning publication grants no implementation or operational access. PE-5.2 resolves mapping authority/contract, storage/current-history/retention/LKG/restart/corruption and execution/trigger/cadence/integration/locking/failure decisions before PE-5.3 implements accepted contracts. Source sync PE-5.4, inactive deployment PE-5.5, bounded validation PE-5.6, conditional activation PE-5.7, natural/operational acceptance PE-5.8 and final closure/private PE-6 handoff PE-5.9 are fixed. Configured mappings remain distinct from Discovery, broker/topic/client observations, HA Discovery and publication. No identity, canonical-IP, observation, liveness, health, Asset, incident, classification or public payload authority is added. Existing MQTT topics/subscriptions/retained messages/credentials/broker/HA consumers stay unchanged; any compatibility change needs explicit review before implementation. Private schema/store evolution is assigned to PE-5.2/3, never silently applied during planning.

## Current PE-5.2 complete contract design

Classification: HISTORICAL_INTENTIONALLY_PRESERVED PE-5.2 lifecycle snapshot at 72e878f9c0c8f5d3fe6357979e045943f3cf9d34. PE5_2_STATUS=COMPLETE_CONTRACT_DESIGN; PE5_3_STARTED=FALSE.
Current next checkpoint: PE-5.3 - Remaining Capability Implementation and Comprehensive Validation.
See [PE-5.2 complete contract design](PE5_MAPPING_CONTRACT_DESIGN.md) and
governance/pe5/pe5-mapping-contract-design.json for source, relationship, schema, privacy,
storage, execution and private PE-6 handoff decisions. Original undefined source/store/
freshness is now DESIGN, not a discovered store. No universal production absence claimed.
Future private configuration config/enrichment/mqtt_mappings.json remains distinct from
known-infrastructure DEVICE METADATA and generated state/enrichment/service_associations/current.json.
Opaque endpoint IDs require no raw topics or live broker/HA/client/Discovery access.
Private source/output persistence required; standalone 15-minute recurrence and 20-minute
handoff validity are selected NEW DESIGN values, not observed schedules. Inventory
freshness remains 2100 seconds; accepted PE-5.1 runtime/caller/schema/rules unchanged.
No public payload/topic/subscription/retention, inventory writer, scheduler or production
change authorized. Separate authorization is required for PE-5.3 and all later checkpoints;
original eight-stage ordering unchanged. PE-6 classification/role_suggestion/metadata_quality
and future Discovery remain outside PE-5.

## Current PE-5.3 repository implementation

Classification: CURRENT. PE5_3_STATUS=COMPLETE_REPOSITORY_IMPLEMENTATION; PE5_4_STARTED=FALSE.
Current next checkpoint: PE-5.4 - PI3 Release Source Synchronization.
The configured mapping resolver, private POSIX composer/store, explicit source installer
and bounded durability recovery are implemented in the repository. Activation remains
disabled; no source provisioning, PI3 synchronization, deployment or production execution
has occurred. PE-5 remains IN_PROGRESS, PE-5.1 remains accepted/closed, PE-4 and Public
Projection remain PASS/CLOSED, and Phase 7A remains ACTIVE.
The PE-5.2 design and its corrected durability contract are unchanged authority.
See [PE-5.3 repository implementation](PE5_CONFIGURED_ASSOCIATION_IMPLEMENTATION.md) and its exact governance payload.
Separate authorization is required for PE-5.4 and every later lifecycle checkpoint.
