# HIOC Project

HIOC is the Home Infrastructure Operations Center: a production-oriented, self-hosted monitoring stack for home infrastructure.

## Document Ownership

This document explains the project at a high level: major subsystems, how they fit together, and where files live.

It links to focused documents instead of duplicating their details:

- Project direction and current phase: [HIOC_MASTER_PLAN.md](HIOC_MASTER_PLAN.md)
- System architecture: [ARCHITECTURE.md](ARCHITECTURE.md)
- Installation and deployment: [INSTALL.md](INSTALL.md)
- MQTT contract: [MQTT.md](MQTT.md)
- Home Assistant integration: [HOME_ASSISTANT.md](HOME_ASSISTANT.md)
- Data model: [DATA_MODEL.md](DATA_MODEL.md)

## Product Principles

- Treat Home Assistant as an operator console, not only a sensor list.
- Explain what is happening, why it is happening, what is affected, and what action is recommended.
- Prefer self-discovery and correlation over manual configuration.
- Keep existing Pi4 toolkit telemetry stable and extend it through HIOC subsystems.
- Store local JSON state before publishing MQTT so data remains inspectable during broker or Home Assistant issues.

## Repository Layout

```text
pi4/bin/                  Pi4 executable engines
pi4/lib/                  Shell and Python shared runtime modules
pi4/config/               Example Pi4 configuration
homeassistant/packages/   Home Assistant packages
homeassistant/dashboards/ Home Assistant dashboard YAML
docs/                     Project documentation
tests/                    Unit tests
```

## Major Subsystems

- Platform Core: shared runtime services used by engines.
- Inventory Engine: passive infrastructure discovery and living documentation.
- Incident Engine and Correlation Engine: active incident state, root cause, evidence, and lifecycle.
- History Engine: historical samples, forecast state, and trend data.
- MQTT Publishing Layer: retained payload contract for Home Assistant.
- Home Assistant Integration: packages, entities, dashboards, and operator console.

For technical runtime flow and subsystem boundaries, see [ARCHITECTURE.md](ARCHITECTURE.md).
