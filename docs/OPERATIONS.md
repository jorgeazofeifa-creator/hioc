## Deployment runtime probe resolved-prefix correction — 2026-10-06

Deployment Runtime Probe Correction PASS/CLOSED. The following chronology is
**OPERATOR_SUPPLIED_PRODUCTION_EVIDENCE**, provenance OPERATOR_SUPPLIED; Codex did not
access PI3 or collect the production observations:

1. First Deployment Execution attempt at 2ef66a2 failed RUNTIME_DRIFT, with durable
   transaction and production deployment NOT_STARTED.
2. Accepted-runtime customization correction at
   `e4d5a19afecccb1584708e3da57ba3c0c4258523` closed the exact reviewed customization policy.
3. Second Deployment Execution attempt at e4d5a19 again failed RUNTIME_DRIFT, with
   durable transaction and production deployment NOT_STARTED; no production mutation,
   adapter execution, HA connection/authentication, scheduling or rollback occurred.
4. Read-only diagnostic passed bootstrap policy extraction and exact customization
   observation, then isolated child NotADirectoryError at active: raw sys.prefix retained
   the governed `/home/jazofv1/hioc/runtime/pe4/active` symlink.
5. The operator's resolved-prefix diagnostic passed customization_validation, RESULT
   and RESOLVED_PREFIX_VALIDATION using the accepted environment's real site-packages.
   It accessed no credential, attempted no HA network and performed no production mutation.
6. The production adapter is unaffected: Runtime.runtime() already derives site from
   the fixed accepted ENVIRONMENT. Its module/entrypoint source bytes remain unchanged.
7. The deployment helper now resolves sys.prefix before site-packages observation;
   runtime_identity() still requires the exact accepted environment. The separately
   governed active link must resolve there before the child starts. No trust policy,
   O_NOFOLLOW traversal, filesystem observation helper or launch flag was weakened.

The child now uses:

```python
raw_prefix = Path(sys.prefix)
resolved_prefix = raw_prefix.resolve()
site = resolved_prefix / "lib/python3.11/site-packages"
```

Its reported prefix is `str(resolved_prefix)`, verified by the unchanged exact runtime
identity contract. Accepted resolved environment remains
`/home/jazofv1/hioc/runtime/pe4/environments/cpython311-websockets16.1.1-lock-v1`;
accepted adapter/runtime child launch remains `/home/jazofv1/hioc/runtime/pe4/active/bin/python -I -B`.
The existing stdlib deployment bootstrap uses -S independently of that accepted launch.
CUSTOMIZATION_POLICY, validate_runtime_customization, runtime_directory,
runtime_file_observation and runtime_customization_observation are unchanged because the
entire approved adapter module remains byte-for-byte identical. .pth, sitecustomize,
usercustomize, package, origin and sys.path gates retain the exact prior trust policy.

The [probe correction record](../governance/pe4/pe4-ha-association-deployment-runtime-probe-correction.json)
and [closed schema](../governance/pe4/pe4-ha-association-deployment-runtime-probe-correction.schema.json)
bind the new helper and unchanged adapter/entrypoint. Prior runtime correction records
and their helper identities remain immutable historical e4d5a19 evidence. Current deployment
preparation is rebound to the successor with immediate parent e4d5a19 and exact subject
`PE-4: fix deployment runtime prefix validation`; all main/origin/clean/0/0/no-operation
guards remain. This correction record is governance-only, not read by Runtime.contracts()
or installed in production. Eight additive targets, six runtime governance contracts and
six category-B dependencies remain unchanged. B policy remains
REQUIRED_EXISTING_EXACT_PRESERVE_ABSENT_OR_DIFFERENT_FAIL_CLOSED.

Validation: deployment focused 83 (including nine resolved-prefix/correction tests),
runtime customization 8, adapter 73, other regressions 275; total 439 run, 438 passed,
one existing release skip because rsync is unavailable on Windows. Behavioral tests execute
the generated child body with injected Linux paths/modules; the old construction reproduces
the safe failure, the resolved construction passes, and every tested runtime prerequisite
failure remains before credential validation, durable intent or production target mutation.
No accepted interpreter, actual adapter, credential, host or network is exercised by tests.

Adapter Implementation PASS/CLOSED, corrected before deployment; Runtime Validation
Correction PASS/CLOSED; Deployment Runtime Probe Correction PASS/CLOSED; Deployment
Preparation PASS/CLOSED, corrected and rebound. Deployment, Bounded Manual Production
Validation, Independent Production Acceptance and Scheduler Deployment NOT STARTED;
Public Projection DEFERRED; PE-4 NOT COMPLETE; Phase 7A ACTIVE; Rollback NOT PERFORMED.
Both failed attempts remain pre-intent failures. Next unchanged:
**PE-4 Home Assistant Association Adapter Deployment Execution**. The regenerated complete
operator block is FOR REVIEW ONLY and was not run. Stop after repository correction.

## Accepted runtime validation correction — 2026-10-06

Runtime Validation Correction PASS/CLOSED. **OPERATOR_SUPPLIED_PRODUCTION_EVIDENCE**:
the first Deployment Execution block was attempted once at
`2ef66a2d575c923c6939a4cd4d5bb2c8aab2f816` and failed safely with RUNTIME_DRIFT.
Deployment transaction and production deployment both remained NOT_STARTED. No production
adapter files, endpoint configuration, association state directory, credential/network
access, scheduler or rollback resulted. Codex did not collect the live evidence or access
PI3. The operator evidence established reviewed startup customization in the unchanged
accepted runtime. Blanket rejection implemented the frozen “no unreviewed customization”
policy too strictly; the correction permits only the exact reviewed identities below.

The [runtime correction record](../governance/pe4/pe4-ha-association-runtime-validation-correction.json)
and [closed schema](../governance/pe4/pe4-ha-association-runtime-validation-correction.schema.json)
bind current source identities and operator provenance. All prior commits and closed
historical records remain immutable. The accepted environment, active symlink, CPython
3.11.2/aarch64/SOABI, websockets 16.1.1 and its origin, sys.path bounds, package bounds and
launch **-I -B** remain unchanged. No runtime mutation occurred.

Exactly one site-packages .pth is required: distutils-precedence.pth, regular/no symlink,
jazofv1:jazofv1, 0640, one link, 151 bytes, SHA-256
`2638ce9e2500e572a5e0de7faed6661eb569d1b696fcba07b0dd223da5f5d224`.
Exact content includes the trailing space before LF. Setuptools 66.1.1 must record the
same basename, location, size and sha256 distribution hash
`JjjOniUA5XKl4N5_rtZmHrVp0baW_LoHsN0iPaX10iQ`. No other .pth is allowed.

sitecustomize must be loaded from `/usr/lib/python3.11/sitecustomize.py`, an exact root:root
symlink to `/etc/python3.11/sitecustomize.py`. The target must be regular root:root,
0644, one link, 155 bytes, exact reviewed content and SHA-256
`43d81125d92376b1a69d53a71126a041cc9a18d8080e92dea0a2ae23be138b1e`.
Debian package/version and successful dpkg verification are operator provenance only;
exact filesystem/module identities are the trust anchors. usercustomize remains prohibited,
loaded or present. Neither customization file is deleted or rewritten.

The adapter and deployment helper use the same literal policy and pure validator. The
helper checks the adapter source SHA-256 and extracts only the literal policy plus four
validation/observation definitions through AST; it does not import the adapter, execute
Runtime/run_cycle/main or invoke network operations. This avoids an extra runtime module
or deployment target. Native bounded no-follow reads pin directory and file bindings,
recheck metadata and symlink destination, and feed the pure validator. Deployment verifies
filesystem properties in its stdlib bootstrap before the accepted -I -B child probe,
which independently verifies the actually loaded module. The bootstrap's existing -S is
not an adapter launch change. Any mismatch fails adapter RUNTIME_VALIDATION_FAILED at
RUNTIME_VALIDATION before credential/network/publication; deployment RUNTIME_DRIFT before
intent or production mutation, with NOT_STARTED transaction/deployment evidence.

The correction record is governance-only: Runtime.contracts() still consumes exactly six
existing governance files. Eight additive A/C targets and six preserved B dependencies
remain unchanged in number. B policy remains
REQUIRED_EXISTING_EXACT_PRESERVE_ABSENT_OR_DIFFERENT_FAIL_CLOSED.

Validation: adapter 73; deployment preparation 74; correction 8; other regressions 275.
Total 430 run, 429 passed, one existing release skip because rsync is unavailable on Windows.
Important runtime logic uses deterministic fixtures and injected Linux metadata, with no
Windows skip. Syntax, import safety, canonical closed schemas, links, source identities,
privacy/prohibited-operation review and diff checks are repository-only.

Adapter Implementation PASS/CLOSED, corrected before deployment; Runtime Validation
Correction PASS/CLOSED; Deployment Preparation PASS/CLOSED, corrected before execution
and rebound to current source. Deployment, Bounded Manual Production Validation,
Independent Production Acceptance and Scheduler Deployment NOT STARTED; Public Projection
DEFERRED; PE-4 NOT COMPLETE; Phase 7A ACTIVE; Rollback NOT PERFORMED.
Next: **PE-4 Home Assistant Association Adapter Deployment Execution**. Stop after
repository correction; the regenerated deployment block remains FOR REVIEW ONLY.

## PE-4 deployment preparation pre-execution correction — 2026-10-06

Deployment Preparation PASS/CLOSED, corrected before execution. Historical preparation
`0040bdc79e66c10db4f180f952d04f97b1070065` is immutable. Current category B policy requires
existing exact dependencies and prohibits install/replace; A/C targets remain additive.
Durable secured journal authority now determines NOT_STARTED/PREPARED/COMMITTED, mapped
to production deployment NOT_STARTED/INCOMPLETE/PASS independently of overall acceptance.
A postcommit failure reports RESULT=FAIL, transaction COMMITTED, deployment PASS; no
automatic rollback. The full corrected operator block is FOR REVIEW ONLY.
72 focused tests plus 345 regressions: 417 run, 416 passed, one existing rsync skip.
No PI3/PI5/HA/real credential access, adapter/network execution, production mutation,
deployment, scheduler activation, MQTT, projection or rollback occurred.
Next remains **PE-4 Home Assistant Association Adapter Deployment Execution**.

[Current corrected preparation](PE4_HOME_ASSISTANT_ASSOCIATION_ADAPTER_DEPLOYMENT_PREPARATION.md) preserves historical evidence and the separate execution boundary.

## PE-4 Home Assistant Association Adapter Deployment Preparation — 2026-10-06

Deployment Preparation PASS/CLOSED, repository-only, from corrected implementation
`5e9d1ff3d74bb22c6cc0c4f726517c1d0b86d7f2`. The dedicated deployment preparation
freezes exact existing dependencies, additive runtime governance/code, endpoint config,
private state/lock prerequisites, local credential/runtime checks and durable deployment
intent. The proposed source-bound PI3 block is FOR REVIEW ONLY; no deployment authority
or production execution follows from repository preparation. No PI3/PI5/HA/credential
access, adapter execution, production mutation, scheduler, MQTT, projection or rollback.
Deployment, Manual Production Validation, Independent Acceptance and Scheduler NOT STARTED;
Public Projection DEFERRED; PE-4 NOT COMPLETE; Phase 7A ACTIVE; Rollback NOT PERFORMED.
Next: **PE-4 Home Assistant Association Adapter Deployment Execution**.

[Deployment preparation](PE4_HOME_ASSISTANT_ASSOCIATION_ADAPTER_DEPLOYMENT_PREPARATION.md) freezes the complete operator review block and rollback boundary.

# HIOC Operations

## PE-4 association adapter pre-deployment correction — 2026-10-06

Independent review of implementation `0bdb9340157daba4a6948251922d762cc4fc97ff`
identified two contract defects before deployment: incomplete canonical-envelope types
and state security checks capable of originating credential failure stages. Both are
corrected. Connection/identifier namespaces share the frozen 128-name bound, established
by the preparation's pinned historical 2b reducer; identifiers remain supporting-only.
[Correction details and current source bindings](PE4_HOME_ASSISTANT_ASSOCIATION_ADAPTER_IMPLEMENTATION.md) preserve the original
implementation record/schema and commit as historical evidence. 70 focused tests and
275 regression tests ran: 344 passed, one existing rsync-dependent skip (345 total).
Adapter Implementation PASS/CLOSED, corrected before deployment. Deployment and
Scheduler Deployment NOT STARTED; Public Projection DEFERRED; PE-4 NOT COMPLETE;
Phase 7A ACTIVE; Rollback NOT PERFORMED. No production deployment occurred before
correction. No real credential, PI3/PI5/HA access, adapter network, production mutation,
MQTT, public projection, scheduler activation or rollback occurred in this checkpoint.
Next: **PE-4 Home Assistant Association Adapter Deployment Preparation**, not begun.
Earlier entries below remain historical implementation evidence.

## PE-4 association adapter implementation — 2026-10-06

Repository-only Adapter Implementation PASS/CLOSED. [Implementation contract](PE4_HOME_ASSISTANT_ASSOCIATION_ADAPTER_IMPLEMENTATION.md)
binds the module, thin entrypoint and closed governance record to frozen 0C/0C.1,
state schema 1.1, and current credential closure. Exact-final-LF credential parsing
supersedes historical optional-LF preparation wording; historical records remain unchanged.
Synthetic adapter and required regression validation passed. Private transactional
publication/recovery and a full six-capability ha_core observation are implemented;
generic integration ingestion is PROHIBITED and Public Projection remains DEFERRED.
No real credential, production hosts, HA/network validation, deployment, scheduler,
MQTT association publication, production state mutation or rollback occurred.
Deployment and Scheduler Deployment NOT STARTED; PE-4 NOT COMPLETE; Phase 7A ACTIVE;
Rollback NOT PERFORMED. Next: **PE-4 Home Assistant Association Adapter Deployment Preparation**.
Older entries below retain their historical status and evidence.

## PE-4 runtime credential provisioning governance closure — 2026-10-06

Operator Credential Installation PASS/CLOSED; Independent Credential Validation
PASS/CLOSED; Governance Closure PASS/CLOSED; Runtime Credential Provisioning
PASS/CLOSED. The [credential closure contract](PE4_HOME_ASSISTANT_RUNTIME_CREDENTIAL_PROVISIONING.md) and dedicated canonical
closure record/schema bind OPERATOR_SUPPLIED PI3 evidence for source synchronization,
first INSTALL, independent root validation and separate actual jazofv1 readability.
Corrected commit d089be8 and tool identities are preserved. Root mode reported
runtime readability NOT_TESTED; the subsequent runtime identity reported TRUE.
Codex did not access or independently inspect PI3. No token or token hash is recorded.

Authentication remains DEFERRED_TO_ADAPTER_VALIDATION; local storage/readability
closure does not establish credential validity, revocation state, HA authentication,
WebSocket/registry access or adapter success. Next: **PE-4 Home Assistant Association Adapter Implementation**,
NOT STARTED. PE-4 NOT COMPLETE; Phase 7A ACTIVE; rollback NOT PERFORMED. No Codex
PI3/PI5/HA access, network validation, adapter implementation, deployment, MQTT
or production mutation occurred. No rotation was reported. Original preparation
and pre-execution correction history are immutable; older entries below describe
historical states and are superseded only for the current lifecycle by this closure.


## PE-4 canonical credential storage pre-execution correction — 2026-10-06

Independent review found that original preparation commit
`afa484620d24a1d6dec2a98e7c06e613f633bfb7` accepted persisted files without
final LF. That commit is preserved in immutable history. Both current tools now
require exactly one final LF, with 1–4096 printable ASCII token bytes and total
file size 2–4097 bytes. Missing LF is rejected without whitespace normalization;
invalid existing files fail before acquisition and remain untouched. Both validator
modes enforce the canonical representation. Source blob/SHA bindings and the closed
canonical preparation record/schema are regenerated by the new corrective commit.

Preparation PASS/CLOSED, corrected before execution; parent PREPARED / NOT COMPLETE.
Operator Installation, Independent Validation, Governance Closure and Adapter
Implementation remain NOT STARTED. PE-4 NOT COMPLETE; Phase 7A ACTIVE; rollback
NOT PERFORMED. No credential, real token, PI3/PI5/HA access, network credential
validation, deployment, production mutation or MQTT occurred. The corrected future
PI3 block is FOR REVIEW ONLY, supersedes the original proposal, uses explicit
return-code handling and no set -e/-u/pipefail, shell exit/exec or logout. It stops
after provisioning, leaves the interactive shell available and does not run the
independent validator. Operator execution remains separately authorized.


## PE-4 separate operator credential installation preparation — 2026-10-06

Preparation PASS/CLOSED; parent Runtime Credential Provisioning PREPARED / NOT
COMPLETE. [Provisioning contract](PE4_HOME_ASSISTANT_RUNTIME_CREDENTIAL_PROVISIONING.md) and canonical closed governance bind
fixed-path operator-only provision and separate read-only validator tools. Hidden
root controlling-TTY input, strict ASCII/4096-byte policy, root:jazofv1 0750/0640,
effective primary plus supplemental group membership and fail-closed FD POSIX ACL
checks precede atomic no-backup installation/rotation. Existing drift is rejected.
Credential remains outside Git/releases and code rollback ownership.

Next: **PE-4 Home Assistant Runtime Credential Provisioning — Operator Installation**. Operator Installation,
Independent Validation and Governance Closure are NOT STARTED. The exact source-bound
manual installation block is supplied after the preparation commit is pushed; stop
after installation, leaving independent root and jazofv1 validation for the next
separately authorized action. No token, token hash, PI3/PI5/HA access, network
authentication, adapter implementation, deployment, production mutation, MQTT,
cron or rollback occurred. PE-4 NOT COMPLETE; Phase 7A ACTIVE. DATA_MODEL and
release/install scripts remain unchanged. Synthetic tests establish repository
preparation only; actual host membership/ACL/TTY/readability remain future proofs.


## PE-4 association adapter implementation preparation - 2026-10-06

[Implementation architecture](PE4_HOME_ASSISTANT_ASSOCIATION_ADAPTER_IMPLEMENTATION_PREPARATION.md) closes Preparation PASS/CLOSED using unchanged
0C and 0C.1 and schema 1.1. Dedicated post-identity module, accepted isolated runtime,
canonical inventory input, lock, recoverable private publication and sole full-map
HA compatibility ownership are frozen. No secure unattended HA credential mechanism
was found in repository source. Next is **PE-4 Home Assistant Runtime Credential
Provisioning**, NOT STARTED, outside Git/release ownership; adapter implementation
and deployment remain NOT STARTED. Public projection is separately deferred.
PE-4 NOT COMPLETE; Phase 7A ACTIVE; rollback NOT PERFORMED. This repository-only
preparation performs no runtime change, credential use, production access or action.

## PE-4.0C.1 association lifecycle clarification - 2026-10-06

[Additive lifecycle authority](PE4_HOME_ASSISTANT_ASSOCIATION_LIFECYCLE_CLARIFICATION.md) closes 0C.1 PASS/CLOSED.
Successful complete cycles keep only reconfirmed active associations and preserve
retired pairs in private bounded history; failed cycles preserve entire prior state.
Safe new HA-ID recreation requires the same HIOC identity and all uniqueness/
history checks. Schema 1.1 adds closed history; original 0C JSON/schema hashes
remain unchanged. Prior preparation correctly stopped with no changes; next is
implementation preparation, still NOT STARTED. Credential provisioning and writer
locking/durability remain separate preparation findings. No runtime implementation,
production access/action, state migration, secret, MQTT publication or rollback.
PE-4 NOT COMPLETE; Phase 7A ACTIVE; rollback NOT PERFORMED.

## PE-4.0C association contract freeze - 2026-10-06

PE-4.0C PASS/CLOSED after repository validation. The [frozen authority](PE4_HOME_ASSISTANT_ASSOCIATION_CONTRACT.md)
requires one valid globally unique HA MAC mapping to one existing HIOC canonical
MAC-backed identity; invalid, colliding, multiple/no-MAC or prior-conflict evidence
cannot automatically associate. Dedicated post-identity state is required; generic
integration ingestion, identity creation/mutation, liveness changes and Asset
overwrite are prohibited. Private/public projection boundaries are frozen.
2b remains PASS/CLOSED; PE-4 NOT COMPLETE; Phase 7A ACTIVE; rollback NOT PERFORMED.
Next: PE-4 Home Assistant Association Adapter Implementation Preparation,
NOT STARTED. No adapter or runtime procedures are introduced; no production access,
credentials, discovery, protected rerun, deployment or state mutation occurred.

## Corrected PE-4.0B.2b production proof and closure - 2026-10-06

Operator-supplied completed execution and independent read-only review establish
PE-4.0B.2b PASS/CLOSED. See the [canonical closure](../governance/pe4/pe4-0b2b-execution-closure.json)
and [current Master Plan](HIOC_MASTER_PLAN.md#implementation-status).
HA Core 2026.9.4 versus source baseline 2026.8.1 was COMPATIBLE_UPDATED:
required capabilities passed, failed capability NONE, no likely update
compatibility break, and central compatibility state agreed with the evidence.
This proves compatibility with the observed interface, not every future HA
release. PE-4.0C Association Contract Freeze is next and NOT STARTED.
No production access or execution occurs during this repository closure.

## Historical checkpoint notices

Earlier dated checkpoint status statements below preserve chronology and are
superseded by the current closure above. Operational procedures retain their
existing scope and authority; historical evidence remains unchanged.

## Compatibility resilience correction - 2026-10-06

The repository now governs capability-first external dependency contracts,
sanitized persistent compatibility status and retained platform diagnostics.
See [COMPATIBILITY_RESILIENCE.md](COMPATIBILITY_RESILIENCE.md) for the complete
42-family audit, exact-pin inventory, implementation boundaries and deferred
host proofs. HA Core 2026.8.1 remains source-review provenance; it is no longer
an exact live-version gate. All four required registry commands and unsafe-schema
failure gates remain. Isolated runtime, SSH and cryptographic identities stay exact.

The first authorized 2b attempt failed safely with UNSUPPORTED_HA_DEPLOYMENT at
HA_DEPLOYMENT_DISCOVERY because of the old version gate. Preserved user-supplied
evidence: `/tmp/hioc-pe4-ha-discovery-22be880b`; report SHA256
`efd3aa0cc2f5bc00a459a0c05055ac14e5a9a7ab6cc13aeeb34aa9aa616cb087`;
result SHA256 `1e11b6e512db860a8f9b2b6af1723c6aabafd75968d7fd643c891144a7a72195`.
No remote evidence was read or changed. The new correction record binds current
source; the original preparation record and earlier exact-version evidence remain
historical. This notice supersedes older current-status statements below.

D/E/F/G PASS/CLOSED; E handoff ACCEPTED; 2a PASS/CLOSED; first 2b ATTEMPTED /
NOT COMPLETE; corrected 2b NOT STARTED; 0C NOT STARTED; PE-4 NOT COMPLETE;
Phase 7A ACTIVE; rollback NOT PERFORMED. No PI3/PI5/HA access, credentials,
deployment or corrected execution occurs in this repository checkpoint.

Compatibility operator workflow: inspect local state/platform/compatibility.json or the retained platform/compatibility topic; read the named dependency, failed capability, previous/current version and recommended action. Review trust changes through the governed trust-anchor workflow. Do not refresh a pin, rerun an action or infer update causality from baseline alone. UNKNOWN requires fresh authorized proof.

## PE-4.0B.2b bounded registry/schema discovery prepared - 2026-10-06

Repository-only preparation follows the immutable 2a PASS/CLOSED closure at
`09814b8ab19553f21ff68c3a617a5164c47ef59f`. The standalone discovery client,
sanitized evidence schema, compact Core **2026.8.1** source contract, and synthetic
tests are bound by
[pe4-0b2b-discovery-preparation.json](../governance/pe4/pe4-0b2b-discovery-preparation.json).
[Preparation details](PE4_REGISTRY_DISCOVERY_PREPARATION.md) freeze exact read-only WebSocket commands
`config/device_registry/list`, `config/entity_registry/list`,
`config/area_registry/list`, and `config_entries/get`; authenticated-user permission
at this tag is a source-level classification, not a versionless API promise.
Documented REST remains insufficient for registry metadata. Unsupported interface
or schema fails closed, with no fallback command.

One authenticated connection, sequential correlated IDs 1–4, a shared 90-second
network deadline, zero retries, strict bounded JSON, immediate memory-only raw
reduction, no MAC hashing, structural evidence allowlists, and private durable
non-overwriting result-last publication define the prepared scope. No credential,
raw registry record, household identifier, or private response is repository evidence.
Unprovable physical/helper/integration/virtual/cloud classifications remain
explicitly unclaimed. The source closure, 2a client identity, historical F/G,
accepted E handoff, dependency lock, and runtime implementation remain unchanged.

No PI3/PI5/HA access, live discovery, real credential, deployment, 2a or D/E/F/G
rerun, rollback, PE-4.0C, or final association adapter occurred. Future execution
requires separate authorization and existing governed source/runtime pre-token
gates; no execution command is provided here.

Lifecycle: D/E/F/G **PASS/CLOSED**, E handoff **ACCEPTED**, 2a **PASS/CLOSED**,
2b **NOT STARTED / PREPARED FOR SEPARATE AUTHORIZATION**, PE-4 **NOT COMPLETE**,
Phase 7A **ACTIVE**, rollback **NOT PERFORMED**.


## PE-4.0B.2a authenticated proof PASS/CLOSED - 2026-10-05

Authenticated production execution and independent evidence review PASS.
Exact successor, preparation and runtime identities are bound in the closure record.

[Canonical execution closure](../governance/pe4/pe4-0b2a-execution-closure.json).

2a proved live approved-endpoint reachability, authenticated REST access and exact
/api/ root capability, authenticated Home Assistant WebSocket handshake, approved
successor/runtime compatibility, bounded credential/private-output behavior, and
a bounded authentication-only interface. It did not prove or execute device/entity/
area registries, config entries, states, services, broader configuration,
subscriptions, event listening, registry/schema relationships or association logic.
These remain separately governed 2b or later work; PE-4 completion is not established.

D/E/F/G remain PASS/CLOSED; Action E handoff ACCEPTED. PE-4.0B.2a is now
PASS/CLOSED; 2b NOT STARTED; PE-4 NOT COMPLETE; Phase 7A ACTIVE; rollback
NOT PERFORMED. F/G were not rerun; rollback and 2b were not executed. No credential
was persisted in repository evidence. This checkpoint accessed no PI3/PI5/HA and
reran no authenticated client. Historical/runtime/implementation identities remain
unchanged. The preparation record remains immutable pre-execution evidence with
2a NOT_STARTED; the new closure record supplies the post-execution state. Next
work requires separate governance; no 2b preparation or execution is authorized here.

## PE-4.0B.2a successor authenticated proof preparation - 2026-10-05

Future execution selects the release-source successor at
`/home/jazofv1/hioc-release-source/tools/hioc-pe4-ha-auth-capability.py` with the
existing `cpython311-websockets16.1.1-lock-v1` isolated interpreter. Client flags
are `-I -B`: isolated Python/user paths and no bytecode writes. Omit `-S` for
the client because CPython 3.11 needs site initialization for the venv prefix
and approved site-packages. The stdlib-only bootstrap uses `-I -B -S`.

The environment is cleared first. Retain only PATH=/usr/bin:/usr/sbin (approved
system tools, including ip), HOME=/nonexistent (no ambient home configuration),
LANG=C.UTF-8 and LC_ALL=C.UTF-8 (fixed encoding), and the validated parent SHELL
(bash/zsh/ash at approved /bin or /usr/bin paths). Operator discovery uses
pwd/geteuid, not environment names. PYTHONPATH, PYTHONHOME and every proxy variable
are absent. The client inherits terminal stderr and receives /dev/tty stdin.

Pre-token gates bind the separately verified preparation commit, clean synchronized
main with no untracked files or active operation, source blob/SHA, PI3 identity,
exact active/final paths, accepted runtime tree bytes/metadata, digest-bound D
distributions, CPython 3.11.2, aarch64 SOABI, and websockets 16.1.1/origin. Read-only
E tree primitives validate the existing runtime; no E/F/G action is invoked.
Source identity is checked again after execution. The future operator block is
delivered in the preparation report and requires separate execution authorization.

[Canonical preparation record](../governance/pe4/pe4-0b2a-successor-preparation.json).

D/E/F/G remain PASS/CLOSED, E handoff ACCEPTED; successor CORRECTED /
REPOSITORY_ONLY / NOT DEPLOYED. 2a is NOT STARTED / PREPARED FOR SEPARATE
AUTHORIZATION; 2b NOT STARTED; PE-4 NOT COMPLETE; Phase 7A ACTIVE; rollback
NOT PERFORMED. Historical F/G identity/runtime and accepted handoff/lock are
unchanged. No authenticated execution, PI3/PI5/HA access, F/G rerun or rollback
occurred. Package installation, another environment and pointer mutation are
excluded. Stop after the separately authorized proof; chain no later action.

## PE-4.0B.2a consolidated client boundary correction - 2026-10-05

The successor corrects absolute REST deadline enforcement, duplicate-safe JSON,
decoder recursion normalization, receive-coroutine ordering, and private network
interrupt handling with RC 130. Existing parser/getpass/timing/send controls remain.
[Canonical identity and correction details](PE4_HOME_ASSISTANT_ACCESS_PRIVACY_CONTRACT.md#pe-40b2a-consolidated-client-boundary-correction---2026-10-05).

Historical F/G identity/runtime are untouched. No PI3/PI5/HA authenticated operation,
F/G action, rollback, or 2b execution occurred. Successor remains repository-only,
not deployed; 2a NOT STARTED / NOT PREPARED and 2b NOT STARTED. Preparation has not
passed. Repeat the comprehensive preparation review separately before any future
operator block or authenticated execution authorization; no preparation JSON is created.

## Authentication send deadline correction - 2026-10-05

Preparation found the unbounded WebSocket authentication send before execution.
One send task now waits only for the remaining shared absolute network deadline.
Timeout maps to ENDPOINT_UNAVAILABLE / WEBSOCKET_CAPABILITY, closes before
cancelling pending send work, and reaps it with finite 5-second cleanup bounds;
failed/timed-out close aborts the transport. Cleanup sends no authentication
retry and performs no second receive. The existing context/socket cleanup remains.
Parser, secure getpass, post-credential timing and receive bounds are unchanged.

New successor blob: 260a4cb2904529983a73fa02ae6cfb13a4c18ab8.
New successor SHA-256: f2c69691f00d9c5952e59b80642015447078509f462c7fc550bb6d4dbfc2e6ab.
Supersedes repository-only candidate a16565101e4695c3c8658508a88d42b6b14e5dad:
blob 9e61dc7758de67a3473961a8f2624ba1f96237b1; SHA-256
561444e4961694072aab602e34227ec3be0598729b9fa778baf61fd9b1ac25b3.

Do not execute authenticated 2a yet; preparation must be repeated before
separate authorization. Historical F/G runtime remains untouched and prohibited
for authenticated use. No PI3/PI5/HA access, real token, authenticated operation,
F/G rerun, runtime publication or rollback occurred.

## Secure credential fallback correction - 2026-10-05

Successor preparation found the insecure getpass fallback before execution.
GetPassWarning is now promoted to an exception only around the approved
Python getpass prompt; warning filters are restored on success and failure.
Failure is AUTHENTICATION_UNAVAILABLE / CREDENTIAL_ACQUISITION before fallback
input, diagnostics, the network clock or network access. No custom credential
reader, retry or alternate secret source was introduced. Parser strictness and
the post-credential shared 20-second network budget are unchanged.

New successor blob: 9e61dc7758de67a3473961a8f2624ba1f96237b1.
New successor SHA-256: 561444e4961694072aab602e34227ec3be0598729b9fa778baf61fd9b1ac25b3.
Supersedes repository-only candidate 92eb4c317f1a50716adbaea2f1d80d3e66ceacc7:
blob be4499c81b0475b0320039ca2bfb74d926aefda4; SHA-256
d41a4991c51bb95546c80e85c39df421b59d29574f8645c328826c3df2e29f65.

Do not execute authenticated 2a: repeat preparation review before separate
authorization. Historical runtime client remains untouched and prohibited for
authenticated use. No PI3/PI5/HA access, real token acquisition, authenticated
operation, F/G rerun, runtime publication or rollback occurred.

## Successor network-budget timing correction - 2026-10-05

Preparation review found the network-budget timing defect before execution.
The 20-second clock now starts immediately after successful getpass credential
acquisition, before REST; local checks and prompt time are excluded. REST and
WebSocket retain one shared deadline, the 5/10-second caps and existing elapsed
checks. Strict authentication-frame parsing, credential privacy and 2b exclusion
remain unchanged. No authenticated operation occurred.

New successor blob: be4499c81b0475b0320039ca2bfb74d926aefda4.
New successor SHA-256: d41a4991c51bb95546c80e85c39df421b59d29574f8645c328826c3df2e29f65.
The repository-only candidate from correction commit
3f625ca0ef46deb83565823eb7ae35aa14aa8055 is superseded (blob
23ad1249c44b5d9b951057ea196e8bce3d598fd5; SHA-256
0e0817f64905eba13d8505a8aa2fa217ff7eab05c918877c8f9809393e4959b0).

Do not execute authenticated 2a yet. The corrected successor is repository-only
and not deployed; preparation must be repeated before separate authorization.
The historical F/G runtime client remains unchanged and prohibited for
authenticated use. No PI3/PI5/HA access, F/G rerun or rollback occurred.

## Repository successor authentication-frame correction — 2026-10-05

The canonical tools/hioc-pe4-ha-auth-capability.py successor source now corrects
the exact-one-key authentication parser defect. Bounded JSON object parsing
requires a string type; phase validators accept only auth_required/auth_ok
with exactly type + string ha_version, or auth_invalid with exactly type +
string message. Ancillary values are validated and discarded. auth_invalid
maps to AUTHENTICATION_FAILED / AUTHENTICATION; other schemas fail closed.
The exchange sends one auth frame and no command after auth_ok. REST, network,
credential acquisition, terminal markers and the 2b prohibition are unchanged.

Successor Git blob: 23ad1249c44b5d9b951057ea196e8bce3d598fd5.
Successor SHA-256: 0e0817f64905eba13d8505a8aa2fa217ff7eab05c918877c8f9809393e4959b0.
This is REPOSITORY_ONLY / NOT DEPLOYED, not executed and not authorized for
execution. Historical F/G identity record, constants, runtime publication and
evidence are unchanged; F/G were not rerun. The old historical runtime client
remains unsuitable and prohibited for authenticated 2a. Earlier defect and
identity-split entries below describe their historical checkpoint state.
Next checkpoint: separate successor preparation review binding the final
correction commit and this source identity; 2a is not prepared here.

D/E/F/G PASS/CLOSED; Action E handoff ACCEPTED; 2a NOT STARTED; 2b NOT STARTED;
PE-4 NOT COMPLETE; Phase 7A ACTIVE; rollback NOT PERFORMED.

## Historical authenticated 2a operator STOP boundary — 2026-10-05

Do not use the historically published F/G client for authenticated 2a: its
authentication-frame parser defect remains unresolved. G remains PASS/CLOSED
for its credential-free contract. Historical identity is pinned in
governance/pe4/historical-fg-client.json; canonical source is unchanged here.
A successor requires separate parser correction, source identity binding and
preparation review. Do not rerun F/G from an evolved successor-client HEAD.
2a is BLOCKED / NOT STARTED; 2b NOT STARTED; PE-4 NOT COMPLETE.

## Current Action G production governance closure — 2026-10-05

Action G is **PASS/CLOSED** after exactly one production execution using
consumer a01dfb53258317ba703d320836b38b38650872bd. Operator-supplied terminal
evidence is RESULT=PASS, ERROR_CODE=NONE, FAILURE_STAGE=COMPLETE,
ROLLBACK_RECOMMENDED=FALSE, EVIDENCE_STATE=CONFIRMED, RC=0,
CREDENTIAL_USE=FALSE and NETWORK_CONNECTION_ATTEMPTED=FALSE.
Final native compatibility, read-only production preparation and independent
post-execution evidence review all PASSed; source pre/postchecks PASSed.
G was not rerun, F was not rerun, and rollback was not performed.

Evidence: /tmp/hioc-pe4-runtime-preflight-97fcfda645295262b1735816c5481544.
Exact file set: result.json; size 1809 bytes; directory 0700 and file 0600,
both owned by 1000:1000.
ACTION_G_PRODUCTION_RESULT_SHA256=e63133f034da322fd761aaf56613a7706e577b332057a8f763891c855bbbb02e
Published bytes exactly matched the preceding canonical preparation and
independent reconstruction, canonical JSON and schema validation.
This /tmp path is production execution evidence, not a durable repository
artifact. These documents durably record the reviewed governance outcome.

F consumer 2a5e6299a0806c3f3d7c3bc11c84fddc8492333c; transaction
17fc3e0580ff007cdcd619ed2e2d3b34; result SHA
d647c7b2241d7800a3c819cf86459e2be95c3ef58581d5ffef2dbf5bd1190941;
COMMITTED SHA 24bb64cc8d885297e5696ddd733ec0dfab4b28a24e18a6996b667c186f2016e9.
Accepted E manifest SHA remains
1ac94f233bf543cafdc81b1f530177bd1c84d46ae13a7a686b33d34032d50c14.
Final environment:
/home/jazofv1/hioc/runtime/pe4/environments/cpython311-websockets16.1.1-lock-v1.
Active target: environments/cpython311-websockets16.1.1-lock-v1.
Frozen client SHA: 5c2886452a61185c7e7329777dbd4fa3de4da98dd4793a1a84501bc30016879e.
Runtime/F revalidation PASSed; environment, active, previous-active and client
remained unchanged through native validation, execution and independent review.

Current status: D PASS/CLOSED; E PASS/CLOSED; Action E handoff ACCEPTED;
F PASS/CLOSED; G PASS/CLOSED; G execution count ONE; independent review PASS;
rollback NOT PERFORMED. Native compatibility is PASS/CLOSED.
**PE-4 NOT COMPLETE**: the master plan's authenticated API interface-contract
freeze and PE-4.0B.1 completion roadmap separately require preparation of
PE-4.0B.2a authenticated API/capability proof (REST_THEN_WEBSOCKET_2A).
That preparation is the next governed checkpoint; execution requires separate
authorization and cannot chain into PE-4.0B.2b registry/schema discovery.
G proves credential-free preflight, not live HA reachability, credentials,
authenticated REST/WebSocket association, service authorization, read scope
or application behavior beyond its bounded contract.

Repository closure validation PASS: exact eight-document scope, unchanged
implementation/tests and all 27 protected baseline blobs, retained historical
records, existing release/static validator, bytecode-free Python compilation
and schema parsing, full diff review and git diff --check. No generated or
untracked artifacts; line-ending warnings are not failures.

This current closure supersedes prior pending-G status and retry instructions.
All earlier checkpoint entries retain their historical meaning and chronology;
they do not assert current pending status. This documentation-only checkpoint
does not access PI3/PI5 or execute any production lifecycle operation.

## Action G compatibility import fallback correction — 2026-10-05

G initially stopped at F HANDOFF because of incorrect recovery semantics;
the handoff correction PASSed. Distribution validation then failed because
standard discovery was removed too early; ordering was corrected.
The next optional python_socks probe converted expected ImportError into
RuntimeError; reviewed optional absence was corrected. POSIX msvcrt platform
detection then failed because recognized stdlib absence was treated as invalid;
platform stdlib absence was corrected. The latest supplied controlled child
now reaches CPython 3.11.2 copy.py's Jython compatibility probe:
from org.python.core import PyStringMap, caught by except ImportError with
PyStringMap=None. G rejected org at its stdlib-name assertion because org
is not a stdlib name. This is a G loader-semantics defect, not a production
dependency defect.

One immutable REVIEWED_ABSENT_TOP_LEVEL policy contains exactly org and
python_socks. Finder returns None for these families and descendants without
PathFinder or disk lookup. Final meta path remains G Finder, BuiltinImporter,
FrozenImporter, so unresolved org produces ModuleNotFoundError / ImportError
and CPython's compatibility fallback continues. Arbitrary non-reviewed
third-party names remain denied with CONTROLLED_RUNTIME_INVALID.

require_reviewed_absence rejects resident org, org.*, python_socks and
python_socks.* before verified package imports and after capabilities/client
phases. No preloaded module is removed or adopted. Generated child includes
the renamed policy/helper. Recognized platform stdlib absence, existing
trusted-origin checks, built-in/frozen handling, verified websockets
source/native loaders, redirect validation, frozen-client detection and
distribution ordering remain unchanged. Startup -I -B -S, sanitized environment,
proxy prohibition, no site/.pth/user site, network/credential prohibitions,
and F/runtime/client revalidation remain in force.

Regression tests cover the exact reviewed tuple, both families and descendants
without PathFinder, preloaded top-level/descendant rejection through real
child_probe, and an isolated CPython-compatible org.python.core import pattern.
Ordinary PathFinder sees a malicious org tree, while G leaves it unexecuted,
raises normal ModuleNotFoundError and generates no bytecode. Existing
python_socks fallback and platform-absent stdlib tests remain green.

Latest supplied G_NATIVE_PREFLIGHT=PASS accepted F transaction
17fc3e0580ff007cdcd619ed2e2d3b34, result SHA
d647c7b2241d7800a3c819cf86459e2be95c3ef58581d5ffef2dbf5bd1190941,
COMMITTED SHA 24bb64cc8d885297e5696ddd733ec0dfab4b28a24e18a6996b667c186f2016e9.
Runtime and F revalidation continue to PASS; source remained clean and no G
evidence has been created. No PI3/PI5 access or production G/F/rollback
execution occurred in this repository checkpoint.

Validation: dedicated G 31/31 PASS; focused F/G/lifecycle 177 total,
176 PASS and one platform skip; full repository 1221 total, 1174 PASS and
47 platform skips. All 138 repository Python files and generated child
compile in memory; schemas parse. Exact ten-file scope, complete diff review,
document synchronization/history retention, and all 27 protected baseline
blob comparisons PASSed. Closed D/E/F artifacts remain unchanged.
git diff --check PASSed with line-ending warnings only; existing unclosed-file
ResourceWarnings did not fail tests.

D PASS/CLOSED; E PASS/CLOSED; Action E handoff ACCEPTED; F PASS/CLOSED;
G NOT STARTED; rollback NOT PERFORMED; PE-4 not complete.
Native compatibility remains pending. Next: separately authorize native retry.
ACTION_G_NATIVE_COMPATIBILITY_RETRY_READY_FOR_SEPARATE_AUTHORIZATION

## Action G platform stdlib absence correction — 2026-10-05

The initial native attempt stopped at HANDOFF because G misread F recovery
semantics. Correction allowed F-to-G handoff to PASS. The next probe stopped
because G removed distribution discovery before metadata validation.
The ordering correction advanced into verified websockets imports; the next
probe stopped because optional python_socks ImportError became RuntimeError.
The optional-dependency correction advanced farther into stdlib imports.
The latest supplied diagnostic identifies msvcrt with origin/search path None
under the trusted POSIX base paths. CPython 3.11.2 subprocess intentionally
catches ModuleNotFoundError for msvcrt to detect the POSIX platform.
This is a G stdlib-loader semantics defect, not a production dependency failure.

Finder still rejects unknown third-party names, retains verified websockets
handling and the reviewed-absent python_socks policy, and returns built-in
and frozen specs unchanged. For recognized stdlib names it searches only
the existing approved path (or supplied package path). An absent spec now
returns None so normal import machinery raises ModuleNotFoundError.
An existing spec must still have a non-None origin within the unchanged
trusted boundary. There is no msvcrt-specific production exception.

Final sys.meta_path remains exactly G Finder, BuiltinImporter, FrozenImporter.
No general PathFinder, cwd, site-packages, site/.pth/user-site loading is added.
Startup -I -B -S, sanitized environment, proxy prohibition, verified
source/native loaders, redirect validation, frozen-client detection,
network/credential prohibitions and runtime/F/client revalidation remain.
The explicit accepted D-evidence distribution identity is unchanged.

Tests cover recognized msvcrt absence, unknown-name denial, accepted and
forged origins, absent package submodules, real built-in/frozen specs, and
an isolated representative platform import probe. A malicious platform-absent
stdlib-name file is visible to ordinary PathFinder but invisible to restricted
trusted lookup; ModuleNotFoundError occurs without execution or bytecode.
Windows uses the actually absent macOS _scproxy analogue for this disk test.
Existing optional dependency, metadata ordering and verified loader tests remain.

Latest supplied G_NATIVE_PREFLIGHT=PASS accepted F transaction
17fc3e0580ff007cdcd619ed2e2d3b34, result SHA
d647c7b2241d7800a3c819cf86459e2be95c3ef58581d5ffef2dbf5bd1190941,
COMMITTED SHA 24bb64cc8d885297e5696ddd733ec0dfab4b28a24e18a6996b667c186f2016e9.
Runtime and F transaction post-diagnostic revalidation PASSed, source was clean,
and no G evidence was created. No PI3/PI5 access or production G/F/rollback
execution occurred in this repository correction.

Validation: dedicated G 30/30 PASS; focused F/G/lifecycle 176 total,
175 PASS and one platform skip; full repository 1220 total, 1173 PASS and
47 platform skips. Compilation of 106 repository Python files and generated
child, schema parsing, exact ten-file scope, complete diff inspection and
all 27 protected baseline blob comparisons PASSed. Closed D/E/F artifacts
remain unchanged. git diff --check PASSed with line-ending warnings only;
existing unclosed-file ResourceWarnings did not fail tests.

D PASS/CLOSED; E PASS/CLOSED; Action E handoff ACCEPTED; F PASS/CLOSED;
G NOT STARTED; rollback NOT PERFORMED; PE-4 not complete.
Native compatibility remains pending. Next: separately authorize native retry.
ACTION_G_NATIVE_COMPATIBILITY_RETRY_READY_FOR_SEPARATE_AUTHORIZATION

## Action G reviewed optional dependency fallback correction — 2026-10-05

The first native compatibility attempt stopped at HANDOFF because G
misread F's recovery semantics. After correction, F-to-G handoff PASSed.
The next controlled probe stopped on distribution discovery because G
removed PathFinder too early. After that correction, G_NATIVE_PREFLIGHT=PASS
and the probe advanced into verified websockets.asyncio.client source.
Its supported python_socks optional import was converted from expected
ImportError into G's CONTROLLED_RUNTIME_INVALID RuntimeError, causing
PROBE_FAILED at PROBE. This is a G loader-semantics defect.

The accepted environment remains exactly pip 23.0.1, setuptools 66.1.1
and websockets 16.1.1. The reviewed-absent immutable policy contains only
python_socks. Finder returns None for that top-level name and descendants,
without PathFinder or disk lookup. With only G Finder, BuiltinImporter
and FrozenImporter installed, absence produces ModuleNotFoundError
(an ImportError), selecting websockets' supported no-SOCKS fallback.
Arbitrary unknown third-party imports still fail closed.

Resident python_socks and python_socks.* keys reject before websockets
imports; they are never removed or adopted. Absence is checked again after
capabilities and frozen-client detection. Verified source/native loaders,
redirect validation, client detection, -I -B -S, sanitized environment,
proxy prohibition, no site/.pth/user site, network/credential prohibitions,
runtime revalidation and fixed F predecessor bindings remain unchanged.

The exact accepted F transaction is 17fc3e0580ff007cdcd619ed2e2d3b34,
result SHA d647c7b2241d7800a3c819cf86459e2be95c3ef58581d5ffef2dbf5bd1190941,
COMMITTED SHA 24bb64cc8d885297e5696ddd733ec0dfab4b28a24e18a6996b667c186f2016e9.
Runtime and F post-failure revalidation PASSed every time. No G evidence
was created. No production G, F or rollback execution occurred here.

Regression coverage proves the representative two-import ImportError
fallback in an isolated subprocess, a searchable malicious disk package
remaining inert, reviewed-only lookup behavior, unknown-package denial,
resident top-level/descendant rejection through real child_probe, repeated
absence checks, and exact final restricted meta path.

Validation: dedicated G 25/25 PASS; focused F/G and lifecycle 171 total,
170 PASS and one platform skip; full repository 1215 total, 1168 PASS and
47 platform skips. In-memory compilation of 106 Python files and generated
child source, schema parsing, exact ten-file scope, complete diff inspection
and 27 protected baseline blob comparisons PASSed. git diff --check PASSed
with line-ending warnings only. Existing unclosed-file ResourceWarnings
did not fail tests. Closed D/E/F artifacts remain unchanged.

D PASS/CLOSED; E PASS/CLOSED; Action E handoff ACCEPTED; F PASS/CLOSED;
G NOT STARTED; rollback NOT PERFORMED. Native compatibility remains pending.
Next checkpoint: separately authorize the native compatibility retry.
ACTION_G_NATIVE_COMPATIBILITY_RETRY_READY_FOR_SEPARATE_AUTHORIZATION

## Action G distribution discovery ordering correction — 2026-10-05

First native compatibility attempt stopped safely at HANDOFF because G
misinterpreted F's in-progress recovery semantics. After that correction,
G_NATIVE_PREFLIGHT=PASS and the exact F transaction/result/COMMITTED bindings
PASSed. The second native retry reached the controlled child but stopped at
PROBE with PROBE_FAILED before WebSocket/client validation or G evidence.
The failed condition was exact distribution dictionary comparison.
An independent read-only diagnostic observed pip==23.0.1,
setuptools==66.1.1 and websockets==16.1.1, with
EXPECTED_EQUALS_OBSERVED=TRUE. Runtime and F transaction postchecks PASSed.
No runtime mutation or G execution occurred. This was a G ordering defect,
not a dependency/runtime failure.

importlib.metadata discovers distributions through sys.meta_path finders.
G removed standard PathFinder before its explicit-site metadata scan; G's
restricted Finder delegates module lookup but supplies no distribution finder.
G now performs the exact accepted D-evidence distribution comparison after
controlled startup, trusted stdlib/descriptor/interpreter/environment checks
and network/credential prohibitions, while standard discovery is available.
It then installs the unchanged restrictive meta path before any websockets,
native speedup or frozen-client import and keeps that path through final checks.

The scan reads metadata only from the final environment's explicit
lib/python3.11/site-packages. Duplicate names, missing/extra names and wrong
versions reject. Package/version policy still comes from accepted D evidence.
No site invocation, .pth processing, user-site scanning or new sys.path entry
is introduced. Startup remains -I -B -S; verified source/native loading,
corrected redirect semantics, client detection and proxy restrictions remain.
PathFinder is not a general entry in the final restricted meta path.

Regression tests exercise real child_probe with target-only startup fixtures,
real explicit-site metadata discovery, and an import boundary proving package
imports occur only after restriction. They reproduce the loss of distribution
discovery after standard PathFinder removal and restore sys.meta_path in finally.
An isolated -I -B -S subprocess proves malicious package/.pth/site customization
fixtures stay inert and create no pyc.

D: PASS/CLOSED. E: PASS/CLOSED. Action E handoff: ACCEPTED. F: PASS/CLOSED.
G: NOT STARTED. Rollback: NOT PERFORMED. Native compatibility remains pending
until the corrected controlled child passes on PI3. PE-4 is not complete.
F/D/E/common, schemas, entrypoint, lock, frozen client and accepted E handoff
remain unchanged. This Windows correction accesses neither PI3 nor PI5.

Next checkpoint:
`ACTION_G_NATIVE_COMPATIBILITY_RETRY_READY_FOR_SEPARATE_AUTHORIZATION`.

Distribution-order correction validation PASS: 20 dedicated G tests; 166 focused
F/G and lifecycle/handoff regressions (165 PASS, one POSIX-only skip); full suite
1210 tests (1163 PASS, 47 platform/tool-dependent skips), zero failures/errors.
Bytecode-suppressed compilation, schema parsing, exact ten-file scope, complete
diff review, synchronized document retention and 27 protected-blob comparisons
PASS. F implementation/schema and closed D/E/F artifacts remain unchanged.
git diff --check PASS; line-ending conversion warnings and pre-existing test
ResourceWarnings are non-failing.

## Action G F-journal recovery correction — 2026-10-05

The first PI3 G native compatibility attempt safely stopped in G.Posix.preflight
with ERROR_TYPE=Failure, FAILURE_CODE=MISMATCH and FAILURE_STAGE=HANDOFF.
The controlled runtime probe and G evidence creation were not reached.
Production/source state remained unchanged; no G execution, F rerun or rollback
occurred. This was a G validator defect, not an F failure.

G incorrectly required recovery FALSE for all numbered F records and the
provisional RESULT. Accepted F version 2.0 intentionally requires recovery TRUE
while its allocated transaction is incomplete. G now validates exact event,
publication, evidence, recovery, result, error/stage and digest progression:
0000–0011 retain recovery TRUE and evidence NOT_CREATED; RESULT retains recovery
TRUE, ACTIVE_SWITCHED and UNCONFIRMED; 0012/RESULT_REFERENCE retains recovery TRUE,
ACTIVE_SWITCHED and CONFIRMED; only 0013/COMMITTED has recovery FALSE, COMPLETE,
CONFIRMED, PASS/NONE/COMPLETE and the exact referenced result digest.
Rollback remains FALSE throughout.

Exact transaction/file set, canonical/schema validation, sequence, chain, event
order, F consumer, production result/COMMITTED SHA pins, reference linkage,
bindings and live-publication checks remain mandatory. F implementation/schema,
F production transaction/evidence, D/E/common/rollback/client/lock, accepted E
manifest, G entrypoint and G result schema are unchanged.

Regression fixtures use the real immutable F Journal serializer/validator with
a small synthetic writer; no F executor or production preflight is invoked.
Tests accept faithful successful incomplete states and reject premature recovery
clearance, COMMITTED recovery TRUE, wrong publication/evidence progression,
wrong result/COMMITTED digests, broken chain/order/sequence, wrong file set and
invalid result/error/stage/rollback/reference contracts.

D: PASS/CLOSED. E: PASS/CLOSED. Action E handoff: ACCEPTED. F: PASS/CLOSED.
G: NOT STARTED. Rollback: NOT PERFORMED. Native compatibility is not yet PASS.
The accepted historical continuity limitation remains
NO_PERSISTED_E_TIME_RECURSIVE_BASELINE. PE-4 remains incomplete.

Next checkpoint:
`ACTION_G_NATIVE_COMPATIBILITY_RETRY_READY_FOR_SEPARATE_AUTHORIZATION`.
This repository correction accesses neither PI3 nor PI5 and authorizes no
production commands.

Repository correction validation PASS: 15 dedicated G tests; 161 focused F/G
and lifecycle/handoff regressions (160 PASS, one POSIX-only skip); full suite
1205 tests (1158 PASS, 47 platform/tool-dependent skips), no failures/errors.
Bytecode-suppressed compilation, schema parsing, exact ten-file scope, complete
diff/document review and 27 protected-blob comparisons PASS. F implementation
and F schema remain exactly unchanged. git diff --check PASS; line-ending
conversion warnings and pre-existing test ResourceWarnings are not failures.

## Action G implementation

G validates the F predecessor and local runtime/client facts only. Credentials,
Home Assistant access, network checks and service operations remain excluded.

## Action F production closure — Evidence Report — 2026-10-05

This is the authoritative current Action F closure. Earlier checkpoint sections
below retain historical status and authorization boundaries; their NOT STARTED
statements and earlier next-checkpoint markers do not describe current F status.
This repository checkpoint records the supplied production execution and
separately completed read-only review; it does not repeat production inspection.

### Deployment result

Action F (PE-4.0B.2a-F) executed exactly once on PI3 using consumer
`2a5e6299a0806c3f3d7c3bc11c84fddc8492333c`.
Production terminal: RESULT=PASS, ERROR_CODE=NONE, FAILURE_STAGE=COMPLETE,
ROLLBACK_RECOMMENDED=FALSE, PUBLICATION_STATE=COMPLETE,
RECOVERY_REQUIRED=FALSE, EVIDENCE_STATE=CONFIRMED; process RC 0.

Transaction ID: `17fc3e0580ff007cdcd619ed2e2d3b34`.
Transaction directory:
`/home/jazofv1/hioc/runtime/pe4/transactions/f-17fc3e0580ff007cdcd619ed2e2d3b34`.

Independent read-only production review PASS: directory mode 0700,
15 transaction files, 14 journal events; chain, event order, schema/canonical
validation, exact result reference and committed-state validation all PASS.
Result record SHA-256:
`d647c7b2241d7800a3c819cf86459e2be95c3ef58581d5ffef2dbf5bd1190941`.
Committed record SHA-256:
`24bb64cc8d885297e5696ddd733ec0dfab4b28a24e18a6996b667c186f2016e9`.

### Intended behavior

Publication-only F consumed and independently validated the accepted Action E
handoff, verified construction against the accepted machine baseline, published
the final environment and HA capability client, established the active pointer,
recorded previous-active=NONE, and produced a durable committed journal.

Final environment:
`/home/jazofv1/hioc/runtime/pe4/environments/cpython311-websockets16.1.1-lock-v1`.
The original construction path is absent after the governed rename.
Client: `/home/jazofv1/hioc/tools/hioc-pe4-ha-auth-capability.py`.
Client SHA-256:
`5c2886452a61185c7e7329777dbd4fa3de4da98dd4793a1a84501bc30016879e`.
Active target: `environments/cpython311-websockets16.1.1-lock-v1`.
Previous-active content: `NONE`.

### Invariant checks

Independent production review recorded PASS for accepted handoff binding,
durable handoff unchanged, original D evidence unchanged, original E evidence
unchanged, final environment tree equality, D eligibility marker preservation,
client SHA, active pointer, previous-active, journal chain, committed record,
source integrity and absence of all F publication temporary files.
Only the permitted root-name/root-ctime transition occurred.
PI3 source remained at the execution consumer above with no source mutation
during execution or independent review.

Retained accepted bindings, all independently reviewed PASS:

- Accepted E manifest SHA-256:
  `1ac94f233bf543cafdc81b1f530177bd1c84d46ae13a7a686b33d34032d50c14`.
- Durable E bundle manifest SHA-256:
  `1f5c5b477a01e3ef82017d8d57a70f864cb0ddb6ba28371989a3124b1cecf804`.
- Accepted construction tree SHA-256:
  `4a929181d69f7391b3e39a0fd27fb17aa9c8883f42d9707af559c9a986d514a9`.
- Continuity attestation SHA-256:
  `0ba4f111a1a8cc21336c7c4676f0f19fa37d166158155aa9fe88153b7dff7c49`.

### Warnings and limitations

The multi-object F publication is journaled and durable, but not globally atomic.
The historical E-to-capture recursive interval remains governance-attested,
not retrospectively machine-proven: GOVERNANCE_ATTESTED_E_TO_CAPTURE with
NO_PERSISTED_E_TIME_RECURSIVE_BASELINE; historical recursive flags remain false.
The accepted capture remains the machine-verifiable continuity baseline forward.
G has not executed; authenticated association/service proof has not yet been
established by G. F performed no service restart/reload.
F success does not certify G's runtime/shared probes or production readiness.

### Repository closure validation

Focused PE-4 governance/lifecycle/handoff checks: 125 tests, 124 PASS,
one POSIX-only skip. Complete repository suite: 1190 tests, 1143 PASS,
47 platform/tool-dependent skips; zero failures/errors.
Exact eight-document scope, synchronized reports and current Master Plan
lifecycle review PASS. All 24 explicitly checked protected blobs match
the implementation consumer; no other tracked path changed.
Accepted E manifest SHA-256 is unchanged.
git diff --check PASS; LF-to-CRLF conversion warnings only.
No PI3 native tests or production access occurred in this closure checkpoint.

### PASS / FAIL and next checkpoint

Action F Evidence Report: **PASS**. F is **PASS/CLOSED**, publication COMPLETE,
recovery required FALSE, rollback recommended FALSE. No recovery action is
required; no rollback is required or authorized.
Replacement B: PASS/CLOSED. C: PASS. D-PREP: PASS/CLOSED.
D: PASS/CLOSED. E: PASS/CLOSED. Action E handoff: ACCEPTED.
F: PASS/CLOSED. G: NOT STARTED. Rollback: NOT PERFORMED.
PE-4 remains incomplete while G is outstanding.

Next is a separately authorized bounded **Action G preparation** review,
not execution:
`ACTION_G_PREPARATION_READY_FOR_SEPARATE_AUTHORIZATION`.
This docs-only closure accesses neither PI3 nor PI5, changes no implementation,
and executes neither F again, G nor rollback.

## Historical Action F implementation checkpoint — production then NOT STARTED

Architecture B is implemented by `tools/hioc-pe4-runtime-publish.py` and the
dedicated `tools/hioc_pe4_action_f.py`. This is PE-4.0B.2a-F implementation,
not authorization or evidence of production execution. D/E/common/lock/client,
G/rollback, all Action E handoff tooling/schemas, and the committed accepted
Action E manifest remain unchanged.

F accepts only the current consumer `--governance-commit`; the committed
accepted handoff selects immutable D/E history and construction. It validates
canonical/schema acceptance, pinned accepted-manifest bytes, local clean
main/HEAD/origin and complete lineage, protected source blobs, the exact durable
bundle inventory/modes/digests, attestation bindings and historical limitation,
and the live construction recursively against the accepted capture. Atime is
excluded; descendant content, metadata, membership and inode changes fail.
Root/interpreter/native/configuration/D-marker bindings are independently
cross-checked. The D marker is read at `0400`. Reviewed durable D/E copies may
replace missing temporary originals; surviving originals must validate exactly.

No construction interpreter, installed module, websockets import, startup hook,
.pth processing, dependency/capability/redirect probe or network request runs.
F requires isolated, no-site, bytecode-suppressed system /usr/bin/python3 startup.
Only sanitized allowlisted local Git/source inspection and local target identity
inspection precede publication. F never invokes D/E/G or rollback.

The first-publication handoff requires absent final environment, active and
previous-active records, plus absence of unresolved transactions. An existing
client requires exact frozen bytes, owner/group, `0700` and retained descriptor
identity/metadata; conflicting clients fail. A POSIX nonblocking exclusive flock
on the retained PE4 root descriptor serializes F invocations through completion.
This lock is cooperative F exclusivity, not exclusion of privileged mutation;
operators must separately exclude other lifecycle writers. No lock-file creation
or journal hierarchy mutation occurs before all preconditions validate.

Transactions are exclusively allocated at
`/home/jazofv1/hioc/runtime/pe4/transactions/f-<32 lowercase hex digits>/`.
Transaction hierarchy is `0700`; sequential canonical records and result are
`0600`. The strict version `2.0` contract is
`governance/pe4/action-f-record.schema.json`.
Each numbered record binds its predecessor digest, transaction/current consumer,
accepted manifest, D/E lineage, bundle/tree/attestation, construction/final
identities, client disposition, pointer identities and publication/evidence state.

Progression is PREPARED; durable INTENT then verified/fsynced CONFIRMED for client
publication when absent, environment rename, previous-active creation, active
link staging and activation; POST_VERIFIED; immutable result; durable
RESULT_REFERENCE; COMMITTED. An exact existing client skips client mutation.
Absent destinations use renameat2(RENAME_NOREPLACE); no existing environment or
pointer is overwritten. Client/result records include file fsync; every boundary
includes directory and relevant parent fsync plus reread verification.
The construction root name and rename-induced ctime may transition once; all
other root fields and descendants must match. The observed final root ctime is
then frozen and recorded. Final pointer identities and exact client metadata
are rechecked. The multi-object transaction is not globally atomic.

PASS and RC 0 require rereading the canonical chained COMMITTED state and its
exact immutable result digest, final-state revalidation and successful descriptor
close. A result file alone is not acceptance. Handled failures are sanitized
finite records with RC 1; arguments reject with RC 2. Incomplete intents, partial
records and fixtures are retained. Unknown mutation outcomes report UNCERTAIN
and recovery-required. Read-only absence proof may establish nonpublication but
never authorizes retry. Second invocation rejects prior transaction state;
there is no resume, adoption, cleanup, rollback or automatic repair.
This initial publication has no validated prior active target, so rollback
recommendation remains FALSE even when reconciliation is required.

Windows synthetic/fault tests prove repository control flow; they do not certify
PI3 flock, no-replace kernel/libc support, POSIX name binding or filesystem
durability. Remaining prerequisites are separately authorized native compatibility
review, independent implementation/transaction review and bounded execution
preparation against the published current consumer. The existing G/rollback
tools are unchanged and are not authorized by this checkpoint; their compatibility
with F version 2.0 must be independently reviewed before any use. No production
validator or PI3 execution commands are issued here.

Final repository validation: 37 dedicated F tests PASS, including the full
intent/confirmation fault matrix. Final lifecycle/handoff regression: 146 tests,
145 PASS and one POSIX-only skip. Complete repository suite: 1190 tests,
1143 PASS and 47 platform/tool-dependent skips; zero failures/errors.
Bytecode-suppressed compilation, strict schema structure, full diff review,
exact 13-file scope and 19 protected-file comparisons PASS. The accepted E
manifest remains byte-identical with SHA-256
1ac94f233bf543cafdc81b1f530177bd1c84d46ae13a7a686b33d34032d50c14.
git diff --check PASS; LF-to-CRLF conversion warnings only.
Created files retain descriptor/name inode pins through write/fsync/reread;
journal rereads reject identical-byte inode replacement. Early synthetic
fixture path/digest/mode differences were corrected before final validation.

D: PASS/CLOSED. E: PASS/CLOSED. Action E handoff: ACCEPTED.
Continuity: ACCEPTED as GOVERNANCE_ATTESTED_E_TO_CAPTURE with
NO_PERSISTED_E_TIME_RECURSIVE_BASELINE; both historical recursive flags remain
false. The accepted capture is the machine-verifiable baseline forward.
F: NOT STARTED. G: NOT STARTED. Rollback: NOT PERFORMED.
No PI3/PI5 access, synchronization or production lifecycle action occurred.

Next checkpoint:
`ACTION_F_NATIVE_COMPATIBILITY_CHECK_READY_FOR_SEPARATE_AUTHORIZATION`.


## Action E handoff acceptance — 2026-10-05

<a id="action-e-handoff-acceptance-2026-10-05"></a>

Repository acceptance is **ACCEPTED** under
`PE4-ACTION-E-HANDOFF-ACCEPTANCE-20261005`.
The committed `governance/pe4/accepted-action-e.json` is canonical and schema
validated; its SHA-256 is `1ac94f233bf543cafdc81b1f530177bd1c84d46ae13a7a686b33d34032d50c14`. This acceptance binds the
already captured, independently reviewed, preserved and independently reviewed
production handoff. It performs no new production operation.

Capture **PASS / NONE / COMPLETE**, independent capture review **PASS**:
`/home/jazofv1/hioc/runtime/pe4/captures/e-ed2af1a61929197bd045c08ee654bba4`.
Capture source and preservation source are both `350dda0d1bc138f5adbbf2c15ac9ecd128eefd9f`.
Capture authorization: `PE4-ACTION-E-CAPTURE-20261005`; capture records remain
`PROPOSED`. Preservation authorization:
`PE4-ACTION-E-PRESERVATION-20261005`; preserved records remain
`APPROVED_FOR_PRESERVATION`. Only repository governance records acceptance.

| Binding | SHA-256 |
| --- | --- |
| Capture manifest | `622c81614ec10a5cd6408b83b506e8d58f21de542b389bcc2dcd3fae4b9f108c` |
| Capture report | `1b3ed36af9da63742d5977bb185084ad152634b8ff3a0a6e97e54d3dfeccd02e` |
| Accepted construction tree | `4a929181d69f7391b3e39a0fd27fb17aa9c8883f42d9707af559c9a986d514a9` |
| Durable manifest | `1f5c5b477a01e3ef82017d8d57a70f864cb0ddb6ba28371989a3124b1cecf804` |
| Continuity attestation | `0ba4f111a1a8cc21336c7c4676f0f19fa37d166158155aa9fe88153b7dff7c49` |

The independently measured pre-capture construction digest equals the accepted
construction-tree digest above. Preservation **PASS / NONE / COMPLETE** and
independent durable-bundle review **PASS** bind
`/home/jazofv1/hioc/runtime/pe4/handoffs/action-e-1c1698f009457baa1c3b548db31916559fcc2fc8`.
Durable directory mode is `0500`, files `0400`; these permissions do not
prevent deliberate owner/root changes. Original D/E copies, staging and the
accepted construction remain retained; no cleanup or baseline replacement is
authorized.

The one-time bridge is accepted exactly once as
`GOVERNANCE_ATTESTED_E_TO_CAPTURE`, with attestation class
`GOVERNANCE_DERIVED_ATTESTATION` and limitation
`NO_PERSISTED_E_TIME_RECURSIVE_BASELINE`.
`historical_recursive_snapshot_persisted=false` and
`historical_recursive_continuity_machine_proven=false` remain mandatory.
The historical E-to-capture recursive interval is not machine or
cryptographically proven. `NO_AUTHORIZED_POST_E_HIOC_MUTATION_RECORDED`
describes governed chronology; it does not claim that every possible mutation
was excluded. The accepted capture now supplies the machine-verifiable recursive
baseline forward (`MACHINE_VERIFIED_CAPTURE_FORWARD`).

The manifest preserves immutable D producer `6c431494c88688fef9a2fec7c7e81de0f503bdc2`,
E execution consumer `1c1698f009457baa1c3b548db31916559fcc2fc8`, original D/E evidence paths and
digests, frozen D source, retained root/interpreter identities and native member
digest. Its ten revalidated observable records retain the exact committed
comparison/source policy. It has no dependency on its enclosing acceptance
commit and invents no runtime timestamp.

D **PASS/CLOSED**; E **PASS/CLOSED** exactly once; Action E handoff **ACCEPTED**;
F **NOT STARTED**; G **NOT STARTED**; rollback **NOT PERFORMED**.
There was no D/E rerun and no production F action. This repository checkpoint
does not access PI3/PI5, rerun native validation, capture or preserve evidence,
change runtime artifacts, or begin F/G. Future F preparation must validate the
accepted bundle and current construction against these pinned records; mismatch
must STOP without refreshing historical values or adopting an alternate bundle.
Any surviving original D/E evidence must still match; reviewed durable copies
may supply the evidence when the temporary originals are absent.

Validation covers canonical/schema acceptance, exact production bindings,
runtime non-promotion and manifest immutability across successful and failed
capture/preservation workflows, plus the focused and complete repository suites.
Runtime tooling and schemas are unchanged. Focused validation: 60 tests,
59 PASS, 1 POSIX-only skip. Complete repository suite: 1153 tests,
1106 PASS, 47 platform/tool-dependent skips, zero failures/errors.
The first sandboxed full run could not read the existing cached PE-4 wheel;
the rerun with local fixture access passed. Canonical/schema, ten-file scope,
19 protected blob comparisons, bytecode-suppressed compilation and
git diff --check passed. Git emitted LF-to-CRLF conversion warnings only.

Next checkpoint:
`ACTION_F_IMPLEMENTATION_READY_FOR_SEPARATE_AUTHORIZATION`.


## Historical tooling checkpoint — continuity NOT ACCEPTED at that checkpoint

Choice 2 is selected as the bounded corrective policy: implement machinery for a
one-time `GOVERNANCE_ATTESTED_E_TO_CAPTURE` bridge. This selects tooling and the
policy; it does **not** accept the actual continuity bridge. No production
capture or preservation has occurred in this checkpoint. No durable accepted
handoff bundle is recorded, and `governance/pe4/accepted-action-e.json` has not
been created. Action F remains blocked and **NOT STARTED**.

The three evidence classes remain distinct:

- `RETAINED_MACHINE_OBSERVATION`: genuinely retained historical measurements.
- `GOVERNANCE_ATTESTED_E_TO_CAPTURE`: the historical interval, supported by
  governed chronology rather than a persisted recursive snapshot.
- `MACHINE_VERIFIED_CAPTURE_FORWARD`: exact comparisons against a future
  canonical capture; operational reliance begins only after independent capture
  review and later repository acceptance.

No E-time recursive snapshot was persisted. The records require
`historical_recursive_snapshot_persisted=false`,
`historical_recursive_continuity_machine_proven=false`, and
`NO_PERSISTED_E_TIME_RECURSIVE_BASELINE`. Current files, package hashes and a
new tree digest cannot manufacture historical recursive proof. Governed
chronology records no authorized post-E HIOC mutation; it does not exclude
out-of-band same-UID or privileged changes. Historical mtime/ctime comparisons
are possible only where actual retained values exist. Complete timestamps and
membership become capture-time observations, with atime excluded.

Immutable E consumer remains `1c1698f009457baa1c3b548db31916559fcc2fc8`; original
E evidence is `/tmp/hioc-pe4-dependency-validate-9ys_lrah`, SHA-256
`8d5ff1f602861d88ea8d363665a67091da2739686d10ab4aa9ac27f22389d834`.
D producer remains `6c431494c88688fef9a2fec7c7e81de0f503bdc2`; original D evidence
is `/tmp/hioc-pe4-runtime-construct-LW9Dvay6`, SHA-256
`a31f1e841f437dece13d327f14a99a93d5f96a8e258b9786cc6e49358821350d`.
Accepted construction remains
`/home/jazofv1/hioc/runtime/pe4/environments/.construct-cpython311-websockets16.1.1-lock-v1-mwJVPNqh`.
Retained root identity is `45826:823199:1000:1000:0750`; interpreter identity is
`45826:823209`. The native member digest remains
`b786db296f7d0677ddeceb7efbe963bc316a094f36e12388caa1333763ca4c1b`.
Mismatch must STOP; expected historical values must never be refreshed.

### Tooling interfaces and authorization boundary

`tools/hioc-pe4-action-e-handoff-capture.py` requires `--governance-commit` and
`--authorization-reference`. Capture source consumer is distinct from immutable
D/E identities. `tools/hioc-pe4-action-e-handoff-preserve.py` additionally requires
`--capture-directory`, `--capture-manifest-sha256`, `--capture-source-commit`,
and `--approval-state APPROVED_FOR_PRESERVATION`. The manifest digest must be
independently reviewed and pinned. An authorization reference records operator
approval; it is not a cryptographic authentication credential.

Both entry points use only `tools/hioc_pe4_action_e_handoff.py` for new logic.
Production guards require PI3 `nutandpihole`, IPv4 `192.168.100.252`, UID/GID
`1000:1000`, `jazofv1:jazofv1`, exact release-source root, clean main/HEAD/origin,
complete Git history, actual commits, no active operation and disabled Git
replacement objects. D is an ancestor of E; E is an ancestor of the current
consumer. Protected historical implementation blobs remain unchanged. The
52-member E policy is read statically from frozen Git source, not imported.

No construction Python, installed package or websockets import runs. Original
D/E records and producer-bound D eligibility must validate exactly. Static
package/member, configuration, hierarchy and retained-identity checks precede
canonical descriptor-relative capture. Construction, evidence and source are
revalidated after writing. Active/previous pointers, final environment and F
transaction artifacts must be absent; an unexpected prepublication state stops
for review rather than being adopted.

Capture deliberately writes evidence; it is construction-read-only, not globally
read-only. It allocates exclusively under
`/home/jazofv1/hioc/runtime/pe4/captures/e-<32 lowercase hex digits>`, with parent
and directory `0700`, files `0600`, owner/group `jazofv1:jazofv1`. The staged set is
`action-e-result.json`, `action-d-result.json`, `construction-tree.json`,
`capture-report.json`, `capture-manifest.json`. Historical result bytes are copied
exactly. Reports/manifests remain `PROPOSED`. Missing/changed staging invalidates
its review; no recreation under the same acceptance decision is permitted.

Preservation never establishes a new baseline: it compares the live construction
with the already staged tree. Original D/E evidence is still required for this
first preservation. It publishes an exclusive sibling bundle with
`renameat2(RENAME_NOREPLACE)` under
`/home/jazofv1/hioc/runtime/pe4/handoffs/action-e-1c1698f009457baa1c3b548db31916559fcc2fc8`.
Final directory is `0500`, files `0400`, owner/group `jazofv1:jazofv1`. Owner read
and traversal remain available; these permissions do not prevent deliberate
owner/root mutation. Required exact files are `action-e-result.json`,
`action-d-result.json`, `construction-tree.json`, `continuity-attestation.json`,
`manifest.json`. The attestation is `GOVERNANCE_DERIVED_ATTESTATION`, at most
`APPROVED_FOR_PRESERVATION`; it is not original supervisor-generated JSON.

Each file, evidence directory and publication parent has an fsync boundary and
independent reopen verification. Unsupported no-replace primitives, collisions,
cross-device errors, changed inputs or failed durability STOP without fallback,
cleanup or retry. Failed staging and originals remain retained. Modes alone are
not proof of durability or authenticity. Cooperative operator exclusivity is
required; descriptor checks cannot exclude privileged/uncooperative mutation.

### Strict records and future acceptance

Seven separate contracts under `governance/pe4` describe accepted handoff,
construction tree, continuity attestation, capture report, capture manifest,
durable bundle and fixed historical identity. The shared runtime validator
executes the bounded JSON Schema keywords used by these files, without a new
third-party dependency. Unknown/missing fields, duplicate keys, wrong types,
noncanonical records, malformed/full-length hashes and traversal are rejected.
New records use sorted compact ASCII-escaped UTF-8 JSON plus one LF; digests
cover exact bytes. Manifests exclude themselves from inventory. Trees use hex
POSIX-byte path components, stable metadata/content and deterministic membership;
limits are 100,000 entries, 64 MiB tree, 64 KiB metadata, 255-byte components and
4096-byte paths, with a bounded traversal depth. Nothing is truncated.

The eventual accepted manifest must bind real capture/report/bundle digests,
fixed D/E history, the continuity limitation, exact revalidated facts and explicit
Decisions/Master Plan authorization. It is created only in a later checkpoint
after independent capture and preservation reviews. Durable original copies may
then replace a missing `/tmp` original for future F preparation; any surviving
original must still match. Preservation deletes neither originals nor staging.

Future validation-to-publication handoffs must persist canonical construction
snapshots/digests at validation acceptance time. This historical exception must
not become the default. Windows synthetic tests do not certify PI3 ownership,
AArch64, real POSIX traversal, fsync or kernel/libc no-replace capability. Separate
native validation preparation/authorization is required before capture.

Current lifecycle remains replacement B PASS/CLOSED; C PASS exactly once;
D-PREP PASS/CLOSED; D PASS/CLOSED; E PASS/CLOSED exactly once; F/G NOT STARTED;
rollback NOT PERFORMED. D/E/F/G/common/lock/client source and historical evidence
are unchanged. This checkpoint does not synchronize PI3, authorize capture,
preserve evidence, accept continuity, or implement corrected F.

Next checkpoint:
`ACTION_E_HANDOFF_CAPTURE_NATIVE_VALIDATION_PREPARATION_READY_FOR_SEPARATE_AUTHORIZATION`.

## Production Action E — PASS / CLOSED

Accept the production Action E evidence and retain the STOP boundary. No F/G execution followed and no retry, cleanup or rollback occurred.

The following production facts are recorded from supplied operator evidence; this
Windows documentation closure does not access production or execute a lifecycle
action. Action E actually executed **exactly once** and is **PASS / CLOSED**.

The immutable execution consumer is
`1c1698f009457baa1c3b548db31916559fcc2fc8`; the accepted Action D producer is
`6c431494c88688fef9a2fec7c7e81de0f503bdc2`. Producer/current compatibility
passed before and after execution. The accepted construction remains
`/home/jazofv1/hioc/runtime/pe4/environments/.construct-cpython311-websockets16.1.1-lock-v1-mwJVPNqh`.
Action D evidence remains `/tmp/hioc-pe4-runtime-construct-LW9Dvay6`, with SHA-256
`a31f1e841f437dece13d327f14a99a93d5f96a8e258b9786cc6e49358821350d`.
Frozen Action D source SHA-256 remains
`e979cc6049f8912c23e880f121fd2988d0354623c4f2a7d27eafb310e4b0c213`.

The exact six production Action E terminal fields were:

```text
RESULT=PASS
ERROR_CODE=NONE
FAILURE_STAGE=COMPLETE
ROLLBACK_RECOMMENDED=FALSE
EVIDENCE_DIR=/tmp/hioc-pe4-dependency-validate-9ys_lrah
CONSTRUCTION_DIRECTORY=/home/jazofv1/hioc/runtime/pe4/environments/.construct-cpython311-websockets16.1.1-lock-v1-mwJVPNqh
```

Process RC was `0`. The sole new Action E namespace entry was
`/tmp/hioc-pe4-dependency-validate-9ys_lrah`; its final file set was exactly
`result.json`, with no `.result.tmp`. Ownership/mode and exact JSON review PASSed.
Accepted evidence SHA-256 is
`8d5ff1f602861d88ea8d363665a67091da2739686d10ab4aa9ac27f22389d834`.
The canonical successful JSON semantic content is:

```json
{"ACTION":"DEPENDENCY_VALIDATION","CAPABILITY_VALIDATION":"PASS","ENVIRONMENT_IDENTITY":"cpython311-websockets16.1.1-lock-v1","INSTALLED_VERSION":"16.1.1","action":"PE-4.0B.2a-E","error_code":"NONE","failure_stage":"COMPLETE","result":"PASS","rollback_recommended":false,"schema_version":"1.0"}
```

The supplied independent supervisor acceptance markers were:

```text
ACTION_E_PREEXECUTION_GUARDS=PASS
CURRENT_FINAL_CONSUMER_SOURCE=PASS
NATIVE_PROOF_CONTINUITY=PASS
ACTION_E_PROCESS_RC=0
ACTION_E_EVIDENCE_BEFORE=[]
ACTION_E_EVIDENCE_AFTER=["/tmp/hioc-pe4-dependency-validate-9ys_lrah"]
ACTION_E_EVIDENCE_OWNERSHIP_MODE=PASS
ACTION_E_EXACT_FILE_SET=PASS
ACTION_E_EXACT_JSON=PASS
ACTION_E_EVIDENCE_SHA256=8d5ff1f602861d88ea8d363665a67091da2739686d10ab4aa9ac27f22389d834
CURRENT_CONSUMER_COMMIT=1c1698f009457baa1c3b548db31916559fcc2fc8
ACTION_D_PRODUCER_COMMIT=6c431494c88688fef9a2fec7c7e81de0f503bdc2
SOURCE_UNCHANGED=TRUE
POST_PRODUCER_CONSUMER_COMPATIBILITY=PASS
CONSTRUCTION_CONTENT_AND_IDENTITY_UNCHANGED=TRUE
ACTION_D_MARKER_UNCHANGED=TRUE
ACTION_D_EVIDENCE_AND_DIGEST_UNCHANGED=TRUE
RUNTIME_HIERARCHY_UNCHANGED=TRUE
PUBLICATION_AND_POINTER_STATE_UNCHANGED=TRUE
ATIME_EXCLUDED=TRUE
ACTION_E_INDEPENDENT_REVIEW=PASS
ACTION_E_ACCEPTANCE=PASS
ACTION_E_LAUNCHED=TRUE
ACTION_F_EXECUTED=FALSE
ACTION_G_EXECUTED=FALSE
AUTOMATIC_RETRY=FALSE
MANUAL_CLEANUP=FALSE
ROLLBACK_PERFORMED=FALSE
STOP_REQUIRED=TRUE
```

The intentional write was only the private Action E evidence directory. Accepted
construction content/identity, D eligibility marker, D evidence/digest, source,
runtime hierarchy and publication/pointer state remained unchanged. Atime was
excluded according to the governed construction immutability contract.

Chronology remains: Action D PASS/CLOSED (third execution, after two historical
failures); earlier read-only D-to-E compatibility validation; controlled-startup
corrective design and implementation at `70cfceba3ddc5dd05818fa6f27653709abd9819c`;
architecture-matched native **non-lifecycle** validation; final PI3 consumer
synchronization to `1c1698f009457baa1c3b548db31916559fcc2fc8`; exactly one actual
production Action E invocation; then this documentation closure. Only the actual
production invocation advances E to PASS/CLOSED. Earlier preparation and native
validation did not execute E; their historical records below remain intact.

Current lifecycle: replacement B **PASS / CLOSED**; C **PASS exactly once**;
D-PREP **PASS / CLOSED**; D **PASS / CLOSED**; E **PASS / CLOSED exactly once**;
F **NOT STARTED**; G **NOT STARTED**; rollback **NOT PERFORMED**. STOP remains
required. No F publication/activation occurred, and F is not prepared here.

This documentation closure creates a descendant of the execution consumer; its
new HEAD is for a later checkpoint and must never be described retroactively as
E's execution consumer. Before future F preparation, separately inspect current F
governance and independently determine how F binds source/current consumer and
accepted E producer/evidence; do not assume E's producer/current model applies.
That inspection/preparation is not performed in this closure. The next checkpoint
is `ACTION_F_PREPARATION_READY_FOR_SEPARATE_AUTHORIZATION`.

## Historical Action E native non-lifecycle validation — prerequisite PASS / CLOSED

Operator boundary: native validation is PASS/CLOSED and is not production dependency-validation Action E execution. Preserve the accepted D handoff; stop for governance closure and separately authorized final repreparation against the resulting current-consumer candidate.

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

Operator boundary: use the future published corrective implementation/closure commit as consumer, retaining the accepted D producer. Validation may read the construction, never normalize, repair, warm caches, delete, retry, or roll back it.

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

Operator evidence confirms the explicitly selected immutable D handoff.
Future review must retain this producer/construction/evidence/digest selection
and evaluate the actual next consumer; no alternate handoff is adopted.

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

## Current Action E producer/current operator review

A later separately authorized review must select an explicit current consumer
`--governance-commit`, accepted D producer `--action-d-governance-commit`, and
construction directory. Neither commit may be inferred from the other. Confirm
producer provenance from the accepted immutable marker and D evidence, including
the selected evidence directory and independently reviewed evidence digest.

The accepted historical handoff remains producer
`6c431494c88688fef9a2fec7c7e81de0f503bdc2`, construction
`/home/jazofv1/hioc/runtime/pe4/environments/.construct-cpython311-websockets16.1.1-lock-v1-mwJVPNqh`,
evidence `/tmp/hioc-pe4-runtime-construct-LW9Dvay6`, SHA-256
`a31f1e841f437dece13d327f14a99a93d5f96a8e258b9786cc6e49358821350d`.
These are accepted review records, not generic source defaults or evidence-retention
guarantees. No production object was accessed or modified by this correction.

Current source must satisfy clean main/HEAD/origin identity, zero ahead/behind,
no active Git operation and all five normalized source identities. Producer/current
compatibility requires real commit objects, replacement protection, complete history,
producer equality/ancestry and exact D/common/lock committed blobs. Strict D marker
and evidence equality must still bind the producer and selected construction;
consumer substitution is forbidden. A failure stops before runtime/evidence work
with bounded diagnostics, without retry, rollback, or cleanup. Compatibility and
operator review are prerequisites, not authorization. Action E remains **NOT STARTED**;
separate E authorization is still required. F/G remain unauthorized.

The original implementation synchronization/read-only validation boundary
is now PASS/CLOSED as recorded above. Next checkpoint:
`ACTION_E_REPREPARATION_READY_FOR_SEPARATE_AUTHORIZATION`.

Action B fails closed if the staging pathname no longer resolves to its exact
creation-time device, inode, UID, and mode. Do not search for, adopt,
or clean a renamed or substituted directory. Treat failed identity proof as
ambiguous and preserve it for a separately authorized investigation. Duplicate
numeric PI3 known-host records or any role-specific ACL deviation on `.ssh`,
`known_hosts`, `id_ed25519`, or `id_ed25519.pub` are preflight failures, not
repair requests. Operators must not force shared OpenSSH objects into the HIOC
private-object ACL model.

The PE-4 authenticated client is an HIOC consumer on PI3 NUT&PIHOLE; PI5 HA is
only the remote API endpoint. Before credentials, a future local, network-free
PI3 preflight must prove execution identity, Python, terminal/getpass,
dependency APIs, and intended deployment permissions. A separate later route
proof may open only one bounded TCP connection to `192.168.100.251:8123`, send
no bytes, and close. Neither is executed here. Do not install HIOC code or
dependencies in PI5's Terminal add-on.

PE-4.0B.1 is COMPLETE / PASS. Its credential-free PI5 preflight proved the
`HA_TERMINAL_ADDON` context, HA OS deployment, and exact endpoint
`http://192.168.100.251:8123`; it performed no registry, state, configuration,
or production mutation. The earlier `UNSUPPORTED_HA_DEPLOYMENT` result remains
historical parser-contract failure evidence, not current status.

The PE-4.0B.2a authenticated capability client now exists at
`tools/hioc-pe4-ha-auth-capability.py` but has not been deployed or executed.
Its next gate is commit review followed by a separate dependency/runtime
preparation checkpoint. When separately authorized, it must use a
repository-controlled Python process and non-echoing `getpass`
prompt, retain the credential only in memory, install nothing, publish no raw
response, and stop for review on every result. It must not automatically run
PE-4.0B.2b registry/schema discovery. No live-state identity authority,
`.storage` fallback, database fallback, adapter implementation, or production
mutation is permitted.

Official API research now requires a repository-controlled client and
`REST_THEN_WEBSOCKET_2A`. The REST root and WebSocket authentication exchange
are the only authorized network interactions; the client must close without a
WebSocket command. A missing approved WebSocket dependency stops before the
credential prompt and must not trigger installation or custom protocol code.

PE-4.0A is repository governance only. It authorizes no PI5 access or operator
command. Before any separately authorized PE-4.0B invocation, operators must
freeze the deployed HA type, supported read-only interface, non-echoing
credential injection, endpoint/TLS trust, bounded queries, and sanitized
private evidence contract. Unsupported access, unexpected schema, credential
uncertainty, privacy risk, or cleanup uncertainty stops without fallback or
rollback. See [PE4_HOME_ASSISTANT_ACCESS_PRIVACY_CONTRACT.md](PE4_HOME_ASSISTANT_ACCESS_PRIVACY_CONTRACT.md).

PE-3 Action 10 requires no production operator action. Transport staging is
already absent and ceased to be authoritative after Action 6 immutable
publication and Action 7 configuration activation. The governed disposition is
`NOOP_ALREADY_ABSENT`: do not access PI3 merely to recheck it, recreate it,
retransmit the dataset, or delete any path. Action 8 and Action 9 evidence are
preserved records, not Action 10 inputs.

Action 10 is **COMPLETE** through administrative repository-only closure;
Actions 1–10 and PE-3 are **COMPLETE**. No Action 10 shell command, PI3 or PI5
action, staging recreation or deletion, production mutation, or Evidence Report
was required. Rollback remained FALSE and was not performed.

The corrected Action 9 read-only production
validation returned `RESULT=PASS`, `ACTION9=COMPLETE`, and
`ROLLBACK_RECOMMENDED=FALSE`; preserve its private Evidence Report at
`/tmp/hioc-pe3-action9-Bb6vGrmm` unchanged. Preserve the successful Action 8
evidence at `/tmp/hioc-pe3-action8-eZxNGrKa` unchanged as well. No production
mutation or rollback occurred. Transport staging remains absent and dataset
retransmission remains unnecessary.

The accepted performance evidence is `12.467231` seconds and `146744` KiB total
peak child RSS, measured under an `UNVALIDATED` baseline and classified
`INSUFFICIENT_BASELINE`. Both historical targets were exceeded but are not
production-enforced. Action 9 remains the final PE-3 production validation and
its Evidence Report remains the final production evidence. No Action 10 command
exists or was executed.

The earlier attempted-but-incomplete Action 9 result and its read-only forensic
analysis remain historical chronology; they do not describe current status.

PE-3 Action 9 is a separately authorized read-only validation checkpoint owned
by `tools/hioc-pe3-action9-validate.sh`. Operators must supply the approved full
governance commit and the exact preserved Action 8 PASS evidence path. The tool
validates evidence provenance/content, current artifacts, privacy, performance,
and protected-state equality, then creates only private invocation-owned Action
9 evidence and stops. It never regenerates outputs, uses `/usr/bin/time`, cleans
evidence or staging, performs rollback, or chains Action 10. Preserve every
reported Action 9 evidence directory for review.

Corrected Action 8 validator deployment is a dedicated, validator-only
checkpoint. The tool produces private invocation evidence and a backup path only
when replacement is required. It never restores automatically. Failures before
target mutation recommend no rollback; uncertain post-publication identity,
protected-state drift, or leftover publication temporary state recommends
operator rollback review. Manufacturer outputs, inventory, configuration, and
the selected immutable pair are read only and must compare exactly pre/post.

Private `manufacturer.json` and `manufacturer_status.json` outputs require exact
mode `0600`. The current `inventory.json` supplied to the manufacturer validator
is a separate input class: read bits may be broader, but group/world write bits
are prohibited. Do not chmod production outputs to work around a validation
failure. The third Action 8 attempt remains incomplete; its rollback advisory is
preserved and no rollback or rerun is authorized by this correction.

PE-3 replacement Action 8 bootstrap preparation stopped before PI3 execution
because the governed source-only trust gate referenced a superseded wrapper
blob. The corrected gate freezes the current reviewed wrapper Git blob while
retaining the operator-supplied governance commit and all clean fast-forward
barriers. It remains unprepared and unexecuted pending a separate post-push
checkpoint; it does not use runtime, manufacturer output, evidence, or transport
staging state.

The following governed Action 8 attempt retained sanitized exit `127` evidence
because `/usr/bin/time` was absent before generator execution could be proven.
Action 8 now uses governed Python for child launch and private elapsed/RSS
measurement. Operators must distinguish `GENERATOR_INVOCATION_FAILED` with
`generator_launch_status=UNCONFIRMED` from a confirmed generator-domain failure.
Neither result authorizes automatic rollback or continuation.

## PE-3 manufacturer dataset conflicts

The offline PE-3 builder may report an aggregate nonzero conflict count for
official assignment keys with multiple normalized organization variants. Such
keys remain in the private database as non-selectable conflict metadata without
organization values. `conflicting_assignment` is an unknown manufacturer result,
not an operational fault, and prevents fallback to a shorter prefix. Operators
must never manually select or patch a winner. IEEE source and generated database
artifacts remain local and outside Git and releases.

## PE-3 production deployment procedure

Production deployment is not an ad hoc shell session. Follow
[PE3_MANUFACTURER_PRODUCTION_RUNBOOK.md](PE3_MANUFACTURER_PRODUCTION_RUNBOOK.md)
one action at a time and return sanitized output after every action. The
supported final dataset path is
`/home/jazofv1/hioc/data/manufacturer/versions/local-ieee-ra--2026-08-11-r1/`.
Never transfer IEEE source CSVs, copy code manually into the runtime, overwrite
an immutable dataset version, silently replace a different configured path, or
interpret conflict/unknown counts as operational failure.

Action 1 accepts the retained external workspace only as an explicit Windows
operator variable. It resolves the exact manager-owned CPython 3.13 interpreter
through `pymanager list --one --format=exe --only-managed 3.13`, validates its
implementation/minor, and never uses default aliases or automatic installation.
Database/manifest selection is based on both frozen SHA-256 values, adjacency,
regular-file/reparse-point checks, and frozen sizes. Multiple identical matches
are selected lexically only after validation; zero matches fail with
`VALIDATED_BUILD_PAIR_NOT_FOUND`. No raw registry value or Windows user path is
printed.

The support state is `supported` with validated patch `3.13.15`; Action 1 is
ready to resume under separate authorization. It still fails closed with
`PYTHON_RUNTIME_SUPPORT_PENDING` if repository governance is not supported.
Action 1 disables Python Install Manager automatic installation. See
[PYTHON_RUNTIME_COMPATIBILITY.md](PYTHON_RUNTIME_COMPATIBILITY.md).

The separate installation/validation action is the repository-controlled
`tools/hioc-python313-validate.ps1`. It verifies its own approved Git identity,
installs through the official WinGet Python Install Manager package, uses
`pymanager` for non-launching management/list operations and the sole explicit
`pymanager install 3.13` mutation, then resolves and directly invokes the exact
managed 3.13 interpreter for the governed validation matrix. Automatic runtime
installation is disabled before any runtime
probe. Native manager stderr is captured and judged with its actual exit code,
so informational stderr with exit zero is not a failure and nonzero exit is.
An existing 3.14 runtime neither satisfies nor blocks the 3.13 checkpoint. It
returns sanitized evidence. It does not execute Action 1 or modify the support
manifest. The checkpoint is one-time evidence tooling and now refuses to run
because support has been promoted; it is not a recurring compatibility test.

The subsequent corrected run passed installation but stopped at
`PYTHON_PROBE`; this is a remaining runtime-invocation stderr-handling defect,
not compatibility evidence. A managed 3.13 runtime may therefore already be
present. The checkpoint now uses the manager's filtered authoritative inventory
to reuse one existing 3.13 entry, installs only when none exists, and fails
closed on malformed or ambiguous inventory. Git, WinGet, manager, runtime
probe, all tests, and compilation share the same exit-code-based native wrapper.

The official manager is present. An informal `py --help` diagnostic installed
CPython 3.14.7 through automatic default-runtime behavior; classify this as
`PYTHON_OPERATOR_DIAGNOSTIC_SIDE_EFFECT — UNINTENDED_DEFAULT_RUNTIME_INSTALL`,
not HIOC support or production state. Do not remove it in this checkpoint. The
safe manager dry run observed CPython 3.13.15 as the current candidate, while
the governed line remains floating 3.13.x and installation/validation remains
pending.

The most recent governed checkpoint result `FULL_REGRESSION_FAILED` is invalid
as compatibility evidence. An immediate direct governed-runtime run completed
506 tests with 13 skips and native exit code 0. The checkpoint had incorrectly
made a parsed `Ran` summary an acceptance gate while bounded capture could omit
the trailing unittest summary. The corrected script uses native exit status as
the acceptance authority and retains counts only for reporting. Do not promote
support until that corrected checkpoint itself passes.

The checkpoint still returned the same failure after that correction, while a
direct 508-test run and a direct run with the checkpoint pycache-prefix both
passed with 13 skips and exit code 0. The execution-wrapper mechanism therefore
remains under governed forensic investigation. Do not rerun the checkpoint.
After its commit is synchronized, run only the repository-controlled
`tools/hioc-python313-process-diagnostic.ps1` when separately authorized. It
compares direct and `ProcessStartInfo` behavior and never prints raw test output.

The diagnostic completed but equivalence failed: direct regression exited 0;
the same resolved `py` App Execution Alias launched by `ProcessStartInfo`
exited 1 after both stream tasks completed and before any unittest summary.
Checkpoint runtime execution now bypasses App Execution Aliases. It asks
`pymanager` for the exact managed 3.13 executable in `exe` format and invokes
that interpreter directly. Diagnostic completion and equivalence are reported
as separate results.

Final exact-interpreter isolation proved the remaining defect was
`ProcessStartInfo` itself: direct exact-interpreter execution passed both with
and without the checkpoint pycache prefix. Governed Python stages now use a
scoped PowerShell-native helper with temporary stream files, immediate
`$LASTEXITCODE` capture, restored error preference, bounded tails, and cleanup.
The process wrapper remains only for non-Python utilities.

Closure evidence: the corrected checkpoint passed on CPython 3.13.15 at commit
`6b622280a6f414d14ca3060da349423d92d664cb`, including 520 full-suite tests with
13 skips, 10 policy tests, 13 Action 1 tests, 119 manufacturer tests, compilation,
and repository cleanliness. Windows CPython 3.13.x is supported. The checkpoint
is one-time and intentionally refuses after promotion. CPython 3.14.7 remains
installed but unsupported pending a separate future disposition review.

For Windows PowerShell 5.1 operator tooling, informational native stderr is not
a failure criterion. Validation-critical native programs must run through the
governed wrapper and be judged by their actual exit code.

The hardened checkpoint subsequently reached the full regression. Its only
errors were three Bash-dependent network-probe governance tests attempting to
execute an unavailable fallback shell on Windows. They now skip individually
and visibly when Bash is absent, consistent with existing optional-tool tests;
the three platform-neutral checks still run, and all six original assertions
run when Bash is available. This correction does not weaken full-regression
failure handling or prescribe installing Bash on the operator workstation.

Action 1 is implemented only by the repository-controlled Windows PowerShell
script `tools/hioc-pe3-action1.ps1`; its source must never be reproduced through
chat. The runbook freezes the script SHA-256 and Git blob identity and provides
only the direct invocation model. Before artifact checks, the script verifies
the approved main/origin commit, its own path and Git identity, repository
cleanliness, and implementation ancestry. A script mismatch reports
`ACTION1_SCRIPT_IDENTITY_MISMATCH`.

Expected precondition and validation failures print a sanitized `RESULT` and
`ERROR_CODE`, then return from the script function. Unexpected exceptions are
caught as `ACTION1_UNEXPECTED_ERROR` with only a bounded `FAILURE_STAGE`. The
script contains no host-level `exit`, so the interactive PowerShell prompt
remains available for evidence capture.

## PE-3.1 manufacturer enrichment boundary

PE-3.1 executable tooling is repository implemented but not deployed. A future operator
obtains IEEE source files independently, records their SHA-256 values, and runs
an offline builder into an immutable local version directory under
`data/manufacturer/versions/`. HIOC never downloads, bundles, or redistributes
registry data. `MANUFACTURER_DB_PATH` is empty by default and a configured value
selects one local normalized database; its manifest is the fixed adjacent
`manufacturer-db.manifest.json`.

The future manually invoked `hioc-generate-manufacturer.py` reads completed
inventory and writes only private manufacturer sidecars. It has no schedule or
inventory hook. Install, upgrade, and rollback preserve local databases,
configuration, and sidecars. Production commands are deliberately deferred.
The binding operational, failure, locking, and rollback behavior is
[PE3_MANUFACTURER_EXECUTABLE_CONTRACT.md](PE3_MANUFACTURER_EXECUTABLE_CONTRACT.md).
The future standalone manufacturer validator is strictly read-only and acquires
no lock. Published database versions require no reader lock because the builder
atomically publishes a complete immutable directory. Runtime sidecar validation
observes independently loaded files and reports inconsistencies without repair.
Only the offline builder and manual generator own manufacturer-specific locks.

PE-3 production sequencing separates transferred-artifact staging from source
identity. Action 3 verifies only PI3 identity and the exact private staging pair.
Action 4 owns the clean release-source fetch/fast-forward and, only afterward,
proves implementation ancestry and protected validator identity, rechecks the
staged hashes and sizes, and invokes the read-only validator. This ordering
allows a stale clean checkout to synchronize without permitting an unverified
validator or any deployment. Action 5 remains the first code-deployment action.

The first Action 3 attempt stopped because its historical block required the
implementation commit before the synchronization action could fetch it. Its
bare assertions under interactive `set -euo pipefail` also terminated the
operator shell. Recovery confirmed the PI3 target and staging directory were
intact and that owner, mode, exact contents, regular-file status, sizes, and
hashes passed. The corrected Action 3/4 function blocks emit bounded
`RESULT`, `ERROR_CODE`, and `FAILURE_STAGE` evidence and return control without
shell-level `errexit`. The accepted staging evidence is preserved; the restart
point is Action 4 after the sequencing-correction commit is approved and pushed.

The first corrected Action 4 synchronized the source and passed implementation
identity, staging type, size, and digest checks, then the approved validator
correctly rejected both staged files at mode `0644`. The frozen database,
manifest, sidecar, and status mode is `0600`; a private `0700` directory alone
does not make permissive files acceptable. Action 4 owns bounded pre-validation
normalization because it is the first point where synchronized implementation
identity and staged content identity are jointly proven.

Permission repair is allowed only for the exact two regular non-symlink files,
owned by `jazofv1:jazofv1`, inside the exact `0700` staging directory containing
no other entries, after frozen sizes and hashes pass. Only `0600` or observed
transport mode `0644` is eligible. After `chmod 0600`, modes and hashes must be
rechecked before validator retry. Transport success and checksums do not imply
permission safety; type, symlink status, ownership, size, digest, and mode are
separate staging invariants. Normalization is allowed only inside an explicitly
governed staging/install transaction after identity proof.

The Action 4 resume implementation is now owned by
`tools/hioc-pe3-action4-resume-permissions.sh`, not chat. It revalidates every
directory and file invariant after normalization, enforces the validator JSON
result/privacy/count contract, and emits a distinct PASS barrier for source,
staging, normalization, post-normalization identity, validator, and Action 4.

The first invocation exposed a separate availability prerequisite: PI3 release
source remained at `653f887a643c877a8f611145c8b8e9f92a65b6cd`, predating the
script. A repository-controlled operator script must never be invoked until the
target repository is fast-forwarded to the exact approved governance commit and
the script's Git object and worktree identities are verified. Source repository
synchronization and script availability are preconditions, not deployment.
They are also a separate trust boundary from execution: Action 4A proves the
script is available and stops; it must never auto-chain into mutating Action 4B.
Action 4B requires reviewed Action 4A PASS and separate authorization. Bootstrap
actions must remain runnable when the target predates the tool they make
available.

Action 5 is the first production mutation and is implemented only by
`tools/hioc-pe3-action5-deploy.sh`. The operator passes the exact approved
post-push governance commit; the script proves target, source, self, and governed
artifact identity before running release validation. It then invokes only the
supported `release/upgrade.sh` flow, proves the timestamped backup, validates the
runtime and deployed artifact identities, and confirms configuration and the
manufacturer dataset were untouched. Every barrier emits explicit sanitized
PASS evidence. A bounded failure reports result, code, stage, and whether
rollback is recommended without terminating the parent terminal or automatically
running rollback. Action 6 always requires separate review and authorization.
The governed script identity is SHA-256
`7cc9e0b7a0c3b06055b329cafdf71fe55ae362a8c1e67b870d8c04655771c690`, Git blob
`b493be45d42c7732f353519beec23fa62d45a942`.

Because PI3 may predate the commit introducing or modifying that script, Action
5 is split into two separately authorized trust boundaries. Bootstrap-safe
Action 5A performs only target identity, clean exact fast-forward, synchronized
HEAD, and Action 5 script Git/worktree identity proof, then stops. Only after
reviewed Action 5A PASS may Action 5B invoke the governed deployment script.
Action 5B remains the first production mutation and alone may emit
`ACTION5=COMPLETE`.

Action 5 protection is semantic. Installer-managed creation or `0700`
normalization of empty, real, correctly owned manufacturer scaffolding is
permitted before Action 6. Any installed-version, database, manifest,
sidecar/status, symlink, unexpected-entry, payload identity, or configuration
change remains a failure. The first Action 5B run exposed the former recursive-
fingerprint false positive after deployment/runtime validation passed; rollback
is not recommended. Closure uses the separately bootstrapped, read-only
`tools/hioc-pe3-action5c-revalidate.sh`, not a repeat deployment. Action 5C-A
is the inline target synchronization and exact script-identity gate; it stops
after PASS. Action 5C-B is the separately authorized read-only closure and may
not be prepared or invoked until that PASS is reviewed.

Any production action containing multiple validations and mutations must be a
repository-controlled operator script unless a smaller inline procedure has
been explicitly validated for interactive use. Authoritative runbooks contain
the exact production-validated command: no shorthand, unresolved placeholder,
or reconstructed equivalent is permitted.
Every repository-controlled production operator script requires a target-side
bootstrap prerequisite whenever the target may predate the commit that added or
changed it. Synchronization proof and script execution are always separate
authorization boundaries. This applies equally to read-only closure and
revalidation scripts: absence of production mutation does not collapse their
synchronization, identity, review, or authorization boundaries.

PE-3 Action 6 immutable dataset installation is owned exclusively by
`tools/hioc-pe3-action6-install.sh`. The retired inline block was not
production-safe: it contained an unresolved staging placeholder, interactive
strict mode and exit, bare assertions, and incomplete evidence. Action 6-A is a
separate bootstrap synchronization/script-identity gate and must stop after
PASS. Action 6-B then verifies the exact preserved staging directory
`/tmp/hioc-pe3-dataset-transfer-PJ5qPbRS`, validates the pair, publishes only by
same-filesystem no-replace atomic rename, and proves configuration unchanged.
It never activates the dataset; Action 7 requires full reviewed Action 6 PASS.

PE-3 Action 7 configuration activation is owned exclusively by
`tools/hioc-pe3-action7-activate.sh`. The retired inline procedure was not
production-safe because it used interactive strict mode and exits, an unresolved
evidence path, and incomplete identity, backup, post-publication, and rollback
evidence. Action 7-A separately synchronizes the clean release source and proves
the activation script's Git/worktree identity, then stops. Separately authorized
Action 7-B changes only `MANUFACTURER_DB_PATH` in `config/hioc.conf`, selecting
the exact installed immutable `local-ieee-ra--2026-08-11-r1` database after
identity and validator PASS. It creates a private durable exact backup only when
activation is required, publishes atomically, validates the selected value and
dataset afterward, and never reloads a service or chains Action 8. Duplicate or
different nonempty values fail closed. Rollback is never automatic and is
recommended only after publication if durability or post-validation fails.

PE-3 Action 8 protected generation is owned by
`tools/hioc-pe3-action8-generate.sh`. The retired inline block was not
production-safe: it used interactive strict mode, a pipefail-sensitive `tee`
pipeline, an unresolved evidence path, bare assertions, and incomplete identity,
publication, failure, and rollback evidence. The governed wrapper invokes only
the established manual generator after proving target/source/runtime identity,
the Action 7 configuration selection, exact immutable dataset, inventory,
output preconditions, and private evidence
state. It validates both generated private artifacts and protected domains after
generation, publishes only aggregate private evidence, and never deploys,
reloads services, changes schedules, cleans staging, or chains Action 9. A
separately authorized bootstrap gate is required because the PI3 source predates
this script. That parent-shell-safe gate performs only clean fast-forward source
synchronization to an explicitly supplied, validated, operator-approved full
40-hex post-push governance commit and exact script Git/worktree identity proof,
then stops without reading production state or transport staging. The commit is
never inferred or frozen before its governing correction is published.

Action 8 does not consume or reuse Action 5/5C evidence. Its child wrapper
creates a unique mode-`0700`, `jazofv1:jazofv1`, invocation-owned
`/tmp/hioc-pe3-action8-XXXXXXXX` directory only after all read-only preconditions
pass. The directory path is emitted on PASS and on later failures where it was
safely created. Operators must return that exact path and preserve it for the
next authorized boundary; arbitrary discovery, substitution, recreation, and
wildcard cleanup are prohibited.

Transport staging is transient transfer state required through Action 6
installation, not an Action 8 input. After reviewed immutable publication and
Action 7 activation, Action 8 relies on the exact installed database/manifest and
configuration selection. It accepts staging absence, never reads or recreates
staging, and retains fail-closed configuration and installed-dataset drift checks.

After the first corrected Action 8 attempt returned a nonzero generator exit,
forensics proved that the wrapper deleted its structured stdout capture and
discarded stderr, leaving no attributable root cause. The corrected failure path
now publishes private sanitized `generation-performance.txt` followed by
result-last `generation-failure.json`. Raw stdout/stderr remain private temporary
captures and are removed; they are never printed or copied into evidence.
Operators must stop and preserve the exact evidence directory after either PASS
or failure. The changed wrapper requires a new bootstrap identity gate before a
future separately authorized Action 8 attempt.

## Known Dangerous Operator Patterns

Operational instructions must state the exact target machine and shell and must
contain the exact validated command. Substantial programs belong in versioned,
repository-controlled scripts; chat is never their sole authoritative copy.
Copy/paste behavior is part of validation, including an intentional harmless
failure proving sanitized evidence, suppression of later stages, survival of
the parent terminal, and return of its prompt.

- PI3 interactive HIOC validation blocks must not enable `set -e`, `set -u`,
  `set -o pipefail`, or `set -euo pipefail` as prerequisites: failed validation
  must preserve the operator's active SSH shell and return its prompt. Do not
  use `exit` or `exec` in these blocks. Capture and report explicit return codes;
  redirect long or diagnostic test output to a bounded or named log when
  appropriate and inspect it separately. A nonzero test result stops lifecycle
  advancement without intentionally terminating the shell. Never chain D-PREP
  or a later action automatically after a test or validation command.
  This operator-safety rule creates no production script or shell framework.
- `grep -q` and pipelines under `pipefail` can report failure because an
  upstream writer receives SIGPIPE after a match. Use an explicitly tested
  bounded check whose authoritative status is unambiguous.
- Shell-level `exit` closes the operator session. Governed scripts may return a
  process status; pasted functions must `return` and preserve the prompt.
- Large pasted implementation blocks are vulnerable to formatting and partial
  delivery. Invoke the checked-in script by its short frozen command instead.
- PowerShell `if`/`else` fragments pasted separately can execute incompletely.
  Use one repository script or one syntactically complete bounded invocation.
- Windows App Execution Aliases are not proof of an installed runtime and may
  return `9009`. Resolve only the governed managed interpreter.
- Windows PowerShell 5.1 can turn native stderr into error records. Governed
  wrappers must use the actual native exit status and tested stderr handling.
- `ProcessStartInfo` can disagree with direct governed Python execution because
  of environment, stream, or argument behavior. HIOC uses the validated direct
  launcher model for governed Python checks.

## Document Ownership

This is the authoritative operational and runtime reference. It defines how current components run, what they produce, and how operators validate and recover them. The current deployed-system overview is in [SYSTEM_REFERENCE.md](SYSTEM_REFERENCE.md); deployment mechanics are in [DEPLOYMENT.md](DEPLOYMENT.md).

## Runtime Health Principle

HIOC runtime is cron-driven, using short-lived jobs protected by `flock`. A healthy deployment should not be expected to show persistent HIOC processes. Health is determined through cron availability, expected entries, fresh status artifacts, successful scheduled output, logs, generated state, and safe manual execution when required.

The confirmed trigger is the `jazofv1` user crontab. Every listed command uses `flock -n`: if another live execution owns the lock, the new invocation exits instead of waiting. A lock-path file may remain after a run; its presence alone does not mean a job is stuck because the lock is held by a live file descriptor.

## Deployed PE-1 Operational Boundary

PE-1 is **complete and production validated**. Its private production sidecars
are `state/inventory/enrichment.json` and
`state/inventory/enrichment_status.json`. PE-1 runs inside the existing
Inventory Engine schedule and lock, adds no cron job or network acquisition,
and publishes neither artifact over MQTT.

Enrichment failure is isolated from
authoritative inventory generation: public inventory remains valid, the last
valid enrichment envelope remains untouched, and a sanitized local status
records the PE-1 failure without changing device health or creating an
incident. Detailed schema, permissions, validation, evidence, and rollback
requirements are in
[PE1_HOSTNAME_ENRICHMENT_SPEC.md](PE1_HOSTNAME_ENRICHMENT_SPEC.md). Corrected
production validation reported status `online`, 153 records, 83 candidates, 82
selected candidates, and zero conflicts. Missing optional source types,
historical candidates, or conflicts are not failures. The public inventory and
all existing consumer, identity, canonical-address, health, liveness, incident,
topology, and service-ownership contracts remained protected.

## Deployed PE-2.1 Operational Boundary

PE-2.0 and the PE-2.1 implementation design are approved; PE-2.1 is implemented,
repository validated, deployed, and production validated.
The local artifacts are
`state/inventory/assets.json` and
`state/inventory/assets_status.json`. A dedicated local CLI—not manual JSON,
MQTT, Home Assistant, dashboards, or an API—will own validated edits under
`/tmp/hioc-assets.lock`, create a validated timestamped backup before each
mutation, and write atomically with restrictive modes. It will read current
inventory only for stable-ID/orphan context and will never mutate or block the
Inventory Engine. The complete contract is in
[PE2_ASSET_FOUNDATION_SPEC.md](PE2_ASSET_FOUNDATION_SPEC.md).

Asset data will remain local and deny-by-default. Missing, empty, or orphaned
Asset metadata will not affect health, liveness, incidents, or any public
consumer. Governed production deployment/validation is prepared in
`tools/hioc-pe2-production-validate.sh`; it must be invoked only through the
approved target/repository bootstrap after its governance commit is pushed.
Preparation does not authorize Codex access, deployment, or production action.
The initial deployment completed, but its validator stopped on a repository-mode
versus runtime-mode contract defect before synthetic validation. The deployed
implementation remains in place with approved restrictive modes. Corrected
validation must use `--revalidate-existing-deployment`; that mode never invokes
`release/upgrade.sh` and produces a new protected evidence directory.

Incident protection for this revalidation is a positive contract, not live-file
digest equality. `tools/validate_pe2_incident_contract.py` validates JSON and
required shape, absence of Asset metadata and synthetic values, and structural
Asset-to-incident isolation. Normal lifecycle, title, telemetry, history, or
summary movement is operational drift. Uncertainty is `VALIDATION_FAIL` with
rollback false; rollback requires a deterministic PE-2-caused regression.

One-time PE-2 residue cleanup uses the committed six-entry manifest and
`tools/hioc-pe2-clean-synthetic-backups.py`. Run validation-only first, then
delete only after every entry passes basename, containment, regular-file,
non-symlink, ownership/mode, SHA-256, JSON, authoritative schema, and synthetic-
only checks. Wildcard, timestamp-range, and discovered-backup deletion are
prohibited. Current state, the backup root, and every unlisted operator backup
are outside scope. Cleanup and final revalidation are separate actions.

Final validation reported deployed-and-validated status, passing Asset and
protected invariants, passing privacy and performance, complete current-run
synthetic cleanup, and incident operational drift without causal PE-2 regression.
No rollback occurred or was required. Evidence is retained at the sanitized
reference `/tmp/hioc-pe2-production-validation-CtZ4WHUN`.

## Canonical Schedule

| Component | Cron expression | Plain-language schedule | Lock |
| --- | --- | --- | --- |
| Daily Maintenance | `15 3 * * *` | Daily at 03:15 | `/tmp/daily-maintenance.lock` |
| Resource Monitor | `*/15 * * * *` | Every 15 minutes | `/tmp/resource-monitor.lock` |
| UPS Monitor | `* * * * *` | Every minute | `/tmp/ups-monitor.lock` |
| DNS Watchdog | `* * * * *` | Every minute | `/tmp/dns-watchdog.lock` |
| PI4 MQTT Health Publisher | `*/1 * * * *` | Every minute | `/tmp/pi4-mqtt-health.lock` |
| HIOC Network Probe | `*/5 * * * *` | Every 5 minutes | `/tmp/hioc-network-probe.lock` |
| HIOC History Engine | `*/5 * * * *` | Every 5 minutes | `/tmp/hioc-history-engine.lock` |
| HIOC Inventory Engine | `*/30 * * * *` | Every 30 minutes | `/tmp/hioc-inventory-engine.lock` |
| HIOC Platform Status | `17 3 * * *` | Daily at 03:17 | `/tmp/hioc-platform-status.lock` |
| HIOC Incident Engine v2 | `*/1 * * * *` | Every minute | `/tmp/hioc-incident-engine.lock` |

All expected runtimes are **Not yet formally baselined**. A future baseline should use timestamped production measurements across normal and degraded conditions and must not be guessed from cron frequency.

The confirmed crontab lines do not redirect stdout or stderr. Repository-managed Inventory and Platform Status jobs log internally to their documented files; Incident Engine v2 emits publication failures to stderr; History Engine may expose uncaught output through cron. Whether host cron mails, journals, or discards otherwise uncaptured output requires production verification. External toolkit logging also requires production verification.

## External Pi4 Toolkit Jobs

The following six scripts are confirmed production components under `/home/jazofv1/pi4-tools`. The network probe is now governed at `pi4-tools/scripts/hioc-network-probe.sh`; the other five implementations remain outside this repository pending complete source intake. Their names, paths, schedules, triggers, and locks are verified; detailed output, log, and recovery contracts require production verification.

### Daily Maintenance

- **Purpose:** External Pi4 toolkit maintenance; exact operations require production verification.
- **Schedule/trigger/lock:** `15 3 * * *`, `jazofv1` crontab, `/tmp/daily-maintenance.lock`.
- **Command:** `/home/jazofv1/pi4-tools/daily-maintenance.sh`.
- **Outputs/status/logs:** Not yet documented in this repository.
- **Recovery:** Inspect cron, lock ownership, toolkit configuration, and existing output before any manual run. Do not delete the lock path blindly.
- **Validation:** Confirm cron is active, entry exists, and production-defined maintenance evidence is current. Exact success artifact requires production verification.

### Resource Monitor

- **Purpose:** External Pi4 resource monitoring; metric and output contract requires production verification.
- **Schedule/trigger/lock:** `*/15 * * * *`, `jazofv1` crontab, `/tmp/resource-monitor.lock`.
- **Command:** `/home/jazofv1/pi4-tools/scripts/resource-monitor.sh`.
- **Outputs/status/logs:** Not yet documented in this repository.
- **Recovery:** Validate configuration and current cron/output evidence before a one-time run.
- **Validation:** Cron entry plus recent repository-external telemetry or artifact; exact artifact is TBD pending production verification.

### UPS Monitor

- **Purpose:** External UPS telemetry used by HIOC incident/history inputs; detailed UPS inventory is not documented.
- **Schedule/trigger/lock:** `* * * * *`, `jazofv1` crontab, `/tmp/ups-monitor.lock`.
- **Command:** `/home/jazofv1/pi4-tools/scripts/ups-monitor.sh`.
- **Outputs/status/logs:** Repository consumers can read toolkit UPS state and MQTT telemetry; the producer contract requires production verification.
- **Recovery:** Inspect NUT health, toolkit configuration, current telemetry, and lock ownership before manual execution.
- **Validation:** NUT reachable, cron present, and recent UPS telemetry available.

### DNS Watchdog

- **Purpose:** External DNS watchdog; corrective behavior and output contract require production verification.
- **Schedule/trigger/lock:** `* * * * *`, `jazofv1` crontab, `/tmp/dns-watchdog.lock`.
- **Command:** `/home/jazofv1/pi4-tools/scripts/dns-watchdog.sh`.
- **Outputs/status/logs:** Not yet documented in this repository.
- **Recovery:** Validate Pi-hole, Unbound, and DNS resolution before considering configuration repair or a one-time run.
- **Validation:** Cron present, DNS resolution succeeds, and any production-defined watchdog evidence is current.

### PI4 MQTT Health Publisher

- **Purpose:** Publishes Pi4 toolkit health telemetry consumed through the legacy MQTT base topic.
- **Schedule/trigger/lock:** `*/1 * * * *`, `jazofv1` crontab, `/tmp/pi4-mqtt-health.lock`.
- **Command:** `/home/jazofv1/pi4-tools/scripts/publish-mqtt-health.sh`.
- **Outputs/status/logs:** MQTT outputs are external to this repository; HIOC consumers use configured legacy topics. Exact publisher topic set requires production verification.
- **Recovery:** Validate broker connectivity and toolkit configuration without exposing credentials, then perform a safe one-time run only under operator control.
- **Validation:** Cron present and expected retained or recent toolkit health telemetry is readable.

### HIOC Network Probe

- **Purpose:** Produces network observations consumed by HIOC history and incident processing.
- **Schedule/trigger/lock:** `*/5 * * * *`, `jazofv1` crontab, `/tmp/hioc-network-probe.lock`.
- **Command:** `/home/jazofv1/pi4-tools/scripts/hioc-network-probe.sh`.
- **Outputs/status/logs:** The governed probe publishes legacy MQTT network
  state and inventory. Production validation at approved commit
  `e06539d9bece040d721b9912213559cc54f1610d` confirmed retained PI5 online
  state and Pi5 inventory identity at the configured address.
- **Recovery:** Inspect gateway, DNS, Internet, MQTT, configuration, and current telemetry before a manual run.
- **Validation:** Cron present and network latency/loss/DNS/MQTT observations
  update as expected. On 2026-07-30 the Git blob, Linux worktree, and deployed
  target matched; syntax, owner, group, mode, connectivity, publication,
  inventory, and incident recovery passed. Backup
  `hioc-network-probe.sh.20260730T203740.backup` was created; rollback was not
  required.

## HIOC Repository-Managed Jobs

### HIOC History Engine

- **Purpose:** Samples legacy MQTT network metrics and local host metrics, appends history CSVs, computes forecast/statistics JSON, and publishes retained history outputs.
- **Schedule/trigger/lock:** `*/5 * * * *`, `jazofv1` crontab, `/tmp/hioc-history-engine.lock`.
- **Command:** `/home/jazofv1/hioc/pi4/bin/hioc-history-engine.py`.
- **Outputs:** `history/network.csv`, `history/host.csv`, `state/forecast.json`, `state/statistics.json`, and retained forecast/statistics/history-status MQTT topics.
- **Status/logs:** `state/history_status.json` with known fields `status` and `updated`. No dedicated repository-derived log filename; cron handling of uncaught output requires production verification.
- **Recovery:** Read-only inspect status, CSV/JSON freshness, broker/config dependencies, and cron. A manual one-time execution is supported only after confirming no live lock owner.
- **Validation:** Status `online`, timestamp fresh relative to the five-minute schedule, JSON valid, history advances, and expected MQTT data is available.

### HIOC Inventory Engine

- **Purpose:** Collects passive inventory evidence, reconciles canonical devices/services, writes inventory projections and events, and publishes retained inventory MQTT state.
- **Schedule/trigger/lock:** `*/30 * * * *`, `jazofv1` crontab, `/tmp/hioc-inventory-engine.lock`.
- **Command:** `/home/jazofv1/hioc/pi4/bin/hioc-inventory-engine.py`.
- **Outputs:** `state/inventory/inventory.json`, `devices.json`, `services.json`, `capabilities.json`, `topology.json`, `dependencies.json`, `summary.json`, `status.json`, and internal events under `state/events/events.json`.
- **Status/logs:** `state/inventory/status.json`; `logs/hioc-inventory-engine.log` from the repository logger. July 29 point-in-time logs showed successful `devices=150 services=8` updates.
- **Recovery:** Inspect status, log, source availability, config, and JSON first. Run once manually only when no execution owns the lock. Deployment repair uses supported release tooling.
- **Validation:** Cron present; status and inventory artifacts valid and fresh; expected source state truthful; current log has successful updates; deployed validator passes.

Canonical IPv4 is the inventory engine's deterministic representative address
for one reconciled MAC-backed identity. It is not complete address history and
does not prove reachability, health, or online status. Strong current or
configured evidence may outrank DHCP; active DHCP outranks `STALE` neighbor
evidence for the same MAC; `FAILED` and `INCOMPLETE` cannot become preferred
operational addresses. Equal evidence uses explicit lease, observation, and
numeric-address tie-breaks rather than collection order. Static devices remain
supported. Production investigation compares DHCP leases, `ip neigh`, the
canonical inventory record, stable ID, sources, and health fields without
treating a lease as a liveness check. See the
[Canonical Address Selection Hardening Evidence Report](CANONICAL_ADDRESS_HARDENING_EVIDENCE.md).

Canonical-address production validation must admit only same-MAC active DHCP
IPv4 versus different `STALE` neighbor IPv4 cases and must exclude local-host,
gateway, configured-integration, `REACHABLE`, and `PERMANENT` evidence. IPv6
and non-canonical address classes cannot qualify. `NO_QUALIFYING_CANDIDATE`
means the deployment and general invariants may pass without a current direct
reproduction; it is not failure and does not justify rollback. Only a
qualifying stale IPv4 that still wins, or an independent deployment/invariant
failure, is `FAIL`.

When retired-address DHCP evidence is found, inspect configured
`HIOC_INVENTORY_DHCP_LEASE_FILES`, readable lease rows and expiry values,
non-secret Pi-hole/dnsmasq reservation definitions, DHCP logs, and neighbor
evidence before classifying or changing it. Evidence collection must not alter
DHCP or network configuration.

The revised validator invariant document has a strict schema. Required Boolean
keys are `artifact_identity`, `unique_mac_identity`,
`inventory_count_consistent`, `health_and_liveness_fields_present`,
`stable_identity_fields_present`, and
`bounded_unrelated_canonical_changes`. All must exist and be JSON Booleans.
Only required `false` values fail an invariant. Keys beginning with `_` are
diagnostic metadata and may contain zero, counts, null, or strings without
affecting the outcome. Missing or mistyped required keys and unexpected
non-underscore keys are explicit input failures.

Production closure passed with strict-validator result
`NO_QUALIFYING_CANDIDATE`: all six Boolean invariants passed, diagnostic counts
were preserved separately, inventory remained at 151 devices, and one
unrelated canonical-address change remained within the bounded invariant.
Comparator source and runtime matched Git-derived SHA-256
`35f36916399331a6e1129f7a49ba86933960eca8e94d6b30c80e9be3d7cd75b8`.
No rollback was recommended or performed. The unexpired `.152` old lease and
its lack of renewal during the bounded 60-second observation remain separate
DHCP cleanup evidence; `.251` had stronger current `REACHABLE` and configured
integration evidence.

### HIOC Platform Status

- **Purpose:** Reads `VERSION.yaml`, builds platform version/status documents, writes local state, and publishes retained platform MQTT topics.
- **Schedule/trigger/lock:** `17 3 * * *`, `jazofv1` crontab, `/tmp/hioc-platform-status.lock`.
- **Command:** `/home/jazofv1/hioc/pi4/bin/hioc-platform-status.py`.
- **Outputs/status:** `state/platform/version.json` and `state/platform/status.json`; retained `platform/version` and `platform/status` MQTT topics.
- **Logs:** `logs/hioc-platform-status.log`.
- **Recovery:** Distinguish historical from current errors, validate `VERSION.yaml` and config, inspect fresh state, and run once only when safe.
- **Validation:** JSON valid, successful current log entry, version matches manifest, and status is fresh relative to the daily schedule.

The log retains July 4 through July 12 historical failures caused by `TypeError: Logger._log() got an unexpected keyword argument 'hioc_version'`. Later successful executions establish that this is resolved historical evidence, not a current failure. Do not erase the old entries.

### HIOC Incident Engine v2

- **Purpose:** Reads telemetry, inventory, and events; correlates incidents; advances lifecycle; writes incident/timeline state; and publishes the retained incident contract.
- **Schedule/trigger/lock:** `*/1 * * * *`, `jazofv1` crontab, `/tmp/hioc-incident-engine.lock`.
- **Command:** `/home/jazofv1/hioc/pi4/bin/hioc-incident-engine-v2.py`.
- **Outputs:** `state/incidents/active.json`, `history.json`, `summary.json`, `timeline.json`, `latest_event.json`, `state/incident_engine_status.json`, events, and retained incident/status MQTT topics.
- **Status/logs:** `state/incident_engine_status.json` with known fields `status`, `version`, and `updated`; shared `logs/hioc.log` is produced by shell/common runtime paths, while Python stderr handling depends on cron. No separate v2 log path is established.
- **Recovery:** Inspect incident status/state, current cron output, MQTT dependency, config, and event/inventory inputs. A required publication failure returns nonzero and must be investigated or handled through supported deployment rollback.
- **Validation:** Status `online`, version correct, timestamp fresh relative to one minute, incident JSON valid, cron entry present, and retained MQTT validator passes when broker validation is required.

## Dated Production Evidence: 2026-07-29

- `cron`: active.
- History engine: online at `2026-07-29T20:25:00-06:00`.
- Incident Engine v2: online, version `1.2.0`, at `2026-07-29T20:27:28-06:00`.
- Inventory engine: recurring successful 30-minute updates; point-in-time count 150 devices and 8 services.
- HIOC deployment validation: **PASS**.
- Port `8091` belonged to Z-Wave JS UI, not HIOC. No HIOC dashboard endpoint was confirmed.

## Safe Operational Validation

1. Confirm cron service is active and expected `jazofv1` entries are present.
2. Inspect lock ownership, not merely lock-path existence.
3. Validate current JSON and timestamps against the component interval.
4. Inspect current log tail while preserving historical evidence.
5. Check generated state and configured external dependencies.
6. Use a manual one-time run only when it will not overlap and its side effects are understood.
7. Use `pi4/validate_pi4.sh` and checkpoint-specific validators.
8. Use supported deployment or rollback for file repair; do not patch the runtime ad hoc.

## Git-Governed Deployment Artifact Identity

The authoritative bytes of a Git-governed deployment artifact are the raw Git
blob at the exact approved commit and repository-relative path. Editor buffers,
temporary copies, uncommitted or platform-normalized worktrees, generated
intermediates, and pre-commit versions are never authoritative.

Use `tools/git_artifact_manifest.py APPROVED_FULL_COMMIT PATH
--compare-worktree` to derive identity. Record the full commit, path, Git blob
ID, Git-derived SHA-256, byte length, mode, and worktree comparison together.
The deterministic output has no timestamp and never accepts a supplied
checksum.

Network-probe deployment uses
`pi4-tools/deploy-network-probe.sh APPROVED_FULL_COMMIT
pi4-tools/scripts/hioc-network-probe.sh`. Synchronization is a separate
prerequisite. The helper requires a clean checkout at the exact full commit, a
tracked executable blob, byte-equal source, valid Bash syntax, a successful
timestamped backup, and byte-equal deployed target. It reports blob, worktree,
and deployed checksums plus the backup path. Do not add an
`EXPECTED_SOURCE_SHA` constant to operator instructions.

All deployment evidence must be regenerated after the final commit and push
from the exact `origin/main` Git object. No pre-commit checksum may appear in
operator instructions, and no manually transcribed checksum may be the sole
artifact identity. An Evidence Report must include approved commit, path, blob
ID, Git-derived SHA-256, worktree comparison, deployed checksum, and
source-to-target byte identity. Repository PASS is prohibited until this
post-push evidence is regenerated.

Deployment correctness and downstream incident recovery are separate
validation domains:

- **PASS:** deterministic deployment and downstream recovery both validated.
- **PARTIAL PASS:** deployment validated while recovery was delayed or
  inconclusive and requires separate downstream-state follow-up.
- **FAIL:** deterministic deployment validation failed.

Delayed recovery, stale presentation, retained state awaiting replacement, or
debounce/polling delay is not by itself a rollback reason. Do not roll back a
byte-identical, valid deployment solely because bounded incident observation
did not converge. The operator procedure captures and validates the helper's
actual timestamped backup and prints, but never automatically executes, a
rollback command reserved for justified deterministic failure.

## Operations Acceptance Standard

The permanent actionable release checklist is in [HIOC_MASTER_PLAN.md](HIOC_MASTER_PLAN.md#operations-acceptance-standard). Operations documentation must allow an operator to answer what exists, why, how it runs, how it is validated, and how it is recovered without rediscovering the system through SSH.
# PE-4.0B.2a dependency/runtime boundary

Do not run the capability client with an ambient interpreter. The future
governed invocation must use
`/home/jazofv1/hioc/runtime/pe4/active/bin/python` after a separately authorized
deployment and complete credential-free preflight. The exact dependency,
offline artifact, permissions, active-pointer, evidence, and rollback contract
is in `PE4_ISOLATED_RUNTIME_DEPENDENCY_CONTRACT.md`. This checkpoint supplies no
operator installation, deployment, authentication, or client command.

Lifecycle actions A-G and rollback are defined in
`PE4_ISOLATED_RUNTIME_LIFECYCLE.md`. Never chain them. A PASS means preserve its
sanitized Evidence Report and STOP for the next authorization. General release
rollback is not PE-4 environment rollback; use only the separately governed
PE-4 pointer rollback after exact eligibility review.

Action A production PASS establishes the durable cache prerequisite. Action B
accepts neither the Action A evidence path nor an operator-selected artifact.
It independently verifies the fixed cache and preserves its PI3 transfer
directory on every post-creation outcome. Return every bounded state marker and
`TRANSFER_DIRECTORY`, then STOP; never chain cleanup, route proof, or install.

Do not manually move, rename, delete, or reconcile Action B remote content.
The tool exclusively creates its result temporary file with no-follow semantics
and publishes the wheel, lock, and result with
`renameat2(RENAME_NOREPLACE)`. Every destination entry is a collision. Accept a
normal return or uncertain rename error only when the exact final object and
durability confirm and the invocation-owned source is absent under
non-following inspection. Retained source state, wrong content or metadata, or
indeterminate absence requires STOP with the preserved transfer directory.
After any result publication attempt, no second result may be attempted.

Do not substitute SCP or an operator-created partial file. Action B sends the
wheel and lock as bounded SSH stdin to its exclusive remote sink; collision or
interruption preserves the private directory and leaves the corresponding
transfer marker false. Preflight must pass the fixed Windows operator/profile,
SSH executable digest, key pair/fingerprint/comment, and numeric PI3 host-key
fingerprint. Evidence state `UNCERTAIN` means publication may have completed
but confirmation was unavailable: preserve everything and STOP. It is neither
confirmed success nor proof that no result exists.

Do not add SSH config, proxy, jump-host, identity, or known-host overrides around
Action B. The tool deliberately reads no SSH configuration and uses only the
fixed current-profile `.ssh/known_hosts` and `.ssh/id_ed25519` after rejecting
missing, empty, symlinked, or reparse-point material. Missing prerequisites are
a bounded STOP, not permission to generate keys, scan hosts, or change files.
Evidence is accepted only after exact post-rename confirmation.

Action A is a Windows-only repository tool. Its result must include all five
acquisition/publication state markers. A failure with
`DURABLE_CACHE_PUBLISHED=TRUE` means preserve the cache and evidence state and
STOP; never redownload, delete, or begin transfer without review.

The first Action A attempt returned `COMMAND_FAILED/WORKSTATION_ACL` before
network access and left only an ordinary inherited-ACL `HIOC` directory. Do not
delete it or repair it manually. The corrected helper accepts it only as the
expected real, non-reparse LocalApplicationData child, then uses .NET ACL APIs
to remove inheritance and all prior Allow/Deny ACEs before installing and
validating the single governed SID rule. Bounded ACL errors distinguish read,
protection, rule update, application, validation read, and individual
post-validation invariant failures. Any such result requires STOP.
## PE-4 dedicated Windows SSH identity

Action B remains blocked while `.ssh/id_ed25519` is absent. The governed
provisioning entrypoint is a Windows-only, non-network prerequisite. It accepts
only a governance commit and emits bounded state, a public SHA-256 fingerprint,
and a protected evidence directory. On PASS or failure, STOP and preserve the
reported evidence. A public-only or private-published failure is not cleaned up
manually; reconciliation and rollback require separate authorization. Never
copy key material into logs, tickets, or repository content.

The provisioning result is governed evidence only when `EVIDENCE_PUBLISHED` is
TRUE after exact final reread and ACL confirmation. Failure cleanup occurs before
the failure payload is constructed. If confirmation fails, preserve the reported
evidence directory and filesystem state; do not overwrite `result.json`, create
a contradictory result, remove a published key, or manually reconcile it.

Execution remains blocked pending publication of the collision/path correction.
The tool must observe true absence of both `.ssh/id_ed25519` names through its
non-following entry primitive; a dangling target is not absence. Key and
evidence publication are valid only through the governed Windows atomic
no-replace operation. The resulting private path is exactly Action B's fixed
`IdentityFile`; no rename, migration, alternate name, or override is permitted.

Provisioning remains blocked until the evidence reconciliation correction is
published and freshly reviewed. Do not interpret exact final evidence alone as
publication success after a move error. Success additionally requires proven
non-following absence of `.result.tmp`; any retained or ambiguous entry requires
STOP, preservation of both paths, and no overwrite, cleanup, or second result.

The first authorized attempt failed safely at `KEY_VALIDATION` with
`PUBLIC_KEY_INVALID`: native Windows OpenSSH used CRLF while the published
parser rejected every carriage return. Neither final key was published and
rollback was not recommended. The corrected parser accepts exactly one terminal
LF or CRLF while retaining the structural, algorithm, Base64, comment, pair,
ACL, and fingerprint gates. Derived-public validation consumes the pinned
generator's native commented record without appending a fourth field. Do not
retry until publication and fresh review.

For Action D, operators supply only the published governance commit and the
preserved Action B transfer directory. The tool itself snapshots verified
wheel/lock bytes and never asks pip to consume the transfer pathname. It emits
bounded construction, snapshot, evidence, eligibility, retention and cleanup
states. Every PASS or FAIL is a STOP. Preserve any reported evidence directory
or retained construction unchanged. Do not invoke Action E unless Action D
reports confirmed evidence and confirmed eligibility; visual similarity of a
construction directory is not acceptance.

Windows OpenSSH servicing drift is a transport trust gate, not permission to
fall back to ambient SSH. The current Action B pins only reviewed System32
Microsoft-signed `OpenSSH_9.5p2` hashes; a hash mismatch stops before any
transport. Historical Action B evidence remains valid when its temporary
staging later disappears, but a replacement transfer requires a fresh,
separately authorized transaction and must never recreate the historical path.
## PE-4 replacement Action B stop boundary

The observed replacement failure `REMOTE_STAGING_IDENTITY_INVALID` left only
the empty PI3 directory `/tmp/hioc-pe4-artifact-transfer-g_jrlqkl` (recorded
UID/GID `1000/1000`, `0700`, device `45826`, inode `131762`). Do not inspect,
reuse, clean, or reconcile it under the consumed attempt authorization. No
wheel/lock transfer or Action D occurred. `ROLLBACK_RECOMMENDED=FALSE` does not
authorize deletion. Preservation was the historical disposition; current
operator checks report that directory ABSENT, with disappearance cause UNKNOWN.

Future replacement Action B execution must invoke the published
`tools/hioc-pe4-action-b-replacement.ps1` once, not manually pasted fragments.
It accepts a managed Python path and the exact published governance commit,
checks the clean synchronized source and governed local inputs/transport, then
stops on every terminal state. It preserves successful staging and rejects both
the historical and failed transfer paths. It cannot authorize Action D.

The first newly authorized wrapper invocation after publication stopped before
Action B launch because Windows PowerShell stripped embedded Python quotes,
causing `NameError: tools`. Treat its historical transaction marker as wrapper
context evidence only. Do not inspect PI3: no SSH or staging creation was
reachable. The corrected wrapper uses structured native argument lists and its
prelaunch terminal state explicitly says wrapper invoked, prechecks failed,
launch not started, and transaction not started. The consumed authorization
does not permit another invocation. Invoke the corrected wrapper only through
the governed managed PowerShell Core host; legacy Windows PowerShell 5.1 fails
closed because it does not implement `ProcessStartInfo.ArgumentList`.
## Action D failure evidence

On failure, retain only governed diagnostic stage, operation, normalized exception
class, and bounded errno. Do not disclose exception messages, tracebacks, paths, or
input contents. Failure evidence never authorizes Action E.

## Action D preparation stop boundary

At the earlier hierarchy-preparation checkpoint, an explicitly authorized
D-PREP invocation was required to
establish or validate the `runtime`, `pe4`, and `environments` hierarchy. It must
not inspect Action B staging or retained Action D evidence, and every result stops.
That prerequisite is now PASS / CLOSED; no D-PREP rerun is authorized or required.

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

Retained close order is evidence, evidence_root, environments, root, runtime,
anchor, after umask restoration. Each non-null close is attempted once; only
OSError is suppressed, later closes continue, and PASS/0 and FAIL/1 survive it.
Umask disposition D requires no further correction/test. Detailed diagnostic and
validation contracts are in HIOC_MASTER_PLAN.md.

### Historical production evidence and current availability

Current operator-observed availability is recorded in the transfer-evidence
recovery status above. Historical paths remain audit facts; no continued
presence, reconstruction, substitution, or cleanup authority is implied.
