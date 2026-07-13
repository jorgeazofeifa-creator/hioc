# HIOC Home Assistant Integration

HIOC integrates with Home Assistant through MQTT sensors, template sensors, and dashboard YAML.

## Document Ownership

This document owns Home Assistant integration: packages, entities, sensors, MQTT discovery behavior, dashboard installation, and dashboard integration points.

It should not duplicate the MQTT contract, data model, dashboard visual design, or dashboard operational-truth policy. For topic details, see [MQTT.md](MQTT.md). For payload fields, see [DATA_MODEL.md](DATA_MODEL.md). For dashboard design and UX rules, see [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md) and [DASHBOARD_V2_PLAN.md](DASHBOARD_V2_PLAN.md). For dashboard truth ownership, layout-baseline protection, and storage-versus-YAML deployment architecture, see [DASHBOARD_ARCHITECTURE.md](DASHBOARD_ARCHITECTURE.md).

## Packages

Installable packages are in `homeassistant/packages`:

- `hioc_incident_center.yaml`
- `hioc_predictive_analytics.yaml`
- `hioc_living_inventory.yaml`
- `hioc_platform.yaml`

The installer copies these files into `/config/packages`.

## Dashboards

Dashboards are in `homeassistant/dashboards` and are copied into `/config/dashboards` by `homeassistant/install_ha.sh`.

The current live Dashboard v2 is storage-managed and does not automatically consume the copied YAML file. The current deployment boundary and the separately planned YAML-mode migration are documented in [DASHBOARD_ARCHITECTURE.md](DASHBOARD_ARCHITECTURE.md).

The Dashboard v2 file is:

- `hioc_dashboard_v2.yaml`

The Living Inventory dashboard uses inventory sensors from `hioc_living_inventory.yaml`.

Correlation Engine v2 uses the existing incident package and sensors wherever possible. Dashboard v2 displays current incident, root cause, confidence, affected systems, and timeline from the retained incident and timeline MQTT payloads without adding a new public MQTT contract.

Dashboard v2 also uses the existing `sensor.hioc_incident_summary` attributes to show incident history context:

- today, 7-day, and 30-day incident counts
- automatic recovery count
- manual intervention count when known
- average and longest incident duration
- recent completed incidents
- the latest completed incident review with impact, evidence, timeline, recovery, and recommended action
