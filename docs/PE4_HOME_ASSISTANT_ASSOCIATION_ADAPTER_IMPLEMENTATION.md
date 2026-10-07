# PE-4 Home Assistant Association Adapter Implementation

## Current pre-deployment correction — 2026-10-06

Adapter Implementation PASS/CLOSED, corrected before deployment. Original implementation
commit `0bdb9340157daba4a6948251922d762cc4fc97ff` passed repository tests but received
an independent pre-deployment review identifying incomplete canonical-envelope type
validation and shared filesystem helpers capable of misclassifying state failures.
No deployment or production adapter execution/authentication occurred before correction.
The [current correction record](../governance/pe4/pe4-ha-association-adapter-predeployment-correction.json)
and [closed schema](../governance/pe4/pe4-ha-association-adapter-predeployment-correction.schema.json)
bind the CURRENT executable identities. The original implementation record/schema
and original commit remain unchanged historical evidence; their source bindings are
historical, not current executable identities.

Canonical input now requires an exact dict root, schema_version 1.0, timezone-aware
updated string, devices/services lists, and topology/dependencies/summary dicts.
Malformed shape fails CANONICAL_INVENTORY_INPUT before credentials/HA. Only devices[].mac
remains association authority; the other root types establish envelope integrity.

NativeFS credential ACL checks retain CREDENTIAL_ACQUISITION. PosixFS explicitly owns
STATE_PUBLICATION security checks; shared name binding dispatches through the filesystem's
security context. Lock, contract, prior and inventory call boundaries retain their respective
LOCK_ACQUISITION, CONTRACT_VALIDATION, PRIOR_STATE_VALIDATION and CANONICAL_INVENTORY_INPUT
stages. Recovery/publication security never originates credential acquisition errors.
No owner, mode, ACL, no-follow, inode/name or durability check was removed.

Namespace conclusion B: the limit is the combined distinct namespace union across
connections and optional identifiers. Frozen preparation transport.max_namespaces is
128; its source_review binding pins the historical 2b reducer to Git blob
`9e77993c3f6a533b3d394017d4d97e2366959797`, SHA-256
`b074608e98e887767be964120e8bfad8b5f7fba5fa17d671b0a1a1704f35c1b8`.
That reducer's consume() loops over connections and identifiers and inserts both
into one namespace_union before enforcing MAX_NAMESPACES. The 0C contract's
Identifier namespaces section denies them HIOC identity authority. Optional identifiers
therefore require reviewed exact two-string pairs, bounded/nonempty strings, and
share the 128-name transport counter. They are never MAC-indexed, matched or persisted.
Connection MAC decision semantics and all other frozen identity/lifecycle rules are unchanged.

Current focused validation: 70 tests passed, including 10 new correction tests with
separate envelope cases, real production ACL/name helpers, native lock validation,
recovery/publication stage assertions, exact LKG/absence and namespace boundaries.
Regressions: 275 run, 274 passed, one existing rsync-unavailable release skip.
Total: 345 run, 344 passed, one skipped. Syntax/import safety, canonical schema/JSON,
links, source identities, privacy/prohibited-path and diff checks passed.

Deployment and Scheduler Deployment NOT STARTED; Public Projection DEFERRED;
PE-4 NOT COMPLETE; Phase 7A ACTIVE; Rollback NOT PERFORMED. No real credential,
PI3/PI5/HA access, adapter network execution, production mutation, deployment,
scheduler activation, MQTT, public projection or rollback occurred.
Next remains **PE-4 Home Assistant Association Adapter Deployment Preparation**;
that checkpoint has not begun.

## Historical original implementation closure

Repository implementation and Windows synthetic validation: PASS/CLOSED.
Starting commit: `8923a074ac304a5cfe46367330819291caed6550`.
[Historical implementation record](../governance/pe4/pe4-ha-association-adapter-implementation.json)
and [closed schema](../governance/pe4/pe4-ha-association-adapter-implementation.schema.json)
bind source blobs and SHA-256 identities without a circular implementation-commit binding.

The [0C contract](PE4_HOME_ASSISTANT_ASSOCIATION_CONTRACT.md),
[0C.1 lifecycle](PE4_HOME_ASSISTANT_ASSOCIATION_LIFECYCLE_CLARIFICATION.md),
[frozen preparation](PE4_HOME_ASSISTANT_ASSOCIATION_ADAPTER_IMPLEMENTATION_PREPARATION.md),
and [current credential closure](PE4_HOME_ASSISTANT_RUNTIME_CREDENTIAL_PROVISIONING.md)
remain authoritative. Historical preparation's optional-LF wording is superseded
by TOKEN_PLUS_EXACTLY_ONE_FINAL_LF and
REQUIRE_AND_REMOVE_EXACTLY_ONE_FINAL_LF_NO_TRIM. Historical artifacts are unchanged.

## Runtime and input gates

The runtime-owned module is `pi4/lib/hioc/home_assistant_association.py`;
`pi4/bin/hioc-home-assistant-association.py` is a thin entrypoint without options.
Future governed launch uses `/home/jazofv1/hioc/runtime/pe4/active/bin/python`
with explicit `-I -B`, installed `/home/jazofv1/hioc/pi4/lib`, and accepted environment
`/home/jazofv1/hioc/runtime/pe4/environments/cpython311-websockets16.1.1-lock-v1`.
CPython 3.11.2, aarch64, cpython-311-aarch64-linux-gnu, websockets 16.1.1,
exact module origin, isolation, no bytecode and no unreviewed site paths are gates.
Only stdlib and accepted websockets are used; tools proof clients are not imported.
Linux/POSIX, actual jazofv1 on nutandpihole, HIOC_HOME `/home/jazofv1/hioc`, and
local IPv4 `192.168.100.252` are required before secrets/network.

Nonsecret `HIOC_HA_ENDPOINT` must be explicitly configured in `config/hioc.conf`
as `ws://192.168.100.251:8123/api/websocket`. Missing/drift fails; no default.
HIOC_HOME/HIOC_HA_ENDPOINT and case-insensitive proxy environment influence fail.
No production configuration or config example was changed.

The permanent 0600 jazofv1:jazofv1 lock is
`/home/jazofv1/hioc/state/inventory/associations/.home_assistant.lock` in owned 0700
associations. Nonblocking exclusive flock has zero acquisition timeout, spans HA
work, releases in finally and is never unlinked. Lock order is association, then
contracts/recovery/prior/inventory, credential, HA without other locks, candidate
and inventory recheck, association commit, existing compatibility lock, unlock.

Only ENOENT initializes an in-memory first baseline. Invalid prior/security/schema
1.0/history fails closed. Canonical inventory is fixed `state/inventory/inventory.json`,
read-only, schema 1.0, <=16 MiB/depth 32/65536 devices, unique dev_ IDs, canonical
MAC set index, aware updated <=5400 seconds old and <=60 seconds future.
Liveness/health never gate association. Before replacement the exact inventory bytes
are reopened, revalidated and compared; no retry or inventory lock.

Credential `/etc/hioc/credentials/home_assistant.token` uses root:jazofv1 0640,
root:jazofv1 0750 directories, single regular link, no-follow descriptor traversal,
NSS reader/ACL checks and before/after/name validation. One 2..4097-byte read requires
exactly one final LF; remaining 1..4096 bytes are printable ASCII 0x21..0x7E.
No trim, prompt, fallback, argv/environment/config token or credential digest.
References are released on network exit; no zeroization guarantee is claimed.

## HA protocol and association

One numeric AF_INET preconnected socket targets 192.168.100.251:8123; no DNS,
proxy, redirect, compression, ping, subscription, retry or alternate endpoint.
Connect 5 seconds; each send/receive 15; close 2; total network 90; invocation 180;
reaping grace 2; messages <=16 MiB, max_queue=1. A silent logger exposes no frames.
Strict JSON rejects duplicates/nonfinite values, depth >32, strings >1024,
record fields >128, distinct fields >256 and namespaces >128. Required bounded
structural cores and registry IDs/entity IDs are validated without last-wins.

After auth_required/auth_ok with consistent sanitized version, commands are exactly:

1. ID 1: `config/device_registry/list`
2. ID 2: `config/entity_registry/list`
3. ID 3: `config/area_registry/list`
4. ID 4: `config_entries/get`

Exact integer correlation, success=true and result shape are mandatory. All reads
must succeed; replay/unexpected responses fail. No fifth command or fallback.
Global HA indexing includes valid evidence on invalid/multiple-MAC devices.
Only one valid distinct noncolliding connection namespace mac mapping to one
canonical HIOC ID is strong. Supporting identifiers and IP/name/hostname/vendor
never create identity; generic HA integration ingestion is prohibited.

0C.1 reconfirms current strong pairs, preserves earliest exact-pair first time,
retires unconfirmed prior active episodes by frozen precedence, retains old episodes
unchanged, enforces historical HA ownership and current one-to-one cardinality.
Safe recreation requires all frozen conditions, absent prior-active/latest-history
source, no tie/competition/conflict; never-bound new pairs get new first time.
Same-pair reactivation preserves earliest first. History limit 4096 has no eviction;
4097 fails with entire LKG unchanged. Failed cycles never retire or advance timestamps.

Entity membership follows entity.device_id through a strong HA pair. Config entries
are deduplicated from reviewed device/member refs and resolve entry_id/domain.
Only direct device area yields area_candidate; via_device_id is private reviewed
metadata. Optional dangling/unsafe/unrepresentable fields/members are omitted with
INCOMPLETE while preserving strong identity. COMPLETE requires all present reviewed
supporting refs safe. Raw unique_id/connections/options/URLs/MAC/IP are never copied.
Closed internal schema validation covers every actual frozen keyword, plus
cross-record chronology, ownership, history preservation, summaries and privacy.

## Durable private publication and compatibility

Private schema 1.1 state is
`/home/jazofv1/hioc/state/inventory/associations/home_assistant.json`, owned 0600.
A random owned 0700 `.home_assistant.txn-<32_lower_hex>` stages 0600 candidate,
exact-prior-inode hardlink when present, closed <=4096-byte intent, and commit marker.
Complete writes, file rereads/fsyncs, directory fsyncs, input/prior/name checks,
atomic replacement and final schema/byte/security verification precede the verified
durable committed marker. Precommit failures durably invalidate an uncommitted marker,
restore the exact prior inode/bytes or absence, fsync and verify. Unproved restoration
returns preservation UNKNOWN and retains material, blocking secrets/network at recovery.
Recovery rejects malformed/multiple pending namespaces; committed state is verified.
Atomic rename to `.home_assistant.done-<32_lower_hex>` and parent fsync precede pinned
child cleanup. Done recovery is cleanup-only and never restores prior state.

ha_core receives a full version_metadata/authentication/device_registry/entity_registry/
area_registry/config_entries bool-or-None map. Existing assess runs before commit using
known compatible history; existing update_status runs after commit or observed HA
failure. Local pre-HA failures do not replace evidence. Version drift alone continues
as COMPATIBLE_UPDATED. No generic compatibility writer or new dependency row exists.
Postcommit reporting or cleanup failure is PASS_WITH_WARNING, preserving committed state.

Output is <=4096 bytes/16 allowlisted lines with factual TRUE/FALSE/UNKNOWN and
validated counts or UNKNOWN, no exception text, token, household IDs or raw response.
PASS and PASS_WITH_WARNING exit zero; FAIL exits nonzero. Retry is next invocation.

## Validation and checkpoint boundary

Focused implementation tests exercise temporary byte flow with synthetic POSIX
ownership/ACL/flock/directory-fsync metadata, memory HA messages and injected syscall
faults, plus the actual complete-write loop. Native Linux deployment syscall proof
remains a separately authorized production checkpoint; no fixture is a production override.
60 focused tests passed. Requested regressions ran 275 tests: 274 passed and one
existing POSIX-rsync-dependent release test was skipped on Windows. Total: 335 run,
334 passed, one skipped. Syntax/import safety, canonical closed JSON, source identities,
protected baseline bytes, documentation links and diff checks also passed.

Existing 0C/0C.1/preparation/credential/closure/2b/Master/inventory/compatibility/release
regressions preserve historical authority and now bind current implementation sources.

| Checkpoint | State |
|---|---|
| Adapter Implementation | PASS/CLOSED |
| Deployment | NOT STARTED |
| Scheduler Deployment | NOT STARTED |
| PE-4 | NOT COMPLETE |
| Phase 7A | ACTIVE |
| Rollback | NOT PERFORMED |

No real credential, PI3/PI5/HA access, network validation, production state mutation,
deployment, scheduler activation, MQTT association publication, public projection or
rollback occurred. Future user cron HIOC_PE4_HA_ASSOCIATION at `5,35 * * * *` remains
uninstalled/inactive. Public projection and PE-5 remain separately governed.
Next: **PE-4 Home Assistant Association Adapter Deployment Preparation**.
No PI3 deployment command is authorized or supplied here.
