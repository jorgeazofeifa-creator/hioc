# HIOC Master Plan

## Permanent operational governance: NO ASSUMPTIONS

NO ASSUMPTIONS. NO EXCEPTIONS. Any unverified material fact is UNKNOWN.
Repository state cannot prove production state. Allowed evidence classes are DIRECT_OBSERVATION, CRYPTOGRAPHICALLY_BOUND_OBSERVATION,
IMMUTABLE_REPOSITORY_FACT (repository claims only), and OPERATOR_SUPPLIED (retain its label). Expected values are not observed values.
Production facts require direct production evidence; OPERATOR_SUPPLIED observations retain that label.
Unknown prerequisites block dependent mutation. Evidence conflicts override plans.
Assumptions discovered in governance are defects and require correction and regression protection.
No automatic adoption of changed production values; no repository-derived production baseline without observation.
Absence of evidence cannot establish absence. UNKNOWN -> VERIFY -> ESTABLISH EVIDENCE -> DECIDE -> ACT.
The closed semantic law is protected by the deployment baseline correction family and its No Assumptions tests.

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

Status: **PHASE 7A IN PROGRESS; PE-0 COMPLETE - DESIGN APPROVED; PE-1 COMPLETE - PRODUCTION VALIDATED; PE-2 COMPLETE - PRODUCTION VALIDATED; PE-3 COMPLETE; PE-3.0 COMPLETE; PE-3.1 IMPLEMENTED - REPOSITORY VALIDATED; PE-3.2 COMPLETE - EXTERNAL DATASET VALIDATED; PE-3.3 COMPLETE - DESIGN APPROVED / REPOSITORY SYNCHRONIZED; PYTHON INSTALL MANAGER PRESENT; WINDOWS PYTHON PREREQUISITE COMPLETE - PRODUCTION OPERATOR VALIDATED; WINDOWS CPYTHON 3.13.X SUPPORTED - VALIDATED PATCH 3.13.15; CPYTHON 3.14.7 PRESENT - NOT HIOC-SUPPORTED; PE-3 ACTIONS 1-10 COMPLETE; ACTION 10 COMPLETE - NOOP_ALREADY_ABSENT; PRODUCTION DEPLOYMENT COMPLETE; PI3 VALIDATION COMPLETE; PE-4 PASS/CLOSED; PUBLIC PROJECTION PASS/CLOSED; ACTIONS D/E/F/G PASS/CLOSED**

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
4. **PE-4 - Home Assistant Association** — PASS/CLOSED; D/E/F/G PASS/CLOSED; E handoff ACCEPTED; PE-4.0B.2a PASS/CLOSED; original 2b preparation complete; first 2b execution historically ATTEMPTED / NOT COMPLETE; Compatibility Resilience audit PASS/CLOSED; corrected preparation and PE-4.0B.2b PASS/CLOSED; PE-4.0C and PE-4.0C.1 PASS/CLOSED; adapter implementation preparation PASS/CLOSED; Runtime Credential Provisioning Preparation PASS/CLOSED; Runtime Credential Provisioning PASS/CLOSED; Operator Installation, Independent Validation and Governance Closure PASS/CLOSED based on operator-supplied PI3 evidence; adapter implementation, deployment, independent production acceptance and Public Projection PASS/CLOSED; scheduler ACTIVE/AUTHORIZED; PE-4 PASS/CLOSED. Production evidence remains OPERATOR_SUPPLIED.
5. **PE-5 - MQTT and Passive Service Association** — COMPLETE. PE5_9_STATUS=COMPLETE/PASS;
   all 37 requirements and 14 Definition of Done conditions accepted.
   NEXT_CHECKPOINT=PE-6.2 - PI3 Release-Source Synchronization; PE6_REPOSITORY_IMPLEMENTED=TRUE;
   separate PE-6.2 authorization required; production deployment/execution remains NOT_AUTHORIZED. The following PE-5.1 planning paragraphs are
   HISTORICAL_INTENTIONALLY_PRESERVED snapshots, not current capability status.
   Historical roadmap status at ed3a80508d101652bac89e1dcc111167670aaebc (HISTORICAL_INTENTIONALLY_PRESERVED):
   **PE-5 - MQTT and Passive Service Association** — not started.
   Current PE-5.1 is an authorized private pure-library implementation candidate; broader runtime integration is NOT_STARTED / NOT AUTHORIZED. The following preparation status is historical at f3730ba5a8745361934ff822a9c29c16c9d0767b.
   Implementation remains NOT_STARTED. Selected next roadmap checkpoint by executive decision; Implementation Preparation is current and PREPARED_FOR_REVIEW. Runtime/production implementation requires separate authorization.
6. **PE-6 - Classification & Metadata Quality** — PE-6.0 COMPLETE/PASS; PE-6.1 repository implementation COMPLETE/PASS. PE-6 IN_PROGRESS; no production deployment/execution. Next PE-6.2 requires separate authorization.
7. **PE-7 - Expected Availability & Permanent IoT Monitoring** — planned. This
   models Asset-layer expected-online intent for wall switches, smart switches,
   smart plugs, Sonoff devices, permanent lighting controls, and other
   infrastructure devices; correlates network and Home Assistant availability;
   detects failure to reconnect; and produces actionable incidents,
   notifications, affected automation/function identification, and recovery
   guidance.
   Future surveillance operating policy reuses PE-7 expected availability and permanent-IoT monitoring; battery, event-driven, maintenance and intentionally-offline cameras must not inherit an always-on assumption.
8. **PE-8 - Automation Correlation & Impact Analysis** — planned. It maps Home
   Assistant automations, scripts, scenes, triggers, entities, and Assets to
   functional impact.
   Future surveillance protection and footage-loss impact reuse PE-8 functional relationships; a failed recording path must identify the functions/assets affected.
9. **PE-9 - Service & Infrastructure Dependency Intelligence** — planned. It
   models MQTT, DNS, DHCP, Pi-hole, Home Assistant, NUT, cameras, switches, and
   other services to explain technical cause, failure propagation, service
   impact, and infrastructure topology. PE-8 owns functional impact; PE-9 owns
   technical dependency and cause.
   Future surveillance reuses PE-9 for shared camera, WAN/cloud, HA, MQTT, recorder and storage dependencies; it must not create a parallel graph or one incident per downstream camera.
10. **PE-10 - Application, Integration & Service Assurance** — planned / not
    started. After PE-8 maps operator-visible impact and PE-9 establishes the
    technical dependency model, PE-10 will determine whether an application-
    level function is actually usable, isolate the failing layer, and design
    evidence-based controlled recovery. It is future architecture work and is
    separate from the current PE-3 execution sequence.
   Surveillance is a future PE-10 specialization with the six bounded checkpoints below. It adds no numbered HIOC phase, calendar date, implementation authorization or change to current sequencing.

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
- Surveillance assurance within PE-10: one future capability, with bounded inventory/policy, layered health, recording/protection, Ring local-capture POC, Ring Protect decision and optional remediation checkpoints. Shared incident, notification, dashboard and history work is reused.

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
Surveillance applies this capability-assurance principle to usable footage, not merely camera reachability. It consumes PE-7 availability, PE-8 impact and PE-9 dependency intelligence; the mandatory roadmap order remains unchanged.

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
#### Surveillance Reliability, Recording Integrity, and Camera Infrastructure Monitoring

Status: **PLANNED / NOT STARTED — IMPLEMENTATION NOT AUTHORIZED**.
Architectural home: PE-10 Application, Integration & Service Assurance, integrated
with PE-7 expected availability, PE-8 functional impact and PE-9 dependency intelligence.
This roadmap preservation is distinct from future implementation. It does not
interrupt Phase 7A, select the current next task, start PE-5, or assign a calendar
position immediately after Phase 7A. Active Discovery remains postponed.

**Operational goal:** surveillance infrastructure should eventually reveal silent
protection failures without routine manual opening of Frigate, Home Assistant,
Ring, Wyze or other applications. HIOC must answer: "If something happens at this
camera right now, am I reasonably confident that usable footage will exist afterward?"
That question is distinct from "Is the camera online?" An online or reachable
camera is not proof of surveillance protection.

The capability is vendor-agnostic: local/cloud, continuous/event-driven,
battery/wired cameras; Wyze Secure RTSP/RTSPS; Frigate and embedded go2rtc;
Home Assistant integrations; official Ring and Ring-MQTT/Mosquitto paths;
local/cloud recording, storage and future camera technologies. Frigate is one
path, not the architecture. Reuse the existing Asset, observation, expected
availability, health, capability, correlation, incident/lifecycle/severity,
notification, history/aggregation/retention, dependency/failure-propagation,
Dashboard v2 and recovery-governance architecture. No parallel surveillance engine.

**One capability; six bounded future checkpoints** (not six new HIOC phases).
Each checkpoint requires its own approved scope, repository validation, applicable
supported deployment/production evidence and Evidence Report. No work below is
authorized by preserving this roadmap.

##### Surveillance checkpoint 1 — Camera inventory, identity and operating policy

Establish authoritative non-secret camera inventory through existing Asset and
stable technical identity architecture. Future metadata may include Asset ID,
friendly name/location, vendor/model, MAC, hostname, network/Wi-Fi/Ethernet,
expected/reserved versus observed IP, power and battery/wired policy, vendor app,
HA entity/integration relationships, RTSP/RTSPS capability, Frigate/Ring-MQTT IDs,
expected video/audio, motion/future AI capability, recording expectation and
destination, retention, local/cloud/subscription dependencies, expected
availability, criticality and maintenance history. These are FUTURE extensions:
accepted PE-2.1 currently supplies friendly_name, physical_location, purpose and
private notes only. Credentials, passwords, tokens and authenticated URLs never
belong in Asset metadata.

Policies distinguish always-on, continuous-recording, event-driven, monitor-only,
battery, wired, cloud-dependent/local-stream, temporarily disabled, maintenance
and intentionally-offline assets. Unsupported capability is N/A; missing evidence
is UNKNOWN, not healthy, degraded or offline without supporting policy/evidence.

Camera address/DHCP hardening is a **separately authorized sub-checkpoint where
required**, not an automatic independent phase. Evaluate camera MAC -> Pi-hole
DHCP reservation -> expected IP -> correlation with HIOC Asset identity; do not
default to device-side static addressing. Asset/stable technical identity is not
derived from an IP alone. Correlate MAC, lease/reservation, neighbor observations,
HA relationships, Frigate source configuration and the Asset record through the
existing DHCP acquisition and central canonical reconciliation. Unexpected IP must
not silently replace expected identity/address state; reservations cannot override
identity or fabricate liveness. Completed Canonical Address Selection Hardening
remains complete; deferred local-address/historical-identity decisions stay separate.
No reservation, address migration or Pi-hole change is authorized here.

##### Surveillance checkpoint 2 — Layered surveillance-path health

Vendor-specific evidence feeds shared HIOC health and dependency reasoning.
Preserve independent physical camera, power, LAN/Wi-Fi, DHCP/addressing, local
camera service, vendor cloud, HA integration/entity freshness, MQTT, Mosquitto,
Ring-MQTT, go2rtc, Frigate, ffmpeg, video frames, audio, recording, storage, motion,
future detection and notification/incident-path observations. Do not collapse all
failures into CAMERA_OFFLINE. Ping/ICMP, DHCP, ARP/neighbor presence or an open port
is only evidence for its own layer, never proof of protection.

Wyze/vendor-app availability can coexist with HA/local surveillance failure.
Distinguish physical/power/network/IP, vendor cloud/app, HA integration/entity,
Secure RTSP/RTSPS, go2rtc, Frigate and recording paths; explain the failed path
rather than declaring the physical camera offline. No Wyze troubleshooting now.

Frigate monitoring may evaluate installed-version capabilities in HA app/process/
container state, API/stats, camera roles, ffmpeg roles, embedded go2rtc, recording,
resource state, watchdog/restarts, HA integration and relevant MQTT evidence.
Separate application unavailable, application running with failed camera/recording/
motion pipeline, go2rtc source failure and ffmpeg consumer failure. These are
conceptual failure distinctions, not a second incident taxonomy. Preserve producer
and consumer existence/connection, bytes/packets progressing, video/expected-audio
codecs and reconnect behavior. A configured stream with stalled media is not
healthy. Evaluate camera_fps, process_fps, skipped_fps, detection_fps and ffmpeg
role-state equivalents with normal grace/debounce. Object detection is not needed
to prove basic recording. Do NOT reintroduce a second go2rtc architecture without a specific future requirement.

Ring has two existing paths: official HA Ring integration, and Ring-MQTT through
Mosquitto with its internal on-demand stream bridge. They offer partially
independent evidence but share WAN/Ring-cloud dependencies, so agreement is not
independent proof. Correlate official Live View/last-recording entities and motion/
ding events with Ring-MQTT motion/ding, snapshots, stream controls, battery, Wi-Fi,
device information, telemetry and service/resource/version capability evidence.
Do not rename production entities. Prefer authoritative existing signals to
duplicate sensors. Ring-MQTT and Mosquitto are infrastructure dependencies; one
shared outage should explain affected observations rather than create duplicate
camera incidents. Ring-MQTT on-demand RTSP remains cloud-dependent, not native
local-camera RTSP. Do not plan permanent 24/7 Ring streams into Frigate; event/
on-demand policy remains default, with separate battery and wired policies.
Ring Protect is a recording CAPABILITY DEPENDENCY, not physical camera health:
absent paid recording may leave device, Live View, events and local capture healthy.

##### Surveillance checkpoint 3 — Recording integrity and protection assurance

Recording integrity is PRIMARY. Ping, DHCP presence, open port, working vendor
app, HA entity, running Frigate, configured go2rtc, existing ffmpeg or MQTT
connectivity is individually insufficient. Independently establish actual output
using applicable newest-segment/finalized-recording timestamps, file creation and
progression, recording API/metrics, current segment progression, media-directory
activity and age of latest valid recording. If expected continuous output stops
beyond an evidence-validated threshold, shared incident architecture must represent
that failure. Exact thresholds/cadences and APIs remain future decisions.

At lower cadence, inspect recently completed media: exists, nonzero size, valid
container, video and expected audio tracks, successful video/audio probe or decode,
sane duration/timestamps and no corruption. ffprobe or another trusted local
validator may be evaluated later; no tool/cadence is selected now. Video/audio are
separate dimensions: video healthy with expected audio missing normally means
degradation, unless Asset policy makes audio critical. Motion processing can fail
while recording remains healthy. Future detector/accelerator availability,
inference/FPS, queue/backlog, latency, acceleration/fallback, crashes and degradation
are separate from basic recording assurance.

Storage health includes expected mount/device, writable state, free capacity and
percentage used, write failures, directory accessibility, recording/abnormal growth,
projected retention, filesystem errors, read-only state and retention pressure.
Storage disappearance or read-only state should be CRITICAL because cameras can remain online while footage is no longer preserved.
Use current measurements; historical capacity is not a permanent assumption.

**Protection Status** is derived capability state, not another core health engine.
Derive reasonable footage expectations from operating policy, evidence freshness,
recording paths/integrity and dependencies. Conceptual outcomes include fully
protected; recording degraded; local path failed; cloud-only or local-only recording;
Live View only; monitoring only; device offline; surveillance unavailable; UNKNOWN.
Do not imply equal protection across local continuous, cloud/event and monitor-only
cameras. Missing evidence never produces an all-clear.

##### Surveillance checkpoint 4 — Ring event-driven local-recording POC

A separate FUTURE PRODUCTION EXPERIMENT, requiring explicit authorization, asks
whether local capture can reduce dependence on Ring Protect without materially
reducing protection. Pipeline to evaluate: motion/ding -> HA and/or Ring-MQTT
event -> event-triggered capture -> Ring-MQTT on-demand stream -> FFmpeg or an
equivalent trusted recorder -> HA external media storage -> media validation ->
HIOC observations/history/protection. Terminate the session after the recording
window; do not leave live streams permanently active.

The beginning of an event cannot be captured locally before event delivery,
reaction, live-session establishment and usable media. Measure T0 physical event
where observable, T1 HA event receipt, T2 RTSP initiation, T3 first usable frame and
T4 recording start; record event-to-frame/event-to-recording deltas and missing
beginning-of-event coverage. Do not infer replacement viability from one success.

The future POC matrix covers motion, ding where applicable and manual capture;
video/audio, startup latency, integrity/duration and clean termination; repeated,
back-to-back and concurrent-camera events; Ring-MQTT/Mosquitto/HA restarts;
Internet loss and safely observable Ring cloud/API disruption; storage loss/
pressure; battery/thermal impact; motion/ding impact; activation failure, recovery,
corruption and missed-event rate. No capture or fault injection occurs now.

##### Surveillance checkpoint 5 — Ring Protect replacement decision

Separate from the POC and based on extended production evidence. Measure motion/
ding capture percentages, median/worst startup latency, valid-video/audio rates,
corruption, lost event beginnings, cloud/bridge/HA/MQTT/storage failures, battery
impact, recovery and protection availability. Permitted eventual conclusions are:
reliably replaces Ring Protect; partially replaces it; works with materially worse
coverage; insufficient reliability for security use; or Ring Protect remains
necessary. No conclusion or subscription cancellation is authorized now.

##### Surveillance checkpoint 6 — Optional controlled remediation

Initial behavior is OBSERVE -> CLASSIFY -> ALERT -> RECORD HISTORY. No automatic
camera/network reboot, HA/Frigate/Ring-MQTT restart, power cycle, DHCP mutation or
storage remount is implicit. Optional later remediation uses shared PE-10 policy,
bounded retries/cooldowns, evidence, recovery verification and separate authorization.

##### Surveillance cross-cutting acceptance and safeguards

Incidents, notifications, unified dashboard and reliability history are acceptance
requirements across checkpoints, not replacement systems. Reuse detected,
confirmed, active, recovering and resolved lifecycle, stable root-cause keys,
affected dependencies, recovery confirmation and grace/debounce to avoid storms.
Represent physical/network loss, address mismatch, stream/authentication/stall,
missing video/audio, integration/Frigate/go2rtc/ffmpeg failure, stale/corrupt media,
motion/detection failure, storage loss/read-only/capacity, reconnect/restart
instability, Ring cloud/Live View/events/snapshot and local-capture failures through
existing/generalized incident semantics. Severity reflects actual protection
impact: snapshot/audio or one integration-path loss is not automatically complete
outage while alternate protection remains.

Use existing HA phone notification delivery and planned notification-semantics
work: camera/location, severity/failure, start/duration, recording/Live View/video/
audio impact, supported cause, recommendation and upstream dependency. Recovery
reports what recovered, duration, automatic/manual recovery, recording resumption,
measured or qualified estimated footage gap and remaining degradation. Use the
same Dashboard v2 with a unified Surveillance / Cameras area: concise overall
health and Protection Status, expected availability, network/address/stream/
recording/media/audio/storage state, freshness, incidents and last outage/check;
vendor telemetry belongs in drill-down. N/A is not failure; UNKNOWN is not healthy.

History/aggregation should retain camera/Live View/recording/protection availability,
footage gaps, reconnects/ffmpeg restarts/stream instability, Ring-MQTT/integration/
storage outages, audio/media failures, capture success/latency, battery impact,
unexpected IP changes, MTBF/MTTR, storage use and projected retention. Reuse
aggregation/downsampling and asset-aware retention; do not retain unnecessary
high-frequency raw telemetry indefinitely. Actual recording retention and HIOC
telemetry retention have distinct policy/evidence but share governance.

Use PE-9 graphs for local camera -> LAN/addressing -> stream -> embedded go2rtc ->
ffmpeg -> recording -> storage; Ring -> WAN/cloud -> official HA integration;
Ring -> WAN/cloud -> Ring-MQTT -> Mosquitto -> HA MQTT evidence; and Ring-MQTT ->
on-demand stream -> recorder -> storage -> media validation. Preserve affected
cameras while correlating common upstream failures. Reuse infrastructure topology,
automatic relationships, failure propagation, trends and predictive recommendations.
Integrate storage/recovery obligations with planned backup/DR/hardware migration
and separate cold-boot proof; none of those checkpoints is silently completed here.

**DENY BY DEFAULT:** retain only explicitly approved non-secret attributes. Never
persist/expose RTSP/RTSPS passwords or authenticated stream URLs, Ring account
email/authentication/refresh tokens, HA/API/proxy tokens, entity_picture query
tokens, video_url values, recording URLs or MQTT passwords. Never dump raw camera
entity attributes into logs, Git, this Master Plan, incidents, Evidence Reports or
dashboards. Secret provisioning, permissions and compatibility must follow existing
HIOC privacy, trust and deployment governance.

**Historical/operator-supplied context only:** PI5 HA is the project HA/surveillance
host; the project-authoritative address reference is 192.168.100.251, not newly
observed production evidence. 192.168.100.152 is obsolete historical addressing,
never a current address. This action does not verify PI5 state. Earlier context:
Frigate as an HA app with embedded go2rtc; redundant standalone go2rtc stopped/
manual boot; camara_parque using Wyze Secure RTSP/RTSPS; historical camera
192.168.100.133, TCP 322, H.264 and PCMA/pcm_alaw; historical roughly 14-day
recording target, storage measurements and 72-hour reliability baseline; motion
tuning postponed and object detection disabled during reliability work. These are
not permanent capacity, traffic, configuration, retention or present-health claims.
The complete requirements below preserve the historical/operator-supplied details; they do not establish newly observed production facts.

Future local/Frigate validation uses reversible/synthetic failures where practical:
power/network loss; reachable camera with RTSPS unavailable; authentication/stall;
Frigate stopped; go2rtc producer/consumer and ffmpeg loss; stopped recording;
unavailable recording directory; storage thresholds/read-only simulation; corrupt
media; missing video/audio; motion/future detector failure; unexpected IP; recovery,
notification delivery, incident resolution, dashboard transitions and history.
Ring retains its separate POC matrix. Completion requires evidence of actual
recording/integrity/protection, useful alerts/recovery and footage gaps, secret
protection, duplicate/storm suppression, scalability to additional cameras,
reservation validation where appropriate, multi-path discrepancy diagnosis and
measured Ring limitations. Sensors alone do not establish success.

Monitoring has conceptual FAST freshness/progression, MEDIUM storage/address/
service/entity/reconnect, and DEEP periodic media/codec/capture/trend layers.
Exact cadences, thresholds, interface versions, schemas and tools require future
approval and capability-first compatibility review, not historical version pinning.
No MQTT, HA sensors/automations/cards, Frigate/go2rtc/Ring-MQTT/Mosquitto/Pi-hole/
DHCP/camera changes, recording scripts, watchdogs, notifications, reservations,
restarts, tuning/detection/acceleration, troubleshooting, migration or storage fault
injection is implemented or authorized by this documentation checkpoint.
##### Original surveillance requirements — complete preservation and applicability

The following is the complete original user-provided 73-section specification,
retained verbatim as the detailed requirements for this ONE future capability.
The six checkpoints above organize its execution; the numbered source sections
below are requirement references, not additional phases or duplicate roadmap entries.
No requirement is replaced by an umbrella statement. The complete source governs
where a preceding overview is less detailed. Suggested A–K phases remain suggestions;
the six-checkpoint organization preserves their subjects without creating eleven phases.

Checkpoint applicability: 1 consumes sections 21, 23–28 and 50; 2 consumes sections
5–6, 8–14, 19, 29–37, 44–48, 52–53; 3 consumes sections 7, 15–18, 20, 22 and 51;
4 consumes sections 38–42; 5 consumes section 43; 6 consumes section 59.
Sections 1–4, 54–58, 60–73 govern the shared architecture, safeguards, acceptance,
sequence and completion of those checkpoints. Shared incidents, notifications,
dashboard and history are reused; no separate surveillance engine is introduced.

All supplied statements about existing/current/observed/validated production
architecture, versions, entities, settings, addresses, measurements, baselines
and failures describe HISTORICAL / OPERATOR_SUPPLIED context at the time of the
original request. They are not newly observed facts or proof of present health.
The current HA address reference remains 192.168.100.251; 192.168.100.152 remains
obsolete historical addressing, never a current endpoint. Historical measurements
are not permanent capacity assumptions. Examples are illustrative, not observations.
Future requirements, constraints, qualifications and acceptance criteria remain
operative when the corresponding checkpoint is separately authorized.

**Historical surveillance-planning applicability snapshot at 6f69c4dfb85924a83b59e85ef2da602fc75ec5ea:** the following preparation/publication and UNKNOWN sequencing sentences preserve their accepted historical state. The current PE-5 executive decision in Current Objective / Next Planned Task supersedes sequencing only; the complete original surveillance source and future implementation safeguards remain unchanged.

The original review and completion directions are preserved as governance gates.
They do not grant implementation, production, staging, commit or push authorization
for this unstaged documentation candidate. Commit/push require separate authorization;
publication itself does not authorize implementation. PE-4 and its documentation
correction remain PASS/CLOSED, Phase 7A remains ACTIVE, PE-5 remains NOT_STARTED
and unauthorized, and the current next task remains UNKNOWN / NOT YET AUTHORIZED.

User-established testing clarification: Normally, HIOC does not intentionally create failures. For future surveillance reliability testing, controlled and reversible failures are allowed when they can be performed safely, because otherwise we may never be able to prove that HIOC detects important camera and recording failures.
This scoped future exception coexists with the normal Decision Log policy;
it authorizes no fault injection, production access or implementation now.

The preserved source follows; its section 66 is subject to that explicit safety
qualification. No original text has been condensed, rewritten or removed.

<!-- ORIGINAL_SURVEILLANCE_SPECIFICATION_BEGIN -->
```text
I want to add a comprehensive future Surveillance Reliability, Recording Integrity, and Camera Infrastructure Monitoring capability to the HIOC Master Plan.

This is a ROADMAP / ARCHITECTURE / DOCUMENTATION task only.

DO NOT begin implementing this capability now unless the current authoritative HIOC Master Plan explicitly shows that surveillance work is the approved active checkpoint.

The purpose of this request is to ensure that this capability is preserved in docs/HIOC_MASTER_PLAN.md and scheduled at the architecturally appropriate point in the HIOC roadmap without interrupting, reordering, bundling with, or destabilizing the work HIOC is currently doing.

======================================================================
1. GOVERNANCE AND SOURCE OF TRUTH
======================================================================

Treat:

docs/HIOC_MASTER_PLAN.md

as the authoritative source of truth.

Before making any change:

1. Read the current Master Plan completely enough to understand:
   - current active phase/checkpoint
   - Implementation Status
   - current corrective work
   - planned future phases
   - health/state architecture
   - incident lifecycle
   - notification architecture
   - asset-centric roadmap
   - canonical IP/address work
   - DHCP work
   - Home Assistant integration plans
   - dependency graph plans
   - historical metrics plans
   - dashboard plans
   - expected-availability work
   - retention/archive plans
   - backup/disaster-recovery plans
   - repository/deployment governance
   - any already-planned camera, media, IoT, or surveillance work

2. Do not assume old chat history represents current project status if the Master Plan says otherwise.

3. Preserve every existing roadmap item and checkpoint.

4. Do not reorder current work merely because this surveillance capability is important.

5. Do not bundle this surveillance work into an unrelated active checkpoint.

6. If existing planned HIOC capabilities already cover part of this requirement, integrate this work with them instead of creating parallel architecture.

7. If the surveillance capability needs to be split into multiple future checkpoints, do so only where architectural dependencies justify it.

8. Avoid creating a surveillance-specific duplicate implementation of:
   - health semantics
   - state semantics
   - incident lifecycle
   - severity
   - notifications
   - asset identity
   - expected availability
   - historical storage
   - dependency modeling
   - dashboard framework

9. Surveillance should become another domain using HIOC's core architecture, not an isolated side system.

======================================================================
2. DOCUMENTATION AND GIT GOVERNANCE
======================================================================

This planning checkpoint must follow the normal HIOC governance model.

At completion:

1. Validate the documentation change.
2. Update the relevant Implementation Status / roadmap / architecture / decisions sections of docs/HIOC_MASTER_PLAN.md.
3. Commit documentation changes.
4. Push them to main.
5. Verify a clean working tree.
6. Produce the standard concise HIOC Evidence Report.

Code and documentation governance rules already established for HIOC remain in force.

Do not leave:
- unexplained modified files
- untracked planning artifacts
- divergent documentation
- duplicate roadmap entries
- temporary files
- incomplete commits

If repository state or current governance prevents a safe Master Plan change, STOP and report the conflict instead of working around it.

Codex has no authenticated PI3 access.

Do not instruct Codex to:
- SSH to PI3
- inspect PI3 directly
- modify PI3
- synchronize PI3
- deploy to PI3

If future implementation requires PI3 changes, Codex must work on the Windows repository only and provide exact operator-run PI3 commands for the user.

======================================================================
3. CAPABILITY NAME
======================================================================

Use a broad capability name such as:

Surveillance Reliability, Recording Integrity, and Camera Infrastructure Monitoring

Do NOT name the architecture only around Frigate.

Frigate is one surveillance path.

Ring, Home Assistant camera integrations, vendor cloud integrations, local RTSP/RTSPS cameras, MQTT, storage, and future camera technologies are other paths.

The HIOC model must be camera/vendor agnostic.

======================================================================
4. BUSINESS / OPERATIONAL GOAL
======================================================================

The operational problem is simple:

I do not intend to manually open Frigate, Home Assistant, the Ring app, or the Wyze app every day to verify that every security camera is still working and footage is still being recorded.

It would be unacceptable to discover after an incident that:

- a camera stopped streaming several days earlier
- Frigate stopped receiving frames
- recordings silently stopped
- storage became unavailable
- audio disappeared
- Home Assistant lost the camera
- an integration failed
- the camera changed IP
- Ring-MQTT stopped working
- a camera was visible in the vendor app but not through the local surveillance path
- files were being created but were corrupt
- the system claimed to be healthy while no usable footage was being preserved

The surveillance system must eventually monitor itself.

HIOC should be able to answer:

"If something happens at this camera right now, am I reasonably confident that usable footage will exist afterward?"

That question is more important than simply:

"Is the camera online?"

======================================================================
5. CURRENT HOME ASSISTANT / SURVEILLANCE HOST
======================================================================

Home Assistant runs on:

PI5 HA

Current LAN IP:

192.168.100.251

Do not use the obsolete historical PI5 address 192.168.100.152.

The current surveillance architecture includes:

- Home Assistant
- Frigate
- embedded Frigate go2rtc
- Ring-MQTT with Video Streaming
- Mosquitto
- official Home Assistant Ring integration
- Wyze cameras
- Ring cameras
- external HDD used for Frigate media
- Pi-hole DHCP running elsewhere in the infrastructure

======================================================================
6. CURRENT FRIGATE ARCHITECTURE
======================================================================

Frigate currently runs as a Home Assistant app.

Known Frigate version when this requirement was created:

0.18.0

Frigate uses its own embedded go2rtc instance.

A previously installed standalone go2rtc app has intentionally been stopped and configured for manual boot because it became redundant.

Do NOT reintroduce a second go2rtc architecture without a specific future requirement.

Current desired path:

Camera
   ->
Frigate embedded go2rtc
   ->
Frigate ffmpeg
   ->
recording / motion processing

The first camera being tested through this architecture is:

camara_parque

Current source technology:

Wyze Secure RTSP / RTSPS

Current camera address at the time of testing:

192.168.100.133

Secure RTSP service:

TCP 322

Current stream capabilities observed:

- H.264 video
- 1920x1080 source
- approximately 20 fps source
- PCMA / pcm_alaw audio

Frigate currently records the original stream.

Motion-analysis path currently uses approximately:

1280x720
5 fps

AI object detection is currently intentionally disabled while stream and recording reliability are validated.

======================================================================
7. CURRENT FRIGATE RETENTION / STORAGE BASELINE
======================================================================

Continuous Frigate recording retention is currently configured for approximately:

14 days

Motion-related retention is also configured for approximately:

14 days

The Frigate recording filesystem is located on the Home Assistant external HDD.

At the time of initial measurement:

- filesystem had roughly 418 GiB free
- one camera consumed approximately 3.65 GiB/day
- estimated 14-day usage for that camera was approximately 51 GiB

These are historical measurements only.

Do NOT hard-code them as permanent capacity assumptions.

Future HIOC storage logic should use actual current measurements.

======================================================================
8. CURRENT 72-HOUR FRIGATE RELIABILITY TEST
======================================================================

A manual reliability baseline is currently being conducted for camara_parque.

The intent is to leave the camera configuration stable for at least 72 hours and later verify:

- stream continuity
- go2rtc connectivity
- Frigate health
- recording continuity
- storage growth
- ffmpeg errors
- RTSPS errors
- reconnects
- recording gaps

Motion tuning is intentionally postponed until after the baseline.

Do NOT alter this current camera configuration merely to add the future HIOC roadmap item.

This current test should be referenced as useful historical evidence, but the Master Plan planning task must not interfere with it.

======================================================================
9. SURVEILLANCE HEALTH MUST BE MULTI-LAYERED
======================================================================

A camera must NOT have a single Boolean "online/offline" health state.

Model independent layers such as:

PHYSICAL CAMERA
    ->
POWER
    ->
NETWORK / LAN / WI-FI
    ->
DHCP / EXPECTED ADDRESS
    ->
LOCAL CAMERA SERVICE
    ->
VENDOR CLOUD, IF APPLICABLE
    ->
HOME ASSISTANT INTEGRATION
    ->
MQTT / BROKER, IF APPLICABLE
    ->
GO2RTC / STREAM BRIDGE
    ->
FRIGATE PIPELINE, IF APPLICABLE
    ->
RECORDING
    ->
MEDIA INTEGRITY
    ->
MOTION PROCESSING
    ->
OBJECT DETECTION, IF APPLICABLE
    ->
STORAGE
    ->
NOTIFICATION / INCIDENT PIPELINE

Each layer may fail independently.

HIOC should eventually identify the failed layer rather than labeling everything CAMERA_OFFLINE.

======================================================================
10. CAMERA NETWORK REACHABILITY
======================================================================

HIOC should monitor whether a physical camera is reachable where network-level observation is meaningful.

However:

PING / ICMP MUST NEVER BE TREATED AS PROOF THAT A CAMERA IS OPERATIONAL.

A camera may:

- respond to ping
- retain a DHCP lease
- appear in the ARP/neighbor table

while:

- RTSP/RTSPS is down
- cloud integration is down
- Home Assistant is unavailable
- Frigate cannot receive frames
- recording has stopped

Network reachability is only one observation.

======================================================================
11. CAMERA STREAM SERVICE HEALTH
======================================================================

For cameras expected to expose a local streaming service, HIOC should eventually distinguish:

- endpoint reachable
- service port open
- authentication successful
- session established
- media negotiation successful
- video frames actually flowing
- audio actually flowing
- stream progressing
- repeated reconnects
- stalled stream
- abnormal disconnect rate

For camara_parque, RTSPS port 322 previously demonstrated an important failure mode:

the camera could remain reachable on the network while Secure RTSP was unavailable.

This must be represented as:

CAMERA NETWORK HEALTHY
LOCAL STREAM SERVICE FAILED

rather than CAMERA OFFLINE.

======================================================================
12. FRIGATE HEALTH
======================================================================

Monitor Frigate itself separately from camera health.

Potential authoritative signals may include:

- Home Assistant app state
- container health
- Frigate API availability
- Frigate stats
- camera role states
- ffmpeg processes
- go2rtc state
- Home Assistant integration entities
- MQTT if/when used
- internal watchdog/restart behavior
- recording activity
- process resource health

Differentiate:

FRIGATE_UNAVAILABLE

from:

FRIGATE_RUNNING_CAMERA_PIPELINE_FAILED

from:

FRIGATE_RUNNING_RECORDING_FAILED

from:

FRIGATE_RUNNING_MOTION_PIPELINE_FAILED

from:

GO2RTC_SOURCE_FAILED

from:

FFMPEG_CONSUMER_FAILED

======================================================================
13. GO2RTC PRODUCER / CONSUMER HEALTH
======================================================================

For Frigate cameras, HIOC should eventually understand the embedded go2rtc producer/consumer relationship.

For camara_parque the validated model is:

RTSPS producer
   ->
Frigate embedded go2rtc
   ->
localhost RTSP restream
   ->
Frigate ffmpeg consumer

go2rtc exposes useful metadata including:

- producer
- consumer
- codecs
- bytes
- packets
- connection state

HIOC should not merely check that a stream is configured.

It should determine whether traffic is progressing.

A configured stream with static packet/byte counters is not healthy.

Potential future checks:

- producer exists
- producer connected
- consumer exists
- consumer connected
- byte counters increasing
- packet counters increasing
- video codec present
- audio codec present
- restart/reconnect rate

======================================================================
14. FRAME HEALTH
======================================================================

HIOC should detect when Frigate stops receiving useful frames.

Evaluate current Frigate metrics such as:

camera_fps
process_fps
skipped_fps
detection_fps
ffmpeg role state
or the current equivalent metrics exposed by the installed Frigate version

A camera expected to be active that reports zero useful frames for a sustained period should transition through normal HIOC health semantics.

Avoid false incidents for extremely short renegotiations.

Use HIOC debounce / grace / incident-lifecycle semantics.

======================================================================
15. RECORDING INTEGRITY IS A PRIMARY REQUIREMENT
======================================================================

This is one of the most important requirements.

HIOC must prove that recording is ACTUALLY OCCURRING.

The following are individually insufficient:

- camera responds to ping
- camera app works
- RTSP/RTSPS port is open
- Frigate app is running
- go2rtc stream exists
- ffmpeg process exists
- camera entity says idle/streaming
- MQTT device says connected

Recording freshness must be independently validated.

Potential signals:

- timestamp of newest recording segment
- recording file creation rate
- Frigate recording API/metrics
- current segment progression
- media directory activity
- most recent successful finalized recording
- age of latest valid recording

If continuous recording is expected and new valid recording output stops beyond an appropriate threshold:

create a recording failure incident.

======================================================================
16. DEEP MEDIA VALIDATION
======================================================================

At a lower cadence than basic health checks, HIOC should inspect a recently completed recording file.

For Frigate/Wyze camara_parque, expected media currently includes:

VIDEO:
H.264

AUDIO:
PCMA / pcm_alaw at the source

Validate at minimum:

- file exists
- file size > 0
- container parses
- video track exists
- audio track exists when audio is expected
- video can be probed/decoded
- audio can be probed/decoded
- duration is sane
- timestamps are sane
- file is not corrupt

Possible future implementation:

ffprobe
or another trusted local media validator

Do not run expensive deep validation every second.

Use an appropriate periodic cadence.

======================================================================
17. AUDIO HEALTH
======================================================================

Audio is part of the expected surveillance evidence for cameras configured with audio.

HIOC should distinguish:

VIDEO HEALTHY
AUDIO HEALTHY

from:

VIDEO HEALTHY
AUDIO MISSING

Loss of audio should normally produce a DEGRADED surveillance state rather than CAMERA OFFLINE, unless camera policy explicitly defines audio as critical.

Recorded-media validation should verify expected audio presence.

======================================================================
18. MOTION PROCESSING HEALTH
======================================================================

Frigate motion processing should be monitored separately from recording.

A valid state may be:

RECORDING:
HEALTHY

MOTION PROCESSING:
FAILED

CAMERA:
ONLINE

Do not classify the entire surveillance pipeline offline because one analytical capability fails.

======================================================================
19. FUTURE OBJECT-DETECTION HEALTH
======================================================================

AI object detection is currently intentionally disabled.

When enabled in a future checkpoint, extend the model to include:

- detector availability
- accelerator availability
- detector FPS / inference health
- detector queue/backlog
- inference latency
- hardware acceleration/fallback
- detector crashes
- CPU fallback
- abnormal performance degradation

Object detection must remain a separate health dimension from recording availability.

======================================================================
20. STORAGE HEALTH
======================================================================

Surveillance reliability depends on storage.

HIOC should eventually monitor:

- expected media filesystem mounted
- expected storage device present
- filesystem writable
- free space
- percent used
- write failures
- media directory accessible
- recording growth
- abnormal storage-growth changes
- projected retention
- filesystem errors
- read-only state
- retention pressure

Storage disappearance or read-only state should be CRITICAL because cameras can remain online while footage is no longer preserved.

Do not use static historical capacity assumptions.

Use current observed storage metrics.

======================================================================
21. EXPECTED AVAILABILITY
======================================================================

Security cameras should be modeled as permanent infrastructure assets.

They are not transient Wi-Fi clients.

A camera expected to be always available should integrate with the HIOC expected-availability model.

The model should support:

- always-on camera
- event camera
- battery camera
- cloud-dependent camera
- temporarily disabled camera
- maintenance state
- intentionally offline state

Expected availability should affect incident generation.

======================================================================
22. PROTECTION STATUS
======================================================================

Add a higher-level surveillance concept:

PROTECTION STATUS

This is separate from ordinary device health.

Example states:

HEALTHY / FULLY PROTECTED

CAMERA HEALTHY / RECORDING DEGRADED

CAMERA HEALTHY / LOCAL PATH FAILED

CAMERA HEALTHY / CLOUD RECORDING ONLY

CAMERA HEALTHY / LOCAL RECORDING ONLY

LIVE VIEW ONLY

MONITORING ONLY

DEVICE OFFLINE

SURVEILLANCE UNAVAILABLE

The protection status should answer:

"If an incident happens right now, what evidence are we reasonably confident will exist?"

======================================================================
23. CAMERA ASSET MODEL
======================================================================

Each camera should eventually become a first-class HIOC asset.

Relevant metadata may include:

- asset ID
- friendly name
- physical location
- vendor
- model
- MAC address
- expected/reserved IP
- current observed IP
- hostname
- power type
- battery-powered vs wired
- Wi-Fi vs Ethernet
- Wi-Fi network
- stream protocol
- stream port
- Frigate camera ID
- Ring-MQTT camera ID
- Home Assistant entity IDs
- expected video codec
- expected audio codec
- expected availability
- criticality
- recording policy
- retention policy
- local/cloud dependencies
- subscription dependency
- motion capability
- object-detection capability
- notes
- maintenance history

Never store stream passwords or authentication tokens in the asset record.

======================================================================
24. CAMERA NETWORK ADDRESS HARDENING
======================================================================

Permanent cameras should not depend on arbitrary DHCP addresses.

However, do NOT default to manually configured device-side static IPs.

The preferred architecture should be:

PI-HOLE DHCP RESERVATIONS / STATIC DHCP LEASES

based on:

MAC ADDRESS
    ->
RESERVED IP
    ->
DOCUMENTED HIOC ASSET IDENTITY

This provides stable addressing while retaining centralized network control.

Before scaling Frigate or other IP-based camera integrations, determine whether surveillance-address hardening should be a prerequisite.

======================================================================
25. CAMERA DHCP RESERVATION CHECKPOINT
======================================================================

Create or preserve a future checkpoint for surveillance address hardening.

Suggested work:

- inventory all cameras
- record MAC
- record current IP
- identify vendor/model
- determine whether MAC is stable
- inspect Pi-hole DHCP configuration
- select intended reservation
- verify no conflict
- ensure reservation fits network addressing plan
- apply reservation
- renew/reboot one camera at a time
- prove correct address is received
- confirm persistence after camera restart
- confirm persistence after Pi-hole restart
- update Frigate/HA references only after identity is proven
- integrate expected IP into HIOC asset metadata

Do not change all cameras simultaneously.

Use incremental production validation.

======================================================================
26. CANONICAL IP WARNING
======================================================================

This camera work must respect HIOC's canonical-address correctness work.

HIOC has previously identified a class of problem where:

one MAC
may have
multiple neighbor-table IP addresses

and a stale neighbor entry may incorrectly become the canonical address even when an active DHCP lease exists.

Do not trust HIOC camera IP conclusions until canonical-address semantics are correct enough for this use.

Camera-IP monitoring should correlate:

- MAC identity
- Pi-hole DHCP lease
- DHCP reservation
- neighbor table
- Home Assistant entities
- Frigate source configuration
- HIOC asset record

An unexpected IP should not silently replace the expected address.

======================================================================
27. UNEXPECTED CAMERA IP CHANGE
======================================================================

For permanent surveillance assets, detect unexpected addressing changes.

Example:

EXPECTED:
192.168.100.133

OBSERVED:
192.168.100.147

Possible causes:

- missing reservation
- reservation not applied
- camera reset
- randomized MAC
- duplicate IP
- stale neighbor entry
- DHCP issue
- manual configuration
- operator change

HIOC should create an observation and possibly an incident depending on impact.

A camera online at the wrong address may still break Frigate.

======================================================================
28. ADDRESS DEPENDENCY MODEL
======================================================================

Represent addressing as part of the dependency graph.

Conceptually:

Camera MAC
   ->
Pi-hole DHCP reservation
   ->
expected IP
   ->
camera stream service
   ->
go2rtc / integration
   ->
recording

HIOC should eventually be able to say:

"Camera is online, but Frigate is still attempting to reach the previous IP."

That is not the same as:

"Camera is offline."

======================================================================
29. WYZE VENDOR-APP VS HOME ASSISTANT DISCREPANCY
======================================================================

There is a real current failure mode that must be preserved in the roadmap as evidence.

At times, Wyze cameras are:

VISIBLE AND WORKING IN THE WYZE APP

while:

NOT AVAILABLE / NOT DISPLAYING CORRECTLY IN HOME ASSISTANT

This is currently happening with more than one Wyze camera.

Do NOT troubleshoot those cameras as part of this documentation-only task.

Instead, preserve the problem as an explicit future surveillance-health scenario.

Potential layers to distinguish later:

- physical camera
- power
- Wi-Fi
- DHCP/IP
- vendor cloud
- Wyze app path
- Home Assistant Wyze integration
- Home Assistant camera entity
- Secure RTSP
- go2rtc
- Frigate
- recording

The architectural requirement is:

HIOC must be capable of explaining WHY a camera is unavailable in Home Assistant even when the vendor app still works.

Do not collapse this into CAMERA_OFFLINE.

======================================================================
30. EXAMPLE WYZE MULTI-PATH STATES
======================================================================

CASE A

Wyze app:
AVAILABLE

LAN:
AVAILABLE

RTSPS:
AVAILABLE

Home Assistant:
UNAVAILABLE

Frigate:
UNAVAILABLE

Interpretation:

camera hardware/network likely healthy
Home Assistant/local integration path degraded

------------------------------------------------------------

CASE B

Wyze app:
AVAILABLE

LAN:
AVAILABLE

RTSPS:
UNAVAILABLE

Home Assistant cloud/vendor integration:
AVAILABLE

Frigate:
UNAVAILABLE

Interpretation:

camera vendor/cloud path works
local Secure RTSP service failed

------------------------------------------------------------

CASE C

Wyze app:
UNAVAILABLE

LAN:
UNAVAILABLE

Frigate:
UNAVAILABLE

Interpretation:

likely camera/power/network outage

------------------------------------------------------------

CASE D

Wyze app:
AVAILABLE

Frigate live stream:
AVAILABLE

Recording:
STALE

Interpretation:

camera can be viewed but surveillance protection has failed

======================================================================
31. EXISTING RING CAMERA ARCHITECTURE
======================================================================

Do NOT treat Ring camera support as an unknown greenfield integration.

A working Ring architecture already exists on PI5 HA and must be preserved, inventoried, and integrated into HIOC.

At the time this requirement was documented, production includes:

- official Home Assistant Ring integration
- Ring-MQTT with Video Streaming 5.9.3
- Mosquitto Broker 7.1.1
- Ring-MQTT set to automatic boot
- Mosquitto set to automatic boot
- Ring-MQTT internal RTSP/go2rtc gateway
- multiple Ring cameras in Home Assistant

Known Ring cameras include at least:

- Puerta principal
- Cochera
- Sala
- Salón

Do not store the Ring account email address anywhere in the Master Plan.

Do not store Ring authentication information, access tokens, entity proxy tokens, recording URLs, or credentials.

======================================================================
32. DUAL RING INTEGRATION MODEL
======================================================================

The existing Ring architecture has two parallel integration paths.

PATH A:
Official Home Assistant Ring integration

PATH B:
Ring-MQTT through Mosquitto

Conceptually:

                         RING CLOUD
                            |
               +------------+------------+
               |                         |
               v                         v
       Official HA Ring              Ring-MQTT
         Integration                + Mosquitto
               |                         |
               |                         +-- MQTT telemetry
               |                         +-- snapshots
               |                         +-- motion/ding
               |                         +-- battery
               |                         +-- Wi-Fi
               |                         +-- device info
               |                         +-- stream controls
               |                         +-- on-demand RTSP
               |
               +-- Live View
               +-- Last Recording
               +-- Motion events
               +-- Ding events

These overlapping paths are valuable.

HIOC should use them as partially independent observations.

======================================================================
33. PROVEN OFFICIAL RING ENTITIES
======================================================================

The Home Assistant entity registry confirms the following are owned by the official Ring integration:

camera.cochera
camera.cochera_live_view

camera.puerta_principal
camera.puerta_principal_live_view

camera.sala
camera.sala_live_view

camera.salon
camera.salon_live_view

Official Ring event entities include:

event.cochera_motion
event.puerta_principal_motion
event.puerta_principal_ding
event.sala_motion
event.salon_motion

Current entity behavior is consistent with the current Home Assistant Ring model:

camera.<name>_live_view
=
LIVE VIEW camera

camera.<name>
=
LAST RECORDING / historical recording camera using its existing legacy entity ID

Observed behavior supporting this:

- _live_view entities expose stream functionality
- plain camera entities do not expose the same stream feature
- both contain Ring video metadata
- official Ring integration currently separates live_view and last_recording behavior

If external verification is performed while updating the Master Plan, confirm this against the current Home Assistant Ring source/documentation.

Do not rename production entities merely to normalize naming.

Existing automations/dashboards may depend on current IDs.

======================================================================
34. RING PROTECT DEPENDENCY
======================================================================

Ring Protect should be modeled as a CAPABILITY DEPENDENCY.

Do not treat subscription state as basic camera health.

Official Ring Live View can operate without Ring Protect.

Official Ring Last Recording depends on Ring cloud recording/history and therefore on an appropriate Ring Protect recording plan.

Ring-MQTT also exposes two distinct video concepts:

<camera_id>_live

and:

<camera_id>_event

LIVE:
current on-demand Ring live session

EVENT:
previously recorded Ring cloud event

The event-recording path depends on Ring cloud recording / subscription.

A Ring camera can therefore be:

CAMERA HEALTHY
LIVE VIEW HEALTHY
MOTION HEALTHY
LOCAL EVENT CAPTURE HEALTHY

while:

RING CLOUD RECORDING NOT AVAILABLE

because Ring Protect is not active.

That is not a camera failure.

======================================================================
35. PROVEN RING-MQTT / MOSQUITTO ENTITIES
======================================================================

The Home Assistant entity registry proves that the following types of entities arrive through MQTT / core Mosquitto.

Known motion/ding sensors:

binary_sensor.cochera_motion
binary_sensor.puerta_principal_motion
binary_sensor.puerta_principal_ding
binary_sensor.sala_motion
binary_sensor.salon_motion

Known snapshot cameras:

camera.cochera_snapshot
camera.puerta_principal_snapshot
camera.sala_snapshot
camera.salon_snapshot

Known live-stream switches:

switch.cochera_live_stream
switch.puerta_principal_live_stream
switch.sala_live_stream
switch.salon_live_stream

Known information sensors include:

sensor.cochera_info
sensor.puerta_principal_info_2
sensor.sala_info
sensor.salon_info

Additional MQTT/Ring-MQTT telemetry already exists for:

- battery
- wireless signal
- last activity
- device info/update timestamps
- snapshot interval
- snapshot mode
- snapshot trigger
- event stream
- event selection
- live stream
- motion duration
- siren/controls where applicable
- Ring-MQTT service running state
- Ring-MQTT CPU usage
- Ring-MQTT memory usage
- Ring-MQTT version
- update availability

Prefer ingesting existing authoritative signals rather than creating duplicates.

======================================================================
36. PROVEN RING-MQTT STREAM GATEWAY
======================================================================

Ring-MQTT already exposes on-demand RTSP streams using an internal streaming bridge.

Known pattern:

rtsp://<ring-mqtt-host>:8554/<camera-id>_live

Equivalent streams exist for:

- Puerta principal
- Cochera
- Sala
- Salón

The RTSP bridge initiates a Ring live session when a client connects.

This is an on-demand bridge.

It does NOT convert the Ring camera into a native local LAN RTSP device.

Underlying video still depends on Ring's cloud infrastructure.

======================================================================
37. DO NOT USE RING AS CONTINUOUS FRIGATE SOURCE
======================================================================

Do NOT plan to configure Ring cameras as permanent 24/7 Frigate sources.

Ring cameras are event/on-demand devices.

Important limitations include:

- Ring video still traverses Ring cloud infrastructure
- live sessions are intended to be temporary
- prolonged use may create power/battery issues
- battery cameras may drain rapidly
- prolonged streaming may create thermal concerns
- while a Ring live session is active, normal Ring motion/ding behavior can be affected
- using Ring as a continuous NVR source is not the intended Ring-MQTT architecture

Therefore:

WYZE LOCAL RTSPS CAMERAS
may use continuous Frigate recording

RING CAMERAS
should use event-driven/on-demand strategies unless future evidence demonstrates another safe supported architecture

Do not force all vendors into identical recording models.

======================================================================
38. RING LOCAL RECORDING WITHOUT RING PROTECT
======================================================================

One explicit user goal is to determine whether local Ring event recording can eventually reduce or eliminate the need to pay for Ring Protect.

This is technically plausible.

Do NOT assume success.

Ring-MQTT already provides an on-demand LIVE stream that can be started without relying on cloud-recorded event playback.

A future proof of concept should determine whether Home Assistant/HIOC can:

1. receive a Ring motion/ding event
2. start the Ring-MQTT live stream
3. capture the stream locally with FFmpeg or an equivalent trusted recorder
4. store the video on the Home Assistant external media HDD
5. capture audio as well as video
6. validate the file
7. stop the Ring stream promptly
8. preserve event metadata/history
9. notify HIOC of recording success/failure

======================================================================
39. PROPOSED RING EVENT RECORDING PIPELINE
======================================================================

Conceptual architecture:

Ring camera detects motion/ding
        |
        v
Ring event reaches HA and/or Ring-MQTT
        |
        v
event-triggered recording logic
        |
        v
connect to Ring-MQTT <camera_id>_live
        |
        v
Ring-MQTT establishes Ring live session
        |
        v
FFmpeg records video + audio locally
        |
        v
file stored on HA external media HDD
        |
        v
media integrity validator
        |
        v
HIOC observation / history / protection state

Terminate the stream after the configured event window.

Do not leave Ring live streams permanently active.

======================================================================
40. IMPORTANT RING LOCAL RECORDING LIMITATION
======================================================================

Local motion-triggered Ring recording cannot begin before the triggering event reaches Home Assistant.

There is also a live-session startup delay.

Therefore locally triggered recording may miss the first seconds of an incident.

Ring Protect may provide better beginning-of-event coverage because Ring can preserve footage before the event notification reaches Home Assistant.

This difference must be measured.

Potential timestamps:

T0
physical motion/event begins, where observable

T1
Ring motion/ding event received by HA

T2
RTSP connection initiated

T3
first usable video frame received

T4
local recording successfully starts

Measure:

T1 - T0 where possible
T2 - T1
T3 - T1
T4 - T1

The security question is:

"How much of the beginning of an incident would local recording miss?"

======================================================================
41. RING RECORDING TEST MATRIX
======================================================================

When the future Ring local-recording checkpoint becomes active, test at least:

1. motion-triggered recording
2. ding-triggered recording where applicable
3. manual recording
4. video presence
5. audio presence
6. startup latency
7. MP4 integrity
8. sane duration
9. clean stream termination
10. repeated events
11. back-to-back events
12. concurrent events on multiple Ring cameras
13. Ring-MQTT restart
14. Mosquitto restart
15. Home Assistant restart
16. Internet loss
17. Ring cloud/API disruption where observable
18. storage unavailable
19. storage full/near threshold
20. battery impact
21. thermal impact where safely observable
22. impact on motion/ding event generation
23. failed stream activation
24. recovery after failed activation
25. file-integrity validation
26. missed-event rate

Do not perform unsafe destructive testing.

======================================================================
42. WIRED VS BATTERY RING CAMERAS
======================================================================

Do not assume all Ring cameras can use the same capture policy.

Battery and wired devices must be modeled separately.

Capture:

- power type
- battery level
- external power state where available
- expected availability
- reasonable event-recording duration
- battery impact
- stream-duration impact
- recovery/charging behavior

Puerta principal currently exposes battery telemetry and should be treated accordingly.

======================================================================
43. RING PROTECT REPLACEMENT DECISION
======================================================================

Do NOT recommend cancellation of Ring Protect just because local recording works once.

The future Ring local-recording architecture must pass an extended production reliability test.

Measure:

- percentage of motion events successfully recorded locally
- percentage of doorbell events successfully recorded locally
- median startup latency
- worst-case startup latency
- percent of recordings with valid video
- percent with valid audio
- corruption rate
- missed beginning-of-event duration
- cloud-related failures
- Ring-MQTT-related failures
- HA-related failures
- MQTT-related failures
- storage-related failures
- battery impact
- recovery behavior
- protection availability percentage

Then classify the result as one of:

LOCAL RECORDING CAN RELIABLY REPLACE RING PROTECT

LOCAL RECORDING CAN PARTIALLY REPLACE RING PROTECT

LOCAL RECORDING WORKS BUT SECURITY COVERAGE IS MATERIALLY WORSE

LOCAL RECORDING IS NOT RELIABLE ENOUGH FOR SECURITY USE

RING PROTECT REMAINS NECESSARY FOR THE DESIRED PROTECTION LEVEL

The conclusion must be evidence-driven.

======================================================================
44. DUAL-PATH RING HEALTH MONITORING
======================================================================

Use the official Ring integration and Ring-MQTT as partially independent observations.

CASE A

Official Ring live view:
HEALTHY

Official Ring events:
HEALTHY

Ring-MQTT:
HEALTHY

RTSP live bridge:
HEALTHY

Interpretation:
Ring surveillance paths healthy

------------------------------------------------------------

CASE B

Official Ring live view:
FAILED

Official Ring events:
FAILED

Ring-MQTT telemetry:
HEALTHY

Ring-MQTT snapshot:
HEALTHY

Interpretation:
do NOT classify physical camera offline

Likely official HA Ring integration/realtime path issue

------------------------------------------------------------

CASE C

Official Ring live view:
HEALTHY

Official Ring events:
HEALTHY

Ring-MQTT telemetry:
STALE

Ring-MQTT service:
FAILED

Interpretation:
Ring-MQTT/MQTT path failure

Camera itself may still be healthy

------------------------------------------------------------

CASE D

Official Ring live view:
HEALTHY

Ring-MQTT telemetry:
HEALTHY

Ring-MQTT RTSP:
FAILED

Interpretation:
Ring-MQTT streaming bridge failure

------------------------------------------------------------

CASE E

Official Ring:
FAILED

Ring-MQTT:
FAILED

WAN:
FAILED

LAN:
HEALTHY

Interpretation:
likely upstream Internet/Ring cloud dependency

Avoid duplicate camera incidents when one WAN incident explains multiple failures.

------------------------------------------------------------

CASE F

Official Ring live view:
HEALTHY

Ring-MQTT RTSP:
HEALTHY

Local event recording:
FAILED

Interpretation:
camera is healthy but protection is degraded

======================================================================
45. OFFICIAL RING EVENTS VS MQTT EVENTS
======================================================================

Two event paths already exist.

Official Ring:

event.cochera_motion
event.puerta_principal_motion
event.puerta_principal_ding
event.sala_motion
event.salon_motion

Ring-MQTT:

binary_sensor.cochera_motion
binary_sensor.puerta_principal_motion
binary_sensor.puerta_principal_ding
binary_sensor.sala_motion
binary_sensor.salon_motion

Use this redundancy for cross-path validation.

Example:

Official Ring event occurs
but Ring-MQTT equivalent does not

or:

Ring-MQTT event occurs
but official Ring event does not

These should become observations.

However:

Do not infer failure merely because no motion occurred for a long period.

A quiet camera may legitimately have no events.

Use corroborating active health signals.

======================================================================
46. RING-MQTT SERVICE HEALTH
======================================================================

Ring-MQTT itself should become a monitored infrastructure dependency.

Existing HA telemetry already includes:

- running state
- CPU usage
- memory usage
- current version
- newest version/update state

Also consider:

- app/container health
- Ring authentication health
- MQTT broker connectivity
- go2rtc/RTSP gateway availability
- stream activation state
- stream activation failure
- abnormal restart frequency
- abnormal CPU/memory behavior

Differentiate:

RING_MQTT_SERVICE_FAILURE

from:

INDIVIDUAL_RING_CAMERA_FAILURE

======================================================================
47. MOSQUITTO DEPENDENCY
======================================================================

Mosquitto is already a production dependency for Ring-MQTT.

It may also become important for Frigate/HIOC monitoring.

Represent it explicitly in the dependency graph.

Conceptually:

Ring camera
   ->
Ring cloud
   ->
Ring-MQTT
   ->
Mosquitto
   ->
HA MQTT entities
   ->
HIOC

A Mosquitto outage can make multiple cameras appear unhealthy at once.

HIOC should correlate this before creating duplicate incidents.

======================================================================
48. CURRENT RING SNAPSHOT PARTIAL FAILURE
======================================================================

Current Ring-MQTT production logs demonstrate a useful real-world partial failure.

Cochera:

interval snapshots are being retrieved successfully.

Sala:

snapshots repeatedly report unavailable.

Salón:

snapshots repeatedly report unavailable.

At the same time:

Ring-MQTT continues publishing device information and stream metadata for Sala and Salón.

Preserve this as evidence that camera health is multi-dimensional.

Possible state:

DEVICE:
HEALTHY

MQTT:
HEALTHY

LIVE STREAM:
HEALTHY

SNAPSHOT:
FAILED

This should generally be DEGRADED rather than OFFLINE.

When the future surveillance-health checkpoint is active, investigate whether this is caused by:

- Ring motion capture settings
- Ring mode configuration
- camera model capability
- Ring-MQTT configuration
- cloud behavior
- permissions
- integration behavior
- another known Ring limitation

Do not troubleshoot this during the documentation-only task.

======================================================================
49. RING PROTECTION STATUS EXAMPLE
======================================================================

Example dashboard state:

PUERTA PRINCIPAL

Physical/device health       HEALTHY
Network                      HEALTHY
Ring cloud path              HEALTHY
Official Ring integration    HEALTHY
Official Live View           HEALTHY
Official Ring events         HEALTHY
Ring-MQTT                    HEALTHY
Mosquitto                    HEALTHY
Snapshot                     HEALTHY
On-demand RTSP               HEALTHY
Local event recording        HEALTHY
Ring cloud recording         PROTECTED
Ring Protect                 ACTIVE

If Protect is later removed:

Physical/device health       HEALTHY
Official Live View           HEALTHY
Official Ring events         HEALTHY
Ring-MQTT                    HEALTHY
On-demand RTSP               HEALTHY
Local event recording        HEALTHY
Ring cloud recording         NOT AVAILABLE
Ring Protect                 NOT ACTIVE

The camera should not become red merely because the paid cloud recording capability is absent.

======================================================================
50. CAMERA ECOSYSTEM INVENTORY
======================================================================

Before broad surveillance implementation, create an authoritative inventory.

For every camera capture:

- HIOC asset ID
- friendly name
- physical location
- vendor
- model
- MAC
- expected/reserved IP
- current IP
- power type
- Wi-Fi/Ethernet
- Wi-Fi network
- vendor application
- HA integration
- local streaming capability
- RTSP/RTSPS capability
- Frigate-compatible
- Frigate ID
- Ring-MQTT ID
- official Ring entities
- MQTT entities
- expected audio
- expected video
- motion capability
- AI capability
- continuous recording expectation
- event recording expectation
- recording destination
- retention
- cloud dependency
- subscription dependency
- expected availability
- criticality

Do not store credentials.

======================================================================
51. RECORDING POLICY BY CAMERA TYPE
======================================================================

Different camera ecosystems require different recording strategies.

CATEGORY A:
LOCAL CONTINUOUS CAMERA

Example:
Wyze Secure RTSPS camera through Frigate

Desired:
- continuous recording
- configured retention
- motion processing
- future AI
- recording-integrity validation

CATEGORY B:
CLOUD / EVENT CAMERA

Example:
Ring

Desired may include:
- live-view health
- event health
- local event capture
- snapshots
- cloud recording awareness
- subscription awareness

CATEGORY C:
MONITOR-ONLY CAMERA

If no reliable recording path exists:

HIOC should still monitor:
- availability
- integration health
- network state
- battery/power
- event path
- vendor/cloud dependencies

Do not imply equal protection across all categories.

======================================================================
52. CROSS-SYSTEM FAILURE CORRELATION
======================================================================

HIOC should identify likely root cause across multiple cameras.

Examples:

MULTIPLE WYZE CAMERAS DISAPPEAR FROM HA
but vendor app remains healthy

Possible root cause:
Home Assistant integration or local stream path

------------------------------------------------------------

ALL FRIGATE CAMERAS FAIL
but cameras remain reachable

Possible root cause:
Frigate/go2rtc

------------------------------------------------------------

ONE CAMERA FAILS EVERYWHERE

Possible root cause:
camera/power/network

------------------------------------------------------------

ALL RING CAMERAS FAIL IN HA
while local Frigate cameras remain healthy

Possible root cause:
Ring cloud/integration/MQTT

------------------------------------------------------------

ALL CLOUD-DEPENDENT CAMERAS FAIL
while local streams remain healthy

Possible root cause:
Internet/WAN

------------------------------------------------------------

ALL RECORDINGS STOP
while streams remain healthy

Possible root cause:
storage/recording subsystem

Avoid opening one incident per downstream symptom when a common dependency explains the failure.

======================================================================
53. DEPENDENCY GRAPH
======================================================================

Eventually represent surveillance dependencies in HIOC.

Example for Wyze:

Camera Parque
   ->
Wi-Fi/LAN
   ->
Pi-hole DHCP reservation
   ->
expected IP
   ->
RTSPS service
   ->
Frigate embedded go2rtc
   ->
Frigate ffmpeg
   ->
recording
   ->
external HDD

Motion:
video stream
   ->
Frigate motion pipeline

Future AI:
video stream
   ->
Frigate
   ->
detector / accelerator

Example for Ring:

Ring camera
   ->
Wi-Fi/Internet
   ->
Ring cloud
   ->
Official Ring integration

and independently:

Ring camera
   ->
Ring cloud
   ->
Ring-MQTT
   ->
Mosquitto
   ->
HA MQTT entities

and for local recording:

Ring-MQTT
   ->
on-demand RTSP
   ->
FFmpeg capture
   ->
external HDD
   ->
media validation

======================================================================
54. INCIDENT MODEL
======================================================================

Use HIOC's existing incident architecture.

Do NOT create an isolated surveillance incident engine.

Conceptual incident classes may include:

CAMERA_OFFLINE
CAMERA_NETWORK_UNAVAILABLE
CAMERA_ADDRESS_MISMATCH
CAMERA_STREAM_UNAVAILABLE
CAMERA_AUTH_FAILURE
CAMERA_STREAM_STALLED
CAMERA_VIDEO_MISSING
CAMERA_AUDIO_MISSING

HOME_ASSISTANT_CAMERA_INTEGRATION_FAILED

FRIGATE_UNAVAILABLE
FRIGATE_CAMERA_PIPELINE_FAILURE
FRIGATE_RECORDING_FAILURE
FRIGATE_REPEATED_RESTART

GO2RTC_SOURCE_FAILURE
GO2RTC_CONSUMER_FAILURE

RECORDING_STALE
RECORDING_CORRUPT
RECORDING_AUDIO_MISSING

CAMERA_MOTION_PIPELINE_FAILURE
CAMERA_OBJECT_DETECTION_FAILURE

SURVEILLANCE_STORAGE_UNAVAILABLE
SURVEILLANCE_STORAGE_READ_ONLY
SURVEILLANCE_STORAGE_LOW
SURVEILLANCE_STORAGE_CRITICAL

CAMERA_RECONNECT_INSTABILITY

RING_INTEGRATION_UNAVAILABLE
RING_MQTT_UNAVAILABLE
RING_CLOUD_PATH_UNAVAILABLE
RING_LIVE_VIEW_UNAVAILABLE
RING_EVENT_PATH_UNAVAILABLE
RING_SNAPSHOT_UNAVAILABLE
RING_LOCAL_RECORDING_FAILED

These names are conceptual.

Review the existing HIOC taxonomy and generalize/reuse existing incident types where practical.

======================================================================
55. SEVERITY MODEL
======================================================================

Severity should reflect surveillance impact.

Conceptual examples:

INFO

- brief reconnect
- automatic recovery
- no meaningful recording loss

WARNING

- short stream interruption
- snapshot capability degraded
- motion-processing failure
- audio missing while video continues
- unexpected IP change without recording loss
- storage capacity trending low
- Ring integration path failed but alternate path still works

CRITICAL

- expected camera unavailable
- no new recording beyond critical threshold
- Frigate unavailable
- recording filesystem missing
- storage read-only
- recording corrupt
- significant footage gap
- camera video pipeline dead
- local Ring recording repeatedly fails when it is the only active recording protection

Align this with HIOC's existing severity semantics.

======================================================================
56. ALERT DEBOUNCE / GRACE PERIODS
======================================================================

Do not alert on every one-second interruption.

Use HIOC lifecycle/debounce semantics.

Conceptually:

brief interruption:
observation / transient degradation

sustained stream failure:
incident

no valid recording for an unacceptable interval:
critical recording incident

Frigate may automatically restart ffmpeg when it detects recording problems.

HIOC should observe these recoveries without producing unnecessary notification storms.

Thresholds must be configurable and validated experimentally.

======================================================================
57. NOTIFICATION REQUIREMENTS
======================================================================

Use HIOC's normal Home Assistant phone-notification architecture.

Notifications should be actionable.

Include where appropriate:

- camera friendly name
- physical location
- severity
- failure type
- start time
- duration
- recording affected yes/no
- live view affected yes/no
- video affected yes/no
- audio affected yes/no
- likely root cause when sufficiently certain
- recommended action
- upstream dependency if relevant

Example:

"Camera Parque recording critical: no valid recording segment for 2m 14s. RTSPS stream is also unavailable."

Example:

"Camera Parque degraded: video recording continues but recent files contain no audio track."

Example:

"Ring Cochera degraded: official Ring live view unavailable, but Ring-MQTT and snapshots remain healthy."

Do not expose:
- camera credentials
- RTSP URLs with credentials
- tokens
- Ring recording URLs
- Ring account identifiers

======================================================================
58. RECOVERY NOTIFICATIONS
======================================================================

Notify on meaningful recovery.

Include:

- what recovered
- outage duration
- whether recovery was automatic
- whether recording resumed
- estimated/measured footage gap
- whether all health dimensions are restored

Example:

"Camera Parque recording restored after 4m 32s. Continuous recording resumed. Estimated footage gap: 4m 10s."

Avoid recovery notifications for trivial one-second events.

======================================================================
59. AUTOMATIC REMEDIATION POLICY
======================================================================

Initial HIOC surveillance behavior should be:

OBSERVE
CLASSIFY
ALERT
RECORD HISTORY

Do NOT automatically:

- reboot cameras
- restart Home Assistant
- restart Frigate
- restart Ring-MQTT
- restart network equipment
- power-cycle devices
- modify DHCP
- remount storage

unless a separately approved future remediation policy exists.

HIOC should record when Frigate's own built-in watchdog performs automatic recovery.

Future controlled remediation may be a separate checkpoint.

======================================================================
60. DASHBOARD INTEGRATION
======================================================================

Surveillance health must appear in the SAME HIOC dashboard.

Do not require routine checking of Frigate/Ring/Wyze interfaces.

Create or plan a unified Surveillance / Cameras area.

High-level view should answer:

ALL CAMERAS HEALTHY

1 CAMERA DEGRADED

1 RECORDING CRITICAL

RING CLOUD DEGRADED

FRIGATE DEGRADED

STORAGE WARNING

For each camera, show only the most important information at top level.

Use drill-down for detailed telemetry.

======================================================================
61. PER-CAMERA DASHBOARD DATA
======================================================================

Potential fields:

- friendly name
- physical location
- vendor
- overall health
- protection status
- expected availability
- network health
- expected IP
- actual IP
- stream health
- video health
- audio health
- camera FPS
- reconnect state
- latest recording age
- recording health
- media-integrity result
- motion pipeline
- object detection status
- storage dependency
- active incident
- last outage
- last successful health check

Frigate-specific detail may include:

- go2rtc producer
- go2rtc consumer
- bytes/packets progressing
- Frigate role status
- ffmpeg status

Ring-specific detail may include:

- official Live View
- official Ring event path
- Ring-MQTT status
- Mosquitto status
- snapshot health
- Ring-MQTT RTSP activation
- battery
- Wi-Fi signal
- Ring Protect state
- cloud recording capability
- local event-recording capability

Do not show unsupported fields as failures.

Use N/A where appropriate.

======================================================================
62. HISTORICAL DATA
======================================================================

Retain enough surveillance history to answer:

- camera availability over 7/30/90 days
- recording availability
- footage gap duration
- number of reconnects
- Frigate ffmpeg restarts
- stream instability
- Ring-MQTT restarts
- integration outages
- storage incidents
- audio-loss events
- media-integrity failures
- local Ring recording success rate
- Ring event capture latency
- battery impact
- unexpected IP changes

Avoid retaining unnecessary high-frequency raw telemetry forever.

Use HIOC's normal aggregation/downsampling strategy.

======================================================================
63. DERIVED RELIABILITY METRICS
======================================================================

Consider metrics such as:

- camera availability %
- live-view availability %
- recording availability %
- protection availability %
- total recording-gap duration
- reconnect count
- MTBF
- MTTR
- latest recording age
- media-validation success %
- Ring local-event capture success %
- median Ring event start latency
- worst-case Ring event start latency
- storage consumption/day
- projected retention
- integration uptime

Use actual observations, not guesses.

======================================================================
64. WATCHDOG CADENCE
======================================================================

Use layered checks.

FAST CHECKS

Examples:
- Frigate availability
- camera FPS
- go2rtc traffic progression
- recording freshness
- Ring-MQTT availability
- Mosquitto availability
- critical stream state

MEDIUM-CADENCE CHECKS

Examples:
- storage state
- file progression
- camera service reachability
- IP-address consistency
- Ring snapshot health
- integration entity freshness
- reconnect frequency

DEEP PERIODIC CHECKS

Examples:
- ffprobe newest completed recording
- validate audio/video tracks
- verify decodability
- verify expected codec
- validate Ring locally recorded event file
- calculate storage consumption trend

Choose exact timing during implementation based on performance and failure-detection requirements.

======================================================================
65. SECURITY / SECRET HANDLING
======================================================================

Camera and integration data can expose sensitive runtime values.

Never expose or persist:

- RTSP passwords
- RTSPS passwords
- authenticated stream URLs
- Ring account email
- Ring refresh/auth tokens
- Home Assistant access tokens
- camera proxy access tokens
- entity_picture query tokens
- video_url values
- recording URLs
- MQTT passwords
- API tokens

Home Assistant Ring camera entities expose sensitive runtime attributes.

The surveillance collector should use:

DENY BY DEFAULT

Only explicitly approved attributes should be retained.

Do not dump raw camera entity attributes into:

- HIOC logs
- Git
- Master Plan
- incidents
- Evidence Reports
- dashboards

======================================================================
66. TESTING REQUIREMENTS
======================================================================

When the future surveillance checkpoint becomes active, deliberately test failures.

For local/Frigate cameras, test at minimum:

1. camera powered off
2. camera Wi-Fi/network unavailable
3. camera still pingable but RTSPS unavailable
4. authentication failure
5. stream stall
6. Frigate app stopped
7. go2rtc producer lost
8. Frigate consumer lost
9. ffmpeg capture failure
10. recording files stop advancing
11. recording directory unavailable
12. storage near threshold
13. safe read-only simulation if possible
14. corrupt media file
15. missing video
16. missing audio
17. motion pipeline failure
18. future detector failure
19. camera IP changes
20. camera returns/recovery
21. notification delivery
22. incident resolution
23. dashboard state transition
24. historical data correctness

For Ring, use the separate Ring test matrix described above.

Use reversible/synthetic fault injection where possible.

======================================================================
67. SUCCESS CRITERIA
======================================================================

This capability is NOT complete merely because sensors exist.

Completion requires evidence that HIOC can:

- detect physical camera/network loss
- detect local stream loss
- detect integration-specific failures
- distinguish vendor-app availability from Home Assistant availability
- detect loss of Frigate frames
- detect actual recording failure
- detect stale recordings
- detect corrupt recordings
- detect missing audio
- detect storage failure
- detect storage capacity risk
- detect camera IP mismatch
- detect Ring-MQTT failure separately from Ring camera failure
- detect Mosquitto dependency failure
- detect Ring official-integration failure separately from Ring-MQTT
- distinguish snapshot degradation from full Ring camera outage
- validate locally captured Ring event video/audio
- notify the user
- detect recovery
- resolve incidents correctly
- preserve historical evidence
- avoid exposing secrets
- avoid notification storms
- scale to additional cameras
- integrate into the unified HIOC dashboard

Additional completion criteria:

- permanent cameras have validated DHCP reservations where appropriate
- unexpected IP changes are detected
- Wyze-app-available / HA-unavailable scenarios are classified
- Ring cameras appear in the same surveillance model as Frigate cameras
- Ring local recording limitations are documented and production-tested
- the dashboard clearly shows each camera's protection level
- HIOC can answer whether usable footage is reasonably expected if an incident happens now

======================================================================
68. RELATIONSHIP TO EXISTING HIOC ROADMAP
======================================================================

This work relates to already planned HIOC concepts including:

- asset-centric living digital twin
- expected availability
- permanent IoT monitoring
- observation vs stale vs degraded vs offline
- canonical IP correctness
- Pi-hole DHCP ingestion
- dependency graph
- automatic service relationships
- failure propagation
- infrastructure topology
- historical trends
- predictive recommendations
- notification semantics
- repository/deployment hygiene
- retention/archive policy
- infrastructure backup/disaster recovery

Do not create competing implementations.

Use the existing architecture.

======================================================================
69. LIKELY ARCHITECTURAL PREREQUISITES
======================================================================

Do not blindly use this order.

Review the current Master Plan and choose the correct placement.

Potential prerequisites may include:

1. asset identity correctness
2. canonical IP correctness
3. Pi-hole DHCP/lease correctness
4. expected-availability semantics
5. health/incident lifecycle
6. notification framework
7. dependency model
8. surveillance asset inventory
9. DHCP reservation/address hardening
10. local/Frigate camera health
11. recording integrity
12. Ring dual-path health
13. Ring local-event recording POC
14. media validation
15. unified dashboard
16. historical reliability analytics
17. Ring Protect replacement decision
18. optional future controlled remediation

The Master Plan must decide the final sequencing.

======================================================================
70. POSSIBLE PHASE STRUCTURE
======================================================================

If this capability is too large for one checkpoint, consider a phased structure such as:

SURVEILLANCE A
Asset inventory and identity

SURVEILLANCE B
Camera address/DHCP hardening

SURVEILLANCE C
Frigate/local-stream health foundation

SURVEILLANCE D
Recording freshness and media integrity

SURVEILLANCE E
Ring dual-path health model

SURVEILLANCE F
Ring event-driven local recording proof of concept

SURVEILLANCE G
Incidents and notifications

SURVEILLANCE H
Unified dashboard

SURVEILLANCE I
Historical reliability and protection metrics

SURVEILLANCE J
Ring Protect replacement decision

SURVEILLANCE K
Optional controlled remediation

Use different names/numbers if the Master Plan structure requires it.

Do not create unnecessary phases.

======================================================================
71. DOCUMENTATION DELIVERABLE
======================================================================

Update docs/HIOC_MASTER_PLAN.md so this requirement survives chat history.

Document:

- why surveillance monitoring is needed
- the operational risk being solved
- heterogeneous camera architecture
- Frigate architecture
- Wyze Secure RTSP path
- Ring dual-integration architecture
- Ring-MQTT
- Mosquitto dependency
- Ring Protect capability dependency
- recording-integrity requirements
- storage health
- audio/video validation
- camera-IP/DHCP hardening
- vendor-app vs HA discrepancies
- expected availability
- protection status
- incidents
- notifications
- recovery
- dashboard integration
- asset model
- dependency graph
- historical metrics
- test requirements
- prerequisites
- explicit deferrals
- success criteria

Also update any relevant:

- Implementation Status
- Future Capabilities
- Architecture
- Decisions
- Dependencies
- Roadmap
- Security
- Validation

sections needed to keep the Master Plan internally consistent.

======================================================================
72. IMPORTANT DEFERRALS
======================================================================

Do NOT implement as part of this planning task:

- MQTT changes
- Frigate config changes
- new HA sensors
- automations
- watchdog code
- notification code
- dashboard cards
- camera restarts
- Ring recording scripts
- FFmpeg recording
- Ring-MQTT changes
- Ring Protect changes
- DHCP reservations
- Pi-hole changes
- Frigate object detection
- hardware acceleration
- Ring snapshot troubleshooting
- Wyze integration troubleshooting
- camera IP migrations
- storage fault injection

This request is documentation / roadmap planning only.

======================================================================
73. STOP CONDITION
======================================================================

After the Master Plan planning/documentation change is completed:

STOP.

Do not begin implementation simply because the roadmap entry exists.

Provide:

1. Exact roadmap/checkpoint placement chosen.
2. Why that placement is architecturally appropriate.
3. Summary of all Master Plan changes.
4. Dependencies/prerequisites identified.
5. Existing HIOC work this integrates with.
6. Any conflicts/overlap discovered.
7. Explicit deferred work.
8. Commit hash.
9. Push confirmation.
10. Clean working tree confirmation.
11. Standard HIOC Evidence Report.

The Evidence Report should include:

- deployment/documentation result
- intended behavior
- invariant/governance checks
- warnings
- PASS/FAIL

The final result should leave HIOC with a clear future surveillance roadmap while preserving the current active project sequence unchanged.
```
<!-- ORIGINAL_SURVEILLANCE_SPECIFICATION_END -->


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
Future surveillance remains within PE-10 and must not reopen completed DHCP ingestion or Canonical Address Selection Hardening. Camera addressing sub-checkpoints and unresolved historical-identity/local-address decisions remain separately governed; no surveillance implementation or current-sequence change is authorized.

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
Future surveillance camera policy extends this same Asset-centric model; it does not claim criticality, expected availability, recording/subscription policy or maintenance fields are already accepted PE-2.1 fields.

### Roadmap Dependencies

- Stable identity and passive discovery are foundational to operator asset enrichment.
- Asset classification must exist before aggressive archival can be safe.
- Expected availability must be defined before disappearance can be treated as failure.
- The improved dependency graph, automatic service relationships, failure propagation visualization, and infrastructure topology become more meaningful after assets and services are identified.
- Historical infrastructure trends and predictive recommendations depend on reliable identity, asset classification, relationships, and retained history.

The asset-centric vision expands the meaning of future work; it does not replace or reorder any existing phase or capability.
Surveillance consumes stable identity/Asset policy and PE-7/PE-8/PE-9 through PE-10. Recording assurance requires actual media/storage evidence; Ring local capture and subscription replacement require separate experiment/decision gates. Retention follows Asset policy, notifications reuse shared semantics, and recovery follows separate backup/DR/cold-boot governance. No future item is promoted to the current next task.

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

## PE-7.3 Windows guarded PI3 delivery transaction preparation

Classification: CURRENT — bounded live HA Dashboard-shape correction; native qualification pending.
PE70_STATUS=COMPLETE/PASS; PE71_STATUS=COMPLETE/PASS; PE72_STATUS=COMPLETE/PASS.
PE6_STATUS=COMPLETE/PASS; PE7_STATUS=IN_PROGRESS; PE73_STATUS=IN_PROGRESS.
PE73_COMPLETE=FALSE; PE74_STATUS=NOT_AUTHORIZED; CODEX_PRODUCTION_ACCESS=FALSE.
Accepted OPERATOR_SUPPLIED filesystem qualification remains PASS and is not repeated.
New OPERATOR_SUPPLIED PI5 receipt at5fc1560a4be75e509e351eaf976364ed9bec62f1:
published source SHA verification PASS; authenticated Supervisor proxy/admin read-only
discovery PASS; HIOC integration absent/inactive; Lovelace resource mode storage.
DASHBOARD_SCHEMA_OR_LIMIT stopped discovery before any Dashboard results; mutation
false; exit1. Actual returned config type/shape/count is not present in that receipt.
It does not establish a malformed Dashboard or prove a particular strategy was used.
Core2026.10.4 returns raw stored Lovelace config; its pinned frontend20260930.5
supports static views OR a strategy. The old qualifier wrongly treated every response
as a static views list and a local32-view cap as a global discovery requirement.
The correction reports fixed-name type/presence/count diagnostics, preserves other
valid Dashboards, and never generates or selects a view. Static scan budget256 is
explicitly local; larger configs report count/omission, not an HA schema defect.
Optional path/cards/sections and generated views remain subject to the unchanged
publisher's actual additive-target requirements; nothing is filled in or migrated.
Unknown catalog rows/default source, shadowed default, legacy resources, auth or
transport failures retain fail-closed resource/qualification gates. Successful null
is not config_not_found. Partial choices survive later failures; private contents do
not enter the report. No .storage, service/write API, target selection or activation.
FOCUSED_NATIVE_VALIDATION=81_RUN_81_PASSED_0_FAILURES_0_ERRORS_0_SKIPPED.
INDEPENDENT_FOCUSED_ACCEPTANCE=PASS_FOR_DASHBOARD_SHAPE_CORRECTION_PUBLICATION.
Existing104 delivery passes remain supported by unchanged delivery/assessment/tests.
13 PI3 delivery,six HA source,39 current successor,449 protected identities verify;
contract,amendment,executive instruction,PI3 evidence and filesystem PASS preserved.
Trust/private files/SPKI/independent ACL, fresh cross-host disabled/exclusive guards,
actual live/local proof and approved target/backup remain required before delivery.
Next action: one operator-run PI5 read-only qualifier bound to this new source SHA/
commit; retain sanitized report and immediate exit status, then stop.
See [Dashboard-shape correction evidence](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-73-live-dashboard-shape-correction).

### Historical initial live API qualification preparation snapshot

Classification: HISTORICAL SNAPSHOT — accepted PI5 filesystem qualification; bounded live API discovery preparation.
PE70_STATUS=COMPLETE/PASS; PE71_STATUS=COMPLETE/PASS; PE72_STATUS=COMPLETE/PASS.
PE6_STATUS=COMPLETE/PASS; PE7_STATUS=IN_PROGRESS; PE73_STATUS=IN_PROGRESS.
PE73_COMPLETE=FALSE; PE74_STATUS=NOT_AUTHORIZED; CODEX_PRODUCTION_ACCESS=FALSE.
OPERATOR_SUPPLIED filesystem result PASS_READ_ONLY_FILESYSTEM_IDENTITY_QUALIFICATION,
exit0, source da630dd9cac20b784a6b433de614bfe323d4576f is accepted, not repeated.
PI5 HA192.168.100.251 HAOS/Core2026.10.4; Terminal/Core0:0; /homeassistant and
Core/config have matching actual filesystem identities/security/namespaces/process.
Required existing directories pass; absent hioc_operator is expected; no mutation.
Installed public source supports Lovelace storage/config, WS context/service response.
New fixed read-only API qualifier uses only the Terminal app's existing supported
Supervisor Core WebSocket proxy authentication, if already permitted. Root is not
HA authorization. Actual admin/current_user is verified; proxy admin is not a human
PE-7 editing actor. No token prompt, extraction, creation, logging or persistence;
only the normal internal authentication handshake receives the existing app token.
Missing/denied permission blocks and names existing browser-admin login as fallback.
Read-only dashboard catalog/config exports report bounded titles/paths/view choices
and resource fingerprints/conflicts, not cards, URLs/query secrets or credentials.
No target selected, duplicate dashboard, YAML migration, .storage access or API save.
Potential legacy-resource lazy import is refused before resources/list; an unprovable
default-source binding blocks rather than allowing a read-side configuration write.
HA integration absence is inactive, not unsafe. HA API observations cannot prove
fresh cross-host evaluator/scheduler/manual-caller exclusion; those guards remain
unknown/false. /local source capability is accepted; the actual route is not inferred
from an absent editor/404. Native delivery remains blocked pending the live guards,
an explicit compatible target, private full API export/backup and actual trust.
Existing strict trust_preflight remains mandatory before Delivery.prepare: real
certificate/assertion identities, private-file security, SPKI and independent ACL.
No trust exemption, issuance, activation, deployment or PE-7.4 authorization.
LIVE_QUALIFIER_IMPLEMENTATION=PASS; FOCUSED_NATIVE_VALIDATION=163_RUN_163_PASSED_0_FAILURES_0_ERRORS_0_SKIPPED.
INDEPENDENT_FOCUSED_ACCEPTANCE=PASS_FOR_BOUNDED_READ_ONLY_REPOSITORY_PUBLICATION.
13 PI3 delivery, six HA source,39 current successor and449 protected identities
verify. Existing delivery/assessment, controller/provider, contract, amendment,
executive instruction, completed PI3 deployment and historical evidence unchanged.
Next action: one operator-run PI5 live read-only API qualification bound to the new
published tool SHA/commit; retain sanitized receipt/exit status and stop.
See [live API qualification evidence](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-73-live-api-dashboard-and-disabled-role-qualification).

### Historical PID-namespace preparation snapshot

Classification: HISTORICAL SNAPSHOT — HA OS PID-namespace preflight correction; qualification pending.
PE70_STATUS=COMPLETE/PASS; PE71_STATUS=COMPLETE/PASS; PE72_STATUS=COMPLETE/PASS.
PE6_STATUS=COMPLETE/PASS; PE7_STATUS=IN_PROGRESS; PE73_STATUS=IN_PROGRESS.
PE73_COMPLETE=FALSE; PE74_STATUS=NOT_AUTHORIZED; CODEX_PRODUCTION_ACCESS=FALSE.
OPERATOR_SUPPLIED PI5 preflight at2d2ecf5b95531b2c514cc4a889aa358f9fc27365
verified source identity, selected/homeassistant, observed Core0:0, no directory
failures, integration absent and no mutation. Docker host PID731186 was not visible
in Terminal/proc: stat/status/cgroup/ns/user/root all ENOENT2. This is namespace
visibility evidence, not a filesystem-security failure or unsafe-directory finding.
The corrected qualifier never opens a Docker host PID in Terminal/proc. One fixed,
noninteractive read-only Docker exec runs stdlib metadata code in the exact Core
container under the observed Core UID/GID. It finds namespace-local Core PID, checks
credentials/user mapping/birth and opens actual Core config objects with NOFOLLOW.
Device/inode/owner/group/mode, absence and ACL checks must agree with Terminal's
secure/homeassistant proof. No mount-string-only admission, shell, extra privileges,
host PID mode, container reconfiguration or persistent service. Failure blocks.
The Core label and optional public-source location now follow the source-supported
Core layout; no exact HA version gate or production identity is invented.
FOCUSED_PID_NAMESPACE_CORRECTION=133_RUN_133_PASSED_0_FAILURES_0_ERRORS_0_SKIPPED.
INDEPENDENT_FOCUSED_ACCEPTANCE=PASS_FOR_REPOSITORY_PUBLICATION. No runtime mutation
or native delivery readiness is claimed. Existing publisher/transaction code is
unchanged.13 PI3,39 successor,449 protected and six HA source identities verify.
Trust, backups, interruption recovery, disabled behavior, runtime independence and
persistent-state isolation remain. All prior PI3/PI5 evidence retains its authority.
Next action: operator-run one consolidated read-only PI5 qualifier bound to this
published correction's exact source SHA/commit. No installation/activation authority.
See [PID-namespace correction evidence](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-73-core-pid-namespace-qualification-correction).

### Historical accepted HA preflight preparation snapshot

Classification: HISTORICAL SNAPSHOT — HA OS preflight prerequisite correction; native qualification pending.
PE70_STATUS=COMPLETE/PASS; PE71_STATUS=COMPLETE/PASS; PE72_STATUS=COMPLETE/PASS.
PE6_STATUS=COMPLETE/PASS; PE7_STATUS=IN_PROGRESS; PE73_STATUS=IN_PROGRESS.
PE73_COMPLETE=FALSE; PE74_STATUS=NOT_AUTHORIZED; CODEX_PRODUCTION_ACCESS=FALSE.
The accepted111-test HA correction and completed OPERATOR_SUPPLIED PI3 deployment
evidence are preserved. This bounded follow-up resolves fresh-install prerequisites.
Missing custom_components/hioc_operator is observed as absence, not an installation
failure. Only that fixed public directory0755 and missing private backups0700 may
be created. Private durable intent precedes creation; exact identities/readback and
Core-visible proof follow. Existing directories are never chmod/chowned or adopted.
Missing backups uses a fixed exclusive private bootstrap intent before mkdir, not
manual directory setup. Uncertain creation remains pending; no retry or auto recovery.
Explicit recovery removes only the empty, exact created HIOC directory; backup and
transaction evidence remain preserved. Missing custom_components/www remains a real
parent prerequisite. HA Core need not traverse private publisher backup storage.
Host PID mode is not a required configuration. Existing proc visibility must prove
the exact Core-container PID, process birth, credentials, user namespace and actual
Core-visible filesystem objects. Matching mount paths or archive metadata alone
are insufficient. Missing/hidden proof blocks; no new privileges, exec, namespace
entry or container change is authorized. Production support remains UNKNOWN.
FOCUSED_PREREQUISITE_CORRECTION=125_RUN_125_PASSED_0_FAILURES_0_ERRORS_0_SKIPPED.
Synthetic Windows results do not establish native Linux filesystem qualification.
All13 PI3 delivery,39 successor and449 protected identities verify; immutable HA
payload, original contract/amendment, trust design and completed PI3 evidence remain.
Disabled behavior, backups, whole-process authority, interruption evidence, runtime
independence and persistent-state isolation are preserved. No installation or Git
publication occurs here. Live HA/Dashboard/trust and native filesystem evidence
remain unverified. PE-7.3 IN_PROGRESS; PE-7.4 NOT_AUTHORIZED.
INDEPENDENT_REPOSITORY_ACCEPTANCE=PASS. The exact code/test candidate was reviewed
against all15 mandatory acceptance gates;125 focused results match unchanged bytes,
and25 preservation checks pass. Native installation/readiness is not established.
This authorized publication records repository acceptance only; no PE-7.3 closure.
Next action: operator-run consolidated read-only PI5 qualification using the accepted
preflight; unavailable Core filesystem proof blocks delivery without a workaround.
See [the prerequisite correction evidence](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-73-preflight-prerequisite-review-and-bounded-correction).

### Historical accepted111-test HA OS correction snapshot

Classification: HISTORICAL SNAPSHOT — HA OS delivery compatibility correction; native delivery unqualified.
PE70_STATUS=COMPLETE/PASS; PE71_STATUS=COMPLETE/PASS; PE72_STATUS=COMPLETE/PASS.
PE6_STATUS=COMPLETE/PASS; PE7_STATUS=IN_PROGRESS; PE73_STATUS=IN_PROGRESS.
PE73_COMPLETE=FALSE; PE74_STATUS=NOT_AUTHORIZED; CODEX_PRODUCTION_ACCESS=FALSE.
The completed PI3 deployment evidence at2784ef31da5e4ebc0e75af19695c8cc68c3d04a1
is preserved as OPERATOR_SUPPLIED; source release1c07932bd43aab1eac693ea07e195a74150fe550.
The existing six-file HA candidate is corrected, not replaced. A one-shot publisher
separates observed Terminal UID/GID0:0 from actual HA Core process ownership.
Only four pinned integration/editor files and a closed private transaction file set
are writable. Public files0644 use qualified Core UID/GID; private records0600 and
transaction directory0700 use publisher0:0. No PI3 ownership exception is introduced.
Before mutation, actual Core-visible descriptor identities must match the Terminal
destination; matching Docker mount-source strings alone are insufficient. Existing
host-PID/proc visibility is required. Missing proof or required existing directories
refuses delivery; no container changes, privilege expansion or guessed owner fallback.
FOCUSED_CORRECTION=111_RUN_111_PASSED_0_FAILURES_0_ERRORS_0_SKIPPED.
Windows descriptor/ownership models are synthetic, not native Linux qualification.
All13 PI3 delivery,39 successor and449 protected identities verify. Original contract,
amendment, controller, executive instruction and PI3 evidence remain unchanged.
Whole-process authority, private backups, durable intent, single-attempt publication,
exact readback and separate unexpected-recovery authority remain mandatory. No retries,
automatic rollback or consumer release. Existing pending transactions require disposition.
Runtime code has no publisher/transaction dependency; persistent Assets, policies,
history and configuration are outside the write scope. No permanent HA version pin,
migration, trust provisioning, activation, scheduling or service operation is added.
Remaining native requirements: actual Core/mount/ownership/security qualification,
supported live HA/API and approved Dashboard/view export, disabled guard, actual trust
identities/private validation, and native filesystem behavior. None is fabricated.
Next action: operator-run the self-contained, no-prompt read-only PI5 identity preflight
in the correction evidence. This is not installation or PE-7.4 authorization.
See [the HA OS correction evidence](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-73-ha-os-delivery-compatibility-correction-and-runtime-protection).

### Historical HA delivery preparation snapshot (superseded compatibility assumptions)

Classification: HISTORICAL SNAPSHOT — HA integration/UI/trust delivery preparation candidate.
PE70_STATUS=COMPLETE/PASS; PE71_STATUS=COMPLETE/PASS; PE72_STATUS=COMPLETE/PASS.
PE6_STATUS=COMPLETE/PASS; PE7_STATUS=IN_PROGRESS; PE73_STATUS=IN_PROGRESS.
PE73_COMPLETE=FALSE; PE74_STATUS=NOT_AUTHORIZED; CODEX_PRODUCTION_ACCESS=FALSE.
The PI3 runtime deployment is a completed, independently verified sub-checkpoint,
recorded as OPERATOR_SUPPLIED production evidence and published at
2784ef31da5e4ebc0e75af19695c8cc68c3d04a1. Its source release was
1c07932bd43aab1eac693ea07e195a74150fe550. That deployment is not reopened.
A finite HA delivery procedure now reuses six immutable PE-7.1 HA artifact identities:
four integration/editor files delivered, Dashboard/package retained as references.
Supported HA resource/card registration preserves existing layout, unrelated cards,
resources and package behavior. No .storage writes or broad installer/restart.
Private before/stage/reference/trust-packet backups and durable pending intent precede
single-attempt mutation. Interrupted operations are not automatically adopted,
retried, rolled back or released. One whole-process authority; no per-operation prompts.
The trust configuration packet preserves mTLS, assertion keys and independent ACLs
and remains disabled/offline; it is not active HA/PI3 configuration or provisioned secrets.
FOCUSED_ACCEPTANCE=69_RUN_69_PASSED_0_FAILURES_0_ERRORS_0_SKIPPED.
IMPLEMENTATION=PARTIAL_NATIVE_DELIVERY_NOT_ESTABLISHED; SYNTHETIC_PROCEDURE=PASS.
The native HA connection, live guard and two-host trust-file validation bindings
are explicit inputs, not manufactured production observations. Actual PI5 roots,
ownership/filesystem capabilities, supported APIs/resources/Dashboard and trust
placement remain required observations. No native end-to-end delivery claim is made.
All13 PI3 delivery,39 successor and449 protected identities verify; original contract,
controller, amendment, executive decision and completed PI3 evidence remain preserved.
Next action: operator-run the single consolidated read-only PI5 capability/integration
assessment below to bind actual paths/capabilities; no new research/checkpoint phase.
PE-7.3 remains IN_PROGRESS; PE-7.4 remains NOT_AUTHORIZED. No activation, migration,
notifications, credentials, service restart, PI3/PI5 access or Git publication here.
See [the integrated HA preparation evidence and assessment](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-73-integrated-ha-integration-ui-and-trust-delivery-preparation).

### Historical PI3 runtime deployment evidence snapshot

Classification: HISTORICAL SNAPSHOT — accepted PI3 runtime delivery evidence.
PE70_STATUS=COMPLETE/PASS; PE71_STATUS=COMPLETE/PASS; PE72_STATUS=COMPLETE/PASS.
PE6_STATUS=COMPLETE/PASS; PE7_STATUS=IN_PROGRESS; PE73_STATUS=IN_PROGRESS.
PE73_COMPLETE=FALSE; PE74_STATUS=NOT_AUTHORIZED; CODEX_PRODUCTION_ACCESS=FALSE.
EVIDENCE_AUTHORITY=OPERATOR_SUPPLIED. Source release1c07932bd43aab1eac693ea07e195a74150fe550.
The owner reports successful interrupted-window recovery and installation: all13
artifact SHA256 identities PASS; transactionCOMMITTED/pendingNone; windowRELEASED;
original12-entry crontab restored exactly; all3 affected HIOC jobs scheduled.
cron,pihole-FTL,unbound,nut-server are reported active. Incident-engine invocation
and recent status output observed; invocation alone does not prove engine completion.
Inventory last observed at09:30 before release; no post-release inventory execution
is established. Daily platform-status at03:17 was not expected in the observed
post-release window; no post-release platform execution is claimed. No HIOC error
matches in inspected cron logs; independent assessment reports zero failed invariants.
These are supplied observations, not a Codex production inspection or universal
service-health/event-history proof. No original receipt bytes or new production
security metadata are manufactured from the owner's summary.
Runtime deployment evidence is recorded as PASS for the supplied bounded facts.
Full PE-7.3 COMPLETE/PASS is not established: the unchanged contract section13
requires guarded artifact/integration/UI/trust delivery and observed HA API/resource
capability; section7 requires supported live Dashboard/resource delivery with backup,
not repository YAML copying. Evidence for these remaining delivery obligations is
not supplied. The approved maintenance-window evidence explicitly states that the
13-file runtime step alone does not close all PE-7.3. No new acceptance gate is added.
Next action: separately authorize completion/evidence of the existing PE-7.3 HA
integration/UI/trust delivery and capability prerequisites, keeping editing/evaluator
disabled except authorized preflight. PE-7.4 bounded functional acceptance remains
later and NOT_AUTHORIZED; no monitoring, migration or notifications are authorized.
Manual-caller restrictions remain procedural; missed/cached/retained/noncooperating
callers remain residual risks, not universally excluded. Executive instruction and
fixed-process authority remain verbatim in the unchanged successor authorization
record. Unexpected recovery, rollback or material scope changes require new authority.
See [the production evidence and closure determination](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-73-pi3-runtime-deployment-evidence-and-governance-closure-determination).

### Historical approved-process recovery correction snapshot

Classification: HISTORICAL SNAPSHOT — approved-process recovery correction, 2026-10-27.
PE70_STATUS=COMPLETE/PASS; PE71_STATUS=COMPLETE/PASS; PE72_STATUS=COMPLETE/PASS.
PE6_STATUS=COMPLETE/PASS; PE7_STATUS=IN_PROGRESS; PE73_STATUS=IN_PROGRESS.
PE73_COMPLETE=FALSE; PE74_STATUS=NOT_AUTHORIZED; CODEX_PRODUCTION_ACCESS=FALSE.
Published baseline1452534a23528af96e69b9ec030f050b61bed859. Current Windows
correction is uncommitted: five existing modified paths and one focused PE-7.3
successor authorization record. No staging, commit, push or PI3/PI5 access performed.
Owner executive decision PE73_OWNER_SEQUENCE_AUTHORIZATION_20261027 is recorded
verbatim in governance/pe7/pe73-sequence-authorization.json. It explicitly supersedes
repeated human authorization inside a previously approved fixed process. Original
contract/amendment text and historical nine-prompt decisions remain preserved.
Normal deployment and the specifically approved EXCLUDED resume now run without
per-operation prompts. Fresh technical grants, material context checks, durable
intent and all transaction/recovery safeguards remain mandatory. Unexpected
recovery, rollback or materially changed scope requires new owner authorization.
The last PI3 report is OPERATOR_SUPPLIED: source1452534a, PREPARED/pendingNone,
windowEXCLUDED, three jobs excluded/nine preserved, no installed artifacts/rollback,
journal SHA256b899a8fa79bde3c6619d6abd8217d88833c414823e7888358ed7a043b766600f.
Failure NATIVE_AUTHORIZATION_CONTEXT_DRIFT is retained. Diagnostic unrelated PID
lists were incorrectly part of context equality; the code defect is reproduced.
The exact historical changed field/PID is unknown because the context pair was not supplied.
The corrected binding retains fresh completeness, boot and exact affected-process
identities while keeping unrelated PID diagnostic churn outside authority.
The bounded resume verifies the exact raw journal anchor, PREPARED/EXCLUDED phase,
all13 current target identities, all13 stages/five backups, source and scheduler
before ATTACH. It never repeats PREPARE/PRESERVE/EXCLUDE or overwrites backups.
Approved continuation: ATTACH,DRAIN,ESTABLISH,COMMIT,AUTHORIZE_RELEASE,
RESTORE_SCHEDULER,RELEASE, with automated fresh per-operation technical validation.
FOCUSED_VALIDATION=66_RUN_66_PASSED_0_FAILURES_0_ERRORS_0_SKIPPED.
All13 delivery,39 successor and449 protected identities verify; original controller,
contract, verbatim amendment and transaction algorithms unchanged. No automatic
retry, rollback, cron restoration, release or uncertain-state adoption is introduced.
The corrected command needs these exact corrected tool bytes in release-source;
the old1452534a runner fails its hash check. Publication/source delivery has not
been performed in this assignment. No production resume/closure is claimed.
See [the recovery evidence and exact operator command](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-73-approved-process-resume-and-material-context-correction--2026-10-27).

### Historical repository-preparation snapshot at85c1a4f1

Classification: HISTORICAL SNAPSHOT. PE70_STATUS=COMPLETE/PASS; PE71_STATUS=COMPLETE/PASS.
PE72_STATUS=COMPLETE/PASS; PE7_STATUS=IN_PROGRESS; PE6_STATUS=COMPLETE/PASS.
PE73_STATUS=IN_PROGRESS_REPOSITORY_PREPARATION; PE73_COMPLETE=FALSE.
PE73_REPOSITORY_IMPLEMENTATION_AUTHORIZED=TRUE; PE73_PRODUCTION_DELIVERY_AUTHORIZED=FALSE.
PE73_PI3_DELIVERY_CANDIDATE=PARTIAL; NATIVE_LIVE_COMMIT=BLOCKED_CONSUMER_COORDINATION_NOT_ESTABLISHED.
PE73_TWO_DEFECT_CORRECTION=PASS_REPOSITORY_SYNTHETIC; FOCUSED_RECHECK=ACCEPT_WITH_EXPLICIT_BLOCKER.
PE73_CONSUMER_MAINTENANCE_IMPLEMENTATION=PASS_REPOSITORY_SYNTHETIC; 104_RUN_104_PASSED.
PE73_RECOVERY_ATTACHMENT_CORRECTION=PASS_REPOSITORY_SYNTHETIC; RECOVERY_FOCUSED_RECHECK=ACCEPT_WITH_NATIVE_GATES.
PE73_NATIVE_QUALIFICATION_PREPARATION=PASS; NATIVE_QUALIFICATION=INCOMPLETE.
PE73_NATIVE_ACTION1=PASS_OPERATOR_SUPPLIED; ACTION1_EXIT_STATUS=0; COMPLETE_CALLER_COVERAGE=FALSE.
PE73_ISOLATED_DESCRIPTOR_CREATE_NOFOLLOW=PASS_OPERATOR_SUPPLIED; ISOLATED_EXIT_STATUS=0.
PE73_MODE0000_ACCESS=PASS_OPERATOR_SUPPLIED; MODE0000_EXIT_STATUS=0; DEPLOYMENT_ACCESS_RESOLVED=FALSE.
PE73_FILESYSTEM_BROKER_PROTOTYPE=PASS_EXPERIMENTAL_WINDOWS_FIXTURES; 54_RUN_54_PASSED.
BROKER_ACCESS_CONTRACT_DELTA=PROPOSED_NOT_ADOPTED; BROKER_NATIVE_INTEGRATION=NOT_AUTHORIZED.
PE73_MAINTENANCE_WINDOW_AMENDMENT=ADOPTED_OPERATOR_APPROVED_2026_10_23; ORIGINAL_CONTRACT_UNCHANGED.
WINDOW_REPOSITORY_IMPLEMENTATION=AUTHORIZED; WINDOW_NATIVE_ACCEPTANCE=NOT_ESTABLISHED; PRODUCTION=NOT_AUTHORIZED.
PE73_MAINTENANCE_WINDOW_IMPLEMENTATION=PASS_REPOSITORY_SYNTHETIC; CONTROLLER_TESTS=110_PASS; FINAL_WINDOW_TESTS=69_PASS; PRIOR_ACCEPTED_COUNTS=104_CONTROLLER_55_WINDOW; PRIOR_INTERIM_VALIDATION=110_CONTROLLER_57_WINDOW.
PE73_RELATIVE_PROCESS_DETECTION_CORRECTION=PASS_REPOSITORY_SYNTHETIC; PE73_RELATIVE_PROCESS_FOCUSED_RECHECK=ACCEPT_FOR_NATIVE_QUALIFICATION; NATIVE_QUALIFICATION=INCOMPLETE.
PE73_PUBLICATION_STABLE_SOURCE_IDENTITY=PASS_REPOSITORY_SYNTHETIC; CONTROLLER_TESTS=110_PASS; WINDOW_TESTS=69_PASS; BROKER_TESTS=54_PASS; REAL_GIT_INTEGRATION=12_PASS.
PUBLICATION_STABLE_CORRECTION_INDEPENDENT_ACCEPTANCE=NOT_PERFORMED; CORRECTION_PUBLICATION=NOT_AUTHORIZED_BY_THIS_ACTION.
Payload release remains `51398bab4e2293b578b2cdac2d0740c3738cab2f`. A clean checkout containing that immutable release in its commit ancestry can pass source integrity without a hardcoded HEAD; this does not approve tooling or authorize mutation.
See [the publication-stable identity evidence](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-73-publication-stable-source-integrity-correction).
MANUAL_CALLER_CONTROL=PROCEDURAL_ONLY; UNIVERSAL_EXCLUSION=FALSE; NATIVE_MUTATION_GATES=RETAINED.
See [the verbatim approved maintenance-window amendment](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-73-approved-maintenance-window-amendment-adoption--2026-10-23).
HISTORICAL_MAINTENANCE_REVIEW=REJECT_FRESH_PROVIDER_RECOVERY; NATIVE_MAINTENANCE_QUALIFICATION=NOT_ESTABLISHED.
The separately authorized Windows-only controller/test candidate pins the 13 PI3
artifacts to accepted release 51398bab4e2293b578b2cdac2d0740c3738cab2f.
It separates read-only preflight, private backup/staging, explicit commit, static
verification and separately authorized rollback. The actual supplied incident,
inventory and platform cron commands are retained as OPERATOR_SUPPLIED evidence.
UNLOCKED_ASSET_OR_CLASSIFICATION_CALLERS=NOT_EXCLUDED. Native live commit/rollback
remain fail-closed; no receipt, matching cron hash or three-lock assumption
establishes complete consumer coordination. Synthetic transaction tests use an
explicitly fixture-only external fence, not invented production maintenance.
See the [existing implementation evidence](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-73-guarded-pi3-delivery-transaction-repository-candidate).
No accepted PE-7.1 runtime source/contract or historical authority is changed.
No PI3/PI5 access, deployment, HA delivery, credentials, Asset migration,
monitoring or notification activation is authorized here. The prior nine-path candidate
was published at302a4e3f34f53fffb8299771d31c115e052b5400. This compatibility correction
remains uncommitted; staging, commit, push and further PI3 operations are not authorized here.
NEXT_ACTION=INDEPENDENT_ACCEPTANCE_OF_UNCOMMITTED_PUBLICATION_STABLE_SOURCE_IDENTITY_CORRECTION_BEFORE_PUBLICATION.
See the [experimental broker evidence](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-73-experimental-filesystem-broker-feasibility-candidate).
The reported process inventory has163 unresolved observations; cached modules/open readers are not excluded.
PE-7.3 remains open; PE-7.4 execution is not authorized.

## Historical PE-7.2 release-source synchronization acceptance and governance closure

Classification: CURRENT. EVIDENCE_AUTHORITY=OPERATOR_SUPPLIED for all PI3 observations.
PE70_STATUS=COMPLETE/PASS; PE71_STATUS=COMPLETE/PASS; PE72_STATUS=COMPLETE/PASS.
PE7_STATUS=IN_PROGRESS; PE6_STATUS=COMPLETE/PASS.
ACCEPTED_SOURCE_COMMIT=51398bab4e2293b578b2cdac2d0740c3738cab2f.
Deployment result: SOURCE_SYNCHRONIZATION_ONLY; no runtime delivery or activation.

The operator synchronized PI3 NUT&PIHOLE (hostname nutandpihole), source checkout
/home/jazofv1/hioc-release-source, remote
https://github.com/jorgeazofeifa-creator/hioc.git. Initially main was clean at
1477f672db00e67bc1923a667a8dd5913f183166, with no stashes and target absent locally.
After git fetch --prune origin main, origin/main was the accepted source commit;
local main was 0 ahead / 4 behind and fast-forward eligible.
git merge --ff-only 51398bab4e2293b578b2cdac2d0740c3738cab2f completed fast-forward:
40 PE-7.1 paths synchronized, HEAD at the accepted commit, tracking origin/main,
working tree clean. Local immutable Git history independently confirms ancestry
and the 40-path change set; Codex did not observe the PI3 checkout.

Operator read-only checks found /home/jazofv1/hioc present and not a Git worktree;
pi4/lib/hioc/availability.py, availability_server.py and asset_policy.py were
ABSENT under that runtime. The synchronization targeted only the source checkout.
This establishes the reported source synchronization and checked module absences,
not historical byte-for-byte runtime preservation, a comprehensive service audit,
production health or PE-7 runtime acceptance. No observation time is supplied.
See the [PE-7.2 Evidence Report](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-72-release-source-synchronization-acceptance-and-governance-closure).
All accepted PE-7.1 implementation and contract bytes remain unchanged.

NEXT_CHECKPOINT=PE-7.3 - Guarded artifact, integration, UI and trust delivery.
PE73_STATUS=NOT_STARTED; PE73_AUTHORIZED=FALSE.
Separate authorization is required. No runtime installation, HA integration delivery,
credential creation, Asset migration, monitoring or notification activation is
authorized by this documentation/source-synchronization checkpoint.
No automatic follow-on action; PE-7 overall remains IN_PROGRESS.

## Historical PE-7.1 accepted repository implementation and governance closure

Classification: CURRENT. Phase 7A ACTIVE; PE6_STATUS=COMPLETE/PASS.
PE70_STATUS=COMPLETE/PASS; PE7_STATUS=IN_PROGRESS.
PE71_STATUS=COMPLETE/PASS; PE71_COMPLETE=TRUE.
PE71_INDEPENDENT_ACCEPTANCE=ACCEPT; PE71_FOCUSED_RECHECK=ACCEPT.
The original independent REJECT identified the HA unknown/unavailable false-outage
defect. The authorized correction passed targeted validation; the focused independent
recheck accepted the corrected candidate with no confirmed blockers remaining.
This is Windows repository implementation acceptance only, not production acceptance.
No PE-7 production deployment, Asset migration, monitoring execution or recurring
activation occurred or is authorized. PE-6 remains COMPLETE/PASS.
See the [accepted contract](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION_CONTRACT.md)
and [implementation Evidence Report](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#final-pe-71-independent-acceptance-and-governance-closure).

Full native validation before the HA correction: 3236 run, 3192 passed, zero
failures/errors, 44 individual skips and five additional class-level skips.
The full suite was not repeated after correction. HA/evaluator/incident correction:
44/44 passed; binding/preservation: 7/7 passed. Exact skip reasons and the four-file
historical fingerprint limitation remain in the Evidence Report.
Controlled publication of this exact accepted candidate is authorized by the final
closure instruction; exact commit/push/remote/clean verification completes that gate.

NEXT_CHECKPOINT=PE-7.2 - Operator-only exact release-source synchronization.
PE72_STATUS=NOT_STARTED; PE72_AUTHORIZED=FALSE.
Separate authorization is required. PE-7.2 permits source synchronization only,
not runtime installation, migration, execution or recurring activation.
No automatic follow-on action. PE-7 overall remains IN_PROGRESS.

## Historical PE-7.1 implementation candidate before final acceptance

PE71_STATUS=CANDIDATE_READY_FOR_INDEPENDENT_ACCEPTANCE; PE71_IMPLEMENTATION_AUTHORIZED=TRUE.
PE71_INDEPENDENT_ACCEPTANCE=NOT_PERFORMED; PE71_COMPLETE=FALSE.
Baseline ad9ddc5ced903f8c922a12c08f843fba6fce907b. The accepted PE-7.0 contract
remains authoritative with the explicitly authorized section 6.1 T03/T04 status-read
extension. See [implementation evidence](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md).
No production access, deployment, monitoring, recurring activation or PE-7.2 is
authorized. No implementation commit or push is authorized. Current PE-7.1 authorization
supersedes earlier NOT STARTED snapshots below; it grants no later checkpoint authority.


## PE-7.0 accepted availability contract and governance closure

Classification: CURRENT. Phase 7A ACTIVE; PE6_STATUS=COMPLETE/PASS; PE6_5_STATUS=COMPLETE/PASS.
PE70_STATUS=COMPLETE/PASS; PE70_INDEPENDENT_CONTRACT_ACCEPTANCE=PASS.
PE70_FOCUSED_RECHECK=ACCEPT; PE7_STATUS=IN_PROGRESS; PE7_DESIGN_STATUS=COMPLETE.
PE71_STATUS=NEXT / NOT STARTED; PE71_STARTED=FALSE; PE71_IMPLEMENTATION_AUTHORIZED=FALSE.
PE7_IMPLEMENTATION_AUTHORIZED=FALSE; PE7_PRODUCTION_AUTHORIZED=FALSE.
PE7_MONITORING_EXECUTION_AUTHORIZED=FALSE; PE7_RECURRING_ACTIVATION_AUTHORIZED=FALSE.
NEXT_CHECKPOINT=PE-7.1 - Repository implementation.

The [accepted consolidated PE-7 implementation contract](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION_CONTRACT.md)
has SHA-256 `57534e84132f4b305608dd1492462b9581e646228bef3bbf0cb47b9b9607f617`.
The original independent review's two blockers were corrected: version-aware PE-6
Asset consumption preserves truthful operator_ha provenance and original bytes;
durable notification authorization serializes with Expected Availability OFF and
bounds pre-OFF grants without claiming recall of in-flight delivery. The focused
independent recheck accepted both corrections. Independent contract acceptance is
PASS; no further contract-review cycle is required for this accepted candidate.

The contract remains byte-identical to its accepted prepared version, including
its preparation-time lifecycle labels. This current Master Plan records subsequent
acceptance and formal PE-7.0 closure; it does not change the accepted architecture.
Mandatory independent Expected Availability and Infrastructure Device Dashboard
toggles, conditional Infrastructure Type, security/schema decisions, all 14
operator transitions, 24 acceptance criteria and PE-7.1 through PE-7.6 remain intact.

PE-7.1 is next, NOT STARTED, and requires separate implementation authorization.
This documentation-only closure performs no implementation, deployment, monitoring,
recurring activation, migration, HA change or credential provisioning. PE-6 evidence
remains closed and unchanged; PE-8/9/10 and all other future commitments retain scope
and order. Following Implementation Status entries are preserved historical records.

## PE-6.5 final PE-6 governance closure and PE-7 handoff

Classification: CURRENT. Phase 7A ACTIVE; PE-4 PASS/CLOSED; Public Projection PASS/CLOSED.
PE5_STATUS=COMPLETE; PE6_STATUS=COMPLETE/PASS; PE6_5_STATUS=COMPLETE/PASS.
PE6_0_STATUS=COMPLETE/PASS; PE6_1_STATUS=COMPLETE/PASS; PE6_2_STATUS=COMPLETE/PASS;
PE6_3_STATUS=COMPLETE/PASS; PE6_4_STATUS=COMPLETE/PASS.
PE7_STATUS=NOT STARTED / NOT AUTHORIZED; PE7_STARTED=FALSE; PE7_AUTHORIZED=FALSE.
NEXT_CHECKPOINT=PE-7 - Expected Availability & Permanent IoT Monitoring.

PE-6 is formally closed. PE-6.0 accepted design, PE-6.1 repository implementation,
PE-6.2 source synchronization and PE-6.3 disabled installation remain accepted;
see [existing implementation and acceptance records](PE6_CLASSIFICATION_IMPLEMENTATION.md).
PE-6.4 third-execution independent acceptance ACCEPT and governance closure at
`8984ce13724b6fb2b4b8c8216b4d396551c137ce` establish the final predecessor.
Its complete Evidence Report and exact accepted receipt/release/capture/endpoint
identities below remain unchanged. All production observations retain OPERATOR_SUPPLIED
status and their documented limitations. The second historical receipt remains
INSUFFICIENT_EVIDENCE; it is not promoted or rewritten.

This completes the [accepted PE-6.5 roadmap](PE6_CLASSIFICATION_CONTRACT_DESIGN.md#pe-65--final-pe-6-governance-closure-and-pe-7-handoff)
through Windows repository governance only. No further PE-6 production actions are
authorized or required by this closure; no production execution or predecessor
validation is repeated. PE-7 is eligible for separate future authorization only;
its existing scope, implementation contract, sequencing and all future roadmap
commitments remain unchanged. No automatic follow-on, implementation, deployment,
classification, producer execution or recurring activation is authorized. STOP.

All following Implementation Status entries, including the PE-6.4 closure report,
are preserved historical checkpoint records; their then-current status and next-task
labels do not supersede this final PE-6 closure and PE-7 handoff.

## PE-6.4 accepted bounded production execution and governance closure

Classification: CURRENT. Phase 7A ACTIVE; PE-4 PASS/CLOSED; Public Projection PASS/CLOSED.
PE5_STATUS=COMPLETE; PE6_STATUS=IN_PROGRESS.
PE6_0_STATUS=COMPLETE/PASS; PE6_1_STATUS=COMPLETE/PASS;
PE6_2_STATUS=COMPLETE/PASS; PE6_3_STATUS=COMPLETE/PASS; PE6_4_STATUS=COMPLETE/PASS.
PE6_REPOSITORY_IMPLEMENTED=TRUE; PE6_PRODUCTION_DEPLOYED=TRUE.
PE6_PRODUCTION_EXECUTION_ESTABLISHED=TRUE; EXECUTION_SCOPE=ONE_BOUNDED_OFFLINE_INVOCATION.
INDEPENDENT_REPOSITORY_ACCEPTANCE=ACCEPT; RECURRING_CLASSIFICATION_ACTIVATION=FALSE.
PE6_5_STATUS=NEXT / NOT STARTED; PE7_STARTED=FALSE.
NEXT_CHECKPOINT=PE-6.5 - Final PE-6 governance closure and PE-7 handoff.
PE-6.5 requires separate authorization; this closure does not start it or authorize PE-7.

### PE-6.4 concise Evidence Report

Evidence class: OPERATOR_SUPPLIED for all PI3 execution observations, not Codex
production observation. Repository release identities and local numerical hash
verification are IMMUTABLE_REPOSITORY_FACT / repository calculations over that
supplied evidence; public hashes do not independently authenticate production.
The distinct third execution was independently adjudicated ACCEPT against the
original [PE-6.4 contract](PE6_CLASSIFICATION_CONTRACT_DESIGN.md#pe-64--bounded-execution-and-concise-independent-production-acceptance)
and [published acceptance workflow](PE6_INDEPENDENT_ACCEPTANCE_WORKFLOW.md).

- Authorization: `PE64_20261020_THIRD_ACCEPTANCE`.
- Expiry disposition: `PE64_20261020_FROZEN_PE1_DISPOSITION`.
- Original sanitized JSON SHA-256 (exact JSON bytes excluding transcript framing):
  `befcea91d121e137dcd448497eba941e443acec70ff243b1242f863b53330291`.
- Acceptance-tool release: `1477f672db00e67bc1923a667a8dd5913f183166`.
- Helper SHA-256: `7155d0f490ebffdc4c94cf2974bda7b9ae4a3e01cb94c3571ae01921a6bb9c4d`.
- Instrument SHA-256: `a71842ce745590e3dac11ca0b0e60367f6c40d1d89b89b0b30518bb0a12d8c61`.
- Receipt source object: `9d6ce274a80a578d488d7245ebfa5bca1d5f5a83`, the instrument's
  pinned runtime source baseline, distinct from its published acceptance-tool release.
- Runtime identity: `980031f9b1ec934b3c41e7429671a57b4849eb7b225d73ab355b314e8180b282`.
- Evaluation time: `2026-10-21T05:35:31.882208Z` (operator receipt UTC).
- Functional verification and positive classification evidence PASS; exactly one
  authorized invocation; 198 devices and two hostname suggestions; both module-origin
  checks PASS. Five optional sources intentionally unselected; PARTIAL describes
  source availability, not execution failure. Process exit code 0; no automatic retry.
- No private output persistence or recurring classification activation.
- All eight protected categories: code, configuration, producer_state,
  historical_journals, runtime_root, locks, schedule and user_crontab.
- Both protected inspections PASS; before/after captures COMPLETE, ordered,
  without protected gate failure; zero changed objects, zero reported differences,
  zero omitted objects, no missing differences and no truncation.
- Before interval: `2026-10-21T05:35:27.181854Z` to `2026-10-21T05:35:30.381408Z`.
- After interval: `2026-10-21T05:35:34.628629Z` to `2026-10-21T05:35:37.373914Z`.
- Identical before/after protected capture SHA-256:
  `33fa99f76eb105550c32cf0bc1ad1d81955113cea96cc453e733a7e3aebe7a4f`.
- Canonical public endpoint-evidence SHA-256 independently recomputed and matched:
  `d3e21e29d737432cfc380aea882c6cb5a0d2a32541f6034abde829fe8d2f8e60`.
  Each endpoint binds to its own original capture identity and interval.
- Same-capture PE5_OUTPUT_DIRECTORY: directory, UID/GID 1000:1000, mode 0700,
  device 45826, inode 825862, link count 2. Both companion files are regular,
  UID/GID 1000:1000, mode 0600, single-link, device 45826; current.json inode
  825867 and current.durability.json inode 825864. All recorded fingerprints,
  sizes and timestamps match between before and after; safety is established by
  these observations, not a later unbound inspection.
- Required directory ancestors were PRESENT and unchanged: runtime root inode
  802322, state root inode 802388, state/enrichment inode 825861, all device 45826.
- Zero protected changes require no PE-5 mutation-attribution permission. Acceptance
  applies absence of unauthorized protected changes, not a producer exemption.

### Preserved history, limitations and next gate

The second production acceptance receipt remains INSUFFICIENT_EVIDENCE, unchanged;
its missing historical directory-safety values are not backfilled or promoted to PASS.
The separately authorized successful third execution supplies its own complete
security observations. Earlier PE-6.0/6.1/6.2/6.3 and timestamp-correction narratives,
original requirements, production evidence and accepted PE-4/PE-5 authority remain historical.

Endpoint observations do not prove universal absence of transient changes or a
complete event history. Public evidence hashes do not authenticate production
provenance. Full private capture preimages are not reconstructed. Five optional
sources remain unselected. The frozen PE-1 candidate has no candidate-specific
expires_at; its accepted expiration-disposition limitation is unchanged, with no
new TTL. The preserved runtime inventory variant is not a universal compatibility
or current health/freshness claim. No recurring activation is authorized.

This governance closure changes documentation only; no Codex PI3/PI5 access,
deployment, classifier/PE-5 execution, production mutation or historical receipt
rewrite occurs. PE-6.5 is eligible after PE-6.4, but remains NOT STARTED pending
separate authorization. It is repository-only final PE-6 closure/handoff, with no
repeated production action. PE-7 remains later and separately authorized. STOP.

Earlier Implementation Status entries below are historical snapshots; their
then-current labels do not supersede this accepted PE-6.4 status.

## Timestamp compatibility repository correction (PE-6.4 prerequisite)

### PE-6.4 - Bounded Execution and Independent Production Acceptance

Classification: CURRENT. Phase 7A ACTIVE; PE-4 PASS/CLOSED; Public Projection PASS/CLOSED.
PE5_STATUS=COMPLETE; PE6_STATUS=IN_PROGRESS.
PE6_0_STATUS=COMPLETE/PASS; PE6_1_STATUS=COMPLETE/PASS;
PE6_2_STATUS=COMPLETE/PASS; PE6_3_STATUS=COMPLETE/PASS.
PE6_REPOSITORY_IMPLEMENTED=TRUE; PE6_PRODUCTION_DEPLOYED=TRUE.
DEPLOYMENT_SCOPE=DISABLED_EXACT_FOUR_FILE_INSTALLATION_ONLY.
PE6_PRODUCTION_EXECUTION_ESTABLISHED=FALSE; PE6_4_STARTED=FALSE.
NEXT_CHECKPOINT=PE-6.4 - Bounded Execution and Independent Production Acceptance.
Separate authorization is required for PE-6.4. No scheduler or automatic activation is authorized.

PE-6.3 accepts only OPERATOR_SUPPLIED PI3 disabled-installation evidence from
source 723c1e71ad2d54e5088c0849ccee59857cbe0794. Four exact new artifacts were
installed without overwriting existing files; seven observed dependencies were preserved.
Codex did not access PI3. No caller execution, initialization, cron change,
service restart, scheduled activation or PE-6.4 execution occurred in this checkpoint.
The inspected activation locations returned no matches; universal indirect invocation
absence and current production health are not established.
Runtime inventory.py differs from source; only KNOWN_FIELDS, OPERATOR_ROLES and
normalize_mac AST definitions were reported equal. Full runtime compatibility is not established.
Rollback was NOT PERFORMED and is not claimed tested. No pre-existing dependency may be removed.
See [PE-6.3 Evidence Report](PE6_CLASSIFICATION_IMPLEMENTATION.md#pe-63-disabled-runtime-installation-acceptance-and-closure).
PE-6 remains IN PROGRESS. PE-6.4 is NEXT / NOT STARTED; PE-6.5 closure and PE-7 remain later.
### Timestamp compatibility correction prerequisite

TIMESTAMP_CORRECTION=REPOSITORY_ONLY; CORRECTED_ARTIFACT_DEPLOYED=NOT_ESTABLISHED.
PE6_4_STARTED=FALSE; PE6_PRODUCTION_EXECUTION_ESTABLISHED=FALSE.
The operator reported inventory.updated=2026-10-17T11:00:02-06:00,
198 parseable devices and freshness at inspection only (OPERATOR_SUPPLIED).
The PE-6.3 installed classifier rejects that accepted PE-5 aware-time form.
The repository correction accepts aware offsets and emits UTC without rewriting inputs.
Production still requires separate operator source synchronization, guarded replacement
of classification.py only, then separately authorized bounded PE-6.4 execution.
No deployment, caller execution, scheduling, PE-6.4 closure or PE-7 is authorized here.
See [Timestamp correction evidence](PE6_CLASSIFICATION_IMPLEMENTATION.md#timestamp-compatibility-correction-prerequisite-to-pe-64).

STOP after the repository correction. No automatic follow-on action is authorized.

Earlier checkpoint entries below remain historical evidence.


## PE-6.3 disabled runtime installation closure

### PE-6.4 - Bounded Execution and Independent Production Acceptance

Classification: CURRENT. Phase 7A ACTIVE; PE-4 PASS/CLOSED; Public Projection PASS/CLOSED.
PE5_STATUS=COMPLETE; PE6_STATUS=IN_PROGRESS.
PE6_0_STATUS=COMPLETE/PASS; PE6_1_STATUS=COMPLETE/PASS;
PE6_2_STATUS=COMPLETE/PASS; PE6_3_STATUS=COMPLETE/PASS.
PE6_REPOSITORY_IMPLEMENTED=TRUE; PE6_PRODUCTION_DEPLOYED=TRUE.
DEPLOYMENT_SCOPE=DISABLED_EXACT_FOUR_FILE_INSTALLATION_ONLY.
PE6_PRODUCTION_EXECUTION_ESTABLISHED=FALSE; PE6_4_STARTED=FALSE.
NEXT_CHECKPOINT=PE-6.4 - Bounded Execution and Independent Production Acceptance.
Separate authorization is required for PE-6.4. No scheduler or automatic activation is authorized.

PE-6.3 accepts only OPERATOR_SUPPLIED PI3 disabled-installation evidence from
source 723c1e71ad2d54e5088c0849ccee59857cbe0794. Four exact new artifacts were
installed without overwriting existing files; seven observed dependencies were preserved.
Codex did not access PI3. No caller execution, initialization, cron change,
service restart, scheduled activation or PE-6.4 execution occurred in this checkpoint.
The inspected activation locations returned no matches; universal indirect invocation
absence and current production health are not established.
Runtime inventory.py differs from source; only KNOWN_FIELDS, OPERATOR_ROLES and
normalize_mac AST definitions were reported equal. Full runtime compatibility is not established.
Rollback was NOT PERFORMED and is not claimed tested. No pre-existing dependency may be removed.
See [PE-6.3 Evidence Report](PE6_CLASSIFICATION_IMPLEMENTATION.md#pe-63-disabled-runtime-installation-acceptance-and-closure).
PE-6 remains IN PROGRESS. PE-6.4 is NEXT / NOT STARTED; PE-6.5 closure and PE-7 remain later.
STOP after PE-6.3. No automatic follow-on action is authorized.

All earlier checkpoint narratives below retain their accepted historical meaning,
including then-current labels and next-task snapshots. They do not supersede this
current status or Next Planned Task. Installation is not classification execution.


## PE-6.2 source synchronization closure

### PE-6.3 - Disabled Exact Runtime Deployment

Classification: CURRENT. Phase 7A ACTIVE; PE-4 PASS/CLOSED; Public Projection PASS/CLOSED.
PE5_STATUS=COMPLETE; PE6_STATUS=IN_PROGRESS_REPOSITORY_IMPLEMENTED.
PE6_0_STATUS=COMPLETE/PASS; PE6_1_STATUS=COMPLETE/PASS; PE6_2_STATUS=COMPLETE/PASS.
PE6_REPOSITORY_IMPLEMENTED=TRUE; PE6_PRODUCTION_DEPLOYED=FALSE.
NEXT_CHECKPOINT=PE-6.3 - Disabled Exact Runtime Deployment.
Separate authorization is required for PE-6.3. PE6_3_STARTED=FALSE.

PE-6.2 accepted source synchronization only from OPERATOR_SUPPLIED PI3 evidence:
main fast-forwarded to 238dfae6cef1d4f17a4b1e52a5f636f01a5651c4, clean, tree
matching accepted PE-6.1. Four PE-6 files were reported absent from runtime;
source and runtime directories were distinct. Codex did not observe PI3 directly.
See [PE-6.2 Evidence Report](PE6_CLASSIFICATION_IMPLEMENTATION.md#pe-62-source-synchronization-acceptance-and-formal-closure).
Historical PE-6.0/PE-6.1 contracts and acceptance evidence remain unchanged.
Source synchronization proves no production functionality, health, freshness or
universal runtime-file preservation. No runtime deployment or caller execution occurred.
PE-6.3 is disabled exact runtime deployment only, with no caller execution,
initialization, activation or cron; it is NOT STARTED and not authorized here.
PE-6.4 remains later bounded execution and independent acceptance under separate authorization.
No recurring activation, automatic execution, PE-7 work or follow-on action is authorized.

All earlier checkpoint narratives below retain their accepted historical meaning,
including then-current labels and next-task snapshots. They do not supersede this
current status or Next Planned Task. PE-6.2 proves source synchronization only.


## Historical accepted PE-6.0 contract design — 2026-10-14

Classification: HISTORICAL_INTENTIONALLY_PRESERVED accepted PE-6.0 snapshot. PE5_STATUS=COMPLETE; PE6_STATUS=DESIGN_COMPLETE_RUNTIME_NOT_IMPLEMENTED.
PE6_0_STATUS=COMPLETE_CONTRACT_DESIGN; PE6_RUNTIME_IMPLEMENTED=FALSE.
NEXT_CHECKPOINT=PE-6.1 - Private classification implementation and comprehensive repository validation.
Separate authorization is required for PE-6.1, including adoption or revision of the proposed design.
This checkpoint authorizes no runtime implementation, production operation or PE-7 work.

The [PE-6 contract design](PE6_CLASSIFICATION_CONTRACT_DESIGN.md) inventories actual
capabilities and preserves the complete original authorization, twenty evidence-backed
technical decisions, exact private schema proposal and six-checkpoint roadmap.
Proposed role suggestions and metadata-quality summaries remain private, deterministic
and separate from operator-owned Asset data and public operational role/health.
Asset schema1.0 and the accepted PE-5.9 governance/runtime remain unchanged.
No PE-6 persistence, cron, inventory hook or public projection is selected.
Actual production inputs/locks/runtime state remain UNKNOWN; only later bounded operator
gates may establish them. All previous OPERATOR_SUPPLIED evidence limitations remain.

## Historical PE-5 final closure — 2026-10-14

Classification: HISTORICAL_INTENTIONALLY_PRESERVED. Phase 7A ACTIVE; PE5_STATUS=COMPLETE.
PE5_9_STATUS=COMPLETE/PASS; PE5_8_STATUS=COMPLETE/PASS.
NEXT_CHECKPOINT=PE-6 - Classification & Metadata Quality; PE6_STARTED=FALSE.
Separate authorization is required for PE-6. PE-6 implementation is NOT authorized.

All 37 original PE-5 requirements and all 14 Definition of Done conditions pass;
all 11 roadmap UNKNOWN decisions have evidence-backed resolutions. The original
roadmap and 46 implementation checklist items remain immutable authority.
The current coverage/evidence ledger and complete private handoff are in
[PE-5 implementation evidence](PE5_CONFIGURED_ASSOCIATION_IMPLEMENTATION.md#current-pe-59-final-closure-and-private-pe-6-handoff)
and final_closure in the existing implementation governance record.
PE-5.6/7/8 accepted observations remain OPERATOR_SUPPLIED. Preserve
OPERATOR_OBSERVATIONS_ONLY; FULL_PRODUCTION_BYTES_NOT_RECEIVED;
NO_NATURAL_FAULT_OR_NATIVE_CRASH_CLAIM; NO_CURRENT_FRESHNESS_CLAIM.
First-cycle fields not separately supplied remain UNKNOWN; none is a completion
waiver or new production observation. No runtime, scheduler, public interface,
MQTT or production change occurs here. PE-6 may later consume only validated,
confirmed, unexpired private relationship evidence under the unchanged contract.
Publication remains gated by exact commit, push and independent GitHub verification.

## Historical PE-5.1 deployment and first native execution acceptance — 2026-10-13

Classification: HISTORICAL_INTENTIONALLY_PRESERVED. Production deployment and the first native private caller
execution are PASS/ACCEPTED on OPERATOR_SUPPLIED evidence. Policy 2100 seconds is
finalized at ed3a80508d101652bac89e1dcc111167670aaebc; execution count 1, return
code 0, valid output/schema, 8 private associations, 0 rejections, snapshot age
1756.120272 seconds, inventory/public inventory unchanged. No persistence,
scheduling, publication or broader PE-5 completion is established. See the current
PE-5.1 acceptance in Current Objective for exact evidence and boundaries.


## Historical/current lifecycle test-binding correction

Historical accepted checkpoint snapshot at 30010c54d3f3078a9b07dada36dfe8dd4db2f6e5.
Its open lifecycle statements below describe that committed correction checkpoint.
The following Public Projection closure candidate remains UNCOMMITTED/UNACCEPTED;
only later full closure validation and acceptance can establish successor lifecycle.

Correction: PASS/CLOSED.
Public Projection production evidence: OPERATOR_SUPPLIED / CLOSURE DRAFT NOT YET ACCEPTED.
Public Projection closure: NOT CLOSED.
PE-4: NOT COMPLETE.
Phase 7A: ACTIVE.
PE-5: NOT STARTED.

The prior closure attempt stopped on regression. The source-binding diagnosis
identified historical checkpoint tests reading evolving current lifecycle
documentation while their current bytes were frozen to historical source.
The successor test-binding correction preserves original historical commits,
blobs, hashes and flags and binds exactly four current lifecycle test identities.
Historical lifecycle assertions read evidence-selected immutable snapshots.
Current lifecycle authority remains owned by accepted successor governance.
The closure draft is durably preserved for later separately authorized resumption.
Production evidence was not rerun; no roadmap transition occurred.

Authority: [test-binding correction](PE4_HOME_ASSISTANT_ASSOCIATION_PUBLIC_PROJECTION_TEST_BINDING_CORRECTION.md).
Next action: separately authorize resumption and validation of the preserved
Public Projection closure draft against this corrected baseline.



## Public Projection production closure and PE-4 completion — 2026-10-09

Accepted Public Projection production closure at 017686549acb27dbf7a8ad3577d0f84cf9f3f066;
PUBLIC_PROJECTION=PASS/CLOSED and PE4=PASS/CLOSED.
Historical vs Current Lifecycle Test-Binding Correction PASS/CLOSED at
30010c54d3f3078a9b07dada36dfe8dd4db2f6e5 is an exact machine-bound prerequisite.
Its original correction artifacts and historical authority remain immutable; exactly four
current test exceptions retain accepted stage-0 identities and normalized checkout proof.

PUBLIC_PROJECTION=PASS/CLOSED; PE4_COMPLETION_AUDIT=PASS; PE4=PASS/CLOSED.
All production evidence is OPERATOR_SUPPLIED; Codex did not observe or access PI3.
The accepted PE-4 completion audit includes the binding correction and evaluates
all mandatory PE-4 prerequisites. PE-4 closure was derived at its accepted checkpoint,
not an immutable repository fact from the historical c7db baseline.
Scheduler closure identifies Public Projection as the remaining checkpoint.
Preparation, Source Implementation, PI3 POSIX Source Validation PASS/CLOSED;
Deployment Preparation PASS/CLOSED WITH BASELINE CORRECTION; Baseline Correction PASS/CLOSED.
Baseline Attempt 1 remains FAIL / BASELINE_MISMATCH / SAFE.
Corrected Baseline PASS; Baseline Receipt PASS / INDEPENDENTLY VERIFIED:
014a901a56ebc613b2235ad434ae124024ae6e01e8e1960ce98e7df6709e9944.
Deployment PASS/CLOSED, VERIFIED_DEPLOYED; Installed-State Review PASS.
First Natural Pre-Slot Observation NOT_PROVEN / EXPECTED / NO FAILURE.
First Natural Inventory Cycle PASS; inventory 2026-10-09T16:30:02-06:00;
status 2026-10-09T16:30:03-06:00; cron 2026-10-09T22:30:01.240256+00:00.
Device count 186; First Natural Public Projection PASS, count 25, zero contract failures.
First Natural MQTT Acceptance PASS; retained topics 7/7; payload equality PASS.
Observer credential accessed TRUE, value exposed FALSE, observer published FALSE.
Deployment/review false execution flags are scoped to those invocations.
Cron journal, state write, timestamps and contract checks establish natural execution.
Broker retained observations and exact payload equality establish separate MQTT acceptance.
No scheduler stdout or process result is reconstructed.

Historical wrapper FAIL, PRODUCTION_FILES_UNCHANGED=FALSE, missing /tmp limitation,
Independent Acceptance Attempt 1 failure and baseline Attempt 1 remain immutable.
Rollback NOT_PERFORMED; Manual Second Adapter Execution NOT_AUTHORIZED / NOT_PERFORMED;
Recurring Association Scheduler ACTIVE / AUTHORIZED; Phase 7A ACTIVE; PE-5 NOT_STARTED.
No runtime implementation or future roadmap work changed.
OPERATOR_SUPPLIED post-closure PI3 release-source synchronization COMPLETED and independent source review PASS: c7db29f795909d7926e36c02f1166034bcebb8b0 -> 30010c54d3f3078a9b07dada36dfe8dd4db2f6e5 (STOP; review PASS) -> 017686549acb27dbf7a8ad3577d0f84cf9f3f066 (STOP; review PASS). Observed final source tree: 6a59929189bc65fa8487e73ba97477eb009a43f0. Production was not accessed or mutated during this source-only sequence; Codex did not perform or observe it.
Historical correction-candidate sequencing at 5472a85194d105f6fb3d08ce51a4788256d8f028: Current governed checkpoint: documentation consistency correction, an uncommitted candidate. Validation, independent review and separately authorized commit/push must close this correction before PE-5.
Ordered next task: PE-5 - MQTT and Passive Service Association; separately governed, NOT_STARTED.
[Closure authority](PE4_HOME_ASSISTANT_ASSOCIATION_PUBLIC_PROJECTION_DEPLOYMENT_CLOSURE.md).

## Historical implementation notices before Public Projection closure

## Association Scheduler Deployment final governance closure — 2026-10-07

**Scheduler Deployment PASS/CLOSED; Recurring Scheduler Operation ACTIVE / AUTHORIZED.**
Preparation and Independent Production Acceptance remain PASS/CLOSED. Operator-supplied source
sync, independent pre-install review, one separately authorized installation (VERIFIED_INSTALLED)
and post-install review PASS. Canonical 5,35 crontab job and protected platform line unchanged.
First natural 20:35 local invocation OBSERVED through valid private-state publication at
2026-10-08T02:35:03.814281Z (2026-10-07 20:35:03.814281 -06:00); schema PASS, mode 0600,
one link, clean transaction namespace, HA version 2026.9.4, sanitized counts 25/170/26/8/0.
Exact scheduled result text and return code NOT OBSERVED BY DESIGN: both cron streams are
discarded by frozen privacy policy. Publication PASS does not reconstruct process result.
Installer/review FALSE activity flags apply only to those actions, not the scheduled cycle.
Manual Second Adapter Execution NOT AUTHORIZED / NOT PERFORMED; scheduled recurring execution
AUTHORIZED. Historical Second Adapter Execution restriction refers to manual execution.
Codex did not access/observe production or run installer/adapter/acceptance/reconciler.
Attempt 1 failed capture and unavailable original evidence limitations remain immutable.
Public Projection DEFERRED; PE-4 NOT COMPLETE because its separately deferred public projection
checkpoint remains; Phase 7A ACTIVE; PE-5 NOT STARTED; rollback NOT PERFORMED.
Next: **PI3 source synchronization to the scheduler deployment closure commit ONLY**; STOP
and independent review. No roadmap transition authorized. Already-active cron may naturally
run during sync; this is not execution by sync. Do not disable it for governance synchronization.
[Scheduler deployment closure](PE4_HOME_ASSISTANT_ASSOCIATION_SCHEDULER_DEPLOYMENT_CLOSURE.md).
Earlier notices remain historical.

## Association Scheduler Deployment preparation — 2026-10-07

**Scheduler Deployment Preparation PASS/CLOSED. Scheduler Deployment NOT STARTED /
PREPARED FOR SEPARATE AUTHORIZATION.** Independent Production Acceptance remains PASS/CLOSED.
Frozen jazofv1 user crontab job HIOC_PE4_HA_ASSOCIATION runs at 5,35 * * * * through the
accepted active interpreter with -I -B, the dedicated entrypoint and its existing internal lock.
The source-bound narrow installer preserves prior crontab bytes/platform line, performs one
installation attempt and exact reread, and requires manual review for uncertain outcomes.
No installation, forced run, adapter/HA/credential access or scheduler mutation occurred here.
No automatic retry/removal/rollback; crontab lacks compare-and-swap, so future execution requires
an exclusive operator maintenance window. Privacy redirects both job streams to /dev/null.
PI3 predecessor source review at 826608b40d5248c67742a17fc95a6e7612981df1 is operator supplied.
Next action: **PI3 source synchronization to the scheduler preparation commit ONLY**; STOP and
independent review. Installation requires separate explicit authorization for recurring natural
5/35 slots; this never authorizes an extra manual second adapter invocation.
Second Adapter Execution NOT AUTHORIZED; Public Projection DEFERRED; PE-4 NOT COMPLETE;
Phase 7A ACTIVE; rollback NOT PERFORMED. Earlier notices remain historical.
[Scheduler preparation](PE4_HOME_ASSISTANT_ASSOCIATION_SCHEDULER_DEPLOYMENT_PREPARATION.md).

## Independent Production Acceptance final governance closure — 2026-10-07

**Independent Production Acceptance PASS/CLOSED; Attempt 2 PASS.** This repository-only
closure records OPERATOR_SUPPLIED_WINDOWS_AND_PRODUCTION_EXECUTION_EVIDENCE and separately
performed OPERATOR_SUPPLIED_WINDOWS_EVIDENCE_REVIEW, not Codex-observed production execution.
PI3 source synchronization through the capture correction to operator-path commit PASS;
Attempt 2 run 20261007T220653-46cef5aace9e, 560-byte validation and 194-byte manifest,
manifest binding and all eight acceptance gates PASS. No retained evidence accessed or recreated.
Attempt 1 remains FAIL / DURABLE CAPTURE, inspection PASS / operator supplied, evidence
NOT PUBLISHED, stdout UNAVAILABLE. Older original-artifact revalidation UNAVAILABLE and
limitation RECORDED remain permanent; disappearance cause UNKNOWN.
Preparation, Capture Correction and Operator Path Integration PASS/CLOSED; native durability PASS.
Second Adapter Execution NOT AUTHORIZED; Scheduler Deployment NOT STARTED; Public Projection
DEFERRED; PE-4 NOT COMPLETE; Phase 7A ACTIVE; rollback NOT PERFORMED.
Next objective: **PE-4 Home Assistant Association Adapter Scheduler Deployment**, NOT STARTED.
Immediate operator handoff is closure source synchronization ONLY; STOP and independent review.
Earlier acceptance notices below are historical and do not override this closure.
[Acceptance closure](PE4_HOME_ASSISTANT_ASSOCIATION_INDEPENDENT_PRODUCTION_ACCEPTANCE_CLOSURE.md).

## Independent Production Acceptance operator-path integration — 2026-10-07

Operator Path Integration **PASS/CLOSED**; native Windows synthetic durability **PASS**.
The committed thin remote read-only wrapper, Windows binary transport orchestrator and capture
helper now share the historical producer's exact PASS=0 / FAIL=2 return-code contract. No ad hoc
acceptance program is needed. Windows PowerShell system module isolation fixes the native ACL
prerequisite. Actual synthetic Windows filesystem and PASS/FAIL subprocess transport tests passed.
Attempt 1 remains inspection PASS (operator supplied), durable capture FAIL, evidence NOT PUBLISHED,
raw stdout UNAVAILABLE; no evidence recreated. Independent Production Acceptance NOT CLOSED.
Attempt 2 **NOT STARTED / READY FOR SEPARATE AUTHORIZATION**, **NOT AUTHORIZED**.
Immediate next action: **PI3 source synchronization to the operator-path integration commit only**;
STOP and independent review, then separate explicit Attempt 2 authorization. No PI3 action here.
Second adapter execution NOT AUTHORIZED; scheduler NOT STARTED; projection DEFERRED;
PE-4 NOT COMPLETE; Phase 7A ACTIVE; rollback NOT PERFORMED. Earlier capture/preparation wording
below is historical. [Operator-path contract](PE4_HOME_ASSISTANT_ASSOCIATION_INDEPENDENT_PRODUCTION_ACCEPTANCE_OPERATOR_PATH.md).


## Independent Production Acceptance capture correction — 2026-10-07

Preparation PASS/CLOSED. Attempt 1 **FAIL / DURABLE CAPTURE**; read-only inspection portion
**PASS** (operator-supplied), durable validation.json/manifest.json **NOT PUBLISHED**.
Independent Production Acceptance **NOT CLOSED**. Capture Correction **PASS/CLOSED**.
The workstation serializer defect is reproduced with synthetic data: Windows PowerShell 5.1
escapes the target ampersand as backslash-u0026 while Python leaves it literal. The corrected
local helper validates original bytes with Python semantics and publishes original bytes only.
Attempt 1 stdout remains UNAVAILABLE for durable revalidation; no evidence is recreated.
Attempt 2 **NOT STARTED / PREPARED FOR SEPARATE AUTHORIZATION**, NOT AUTHORIZED; no automatic retry.
Native workstation ACL/durability compatibility must be checked synthetically before authorization.
Immediate next action: **PI3 source synchronization to the capture correction commit only**;
STOP and independent review. No acceptance, adapter or reconciler execution is authorized here.
Scheduler NOT STARTED; Public Projection DEFERRED; PE-4 NOT COMPLETE; Phase 7A ACTIVE;
rollback NOT PERFORMED; second adapter execution NOT AUTHORIZED. Earlier preparation sequencing
below is historical. [Correction contract](PE4_HOME_ASSISTANT_ASSOCIATION_INDEPENDENT_PRODUCTION_ACCEPTANCE_CAPTURE_CORRECTION.md).


## Independent Production Acceptance preparation — 2026-10-07

Independent Production Acceptance Preparation: **PASS/CLOSED**.
Acceptance execution: **NOT STARTED / PREPARED FOR SEPARATE AUTHORIZATION**.
Current objective remains PE-4 Home Assistant Association Adapter Independent Production Acceptance.
Immediate next operator action: **PI3 source synchronization to the acceptance preparation commit only**,
then STOP and independent source synchronization review, then separate authorization for read-only
acceptance execution. The closure-commit synchronization below is completed operator-supplied history.
The governed existing read-only function sequence inspects current durable state without HA network,
credential access, adapter rerun or production mutation. No new acceptance tool is required.
[Preparation contract](PE4_HOME_ASSISTANT_ASSOCIATION_INDEPENDENT_PRODUCTION_ACCEPTANCE_PREPARATION.md).
Scheduler Deployment NOT STARTED; Public Projection DEFERRED; PE-4 NOT COMPLETE; Phase 7A ACTIVE;
rollback NOT PERFORMED; second adapter execution NOT AUTHORIZED. Historical wrapper failure and
unavailable original-artifact limitation remain unchanged. Existing roadmap items are preserved.


Current authority (2026-10-07): **PE-4 Home Assistant Association Adapter Independent Production Acceptance**.
Durable Post-Run Reconciliation and Bounded Manual Production Validation are PASS/CLOSED
through explicit repository governance closure. OPERATOR_SUPPLIED_PRODUCTION_EVIDENCE:
PI3 source synchronization to 96150db5e28b065a587ae09ce0522ef6bd66f3be PASS/rc0, independent
source review, then one separately authorized durable reconciliation PASS/rc0. All protected
production surfaces and current durable gates passed without another adapter invocation.
Historical adapter execution remains COMPLETED ONCE / PASS; historical wrapper FAIL/rc1 /
MANUAL REVIEW REQUIRED and PRODUCTION_FILES_UNCHANGED=FALSE remain unchanged. First reconciliation
attempt remains FAIL / HISTORICAL_EVIDENCE. Original ephemeral files remain unavailable for
byte, metadata, canonical JSON or cross-file revalidation; the mandatory limitation is RECORDED.
The disappearance cause is UNKNOWN; no cause is inferred. Committed operator-supplied historical
report authority remains separate from current durable-state evidence.
Independent Production Acceptance and Scheduler Deployment NOT STARTED; Public Projection
DEFERRED; PE-4 NOT COMPLETE; Phase 7A Passive Living Inventory ACTIVE; rollback NOT PERFORMED;
second adapter execution NOT AUTHORIZED. Active Discovery remains postponed except already-governed
PE-4 work. Codex performed repository-only governance work and no production access or execution.
Next operator action: source synchronization to this closure commit only, STOP and independent
review. Independent Production Acceptance remains the next separately governed project checkpoint.

See [durable reconciliation closure](PE4_HOME_ASSISTANT_ASSOCIATION_DURABLE_POST_RUN_RECONCILIATION_CLOSURE.md).

## Historical evidence-authority preparation — superseded current sequencing


Current authority (2026-10-07): **PE-4 Home Assistant Association Adapter Durable Post-Run Reconciliation**.
The first live adapter run completed once (PASS/rc0); historical wrapper FAIL/rc1 and manual
review remain unchanged. Scope correction PASS/CLOSED was followed by operator-supplied PI3
source synchronization PASS to d767ad4 and one separately authorized reconciler attempt:
FAIL at HISTORICAL_EVIDENCE before durable checks. A narrow diagnostic reported
FileNotFoundError; a separate presence check proved the exact original /tmp directory absent
and zero matching manual-evidence directories. No disappearance cause is inferred.
No historical artifacts were recreated. The frozen committed operator report remains available;
original file metadata, bytes, canonical JSON and cross-file equality are unavailable for
revalidation. The evidence-authority correction is PASS/CLOSED; durable reconciliation is
PREPARED FOR SEPARATE AUTHORIZATION and eventual closure must retain the evidence limitation.
Next operator action: **PI3 source synchronization to the evidence-authority correction commit**,
STOP, independent review, then separate authorization for read-only durable reconciliation.
Independent acceptance and scheduler NOT STARTED; projection DEFERRED; PE-4 NOT COMPLETE;
Phase 7A ACTIVE; rollback NOT PERFORMED; second adapter execution NOT AUTHORIZED.


The earlier checkpoint notices below retain their historical scope and are superseded for current sequencing by this authority.


## PE-4 bounded manual validation production-scope correction - 2026-10-07

Repository-only correction PASS/CLOSED. [Correction procedure](PE4_HOME_ASSISTANT_ASSOCIATION_BOUNDED_MANUAL_VALIDATION_CORRECTION.md)
and [canonical record](../governance/pe4/pe4-ha-association-bounded-manual-validation-correction.json)
preserve OPERATOR_SUPPLIED first-run adapter PASS/rc0 and historical wrapper FAIL/rc1.
The adapter executed once and published valid private state. Historical PRODUCTION_FILES_UNCHANGED=FALSE
retains its original meaning; unrelated runtime churn makes that global invariant unsuitable.
Explicit protected surfaces replace it for corrected checks. No adapter defect or original differing
file is established. A second adapter execution is NOT AUTHORIZED.
Current objective: **PE-4 Home Assistant Association Adapter Durable Post-Run Reconciliation**.
Bounded Manual Production Validation ATTEMPTED / REVIEW REQUIRED; correction PASS/CLOSED;
Post-Run Reconciliation PREPARED FOR SEPARATE AUTHORIZATION. Next operator action:
**PI3 source synchronization to the evidence-authority correction commit**, STOP, independent sync review, then
separately authorize READ-ONLY reconciliation of existing evidence/state without adapter/credential/HA.
Deployment and preparation PASS/CLOSED; Independent Production Acceptance and Scheduler Deployment
NOT STARTED; Public Projection DEFERRED; PE-4 NOT COMPLETE; Phase 7A ACTIVE; rollback NOT PERFORMED.
Codex performed no production access/execution/mutation, deployment, scheduler, MQTT or projection.



## PE-4 bounded manual association validation preparation - 2026-10-06

Repository-only preparation PASS/CLOSED. [Preparation procedure](PE4_HOME_ASSISTANT_ASSOCIATION_BOUNDED_MANUAL_VALIDATION_PREPARATION.md)
and [canonical record](../governance/pe4/pe4-ha-association-bounded-manual-validation-preparation.json)
bind immutable deployment closure/source, the single future adapter invocation, privacy-safe evidence,
exact pre/post invariants and warning/failure handling. Deployment remains PASS/CLOSED.
Bounded Manual Production Validation is PREPARED FOR SEPARATE AUTHORIZATION, not executed or PASS.
Current objective remains **PE-4 Home Assistant Association Adapter Bounded Manual Production Validation**.
Next operator action: **PI3 source synchronization to the approved preparation commit**; STOP,
independent sync review, then separate live-execution authorization. Do not combine the actions.
Independent Production Acceptance and Scheduler Deployment NOT STARTED; Public Projection DEFERRED;
PE-4 NOT COMPLETE; Phase 7A ACTIVE; rollback NOT PERFORMED. No PI3/PI5/SSH/HA/credential access,
adapter/platform-status execution, deployment, production mutation, scheduler, MQTT or projection.


**Deployment PASS/CLOSED.** The operator reported successful governed deployment at
`4912f20d8b2ff78dcdaf8b3e0f52e57d5de5e3a2` and a separate PASS read-only static acceptance.
Both are OPERATOR_SUPPLIED_PRODUCTION_EVIDENCE, provenance OPERATOR_SUPPLIED; Codex did
not collect them or access PI3. Transaction COMMITTED; five dependencies preserved;
nine targets verified, all nine newly created; endpoint added. The three earlier failures
remain historical pre-intent NOT_STARTED attempts, with no partial deployment or rollback.

Deployment-local credential validation PASS used the governed local validator; this is
not a claim that deployment never read the credential file. No credential content was
exposed/persisted in evidence, placed in argv/environment or used for HA authentication.
The separate static acceptance accessed no credential. Codex accessed no real credential.
Adapter/platform-status remained unexecuted; no adapter HA network/authentication or
association state publication occurred. Association scheduler absent; existing platform
cron unchanged; pre-compatibility platform-status and compatibility-state metadata preserved.

Current objective and exact next task: **PE-4 Home Assistant Association Adapter Bounded Manual Production Validation**.
It remains NOT STARTED and requires separate first-run authorization. Independent Production
Acceptance and Scheduler Deployment NOT STARTED; Public Projection DEFERRED; PE-4 NOT COMPLETE;
Phase 7A ACTIVE; Rollback NOT PERFORMED. Stop before first adapter execution.
[Focused deployment closure](PE4_HOME_ASSISTANT_ASSOCIATION_ADAPTER_DEPLOYMENT_CLOSURE.md)
consolidates the two evidence sets and boundaries. Earlier checkpoint narratives retain
historical states and next tasks; this closure supersedes their current-authority wording.


## Deployment Execution governance closure — 2026-10-06

**Deployment PASS/CLOSED.** The operator reported successful governed deployment at
`4912f20d8b2ff78dcdaf8b3e0f52e57d5de5e3a2` and a separate PASS read-only static acceptance.
Both are OPERATOR_SUPPLIED_PRODUCTION_EVIDENCE, provenance OPERATOR_SUPPLIED; Codex did
not collect them or access PI3. Transaction COMMITTED; five dependencies preserved;
nine targets verified, all nine newly created; endpoint added. The three earlier failures
remain historical pre-intent NOT_STARTED attempts, with no partial deployment or rollback.

Deployment-local credential validation PASS used the governed local validator; this is
not a claim that deployment never read the credential file. No credential content was
exposed/persisted in evidence, placed in argv/environment or used for HA authentication.
The separate static acceptance accessed no credential. Codex accessed no real credential.
Adapter/platform-status remained unexecuted; no adapter HA network/authentication or
association state publication occurred. Association scheduler absent; existing platform
cron unchanged; pre-compatibility platform-status and compatibility-state metadata preserved.

Current objective and exact next task: **PE-4 Home Assistant Association Adapter Bounded Manual Production Validation**.
It remains NOT STARTED and requires separate first-run authorization. Independent Production
Acceptance and Scheduler Deployment NOT STARTED; Public Projection DEFERRED; PE-4 NOT COMPLETE;
Phase 7A ACTIVE; Rollback NOT PERFORMED. Stop before first adapter execution.
[Focused deployment closure](PE4_HOME_ASSISTANT_ASSOCIATION_ADAPTER_DEPLOYMENT_CLOSURE.md)
consolidates the two evidence sets and boundaries. Earlier checkpoint narratives retain
historical states and next tasks; this closure supersedes their current-authority wording.


## Historical Production compatibility dependency classification correction — 2026-10-06

Production Dependency Classification Correction PASS/CLOSED. The production observations
below are **OPERATOR_SUPPLIED_PRODUCTION_EVIDENCE**, provenance OPERATOR_SUPPLIED;
Codex did not access PI3, collect production evidence or execute the adapter/platform-status.

1. First deployment attempt failed RUNTIME_DRIFT / NOT_STARTED at 2ef66a2.
2. Exact accepted-runtime customization validation was corrected at e4d5a19.
3. Second attempt failed RUNTIME_DRIFT / NOT_STARTED at e4d5a19.
4. The raw-prefix child-probe construction was corrected at 84635cb.
5. Third attempt at `84635cb88380c590d2adfb655c37afd2118c629f` failed safely with
   DEPENDENCY_DRIFT / NOT_STARTED. No durable intent, production mutation, adapter
   execution, HA network/authentication, scheduler installation or rollback occurred.
6. Read-only evidence showed five category-B objects present/exact and compatibility.py absent.
7. Production platform-status is the known PRE_COMPATIBILITY_KNOWN_VERSION, SHA-256
   `b65464e722bf9a4da0004ecf3bb05e4105f345a87c62405ce92d97c6298b2af8`,
   jazofv1:jazofv1 mode 0755. Its existing cron is preserved. Current repository
   platform-status SHA-256 is `55f75b7945b02f5d23759cf277b0e008a407d9d71e51a9c12b40a3cd1855c733`.
8. The recent production compatibility state does not prove module deployment:
   tools/hioc-pe4-ha-registry-discovery.py record_compatibility() inserts its source-root
   pi4/lib into sys.path on POSIX, imports compatibility from the release-source tree,
   and calls refresh_status with StateStore under /home/jazofv1/hioc/state/platform.
   The PE-4.0B.2b source-tree writer can therefore produce sanitized central state
   without installing compatibility.py in production. No private state contents are recorded.
9. compatibility.py was introduced at `8187114c7233be82b188f0fc03b93a022787e7bb`,
   “HIOC: add compatibility resilience and drift diagnostics”. Its classification as
   an already existing production dependency was a preparation defect, not byte drift.
10. It is now A_NEW_FILE_TO_DEPLOY, using the ordinary additive transaction path.
11. No platform-status upgrade or general compatibility-framework deployment is bundled.

Current manifest: **five required existing dependencies, nine additive targets**.
Only compatibility.py moved category; its source bytes are unchanged. Remaining B files
retain REQUIRED_EXISTING_EXACT_PRESERVE_ABSENT_OR_DIFFERENT_FAIL_CLOSED. compatibility.py
is installed only when absent, preserved when exact, and rejected when different/unsafe;
source blob `1ba46d4ebf3819e2fa3ee9365e5b0088ba0b4a1a`, SHA-256
`713c292c09282f3be524bc8a2090de43cf0fb78a81b3c71eed143b7a0d68e952`,
owner/group jazofv1:jazofv1, mode 0644. The supplied request's SHA text had 63 characters;
the specified immutable Git blob and existing manifest establish this 64-character SHA.
The record preserves that transcription separately from the verified source identity.

Adapter direct local imports remain core.config, core.compatibility and core.state;
StateStore requires core.schemas. compatibility module-load imports are standard-library
only. The consumed safe_version/load_registry/assess/update_status call closure adds no
local dependency and does not reach mqtt_observation(), whose conditional ..mqtt import
is therefore outside the adapter path. No additional mandatory dependency was found.
Adapter, entrypoint, compatibility module and all runtime-policy source bytes are unchanged.

Compatibility installation is code-file publication only: durable intent records its
exact target/hash and created-file status; generic staged renameat2 NOREPLACE publication,
post-verification, resume and committed idempotence protections apply. Deployment never
imports compatibility.py, runs refresh_status/update_status/mqtt_observation/platform-status,
rewrites compatibility state or inventory, publishes MQTT or executes the adapter.
The accepted runtime, launch flags, customization policy and resolved-prefix correction
remain unchanged. Transaction evidence remains NOT_STARTED -> NOT_STARTED,
PREPARED -> INCOMPLETE, COMMITTED -> PASS. All three previous attempts remained NOT_STARTED.

The [production dependency correction record](../governance/pe4/pe4-ha-association-production-dependency-correction.json)
and [closed schema](../governance/pe4/pe4-ha-association-production-dependency-correction.schema.json)
bind the source/classification and operator provenance. All correction records are
repository-only governance, not additional production contracts. Runtime.contracts()
still reads six governance files. Prior correction records and commits remain immutable.
Older six-B/eight-additive statements below describe historical preparation and are
superseded by the five-B/nine-additive current manifest. Current helper source binding
requires the exact successor subject `PE-4: correct production compatibility dependency`,
immediate parent 84635cb, main/origin equality, clean tree, 0/0 and no Git operation.

Validation: deployment focused 83, runtime customization 8, adapter 73, production
dependency correction 14, other regressions 275; total 453 run, 452 passed, one existing
rsync-unavailable release skip on Windows. Tests cover absent/exact/different/unsafe,
intent, interruption immediately before/after compatibility publication, resume,
idempotence, all five required dependencies, state/platform/cron preservation and import
closure. No accepted interpreter, actual adapter/platform-status, live host or credential
is exercised. Syntax/import safety, canonical closed schemas, links, source identities,
privacy/prohibited-operation checks and diff checks are repository-only.

Adapter Implementation PASS/CLOSED, corrected before deployment; Runtime Validation
Correction PASS/CLOSED; Deployment Runtime Probe Correction PASS/CLOSED; Production
Dependency Classification Correction PASS/CLOSED; Deployment Preparation PASS/CLOSED,
corrected and rebound. Deployment, Bounded Manual Production Validation, Independent
Production Acceptance and Scheduler Deployment NOT STARTED; Public Projection DEFERRED;
PE-4 NOT COMPLETE; Phase 7A ACTIVE; Rollback NOT PERFORMED. Next unchanged:
**PE-4 Home Assistant Association Adapter Deployment Execution**. Complete operator block
is FOR REVIEW ONLY and was not run. Stop after repository correction.


## Historical Deployment runtime probe resolved-prefix correction — 2026-10-06

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


## Historical Accepted runtime validation correction — 2026-10-06

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


Permanent production-validation evidence durability rule: Closure-critical evidence must not rely solely on ephemeral /tmp storage. During the same governed checkpoint, before depending on later file-level revalidation, retain a sanitized copy in a durable governed evidence directory, persist canonical sanitized repository governance, or record required evidence-file SHA-256 identities and metadata in durable governance before loss. Preserve privacy: never persist raw private HA, inventory or credential data for durability. Hashes and metadata cannot recover lost bytes; record retention and revalidation limits. This rule covers future HIOC production validation checkpoints, without expanding into backup or disaster recovery work.

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
| PE-4 Home Assistant Runtime Credential Provisioning | PASS/CLOSED |
| Operator Credential Installation | PASS/CLOSED |
| Independent Credential Validation | PASS/CLOSED |
| Credential Provisioning Governance Closure | PASS/CLOSED |
| PE-4 Home Assistant Association Adapter Implementation | PASS/CLOSED, corrected before deployment |
| PE-4 Home Assistant Association Adapter Pre-deployment Correction | PASS/CLOSED |
| PE-4 Home Assistant Association Adapter Runtime Validation Correction | PASS/CLOSED |
| PE-4 Home Assistant Association Adapter Deployment Runtime Probe Correction | PASS/CLOSED |
| PE-4 Home Assistant Association Adapter Production Dependency Classification Correction | PASS/CLOSED |
| PE-4 Home Assistant Association Adapter Deployment Preparation | PASS/CLOSED, corrected and rebound |
| PE-4 Home Assistant Association Adapter Deployment Preparation Pre-execution Correction | PASS/CLOSED |
| PE-4 Home Assistant Association Adapter Deployment | PASS/CLOSED |
| PE-4 Home Assistant Association Adapter Bounded Manual Validation Preparation | PASS/CLOSED |
| PE-4 Home Assistant Association Adapter Bounded Manual Production Validation | PASS/CLOSED |
| PE-4 Home Assistant Association Adapter Bounded Validation Scope Correction | PASS/CLOSED |
| First Live Adapter Invocation | COMPLETED ONCE / ADAPTER PASS |
| Historical Wrapper | FAIL / MANUAL REVIEW REQUIRED |
| Post-Run Reconciliation Attempt 1 | FAIL / HISTORICAL_EVIDENCE |
| Reconciliation Evidence Authority Correction | PASS/CLOSED |
| PE-4 Home Assistant Association Adapter Durable Post-Run Reconciliation | PASS/CLOSED |
| Second Adapter Execution | NOT AUTHORIZED |
| PE-4 Home Assistant Association Adapter Independent Production Acceptance Preparation | PASS/CLOSED |
| Independent Production Acceptance Attempt 1 | FAIL / DURABLE CAPTURE |
| Read-only inspection portion | PASS (operator-supplied) |
| Durable acceptance evidence | NOT PUBLISHED |
| Independent Production Acceptance Capture Correction | PASS/CLOSED |
| Independent Production Acceptance Operator Path Integration | PASS/CLOSED |
| Native Windows capture durability prerequisite | PASS |
| Independent Production Acceptance Attempt 2 | PASS |
| PE-4 Home Assistant Association Adapter Independent Production Acceptance | PASS/CLOSED |
| PE-4 Home Assistant Association Public Projection Preparation | PASS/CLOSED |
| PE-4 Home Assistant Association Public Projection Source Implementation | PASS/CLOSED |
| PE-4 Home Assistant Association Public Projection PI3 POSIX Source Validation | PASS/CLOSED |
| PE-4 Home Assistant Association Public Projection Deployment Preparation | PASS/CLOSED WITH BASELINE CORRECTION |
| PE-4 Home Assistant Association Public Projection Deployment Baseline Correction | PASS/CLOSED |
| PE-4 Home Assistant Association Public Projection Corrected Baseline Validation | PASS |
| PE-4 Home Assistant Association Public Projection Baseline Validation Attempt 1 | FAIL / BASELINE_MISMATCH / SAFE |
| PE-4 Home Assistant Association Public Projection Deployment | PASS/CLOSED |
| PE-4 Home Assistant Association Public Projection Production Execution | PASS |
| PE-4 Home Assistant Association Adapter Scheduler Deployment Preparation | PASS/CLOSED |
| PE-4 Home Assistant Association Adapter Scheduler Deployment | PASS/CLOSED |
| Recurring Scheduler Operation | ACTIVE / AUTHORIZED |
| First Natural Scheduled Invocation | OBSERVED |
| First Natural Scheduled State Publication | PASS |
| Manual Second Adapter Execution | NOT AUTHORIZED / NOT PERFORMED |
| Public Projection Baseline Receipt | PASS / INDEPENDENTLY VERIFIED |
| Public Projection Installed-State Review | PASS |
| First Natural Public Projection Pre-Slot Observation | NOT_PROVEN / EXPECTED / NO FAILURE |
| First Natural Public Projection Inventory Cycle | PASS |
| First Natural Public Projection Count | 25 |
| First Natural Public Projection MQTT Acceptance | PASS |
| Public Projection Retained MQTT Topics | 7/7 |
| Public Projection Retained Payload Equality | PASS |
| PE-5 | COMPLETE; PE-5.9 COMPLETE/PASS; PE-6.0 COMPLETE/PASS; PE-6.1 repository implementation COMPLETE/PASS; PE-6 IN_PROGRESS; PE-6.2 next separately authorized; no production deployment/execution |
| Historical vs Current Lifecycle Test-Binding Correction | PASS/CLOSED |
| Documentation Consistency Correction | PASS/CLOSED |
| PE-4 | PASS/CLOSED |
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

### PE-4 Home Assistant Runtime Credential Provisioning Governance Closure - 2026-10-06

Operator Credential Installation PASS/CLOSED; Independent Credential Validation
PASS/CLOSED; Governance Closure PASS/CLOSED; parent Runtime Credential Provisioning
PASS/CLOSED. The [closure record](../governance/pe4/pe4-ha-runtime-credential-provisioning-closure.json)
binds unchanged corrected tool identities and OPERATOR_SUPPLIED PI3 evidence:
source fast-forward to d089be8, INSTALL, root filesystem/security/content validation,
and a separate actual jazofv1 read. Root mode correctly reported runtime readability
NOT_TESTED; the separate runtime identity reported TRUE. No rotation occurred.
Codex did not access or independently inspect PI3. No token or secret-derived
hash is recorded. Authentication remains DEFERRED_TO_ADAPTER_VALIDATION; this
closure proves local storage and readability, not HA credential validity or access.
Preparation/correction history and records are preserved. Adapter Implementation
NOT STARTED; PE-4 NOT COMPLETE; Phase 7A ACTIVE; rollback NOT PERFORMED.

The following preparation and pre-execution correction narratives describe their
historical states; the authoritative current lifecycle table and closure above
supersede their prior NOT STARTED/PREPARED statements.

### PE-4 Canonical Credential Storage Pre-execution Correction - 2026-10-06

Credential Provisioning Preparation remains PASS/CLOSED, corrected before execution.
Independent review identified missing-final-LF acceptance in original preparation
commit `afa484620d24a1d6dec2a98e7c06e613f633bfb7`, preserved in immutable Git
history. The current [provisioning contract](PE4_HOME_ASSISTANT_RUNTIME_CREDENTIAL_PROVISIONING.md)
and both tools require exactly one final LF; noncanonical existing files fail before
the hidden prompt without replacement. The closed preparation record/schema binds
corrected executable identities. The corrected PI3 block is FOR REVIEW ONLY and
uses explicit return-code handling without shell-exiting options or commands.
No operator execution occurred. Parent PREPARED / NOT COMPLETE; Installation,
Independent Validation, Governance Closure and Adapter Implementation NOT STARTED;
PE-4 NOT COMPLETE; Phase 7A ACTIVE; rollback NOT PERFORMED. Next remains the separately
authorized **PE-4 Home Assistant Runtime Credential Provisioning — Operator Installation**.

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
### PE-7.3 - Guarded PI3 delivery transaction repository preparation

Classification: CURRENT — bounded live HA Dashboard-shape correction; native qualification pending.
PE70_STATUS=COMPLETE/PASS; PE71_STATUS=COMPLETE/PASS; PE72_STATUS=COMPLETE/PASS.
PE6_STATUS=COMPLETE/PASS; PE7_STATUS=IN_PROGRESS; PE73_STATUS=IN_PROGRESS.
PE73_COMPLETE=FALSE; PE74_STATUS=NOT_AUTHORIZED; CODEX_PRODUCTION_ACCESS=FALSE.
Accepted OPERATOR_SUPPLIED filesystem qualification remains PASS and is not repeated.
New OPERATOR_SUPPLIED PI5 receipt at5fc1560a4be75e509e351eaf976364ed9bec62f1:
published source SHA verification PASS; authenticated Supervisor proxy/admin read-only
discovery PASS; HIOC integration absent/inactive; Lovelace resource mode storage.
DASHBOARD_SCHEMA_OR_LIMIT stopped discovery before any Dashboard results; mutation
false; exit1. Actual returned config type/shape/count is not present in that receipt.
It does not establish a malformed Dashboard or prove a particular strategy was used.
Core2026.10.4 returns raw stored Lovelace config; its pinned frontend20260930.5
supports static views OR a strategy. The old qualifier wrongly treated every response
as a static views list and a local32-view cap as a global discovery requirement.
The correction reports fixed-name type/presence/count diagnostics, preserves other
valid Dashboards, and never generates or selects a view. Static scan budget256 is
explicitly local; larger configs report count/omission, not an HA schema defect.
Optional path/cards/sections and generated views remain subject to the unchanged
publisher's actual additive-target requirements; nothing is filled in or migrated.
Unknown catalog rows/default source, shadowed default, legacy resources, auth or
transport failures retain fail-closed resource/qualification gates. Successful null
is not config_not_found. Partial choices survive later failures; private contents do
not enter the report. No .storage, service/write API, target selection or activation.
FOCUSED_NATIVE_VALIDATION=81_RUN_81_PASSED_0_FAILURES_0_ERRORS_0_SKIPPED.
INDEPENDENT_FOCUSED_ACCEPTANCE=PASS_FOR_DASHBOARD_SHAPE_CORRECTION_PUBLICATION.
Existing104 delivery passes remain supported by unchanged delivery/assessment/tests.
13 PI3 delivery,six HA source,39 current successor,449 protected identities verify;
contract,amendment,executive instruction,PI3 evidence and filesystem PASS preserved.
Trust/private files/SPKI/independent ACL, fresh cross-host disabled/exclusive guards,
actual live/local proof and approved target/backup remain required before delivery.
Next action: one operator-run PI5 read-only qualifier bound to this new source SHA/
commit; retain sanitized report and immediate exit status, then stop.
See [Dashboard-shape correction evidence](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-73-live-dashboard-shape-correction).

### Historical initial live API qualification preparation snapshot

Classification: HISTORICAL SNAPSHOT — accepted PI5 filesystem qualification; bounded live API discovery preparation.
PE70_STATUS=COMPLETE/PASS; PE71_STATUS=COMPLETE/PASS; PE72_STATUS=COMPLETE/PASS.
PE6_STATUS=COMPLETE/PASS; PE7_STATUS=IN_PROGRESS; PE73_STATUS=IN_PROGRESS.
PE73_COMPLETE=FALSE; PE74_STATUS=NOT_AUTHORIZED; CODEX_PRODUCTION_ACCESS=FALSE.
OPERATOR_SUPPLIED filesystem result PASS_READ_ONLY_FILESYSTEM_IDENTITY_QUALIFICATION,
exit0, source da630dd9cac20b784a6b433de614bfe323d4576f is accepted, not repeated.
PI5 HA192.168.100.251 HAOS/Core2026.10.4; Terminal/Core0:0; /homeassistant and
Core/config have matching actual filesystem identities/security/namespaces/process.
Required existing directories pass; absent hioc_operator is expected; no mutation.
Installed public source supports Lovelace storage/config, WS context/service response.
New fixed read-only API qualifier uses only the Terminal app's existing supported
Supervisor Core WebSocket proxy authentication, if already permitted. Root is not
HA authorization. Actual admin/current_user is verified; proxy admin is not a human
PE-7 editing actor. No token prompt, extraction, creation, logging or persistence;
only the normal internal authentication handshake receives the existing app token.
Missing/denied permission blocks and names existing browser-admin login as fallback.
Read-only dashboard catalog/config exports report bounded titles/paths/view choices
and resource fingerprints/conflicts, not cards, URLs/query secrets or credentials.
No target selected, duplicate dashboard, YAML migration, .storage access or API save.
Potential legacy-resource lazy import is refused before resources/list; an unprovable
default-source binding blocks rather than allowing a read-side configuration write.
HA integration absence is inactive, not unsafe. HA API observations cannot prove
fresh cross-host evaluator/scheduler/manual-caller exclusion; those guards remain
unknown/false. /local source capability is accepted; the actual route is not inferred
from an absent editor/404. Native delivery remains blocked pending the live guards,
an explicit compatible target, private full API export/backup and actual trust.
Existing strict trust_preflight remains mandatory before Delivery.prepare: real
certificate/assertion identities, private-file security, SPKI and independent ACL.
No trust exemption, issuance, activation, deployment or PE-7.4 authorization.
LIVE_QUALIFIER_IMPLEMENTATION=PASS; FOCUSED_NATIVE_VALIDATION=163_RUN_163_PASSED_0_FAILURES_0_ERRORS_0_SKIPPED.
INDEPENDENT_FOCUSED_ACCEPTANCE=PASS_FOR_BOUNDED_READ_ONLY_REPOSITORY_PUBLICATION.
13 PI3 delivery, six HA source,39 current successor and449 protected identities
verify. Existing delivery/assessment, controller/provider, contract, amendment,
executive instruction, completed PI3 deployment and historical evidence unchanged.
Next action: one operator-run PI5 live read-only API qualification bound to the new
published tool SHA/commit; retain sanitized receipt/exit status and stop.
See [live API qualification evidence](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-73-live-api-dashboard-and-disabled-role-qualification).

### Historical PID-namespace preparation snapshot

Classification: HISTORICAL SNAPSHOT — HA OS PID-namespace preflight correction; qualification pending.
PE70_STATUS=COMPLETE/PASS; PE71_STATUS=COMPLETE/PASS; PE72_STATUS=COMPLETE/PASS.
PE6_STATUS=COMPLETE/PASS; PE7_STATUS=IN_PROGRESS; PE73_STATUS=IN_PROGRESS.
PE73_COMPLETE=FALSE; PE74_STATUS=NOT_AUTHORIZED; CODEX_PRODUCTION_ACCESS=FALSE.
OPERATOR_SUPPLIED PI5 preflight at2d2ecf5b95531b2c514cc4a889aa358f9fc27365
verified source identity, selected/homeassistant, observed Core0:0, no directory
failures, integration absent and no mutation. Docker host PID731186 was not visible
in Terminal/proc: stat/status/cgroup/ns/user/root all ENOENT2. This is namespace
visibility evidence, not a filesystem-security failure or unsafe-directory finding.
The corrected qualifier never opens a Docker host PID in Terminal/proc. One fixed,
noninteractive read-only Docker exec runs stdlib metadata code in the exact Core
container under the observed Core UID/GID. It finds namespace-local Core PID, checks
credentials/user mapping/birth and opens actual Core config objects with NOFOLLOW.
Device/inode/owner/group/mode, absence and ACL checks must agree with Terminal's
secure/homeassistant proof. No mount-string-only admission, shell, extra privileges,
host PID mode, container reconfiguration or persistent service. Failure blocks.
The Core label and optional public-source location now follow the source-supported
Core layout; no exact HA version gate or production identity is invented.
FOCUSED_PID_NAMESPACE_CORRECTION=133_RUN_133_PASSED_0_FAILURES_0_ERRORS_0_SKIPPED.
INDEPENDENT_FOCUSED_ACCEPTANCE=PASS_FOR_REPOSITORY_PUBLICATION. No runtime mutation
or native delivery readiness is claimed. Existing publisher/transaction code is
unchanged.13 PI3,39 successor,449 protected and six HA source identities verify.
Trust, backups, interruption recovery, disabled behavior, runtime independence and
persistent-state isolation remain. All prior PI3/PI5 evidence retains its authority.
Next action: operator-run one consolidated read-only PI5 qualifier bound to this
published correction's exact source SHA/commit. No installation/activation authority.
See [PID-namespace correction evidence](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-73-core-pid-namespace-qualification-correction).

### Historical accepted HA preflight preparation snapshot

Classification: HISTORICAL SNAPSHOT — HA OS preflight prerequisite correction; native qualification pending.
PE70_STATUS=COMPLETE/PASS; PE71_STATUS=COMPLETE/PASS; PE72_STATUS=COMPLETE/PASS.
PE6_STATUS=COMPLETE/PASS; PE7_STATUS=IN_PROGRESS; PE73_STATUS=IN_PROGRESS.
PE73_COMPLETE=FALSE; PE74_STATUS=NOT_AUTHORIZED; CODEX_PRODUCTION_ACCESS=FALSE.
The accepted111-test HA correction and completed OPERATOR_SUPPLIED PI3 deployment
evidence are preserved. This bounded follow-up resolves fresh-install prerequisites.
Missing custom_components/hioc_operator is observed as absence, not an installation
failure. Only that fixed public directory0755 and missing private backups0700 may
be created. Private durable intent precedes creation; exact identities/readback and
Core-visible proof follow. Existing directories are never chmod/chowned or adopted.
Missing backups uses a fixed exclusive private bootstrap intent before mkdir, not
manual directory setup. Uncertain creation remains pending; no retry or auto recovery.
Explicit recovery removes only the empty, exact created HIOC directory; backup and
transaction evidence remain preserved. Missing custom_components/www remains a real
parent prerequisite. HA Core need not traverse private publisher backup storage.
Host PID mode is not a required configuration. Existing proc visibility must prove
the exact Core-container PID, process birth, credentials, user namespace and actual
Core-visible filesystem objects. Matching mount paths or archive metadata alone
are insufficient. Missing/hidden proof blocks; no new privileges, exec, namespace
entry or container change is authorized. Production support remains UNKNOWN.
FOCUSED_PREREQUISITE_CORRECTION=125_RUN_125_PASSED_0_FAILURES_0_ERRORS_0_SKIPPED.
Synthetic Windows results do not establish native Linux filesystem qualification.
All13 PI3 delivery,39 successor and449 protected identities verify; immutable HA
payload, original contract/amendment, trust design and completed PI3 evidence remain.
Disabled behavior, backups, whole-process authority, interruption evidence, runtime
independence and persistent-state isolation are preserved. No installation or Git
publication occurs here. Live HA/Dashboard/trust and native filesystem evidence
remain unverified. PE-7.3 IN_PROGRESS; PE-7.4 NOT_AUTHORIZED.
INDEPENDENT_REPOSITORY_ACCEPTANCE=PASS. The exact code/test candidate was reviewed
against all15 mandatory acceptance gates;125 focused results match unchanged bytes,
and25 preservation checks pass. Native installation/readiness is not established.
This authorized publication records repository acceptance only; no PE-7.3 closure.
Next action: operator-run consolidated read-only PI5 qualification using the accepted
preflight; unavailable Core filesystem proof blocks delivery without a workaround.
See [the prerequisite correction evidence](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-73-preflight-prerequisite-review-and-bounded-correction).

### Historical accepted111-test HA OS correction snapshot

Classification: HISTORICAL SNAPSHOT — HA OS delivery compatibility correction; native delivery unqualified.
PE70_STATUS=COMPLETE/PASS; PE71_STATUS=COMPLETE/PASS; PE72_STATUS=COMPLETE/PASS.
PE6_STATUS=COMPLETE/PASS; PE7_STATUS=IN_PROGRESS; PE73_STATUS=IN_PROGRESS.
PE73_COMPLETE=FALSE; PE74_STATUS=NOT_AUTHORIZED; CODEX_PRODUCTION_ACCESS=FALSE.
The completed PI3 deployment evidence at2784ef31da5e4ebc0e75af19695c8cc68c3d04a1
is preserved as OPERATOR_SUPPLIED; source release1c07932bd43aab1eac693ea07e195a74150fe550.
The existing six-file HA candidate is corrected, not replaced. A one-shot publisher
separates observed Terminal UID/GID0:0 from actual HA Core process ownership.
Only four pinned integration/editor files and a closed private transaction file set
are writable. Public files0644 use qualified Core UID/GID; private records0600 and
transaction directory0700 use publisher0:0. No PI3 ownership exception is introduced.
Before mutation, actual Core-visible descriptor identities must match the Terminal
destination; matching Docker mount-source strings alone are insufficient. Existing
host-PID/proc visibility is required. Missing proof or required existing directories
refuses delivery; no container changes, privilege expansion or guessed owner fallback.
FOCUSED_CORRECTION=111_RUN_111_PASSED_0_FAILURES_0_ERRORS_0_SKIPPED.
Windows descriptor/ownership models are synthetic, not native Linux qualification.
All13 PI3 delivery,39 successor and449 protected identities verify. Original contract,
amendment, controller, executive instruction and PI3 evidence remain unchanged.
Whole-process authority, private backups, durable intent, single-attempt publication,
exact readback and separate unexpected-recovery authority remain mandatory. No retries,
automatic rollback or consumer release. Existing pending transactions require disposition.
Runtime code has no publisher/transaction dependency; persistent Assets, policies,
history and configuration are outside the write scope. No permanent HA version pin,
migration, trust provisioning, activation, scheduling or service operation is added.
Remaining native requirements: actual Core/mount/ownership/security qualification,
supported live HA/API and approved Dashboard/view export, disabled guard, actual trust
identities/private validation, and native filesystem behavior. None is fabricated.
Next action: operator-run the self-contained, no-prompt read-only PI5 identity preflight
in the correction evidence. This is not installation or PE-7.4 authorization.
See [the HA OS correction evidence](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-73-ha-os-delivery-compatibility-correction-and-runtime-protection).

### Historical HA delivery preparation snapshot (superseded compatibility assumptions)

Classification: HISTORICAL SNAPSHOT — HA integration/UI/trust delivery preparation candidate.
PE70_STATUS=COMPLETE/PASS; PE71_STATUS=COMPLETE/PASS; PE72_STATUS=COMPLETE/PASS.
PE6_STATUS=COMPLETE/PASS; PE7_STATUS=IN_PROGRESS; PE73_STATUS=IN_PROGRESS.
PE73_COMPLETE=FALSE; PE74_STATUS=NOT_AUTHORIZED; CODEX_PRODUCTION_ACCESS=FALSE.
The PI3 runtime deployment is a completed, independently verified sub-checkpoint,
recorded as OPERATOR_SUPPLIED production evidence and published at
2784ef31da5e4ebc0e75af19695c8cc68c3d04a1. Its source release was
1c07932bd43aab1eac693ea07e195a74150fe550. That deployment is not reopened.
A finite HA delivery procedure now reuses six immutable PE-7.1 HA artifact identities:
four integration/editor files delivered, Dashboard/package retained as references.
Supported HA resource/card registration preserves existing layout, unrelated cards,
resources and package behavior. No .storage writes or broad installer/restart.
Private before/stage/reference/trust-packet backups and durable pending intent precede
single-attempt mutation. Interrupted operations are not automatically adopted,
retried, rolled back or released. One whole-process authority; no per-operation prompts.
The trust configuration packet preserves mTLS, assertion keys and independent ACLs
and remains disabled/offline; it is not active HA/PI3 configuration or provisioned secrets.
FOCUSED_ACCEPTANCE=69_RUN_69_PASSED_0_FAILURES_0_ERRORS_0_SKIPPED.
IMPLEMENTATION=PARTIAL_NATIVE_DELIVERY_NOT_ESTABLISHED; SYNTHETIC_PROCEDURE=PASS.
The native HA connection, live guard and two-host trust-file validation bindings
are explicit inputs, not manufactured production observations. Actual PI5 roots,
ownership/filesystem capabilities, supported APIs/resources/Dashboard and trust
placement remain required observations. No native end-to-end delivery claim is made.
All13 PI3 delivery,39 successor and449 protected identities verify; original contract,
controller, amendment, executive decision and completed PI3 evidence remain preserved.
Next action: operator-run the single consolidated read-only PI5 capability/integration
assessment below to bind actual paths/capabilities; no new research/checkpoint phase.
PE-7.3 remains IN_PROGRESS; PE-7.4 remains NOT_AUTHORIZED. No activation, migration,
notifications, credentials, service restart, PI3/PI5 access or Git publication here.
See [the integrated HA preparation evidence and assessment](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-73-integrated-ha-integration-ui-and-trust-delivery-preparation).

### Historical PI3 runtime deployment evidence snapshot

Classification: HISTORICAL SNAPSHOT — accepted PI3 runtime delivery evidence.
PE70_STATUS=COMPLETE/PASS; PE71_STATUS=COMPLETE/PASS; PE72_STATUS=COMPLETE/PASS.
PE6_STATUS=COMPLETE/PASS; PE7_STATUS=IN_PROGRESS; PE73_STATUS=IN_PROGRESS.
PE73_COMPLETE=FALSE; PE74_STATUS=NOT_AUTHORIZED; CODEX_PRODUCTION_ACCESS=FALSE.
EVIDENCE_AUTHORITY=OPERATOR_SUPPLIED. Source release1c07932bd43aab1eac693ea07e195a74150fe550.
The owner reports successful interrupted-window recovery and installation: all13
artifact SHA256 identities PASS; transactionCOMMITTED/pendingNone; windowRELEASED;
original12-entry crontab restored exactly; all3 affected HIOC jobs scheduled.
cron,pihole-FTL,unbound,nut-server are reported active. Incident-engine invocation
and recent status output observed; invocation alone does not prove engine completion.
Inventory last observed at09:30 before release; no post-release inventory execution
is established. Daily platform-status at03:17 was not expected in the observed
post-release window; no post-release platform execution is claimed. No HIOC error
matches in inspected cron logs; independent assessment reports zero failed invariants.
These are supplied observations, not a Codex production inspection or universal
service-health/event-history proof. No original receipt bytes or new production
security metadata are manufactured from the owner's summary.
Runtime deployment evidence is recorded as PASS for the supplied bounded facts.
Full PE-7.3 COMPLETE/PASS is not established: the unchanged contract section13
requires guarded artifact/integration/UI/trust delivery and observed HA API/resource
capability; section7 requires supported live Dashboard/resource delivery with backup,
not repository YAML copying. Evidence for these remaining delivery obligations is
not supplied. The approved maintenance-window evidence explicitly states that the
13-file runtime step alone does not close all PE-7.3. No new acceptance gate is added.
Next action: separately authorize completion/evidence of the existing PE-7.3 HA
integration/UI/trust delivery and capability prerequisites, keeping editing/evaluator
disabled except authorized preflight. PE-7.4 bounded functional acceptance remains
later and NOT_AUTHORIZED; no monitoring, migration or notifications are authorized.
Manual-caller restrictions remain procedural; missed/cached/retained/noncooperating
callers remain residual risks, not universally excluded. Executive instruction and
fixed-process authority remain verbatim in the unchanged successor authorization
record. Unexpected recovery, rollback or material scope changes require new authority.
See [the production evidence and closure determination](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-73-pi3-runtime-deployment-evidence-and-governance-closure-determination).

### Historical approved-process recovery correction snapshot

Classification: HISTORICAL SNAPSHOT — approved-process recovery correction, 2026-10-27.
PE70_STATUS=COMPLETE/PASS; PE71_STATUS=COMPLETE/PASS; PE72_STATUS=COMPLETE/PASS.
PE6_STATUS=COMPLETE/PASS; PE7_STATUS=IN_PROGRESS; PE73_STATUS=IN_PROGRESS.
PE73_COMPLETE=FALSE; PE74_STATUS=NOT_AUTHORIZED; CODEX_PRODUCTION_ACCESS=FALSE.
Published baseline1452534a23528af96e69b9ec030f050b61bed859. Current Windows
correction is uncommitted: five existing modified paths and one focused PE-7.3
successor authorization record. No staging, commit, push or PI3/PI5 access performed.
Owner executive decision PE73_OWNER_SEQUENCE_AUTHORIZATION_20261027 is recorded
verbatim in governance/pe7/pe73-sequence-authorization.json. It explicitly supersedes
repeated human authorization inside a previously approved fixed process. Original
contract/amendment text and historical nine-prompt decisions remain preserved.
Normal deployment and the specifically approved EXCLUDED resume now run without
per-operation prompts. Fresh technical grants, material context checks, durable
intent and all transaction/recovery safeguards remain mandatory. Unexpected
recovery, rollback or materially changed scope requires new owner authorization.
The last PI3 report is OPERATOR_SUPPLIED: source1452534a, PREPARED/pendingNone,
windowEXCLUDED, three jobs excluded/nine preserved, no installed artifacts/rollback,
journal SHA256b899a8fa79bde3c6619d6abd8217d88833c414823e7888358ed7a043b766600f.
Failure NATIVE_AUTHORIZATION_CONTEXT_DRIFT is retained. Diagnostic unrelated PID
lists were incorrectly part of context equality; the code defect is reproduced.
The exact historical changed field/PID is unknown because the context pair was not supplied.
The corrected binding retains fresh completeness, boot and exact affected-process
identities while keeping unrelated PID diagnostic churn outside authority.
The bounded resume verifies the exact raw journal anchor, PREPARED/EXCLUDED phase,
all13 current target identities, all13 stages/five backups, source and scheduler
before ATTACH. It never repeats PREPARE/PRESERVE/EXCLUDE or overwrites backups.
Approved continuation: ATTACH,DRAIN,ESTABLISH,COMMIT,AUTHORIZE_RELEASE,
RESTORE_SCHEDULER,RELEASE, with automated fresh per-operation technical validation.
FOCUSED_VALIDATION=66_RUN_66_PASSED_0_FAILURES_0_ERRORS_0_SKIPPED.
All13 delivery,39 successor and449 protected identities verify; original controller,
contract, verbatim amendment and transaction algorithms unchanged. No automatic
retry, rollback, cron restoration, release or uncertain-state adoption is introduced.
The corrected command needs these exact corrected tool bytes in release-source;
the old1452534a runner fails its hash check. Publication/source delivery has not
been performed in this assignment. No production resume/closure is claimed.
See [the recovery evidence and exact operator command](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-73-approved-process-resume-and-material-context-correction--2026-10-27).

#### Historical repository-preparation snapshot at85c1a4f1

Classification: HISTORICAL SNAPSHOT. PE73_STATUS=IN_PROGRESS_REPOSITORY_PREPARATION.
PE73_COMPLETE=FALSE; PE73_PRODUCTION_DELIVERY_AUTHORIZED=FALSE.
PE73_PI3_DELIVERY_CANDIDATE=PARTIAL; NATIVE_LIVE_COMMIT=BLOCKED_CONSUMER_COORDINATION_NOT_ESTABLISHED.
PE73_TWO_DEFECT_CORRECTION=PASS_REPOSITORY_SYNTHETIC; FOCUSED_RECHECK=ACCEPT_WITH_EXPLICIT_BLOCKER.
PE73_CONSUMER_MAINTENANCE_IMPLEMENTATION=PASS_REPOSITORY_SYNTHETIC; 104_RUN_104_PASSED.
PE73_RECOVERY_ATTACHMENT_CORRECTION=PASS_REPOSITORY_SYNTHETIC; RECOVERY_FOCUSED_RECHECK=ACCEPT_WITH_NATIVE_GATES.
PE73_NATIVE_QUALIFICATION_PREPARATION=PASS; NATIVE_QUALIFICATION=INCOMPLETE.
PE73_NATIVE_ACTION1=PASS_OPERATOR_SUPPLIED; ACTION1_EXIT_STATUS=0; COMPLETE_CALLER_COVERAGE=FALSE.
PE73_ISOLATED_DESCRIPTOR_CREATE_NOFOLLOW=PASS_OPERATOR_SUPPLIED; ISOLATED_EXIT_STATUS=0.
PE73_MODE0000_ACCESS=PASS_OPERATOR_SUPPLIED; MODE0000_EXIT_STATUS=0; DEPLOYMENT_ACCESS_RESOLVED=FALSE.
PE73_FILESYSTEM_BROKER_PROTOTYPE=PASS_EXPERIMENTAL_WINDOWS_FIXTURES; 54_RUN_54_PASSED.
BROKER_ACCESS_CONTRACT_DELTA=PROPOSED_NOT_ADOPTED; BROKER_NATIVE_INTEGRATION=NOT_AUTHORIZED.
PE73_MAINTENANCE_WINDOW_AMENDMENT=ADOPTED_OPERATOR_APPROVED_2026_10_23; ORIGINAL_CONTRACT_UNCHANGED.
WINDOW_REPOSITORY_IMPLEMENTATION=AUTHORIZED; WINDOW_NATIVE_ACCEPTANCE=NOT_ESTABLISHED; PRODUCTION=NOT_AUTHORIZED.
PE73_MAINTENANCE_WINDOW_IMPLEMENTATION=PASS_REPOSITORY_SYNTHETIC; CONTROLLER_TESTS=110_PASS; FINAL_WINDOW_TESTS=69_PASS; PRIOR_ACCEPTED_COUNTS=104_CONTROLLER_55_WINDOW; PRIOR_INTERIM_VALIDATION=110_CONTROLLER_57_WINDOW.
PE73_RELATIVE_PROCESS_DETECTION_CORRECTION=PASS_REPOSITORY_SYNTHETIC; PE73_RELATIVE_PROCESS_FOCUSED_RECHECK=ACCEPT_FOR_NATIVE_QUALIFICATION; NATIVE_QUALIFICATION=INCOMPLETE.
PE73_PUBLICATION_STABLE_SOURCE_IDENTITY=PASS_REPOSITORY_SYNTHETIC; CONTROLLER_TESTS=110_PASS; WINDOW_TESTS=69_PASS; BROKER_TESTS=54_PASS; REAL_GIT_INTEGRATION=12_PASS.
PUBLICATION_STABLE_CORRECTION_INDEPENDENT_ACCEPTANCE=NOT_PERFORMED; CORRECTION_PUBLICATION=NOT_AUTHORIZED_BY_THIS_ACTION.
Payload release remains `51398bab4e2293b578b2cdac2d0740c3738cab2f`. A clean checkout containing that immutable release in its commit ancestry can pass source integrity without a hardcoded HEAD; this does not approve tooling or authorize mutation.
See [the publication-stable identity evidence](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-73-publication-stable-source-integrity-correction).
MANUAL_CALLER_CONTROL=PROCEDURAL_ONLY; UNIVERSAL_EXCLUSION=FALSE; NATIVE_MUTATION_GATES=RETAINED.
See [the verbatim approved maintenance-window amendment](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-73-approved-maintenance-window-amendment-adoption--2026-10-23).
HISTORICAL_MAINTENANCE_REVIEW=REJECT_FRESH_PROVIDER_RECOVERY; NATIVE_MAINTENANCE_QUALIFICATION=NOT_ESTABLISHED.
The prior nine-path repository candidate is published at302a4e3f34f53fffb8299771d31c115e052b5400; this compatibility correction remains uncommitted.
Staging/publication and production operations are not authorized by this action; native qualification remains incomplete. Action 1 capability PASS is OPERATOR_SUPPLIED; native qualification remains incomplete.
The isolated descriptor/create/no-follow test is PASS_OPERATOR_SUPPLIED; native qualification remains incomplete.
The mode0000 characterization is PASS_OPERATOR_SUPPLIED; deployment access remains unresolved.
The standalone nonprivileged filesystem-broker feasibility prototype passed54 focused tests.
Its proposed access-contract delta is not adopted; native privilege/integration remain unauthorized.
Next action is independent acceptance of this exact uncommitted publication-stable
source-integrity correction before separate publication authorization. The broker remains experimental and unadopted.
See the [experimental broker evidence](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-73-experimental-filesystem-broker-feasibility-candidate).
No native enablement, production operation or isolated-test execution is authorized here.
See [delivery preparation evidence](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-73-guarded-pi3-delivery-transaction-repository-candidate).

### Historical PE-7.3 next-task snapshot before repository preparation authorization

### PE-7.3 - Guarded artifact, integration, UI and trust delivery

Classification: CURRENT. PE70_STATUS=COMPLETE/PASS; PE71_STATUS=COMPLETE/PASS.
PE72_STATUS=COMPLETE/PASS; PE7_STATUS=IN_PROGRESS; PE6_STATUS=COMPLETE/PASS.
ACCEPTED_SOURCE_COMMIT=51398bab4e2293b578b2cdac2d0740c3738cab2f.
NEXT_CHECKPOINT=PE-7.3 - Guarded artifact, integration, UI and trust delivery.
PE73_STATUS=NOT_STARTED; PE73_AUTHORIZED=FALSE.
Separate authorization is required. PE-7.2 accepts OPERATOR_SUPPLIED release-source
synchronization only. No runtime deployment, HA integration installation, service
change, operational credentials, Asset migration, monitoring or notification
activation is authorized here.
See the [PE-7.2 Evidence Report](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-72-release-source-synchronization-acceptance-and-governance-closure)
and [accepted checkpoint sequence](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION_CONTRACT.md#13-bounded-checkpoint-sequence-and-implementation-scope).
No automatic follow-on action.

### Historical PE-7.2 next-task snapshot before source synchronization acceptance

### PE-7.2 - Operator-only exact release-source synchronization

Classification: CURRENT. PE70_STATUS=COMPLETE/PASS; PE71_STATUS=COMPLETE/PASS.
PE71_INDEPENDENT_ACCEPTANCE=ACCEPT; PE71_FOCUSED_RECHECK=ACCEPT.
PE7_STATUS=IN_PROGRESS; PE6_STATUS=COMPLETE/PASS.
NEXT_CHECKPOINT=PE-7.2 - Operator-only exact release-source synchronization.
PE72_STATUS=NOT_STARTED; PE72_AUTHORIZED=FALSE.
Separate authorization is required. No PI3 source synchronization, runtime delivery,
HA integration installation, Asset migration, monitoring or recurring activation is
authorized here. PE-7.1 repository implementation acceptance does not establish
production operation. See the [implementation Evidence Report](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#final-pe-71-independent-acceptance-and-governance-closure)
and [accepted checkpoint sequence](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION_CONTRACT.md#13-bounded-checkpoint-sequence-and-implementation-scope).
No automatic follow-on action.

### Historical PE-7.1 candidate before independent acceptance

### PE-7.1 - Repository implementation and native validation

Classification: CURRENT. PE70_STATUS=COMPLETE/PASS; PE70_INDEPENDENT_CONTRACT_ACCEPTANCE=PASS.
PE7_STATUS=IN_PROGRESS; PE7_DESIGN_STATUS=COMPLETE; PE6_STATUS=COMPLETE/PASS.
PE71_STATUS=CANDIDATE_READY_FOR_INDEPENDENT_ACCEPTANCE; PE71_STARTED=TRUE; PE71_IMPLEMENTATION_AUTHORIZED=TRUE.
The separately authorized Windows-only [implementation candidate](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md)
follows [the accepted PE-7 contract](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION_CONTRACT.md).
Repository native validation PASS: 3236 run, 3192 passed, 44 individual skips, 5 class-level skips, zero failures/errors.
Unexecuted-test limitations are recorded in implementation evidence. Independent
implementation acceptance remains NOT_PERFORMED; PE71_COMPLETE=FALSE.
NEXT_ACTION=INDEPENDENT_PE71_IMPLEMENTATION_CANDIDATE_ACCEPTANCE.
PE72_STATUS=NOT_STARTED; PE72_AUTHORIZED=FALSE. No commit or push is authorized.
PE7_PRODUCTION_AUTHORIZED=FALSE; PE7_MONITORING_EXECUTION_AUTHORIZED=FALSE;
PE7_RECURRING_ACTIVATION_AUTHORIZED=FALSE. No automatic follow-on action.

### Historical PE-6.5 handoff snapshot before PE-7.0 preparation

### PE-7 - Expected Availability & Permanent IoT Monitoring

Classification: CURRENT. Phase 7A ACTIVE; PE6_STATUS=COMPLETE/PASS; PE6_5_STATUS=COMPLETE/PASS.
PE7_STATUS=NOT STARTED / NOT AUTHORIZED; PE7_STARTED=FALSE; PE7_AUTHORIZED=FALSE.
NEXT_CHECKPOINT=PE-7 - Expected Availability & Permanent IoT Monitoring.
PE-6 closure establishes eligibility only. Separate PE-7 authorization is required;
existing PE-7 scope and roadmap sequencing remain unchanged. No implementation,
production action or automatic follow-on is authorized. STOP.

### Historical PE-6.4 closure handoff snapshot before PE-6.5 completion

### PE-6.5 - Final PE-6 governance closure and PE-7 handoff

Classification: CURRENT. Phase 7A ACTIVE; PE5_STATUS=COMPLETE; PE6_STATUS=IN_PROGRESS.
PE6_4_STATUS=COMPLETE/PASS; INDEPENDENT_REPOSITORY_ACCEPTANCE=ACCEPT.
PE6_5_STATUS=NEXT / NOT STARTED; PE7_STARTED=FALSE.
NEXT_CHECKPOINT=PE-6.5 - Final PE-6 governance closure and PE-7 handoff.
The PE-6.4 prerequisite is accepted. Separate authorization is required for PE-6.5:
repository-only final PE-6 closure and PE-7 handoff after all required evidence,
without repeated production action. No PE-6.5 work or PE-7 implementation begins here.
See the current PE-6.4 Evidence Report in Implementation Status and the
[accepted PE-6.5 roadmap](PE6_CLASSIFICATION_CONTRACT_DESIGN.md#pe-65--final-pe-6-governance-closure-and-pe-7-handoff).
No production access, classification execution, recurring activation or automatic
follow-on action is authorized. STOP.

### Historical timestamp-correction objective snapshot before PE-6.4 closure

### PE-6.4 - Bounded Execution and Independent Production Acceptance

Classification: CURRENT. Phase 7A ACTIVE; PE-4 PASS/CLOSED; Public Projection PASS/CLOSED.
PE5_STATUS=COMPLETE; PE6_STATUS=IN_PROGRESS.
PE6_0_STATUS=COMPLETE/PASS; PE6_1_STATUS=COMPLETE/PASS;
PE6_2_STATUS=COMPLETE/PASS; PE6_3_STATUS=COMPLETE/PASS.
PE6_REPOSITORY_IMPLEMENTED=TRUE; PE6_PRODUCTION_DEPLOYED=TRUE.
DEPLOYMENT_SCOPE=DISABLED_EXACT_FOUR_FILE_INSTALLATION_ONLY.
PE6_PRODUCTION_EXECUTION_ESTABLISHED=FALSE; PE6_4_STARTED=FALSE.
NEXT_CHECKPOINT=PE-6.4 - Bounded Execution and Independent Production Acceptance.
Separate authorization is required for PE-6.4. No scheduler or automatic activation is authorized.

PE-6.3 accepts only OPERATOR_SUPPLIED PI3 disabled-installation evidence from
source 723c1e71ad2d54e5088c0849ccee59857cbe0794. Four exact new artifacts were
installed without overwriting existing files; seven observed dependencies were preserved.
Codex did not access PI3. No caller execution, initialization, cron change,
service restart, scheduled activation or PE-6.4 execution occurred in this checkpoint.
The inspected activation locations returned no matches; universal indirect invocation
absence and current production health are not established.
Runtime inventory.py differs from source; only KNOWN_FIELDS, OPERATOR_ROLES and
normalize_mac AST definitions were reported equal. Full runtime compatibility is not established.
Rollback was NOT PERFORMED and is not claimed tested. No pre-existing dependency may be removed.
See [PE-6.3 Evidence Report](PE6_CLASSIFICATION_IMPLEMENTATION.md#pe-63-disabled-runtime-installation-acceptance-and-closure).
PE-6 remains IN PROGRESS. PE-6.4 is NEXT / NOT STARTED; PE-6.5 closure and PE-7 remain later.
### Timestamp compatibility correction prerequisite

TIMESTAMP_CORRECTION=REPOSITORY_ONLY; CORRECTED_ARTIFACT_DEPLOYED=NOT_ESTABLISHED.
PE6_4_STARTED=FALSE; PE6_PRODUCTION_EXECUTION_ESTABLISHED=FALSE.
The operator reported inventory.updated=2026-10-17T11:00:02-06:00,
198 parseable devices and freshness at inspection only (OPERATOR_SUPPLIED).
The PE-6.3 installed classifier rejects that accepted PE-5 aware-time form.
The repository correction accepts aware offsets and emits UTC without rewriting inputs.
Production still requires separate operator source synchronization, guarded replacement
of classification.py only, then separately authorized bounded PE-6.4 execution.
No deployment, caller execution, scheduling, PE-6.4 closure or PE-7 is authorized here.
See [Timestamp correction evidence](PE6_CLASSIFICATION_IMPLEMENTATION.md#timestamp-compatibility-correction-prerequisite-to-pe-64).

STOP after the repository correction. No automatic follow-on action is authorized.

### Historical accepted PE-6.0 next-task snapshot at ea4a93fba1615af1d6641c7f0683b8e912c03d72

### PE-6.1 - Private classification implementation and comprehensive repository validation

Classification: HISTORICAL_INTENTIONALLY_PRESERVED accepted PE-6.0 snapshot. PE5_STATUS=COMPLETE; PE6_STATUS=DESIGN_COMPLETE_RUNTIME_NOT_IMPLEMENTED.
PE6_0_STATUS=COMPLETE_CONTRACT_DESIGN; PE6_RUNTIME_IMPLEMENTED=FALSE.
NEXT_CHECKPOINT=PE-6.1 - Private classification implementation and comprehensive repository validation.
Separate authorization is required for PE-6.1, including adoption or revision of the proposed design.
This checkpoint authorizes no runtime implementation, production operation or PE-7 work.

The [PE-6 contract design](PE6_CLASSIFICATION_CONTRACT_DESIGN.md) inventories actual
capabilities and preserves the complete original authorization, twenty evidence-backed
technical decisions, exact private schema proposal and six-checkpoint roadmap.
Proposed role suggestions and metadata-quality summaries remain private, deterministic
and separate from operator-owned Asset data and public operational role/health.
Asset schema1.0 and the accepted PE-5.9 governance/runtime remain unchanged.
No PE-6 persistence, cron, inventory hook or public projection is selected.
Actual production inputs/locks/runtime state remain UNKNOWN; only later bounded operator
gates may establish them. All previous OPERATOR_SUPPLIED evidence limitations remain.

### Historical accepted PE-5.9 handoff at d6f9d3c6bd07b16fc515ae531b6aa0a3e9188221

### PE-6 - Classification & Metadata Quality

Classification: HISTORICAL_INTENTIONALLY_PRESERVED. Phase 7A ACTIVE; PE5_STATUS=COMPLETE.
PE5_9_STATUS=COMPLETE/PASS; PE5_8_STATUS=COMPLETE/PASS.
NEXT_CHECKPOINT=PE-6 - Classification & Metadata Quality; PE6_STARTED=FALSE.
Separate authorization is required for PE-6. PE-6 implementation is NOT authorized.

All 37 original PE-5 requirements and all 14 Definition of Done conditions pass;
all 11 roadmap UNKNOWN decisions have evidence-backed resolutions. The original
roadmap and 46 implementation checklist items remain immutable authority.
The current coverage/evidence ledger and complete private handoff are in
[PE-5 implementation evidence](PE5_CONFIGURED_ASSOCIATION_IMPLEMENTATION.md#current-pe-59-final-closure-and-private-pe-6-handoff)
and final_closure in the existing implementation governance record.
PE-5.6/7/8 accepted observations remain OPERATOR_SUPPLIED. Preserve
OPERATOR_OBSERVATIONS_ONLY; FULL_PRODUCTION_BYTES_NOT_RECEIVED;
NO_NATURAL_FAULT_OR_NATIVE_CRASH_CLAIM; NO_CURRENT_FRESHNESS_CLAIM.
First-cycle fields not separately supplied remain UNKNOWN; none is a completion
waiver or new production observation. No runtime, scheduler, public interface,
MQTT or production change occurs here. PE-6 may later consume only validated,
confirmed, unexpired private relationship evidence under the unchanged contract.
Publication remains gated by exact commit, push and independent GitHub verification.

### Historical PE-5.8 closure at 10b9c9929f740f3cd24c1768998f854d4837c3bb

### PE-5.9 - Final PE-5 Closure and PE-6 Handoff

Classification: HISTORICAL_INTENTIONALLY_PRESERVED. Phase 7A ACTIVE; PE-5 IN_PROGRESS.
PE5_6_STATUS=COMPLETE/PASS; PE5_7_STATUS=COMPLETE/PASS; PE5_8_STATUS=COMPLETE/PASS.
RECURRING_EXECUTION_ACTIVE=TRUE; PE5_9_STARTED=FALSE.
Current next checkpoint: PE-5.9 - Final PE-5 Closure and PE-6 Handoff.
Separate authorization is required for PE-5.9. It has not started; PE-5 is not yet closed.

OPERATOR_SUPPLIED read-only observations establish the required minimum of three
consecutive natural successful scheduler windows (:17, :32, :47 on 2026-10-14).
No manual producer execution occurred during PE-5.8; PE-5.6's bounded manual run
is historical and is not counted. PE-5.7 activation remains historical accepted evidence.
Cycle1 evaluated_at=2026-10-14T20:17:02.619461Z;
output SHA256 a5bea06825a63b1cd29ac705defe1066cc1f97ac678648d5fd97d9e322ebfe90;
CONFIRMED transaction dur_104bbbd8cb45467b8a53cc7d88dc497a.
Cycle2 evaluated_at=2026-10-14T20:32:01.823448Z;
output SHA256 c28f22d1272031a6586ee1673719c8b1061e06a2c120237df2140e8007082a7a;
CONFIRMED transaction dur_f70cd9091d5b4536929b329deac70e22.
Cycle3 evaluated_at=2026-10-14T20:47:02.451624Z;
output SHA256 aff03e297ae81bc9a9deff52884d2779b6138eb4b2f8592fe05f78272aa98120;
CONFIRMED transaction dur_e7a270926be543808b7711c5885778d7.
Second/third sidecar confirmed SHA equals its corresponding observed output SHA;
candidate=None. First CONFIRMED state/transaction was supplied, but a separate
confirmed_sha256 field was not supplied and is not fabricated.
Source revision1 and SHA256
961b72e8918606caeac565a8d472d03c4784d9a3b43eae6deb4085865330d295
remained unchanged. Third source sidecar also confirms that SHA/revision.
The accepted scheduler SHA256 remained
3f56b904fc1dd40ccbfa3fdd61cb910c4d215e9ac28a9bf2dcdf3721c73b62a9,
with one marker and one entry; cadence 2,17,32,47 * * * * and command unchanged.

Second/third outputs report schema2.0 VALID, configured VALID/revision1 with
one candidate and zero rejections; local eight associations and zero rejections.
LOCAL_STATE=None is a reported lookup: the closed local envelope has no state
field. Local schema1.0 is embedded unchanged in combined schema2.0.
Third valid_until=2026-10-14T21:05:02.000000Z is within the accepted upper bound;
its earlier deadline is consistent with the inventory expiry cap. Exact third
inventory.updated was not supplied and is not inferred.

Overlap, missed-cycle/no-catch-up, expiry, failure, restart/corruption and durability
semantics are supported by committed contract/static implementation and passing
synthetic Windows fixtures, as PE-5.2 explicitly permits. They are NOT claimed as
naturally observed faults or native PI3 crash tests. No artificial production
fault, manual execution or production mutation was performed for this acceptance.
Full production envelopes/crontab bytes were not independently received; supplied
production SHA values are operator observations, not independently recomputed hashes.
Current freshness beyond the supplied observation times is not asserted.
The earlier two-cycle STOP is preserved as process history; the third observation
resolved it without waiving any requirement. Existing PE-5.6/7 history remains preserved.
See [implementation evidence](PE5_CONFIGURED_ASSOCIATION_IMPLEMENTATION.md) and
operational_acceptance in the existing governance record for exact receipts,
evidence limitations and repository validation. No runtime or authority model changes.
Codex accessed no PI3, PI5 or production. PE-5.9 requires separate authorization.

### Historical PE-5.7 closure at de0279fd3667e096fd940b80d20a096f7082e8ac

### PE-5.8 - Operational Evidence and Independent Production Acceptance

Classification: HISTORICAL_INTENTIONALLY_PRESERVED. Phase 7A ACTIVE; PE-5 IN_PROGRESS.
PE5_6_STATUS=COMPLETE/PASS; PE5_7_STATUS=COMPLETE/PASS.
RECURRING_EXECUTION_ACTIVE=TRUE; PE5_8_STARTED=FALSE.
Current next checkpoint: PE-5.8 - Operational Evidence and Independent Production Acceptance.
Separate authorization is required for PE-5.8. No PE-5.8 work is performed here.

OPERATOR_SUPPLIED evidence reports one separately authorized jazofv1 scheduler
activation: PASS_PE5_7_SCHEDULER_ACTIVATION. The accepted entry is exactly:
2,17,32,47 * * * * /usr/bin/python3 /home/jazofv1/hioc/pi4/bin/hioc-compose-service-associations.py
Marker: # HIOC_PE5_SERVICE_ASSOCIATIONS. Marker count1, entry count1,
unexpected PE-5 entry count0. Before crontab SHA256:
8f900f4679aa861b02e781a61927683db5900ddfe159d78c3831a1595ae7fe71.
After/install/read-only-verification SHA256:
3f56b904fc1dd40ccbfa3fdd61cb910c4d215e9ac28a9bf2dcdf3721c73b62a9.
Full crontab bytes were not independently received; these hashes and exact
post-install-byte verification are operator observations, not repository-derived hashes.
Existing jobs were reported preserved, including the governed PE-4 5/35 entry.

Activation did not manually execute the composer, execute the installer, or access MQTT.
The command uses the existing internal shared nonblocking lock; no execution-model,
runtime implementation, persistence, public inventory or authority change is made here.
The disabled deployment template remains byte-identical and commented; activation
changed the operator's crontab, not that source artifact.

Pre-activation PI3 source HEAD/origin were reported as
4990c62afbce22a804229f3cb8329986741067a6 with empty porcelain status.
No synchronization to PE-5.6 closure commit 21ca5f676bb96d376b3a6f098decfecfe3c6ea49
is inferred. Immutable Git comparison establishes unchanged runtime payload between
those commits; reported composer and disabled-template hashes match accepted bytes.

Separate post-activation read-only verification reported the same crontab hash,
one marker, one accepted entry and no unexpected PE-5 entry.
NO_RELEVANT_PROCESS_MATCH records only that instant. It does not prove no natural
scheduled cycle has ever occurred. Natural-cycle evidence is NOT ESTABLISHED.
No current generated-output freshness, recurring operational acceptance or naturally
observed overlap/missed-cycle/staleness/failure behavior is claimed.
PE-5.8 retains its natural-cycle and independent production acceptance requirements.
PE-5.6 first-failure, corrected-deployment and bounded-execution evidence remains historical.
Codex performed repository work only; no PI3/PI5/production access or mutation occurred.
See [implementation evidence](PE5_CONFIGURED_ASSOCIATION_IMPLEMENTATION.md) and the
existing governance record's scheduler_activation evidence.


### Historical PE-5.6 closure at 21ca5f676bb96d376b3a6f098decfecfe3c6ea49

### PE-5.7 - Conditional Execution Activation

Classification: HISTORICAL_INTENTIONALLY_PRESERVED. Phase 7A ACTIVE; PE-5 IN_PROGRESS.
PE5_6_STATUS=COMPLETE/PASS; PE5_7_STARTED=FALSE; RECURRING_EXECUTION_ACTIVE=FALSE.
Current next checkpoint: PE-5.7 - Conditional Execution Activation.
PE-4/Public Projection remain PASS/CLOSED; PE-5.1 remains accepted/closed.

OPERATOR_SUPPLIED production evidence establishes corrected one-artifact deployment
of commit 4990c62afbce22a804229f3cb8329986741067a6, then one separately authorized
corrected initial installation PASS_PRIVATE_PERSISTENCE / CONFIRMED_DURABLE_CURRENT,
then exactly one separately authorized bounded composer execution
PASS_PRIVATE_ASSOCIATIONS / ACCEPTED_COUNT=1 / REJECTED_COUNT=0.
This is not recurring execution. No second corrected installation or extra composer
execution is authorized by closure. PE-5.7 has not executed; scheduler remains disabled.

The first initialization WRITE_FAILED / LOCK_UNAVAILABLE remains historical evidence.
The correction fixed missing-directory bootstrap before the shared lock; no lock
contention was established. Failed-attempt absence evidence and the intact candidate
are preserved alongside the accepted correction and separately authorized success.

Configured source revision1 SHA256:
961b72e8918606caeac565a8d472d03c4784d9a3b43eae6deb4085865330d295.
Configured relationship:
mqra_01d1d5edfdc1db0fa63b14b5b9b0b9701b4ff183a946fcb63751fb14910fe028.
Provenance: operator_mqtt_v1 / configured_mqtt / declared_endpoint_device_v1.
Generated output SHA256:
f1b219dc413325a557c71e3561804afcc3bdf26f87d2d6fdb71bb3e7c97f5e2c.
Both durability domains were observed CONFIRMED, candidate=null, bound to revision1;
exact transaction identities, metadata and source/output observations are recorded in
the existing implementation governance record's production_validation evidence.

The local branch retained eight existing_service_ownership/high relationships under
unchanged schema1.0 / 2100-second policy. The receipt is historically bound to consumed
inventory SHA256 394b5cf4007fccd1aec0beb862f29ed6dfb78a76a2903cb6174b08f0c5d17607,
updated 2026-10-14T17:00:01.000000Z, evaluated 2026-10-14T17:04:50.224530Z,
valid_until 2026-10-14T17:24:50.224530Z. Later observed inventory SHA differed;
its cause is UNKNOWN, the difference alone is not a defect and does not rebind the
receipt. No present receipt consumability or freshness is asserted.

The bounded public-inventory search for the five reported configured-MQTT terms found
zero matches: PASS for that check only. No universal privacy/transport claim is made.
Post-execution operator checks reported clean source at the correction commit,
unchanged corrected artifact, private0700 directories/0600 single-link files,
NO_PE5_CRONTAB_MATCH and NO_RELEVANT_PROCESS_MATCH.
Repository-derived checks separately reproduced the source SHA/size, relationship ID,
output-sidecar SHA/size and timing bound; full output bytes were not independently received.
All required committed Windows suites passed before closure; native fault/crash evidence
and PE-5.8 natural-cycle requirements are not waived. Codex accessed no production system.
See [implementation evidence](PE5_CONFIGURED_ASSOCIATION_IMPLEMENTATION.md).
Separate authorization is required for PE-5.7. Do not activate or implement it here.


### Historical PE-5.6 correction pending deployment at 4990c62afbce22a804229f3cb8329986741067a6

### PE-5.6 - Bounded Mapping and Storage Production Validation

Classification: HISTORICAL_INTENTIONALLY_PRESERVED. Phase 7A ACTIVE; PE-5 IN_PROGRESS; PE-4 and Public Projection PASS/CLOSED.
PE5_3_STATUS=COMPLETE_REPOSITORY_IMPLEMENTATION.
CURRENT_PE5_CHECKPOINT=PE-5.6.
PE5_6_STATUS=BLOCKED_PENDING_CORRECTED_DEPLOYMENT_AND_SEPARATE_RETRY.
PE5_7_STARTED=FALSE. Recurring execution remains disabled.

OPERATOR_SUPPLIED evidence reports PE-5.5 installed the accepted six-artifact disabled
payload. The first PE-5.6 approved revision-1 source installation returned
WRITE_FAILED / LOCK_UNAVAILABLE. This was missing infrastructure, not lock contention.
Post-failure observation established config exists, jazofv1:jazofv1 mode0755; no
config/enrichment, source, source sidecar, state/enrichment, output parent, lock,
output or output sidecar existed; no relevant installer/composer process was running.
Candidate /home/jazofv1/pe5-mqtt-mappings-candidate.json remained intact,
SHA256 961b72e8918606caeac565a8d472d03c4784d9a3b43eae6deb4085865330d295.

The implementation incorrectly required the shared lock parent to preexist before
initialization. Repository correction now bounds directory creation to approved
initial source installation. No retry has occurred. Corrected production deployment
is NOT ESTABLISHED. Source state does not prove production state.
Next operator actions: independently accept repository correction, synchronize exact
accepted source, replace only changed accepted payload bytes, independently accept
corrected deployment, then separately authorize the PE-5.6 initialization retry.
No composer invocation, scheduler activation, recovery, or PE-5.7 is authorized here.
See [configured association implementation](PE5_CONFIGURED_ASSOCIATION_IMPLEMENTATION.md).
Separate authorization is required for the retry and every later checkpoint.


### Historical PE-5.3 repository completion at 348f9787ae0ab364570a2ba07ada9527fc8db0e2

Classification: HISTORICAL_INTENTIONALLY_PRESERVED.
### PE-5.3 repository implementation complete

Classification: HISTORICAL_INTENTIONALLY_PRESERVED. PE5_3_STATUS=COMPLETE_REPOSITORY_IMPLEMENTATION; PE5_4_STARTED=FALSE.
Current next checkpoint: PE-5.4 - PI3 Release Source Synchronization.
The configured mapping resolver, private POSIX composer/store, explicit source installer
and bounded durability recovery are implemented in the repository. Activation remains
disabled; no source provisioning, PI3 synchronization, deployment or production execution
has occurred. PE-5 remains IN_PROGRESS, PE-5.1 remains accepted/closed, PE-4 and Public
Projection remain PASS/CLOSED, and Phase 7A remains ACTIVE.
The PE-5.2 design and its corrected durability contract are unchanged authority.
See [PE-5.3 repository implementation](PE5_CONFIGURED_ASSOCIATION_IMPLEMENTATION.md) and its exact governance payload.
Separate authorization is required for PE-5.4 and every later lifecycle checkpoint.


### Historical PE-5.2 complete contract design closure at 72e878f9c0c8f5d3fe6357979e045943f3cf9d34

Classification: HISTORICAL_INTENTIONALLY_PRESERVED PE-5.2 lifecycle snapshot at 72e878f9c0c8f5d3fe6357979e045943f3cf9d34. PE5_2_STATUS=COMPLETE_CONTRACT_DESIGN; PE5_3_STARTED=FALSE.
Original mapping authority/store/freshness UNKNOWNs resolved by explicit governed design, not assumed historical deployment. All 30 decisions closed in [the contract](PE5_MAPPING_CONTRACT_DESIGN.md). No runtime/prod activity occurred. Next separately authorized PE-5.3. Accepted PE-5.1 foundation below remains current evidence, not reopened.

### PE-5.1 deployment and first native execution — accepted current state

Classification: CURRENT. The formerly current policy-candidate and pre-production
sequencing statements were STALE_REQUIRES_UPDATE. They are retained below as
HISTORICAL_INTENTIONALLY_PRESERVED snapshots of their original checkpoint.

PE5_1_SNAPSHOT_AGE_POLICY_STATUS=SELECTED_FINALIZED
PE5_1_MAX_SNAPSHOT_AGE_SECONDS=2100

The policy was independently accepted, committed and pushed in
ed3a80508d101652bac89e1dcc111167670aaebc (PE-5.1: select snapshot age policy),
whose parent is eda8c9930d7f7fbf09bcc08b252bef05b385cf7e.
Independent GitHub verification and PI3 source synchronization completed.
OPERATOR_SUPPLIED source evidence establishes /home/jazofv1/hioc-release-source,
main, HEAD=origin/main=ed3a80508d101652bac89e1dcc111167670aaebc,
ahead/behind=0/0 and a clean source tree. That source-sync checkpoint performed
no production deployment; deployment and execution were separately authorized later.

OPERATOR_SUPPLIED production evidence establishes:
PASS_PE5_1_PRODUCTION_DEPLOYMENT; two authorized runtime artifacts installed,
DEPLOYED_SET_VERIFIED=true and PROTECTED_SURFACES_UNCHANGED=true;
TRANSACTION_STATUS=ABSENT, ROLLBACK=NOT_PERFORMED, MANUAL_REVIEW_REQUIRED=false.
The deployment itself executed neither PE-5.1, the inventory engine nor the adapter.
The corrected historical-journal gate is closed; the valid COMMITTED historical
PE-4 association journal remained protected and unchanged. No journal revalidation
or cleanup is required by this documentation reconciliation.

The installed artifacts are:
- pi4/lib/hioc/service_association.py: SHA-256
  dfdbab8bea085dfa0755e61b1952ee7991d663055c1f58b715997af751260bc5;
  Git blob e7a758dd8187027b50e01b1f3edde06be6f44f86; mode 0644; UID/GID 1000/1000.
- pi4/bin/hioc-resolve-local-services.py: SHA-256
  6e22fdd9f5e6e4d2d6d9540aa97a17c4927818ed688198cfda52887fc3b0ffef;
  Git blob 9c756dd0c928509252afa2a6bf4c367c6fb5f47f; mode 0755; UID/GID 1000/1000.

The separately authorized first native production execution is accepted:
PASS_PE5_1_FIRST_NATIVE_PRODUCTION_EXECUTION; SOURCE_COMMIT=
ed3a80508d101652bac89e1dcc111167670aaebc; execution count exactly 1;
caller return code 0; private output valid and closed schema valid.
INVENTORY_PATH=/home/jazofv1/hioc/state/inventory/inventory.json;
INVENTORY_UPDATED=2026-10-13T14:30:02-06:00;
EVALUATED_AT=2026-10-13T20:59:18.120272Z;
SNAPSHOT_AGE_SECONDS=1756.120272, fresh under the explicit 2100-second policy.
The private result contained 8 service associations and 0 rejections;
STDOUT_BYTES=3826 and STDERR_BYTES=0. No raw private association material is recorded.
These eight private results are not public inventory authority.

Inventory and public inventory remained unchanged. No persistent PE-5.1
association state was created. Neither the deployment nor first-execution block
intentionally executed the inventory engine or PE-4 adapter, mutated cron or
scheduler configuration, restarted a service, published MQTT, accessed Home
Assistant or accessed credentials. These are operator-supplied observations,
not independent Codex production observations or claims about unrelated activity.

PRIVATE_STATE_REQUIREMENT=DEFERRED_NOT_REQUIRED_FOR_OFFLINE_CALLER.
The first manual execution authorization is exhausted; no repeat execution,
producer integration, persistence, scheduler, MQTT mapping/subscription/publication
or public projection is authorized by this closure. PE-5 remains in progress;
this accepted PE-5.1 checkpoint does not complete the wider PE-5 capability.
Phase 7A remains ACTIVE; PE-4 and Public Projection remain PASS/CLOSED.

NEXT_CHECKPOINT=PE-5.2 - Mapping Source Authority and Complete Contract Design.
Historical reconstruction correctly found no named successor before this planning task. This separately authorized decomposition now fixes PE-5.2 through PE-5.9; technical unknowns belong to predefined gates. PE-6 onward, surveillance and Active Discovery remain later/postponed. No implementation or production command is prepared here.

### Historical policy-selection candidate at ed3a80508d101652bac89e1dcc111167670aaebc

Classification: HISTORICAL_INTENTIONALLY_PRESERVED. The following candidate text
and its original marker names describe the policy preparation checkpoint, not
current authorization, completion or sequencing.

<!-- PE5_1_CURRENT_POLICY_BEGIN -->
PE5_1_SNAPSHOT_AGE_POLICY_STATUS=SELECTED_CANDIDATE_PENDING_COMMIT
PE5_1_MAX_SNAPSHOT_AGE_SECONDS=2100

Explicit user-approved operational policy informed by OPERATOR_SUPPLIED production evidence:
accept finalized inventory when evaluation_time - inventory.updated <= 2100 seconds;
reject age > 2100 seconds, including one microsecond beyond the boundary.
Existing future-timestamp rejection remains unchanged. The pure resolver and offline caller
retain required explicit age/time inputs, no policy default, and byte-identical runtime code.

Observed */30 cadence, active cron/canonical command and synchronized NTP accompanied two
natural refreshes. Previous-snapshot ages at replacement were approximately 1801.594635 and
1800.903011 seconds; new-snapshot ages at observation were 6.096861 and 5.739757 seconds.
Engine duration bounds were several seconds. The directly observed producer hashes match
historical deployment authority: engine 5c12a368d8db7b045348cf201331c5e24390fbfe715fe399a4afef79fa594ca0;
inventory module df1dc4e2de7d8d77b54acdcb3f340281ead6cc03d74a73ad59b2864b03564503.
These are OPERATOR_SUPPLIED production observations linked to IMMUTABLE_REPOSITORY_FACT authority.
No final capture_summary was obtained; termination cause remains UNKNOWN and bounded logs
do not prove complete failure history. No additional long capture is required for this decision.

1800 seconds is too strict for the observed normal replacement window. The selected 2100 seconds
allows 300 seconds of operational tolerance beyond the scheduled 1800-second cadence.
It refuses an unchanged snapshot after 35 minutes, before a second full scheduled interval.
A skipped nonblocking flock attempt does not refresh inventory.updated or extend this allowance.
Five minutes of jitter was NOT observed; 2100 is neither a measured worst-case bound nor a
guarantee for future successful cycles. Longer collection/scheduling delay fails closed.

Repository and independently accepted PI3 release source are at eda8c9930d7f7fbf09bcc08b252bef05b385cf7e.
Source synchronization does not prove production state. PE-5.1 production deployment/use,
runtime execution/integration and the next implementation checkpoint remain NOT AUTHORIZED.
No producer hook, persistence, scheduler, cadence, MQTT, HA, credentials or public contract changes.
PRIVATE_STATE_REQUIREMENT=DEFERRED_NOT_REQUIRED_FOR_OFFLINE_CALLER.
Current policy selection replaces historical UNKNOWN only; historical records remain immutable.
Next action: CONCISE_INDEPENDENT_CANDIDATE_ACCEPTANCE; STOP before commit or push.
<!-- PE5_1_CURRENT_POLICY_END -->

### Historical caller checkpoint at eda8c9930d7f7fbf09bcc08b252bef05b385cf7e

**PE-5.1 - Runtime/Caller Integration Preparation: bounded repository caller candidate**

Separate user authorization permits this repository-only caller checkpoint. Phase 7A ACTIVE;
PE-4 PASS/CLOSED; Public Projection PASS/CLOSED. The accepted private pure resolver remains
committed at e30e483d7e5ede1cde1f75bc25bc65ff4ec115b1, without redesign.
The candidate adds an explicit offline caller for a privately supplied finalized inventory file.
No inventory-engine hook, writer, persistence, scheduler, MQTT or public projection is added.
Production deployment/use and the next PE-5 checkpoint remain NOT AUTHORIZED.
Snapshot-age policy remains UNKNOWN_REQUIRED_BEFORE_OPERATIONAL_USE.
Current work: validate and independently review the caller candidate; commit/push require separate authorization.
[Caller design and source evidence](PE5_LOCAL_SERVICE_ASSOCIATION_IMPLEMENTATION.md#current-runtimecaller-integration-preparation).
Surveillance remains PLANNED_NOT_STARTED; Active Discovery remains postponed.

### Historical pure-resolver objective at e30e483d7e5ede1cde1f75bc25bc65ff4ec115b1
**PE-5.1 - Private Local Service Association Contract and Pure Resolver: repository implementation candidate**

The user separately authorized the bounded PE-5.1 library, private contract and synthetic tests.
The pure resolver is IMPLEMENTED_REPOSITORY_CANDIDATE. This is descriptive post-identity
association using finalized inventory and explicit time/age inputs; no collection or runtime integration.
Phase 7A ACTIVE; PE-4 PASS/CLOSED; Public Projection PASS/CLOSED;
Documentation Consistency Correction PASS/CLOSED. PE-5 preparation is committed at
f3730ba5a8745361934ff822a9c29c16c9d0767b; no completed checkpoint is reopened.
PE-5 remains in progress for repository work only; runtime integration, publication,
persistence, scheduling and production implementation remain NOT AUTHORIZED.
Snapshot-age policy remains UNKNOWN_REQUIRED_BEFORE_OPERATIONAL_USE; no production threshold is chosen.
Current next task: validate/review the PE-5.1 repository candidate, then obtain separate commit/push authorization.
[Implementation contract, tests and STOP boundary](PE5_LOCAL_SERVICE_ASSOCIATION_IMPLEMENTATION.md).
Surveillance remains PLANNED_NOT_STARTED future PE-10 work; Active Discovery remains postponed.
The prior preparation objective and UNKNOWN chronology below remain historical.

### Historical implementation-preparation objective at f3730ba5a8745361934ff822a9c29c16c9d0767b

**PE-5 - MQTT and Passive Service Association: Implementation Preparation**

The user selected PE-5 as the next authorized HIOC roadmap checkpoint and authorized
Implementation Preparation ONLY. Executive sequencing decision, preserved exactly:

> if everything related to P4-4 and everything before it is completed successfully and documented, then start with PE-5.

Phase 7A ACTIVE; PE-4 PASS/CLOSED; Public Projection PASS/CLOSED;
Documentation Consistency Correction PASS/CLOSED. Completed preceding work stays closed.
PE-5 runtime implementation NOT_STARTED. PE-5 preparation is PREPARED_FOR_REVIEW;
PE-5 runtime/production implementation NOT AUTHORIZED. No new production evidence.
Current governed checkpoint and next task: PE-5 Implementation Preparation candidate
review, then separate authorization of the bounded first implementation checkpoint.
[Preparation findings and first checkpoint](PE5_IMPLEMENTATION_PREPARATION.md).
First implementation checkpoint: PE-5.1 - Private Local Service Association Contract and Pure Resolver.
That checkpoint is NOT_STARTED and NOT_IMPLEMENTED; it needs separate authorization.
Surveillance remains PLANNED_NOT_STARTED future PE-10 work; Active Discovery remains
postponed. No other roadmap item is reordered and no completed checkpoint is reopened.

### Historical post-closure objective snapshot at 6f69c4dfb85924a83b59e85ef2da602fc75ec5ea

The following closure and UNKNOWN statements were current at that accepted commit; they are historical after the executive PE-5 decision.


**PE-4 Documentation Consistency Correction Closure**

Documentation Consistency Correction PASS/CLOSED. Accepted correction commit: 5472a85194d105f6fb3d08ce51a4788256d8f028.
Validation, independent review, commit, push, independent repository/GitHub verification and repository synchronization are complete.
Authorized stash disposition is complete: the superseded PE-4 closure-draft stash was separately dropped; no stash remains.
PE-4 PASS/CLOSED; Public Projection PASS/CLOSED; Phase 7A ACTIVE; PE-5 NOT_STARTED.
PE-5 START NOT AUTHORIZED. Post-closure next task: UNKNOWN / NOT YET AUTHORIZED.
No operational or roadmap capability work is authorized by this closure transition.

Post-closure PI3 source synchronization and independent source review through 017686549acb27dbf7a8ad3577d0f84cf9f3f066 remain COMPLETED/PASS on OPERATOR_SUPPLIED evidence. No new source synchronization or production action is authorized.
[Closure authority](PE4_DOCUMENTATION_CONSISTENCY_CORRECTION_CLOSURE.md).

### Historical documentation correction candidate objective at 5472a85194d105f6fb3d08ce51a4788256d8f028

The following snapshot records preparation before acceptance; its pending gates are historical, not current authority.

**PE-4 Documentation Consistency Correction**

PE-4 PASS/CLOSED; Public Projection PASS/CLOSED; Phase 7A ACTIVE; PE-5 NOT_STARTED.
Audit PASS_CORRECTIONS_REQUIRED: 74 documents, 49 findings, 17 existing document paths.
The successor correction is an uncommitted candidate; PE-4 closure remains accepted.

Public Projection PASS/CLOSED; PE-4 PASS/CLOSED after repository-wide prerequisite audit.
Evidence OPERATOR_SUPPLIED. No Codex PI3 access or production action.
OPERATOR_SUPPLIED post-closure PI3 release-source synchronization COMPLETED and independent source review PASS: c7db29f795909d7926e36c02f1166034bcebb8b0 -> 30010c54d3f3078a9b07dada36dfe8dd4db2f6e5 (STOP; review PASS) -> 017686549acb27dbf7a8ad3577d0f84cf9f3f066 (STOP; review PASS). Observed final source tree: 6a59929189bc65fa8487e73ba97477eb009a43f0. Production was not accessed or mutated during this source-only sequence; Codex did not perform or observe it.
Current governed checkpoint: documentation consistency correction, an uncommitted candidate. Validation, independent review and separately authorized commit/push must close this correction before PE-5.
Phase 7A ACTIVE; PE-5 NOT_STARTED; rollback NOT_PERFORMED.
No new production validation, deployment, inventory, adapter, MQTT, HA or credential action.

### Historical objective before Public Projection production closure

**PE-4 Home Assistant Association Public Projection Deployment Baseline Correction**

PASS/CLOSED. Deployment Preparation PASS/CLOSED WITH BASELINE CORRECTION.
Attempt 1 remains FAIL / BASELINE_MISMATCH / SAFE, OPERATOR_SUPPLIED.
Root cause: UNVERIFIED REPOSITORY-DERIVED PRODUCTION BASELINE ASSUMPTION.
The supplied historically governed mixed runtime is preserved with an exact Public Projection backport
onto the observed PE1 production generation. Broader Compatibility Resilience deployment is NOT AUTHORIZED.
The correction family binds the explicit payload and preserves all canonical and private implementation identities.

Corrected baseline validation NOT STARTED / PREPARED FOR SEPARATE AUTHORIZATION; REQUIRED BEFORE DEPLOYMENT.
Deployment NOT STARTED / PREPARED FOR SEPARATE AUTHORIZATION; Production Execution NOT STARTED.
Public Projection Preparation PASS/CLOSED; source IMPLEMENTED / WINDOWS SYNTHETIC VALIDATION PASS;
PI3 POSIX Source Validation PASS/CLOSED. PE-4 NOT COMPLETE; Phase 7A ACTIVE; PE-5 NOT STARTED; rollback NOT PERFORMED.

Immediate next: PI3 source synchronization to the Baseline Correction commit ONLY;
STOP and independent source review; separately authorize corrected baseline observation;
STOP and independently review exact output before explicit receipt acceptance and SHA binding.
Only a later separate deployment authorization may permit production mutation.
See [correction authority](PE4_HOME_ASSISTANT_ASSOCIATION_PUBLIC_PROJECTION_DEPLOYMENT_BASELINE_CORRECTION.md).

### Historical public projection deployment preparation objective

**PE-4 Home Assistant Association Public Projection Deployment Preparation** -
**PASS/CLOSED**. Public Projection Preparation PASS/CLOSED; Source Implementation
IMPLEMENTED / WINDOWS SYNTHETIC VALIDATION PASS; PI3 POSIX Source Validation
PASS/CLOSED based on OPERATOR_SUPPLIED evidence. Codex did not observe or repeat
that production validation. Deployment NOT STARTED / PREPARED FOR SEPARATE AUTHORIZATION;
Production Execution NOT STARTED. The repository contains the dedicated one-shot
inventory-only maintenance tool, read-only baseline/installed reviewer, closed
contract and synthetic transaction/security tests. Runtime and private producer
bytes remain unchanged. See [deployment preparation](PE4_HOME_ASSISTANT_ASSOCIATION_PUBLIC_PROJECTION_DEPLOYMENT_PREPARATION.md).

Immediate operator action: PI3 source synchronization to the Deployment Preparation commit ONLY;
STOP and independent source review. PRE-DEPLOYMENT PI3 BASELINE VALIDATION
NOT STARTED / REQUIRED BEFORE DEPLOYMENT must then receive separate authorization
and independent evidence review. Actual deployment requires separate explicit
--deploy-authorized authorization; source synchronization and baseline review do
not authorize it. No forced inventory run, adapter execution, HA, credential,
MQTT, cron, production mutation or rollback was performed by Codex.
Scheduler Deployment PASS/CLOSED; recurring association scheduler ACTIVE / AUTHORIZED;
inventory scheduler ACTIVE. Manual Second Adapter Execution NOT AUTHORIZED / NOT PERFORMED.
PE-4 NOT COMPLETE; Phase 7A ACTIVE; PE-5 NOT STARTED; rollback NOT PERFORMED.

### Historical public projection POSIX source validation objective

**PE-4 Home Assistant Association Public Projection PI3 POSIX Source Validation** -
**PASS/CLOSED**, based on OPERATOR_SUPPLIED actual PI3 validation on nutandpihole.
Codex did not observe or repeat that execution. Source Implementation remains
IMPLEMENTED / WINDOWS SYNTHETIC VALIDATION PASS; Preparation PASS/CLOSED.
The read-only validator verified the implementation/private identities, POSIX paths,
shared lock, clean transaction namespace, coherent private copy, validation and
in-memory candidate/intersection. Prior/current public projection was absent at
validation time; no output, MQTT, HA, credential, adapter, cron or production
mutation was reported. This does not prove deployment or production execution.
Public Projection Deployment and Production Execution remain NOT STARTED. See
[the POSIX source validation closure](PE4_HOME_ASSISTANT_ASSOCIATION_PUBLIC_PROJECTION_POSIX_SOURCE_VALIDATION_CLOSURE.md).
Immediate next: PI3 source synchronization to the POSIX validation closure commit ONLY;
STOP and independent source review. Public Projection Deployment Preparation
requires separate authorization after that review; no deployment is authorized here.
Scheduler Deployment PASS/CLOSED; recurring association scheduler ACTIVE / AUTHORIZED;
inventory scheduler ACTIVE. Manual Second Adapter Execution NOT AUTHORIZED / NOT PERFORMED.
PE-4 NOT COMPLETE; Phase 7A ACTIVE; PE-5 NOT STARTED; rollback NOT PERFORMED.
Codex performed repository governance only, with no production or validator execution.

### Historical public projection source implementation objective

**PE-4 Home Assistant Association Public Projection Source Implementation** —
**IMPLEMENTED / WINDOWS SYNTHETIC VALIDATION PASS**. Preparation PASS/CLOSED.
PI3 POSIX Source Validation **NOT STARTED / PREPARED FOR SEPARATE AUTHORIZATION**;
Public Projection Deployment and Production Execution **NOT STARTED**.
The optional source helper and inventory integration exist only in the repository;
Windows fixture tests do not prove actual POSIX production readiness. See
[the source implementation contract](PE4_HOME_ASSISTANT_ASSOCIATION_PUBLIC_PROJECTION_IMPLEMENTATION.md).
Immediate next: PI3 source synchronization to the source implementation commit ONLY;
STOP and independent source review. Read-only PI3 POSIX source validation requires
separate later authorization and must precede any deployment checkpoint.
Scheduler Deployment PASS/CLOSED; recurring association scheduler ACTIVE / AUTHORIZED;
inventory scheduler ACTIVE. Manual Second Adapter Execution NOT AUTHORIZED / NOT PERFORMED.
PE-4 NOT COMPLETE; Phase 7A ACTIVE; PE-5 NOT STARTED; rollback NOT PERFORMED.
No PI3, HA, credential, broker, production or scheduler access/mutation occurred.

### Historical public projection preparation objective

**PE-4 Home Assistant Association Public Projection Preparation** — **PASS/CLOSED**.
Public Projection **NOT STARTED / PREPARED FOR SEPARATE IMPLEMENTATION**.
The inventory engine remains the sole public writer. The prepared optional
`home_assistant` object contains exactly five public-safe association facts;
private state and history stay private. Preparation creates governance/docs/tests
only and does not implement or execute the projection. See
[the frozen preparation contract](PE4_HOME_ASSISTANT_ASSOCIATION_PUBLIC_PROJECTION_PREPARATION.md).
Scheduler Deployment Preparation and Scheduler Deployment PASS/CLOSED; recurring
scheduler ACTIVE / AUTHORIZED. First natural invocation OBSERVED, private-state
publication PASS; scheduled result/return code NOT OBSERVED BY DESIGN.
Independent Production Acceptance PASS/CLOSED. Manual Second Adapter Execution
NOT AUTHORIZED / NOT PERFORMED. Immediate next: PI3 source synchronization to the
public projection preparation commit ONLY; STOP and independent source review.
Implementation requires a separate future checkpoint and authorization.
PE-4 NOT COMPLETE; Phase 7A ACTIVE; PE-5 NOT STARTED; rollback NOT PERFORMED.
No production, HA, credential, broker or scheduler access/mutation occurred.

### Historical scheduler deployment closure objective

**PE-4 Home Assistant Association Adapter Scheduler Deployment** — **PASS/CLOSED**.
Historical next action was PI3 source synchronization to the scheduler deployment closure
commit ONLY; STOP and independent review. That predecessor was independently reviewed
according to operator-supplied authority; original evidence limitations remain unchanged.

### Historical scheduler preparation objective

**PE-4 Home Assistant Association Adapter Scheduler Deployment** — **NOT STARTED / PREPARED FOR SEPARATE AUTHORIZATION**.
Scheduler Deployment Preparation PASS/CLOSED; Independent Production Acceptance PASS/CLOSED.
Immediate next action: PI3 source synchronization to the scheduler preparation commit ONLY;
STOP and independent review. No scheduler installation or execution is authorized here.
Future scheduler authorization permits recurring natural 5/35 slots under existing input/lock
semantics, not an extra manual adapter invocation. Second Adapter Execution NOT AUTHORIZED;
Public Projection DEFERRED; PE-4 NOT COMPLETE; Phase 7A ACTIVE; rollback NOT PERFORMED.
Attempt 1 capture failure and permanent historical evidence limitations remain unchanged.

### Historical acceptance closure objective

**PE-4 Home Assistant Association Adapter Scheduler Deployment** — **NOT STARTED**.
Independent Production Acceptance PASS/CLOSED; Attempt 2 PASS based on operator-supplied
execution and durable review. Attempt 1 FAIL / DURABLE CAPTURE and original evidence limitations
remain unchanged. Second Adapter Execution NOT AUTHORIZED; Public Projection DEFERRED;
PE-4 NOT COMPLETE; Phase 7A ACTIVE; rollback NOT PERFORMED.
Immediate operator action: PI3 source synchronization to the acceptance closure commit only;
STOP and independent review. No scheduler implementation or execution is authorized here.

### Historical acceptance objective and handoff chronology

Operator Path Integration PASS/CLOSED; native Windows durability PASS. Attempt 2 NOT STARTED /
READY FOR SEPARATE AUTHORIZATION and NOT AUTHORIZED. Immediate action: PI3 source synchronization
to the operator-path integration commit ONLY; STOP and independent review. Acceptance NOT CLOSED.
Earlier correction/preparation sequencing below is historical.


Current acceptance NOT CLOSED: Attempt 1 inspection PASS, capture FAIL; evidence NOT PUBLISHED.
Capture Correction PASS/CLOSED; Attempt 2 NOT STARTED / PREPARED FOR SEPARATE AUTHORIZATION
and NOT AUTHORIZED. Immediate action: PI3 source synchronization to the capture correction
commit only, STOP and independent review. Previous preparation text below is historical.


Preparation PASS/CLOSED; execution NOT STARTED / PREPARED FOR SEPARATE AUTHORIZATION.
Immediate operator action: PI3 source synchronization to the acceptance preparation commit only;
STOP, independent review, then separate read-only acceptance execution authorization.
The earlier closure-sync instruction retained below is completed historical sequencing.


Current authority (2026-10-07): **PE-4 Home Assistant Association Adapter Independent Production Acceptance**.
Durable Post-Run Reconciliation and Bounded Manual Production Validation are PASS/CLOSED
through explicit repository governance closure. OPERATOR_SUPPLIED_PRODUCTION_EVIDENCE:
PI3 source synchronization to 96150db5e28b065a587ae09ce0522ef6bd66f3be PASS/rc0, independent
source review, then one separately authorized durable reconciliation PASS/rc0. All protected
production surfaces and current durable gates passed without another adapter invocation.
Historical adapter execution remains COMPLETED ONCE / PASS; historical wrapper FAIL/rc1 /
MANUAL REVIEW REQUIRED and PRODUCTION_FILES_UNCHANGED=FALSE remain unchanged. First reconciliation
attempt remains FAIL / HISTORICAL_EVIDENCE. Original ephemeral files remain unavailable for
byte, metadata, canonical JSON or cross-file revalidation; the mandatory limitation is RECORDED.
The disappearance cause is UNKNOWN; no cause is inferred. Committed operator-supplied historical
report authority remains separate from current durable-state evidence.
Independent Production Acceptance and Scheduler Deployment NOT STARTED; Public Projection
DEFERRED; PE-4 NOT COMPLETE; Phase 7A Passive Living Inventory ACTIVE; rollback NOT PERFORMED;
second adapter execution NOT AUTHORIZED. Active Discovery remains postponed except already-governed
PE-4 work. Codex performed repository-only governance work and no production access or execution.
Next operator action: source synchronization to this closure commit only, STOP and independent
review. Independent Production Acceptance remains the next separately governed project checkpoint.

Deployment retains five preserved dependencies and nine newly created deployment targets,
COMMITTED authority and exact deployed source 4912f20d8b2ff78dcdaf8b3e0f52e57d5de5e3a2.
Durable Post-Run Reconciliation is PASS/CLOSED with explicit UNAVAILABLE original-artifact
revalidation and RECORDED evidence limitation. See [durable reconciliation closure](PE4_HOME_ASSISTANT_ASSOCIATION_DURABLE_POST_RUN_RECONCILIATION_CLOSURE.md).

## Next Planned Task
### PE-7.3 - Guarded PI3 delivery transaction repository preparation

Classification: CURRENT — bounded live HA Dashboard-shape correction; native qualification pending.
PE70_STATUS=COMPLETE/PASS; PE71_STATUS=COMPLETE/PASS; PE72_STATUS=COMPLETE/PASS.
PE6_STATUS=COMPLETE/PASS; PE7_STATUS=IN_PROGRESS; PE73_STATUS=IN_PROGRESS.
PE73_COMPLETE=FALSE; PE74_STATUS=NOT_AUTHORIZED; CODEX_PRODUCTION_ACCESS=FALSE.
Accepted OPERATOR_SUPPLIED filesystem qualification remains PASS and is not repeated.
New OPERATOR_SUPPLIED PI5 receipt at5fc1560a4be75e509e351eaf976364ed9bec62f1:
published source SHA verification PASS; authenticated Supervisor proxy/admin read-only
discovery PASS; HIOC integration absent/inactive; Lovelace resource mode storage.
DASHBOARD_SCHEMA_OR_LIMIT stopped discovery before any Dashboard results; mutation
false; exit1. Actual returned config type/shape/count is not present in that receipt.
It does not establish a malformed Dashboard or prove a particular strategy was used.
Core2026.10.4 returns raw stored Lovelace config; its pinned frontend20260930.5
supports static views OR a strategy. The old qualifier wrongly treated every response
as a static views list and a local32-view cap as a global discovery requirement.
The correction reports fixed-name type/presence/count diagnostics, preserves other
valid Dashboards, and never generates or selects a view. Static scan budget256 is
explicitly local; larger configs report count/omission, not an HA schema defect.
Optional path/cards/sections and generated views remain subject to the unchanged
publisher's actual additive-target requirements; nothing is filled in or migrated.
Unknown catalog rows/default source, shadowed default, legacy resources, auth or
transport failures retain fail-closed resource/qualification gates. Successful null
is not config_not_found. Partial choices survive later failures; private contents do
not enter the report. No .storage, service/write API, target selection or activation.
FOCUSED_NATIVE_VALIDATION=81_RUN_81_PASSED_0_FAILURES_0_ERRORS_0_SKIPPED.
INDEPENDENT_FOCUSED_ACCEPTANCE=PASS_FOR_DASHBOARD_SHAPE_CORRECTION_PUBLICATION.
Existing104 delivery passes remain supported by unchanged delivery/assessment/tests.
13 PI3 delivery,six HA source,39 current successor,449 protected identities verify;
contract,amendment,executive instruction,PI3 evidence and filesystem PASS preserved.
Trust/private files/SPKI/independent ACL, fresh cross-host disabled/exclusive guards,
actual live/local proof and approved target/backup remain required before delivery.
Next action: one operator-run PI5 read-only qualifier bound to this new source SHA/
commit; retain sanitized report and immediate exit status, then stop.
See [Dashboard-shape correction evidence](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-73-live-dashboard-shape-correction).

### Historical initial live API qualification preparation snapshot

Classification: HISTORICAL SNAPSHOT — accepted PI5 filesystem qualification; bounded live API discovery preparation.
PE70_STATUS=COMPLETE/PASS; PE71_STATUS=COMPLETE/PASS; PE72_STATUS=COMPLETE/PASS.
PE6_STATUS=COMPLETE/PASS; PE7_STATUS=IN_PROGRESS; PE73_STATUS=IN_PROGRESS.
PE73_COMPLETE=FALSE; PE74_STATUS=NOT_AUTHORIZED; CODEX_PRODUCTION_ACCESS=FALSE.
OPERATOR_SUPPLIED filesystem result PASS_READ_ONLY_FILESYSTEM_IDENTITY_QUALIFICATION,
exit0, source da630dd9cac20b784a6b433de614bfe323d4576f is accepted, not repeated.
PI5 HA192.168.100.251 HAOS/Core2026.10.4; Terminal/Core0:0; /homeassistant and
Core/config have matching actual filesystem identities/security/namespaces/process.
Required existing directories pass; absent hioc_operator is expected; no mutation.
Installed public source supports Lovelace storage/config, WS context/service response.
New fixed read-only API qualifier uses only the Terminal app's existing supported
Supervisor Core WebSocket proxy authentication, if already permitted. Root is not
HA authorization. Actual admin/current_user is verified; proxy admin is not a human
PE-7 editing actor. No token prompt, extraction, creation, logging or persistence;
only the normal internal authentication handshake receives the existing app token.
Missing/denied permission blocks and names existing browser-admin login as fallback.
Read-only dashboard catalog/config exports report bounded titles/paths/view choices
and resource fingerprints/conflicts, not cards, URLs/query secrets or credentials.
No target selected, duplicate dashboard, YAML migration, .storage access or API save.
Potential legacy-resource lazy import is refused before resources/list; an unprovable
default-source binding blocks rather than allowing a read-side configuration write.
HA integration absence is inactive, not unsafe. HA API observations cannot prove
fresh cross-host evaluator/scheduler/manual-caller exclusion; those guards remain
unknown/false. /local source capability is accepted; the actual route is not inferred
from an absent editor/404. Native delivery remains blocked pending the live guards,
an explicit compatible target, private full API export/backup and actual trust.
Existing strict trust_preflight remains mandatory before Delivery.prepare: real
certificate/assertion identities, private-file security, SPKI and independent ACL.
No trust exemption, issuance, activation, deployment or PE-7.4 authorization.
LIVE_QUALIFIER_IMPLEMENTATION=PASS; FOCUSED_NATIVE_VALIDATION=163_RUN_163_PASSED_0_FAILURES_0_ERRORS_0_SKIPPED.
INDEPENDENT_FOCUSED_ACCEPTANCE=PASS_FOR_BOUNDED_READ_ONLY_REPOSITORY_PUBLICATION.
13 PI3 delivery, six HA source,39 current successor and449 protected identities
verify. Existing delivery/assessment, controller/provider, contract, amendment,
executive instruction, completed PI3 deployment and historical evidence unchanged.
Next action: one operator-run PI5 live read-only API qualification bound to the new
published tool SHA/commit; retain sanitized receipt/exit status and stop.
See [live API qualification evidence](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-73-live-api-dashboard-and-disabled-role-qualification).

### Historical PID-namespace preparation snapshot

Classification: HISTORICAL SNAPSHOT — HA OS PID-namespace preflight correction; qualification pending.
PE70_STATUS=COMPLETE/PASS; PE71_STATUS=COMPLETE/PASS; PE72_STATUS=COMPLETE/PASS.
PE6_STATUS=COMPLETE/PASS; PE7_STATUS=IN_PROGRESS; PE73_STATUS=IN_PROGRESS.
PE73_COMPLETE=FALSE; PE74_STATUS=NOT_AUTHORIZED; CODEX_PRODUCTION_ACCESS=FALSE.
OPERATOR_SUPPLIED PI5 preflight at2d2ecf5b95531b2c514cc4a889aa358f9fc27365
verified source identity, selected/homeassistant, observed Core0:0, no directory
failures, integration absent and no mutation. Docker host PID731186 was not visible
in Terminal/proc: stat/status/cgroup/ns/user/root all ENOENT2. This is namespace
visibility evidence, not a filesystem-security failure or unsafe-directory finding.
The corrected qualifier never opens a Docker host PID in Terminal/proc. One fixed,
noninteractive read-only Docker exec runs stdlib metadata code in the exact Core
container under the observed Core UID/GID. It finds namespace-local Core PID, checks
credentials/user mapping/birth and opens actual Core config objects with NOFOLLOW.
Device/inode/owner/group/mode, absence and ACL checks must agree with Terminal's
secure/homeassistant proof. No mount-string-only admission, shell, extra privileges,
host PID mode, container reconfiguration or persistent service. Failure blocks.
The Core label and optional public-source location now follow the source-supported
Core layout; no exact HA version gate or production identity is invented.
FOCUSED_PID_NAMESPACE_CORRECTION=133_RUN_133_PASSED_0_FAILURES_0_ERRORS_0_SKIPPED.
INDEPENDENT_FOCUSED_ACCEPTANCE=PASS_FOR_REPOSITORY_PUBLICATION. No runtime mutation
or native delivery readiness is claimed. Existing publisher/transaction code is
unchanged.13 PI3,39 successor,449 protected and six HA source identities verify.
Trust, backups, interruption recovery, disabled behavior, runtime independence and
persistent-state isolation remain. All prior PI3/PI5 evidence retains its authority.
Next action: operator-run one consolidated read-only PI5 qualifier bound to this
published correction's exact source SHA/commit. No installation/activation authority.
See [PID-namespace correction evidence](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-73-core-pid-namespace-qualification-correction).

### Historical accepted HA preflight preparation snapshot

Classification: HISTORICAL SNAPSHOT — HA OS preflight prerequisite correction; native qualification pending.
PE70_STATUS=COMPLETE/PASS; PE71_STATUS=COMPLETE/PASS; PE72_STATUS=COMPLETE/PASS.
PE6_STATUS=COMPLETE/PASS; PE7_STATUS=IN_PROGRESS; PE73_STATUS=IN_PROGRESS.
PE73_COMPLETE=FALSE; PE74_STATUS=NOT_AUTHORIZED; CODEX_PRODUCTION_ACCESS=FALSE.
The accepted111-test HA correction and completed OPERATOR_SUPPLIED PI3 deployment
evidence are preserved. This bounded follow-up resolves fresh-install prerequisites.
Missing custom_components/hioc_operator is observed as absence, not an installation
failure. Only that fixed public directory0755 and missing private backups0700 may
be created. Private durable intent precedes creation; exact identities/readback and
Core-visible proof follow. Existing directories are never chmod/chowned or adopted.
Missing backups uses a fixed exclusive private bootstrap intent before mkdir, not
manual directory setup. Uncertain creation remains pending; no retry or auto recovery.
Explicit recovery removes only the empty, exact created HIOC directory; backup and
transaction evidence remain preserved. Missing custom_components/www remains a real
parent prerequisite. HA Core need not traverse private publisher backup storage.
Host PID mode is not a required configuration. Existing proc visibility must prove
the exact Core-container PID, process birth, credentials, user namespace and actual
Core-visible filesystem objects. Matching mount paths or archive metadata alone
are insufficient. Missing/hidden proof blocks; no new privileges, exec, namespace
entry or container change is authorized. Production support remains UNKNOWN.
FOCUSED_PREREQUISITE_CORRECTION=125_RUN_125_PASSED_0_FAILURES_0_ERRORS_0_SKIPPED.
Synthetic Windows results do not establish native Linux filesystem qualification.
All13 PI3 delivery,39 successor and449 protected identities verify; immutable HA
payload, original contract/amendment, trust design and completed PI3 evidence remain.
Disabled behavior, backups, whole-process authority, interruption evidence, runtime
independence and persistent-state isolation are preserved. No installation or Git
publication occurs here. Live HA/Dashboard/trust and native filesystem evidence
remain unverified. PE-7.3 IN_PROGRESS; PE-7.4 NOT_AUTHORIZED.
INDEPENDENT_REPOSITORY_ACCEPTANCE=PASS. The exact code/test candidate was reviewed
against all15 mandatory acceptance gates;125 focused results match unchanged bytes,
and25 preservation checks pass. Native installation/readiness is not established.
This authorized publication records repository acceptance only; no PE-7.3 closure.
Next action: operator-run consolidated read-only PI5 qualification using the accepted
preflight; unavailable Core filesystem proof blocks delivery without a workaround.
See [the prerequisite correction evidence](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-73-preflight-prerequisite-review-and-bounded-correction).

### Historical accepted111-test HA OS correction snapshot

Classification: HISTORICAL SNAPSHOT — HA OS delivery compatibility correction; native delivery unqualified.
PE70_STATUS=COMPLETE/PASS; PE71_STATUS=COMPLETE/PASS; PE72_STATUS=COMPLETE/PASS.
PE6_STATUS=COMPLETE/PASS; PE7_STATUS=IN_PROGRESS; PE73_STATUS=IN_PROGRESS.
PE73_COMPLETE=FALSE; PE74_STATUS=NOT_AUTHORIZED; CODEX_PRODUCTION_ACCESS=FALSE.
The completed PI3 deployment evidence at2784ef31da5e4ebc0e75af19695c8cc68c3d04a1
is preserved as OPERATOR_SUPPLIED; source release1c07932bd43aab1eac693ea07e195a74150fe550.
The existing six-file HA candidate is corrected, not replaced. A one-shot publisher
separates observed Terminal UID/GID0:0 from actual HA Core process ownership.
Only four pinned integration/editor files and a closed private transaction file set
are writable. Public files0644 use qualified Core UID/GID; private records0600 and
transaction directory0700 use publisher0:0. No PI3 ownership exception is introduced.
Before mutation, actual Core-visible descriptor identities must match the Terminal
destination; matching Docker mount-source strings alone are insufficient. Existing
host-PID/proc visibility is required. Missing proof or required existing directories
refuses delivery; no container changes, privilege expansion or guessed owner fallback.
FOCUSED_CORRECTION=111_RUN_111_PASSED_0_FAILURES_0_ERRORS_0_SKIPPED.
Windows descriptor/ownership models are synthetic, not native Linux qualification.
All13 PI3 delivery,39 successor and449 protected identities verify. Original contract,
amendment, controller, executive instruction and PI3 evidence remain unchanged.
Whole-process authority, private backups, durable intent, single-attempt publication,
exact readback and separate unexpected-recovery authority remain mandatory. No retries,
automatic rollback or consumer release. Existing pending transactions require disposition.
Runtime code has no publisher/transaction dependency; persistent Assets, policies,
history and configuration are outside the write scope. No permanent HA version pin,
migration, trust provisioning, activation, scheduling or service operation is added.
Remaining native requirements: actual Core/mount/ownership/security qualification,
supported live HA/API and approved Dashboard/view export, disabled guard, actual trust
identities/private validation, and native filesystem behavior. None is fabricated.
Next action: operator-run the self-contained, no-prompt read-only PI5 identity preflight
in the correction evidence. This is not installation or PE-7.4 authorization.
See [the HA OS correction evidence](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-73-ha-os-delivery-compatibility-correction-and-runtime-protection).

### Historical HA delivery preparation snapshot (superseded compatibility assumptions)

Classification: HISTORICAL SNAPSHOT — HA integration/UI/trust delivery preparation candidate.
PE70_STATUS=COMPLETE/PASS; PE71_STATUS=COMPLETE/PASS; PE72_STATUS=COMPLETE/PASS.
PE6_STATUS=COMPLETE/PASS; PE7_STATUS=IN_PROGRESS; PE73_STATUS=IN_PROGRESS.
PE73_COMPLETE=FALSE; PE74_STATUS=NOT_AUTHORIZED; CODEX_PRODUCTION_ACCESS=FALSE.
The PI3 runtime deployment is a completed, independently verified sub-checkpoint,
recorded as OPERATOR_SUPPLIED production evidence and published at
2784ef31da5e4ebc0e75af19695c8cc68c3d04a1. Its source release was
1c07932bd43aab1eac693ea07e195a74150fe550. That deployment is not reopened.
A finite HA delivery procedure now reuses six immutable PE-7.1 HA artifact identities:
four integration/editor files delivered, Dashboard/package retained as references.
Supported HA resource/card registration preserves existing layout, unrelated cards,
resources and package behavior. No .storage writes or broad installer/restart.
Private before/stage/reference/trust-packet backups and durable pending intent precede
single-attempt mutation. Interrupted operations are not automatically adopted,
retried, rolled back or released. One whole-process authority; no per-operation prompts.
The trust configuration packet preserves mTLS, assertion keys and independent ACLs
and remains disabled/offline; it is not active HA/PI3 configuration or provisioned secrets.
FOCUSED_ACCEPTANCE=69_RUN_69_PASSED_0_FAILURES_0_ERRORS_0_SKIPPED.
IMPLEMENTATION=PARTIAL_NATIVE_DELIVERY_NOT_ESTABLISHED; SYNTHETIC_PROCEDURE=PASS.
The native HA connection, live guard and two-host trust-file validation bindings
are explicit inputs, not manufactured production observations. Actual PI5 roots,
ownership/filesystem capabilities, supported APIs/resources/Dashboard and trust
placement remain required observations. No native end-to-end delivery claim is made.
All13 PI3 delivery,39 successor and449 protected identities verify; original contract,
controller, amendment, executive decision and completed PI3 evidence remain preserved.
Next action: operator-run the single consolidated read-only PI5 capability/integration
assessment below to bind actual paths/capabilities; no new research/checkpoint phase.
PE-7.3 remains IN_PROGRESS; PE-7.4 remains NOT_AUTHORIZED. No activation, migration,
notifications, credentials, service restart, PI3/PI5 access or Git publication here.
See [the integrated HA preparation evidence and assessment](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-73-integrated-ha-integration-ui-and-trust-delivery-preparation).

### Historical PI3 runtime deployment evidence snapshot

Classification: HISTORICAL SNAPSHOT — accepted PI3 runtime delivery evidence.
PE70_STATUS=COMPLETE/PASS; PE71_STATUS=COMPLETE/PASS; PE72_STATUS=COMPLETE/PASS.
PE6_STATUS=COMPLETE/PASS; PE7_STATUS=IN_PROGRESS; PE73_STATUS=IN_PROGRESS.
PE73_COMPLETE=FALSE; PE74_STATUS=NOT_AUTHORIZED; CODEX_PRODUCTION_ACCESS=FALSE.
EVIDENCE_AUTHORITY=OPERATOR_SUPPLIED. Source release1c07932bd43aab1eac693ea07e195a74150fe550.
The owner reports successful interrupted-window recovery and installation: all13
artifact SHA256 identities PASS; transactionCOMMITTED/pendingNone; windowRELEASED;
original12-entry crontab restored exactly; all3 affected HIOC jobs scheduled.
cron,pihole-FTL,unbound,nut-server are reported active. Incident-engine invocation
and recent status output observed; invocation alone does not prove engine completion.
Inventory last observed at09:30 before release; no post-release inventory execution
is established. Daily platform-status at03:17 was not expected in the observed
post-release window; no post-release platform execution is claimed. No HIOC error
matches in inspected cron logs; independent assessment reports zero failed invariants.
These are supplied observations, not a Codex production inspection or universal
service-health/event-history proof. No original receipt bytes or new production
security metadata are manufactured from the owner's summary.
Runtime deployment evidence is recorded as PASS for the supplied bounded facts.
Full PE-7.3 COMPLETE/PASS is not established: the unchanged contract section13
requires guarded artifact/integration/UI/trust delivery and observed HA API/resource
capability; section7 requires supported live Dashboard/resource delivery with backup,
not repository YAML copying. Evidence for these remaining delivery obligations is
not supplied. The approved maintenance-window evidence explicitly states that the
13-file runtime step alone does not close all PE-7.3. No new acceptance gate is added.
Next action: separately authorize completion/evidence of the existing PE-7.3 HA
integration/UI/trust delivery and capability prerequisites, keeping editing/evaluator
disabled except authorized preflight. PE-7.4 bounded functional acceptance remains
later and NOT_AUTHORIZED; no monitoring, migration or notifications are authorized.
Manual-caller restrictions remain procedural; missed/cached/retained/noncooperating
callers remain residual risks, not universally excluded. Executive instruction and
fixed-process authority remain verbatim in the unchanged successor authorization
record. Unexpected recovery, rollback or material scope changes require new authority.
See [the production evidence and closure determination](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-73-pi3-runtime-deployment-evidence-and-governance-closure-determination).

### Historical approved-process recovery correction snapshot

Classification: HISTORICAL SNAPSHOT — approved-process recovery correction, 2026-10-27.
PE70_STATUS=COMPLETE/PASS; PE71_STATUS=COMPLETE/PASS; PE72_STATUS=COMPLETE/PASS.
PE6_STATUS=COMPLETE/PASS; PE7_STATUS=IN_PROGRESS; PE73_STATUS=IN_PROGRESS.
PE73_COMPLETE=FALSE; PE74_STATUS=NOT_AUTHORIZED; CODEX_PRODUCTION_ACCESS=FALSE.
Published baseline1452534a23528af96e69b9ec030f050b61bed859. Current Windows
correction is uncommitted: five existing modified paths and one focused PE-7.3
successor authorization record. No staging, commit, push or PI3/PI5 access performed.
Owner executive decision PE73_OWNER_SEQUENCE_AUTHORIZATION_20261027 is recorded
verbatim in governance/pe7/pe73-sequence-authorization.json. It explicitly supersedes
repeated human authorization inside a previously approved fixed process. Original
contract/amendment text and historical nine-prompt decisions remain preserved.
Normal deployment and the specifically approved EXCLUDED resume now run without
per-operation prompts. Fresh technical grants, material context checks, durable
intent and all transaction/recovery safeguards remain mandatory. Unexpected
recovery, rollback or materially changed scope requires new owner authorization.
The last PI3 report is OPERATOR_SUPPLIED: source1452534a, PREPARED/pendingNone,
windowEXCLUDED, three jobs excluded/nine preserved, no installed artifacts/rollback,
journal SHA256b899a8fa79bde3c6619d6abd8217d88833c414823e7888358ed7a043b766600f.
Failure NATIVE_AUTHORIZATION_CONTEXT_DRIFT is retained. Diagnostic unrelated PID
lists were incorrectly part of context equality; the code defect is reproduced.
The exact historical changed field/PID is unknown because the context pair was not supplied.
The corrected binding retains fresh completeness, boot and exact affected-process
identities while keeping unrelated PID diagnostic churn outside authority.
The bounded resume verifies the exact raw journal anchor, PREPARED/EXCLUDED phase,
all13 current target identities, all13 stages/five backups, source and scheduler
before ATTACH. It never repeats PREPARE/PRESERVE/EXCLUDE or overwrites backups.
Approved continuation: ATTACH,DRAIN,ESTABLISH,COMMIT,AUTHORIZE_RELEASE,
RESTORE_SCHEDULER,RELEASE, with automated fresh per-operation technical validation.
FOCUSED_VALIDATION=66_RUN_66_PASSED_0_FAILURES_0_ERRORS_0_SKIPPED.
All13 delivery,39 successor and449 protected identities verify; original controller,
contract, verbatim amendment and transaction algorithms unchanged. No automatic
retry, rollback, cron restoration, release or uncertain-state adoption is introduced.
The corrected command needs these exact corrected tool bytes in release-source;
the old1452534a runner fails its hash check. Publication/source delivery has not
been performed in this assignment. No production resume/closure is claimed.
See [the recovery evidence and exact operator command](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-73-approved-process-resume-and-material-context-correction--2026-10-27).

#### Historical repository-preparation snapshot at85c1a4f1

Classification: HISTORICAL SNAPSHOT. PE73_STATUS=IN_PROGRESS_REPOSITORY_PREPARATION.
PE73_COMPLETE=FALSE; PE73_PRODUCTION_DELIVERY_AUTHORIZED=FALSE.
PE73_PI3_DELIVERY_CANDIDATE=PARTIAL; NATIVE_LIVE_COMMIT=BLOCKED_CONSUMER_COORDINATION_NOT_ESTABLISHED.
PE73_TWO_DEFECT_CORRECTION=PASS_REPOSITORY_SYNTHETIC; FOCUSED_RECHECK=ACCEPT_WITH_EXPLICIT_BLOCKER.
PE73_CONSUMER_MAINTENANCE_IMPLEMENTATION=PASS_REPOSITORY_SYNTHETIC; 104_RUN_104_PASSED.
PE73_RECOVERY_ATTACHMENT_CORRECTION=PASS_REPOSITORY_SYNTHETIC; RECOVERY_FOCUSED_RECHECK=ACCEPT_WITH_NATIVE_GATES.
PE73_NATIVE_QUALIFICATION_PREPARATION=PASS; NATIVE_QUALIFICATION=INCOMPLETE.
PE73_NATIVE_ACTION1=PASS_OPERATOR_SUPPLIED; ACTION1_EXIT_STATUS=0; COMPLETE_CALLER_COVERAGE=FALSE.
PE73_ISOLATED_DESCRIPTOR_CREATE_NOFOLLOW=PASS_OPERATOR_SUPPLIED; ISOLATED_EXIT_STATUS=0.
PE73_MODE0000_ACCESS=PASS_OPERATOR_SUPPLIED; MODE0000_EXIT_STATUS=0; DEPLOYMENT_ACCESS_RESOLVED=FALSE.
PE73_FILESYSTEM_BROKER_PROTOTYPE=PASS_EXPERIMENTAL_WINDOWS_FIXTURES; 54_RUN_54_PASSED.
BROKER_ACCESS_CONTRACT_DELTA=PROPOSED_NOT_ADOPTED; BROKER_NATIVE_INTEGRATION=NOT_AUTHORIZED.
PE73_MAINTENANCE_WINDOW_AMENDMENT=ADOPTED_OPERATOR_APPROVED_2026_10_23; ORIGINAL_CONTRACT_UNCHANGED.
WINDOW_REPOSITORY_IMPLEMENTATION=AUTHORIZED; WINDOW_NATIVE_ACCEPTANCE=NOT_ESTABLISHED; PRODUCTION=NOT_AUTHORIZED.
PE73_MAINTENANCE_WINDOW_IMPLEMENTATION=PASS_REPOSITORY_SYNTHETIC; CONTROLLER_TESTS=110_PASS; FINAL_WINDOW_TESTS=69_PASS; PRIOR_ACCEPTED_COUNTS=104_CONTROLLER_55_WINDOW; PRIOR_INTERIM_VALIDATION=110_CONTROLLER_57_WINDOW.
PE73_RELATIVE_PROCESS_DETECTION_CORRECTION=PASS_REPOSITORY_SYNTHETIC; PE73_RELATIVE_PROCESS_FOCUSED_RECHECK=ACCEPT_FOR_NATIVE_QUALIFICATION; NATIVE_QUALIFICATION=INCOMPLETE.
PE73_PUBLICATION_STABLE_SOURCE_IDENTITY=PASS_REPOSITORY_SYNTHETIC; CONTROLLER_TESTS=110_PASS; WINDOW_TESTS=69_PASS; BROKER_TESTS=54_PASS; REAL_GIT_INTEGRATION=12_PASS.
PUBLICATION_STABLE_CORRECTION_INDEPENDENT_ACCEPTANCE=NOT_PERFORMED; CORRECTION_PUBLICATION=NOT_AUTHORIZED_BY_THIS_ACTION.
Payload release remains `51398bab4e2293b578b2cdac2d0740c3738cab2f`. A clean checkout containing that immutable release in its commit ancestry can pass source integrity without a hardcoded HEAD; this does not approve tooling or authorize mutation.
See [the publication-stable identity evidence](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-73-publication-stable-source-integrity-correction).
MANUAL_CALLER_CONTROL=PROCEDURAL_ONLY; UNIVERSAL_EXCLUSION=FALSE; NATIVE_MUTATION_GATES=RETAINED.
See [the verbatim approved maintenance-window amendment](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-73-approved-maintenance-window-amendment-adoption--2026-10-23).
HISTORICAL_MAINTENANCE_REVIEW=REJECT_FRESH_PROVIDER_RECOVERY; NATIVE_MAINTENANCE_QUALIFICATION=NOT_ESTABLISHED.
The prior nine-path repository candidate is published at302a4e3f34f53fffb8299771d31c115e052b5400; this compatibility correction remains uncommitted.
Staging/publication and production operations are not authorized by this action; native qualification remains incomplete. Action 1 capability PASS is OPERATOR_SUPPLIED; native qualification remains incomplete.
The isolated descriptor/create/no-follow test is PASS_OPERATOR_SUPPLIED; native qualification remains incomplete.
The mode0000 characterization is PASS_OPERATOR_SUPPLIED; deployment access remains unresolved.
The standalone nonprivileged filesystem-broker feasibility prototype passed54 focused tests.
Its proposed access-contract delta is not adopted; native privilege/integration remain unauthorized.
Next action is independent acceptance of this exact uncommitted publication-stable
source-integrity correction before separate publication authorization. The broker remains experimental and unadopted.
See the [experimental broker evidence](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-73-experimental-filesystem-broker-feasibility-candidate).
No native enablement, production operation or isolated-test execution is authorized here.
See [delivery preparation evidence](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-73-guarded-pi3-delivery-transaction-repository-candidate).

### Historical PE-7.3 next-task snapshot before repository preparation authorization

### PE-7.3 - Guarded artifact, integration, UI and trust delivery

Classification: CURRENT. PE70_STATUS=COMPLETE/PASS; PE71_STATUS=COMPLETE/PASS.
PE72_STATUS=COMPLETE/PASS; PE7_STATUS=IN_PROGRESS; PE6_STATUS=COMPLETE/PASS.
ACCEPTED_SOURCE_COMMIT=51398bab4e2293b578b2cdac2d0740c3738cab2f.
NEXT_CHECKPOINT=PE-7.3 - Guarded artifact, integration, UI and trust delivery.
PE73_STATUS=NOT_STARTED; PE73_AUTHORIZED=FALSE.
Separate authorization is required. PE-7.2 accepts OPERATOR_SUPPLIED release-source
synchronization only. No runtime deployment, HA integration installation, service
change, operational credentials, Asset migration, monitoring or notification
activation is authorized here.
See the [PE-7.2 Evidence Report](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#pe-72-release-source-synchronization-acceptance-and-governance-closure)
and [accepted checkpoint sequence](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION_CONTRACT.md#13-bounded-checkpoint-sequence-and-implementation-scope).
No automatic follow-on action.

### Historical PE-7.2 next-task snapshot before source synchronization acceptance

### PE-7.2 - Operator-only exact release-source synchronization

Classification: CURRENT. PE70_STATUS=COMPLETE/PASS; PE71_STATUS=COMPLETE/PASS.
PE71_INDEPENDENT_ACCEPTANCE=ACCEPT; PE71_FOCUSED_RECHECK=ACCEPT.
PE7_STATUS=IN_PROGRESS; PE6_STATUS=COMPLETE/PASS.
NEXT_CHECKPOINT=PE-7.2 - Operator-only exact release-source synchronization.
PE72_STATUS=NOT_STARTED; PE72_AUTHORIZED=FALSE.
Separate authorization is required. No PI3 source synchronization, runtime delivery,
HA integration installation, Asset migration, monitoring or recurring activation is
authorized here. PE-7.1 repository implementation acceptance does not establish
production operation. See the [implementation Evidence Report](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md#final-pe-71-independent-acceptance-and-governance-closure)
and [accepted checkpoint sequence](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION_CONTRACT.md#13-bounded-checkpoint-sequence-and-implementation-scope).
No automatic follow-on action.

### Historical PE-7.1 candidate before independent acceptance

### PE-7.1 - Repository implementation and native validation

Classification: CURRENT. PE70_STATUS=COMPLETE/PASS; PE70_INDEPENDENT_CONTRACT_ACCEPTANCE=PASS.
PE7_STATUS=IN_PROGRESS; PE7_DESIGN_STATUS=COMPLETE; PE6_STATUS=COMPLETE/PASS.
PE71_STATUS=CANDIDATE_READY_FOR_INDEPENDENT_ACCEPTANCE; PE71_STARTED=TRUE; PE71_IMPLEMENTATION_AUTHORIZED=TRUE.
The separately authorized Windows-only [implementation candidate](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md)
follows [the accepted PE-7 contract](PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION_CONTRACT.md).
Repository native validation PASS: 3236 run, 3192 passed, 44 individual skips, 5 class-level skips, zero failures/errors.
Unexecuted-test limitations are recorded in implementation evidence. Independent
implementation acceptance remains NOT_PERFORMED; PE71_COMPLETE=FALSE.
NEXT_ACTION=INDEPENDENT_PE71_IMPLEMENTATION_CANDIDATE_ACCEPTANCE.
PE72_STATUS=NOT_STARTED; PE72_AUTHORIZED=FALSE. No commit or push is authorized.
PE7_PRODUCTION_AUTHORIZED=FALSE; PE7_MONITORING_EXECUTION_AUTHORIZED=FALSE;
PE7_RECURRING_ACTIVATION_AUTHORIZED=FALSE. No automatic follow-on action.

### Historical PE-6.5 handoff snapshot before PE-7.0 preparation

### PE-7 - Expected Availability & Permanent IoT Monitoring

Classification: CURRENT. Phase 7A ACTIVE; PE6_STATUS=COMPLETE/PASS; PE6_5_STATUS=COMPLETE/PASS.
PE7_STATUS=NOT STARTED / NOT AUTHORIZED; PE7_STARTED=FALSE; PE7_AUTHORIZED=FALSE.
NEXT_CHECKPOINT=PE-7 - Expected Availability & Permanent IoT Monitoring.
PE-6 closure establishes eligibility only. Separate PE-7 authorization is required;
existing PE-7 scope and roadmap sequencing remain unchanged. No implementation,
production action or automatic follow-on is authorized. STOP.

### Historical PE-6.4 closure handoff snapshot before PE-6.5 completion

### PE-6.5 - Final PE-6 governance closure and PE-7 handoff

Classification: CURRENT. Phase 7A ACTIVE; PE5_STATUS=COMPLETE; PE6_STATUS=IN_PROGRESS.
PE6_4_STATUS=COMPLETE/PASS; INDEPENDENT_REPOSITORY_ACCEPTANCE=ACCEPT.
PE6_5_STATUS=NEXT / NOT STARTED; PE7_STARTED=FALSE.
NEXT_CHECKPOINT=PE-6.5 - Final PE-6 governance closure and PE-7 handoff.
The PE-6.4 prerequisite is accepted. Separate authorization is required for PE-6.5:
repository-only final PE-6 closure and PE-7 handoff after all required evidence,
without repeated production action. No PE-6.5 work or PE-7 implementation begins here.
See the current PE-6.4 Evidence Report in Implementation Status and the
[accepted PE-6.5 roadmap](PE6_CLASSIFICATION_CONTRACT_DESIGN.md#pe-65--final-pe-6-governance-closure-and-pe-7-handoff).
No production access, classification execution, recurring activation or automatic
follow-on action is authorized. STOP.

### Historical timestamp-correction next-task snapshot before PE-6.4 closure

### PE-6.4 - Bounded Execution and Independent Production Acceptance

Classification: CURRENT. Phase 7A ACTIVE; PE-4 PASS/CLOSED; Public Projection PASS/CLOSED.
PE5_STATUS=COMPLETE; PE6_STATUS=IN_PROGRESS.
PE6_0_STATUS=COMPLETE/PASS; PE6_1_STATUS=COMPLETE/PASS;
PE6_2_STATUS=COMPLETE/PASS; PE6_3_STATUS=COMPLETE/PASS.
PE6_REPOSITORY_IMPLEMENTED=TRUE; PE6_PRODUCTION_DEPLOYED=TRUE.
DEPLOYMENT_SCOPE=DISABLED_EXACT_FOUR_FILE_INSTALLATION_ONLY.
PE6_PRODUCTION_EXECUTION_ESTABLISHED=FALSE; PE6_4_STARTED=FALSE.
NEXT_CHECKPOINT=PE-6.4 - Bounded Execution and Independent Production Acceptance.
Separate authorization is required for PE-6.4. No scheduler or automatic activation is authorized.

PE-6.3 accepts only OPERATOR_SUPPLIED PI3 disabled-installation evidence from
source 723c1e71ad2d54e5088c0849ccee59857cbe0794. Four exact new artifacts were
installed without overwriting existing files; seven observed dependencies were preserved.
Codex did not access PI3. No caller execution, initialization, cron change,
service restart, scheduled activation or PE-6.4 execution occurred in this checkpoint.
The inspected activation locations returned no matches; universal indirect invocation
absence and current production health are not established.
Runtime inventory.py differs from source; only KNOWN_FIELDS, OPERATOR_ROLES and
normalize_mac AST definitions were reported equal. Full runtime compatibility is not established.
Rollback was NOT PERFORMED and is not claimed tested. No pre-existing dependency may be removed.
See [PE-6.3 Evidence Report](PE6_CLASSIFICATION_IMPLEMENTATION.md#pe-63-disabled-runtime-installation-acceptance-and-closure).
PE-6 remains IN PROGRESS. PE-6.4 is NEXT / NOT STARTED; PE-6.5 closure and PE-7 remain later.
### Timestamp compatibility correction prerequisite

TIMESTAMP_CORRECTION=REPOSITORY_ONLY; CORRECTED_ARTIFACT_DEPLOYED=NOT_ESTABLISHED.
PE6_4_STARTED=FALSE; PE6_PRODUCTION_EXECUTION_ESTABLISHED=FALSE.
The operator reported inventory.updated=2026-10-17T11:00:02-06:00,
198 parseable devices and freshness at inspection only (OPERATOR_SUPPLIED).
The PE-6.3 installed classifier rejects that accepted PE-5 aware-time form.
The repository correction accepts aware offsets and emits UTC without rewriting inputs.
Production still requires separate operator source synchronization, guarded replacement
of classification.py only, then separately authorized bounded PE-6.4 execution.
No deployment, caller execution, scheduling, PE-6.4 closure or PE-7 is authorized here.
See [Timestamp correction evidence](PE6_CLASSIFICATION_IMPLEMENTATION.md#timestamp-compatibility-correction-prerequisite-to-pe-64).

STOP after the repository correction. No automatic follow-on action is authorized.

### Historical accepted PE-6.0 next-task snapshot at ea4a93fba1615af1d6641c7f0683b8e912c03d72

### PE-6.1 - Private classification implementation and comprehensive repository validation

Classification: HISTORICAL_INTENTIONALLY_PRESERVED accepted PE-6.0 snapshot. PE5_STATUS=COMPLETE; PE6_STATUS=DESIGN_COMPLETE_RUNTIME_NOT_IMPLEMENTED.
PE6_0_STATUS=COMPLETE_CONTRACT_DESIGN; PE6_RUNTIME_IMPLEMENTED=FALSE.
NEXT_CHECKPOINT=PE-6.1 - Private classification implementation and comprehensive repository validation.
Separate authorization is required for PE-6.1, including adoption or revision of the proposed design.
This checkpoint authorizes no runtime implementation, production operation or PE-7 work.

The [PE-6 contract design](PE6_CLASSIFICATION_CONTRACT_DESIGN.md) inventories actual
capabilities and preserves the complete original authorization, twenty evidence-backed
technical decisions, exact private schema proposal and six-checkpoint roadmap.
Proposed role suggestions and metadata-quality summaries remain private, deterministic
and separate from operator-owned Asset data and public operational role/health.
Asset schema1.0 and the accepted PE-5.9 governance/runtime remain unchanged.
No PE-6 persistence, cron, inventory hook or public projection is selected.
Actual production inputs/locks/runtime state remain UNKNOWN; only later bounded operator
gates may establish them. All previous OPERATOR_SUPPLIED evidence limitations remain.

### Historical accepted PE-5.9 handoff at d6f9d3c6bd07b16fc515ae531b6aa0a3e9188221

### PE-6 - Classification & Metadata Quality

Classification: HISTORICAL_INTENTIONALLY_PRESERVED. Phase 7A ACTIVE; PE5_STATUS=COMPLETE.
PE5_9_STATUS=COMPLETE/PASS; PE5_8_STATUS=COMPLETE/PASS.
NEXT_CHECKPOINT=PE-6 - Classification & Metadata Quality; PE6_STARTED=FALSE.
Separate authorization is required for PE-6. PE-6 implementation is NOT authorized.

All 37 original PE-5 requirements and all 14 Definition of Done conditions pass;
all 11 roadmap UNKNOWN decisions have evidence-backed resolutions. The original
roadmap and 46 implementation checklist items remain immutable authority.
The current coverage/evidence ledger and complete private handoff are in
[PE-5 implementation evidence](PE5_CONFIGURED_ASSOCIATION_IMPLEMENTATION.md#current-pe-59-final-closure-and-private-pe-6-handoff)
and final_closure in the existing implementation governance record.
PE-5.6/7/8 accepted observations remain OPERATOR_SUPPLIED. Preserve
OPERATOR_OBSERVATIONS_ONLY; FULL_PRODUCTION_BYTES_NOT_RECEIVED;
NO_NATURAL_FAULT_OR_NATIVE_CRASH_CLAIM; NO_CURRENT_FRESHNESS_CLAIM.
First-cycle fields not separately supplied remain UNKNOWN; none is a completion
waiver or new production observation. No runtime, scheduler, public interface,
MQTT or production change occurs here. PE-6 may later consume only validated,
confirmed, unexpired private relationship evidence under the unchanged contract.
Publication remains gated by exact commit, push and independent GitHub verification.

### Historical PE-5.8 closure at 10b9c9929f740f3cd24c1768998f854d4837c3bb

### PE-5.9 - Final PE-5 Closure and PE-6 Handoff

Classification: HISTORICAL_INTENTIONALLY_PRESERVED. Phase 7A ACTIVE; PE-5 IN_PROGRESS.
PE5_6_STATUS=COMPLETE/PASS; PE5_7_STATUS=COMPLETE/PASS; PE5_8_STATUS=COMPLETE/PASS.
RECURRING_EXECUTION_ACTIVE=TRUE; PE5_9_STARTED=FALSE.
Current next checkpoint: PE-5.9 - Final PE-5 Closure and PE-6 Handoff.
Separate authorization is required for PE-5.9. It has not started; PE-5 is not yet closed.

OPERATOR_SUPPLIED read-only observations establish the required minimum of three
consecutive natural successful scheduler windows (:17, :32, :47 on 2026-10-14).
No manual producer execution occurred during PE-5.8; PE-5.6's bounded manual run
is historical and is not counted. PE-5.7 activation remains historical accepted evidence.
Cycle1 evaluated_at=2026-10-14T20:17:02.619461Z;
output SHA256 a5bea06825a63b1cd29ac705defe1066cc1f97ac678648d5fd97d9e322ebfe90;
CONFIRMED transaction dur_104bbbd8cb45467b8a53cc7d88dc497a.
Cycle2 evaluated_at=2026-10-14T20:32:01.823448Z;
output SHA256 c28f22d1272031a6586ee1673719c8b1061e06a2c120237df2140e8007082a7a;
CONFIRMED transaction dur_f70cd9091d5b4536929b329deac70e22.
Cycle3 evaluated_at=2026-10-14T20:47:02.451624Z;
output SHA256 aff03e297ae81bc9a9deff52884d2779b6138eb4b2f8592fe05f78272aa98120;
CONFIRMED transaction dur_e7a270926be543808b7711c5885778d7.
Second/third sidecar confirmed SHA equals its corresponding observed output SHA;
candidate=None. First CONFIRMED state/transaction was supplied, but a separate
confirmed_sha256 field was not supplied and is not fabricated.
Source revision1 and SHA256
961b72e8918606caeac565a8d472d03c4784d9a3b43eae6deb4085865330d295
remained unchanged. Third source sidecar also confirms that SHA/revision.
The accepted scheduler SHA256 remained
3f56b904fc1dd40ccbfa3fdd61cb910c4d215e9ac28a9bf2dcdf3721c73b62a9,
with one marker and one entry; cadence 2,17,32,47 * * * * and command unchanged.

Second/third outputs report schema2.0 VALID, configured VALID/revision1 with
one candidate and zero rejections; local eight associations and zero rejections.
LOCAL_STATE=None is a reported lookup: the closed local envelope has no state
field. Local schema1.0 is embedded unchanged in combined schema2.0.
Third valid_until=2026-10-14T21:05:02.000000Z is within the accepted upper bound;
its earlier deadline is consistent with the inventory expiry cap. Exact third
inventory.updated was not supplied and is not inferred.

Overlap, missed-cycle/no-catch-up, expiry, failure, restart/corruption and durability
semantics are supported by committed contract/static implementation and passing
synthetic Windows fixtures, as PE-5.2 explicitly permits. They are NOT claimed as
naturally observed faults or native PI3 crash tests. No artificial production
fault, manual execution or production mutation was performed for this acceptance.
Full production envelopes/crontab bytes were not independently received; supplied
production SHA values are operator observations, not independently recomputed hashes.
Current freshness beyond the supplied observation times is not asserted.
The earlier two-cycle STOP is preserved as process history; the third observation
resolved it without waiving any requirement. Existing PE-5.6/7 history remains preserved.
See [implementation evidence](PE5_CONFIGURED_ASSOCIATION_IMPLEMENTATION.md) and
operational_acceptance in the existing governance record for exact receipts,
evidence limitations and repository validation. No runtime or authority model changes.
Codex accessed no PI3, PI5 or production. PE-5.9 requires separate authorization.

### Historical PE-5.7 closure at de0279fd3667e096fd940b80d20a096f7082e8ac

### PE-5.8 - Operational Evidence and Independent Production Acceptance

Classification: HISTORICAL_INTENTIONALLY_PRESERVED. Phase 7A ACTIVE; PE-5 IN_PROGRESS.
PE5_6_STATUS=COMPLETE/PASS; PE5_7_STATUS=COMPLETE/PASS.
RECURRING_EXECUTION_ACTIVE=TRUE; PE5_8_STARTED=FALSE.
Current next checkpoint: PE-5.8 - Operational Evidence and Independent Production Acceptance.
Separate authorization is required for PE-5.8. No PE-5.8 work is performed here.

OPERATOR_SUPPLIED evidence reports one separately authorized jazofv1 scheduler
activation: PASS_PE5_7_SCHEDULER_ACTIVATION. The accepted entry is exactly:
2,17,32,47 * * * * /usr/bin/python3 /home/jazofv1/hioc/pi4/bin/hioc-compose-service-associations.py
Marker: # HIOC_PE5_SERVICE_ASSOCIATIONS. Marker count1, entry count1,
unexpected PE-5 entry count0. Before crontab SHA256:
8f900f4679aa861b02e781a61927683db5900ddfe159d78c3831a1595ae7fe71.
After/install/read-only-verification SHA256:
3f56b904fc1dd40ccbfa3fdd61cb910c4d215e9ac28a9bf2dcdf3721c73b62a9.
Full crontab bytes were not independently received; these hashes and exact
post-install-byte verification are operator observations, not repository-derived hashes.
Existing jobs were reported preserved, including the governed PE-4 5/35 entry.

Activation did not manually execute the composer, execute the installer, or access MQTT.
The command uses the existing internal shared nonblocking lock; no execution-model,
runtime implementation, persistence, public inventory or authority change is made here.
The disabled deployment template remains byte-identical and commented; activation
changed the operator's crontab, not that source artifact.

Pre-activation PI3 source HEAD/origin were reported as
4990c62afbce22a804229f3cb8329986741067a6 with empty porcelain status.
No synchronization to PE-5.6 closure commit 21ca5f676bb96d376b3a6f098decfecfe3c6ea49
is inferred. Immutable Git comparison establishes unchanged runtime payload between
those commits; reported composer and disabled-template hashes match accepted bytes.

Separate post-activation read-only verification reported the same crontab hash,
one marker, one accepted entry and no unexpected PE-5 entry.
NO_RELEVANT_PROCESS_MATCH records only that instant. It does not prove no natural
scheduled cycle has ever occurred. Natural-cycle evidence is NOT ESTABLISHED.
No current generated-output freshness, recurring operational acceptance or naturally
observed overlap/missed-cycle/staleness/failure behavior is claimed.
PE-5.8 retains its natural-cycle and independent production acceptance requirements.
PE-5.6 first-failure, corrected-deployment and bounded-execution evidence remains historical.
Codex performed repository work only; no PI3/PI5/production access or mutation occurred.
See [implementation evidence](PE5_CONFIGURED_ASSOCIATION_IMPLEMENTATION.md) and the
existing governance record's scheduler_activation evidence.


### Historical PE-5.6 closure at 21ca5f676bb96d376b3a6f098decfecfe3c6ea49

### PE-5.7 - Conditional Execution Activation

Classification: HISTORICAL_INTENTIONALLY_PRESERVED. Phase 7A ACTIVE; PE-5 IN_PROGRESS.
PE5_6_STATUS=COMPLETE/PASS; PE5_7_STARTED=FALSE; RECURRING_EXECUTION_ACTIVE=FALSE.
Current next checkpoint: PE-5.7 - Conditional Execution Activation.
PE-4/Public Projection remain PASS/CLOSED; PE-5.1 remains accepted/closed.

OPERATOR_SUPPLIED production evidence establishes corrected one-artifact deployment
of commit 4990c62afbce22a804229f3cb8329986741067a6, then one separately authorized
corrected initial installation PASS_PRIVATE_PERSISTENCE / CONFIRMED_DURABLE_CURRENT,
then exactly one separately authorized bounded composer execution
PASS_PRIVATE_ASSOCIATIONS / ACCEPTED_COUNT=1 / REJECTED_COUNT=0.
This is not recurring execution. No second corrected installation or extra composer
execution is authorized by closure. PE-5.7 has not executed; scheduler remains disabled.

The first initialization WRITE_FAILED / LOCK_UNAVAILABLE remains historical evidence.
The correction fixed missing-directory bootstrap before the shared lock; no lock
contention was established. Failed-attempt absence evidence and the intact candidate
are preserved alongside the accepted correction and separately authorized success.

Configured source revision1 SHA256:
961b72e8918606caeac565a8d472d03c4784d9a3b43eae6deb4085865330d295.
Configured relationship:
mqra_01d1d5edfdc1db0fa63b14b5b9b0b9701b4ff183a946fcb63751fb14910fe028.
Provenance: operator_mqtt_v1 / configured_mqtt / declared_endpoint_device_v1.
Generated output SHA256:
f1b219dc413325a557c71e3561804afcc3bdf26f87d2d6fdb71bb3e7c97f5e2c.
Both durability domains were observed CONFIRMED, candidate=null, bound to revision1;
exact transaction identities, metadata and source/output observations are recorded in
the existing implementation governance record's production_validation evidence.

The local branch retained eight existing_service_ownership/high relationships under
unchanged schema1.0 / 2100-second policy. The receipt is historically bound to consumed
inventory SHA256 394b5cf4007fccd1aec0beb862f29ed6dfb78a76a2903cb6174b08f0c5d17607,
updated 2026-10-14T17:00:01.000000Z, evaluated 2026-10-14T17:04:50.224530Z,
valid_until 2026-10-14T17:24:50.224530Z. Later observed inventory SHA differed;
its cause is UNKNOWN, the difference alone is not a defect and does not rebind the
receipt. No present receipt consumability or freshness is asserted.

The bounded public-inventory search for the five reported configured-MQTT terms found
zero matches: PASS for that check only. No universal privacy/transport claim is made.
Post-execution operator checks reported clean source at the correction commit,
unchanged corrected artifact, private0700 directories/0600 single-link files,
NO_PE5_CRONTAB_MATCH and NO_RELEVANT_PROCESS_MATCH.
Repository-derived checks separately reproduced the source SHA/size, relationship ID,
output-sidecar SHA/size and timing bound; full output bytes were not independently received.
All required committed Windows suites passed before closure; native fault/crash evidence
and PE-5.8 natural-cycle requirements are not waived. Codex accessed no production system.
See [implementation evidence](PE5_CONFIGURED_ASSOCIATION_IMPLEMENTATION.md).
Separate authorization is required for PE-5.7. Do not activate or implement it here.


### Historical PE-5.6 correction pending deployment at 4990c62afbce22a804229f3cb8329986741067a6

### PE-5.6 - Bounded Mapping and Storage Production Validation

Classification: HISTORICAL_INTENTIONALLY_PRESERVED. Phase 7A ACTIVE; PE-5 IN_PROGRESS; PE-4 and Public Projection PASS/CLOSED.
PE5_3_STATUS=COMPLETE_REPOSITORY_IMPLEMENTATION.
CURRENT_PE5_CHECKPOINT=PE-5.6.
PE5_6_STATUS=BLOCKED_PENDING_CORRECTED_DEPLOYMENT_AND_SEPARATE_RETRY.
PE5_7_STARTED=FALSE. Recurring execution remains disabled.

OPERATOR_SUPPLIED evidence reports PE-5.5 installed the accepted six-artifact disabled
payload. The first PE-5.6 approved revision-1 source installation returned
WRITE_FAILED / LOCK_UNAVAILABLE. This was missing infrastructure, not lock contention.
Post-failure observation established config exists, jazofv1:jazofv1 mode0755; no
config/enrichment, source, source sidecar, state/enrichment, output parent, lock,
output or output sidecar existed; no relevant installer/composer process was running.
Candidate /home/jazofv1/pe5-mqtt-mappings-candidate.json remained intact,
SHA256 961b72e8918606caeac565a8d472d03c4784d9a3b43eae6deb4085865330d295.

The implementation incorrectly required the shared lock parent to preexist before
initialization. Repository correction now bounds directory creation to approved
initial source installation. No retry has occurred. Corrected production deployment
is NOT ESTABLISHED. Source state does not prove production state.
Next operator actions: independently accept repository correction, synchronize exact
accepted source, replace only changed accepted payload bytes, independently accept
corrected deployment, then separately authorize the PE-5.6 initialization retry.
No composer invocation, scheduler activation, recovery, or PE-5.7 is authorized here.
See [configured association implementation](PE5_CONFIGURED_ASSOCIATION_IMPLEMENTATION.md).
Separate authorization is required for the retry and every later checkpoint.


### Historical PE-5.3 repository completion at 348f9787ae0ab364570a2ba07ada9527fc8db0e2

Classification: HISTORICAL_INTENTIONALLY_PRESERVED.
### PE-5.4 - PI3 Release Source Synchronization

Classification: HISTORICAL_INTENTIONALLY_PRESERVED. PE5_3_STATUS=COMPLETE_REPOSITORY_IMPLEMENTATION; PE5_4_STARTED=FALSE.
Current next checkpoint: PE-5.4 - PI3 Release Source Synchronization.
The configured mapping resolver, private POSIX composer/store, explicit source installer
and bounded durability recovery are implemented in the repository. Activation remains
disabled; no source provisioning, PI3 synchronization, deployment or production execution
has occurred. PE-5 remains IN_PROGRESS, PE-5.1 remains accepted/closed, PE-4 and Public
Projection remain PASS/CLOSED, and Phase 7A remains ACTIVE.
The PE-5.2 design and its corrected durability contract are unchanged authority.
See [PE-5.3 repository implementation](PE5_CONFIGURED_ASSOCIATION_IMPLEMENTATION.md) and its exact governance payload.
Separate authorization is required for PE-5.4 and every later lifecycle checkpoint.


### Historical PE-5.3 implementation selection at 72e878f9c0c8f5d3fe6357979e045943f3cf9d34

### PE-5.3 - Remaining Capability Implementation and Comprehensive Validation

Classification: HISTORICAL_INTENTIONALLY_PRESERVED pre-implementation selection at 72e878f9c0c8f5d3fe6357979e045943f3cf9d34. PE5_2_STATUS=COMPLETE_CONTRACT_DESIGN; CURRENT_PE5_CHECKPOINT=PE-5.3; PE5_3_STARTED=FALSE. Next is PE-5.3 implementation/validation under separate authorization, then unchanged PE-5.4 through PE-5.9 and PE-6. See [complete contract](PE5_MAPPING_CONTRACT_DESIGN.md). Separate authorization is required; PE-5.1 first execution is complete and is not repeated.


PE-5.2 atomic durability contract correction is complete in repository design.
PE-5.3 previously returned STOP_PE5_3_ATOMIC_FAILURE_CONTRACT_CONTRADICTION before
implementation: a synthetic post-replace parent-fsync fault disproved the broad
old-file guarantee. Historical STOP evidence is preserved. The corrected contract
separates pre-replace preservation from INDETERMINATE_DURABILITY, fails closed,
retains the prior confirmed logical identity and requires explicit recovery without
automatic rollback. See [corrected persistence contract](PE5_MAPPING_CONTRACT_DESIGN.md#atomic-durability-boundary-correction)
and governance/pe5/pe5-atomic-durability-contract-correction.json.
PE5_3_STARTED=FALSE; PE5_4_STARTED=FALSE. This correction implements no runtime,
provisions no source and authorizes no production action. Resume PE-5.3 only as
the next separate action after this correction is validated and published.

### Historical policy-selection next task at ed3a80508d101652bac89e1dcc111167670aaebc

Classification: HISTORICAL_INTENTIONALLY_PRESERVED.

### PE-5.1 snapshot-age policy — independent candidate acceptance

PE5_1_MAX_SNAPSHOT_AGE_SECONDS=2100; SELECTED_CANDIDATE_PENDING_COMMIT.
Next action: CONCISE_INDEPENDENT_CANDIDATE_ACCEPTANCE. STOP before commit/push.
Phase 7A ACTIVE; PE-4 PASS/CLOSED; Public Projection PASS/CLOSED.
Production deployment/use and further implementation remain NOT AUTHORIZED.
See Current Objective and the successor policy record.

### Historical caller checkpoint at eda8c9930d7f7fbf09bcc08b252bef05b385cf7e

### PE-5.1 caller integration — repository candidate validation and review

Validate/review the explicitly authorized offline caller; STOP for separate commit/push authorization.
Phase 7A ACTIVE; PE-4 PASS/CLOSED; Public Projection PASS/CLOSED.
Operational integration/deployment and production use remain NOT AUTHORIZED.
The required policy is UNKNOWN_REQUIRED_BEFORE_OPERATIONAL_USE; no default threshold is chosen.
No scheduler, persistence, MQTT mapping/Discovery, public projection, Active Discovery or surveillance is authorized.
PE-6 through PE-10 ordering is unchanged.

### Historical pure-resolver next task at e30e483d7e5ede1cde1f75bc25bc65ff4ec115b1
### PE-5.1 private resolver — implementation candidate review

Current governed work is the separately authorized PE-5.1 repository implementation and validation.
The private contract/pure resolver is IMPLEMENTED_REPOSITORY_CANDIDATE; after validation STOP for independent review.
Commit and push require separate authorization. No next runtime/integration checkpoint is authorized.
Phase 7A ACTIVE; PE-4 PASS/CLOSED; Public Projection PASS/CLOSED; completed preceding work remains closed.
PE-5.1 production use, deployment, MQTT ingestion/publication, persistence and scheduling remain NOT AUTHORIZED.
The snapshot-age threshold remains UNKNOWN_REQUIRED_BEFORE_OPERATIONAL_USE; synthetic supplied values are not production policy.
PE-6 through PE-10 sequencing is unchanged; surveillance and Active Discovery remain deferred.
See [bounded implementation](PE5_LOCAL_SERVICE_ASSOCIATION_IMPLEMENTATION.md).

### Historical implementation-preparation next task at f3730ba5a8745361934ff822a9c29c16c9d0767b

### PE-5 Implementation Preparation — current governed checkpoint

The explicit user executive sequencing decision resolves the former UNKNOWN next-task
state. PE-5 is selected; only preparation is authorized. The immediate governed work
is preparation-candidate review and separate authorization of PE-5.1 - Private Local Service Association Contract and Pure Resolver.
PE-5 runtime implementation NOT_STARTED; runtime/production implementation NOT AUTHORIZED.
Phase 7A ACTIVE; PE-4 PASS/CLOSED; Public Projection PASS/CLOSED; Documentation Consistency Correction PASS/CLOSED.
The read-only sequencing review and completed prerequisites are repository evidence;
no current production state is inferred from them. No PI3/PI5/HA/broker access,
source synchronization, deployment, MQTT mutation, credentials, scheduling or rollback
is authorized. The ordered PE-6 through PE-10 and other future checkpoints stay intact.
See [PE-5 Implementation Preparation](PE5_IMPLEMENTATION_PREPARATION.md).

### Historical post-closure next-task snapshot at 6f69c4dfb85924a83b59e85ef2da602fc75ec5ea

The following UNKNOWN statements preserve the prior valid sequencing state, not the current next task.


### Post-Closure Next Task — UNKNOWN / NOT YET AUTHORIZED

Documentation Consistency Correction PASS/CLOSED. Accepted correction commit: 5472a85194d105f6fb3d08ce51a4788256d8f028.
Validation, independent review, commit, push, independent repository/GitHub verification and repository synchronization are complete.
Authorized stash disposition is complete: the superseded PE-4 closure-draft stash was separately dropped; no stash remains.
PE-4 PASS/CLOSED; Public Projection PASS/CLOSED; Phase 7A ACTIVE; PE-5 NOT_STARTED.
PE-5 START NOT AUTHORIZED. Post-closure next task: UNKNOWN / NOT YET AUTHORIZED.
No operational or roadmap capability work is authorized by this closure transition.

The correction closure is complete; current authoritative evidence does not establish a next authorized operational/roadmap task. UNKNOWN remains UNKNOWN. Separate governance must establish sequencing and separate authorization before implementation. No PI3 or production action is authorized.
PE-5 is a later roadmap capability, not the immediate authorized task. Existing future roadmap commitments retain their order and gates.

### Historical documentation correction candidate next-task snapshot at 5472a85194d105f6fb3d08ce51a4788256d8f028

The following preparation snapshot is preserved as historical evidence. It is not current sequencing or authorization.

### PE-4 Documentation Consistency Correction Validation and Independent Review

Current governed checkpoint: documentation consistency correction, an uncommitted candidate. Validation, independent review and separately authorized commit/push must close this correction before PE-5.
The next numbered roadmap capability remains PE-5, NOT_STARTED and separately authorized.
PE-4 PASS/CLOSED; Public Projection PASS/CLOSED; Phase 7A ACTIVE; PE-5 NOT_STARTED.
Candidate correction acceptance remains pending validation, independent review and separately authorized commit/push.

After those gates, synchronize PI3 release-source to the actual accepted final
closure commit ONLY; STOP and perform independent read-only source review.
OPERATOR_SUPPLIED post-closure PI3 release-source synchronization COMPLETED and independent source review PASS: c7db29f795909d7926e36c02f1166034bcebb8b0 -> 30010c54d3f3078a9b07dada36dfe8dd4db2f6e5 (STOP; review PASS) -> 017686549acb27dbf7a8ad3577d0f84cf9f3f066 (STOP; review PASS). Observed final source tree: 6a59929189bc65fa8487e73ba97477eb009a43f0. Production was not accessed or mutated during this source-only sequence; Codex did not perform or observe it.
Documenting the completed handoff authorizes no new source synchronization,
deployment, validator, inventory, adapter, MQTT, HA, credential, cron or rollback action.

#### Mandatory whole-repository documentation consistency audit

Read-only audit COMPLETED: PASS_CORRECTIONS_REQUIRED; all 74 documents reviewed,
49 findings on 17 existing documentation paths. The current governed correction
updates those paths and eight binding tests with the separately authorized successor
[correction package](PE4_DOCUMENTATION_CONSISTENCY_CORRECTION.md). Historical
checkpoint evidence is preserved. Correction validation and independent review,
then separately authorized commit/push and closure remain required before PE-5.
This uncommitted candidate authorizes no roadmap implementation.

### Historical PE-5 roadmap selection before current production acceptance

Classification: HISTORICAL_INTENTIONALLY_PRESERVED. Current sequencing is the
complete sequence recorded at the start of Next Planned Task, not the prior
selection below.

Current selection is PE-5.1 private pure-resolver repository implementation/validation, followed by independent candidate review. Production and runtime integration remain NOT AUTHORIZED. The following preparation selection is historical at f3730ba5a8745361934ff822a9c29c16c9d0767b.

**Current selection:** PE-5 Implementation Preparation is the current authorized checkpoint, PREPARED_FOR_REVIEW; runtime implementation remains NOT_STARTED / NOT AUTHORIZED. See the current section above and the preparation document. The following NEXT ROADMAP CAPABILITY / no-authorization paragraph is preserved as the historical pre-executive-decision definition; it no longer controls current sequencing.


NEXT ROADMAP CAPABILITY after PE-4; not the immediate operational/governance action.
PE-5 NOT_STARTED; separate governance and authorization required after the PE-4
handoff and mandatory documentation audit are resolved. No PE-5 work is authorized.
Phase 7A ACTIVE; closing PE-4 does not close the remaining passive-enrichment roadmap.

### Historical next tasks before Public Projection production closure

### PE-4 Home Assistant Association Public Projection Corrected Pre-Deployment PI3 Baseline Validation

NOT STARTED / REQUIRED BEFORE DEPLOYMENT. PREPARED FOR SEPARATE AUTHORIZATION.
Synchronize PI3 release-source to the Baseline Correction commit ONLY; STOP and independent source review.
No baseline validator, deployment, production inventory/platform execution, MQTT, HA, credential or cron operation
is authorized by this checkpoint. Capture future exact baseline stdout, STOP, independently review and explicitly
accept before creating a 0600 receipt and independently binding its SHA-256. Never auto-adopt changed values.
Deployment NOT STARTED; Production Execution NOT STARTED; PE-4 NOT COMPLETE; Phase 7A ACTIVE; PE-5 NOT STARTED.

### Historical original pre-deployment baseline validation next task

### PE-4 Home Assistant Association Public Projection Pre-Deployment PI3 Baseline Validation

NOT STARTED / REQUIRED BEFORE DEPLOYMENT. First perform PI3 source synchronization
to the Deployment Preparation commit ONLY; STOP and independent source review.
Then the separately authorized read-only baseline gate must verify production
engine candidate bytes and observed owner/mode, absence of helper/schema/public
namespace, unchanged private/runtime/lock identities and the exact original cron.
Repository evidence does not prove the current deployed engine or its mode.
Review and freeze the exact sanitized baseline receipt and SHA-256 independently.
Any mismatch requires manual governance review; no automatic adoption or deployment.

Public Projection Deployment Preparation PASS/CLOSED; Deployment NOT STARTED /
PREPARED FOR SEPARATE AUTHORIZATION; Production Execution NOT STARTED.
Deployment and first natural inventory cycle acceptance remain separate later gates.
Association scheduler ACTIVE / AUTHORIZED; inventory scheduler ACTIVE; Manual Second
Adapter Execution NOT AUTHORIZED / NOT PERFORMED. PE-4 NOT COMPLETE; Phase 7A ACTIVE;
PE-5 NOT STARTED; rollback NOT PERFORMED. Natural inventory/association cycles may
continue independently. Source sync does not quiesce cron, acquire production
locks, execute inventory/adapter/projection, publish MQTT, contact HA or read credentials.

### Historical public projection deployment preparation next task

### PE-4 Home Assistant Association Public Projection Deployment Preparation

NOT STARTED / REQUIRES SEPARATE AUTHORIZATION. Immediate operator action remains
PI3 source synchronization to the POSIX validation closure commit ONLY;
STOP and independent source review. Deployment Preparation needs separate later
authorization and is not deployment execution. Its future scope must freeze the
inventory-only maintenance window, inventory scheduler quiescence and process drain,
unchanged association scheduler condition, coherent artifact set, helper/contract
before engine, engine last, no forced inventory run, exact schedule restoration,
deployment validation, rollback design, post-deployment production acceptance and
first natural inventory cycle evidence. None of that work is performed here.
POSIX Source Validation PASS/CLOSED based on OPERATOR_SUPPLIED actual PI3 evidence;
Source Implementation IMPLEMENTED / WINDOWS SYNTHETIC VALIDATION PASS;
Preparation PASS/CLOSED; Deployment NOT STARTED; Production Execution NOT STARTED.
Scheduler Deployment PASS/CLOSED; recurring scheduler ACTIVE / AUTHORIZED;
inventory scheduler ACTIVE; Manual Second Adapter Execution NOT AUTHORIZED / NOT PERFORMED.
PE-4 NOT COMPLETE; Phase 7A ACTIVE; PE-5 NOT STARTED; rollback NOT PERFORMED.
Natural inventory/association cycles may continue independently using deployed code;
source sync does not execute them or the validator, authorize deployment or mutate cron.

### Historical public projection source implementation next task

### PE-4 Home Assistant Association Public Projection POSIX Source Validation

NOT STARTED / PREPARED FOR SEPARATE AUTHORIZATION. Immediate action is PI3 source
synchronization to the source implementation commit ONLY; STOP and independent
source review. Synchronization does not authorize the committed read-only validator.
Its execution requires a separate future operator authorization. Do not deploy,
run inventory/adapter/public projection production paths, mutate cron, read HA
credentials, contact HA/broker, perform rollback or begin PE-5 here.
Source Implementation IMPLEMENTED / WINDOWS SYNTHETIC VALIDATION PASS;
Preparation PASS/CLOSED; Deployment NOT STARTED; Production Execution NOT STARTED.
Scheduler Deployment PASS/CLOSED; recurring scheduler ACTIVE / AUTHORIZED;
inventory scheduler ACTIVE; Manual Second Adapter Execution NOT AUTHORIZED / NOT PERFORMED.
PE-4 NOT COMPLETE; Phase 7A ACTIVE; PE-5 NOT STARTED; rollback NOT PERFORMED.
Independent natural inventory/association cron cycles remain unrelated to source sync.

### Historical public projection preparation next task

### PE-4 Home Assistant Association Public Projection

NOT STARTED / PREPARED FOR SEPARATE IMPLEMENTATION. Public Projection Preparation
PASS/CLOSED. PI3 source synchronization to the public projection preparation commit ONLY;
STOP and independent source review. No implementation or deployment is authorized here.
Recurring scheduler ACTIVE / AUTHORIZED; natural 5/35 cycles may continue independently
of source synchronization. Do not run adapter, installer, acceptance or reconciliation,
change crontab, disable association scheduling, contact HA/credentials/broker, run projection,
mutate production, perform rollback or begin PE-5.
Manual Second Adapter Execution NOT AUTHORIZED / NOT PERFORMED; PE-4 NOT COMPLETE;
Phase 7A ACTIVE; PE-5 NOT STARTED; rollback NOT PERFORMED.

### Historical scheduler deployment closure next task

Scheduler Deployment PASS/CLOSED. Historical action: PI3 source synchronization to the scheduler deployment closure
commit ONLY; STOP and independent review. That source predecessor is now independently reviewed.

### Historical scheduler preparation next task

### PE-4 Home Assistant Association Adapter Scheduler Deployment

NOT STARTED / PREPARED FOR SEPARATE AUTHORIZATION. Preparation and Independent Production
Acceptance PASS/CLOSED. Immediate handoff: PI3 source synchronization to the scheduler preparation
commit ONLY; STOP and independent review. No scheduler installation authorized by preparation.
Future execution requires separate authorization and an exclusive operator crontab maintenance
window. No manual adapter run, forced cron trigger, retry/removal or Public Projection.
Second Adapter Execution NOT AUTHORIZED; Public Projection DEFERRED; PE-4 NOT COMPLETE;
Phase 7A ACTIVE; rollback NOT PERFORMED.

### Historical acceptance closure next task

### PE-4 Home Assistant Association Adapter Scheduler Deployment

NOT STARTED. Independent Production Acceptance PASS/CLOSED is the completed prerequisite.
Next handoff: PI3 source synchronization to the acceptance closure commit only; STOP and
independent review. Scheduler checkpoint work and execution require separate authorization.
Do not rerun acceptance, adapter or reconciler or begin Public Projection.
Second Adapter Execution NOT AUTHORIZED; Public Projection DEFERRED; PE-4 NOT COMPLETE;
Phase 7A ACTIVE; rollback NOT PERFORMED.

### Historical acceptance next-task chronology

### PE-4 Home Assistant Association Adapter Independent Production Acceptance

Current checkpoint: Independent Production Acceptance NOT CLOSED. Attempt 1 inspection PASS,
durable capture FAIL; Attempt 2 NOT STARTED / READY FOR SEPARATE AUTHORIZATION.
Immediate operator action: **PI3 source synchronization to the operator-path integration commit only**,
then STOP and independent review; Attempt 2 requires separate explicit authorization.
Native synthetic capture security/durability prerequisite PASS. Historical correction-sync handoff
remains preserved below. Completed historical handoff: source synchronization to
the acceptance preparation commit.
Completed historical handoff: PI3 source synchronization to the durable reconciliation closure commit.
This preparation authorizes no acceptance execution, adapter rerun, scheduler deployment,
production mutation or Public Projection.

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

## PE-5.1 separate caller-integration preparation authorization

The user authorized source-based preparation and bounded repository caller implementation/testing.
Production access/deployment and policy selection are not authorized. The minimal caller reads an
explicit finalized inventory copy, requires explicit evaluation time/maximum age, and returns private
in-memory/stdout output only. Persistence and automatic inventory-engine integration remain deferred.


## PE-5.1 bounded repository implementation authorization

The user separately authorized the Private Local Service Association Contract and Pure Resolver only.
Inputs are finalized inventory, explicit evaluation time and explicitly supplied maximum snapshot age.
No operational age threshold, collector, network/MQTT access, persistence, scheduler,
public projection, runtime integration or production work is authorized. The candidate stops
after repository validation for review and separate commit/push authorization.


## PE-5 executive sequencing decision — preparation only

> if everything related to P4-4 and everything before it is completed successfully and documented, then start with PE-5.

The user explicitly selects PE-5 - MQTT and Passive Service Association as the next
roadmap checkpoint, beginning with Implementation Preparation. This supersedes only
the former current UNKNOWN sequencing state; its historical snapshots are preserved.
The authorization permits repository preparation, not arbitrary implementation or
production work. PE-4 and all completed prerequisites remain closed. The first
implementation checkpoint is PE-5.1 - Private Local Service Association Contract and Pure Resolver,
requiring separate authorization. Source/private relationships do not acquire identity,
canonical-IP, liveness, health, Asset, incident or expected-availability authority.



## 2026-07

Architectural decisions currently in effect:

- Dashboard v2 is the primary operator interface.
- Passive Living Inventory must be completed before Active Discovery.
- HIOC favors operator explanations over raw metrics.
- Historical incident review is a first-class feature.
- Incident testing will occur during real operational events rather than synthetic simulations.
- New features must not interrupt the current implementation phase.
- Scope changes require an intentional revision of this master plan.

## Surveillance roadmap planning — user-established future testing exception

- Surveillance roadmap preservation is documentation only, under future PE-10, using the six approved architectural checkpoints and existing shared HIOC models. Current sequencing and implementation authorization are unchanged.
- Normally, HIOC does not intentionally create failures. For future surveillance reliability testing, controlled and reversible failures are allowed when they can be performed safely, because otherwise we may never be able to prove that HIOC detects important camera and recording failures. This is the explicit future surveillance exception to the normal incident-testing policy above; no failure injection is authorized by this planning record.

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

## Complete PE-5 Execution Roadmap

Classification: HISTORICAL_INTENTIONALLY_PRESERVED planning snapshot accepted in 78ee4cd16120bf4ea3166901994727a19d1faad1. Checkpoint order/Definition of Done remain authoritative; planning-era current-pointer/UNKNOWN statements superseded by PE-5.2 complete design for current status only.


<!-- PE5_EXECUTION_ROADMAP_BEGIN -->

Classification: CURRENT. This user-authorized decomposition resolves the formerly undefined sequence, without starting any implementation or production checkpoint. Original architecture c914cfc4dc39a90005bad42984396291f5b2a751 and preparation f3730ba5a8745361934ff822a9c29c16c9d0767b retain their scope; historical records are immutable.

PE5_STATUS=IN_PROGRESS
PE5_1_STATUS=COMPLETE_THROUGH_ACCEPTED_FIRST_NATIVE_EXECUTION
CURRENT_PE5_CHECKPOINT=PE-5.2 - Mapping Source Authority and Complete Contract Design
PE5_FINAL_CHECKPOINT=PE-5.9 - Final PE-5 Closure and PE-6 Handoff
PE5_FINAL_SUCCESSOR=PE-6
TOTAL_REMAINING_PE5_CHECKPOINTS=8

PE-5.1 remains accepted: policy/source ed3a80508d101652bac89e1dcc111167670aaebc, explicit 2100 seconds, one execution, return 0, valid private output/schema, 8 associations, 0 rejections, inventory/public inventory unchanged, no persistent state or scheduler mutation. Counts are not public authority; the first execution is not repeated.

### Ordered checkpoint table

| Number | Name | Objective | Prerequisite | Type | Production access | Acceptance | Successor |
|---|---|---|---|---|---|---|---|
| PE-5.2 | Mapping Source Authority and Complete Contract Design | Establish source/producer authority first, then close complete mapping, persistence, retention, execution-model and handoff design before implementation. | PE-5.1 | DISCOVERY/DESIGN | READ_ONLY | Resolved facts/invariants/exact identity and concise independent acceptance | PE-5.3 |
| PE-5.3 | Remaining Capability Implementation and Comprehensive Validation | Implement only accepted remaining contracts, including any required private store and disabled execution adapter; comprehensive tests and concise independent candidate acceptance. | PE-5.2 | IMPLEMENTATION/VALIDATION | NONE | Resolved facts/invariants/exact identity and concise independent acceptance | PE-5.4 |
| PE-5.4 | PI3 Release Source Synchronization | Synchronize only the accepted independently verified commit into the PI3 Git release source; no runtime installation. | PE-5.3 | DEPLOYMENT | NONE | Resolved facts/invariants/exact identity and concise independent acceptance | PE-5.5 |
| PE-5.5 | Disabled Production Deployment | Prepare reviewed operator transaction and install the exact accepted remaining payload, with recurring execution disabled. | PE-5.4 | DEPLOYMENT | MUTATING | Resolved facts/invariants/exact identity and concise independent acceptance | PE-5.6 |
| PE-5.6 | Bounded Mapping and Storage Production Validation | One separately authorized bounded mapping-branch execution; validate output and required private-store behavior plus protected invariants before activation. | PE-5.5 | VALIDATION | MUTATING_IF_APPROVED_STORE_REQUIRED_OTHERWISE_READ_ONLY | Resolved facts/invariants/exact identity and concise independent acceptance | PE-5.7 |
| PE-5.7 | Conditional Execution Activation | Activate only the accepted execution model under separate authorization, or accept an explicit not-required receipt and advance. | PE-5.6 | DEPLOYMENT | MUTATING_IF_REQUIRED_OTHERWISE_NONE | Resolved facts/invariants/exact identity and concise independent acceptance | PE-5.8 |
| PE-5.8 | Operational Evidence and Independent Production Acceptance | Observe required natural cycles without manual producer execution; or accept the approved manual model evidence. Independently accept direct results. | PE-5.7 | VALIDATION | READ_ONLY | Resolved facts/invariants/exact identity and concise independent acceptance | PE-5.9 |
| PE-5.9 | Final PE-5 Closure and PE-6 Handoff | Close all coverage/dispositions, operational documentation and private handoff readiness; PE-5 COMPLETE before PE-6. | PE-5.8 | CLOSURE | NONE | Resolved facts/invariants/exact identity and concise independent acceptance | PE-6 |

### Detailed checkpoint contracts

Common rule: separate authorization for every future checkpoint; Codex PI3/PI5/production access prohibited. No PI5 action, live MQTT broker access, Discovery subscriber, publication, credential access or public inventory change is required by this plan. A demonstrated necessity outside these boundaries stops for specific authority, not silent scope expansion. GitHub publication is not PI3 source sync; source sync is not production installation. /home/jazofv1/hioc-release-source remains Git source; /home/jazofv1/hioc remains non-Git runtime. Valid historical COMMITTED PE-4 journals remain preserved, not presumed conflicts or cleaned; unknown active transactions require authoritative review. Source-only operations never authorize runtime changes.

#### PE-5.2 - Mapping Source Authority and Complete Contract Design

- **objective:** Establish source/producer authority first, then close complete mapping, persistence, retention, execution-model and handoff design before implementation.
- **why required:** Original PE-5 scope plus this authorized complete decomposition; no silent omission.
- **authoritative dependency:** Original architecture c914cfc4dc39a90005bad42984396291f5b2a751, preparation f3730ba5a8745361934ff822a9c29c16c9d0767b, accepted PE-5.1 edb406b2243b7256c919a08a7162971265df1d08
- **predecessor:** PE-5.1
- **dependencies:** PE-5.1
- **inputs:** Accepted predecessor evidence; Original descriptive relationship/privacy/protected-field contracts
- **outputs:** Sanitized Evidence Report; Exact accepted artifacts/decisions and next-stage gate
- **established facts:** PE-5.1 accepted; no reopening; Inventory policy explicit 2100 seconds; Planning grants no operational authorization
- **facts resolved:** source/store existence and location, producer/owner authority, identifier and relationship semantics; meaningful timestamps versus configuration version, freshness/expiry/conflict/privacy and secret handling; whether shared private storage is required for PE-5 completion; exact artifact/schema/ownership/permissions/atomic writes/readers/writers/current versus history/retention/LKG/restart/corruption; whether recurring execution is required; trigger/cadence/independent versus inventory or other producer integration/locking/missed execution/restart/failure; exact private file/API/schema/version/freshness/conflict handoff to PE-6
- **types:** DISCOVERY; DESIGN
- **production access:** READ_ONLY
- **repository changes allowed:** Direct design/implementation/evidence/docs only; immutable historical records preserved
- **production observation allowed:** Separately authorized operator-only bounded read-only observation
- **production mutation allowed:** PROHIBITED
- **pi3 operator action required:** True
- **codex pi3 access:** PROHIBITED
- **pi5 action:** NOT_REQUIRED
- **mqtt access:** NOT_REQUIRED; live broker/Discovery/subscription/publication changes outside this plan
- **credential access:** PROHIBITED; any demonstrated necessity stops for specific separate authority and secret-safe contract
- **persistence changes:** Design decision only
- **scheduler changes:** Design decision only
- **inventory engine changes:** Decision only, no code
- **public inventory changes:** PROHIBITED
- **mqtt publication changes:** PROHIBITED
- **tests required:** Focused contract/current bindings; Affected cross-phase consumers; Relevant native regression; full suite for source implementation; Privacy and protected invariants; Synthetic operator/fault validation
- **production validation required:** Future direct operator result when applicable; none during planning; never infer live facts
- **evidence report required:** True
- **acceptance criteria:** All prerequisites established before action; Resolved facts and exact identities; Protected invariants unchanged; Concise independent acceptance; No unauthorized MQTT or later-phase behavior; Signed REQUIRED, NOT_REQUIRED_WITH_AUTHORITY or DEFERRED_OUTSIDE_PE5_WITH_AUTHORITY decisions; no silent waiver of original scope; complete all detail before PE-5.3
- **rollback recovery:** No production rollback; preserve source/evidence
- **stop condition:** STOP on missing authority/prerequisite, mismatch, leak, protected change, failed validation or uncertain mutation; never invent successor
- **successor:** PE-5.3
- **conditional disposition:** Always required
- **authorization:** PLANNED_ONLY_SEPARATE_CHECKPOINT_AUTHORIZATION_REQUIRED

#### PE-5.3 - Remaining Capability Implementation and Comprehensive Validation

- **objective:** Implement only accepted remaining contracts, including any required private store and disabled execution adapter; comprehensive tests and concise independent candidate acceptance.
- **why required:** Original PE-5 scope plus this authorized complete decomposition; no silent omission.
- **authoritative dependency:** Original architecture c914cfc4dc39a90005bad42984396291f5b2a751, preparation f3730ba5a8745361934ff822a9c29c16c9d0767b, accepted PE-5.1 edb406b2243b7256c919a08a7162971265df1d08
- **predecessor:** PE-5.2
- **dependencies:** PE-5.2
- **inputs:** Accepted predecessor evidence; Original descriptive relationship/privacy/protected-field contracts
- **outputs:** Sanitized Evidence Report; Exact accepted artifacts/decisions and next-stage gate
- **established facts:** PE-5.1 accepted; no reopening; Inventory policy explicit 2100 seconds; Planning grants no operational authorization; Accepted complete PE-5.2 decisions
- **facts resolved:** accepted design implemented; exact payload manifest; synthetic tests, privacy review and independent candidate acceptance
- **types:** IMPLEMENTATION; VALIDATION
- **production access:** NONE
- **repository changes allowed:** Direct design/implementation/evidence/docs only; immutable historical records preserved
- **production observation allowed:** NONE
- **production mutation allowed:** PROHIBITED
- **pi3 operator action required:** False
- **codex pi3 access:** PROHIBITED
- **pi5 action:** NOT_REQUIRED
- **mqtt access:** NOT_REQUIRED; live broker/Discovery/subscription/publication changes outside this plan
- **credential access:** PROHIBITED; any demonstrated necessity stops for specific separate authority and secret-safe contract
- **persistence changes:** Accepted PE-5.2 private-storage contract only, separately authorized in production
- **scheduler changes:** Disabled implementation only, no scheduler mutation
- **inventory engine changes:** Only if PE-5.2 proves required and approves isolated additive integration; no PE-5.1 redesign
- **public inventory changes:** PROHIBITED
- **mqtt publication changes:** PROHIBITED
- **tests required:** Focused contract/current bindings; Affected cross-phase consumers; Relevant native regression; full suite for source implementation; Privacy and protected invariants; Synthetic operator/fault validation
- **production validation required:** Future direct operator result when applicable; none during planning; never infer live facts
- **evidence report required:** True
- **acceptance criteria:** All prerequisites established before action; Resolved facts and exact identities; Protected invariants unchanged; Concise independent acceptance; No unauthorized MQTT or later-phase behavior
- **rollback recovery:** No production rollback; preserve source/evidence
- **stop condition:** STOP on missing authority/prerequisite, mismatch, leak, protected change, failed validation or uncertain mutation; never invent successor
- **successor:** PE-5.4
- **conditional disposition:** Always required
- **authorization:** PLANNED_ONLY_SEPARATE_CHECKPOINT_AUTHORIZATION_REQUIRED

#### PE-5.4 - PI3 Release Source Synchronization

- **objective:** Synchronize only the accepted independently verified commit into the PI3 Git release source; no runtime installation.
- **why required:** Original PE-5 scope plus this authorized complete decomposition; no silent omission.
- **authoritative dependency:** Original architecture c914cfc4dc39a90005bad42984396291f5b2a751, preparation f3730ba5a8745361934ff822a9c29c16c9d0767b, accepted PE-5.1 edb406b2243b7256c919a08a7162971265df1d08
- **predecessor:** PE-5.3
- **dependencies:** PE-5.3
- **inputs:** Accepted predecessor evidence; Original descriptive relationship/privacy/protected-field contracts
- **outputs:** Sanitized Evidence Report; Exact accepted artifacts/decisions and next-stage gate
- **established facts:** PE-5.1 accepted; no reopening; Inventory policy explicit 2100 seconds; Planning grants no operational authorization; Accepted complete PE-5.2 decisions
- **facts resolved:** exact commit, parent/subject/scope; source main/origin clean and synchronized
- **types:** DEPLOYMENT
- **production access:** NONE
- **repository changes allowed:** Safe preparation/evidence/closure docs and exact bindings; no ad hoc implementation
- **production observation allowed:** NONE
- **production mutation allowed:** PROHIBITED
- **pi3 operator action required:** True
- **codex pi3 access:** PROHIBITED
- **pi5 action:** NOT_REQUIRED
- **mqtt access:** NOT_REQUIRED; live broker/Discovery/subscription/publication changes outside this plan
- **credential access:** PROHIBITED; any demonstrated necessity stops for specific separate authority and secret-safe contract
- **persistence changes:** PROHIBITED
- **scheduler changes:** PROHIBITED
- **inventory engine changes:** PROHIBITED
- **public inventory changes:** PROHIBITED
- **mqtt publication changes:** PROHIBITED
- **tests required:** Focused contract/current bindings; Affected cross-phase consumers; Relevant native regression; full suite for source implementation; Privacy and protected invariants; Synthetic operator/fault validation
- **production validation required:** Future direct operator result when applicable; none during planning; never infer live facts
- **evidence report required:** True
- **acceptance criteria:** All prerequisites established before action; Resolved facts and exact identities; Protected invariants unchanged; Concise independent acceptance; No unauthorized MQTT or later-phase behavior
- **rollback recovery:** No production rollback; preserve source/evidence
- **stop condition:** STOP on missing authority/prerequisite, mismatch, leak, protected change, failed validation or uncertain mutation; never invent successor
- **successor:** PE-5.5
- **conditional disposition:** Always required
- **authorization:** PLANNED_ONLY_SEPARATE_CHECKPOINT_AUTHORIZATION_REQUIRED

#### PE-5.5 - Disabled Production Deployment

- **objective:** Prepare reviewed operator transaction and install the exact accepted remaining payload, with recurring execution disabled.
- **why required:** Original PE-5 scope plus this authorized complete decomposition; no silent omission.
- **authoritative dependency:** Original architecture c914cfc4dc39a90005bad42984396291f5b2a751, preparation f3730ba5a8745361934ff822a9c29c16c9d0767b, accepted PE-5.1 edb406b2243b7256c919a08a7162971265df1d08
- **predecessor:** PE-5.4
- **dependencies:** PE-5.4
- **inputs:** Accepted predecessor evidence; Original descriptive relationship/privacy/protected-field contracts
- **outputs:** Sanitized Evidence Report; Exact accepted artifacts/decisions and next-stage gate
- **established facts:** PE-5.1 accepted; no reopening; Inventory policy explicit 2100 seconds; Planning grants no operational authorization; Accepted complete PE-5.2 decisions
- **facts resolved:** exact installed identities and metadata; inactive activation state; current prerequisites and provenance-bound rollback
- **types:** DEPLOYMENT
- **production access:** MUTATING
- **repository changes allowed:** Safe preparation/evidence/closure docs and exact bindings; no ad hoc implementation
- **production observation allowed:** Separately authorized operator-only bounded read-only observation
- **production mutation allowed:** Exact approved inactive installation only
- **pi3 operator action required:** True
- **codex pi3 access:** PROHIBITED
- **pi5 action:** NOT_REQUIRED
- **mqtt access:** NOT_REQUIRED; live broker/Discovery/subscription/publication changes outside this plan
- **credential access:** PROHIBITED; any demonstrated necessity stops for specific separate authority and secret-safe contract
- **persistence changes:** Accepted PE-5.2 private-storage contract only, separately authorized in production
- **scheduler changes:** PROHIBITED
- **inventory engine changes:** Only if PE-5.2 proves required and approves isolated additive integration; no PE-5.1 redesign
- **public inventory changes:** PROHIBITED
- **mqtt publication changes:** PROHIBITED
- **tests required:** Focused contract/current bindings; Affected cross-phase consumers; Relevant native regression; full suite for source implementation; Privacy and protected invariants; Synthetic operator/fault validation
- **production validation required:** Future direct operator result when applicable; none during planning; never infer live facts
- **evidence report required:** True
- **acceptance criteria:** All prerequisites established before action; Resolved facts and exact identities; Protected invariants unchanged; Concise independent acceptance; No unauthorized MQTT or later-phase behavior
- **rollback recovery:** Reviewed exact provenance-bound recovery before mutation; preserve historical journals; no guessed cleanup, broad rollback or repeated execution
- **stop condition:** STOP on missing authority/prerequisite, mismatch, leak, protected change, failed validation or uncertain mutation; never invent successor
- **successor:** PE-5.6
- **conditional disposition:** Always required
- **authorization:** PLANNED_ONLY_SEPARATE_CHECKPOINT_AUTHORIZATION_REQUIRED

#### PE-5.6 - Bounded Mapping and Storage Production Validation

- **objective:** One separately authorized bounded mapping-branch execution; validate output and required private-store behavior plus protected invariants before activation.
- **why required:** Original PE-5 scope plus this authorized complete decomposition; no silent omission.
- **authoritative dependency:** Original architecture c914cfc4dc39a90005bad42984396291f5b2a751, preparation f3730ba5a8745361934ff822a9c29c16c9d0767b, accepted PE-5.1 edb406b2243b7256c919a08a7162971265df1d08
- **predecessor:** PE-5.5
- **dependencies:** PE-5.5
- **inputs:** Accepted predecessor evidence; Original descriptive relationship/privacy/protected-field contracts
- **outputs:** Sanitized Evidence Report; Exact accepted artifacts/decisions and next-stage gate
- **established facts:** PE-5.1 accepted; no reopening; Inventory policy explicit 2100 seconds; Planning grants no operational authorization; Accepted complete PE-5.2 decisions
- **facts resolved:** direct native mapping evidence/output identity, bounds, missing/duplicate/conflict cases and approved store/restart/corruption behavior where applicable
- **types:** VALIDATION
- **production access:** MUTATING_IF_APPROVED_STORE_REQUIRED_OTHERWISE_READ_ONLY
- **repository changes allowed:** Safe preparation/evidence/closure docs and exact bindings; no ad hoc implementation
- **production observation allowed:** Separately authorized operator-only bounded read-only observation
- **production mutation allowed:** Accepted mapping branch/private store operation only; never another PE-5.1 first execution
- **pi3 operator action required:** True
- **codex pi3 access:** PROHIBITED
- **pi5 action:** NOT_REQUIRED
- **mqtt access:** NOT_REQUIRED; live broker/Discovery/subscription/publication changes outside this plan
- **credential access:** PROHIBITED; any demonstrated necessity stops for specific separate authority and secret-safe contract
- **persistence changes:** Accepted PE-5.2 private-storage contract only, separately authorized in production
- **scheduler changes:** PROHIBITED
- **inventory engine changes:** PROHIBITED
- **public inventory changes:** PROHIBITED
- **mqtt publication changes:** PROHIBITED
- **tests required:** Focused contract/current bindings; Affected cross-phase consumers; Relevant native regression; full suite for source implementation; Privacy and protected invariants; Synthetic operator/fault validation
- **production validation required:** Future direct operator result when applicable; none during planning; never infer live facts
- **evidence report required:** True
- **acceptance criteria:** All prerequisites established before action; Resolved facts and exact identities; Protected invariants unchanged; Concise independent acceptance; No unauthorized MQTT or later-phase behavior
- **rollback recovery:** Reviewed exact provenance-bound recovery before mutation; preserve historical journals; no guessed cleanup, broad rollback or repeated execution
- **stop condition:** STOP on missing authority/prerequisite, mismatch, leak, protected change, failed validation or uncertain mutation; never invent successor
- **successor:** PE-5.7
- **conditional disposition:** Always required
- **authorization:** PLANNED_ONLY_SEPARATE_CHECKPOINT_AUTHORIZATION_REQUIRED

#### PE-5.7 - Conditional Execution Activation

- **objective:** Activate only the accepted execution model under separate authorization, or accept an explicit not-required receipt and advance.
- **why required:** Original PE-5 scope plus this authorized complete decomposition; no silent omission.
- **authoritative dependency:** Original architecture c914cfc4dc39a90005bad42984396291f5b2a751, preparation f3730ba5a8745361934ff822a9c29c16c9d0767b, accepted PE-5.1 edb406b2243b7256c919a08a7162971265df1d08
- **predecessor:** PE-5.6
- **dependencies:** PE-5.6
- **inputs:** Accepted predecessor evidence; Original descriptive relationship/privacy/protected-field contracts
- **outputs:** Sanitized Evidence Report; Exact accepted artifacts/decisions and next-stage gate
- **established facts:** PE-5.1 accepted; no reopening; Inventory policy explicit 2100 seconds; Planning grants no operational authorization; Accepted complete PE-5.2 decisions
- **facts resolved:** activation necessity/mechanism already approved by PE-5.2; exact activation result or not-required receipt
- **types:** DEPLOYMENT
- **production access:** MUTATING_IF_REQUIRED_OTHERWISE_NONE
- **repository changes allowed:** Safe preparation/evidence/closure docs and exact bindings; no ad hoc implementation
- **production observation allowed:** Separately authorized operator-only bounded read-only observation
- **production mutation allowed:** Accepted activation only
- **pi3 operator action required:** True
- **codex pi3 access:** PROHIBITED
- **pi5 action:** NOT_REQUIRED
- **mqtt access:** NOT_REQUIRED; live broker/Discovery/subscription/publication changes outside this plan
- **credential access:** PROHIBITED; any demonstrated necessity stops for specific separate authority and secret-safe contract
- **persistence changes:** PROHIBITED
- **scheduler changes:** Accepted model activation under separate authorization
- **inventory engine changes:** Only if PE-5.2 proves required and approves isolated additive integration; no PE-5.1 redesign
- **public inventory changes:** PROHIBITED
- **mqtt publication changes:** PROHIBITED
- **tests required:** Focused contract/current bindings; Affected cross-phase consumers; Relevant native regression; full suite for source implementation; Privacy and protected invariants; Synthetic operator/fault validation
- **production validation required:** Future direct operator result when applicable; none during planning; never infer live facts
- **evidence report required:** True
- **acceptance criteria:** All prerequisites established before action; Resolved facts and exact identities; Protected invariants unchanged; Concise independent acceptance; No unauthorized MQTT or later-phase behavior
- **rollback recovery:** Reviewed exact provenance-bound recovery before mutation; preserve historical journals; no guessed cleanup, broad rollback or repeated execution
- **stop condition:** STOP on missing authority/prerequisite, mismatch, leak, protected change, failed validation or uncertain mutation; never invent successor
- **successor:** PE-5.8
- **conditional disposition:** Approved PE-5.2 not-required receipt may close this conditional stage with the same fixed successor
- **authorization:** PLANNED_ONLY_SEPARATE_CHECKPOINT_AUTHORIZATION_REQUIRED

#### PE-5.8 - Operational Evidence and Independent Production Acceptance

- **objective:** Observe required natural cycles without manual producer execution; or accept the approved manual model evidence. Independently accept direct results.
- **why required:** Original PE-5 scope plus this authorized complete decomposition; no silent omission.
- **authoritative dependency:** Original architecture c914cfc4dc39a90005bad42984396291f5b2a751, preparation f3730ba5a8745361934ff822a9c29c16c9d0767b, accepted PE-5.1 edb406b2243b7256c919a08a7162971265df1d08
- **predecessor:** PE-5.7
- **dependencies:** PE-5.7
- **inputs:** Accepted predecessor evidence; Original descriptive relationship/privacy/protected-field contracts
- **outputs:** Sanitized Evidence Report; Exact accepted artifacts/decisions and next-stage gate
- **established facts:** PE-5.1 accepted; no reopening; Inventory policy explicit 2100 seconds; Planning grants no operational authorization; Accepted complete PE-5.2 decisions
- **facts resolved:** natural-cycle/overlap/missed-cycle/staleness/failure evidence required by contract; independent production acceptance
- **types:** VALIDATION
- **production access:** READ_ONLY
- **repository changes allowed:** Safe preparation/evidence/closure docs and exact bindings; no ad hoc implementation
- **production observation allowed:** Separately authorized operator-only bounded read-only observation
- **production mutation allowed:** PROHIBITED
- **pi3 operator action required:** True
- **codex pi3 access:** PROHIBITED
- **pi5 action:** NOT_REQUIRED
- **mqtt access:** NOT_REQUIRED; live broker/Discovery/subscription/publication changes outside this plan
- **credential access:** PROHIBITED; any demonstrated necessity stops for specific separate authority and secret-safe contract
- **persistence changes:** PROHIBITED
- **scheduler changes:** PROHIBITED
- **inventory engine changes:** PROHIBITED
- **public inventory changes:** PROHIBITED
- **mqtt publication changes:** PROHIBITED
- **tests required:** Focused contract/current bindings; Affected cross-phase consumers; Relevant native regression; full suite for source implementation; Privacy and protected invariants; Synthetic operator/fault validation
- **production validation required:** Future direct operator result when applicable; none during planning; never infer live facts
- **evidence report required:** True
- **acceptance criteria:** All prerequisites established before action; Resolved facts and exact identities; Protected invariants unchanged; Concise independent acceptance; No unauthorized MQTT or later-phase behavior
- **rollback recovery:** No production rollback; preserve source/evidence
- **stop condition:** STOP on missing authority/prerequisite, mismatch, leak, protected change, failed validation or uncertain mutation; never invent successor
- **successor:** PE-5.9
- **conditional disposition:** Approved PE-5.2 not-required receipt may close this conditional stage with the same fixed successor
- **authorization:** PLANNED_ONLY_SEPARATE_CHECKPOINT_AUTHORIZATION_REQUIRED

#### PE-5.9 - Final PE-5 Closure and PE-6 Handoff

- **objective:** Close all coverage/dispositions, operational documentation and private handoff readiness; PE-5 COMPLETE before PE-6.
- **why required:** Original PE-5 scope plus this authorized complete decomposition; no silent omission.
- **authoritative dependency:** Original architecture c914cfc4dc39a90005bad42984396291f5b2a751, preparation f3730ba5a8745361934ff822a9c29c16c9d0767b, accepted PE-5.1 edb406b2243b7256c919a08a7162971265df1d08
- **predecessor:** PE-5.8
- **dependencies:** PE-5.8
- **inputs:** Accepted predecessor evidence; Original descriptive relationship/privacy/protected-field contracts
- **outputs:** Sanitized Evidence Report; Exact accepted artifacts/decisions and next-stage gate
- **established facts:** PE-5.1 accepted; no reopening; Inventory policy explicit 2100 seconds; Planning grants no operational authorization; Accepted complete PE-5.2 decisions
- **facts resolved:** complete coverage/evidence ledger; private handoff contract and operational documents; no unknown completion requirements
- **types:** CLOSURE
- **production access:** NONE
- **repository changes allowed:** Direct design/implementation/evidence/docs only; immutable historical records preserved
- **production observation allowed:** NONE
- **production mutation allowed:** PROHIBITED
- **pi3 operator action required:** False
- **codex pi3 access:** PROHIBITED
- **pi5 action:** NOT_REQUIRED
- **mqtt access:** NOT_REQUIRED; live broker/Discovery/subscription/publication changes outside this plan
- **credential access:** PROHIBITED; any demonstrated necessity stops for specific separate authority and secret-safe contract
- **persistence changes:** PROHIBITED
- **scheduler changes:** PROHIBITED
- **inventory engine changes:** PROHIBITED
- **public inventory changes:** PROHIBITED
- **mqtt publication changes:** PROHIBITED
- **tests required:** Focused contract/current bindings; Affected cross-phase consumers; Relevant native regression; full suite for source implementation; Privacy and protected invariants; Synthetic operator/fault validation
- **production validation required:** Future direct operator result when applicable; none during planning; never infer live facts
- **evidence report required:** True
- **acceptance criteria:** All prerequisites established before action; Resolved facts and exact identities; Protected invariants unchanged; Concise independent acceptance; No unauthorized MQTT or later-phase behavior
- **rollback recovery:** No production rollback; preserve source/evidence
- **stop condition:** STOP on missing authority/prerequisite, mismatch, leak, protected change, failed validation or uncertain mutation; never invent successor
- **successor:** PE-6
- **conditional disposition:** Always required
- **authorization:** PLANNED_ONLY_SEPARATE_CHECKPOINT_AUTHORIZATION_REQUIRED

### Original requirement coverage

| Requirement | Disposition | Checkpoints |
|---|---|---|
| local service ownership relationships | COVERED_BY_COMPLETED_PE5_1 | PE-5.1 |
| systemd evidence | COVERED_BY_COMPLETED_PE5_1 | PE-5.1 |
| ss/listening-socket evidence | COVERED_BY_COMPLETED_PE5_1 | PE-5.1 |
| stable device binding | COVERED_BY_COMPLETED_PE5_1 | PE-5.1 |
| stable relationship identifiers | ASSIGNED_TO_PE5_X | PE-5.2, PE-5.3, PE-5.6, PE-5.8, PE-5.9 |
| source provenance | ASSIGNED_TO_PE5_X | PE-5.2, PE-5.3, PE-5.6, PE-5.8, PE-5.9 |
| rule provenance | ASSIGNED_TO_PE5_X | PE-5.2, PE-5.3, PE-5.6, PE-5.8, PE-5.9 |
| configured MQTT mappings | ASSIGNED_TO_PE5_X | PE-5.2, PE-5.3, PE-5.6, PE-5.8, PE-5.9 |
| MQTT association evidence | ASSIGNED_TO_PE5_X | PE-5.2, PE-5.3, PE-5.6, PE-5.8, PE-5.9 |
| mapping source authority | ASSIGNED_TO_PE5_X | PE-5.2 |
| mapping producer authority | ASSIGNED_TO_PE5_X | PE-5.2 |
| mapping identifier semantics | ASSIGNED_TO_PE5_X | PE-5.2 |
| mapping relationship semantics | ASSIGNED_TO_PE5_X | PE-5.2 |
| mapping freshness | ASSIGNED_TO_PE5_X | PE-5.2 |
| mapping expiry | ASSIGNED_TO_PE5_X | PE-5.2 |
| duplicate handling | ASSIGNED_TO_PE5_X | PE-5.2, PE-5.3, PE-5.6, PE-5.8, PE-5.9 |
| conflict handling | ASSIGNED_TO_PE5_X | PE-5.2, PE-5.3, PE-5.6, PE-5.8, PE-5.9 |
| missing endpoint handling | ASSIGNED_TO_PE5_X | PE-5.2, PE-5.3, PE-5.6, PE-5.8, PE-5.9 |
| privacy | ASSIGNED_TO_PE5_X | PE-5.2, PE-5.3, PE-5.6, PE-5.8, PE-5.9 |
| credentials/secrets | ASSIGNED_TO_PE5_X | PE-5.2, PE-5.3, PE-5.6, PE-5.8, PE-5.9 |
| topic leakage prevention | ASSIGNED_TO_PE5_X | PE-5.2, PE-5.3, PE-5.6, PE-5.8, PE-5.9 |
| no identity authority | ASSIGNED_TO_PE5_X | PE-5.2, PE-5.3, PE-5.6, PE-5.8, PE-5.9 |
| no canonical-IP authority | ASSIGNED_TO_PE5_X | PE-5.2, PE-5.3, PE-5.6, PE-5.8, PE-5.9 |
| no liveness authority | ASSIGNED_TO_PE5_X | PE-5.2, PE-5.3, PE-5.6, PE-5.8, PE-5.9 |
| no health authority | ASSIGNED_TO_PE5_X | PE-5.2, PE-5.3, PE-5.6, PE-5.8, PE-5.9 |
| bounded diff | ASSIGNED_TO_PE5_X | PE-5.2, PE-5.3, PE-5.6, PE-5.8, PE-5.9 |
| unchanged publish/subscribe behavior | ASSIGNED_TO_PE5_X | PE-5.2, PE-5.3, PE-5.6, PE-5.8, PE-5.9 |
| persistence requirement | ASSIGNED_TO_PE5_X | PE-5.2 |
| recurring execution decision | ASSIGNED_TO_PE5_X | PE-5.2 |
| producer/inventory integration decision | ASSIGNED_TO_PE5_X | PE-5.2 |
| retention decision | ASSIGNED_TO_PE5_X | PE-5.2 |
| deployment | ASSIGNED_TO_PE5_X | PE-5.4, PE-5.5 |
| bounded production validation | ASSIGNED_TO_PE5_X | PE-5.6, PE-5.8 |
| independent acceptance | ASSIGNED_TO_PE5_X | PE-5.3, PE-5.6, PE-5.8, PE-5.9 |
| operational documentation | ASSIGNED_TO_PE5_X | PE-5.2, PE-5.9 |
| final PE-5 closure | ASSIGNED_TO_PE5_X | PE-5.9 |
| PE-6 handoff readiness | ASSIGNED_TO_PE5_X | PE-5.2, PE-5.3, PE-5.8, PE-5.9 |

Local-branch completion never waives mapping-branch invariants. PE-5.2 decides REQUIRED / NOT_REQUIRED_WITH_AUTHORITY / DEFERRED_OUTSIDE_PE5_WITH_AUTHORITY with explicit evidence; original scope cannot be silently cancelled. Required storage: implementation PE-5.3, deployment PE-5.5, validation PE-5.6/8, acceptance PE-5.9. Required execution adapter: implementation PE-5.3, inactive deployment PE-5.5, activation PE-5.7, natural validation PE-5.8 and closure PE-5.9. Conditional receipts retain fixed successors, not new checkpoint discovery.

### UNKNOWN resolution matrix

| Unknown fact | Resolution | Blocks |
|---|---|---|
| source/store existence and location, producer/owner authority, identifier and relationship semantics | PE-5.2 | PE-5.3, PE-5.4, PE-5.5, PE-5.6, PE-5.7, PE-5.8, PE-5.9 |
| meaningful timestamps versus configuration version, freshness/expiry/conflict/privacy and secret handling | PE-5.2 | PE-5.3, PE-5.4, PE-5.5, PE-5.6, PE-5.7, PE-5.8, PE-5.9 |
| whether shared private storage is required for PE-5 completion; exact artifact/schema/ownership/permissions/atomic writes/readers/writers/current versus history/retention/LKG/restart/corruption | PE-5.2 | PE-5.3, PE-5.4, PE-5.5, PE-5.6, PE-5.7, PE-5.8, PE-5.9 |
| whether recurring execution is required; trigger/cadence/independent versus inventory or other producer integration/locking/missed execution/restart/failure | PE-5.2 | PE-5.3, PE-5.4, PE-5.5, PE-5.6, PE-5.7, PE-5.8, PE-5.9 |
| exact private file/API/schema/version/freshness/conflict handoff to PE-6 | PE-5.2 | PE-5.3, PE-5.4, PE-5.5, PE-5.6, PE-5.7, PE-5.8, PE-5.9 |
| exact commit, parent/subject/scope; source main/origin clean and synchronized | PE-5.4 | PE-5.5, PE-5.6, PE-5.7, PE-5.8, PE-5.9 |
| exact installed identities and metadata; inactive activation state; current prerequisites and provenance-bound rollback | PE-5.5 | PE-5.6, PE-5.7, PE-5.8, PE-5.9 |
| direct native mapping evidence/output identity, bounds, missing/duplicate/conflict cases and approved store/restart/corruption behavior where applicable | PE-5.6 | PE-5.7, PE-5.8, PE-5.9 |
| activation necessity/mechanism already approved by PE-5.2; exact activation result or not-required receipt | PE-5.7 | PE-5.8, PE-5.9 |
| natural-cycle/overlap/missed-cycle/staleness/failure evidence required by contract; independent production acceptance | PE-5.8 | PE-5.9 |
| complete coverage/evidence ledger; private handoff contract and operational documents; no unknown completion requirements | PE-5.9 |  |

### PE-5 Definition of Done

1. Accepted local branch preserved; no repeated PE-5.1 first execution.
2. Declared mapping source/producer/identifier/time/expiry authority established.
3. Local and mapping relationships stable/deterministic/bounded with source/rule provenance.
4. Ambiguity/missing endpoints/duplicates/conflicts handled by accepted contract.
5. No transport-based identity/canonical-IP/observation/liveness/health authority.
6. No secrets/topic leakage/private raw exposure/public or publish-subscribe compatibility change.
7. Private-storage/current-history/retention/LKG/restart/corruption disposition approved and implemented/validated if required.
8. Execution/trigger/cadence/integration/locking/missed/failure disposition approved; required activation and natural cycles accepted.
9. Governed source sync, exact deployment, bounded validation and independent acceptance complete.
10. Private file/API/schema/version/freshness/conflict handoff sufficient for PE-6, without implementing PE-6.
11. Operational docs answer what/why/how/source/freshness/failure/rollback; Master Plan synchronized.
12. Privacy-safe durable Evidence Reports/exact commit identities; source/runtime separation and clean synchronized Git.
13. Every original requirement COMPLETE or explicit authorized outside-phase/not-required disposition; no unknown completion requirement.
14. Only after all gates PE5_STATUS=COMPLETE; PE-6 then becomes next passive-enrichment checkpoint under separate authorization.

### Efficiency review

Source-authority observation and complete contract design are combined in PE-5.2: evidence first, design next, no production mutation. Mapping/schema/storage/execution/retention/handoff decisions are one package. Implementation, comprehensive validation, privacy review and concise independent acceptance are combined in PE-5.3. Each production checkpoint includes safe preparation, authorized operator action, direct-result review and documentation closure. Commit/identity verification/push/independent GitHub verification are gates inside checkpoints, not acceptance-only micro-checkpoints.

Keep PE-5.2 before implementation while unknown decisions remain. Keep source sync PE-5.4 separate from production deployment PE-5.5: source acceptance cannot authorize runtime mutation. Keep inactive installation before bounded execution PE-5.6 so exact installed identity/rollback are accepted first. Keep execution before activation PE-5.7 because scheduling changes execution and recovery authority. Keep activation before natural evidence PE-5.8: no forced producer run or assumed future cycle. Whole-phase PE-5.9 closes all requirements/handoff, not identical-byte rereviews. Eight is the fewest safe structural stages under these source/mutation/execution/evidence boundaries, with conditional gates closed only by accepted not-required receipts.

### Deferred cross-phase work

- PE-6 classification/role_suggestion/metadata_quality.
- PE-7 expected availability/permanent IoT monitoring.
- PE-8 functional/automation impact.
- PE-9 dependency intelligence/automatic service relationships/improved graph/topology.
- PE-10 application/integration/service assurance/surveillance reliability.
- MQTT Discovery/live broker/client/topic observation/new public projection or publication.
- DHCP service health/capacity.
- canonical-address changes.
- phone notifications.
- Asset-aware retention/archive.
- incident-history validator hardening.
- backup/disaster recovery/hardware migration.
- cold-boot/power-loss recovery.
- failure propagation visualization.
- historical trends.
- predictive recommendations.
- Safe Active Discovery.

### Audit and validation authority

Task L.5 precedes Task M. Every tracked baseline file (428) was searched without exclusions. Counts use one classified file-level reference group per keyword-matched or explicitly traced dependency file, retaining literal keyword-hit counts and separate test-binding functions. Three new candidate record/schema/test files are reviewed separately from the 428-file tracked baseline. The canonical record/schema in governance/pe5 use the existing exact typed checkpoint convention, not a new governance hierarchy. Original preparation/implementation/caller/policy records stay historical; current consumers follow an exact successor artifact map. Historical validator bodies read their accepted Git snapshots. The roadmap validator likewise resolves its unique accepted child of the planning baseline by exact subject/parent and replays that immutable object, rather than requiring every future HEAD to be the roadmap commit. Every later checkpoint must synchronize its directly affected current-consumer artifact bindings within its existing implementation/evidence scope; this is an explicit lifecycle dependency, not a new planning checkpoint. See governance/pe5/pe5-execution-roadmap.json for all reference classifications, contradiction dispositions and affected tests. Acceptance requires focused/current consumers, affected cross-phase tests, broader PE regression and full native suite; zero unexplained material references or known static contradictions. No technical checkpoint runs in this planning task.

<!-- PE5_EXECUTION_ROADMAP_END -->

## Current PE-5.2 complete contract design

Classification: HISTORICAL_INTENTIONALLY_PRESERVED PE-5.2 lifecycle snapshot at 72e878f9c0c8f5d3fe6357979e045943f3cf9d34. PE5_2_STATUS=COMPLETE_CONTRACT_DESIGN; PE5_3_STARTED=FALSE.
Current next checkpoint: PE-5.3 - Remaining Capability Implementation and Comprehensive Validation.
See [PE-5.2 complete contract design](PE5_MAPPING_CONTRACT_DESIGN.md) and
governance/pe5/pe5-mapping-contract-design.json for source, relationship, schema, privacy,
storage, execution and private PE-6 handoff decisions. Original undefined source/store/
freshness is now DESIGN, not a discovered store. No universal production absence claimed.
Future private configuration config/enrichment/mqtt_mappings.json remains distinct from
known-infrastructure DEVICE METADATA and generated state/enrichment/service_associations/current.json.
Opaque endpoint IDs require no raw topics or live broker/HA/client/Discovery access.
Private source/output persistence required; standalone 15-minute recurrence and 20-minute
handoff validity are selected NEW DESIGN values, not observed schedules. Inventory
freshness remains 2100 seconds; accepted PE-5.1 runtime/caller/schema/rules unchanged.
No public payload/topic/subscription/retention, inventory writer, scheduler or production
change authorized. Separate authorization is required for PE-5.3 and all later checkpoints;
original eight-stage ordering unchanged. PE-6 classification/role_suggestion/metadata_quality
and future Discovery remain outside PE-5.

## Historical PE-5.3 repository implementation

Classification: HISTORICAL_INTENTIONALLY_PRESERVED. PE5_3_STATUS=COMPLETE_REPOSITORY_IMPLEMENTATION; PE5_4_STARTED=FALSE.
Current next checkpoint: PE-5.4 - PI3 Release Source Synchronization.
The configured mapping resolver, private POSIX composer/store, explicit source installer
and bounded durability recovery are implemented in the repository. Activation remains
disabled; no source provisioning, PI3 synchronization, deployment or production execution
has occurred. PE-5 remains IN_PROGRESS, PE-5.1 remains accepted/closed, PE-4 and Public
Projection remain PASS/CLOSED, and Phase 7A remains ACTIVE.
The PE-5.2 design and its corrected durability contract are unchanged authority.
See [PE-5.3 repository implementation](PE5_CONFIGURED_ASSOCIATION_IMPLEMENTATION.md) and its exact governance payload.
Separate authorization is required for PE-5.4 and every later lifecycle checkpoint.

## Historical PE-5.6 initial infrastructure defect correction

Classification: HISTORICAL_INTENTIONALLY_PRESERVED. Phase 7A ACTIVE; PE-5 IN_PROGRESS; PE-4 and Public Projection PASS/CLOSED.
PE5_3_STATUS=COMPLETE_REPOSITORY_IMPLEMENTATION.
CURRENT_PE5_CHECKPOINT=PE-5.6.
PE5_6_STATUS=BLOCKED_PENDING_CORRECTED_DEPLOYMENT_AND_SEPARATE_RETRY.
PE5_7_STARTED=FALSE. Recurring execution remains disabled.

OPERATOR_SUPPLIED evidence reports PE-5.5 installed the accepted six-artifact disabled
payload. The first PE-5.6 approved revision-1 source installation returned
WRITE_FAILED / LOCK_UNAVAILABLE. This was missing infrastructure, not lock contention.
Post-failure observation established config exists, jazofv1:jazofv1 mode0755; no
config/enrichment, source, source sidecar, state/enrichment, output parent, lock,
output or output sidecar existed; no relevant installer/composer process was running.
Candidate /home/jazofv1/pe5-mqtt-mappings-candidate.json remained intact,
SHA256 961b72e8918606caeac565a8d472d03c4784d9a3b43eae6deb4085865330d295.

The implementation incorrectly required the shared lock parent to preexist before
initialization. Repository correction now bounds directory creation to approved
initial source installation. No retry has occurred. Corrected production deployment
is NOT ESTABLISHED. Source state does not prove production state.
Next operator actions: independently accept repository correction, synchronize exact
accepted source, replace only changed accepted payload bytes, independently accept
corrected deployment, then separately authorize the PE-5.6 initialization retry.
No composer invocation, scheduler activation, recovery, or PE-5.7 is authorized here.
See [configured association implementation](PE5_CONFIGURED_ASSOCIATION_IMPLEMENTATION.md).
Separate authorization is required for the retry and every later checkpoint.

## Historical PE-5.6 final acceptance and closure

Classification: HISTORICAL_INTENTIONALLY_PRESERVED. Phase 7A ACTIVE; PE-5 IN_PROGRESS.
PE5_6_STATUS=COMPLETE/PASS; PE5_7_STARTED=FALSE; RECURRING_EXECUTION_ACTIVE=FALSE.
Current next checkpoint: PE-5.7 - Conditional Execution Activation.
PE-4/Public Projection remain PASS/CLOSED; PE-5.1 remains accepted/closed.

OPERATOR_SUPPLIED production evidence establishes corrected one-artifact deployment
of commit 4990c62afbce22a804229f3cb8329986741067a6, then one separately authorized
corrected initial installation PASS_PRIVATE_PERSISTENCE / CONFIRMED_DURABLE_CURRENT,
then exactly one separately authorized bounded composer execution
PASS_PRIVATE_ASSOCIATIONS / ACCEPTED_COUNT=1 / REJECTED_COUNT=0.
This is not recurring execution. No second corrected installation or extra composer
execution is authorized by closure. PE-5.7 has not executed; scheduler remains disabled.

The first initialization WRITE_FAILED / LOCK_UNAVAILABLE remains historical evidence.
The correction fixed missing-directory bootstrap before the shared lock; no lock
contention was established. Failed-attempt absence evidence and the intact candidate
are preserved alongside the accepted correction and separately authorized success.

Configured source revision1 SHA256:
961b72e8918606caeac565a8d472d03c4784d9a3b43eae6deb4085865330d295.
Configured relationship:
mqra_01d1d5edfdc1db0fa63b14b5b9b0b9701b4ff183a946fcb63751fb14910fe028.
Provenance: operator_mqtt_v1 / configured_mqtt / declared_endpoint_device_v1.
Generated output SHA256:
f1b219dc413325a557c71e3561804afcc3bdf26f87d2d6fdb71bb3e7c97f5e2c.
Both durability domains were observed CONFIRMED, candidate=null, bound to revision1;
exact transaction identities, metadata and source/output observations are recorded in
the existing implementation governance record's production_validation evidence.

The local branch retained eight existing_service_ownership/high relationships under
unchanged schema1.0 / 2100-second policy. The receipt is historically bound to consumed
inventory SHA256 394b5cf4007fccd1aec0beb862f29ed6dfb78a76a2903cb6174b08f0c5d17607,
updated 2026-10-14T17:00:01.000000Z, evaluated 2026-10-14T17:04:50.224530Z,
valid_until 2026-10-14T17:24:50.224530Z. Later observed inventory SHA differed;
its cause is UNKNOWN, the difference alone is not a defect and does not rebind the
receipt. No present receipt consumability or freshness is asserted.

The bounded public-inventory search for the five reported configured-MQTT terms found
zero matches: PASS for that check only. No universal privacy/transport claim is made.
Post-execution operator checks reported clean source at the correction commit,
unchanged corrected artifact, private0700 directories/0600 single-link files,
NO_PE5_CRONTAB_MATCH and NO_RELEVANT_PROCESS_MATCH.
Repository-derived checks separately reproduced the source SHA/size, relationship ID,
output-sidecar SHA/size and timing bound; full output bytes were not independently received.
All required committed Windows suites passed before closure; native fault/crash evidence
and PE-5.8 natural-cycle requirements are not waived. Codex accessed no production system.
See [implementation evidence](PE5_CONFIGURED_ASSOCIATION_IMPLEMENTATION.md).
Separate authorization is required for PE-5.7. Do not activate or implement it here.

## Historical PE-5.7 final acceptance and closure

Classification: HISTORICAL_INTENTIONALLY_PRESERVED. Phase 7A ACTIVE; PE-5 IN_PROGRESS.
PE5_6_STATUS=COMPLETE/PASS; PE5_7_STATUS=COMPLETE/PASS.
RECURRING_EXECUTION_ACTIVE=TRUE; PE5_8_STARTED=FALSE.
Current next checkpoint: PE-5.8 - Operational Evidence and Independent Production Acceptance.
Separate authorization is required for PE-5.8. No PE-5.8 work is performed here.

OPERATOR_SUPPLIED evidence reports one separately authorized jazofv1 scheduler
activation: PASS_PE5_7_SCHEDULER_ACTIVATION. The accepted entry is exactly:
2,17,32,47 * * * * /usr/bin/python3 /home/jazofv1/hioc/pi4/bin/hioc-compose-service-associations.py
Marker: # HIOC_PE5_SERVICE_ASSOCIATIONS. Marker count1, entry count1,
unexpected PE-5 entry count0. Before crontab SHA256:
8f900f4679aa861b02e781a61927683db5900ddfe159d78c3831a1595ae7fe71.
After/install/read-only-verification SHA256:
3f56b904fc1dd40ccbfa3fdd61cb910c4d215e9ac28a9bf2dcdf3721c73b62a9.
Full crontab bytes were not independently received; these hashes and exact
post-install-byte verification are operator observations, not repository-derived hashes.
Existing jobs were reported preserved, including the governed PE-4 5/35 entry.

Activation did not manually execute the composer, execute the installer, or access MQTT.
The command uses the existing internal shared nonblocking lock; no execution-model,
runtime implementation, persistence, public inventory or authority change is made here.
The disabled deployment template remains byte-identical and commented; activation
changed the operator's crontab, not that source artifact.

Pre-activation PI3 source HEAD/origin were reported as
4990c62afbce22a804229f3cb8329986741067a6 with empty porcelain status.
No synchronization to PE-5.6 closure commit 21ca5f676bb96d376b3a6f098decfecfe3c6ea49
is inferred. Immutable Git comparison establishes unchanged runtime payload between
those commits; reported composer and disabled-template hashes match accepted bytes.

Separate post-activation read-only verification reported the same crontab hash,
one marker, one accepted entry and no unexpected PE-5 entry.
NO_RELEVANT_PROCESS_MATCH records only that instant. It does not prove no natural
scheduled cycle has ever occurred. Natural-cycle evidence is NOT ESTABLISHED.
No current generated-output freshness, recurring operational acceptance or naturally
observed overlap/missed-cycle/staleness/failure behavior is claimed.
PE-5.8 retains its natural-cycle and independent production acceptance requirements.
PE-5.6 first-failure, corrected-deployment and bounded-execution evidence remains historical.
Codex performed repository work only; no PI3/PI5/production access or mutation occurred.
See [implementation evidence](PE5_CONFIGURED_ASSOCIATION_IMPLEMENTATION.md) and the
existing governance record's scheduler_activation evidence.

## Historical PE-5.8 final acceptance and closure

Classification: HISTORICAL_INTENTIONALLY_PRESERVED. Phase 7A ACTIVE; PE-5 IN_PROGRESS.
PE5_6_STATUS=COMPLETE/PASS; PE5_7_STATUS=COMPLETE/PASS; PE5_8_STATUS=COMPLETE/PASS.
RECURRING_EXECUTION_ACTIVE=TRUE; PE5_9_STARTED=FALSE.
Current next checkpoint: PE-5.9 - Final PE-5 Closure and PE-6 Handoff.
Separate authorization is required for PE-5.9. It has not started; PE-5 is not yet closed.

OPERATOR_SUPPLIED read-only observations establish the required minimum of three
consecutive natural successful scheduler windows (:17, :32, :47 on 2026-10-14).
No manual producer execution occurred during PE-5.8; PE-5.6's bounded manual run
is historical and is not counted. PE-5.7 activation remains historical accepted evidence.
Cycle1 evaluated_at=2026-10-14T20:17:02.619461Z;
output SHA256 a5bea06825a63b1cd29ac705defe1066cc1f97ac678648d5fd97d9e322ebfe90;
CONFIRMED transaction dur_104bbbd8cb45467b8a53cc7d88dc497a.
Cycle2 evaluated_at=2026-10-14T20:32:01.823448Z;
output SHA256 c28f22d1272031a6586ee1673719c8b1061e06a2c120237df2140e8007082a7a;
CONFIRMED transaction dur_f70cd9091d5b4536929b329deac70e22.
Cycle3 evaluated_at=2026-10-14T20:47:02.451624Z;
output SHA256 aff03e297ae81bc9a9deff52884d2779b6138eb4b2f8592fe05f78272aa98120;
CONFIRMED transaction dur_e7a270926be543808b7711c5885778d7.
Second/third sidecar confirmed SHA equals its corresponding observed output SHA;
candidate=None. First CONFIRMED state/transaction was supplied, but a separate
confirmed_sha256 field was not supplied and is not fabricated.
Source revision1 and SHA256
961b72e8918606caeac565a8d472d03c4784d9a3b43eae6deb4085865330d295
remained unchanged. Third source sidecar also confirms that SHA/revision.
The accepted scheduler SHA256 remained
3f56b904fc1dd40ccbfa3fdd61cb910c4d215e9ac28a9bf2dcdf3721c73b62a9,
with one marker and one entry; cadence 2,17,32,47 * * * * and command unchanged.

Second/third outputs report schema2.0 VALID, configured VALID/revision1 with
one candidate and zero rejections; local eight associations and zero rejections.
LOCAL_STATE=None is a reported lookup: the closed local envelope has no state
field. Local schema1.0 is embedded unchanged in combined schema2.0.
Third valid_until=2026-10-14T21:05:02.000000Z is within the accepted upper bound;
its earlier deadline is consistent with the inventory expiry cap. Exact third
inventory.updated was not supplied and is not inferred.

Overlap, missed-cycle/no-catch-up, expiry, failure, restart/corruption and durability
semantics are supported by committed contract/static implementation and passing
synthetic Windows fixtures, as PE-5.2 explicitly permits. They are NOT claimed as
naturally observed faults or native PI3 crash tests. No artificial production
fault, manual execution or production mutation was performed for this acceptance.
Full production envelopes/crontab bytes were not independently received; supplied
production SHA values are operator observations, not independently recomputed hashes.
Current freshness beyond the supplied observation times is not asserted.
The earlier two-cycle STOP is preserved as process history; the third observation
resolved it without waiving any requirement. Existing PE-5.6/7 history remains preserved.
See [implementation evidence](PE5_CONFIGURED_ASSOCIATION_IMPLEMENTATION.md) and
operational_acceptance in the existing governance record for exact receipts,
evidence limitations and repository validation. No runtime or authority model changes.
Codex accessed no PI3, PI5 or production. PE-5.9 requires separate authorization.

## Historical PE-5.9 final closure and private PE-6 handoff

Classification: HISTORICAL_INTENTIONALLY_PRESERVED. Phase 7A ACTIVE; PE5_STATUS=COMPLETE.
PE5_9_STATUS=COMPLETE/PASS; PE5_8_STATUS=COMPLETE/PASS.
NEXT_CHECKPOINT=PE-6 - Classification & Metadata Quality; PE6_STARTED=FALSE.
Separate authorization is required for PE-6. PE-6 implementation is NOT authorized.

All 37 original PE-5 requirements and all 14 Definition of Done conditions pass;
all 11 roadmap UNKNOWN decisions have evidence-backed resolutions. The original
roadmap and 46 implementation checklist items remain immutable authority.
The current coverage/evidence ledger and complete private handoff are in
[PE-5 implementation evidence](PE5_CONFIGURED_ASSOCIATION_IMPLEMENTATION.md#current-pe-59-final-closure-and-private-pe-6-handoff)
and final_closure in the existing implementation governance record.
PE-5.6/7/8 accepted observations remain OPERATOR_SUPPLIED. Preserve
OPERATOR_OBSERVATIONS_ONLY; FULL_PRODUCTION_BYTES_NOT_RECEIVED;
NO_NATURAL_FAULT_OR_NATIVE_CRASH_CLAIM; NO_CURRENT_FRESHNESS_CLAIM.
First-cycle fields not separately supplied remain UNKNOWN; none is a completion
waiver or new production observation. No runtime, scheduler, public interface,
MQTT or production change occurs here. PE-6 may later consume only validated,
confirmed, unexpired private relationship evidence under the unchanged contract.
Publication remains gated by exact commit, push and independent GitHub verification.

### Individual PE-5 Definition of Done acceptance

1. **PASS — Accepted local branch preserved; no repeated PE-5.1 first execution**. Unchanged local resolver/caller and policy2100; accepted first execution retained, never repeated.

2. **PASS — Declared mapping source/producer/identifier/time/expiry authority established**. Corrected PE-5.2 contract plus 46 PE-5.3 implementation checklist items; source installer and explicit revision authority.

3. **PASS — Local and mapping relationships stable/deterministic/bounded with source/rule provenance**. Local semantic IDs and configured mqra_ semantic domain; deterministic source/rule provenance fixtures.

4. **PASS — Ambiguity/missing endpoints/duplicates/conflicts handled by accepted contract**. Closed source/input schemas, duplicate/conflict/device/service/expiry fixtures; no fabricated missing-input success.

5. **PASS — No transport-based identity/canonical-IP/observation/liveness/health authority**. Protected 226 artifacts and no runtime changes; relationship-only source/rule provenance.

6. **PASS — No secrets/topic leakage/private raw exposure/public or publish-subscribe compatibility change**. Closed no-secret/topic schemas, bounded prior operator search, static no-network mutation tests; public compatibility unchanged.

7. **PASS — Private-storage/current-history/retention/LKG/restart/corruption disposition approved and implemented/validated if required**. PE-5.2 atomic correction; PE-5.6 accepted corrected initialization; PENDING/CONFIRMED recovery/corruption synthetic fault fixtures.

8. **PASS — Execution/trigger/cadence/integration/locking/missed/failure disposition approved; required activation and natural cycles accepted**. PE-5.2 900-second schedule, flock/no-catch-up; PE-5.7 accepted cron and PE-5.8 three consecutive natural windows.

9. **PASS — Governed source sync, exact deployment, bounded validation and independent acceptance complete**. 4990c62 Master Plan records accepted disabled PE-5.5 payload/source; PE-5.6 corrected one-artifact deployment and bounded acceptance; PE-5.7/8 immutable independent closures.

10. **PASS — Private file/API/schema/version/freshness/conflict handoff sufficient for PE-6, without implementing PE-6**. Complete private handoff below; exact schema/semantic/confirmation/time/input identity gates; no PE-6 implementation.

11. **PASS — Operational docs answer what/why/how/source/freshness/failure/rollback; Master Plan synchronized**. Seventeen existing affected paths synchronized; operational what/why/how/inputs/failures/recovery and canonical changelog updated.

12. **PASS — Privacy-safe durable Evidence Reports/exact commit identities; source/runtime separation and clean synchronized Git**. Immutable predecessor commit references; accepted source/runtime distinction; final publication acceptance requires exact commit/push/independent GitHub and clean main=origin/main.

13. **PASS — Every original requirement COMPLETE or explicit authorized outside-phase/not-required disposition; no unknown completion requirement**. Thirty-seven COMPLETE evidence rows; all eleven UNKNOWN decisions resolved, original assignments and deferrals preserved.

14. **PASS — Only after all gates PE5_STATUS=COMPLETE; PE-6 then becomes next passive-enrichment checkpoint under separate authorization**. Only final accepted PE-5.9 closure marks PE-5 COMPLETE; PE-6 next NOT_STARTED with separate authorization.

## Historical accepted PE-6.0 contract design and execution roadmap

Classification: HISTORICAL_INTENTIONALLY_PRESERVED accepted PE-6.0 snapshot. PE5_STATUS=COMPLETE; PE6_STATUS=DESIGN_COMPLETE_RUNTIME_NOT_IMPLEMENTED.
PE6_0_STATUS=COMPLETE_CONTRACT_DESIGN; PE6_RUNTIME_IMPLEMENTED=FALSE.
NEXT_CHECKPOINT=PE-6.1 - Private classification implementation and comprehensive repository validation.
Separate authorization is required for PE-6.1, including adoption or revision of the proposed design.
This checkpoint authorizes no runtime implementation, production operation or PE-7 work.

The [PE-6 contract design](PE6_CLASSIFICATION_CONTRACT_DESIGN.md) inventories actual
capabilities and preserves the complete original authorization, twenty evidence-backed
technical decisions, exact private schema proposal and six-checkpoint roadmap.
Proposed role suggestions and metadata-quality summaries remain private, deterministic
and separate from operator-owned Asset data and public operational role/health.
Asset schema1.0 and the accepted PE-5.9 governance/runtime remain unchanged.
No PE-6 persistence, cron, inventory hook or public projection is selected.
Actual production inputs/locks/runtime state remain UNKNOWN; only later bounded operator
gates may establish them. All previous OPERATOR_SUPPLIED evidence limitations remain.

## Current PE-6.1 repository implementation and validation

Classification: CURRENT. Phase 7A ACTIVE; PE-4 PASS/CLOSED; Public Projection PASS/CLOSED.
PE5_STATUS=COMPLETE; PE6_STATUS=IN_PROGRESS_REPOSITORY_IMPLEMENTED.
PE6_0_STATUS=COMPLETE/PASS; PE6_1_STATUS=COMPLETE/PASS.
PE6_REPOSITORY_IMPLEMENTED=TRUE; PE6_PRODUCTION_DEPLOYED=FALSE.
NEXT_CHECKPOINT=PE-6.2 - PI3 Release-Source Synchronization.
Separate authorization is required for PE-6.2. PE6_2_STARTED=FALSE.

The explicitly adopted [PE-6.0 design](PE6_CLASSIFICATION_CONTRACT_DESIGN.md) is
preserved byte-for-byte at ea4a93fba1615af1d6641c7f0683b8e912c03d72.
The [PE-6.1 implementation evidence](PE6_CLASSIFICATION_IMPLEMENTATION.md) records
the private stateless resolver, explicit offline caller, exact source/provenance
validation, unchanged Asset schema1.0 and complete PE-5 private handoff.
Suggestions never confirm operator intent, alter identity/canonical IP, or affect
public inventory, MQTT, health, liveness, monitoring or incidents.
No persistent result store, last-known-good result, scheduler, inventory hook,
producer execution, deployment, PI3/PI5/HA/MQTT/credential or production access
is authorized or performed. Operational inputs, configured locks and production
facts remain UNKNOWN until separately authorized operator checkpoints.
All PE-4/PE-5 production observations retain OPERATOR_SUPPLIED limitations.
The closure text is an unpublished candidate until all required validation and
independent acceptance pass; actual final totals are recorded in the accepted
commit Evidence Report. Failed validation prevents publication.
