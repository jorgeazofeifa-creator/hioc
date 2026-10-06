# PE-4 Home Assistant Association Adapter Implementation Preparation

## Closure and immediate prerequisite

Implementation Preparation is PASS/CLOSED, resumed from clean synchronized main
`9bdf8bdfb990c4cedb821f79c5e2306b868a92fa`. The prior attempt correctly stopped
without changes. [0C](PE4_HOME_ASSISTANT_ASSOCIATION_CONTRACT.md) and
[0C.1](PE4_HOME_ASSISTANT_ASSOCIATION_LIFECYCLE_CLARIFICATION.md) now provide the
identity and successful-cycle lifecycle authorities. Historical records/schemas
are unchanged. Future state uses
[schema 1.1](../governance/pe4/pe4-home-assistant-association-state-v1.1.schema.json).

The [canonical preparation record](../governance/pe4/pe4-ha-association-adapter-implementation-preparation.json)
and [closed record schema](../governance/pe4/pe4-ha-association-adapter-implementation-preparation.schema.json)
freeze this architecture. The record binds 59 reviewed baseline source artifacts
by Git blob and SHA-256, grouped by role. These are local source findings, with no
fresh production or host-support claim.

Immediate next: **PE-4 Home Assistant Runtime Credential Provisioning**, NOT STARTED.
No repository-supported HA secret mechanism satisfies this unattended contract.
That prerequisite must close before **PE-4 Home Assistant Association Adapter
Implementation**, also NOT STARTED. No credential or runtime file is created here.
D/E/F/G, E handoff, 2a, 2b, 0C and 0C.1 retain accepted closures. PE-4 remains
NOT COMPLETE, Phase 7A ACTIVE, rollback NOT PERFORMED. No production authorization.

## Actual source review

| Boundary | Exact repository sources | Finding and design |
| --- | --- | --- |
| Canonical identity | [inventory.py](../pi4/lib/hioc/inventory.py), [Inventory Engine](../pi4/bin/hioc-inventory-engine.py), [schemas](../pi4/lib/hioc/core/schemas.py) | Reconciliation produces devices[].id/mac; engine atomically replaces canonical envelope before sidecars. Consume that envelope only. |
| Generic integration | integration_inventory, PassiveNetworkDriver, merge_records in inventory.py | Input participates in identity/observation reconciliation. HOME_ASSISTANT_GENERIC_INTEGRATION_INGESTION = PROHIBITED. |
| State publication | [StateStore](../pi4/lib/hioc/core/state.py), [manufacturer writer/lock](../pi4/lib/hioc/manufacturer.py), [private runtime writer](../tools/hioc_pe4_runtime_common.py) | Generic writer fixed .tmp has incomplete no-follow/ownership/locking/fsync safeguards. Reviewed private patterns inform a dedicated association writer. |
| Compatibility | [engine](../pi4/lib/hioc/core/compatibility.py), [registry](../governance/compatibility-contracts.json), [platform](../pi4/bin/hioc-platform-status.py) | ha_core requires six capabilities. Locked update_status preserves other dependencies but replaces a supplied dependency's map, without partial-producer aggregation. |
| Proof clients | [2a](../tools/hioc-pe4-ha-auth-capability.py), [2b](../tools/hioc-pe4-ha-registry-discovery.py), [closure](../governance/pe4/pe4-0b2b-execution-closure.json) | Interactive getpass suits bounded proofs. 2b supplies reviewed numeric WebSocket transport/correlation/privacy. Preserve identities; no production tools imports. |
| Isolated runtime | [lock](../requirements-pe4.lock), [accepted E](../governance/pe4/accepted-action-e.json), [G](../tools/hioc_pe4_action_g.py), [dependency contract](PE4_ISOLATED_RUNTIME_DEPENDENCY_CONTRACT.md), [lifecycle](PE4_ISOLATED_RUNTIME_LIFECYCLE.md) | Accepted CPython/websockets plus stdlib suffice. G controlled child is historical credential-free proof architecture. No new package/runtime needed. |
| Config/logging | [ConfigService](../pi4/lib/hioc/core/config.py), [defaults](../pi4/lib/hioc/config.py), [example](../pi4/config/hioc.conf.example), [runtime](../pi4/lib/hioc/runtime.py), [logger](../pi4/lib/hioc/core/logging.py) | Config merges toolkit/config/environment. Validate final nonsecret endpoint strictly. Logger allows arbitrary fields/tracebacks; association constrains safe output. |
| Secret audit | [MQTT](../pi4/lib/hioc/mqtt.py), [toolkit operator](../pi4-tools/operator-deploy-network-probe.sh), [network probe](../pi4-tools/scripts/hioc-network-probe.sh), config/install sources | MQTT config/environment/argv patterns do not meet HA contract. Source search found no HIOC LoadCredential, credential-directory delivery, validated HA helper, provisioning or rotation support. No real secret file opened. |
| Scheduling | [installer](../pi4/install_pi4.sh), [uninstaller](../pi4/uninstall_pi4.sh), [Operations](OPERATIONS.md) | User cron/flock, inventory at 0/30; no HIOC systemd credential service/timer architecture. Select separate cron job with internal lock. |
| Releases | [install](../release/install.sh), [build](../release/build.sh), [package](../release/package.sh), [helpers](../release/lib.sh), [upgrade](../release/upgrade.sh), [rollback](../release/rollback.sh), [Deployment](DEPLOYMENT.md), [HA installer](../homeassistant/install_ha.sh) | Tracked-source build/rsync install. Upgrade excludes state/runtime/pe4; rollback restores code and invokes installer. Secrets outside release ownership; no HA package changes. |
| Recovery/tests | [runtime rollback](../tools/hioc-pe4-runtime-rollback.py), [release tests](../tests/test_release.py), [compatibility tests](../tests/test_compatibility.py), [2b tests](../tests/test_pe4_ha_registry_discovery.py), 0C/0C.1/closure/governance tests | Runtime rollback governs accepted isolated artifacts only. Future association rollback preserves state/history/schema and credentials. Fault tests belong to implementation. |

## Exact future files and runtime

Module `pi4/lib/hioc/home_assistant_association.py`; executable
`pi4/bin/hioc-home-assistant-association.py`, following current module/CLI conventions.
Neither file exists yet. Production module owns reviewed transport, private schema
projection, validators, locking/publication; CLI coordinates stages and safe results.
No tools import or proof-evidence persistence shortcut.

Use `/home/jazofv1/hioc/runtime/pe4/active/bin/python` with `-I -B`, resolving to
`/home/jazofv1/hioc/runtime/pe4/environments/cpython311-websockets16.1.1-lock-v1`.
CPython 3.11.2, aarch64, SOABI cpython-311-aarch64-linux-gnu, websockets 16.1.1.
Only stdlib plus accepted websockets; no jsonschema package is available/required.
Later validator must enforce every frozen schema keyword, reject unsupported ones,
and be checked against independent test validation. Shallow core Schema is insufficient.

Entry admits only verified installed pi4/lib. Before secrets, verify release source,
accepted runtime tree/distributions/prefix/import origins, isolated/no-bytecode flags,
endpoint. No unreviewed .pth/site customization; isolated mode ignores user site and
Python environment overrides. Explicit interpreter for cron/manual execution; no
system-Python shebang reliance. No F/G rerun, runtime mutation or new Python line.

## Canonical inventory input

Read only `/home/jazofv1/hioc/state/inventory/inventory.json` (relative
`state/inventory/inventory.json`), produced by Inventory Engine. Never devices.json,
raw ARP/DHCP/integrations/known infrastructure/MQTT/HA input. Require schema_version
1.0, timezone-aware updated, devices/services arrays, topology/dependencies/summary
objects, matching current producer. Inventory need not be closed; other fields do
not gain HA matching authority.

Bound bytes 16 MiB, depth 32, devices 65536. Every device object has a unique stable
id matching dev_[0-9a-f]{16}. Read canonical devices[].mac if present: string, empty
for non-MAC identity, otherwise valid existing trim/lowercase/hyphen-to-colon form.
Malformed nonempty canonical MAC fails input validation. Copy existing id, never
create/repair/promote identity. Index each normalized MAC to a set of HIOC IDs;
duplicates are HIOC ambiguity, never last-record-wins. Non-MAC identity is excluded.

Missing/unreadable/malformed/oversized/unsupported/duplicate-ID/unstable input fails
CANONICAL_INVENTORY_INPUT. Valid empty devices permits genuine disappearance under
0C.1; missing file never becomes empty fallback. Do not use read_json fallback.
Require publication updated no older than 5400 seconds (three half-hour periods),
no more than 60 seconds future skew. This is publication freshness, not device
liveness: last_seen/offline/health never gate association. Parse timezone-aware
instants/current UTC; bad clock/freshness fails closed.

No-follow validated owned traversal, one regular-file FD, bounded read, before/after
fstat/inode pin. Atomic inventory replacement leaves a complete prior/new envelope.
Before association commit, reopen and compare current bytes; change fails cycle for
later scheduled retry, no internal reread loop. This is coherence at final check,
not cross-file atomicity with later inventory generations. Hold no inventory lock.

## Dedicated lock and ordering

`state/inventory/associations/.home_assistant.lock`, jazofv1:jazofv1, exact 0600,
regular single-link file; parent associations directory exact 0700, same owner/group.
Pin directory FDs and inode/name bindings; forbid symlink/reparse/special objects,
mode/ownership drift. Ancestors root/approved operator owned and not untrusted-writable.
Verified runtime active pointer is a specific exception, never a state/secret exception.

POSIX exclusive nonblocking flock, timeout zero. Contention LOCK_ACQUISITION_FAILED
before secrets/network. Permanent lock file; unlock/close finally, never unlink.
Manual/scheduled invocations share the same internal lock.

Order: association lock; contracts/transaction recovery; validated prior and inventory;
credential; bounded HA acquisition; full candidate validation/inventory recheck;
association commit; short compatibility update under engine lock; association unlock.
Dedicated lock intentionally spans bounded HA work (90 seconds networking), serializing
prior/candidate generation. Never hold inventory/compatibility locks during network.
Existing compatibility writers never acquire association lock; sole nested order is
association then compatibility, no reverse path. Unlocked two-phase generation adds
prior-generation races without useful benefit at half-hour cadence.

## Dedicated private publication transaction

`state/inventory/associations/home_assistant.json`, exact 0600 jazofv1:jazofv1,
closed schema 1.1. Prior owned regular state validated before use. Only ENOENT permits
empty in-memory first-run baseline. Malformed/schema-1.0 prior fails closed; no reset
or implicit migration. Full candidate schema/semantic/privacy validation precedes
staging; UTF-8 compact sorted JSON plus LF, allow_nan false, maximum 16 MiB.

Under association lock allocate exclusive owned 0700 same-filesystem staging
`.home_assistant.txn-<32_lower_hex>` under associations. Children descriptor-relative
O_EXCL/O_NOFOLLOW, 0600. Pin original final inode; private hard link prior.json if
present, otherwise absence marker. Prior link count increases only for verified
transaction backup and returns to one on cleanup. This is private association data,
never proof evidence or credentials.

intent.json is closed metadata at most 4096 bytes: transaction ID, fixed final basename,
prior-presence boolean, prior/candidate lengths and SHA-256 identities; no arbitrary
paths/household values. Durably prepare candidate/backup/intent before replacement:
complete write, file flush/fsync, reread/hash/schema/metadata, transaction and parent
fsync. Revalidate parent/name/prior bindings; atomically replace final with pinned
candidate; no-follow reread verifies exact bytes/schema/owner/mode; fsync associations.
Write/sync closed committed.json (transaction ID, intent/candidate digest) and its
directory. Verified durable commit alone is success. No Path.replace-only shortcut.

Pre-commit failure retains or restores original inode/absence, fsyncs and verifies.
Durably invalidate any uncommitted commit marker before restoring. Interrupted
uncommitted intent recovers under lock before prior read/credential/network. Valid
committed marker preserves candidate and completes cleanup. Multiple pending
transactions or unexpected names/metadata stop; no arbitrary winner. No failed
candidate becomes accepted current state.

After commit atomically rename staging to `.home_assistant.done-<32_lower_hex>` and
fsync parent before removing children. Done namespace is cleanup-only, so interrupted
cleanup never restores an older successful state. Uncommitted cleanup follows verified
restoration. Delete only pinned transaction-owned objects, no wildcard deletion.
Unverifiable restoration/durability stops STATE_PUBLICATION_FAILED, retains recovery
material, reports preservation UNKNOWN, and permits no new secret/network work.
Implementation must prove fault paths; never fabricate TRUE on physical storage failure.
Post-commit cleanup/reporting errors are committed PASS_WITH_WARNING, not failed cycles
or a reason to rewrite valid state. This boundary preserves 0C.1 failed-cycle semantics.

## Unattended credential architecture and prerequisite

Select root-managed private file: current HIOC uses user cron, with no systemd
credential delivery. Logical name home_assistant_access_token, storage
`/etc/hioc/credentials/home_assistant.token`, root:jazofv1 exact 0640. Directories
/etc/hioc and credentials root:jazofv1 exact 0750, root writable only. Provisioning
must prove group readers are only approved runtime operator/root; validate ancestors,
ACLs, regular single-link file, mode/owner, no-follow/symlink/reparse policy and
inode/name binding. No real token in Git or any preparation artifact.

Read once after practical secret-free preflight. Token at most 4096 bytes; file at
most 4097 including optional one final LF. Remove at most that LF, no generic strip.
Nonempty ASCII 0x21-0x7E only; no spaces/tabs/CR/interior LF/NUL/non-ASCII. No prompt,
retry/fallback. O_NOFOLLOW/O_NONBLOCK, metadata before/after; reject special files.

No token argv/subprocess/normal environment/ordinary configuration/state/evidence/logs/
MQTT/exception text/traceback. Process-memory references only, minimize copies, release
after HA networking on all paths. Reference release is not physical zeroization.
Root-authorized private exclusive staging/validation/fsync/atomic replacement rotates
secret. Inflight pinned descriptor/token may complete; next invocation reads new file.
Deletion makes next invocation fail and retain LKG. Installer never creates/overwrites
secret; /etc location is outside Git/releases/upgrade backups/code rollback.

Credential provisioning must independently prove local permissions, redacted acquisition,
rotation/deletion, upgrade/rollback preservation without token evidence. HA authentication
belongs to later adapter validation, not provisioning/discovery/repeated proofs.

## Governed endpoint and transport

Future nonsecret key HIOC_HA_ENDPOINT in `/home/jazofv1/hioc/config/hioc.conf`, existing
ConfigService. It is absent today; support belongs to later implementation. Require
exact final effective `ws://192.168.100.251:8123/api/websocket`, no implicit default.
Missing/different endpoint fails TARGET_VALIDATION. Validate HIOC_HOME
/home/jazofv1/hioc, PI3 hostname nutandpihole, operator jazofv1, IPv4 192.168.100.252
before secrets. Instance PI5_HA. Config contains neither token nor token path.
Reject target/home-changing environment overrides and proxy influence. Remote PI5
architecture unchanged; no alternate hosts, discovery, broad scan or TLS-policy change.

Reimplement reviewed 2b transport in production module: one numeric AF_INET preconnected
socket, no DNS/redirect/proxy/compression/ping/subscription/fallback, bounded queue,
silent WebSocket logger. Connect 5 seconds, send/receive 15, close 2, shared total
network budget 90 seconds immediately after credential acquisition; task reaping grace
at most 2 with no new network work. Whole invocation 180 seconds; publication
interruptions obey recovery contract.

Bounds: message 16 MiB, depth 32, fields/record 128, distinct field names 256,
namespaces 128, strings 1024 characters; device/entity/area/config-entry records
4096/65536/2048/4096. Strict JSON rejects duplicate keys/nonfinite numbers/wrong types.
Check greeting/auth and sanitized consistent HA version. Commands in exact order,
strict integer IDs 1,2,3,4:

1. config/device_registry/list
2. config/entity_registry/list
3. config/area_registry/list
4. config_entries/get

All four successes and compatible structural cores mandatory. Correlated
id/type/success/result; reject errors/replays/unexpected messages/timeouts/oversize.
Zero retries, fifth command, subscriptions, state polls, services, mutations, .storage,
database, raw persistence/logging or fallback. Use 0C structural cores rather than
making every 2026.9.4 optional field required. Recognized consumed fields retain
reviewed types; unknown optional fields/namespaces are bounded count/type only.

## Compatibility ownership

Existing single ha_core dependency, `governance/compatibility-contracts.json`, status
`state/platform/compatibility.json`. Required exactly version_metadata, authentication,
device_registry, entity_registry, area_registry, config_entries. None downgraded.
Association is sole recurring HA observer; whole six-capability map per actual HA
observation. True proven, False observed break, None unobserved; transport unavailable
sets available False. Local credential/lock/inventory errors do not erase HA evidence.
No second HA row, partial producers or unions of stale evidence.

Historical 2b record_compatibility uses observation_from_ha/refresh_status and remains
unchanged. After cutover no proof rerun is authorized; later HA proofs need separate
governance/scheduler quiescence before writing same dependency. Existing inventory/
platform observers write other dependencies through serialized update_status, preserving
HA entries subject to current freshness semantics. No aggregation prerequisite with
selected single full-map HA producer. Multiple HA producers would reopen aggregation
governance before implementation.

Assess current full observation using existing assess and last-known-compatible history
before association commit. Version informational; COMPATIBLE_UPDATED continues, no
exact HA release gate. Required failures isolate association, not DHCP/NUT/inventory/
manufacturer/others. Update actual HA observations through update_status, short
three-second compatibility lock, no direct unguarded writer. Failure observations may
update compatibility while association stays prior. Post-commit reporting failure is
COMPATIBILITY_REPORTING_FAILED/PASS_WITH_WARNING: private state already passed
assessment. No adapter MQTT; existing platform subsystem owns its existing sanitized
compatibility projection.

## 0C.1 algorithm and private relationships

Required inputs/compatibility complete before retirement. Build global HA distinct
normalized MAC sets, invalid flags/reverse index, including valid MACs on invalid/
multiple records; then HIOC canonical MAC-to-ID sets. Apply all deterministic 0C
outcomes, no fuzzy/name/IP/hostname/manufacturer matching.

Validate prior active/history ownership/cardinality. Same pair strong reconfirmation
retains earliest first timestamp, current successful UTC last confirmation. Historical
same pair reactivates only same HIOC ID. New HA ID requires all ten 0C.1 conditions:
absent source, unique valid MAC, same unique HIOC, no competing/ambiguous/history
conflict. Source prior active else latest historical confirmation; distinct tied IDs
review only. New exact pair gets new first time. Already retired source retains its
original episode/reason/time; no rewritten retirement.

Retire unconfirmed prior active pairs by frozen precedence with safe-recreation override.
Deduplicate (HA ID,HIOC ID,parsed UTC last-confirmed), preserve existing episodes; new
episode only after later successful reactivation. History six closed fields, max 4096,
no eviction/forgotten targets. BINDING_HISTORY_CAPACITY_EXCEEDED preserves entire LKG.
Successful HIOC disappearance/MAC change retires; failed inventory never does.
Sort active HIOC/HA, history HA/HIOC/parsed instant. Validate strict cycle advancement,
chronology and every 0C.1 cross-record invariant. No identity/MAC/IP/observation/liveness/
health/incident/Asset changes.

Explicit state-schema allowlist after strong association: HIOC/HA IDs, unique_mac,
ASSOCIATED_STRONG_MAC, pair timestamps, safe observed version, contract 1.0, relationship
status; root schema 1.1/instance PI5_HA. ha_metadata only names/manufacturer/model/
hw_version/sw_version/disabled_by/reviewed via_device_id. via_device_id must resolve
in successful device response; no topology promotion. Omit unsafe optional metadata
and mark INCOMPLETE; never truncate/fabricate private IDs. No serial/unique_id/URL/raw
identifiers/connections/MAC/IP/hostname.

Entities only through entity.device_id -> strongly associated HA device. Map entity.id
to registry_id, retain entity_id/platform and permitted disabled/category metadata.
Resolve present area/config-entry refs before retention; omit dangling refs and mark
INCOMPLETE. Orphans count ENTITY_WITHOUT_DEVICE_IDENTITY, never create identity.
Deduplicate device config_entry_id/reviewed config_entries plus member-entity refs;
resolve exact entry_id/domain, permitted state/disabled_by; no title/source/options.
Direct device area_id -> resolved area_id/name candidate; no entity-area or Asset
promotion. COMPLETE means all present permitted refs resolve safely. INCOMPLETE means
supporting refs missing/dangling/unsafe in successful reads, never command/network/auth/
compatibility/structural-core failure. Disabled remains metadata, not offline evidence.

Summary exactly six schema fields, current outcomes plus historical episode count;
history adds no current association/entity total. Unique bounded diagnostic reasons/
counts, PRIOR_BINDING_RETIRED new episodes, HA_DEVICE_ID_RECREATED safe rotations.
Schema and semantic checks mandatory, not just successful MAC decisions.
The record freezes exact field-to-source mappings for every retained metadata object.
If a supporting member record cannot fit required private schema fields, omit that
member and mark the strong pair INCOMPLETE, never truncate or invent an ID.
Duplicate device/entity/entity-registry/area/config-entry keys within the respective
successful response fail REGISTRY_SCHEMA; do not choose a last record.

## Scheduler and first implementation

jazofv1 user cron, job HIOC_PE4_HA_ASSOCIATION, cadence `5,35 * * * *`, explicit
accepted interpreter, internal dedicated lock. No selected service/timer files.
First scheduled slot with valid/fresh canonical input; five-minute offset helps 0/30
inventory scheduling but never substitutes for input gate. No forced boot network.
Separate process, no PassiveNetworkDriver attachment/inventory dependency on its exit.
Retry next scheduled invocation only. Scheduler deployment NOT STARTED.

First scope: local preflight/recovery, dedicated lock/contracts/prior/inventory,
credential/auth/four reads, compatibility, structural validation/global indexes,
0C decisions/0C.1 lifecycle, private relationships/summary/diagnostics, full schema/
semantic validation, hardened publication, compatibility update, safe result.

Public projection DEFERRED: **PE-4 Home Assistant Association Public Projection**,
after private implementation and separately governed production validation. History
never associated=true. MQTT associations/dashboards/Compatibility Diagnostics UX/
HA or phone notifications/PE7-10/Asset writes/liveness/health/incidents/HA mutations/
remediation deferred.

## Results and failure model

At most 4096 bytes/16 allowlisted lines: RESULT, ERROR_CODE, FAILURE_STAGE,
COMPATIBILITY_STATUS, OBSERVED_HA_VERSION, ASSOCIATED_COUNT, REVIEW_ONLY_COUNT,
REJECTED_COUNT, UNMATCHED_COUNT, HISTORICAL_BINDING_COUNT, STATE_PUBLISHED,
LAST_KNOWN_GOOD_PRESERVED. Validated bounded counts or UNKNOWN; safe_version or
UNKNOWN; factual TRUE/FALSE/UNKNOWN on unverifiable storage. Failed-cycle counts
refer to validated prior when available, never imply candidate publication. First-run
absence distinguished from malformed prior. No household fields.

Record failure_model maps all 17 classes to preservation/credential/network/candidate/
publication possibilities. Codes <CLASS>_FAILED except BINDING_HISTORY_CAPACITY_EXCEEDED.
Initial preflight before secrets/network; inventory recheck can fail after acquisition.
Pre-commit failure preserves entire prior/absence; STATE_PUBLICATION may restore an
uncommitted replacement. UNEXPECTED_INTERNAL any stage, no exception echo.
Unverifiable recovery stops before new secrets/network, no unproved preservation TRUE.
Post-durable-commit cleanup/reporting warning retains successful state, PASS_WITH_WARNING.
RESULT=FAIL is noncommitted cycle. Log allowlist stage/result/counts/status/version/
duration/codes only; no MAC/IP/name/HA ID/entity/config-entry/area refs/raw values/token/
responses/debug frames/tracebacks.

## Upgrade, rollback and future acceptance sequence

Normal upgrade preserves state/history, validates schema, never resets on code-version
change. Older code unable to read 1.1 fails closed; no downgrade/delete/rewrite.
Credentials outside releases. Quiesce schedule before separately approved code change,
revalidate before enabling, preserve canonical inventory. Existing release scripts
alone are insufficient acceptance for new artifacts: later deployment explicitly
protects directories/state/transactions/external secret. No scripts changed now.

Sequence: credential provisioning closure; separate adapter implementation/synthetic
validation; separate PI3 deployment preparation/execution; separately authorized
bounded manual validation with schedule disabled; independent acceptance; separately
authorized schedule activation. Public projection later. No production command recipe.

Implementation tests: all 0C/0C.1 outcomes/order independence, normalization/dedup/invalid
plus valid/collision/ambiguity, reconfirm/retire/reactivate/recreate conflicts, history
idempotence/episodes/capacity, incomplete relationships, unknown fields/namespaces,
corrupt prior/input, secret failure/redaction/rotation/deletion, manual/cron lock
contention/concurrency, each transaction interruption/replace/fsync/reread/recovery
fault, byte-exact LKG, compatibility drift/auth/schema/transport, oversize/correlation/
replay/zero retries, schema/semantic/privacy checks. Synthetic memory transports and
controlled temporary POSIX fixtures, no actual credentials/HA tests.

Later production proof: pinned PI3 source/runtime and credential metadata without
content, one bounded execution, private owner/mode/schema, strong bindings/ambiguity/
history, full-map compatibility, safe logs. Compare canonical/public inventory, stable
IDs/MAC/IP/liveness/health/incidents before/after; account for unrelated scheduled
inventory generations. Prove generic integration uninvolved, public projection absent,
repeat idempotence/failure LKG under separately authorized bounded scenarios. Evidence
chooses rollback recommendation; no implicit rollback. None executed here.

Future stops: authority/source/runtime/endpoint drift, prerequisite not closed, state
migration, publication invariant unimplementable, multiple HA producers without
aggregation governance, or expanded public/identity authority. No remaining governance
contradiction prevents this architecture closure.
