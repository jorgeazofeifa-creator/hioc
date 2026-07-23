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

The Incident Engine publishes the same ordered topic and payload set over one Core MQTT connection per run. This transport implementation does not change topic names, retained semantics, JSON structures, embedded reviews, history ordering, or status content. Authoritative local files are written before publication. A required connection or publication failure produces a nonzero Incident Engine status; earlier topics may already have been retained when a later topic fails, and the final online status is not published after such a failure.

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
The Living Inventory and Incident engines publish their topic sets over one persistent MQTT connection per run. The public topic names and JSON schemas remain unchanged.

## Operational Validation

Runtime MQTT validation proves that the deployed HIOC configuration can reach the
broker and retrieve the retained Incident Engine contract. Run the deployed
validator after an install or upgrade:

```bash
/home/jazofv1/hioc/pi4/bin/hioc-validate-mqtt.py
```

The command loads `MQTT_HOST`, `MQTT_PORT`, optional `MQTT_USER` and
`MQTT_PASSWORD`, and `HIOC_BASE_TOPIC` through HIOC's existing configuration
service. Configuration precedence remains the Pi4 toolkit configuration,
deployed HIOC configuration, and then matching process-environment overrides.
The broker is not assumed to be local. Current HIOC MQTT clients do not define a
TLS configuration contract, and this validator does not introduce one.

`python3` and `mosquitto_sub` must be installed, and the configured account must
be allowed to read the retained topics. Each read has a bounded timeout. The
validator checks:

```text
<HIOC_BASE_TOPIC>/incidents/active
<HIOC_BASE_TOPIC>/incidents/history
<HIOC_BASE_TOPIC>/incidents/summary
<HIOC_BASE_TOPIC>/timeline/history
<HIOC_BASE_TOPIC>/timeline/latest
<HIOC_BASE_TOPIC>/status/detail
<HIOC_BASE_TOPIC>/status
```

JSON topics must contain a nonempty, valid UTF-8 JSON payload. The scalar status
must be `online`. Output reports each observed topic and payload byte count
without dumping payloads or credentials. Incident history also reports its
record count when it is a JSON array and whether any record contains an embedded
review.

- `PASS` and exit code `0` mean every required retained topic was read and
  validated. A legacy nonempty history without embedded review data is reported
  as a warning but does not independently fail the transport contract.
- `FAIL` and exit code `1` mean required configuration, subscriber execution,
  connectivity, payload presence, JSON, UTF-8, or scalar status validation
  failed.
- `INCOMPLETE` and exit code `2` mean at least one bounded read ended without a
  retained payload, while no stronger failure was observed.

The command is read-only: it never publishes a test payload or changes retained
state. Preserve its concise console output, exit status, deployed commit, and
relevant redacted broker or consumer evidence in the checkpoint Evidence Report.
Source comparison and unit tests remain necessary, but they do not prove
end-to-end retained MQTT behavior in the deployed environment.
