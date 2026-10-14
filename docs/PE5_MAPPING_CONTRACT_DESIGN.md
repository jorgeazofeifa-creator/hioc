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
- **revision**: Integer 1..9007199254740991; every authorized content change increments revision. Canonical SHA256 identifies complete content. Future installer compares current schema-valid source and prior valid configured receipt when available: equal revision with changed digest/lower revision rejected. Intentional rollback requires a higher revision. If no valid anchor exists, fail closed until explicit operator recovery supplies an approved initial revision; no historical anti-rollback proof is claimed.
- **schema_version**: 1.0
- **selection**: One fixed production-root-relative path; no config/environment fallback, known-infrastructure/integration auto-promotion, globbing or live discovery
- **source_id**: operator_mqtt_v1
- **time**: Configuration state, not observation. No observed_at/last_seen timestamp or file mtime authority. Active declarations remain until replaced/removed; no wall-clock TTL. Inventory validity is checked independently at each evaluation with accepted 2100-second policy.
- **update**: Offline validation -> same-directory exclusive temporary file -> mode 0600 -> flush/fsync -> atomic replace -> parent directory fsync under shared PE-5 lock. Source and output files remain distinct; no secret required.
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

- **atomic**: Future implementation uses source snapshot immutability check, single shared flock, regular exclusive same-directory temp file, 0600, fsync(file), os.replace, fsync(parent). Reject symlink/nonregular/hardlink paths and unexpected metadata; never truncate current in place. No multi-file atomicity is claimed; source SHA/revision binds each output.
- **backup_recovery**: Private source backed up only via separately authorized secret-free restricted operator workflow, no implicit new production backup job. Generated current is reproducible, not restored as authority. Source rollback requires higher revision; no PE-4 journals touched.
- **corruption**: Source invalid => unavailable branch; inventory invalid => whole output unavailable; output invalid => PE-6 rejects. Partial/interrupted writes cannot produce a consumable mixed envelope.
- **directory_mode**: 0700
- **file_mode**: 0600
- **history**: One current envelope only, no relationship archive or hidden last-valid store. Prior receipt is comparison/revision evidence only when its configured branch is valid; an unavailable replacement cannot be used as a revision anchor. Source installer uses current valid source as its other anchor. No automatic use of stale associations.
- **lkg**: No automatic fallback to stale associations. If source/input fails, write unavailable envelope if possible; if writing fails, old file remains physically but becomes unconsumable after validity deadline. Prior receipt is not relationship authority.
- **lkg_required**: false
- **output_bytes**: 16777216
- **output_path**: /home/jazofv1/hioc/state/enrichment/service_associations/current.json
- **owner**: jazofv1
- **readers**: ["Future PE-6 private reader", "Authorized operator bounded private validator"]
- **reason**: Durable operator configuration is necessary across restarts; a private current relationship receipt provides atomic PE-6 consumption, provenance/revision checks and bounded changes without changing public inventory.
- **required**: true
- **restart**: Reread source/inventory; never recover associations from output alone. Corrupt existing receipt => PRIOR_STATE_INVALID, explicit authorized recovery before resumption. Missing receipt is first-run initialization, not corruption. Valid but unavailable prior receipt permits recomputation without diff baseline; source revision still checked against current approved source at installation. If neither valid source nor receipt anchors recovery, operator approves initial revision explicitly; no silent rollback protection claim.
- **retention**: Current replaced atomically each evaluation; exclusive temp removed on handled failure. No unbounded journal/backup/history. Stale crash temp is never followed/used; future recovery validator identifies exact owned temp before separately authorized removal. Future retention project remains separate.
- **schema_version**: 2.0
- **writer**: One future PE-5.3 standalone private composer; never inventory-engine or PE-5.1 caller modifications
- **schema_storage**: Design input/output schemas are embedded in governance/pe5/pe5-mapping-contract-design.json and printed in docs/PE5_MAPPING_CONTRACT_DESIGN.md. PE-5.3 must materialize or deterministically embed these exact schemas in its validator; installed schema hashes bind during PE-5.5. No runtime schema is installed now.


### Execution

- **cadence_seconds**: 900
- **clock**: UTC evaluated_at and valid_until. Future timestamp, backward clock relative to prior valid receipt, or invalid clock => fail closed. valid_until=min(evaluated_at+1200 seconds, inventory.updated+2100 seconds). New schema distinguishes evaluation time from observations.
- **failure**: Source failures produce unavailable configured branch with empty association set and counts; invalid inventory/clock/receipt causes whole unavailable output. Nonzero return code and fixed safe status/error log without endpoint/topic/device labels or credentials. Write failure leaves prior file, freshness gate rejects stale output.
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
- **validity**: PE-6 validates closed schema, metadata, timestamps/deadline and same-current input/source identities before use. Any current source change invalidates prior configured evidence immediately; stale/missing/invalid inventory or receipt -> unavailable, not empty healthy state.
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

- **atomic_input**: Source and inventory fingerprints/stat stable before/after read and immediately before output replace. Change aborts with SOURCE_CHANGED or INVENTORY_INVALID. Later changes invalidate consumer use through same-current digest comparisons.
- **comparison**: All configured rows share validated source revision/digest. baseline=false => zero changes/counts; baseline=true => exact complete difference counts, sorted arrays capped64, accurate truncation flag. Unavailable branches never report fabricated removals.
- **deadlines**: VALID deadline strictly after evaluation and no later than evaluation+1200 or inventory.updated+2100. Whole UNAVAILABLE deadline==evaluation. Invalid clock produces no fabricated timestamp or replacement; fixed failure, old receipt expires.
- **deployment**: Exact installed bytes are PE-5.3 implementation outputs; entrypoint/installer paths and interfaces are already defined here. PE-5.5 installs disabled runtime plus schemas, preserving existing source and refusing unexpected target contents. No source auto-created. PE-5.6 requires approved real positive mapping plus bounded nonactive negative fixtures.
- **local**: Embedded PE-5.1 result must pass unchanged validator, policy2100, same inventory digest/time/evaluation. No local schema/rule/caller changes.
- **root_state**: VALID means current inventory/time prerequisites usable, not that all branches are valid. UNAVAILABLE means no branch consumable. local=null means unavailable, never zero confirmed local associations.
- **schema_evolution**: New kinds/fields/identifier grammar require separately governed schema/rule version. Output2.0 wraps unchanged local1.0; never silently substitutes it.
- **serialization**: Sorted associations by relationship_id; rejections by mapping_id/code. Canonical ASCII compact sorted-key JSON plus LF; strict UTF-8; duplicate JSON keys and NaN/infinities rejected; byte/array bounds applied before ingestion.
- **source_install**: Future installer and composer share lock. Installer compares current valid source and prior valid configured receipt where available; no hidden retained last-valid store. If neither anchor is available, explicit operator-approved initialization/recovery is required. Composer never writes source.
- **source_state**: Configured VALID requires revision/digest, null error_code, candidate_count==accepted+rejected, unique IDs/endpoint declarations. UNAVAILABLE requires empty accepted associations and fixed nonnull error; revision/digest null and candidate_count/rejections zero when source cannot be safely validated.


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
