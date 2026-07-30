# HIOC Incident Model

## Document Ownership

This document owns incident semantics and their relationship to operational evidence. It does not change the current JSON schema, topic contract, or lifecycle implementation. See [DATA_MODEL.md](DATA_MODEL.md) for fields and [MQTT.md](MQTT.md) for publication.

## Evidence Semantics

- **Observation:** usable evidence that an entity was seen. Observation does not by itself establish expected availability.
- **Staleness:** positive observation is older than its freshness policy. Staleness is not automatically degradation or offline state.
- **Degraded:** an availability-monitored system or service is functioning below its documented operational contract.
- **Offline:** authoritative evidence or policy establishes that an availability-monitored system is unavailable.
- **Incident:** a stable lifecycle record correlating operational signals, impact, root cause, confidence, and recovery.

DHCP assignment evidence does not create positive liveness, directly assert online or offline, or refresh `last_seen`. A daemon being active establishes process health only; service health also includes successful delivery, dependencies, and capacity. The July 29 DHCP incident demonstrates that a running DHCP daemon can coexist with selective address-allocation failure caused by pool exhaustion.

## Lifecycle

Incident Engine v2 uses `detected`, `confirmed`, `active`, `recovering`, and `resolved` phases. Stable incident identity prevents repeated symptoms from creating unrelated incidents for the same root cause. Recovery confirmation precedes resolution. Historical records and reviews remain evidence after resolution.

## Severity and Operational Truth

Severity communicates impact and urgency using existing project conventions. Source authority, freshness, expected availability, and affected dependencies determine which conclusions are safe. Historical log errors are not current failures when later successful runs and fresh state establish recovery, but the old entries must remain available for audit.

## Capacity and Service Health

Capacity is part of service health. Current HIOC does not yet implement DHCP capacity incidents. The future DHCP Service Health & Capacity Monitoring phase will plan healthy, warning, degraded, critical, and unavailable interpretations without redesigning the global incident schema in advance.

## Validation

Incident validation combines fresh status, current state, lifecycle consistency, retained publication where applicable, logs, and resolution behavior. Persistent process presence is not an appropriate primary check for cron-driven HIOC engines. See [OPERATIONS.md](OPERATIONS.md).
