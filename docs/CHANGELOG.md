# HIOC Changelog

## Document Ownership

This document owns released and delivered work.

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

- Recorded successful ADR-0014 production validation and made the repository the
  authoritative operational reference for configured, read-only MQTT runtime
  validation after installation or upgrade.
- Documented the planned asset-centric Living Inventory vision, including evidence authority, observation versus availability, operator-managed asset knowledge, lifecycle-safe retention principles, and roadmap dependencies; no runtime behavior changed.

### Fixed

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
