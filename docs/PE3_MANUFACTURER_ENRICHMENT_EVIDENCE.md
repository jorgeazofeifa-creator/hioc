# PE-3.1 Manufacturer Enrichment Repository Evidence

Status: **PASS — EXECUTABLE IMPLEMENTATION REPOSITORY VALIDATED; PRODUCTION PENDING**

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
values. It supports the frozen UTF-8/BOM/RFC-4180 structure, normalization,
duplicates, conflicts, bounds, and exact error mappings. It owns the exclusive
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

The corrected first-class mappings are conflict/10, determinism/11,
sidecar-invalid/15, and status-invalid/16; exits 1 and 13 remain unused. Installer
and release integration deploy the library at `0600`, commands at `0700`, create
only an empty private versions directory, preserve manufacturer data/config/state
across install, upgrade, and rollback, and add no dataset, schedule, service, or
network action. Narrow ignores and governance tests exclude production registry
artifacts while allowing explicitly marked small synthetic fixtures.

## Repository validation

- Focused PE-3 suite: 96 tests passed.
- Full regression: 444 tests passed with 8 environment-dependent skips.
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

## Production boundary

No IEEE data was downloaded, committed, transformed, or built. No production
database or manifest exists. PI3 and PI5 were not accessed. No deployment or
production command occurred. Production dataset acquisition, local build,
deployment, performance proof, and validation remain separately authorized and
pending. PE-4 has not started. PE-3 is not complete.
