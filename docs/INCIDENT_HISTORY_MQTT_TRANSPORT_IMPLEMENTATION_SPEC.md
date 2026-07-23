# Incident History MQTT Transport Implementation Specification

## 1. Purpose

This specification implements accepted [ADR-0014](../DECISIONS.md#adr-0014-use-core-mqtt-for-incident-publication) by replacing Incident Engine subprocess MQTT publication with the existing Core MQTT publisher while preserving documented storage and external contracts. It is a bounded correction for the proven process-argument failure. Repository implementation is complete; production validation has not occurred.

**Repository implementation status:** Implemented and repository-validated. Production deployment and validation remain pending; the defect is not complete until the production Evidence Report passes.

The architectural evidence and neutral candidate comparison remain in the [preparation memorandum](INCIDENT_HISTORY_MQTT_ARCHITECTURE_DECISION_PREPARATION.md). The [HIOC Master Plan](HIOC_MASTER_PLAN.md) authorizes this specification as the next implementation checkpoint.

## 2. Scope

### In scope

- Incident Engine MQTT publication path.
- Integration with the shared Core `MqttClient`.
- Removal of the Incident Engine's local subprocess publisher.
- Publication of the existing large retained history payload.
- Explicit publication error propagation and partial-publication reporting.
- Truthful Incident Engine, installer, release, and upgrade exit status.
- Focused Core and Incident Engine tests.
- Documentation synchronized with implementation and production validation.
- Supported deployment, validation, and rollback.

### Out of scope

- Changing `history.json` or Incident Review content.
- Normalizing, shrinking, or deduplicating reviews.
- Changing history-retention defaults or adding a byte budget.
- Changing MQTT topic names, retained semantics, or external JSON fields.
- Pagination, segmentation, or a new public protocol.
- Home Assistant entity or dashboard redesign.
- General MQTT or Core refactoring.
- Broker configuration changes unless later production validation proves one is required.
- Unrelated Incident Engine cleanup.
- Changes to the separate predictive/history engine or shell MQTT helpers.

## 3. Current implementation map

| File and function/section | Current responsibility | Planned change | Required compatibility |
|---|---|---|---|
| `pi4/bin/hioc-incident-engine-v2.py`: imports and `cfg()` | Loads toolkit and HIOC shell configuration; uses Core correlation, events, review, and state modules. | Import `MqttClient` from `hioc.mqtt`. Continue passing the existing `cfg()` result so MQTT host, port, user, and password retain their current precedence; preserve the legacy publisher's `localhost:1883` defaults when those values are absent. | Configuration values and non-publication behavior remain identical. |
| `pi4/bin/hioc-incident-engine-v2.py`: `mqtt_pub()` | Constructs and executes `mosquitto_pub -m <payload>` once per topic. | Delete this local function. Do not replace it with another subprocess or duplicate MQTT wrapper. | No consumer-visible contract is attached to this private helper. |
| `pi4/bin/hioc-incident-engine-v2.py`: `publish_all()` | Reads existing payload files in insertion order, skips missing files, publishes six file topics and then `status=online`. | Preflight all present file payloads, validate file-backed JSON without reserializing it, open one `MqttClient` connection, publish the same ordered topics with `retain=True`, then close it. | Preserve topic set, ordering, skipped-missing-file behavior, payload text, status text, and retained flag. |
| `pi4/bin/hioc-incident-engine-v2.py`: `main()` and entry point | Writes authoritative local incident state, then calls `publish_all()`; an uncaught Python exception currently yields nonzero status. | Return an explicit integer. On publication failure, emit one redacted diagnostic to stderr and return 1; on success return 0. Invoke with `raise SystemExit(main())`. | State generation remains before publication. Required publication failure must make installer/upgrade fail. |
| `pi4/lib/hioc/mqtt.py`: `_encode_remaining_length()` | Encodes MQTT Remaining Length using base-128 continuation bytes. | No production-code change expected. Add focused tests for three-byte encoding and large packets. If tests expose a blocking defect at the required size, stop rather than redesign. | Existing inventory and platform publishers must remain compatible. |
| `pi4/lib/hioc/mqtt.py`: `MqttClient` | MQTT 3.1.1, retained QoS 0 socket publisher with one connection per context-manager lifetime. | Reuse unchanged unless a blocking test failure proves a narrow correction necessary. | Existing API, authentication, retain default, serialization, and consumers remain unchanged. |
| `pi4/bin/hioc-inventory-engine.py` | Uses one Core client per inventory publication cycle. | Remain unchanged; its usage is the repository convention for one connection and multiple publishes. | Existing inventory behavior and tests must pass. |
| `pi4/bin/hioc-platform-status.py` | Uses Core client for one retained status publication. | Remain unchanged. | Existing status behavior and tests must pass. |
| `pi4/install_pi4.sh` | Installs cron and directly invokes the Incident Engine under `set -e`, making nonzero status fail installation/upgrade. | No planned code change. Validate truthful propagation after the engine returns an explicit status. | Existing installation, cron, and upgrade flow remain unchanged. |
| `release/upgrade.sh` | Backs up and deploys source, then runs `pi4/install_pi4.sh`. | No planned code change. Validate success after correction and failure when Incident Engine publication is deliberately made unavailable in controlled tests. | Existing backup and rollback contracts remain unchanged. |
| `pi4/validate_pi4.sh` | Validates engine executable, cron entry, and incident JSON validity. | No planned change unless implementation review finds a narrowly necessary validation assertion already within scope. | Existing validation continues to pass. |
| `tests/test_core.py` | Tests Core state, schemas, events, drivers, and capabilities; it has no packet-size MQTT tests. | Add isolated fake-socket tests for Core packet encoding, payload bytes, retain flag, errors, and cleanup. | No network access. |
| `tests/test_incident_mqtt.py` | Does not currently exist. | Add focused module-level tests for the Incident Engine publication contract using a temporary state tree and fake Core client. | No broker, subprocess, or production state. |
| `tests/test_incident_review.py` | Protects review construction and derived history content. | Remain unchanged and pass as regression coverage. | Review model is unchanged. |
| `tests/test_platform_status.py`, inventory tests, and `tests/test_release.py` | Protect existing Core consumer and release behavior. | Remain unchanged unless a focused compatibility assertion is required. | All existing tests pass. |
| `docs/MQTT.md`, `docs/DATA_MODEL.md`, and `docs/HOME_ASSISTANT.md` | Own topics, review schema, and operator presentation. | Their contracts remain unchanged; record transport implementation only where document ownership requires it. | No topic, payload, entity, or dashboard change. |

The Incident Engine is scheduled by cron every minute through `flock`; no systemd service definition for it exists in the repository. Installation also invokes it synchronously, which is how publication failure propagates into supported upgrade status.

## 4. Core MQTT capability assessment

### Confirmed implementation behavior

- **Protocol:** MQTT 3.1.1 (`MQTT` protocol name, level 4).
- **Publication:** QoS 0 with retained flag by default; fixed header `0x31` when retained and `0x30` otherwise.
- **Serialization:** dictionaries and lists use `json.dumps(..., sort_keys=True)`; other values use `str(payload)` and UTF-8 encoding.
- **String behavior:** Incident Engine file payloads can be passed as strings without JSON reserialization, preserving their exact UTF-8 payload bytes.
- **Connection:** `socket.create_connection()` with an eight-second timeout, then one MQTT CONNECT/CONNACK exchange. The context manager disconnects and closes the socket.
- **Reconnect:** none. A failed connection or publish is not retried.
- **Socket writes:** CONNECT, each PUBLISH packet, and DISCONNECT each use one `socket.sendall()` call. `sendall()` continues OS-level sends until all bytes are accepted by the socket layer or raises; it does not prove broker processing.
- **Exceptions:** missing host raises `MqttPublishError`; connection, timeout, encoding, and send errors propagate. DISCONNECT-send `OSError` is intentionally ignored while socket close is still attempted.
- **Broker acknowledgement:** CONNECT expects CONNACK. QoS 0 PUBLISH has no PUBACK, so successful `sendall()` is not broker-level acknowledgement. Production retained-message retrieval is required for end-to-end proof.

### Packet length and capacity

MQTT 3.1.1 Remaining Length supports at most four encoded bytes and a protocol maximum of 268,435,455 bytes. The current encoder has no explicit upper-bound check and will emit additional bytes for an out-of-protocol value; that latent upper-bound validation question is deferred because it does not affect this checkpoint's payload.

A payload around 193 KB or at least 200 KB, plus the short topic field, uses a valid three-byte Remaining Length. The current algorithm correctly represents that range. `publish()` contains no smaller payload-size check, and the payload is carried in socket bytes rather than a process argument. The two-byte `_field()` limit applies to the topic string, not the message body.

No existing large-payload unit tests were found. The required tests must prove the encoder and packet bytes at greater than 131,072 bytes, around 193 KB, and at least 200 KB.

**Assessment:** no repository-visible blocking defect prevents Candidate C from representing and sending the established payload size. Production broker and consumer capacity still require validation.

## 5. Target design

1. Import `MqttClient` from `hioc.mqtt`.
2. Keep `cfg()` as the source of MQTT connection settings.
3. Build the existing ordered publication plan: active, history, summary, timeline history, latest timeline event, status detail, then scalar status.
4. Before opening MQTT, read every present file using UTF-8 and validate each with `json.loads()`. Preserve missing-file skipping. Publish the original strings rather than reserialized objects.
5. Open exactly one connection per Incident Engine run with `MqttClient(config, client_id="hioc-incident-engine")`.
6. Reuse that connection for all publications in the cycle.
7. Call `publish(topic, payload, retain=True)` explicitly for every topic.
8. Preserve existing publication order. This keeps status last and minimizes consumer-visible change.
9. Stop on the first publication failure. Record the failed topic and already-published topic count without logging payloads, credentials, or secrets. Later topics are not attempted.
10. Allow the context manager to close the connection on success or failure.
11. Propagate failure to `main()`, print a concise redacted stderr diagnostic, and return 1. Return 0 only after the complete required cycle succeeds.
12. Do not roll back or delete local incident state after publication failure; local state was committed first and remains diagnostic authority.
13. Do not retry within the run. The cron schedule provides a later independent attempt; no new retry policy is introduced.
14. Remove the local `mqtt_pub()` function. Keep `subprocess` because MQTT reads still use `mosquitto_sub` and other command execution.

MQTT publication is not transactional. If a later topic fails, earlier retained topics may already have advanced. The failure diagnostic and nonzero status must state that the cycle was partial. Fail-fast is selected because it matches exception propagation, avoids publishing final `status=online` after a required failure, and avoids inventing aggregate/retry semantics.

## 6. Exact code-change plan

### Incident Engine

1. **Imports — `pi4/bin/hioc-incident-engine-v2.py`**
   - Add `from hioc.mqtt import MqttClient`.
   - Retain `subprocess` for reads; remove no unrelated imports.
   - Test module import with the repository library path.

2. **Delete local `mqtt_pub()`**
   - Remove only the function that starts `mosquitto_pub`.
   - Do not alter `mqtt_read()` or other engines and shell helpers.
   - Static test must show no `mosquitto_pub` string or local `mqtt_pub` definition remains in Incident Engine v2.

3. **Refactor `publish_all()`**
   - Signature becomes `publish_all(base, config)` and returns the ordered list of successfully published topics after a complete cycle; any failure raises before a success return.
   - Use an explicit ordered tuple/list rather than relying implicitly on mapping order.
   - Pre-read and JSON-validate all present file payloads before connecting.
   - Preserve original UTF-8 strings and missing-file behavior.
   - Append existing scalar status payload last.
   - Open one `MqttClient(config, client_id="hioc-incident-engine")` context.
   - Publish each topic with `retain=True`.
   - On error, raise a redacted `RuntimeError` identifying phase, failed topic when applicable, and count completed, chaining the original exception.

4. **Make `main()` status explicit**
   - Call `publish_all(base, c)` after all existing state writes.
   - Catch publication exceptions only at the outer publication boundary. Print exactly one diagnostic in the form `incident MQTT publication failed phase=<preflight|connect|publish|cleanup> topic=<topic-or-none> completed=<count>: <ExceptionType>: <message>`, with secrets and payloads excluded, and return 1.
   - Do not catch or convert unrelated engine failures differently in this checkpoint; unexpected exceptions continue to produce nonzero process status.
   - Return 0 after a complete publication cycle.
   - Change the entry point to `raise SystemExit(main())`.

### Core MQTT

No production-code change is currently required. `MqttClient` already supports the required retained string payload over one persistent cycle. Add tests to `tests/test_core.py` without changing existing consumers.

If tests reveal failure to encode or send the required ~200 KB payload, stop implementation and reopen ADR-0014 rather than broadening Core. Explicit MQTT protocol-maximum enforcement, reconnect, QoS changes, and resilience redesign remain deferred because they are not blockers at the established payload size.

### Legacy helper removal

Delete the Incident Engine v2 local publisher. Do not retain a thin subprocess wrapper. Do not remove:

- `mqtt_read()` or `mosquitto_sub` usage;
- `pi4/lib/hioc-common.sh` publication helpers;
- the shell incident engine's helper;
- the predictive/history engine's publisher;
- installer checks for `mosquitto_pub`, because other installed components still use it.

## 7. Payload compatibility requirements

Implementation must prove:

- identical MQTT topic names;
- retained flag remains true;
- the same active, history, summary, timeline, latest-event, status-detail, and scalar-status payloads;
- identical top-level JSON fields;
- unchanged embedded reviews, history ordering, summary fields, timeline structure, status content, and active-incident structure;
- missing file topics remain skipped;
- scalar status remains `online` and is last;
- no payload is changed merely to reduce size.

Repository consumers parse JSON and access named attributes; no evidence makes formatting whitespace or object-key order contractual. Compatibility is therefore semantic for JSON structure and values. Nevertheless, because file payloads are passed as strings, focused tests must also prove that the original UTF-8 file bytes become the MQTT payload bytes without reserialization. Exact overall MQTT packet bytes will differ from the subprocess implementation and are not a public contract.

## 8. Error and exit-status contract

| Failure | Required behavior |
|---|---|
| MQTT connection failure or broker unavailable | Core exception propagates to publication boundary; stderr identifies connection phase with no secret; engine exits 1; installer/upgrade fails; existing local state remains; no retry. |
| First-topic publish failure | No topic is counted successful; stop immediately; stderr identifies topic and zero completed; exit 1; local state remains. |
| Later-topic publish failure | Earlier retained publications remain; stop before later topics; report failed topic and completed count as partial publication; exit 1; do not publish final online status. |
| Serialization or JSON-validation failure | Validate all file payloads before connection; report file/topic without payload; publish nothing; exit 1; do not rewrite the malformed file in the publisher. |
| Local file read failure | Preflight fails before connection; publish nothing; report path without contents; exit 1. Missing files continue to be skipped as existing behavior. |
| Malformed local JSON | Fail preflight before connection and publication; exit 1. This does not authorize repair or migration. |
| Timeout | Propagate the socket timeout through the same redacted publication diagnostic; exit 1; no in-run retry. |
| Socket send failure | Propagate, report failed topic/completed count, close through context manager, exit 1. |
| DISCONNECT send failure after all publishes | Preserve Core behavior: `OSError` while sending DISCONNECT is best-effort and ignored; socket close still occurs. It does not retroactively mark sent QoS 0 packets acknowledged. Production retained retrieval remains the proof. |
| Socket close failure | If Core propagates it, engine exits 1 and reports cleanup failure. Do not redesign Core cleanup in this checkpoint. |
| Unexpected publication exception | Redacted type/message to stderr, exit 1, no payload or credential logging, no retry. |
| Unexpected non-publication engine exception | Preserve current uncaught nonzero behavior; broad engine error handling is out of scope. |

Publication never deletes or rolls back `active.json`, `history.json`, `summary.json`, timeline files, or status detail. A failed publication cycle must not claim process success. Cron receives the same nonzero status; synchronous installer invocation under `set -e` causes the supported upgrade to fail truthfully.

## 9. Test specification

### Unit tests — `tests/test_core.py`

Use fake sockets and patched `socket.create_connection`; never contact a broker.

- **New:** Remaining Length round-trip for values requiring one, two, three, and four valid bytes; expected bytes are asserted independently of the production encoder.
- **New:** retained fixed header is `0x31`; non-retained control remains `0x30`.
- **New:** exact topic field and payload bytes for a string.
- **New:** payload greater than 131,072 bytes uses a valid three-byte Remaining Length.
- **New:** representative 193,053-byte payload is completely present in the sent packet.
- **New:** payload of at least 204,800 bytes is completely present and produces no internal-limit error.
- **New:** dict/list serialization retains existing sorted-key behavior.
- **New:** missing host, connection rejection, socket timeout, and publish `sendall()` failure propagate deterministically.
- **New:** context cleanup closes and clears the socket after success and publication failure; DISCONNECT-send `OSError` remains best-effort.

Expected result: exact packet construction and exception behavior pass without network access. Tests must not treat QoS 0 send completion as broker acknowledgement.

### Incident Engine tests — new `tests/test_incident_mqtt.py`

Load the script with `importlib`, a temporary `HIOC_HOME`, controlled environment, and fake `MqttClient`. Use real temporary JSON payload files and capture calls.

- `publish_all()` emits all seven existing topics in the current order.
- Every call explicitly retains.
- Existing file payload strings, including whitespace and embedded reviews, reach the fake client unchanged.
- Active, history, summary, timeline, latest event, status detail, and scalar status remain structurally compatible.
- History ordering and embedded review objects remain unchanged.
- A payload larger than the demonstrated Linux single-argument case passes through the fake Core client without subprocess invocation.
- Missing optional/presently skipped files remain skipped; status still publishes last when all required present publications succeed.
- Malformed JSON or read failure stops before client connection and produces zero publishes.
- Connection failure produces nonzero `main()` status with state files preserved.
- First and later publish failures stop immediately, report completed count, return nonzero, and leave local files byte-for-byte unchanged after the publication attempt.
- Later failure proves later topics and final online status are not published.
- Context exit occurs on success and failure.
- Static source assertion proves no Incident Engine v2 `mosquitto_pub` invocation and no local `mqtt_pub()` remain; `mosquitto_sub` remains allowed.

Expected result: transport changes while topic, payload, retention, ordering, and state invariants remain unchanged.

### Regression tests

- Existing `tests.test_incident_review`, `tests.test_correlation`, and any incident-history coverage pass unchanged.
- Existing inventory suite passes, including Core MQTT consumer behavior.
- Existing `tests.test_platform_status` passes.
- Existing `tests.test_release` passes and continues proving installer/upgrade invocation.
- Full UTF-8 repository suite passes.
- Python compile validation covers `pi4/lib/hioc` and `pi4/bin`.

### Static checks

- `git diff --check` passes.
- No unused import or dead publisher function remains.
- No Incident Engine v2 `mosquitto_pub -m` path remains.
- Topic literals compare exactly with the pre-change list.
- Documentation local-link and UTF-8 validation pass.

## 10. Deployment specification

This sequence is for the future implementation checkpoint and is not executed now:

1. Implement in the authorized repository.
2. Run focused, regression, full-suite, compile, static, and documentation validation.
3. Commit code, tests, and documentation together and push `main`.
4. On `PI3 NUT&PIHOLE`, update `/home/jazofv1/hioc-release-source` through the supported Git workflow.
5. Confirm clean source and exact approved commit.
6. Create and verify the supported pre-upgrade backup.
7. Run the supported release/upgrade path.
8. Confirm successful upgrade exit status and source-to-runtime file identity.
9. Confirm Incident Engine cron/process status and one-run behavior.
10. Confirm retained incident-history publication succeeds and is valid JSON.
11. Confirm all other incident topics remain valid and retained.
12. Confirm Home Assistant incident entities and Dashboard v2 history presentation remain functional.
13. Confirm no history record or embedded review was lost.
14. Confirm one connection per engine run, no repeated loop, and no parallel legacy incident publisher.
15. Produce the established Evidence Report.
16. Update Master Plan implementation status and decision evidence after validation.
17. Commit and push validation documentation and verify clean repositories.

Future PI3 instructions must identify `PI3 NUT&PIHOLE`, be complete and self-contained, avoid assumed working directories, provide one action at a time, and wait for operator output before continuing.

## 11. Production validation specification

Collect and preserve:

- approved source commit and clean `/home/jazofv1/hioc-release-source` status;
- release/upgrade command and exit status;
- output and exit status from the deployed read-only
  `pi4/bin/hioc-validate-mqtt.py` command;
- Incident Engine direct/scheduled exit status;
- cron and relevant process status; no systemd service is expected by current source;
- relevant redacted logs and stderr;
- absence of `E2BIG`;
- deployed source inspection proving Incident Engine has no `mosquitto_pub -m` publication path;
- retained history topic byte size, valid JSON, record count, ordering, and embedded-review presence;
- schema comparison for history, summary, active, timeline, status detail, and scalar status;
- retained flags and unchanged topic names;
- Home Assistant incident entity availability;
- Dashboard v2 incident-history visibility;
- source-to-runtime hashes for changed runtime files;
- authoritative Windows repository and PI3 source checkout cleanliness;
- before/after history hashes and semantic comparison proving no data loss;
- proof that other incident topics have no regression;
- observed connection/publication behavior without a repeated loop.

The repository-owned validator supplies bounded retained reads, configured
broker and authentication handling, payload byte counts, JSON checks, history
record counts, and embedded-review detection without publishing or modifying
retained state. It supports this Evidence Report but does not replace Home
Assistant, dashboard, source-to-runtime, data-loss, or connection-lifecycle
checks.

Evidence Report format:

- **Deployment result**
- **Intended behavior**
- **Invariant checks**
- **Warnings and deferred risks**
- **Final PASS or FAIL**

Any missing required evidence, data loss, contract change, failed publication, false success status, or consumer regression yields FAIL and stops further roadmap work.

## 12. Rollback specification

Use the supported prior-release restoration or a deliberate Git revert of the implementation commit followed by the supported release process. Before rollback:

1. stop overlapping scheduled execution through the approved operational procedure;
2. preserve and hash current incident state and any incidents created since deployment;
3. identify the verified pre-upgrade backup and prior source commit;
4. ensure rollback restoration excludes persistent state from destructive replacement.

Restore prior runtime code, retain current `state/incidents` files, restart or re-enable the existing cron path, and validate file identity, engine status, topics, local history count, and new-incident preservation. If the prior code cannot safely process records created after deployment, stop rather than discard them.

Rollback is mandatory for history loss, schema or topic regression, broken Home Assistant visibility, repeated connection loops, uncontrolled resource use, or an engine/release status that falsely reports success. Rollback may also be required for broker incompatibility that cannot be resolved within the accepted decision.

Rollback to the previous subprocess publisher restores the known `E2BIG` limitation for sufficiently large history payloads. It is a safety restoration, not a permanent correction, and publication may remain unavailable while authoritative local history is preserved.

## 13. Documentation update plan

| Document | Required change and timing |
|---|---|
| `docs/HIOC_MASTER_PLAN.md` | Updated now to authorize implementation; update after implementation and again after production Evidence Report. |
| `DECISIONS.md` | ADR-0014 accepted now; append validation consequences only if decision scope changes or production evidence materially qualifies it. |
| `docs/INCIDENT_HISTORY_MQTT_ARCHITECTURE_DECISION_PREPARATION.md` | Add decision outcome now; preserve its neutral investigation as historical rationale. |
| This specification | Created now; update only for an approved specification correction or to record final validation linkage. |
| `docs/ARCHITECTURE.md` | After implementation, record that Incident Engine uses Core MQTT; avoid duplicating this specification. |
| `docs/CORE.md` | After implementation, list Incident Engine as a Core MQTT consumer and document any narrow capability clarification actually implemented. |
| `docs/MQTT.md` | After implementation, record transport migration and unchanged contract; after production validation, link the result if appropriate. |
| `docs/DATA_MODEL.md` | No change expected because storage and review schema are preserved. Change only if tests expose a real undocumented inconsistency. |
| `docs/HOME_ASSISTANT.md` | No change expected because entities and attributes are preserved. Record only a discovered compatibility qualification. |
| `docs/RELEASE.md` | After implementation, document required publication failure propagation if existing release text is insufficient; do not duplicate operational commands. |
| `docs/RECOVERY_BASELINE.md` | No change; it is immutable historical evidence. New recovery evidence belongs in a new record. |
| Test documentation/reviews | Update only where the repository convention records the new focused coverage; do not rewrite archived reviews. |

## 14. Deferred work

- Explicit MQTT payload-size policy and byte-budget invariant.
- Broker maximum-message configuration review beyond Candidate C validation.
- External-consumer maximum-payload review.
- History count versus byte-budget policy.
- Review immutability versus regeneration.
- Summary review duplication.
- Stable incident identity versus historical occurrence semantics.
- Review normalization or smaller derived external projections.
- Chunking or pagination.
- Migration of the predictive/history engine and other legacy MQTT publishers.
- Explicit enforcement of MQTT's four-byte Remaining Length maximum.
- Broader Core MQTT reconnect, acknowledgement, resilience, TLS, and observability improvements not required for this correction.

These items must not be implemented unless a specific one proves blocking during Candidate C implementation or validation; a blocker requires stopping and updating the decision.

## 15. Definition of ready for implementation

Implementation is ready because:

- ADR-0014 is accepted and explicitly selects Candidate C;
- repository inspection found no blocking Core MQTT defect at approximately 200 KB;
- exact files, functions, publication order, connection lifecycle, and failure behavior are specified;
- storage, topic, retained, and payload compatibility contracts are documented;
- focused and regression tests are specified;
- deployment and production validation evidence are specified;
- rollback and state-preservation behavior are specified;
- documentation ownership and deferred work are recorded;
- the Master Plan authorizes the bounded implementation checkpoint; and
- this decision checkpoint must be clean, committed, and pushed before code work begins.

Repository implementation has occurred and passed the specified automated validation. Production remains unresolved until the approved code is deployed and the Evidence Report passes.
