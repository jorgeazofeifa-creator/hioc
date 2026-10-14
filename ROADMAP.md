# HIOC Roadmap

## Document Ownership

This file is the short public roadmap summary.

The detailed implementation roadmap is maintained in [docs/HIOC_MASTER_PLAN.md](docs/HIOC_MASTER_PLAN.md).

## Current Phase

Phase 7A - Passive Living Inventory.

Goal: enrich the Living Inventory using passive infrastructure data only.

## Authoritative Passive-Enrichment Sequence

The detailed status and sequencing authority is
[docs/HIOC_MASTER_PLAN.md](docs/HIOC_MASTER_PLAN.md). The agreed order is:

1. PE-1 - Hostname Enrichment — complete, production validated.
2. PE-2 - Asset Foundation — complete, production validated.
3. PE-3 - Manufacturer Reference Enrichment — PE-3.0 through PE-3.3 and
   production Actions 1-10 complete; deployment and PI3 validation complete.
4. PE-4 - Home Assistant Association — PASS/CLOSED; Public Projection PASS/CLOSED.
5. PE-5 - MQTT and Passive Service Association — IN PROGRESS; PE-5.1 accepted; wider PE-5 incomplete. Next: PE-5.3 - Remaining Capability Implementation and Comprehensive Validation; all eight remaining stages through PE-5.9 / PE-6 are defined in the Master Plan.
6. PE-6 - Classification & Metadata Quality — not started.
7. PE-7 - Expected Availability & Permanent IoT Monitoring — planned.
8. PE-8 - Automation Correlation & Impact Analysis — planned.
9. PE-9 - Service & Infrastructure Dependency Intelligence — planned.
10. PE-10 - Application, Integration & Service Assurance - planned / not started.

Retention/archival, DHCP service health/capacity, notification semantics,
incident-history validator hardening, infrastructure disaster recovery, and
hardware migration remain separate governed future checkpoints.

## Next Phase

Phase 7B - Safe Active Discovery.

Status: planned, not started.

Active discovery remains postponed until Phase 7A is complete.

## Future Phases

Future work is tracked in [docs/HIOC_MASTER_PLAN.md](docs/HIOC_MASTER_PLAN.md).

## Current PE-5.2 complete contract design

Classification: CURRENT. PE5_2_STATUS=COMPLETE_CONTRACT_DESIGN; PE5_3_STARTED=FALSE.
Current next checkpoint: PE-5.3 - Remaining Capability Implementation and Comprehensive Validation.
See [PE-5.2 complete contract design](docs/PE5_MAPPING_CONTRACT_DESIGN.md) and
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
