# PE-5.1 - Private Local Service Association Contract and Pure Resolver

Status: **IMPLEMENTED_REPOSITORY_CANDIDATE**, pending complete regression and independent review.
Authority: separate user authorization following committed [Preparation](PE5_IMPLEMENTATION_PREPARATION.md)
at f3730ba5a8745361934ff822a9c29c16c9d0767b. The [Master Plan](HIOC_MASTER_PLAN.md#current-objective)
owns current sequencing. PE-4, Public Projection, Hygiene and Documentation Correction remain closed.
This is repository-only implementation. Production, deployment, runtime integration, persistence,
collection, MQTT, scheduling, Active Discovery and surveillance remain NOT AUTHORIZED.
Commit/push require separate authorization. No production access or observation occurred.

## API and input authority

pi4/lib/hioc/service_association.py exports resolve_service_associations(snapshot, evaluated_at,
max_snapshot_age_seconds), validate_service_association_envelope(envelope), contract_schema(),
and safe ServiceAssociationError(code). All three resolver inputs are required. There is no default age,
clock, environment/configuration input, file/state read, network, subprocess, broker or scheduler.
Existing inventory.normalize_mac and inventory.stable_device_id are reused, not reimplemented.

Input is finalized Inventory schema 1.0 JSON data with updated, devices, services, topology,
dependencies and summary. Existing additional inventory/device metadata remains unmodified and
unpublished. Input subclasses/custom objects, non-finite numbers, non-string keys or excessive nesting
fail the whole contract. Records are never modified. A malformed/unidentifiable device record fails
SNAPSHOT_DEVICE_INVALID because global owner uniqueness cannot be established. Recognizable
malformed owners are rejected at service level, not silently repaired.

RFC3339 input timestamps require date, time, seconds and timezone, with at most six fractional digits.
UTC output uses microseconds and Z. Missing/invalid timestamps, future or stale snapshots produce
safe whole-input exceptions with no current association output. Age is compared exactly, including
microseconds; the supplied nonnegative integer is inclusive. Boolean/floating/string/negative policy
values fail INVALID_MAX_SNAPSHOT_AGE. The JSON-safe integer ceiling 2**53-1 is a representation bound,
not production policy. Policy status remains UNKNOWN_REQUIRED_BEFORE_OPERATIONAL_USE.
Repository implementation and synthetic testing are possible without choosing a production threshold;
operational use requires independently approved policy/source/native evidence.

## Resource and shape bounds

4096 devices, 4096 services, 16 MiB canonical input bytes and 32 JSON nesting levels are fail-closed
resource limits, not an operational snapshot-age threshold or assumptions about production counts.
There is no truncation or subset promotion on oversized input. Service fields are restricted to the
existing id/name/type/device_id/status/source/port/host/dependency shape. Display/status values are
validated for shape but never used as identity, freshness or health authority and never emitted.

Service IDs are existing build_services forms: svc_<mqtt|dns|dhcp|ups|ssh|scheduler>_<8 hex>,
svc_mqtt_listener, svc_network_53 and svc_network_67. Systemd hashed IDs must agree with type;
ss fixed IDs must agree with type and explicit existing port 1883/53/67. Port is consistency evidence
only, never owner identity. Unsupported sources/types/IDs cannot enter accepted output.

## Strong ownership, duplicates and rejection

An accepted owner is an existing dev_<16 hex> reference with exactly one device record, a valid
normalized nonempty MAC appearing in exactly one device record, and an ID equal to the existing
MAC-derived stable_device_id. No IP, hostname, name, port, topic, vendor, dependency or health match
can establish ownership. Duplicate owner IDs and MAC collisions reject; valid MAC with inconsistent
ID rejects. Missing/weak/malformed owners reject. Nothing creates or merges devices, changes canonical
IP/MAC/IDs or observation timestamps, or writes health, availability, Assets, incidents or graphs.

Identical consumed (service ID, owner ID, source, type) tuples deduplicate even when non-authoritative
display/status metadata differ. Any same-ID disagreement in owner/source/type rejects the entire ID
instead of choosing first/last; malformed same-ID evidence mixed with valid evidence also rejects.
No pre-collector evidence discarded by existing build_services can be reconstructed or claimed here.
Each safe-ID group produces one acceptance or rejection. Malformed/unsafe-ID rows each produce a
null-ID rejection, never disappear silently. Output ordering is deterministic, including null-ID rejections: the total sort key includes
safe owner/source references after service ID and reason, so ties do not preserve input order.
The combined acceptance/rejection count also cannot exceed the input record limit.

Safe per-service reason enum:
MALFORMED_SERVICE, UNEXPECTED_SERVICE_FIELD, INVALID_SERVICE_ID, UNSUPPORTED_SOURCE,
UNSUPPORTED_SERVICE_TYPE, SOURCE_ID_TYPE_MISMATCH, CONFLICTING_SERVICE_ID, MISSING_OWNER,
WEAK_OWNER, AMBIGUOUS_OWNER, MALFORMED_DEVICE, MALFORMED_MAC, OWNER_MAC_COLLISION,
OWNER_ID_MISMATCH. Whole errors are SNAPSHOT_INVALID, SNAPSHOT_DEVICE_INVALID,
SNAPSHOT_LIMIT_EXCEEDED, INVALID_SNAPSHOT_TIME, INVALID_EVALUATION_TIME,
INVALID_MAX_SNAPSHOT_AGE, SNAPSHOT_FUTURE, SNAPSHOT_STALE and ENVELOPE_INVALID.
Exceptions/rejections contain fixed codes only; no raw data or secret-bearing diagnostic messages.

## Closed private output and provenance

The private schema is governance/pe5/pe5-local-service-association-envelope.schema.json, closed at
all object levels. The library constructs the same schema without reading it. The eight envelope keys
are schema_version=1.0, inventory_updated, evaluated_at, max_snapshot_age_seconds,
association_count, service_associations, rejection_count and rejections.

Accepted edge fields are association_id, service_id, stable_device_id, service_type, source_type,
association_basis=existing_service_ownership, confidence=high and collection_provenance.
lsa_<SHA256> derives from the canonical existing service ID/owner/source tuple, excludes timestamps
and cannot replace device/service IDs. high describes verified reference ownership only, not health,
reachability, physical identity, availability or collector success.

Rejected fields are service_id (safe ID or null), reason, owner_reference (syntactically safe unconfirmed
source claim or null), source_type (systemd/ss only or null) and collection_provenance. Conflicting or
unsafe reference values are null, never first/last selection. Rejection references are not accepted owners.
Both accepted/rejected provenance contains normalized inventory_updated and inventory_snapshot_sha256.
The SHA is over canonical full JSON with top-level devices/services records sorted by canonical JSON;
object-key and top-level record reorderings therefore do not change output. Other snapshot changes,
including duplicate row counts, legitimately change the snapshot reference; deduplication leaves the
same accepted edge ID/cardinality, not a fabricated identical original snapshot. Raw snapshot byte hash
for future operator evidence is a separate capture hash. No per-service observed_at is invented.

Semantic validation enforces counts, unique accepted/rejected safe IDs, disjoint outcomes, stable edge
IDs, source/type/ID consistency, timestamp freshness, identical snapshot references, provenance timestamp
agreement and deterministic sorting. Owner membership/MAC authority is verified by the resolver against
its input; standalone envelope validation cannot authenticate an arbitrary claimed inventory snapshot.
The standalone validator never fetches state to pretend otherwise.

No raw MAC/IP/names/status/topics/HA IDs/Asset values/credentials are output. Nothing is projected
into public inventory, inventory/services or inventory/devices, MQTT, dashboards, incident/history
payloads or correlation. The existing seven inventory MQTT publications and PE-4 remain unchanged.

## Empty collections and side effects

Empty services yield zero accepted and zero rejected relationships only. The envelope has no collection
success, service-absence, health, outage or expected-availability assertion. Existing failed collectors
can return empty without a marker; source success remains UNKNOWN and cannot be recovered here.

There is no persistence or atomic writer; LKG/locking/restart persistence are not applicable to this pure
checkpoint and remain required for any later writer. Repeated identical explicit inputs produce identical
outputs. Tests deny filesystem/network/subprocess/clock/environment use at resolve and business I/O
at module initialization, and verify all input/protected fields unchanged. Artifact import itself is the
normal Python loader, not a resolver state/configuration read.

## Validation and candidate integrity

Focused synthetic tests cover positive systemd/ss, multiple services, normalization, duplicate/conflict
and malformed evidence, weak/IP/hostname/port-only rejection, ownership uniqueness, stale/future/exact
age boundary, timezone equivalence, invalid policy, closed schema, semantic counts, secret rejection,
provenance, ordering/re-run, resource bounds, input immutability and absence of side effects/integration.
The runtime engine, inventory identity functions, MQTT, private PE-4 producer/projection, Assets,
correlation, history and Home Assistant consumers are compared to the authorized baseline.

Current Master/architecture sequencing updates preserve their previous preparation state historically.
The preparation test now reads the immutable accepted f3730ba Git package for its historical assertions;
its historical validator body is unchanged. A current successor map owns this candidate's exact path set.
The shared PE-4 current-artifact map also overlays this exact successor map; its original historical source validation remains unchanged.
The candidate has ten paths: six new implementation/contract/test/document/record/schema artifacts
and four current sequencing/binding updates. Preparation and older PE-4/PE-10 records/schemas remain immutable. No test source gate is waived for
runtime changes. Candidate results/counts are supplied by the validation Evidence Report, not fabricated
inside this pre-regression document. Stop and diagnose any failure before considering a related repair.

## Production path, UNKNOWNs and STOP

No production validation was performed. Later separately authorized operator validation must establish
source publication/native compatibility, privately bind a finalized snapshot/capture, independently
approve maximum age, run this library offline on the bound copy, compare counts/deterministic hashes
and protected-state/public-topic invariants, and provide a sanitized Evidence Report. Missing policy,
source or native evidence is UNKNOWN/STOP. No raw state or credentials enter Git.

Actual broker/security/base, production collector activation/cadence, configured mapping authority and
retention, current eligible MAC-backed owners and production age policy remain UNKNOWN. They do
not justify changing collectors, TLS, configuration, credentials or identity. Empty/failure ambiguity,
open inventory object validation and heuristic dependencies remain acknowledged upstream limitations.

After focused/affected/full Windows regression and diff/integrity checks, STOP for independent review
and separate commit/push authorization. Runtime integration, persistence, MQTT mapping/Discovery,
remote service evidence, schedulers, deployment, public projection, dependency intelligence, PE-6 onward,
Active Discovery and surveillance are separate work. PE-5 as a whole is not closed by this library.
