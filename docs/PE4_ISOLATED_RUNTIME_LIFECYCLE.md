# PE-4.0B.2a Isolated Runtime Lifecycle

The staging creation result includes bounded device, inode, UID, and mode
identity. Every subsequent command independently opens the governed
path with `O_DIRECTORY|O_NOFOLLOW`, verifies the complete tuple using `fstat`,
and performs child operations relative to that descriptor. Replacement,
renaming, inode mismatch, or indeterminate inspection blocks all state advance;
no replacement directory is adopted or cleaned. Runtime preflight applies
role-specific, read-only Windows ACL validation: `.ssh` must have its governed
inherited compatibility layout; `known_hosts` its governed protected trust-file
layout; and both dedicated keys the strict protected private-object layout.
It also accepts exactly one numeric PI3 host-key record.

## Authority and status

This document governs repository-controlled execution of the already-selected
PE-4 runtime. It does not authorize execution. PI3 remains the execution host,
PI5 HA remains the remote API source, CPython 3.11.2 remains accepted, and
`websockets==16.1.1` remains frozen by
`PE4_ISOLATED_RUNTIME_DEPENDENCY_CONTRACT.md` and `requirements-pe4.lock`.

```text
ROUTE_PROOF_ORDER=BEFORE_DEPENDENCY_DEPLOYMENT
PE4_0B2A=NOT_STARTED
PE4_0B2B=NOT_STARTED
PE4_0C=NOT_STARTED
ACTION_A=COMPLETE
WINDOWS_SSH_IDENTITY_PROVISIONING=COMPLETE_PASS
PI3_PUBLIC_KEY_AUTHORIZATION=COMPLETE_PASS
ACTION_B=COMPLETE_PASS
ACTION_C=COMPLETE_PASS_EXACTLY_ONCE
D_PREP=PRODUCTION_EXECUTED_PASS
ACTION_D=COMPLETE_PASS
ACTION_E=NOT_STARTED
ACTION_F=NOT_STARTED
ACTION_G=NOT_STARTED
ROLLBACK=NOT_PERFORMED
```

Every action is separately authorized, emits a bounded terminal result, and
stops. PASS never chains the next action.

## Action boundaries and tools

| Action | Repository entrypoint | Network boundary | Mutation boundary |
| --- | --- | --- | --- |
| Windows identity prerequisite | `tools/hioc-pe4-windows-ssh-identity-provision.py` | None | One invocation-owned `.ssh` staging directory, the fixed public/private identity pair, and private Windows evidence only |
| PE-4.0B.2a-A | `tools/hioc-pe4-artifact-acquire.py` | Exact governed HTTPS `files.pythonhosted.org` wheel URL only | Private workstation staging and durable off-device cache only |
| PE-4.0B.2a-B | `tools/hioc-pe4-artifact-transfer.py` | Bounded SSH command streaming only to `jazofv1@192.168.100.252`, strict pinned known-host checking; no SCP | One private `/tmp/hioc-pe4-artifact-transfer-XXXXXXXX` directory only |
| PE-4.0B.2a-C | `tools/hioc-pe4-route-proof.py` | One TCP connection to `192.168.100.251:8123`; no HTTP, WebSocket, credentials, proxy, DNS, redirect, or retry | None |
| PE-4.0B.2a-D | `tools/hioc-pe4-runtime-construct.py` | None | One private construction directory and offline venv installation |
| PE-4.0B.2a-E | `tools/hioc-pe4-dependency-validate.py` | None | None; isolation, distribution, and API behavior validation only |
| PE-4.0B.2a-F | `tools/hioc-pe4-runtime-publish.py` | None | Exact client, versioned environment, and active pointer only |
| PE-4.0B.2a-G | `tools/hioc-pe4-runtime-preflight.py` | None | None; complete credential-free runtime preflight only |
| Rollback | `tools/hioc-pe4-runtime-rollback.py` | None | Atomic active-pointer restoration to a retained eligible environment only |

## Action B publication boundary

The tool streams each fixed local artifact on SSH stdin to a bounded remote
Python sink. A no-follow directory descriptor anchors the private staging
directory; `O_CREAT|O_EXCL|O_NOFOLLOW` creates only `.wheel.part` or
`.lock.part` relative to that descriptor. Size and SHA-256 are checked while
reading bounded input and the owned partial is fsynced. After independent
identity checks, the tool publishes each final artifact through
Linux `renameat2` with `RENAME_NOREPLACE`; an existing regular file, directory,
symlink, dangling symlink, or any other directory entry is a collision. The
tool never removes or replaces the collided entry. Publication is complete only
after final filename, regular/non-symlink type, owner `jazofv1`, mode `0600`,
size where governed, SHA-256, file/directory durability, and non-following
absence of the partial source all confirm.

Result-last evidence is prepared with `O_CREAT|O_EXCL|O_NOFOLLOW` after both its
temporary and final names are observed absent. It uses the same no-replace
publication and requires exact payload digest, metadata, durability, and
temporary-source consumption. A reported rename error is reconciled by that
complete proof only. Once evidence publication is attempted, failure cannot
trigger a second result publication.

Local preflight requires Windows operator `JorgeAzofeifaCastill`, the exact
Known Folder profile, the governed `ssh.exe` and `ssh-keygen.exe` digests, the
reviewed Ed25519 pair/comment/fingerprint, and the reviewed numeric PI3 host-key
fingerprint. No key or known-host bytes are emitted. Evidence terminal state is
`NOT_PUBLISHED`, `CONFIRMED`, or `UNCERTAIN`; the immutable payload says
`AWAITING_CONFIRMATION` because it is written before independent confirmation.

The tools share `tools/hioc_pe4_runtime_common.py`. The shared module freezes
paths, identities, modes, evidence fields, cleanup boundaries, exact installed
distribution policy, and source/client verification; it is not an entrypoint.

## Artifact acquisition, cache, and transfer

Action A creates a unique private directory below the workstation's local HIOC
artifact root, refuses symlinked or unsafe paths, downloads only the exact
official URL with bounded size and time, and verifies filename, 188095-byte
size, and SHA-256 before same-root durable-cache publication. The cache is
off-device recovery input and is never Git content. Failure removes only the
invocation directory after proving its parent and type.

The exact Windows layout is the Known Folder `LocalApplicationData` followed by
`HIOC/artifacts/pe4/{cache,staging,evidence}`. The Known Folder is the trusted
boundary; every existing child component is rejected if it is a file, symlink,
junction, mount point, or other reparse point. Each governed directory and file
uses a protected DACL with inheritance removed and exactly the current user SID
allowed Full Control. Windows security is proved by DACL, never POSIX mode.

ACL persistence does not use `Get-Acl` or `Set-Acl`. A child-only environment
passes the already validated path to Windows PowerShell; the helper loads the
existing `DirectorySecurity` or `FileSecurity` access descriptor through
`DirectoryInfo`/`FileInfo`, disables inheritance without retaining inherited
rules, removes every remaining explicit Allow or Deny rule, adds exactly one
current-user SID FullControl rule, persists the descriptor, and rereads it.
Validation requires a protected DACL, exactly one non-inherited Allow ACE, the
exact SID and FullControl rights, directory `ContainerInherit|ObjectInherit` or
file `None`, and `PropagationFlags=None`. Read, protection, rule-update,
application, reread, and each validation failure have bounded error codes.

The first production attempt created only the expected `HIOC` directory and
stopped at ACL application before acquisition. A retry after separate
publication and authorization must reject it if it is a file or reparse point;
otherwise it hardens that existing directory before creating or using any
descendant. No operator deletion or manual ACL change is required or allowed.

Action A uses a direct HTTPS connection to the single frozen
`files.pythonhosted.org` host/path, with no proxy, redirect, retry, alternate
endpoint, or URL resolution. A monotonic 20-second total deadline is propagated
as the maximum remaining timeout for connection, response, and every bounded
read. At most 188096 bytes are read. Result-last evidence is an invocation-owned
child under the governed evidence root: a same-directory temporary file is
flushed, atomically replaced as `result.json`, and ACL-validated. Windows does
not claim POSIX directory-fsync durability.

Terminal and evidence state explicitly report `ARTIFACT_ACQUIRED`,
`ARTIFACT_VERIFIED`, `DURABLE_CACHE_PUBLISHED`, `CACHE_REUSED`, and
`EVIDENCE_PUBLISHED`. Evidence failure after durable publication therefore
cannot be mistaken for non-publication. Invalid CLI input emits only bounded
failure markers. Action A PASS stops before Action B.

Action A production evidence records fresh acquisition, exact verification,
durable publication, result-last evidence, and PASS. Action B consumes only the
exact wheel at the fixed `LocalApplicationData/HIOC/artifacts/pe4/cache` path
and the repository lock; it accepts no caller-selected path and does not consume
Action A evidence. It validates cache components as non-reparse directories
with governed protected DACLs and independently verifies filename, size,
SHA-256, lock identity, governance commit, and source identities.

Action B resolves only Windows system OpenSSH executables, never `PATH`. It uses
strict known-host verification, numeric PI3 addressing, bounded attempts/time/
output, public-key-only batch authentication, and no password fallback. Wheel
and lock transfer separately into one private, owner/mode-validated PI3 staging
directory and are independently verified before atomic rename. Result-last
sanitized evidence records partial state. The directory is reported and
preserved on PASS or any post-creation failure; there is no automatic cleanup.
Action B remains blocked until its dedicated identity is separately provisioned,
the public key is separately authorized on PI3, and transfer is then prepared
and authorized.

The first published transfer correction remained blocked during final review:
OpenSSH still accepted user/system configuration capable of substituting
`Hostname`, port, proxy/jump routing, known-hosts, or identity inputs, and a
post-rename evidence error could leave terminal and persisted publication state
ambiguous. The corrected transport uses `-F none`, pins numeric hostname and
port 22, disables proxy/jump/canonicalization, pins the current Windows profile's
non-reparse `.ssh/known_hosts` and `.ssh/id_ed25519`, disables agent/configured
identity selection, and retains strict public-key-only authentication. Evidence
is prepared and fsynced, atomically renamed, then independently digest-, mode-,
owner-, file-, and directory-fsync-confirmed. A rename command failure is
accepted only when that exact confirmation succeeds. Action B remains
**BLOCKED / NOT EXECUTED** pending publication and fresh preparation.

## Dedicated Windows SSH identity prerequisite

Read-only discovery found no suitable private key: `.ssh` is a real directory,
the fixed numeric-PI3 `known_hosts` prerequisite exists, and both `id_ed25519`
and `id_ed25519.pub` are absent. This is CASE C discovery and CASE B lifecycle
governance: provisioning is a new repository-controlled operation, not an ad
hoc operator command. Its implementation does not authorize execution.

`tools/hioc-pe4-windows-ssh-identity-provision.py` accepts only the governance
commit. It derives the current profile with the Windows Known Folder API and
fixes `.ssh/id_ed25519`, `.ssh/id_ed25519.pub`, Ed25519, comment
`hioc-pe4-action-b-windows`, and system
`C:/Windows/System32/OpenSSH/ssh-keygen.exe` with reviewed SHA-256
`47f009c35523b6997aff0f0528dae84f1545465479d722292499941cd5cb83b5`.
No caller may override a path, algorithm, comment, executable, or host. The key
has an empty passphrase because Action B disables agents and prompts through
`BatchMode=yes`, `IdentityAgent=none`, and `IdentitiesOnly=yes`.

The Windows OpenSSH trust-anchor refresh accepts exactly the reviewed
Microsoft-signed System32 `OpenSSH_9.5p2` executables: `ssh.exe`
`786ff14be7cd652b2b9770a57e9b1aa5e03a052ce3a3d641fb4760c0ff3fde05` and
`ssh-keygen.exe`
`47f009c35523b6997aff0f0528dae84f1545465479d722292499941cd5cb83b5`.
Both were regular non-reparse files under a non-reparse System32 OpenSSH
directory, TrustedInstaller-owned with protected ACLs and valid Microsoft
Authenticode signatures. Their observed September 9, 2026 servicing cause is
unproven. Exact single-hash pinning remains mandatory; this update does not
authorize a replacement Action B transfer.

Both final names must remain absent at preflight, immediately before generation,
and immediately before their respective publications. Generation occurs only
in an invocation-owned, protected, non-reparse child of `.ssh`. The directory
must contain exactly the generated pair. Each file receives and independently
rereads the protected current-SID-only FullControl DACL. The public record must
be exactly `ssh-ed25519`, carry the fixed comment, match public material derived
from the private file, and yield only a parsed bounded `SHA256:` fingerprint.
No key material enters terminal output or evidence.

The pinned Windows OpenSSH implementation writes that one public record with a
CRLF terminator. Validation accepts exactly one optional LF or CRLF terminator,
then applies the algorithm, Base64, comment, pair, and fingerprint checks to the
single record. Bare CR, embedded line endings, multiple records, extra blank
lines, and oversized or malformed input remain invalid. The derived-public
record is parsed in that same native form, including its governed comment; no
synthetic field is appended.

Absence is established with a non-following directory-entry probe. Only the
operating system's not-found result is accepted; a regular file or directory,
symlink, dangling symlink, junction, dangling junction, mount point, another
reparse entry, or an indeterminate inspection result is a collision. Final key
and `result.json` publication uses same-directory Windows `MoveFileExW` with
write-through and no replacement flag. Thus a destination created after the
last inspection is rejected atomically rather than overwritten.

The authoritative pair remains `.ssh/id_ed25519` and `.ssh/id_ed25519.pub`.
That pair was deliberately frozen as Action B's dedicated identity when its
ambient SSH inputs were eliminated; a later preparation description naming
`hioc_pe4_pi3_ed25519` was not repository governance. Provisioning and Action B
derive the private name from the same shared constant and tests fail on drift.

Evidence reconciliation additionally proves publisher ownership. If the
no-replace move reports an error, exact final bytes, digest, type, non-reparse
state, and DACL are necessary but not sufficient: `.result.tmp` must also be
truly absent under the same non-following entry semantics. A retained file,
dangling link, junction, mount point, other reparse entry, or inspection error
means the prepared source was not proven consumed and publication remains
FALSE. Normal success confirms the same absence after final readback. A raced
exact result is preserved but neither accepted nor overwritten, and no second
result is published.

After staged validation the public file is atomically published first and the
private file last. The private rename is the local completion marker because
Action B consumes it, but PASS additionally requires complete final filesystem,
ACL, pair, comment, algorithm, fingerprint, and result-last evidence validation.
Evidence is an invocation-owned protected child of the existing Windows PE-4
evidence hierarchy. Failure before publication may clean only the proven staging
child. Any public-only or private-published state is preserved and reported;
final keys are never automatically deleted, and reconciliation/rollback requires
separate authorization. Provisioning PASS stops before PI3 public-key
authorization and before Action B.

Execution preparation subsequently found that failure evidence could precede
staging cleanup, post-rename ACL failure could leave an unconfirmed result, and
child creation could lose its cleanup identity when ACL initialization failed.
The corrected lifecycle records each invocation child through an explicit
creation callback before hardening. It cleans only a confirmed invocation child
and finalizes cleanup state before building failure evidence, preserving the
primary error while separately recording cleanup failure.

Evidence now has one prepare/publish/confirm attempt. Preparation serializes the
final bounded state deterministically, computes its digest, flushes a private
temporary file, applies the DACL, and validates exact bytes, digest, type,
non-reparse status, and ACL. Publication refuses an existing `result.json` and
uses atomic same-directory replacement. Confirmation independently repeats all
invariants on the final path. A rename error is reconciled only if the exact
intended final result fully confirms. Otherwise publication remains FALSE; the
unexpected result is not overwritten and no contradictory second result is
published. Confirmed persistent and terminal state agree for key publication,
pair confirmation, staging/evidence-child cleanup, evidence publication,
result, error, stage, and rollback recommendation.

## Construction and validation

Action D opens the exact transferred directory without following links and
copies only the independently verified wheel and lock into an invocation-owned
`/tmp/hioc-pe4-runtime-input-*` snapshot. Source and destination descriptors,
metadata, byte counts, and SHA-256 digests remain bound through the copy; pip
uses only `/proc/self/fd` references to that snapshot. The requirements lock is
also copied into a write-sealed anonymous descriptor, and pip reads that exact
descriptor; the governed hash in that sealed lock protects wheel consumption
against a same-account directory-entry race. The Action B directory is never
modified. The snapshot is removed by descriptor on every successful
construction and on ordinary failure; cleanup failure is reported separately.

The runtime root and `environments` child are opened without following links,
validated for exact owner, group and `0750` mode, and retained by descriptor.
Action D exclusively creates its construction child relative to that descriptor
and never discards this identity before venv construction. The venv is created
in the already-existing directory with `/usr/bin/python3 -I -m venv --copies .`.
The directory and parent identities are revalidated afterward. Standard CPython
POSIX `lib64 -> lib` is the sole permitted internal symlink; every other symlink,
including an escaping link, fails closed.

Before installation Action D proves CPython 3.11.2, the `/usr/bin/python3` base
interpreter, isolated prefix, disabled user/system sites, the Linux AArch64
SOABI, and required pip options. Installation uses a minimal explicit
environment, ignores ambient Python, pip, proxy and index configuration, sets
`PIP_CONFIG_FILE=/dev/null`, disables input, keyring and version checks, and
uses exactly:

```text
--isolated --no-index --no-deps --require-hashes --only-binary=:all: --no-cache-dir
```

The private snapshot descriptor is the sole `--find-links` source. Pip isn't
upgraded. The final set contains exactly one pip, no more than one setuptools,
exactly `websockets==16.1.1`, and nothing else. Failure cleanup is
descriptor-relative and may delete only the retained invocation-owned tree.

Action D publishes private result-last evidence with atomic no-replace linking,
fsync, exact reread and digest/metadata confirmation. After a confirmed
construction, evidence or handoff failure intentionally retains the tree but
leaves it ineligible. Only confirmed evidence permits a read-only
`.hioc-action-d-eligibility.json` marker binding the construction, commit,
artifacts and evidence digest. Action E validates both records before inspecting
distributions. Terminal markers separately report construction, snapshot,
evidence, eligibility, retention and cleanup state.

Action E independently proves the installed distribution set is limited to
venv bootstrap components plus exactly `websockets==16.1.1`. It proves canonical
asyncio `connect`, `max_size`, `proxy`, `open_timeout`, `close_timeout`, `**kwargs`
preconnected-socket support, redirect refusal with that socket, `PayloadTooBig`,
and `InvalidStatus`. Install success alone is never acceptance.

## Publication, backup, and rollback

Action F revalidates source commit, clean `main`, `origin/main`, client Git blob
and SHA-256, dependency capabilities, construction ownership, and non-symlinked
paths. It creates the exact immutable versioned environment, installs the client
at `/home/jazofv1/hioc/tools/hioc-pe4-ha-auth-capability.py` with mode `0700`,
and atomically replaces the active pointer only after validation. Existing
unexpected destinations fail closed. The prior active target is recorded and
retained; environments are never modified in place.

General release backup, deployment, and rollback flows treat `runtime/pe4` as
release-managed externalized content: they neither overwrite nor restore it.
Recovery inputs are the Git lock and tools, exact frozen artifact identity, the
durable off-device wheel cache, and retained prior approved environment. State,
history, logs, backups, configuration, manufacturer data, and credentials keep
their existing protected classifications.

PE-4 rollback is separate from general release rollback. It accepts only a
basename matching the governed environment form, proves it is a non-symlinked
direct child with safe ownership/mode and an acceptable distribution set, and
reads that basename only from the tool-published private `previous-active`
record rather than caller input, then atomically restores only the active
pointer. It never contacts an index and
never deletes the failed or restored environment automatically.

## Evidence, failure, and cleanup

Persistent evidence uses a tool-created private `/tmp` directory (`0700`) and
atomic result-last `result.json` (`0600`) with fsync. Allowed content is limited
to action/target classification, governed artifact filename/size/digests,
environment identity, client blob/digest, owner/mode result, installed version,
capability/preflight result, prior/current active target, bounded error/stage,
result, and rollback recommendation.

Credentials, tokens, authorization headers, HA bodies, secrets, environment
dumps, raw command output, arbitrary package metadata, and unrelated system or
household information are prohibited. Every failure stops. Cleanup may target
only a validated invocation path; neither `/home/jazofv1/hioc` nor
`/home/jazofv1/hioc/runtime/pe4/environments` may be recursively removed.
## Replacement Action B failed transaction

Replacement Action B is **ATTEMPTED_NOT_COMPLETE**, not eligible for retry
under its consumed authorization. Its first attempt created the empty private
directory `/tmp/hioc-pe4-artifact-transfer-g_jrlqkl` (UID/GID `1000/1000`, mode
`0700`, device `45826`, inode `131762`) and stopped at
`REMOTE_STAGING_IDENTITY_INVALID` before wheel or lock transfer, evidence
publication, or Action D. This is a transaction-staging disposition issue, not
a runtime rollback: `ROLLBACK_RECOMMENDED=FALSE`; the historical disposition
was preservation without cleanup. Current operator checks report ABSENT.

A future attempt is governed by `tools/hioc-pe4-action-b-replacement.ps1` as a
single invocation: all repository and local transport prechecks precede the one
tool launch; native Git divergence must parse as exactly two non-negative zero
fields; output is preserved; current PASS markers and a new shared-grammar
transfer path are required. Every terminal outcome emits `STOP_REQUIRED=TRUE`.
The wrapper never launches Action D or retries.

One separately authorized invocation of the original governed wrapper stopped
at local precheck with `NameError: tools` caused by Windows PowerShell native
argument serialization. The wrapper was entered but its Action B launch was
not started: no process, SSH, PI3 staging, or transfer occurred. Historical
`REPLACEMENT_TRANSACTION=TRUE` from that wrapper version denotes wrapper
context only. The corrected wrapper uses structured argument lists and emits
separate wrapper/precheck/launch/transaction markers. That authorization is
consumed and cannot be retried without a new review and authorization. Managed
PowerShell Core is mandatory because legacy Windows PowerShell 5.1 cannot carry
the required discrete argument list.
## Action D diagnostic retention

If Action D fails, the primary failure remains authoritative while cleanup and failure-
evidence publication outcomes remain separate. The original Action B transaction is
never changed, and a corrected Action D retry still requires new authorization.

## Action D runtime hierarchy preparation

`PE-4.0B.2a-D-PREP` is a separate mandatory STOP checkpoint before any newly
authorized Action D attempt. Its repository entrypoint creates or independently
validates only `runtime`, `runtime/pe4`, and `runtime/pe4/environments` beneath
the existing `/home/jazofv1/hioc` trust anchor. Every owned directory is a
non-symlink `jazofv1:jazofv1` directory at exact mode `0750`. A valid existing
`runtime` mount is permitted, while `pe4` and `environments` must be on their
respective parent devices. Existing noncompliance fails closed without chmod or
chown; confirmed partial hierarchy is retained for an explicitly authorized
retry. D-PREP evidence is audit-only: Action D remains construction-only and
independently revalidates the hierarchy without consuming D-PREP evidence.

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

Action D is complete; the next boundary is separate Action E preparation.
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

Current sequence: A -> B -> C -> D-PREP -> D -> E -> F -> G, with separately
authorized STOP boundaries at every step.
