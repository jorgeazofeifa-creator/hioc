# HIOC Release Process

PE-3 Action 9 is outside the release path. After its new tool is reviewed,
committed, pushed, source-synchronized, and separately authorized, it may verify
the exact Action 8 PASS evidence and current runtime read only. It does not use
`release/upgrade.sh`, `pi4/install_pi4.sh`, `/usr/bin/time`, or the manufacturer
generator. Its private Evidence Report does not alter release artifacts,
production files, transport staging, or future checkpoints.

The corrected manufacturer-validator deployment is intentionally outside
`release/upgrade.sh`: the broad release path invokes installer behavior that is
unrelated to this corrective checkpoint. The dedicated PE-3 tool may publish
only `pi4/bin/hioc-validate-manufacturer.py`. It requires a prior separately
reviewed release-source synchronization PASS and stops after validator identity
and protected-state evidence. No restart, reload, schedule change, engine run,
generator run, or later PE-3 action is part of this boundary.

The Action 8 permission-class correction changes the manufacturer validator:
private sidecar/status files remain exact `0600`, while the inventory input uses
its established no-group/world-write rule. It does not change the Action 8
wrapper or its bootstrap blob. The corrected validator still requires governed
source synchronization and supported runtime deployment/identity verification
before any separately authorized rerun.

The PE-3 Action 8 bootstrap remains a separate source-checkout synchronization
boundary. Its committed trust gate now freezes the current independently
reviewed wrapper blob after preparation stopped on the superseded identity.
This repository correction does not itself prepare or execute the bootstrap and
does not authorize runtime deployment, Action 8, or Action 9.

Action 8 performance evidence no longer relies on `/usr/bin/time`; governed
Python performs child launch and measurement. This is a wrapper/governance
change, not a new host-package or runtime-deployment dependency. Its new Git
blob must pass a separately authorized post-push bootstrap before another run.

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
The invocation is Action 5B and is forbidden until the separate bootstrap-safe
Action 5A has synchronized the target source and proven the script's exact Git
and worktree identity.

The installer owns creation and `0700` normalization of empty manufacturer
scaffolding. Release protection distinguishes that scaffolding from payload:
versions, database/manifest bytes, sidecar/status artifacts, unexpected entries,
symlinks, and configuration remain protected. Release backup intentionally
excludes persistent manufacturer data, so rollback does not correct a
scaffolding-only observation. The read-only Action 5C closes the deployed
runtime after exact semantic revalidation. Because the target may predate that
new script, inline Action 5C-A first synchronizes the clean release-source
checkout and proves the script's Git/worktree identity, then stops. The
repository-controlled Action 5C-B remains a separate authorization and never
invokes upgrade or creates another release backup.

PE-3 Action 6 is not a release deployment and creates no release backup. Its
repository-controlled installer verifies exact source/self/validator/runtime
identity, then publishes only the frozen manufacturer database/manifest pair as
one immutable version. Action 6-A bootstrap and Action 6-B installation are
separate authorizations. Configuration activation remains Action 7.

Action 7 is not a release deployment. Its repository-controlled script is made
available through a separate Action 7-A source synchronization/identity gate;
only separately authorized Action 7-B may atomically activate the exact
installed immutable manufacturer dataset in runtime configuration. It does not
invoke the release upgrade or rollback flow and cannot chain manufacturer
generation.

Action 8 likewise is not a release deployment. Its governed source-side wrapper
coordinates the already deployed manual generator and bounded evidence only.
Making that new wrapper available requires a separately authorized
release-source fast-forward/script-identity gate that stops after exact proof;
its exact full 40-hex governance commit is supplied only after publication and
explicit approval. It is not a runtime upgrade and cannot invoke generation.
The separately authorized generator wrapper accepts no release-evidence path;
it creates and reports one private invocation-owned Action 8 evidence directory
after its read-only preconditions pass.
The wrapper validates the installed immutable dataset selected by configuration;
it does not consume or require the earlier `/tmp` transport staging. Transfer
staging ceases to be authoritative after reviewed immutable publication and may
be removed only through a separately authorized cleanup boundary.
Generator failure evidence is likewise not a release artifact. The Action 8
wrapper retains it privately in the invocation-owned evidence directory as
performance followed by result-last `generation-failure.json`; raw captures are
not published. Any wrapper identity change requires a new separately authorized
release-source synchronization/script-identity gate before execution.

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
