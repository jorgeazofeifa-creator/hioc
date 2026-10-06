# PE-4.0B.2b registry/schema discovery preparation

## Corrected PE-4.0B.2b execution closure - 2026-10-06

**Current PE-4.0B.2b: PASS/CLOSED; PE-4.0C: NOT STARTED.**
This repository closure records operator-supplied completed production execution
and independent read-only review; Codex did not remotely inspect production.
Canonical authority: [execution closure](../governance/pe4/pe4-0b2b-execution-closure.json).
Original preparation completed, compatibility correction completed, corrected
preparation PASS/CLOSED, one separately authorized corrected live execution PASS,
and independent evidence review PASS. The initial synthetic probe failed because
its harness replaced shared `socket.socket`, preventing asyncio's local socketpair;
this was not a HIOC client or production failure. The corrected credential-free
synthetic retest PASSed without real network, credentials, evidence or state mutation.

Execution source was `063f3ab86c6f6c8c1ae649335856700dfeda6a22` on governed PI3
`nutandpihole`, operator `jazofv1`, execution IPv4 `192.168.100.252`, logical HA
instance `PI5_HA`. Source/governance/target/runtime prechecks, sanitized evidence
validation and source postcheck PASSed. Client and operator block return codes
were zero. The credential value was not persisted and is not repository evidence.

Observed HA Core **2026.9.4**, source-review baseline **2026.8.1**:
**COMPATIBLE_UPDATED**, failed capability **NONE**, no likely update compatibility
break. Required capabilities passed, and authoritative central compatibility state
agreed with the evidence. This demonstrates capability-first compatibility with
the observed 2026.9.4 interface and the mechanism for later versions; it does not
prove compatibility with every future HA release.

Sanitized aggregate counts: devices **229**, entities **2425**, areas **22**,
config entries **97**. Accepted PASS warnings: `CLASSIFICATION_NOT_DERIVED`
(unproven identity classes deliberately not inferred), `UNKNOWN_FIELDS`
(additive fields counted by type without publishing names/values), and
`UNPUBLISHED_NAMESPACES` (non-allowlisted namespaces counted without literals).
These warnings do not invalidate 2b or indicate a compatibility failure.

Private evidence reference: `/tmp/hioc-pe4-ha-discovery-7bb82b7c`.
Report SHA-256: `322e237404c3c721be782e9ce2dbc4ceb1e63b8374af00b6fe75a940624d2ded`.
Result SHA-256: `685606f76aad93ede32b52c2ffa34984408d62d408185ab6141791eded478e43`.
The operator's independent read-only review PASSed source/directory/hash/schema
binding, report schema, success semantics, structure fingerprint, result marker,
privacy scan, compatibility-state schema/HA binding and clean source postcheck.
Review used no credential or network and did not execute the discovery client.
Evidence is referenced only: not accessed, copied, recreated, mutated or deleted.

The first exact-version-gate FAIL remains immutable historical evidence; this
corrected PASS supersedes it as the authoritative current 2b outcome. D/E/F/G and
2a retain PASS/CLOSED, E handoff ACCEPTED, Compatibility Resilience audit and
Master Plan synchronization PASS/CLOSED. No 2a/F/G rerun occurred. PE-4 remains
NOT COMPLETE, Phase 7A ACTIVE, rollback NOT PERFORMED. Next checkpoint:
**PE-4.0C Association Contract Freeze**, separately governed and NOT STARTED.
No PI3/PI5/HA access, credentials, discovery execution, rerun, deployment,
rollback or PE-4.0C occurs during this repository closure.

## Historical checkpoint chronology

Earlier checkpoint statements below are historical and superseded by the current
closure above; their historical evidence remains unchanged.

## Compatibility resilience correction - 2026-10-06

The repository now governs capability-first external dependency contracts,
sanitized persistent compatibility status and retained platform diagnostics.
See [COMPATIBILITY_RESILIENCE.md](COMPATIBILITY_RESILIENCE.md) for the complete
42-family audit, exact-pin inventory, implementation boundaries and deferred
host proofs. HA Core 2026.8.1 remains source-review provenance; it is no longer
an exact live-version gate. All four required registry commands and unsafe-schema
failure gates remain. Isolated runtime, SSH and cryptographic identities stay exact.

The first authorized 2b attempt failed safely with UNSUPPORTED_HA_DEPLOYMENT at
HA_DEPLOYMENT_DISCOVERY because of the old version gate. Preserved user-supplied
evidence: `/tmp/hioc-pe4-ha-discovery-22be880b`; report SHA256
`efd3aa0cc2f5bc00a459a0c05055ac14e5a9a7ab6cc13aeeb34aa9aa616cb087`;
result SHA256 `1e11b6e512db860a8f9b2b6af1723c6aabafd75968d7fd643c891144a7a72195`.
No remote evidence was read or changed. The new correction record binds current
source; the original preparation record and earlier exact-version evidence remain
historical. This notice supersedes older current-status statements below.

D/E/F/G PASS/CLOSED; E handoff ACCEPTED; 2a PASS/CLOSED; first 2b ATTEMPTED /
NOT COMPLETE; corrected 2b NOT STARTED; 0C NOT STARTED; PE-4 NOT COMPLETE;
Phase 7A ACTIVE; rollback NOT PERFORMED. No PI3/PI5/HA access, credentials,
deployment or corrected execution occurs in this repository checkpoint.

Repository preparation only, completed 2026-10-06. No live discovery, deployment, token,
PI3/PI5/HA access, 2a or D/E/F/G rerun, rollback, PE-4.0C, or final association
adapter is authorized by this preparation. Future execution requires separate
authorization and the existing accepted runtime/source pre-token gates.

Canonical preparation: [pe4-0b2b-discovery-preparation.json](../governance/pe4/pe4-0b2b-discovery-preparation.json).
Prerequisite: the immutable [2a execution closure](../governance/pe4/pe4-0b2a-execution-closure.json)
at `09814b8ab19553f21ff68c3a617a5164c47ef59f`. The closed 2a client retains blob
`85842a81c57187c9e119d1065fce433e5b067e1f` and SHA-256
`aa0e58ed6c7bb4586625836cc71ad0cab9270e6b11a6a5db66497115b001decf`.

## Frozen source contract

Review is pinned to **Home Assistant Core 2026.8.1**. Compact reviewed facts,
exact source paths/URLs, serializers, mandatory core, and recognized field types
are in [the Core source contract](../governance/pe4/pe4-0b2b-core-source-contract.json).
It covers the four config component files, device/entity/area registry helpers,
`homeassistant/config_entries.py`, WebSocket messages, and connection dispatch.
No large source files are vendored.

| Sequential ID | Command | Reviewed result | Permission at this tag |
|---|---|---|---|
| 1 | `config/device_registry/list` | Array from `DeviceEntry.dict_repr/json_repr` | Authenticated user; no admin decorator |
| 2 | `config/entity_registry/list` | Array from `RegistryEntry.as_partial_dict/partial_json_repr` | Authenticated user; no admin decorator |
| 3 | `config/area_registry/list` | Array from `AreaEntry.json_fragment` | Authenticated user; no admin decorator |
| 4 | `config_entries/get` | Unfiltered array of `ConfigEntry.as_json_fragment` | Authenticated user; no admin decorator |

The registered handlers list existing metadata without registry/configuration
mutation calls. Serializer cache computation is not a configuration mutation.
This source-level permission classification does not assert that a future
credential or installation will actually permit each command.

Documented REST is `NOT_SUPPORTED_BY_DOCUMENTED_REST` for this registry metadata.
These are version-pinned Core-source interfaces, not a versionless public
compatibility promise. Historical/superseded: the original tool required exact pinned version equality
in both WebSocket authentication messages. Current capability-first behavior
retains 2026.8.1 solely as source-review provenance and rejects required-capability
or unsafe-schema failures; compatible additive evolution continues.
There are no fallback, mutation, subscription, supported-features, linked-device,
get-by-ID, recursive, polling, service, state, event, or flow commands.

Device records use the single `config_entry_id`; the recognized deprecated
`config_entries`, `config_entries_subentries`, and `primary_config_entry` fields
are inventoried by type, not used to invent alternative ownership semantics.
Entity lists are partial registry records, not extended records or entity states.
Area wire records use `area_id`, not their storage serializer's `id`.
Config-entry metadata includes `state` and nested translation/subentry metadata;
only top-level types are observed, never their values or nested contents.

## Client and schema strategy

The standalone `tools/hioc-pe4-ha-registry-discovery.py` has no dependency on the
closed 2a tool, F/G, or runtime implementation. One numeric AF_INET preconnected
socket avoids DNS; a reviewed connect subclass returns every redirect exception,
`proxy=None`, no compression, no keepalive ping, queue bound one, and a silent
logger prevent fallback/network expansion and payload logging.

After one `auth_required/auth/auth_ok` exchange it sends exactly the four commands
above sequentially. IDs are strictly integer 1 through 4. Each response must have
matching `id`, `type=result`, boolean `success`, and exactly result or error.
Unknown/unauthorized commands stop; private server error text is discarded.
One bounded close follows the fourth response. One post-close receive checks
already buffered messages or the normal closed condition; it sends nothing and
is not a fifth read command or a polling loop. Extra/replayed/event messages fail.

Strict JSON rejects duplicate members, nonfinite numbers, malformed/binary
messages, and excessive nesting before decoding; decoder resource failures are
normalized. Websockets `max_size` limits messages before JSON materialization.

Each registry has a small mandatory structural core:

- device: `id`, `config_entry_id`, `connections`, `identifiers`, `area_id`,
  `disabled_by`, `via_device_id`;
- entity: `entity_id`, `platform`, `device_id`, `area_id`, `config_entry_id`,
  `disabled_by`;
- area: `area_id`;
- config entry: `entry_id`, `domain`.

Recognized fields must match source-reviewed top-level types. Optional recognized
fields may be absent; new fields are counted by top-level type. Unknown names
and nested values are never published. Inventory `optional` means observed
absence among this invocation's records, not a universal source guarantee.
Empty registries have empty observed field inventories.

Raw messages/records remain memory-only and are reduced registry by registry.
Only private ID/relationship and connection indexes survive between responses;
they are discarded after aggregate construction or failure. Four sequential reads
are not an atomic HA snapshot: dangling references are counted and produce a
bounded snapshot warning, not fabricated relationships.

## Frozen bounds and rationale

| Bound | Frozen value |
|---|---|
| Connect / WebSocket handshake | 5 seconds per operation |
| Send / receive | 15 seconds per operation |
| Absolute network deadline | 90 seconds including authentication, four command exchanges, and close |
| Close | 2 seconds, clipped by the same deadline |
| Task cancellation reaping | At most 2 seconds; transport already aborted, no new network work |
| Message | 16,777,216 bytes; no compression |
| Device / entity / area / config-entry records | 4,096 / 65,536 / 2,048 / 4,096 |
| Distinct namespace names | 128 across the invocation |
| Fields per record / distinct field names | 128 / 256 |
| JSON nesting | 32 levels |
| Interpreted identity/namespace string | 1,024 characters |
| Sanitized JSON evidence | 262,144 bytes |
| Warnings | 16, from fixed enum only |
| Retries | 0 |

Existing repository history records approximately 151 HIOC devices (master plan
and operations). A 4,096-device ceiling provides over 27 times that scale;
65,536 entities allows substantial multi-entity and virtual-entity headroom.
HA registry counts are not assumed equal to HIOC counts. Areas/config entries
also receive generous home-scale ceilings. Core returns full arrays, so 16 MiB
supports thousands of records with metadata while bounding one raw JSON message
in memory. Decoded CPython overhead may exceed wire size; the record/field/depth
limits bound that expansion. This is not a measured production memory guarantee.
The exact byte bound and record ceilings are tested at the limit and one above.

The 90-second shared budget accommodates authentication and four 15-second
responses plus bounded connection/close overhead. Each operation checks expiry
before constructing a coroutine. Expiry aborts the transport before cancellation;
the pinned asyncio/websockets operations are reaped. Stalled sends, receives,
connect, close, slow-drip progress, expiry, and interruption are synthetic tests.
No background worker or additional network cleanup budget is introduced.

## Sanitized evidence and privacy

Schema: [pe4-0b2b-discovery-report.schema.json](../governance/pe4/pe4-0b2b-discovery-report.schema.json),
version `1.0`. Fixed instance reference is `PI5_HA` with
`INSTANCE_REFERENCE_METHOD=OPERATOR_LOGICAL_LABEL`. Version output is the fixed
source reference, not a private server-supplied version dump. Deployment is
classified only as a remote HA endpoint; no OS/container/install type is inferred.

Permitted evidence comprises fixed classifications, recognized field/type/observed
optionality inventory, aggregate cardinalities and relationship-presence counts,
connection and identifier collisions, MAC structure, bounded enum warnings,
privacy validation, finite error code/stage, and a schema-only SHA-256 fingerprint.
The fingerprint hashes canonical sorted registry names and recognized field
names/types/observed optionality. It excludes namespaces, counts, IDs, names,
MACs, IPs, and every raw value. MACs and other private index values are never hashed.

Published namespace names are limited to the reviewed literal allowlist
`mac`, `bluetooth`, `zigbee`, `zwave`, `upnp`, `mqtt`, `hue`, `esphome`, `zha`,
`zwave_js`. The privacy contract permits namespace categories, but arbitrary
namespace strings could conceal a hostname or other value; all other namespaces
are counted only. No raw household identifier can select an evidence key.

MAC evidence counts canonical, normalization-required, invalid, zero/one/multiple,
duplicate-within-device, collision-value, and conflicting-device categories.
Normalization accepts standard colon, hyphen, dotted, or compact 12-hex forms
only and is used transiently for comparisons. It is not an association decision.

Entity device membership, disabled status, via-device, area, and config-entry
relationships are aggregate facts. `template_platform`, `group_domain`,
`scene_domain`, and `automation_domain` are exact structural labels, not assertions
of helper/physical/cloud identity. Physical, helper, integration-level,
virtual/cloud classifications are explicitly `NOT_DERIVED`: the authorized
records cannot reliably prove them. No final association adapter is implemented.

Final evidence validation uses exact structural allowlists, finite enums, integer
bounds, type checks, namespace literals, schema fingerprint recomputation, and
textual defenses on allowed schema tokens. It rejects raw fields/values, addresses,
hostnames, IDs, secrets, URLs, arbitrary warnings, and nested raw objects. Failure
reports have empty registry inventories. Synthetic household-looking values must
be absent from every report/result/terminal output. No Python zeroization claim
is made; credentials and raw values exist only in process memory.

## Execution prerequisites and publication

Future execution host/operator/address remain PI3 `nutandpihole` / `jazofv1` /
`192.168.100.252`; HA remains the approved numeric remote endpoint. Runtime remains
`/home/jazofv1/hioc/runtime/pe4/environments/cpython311-websockets 16.1.1-lock-v1`,
CPython 3.11.2 and websockets 16.1.1. No runtime republish/reinstallation occurs.
Existing accepted-tree, architecture/SOABI, distribution, source-clean/synchronized,
source blob/SHA, parent-shell/TTY, and postcheck gates remain required by the future
separate authorization. The client additionally checks runtime prefix/version,
isolated/no-bytecode flags, dependency origin/version, execution identity,
TTY, and absence of proxy influence. Credential acquisition is `getpass` only,
with locally fatal `GetPassWarning`; no argv/env/file/fallback credential source.

Evidence uses one tool-created directory `/tmp/hioc-pe4-ha-discovery-XXXXXXXX`
with eight random hex suffix characters, mode `0700`, under the checked root-owned
sticky `/tmp` descriptor. There is no caller-supplied path and no mkdir retry.
Files are only `discovery-report.json` and `discovery-result.txt`, mode `0600`.
Exclusive no-follow temporary creation, complete writes, file fsync, atomic
non-overwriting hard-link publication, directory fsync, and repeated descriptor/
name checks precede result-last publication. The result completion marker is
withdrawn if its final durability/binding cannot be confirmed. Existing collision
names are never deleted or overwritten. Interruption removes only invocation-owned
unpublished temporary names; sanitized incomplete evidence may remain without a
completion marker. Failures after preflight may publish minimal sanitized FAIL
reports; publication itself is never retried.

Repository tests use only synthetic adapters and controlled temporary fixtures;
they do not create `/tmp` discovery directories, make network calls, or use real
credentials. Windows synthetic tests verify POSIX call semantics; no privileged
mount/namespace/WSL/production test is required or performed in preparation.

## Prepared lifecycle and live-only uncertainties

D/E/F/G **PASS/CLOSED**; E handoff **ACCEPTED**; 2a **PASS/CLOSED**;
2b **NOT STARTED / PREPARED FOR SEPARATE AUTHORIZATION**; PE-4 **NOT COMPLETE**;
Phase 7A **ACTIVE**; rollback **NOT PERFORMED**.

Actual command permission/availability, registry shape/size, snapshot completeness,
MAC representation/collisions, and production timing remain live-only unknowns.
They must be observed by a separately authorized bounded 2b execution; unsupported
structure or bounds fail closed. This document provides no PI3 execution command.

## Resumed preparation review

The preserved worktree at baseline 09814b8ab19553f21ff68c3a617a5164c47ef59f
contained five modified governance documents and six new 2b artifacts, all expected
preparation work. No staged changes, active Git operation, unrelated work, or
uncertain-provenance items were found. No existing work was reset, stashed,
checked out, cleaned, or discarded.

The review added a narrowly scoped standalone-client exemption to the runtime
lifecycle entrypoint enumeration, parallel to the existing 2a exemption. Runtime
implementations and historical evidence remain byte-identical. New discovery tests
verify that the 2b preparation record requires separate execution authorization
and that the standalone client rejects lifecycle CLI arguments. Duplicate warning
entries are rejected by both the final evidence validator and schema.

## Final repository validation - 2026-10-06

- Full repository suite ran once: 1,289 tests, 47 skips. Its document encoding
  failure was corrected and historical document text was verified unchanged.
  Its wheel-cache setup error was resolved with read access to the existing
  governed cache; no runtime installation/publication occurred.
- Focused follow-up covered 273 tests, including 62 discovery tests, the closed
  2a checks, runtime/governance regressions, and 26 controlled Action E tests.
  One shell check selected the Windows WSL launcher and could not resolve the
  Windows source path; all 22 affected Action 9 checks then passed with Git Bash.
  No unresolved test failure remains.
- Release manifest/artifact and all 26 shell syntax checks passed. The release
  script skipped its unavailable python3 alias; separate in-memory compilation
  passed for all 140 repository Python files in tools, tests, pi4/bin and pi4/lib.
- Thirteen synthetic success/failure evidence reports passed the repository
  schema validator. Bound source/schema/prerequisite digests, command allowlist,
  privacy fixtures, protected 2a identity, scope, and whitespace checks passed.
- No live endpoint, PI3, PI5, real credential, discovery invocation, deployment,
  or production lifecycle action was used. Historical implementation/evidence
  and accepted runtime/dependency artifacts remain unchanged.

The Core device/entity list handlers may omit entries that cannot be serialized.
Discovery cardinalities therefore describe returned records, not an independent
proof of total internal registry membership. No extra enumeration is authorized.
