# Passive Enrichment Architecture and Specification

Status: **IN PROGRESS - DESIGN REVIEW; NO IMPLEMENTATION STARTED**

This document is the implementation-ready design for the remaining Phase 7A
passive-enrichment work. It does not authorize executable changes, production
deployment, Active Discovery, retention or archival policy, permanent-IoT
monitoring, or DHCP service-health work. Canonical IPv4 selection, stable
identity, liveness, health, and existing retention behavior remain unchanged.

## Repository baseline

The design review began from clean branch `main` at
`5f413fdbdeb8250a42e32f2ee7ca195c426c062b`, equal to `origin/main`, with no
merge, rebase, cherry-pick, revert, or bisect operation in progress. Canonical
Address Selection Hardening was complete and production validated. The Master
Plan identified passive enrichment as the next Phase 7A work.

## Current enrichment source map

| Source | Acquisition and authority today | Fields available | Current conflict behavior | Provenance, trust, and freshness | Gaps |
|---|---|---|---|---|---|
| Local host | `local_ipv4_addresses`, OS release, canonical local-interface selection, and local service collection | IP, MAC, hostname, type, interfaces, firmware, services | Highest generic observed authority; known infrastructure cannot replace protected local `hostname` or `type` | `source=local_host`; direct, current collector evidence | No field-level candidates or confidence |
| Default gateway | `default_gateway` | gateway IP, interface, type/role hints | Second-highest generic observed authority | `source=gateway`; direct route evidence | Sparse descriptive metadata |
| Neighbor table | One passive `ip neigh` snapshot through `_collect_neighbor_table` | IP, MAC, neighbor state | MAC reconciliation; canonical IP uses ADR-0018; unusable states rejected | `source=arp_table`; state is private reconciliation evidence; positive states may establish observation | Hostname/vendor/location absent; no address-candidate history |
| Pi-hole/dnsmasq DHCP leases | Configured files or `/etc/pihole/dhcp.leases` | IP, MAC, hostname, client ID, source path, expiry | Assignment-only; active/infinite IPv4 rows; cannot establish liveness; ADR-0018 owns canonical IP | `source=dhcp_leases`; file and expiry retained | DHCP hostname has no field-level provenance or conflict record |
| Integration JSON directory | `integration_inventory`, one or more JSON files under the configured integration directory | Open device dictionaries, commonly identity and descriptive fields | Generic integration authority is below local/gateway and above ARP/DHCP; central reconciliation owns identity | `source=integration:<file>`; file identity retained | Input contract is permissive; producer trust and per-field authority are not declared |
| Known infrastructure | Operator-maintained JSON selected by `HIOC_INVENTORY_KNOWN_INFRASTRUCTURE_FILE` | `name`, hostname, IP, MAC, role, type, vendor, model, location, area, topology hints, notes | Exact MAC first; ambiguous/conflicting identifiers do not merge; operator metadata fills approved metadata fields; local protected fields remain observed | `source=known_infrastructure`; configured metadata, not an observation | `name` is later collapsed into `display_name`; no field provenance, edit timestamp, or separate physical/network location |
| Retained prior inventory | Previous generated inventory supplied to `merge_records` | Prior public device record and first/last-seen state | Preserves stable identities and prior records; current evidence can update selected fields | Aggregate `sources`, `first_seen`, `last_seen` | Historical candidates cannot be distinguished from selected values |
| Derived classification | `classify_device`, `operator_role`, `inventory_class`, health and monitoring helpers | roles, public role, class, display name, status, observation and health fields | Deterministic keyword and state rules after source merge | Result exists, but derivation inputs/rule version are not recorded per field | Derived value may look observed; no explanation/confidence envelope |
| Local services and sockets | systemd and listening-socket collection | service name/type/status/port/device owner | Stable service construction, then dependency enrichment | `source=systemd` or `ss` | Device descriptive enrichment is not obtained from services |
| Home Assistant registry metadata | No repository ingestion path found | Planned names, areas, device/entity associations | None | Home Assistant consumes HIOC inventory; it is not a proven enrichment producer | Requires a future read-only, secret-safe adapter and explicit authority contract |
| MQTT metadata | No central inventory enrichment subscriber found | HIOC inventory and summaries are published retained | None as an input | MQTT is transport/publication today | Legacy/external publishers must not silently become enrichment authority |
| MAC/OUI vendor lookup | No repository implementation found | None today; `vendor` may arrive from known or integration records | None | Not implemented | Requires pinned local data, license/version governance, and deterministic fallback |
| Legacy network probe | Separate governed producer publishes bounded PI5/network evidence | Configured PI5 identity/reachability | Does not feed central `inventory.py` merge in repository evidence | External MQTT producer with its own governed configuration | Must not be mistaken for central enrichment or a second identity authority |

`reverse_dns`, subnet scanning, ping, and SNMP helpers exist, but Safe Active
Discovery is postponed. They are not approved passive-enrichment inputs.

### Source-to-serialization evidence

The acquisition and reconciliation path is
`pi4/lib/hioc/inventory.py:discover_inventory` -> registered
`PassiveNetworkDriver.collect` -> local/gateway/neighbor/DHCP/integration
records -> `append_known_infrastructure` -> classification -> `merge_records`
-> topology/dependencies/summary. `pi4/bin/hioc-inventory-engine.py` validates
the top-level schema, writes inventory component JSON files, and publishes the
retained inventory topics. Home Assistant packages under
`homeassistant/packages/` and Dashboard V2 YAML under
`homeassistant/dashboards/` consume those selected values.

Implementation anchors and coverage are:

| Source | Repository anchors | Normalization and influence | Representative coverage |
|---|---|---|---|
| Local/gateway | `local_ipv4_addresses`, `default_gateway`, `select_canonical_local_interface` | MAC/IPv4 normalization; owns collector identity and service ownership; direct liveness evidence | `tests/test_inventory.py` canonical-local-interface, local-authority, and service-ownership cases |
| Neighbor | `_collect_neighbor_table`, `neighbor_table` | `normalize_mac`; durable states only; affects observation and ADR-0018 candidate rank | neighbor state-matrix, snapshot, failure, retention, and canonical-selection suites |
| DHCP | `dhcp_lease_paths`, `_parse_dhcp_lease_line`, `capture_dhcp_lease_snapshot`, `dhcp_lease_observations` | normalized MAC/hostname and IPv4; fixed collection epoch; assignment/canonical candidate only, never liveness | DHCP parser, snapshot, expiry, source-status, merge, liveness, and canonical suites |
| Integration | `integration_inventory` and `PassiveNetworkDriver.collect` | object passthrough plus parent-MAC normalization and `integration:<stem>` source | integration preservation, hint compatibility, permutation, and canonical exclusion tests |
| Known/operator | `known_infrastructure_path`, `_clean_known_record`, `known_infrastructure`, `append_known_infrastructure` | closed accepted key set, identifier validation, empty-value removal, exact-MAC preference | known validation, duplicate/conflict, authority, enrichment, topology, and never-observed tests |
| Retained/merge | `_record_authority`, `_select_observed_value`, `_merge_record_values`, `merge_records` | deterministic authority and stable identity reconciliation; aggregate sources and timestamps | order/permutation, weak/strong identity, retained observation, first-seen, and health tests |
| Derived | `classify_device`, `operator_role`, `inventory_class`, `observation_freshness`, `health_score` | keyword/state derivation after acquisition | classification, health, monitoring, correlation, and presentation suites |
| Services/relationships | `LocalServiceDriver`, `build_services`, `build_topology`, `build_dependencies`, `enrich_services` | stable device ownership and configured parent hints | topology, dependency, service enrichment, and collector-ownership tests |
| Serialization/consumers | `pi4/bin/hioc-inventory-engine.py`, `pi4/lib/hioc/core/schemas.py`, Home Assistant packages/dashboards | top-level schema only; public selected values and summaries | inventory, schema/core, dashboard dynamic-truth, inventory-presentation, and watch-device suites |

No repository path proved ingestion from Home Assistant registries, MQTT
metadata, or an OUI reference. Those are unresolved/planned sources, not
current capabilities. Repository searches also found no approved enrichment
path that directly assigns a stable ID from a name or changes canonical IP
outside central inventory reconciliation.

## Current inventory schema findings

The public inventory envelope requires `schema_version`, `updated`, `devices`,
`services`, `topology`, `dependencies`, and `summary`. The schema validator
checks those top-level types only; it does not enforce a closed device schema.
That compatibility freedom is useful but cannot substitute for an explicit
enrichment contract.

Current device fields fall into these groups:

| Group | Fields | Type/default and ownership |
|---|---|---|
| Stable identity | `id`, `mac`, `ip`, `hostname` | Strings when known; MAC-backed `id` preferred. Central reconciliation and ADR-0018 own identity/canonical IP. Enrichment must not modify them. |
| Presentation/classification | `name`, `display_name`, `role`, `roles`, `type`, `inventory_class` | Strings/list. `display_name` falls back through configured name, hostname, IP, ID; `name` is then set to it. Role/type/class may be configured or derived. |
| Device description | `vendor`, `model`, `firmware`, `interfaces` | Optional strings/list from local, integration, retained, or known records. Missing values are normally omitted rather than `null`. |
| Operator context | `location`, `area`, `notes` | Optional strings from known/integration/retained records; physical and network location are not separated. |
| Relationship hints | `parent_id`, `parent_device_id`, `parent_mac`, `parent_ip`, `uplink_mac`, `uplink_ip` | Optional strings; normalized during known-record intake and resolved to stable IDs when possible. |
| Source/observation | `source`, `sources`, `last_seen_source`, `first_seen`, `last_seen`, `last_seen_epoch` | Aggregate strings/list/timestamps. Sources are retained, but selected-field attribution is not. |
| DHCP assignment | `dhcp_client_id`, `dhcp_lease_source`, `lease_expires_epoch` | Optional strings/integer. Assignment evidence only; it does not refresh liveness. |
| Liveness/health | `reachable`, `observation_status`, `observation_age_seconds`, `health_status`, `health_score`, `health_reasons`, `status`, `operationally_monitored` | Optional/derived Boolean, numeric, string, and list fields. Existing monitoring contracts own them. |

Private underscore-prefixed reconciliation fields may exist during collection
but are not a supported public contract. Services are separate objects with
stable ID, name, type, owning `device_id`, status, source, and sometimes port.
Topology and dependency edges use stable IDs. Inventory summaries and Home
Assistant presentation consume selected public values, not candidate evidence.

The critical modeling defects for enrichment are: `name` mixes operator intent
with fallback presentation; `location` does not distinguish physical placement
from network attachment; aggregate `sources` cannot explain a selected field;
conflicting values are normally resolved or discarded without a durable
field-level record; and derived roles do not carry rule provenance.

## Proposed enrichment domain model

Enrichment is descriptive knowledge attached to an already reconciled stable
device identity. It is not another identity engine.

1. **Observed identity attributes** are evidence such as DHCP hostname or an
   integration-reported model. They may conflict and expire, but do not replace
   stable identity or canonical IP.
2. **Derived metadata** is deterministic interpretation such as manufacturer
   from a pinned OUI dataset or a role suggestion. It records rule/dataset
   version and inputs.
3. **Operator-managed metadata** expresses intent: friendly name, physical
   location, purpose, notes, and later lifecycle facts. It is authoritative for
   its own field and is never silently overwritten by discovery.
4. **Relationship metadata** associates a stable device with an area, parent,
   service, Home Assistant device/entity, or later automation. It does not
   imply identity equivalence or liveness.

The initial storage contract is a parallel local artifact,
`state/inventory/enrichment.json`, keyed by stable device ID. It is generated
atomically with inventory, excluded from source control and MQTT, and has this
conceptual shape:

```json
{
  "schema_version": "1.0",
  "updated": "RFC3339 timestamp",
  "devices": {
    "stable-device-id": {
      "fields": {
        "observed_hostname": {
          "selected": {"value": "host", "candidate_id": "..."},
          "candidates": [],
          "conflict": {"status": "none", "candidate_ids": []}
        }
      }
    }
  }
}
```

The first implementation must not project this envelope into public inventory,
MQTT, Home Assistant, dashboards, incidents, or identity selection. A later
additive public projection requires its own schema compatibility and consumer
review.

### Field catalog and rollout

| Layer/field | Type/default | Eligible sources and merge rule | Conflict/provenance/confidence | Mutability/retention | Exposure | Rollout |
|---|---|---|---|---|---|---|
| `observed_hostname` | string/absent | local, integration, DHCP; select by authority, then evidence strength and meaningful recency | Retain all normalized distinct candidates | Source-managed; current-cycle evidence only in MVP | Local envelope only | MVP |
| `friendly_name` | string/absent | operator known-infrastructure value only; discovered names remain candidates, never replacements | Operator provenance; discovered disagreement is informational | Operator mutable; no automatic deletion | Later inventory/dashboard opt-in | Next |
| `physical_location` | string/absent | operator metadata only | Operator provenance; never inferred from IP/interface | Operator mutable; sensitive | Later restricted display | Next |
| `network_location` | object/absent | observed interface/parent/topology evidence | Candidate associations and conflicts retained | Recomputed; no lifecycle retention decision here | Later operations view | Later |
| `manufacturer` | string/absent | operator override, trusted integration, then pinned OUI derivation | Dataset/version or operator source required | Recomputed on dataset update; operator value persists | Later inventory/dashboard | Later |
| `model` | string/absent | operator, trusted integration, observed source | Preserve disagreements | Operator value persists; observations current | Later inventory | Later |
| `role_suggestion` | list/empty | deterministic classifier only | Rule version, input field IDs, categorical confidence | Recomputed; never overwrites operator role | Later review UI | Later |
| `operator_role` | string/absent | operator only | Operator provenance | Operator mutable | Later inventory/dashboard | Later |
| `purpose`, `notes` | string/absent | operator only | Operator provenance | Operator mutable; potentially sensitive | Restricted/opt-in | Later |
| `ha_device_ids`, `ha_entity_ids` | string lists/empty | future read-only HA registry adapter | Registry instance and observation time | Recomputed; stale association policy deferred | Restricted operations | Later |
| `service_associations` | object list/empty | local services and future trusted integration/MQTT association evidence | Source and rule per edge | Recomputed | Operations | Later |
| `metadata_quality` | enum/`unknown` | derived from completeness/conflicts | Rule version and reasons | Recomputed | Summary/dashboard candidate | Later |
| purchase date, owner, photo reference, lifecycle state | typed/absent | operator only | Operator provenance | Lifecycle retention requires separate approved policy | Private by default | Deferred |

No enrichment field may write `id`, `mac`, canonical `ip`, `first_seen`,
`last_seen`, liveness, health, monitoring eligibility, incident state, or
retention/archive state.

## Source authority and conflict contract

Authority is field-specific. The hierarchy for descriptive enrichment is:

1. operator-pinned value for the same operator field;
2. explicit known-infrastructure metadata;
3. a configured trusted integration for a declared field;
4. strong direct passive observation;
5. deterministic derived reference data;
6. weak passive observation;
7. retained historical candidate;
8. presentation fallback.

This hierarchy does not replace the current identity, canonical-address, or
liveness comparators. A source must declare which fields it may supply.
Unknown integration keys remain compatibility data but cannot gain enrichment
authority automatically.

Different nonempty normalized values create a conflict. The system retains the
candidates and selects deterministically by field authority, confidence,
meaningful observation time, normalized value, then stable source identifier.
Timestamps are compared only between observational candidates with comparable
semantics; configuration time is never fabricated as observation time.
Operator values remain selected until explicitly changed or removed. DHCP and
Home Assistant names may suggest but never overwrite `friendly_name`.

## Provenance model

Each candidate contains:

- stable `candidate_id` derived from device ID, field, normalized value, source,
  and source instance;
- `value` and `normalized_value`;
- `source_type`, stable `source_id`, and optional source-instance/version;
- `authority` and `confidence` categories;
- `observed_at` and `expires_at` only when the source supplies meaningful time;
- `derived_by` and input candidate IDs for derived values;
- `active` state and a non-sensitive reason;
- first/last collected timestamps for operational diagnostics, not identity.

The parallel artifact is the initial source of field-level evidence. Aggregate
`source`/`sources` remain unchanged for backward compatibility. Field-level
provenance may be projected into public inventory only after a separate payload
size, schema, privacy, Home Assistant, and MQTT review. No database is required
for the minimum implementation.

## Confidence model

Confidence is categorical and separate from authority:

- `authoritative`: explicit operator/configuration statement for its owned field;
- `high`: direct, unambiguous, current evidence from a trusted source;
- `medium`: deterministic derivation from versioned data or corroborated evidence;
- `low`: weak, ambiguous, stale, or uncorroborated observation;
- `unknown`: insufficient evidence.

Confidence never changes source ownership and is not a probability. A lower-
confidence operator value still owns an operator field until the operator
changes it. Conflicts reduce derived `metadata_quality`; they do not affect
identity, health, or availability.

## Minimum viable passive enrichment

The smallest safe first implementation is **PE-1: Hostname Enrichment Evidence
Envelope**. It records local-host, configured-integration, and DHCP hostname
candidates for existing stable device IDs in the parallel local artifact,
normalizes them, applies the field-specific deterministic selector, and exposes
conflicts in that artifact only.

PE-1 must not change selected inventory hostname/name/display name, canonical
IP, stable ID, source merge, health, liveness, retention, MQTT, Home Assistant,
dashboards, or incidents. It is valuable because hostname conflict is already
present in available passive sources and it proves the provenance pattern
before operator metadata or external datasets are introduced.

Acceptance evidence: clean governed source; focused normalization, source-
authority, order-independence, conflict, missing-time, and no-public-change
tests; full inventory regression; before/after inventory invariant comparison;
valid atomic artifact with no secrets; unchanged device count/IDs/canonical
IPs/health; and runtime artifact identity if deployed. Roll back PE-1 only for
artifact generation failure that disrupts inventory, schema/secret leakage,
nondeterminism, or any change to protected invariants. A hostname conflict is
expected evidence, not rollback cause.

Likely PE-1 files are `pi4/lib/hioc/inventory.py` for candidate construction,
a small schema/serializer module under `pi4/lib/hioc/core/` if separation is
needed, `pi4/bin/hioc-inventory-engine.py` for atomic local artifact output,
`tests/test_inventory.py` plus a focused enrichment test module, and Operations,
System Reference, Data Model, this specification, Decisions, and Changelog
documentation. No Home Assistant, dashboard, MQTT topic, incident, deployment,
or identity module should change. The enrichment file is additive local state;
absence or disabled generation must leave current inventory behavior intact.

PE-1 stopping conditions are any need to change identity/canonical logic,
public device fields, production source configuration, retention semantics, or
consumer contracts; any such need returns the design for approval instead of
expanding scope.

## Ordered implementation sequence

1. **PE-0 - Architecture and specification (current):** design review only.
2. **PE-1 - Hostname enrichment evidence envelope:** minimum implementation
   above.
3. **PE-2 - Operator-friendly naming and physical-location foundation:** split
   configured intent from fallback `name`, using known infrastructure and the
   proven provenance envelope.
4. **PE-3 - Manufacturer reference enrichment:** approve and pin a local OUI
   dataset, license/version/update governance, and deterministic derivation.
5. **PE-4 - Trusted integration association:** add a read-only Home Assistant
   registry adapter and declared field/association authority; do not infer
   availability.
6. **PE-5 - Passive service and MQTT association provenance:** describe existing
   relationships without making transport evidence an identity authority.
7. **PE-6 - Classification suggestions and metadata-quality summaries:** expose
   explainable derived suggestions; operator role remains protected.
8. **Expected-availability classification foundation:** design and approve only
   after passive descriptive enrichment is stable.
9. **Permanent IoT monitoring, Home Assistant availability correlation,
   automation-impact mapping, and actionable IoT incidents:** separate ordered
   checkpoints after expected-availability semantics are approved.
10. **Retention/archival and maintenance workflows:** separately designed and
    approved; no lifecycle semantics are implied by this specification.

Implementation packages PE-1 through PE-6 are bounded as follows:

| Package | Objective, fields, and likely modules | Schema and protected invariants | Tests and production validation | Dependencies, rollback, and deferred work |
|---|---|---|---|---|
| PE-1 | `observed_hostname` candidates/conflict in `inventory.py`, a core enrichment serializer, inventory engine, and focused tests | New local artifact only; public schema, IDs, IPs, liveness, health unchanged | Candidate normalization/authority/order/conflict tests; full inventory regression; before/after protected-invariant and governed-artifact proof | Depends on design approval; roll back for generation disruption, nondeterminism, leakage, or invariant change; public projection deferred |
| PE-2 | `friendly_name` and `physical_location`; known-infrastructure loader, enrichment model, synthetic example/schema, and later presentation adapter | Additive configuration keys only after compatibility review; no name-based identity; no canonical/liveness/health effect | Empty/duplicate/conflict/operator-precedence tests; old-config compatibility; production proof that IDs/IPs/count/health remain stable and only approved metadata changes | Depends on PE-1; roll back for silent overwrite, private-data exposure, or invariant change; owner/purpose/lifecycle deferred |
| PE-3 | `manufacturer` candidates using known/integration values and a pinned local OUI reference adapter | Local enrichment extension; dataset version/license explicit; vendor cannot influence identity or canonical rank | MAC-prefix, local/private/randomized MAC, override, dataset-version, determinism tests; governed dataset/artifact identity and bounded metadata-only production diff | Depends on PE-1 and dataset approval; roll back for licensing, nondeterminism, excessive/unbounded changes, or protected-field changes; online lookup prohibited |
| PE-4 | `ha_device_ids`, `ha_entity_ids`, and area/name candidates through a new read-only adapter | Local association evidence initially; HA names cannot replace operator fields; availability is excluded | Synthetic registry fixtures, secret redaction, missing/duplicate association, order tests; least-privilege read proof, bounded association counts, unchanged public/health state | Depends on PE-1/2 and access/schema approval; roll back for secret leakage, ambiguous identity mutation, or HA impact; availability correlation deferred |
| PE-5 | `service_associations` and MQTT association evidence using existing service ownership and declared configured mappings | Relationship layer only; MQTT presence is not device observation or health | Edge stability, missing endpoint, duplicate/conflict, no-liveness tests; bounded relationship diff and no publish/subscribe behavior change | Depends on provenance foundation; roll back for cycles, unstable IDs, topic leakage, or protected-state change; automation dependencies deferred |
| PE-6 | `role_suggestion` and `metadata_quality` with rule/version/reasons | Derived local values; cannot overwrite `operator_role` or create incidents | Rule explanation, agreement/conflict, missing-data, determinism, no-health-coupling tests; bounded derived-only diff and operator-value preservation | Depends on PE-1 through applicable sources; roll back for unexplained output, operator overwrite, or operational-state change; expected availability remains next design foundation |

For every package, identity invariants are stable device count/IDs and no
metadata-based merge/split; canonical invariants are unchanged selected IPs
except independently governed input changes; liveness invariants are unchanged
positive-observation timestamps/status; and health invariants are unchanged
scores, reasons, monitoring eligibility, and incidents. Production validation
uses a pre-deployment baseline, governed artifact identity, post-deployment
capture, bounded field-specific diff, invariant comparison, and explicit
rollback decision. Missing optional metadata is never a deployment failure.

Each executable sub-checkpoint requires repository tests, secret review,
before/after protected-invariant evidence, supported deployment if needed,
production Evidence Report, and explicit closure. A sub-checkpoint stops and
rolls back for protected-invariant change, secret/private-data exposure,
nondeterminism, unsupported consumer breakage, or failed governed artifact
identity. Missing enrichment or honest conflict is degraded enrichment, not an
offline device or automatic rollback.

## Dashboard and operations impact

PE-1 has no dashboard or MQTT impact. Later dashboards should show selected
descriptive value, source category, confidence label, and a concise conflict
indicator without presenting inference as fact. Operator value and discovered
suggestion must be visually distinct. Missing enrichment remains `Unknown`, not
unhealthy or offline. Detailed candidates belong in diagnostics, not the main
incident view.

Operations must document source enablement, supported schemas, artifact
freshness, non-secret diagnostics, and rollback boundaries for each adapter.
Enrichment-source failure may produce a discovery limitation but must not erase
the last selected operator value or fabricate a device incident.

## Security and privacy findings

Hostnames, MACs, internal IPs, Home Assistant device/entity identifiers,
physical locations, notes, owner, purchase information, photos, service names,
and automation associations can reveal occupancy, behavior, and network
structure. Production values and credentials must never enter Git or test
fixtures. Tests use synthetic data. Local artifacts inherit restrictive state
permissions and atomic writes.

MQTT publication is deny-by-default for physical location, notes, owner,
purchase data, photos, raw HA identifiers, candidate histories, and conflict
details. Logs and notifications report counts/source IDs and sanitized reasons,
not sensitive values. Dashboard exposure is field-specific and opt-in; remote
notifications must not include private enrichment without a separately
approved policy. Future HA access must be read-only, least-privilege, and
secret-file/config based.

## Open design decisions

- Approve PE-1's parallel local artifact as the first provenance boundary.
- Approve categorical authority/confidence rather than numeric scores.
- Define a versioned integration input schema before trusting new fields.
- Select and license a local OUI dataset before PE-3.
- Decide which later enrichment fields may enter retained MQTT and dashboards.
- Design expected availability and retention/archival in their own checkpoints.

No open decision blocks review of this specification, but PE-1 must not start
until explicit approval is given.
