# Incident History Storage and MQTT Publication Architecture Decision Preparation

## 1. Purpose

This memorandum prepares, but does not approve, an architecture decision concerning incident-history storage, embedded Incident Review data, retained MQTT exposure, MQTT transport implementation, compatibility boundaries, retention, and payload-size expectations.

It is governed by the [HIOC Master Plan](HIOC_MASTER_PLAN.md), [architecture](ARCHITECTURE.md), [data model](DATA_MODEL.md), [MQTT contract](MQTT.md), [Core runtime](CORE.md), and [decision log](../DECISIONS.md). No implementation candidate has been selected or authorized.

## 2. Current operational problem

The supported production upgrade reached `hioc-incident-engine-v2.py` and exited with status 1 after MQTT publication raised `OSError: [Errno 7] Argument list too long: 'mosquitto_pub'`. Established production evidence shows that `state/incidents/history.json` was approximately 193,053 bytes with 24 records, that most records were approximately 6–7 KB, that embedded `review` data contributed approximately 5.2 KB to most large records, and that a read-only argument-size test reproduced `E2BIG` for that file while the other incident payload files passed. The operating system reported `ARG_MAX` as 2,097,152 bytes; that aggregate value does not invalidate the demonstrated per-argument failure. The intended Identity Reconciliation Hardening runtime files had already copied successfully and matched authoritative source, so the upgrade failure is specifically recorded at incident publication rather than as a failed source copy.

The immediate failure occurs because the complete serialized history document is supplied as one process argument through `mosquitto_pub -m`. This locates the operational failure but does not decide whether the durable architecture should change transport, storage representation, retention, the external payload contract, or a documented combination of those layers.

## 3. Established architectural facts

### Persistent storage

The incident engine writes authoritative local incident state before MQTT publication. Completed incidents are retained in `state/incidents/history.json`, and timeline history is retained separately. Both lists are bounded by `HIOC_HISTORY_LIMIT`. Commit `60285126075c7be4e5cd90b760c6afe6cac36f8a` (`Add Pi4 configuration example`) introduced the 50-record configuration default, and commit `e75e706d8668bd8959343cfa5bebe159429b2535` (`Add intelligent incident correlation engine`) introduced the Python engine's fallback of 100. Repository history contains no sizing rationale for either value.

### Internal incident data model

Commit `3e6a6f4287a1b20567396440ccfed2cd945174dc` (`feat: implement Incident Review history`) introduced the review model. Every processed completed-history record receives a complete derived `review`. Reviews contain operator-facing root cause, impact, evidence, timeline, recovery, confidence, and recommended action. The enriched history is persisted. Incident summary state also contains history statistics, compact recent incidents, full recent reviews, and the latest full review.

The repository establishes that reviews are derived and persisted. It does not establish whether they must be immutable snapshots or may be regenerated projections.

### External MQTT payload schema

The persisted history document is published without a separate external projection, making embedded reviews externally observable. The incident summary payload exposes `history_stats`, `recent_incidents`, `recent_incident_reviews`, and `latest_incident_review`. These are documented as additive fields used by Dashboard v2.

### External MQTT topic contract

Active incidents, history, summary, timeline history, latest timeline event, and status use established retained MQTT topics. ADR-0002 makes retained MQTT the Home Assistant contract. ADR-0010 preserves existing incident topics, sensors, and established incident fields while allowing additive fields.

### Transport implementation

The Python incident engine reads each complete JSON file and passes its serialized contents to a local `mqtt_pub()` helper. That helper starts `mosquitto_pub` with the payload as the single argument following `-m`. Whole-document `mosquitto_pub -m` publication originated in commit `d861d2206dbd791b31adab56be5debf0fb960372` (`Add Pi4 common library`) and was retained by the first incident engine and Python correlation engine before Incident Review existed. The process invocation is an internal implementation detail; the retained topics and externally visible payload are separate contracts.

### Shared Core runtime architecture

Commit `01f321b55a27849d6ae2a12d50269a9203fb1f9e` (`feat: introduce HIOC Core runtime`) added a persistent MQTT 3.1.1 socket publisher now used by Living Inventory and platform status. Commit `f57d200be0145305338d5a41bd34a505a1a1a7d0` (`Implement Correlation Engine v2`) adopted Core correlation, event, and state services but retained the local MQTT helper. The architecture review archived by commit `b04c6a507b3b55527d35652d63683419a73c8be8` identifies this split, repeated subprocesses, and growing retained JSON as technical debt. No repository evidence says that the Core client was rejected for incidents or that preserving `mosquitto_pub -m` was an architectural decision.

## 4. Confirmed invariants

| Concern | Classification | Repository basis |
|---|---|---|
| Authoritative local state is written before MQTT publication | Confirmed invariant | ADR-0003 and current engine ordering preserve diagnosis when MQTT or Home Assistant is unavailable. |
| Established incident MQTT topic compatibility | Confirmed invariant | ADR-0002 and ADR-0010. A breaking migration requires explicit approval. |
| Retained publication semantics | Confirmed invariant | MQTT documentation and current Home Assistant contract. |
| Established incident fields remain compatible | Confirmed invariant | ADR-0010. Additions are permitted; incompatible changes require migration approval. |
| Operator-facing Incident Review semantics | Confirmed invariant | Data Model, MQTT, Home Assistant, and Master Plan documentation. |
| Bounded incident and timeline history | Confirmed invariant | Both implementations apply `HIOC_HISTORY_LIMIT`; the correct numeric or byte bound is unresolved. |
| Home Assistant incident visibility | Confirmed invariant | ADR-0010 and Home Assistant documentation. |
| Diagnostic availability during MQTT or Home Assistant failure | Confirmed invariant | ADR-0003 requires local persistence before publication. |
| Deterministic and reproducible publication | Likely expectation | Deterministic JSON state and retained replacement behavior support it, but no complete publication-determinism contract is recorded. |
| Publication failure must be observable rather than silently swallowed | Likely expectation | Current Python publication propagates failure and repository review calls for engine failure observability; a formal incident publication policy is absent. |
| Production deployment returns a truthful exit status | Confirmed invariant | Supported release validation and governance require truthful PASS/FAIL and the observed upgrade correctly returned failure. |
| Historical data is not silently discarded during migration | Confirmed invariant | Repository recovery, rollback, evidence-preservation, and governance rules prohibit unapproved loss. |
| Existing history payload shape is immutable | Unresolved | Additive compatibility is documented, but the exact compatibility boundary for embedded historical reviews is not. |
| A particular maximum MQTT payload size is supported | Unresolved | No byte-size contract or validated limit is documented. |

## 5. Genuine unresolved decisions

### Implementation-blocking

1. Must local historical records remain self-contained, or may review data be referenced or reconstructed?
2. Are reviews immutable historical snapshots or regenerated projections whose content may evolve?
3. Must the full embedded review schema remain on the existing history topic?
4. Which repository and external consumers depend on the complete history payload and its exact shape?
5. Does compatibility protect topic names, established fields, full payload shape, or all three?
6. What maximum payload size must incident publication support, and does that become an explicit MQTT invariant?
7. Should incident publication complete the partial migration to Core MQTT, and is the current Core client sufficient for the selected payload contract?
8. How must incident-engine publication failure affect engine, installer, service, and supported-upgrade exit status?
9. If storage representation changes, how are existing history files migrated without loss and rolled back safely?
10. What production validation proves retained publication, consumer compatibility, failure behavior, and recovery?

### Safely deferrable if the selected correction does not alter them

1. Should record-count retention and a future byte budget be separate controls?
2. Is duplication between `recent_incident_reviews` and `latest_incident_review` intentional long-term architecture?
3. Does the relationship between stable incident identity and historical occurrence identity require clearer documentation?
4. Should full history eventually use segmentation, pagination, or another public protocol after the immediate bounded correction?

Deferral is valid only when recorded in the Master Plan or decision record and when it does not leave the selected implementation contract ambiguous.

## 6. Viable architecture decision candidates

No candidate is selected here.

### Candidate A — Preserve storage and external payload contracts; replace only publication transport

- **Preserves:** `history.json`, embedded reviews, retained topics, payload fields, and current retention behavior.
- **Changes:** internal transport implementation.
- **Advantages:** smallest observable compatibility surface; existing consumers continue receiving the same document.
- **Disadvantages:** retained payload growth and review duplication remain; broker and consumer limits still require evidence.
- **Compatibility impact:** intended to be none, subject to byte-equivalent payload and retained-message validation.
- **Migration requirements:** no state migration; deployment and rollback of the publisher still require validation.
- **Operational risks:** timeouts, connection failure, partial topic publication, and large-message behavior may differ.
- **Testing:** payload equivalence, retained flags, topic set, authentication, failures, exit status, and large-payload boundaries.
- **Documentation:** transport and failure semantics; no Data Model change if payloads are unchanged.
- **Coverage:** addresses the immediate argument failure; broader payload scalability remains.

### Candidate B — Normalize internal review storage while reconstructing the existing external payload

- **Preserves:** external topics and reconstructed payload shape.
- **Changes:** local storage and review ownership.
- **Advantages:** may reduce local duplication and separate evidence from derived presentation.
- **Disadvantages:** introduces a reference, join, or regeneration contract and does not reduce the external message by itself.
- **Compatibility impact:** intended to be external-compatible but materially changes internal recovery behavior.
- **Migration requirements:** lossless conversion of existing history, versioning, rollback, and mixed-version handling.
- **Operational risks:** missing references, inconsistent reconstruction, changed historical wording, and recovery complexity.
- **Testing:** migration round trips, reconstruction equivalence, immutability/regeneration policy, corruption, and rollback.
- **Documentation:** Data Model, recovery, migration, and review-authority contracts.
- **Coverage:** may address storage scalability; does not alone resolve the current transport limit.

### Candidate C — Preserve storage and payloads; migrate incident publication to Core MQTT

Candidate C is the repository-specific implementation of Candidate A.

- **Preserves:** storage, embedded reviews, retained topics, fields, and payload shape.
- **Changes:** incident publication uses shared Core infrastructure instead of its local subprocess helper.
- **Advantages:** aligns with documented Core direction and removes duplicated MQTT implementation and process-argument transport.
- **Disadvantages:** Core large-message, reconnect, timeout, and failure behavior require validation; message growth remains.
- **Compatibility impact:** intended to be none.
- **Migration requirements:** no history migration; runtime dependency and rollback validation are required.
- **Operational risks:** packet construction limits, socket interruption, authentication differences, and partial multi-topic publication.
- **Testing:** Core packet boundaries, exact topics/payloads/retain flags, failures, exit status, repeated runs, and rollback.
- **Documentation:** Core usage and incident publication failure contract.
- **Coverage:** addresses the immediate failure and existing publisher duplication, but not broader retained-message growth.

### Candidate D — Use retention-count reduction as the primary bound while preserving the publisher

- **Preserves:** storage shape, topic contract, and current publisher.
- **Changes:** retained history depth through configuration or default policy.
- **Advantages:** uses an existing control and requires no new transport.
- **Disadvantages:** record count is not a byte guarantee; review size varies; historical visibility decreases.
- **Compatibility impact:** payload shape remains, but observable history depth changes.
- **Migration requirements:** explicit preservation or archival decision for records beyond the new bound.
- **Operational risks:** recurrence of `E2BIG`, silent operator-history loss if poorly migrated, and configuration drift.
- **Testing:** boundary records of varied size, retention behavior, history preservation, and upgrade behavior.
- **Documentation:** rationale for the bound, retention semantics, and data-preservation policy.
- **Coverage:** may relieve the immediate case but does not establish a robust payload-size invariant.

### Candidate E — Keep full local history but publish a smaller derived history representation

- **Preserves:** full local history and operator evidence.
- **Changes:** external history payload unless introduced through an additive compatibility path.
- **Advantages:** separates durable diagnosis from transport presentation and can establish a bounded public payload.
- **Disadvantages:** existing consumers may rely on embedded reviews; access to full review content needs an explicit contract.
- **Compatibility impact:** potentially breaking unless existing fields and access paths are preserved through an approved migration.
- **Migration requirements:** consumer transition, Home Assistant mapping changes, and compatibility period if required.
- **Operational risks:** reduced diagnostic visibility, divergence between local and external views, and stale derived projections.
- **Testing:** consumer compatibility, projection correctness, bounds, retained behavior, and local-state availability.
- **Documentation:** MQTT schema, Home Assistant contract, Data Model projection ownership, and migration notice.
- **Coverage:** addresses immediate and broader external payload growth while leaving local duplication unchanged.

### Candidate F — Segment or paginate external incident history

- **Preserves:** potentially the full logical history and embedded reviews.
- **Changes:** public topic/message protocol and consumer assembly behavior.
- **Advantages:** creates an explicit message-size boundary without removing history content.
- **Disadvantages:** no existing HIOC chunk/reassembly contract; retained ordering, completeness, replacement, and cleanup become complex.
- **Compatibility impact:** substantial unless added alongside the existing topic during migration.
- **Migration requirements:** new topics or fields, consumer migration, retained-fragment cleanup, and rollback rules.
- **Operational risks:** incomplete page sets, stale segments, ordering errors, and more complex recovery.
- **Testing:** segmentation boundaries, atomic visibility, reassembly, missing pages, retained cleanup, compatibility, and rollback.
- **Documentation:** new MQTT protocol, schema, consumer behavior, and operational recovery.
- **Coverage:** addresses immediate and broader message scaling but creates the largest public-contract change.

## 7. Required evidence before selecting a candidate

| Evidence | Why necessary | Repository inspection | Production inspection | Blocks decision |
|---|---|---|---|---|
| All consumers of incident history and review fields | Defines the compatibility boundary. | Can identify repository-owned consumers and tests. | Needed only for external consumers not represented in source. | Yes. |
| Home Assistant entities and dashboard mappings | Shows which fields and topics are operator-visible. | Expected to answer repository-owned mappings. | Only if deployed configuration differs from authoritative source. | Yes. |
| Core MQTT packet-size and failure behavior | Establishes whether Candidate C satisfies the selected payload and failure contracts. | Code and focused tests can establish implementation behavior. | Broker interaction is required later for operational validation, not initial code-path understanding. | Yes for Candidate C. |
| Broker message-size configuration | Distinguishes process-argument capacity from broker capacity. | Usually not authoritative in this repository. | Required if preserving large full-history publication. | Candidate-dependent. |
| Retained-message behavior | Confirms replacement, reconnect, and consumer visibility semantics. | Expected semantics are documented; implementation tests can cover encoding. | Required before production approval of a changed transport. | Candidate-dependent. |
| Release, installer, and service failure semantics | Defines truthful failure propagation. | Scripts and tests can answer intended flow. | Production validation is required after implementation. | Yes. |
| Compatibility test expectations | Prevents accidental topic, field, or shape changes. | Existing tests plus a bounded gap assessment can answer. | No, unless an external consumer is discovered. | Yes. |
| Historical file migration requirements | Determines whether existing history needs transformation. | Repository schema and candidate choice provide the initial answer. | A production-shaped copy is required before approving a storage migration. | Yes for Candidates B or D; otherwise likely no. |

No broader investigation is justified unless one of these bounded checks exposes a specific blocking gap. This memorandum intentionally prescribes no production commands.

## 8. Implementation constraints

Any approved implementation must provide:

- no silent history loss;
- no accidental MQTT topic or payload-contract break;
- no assumption that retained payloads may grow without a documented bound;
- no process-argument publication of arbitrarily sized documents;
- no duplicate MQTT implementation if shared Core infrastructure is selected;
- truthful errors, status, and exit behavior;
- atomic authoritative local-state behavior before publication;
- deterministic tests and reproducible payloads;
- backward compatibility or an explicitly approved and documented migration;
- production validation against the selected payload and failure contracts;
- synchronized Master Plan, ADR, architecture, data-model, MQTT, and operator documentation where affected;
- Git-governed implementation and evidence;
- safe restoration or rollback without historical-data loss.

## 9. Definition of ready for implementation

An implementation specification may begin only after:

1. one architecture candidate is selected;
2. the compatibility boundary for topics, fields, and payload shape is documented;
3. repository and known external consumer impact is understood;
4. the supported payload-size contract is documented;
5. transport and publication failure semantics are documented;
6. historical migration and rollback behavior are documented, including an explicit no-migration conclusion when applicable;
7. the validation strategy is reviewed and approved;
8. the Master Plan identifies the bounded implementation checkpoint; and
9. the final decision is recorded in `DECISIONS.md` or a dedicated accepted ADR.

Until all conditions are satisfied, implementation remains unauthorized.

## 10. Relationship to roadmap and dashboard progress

This is a bounded architectural-defect checkpoint required to restore reliable deployment and incident publication. It must not become a general MQTT redesign or absorb unrelated incident-history redesign. Deferred improvements must be recorded separately rather than implemented opportunistically.

The checkpoint remains separate from incident-history schema-validator hardening, stale-client retention and archival, repository and deployment hygiene, new inventory enrichment, unrelated dashboard redesign, and broader MQTT protocol redesign. After the selected correction is implemented and validated, work returns to the authoritative Phase 7A roadmap. Operator-facing and dashboard progress resumes as soon as the current correctness and deployment blockers are resolved.
