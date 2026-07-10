# HIOC MQTT Contract

## Document Ownership

This document owns MQTT topics, payload expectations, retention behavior, publishing strategy, topic hierarchy, and MQTT discovery/integration notes.

It should not contain roadmap, dashboard design, installation, or Home Assistant UI details. For payload object fields, see [DATA_MODEL.md](DATA_MODEL.md). For Home Assistant entities, see [HOME_ASSISTANT.md](HOME_ASSISTANT.md).

Default base topic:

```text
home/infrastructure/hioc
```

## Incident Topics

```text
home/infrastructure/hioc/incidents/active
home/infrastructure/hioc/incidents/history
home/infrastructure/hioc/incidents/summary
home/infrastructure/hioc/timeline/history
home/infrastructure/hioc/timeline/latest
home/infrastructure/hioc/status
home/infrastructure/hioc/status/detail
```

Correlation Engine v2 publishes through the same incident topics. The public topic names are unchanged, and existing Home Assistant sensors continue to read `status`, `severity`, `system`, `title`, `root_cause`, `confidence_percent`, `affected`, and timeline fields from the retained JSON payloads.

Completed incident history entries include a derived `review` object so operators can understand what happened after recovery. The `incidents/summary` payload also includes `history_stats`, `recent_incidents`, `recent_incident_reviews`, and `latest_incident_review` attributes for Dashboard v2. These are additive fields on existing retained topics.

## Forecast Topics

```text
home/infrastructure/hioc/forecast
home/infrastructure/hioc/statistics
home/infrastructure/hioc/history/status
```

## Living Inventory Topics

```text
home/infrastructure/hioc/inventory
home/infrastructure/hioc/inventory/devices
home/infrastructure/hioc/inventory/services
home/infrastructure/hioc/inventory/topology
home/infrastructure/hioc/inventory/dependencies
home/infrastructure/hioc/inventory/summary
home/infrastructure/hioc/inventory/status
```

## Platform Topics

```text
home/infrastructure/hioc/platform/version
home/infrastructure/hioc/platform/status
```

All HIOC publications are retained so Home Assistant recovers state after restart.
The Living Inventory engine publishes all inventory topics over one persistent MQTT connection per run. The public topic names and JSON schema remain unchanged.
