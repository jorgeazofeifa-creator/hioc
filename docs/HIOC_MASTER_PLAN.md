# HIOC Master Plan

**Version:** 1.0  
**Status:** Active  
**Owner:** Jorge Azofeifa  
**Project:** Home Infrastructure Operations Center (HIOC)

---

## Purpose of this Document

This document is the authoritative roadmap for the HIOC project.

It defines the project's vision, guiding principles, architecture, implementation roadmap, and working agreements. When implementation decisions conflict with conversational guidance, this document takes precedence unless it is intentionally revised.

Every contributor, human or AI, should read this document before making changes to the project.

---

## Document Ownership

This document is the constitution of the project.

It owns:

- vision
- philosophy
- principles
- roadmap
- implementation phases
- current phase
- current objective
- next task
- working agreement

It should not contain detailed architecture, runtime procedures, network configuration, MQTT documentation, Home Assistant documentation, data model details, installation instructions, release procedures, design system rules, or dashboard implementation details. Those belong in the focused documents linked from [../README.md](../README.md).

The Master Plan explains how HIOC is built and evolves. [SYSTEM_REFERENCE.md](SYSTEM_REFERENCE.md) explains what HIOC is today. [OPERATIONS.md](OPERATIONS.md) is the authoritative runtime reference, [NETWORK_FOUNDATION.md](NETWORK_FOUNDATION.md) owns network dependencies, [DEPLOYMENT.md](DEPLOYMENT.md) owns deployment boundaries, and [INCIDENT_MODEL.md](INCIDENT_MODEL.md) owns incident semantics.

Update this document only when project direction, roadmap, phase, objective, next task, or implementation status changes.

---

# Vision

HIOC (Home Infrastructure Operations Center) is an operational platform for monitoring, understanding, documenting, and troubleshooting a home infrastructure.

Its primary purpose is **not** monitoring.

Its primary purpose is helping the operator immediately answer:

- What is happening?
- Why is it happening?
- What is affected?
- What should I do?
- What happened while I was away?

HIOC should behave like a miniature Network Operations Center (NOC), providing operator-oriented information instead of raw metrics.

---

# Design Principles

These principles override every implementation decision.

## 1. Stability Before Features

Never add features simply because they are possible.

Every feature must improve operator awareness.

---

## 2. Follow the Current Phase

Implement only the current planned phase.

Avoid introducing unrelated improvements or redesigning existing systems unless fixing a defect or explicitly approved.

When a phase is complete:

- Validate
- Commit
- Return to this document
- Continue with the next phase

---

## 3. One Problem at a Time

Each phase has one primary objective.

Complete it before beginning another.

Avoid parallel feature development.

---

## 4. Operator First

Dashboards exist for humans.

Every card should answer an operational question.

Avoid exposing implementation details whenever possible.

---

## 5. Explain, Don't Display

Do not simply expose values.

Explain:

- Meaning
- Impact
- Recommendation

The dashboard should reduce operator thinking, not increase it.

---

## 6. Passive Before Active

Always prefer information already available from the infrastructure.

Only perform active discovery when passive information cannot achieve the required objective.

---

## 7. Safe Operation

HIOC must never negatively impact the infrastructure it monitors.

Avoid unnecessary:

- Polling
- Network scans
- Broadcast traffic
- CPU usage
- Disk writes

---

## 8. Reuse Existing Components

Enhance existing systems whenever practical.

Avoid duplicate engines or overlapping functionality.

---

## 9. Incremental Evolution

Prefer extending existing architecture over replacing it.

Large redesigns require explicit approval.

---

# Architecture

Current major components include:

- Platform Core
- Inventory Engine
- Incident Engine
- Correlation Engine
- History Engine
- Dashboard v2
- MQTT Publishing Layer
- Home Assistant Integration

Additional components should integrate cleanly into this architecture.

---

# Dashboard Philosophy

Dashboard v2 is the primary operator interface.

Each page has a specific purpose.

## Operations

Current infrastructure health.

## Diagnostics

Current evidence.

## History

Past incidents.

## Inventory

Living infrastructure documentation.

## Network

Network diagnostics.

## Servers

Server diagnostics.

Future pages should have equally focused responsibilities.

---

# Incident Philosophy

Every incident should produce:

- Live status
- Supporting evidence
- Affected systems
- Dependency path
- Recommended action

When resolved, every incident should automatically produce:

- Timeline
- Summary
- Probable cause
- Duration
- Affected services
- Operator review

Historical analysis is considered a first-class feature.

---

# Inventory Philosophy

The Inventory is the living documentation of the infrastructure.

It should answer:

- What exists?
- Where is it?
- What does it do?
- What depends on it?
- Is it healthy?
- When was it last seen?
- How was it discovered?

Inventory information should become richer over time while remaining trustworthy.

---

# Development Roadmap

## Completed

- Platform Foundation
- MQTT Publishing
- Dashboard v2
- Incident Engine
- Correlation Engine
- History Engine
- Incident Review
- Dashboard usability improvements
- Initial Living Inventory

---

## Current Phase

### Phase 7A - Passive Living Inventory

Objective:

Build the richest possible infrastructure inventory without performing active network discovery.

Passive information sources include:

- Pi-hole DHCP leases
- Linux ARP / Neighbor tables
- Home Assistant Device Registry
- Home Assistant Entity Registry
- MQTT Discovery
- Existing integrations
- Known infrastructure definitions
- Routing information
- Passive operating system information

Expected outcome:

The Inventory becomes the authoritative documentation of the infrastructure without requiring active scans.

---

#### Phase 7A.8 Recovery Validation Chain

Status: **COMPLETE**

Scope: Recovery and re-validation of the approved lifecycle migration baseline after temporary validation state loss.

Completed validation sequence: R1, Post-R1, R2, Post-R2, R3, Post-R3, R4, and Post-R4. R4 received the formal decision **A. R4 APPROVED**.

- Approved generation: `gen_1784229948679_0a45eaf2f2f7`
- Approved recovery epoch: `/home/jazofv1/hioc-validation/phase7a8/epoch-20260716T173541Z`

The recovery sequence is complete, and the approved migrated baseline is the authoritative lifecycle recovery reference. The original HIOC Master Plan remains authoritative; Phase 7A Passive Living Inventory remains active; Active Discovery remains postponed. R5 is a future checkpoint and was not prepared or executed by this finalization.

This checkpoint preserves phased work, no scope creep, production validation, Evidence Reports, and return to the Master Plan after each completed sub-step.

#### Phase 7A.9 Passive Inventory Correctness Validation

Status: **COMPLETE**

Scope: Read-only production validation of the existing passive-inventory baseline, with no behavioral changes or corrective implementation.

##### Evidence Report

**Deployment result:** No deployment or runtime change was part of this checkpoint. Production validation covered `inventory.json`, `devices.json`, `services.json`, `capabilities.json`, `topology.json`, `dependencies.json`, `summary.json`, and `status.json`; every file was present and valid. The official HIOC production validator, `bash /home/jazofv1/hioc/pi4/validate_pi4.sh`, completed successfully with all checks passing.

**Intended behavior:** Passive Inventory must preserve stable identity and internally consistent projections while keeping DHCP assignment evidence, observation freshness, operational monitoring, and source authority semantically distinct.

**Validation performed:** Stable snapshots confirmed that `inventory.devices` matched `devices.json`, `inventory.services` matched `services.json`, summary counts matched the projections, and counts remained internally consistent. Health categories, Watch-device records, health reasons, projection counts, and summary counts were mutually consistent.

**Invariant checks:** The baseline contained 140 devices, 140 unique IDs, 140 unique MAC addresses, and 140 unique IP addresses, with no duplicate identities or malformed MAC addresses. Runtime behavior agreed with the documented observation model: DHCP remained identity evidence rather than liveness evidence; freshness remained separate from operational monitoring; monitoring remained policy-driven; and weak evidence did not overwrite stronger identity. Result: **PASS**.

**Warnings and deferred risks:** This checkpoint establishes the production baseline but does not complete or reorder the remaining corrective sequence. Identity Reconciliation Hardening remains next, followed by the other already-listed inventory correctness tasks. The separate unresolved `mosquitto_pub` issue remained outside scope and was not investigated or modified.

**Final result:** **PASS**

#### Identity Reconciliation Hardening

Status: **COMPLETE**

Objective: Validate and strengthen the canonical identity model itself before additional passive enrichment resumes. Phase 7A.9 confirmed that the current production snapshot has no IP-only identities, duplicate MAC identities, duplicate IDs, or duplicate IPs, and that ARP/DHCP multi-source reconciliation is operating correctly. This checkpoint must establish that supported passive discovery cannot produce persistent duplicate identities under the documented identity model; it is not merely another search for duplicates in one snapshot.

Identity invariants:

- Every physical device has exactly one canonical identity.
- MAC-backed identities supersede weak IP-only identities whenever reconciliation is unambiguous.
- Weak identities cannot persist after successful reconciliation.
- Multiple passive collectors cannot create parallel identities for the same device.
- Collector execution order does not change the final inventory.
- Identity reconciliation is idempotent across repeated collection cycles.
- Ambiguous evidence never causes an incorrect merge.
- Identity provenance remains preserved after reconciliation.
- Future passive collectors participate in the documented canonical identity model.

Required hardening work:

- Review the reconciliation implementation against [DATA_MODEL.md](DATA_MODEL.md).
- Correct any remaining implementation defects found within this checkpoint's scope.
- Add focused regression tests for identity invariants where appropriate.
- Produce production validation evidence after completion.

Completion criterion: Evidence demonstrates that the supported passive-discovery architecture cannot produce persistent duplicate identities under the documented canonical identity model.

Deferred identity architecture decisions remain outside this checkpoint:

- **Historical identity continuity:** A weak IP-based identity may be replaced in current inventory and projections by an unambiguous MAC-backed canonical identity, while historical events or external references may retain the earlier weak ID. HIOC has no formal alias table, promotion record, or historical identity resolution contract. A future explicit architecture checkpoint must decide whether historical identities remain immutable evidence identifiers, resolve through an alias or promotion mapping, or are migrated to canonical identities; this checkpoint must not invent a schema or migration mechanism.
- **Randomized-MAC asset continuity:** Passive reconciliation must not guess that unrelated MAC addresses represent one physical device. Randomized or rotated MAC addresses remain separate discovered identities unless authoritative linking evidence exists. The one-physical-device/one-canonical-identity invariant applies within supported, unambiguous identity evidence. Future operator-approved linking of multiple discovered identities to one asset belongs to the asset-centric Living Digital Twin roadmap, not heuristic passive merging.

##### Identity Reconciliation Production Evidence Report

**Deployment result:** **PASS**. Repository review found that the existing identity-reconciliation implementation already satisfied the documented architecture and required no modification. The authoritative source was synchronized, supported release validation passed, the supported release deployment completed successfully, and production validation completed successfully. Repeated production inventory reconciliation also completed successfully.

**Intended behavior:** Identity reconciliation preserves the documented canonical identity model. Weak identities reconcile into canonical MAC-backed identities only when the evidence is unambiguous; ambiguous evidence never causes an incorrect merge. Repeated reconciliation remains stable, and collector ordering does not change the resulting inventory.

**Validation performed:** Repository validation confirmed that the implementation matches [DATA_MODEL.md](DATA_MODEL.md), focused invariant regression coverage already exists, Python compilation passed, focused tests passed, and the full regression suite passed. Production validation confirmed successful deployment and runtime validation, successful repeated inventory reconciliation, and a stable inventory containing 140 devices and 8 services.

**Invariant checks:** No reconciliation failures or duplicate-identity behavior were observed. Repository regression coverage confirms canonical promotion, collector-order independence, idempotence, ambiguity protection, provenance preservation, duplicate prevention, and centralized reconciliation for future passive collectors. Repository validation and production evidence together demonstrate that supported passive discovery cannot produce persistent duplicate identities under the documented canonical identity model.

**Warnings and deferred risks:** Historical identity continuity, alias mapping, randomized-MAC continuity, and future operator-approved asset association remain intentionally deferred exactly as documented above.

**Final result:** **PASS**

#### FAILED/INCOMPLETE ARP Semantics

Status: **COMPLETE**

The original unresolved-neighbor semantics were confirmed correct: `FAILED`, `INCOMPLETE`, `NONE`, `NOARP`, MAC-less, and other non-durable entries do not create device evidence or refresh positive-observation timestamps. The bounded correction removes duplicate neighbor-table acquisition within one inventory cycle and distinguishes successful empty accepted evidence from total ARP collector unavailability. Discovery-source status and passive device evidence now derive from the same authoritative snapshot.

Implementation commit `8278e54bacb68f25821e6a4981bb01273c32e469` (`Phase 7A: unify ARP snapshot and collector semantics`) preserves `neighbor_table()` as a dictionary-returning compatibility wrapper and keeps `NeighborTableResult`, sanitized exit-code diagnostics, and command-failure details internal. No public schema, topic, entity, dashboard field, event payload, or general driver-framework contract changed.

##### Production Evidence Report

**Deployment result:** **PASS**. The authoritative Windows repository and `origin/main` matched at the implementation commit before PI3 source was fast-forwarded to it. On PI3 NUT&PIHOLE, `bash /home/jazofv1/hioc-release-source/release/validate.sh`, the supported `bash /home/jazofv1/hioc-release-source/release/upgrade.sh`, and `bash /home/jazofv1/hioc/pi4/validate_pi4.sh` all passed. The upgrade created install backup `/home/jazofv1/hioc/backups/install-20260724-194147` and release backup `/home/jazofv1/hioc/backups/release-upgrade-20260724-194146`.

**Intended behavior:** One logical neighbor-table acquisition supplies both discovery-source reporting and `PassiveNetworkDriver`. A successful acquisition with no accepted records reports `arp_table_empty`; failure of both supported commands reports `arp_table_unavailable`. Raw stderr is discarded, diagnostics remain internal, and accepted NUD-state and unresolved-neighbor filtering behavior remain unchanged.

**Invariant checks:** Pre-commit Python compilation passed; inventory/correlation tests passed 111 tests; the complete suite passed 161 tests with 6 skips; release validation and `git diff --check` passed. Production state under `/home/jazofv1/hioc/state/inventory` was online with schema `1.0`, 140 devices, 138 clients, 2 infrastructure devices, 8 services, 280 dependency edges, 139 topology edges, 98 healthy devices, 42 Watch devices, no degraded or offline devices, and lowest health score 75. During the `2026-07-24T19:42:05-06:00` through `2026-07-24T19:42:06-06:00` evidence window, discovery sources were exactly `local_host`, `gateway`, `arp_table`, `dhcp_leases_found`, and `known_infrastructure`; `discovery_limited` was false and `discovery_limit_reason` was empty. Inventory and capability projections remained populated, and no internal result or diagnostic fields appeared in public output.

**Warnings and deferred risks:** Automated regression tests validate the `arp_table_unavailable` path and diagnostic isolation. Production validated the normal successful `arp_table` path and showed no false unavailable or limited state; neighbor collection was not deliberately disrupted to exercise command failure. Dashboard severity mapping, collector canonical ownership, Pi-hole DHCP validation, and passive enrichment remain separate later work.

**Final result:** **PASS**

#### Dashboard Severity Mapping — COMPLETE

Repository review identified two bounded presentation defects. Aggregate Watch wording treated every Watch record as a stale observation even though Watch can also represent expired passive evidence or DHCP-only operational availability that remains unknown. Dashboard v2's Inventory Summary accent also evaluated retained offline or degraded counts before an unavailable inventory status, allowing confident severity styling when current inventory truth was unavailable.

The repository correction uses policy-neutral aggregate Watch wording and makes unknown inventory status take precedence in the affected Inventory Summary style. Detailed per-device `health_reasons`, health computation, health-score thresholds, Watch membership, inventory counts, schemas, the `status.json` contract, MQTT contracts, Home Assistant entities and attributes, incident severity, dashboard layout, and collector and DHCP behavior remain unchanged. The existing blue Watch palette is intentionally preserved; its relationship to the Design System remains deferred to a separate UX/design decision.

##### Production Evidence Report

**Deployment result:** **PASS**. Implementation commit `1e2dcf973d02514561b7bb8a4f5c6f495350ab09` (`Phase 7A: refine dashboard severity presentation`) passed release-source validation and the supported production upgrade. The installed runtime remained `/home/jazofv1/hioc`; install backup `/home/jazofv1/hioc/backups/install-20260727-205938` and release-upgrade backup `/home/jazofv1/hioc/backups/release-upgrade-20260727-205938` were created. `bash pi4/validate_pi4.sh` reported `HIOC Pi4 validation passed.`

**Intended behavior:** Aggregate Watch presentation describes observation or availability review without claiming every Watch condition is stale. Dashboard v2 Inventory Summary styling treats unknown, unavailable, invalid, or otherwise untrustworthy inventory status as higher priority than retained offline or degraded counts. Health and inventory semantics, public contracts, incident presentation, layout, and the existing blue Watch palette remain unchanged.

**Invariant checks:** Production inventory status was `online`, schema version was `1.0`, and status `device_count` matched summary `device_count` at 148. Health categories reconciled exactly: 96 healthy + 52 Watch + 0 degraded + 0 offline = 148 devices. Inventory classes reconciled exactly: 2 infrastructure + 146 clients = 148 devices, and `network_client_count` equaled `client_count` at 146. Both infrastructure devices were healthy with health score 100. Lowest inventory health score was 75; 8 services, 147 topology edges, and 296 dependency edges remained present. Discovery was not limited, the limit reason was empty, and expected sources `local_host`, `gateway`, `arp_table`, `dhcp_leases_found`, and `known_infrastructure` were present.

**Warnings and deferred risks:** The 52 Watch devices are expected operational inventory state and are not a deployment failure. The separate Watch color and Design System UX decision remains explicitly deferred and was not resolved by this checkpoint.

**Final result:** **PASS**

#### Collector Canonical Ownership

Status: **COMPLETE**

The bounded repository implementation corrects two confirmed ownership defects. Collector identity previously depended on local-interface enumeration order and could compose an IP from one interface with a MAC from another. Known-infrastructure enrichment also discarded operator metadata after a legitimate observed IP or hostname change despite an exact normalized MAC match.

Canonical collector IP and MAC now come atomically from one complete interface record. A complete record requires an interface identifier, a valid IPv4 address, and a valid normalized MAC address. The default-route interface, obtained from the existing route discovery source, is preferred. If it has no complete record, selection uses stable ordering by interface identifier, numeric IPv4 address, normalized MAC, and CIDR. Incomplete records are never combined; when no complete record exists, there is no canonical collector selection and local services are omitted rather than assigned to an unrelated device. The full interfaces list remains observational evidence.

Exact normalized MAC matches now establish canonical discovered identity for known-infrastructure enrichment even when configured IP or hostname values are stale. Current observed IP, MAC, hostname, positive-observation timestamps, reachability, and discovery provenance remain authoritative, while supported operator metadata continues to enrich the device and preserve its configured classification. Weaker IP- or hostname-only matches continue rejecting conflicting MAC evidence and ambiguous identities are not guessed together. A MAC change does not imply continuity.

Implementation commit `054fb55a2e70901f3230145b76983c31d2b5ce61` (`Phase 7A: harden collector canonical ownership`) implements the bounded correction. `stable_device_id()` was unchanged. The exact-MAC known-infrastructure continuity behavior was validated by the implementation and regression suite. No inventory schema, stable-ID precedence, MQTT topic or payload, Home Assistant contract, dashboard contract, health behavior, incident behavior, discovery policy, or MAC-change continuity policy changed.

##### Production Evidence Report

**Deployment result:** **PASS**. The PI3 release source was fast-forwarded to implementation commit `054fb55a2e70901f3230145b76983c31d2b5ce61`. Release validation reported `HIOC release validation passed.`, the supported production upgrade completed successfully, and production validation reported `HIOC Pi4 validation passed.` The installed runtime remained `/home/jazofv1/hioc`; release-upgrade backup `/home/jazofv1/hioc/backups/release-upgrade-20260728-114736` and install backup `/home/jazofv1/hioc/backups/install-20260728-114737` were created.

**Intended behavior:** Collector identity is derived from one deterministic complete local-interface record, with default-route preference and atomic IP/MAC ownership. Exact normalized MAC matches preserve supported known-infrastructure metadata across legitimate observed IP or hostname movement while current observed runtime fields remain authoritative. Weaker IP or hostname matches continue rejecting conflicting MAC identities, and no heuristic continuity across MAC changes is inferred.

**Invariant checks:** Pre-commit validation passed with 107 focused inventory tests, 169 full-suite tests and 6 skips, Python compilation, release validation, and final diff review. At `2026-07-28T11:47:56-06:00`, production inventory was online at schema `1.0` with 148 devices, 107 healthy, 41 Watch, 0 degraded, 0 offline, 2 infrastructure devices, 146 clients, 8 services, 147 topology edges, 296 dependency edges, and unrestricted discovery. The canonical collector was `Pi3 - NUT and Pi-hole`, role `Core Infrastructure`, at observed IP `192.168.100.252` and MAC `b8:27:eb:70:ab:df`, online and healthy with health score 100 and sources `known_infrastructure` and `local_host`. All eight discovered services—`pihole-FTL`, `pihole-FTL.service`, network service ports 53 and 67, `cron`, `ssh`, `nut-monitor`, and `nut-server`—were owned by that collector and reported host `Pi3 - NUT and Pi-hole`. No service was assigned to the historical incorrect `.105` owner. Inventory generation remained healthy, discovery was not limited, and no JSON, MQTT, Home Assistant, or dashboard contract failure was observed.

**Warnings and deferred risks:** No checkpoint-specific production warning was observed. Pi-hole DHCP lease ingestion validation and the subsequent passive-enrichment roadmap remain separate work.

**Final result:** **PASS**

#### Pi-hole DHCP Lease Ingestion

Status: **COMPLETE - PASS WITH DOCUMENTED WARNING**

##### Single Snapshot Acquisition

Status: **COMPLETE**

Implementation commit `a01b6b77350ee22a40e8aacca72e256b826c8a3f` (`Phase 7A: unify DHCP lease snapshot acquisition`) establishes one authoritative DHCP lease snapshot per inventory cycle. `discover_inventory()` acquires configured lease sources exactly once into a cycle-local immutable tuple and shares that captured input across discovery-source status, `PassiveNetworkDriver` observations, and central reconciliation. This removes duplicate lease-file acquisition during one inventory cycle while preserving all existing DHCP parsing, assignment-only observation, source-state, deterministic ordering, source-authority, identity, health, topology, dependency, schema, MQTT, Home Assistant, dashboard, and event semantics.

###### Evidence Report

**Implementation validation:** **PASS**. Automated regression tests establish one source acquisition per inventory cycle for one and multiple configured files, immutable snapshot reuse by both consumers, absence of a secondary acquisition, consistent discovery-status and observation inputs for valid, missing, and partial snapshots, and a single sanitized malformed-row warning. Standalone compatibility helpers continue acquiring current results when no snapshot is supplied. The focused inventory suite passed 115 tests; the full regression suite passed 177 tests with 6 skips. Python compilation, release validation, and `git diff --check` also passed.

**Production validation:** **PASS** for externally observable behavior. The release source synchronized successfully, the supported upgrade completed successfully, and production validation completed successfully. Inventory generation succeeded with `dhcp_leases_found` among its discovery sources. The production inventory contained 145 DHCP-backed devices; sampled DHCP-backed records originated from `/etc/pihole/dhcp.leases`, and their lease metadata remained present. No observable inventory regression was reported.

**Important engineering note:** The single-acquisition invariant is an internal implementation property established by automated regression testing, not by production runtime artifacts. Production validation confirms the observable inventory behavior resulting from the implementation but does not expose or prove lease-file acquisition counts. HIOC evidence reports must preserve this distinction between implementation invariants and production observables.

**Intentionally unchanged:** This sub-checkpoint does not alter lease-expiration policy, IPv6 handling, ISC lease compatibility, or discovery-limitation semantics.

**Final result at this sub-checkpoint:** **PASS** for Single Snapshot Acquisition only. The overall Pi-hole DHCP Lease Ingestion checkpoint remained **IN PROGRESS** until the later bounded implementation and production validation recorded below.

##### DHCP Identity Architecture Decision

Status: **COMPLETE - PASS WITH DOCUMENTED WARNING**

The approved architecture is **Pi-hole-specific integration through the existing passive-driver and source-tagged device-record convention**. Pi-hole lease acquisition and parsing remain source-specific adapter functions used by `PassiveNetworkDriver`; valid records enter the existing `DriverResult.devices` flow and central `merge_records()` reconciliation. No new `IdentitySource` protocol, abstract base class, registry, plugin framework, dependency-injection layer, or generalized provider model is introduced. [ADR-0015](../DECISIONS.md#adr-0015-keep-pi-hole-dhcp-within-the-existing-passive-driver-contract) records the binding decision.

This choice preserves the repository's current separation of concerns. Collection adapters acquire and normalize evidence; source-tagged records carry provenance; centralized reconciliation selects canonical identity and field values; known infrastructure supplies limited operator metadata; observation timestamps represent positive observation only; and health, monitoring, topology, dependencies, MQTT publication, and Home Assistant projections consume the reconciled inventory. The existing `DriverResult` mapping convention is already the minimal generic boundary. Adding another identity-source interface would duplicate it and force a classification hierarchy that the current single DHCP implementation does not need.

###### Identity and field ownership

| Field | Approved DHCP contribution |
|---|---|
| MAC address | A valid normalized MAC may create a MAC-backed technical identity or confirm an existing matching identity. It may upgrade one unambiguous IP-only weak identity through existing reconciliation. It never replaces a conflicting MAC or causes ambiguous identities to merge. |
| IP address | Assignment evidence. It may populate the current record and participate in unambiguous reconciliation, but it does not override a stronger current local-host, gateway, ARP, or integration association. A differing passive IP remains stronger current observation evidence. |
| DHCP hostname | Technical identity metadata. It may populate a missing hostname and may win only among DHCP observations by deterministic lease ordering. It does not replace a stronger current passive hostname. |
| Friendly name | DHCP never contributes `name` or future `friendly_name` and never overwrites operator-managed naming. |
| Vendor | DHCP does not contribute or alter vendor information. |
| Lease start | The supported Pi-hole/dnsmasq row does not supply a lease-start value, so none is fabricated. A future source-format decision is required before adding such a field. |
| Lease expiry | Preserved as source attribution metadata in `lease_expires_epoch`. Zero retains its infinite-lease meaning. A finite lease contributes current assignment evidence only when its expiry is later than the inventory cycle's fixed collection epoch. |
| Lease active state | Assignment evidence only. No canonical online, offline, health, reachability, or observation field is derived from it. Presence, active assignment, positive observation, staleness, degradation, and offline state remain distinct. |
| Last seen | Never created or refreshed by DHCP. `_positive_observation` remains false for DHCP records. |
| Online or offline state | DHCP has no direct authority. Expiry never becomes an offline event. |
| Device identity | A valid MAC-backed lease may create a technical inventory record. A hostname-only or unusable-MAC lease cannot. Stable identity remains MAC-first, and conflicts remain separate. |
| Source provenance | Records retain `source: dhcp_leases`, combined canonical `sources`, the source file in `dhcp_lease_source`, and source status in `discovery_sources`. No field-level provenance system is added. |
| Confidence or authority | Deterministic source precedence and ambiguity checks remain sufficient. No numeric confidence score is introduced. |

###### Deterministic conflict and edge-case rules

1. A DHCP record with the same valid MAC as an existing strong identity merges into that identity; stronger current values remain authoritative.
2. One IP-only weak identity and one DHCP MAC-backed identity sharing an IP reconcile only when the existing central rules find exactly one weak identity, one strong identity, and no conflicting MAC.
3. A conflicting passive hostname outranks the DHCP hostname. A DHCP hostname may fill a missing hostname.
4. DHCP never contributes `name` or `friendly_name`, so operator naming remains unchanged.
5. When DHCP reports a different IP from a stronger recent passive observation, the passive IP remains canonical and the DHCP assignment remains source evidence.
6. An expired finite lease contributes no current assignment evidence, is not positive observation, does not enrich or refresh a retained device, and never proves offline.
7. Multiple leases for one MAC remain separate input observations until central deterministic selection; the established ordering selects the infinite lease first, otherwise the greatest expiry, followed by stable source and value tie-breakers.
8. The same IP associated with different MACs produces separate MAC-backed identities. It never authorizes a merge; ambiguous weak reconciliation is skipped.
9. Malformed, unsupported, or incomplete rows contribute no identity record. Sanitized warnings and source health preserve malformed, unsupported, partial, unreadable, I/O-error, missing, disabled, empty, and found distinctions.
10. A hostname with no usable MAC is rejected by this Pi-hole lease path and cannot create an IP-only or hostname-only device.
11. A valid MAC with a blank or `*` hostname is accepted without fabricating a hostname.
12. No archived-asset schema or retention policy exists. Later implementation must preserve retained canonical records and must not invent archive revival or deletion behavior.
13. Temporary source unavailability contributes no new evidence, preserves prior inventory through existing retention behavior, and reports the established source status and discovery limitation semantics.
14. Successful collection with zero leases contributes no devices and reports `dhcp_leases_empty`; it is not treated as failure, device disappearance, or offline evidence.

###### Implementation Evidence Report

**Implementation validation:** **PASS**. Pi-hole/dnsmasq rows now use one fixed collection epoch per inventory cycle. Active finite IPv4 leases and expiry-zero infinite leases remain eligible; expired finite leases, IPv6 entries, clearly recognized ISC lease blocks, malformed rows, and unusable identities contribute no device evidence. Expired leases cannot enrich, move, refresh, or mark retained devices offline. DHCP remains assignment-only and cannot overwrite stronger current MAC-backed, local-host, gateway, ARP, integration, known-infrastructure, or operator-managed metadata.

Source aggregation now preserves complete `found`, `empty`, and explicitly `disabled` states; distinguishes missing, unreadable, malformed, unsupported, I/O-error, and partial input; and reports configured incomplete or unavailable DHCP evidence as a discovery limitation independently of integration evidence. Existing inventory and all other discovery sources remain preserved. The default source is the production-confirmed `/etc/pihole/dhcp.leases`; other dnsmasq-format files require explicit configuration, and ISC `dhcpd.leases` is not advertised as supported.

The focused identity checks passed 6 tests, the inventory suite passed 123 tests, the correlation suite passed 12 tests, and the full regression suite passed 191 tests with 7 skips.

###### Production Evidence Report

**Deployment result:** **PASS**. Implementation commit `be9035a0641f16cdfc5c8aa1b090056c519881b7` was deployed through the supported production upgrade, which exited 0 and created install backup `install-20260729-102325` and release-upgrade backup `release-upgrade-20260729-102325`. The general PI3 validator passed with exit code 0 and confirmed that at least one configured DHCP lease file was readable. The inventory engine exited 0 and regenerated valid `inventory.json`, `devices.json`, `services.json`, `capabilities.json`, `topology.json`, `dependencies.json`, `summary.json`, and `status.json` artifacts.

**Intended behavior:** Pi-hole DHCP ingestion reads eligible active IPv4 dnsmasq leases, preserves assignment provenance and expiry metadata, reconciles them with stable MAC-backed identities, and does not treat DHCP evidence as positive liveness, a health reason, or direct online or offline authority. Canonical-address selection remains governed by existing reconciliation and was not changed by this checkpoint.

**Invariant checks:** At collection time the source contained 140 nonblank rows, all 140 of which were valid active finite IPv4 leases with 140 unique MACs, IPv4 addresses, and MAC/IP pairs. There were no expired, infinite, IPv6, ISC, or malformed source rows. All 140 active lease MAC identities were represented in the canonical inventory. The 150-device inventory contained 147 DHCP-backed canonical identities, all with DHCP provenance and lease-expiry metadata, with no missing or unexpected source path. DHCP-backed records did not assert `_positive_observation=true`, add DHCP or lease text to health reasons, or directly assert online or offline from DHCP-only evidence. Discovery reported `dhcp_leases_found`, `discovery_limited=false`, and an empty limit reason. Seven DHCP-backed identities beyond the 140 active leases were retained expired historical canonical records with no corresponding active lease, consistent with persistent inventory behavior rather than duplicate active ingestion.

**Warnings:** One active lease MAC/IP pair did not match the chosen canonical IP, although the active lease MAC identity was represented. The same MAC owned two simultaneous `STALE` neighbor-table addresses: one was the selected canonical IP and the other was the active DHCP lease IP. The lease IP had no conflicting active DHCP owner. This exposes a separate canonical-address selection concern, not a DHCP ingestion failure. The mismatch was not resolved by this checkpoint, and DHCP assignment evidence alone must not be allowed to fabricate liveness in the future correction.

**Final result:** **PASS WITH DOCUMENTED WARNING**. Pi-hole DHCP Lease Ingestion is complete. Canonical-address selection remains unchanged and is retained as a separate Phase 7A hardening checkpoint. Active Discovery remains postponed.

##### Resolved DHCP Implementation Decisions

- **Expired finite-lease policy:** Only finite leases with expiry later than the fixed cycle epoch contribute current assignment evidence. Expiry zero remains infinite.
- **ISC `dhcpd.leases` compatibility:** ISC syntax is unsupported and is no longer included in default source paths.
- **IPv4 / IPv6 contract:** This ingestion path is IPv4-only. IPv6 rows are unsupported.
- **Explicit empty-list behavior:** An explicitly blank configured path list disables DHCP acquisition and reports `dhcp_leases_disabled`; absent configuration uses the Pi-hole default.
- **Discovery-limitation semantics:** Found, empty, and disabled are complete states. Missing, unreadable, malformed, unsupported, I/O-error, and partial configured input limit discovery independently of integration evidence.

These decisions and the production Evidence Report complete the bounded Pi-hole DHCP Lease Ingestion checkpoint.

#### Canonical Address Selection Hardening

Status: **COMPLETE - PRODUCTION VALIDATED**

Production DHCP validation demonstrated that one MAC may have multiple neighbor-table IP entries and that multiple entries may simultaneously be `STALE`. The current canonical selector may choose a stale non-DHCP address even when the active DHCP lease address is also present in the neighbor table, owned by the same MAC, and has no conflicting active DHCP owner.

This checkpoint must investigate and define deterministic canonical-address precedence using source authority, observation recency, neighbor state, lease validity, and existing identity invariants. Any correction must preserve stable MAC-backed identity, prevent duplicate canonical identities, and must not allow DHCP assignment evidence alone to fabricate liveness. It must include regression validation, supported production validation, and a Production Evidence Report. This work is distinct from the completed Collector Canonical Ownership and Pi-hole DHCP Lease Ingestion checkpoints.

Repository implementation now preserves neighbor state as private reconciliation
evidence and selects canonical IPv4 through one explicit, order-independent
comparator. Local collector, gateway, configured integration, `REACHABLE`, and
`PERMANENT` evidence outrank active DHCP; active DHCP outranks `DELAY`, `PROBE`,
unknown fallback ARP, and `STALE`; unusable neighbor states cannot become
preferred operational addresses. Equal evidence uses lease validity/expiry,
observation epoch, and numeric IPv4 tie-breaking. Selection remains separate
from MAC-backed identity, positive observation, health, and retention.

The repository defect reproduction, contract, source map, downstream review,
validation record, warnings, and pending production requirements are in the
[Canonical Address Selection Hardening Evidence Report](CANONICAL_ADDRESS_HARDENING_EVIDENCE.md).
At that implementation stage, the checkpoint remained open until supported
deployment, production evidence, and documentation closeout passed.

The first governed production run deployed implementation commit
`839e924b2249bec736ff74d9a2ac593c7fee6bb8` successfully and passed artifact,
release, runtime, identity, provenance, monitoring, health, and bounded
unrelated-device checks. Its final result was invalidated by the validation
procedure: it admitted a link-local IPv6 `STALE` neighbor, failed to exclude
higher-authority configured integration evidence, and incorrectly required
every active DHCP address to become canonical. The retained `.251` PI5 address
therefore does not prove an ADR-0018 failure. Rollback was not performed.

Revised repository-owned validation distinguishes `PASS`,
`NO_QUALIFYING_CANDIDATE`, and genuine `FAIL`; only genuine failure recommends
rollback. Separately, active DHCP evidence for retired PI5 address `.152`
remains an unresolved production finding. Read-only PI3 evidence must identify
its source, expiry, reservation/configuration status, interface ownership, and
recent DHCP activity before any DHCP cleanup or parser follow-up is proposed.
At that first-run stage, the comparator remained deployed and the checkpoint
remained **IN PROGRESS**.

A second production validator execution passed comparator identity and all six
real Boolean invariants, with 151 devices before and after and zero unrelated
canonical-address changes. No candidate qualified because PI5 had current
`REACHABLE` IPv4 `.251`, DHCP IPv4 `.152`, and only an IPv6 link-local `STALE`
neighbor. Generic truthiness incorrectly treated diagnostic metadata value
`_unrelated_canonical_change_count: 0` as a failed invariant and returned
`FAIL`. Rollback was not performed. The corrected validator requires exactly
the six documented Boolean invariants, preserves underscore-prefixed metadata
without evaluating it, and rejects missing, mistyped, or unexpected public
keys explicitly. The expected evidence result was
`NO_QUALIFYING_CANDIDATE`, pending the strict PI3 rerun recorded below.

The `.152` finding is separately recorded as an unexpired old lease with no
renewal observed during the bounded 60-second check. It remains an
infrastructure-evidence finding and does not change ADR-0018 or justify
comparator rollback.

Final strict validation synchronized clean source commit
`b3621c3765e56b9741565ac58be6a5fad4d0f302` and retained the unchanged
comparator from `839e924b2249bec736ff74d9a2ac593c7fee6bb8`. Source and runtime
bytes matched Git-derived SHA-256
`35f36916399331a6e1129f7a49ba86933960eca8e94d6b30c80e9be3d7cd75b8`.
All six Boolean invariants passed; inventory stayed at 151 devices; diagnostic
metadata recorded one unrelated canonical-address change within the approved
bound; and no input errors occurred. With no qualifying candidate, the
successful result was `NO_QUALIFYING_CANDIDATE`, exit code 0, with no rollback
recommendation or action.

Both earlier failures were validator defects: the first imposed unconditional
DHCP precedence and admitted link-local IPv6; the second applied Boolean
truthiness to numeric diagnostic metadata. The strict typed contract resolved
both. Canonical Address Selection Hardening is production validated and
**COMPLETE**. The `.152` lease residue and DHCP Service Health & Capacity
Monitoring remain separate future work.

#### July 29 DHCP Pool Exhaustion Incident - RESOLVED

The production address-allocation failure was caused by exhaustion of the former `192.168.100.50 - 192.168.100.150` dynamic pool. The operator expanded it to `192.168.100.50 - 192.168.100.250`; a previously failing client immediately obtained a lease; critical static networking and infrastructure services were validated; and HIOC deployment validation passed. The permanent evidence report is [INCIDENT_2026-07-29_DHCP_POOL_EXHAUSTION.md](INCIDENT_2026-07-29_DHCP_POOL_EXHAUSTION.md). This resolved incident motivates a future DHCP capacity-monitoring phase but does not alter the current Phase 7A corrective sequence.

#### Remaining Phase 7A Corrective Sequence

1. Repository and Deployment Hygiene - **COMPLETE**.
2. Phase 7A.9 Passive Inventory Correctness Validation — **COMPLETE**.
3. Remaining inventory correctness work: Identity Reconciliation Hardening — **COMPLETE**; FAILED/INCOMPLETE ARP semantics — **COMPLETE**; Dashboard Severity Mapping — **COMPLETE**; Collector Canonical Ownership — **COMPLETE**; Pi-hole DHCP Lease Ingestion — **COMPLETE WITH DOCUMENTED WARNING**; and Canonical Address Selection Hardening — **COMPLETE; PRODUCTION VALIDATED**.
4. Resume passive enrichment.
5. Continue toward asset-centric inventory.
6. Design and approve retention and archival policy.
7. Complete Phase 7A.
8. Begin Phase 7B Safe Active Discovery.

Repository and Deployment Hygiene, Release Boundary Hardening, Phase 7A.9, Identity Reconciliation Hardening, FAILED/INCOMPLETE ARP semantics, Dashboard Severity Mapping, Collector Canonical Ownership, Pi-hole DHCP Lease Ingestion, and Canonical Address Selection Hardening are complete. Passive enrichment may resume in its documented order; the separate `.152` DHCP residue and DHCP service-health roadmap work remain open.

#### Passive Enrichment Architecture and Specification

Status: **PE-0 COMPLETE; PE-1 COMPLETE - PRODUCTION VALIDATED; PE-2.0 COMPLETE - DESIGN APPROVED; PE-2.1 DESIGN APPROVED; PE-2.1 EXECUTABLE IMPLEMENTED - REPOSITORY VALIDATED; PE-2.1 PRODUCTION PENDING**

The implementation-ready design is maintained in
[PASSIVE_ENRICHMENT_ARCHITECTURE.md](PASSIVE_ENRICHMENT_ARCHITECTURE.md). It
maps every current passive source, audits the permissive inventory schema,
separates observed, derived, operator-managed, and relationship metadata, and
defines field-level authority, provenance, confidence, conflict, privacy, and
rollback contracts.

The completed minimum implementation is a parallel, local-only hostname
evidence envelope. It proved deterministic candidate selection and
conflict preservation without changing identity, canonical address, public
inventory, MQTT, Home Assistant, dashboards, incidents, liveness, health, or
retention. Repository implementation, governed deployment, Git-derived
artifact identity, authoritative schema validation, and corrected production
validation passed. Production reported `online`, 153 records, 83 candidates,
82 selections, and zero conflicts. Expected availability, permanent-IoT monitoring, Home Assistant
availability correlation, automation impact, incidents, retention, DHCP
service health, and `.152` lease cleanup remain separate future work.

The permanent design distinguishes **Observation** (what passive sources saw),
**Enrichment** (what HIOC learned or inferred), and **Asset** (what the operator
knows and intends). These layers have separate authority, mutability,
persistence, provenance, privacy, and operational meaning. They reference one
another without destructive transformation. PE-0 is complete and design
approved. The PE-1 package in
[PE1_HOSTNAME_ENRICHMENT_SPEC.md](PE1_HOSTNAME_ENRICHMENT_SPEC.md) is
implemented, deployed, and production validated. It adds only private local
sidecars and does not change public inventory or consumer/operational contracts.
The absence of trusted-integration, historical, and conflict candidates in the
validated production snapshot is acceptable. PE-2.0 is design approved in
[PE2_ASSET_FOUNDATION_SPEC.md](PE2_ASSET_FOUNDATION_SPEC.md). It defines a
separate stable-ID-keyed, local-only Asset store and governed CLI for
`friendly_name`, `physical_location`, `purpose`, and private `notes`, while
deferring owner, public projection, expected availability, lifecycle, and
identity migration. The PE-2.1 implementation design is approved in
[PE2_ASSET_IMPLEMENTATION_DESIGN.md](PE2_ASSET_IMPLEMENTATION_DESIGN.md), while
executable implementation remains not started. The Git
commit containing this documentation closure is the authoritative completion
commit; its hash is reported after commit to avoid a self-referential
documentation identity. Repository evidence is in
[PE1_HOSTNAME_ENRICHMENT_EVIDENCE.md](PE1_HOSTNAME_ENRICHMENT_EVIDENCE.md).

---

## Planned Phase

### Phase 7B - Safe Active Discovery

Status:

Not started.

This phase is intentionally postponed until Phase 7A is complete.

Goals include:

- Manual discovery
- Scheduled low-frequency discovery
- Safe network probing
- No continuous scanning
- No aggressive port scanning

---

### Future Phase - DHCP Service Health & Capacity Monitoring

Status: **PLANNED; NOT IMPLEMENTED**

Originating production evidence: [July 29, 2026 DHCP Pool Exhaustion Incident](INCIDENT_2026-07-29_DHCP_POOL_EXHAUSTION.md). This phase does not supersede Phase 7A, its corrective checkpoints, or postponed Phase 7B.

#### Pool Utilization

Plan monitoring for configured pool size, active leases, free addresses, utilization percentage, configurable warning and critical thresholds, exhaustion, and trend over time.

#### Lease and Transaction Failures

Plan detection of repeated unsuccessful client acquisition attempts without assuming every failure is capacity-related. Future design must evaluate DHCP `DISCOVER`, `OFFER`, `REQUEST`, `ACK`, `NAK`, declines, timeouts, repeated attempts, and incomplete exchanges. Packet capture may be evaluated as a design option but is not selected by this plan.

#### Selective Allocation Failure

Detect the condition where the DHCP daemon is active and some clients retain connectivity while new or renewing clients cannot obtain usable leases. Daemon-up status alone is insufficient.

#### Planned Health and Incident Semantics

Interpret service evidence through existing project conventions for healthy, warning, degraded, critical, and unavailable states. Plan stable incident lifecycle behavior for high and critical utilization, exhaustion, unanswered requests, missing OFFER or ACK behavior, abnormal lease churn, transaction failures, selective degradation, recovery, and resolution. Do not implement or conflate the deferred incident-history validator rewrite.

#### Planned Dashboard Visibility

Plan current DHCP health, utilization, free capacity, trend, active warning or incident, recent transaction failures, affected-client count where measurable, and last successful DHCP activity. No HIOC dashboard endpoint or port is established by this phase.

#### Future Production Validation

Validation must cover normal capacity, warning threshold, critical threshold, full pool, successful lease recovery after capacity restoration, selective client failure, daemon healthy while service is degraded, incident creation and resolution, dashboard accuracy, and no false offline state for retained leases. Implementation, tests, deployment, production Evidence Report, and documentation closeout are all required before this phase may be complete.

---

## Future Enhancements

Potential future work includes:

- Dependency graph visualization
- Infrastructure topology
- Automatic service relationships
- Failure propagation visualization
- Historical infrastructure trends
- Predictive recommendations
- Expanded operational analytics
- Backup and disaster recovery

These items remain intentionally out of scope until the current roadmap reaches them.

### Phase 7A Continuity and Deferred Hardening

Phase 7A remains focused on trustworthy passive discovery and enrichment. Completed corrective checkpoints, including Watch-device discoverability, remain part of that foundation. Deferred Phase 7A work remains preserved:

- Configurable passive-client retention and archival, after asset policy is designed.
- Canonical local-address hardening without production-specific identity exceptions.
- An explicit historical identity continuity decision covering immutable evidence IDs, alias or promotion resolution, and migration policy without presupposing a schema.
- Continued Phase 7A enrichment from passive sources.

Active Discovery remains postponed. Future YAML dashboard deployment modernization also remains planned and must not be folded into unrelated inventory checkpoints.

### Asset-Centric Evolution

After reliable passive identity is established, Living Inventory should gradually evolve from unknown technical devices into identified, operator-managed assets. Planned capabilities include:

- Operator asset identity and friendly naming.
- Physical location and purpose.
- Owner or responsible person.
- Asset classification and operational criticality.
- Expected availability and explicit monitoring expectations.
- Asset lifecycle state, including active, retired, and archived concepts.
- Maintenance expectations, purchase or installation context, maintenance history, notes, and optional photo references.
- An operator workflow for physically matching discovered MAC addresses and other stable evidence to real assets.
- Operator-approved asset linkage that may associate multiple discovered identities, including identities created by randomized or rotated MAC addresses, with one physical asset without heuristic passive merging.
- Gradual enrichment from an unknown device to an identified, managed asset without losing discovery provenance.
- Safe configurable retention and archival governed by asset policy rather than stale age alone.

These are future concepts. They do not add runtime fields or change current health, monitoring, incident, retention, or discovery behavior.

### Roadmap Dependencies

- Stable identity and passive discovery are foundational to operator asset enrichment.
- Asset classification must exist before aggressive archival can be safe.
- Expected availability must be defined before disappearance can be treated as failure.
- The improved dependency graph, automatic service relationships, failure propagation visualization, and infrastructure topology become more meaningful after assets and services are identified.
- Historical infrastructure trends and predictive recommendations depend on reliable identity, asset classification, relationships, and retained history.

The asset-centric vision expands the meaning of future work; it does not replace or reorder any existing phase or capability.

---

# Repository and Deployment Governance

HIOC formally separates the authoritative source checkout from the deployed production runtime:

```text
GitHub
  |
  v
/home/jazofv1/hioc-release-source
  authoritative source checkout for release execution on PI3
  |
  | release validation and the supported release process
  v
/home/jazofv1/hioc
  deployed production runtime
```

Deliberate source changes are developed and validated in an authorized development checkout, then committed and pushed to GitHub as the shared project history. After the approved changes are pulled on PI3, `/home/jazofv1/hioc-release-source` is the authoritative source checkout for release preparation and the supported release workflow. It should remain clean except for deliberate release work in progress.

`/home/jazofv1/hioc` is the deployed production runtime. It is expected to contain persistent operator configuration, runtime state, incident and inventory history, logs, backups, generated files, installer-managed permissions, and other operational artifacts. Production updates must use the supported release process from the authoritative source checkout or a validated release package, not direct Git updates inside the runtime.

The current repository workflow was not introduced through a single planned migration. It evolved organically as operational experience demonstrated the need to separate a clean development and release checkout from the production runtime. This document formalizes that proven workflow rather than introducing a new architectural model.

The production runtime is formally a non-Git deployment target. Its historical `.git` directory was residue from the former clone-in-place installation model, not an operational dependency, and has been retired. The authoritative Windows repository, GitHub, and `/home/jazofv1/hioc-release-source` own Git history and source operations. Retirement preserved configuration, state, history, logs, backups, credentials, permissions, and all other operational data.

## Repository and Deployment Hygiene Checkpoint

Status: **COMPLETE**

The source/runtime architecture is settled and is not being reopened. The Windows repository work, PI3 release-source audit, runtime provenance audit, controlled runtime Git quarantine and removal, production engineering validation, upgrade proof, rollback proof, and source/runtime consistency validation are complete. All Repository and Deployment Hygiene closure criteria are satisfied.

### Release Boundary Hardening

Status: **COMPLETE**

**Engineering problem:** `release/build.sh` previously traversed the working directory and attempted to protect the release through exclusion patterns. Git ignore rules did not participate in that traversal, so an ignored or untracked workspace artifact could enter a release unless it happened to match a build-specific exclusion. Release contents could therefore depend on workspace residue rather than solely on intentional repository source.

**Implemented solution:** Release construction now obtains its complete source set from the repository index through Git's NUL-delimited tracked-file listing. Each copied file is included because it is explicitly tracked; ignored, untracked, cache, recovery, and temporary files are outside the source set without relying on filename exclusions. This preserves the existing build directory, version lookup, project-file layout, and downstream package and deployment flow. `RELEASE_MANIFEST.txt` remains the one intentionally generated build file and now records stable version, build, and source-commit values without checkout-path or wall-clock fields.

**Validation:** Focused release tests prove that the build is Git-aware, uses a NUL-safe tracked-file stream, does not fall back to workspace traversal or a special `*.tmp` exclusion, and produces a checkout-independent manifest. The then-existing ignored `hioc_known_hosts.tmp` file was retained during this sub-checkpoint as validation evidence and was excluded because it was not tracked, as are arbitrary future ignored or untracked artifacts; its later workspace disposition is recorded under Repository Governance Reconciliation. Tracked project files remain the build input. Focused release and version tests, the full regression suite, Python compilation, shell syntax validation, release validation, and direct build-content comparison passed. No runtime, inventory, Home Assistant, deployment, upgrade, validation, or public-contract behavior changed.

### Changelog Governance Reconciliation

Status: **COMPLETE**

Git history establishes the intended single-authority model. Documentation-governance commit `5b2fe6ed2a4f7916032198c4ecaf645aa3937b72` migrated released-work history into `docs/CHANGELOG.md`, declared that file's ownership, converted root `CHANGELOG.md` into a discoverability pointer, and directed README readers to the authoritative docs path. Implementation commit `054fb55a2e70901f3230145b76983c31d2b5ce61` later replaced the root pointer with a bounded Collector Canonical Ownership implementation entry. Subsequent production-validation and closeout work correctly updated `docs/CHANGELOG.md`, leaving the duplicate root entry stale.

The original governance model is restored: `docs/CHANGELOG.md` is the single authoritative record of released and delivered work, and root `CHANGELOG.md` is a pointer retained for conventional repository discoverability. Future release and completed-checkpoint entries must be written only to `docs/CHANGELOG.md`. A second overlapping full changelog is prohibited unless a separately approved governance decision establishes a distinct, non-overlapping purpose. Git history preserves all earlier root content, so the pointer loses no historical traceability. README already targets the authoritative file; release and installer tooling merely exclude the root source-only path and require no change.

The stale Collector Canonical Ownership statement is removed from the active root pointer. The authoritative changelog and Master Plan record the complete evidence chain: implementation, regression validation, production validation, and documentation closeout all completed. Documentation links, release-contract tests, the full regression suite, and `git diff --check` passed. No application, release, deployment, test, inventory, or Home Assistant behavior changed.

### Repository Governance Reconciliation

Status: **COMPLETE**

Decision date: **2026-07-28**

Every remaining Windows repository governance artifact has an explicit disposition:

| Artifact | Evidence | Disposition |
|---|---|---|
| `validation/phase-7a8-lifecycle` | Its sole branch-only commit, `be7b69d1da1a3b5c3c7a9e7ca27d1280b8f41cd1`, adds the asset-lifecycle foundation and is not an ancestor of `main`. `docs/RECOVERY_BASELINE.md` identifies that exact commit and tree as the approved Phase 7A.8 recovery candidate. No tag or other branch preserves it. | **Retained intentionally**, locally and on `origin`, as the named reachability reference for the immutable approved recovery candidate. It is not approved for merge into `main`; future disposition requires a separate evidence-based decision that preserves the recovery reference. |
| `correlation-engine-v2` | Tip `42ea8d2d1ebeecc6e18aff6bb35dccea00e86426` is an ancestor of `main` through merge commit `80411124e584da17c8f532dbae0cd54a638ef181`; no unique commit remains. Its remote branch was already absent. | **Resolved:** deleted locally. Commit history remains reachable from `main`. |
| `docs/reconcile-phase-7a8-recovery-baseline` | Tip `0463a648b93626ca8a0570654cb4074ed21a01aa` is an ancestor of `main` through merge commit `f20b161b1a0f7cb59d994f25f1bf84d1d0e8db96`; its recovery documentation remains on `main`. | **Resolved:** deleted locally and remotely. Commit history remains reachable from `main`. |
| `docs/repository-deployment-governance` | Tip `8174187c04591319374e2f72c37dac9e731c5a5c` is an ancestor of `main` through merge commit `8a35d6d3746cf001a88b558f63d673797262ec43`; its governance documentation remains on `main`. | **Resolved:** deleted locally and remotely. Commit history remains reachable from `main`. |
| `hioc_known_hosts.tmp` | The ignored root file contained one SSH host-key line and had no Git history. No runtime, release, deployment, or automation code consumed it; a focused regression assertion mentions its name only to prove that it is absent from Git-tracked release inputs and does not require the file to exist. SSH host trust is user-workspace state, not project source. | **Resolved:** removed from the repository workspace. Future SSH known-host artifacts must be stored in the user's SSH configuration area or another external temporary location, never in the repository. |

The retained lifecycle branch is not stale or ambiguous: it has a documented recovery-evidence purpose and must remain until a separately approved archival or integration decision provides an equally durable reference. Fully merged topic branches should be removed after their merge and evidence are verified. Temporary access artifacts must remain outside the repository. These rules preserve historical reachability without treating completed topic branches or user-specific access state as active project source.

Validation confirmed the retained branch at its documented commit, all removed branch tips reachable from `main`, no dangling or broken Git references, valid Markdown links, a passing full regression suite, and a clean documentation diff. No application, release, deployment, inventory, Home Assistant, or runtime behavior changed.

### Runtime Git Metadata Retirement

Status: **COMPLETE**

The architectural investigation reviewed runtime code, installers, release build and packaging, upgrade, backup, rollback, validation, uninstall, version reporting, recovery documentation, operator workflows, ADRs, tests, and relevant Git history. It found no supported runtime, installation, validation, versioning, upgrade, rollback, or disaster-recovery dependency on `/home/jazofv1/hioc/.git`. Runtime version identity comes from `VERSION.yaml` and release metadata. Git is used only at the authoritative source boundary. The runtime `.git` directory is historical residue from the original installation model in which the production path was also a clone.

ADR-0013 is resolved: `/home/jazofv1/hioc` is a non-Git deployment target, all Git operations belong to an authoritative development repository or `/home/jazofv1/hioc-release-source`, and direct runtime Git workflows are unsupported. README installation guidance now uses the release-source workflow. Installation and deployment already excluded `.git`; this repository implementation additionally excludes `.git` from new upgrade backups and from rollback restoration. The rollback exclusion applies to historical backups and nested `.git` directories without excluding other hidden files. Existing protections for `config`, `state`, `history`, `logs`, `backups`, credentials, permissions, and installer-managed data remain unchanged.

Repository validation established the exact backup, deployment, and rollback contracts; continued persistent-state exclusions; `VERSION.yaml` as runtime version authority; Git-aware source construction only in the authoritative checkout; shell syntax; release build and package validity; documentation-link integrity; contradiction-free active guidance; the complete regression suite; and a clean diff. Focused release and version tests passed 13 tests with one Windows-only `rsync` availability skip. The full suite passed 183 tests with 7 skips. Python compilation, release validation, shell syntax, Markdown link checks, package construction, required-file checks, and archive inspection for `.git` all passed. The executable `rsync` semantics test preserves legitimate hidden files while excluding root and nested `.git` directories and will run on hosts where `rsync` is installed, including PI3. Repository implementation and documentation are committed and pushed together only after these checks pass.

Production migration, engineering validation, and quarantine removal are complete. `/home/jazofv1/hioc` is formally non-Git. Its historical `61/62 commits behind` condition is permanently resolved because that status described stale, intentionally excluded runtime metadata rather than deployed application content, and the runtime is no longer a Git checkout.

#### Production Evidence Report

**Deployment result:** `/home/jazofv1/hioc-release-source` was synchronized at commit `5d189535d81a5689b9d5f0d96caba49d3fee609c` with clean `main` matching `origin/main`. The supported hardened upgrade completed. Runtime Git metadata was moved to `/home/jazofv1/hioc-hygiene-evidence/runtime-git-quarantine-20260729T001505Z/runtime.git`, validated, and then removed after approval. `/home/jazofv1/hioc/.git` does not exist, the runtime is not a Git working tree, and quarantine removal reported `PASS`.

**Intended behavior:** The production runtime operates without Git metadata. Supported deployment, upgrade, backup, rollback, validation, version reporting, and recovery continue through release artifacts and `/home/jazofv1/hioc-release-source`. Runtime state and legitimate hidden files remain protected. Runtime Git metadata cannot be recreated by upgrade or restored by rollback.

**Validation performed:** The historical runtime repository reported HEAD `94e1997f0d9df9e43209e44f7eb62a8d808714cc`, while its stale `origin/main` reference was `5d189535d81a5689b9d5f0d96caba49d3fee609c`. Its HEAD was an ancestor of authoritative history; no runtime-only commits, branches, tags, or stashes existed. The approximately 2.6 MB repository was quarantined, remained readable, and passed `git fsck --full`. Pre-migration evidence at `/home/jazofv1/hioc-hygiene-evidence/pre-migration-20260728T231517Z` inventoried 17,449 runtime paths, checksummed 72 deployment-managed files, recorded persistent directories and Git provenance, and included an evidence checksum manifest. `pi4/validate_pi4.sh` passed after quarantine. A subsequent supported non-Git upgrade and controlled rollback both completed, left the runtime non-Git, and passed production validation. Post-rollback SHA-256 comparisons matched release source and runtime for `release/upgrade.sh`, `release/rollback.sh`, `release/validate.sh`, `pi4/validate_pi4.sh`, and `VERSION.yaml`.

**Invariant checks:** Upgrade backup `/home/jazofv1/hioc/backups/release-upgrade-20260728-181815`, install backup `/home/jazofv1/hioc/backups/install-20260728-181815`, and the plain-text `last-upgrade-backup` pointer were valid. Rollback from that release-upgrade backup did not restore `.git`. `VERSION.yaml` remained valid. Binaries, configuration, runtime state, JSON projections, cron entries, DHCP lease access, version declarations, validators, and persistent runtime data remained operational and intact. Checked deployment artifacts matched the authoritative release source after rollback.

**Warnings / remaining action:** No Repository and Deployment Hygiene engineering work remains. Interactive console sessions that closed during evidence collection are not classified as HIOC failures: upgrade, rollback, and validation completed successfully, and pasted commands used persistent interactive `set -euo pipefail` with visible paste corruption. Future interactive validation should contain strict mode inside a script or subshell and capture output and exit status so the outer session remains open.

**Final result:** **PASS; REPOSITORY AND DEPLOYMENT HYGIENE COMPLETE**

Closure requires every item below:

- [x] hardened backup behavior validated;
- [x] hardened rollback behavior validated;
- [x] documentation reconciled through the production Evidence Report working-tree update;
- [x] runtime `.git` provenance captured;
- [x] unique runtime-only commits ruled out;
- [x] runtime `.git` quarantined outside both repositories;
- [x] production validation passes without runtime `.git`;
- [x] supported upgrade does not recreate `.git`;
- [x] supported rollback does not restore `.git`;
- [x] persistent `config`, `state`, `history`, `logs`, and `backups` remain intact;
- [x] quarantine copy removed after final approval;
- [x] production Evidence Report recorded in this working-tree update;
- [x] final documentation closeout prepared and validated;
- [x] Windows `main`, `origin/main`, and PI3 release-source synchronization established for the validated implementation baseline;
- [x] documentation-only working-tree scope confirmed for final review.

The overall Repository and Deployment Hygiene checkpoint is complete. Runtime migration, production validation, supported upgrade and rollback proof, quarantine removal, evidence documentation, and repository-scope validation are complete.

**Remaining Repository and Deployment Hygiene checkpoints:**

None. Repository and Deployment Hygiene is complete.

Repository and runtime artifacts use these disposition categories:

| Category | First-pass classification |
|---|---|
| AUTHORITATIVE SOURCE | GitHub `main` and the clean source checkout at `/home/jazofv1/hioc-release-source`. |
| DEPLOYED APPLICATION | `pi4/bin/`, `pi4/lib/`, required runtime configuration examples and support files, and `homeassistant/`. Preserve. |
| PERSISTENT RUNTIME DATA | `config/`, `state/`, `history/`, and `logs/`. Preserve. |
| DEPLOYMENT TOOLING | `release/`, `pi4/install_pi4.sh`, `pi4/uninstall_pi4.sh`, `pi4/validate_pi4.sh`, `homeassistant/install_ha.sh`, `homeassistant/validate_ha.sh`, and `VERSION.yaml`. Preserve pending dependency review. |
| BACKUP / ARCHIVE | `backups/`. Preserve pending backup and retention review. |
| GENERATED / TRANSIENT | `__pycache__/`, `*.pyc`, `.pytest_cache/`, and similar generated caches. Cleanup candidates only after validation. |
| SOURCE-ONLY | `README.md`, `ROADMAP.md`, `DECISIONS.md`, `CHANGELOG.md`, and `docs/` remain in authoritative source and are excluded from production deployment. |
| SOURCE / RELEASE VALIDATION | `tests/` is used by `release/validate.sh` in the source or release-validation context and is excluded from production deployment. |
| RETIRED HISTORICAL RUNTIME METADATA | The production runtime's former `.git/` directory was proven historical residue, quarantined, validated, and removed after approval. It was not source, runtime state, or a recovery dependency. |

### Dependency Review Findings

The initial dependency review is complete for the current provisional source-only candidates. It reflects the evidence gathered against the current deployment architecture and establishes the baseline for subsequent deployment-manifest validation. No runtime, cron, systemd, installer, rollback, Home Assistant, or other operational dependency was discovered for `README.md`, `ROADMAP.md`, `DECISIONS.md`, `CHANGELOG.md`, or `docs/`. References among those files are documentation-to-documentation links rather than runtime dependencies.

`tests/` has a different role: `release/validate.sh` compiles the repository's test tree during source or release validation. This establishes a source/release-validation dependency but does not establish that `tests/` is required in the production runtime.

PI3-only recovery commit `5d0473dfd20efe7b07cf9167803d02aead10d61e` was reviewed against the authoritative `origin/main` history. Its `docs/RECOVERY_BASELINE.md` content is byte-for-byte identical to the authoritative version, and every substantive Master Plan addition is already present. The commit is therefore formally superseded and requires no merge or cherry-pick. It was temporarily preserved on the PI3 local branch `recovery/phase-7a8-documentation-pi3` until this supersession record was committed and pushed; that condition was satisfied, and branch removal was then separately validated.

The deployment exclusions were implemented in `release/upgrade.sh` and `pi4/install_pi4.sh`. Future production copies exclude the six approved source-only root paths without adding `--delete`; runtime-generated, persistent, and operational content remains preserved.

### Production Evidence Report

**Deployment result:** PI3 authoritative source was fast-forwarded to `9f0653075bbe67cc880904e6a4970dcab004d401`; source `main` matched `origin/main`, and the working tree was clean. Updated `release/upgrade.sh` and `pi4/install_pi4.sh` were copied into the production runtime, where their SHA-256 hashes exactly matched the authoritative source copies.

**Intended behavior:** Production deployments exclude the source-only root paths `README.md`, `ROADMAP.md`, `DECISIONS.md`, `CHANGELOG.md`, `docs/`, and `tests/`. Runtime deployment continues without `--delete`, preserving runtime-generated and operational directories.

**One-time cleanup:** The six approved source-only paths were removed from `/home/jazofv1/hioc`. Copies remain in authoritative source and in `/home/jazofv1/hioc/backups/release-upgrade-20260720-185835/current`.

**Invariant validation:** Runtime `config/`, `state/`, `history/`, `logs/`, `backups/`, and `pi4/bin/` remained present. An `rsync` dry run confirmed that the six excluded source-only paths would not be copied back. Final production hygiene validation result: **PASS**.

**Repository governance:** The temporary local PI3 branch `recovery/phase-7a8-documentation-pi3` was deleted only after its superseded commit was documented and preserved in authoritative history. The PI3 source repository remained on clean `main`, synchronized with `origin/main`.

### Unresolved Operational Issue

During `release/upgrade.sh`, `pi4/install_pi4.sh` reached its existing invocation of `hioc-incident-engine-v2.py`, which failed with `OSError: [Errno 7] Argument list too long: 'mosquitto_pub'`.

The incident-engine invocation was neither introduced nor changed by the Repository and Deployment Hygiene work; the only `pi4/install_pi4.sh` change in this checkpoint was the addition of the six `rsync` exclusions. The MQTT publishing failure is therefore not attributed to the hygiene implementation. At that closeout it remained unresolved and was assigned to a separate, scoped investigation; the hygiene checkpoint itself did not diagnose, redesign, or propose a correction for it.

### Incident History MQTT Transport Correction

Status: **COMPLETE**

The repository archaeology and architecture investigation are complete. Established production evidence shows that `state/incidents/history.json` was approximately 193,053 bytes with 24 records and that complete publication through one `mosquitto_pub -m` process argument reproduced `E2BIG`; the supported upgrade therefore returned failure. This immediate transport failure does not by itself decide whether transport, storage representation, retention, or the external payload contract should change.

The architecture is recorded as separate layers: authoritative local history is written before MQTT; completed records intentionally contain embedded operator-facing reviews; review data and review-derived summary fields are externally observable; established retained topics and incident fields are compatibility contracts; and the `mosquitto_pub -m` invocation is an internal legacy mechanism. Correlation Engine v2 partially adopted Core while retaining a publisher already identified by the archived architecture review as technical debt. No evidence shows that retaining that subprocess implementation was an affirmative decision.

The bounded evidence, confirmed invariants, unresolved decisions, and neutral candidate comparison remain in [Incident History Storage and MQTT Publication Architecture Decision Preparation](INCIDENT_HISTORY_MQTT_ARCHITECTURE_DECISION_PREPARATION.md). Accepted [ADR-0014](../DECISIONS.md#adr-0014-use-core-mqtt-for-incident-publication) selects Candidate C: preserve local history, embedded Incident Review, retained topics, and external payloads while replacing only the Incident Engine's local subprocess publisher with the existing Core MQTT client. This removes the payload from the failing process-argument boundary, aligns the engine with shared Core architecture, minimizes consumer and migration risk, and introduces no new protocol.

The binding [Incident History MQTT Transport Implementation Specification](INCIDENT_HISTORY_MQTT_TRANSPORT_IMPLEMENTATION_SPEC.md) defines the exact connection lifecycle, publication order, compatibility boundary, failure and exit-status behavior, tests, deployment validation, rollback, documentation plan, and deferred work. Candidate C is implemented in the repository: Incident Engine publication uses one Core MQTT connection per run, retains the existing ordered topics and payload strings, stops on the first required failure, reports partial progress, and returns nonzero without discarding local state. Focused and full repository validation passed, and the supported production deployment and runtime validation completed successfully.

This bounded MQTT checkpoint was related to Phase 7A only because it blocked
truthful supported deployment and reliable incident publication. It remains
separate from incident-history schema-validator hardening, stale-client retention
and archival, repository and deployment hygiene, new inventory enrichment,
unrelated dashboard redesign, and broader MQTT protocol redesign. The completed
correction and validation return work to the authoritative roadmap so
operator-facing and dashboard progress can resume.

#### MQTT Runtime Validation Checkpoint

Status: **COMPLETE**

The repository now owns a bounded, read-only post-install and post-upgrade
validator for the retained Incident Engine MQTT contract. The deployed command
loads the existing toolkit and HIOC configuration, respects the configured HIOC
base topic, reads all seven retained incident and status topics with predictable
timeouts, validates payload presence and JSON or scalar status semantics, and
reports concise PASS, FAIL, INCOMPLETE, warning, byte-size, record-count, and
embedded-review evidence without printing credentials or publishing test state.
Focused and full repository validation passed. Operator production execution and
the required Evidence Report also passed.

This checkpoint does not change ADR-0014 transport, MQTT topics, retained flags,
payload schemas, broker configuration, Incident Engine behavior, Home Assistant,
or dashboards. Work now returns to the next incomplete checkpoint already
defined by this Master Plan.

##### Production Evidence Report

**Deployment result:** Implementation commit
`2b0b2ab6b9007a5a61025c847ceabb5030d8638a` was deployed through the supported
release workflow. Release validation, release upgrade, the standalone MQTT
validator, and general Pi4 validation all returned PASS. The production Evidence
Report is
`/tmp/hioc-mqtt-runtime-validation-20260723T040611Z/MQTT_RUNTIME_VALIDATION_PRODUCTION_EVIDENCE_REPORT.md`
with SHA-256
`01a7cac95e426b348b97222cc7b1f6deeee1147fbd1ae011efd6acee73f627f4`.

**Intended behavior:** The deployed validator resolves the broker through the
supported configuration hierarchy, performs subscription-only reads of the
seven required retained topics, validates payload presence and structure, and
reports PASS, FAIL, or INCOMPLETE without publishing or mutating retained state.

**Invariant checks:** All 7 required topics passed. Incident history was exactly
230660 bytes with 27 records and embedded review data present. Retained and local
history byte size, record count, and embedded-review evidence matched. No
hardcoded localhost assumption, credential disclosure, public-topic change,
payload-schema change, Home Assistant change, or retained-state mutation was
observed. The deployed validator SHA-256 was
`d4be8debbd9c926fbc3526bd0ae7f5f3473c68ef9853d7f0d995762170b12d53`.
The release-upgrade backup is
`/home/jazofv1/hioc/backups/release-upgrade-20260722-220732`, and the installer
backup is `/home/jazofv1/hioc/backups/install-20260722-220732`.

**Warnings and deferred risks:** None were reported by this production
checkpoint. TLS, explicit MQTT byte-size policy, broader broker resilience,
other legacy publishers, retention policy, and future MQTT architecture remain
outside ADR-0014 and are not marked complete.

**Final result:** **PASS**

---

# Repository Rules

Every completed phase must:

- Compile successfully
- Pass unit tests
- Validate Home Assistant YAML
- Preserve backward compatibility unless explicitly approved

Every checkpoint Evidence Report must state:

- Deployment result.
- Intended behavior.
- Invariant checks.
- Warnings and deferred risks.
- Final PASS or FAIL.

Repository and deployment rules:

- Investigate documentation first: review this Master Plan, applicable ADRs, architecture and data-model documents, Git history, implementation, and existing validation evidence before proposing production experimentation. Use production investigation only for a specific evidence gap that repository evidence cannot answer.
- Record every material architecture or implementation decision, compatibility boundary, assumption, validation result, deviation, deferral, and unresolved question in the appropriate repository document; do not leave authoritative conclusions only in chat, commits, code, test output, production state, or human memory.
- Keep investigations bounded to questions that materially block the current decision. Record unrelated improvements for later and return to roadmap and operator-facing progress after each corrective checkpoint.
- Begin all deliberate source changes in an authorized development checkout.
- Keep documentation and code synchronized when behavior and operating procedures change together.
- Never copy generated runtime state back into source control.
- Do not allow the production runtime to become an alternate development branch.
- Investigate and classify unexplained source/runtime divergence before cleanup.
- Do not remove obsolete-looking files without evidence that they are unused.
- Ensure deployments are reproducible from the authoritative source checkout on the target host or a validated release package.
- Classify runtime and generated artifacts explicitly, then preserve or exclude them intentionally.
- Commit accepted recovery manifests and similar historical evidence documents to the authoritative repository history. Keep approved historical records immutable; new recovery work must create new evidence instead of modifying them or leaving them only in temporary branches or local repositories.

Unless specifically requested:

- Do not redesign unrelated code
- Do not rename MQTT topics
- Do not rename entities
- Do not introduce breaking changes

---

# Commit Rules

Every completed phase ends with:

1. Validate the intended behavior.
2. Validate applicable invariants and backward compatibility.
3. Update the Implementation Status and any relevant roadmap, governance, or decision sections in this document.
4. Commit code and documentation together when both changed.
5. Push to main.
6. Verify the development checkout has a clean working tree and the shared history contains the approved commit.
7. Record an Evidence Report containing the deployment result when applicable, intended behavior, invariant checks, warnings, and final PASS or FAIL.

`docs/HIOC_MASTER_PLAN.md` remains the authoritative project source of truth.

## Operations Acceptance Standard

A release or completed checkpoint is not operationally complete until committed repository documentation answers, without requiring SSH discovery:

- What exists?
- Why does it exist?
- How does it run?
- How is it validated?
- How is it recovered?

Each completion review must verify:

- All new runtime components and their purposes are listed.
- Execution mechanisms, schedules, triggers, and locks are documented.
- Outputs, logs, status artifacts, and freshness expectations are documented.
- Validation and safe recovery procedures are documented.
- Relevant network ports and dependencies are documented without unsupported guesses.
- Current-state documentation and cross-references are synchronized.
- No critical operational fact exists only in chat history or only on the production host.

If production verification is required, it must be captured in an Evidence Report and committed back to the repository. This standard adds to, and does not weaken, the permanent workflow to validate, update the Master Plan and affected documentation, commit code and documentation together, push `main`, and verify a clean synchronized working tree.

---

# Working Agreement

While implementing HIOC:

- Stay focused on the current phase.
- Avoid scope creep.
- Record future ideas instead of implementing them immediately.
- Return to this document whenever a phase is completed.
- Keep changes consistent with the project's architecture and philosophy.

---

# Implementation Status

This section reflects the current state of the project.

It should be updated whenever a development phase is completed.

The Phase 7A.8 Recovery Validation Chain, repository governance reconstruction, reconciliation of the historical recovery documentation, Release Boundary Hardening, Changelog Governance Reconciliation, Repository Governance Reconciliation, Runtime Git Metadata Retirement, and the overall Repository and Deployment Hygiene checkpoint are complete. PI3 production migration, validation, supported upgrade proof, supported rollback proof, and quarantine removal are complete. ADR-0013 is resolved, and `/home/jazofv1/hioc` is formally non-Git. The former `61/62 commits behind` runtime condition is permanently resolved because the runtime is no longer a Git checkout and Git history belongs to the authoritative repositories. The approved lifecycle candidate remains intentionally reachable through `validation/phase-7a8-lifecycle`; completed merged topic branches and the temporary Windows SSH artifact have been retired. GitHub history is authoritative. Development checkouts, the authoritative source checkout for PI3 release execution, and the deployed production runtime have formally documented roles. The ADR-0014 Core MQTT correction, production deployment, and MQTT production Evidence Report are complete. Pi-hole DHCP Lease Ingestion implementation and production validation are complete with a documented warning. Canonical Address Selection Hardening is production validated and complete. The network-probe checksum-governance and PI5 endpoint-migration correction is complete: repository correction, governed deployment, Phase A, Phase B incident recovery, and overall production validation passed at approved commit `e06539d9bece040d721b9912213559cc54f1610d`. The July 29 DHCP pool-exhaustion incident is resolved, HIOC deployment validation passed, and the documentation architecture now assigns current-state, runtime, network, deployment, incident, and recovery authority to focused documents. DHCP Service Health & Capacity Monitoring and `.152` DHCP residue cleanup remain separate future work. Phase 7A remains active and Active Discovery remains postponed.

## Current Branch

main

## Current Commit

Tracked by Git history. Do not update this document solely to record documentation-only commit hashes.

## Current Phase

Phase 7A - Passive Living Inventory

## Phase Progress

| Phase | Status |
|--------|--------|
| Platform Foundation | ✅ Complete |
| MQTT Publishing | ✅ Complete |
| Dashboard v2 | ✅ Complete |
| Incident Engine | ✅ Complete |
| Correlation Engine | ✅ Complete |
| History Engine | ✅ Complete |
| Incident Review | ✅ Complete |
| Dashboard Usability Improvements | ✅ Complete |
| Initial Living Inventory | ✅ Complete |
| Phase 7A - Passive Living Inventory | 🚧 In Progress |
| Phase 7B - Safe Active Discovery | ⏳ Planned |
| DHCP Service Health & Capacity Monitoring | ⏳ Planned |

## Current Objective

Maintain Phase 7A after completing and production-validating PE-1 and approving
the PE-2.0 Asset foundation design and repository-validating the PE-2.1
executable implementation. PE-2.1 production deployment and validation remain
pending.

## Next Planned Task

The next authoritative checkpoint requires separate authorization for PE-2.1
production deployment and validation. Do not mark Phase 7A complete.

Remaining Phase 7A corrective work and passive enrichment follow in the documented sequence.

Do not begin Active Discovery until Phase 7A has been completed.

---

# Decision Log

## 2026-07

Architectural decisions currently in effect:

- Dashboard v2 is the primary operator interface.
- Passive Living Inventory must be completed before Active Discovery.
- HIOC favors operator explanations over raw metrics.
- Historical incident review is a first-class feature.
- Incident testing will occur during real operational events rather than synthetic simulations.
- New features must not interrupt the current implementation phase.
- Scope changes require an intentional revision of this master plan.

---

# Maintaining This Document

This document should evolve deliberately.

Routine implementation work should update only:

- Current Phase
- Phase Progress
- Current Objective
- Next Planned Task

Changes to the project's philosophy, architecture, or roadmap should be made intentionally and reflected in the Decision Log.


## Phase 7A Network Probe Source Governance and MQTT Health Hardening

Status: **COMPLETE — REPOSITORY, DEPLOYMENT, AND PRODUCTION VALIDATION PASS**.

This bounded corrective checkpoint responds to the July 29, 2026 PI5 address change from `192.168.100.152` to `192.168.100.251`. The operator corrected `HOME_ASSISTANT_IP`, `MQTT_HOST`, and the webhook endpoint in PI3 `toolkit.conf`, and host and service-port checks passed. The network probe nevertheless retained two old executable literals, so MQTT publication and PI5 probing used competing endpoint sources.

The production probe was absent from every Git repository. The first implementation attempt stopped because rebuilding production behavior from fragments was unsafe. The operator captured the complete script and evidence. The intake archive SHA-256 `74e7e251bd0848a0b87d2f314fd2d0958bd5c9730a8b6ff37fff449c1052bf6d` and script SHA-256 `edf6ad456292a0fb9441f09e7eb59fa02831cee46aa7071dcaa7b8d3eadc39a1` were verified before import.

The authoritative source is now `pi4-tools/scripts/hioc-network-probe.sh`; the production path remains `/home/jazofv1/pi4-tools/scripts/hioc-network-probe.sh`. The probe derives PI5 reachability and inventory addressing only from required `HOME_ASSISTANT_IP`. `toolkit.conf` remains runtime configuration and is not committed. `pi4-tools/deploy-network-probe.sh` validates syntax, creates a timestamped backup, installs atomically with owner/group `jazofv1` and mode `0755`, and verifies source/deployed hashes without touching configuration, logs, state, or prior backups.

Dashboard V2 now separates MQTT Operational Health from MQTT Forecast Trend. Operational health uses the parseable last-success timestamp with a 12-minute freshness threshold and two-minute future-clock tolerance. Unavailable, unknown, empty, invalid, stale, or implausibly future data cannot be green. The cumulative failure counter remains historical evidence and is not reset or treated as permanent current degradation. Forecast rising is Watch; stable or falling is Favorable and cannot override operational health.

### Infrastructure-change governance

Any IP address, hostname, DNS name, broker, Home Assistant endpoint, webhook, service port, or comparable dependency change requires repository and production impact review. Review active configuration, executable scripts, cron/timers, systemd, publishers/subscribers, Home Assistant integrations, dashboards, inventory, incidents, health models, deployment, backup/restore, tests, runbooks, and evidence classification where applicable. Historical evidence is not rewritten. Current documentation reflects current infrastructure. Executable code uses an authoritative configuration value instead of duplicated literals whenever one exists.

Validation order is: configuration values; host reachability; service-port reachability; controlled publisher execution; subscriber receipt; last-success advancement; failure-counter behavior; freshness; dashboard operational health; forecast separation; inventory address; incident behavior; runtime checksum; repository cleanliness.

### Future complete pi4-tools source-governance checkpoint

Only `hioc-network-probe.sh` was captured. A future checkpoint must perform complete checksum-verified intake of all active scripts, secret-free configuration templates, cron ownership, state/log/generated/backup boundaries, deployment and restore procedures, tests, documentation, and production checksum validation. No uncaptured script is fabricated or claimed as governed here.

### Evidence Report

Repository evidence is recorded in [NETWORK_PROBE_GOVERNANCE_EVIDENCE.md](NETWORK_PROBE_GOVERNANCE_EVIDENCE.md). At that repository-only stage, implementation could pass independently while the overall checkpoint remained open until controlled deployment evidence was returned and documented.

Closure: operator evidence for approved commit
`e06539d9bece040d721b9912213559cc54f1610d` records matching Git blob,
worktree, and deployed checksums, successful PI5/MQTT/inventory validation, and
cleared false incident. The historical pending condition is satisfied.

## Phase 7A Corrective Checksum-Governance Checkpoint

Status: **COMPLETE — CORRECTION, PHASE A, PHASE B, AND PRODUCTION PASS**.

The first PI3 deployment attempt stopped safely before deployment because the
operator command contained an incorrect manually transcribed checksum. The
value is proven to be the SHA-256 of the CRLF Windows checkout, while the
approved commit stores an LF blob. This is a governance defect, not a PI3
synchronization, checkout, branch, or production-file failure.

The corrective checkpoint establishes raw Git objects at an exact approved
commit as the sole artifact-byte authority. It adds deterministic
commit/path/blob/SHA-256 reporting, prevents manually supplied hashes from
overriding Git identity, binds the network-probe deployment helper to a clean
exact commit, and proves blob/source/deployed byte identity in isolated tests.
The dynamic-manifest design avoids a tracked self-referential checksum.

All deployment evidence is regenerated only after the final corrective commit
is pushed and `HEAD` equals `origin/main`. No checksum calculated before that
point can enter operator instructions. Repository correction does not complete
the PI3 deployment; controlled PI5 connectivity, probe, MQTT, inventory, and
production artifact validation remain pending. Active Discovery and normal
roadmap work remain paused for this correction.

The final refinement separates deterministic governed deployment from
downstream incident recovery. Phase A failure remains fail-closed. Delayed or
inconclusive Phase B convergence produces **PARTIAL PASS**, exits successfully,
and requires separate follow-up without rollback based solely on observation.
Full **PASS** requires both domains; **FAIL** is reserved for deterministic
deployment failure. The checksum-origin and Endpoint Migration Audit findings
remain unchanged. Before operator execution, production stayed open pending
evidence review.

Closure evidence records Phase A **PASS**, Phase B **PASS**, and overall
production validation **PASS**. Seven reads succeeded with no failures or
malformed payloads, false PI5 evidence was absent, the backup was created, and
no rollback occurred or was required. This closes only this corrective
checkpoint. Phase 7A remains in progress; Canonical Address Selection
Hardening remains next.
