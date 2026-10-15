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
5. PE-5 - MQTT and Passive Service Association — COMPLETE; PE-5.9 COMPLETE/PASS. PE-6 contract design complete; PE-6.1 implementation/validation next, separately authorized.
6. PE-6 - Classification & Metadata Quality — contract design COMPLETE; runtime NOT_IMPLEMENTED. Next: PE-6.1 implementation/validation under separate authorization.
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

Classification: HISTORICAL_INTENTIONALLY_PRESERVED PE-5.2 lifecycle snapshot at 72e878f9c0c8f5d3fe6357979e045943f3cf9d34. PE5_2_STATUS=COMPLETE_CONTRACT_DESIGN; PE5_3_STARTED=FALSE.
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

## Current PE-5.3 repository implementation

Classification: HISTORICAL_INTENTIONALLY_PRESERVED PE-5.3 completion snapshot. PE5_3_STATUS=COMPLETE_REPOSITORY_IMPLEMENTATION; PE5_4_STARTED=FALSE.
Current next checkpoint: PE-5.4 - PI3 Release Source Synchronization.
The configured mapping resolver, private POSIX composer/store, explicit source installer
and bounded durability recovery are implemented in the repository. Activation remains
disabled; no source provisioning, PI3 synchronization, deployment or production execution
has occurred. PE-5 remains IN_PROGRESS, PE-5.1 remains accepted/closed, PE-4 and Public
Projection remain PASS/CLOSED, and Phase 7A remains ACTIVE.
The PE-5.2 design and its corrected durability contract are unchanged authority.
See [PE-5.3 repository implementation](docs/PE5_CONFIGURED_ASSOCIATION_IMPLEMENTATION.md) and its exact governance payload.
Separate authorization is required for PE-5.4 and every later lifecycle checkpoint.

## Current PE-5.6 production validation closure

Classification: HISTORICAL_INTENTIONALLY_PRESERVED PE-5.6 closure snapshot. PE5_6_STATUS=COMPLETE/PASS; PE5_7_STARTED=FALSE.
OPERATOR_SUPPLIED evidence records accepted corrected deployment, one successful
corrected source initialization and exactly one successful bounded composer execution.
Recurring execution remains disabled. The failed first initialization and its
bootstrap correction remain historical evidence. No runtime/authority contract changes.
Next: PE-5.7 - Conditional Execution Activation; separate authorization required.
See the authoritative [Master Plan](docs/HIOC_MASTER_PLAN.md) and its linked implementation evidence.

## Current PE-5.7 activation closure

Classification: HISTORICAL_INTENTIONALLY_PRESERVED PE-5.7 closure snapshot. PE5_7_STATUS=COMPLETE/PASS; RECURRING_EXECUTION_ACTIVE=TRUE.
OPERATOR_SUPPLIED activation/read-only verification reported one accepted marker
and one accepted entry, zero unexpected PE-5 entries, and identical post-activation
crontab SHA256 3f56b904fc1dd40ccbfa3fdd61cb910c4d215e9ac28a9bf2dcdf3721c73b62a9.
No manual composer execution occurred during activation. Natural-cycle evidence and
current output freshness are not established by activation. PE5_8_STARTED=FALSE.
Next: PE-5.8 - Operational Evidence and Independent Production Acceptance;
separate authorization required. No runtime or execution-model change.
See the authoritative [Master Plan](docs/HIOC_MASTER_PLAN.md).

## Current PE-5.8 operational acceptance closure

Classification: HISTORICAL_INTENTIONALLY_PRESERVED PE-5.8 closure snapshot. PE5_8_STATUS=COMPLETE/PASS; RECURRING_EXECUTION_ACTIVE=TRUE.
OPERATOR_SUPPLIED observations establish three consecutive natural successful
windows (:17/:32/:47), distinct outputs and CONFIRMED transactions, unchanged
source revision1/SHA and accepted scheduler SHA. No manual PE-5.8 producer run.
Overlap/missed-cycle/expiry/failure/corruption evidence is committed synthetic
Windows validation and static contract evidence, not naturally observed faults.
Local envelope has no state field. Production hashes were operator-supplied;
full production bytes and freshness after observation times are not asserted.
PE-5 remains IN_PROGRESS. PE5_9_STARTED=FALSE.
Next: PE-5.9 - Final PE-5 Closure and PE-6 Handoff; separate authorization required.
See the authoritative [Master Plan](docs/HIOC_MASTER_PLAN.md) for exact receipts and limitations.

## Current PE-5.9 final closure and private PE-6 handoff

Classification: HISTORICAL_INTENTIONALLY_PRESERVED accepted PE-5.9 handoff snapshot. Phase 7A ACTIVE; PE5_STATUS=COMPLETE.
PE5_9_STATUS=COMPLETE/PASS; PE5_8_STATUS=COMPLETE/PASS.
NEXT_CHECKPOINT=PE-6 - Classification & Metadata Quality; PE6_STARTED=FALSE.
Separate authorization is required for PE-6. PE-6 implementation is NOT authorized.

All 37 original PE-5 requirements and all 14 Definition of Done conditions pass;
all 11 roadmap UNKNOWN decisions have evidence-backed resolutions. The original
roadmap and 46 implementation checklist items remain immutable authority.
The current coverage/evidence ledger and complete private handoff are in
[PE-5 implementation evidence](docs/PE5_CONFIGURED_ASSOCIATION_IMPLEMENTATION.md#current-pe-59-final-closure-and-private-pe-6-handoff)
and final_closure in the existing implementation governance record.
PE-5.6/7/8 accepted observations remain OPERATOR_SUPPLIED. Preserve
OPERATOR_OBSERVATIONS_ONLY; FULL_PRODUCTION_BYTES_NOT_RECEIVED;
NO_NATURAL_FAULT_OR_NATIVE_CRASH_CLAIM; NO_CURRENT_FRESHNESS_CLAIM.
First-cycle fields not separately supplied remain UNKNOWN; none is a completion
waiver or new production observation. No runtime, scheduler, public interface,
MQTT or production change occurs here. PE-6 may later consume only validated,
confirmed, unexpired private relationship evidence under the unchanged contract.
Publication remains gated by exact commit, push and independent GitHub verification.

## Current PE-6 contract design and execution roadmap

Classification: CURRENT. PE5_STATUS=COMPLETE; PE6_STATUS=DESIGN_COMPLETE_RUNTIME_NOT_IMPLEMENTED.
PE6_0_STATUS=COMPLETE_CONTRACT_DESIGN; PE6_RUNTIME_IMPLEMENTED=FALSE.
NEXT_CHECKPOINT=PE-6.1 - Private classification implementation and comprehensive repository validation.
Separate authorization is required for PE-6.1, including adoption or revision of the proposed design.
This checkpoint authorizes no runtime implementation, production operation or PE-7 work.

The [PE-6 contract design](docs/PE6_CLASSIFICATION_CONTRACT_DESIGN.md) inventories actual
capabilities and preserves the complete original authorization, twenty evidence-backed
technical decisions, exact private schema proposal and six-checkpoint roadmap.
Proposed role suggestions and metadata-quality summaries remain private, deterministic
and separate from operator-owned Asset data and public operational role/health.
Asset schema1.0 and the accepted PE-5.9 governance/runtime remain unchanged.
No PE-6 persistence, cron, inventory hook or public projection is selected.
Actual production inputs/locks/runtime state remain UNKNOWN; only later bounded operator
gates may establish them. All previous OPERATOR_SUPPLIED evidence limitations remain.
