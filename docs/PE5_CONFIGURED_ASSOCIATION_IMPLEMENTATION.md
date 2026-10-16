# PE-5.3 Configured Association Repository Implementation

Classification: HISTORICAL_INTENTIONALLY_PRESERVED PE-5.3 completion snapshot. PE5_3_STATUS=COMPLETE_REPOSITORY_IMPLEMENTATION.
Baseline: 72e878f9c0c8f5d3fe6357979e045943f3cf9d34.
Next: PE-5.4 - PI3 Release Source Synchronization; NOT STARTED.
PE-5 is IN_PROGRESS; PE-5.1 remains accepted. No production authority is granted.

## Frozen authority and components

[PE-5.2 design](PE5_MAPPING_CONTRACT_DESIGN.md) and the unchanged atomic correction
record/schema govern all input/output/metadata fields. The three exact schemas are
deterministically embedded in configured_association_schemas.py. No runtime source
configuration or generated state is committed. Original PE-5.3 STOP evidence remains
in the protected correction record; it was corrected before implementation.

configured_association.py performs strict bounded UTF-8/duplicate-key/nonfinite-number
rejection, closed source validation, revision checks, stable domain-separated IDs,
strong existing-device/MAC binding, service-owner validation, explicit per-row
rejections, deterministic ordering and private combined output validation. It uses
the accepted PE-5.1 pure resolver unchanged. No identity, IP, observation, liveness,
health, public inventory or PE-6 classification authority is added.

configured_association_store.py is a POSIX-only filesystem writer/reader using
anchored directory descriptors, no-follow regular single-link files, exact private
0700 directories and 0600 files owned by jazofv1, bounded reads and file fingerprints,
input checks immediately before output replacement, and one nonblocking shared
fcntl.flock held for the entire transaction. Unsupported native capabilities fail
closed. It reads only finalized inventory; it never executes the inventory engine.

## Persistence and explicit recovery

Each primary has one private bounded durability sidecar with the exact closed schema.
Publication validates inputs/confirmed anchors, resyncs surviving confirmation,
durably records PENDING with the prior confirmed descriptor, writes/fsyncs an exclusive
owned temporary file, replaces primary once, fsyncs its parent, then persists CONFIRMED.
Owned uncommitted temps are cleaned safely; unrelated/crash temp files are never used.

Pre-replacement failure preserves prior primary bytes when present. A successful
primary replace followed by parent-sync failure returns WRITE_FAILED with
INDETERMINATE_DURABILITY: new bytes may be visible, old physical presence is not
guaranteed, PENDING retains the prior logical descriptor and no rollback occurs.
Confirmation-metadata failure separately returns CONFIRMATION_METADATA_UNCONFIRMED.
A surviving CONFIRMED witness records already completed primary durability, not its
own future directory-sync success. A surviving PENDING witness blocks affected use.

Normal invocations refuse missing/malformed/mismatched confirmation or corrupt output.
Operator-approved recertification revalidates recorded candidate/prior binding and
current consumption rules, resyncs existing bytes/parent and confirms metadata without
replacing primary or refreshing timestamps. Unmatched/missing/corrupt state requires
explicit fresh producer recovery or approved initialization, never automatic adoption.
Different source content during pending recovery must exceed retained revision floors.

Source uncertainty blocks configured evidence, preserving the independently valid
local branch only when the output itself is confirmed and its unchanged gates pass.
Whole-unavailable output contains no consumable branch and no fabricated removals.
No application payload LKG/archive, hidden old relationship store or new backup job exists.

## Interfaces and execution boundary

hioc-compose-service-associations.py has fixed production root and paths, no CLI/env
root, configuration or secret overrides. It uses UTC system time, accepted inventory
policy 2100 seconds, handoff horizon 1200 seconds, no catch-up/retry loop, and fixed
safe status/error/phase/count diagnostics without private identifiers or labels.
hioc-install-mqtt-mappings.py requires explicit operator approval and a private
secret-free candidate file for install; initialization/fresh recovery are explicit.
Its recertify source/output and recompute-output actions require approval and the
same lock. They are future operator operations, not executed by this checkpoint.

deploy/pe5-service-associations.cron.disabled contains only commented configuration:
2,17,32,47 * * * * with the fixed absolute composer path, under jazofv1.
It is not an active crontab. PE-5.5 deployment must leave it disabled; PE-5.7 owns
separate conditional activation. No transaction, source sync or deployment occurs here.

## Private PE-6 handoff

Store.read_handoff holds the shared lock, requires a bound CONFIRMED output, validates
closed shape/semantics and deadline, and verifies the same current inventory and
configured source/durability binding where the configured branch claims VALID.
Expired, changed, missing, corrupt or unconfirmed evidence is unavailable.
Configured provenance remains distinct from future Discovery; no live MQTT/broker,
client/topic/retained-message, HA, DNS/HTTP/socket/SSH or credential reader is introduced.

## Deployment readiness and limits

The exact six-item payload with source/destination/mode/owner/SHA256/Git blob is bound
in governance/pe5/pe5-configured-association-implementation.json. Modules are 0644;
entrypoints 0755; the disabled cron reference 0644. Owner jazofv1 is resolved on the
target, never assumed from current production observations. CPython 3.10 is the
repository language floor; POSIX no-follow directory descriptors, fsync and flock are
mandatory. Existing PE-5.1 and inventory dependencies remain protected installed
prerequisites. Deployment must independently verify them and interpreter capabilities.

Required future private directories: config/enrichment and
state/enrichment/service_associations, owner jazofv1 mode0700. Runtime source/output,
sidecars and lock are private0600. Existing source is preserved; no empty source is
automatically created. Unexpected targets stop disabled deployment; backup/rollback
prerequisites remain a separately accepted PE-5.5 procedure. No PE-4 journal is touched.
Rollback of deployment payload is distinct from prohibited automatic primary rollback.

Controlled Windows fixtures use real temporary-file read/write/fsync/replace with
injected POSIX metadata, directory-sync and flock outcomes. These establish repository
semantics, not native PI3 crash, ownership, locking or power-loss evidence. Native
bounded validation remains PE-5.6 and operational evidence PE-5.8; PE-5.9 final closure
and PE-6 interpretation remain later checkpoints.

## Implementation coverage

- A: operator-managed configured mapping source; configured_association.validate_source; store.install_source; schema/approval/install tests.
- B: mapping source path/domain; store.SOURCE; installer CLI; fixed-path/env/symlink tests.
- C: mapping schema; configured_association.input_schema; exact embedded schema + schema mutants.
- D: configuration revision; check_revision; install_source; rollback/equal-content/no-anchor tests.
- E: opaque endpoint IDs; validate_source; identifier tests.
- F: reconciled device IDs; resolve_configured; missing/weak/collision/ID mismatch tests.
- G: relationship meaning; resolve_configured; descriptive-only fields tests.
- H: stable relationship IDs; relationship_id; domain tuple/hash/revision invariance tests.
- I: source provenance; resolve_configured; source_id/revision/digest tests.
- J: rule provenance; resolve_configured; fixed rule_id tests.
- K: duplicates; validate_source; duplicate row/ID/endpoint tests.
- L: conflicts; validate_source; conflicting endpoint/permutation tests.
- M: missing endpoints; resolve_configured; no probing; missing targets/services tests.
- N: malformed config; strict_json; validate_source; duplicate keys/UTF8/NaN/extra fields/bounds.
- O: privacy; schemas; CLI safe diagnostics; no labels/IDs in logs; private modes.
- P: secrets prohibited; schemas; CLI; forbidden fields/no config reader/static review.
- Q: topic handling; closed schema; topic/client/URL reject tests.
- R: no live MQTT; pure resolver; filesystem runner; network guard + import/call AST.
- S: private output; compose; accepted/rejected branch cases.
- T: output schema; validate_envelope; schema + semantic corruption cases.
- U: output path/domain; store.OUTPUT; fixed path tests.
- V: source/output separation; store; source untouched by composer; output ownership.
- W: persistence; store; read/restart tests.
- X: atomic writes; Store.atomic/Store.publish; fsync/replace/failure/input race tests.
- Y: permissions/ownership; PosixFS; UID/GID/mode/link/path guards.
- Z: current/history; compose; store; one current receipt; no archive tests.
- AA: retention; Store.atomic/Store.publish cleanup; handled failure cleanup/crash temp non-use.
- AB: LKG/recovery; Store.composer recovery gate; no stale promotion; explicit recovery tests.
- AC: corruption; strict_json; validate_envelope; sticky prior corruption/source corruption tests.
- AD: recurrence; composer CLI; disabled cron; standalone/no engine invocation.
- AE: trigger/cadence; cron.disabled; exact four slots; no active scheduler.
- AF: locking; PosixFS.lock; flock nonblocking lifecycle tests.
- AG: overlap; Store.composer; skip/no output replace tests.
- AH: missed execution; validate_handoff; expiry/no catch-up tests.
- AI: failure; safe errors/unavailable receipt; nonzero/fixed diagnostics/write failures.
- AJ: restart; Store.composer; missing/valid unavailable/corrupt cases.
- AK: observability; CLI; safe fixed status/error/counters.
- AL: PE-6 handoff; validate_handoff; read_handoff; source/input/digest/deadline tests.
- AM: source/runtime separation; payload manifest; no actual mapping/state payload.
- AN: identity boundary; pure resolution; deepcopy inventory unchanged.
- AO: IP boundary; closed rows; no IP fields/overwrite tests.
- AP: observation/liveness; closed rows; no timestamp/liveness promotion.
- AQ: health boundary; closed rows; no health inference.
- AR: public projection; separate output path; public writer/module unchanged.
- AS: MQTT compatibility; additive modules; existing publisher artifacts unchanged.
- AT: future Discovery provenance; source_kind const; reject discovered kind/no subscriber.


## Historical PE-5.6 production-found initial infrastructure correction

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

### Exact bootstrap authority and security

Only install --approved --initialize without --fresh-recovery may bootstrap.
The source schema is validated before any bootstrap syscall. Existing root,
config and state directories must be owned by jazofv1, have owner rwx and no
group/world write bits; config0755 is accepted. They are never created or repaired.
The only creatable paths are config/enrichment, state/enrichment and
state/enrichment/service_associations, each exact0700, owner jazofv1.
Anchored mkdir/open with dir_fd and O_DIRECTORY|O_NOFOLLOW validates each opened
directory, its visible identity and held ancestor identities. Existing wrong-owner,
wrong-mode, symlink or non-directory paths fail closed; no chmod/chown repair.
Concurrent mkdir EEXIST is accepted only after the same full validation.
Directory and parent fsync certify each entry before opening the shared0600 lock.
Held anchors are revalidated before source replacement. Failure may leave safe empty
directories; no automatic directory or primary rollback is introduced.
INITIALIZATION_INFRASTRUCTURE_FAILED reports mkdir/fsync/open failure; an absent
lock parent outside initialization retains LOCK_UNAVAILABLE, never OVERLAP_SKIPPED.
Actual nonblocking flock contention still returns OVERLAP_SKIPPED.
Composer, handoff, recertify, output recompute and fresh source recovery have no
missing-directory creation authority. Publication PENDING/primary/CONFIRMED,
single replacement, explicit recovery, revision and privacy semantics are unchanged.

### Deployment impact and evidence limits

Compare against accepted PE-5.3 commit 348f9787ae0ab364570a2ba07ada9527fc8db0e2:
only pi4/lib/hioc/configured_association_store.py changes in the six-artifact payload.
The other five installed artifacts retain exact accepted bytes.
Intended replacement: /home/jazofv1/hioc/pi4/lib/hioc/configured_association_store.py,
owner/group jazofv1:jazofv1, mode0644. Exact final SHA256/blob is recorded in the existing
implementation governance payload. The historical PE-5.3 manifest remains available
from its immutable commit. No new checkpoint or governance hierarchy is introduced.
Windows fixtures simulate POSIX ownership, directory fsync and flock; they are not
native PI3 crash or permission evidence. Corrected deployment and retry are separate
operator-controlled actions; no production correction or PE-5.6 closure is claimed.

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

### Sanitized operator evidence and exact durability identities

Source witness: CONFIGURED_MAPPING_SOURCE / CONFIRMED / candidate=null,
confirmed SHA256 961b72e8918606caeac565a8d472d03c4784d9a3b43eae6deb4085865330d295,
source_revision1, transaction_id dur_ae948c45234a43edbb4194d6c2052732.
Source: 241-byte regular0600 single-link UID/GID1000/1000, exact approved candidate.
Source-sidecar file SHA was not supplied; no independent byte-hash observation is claimed.

Output witness: GENERATED_RELATIONSHIP_OUTPUT / CONFIRMED / candidate=null,
confirmed SHA256 f1b219dc413325a557c71e3561804afcc3bdf26f87d2d6fdb71bb3e7c97f5e2c,
source_revision1, transaction_id dur_fe5cd411ccee4e328326e85d6c30c7ac.
Output: 4916-byte regular0600 single-link UID/GID1000/1000.
Output sidecar: 269-byte regular0600 single-link UID/GID1000/1000, SHA256
00169ad24bfa1bf9ec0619cd447125d5b0f860f425cb88bc80081f2b76498a1d.

Configured association evidence uses opaque IDs: endpoint
me_f14314f531e241e091b79ccc380323a2, mapping map_b90cf00b53ff4fc584716f2d4b531743,
existing device dev_703040cb07a3046f, service_id=null, direction endpoint_to_device.
This evidence is not a committed runtime configuration or generated output file.
Complete sanitized observation fields and the eight local service identifiers are
retained in production_validation of the existing governance record.
The later observed inventory SHA256 was
885af752b89d840ad8f1265a69bb6dbdc0f7e541e8a2c7b55d1ae87c4625a726,
updated 2026-10-14T11:00:01-06:00. No cause of its SHA difference is established.

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

### Pre-activation evidence scope

The disabled artifact was reported regular0644 jazofv1:jazofv1 links1 size184,
SHA256 70ef96a7913946fb5d381b1214739160daa3db5fd5f55f1e9f172539bdda1e67.
Composer: regular0755 jazofv1:jazofv1 links1,
SHA256 4f3aa3f2f60d33a995d328411b0fbf696aa5967ee9ac9c51c2eb7237a696bc18.
Before activation, source/source-sidecar/lock/output/output-sidecar were reported
regular0600 jazofv1:jazofv1 links1, sizes241/265/0/4916/269 respectively.
Source/output metadata were reported CONFIRMED, candidate=None, revision1, with
primary hashes matching the prior accepted PE-5.6 observations. These are
PRE-ACTIVATION observations, not claims of current post-activation file contents.
No new scheduler, deployment mechanism, evidence hierarchy or runtime behavior is introduced.

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

## Current PE-5.9 final closure and private PE-6 handoff

Classification: HISTORICAL_INTENTIONALLY_PRESERVED accepted PE-5.9 handoff snapshot. Phase 7A ACTIVE; PE5_STATUS=COMPLETE.
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

### Authority and original requirement reconciliation

The following 37 rows preserve the exact original requirement and checkpoint assignments
from governance/pe5/pe5-execution-roadmap.json. The original architecture is
c914cfc4dc39a90005bad42984396291f5b2a751:docs/PASSIVE_ENRICHMENT_ARCHITECTURE.md; original preparation f3730ba5a8745361934ff822a9c29c16c9d0767b:docs/PE5_IMPLEMENTATION_PREPARATION.md.
Each row is COMPLETE/PASS using existing behavior and accepted evidence, not merely
because its historical roadmap disposition was ASSIGNED. Production scope and limits
above apply to every row. Exact structured authorities and per-row current references
are in final_closure.coverage of the existing implementation record.

#### Requirement 1: local service ownership relationships

Status: COMPLETE/PASS. Assigned: PE-5.1.

Existing strong-MAC device and same-owner service references only; local schema 1.0 embedded unchanged.

Evidence: PE-5.1 accepted first execution; PE-5.6 bounded and PE-5.8 natural local eight/zero observations.
Validation: tests/test_pe5_local_service_association.py:LocalServiceAssociationTests.test_valid_systemd_strong_owner_existing_ids_and_provenance.

#### Requirement 2: systemd evidence

Status: COMPLETE/PASS. Assigned: PE-5.1.

systemd ownership is relationship evidence using existing stable service/device IDs.

Evidence: PE-5.1 accepted implementation and first execution.
Validation: tests/test_pe5_local_service_association.py:LocalServiceAssociationTests.test_valid_systemd_strong_owner_existing_ids_and_provenance.

#### Requirement 3: ss/listening-socket evidence

Status: COMPLETE/PASS. Assigned: PE-5.1.

ss/listening-socket input joins existing ownership; no network probe or live broker observation.

Evidence: PE-5.1 accepted implementation; existing inventory snapshot authority.
Validation: tests/test_pe5_local_service_association.py:LocalServiceAssociationTests.test_multiple_services_one_owner_and_all_ss_services.

#### Requirement 4: stable device binding

Status: COMPLETE/PASS. Assigned: PE-5.1.

Reject missing, weak, malformed or mismatched MAC-derived dev_ identities; no identity creation.

Evidence: PE-5.1 strong-owner resolver and PE-5.3 configured device rejection fixtures.
Validation: tests/test_pe5_local_service_association.py:LocalServiceAssociationTests.test_device_id_must_match_mac_derived_existing_id.

#### Requirement 5: stable relationship identifiers

Status: COMPLETE/PASS. Assigned: PE-5.2, PE-5.3, PE-5.6, PE-5.8, PE-5.9.

Deterministic domain-separated semantic relationship identity; source revision/mapping row label/evaluation do not change identity.

Evidence: PE-5.3 implementation accepted; local:test_ids_stable_across_snapshot_cycles.
Validation: tests/test_pe5_configured_association_implementation.py:ConfiguredResolutionTests.test_relationship_id_exact_domain_and_revision_invariance.

#### Requirement 6: source provenance

Status: COMPLETE/PASS. Assigned: PE-5.2, PE-5.3, PE-5.6, PE-5.8, PE-5.9.

Private source kind, source_id, source revision and digest identify declared configuration; local consumed provenance retained.

Evidence: PE-5.6 configured association and PE-5.8 stable source receipts.
Validation: tests/test_pe5_configured_association_implementation.py:ConfiguredResolutionTests.test_valid_configured_opaque_strong_owner_private_provenance.

#### Requirement 7: rule provenance

Status: COMPLETE/PASS. Assigned: PE-5.2, PE-5.3, PE-5.6, PE-5.8, PE-5.9.

Private rule_id declared_endpoint_device_v1 and unchanged local rule provenance explain relationships.

Evidence: PE-5.3 closed schemas and deterministic rule implementation.
Validation: tests/test_pe5_configured_association_implementation.py:ConfiguredResolutionTests.test_preserves_exact_local_foundation.

#### Requirement 8: configured MQTT mappings

Status: COMPLETE/PASS. Assigned: PE-5.2, PE-5.3, PE-5.6, PE-5.8, PE-5.9.

Explicit approved offline source installation, closed schema and bounded rows; configuration is not observation.

Evidence: PE-5.6 corrected source installation accepted once; PE-5.8 configured one/zero.
Validation: tests/test_pe5_configured_association_implementation.py:ConfiguredResolutionTests.test_valid_configured_opaque_strong_owner_private_provenance.

#### Requirement 9: MQTT association evidence

Status: COMPLETE/PASS. Assigned: PE-5.2, PE-5.3, PE-5.6, PE-5.8, PE-5.9.

Declared opaque MQTT endpoint-to-device relationship only; no broker/client/topic telemetry required.

Evidence: PE-5.2 corrected contract mqtt requirements false; PE-5.3 synthetic validation.
Validation: tests/test_pe5_configured_association_implementation.py:ConfiguredResolutionTests.test_closed_source_rejects_secrets_topics_authority_fields.

#### Requirement 10: mapping source authority

Status: COMPLETE/PASS. Assigned: PE-5.2.

Private operator configuration is mapping authority; no unseen production store presumed.

Evidence: PE-5.2 absent-source observation and approved design; PE-5.6 created source receipt.
Validation: tests/test_pe5_configured_association_implementation.py:PersistenceTests.test_approval_and_explicit_initialization_required.

#### Requirement 11: mapping producer authority

Status: COMPLETE/PASS. Assigned: PE-5.2.

Approved installer is source writer; standalone composer is output writer; owner jazofv1.

Evidence: PE-5.5 accepted disabled six-artifact installation; PE-5.6 corrected installer acceptance.
Validation: tests/test_pe5_configured_association_implementation.py:PersistenceTests.test_source_output_separation_and_confirmed_handoff.

#### Requirement 12: mapping identifier semantics

Status: COMPLETE/PASS. Assigned: PE-5.2.

Opaque me_ and map_ 32-hex IDs, existing dev_ 16-hex and optional same-owner existing service.

Evidence: Frozen PE-5.2 input schema and PE-5.3 parser.
Validation: tests/test_pe5_configured_association_implementation.py:ConfiguredResolutionTests.test_unknown_schema_and_identifiers.

#### Requirement 13: mapping relationship semantics

Status: COMPLETE/PASS. Assigned: PE-5.2.

Source-scoped endpoint/device/service semantics; sorted deterministic rows and fan-in, no arbitrary dependency inference.

Evidence: PE-5.2 corrected relationship contract.
Validation: tests/test_pe5_configured_association_implementation.py:ConfiguredResolutionTests.test_deterministic_multirow_sorting_and_fan_in.

#### Requirement 14: mapping freshness

Status: COMPLETE/PASS. Assigned: PE-5.2.

Source configuration has revision, not liveness timestamp/TTL; output freshness comes from inventory/evaluation.

Evidence: PE-5.2 revision contract; PE-5.8 source revision1 unchanged.
Validation: tests/test_pe5_configured_association_implementation.py:ConfiguredResolutionTests.test_revision_rollback_equal_changed_and_equal_identical.

#### Requirement 15: mapping expiry

Status: COMPLETE/PASS. Assigned: PE-5.2.

Current output expires at min(evaluation+1200, inventory.updated+2100); now >= deadline rejects.

Evidence: PE-5.1 policy2100 preserved; PE-5.8 observed bounded deadlines.
Validation: tests/test_pe5_configured_association_implementation.py:ConfiguredResolutionTests.test_inventory_clock_freshness_and_deadline.

#### Requirement 16: duplicate handling

Status: COMPLETE/PASS. Assigned: PE-5.2, PE-5.3, PE-5.6, PE-5.8, PE-5.9.

Identical consumed local duplicates deduplicate; configured duplicate mapping/endpoint rows reject under closed source contract.

Evidence: local:test_identical_consumed_duplicates_deduplicate_without_rejection.
Validation: tests/test_pe5_configured_association_implementation.py:ConfiguredResolutionTests.test_duplicate_rows_ids_and_endpoints.

#### Requirement 17: conflict handling

Status: COMPLETE/PASS. Assigned: PE-5.2, PE-5.3, PE-5.6, PE-5.8, PE-5.9.

Conflicting endpoint/device declarations reject whole configured source; conflicting local service ownership rejects ambiguous IDs.

Evidence: local:test_conflicting_service_ownership_rejects_all_same_id.
Validation: tests/test_pe5_configured_association_implementation.py:ConfiguredResolutionTests.test_conflicting_endpoint_rejects_whole_source.

#### Requirement 18: missing endpoint handling

Status: COMPLETE/PASS. Assigned: PE-5.2, PE-5.3, PE-5.6, PE-5.8, PE-5.9.

Unknown device/service rejected; missing/invalid source does not fabricate relationships or absence; independent local branch remains available.

Evidence: PE-5.2 source-state semantics and device/service rejection fixtures.
Validation: tests/test_pe5_configured_association_implementation.py:ConfiguredResolutionTests.test_absent_or_invalid_source_keeps_independent_local.

#### Requirement 19: privacy

Status: COMPLETE/PASS. Assigned: PE-5.2, PE-5.3, PE-5.6, PE-5.8, PE-5.9.

Private source/output/sidecars owner-restricted, opaque metadata only; public inventory and protected contracts unchanged.

Evidence: PE-5.6 bounded five-term inventory search only; protected 226 artifact check.
Validation: tests/test_pe5_configured_association_implementation.py:ConfiguredResolutionTests.test_network_subprocess_and_input_authority_untouched.

#### Requirement 20: credentials/secrets

Status: COMPLETE/PASS. Assigned: PE-5.2, PE-5.3, PE-5.6, PE-5.8, PE-5.9.

No credentials are required by declared-source design; closed fields reject secrets and unsafe free text.

Evidence: PE-5.2 broker/HA/credential requirements explicitly false; no access this checkpoint.
Validation: tests/test_pe5_configured_association_implementation.py:ConfiguredResolutionTests.test_closed_source_rejects_secrets_topics_authority_fields.

#### Requirement 21: topic leakage prevention

Status: COMPLETE/PASS. Assigned: PE-5.2, PE-5.3, PE-5.6, PE-5.8, PE-5.9.

Opaque endpoints and closed schemas prohibit topics, payloads, discovery internals and raw broker identifiers.

Evidence: PE-5.3 privacy fixtures and protected public projection.
Validation: tests/test_pe5_configured_association_implementation.py:ConfiguredResolutionTests.test_closed_source_rejects_secrets_topics_authority_fields.

#### Requirement 22: no identity authority

Status: COMPLETE/PASS. Assigned: PE-5.2, PE-5.3, PE-5.6, PE-5.8, PE-5.9.

Consume existing strong identity only; relationship evidence cannot assign identity.

Evidence: local:test_device_id_must_match_mac_derived_existing_id.
Validation: tests/test_pe5_configured_association_implementation.py:ConfiguredResolutionTests.test_device_rejections.

#### Requirement 23: no canonical-IP authority

Status: COMPLETE/PASS. Assigned: PE-5.2, PE-5.3, PE-5.6, PE-5.8, PE-5.9.

No canonical address mutation or preference from transport; input snapshot remains unchanged.

Evidence: local:test_inputs_all_protected_fields_unchanged_and_no_data_leaks.
Validation: tests/test_pe5_configured_association_implementation.py:ConfiguredResolutionTests.test_network_subprocess_and_input_authority_untouched.

#### Requirement 24: no liveness authority

Status: COMPLETE/PASS. Assigned: PE-5.2, PE-5.3, PE-5.6, PE-5.8, PE-5.9.

No service/MQTT transport evidence confers observation, presence or liveness; empty local collections are not successful collection.

Evidence: Frozen PE-5.2 forbidden authority boundaries.
Validation: tests/test_pe5_local_service_association.py:LocalServiceAssociationTests.test_empty_collections_do_not_assert_health_success_or_absence.

#### Requirement 25: no health authority

Status: COMPLETE/PASS. Assigned: PE-5.2, PE-5.3, PE-5.6, PE-5.8, PE-5.9.

Transport/relationship does not confer health, expected availability or asset/role classification.

Evidence: PE-5.2 forbidden authority; PE-6 responsibility remains future.
Validation: tests/test_pe5_configured_association_implementation.py:ConfiguredResolutionTests.test_closed_source_rejects_secrets_topics_authority_fields.

#### Requirement 26: bounded diff

Status: COMPLETE/PASS. Assigned: PE-5.2, PE-5.3, PE-5.6, PE-5.8, PE-5.9.

Bounded deterministic added/removed change summary from comparable valid prior result; unavailable prior does not fabricate removals.

Evidence: configured:test_bounded_change_fields_checked.
Validation: tests/test_pe5_configured_association_implementation.py:ConfiguredResolutionTests.test_current_comparison_and_unavailable_do_not_fabricate_removals.

#### Requirement 27: unchanged publish/subscribe behavior

Status: COMPLETE/PASS. Assigned: PE-5.2, PE-5.3, PE-5.6, PE-5.8, PE-5.9.

No new subscribe/publish/runtime public fields; MQTT Discovery and live telemetry explicitly deferred.

Evidence: Unchanged protected MQTT/public schemas and publisher artifacts.
Validation: tests/test_pe5_configured_association_implementation.py:EntrypointAndGovernanceTests.test_static_no_network_shell_credentials_public_mutation.

#### Requirement 28: persistence requirement

Status: COMPLETE/PASS. Assigned: PE-5.2.

Shared private current output plus bounded exact durability sidecars required; one primary replace and explicit approval.

Evidence: PE-5.2 corrected atomic contract; PE-5.6 confirmed native bounded output.
Validation: tests/test_pe5_configured_association_implementation.py:PersistenceTests.test_exact_atomic_order_and_one_primary_replace.

#### Requirement 29: recurring execution decision

Status: COMPLETE/PASS. Assigned: PE-5.2.

Independent recurring composer required, activated once; three natural consecutive successful windows accepted.

Evidence: PE-5.7 activation and PE-5.8 20:17/20:32/20:47 operator receipts.
Validation: tests/test_pe5_configured_association_implementation.py:PersistenceTests.test_overlap_nonblocking_no_output_replace.

#### Requirement 30: producer/inventory integration decision

Status: COMPLETE/PASS. Assigned: PE-5.2.

Standalone producer only; no inventory engine hook or hidden caller side effect; existing local caller retained.

Evidence: PE-5.2 independent execution contract; protected payload/engine invariants.
Validation: tests/test_pe5_configured_association_implementation.py:EntrypointAndGovernanceTests.test_static_no_network_shell_credentials_public_mutation.

#### Requirement 31: retention decision

Status: COMPLETE/PASS. Assigned: PE-5.2.

Only current primary and bounded sidecar descriptors; no archive/payload last-known-good replay; stale temporary files not adopted.

Evidence: PE-5.2 approved retention and explicit recovery disposition.
Validation: tests/test_pe5_configured_association_implementation.py:PersistenceTests.test_no_stale_temp_or_hidden_payload_lkg_consumed.

#### Requirement 32: deployment

Status: COMPLETE/PASS. Assigned: PE-5.4, PE-5.5.

Accepted disabled installation plus bounded one-artifact store correction; no deployment performed for PE-5.9.

Evidence: PE-5.6 production_validation.corrected_deployment and source identity receipts; original six-artifact acceptance in 4990c62 Master Plan.
Validation: tests/test_pe5_configured_association_implementation.py:InitialInfrastructureTests.test_composer_cannot_bootstrap.

#### Requirement 33: bounded production validation

Status: COMPLETE/PASS. Assigned: PE-5.6, PE-5.8.

Approved initial source once and composer once accepted; synthetic faults allowed by contract; no repeated first execution.

Evidence: PE-5.6 production_validation, preserved bootstrap failure and corrected acceptance.
Validation: tests/test_pe5_configured_association_implementation.py:PersistenceTests.test_post_replace_parent_failure_indeterminate_no_rollback.

#### Requirement 34: independent acceptance

Status: COMPLETE/PASS. Assigned: PE-5.3, PE-5.6, PE-5.8, PE-5.9.

Repository validation and concise independent acceptance; OPERATOR_SUPPLIED operational evidence accepted at immutable predecessor closures.

Evidence: PE-5.6/7/8 immutable closure commits and present PE-5.9 independent Git-object acceptance.
Validation: tests/test_pe5_configured_association_implementation.py:EntrypointAndGovernanceTests.test_exact_implementation_contract_scope_and_payload.

#### Requirement 35: operational documentation

Status: COMPLETE/PASS. Assigned: PE-5.2, PE-5.9.

Current Master Plan, operations/data model/deployment/reference and roadmap synchronized; historical receipts retained.

Evidence: Existing 17-path PE-5.9 documentation/governance scope; canonical docs/CHANGELOG.md.
Validation: tests/test_pe5_configured_association_implementation.py:FinalClosureTests.test_complete_ledger_handoff_and_sequence.

#### Requirement 36: final PE-5 closure

Status: COMPLETE/PASS. Assigned: PE-5.9.

All 37 original requirements, 11 resolved UNKNOWN rows and 14 DoD conditions evaluated; closure only through gated validation/publication.

Evidence: PE-5.9 final_closure and published commit verification; PE-5.8 predecessor preserved.
Validation: tests/test_pe5_configured_association_implementation.py:FinalClosureTests.test_complete_ledger_handoff_and_sequence.

#### Requirement 37: PE-6 handoff readiness

Status: COMPLETE/PASS. Assigned: PE-5.2, PE-5.3, PE-5.8, PE-5.9.

Exact private file/API, schemas, identities, confirmation, time, failure and authority gates established; PE-6 implementation requires separate authorization.

Evidence: Frozen PE-5.2 corrected contract, PE-5.3 implementation, accepted PE-5.6/7/8 evidence and PE-5.9 handoff.
Validation: tests/test_pe5_configured_association_implementation.py:FinalClosureTests.test_reject_unconfirmed_reader_or_pe6_start.

### All eleven original UNKNOWN resolutions

1. **RESOLVED — source/store existence and location, producer/owner authority, identifier and relationship semantics** (PE-5.2). Corrected PE-5.2 contract establishes private source paths and writers; earlier absent source observation is historical, PE-5.6 approved source creation accepted.

2. **RESOLVED — meaningful timestamps versus configuration version, freshness/expiry/conflict/privacy and secret handling** (PE-5.2). PE-5.2 immutable revision/configuration versus evaluation/inventory time distinction, expiry/conflict/privacy contract and PE-5.3 tests.

3. **RESOLVED — whether shared private storage is required for PE-5 completion; exact artifact/schema/ownership/permissions/atomic writes/readers/writers/current versus history/retention/LKG/restart/corruption** (PE-5.2). PE-5.2 corrected atomic durability contract; PE-5.3 implementation and PE-5.6 bootstrap correction/accepted private store.

4. **RESOLVED — whether recurring execution is required; trigger/cadence/independent versus inventory or other producer integration/locking/missed execution/restart/failure** (PE-5.2). PE-5.2 independent recurring composer disposition; PE-5.7 accepted activation and PE-5.8 natural cycles.

5. **RESOLVED — exact private file/API/schema/version/freshness/conflict handoff to PE-6** (PE-5.2). Unchanged accepted private schemas plus complete PE-5.9 handoff; PE-6 implementation not required for readiness.

6. **RESOLVED — exact commit, parent/subject/scope; source main/origin clean and synchronized** (PE-5.4). Accepted source synchronization recorded in 4990c62 Master Plan and PE-5.6 source identity receipts; Git commit ancestry independently readable.

7. **RESOLVED — exact installed identities and metadata; inactive activation state; current prerequisites and provenance-bound rollback** (PE-5.5). 4990c62 Master Plan records accepted disabled six-artifact deployment; PE-5.6 bounded correction establishes exact changed store identity. No new full installed-byte receipt is claimed.

8. **RESOLVED — direct native mapping evidence/output identity, bounds, missing/duplicate/conflict cases and approved store/restart/corruption behavior where applicable** (PE-5.6). PE-5.6 once-only approved installation/composition receipts; bounded output/schema validation and accepted synthetic duplicate/conflict/fault cases; native crash not established.

9. **RESOLVED — activation necessity/mechanism already approved by PE-5.2; exact activation result or not-required receipt** (PE-5.7). PE-5.7 accepted one marker/entry/cadence/command identity; no manual producer at activation.

10. **RESOLVED — natural-cycle/overlap/missed-cycle/staleness/failure evidence required by contract; independent production acceptance** (PE-5.8). PE-5.8 accepted three natural cycles and synthetic overlap/missed/expiry/failure disposition; operator-only/full-bytes/current-freshness limits preserved.

11. **RESOLVED — complete coverage/evidence ledger; private handoff contract and operational documents; no unknown completion requirements** (PE-5.9). Present complete 37-row ledger, 14 DoD evaluations, private handoff and synchronized current docs; publication remains a mandatory final verification gate.

### Fourteen individual Definition of Done decisions

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

### Complete private PE-6 handoff

These are accepted existing PE-5.2/3 contracts, not a schema redesign or PE-6 authorization.

- **authority**: 72e878f9c0c8f5d3fe6357979e045943f3cf9d34:governance/pe5/pe5-atomic-durability-contract-correction.json
- **producer**: Approved offline installer writes source; standalone recurring composer writes output; never inventory engine or caller hook.
- **consumer**: Future PE-6 private relationship reader only; no current PE-6 implementation or runtime authorization.
- **root**: /home/jazofv1/hioc
- **source**: config/enrichment/mqtt_mappings.json
- **source_metadata**: config/enrichment/mqtt_mappings.durability.json
- **output**: state/enrichment/service_associations/current.json
- **output_metadata**: state/enrichment/service_associations/current.durability.json
- **inventory**: state/inventory/inventory.json
- **lock**: state/enrichment/service_associations/.lock
- **versions**: {"durability": "1.0", "local": "1.0", "output": "2.0", "source": "1.0"}
- **schema_authority**: {"input_schema": "c4ca34ae123617769d25a694d55f50473d7f69670974e6cfae2a9607e9bbe6c4", "metadata_schema": "18c041c4d2dafb3d7420260a5fe4fc8edf8aee6759253a9f4ad8e8683a75972c", "output_schema": "c2e33c2cbaa1c26d73f153a5dcd4be224c96b682e793a6b751f3d63d9ed6bba6"}
- **source_id**: operator_mqtt_v1 (exact schema constant)
- **source_fields**: ["schema_version", "source_id", "revision", "mappings"]
- **mapping_fields**: ["mapping_id", "endpoint_id", "device_id", "service_id"]
- **output_fields**: ["changes", "configured", "evaluated_at", "inventory", "local", "schema_version", "state", "valid_until"]
- **local_state_field_defined**: false
- **permissions**: Private parents 0700; regular nonlink single-link files 0600; owner jazofv1, accepted operator UID/GID1000/1000. Future consumer must enforce safety; no permission change here.
- **bounds**: {"mapping_rows": 4096, "metadata_bytes": 8192, "output_bytes": 16777216, "source_bytes": 262144}
- **identifiers**: Opaque endpoint me_[0-9a-f]{32}; row map_[0-9a-f]{32}; existing strong dev_[0-9a-f]{16}; optional existing same-owner service.
- **relationship_identity**: mqra_ + SHA256(ASCII canonical JSON array ['configured_mqtt_v1',source_id,endpoint_id,device_id,service_id,'endpoint_to_device']); excludes revision, mapping_id and evaluation.
- **provenance**: source_kind configured_mqtt, rule_id declared_endpoint_device_v1; source_id/revision/digest/mapping_id remain private. Local schema unchanged.
- **revision**: Integer 1..9007199254740991, never bool; approved content changes increment revision; rollback or equal revision with changed content rejected; PENDING recovery floors enforced. No source TTL/observed_at/mtime authority.
- **cadence**: 2,17,32,47 * * * *; independent composer every900 seconds, no catch-up/retry
- **command**: /usr/bin/python3 /home/jazofv1/hioc/pi4/bin/hioc-compose-service-associations.py
- **freshness**: Inventory age <=2100 seconds with accepted clock rules; output valid_until=min(evaluated_at+1200,inventory.updated+2100). Reject at now>=valid_until and on future/backward clock or changed consumed inventory/source identity.
- **reader_api**: hioc.configured_association_store.Store.read_handoff(evaluated_at)
- **reader_lock_may_create_file**: true
- **reader_lock_note**: Store.lock() uses nonblocking exclusive flock and may create missing .lock in approved private parent. Existing API is not a filesystem-pure read; future PE-6 must explicitly govern reader/lock lifecycle. Do not call it in PE-5.9.
- **required_output_confirmation**: CONFIRMED matching current output digest/domain/revision, closed schema, stable read fingerprint; reject PENDING/missing/malformed/mismatched sidecar.
- **configured_valid_requires_confirmed_source**: true
- **source_confirmation**: For configured VALID require CONFIRMED current source digest/revision and final source/output rechecks under lock. Root VALID alone does not establish all branches valid.
- **missing_and_errors**: Absent/invalid source may preserve independent local output only with confirmed current output and valid current inputs/schema/time; local null is unavailable, not empty/success. Explicit empty source is known-empty; reject conflicting/duplicate or unknown-owner configured rows per contract.
- **durability**: PENDING barrier -> exclusive temporary write/file fsync -> one primary replace -> parent fsync -> CONFIRMED sidecar/file/parent barriers. Pre-replace failure preserves prior; post-replace parent failure is INDETERMINATE/WRITE_FAILED, not rollback success.
- **recovery**: Only separately approved recertification of exact recorded candidate/prior, fsync without primary replacement or time refresh; unmatched/corrupt bytes stop. Fresh producer recomputation is separate approved action.
- **retention**: One current primary per domain and bounded sidecar descriptors; no archive/application-payload LKG replay. Stale crash temporaries never adopted; cleanup not authorized.
- **private_only**: true
- **prohibited_authority**: ["identity", "canonical_ip", "observation", "liveness", "health", "asset_classification", "operator_role"]
- **public_boundary**: No raw private source/output/endpoint/topic/credential exposure, public schema change, publication/subscription or inference of MQTT broker health.
- **pe6_responsibility**: Separately authorized explainable classification/role_suggestion/metadata_quality design and validation; protect operator_role, provenance/privacy/time/rejection and reader-lock lifecycle; no automatic promotion of relationships.

### Production provenance, recovery and deferred work

PE-5.6 corrected installation and bounded execution; PE-5.7 single-entry activation;
PE-5.8 three consecutive natural cycles remain accepted OPERATOR_SUPPLIED historical
receipts in production_validation, scheduler_activation and operational_acceptance.
The last is reclassified historical, never rewritten. Exact accepted output/source/
scheduler hashes, transactions, counts, limitations and supplied/unknown fields remain
there and in the historical sections above. No native fault/crash or current freshness
claim is introduced. Original failed bootstrap is retained. Source checkout, accepted
installed runtime and current output observations are distinct authorities.

Recovery is governed by the existing PE-5.2 atomic correction and PE-5.6 accepted
correction: retain indeterminate evidence, reject unconfirmed output, separately approve
exact recertification/fresh recomputation; no automatic rollback, adoption, time refresh,
manual producer, deployment or scheduler change is authorized by closure. Original
provenance-bound deployment rollback guidance remains in DEPLOYMENT.md and historical
PE-5.6 sections; do not treat source synchronization as runtime rollback.

Explicitly deferred (unchanged original roadmap):

- PE-6 classification/role_suggestion/metadata_quality
- PE-7 expected availability/permanent IoT monitoring
- PE-8 functional/automation impact
- PE-9 dependency intelligence/automatic service relationships/improved graph/topology
- PE-10 application/integration/service assurance/surveillance reliability
- MQTT Discovery/live broker/client/topic observation/new public projection or publication
- DHCP service health/capacity
- canonical-address changes
- phone notifications
- Asset-aware retention/archive
- incident-history validator hardening
- backup/disaster recovery/hardware migration
- cold-boot/power-loss recovery
- failure propagation visualization
- historical trends
- predictive recommendations
- Safe Active Discovery

### Exact Windows validation and publication gates

Established bundled interpreter: C:/Users/JorgeAzofeifaCastill/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe -B - (stdin unittest harness), repository root working directory.
PYTHONUTF8=1; PYTHONDONTWRITEBYTECODE=1; HIOC_TEST_SHELL removed. PATH contains only Windows System32, Windows root, WindowsPowerShell/v1.0, Git/cmd and bundled interpreter directory (no shell tools). sys.path[:0]=['tests','pi4/lib'].

Exact selections: unittest.defaultTestLoader.loadTestsFromName('test_pe5_configured_association_implementation'); unittest.defaultTestLoader.discover('tests',pattern='test_pe5*.py'); unittest.defaultTestLoader.discover('tests',pattern='test_pe4*.py').
Affected suite loads test_pe4_documentation_consistency_correction, test_pe4_documentation_consistency_correction_closure, test_pe4_ha_association_public_projection_test_binding_correction, test_pe4_ha_association_public_projection_deployment_closure, test_pe10_surveillance_roadmap_preservation, test_compatibility_master_plan_governance, test_pe3_action10_governance, test_release, test_python_runtime_compatibility, test_mqtt_runtime_validation, test_mqtt_dashboard_health, test_incident_mqtt, test_inventory, test_compatibility.

Direct baseline unittest result counts (run/passed/failed/errors/skipped/class-level skips):

- focused: 79/79/0/0/0/0.
- pe5: 238/238/0/0/0/0.
- cross: 333/332/0/0/1/0.
- compatibility: 1905/1887/0/0/18/0.

Baseline broader regression is retained because runtime sources/frozen contracts and all existing test bodies remain unchanged; focused/PE-5/affected selections run again on final candidate including closure-specific positive/negative tests. Exact final counts are reported from direct unittest results before commit. Static independent Git-object acceptance verifies all 226 protected objects, payloads, preserved historical evidence, scope, schemas/identities, original surveillance specification and clean publication state. Full suite: NOT_REQUIRED_WITH_AUTHORITY: Master Plan PE-5.9 Tests required specifies full suite for source implementation. Only current documentation/governance/test bindings change; every runtime payload and frozen contract unchanged.
No unobserved final counts or commit SHA are fabricated in this self-bound record. Commit identity, normal main-only push, independent GitHub retrieval and clean HEAD=origin/main are mandatory final external publication evidence. Stop if any required validation/publication fails; do not start PE-6.

### Durability and private branch field reference

- **metadata_fields**: ["candidate", "confirmed", "domain", "schema_version", "state", "transaction_id"]
- **metadata_domains**: ["CONFIGURED_MAPPING_SOURCE", "GENERATED_RELATIONSHIP_OUTPUT"]
- **metadata_descriptor_contract**: Closed schema1.0: dur_[0-9a-f]{32} transaction_id; PENDING requires candidate descriptor and nullable prior confirmed; CONFIRMED requires candidate=null and confirmed descriptor. Descriptors contain only sha256 (64 lowercase hex) and source_revision. Source revision is integer1..9007199254740991; output source_revision may be null for no configured revision. Exact current bytes/domain/revision must match; filenames alone are not confirmation.
- **configured_fields**: ["associations", "candidate_count", "error_code", "rejections", "revision", "source_id", "source_sha256", "state"]
- **configured_states**: ["VALID", "UNAVAILABLE"]
- **relationship_fields**: ["device_id", "direction", "endpoint_id", "mapping_id", "relationship_id", "rule_id", "service_id", "source_id", "source_kind", "source_revision", "source_sha256"]
- **changes_fields**: ["added", "added_count", "baseline", "removed", "removed_count", "truncated"]
- **changes_bound**: added/removed relationship-ID arrays at most64 each; exact total counts and truncation flag, no invented removal from unavailable/noncomparable prior.

### Observed candidate validation results

Direct established Windows harness results (run/passed/failed/errors/skipped/class-level skips):

- focused: 84/84/0/0/0/0.
- pe5: 243/243/0/0/0/0.
- cross: 333/332/0/0/1/0.

The exact selections and interpreter/environment are recorded above. These observed results are synchronized into final_closure.validation.candidate_results; final unchanged-code binding validation rechecks this evidence-bearing candidate before commit. No source or execution model change is made. Broader baseline remains 1905/1887/0/0/18/0 under the same frozen runtime and preserved original test classes. Final publication remains separately verified from exact committed Git objects and GitHub.

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
