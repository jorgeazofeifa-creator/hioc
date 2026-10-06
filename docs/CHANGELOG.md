# HIOC Changelog

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

Separately authorized PI3 production execution PASS; independent read-only
evidence review PASS, as supplied for this closure. Client and operator RCs were
0; source precheck/runtime precheck/source postcheck passed and the execution
source remained clean and synchronized at preparation commit
03f43e5231e59ec396665bb8bda9faf2447c5276. Successor blob
85842a81c57187c9e119d1065fce433e5b067e1f; SHA-256
aa0e58ed6c7bb4586625836cc71ad0cab9270e6b11a6a5db66497115b001decf.
Active target: environments/cpython311-websockets16.1.1-lock-v1.

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

Candidate blob 85842a81c57187c9e119d1065fce433e5b067e1f; SHA-256
aa0e58ed6c7bb4586625836cc71ad0cab9270e6b11a6a5db66497115b001decf.

[Canonical preparation record](../governance/pe4/pe4-0b2a-successor-preparation.json).

Validation: 160 focused regressions PASS; full suite 1253 run, 1206 PASS,
47 platform skips. In-memory compilation of 138 tracked Python files, static
privacy/output checks, Git Bash release validation and future block syntax/
Python compilation PASS. Preparation JSON is canonical and source-bound.
Existing G-test ResourceWarnings and Git line-ending warnings are informational.

D/E/F/G remain PASS/CLOSED, E handoff ACCEPTED; successor CORRECTED /
REPOSITORY_ONLY / NOT DEPLOYED. 2a is NOT STARTED / PREPARED FOR SEPARATE
AUTHORIZATION; 2b NOT STARTED; PE-4 NOT COMPLETE; Phase 7A ACTIVE; rollback
NOT PERFORMED. Historical F/G identity/runtime and accepted handoff/lock are
unchanged. No authenticated execution, PI3/PI5/HA access, F/G rerun or rollback
occurred. Package installation, another environment and pointer mutation are
excluded. Stop after the separately authorized proof; chain no later action.

## PE-4.0B.2a consolidated client boundary correction - 2026-10-05

Corrected all five audited boundaries in one repository-only batch: absolute REST
deadline, duplicate-safe JSON, decoder recursion normalization, receive-coroutine
ordering, and bounded network interruption handling (RC 130). Previous parser,
secure-getpass, network-budget and authentication-send corrections remain intact.

Validation: 54 client tests PASS; 160 focused client/privacy/historical/runtime
regressions PASS. Full suite: 1253 run, 1206 PASS, 47 platform skips. All 138 tracked
Python files compile in memory; static privacy/output and Git Bash release checks
PASS. Initial shell-alias platform failures were resolved by excluding WindowsApps
bash from the test process PATH. Git diff checks have line-ending warnings only.
The real HTTP parser over controlled transports reproduces baseline overruns and
proves corrected slow writes/headers/bodies stop within the shared 20-second budget.

New blob: 85842a81c57187c9e119d1065fce433e5b067e1f; SHA-256:
aa0e58ed6c7bb4586625836cc71ad0cab9270e6b11a6a5db66497115b001decf.
[Canonical correction and superseded identity](PE4_HOME_ASSISTANT_ACCESS_PRIVACY_CONTRACT.md#pe-40b2a-consolidated-client-boundary-correction---2026-10-05).
Historical F/G identity/runtime are unchanged; no authenticated execution occurred.
2a remains NOT STARTED / NOT PREPARED. Preparation review must be repeated separately.

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

Validation: client/privacy 49 PASS, including six send/cleanup/deadline tests;
98 historical F/G/runtime/API regressions PASS. Full suite: 1240 run,
1193 PASS, 47 platform skips. In-memory compilation of 138 Python files,
static output/privacy and release validation, complete diff and seven-file scope
PASS. Diff checks report Git line-ending warnings only. The old flow fails the
finite stalled-send check; corrected tests need no external client cancellation.

Added stalled-send, close-unblocks-send, no-orphan, stalled-close transport-abort,
remaining-deadline, expired-before-send, exception and run-level privacy tests.
Historical F/G identity/runtime are unchanged; no authenticated operation occurred.
2a remains NOT STARTED / NOT PREPARED; repeat preparation separately.

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

Validation: client/privacy 43 PASS, including fallback and filter-scope tests;
98 historical F/G/runtime/API regressions PASS. Full suite: 1234 run,
1187 PASS, 47 platform skips. In-memory compilation of 138 Python files,
static privacy/output and release checks, complete diff and seven-file scope
PASS. Diff checks have Git line-ending warnings only.

Added real fallback-reader, warning continuation, filter restoration and
run-level no-clock/no-network regressions; normal prompt and existing failures
remain covered. Historical F/G runtime is unchanged; no authenticated operation
occurred. 2a remains NOT STARTED / NOT PREPARED; preparation must be repeated.

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

Validation: 39 client/privacy tests PASS, including five timing regressions;
98 historical F/G/runtime/API regressions PASS. Full suite: 1230 run,
1183 PASS, 47 platform skips. In-memory compilation of 138 Python files,
static output/privacy and release checks, complete diff and exact seven-file
scope PASS; diff checks have only Git line-ending warnings.

Added mocked timing regressions for slow prompts, long local checks, shared
deadlines, credential failure and network elapsed-time exhaustion. Historical
F/G identity/runtime are unchanged; no F/G rerun, deployment or rollback.
2a remains NOT STARTED / NOT PREPARED; separate preparation review is next.

## Repository successor authentication-frame correction — 2026-10-05

The canonical tools/hioc-pe4-ha-auth-capability.py successor source now corrects
the exact-one-key authentication parser defect. Bounded JSON object parsing
requires a string type; phase validators accept only auth_required/auth_ok
with exactly type + string ha_version, or auth_invalid with exactly type +
string message. Ancillary values are validated and discarded. auth_invalid
maps to AUTHENTICATION_FAILED / AUTHENTICATION; other schemas fail closed.
The exchange sends one auth frame and no command after auth_ok. REST, network,
credential acquisition, terminal markers and the 2b prohibition are unchanged.

Validation: client/privacy 34 PASS; historical F/G/runtime/API regressions
98 PASS; full repository suite 1225 run, 1178 PASS, 47 platform skips.
In-memory compilation of 138 Python files and the generated G child PASSed;
static release/output/privacy checks, exact seven-file scope and diff checks
PASSed. Tests used synthetic credentials and mocked HA transports; no live
HA, PI3/PI5 access, token acquisition, deployment or persistent proof occurred.

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

## Action G implementation

Added the controlled credential-free G preflight and dedicated result contract.
Production execution remains NOT STARTED.

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

Record production Action E completion and its documentation/governance closure; the earlier native validation remains a prerequisite event.

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

Closed the separately authorized PI3 source synchronization and native non-lifecycle validation for the controlled-startup implementation. This documentation-only closure changes no source, tests, lock, runtime implementation, or lifecycle state.

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

Implemented controlled Action E startup, verified package loading, corrected redirect refusal, and behavioral synthetic immutability tests. This is repository engineering, not production lifecycle execution.

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

Closed the operator-reported PI3 synchronization and read-only D-to-E
compatibility validation after publication of the producer/current correction.
This entry records compatibility validation, not executed dependency validation.

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

- Corrected Action E's producer/current governance binding. E retains mandatory
  `--governance-commit` for current source and adds mandatory
  `--action-d-governance-commit` for accepted D provenance, with no fallback.
  A separate compatibility module proves actual commit objects without replacement
  substitution, producer ancestry and exact D/common/lock blob equality, plus
  current checkout governance and normalized source identity. Strict D eligibility,
  E dependency/capability checks and E success JSON remain unchanged. Local Windows
  compatibility tests passed (36 run, zero skips); related PE-4 regressions passed
  (164 run, 11 POSIX-only skips). D/common/lock and F/G source remain unchanged.
  The accepted D handoff remains immutable. Action E has not executed and remains
  **NOT STARTED**; F/G remain unauthorized. No PI3/PI5 access or lifecycle execution
  occurred during implementation. The later separately authorized PI3
  synchronization/read-only compatibility validation PASSed as recorded above.

- Closed the operator-reported successful third actual Action D execution:
  process RC 0, construction confirmed/retained, evidence and eligibility CONFIRMED,
  cleanup COMPLETE and independent review PASS. Earlier two failures remain history;
  the intervening pre-execution stop was not an execution. Replacement B staging
  and source were unchanged, hierarchy remained compliant, and no new snapshot
  entries remained. Action C and D-PREP were not rerun; Action E remains NOT STARTED
  and unauthorized. No later action, combined suite, or rollback occurred.

- Closed one operator-executed fresh replacement Action B transaction: PASS,
  terminal evidence CONFIRMED, wrapper RC 0 and independent input review PASS.
  Accepted staging is `/tmp/hioc-pe4-artifact-transfer-l3t4crcg`; historical
  unavailable staging remains audit history. Action C and D-PREP were not rerun;
  Action D remains failed twice with no third execution and requires separate
  preparation/authorization. No later action or rollback occurred.

- Reconciled operator-observed loss of historical B staging and second D failure
  evidence, with cause UNKNOWN. Historical PASS results and D-PREP closure remain
  valid; the recovery wrapper did not launch a third D execution. Both read-only
  readiness checkpoints PASS; replacement B remains unexecuted and unauthorized.

- Closed operator-reported D-PREP production execution: all three absent runtime
  hierarchy components were created and confirmed compliant, private evidence
  was CONFIRMED, process RC was 0, and post-validation passed. Rollback was not
  recommended; no later action executed. Action D remains failed twice and
  pending a separately authorized retry.

- Closed operator-reported PI3 native D-PREP portability revalidation: 115/115
  PASS, zero skips/failures/errors, and all seven POSIX-specific tests PASS.
  Pre/post source identity remained `c5181a0d65da294e5db2dbd6795f20889b972a22`;
  Action D retained its frozen SHA-256. D-PREP production execution and Action D
  retry did not occur; the combined suite did not execute on PI3.

- Recorded the PI3 native D-PREP test-harness portability failure (115 tests,
  18 failures / 1 error): process-global OS mocking defects were exposed, while
  all seven real POSIX-only tests passed. A private HIOC OS facade now isolates
  synthetic behavior, and temp-root comparison uses host-native pathlib semantics.
  Corrected Windows D-PREP (115 tests) and combined lifecycle (126 tests) suites
  pass with the same seven skips. Native PI3 revalidation remains pending;
  D-PREP has not executed and Action D has not been retried.

- Added the separately governed PE-4 D-PREP runtime-hierarchy checkpoint. It
  prepares or validates only the descriptor-bound `runtime/pe4/environments`
  hierarchy, retains valid partial state, and cannot chain into Action D.

- Refreshed PE-4 Action B's exact Windows System32 OpenSSH trust anchors after
  valid Microsoft-signed `OpenSSH_9.5p2` servicing drift. The reviewed new
  `ssh.exe` and `ssh-keygen.exe` hashes replace, rather than supplement, stale
  pins; servicing causality remains unproven. No transport was executed.

- Corrected PE-4 Action B's Windows SSH ACL preflight. Shared `.ssh`, protected
  `known_hosts`, and dedicated key files now use independent fail-closed
  ownership and ACE policies derived from the reviewed Windows layouts. No live
  ACL or SSH material was changed; Action B remains blocked and unexecuted.

- Corrected PE-4 Action B so every independent SSH command proves the exact
  staging device/inode/UID/mode identity before descriptor-relative child
  access; duplicate numeric host records and unsafe SSH-material ACLs now fail
  closed. Action B remains unexecuted pending publication and PI3 preflight.

- Replaced Action B's predictable SCP partial destinations with bounded SSH
  streaming into directory-fd-relative `O_EXCL|O_NOFOLLOW` sinks. Runtime
  preflight now pins the Windows operator/profile, `ssh.exe`, reviewed key pair
  and fingerprint, and numeric PI3 host trust. Evidence terminal state now
  distinguishes not published, confirmed, and uncertain while persistent
  result-last evidence records its pre-confirmation state. Action B remains
  blocked and unexecuted.

- Corrected PE-4 Action B remote publication before execution. Wheel, lock, and
  result evidence now use `renameat2(RENAME_NOREPLACE)` rather than ordinary
  `mv`; every raced destination object is a collision. Evidence preparation is
  exclusive and non-following. Normal and uncertain-error success both require
  exact durable final confirmation plus proven consumption of the
  invocation-owned source. A failed result attempt cannot publish a second,
  contradictory result. Action B remains blocked and unexecuted.

- Corrected the PE-4 Windows SSH identity public-record parser after the first
  governed production attempt failed safely. The pinned Windows OpenSSH
  generator emits its single public-key record with a CRLF terminator; the
  parser now accepts exactly one LF or CRLF terminator while continuing to
  reject embedded, bare-CR, multiline, malformed, or oversized records. Pair
  validation consumes the pinned generator's real derived record and comment
  instead of appending a synthetic fourth field.

- Corrected PE-4 identity evidence no-replace reconciliation. An exact raced
  `result.json` is no longer accepted while `.result.tmp` remains in any form;
  post-error success requires exact final confirmation and proven non-following
  temporary-source absence. Normal success enforces the same invariant, and no
  collision triggers overwrite or a second result publication.

- Corrected the PE-4 Windows SSH identity collision and path contracts before
  execution. Non-following entry inspection rejects files, directories,
  dangling links, junctions, mount points, and all other reparse entries;
  Windows no-replace publication closes the remaining race for keys and
  evidence. Provisioning and Action B now have regression-locked shared
  `.ssh/id_ed25519` paths. Neither operation has executed.

- Corrected the PE-4 Windows SSH identity provisioning evidence lifecycle.
  Invocation children remain known across ACL initialization failure, cleanup
  reaches its final state before failure evidence, and one prepare/publish/
  confirm attempt reconciles rename uncertainty through exact content and DACL
  readback. Ambiguous results remain unaccepted and are not overwritten.
  Provisioning and Action B remain unexecuted.

- Added the repository-governed Windows prerequisite for Action B's dedicated
  Ed25519 identity. It fixes Known Folder paths, system `ssh-keygen.exe`, empty
  passphrase and comment, rejects collisions/reparse traversal, applies and
  rereads current-operator-only DACLs, validates the pair and sanitized
  fingerprint, publishes public-first/private-last, and stops before PI3 or
  Action B. No production identity has been generated; Action B remains blocked.

- Corrected the remaining PE-4 Action B OpenSSH configuration-isolation and
  evidence-publication defects. Action B now ignores user/system SSH config,
  pins numeric PI3 and port 22, disables proxies/canonicalization/agents, uses
  fixed non-reparse known-hosts and Ed25519 identity files, and reconciles any
  post-rename evidence failure through exact durable read-back confirmation.
  Action B remains blocked and unexecuted pending publication and preparation.

- Accepted PE-4 Action A production PASS and corrected Action B before any
  transfer. Action B now derives the exact durable cache, validates Windows
  reparse/DACL boundaries, uses system OpenSSH with strict noninteractive
  bounded options, separately transfers and validates wheel and lock, and
  publishes result-last partial-state evidence. Action B remains unexecuted.

- Corrected the PE-4 Action A Windows ACL implementation after its first
  production attempt stopped before network access at `WORKSTATION_ACL`. The
  Python-launched Windows PowerShell process could not autoload the
  `Microsoft.PowerShell.Security` cmdlets, and trailing `-Command` values were
  not a governed `$args` transport. ACL hardening now passes the target through
  a child-only environment, modifies the existing .NET security descriptor,
  removes inherited and explicit ACEs, installs one SID-based FullControl rule,
  persists through `DirectoryInfo`/`FileInfo`, and revalidates every invariant.
  Action A remains attempted but not complete; no wheel was downloaded.

- Corrected PE-4.0B.2a execution architecture: the client is an HIOC consumer
  on PI3 while PI5 HA remains the exact remote API source. Separated execution
  and endpoint identity in code/tests, retained endpoint/privacy/network bounds,
  preserved the failed PI5-local precheck as history, and designed separate
  credential-free PI3 runtime and route proofs. Nothing was installed,
  deployed, connected, or executed; PE-4.0B.2a remains not started.

- Corrected the PE-4.0B.2a `websockets` redirect-suppression defect by binding
  the handshake to one pre-connected governed-target socket. The dependency
  refuses redirects on this path before another endpoint is contacted. Added
  compatibility and redirect-path tests; runtime preparation remains blocked
  pending publication, and PE-4.0B.2a remains not started.

- Corrected the PE-4.0B.2a websocket-client receive-bound defect by removing
  that dependency path and requiring compatible `websockets` support with
  `max_size=65536` at connection creation. Added dependency-level oversized
  failure coverage and preserved fail-before-credential behavior. This is a
  repository correction only; 2a remains not started.

- Implemented the repository-controlled PE-4.0B.2a client at
  `tools/hioc-pe4-ha-auth-capability.py` with offline tests for exact target,
  dependency-before-secret, terminal-only credential handling, REST then
  WebSocket authentication, strict bounds, proxy/redirect refusal, closed
  privacy output, and fail-closed sequencing. It has not been committed,
  deployed, or executed against PI5; PE-4.0B.2a and 2b remain not started.

- Froze the official PE-4.0B.2a interface contract to authenticated `GET /api/`
  followed by `/api/websocket` authentication only. Recorded fixed response and
  handshake schemas, bearer-token handling, exact bounds and terminal markers,
  REST registry non-support, version-pinned frontend/source registry findings,
  and the repository-controlled-client requirement. No client, credential,
  network request, registry discovery, evidence, deployment, or production
  change was created; 2a and 2b remain not started.

- Recorded PE-4.0B.1 production preflight COMPLETE / PASS. The credential-free
  check proved PI5's HA Terminal add-on context, HA OS/Core/Supervisor
  classification, exact no-proxy HTTP endpoint, available secure prompt and
  client tooling, and absence of a dedicated WebSocket client, without registry,
  state, internal-file, database, or production mutation. The earlier
  `UNSUPPORTED_HA_DEPLOYMENT` parser-contract failure remains historical.
  PE-4.0B.2 is not started and is split into separately authorized 2a
  authenticated capability proof and 2b sanitized registry/schema discovery;
  PE-4.0C, association implementation, and deployment remain not started.

- Defined the PE-4.0A Home Assistant access and privacy contract before live
  discovery. It classifies supported API access as candidate-only pending PI5
  deployment/interface proof; prohibits internal files/databases, states,
  mutations, secrets, and household identifiers; freezes HIOC/Asset authority;
  and requires bounded, private, result-last count/category evidence. PE-4.0B
  and runtime implementation remain not started.

- Recorded PE-3 completion. Action 10 completed administratively with disposition
  `NOOP_ALREADY_ABSENT`; Actions 1–10 and PE-3 are complete. No PI3 or PI5
  action, staging recreation or deletion, production mutation, rollback, or
  Action 10 Evidence Report was required. Action 9 PASS and its Evidence Report
  remain the final PE-3 production validation and evidence. Transport staging
  remains absent, retransmission remains unnecessary, and all future-roadmap
  checkpoints remain preserved.

- Corrected PE-3 Action 10 governance as **CASE C — ADMINISTRATIVE NO-OP
  CLOSURE**. Historical Action 10 only deleted the two-file transport directory
  and rewrote an obsolete combined evidence report. Transport staging is already
  absent and non-authoritative after Action 6 immutable publication and Action 7
  activation; Actions 8 and 9 do not consume it. No PI3 verification, deletion,
  reconstruction, retransmission, or Action 8/9 evidence input is required.
  `NOOP_ALREADY_ABSENT` is the administrative disposition. Action 10 remains not
  complete pending validation, commit, push, and clean-tree verification of this
  correction, followed by a separate repository-only completion record.

- Recorded the governed PE-3 Action 9 production PASS. The read-only validation
  published its private Evidence Report at
  `/tmp/hioc-pe3-action9-Bb6vGrmm`, returned `ACTION9=COMPLETE` and
  `ROLLBACK_RECOMMENDED=FALSE`, and caused no production mutation or rollback.
  Its valid `12.467231`-second and `146744`-KiB total-peak-child-RSS
  observations remain `UNVALIDATED`/`INSUFFICIENT_BASELINE`; both historical
  targets were exceeded but were not production enforced. Actions 1–9 are
  complete, Action 10 remains not started/not prepared, Action 8 evidence remains
  preserved at `/tmp/hioc-pe3-action8-eZxNGrKa`, transport staging remains
  absent, retransmission remains unnecessary, and all future checkpoints are
  preserved.

- Corrected PE-3 Action 9 performance validation after its first read-only
  production attempt isolated a performance-only failure. Result and protected
  schemas passed; measured elapsed time was `12.467231` seconds and total peak
  child RSS was `146744` KiB. The four-second and incremental-RSS 48-MiB design
  targets lack current PI3 production provenance and no longer hard-fail Action
  9. Independent result, performance-syntax, insufficient-baseline assessment,
  and protected-snapshot stages replace the collapsed diagnostic. The private
  Evidence Report records sanitized observations and historical comparisons.
  No Action 9 evidence directory or production mutation occurred; rollback is
  FALSE, Action 9 is attempted but incomplete, and Action 10 is not started.

- Replaced the unsafe historical PE-3 Action 9 inline procedure with a governed
  read-only validation tool. It strictly validates the operator-supplied Action
  8 PASS evidence, reuses its portable performance record, independently proves
  current production artifacts and protected state unchanged, and publishes a
  private result-last Evidence Report. It has no `/usr/bin/time`, generator,
  strict interactive shell, staging, rollback, or Action 10 behavior. Action 9
  remains not started pending commit, push, synchronization, and authorization.

- Recorded the governed PE-3 Action 8 production PASS at commit
  `fa344828161e892523faa3da5d4cdf07d2e8e792`, including preserved private
  evidence `/tmp/hioc-pe3-action8-eZxNGrKa`, current source-refresh and
  corrected-validator deployment prerequisites, `ROLLBACK_RECOMMENDED=FALSE`,
  no rollback, absent/unnecessary transport staging, and no retransmission.
  Action 8 is complete; Action 9 remains not started pending a separate governed
  checkpoint after this completion record is committed and pushed.

- Corrected the active Action 8 bootstrap status from the stale historical
  `NOT STARTED` state to `ATTEMPTED BUT NOT COMPLETE`. The active contract now
  preserves Action 9 as `NOT STARTED` and requires reviewed source refresh and
  corrected-validator deployment before another separately authorized attempt;
  dated historical checkpoint statements remain historical evidence.

- Added a governed validator-only Action 8 corrective deployment boundary. It
  independently freezes the reviewed validator identity, supports exact
  identical no-op, creates a private durable backup only for replacement,
  publishes atomically in the runtime target directory, and proves protected
  manufacturer/configuration/dataset/inventory state unchanged. It does not use
  the broad release upgrade or invoke engines, schedules, Action 8, or Action 9.

- Corrected the Action 8 validator permission-class mismatch exposed by the
  third governed attempt. Both generated private artifacts passed exact `0600`
  identity checks, but the validator later applied their private bitmask to the
  inventory input and returned `MANUFACTURER_PERMISSION_ERROR`. Manufacturer
  outputs remain exact `0600`; inventory retains its no-group/world-write rule.
  Action 8 remains incomplete, the rollback advisory remains true, and no
  rollback or production action occurred.

- Replaced Action 8's undeclared hard-coded `/usr/bin/time` launcher after PI3
  retained sanitized exit-127 evidence proving instrumentation blocked the
  governed generator before execution was confirmed. Governed Python now owns
  child launch, monotonic timing, child maximum-RSS measurement, and a bounded
  launch-status marker. No output changed and rollback remains unrecommended.

- Corrected the active PE-3 Action 8 bootstrap trust gate after preparation
  stopped before PI3 execution because it still froze the superseded wrapper
  blob. The independently reviewed Git-blob anchor now names the current
  diagnostic-retention wrapper; parameterized governance-commit validation and
  every source-only fail-closed boundary remain unchanged. The replacement
  bootstrap remains not prepared or executed.

- Corrected PE-3 Action 8 generator-failure diagnostic retention after production
  forensics proved the failed invocation retained only protected pre-state. The
  wrapper now publishes private sanitized performance followed by result-last
  `generation-failure.json`, records allowlisted root cause, exit status, output
  mutation, and rollback advice, and deletes raw stdout/stderr captures. Action 8
  remains incomplete, Action 9 remains not started, and the changed wrapper
  requires a new post-push bootstrap before another separately authorized run.

- Removed PE-3 Action 8's unverifiable historical evidence-directory input.
  The wrapper now creates one unique private invocation-owned
  `/tmp/hioc-pe3-action8-XXXXXXXX` directory after read-only preconditions pass,
  publishes sanitized performance then result-last aggregate evidence, and
  reports the exact path. No bootstrap, generation, production, or later action
  occurred; the changed script requires a new post-push bootstrap identity gate.

- Corrected the PE-3 Action 8 bootstrap's self-stale governance identity. The
  gate now accepts an explicitly approved literal full 40-hex post-push commit,
  validates it before target/network work, and retains exact remote, ancestry,
  fast-forward, synchronized HEAD, cleanliness, and frozen script-blob barriers.
  No bootstrap, generation, production, staging, or later action occurred.

- Governed the separate PE-3 Action 8 bootstrap as a source-only clean
  fast-forward and exact script Git/worktree identity gate. It stops before
  generation and never reads or changes runtime state, configuration, dataset,
  manufacturer artifacts, Action 8 evidence, or transport staging. The
  bootstrap is prepared but not executed; Action 8 remains not started.

- Corrected the PE-3 Action 8 transport-staging lifetime defect exposed by the
  pre-generation `TRANSPORT_STAGING_INVALID` stop. Action 8 now treats transfer
  staging as transient Action 6 input, validates the installed immutable pair and
  active configuration as authoritative, and neither reads, recreates,
  retransmits, nor cleans staging. The stopped attempt generated no manufacturer
  artifacts; rollback is not recommended and Action 9 remains not started.

- Replaced the unsafe PE-3 Action 8 inline generation block with a governed
  protected-generation wrapper. It verifies target/source/runtime, activated
  configuration, exact immutable dataset, inventory, output preconditions,
  installed dataset, protected state, generated sidecar/status, and private
  aggregate evidence; preserves the generator's existing lock and atomic-write
  contracts; and stops before Action 9. Action 7 is complete, Action 8 remains
  not started, and no production action occurred.

- Replaced the unsafe PE-3 Action 7 inline configuration block with a separately
  bootstrapped repository-controlled activation transaction. The corrected
  contract proves source/runtime and exact immutable dataset identity, validates
  privacy-safe record count, preserves unrelated configuration, creates a
  private durable backup when needed, publishes atomically, validates the
  selected runtime path, reports bounded rollback guidance, and stops before
  Action 8. Action 7 remains not started; no production action occurred.

- Added the future PE-10 Application, Integration & Service Assurance roadmap
  phase. It distinguishes infrastructure availability from functional service
  health; preserves PE-7 expected availability and the existing PE-8/PE-9 Asset,
  impact, dependency, topology, and propagation work; records Tuya/Smart Life
  stale-state and Google Cast use cases; and defines evidence-based, bounded,
  functionally validated recovery and operator-focused notification targets.
  No implementation or production behavior changed.

- Synchronized the authoritative PE-3 status after reviewed production evidence:
  Actions 1-5, 6-A, and 6-B are complete; Action 6 is complete; Action 7 is not
  started; no rollback is recommended; the deployed runtime and transport
  staging remain preserved. This checkpoint did not prepare or execute Action 7.

- Replaced the unsafe PE-3 Action 6 inline immutable-install block with a
  separately bootstrapped repository-controlled installer. The corrected
  contract freezes the exact preserved staging path, full source/staging/
  configuration barriers, privacy-safe validation, same-filesystem no-replace
  atomic publication, bounded cleanup/failures, complete PASS evidence, and an
  explicit Action 7 authorization barrier. No target or dataset action occurred.

- Added the missing PE-3 Action 5C bootstrap contract. Inline Action 5C-A now
  performs only clean target synchronization and exact Action 5C script
  identity before stopping; separately authorized Action 5C-B remains the
  read-only closure. No target access, synchronization, revalidation,
  deployment, rollback, manufacturer mutation, or Action 6 work occurred.

- Corrected PE-3 Action 5 manufacturer protection after the first Action 5B
  deployment passed code/runtime validation but a raw recursive fingerprint
  misclassified release-managed empty `0700` scaffolding as dataset mutation.
  Read-only forensics proved no manufacturer payload or configuration activation
  existed, so rollback is not recommended. Added semantic payload protection,
  explicit payload/scaffolding/configuration evidence, and a separately
  bootstrapped read-only Action 5C closure. Added the future PI3 + PI5 abrupt
  power-loss/cold-boot recovery checkpoint; Action 6 remains not started.
  Validation passed 25 focused Action 5 tests, 120 manufacturer tests, and all
  571 repository tests with 8 environment-dependent skips.

- Added an explicit PE-3 Action 5A bootstrap gate because PI3 may remain at the
  prior Action 4 commit that predates the Action 5 deployment script. Action 5A
  performs only a clean exact fast-forward and proves the deployment script's
  availability and Git/worktree identity before stopping. Action 5B requires
  separate authorization and remains the first production mutation.
  Validation passed 29 focused tests, 17 release/governance tests, 120
  manufacturer tests, and all 560 repository tests.

- Hardened PE-3 Production Action 5 before its first execution. Replaced the
  unsafe interactive strict-mode/`tee` block and unresolved governance commit
  placeholder with `tools/hioc-pe3-action5-deploy.sh`. The governed script
  verifies target/source/self/artifact identity, performs pre-deployment release
  validation, uses only the supported upgrade path, proves the new backup,
  validates runtime identities, preserves dataset/configuration state, emits
  bounded evidence and rollback guidance, and stops before Action 6.
  Validation passed 24 focused tests, 120 manufacturer tests, and all 555
  repository tests with 19 environment-dependent skips.

- Split PE-3 Action 4 into separately authorized 4A synchronization/script
  identity and 4B permission-normalization/validator boundaries. Action 4A now
  emits eight explicit PASS barriers and stops without staging access or script
  execution. Action 4B remains the unchanged repository script and alone may
  complete Action 4 after separate authorization. No production action occurred.

- Gated the PE-3 Action 4 resume on target release-source synchronization after
  PI3 was found at `653f887a643c877a8f611145c8b8e9f92a65b6cd`, before the resume
  script existed. The bounded prerequisite permits only a clean exact
  fast-forward, verifies script Git/worktree identity, and dispatches only after
  availability passes. Existing staging was untouched and Action 5 remains not
  started.

- Completed the PE-3 Action 4 resume contract after finding that the inline
  procedure rechecked only modes and hashes after normalization and did not
  explicitly enforce validator JSON privacy/count fields. The exact operation
  now lives in a repository-controlled Bash script with full pre/post identity
  barriers, bounded chmod targets, explicit sanitized evidence, failure-path
  terminal safety, and permanent dangerous-operator-pattern guidance. Action 4
  remains stopped; no PI, staging, deployment, or production action occurred.

- Corrected the PE-3 staged-artifact permission contract after synchronized
  Action 4 safely stopped on validator rejection of transport-created `0644`
  files. Action 4 now identity-gates normalization of only the exact database
  and manifest to frozen mode `0600`, then rechecks mode and hashes before the
  read-only validator. Existing staging and completed synchronization evidence
  are preserved; Action 5 and production remain untouched.

- Corrected the PE-3 Action 3/4 sequencing contradiction discovered on PI3.
  Action 3 now verifies staging only; Action 4 synchronizes the clean source,
  proves implementation/validator identity, rechecks staged identity, and runs
  the read-only validator before Action 5 can deploy. Function-scoped operator
  failures now preserve the interactive shell and emit sanitized codes. The
  already-passed staging evidence is retained; no production action occurred.

- Promoted Windows CPython 3.13.x to supported after the first trustworthy
  governed checkpoint PASS on 3.13.15: full suite 520 with 13 skips, policy 10,
  Action 1 governance 13, manufacturer 119, compilation PASS, and clean tree.
  Action 1 now resolves only the exact manager-owned 3.13 interpreter. The
  validation checkpoint is explicitly one-time and refuses after promotion.
  CPython 3.14.7 remains an unsupported diagnostic side effect pending separate
  disposition. No PE-3 or production action occurred.

- Removed `ProcessStartInfo` from all governed Python runtime execution after
  final operator isolation proved the exact managed interpreter passes directly
  both normally and with the checkpoint pycache prefix, but fails through that
  wrapper. The checkpoint now uses scoped PowerShell-native invocation with
  immediate exit-code capture, temporary redirected streams, bounded tails,
  restored error policy, and cleanup for every Python stage. Non-Python utility
  execution is unchanged; support remains pending.

- Corrected Windows CPython checkpoint execution after governed evidence proved
  direct `py -3.13` passed while `ProcessStartInfo` launching the resolved App
  Execution Alias exited 1 despite completed stream tasks. Runtime execution now
  resolves the exact managed 3.13 interpreter with `pymanager list --format=exe`
  and invokes it directly, excluding default/3.14 selection and automatic
  installation. Diagnostic output now separates successful diagnostic execution
  from failed equivalence. Support remains pending and no checkpoint or
  production action was executed.

- Added a repository-controlled Windows process-wrapper forensic diagnostic
  after the governed checkpoint continued to report `FULL_REGRESSION_FAILED`
  while direct CPython 3.13 runs passed 508 tests with 13 skips and exit code 0,
  including with the checkpoint pycache prefix. The diagnostic compares direct
  PowerShell and current `ProcessStartInfo` execution using identical launcher,
  argv, environment, working directory, and suite, emitting only sanitized
  process metadata. Portable Windows tests cover large/simultaneous streams,
  nonzero exits, argv fidelity, spaced executable paths, repetition, and
  cleanup. The checkpoint and support state are unchanged pending evidence.

- Corrected a false `FULL_REGRESSION_FAILED` classification after an immediate
  direct governed CPython 3.13 run passed 506 tests with 13 skips and exit code
  0. The checkpoint had used a parsed `Ran` count as an extra acceptance gate
  while bounded capture retained the stream head and could omit unittest's
  trailing summary. Test stages now accept only authoritative native exit zero,
  preserve stream tails for sanitized count reporting, and retain every real
  nonzero failure. Focused regression coverage reproduces summary truncation.
  Support remains pending with no validated patch; no checkpoint, PE-3, PI, or
  production action was executed.

- Corrected the network-probe governance module's cross-platform prerequisite
  contract after the Windows CPython 3.13 checkpoint reached full regression.
  Three Bash-dependent tests had attempted an unresolved fallback executable
  and raised `WinError 2`; they now skip individually and visibly only when
  Bash is unavailable, while three platform-neutral checks always run and all
  six original assertions run where Bash exists. Full-regression failure/error
  handling and actual test/skip reporting remain unchanged. No runtime,
  support-state, PI, deployment, or production mutation occurred.

- Hardened every native execution path in the Windows CPython 3.13 checkpoint
  after the corrected operator run passed installation and failed at
  `PYTHON_PROBE`. Git, WinGet, `pymanager`, the exact 3.13 probe, all test
  stages, and compilation now share one PowerShell 5.1-safe wrapper with
  deterministic argument quoting, bounded stream capture, and native-exit-code
  semantics. The checkpoint reuses an authoritative managed 3.13 selection and
  installs only when absent. No exact 3.13 patch or compatibility result is
  inferred, support remains pending, and no Python/PI/production action occurred
  in this repository correction.

- Corrected the governed Windows CPython 3.13 checkpoint after forensic review
  proved that informational Python Manager stderr could become a PowerShell 5.1
  exception before native exit-code evaluation. Scripted management now uses
  `pymanager`, automatic runtime installation is disabled before every launcher
  probe, and one native-process helper captures stdout/stderr with the actual
  exit code. The official manager is present; an informal diagnostic's
  unintended CPython 3.14.7 installation is preserved and classified as an
  operator side effect, not HIOC support or production state. A safe dry run
  observed 3.13.15, while the governed line remains floating 3.13.x and pending
  validation. No Python install/uninstall or production action occurred here.

- Added the repository-controlled Windows CPython 3.13 installation and
  compatibility-validation checkpoint. The PowerShell script self-verifies its
  approved Git identity and pending support state, uses only the official WinGet
  Python Install Manager path, executes the complete governed validation matrix
  through `py -3.13`, preserves repository cleanliness, and emits sanitized
  promotion evidence. It does not promote support, execute PE-3 Action 1, or
  perform production work. No installation was executed in this commit.

- Established the authoritative Model D Python runtime compatibility policy.
  CPython 3.10 is the language floor, CPython 3.12.13 is the sole exact
  full-suite-tested version, Windows CPython 3.13.x is proposed with validation
  pending, and the distribution-managed production version remains unverified.
  Action 1 now requires explicit repository support promotion, probes only
  CPython 3.13 in `py -3.13`, `python3`, `python` order, disables automatic
  installation, and distinguishes missing from incompatible runtimes. The
  genuine Windows prerequisite failure remains separate from the earlier chat
  delivery defects. No Python installation or production action occurred.

- Replaced chat-delivered PE-3.3 Action 1 source with the repository-controlled
  Windows PowerShell script `tools/hioc-pe3-action1.ps1`. The runbook now records
  the script SHA-256 and Git blob and exposes only a direct parameterized
  invocation. The script self-verifies repository, governance, implementation,
  and script identity before the unchanged read-only artifact validation. Both
  failed operator attempts are delivery-path defects with no valid Action 1
  evidence and no PI3 or production impact.

- Attempted a PE-3.3 Action 1 operator-copy integrity correction after a
  delivered block was corrupted by Markdown escaping and backslash loss. That
  chat-delivery approach was later superseded by the repository-controlled
  script recorded above. The failed transcript is delivery failure, not
  manufacturer validation evidence; no production action occurred.

- Corrected the PE-3.3 Action 1 interactive-session defect. Expected Python,
  build-pair, repository/Git, containment, and validator failures now print
  sanitized result/error codes and return from a single function-scoped block;
  unexpected exceptions return `ACTION1_UNEXPECTED_ERROR`. Action 1 contains no
  `exit`, preserving the PowerShell prompt and evidence. No Action 1 validation
  evidence was accepted, and no PI3/PI5 access, transfer, deployment, production
  mutation, sidecar generation, or PE-4 work occurred.

- Hardened the documentation-only PE-3.3 Action 1 operator procedure after
  pre-execution review. It now resolves an executable Python 3 in the frozen
  `py -3`, `python3`, `python` order with `PYTHON3_NOT_FOUND`, and discovers an
  adjacent database/manifest pair only after both frozen hashes and sizes match,
  with deterministic selection among identical matches and
  `VALIDATED_BUILD_PAIR_NOT_FOUND` for zero matches. No Action 1 execution,
  artifact change, transfer, PI3/PI5 access, deployment, production mutation, or
  PE-4 work occurred.

- Audited and synchronized repository-wide documentation governance against Git
  history through PE-3.3. Corrected stale PE-1, PE-2, and PE-3 implementation
  status statements; restored the explicit PE-1 through PE-9 roadmap; preserved
  deferred monitoring, retention, notification, validator, dependency, and
  disaster-recovery work; documented authority and status vocabulary; and added
  `DOCUMENTATION_GOVERNANCE_AUDIT.md`. No executable, test, schema, production
  configuration, dataset, deployment, PI3/PI5, or PE-4 action occurred.

- Defined the documentation-only PE-3.3 production deployment and validation
  runbook. It freezes ten separately authorized operator actions, transfers only
  the validated normalized database/manifest, uses Git-object artifact identity
  and supported release deployment, atomically installs an immutable version,
  guards configuration changes, validates private sidecars and protected state,
  measures PI3 thresholds, and separates rollback domains. No transfer,
  deployment, PI3/PI5 access, sidecar generation, or PE-4 work occurred.

- Corrected PE-3.1 official-source normalization and conflict preservation.
  Organization normalization removes only U+200B/U+200E, collapses TAB as
  whitespace, and leaves every other prohibited control fail-closed. Assignment
  keys with multiple normalized organizations are stored without organization
  variants as explicit non-selectable conflicts; lookup returns
  `conflicting_assignment` and blocks weaker-prefix fallback. No IEEE rows or
  generated production artifacts entered Git.

- Implemented and repository-validated the private PE-3.1 manufacturer
  foundation: closed schemas, deterministic 36/28/24 lookup, local-only builder,
  lock-free validator, separately locked manual generator, atomic immutable
  publication/state writes, exact corrected errors, release preservation, data
  exclusion governance, 96 synthetic tests, and repository-host performance
  evidence. No IEEE or production data, network client, schedule, public
  inventory/consumer change, deployment, or production action occurred.

- Corrected the documentation-only PE-3.1 validator lock semantics. The
  standalone validator now explicitly acquires no lock and performs no mutation;
  database safety derives from atomic publication of complete immutable version
  directories. Runtime sidecar validation observes independently loaded files
  and reports cross-generation mismatches without repair. The exclusive builder
  and generator locks remain unchanged and are the complete manufacturer lock
  inventory. Future acceptance tests must prove the lock-free/read-only behavior.
  No executable, test, dataset, deployment, or production change occurred.

- Corrected the documentation-only PE-3.1 manufacturer error mappings by adding
  first-class bounded codes for dataset conflict, deterministic-build mismatch,
  sidecar validation, and status validation at the already frozen exits 10, 11,
  15, and 16. The `(code, message)` interface and every existing mapping remain
  unchanged. Builder owns conflict/determinism; validator and generator own
  sidecar/status validation. These failures prevent invalid artifact creation or
  publication, leave inventory and protected subsystems unaffected, and do not
  independently imply rollback. No executable, test, dataset, deployment, or
  production change occurred.

- Corrected the documentation-only PE-3.1 manufacturer generator lock order.
  The dedicated manufacturer lock now unambiguously covers database, manifest,
  and completed-inventory snapshot loading and validation through sidecar/status
  generation and writes. This closes the validation-to-generation TOCTOU gap
  while serializing manufacturer generators only; it does not acquire an
  inventory, PE-1, Asset, or other HIOC state lock and does not block or mutate
  inventory generation. The prior validate-before-lock implementation instruction
  is superseded only in this respect. No executable, test, dataset, deployment,
  or production change occurred.

- Froze the documentation-only PE-3.1 executable contract. Resolved the sidecar
  list-versus-map conflict and specified the separate manual generator, exact
  APIs/dataclasses/exceptions, database/manifest/sidecar/status schemas, builder,
  validator and generator CLIs, shared exit/error codes, configuration/paths,
  locks, atomic transactions, failure preservation, parser rules, EUI-64
  no-claim behavior, inventory input, privacy, release preservation, 92-test
  mapping, performance, production validation, and rollback. Local acquisition
  and transformation are approved; no code, test, dataset, deployment, or
  production change occurred.

- Approved the documentation-only PE-3.1 Manufacturer Enrichment implementation
  design. Froze restrictive license and external-injection governance, the
  normalized MA-L/MA-M/MA-S database schema and digest semantics, O(1)
  longest-prefix lookup, EUI/address-class behavior, three-module boundary,
  separate private manufacturer sidecars, provenance, PI3 performance bounds,
  fail-open isolation, privacy, production validation, rollback, and a 76-test
  executable plan. No code, dataset, deployment, or production change occurred;
  executable implementation remains gated and not started.

- Defined PE-3.0 Manufacturer Reference Enrichment architecture and governance
  without code, schema, tests, dataset or runtime changes. Selected pinned IEEE
  Registration Authority listings as the future authoritative upstream subject
  to an explicit redistribution-license gate; fixed deterministic lookup,
  provenance, confidence, privacy, failure-isolation, invariant, performance,
  validation and 64-case test contracts. PE-3.1 remains not started.

- Closed PE-2.1 Asset Foundation as **COMPLETE - PRODUCTION VALIDATED**. Deployed
  Git-derived identity, restrictive permissions, synthetic transactions and
  cleanup, final Asset equality, protected contracts, privacy, performance, and
  incident operational-drift classification passed. Four validator-governance
  defects were corrected without changing deployed Asset implementation files;
  no rollback occurred. PE-3 remains not started.

- Governed one-time cleanup of six exact PE-2 synthetic-only validation backups.
  Added an exact basename/SHA manifest, two-phase schema-aware cleanup tool, and
  moved future tracked current-run backup cleanup before unrelated invariants.
  No Asset implementation, real Asset state, retention policy, deployment, or
  rollback behavior changed.

- Corrected the second PE-2.1 validator-contract defect. Live `active.json` is
  no longer digest-immutable; a sanitized positive comparator classifies valid
  operational drift, proves Asset-to-incident isolation, and reserves rollback
  for causally demonstrated protected regressions. PE-2.1 remains deployed and
  open for validation-only production closure.

- Corrected the PE-2 production validator after the first supported deployment.
  All runtime artifact bytes matched Git, while the validator incorrectly
  treated Git `100644`/`100755` modes as runtime `0644`/`0755` requirements and
  its report writer inserted lowercase JSON booleans into Python source. A
  shared runtime-permission manifest, independent content/permission checks,
  safe JSON report renderer, corrected rollback classification and no-deploy
  revalidation mode now govern closure. No rollback occurred; PE-2.1 remains
  deployed and awaits corrected production revalidation.

- Implemented and repository-validated PE-2.1 Asset Foundation: strict private
  store/status schemas, governed local CLI, read-only validator, dedicated
  bounded lock, optimistic revisions, atomic fsync transactions, validated
  backup/restore, orphan context, privacy-safe output, conditional installer
  validation, release-preservation guards and synthetic tests. No public
  inventory, consumer, schedule or production change occurred; deployment and
  production validation remain pending.

- Completed the PE-2.1 Implementation Design Review without executable or
  production change. The approved design freezes module boundaries, schemas,
  normalization, locks, revisions, atomic transactions, backups/restores,
  sanitized output, exit/error codes, privacy, failures, production validation,
  cleanup, performance, release preservation, tests and the future implementation
  prompt. PE-2.1 executable implementation remains not started.

- Completed PE-2.0 design review and approved the implementation-ready Asset
  foundation for operator-managed `friendly_name`, `physical_location`,
  `purpose`, and private `notes`. The design uses a separate stable-ID-keyed
  closed local store, governed CLI, dedicated lock, atomic writes, validated
  per-mutation backups, explicit orphan handling, and deny-by-default privacy.
  Existing public naming/location fields are not reinterpreted; owner, public
  projection, expected availability, lifecycle, identity migration, UI and
  integrations remain deferred. PE-2.1 is not started and no executable or
  production behavior changed.

- Closed PE-1 Hostname Enrichment Evidence Envelope as **COMPLETE - PRODUCTION
  VALIDATED**. Git-derived artifact identity, supported deployment and backups,
  authoritative schema validation, and corrected production validation passed.
  Production reported `online`, 153 records, 83 candidates, 82 selections, zero
  conflicts, and the three observed source types `assignment_observation`,
  `configured_infrastructure`, and `direct_observation`. Missing optional source
  types, history, and conflicts were acceptable; protected public and
  operational contracts did not regress, no rollback occurred, and PE-2 was not
  started.

- Corrected the PE-1 production aggregate validator after its duplicated
  `source_type` allowlist used acquisition/source identity names instead of the
  emitted closed-schema values. Deployment, Git/runtime artifact identity,
  controlled inventory execution, and authoritative enrichment validation had
  already passed; no rollback condition was demonstrated, and the deployed
  PE-1 implementation remains unchanged.

## Document Ownership

This document owns released and delivered work.

This is the repository's single authoritative changelog. The root [CHANGELOG.md](../CHANGELOG.md) is a discoverability pointer only. All future release and completed-checkpoint entries must be written here. Maintaining a second overlapping full changelog is prohibited unless a separately approved governance decision establishes a distinct, non-overlapping purpose.

Use these categories when applicable:

- Added
- Changed
- Removed
- Fixed
- Deprecated
- Security

Do not place roadmap items here. Future work belongs in [../ROADMAP.md](../ROADMAP.md) and detailed implementation direction belongs in [HIOC_MASTER_PLAN.md](HIOC_MASTER_PLAN.md).

## Unreleased

### Added

- Implemented the repository-validated PE-1 Hostname Enrichment Evidence
  Envelope. The Inventory Engine now produces validated, restrictive local
  `enrichment.json` and `enrichment_status.json` sidecars from the four approved
  existing hostname sources, with deterministic normalization, authority,
  conflict, confidence, bounded history, atomic writes, and fail-open isolation.
  Public inventory, MQTT, Home Assistant, dashboards, incidents, identity,
  canonical address, liveness, health, topology, service ownership, retention,
  and operator metadata remain unchanged. Production deployment and validation
  subsequently passed.

- Added a deployed, read-only MQTT runtime validator that uses existing HIOC
  configuration to perform bounded retained-topic checks and emit concise
  post-install or post-upgrade Evidence Report output without publishing state
  or exposing credentials.

### Documentation

- Completed PE-0 design review and approved the implementation-ready PE-1
  Hostname Enrichment Evidence Envelope specification. The package closes
  hostname source eligibility, normalization, authority, deterministic
  selection, conflict/confidence, local schema, bounded lifecycle,
  failure-isolation, module, test, production-evidence, rollback, and privacy
  decisions. PE-1 remains not started; no executable or production behavior
  changed.

- Refined the proposed Passive Enrichment architecture into permanent,
  non-destructive Observation, Enrichment, and Asset information layers.
  Documented their separate authority, mutability, provenance, persistence,
  privacy, stale-observation, and expected-availability meanings; clarified
  that PE-1 records hostname observations and enrichment candidates but creates
  no Asset name or public/runtime behavior. PE-0 remains in design review and
  PE-1 remains not started.

- Defined the Phase 7A Passive Enrichment Architecture and Specification for
  design review. It maps implemented and absent passive sources, audits the
  current schema, separates metadata layers, and proposes field-level
  provenance, conflicts, categorical confidence, privacy boundaries, and an
  ordered implementation sequence. The first proposed sub-checkpoint is a
  local-only hostname evidence envelope. No executable or production behavior
  changed, and implementation remains subject to explicit approval.

- Closed Canonical Address Selection Hardening as production validated. The
  unchanged comparator from `839e924` matched source and runtime at the
  approved Git-derived SHA-256; all six strict Boolean invariants passed;
  diagnostic metadata remained informational; inventory stayed at 151 devices;
  and one unrelated canonical-address change remained within the bounded
  invariant. Final result was `NO_QUALIFYING_CANDIDATE` with no rollback. Both
  earlier failures were validator defects, not comparator defects. The
  unexpired `.152` old lease remains separate future DHCP cleanup evidence.

- Established the focused documentation architecture: the Master Plan remains the authoritative roadmap; the new System Reference Manual owns current state; Operations owns the cron-driven runtime and freshness-based health model; Network Foundation owns critical addresses and dependencies; Deployment owns source-to-runtime boundaries; and Incident Model owns operational incident semantics. Added the permanent July 29 DHCP pool-exhaustion incident report, recorded HIOC deployment validation as PASS, added the Operations Acceptance Standard, and planned a future DHCP Service Health & Capacity Monitoring phase without implementing it.
- Closed Pi-hole DHCP Lease Ingestion as **PASS WITH DOCUMENTED WARNING** after supported production upgrade, PI3 validation, and successful inventory generation. All 140 active lease MAC identities were represented with DHCP provenance and expiry metadata; seven additional DHCP-backed identities were confirmed as retained expired historical records rather than duplicate active leases. One active lease MAC/IP pair differed from the selected canonical IP because the same MAC owned two simultaneous `STALE` neighbor addresses. DHCP ingestion remains passed; deterministic canonical-address precedence is deferred to a separate Phase 7A hardening checkpoint that must preserve MAC-backed identity and must not treat DHCP assignment as liveness.
- Accepted ADR-0015 for the active Pi-hole DHCP Lease Ingestion checkpoint. Pi-hole DHCP remains a source-specific adapter within the existing passive-driver and source-tagged device-record convention; central reconciliation continues owning canonical identity, authority, and observation semantics. The decision rejects a new `IdentitySource` or plugin framework, defines DHCP field ownership and deterministic conflict rules, and bounds the later implementation without marking DHCP ingestion complete.
- Completed Repository and Deployment Hygiene. Historical runtime provenance proved that HEAD `94e1997f0d9df9e43209e44f7eb62a8d808714cc` was preserved in authoritative history and that no runtime-only commits, branches, tags, or stashes existed. The approximately 2.6 MB `.git` directory was quarantined and validated, the non-Git runtime passed production validation, a supported upgrade did not recreate `.git`, rollback did not restore it, post-rollback SHA-256 comparisons matched the authoritative release source for the checked deployment artifacts, and persistent runtime data remained intact. The approved quarantine path was removed successfully, the runtime remains formally non-Git, and all checkpoint closure criteria are satisfied.
- Completed Repository Governance Reconciliation on 2026-07-28: retained `validation/phase-7a8-lifecycle` locally and remotely as the intentional reachability reference for approved recovery candidate `be7b69d`; retired three fully merged local branches and the two corresponding remote branches that still existed; and removed the untracked `hioc_known_hosts.tmp` workspace artifact after confirming that no operational tooling consumed it. At that stage the overall Repository and Deployment Hygiene checkpoint remained open for the two manual PI3 audits and final closeout; the audits and production engineering validation are recorded as complete in the later entry above.
- Reconciled changelog governance by restoring the root `CHANGELOG.md` as a pointer to this authoritative record. Repository history confirms that the documentation-governance migration established this single-authority model; a later bounded implementation entry accidentally replaced the pointer and became stale after Collector Canonical Ownership regression, production, and documentation validation completed. No historical evidence was removed from Git history.
- Closed the Phase 7A Collector Canonical Ownership checkpoint after implementation commit `054fb55a2e70901f3230145b76983c31d2b5ce61` passed release validation, supported production upgrade, Pi4 validation, and production evidence review. The canonical collector remained MAC-backed at `192.168.100.252`, all eight services were owned by `Pi3 - NUT and Pi-hole`, and the historical `.105` ownership defect was not observed; this documentation-only closeout does not change runtime or public contracts.
- Recorded successful production deployment and validation of the single-snapshot ARP semantics correction: normal discovery reported `arp_table`, discovery remained unlimited, and the checkpoint closed after PASS evidence.
- Recorded successful ADR-0014 production validation and made the repository the
  authoritative operational reference for configured, read-only MQTT runtime
  validation after installation or upgrade.
- Documented the planned asset-centric Living Inventory vision, including evidence authority, observation versus availability, operator-managed asset knowledge, lifecycle-safe retention principles, and roadmap dependencies; no runtime behavior changed.

### Fixed

- Fixed the revised canonical production validator's invariant input contract.
  It previously applied generic truthiness to diagnostic metadata and treated
  `_unrelated_canonical_change_count: 0` as failure despite all six Boolean
  invariants passing. The validator now requires the closed, typed Boolean
  schema, preserves underscore-prefixed diagnostics without evaluating them,
  and reports malformed input explicitly. At that correction stage the
  expected rerun result was `NO_QUALIFYING_CANDIDATE`; rollback was not
  performed, the comparator was unchanged, and closure remained pending the
  PI3 rerun recorded above.

- Corrected the Canonical Address Selection production-validation procedure
  after the first governed run admitted an IPv6 link-local stale neighbor and
  ignored higher-authority configured integration evidence. Repository-owned
  validation now enforces the intended stale-IPv4-versus-active-DHCP contract
  and distinguishes `PASS`, non-rollback `NO_QUALIFYING_CANDIDATE`, and genuine
  `FAIL`. The comparator was unchanged and remained deployed. Active DHCP
  evidence for retired PI5 address `.152` remained unresolved pending the
  read-only PI3 investigation, and the checkpoint remained open at that stage.

- Implemented the repository correction for deterministic canonical IPv4
  selection. Neighbor state now participates as private reconciliation
  evidence; an active DHCP assignment for a MAC cannot lose merely to a stale
  neighbor address, while stronger current/configured evidence and legitimate
  static devices remain supported. Stable MAC identity, aggregate provenance,
  liveness, health, schemas, dashboards, incidents, and retention are
  unchanged. Production validation remains pending, so the Phase 7A checkpoint
  is still open.

- Closed the network-probe checksum-governance and PI5 endpoint-migration
  correction after governed PI3 deployment at
  `e06539d9bece040d721b9912213559cc54f1610d`. Blob, worktree, and deployed
  checksums matched; Phase A and Phase B passed; retained PI5 state and
  inventory were correct; the false incident cleared; and no rollback or
  warning was required. Phase 7A remains active.

- Separated deterministic network-probe deployment validation from bounded
  downstream incident-recovery observation. Delayed or inconclusive recovery
  now produces PARTIAL PASS and follow-up without rollback. Added safe read
  accounting, malformed-payload handling, backup validation, and a tracked
  operator procedure.

- Corrected the Phase 7A network-probe checksum-governance defect. The
  previously reported `27e4dec6...` checksum remains only as incident evidence:
  it is proven to be the CRLF Windows checkout hash, not the approved Git blob
  hash. Added deterministic Git-object identity, commit-bound deployment with
  blob/source/target byte comparisons, and stale-checksum regression tests.
  PI3 deployment was pending at that implementation stage and is closed by the
  later production-validation entry above.

- Implemented bounded Pi-hole DHCP lease ingestion semantics. Inventory cycles use one fixed collection epoch; only active finite or infinite IPv4 Pi-hole/dnsmasq leases contribute assignment evidence; expired, IPv6, ISC-format, malformed, and unusable rows contribute no identity evidence. Explicit blank configuration disables acquisition, the default is limited to `/etc/pihole/dhcp.leases`, source aggregation preserves complete and incomplete states, and unavailable configured DHCP evidence reports truthful discovery limitation without weakening MAC-backed identity or observation authority. Automated regression validation passed, and the later production Evidence Report closes the checkpoint with a documented canonical-address warning.
- Implemented the repository side of runtime Git metadata retirement. Upgrade backups now exclude `.git`, rollback restoration excludes `.git` even from historical backups, and tests preserve legitimate hidden files and persistent-state protections. README and operator documentation now use the release-source installation model, ADR-0013 formally defines `/home/jazofv1/hioc` as a non-Git runtime, and runtime version identity remains owned by `VERSION.yaml`. Manual PI3 provenance capture, quarantine, upgrade, rollback, and production validation were pending at that stage and are recorded as complete in the later production Evidence Report entry, including approved quarantine removal.
- Hardened release construction so `release/build.sh` obtains its complete source set from Git-tracked files instead of traversing the workspace. Ignored, untracked, cache, and temporary artifacts—including `hioc_known_hosts.tmp`—cannot enter a release merely by existing beside the source. The generated manifest now records the source commit without checkout-path or wall-clock fields, while deployment and runtime behavior remain unchanged.
- Deployed the bounded Pi-hole DHCP Single Snapshot Acquisition correction: inventory captures lease files once into a cycle-local immutable snapshot and reuses it throughout discovery status, passive observations, and reconciliation, removing duplicate acquisition without intentionally changing functional behavior. Automated regression tests prove the single-acquisition invariant; successful production deployment confirmed `dhcp_leases_found`, 145 DHCP-backed devices, preserved `/etc/pihole/dhcp.leases` metadata, and no observable inventory regression. The broader DHCP checkpoint remains open.
- Completed the Dashboard Severity Mapping checkpoint at implementation commit `1e2dcf973d02514561b7bb8a4f5c6f495350ab09`: Living Inventory aggregate Watch wording now covers observation or availability review without incorrectly describing every Watch condition as stale, Dashboard v2 gives unavailable inventory status precedence over retained device counts when styling Inventory Summary, and production deployment and validation passed. Health, schemas, MQTT, entities, incidents, layout, and the existing blue Watch palette remain unchanged; the Watch color UX/design decision remains deferred.
- ARP discovery-source status and passive device evidence now share one authoritative neighbor-table acquisition per inventory cycle, and total primary-plus-fallback command failure is reported as unavailable rather than successful empty evidence. Unresolved-neighbor filtering, identity, retention, health, monitoring, and accepted NUD-state behavior remain unchanged.
- Incident Engine retained publication now uses one shared Core MQTT connection per run instead of placing complete payload documents in `mosquitto_pub -m` process arguments, preserving local history, embedded reviews, topics, retained semantics, and payload schemas while returning a truthful nonzero status for required publication failures.
- Living Inventory now includes a dedicated Watch Devices presentation, ordered by oldest known observation first and showing authoritative identity, observation, provenance, and health-reason details without changing inventory semantics.
- Pi-hole DHCP lease ingestion now distinguishes missing, unreadable, malformed, I/O-error, empty, partial, and usable sources; validates lease fields; preserves assignment metadata without treating a lease as liveness; and prevents DHCP data from overriding stronger current identity evidence.
- Local services now retain ownership by the canonical pre-enrichment collector identity; known-infrastructure classification can no longer erase local-host ownership, and a missing collector no longer falls back to an arbitrary inventory device. Canonical-address selection is unchanged and remains a separate future hardening checkpoint.
- Inventory Summary now renders the dedicated recommendation entity so watch-only passive clients do not imply operator attention; degraded and offline guidance is unchanged.
- Home Assistant operational presentation now preserves the operator-supplied Dashboard v2 layout, treats missing incident/inventory/forecast/platform payload values as unknown instead of all-clear or zero, and protects the reconciled layout and dynamic-truth policy with focused regression tests.

### Added

- Dashboard architecture guidance defining operational-truth ownership, unknown-state handling, operator-layout protection, and the current storage-managed deployment boundary.
- Living Inventory engine with local/network discovery, inventory database, topology, service dependency graph, firmware fields, MAC/IP tracking, health scoring, and last-seen timestamps.
- Retained MQTT inventory topics under `home/infrastructure/hioc/inventory`.
- Home Assistant Living Inventory package and dashboard.
- Pi4 installer, uninstaller, and validation integration for inventory.
- Unit tests for inventory identity, health scoring, topology, and dependencies.
- Architecture, project, MQTT, Home Assistant, data model, roadmap, and decision documentation.
- Passive-by-default inventory discovery with active discovery disabled unless explicitly configured.
- Persistent MQTT client abstraction for Living Inventory publications.
- 30-minute default inventory refresh interval.
- Topology inference for intermediate infrastructure devices and integration-provided parent hints.
- HIOC Core v1.0 shared runtime with StateStore, schema validation, event bus, driver registry, capability registry, configuration service, and structured logging.
- Living Inventory internal events and capability state without changing public MQTT or Home Assistant entities.
- Dashboard v2 with Executive, Operations, Diagnostics, Inventory, Network, and Servers views built from real HIOC-owned entities.
- Release System v1.0 with version manifest, build/package/validate/install/upgrade/rollback scripts, platform status publisher, MQTT platform topics, and Home Assistant platform entities.
- Correlation Engine v2 with Core event context, topology-aware root-cause analysis, confidence scoring, lifecycle phases, duplicate suppression, and backward-compatible incident MQTT/Home Assistant output.
- HIOC Master Plan as the authoritative project charter.
- Passive known infrastructure definitions from `/home/jazofv1/hioc/config/inventory/known_infrastructure.json` to enrich Living Inventory without active discovery.

### Fixed

- Passive ARP/DHCP-only clients now retain stale observation state without generating availability incidents, while a centralized Core policy keeps infrastructure and authoritative sources operationally monitored.
- Dashboard v2 now presents active incidents using their actual Warning, Major, or Critical severity, with an Unknown fallback for unavailable severity or status.
- Release upgrades now invoke the Pi4 installer through Bash so clean source-controlled copies do not require the executable bit before installation.
- Platform-status logging now uses standard logging arguments so successful installation and upgrade runs can complete.
- Inventory now reconciles unique current or retained IP-only identities with unique current or retained MAC-backed identities without merging conflicting MACs.
- Inventory now excludes unresolved or MAC-less neighbor-cache entries from durable devices and removes legacy MAC-less records supported only by ARP provenance.

## v1.0.0-core

Initial real HIOC core foundation.

### Added

- Pi4 installer and uninstaller.
- Incident engine that reads existing Pi4 probe state and publishes structured MQTT JSON.
- Persistent active incident, incident history, summary, and timeline JSON files.
- Duplicate suppression through stable incident keys.
- Recovery detection and duration calculation.
- Home Assistant MQTT sensors for active incident, severity, status, system, summary, history count, and latest timeline event.
- Home Assistant notification automation driven from structured incidents.
- Documentation for architecture, incident model, MQTT topics, and installation.

### Notes

- This release is intentionally compatible with the existing `~/pi4-tools` installation.
- It does not replace the existing `hioc-network-probe.sh`.

- Phase 7A repository governance now owns the checksum-verified HIOC network probe source, derives PI5 probing and inventory addressing from `HOME_ASSISTANT_IP`, provides guarded deterministic deployment, and separates Dashboard V2 MQTT operational freshness from forecast trend. This entry records the earlier pending state; the Unreleased production-validation entry closes it.
# Unreleased

- Governed CASE A for the PE-4.0B.2a PI3 dependency: retained the accepted
  distribution CPython 3.11.2, froze the official AArch64
  `websockets==16.1.1` wheel and SHA-256 in an offline lock, and defined a
  versioned release-managed virtual environment with atomic activation and
  bounded rollback. No dependency was downloaded, installed, or deployed and
  PE-4.0B.2a remains not started.

- Implemented repository-controlled PE-4.0B.2a isolated-runtime lifecycle
  tooling with separate A-G authorization boundaries, offline hash-locked
  construction, capability validation, atomic pointer publication, bounded
  cleanup, sanitized evidence, durable artifact-cache recovery, and dedicated
  rollback. No tool was executed against PI3, PI5, or Home Assistant.

- Corrected the PE-4.0B.2a-A Windows acquisition contract: removed POSIX `/tmp`
  evidence assumptions, added protected Known-Folder cache/evidence DACLs and
  reparse rejection, enforced a monotonic total download deadline, bounded CLI
  failures, and recorded explicit durable-cache/evidence partial-success state.
  Action A remains unexecuted.

- Corrected the PE-4 Action D transfer-consumption, environment/construction
  identity, offline pip isolation, cleanup and evidence-lifecycle defect.
  Action D now uses an invocation-owned verified snapshot, descriptor-anchored
  construction, explicit Python/pip isolation, exact distributions,
  no-replace confirmed evidence and an Action E eligibility marker. Action D
  remains blocked and not executed pending publication and fresh review.
- Corrected the PE-4 replacement Action B transaction boundary after its first
  governed replacement attempt stopped at `REMOTE_STAGING_IDENTITY_INVALID`.
  CPython may generate `_` in the eight-character temporary suffix; the shared
  Action B/Action D grammar now accepts exactly `[A-Za-z0-9_]{8}` while Action
  D retains its independent descriptor, entry-set, artifact, PASS-evidence,
  and confirmation gates. Added a version-controlled one-shot PowerShell
  wrapper that parses Git divergence semantically, preserves tool output, and
  cannot chain into Action D. The failed empty PI3 staging directory is retained
  for separate disposition; no transfer, Action D, cleanup, or retry occurred.
- Corrected the replacement Action B wrapper's Windows PowerShell native
  argument transport. One governed wrapper invocation stopped at local precheck
  because legacy argument serialization stripped quoted Python literals and
  yielded `NameError: tools`. The Action B launch site was not reached; no SSH,
  PI3 staging, transfer, or PI3 forensic work occurred. Every wrapper Python
  invocation now uses structured `ProcessStartInfo.ArgumentList`, and terminal
  markers distinguish wrapper entry, prechecks, launch, and transaction state.
  The wrapper now fails closed under legacy Windows PowerShell 5.1 and requires
  the governed managed PowerShell Core host that supports `ArgumentList`.
## Unreleased

- Action D now retains bounded sanitized diagnostics and separate private failure
  evidence without changing runtime construction or eligibility semantics.

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

Final repository hardening validates descriptor ownership and cleanup, Policy C
(no exceptional evidence-child pathname deletion), bounded publication/verification,
4096-byte evidence including newline, temp-root acquisition, and precise confirmed
evidence disclosure. These repository changes are not deployed. Final technical
contracts and validation evidence are recorded in HIOC_MASTER_PLAN.md and
PE4_ISOLATED_RUNTIME_DEPENDENCY_CONTRACT.md.
