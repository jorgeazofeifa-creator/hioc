# Canonical Address Selection Hardening Evidence Report

## Checkpoint

Phase 7A Canonical Address Selection Hardening. Repository implementation is
complete and production validation is pending. The checkpoint remains
**IN PROGRESS** until governed PI3 deployment, production evidence, and
documentation closeout are complete.

## Repository Baseline

Work began on clean `main` at
`8d86fb5e90600233ba0152070657726daf4098e1`, with `HEAD` equal to
`origin/main` and no Git operation active. Codex used only the Windows
repository and did not access PI3, PI5, Home Assistant, MQTT, or production.

## Current Selection Path and Source Map

| Path and symbol | Purpose | Inputs and relevant fields | Output and precedence |
| --- | --- | --- | --- |
| `pi4/lib/hioc/inventory.py::_parse_dhcp_lease_line`, `_read_dhcp_lease_source`, `capture_dhcp_lease_snapshot`, `dhcp_lease_observations` | Capture one immutable cycle snapshot and normalize eligible Pi-hole/dnsmasq leases. | IPv4, normalized MAC, hostname, source path, client ID, expiry, fixed collection epoch. | Active finite and infinite leases become `source=dhcp_leases`, assignment-only records. Expired, malformed, IPv6, and unusable rows contribute no current observation. |
| `pi4/lib/hioc/inventory.py::_collect_neighbor_table` | Parse primary `ip neigh` or fallback ARP output. | IPv4, MAC, interface, and NUD state. | Durable records carry `source=arp_table` and private `_neighbor_state`. `FAILED`, `INCOMPLETE`, unresolved, and non-durable rows are rejected before merge. |
| `pi4/lib/hioc/inventory.py::normalize_mac`, `stable_device_id`, `_record_key`, `_reconcile_ip_only_identities`, `merge_records` | Normalize identity, reconcile one unambiguous weak IP identity, group observations, and preserve one stable device per MAC. | Source-tagged records and previous inventory. | MAC-first `dev_...` identity; conflicting MACs do not collapse. |
| `pi4/lib/hioc/inventory.py::select_canonical_ip`, `_select_observed_value`, `_merge_record_values` | Select one representative IPv4 from candidates grouped for one identity. | Address validity, source class, neighbor state, lease activity/expiry, observation epoch. | Explicit deterministic comparator documented below. Other field selection is unchanged. |
| `pi4/lib/hioc/inventory.py::health_score`, `merge_records` | Calculate observation freshness and health separately from address selection. | Positive-observation timestamps, thresholds, and retained state. | DHCP assignment does not refresh `last_seen` or force online state. |
| `pi4/lib/hioc/inventory.py::discover_inventory`, `build_topology`, `build_dependencies`, `inventory_summary_lists` | Build inventory and projections. | Reconciled devices and services. | Selected `device.ip` is serialized and used by summaries and IP lookup; other policies are unchanged. |
| `pi4/bin/hioc-inventory-engine.py` | Write and publish established inventory documents. | `discover_inventory()` result. | Existing JSON and MQTT schemas are unchanged; private comparator fields are not serialized. |

There is one authoritative general device-address selector:
`select_canonical_ip()` through `_select_observed_value(field="ip")`.
`select_canonical_local_interface()` remains an intentional separate
collector-interface selector. It atomically selects the local IP/MAC pair using
default-route preference before device merging and is not a competing general
inventory selector.

## Defect Reproduction

Before production logic changed, an isolated repository reproduction called
the baseline `merge_records()` with one active DHCP record at
`192.168.100.252` and one `STALE` neighbor record at `192.168.100.105`, both
owned by the same normalized MAC. It selected `192.168.100.105`. Adding a
second stale neighbor at `192.168.100.106` selected `192.168.100.106`,
regardless of reversing input order.

The stable identity remained `dev_317060aa70a5a9e8`; sources were aggregated
and liveness came from positive neighbor observation. The defect did not
require a particular insertion order or timestamp. Generic source precedence
ranked `arp_table` 400 over `dhcp_leases` 300, then broke equal ARP ties by
lexical value.

## Canonical Address Contract

Canonical address means the selected representative address, not complete
address history, reachability, device health, or proof that an asset is online.
Strong identity ownership remains MAC-backed.

Candidates must be usable canonical IPv4 unicast addresses. IPv6 is outside
this existing inventory contract. Unspecified, loopback, link-local,
multicast, reserved, limited-broadcast, and malformed addresses cannot win.

The deterministic evidence rank, highest first, is:

1. local collector observation (`800`);
2. gateway observation (`750`);
3. explicitly configured integration observation (`700`);
4. `REACHABLE` neighbor (`600`);
5. `PERMANENT` neighbor (`590`);
6. active DHCP assignment (`500`);
7. `DELAY` neighbor (`450`);
8. `PROBE` neighbor (`440`);
9. fallback neighbor with unknown state (`350`);
10. `STALE` neighbor (`300`);
11. generic driver evidence (`250`);
12. expired DHCP evidence (`200`, if directly presented to the selector);
13. other owned evidence (`150`);
14. `NOARP`, `NONE`, `FAILED`, and `INCOMPLETE` neighbor evidence (`100` or
    lower); normal collection rejects unusable states before selection.

DHCP therefore does not always win: strong current or explicitly configured
evidence can outrank it, and legitimate static devices remain supported. An
active DHCP assignment cannot lose merely to stale neighbor evidence for the
same MAC.

Equal-rank candidates use, in order: infinite DHCP lease, later finite expiry,
later observation epoch when available, and numerically lowest IPv4. Missing
timestamps become zero. Duplicates and all input permutations are stable. DHCP
reservations are not distinguishable from active leases in the supported
format. The repository has no operator-pinned canonical-IP feature and no
multi-collector candidate model.

Retained offline assets keep their last valid canonical address through
existing retention behavior. This checkpoint neither creates address-history
storage nor defines retention or archival policy. The public model preserves
aggregate `sources` and DHCP metadata, but not field-level history for every
discarded candidate address.

## Implementation Summary

- Preserve accepted neighbor NUD state as private merge evidence.
- Route only canonical IP selection through an explicit comparator.
- Validate IPv4 candidates and use numeric, not lexical, final tie-breaking.
- Keep device grouping, IDs, DHCP parsing, provenance aggregation, observation
  timestamps, health, schemas, and public projections unchanged.
- Add focused regression coverage for precedence, order independence, invalid
  candidates, identity/provenance preservation, and liveness independence.

## Downstream Impact Review

| Consumer | Classification | Evidence |
| --- | --- | --- |
| Inventory JSON and device summaries | Expected beneficial change | They serialize reconciled `device.ip`; the affected MAC gets the better representative without a schema change. |
| Device detail/API and dashboards | Expected beneficial change | Repository consumers display inventory projections; no independent selector or layout change exists. |
| Service ownership and hostname association | Expected beneficial change for affected identities | Services retain stable MAC-backed `device_id`; displayed IP follows the corrected device. |
| Collector ownership | No behavioral change | The completed `.105`/`.252` collector correction uses the separate atomic local-interface selector and remains untouched. |
| Diagnostics and incident evidence | Expected beneficial change where inventory IP is consumed | They can receive the corrected representative; rules, severity, and lifecycle are unchanged. |
| Topology | Expected beneficial change only for IP hints | IP lookup uses canonical device values; topology policy is unchanged. |
| Dependency mapping | No behavioral change | Edges use service types and stable IDs, not candidate-IP ranking. |
| Historical storage | No behavioral change | No address-history or retention schema is added. |
| Enrichment joins | Expected beneficial change for IP-only hints; MAC behavior unchanged | MAC identity and ambiguity guards remain authoritative. |
| Production affected MAC and addresses | Insufficient evidence until operator capture | Fixtures reproduce the class; production was not accessed. |

## Invariant Checks and Tests

Focused tests cover active DHCP against one and multiple stale neighbors,
permutations, strong/static neighbor evidence, expired DHCP, failed and
incomplete evidence, multiple active leases, equal/missing timestamps,
duplicates, invalid and IPv6 candidates, retired-address replacement,
one-MAC identity, aggregate provenance, private-field serialization, liveness
independence, and collector precedence.

The focused canonical and inventory suites passed 137 tests. The full
repository set excluding the Bash-dependent network-probe governance module
passed 219 tests with nine unrelated environment-dependent skips. An
unfiltered 225-test discovery run passed its non-shell tests but reported three
environment errors because no Bash executable is installed; those errors are
confined to the pre-existing network-probe shell-governance module. Release
shell validation remains an operator gate on PI3. Python compilation,
documentation links, diff checks, secret review, bypass-pattern review, and
final Git checks are recorded with commit evidence.

## Warnings and Deferred Risks

- Production must identify the affected MAC, active lease, competing neighbor
  evidence, before/after canonical address, and unrelated-device stability.
- Neighbor-state quality is cycle-local private evidence. The public schema
  still exposes aggregate provenance rather than candidate-address history.
- Retention, archival, topology redesign, dependency redesign, active
  discovery, and broader address-history modeling remain outside scope.

## Production Validation Status

### First governed run

Deployment of `839e924b2249bec736ff74d9a2ac593c7fee6bb8`
succeeded. Source synchronization, Git-derived artifact identity, release
validation, supported upgrade, runtime artifact equality, PI3 validation,
inventory generation, stable one-MAC identity, aggregate provenance,
monitoring classification, health status, and bounded unrelated-device
comparison passed. Evidence is in
`/tmp/hioc-canonical-address-evidence-YKhSwI3v`; rollback backup
`/home/jazofv1/hioc/backups/release-upgrade-20260730-211723` remains available.
Rollback was not executed.

The final candidate assertion was invalid. The script selected MAC
`2c:cf:67:2e:49:d6`, treated active DHCP address `192.168.100.152` as
unconditionally canonical, and accepted link-local IPv6 neighbor
`fe80::6c67:535a:74ef:625c` as its supposed competing `STALE` address. The
inventory instead retained `192.168.100.251`, supported by higher-authority
configured integration evidence. This did not reproduce the intended
STALE-IPv4-versus-active-DHCP-IPv4 defect and does not establish a comparator
failure.

The original validation logic failed to restrict neighbor candidates to
canonical IPv4, exclude higher-ranked local, gateway, integration,
`REACHABLE`, or `PERMANENT` evidence, or apply ADR-0018 conditionally. Its
assumption that every active DHCP address must win contradicted the approved
comparator.

### Revised production validation contract

A direct production candidate requires exactly one normalized MAC-backed
identity, active valid DHCP IPv4, a different `STALE` neighbor IPv4 for the
same MAC, no higher-ranked source or neighbor evidence, and—when historical
pre-fix inventory is supplied—a historical canonical address equal to the
stale candidate. Invalid, IPv6, loopback, link-local, multicast, broadcast,
unspecified, reserved, and malformed addresses are ineligible.

Repository-owned tooling now reports:

- `PASS`: a qualifying candidate exists and active DHCP wins, with all general
  invariants passing;
- `NO_QUALIFYING_CANDIDATE`: no current production observation can directly
  reproduce the bounded defect; this is not failure and never recommends
  rollback;
- `FAIL`: a qualifying stale IPv4 still wins, or an independent deployment or
  invariant check fails. Only this outcome recommends rollback.

Ten focused validator tests cover all three outcomes, IPv6 link-local
rejection, integration/local/gateway exclusion, `REACHABLE`/`PERMANENT`
exclusion, historical-canonical matching, expired/invalid DHCP exclusion, and
independent invariant failure. The combined canonical-validator,
canonical-selector, and inventory suites passed 147 tests. The broader
non-Bash repository suite passed 229 tests with nine environment-dependent
skips.

### Second governed validator run

The second run again proved comparator artifact identity and all six actual
Boolean invariants: artifact identity, unique MAC identity, inventory-count
consistency, health/liveness field presence, stable identity fields, and
bounded unrelated canonical changes. Device count remained 151 and unrelated
canonical-IP changes were zero. No candidate qualified: PI5 had DHCP IPv4
`.152`, a current `REACHABLE` IPv4 at `.251`, and only a link-local IPv6
`STALE` neighbor.

The validator nevertheless returned `FAIL` because it evaluated every value in
the invariant JSON with generic truthiness. Diagnostic metadata
`_unrelated_canonical_change_count: 0` was therefore incorrectly added to
`failed_invariants`. Rollback was not performed. This is a validator
input-contract defect; the evidence implies
`NO_QUALIFYING_CANDIDATE` with `rollback_recommended=false`.

The corrected contract is closed and typed. Exactly six required invariant
names must be present and each must be a JSON Boolean. Required `false` values
are genuine failed invariants. Missing or non-Boolean required values and
unexpected non-underscore keys are explicit input errors and produce `FAIL`.
Underscore-prefixed keys are preserved as diagnostic metadata and never
participate in Boolean evaluation; zero, positive counts, null, and strings are
valid metadata values.

Sixteen focused validator tests cover valid `PASS`,
`NO_QUALIFYING_CANDIDATE`, and `FAIL` paths; zero, positive, null, and string
diagnostics; required false values; missing fields; integer `0` and `1` type
errors; and unexpected public keys. The combined validator, canonical-address,
and inventory suites passed 153 tests. The broader non-Bash regression suite
passed 235 tests with nine environment-dependent skips.

### Retired `.152` DHCP finding

The retired PI5 address `192.168.100.152` was confirmed as an unexpired old
lease, with no renewal observed during the bounded 60-second production check.
Its ultimate classification and any cleanup remain unresolved. Repository
configuration selects
`HIOC_INVENTORY_DHCP_LEASE_FILES`, defaulting to
`/etc/pihole/dhcp.leases`; explicit configuration can name multiple
comma-separated dnsmasq-format files. Repository evidence cannot determine
which production file supplied this row, its exact expiry, whether a Pi-hole
or dnsmasq reservation exists, whether `.251` is also configured, whether the
MAC identifies a current PI5 interface, or whether recent DHCP requests
occurred. The read-only operator investigation must answer those questions
before classifying the finding as migration cleanup, parser defect, or valid
multi-address behavior.

The parser treats expiry zero as an infinite active assignment and a positive
epoch strictly greater than the fixed collection epoch as active. The source
format uses epoch seconds. Expired rows, IPv6 rows, malformed rows, and
unusable MAC/IP identities are rejected. Duplicate rows are deterministically
ordered, preferring infinite expiry and otherwise later expiry. The parser
cannot distinguish a configured reservation from an active lease-file row.
Repository tests cover finite active, expired, zero-expiry, duplicate,
conflicting-MAC, malformed, IPv6, and deterministic multi-source cases. Whether
Pi-hole emits static reservations into the runtime lease file is production
configuration evidence, not proven by this repository.

**IN PROGRESS.** The comparator is deployed, but production validation remains
open. The corrected strict validator must be rerun on PI3. No success is
declared and rollback is not recommended from either validator defect.

## Final Result

**IN PROGRESS.** Deployment succeeded, but closure requires the revised
validation outcome, explicit `.152` DHCP evidence, and committed production
closeout documentation.
