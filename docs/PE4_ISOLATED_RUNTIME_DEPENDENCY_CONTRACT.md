# PE-4 Isolated Runtime and Dependency Contract

## Current PI3 D-to-E read-only compatibility validation — PASS / CLOSED

The existing ancestry, critical-blob equality, replacement-protection and
producer-bound eligibility policy PASSed on PI3 for the reviewed pair. The
contract and source remain unchanged; compatibility is separate from authorization.

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

## Corrected D-to-E governance compatibility contract

E requires `--governance-commit` (current consumer/source) and
`--action-d-governance-commit` (immutable D producer), with no default/fallback.
Both must be full lowercase 40-hex IDs resolving to actual Git commit objects;
tags, trees, blobs, refs, abbreviated IDs and missing objects are rejected.
Compatibility-critical Git reads and ancestry checks use `--no-replace-objects`.
Complete history is mandatory. Producer must equal or be an ancestor of consumer;
divergence, descendant/unrelated producers, shallow/missing history and Git errors
fail closed.

Exactly these upstream committed blob identities must match producer and consumer:
`tools/hioc-pe4-runtime-construct.py`, `tools/hioc_pe4_runtime_common.py`, and
`requirements-pe4.lock`. Missing paths or nonblob tree entries reject. Changes
outside this critical set can be compatible if all current-source gates pass.
Current source must be clean main, HEAD and local origin/main equal consumer,
ahead/behind zero, and free of active Git operations. Normalized committed/worktree
blobs must match consumer for E, the new compatibility helper and those three
critical files. Hidden worktree modifications are rejected by direct blob checks.

The unchanged strict D validator receives producer, never consumer. Marker/evidence
must retain their existing producer, selected construction, environment, approved
wheel/lock, evidence path/digest, PASS and persisted eligibility-state bindings.
Compatibility rejection precedes construction access, distributions, capability
probe and E evidence allocation. Codes/stages are finite and sanitized; there is
no retry, rollback or cleanup. E still independently validates exact distributions,
`websockets==16.1.1`, the asyncio connect API/keywords, exception capabilities,
isolated prefixes, preexisting-socket redirect refusal and owned hierarchy/device
semantics. E success JSON is unchanged. Compatibility is separate from authorization.
Action E remains **NOT STARTED**; F/G remain separate and unauthorized.

The original implementation synchronization/read-only validation boundary
is now PASS/CLOSED as recorded above. Next checkpoint:
`ACTION_E_REPREPARATION_READY_FOR_SEPARATE_AUTHORIZATION`.

Action B's invocation-owned staging identity is the tuple of its governed path,
device, inode, UID, and mode `0700`. Each independent
remote primitive must open the directory non-followingly, compare `fstat` to
the complete tuple, and use descriptor-relative fixed child names. A pathname
replacement is never equivalent, even with the same owner, mode, and expected
bytes. Numeric PI3 trust requires exactly one accepted Ed25519 record. The
Windows transport material is validated by role. The shared `.ssh` directory
must be non-reparse, owned by the current operator or Administrators, inherit
only FullControl Allow ACEs for SYSTEM, Administrators, and the current
operator, and have no other ACE. The protected `known_hosts` file must be owned
by the current operator and contain only explicit SYSTEM/Administrators
FullControl plus current-operator Modify/Synchronize Allow ACEs. Each dedicated
key remains protected, current-operator-owned, and governed by exactly one
explicit current-operator FullControl Allow ACE.

The current Windows transport trust anchors are the reviewed System32
Microsoft-signed `OpenSSH_9.5p2` `ssh.exe`
`786ff14be7cd652b2b9770a57e9b1aa5e03a052ce3a3d641fb4760c0ff3fde05` and
`ssh-keygen.exe`
`47f009c35523b6997aff0f0528dae84f1545465479d722292499941cd5cb83b5`.
They replace stale hashes after legitimate-looking servicing drift; exact
servicing causality remains unproven. Both remain single exact fail-closed
identities, not a compatibility allow-list.

## Status and authority

This repository-only checkpoint governs the future PI3 runtime for the
PE-4.0B.2a Home Assistant capability client. It does not install, deploy, or
execute anything. PE-4.0B.2a remains **NOT STARTED**.

```text
PI3_PYTHON_POLICY=SATISFIES_EXISTING_HIOC_POLICY
PI3_PYTHON_RUNTIME=CPYTHON_3_11_2
PYTHON_VERSION_CHANGE_REQUIRED=FALSE
DEPENDENCY_ARCHITECTURE=CASE_A_ISOLATED_RUNTIME
READINESS=READY_FOR_PE4_0B2A_ISOLATED_RUNTIME_GOVERNANCE_COMMIT_REVIEW
```

The existing Python policy remains authoritative: CPython 3.10 is the language
floor and production uses its independently validated distribution-managed
`python3`. The observed PI3 CPython 3.11.2 runtime satisfies that policy. This
checkpoint does not replace, upgrade, or otherwise modify the system Python.

## Frozen dependency artifact

The sole third-party runtime dependency is `websockets==16.1.1`. Its official
PyPI metadata declares Python `>=3.10`, includes Python 3.11 support, and lists
no required distributions. Consequently the governed transitive dependency set
is empty.

```text
PROJECT=websockets
VERSION=16.1.1
FILENAME=websockets-16.1.1-cp311-cp311-manylinux2014_aarch64.manylinux_2_17_aarch64.manylinux_2_28_aarch64.whl
SIZE_BYTES=188095
SHA256=86d7f0f8bdb25d2c632b72527325e4776430fd5bc61b9118de4e2b8ddb5f5b01
PYTHON_TAG=cp311
ABI_TAG=cp311
PLATFORM_TAGS=manylinux2014_aarch64,manylinux_2_17_aarch64,manylinux_2_28_aarch64
TRANSITIVE_DEPENDENCIES=NONE
```

The wheel matches the observed CPython 3.11 AArch64 Linux SOABI. The exact
filename, byte count, digest, and package/version must all match before it can
enter a later deployment. A differently named file, sdist, universal wheel,
different version, different digest, or additional dependency fails closed.
The artifact isn't committed to Git. It must be retained in a governed durable
off-device artifact cache or backup; a PI3 transfer location is temporary and
invocation-owned.

`requirements-pe4.lock` is the machine-readable project/version/hash lock.
Installation must be offline and hash-enforced with the isolated interpreter:

```text
python -m pip install --no-index --no-deps --require-hashes --only-binary=:all: --find-links <private-wheel-directory> -r requirements-pe4.lock
```

`<private-wheel-directory>` is a future deployment-tool-owned private input,
not an operator-selected reusable directory. `--no-deps` is permitted only
because official metadata records no required distributions. No live package
index, resolver drift, dependency upgrade, vendoring, or unbounded pip upgrade
is permitted. The isolated pip version and its required option capabilities
must be recorded and validated before installation; `ensurepip` may bootstrap
pip without network access but isn't proof of the dependency installation.

## PI3 filesystem and interpreter contract

The release-managed runtime layout is:

```text
RUNTIME_ROOT=/home/jazofv1/hioc/runtime/pe4
ENVIRONMENT_ROOT=/home/jazofv1/hioc/runtime/pe4/environments
VERSIONED_ENVIRONMENT=/home/jazofv1/hioc/runtime/pe4/environments/cpython311-websockets16.1.1-lock-v1
ACTIVE_POINTER=/home/jazofv1/hioc/runtime/pe4/active
ACTIVE_INTERPRETER=/home/jazofv1/hioc/runtime/pe4/active/bin/python
CLIENT=/home/jazofv1/hioc/tools/hioc-pe4-ha-auth-capability.py
OWNER_GROUP=jazofv1:jazofv1
```

Runtime root, environment root, and versioned environment are mode `0750`;
the deployed client is mode `0700`; a private artifact staging directory is
mode `0700` and its wheel is `0600`. The repository lock is ordinary reviewed
release content (`0644`). No governed path may be group- or world-writable.
Symlinks are rejected throughout except for the strictly managed active pointer.

The environment is created with `/usr/bin/python3 -m venv` without
`--system-site-packages`. It is validated as CPython 3.11.2 with the expected
Linux AArch64/SOABI, isolated `sys.prefix`, no system-site inheritance, the
exact installed dependency version, and the client-required API surface.
The client and environment form one compatibility unit and the client is
invoked only with `ACTIVE_INTERPRETER`, never an ambient `python` or directly
from release source.

The active pointer target is not caller supplied. A future repository tool must
validate a basename-only target under `ENVIRONMENT_ROOT`, prove that target is
complete and non-symlinked, and replace the pointer atomically. The previously
active immutable environment is preserved for immediate pointer rollback.
Symlink mode isn't treated as an access-control boundary; directory ownership
and permissions are authoritative.

## Lifecycle, rollback, and evidence

The isolated environment is reproducible release content, not persistent
application state. Future backup/restore governance must preserve the lock,
artifact identity, durable off-device wheel, deployment tooling, and prior
active environment needed for bounded rollback; it must not treat arbitrary
environment bytes as irreplaceable state. Ordinary release backup exclusions
may omit environment bytes only after that correction is separately reviewed.

A later deployment must create a new versioned environment, validate it fully,
deploy the identity-checked client, atomically activate it, and rerun the full
credential-free runtime preflight through the absolute active interpreter.
Failure before activation leaves the current pointer unchanged. Failure after
activation restores only the preserved prior pointer when the governed rollback
contract says to do so. It never changes system Python or production data.

The independent credential-free PI3-to-PI5 route proof should precede runtime
deployment to preserve fault isolation. Neither proof authorizes credentials,
Home Assistant access, client execution, PE-4.0B.2b, or PE-4.0C.

The executable lifecycle, separate A-G authorization boundaries, evidence,
cleanup, backup, and rollback rules are governed by
`PE4_ISOLATED_RUNTIME_LIFECYCLE.md`. Implementation does not authorize use.
Action A's Windows cache, evidence, DACL, reparse, deadline, partial-success,
and bounded-CLI semantics are governed there; it never uses `/tmp`.
The production ACL correction retains the same security invariant while
removing PowerShell ACL-cmdlet dependence: existing descriptors are hardened
and persisted through Windows .NET file/directory APIs. The first attempt did
not acquire the wheel. The corrected retry established Action A production
PASS and the durable cache. Action B derives that fixed cache internally,
validates its DACL/reparse boundary and exact artifact/lock identities, uses
bounded system OpenSSH, records partial states in result-last evidence,
preserves its private PI3 directory, and stops.

Remote publication is fail-closed and no-replace. The wheel, frozen lock, and
result evidence are moved within the invocation-owned PI3 directory only by
`renameat2(RENAME_NOREPLACE)`. Every destination entry detected by non-following
inspection, including dangling links, is a collision; a race is rejected by
the kernel operation. Evidence temporary creation is exclusive and
non-following. Exact final identity and durability never suffice alone:
publication also requires proof that the corresponding invocation source was
consumed. No collision is deleted, replaced, or reconciled into a second
result.

Artifact ingress does not use SCP. Each governed source is supplied as bounded
stdin to the fixed remote SSH command. The remote sink anchors the `0700`
staging directory through a non-following directory descriptor and exclusively
creates the fixed partial basename relative to it. Size and digest are checked
during the stream; mismatch, interruption, timeout, collision, or an unsafe
directory leaves transfer state false and preserves the invocation directory.
Action B additionally pins the reviewed Windows operator/profile, system SSH
digest, Ed25519 key identity, and numeric PI3 host trust before any connection.

The final transport gate does not inherit OpenSSH configuration or agent state.
It pins numeric PI3 port 22, disables proxy/jump/canonicalization behavior, and
uses fixed non-reparse current-profile `known_hosts` and `id_ed25519` files.
Result-last evidence is complete only after exact post-rename digest, owner,
mode, file-fsync, and directory-fsync confirmation.

The required Action B private identity is provisioned only by
`tools/hioc-pe4-windows-ssh-identity-provision.py`. The tool fixes the current
Known Folder profile's `.ssh/id_ed25519` pair, Ed25519, the
`hioc-pe4-action-b-windows` comment, an empty passphrase, and the reviewed
system `ssh-keygen.exe` digest. It refuses every existing final target and all
reparse traversal. Generation is isolated in a current-SID-only staging child;
the pair, comment, algorithm, ACL, and bounded SHA-256 fingerprint are validated
before public-first/private-last atomic publication and repeated afterward.
Sanitized Windows result-last evidence contains no key material. Identity
provisioning, PI3 public-key authorization, and Action B transfer are three
separate authorizations and STOP boundaries.

Public-record parsing is compatible with the pinned Windows generator's native
single-record CRLF output. One optional LF or CRLF terminator is accepted;
embedded or repeated line endings, bare CR, malformed fields, invalid Base64,
wrong algorithm/comment, and oversized records remain fail-closed inputs. The
same rule consumes the actual three-field derived-public record without adding
a synthetic comment field.

Provisioning evidence is accepted only after all represented cleanup is final
and after exact post-rename content, digest, regular-file, non-reparse, and
protected-DACL confirmation. Invocation-child identity is retained before ACL
hardening so initialization failure cannot orphan an unknown cleanup target.
Rename uncertainty is reconciled only by full confirmation; an unexpected or
ambiguous result remains unaccepted and is never overwritten by a second result.

Final-target absence is non-following and entry-based, not target-based. Only a
not-found result is absence; every file, directory, link, junction, mount point,
other reparse entry, or inspection error is a collision. Windows publication
uses an atomic write-through move without replacement for both keys and final
evidence. The shared `.ssh/id_ed25519` constant is authoritative for both the
provisioning output and Action B `IdentityFile`; `id_ed25519.pub` is the sole
public-key output for the later authorization checkpoint.

Result reconciliation requires proof that the governed publication consumed
its prepared source. After either normal return or an uncertain move error, the
exact final result must confirm and `.result.tmp` must be truly absent according
to the non-following entry primitive. Retained or indeterminate temporary state
fails closed even when an independently created final file has identical bytes
and ACL. Such a collision is preserved without overwrite or a second result.

Action D consumes Action B through an invocation-owned immutable input
snapshot, never through repeated pathname checks. It retains descriptor
identity for the runtime root, `environments` child, construction child and
cleanup target. The explicit Python/pip environment permits no caller-selected
index, proxy, configuration, keyring, user site or package source. Standard
bounded `lib64 -> lib` is the only allowed venv symlink. The accepted
distribution set is one pip, optional single setuptools, exactly
`websockets==16.1.1`, and nothing else. Action E requires the confirmed Action
D evidence digest and construction eligibility marker. Action D was
**BLOCKED / NOT EXECUTED** at that correction checkpoint; current third-execution
closure is PASS / CLOSED. Actions E-G remain not started.
## Replacement Action B transaction identity

The complete canonical Action B staging path is exactly
`/tmp/hioc-pe4-artifact-transfer-[A-Za-z0-9_]{8}`. The shared runtime helper is
the single owner of this fully anchored grammar; it permits only ASCII letters,
decimal digits, and underscore in an eight-character suffix. Syntax is never
Action D eligibility. Action D still requires the owned `0700` directory, the
exact wheel/lock/result entry set, governed digests, and confirmed Action B
PASS evidence before creating its descriptor-bound input snapshot.

The failed replacement path `/tmp/hioc-pe4-artifact-transfer-g_jrlqkl` is
therefore syntactically valid but ineligible: recorded evidence proves it was
empty and lacked every required confirmed artifact and result. Retention
unchanged was the historical disposition; current operator checks report ABSENT.
A future replacement transaction must use a
new invocation-owned directory and may never report either that path or the
missing historical `/tmp/hioc-pe4-artifact-transfer-7g3xp1lk` as success.

The replacement wrapper's local Python prechecks and canonical grammar check
are governed native subprocesses. They use `ProcessStartInfo.ArgumentList` for
each executable argument and never depend on Windows PowerShell legacy command
line flattening. A wrapper precheck failure reports wrapper entry but
`ACTION_B_LAUNCH=NOT_STARTED` and `ACTION_B_TRANSACTION=NOT_STARTED`; it is not
an Action B transaction or an eligible Action D input. The governed invocation
requires managed PowerShell Core: legacy Windows PowerShell 5.1 lacks the
required `ArgumentList` API and fails closed before prechecks proceed.
## Action D sanitized failure evidence

Action D failure evidence is distinct from successful evidence: it is an owned
`/tmp/hioc-pe4-runtime-construct-failure-XXXXXXXX` directory containing a result-last
`failure-result.json` with finite diagnostic enums only. It never creates eligibility.

## D-PREP hierarchy prerequisite

D-PREP validates the existing HIOC anchor and creates only absent exact `0750`
`jazofv1:jazofv1` hierarchy children. Its evidence is audit-only; Action D does
not consume it and still independently validates hierarchy identity.

The anchor is retained through descriptor-bound ancestry and revalidated at each
hierarchy boundary. `EVIDENCE_DIR` is disclosed only after exact, durable,
result-last confirmation; an unconfirmed evidence attempt has no disclosed path.
Each component reports finite `PREEXISTING_COMPLIANT`, `CREATED_CONFIRMED`,
`NOT_REACHED`, or `CREATION_OCCURRED_BUT_FINAL_STATE_UNCONFIRMED` state.

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

### Final repository validation and finalization

D-PREP: 115 run, 108 passed, 7 skipped, zero failures/errors. D-PREP/lifecycle:
126 run, 119 passed, 7 skipped, zero failures/errors. The seven known Windows skips
are POSIX-only; this checkpoint adds no WSL requirement. They are:

- `test_posix_named_child_create_then_idempotent_open`
- `test_posix_path_bound_ancestor_rename_away_is_rejected_as_name_lost`
- `test_posix_path_bound_ancestor_replacement_is_rejected_as_name_substituted`
- `test_posix_path_bound_leaf_removal_is_rejected_as_name_lost`
- `test_posix_path_bound_leaf_rename_away_is_rejected_as_name_lost`
- `test_posix_path_bound_leaf_replacement_is_rejected_as_name_substituted`
- `test_posix_path_bound_unchanged_leaf_revalidates`

Private-child creation retains eight random characters from
`string.ascii_letters + string.digits`, FileExistsError-only retry, 32 candidates,
DIRECTORY_NAME_EXHAUSTED, local fd ownership until transfer, type/UID/GID/mode/device
validation, real descriptor/path revalidation, child fsync then parent fsync and
transfer. Temp-root real-helper coverage includes success transfer, UID mismatch,
raw post-open fstat OSError, cleanup-close preservation, observed wrong type and
symlink, unsupported primitives, open OSError, opened nondirectory, and raw pre-open
lstat OSError. GID/mode variants are redundant with metadata-comparison coverage.

The closed publisher matrix covers temporary-name ownership; temporary and
verification descriptor lifecycles; exact/partial and nonpositive writes;
temporary and final-target collisions; pre-link faults; explicit post-link unlink
and cleanup-retry faults; directory fsync; verification open/fstat/metadata/read/
content/close faults; final revalidation; payload equality and digest timing.
Order remains write, fchmod, file fsync, close, final link, temporary unlink,
directory fsync, reread/verification/close, directory revalidation, digest return.
Once published, the final result may survive later unlink/fsync/verification/
revalidation failure even though the operation fails.

Representative evidence failures retain DIAGNOSTIC_STAGE=EVIDENCE_PUBLICATION and
DIAGNOSTIC_OPERATION=PUBLISH_EVIDENCE. Governed Failure and NamedChildFailure use
GOVERNED_FAILURE / errno NONE; raw OSError uses bounded OS classification and real
nonnegative errno; other exceptions use bounded unexpected classification. Failure
output retains STOP_REQUIRED=TRUE and governed rollback recommendation FALSE.
Retained closes run evidence, evidence_root, environments, root, runtime, anchor;
each non-null handle gets one attempt, only OSError is suppressed, later closes
continue, and PASS/0 or FAIL/1 survives cleanup-close OSError.

Umask review: D. NO MATERIAL CHECKPOINT NEEDED. `old_umask = os.umask(0o027)` saves
the valid previous mask unchanged; finally restores `os.umask(old_umask)` before
retained closes. No source path corrupts it. No normal intended-Linux restoration
failure was established. An injected restore exception could override a pending
return and skip closes; this is injected-only structural behavior, not a production
blocker, with no dedicated test/correction required.

Action D is unchanged, construction-only, and independently validates the hierarchy;
D-PREP evidence is audit-only. Frozen Action D SHA-256:
`e979cc6049f8912c23e880f121fd2988d0354623c4f2a7d27eafb310e4b0c213`.

### Historical production evidence and current availability

Current operator-observed availability is recorded in the transfer-evidence
recovery status above. Historical paths remain audit facts; no continued
presence, reconstruction, substitution, or cleanup authority is implied.
