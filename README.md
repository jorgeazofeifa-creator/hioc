# HIOC

Home Infrastructure Operations Center.

HIOC turns a Raspberry Pi 4 into a self-hosted infrastructure monitoring appliance and uses Home Assistant as the operator console.

Its purpose is to help an operator quickly answer:

- What is happening?
- Why is it happening?
- What is affected?
- What should I do?
- What happened while I was away?

## Main Capabilities

- Pi4 infrastructure monitoring and retained MQTT telemetry.
- Incident detection, correlation, lifecycle tracking, and historical incident review.
- Passive Living Inventory for infrastructure documentation, device health, services, topology, and dependencies.
- Forecast and history data for operational trends.
- Dashboard v2 Home Assistant console for Executive, Operations, Diagnostics, Inventory, Network, and Servers views.
- Release packaging, install, upgrade, validation, rollback, and platform version reporting.

## Repository Structure

```text
pi4/                    Pi4 engines, shared runtime, configuration, and validation
homeassistant/          Home Assistant packages, dashboards, install, and validation
release/                Release build, package, install, upgrade, rollback, and validation scripts
docs/                   Project, architecture, install, integration, design, and data documentation
docs/reviews/           Archived historical reviews
tests/                  Unit and YAML validation tests
ROADMAP.md              Short public roadmap summary
DECISIONS.md            Architecture Decision Record log
VERSION.yaml            Machine-readable release version manifest
```

## Installation Overview

On PI3, clone or update the Git-managed release source, validate it, and install from there:

```bash
git clone https://github.com/jorgeazofeifa-creator/hioc.git /home/jazofv1/hioc-release-source
cd /home/jazofv1/hioc-release-source
bash release/validate.sh
bash release/install.sh pi4
/home/jazofv1/hioc/pi4/validate_pi4.sh
```

`/home/jazofv1/hioc` is the deployed production runtime, not a Git checkout. Do not run `git pull`, `git reset`, `git clean`, `git checkout`, or other source-management commands there. Initial installation and upgrades must use `/home/jazofv1/hioc-release-source` or a validated release package. Production version identity comes from `VERSION.yaml` and release metadata, not runtime Git state.

For Home Assistant:

```bash
cd /config/hioc
bash homeassistant/install_ha.sh
bash homeassistant/validate_ha.sh
ha core check
ha core restart
```

See [docs/INSTALL.md](docs/INSTALL.md) for installation, configuration, upgrade, and rollback details.

## Documentation

[docs/HIOC_MASTER_PLAN.md](docs/HIOC_MASTER_PLAN.md) is the authoritative source for project direction, implementation phases, and current development status.

The Master Plan governs project direction. It does not replace the technical documentation below.

## Documentation Map

| I want to know... | Read |
| --- | --- |
| What is HIOC? | [README.md](README.md) |
| Where is the project going? | [docs/HIOC_MASTER_PLAN.md](docs/HIOC_MASTER_PLAN.md) |
| What is deployed today? | [docs/SYSTEM_REFERENCE.md](docs/SYSTEM_REFERENCE.md) |
| What is the project context? | [docs/PROJECT.md](docs/PROJECT.md) |
| How is it built? | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| How does it run and how is it validated or recovered? | [docs/OPERATIONS.md](docs/OPERATIONS.md) |
| What network infrastructure does it depend on? | [docs/NETWORK_FOUNDATION.md](docs/NETWORK_FOUNDATION.md) |
| How does source become a production deployment? | [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) |
| What do incident states mean? | [docs/INCIDENT_MODEL.md](docs/INCIDENT_MODEL.md) |
| What is the approved recovery baseline? | [docs/RECOVERY_BASELINE.md](docs/RECOVERY_BASELINE.md) |
| How will devices evolve into operator-managed assets? | [docs/ASSET_MODEL.md](docs/ASSET_MODEL.md) |
| How do shared runtime libraries work? | [docs/CORE.md](docs/CORE.md) |
| How does MQTT work? | [docs/MQTT.md](docs/MQTT.md) |
| How does Home Assistant integrate? | [docs/HOME_ASSISTANT.md](docs/HOME_ASSISTANT.md) |
| How does the dashboard consume operational truth and preserve its layout? | [docs/DASHBOARD_ARCHITECTURE.md](docs/DASHBOARD_ARCHITECTURE.md) |
| What is the data model? | [docs/DATA_MODEL.md](docs/DATA_MODEL.md) |
| How is the dashboard designed visually? | [docs/DESIGN_SYSTEM.md](docs/DESIGN_SYSTEM.md) |
| How is Dashboard v2 organized? | [docs/DASHBOARD_V2_PLAN.md](docs/DASHBOARD_V2_PLAN.md) |
| How do I install it? | [docs/INSTALL.md](docs/INSTALL.md) |
| What changed between versions? | [docs/CHANGELOG.md](docs/CHANGELOG.md) |
| How are releases built? | [docs/RELEASE.md](docs/RELEASE.md) |
| Why were major technical decisions made? | [DECISIONS.md](DECISIONS.md) |
| What comes next? | [ROADMAP.md](ROADMAP.md) |

## Documentation Governance

- [docs/HIOC_MASTER_PLAN.md](docs/HIOC_MASTER_PLAN.md) owns project direction, implementation phases, current objective, next task, and working agreements.
- [docs/SYSTEM_REFERENCE.md](docs/SYSTEM_REFERENCE.md) is the authoritative current-state reference: the Master Plan explains how HIOC evolves, while the System Reference Manual explains what HIOC is today.
- [docs/OPERATIONS.md](docs/OPERATIONS.md) owns current runtime operation, schedules, outputs, validation, and recovery procedures.
- [docs/NETWORK_FOUNDATION.md](docs/NETWORK_FOUNDATION.md), [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md), and [docs/INCIDENT_MODEL.md](docs/INCIDENT_MODEL.md) own their focused operational contracts.
- Technical details belong in the focused technical documents linked above.
- [ROADMAP.md](ROADMAP.md) is a short public summary and points to the Master Plan for the detailed implementation roadmap.
- [DECISIONS.md](DECISIONS.md) explains why long-term architectural decisions were made.
- [VERSION.yaml](VERSION.yaml) is machine-readable version data and should only change during releases.
- Files in [docs/reviews/](docs/reviews/) are archived historical reviews and should not be rewritten.
