# HIOC Core v1.0

HIOC Core is the shared runtime layer used by engines and future subsystems.

## Document Ownership

This document owns the Core runtime: execution model, engine lifecycle, scheduling assumptions, shared services, subsystem initialization, internal events, drivers, and capabilities.

It should not duplicate architecture diagrams or project roadmap content. For system architecture, see [ARCHITECTURE.md](ARCHITECTURE.md). For project direction and phases, see [HIOC_MASTER_PLAN.md](HIOC_MASTER_PLAN.md).

## Core Services

- `ConfigService`: loads defaults, Pi4 toolkit config, HIOC config, and environment overrides.
- `StateStore`: reads and writes JSON state with atomic temp-file replacement.
- `MqttClient`: publishes retained MQTT payloads over a persistent MQTT connection.
- `EngineLogger`: writes structured engine log lines.
- `Schema`: validates required payload fields and basic field types.
- `EventBus`: records internal semantic events in local JSON.
- `DriverRegistry`: runs discovery/service drivers and isolates driver failures.
- `CapabilityRegistry`: derives infrastructure capabilities from devices and services.

## Internal Events

Events are stored under:

```text
state/events/events.json
state/events/latest_event.json
```

Current Living Inventory events:

- `DeviceDiscovered`
- `InventoryChanged`
- `TopologyChanged`

Events are internal contracts. They do not replace retained MQTT topics, which remain the Home Assistant integration contract.

## Drivers

Living Inventory now uses concrete drivers:

- `PassiveNetworkDriver`: neighbor table, DHCP leases, and integration hint files.
- `ActiveNetworkDriver`: existing extension point for active discovery; current approved inventory operation remains passive until Phase 7B safe active discovery is approved.
- `LocalServiceDriver`: systemd and listening socket service discovery.

Drivers return normalized devices and services. Future gateway, camera, MQTT broker, UPS, Home Assistant, SNMP, mDNS, and vendor-specific drivers should use the same `DriverResult` contract.

## Capabilities

Capabilities are stored under:

```text
state/inventory/capabilities.json
```

Capabilities are inferred from device roles, firmware, and detected services. They are currently internal state so existing MQTT topics and Home Assistant entities remain stable.
