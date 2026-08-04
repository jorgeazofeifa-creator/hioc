# PE-3.1 Manufacturer Enrichment Implementation Design

Status: **DESIGN APPROVED; EXECUTABLE IMPLEMENTATION NOT STARTED**

This document freezes the PE-3.1 implementation contract. It creates no
executable, dataset, runtime, deployment, or production change. The governing
architecture remains [PE3_MANUFACTURER_ENRICHMENT_SPEC.md](PE3_MANUFACTURER_ENRICHMENT_SPEC.md).

## Scope and non-authority

PE-3.1 derives private manufacturer-reference evidence from an existing,
authoritatively selected device address and an approved offline reference
artifact. It never selects identity or canonical IP and never modifies
inventory, Assets, incidents, health, liveness, MQTT, Home Assistant, dashboards,
topology, dependencies, or service ownership. It performs no networking, online
lookup, or dataset download.

The implementation is split into a pure lookup library, an offline build tool,
and a read-only validator. Dataset injection is intentionally independent of
runtime lookup so a later redistribution decision cannot require runtime code
changes.

## License, acquisition, and distribution gate

IEEE Registration Authority remains the selected prospective authority, but no
standalone permission to redistribute its public registry data has been
established. Public availability is not redistribution permission. Until a
recorded review approves a use, the following restrictive decision applies:

- raw IEEE files must not be committed, bundled, mirrored, or redistributed;
- the normalized database and other artifacts containing assignment names or
  prefixes must not be committed, bundled, or redistributed;
- generated manifests containing only hashes, counts, tool identity, and
  license-review metadata may be retained, but not source rows or organization
  names;
- no dataset download is performed by HIOC runtime, deployment, or build tools;
- production use remains blocked until acquisition and use are approved.

The exact future acquisition workflow is:

1. A designated reviewer records the IEEE terms/pages reviewed, review date,
   reviewer, allowed acquisition/use/distribution, attribution, retention, and
   approval reference.
2. On a governed non-production workstation, an operator downloads the approved
   MA-L, MA-M, and MA-S source files from the recorded canonical HTTPS URLs into
   an external temporary directory. The filenames, sizes, retrieval UTC time,
   and SHA-256 values are captured before parsing.
3. The offline builder receives only explicit local input paths. It has no HTTP
   client and rejects missing, unexpected, or duplicate inputs. Expected source
   checksums are supplied in an approved acquisition manifest and checked before
   parsing.
4. The builder validates source shape, normalizes approved fields, rejects
   conflicts, produces a deterministic database in a temporary directory, and
   emits a sanitized build report. A second build must be byte-identical.
5. The normalized database is validated and its complete-file SHA-256 is added
   to the release/deployment manifest. Deployment injects the exact verified
   file at the configured reference path; runtime never sees raw IEEE files.
6. Production deployment remains offline. The target verifies the normalized
   database checksum, schema, counts, and permissions before atomically making
   the complete artifact current.

If redistribution is later approved, a reviewed release may contain the same
normalized file. If it is not approved, an authorized operator builds and
injects that file locally. Both paths use the same artifact schema, checksum
verification, configuration key, loader, lookup algorithm, and validation.

Updates are one-version-at-a-time governed transactions: acquire new pinned
inputs outside production, build twice, compare semantic and count diffs,
review license/attribution again, test, approve, and deploy a complete artifact.
There is no automatic refresh or `latest` selector. Rollback atomically restores
the preceding normalized artifact and manifest, verifies its checksum, reruns
validation, and does not modify any inventory or Asset state. A partial file is
never promoted.

## Normalized runtime dataset

The runtime consumes one UTF-8 JSON file, `manufacturer-db.json`, with a final
newline. JSON is emitted with keys in the order shown, two-space indentation,
Unicode NFC strings, and no locale-dependent transformation. The top-level
object contains exactly:

| Field | Frozen contract |
| --- | --- |
| `schema_version` | String, exactly `1.0` for this design |
| `dataset_version` | Immutable string `ieee-ra-YYYYMMDD-<12 lowercase digest characters>` derived from acquisition evidence, never `latest` |
| `dataset_source` | String, exactly `ieee_registration_authority` |
| `dataset_sha256` | Lowercase SHA-256 of the canonical UTF-8 `records` array bytes defined below; it is not the self-referential whole-file hash |
| `generated_at` | UTC RFC 3339 timestamp with `Z`; provenance only and excluded from semantic equality |
| `record_count` | Integer equal to `len(records)` and the three class counts summed |
| `ma_l_count` | Integer count of 24-bit MA-L rows |
| `ma_m_count` | Integer count of 28-bit MA-M rows |
| `ma_s_count` | Integer count of 36-bit MA-S rows |
| `records` | Deterministically ordered array of closed records |

Each record contains exactly `prefix`, `prefix_length`, `assignment_type`, and
`organization`, in that key order. `prefix` is uppercase hexadecimal with no
separator and exactly 6, 7, or 9 digits for 24, 28, or 36 bits. The paired
`assignment_type` is exactly `MA-L`, `MA-M`, or `MA-S`. `organization` is the
trimmed, whitespace-collapsed, NFC organization label; empty/control-bearing
labels are rejected. Street addresses, country, contact details, private rows,
source formatting, and aliases are excluded.

Records sort by descending `prefix_length`, then ascending `prefix`, then
Unicode-code-point `organization`. Duplicate identical rows collapse before
counts are calculated. A repeated prefix with different content is a fatal
dataset conflict. The canonical `records` bytes used for `dataset_sha256` are
compact JSON (`ensure_ascii=false`, separators `,` and `:`), with the frozen key
order and no final newline. The deployment manifest separately stores the
SHA-256 of the complete formatted database file and its Git/build identity.

Raw IEEE text or CSV is never installed or parsed at runtime.

## Deterministic lookup

At load time, validated records populate three immutable maps keyed by their
24-, 28-, and 36-bit integer prefixes. Lookup normalizes the caller-supplied
address, rejects prohibited classes, and checks 36, then 28, then 24 bits.
This makes lookup O(1) with three bounded map operations. Longest prefix always
wins; equal-prefix ties cannot survive dataset validation. Input and output are
independent of source order, locale, hash iteration order, platform, and time.

- MA-L is exactly 24 bits, MA-M exactly 28 bits, and MA-S exactly 36 bits.
- EUI-48 accepts only six colon- or hyphen-separated octets, three dotted
  four-hex groups, or 12 unseparated hexadecimal characters; mixed separators,
  whitespace, all-zero, broadcast, malformed, and over/under-length values are
  invalid.
- A multicast/group address returns `multicast` without lookup.
- A locally administered address returns `locally_administered` without clearing
  the U/L bit or guessing. Randomized MACs therefore do not claim a manufacturer.
- EUI-64 is accepted only through an explicit `address_kind="eui64"` API input,
  with 16 hexadecimal digits under the same separator rules. It is matched on
  its leading allocation bits. It is never inferred from length in inventory,
  never collapsed by removing `FF:FE`, and never used to alter identity.
- No match returns `unknown`; dataset unavailability returns `unavailable`.
- A valid match returns the selected organization, assignment type, matched
  prefix/length, `longest_prefix_v1`, and `high` confidence. Every non-match
  class returns a null manufacturer and `unknown` confidence.

Invalid input is a per-record result, not a crash. Invalid dataset records are a
whole-artifact error and the database is not loaded.

## Module architecture

### `pi4/lib/hioc/manufacturer.py`

Pure, offline domain module. It defines the closed schemas/enums, validates the
normalized artifact, verifies the records digest, builds immutable prefix maps,
normalizes explicit EUI-48/EUI-64 input, performs deterministic lookup, and
constructs sanitized sidecar records. It has no downloader, socket, DNS, system
OUI fallback, mutable global cache, inventory writer, or Asset writer.

### `pi4/bin/hioc-build-manufacturer-db.py`

Governed build-time tool only. It accepts explicit external source files and an
approved acquisition manifest, verifies source SHA-256 values, parses only the
approved IEEE layouts, creates the normalized artifact in a temporary location,
checks duplicate/conflict/count rules, and atomically writes an explicitly named
output. It never downloads and is not invoked by production inventory runtime.

### `pi4/bin/hioc-validate-manufacturer.py`

Read-only validator. It checks Git-derived implementation identity, manifest and
artifact checksums, closed schemas, deterministic lookup vectors, sidecar/status
coherence, privacy, performance, and protected-invariant evidence. Output is a
sanitized Evidence Report containing counts, hashes, timings, statuses, and
failures—not MACs, stable IDs, organization lists, or lookup traces.

No PE-3 module may modify identity, canonical IP, inventory, Assets, incidents,
health, liveness, MQTT, Home Assistant, dashboards, or perform networking,
online lookup, or dataset download.

## Runtime and storage architecture

The configured normalized database path is
`${HIOC_STATE_DIR}/reference/manufacturer/manufacturer-db.json`; the adjacent
private manifest is `manufacturer-db.manifest.json`. The path may be supplied by
one configuration key, `MANUFACTURER_DB_PATH`, whose default is the path above.
There is no second version selector: the file content and verified manifest own
dataset identity.

Manufacturer results use a separate private sidecar rather than extending PE-1
`enrichment.json`:

- `${HIOC_STATE_DIR}/inventory/manufacturer.json`
- `${HIOC_STATE_DIR}/inventory/manufacturer_status.json`

Separation is required because hostname evidence and reference-dataset evidence
have different schemas, refresh triggers, license provenance, failure modes,
retention, and rollback. It avoids changing the production-validated PE-1
contract and lets manufacturer generation fail open without rewriting hostname
evidence. It also prevents reference-artifact lifecycle from coupling to Asset
transactions. Both files use the existing restrictive state permissions,
temporary-file validation, fsync/atomic replace, and deterministic ordering.

`manufacturer.json` contains exactly `schema_version`, `generated_at`,
`dataset_version`, `dataset_source`, `dataset_sha256`, `device_count`, and
`records`. `schema_version` is `1.0`; `records` is a list sorted by
`stable_device_id`. Each record contains exactly:

`stable_device_id`, `manufacturer`, `lookup_status`, `selection_rule`,
`dataset_version`, `dataset_sha256`, `matched_prefix`,
`matched_prefix_length`, `assignment_type`, `source`, `confidence`, and
`looked_up_at`.

`selection_rule` is `longest_prefix_v1` for a match and `none` otherwise;
`source` is `ieee_registration_authority`; timestamps are UTC RFC 3339. Matched
prefix is the public allocation prefix only, never the full address. Nulls are
explicit. `device_count` equals list length and stable IDs are unique.

`manufacturer_status.json` contains exactly `schema_version`, `generated_at`,
`status`, `dataset_version`, `dataset_sha256`, `device_count`, `matched_count`,
`unknown_count`, `locally_administered_count`, `multicast_count`,
`invalid_count`, `duration_ms`, and `reason`. `status` is `online`, `degraded`,
or `unavailable`; `reason` is a closed sanitized code. It contains no record
values or identifiers.

Future operator manufacturer corrections remain PE-2 Asset metadata under a
separately approved field/schema migration. They may be selected for display by
a future adapter but never overwrite, mutate, or suppress these reference
records or their dataset provenance.

## Performance contract

- immutable three-map index and O(1) lookup;
- normalized artifact target at most 10 MiB;
- peak incremental resident memory at most 32 MiB on PI3;
- load, checksum, schema validation, and index construction at most 500 ms p95;
- individual lookup at most 1 ms median and 5 ms p95;
- full 500-device enrichment at most 1 second p95 after operating-system cache
  warm-up and at most 2 seconds cold;
- one database load per inventory process, no daemon, per-device disk cache,
  unbounded memoization, runtime source parsing, or networking.

Performance validation uses monotonic time, at least five warm iterations, a
documented cold run, synthetic addresses, and reports aggregates only.

## Failure isolation

Missing dataset/manifest, corrupt JSON, schema mismatch, record-digest or
complete-file checksum mismatch, unsupported schema/dataset source, partial
artifact, empty artifact, count mismatch, duplicate conflict, invalid encoding,
or permission error prevents the candidate artifact from loading. The generator
records a sanitized `unavailable`/`degraded` status and exits its enrichment
step without changing the last valid manufacturer sidecar. A first-run failure
may leave the sidecar absent. Empty datasets are invalid even when counts agree.

There is no fallback database or online query. Temporary/partial output is
deleted or left outside the current path. Inventory continues normally, and no
failure may affect identity, canonical IP, inventory output, Assets, health,
liveness, MQTT, Home Assistant, dashboards, or incidents. Rollback is
recommended only when PE-3 deterministically breaks a protected invariant,
leaks protected data, produces nondeterministic output, or promotes an invalid
artifact—not merely because manufacturer enrichment is unavailable or unknown.

## Privacy contract

Manufacturer assignment data is public reference material, subject to the
license gate, but correlation with household devices is private. Raw source
evidence remains private. The dataset excludes addresses and contacts; the
sidecar and logs exclude full MACs. Validation output excludes stable IDs,
organization values, per-record lookup traces, internal paths containing user
data, source rows, inventory values, and Asset metadata. No PE-3 data is
published to MQTT, Home Assistant, dashboards, notifications, or incidents.
Debug mode cannot relax these rules.

## Production validation contract

Future deployment requires a pre-change Evidence Report, governed deployment,
post-change report, invariant comparison, and explicit rollback decision. It
must prove:

1. clean source and exact approved Git commit for all three implementation files;
2. normalized records digest, complete artifact checksum, acquisition-manifest
   checksums, schema, counts, source, and version;
3. byte-identical cross-platform build fixtures and deterministic lookup vectors;
4. sidecar/status closed schemas, atomic generation, and provenance coherence;
5. performance bounds on PI3 without raw values in timing output;
6. absence of MACs, organization lists, stable IDs, Assets, or lookup traces in
   logs, status, reports, MQTT, Home Assistant, and public inventory;
7. exact equality for inventory membership/IDs, canonical IPs, identity events,
   observation, health, liveness, incidents, Assets, MQTT payloads, Home
   Assistant contracts, topology, dependencies, and service ownership;
8. unchanged PE-1 and PE-2 artifacts; and
9. final state equality after synthetic failure/rollback exercises.

The sanitized report includes Git commit, file/artifact hashes, dataset version
and hashes, counts, closed result codes, aggregate timings, invariant booleans,
privacy result, rollback recommendation, and evidence-file checksums. It contains
no production record values. A genuine deterministic invariant, privacy,
identity, checksum, schema, atomicity, or reproducibility failure is rollback
eligible. Missing matches, local/randomized addresses, honest unknowns, or an
unavailable optional dataset with inventory intact are not.

## Executable test plan (76 tests)

The next executable checkpoint must implement approximately this matrix:

| Area | Tests | Required cases |
| --- | ---: | --- |
| Dataset closed schema | 10 | valid artifact; missing/extra/type-invalid top fields; unsupported schema/source; empty artifact; count sum; records digest; complete-file manifest digest |
| Record normalization | 9 | valid MA-L/MA-M/MA-S; exact prefix widths; invalid hex; invalid length/type pairing; empty/control organization; NFC/whitespace; identical duplicate collapse; conflicting duplicate reject |
| Prefix selection | 10 | 24/28/36 matches; 36-over-28/24; 28-over-24; unknown; source-order independence; map-order independence; prefix boundary low/high; tie impossible/rejected |
| Address parsing | 12 | colon, hyphen, dotted, compact EUI-48; lowercase normalization; mixed separators; whitespace; short/long; nonhex; zero; broadcast; explicit EUI-64 |
| Address classes | 8 | multicast; local-admin; two randomized patterns; global; explicit EUI-64 direct prefix; no FF:FE collapse; invalid implicit EUI-64 |
| Result/provenance | 7 | matched/unknown/unavailable; exact rule/source/version/digest; public matched prefix only; confidence; timestamp exclusion from semantic equality |
| Sidecar and failure | 8 | deterministic ordering; unique stable IDs/count; atomic replace; preserve prior on missing/corrupt/checksum/schema/partial/permission failure; first-run absence |
| Privacy | 4 | no full MAC; no organization list/trace in report; no Asset values; no MQTT/HA/public inventory output |
| Performance | 3 | load/memory, single lookup, 500-device batch bounds |
| Reproducibility | 3 | Windows/Linux byte identity; locale/time-zone independence; repeated-build identity |
| Protected invariants | 2 | before/after complete contract equality; synthetic rollback final-state equality |
| **Total** | **76** | |

Tests use synthetic organizations and prefixes only; no IEEE rows or production
identifiers enter fixtures. Focused tests must be accompanied by the existing
inventory, PE-1, PE-2, incident, MQTT/HA contract, link, secret, and full relevant
regression suites. No test may require a network connection.

## Frozen decisions and next gate

This checkpoint freezes schema, digest semantics, file paths, sidecar separation,
module responsibilities, lookup/class behavior, provenance, performance,
failure, privacy, validation, and tests. It does not approve dataset acquisition,
commit, redistribution, production use, or executable implementation.

The next authoritative checkpoint is **PE-3.1 executable implementation**, and
it remains blocked until the IEEE license/use review explicitly approves an
acquisition and deployment mode. If approval permits external use but not
redistribution, implementation proceeds with synthetic fixtures and the frozen
injection interface; the repository still contains no IEEE-derived data.
PE-3.2 and later phases are not started.
