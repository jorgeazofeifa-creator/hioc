# PE-3 Manufacturer Reference Enrichment Specification

Status: **PE-3.0 ARCHITECTURE DEFINED; PE-3.1 IMPLEMENTATION DESIGN APPROVED; EXECUTABLE NOT STARTED**

## Purpose and boundary

PE-3 adds reproducible, offline manufacturer-reference knowledge to existing
stable devices. It helps an operator interpret otherwise opaque MAC evidence,
explain lookup provenance, and prepare later descriptive enrichment. It does not
identify a physical device, prove ownership, classify device function, or prove
that an organization manufactured the final product rather than an interface or
module.

Manufacturer information is descriptive **Enrichment** only. It cannot affect
stable identity, canonical address, inventory membership, liveness, health,
incidents, expected availability, Asset ownership, topology, service ownership,
dependencies, MQTT, Home Assistant, dashboards, notifications, or automation.
PE-3.0 changes no schema or runtime behavior.

## Dataset evaluation

| Candidate | Authority and coverage | License / redistribution | Maintenance and reproducibility | Decision |
| --- | --- | --- | --- | --- |
| IEEE Registration Authority public listings | Primary assignment authority; publishes MA-L/OUI, MA-M, MA-S/OUI-36, CID and related public registries; UTF-8 CSV/text downloads | Public download is explicit, but the public pages do not state a standalone open-data redistribution license. Repository vendoring or release redistribution therefore requires a recorded terms review and approval. | Registry owner; public listings are updated regularly and can be acquired offline, hashed and pinned. | **Selected authoritative upstream, subject to the license gate.** |
| Wireshark `manuf` | Composite of IEEE and community/legacy sources; supports variable prefix lengths and well-known addresses; collisions prefer Wireshark, then legacy data, then IEEE | File declares `GPL-2.0-or-later`; redistribution must preserve applicable GPL obligations. | Actively maintained and pinnable by repository commit, but composite corrections are not identical to registration authority. | Approved only as a future comparison/input candidate, never the PE-3 authority without a new decision. |
| `nmap-mac-prefixes` | Practical 24-bit vendor map distributed with Nmap | Nmap Public Source License adds redistribution and embedded-product restrictions; OEM rights may be required in some distributions. | Release-pinnable and offline, but narrower than current IEEE block sizes and coupled to Nmap releases. | Rejected for PE-3 authority. |
| Online lookup services or scraped mirrors | Variable, often derived from IEEE | Terms, attribution, freshness and availability vary | Not reproducible; introduces network disclosure and runtime dependency | Prohibited. |

Primary references:

- [IEEE Registration Authority public listing](https://standards.ieee.org/products-programs/regauth/)
- [IEEE MA-L/OUI definition](https://standards.ieee.org/products-programs/regauth/oui/)
- [IEEE EUI/OUI/CID guidance](https://standards.ieee.org/wp-content/uploads/import/documents/tutorials/eui.pdf)
- [Wireshark repository and licensing](https://gitlab.com/wireshark/wireshark/)
- [Wireshark `manuf` provenance and precedence](https://gitlab.com/wireshark/wireshark/-/blob/master/manuf)
- [Nmap public-source license](https://nmap.org/npsl/)
- [Nmap MAC prefix data description](https://nmap.org/book/nmap-mac-prefixes.html)

No dataset is approved for download, commit, distribution or production use in
PE-3.0. Before PE-3.1 executable work, governance must record the IEEE terms reviewed, reviewer,
date, permitted repository/release use, attribution, and any redistribution
conditions. Failure to obtain approval stops implementation and may trigger a
new source-selection decision; it never permits silent substitution.

## Dataset artifact governance

The future source artifact is a complete, immutable snapshot of the approved
IEEE public assignment registries needed for MA-L, MA-M and MA-S/OUI-36 lookup.
CID is retained only for explicit non-manufacturer/private classification and
must not be mislabeled as an EUI manufacturer match.

Each approved snapshot must have a closed manifest containing:

- schema version;
- upstream name and canonical HTTPS URLs;
- retrieval UTC timestamp and upstream metadata where available;
- exact source filenames, byte sizes and SHA-256 values;
- normalized derived-artifact SHA-256;
- record counts by registry and prefix length;
- duplicate/conflict counts and deterministic resolution report;
- license identifier, notice path, review decision and approval reference;
- parser version and source Git commit;
- dataset version label derived from immutable evidence, never only “latest”.

The PE-3.1 design supersedes the conceptual repository reservation with the
private runtime path and single configuration key defined in
[PE3_MANUFACTURER_IMPLEMENTATION_DESIGN.md](PE3_MANUFACTURER_IMPLEMENTATION_DESIGN.md).
No repository dataset path is approved. Runtime must use only a governed,
checksum-verified injected snapshot; it must never fetch data. Builds operate
from pinned bytes and reproduce the same normalized artifact on Windows and Linux.

Updates are separate reviewed commits. The updater, if later authorized, runs
outside production, downloads to a temporary location, verifies transport and
format, produces a semantic diff and license review, and requires explicit
approval. Production never auto-updates. Rollback selects the previous complete
manifest/artifact pair through supported deployment; partial mixing is forbidden.
Replacing IEEE or adding a second source requires a new architecture decision,
mapping and confidence review, migration plan, compatibility tests and production
approval.

## Deterministic lookup contract

1. Accept only an already-resolved device MAC supplied by authoritative inventory
   identity processing. PE-3 never chooses or reconciles MAC identity.
2. Parse supported EUI-48 forms by removing only approved separators (`:`, `-`,
   or dotted groups), requiring exactly 12 hexadecimal digits, and canonicalize
   to uppercase colon-delimited octets.
3. EUI-64 is accepted only when a future schema explicitly supplies a genuine
   64-bit identifier. Do not infer an EUI-48 by removing `FF:FE`; modified EUI-64
   construction is not reliable manufacturer proof. Native EUI-64 lookup uses
   only an allocation type explicitly supported by the pinned registry.
4. Reject empty, malformed, all-zero, broadcast and multicast addresses before
   lookup. Multicast/group addresses are never manufacturer evidence.
5. If the local-admin bit is set, return `locally_administered`; do not look
   through it, clear the bit, or claim the apparent global prefix. This covers
   randomized Wi-Fi, virtual interfaces, containers and many hypervisors.
6. IEEE entries marked private produce `private_assignment`, not an organization
   guess. CID matches produce `company_identifier`, not manufacturer.
7. For a globally administered address, match the longest valid approved prefix:
   MA-S/OUI-36 before MA-M before MA-L/OUI. A shorter match cannot override a
   longer one.
8. Exact duplicate prefix/value rows normalize to one result. Conflicting rows
   within a supposedly valid snapshot make the dataset invalid; runtime does not
   choose arbitrarily.
9. No match returns `unknown`, preserving normalized input class and provenance
   without fabricating a name.
10. Lookup order, Unicode normalization, whitespace handling and output ordering
    are fixed and locale-independent. No DNS, web API, network scan, system OUI
    database, Wireshark installation or Nmap installation may influence output.

## Enrichment model

PE-3.1 has frozen a closed private sidecar schema in
[PE3_MANUFACTURER_IMPLEMENTATION_DESIGN.md](PE3_MANUFACTURER_IMPLEMENTATION_DESIGN.md).
The conceptual fields below remain the architecture basis; no existing schema
or runtime has been modified:

| Field | Meaning |
| --- | --- |
| `stable_device_id` | Reference to existing identity; never created by PE-3 |
| `manufacturer` | Exact display organization from the selected dataset, nullable |
| `organization` | Optional normalized full organization label, if distinct and approved |
| `vendor` | Compatibility alias is discouraged; if later required, it must be defined once rather than diverging from manufacturer |
| `lookup_status` | Closed result such as matched, unknown, private assignment, locally administered, multicast, invalid or unavailable |
| `assignment_type` | MA-L, MA-M, MA-S/OUI-36, CID or none |
| `matched_prefix_length` | 24, 28, 36 or other explicitly approved length |
| `source` | Stable dataset source identifier |
| `dataset_version` | Pinned immutable version label |
| `dataset_sha256` | Identity of the normalized reference artifact |
| `lookup_method` | Closed deterministic algorithm version |
| `normalization` | Closed MAC normalization method/version |
| `confidence` | Manufacturer-reference confidence only |
| `looked_up_at` | Generation timestamp; excluded from semantic selection/equality where appropriate |
| `provenance` | Sanitized structured source, match and status facts |

Raw dataset addresses, assignee street/contact details and unused upstream fields
must not enter enrichment. The sidecar must be keyed by existing stable device ID,
written atomically and privately, and remain separate from Observation and Asset.
Missing manufacturer is a valid result, not an inventory error.

## Confidence model

| Confidence | Manufacturer meaning |
| --- | --- |
| `authoritative` | Reserved for a future explicit operator Asset override or trusted integration assertion with field authority; IEEE prefix lookup alone does not reach this level |
| `high` | Current pinned IEEE globally administered longest-prefix match with valid artifact identity |
| `medium` | Future trusted integration corroboration or an older approved dataset under a documented stale policy; exact rule requires later approval |
| `low` | Ambiguous legacy/community evidence retained only for explanation and normally nonselectable |
| `unknown` | No usable manufacturer conclusion: unknown, private, local-admin, multicast, invalid or unavailable |

This confidence describes only “which organization owns the matched assignment.”
It is independent of identity confidence, canonical-address confidence and future
PE-6 classification confidence. A high-confidence OUI match can coexist with an
unknown device type and cannot strengthen liveness or health.

## Provenance and unknown handling

Every result, including failure, records the source identifier, pinned dataset
version/digest, algorithm and normalization versions, assignment class, lookup
status, match length when safe, and generation time. It must not copy the full
MAC into routine status or logs.

Unknown, private and locally administered results remain explicit and stable.
Custom hardware is not guessed. A future operator manufacturer override belongs
in Asset because it expresses durable operator knowledge; it must preserve the
reference result as separate provenance. PE-3 does not implement overrides.

Future conflicts retain candidates rather than overwrite history. Field authority
order is future explicit Asset override, future trusted integration assertion,
then pinned IEEE reference. Dataset updates may correct a label but cannot rewrite
identity or silently erase the previous dataset/version evidence. Multiple source
support requires deterministic source priority and conflict representation in a
new approved contract.

## Storage architecture and privacy

Manufacturer reference is **Enrichment**: it is derived reproducibly from an
Observation/identity MAC plus a reference dataset. It is not Observation because
the organization was not directly observed, and it is not Asset because it is not
operator intent. Future overrides are Asset facts and remain separately sourced.

The eventual private PE-3 sidecar must extend the enrichment layer rather than
public inventory or `assets.json`. Schema evolution must be closed, versioned and
forward-incompatible by default until an explicit migration exists. PE-1 sidecars
and PE-2 stores remain unchanged.

An organization label and assignment class are generally low sensitivity, but
the input MAC, stable device ID, household inventory, match failures, custom
labels, dataset contact/address fields and correlations remain private. PE-3.1
starts local-only and deny-by-default. No MQTT, Home Assistant, dashboard, log or
public inventory publication is approved. A later publication decision may expose
only selected manufacturer label/status with minimization, schema/version review,
and proof that raw identifiers or private Asset data cannot leak.

## Protected invariants

PE-3 implementation and dataset updates must prove no change to:

- stable IDs, MAC reconciliation or identity events;
- canonical IP selection or address history;
- inventory device count or membership;
- observation, liveness, health or expected availability;
- incidents, history, summaries or notifications;
- Asset records, revisions, backups or authority;
- public inventory and established MQTT contracts;
- Home Assistant entities, packages or contracts;
- dashboards or presentation contracts;
- topology, service ownership or dependency graph;
- schedules, locks or existing PE-1/PE-2 retention semantics.

Manufacturer output cannot be consumed by these systems in PE-3.

## Performance and caching

On PI3-class hardware, reference load and validation target is at most 500 ms per
inventory generation, lookup target is at most 1 ms median and 5 ms p95 per MAC,
and total PE-3 work for 500 devices is at most 1 second after file cache warm-up.
Peak additional resident memory target is 32 MiB and normalized artifact target
is 10 MiB unless PE-3.1 evidence justifies a reviewed bound.

Load once per inventory process, index immutable prefixes by length, and perform
O(1)-style map lookup for each approved prefix length. Do not maintain a daemon,
write per-device caches, use unbounded memoization, or share mutable cache state.
The pinned artifact checksum/version is the cache key. These are design targets,
not measurements.

## Failure isolation

Missing dataset, missing manifest, checksum mismatch, corrupt JSON/CSV, unsupported
schema/version, duplicate conflict, invalid encoding, permission failure, parser
failure, lookup exception or failed update makes PE-3 unavailable/degraded in a
sanitized private status. Inventory generation remains fail-open and continues
without new manufacturer enrichment. The last valid sidecar may be preserved but
must be marked with its own dataset version and freshness; invalid new output
must never replace it.

Update failure leaves the approved current artifact untouched. No fallback to an
unpinned system database, secondary dataset or online query is allowed. Dataset
or enrichment failure cannot recommend production rollback unless the deployed
PE-3 change deterministically breaks a protected invariant. A corrupt or
mislicensed new artifact justifies reverting the PE-3 artifact/code release, not
altering identity or Asset state.

## Relationships to later checkpoints

- **PE-6 classification:** manufacturer answers “What organization owns the
  address assignment?” or colloquially “What built the interface?” Classification
  answers “What is the device?” Manufacturer never deterministically supplies
  category, role, criticality or device type.
- **PE-2 Asset:** reference manufacturer is derived Enrichment. Future operator
  correction is durable Asset knowledge, separately authoritative and
  provenance-preserving. PE-3 implements no override.
- **PE-4 Home Assistant association:** a future read-only registry adapter may
  contribute an independent manufacturer assertion and raise field confidence
  under an approved authority rule. It cannot retroactively make an OUI identity
  evidence or infer availability.
- **PE-5:** passive service/MQTT association cannot override manufacturer merely
  because a service name resembles a vendor.

PE-4 through PE-9 definitions remain unchanged and are not started.

## Production validation plan

PE-3.1 must first pass repository review of license approval, pinned raw and
normalized artifact manifests, Git-object identity, parser determinism, schema,
privacy, failure isolation, performance targets, packaging, deployment and
rollback. Dataset generation must reproduce byte-identical normalized output from
the same pinned sources in isolated environments.

Governed production validation must capture pre-state, verify target/repository,
deploy through the supported release path only after authorization, verify source
and runtime hashes/modes, validate dataset and parser identity offline, execute a
bounded lookup corpus, run inventory once, compare protected invariants, measure
time/memory, scan all outputs for prohibited identifiers, and produce a sanitized
Evidence Report. Manufacturer changes must be bounded and explainable by matched
prefixes; inventory and operational contracts must remain identical.

Rollback is justified only by deterministic PE-3 artifact/code mismatch,
unsupported/corrupt dataset accepted as valid, nondeterminism, privacy leakage,
performance outside approved hard bounds, failure to remain fail-open, licensing
violation, or protected-invariant regression caused by PE-3. Unknown vendors,
local-admin results, normal dataset corrections and absence of optional matches
are not rollback conditions.

## PE-3.0 architecture test matrix

These 64 architecture cases established the minimum scope. The PE-3.1 design
refines them into the binding 76-test executable plan; where grouping or exact
schema behavior differs, the implementation design controls.

| # | Area | Case and expected result |
| ---: | --- | --- |
| 1 | Normalization | Uppercase colon EUI-48 normalizes identically |
| 2 | Normalization | Lowercase colon form normalizes identically |
| 3 | Normalization | Hyphen form normalizes identically |
| 4 | Normalization | Approved dotted form normalizes identically |
| 5 | Normalization | Bare 12-hex form behavior is explicitly fixed and tested |
| 6 | Normalization | Leading/trailing whitespace follows closed rule |
| 7 | Normalization | Mixed separators rejected |
| 8 | Normalization | Too few octets rejected |
| 9 | Normalization | Too many octets rejected |
| 10 | Normalization | Non-hex character rejected |
| 11 | Address class | All-zero address rejected |
| 12 | Address class | Broadcast address rejected |
| 13 | Address class | Multicast address classified without lookup |
| 14 | Address class | Locally administered address classified without lookup |
| 15 | Address class | Randomized Wi-Fi MAC never yields global vendor |
| 16 | Address class | Virtual-interface local MAC remains unknown |
| 17 | EUI-64 | Native supported EUI-64 rule is deterministic |
| 18 | EUI-64 | Modified EUI-64 is not collapsed to EUI-48 |
| 19 | Lookup | Exact MA-L 24-bit match succeeds |
| 20 | Lookup | Exact MA-M 28-bit match succeeds |
| 21 | Lookup | Exact MA-S/OUI-36 match succeeds |
| 22 | Lookup | Longest prefix wins over valid shorter prefix |
| 23 | Lookup | Unknown global prefix returns unknown |
| 24 | Lookup | Private IEEE assignment returns private status |
| 25 | Lookup | CID is not labeled manufacturer |
| 26 | Lookup | Organization Unicode is normalized deterministically |
| 27 | Lookup | Empty organization is rejected at dataset validation |
| 28 | Dataset | Manifest schema is closed |
| 29 | Dataset | Unknown manifest field rejected |
| 30 | Dataset | Unsupported manifest version rejected |
| 31 | Dataset | Missing source file fails closed for PE-3 only |
| 32 | Dataset | Source SHA mismatch rejected |
| 33 | Dataset | Derived-artifact SHA mismatch rejected |
| 34 | Dataset | Record-count mismatch rejected |
| 35 | Dataset | Invalid UTF-8 rejected |
| 36 | Dataset | Malformed CSV/record rejected |
| 37 | Dataset | Exact duplicate collapses deterministically |
| 38 | Dataset | Conflicting duplicate invalidates artifact |
| 39 | Dataset | Unsupported prefix length rejected |
| 40 | Dataset | Prefix bits outside declared length rejected |
| 41 | Determinism | Input order cannot change derived bytes |
| 42 | Determinism | Host locale cannot change output |
| 43 | Determinism | Windows/Linux line endings cannot change output |
| 44 | Determinism | Repeated lookup produces identical semantic result |
| 45 | Determinism | Dataset timestamp does not affect selection |
| 46 | Provenance | Match records source/version/digest/method |
| 47 | Provenance | Unknown result retains sanitized provenance |
| 48 | Provenance | Failure records safe error code without MAC |
| 49 | Confidence | IEEE global longest-prefix match is high only |
| 50 | Confidence | Local/private/unknown result is unknown confidence |
| 51 | Confidence | Manufacturer confidence cannot alter identity confidence |
| 52 | Confidence | Manufacturer confidence cannot create classification |
| 53 | Privacy | Public inventory contains no PE-3 fields initially |
| 54 | Privacy | MQTT receives no PE-3 topic or field |
| 55 | Privacy | HA/dashboard contracts receive no PE-3 field |
| 56 | Privacy | Logs/status omit full MAC and stable device ID |
| 57 | Privacy | Dataset contact/address fields are discarded |
| 58 | Isolation | Missing dataset leaves inventory generation successful |
| 59 | Isolation | Corrupt dataset preserves last valid sidecar |
| 60 | Isolation | Permission failure cannot change authoritative inventory |
| 61 | Invariants | Stable IDs, canonical IP and device count remain equal |
| 62 | Invariants | Health/liveness/incidents/Assets/topology remain equal |
| 63 | Performance | 500-device warm lookup meets approved time/memory bounds |
| 64 | Future | New dataset/source/override fields are rejected until schema approval |

Additional release, installer, artifact-identity, rollback and documentation-link
tests remain mandatory. Fixtures must use synthetic MACs and organizations and
must not embed household data.

## Checkpoint decision

PE-3.0 defines architecture and governance only. PE-3.1 implementation design is
approved, but no dataset, executable, test, runtime, or production change is
authorized. PE-3.1 executable implementation remains **NOT STARTED** pending
explicit authorization and successful IEEE license/use review.
