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
