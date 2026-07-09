# HIOC Roadmap

## Milestone 2: HIOC Core v1.0

Status: implemented in workspace.

- Shared runtime package.
- Configuration service.
- Atomic JSON StateStore.
- Persistent MQTT client abstraction.
- Schema validation.
- Structured engine logging.
- Internal event bus.
- Driver registry.
- Capability registry.
- Living Inventory integration with Core while preserving public MQTT and Home Assistant contracts.

## Milestone 3: Dashboard v2 Design System

Status: implemented in workspace.

- Define HIOC visual language.
- Add Operations wallboard page.
- Reduce Executive to seven command elements.
- Turn Diagnostics into Mission Control.
- Standardize card archetypes, terminology, colors, icons, and density rules.
- Rebuild dashboards from information architecture rather than adding more cards.

## Milestone 4: Release System v1.0

Status: implemented in workspace.

- Version manifest.
- Release build/package/validate/install/upgrade/rollback scripts.
- Runtime platform version/status JSON.
- Retained MQTT platform version/status topics.
- Home Assistant platform version entities.
- Dashboard v2 platform metadata display.

## Milestone 5: Correlation Engine v2

Status: implemented in workspace.

- Core correlation module fed by telemetry, Living Inventory, topology, dependencies, and internal events.
- Root-cause confidence scoring and incident lifecycle phases.
- Duplicate suppression by stable root-cause key.
- Incident history records start time, end time, duration, root cause, confidence, and impacted systems.
- Existing MQTT incident API and Home Assistant incident entities preserved.

## Milestone 1: Living Inventory

Status: implemented in workspace.

- Automatic infrastructure discovery.
- Device inventory database.
- Parent/child topology relationships.
- Service dependency graph.
- Firmware tracking.
- MAC and IP address tracking.
- Device health scoring.
- Last-seen timestamps.
- MQTT publication.
- Home Assistant entities.
- Inventory dashboard.
- Installer and validation integration.
- Unit tests.
- Documentation updates.

## Milestone 2: Configurable Notifications

- Replace hardcoded notification target with configurable Home Assistant helpers.
- Preserve current notification behavior for existing installs.

## Milestone 3: Broker and Service Telemetry

- Add MQTT broker statistics.
- Add connected client counts and message rates.
- Correlate broker degradation with incident evidence.

## Milestone 4: Inventory-Driven Incidents

- Feed inventory health and dependency graph into incident root-cause correlation.
- Identify affected services from topology and dependencies.
