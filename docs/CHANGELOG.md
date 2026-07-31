# HIOC Changelog

## Document Ownership

This document owns released and delivered work.

This is the repository's single authoritative changelog. The root [CHANGELOG.md](../CHANGELOG.md) is a discoverability pointer only. All future release and completed-checkpoint entries must be written here. Maintaining a second overlapping full changelog is prohibited unless a separately approved governance decision establishes a distinct, non-overlapping purpose.

Use these categories when applicable:

- Added
- Changed
- Removed
- Fixed
- Deprecated
- Security

Do not place roadmap items here. Future work belongs in [../ROADMAP.md](../ROADMAP.md) and detailed implementation direction belongs in [HIOC_MASTER_PLAN.md](HIOC_MASTER_PLAN.md).

## Unreleased

### Added

- Added a deployed, read-only MQTT runtime validator that uses existing HIOC
  configuration to perform bounded retained-topic checks and emit concise
  post-install or post-upgrade Evidence Report output without publishing state
  or exposing credentials.

### Documentation

- Established the focused documentation architecture: the Master Plan remains the authoritative roadmap; the new System Reference Manual owns current state; Operations owns the cron-driven runtime and freshness-based health model; Network Foundation owns critical addresses and dependencies; Deployment owns source-to-runtime boundaries; and Incident Model owns operational incident semantics. Added the permanent July 29 DHCP pool-exhaustion incident report, recorded HIOC deployment validation as PASS, added the Operations Acceptance Standard, and planned a future DHCP Service Health & Capacity Monitoring phase without implementing it.
- Closed Pi-hole DHCP Lease Ingestion as **PASS WITH DOCUMENTED WARNING** after supported production upgrade, PI3 validation, and successful inventory generation. All 140 active lease MAC identities were represented with DHCP provenance and expiry metadata; seven additional DHCP-backed identities were confirmed as retained expired historical records rather than duplicate active leases. One active lease MAC/IP pair differed from the selected canonical IP because the same MAC owned two simultaneous `STALE` neighbor addresses. DHCP ingestion remains passed; deterministic canonical-address precedence is deferred to a separate Phase 7A hardening checkpoint that must preserve MAC-backed identity and must not treat DHCP assignment as liveness.
- Accepted ADR-0015 for the active Pi-hole DHCP Lease Ingestion checkpoint. Pi-hole DHCP remains a source-specific adapter within the existing passive-driver and source-tagged device-record convention; central reconciliation continues owning canonical identity, authority, and observation semantics. The decision rejects a new `IdentitySource` or plugin framework, defines DHCP field ownership and deterministic conflict rules, and bounds the later implementation without marking DHCP ingestion complete.
- Completed Repository and Deployment Hygiene. Historical runtime provenance proved that HEAD `94e1997f0d9df9e43209e44f7eb62a8d808714cc` was preserved in authoritative history and that no runtime-only commits, branches, tags, or stashes existed. The approximately 2.6 MB `.git` directory was quarantined and validated, the non-Git runtime passed production validation, a supported upgrade did not recreate `.git`, rollback did not restore it, post-rollback SHA-256 comparisons matched the authoritative release source for the checked deployment artifacts, and persistent runtime data remained intact. The approved quarantine path was removed successfully, the runtime remains formally non-Git, and all checkpoint closure criteria are satisfied.
- Completed Repository Governance Reconciliation on 2026-07-28: retained `validation/phase-7a8-lifecycle` locally and remotely as the intentional reachability reference for approved recovery candidate `be7b69d`; retired three fully merged local branches and the two corresponding remote branches that still existed; and removed the untracked `hioc_known_hosts.tmp` workspace artifact after confirming that no operational tooling consumed it. At that stage the overall Repository and Deployment Hygiene checkpoint remained open for the two manual PI3 audits and final closeout; the audits and production engineering validation are recorded as complete in the later entry above.
- Reconciled changelog governance by restoring the root `CHANGELOG.md` as a pointer to this authoritative record. Repository history confirms that the documentation-governance migration established this single-authority model; a later bounded implementation entry accidentally replaced the pointer and became stale after Collector Canonical Ownership regression, production, and documentation validation completed. No historical evidence was removed from Git history.
- Closed the Phase 7A Collector Canonical Ownership checkpoint after implementation commit `054fb55a2e70901f3230145b76983c31d2b5ce61` passed release validation, supported production upgrade, Pi4 validation, and production evidence review. The canonical collector remained MAC-backed at `192.168.100.252`, all eight services were owned by `Pi3 - NUT and Pi-hole`, and the historical `.105` ownership defect was not observed; this documentation-only closeout does not change runtime or public contracts.
- Recorded successful production deployment and validation of the single-snapshot ARP semantics correction: normal discovery reported `arp_table`, discovery remained unlimited, and the checkpoint closed after PASS evidence.
- Recorded successful ADR-0014 production validation and made the repository the
  authoritative operational reference for configured, read-only MQTT runtime
  validation after installation or upgrade.
- Documented the planned asset-centric Living Inventory vision, including evidence authority, observation versus availability, operator-managed asset knowledge, lifecycle-safe retention principles, and roadmap dependencies; no runtime behavior changed.

### Fixed

- Implemented the repository correction for deterministic canonical IPv4
  selection. Neighbor state now participates as private reconciliation
  evidence; an active DHCP assignment for a MAC cannot lose merely to a stale
  neighbor address, while stronger current/configured evidence and legitimate
  static devices remain supported. Stable MAC identity, aggregate provenance,
  liveness, health, schemas, dashboards, incidents, and retention are
  unchanged. Production validation remains pending, so the Phase 7A checkpoint
  is still open.

- Closed the network-probe checksum-governance and PI5 endpoint-migration
  correction after governed PI3 deployment at
  `e06539d9bece040d721b9912213559cc54f1610d`. Blob, worktree, and deployed
  checksums matched; Phase A and Phase B passed; retained PI5 state and
  inventory were correct; the false incident cleared; and no rollback or
  warning was required. Phase 7A remains active.

- Separated deterministic network-probe deployment validation from bounded
  downstream incident-recovery observation. Delayed or inconclusive recovery
  now produces PARTIAL PASS and follow-up without rollback. Added safe read
  accounting, malformed-payload handling, backup validation, and a tracked
  operator procedure.

- Corrected the Phase 7A network-probe checksum-governance defect. The
  previously reported `27e4dec6...` checksum remains only as incident evidence:
  it is proven to be the CRLF Windows checkout hash, not the approved Git blob
  hash. Added deterministic Git-object identity, commit-bound deployment with
  blob/source/target byte comparisons, and stale-checksum regression tests.
  PI3 deployment was pending at that implementation stage and is closed by the
  later production-validation entry above.

- Implemented bounded Pi-hole DHCP lease ingestion semantics. Inventory cycles use one fixed collection epoch; only active finite or infinite IPv4 Pi-hole/dnsmasq leases contribute assignment evidence; expired, IPv6, ISC-format, malformed, and unusable rows contribute no identity evidence. Explicit blank configuration disables acquisition, the default is limited to `/etc/pihole/dhcp.leases`, source aggregation preserves complete and incomplete states, and unavailable configured DHCP evidence reports truthful discovery limitation without weakening MAC-backed identity or observation authority. Automated regression validation passed, and the later production Evidence Report closes the checkpoint with a documented canonical-address warning.
- Implemented the repository side of runtime Git metadata retirement. Upgrade backups now exclude `.git`, rollback restoration excludes `.git` even from historical backups, and tests preserve legitimate hidden files and persistent-state protections. README and operator documentation now use the release-source installation model, ADR-0013 formally defines `/home/jazofv1/hioc` as a non-Git runtime, and runtime version identity remains owned by `VERSION.yaml`. Manual PI3 provenance capture, quarantine, upgrade, rollback, and production validation were pending at that stage and are recorded as complete in the later production Evidence Report entry, including approved quarantine removal.
- Hardened release construction so `release/build.sh` obtains its complete source set from Git-tracked files instead of traversing the workspace. Ignored, untracked, cache, and temporary artifacts—including `hioc_known_hosts.tmp`—cannot enter a release merely by existing beside the source. The generated manifest now records the source commit without checkout-path or wall-clock fields, while deployment and runtime behavior remain unchanged.
- Deployed the bounded Pi-hole DHCP Single Snapshot Acquisition correction: inventory captures lease files once into a cycle-local immutable snapshot and reuses it throughout discovery status, passive observations, and reconciliation, removing duplicate acquisition without intentionally changing functional behavior. Automated regression tests prove the single-acquisition invariant; successful production deployment confirmed `dhcp_leases_found`, 145 DHCP-backed devices, preserved `/etc/pihole/dhcp.leases` metadata, and no observable inventory regression. The broader DHCP checkpoint remains open.
- Completed the Dashboard Severity Mapping checkpoint at implementation commit `1e2dcf973d02514561b7bb8a4f5c6f495350ab09`: Living Inventory aggregate Watch wording now covers observation or availability review without incorrectly describing every Watch condition as stale, Dashboard v2 gives unavailable inventory status precedence over retained device counts when styling Inventory Summary, and production deployment and validation passed. Health, schemas, MQTT, entities, incidents, layout, and the existing blue Watch palette remain unchanged; the Watch color UX/design decision remains deferred.
- ARP discovery-source status and passive device evidence now share one authoritative neighbor-table acquisition per inventory cycle, and total primary-plus-fallback command failure is reported as unavailable rather than successful empty evidence. Unresolved-neighbor filtering, identity, retention, health, monitoring, and accepted NUD-state behavior remain unchanged.
- Incident Engine retained publication now uses one shared Core MQTT connection per run instead of placing complete payload documents in `mosquitto_pub -m` process arguments, preserving local history, embedded reviews, topics, retained semantics, and payload schemas while returning a truthful nonzero status for required publication failures.
- Living Inventory now includes a dedicated Watch Devices presentation, ordered by oldest known observation first and showing authoritative identity, observation, provenance, and health-reason details without changing inventory semantics.
- Pi-hole DHCP lease ingestion now distinguishes missing, unreadable, malformed, I/O-error, empty, partial, and usable sources; validates lease fields; preserves assignment metadata without treating a lease as liveness; and prevents DHCP data from overriding stronger current identity evidence.
- Local services now retain ownership by the canonical pre-enrichment collector identity; known-infrastructure classification can no longer erase local-host ownership, and a missing collector no longer falls back to an arbitrary inventory device. Canonical-address selection is unchanged and remains a separate future hardening checkpoint.
- Inventory Summary now renders the dedicated recommendation entity so watch-only passive clients do not imply operator attention; degraded and offline guidance is unchanged.
- Home Assistant operational presentation now preserves the operator-supplied Dashboard v2 layout, treats missing incident/inventory/forecast/platform payload values as unknown instead of all-clear or zero, and protects the reconciled layout and dynamic-truth policy with focused regression tests.

### Added

- Dashboard architecture guidance defining operational-truth ownership, unknown-state handling, operator-layout protection, and the current storage-managed deployment boundary.
- Living Inventory engine with local/network discovery, inventory database, topology, service dependency graph, firmware fields, MAC/IP tracking, health scoring, and last-seen timestamps.
- Retained MQTT inventory topics under `home/infrastructure/hioc/inventory`.
- Home Assistant Living Inventory package and dashboard.
- Pi4 installer, uninstaller, and validation integration for inventory.
- Unit tests for inventory identity, health scoring, topology, and dependencies.
- Architecture, project, MQTT, Home Assistant, data model, roadmap, and decision documentation.
- Passive-by-default inventory discovery with active discovery disabled unless explicitly configured.
- Persistent MQTT client abstraction for Living Inventory publications.
- 30-minute default inventory refresh interval.
- Topology inference for intermediate infrastructure devices and integration-provided parent hints.
- HIOC Core v1.0 shared runtime with StateStore, schema validation, event bus, driver registry, capability registry, configuration service, and structured logging.
- Living Inventory internal events and capability state without changing public MQTT or Home Assistant entities.
- Dashboard v2 with Executive, Operations, Diagnostics, Inventory, Network, and Servers views built from real HIOC-owned entities.
- Release System v1.0 with version manifest, build/package/validate/install/upgrade/rollback scripts, platform status publisher, MQTT platform topics, and Home Assistant platform entities.
- Correlation Engine v2 with Core event context, topology-aware root-cause analysis, confidence scoring, lifecycle phases, duplicate suppression, and backward-compatible incident MQTT/Home Assistant output.
- HIOC Master Plan as the authoritative project charter.
- Passive known infrastructure definitions from `/home/jazofv1/hioc/config/inventory/known_infrastructure.json` to enrich Living Inventory without active discovery.

### Fixed

- Passive ARP/DHCP-only clients now retain stale observation state without generating availability incidents, while a centralized Core policy keeps infrastructure and authoritative sources operationally monitored.
- Dashboard v2 now presents active incidents using their actual Warning, Major, or Critical severity, with an Unknown fallback for unavailable severity or status.
- Release upgrades now invoke the Pi4 installer through Bash so clean source-controlled copies do not require the executable bit before installation.
- Platform-status logging now uses standard logging arguments so successful installation and upgrade runs can complete.
- Inventory now reconciles unique current or retained IP-only identities with unique current or retained MAC-backed identities without merging conflicting MACs.
- Inventory now excludes unresolved or MAC-less neighbor-cache entries from durable devices and removes legacy MAC-less records supported only by ARP provenance.

## v1.0.0-core

Initial real HIOC core foundation.

### Added

- Pi4 installer and uninstaller.
- Incident engine that reads existing Pi4 probe state and publishes structured MQTT JSON.
- Persistent active incident, incident history, summary, and timeline JSON files.
- Duplicate suppression through stable incident keys.
- Recovery detection and duration calculation.
- Home Assistant MQTT sensors for active incident, severity, status, system, summary, history count, and latest timeline event.
- Home Assistant notification automation driven from structured incidents.
- Documentation for architecture, incident model, MQTT topics, and installation.

### Notes

- This release is intentionally compatible with the existing `~/pi4-tools` installation.
- It does not replace the existing `hioc-network-probe.sh`.

- Phase 7A repository governance now owns the checksum-verified HIOC network probe source, derives PI5 probing and inventory addressing from `HOME_ASSISTANT_IP`, provides guarded deterministic deployment, and separates Dashboard V2 MQTT operational freshness from forecast trend. This entry records the earlier pending state; the Unreleased production-validation entry closes it.
