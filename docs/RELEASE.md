# HIOC Release Process

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

## Action G implementation status

The dedicated controlled preflight and strict result contract are implemented.
No production G execution or authenticated Home Assistant validation occurred.

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

Record Action E release-governance closure and retain the exact accepted evidence; publication and activation remain separately authorized future work.

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
