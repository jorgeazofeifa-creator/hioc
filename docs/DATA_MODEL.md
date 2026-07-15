# HIOC Data Model

## Document Ownership

This document owns entities, relationships, JSON structures, MQTT payload shapes, and internal objects such as inventory, incidents, history, forecasts, capabilities, and platform status.

It should not contain roadmap or implementation-phase information. For roadmap and current phase, see [HIOC_MASTER_PLAN.md](HIOC_MASTER_PLAN.md). For topic names and publishing strategy, see [MQTT.md](MQTT.md).

## Living Inventory

Inventory root object:

```json
{
  "schema_version": "1.0",
  "updated": "ISO-8601 timestamp",
  "devices": [],
  "services": [],
  "topology": {},
  "dependencies": {},
  "summary": {}
}
```

Device object:

- `id`: stable ID generated from MAC, then IP, then hostname.
- `display_name`: operator name, hostname, IP, or ID.
- `type`: local host, network device, collector, gateway, or endpoint.
- `roles`: inferred operational roles.
- `ip`
- `mac`
- `hostname`
- `interfaces`
- `firmware`
- `reachable`
- `first_seen`
- `last_seen`
- `last_seen_epoch`
- `observation_status`: `recent`, `stale`, `expired`, `unobserved`, or `unknown`.
- `observation_age_seconds`: age of the last positive observation, or `null` when no timestamp exists.
- `operationally_monitored`: derived monitoring-policy decision used by health and incident correlation.
- `health_score`
- `health_status`
- `health_reasons`
- `parent_id`
- optional integration hints such as `parent_mac`, `parent_ip`, `uplink_mac`, `uplink_ip`, or `parent_device_id`

### Discovered Device and Operator-Managed Asset Metadata

A discovered device record is technical evidence: stable identity, addresses, hostname, interfaces, discovery sources, services, observations, and derived current health. Its provenance must remain visible so consumers can understand what each fact proves.

Operator-managed asset metadata is the human meaning linked to that identity: what the equipment is called, where it is, what it does, who is responsible for it, how important it is, and when it is expected to be available. Some current known-infrastructure fields already provide limited operator enrichment, but HIOC does not yet implement the complete asset model described in [ASSET_MODEL.md](ASSET_MODEL.md).

Technical identity and operator knowledge should remain separable. Rediscovery, DHCP reassignment, or an IP change must not erase confirmed asset knowledge, and operator metadata must not fabricate a technical observation.

### Current Observation Semantics

`first_seen` records the earliest retained discovery time. `last_seen` and `last_seen_epoch` record the last usable positive observation. `observation_age_seconds` is derived from that timestamp and is `null` when no usable timestamp exists.

Current `observation_status` meanings are:

- `recent`: positive evidence is inside the freshness window.
- `stale`: positive evidence is older than the stale threshold; failure is not automatically proven.
- `expired`: positive evidence is older than the offline threshold; failure is not automatically proven.
- `unobserved`: a configured record has not received positive discovery evidence.
- `unknown`: usable positive-observation history is unavailable.

DHCP assignment is identity/address evidence, not liveness, and does not update the positive-observation fields. `operationally_monitored`, health, and incident interpretation are separate policy and derived-state concerns.

### Planned Asset Metadata

The following names illustrate possible future information. They are planning concepts, not a current runtime schema or finalized field contract:

- an `asset_id` or other stable linkage to the discovered device identity;
- `friendly_name`;
- physical `location`;
- `purpose`;
- `owner` or responsible person;
- asset `category`;
- operational `criticality`;
- `expected_availability`;
- an explicit `monitoring_policy` or monitoring expectation;
- `lifecycle_state`, such as active, retired, or archived;
- `notes` and an optional photo reference;
- purchase or installation date;
- maintenance expectations and maintenance history.

Future schema work must preserve operator asset knowledge across IP changes and rediscovery while keeping discovered truth authoritative for observations. Asset classification and expected availability must be designed before they influence archival or incident decisions.

Known infrastructure definitions are optional operator-supplied passive inventory input. The default file is:

```text
/home/jazofv1/hioc/config/inventory/known_infrastructure.json
```

Schema:

```json
{
  "devices": [
    {
      "id": "operator-stable-alias",
      "name": "Office Switch",
      "hostname": "office-switch",
      "ip": "192.168.1.10",
      "mac": "aa:bb:cc:dd:ee:ff",
      "role": "Network Equipment",
      "type": "network_device",
      "vendor": "Netgear",
      "model": "GS108",
      "location": "Network closet",
      "area": "Infrastructure",
      "parent_id": "gateway",
      "parent_device_id": "gateway",
      "parent_mac": "11:22:33:44:55:66",
      "parent_ip": "192.168.1.1",
      "uplink_mac": "11:22:33:44:55:66",
      "uplink_ip": "192.168.1.1",
      "notes": "Operator-owned metadata",
      "enabled": true
    }
  ]
}
```

Supported roles are `Core Infrastructure`, `Network Equipment`, `Server`, `IoT`, `Media`, `Workstation`, `Mobile`, and `Unknown`.

Known definitions enrich observed passive inventory by normalized MAC first, then exact IP or normalized hostname when stronger identifiers do not conflict. Configured metadata can provide operator names, roles, model/vendor details, location, notes, and topology hints. Runtime fields such as observed status, health, last-seen timestamps, and service observations remain owned by passive discovery. A configured device that has never been observed is represented as offline and does not receive a fabricated `last_seen`.

When exactly one MAC-less identity and exactly one MAC-backed identity share an IP, inventory reconciles the weak identity into the canonical MAC-derived device. This applies when either identity is current or retained, including a current IP-only observation matched to one retained MAC-backed identity. The earliest valid `first_seen` and combined discovery provenance are preserved, while current observation timestamps remain current and non-empty stable metadata remains authoritative from the MAC-backed identity. Conflicting or ambiguous MAC identities are never reconciled.

Positive evidence creates or refreshes durable inventory. Unresolved neighbor-cache evidence such as `FAILED`, `INCOMPLETE`, `NONE`, or a MAC-less entry is diagnostic-only: it does not create an identity or refresh `last_seen`. Legacy MAC-less records are removed only when their complete provenance is exactly `arp_table`; records supported by any other source remain retained.

DHCP lease input is passive assignment metadata. Valid records may contribute `ip`, normalized `mac`, `hostname`, `lease_expires_epoch`, `dhcp_client_id`, and `dhcp_lease_source`, but DHCP cannot overwrite stronger current collector, gateway, integration, or known-infrastructure identity metadata. A lease never sets reachability and never creates or refreshes `last_seen`. Multiple clients that share an IP remain separate when their normalized MAC addresses differ. Source health distinguishes found, empty, missing, unreadable, malformed, I/O-error, and partial input states without exposing rejected record contents.

Operational monitoring is separate from passive observation. The authoritative policy is `is_operationally_monitored()` in HIOC Core. Infrastructure-class devices, gateway and collector roles/types, known-infrastructure definitions, local-host and gateway records, authoritative integration records, and explicitly monitored records remain monitored. Unknown and future discovery sources default to monitored until their semantics are deliberately added to that policy boundary.

An ordinary client whose complete provenance is limited to `arp_table` and/or `dhcp_leases` remains inventory-visible but is not availability-monitored. Once its passive evidence ages, it remains `watch`, exposes `status: stale` or `status: unknown`, preserves the last positive observation, and does not generate an availability incident from observation age alone. A DHCP-only record remains `watch` with operational status `unknown` even while its assignment observation is current, because DHCP assignment does not prove current reachability.

Passive-client archival or expiration is not defined by this correction. Retention duration and cleanup remain a separate future configurable policy checkpoint.

Service object:

- `id`
- `name`
- `type`
- `device_id`
- `status`
- `port`
- `source`

Topology object:

- `root_id`
- `edges`: parent/child network relationships.

Dependency object:

- `edges`: service dependency relationships such as device-to-DNS, device-to-DHCP, and device-to-MQTT.

## Internal Event

Internal events are stored locally and are not public MQTT contracts.

- `id`
- `type`
- `timestamp`
- `source`
- `payload`

Current inventory event types:

- `DeviceDiscovered`
- `InventoryChanged`
- `TopologyChanged`

## Correlated Incident

Correlated incident state is stored in `state/incidents/active.json`, `state/incidents/history.json`, and `state/incidents/summary.json`.

- `id`: stable incident identifier derived from the correlated root-cause key.
- `key`: duplicate-suppression key for the probable root cause.
- `status`: public compatibility status, typically `active`, `resolved`, or `none`.
- `phase` / `lifecycle`: detailed lifecycle phase: `detected`, `confirmed`, `active`, `recovering`, or `resolved`.
- `severity`: highest correlated severity.
- `system`: primary affected domain.
- `root_cause`: probable root cause.
- `confidence_percent`: root-cause confidence from 0 to 100.
- `affected`: impacted systems and services.
- `evidence`: correlated signal reasons.
- `started`, `updated`, `resolved`, `end_time`: ISO-8601 lifecycle timestamps.
- `duration_seconds`: final incident duration after resolution or supersession.
- `recovery_type`: derived recovery category such as `automatic`, `superseded`, `interrupted`, or `unknown`.
- `review`: operator review generated for completed history entries.

Incident review object:

- `title`
- `severity`
- `started`
- `resolved`
- `duration`
- `duration_seconds`
- `root_cause`
- `confidence_percent`
- `affected_systems`
- `affected_services`
- `impact_summary`
- `evidence`
- `timeline`: chronological event rows with `timestamp` and `message`.
- `recovery`
- `recommended_action`
- `incident_id`
- `recovery_type`

Incident summary includes derived history context:

- `history_stats.today`
- `history_stats.last_7_days`
- `history_stats.last_30_days`
- `history_stats.automatic_recoveries`
- `history_stats.manual_intervention_required`
- `history_stats.average_duration`
- `history_stats.longest_incident`
- `recent_incidents`: compact completed incident rows for dashboard review.
- `recent_incident_reviews`: full review objects for the most recent completed incidents.
- `latest_incident_review`: full review for the most recent completed incident.

## Capability

Capabilities are stored locally in `state/inventory/capabilities.json`.

- `id`
- `device_id`
- `capability`
- `source`
- `status`
- `metadata`

## Platform Version

Platform version state is stored in `state/platform/version.json`.

- `status`
- `updated`
- `versions`

The `versions` object mirrors `VERSION.yaml`.

## Platform Status

Platform status state is stored in `state/platform/status.json`.

- `status`
- `updated`
- `hioc_version`
- `core`
- `dashboard`
- `schema`
- `mqtt_api`
- `build`
