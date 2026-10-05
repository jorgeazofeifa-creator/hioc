# HIOC Deployment

## Production Action E — PASS / CLOSED

Action E has completed successfully. Publication and activation remain a separate later Action F checkpoint; F is not prepared here.

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

Deployment prerequisite satisfied: PI3 synchronization to the controlled-startup implementation and architecture-matched non-lifecycle validation PASSed. The resulting documentation closure still requires separately authorized synchronization and Action E repreparation before eventual E execution.

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

Deployment prerequisite: publish the corrective consumer, separately prepare and authorize source synchronization and architecture-matched non-lifecycle validation, then independently reprepare Action E. Do not synchronize the superseded 5c9afc5 baseline merely for this correction.

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

PI3 synchronization to the reviewed implementation consumer is PASS/CLOSED.
Future source synchronization, compatibility review and Action E authorization
remain separate governed operations; this closure synchronizes no production host.

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

## Current D-to-E source synchronization prerequisite

Action E now requires both explicit commit arguments: `--governance-commit`
selects the current consumer source commit, while `--action-d-governance-commit`
selects the accepted D producer recorded by immutable D marker/evidence. The
construction selection remains explicit. Omitted producer input fails CLI
validation before host or lifecycle checks; there is no HEAD or consumer fallback.

After publication, source synchronization to PI3 requires separate authorization.
The synchronized checkout must be clean `main`, HEAD and local `origin/main` at
the consumer commit, ahead/behind `0 0`, no active Git operation, and normalized
committed/worktree identities matching E, the compatibility helper, D, common and
lock. Compatibility requires real lowercase 40-hex commit objects, complete
history, producer equality/ancestry and exact D/common/lock committed blob equality,
with Git replacement substitution disabled. Current-source validation and immutable
upstream producer validation remain distinct trust boundaries.

Synchronization is not evidence migration: do not rewrite or recreate the accepted
D marker/evidence to bind the newer consumer. The unchanged strict eligibility
validator must accept the explicit producer before distribution/capability checks.
This correction deployed nothing and did not access PI3/PI5. Action E remains
**NOT STARTED**. F/G remain unchanged and separately unauthorized.

The original implementation synchronization/read-only validation boundary
is now PASS/CLOSED as recorded above. Next checkpoint:
`ACTION_E_REPREPARATION_READY_FOR_SEPARATE_AUTHORIZATION`.

PE-4 Action B staging paths are not sufficient identity. Operators must retain
the bounded creation token, and every ingress, validation, publication, and
evidence command must match it through `open(O_DIRECTORY|O_NOFOLLOW)` plus
`fstat`. Any mismatch blocks deployment and is preserved without cleanup. The
fixed numeric host trust must contain exactly one accepted record, and Windows
SSH-material ACL validation is mandatory before SSH starts. It is
role-specific: shared `.ssh` inheritance, the protected `known_hosts` trust
file, and protected dedicated keys each have an independent ownership and ACE
contract. Validation is read-only and never normalizes a live ACL.

PE-4 client execution is governed on PI3, not in the PI5 Home Assistant
Terminal add-on. `/home/jazofv1/hioc-release-source` remains authoritative clean
release source and `/home/jazofv1/hioc` remains the non-Git deployed runtime.
Exact Python, dependency, environment, installed path, ownership, and modes
require credential-free PI3 preflight. Prefer a release-managed isolated
environment if PI3 capability proof supports it; none is created here.

The repository now contains `tools/hioc-pe4-ha-auth-capability.py`; this
implementation checkpoint deploys nothing. A future checkpoint must freeze its
committed blob/SHA-256, prove one approved installed WebSocket dependency, and
choose governed source execution or a restrictive runtime installation. Any
future installed copy must be byte-identical to the approved Git object and use
ownership and modes proved and separately approved for PI3; the former PI5-local
`root:root` assumption is superseded. No dependency installation is authorized
or implied.

PE-4.0B.1 is complete and deployed nothing. The accepted preflight was
credential-free and read-only. PE-4.0B.2a capability proof, PE-4.0B.2b
registry/schema discovery, PE-4.0C, the adapter, and production deployment are
not started. No package installation or WebSocket-client deployment is implied
by Python availability or by the absence of a dedicated WebSocket client.
The frozen 2a contract adds no deployed artifact. Its repository-controlled
client and any dependency decision require separate commit, release/runtime,
and execution gates.

PE-4.0A deploys nothing. PE-4.0B preparation may approve only a supported,
read-only Home Assistant interface after PI5 deployment classification. Direct
`.storage`, database, add-on, supervisor, shell, service, registry-write,
restart, or reload paths are not deployment shortcuts. No adapter or discovery
tool is deployed by this checkpoint.

Action 10 is not deployment or production cleanup. Its historical transient
transfer target is already absent and non-authoritative. The corrected boundary
is repository-only administrative closure with disposition
`NOOP_ALREADY_ABSENT`; it performs no PI3 verification, deletion, staging
reconstruction, retransmission, runtime mutation, or evidence mutation. Action
10 is complete through the repository-only completion record, with Actions 1–10
and PE-3 complete. No Action 10 Evidence Report was required.

Action 9 production validation is now **PASS / COMPLETE**. It was read only and
created only its private Evidence Report at
`/tmp/hioc-pe3-action9-Bb6vGrmm`; no runtime deployment, production mutation, or
rollback occurred. Action 9 and its Evidence Report remain the final PE-3
production validation and evidence. Transport staging remains absent,
retransmission remains unnecessary, and no Action 10 production action occurred.

The historical Action 9 performance correction was repository governance, not
deployment. The first attempt changed no production state and created no Action 9 evidence
directory. Current Action 9 records valid performance as an observation with an
unvalidated baseline; it does not deploy code, invoke generation, or enforce the
historical four-second/incremental-RSS targets as current production limits.
Any changed Action 9 tool requires a new post-push source-governance refresh,
but no runtime deployment: Action 9 executes from release-source and continues
to verify the already-deployed validator/library identity read only.

Action 9 is not deployment. Its repository-controlled tool reads the clean
exact-commit release source, deployed validator/library, current manufacturer
artifacts, immutable dataset selection, inventory, and reviewed Action 8 PASS
evidence. Runtime content is not published or changed. The sole permitted
mutation is a private invocation-owned Action 9 Evidence Report directory under
`/tmp`. No release upgrade, installer, generator, service action, staging,
retransmission, rollback, or later action belongs to this boundary.

The bounded corrected-manufacturer-validator checkpoint is owned only by
`tools/hioc-pe3-action8-validator-deploy.sh`. It is not a release upgrade. It
requires release-source already synchronized to the approved full commit, then
proves source Git/worktree identity and the independently frozen validator blob.
An exact runtime match is `NOOP_IDENTICAL`; otherwise a safe existing validator
is backed up privately and replaced atomically at owner/group
`jazofv1:jazofv1`, mode `0700`, with file and directory durability checks.
Source synchronization and validator deployment are separate review/STOP
boundaries. Neither boundary authorizes Action 8.

The Action 8 permission correction changes the governed validator source, not
the generated production artifacts or their exact `0600` requirement.
Production runtime must not be edited ad hoc. Source synchronization, supported
runtime deployment/identity proof, and any later Action 8 attempt require their
own reviewed authorizations. The Action 8 wrapper is unchanged, so its bootstrap
script-blob trust anchor does not change.

The active PE-3 Action 8 bootstrap trust gate freezes the independently reviewed
diagnostic-retention wrapper blob
`482f83584a62be2f02b2a73af4e78b0f4ebf447a`. The prior stale identity blocked
preparation before execution. Correcting the repository contract does not
prepare or execute synchronization, deploy runtime code, require transport
staging, or authorize Action 8 or Action 9.

Action 8 no longer depends on the undeclared host utility `/usr/bin/time`.
Performance instrumentation is owned by the already-required governed Python
runtime, so no host package installation is part of deployment. The changed
wrapper requires a new source-only bootstrap identity gate after publication;
it does not require runtime deployment or transport staging.

For PE-3 Production Action 5, the authoritative runbook invokes the checked-in
`tools/hioc-pe3-action5-deploy.sh`; do not reconstruct its deployment logic in
an interactive shell. The action changes only supported runtime code and release
backup state, reports bounded sanitized evidence, and stops before dataset or
configuration actions.
Before that invocation, separately authorized Action 5A must synchronize the
clean PI3 release-source checkout to the exact approved commit and prove the
script's Git/worktree identity. Action 5A stops without deployment; Action 5B
owns the supported upgrade.

Manufacturer protection across that upgrade is semantic: empty, private,
correctly owned installer scaffolding may be created or mode-normalized, but
payload, sidecar/status, symlink, unexpected-entry, and configuration changes
are prohibited. The initial Action 5B deployment passed runtime validation but
hit the former scaffolding false positive. It remains deployed; rollback is not
recommended. A separately bootstrapped read-only Action 5C validates and closes
the existing deployment without repeating it. Its bootstrap boundary is Action
5C-A: clean exact target synchronization plus Action 5C script identity, then a
mandatory stop. Action 5C-B is prepared only after reviewed Action 5C-A PASS and
separate authorization.

Action 6 uses a separately bootstrapped repository-controlled installer. Action
6-A synchronizes and proves `tools/hioc-pe3-action6-install.sh`, then stops.
Action 6-B alone may create the immutable dataset version through a private
same-filesystem staging directory and no-replace atomic publication. It does
not activate configuration, clean transport staging, or invoke Action 7.

Action 7 uses the same split trust boundary. Action 7-A performs only clean
release-source synchronization and exact identity proof for
`tools/hioc-pe3-action7-activate.sh`, then stops. Action 7-B is separately
authorized and changes only the runtime `MANUFACTURER_DB_PATH` setting after
proving the exact Action 6 immutable dataset. It preserves unrelated
configuration, creates a private durable backup when mutation is needed,
publishes atomically, and does not deploy code, reload services, touch transport
staging, modify the immutable dataset, generate sidecars/status, or invoke
Action 8.

Action 8 is not a release deployment. Its repository-controlled wrapper invokes
the already deployed manual manufacturer generator only after source/runtime,
configuration, installed dataset, inventory, output, protected-state, and
evidence gates pass. Because PI3 currently predates the wrapper, a separate
source-synchronization/script-identity bootstrap must pass before the mutating
action can be considered. The bootstrap only fast-forwards the clean release
source to the explicitly supplied and validated operator-approved full 40-hex
post-push commit, proves exact script identity, and stops. Action 8
does not use `release/upgrade.sh`, alter deployed code, or chain Action 9.
It creates its own private temporary evidence directory only after deployment,
source, runtime, configuration, installed dataset, inventory, and output
preconditions pass; no Action 5/5C evidence directory is an input.
Transport staging is transient pre-install state and is not consumed or required
after Action 6 immutable publication and Action 7 activation. Its absence does
not authorize recreation or retransmission and does not weaken installed-dataset
identity validation.

Action 8 generator failures now retain a private, structured failure artifact
without deploying code or exposing raw generator streams. The wrapper publishes
performance first and `generation-failure.json` last, records bounded root-cause
and output-mutation evidence, removes raw captures, and stops. This repository
change does not authorize synchronization, deployment, generation, or Action 9;
the changed wrapper requires a separate post-push bootstrap identity gate.

## Document Ownership

This document owns the repository-to-production workflow, source and runtime boundaries, operator responsibilities, synchronization expectations, and production acceptance boundary. Detailed commands remain in [INSTALL.md](INSTALL.md) and packaging mechanics remain in [RELEASE.md](RELEASE.md).

## Deployment Boundaries

| Boundary | Role |
| --- | --- |
| Windows development repository | Authoritative development workspace; changes are validated, committed, and pushed here. |
| GitHub `main` | Shared authoritative Git history. |
| `/home/jazofv1/hioc-release-source` | PI3 Git checkout used for release validation and supported deployment execution. |
| `/home/jazofv1/hioc` | Non-Git production runtime containing deployed files and persistent runtime data. |

The supported flow is:

```text
Windows repository -> GitHub main -> PI3 release source -> validated upgrade -> non-Git runtime
```

Codex operates only in the Windows repository. The operator performs PI3 synchronization, deployment, rollback, and production evidence capture. Direct Git operations inside `/home/jazofv1/hioc` are unsupported.

## Supported Workflow

1. Validate repository changes.
2. Update the Master Plan and affected focused documentation.
3. Commit related code and documentation together.
4. Push `main` and verify a clean Windows working tree.
5. Operator verifies a clean, non-divergent PI3 release-source checkout and fast-forwards it to `origin/main`.
   When a governed production script may be absent or older on the target, this
   synchronization and script-identity proof is a separate authorization gate.
6. Operator runs `release/validate.sh` and the supported `release/upgrade.sh` when runtime files changed.
7. Operator runs `/home/jazofv1/hioc/pi4/validate_pi4.sh` and any checkpoint-specific validation.
8. Operator captures production evidence and commits required closeout documentation.

Documentation-only source changes are excluded from the deployed runtime by `pi4/install_pi4.sh`. Whether to run a production upgrade for such a commit must follow the operator handoff and the established release workflow; do not copy documentation ad hoc into the non-Git runtime.

## Preservation and Recovery

Upgrade preserves `config`, `state`, `history`, `logs`, and `backups`. Supported rollback uses `release/rollback.sh` and excludes `.git`. Source recovery comes from GitHub, the release-source checkout, or an approved release package. Runtime recovery comes from release backups and preserved persistent data. See [RECOVERY_BASELINE.md](RECOVERY_BASELINE.md).

## Production Validation Expectations

Production acceptance uses the deployed validator, cron inspection, fresh state, logs, generated artifacts, and checkpoint-specific evidence. A successful repository test does not prove production behavior. A production observation does not prove an internal implementation invariant unless the artifact exposes it.

## Operations Acceptance Standard

A release is not complete until repository documentation answers what exists, why it exists, how it runs, how it is validated, and how it is recovered without requiring SSH discovery. The actionable checklist is authoritative in [HIOC_MASTER_PLAN.md](HIOC_MASTER_PLAN.md#operations-acceptance-standard). Any required production verification must be captured in an Evidence Report and committed back to the repository.
# PE-4.0B.2a isolated runtime (governance only)

The governed design is CASE A in
`PE4_ISOLATED_RUNTIME_DEPENDENCY_CONTRACT.md`. A future separately authorized
deployment must build a new versioned environment from `requirements-pe4.lock`
using the exact verified offline wheel, validate it, deploy the reviewed client,
then atomically update the managed active pointer. It must not modify system
Python, install globally, use live indexes, inherit system site packages, or
access Home Assistant. No deployment is authorized by this checkpoint.

The implementation is split across the repository-controlled A-G tools listed
in `PE4_ISOLATED_RUNTIME_LIFECYCLE.md`. General release deployment must preserve
`runtime/pe4` unchanged; PE-4 tools alone own its immutable environments and
active pointer. Route proof precedes mutation, transfer stops before install,
and publication stops before any authenticated execution.

The Action A Windows correction removes the former POSIX `/tmp`, mode, and
directory-fsync assumptions. Cache and sanitized evidence now share the
Known-Folder-rooted, current-user-only DACL hierarchy, while Actions B-G retain
their Linux owner/mode/fsync contract.

The first Action A attempt stopped before acquisition because its child
Windows PowerShell process could not load the ACL cmdlets. The corrected
deployment boundary uses .NET `DirectoryInfo`/`FileInfo` ACL methods, starting
from the existing descriptor and validating protected, non-inherited,
current-SID-only FullControl after persistence. The ordinary `HIOC` directory
left by that attempt is hardened in place before `artifacts/pe4` is created.
Action A remains incomplete and this correction authorizes no retry.

Action A later completed with production PASS. Action B creates only one
private PI3 `/tmp` directory and transfers the exact frozen wheel and lock; it
does not synchronize or alter either source or runtime tree. The corrected tool
uses the fixed durable cache, system OpenSSH, strict noninteractive identity,
separate partial names, remote owner/mode/digest validation, and result-last
partial-state evidence. Separate publication and authorization remain required.

Action B additionally ignores ambient OpenSSH configuration, pins direct
numeric PI3 port 22 transport, and uses only fixed profile known-hosts and
Ed25519 identity files. It never changes source/runtime deployment trees.
Result publication is complete only after exact post-rename digest and
durability confirmation; repository correction still authorizes no transfer.
## PE-4 Action B Windows identity prerequisite

Before Action B can be prepared, execute only the separately published and
authorized `tools/hioc-pe4-windows-ssh-identity-provision.py` from the governed
Windows repository with its sole `--governance-commit <40-hex>` argument. It
does not contact PI3. PASS establishes the fixed local Ed25519 pair and a
sanitized fingerprint; the operator must STOP. PI3 authorization of that exact
public key and Action B transfer require later separate checkpoints. Manual key
generation, target overrides, agent use, identity reuse, and cleanup of a
partial published state are prohibited.

Provisioning remains blocked until the corrected evidence lifecycle is
published and separately prepared. A result rename alone is not success: the
exact payload, digest, file type, non-reparse state, and protected DACL must be
reread and confirmed after publication. Cleanup state is finalized before any
failure result is constructed, and rename uncertainty never authorizes an
overwrite or a second contradictory result.

The next provisioning release also rejects every existing Windows directory
entry without following reparse targets and atomically publishes without
replacement. It preserves the historically governed dedicated pair
`.ssh/id_ed25519`/`.ssh/id_ed25519.pub`, which is the exact Action B identity
contract. Publication of this repository correction does not provision a key,
authorize it on PI3, or execute Action B.

Evidence deployment semantics now distinguish uncertain completed publication
from a no-replace collision. Exact final confirmation reconciles an error only
when `.result.tmp` is also proven absent without following reparse targets.
Retained or indeterminate temporary state leaves publication false and does not
authorize overwrite, cleanup, a second result, key provisioning, or Action B.

The initial production provisioning attempt also exposed a Windows-format
compatibility defect before either key was published: system OpenSSH emits a
single CRLF-terminated public record. The corrected release accepts that native
terminator but rejects bare, embedded, or repeated line endings and malformed
records, and parses the native commented derived-public record without a
synthetic field. Retry requires correction publication and separate preparation.

## PE-4 Action B remote publication gate

The final wheel, lock, and `result.json` use Linux
`renameat2(RENAME_NOREPLACE)` inside the private staging directory. Evidence
temporary creation is `O_EXCL|O_NOFOLLOW`; all existing destination object
types fail closed. Deployment state advances only after exact final metadata,
identity, durability, and disappearance of the invocation-owned partial or
temporary source confirm. A reported rename error uses the same proof and can
never authorize overwrite, cleanup, or a contradictory result.

Action B ingress is SSH streaming, not SCP publication. The remote Python sink
uses a no-follow directory descriptor and exclusive, no-follow partial creation
before accepting bytes; it validates the exact length and digest and fsyncs the
owned partial. Local deployment preflight pins the reviewed operator/profile,
`ssh.exe`, SSH key pair and fingerprint, and numeric PI3 trust identity.
Evidence confirmation is three-state: `NOT_PUBLISHED`, `CONFIRMED`, or
`UNCERTAIN`; uncertain state preserves the directory and authorizes no later
action.

Windows OpenSSH executable drift is handled through a reviewed single-hash
trust-anchor refresh, never by relaxing the Action B transport gate. The
reviewed System32 Microsoft-signed `OpenSSH_9.5p2` identities supersede stale
hashes; exact servicing causality remains unproven. This correction neither
executes a replacement transfer nor recreates historical temporary staging.

Action D must not consume the Action B transfer by ordinary pathname. The
published tool creates and validates its own private input snapshot, retains
directory identities through construction and cleanup, and runs venv/pip with
an explicit network-free environment. The snapshot is never a deployment
artifact and is removed after confirmed installation. A retained construction
may proceed to Action E only with the exact confirmed Action D evidence and
`.hioc-action-d-eligibility.json` marker. This correction does not authorize
Action D, Action E, or any production deployment.
## PE-4 replacement Action B publication and disposition boundary

The prior replacement authorization is consumed. The first invocation stopped
before transfer with `REMOTE_STAGING_IDENTITY_INVALID` after creation of the
empty, private PI3 directory `/tmp/hioc-pe4-artifact-transfer-g_jrlqkl`
(UID/GID `1000/1000`, mode `0700`, device `45826`, inode `131762`). It made no
runtime mutation and required no rollback. Preservation was the disposition
at that checkpoint; current operator checks report the directory ABSENT.

Publication of this correction is not execution authority. After publication,
the order is PI3 release-source synchronization, failed-staging disposition
review, fresh readiness review, and a new exactly-once replacement Action B
authorization. The governed wrapper has one tool launch after all prechecks;
it rejects malformed/nonzero Git divergence, validates all Action B PASS
markers, and keeps a successful new transfer directory for later Action D
readiness only.

The `1bf339d` wrapper itself required a source correction after one authorized
precheck-only invocation. Its Python source was flattened by Windows
PowerShell's native argument serialization, yielding `NameError: tools` before
the Action B process-launch site. Publication of the structured-argument
correction does not revive that authorization. It must be followed by fresh
readiness and one new explicit execution authorization; no PI3 cleanup or
forensics is required for the precheck-only event. The later invocation uses
managed PowerShell Core, not legacy Windows PowerShell 5.1, because only the
former provides the required discrete `ArgumentList` transport.
## Action D failure diagnostics

Action D failure evidence is private, retained, and diagnostic-only. It is not a
deployment result and cannot authorize Action E or runtime publication.

## PE-4 D-PREP runtime hierarchy boundary

D-PREP is the sole lifecycle action that may create the PE-4 runtime hierarchy
under the existing non-Git HIOC runtime. Ordinary release upgrade and rollback
continue to exclude `runtime/pe4`; D-PREP PASS is a STOP, not runtime deployment
or Action D authority.

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
