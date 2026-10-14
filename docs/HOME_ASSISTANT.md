# HIOC Home Assistant Integration

HIOC integrates with Home Assistant through MQTT sensors, template sensors, and dashboard YAML.

## Document Ownership

This document owns Home Assistant integration: packages, entities, sensors, MQTT discovery behavior, dashboard installation, and dashboard integration points.

It should not duplicate the MQTT contract, data model, dashboard visual design, or dashboard operational-truth policy. For topic details, see [MQTT.md](MQTT.md). For payload fields, see [DATA_MODEL.md](DATA_MODEL.md). For dashboard design and UX rules, see [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md) and [DASHBOARD_V2_PLAN.md](DASHBOARD_V2_PLAN.md). For dashboard truth ownership, layout-baseline protection, and storage-versus-YAML deployment architecture, see [DASHBOARD_ARCHITECTURE.md](DASHBOARD_ARCHITECTURE.md).

PE-4 Home Assistant Association is governed separately by
[PE4_HOME_ASSISTANT_ACCESS_PRIVACY_CONTRACT.md](PE4_HOME_ASSISTANT_ACCESS_PRIVACY_CONTRACT.md).
The current MQTT/YAML integration is consumer-side context, not permission to
read registries, `.storage`, recorder databases, entity states, or credentials.
PE-4.0B.1 credential-free preflight and authenticated 2a/2b proof are PASS/CLOSED.
The dedicated post-identity association adapter, independent production acceptance
and sanitized Public Projection are PASS/CLOSED; recurring scheduler ACTIVE/AUTHORIZED.
See the [Master Plan](HIOC_MASTER_PLAN.md#authoritative-current-pe-4-lifecycle). Evidence is OPERATOR_SUPPLIED; private HA identifiers remain private.
Historical correction boundary: it granted no API access or execution and recorded PE-5 NOT_STARTED then. Current PE-5 IN_PROGRESS; PE-5.1 accepted. The complete roadmap grants no additional HA access, MQTT behavior or public projection.

PE-4.0B.2a is frozen to authenticated `GET /api/` followed by WebSocket
authentication at `/api/websocket`, with no command or data enumeration. See
the access/privacy contract for the official-source basis and exact limits.

## Packages

Installable packages are in `homeassistant/packages`:

- `hioc_incident_center.yaml`
- `hioc_predictive_analytics.yaml`
- `hioc_living_inventory.yaml`
- `hioc_platform.yaml`

The installer copies these files into `/config/packages`.

## Dashboards

Dashboards are in `homeassistant/dashboards` and are copied into `/config/dashboards` by `homeassistant/install_ha.sh`.

The current live Dashboard v2 is storage-managed and does not automatically consume the copied YAML file. The current deployment boundary and the separately planned YAML-mode migration are documented in [DASHBOARD_ARCHITECTURE.md](DASHBOARD_ARCHITECTURE.md).

The Dashboard v2 file is:

- `hioc_dashboard_v2.yaml`

The Living Inventory dashboard uses inventory sensors from `hioc_living_inventory.yaml`.

Correlation Engine v2 uses the existing incident package and sensors wherever possible. Dashboard v2 displays current incident, root cause, confidence, affected systems, and timeline from the retained incident and timeline MQTT payloads without adding a new public MQTT contract.

Dashboard v2 also uses the existing `sensor.hioc_incident_summary` attributes to show incident history context:

- today, 7-day, and 30-day incident counts
- automatic recovery count
- manual intervention count when known
- average and longest incident duration
- recent completed incidents
- the latest completed incident review with impact, evidence, timeline, recovery, and recommended action

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

Classification: HISTORICAL_INTENTIONALLY_PRESERVED PE-5.3 completion snapshot. PE5_3_STATUS=COMPLETE_REPOSITORY_IMPLEMENTATION; PE5_4_STARTED=FALSE.
Current next checkpoint: PE-5.4 - PI3 Release Source Synchronization.
The configured mapping resolver, private POSIX composer/store, explicit source installer
and bounded durability recovery are implemented in the repository. Activation remains
disabled; no source provisioning, PI3 synchronization, deployment or production execution
has occurred. PE-5 remains IN_PROGRESS, PE-5.1 remains accepted/closed, PE-4 and Public
Projection remain PASS/CLOSED, and Phase 7A remains ACTIVE.
The PE-5.2 design and its corrected durability contract are unchanged authority.
See [PE-5.3 repository implementation](PE5_CONFIGURED_ASSOCIATION_IMPLEMENTATION.md) and its exact governance payload.
Separate authorization is required for PE-5.4 and every later lifecycle checkpoint.

## Current PE-5.6 production validation closure

Classification: HISTORICAL_INTENTIONALLY_PRESERVED PE-5.6 closure snapshot. PE5_6_STATUS=COMPLETE/PASS; PE5_7_STARTED=FALSE.
OPERATOR_SUPPLIED evidence records accepted corrected deployment, one successful
corrected source initialization and exactly one successful bounded composer execution.
Recurring execution remains disabled. The failed first initialization and its
bootstrap correction remain historical evidence. No runtime/authority contract changes.
Next: PE-5.7 - Conditional Execution Activation; separate authorization required.
See the authoritative [Master Plan](HIOC_MASTER_PLAN.md) and its linked implementation evidence.

## Current PE-5.7 activation closure

Classification: CURRENT. PE5_7_STATUS=COMPLETE/PASS; RECURRING_EXECUTION_ACTIVE=TRUE.
OPERATOR_SUPPLIED activation/read-only verification reported one accepted marker
and one accepted entry, zero unexpected PE-5 entries, and identical post-activation
crontab SHA256 3f56b904fc1dd40ccbfa3fdd61cb910c4d215e9ac28a9bf2dcdf3721c73b62a9.
No manual composer execution occurred during activation. Natural-cycle evidence and
current output freshness are not established by activation. PE5_8_STARTED=FALSE.
Next: PE-5.8 - Operational Evidence and Independent Production Acceptance;
separate authorization required. No runtime or execution-model change.
See the authoritative [Master Plan](HIOC_MASTER_PLAN.md).
