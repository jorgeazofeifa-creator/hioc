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

## Current PE-5.8 final acceptance and closure

Classification: CURRENT. Phase 7A ACTIVE; PE-5 IN_PROGRESS.
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
