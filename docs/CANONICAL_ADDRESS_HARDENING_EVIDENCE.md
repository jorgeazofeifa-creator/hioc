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

**PENDING OPERATOR EXECUTION.** Codex did not access PI3 or PI5. No production
action occurred. Production validation must use the supported release workflow,
capture bounded before/after evidence, and record rollback readiness.

## Final Result

**IN PROGRESS.** Repository implementation is ready for governed operator
validation. Closure requires passing production deployment and evidence and a
committed Production Evidence Report.
