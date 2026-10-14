# PE-5.2 Mapping Source Authority and Complete Contract Design

Classification: CURRENT. PE5_2_STATUS=COMPLETE_CONTRACT_DESIGN.
PE5_3_STARTED=FALSE. PE-5 remains IN_PROGRESS; PE-5.1 remains accepted and closed.
Next: PE-5.3 - Remaining Capability Implementation and Comprehensive Validation.
Separate authorization is required. No runtime implementation, source provisioning,
deployment, activation, live MQTT/HA/PI3/PI5 access or PE-6 implementation is granted.

## Evidence and corrected premise

Baseline: 78ee4cd16120bf4ea3166901994727a19d1faad1 (accepted complete roadmap).
Original architecture/preparation require declared configured MQTT mappings but establish
no deployed mapping authority/store/freshness mechanism. An undefined mechanism is a
design responsibility, not proof a generic mapping store existed. No universal production
absence is claimed.

OPERATOR_SUPPLIED observation on nutandpihole as jazofv1 established runtime root/config
files, no integration/known-infrastructure override declarations in those files, absent
default integration directory and known_infrastructure.json 785 bytes mode 0640 UID/GID 1000/1000.
Environment overrides were not observed. This proves neither mapping authority nor absence
elsewhere. Known infrastructure is operator-supplied DEVICE METADATA under its committed
consumer, not a MQTT relationship source.

Two later proposed observations were NOT EXECUTED and are SUPERSEDED. Additional
production observation is NOT REQUIRED for this design. Former inventory items 1/31/32/33
become DESIGN DECISIONS about the new source; item 2 is an established REPOSITORY FACT;
item 34 is NOT REQUIRED. All original 30 design requirements are resolved below.

Preserved conceptual context: Ring camera -> Ring cloud -> Ring-MQTT -> Mosquitto ->
HA MQTT entities -> HIOC. Not newly verified live topology. Broker and individual-device
health remain distinct. Dependency correlation/classification belongs to later authority.

## Source choice and alternatives

Selected: HIOC-owned operator-declared private configuration with a closed schema.
This directly implements declared mappings with deterministic auditable revisions,
privacy, testability and isolated failures without transport interrogation.
Maintainer approval grants configuration authority; filesystem ownership alone does not.

Rejected: automatic promotion of known-infrastructure/integration device metadata,
whose existing contracts do not grant relationship authority. Rejected: broker/HA/client/
Discovery harvesting, which does not establish declared ownership and adds unapproved
credential/payload/discovery scope. Combination is limited to the unchanged local-service
result and a separately typed configured branch. Future Discovery requires distinct
provenance and separate authorization.

## Complete contract decisions

### Premise

- **preexisting_generic_mapping_store_required**: false
- **original_deployed_authority**: UNDEFINED
- **original_deployed_store**: UNDEFINED
- **original_mapping_freshness**: UNDEFINED
- **production_absence_claimed**: false
- **additional_production_observation_required**: false
- **superseded_unexecuted_procedures**: ["redacted-known-infrastructure-only", "interactive-maintainer-attestation"]

### Source

- **authority**: Operator-approved explicit configuration, accepted only after closed-schema/identity/revision validation; filesystem ownership alone is insufficient
- **availability**: Required for a complete configured branch. Absence is SOURCE_ABSENT, never proof no relationships or no devices. Explicit approved empty mappings array is valid known-empty configuration; operator source provisioning occurs only in later authorized deployment.
- **consumers**: ["Future PE-5.3 private composer only"]
- **failure**: Absent/unreadable/wrong owner/mode/link/schema/bounds/corruption -> configured branch unavailable, safe fixed error code; no partial source ingestion. Existing local branch may remain separately valid.
- **limits**: {"mappings": 4096, "source_bytes": 262144}
- **model**: HIOC-owned operator-declared private JSON configuration
- **owner**: jazofv1
- **path**: /home/jazofv1/hioc/config/enrichment/mqtt_mappings.json
- **privacy**: Private 0700 source directory, 0600 regular single-link non-symlink file; owner resolved from jazofv1 during future deployment. Source excluded from Git/release/public MQTT/HA. No labels, topic strings, URLs, client IDs, credentials or private authentication material.
- **revision**: Integer 1..9007199254740991; every authorized content change increments revision. Canonical SHA256 identifies complete content. Normal installer anchors come only from CONFIRMED source/output persistence identities, never a PENDING visible revision. Equal confirmed revision with changed digest or lower revision is rejected. No valid anchor requires explicit operator-approved initialization/recovery. A different replacement during pending recovery must exceed both prior confirmed and pending candidate source revisions; recertification of the exact recorded candidate may retain its revision. No historical anti-rollback proof is claimed.
- **schema_version**: 1.0
- **selection**: One fixed production-root-relative path; no config/environment fallback, known-infrastructure/integration auto-promotion, globbing or live discovery
- **source_id**: operator_mqtt_v1
- **time**: Configuration state, not observation. No observed_at/last_seen timestamp or file mtime authority. Active declarations remain until replaced/removed; no wall-clock TTL. Inventory validity is checked independently at each evaluation with accepted 2100-second policy.
- **update**: Under the shared PE-5 lock, validate candidate/source/identity/revision and prepare a durable PENDING sidecar with prior confirmed identity and candidate identity BEFORE primary replacement. Use exclusive same-directory non-authoritative temp, mode0600, flush/fsync(file), os.replace(primary), fsync(primary parent). Only after primary durability succeeds write CONFIRMED sidecar, fsync its file/parent. Source/output remain distinct; no secrets/network. Failure boundaries/recovery are defined in atomic_durability.
- **writer**: Authorized operator using a future PE-5.3 offline configuration validator and atomic installer; no broker/HA/existing inventory writer
- **configuration_authority**: Future offline installer accepts only an explicit operator-approved artifact; composer reads only fixed path. No empty configuration automatically created by deployment: absent source remains unavailable until separately authorized operator provisioning. Source schema lives in this governed contract, then PE-5.3 validator/exact installed schema; permission ownership is a necessary safety check, not the producer-authority proof.


### Relationships

- **cardinality**: One endpoint has at most one declared target device and optional service; many endpoints may attach to one device. No topic fanout inference.
- **conflict**: Malformed source/duplicate/conflicting declarations -> no accepted configured associations for that cycle. Local and configured branches retain distinct provenance; no authoritative field overwrite or endpoint/name/IP fuzzy joins.
- **device_pattern**: ^dev_[0-9a-f]{16}$
- **difference**: Compare semantic relationship ID sets with prior valid configured output only when both snapshots are consumable. Sorted added/removed IDs limited to 64 each plus exact totals/truncated flag; initial/invalid prior state yields baseline=false and no fabricated removal claims.
- **direction**: endpoint_to_device; descriptive association only
- **duplicates**: Exact duplicate rows and repeated mapping_id invalidate the entire source. Multiple rows with same endpoint, even same owner, invalidate the source; conflicting endpoint owners are configuration conflict, not inferred merge.
- **endpoint_pattern**: ^me_[0-9a-f]{32}$
- **identity**: Target must exist exactly once in finalized inventory with valid normalized MAC, ID==existing stable_device_id(MAC), no MAC collision; mapping cannot create/merge identities or override IP. Missing/weak/ambiguous device -> rejection, never synthetic device.
- **mapping_pattern**: ^map_[0-9a-f]{32}$
- **meaning**: DECLARED_ENDPOINT_DEVICE_ASSOCIATION: operator assertion that an opaque MQTT/integration endpoint belongs to an already reconciled device; not ownership discovery, connectivity, health, role or a dependency graph
- **missing**: Unknown endpoint is not probed. Opaque declared endpoint requires no independent live existence proof. Missing target device/service -> per-row rejection. Service owner mismatch or ambiguous service ID -> per-row rejection.
- **provenance**: source_kind=configured_mqtt; source_id; source revision and digest; mapping_id; rule_id=declared_endpoint_device_v1. Future discovery evidence needs separately authorized source_kind and rules; never silently shares configured authority.
- **relationship_id**: mqra_ + SHA256(ASCII canonical JSON array ['configured_mqtt_v1',source_id,endpoint_id,device_id,service_id,'endpoint_to_device']). mapping_id/revision/evaluation time are excluded so unchanged semantic bindings retain IDs.
- **service**: Null or an existing finalized inventory service ID whose strongly bound owner is the same device; no new service inferred. Supported ID grammar remains the closed PE-5.1 service ID grammar.
- **identifier_allocation**: Operator allocates endpoint_id and mapping_id once as UUID4 lowercase32-hex with me_/map_ prefixes and maintains their binding in private configuration. They do not derive from topic/IP/name/device labels. Preserve endpoint_id when configuration revision changes; retire and allocate a new ID for a different endpoint. Mapping row IDs do not confer identity authority.


### Mqtt

- **live_broker_access_required**: false
- **subscription_required**: false
- **discovery_subscriber_required**: false
- **publication_required**: false
- **client_enumeration_required**: false
- **topic_content_reading_required**: false
- **reason**: Input is explicit local configuration of opaque endpoint bindings. Evaluation requires only configuration plus reconciled local inventory, not broker presence, payloads, topics, HA entities or clients. Existing MQTT publishers/subscriptions/retention are unchanged; Ring -> cloud -> Ring-MQTT -> Mosquitto -> HA -> HIOC is preserved context, not verified live topology or authority to interrogate it.
- **raw_topics_required**: false

### Persistence

- **atomic**: Under the shared flock, durable PENDING intent must precede any primary os.replace. Primary write order remains exclusive temp0600 -> flush/fsync(file) -> os.replace(primary) -> fsync(primary parent). PRE_REPLACEMENT_FAILURE preserves prior authoritative pathname/bytes (if present); temp is non-authoritative and safely cleaned. Successful primary replacement plus failed parent fsync is POST_REPLACEMENT_DURABILITY_FAILURE: replacement may be visible, prior physical presence is NOT guaranteed, durability INDETERMINATE, fail closed and report WRITE_FAILED; no automatic rollback or second primary replacement. Confirmation metadata follows primary durability success; details in atomic_durability. Reject unsafe metadata/links; no multi-file atomicity claimed. Never truncate the primary in place; retain unchanged source snapshot, symlink/nonregular/hardlink and metadata rejection gates.
- **backup_recovery**: Source backups remain separately authorized/private; no new backup job. Generated current is reproducible and is not restored as authority. Logical confirmed persistence metadata cannot recreate old payloads. Source rollback/replacement still needs explicit approval and appropriate higher revision. Pending recovery recertifies recorded visible bytes through successful fsync or uses a separately authorized fresh producer replacement; never automatic rollback. No PE-4 journals touched.
- **corruption**: Invalid source/input/output keeps its original unavailable/rejection semantics. Missing/invalid/inconsistent durability metadata or PENDING state additionally blocks confirmation/consumption. A valid-looking visible file is insufficient evidence of confirmed durability. No automatic reconstruction of missing old payloads and no assumed crash survival.
- **directory_mode**: 0700
- **file_mode**: 0600
- **history**: One primary current envelope plus one fixed-size private durability sidecar per source/output domain; no payload archive, hidden last-valid relationship store or generic journal. CONFIRMED descriptors supply comparison/revision anchors; PENDING descriptors are logical recovery authority only, never usable associations. Ordinary prior-receipt comparison still requires valid/fresh evidence; no LKG promotion from mere visibility.
- **lkg**: Application lkg_required remains FALSE: no automatic stale-association fallback. The logical persistence LKG is only the last confirmed durable artifact ID/hash/revision, not retained relationship payloads. Before successful primary replacement, prior bytes remain unchanged. After successful replacement and failed parent fsync, prior physical presence is NOT guaranteed; PENDING.confirmed retains the prior logical confirmed identity and visible candidate is not promoted. Persistence uncertainty blocks consumer use until deterministic explicit recovery.
- **lkg_required**: false
- **output_bytes**: 16777216
- **output_path**: /home/jazofv1/hioc/state/enrichment/service_associations/current.json
- **owner**: jazofv1
- **readers**: ["Future PE-6 private reader", "Authorized operator bounded private validator"]
- **reason**: Durable operator configuration is necessary across restarts; a private current relationship receipt provides atomic PE-6 consumption, provenance/revision checks and bounded changes without changing public inventory.
- **required**: true
- **restart**: Next invocation validates private metadata and primary binding under the lock. PENDING, malformed/missing sidecar with an existing primary, or digest/domain/revision mismatch -> fail closed, WRITE_FAILED, no replacement/consumption of the affected primary domain and explicit operator recovery. CONFIRMED is a witness written only after primary fsync success; matching primary may pass existing application validators. No-schema-valid receipt is inferred from visibility. Missing primary and sidecar is initialization only under existing source approval/first-run rules. Corrupt prior receipt still requires explicit recovery; no stale fallback.
- **retention**: One current primary and one bounded durability sidecar per domain. Sidecar max8192 bytes, contains identities/revisions only. Owned exclusive temp artifacts are non-authoritative and safely removed on handled failure; stale crash temps never followed/used and require bounded authorized cleanup. No unbounded journal/backup/history. Sidecars are not auto-deleted while recovery is pending.
- **schema_version**: 2.0
- **writer**: One future PE-5.3 standalone private composer; never inventory-engine or PE-5.1 caller modifications
- **schema_storage**: Design input/output schemas are embedded in governance/pe5/pe5-mapping-contract-design.json and printed in docs/PE5_MAPPING_CONTRACT_DESIGN.md. PE-5.3 must materialize or deterministically embed these exact schemas in its validator; installed schema hashes bind during PE-5.5. No runtime schema is installed now.


### Execution

- **cadence_seconds**: 900
- **clock**: UTC evaluated_at and valid_until. Future timestamp, backward clock relative to prior valid receipt, or invalid clock => fail closed. valid_until=min(evaluated_at+1200 seconds, inventory.updated+2100 seconds). New schema distinguishes evaluation time from observations.
- **failure**: Source/input/receipt errors retain original unavailable/fixed-code/nonzero semantics. PRE_REPLACEMENT_FAILURE preserves prior primary bytes when present. POST_REPLACEMENT_DURABILITY_FAILURE may leave replacement visible; prior file is not guaranteed, primary durability INDETERMINATE, execution fails closed with WRITE_FAILED and safe phase diagnostics. No success/durable-commit claim or automatic rollback. Pending recovery blocks normal subsequent writes/consumption of the affected primary domain; confirmed old identity remains logical LKG only. Confirmation-metadata failure is separately classified as described in atomic_durability. Source failure still yields an unavailable configured branch; invalid inventory/clock/receipt still yields whole unavailable output when safe publication is possible, with nonzero return and fixed sanitized diagnostics.
- **handoff_max_age_seconds**: 1200
- **inventory_max_age_seconds**: 2100
- **lock**: /home/jazofv1/hioc/state/enrichment/service_associations/.lock; owner jazofv1 mode0600 in0700 directory; fcntl.flock LOCK_EX|LOCK_NB shared by composer and source installer
- **missed**: No catch-up. Next normal cycle recomputes from current inputs. PE-6 expires old receipt at 1200 seconds or input expiry, whichever earlier; scheduler presence does not prove success.
- **model**: Separate private standalone composer; accepted PE-5.1 pure resolver may be reused with unchanged schema/rules, but accepted caller executable and inventory engine remain byte-identical. No additional PE-5.1 execution occurs during PE-5.2.
- **operational_evidence**: PE-5.8 requires at least three consecutive natural successful cycles plus synthetic/native bounded overlap, missed-cycle expiry, invalid/absent source and restart/corruption cases at PE-5.6/8; no destructive production faults without separate explicit authority.
- **overlap**: No waiting/backlog; overlapping invocation returns fixed OVERLAP_SKIPPED code without replacing output. Lock FD held for full read/validate/write transaction; OS releases on exit/restart.
- **recurring_required**: true
- **retry**: No retry loop; next scheduled cycle. Manual bounded future diagnostic only with separate authority, no implicit second historical execution.
- **trigger**: Future PE-5.7 operator-authorized jazofv1 cron entry: 2,17,32,47 * * * * using absolute future composer path and fixed root; disabled through PE-5.5. These are new design values, not observed schedule.
- **command_interface**: Future PE-5.3 entrypoint /home/jazofv1/hioc/pi4/bin/hioc-compose-service-associations.py: standalone no-network execution with fixed /home/jazofv1/hioc root and no environment/config overrides. Operator-managed source updates use future offline installer /home/jazofv1/hioc/pi4/bin/hioc-install-mqtt-mappings.py with explicitly supplied secret-free candidate file, no shell sourcing. Entry point bytes are PE-5.3 outputs; interfaces/paths selected here.
- **input_path**: /home/jazofv1/hioc/state/inventory/inventory.json; read finalized producer artifact only; no inventory engine execution or write


### Handoff

- **path**: /home/jazofv1/hioc/state/enrichment/service_associations/current.json
- **schema_version**: 2.0
- **content**: Private envelope of untouched PE-5.1 schema1.0 result (or null if unavailable) and separately typed configured branch; inventory digest/updated time; source revision/digest; evaluation/deadline; provenance, accepted associations and safe rejection/error counts; bounded changes. No MQTT topics, payloads, credentials, names, health/status classifications, raw IP or MAC copied into configured output.
- **validity**: The output primary always requires a matching private CONFIRMED durability sidecar. A configured branch claimed VALID additionally requires a matching CONFIRMED source sidecar and source hash/revision. PENDING, missing/malformed/inconsistent confirmation blocks consumption of the affected artifact, never promotes visible candidates. Source absence or uncertainty retains the original configured-unavailable semantics; an independently valid local branch may remain consumable when the output itself is confirmed and all unchanged local/current-input/freshness/deadline gates pass. Neither branch may bypass its own confirmation or schema/provenance/identity gates. Recertification never refreshes evaluated_at/valid_until or identity/liveness/health.
- **authority**: Descriptive evidence only; PE-6 owns role_suggestion, metadata_quality and classification. No PE-6 implementation or public projection here.
- **future_discovery**: Different source_kind/schema/rule explicitly versioned under later authority. No configured provenance laundering of broker/HA/Discovery observations.

### Decision Count

30

### Next Checkpoint

"PE-5.3"

### Runtime Implementation Authorized

false

### Production Mutation Authorized

false

### Schemas Semantics

- **atomic_input**: Source and inventory fingerprints/stat stable before/after read and immediately before output replace. Change aborts with SOURCE_CHANGED or INVENTORY_INVALID. Later changes invalidate consumer use through same-current digest comparisons. Each artifact used as valid evidence additionally requires its matching CONFIRMED durability sidecar, read consistently under the shared lock; uncertainty never promotes visible candidates. An unavailable configured branch grants no source authority and retains the original independently valid local-branch semantics.
- **comparison**: All configured rows share validated source revision/digest. baseline=false => zero changes/counts; baseline=true => exact complete difference counts, sorted arrays capped64, accurate truncation flag. Unavailable branches never report fabricated removals.
- **deadlines**: VALID deadline strictly after evaluation and no later than evaluation+1200 or inventory.updated+2100. Whole UNAVAILABLE deadline==evaluation. Invalid clock produces no fabricated timestamp or replacement; fixed failure, old receipt expires.
- **deployment**: Exact installed bytes are PE-5.3 implementation outputs; entrypoint/installer paths and interfaces are already defined here. PE-5.5 installs disabled runtime plus schemas, preserving existing source and refusing unexpected target contents. No source auto-created. PE-5.6 requires approved real positive mapping plus bounded nonactive negative fixtures. The two private durability sidecars are generated runtime metadata, not release payload or operator mapping data. Existing primary without valid confirmation requires explicit bounded bootstrap/recovery, never automatic adoption.
- **local**: Embedded PE-5.1 result must pass unchanged validator, policy2100, same inventory digest/time/evaluation. No local schema/rule/caller changes.
- **root_state**: VALID means current inventory/time prerequisites usable, not that all branches are valid. UNAVAILABLE means no branch consumable. local=null means unavailable, never zero confirmed local associations.
- **schema_evolution**: New kinds/fields/identifier grammar require separately governed schema/rule version. Output2.0 wraps unchanged local1.0; never silently substitutes it.
- **serialization**: Sorted associations by relationship_id; rejections by mapping_id/code. Canonical ASCII compact sorted-key JSON plus LF; strict UTF-8; duplicate JSON keys and NaN/infinities rejected; byte/array bounds applied before ingestion.
- **source_install**: Installer/composer share the same lock. Revision/comparison anchors must be CONFIRMED, bound to current schema-valid source or valid prior receipt. PENDING visible data never becomes an anchor; block normal transactions until explicit recovery. No hidden payload-LKG store; initialization/recovery remains explicitly approved. Composer never writes source.
- **source_state**: Configured VALID requires revision/digest, null error_code, candidate_count==accepted+rejected, unique IDs/endpoint declarations. UNAVAILABLE requires empty accepted associations and fixed nonnull error; revision/digest null and candidate_count/rejections zero when source cannot be safely validated. Persistence uncertainty uses existing WRITE_FAILED safe error code and out-of-band fixed phase diagnostics; no new mapping/output fields or MQTT publication.


## All 30 design resolutions

| # | Decision | Contract |
|---|---|---|
| 1 | mapping source/store location | source — RESOLVED_DESIGN |
| 2 | mapping producer/owner authority | source — RESOLVED_DESIGN |
| 3 | mapping identifiers | relationships — RESOLVED_DESIGN |
| 4 | exact relationship meaning | relationships — RESOLVED_DESIGN |
| 5 | timestamp versus configuration version | source — RESOLVED_DESIGN |
| 6 | freshness | source — RESOLVED_DESIGN |
| 7 | expiry | source — RESOLVED_DESIGN |
| 8 | conflicts | relationships — RESOLVED_DESIGN |
| 9 | privacy | source — RESOLVED_DESIGN |
| 10 | credentials/secrets | source — RESOLVED_DESIGN |
| 11 | storage necessity | persistence — RESOLVED_DESIGN |
| 12 | storage artifact/schema | persistence — RESOLVED_DESIGN |
| 13 | storage ownership | persistence — RESOLVED_DESIGN |
| 14 | storage permissions | persistence — RESOLVED_DESIGN |
| 15 | atomic writes | persistence — RESOLVED_DESIGN |
| 16 | readers/writers | persistence — RESOLVED_DESIGN |
| 17 | current/history | persistence — RESOLVED_DESIGN |
| 18 | retention | persistence — RESOLVED_DESIGN |
| 19 | LKG | persistence — RESOLVED_DESIGN |
| 20 | restart | persistence — RESOLVED_DESIGN |
| 21 | corruption | persistence — RESOLVED_DESIGN |
| 22 | recurrence | execution — RESOLVED_DESIGN |
| 23 | trigger | execution — RESOLVED_DESIGN |
| 24 | cadence | execution — RESOLVED_DESIGN |
| 25 | producer/integration | execution — RESOLVED_DESIGN |
| 26 | locking | execution — RESOLVED_DESIGN |
| 27 | overlap | execution — RESOLVED_DESIGN |
| 28 | missed execution | execution — RESOLVED_DESIGN |
| 29 | failure | execution — RESOLVED_DESIGN |
| 30 | PE-6 private handoff | handoff — RESOLVED_DESIGN |

## Closed source schema (design only)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Private configured MQTT mappings 1.0",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "mappings",
    "revision",
    "schema_version",
    "source_id"
  ],
  "properties": {
    "schema_version": {
      "const": "1.0"
    },
    "source_id": {
      "const": "operator_mqtt_v1"
    },
    "revision": {
      "type": "integer",
      "minimum": 1,
      "maximum": 9007199254740991
    },
    "mappings": {
      "type": "array",
      "maxItems": 4096,
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": [
          "device_id",
          "endpoint_id",
          "mapping_id",
          "service_id"
        ],
        "properties": {
          "mapping_id": {
            "type": "string",
            "pattern": "^map_[0-9a-f]{32}$",
            "maxLength": 128
          },
          "endpoint_id": {
            "type": "string",
            "pattern": "^me_[0-9a-f]{32}$",
            "maxLength": 128
          },
          "device_id": {
            "type": "string",
            "pattern": "^dev_[0-9a-f]{16}$",
            "maxLength": 128
          },
          "service_id": {
            "anyOf": [
              {
                "type": "null"
              },
              {
                "type": "string",
                "pattern": "^(?:svc_(?:mqtt|dns|dhcp|ups|ssh|scheduler)_[0-9a-f]{8}|svc_mqtt_listener|svc_network_(?:53|67))$",
                "maxLength": 128
              }
            ]
          }
        }
      },
      "uniqueItems": true
    }
  }
}
```

## Closed private output schema (design only)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Private combined service relationship receipt 2.0",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "changes",
    "configured",
    "evaluated_at",
    "inventory",
    "local",
    "schema_version",
    "state",
    "valid_until"
  ],
  "properties": {
    "schema_version": {
      "const": "2.0"
    },
    "state": {
      "enum": [
        "VALID",
        "UNAVAILABLE"
      ]
    },
    "evaluated_at": {
      "type": "string",
      "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{1,6})?Z$",
      "maxLength": 32,
      "format": "date-time"
    },
    "valid_until": {
      "type": "string",
      "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{1,6})?Z$",
      "maxLength": 32,
      "format": "date-time"
    },
    "inventory": {
      "anyOf": [
        {
          "type": "null"
        },
        {
          "type": "object",
          "additionalProperties": false,
          "required": [
            "sha256",
            "updated"
          ],
          "properties": {
            "sha256": {
              "type": "string",
              "pattern": "^[0-9a-f]{64}$",
              "maxLength": 128
            },
            "updated": {
              "type": "string",
              "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{1,6})?Z$",
              "maxLength": 32,
              "format": "date-time"
            }
          }
        }
      ]
    },
    "local": {
      "anyOf": [
        {
          "type": "null"
        },
        {
          "$schema": "https://json-schema.org/draft/2020-12/schema",
          "title": "PE-5.1 private local service association envelope",
          "type": "object",
          "additionalProperties": false,
          "required": [
            "association_count",
            "evaluated_at",
            "inventory_updated",
            "max_snapshot_age_seconds",
            "rejection_count",
            "rejections",
            "schema_version",
            "service_associations"
          ],
          "properties": {
            "schema_version": {
              "const": "1.0"
            },
            "inventory_updated": {
              "type": "string",
              "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{1,6})?(?:Z|[+-]\\d{2}:\\d{2})$",
              "format": "date-time",
              "maxLength": 32
            },
            "evaluated_at": {
              "type": "string",
              "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{1,6})?(?:Z|[+-]\\d{2}:\\d{2})$",
              "format": "date-time",
              "maxLength": 32
            },
            "max_snapshot_age_seconds": {
              "type": "integer",
              "minimum": 0,
              "maximum": 9007199254740991
            },
            "association_count": {
              "type": "integer",
              "minimum": 0,
              "maximum": 4096
            },
            "service_associations": {
              "type": "array",
              "maxItems": 4096,
              "uniqueItems": true,
              "items": {
                "type": "object",
                "additionalProperties": false,
                "required": [
                  "association_basis",
                  "association_id",
                  "collection_provenance",
                  "confidence",
                  "service_id",
                  "service_type",
                  "source_type",
                  "stable_device_id"
                ],
                "properties": {
                  "association_id": {
                    "type": "string",
                    "pattern": "^lsa_[0-9a-f]{64}$"
                  },
                  "service_id": {
                    "type": "string",
                    "pattern": "^(?:svc_(?:mqtt|dns|dhcp|ups|ssh|scheduler)_[0-9a-f]{8}|svc_mqtt_listener|svc_network_(?:53|67))$"
                  },
                  "stable_device_id": {
                    "type": "string",
                    "pattern": "^dev_[0-9a-f]{16}$"
                  },
                  "service_type": {
                    "enum": [
                      "mqtt",
                      "dns",
                      "dhcp",
                      "ups",
                      "ssh",
                      "scheduler"
                    ]
                  },
                  "source_type": {
                    "enum": [
                      "systemd",
                      "ss"
                    ]
                  },
                  "association_basis": {
                    "const": "existing_service_ownership"
                  },
                  "confidence": {
                    "const": "high"
                  },
                  "collection_provenance": {
                    "type": "object",
                    "additionalProperties": false,
                    "required": [
                      "inventory_snapshot_sha256",
                      "inventory_updated"
                    ],
                    "properties": {
                      "inventory_updated": {
                        "type": "string",
                        "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{1,6})?(?:Z|[+-]\\d{2}:\\d{2})$",
                        "format": "date-time",
                        "maxLength": 32
                      },
                      "inventory_snapshot_sha256": {
                        "type": "string",
                        "pattern": "^[0-9a-f]{64}$"
                      }
                    }
                  }
                }
              }
            },
            "rejection_count": {
              "type": "integer",
              "minimum": 0,
              "maximum": 4096
            },
            "rejections": {
              "type": "array",
              "maxItems": 4096,
              "items": {
                "type": "object",
                "additionalProperties": false,
                "required": [
                  "collection_provenance",
                  "owner_reference",
                  "reason",
                  "service_id",
                  "source_type"
                ],
                "properties": {
                  "service_id": {
                    "type": [
                      "string",
                      "null"
                    ],
                    "pattern": "^(?:svc_(?:mqtt|dns|dhcp|ups|ssh|scheduler)_[0-9a-f]{8}|svc_mqtt_listener|svc_network_(?:53|67))$"
                  },
                  "reason": {
                    "enum": [
                      "MALFORMED_SERVICE",
                      "UNEXPECTED_SERVICE_FIELD",
                      "INVALID_SERVICE_ID",
                      "UNSUPPORTED_SOURCE",
                      "UNSUPPORTED_SERVICE_TYPE",
                      "SOURCE_ID_TYPE_MISMATCH",
                      "CONFLICTING_SERVICE_ID",
                      "MISSING_OWNER",
                      "WEAK_OWNER",
                      "AMBIGUOUS_OWNER",
                      "MALFORMED_DEVICE",
                      "MALFORMED_MAC",
                      "OWNER_MAC_COLLISION",
                      "OWNER_ID_MISMATCH"
                    ]
                  },
                  "owner_reference": {
                    "type": [
                      "string",
                      "null"
                    ],
                    "pattern": "^dev_[0-9a-f]{16}$"
                  },
                  "source_type": {
                    "enum": [
                      null,
                      "systemd",
                      "ss"
                    ]
                  },
                  "collection_provenance": {
                    "type": "object",
                    "additionalProperties": false,
                    "required": [
                      "inventory_snapshot_sha256",
                      "inventory_updated"
                    ],
                    "properties": {
                      "inventory_updated": {
                        "type": "string",
                        "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{1,6})?(?:Z|[+-]\\d{2}:\\d{2})$",
                        "format": "date-time",
                        "maxLength": 32
                      },
                      "inventory_snapshot_sha256": {
                        "type": "string",
                        "pattern": "^[0-9a-f]{64}$"
                      }
                    }
                  }
                }
              }
            }
          }
        }
      ]
    },
    "configured": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "associations",
        "candidate_count",
        "error_code",
        "rejections",
        "revision",
        "source_id",
        "source_sha256",
        "state"
      ],
      "properties": {
        "state": {
          "enum": [
            "VALID",
            "UNAVAILABLE"
          ]
        },
        "source_id": {
          "const": "operator_mqtt_v1"
        },
        "revision": {
          "anyOf": [
            {
              "type": "null"
            },
            {
              "type": "integer",
              "minimum": 1,
              "maximum": 9007199254740991
            }
          ]
        },
        "source_sha256": {
          "anyOf": [
            {
              "type": "null"
            },
            {
              "type": "string",
              "pattern": "^[0-9a-f]{64}$",
              "maxLength": 128
            }
          ]
        },
        "candidate_count": {
          "type": "integer",
          "minimum": 0,
          "maximum": 4096
        },
        "associations": {
          "type": "array",
          "maxItems": 4096,
          "items": {
            "type": "object",
            "additionalProperties": false,
            "required": [
              "device_id",
              "direction",
              "endpoint_id",
              "mapping_id",
              "relationship_id",
              "rule_id",
              "service_id",
              "source_id",
              "source_kind",
              "source_revision",
              "source_sha256"
            ],
            "properties": {
              "relationship_id": {
                "type": "string",
                "pattern": "^mqra_[0-9a-f]{64}$",
                "maxLength": 128
              },
              "mapping_id": {
                "type": "string",
                "pattern": "^map_[0-9a-f]{32}$",
                "maxLength": 128
              },
              "endpoint_id": {
                "type": "string",
                "pattern": "^me_[0-9a-f]{32}$",
                "maxLength": 128
              },
              "device_id": {
                "type": "string",
                "pattern": "^dev_[0-9a-f]{16}$",
                "maxLength": 128
              },
              "service_id": {
                "anyOf": [
                  {
                    "type": "null"
                  },
                  {
                    "type": "string",
                    "pattern": "^(?:svc_(?:mqtt|dns|dhcp|ups|ssh|scheduler)_[0-9a-f]{8}|svc_mqtt_listener|svc_network_(?:53|67))$",
                    "maxLength": 128
                  }
                ]
              },
              "direction": {
                "const": "endpoint_to_device"
              },
              "source_kind": {
                "const": "configured_mqtt"
              },
              "source_id": {
                "const": "operator_mqtt_v1"
              },
              "source_revision": {
                "type": "integer",
                "minimum": 1,
                "maximum": 9007199254740991
              },
              "source_sha256": {
                "type": "string",
                "pattern": "^[0-9a-f]{64}$",
                "maxLength": 128
              },
              "rule_id": {
                "const": "declared_endpoint_device_v1"
              }
            }
          },
          "uniqueItems": true
        },
        "rejections": {
          "type": "array",
          "maxItems": 4096,
          "items": {
            "type": "object",
            "additionalProperties": false,
            "required": [
              "code",
              "mapping_id"
            ],
            "properties": {
              "mapping_id": {
                "anyOf": [
                  {
                    "type": "null"
                  },
                  {
                    "type": "string",
                    "pattern": "^map_[0-9a-f]{32}$",
                    "maxLength": 128
                  }
                ]
              },
              "code": {
                "enum": [
                  "MISSING_DEVICE",
                  "WEAK_DEVICE",
                  "AMBIGUOUS_DEVICE",
                  "DEVICE_ID_MISMATCH",
                  "MAC_COLLISION",
                  "MISSING_SERVICE",
                  "AMBIGUOUS_SERVICE",
                  "SERVICE_OWNER_MISMATCH"
                ]
              }
            }
          },
          "uniqueItems": true
        },
        "error_code": {
          "enum": [
            null,
            "SOURCE_ABSENT",
            "SOURCE_UNREADABLE",
            "SOURCE_METADATA_INVALID",
            "SOURCE_SCHEMA_INVALID",
            "SOURCE_CHANGED",
            "SOURCE_REVISION_CONFLICT",
            "SOURCE_REVISION_ROLLBACK",
            "SOURCE_DUPLICATE",
            "SOURCE_CONFLICT",
            "INVENTORY_INVALID",
            "INVENTORY_STALE",
            "INVENTORY_FUTURE",
            "CLOCK_INVALID",
            "PRIOR_STATE_INVALID",
            "WRITE_FAILED",
            "OVERLAP_SKIPPED"
          ]
        }
      }
    },
    "changes": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "added",
        "added_count",
        "baseline",
        "removed",
        "removed_count",
        "truncated"
      ],
      "properties": {
        "baseline": {
          "type": "boolean"
        },
        "added": {
          "type": "array",
          "maxItems": 64,
          "items": {
            "type": "string",
            "pattern": "^mqra_[0-9a-f]{64}$",
            "maxLength": 128
          },
          "uniqueItems": true
        },
        "removed": {
          "type": "array",
          "maxItems": 64,
          "items": {
            "type": "string",
            "pattern": "^mqra_[0-9a-f]{64}$",
            "maxLength": 128
          },
          "uniqueItems": true
        },
        "added_count": {
          "type": "integer",
          "minimum": 0,
          "maximum": 9007199254740991
        },
        "removed_count": {
          "type": "integer",
          "minimum": 0,
          "maximum": 9007199254740991
        },
        "truncated": {
          "type": "boolean"
        }
      }
    }
  }
}
```

## Validation and later acceptance gates

PE-5.2 validates current identities, immutable history, closed declarative schemas,
privacy/shape/bounds mutants and current sequencing. No runtime composer, source installer,
scheduler, transaction or runtime validator is implemented/executed. PE-5.3 must test strong
identity/service owner checks, stable IDs/permutation determinism, revision rollback/conflict,
sorted differences, input races, clock/deadline bounds, native atomic/fsync/permissions/locks,
interrupted writes, restart/corruption recovery, no LKG promotion, expiry and safe errors.
These runtime tests are not claimed to pass merely because the design exists.

PE-5.4 source sync, PE-5.5 inactive deployment, PE-5.6 bounded validation, PE-5.7 activation,
PE-5.8 operational evidence and PE-5.9 closure remain separately authorized.
No historical PE-4 journal cleanup or extra PE-5.1 native execution is permitted.
PE-6, later Discovery/Active Discovery/surveillance/retention/PE-7 through PE-10 stay outside.

## Consistency review

CURRENT: descriptive association, reconciled identity, private/public separation,
unchanged MQTT and accepted PE-5.1 policy/rules preserved; next is separately authorized PE-5.3.
HISTORICAL_INTENTIONALLY_PRESERVED: roadmap/PE-5.1/PE-4 records and original UNKNOWNs/identities.
STALE_REQUIRES_UPDATE: current next-task/checkpoint documentary pointers now follow this successor.
UNRELATED_REFERENCE: later Discovery/health/classification/surveillance confer no PE-5 authority.
No unresolved current-authority contradiction identified.

## Atomic durability boundary correction

Classification: CURRENT. Narrow successor to the accepted design at 0c9c40d42c829c280341e73e475aac2ff4abf897.
The original record/schema and STOP_PE5_3_ATOMIC_FAILURE_CONTRACT_CONTRADICTION remain historical.
PE-5.3 exposed the post-replace boundary before implementation; its one synthetic
fault test passed and proved that replacement visibility does not preserve old bytes.
No production evidence or implementation was performed. The current persistence
contract is bound by governance/pe5/pe5-atomic-durability-contract-correction.json;
unchanged mapping input/output schemas retain their original authority.

- **scope**: Narrow correction of the post-os.replace parent-fsync failure boundary; PE-5.3 implementation remains NOT PERFORMED. No generic transaction framework. Failure and recovery gates apply to the affected primary domain. Source uncertainty blocks configured evidence/source installation; it does not invent a dependency of an independently valid local branch on a valid configured source. Every published output still requires its own confirmation, and source/input change-abort checks are unchanged.
- **domains**: [{"domain": "CONFIGURED_MAPPING_SOURCE", "metadata": "/home/jazofv1/hioc/config/enrichment/mqtt_mappings.durability.json", "primary": "/home/jazofv1/hioc/config/enrichment/mqtt_mappings.json"}, {"domain": "GENERATED_RELATIONSHIP_OUTPUT", "metadata": "/home/jazofv1/hioc/state/enrichment/service_associations/current.durability.json", "primary": "/home/jazofv1/hioc/state/enrichment/service_associations/current.json"}]
- **metadata**: One bounded closed-schema sidecar per domain, schema1.0, max8192 bytes, owner jazofv1, regular single-link non-symlink file0600 in existing approved0700 private directory. Contains domain, opaque per-attempt transaction_id, state, confirmed descriptor and candidate descriptor only. Descriptor={sha256,source_revision}; hash is canonical primary ASCII JSON+LF. source_revision mandatory for source, nullable for generated unavailable branch. No endpoint/device/service values, topics, credentials, payloads, timestamps or health fields.
- **pending_barrier**: Atomically write/fsync PENDING metadata and fsync its parent before touching the primary authoritative pathname. PENDING.confirmed is an exact copy of the last validated CONFIRMED descriptor (or null for approved initial absence); candidate is proposed validated digest/revision. If the barrier fails, no primary replacement is attempted. Any visible PENDING record blocks normal use even if the primary matches prior/candidate.
- **primary_sequence**: ["validate_inputs_and_confirmed_anchor", "durable_pending_barrier", "write_exclusive_primary_temp", "fsync_primary_temp", "replace_primary_once", "fsync_primary_parent", "publish_confirmed_metadata", "fsync_confirmation_metadata_parent"]
- **pre_replacement**: {"cleanup": "Only owned non-authoritative temp artifacts; pending metadata is retained as recovery evidence if the barrier was published. Metadata cleanup must never be described as primary rollback.", "logical_lkg": "prior confirmed descriptor unchanged", "new_current_accepted": false, "prior_path_unchanged": true, "prior_present_if_previously_present": true, "state": "PRE_REPLACEMENT_FAILURE", "temp_authoritative": false}
- **success**: {"new_current_may_be_consumed": "Only after all unchanged schema/identity/freshness/provenance gates; durability is not liveness or health.", "requires": "Primary bytes and directory-entry fsync succeeded AND matching CONFIRMED sidecar file/parent persistence succeeded; only then report publication success.", "state": "CONFIRMED_DURABLE_CURRENT"}
- **post_primary_parent_failure**: {"automatic_rollback": false, "confirmation_write_allowed": false, "error_code": "WRITE_FAILED", "fail_closed": true, "logical_lkg": "PENDING.confirmed retains last prior confirmed durable identity, even if old payload is no longer present.", "new_durable_commit_claimed": false, "primary_replace_succeeded": true, "prior_physical_presence_guaranteed": false, "replacement_may_be_visible": true, "second_primary_replace_as_rollback": false, "state": "INDETERMINATE_DURABILITY"}
- **confirmation_metadata_failure**: Distinct secondary phase: CONFIRMED metadata is constructed/published ONLY after primary file+parent fsync returned success. If its temp/file/replace/parent sync fails, report WRITE_FAILED and CONFIRMATION_METADATA_UNCONFIRMED, not complete transaction success. A surviving PENDING record blocks use. A surviving valid matching CONFIRMED witness proves the earlier primary fsync succeeded, not that its own directory sync succeeded; next writer validates binding and re-fsyncs primary/metadata and their directories before starting another transaction. No recursion: the witness records an already completed PRIMARY durability event, never predicts its own future durability.
- **restart_rules**: ["PENDING: block normal writes/consumption, retain logical prior descriptor, no guess based on visible primary or apparent crash survival.", "CONFIRMED plus exact primary binding: only confirms the primary durability event its trusted writer already completed; unchanged application validators still apply. Writer re-fsyncs bound primary/metadata before a new pending barrier; any error stops without a new primary replacement.", "Missing/invalid sidecar with existing primary, unknown domain, unsafe metadata or digest/revision mismatch: unconfirmed; stop for explicit recovery, no automatic adoption.", "Primary and sidecar both absent: no confirmed LKG exists; original explicit source initialization or generated first-run rules apply."]
- **explicit_recovery**: Operator-authorized local recovery under same lock, never MQTT/HA/production observation by Codex. Validate safe metadata, closed primary schema and recorded binding. If visible bytes match recorded candidate or prior confirmed descriptor, re-fsync that primary and its parent successfully, then write/fsync matching CONFIRMED sidecar. No primary os.replace or automatic rollback is used for recertification. Recertification proves persistence only; never refreshes application time or overrides current-input/source/identity checks. If no recorded binding matches, file is missing/invalid or current input cannot support acceptance, stop; a separately approved fresh source replacement or output recomputation is required, using a fresh PENDING barrier and normal producer validations. Replacement source revision must exceed all retained prior/candidate revisions when contents differ.
- **metadata_failure_safety**: Before-primary sidecar uncertainty cannot change primary bytes. A primary-parent failure cannot produce a new CONFIRMED witness because publication of that witness is gated after successful primary fsync. If a crash restores PENDING, block conservatively; if it restores valid CONFIRMED binding, its protocol meaning is explicit. No assumption that pending candidate or old payload survived.
- **authority_boundaries**: Logical persistence LKG descriptors are not application LKG associations. lkg_required remains FALSE; source/output schemas, public projection, identity/IP/observation/liveness/health, 2100/900/1200 time contracts, broker/HA/Discovery boundaries all unchanged.
- **stop_evidence**: STOP_PE5_3_ATOMIC_FAILURE_CONTRACT_CONTRADICTION is preserved: one synthetic temporary-file test showed replacement visible after injected post-replace directory-fsync failure. No production action occurred; this correction precedes implementation.

The synthetic tests model directory-sync outcomes and use actual temporary-file
replacement. They do not prove native PI3 crash durability, permissions or locking;
those remain separately authorized implementation/native validation obligations.

### Private durability metadata schema

Canonical UTF-8 ASCII JSON plus LF, maximum 8192 bytes. No primary schema change.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "anyOf": [
    {
      "additionalProperties": false,
      "properties": {
        "candidate": {
          "additionalProperties": false,
          "properties": {
            "sha256": {
              "pattern": "^[0-9a-f]{64}$",
              "type": "string"
            },
            "source_revision": {
              "maximum": 9007199254740991,
              "minimum": 1,
              "type": "integer"
            }
          },
          "required": [
            "sha256",
            "source_revision"
          ],
          "type": "object"
        },
        "confirmed": {
          "anyOf": [
            {
              "additionalProperties": false,
              "properties": {
                "sha256": {
                  "pattern": "^[0-9a-f]{64}$",
                  "type": "string"
                },
                "source_revision": {
                  "maximum": 9007199254740991,
                  "minimum": 1,
                  "type": "integer"
                }
              },
              "required": [
                "sha256",
                "source_revision"
              ],
              "type": "object"
            },
            {
              "type": "null"
            }
          ]
        },
        "domain": {
          "const": "CONFIGURED_MAPPING_SOURCE"
        },
        "schema_version": {
          "const": "1.0"
        },
        "state": {
          "const": "PENDING"
        },
        "transaction_id": {
          "pattern": "^dur_[0-9a-f]{32}$",
          "type": "string"
        }
      },
      "required": [
        "candidate",
        "confirmed",
        "domain",
        "schema_version",
        "state",
        "transaction_id"
      ],
      "type": "object"
    },
    {
      "additionalProperties": false,
      "properties": {
        "candidate": {
          "type": "null"
        },
        "confirmed": {
          "additionalProperties": false,
          "properties": {
            "sha256": {
              "pattern": "^[0-9a-f]{64}$",
              "type": "string"
            },
            "source_revision": {
              "maximum": 9007199254740991,
              "minimum": 1,
              "type": "integer"
            }
          },
          "required": [
            "sha256",
            "source_revision"
          ],
          "type": "object"
        },
        "domain": {
          "const": "CONFIGURED_MAPPING_SOURCE"
        },
        "schema_version": {
          "const": "1.0"
        },
        "state": {
          "const": "CONFIRMED"
        },
        "transaction_id": {
          "pattern": "^dur_[0-9a-f]{32}$",
          "type": "string"
        }
      },
      "required": [
        "candidate",
        "confirmed",
        "domain",
        "schema_version",
        "state",
        "transaction_id"
      ],
      "type": "object"
    },
    {
      "additionalProperties": false,
      "properties": {
        "candidate": {
          "additionalProperties": false,
          "properties": {
            "sha256": {
              "pattern": "^[0-9a-f]{64}$",
              "type": "string"
            },
            "source_revision": {
              "anyOf": [
                {
                  "maximum": 9007199254740991,
                  "minimum": 1,
                  "type": "integer"
                },
                {
                  "type": "null"
                }
              ]
            }
          },
          "required": [
            "sha256",
            "source_revision"
          ],
          "type": "object"
        },
        "confirmed": {
          "anyOf": [
            {
              "additionalProperties": false,
              "properties": {
                "sha256": {
                  "pattern": "^[0-9a-f]{64}$",
                  "type": "string"
                },
                "source_revision": {
                  "anyOf": [
                    {
                      "maximum": 9007199254740991,
                      "minimum": 1,
                      "type": "integer"
                    },
                    {
                      "type": "null"
                    }
                  ]
                }
              },
              "required": [
                "sha256",
                "source_revision"
              ],
              "type": "object"
            },
            {
              "type": "null"
            }
          ]
        },
        "domain": {
          "const": "GENERATED_RELATIONSHIP_OUTPUT"
        },
        "schema_version": {
          "const": "1.0"
        },
        "state": {
          "const": "PENDING"
        },
        "transaction_id": {
          "pattern": "^dur_[0-9a-f]{32}$",
          "type": "string"
        }
      },
      "required": [
        "candidate",
        "confirmed",
        "domain",
        "schema_version",
        "state",
        "transaction_id"
      ],
      "type": "object"
    },
    {
      "additionalProperties": false,
      "properties": {
        "candidate": {
          "type": "null"
        },
        "confirmed": {
          "additionalProperties": false,
          "properties": {
            "sha256": {
              "pattern": "^[0-9a-f]{64}$",
              "type": "string"
            },
            "source_revision": {
              "anyOf": [
                {
                  "maximum": 9007199254740991,
                  "minimum": 1,
                  "type": "integer"
                },
                {
                  "type": "null"
                }
              ]
            }
          },
          "required": [
            "sha256",
            "source_revision"
          ],
          "type": "object"
        },
        "domain": {
          "const": "GENERATED_RELATIONSHIP_OUTPUT"
        },
        "schema_version": {
          "const": "1.0"
        },
        "state": {
          "const": "CONFIRMED"
        },
        "transaction_id": {
          "pattern": "^dur_[0-9a-f]{32}$",
          "type": "string"
        }
      },
      "required": [
        "candidate",
        "confirmed",
        "domain",
        "schema_version",
        "state",
        "transaction_id"
      ],
      "type": "object"
    }
  ],
  "title": "Private primary durability witness, canonical bytes bounded to 8192"
}
```
