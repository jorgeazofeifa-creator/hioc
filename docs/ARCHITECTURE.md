# HIOC Architecture

HIOC is a self-hosted home infrastructure monitoring platform optimized for a Pi4 collector and Home Assistant operator console.

## Runtime Flow

```text
Pi4 toolkit telemetry
  -> HIOC incident engine and Correlation Engine v2
  -> incident JSON state
  -> retained MQTT
  -> Home Assistant incident entities

Pi4 local/network discovery
  -> HIOC inventory engine
  -> inventory JSON state
  -> retained MQTT
  -> Home Assistant inventory entities

Pi4 historical sampling
  -> HIOC history engine
  -> CSV history and forecast JSON
  -> retained MQTT
  -> Home Assistant predictive entities
```

## HIOC Core

HIOC Core provides shared runtime services for configuration, atomic JSON state, retained MQTT publishing, structured logging, schema validation, internal events, driver execution, and capability inference. New subsystems should use Core instead of creating local config, MQTT, state, or logging helpers.

## Correlation Engine v2

The incident engine delegates root-cause analysis to the shared Core correlation module. It consumes Pi4 telemetry, Living Inventory health, topology and dependency relationships, and contextual events from the internal event bus. Related failures are merged into a single stable incident key so repeated symptoms do not create duplicate incidents for the same root cause.

Correlation Engine v2 assigns each incident a lifecycle phase of `detected`, `confirmed`, `active`, `recovering`, or `resolved`, calculates a 0-100 confidence score, records affected systems and services, and writes incident history with start time, end time, duration, root cause, confidence, and impacted systems. Public MQTT topics and Home Assistant incident entities remain backward compatible; new fields are added inside the existing JSON payloads.

## Living Inventory

The inventory engine uses passive discovery by default and can optionally run active discovery when configured. Passive sources are:

- Pi4 host identity, interfaces, operating system, kernel, and package versions.
- Default route and gateway.
- Kernel neighbor table.
- Pi-hole/dnsmasq DHCP leases where present.
- Local systemd services and listening network sockets.
- Integration hint JSON from `state/inventory/integrations` or `HIOC_INVENTORY_INTEGRATION_DIR`.

Active discovery is disabled by default. When `HIOC_INVENTORY_ACTIVE_DISCOVERY=on`, HIOC may use reverse DNS, ping reachability checks, optional configured subnet scan using `nmap` when available, bounded ping sweep, and optional SNMP system description.

Topology generation uses the default gateway as root, supports integration-provided parent hints, and can place endpoint devices behind intermediate infrastructure such as Orbi satellites and switches when those devices are discovered.

Inventory state is stored in `state/inventory` and published under `home/infrastructure/hioc/inventory`.

Living Inventory emits internal events for device discovery, inventory changes, and topology changes. It also writes internal capabilities without changing the public MQTT inventory schema.

## Compatibility

HIOC keeps the existing Pi4 toolkit and legacy MQTT topics intact. New subsystems publish under the HIOC base topic and read existing telemetry through `HIOC_LEGACY_BASE_TOPIC`.
