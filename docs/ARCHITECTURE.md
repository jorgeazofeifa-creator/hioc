# HIOC Architecture

HIOC is a self-hosted home infrastructure monitoring platform optimized for a Pi4 collector and Home Assistant operator console.

## Document Ownership

This document owns system architecture: component interactions, subsystem boundaries, and major runtime flow.

It is not the roadmap and should not track current phase, implementation status, release history, or future task sequencing. For those, see [HIOC_MASTER_PLAN.md](HIOC_MASTER_PLAN.md) and [../ROADMAP.md](../ROADMAP.md).

Related technical documents:

- Core runtime: [CORE.md](CORE.md)
- Data model: [DATA_MODEL.md](DATA_MODEL.md)
- MQTT contract: [MQTT.md](MQTT.md)
- Home Assistant integration: [HOME_ASSISTANT.md](HOME_ASSISTANT.md)
- Asset model and operator concepts: [ASSET_MODEL.md](ASSET_MODEL.md)

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

Correlation Engine v2 assigns each incident a lifecycle phase of `detected`, `confirmed`, `active`, `recovering`, or `resolved`, calculates a 0-100 confidence score, records affected systems and services, and writes incident history with start time, end time, duration, root cause, confidence, and impacted systems. The Incident Engine publishes its existing retained payloads through one shared Core MQTT connection per run; local incident state remains authoritative and is written before publication. Public MQTT topics, payload structures, and Home Assistant incident entities remain backward compatible.

## Living Inventory

The inventory engine prioritizes passive discovery. Passive sources are:

- Pi4 host identity, interfaces, operating system, kernel, and package versions.
- Default route and gateway.
- Kernel neighbor table.
- Pi-hole/dnsmasq DHCP leases where present.
- Local systemd services and listening network sockets.
- Integration hint JSON from `state/inventory/integrations` or `HIOC_INVENTORY_INTEGRATION_DIR`.

Active-discovery configuration and code hooks may exist in the repository, but the currently approved operating mode is passive discovery. Broader Safe Active Discovery behavior belongs to the planned Phase 7B work described in [HIOC_MASTER_PLAN.md](HIOC_MASTER_PLAN.md). It must remain safe, explicit, and non-disruptive before operational use is approved.

Topology generation uses the default gateway as root, supports integration-provided parent hints, and can place endpoint devices behind intermediate infrastructure such as Orbi satellites and switches when those devices are discovered.

Inventory state is stored in `state/inventory` and published under `home/infrastructure/hioc/inventory`.

Living Inventory emits internal events for device discovery, inventory changes, and topology changes. It also writes internal capabilities without changing the public MQTT inventory schema.

Passive observation freshness and operational monitoring are separate concerns. HIOC Core owns one `is_operationally_monitored()` policy boundary used by both inventory health and incident correlation. Ordinary ARP/DHCP-only clients remain visible as stale or unknown when positive evidence ages, while infrastructure, known infrastructure, local/gateway records, authoritative integrations, explicitly monitored assets, and future unclassified sources remain availability-monitored. New discovery sources, including future Active Discovery sources, must make an intentional policy decision at this boundary rather than adding scattered correlation exceptions.

This policy does not define passive-client archival or permanent retention. Configurable archival and expiration remain a separate future checkpoint.

## Observation Is Not Availability

Observation answers whether HIOC has usable positive evidence that a device was seen. Availability asks whether an asset that is expected to operate is actually available. These are deliberately separate architectural concerns.

Evidence authority determines what conclusions are safe. ARP can provide recent network association; DHCP provides identity and address assignment but not liveness; known infrastructure provides operator knowledge but not current reachability; the local collector has authority over its own identity and services; integrations have authority only within their documented scope; and future active probes can show a point-in-time response without establishing purpose or expected availability.

A weaker source must not overwrite stronger identity or observation evidence. Likewise, stale or expired evidence cannot by itself prove that a mobile or transient device failed. Future incident interpretation can consider asset expectations only after those expectations are explicitly modeled.

## Future Asset-Centric Flow

The planned architectural direction is:

```text
Discovery evidence
  -> stable device identity
  -> operator asset enrichment
  -> expected-availability policy
  -> health and incident interpretation
  -> dependency and failure analysis
  -> historical and predictive intelligence
```

Stable discovery identity is the anchor: operator knowledge must survive address changes and rediscovery. Asset enrichment remains separable from discovered truth, and expected availability must precede any policy that interprets disappearance as failure. This flow is planned evolution rather than current completed behavior.

## Compatibility

HIOC keeps the existing Pi4 toolkit and legacy MQTT topics intact. New subsystems publish under the HIOC base topic and read existing telemetry through `HIOC_LEGACY_BASE_TOPIC`.
