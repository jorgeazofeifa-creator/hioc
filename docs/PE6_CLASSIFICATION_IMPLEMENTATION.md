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
