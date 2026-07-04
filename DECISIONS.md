# HIOC Architecture Decisions

## ADR-0001: Keep Pi4 Toolkit Compatibility

Decision: HIOC reads existing Pi4 telemetry and does not replace the Pi4 toolkit.

Rationale: Existing installations remain stable while HIOC adds higher-level incident, forecast, and inventory behavior.

## ADR-0002: Use Retained MQTT as the Home Assistant Contract

Decision: HIOC publishes retained JSON payloads under `home/infrastructure/hioc`.

Rationale: Home Assistant restarts should recover the latest operational state without waiting for a fresh scan.

## ADR-0003: Store Local JSON Before MQTT Publication

Decision: Engines persist state under `state/` before publishing MQTT.

Rationale: Local files preserve diagnosis data when MQTT or Home Assistant is degraded.

## ADR-0004: Living Inventory Uses Real Discovery Sources

Decision: Inventory discovery uses local host facts, routes, neighbor tables, DHCP leases, optional subnet scan, systemd, sockets, and optional SNMP.

Rationale: Production inventory must reflect observed infrastructure rather than static demo data.

## ADR-0005: Modular Python Runtime for New Subsystems

Decision: New Python subsystem code lives in reusable modules under `pi4/lib/hioc`.

Rationale: Configuration, logging, JSON state, MQTT, and data modeling should be shared as HIOC grows.

## ADR-0006: Keep JSON And Cron While Adding Core Contracts

Decision: HIOC Core v1.0 keeps JSON state files and cron scheduling, but centralizes state writes, config loading, logging, schemas, events, drivers, and capabilities.

Rationale: Current deployment scale does not require a database or scheduler replacement. Shared contracts provide most of the maintainability gain without adding premature operational complexity.

## ADR-0007: Internal Events Are Local State

Decision: Internal semantic events are written to local JSON state and do not replace public MQTT topics.

Rationale: MQTT remains the Home Assistant and external integration contract. Local events reduce internal coupling while preserving compatibility.

## ADR-0008: HIOC Dashboards Are Operations Surfaces

Decision: HIOC dashboard v2 will use a defined design system and operations hierarchy rather than continuing to add ad hoc Lovelace cards.

Rationale: Commercial operations consoles need prioritization, consistent terminology, and repeatable card patterns. Executive, Operations, Diagnostics, Inventory, Network, and Servers each answer different operator questions.

## ADR-0009: Releases Use Versioned Packages

Decision: HIOC has a formal release process with a version manifest, build/package scripts, install/upgrade/rollback wrappers, and runtime version reporting.

Rationale: HIOC should behave like installable software rather than a collection of copied files. Versioned artifacts and rollback metadata improve operator confidence and support long-term maintenance.
