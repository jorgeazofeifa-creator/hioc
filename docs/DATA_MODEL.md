# HIOC Data Model

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
- `display_name`: hostname, name, IP, or ID.
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
- `health_score`
- `health_status`
- `health_reasons`
- `parent_id`
- optional integration hints such as `parent_mac`, `parent_ip`, `uplink_mac`, `uplink_ip`, or `parent_device_id`

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
