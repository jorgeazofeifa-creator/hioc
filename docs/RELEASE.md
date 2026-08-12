# HIOC Release Process

HIOC releases are built from the repository into a versioned package.

## Document Ownership

This document owns release procedure, branch strategy, tagging expectations, packaging, versioning workflow, and release checklists.

It should not contain roadmap or implementation status. For install and upgrade commands from an operator perspective, see [INSTALL.md](INSTALL.md). For repository-to-production boundaries, see [DEPLOYMENT.md](DEPLOYMENT.md). For the current development phase, see [HIOC_MASTER_PLAN.md](HIOC_MASTER_PLAN.md).

## Release Execution Context

PE-3 Production Action 5 invokes the supported upgrade flow only through
`tools/hioc-pe3-action5-deploy.sh`. That governed transaction proves source and
script identity and release validation before mutation, captures and validates
the resulting timestamped backup, and verifies deployed runtime artifacts. It
does not install manufacturer data or activate configuration.

On PI3, normal release work is prepared or executed from the authoritative source checkout after approved changes are pulled from GitHub:

```text
/home/jazofv1/hioc-release-source
```

This is the authoritative clean source checkout for release execution on PI3. Release validation, build, package, install, upgrade, and rollback operations use this development and release checkout. `/home/jazofv1/hioc` is a non-Git deployed production runtime containing persistent runtime state and installer-managed differences. Git operations are unsupported inside the runtime.

Validated versioned release packages remain supported and do not require deployment directly from a Git checkout. See [HIOC_MASTER_PLAN.md](HIOC_MASTER_PLAN.md) for governance, [../DECISIONS.md](../DECISIONS.md#adr-0013-development-checkout-and-production-runtime-have-separate-roles) for ADR-0013, and [INSTALL.md](INSTALL.md) for operator commands.

## Version Manifest

The authoritative version file is:

```text
VERSION.yaml
```

Required keys:

- `hioc_version`
- `core`
- `incident_engine`
- `correlation_engine`
- `forecast_engine`
- `inventory_engine`
- `dashboard`
- `schema`
- `mqtt_api`
- `installer`
- `build`

## Release Scripts

Release scripts live in `release/`:

- `build.sh`: creates `dist/build/HIOC-<version>`.
- `package.sh`: creates `dist/packages/HIOC-<version>.tar.gz`.
- `validate.sh`: validates release source structure, version manifest, Python syntax, and shell syntax when tools are available.
- `install.sh`: installs Pi4 and, when `/config` exists, Home Assistant files.
- `upgrade.sh`: backs up the current install, copies the new release, and reruns install.
- `rollback.sh`: restores the last release-upgrade backup or a provided backup path.

## Build

`release/build.sh` uses Git only at the authoritative source boundary to enumerate tracked project files and record the source commit. Release artifacts contain tracked source plus the generated release manifest and never contain `.git`.

```bash
bash release/build.sh
bash release/package.sh
```

Artifact:

```text
dist/packages/HIOC-1.0.0.tar.gz
```

## Install

```bash
bash release/install.sh
```

The default target auto-detects the Pi4 collector when the Pi4 toolkit config exists and Home Assistant when `/config` exists.

Install only Pi4:

```bash
bash release/install.sh pi4
```

Install only Home Assistant files:

```bash
bash release/install.sh ha
```

## Upgrade

```bash
cd /home/jazofv1/hioc-release-source
bash release/validate.sh
bash release/upgrade.sh
```

The upgrade script writes the latest backup path to:

```text
$HIOC_INSTALL_DIR/backups/last-upgrade-backup
```

`HIOC_INSTALL_DIR` defaults to `/home/jazofv1/hioc`. The upgrade requires `rsync`, backs up replaceable installation content including configuration, preserves `state`, `history`, `logs`, and `backups`, copies the validated release without `.git` or `dist`, and reruns the Pi4 installer. New upgrade backups exclude `.git`, whether or not historical runtime metadata still exists when the backup is created.

The installer synchronously runs required HIOC engines under fail-fast shell behavior. A required Incident Engine MQTT connection or publication failure returns a nonzero engine status and therefore fails installation or upgrade truthfully. Incident state is written locally before MQTT publication and remains available for diagnosis; a failed upgrade must be investigated or rolled back rather than reported as successful.

After a successful install or upgrade, run the deployed read-only MQTT validator
and retain its output and exit status with the release evidence:

```bash
/home/jazofv1/hioc/pi4/bin/hioc-validate-mqtt.py
```

The command validates the retained Incident Engine contract against the
configured broker; [MQTT.md](MQTT.md#operational-runtime-validation) owns its detailed
semantics and prerequisites.

## Rollback

Use the latest upgrade backup:

```bash
cd /home/jazofv1/hioc-release-source
bash release/rollback.sh
```

Use a specific backup:

```bash
cd /home/jazofv1/hioc-release-source
bash release/rollback.sh /home/jazofv1/hioc/backups/release-upgrade-YYYYMMDD-HHMMSS
```

With no argument, rollback reads `$HIOC_INSTALL_DIR/backups/last-upgrade-backup`. A specific backup path is also supported. Run rollback from the authoritative source checkout or a validated release package so the supported script is used; restoration targets `HIOC_INSTALL_DIR`, which defaults to `/home/jazofv1/hioc`. Rollback excludes every `.git` directory, including nested metadata in historical backups, while restoring legitimate application files and hidden files. It does not use runtime Git history and cannot recreate runtime Git metadata.

Source recovery comes from GitHub, the authoritative release-source checkout, or an approved release package. Runtime recovery comes from release backups and preserved configuration, state, history, logs, and operational data. Neither recovery boundary depends on `/home/jazofv1/hioc/.git`.

## Runtime Version Reporting

The platform status publisher writes:

```text
state/platform/version.json
state/platform/status.json
```

It publishes retained MQTT topics:

```text
home/infrastructure/hioc/platform/version
home/infrastructure/hioc/platform/status
```
