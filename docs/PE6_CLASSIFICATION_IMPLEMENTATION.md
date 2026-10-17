# PE-6.1 Private Classification Implementation and Repository Evidence

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


## Authority and scope

The user explicitly adopted all twenty PE-6.0 decisions at
ea4a93fba1615af1d6641c7f0683b8e912c03d72. The accepted design record, schema,
document, original authorization appendix, and PE-4/PE-5 records are immutable.
This checkpoint implements the adopted private API and offline caller in the
Windows repository. PE-6 as a phase remains IN_PROGRESS; PE-6.2 is not started.

## Private API and exact source snapshots

hioc.classification.resolve_classification(inputs, evaluated_at, policy) is pure:
no files, clock acquisition, environment, subprocess, network, publication or writes.
Inputs have seven allowed kinds. Each supplied snapshot has exactly state, sha256,
value and raw; raw is captured UTF-8 JSON, SHA-256 covers the exact original bytes,
strict JSON rejects duplicates/nonfinite/deep values, and schema validation uses
the parsed original bytes. The convenience snapshot helper preserves field order;
the canonical encoder is only for deterministic identities and comparison.

The accepted output shape/rules/dimensions are copied exactly into
classification_contract.py. Its original schema title is historical design text;
the implementation record and Master Plan own current lifecycle. Semantic validation
recomputes every result from current snapshots and policy at original evaluation,
then rechecks source validity at a newly supplied current time. There is no trusted
stored result, LKG, restart adoption or history cleanup. Required bad inventory yields
UNAVAILABLE; rejected optional sources yield PARTIAL and explicit source reasons.
Asset/configuration data is durable knowledge with no invented observation TTL.

Identity eligibility reuses PE-5 unique current ID/MAC and MAC-derived owner checks.
PE-6 creates no identity or physical Asset classification. Weak/orphan data remains
unchanged. Only approved exact original known-config bytes plus unique strong MAC
binding establish operator_role; explicit Unknown remains explicit. Competing roles
remain conflicted with no selected declaration. Public role/type/sources are not proof.

Seven rule identities remain versioned pe6-role-v1: six exact ASCII PE-1 token
families and confirmed PE-5 local service ownership. Historical, invalid, unpaired,
conflicted, Unicode/punycode-uncertain evidence cannot supply hostname suggestions.
All automatic confidence remains low, even with correlated or repeated evidence.
Sorted rule/evidence/correlation IDs preserve explanation without raw names or topics.
Suggestion identity hashes the accepted [version,device,role] array without newline;
digest/revision/time changes do not change that semantic ID.

Metadata quality applies conflicted > unknown > incomplete > documented.
The eight source-owned dimensions separate identity, Asset completeness,
manufacturer attribution, operator confirmation, unsupported physical classification,
suggestions, relationship evidence and provenance. Notes are optional and never
parsed. Name/location/purpose are not copied to public fields. Quality is not health,
availability, truth or confidence; no score is introduced.

Manufacturer attribution requires the closed PE-3 validator, exact approved manifest,
database byte checksum/size, semantic digest, manifest/database agreement and a
recomputed current-MAC sidecar using existing PE-3 lookup semantics. Manufacturer,
HA domains/area candidates, MQTT mappings, ports and IPs alone produce no role.
HA input accepts only the existing sanitized five-field strong-MAC summary.

PE-5 evidence is captured through Store.read_handoff plus confirmed output/source
authority. The pure consumer additionally validates current inventory digest,
configured source/revision and original handoff semantics. PENDING or mismatched
evidence never becomes confirmation; root VALID does not mean all branches valid.
Inventory deadline is updated+2100; accepted PE-5 evidence further caps the result
at its unchanged valid_until (at most evaluation+1200). Use at the deadline,
backward/future clock and changed input proofs is rejected.

## Offline caller and lock lifecycle

pi4/bin/hioc-classify-metadata.py requires explicit inventory input and prints only
state and aggregate counts by default. There is no output-path, public projection,
scheduler, collection, repair, deployment or credential option.
Optional paths are --assets, --known-operator-role, --hostname, --manufacturer and
--home-assistant-summary. Known declarations require --approved-known-sha256 for
the exact original file bytes. Manufacturer support requires explicit database,
manifest and approved-manifest SHA-256 options. These are operator-approved inputs,
not permission to select or inspect current production sources in this checkpoint.

--assets additionally requires --asset-lock matching the separately established
existing Asset writer lock. Missing locks are not initialized. Shared Asset acquisition
uses the existing AssetLock and can invoke its existing chmod on an approved lock;
it does not rewrite Asset content. PE-5 --pe5-handoff uses the established fixed-root
Store reader, whose existing lock may create its .lock. Those bounded lock side
effects must be separately authorized operationally; no runtime use is authorized here.
Each lock is released before the next family is acquired, including capture failure,
PE-5 failure and final recheck failure. No nested Asset/PE-5 locks are introduced.
No composer, producer, durability repair, resync, initialization or recovery runs.

Reads are bounded, reject links/hardlinks/nonregular files, check parent/file metadata
and fingerprints, then recheck all captured sources. POSIX uses the existing descriptor-
relative no-follow filesystem seam. Native Windows fixtures use the read-only Windows
seam and reject reparse ancestry. Synthetic Windows evidence is not a claim of native
Linux lock, filesystem-race or crash behavior. Such deployment/execution evidence stays
behind the separately authorized later checkpoints.

Limits are 4096 devices/services/Asset records, 16MiB per source/output, and 64
candidate/evidence IDs per admitted branch. Overflow reports LIMIT_EXCEEDED or
UNAVAILABLE; there is no truncation or mutation of larger existing stores.

## Preserved failure and correction evidence

The first stopped validation expected documented but received unknown. The fixture
serialized an Asset store through PE-6's lexically sorted encoder, violating the
ordered Asset schema. The source validator correctly rejected those bytes. The fixture
now uses assets.serialize_store; snapshot schema validation uses exact parsed bytes.
Focused tests preserve this distinction, valid exact-ID documentation, and success/
failure lock release/non-nesting. The accepted retry evidence was exact1/class9/
focused45/Asset27 with zero failures/errors, before the next stopped PE-5 group.

The next historical run stopped after 52 PE-5 tests: 51 passed, one error.
A sequencing consumer reached the PE-6.0 path-set check against the new PE-6.1 tree.
The original validate_design body, 21-path set, records and identities are retained.
Historical validation replays ea4a93f's exact Git objects and d6f9d3c..ea4a93f path delta;
it never suppresses current unauthorized paths. A separate exact PE-6.1 map validates
current bytes, full current scope, protected baseline and current lifecycle.
PE-4/PE-5 consumers overlay this validated successor last.
Negative tests reject refreshed historical identities, historical scope expansion,
protected-file changes, unrelated untracked files and current/historical substitution.
Earlier stopped runs remain historical evidence, not passing acceptance runs.

## Validation and operational limits

Native bundled Windows Python; repository-root stdin unittest harness; shell-free
PATH; HIOC_TEST_SHELL removed; PYTHONUTF8/PYTHONDONTWRITEBYTECODE enabled;
sys.path[:0]=['tests','pi4/lib']. Exact result counts are captured directly from
unittest results, with individual and class-level skips separated.

Required selections: exact prior PE-5 failure; affected PE-5 governance/bindings;
test_pe6*.py; test_assets*.py; test_pe5*.py; affected cross-phase modules from the
accepted design; privacy/provenance/schema/lock/protected tests; and the complete
unittest.defaultTestLoader.discover('tests') suite. Full native regression is mandatory
because this checkpoint adds product source. Optional dependency/POSIX skips are
not passes; no dependency installation or production fault claim is authorized.

The implementation record carries all thirty adopted fixture obligations and their
repository evidence versus later native checkpoint dispositions. Final observed counts
and concise independent acceptance are recorded in the publication Evidence Report;
no pending or failed suite is represented as passed. All baseline paths outside the
finite authorized implementation map must remain byte/mode-identical.

## Next checkpoint

PE-6.2 - PI3 Release-Source Synchronization requires separate authorization and
operator source-only evidence. No source synchronization, deployment, bounded
production execution, recurring activation or PE-7 work begins here.

## Exact additive runtime-gate compatibility correction

The original 26-path candidate is preserved and continued. Comprehensive validation
identified an additional current successor-consumer gap: the shared historical runtime
guard admitted the two PE-5.1 and five PE-5.3 sources but omitted the four new PE-6
files. Git proves all four are absent at both its historical PE-4 source and the
accepted PE-6.1 baseline. No historical runtime mutation caused the rejection.
The consolidated authorization permits justified final implementation changes.
Only tests/test_pe5_service_association_caller.py is added, making 27 authorized
paths. Its current guard now admits exactly the four identity-validated PE-6 files,
requires their absence at the baseline and historical source, and preserves every
original guard statement and test class. It does not exempt existing runtime files
or arbitrary new paths. The historical helper Git object, PE-6.0 21-path authority
and accepted governance records remain unchanged. The remaining 434 baseline files,
including all existing runtime and governance artifacts, remain protected.
The prior PE-4 run stopped at 1170 run/1152 passed/17 skipped/one error; the full
run stopped at 1850 run/1807 passed/42 individual skips/four class skips/one error.
These are retained failed historical attempts, not passing acceptance evidence.

## Consolidated correction and final repository acceptance

Windows comparisons now use explicit birthtime, mtime, device/inode, size, mode,
ownership, link count, file attributes and reparse tag. Missing reliable identity or
birthtime fails closed. Windows ctime is not used as interchangeable creation/change
[time](https://docs.python.org/3.12/library/os.html#os.stat_result.st_birthtime_ns).
The protected POSIX fingerprint still includes ctime. Bounded reads, directory
identity, regular-file/link/reparse checks, content digest and source rechecks remain.
Real Windows fixtures explicitly set different creation/write times without sleeps.
Same-size content changes with restored mtime and genuine replacements are rejected.

Current implementation acceptance is uncached: every public current binding and
lifecycle entry rechecks live scope, stage-zero objects/modes, record/schema, artifact
identities and protected files. Immutable Git bytes and historical design validation
remain cached; current preservation guards are fresh and historical return values are
independent copies. Warm-up tests simulate unauthorized paths, protected changes,
changed record/schema, artifact identity and index changes without repository mutation.

The existing OperatorPath Windows durability fixture creates an owned, unignored
 .hioc-capture-synthetic-UUID directory in the checkout and removes only that
fixture in its guarded finally block. Concurrent namespace validation is unsafe.
Observed write events and source/ignore rules establish that interference mechanism;
the original failed-run UUID was not captured. The final runs are sequential, with
no fixture exemption, ignore-rule change or relaxation of current scope checks.

The original recurring D execution did not capture its metadata. Its individual
historical filesystem state remains unknown; the reader failure mechanism itself was
causally reproduced in the read-only audit. Earlier failed runs remain historical
evidence. Fresh acceptance below is separate and all failures/errors are zero.

| Executed selection | Run | Passed | Failures | Errors | Individual skips | Class skips |
|---|---:|---:|---:|---:|---:|---:|
| additive_runtime_gate | 6 | 6 | 0 | 0 | 0 | 0 |
| exact_pe5_retry | 1 | 1 | 0 | 0 | 0 | 0 |
| governance | 64 | 64 | 0 | 0 | 0 | 0 |
| exact_lock_after_governance | 1 | 1 | 0 | 0 | 0 | 0 |
| caller_after_governance | 9 | 9 | 0 | 0 | 0 | 0 |
| focused_after_governance | 93 | 93 | 0 | 0 | 0 | 0 |
| full_native | 2974 | 2930 | 0 | 0 | 44 | 5 |

Required subset coverage was verified against actual full-suite executed test IDs.
These rows describe coverage within that full run, not additional suite executions.

| Coverage from full native suite | Run | Passed | Failures | Errors | Individual skips | Class skips |
|---|---:|---:|---:|---:|---:|---:|
| assets | 27 | 27 | 0 | 0 | 0 | 0 |
| pe5 | 243 | 243 | 0 | 0 | 0 | 0 |
| pe4 | 1905 | 1887 | 0 | 0 | 18 | 0 |
| pe6 | 93 | 93 | 0 | 0 | 0 | 0 |
| cross_phase | 517 | 515 | 0 | 0 | 2 | 3 |

Actual interpreter: 3.12.14 (main, Aug 25 2026, 14:01:42) [MSC v.1944 64 bit (AMD64)].
Established Windows repository-root stdin harness; shell-free PATH; HIOC_TEST_SHELL
cleared; PYTHONUTF8=1; PYTHONDONTWRITEBYTECODE=1; sys.path[:0]=['tests','pi4/lib'].
Environment and POSIX skips are listed in the existing implementation record and
are not passes. No dependency was installed. Full native execution covers the final
product-source bytes. Subsequent closure synchronization changes only this document
and the existing record/schema; fresh final binding and identity checks precede publication.
PE-5 and PE-6.0 remain COMPLETE/PASS. PE-6.1 repository implementation is COMPLETE/PASS;
PE-6 remains IN_PROGRESS. PE-6.2 is not started and requires separate authorization.
No production state, Linux lock/race/crash behavior or current production freshness is
claimed. Accepted PE-4/PE-5 observations remain OPERATOR_SUPPLIED. No PI3/PI5, HA, MQTT,
credentials or production access/mutation occurred.


## PE-6.2 source synchronization acceptance and formal closure

Classification: CURRENT; repository closure candidate until required validation,
commit, push and independent publication verification pass.
PE6_2_STATUS=COMPLETE/PASS; EVIDENCE_AUTHORITY=OPERATOR_SUPPLIED.
This is source synchronization only, with no production functionality acceptance.
Accepted PE-6.1 remains 94f014cea1d5216a1deeef9fd1d0a025f1c7083e.
The PE-6.0 design and PE-6.1 records/schemas and all preceding document bytes
remain immutable historical evidence; their then-next PE-6.2 statements are historical.

### Exact operator receipt and evidence limitations

Target: PI3 NUT&PIHOLE, hostname nutandpihole; all following PI3 facts are
OPERATOR_SUPPLIED, not Codex observations or independently recomputed production hashes.
Source: /home/jazofv1/hioc-release-source; runtime: /home/jazofv1/hioc.
Initial source main, HEAD=origin/main=4990c62afbce22a804229f3cb8329986741067a6,
clean working tree, no untracked files; remote=https://github.com/jorgeazofeifa-creator/hioc.git.
Fetch command git fetch --no-tags origin main returned 0; origin/main became
238dfae6cef1d4f17a4b1e52a5f636f01a5651c4. Ancestor check returned 0.
git merge --ff-only origin/main returned 0. Final source HEAD=origin/main=
238dfae6cef1d4f17a4b1e52a5f636f01a5651c4; final working tree clean.
Observed source tree=aaf32cd1d0c9ce1dc1e6e00382322226030738d7,
matching accepted PE-6.1 tree. Local immutable Git history independently verifies
ancestry and tree equality; it does not independently observe PI3 state.

All four tracked source artifacts were observed ABSENT under the runtime root:
- pi4/bin/hioc-classify-metadata.py
- pi4/lib/hioc/classification.py
- pi4/lib/hioc/classification_caller.py
- pi4/lib/hioc/classification_contract.py

Observed source directory inode=654548; runtime directory inode=802322;
both device=45826. They are distinct directories. No runtime deployment, caller
execution, scheduler activation, cron modification, service restart, MQTT operation
or PI5 operation was performed during this checkpoint. These observations do not
prove that every runtime file is unchanged, production health, current freshness,
input suitability, Linux execution semantics, or classification behavior in production.
Codex accessed no PI3, PI5, Home Assistant, MQTT, credentials or production system.
No new observation time, transcript, staging-state field or runtime hash is invented.

### Binding correction and validation boundary

The old current PE-6.1 validator froze exact current artifacts, path scope and next
checkpoint to PE-6.2. Its original validation body now replays the accepted PE-6.1
Git snapshot with its exact original index, 27-path delta and protected identities.
The existing PE-6.0 historical replay remains independent. Fresh PE-6.2 validation
owns exactly four paths: this document, HIOC_MASTER_PLAN.md and the two existing
PE-6 design/implementation test modules. It does not inherit PE-6.1 edit authority.
All other accepted-tree artifacts, including all product/runtime sources and old
records/schemas, remain byte/blob/mode-identical. Current stage-zero provenance,
exact document changes, lifecycle, scope, historical evidence and unexpected paths
are rechecked on every public current entry. Immutable Git bytes alone may be cached.
PE-4/PE-5 consumers retain their existing delegation and original historical checks.
Targeted historical/current, tamper, lifecycle, stage, cross-phase and protection
regressions are required. The prior 2974-test suite remains PE-6.1 product acceptance;
no runtime source changes occur here. Exact observed counts are recorded in the
closure commit/report, never substituted by historical totals. A failed gate blocks publication.

### Next separate checkpoint

PE6_1_STATUS=COMPLETE/PASS; PE6_REPOSITORY_IMPLEMENTED=TRUE;
PE6_PRODUCTION_DEPLOYED=FALSE; PE6_3_STARTED=FALSE.
NEXT_CHECKPOINT=PE-6.3 - Disabled Exact Runtime Deployment.
Separate authorization is required for PE-6.3: disabled exact runtime artifact
installation only; no caller execution, initialization, activation or cron.
PE-6.4 remains later separately authorized bounded execution and independent acceptance.
No recurring activation or automatic follow-on action is authorized. STOP after PE-6.2.

### Preserved validation diagnosis

The initial focused correction run completed 50 tests: 49 passed, zero failures,
one error. A new substitution fixture called the patched raw reader recursively.
It now captures current bytes before historical replay patching; the unchanged
historical validator must reject that substituted snapshot. This initial run is
failed evidence, not acceptance. Caller-visible scope/index values are copied to
prevent mutation from changing later authority. Final observed validation totals
are reported separately in the closure commit and Evidence Report.

The first complete affected run was 231 tests: 230 passed, zero failures, one error
in the existing PE-5 status-section interface. The new current entry had required
only a full document, overlooking that established caller. It now accepts only
the exact freshly bound full document or its exact Implementation Status section;
modified or historical substitutes are still rejected. All PE-4/PE-5 test bodies
remain unchanged. The complete focused and affected families are rerun after this
correction; the failed attempt is preserved and is not acceptance evidence.


## PE-6.3 disabled runtime installation acceptance and closure

PE6_3_STATUS=COMPLETE/PASS; EVIDENCE_AUTHORITY=OPERATOR_SUPPLIED.
Acceptance is disabled exact installation only, conditional on repository validation
and publication gates. All preceding PE-6.1/PE-6.2 document bytes remain an exact
accepted historical prefix; their deployment/next-task statements refer to those checkpoints.
PE-6.0 design and PE-6.1 governance records/schemas are unchanged.

### Source identity and operator-reported installation

Every PI3 statement below is OPERATOR_SUPPLIED, including the reported independent
post-installation verification. Codex did not independently observe PI3.
Target: PI3 NUT&PIHOLE, hostname nutandpihole; Python 3.11.2.
Source: /home/jazofv1/hioc-release-source; runtime: /home/jazofv1/hioc.
Source main HEAD=origin/main=723c1e71ad2d54e5088c0849ccee59857cbe0794,
clean; source and runtime directories separate. Source Git blobs were reported
equal to working-file blobs. Each source file was regular, owner jazofv1:jazofv1,
mode 644, one hard link. Local Git objects independently match the four supplied
source digests; this repository fact does not independently observe installed bytes.
PREFLIGHT=PASS; INSTALLATION=PASS; POST_INSTALL_ARTIFACT_VERIFICATION=PASS.
Exactly four previously absent destination files were installed, with no overwrite.

| Runtime-relative artifact | Accepted source / observed installed SHA-256 |
|---|---|
| pi4/bin/hioc-classify-metadata.py | 40d264d44ed9b52baa0abfc911afe98b29e84275e841769952922c66aafe5d03 |
| pi4/lib/hioc/classification.py | 29b33e0ac6ad06b7b8eb360f10e9403ffb29993830eee16e21ff1b448bfd7f1c |
| pi4/lib/hioc/classification_caller.py | b9238415e99d935b232481d8cb7a7f70adfbf2f353ed3e07f839810c540c78ca |
| pi4/lib/hioc/classification_contract.py | 6be0c1cf21b159b74878ab1174e0239dd748f416d5c383ebd14091e45e533561 |

All four installed files were reported regular, one hard link, UID:GID 1000:1000,
mode 0600. Destination parent directories already existed, were ordinary directories,
owner jazofv1:jazofv1, mode 755. No additional installation or runtime copy is authorized here.

### Seven existing dependencies preserved in the observed checks

PROTECTED_DEPENDENCY_VERIFICATION=PASS. These before/after runtime identities
were supplied by the operator; they do not prove preservation of every runtime file.
No listed dependency was replaced or removed in this checkpoint.

| Existing runtime dependency | Preserved operator-reported SHA-256 |
|---|---|
| assets.py | 9079c976e633d6d1f1c11bf051fc24ea5746500267f0fdfaf9ae1c5c8aea35c9 |
| enrichment.py | ce3a60521bdb5b0d100e45d688b2a5847fbf56db1b87fce3ead0c65840d2804a |
| manufacturer.py | 30d4ca1305b345442229395ac17b31a9e229ece08abc1f10732cb970c977cd08 |
| service_association.py | dfdbab8bea085dfa0755e61b1952ee7991d663055c1f58b715997af751260bc5 |
| configured_association.py | 9bab6fdfb0475a08d30c5d0c51c66ce3b9c841446047d420dccb41aa949357d8 |
| configured_association_store.py | 1d5aa3d76a948e0f5bb0049f1abf8fd6cf2343be217796728ce66cee633c77b1 |
| inventory.py | df1dc4e2de7d8d77b54acdcb3f340281ead6cc03d74a73ad59b2864b03564503 |

### Explicit inventory.py discrepancy and compatibility limit

Accepted source SHA-256:
4dad543d46c62a3335776d239f983082574361979200379990cf6c2ddfa3fb7e
Existing runtime SHA-256:
df1dc4e2de7d8d77b54acdcb3f340281ead6cc03d74a73ad59b2864b03564503
The complete operator-observed diff has two differences: source imports
from .core.compatibility import lease_observation; source adds
_compatibility.pihole_leases to inventory output when hostname evidence is included.
The operator reported exactly equal AST definitions for KNOWN_FIELDS, OPERATOR_ROLES
and normalize_mac. This establishes only those three definitions, not complete
runtime compatibility, every dependency behavior, or successful caller execution.
The differing runtime inventory.py is intentionally preserved. No replacement or
compatibility repair is authorized by PE-6.3. This remains a production warning
for separately authorized PE-6.4 input/dependency acceptance.

### Disabled activation: observed scope, not universal absence

Before installation, inspected locations returned no matching classification process,
scheduler or runtime classification artifact. After installation, the operator inspected:
user crontab; /etc/crontab; /etc/cron.d; /etc/cron.hourly; /etc/cron.daily;
/etc/cron.weekly; /etc/cron.monthly; /etc/systemd/system; /run/systemd/system;
and running processes matching the classification entry point or caller.
No matching entries or processes were returned. Release-source working tree remained clean.
No universal absence of indirect invocation mechanisms is claimed. There is no
classification caller execution, initialization, cron modification, service restart,
scheduled activation or PE-6.4 execution in this checkpoint's operator receipt.
No scheduler or automatic activation is authorized. Codex made no PI3/PI5,
Home Assistant, MQTT, credential or production access or mutation.

### Rollback boundary and remaining operational limitations

ROLLBACK=NOT_PERFORMED; ROLLBACK_TEST=NOT_ESTABLISHED.
The provenance-bound prior state is absence of precisely the four installed files;
no pre-existing destination bytes were overwritten or require backup restoration.
No backup/archive location or completed rollback receipt was supplied or is invented.
A future rollback requires separate operator authorization. First verify the exact
four destination paths, installed SHA-256 values, regular-file/owner/mode/link identities,
and relevant runtime-use conditions; resolve any change or use uncertainty before removal.
If all authorized preconditions hold, remove only those four specifically installed
artifacts to restore their prior absence. Preserve every pre-existing dependency,
parent directory, operator input, existing runtime configuration and historical journal.
Stop on identity drift or unresolved use; do not replace/delete inventory.py or perform
unrelated cleanup. Recheck the four-file absence and protected dependencies afterward.
This documents the bounded procedure; it is not an executed or fully tested rollback,
a production command authorization, or a universal proof of disabled invocation.

### Repository acceptance and next separate gate

Historical PE-6.1 validates at 94f014cea1d5216a1deeef9fd1d0a025f1c7083e.
Historical PE-6.2 validates its unchanged original four-path law and full/status
interfaces at 723c1e71ad2d54e5088c0849ccee59857cbe0794. Fresh current PE-6.3
owns only this document, HIOC_MASTER_PLAN.md and the implementation-binding test
module. All other accepted-tree files, product sources and old records/schemas
remain byte/blob/mode-identical. Full-document and exact Implementation Status
interfaces are retained; historical/current substitution and altered receipts are rejected.
Only immutable Git data/replay may be cached; current scope, stage, artifacts,
closed evidence, lifecycle and protected files are checked afresh.
Fast static/negative, focused PE-6 and directly affected PE-4/PE-5 tests precede
publication. Exact observed totals belong to the closure commit and Evidence Report.
The accepted 2974-test PE-6.1 product suite is historical evidence, not a new test run;
no product implementation changes occur here. Failed gates prevent publication.
PE-6 remains IN PROGRESS; PE-6.3 COMPLETE/PASS is disabled installation only.
PE-6.4 bounded execution and independent acceptance is NEXT / NOT STARTED and
requires separate authorization. No caller execution, activation or follow-on action
is authorized by this closure. STOP after PE-6.3.


## Timestamp compatibility correction prerequisite to PE-6.4

REPOSITORY_TIMESTAMP_CORRECTION=PREPARED_FOR_VALIDATION_AND_PUBLICATION.
This section records a repository correction, not PE-6.4 production acceptance.
All preceding PE-6.1/6.2/6.3 Evidence Report bytes are preserved exactly from
b83f56d19912b2b36b689cf95af8a56a45d02474. Their installation identities describe
that historical receipt, not deployment of the corrected classifier.

### Cause, timestamp dependency analysis and exact correction

OPERATOR_SUPPLIED: inventory.updated was 2026-10-17T11:00:02-06:00;
JSON parseable, 198 devices, fresh at inspection; classification not executed.
These are supplied observations, not Codex production access or current freshness.
The PE-5 service_association.TIMESTAMP_PATTERN/_time parser already accepts aware
Z and +/-HH:MM timestamps and normalizes to UTC. PE-6 timestamp() imposed an
additional Z-only gate before delegating to it, rejecting valid offset inventory.
The classifier now uses that accepted grammar/parser, with explicit offset-hour
and minute bounds to reject fromisoformat's normalization of malformed +01:60.
Naive timestamps, unsupported forms, invalid dates and impossible times fail closed
with the existing CLOCK_INVALID safe code. No input or inventory file is rewritten.

All timestamp() consumers were traced: evaluation clock; inventory.updated and
its 2100-second deadline; hostname candidate observed_at comparison; PE-5 handoff
valid_until cap; result original/current time, deadline and backwards-clock checks.
External inventory and paired hostname/manufacturer generated_at remain unchanged
in captured source bytes and SHA-256 provenance. UTC projection is used only in
output proof timestamps. Caller-generated clocks and deadline output remain UTC.
Offset evaluation values are projected to canonical UTC; existing Z representation
is retained. The immutable closed PE-6 output schema, rules and dimensions are
unchanged. _hostname retains exact generated_at/inventory.updated source pairing;
equivalent time does not substitute for exact source identity. _handoff continues
using PE-5's original confirmation, schema, inventory-digest and expiry authority.
No source-specific validator is weakened. Result validation rederives from current
inputs, rechecks original fingerprints and temporal validity, and rejects reencoding
of a bound source even when it denotes the same instant. Caller Reader/fingerprint,
recheck/lock code and CLI remain byte-identical. Missing/rejected required inventory
remains UNAVAILABLE with no fabricated devices. Future times, backwards clocks and
rejection exactly at 2100 seconds remain protected. Identity, canonical IP, health,
liveness, public inventory, MQTT and every other runtime source remain unchanged.

### Regression and historical authority

Deterministic fixtures cover Z, -06:00, positive offsets, equal instants, fresh
offset inventory, raw identity, UTC output schema, exclusive 2100-second deadline,
future/backwards time, naive/malformed offsets, calendar/time errors, exact hostname
pairing and confirmed PE-5 handoff. Existing privacy/provenance/caller tests remain.
The accepted design requires a full native suite for product source changes.
Focused timestamp, PE-6 contract/caller, affected cross-phase and full native tests
must all pass before publication; exact observed totals are retained in the commit
and Evidence Report. Environment skips are not passes or Linux production proof.

PE-6.1/6.2/6.3 original validators and authoritative constants remain unchanged.
Historical PE-6.3 replays its exact accepted Git bytes, original three-path scope,
installed-source hashes and full/status interfaces. The fresh current correction
owns exactly five paths: classification.py, its existing product test, the existing
implementation-binding test and these two documents. Existing PE-4/PE-5 consumers
continue delegating to the current successor map. Every other accepted artifact,
old governance record/schema and executable remains byte/blob/mode-identical.
New current validation checks scope/index/modes, exact correction source/test
identities, document changes, protected files and publication lineage afresh.
Only immutable Git snapshots/replays are cached. New negatives protect historical
identity/authority against current substitution and false production acceptance.

### Required next operator-only action and retained limitations

No PI3/PI5, HA, MQTT, credential or production access/mutation occurred. The accepted
PE-6.3 installed classification.py SHA-256 remains historically
29b33e0ac6ad06b7b8eb360f10e9403ffb29993830eee16e21ff1b448bfd7f1c.
It does not prove current runtime bytes. Corrected artifact deployment and production
execution are NOT ESTABLISHED. PE-6.4 is NOT CLOSED; PE-6 remains IN_PROGRESS.
The previously reported runtime/source inventory.py difference and limited three-AST
comparison remain unresolved full-compatibility warnings. No inventory replacement,
threshold change, scheduled activation or automatic follow-on is authorized.

Next requires separate operator authorization: fast-forward the clean PI3 release
source checkout to the published correction commit, verify its exact tree and
classification.py Git blob/SHA-256, and prepare a guarded one-file replacement of
/home/jazofv1/hioc/pi4/lib/hioc/classification.py from that source. First establish
current runtime-use conditions and match the historical installed classifier hash,
ordinary path/parent identities, UID:GID 1000:1000, mode 0600 and single link; stop
on drift or unresolved use. Preserve exact old bytes and metadata as a private,
non-overwriting rollback backup, then replace only this artifact atomically with
verified corrected bytes, preserving ownership/mode and rechecking destination
hash/identity and all other PE-6 artifacts/dependencies. Do not execute classification,
change inventory, scheduling or services. Deployment receipt must be accepted before
separately authorized bounded PE-6.4 execution. This describes the next gate; it is
not an operator deployment command or authorization to perform it now. STOP.
