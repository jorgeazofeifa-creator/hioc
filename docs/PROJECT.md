# HIOC Project

HIOC is the Home Infrastructure Operations Center: a production-oriented, self-hosted monitoring stack for home infrastructure.

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

