# HIOC Master Plan

## Compatibility roadmap governance synchronization - 2026-10-06

The accepted Compatibility Resilience implementation and dependency audit at
`8187114c7233be82b188f0fc03b93a022787e7bb` remain unchanged. This repository-only
checkpoint completes the permanent principles, roadmap, current lifecycle,
sequencing and future operator-awareness commitments below. It does not repeat
the audit, change runtime behavior, deploy, access PI3/PI5/HA, use credentials,
execute corrected PE-4.0B.2b or begin PE-4.0C.

The [Implementation Status](#implementation-status) and
[Next Planned Task](#next-planned-task) sections are authoritative for current
state and sequencing. Earlier checkpoint narratives are explicitly historical.
[COMPATIBILITY_RESILIENCE.md](COMPATIBILITY_RESILIENCE.md) owns the detailed
matrix, probes, algorithms, fields, schemas, mechanics and audit inventory;
this Master Plan owns principles, roadmap, state, sequencing and completion rules.

# Historical Checkpoint Chronology

The following dated checkpoint narratives preserve the state and authority at
the time written. Their older NOT STARTED, pending or next-task statements do
not supersede the current Implementation Status and Next Planned Task sections.

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

D/E/F/G remain PASS/CLOSED; Action E handoff ACCEPTED. PE-4.0B.2a is now
PASS/CLOSED; 2b NOT STARTED; PE-4 NOT COMPLETE; Phase 7A ACTIVE; rollback
NOT PERFORMED. F/G were not rerun; rollback and 2b were not executed. No credential
was persisted in repository evidence. This checkpoint accessed no PI3/PI5/HA and
reran no authenticated client. Historical/runtime/implementation identities remain
unchanged. The preparation record remains immutable pre-execution evidence with
2a NOT_STARTED; the new closure record supplies the post-execution state. Next
work requires separate governance; no 2b preparation or execution is authorized here.

## PE-4.0B.2a successor authenticated proof preparation - 2026-10-05

Comprehensive repository-only review PASS: credential, shared absolute network
deadline, REST partial progress/cleanup, strict JSON, WebSocket receive/send/cleanup,
interruption RC 130, exact authentication schemas, and absence of 2b commands.
No implementation or test changes were required.

[Canonical preparation record](../governance/pe4/pe4-0b2a-successor-preparation.json).

D/E/F/G remain PASS/CLOSED, E handoff ACCEPTED; successor CORRECTED /
REPOSITORY_ONLY / NOT DEPLOYED. 2a is NOT STARTED / PREPARED FOR SEPARATE
AUTHORIZATION; 2b NOT STARTED; PE-4 NOT COMPLETE; Phase 7A ACTIVE; rollback
NOT PERFORMED. Historical F/G identity/runtime and accepted handoff/lock are
unchanged. No authenticated execution, PI3/PI5/HA access, F/G rerun or rollback
occurred. Package installation, another environment and pointer mutation are
excluded. Stop after the separately authorized proof; chain no later action.

## PE-4.0B.2a consolidated client boundary correction - 2026-10-05

All five successor boundary defects are corrected together: absolute REST deadline,
duplicate-safe JSON, decoder recursion normalization, receive-coroutine ordering,
and bounded network interruption. Prior parser/getpass/timing/send corrections remain.
[Canonical successor identity and validation scope](PE4_HOME_ASSISTANT_ACCESS_PRIVACY_CONTRACT.md#pe-40b2a-consolidated-client-boundary-correction---2026-10-05).

D/E/F/G remain PASS/CLOSED; Action E handoff ACCEPTED. Historical F/G identity and
runtime are unchanged. Successor remains CORRECTED / REPOSITORY_ONLY / NOT DEPLOYED.
2a is NOT STARTED / NOT PREPARED; 2b NOT STARTED; PE-4 NOT COMPLETE; Phase 7A ACTIVE;
rollback NOT PERFORMED. No authenticated execution occurred and preparation has not
passed. Next: separately authorized comprehensive successor authenticated proof
preparation review. No preparation record or operator command is issued here.

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

Successor remains CORRECTED / REPOSITORY_ONLY / NOT DEPLOYED; 2a NOT STARTED /
NOT PREPARED. Repeat preparation review separately. D/E/F/G PASS/CLOSED;
E handoff ACCEPTED; 2b NOT STARTED; PE-4 NOT COMPLETE; Phase 7A ACTIVE;
rollback NOT PERFORMED. No authenticated operation occurred.

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

Successor is CORRECTED / REPOSITORY_ONLY / NOT DEPLOYED. 2a remains NOT STARTED /
NOT PREPARED; separate preparation review must be repeated. D/E/F/G PASS/CLOSED;
E handoff ACCEPTED; 2b NOT STARTED; PE-4 NOT COMPLETE; Phase 7A ACTIVE;
rollback NOT PERFORMED. Historical F/G runtime is unchanged.

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

Successor is CORRECTED / REPOSITORY_ONLY / NOT DEPLOYED; 2a NOT STARTED /
NOT PREPARED. Repeat successor authenticated proof preparation review in a
separate checkpoint. D/E/F/G PASS/CLOSED; E handoff ACCEPTED; 2b NOT STARTED;
PE-4 NOT COMPLETE; Phase 7A ACTIVE; rollback NOT PERFORMED.

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

## Historical F/G client and successor source boundary — 2026-10-05

governance/pe4/historical-fg-client.json durably pins the immutable closed
F/G client: F consumer 2a5e6299a0806c3f3d7c3bc11c84fddc8492333c,
Git blob 09d66b041796dd6ec2efdb88f7a71b3f99e9a27a, SHA-256
5c2886452a61185c7e7329777dbd4fa3de4da98dd4793a1a84501bc30016879e,
runtime path /home/jazofv1/hioc/tools/hioc-pe4-ha-auth-capability.py.
Identity class is IMMUTABLE_CLOSED_ARTIFACT; F/G remain PASS/CLOSED.

The canonical tools/hioc-pe4-ha-auth-capability.py source remains unchanged
here but may evolve only through a separately reviewed successor checkpoint.
Historical identity tests and F fixtures now read the pinned F-consumer Git
artifact, not current source bytes. Other source/API tests review the current
client's behavior; runtime identities and prior evidence remain historical.
Changing source later neither rewrites nor invalidates F/G history.
F/G executors and their historical source verifier must not be rerun from
an evolved successor-client HEAD. Runtime common constants/verifier remain
unchanged. Future 2a source execution needs its own governance commit, blob,
SHA-256, source path and execution model; no successor identity exists yet
and no claim of historical F publication extends to a successor.

Repository-only preparation found the documented authentication-frame parser
defect before any authenticated execution. It remains unresolved: the published
client is valid historical evidence for G's credential-free contract but
unsuitable for authenticated 2a. No parser correction, deployment, duplicate
client, runtime mutation, F/G rerun or rollback occurs in this checkpoint.
Next: separately governed parser correction, then successor preparation review.

D/E/F/G PASS/CLOSED; Action E handoff ACCEPTED; 2a BLOCKED / NOT STARTED;
2b NOT STARTED; PE-4 NOT COMPLETE; Phase 7A ACTIVE; rollback NOT PERFORMED.

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

## Action G controlled preflight implementation — production NOT STARTED

Corrected G is implemented as a dedicated controlled runtime preflight. It
consumes the fixed successful F journal before runtime code, uses `-I -B -S`
and a restricted loader, performs no credentials or network validation, and
revalidates the published runtime before PASS. D/E/F remain PASS/CLOSED; G is
NOT STARTED pending native compatibility and separately authorized execution.

Next checkpoint: `ACTION_G_NATIVE_COMPATIBILITY_CHECK_READY_FOR_SEPARATE_AUTHORIZATION`.

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

Historical roadmap status `PE-4 NOT STARTED` preceded the accepted D/E lifecycle;
current PE-4 is in progress with E PASS/CLOSED and F/G NOT STARTED.

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

PE-4 remains in progress: Action E is PASS/CLOSED, while F/G and the later authenticated association proof remain NOT STARTED.

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

The architecture-matched native-validation prerequisite is PASS/CLOSED. Action E remains NOT STARTED; the next checkpoint is final repreparation under separate authorization, using the resulting documentation closure as current consumer candidate.

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

The startup/import design blocker is resolved in repository implementation. Production readiness remains open pending architecture-matched non-lifecycle validation; Action E remains NOT STARTED.

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

The producer/current preparation blocker correction now has a successful
operator-reported PI3 read-only compatibility proof. The synchronization/review
boundary is closed; Action E re-preparation is the next separately authorized step.

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

## Historical Action E preparation blocker correction

Read-only preparation identified a governance-binding blocker: Action E used its
current source commit to validate immutable D producer evidence. Normal closure
commits advance source while the accepted D handoff remains bound to its producer.
The repository-only correction separates mandatory current-consumer
`--governance-commit` from mandatory producer `--action-d-governance-commit`.

The compatibility guard proves actual commit identities without replacement
substitution, complete history, producer equality/ancestry and exact committed
D/common/lock blobs. Current checkout/source governance remains strict; the common
D eligibility equality contract, E runtime checks and E success schema are unchanged.
Local/native Windows focused and regression tests passed. The accepted D handoff
remains immutable, D/common/lock and F/G source are unchanged, and no PI3/PI5
access or production lifecycle action occurred during this implementation.

Replacement Action B remains PASS/CLOSED, Action C PASS exactly once, D-PREP
PASS/CLOSED and Action D PASS/CLOSED. Action E remains **NOT STARTED** and requires
separate authorization; Actions F/G remain NOT STARTED and unauthorized. No rollback
occurred. After implementation publication, the separately authorized PI3 source
synchronization and read-only D-to-E compatibility validation PASSed. Neither
that validation nor this documentation closure authorizes E execution.

The original implementation synchronization/read-only validation boundary
is now PASS/CLOSED as recorded above. Next checkpoint:
`ACTION_E_REPREPARATION_READY_FOR_SEPARATE_AUTHORIZATION`.

## Historical governed status — Phase 7A

Phase 7A is **ACTIVE / IN PROGRESS**. Passive Enrichment PE-0 through PE-3 are
complete; PE-4 is current and not complete. PE-4.0A and PE-4.0B.1 are
**COMPLETE / PASS**. Action A, dedicated Windows SSH identity provisioning,
PI3 public-key authorization, historical successful replacement Action B, and Action C
are **COMPLETE / PASS**. Action D is **PASS / CLOSED** after its third actual
execution. The first two failures remain historical; the later pre-execution
recovery stop did not launch Action D and is not an execution.

`PE-4.0B.2a-D-PREP` native validation and production execution are **PASS / CLOSED**.
Its hierarchy prerequisite remains compliant. Action E is **PASS / CLOSED**
after exactly one authorized production invocation under consumer
`1c1698f009457baa1c3b548db31916559fcc2fc8`.
Actions F/G, authenticated
PE-4.0B.2a proof, PE-4.0B.2b, PE-4.0C, the HA association adapter, and PE-4
production deployment remain **NOT STARTED** or **NOT COMPLETE** as applicable.
The older checkpoint narratives below retain their historical status at the
time written and are not current lifecycle assertions.

Current correction status: Windows validation passed; source synchronization to PI3
at `c5181a0d65da294e5db2dbd6795f20889b972a22` and corrected native D-PREP
revalidation are complete. Native result: 115 run / 115 pass / 0 skip / 0 fail /
0 error. D-PREP subsequently executed successfully at governance commit
`5783951fdd33e0bb476c0fa53022633adddf1b8c`: three absent hierarchy components
were CREATED_CONFIRMED, evidence CONFIRMED, process RC 0, and post-validation PASS.
The separately authorized third Action D execution subsequently PASSed; the
combined suite has not executed on PI3.
Replacement Action B is **PASS / CLOSED**; accepted fresh transfer input is
`/tmp/hioc-pe4-artifact-transfer-l3t4crcg`. Historical B staging remains unavailable.
Action D is **PASS / CLOSED** with confirmed retained construction and independent
review PASS. Action C and D-PREP were not rerun. Action E remains NOT STARTED
and unauthorized; PI3 synchronization/read-only D-to-E compatibility validation
is PASS/CLOSED. Separately authorized E re-preparation against the resulting
documentation closure consumer commit is the next checkpoint.

## PE-4.0B.2a Action B Windows SSH ACL compatibility correction

Read-only workstation forensics proved that Action B incorrectly applied the
HIOC private-object ACL model to shared Windows OpenSSH objects. The corrected
preflight now uses three fail-closed roles: `.ssh` accepts only the governed
inherited SYSTEM, Administrators, and current-operator FullControl layout;
`known_hosts` accepts only the governed protected explicit SYSTEM and
Administrators FullControl plus current-operator Modify/Synchronize layout;
and both dedicated key files retain the protected, explicit,
current-operator-only FullControl model. Ownership, object type, reparse state,
ACE principals, rights, inheritance, and propagation are independently checked
for every role. No ACL is normalized or changed. Action B remains **BLOCKED /
NOT EXECUTED** and the PI3 primitive preflight remains **NOT STARTED**.

## PE-4.0B.2a Action B invocation-identity correction

Fresh readiness review found whole-directory substitution, duplicate numeric
known-host ambiguity, and missing runtime ACL enforcement. The corrected tool
binds every remote command to the creation-time device/inode/UID/mode
token through a no-follow directory descriptor, requires exactly one governed
numeric PI3 host record, and validates the strict ACL contract for `.ssh`, the
key pair, and `known_hosts`. This is repository-only. Action B remains
**BLOCKED / NOT EXECUTED**. The production PI3 primitive preflight remains a
separate future checkpoint.

## PE-4.0B.2a Action B ingress and confirmation correction

Fresh readiness review rejected direct SCP-to-predictable-partial ingress,
path-only local transport trust, and binary evidence publication state. The
repository now streams the fixed wheel and lock over isolated SSH into
exclusive, non-following, directory-fd-relative sinks; pins the reviewed
Windows operator/profile, SSH executable, key pair/fingerprint/comment, and
numeric PI3 host trust; and reports evidence as **NOT_PUBLISHED**,
**CONFIRMED**, or **UNCERTAIN** with a persistent **AWAITING_CONFIRMATION**
marker. This is repository-only. Action A, identity provisioning, and PI3
authorization remain **COMPLETE / PASS**. Action B remains **BLOCKED / NOT
EXECUTED** and all later PE-4 actions remain **NOT STARTED**.

## PE-4.0B.2a Action B remote publication correction

Fresh Action B preparation found that temporary evidence creation could follow
a raced link and that ordinary `mv` could replace a destination raced into
place. Wheel, lock, and result publication now use the governed Linux
`renameat2(RENAME_NOREPLACE)` primitive. Evidence creation uses exclusive,
non-following creation. Every success path, including rename-error
reconciliation, requires the exact durable final object and true non-following
absence of the invocation-owned source. Collisions are preserved without
overwrite, deletion, or a second result attempt. Action A, Windows SSH identity
provisioning, and PI3 public-key authorization remain **COMPLETE / PASS**.
Action B remains **BLOCKED / NOT EXECUTED**; Action C, Actions D-G,
PE-4.0B.2a, PE-4.0B.2b, and PE-4.0C remain **NOT STARTED**.

## PE-4.0B.2a SSH identity evidence-lifecycle correction

Execution preparation found the **PE-4 WINDOWS SSH IDENTITY PROVISIONING
FAILURE-EVIDENCE ORDERING AND INVOCATION-CLEANUP DEFECT**. The corrected
repository lifecycle retains every invocation child immediately after creation,
even if ACL initialization fails; completes governed cleanup before constructing
failure evidence; and publishes evidence through one prepare, atomic publish,
and exact content/DACL reread confirmation attempt. A reported rename failure is
accepted only when the exact intended final result independently confirms.
Unexpected or ambiguous results are never overwritten, and no second
contradictory result is published. Terminal and confirmed persistent state now
share the final publication, pair-confirmation, cleanup, result, error, stage,
and rollback fields. This correction is repository-only. Provisioning remains
**NOT EXECUTED**, Action B remains **BLOCKED / NOT EXECUTED**, and Action C and
all later PE-4 actions remain **NOT STARTED** pending publication and a fresh
execution-preparation checkpoint.

## PE-4.0B.2a dedicated Action B identity governance

Read-only Windows discovery established `CASE C`: no suitable existing private
key exists at the fixed Action B identity path. The repository now implements
the separately gated provisioning lifecycle at
`tools/hioc-pe4-windows-ssh-identity-provision.py`. It fixes system
`ssh-keygen.exe`, Ed25519, the exact comment and empty-passphrase contract,
current-profile paths, protected current-operator DACLs, invocation-owned
staging, public-first/private-last publication, bounded fingerprint evidence,
and fail-closed partial-publication behavior. This repository implementation is
not execution. Action A remains **COMPLETE / PASS**; Action B remains **BLOCKED
/ NOT EXECUTED** on the missing identity; Action C, Actions D-G, PE-4.0B.2a,
PE-4.0B.2b, and PE-4.0C remain **NOT STARTED**. PI3 public-key authorization and
Action B execution remain distinct future checkpoints.

## PE-4.0B.2a PI3 execution architecture

PE-4 Home Assistant API consumption belongs to the HIOC execution environment
on PI3 NUT&PIHOLE. PI5 HA remains the remote supported API source at
`192.168.100.251:8123`; it is not a HIOC Python or dependency deployment host.
The client separates PI3 execution-host identity from the fixed PI5 endpoint.
The earlier PI5-local dependency precheck remains valid historical evidence of
the superseded architecture. Credential-free PI3 runtime preflight, a separate
one-endpoint route proof, dependency deployment, and 2a execution remain **NOT
STARTED**. PE-4.0B.2b and PE-4.0C remain **NOT STARTED**.

## PE-4.0B.2a WebSocket redirect-suppression correction

Runtime-precheck preparation found the **PE-4.0B.2A WEBSOCKETS
REDIRECT-SUPPRESSION ENFORCEMENT DEFECT — CLIENT ACCEPTS A DEPENDENCY API THAT
MAY FOLLOW HANDSHAKE REDIRECTS WITHOUT AN EXPLICIT ZERO-REDIRECT CONTROL**. The
corrected client binds `websockets.connect()` to its already-connected governed
target socket. The supported dependency refuses every handshake redirect when
a pre-existing socket is supplied, before another endpoint can be contacted.
Compatibility must be proved before credential acquisition and the future
runtime precheck must emit `REDIRECT_SUPPRESSION_CAPABILITY=PASS`. The correction
has not been deployed or executed; PE-4.0B.2a remains **NOT STARTED**, and runtime
precheck preparation remains blocked until commit and push.

## PE-4.0B.2a WebSocket receive-bound correction

Runtime-precheck preparation found that the preferred websocket-client path
checked 65,536 bytes only after `recv()` had materialized a complete message.
This is the **PE-4.0B.2A WEBSOCKET-CLIENT MESSAGE-BOUND ENFORCEMENT DEFECT —
PREFERRED DEPENDENCY PATH APPLIES THE 65,536-BYTE LIMIT ONLY AFTER UNBOUNDED
MESSAGE MATERIALIZATION**. The corrected client removes websocket-client and
accepts only a compatible `websockets` API with dependency-enforced
`max_size=65536`, explicit proxy suppression, and bounded timeouts. Missing or
incompatible support stops before credential acquisition. The correction has
not been deployed or executed; PE-4.0B.2a remains **NOT STARTED**, and runtime
precheck preparation remains blocked until commit and push.

## PE-4.0B.2a repository-controlled client implementation

The repository now contains the standalone, terminal-only client
`tools/hioc-pe4-ha-auth-capability.py` and comprehensive offline tests. It
implements the frozen `REST_THEN_WEBSOCKET_2A` proof, closed output/privacy
schema, target and proxy gates, secure in-memory credential prompt, explicit
network bounds, and approved-library WebSocket authentication without any 2b
command. The implementation has **NOT been executed against PI5**, is not
deployed, and has no runtime copy. PE-4.0B.2a remains **NOT STARTED** until a
separately reviewed dependency/identity, deployment-or-source-execution, and
operator-invocation checkpoint is authorized. PE-4.0B.2b and PE-4.0C remain
**NOT STARTED**.

## PE-4.0B.2a authenticated API interface-contract freeze

Official Home Assistant research freezes `REST_THEN_WEBSOCKET_2A`: authenticated
`GET /api/` must return only HTTP 200 JSON `{"message":"API running."}`, then
`ws://192.168.100.251:8123/api/websocket` must complete only the documented
`auth_required` → `auth` → `auth_ok` exchange. No command, registry, state,
config, subscription, or response body is published. PE-4.0B.2a remains **NOT
STARTED** pending separately governed review, publication, and execution of the
repository-controlled client; 2b and PE-4.0C remain **NOT STARTED**.

## PE-4.0B.1 Home Assistant production preflight completion

PE-4.0B.1 is **COMPLETE / PASS**. The operator-run PI5 preflight proved an
`HA_TERMINAL_ADDON` execution context with interactive zsh, Home Assistant OS
18.1, Core 2026.8.1, supported and healthy Supervisor 2026.07.5, and the exact
no-proxy endpoint `http://192.168.100.251:8123`. TLS is not applicable to that
currently governed HTTP endpoint. Bash, Python 3.14.5, curl, OpenSSL, jq, the HA
CLI, and a secure non-echoing prompt are available; no dedicated WebSocket
client was detected. No credential, registry, `.storage`, database, live-state,
configuration, or production mutation was involved. Rollback recommendation is
FALSE and no rollback occurred.

The earlier preflight stopped at `HA_DEPLOYMENT` with
`UNSUPPORTED_HA_DEPLOYMENT`. It remains historical evidence of the
**PE-4.0B.1 HA CLI PARSER-CONTRACT DEFECT — RECURSIVE/NONAUTHORITATIVE STATE
FIELD USED FOR DEPLOYMENT VALIDATION**. The corrected operator procedure—not
active repository code—subsequently produced the accepted PASS above.

Phase 7A remains **ACTIVE**; PE-3, PE-4 prerequisite/governance discovery,
PE-4.0A, and PE-4.0B.1 are complete. PE-4.0B.2, PE-4.0C, the association
adapter, and production deployment remain **NOT STARTED**. PE-4 overall is not
complete. The next separately authorized checkpoint is preparation only of
PE-4.0B.2a authenticated API/capability proof; it cannot continue automatically
to PE-4.0B.2b registry/schema discovery.

## PE-4.0A Home Assistant access and privacy contract

PE-4.0A is **COMPLETE in repository governance**. The authoritative
[access and privacy contract](PE4_HOME_ASSISTANT_ACCESS_PRIVACY_CONTRACT.md)
defines supported-interface candidacy, least-privilege credentials, read-only
schema discovery, household-data exclusion, count-only sanitized evidence,
identity and Asset authority, bounded failures, and private result-last
evidence. No live Home Assistant or PI5 access occurred.

Phase 7A remains active. PE-3 remains complete. PE-4.0B live/schema discovery
has completed only its PE-4.0B.1 preflight; PE-4.0B.2 and PE-4 implementation remain **NOT STARTED** and separately gated.

## PE-4 repository discovery checkpoint

PE-4 — Home Assistant Association remains **PLANNED / NOT STARTED**. Repository
forensics confirm that it is a read-only trusted-integration association layer,
not a new identity engine: Home Assistant device/entity identifiers and
area/name candidates may become local provenance-backed association evidence,
but cannot replace canonical HIOC identity, operator Asset fields, liveness,
health, or availability semantics. Live Home Assistant access, schema approval,
implementation, deployment, and production validation remain separately gated.

The authoritative passive-enrichment architecture previously retained an active
pre-completion PE-3 status. That stale status is corrected to record PE-3 and
Actions 1–10 complete. This repository-only correction performs no PE-4
implementation or production access and preserves Phase 7A and all later roadmap
checkpoints.

## PE-3 completion checkpoint

PE-3 is **COMPLETE**. Actions 1–10 are **COMPLETE**. Action 10 completed
administratively with disposition `NOOP_ALREADY_ABSENT`: no PI3 or PI5 action,
staging recreation or deletion, production mutation, or Action 10 Evidence
Report was required. Action 9 remains the final production validation and its
Evidence Report at `/tmp/hioc-pe3-action9-Bb6vGrmm` remains the final PE-3
production evidence. Rollback remained FALSE and was not performed. Transport
staging remains absent and retransmission remains unnecessary.

Phase 7A remains the active parent phase. PE-3 closure does not begin the next
checkpoint; future performance-baseline work, PE-10, and every other governed
roadmap commitment remain planned and separate.

## Historical PE-3 Action 10 administrative no-op closure governance

Action 10 is classified **CASE C — ACTION 10 ADMINISTRATIVE NO-OP CLOSURE**.
Its original purpose was only deletion of the transient two-file transport
directory after validation. Action 6 already consumed, validated, and durably
published the immutable dataset; Action 7 selected it in configuration; Action
8 retired the staging dependency after the directory was confirmed absent; and
Action 9 completed the final read-only production validation and Evidence
Report. Installed immutable dataset plus active configuration remain
authoritative. Retransmission or staging reconstruction would add no provenance
or safety value.

No PI3 action, absence recheck, cleanup, mutation, or new Action 10 Evidence
Report is required. Action 8 and Action 9 evidence remain preserved but are not
Action 10 inputs. The administrative disposition is `NOOP_ALREADY_ABSENT`, with
rollback FALSE. This correction retires the active deletion/PASS ledger and
stale Action 9 timing/required-threshold wording. Action 10 remains **NOT
COMPLETE** until the correction is validated, committed, pushed, and the clean
published repository is verified. A later repository-only completion record
may then mark Actions 1–10 and PE-3 complete. Future performance-baseline work,
PE-10, and all other roadmap commitments remain separate and preserved.

## PE-3 Action 9 production completion checkpoint

The corrected governed Action 9 production validation is **PASS / COMPLETE**.
It returned `RESULT=PASS`, `ACTION9=COMPLETE`, and
`ROLLBACK_RECOMMENDED=FALSE`, with its private Evidence Report preserved at
`/tmp/hioc-pe3-action9-Bb6vGrmm`. Validation was read only and caused no
production mutation or rollback. Successful Action 8 evidence remains preserved
at `/tmp/hioc-pe3-action8-eZxNGrKa`.

Performance evidence recorded `12.467231` seconds and `146744` KiB with
`PERFORMANCE_RSS_SEMANTIC=TOTAL_PEAK_CHILD_RSS`, measurement status `MEASURED`,
baseline status `UNVALIDATED`, and observation `INSUFFICIENT_BASELINE`. Both
historical targets were exceeded, but
`HISTORICAL_TARGETS_PRODUCTION_ENFORCED=FALSE`; no replacement threshold was
introduced. Actions 1–9 are **COMPLETE**. Action 10 remains **NOT STARTED / NOT
PREPARED** until this completion checkpoint is committed and pushed and a
separate operator-safety/governance review is authorized. Transport staging
remains absent, retransmission remains unnecessary, and the future governed
performance-baseline checkpoint, PE-10, and every future-roadmap commitment
remain preserved.

## Historical PE-3 Action 9 performance-contract correction

The first Action 9 production attempt is **ATTEMPTED BUT NOT COMPLETE**. Source
refresh is **PASS / COMPLETE / CURRENT**. The attempt failed only at the former
combined `ACTION8_EVIDENCE_VALIDATION` stage; read-only forensics proved the
Action 8 result schema/count partition and protected snapshot passed, while the
measured `12.467231` seconds and `146744` KiB total peak child RSS exceeded
historical design targets. It created no Action 9 evidence directory, changed no
production state, and recommends no rollback.

The classification is **CASE D — BOTH CONTRACT AND MEASUREMENT DEFECTS**. The
four-second and incremental-RSS 48-MiB targets have no validated current PI3
baseline and are not hard production gates. Result validation, performance
syntax, insufficient-baseline assessment, and protected-snapshot validation are
now separate domains. A future versioned benchmark must define hardware,
workload, repetition/percentile method, and total-versus-incremental RSS before
hard limits can be authorized. Actions 1–8 remain complete; Action 10 remains
**NOT STARTED / NOT PREPARED**; all future-roadmap commitments are preserved.

## PE-3 Action 9 operator-safety and evidence-contract correction

Repository forensics reject the historical Action 9 inline block as **PE-3
ACTION 9 OPERATOR-SAFETY AND EVIDENCE-CONTRACT DEFECT — STALE EVIDENCE INPUT,
INTERACTIVE STRICT MODE, UNDECLARED TIMING DEPENDENCY, AND UNBOUNDED FAILURE
SEMANTICS**. It referenced an unrelated historical evidence prefix, could kill
an interactive parent shell, depended on unavailable `/usr/bin/time`, reran the
generator, and lacked private invocation evidence with bounded failures.

At that pre-attempt repository correction, the architecture assigned Action 9 only to
`tools/hioc-pe3-action9-validate.sh`. It validates the exact operator-supplied
Action 8 PASS evidence, uses its governed performance record without generation,
independently validates current production artifacts and protected-state
identity, and publishes a private result-last Evidence Report. Production is
read only; only invocation-owned Action 9 evidence may be written. Actions 1–8
remained complete, Action 9 was **NOT STARTED**, and Action 10 was **NOT STARTED
/ NOT PREPARED**. No production, rollback, staging, retransmission, or
future-roadmap action was performed by that correction.

## PE-3 Action 8 production completion checkpoint

The governed PI3 Action 8 execution at governance commit
`fa344828161e892523faa3da5d4cdf07d2e8e792` completed with `ACTION8=COMPLETE`,
`RESULT=PASS`, and `ROLLBACK_RECOMMENDED=FALSE`. The prerequisite source refresh
and corrected-validator deployment are **PASS / COMPLETE / CURRENT**. Private
Action 8 evidence is preserved at `/tmp/hioc-pe3-action8-eZxNGrKa`; it must not
be modified, deleted, reused, or cleaned. No rollback was performed. Transport
staging remains absent and unnecessary, and retransmission is not required.

Action 8 is **PASS / COMPLETE** and Action 9 remains **NOT STARTED**. In
accordance with the permanent completion and commit rules, this production
result must be validated, committed, pushed to `main`, and followed by a clean
synchronized-tree verification before any Action 9 preparation. PE-10, the PI3
+ PI5 abrupt power-loss/cold-boot checkpoint, and every other future-roadmap
commitment remain preserved.

## Historical PE-3 active Action 8 status-governance correction

At that pre-completion checkpoint, the active source-refresh/bootstrap contract
stopped repeating the earlier pre-execution state and recorded Action 8 as
**ATTEMPTED BUT NOT COMPLETE**, Action 9 as **NOT STARTED**, and reviewed source
refresh plus corrected-validator runtime deployment as prerequisites for a
separately authorized attempt. This section is retained as historical governance
evidence; current status is recorded in the completion checkpoint above.

## Historical PE-3 Action 8 corrected-validator deployment governance

The permission-class correction exposed a second defect: **PE-3 ACTION 8
CORRECTED VALIDATOR DEPLOYMENT GOVERNANCE GAP — NO BOUNDED VALIDATOR-ONLY
RUNTIME PUBLICATION CONTRACT**. The supported release upgrade is intentionally
too broad because it copies unrelated code, invokes installer behavior, manages
schedules/permissions, and runs engines.

Repository implementation now assigns only the corrected validator checkpoint
to `tools/hioc-pe3-action8-validator-deploy.sh`. The tool independently freezes
the reviewed validator, accepts exact identical runtime state as a no-op,
otherwise creates a private durable backup and performs same-directory atomic
publication with durability and final identity proof. It compares manufacturer
outputs, inventory, active configuration, and the immutable pair before/after
without exposing their contents. At that checkpoint, source refresh and runtime
deployment were **NOT EXECUTED** and required separate reviewed STOP boundaries;
Action 8 was **ATTEMPTED BUT NOT COMPLETE**, Action 9 was **NOT STARTED**, and
the prior rollback recommendation remained advisory with no rollback performed.
The current completion state is recorded above.

## Historical PE-3 Action 8 permission-contract corrective checkpoint

The third Action 8 attempt generated and identity-checked private
`manufacturer.json` and `manufacturer_status.json` files at exact mode `0600`,
with no temporary manufacturer artifacts, but dedicated validation stopped with
`MANUFACTURER_PERMISSION_ERROR`. Repository forensics classified this as
**PE-3 ACTION 8 MANUFACTURER INPUT PERMISSION-CLASS DEFECT — PRIVATE ARTIFACT
MODE RULE APPLIED TO INVENTORY INPUT**.

The correction keeps exact `0600` mandatory for both manufacturer artifacts and
retains the inventory rule prohibiting group/world writes. Available evidence
supported permission safety, not completed semantic validation. At that
checkpoint the rollback advisory was `TRUE`, no rollback had occurred, Action 8
was **ATTEMPTED BUT NOT COMPLETE**, and Action 9 was **NOT STARTED**. The current
completion state is recorded above; all future checkpoints remain preserved.

**Version:** 1.0  
**Status:** Active  
**Owner:** Jorge Azofeifa  
**Project:** Home Infrastructure Operations Center (HIOC)

---

## Purpose of this Document

This document is the authoritative roadmap for the HIOC project.

It defines the project's vision, guiding principles, architecture, implementation roadmap, and working agreements. When implementation decisions conflict with conversational guidance, this document takes precedence unless it is intentionally revised.

Every contributor, human or AI, should read this document before making changes to the project.

---

## Document Ownership

This document is the constitution of the project.

It owns:

- vision
- philosophy
- principles
- roadmap
- implementation phases
- current phase
- current objective
- next task
- working agreement

It should not contain detailed architecture, runtime procedures, network configuration, MQTT documentation, Home Assistant documentation, data model details, installation instructions, release procedures, design system rules, or dashboard implementation details. Those belong in the focused documents linked from [../README.md](../README.md).

The Master Plan explains how HIOC is built and evolves. [SYSTEM_REFERENCE.md](SYSTEM_REFERENCE.md) explains what HIOC is today. [OPERATIONS.md](OPERATIONS.md) is the authoritative runtime reference, [NETWORK_FOUNDATION.md](NETWORK_FOUNDATION.md) owns network dependencies, [DEPLOYMENT.md](DEPLOYMENT.md) owns deployment boundaries, and [INCIDENT_MODEL.md](INCIDENT_MODEL.md) owns incident semantics.

Update this document only when project direction, roadmap, phase, objective, next task, or implementation status changes.

---

# Vision

HIOC (Home Infrastructure Operations Center) is an operational platform for monitoring, understanding, documenting, and troubleshooting a home infrastructure.

Its primary purpose is **not** monitoring.

Its primary purpose is helping the operator immediately answer:

- What is happening?
- Why is it happening?
- What is affected?
- What should I do?
- What happened while I was away?

HIOC should behave like a miniature Network Operations Center (NOC), providing operator-oriented information instead of raw metrics.

---

# Design Principles

These principles override every implementation decision.

## 1. Stability Before Features

Never add features simply because they are possible.

Every feature must improve operator awareness.

---

## 2. Follow the Current Phase

Implement only the current planned phase.

Avoid introducing unrelated improvements or redesigning existing systems unless fixing a defect or explicitly approved.

When a phase is complete:

- Validate
- Commit
- Return to this document
- Continue with the next phase

---

## 3. One Problem at a Time

Each phase has one primary objective.

Complete it before beginning another.

Avoid parallel feature development.

---

## 4. Operator First

Dashboards exist for humans.

Every card should answer an operational question.

Avoid exposing implementation details whenever possible.

---

## 5. Explain, Don't Display

Do not simply expose values.

Explain:

- Meaning
- Impact
- Recommendation

The dashboard should reduce operator thinking, not increase it.

---

## 6. Passive Before Active

Always prefer information already available from the infrastructure.

Only perform active discovery when passive information cannot achieve the required objective.

---

## 7. Safe Operation

HIOC must never negatively impact the infrastructure it monitors.

Avoid unnecessary:

- Polling
- Network scans
- Broadcast traffic
- CPU usage
- Disk writes

---

## 8. Reuse Existing Components

Enhance existing systems whenever practical.

Avoid duplicate engines or overlapping functionality.

---

## 9. Incremental Evolution

Prefer extending existing architecture over replacing it.

Large redesigns require explicit approval.

---

## 10. Compatibility Resilience

> Accept compatible external evolution. Preserve intentional HIOC-controlled and security identities. Diagnose both clearly.

HIOC prefers capability and structural compatibility over exact versions for
independently updated external software. Version drift alone is not failure;
compatible updates continue automatically. Required capability, schema or
protocol failures fail clearly with the affected dependency and subsystem.
Exact identities remain intentional for HIOC-controlled frozen runtimes,
immutable evidence, cryptographic verification and security/provenance trust
anchors. This policy is capability-first compatibility, not "always accept newer."

### Dependency Classification

Development distinguishes independently updated external dependencies;
HIOC-controlled isolated/vendored dependencies; security/provenance trust
anchors; supported runtime/tool families; external protocol/data-schema
dependencies; and internal HIOC schemas/protocols. Internal contracts remain
HIOC governed; supported families separate permitted patch evolution from exact
tested evidence. Detailed classification and boundaries belong in the
[compatibility documentation](COMPATIBILITY_RESILIENCE.md) and registry.

### Standard Compatibility States

The standard HIOC semantics for future external dependencies are:
`COMPATIBLE`, `COMPATIBLE_UPDATED`, `COMPATIBILITY_UNKNOWN`,
`COMPATIBILITY_DEGRADED`, `INCOMPATIBLE`, `TRUST_ANCHOR_CHANGED`, and
`DEPENDENCY_UNAVAILABLE`. Exact field/schema definitions remain in
[COMPATIBILITY_RESILIENCE.md](COMPATIBILITY_RESILIENCE.md).

### Update Causality and Last-Known-Compatible History

A dependency update must not be blamed merely because a failure happened after
an update. A likely update-related compatibility break requires evidence of:

1. a previously known-compatible dependency version/identity;
2. a different current version/identity; and
3. failure of a required compatibility capability after the change.

A capability failure without established version drift is reported as
incompatibility without claiming that an update caused it. Changed version with
passing capabilities is `COMPATIBLE_UPDATED`; normal operation continues.
Detailed causality implementation remains in the focused compatibility document.

Retain safe, non-secret last-known-compatible observations where useful to show
what previously worked, what is running now, what changed, which capability
failed, when incompatibility first appeared and which subsystem is affected.
An incompatible current observation must not erase the previous known-good
observation.

### Subsystem Failure Isolation

A compatibility failure in one dependency must not make unrelated HIOC
subsystems appear globally broken. HA registry incompatibility isolates HA
association; Pi-hole contract failure isolates dependent DHCP/inventory
processing; NUT incompatibility isolates UPS observations; go2rtc incompatibility
isolates camera integration. MQTT failure affects publication but must not erase
authoritative local state. Operator-tool trust drift blocks operations requiring
that trusted tool where practical. Detailed boundaries stay in the registry.

---

# Architecture

Current major components include:

- Platform Core
- Inventory Engine
- Incident Engine
- Correlation Engine
- History Engine
- Dashboard v2
- MQTT Publishing Layer
- Home Assistant Integration

Additional components should integrate cleanly into this architecture.

---

## Compatibility Status Architecture

Permanent HIOC operator-awareness contracts, rather than temporary PE-4 evidence:

- Authoritative local state: `state/platform/compatibility.json`.
- Retained MQTT status: `<HIOC_BASE_TOPIC>/platform/compatibility`.
- Compatibility summary integrated with platform status.

The focused [compatibility documentation](COMPATIBILITY_RESILIENCE.md) owns the
exact schemas. Future presentation consumes these central contracts rather than
creating a separate monitoring island.

# Dashboard Philosophy

Dashboard v2 is the primary operator interface.

Each page has a specific purpose.

## Operations

Current infrastructure health.

## Diagnostics

Current evidence.

## History

Past incidents.

## Inventory

Living infrastructure documentation.

## Network

Network diagnostics.

## Servers

Server diagnostics.

Future pages should have equally focused responsibilities.

---

# Incident Philosophy

Every incident should produce:

- Live status
- Supporting evidence
- Affected systems
- Dependency path
- Recommended action

When resolved, every incident should automatically produce:

- Timeline
- Summary
- Probable cause
- Duration
- Affected services
- Operator review

Historical analysis is considered a first-class feature.

---

# Inventory Philosophy

The Inventory is the living documentation of the infrastructure.

It should answer:

- What exists?
- Where is it?
- What does it do?
- What depends on it?
- Is it healthy?
- When was it last seen?
- How was it discovered?

Inventory information should become richer over time while remaining trustworthy.

---

# Development Roadmap

## Completed

- Platform Foundation
- MQTT Publishing
- Dashboard v2
- Incident Engine
- Correlation Engine
- History Engine
- Incident Review
- Dashboard usability improvements
- Initial Living Inventory

---

## Current Phase

### Phase 7A - Passive Living Inventory

Objective:

Build the richest possible infrastructure inventory without performing active network discovery.

Passive information sources include:

- Pi-hole DHCP leases
- Linux ARP / Neighbor tables
- Home Assistant Device Registry
- Home Assistant Entity Registry
- MQTT Discovery
- Existing integrations
- Known infrastructure definitions
- Routing information
- Passive operating system information

Expected outcome:

The Inventory becomes the authoritative documentation of the infrastructure without requiring active scans.

---

#### Phase 7A.8 Recovery Validation Chain

Status: **COMPLETE**

Scope: Recovery and re-validation of the approved lifecycle migration baseline after temporary validation state loss.

Completed validation sequence: R1, Post-R1, R2, Post-R2, R3, Post-R3, R4, and Post-R4. R4 received the formal decision **A. R4 APPROVED**.

- Approved generation: `gen_1784229948679_0a45eaf2f2f7`
- Approved recovery epoch: `/home/jazofv1/hioc-validation/phase7a8/epoch-20260716T173541Z`

The recovery sequence is complete, and the approved migrated baseline is the authoritative lifecycle recovery reference. The original HIOC Master Plan remains authoritative; Phase 7A Passive Living Inventory remains active; Active Discovery remains postponed. R5 is a future checkpoint and was not prepared or executed by this finalization.

This checkpoint preserves phased work, no scope creep, production validation, Evidence Reports, and return to the Master Plan after each completed sub-step.

#### Phase 7A.9 Passive Inventory Correctness Validation

Status: **COMPLETE**

Scope: Read-only production validation of the existing passive-inventory baseline, with no behavioral changes or corrective implementation.

##### Evidence Report

**Deployment result:** No deployment or runtime change was part of this checkpoint. Production validation covered `inventory.json`, `devices.json`, `services.json`, `capabilities.json`, `topology.json`, `dependencies.json`, `summary.json`, and `status.json`; every file was present and valid. The official HIOC production validator, `bash /home/jazofv1/hioc/pi4/validate_pi4.sh`, completed successfully with all checks passing.

**Intended behavior:** Passive Inventory must preserve stable identity and internally consistent projections while keeping DHCP assignment evidence, observation freshness, operational monitoring, and source authority semantically distinct.

**Validation performed:** Stable snapshots confirmed that `inventory.devices` matched `devices.json`, `inventory.services` matched `services.json`, summary counts matched the projections, and counts remained internally consistent. Health categories, Watch-device records, health reasons, projection counts, and summary counts were mutually consistent.

**Invariant checks:** The baseline contained 140 devices, 140 unique IDs, 140 unique MAC addresses, and 140 unique IP addresses, with no duplicate identities or malformed MAC addresses. Runtime behavior agreed with the documented observation model: DHCP remained identity evidence rather than liveness evidence; freshness remained separate from operational monitoring; monitoring remained policy-driven; and weak evidence did not overwrite stronger identity. Result: **PASS**.

**Warnings and deferred risks:** This checkpoint establishes the production baseline but does not complete or reorder the remaining corrective sequence. Identity Reconciliation Hardening remains next, followed by the other already-listed inventory correctness tasks. The separate unresolved `mosquitto_pub` issue remained outside scope and was not investigated or modified.

**Final result:** **PASS**

#### Identity Reconciliation Hardening

Status: **COMPLETE**

Objective: Validate and strengthen the canonical identity model itself before additional passive enrichment resumes. Phase 7A.9 confirmed that the current production snapshot has no IP-only identities, duplicate MAC identities, duplicate IDs, or duplicate IPs, and that ARP/DHCP multi-source reconciliation is operating correctly. This checkpoint must establish that supported passive discovery cannot produce persistent duplicate identities under the documented identity model; it is not merely another search for duplicates in one snapshot.

Identity invariants:

- Every physical device has exactly one canonical identity.
- MAC-backed identities supersede weak IP-only identities whenever reconciliation is unambiguous.
- Weak identities cannot persist after successful reconciliation.
- Multiple passive collectors cannot create parallel identities for the same device.
- Collector execution order does not change the final inventory.
- Identity reconciliation is idempotent across repeated collection cycles.
- Ambiguous evidence never causes an incorrect merge.
- Identity provenance remains preserved after reconciliation.
- Future passive collectors participate in the documented canonical identity model.

Required hardening work:

- Review the reconciliation implementation against [DATA_MODEL.md](DATA_MODEL.md).
- Correct any remaining implementation defects found within this checkpoint's scope.
- Add focused regression tests for identity invariants where appropriate.
- Produce production validation evidence after completion.

Completion criterion: Evidence demonstrates that the supported passive-discovery architecture cannot produce persistent duplicate identities under the documented canonical identity model.

Deferred identity architecture decisions remain outside this checkpoint:

- **Historical identity continuity:** A weak IP-based identity may be replaced in current inventory and projections by an unambiguous MAC-backed canonical identity, while historical events or external references may retain the earlier weak ID. HIOC has no formal alias table, promotion record, or historical identity resolution contract. A future explicit architecture checkpoint must decide whether historical identities remain immutable evidence identifiers, resolve through an alias or promotion mapping, or are migrated to canonical identities; this checkpoint must not invent a schema or migration mechanism.
- **Randomized-MAC asset continuity:** Passive reconciliation must not guess that unrelated MAC addresses represent one physical device. Randomized or rotated MAC addresses remain separate discovered identities unless authoritative linking evidence exists. The one-physical-device/one-canonical-identity invariant applies within supported, unambiguous identity evidence. Future operator-approved linking of multiple discovered identities to one asset belongs to the asset-centric Living Digital Twin roadmap, not heuristic passive merging.

##### Identity Reconciliation Production Evidence Report

**Deployment result:** **PASS**. Repository review found that the existing identity-reconciliation implementation already satisfied the documented architecture and required no modification. The authoritative source was synchronized, supported release validation passed, the supported release deployment completed successfully, and production validation completed successfully. Repeated production inventory reconciliation also completed successfully.

**Intended behavior:** Identity reconciliation preserves the documented canonical identity model. Weak identities reconcile into canonical MAC-backed identities only when the evidence is unambiguous; ambiguous evidence never causes an incorrect merge. Repeated reconciliation remains stable, and collector ordering does not change the resulting inventory.

**Validation performed:** Repository validation confirmed that the implementation matches [DATA_MODEL.md](DATA_MODEL.md), focused invariant regression coverage already exists, Python compilation passed, focused tests passed, and the full regression suite passed. Production validation confirmed successful deployment and runtime validation, successful repeated inventory reconciliation, and a stable inventory containing 140 devices and 8 services.

**Invariant checks:** No reconciliation failures or duplicate-identity behavior were observed. Repository regression coverage confirms canonical promotion, collector-order independence, idempotence, ambiguity protection, provenance preservation, duplicate prevention, and centralized reconciliation for future passive collectors. Repository validation and production evidence together demonstrate that supported passive discovery cannot produce persistent duplicate identities under the documented canonical identity model.

**Warnings and deferred risks:** Historical identity continuity, alias mapping, randomized-MAC continuity, and future operator-approved asset association remain intentionally deferred exactly as documented above.

**Final result:** **PASS**

#### FAILED/INCOMPLETE ARP Semantics

Status: **COMPLETE**

The original unresolved-neighbor semantics were confirmed correct: `FAILED`, `INCOMPLETE`, `NONE`, `NOARP`, MAC-less, and other non-durable entries do not create device evidence or refresh positive-observation timestamps. The bounded correction removes duplicate neighbor-table acquisition within one inventory cycle and distinguishes successful empty accepted evidence from total ARP collector unavailability. Discovery-source status and passive device evidence now derive from the same authoritative snapshot.

Implementation commit `8278e54bacb68f25821e6a4981bb01273c32e469` (`Phase 7A: unify ARP snapshot and collector semantics`) preserves `neighbor_table()` as a dictionary-returning compatibility wrapper and keeps `NeighborTableResult`, sanitized exit-code diagnostics, and command-failure details internal. No public schema, topic, entity, dashboard field, event payload, or general driver-framework contract changed.

##### Production Evidence Report

**Deployment result:** **PASS**. The authoritative Windows repository and `origin/main` matched at the implementation commit before PI3 source was fast-forwarded to it. On PI3 NUT&PIHOLE, `bash /home/jazofv1/hioc-release-source/release/validate.sh`, the supported `bash /home/jazofv1/hioc-release-source/release/upgrade.sh`, and `bash /home/jazofv1/hioc/pi4/validate_pi4.sh` all passed. The upgrade created install backup `/home/jazofv1/hioc/backups/install-20260724-194147` and release backup `/home/jazofv1/hioc/backups/release-upgrade-20260724-194146`.

**Intended behavior:** One logical neighbor-table acquisition supplies both discovery-source reporting and `PassiveNetworkDriver`. A successful acquisition with no accepted records reports `arp_table_empty`; failure of both supported commands reports `arp_table_unavailable`. Raw stderr is discarded, diagnostics remain internal, and accepted NUD-state and unresolved-neighbor filtering behavior remain unchanged.

**Invariant checks:** Pre-commit Python compilation passed; inventory/correlation tests passed 111 tests; the complete suite passed 161 tests with 6 skips; release validation and `git diff --check` passed. Production state under `/home/jazofv1/hioc/state/inventory` was online with schema `1.0`, 140 devices, 138 clients, 2 infrastructure devices, 8 services, 280 dependency edges, 139 topology edges, 98 healthy devices, 42 Watch devices, no degraded or offline devices, and lowest health score 75. During the `2026-07-24T19:42:05-06:00` through `2026-07-24T19:42:06-06:00` evidence window, discovery sources were exactly `local_host`, `gateway`, `arp_table`, `dhcp_leases_found`, and `known_infrastructure`; `discovery_limited` was false and `discovery_limit_reason` was empty. Inventory and capability projections remained populated, and no internal result or diagnostic fields appeared in public output.

**Warnings and deferred risks:** Automated regression tests validate the `arp_table_unavailable` path and diagnostic isolation. Production validated the normal successful `arp_table` path and showed no false unavailable or limited state; neighbor collection was not deliberately disrupted to exercise command failure. Dashboard severity mapping, collector canonical ownership, Pi-hole DHCP validation, and passive enrichment remain separate later work.

**Final result:** **PASS**

#### Dashboard Severity Mapping — COMPLETE

Repository review identified two bounded presentation defects. Aggregate Watch wording treated every Watch record as a stale observation even though Watch can also represent expired passive evidence or DHCP-only operational availability that remains unknown. Dashboard v2's Inventory Summary accent also evaluated retained offline or degraded counts before an unavailable inventory status, allowing confident severity styling when current inventory truth was unavailable.

The repository correction uses policy-neutral aggregate Watch wording and makes unknown inventory status take precedence in the affected Inventory Summary style. Detailed per-device `health_reasons`, health computation, health-score thresholds, Watch membership, inventory counts, schemas, the `status.json` contract, MQTT contracts, Home Assistant entities and attributes, incident severity, dashboard layout, and collector and DHCP behavior remain unchanged. The existing blue Watch palette is intentionally preserved; its relationship to the Design System remains deferred to a separate UX/design decision.

##### Production Evidence Report

**Deployment result:** **PASS**. Implementation commit `1e2dcf973d02514561b7bb8a4f5c6f495350ab09` (`Phase 7A: refine dashboard severity presentation`) passed release-source validation and the supported production upgrade. The installed runtime remained `/home/jazofv1/hioc`; install backup `/home/jazofv1/hioc/backups/install-20260727-205938` and release-upgrade backup `/home/jazofv1/hioc/backups/release-upgrade-20260727-205938` were created. `bash pi4/validate_pi4.sh` reported `HIOC Pi4 validation passed.`

**Intended behavior:** Aggregate Watch presentation describes observation or availability review without claiming every Watch condition is stale. Dashboard v2 Inventory Summary styling treats unknown, unavailable, invalid, or otherwise untrustworthy inventory status as higher priority than retained offline or degraded counts. Health and inventory semantics, public contracts, incident presentation, layout, and the existing blue Watch palette remain unchanged.

**Invariant checks:** Production inventory status was `online`, schema version was `1.0`, and status `device_count` matched summary `device_count` at 148. Health categories reconciled exactly: 96 healthy + 52 Watch + 0 degraded + 0 offline = 148 devices. Inventory classes reconciled exactly: 2 infrastructure + 146 clients = 148 devices, and `network_client_count` equaled `client_count` at 146. Both infrastructure devices were healthy with health score 100. Lowest inventory health score was 75; 8 services, 147 topology edges, and 296 dependency edges remained present. Discovery was not limited, the limit reason was empty, and expected sources `local_host`, `gateway`, `arp_table`, `dhcp_leases_found`, and `known_infrastructure` were present.

**Warnings and deferred risks:** The 52 Watch devices are expected operational inventory state and are not a deployment failure. The separate Watch color and Design System UX decision remains explicitly deferred and was not resolved by this checkpoint.

**Final result:** **PASS**

#### Collector Canonical Ownership

Status: **COMPLETE**

The bounded repository implementation corrects two confirmed ownership defects. Collector identity previously depended on local-interface enumeration order and could compose an IP from one interface with a MAC from another. Known-infrastructure enrichment also discarded operator metadata after a legitimate observed IP or hostname change despite an exact normalized MAC match.

Canonical collector IP and MAC now come atomically from one complete interface record. A complete record requires an interface identifier, a valid IPv4 address, and a valid normalized MAC address. The default-route interface, obtained from the existing route discovery source, is preferred. If it has no complete record, selection uses stable ordering by interface identifier, numeric IPv4 address, normalized MAC, and CIDR. Incomplete records are never combined; when no complete record exists, there is no canonical collector selection and local services are omitted rather than assigned to an unrelated device. The full interfaces list remains observational evidence.

Exact normalized MAC matches now establish canonical discovered identity for known-infrastructure enrichment even when configured IP or hostname values are stale. Current observed IP, MAC, hostname, positive-observation timestamps, reachability, and discovery provenance remain authoritative, while supported operator metadata continues to enrich the device and preserve its configured classification. Weaker IP- or hostname-only matches continue rejecting conflicting MAC evidence and ambiguous identities are not guessed together. A MAC change does not imply continuity.

Implementation commit `054fb55a2e70901f3230145b76983c31d2b5ce61` (`Phase 7A: harden collector canonical ownership`) implements the bounded correction. `stable_device_id()` was unchanged. The exact-MAC known-infrastructure continuity behavior was validated by the implementation and regression suite. No inventory schema, stable-ID precedence, MQTT topic or payload, Home Assistant contract, dashboard contract, health behavior, incident behavior, discovery policy, or MAC-change continuity policy changed.

##### Production Evidence Report

**Deployment result:** **PASS**. The PI3 release source was fast-forwarded to implementation commit `054fb55a2e70901f3230145b76983c31d2b5ce61`. Release validation reported `HIOC release validation passed.`, the supported production upgrade completed successfully, and production validation reported `HIOC Pi4 validation passed.` The installed runtime remained `/home/jazofv1/hioc`; release-upgrade backup `/home/jazofv1/hioc/backups/release-upgrade-20260728-114736` and install backup `/home/jazofv1/hioc/backups/install-20260728-114737` were created.

**Intended behavior:** Collector identity is derived from one deterministic complete local-interface record, with default-route preference and atomic IP/MAC ownership. Exact normalized MAC matches preserve supported known-infrastructure metadata across legitimate observed IP or hostname movement while current observed runtime fields remain authoritative. Weaker IP or hostname matches continue rejecting conflicting MAC identities, and no heuristic continuity across MAC changes is inferred.

**Invariant checks:** Pre-commit validation passed with 107 focused inventory tests, 169 full-suite tests and 6 skips, Python compilation, release validation, and final diff review. At `2026-07-28T11:47:56-06:00`, production inventory was online at schema `1.0` with 148 devices, 107 healthy, 41 Watch, 0 degraded, 0 offline, 2 infrastructure devices, 146 clients, 8 services, 147 topology edges, 296 dependency edges, and unrestricted discovery. The canonical collector was `Pi3 - NUT and Pi-hole`, role `Core Infrastructure`, at observed IP `192.168.100.252` and MAC `b8:27:eb:70:ab:df`, online and healthy with health score 100 and sources `known_infrastructure` and `local_host`. All eight discovered services—`pihole-FTL`, `pihole-FTL.service`, network service ports 53 and 67, `cron`, `ssh`, `nut-monitor`, and `nut-server`—were owned by that collector and reported host `Pi3 - NUT and Pi-hole`. No service was assigned to the historical incorrect `.105` owner. Inventory generation remained healthy, discovery was not limited, and no JSON, MQTT, Home Assistant, or dashboard contract failure was observed.

**Warnings and deferred risks:** No checkpoint-specific production warning was observed. Pi-hole DHCP lease ingestion validation and the subsequent passive-enrichment roadmap remain separate work.

**Final result:** **PASS**

#### Pi-hole DHCP Lease Ingestion

Status: **COMPLETE - PASS WITH DOCUMENTED WARNING**

##### Single Snapshot Acquisition

Status: **COMPLETE**

Implementation commit `a01b6b77350ee22a40e8aacca72e256b826c8a3f` (`Phase 7A: unify DHCP lease snapshot acquisition`) establishes one authoritative DHCP lease snapshot per inventory cycle. `discover_inventory()` acquires configured lease sources exactly once into a cycle-local immutable tuple and shares that captured input across discovery-source status, `PassiveNetworkDriver` observations, and central reconciliation. This removes duplicate lease-file acquisition during one inventory cycle while preserving all existing DHCP parsing, assignment-only observation, source-state, deterministic ordering, source-authority, identity, health, topology, dependency, schema, MQTT, Home Assistant, dashboard, and event semantics.

###### Evidence Report

**Implementation validation:** **PASS**. Automated regression tests establish one source acquisition per inventory cycle for one and multiple configured files, immutable snapshot reuse by both consumers, absence of a secondary acquisition, consistent discovery-status and observation inputs for valid, missing, and partial snapshots, and a single sanitized malformed-row warning. Standalone compatibility helpers continue acquiring current results when no snapshot is supplied. The focused inventory suite passed 115 tests; the full regression suite passed 177 tests with 6 skips. Python compilation, release validation, and `git diff --check` also passed.

**Production validation:** **PASS** for externally observable behavior. The release source synchronized successfully, the supported upgrade completed successfully, and production validation completed successfully. Inventory generation succeeded with `dhcp_leases_found` among its discovery sources. The production inventory contained 145 DHCP-backed devices; sampled DHCP-backed records originated from `/etc/pihole/dhcp.leases`, and their lease metadata remained present. No observable inventory regression was reported.

**Important engineering note:** The single-acquisition invariant is an internal implementation property established by automated regression testing, not by production runtime artifacts. Production validation confirms the observable inventory behavior resulting from the implementation but does not expose or prove lease-file acquisition counts. HIOC evidence reports must preserve this distinction between implementation invariants and production observables.

**Intentionally unchanged:** This sub-checkpoint does not alter lease-expiration policy, IPv6 handling, ISC lease compatibility, or discovery-limitation semantics.

**Final result at this sub-checkpoint:** **PASS** for Single Snapshot Acquisition only. The overall Pi-hole DHCP Lease Ingestion checkpoint remained **IN PROGRESS** until the later bounded implementation and production validation recorded below.

##### DHCP Identity Architecture Decision

Status: **COMPLETE - PASS WITH DOCUMENTED WARNING**

The approved architecture is **Pi-hole-specific integration through the existing passive-driver and source-tagged device-record convention**. Pi-hole lease acquisition and parsing remain source-specific adapter functions used by `PassiveNetworkDriver`; valid records enter the existing `DriverResult.devices` flow and central `merge_records()` reconciliation. No new `IdentitySource` protocol, abstract base class, registry, plugin framework, dependency-injection layer, or generalized provider model is introduced. [ADR-0015](../DECISIONS.md#adr-0015-keep-pi-hole-dhcp-within-the-existing-passive-driver-contract) records the binding decision.

This choice preserves the repository's current separation of concerns. Collection adapters acquire and normalize evidence; source-tagged records carry provenance; centralized reconciliation selects canonical identity and field values; known infrastructure supplies limited operator metadata; observation timestamps represent positive observation only; and health, monitoring, topology, dependencies, MQTT publication, and Home Assistant projections consume the reconciled inventory. The existing `DriverResult` mapping convention is already the minimal generic boundary. Adding another identity-source interface would duplicate it and force a classification hierarchy that the current single DHCP implementation does not need.

###### Identity and field ownership

| Field | Approved DHCP contribution |
|---|---|
| MAC address | A valid normalized MAC may create a MAC-backed technical identity or confirm an existing matching identity. It may upgrade one unambiguous IP-only weak identity through existing reconciliation. It never replaces a conflicting MAC or causes ambiguous identities to merge. |
| IP address | Assignment evidence. It may populate the current record and participate in unambiguous reconciliation, but it does not override a stronger current local-host, gateway, ARP, or integration association. A differing passive IP remains stronger current observation evidence. |
| DHCP hostname | Technical identity metadata. It may populate a missing hostname and may win only among DHCP observations by deterministic lease ordering. It does not replace a stronger current passive hostname. |
| Friendly name | DHCP never contributes `name` or future `friendly_name` and never overwrites operator-managed naming. |
| Vendor | DHCP does not contribute or alter vendor information. |
| Lease start | The supported Pi-hole/dnsmasq row does not supply a lease-start value, so none is fabricated. A future source-format decision is required before adding such a field. |
| Lease expiry | Preserved as source attribution metadata in `lease_expires_epoch`. Zero retains its infinite-lease meaning. A finite lease contributes current assignment evidence only when its expiry is later than the inventory cycle's fixed collection epoch. |
| Lease active state | Assignment evidence only. No canonical online, offline, health, reachability, or observation field is derived from it. Presence, active assignment, positive observation, staleness, degradation, and offline state remain distinct. |
| Last seen | Never created or refreshed by DHCP. `_positive_observation` remains false for DHCP records. |
| Online or offline state | DHCP has no direct authority. Expiry never becomes an offline event. |
| Device identity | A valid MAC-backed lease may create a technical inventory record. A hostname-only or unusable-MAC lease cannot. Stable identity remains MAC-first, and conflicts remain separate. |
| Source provenance | Records retain `source: dhcp_leases`, combined canonical `sources`, the source file in `dhcp_lease_source`, and source status in `discovery_sources`. No field-level provenance system is added. |
| Confidence or authority | Deterministic source precedence and ambiguity checks remain sufficient. No numeric confidence score is introduced. |

###### Deterministic conflict and edge-case rules

1. A DHCP record with the same valid MAC as an existing strong identity merges into that identity; stronger current values remain authoritative.
2. One IP-only weak identity and one DHCP MAC-backed identity sharing an IP reconcile only when the existing central rules find exactly one weak identity, one strong identity, and no conflicting MAC.
3. A conflicting passive hostname outranks the DHCP hostname. A DHCP hostname may fill a missing hostname.
4. DHCP never contributes `name` or `friendly_name`, so operator naming remains unchanged.
5. When DHCP reports a different IP from a stronger recent passive observation, the passive IP remains canonical and the DHCP assignment remains source evidence.
6. An expired finite lease contributes no current assignment evidence, is not positive observation, does not enrich or refresh a retained device, and never proves offline.
7. Multiple leases for one MAC remain separate input observations until central deterministic selection; the established ordering selects the infinite lease first, otherwise the greatest expiry, followed by stable source and value tie-breakers.
8. The same IP associated with different MACs produces separate MAC-backed identities. It never authorizes a merge; ambiguous weak reconciliation is skipped.
9. Malformed, unsupported, or incomplete rows contribute no identity record. Sanitized warnings and source health preserve malformed, unsupported, partial, unreadable, I/O-error, missing, disabled, empty, and found distinctions.
10. A hostname with no usable MAC is rejected by this Pi-hole lease path and cannot create an IP-only or hostname-only device.
11. A valid MAC with a blank or `*` hostname is accepted without fabricating a hostname.
12. No archived-asset schema or retention policy exists. Later implementation must preserve retained canonical records and must not invent archive revival or deletion behavior.
13. Temporary source unavailability contributes no new evidence, preserves prior inventory through existing retention behavior, and reports the established source status and discovery limitation semantics.
14. Successful collection with zero leases contributes no devices and reports `dhcp_leases_empty`; it is not treated as failure, device disappearance, or offline evidence.

###### Implementation Evidence Report

**Implementation validation:** **PASS**. Pi-hole/dnsmasq rows now use one fixed collection epoch per inventory cycle. Active finite IPv4 leases and expiry-zero infinite leases remain eligible; expired finite leases, IPv6 entries, clearly recognized ISC lease blocks, malformed rows, and unusable identities contribute no device evidence. Expired leases cannot enrich, move, refresh, or mark retained devices offline. DHCP remains assignment-only and cannot overwrite stronger current MAC-backed, local-host, gateway, ARP, integration, known-infrastructure, or operator-managed metadata.

Source aggregation now preserves complete `found`, `empty`, and explicitly `disabled` states; distinguishes missing, unreadable, malformed, unsupported, I/O-error, and partial input; and reports configured incomplete or unavailable DHCP evidence as a discovery limitation independently of integration evidence. Existing inventory and all other discovery sources remain preserved. The default source is the production-confirmed `/etc/pihole/dhcp.leases`; other dnsmasq-format files require explicit configuration, and ISC `dhcpd.leases` is not advertised as supported.

The focused identity checks passed 6 tests, the inventory suite passed 123 tests, the correlation suite passed 12 tests, and the full regression suite passed 191 tests with 7 skips.

###### Production Evidence Report

**Deployment result:** **PASS**. Implementation commit `be9035a0641f16cdfc5c8aa1b090056c519881b7` was deployed through the supported production upgrade, which exited 0 and created install backup `install-20260729-102325` and release-upgrade backup `release-upgrade-20260729-102325`. The general PI3 validator passed with exit code 0 and confirmed that at least one configured DHCP lease file was readable. The inventory engine exited 0 and regenerated valid `inventory.json`, `devices.json`, `services.json`, `capabilities.json`, `topology.json`, `dependencies.json`, `summary.json`, and `status.json` artifacts.

**Intended behavior:** Pi-hole DHCP ingestion reads eligible active IPv4 dnsmasq leases, preserves assignment provenance and expiry metadata, reconciles them with stable MAC-backed identities, and does not treat DHCP evidence as positive liveness, a health reason, or direct online or offline authority. Canonical-address selection remains governed by existing reconciliation and was not changed by this checkpoint.

**Invariant checks:** At collection time the source contained 140 nonblank rows, all 140 of which were valid active finite IPv4 leases with 140 unique MACs, IPv4 addresses, and MAC/IP pairs. There were no expired, infinite, IPv6, ISC, or malformed source rows. All 140 active lease MAC identities were represented in the canonical inventory. The 150-device inventory contained 147 DHCP-backed canonical identities, all with DHCP provenance and lease-expiry metadata, with no missing or unexpected source path. DHCP-backed records did not assert `_positive_observation=true`, add DHCP or lease text to health reasons, or directly assert online or offline from DHCP-only evidence. Discovery reported `dhcp_leases_found`, `discovery_limited=false`, and an empty limit reason. Seven DHCP-backed identities beyond the 140 active leases were retained expired historical canonical records with no corresponding active lease, consistent with persistent inventory behavior rather than duplicate active ingestion.

**Warnings:** One active lease MAC/IP pair did not match the chosen canonical IP, although the active lease MAC identity was represented. The same MAC owned two simultaneous `STALE` neighbor-table addresses: one was the selected canonical IP and the other was the active DHCP lease IP. The lease IP had no conflicting active DHCP owner. This exposes a separate canonical-address selection concern, not a DHCP ingestion failure. The mismatch was not resolved by this checkpoint, and DHCP assignment evidence alone must not be allowed to fabricate liveness in the future correction.

**Final result:** **PASS WITH DOCUMENTED WARNING**. Pi-hole DHCP Lease Ingestion is complete. Canonical-address selection remains unchanged and is retained as a separate Phase 7A hardening checkpoint. Active Discovery remains postponed.

##### Resolved DHCP Implementation Decisions

- **Expired finite-lease policy:** Only finite leases with expiry later than the fixed cycle epoch contribute current assignment evidence. Expiry zero remains infinite.
- **ISC `dhcpd.leases` compatibility:** ISC syntax is unsupported and is no longer included in default source paths.
- **IPv4 / IPv6 contract:** This ingestion path is IPv4-only. IPv6 rows are unsupported.
- **Explicit empty-list behavior:** An explicitly blank configured path list disables DHCP acquisition and reports `dhcp_leases_disabled`; absent configuration uses the Pi-hole default.
- **Discovery-limitation semantics:** Found, empty, and disabled are complete states. Missing, unreadable, malformed, unsupported, I/O-error, and partial configured input limit discovery independently of integration evidence.

These decisions and the production Evidence Report complete the bounded Pi-hole DHCP Lease Ingestion checkpoint.

#### Canonical Address Selection Hardening

Status: **COMPLETE - PRODUCTION VALIDATED**

Production DHCP validation demonstrated that one MAC may have multiple neighbor-table IP entries and that multiple entries may simultaneously be `STALE`. The current canonical selector may choose a stale non-DHCP address even when the active DHCP lease address is also present in the neighbor table, owned by the same MAC, and has no conflicting active DHCP owner.

This checkpoint must investigate and define deterministic canonical-address precedence using source authority, observation recency, neighbor state, lease validity, and existing identity invariants. Any correction must preserve stable MAC-backed identity, prevent duplicate canonical identities, and must not allow DHCP assignment evidence alone to fabricate liveness. It must include regression validation, supported production validation, and a Production Evidence Report. This work is distinct from the completed Collector Canonical Ownership and Pi-hole DHCP Lease Ingestion checkpoints.

Repository implementation now preserves neighbor state as private reconciliation
evidence and selects canonical IPv4 through one explicit, order-independent
comparator. Local collector, gateway, configured integration, `REACHABLE`, and
`PERMANENT` evidence outrank active DHCP; active DHCP outranks `DELAY`, `PROBE`,
unknown fallback ARP, and `STALE`; unusable neighbor states cannot become
preferred operational addresses. Equal evidence uses lease validity/expiry,
observation epoch, and numeric IPv4 tie-breaking. Selection remains separate
from MAC-backed identity, positive observation, health, and retention.

The repository defect reproduction, contract, source map, downstream review,
validation record, warnings, and pending production requirements are in the
[Canonical Address Selection Hardening Evidence Report](CANONICAL_ADDRESS_HARDENING_EVIDENCE.md).
At that implementation stage, the checkpoint remained open until supported
deployment, production evidence, and documentation closeout passed.

The first governed production run deployed implementation commit
`839e924b2249bec736ff74d9a2ac593c7fee6bb8` successfully and passed artifact,
release, runtime, identity, provenance, monitoring, health, and bounded
unrelated-device checks. Its final result was invalidated by the validation
procedure: it admitted a link-local IPv6 `STALE` neighbor, failed to exclude
higher-authority configured integration evidence, and incorrectly required
every active DHCP address to become canonical. The retained `.251` PI5 address
therefore does not prove an ADR-0018 failure. Rollback was not performed.

Revised repository-owned validation distinguishes `PASS`,
`NO_QUALIFYING_CANDIDATE`, and genuine `FAIL`; only genuine failure recommends
rollback. Separately, active DHCP evidence for retired PI5 address `.152`
remains an unresolved production finding. Read-only PI3 evidence must identify
its source, expiry, reservation/configuration status, interface ownership, and
recent DHCP activity before any DHCP cleanup or parser follow-up is proposed.
At that first-run stage, the comparator remained deployed and the checkpoint
remained **IN PROGRESS**.

A second production validator execution passed comparator identity and all six
real Boolean invariants, with 151 devices before and after and zero unrelated
canonical-address changes. No candidate qualified because PI5 had current
`REACHABLE` IPv4 `.251`, DHCP IPv4 `.152`, and only an IPv6 link-local `STALE`
neighbor. Generic truthiness incorrectly treated diagnostic metadata value
`_unrelated_canonical_change_count: 0` as a failed invariant and returned
`FAIL`. Rollback was not performed. The corrected validator requires exactly
the six documented Boolean invariants, preserves underscore-prefixed metadata
without evaluating it, and rejects missing, mistyped, or unexpected public
keys explicitly. The expected evidence result was
`NO_QUALIFYING_CANDIDATE`, pending the strict PI3 rerun recorded below.

The `.152` finding is separately recorded as an unexpired old lease with no
renewal observed during the bounded 60-second check. It remains an
infrastructure-evidence finding and does not change ADR-0018 or justify
comparator rollback.

Final strict validation synchronized clean source commit
`b3621c3765e56b9741565ac58be6a5fad4d0f302` and retained the unchanged
comparator from `839e924b2249bec736ff74d9a2ac593c7fee6bb8`. Source and runtime
bytes matched Git-derived SHA-256
`35f36916399331a6e1129f7a49ba86933960eca8e94d6b30c80e9be3d7cd75b8`.
All six Boolean invariants passed; inventory stayed at 151 devices; diagnostic
metadata recorded one unrelated canonical-address change within the approved
bound; and no input errors occurred. With no qualifying candidate, the
successful result was `NO_QUALIFYING_CANDIDATE`, exit code 0, with no rollback
recommendation or action.

Both earlier failures were validator defects: the first imposed unconditional
DHCP precedence and admitted link-local IPv6; the second applied Boolean
truthiness to numeric diagnostic metadata. The strict typed contract resolved
both. Canonical Address Selection Hardening is production validated and
**COMPLETE**. The `.152` lease residue and DHCP Service Health & Capacity
Monitoring remain separate future work.

#### July 29 DHCP Pool Exhaustion Incident - RESOLVED

The production address-allocation failure was caused by exhaustion of the former `192.168.100.50 - 192.168.100.150` dynamic pool. The operator expanded it to `192.168.100.50 - 192.168.100.250`; a previously failing client immediately obtained a lease; critical static networking and infrastructure services were validated; and HIOC deployment validation passed. The permanent evidence report is [INCIDENT_2026-07-29_DHCP_POOL_EXHAUSTION.md](INCIDENT_2026-07-29_DHCP_POOL_EXHAUSTION.md). This resolved incident motivates a future DHCP capacity-monitoring phase but does not alter the current Phase 7A corrective sequence.

#### Remaining Phase 7A Corrective Sequence

1. Repository and Deployment Hygiene - **COMPLETE**.
2. Phase 7A.9 Passive Inventory Correctness Validation — **COMPLETE**.
3. Remaining inventory correctness work: Identity Reconciliation Hardening — **COMPLETE**; FAILED/INCOMPLETE ARP semantics — **COMPLETE**; Dashboard Severity Mapping — **COMPLETE**; Collector Canonical Ownership — **COMPLETE**; Pi-hole DHCP Lease Ingestion — **COMPLETE WITH DOCUMENTED WARNING**; and Canonical Address Selection Hardening — **COMPLETE; PRODUCTION VALIDATED**.
4. Resume passive enrichment.
5. Continue toward asset-centric inventory.
6. Design and approve retention and archival policy.
7. Complete Phase 7A.
8. Begin Phase 7B Safe Active Discovery.

Repository and Deployment Hygiene, Release Boundary Hardening, Phase 7A.9, Identity Reconciliation Hardening, FAILED/INCOMPLETE ARP semantics, Dashboard Severity Mapping, Collector Canonical Ownership, Pi-hole DHCP Lease Ingestion, and Canonical Address Selection Hardening are complete. Passive enrichment may resume in its documented order; the separate `.152` DHCP residue and DHCP service-health roadmap work remain open.

#### Passive Enrichment Architecture and Specification

Status: **PHASE 7A IN PROGRESS; PE-0 COMPLETE - DESIGN APPROVED; PE-1 COMPLETE - PRODUCTION VALIDATED; PE-2 COMPLETE - PRODUCTION VALIDATED; PE-3 COMPLETE; PE-3.0 COMPLETE; PE-3.1 IMPLEMENTED - REPOSITORY VALIDATED; PE-3.2 COMPLETE - EXTERNAL DATASET VALIDATED; PE-3.3 COMPLETE - DESIGN APPROVED / REPOSITORY SYNCHRONIZED; PYTHON INSTALL MANAGER PRESENT; WINDOWS PYTHON PREREQUISITE COMPLETE - PRODUCTION OPERATOR VALIDATED; WINDOWS CPYTHON 3.13.X SUPPORTED - VALIDATED PATCH 3.13.15; CPYTHON 3.14.7 PRESENT - NOT HIOC-SUPPORTED; PE-3 ACTIONS 1-10 COMPLETE; ACTION 10 COMPLETE - NOOP_ALREADY_ABSENT; PRODUCTION DEPLOYMENT COMPLETE; PI3 VALIDATION COMPLETE; PE-4 IN PROGRESS - ACTION E PASS/CLOSED; ACTIONS F/G NOT STARTED**

The implementation-ready design is maintained in
[PASSIVE_ENRICHMENT_ARCHITECTURE.md](PASSIVE_ENRICHMENT_ARCHITECTURE.md). It
maps every current passive source, audits the permissive inventory schema,
separates observed, derived, operator-managed, and relationship metadata, and
defines field-level authority, provenance, confidence, conflict, privacy, and
rollback contracts.

The completed minimum implementation is a parallel, local-only hostname
evidence envelope. It proved deterministic candidate selection and
conflict preservation without changing identity, canonical address, public
inventory, MQTT, Home Assistant, dashboards, incidents, liveness, health, or
retention. Repository implementation, governed deployment, Git-derived
artifact identity, authoritative schema validation, and corrected production
validation passed. Production reported `online`, 153 records, 83 candidates,
82 selections, and zero conflicts. Expected availability, permanent-IoT monitoring, Home Assistant
availability correlation, automation impact, incidents, retention, DHCP
service health, and `.152` lease cleanup remain separate future work.

The permanent design distinguishes **Observation** (what passive sources saw),
**Enrichment** (what HIOC learned or inferred), and **Asset** (what the operator
knows and intends). These layers have separate authority, mutability,
persistence, provenance, privacy, and operational meaning. They reference one
another without destructive transformation. PE-0 is complete and design
approved. The PE-1 package in
[PE1_HOSTNAME_ENRICHMENT_SPEC.md](PE1_HOSTNAME_ENRICHMENT_SPEC.md) is
implemented, deployed, and production validated. It adds only private local
sidecars and does not change public inventory or consumer/operational contracts.
The absence of trusted-integration, historical, and conflict candidates in the
validated production snapshot is acceptable. PE-2.0 is design approved in
[PE2_ASSET_FOUNDATION_SPEC.md](PE2_ASSET_FOUNDATION_SPEC.md). It defines a
separate stable-ID-keyed, local-only Asset store and governed CLI for
`friendly_name`, `physical_location`, `purpose`, and private `notes`, while
deferring owner, public projection, expected availability, lifecycle, and
identity migration. The PE-2.1 implementation design is approved in
[PE2_ASSET_IMPLEMENTATION_DESIGN.md](PE2_ASSET_IMPLEMENTATION_DESIGN.md), and
its private Asset foundation is implemented, deployed, and production validated.
Repository evidence is in
[PE1_HOSTNAME_ENRICHMENT_EVIDENCE.md](PE1_HOSTNAME_ENRICHMENT_EVIDENCE.md) and
[PE2_ASSET_FOUNDATION_EVIDENCE.md](PE2_ASSET_FOUNDATION_EVIDENCE.md).

PE-3.0 manufacturer-reference architecture is defined in
[PE3_MANUFACTURER_ENRICHMENT_SPEC.md](PE3_MANUFACTURER_ENRICHMENT_SPEC.md).
It selects pinned IEEE Registration Authority public assignment listings as the
authoritative upstream, subject to an explicit redistribution-license gate before
any dataset is committed or distributed. Manufacturer is private descriptive
Enrichment only and cannot affect identity, address selection, availability,
operations, Asset facts or consumer contracts. The frozen PE-3.1 executable
contract is [PE3_MANUFACTURER_EXECUTABLE_CONTRACT.md](PE3_MANUFACTURER_EXECUTABLE_CONTRACT.md):
an externally injected normalized database, separate manufacturer sidecar,
O(1) longest-prefix lookup, closed provenance, fail-open isolation, exact APIs,
commands, schemas, transactions, and a 92-test mapping. The executable is
repository validated. PE-3.2 validated the production-intended database and
manifest in the external operator workspace; neither artifact is committed or
deployed. Local transformation is approved; commit and redistribution remain prohibited.

---

## Planned Phase

### Phase 7B - Safe Active Discovery

Status:

Not started.

This phase is intentionally postponed until Phase 7A is complete.

Goals include:

- Manual discovery
- Scheduled low-frequency discovery
- Safe network probing
- No continuous scanning
- No aggressive port scanning

---

### Future Phase - DHCP Service Health & Capacity Monitoring

Status: **PLANNED; NOT IMPLEMENTED**

Originating production evidence: [July 29, 2026 DHCP Pool Exhaustion Incident](INCIDENT_2026-07-29_DHCP_POOL_EXHAUSTION.md). This phase does not supersede Phase 7A, its corrective checkpoints, or postponed Phase 7B.

#### Pool Utilization

Plan monitoring for configured pool size, active leases, free addresses, utilization percentage, configurable warning and critical thresholds, exhaustion, and trend over time.

#### Lease and Transaction Failures

Plan detection of repeated unsuccessful client acquisition attempts without assuming every failure is capacity-related. Future design must evaluate DHCP `DISCOVER`, `OFFER`, `REQUEST`, `ACK`, `NAK`, declines, timeouts, repeated attempts, and incomplete exchanges. Packet capture may be evaluated as a design option but is not selected by this plan.

#### Selective Allocation Failure

Detect the condition where the DHCP daemon is active and some clients retain connectivity while new or renewing clients cannot obtain usable leases. Daemon-up status alone is insufficient.

#### Planned Health and Incident Semantics

Interpret service evidence through existing project conventions for healthy, warning, degraded, critical, and unavailable states. Plan stable incident lifecycle behavior for high and critical utilization, exhaustion, unanswered requests, missing OFFER or ACK behavior, abnormal lease churn, transaction failures, selective degradation, recovery, and resolution. Do not implement or conflate the deferred incident-history validator rewrite.

#### Planned Dashboard Visibility

Plan current DHCP health, utilization, free capacity, trend, active warning or incident, recent transaction failures, affected-client count where measurable, and last successful DHCP activity. No HIOC dashboard endpoint or port is established by this phase.

#### Future Production Validation

Validation must cover normal capacity, warning threshold, critical threshold, full pool, successful lease recovery after capacity restoration, selective client failure, daemon healthy while service is degraded, incident creation and resolution, dashboard accuracy, and no false offline state for retained leases. Implementation, tests, deployment, production Evidence Report, and documentation closeout are all required before this phase may be complete.

---

## Future Enhancements

The authoritative passive-enrichment roadmap is ordered and mandatory:

1. **PE-1 - Hostname Enrichment** — complete, production validated.
2. **PE-2 - Asset Foundation** — complete, production validated.
3. **PE-3 - Manufacturer Reference Enrichment** — complete. Actions 1–10,
   production deployment, generation, PI3 validation, final Evidence Report,
   administrative Action 10 closure, and final governance closure are complete.
4. **PE-4 - Home Assistant Association** — in progress; D/E/F/G PASS/CLOSED; E handoff ACCEPTED; PE-4.0B.2a PASS/CLOSED; original 2b preparation complete; first 2b execution historically ATTEMPTED / NOT COMPLETE; Compatibility Resilience audit PASS/CLOSED; corrected preparation and PE-4.0B.2b PASS/CLOSED; PE-4.0C and PE-4.0C.1 PASS/CLOSED; adapter implementation preparation PASS/CLOSED; Runtime Credential Provisioning Preparation PASS/CLOSED; Runtime Credential Provisioning PREPARED / NOT COMPLETE; Operator Installation and Independent Validation NOT STARTED; adapter implementation NOT STARTED; PE-4 NOT COMPLETE.
5. **PE-5 - MQTT and Passive Service Association** — not started.
6. **PE-6 - Classification & Metadata Quality** — not started.
7. **PE-7 - Expected Availability & Permanent IoT Monitoring** — planned. This
   models Asset-layer expected-online intent for wall switches, smart switches,
   smart plugs, Sonoff devices, permanent lighting controls, and other
   infrastructure devices; correlates network and Home Assistant availability;
   detects failure to reconnect; and produces actionable incidents,
   notifications, affected automation/function identification, and recovery
   guidance.
8. **PE-8 - Automation Correlation & Impact Analysis** — planned. It maps Home
   Assistant automations, scripts, scenes, triggers, entities, and Assets to
   functional impact.
9. **PE-9 - Service & Infrastructure Dependency Intelligence** — planned. It
   models MQTT, DNS, DHCP, Pi-hole, Home Assistant, NUT, cameras, switches, and
   other services to explain technical cause, failure propagation, service
   impact, and infrastructure topology. PE-8 owns functional impact; PE-9 owns
   technical dependency and cause.
10. **PE-10 - Application, Integration & Service Assurance** — planned / not
    started. After PE-8 maps operator-visible impact and PE-9 establishes the
    technical dependency model, PE-10 will determine whether an application-
    level function is actually usable, isolate the failing layer, and design
    evidence-based controlled recovery. It is future architecture work and is
    separate from the current PE-3 execution sequence.

Separate governed future checkpoints also preserve:

- Dependency graph visualization
- Infrastructure topology
- Automatic service relationships
- Failure propagation visualization
- Historical infrastructure trends
- Predictive recommendations
- Expanded operational analytics
- Asset-aware configurable retention and archival for stale passive clients.
- Incident-history validator hardening: stable incident identities, timestamp
  `resolved`, legacy `end_time`, optional legacy lifecycle, and mixed schemas.
- Notification semantics translating UPS/NUT states such as `OL LB` into cause,
  severity, recommended action, line/on-battery/low-battery/driver distinctions,
  and impact-aware internet latency severity.
- Infrastructure Backup, Disaster Recovery, and Hardware Migration for both PI3
  NUT&PIHOLE and PI5 HA, including services, configs, data, secrets, permissions,
  ACLs, schedulers, networking, MQTT, off-device backups, restore validation,
  hardware replacement, HA backup awareness, independent host recovery, and
  full-machine migration.
- PI3 + PI5 Abrupt Power-Loss / Cold-Boot Recovery Validation, as a separate
  operational-hardening checkpoint: actual abrupt power loss; filesystem and
  storage integrity; automatic boot; systemd/Docker and HIOC recovery; PI3
  Pi-hole/DHCP/NUT recovery; PI5 Home Assistant dependency recovery; MQTT and,
  where applicable, go2rtc/camera recovery; simultaneous-boot network retry;
  HIOC database/state and manufacturer dataset/config persistence; no `/tmp`
  dependency or manual intervention; correct incident/state semantics; logs
  free of corruption indicators; and a final Evidence Report PASS.

These items remain intentionally out of scope until the current roadmap reaches them.

### Compatibility Diagnostics UX

Status: **PLANNED / NOT STARTED — ROADMAP PRESERVATION ONLY**

Objective: make dependency compatibility failures visible and understandable
without requiring SSH, JSON inspection or source-code debugging. This named
checkpoint is permanent future roadmap work; it is not implemented or authorized
by the current governance completion and does not reorder PE-4 or other phases.

Planned presentation layers:

1. authoritative PI3 compatibility state;
2. HIOC logs;
3. retained MQTT compatibility status;
4. Home Assistant HIOC dashboard compatibility/system-health presentation;
5. persistent Home Assistant notifications for actionable compatibility failures;
6. later integration with the existing phone-notification semantics checkpoint.

#### Dashboard Compatibility Presentation

Remain quiet/normal for `COMPATIBLE`; do not alarm merely for
`COMPATIBLE_UPDATED`. Actionable failures identify the dependency and affected
subsystem, distinguish degraded/incompatible/unavailable/trust-change conditions,
provide recommended operator action and show what remains unaffected where
practical. Visual design and exact wording are not frozen.

#### Persistent Home Assistant Notifications

Future persistent Home Assistant notifications are required for actionable
compatibility problems according to subsystem impact: `INCOMPATIBLE`,
`TRUST_ANCHOR_CHANGED`, significant `COMPATIBILITY_DEGRADED`, or required
`DEPENDENCY_UNAVAILABLE`. `COMPATIBLE_UPDATED` alone must not trigger an alarming
persistent notification. This is a future UX commitment, not current implementation.

#### Phone-Notification Integration

Compatibility events will later feed the existing planned phone-notification
semantics checkpoint. Do not create a second or conflicting phone notification
architecture. That work determines severity, wording, rate limiting and actionability.
The existing UPS/NUT and internet-latency notification roadmap remains preserved.

#### User-Visible Diagnostic Semantics

A compatibility warning must answer: what changed; which dependency is affected;
which capability stopped being compatible; which HIOC subsystem is affected;
what remains operational; what the operator should do next; and whether an
update is a likely cause or causality is unproven. Literal UI wording is not frozen.

### PE-10 - Application, Integration & Service Assurance

Status: **PLANNED / NOT STARTED — FUTURE ARCHITECTURE**

Architectural principle: **Infrastructure health is not the same as service
health.** Ping, neighbor/ARP presence, or an `online` device state does not prove
that the application-level function an operator depends on is usable. HIOC must
eventually answer, "Will this function work when the operator tries to use it?"
as well as, "Is this device online?"

This phase complements rather than replaces PE-7 expected availability, PE-8
functional-impact correlation, PE-9 dependency intelligence, the asset-centric
Living Digital Twin, retention/archival, backup/DR/hardware migration, and the
separate abrupt-power-loss/cold-boot checkpoint. PE-7 asks whether an asset
should be online and is online. PE-10 asks whether the capabilities and services
provided by the asset and its dependency chain are usable.

#### Home Assistant integration health and state freshness

The motivating incident is an intermittent real Tuya / Smart Life failure: a
presence sensor reported correctly in Smart Life while Home Assistant continued
to show occupancy clear because its Tuya integration had stopped refreshing.
Reloading the integration restored the presence state and caused other stale
Tuya-backed states to update, revealing that failures such as outdoor lighting
remaining on during daylight could otherwise go unnoticed. The operator had
usually discovered the condition only after an expected automation failed.

Future design must keep these evidence layers distinct:

1. physical/device availability;
2. local network availability;
3. applicable Internet/cloud dependency availability;
4. vendor service availability;
5. Home Assistant integration health;
6. Home Assistant entity availability;
7. state freshness;
8. state consistency or corroboration;
9. automation dependency; and
10. operator-visible functional impact.

An available entity is not sufficient evidence of a healthy integration.
Investigation must consider, without prematurely selecting one mechanism,
entity `last_updated`/`last_changed` behavior, integration update activity,
expected event cadence, independent observations, correlated staleness across
entities in one integration, network/cloud/device reachability, Home Assistant
config-entry state, automation behavior, and historical state patterns.

#### Dependency, impact, and asset-capability model

PE-10 consumes and extends the existing graph work rather than inventing a
parallel model. A representative functional chain is:

```text
Office Presence Function
  -> Tuya presence sensor
  -> network/cloud connectivity
  -> Tuya vendor service and Home Assistant integration
  -> Home Assistant entity and office-presence automation
  -> Hue lighting service
  -> Office Hue lights
```

HIOC should progressively isolate the failed domain and identify the affected
operator-visible function, using PE-8 impact relationships and PE-9 automatic
service relationships, dependency graphs, failure propagation, and topology.
The asset model must expose independently monitored capabilities rather than a
single online/offline flag. An Office Speaker can separately expose network
presence, IP/MAC identity, DNS/Internet connectivity, mDNS advertisement, Cast
service, Home Assistant representation, and dependent automations. An Office
Presence Sensor can separately expose network/cloud reachability, vendor
service, HA integration, entity freshness, automation, and downstream lighting.

#### Safe automated recovery

Future remediation is evidence-based, bounded, and policy controlled. If device,
network, external connectivity, and Home Assistant evidence are healthy while
multiple Tuya-backed states are stale and evidence isolates the HA Tuya
integration, an operator policy may eventually allow a controlled integration
reload. The design must require bounded retries, cooldown/backoff, loop
prevention, pre-remediation evidence, post-remediation functional validation,
incident history, operator notification, escalation on failure, configurable
automation policy, and manual approval for risky actions. A successful API or
service call alone does not prove recovery.

#### Casting and media service assurance

Google Cast and similar services are explicit PE-10 use cases. Design must
separately test device availability; LAN/subnet/VLAN/routing/firewall/Wi-Fi path;
mDNS/DNS-SD advertisement and discovery; application-level Cast response; Home
Assistant visibility and state freshness; harmless functional capability; and
Internet, firmware, API, protocol, or manufacturer dependencies. Synthetic
checks must be non-disruptive and must never play random audio or video merely
to establish health.

#### Incident and notification experience

Service-assurance notifications must identify the affected function/service,
severity, affected assets, tests performed, healthy and failed evidence, likely
failure domain, operator impact, recommended action, any automated recovery,
and its result. Recommendations must be the narrowest evidence-supported action.
Design targets include a multi-endpoint Cast failure where speakers remain
online but mDNS discovery and Home Assistant discovery fail, leading HIOC to
recommend multicast/discovery investigation rather than device reboot; and an
isolated Office Speaker failure where network, DNS, Internet, mDNS, and other
Cast devices are healthy but that endpoint does not respond, leading HIOC to
recommend restarting only that speaker.

### Status Vocabulary

- **COMPLETE - DESIGN APPROVED:** the design gate is closed; implementation is
  not implied.
- **IMPLEMENTED - REPOSITORY VALIDATED:** executable work and repository tests
  pass; deployment is not implied.
- **COMPLETE - EXTERNAL DATASET VALIDATED:** bounded external artifacts passed
  validation without entering Git; deployment is not implied.
- **COMPLETE - PRODUCTION VALIDATED:** governed deployment and production
  evidence passed and the checkpoint is closed.
- **IN PROGRESS:** authorized work has begun and closure criteria remain.
- **PLANNED / NOT STARTED:** roadmap scope is preserved but work has not begun.
- **OPEN / DEFERRED / POSTPONED:** preserved work is intentionally not current;
  the owning section must state its future gate.

### Phase 7A Continuity and Deferred Hardening

Phase 7A remains focused on trustworthy passive discovery and enrichment. Completed corrective checkpoints, including Watch-device discoverability, remain part of that foundation. Deferred Phase 7A work remains preserved:

- Configurable passive-client retention and archival, after asset policy is designed.
- Canonical local-address hardening without production-specific identity exceptions.
- An explicit historical identity continuity decision covering immutable evidence IDs, alias or promotion resolution, and migration policy without presupposing a schema.
- Continued Phase 7A enrichment from passive sources.

Active Discovery remains postponed. Future YAML dashboard deployment modernization also remains planned and must not be folded into unrelated inventory checkpoints.

### Asset-Centric Evolution

After reliable passive identity is established, Living Inventory should gradually evolve from unknown technical devices into identified, operator-managed assets. Planned capabilities include:

- Operator asset identity and friendly naming.
- Physical location and purpose.
- Owner or responsible person.
- Asset classification and operational criticality.
- Expected availability and explicit monitoring expectations.
- Asset lifecycle state, including active, retired, and archived concepts.
- Maintenance expectations, purchase or installation context, maintenance history, notes, and optional photo references.
- An operator workflow for physically matching discovered MAC addresses and other stable evidence to real assets.
- Operator-approved asset linkage that may associate multiple discovered identities, including identities created by randomized or rotated MAC addresses, with one physical asset without heuristic passive merging.
- Gradual enrichment from an unknown device to an identified, managed asset without losing discovery provenance.
- Safe configurable retention and archival governed by asset policy rather than stale age alone.

These are future concepts. They do not add runtime fields or change current health, monitoring, incident, retention, or discovery behavior.

### Roadmap Dependencies

- Stable identity and passive discovery are foundational to operator asset enrichment.
- Asset classification must exist before aggressive archival can be safe.
- Expected availability must be defined before disappearance can be treated as failure.
- The improved dependency graph, automatic service relationships, failure propagation visualization, and infrastructure topology become more meaningful after assets and services are identified.
- Historical infrastructure trends and predictive recommendations depend on reliable identity, asset classification, relationships, and retained history.

The asset-centric vision expands the meaning of future work; it does not replace or reorder any existing phase or capability.

---

# Repository and Deployment Governance

HIOC formally separates the authoritative source checkout from the deployed production runtime:

```text
GitHub
  |
  v
/home/jazofv1/hioc-release-source
  authoritative source checkout for release execution on PI3
  |
  | release validation and the supported release process
  v
/home/jazofv1/hioc
  deployed production runtime
```

Deliberate source changes are developed and validated in an authorized development checkout, then committed and pushed to GitHub as the shared project history. After the approved changes are pulled on PI3, `/home/jazofv1/hioc-release-source` is the authoritative source checkout for release preparation and the supported release workflow. It should remain clean except for deliberate release work in progress.

`/home/jazofv1/hioc` is the deployed production runtime. It is expected to contain persistent operator configuration, runtime state, incident and inventory history, logs, backups, generated files, installer-managed permissions, and other operational artifacts. Production updates must use the supported release process from the authoritative source checkout or a validated release package, not direct Git updates inside the runtime.

The current repository workflow was not introduced through a single planned migration. It evolved organically as operational experience demonstrated the need to separate a clean development and release checkout from the production runtime. This document formalizes that proven workflow rather than introducing a new architectural model.

The production runtime is formally a non-Git deployment target. Its historical `.git` directory was residue from the former clone-in-place installation model, not an operational dependency, and has been retired. The authoritative Windows repository, GitHub, and `/home/jazofv1/hioc-release-source` own Git history and source operations. Retirement preserved configuration, state, history, logs, backups, credentials, permissions, and all other operational data.

## Repository and Deployment Hygiene Checkpoint

Status: **COMPLETE**

The source/runtime architecture is settled and is not being reopened. The Windows repository work, PI3 release-source audit, runtime provenance audit, controlled runtime Git quarantine and removal, production engineering validation, upgrade proof, rollback proof, and source/runtime consistency validation are complete. All Repository and Deployment Hygiene closure criteria are satisfied.

### Release Boundary Hardening

Status: **COMPLETE**

**Engineering problem:** `release/build.sh` previously traversed the working directory and attempted to protect the release through exclusion patterns. Git ignore rules did not participate in that traversal, so an ignored or untracked workspace artifact could enter a release unless it happened to match a build-specific exclusion. Release contents could therefore depend on workspace residue rather than solely on intentional repository source.

**Implemented solution:** Release construction now obtains its complete source set from the repository index through Git's NUL-delimited tracked-file listing. Each copied file is included because it is explicitly tracked; ignored, untracked, cache, recovery, and temporary files are outside the source set without relying on filename exclusions. This preserves the existing build directory, version lookup, project-file layout, and downstream package and deployment flow. `RELEASE_MANIFEST.txt` remains the one intentionally generated build file and now records stable version, build, and source-commit values without checkout-path or wall-clock fields.

**Validation:** Focused release tests prove that the build is Git-aware, uses a NUL-safe tracked-file stream, does not fall back to workspace traversal or a special `*.tmp` exclusion, and produces a checkout-independent manifest. The then-existing ignored `hioc_known_hosts.tmp` file was retained during this sub-checkpoint as validation evidence and was excluded because it was not tracked, as are arbitrary future ignored or untracked artifacts; its later workspace disposition is recorded under Repository Governance Reconciliation. Tracked project files remain the build input. Focused release and version tests, the full regression suite, Python compilation, shell syntax validation, release validation, and direct build-content comparison passed. No runtime, inventory, Home Assistant, deployment, upgrade, validation, or public-contract behavior changed.

### Changelog Governance Reconciliation

Status: **COMPLETE**

Git history establishes the intended single-authority model. Documentation-governance commit `5b2fe6ed2a4f7916032198c4ecaf645aa3937b72` migrated released-work history into `docs/CHANGELOG.md`, declared that file's ownership, converted root `CHANGELOG.md` into a discoverability pointer, and directed README readers to the authoritative docs path. Implementation commit `054fb55a2e70901f3230145b76983c31d2b5ce61` later replaced the root pointer with a bounded Collector Canonical Ownership implementation entry. Subsequent production-validation and closeout work correctly updated `docs/CHANGELOG.md`, leaving the duplicate root entry stale.

The original governance model is restored: `docs/CHANGELOG.md` is the single authoritative record of released and delivered work, and root `CHANGELOG.md` is a pointer retained for conventional repository discoverability. Future release and completed-checkpoint entries must be written only to `docs/CHANGELOG.md`. A second overlapping full changelog is prohibited unless a separately approved governance decision establishes a distinct, non-overlapping purpose. Git history preserves all earlier root content, so the pointer loses no historical traceability. README already targets the authoritative file; release and installer tooling merely exclude the root source-only path and require no change.

The stale Collector Canonical Ownership statement is removed from the active root pointer. The authoritative changelog and Master Plan record the complete evidence chain: implementation, regression validation, production validation, and documentation closeout all completed. Documentation links, release-contract tests, the full regression suite, and `git diff --check` passed. No application, release, deployment, test, inventory, or Home Assistant behavior changed.

### Repository Governance Reconciliation

Status: **COMPLETE**

Decision date: **2026-07-28**

Every remaining Windows repository governance artifact has an explicit disposition:

| Artifact | Evidence | Disposition |
|---|---|---|
| `validation/phase-7a8-lifecycle` | Its sole branch-only commit, `be7b69d1da1a3b5c3c7a9e7ca27d1280b8f41cd1`, adds the asset-lifecycle foundation and is not an ancestor of `main`. `docs/RECOVERY_BASELINE.md` identifies that exact commit and tree as the approved Phase 7A.8 recovery candidate. No tag or other branch preserves it. | **Retained intentionally**, locally and on `origin`, as the named reachability reference for the immutable approved recovery candidate. It is not approved for merge into `main`; future disposition requires a separate evidence-based decision that preserves the recovery reference. |
| `correlation-engine-v2` | Tip `42ea8d2d1ebeecc6e18aff6bb35dccea00e86426` is an ancestor of `main` through merge commit `80411124e584da17c8f532dbae0cd54a638ef181`; no unique commit remains. Its remote branch was already absent. | **Resolved:** deleted locally. Commit history remains reachable from `main`. |
| `docs/reconcile-phase-7a8-recovery-baseline` | Tip `0463a648b93626ca8a0570654cb4074ed21a01aa` is an ancestor of `main` through merge commit `f20b161b1a0f7cb59d994f25f1bf84d1d0e8db96`; its recovery documentation remains on `main`. | **Resolved:** deleted locally and remotely. Commit history remains reachable from `main`. |
| `docs/repository-deployment-governance` | Tip `8174187c04591319374e2f72c37dac9e731c5a5c` is an ancestor of `main` through merge commit `8a35d6d3746cf001a88b558f63d673797262ec43`; its governance documentation remains on `main`. | **Resolved:** deleted locally and remotely. Commit history remains reachable from `main`. |
| `hioc_known_hosts.tmp` | The ignored root file contained one SSH host-key line and had no Git history. No runtime, release, deployment, or automation code consumed it; a focused regression assertion mentions its name only to prove that it is absent from Git-tracked release inputs and does not require the file to exist. SSH host trust is user-workspace state, not project source. | **Resolved:** removed from the repository workspace. Future SSH known-host artifacts must be stored in the user's SSH configuration area or another external temporary location, never in the repository. |

The retained lifecycle branch is not stale or ambiguous: it has a documented recovery-evidence purpose and must remain until a separately approved archival or integration decision provides an equally durable reference. Fully merged topic branches should be removed after their merge and evidence are verified. Temporary access artifacts must remain outside the repository. These rules preserve historical reachability without treating completed topic branches or user-specific access state as active project source.

Validation confirmed the retained branch at its documented commit, all removed branch tips reachable from `main`, no dangling or broken Git references, valid Markdown links, a passing full regression suite, and a clean documentation diff. No application, release, deployment, inventory, Home Assistant, or runtime behavior changed.

### Runtime Git Metadata Retirement

Status: **COMPLETE**

The architectural investigation reviewed runtime code, installers, release build and packaging, upgrade, backup, rollback, validation, uninstall, version reporting, recovery documentation, operator workflows, ADRs, tests, and relevant Git history. It found no supported runtime, installation, validation, versioning, upgrade, rollback, or disaster-recovery dependency on `/home/jazofv1/hioc/.git`. Runtime version identity comes from `VERSION.yaml` and release metadata. Git is used only at the authoritative source boundary. The runtime `.git` directory is historical residue from the original installation model in which the production path was also a clone.

ADR-0013 is resolved: `/home/jazofv1/hioc` is a non-Git deployment target, all Git operations belong to an authoritative development repository or `/home/jazofv1/hioc-release-source`, and direct runtime Git workflows are unsupported. README installation guidance now uses the release-source workflow. Installation and deployment already excluded `.git`; this repository implementation additionally excludes `.git` from new upgrade backups and from rollback restoration. The rollback exclusion applies to historical backups and nested `.git` directories without excluding other hidden files. Existing protections for `config`, `state`, `history`, `logs`, `backups`, credentials, permissions, and installer-managed data remain unchanged.

Repository validation established the exact backup, deployment, and rollback contracts; continued persistent-state exclusions; `VERSION.yaml` as runtime version authority; Git-aware source construction only in the authoritative checkout; shell syntax; release build and package validity; documentation-link integrity; contradiction-free active guidance; the complete regression suite; and a clean diff. Focused release and version tests passed 13 tests with one Windows-only `rsync` availability skip. The full suite passed 183 tests with 7 skips. Python compilation, release validation, shell syntax, Markdown link checks, package construction, required-file checks, and archive inspection for `.git` all passed. The executable `rsync` semantics test preserves legitimate hidden files while excluding root and nested `.git` directories and will run on hosts where `rsync` is installed, including PI3. Repository implementation and documentation are committed and pushed together only after these checks pass.

Production migration, engineering validation, and quarantine removal are complete. `/home/jazofv1/hioc` is formally non-Git. Its historical `61/62 commits behind` condition is permanently resolved because that status described stale, intentionally excluded runtime metadata rather than deployed application content, and the runtime is no longer a Git checkout.

#### Production Evidence Report

**Deployment result:** `/home/jazofv1/hioc-release-source` was synchronized at commit `5d189535d81a5689b9d5f0d96caba49d3fee609c` with clean `main` matching `origin/main`. The supported hardened upgrade completed. Runtime Git metadata was moved to `/home/jazofv1/hioc-hygiene-evidence/runtime-git-quarantine-20260729T001505Z/runtime.git`, validated, and then removed after approval. `/home/jazofv1/hioc/.git` does not exist, the runtime is not a Git working tree, and quarantine removal reported `PASS`.

**Intended behavior:** The production runtime operates without Git metadata. Supported deployment, upgrade, backup, rollback, validation, version reporting, and recovery continue through release artifacts and `/home/jazofv1/hioc-release-source`. Runtime state and legitimate hidden files remain protected. Runtime Git metadata cannot be recreated by upgrade or restored by rollback.

**Validation performed:** The historical runtime repository reported HEAD `94e1997f0d9df9e43209e44f7eb62a8d808714cc`, while its stale `origin/main` reference was `5d189535d81a5689b9d5f0d96caba49d3fee609c`. Its HEAD was an ancestor of authoritative history; no runtime-only commits, branches, tags, or stashes existed. The approximately 2.6 MB repository was quarantined, remained readable, and passed `git fsck --full`. Pre-migration evidence at `/home/jazofv1/hioc-hygiene-evidence/pre-migration-20260728T231517Z` inventoried 17,449 runtime paths, checksummed 72 deployment-managed files, recorded persistent directories and Git provenance, and included an evidence checksum manifest. `pi4/validate_pi4.sh` passed after quarantine. A subsequent supported non-Git upgrade and controlled rollback both completed, left the runtime non-Git, and passed production validation. Post-rollback SHA-256 comparisons matched release source and runtime for `release/upgrade.sh`, `release/rollback.sh`, `release/validate.sh`, `pi4/validate_pi4.sh`, and `VERSION.yaml`.

**Invariant checks:** Upgrade backup `/home/jazofv1/hioc/backups/release-upgrade-20260728-181815`, install backup `/home/jazofv1/hioc/backups/install-20260728-181815`, and the plain-text `last-upgrade-backup` pointer were valid. Rollback from that release-upgrade backup did not restore `.git`. `VERSION.yaml` remained valid. Binaries, configuration, runtime state, JSON projections, cron entries, DHCP lease access, version declarations, validators, and persistent runtime data remained operational and intact. Checked deployment artifacts matched the authoritative release source after rollback.

**Warnings / remaining action:** No Repository and Deployment Hygiene engineering work remains. Interactive console sessions that closed during evidence collection are not classified as HIOC failures: upgrade, rollback, and validation completed successfully, and pasted commands used persistent interactive `set -euo pipefail` with visible paste corruption. Future interactive validation should contain strict mode inside a script or subshell and capture output and exit status so the outer session remains open.

**Final result:** **PASS; REPOSITORY AND DEPLOYMENT HYGIENE COMPLETE**

Closure requires every item below:

- [x] hardened backup behavior validated;
- [x] hardened rollback behavior validated;
- [x] documentation reconciled through the production Evidence Report working-tree update;
- [x] runtime `.git` provenance captured;
- [x] unique runtime-only commits ruled out;
- [x] runtime `.git` quarantined outside both repositories;
- [x] production validation passes without runtime `.git`;
- [x] supported upgrade does not recreate `.git`;
- [x] supported rollback does not restore `.git`;
- [x] persistent `config`, `state`, `history`, `logs`, and `backups` remain intact;
- [x] quarantine copy removed after final approval;
- [x] production Evidence Report recorded in this working-tree update;
- [x] final documentation closeout prepared and validated;
- [x] Windows `main`, `origin/main`, and PI3 release-source synchronization established for the validated implementation baseline;
- [x] documentation-only working-tree scope confirmed for final review.

The overall Repository and Deployment Hygiene checkpoint is complete. Runtime migration, production validation, supported upgrade and rollback proof, quarantine removal, evidence documentation, and repository-scope validation are complete.

**Remaining Repository and Deployment Hygiene checkpoints:**

None. Repository and Deployment Hygiene is complete.

Repository and runtime artifacts use these disposition categories:

| Category | First-pass classification |
|---|---|
| AUTHORITATIVE SOURCE | GitHub `main` and the clean source checkout at `/home/jazofv1/hioc-release-source`. |
| DEPLOYED APPLICATION | `pi4/bin/`, `pi4/lib/`, required runtime configuration examples and support files, and `homeassistant/`. Preserve. |
| PERSISTENT RUNTIME DATA | `config/`, `state/`, `history/`, and `logs/`. Preserve. |
| DEPLOYMENT TOOLING | `release/`, `pi4/install_pi4.sh`, `pi4/uninstall_pi4.sh`, `pi4/validate_pi4.sh`, `homeassistant/install_ha.sh`, `homeassistant/validate_ha.sh`, and `VERSION.yaml`. Preserve pending dependency review. |
| BACKUP / ARCHIVE | `backups/`. Preserve pending backup and retention review. |
| GENERATED / TRANSIENT | `__pycache__/`, `*.pyc`, `.pytest_cache/`, and similar generated caches. Cleanup candidates only after validation. |
| SOURCE-ONLY | `README.md`, `ROADMAP.md`, `DECISIONS.md`, `CHANGELOG.md`, and `docs/` remain in authoritative source and are excluded from production deployment. |
| SOURCE / RELEASE VALIDATION | `tests/` is used by `release/validate.sh` in the source or release-validation context and is excluded from production deployment. |
| RETIRED HISTORICAL RUNTIME METADATA | The production runtime's former `.git/` directory was proven historical residue, quarantined, validated, and removed after approval. It was not source, runtime state, or a recovery dependency. |

### Dependency Review Findings

The initial dependency review is complete for the current provisional source-only candidates. It reflects the evidence gathered against the current deployment architecture and establishes the baseline for subsequent deployment-manifest validation. No runtime, cron, systemd, installer, rollback, Home Assistant, or other operational dependency was discovered for `README.md`, `ROADMAP.md`, `DECISIONS.md`, `CHANGELOG.md`, or `docs/`. References among those files are documentation-to-documentation links rather than runtime dependencies.

`tests/` has a different role: `release/validate.sh` compiles the repository's test tree during source or release validation. This establishes a source/release-validation dependency but does not establish that `tests/` is required in the production runtime.

PI3-only recovery commit `5d0473dfd20efe7b07cf9167803d02aead10d61e` was reviewed against the authoritative `origin/main` history. Its `docs/RECOVERY_BASELINE.md` content is byte-for-byte identical to the authoritative version, and every substantive Master Plan addition is already present. The commit is therefore formally superseded and requires no merge or cherry-pick. It was temporarily preserved on the PI3 local branch `recovery/phase-7a8-documentation-pi3` until this supersession record was committed and pushed; that condition was satisfied, and branch removal was then separately validated.

The deployment exclusions were implemented in `release/upgrade.sh` and `pi4/install_pi4.sh`. Future production copies exclude the six approved source-only root paths without adding `--delete`; runtime-generated, persistent, and operational content remains preserved.

### Production Evidence Report

**Deployment result:** PI3 authoritative source was fast-forwarded to `9f0653075bbe67cc880904e6a4970dcab004d401`; source `main` matched `origin/main`, and the working tree was clean. Updated `release/upgrade.sh` and `pi4/install_pi4.sh` were copied into the production runtime, where their SHA-256 hashes exactly matched the authoritative source copies.

**Intended behavior:** Production deployments exclude the source-only root paths `README.md`, `ROADMAP.md`, `DECISIONS.md`, `CHANGELOG.md`, `docs/`, and `tests/`. Runtime deployment continues without `--delete`, preserving runtime-generated and operational directories.

**One-time cleanup:** The six approved source-only paths were removed from `/home/jazofv1/hioc`. Copies remain in authoritative source and in `/home/jazofv1/hioc/backups/release-upgrade-20260720-185835/current`.

**Invariant validation:** Runtime `config/`, `state/`, `history/`, `logs/`, `backups/`, and `pi4/bin/` remained present. An `rsync` dry run confirmed that the six excluded source-only paths would not be copied back. Final production hygiene validation result: **PASS**.

**Repository governance:** The temporary local PI3 branch `recovery/phase-7a8-documentation-pi3` was deleted only after its superseded commit was documented and preserved in authoritative history. The PI3 source repository remained on clean `main`, synchronized with `origin/main`.

### Unresolved Operational Issue

During `release/upgrade.sh`, `pi4/install_pi4.sh` reached its existing invocation of `hioc-incident-engine-v2.py`, which failed with `OSError: [Errno 7] Argument list too long: 'mosquitto_pub'`.

The incident-engine invocation was neither introduced nor changed by the Repository and Deployment Hygiene work; the only `pi4/install_pi4.sh` change in this checkpoint was the addition of the six `rsync` exclusions. The MQTT publishing failure is therefore not attributed to the hygiene implementation. At that closeout it remained unresolved and was assigned to a separate, scoped investigation; the hygiene checkpoint itself did not diagnose, redesign, or propose a correction for it.

### Incident History MQTT Transport Correction

Status: **COMPLETE**

The repository archaeology and architecture investigation are complete. Established production evidence shows that `state/incidents/history.json` was approximately 193,053 bytes with 24 records and that complete publication through one `mosquitto_pub -m` process argument reproduced `E2BIG`; the supported upgrade therefore returned failure. This immediate transport failure does not by itself decide whether transport, storage representation, retention, or the external payload contract should change.

The architecture is recorded as separate layers: authoritative local history is written before MQTT; completed records intentionally contain embedded operator-facing reviews; review data and review-derived summary fields are externally observable; established retained topics and incident fields are compatibility contracts; and the `mosquitto_pub -m` invocation is an internal legacy mechanism. Correlation Engine v2 partially adopted Core while retaining a publisher already identified by the archived architecture review as technical debt. No evidence shows that retaining that subprocess implementation was an affirmative decision.

The bounded evidence, confirmed invariants, unresolved decisions, and neutral candidate comparison remain in [Incident History Storage and MQTT Publication Architecture Decision Preparation](INCIDENT_HISTORY_MQTT_ARCHITECTURE_DECISION_PREPARATION.md). Accepted [ADR-0014](../DECISIONS.md#adr-0014-use-core-mqtt-for-incident-publication) selects Candidate C: preserve local history, embedded Incident Review, retained topics, and external payloads while replacing only the Incident Engine's local subprocess publisher with the existing Core MQTT client. This removes the payload from the failing process-argument boundary, aligns the engine with shared Core architecture, minimizes consumer and migration risk, and introduces no new protocol.

The binding [Incident History MQTT Transport Implementation Specification](INCIDENT_HISTORY_MQTT_TRANSPORT_IMPLEMENTATION_SPEC.md) defines the exact connection lifecycle, publication order, compatibility boundary, failure and exit-status behavior, tests, deployment validation, rollback, documentation plan, and deferred work. Candidate C is implemented in the repository: Incident Engine publication uses one Core MQTT connection per run, retains the existing ordered topics and payload strings, stops on the first required failure, reports partial progress, and returns nonzero without discarding local state. Focused and full repository validation passed, and the supported production deployment and runtime validation completed successfully.

This bounded MQTT checkpoint was related to Phase 7A only because it blocked
truthful supported deployment and reliable incident publication. It remains
separate from incident-history schema-validator hardening, stale-client retention
and archival, repository and deployment hygiene, new inventory enrichment,
unrelated dashboard redesign, and broader MQTT protocol redesign. The completed
correction and validation return work to the authoritative roadmap so
operator-facing and dashboard progress can resume.

#### MQTT Runtime Validation Checkpoint

Status: **COMPLETE**

The repository now owns a bounded, read-only post-install and post-upgrade
validator for the retained Incident Engine MQTT contract. The deployed command
loads the existing toolkit and HIOC configuration, respects the configured HIOC
base topic, reads all seven retained incident and status topics with predictable
timeouts, validates payload presence and JSON or scalar status semantics, and
reports concise PASS, FAIL, INCOMPLETE, warning, byte-size, record-count, and
embedded-review evidence without printing credentials or publishing test state.
Focused and full repository validation passed. Operator production execution and
the required Evidence Report also passed.

This checkpoint does not change ADR-0014 transport, MQTT topics, retained flags,
payload schemas, broker configuration, Incident Engine behavior, Home Assistant,
or dashboards. Work now returns to the next incomplete checkpoint already
defined by this Master Plan.

##### Production Evidence Report

**Deployment result:** Implementation commit
`2b0b2ab6b9007a5a61025c847ceabb5030d8638a` was deployed through the supported
release workflow. Release validation, release upgrade, the standalone MQTT
validator, and general Pi4 validation all returned PASS. The production Evidence
Report is
`/tmp/hioc-mqtt-runtime-validation-20260723T040611Z/MQTT_RUNTIME_VALIDATION_PRODUCTION_EVIDENCE_REPORT.md`
with SHA-256
`01a7cac95e426b348b97222cc7b1f6deeee1147fbd1ae011efd6acee73f627f4`.

**Intended behavior:** The deployed validator resolves the broker through the
supported configuration hierarchy, performs subscription-only reads of the
seven required retained topics, validates payload presence and structure, and
reports PASS, FAIL, or INCOMPLETE without publishing or mutating retained state.

**Invariant checks:** All 7 required topics passed. Incident history was exactly
230660 bytes with 27 records and embedded review data present. Retained and local
history byte size, record count, and embedded-review evidence matched. No
hardcoded localhost assumption, credential disclosure, public-topic change,
payload-schema change, Home Assistant change, or retained-state mutation was
observed. The deployed validator SHA-256 was
`d4be8debbd9c926fbc3526bd0ae7f5f3473c68ef9853d7f0d995762170b12d53`.
The release-upgrade backup is
`/home/jazofv1/hioc/backups/release-upgrade-20260722-220732`, and the installer
backup is `/home/jazofv1/hioc/backups/install-20260722-220732`.

**Warnings and deferred risks:** None were reported by this production
checkpoint. TLS, explicit MQTT byte-size policy, broader broker resilience,
other legacy publishers, retention policy, and future MQTT architecture remain
outside ADR-0014 and are not marked complete.

**Final result:** **PASS**

---

# Repository Rules

Every completed phase must:

- Compile successfully
- Pass unit tests
- Validate Home Assistant YAML
- Preserve backward compatibility unless explicitly approved

Every checkpoint Evidence Report must state:

- Deployment result.
- Intended behavior.
- Invariant checks.
- Warnings and deferred risks.
- Final PASS or FAIL.

Repository and deployment rules:

- Investigate documentation first: review this Master Plan, applicable ADRs, architecture and data-model documents, Git history, implementation, and existing validation evidence before proposing production experimentation. Use production investigation only for a specific evidence gap that repository evidence cannot answer.
- Record every material architecture or implementation decision, compatibility boundary, assumption, validation result, deviation, deferral, and unresolved question in the appropriate repository document; do not leave authoritative conclusions only in chat, commits, code, test output, production state, or human memory.
- Keep investigations bounded to questions that materially block the current decision. Record unrelated improvements for later and return to roadmap and operator-facing progress after each corrective checkpoint.
- Begin all deliberate source changes in an authorized development checkout.
- Keep documentation and code synchronized when behavior and operating procedures change together.
- Never copy generated runtime state back into source control.
- Do not allow the production runtime to become an alternate development branch.
- Investigate and classify unexplained source/runtime divergence before cleanup.
- Do not remove obsolete-looking files without evidence that they are unused.
- Ensure deployments are reproducible from the authoritative source checkout on the target host or a validated release package.
- Classify runtime and generated artifacts explicitly, then preserve or exclude them intentionally.
- Commit accepted recovery manifests and similar historical evidence documents to the authoritative repository history. Keep approved historical records immutable; new recovery work must create new evidence instead of modifying them or leaving them only in temporary branches or local repositories.

Unless specifically requested:

- Do not redesign unrelated code
- Do not rename MQTT topics
- Do not rename entities
- Do not introduce breaking changes

---

# Commit Rules

Every completed phase ends with:

1. Validate the intended behavior.
2. Validate applicable invariants and backward compatibility.
3. Update the Implementation Status and any relevant roadmap, governance, or decision sections in this document.
4. Commit code and documentation together when both changed.
5. Push to main.
6. Verify the development checkout has a clean working tree and the shared history contains the approved commit.
7. Record an Evidence Report containing the deployment result when applicable, intended behavior, invariant checks, warnings, and final PASS or FAIL.

`docs/HIOC_MASTER_PLAN.md` remains the authoritative project source of truth.

## Operations Acceptance Standard

A release or completed checkpoint is not operationally complete until committed repository documentation answers, without requiring SSH discovery:

- What exists?
- Why does it exist?
- How does it run?
- How is it validated?
- How is it recovered?

Each completion review must verify:

- All new runtime components and their purposes are listed.
- Execution mechanisms, schedules, triggers, and locks are documented.
- Outputs, logs, status artifacts, and freshness expectations are documented.
- Validation and safe recovery procedures are documented.
- Relevant network ports and dependencies are documented without unsupported guesses.
- Current-state documentation and cross-references are synchronized.
- No critical operational fact exists only in chat history or only on the production host.

If production verification is required, it must be captured in an Evidence Report and committed back to the repository. This standard adds to, and does not weaken, the permanent workflow to validate, update the Master Plan and affected documentation, commit code and documentation together, push `main`, and verify a clean synchronized working tree.

---

### Operational Dependency Compatibility Acceptance

For each operational external dependency, committed repository documentation
must answer without ad hoc troubleshooting:

- What dependency does HIOC rely on?
- What capability does HIOC actually require?
- Is the version expected to float?
- How is compatibility determined?
- What status/error appears when compatibility breaks?
- Which HIOC subsystem is affected?
- What should the operator do?

Detailed answers may live in the registry and focused compatibility document;
this requirement remains part of the Operations Acceptance Standard.

# Working Agreement

While implementing HIOC:

- Stay focused on the current phase.
- Avoid scope creep.
- Record future ideas instead of implementing them immediately.
- Return to this document whenever a phase is completed.
- Keep changes consistent with the project's architecture and philosophy.

---

### External Dependency Compatibility Review

Whenever a new or changed external dependency, executable, API, protocol,
runtime, file format or data source is introduced, development must establish:

1. whether it is independently updated;
2. whether version is informational or gating;
3. the actual capability HIOC requires;
4. how compatibility is validated;
5. behavior after a compatible update;
6. behavior after an incompatible update;
7. diagnostic dependency identity;
8. affected subsystem/failure-isolation boundary;
9. whether exact identity is required for security/provenance; and
10. how the operator will know what happened.

Detailed answers may live in the registry/focused documentation, but this review
is a permanent Working Agreement completion requirement.

# Implementation Status

## Authoritative Current PE-4 Lifecycle

This section reflects the current project state and is updated at checkpoint
completion. Historical chronology elsewhere does not override it.

| Checkpoint | Current state |
| --- | --- |
| D | PASS/CLOSED |
| E | PASS/CLOSED |
| E handoff | ACCEPTED |
| F | PASS/CLOSED |
| G | PASS/CLOSED |
| PE-4.0B.2a | PASS/CLOSED |
| Original PE-4.0B.2b preparation | COMPLETE |
| First PE-4.0B.2b live execution (historical; superseded) | ATTEMPTED / NOT COMPLETE |
| Compatibility Resilience and Dependency Drift Audit | PASS/CLOSED |
| Compatibility Master Plan synchronization | PASS/CLOSED |
| Corrected PE-4.0B.2b execution preparation | PASS/CLOSED |
| Exact-version HA runtime gate | CORRECTED IN REPOSITORY |
| Corrected PE-4.0B.2b execution | PASS/CLOSED |
| PE-4.0B.2b | PASS/CLOSED |
| PE-4.0C | PASS/CLOSED |
| PE-4.0C.1 Association Lifecycle Clarification | PASS/CLOSED |
| PE-4 Home Assistant Association Adapter Implementation Preparation | PASS/CLOSED |
| PE-4 Home Assistant Runtime Credential Provisioning Preparation | PASS/CLOSED |
| PE-4 Home Assistant Runtime Credential Provisioning | PREPARED / NOT COMPLETE |
| Operator Credential Installation | NOT STARTED |
| Independent Credential Validation | NOT STARTED |
| Credential Provisioning Governance Closure | NOT STARTED |
| PE-4 Home Assistant Association Adapter Implementation | NOT STARTED |
| PE-4 | NOT COMPLETE |
| Phase 7A | ACTIVE |
| Rollback | NOT PERFORMED |

Replacement B, C, D-PREP and native prerequisites retain their accepted closures.
The E historical bridge retains NO_PERSISTED_E_TIME_RECURSIVE_BASELINE; both
historical recursive flags remain false. No new production authority follows
from this documentation-only checkpoint.

### Completed Compatibility Resilience and Dependency Drift Audit

The **HIOC Compatibility Resilience and Dependency Drift Audit** completed with
PASS at `8187114c7233be82b188f0fc03b93a022787e7bb`, independently reviewed and
accepted. Repository-wide scope included Home Assistant, Pi-hole/DHCP contracts,
NUT, Unbound where applicable (no consumed dependency was found), MQTT, go2rtc,
Python runtimes/packages, OpenSSH, Git, Bash/shell, PowerShell, Linux utilities,
filesystem/OS facilities and external APIs/protocols/file formats/data shapes
actually consumed by HIOC. Counts, matrix and unresolved live proofs remain in
[COMPATIBILITY_RESILIENCE.md](COMPATIBILITY_RESILIENCE.md); this checkpoint does
not repeat the audit or claim deployment.

### PE-4 Home Assistant Runtime Credential Provisioning Preparation - 2026-10-06

Repository Preparation PASS/CLOSED; parent Runtime Credential Provisioning is
PREPARED / NOT COMPLETE. The [provisioning contract](PE4_HOME_ASSISTANT_RUNTIME_CREDENTIAL_PROVISIONING.md)
and closed canonical preparation record bind separate fixed-path provision/validate
tools, root:jazofv1 0750 directories and 0640 single-link regular file, bounded
hidden TTY input, strict ASCII policy, effective group readers, Linux FD POSIX ACL
checks and atomic no-backup rotation. Repository-only synthetic tests establish
preparation; actual PI3 account/ACL/readability and installation remain unproved.
Operator Credential Installation, Independent Credential Validation and Credential
Provisioning Governance Closure are NOT STARTED. Adapter Implementation is NOT
STARTED. No credential, authentication, production execution, deployment or rollback
occurred. PE-4 NOT COMPLETE; Phase 7A ACTIVE. Next is the separately authorized
**PE-4 Home Assistant Runtime Credential Provisioning — Operator Installation**.

### PE-4 Home Assistant Association Adapter Implementation Preparation - 2026-10-06

Implementation Preparation PASS/CLOSED after resumed repository-only review using
both closed 0C and 0C.1, with future private-state schema 1.1. The
[prepared architecture](PE4_HOME_ASSISTANT_ASSOCIATION_ADAPTER_IMPLEMENTATION_PREPARATION.md)
freezes dedicated production module/entrypoint, accepted isolated runtime, canonical
read-only inventory, dedicated lock and recoverable hardened publication. Generic
integration ingestion remains prohibited. All four registry commands are mandatory;
INCOMPLETE means safely unresolved relationships within successful reads.
The sole recurring HA producer owns the complete six-capability ha_core map.

At implementation preparation, no compliant unattended HA credential mechanism
existed in the reviewed repository. At that preparation closure the next prerequisite was **PE-4 Home Assistant Runtime
Credential Provisioning**. Its repository preparation is now PASS/CLOSED; the parent
is PREPARED / NOT COMPLETE for root-managed private delivery outside Git/releases.
Adapter Implementation is NOT STARTED and must follow prerequisite closure. Public projection is separately
DEFERRED to **PE-4 Home Assistant Association Public Projection** after private
implementation and authorized production validation. No runtime source, deployment,
credential or production action occurred. PE-4 NOT COMPLETE; Phase 7A ACTIVE;
rollback NOT PERFORMED. Prior stopped review and original closures remain historical.

### PE-4.0C.1 Association Lifecycle Clarification - 2026-10-06

PE-4.0C.1 PASS/CLOSED, additive to unchanged closed 0C JSON and schema 1.0.
The prior implementation-preparation attempt correctly stopped with no changes
because successful-snapshot lifecycle semantics were incomplete. The
[lifecycle authority](PE4_HOME_ASSISTANT_ASSOCIATION_LIFECYCLE_CLARIFICATION.md)
now freezes current confirmed associations versus private retired binding history,
safe same-HIOC HA registry-ID recreation, bounded history without silent eviction,
and full last-known-good retention on failed cycles. Future state uses schema 1.1.
Preparation remains NOT STARTED; this checkpoint does not resume or close it.
The likely unattended credential-provisioning prerequisite and stronger writer/
locking design remain for resumed preparation. No runtime or production action.

### PE-4.0C Association Contract Freeze - 2026-10-06

PE-4.0C PASS/CLOSED after repository-only validation. Automatic association
requires one valid globally unique HA MAC mapping to one existing HIOC canonical
MAC-backed identity, with no invalid evidence, HIOC ambiguity or prior-binding
conflict. HA cannot create or mutate HIOC stable ID, MAC or canonical IP.
A dedicated post-identity association layer is required; generic integration
inventory ingestion is PROHIBITED. No liveness, health, incident or Asset authority
is granted. Snapshot evidence of 169 no-MAC devices, 8 invalid MAC entries and
9 colliding MAC values across 18 HA devices motivates fail-closed rules.
The [human authority](PE4_HOME_ASSISTANT_ASSOCIATION_CONTRACT.md) links the
canonical frozen contract and bounded future private-state schema. No household
values or production state are published. Compatibility Diagnostics UX and all
other future roadmap work remain separately governed.

The corrected 2b closure below is historical completed evidence; its then-next
0C NOT STARTED statements do not override the current PASS/CLOSED lifecycle.

### Corrected PE-4.0B.2b execution closure - 2026-10-06

**Current PE-4.0B.2b: PASS/CLOSED; PE-4.0C: NOT STARTED.**
This repository closure records operator-supplied completed production execution
and independent read-only review; Codex did not remotely inspect production.
Canonical authority: [execution closure](../governance/pe4/pe4-0b2b-execution-closure.json).
Original preparation completed, compatibility correction completed, corrected
preparation PASS/CLOSED, one separately authorized corrected live execution PASS,
and independent evidence review PASS. The initial synthetic probe failed because
its harness replaced shared `socket.socket`, preventing asyncio's local socketpair;
this was not a HIOC client or production failure. The corrected credential-free
synthetic retest PASSed without real network, credentials, evidence or state mutation.

Execution source was `063f3ab86c6f6c8c1ae649335856700dfeda6a22` on governed PI3
`nutandpihole`, operator `jazofv1`, execution IPv4 `192.168.100.252`, logical HA
instance `PI5_HA`. Source/governance/target/runtime prechecks, sanitized evidence
validation and source postcheck PASSed. Client and operator block return codes
were zero. The credential value was not persisted and is not repository evidence.

Observed HA Core **2026.9.4**, source-review baseline **2026.8.1**:
**COMPATIBLE_UPDATED**, failed capability **NONE**, no likely update compatibility
break. Required capabilities passed, and authoritative central compatibility state
agreed with the evidence. This demonstrates capability-first compatibility with
the observed 2026.9.4 interface and the mechanism for later versions; it does not
prove compatibility with every future HA release.

Sanitized aggregate counts: devices **229**, entities **2425**, areas **22**,
config entries **97**. Accepted PASS warnings: `CLASSIFICATION_NOT_DERIVED`
(unproven identity classes deliberately not inferred), `UNKNOWN_FIELDS`
(additive fields counted by type without publishing names/values), and
`UNPUBLISHED_NAMESPACES` (non-allowlisted namespaces counted without literals).
These warnings do not invalidate 2b or indicate a compatibility failure.

Private evidence reference: `/tmp/hioc-pe4-ha-discovery-7bb82b7c`.
Report SHA-256: `322e237404c3c721be782e9ce2dbc4ceb1e63b8374af00b6fe75a940624d2ded`.
Result SHA-256: `685606f76aad93ede32b52c2ffa34984408d62d408185ab6141791eded478e43`.
The operator's independent read-only review PASSed source/directory/hash/schema
binding, report schema, success semantics, structure fingerprint, result marker,
privacy scan, compatibility-state schema/HA binding and clean source postcheck.
Review used no credential or network and did not execute the discovery client.
Evidence is referenced only: not accessed, copied, recreated, mutated or deleted.

The first exact-version-gate FAIL remains immutable historical evidence; this
corrected PASS supersedes it as the authoritative current 2b outcome. D/E/F/G and
2a retain PASS/CLOSED, E handoff ACCEPTED, Compatibility Resilience audit and
Master Plan synchronization PASS/CLOSED. No 2a/F/G rerun occurred. PE-4 remains
NOT COMPLETE, Phase 7A ACTIVE, rollback NOT PERFORMED. Next checkpoint:
**PE-4.0C Association Contract Freeze**, separately governed and NOT STARTED.
No PI3/PI5/HA access, credentials, discovery execution, rerun, deployment,
rollback or PE-4.0C occurs during this repository closure.

### First PE-4.0B.2b Failed Execution Evidence

Preserved user-supplied historical interpretation: the first live 2b reached the
HA endpoint, received a valid WebSocket greeting and stopped because exact
Core-version equality had incorrectly been treated as compatibility. The
authentication frame was not sent; zero registry commands were sent; evidence
validation passed. Result FAIL, error UNSUPPORTED_HA_DEPLOYMENT, stage
HA_DEPLOYMENT_DISCOVERY; 2b remained NOT COMPLETE. 2a/F/G were not rerun and
rollback was not performed.

Evidence: `/tmp/hioc-pe4-ha-discovery-22be880b`.
Report SHA-256: `efd3aa0cc2f5bc00a459a0c05055ac14e5a9a7ab6cc13aeeb34aa9aa616cb087`.
Result SHA-256: `1e11b6e512db860a8f9b2b6af1723c6aabafd75968d7fd643c891144a7a72195`.
The evidence is referenced, not accessed or mutated here. Core `2026.8.1` remains
historical source-review baseline provenance, not required live runtime equality.

PE-4 Action E is **PASS / CLOSED** after exactly one production invocation under
consumer `1c1698f009457baa1c3b548db31916559fcc2fc8`, with immutable D producer
`6c431494c88688fef9a2fec7c7e81de0f503bdc2`. Retained E evidence is
`/tmp/hioc-pe4-dependency-validate-9ys_lrah`, SHA-256
`8d5ff1f602861d88ea8d363665a67091da2739686d10ab4aa9ac27f22389d834`.
Independent supervisor acceptance PASSed; construction, D handoff and source
remained unchanged. F and G are now **PASS/CLOSED**;
rollback **NOT PERFORMED**.
The production closure record above preserves the full prerequisite chronology.

PE-3 is complete and Actions 1–10 are complete. Action 10 completed
administratively with disposition `NOOP_ALREADY_ABSENT`; no PI3 or PI5 action,
staging recreation or deletion, production mutation, or Action 10 Evidence
Report was required. Action 8 evidence remains preserved at
`/tmp/hioc-pe3-action8-eZxNGrKa`. Action 9 completed read-only production
validation with private Evidence Report `/tmp/hioc-pe3-action9-Bb6vGrmm`, which
remains the final PE-3 production evidence. Rollback remained FALSE and was not
performed. Transport staging remains absent and retransmission is not required.

The Phase 7A.8 Recovery Validation Chain, repository governance reconstruction, reconciliation of the historical recovery documentation, Release Boundary Hardening, Changelog Governance Reconciliation, Repository Governance Reconciliation, Runtime Git Metadata Retirement, and the overall Repository and Deployment Hygiene checkpoint are complete. PI3 production migration, validation, supported upgrade proof, supported rollback proof, and quarantine removal are complete. ADR-0013 is resolved, and `/home/jazofv1/hioc` is formally non-Git. The former `61/62 commits behind` runtime condition is permanently resolved because the runtime is no longer a Git checkout and Git history belongs to the authoritative repositories. The approved lifecycle candidate remains intentionally reachable through `validation/phase-7a8-lifecycle`; completed merged topic branches and the temporary Windows SSH artifact have been retired. GitHub history is authoritative. Development checkouts, the authoritative source checkout for PI3 release execution, and the deployed production runtime have formally documented roles. The ADR-0014 Core MQTT correction, production deployment, and MQTT production Evidence Report are complete. Pi-hole DHCP Lease Ingestion implementation and production validation are complete with a documented warning. Canonical Address Selection Hardening is production validated and complete. The network-probe checksum-governance and PI5 endpoint-migration correction is complete: repository correction, governed deployment, Phase A, Phase B incident recovery, and overall production validation passed at approved commit `e06539d9bece040d721b9912213559cc54f1610d`. The July 29 DHCP pool-exhaustion incident is resolved, HIOC deployment validation passed, and the documentation architecture now assigns current-state, runtime, network, deployment, incident, and recovery authority to focused documents. DHCP Service Health & Capacity Monitoring and `.152` DHCP residue cleanup remain separate future work. Phase 7A remains active and Active Discovery remains postponed.

## Current Branch

main

## Current Commit

Tracked by Git history. Do not update this document solely to record documentation-only commit hashes.

## Current Phase

Phase 7A - Passive Living Inventory

## Phase Progress

| Phase | Status |
|--------|--------|
| Platform Foundation | ✅ Complete |
| MQTT Publishing | ✅ Complete |
| Dashboard v2 | ✅ Complete |
| Incident Engine | ✅ Complete |
| Correlation Engine | ✅ Complete |
| History Engine | ✅ Complete |
| Incident Review | ✅ Complete |
| Dashboard Usability Improvements | ✅ Complete |
| Initial Living Inventory | ✅ Complete |
| Phase 7A - Passive Living Inventory | 🚧 In Progress |
| Phase 7B - Safe Active Discovery | ⏳ Planned |
| DHCP Service Health & Capacity Monitoring | ⏳ Planned |

## Current Objective

**PE-4 Home Assistant Runtime Credential Provisioning** remains the current
separately governed objective. Implementation Preparation and Credential Provisioning
Preparation are PASS/CLOSED. The parent is PREPARED / NOT COMPLETE. Operator
Installation, Independent Validation, Governance Closure, adapter implementation
and deployment remain NOT STARTED. Both PE-4.0C and PE-4.0C.1 remain PASS/CLOSED.
Phase 7A ACTIVE; PE-4 NOT COMPLETE; rollback NOT PERFORMED.

## Next Planned Task

### PE-4 Home Assistant Runtime Credential Provisioning — Operator Installation

Separately authorize the human operator's local hidden-TTY installation on PI3
NUT&PIHOLE using the exact pushed preparation commit and both tool source identities
from the [provisioning preparation](PE4_HOME_ASSISTANT_RUNTIME_CREDENTIAL_PROVISIONING.md).
Stop after installation. Independent root metadata and actual jazofv1 readability
validation follow as a separately authorized action; governance closure follows
accepted evidence. The parent must close before Adapter Implementation. This
repository preparation neither provisions a credential nor authorizes deployment.
Public projection remains a later named checkpoint.

### Future Compatibility Diagnostics UX Checkpoint

**Compatibility Diagnostics UX** remains named future visible-product work.
It consumes the central status architecture and integrates with the existing
phone-notification semantics roadmap; it does not replace or reorder other work.

PE-5 through PE-10, DHCP Service Health & Capacity Monitoring, expected-
availability monitoring, configurable stale-client retention/archive, the
asset-centric living digital twin, improved dependency graph, automatic service
relationships, failure propagation visualization, infrastructure topology,
historical trends, predictive recommendations, infrastructure backup/disaster
recovery/hardware migration, incident-history validator hardening, existing
Phase 7A and later checkpoints all remain preserved and separately governed.

# Historical Operator Preparation Chronology

The following superseded status/objective/next-task statements and operator
preparation records are historical only; they do not govern the current sequence.

## Historical Successor Status Before PE-4.0B.2a Closure

Replacement B PASS/CLOSED; C PASS; D-PREP PASS/CLOSED.
D PASS/CLOSED; E PASS/CLOSED; Action E handoff ACCEPTED; F PASS/CLOSED;
G PASS/CLOSED after one production execution and independent review PASS.
Native compatibility PASS/CLOSED; rollback NOT PERFORMED. PE-4 NOT COMPLETE.
The current Action G closure and repository successor correction above are
authoritative. Successor source is corrected, REPOSITORY_ONLY / NOT DEPLOYED,
not executed and not yet authorized; 2a is not prepared and remains NOT STARTED.
The authentication send deadline correction supersedes the earlier candidate.
Next: repeat separate successor preparation review for PE-4.0B.2a under
REST_THEN_WEBSOCKET_2A; no automatic 2b registry/schema discovery.
The accepted E historical bridge retains NO_PERSISTED_E_TIME_RECURSIVE_BASELINE
and both historical recursive flags remain false.

At that checkpoint, this section reflected the then-current project state.

It is retained here as historical chronology.

## Historical Manufacturer Objective

Maintain Phase 7A after completing and production-validating PE-1 and PE-2.1,
defining PE-3.0 architecture, freezing the PE-3.1 executable contract, and
correcting its manufacturer lock order so all mutable generator inputs are read
and validated under the dedicated manufacturer lock. The frozen error model now
also has explicit, non-overlapping causes for dataset conflict, deterministic-
build mismatch, sidecar validation, and status validation without changing any
other exit/error semantics. The standalone validator is now explicitly lock-free
and read-only: immutable database safety comes from atomic directory publication,
while the builder and generator remain the only owners of the two exclusive
manufacturer locks.
PE-3.1 executable implementation is repository validated. A production-intended
dataset has been built and validated only in the external operator workspace;
no PE-3 dataset is deployed and no production runtime behavior exists. Phase 7A
is not complete.

The bounded real-source correction removes only U+200B/U+200E from organization
labels, collapses TAB as whitespace, and preserves official multi-organization
assignment keys as explicit non-selectable conflicts. Conflicted keys block
weaker-prefix fallback and cannot produce manufacturer claims. No source row or
organization variant enters Git.

## Historical PE-3-to-PE-4 Next Task

PE-3 is **COMPLETE** with Actions 1–10 complete. The next ordered passive-
enrichment checkpoint is **PE-4 - Home Assistant Association**, already planned
and not started. Before implementation, its separately governed access/schema
approval must authorize the read-only Home Assistant registry adapter and its
association authority. This completion record does not begin that checkpoint.
Phase 7A remains the active parent phase; PE-3 closure does not complete or
replace it. PE-5 through PE-10 and all other future-roadmap commitments remain
planned and separate.

Action 1 pre-execution review identified two operator-input defects without
executing the action: a hard-coded `python` PATH assumption and ambiguous choice
between two already-proven deterministic build directories. The corrected
historical runbook correction resolved Python 3 in the order `py -3`, `python3`, `python`
and discovers an adjacent database/manifest pair only when both frozen hashes
and sizes match. This correction performs no artifact validation run, transfer,
production access, deployment, configuration change, or sidecar generation.

The first operator attempt exposed a runbook-only control-flow defect: expected
`exit 20` branches closed the interactive PowerShell host before evidence could
be returned. Action 1 is now one function-scoped copy/paste block. Every expected
failure reports a sanitized result/code and returns; unexpected exceptions map
to `ACTION1_UNEXPECTED_ERROR`. No `exit` remains, so the operator prompt survives.
The attempted action produced no accepted evidence and did not start transfer or
production work.

Two operator attempts are classified as Action 1 delivery-path defects, not
Python, manufacturer-validator, dataset, repository, or production failures.
The first delivered block lost literal Windows syntax; the second escaped
underscores and changed `$env:HIOC_HOME` before PowerShell parsed it. Neither
attempt produced valid Action 1 evidence or reached PI3 or production.

Action 1 is now executed only from the repository-controlled Windows PowerShell
script `tools/hioc-pe3-action1.ps1`. The runbook remains the procedural
authority, freezes the script SHA-256 and Git blob identity, and publishes only
the direct parameterized invocation. The script verifies its own approved Git
identity before artifact validation and preserves every previously frozen
read-only, containment, hash, size, ancestry, resolver, validator, sanitization,
and stop boundary. Script source must not be distributed through chat.

Repository-controlled execution then eliminated delivery transport as a
variable and produced the first genuine prerequisite result:
`FAILURE_STAGE=PYTHON_RESOLUTION`. Read-only diagnostics established that `py`
was absent, `python3` and `python` were only nonfunctional WindowsApps aliases
returning 9009, and no real installation existed in bounded normal locations.
This is **ACTION1_PREREQUISITE_MISSING — PYTHON3**, not a manufacturer,
dataset, repository, or production failure.

The resulting repository-wide audit froze CPython 3.10 as the language floor,
recorded CPython 3.12.13 as the sole exact full-suite-tested runtime, proposed
CPython 3.13.x for Windows with validation pending, and left the exact
distribution-managed production Python version unverified. Action 1 now prefers
`py -3.13`, rejects other implementations/minor lines, distinguishes absent and
incompatible runtimes, and requires an approved support-state promotion before
Python or artifact validation can proceed.

The official Python Install Manager is now present. The first governed
installation checkpoint stopped at `PYTHON_INSTALLATION` because Windows
PowerShell 5.1 treated informational native stderr as an exception under the
script's stop-on-error policy. A later informal `py --help` diagnostic triggered
automatic default-runtime installation and left CPython 3.14.7 installed. This
is `PYTHON_OPERATOR_DIAGNOSTIC_SIDE_EFFECT —
UNINTENDED_DEFAULT_RUNTIME_INSTALL`, not HIOC support, PE-3 evidence, or
production state. It remains installed pending a separate cleanup decision.
The official manager's safe dry run resolved CPython 3.13.15 as the current
candidate, but accepted evidence does not establish the current 3.13
installation or validation result, and support remains `validation_pending`.

The next retry must not infer a patch from the completed install stage. It must
use the hardened manager inventory and wrapped `py -3.13` probe, then complete
the full wrapped validation matrix. PE-3 Action 1 remains blocked throughout.

The hardened retry successfully passed repository, script, support, manager,
managed-runtime selection, and CPython 3.13 execution checks before stopping at
`FULL_REGRESSION`. A direct verbose run executed 504 tests and isolated all
three errors to Bash-dependent network-probe governance tests raising Windows
`FileNotFoundError` / `WinError 2` for an unavailable shell. This is
**CROSS-PLATFORM TEST PREREQUISITE CONTRACT DEFECT — MISSING BASH REPORTED AS
ERROR**, not Python 3.13 incompatibility. The three Bash-only tests now skip
explicitly when Bash is unavailable; three platform-neutral checks continue to
run, and all six original assertions run when Bash exists. Support remains
`validation_pending`; Action 1, deployment, PI3 validation, and PE-4 remain not
started.

A subsequent governed retry again reported `FULL_REGRESSION_FAILED`. Immediate
direct execution on the same Windows workstation, repository, and governed
CPython 3.13 runtime ran 506 tests in 14.889 seconds, returned
`OK (skipped=13)`, and exited 0. Forensic review established **CHECKPOINT
FULL-REGRESSION RESULT-CLASSIFICATION DEFECT — NON-AUTHORITATIVE SUMMARY PARSE
USED AS ACCEPTANCE GATE**: the checkpoint had the correct native exit result
but additionally rejected a missing parsed `Ran` count, while head-only bounded
capture could omit unittest's trailing summary. The corrected checkpoint uses
native exit status as the sole test-stage acceptance criterion, retains output
tails for sanitized count reporting, and never makes test or skip totals gates.
Support remains `validation_pending` with `validated_patch: null`; Action 1,
deployment, PI3 validation, and PE-4 remain not started.

That result-classification correction did not resolve the real operator result:
the governed checkpoint again returned `FULL_REGRESSION_FAILED`, while direct
CPython 3.13 runs passed 508 tests with 13 skips and exit code 0 both normally
and under the checkpoint's temporary `PYTHONPYCACHEPREFIX`. The remaining
behavioral difference is the Windows PowerShell 5.1 `ProcessStartInfo` wrapper.
Because the Codex repository process cannot resolve the operator's `py`
launcher, the exact same-launcher mechanism remains unproven. A checked-in,
sanitized direct-versus-wrapper diagnostic is prepared for one separately
authorized operator execution after push. Support stays `validation_pending`
with `validated_patch: null`; no PE-3 or production action has started.

The synchronized diagnostic completed successfully but reported execution
equivalence failure. Direct `py -3.13` regression exited 0 with a valid
516-test/13-skip summary; `ProcessStartInfo` launching the resolved `py` App
Execution Alias exited 1 after both stream tasks completed and produced no
unittest summary. This is a Windows runtime-launch layer defect, not Python
compatibility evidence. The checkpoint now resolves the exact manager-owned
3.13 interpreter via machine-oriented `pymanager list --format=exe` output and
invokes it directly, bypassing App Execution Aliases and excluding 3.14.7.
Support remains pending; no PE-3 or production action has started.

Final operator isolation resolved the remaining ambiguity. The exact managed
interpreter path was valid and passed directly; it also passed 518 tests with
13 skips and exit code 0 under the checkpoint's pycache environment. It failed
only when Python was executed via `ProcessStartInfo`. The final checkpoint
architecture retains exact manager-owned 3.13 selection but runs every Python
stage through scoped PowerShell-native invocation with immediate exit capture,
bounded temporary-file streams, and cleanup. Support remains pending and no
PE-3 or production action has started.

The corrected governed checkpoint then returned PASS on CPython 3.13.15 at
commit `6b622280a6f414d14ca3060da349423d92d664cb`: full regression 520 tests with
13 skips, policy tests 10, Action 1 tests 13, manufacturer tests 119, compilation
PASS, and clean repository. Windows CPython 3.13.x is now supported for the
operator workstation, with 3.13.15 recorded as validated patch evidence. PE-3
Action 1 is ready to resume under separate authorization but was not executed in
this checkpoint. PE-3 deployment and PI3 validation remain not started.

The first PI3 Action 3 attempt established target identity and complete staging
identity: private owner/mode, exact two regular non-symlink files, frozen byte
sizes, and frozen SHA-256 values all passed. The subsequent implementation
history check failed because the clean `main` release-source checkout did not
yet contain implementation commit `157ae644dcedcbec7c69cb0d8b054e104335e024`.
This is **PE-3 ACTION 3 / ACTION 4 REPOSITORY-SEQUENCING CONTRADICTION**, not a
dataset, repository-corruption, manufacturer, or production failure. The
historical interactive block also closed the operator shell through unbounded
`set -euo pipefail`; staging remained intact and was recovered read-only.

The corrected immediate sequence is frozen: Action 3 is staging-only; Action 4
first performs the governed clean fast-forward, then proves implementation and
validator identity, revalidates the staged pair at point of use, and runs the
read-only validator; Action 5 remains the first deployment action. Operator
verification functions return sanitized failure evidence without terminating
the shell. Accepted staging evidence is preserved, so the exact restart point
is preparation of corrected Action 4 after this correction is approved and
pushed. No Action 3 rerun is required unless staging changes.

Corrected Action 4 synchronized PI3 release source and passed implementation
identity and staged size/hash checks, then the approved validator returned
`MANUFACTURER_PERMISSION_ERROR` because both staged files were mode `0644`.
This is **PE-3 STAGED ARTIFACT PERMISSION CONTRACT DEFECT**, not dataset
corruption, transfer-integrity failure, validator defect, or production failure.
The shell-safe failure contract worked and returned control to the operator.

The executable contract requires database and manifest mode `0600` (and
sidecar/status `0600`; version directories `0700`). Model C is adopted: Action 4
owns bounded permission normalization after exact directory contents, regular
non-symlink type, owner, sizes, and hashes are proven. Only the exact two files
at `0600` or observed `0644` may be normalized to `0600`; modes and hashes are
then revalidated before validator retry. Existing staging and completed source
synchronization are preserved. The restart point is Action 4
`STAGING_PERMISSION_NORMALIZATION` after this correction is pushed and PI3
source is synchronized to it. Action 5 remains not started.

The resume contract gap is corrected in a repository-controlled Bash script.
The script rechecks all staging invariants after normalization and requires the
validator's PASS, privacy-safe, and 53,581-record fields explicitly. Separate
source, staging, permission, post-normalization, validator, and Action 4 PASS
barriers are mandatory. This repository correction does not execute the resume;
Action 4 remains stopped at `STAGING_PERMISSION_NORMALIZATION`, existing staging
evidence is preserved, and Action 5 remains not started.

The first script invocation found PI3 release source still at
`653f887a643c877a8f611145c8b8e9f92a65b6cd`; the later resume script was absent.
This is **PE-3 ACTION 4 RESUME SCRIPT AVAILABILITY DEFECT — TARGET
RELEASE-SOURCE STALE AFTER GOVERNANCE UPDATE**, not an operator, script,
staging, dataset, manufacturer, or production failure. The corrected restart
point is bounded target-source synchronization, script identity verification,
then the existing permission-normalization resume in the same Action 4. Staging
remains preserved and Action 5 remains not started.

The execution-boundary correction splits the restart into Action 4A (target
repository synchronization and resume-script identity) and Action 4B (bounded
staging permission normalization and manufacturer validation). Action 4A must
PASS and stop; Action 4B requires separate authorization. `ACTION4=COMPLETE`
belongs only to Action 4B after reviewed Action 4A PASS. Action 5 remains the
first deployment action and is not started.

**PE-3 Action 5 governance correction (2026-08-12):** Actions 1 through 4 are
complete; Action 5 and Action 6 remain not started. Pre-execution review found
that the old Action 5 operator block used interactive `set -euo pipefail`, a
`tee` pipeline, bare assertions, an unresolved commit placeholder, and no
bounded result/error/stage contract. This is an operator-safety contract defect,
not a deployment failure. Action 5 is now owned by the repository-controlled
`tools/hioc-pe3-action5-deploy.sh`, with exact governance/self identity,
pre-mutation release validation, supported upgrade and backup proof, runtime
artifact verification, unchanged dataset/configuration evidence, explicit PASS
barriers, and stage-aware rollback recommendation. It never chains Action 6.

**PE-3 Action 5 bootstrap correction (2026-08-12):** PI3 was last proven at the
prior Action 4 governance commit, which predates the Action 5 deployment script.
This is **PE-3 ACTION 5 BOOTSTRAP PREREQUISITE DEFECT — TARGET RELEASE-SOURCE
MAY PREDATE DEPLOYMENT SCRIPT**, not a deployment, staging, manufacturer, or
operator failure. Action 5A now owns only bootstrap-safe target synchronization
and exact deployment-script identity, then stops. Separately authorized Action
5B remains the first production deployment mutation. Neither has been executed;
Action 6 remains not started.

**PE-3 Action 5 protection correction (2026-08-12):** Action 5A passed. Action
5B deployed and validated supported runtime code, then falsely classified
installer-created empty private manufacturer scaffolding as a dataset change.
Read-only PI3 evidence proved there was no version, database, manifest, sidecar,
status artifact, or configuration activation. The condition is **ACTION 5
PROTECTION SNAPSHOT FALSE POSITIVE — RELEASE-MANAGED EMPTY MANUFACTURER
SCAFFOLDING**; rollback is not recommended. Action 5 protection now compares
payload and configuration semantics while permitting only empty owned `0700`
scaffolding creation/normalization. Action 5 remains incomplete pending a new,
separately bootstrapped, read-only Action 5C revalidation; Action 6 is not
started.

**PE-3 Action 5C bootstrap-contract correction (2026-08-12):** The target may
predate the new Action 5C script. This is **PE-3 ACTION 5C BOOTSTRAP CONTRACT
MISSING — TARGET MAY PREDATE REVALIDATION SCRIPT**, a governance/runbook
deficiency rather than a production failure. Action 5C-A now owns only inline,
bootstrap-safe clean fast-forward synchronization and exact Action 5C script
Git/worktree identity, then stops. Action 5C-B remains a separately authorized,
read-only closure of the already-deployed runtime. Neither action has been
executed; Action 5 remains incomplete, rollback is not recommended, and Action
6 is not started.

**PE-3 Action 6 operator-safety correction (2026-08-12):** Action 5 is complete
after reviewed Action 5C-B PASS; Action 6 and Action 7 are not started. The old
Action 6 inline block is classified as **PE-3 ACTION 6 OPERATOR-SAFETY AND
EVIDENCE CONTRACT DEFECT — IMMUTABLE DATASET INSTALLATION PROCEDURE NOT
PRODUCTION-SAFE**. It used an unresolved staging placeholder, interactive
strict mode/exit, bare assertions, and incomplete evidence. The corrected
architecture splits bootstrap-safe Action 6-A synchronization/script identity
from separately authorized repository-controlled Action 6-B. Action 6-B
installs only the validated immutable pair by same-filesystem no-replace atomic
publication, accepts only an exactly identical existing version, fails closed
on any conflict, preserves configuration, and cannot chain Action 7. No Action
6 production mutation occurred.

**PE-3 Action 7 operator-safety correction (2026-08-22):** Action 6-A and
Action 6-B passed; Action 6 is complete and Action 7 remains not started. The
historical Action 7 inline block is classified as **PE-3 ACTION 7
OPERATOR-SAFETY AND EVIDENCE CONTRACT DEFECT — CONFIGURATION ACTIVATION
PROCEDURE NOT PRODUCTION-SAFE** because it used interactive strict mode and
exits, an unresolved evidence path, and incomplete identity, backup,
post-publication, and rollback evidence. The corrected architecture splits
bootstrap-safe Action 7-A synchronization/script identity from separately
authorized repository-controlled Action 7-B. Action 7-B changes only the
`MANUFACTURER_DB_PATH` selection after exact immutable dataset validation,
preserves all unrelated configuration and staging, performs no reload or
sidecar generation, and cannot chain Action 8. No Action 7 or production action
occurred; no rollback is recommended and the current deployed runtime remains
in place.

**PE-3 Action 8 operator-safety correction (2026-08-22):** Action 7-A and
Action 7-B passed; Action 7 is complete and Action 8 remains not started. The
historical Action 8 inline block is classified as **PE-3 ACTION 8
OPERATOR-SAFETY AND EVIDENCE CONTRACT DEFECT — MANUFACTURER GENERATION
PROCEDURE NOT PRODUCTION-SAFE** because it used interactive strict mode, a
pipefail-sensitive `tee` pipeline, an unresolved evidence path, bare assertions,
and incomplete identity, protected-state, publication, failure, and rollback
evidence. The corrected repository-controlled Action 8 transaction verifies the
activated configuration, exact immutable dataset, current inventory, output
preconditions, protected state, transport staging, generated sidecar/status, and
private aggregate evidence. It performs no deployment, service activation,
staging cleanup, or Action 9 chaining. Because the published PI3 source predates
the new script, a separately reviewed future bootstrap gate is required after
commit/push and is not prepared here. No Action 8 or production action occurred.

**PE-3 Action 8 bootstrap governance (2026-08-22):** The required bootstrap is
now governed as a separately authorized, inline, parent-shell-safe synchronization
and script-identity gate. It accepts the exact operator-approved full 40-hex
post-push governance commit, validates it before network or mutation, may only
fast-forward the clean PI3 release-source checkout to that exact commit, and
proves Git/worktree identity
for `tools/hioc-pe3-action8-generate.sh` at blob
`91360c1f83c890dd340a9a6390bf462cb0f95731`, then stop. It does not read or
change runtime configuration, dataset, inventory, sidecar/status, evidence, or
transport staging and cannot invoke Action 8 or Action 9. The bootstrap is
prepared but not executed; Action 8 remains not started.

**PE-3 Action 8 bootstrap governance-commit correction (2026-08-22):** The
first bootstrap checkpoint incorrectly froze its pre-correction parent commit,
creating a self-stale contract after publication. This is classified as **PE-3
ACTION 8 BOOTSTRAP GOVERNANCE-COMMIT SELF-STALE CONTRACT DEFECT**. The corrected
gate takes the explicitly approved literal full 40-hex post-push commit as its
sole argument, rejects invalid or symbolic input before target/network work, and
still requires exact `origin/main`, ancestry, fast-forward, post-sync HEAD, clean
tree, and frozen script Git/worktree identity. No bootstrap or production action
occurred; Action 8 remains not started.

**PE-3 Action 8 evidence-directory correction (2026-08-22):** The wrapper's
operator-supplied `/tmp/hioc-pe3-production-validation-*` destination had no
Action 5/5C provenance marker, durable discriminator, or safe recovery contract.
This is classified as **PE-3 ACTION 8 EVIDENCE-DIRECTORY PROVENANCE AND
DURABILITY CONTRACT DEFECT — EPHEMERAL PATH IS NOT DURABLY IDENTIFIABLE**.
Action 8 needs no historical Action 5 evidence. The corrected wrapper accepts
only the governance commit and, after all read-only preconditions pass, creates
one unique private invocation-owned `/tmp/hioc-pe3-action8-XXXXXXXX` directory,
publishes aggregate evidence result-last, and reports its exact path. Loss of
that temporary evidence blocks later authorization; it is never reconstructed.
Because the script identity changes, the reviewed bootstrap PASS for the prior
blob remains historical and a new bootstrap is required after commit/push. No
replacement bootstrap, Action 8, Action 9, or production action occurred.

**PE-3 Action 8 transport-staging lifetime correction (2026-08-22):** The first
post-bootstrap Action 8 attempt passed target, source, runtime, configuration,
installed dataset, dataset validation, and inventory, then stopped before
generation with `TRANSPORT_STAGING_INVALID` because the historical `/tmp`
transfer directory was absent. Repository review confirms Action 8 consumes no
staging bytes: Action 6 already validated and atomically published the immutable
pair, and Action 7 selected that installed database. The former requirement is
classified as **PE-3 ACTION 8 TRANSPORT-STAGING LIFETIME CONTRACT DEFECT —
EPHEMERAL TRANSFER STATE INCORRECTLY REQUIRED AFTER IMMUTABLE INSTALLATION**.
Action 8 now accepts absent staging while retaining exact active-configuration,
installed-dataset, validator, privacy, and protected-state barriers. It does not
recreate, retransmit, or clean staging. The attempt caused no generation
mutation; Action 8 remains incomplete, Action 9 remains not started, and rollback
is not recommended. The changed script requires a new post-push bootstrap gate.

**PE-3 Action 8 generator-failure diagnostic-retention correction
(2026-08-22):** The separately authorized Action 8 attempt reached
`PROTECTED_PRE_STATE=PASS` and stopped on a nonzero generator exit. Its private
evidence directory `/tmp/hioc-pe3-action8-gbLOVQJW` was preserved. Reviewed
read-only forensics found exactly `pre/protected.json`, no status file, and no
temporary, performance, success-result, or failure-result evidence. The
underlying generator error cannot be recovered. This is classified as **PE-3
ACTION 8 GENERATOR FAILURE DIAGNOSTIC RETENTION DEFECT — WRAPPER COLLAPSES
GENERATOR FAILURE WITHOUT DURABLE SANITIZED ROOT-CAUSE EVIDENCE**.

The corrected wrapper retains only private bounded failure evidence: performance
is published before result-last `generation-failure.json`; the document records
the numeric exit status, allowlisted generator code when available, structured
result and stderr-presence booleans, safe sidecar/status change summaries,
temporary-artifact presence, mutation class, and rollback recommendation. Raw
stdout/stderr are never published and are removed. Safe status-only failure
updates remain non-rollback; sidecar mutation, unsafe output state, leftover
temporaries, or evidence/cleanup uncertainty requires manual rollback review.
No rollback is automatic. Action 8 remains **NOT COMPLETE**, Action 9 remains
**NOT STARTED**, transport staging remains irrelevant, and a new post-push
bootstrap is required for the changed wrapper. PE-10 remains **PLANNED / NOT
STARTED — FUTURE ARCHITECTURE**; the PI3 + PI5 Abrupt Power-Loss / Cold-Boot
Recovery Validation checkpoint and all other future roadmap commitments remain
preserved.

**PE-3 Action 8 bootstrap script-identity correction (2026-08-22):**
Replacement-bootstrap preparation stopped before PI3 execution because the
active governed trust gate still froze superseded wrapper blob
`91360c1f83c890dd340a9a6390bf462cb0f95731`. This is classified as **PE-3
ACTION 8 BOOTSTRAP SCRIPT-IDENTITY GOVERNANCE DEFECT — GOVERNED TRUST GATE
REFERENCES SUPERSEDED WRAPPER BLOB**. The active bootstrap now independently
freezes the reviewed diagnostic-retention wrapper blob
`482f83584a62be2f02b2a73af4e78b0f4ebf447a`; the operator-supplied governance
commit, exact Git-object/worktree checks, and source-only fast-forward boundary
remain unchanged. No bootstrap was prepared or executed, no PI3 or production
action occurred, and no retransmission or transport staging is required.
Action 8 remains **ATTEMPTED BUT NOT COMPLETE**, Action 9 remains **NOT
STARTED**, and the historical failed-attempt rollback remains **NOT
RECOMMENDED**. A separate post-push preparation checkpoint is still required.
PE-10 and the PI3 + PI5 abrupt power-loss/cold-boot checkpoint remain preserved.

**PE-3 Action 8 performance-instrumentation portability correction
(2026-08-22):** The second governed attempt passed all source, runtime,
configuration, dataset, inventory, output, evidence, and protected-pre-state
checks, then retained sanitized exit `127` evidence in
`/tmp/hioc-pe3-action8-hGuyFmbK`. PI3 lacked the wrapper's undeclared hard-coded
`/usr/bin/time`; no manufacturer output changed, rollback was not recommended,
and the governed generator was not proven to have executed. This is **PE-3
ACTION 8 PERFORMANCE-INSTRUMENTATION PORTABILITY DEFECT — OPTIONAL
/usr/bin/time DEPENDENCY BLOCKS GOVERNED MANUFACTURER GENERATION**.

The wrapper now measures the child with governed Python monotonic timing and
child resource usage, records launch as confirmed only after successful child
creation, and distinguishes invocation failure from generator failure. Private
performance and result-last evidence ordering remain mandatory. Action 8 is
**ATTEMPTED BUT NOT COMPLETE**, Action 9 is **NOT STARTED**, and the current
bootstrap PASS becomes historical/stale because the wrapper changed. A new
post-push bootstrap is required. Transport staging remains absent and unrelated;
PE-10 and every preserved future checkpoint remain unchanged.

Do not begin Active Discovery until Phase 7A has been completed.

---

# Decision Log

## 2026-07

Architectural decisions currently in effect:

- Dashboard v2 is the primary operator interface.
- Passive Living Inventory must be completed before Active Discovery.
- HIOC favors operator explanations over raw metrics.
- Historical incident review is a first-class feature.
- Incident testing will occur during real operational events rather than synthetic simulations.
- New features must not interrupt the current implementation phase.
- Scope changes require an intentional revision of this master plan.

---

# Maintaining This Document

This document should evolve deliberately.

Routine implementation work should update only:

- Current Phase
- Phase Progress
- Current Objective
- Next Planned Task

Changes to the project's philosophy, architecture, or roadmap should be made intentionally and reflected in the Decision Log.


## Phase 7A Network Probe Source Governance and MQTT Health Hardening

Status: **COMPLETE — REPOSITORY, DEPLOYMENT, AND PRODUCTION VALIDATION PASS**.

This bounded corrective checkpoint responds to the July 29, 2026 PI5 address change from `192.168.100.152` to `192.168.100.251`. The operator corrected `HOME_ASSISTANT_IP`, `MQTT_HOST`, and the webhook endpoint in PI3 `toolkit.conf`, and host and service-port checks passed. The network probe nevertheless retained two old executable literals, so MQTT publication and PI5 probing used competing endpoint sources.

The production probe was absent from every Git repository. The first implementation attempt stopped because rebuilding production behavior from fragments was unsafe. The operator captured the complete script and evidence. The intake archive SHA-256 `74e7e251bd0848a0b87d2f314fd2d0958bd5c9730a8b6ff37fff449c1052bf6d` and script SHA-256 `edf6ad456292a0fb9441f09e7eb59fa02831cee46aa7071dcaa7b8d3eadc39a1` were verified before import.

The authoritative source is now `pi4-tools/scripts/hioc-network-probe.sh`; the production path remains `/home/jazofv1/pi4-tools/scripts/hioc-network-probe.sh`. The probe derives PI5 reachability and inventory addressing only from required `HOME_ASSISTANT_IP`. `toolkit.conf` remains runtime configuration and is not committed. `pi4-tools/deploy-network-probe.sh` validates syntax, creates a timestamped backup, installs atomically with owner/group `jazofv1` and mode `0755`, and verifies source/deployed hashes without touching configuration, logs, state, or prior backups.

Dashboard V2 now separates MQTT Operational Health from MQTT Forecast Trend. Operational health uses the parseable last-success timestamp with a 12-minute freshness threshold and two-minute future-clock tolerance. Unavailable, unknown, empty, invalid, stale, or implausibly future data cannot be green. The cumulative failure counter remains historical evidence and is not reset or treated as permanent current degradation. Forecast rising is Watch; stable or falling is Favorable and cannot override operational health.

### Infrastructure-change governance

Any IP address, hostname, DNS name, broker, Home Assistant endpoint, webhook, service port, or comparable dependency change requires repository and production impact review. Review active configuration, executable scripts, cron/timers, systemd, publishers/subscribers, Home Assistant integrations, dashboards, inventory, incidents, health models, deployment, backup/restore, tests, runbooks, and evidence classification where applicable. Historical evidence is not rewritten. Current documentation reflects current infrastructure. Executable code uses an authoritative configuration value instead of duplicated literals whenever one exists.

Validation order is: configuration values; host reachability; service-port reachability; controlled publisher execution; subscriber receipt; last-success advancement; failure-counter behavior; freshness; dashboard operational health; forecast separation; inventory address; incident behavior; runtime checksum; repository cleanliness.

### Future complete pi4-tools source-governance checkpoint

Only `hioc-network-probe.sh` was captured. A future checkpoint must perform complete checksum-verified intake of all active scripts, secret-free configuration templates, cron ownership, state/log/generated/backup boundaries, deployment and restore procedures, tests, documentation, and production checksum validation. No uncaptured script is fabricated or claimed as governed here.

### Evidence Report

Repository evidence is recorded in [NETWORK_PROBE_GOVERNANCE_EVIDENCE.md](NETWORK_PROBE_GOVERNANCE_EVIDENCE.md). At that repository-only stage, implementation could pass independently while the overall checkpoint remained open until controlled deployment evidence was returned and documented.

Closure: operator evidence for approved commit
`e06539d9bece040d721b9912213559cc54f1610d` records matching Git blob,
worktree, and deployed checksums, successful PI5/MQTT/inventory validation, and
cleared false incident. The historical pending condition is satisfied.

## Phase 7A Corrective Checksum-Governance Checkpoint

Status: **COMPLETE — CORRECTION, PHASE A, PHASE B, AND PRODUCTION PASS**.

The first PI3 deployment attempt stopped safely before deployment because the
operator command contained an incorrect manually transcribed checksum. The
value is proven to be the SHA-256 of the CRLF Windows checkout, while the
approved commit stores an LF blob. This is a governance defect, not a PI3
synchronization, checkout, branch, or production-file failure.

The corrective checkpoint establishes raw Git objects at an exact approved
commit as the sole artifact-byte authority. It adds deterministic
commit/path/blob/SHA-256 reporting, prevents manually supplied hashes from
overriding Git identity, binds the network-probe deployment helper to a clean
exact commit, and proves blob/source/deployed byte identity in isolated tests.
The dynamic-manifest design avoids a tracked self-referential checksum.

All deployment evidence is regenerated only after the final corrective commit
is pushed and `HEAD` equals `origin/main`. No checksum calculated before that
point can enter operator instructions. Repository correction does not complete
the PI3 deployment; controlled PI5 connectivity, probe, MQTT, inventory, and
production artifact validation remain pending. Active Discovery and normal
roadmap work remain paused for this correction.

The final refinement separates deterministic governed deployment from
downstream incident recovery. Phase A failure remains fail-closed. Delayed or
inconclusive Phase B convergence produces **PARTIAL PASS**, exits successfully,
and requires separate follow-up without rollback based solely on observation.
Full **PASS** requires both domains; **FAIL** is reserved for deterministic
deployment failure. The checksum-origin and Endpoint Migration Audit findings
remain unchanged. Before operator execution, production stayed open pending
evidence review.

Closure evidence records Phase A **PASS**, Phase B **PASS**, and overall
production validation **PASS**. Seven reads succeeded with no failures or
malformed payloads, false PI5 evidence was absent, the backup was created, and
no rollback occurred or was required. This closes only this corrective
checkpoint. Phase 7A remains in progress; Canonical Address Selection
Hardening remains next.
# PE-4.0B.2a isolated runtime dependency governance

Status: **READY FOR GOVERNANCE COMMIT REVIEW — NOT DEPLOYED / NOT EXECUTED**.

PI3 CPython 3.11.2 satisfies the existing HIOC CPython policy; no Python
version change is required. CASE A freezes `websockets==16.1.1` to the exact
official CPython 3.11 AArch64 wheel and SHA-256, with no transitive dependencies,
and defines a versioned release-managed virtual environment with an atomic
active pointer. The independent route proof remains credential-free and should
precede dependency deployment. Runtime preflight remains attempted but not
complete and must be rerun through the future absolute isolated interpreter.
PE-4.0B.2a, PE-4.0B.2b, and PE-4.0C remain **NOT STARTED**.

Repository-controlled lifecycle tooling now implements the separately gated
PE-4.0B.2a-A through G sequence plus rollback. Route proof remains ordered
before dependency deployment. This repository checkpoint does not acquire or
transfer the artifact, contact PI3/PI5, construct an environment, deploy the
client, run preflight, or authorize production. Each action still requires its
own post-publication preparation, authorization, Evidence Report, and STOP.

Action A preparation subsequently found a Windows contract defect: evidence
used `/tmp` and POSIX modes/directory fsync, cache ancestors lacked reparse-point
validation, network timeout was not a total deadline, and argparse bypassed the
bounded terminal result. The repository correction uses a protected
LocalApplicationData hierarchy, Windows DACL authority, Windows-safe result-last
publication, explicit partial-success markers, a monotonic 20-second total
deadline, reparse rejection, and bounded CLI parsing. Action A remains **NOT
STARTED** pending correction review, commit, push, and fresh preparation.

The first subsequently authorized Action A attempt stopped fail-closed while
securing the newly created LocalApplicationData `HIOC` directory. No network
request occurred and no artifact, cache, staging, or evidence content was
created. Production established that the Python-launched `powershell.exe`
could not autoload `Get-Acl`/`Set-Acl` from `Microsoft.PowerShell.Security`;
the implementation also incorrectly treated trailing `-Command` values as
`$args`. The corrected implementation uses no ACL cmdlets: it transports the
validated target through child-only environment values, reads the existing
.NET file/directory security descriptor, protects it without preserving
inheritance, removes every remaining ACE, adds exactly one current-SID
FullControl rule, persists it through `DirectoryInfo`/`FileInfo`, and rereads
all DACL invariants. The existing ordinary `HIOC` directory is accepted only
after file/reparse checks and hardened before descendants are created. Action A
is **ATTEMPTED BUT NOT COMPLETE** and requires correction publication, fresh
preparation, and separate execution authorization.

The corrected retry completed Action A with production PASS. Action B
preparation then found the committed transfer tool unsafe before PI3 access: it
selected the wrong cache level, relied on `PATH` OpenSSH, captured unbounded
diagnostics, and could not distinguish partial transfer state. The correction
uses the fixed durable cache, Windows reparse/DACL validation, bounded system
OpenSSH, separate wheel/lock stages, remote owner/mode/digest validation, and
sanitized result-last evidence. Action A is **COMPLETE / PASS**. Action B is
**BLOCKED / NOT EXECUTED** pending commit, push, preparation, and authorization.
Actions C-G remain not started.

Final Action B preparation found a second repository defect before execution:
ambient OpenSSH configuration could still redirect the effective hostname,
port, proxy/jump route, known-hosts, or identity source, and failure after
evidence rename could disagree with terminal publication state. The repository
correction disables all SSH configuration files and agents, pins numeric PI3,
port 22, proxy/canonicalization suppression, and exact non-reparse profile
known-hosts/Ed25519 paths. Evidence now requires exact post-rename digest,
owner, mode, file fsync, and directory fsync confirmation, including recovery
from an uncertain rename command. Action A remains **COMPLETE / PASS**. Action
B remains **BLOCKED / NOT EXECUTED**. Actions C-G and PE-4.0B.2a remain not
started pending commit, push, and fresh preparation.

Final Windows identity execution preparation then found two coupled governance
defects before key generation. `Path.exists()`/`Path.is_symlink()` could mistake
a dangling non-symlink reparse entry for absence, and a prior report named a key
path inconsistent with the repository's dedicated Action B contract. The
correction uses non-following entry inspection at every key/evidence collision
boundary and Windows atomic write-through publication without replacement.
Repository history confirms `.ssh/id_ed25519`/`.ssh/id_ed25519.pub` as the
intentional dedicated PE-4 pair; provisioning and Action B now have an explicit
shared-contract regression. Action A remains **COMPLETE / PASS**. Windows
identity provisioning and Action B remain **BLOCKED / NOT EXECUTED**. Action C,
Actions D-G, PE-4.0B.2a, PE-4.0B.2b, and PE-4.0C remain not started.

Fresh provisioning readiness review then found an evidence reconciliation
defect: after a no-replace collision, an independently created exact
`result.json` could be accepted without proving that the invocation's own
`.result.tmp` had been consumed. The correction requires exact final
confirmation plus non-following true absence of the temporary source on both
normal and uncertain-error paths. Retained files, dangling links, junctions,
other reparse entries, and inspection errors fail closed; collided evidence is
preserved without overwrite or a second result. Action A remains **COMPLETE /
PASS**. Provisioning and Action B remain **BLOCKED / NOT EXECUTED** pending
review, commit, push, and fresh execution preparation. Action C, Actions D-G,
PE-4.0B.2a, PE-4.0B.2b, and PE-4.0C remain not started.

Action D readiness after Action B and Action C production PASS identified a
repository defect: transferred inputs, construction pathname, environment
root, pip environment, cleanup target and evidence-to-Action-E handoff were not
continuously identity-bound. The correction adds a descriptor-bound input
snapshot and construction, explicit offline Python/pip isolation, accurate
`lib64 -> lib` venv policy, exact distribution governance, descriptor-relative
cleanup, confirmed result-last evidence and mandatory Action E eligibility.
Action D remains **BLOCKED / NOT EXECUTED**; Actions E-G and later PE-4 phases
remain **NOT STARTED** pending commit, push, PI3 synchronization and review.

The first separately authorized provisioning attempt then failed safely after
generation and staged ACL validation but before pair validation or publication.
Forensics reproduced the exact cause with disposable material: pinned Windows
OpenSSH emits its public record with CRLF, while the published parser rejected
every carriage return. The corrected contract accepts one optional LF or CRLF
terminator and still rejects bare, embedded, or repeated line endings and
malformed records. Complete real-output reproduction also proved that the
pinned derived-public command already emits the governed comment; the corrected
path parses that native three-field record rather than adding a fourth field.
No production key was published, rollback remains not recommended, and
provisioning plus Action B remain **BLOCKED / NOT EXECUTED**
pending review, commit, push, and fresh preparation. Action C, Actions D-G,
PE-4.0B.2a, PE-4.0B.2b, and PE-4.0C remain not started.

**PE-4 Windows OpenSSH trust-anchor refresh (2026-09-16):** Read-only
forensics found stale Action B `ssh.exe` and `ssh-keygen.exe` hashes after
observed September 9, 2026 System32 `OpenSSH_9.5p2` servicing drift. Both
current files were valid Microsoft-signed, TrustedInstaller-owned,
protected-ACL, non-reparse executables; exact servicing causality is
unproven. The correction updates the sole fail-closed hashes without weakening
the transport contract. Historical Action B remains **COMPLETE / PASS**, its
temporary staging remains **MISSING**, and replacement Action B plus Action D
remain **NOT EXECUTED**.
## PE-4 replacement Action B failed-transaction correction

The published replacement Action B attempt is **ATTEMPTED_NOT_COMPLETE**. It
created `/tmp/hioc-pe4-artifact-transfer-g_jrlqkl` but stopped safely at
`REMOTE_STAGING_IDENTITY_INVALID`: CPython's tempfile token contained `_`,
which the then-shared parser incorrectly excluded. Recorded PI3 forensic
identity is directory, UID/GID `1000/1000`, mode `0700`, device `45826`, inode
`131762`, and empty contents. No wheel or lock transferred, no Action D ran,
and `ROLLBACK_RECOMMENDED=FALSE`; preservation pending separate disposition
was the historical decision. Current operator checks report the directory ABSENT.
The same external wrapper also split prechecks from the
launch and misparsed Git's tab-separated `0\t0` output. The corrected repository
owns one atomic, no-retry wrapper and the sole shared full-path grammar
`/tmp/hioc-pe4-artifact-transfer-[A-Za-z0-9_]{8}`. Historical successful
staging remains missing and neither it nor the failed path may be reused.

Action A and historical Action B remain **COMPLETE / PASS**; Action C remains
**COMPLETE / PASS**; Action D is **NOT EXECUTED**; Actions E-G and PE-4.0B.2a,
PE-4.0B.2b, and PE-4.0C are **NOT STARTED**. The consumed authorization grants
no retry. Required future order is publication, PI3 source synchronization,
failed-staging disposition review, fresh replacement readiness review, and a
new exactly-once replacement Action B authorization; Action D readiness follows
only a confirmed new Action B PASS.

## PE-4 replacement Action B wrapper native-argument correction

One new authorized invocation of the `1bf339d` replacement wrapper occurred
and stopped at local precheck. Windows PowerShell legacy serialization removed
embedded quotes in its Python preflight source, so `root/"tools"` became
`root/tools` and Python raised `NameError: tools`. This was a wrapper defect,
not an Action B or PI3 event: launch was not reached, no Action B process or
SSH occurred, no PI3 staging was created, and PI3 forensics were unnecessary.
The authorization is consumed at wrapper-entry level. The corrected wrapper
uses discrete `ProcessStartInfo.ArgumentList` arguments for every Python
process and unambiguously reports wrapper, precheck, launch, and transaction
state. Because Windows PowerShell 5.1 lacks `ArgumentList`, the wrapper rejects
that legacy host and requires the managed PowerShell Core host. A new
authorization remains required after correction publication and fresh
readiness.
## Action D diagnostic-retention checkpoint

The first Action D failure is diagnostically incomplete, not a proven functional
failure. A corrected future attempt requires separate authorization; its private
failure evidence records only bounded sanitized diagnostic fields.

## PE-4 D-PREP runtime hierarchy preparation

Action A, dedicated Windows SSH identity provisioning, PI3 public-key authorization,
the current replacement Action B, and Action C are **COMPLETE / PASS**. Action D
has been attempted twice and is **NOT COMPLETE**: the second attempt localized the
missing prerequisite at `RUNTIME_PARENT_VALIDATION / OPEN_RUNTIME_PARENT`.
`PE-4.0B.2a-D-PREP` is now the mandatory separately authorized predecessor. It
creates or validates only `runtime`, `runtime/pe4`, and `runtime/pe4/environments`
under the existing HIOC runtime, preserves compliant partial hierarchy, and stops.
Action D remains construction-only and independently validates that hierarchy.
Actions E-G, authenticated PE-4.0B.2a proof, PE-4.0B.2b, and PE-4.0C remain
**NOT STARTED**.

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

### Accepted replacement staging — independent observation

Operator-supplied independent read-only review established directory mode `0700`,
UID/GID `1000/1000`, device `45826`, inode `131986`, with exactly the following
three files and no unexpected entries. Each file was regular, mode `0600`,
UID/GID `1000/1000`:

| File | Size | SHA-256 |
| --- | --- | --- |
| `websockets-16.1.1-cp311-cp311-manylinux2014_aarch64.manylinux_2_17_aarch64.manylinux_2_28_aarch64.whl` | 188095 | `86d7f0f8bdb25d2c632b72527325e4776430fd5bc61b9118de4e2b8ddb5f5b01` |
| `requirements-pe4.lock` | 308 | `19433d53e3015157207d1af4ef07930db6f0e0d525597485384b3b7d42628e96` |
| `result.json` | 321 | `e77259f28a18be5b51943db09de46d17d942f5709e70654f276f6a1a1afb58bb` |

Exact governed persisted result object:

```json
{"action":"PE-4.0B.2a-B","error_code":"NONE","evidence_state":"AWAITING_CONFIRMATION","failure_stage":"COMPLETE","lock_transferred":true,"remote_artifact_verified":true,"remote_lock_verified":true,"remote_staging_created":true,"result":"PASS","rollback_recommended":false,"schema_version":"1.0","wheel_transferred":true}
```

The persisted JSON intentionally says `AWAITING_CONFIRMATION`; terminal
`EVIDENCE_STATE=CONFIRMED` follows final publication confirmation. The JSON must
not be rewritten to CONFIRMED. Independent validation accepted its exact contract.

### Completed Windows replacement B readiness evidence

The separate read-only Windows checkpoint used clean `main`, HEAD/local
`origin/main` `b6199596fd486967fa166513c7b8c0fa7dd90328`, ahead/behind `0 0`;
governed source identities PASS. No network connection or Action B execution
occurred. Authoritative `local_inputs()` and local transport validation PASS.

- Durable cache: `C:\Users\JorgeAzofeifaCastill\AppData\Local\HIOC\artifacts\pe4\cache`.
- Exact wheel: `websockets-16.1.1-cp311-cp311-manylinux2014_aarch64.manylinux_2_17_aarch64.manylinux_2_28_aarch64.whl`;
  exists, regular file, non-reparse hierarchy, protected ACL contract PASS;
  size `188095`, SHA-256 `86d7f0f8bdb25d2c632b72527325e4776430fd5bc61b9118de4e2b8ddb5f5b01`.
- `requirements-pe4.lock`: committed/worktree Git blob
  `8f2652298f12734b0e4f43341a48ed5702fe696e`, SHA-256
  `19433d53e3015157207d1af4ef07930db6f0e0d525597485384b3b7d42628e96`; readiness PASS.
- Managed PowerShell executable:
  `C:\Users\JorgeAzofeifaCastill\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe`;
  Core `7.6.5`, required `ProcessStartInfo.ArgumentList` PASS, replacement-wrapper
  syntax PASS, execution policy `RemoteSigned`. No numeric minimum is newly defined.
- Local SSH/transport prerequisites PASS: expected Windows operator/profile,
  `.ssh` security/type/reparse policy, protected `known_hosts`, exactly one matching
  PI3 ED25519 record, dedicated `.ssh\id_ed25519` and public key, private-key ACLs,
  key fingerprint/comment/pair correspondence, pinned System32 `ssh.exe` and
  `ssh-keygen.exe`, and configured target `jazofv1@192.168.100.252:22`.

These are completed readiness facts, not a fresh execution authorization.

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

### Operator-supplied D-PREP production execution evidence

The operator executed D-PREP on `nutandpihole` as `jazofv1` from
`/home/jazofv1/hioc-release-source`, synchronized beforehand to governance commit
`5783951fdd33e0bb476c0fa53022633adddf1b8c` (subject
`PE-4: close native D-PREP revalidation`). `PRE_EXECUTION_GUARDS=PASS`.
This documentation checkpoint did not access PI3 or independently inspect evidence.

All three hierarchy components were ABSENT before execution and are now confirmed:

| Path | State | Created | Type | Owner/group | Mode | Device |
| --- | --- | --- | --- | --- | --- | --- |
| `/home/jazofv1/hioc/runtime` | CREATED_CONFIRMED | TRUE | directory | jazofv1:jazofv1 | 0750 | 45826 |
| `/home/jazofv1/hioc/runtime/pe4` | CREATED_CONFIRMED | TRUE | directory | jazofv1:jazofv1 | 0750 | 45826 |
| `/home/jazofv1/hioc/runtime/pe4/environments` | CREATED_CONFIRMED | TRUE | directory | jazofv1:jazofv1 | 0750 | 45826 |

```text
RUNTIME_PARENT_STATE=CREATED_CONFIRMED
RUNTIME_ROOT_STATE=CREATED_CONFIRMED
ENVIRONMENTS_STATE=CREATED_CONFIRMED
CREATED_RUNTIME_PARENT=TRUE
CREATED_RUNTIME_ROOT=TRUE
CREATED_ENVIRONMENTS=TRUE
CLEANUP_STATE=NOT_APPLICABLE
EVIDENCE_STATE=CONFIRMED
RESULT=PASS
ERROR_CODE=NONE
FAILURE_STAGE=COMPLETE
ROLLBACK_RECOMMENDED=FALSE
STOP_REQUIRED=TRUE
D_PREP_PROCESS_RC=0
POST_EXECUTION_VALIDATION=PASS
CHECKPOINT=D_PREP_PASS_STOP_FOR_REVIEW
NO_LATER_ACTION_EXECUTED=TRUE
INTERACTIVE_SHELL_PRESERVED=YES
```

Confirmed private evidence: `/tmp/hioc-pe4-runtime-hierarchy-prepare-8OfcmWdP`,
directory owned by `jazofv1:jazofv1`, mode `0700`, device `45826`. Preserve this
execution evidence; this closure grants no authority to inspect, modify or delete it.
The operator supplied the following confirmed `result.json`:

```json
{"action":"PE-4.0B.2a-D-PREP","cleanup_state":"NOT_APPLICABLE","created_environments":true,"created_runtime_parent":true,"created_runtime_root":true,"device_relationship":"RUNTIME_TO_PE4_SAME_DEVICE;PE4_TO_ENVIRONMENTS_SAME_DEVICE","environments_mode":"0750","environments_state":"CREATED_CONFIRMED","error_code":"NONE","failure_stage":"COMPLETE","governance_commit":"5783951fdd33e0bb476c0fa53022633adddf1b8c","result":"PASS","rollback_recommended":false,"runtime_parent_mode":"0750","runtime_parent_state":"CREATED_CONFIRMED","runtime_root_mode":"0750","runtime_root_state":"CREATED_CONFIRMED","schema_version":"1.0"}
```

D-PREP production execution is PASS and CLOSED. The missing runtime-hierarchy
prerequisite behind the second Action D failure has been corrected. This is not
Action D success: `ACTION_D=FAILED_TWICE_NOT_COMPLETE`, with no retry. No combined
native suite or later lifecycle action ran, and no rollback occurred. Action D
retry requires separate operator authorization; no command is prepared here.

### Operator-supplied native PI3 revalidation evidence

The operator manually ran the corrected D-PREP test suite on host `nutandpihole`,
user `jazofv1`, in `/home/jazofv1/hioc-release-source`. This Windows documentation
checkpoint did not connect to PI3 or independently inspect its evidence log.
The terminal-safe validation returned control to the interactive shell.

Pre-test guards: HOST=nutandpihole, USER=jazofv1, BRANCH=main; HEAD and ORIGIN_MAIN
both `c5181a0d65da294e5db2dbd6795f20889b972a22`; subject
`PE-4: isolate D-PREP tests across host platforms`; committed and worktree test blobs
both `9f2efe579acc674513594c15cba29cb37c66a45b`; Action D SHA-256
`e979cc6049f8912c23e880f121fd2988d0354623c4f2a7d27eafb310e4b0c213`.
All guards passed: `PRE_TEST_GUARD=PASS`.

```text
TESTS_RUN=115
FAILURES=0
ERRORS=0
SKIPPED=0
EXPECTED_FAILURES=0
UNEXPECTED_SUCCESSES=0
Ran 115 tests in 2.568s
OK
PI3_NATIVE_D_PREP_REVALIDATION=PASS
```

All seven POSIX-specific tests executed and passed:

- `test_posix_named_child_create_then_idempotent_open`
- `test_posix_path_bound_ancestor_rename_away_is_rejected_as_name_lost`
- `test_posix_path_bound_ancestor_replacement_is_rejected_as_name_substituted`
- `test_posix_path_bound_leaf_removal_is_rejected_as_name_lost`
- `test_posix_path_bound_leaf_rename_away_is_rejected_as_name_lost`
- `test_posix_path_bound_leaf_replacement_is_rejected_as_name_substituted`
- `test_posix_path_bound_unchanged_leaf_revalidates`

Post-test HEAD_POST and ORIGIN_MAIN_POST remained
`c5181a0d65da294e5db2dbd6795f20889b972a22`; WORKTREE_TEST_BLOB_POST remained
`9f2efe579acc674513594c15cba29cb37c66a45b`; ACTION_D_SHA256_POST remained
`e979cc6049f8912c23e880f121fd2988d0354623c4f2a7d27eafb310e4b0c213`.
`POST_TEST_IDENTITY=PASS`. Operator-reported native log:
`/tmp/hioc-dprep-native-revalidation-20261004-223906.log`.

Negative evidence at that native test-only checkpoint: `D_PREP_EXECUTED=FALSE`, `ACTION_D_RETRIED=FALSE`,
`COMBINED_SUITE_EXECUTED=FALSE`, `INTERACTIVE_SHELL_PRESERVED=YES`.
This is native test-validation evidence, not D-PREP production execution evidence.
The corrected harness is now natively validated; production advancement remains
separately authorized and no later lifecycle action is closed by this result.

### Native validation failure and bounded harness correction

The operator-reported native PI3 run of
`tests.test_pe4_action_d_hierarchy_prepare` ran 115 tests and returned **18 failures
and 1 error**. This was a TEST validation failure, not a D-PREP production execution
failure. All seven tests previously skipped on Windows executed and PASSED on PI3:

- `test_posix_named_child_create_then_idempotent_open`
- `test_posix_path_bound_ancestor_rename_away_is_rejected_as_name_lost`
- `test_posix_path_bound_ancestor_replacement_is_rejected_as_name_substituted`
- `test_posix_path_bound_leaf_removal_is_rejected_as_name_lost`
- `test_posix_path_bound_leaf_rename_away_is_rejected_as_name_lost`
- `test_posix_path_bound_leaf_replacement_is_rejected_as_name_substituted`
- `test_posix_path_bound_unchanged_leaf_revalidates`

The remaining failures are classified as test-harness portability/isolation defects.
Seventeen orchestration/device-policy failures were consistent with synthetic
patches through PREP.os / shared stdlib os intercepting unrelated runtime or stdlib
operations before intended HIOC checkpoints. The UNSUPPORTED_PRIMITIVES subcase
proved process-global contamination directly: synthetic `os.name = "nt"` caused
Linux pathlib to attempt WindowsPath construction and raise
`NotImplementedError: cannot instantiate 'WindowsPath' on your system`.
The downstream temp-root completeness failure resulted from that failed subcase.
No production implementation semantic defect was established by the earlier run.
At that historical checkpoint, corrected native PASS had not yet been established.

The bounded correction modifies only `tests/test_pe4_action_d_hierarchy_prepare.py`.
Its `_isolated_hioc_os()` private facade is separately bound to PREP.os and the os
global in hioc_pe4_runtime_common: functions imported with
`from hioc_pe4_runtime_common import *` retain their defining module globals.
Affected synthetic stat/fstat/open/close, UID/GID, primitive flags, os.name,
mutation and umask patches target that facade. Pathlib and unrelated stdlib
consumers retain the real host OS namespace. The temp-root assertion now compares
`path == pathlib.Path("/tmp")` instead of `str(path) == "/tmp"`, preserving exact
flags. No test was removed, renamed, newly skipped, marked expected-failure, or
weakened to obtain PASS.

The targeted temp-root portability test passed. Latest authoritative corrected
Windows validation (not rerun during this documentation-only checkpoint):

```text
----------------------------------------------------------------------
Ran 115 tests in 0.130s

OK (skipped=7)

----------------------------------------------------------------------
Ran 126 tests in 0.151s

OK (skipped=7)
```

The first footer is D-PREP; the second is D-PREP plus lifecycle. Both have zero
failures/errors; the seven Windows skips are exactly the POSIX tests listed above.
Four-file bytecode-write-suppressed compilation and `git diff --check` passed.
Frozen Action D SHA-256 remained
`e979cc6049f8912c23e880f121fd2988d0354623c4f2a7d27eafb310e4b0c213`.
Corrected full native PI3 validation was pending at that historical Windows
checkpoint; the operator-supplied native PASS above now closes that requirement.
D-PREP production execution subsequently passed as recorded above; the PE-4
roadmap remains incomplete.

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
