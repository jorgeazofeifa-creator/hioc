# PE-1 Hostname Enrichment Evidence Report

Status: **REPOSITORY IMPLEMENTATION PASS - PRODUCTION VALIDATION PENDING**

## Repository baseline

Implementation began on clean branch `main` at approved commit
`6336cae31b466fb347ec92f79d2528391742da33`, equal to `origin/main`, with no
active Git operation. PE-0 was complete and design approved. PE-1 had not
started. No PI3, PI5, Home Assistant, or MQTT system was accessed.

## Implementation summary

PE-1 adds a closed, versioned, local hostname evidence envelope and independent
status artifact. It accepts only technical hostnames already acquired in the
current inventory cycle from known infrastructure, configured integrations,
the local collector, and DHCP. It preserves raw evidence, normalizes comparison
values, records agreement/conflict, selects deterministically, and retains at
most the immediately previous selected candidate for one successful generation.

The Inventory Engine remains the scheduler and identity owner. Central
reconciliation binds source records to the stable ID it already resolved. The
normal `discover_inventory` API remains unchanged unless the engine explicitly
requests a private transient evidence handoff. The engine removes this handoff
before public schema validation, JSON projections, events, and MQTT payload
construction. Enrichment executes after authoritative inventory writes and is
fail-open relative to inventory and publication.

## Files created

- `pi4/lib/hioc/enrichment.py`: normalization, eligibility, candidates,
  selection, conflict/confidence, bounded history, strict schema/status, prior
  validation, and isolated future-enricher registry.
- `pi4/bin/hioc-validate-enrichment.py`: sanitized artifact validator.
- `tests/test_hostname_enrichment.py`: PE-1 and protected-invariant coverage.
- This Evidence Report.

## Files modified

- `pi4/lib/hioc/inventory.py`: optional private stable-ID evidence binding.
- `pi4/bin/hioc-inventory-engine.py`: fail-open sidecar/status generation.
- `pi4/lib/hioc/core/state.py`: optional restrictive atomic-write mode and
  handled temporary cleanup; existing callers remain compatible.
- `pi4/validate_pi4.sh`: validates paired PE-1 artifacts when present.
- Directly affected architecture, roadmap, operations, reference, decision,
  specification, and changelog documentation.

No Home Assistant, dashboard, MQTT client/topic, incident, correlation,
topology, service discovery, operator metadata, identity comparator,
canonical-address comparator, retention, archival, expected-availability, or
Active Discovery file changed.

## Schema and source validation

The two closed version `1.0` validators enforce exact fields/types/enums, RFC
3339 timestamps, stable-ID/key equality, candidate content IDs, unique IDs,
deterministic ordering, selected-flag and conflict/status consistency, and
record/candidate/conflict counts. Unknown fields and versions fail. Runtime
validates before replacement; the standalone validator accepts valid pairs and
rejects malformed artifacts with sanitized output.

Tests prove all four approved sources and stable identifiers. `name`, ARP,
service, reverse-DNS/Active Discovery, MQTT, Home Assistant, ambiguous-source,
and unbound records cannot become candidates. DHCP paths become deterministic
12-hex source digests and do not appear in artifacts.

Normalization coverage includes empty/wildcard rejection; case, Unicode NFC,
IDNA, and trailing-dot agreement; `.lan`/`.local` preservation; FQDN/short-name
distinction; placeholders, IPs, MACs, generated/nonstandard names; invalid
characters, repeated labels, and length bounds. Raw/display/comparison values
remain distinct.

## Protected invariants

Regression tests compare reconciliation with and without evidence binding and
prove identical public devices, including stable ID, canonical IP, hostname,
`name`, `display_name`, health, observation status, device count, and aggregate
provenance. Engine tests prove:

- public `inventory.json` equals the authoritative input after only pre-existing
  private fields are removed;
- MQTT remains the seven existing inventory topics and contains no enrichment;
- failure preserves the previous envelope while inventory writes and MQTT
  publication continue;
- unavailable/degraded/error enrichment does not change device health;
- raw failure values do not enter logs;
- no topology, dependency, service ownership, dashboard, Home Assistant, or
  incident path is introduced;
- future enrichers receive isolated context copies and cannot mutate protected
  inventory objects.

Production invariant comparison remains pending controlled deployment.

## Determinism, lifecycle, and failure paths

Tests prove input-order independence, deterministic ties and duplicate collapse,
agreement, active conflict, historical disagreement, one-generation fallback,
device omission, empty/multiple-device output, and strict count validation. Two
engine runs over identical captured input produce byte-identical envelope bytes.

Malformed prior input is not repaired in place; current evidence can replace it
with a valid degraded result. Forced atomic replacement failure preserves the
previous file and cleans the temporary. Forced enrichment failure produces a
sanitized status where possible, preserves the last envelope, returns inventory
success, continues MQTT publication, and leaks no exception value. Missing
private evidence produces enrichment `unavailable`, never device-health state.

## Validation results

- PE-1 suite: **PASS**, 33 tests covering all approved matrix items.
- Full regression: **PASS**, 274 tests with 7 expected skips.
- Python compilation (`pi4`, `tests`): **PASS**.
- Release validation and all shell syntax: **PASS**. Git Bash was explicitly
  supplied on Windows; its environment lacked `python3`, while compilation had
  already passed with the bundled workspace interpreter.

The first full run found three environment-only errors because Bash was not
resolved. Rerunning the same complete suite with installed Git Bash passed; no
implementation correction was required for that environment issue.

## Performance

Ten-run in-process Windows repository benchmarks:

- 151 devices/candidates: median **4.012 ms**, maximum **7.552 ms**.
- 1,000 devices/candidates: median **33.395 ms**, maximum **37.426 ms**.

The focused suite enforces completion below two seconds for 1,000 devices. No
network I/O or source reread occurs. Production end-to-end timing is pending.

## Security and privacy

Sidecar and temporary writes request `0600`; the state directory is constrained
to `0750` maximum. POSIX mode behavior is tested where supported without
claiming Windows POSIX equivalence. Logs contain only status, sanitized codes,
and counts. Status contains no hostname/path. Fixtures are synthetic.
Production sidecars must never enter Git or unredacted reports.

## Deployment and repository result

No deployment occurred. Future authorized validation must prove exact approved
commit/artifact identity, supported deployment and backup, restrictive valid
sidecars, deterministic second-run behavior, real source capture, protected
pre/post invariants, unchanged consumers, bounded runtime, redaction, and
rollback availability under the approved
[PE-1 specification](PE1_HOSTNAME_ENRICHMENT_SPEC.md).

**PASS - IMPLEMENTED AND REPOSITORY VALIDATED; PRODUCTION PENDING.** This does
not authorize deployment, close production validation, or begin PE-2.
