# HIOC Release Process

## Action E native non-lifecycle validation — PASS / CLOSED

Release prerequisite: architecture-matched PI3 validation for the hardened Action E implementation is PASS/CLOSED. Production Action E remains NOT STARTED and requires current-consumer compatibility, separate synchronization, final repreparation, and exactly-one-invocation authorization.

Operator-reported evidence records separate PI3 synchronization from
`8e4880c7fa5fbea4583eea0d4485a65493fb6b36` to implementation commit
`70cfceba3ddc5dd05818fa6f27653709abd9819c` as **PASS**. On host `nutandpihole`
as `jazofv1`, branch `main`, HEAD and `origin/main` matched the implementation,
ahead/behind was `0 0`, source was clean, and synchronization checks PASSed.
No native validation or lifecycle action ran during synchronization.

The subsequent separately authorized read-only supervisor directly exercised
committed controlled validation primitives without calling production Action E
`main()` or allocating Action E evidence. **`ACTION_E_NATIVE_VALIDATION=PASS`**
closes the architecture-matched prerequisite; it does not mean lifecycle Action E
PASS or completion. Target, current source, producer/consumer compatibility,
strict D eligibility, controlled startup, distributions, native integrity,
capability, network-side-effect and construction-immutability checks all PASSed.
No native-validation failure code or failure stage was reported.

Both controlled `-I -B -S` children measured implementation `cpython`, version
`[3, 11, 2]`, SOABI `cpython-311-aarch64-linux-gnu`; prefix, base prefix, exec
prefix and base exec prefix were `/usr`. Base executable was `/usr/bin/python3.11`.
Isolated, no-site, no-user-site, environment-ignore, safe-path and bytecode
suppression were active. Exact initial paths were `/usr/lib/python311.zip`,
`/usr/lib/python3.11`, `/usr/lib/python3.11/lib-dynload`.

Measured construction executable:
`/home/jazofv1/hioc/runtime/pe4/environments/.construct-cpython311-websockets16.1.1-lock-v1-mwJVPNqh/bin/python`.
Its measured filesystem identity was device `45826`, inode `823209`.
Exact installed distributions were
`{"pip": "23.0.1", "setuptools": "66.1.1", "websockets": "16.1.1"}`.
The actual governed AArch64 native module loaded from
`/home/jazofv1/hioc/runtime/pe4/environments/.construct-cpython311-websockets16.1.1-lock-v1-mwJVPNqh/lib/python3.11/site-packages/websockets/speedups.cpython-311-aarch64-linux-gnu.so`
through `VerifiedNativeLoader`, with SHA-256
`b786db296f7d0677ddeceb7efbe963bc316a094f36e12388caa1333763ca4c1b`.
This native proof exercised the AArch64 extension, not the Windows source fallback,
and the corrected controlled capability flow PASSed.

Measured `FILESYSTEM_WRITE_ATTEMPTS=0`, `NETWORK_ATTEMPTS=0`,
`CONSTRUCTION_IMMUTABILITY=PASS`, `ACTION_D_HANDOFF_UNCHANGED=TRUE`,
`NO_ACTION_E_EVIDENCE_CREATED=TRUE`, `SOURCE_UNCHANGED=TRUE`, and
`ATIME_EXCLUDED=TRUE` preserve the read-only comparison boundary. No production
Action E evidence or production E terminal PASS is claimed.

The immutable D producer remains `6c431494c88688fef9a2fec7c7e81de0f503bdc2`.
Accepted construction remains
`/home/jazofv1/hioc/runtime/pe4/environments/.construct-cpython311-websockets16.1.1-lock-v1-mwJVPNqh`;
accepted D evidence remains `/tmp/hioc-pe4-runtime-construct-LW9Dvay6`, SHA-256
`a31f1e841f437dece13d327f14a99a93d5f96a8e258b9786cc6e49358821350d`.
Frozen D source SHA-256 remains
`e979cc6049f8912c23e880f121fd2988d0354623c4f2a7d27eafb310e4b0c213`.
Validated E source blob was `f672c9327e2308593f218eadad5abd158006d498`;
compatibility-helper blob was `807599005ad5ff0adc9335daf04b2598a3335dd6`.
D/common/lock blobs remained respectively
`6dc8fe1c058f8b1de6f16d7ea7c88c133e1128b7`,
`4d9289d174e8647bbc67b1a6b83868bda699bad7`,
`8f2652298f12734b0e4f43341a48ed5702fe696e`.

The resulting documentation-only descendant closure commit is the **next Action E
current-consumer candidate**. Do not permanently pin implementation commit
`70cfceba3ddc5dd05818fa6f27653709abd9819c` as the final E consumer. Before eventual
E execution, reverify producer/new-consumer compatibility, separately authorize
PI3 synchronization from the implementation to the resulting closure commit,
reprepare Action E against that closure commit, then obtain separate authorization
for exactly one Action E invocation. This closure performs or authorizes none of
those operations and changes no source, tests, dependency lock, or runtime objects.

Lifecycle remains: replacement B PASS/CLOSED; C PASS exactly once; D-PREP
PASS/CLOSED; D PASS/CLOSED; E NOT STARTED; F NOT STARTED; G NOT STARTED;
rollback NOT PERFORMED. Operator evidence explicitly reported
`ACTION_E_EXECUTED=FALSE`, `ACTION_F_EXECUTED=FALSE`, `ACTION_G_EXECUTED=FALSE`,
`NO_LIFECYCLE_ACTION_EXECUTED=TRUE`, `AUTOMATIC_RETRY=FALSE`,
`MANUAL_CLEANUP=FALSE`, `ROLLBACK_PERFORMED=FALSE`, `STOP_REQUIRED=TRUE`.
No lifecycle action ran during native validation or documentation closure.
No PI3/PI5 access or production synchronization occurs during this closure.
Next checkpoint: `ACTION_E_FINAL_REPREPARATION_READY_FOR_SEPARATE_AUTHORIZATION`.

## Historical Action E controlled startup implementation — native prerequisite then pending

The corrective source is the next consumer candidate. Windows synthetic validation does not certify the Linux AArch64 native module; architecture-matched non-lifecycle validation remains a release prerequisite before E authorization.

Action E construction interpreters use **`-I -B -S`**: isolated startup,
interpreter-level bytecode suppression, and no normal `site` initialization.
Neither `site.main()` nor `site.addsitedir()` is called. Executable/library
`._pth` overrides, build-layout markers, malformed/duplicate venv configuration,
wrong interpreter binding, and unexpected initial paths fail closed before
package execution. The outer process validates the construction interpreter
against the governed `/usr/bin/python3` used by D's `--copies` installation.
Python 3.11 `-S` leaves base prefixes active; E validates venv provenance
separately and never changes `sys.prefix` to fake activation.

The governed initial path model is exactly `/usr/lib/python311.zip`,
`/usr/lib/python3.11`, `/usr/lib/python3.11/lib-dynload`. No user site, cwd,
ambient `PYTHONPATH`, additional site/dist-packages root, or `.pth` path is
adopted. Distribution discovery explicitly reads the single validated
construction `lib/python3.11/site-packages` through standard-library metadata;
pip, setuptools, websockets and entry points are not executed by discovery.
One pip, optional single setuptools, exactly websockets `16.1.1`, no extras or
duplicates, and bounded bootstrap-version syntax remain the acceptance policy.

The E-local 52-member manifest comes from the exact frozen 188095-byte wheel
with SHA-256 `86d7f0f8bdb25d2c632b72527325e4776430fd5bc61b9118de4e2b8ddb5f5b01`.
Installed member bytes are verified before execution. The restricted capability
loader compiles verified package source in memory, ignores construction `.pyc`,
and permits only the reviewed websockets graph plus trusted standard-library
imports. Optional `python_socks` and unrelated third-party imports are blocked.
The native member is bound to SHA-256
`b786db296f7d0677ddeceb7efbe963bc316a094f36e12388caa1333763ca4c1b`.
The capability child appends exactly one governed site directory after validating
its startup/finder state, keeping standard-library paths first.

The E-local redirect probe now supplies `InvalidStatus(Response(...))` and
validates the returned preexisting-socket refusal exception, matching the exact
16.1.1 API. Version, canonical asyncio connect, required signature parameters,
`**kwargs`, `InvalidStatus`, and `PayloadTooBig` remain required. No actual
connect, DNS, proxy lookup, event-loop connection, SOCKS call, or URL open is
performed. Common/F/G's historical probe is not changed or certified here.

Construction-read-only means unchanged directory entries, content, sizes,
ownership, permissions, identities, symlink targets, mtime and ctime. Recursive
checks exclude atime and cover the D eligibility marker and D evidence too,
including ordinary validation and E-evidence-publication failure paths. E's
only deliberate filesystem writes are its own `/tmp` evidence. No permission
flipping, construction copy, cleanup dependence, retry, rollback or F/G chaining
is introduced. Child output is limited to 64 KiB per stream with a 60-second
execution timeout. Success evidence retains its existing ten-field JSON and
six-field terminal contract.

Trust remains bounded to governed CPython/system libraries and the hash-bound
reviewed wheel; this is not an OS sandbox for arbitrary hostile native code or
concurrent same-account modification. Windows fixtures exercise real controlled
interpreters and the exact wheel's source; they do not execute/certify its
AArch64 native component. POSIX descriptor behavior, CPython 3.11.2/AArch64 SOABI,
actual initial paths/configuration and native loading require a separately
authorized architecture-matched **non-lifecycle** validation checkpoint before
production Action E authorization. No PI3/PI5 access occurs in this implementation.

The accepted producer remains `6c431494c88688fef9a2fec7c7e81de0f503bdc2`.
D/common/lock, the handoff compatibility helper, and F/G source remain unchanged;
exact producer/current critical-blob compatibility remains required. The future
published corrective implementation/closure commit is the consumer, not
`5c9afc5cb921681121fbbb71d64d6fe1cf29e242`. Historical PI3 compatibility closure
remains historical evidence and does not validate this correction.

Lifecycle: replacement B PASS/CLOSED; C PASS exactly once; D-PREP PASS/CLOSED;
D PASS/CLOSED; E NOT STARTED; F NOT STARTED; G NOT STARTED; rollback NOT PERFORMED.
No production synchronization or lifecycle action is performed or authorized here.
Next checkpoint: `ACTION_E_NATIVE_VALIDATION_PREPARATION_READY_FOR_SEPARATE_AUTHORIZATION`.

## Historical PI3 D-to-E read-only compatibility validation — PASS / CLOSED

The published implementation consumer was synchronized and validated on PI3
in a separately governed read-only checkpoint. This documentation release
changes the next consumer candidate and grants no runtime or lifecycle authority.

Operator-supplied evidence reports host `nutandpihole`, user `jazofv1`, clean
`main`, HEAD/local `origin/main` both `8e4880c7fa5fbea4583eea0d4485a65493fb6b36`,
and ahead/behind `0 0` before and after validation. Source synchronization PASSed;
producer `6c431494c88688fef9a2fec7c7e81de0f503bdc2` and reviewed consumer
`8e4880c7fa5fbea4583eea0d4485a65493fb6b36` were actual commit objects, producer
ancestry PASSed, and the real replacement-protected compatibility helper PASSed.

Reviewed producer/current critical blobs were identical:

| Contract file | Producer and reviewed consumer blob |
|---|---|
| `tools/hioc-pe4-runtime-construct.py` | `6dc8fe1c058f8b1de6f16d7ea7c88c133e1128b7` |
| `tools/hioc_pe4_runtime_common.py` | `4d9289d174e8647bbc67b1a6b83868bda699bad7` |
| `requirements-pe4.lock` | `8f2652298f12734b0e4f43341a48ed5702fe696e` |

Current committed/worktree E blob was `402664a4533ab98c27358d3b48d37b69e72bf1de`;
compatibility-helper blob was `807599005ad5ff0adc9335daf04b2598a3335dd6`.
All five reviewed blobs and source remained unchanged. Frozen D SHA-256 remained
`e979cc6049f8912c23e880f121fd2988d0354623c4f2a7d27eafb310e4b0c213`.

Strict producer-bound D eligibility and runtime hierarchy/construction validation
PASSed for construction
`/home/jazofv1/hioc/runtime/pe4/environments/.construct-cpython311-websockets16.1.1-lock-v1-mwJVPNqh`,
observed identity `45826:823199:1000:1000:0750`. Marker producer remained
`6c431494c88688fef9a2fec7c7e81de0f503bdc2`; accepted evidence remained
`/tmp/hioc-pe4-runtime-construct-LW9Dvay6`, SHA-256
`a31f1e841f437dece13d327f14a99a93d5f96a8e258b9786cc6e49358821350d`.
Evidence review confirmed environment `cpython311-websockets16.1.1-lock-v1`, wheel
SHA-256 `86d7f0f8bdb25d2c632b72527325e4776430fd5bc61b9118de4e2b8ddb5f5b01`,
lock SHA-256 `19433d53e3015157207d1af4ef07930db6f0e0d525597485384b3b7d42628e96`,
and persisted `eligibility_state="AWAITING_CONFIRMATION"`. Marker/evidence remained
unchanged; no rewrite, migration, recreation or Action D rerun occurred.

```text
PI3_SOURCE_SYNCHRONIZATION=PASS
CURRENT_CONSUMER_SOURCE=PASS
PRODUCER_CONSUMER_COMPATIBILITY=PASS
PRODUCER_ANCESTRY=PASS
STRICT_ACTION_D_ELIGIBILITY=PASS
RUNTIME_HIERARCHY_CONSTRUCTION=PASS
ACCEPTED_D_EVIDENCE=PASS
D_MARKER_AND_EVIDENCE_UNCHANGED=TRUE
ACTION_E_EVIDENCE_BEFORE=[]
ACTION_E_EVIDENCE_AFTER=[]
NO_NEW_ACTION_E_EVIDENCE=TRUE
CURRENT_SOURCE_UNCHANGED=TRUE
D_TO_E_READ_ONLY_COMPATIBILITY=PASS
ACTION_E_EXECUTED=FALSE
ACTION_F_EXECUTED=FALSE
ACTION_G_EXECUTED=FALSE
NO_LIFECYCLE_ACTION_EXECUTED=TRUE
STOP_REQUIRED=TRUE
```

No ERROR_CODE or FAILURE_STAGE was emitted. No Action E main invocation,
distribution validation or websockets capability probing occurred. This Windows
documentation closure accessed neither PI3 nor PI5 and executed no lifecycle
action, synchronization, or combined suite.

Replacement B remains PASS/CLOSED, Action C PASS exactly once, D-PREP PASS/CLOSED,
and Action D PASS/CLOSED. Actions E/F/G remain **NOT STARTED** and separately
unauthorized. Rollback remains NOT PERFORMED.

The resulting documentation-only closure commit becomes the next current
consumer/source candidate for Action E. `8e4880c7fa5fbea4583eea0d4485a65493fb6b36`
is the reviewed historical consumer, not a permanent E consumer pin. The immutable
producer remains `6c431494c88688fef9a2fec7c7e81de0f503bdc2`. Before eventual E
execution, current-source integrity and the same compatibility policy must be
validated again against the new consumer commit. This prior PASS does not replace
that evaluation or separate Action E execution authorization.

Next checkpoint: `ACTION_E_REPREPARATION_READY_FOR_SEPARATE_AUTHORIZATION`.

## Action E producer/current governance release prerequisite

The published correction requires E's current-consumer `--governance-commit` and
immutable D producer `--action-d-governance-commit` as distinct mandatory inputs.
Release review must verify actual commit objects without replacement substitution,
complete history, producer equality/ancestry and identical committed D/common/lock
blobs. The current source checkout must also satisfy clean main/HEAD/origin identity,
zero ahead/behind, no active Git operation and normalized identities for E, the
compatibility helper and all three upstream critical files.

The common strict producer-bound eligibility/evidence contract, runtime/capability
checks and E success JSON remain unchanged. Local Windows tests passed; publication
is a governance prerequisite, not production synchronization, evidence migration,
D rerun, or E execution. Accepted D evidence/marker remain immutable. D/common/lock
and F/G source remain unchanged. Action E has not executed and remains **NOT STARTED**;
F/G remain NOT STARTED and unauthorized. No PI3/PI5 access, lifecycle execution or
rollback occurred in this checkpoint. The later separately authorized
synchronization and read-only compatibility validation PASSed as recorded above;
E execution remains unauthorized.

The original implementation synchronization/read-only validation boundary
is now PASS/CLOSED as recorded above. Next checkpoint:
`ACTION_E_REPREPARATION_READY_FOR_SEPARATE_AUTHORIZATION`.

Action B release identity includes three independent, read-only Windows SSH ACL
contracts: the shared `.ssh` compatibility layout, the protected `known_hosts`
trust-file layout, and the strict protected dedicated-key layout. Publication
does not normalize workstation ACLs or authorize Action B execution.

The Action B staging-identity/known-host/ACL correction must be published before
any new execution review. Publication alone does not authorize Action B. A
separate read-only PI3 preflight must then verify Python, filesystem flags,
file/directory fsync, libc `renameat2(RENAME_NOREPLACE)`, account identity,
`/tmp`, and required fixed utilities.

The PE-4 identity evidence reconciliation correction is repository-only.
Publication is not complete unless the exact final result confirms and the
prepared `.result.tmp` is proven absent without following reparse targets.
Publishing this source correction does not provision a key or execute Action B.

The PE-4 Windows identity correction is repository governance only. It makes
final collision checks non-following, uses Windows atomic no-replace key and
evidence publication, and locks provisioning and Action B to the shared
`.ssh/id_ed25519` identity. Release does not generate or migrate a key, modify
`.ssh`, contact PI3, authorize a public key, or execute Action B.

The PE-4 client follows the established PI3 source/runtime boundary:
`/home/jazofv1/hioc-release-source` is authoritative Git source and
`/home/jazofv1/hioc` is the non-Git deployed runtime. PI5 HA remains a remote
API source and receives no HIOC client or dependency. A future credential-free
preflight must prove PI3 Python/dependency and installation facts before a
release-managed, preferably isolated dependency design can be approved. This
checkpoint deploys and installs nothing.

The repository-controlled PE-4.0B.2a client is implemented and tested offline,
but is unstaged, uncommitted, unreleased, undeployed, and unexecuted at this
checkpoint. Its next boundary is exact diff/identity commit review. Only after
commit and push may a separate checkpoint freeze the runtime invocation and
installed WebSocket dependency. It cannot release an adapter,
install a client dependency, execute registry discovery, or continue to
PE-4.0B.2b automatically.
Official API research froze REST-root then WebSocket authentication. The new
client source implements that contract, while publication and production
execution remain separate checkpoints.

The PE-4.0A access/privacy contract is documentation and focused governance
tests only. It adds no release artifact, credential, discovery executable,
adapter, deployment, or production step. PE-4.0B preparation and any later
implementation have separate review, commit, release, and authorization gates.

Action 10 has no release or target-host step. Its original transport-cleanup
operation is superseded because staging is absent and the installed immutable
dataset plus active configuration are authoritative. Administrative disposition
`NOOP_ALREADY_ABSENT` requires only governed repository closure; it must not
recreate, retransmit, verify, or delete staging and must not consume or alter
Action 8/9 evidence. The repository-only completion record is now present:
Action 10, Actions 1–10, and PE-3 are complete with no release or production
action and no Action 10 Evidence Report.

The corrected Action 9 validation completed successfully outside the release
path, publishing only private evidence at
`/tmp/hioc-pe3-action9-Bb6vGrmm`. It performed no release, runtime deployment,
production mutation, or rollback. Action 9 and its Evidence Report remain the
final PE-3 production validation and evidence. Transport staging remains absent
and retransmission remains unnecessary.

The corrected Action 9 tool remains outside the release path. Its historical
first attempt is recorded as attempted but incomplete after a performance-only failure, with
no evidence directory or production mutation and rollback FALSE. Result and
protected schemas passed; `12.467231` seconds and `146744` KiB total peak child
RSS are observations under an unvalidated baseline. Historical four-second and
incremental-RSS 48-MiB targets are not current hard gates. After commit/push, a
separate release-source synchronization is required for the changed tool; no
runtime deployment, upgrade, installer, generator, or Action 10 step is implied.

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
# PE-4.0B.2a isolated runtime release boundary

The lock file and dependency contract are governed release content; the wheel
is a digest-verified off-device artifact and is not stored in Git. Versioned
virtual-environment bytes are reproducible release products, not persistent
state. A future release correction must govern creation, atomic active-pointer
switching, prior-environment rollback retention, artifact-cache preservation,
and backup exclusions before deployment. Nothing is installed or released by
this checkpoint.

The reviewed lifecycle correction now externalizes `runtime/pe4` from ordinary
release backup, deployment, and rollback. Its recovery basis is the Git lock
and tooling, exact frozen identity, durable workstation artifact cache, and
retained prior immutable environment. PE-4 publication and pointer rollback are
performed only by the dedicated tools in `PE4_ISOLATED_RUNTIME_LIFECYCLE.md`.

Action A's durable cache is production-proven. Action B transfers only the
identity-checked wheel and lock into invocation-owned PI3 staging; it does not
modify Git source or the non-Git runtime. Partial-transfer evidence and the
preserved directory are review inputs, not release deployment.

Action B transport isolation is part of release identity: ambient SSH config,
agents, proxies, jump hosts, canonicalization, alternate ports, and alternate
known-host/identity files are excluded. Its remote result becomes governed
evidence only after exact digest and durability confirmation following rename.

The published Action B executable identities are refreshed only after a
read-only Microsoft-signature, System32-path, ownership, ACL, non-reparse, and
version review. The current `OpenSSH_9.5p2` hashes supersede stale anchors;
servicing causality remains unproven. This release-record correction does not
authorize replacement transport or Action D.
## PE-4 Action B identity release boundary

Publishing the provisioning implementation does not provision an identity.
Provisioning execution, PI3 authorization of the reviewed public fingerprint,
and Action B artifact transfer are independently authorized checkpoints. The
private/public key pair and Windows evidence are operator-local protected state,
not release content, and must never be committed, packaged, transferred by the
release process, or recreated during rollback.

The initial provisioning implementation is not executable release authority:
its evidence-ordering and invocation-child ownership defect required correction.
Only a committed and published tool identity with final-cleanup-before-evidence
and exact post-rename confirmation may proceed to a fresh preparation checkpoint.

The first authorized run of that published identity failed safely before key
publication because its parser rejected the CRLF terminator produced by pinned
Windows OpenSSH. A releasable correction accepts exactly one native LF or CRLF
record terminator, retains every other identity gate, and carries a realistic
Windows-output regression for both generated and derived records. It must not
append a synthetic comment to the already-commented derived record. Publication
alone does not authorize a retry.

## PE-4 Action B no-replace release boundary

Action B publication is complete only through Linux
`renameat2(RENAME_NOREPLACE)`, exact final identity/durability confirmation,
and proof that the invocation source was consumed. This applies independently
to the wheel, lock, and result-last evidence. Existing or raced destination
objects remain untouched; exclusive evidence creation cannot follow a link;
and a result publication attempt never falls through to a second,
contradictory result. This repository correction does not execute Action B.

## PE-4 Action B ingress identity boundary

Release identity now includes the reviewed Windows operator/profile, system
`ssh.exe` digest, pinned key generator, Ed25519 pair/fingerprint/comment, and
numeric PI3 host-key fingerprint. Direct SCP partial ingress is excluded.
Bounded SSH stdin feeds an exclusive, no-follow, directory-fd-relative sink;
the existing no-replace final publication remains unchanged. Persistent result
evidence records `AWAITING_CONFIRMATION`, while terminal state distinguishes
confirmed, definitely unpublished, and indeterminate publication. Publication
of this source does not authorize Action B execution.

The Action D correction is source governance only. Publication must be followed
by PI3 release-source synchronization and a fresh readiness review before any
construction authorization. The corrected release source binds verified Action
B inputs into a private snapshot, constructs through retained directory
descriptors, isolates pip offline, and publishes confirmed evidence plus an
Action E eligibility marker. A failed or ambiguous evidence handoff cannot be
promoted merely because a construction tree exists. Action D was blocked at
that correction checkpoint; its current third-execution closure is PASS / CLOSED.
Actions E-G remain not started.
## PE-4 replacement Action B correction release boundary

This release corrects only the shared temporary-directory compatibility and the
future Windows operator transaction boundary. CPython tempfile suffixes may
contain `_`; all Action B/Action D consumers now use the shared, anchored
eight-character `[A-Za-z0-9_]` contract. The correction does not adopt the
failed empty staging directory, recreate historical staging, transfer content,
or run Action D.

The version-controlled replacement wrapper is release-governed source, not a
general PowerShell snippet. It parses Git's two native divergence fields rather
than formatting assumptions, permits precisely one Action B process launch,
preserves stdout/stderr, validates the current PASS contract, and always stops.
New execution requires a separately published/synchronized/readiness-reviewed
authorization; the old authorization is consumed.

The wrapper release at `1bf339d` was invoked once and failed before Action B
launch because Windows PowerShell stripped embedded quotes from local Python
preflight source. This release replaces all wrapper Python native invocations
with `ProcessStartInfo.ArgumentList` transport and regression-tests that exact
boundary. It makes wrapper entry, precheck state, launch state, and transaction
state distinct. No Action B, SSH, PI3 staging, or transfer occurred in the
historical precheck-only event. Release execution is pinned to managed
PowerShell Core; legacy Windows PowerShell 5.1 fails closed because it lacks
the required `ArgumentList` API.
## Action D diagnostic retention

Private Action D failure evidence is not a release artifact. It preserves bounded
sanitized diagnostic context only and cannot be interpreted as a successful runtime.

## D-PREP hierarchy preparation

The PE-4 runtime hierarchy is release-managed externalized content. Its governed
creation is D-PREP, not ordinary upgrade or rollback; Action D independently
validates it and no D-PREP result chains into construction or publication.

## Current transfer-evidence recovery status

Operator-supplied recovery readiness observations remain historical audit facts:

| Historical evidence/staging path | Observed state |
| --- | --- |
| `/tmp/hioc-pe4-artifact-transfer-_w3qekbv` | ABSENT |
| `/tmp/hioc-pe4-artifact-transfer-g_jrlqkl` | ABSENT |
| `/tmp/hioc-pe4-runtime-construct-failure-aih8dlDw` | ABSENT |
| `/tmp/hioc-pe4-runtime-hierarchy-prepare-8OfcmWdP` | PRESENT at readiness observation |

The three absent objects were historically created and used as governed
evidence/staging. Their disappearance cause is UNKNOWN. Historical Action A PASS
and Action B PASS remain valid; `_w3qekbv` remains historically accepted but
currently unavailable and cannot supply Action D input. It is not renamed or
replaced in the audit history. Manual reconstruction or substitution is prohibited.
The D-PREP evidence presence observation is not an indefinite retention guarantee.

### Successful fresh replacement Action B — PASS / CLOSED

Operator evidence establishes one separately authorized new replacement B
transaction at governance commit `8d5dae032267725ea688e72925676306312e745c`.
This was not a rerun in place or reuse of historical staging. Wrapper process RC
was `0`, terminal evidence was CONFIRMED, and independent read-only review PASS.
This closure designates `/tmp/hioc-pe4-artifact-transfer-l3t4crcg` as the accepted
replacement transfer directory for the next separately prepared Action D checkpoint.
Fresh input was available at the successful independent observation; continued
availability must be revalidated during preparation. No path is hard-coded in source.

```text
REMOTE_STAGING_CREATED=TRUE
WHEEL_TRANSFERRED=TRUE
LOCK_TRANSFERRED=TRUE
REMOTE_ARTIFACT_VERIFIED=TRUE
REMOTE_LOCK_VERIFIED=TRUE
EVIDENCE_STATE=CONFIRMED
ACTION_B=COMPLETE
RESULT=PASS
ERROR_CODE=NONE
FAILURE_STAGE=COMPLETE
ROLLBACK_RECOMMENDED=FALSE
TRANSFER_DIRECTORY=/tmp/hioc-pe4-artifact-transfer-l3t4crcg
REPLACEMENT_WRAPPER=INVOKED
PRECHECKS=PASS
ACTION_B_LAUNCH=STARTED
ACTION_B_TRANSACTION=COMPLETE
ACTION_B_REPLACEMENT=COMPLETE
STAGING_PRESERVED=TRUE
WRAPPER_PROCESS_RC=0
INDEPENDENT_ACTION_B_INPUT_REVIEW=PASS
WINDOWS_REPOSITORY_SOURCE_UNCHANGED=TRUE
ACTION_C_RERUN=FALSE
D_PREP_RERUN=FALSE
ACTION_D_EXECUTED=FALSE
EVIDENCE_REVIEW_REQUIRED=TRUE
STOP_REQUIRED=TRUE
```

The tool and wrapper each emitted `RESULT=PASS` and the same transfer path.
Staging was preserved at the observation. Do not modify or delete fresh staging;
this documentation authorizes no PI3 access, cleanup, retry, or later execution.

Action C remains PASS exactly once, not invalidated and not rerun. No new route
proof is required or authorized. D-PREP native validation and production execution
remain PASS / CLOSED, not invalidated and not rerun; the compliant hierarchy remains
valid. Earlier PI3 read-only readiness reconfirmed `runtime`, `runtime/pe4`, and
`runtime/pe4/environments` under `/home/jazofv1/hioc`, each mode `0750`, device
`45826`. PI3 read-only readiness and Windows replacement-B readiness both PASS.

The prior recovery Action D wrapper stopped during pre-execution B input validation
before `PRE_EXECUTION_GUARDS=PASS`: no Action D process or new D evidence resulted.
At the replacement-B closure, `ACTION_D=FAILED_TWICE_NOT_COMPLETE` and
`ACTION_D_RETRIED=FALSE` after D-PREP were the historical status: no third execution
had then occurred. Replacement B restored input availability, not execution
authority. A subsequent separate authorization led to the successful third actual
Action D execution recorded in the current closure below. Actions E/F/G,
authenticated PE-4.0B.2a proof, PE-4.0B.2b and PE-4.0C remain NOT_STARTED;
rollback remains NOT_PERFORMED. `ROUTE_PROOF_ORDER=BEFORE_DEPENDENCY_DEPLOYMENT`
is unchanged.

Replacement B is not idempotent; each invocation allocates a fresh random directory.
The successful transaction's authorization is consumed and grants no repeat.
The prior ephemeral `/tmp` evidence-loss finding remains historical context;
durable retention requires a separate future design/governance decision. No retention
redesign is included here.

Exact staging file identities and the persisted result contract are recorded
in HIOC_MASTER_PLAN.md, Accepted replacement staging — independent observation.

## Current Action D closure — third actual execution PASS / CLOSED

Operator-supplied evidence establishes that the separately authorized third
actual Action D invocation PASSed at governance commit
`6c431494c88688fef9a2fec7c7e81de0f503bdc2`. Pre-execution guards PASSed;
Action D process RC was `0` and independent post-execution review PASSed.

Historical chronology remains: first Action D failure; second Action D failure
(`RUNTIME_PARENT_VALIDATION / OPEN_RUNTIME_PARENT / FILE_NOT_FOUND / errno 2`);
later recovery wrapper stop before launch because historical B input was absent;
then this successful third actual execution. The recovery stop was not an Action D
execution and did not increment the invocation count. D-PREP corrected the missing
hierarchy prerequisite. Earlier failed-twice statuses below are historical only.

Accepted construction, created, confirmed, retained and independently validated:

`/home/jazofv1/hioc/runtime/pe4/environments/.construct-cpython311-websockets16.1.1-lock-v1-mwJVPNqh`

Confirmed successful evidence directory observed at closure:

`/tmp/hioc-pe4-runtime-construct-LW9Dvay6`

Evidence SHA-256:
`a31f1e841f437dece13d327f14a99a93d5f96a8e258b9786cc6e49358821350d`.
These are operator observations, not indefinite filesystem-retention guarantees.
No construction, staging, or evidence is renamed, moved, published, activated,
rewritten, or cleaned by this documentation checkpoint.

```text
ACTION_D=COMPLETE_PASS
PRE_EXECUTION_GUARDS=PASS
CONSTRUCTION_CREATED=TRUE
CONSTRUCTION_CONFIRMED=TRUE
CONSTRUCTION_RETAINED=TRUE
INPUT_SNAPSHOT_CREATED=TRUE
INPUT_SNAPSHOT_RETAINED=FALSE
EVIDENCE_STATE=CONFIRMED
ACTION_D_ELIGIBILITY=CONFIRMED
CLEANUP_STATE=COMPLETE
RESULT=PASS
ERROR_CODE=NONE
FAILURE_STAGE=COMPLETE
ROLLBACK_RECOMMENDED=FALSE
ACTION_D_PROCESS_RC=0
INDEPENDENT_ACTION_D_REVIEW=PASS
REPLACEMENT_ACTION_B_STAGING_UNCHANGED=TRUE
SOURCE_REPOSITORY_UNCHANGED=TRUE
D_PREP_HIERARCHY_COMPLIANT=TRUE
NEW_INPUT_SNAPSHOT_ENTRIES_RETAINED=FALSE
EVIDENCE_REVIEW_REQUIRED=TRUE
ACTION_D_LAUNCHED=TRUE
ACTION_C_RERUN=FALSE
D_PREP_RERUN=FALSE
ACTION_E_EXECUTED=FALSE
STOP_REQUIRED=TRUE
```

Persisted success evidence intentionally retains
`eligibility_state="AWAITING_CONFIRMATION"`; terminal
`ACTION_D_ELIGIBILITY=CONFIRMED` follows eligibility-marker publication.
The confirmed handoff binds governance commit, construction path, environment
identity, wheel/lock hashes, evidence path and evidence SHA-256. Evidence is not
rewritten to CONFIRMED by this closure.

Independent runtime validation PASSed: CPython `3.11.2`, SOABI
`cpython-311-aarch64-linux-gnu`, base executable `/usr/bin/python3.11`, base
prefix `/usr`, environment prefix equal to the accepted construction path,
user site disabled (`true`), and site-packages isolated under that construction.
Observed installed distributions were exactly `pip==23.0.1`,
`setuptools==66.1.1`, and `websockets==16.1.1`. Pip/setuptools versions are
observations, not new immutable requirements; existing policy remains one pip,
optional single setuptools, frozen websockets `16.1.1`, and no other distributions.

Action A and historical Action B remain historical PASS; unavailable historical
staging remains audit history. Replacement Action B remains PASS / CLOSED with
accepted input `/tmp/hioc-pe4-artifact-transfer-l3t4crcg`, unchanged during D.
Action C remains PASS exactly once, not invalidated or rerun. D-PREP native and
production remain PASS / CLOSED, not rerun, and hierarchy compliant. No new
input-snapshot namespace entries remained. No combined suite ran on PI3.
Action E is NOT_STARTED and separately unauthorized; Actions F/G and later
PE-4 actions remain NOT_STARTED. Rollback remains NOT_PERFORMED.

Action D remains complete. The subsequent repository correction separates D
producer provenance from E current source. The separately authorized PI3
synchronization and read-only D-to-E compatibility validation subsequently
PASSed. The next boundary is separately authorized Action E re-preparation
against the resulting documentation closure consumer commit; the accepted D
producer remains immutable.
This closure prepares and authorizes no Action E execution or later lifecycle
action. It grants no repeat Action D invocation or cleanup authority.

## Historical D-PREP reconciliation status

The following records the D-PREP closure checkpoint before the third Action D
execution. Its failed-twice/no-retry assertions are historical; current Action D
is PASS / CLOSED as recorded above.


Operator-supplied evidence establishes that corrected source was published and
synchronized to PI3 at `c5181a0d65da294e5db2dbd6795f20889b972a22` before native
validation. PI3 native D-PREP revalidation is PASS and CLOSED: 115 run / 115 pass /
0 skip / 0 fail / 0 error, including all seven POSIX-specific tests. Pre- and
post-test source identity and frozen Action D SHA-256 were preserved. The prior
Linux failures are closed as test-harness portability/isolation defects.

```text
D_PREP=PRODUCTION_EXECUTED_PASS
PI3_NATIVE_D_PREP_REVALIDATION=PASS
D_PREP_EXECUTED=TRUE
ACTION_D=FAILED_TWICE_NOT_COMPLETE
ACTION_D_RETRIED=FALSE
PI3_COMBINED_SUITE_EXECUTED=FALSE
ACTION_E=NOT_STARTED
ACTION_F=NOT_STARTED
ACTION_G=NOT_STARTED
PE4_0B2A=NOT_STARTED
PE4_0B2B=NOT_STARTED
PE4_0C=NOT_STARTED
ROLLBACK=NOT_PERFORMED
```

Operator-supplied production evidence now closes D-PREP execution as PASS at
`5783951fdd33e0bb476c0fa53022633adddf1b8c`. All three previously absent hierarchy
components were CREATED_CONFIRMED, owned by `jazofv1:jazofv1`, mode `0750`, device
`45826`. Evidence was CONFIRMED, process RC was `0`, post-validation passed, and
`ROLLBACK_RECOMMENDED=FALSE`. The missing-hierarchy prerequisite is corrected;
this is not Action D success. Action D remains failed twice, incomplete, and not
retried. The combined
D-PREP/lifecycle suite has NOT EXECUTED on PI3; its earlier Windows validation is
historical and separate. Action A and corrected B remain COMPLETE / PASS; Action C
remains COMPLETE / PASS exactly once and must not be rerun absent an authorized
finding of invalidation. Later lifecycle actions remain NOT STARTED and no rollback
occurred. Phase 7A remains active; PE-4 is incomplete and Active Discovery postponed.

Action D retry requires separate operator authorization.
This documentation closure grants no execution authority. No production state or
preserved evidence was changed by this checkpoint. Earlier checkpoint narratives
retain historical status; HIOC_MASTER_PLAN.md remains the authoritative source.

### Final hierarchy and evidence contract

D-PREP owns only `/home/jazofv1/hioc/runtime`,
`/home/jazofv1/hioc/runtime/pe4`, and
`/home/jazofv1/hioc/runtime/pe4/environments`: directories, no symlinks,
`jazofv1:jazofv1`, exact mode `0750`. `/home`, `/home/jazofv1`, and
`/home/jazofv1/hioc` are validate-only anchors. Existing noncompliance is rejected,
not normalized. hioc -> runtime permits cross-device operation with
`require_same_device=False`; runtime -> pe4 and pe4 -> environments require the
same device. States are `NOT_REACHED`, `PREEXISTING_COMPLIANT`, `CREATED_CONFIRMED`,
and `CREATION_OCCURRED_BUT_FINAL_STATE_UNCONFIRMED`. Valid partial hierarchy is
durable and resumable; no recursive rollback or automatic deletion of valid
created hierarchy occurs. Governed failures retain `ROLLBACK_RECOMMENDED=FALSE`.

Private evidence is under `/tmp/hioc-pe4-runtime-hierarchy-prepare-XXXXXXXX`,
directory mode `0700`, `result.json` mode `0600`. D-PREP `EVIDENCE_MAX_BYTES=4096`
includes the final newline; its publisher explicitly receives 4096, and bounded
reread detects overflow under that limit. The shared publisher default remains
65536 bytes, not D-PREP's limit. Publication uses an atomic no-replace final link,
exact payload verification, final directory revalidation, and a digest calculated
only after confirmation steps. States are `NOT_CREATED`, `CREATED`, `UNCONFIRMED`,
and `CONFIRMED`: pre-evidence validation failures remain NOT_CREATED; evidence
acquisition/creation/publication failures become UNCONFIRMED. Publication success
sets CONFIRMED before final hierarchy validation. Unconfirmed evidence failures
withhold `EVIDENCE_DIR`; a later governed final-validation failure retains CONFIRMED
and may disclose the confirmed path despite overall FAIL. Unexpected evidence
failures disclose no unconfirmed path. Confirmation is distinct from overall success.

Policy C: `create_owned_child()` performs no pathname deletion during exceptional
cleanup after successful mkdir: no rmdir, unlink, or alternate removal. It captures
and clears local fd ownership, closes once if acquired, suppresses cleanup-close
OSError, and bare re-raises the primary. Thus exceptional cleanup cannot delete an
unrelated current basename occupant through pathname removal. Creation/acquisition
is not race-free or atomic: namespace may change, original-object fate after
substitution may be unknown, failures may leave private/remnant directories, and
repeated failures may accumulate remnants. No automatic remnant cleanup exists.
These accepted nonblocking limits are distinct from hierarchy rollback; original
object persistence is not guaranteed.

Temp-root policy uses pre-open lstat, rejects observed nondirectories/symlinks,
requires POSIX primitives, opens with directory/no-follow flags, and validates
post-open directory type/token and UID/GID/mode against the observed policy, with
retained descriptor ownership. It imposes no fixed /tmp UID/GID/mode, sticky-bit
policy, or observed/opened dev/inode continuity requirement.

### Historical production evidence and current availability

Current operator-observed availability is recorded in the transfer-evidence
recovery status above. Historical paths remain audit facts; no continued
presence, reconstruction, substitution, or cleanup authority is implied.

Final validation counts, publisher fault coverage, and umask disposition D are
recorded in HIOC_MASTER_PLAN.md; these do not establish production execution.
