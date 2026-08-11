# PE-3.1 Manufacturer Enrichment Executable Contract

Status: **COMPLETE — EXECUTABLE CONTRACT FROZEN; IMPLEMENTATION NOT STARTED**

This is the single normative executable contract for PE-3.1. It refines the
architecture in [PE3_MANUFACTURER_ENRICHMENT_SPEC.md](PE3_MANUFACTURER_ENRICHMENT_SPEC.md)
and supersedes conflicting implementation details in
[PE3_MANUFACTURER_IMPLEMENTATION_DESIGN.md](PE3_MANUFACTURER_IMPLEMENTATION_DESIGN.md).
Every name, schema, path, command, result, error, transaction, and boundary below
is binding. Examples are explicitly non-normative and use synthetic values.

## 1. Execution model

PE-3.1 uses **Model B: a separate bounded local command**. The executable is
`pi4/bin/hioc-generate-manufacturer.py`. It reads the completed private
`state/inventory/inventory.json`, a locally generated normalized database, and
its adjacent manifest. It writes only `state/inventory/manufacturer.json` and
`state/inventory/manufacturer_status.json`.

The command is manually invoked in PE-3.1. No inventory-engine hook, caller,
cron entry, timer, daemon, service, automatic update, or download exists.
`inventory.py`, `enrichment.py`, the inventory engine, PE-1, and PE-2 never call
it. Future orchestration requires a separately approved checkpoint.

## 2. Exact future file set

Executable implementation creates exactly:

- `pi4/lib/hioc/manufacturer.py`
- `pi4/bin/hioc-build-manufacturer-db.py`
- `pi4/bin/hioc-validate-manufacturer.py`
- `pi4/bin/hioc-generate-manufacturer.py`
- `tests/test_manufacturer_schema.py`
- `tests/test_manufacturer_lookup.py`
- `tests/test_manufacturer_builder.py`
- `tests/test_manufacturer_cli.py`
- `tests/test_manufacturer_sidecar.py`
- `tests/test_manufacturer_release.py`
- `tests/test_manufacturer_governance.py`
- `docs/PE3_MANUFACTURER_ENRICHMENT_EVIDENCE.md`

It may modify only `pi4/install_pi4.sh`, `pi4/validate_pi4.sh`,
`release/install.sh`, `release/upgrade.sh`, `release/rollback.sh`,
`pi4/config/hioc.conf.example`, `.gitignore`, and PE-3/governance documentation.
It must not modify `pi4/lib/hioc/inventory.py`,
`pi4/lib/hioc/enrichment.py`, PE-2 code, MQTT, Home Assistant, dashboards,
incidents, topology, dependencies, or service ownership.

## 3. Module constants and immutable structures

`pi4/lib/hioc/manufacturer.py` exports these exact constants:

```python
MANUFACTURER_DB_SCHEMA_VERSION = "1.0"
MANUFACTURER_MANIFEST_SCHEMA_VERSION = "1.0"
MANUFACTURER_SIDECAR_SCHEMA_VERSION = "1.0"
MANUFACTURER_STATUS_SCHEMA_VERSION = "1.0"
MANUFACTURER_GENERATOR_VERSION = "hioc-manufacturer-1"
ASSIGNMENT_CLASSES = frozenset({"MA-L", "MA-M", "MA-S"})
LOOKUP_STATUSES = frozenset({"matched", "unknown_prefix", "invalid_address",
    "multicast_address", "locally_administered_address", "missing_address",
    "unsupported_address_type"})
MANUFACTURER_CONFIDENCES = frozenset({"high", "unknown"})
MANUFACTURER_STATUS_VALUES = frozenset({"online", "degraded", "unavailable", "error"})
```

It exports frozen dataclasses `ManufacturerRecord`, `ManufacturerManifest`,
`ManufacturerDatabase`, and `ManufacturerLookupResult`. Dataclass fields are:

```python
ManufacturerRecord(prefix: str, prefix_length: int,
                   assignment_class: str, organization: str)
ManufacturerManifest(document: dict, database_sha256: str,
                     database_semantic_sha256: str)
ManufacturerDatabase(document: dict, manifest: ManufacturerManifest,
                     ma_l: MappingProxyType, ma_m: MappingProxyType,
                     ma_s: MappingProxyType)
ManufacturerLookupResult(lookup_status: str, manufacturer: str | None,
                         confidence: str, assignment_class: str | None,
                         matched_prefix: str | None,
                         matched_prefix_length: int | None,
                         lookup_method: str)
```

`ManufacturerSidecar` and `ManufacturerStatus` are type aliases for validated
plain `dict` objects because repository sidecars use closed ordered dictionaries.
All returned structures are new objects; public functions never mutate inputs.

## 4. Exact public functions

The module exports only these PE-3 public functions in addition to the constants,
dataclasses, and exceptions:

```python
normalize_eui48(value: str) -> str
normalize_eui64(value: str) -> str
is_multicast_address(normalized: str) -> bool
is_locally_administered_address(normalized: str) -> bool
normalize_organization(value: str) -> str
validate_database(document: object) -> dict
validate_manifest(document: object) -> dict
validate_manufacturer_sidecar(document: object) -> dict
validate_manufacturer_status(document: object) -> dict
load_database(database_path: pathlib.Path,
              manifest_path: pathlib.Path) -> ManufacturerDatabase
lookup_manufacturer_eui48(database: ManufacturerDatabase,
                         mac: str) -> ManufacturerLookupResult
lookup_manufacturer_eui64(database: ManufacturerDatabase,
                         eui64: str) -> ManufacturerLookupResult
build_manufacturer_sidecar(inventory_document: dict,
                           database: ManufacturerDatabase,
                           *, generated_at: str) -> tuple[dict, dict]
canonical_json_bytes(document: object) -> bytes
semantic_sha256(document: object) -> str
file_sha256(path: pathlib.Path) -> str
write_json_atomic(path: pathlib.Path, document: object,
                  *, mode: int) -> None
```

Normalizers accept strings only and raise `ManufacturerInputError` otherwise.
Validators return deep-copied validated documents and perform no I/O.
`load_database` performs local file, permission, closed-schema, complete-file
checksum, semantic checksum, count, ordering, and manifest coherence checks,
then creates immutable maps. Lookup performs no I/O. Sidecar construction reads
only its arguments and returns `(sidecar, status)`. Hash functions are pure
except `file_sha256`, which reads one local regular file without following a
symlink. `write_json_atomic` is the only library writer; it validates the parent,
writes canonical presentation JSON, fsyncs, applies the requested mode, replaces,
fsyncs the directory, and never logs document values.

Function ownership and failures are exact:

| Function | Failure classes | Test owner |
| --- | --- | --- |
| `normalize_eui48`, `normalize_eui64` | `ManufacturerInputError` | lookup |
| address-class predicates | input error for noncanonical input | lookup |
| `normalize_organization` | `ManufacturerInputError` | builder |
| four validators | `ManufacturerValidationError` | schema |
| `load_database` | unavailable, validation, integrity, or permission error | schema/validator |
| two lookup functions | wrong API type raises input error; malformed text returns `invalid_address` | lookup |
| `build_manufacturer_sidecar` | validation error for inventory/timestamp; exclusions return records | sidecar |
| canonical JSON and semantic hash | validation error for unsupported JSON values | schema/builder |
| `file_sha256` | unavailable or permission error | builder/validator |
| `write_json_atomic` | write or privacy error | sidecar |

No function logs. Pure functions perform no I/O, time access, environment access,
or mutation. Test-owner names refer to the exact modules in section 25.

## 5. Exception contract

The smallest binding hierarchy is:

```python
ManufacturerError(Exception)                 # base; code, safe_message, exit_code
ManufacturerInputError(ManufacturerError)    # invalid CLI/domain input
ManufacturerValidationError(ManufacturerError) # schema/version/content
ManufacturerUnavailableError(ManufacturerError) # required local file unavailable
ManufacturerIntegrityError(ManufacturerError) # checksum/semantic/determinism/conflict
ManufacturerLockError(ManufacturerError)     # lock timeout
ManufacturerWriteError(ManufacturerError)    # permission or atomic write
ManufacturerPrivacyError(ManufacturerError)  # prohibited disclosure/output
```

Each constructor is `(code: str, message: str)`. The base collapses whitespace,
removes path components to basenames, and limits `safe_message` to 160 Unicode
characters. Unknown codes become `MANUFACTURER_INTERNAL_ERROR`. Exceptions are
public for CLI mapping and tests. A retry may succeed for unavailable, lock, and
write failures. Inventory is always unaffected. Repository exceptions alone
never recommend production rollback.

Default subclass exit codes are: input 3, validation 6, unavailable 4,
integrity 7, lock 17, write 12, and privacy 18. A specific error code overrides
the default only for semantic mismatch 8, unsupported version 9,
`MANUFACTURER_DATASET_CONFLICT` 10, `MANUFACTURER_DETERMINISM_FAILED` 11,
inventory 14, `MANUFACTURER_SIDECAR_INVALID` 15,
`MANUFACTURER_STATUS_INVALID` and `MANUFACTURER_STATUS_WRITE_FAILED` 16,
permission 5, and unexpected internal failure 70. `ManufacturerError` owns this
single mapping for every CLI. The constructor remains exactly `(code, message)`;
these four explicit codes are first-class members of `MANUFACTURER_ERROR_CODES`
and never collapse to `MANUFACTURER_INTERNAL_ERROR`.

## 6. Normalized database closed schema

`manufacturer-db.json` is an ordered object with exactly:

```json
{
  "schema_version": "1.0",
  "dataset_id": "local-ieee-ra",
  "dataset_version": "2026-08-04-r1",
  "parser_version": "hioc-manufacturer-1",
  "semantic_sha256": "<64 lowercase hex>",
  "record_count": 3,
  "ma_l_count": 1,
  "ma_m_count": 1,
  "ma_s_count": 1,
  "conflict_count": 0,
  "records": {}
}
```

The values above are non-normative synthetic examples. `dataset_id` matches
`^[a-z0-9][a-z0-9._-]{0,63}$`; `dataset_version` matches
`^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$`; parser version is exactly the generator
version. Counts are nonnegative JSON integers, never booleans. A successful
database is nonempty, `conflict_count` is zero, and class counts sum to
`record_count`.

`records` is a mapping ordered lexically by key. The exact key is
`<prefix_length>:<uppercase_hex_prefix>`, for example the non-normative synthetic
keys `24:A1B2C3`, `28:A1B2C3D`, and `36:A1B2C3D4E`. Each value has exactly, in
order, `prefix`, `prefix_length`, `assignment_class`, `organization`. Prefix
length/class pairs are 24/`MA-L`, 28/`MA-M`, and 36/`MA-S`; prefix widths are
6, 7, and 9 uppercase hexadecimal digits. Key and fields must agree.

The semantic payload is the database object with `semantic_sha256` omitted,
preserving the specified field and record-key order. `semantic_sha256` is the
lowercase SHA-256 of `canonical_json_bytes(payload)`. Runtime builds immutable
`ma_l`, `ma_m`, and `ma_s` maps. Unknown fields, wrong order, empty data,
duplicate keys, invalid types, noncanonical values, and unsupported versions
are rejected.

Canonical JSON is UTF-8, `ensure_ascii=False`, NFC strings, two-space indentation,
`, ` and `: ` separators, exact insertion order, and one LF final newline. CRLF
is never emitted. File bytes are reproducible across locale, timezone, Windows,
and Linux.

## 7. Adjacent manifest closed schema

The filename is exactly `manufacturer-db.manifest.json`. It is an ordered object
with exactly:

```json
{
  "schema_version": "1.0",
  "database_filename": "manufacturer-db.json",
  "database_sha256": "<64 lowercase hex>",
  "database_size_bytes": 0,
  "database_semantic_sha256": "<64 lowercase hex>",
  "database_schema_version": "1.0",
  "dataset_id": "local-ieee-ra",
  "dataset_version": "2026-08-04-r1",
  "parser_version": "hioc-manufacturer-1",
  "record_count": 0,
  "ma_l_count": 0,
  "ma_m_count": 0,
  "ma_s_count": 0,
  "duplicate_count": 0,
  "conflict_count": 0,
  "source_files": [],
  "build": {
    "canonicalization_version": "1",
    "deterministic_build_verified": true
  }
}
```

All three source classes are mandatory and `source_files` contains exactly three
objects sorted `MA-L`, `MA-M`, `MA-S`. Each object has exactly
`source_class`, `source_filename`, `source_sha256`, `source_size_bytes`.
Filenames are nonempty basenames only; absolute paths, path separators, URLs,
hostnames, usernames, timestamps, environment details, notes, and organization
values are prohibited. SHA values are lowercase 64-hex strings; sizes are
positive integers. Database counts/digests/identity must equal the database.
`database_size_bytes` is the exact complete-file size. Unknown fields and wrong
ordering are rejected. The manifest is deterministic canonical JSON, mode 0600.
License approval belongs in repository governance, not the runtime manifest.
No separate build receipt exists.

## 8. Builder CLI

Exact command:

```text
hioc-build-manufacturer-db.py --ma-l PATH --ma-m PATH --ma-s PATH
  --ma-l-sha256 HEX --ma-m-sha256 HEX --ma-s-sha256 HEX
  --dataset-id ID --dataset-version VERSION --output-directory DIR
  [--json]
```

All arguments except `--json` are required. All three sources are regular,
readable, nonsymlink files outside the output directory. SHA arguments are
required and verified before parsing. `DIR` is an absolute, nonexistent path;
its parent must exist, be writable, and not be a symlink. The builder creates
the version directory atomically with mode 0700 containing exactly the database
and manifest at mode 0600. Existing output is an input error; there is no
`--replace`, download, URL, dry-run, validate-only, or alternate-output flag.

The deterministic second in-memory build is mandatory. Human success output is
`manufacturer database build passed | records=N | duplicate_count=N`; failures
print only `manufacturer database build failed | error=CODE` to stderr. `--json`
emits one compact object with exactly `schema_version`, `result`, `record_count`,
`ma_l_count`, `ma_m_count`, `ma_s_count`, `duplicate_count`, `conflict_count`,
`database_sha256`, `database_semantic_sha256`, `error`; `error` is null on PASS
or `{code,message}` on FAIL. It never prints organizations, prefixes, rows, or
source paths.

## 9. Validator CLI

Exact commands:

```text
hioc-validate-manufacturer.py database --database PATH --manifest PATH [--json]
hioc-validate-manufacturer.py sidecar --sidecar PATH --status PATH
  [--inventory PATH] [--database PATH --manifest PATH] [--json]
```

`database` requires both paths. `sidecar` requires sidecar/status; inventory is
optional for ID/count equality. Database and manifest are jointly optional for
sidecar validation but must appear together. It verifies regular nonsymlink
files, modes no broader than 0600 on POSIX, parent modes no broader than 0750,
no `.manufacturer*.tmp` siblings, schemas, ordering, counts, hashes, and
coherence. It performs no writes, repair, chmod, timestamp update, or lock-file
mutation. It obtains a shared database lock only when database files are read.

Human output is `manufacturer validation passed | target=database|sidecar` or a
sanitized failure. JSON contains exactly `schema_version`, `result`, `target`,
`status`, `record_count`, `matched_count`, `privacy_safe`, `error`, using nulls
when not applicable.

## 10. Generator CLI

Exact command:

```text
hioc-generate-manufacturer.py [--home DIR] [--inventory PATH]
  [--database PATH] [--manifest PATH] [--output-sidecar PATH]
  [--output-status PATH] [--json]
```

`--home` defaults to `HIOC_HOME`, then `/home/jazofv1/hioc`. Inventory defaults
to `<home>/state/inventory/inventory.json`; outputs default to the two frozen
state paths. Database defaults to `MANUFACTURER_DB_PATH` from
`<home>/config/hioc.conf`; CLI overrides configuration. Manifest defaults to
the fixed sibling `manufacturer-db.manifest.json`. Explicit paths must be
absolute. The command never alters inventory and uses the generation transaction
in section 18.

Human success output is `manufacturer generation passed | records=N | matched=N`.
JSON contains exactly `schema_version`, `result`, `status`, `record_count`,
`matched_count`, `unknown_count`, `excluded_count`, `invalid_count`, `error`.
No raw values are emitted.

## 11. Shared process exit codes

| Code | Meaning | Tools |
| ---: | --- | --- |
| 0 | success, including semantic no-op | all |
| 2 | CLI usage | all |
| 3 | invalid domain input/path relationship | all |
| 4 | required file unavailable or not configured | all |
| 5 | permission/ownership/mode refusal | all |
| 6 | closed-schema/content validation failure | all |
| 7 | complete-file/source checksum mismatch | builder, validator, generator |
| 8 | semantic digest mismatch | validator, generator |
| 9 | unsupported schema/parser version | all |
| 10 | conflicting normalized dataset record | builder |
| 11 | deterministic second-build mismatch | builder |
| 12 | atomic write/transaction failure | builder, generator |
| 14 | inventory missing or invalid | validator sidecar, generator |
| 15 | sidecar validation failure | validator, generator |
| 16 | status validation/write failure | validator, generator |
| 17 | lock timeout | all when a database/generation lock is required |
| 18 | privacy-policy refusal | all |
| 70 | sanitized unexpected internal error | all |

Exit code 1 and 13 are unused. CLI errors alone never imply rollback.

## 12. Status error codes

`MANUFACTURER_ERROR_CODES` is exactly:

```text
MANUFACTURER_NOT_CONFIGURED
MANUFACTURER_DATABASE_MISSING
MANUFACTURER_MANIFEST_MISSING
MANUFACTURER_DATABASE_UNREADABLE
MANUFACTURER_MANIFEST_UNREADABLE
MANUFACTURER_DATABASE_SCHEMA_INVALID
MANUFACTURER_MANIFEST_SCHEMA_INVALID
MANUFACTURER_DATABASE_CHECKSUM_MISMATCH
MANUFACTURER_DATABASE_SEMANTIC_MISMATCH
MANUFACTURER_VERSION_UNSUPPORTED
MANUFACTURER_DATASET_EMPTY
MANUFACTURER_DATASET_CONFLICT
MANUFACTURER_DETERMINISM_FAILED
MANUFACTURER_INVENTORY_MISSING
MANUFACTURER_INVENTORY_INVALID
MANUFACTURER_LOCK_TIMEOUT
MANUFACTURER_SIDECAR_INVALID
MANUFACTURER_SIDECAR_WRITE_FAILED
MANUFACTURER_STATUS_INVALID
MANUFACTURER_STATUS_WRITE_FAILED
MANUFACTURER_PERMISSION_ERROR
MANUFACTURER_PRIVACY_REFUSED
MANUFACTURER_INTERNAL_ERROR
```

The exact special ownership and mapping is:

| Error code | Exit | Tools | Bounded meaning |
| --- | ---: | --- | --- |
| `MANUFACTURER_DATASET_CONFLICT` | 10 | builder | Conflicting normalized records prevent building a valid database. |
| `MANUFACTURER_DETERMINISM_FAILED` | 11 | builder | The mandatory second build differs and no database/manifest pair is published. |
| `MANUFACTURER_SIDECAR_INVALID` | 15 | validator, generator | Sidecar validation failed, so an invalid sidecar is neither accepted nor published. |
| `MANUFACTURER_STATUS_INVALID` | 16 | validator, generator | Status validation failed, so an invalid status artifact is neither accepted nor published. |

`MANUFACTURER_STATUS_WRITE_FAILED` continues to map to exit 16 for the already
frozen status-write case. No existing exit or error code is renumbered or
repurposed; exits 1 and 13 remain unused. The four new codes are limited to the
causes above.

Not configured/missing/unreadable produce `unavailable`; invalid schema,
checksum, semantic, version, empty, or invalid inventory produce `error`; lock
and write failures produce `degraded` when an earlier valid sidecar exists and
`error` otherwise. Error messages are null or sanitized to 160 characters.
They never contain paths beyond basenames, source filenames, manufacturer names,
prefixes, MACs, IDs, IPs, hostnames, or rows. Counts are zero when no fresh
candidate could be built.

## 13. Manufacturer sidecar closed schema

The list-versus-map conflict is resolved in favor of a mapping. The exact
top-level order is:

```text
schema_version, generated_at, dataset_id, dataset_version,
dataset_semantic_sha256, record_count, matched_count, unknown_count,
excluded_count, invalid_count, records
```

`records` maps stable device IDs to records in lexical key order. Every key is
`^dev_[0-9a-f]{16}$`, appears again as `stable_device_id`, and is unique. Every
inventory device with a valid stable ID receives exactly one record, so
`record_count == len(records) == inventory device count`. Each record has exactly:

```text
stable_device_id, lookup_status, manufacturer, confidence, assignment_class,
matched_prefix, matched_prefix_length, source, dataset_version,
dataset_semantic_sha256, lookup_method
```

For `matched`, manufacturer is normalized text, confidence `high`, assignment
class/prefix/length are nonnull, source is `ieee_registration_authority`, and
method is `longest_prefix_v1`. Otherwise manufacturer/class/prefix/length are
null, confidence is `unknown`, source remains the dataset source, and method is
`none`. Dataset version/digest are repeated to make each private record
self-explanatory. Raw MAC, IP, hostname, and Asset data are prohibited.

Counts partition records: `matched_count` is `matched`; `unknown_count` is
`unknown_prefix` or `unsupported_address_type`; `excluded_count` is multicast or
locally administered; `invalid_count` is missing or invalid address. Counts sum
to `record_count`. `generated_at` is `%Y-%m-%dT%H:%M:%S.%fZ`.

## 14. Lookup result and address contract

`ManufacturerLookupResult` contains exactly the seven dataclass fields listed in
section 3. A match uses `lookup_method="longest_prefix_v1"`; every nonmatch uses
`none`. Dataset provenance is attached by sidecar construction, not duplicated
inside this in-memory result.

EUI-48 accepts compact 12-hex, six colon octets, six hyphen octets, or three
dotted four-hex groups. It returns uppercase colon octets. Mixed separators,
whitespace, zero, broadcast, wrong type/length, and nonhex are invalid.
Multicast is tested before local-admin; local-admin includes randomized MACs.
Eligible global addresses probe immutable maps in 36, 28, 24 order.

EUI-64 support is **validation without manufacturer claim**. It accepts compact
16-hex or eight consistently colon/hyphen-separated octets and normalizes to
uppercase colon octets. Multicast and local-admin classifications still apply;
other valid global EUI-64 values return `unsupported_address_type`. PE-3.1 never
removes `FF:FE`, never converts to EUI-48, and never prefix-matches EUI-64.

## 15. Manufacturer status closed schema

Exact ordered fields are:

```text
schema_version, updated, status, dataset_available, dataset_id, dataset_version,
dataset_semantic_sha256, record_count, matched_count, unknown_count,
excluded_count, invalid_count, conflict_count, generator, error_code,
error_message
```

`schema_version` is `1.0`; `generator` is `hioc-manufacturer-1`; status is
`online`, `degraded`, `unavailable`, or `error`. Dataset identity fields are
nonnull only after a valid dataset load. Counts are nonnegative integers.
`conflict_count` is zero for valid datasets. Online requires dataset available,
all identity fields, null error fields, and counts matching the new sidecar.

On successful generation, `updated` exactly equals sidecar `generated_at`.
Failure status may be newer while the last valid sidecar remains unchanged; its
counts describe the failed current attempt and are zero unless validated counts
are safely available. Status never describes device health and contains no
record values or identifiers.

## 16. Failure matrix

| Failure | Exit | Status/code | Existing sidecar | Status replacement |
| --- | ---: | --- | --- | --- |
| not configured | 4 | unavailable / `MANUFACTURER_NOT_CONFIGURED` | preserve | attempt sanitized replace |
| database missing | 4 | unavailable / `MANUFACTURER_DATABASE_MISSING` | preserve | attempt replace |
| manifest missing | 4 | unavailable / `MANUFACTURER_MANIFEST_MISSING` | preserve | attempt replace |
| unreadable/permission | 5 | unavailable / matching unreadable or permission code | preserve | attempt replace if writable |
| schema/empty/version | 6 or 9 | error / matching schema, empty, or version code | preserve | attempt replace |
| file/semantic mismatch | 7 or 8 | error / matching checksum code | preserve | attempt replace |
| inventory missing/invalid | 14 | error / inventory code | preserve | attempt replace |
| lock timeout | 17 | degraded or error / lock code | preserve | do not write while lock unavailable |
| sidecar write failure | 12 | degraded or error / sidecar-write code | preserve through atomicity | attempt status replace |
| status write failure before sidecar commit | 16 | degraded or error / status-write code | preserve | preserve prior status |
| status write failure after sidecar commit | 16 | degraded / status-write code | new valid sidecar remains | preserve prior status; stderr/JSON reports failure |

Retry is safe for every row after the cause is corrected. Inventory and all
public systems remain untouched. No fallback dataset is permitted. Rollback is
irrelevant unless deployed PE-3 code caused a protected regression or corruption.
Dataset conflict and determinism failure are manufacturer build failures;
sidecar and status validation failures are manufacturer-subsystem validation
failures. By themselves they never imply production rollback. A conflict
prevents a valid database build, determinism failure prevents publication of the
database/manifest pair, sidecar validation failure prevents accepting or
publishing an invalid sidecar, and status validation failure prevents accepting
or publishing an invalid status artifact. Inventory and every protected
subsystem remain unaffected.

## 17. Configuration and paths

The only key is `MANUFACTURER_DB_PATH`. Default is the empty string, meaning
disabled/not configured. A configured value must be an absolute path to a regular,
nonsymlink database. The manifest is the fixed sibling
`manufacturer-db.manifest.json`; no manifest key exists. The resolved database
and manifest must share a directory with mode no broader than 0700 and files
0600. Owner is the HIOC runtime user; group is its primary group. Paths outside
HIOC home are allowed only when every resolved parent is nonsymlink,
operator-approved, not group/world writable, and the files meet ownership/mode
rules.

The supported production layout is:

```text
/home/jazofv1/hioc/data/manufacturer/versions/<dataset-id>--<dataset-version>/manufacturer-db.json
/home/jazofv1/hioc/data/manufacturer/versions/<dataset-id>--<dataset-version>/manufacturer-db.manifest.json
/home/jazofv1/hioc/state/inventory/manufacturer.json
/home/jazofv1/hioc/state/inventory/manufacturer_status.json
```

Generated data is outside the Git checkout in installed runtime state, excluded
from release payloads, and preserved by install, upgrade, and rollback.

## 18. Generator locking and atomic writes

Generation uses exclusive nonblocking `flock` on `/tmp/hioc-manufacturer.lock`,
mode 0600, owned by the runtime user, with a 10-second monotonic timeout and
100-ms bounded polling. Kernel lock release handles crash/stale files; the file
is never deleted for recovery. Nested manufacturer locks and inventory locks are
prohibited.

The exact transaction order is:

1. Parse CLI arguments.
2. Resolve configuration and all effective paths.
3. Perform only non-content precondition checks that do not require reading
   mutable manufacturer or inventory data.
4. Acquire the dedicated manufacturer lock.
5. Under the lock, load and validate the manufacturer database.
6. Under the lock, load and validate the adjacent manufacturer manifest.
7. Under the lock, verify database/manifest checksum, semantic digest, version,
   and count consistency.
8. Under the lock, load and validate `inventory.json`.
9. Under the lock, build manufacturer sidecar and manufacturer status fully in
   memory.
10. Validate both generated documents fully in memory.
11. Determine semantic no-op behavior exactly as frozen below.
12. Write `manufacturer.json` through the approved same-directory atomic-write
    process.
13. Fsync the sidecar and parent directory as required.
14. Write `manufacturer_status.json` through the approved atomic-write process.
15. Fsync as required.
16. Release the manufacturer lock.
17. Return the documented sanitized result and exit code.

Before lock acquisition, processing is limited to CLI parsing and syntax,
required-argument presence, path-string normalization, configuration resolution,
and confirmation that required path arguments were supplied. Opening or
content-validating the database, manifest, or inventory; reading device IDs or
MAC fields; checksum, semantic, schema, version, or count validation; generation;
no-op comparison; and state writes occur only while the manufacturer lock is
held. Temporary files are unique, mode 0600, same-directory, cleaned on handled
failure, and named `.manufacturer.<pid>.*.tmp`.

This order supplies one stable manufacturer-generation transaction boundary,
closes the time-of-check/time-of-use gap between validation and generation, and
prevents concurrent manufacturer generators from validating one manufacturer
state and writing from another. It does not lock `inventory.json`: the
manufacturer lock serializes manufacturer-generation operations only. Inventory
remains externally managed. After acquiring the manufacturer lock, the generator
validates and reads one completed inventory snapshot and uses that loaded
in-memory snapshot for the rest of the generation. Replacement of
`inventory.json` after that read does not change the current generation, mutate
inventory, or block inventory generation. No inventory, PE-1 enrichment, Asset,
or other HIOC state lock is acquired or nested.

The earlier PE-3.1 executable implementation authorization is corrected only in
this respect: any instruction to validate manufacturer database, manifest, or
inventory content before acquiring `/tmp/hioc-manufacturer.lock` is superseded.
All other frozen PE-3.1 implementation contracts remain unchanged.

On semantic no-op, the sidecar is not rewritten and retains `generated_at`;
status is refreshed with `updated` equal to the retained timestamp and exit 0.
The status-after-sidecar partial failure is governed by section 16; a valid new
sidecar is never rolled back merely because sanitized status could not update.

## 19. Builder two-file transaction

The builder obtains exclusive `/tmp/hioc-manufacturer-build.lock` under the same
lock rules. It validates paths/checksums, parses, normalizes, resolves duplicates,
constructs database/digest/manifest, validates both, rebuilds independently in
memory, and requires byte equality. It creates a unique sibling staging
directory at mode 0700, writes/fsyncs both 0600 files, fsyncs the staging
directory, then atomically renames the entire staging directory to the requested
previously nonexistent `--output-directory` and fsyncs the parent.

Because the immutable version directory is the transaction unit, no compliant
reader can observe a mixed database/manifest pair. Failed builds remove staging
content and leave all existing version directories unchanged. Replacement is
prohibited. Dataset activation is a later governed configuration/deployment
change, never part of the builder.

## 20. Conflict and organization normalization

Exact normalized duplicates (same class, prefix, organization) collapse and
increment manifest `duplicate_count`. Same length/prefix with different
organization or class is a hard conflict and produces no artifact. Valid
different-length overlaps are retained; longest prefix resolves lookup. Invalid
lengths/prefixes and blank organizations fail.

Organization normalization is Unicode NFC, outer trim, and collapse of each
Unicode whitespace run to one ASCII space. CR/LF and Unicode control/format/
surrogate/private-use/unassigned characters are rejected before collapse.
Length after normalization is 1–256 code points. Case and punctuation are
preserved. HTML entities are not decoded, corporate suffixes are not changed,
and similar names or parent companies are never merged. CSV quoting is decoded
only by the CSV parser.

## 21. Source CSV parser

Each required source is UTF-8 with optional UTF-8 BOM, RFC 4180 comma CSV,
double-quote escaping, and LF or CRLF. Required logical columns are exactly
`Registry`, `Assignment`, and `Organization Name`; column order is arbitrary.
Additional columns are ignored and never copied. Missing, duplicate, or
case-different required headers are rejected. Blank physical lines are ignored;
comment syntax is unsupported and comment-looking rows are parsed normally.

`Registry` must equal the CLI source class exactly (`MA-L`, `MA-M`, `MA-S`).
`Assignment` is separator-free hexadecimal and normalized uppercase; widths
must match its class. Organization uses section 20. Malformed rows fail the
whole build. Each file is limited to 64 MiB and 500,000 data rows; excess is an
input refusal. Symlinks, nonregular files, NUL bytes, invalid UTF-8, and non-CSV
inputs are rejected. Tests use only synthetic structural fixtures marked
`synthetic fixture; not sourced from IEEE`.

## 22. Inventory input contract

The source is `<home>/state/inventory/inventory.json`. It must be an object with
a `devices` list; other existing inventory fields are read but ignored. Each
device must be an object with unique `id` matching `^dev_[0-9a-f]{16}$`.
The sole address input is device `mac`; PE-3 never consults IP, hostname,
provenance, identity strength, historical candidates, or another MAC field.

Missing/null/empty MAC yields `missing_address`; nonstring or malformed MAC
yields `invalid_address`; local/multicast/global rules then apply. Every valid
stable device receives a record, including IP-only devices. Duplicate/invalid
stable IDs or a non-list device collection make the entire inventory invalid.
Input device order cannot affect output. Manufacturer generation performs no
identity reconciliation and requires sidecar record count equality.

## 23. Privacy

The private sidecar may contain stable IDs, selected manufacturer, public matched
prefix, assignment class, confidence/status, and dataset provenance exactly as
its schema permits. Matched prefixes are prohibited everywhere else. Status,
human/JSON CLI output, routine logs, Evidence Reports, and validator output must
not contain stable IDs, MACs, IPs, hostnames, matched prefixes, manufacturer
names/lists, rows, source contents, absolute source paths, Assets, or household
metadata. Errors may contain only safe basenames when necessary.

Evidence Reports contain Git identity, aggregate counts, versions/digests,
timings, Boolean invariants, result/rollback codes, and evidence checksums.
Tests/documentation use synthetic IDs, addresses, prefixes, and organizations
only. No debug option weakens privacy.

## 24. Installer and release contract

Modes are: `manufacturer.py` 0600; builder/validator/generator 0700; data and
version directories 0700; database/manifest 0600; sidecar/status 0600. Owner is
the HIOC runtime user and group its primary group. Installer creates empty
`data/manufacturer/versions` at 0700, deploys code/modes, and adds the empty
configuration key only when creating a new configuration. It creates no dataset,
manifest, sidecar, status, backup, schedule, or network action.

Install, upgrade, and rollback exclude `data/manufacturer/**` and manufacturer
sidecars from replacement/deletion and preserve an existing configuration value.
Immutable version directories provide dataset history; no extra backup path is
created. Release validation proves scripts/library/modes and absence of bundled
database/source files, services, timers, cron, download code, or network clients.
An unconfigured dataset is normal.

## 25. Exact test mapping

The implementation must provide at least 92 tests, retaining all approved
76-case coverage:

| File | Minimum | Ownership |
| --- | ---: | --- |
| `test_manufacturer_schema.py` | 18 | database, manifest, sidecar/status closed schemas, order, counts, digests |
| `test_manufacturer_lookup.py` | 18 | EUI-48 forms/classes, 36/28/24 precedence, unknown, explicit EUI-64 no-claim |
| `test_manufacturer_builder.py` | 16 | CSV/checksums, normalization, duplicates/conflicts, limits, determinism, directory transaction |
| `test_manufacturer_cli.py` | 12 | exact flags, output schemas, exit/error mapping, privacy, read-only validator |
| `test_manufacturer_sidecar.py` | 12 | inventory contract, mapping/counts, no-op, lock, atomic/failure preservation |
| `test_manufacturer_release.py` | 8 | install/modes/preservation/rollback, no dataset/schedule/network |
| `test_manufacturer_governance.py` | 8 | synthetic markers, forbidden dataset patterns/size, file boundaries, consumer invariants |
| **Total** | **92** | |

Tests also run PE-1, PE-2, identity, canonical, inventory, release, compilation,
shell, documentation, and full regression suites. No test uses a network, real
assignment, production identifier, root access, locale dependence, or clock
dependence.

## 26. Performance contract

Synthetic representative database is 100,000 records and builder input is
100,000 rows. Repository-host results are informational but must reveal no
unbounded behavior. PI3 thresholds are: load/manifest/index p95 ≤750 ms; lookup
p95 ≤5 ms and median ≤1 ms; 1,000-device generation p95 ≤2.0 s warm and ≤4.0 s
cold; builder ≤15 s for 100,000 rows; peak incremental RSS ≤48 MiB. Warning
threshold is 80% of a bound. Lock timeout is 10 s.

Production rollback requires two governed repeated measurements above 150% of
a hard bound with stable inputs and demonstrated PE-3 causality. A single noisy
measurement, repository-host variance, or optional dataset absence is not
rollback-worthy.

## 27. Production validation boundary

No production command is defined here. Future validation phases are exactly:
target/repository verification; Git artifact identity; local acquisition
evidence; offline build; deterministic second-build proof; database/manifest
validation; supported deployment; runtime artifact identity; manual generator;
sidecar/status validation; controlled synthetic lookup validation; sanitized
aggregate production count review; protected-invariant comparison; privacy;
performance; rollback classification; sanitized Evidence Report.

Real data proof is structural/statistical only: hashes, counts by class, schema,
determinism, and aggregate match/status counts. It never prints names, prefixes,
MACs, or rows. Lookup correctness is proven separately with a locally generated
synthetic mini-database before real local generation. Stable identifiers, if
needed for comparison, appear only as salted run-local digests and are not
retained in repository evidence.

## 28. Result and rollback semantics

`PASS` means every required implementation, artifact, privacy, performance, and
protected-invariant check passed. `PARTIAL_PASS` means optional enrichment
evidence is unavailable while all protected invariants and validated available
artifacts pass; it never authorizes claiming production validation complete.
`INPUT_OR_PRECONDITION_ERROR` means target, Git, configuration, acquisition,
or required input cannot be proven. `VALIDATION_FAIL` means a validator found a
deterministic schema, identity, checksum, privacy, or performance failure.
`FAIL` means a demonstrated deployed regression or transaction corruption.

Rollback may be recommended only for deployed-code mismatch, installer/release
corruption, protected public/inventory regression caused by PE-3, PE-3 state
corruption, privacy leak, loss/overwrite of preexisting local data, or the
repeated causal performance condition in section 26. No configured dataset,
missing preexisting dataset, unknown/zero matches, local addresses, unattractive
labels, incomplete licensing acquisition, uncertainty, or unavailable optional
evidence never recommends rollback.

## 29. Dataset exclusion governance

Git and release tests reject source basenames matching IEEE registry CSV patterns,
any `manufacturer-db.json` or `manufacturer-db.manifest.json` outside explicitly
marked small synthetic temporary fixtures, and large OUI-like snapshots. Fixture
documents must contain metadata/comment marker `synthetic fixture; not sourced
from IEEE`, be under `tests/fixtures/manufacturer/`, and remain below 64 KiB.
Runtime paths `data/manufacturer/**` and generated manufacturer sidecars are
specifically ignored without ignoring documentation or fixtures. Tests use path,
marker, schema, and size rules—not organization-name guesses.

## 30. Checkpoint boundary

The executable implementation may now be mechanical. It still requires explicit
authorization. No IEEE data is approved for Git or release redistribution. Local
operator acquisition/transformation is the only approved dataset model.
Production dataset build, deployment, validation, PE-4, scheduling, and consumer
publication remain separate and not started.
