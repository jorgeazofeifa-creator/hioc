# PE-4.0B.2a Isolated Runtime Lifecycle

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

G consumes immutable F completion facts and proves only local credential-free,
network-free runtime health and client detection. D/E/F remain closed; G remains
NOT STARTED pending separately authorized native and production checks.

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

Preserve the full lifecycle chronology and the immutable identity of the single actual production Action E execution.

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

Chronology: separate PI3 synchronization PASS was followed by separately authorized native non-lifecycle validation PASS. Neither checkpoint invoked Action E main() or advanced Action E/F/G; the accepted D chronology and immutable handoff remain intact.

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

This is an Action E implementation correction only. The accepted D chronology, construction, marker and evidence remain untouched. Action E/F/G remain NOT STARTED and separately unauthorized.

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

The separately executed PI3 read-only D-to-E review is PASS/CLOSED. It is
a governance validation between lifecycle actions, not an Action E invocation
or capability probe. Existing Action D chronology remains unchanged.

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

## Corrected Action D to Action E transition

The accepted third Action D execution remains PASS/CLOSED with immutable producer
provenance. A later documentation/source closure commit does not rewrite that
handoff. E now distinguishes current source `--governance-commit` from mandatory
D producer `--action-d-governance-commit`; no fallback is permitted.

E parses both identities before its host gate, validates current clean checkout
and normalized source, then proves producer equality/ancestry and exact committed
D/common/lock blobs with replacement-object substitution disabled and complete
history required. Only after compatibility passes does E open the selected
construction and call the unchanged strict D eligibility validator with producer.
Existing distribution and capability checks then precede existing E validation
evidence and terminal PASS. The E success JSON schema is unchanged.

This is a repository correction, not a D rerun or E execution. Historical first
two D failures and the intervening pre-execution stop remain historical; the third
D execution remains accepted. Replacement B PASS/CLOSED, C PASS exactly once and
D-PREP PASS/CLOSED are unchanged. E/F/G remain NOT STARTED. F publication and G
preflight remain separate, unchanged actions; no E-to-F evidence gate or combined
production suite is introduced. No rollback or cleanup occurred. The separately
authorized PI3 synchronization/read-only compatibility validation subsequently
PASSed. The next boundary is separately authorized E
re-preparation against the resulting documentation closure consumer commit.

The original implementation synchronization/read-only validation boundary
is now PASS/CLOSED as recorded above. Next checkpoint:
`ACTION_E_REPREPARATION_READY_FOR_SEPARATE_AUTHORIZATION`.

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

Current sequence: A -> B -> C -> D-PREP -> D -> E -> F -> G, with separately
authorized STOP boundaries at every step.
