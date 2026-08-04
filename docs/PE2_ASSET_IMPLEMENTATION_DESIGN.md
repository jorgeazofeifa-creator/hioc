# PE-2.1 Asset Implementation Design

Status: **COMPLETE - IMPLEMENTATION DESIGN APPROVED; EXECUTABLE IMPLEMENTED - REPOSITORY VALIDATED; PRODUCTION PENDING**

This document freezes the executable design for PE-2.1. It is subordinate to
[PE2_ASSET_FOUNDATION_SPEC.md](PE2_ASSET_FOUNDATION_SPEC.md) for product scope
and privacy authority. If implementation cannot follow this contract exactly,
it stops for a new design decision. PE-2.1 adds no daemon, cron job, public
projection, inventory dependency, MQTT, Home Assistant, dashboard, incident,
identity, canonical-address, health, liveness, topology, or service change.

## Existing implementation-pattern audit

| Repository evidence | Purpose | Reuse and adaptation |
| --- | --- | --- |
| `pi4/lib/hioc/core/state.py::StateStore` | Sorted/indented temporary JSON replace | Do not use for Asset transactions. It has a predictable `.tmp`, catches read errors, and lacks locking, fsync, closed validation, backup, ownership checks and directory fsync. Extending it risks existing callers; implement the stricter primitive once in `assets.py`. |
| `pi4/lib/hioc/core/schemas.py` | Shallow required field/type checks | Do not use for closed Asset schemas: it permits unknown fields and cannot express version, cross-field, timestamp, ID, count or normalization rules. |
| `pi4/lib/hioc/core/config.py::ConfigService` | Layered `HIOC_HOME` configuration | Reuse; no second config parser. |
| `pi4/lib/hioc/core/logging.py::EngineLogger` | Structured file logging | Reuse behind an Asset-safe facade; never pass values/raw IDs. |
| `pi4/lib/hioc/enrichment.py` | Closed PE-1 validation and deterministic envelopes | Reuse pattern, not code; Asset owns its distinct strict schemas. |
| `pi4/bin/hioc-validate-enrichment.py` and `hioc-validate-mqtt.py` | Sanitized validators, argparse, bounded summaries | Reuse CLI conventions, not subsystem-specific result codes. |
| `pi4/lib/hioc/inventory.py::stable_device_id` | Generates current `dev_` IDs | Validate format only; Asset never generates identity. |
| `pi4/bin/hioc-inventory-engine.py` | Creates inventory state and enforces `0750` | Reuse directory policy; Asset adds `0600` files and `0700` backup directory. |
| `pi4/install_pi4.sh` | Installation, executable modes, runtime directories, cron | Modify minimally for Asset files/directories; add no job. |
| `pi4/validate_pi4.sh` | Runtime presence/schema checks | If either Asset artifact exists, require the pair and run the read-only validator; never initialize or refresh. |
| `release/upgrade.sh`, `release/rollback.sh` | Preserve `state` and `backups` | Reuse unchanged unless preservation tests fail. Release rollback is not Asset restore. |
| `tests/test_release.py`, PE-1 tests and Evidence Reports | Synthetic fixtures and governed proof | Reuse isolation/evidence patterns; no network, root or production metadata. |

The duplication risk is explicit: Asset must not create another config reader,
logger, stable-ID generator or release copier, but the current shared StateStore
is not safe enough for durable private operator state and must not be silently
strengthened for unrelated callers.

## Execution model and call graph

PE-2.1 runs only through the operator CLI, read-only Asset validator, or existing
release/runtime validation invoking that validator. There is no automatic Asset
mutation, scheduled job or daemon.

```text
pi4/bin/hioc-assets.py -> AssetCli -> AssetService -> AssetStore
                                              |-> assets.json
                                              |-> assets_status.json
                                              `-> backups/assets/
pi4/bin/hioc-validate-assets.py -> validation functions (read-only)
pi4/validate_pi4.sh -> hioc-validate-assets.py only when artifacts exist
```

Status is written by initialize, successful/no-op mutations, validate, backup
and restore. List/show and standalone/release/runtime validation never write.
Asset reads inventory only for orphan context. Inventory imports no Asset code,
reads no Asset file and remains independent of malformed Asset state.

## Inventory interaction decision

Model **A** is authoritative. Asset reads
`$HIOC_HOME/state/inventory/inventory.json` only during Asset validation/orphan
calculation. A usable snapshot is an object with a `devices` list and valid IDs
for entries used. Other public fields are ignored; age is diagnostic, not a
validity gate. Missing/unreadable/malformed inventory makes orphan count null,
status degraded and list/show orphan state unknown. Existing records remain
editable; creation requires `--allow-orphan`. Asset state never affects identity,
canonical IP, public inventory, health, liveness, incidents, topology, service
ownership or inventory success.

## Modules and exact API

New executable files are limited to:

- `pi4/lib/hioc/assets.py`: constants, normalization, closed validation,
  deterministic serialization, locks, permissions, reads, atomic replacement,
  backup/restore, status and orphan calculation.
- `pi4/bin/hioc-assets.py`: `AssetCli` and
  `main(argv: list[str] | None = None) -> int`; parsing/presentation only.
- `pi4/bin/hioc-validate-assets.py`: read-only paired validator and matching
  `main` signature.

`assets.py` defines constants `SCHEMA_VERSION`, `GENERATOR`, `STORE_KEYS`,
`RECORD_KEYS`, `STATUS_KEYS`, `STATUS_VALUES`, `ERROR_CODES`, `FIELD_LIMITS`;
exceptions `AssetError(code, message)`, `AssetUsageError`,
`AssetValidationError`, `AssetNotFoundError`, `AssetRevisionConflict`,
`AssetLockTimeout`, `AssetBackupError`, `AssetWriteError`, `AssetRestoreError`,
`AssetPrivacyError`; pure functions `utc_now(clock=datetime.now) -> str`,
`normalize_field(field, value) -> str | None`, `validate_stable_id(value) -> str`,
`validate_store(value) -> dict`, `validate_status(value) -> dict`,
`serialize_store(value) -> bytes`, `redacted_id(value) -> str` (first 12 SHA-256
hex), and `calculate_orphans(store, inventory) -> set[str]`.

`AssetLock(path, shared, timeout=5.0)` is a non-reentrant context manager using
`fcntl.flock`. `AssetStore(home, clock)` owns paths, strict loads, modes,
ownership, atomic writes, backup/restore and status. `AssetService(store)` exposes
`initialize`, `list_assets`, `show_asset`, `set_fields`, `clear_field`, `remove`,
`validate`, `backup`, `restore`, returning sanitized dictionaries and never
printing. Service mutations own one exclusive lock; reads one shared lock.

## CLI command contract

Global `--json` precedes the command. Exact surface:

```text
hioc-assets.py [--json] initialize
hioc-assets.py [--json] list
hioc-assets.py [--json] show --device-id ID [--show-sensitive]
hioc-assets.py [--json] set --device-id ID [--friendly-name VALUE]
  [--physical-location VALUE] [--purpose VALUE] [--notes VALUE]
  [--allow-orphan] [--expected-revision N]
hioc-assets.py [--json] clear-field --device-id ID --field
  {friendly_name,physical_location,purpose,notes} --expected-revision N
hioc-assets.py [--json] remove --device-id ID --expected-revision N
hioc-assets.py [--json] validate
hioc-assets.py [--json] backup
hioc-assets.py [--json] restore --backup BASENAME
```

Set requires a field. Creation omits expected revision; an existing-record update
requires it. Clear/remove require it. Allow-orphan applies only to creation when
inventory cannot prove existence. Clearing the final populated field removes.
Initialize is idempotent. Normalized no-ops return success without changing
timestamp, revision, backup or store bytes.

## Output and exit-code contract

Human output is concise and value-free. JSON emits exactly one object plus LF:

```json
{"schema_version":"1.0","command":"set","result":"updated","status":"online","redacted":true,"data":{},"error":null}
```

Keys are always present in that order. Initialize data: `asset_count`,
`initialized`. List: counts, inventory context, and records containing only ID
digest, revision, populated field names, orphan state and timestamps. Show adds
values only under authorized sensitive display. Mutations: ID digest, revision
(null after removal), changed fields and backup (null for no-op). Validate:
counts/context/invariant booleans. Backup: count/basename. Restore:
count/source/pre-restore basenames. Errors have empty data and only bounded
sanitized code/message. Results are `initialized`, `already_initialized`,
`listed`, `shown`, `created`, `updated`, `removed`, `no_change`, `valid`,
`backed_up`, `restored`, `error`. No stack trace.

| Exit | Meaning | Required handling |
| --- | --- | --- |
| 0 | success/no-op | no rollback |
| 2 | usage/privacy refusal | correct invocation |
| 3 | invalid ID/field/content | correct data/investigate |
| 4 | record/backup not found | correct target |
| 5 | revision conflict | re-read/retry |
| 6 | five-second lock timeout | retry safely |
| 7 | backup creation/validation failure | store unchanged; investigate |
| 8 | store/status write or permission failure | inspect documented partial outcome |
| 9 | restore rejection/failure | current store normally unchanged |
| 10 | malformed current store | explicit recovery |
| 11 | unsupported schema | migration authorization |
| 12 | unavailable inventory when proof required | restore context or allow orphan |
| 13 | ownership/mode/path/symlink/privacy failure | correct security boundary |
| 70 | unexpected implementation failure | investigate; sanitize output |

Operator/input/concurrency failures never recommend rollback. Rollback is only
for the frozen production criteria below.

## Asset and status schema freeze

The store is exactly foundation version 1.0. Top-level order:
`schema_version`, `updated_at`, `asset_count`, `assets`. Record order:
`stable_device_id`, `friendly_name`, `physical_location`, `purpose`, `notes`,
`created_at`, `updated_at`, `update_source`, `revision`. Version is string
`"1.0"`; timestamps are RFC 3339 UTC with six fractional digits and `Z`. JSON
is UTF-8, two-space indented, deterministic and LF-terminated; assets sort
lexically. IDs match key and `^dev_[0-9a-f]{16}$`. Unknown/missing fields and
future versions fail. Revisions start at 1 and increment once per content change.
All four operator fields exist as string/null and at least one is non-null.

Status keys, in order: `schema_version`, `updated`, `status`, `asset_count`,
`orphaned_asset_count`, `invalid_record_count`, `generator`, `error_code`,
`error_message`; all required. Error message is null on success or sanitized,
maximum 160 code points. Status is online/degraded/error/unavailable. Orphan
count is integer with valid inventory, else null. Missing store is unavailable;
valid store plus bad/missing inventory degraded; malformed/unsupported store
error. A status-write failure never rolls back valid Asset content.

## Field normalization freeze

All text is Unicode NFC and limits count normalized code points. Friendly name
and physical location max 128; purpose max **256**. These trim outer Unicode
whitespace, reject tabs, controls and line separators, preserve case/internal
printable spacing, and become null when empty. Duplicate names are allowed;
location has no hierarchy parsing.

Notes normalize CRLF/CR to LF, remove trailing whitespace per line, trim outer
blank/whitespace-only lines, permit internal blank lines, reject tabs/controls
except LF, and become null when empty. Maximum is 1,024 code points/eight lines.
Notes are inert plain text, never Markdown, HTML, template or command input.

## Mutation and read transactions

Mutation order is fixed: parse; ID/options validation; normalization; exclusive
lock; path ownership/mode enforcement; strict current load or canonical empty
initial state; inventory context; revision check; no-op detection; new in-memory
store and validation; validated pre-mutation backup; unique same-directory temp;
flush/fsync; chmod `0600`; temp re-read/validation; `os.replace`; parent fsync;
sanitized status atomic write; unlock; result.

No-op has no backup/store write/revision/timestamp change, but may refresh status.
Initialization backs up canonical empty store even if no prior file. Backup
failure leaves store unchanged. Replace failure retains backup and old store when
replace did not occur. Parent-fsync failure after replace returns 8 and preserves
backup; do not guess durability or auto-restore. Status failure after content
replace leaves content committed, returns 8/`STATUS_WRITE_FAILED`, and does not
auto-rollback. Restore uses the same transaction and first backs up current
state. Handled failures remove only the verified transaction temp.

List/show acquire shared lock, validate and never refresh status. Validate first
reads under shared lock, then separately takes exclusive lock only to write
status; it never changes store. Missing: list is empty/uninitialized, show exit
4, validate writes unavailable and exits 3. Malformed store exits 10.

## Lock and revision model

Lock path `/tmp/hioc-assets.lock`, mode `0600`, runtime-user owned, opened without
following symlinks. Shared/exclusive nonblocking `flock` polls to a hard five
seconds. Kernel ownership means a leftover file is harmless and never deleted as
stale; crash releases lock. Locks are non-reentrant/nonnested. Asset never takes
inventory/enrichment locks; ordering is only Asset lock then Asset-local
backup/status operations.

Creation revision 1; each successful content mutation +1; no-op unchanged.
Existing update/clear/remove require expected revision. Restore preserves record
revisions/timestamps and changes only top-level transaction time. Import and
migration are absent.

## Backup, restore and initialization

Backup root `$HIOC_HOME/backups/assets`, directory `0700`, files `0600`, expected
production owner `jazofv1:jazofv1`. Name:
`assets-YYYYMMDDTHHMMSSffffffZ-<12-lowercase-SHA256>.json`; digest covers exact
bytes. Collision is accepted only for identical bytes, otherwise fails without
overwrite. Backups are exact source bytes; first initialization backs up
canonical empty-store bytes. Unique temp, fsync, mode, replace, parent fsync,
re-read, digest and schema validation are required. No sidecar/pruning.

Restore accepts a matching basename only. Reject separators, traversal,
symlinks, non-regular/out-of-root files, bad digest/name, unsafe ownership/mode,
invalid schema/ID/field/version. Validate candidate before creating pre-restore
backup; under exclusive lock atomically restore semantic content with new
top-level transaction time and status. Failure before replace leaves current
state. Post-replace failure follows the partial-outcome rules. No arbitrary path.

Missing store is empty but uninitialized for list. Initialize creates empty
store/status and is idempotent. Set may initialize atomically, using canonical
empty backup. List/show/standalone validator never create status.

## Orphan, error, logging and privacy contract

Orphan means Asset ID absent from valid current inventory. Orphans remain valid,
editable/restorable, never auto-deleted/published/unhealthy/incidents. Missing or
malformed inventory yields unknown/null/degraded and needs allow-orphan to create.

Closed error codes: `STORE_MISSING`, `STORE_INVALID_JSON`,
`STORE_SCHEMA_INVALID`, `STORE_UNSUPPORTED_VERSION`, `STORE_PERMISSION_ERROR`,
`LOCK_TIMEOUT`, `INVALID_STABLE_ID`, `INVALID_FIELD`, `NOT_FOUND`,
`REVISION_CONFLICT`, `INVENTORY_UNAVAILABLE`, `INVENTORY_INVALID`,
`BACKUP_FAILED`, `BACKUP_INVALID`, `WRITE_FAILED`, `STATUS_WRITE_FAILED`,
`RESTORE_REJECTED`, `RESTORE_INVALID`, `PRIVACY_REFUSED`, `INTERNAL_ERROR`.
Status uses only subsystem/store/inventory/transaction codes; syntax/not-found/
revision/privacy appear only in CLI/evidence. Messages exclude values, raw IDs,
arbitrary paths and exceptions.

Logs allow command, result, counts, duration, revision, changed field names,
backup basename, error code and 12-hex ID digest. Values/raw IDs/bytes are banned.
Default list/show redact. Sensitive display requires local interactive TTY,
refuses `--json` or redirection, warns on stderr and requires typing `SHOW` on
the controlling terminal. It never changes logging and production validation
must not use it. No remote/public mode exists.

## Failure taxonomy

| Domain/examples | State outcome | Retry/action | Rollback |
| --- | --- | --- | --- |
| Wrong host/repository/artifact | no transaction | stop/correct governance | deployed artifact mismatch: yes |
| Syntax, ID/field, not-found, privacy refusal | unchanged/no backup | correct input | no |
| Lock timeout/revision conflict | unchanged/no backup | re-read/retry | no |
| Missing/malformed/future store | unchanged; sanitized status when possible | initialize or explicit recovery/migration | only deployment-caused corruption |
| Missing/malformed/stale inventory | degraded; explicit mutation rules | restore context/allow orphan | no |
| Backup permission/write/fsync/validation/disk full | unchanged | repair/retry | yes if required production invariant cannot pass |
| Temp/fsync/replace/parent-fsync/disk/permission | backup retained; old or explicitly uncertain committed state | inspect hashes/status before retry | yes for deterministic corruption |
| Status failure after replace | content committed, status stale | validate/repair/refresh | not alone |
| Traversal/symlink/arbitrary restore/digest/schema | unchanged | choose governed backup | no; actual disclosure yes |
| Crash after backup / after replace-before-status | kernel unlock; backup persists; old/new valid store depending boundary | validate hashes, refresh | only corruption/invariant failure |
| Public/identity/canonical/MQTT/HA/dashboard/incident/topology/service regression | prohibited implementation failure | stop | yes |

## Production validation and synthetic record

A later authorization provides the command. Frozen phases: A target/clean
approved source; B privacy-safe pre-evidence; C Git blob/SHA-256 identity; D
supported deployment/release backup; E installed modes, paired validation and
timings; F synthetic transaction; G protected inventory/consumer invariants; H
backup/restore; I invalid write/revision/restore rejection without byte change;
J cleanup; K final semantic equality; L Evidence Report.

Reserved synthetic orphan: `dev_0000000000000000`, only after proving absence
from inventory/store. Values: friendly name `HIOC PE2 Validation Asset`, physical
location `Validation Lab`, purpose `Governed production validation`, notes
`Synthetic temporary record for PE-2.1 validation.` No real device is used. If
reserved ID exists, PARTIAL PASS with no synthetic mutation; no invented fallback.

Capture pre-test bytes/SHA-256 and semantic digest excluding only top-level
transaction time. Initialize if needed; create; validate; update purpose; clear
location; reject stale revision; backup; restore; remove; validate; compare final
semantic content. Delete only the exact recorded synthetic-sequence backups after
equality. Cleanup failure is PARTIAL PASS and records basename/count, not content;
pre-existing backups remain untouched.

Evidence permits commit/blob/hash, counts, modes, durations, 12-hex ID digest,
field names, revisions, backup basenames, error codes, invariant booleans and
PASS/PARTIAL PASS/FAIL. It prohibits values, real IDs/hostnames/MAC/IP, raw store
and backup contents. PASS requires deterministic/protected invariants. PARTIAL
PASS is limited to reserved-ID collision, optional observation unavailable, or
synthetic-backup cleanup failure with state/protected invariants intact. FAIL is
artifact/schema/transaction/backup/restore/privacy/performance/protected-contract
failure. Rollback only for deployed mismatch, corruption, required backup/restore
failure, privacy exposure, protected regression or inventory-affecting runtime.

## Performance, schema evolution and release integration

Up to 1,000 Assets on PI3-class hardware: list/show <=1s, mutation <=3s excluding
lock, backup <=2s, validation <=2s, lock wait <=5s, inventory impact zero. One
target exceedance warns; repeat above 2x is PARTIAL PASS if correct; >10s or any
inventory regression is FAIL. Performance is rollback-worthy only if repeatable,
deployment-attributable and operationally blocking.

Version 1.0 rejects unknown/future versions without rewrite/downgrade/migration.
Read-only validation reports unsupported version. Future migration requires new
contract, validated backup, explicit command/tests/evidence/rollback.

Implementation changes `pi4/install_pi4.sh` only for restrictive directories,
preservation and executable bits; no overwrite/job. PE-2.1 artifact modes are
owned by `pi4/config/pe2_artifacts.json`, which distinguishes Git mode, runtime
mode, executability, ownership and privacy. Runtime validator checks a
paired store/status only when either exists. Existing release exclusions already
preserve state/backups; tests must prove install/upgrade/rollback byte identity.
If they fail, reopen design before changing release scripts.

## Test plan and implementation file plan

New tests: `tests/test_assets_schema.py` (schemas, normalization, ordering,
timestamps, deterministic bytes), `tests/test_assets_store.py` (reads, locks,
atomic failure, modes, backup/restore, revisions/crashes),
`tests/test_assets_cli.py` (commands, envelopes, exits, redaction/TTY),
`tests/test_assets_orphans.py` (inventory states/isolation), and
`tests/test_assets_release.py` (install/upgrade/rollback preservation and source
guards). Use temp roots, synthetic values, injected UTC clock, mocked failures,
no network/root/production metadata.

Foundation cases 1-22/51-52 map to schema/normalization; 23-34 to store/lock/
backup/restore; 35-45/53 to protected guards/full regression; 46-48 to status/
orphans; 49-50 to CLI privacy/fixtures, plus every command-specific case.

Approved new files: the three executable files, five test files and
`docs/PE2_ASSET_FOUNDATION_EVIDENCE.md`. Approved modifications:
`pi4/install_pi4.sh`, `pi4/validate_pi4.sh`, documentation, and release scripts
only under the stop condition. Prohibited: inventory/enrichment, MQTT, HA,
dashboard, incident, topology, service modules and public schemas.

## Copy-ready implementation prompt

> Implement the approved PE-2.1 design exactly from
> `docs/PE2_ASSET_IMPLEMENTATION_DESIGN.md` and
> `docs/PE2_ASSET_FOUNDATION_SPEC.md`. Create only the approved Asset module,
> CLI, read-only validator, five test modules and evidence skeleton; make only
> approved installer/runtime-validator/documentation changes. Implement the
> named APIs, exact CLI, schemas, normalization, envelopes, exit/error codes,
> five-second dedicated flock, revision, atomic/fsync transaction, validated
> backup/restore, initialization/orphan/privacy/logging contracts and tests. Add
> no cron, daemon or public/runtime integration. Do not change inventory,
> enrichment, identity, canonical address, current names, MQTT, HA, dashboards,
> incidents, health, liveness, topology or service ownership. Run focused Asset,
> release preservation and full regression tests plus links/contracts/privacy/
> secrets/`git diff --check`/complete diff review. Create the evidence document,
> keep production unchanged, and commit locally as
> `Phase 7A: implement PE-2 asset foundation`. Do not push, deploy, access
> PI3/PI5, produce PI3 commands or begin PE-2.2. Reopen design if prohibited
> behavior is required.

## Checkpoint boundary

PE-2.0 is **COMPLETE - DESIGN APPROVED**. PE-2.1 Implementation Design Review is
**COMPLETE - IMPLEMENTATION DESIGN APPROVED**. PE-2.1 executable implementation
is **IMPLEMENTED - REPOSITORY VALIDATED**. Production remains unchanged; its
deployment and validation are pending separate explicit authorization.
