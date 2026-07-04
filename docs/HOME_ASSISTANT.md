# HIOC Home Assistant Integration

HIOC integrates with Home Assistant through MQTT sensors, template sensors, and dashboard YAML.

## Packages

Installable packages are in `homeassistant/packages`:

- `hioc_incident_center.yaml`
- `hioc_predictive_analytics.yaml`
- `hioc_living_inventory.yaml`
- `hioc_platform.yaml`

The installer copies these files into `/config/packages`.

## Dashboards

Dashboards are in `homeassistant/dashboards` and are copied into `/config/dashboards` by `homeassistant/install_ha.sh`.

The Dashboard v2 file is:

- `hioc_dashboard_v2.yaml`

The Living Inventory dashboard uses inventory sensors from `hioc_living_inventory.yaml`.
