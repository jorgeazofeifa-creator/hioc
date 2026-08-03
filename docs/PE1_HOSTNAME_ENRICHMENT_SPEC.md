# PE-1 Hostname Enrichment Evidence Envelope Specification

Status: **APPROVED SPECIFICATION - IMPLEMENTATION NOT STARTED**

PE-1 is a bounded Phase 7A implementation package. It records hostname
Observation evidence already acquired during an inventory cycle, evaluates it
in the Enrichment layer, and writes a local sidecar artifact. It does not
create Asset metadata and changes no public inventory or operational behavior.

## Purpose and exclusions

PE-1 answers: which technical hostname values did existing approved sources
supply for each resolved stable device identity, which value would the approved
Enrichment contract select, and where do current or immediately preceding
values disagree?

It is not friendly naming, Asset editing, Home Assistant ingestion, MQTT input,
reverse-DNS discovery, OUI enrichment, service discovery, expected
availability, dashboard presentation, incident generation, identity or
canonical-address selection, liveness, health, observation status, or
retention/archival policy.

## Current hostname path and source map

Current acquisition flows through `pi4/lib/hioc/inventory.py`. Records enter
`discover_inventory`, are grouped by `_record_key`, selected by
`_merge_record_values`/`_select_observed_value`, and receive stable IDs in
`merge_records`. Public presentation then sets `display_name` to `name`,
hostname, IP, or ID and overwrites `name` with that display value. The inventory
engine writes `inventory.json` and `devices.json`, publishes retained inventory
topics, and Home Assistant dashboards render `display_name`, `name`, and
optional hostname. PE-1 does not change this path.

| Source | Repository evidence and input | Current treatment | Time/source identity | PE-1 decision |
|---|---|---|---|---|
| Local collector | `discover_inventory`; `socket.gethostname()` -> local record `hostname` and `name` | `source=local_host`; strongest observed authority; can determine current hostname/name | No source observation time; stable ID `local_host` | Include only `hostname` as direct Observation; exclude duplicate `name` |
| Known infrastructure technical hostname | `_clean_known_record`, `known_infrastructure`, `append_known_infrastructure`; explicit `hostname` | Configured fact; can fill missing hostname but does not replace an observed hostname; exact-MAC association preferred | No observation time; `known_infrastructure` | Include explicit `hostname` as configured fact |
| Known infrastructure `name` | Same path; explicit `name` | Operator display metadata; wins `display_name` after valid association | No observation time | Exclude: it is not a technical hostname and belongs to future Asset naming |
| Configured integration hostname | `integration_inventory`; record `hostname` | `source=integration:<file-stem>`; trusted observed/configured input, above ARP/DHCP in generic selection; can influence hostname/name fallback | No source timestamp contract; current stable source includes file stem | Include explicit `hostname`; preserve current `integration:<stem>` identity |
| Configured integration `name` | `integration_inventory`; record `name` | Open metadata; can become public display name | No timestamp contract | Exclude: semantic meaning is not constrained to technical hostname |
| DHCP lease hostname | `_parse_dhcp_lease_line`, captured snapshot, `dhcp_lease_observations`; fourth dnsmasq field | `*` becomes empty; assignment-only; can fill missing hostname but cannot create liveness | Lease expiry is not observation time; `dhcp_leases` plus source path | Include nonempty hostname as assignment Observation; use redacted stable source instance |
| Retained inventory hostname | `merge_records(previous=inventory.json)` | Historical selected public value may persist with aggregate provenance | Existing first/last seen are device observation times, not hostname times | Do not bootstrap as evidence because field source is unprovable; only PE-1's prior selected candidate may supply bounded history |
| Neighbor/ARP | `_collect_neighbor_table` | Produces IP, MAC, state; repository collector does not produce hostname | Snapshot collection only; `arp_table` | Exclude: no implemented hostname value |
| Local service names | `LocalServiceDriver`, `build_services` | Service identity/presentation, not device hostname | `systemd`/`ss` | Exclude |
| Reverse DNS | `reverse_dns`; called only when `HIOC_INVENTORY_ACTIVE_DISCOVERY` is enabled | Active-discovery hostname fallback | Point-in-time query; no retained field provenance | Exclude; Active Discovery remains postponed |
| MQTT-originated name | No central inventory metadata subscriber found | MQTT publishes inventory; it is not a hostname input | None | Deferred/unavailable |
| Home Assistant name | No registry ingestion found | Home Assistant consumes inventory | None | Deferred/unavailable |
| Legacy pi4-tools | Separate network-probe/telemetry producers; no repository path into central hostname merge proved | External producer boundary | External | Exclude |

Repository tests already prove local/integration/DHCP/known merge authority,
collector-order independence, known-name display behavior, DHCP assignment-only
semantics, and dashboard consumption. PE-1 adds evidence-specific tests without
altering those results.

## Eligible sources and stable identifiers

Only technical `hostname` fields already present in the same inventory cycle
are eligible:

| Source | `source_id` | `source_type` | Authority | Confidence |
|---|---|---|---|---|
| Known infrastructure | `known_infrastructure` | `configured_infrastructure` | `configured_fact` | `authoritative` |
| Configured integration | existing `integration:<normalized-file-stem>` | `trusted_integration` | `trusted_enrichment` | `high` |
| Local collector | `local_host` | `direct_observation` | `strong_observation` | `high` |
| DHCP lease | `dhcp_leases:<12-hex SHA-256 of normalized source path>` | `assignment_observation` | `weak_observation` | `medium` for normal values, `low` for low-quality values |

The DHCP digest prevents internal paths from appearing in the artifact while
remaining stable across processing order. It is not a security hash or artifact
identity. Integration source IDs reuse the current repository convention; file
iteration is sorted and array position never enters identity. An empty or
unsafe integration stem is normalized to a deterministic 12-hex digest.

Configured technical hostname and configured display `name` remain distinct.
PE-1 never promotes `name` into hostname or Asset `friendly_name`.

## Artifact and schema

The approved paths are:

- `state/inventory/enrichment.json`: hostname evidence envelope.
- `state/inventory/enrichment_status.json`: PE-1 generation status only.

Both are local runtime state, excluded from Git and all MQTT payloads. The
artifact is keyed by the existing stable device ID:

```json
{
  "schema_version": "1.0",
  "generated_at": "2026-08-03T12:00:00-06:00",
  "generator": "hioc-inventory-engine",
  "record_count": 1,
  "candidate_count": 0,
  "conflict_count": 0,
  "records": {
    "dev_0123456789abcdef": {
      "device_id": "dev_0123456789abcdef",
      "hostname": {
        "selected_candidate_id": null,
        "candidates": [],
        "conflict": false,
        "evidence_status": "no_evidence",
        "selection_rule": "no_valid_candidate"
      }
    }
  }
}
```

Top-level fields are required and closed for version `1.0`:

- `schema_version`: exact string `1.0`.
- `generated_at`: valid RFC 3339 timestamp for this generation attempt.
- `generator`: exact string `hioc-inventory-engine`.
- `record_count`: nonnegative integer equal to `len(records)`.
- `candidate_count`: nonnegative integer equal to all candidate entries.
- `conflict_count`: nonnegative integer equal to hostname envelopes whose
  `conflict` is true.
- `records`: object sorted by stable device ID. Every current resolved device
  has one entry, including devices with no eligible hostname evidence.

Each record is closed and contains:

- `device_id`: exact match for its object key.
- `hostname.selected_candidate_id`: candidate ID or JSON `null`.
- `hostname.candidates`: deterministically sorted candidate array.
- `hostname.conflict`: Boolean active-conflict indicator.
- `hostname.evidence_status`: `selected`, `selected_with_agreement`,
  `selected_with_conflict`, `no_valid_candidate`, or `no_evidence`.
- `hostname.selection_rule`: `configured_fact`, `trusted_integration`,
  `local_host`, `active_dhcp`, `source_agreement`, `historical_fallback`, or
  `no_valid_candidate`.

Each candidate is closed and contains:

- `candidate_id`: `hce_` plus the first 20 hex characters of SHA-256 over the
  canonical JSON tuple `(device_id, "hostname", normalized_value, source_id,
  state)`.
- `raw_value`: original source string after JSON decoding; never rewritten.
- `display_value`: Unicode-NFC, outer-whitespace-trimmed value with terminal
  absolute dot removed; intended only for future diagnostics.
- `normalized_value`: deterministic comparison value.
- `source_id`: stable identifier above.
- `source_type`: one of the four approved types above, or `historical` for the
  bounded previous selection.
- `source_reference`: sanitized integration stem, DHCP source digest, or JSON
  `null`; never a full file path.
- `authority`: `configured_fact`, `trusted_enrichment`,
  `strong_observation`, `weak_observation`, or `historical`.
- `confidence`: `authoritative`, `high`, `medium`, `low`, or `unknown`.
- `quality`: `normal`, `low`, `placeholder`, or `invalid`.
- `selectable`: Boolean.
- `observed_at`: RFC 3339 or `null`; PE-1 sources currently use `null` because
  none supplies a truthful hostname-observation timestamp.
- `first_available_at`, `last_available_at`: required RFC 3339 snapshot
  availability times maintained by PE-1. They are not source observation time.
- `state`: `active` or `historical`.
- `selected`: Boolean; exactly one candidate matches the selected ID, or none.
- `conflict_status`: `none`, `agreement`, `active_conflict`, or
  `historical_disagreement`.
- `derivation_rule`: `hostname_normalization_v1` for normalized candidates;
  it never claims the hostname itself was derived.

Candidates sort by normalized value, descending source-authority rank, source
ID, state, then candidate ID. JSON objects serialize with sorted keys. Counts
and selected flags are validated, not trusted from callers.

## Normalization and quality contract

PE-1 preserves `raw_value` and derives two separate values:

1. `display_value`: apply Unicode NFC, trim leading/trailing Unicode
   whitespace, and remove terminal dots that only mark an absolute DNS name.
   Preserve original case and suffix otherwise.
2. `normalized_value`: Unicode NFC followed by IDNA conversion per label when
   valid, ASCII lowercase, and no terminal dot. Case-only, Unicode-equivalent,
   IDNA-equivalent, and trailing-dot differences therefore agree.

PE-1 does **not** strip `.local`, `.lan`, or any other suffix. A short hostname
and an FQDN are distinct normalized values and active candidates conflict.
Suffix relationships may be modeled later; PE-1 does not guess search domains.

Normal DNS form permits total ASCII length 1-253, labels 1-63, letters, digits,
and interior hyphens, with no leading/trailing hyphen or empty/repeated labels.
Values using underscores are retained as nonstandard low-quality evidence with
deterministic ASCII-lower normalization. Spaces, controls, invalid IDNA,
invalid/repeated separators, or excessive lengths are retained as `invalid`,
nonselectable evidence when a nonempty source value exists.

Value handling is:

| Input class | Treatment |
|---|---|
| JSON null, empty/whitespace, `*` | Reject; no candidate |
| `unknown`, `localhost`, `localhost.localdomain` | Retain as `placeholder`, nonselectable, low confidence |
| IPv4/IPv6 literal or exact MAC address | Retain as `placeholder`, nonselectable, low confidence |
| Direct MAC-derived placeholder | Retain as `placeholder`, nonselectable when normalized value is only the MAC with separators removed or a fixed `mac-`/`device-` prefix plus the full MAC |
| Common generated names such as `android-<suffix>`, `ESP_<suffix>`, `DESKTOP-<suffix>` | Retain as `low`, selectable; ugliness does not erase real evidence |
| Generic vendor defaults | Retain as `low`, selectable when syntactically usable; PE-1 has no vendor dictionary and must not guess beyond documented patterns |
| Valid Unicode/IDNA hostname | Retain as `normal`, selectable with ASCII comparison value and Unicode display value |
| Other syntactically invalid nonempty value | Retain as `invalid`, nonselectable |

The documented low/placeholder pattern list is versioned with
`hostname_normalization_v1`. Adding patterns is an implementation-contract
change requiring tests; environment-specific values are not hardcoded.

## Authority, selection, conflict, and confidence

Selection is field-specific and independent of current public hostname choice:

1. active selectable configured infrastructure hostname;
2. active selectable configured-integration hostname;
3. active selectable local-host hostname;
4. active selectable DHCP hostname;
5. immediately previous selected candidate as historical fallback.

Within one authority class: active beats historical; `normal` beats `low`;
higher categorical confidence wins; comparable truthful `last_available_at`
breaks ties; normalized value, source ID, and candidate ID provide ascending
lexical final ties. DHCP lease expiry is not hostname recency. Input, file, and
dictionary order never participate.

When two or more active sources have the same normalized value they are source
agreement, not conflict. If the winning normalized value has agreement and no
other active selectable normalized value exists, `selection_rule` is
`source_agreement`. Otherwise the winning authority determines the rule.

An active conflict exists when two or more distinct normalized values are
active and selectable, even when one source has higher authority. Losing active
candidates are marked `active_conflict`; the selected candidate is also marked
`active_conflict`. Nonselectable placeholders/invalid values do not create an
active conflict. A historical candidate different from all active values is
`historical_disagreement`, not an active conflict. Multiple DHCP names are
active conflicts only when present in the same captured cycle; a prior selected
DHCP name is historical disagreement on the next cycle.

Confidence and authority remain separate. Configured infrastructure is
`authoritative`; integration and local host are `high`; normal DHCP is
`medium`; low-quality values are capped at `low`; placeholders/invalid and
historical fallback are `low` or `unknown`. Agreement may support
`selection_rule=source_agreement` but does not elevate authority or confidence.
No candidate affects identity, health, or incidents.

## Persistence, status, and failure policy

The existing inventory engine remains the sole scheduler and lock owner. After
identity resolution, it invokes a library function using the already acquired
cycle records and resolved devices. No source is reread and no cron job is
added.

`enrichment.json` is a bounded two-generation view:

- all active candidates for devices present in the resolved inventory;
- at most the immediately previous selected candidate when it is absent from
  the current cycle;
- no prior nonselected candidates;
- the historical candidate survives one successful generation only unless it
  becomes active or selected again;
- entries disappear when their stable device is absent from resolved inventory;
  this is snapshot omission, not Asset retirement or evidence erasure policy.

This provides transition evidence without inventing permanent retention or
unbounded growth. Empty inventory produces a valid zero-count artifact. A
device with no candidates receives `selected=null`, empty candidates,
`conflict=false`, `no_evidence`, and `no_valid_candidate`.

A malformed/mismatched prior envelope is ignored for historical continuity;
current evidence still produces a valid artifact and status `degraded` with
sanitized code `prior_artifact_invalid`. File modification time is never used
as evidence time.

Both files use `StateStore`-style same-directory temporary write and atomic
replace. Implementation must validate before replacement, remove no last-valid
artifact on failure, create `state/inventory` as owner-only writable directory
(`0750` maximum), and enforce file mode `0600` after replacement. Temporary
files receive the same restrictive mode and are cleaned on handled failure.

`enrichment_status.json` is closed version `1.0` with: `schema_version`,
`updated`, `status` (`online`, `degraded`, or `error`), `record_count`,
`candidate_count`, `conflict_count`, `generator`, and nullable sanitized
`error_code`. `unavailable` is a consumer interpretation when no status exists,
not a written state. It contains no hostname values, source paths, exception
text, or stack traces.

Enrichment is fail-open relative to authoritative inventory. Inventory is
resolved and its normal artifacts/publication remain authoritative. A PE-1
failure logs a sanitized error code, atomically writes `status=error`, leaves
the last valid enrichment artifact untouched, and does not fail inventory,
publish a device-health event, or create an incident. Inventory failure remains
governed by existing behavior and prevents a new enrichment generation.

## Engine and module architecture

Use a new library module, `pi4/lib/hioc/enrichment.py`, called from
`discover_inventory` after identity resolution but while the cycle's source
records remain available. Its public boundaries are conceptually:

- `collect_hostname_candidates(records, resolved_devices, generated_at)`:
  extract only approved technical hostname fields and bind candidates to the
  resolved stable identity without performing identity matching of its own.
- `build_hostname_envelope(resolved_devices, candidates, previous_envelope,
  generated_at)`: normalize, select, preserve bounded history, count, and
  validate a deterministic document.
- `validate_hostname_envelope(payload)`: closed version-aware structural and
  cross-field validation.
- `hostname_status(...)`: produce sanitized independent status.

The central inventory code remains the only owner of record-to-device identity.
The enrichment module receives an explicit mapping established during current
reconciliation and must reject unbound evidence rather than match by hostname,
IP, or name. It never calls network, filesystem source, MQTT, or Home Assistant
APIs.

For the smallest change compatible with current `_capabilities` precedent,
`discover_inventory` may return private transient `_enrichment` or
`_enrichment_error` data. `hioc-inventory-engine.py` must pop it before schema
validation, events, JSON projections, comparison, or MQTT payload construction.
The enrichment exception boundary must not wrap or weaken authoritative
inventory failures.

Scheduling remains the existing inventory cron and lock. Expected runtime is
linear in device/candidate count, with no network I/O and a bounded candidate
set. Production validation treats a sustained increase above 20% of the
baseline inventory-engine duration or 2 seconds, whichever is larger, as an
unbounded regression requiring investigation and normally rollback.

## File and module plan

Expected implementation changes are:

- `pi4/lib/hioc/enrichment.py` (new): normalization, candidates, selection,
  lifecycle, validation, status.
- `pi4/lib/hioc/inventory.py`: pass already acquired source records and their
  resolved identity binding to the enrichment module; no public field logic
  changes.
- `pi4/bin/hioc-inventory-engine.py`: read previous sidecar, strip transient
  data, atomically write sidecar/status after authoritative inventory, and keep
  enrichment failure isolated.
- `pi4/lib/hioc/core/state.py`: only if necessary to support explicit mode and
  validated atomic replacement without changing existing callers.
- `pi4/lib/hioc/core/schemas.py` or a dedicated validator in `enrichment.py`:
  register closed version-aware validation; do not loosen public schemas.
- `pi4/validate_pi4.sh`: validate optional PE-1 artifacts when present and
  reject malformed/current-version documents without making absence a legacy
  install failure before PE-1 deployment.
- installer/release validation: include the new tracked module and preserve
  runtime-state boundaries; no configuration or cron change.
- `tests/test_hostname_enrichment.py` (new) plus focused inventory/engine,
  release, validator, and public-payload regression tests.
- documentation listed below and a new PE-1 Evidence Report during
  implementation/production closure.

No Home Assistant, dashboard, MQTT client/topic, incident, correlation,
topology, service ownership, or configuration-template file should change.

## Schema and compatibility validation

Use the repository's Python validation approach rather than adding a JSON
Schema dependency solely for PE-1. The version-aware validator is strict for
known version `1.0`: required fields, exact types/enums, timestamp parsing,
stable-ID/key agreement, unique candidate IDs, deterministic ordering, count
agreement, selected-flag agreement, conflict/evidence-status consistency, and
no unknown fields. Future versions require an explicit validator and migration
decision; they are not silently accepted.

Runtime validates before atomic replacement. The PI4 validator validates both
artifacts if PE-1 is installed. A malformed artifact leaves the last valid file
in place when generated, reports sanitized status, and never becomes public
inventory. Upgrade/installer logic treats these as runtime-generated files and
does not overwrite or back them up as source artifacts; normal release rollback
restores code, while the PE-1 rollback procedure may quarantine the sidecars.

Semantic or byte comparison must prove existing `inventory.json`,
`devices.json`, MQTT payload construction, names, hostnames, IDs, IPs, health,
observation status, topology, dependencies, and service ownership are unchanged
for identical captured inputs except existing generation timestamps.

## Required test matrix

Implementation must cover all of the following:

1. One valid DHCP hostname candidate.
2. One known-infrastructure technical hostname.
3. One configured-integration hostname.
4. One local-host hostname.
5. Same normalized value from multiple sources and agreement.
6. Case-only agreement.
7. Trailing-dot agreement.
8. FQDN versus short-name active conflict.
9. `.lan` preserved and distinct.
10. `.local` preserved and distinct.
11. Empty value rejected.
12. Wildcard `*` rejected.
13. `unknown` retained nonselectable.
14. Raw IPv4 and IPv6 retained nonselectable.
15. Exact/direct MAC placeholder retained nonselectable.
16. Generic generated/vendor name retained at low quality.
17. Unicode NFC and IDNA equivalence.
18. Invalid characters, repeated separators, label and total-length limits.
19. Multiple active conflicting candidates.
20. Active candidate versus one-generation historical candidate.
21. Equal-authority deterministic tie-break.
22. All relevant input-order permutations.
23. Missing source timestamps remain null; availability times remain distinct.
24. Duplicate candidate records deduplicate deterministically.
25. Device with no hostname candidates.
26. Device absent from resolved inventory is omitted without retirement claim.
27. Stable device ID and record-key agreement.
28. Canonical IP unchanged.
29. Public inventory `name` unchanged.
30. Public inventory hostname unchanged.
31. Health/liveness fields unchanged.
32. Observation status/age unchanged.
33. Public inventory JSON semantic compatibility and timestamp-normalized byte
    compatibility.
34. MQTT topic set and payload values unchanged.
35. Conflict count validation.
36. Candidate/record count validation.
37. Online and degraded status documents.
38. Atomic-write failure leaves last valid artifact and writes sanitized error
    status where possible.
39. Malformed/version-mismatched prior envelope is ignored with degraded status.
40. Empty inventory produces valid zero-count artifacts.
41. Multiple assets sort and serialize deterministically.
42. No credentials, paths, or real household values leak.
43. Repeated identical input produces deterministic content apart from approved
    generation/availability timestamps; normalized comparison is deterministic.
44. Strict schema, enums, unknown-field rejection, and cross-field validation.
45. Full inventory and complete regression suites.

Negative tests must prove that `name`, service names, ARP rows, reverse DNS,
MQTT, Home Assistant, and unbound evidence do not become candidates.

## Deployment and production validation

PE-1 uses the supported release deployment; it adds no cron entry, service,
configuration source, MQTT topic, or Home Assistant change. The implementation
checkpoint must create `docs/PE1_HOSTNAME_ENRICHMENT_EVIDENCE.md` following
existing Evidence Report conventions.

Future operator evidence, without embedding a command in this specification,
must capture:

- clean exact approved source commit and Git-derived identities for every
  changed executable artifact;
- supported deployment and rollback backup identity;
- pre/post inventory artifacts with timestamps normalized for comparison;
- stable device count, IDs, MAC identity, canonical IP, aggregate provenance,
  hostname, name, display name, health/liveness/observation fields, topology
  IDs, and service ownership invariants;
- valid sidecar/status schema, restrictive modes, stable device keys, correct
  counts, eligible real source IDs, deterministic selection, conflict and
  agreement preservation, and no full DHCP paths;
- a second controlled inventory run showing deterministic selection and bounded
  lifecycle behavior;
- unchanged MQTT topic/payload contract, with no enrichment publication;
- no Home Assistant, dashboard, incident, or configuration changes;
- secret-pattern/redaction review and bounded runtime comparison;
- deployed source/runtime artifact equality and available rollback backup.

Outcomes:

- **PASS:** deployment identity and every protected invariant pass; valid
  sidecars/status are produced; selection follows the contract. A production
  conflict is not required, and devices with no eligible hostname evidence are
  valid zero-candidate records.
- **PARTIAL PASS:** authoritative inventory and protected invariants pass, but
  a required validation observation is unavailable or inconclusive, such as a
  second controlled generation not completing or a configured source expected
  to exercise its adapter being unavailable. No rollback is recommended solely
  for these conditions; follow-up evidence is required.
- **FAIL:** deterministic implementation, artifact, invariant, privacy, or
  runtime-isolation failure. Rollback is recommended.

## Rollback and stopping conditions

Recommend rollback for broken/blocked inventory generation, unexpected public
schema or MQTT change, changed stable IDs/canonical IP/hostname/name/display
name/health/liveness/observation status, malformed newly generated sidecar,
validator failure, Git/source/runtime mismatch, secret/path exposure,
unbounded runtime regression, failed atomic isolation, or enrichment failure
that prevents normal inventory operation.

Do not recommend rollback because production has no conflict, a device has no
evidence, low-confidence values appear, a syntactically unattractive value wins
the approved deterministic contract, or optional observational evidence is
inconclusive.

Implementation must stop for new-source ingestion, need to change current
hostname/name/display behavior, identity/canonical/liveness/health semantics,
public schema/MQTT/dashboard/incident scope, permanent retention, Asset editing,
or any architectural ambiguity not resolved here. Those require separate
approval rather than scope expansion.

## Security and documentation requirements

Production sidecars contain private hostnames, stable IDs, sources, timestamps,
and conflicts. Directory mode is at most `0750`; files and temporary files are
`0600`. Raw hostname evidence never appears in routine logs, status, MQTT,
notifications, dashboards, or committed Evidence Reports. Logs contain only
sanitized codes and counts. Evidence Reports use aggregate counts, source-type
labels, approved synthetic examples, and redacted/hash identifiers when a
specific record is necessary. Production sidecars are never committed to Git.
Fixtures use synthetic names, addresses, IDs, and paths and contain no household
metadata or credentials.

Implementation and closure documentation updates:

- this specification and `PASSIVE_ENRICHMENT_ARCHITECTURE.md`;
- `HIOC_MASTER_PLAN.md`, `SYSTEM_REFERENCE.md`, `OPERATIONS.md`,
  `CHANGELOG.md`, and `DECISIONS.md`;
- new `PE1_HOSTNAME_ENRICHMENT_EVIDENCE.md` containing repository,
  deployment, production, invariant, privacy, runtime, and rollback evidence.

PE-1 remains **NOT STARTED** until a separate implementation authorization.
