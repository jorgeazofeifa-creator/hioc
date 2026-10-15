# HIOC Data Model

## Document Ownership

This document owns entities, relationships, JSON structures, MQTT payload shapes, and internal objects such as inventory, incidents, history, forecasts, capabilities, and platform status.

It should not contain roadmap or implementation-phase information. For roadmap and current phase, see [HIOC_MASTER_PLAN.md](HIOC_MASTER_PLAN.md). For topic names and publishing strategy, see [MQTT.md](MQTT.md).

## Home Assistant Association Authority

Home Assistant association occurs after HIOC identity reconciliation in a
[dedicated association layer](PE4_HOME_ASSISTANT_ASSOCIATION_CONTRACT.md),
with accepted private schema 1.1 state `state/inventory/associations/home_assistant.json`.
It does not create devices, participate in weak-IP promotion, supersede normalized
MAC identity, or become a liveness source. Generic integration inventory ingestion
must not receive HA registry records. HIOC stable device ID references the
existing canonical identity; private association state adds no authoritative MAC,
IP or hostname. HA relationship/metadata fields cannot overwrite operator Asset
fields, canonical identity, passive observations, health or incidents.
Only one valid globally unique HA MAC mapping to exactly one existing HIOC
MAC-backed canonical identity, without prior-binding conflict, permits automatic
association. Public enrichment excludes private HA identifiers by default.

The [0C.1 lifecycle clarification](PE4_HOME_ASSISTANT_ASSOCIATION_LIFECYCLE_CLARIFICATION.md)
adds private binding_history in association-state schema 1.1. Current associations
and historical binding safety memory are both post-identity metadata. Only
current confirmed bindings can project associated=true; history cannot resurrect
HIOC devices or acquire identity/liveness authority. Failed cycles preserve the
entire prior state; successful cycles may retire unconfirmed pairs into bounded
private history without changing canonical inventory.

The association producer retains governed private schema 1.1 and private
transaction/locking authority. The public projection
[production closure](PE4_HOME_ASSISTANT_ASSOCIATION_PUBLIC_PROJECTION_DEPLOYMENT_CLOSURE.md)
is **PASS/CLOSED**, including PI3 POSIX validation, deployment and production acceptance.
Evidence is OPERATOR_SUPPLIED; no fresh production observation occurs here. The
[source implementation](PE4_HOME_ASSISTANT_ASSOCIATION_PUBLIC_PROJECTION_IMPLEMENTATION.md)
remains the historical source checkpoint, not current deployment-status authority.
The inventory engine remains the sole public writer; the optional closed
`home_assistant` device object contains associated=true, association_basis=strong_mac,
entity_count, config-entry integration_domains and has_area_candidate only.
Nonassociated devices omit it. The object is recomputed after identity, never
from binding history or previous public objects. Optional read/validation failure
omits this metadata for the cycle without changing base inventory or private LKG.
Inventory schema 1.0 and every existing identity/liveness/health/Asset boundary
remain unchanged. No generic HA integration ingestion is authorized.

## Living Inventory

Inventory root object:

```json
{
  "schema_version": "1.0",
  "updated": "ISO-8601 timestamp",
  "devices": [],
  "services": [],
  "topology": {},
  "dependencies": {},
  "summary": {}
}
```

Device object:

- `id`: stable ID generated from MAC, then IP, then hostname.
- `display_name`: operator name, hostname, IP, or ID.
- `type`: local host, network device, collector, gateway, or endpoint.
- `roles`: inferred operational roles.
- `ip`
- `mac`
- `hostname`
- `interfaces`
- `firmware`
- `reachable`
- `first_seen`
- `last_seen`
- `last_seen_epoch`
- `observation_status`: `recent`, `stale`, `expired`, `unobserved`, or `unknown`.
- `observation_age_seconds`: age of the last positive observation, or `null` when no timestamp exists.
- `operationally_monitored`: derived monitoring-policy decision used by health and incident correlation.
- `health_score`
- `health_status`
- `health_reasons`
- `parent_id`
- optional integration hints such as `parent_mac`, `parent_ip`, `uplink_mac`, `uplink_ip`, or `parent_device_id`

### Discovered Device and Operator-Managed Asset Metadata

A discovered device record is technical evidence: stable identity, addresses, hostname, interfaces, discovery sources, services, observations, and derived current health. Its provenance must remain visible so consumers can understand what each fact proves.

Operator-managed asset metadata is the human meaning linked to that identity: what the equipment is called, where it is, what it does, who is responsible for it, how important it is, and when it is expected to be available. Some current known-infrastructure fields already provide limited operator enrichment, but HIOC does not yet implement the complete asset model described in [ASSET_MODEL.md](ASSET_MODEL.md).

Technical identity and operator knowledge should remain separable. Rediscovery, DHCP reassignment, or an IP change must not erase confirmed asset knowledge, and operator metadata must not fabricate a technical observation.

### Current Observation Semantics

`first_seen` records the earliest retained discovery time. `last_seen` and `last_seen_epoch` record the last usable positive observation. `observation_age_seconds` is derived from that timestamp and is `null` when no usable timestamp exists.

Current `observation_status` meanings are:

- `recent`: positive evidence is inside the freshness window.
- `stale`: positive evidence is older than the stale threshold; failure is not automatically proven.
- `expired`: positive evidence is older than the offline threshold; failure is not automatically proven.
- `unobserved`: a configured record has not received positive discovery evidence.
- `unknown`: usable positive-observation history is unavailable.

DHCP assignment is identity/address evidence, not liveness, and does not update the positive-observation fields. `operationally_monitored`, health, and incident interpretation are separate policy and derived-state concerns.

### PE-2.1 Asset Metadata

PE-2.0 approved a separate local Asset store keyed by stable device ID. PE-2.1
is implemented, deployed, and production validated; the public inventory schema
remains unchanged.
Its closed private schemas and transaction behavior are frozen in
[PE2_ASSET_IMPLEMENTATION_DESIGN.md](PE2_ASSET_IMPLEMENTATION_DESIGN.md).
The closed schema and validation rules are owned by
[PE2_ASSET_FOUNDATION_SPEC.md](PE2_ASSET_FOUNDATION_SPEC.md).

The approved first operator fields are:

- `friendly_name`;
- `physical_location`;
- `purpose`;
- private `notes`.

The following remain later planning concepts rather than PE-2.1 fields:

- `owner` or responsible person;
- asset `category`;
- operational `criticality`;
- `expected_availability`;
- an explicit `monitoring_policy` or monitoring expectation;
- `lifecycle_state`, such as active, retired, or archived;
- an optional photo reference;
- purchase or installation date;
- maintenance expectations and maintenance history.

Future schema work must preserve operator asset knowledge across IP changes and rediscovery while keeping discovered truth authoritative for observations. Asset classification and expected availability must be designed before they influence archival or incident decisions.

Known infrastructure definitions are optional operator-supplied passive inventory input. The default file is:

```text
/home/jazofv1/hioc/config/inventory/known_infrastructure.json
```

Schema:

```json
{
  "devices": [
    {
      "id": "operator-stable-alias",
      "name": "Office Switch",
      "hostname": "office-switch",
      "ip": "192.168.1.10",
      "mac": "aa:bb:cc:dd:ee:ff",
      "role": "Network Equipment",
      "type": "network_device",
      "vendor": "Netgear",
      "model": "GS108",
      "location": "Network closet",
      "area": "Infrastructure",
      "parent_id": "gateway",
      "parent_device_id": "gateway",
      "parent_mac": "11:22:33:44:55:66",
      "parent_ip": "192.168.1.1",
      "uplink_mac": "11:22:33:44:55:66",
      "uplink_ip": "192.168.1.1",
      "notes": "Operator-owned metadata",
      "enabled": true
    }
  ]
}
```

Supported roles are `Core Infrastructure`, `Network Equipment`, `Server`, `IoT`, `Media`, `Workstation`, `Mobile`, and `Unknown`.

Known definitions enrich observed passive inventory by normalized MAC first, then exact IP or normalized hostname when stronger identifiers do not conflict. Configured metadata can provide operator names, roles, model/vendor details, location, notes, and topology hints. Runtime fields such as observed status, health, last-seen timestamps, and service observations remain owned by passive discovery. A configured device that has never been observed is represented as offline and does not receive a fabricated `last_seen`.

When exactly one MAC-less identity and exactly one MAC-backed identity share an IP, inventory reconciles the weak identity into the canonical MAC-derived device. This applies when either identity is current or retained, including a current IP-only observation matched to one retained MAC-backed identity. The earliest valid `first_seen` and combined discovery provenance are preserved, while current observation timestamps remain current and non-empty stable metadata remains authoritative from the MAC-backed identity. Conflicting or ambiguous MAC identities are never reconciled.

This reconciliation guarantee applies to current inventory and its projections. Historical events or external references may retain an earlier weak IP-derived ID; HIOC currently defines no alias table, promotion record, historical resolution contract, or identity-migration behavior. Those alternatives require a future explicit architecture decision and are not current schema.

The canonical-identity model operates only on supported, unambiguous evidence. Passive reconciliation must not infer that unrelated, randomized, or rotated MAC addresses belong to one physical device. They remain separate discovered identities unless authoritative linking evidence exists. Future operator-approved association of multiple discovered identities with one asset belongs to the planned asset layer described in [ASSET_MODEL.md](ASSET_MODEL.md), not to heuristic passive merging.

Positive evidence creates or refreshes durable inventory. Unresolved neighbor-cache evidence such as `FAILED`, `INCOMPLETE`, `NONE`, or a MAC-less entry is diagnostic-only: it does not create an identity or refresh `last_seen`. Legacy MAC-less records are removed only when their complete provenance is exactly `arp_table`; records supported by any other source remain retained.

Each inventory cycle uses one authoritative ARP/neighbor-table acquisition for both passive device evidence and discovery-source status. A successful acquisition with no accepted evidence is reported as empty, while failure of both the primary and fallback commands is reported as collector unavailability. Unavailability creates no device evidence. Unresolved, MAC-less, and non-durable entries remain diagnostic-only, and the existing accepted and rejected NUD-state behavior is unchanged.

DHCP lease input is passive IPv4 assignment metadata. The supported source format is the Pi-hole/dnsmasq row format: expiry epoch, MAC address, IPv4 address, hostname, and optional client ID. A finite lease is eligible only when its expiry is later than the inventory cycle's fixed collection epoch; expiry zero remains an infinite lease. Expired rows contribute no current assignment evidence, do not enrich retained devices, and do not create offline evidence. IPv6 rows and clearly recognized ISC `dhcpd.leases` blocks are unsupported and contribute no identity record.

Eligible records may contribute `ip`, normalized `mac`, `hostname`, `lease_expires_epoch`, `dhcp_client_id`, and `dhcp_lease_source`, but DHCP cannot overwrite stronger current collector, gateway, ARP, integration, or known-infrastructure identity metadata. A lease never sets reachability and never creates or refreshes `last_seen`. Multiple clients that share an IP remain separate when their normalized MAC addresses differ. Source health distinguishes found, empty, disabled, missing, unreadable, malformed, unsupported, I/O-error, and partial input states without exposing rejected record contents. Empty and explicitly disabled input are complete states; incomplete or unavailable configured input limits discovery while preserving existing inventory and other discovery sources.

Operational monitoring is separate from passive observation. The authoritative policy is `is_operationally_monitored()` in HIOC Core. Infrastructure-class devices, gateway and collector roles/types, known-infrastructure definitions, local-host and gateway records, authoritative integration records, and explicitly monitored records remain monitored. Unknown and future discovery sources default to monitored until their semantics are deliberately added to that policy boundary.

An ordinary client whose complete provenance is limited to `arp_table` and/or `dhcp_leases` remains inventory-visible but is not availability-monitored. Once its passive evidence ages, it remains `watch`, exposes `status: stale` or `status: unknown`, preserves the last positive observation, and does not generate an availability incident from observation age alone. A DHCP-only record remains `watch` with operational status `unknown` even while its assignment observation is current, because DHCP assignment does not prove current reachability.

Passive-client archival or expiration is not defined by this correction. Retention duration and cleanup remain a separate future configurable policy checkpoint.

Service object:

- `id`
- `name`
- `type`
- `device_id`
- `status`
- `port`
- `source`

Topology object:

- `root_id`
- `edges`: parent/child network relationships.

Dependency object:

- `edges`: service dependency relationships such as device-to-DNS, device-to-DHCP, and device-to-MQTT.

## Internal Event

Internal events are stored locally and are not public MQTT contracts.

- `id`
- `type`
- `timestamp`
- `source`
- `payload`

Current inventory event types:

- `DeviceDiscovered`
- `InventoryChanged`
- `TopologyChanged`

## Correlated Incident

Correlated incident state is stored in `state/incidents/active.json`, `state/incidents/history.json`, and `state/incidents/summary.json`.

- `id`: stable incident identifier derived from the correlated root-cause key.
- `key`: duplicate-suppression key for the probable root cause.
- `status`: public compatibility status, typically `active`, `resolved`, or `none`.
- `phase` / `lifecycle`: detailed lifecycle phase: `detected`, `confirmed`, `active`, `recovering`, or `resolved`.
- `severity`: highest correlated severity.
- `system`: primary affected domain.
- `root_cause`: probable root cause.
- `confidence_percent`: root-cause confidence from 0 to 100.
- `affected`: impacted systems and services.
- `evidence`: correlated signal reasons.
- `started`, `updated`, `resolved`, `end_time`: ISO-8601 lifecycle timestamps.
- `duration_seconds`: final incident duration after resolution or supersession.
- `recovery_type`: derived recovery category such as `automatic`, `superseded`, `interrupted`, or `unknown`.
- `review`: operator review generated for completed history entries.

Incident review object:

- `title`
- `severity`
- `started`
- `resolved`
- `duration`
- `duration_seconds`
- `root_cause`
- `confidence_percent`
- `affected_systems`
- `affected_services`
- `impact_summary`
- `evidence`
- `timeline`: chronological event rows with `timestamp` and `message`.
- `recovery`
- `recommended_action`
- `incident_id`
- `recovery_type`

Incident summary includes derived history context:

- `history_stats.today`
- `history_stats.last_7_days`
- `history_stats.last_30_days`
- `history_stats.automatic_recoveries`
- `history_stats.manual_intervention_required`
- `history_stats.average_duration`
- `history_stats.longest_incident`
- `recent_incidents`: compact completed incident rows for dashboard review.
- `recent_incident_reviews`: full review objects for the most recent completed incidents.
- `latest_incident_review`: full review for the most recent completed incident.

## Capability

Capabilities are stored locally in `state/inventory/capabilities.json`.

- `id`
- `device_id`
- `capability`
- `source`
- `status`
- `metadata`

## Platform Version

Platform version state is stored in `state/platform/version.json`.

- `status`
- `updated`
- `versions`

The `versions` object mirrors `VERSION.yaml`.

## Platform Status

Platform status state is stored in `state/platform/status.json`.

- `status`
- `updated`
- `hioc_version`
- `core`
- `dashboard`
- `schema`
- `mqtt_api`
- `build`

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

Classification: HISTORICAL_INTENTIONALLY_PRESERVED PE-5.7 closure snapshot. PE5_7_STATUS=COMPLETE/PASS; RECURRING_EXECUTION_ACTIVE=TRUE.
OPERATOR_SUPPLIED activation/read-only verification reported one accepted marker
and one accepted entry, zero unexpected PE-5 entries, and identical post-activation
crontab SHA256 3f56b904fc1dd40ccbfa3fdd61cb910c4d215e9ac28a9bf2dcdf3721c73b62a9.
No manual composer execution occurred during activation. Natural-cycle evidence and
current output freshness are not established by activation. PE5_8_STARTED=FALSE.
Next: PE-5.8 - Operational Evidence and Independent Production Acceptance;
separate authorization required. No runtime or execution-model change.
See the authoritative [Master Plan](HIOC_MASTER_PLAN.md).

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
See the authoritative [Master Plan](HIOC_MASTER_PLAN.md) for exact receipts and limitations.

## Current PE-5.9 final closure and private PE-6 handoff

Classification: HISTORICAL_INTENTIONALLY_PRESERVED accepted PE-5.9 handoff snapshot. Phase 7A ACTIVE; PE5_STATUS=COMPLETE.
PE5_9_STATUS=COMPLETE/PASS; PE5_8_STATUS=COMPLETE/PASS.
NEXT_CHECKPOINT=PE-6 - Classification & Metadata Quality; PE6_STARTED=FALSE.
Separate authorization is required for PE-6. PE-6 implementation is NOT authorized.

All 37 original PE-5 requirements and all 14 Definition of Done conditions pass;
all 11 roadmap UNKNOWN decisions have evidence-backed resolutions. The original
roadmap and 46 implementation checklist items remain immutable authority.
The current coverage/evidence ledger and complete private handoff are in
[PE-5 implementation evidence](PE5_CONFIGURED_ASSOCIATION_IMPLEMENTATION.md#current-pe-59-final-closure-and-private-pe-6-handoff)
and final_closure in the existing implementation governance record.
PE-5.6/7/8 accepted observations remain OPERATOR_SUPPLIED. Preserve
OPERATOR_OBSERVATIONS_ONLY; FULL_PRODUCTION_BYTES_NOT_RECEIVED;
NO_NATURAL_FAULT_OR_NATIVE_CRASH_CLAIM; NO_CURRENT_FRESHNESS_CLAIM.
First-cycle fields not separately supplied remain UNKNOWN; none is a completion
waiver or new production observation. No runtime, scheduler, public interface,
MQTT or production change occurs here. PE-6 may later consume only validated,
confirmed, unexpired private relationship evidence under the unchanged contract.
Publication remains gated by exact commit, push and independent GitHub verification.

### PE-5 private envelope contract for later PE-6

{"durability": "1.0", "local": "1.0", "output": "2.0", "source": "1.0"}
Source required fields: schema_version, source_id, revision, mappings.
Mapping required fields: mapping_id, endpoint_id, device_id, service_id.
Output required fields: changes, configured, evaluated_at, inventory, local, schema_version, state, valid_until.
Opaque endpoint me_[0-9a-f]{32}; row map_[0-9a-f]{32}; existing strong dev_[0-9a-f]{16}; optional existing same-owner service.
mqra_ + SHA256(ASCII canonical JSON array ['configured_mqtt_v1',source_id,endpoint_id,device_id,service_id,'endpoint_to_device']); excludes revision, mapping_id and evaluation.
source_kind configured_mqtt, rule_id declared_endpoint_device_v1; source_id/revision/digest/mapping_id remain private. Local schema unchanged.
Integer 1..9007199254740991, never bool; approved content changes increment revision; rollback or equal revision with changed content rejected; PENDING recovery floors enforced. No source TTL/observed_at/mtime authority.
Inventory age <=2100 seconds with accepted clock rules; output valid_until=min(evaluated_at+1200,inventory.updated+2100). Reject at now>=valid_until and on future/backward clock or changed consumed inventory/source identity.
The closed embedded local schema has NO state field; local null means unavailable. Root VALID does not assert configured/local branch validity or service health. Exact closed nested schemas remain in the immutable corrected PE-5.2 contract and unchanged runtime schema module; PE-5.9 private_handoff stores their canonical SHA-256 identities. Public inventory and schemas are unchanged.

### Durability and private branch field reference

- **metadata_fields**: ["candidate", "confirmed", "domain", "schema_version", "state", "transaction_id"]
- **metadata_domains**: ["CONFIGURED_MAPPING_SOURCE", "GENERATED_RELATIONSHIP_OUTPUT"]
- **metadata_descriptor_contract**: Closed schema1.0: dur_[0-9a-f]{32} transaction_id; PENDING requires candidate descriptor and nullable prior confirmed; CONFIRMED requires candidate=null and confirmed descriptor. Descriptors contain only sha256 (64 lowercase hex) and source_revision. Source revision is integer1..9007199254740991; output source_revision may be null for no configured revision. Exact current bytes/domain/revision must match; filenames alone are not confirmation.
- **configured_fields**: ["associations", "candidate_count", "error_code", "rejections", "revision", "source_id", "source_sha256", "state"]
- **configured_states**: ["VALID", "UNAVAILABLE"]
- **relationship_fields**: ["device_id", "direction", "endpoint_id", "mapping_id", "relationship_id", "rule_id", "service_id", "source_id", "source_kind", "source_revision", "source_sha256"]
- **changes_fields**: ["added", "added_count", "baseline", "removed", "removed_count", "truncated"]
- **changes_bound**: added/removed relationship-ID arrays at most64 each; exact total counts and truncation flag, no invented removal from unavailable/noncomparable prior.

## Current PE-6 contract design and execution roadmap

Classification: CURRENT. PE5_STATUS=COMPLETE; PE6_STATUS=DESIGN_COMPLETE_RUNTIME_NOT_IMPLEMENTED.
PE6_0_STATUS=COMPLETE_CONTRACT_DESIGN; PE6_RUNTIME_IMPLEMENTED=FALSE.
NEXT_CHECKPOINT=PE-6.1 - Private classification implementation and comprehensive repository validation.
Separate authorization is required for PE-6.1, including adoption or revision of the proposed design.
This checkpoint authorizes no runtime implementation, production operation or PE-7 work.

The [PE-6 contract design](PE6_CLASSIFICATION_CONTRACT_DESIGN.md) inventories actual
capabilities and preserves the complete original authorization, twenty evidence-backed
technical decisions, exact private schema proposal and six-checkpoint roadmap.
Proposed role suggestions and metadata-quality summaries remain private, deterministic
and separate from operator-owned Asset data and public operational role/health.
Asset schema1.0 and the accepted PE-5.9 governance/runtime remain unchanged.
No PE-6 persistence, cron, inventory hook or public projection is selected.
Actual production inputs/locks/runtime state remain UNKNOWN; only later bounded operator
gates may establish them. All previous OPERATOR_SUPPLIED evidence limitations remain.
