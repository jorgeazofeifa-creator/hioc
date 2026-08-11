# PE-3.1 Manufacturer Enrichment Repository Evidence

Status: **PASS — EXECUTABLE IMPLEMENTATION REPOSITORY VALIDATED; PRODUCTION PENDING**

PE-3.3 freezes the production deployment and validation procedure in
[PE3_MANUFACTURER_PRODUCTION_RUNBOOK.md](PE3_MANUFACTURER_PRODUCTION_RUNBOOK.md).
The design transfers only the validated normalized database and manifest,
installs the immutable `local-ieee-ra--2026-08-11-r1` version after supported
code deployment and staged validation, activates configuration conditionally,
generates the private sidecar, and captures aggregate protected/privacy/
performance evidence one operator action at a time. This design has not been
executed and does not constitute production validation.

## Scope and implementation

PE-3.1 now provides the isolated manufacturer library, offline local-source
builder, strictly read-only validator, and separate manually invoked generator.
It creates no inventory hook, schedule, service, network lookup, dataset, or
public consumer. Manufacturer remains private descriptive Enrichment and cannot
affect identity, canonical address, inventory membership, PE-1, PE-2, health,
liveness, incidents, MQTT, Home Assistant, dashboards, topology, dependencies,
services, expected availability, automation correlation, or retention.

The normalized database, adjacent manifest, manufacturer sidecar, and subsystem
status implement the closed version `1.0` schemas. Database records use lexical
`<prefix-length>:<uppercase-prefix>` keys. Canonical UTF-8 JSON, the semantic
digest self-exclusion rule, complete-file checksum, counts, source identities,
deterministic ordering, unknown-field rejection, and immutable maps are enforced.

## Lookup, confidence, and provenance

Eligible global EUI-48 values use deterministic 36-, 28-, then 24-bit lookup.
Explicit EUI-64 is validated and classified but never converted or matched.
Matched pinned reference data has `high` confidence; every nonclaim is `unknown`.
The private sidecar records the frozen source, dataset version/digest, assignment
class, safe matched prefix, and lookup method without storing raw MAC, IP, or
hostname. Status and CLI output contain aggregate sanitized values only.

## Builder and publication

The builder accepts only three explicit local CSV paths and expected SHA-256
values. It supports the frozen UTF-8/BOM/RFC-4180 structure, bounded
normalization, duplicate collapse, explicit non-selectable conflict preservation,
bounds, and exact error mappings. It owns the exclusive
`/tmp/hioc-manufacturer-build.lock`, constructs twice, validates, fsyncs two
private staging files and their directory, atomically promotes the previously
nonexistent immutable version directory, and fsyncs the parent. It has no network
or replacement mode.

## Validator and generator

The validator has no lock or writer. Tests prove it contains no `flock`, builder
lock, generator lock, or third lock and leaves validated files unchanged. Its
safety for database pairs derives from immutable atomic publication. Runtime
cross-file inconsistencies are reported without repair.

The generator owns the exclusive `/tmp/hioc-manufacturer.lock`. Source and tests
prove database, manifest, and inventory reads occur only after acquisition. One
validated inventory snapshot is used in memory; no other state lock is acquired.
Sidecar/status documents are validated before restrictive atomic writes. The
semantic no-op retains the sidecar bytes and timestamp. Invalid existing sidecar,
write, status, dataset, inventory, checksum, schema, and lock failures remain
isolated and preserve authoritative inventory and public systems.

## Error mappings and release preservation

The corrected first-class mappings are structurally irreconcilable conflict/10, determinism/11,
sidecar-invalid/15, and status-invalid/16; exits 1 and 13 remain unused. Installer
and release integration deploy the library at `0600`, commands at `0700`, create
only an empty private versions directory, preserve manufacturer data/config/state
across install, upgrade, and rollback, and add no dataset, schedule, service, or
network action. Narrow ignores and governance tests exclude production registry
artifacts while allowing explicitly marked small synthetic fixtures.

## Repository validation

- Focused PE-3 suite: 119 tests passed.
- Full regression: 467 tests passed with 8 environment-dependent skips.
- Python compilation, shell syntax, release validation, documentation links,
  exclusion, privacy, secret, protected-file, and diff checks passed.
- No IEEE source or transformed registry row is present. Test values and names
  are fictional and explicitly marked `synthetic fixture; not sourced from IEEE`.

Repository-host synthetic measurements:

| Target | Result |
| --- | ---: |
| Database load | 2.73 ms |
| Database validation mean | 0.094 ms |
| MA-L lookup | 5.04 µs |
| MA-M lookup | 4.59 µs |
| MA-S lookup | 4.60 µs |
| Unknown lookup | 4.45 µs |
| 1,000-device generation | 19.4 ms |
| 100,002-row builder transaction | 11.23 s |

Repository timings are informational. PI3 timing and incremental RSS remain
production-validation evidence and were not measured here.

## PE-3.2 sanitized local dataset-build evidence

The official MA-L, MA-M, and MA-S public listings were acquired and retained
only in the external operator workspace. Their hashes are recorded in the
external evidence report. Bounded source compatibility removes U+200B/U+200E,
collapses TAB as whitespace, and preserves two aggregate MA-L conflict keys as
non-selectable entries without organization variants.

Two independent external builds produced byte-identical database and manifest
artifacts. Each contains 53,581 selectable records and 2 conflict keys, totaling
53,583 normalized unique assignment keys. Class counts are MA-L 39,916, MA-M
6,538, and MA-S 7,127; exact normalized duplicate count is zero. The database
SHA-256 is `81f147cc57768c5797c4ad73a8c0369001bbdcbfe1548e71d3702c8c7f81e0e1`,
semantic SHA-256 is `2dbda82441416feea8d2f60c4ebe043c033c1de80ed50460e55a5367dcc1083c`,
and manifest SHA-256 is `10c8097c0a4ec6e8cc4cd3dc61afc7f368057f4ef4b6534df9f6dd31634a4ac4`.
Both lock-free validator runs passed with zero file mutation. Synthetic conflict
lookup controls, aggregate validation, privacy, and repository contamination
checks passed.

Local production-intended measurements were 913.687 ms mean database load,
865.423 ms mean complete validation, 6.952 microseconds mean synthetic excluded
lookup, 115,190,469 bytes traced peak allocation, 8,652,642 database bytes, and
1,338 manifest bytes. PI3 performance remains pending.

## Production boundary

Official IEEE source and the production-intended database/manifest exist only in
the external operator workspace; none was committed or packaged. PI3 and PI5
were not accessed. No deployment, production sidecar generation, or production
validation occurred. Deployment and PI3 validation remain separately authorized
and pending. PE-4 has not started. PE-3 is not complete.
