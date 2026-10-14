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


## Current PE-5.6 production-found initial infrastructure correction

Classification: CURRENT. Phase 7A ACTIVE; PE-5 IN_PROGRESS; PE-4 and Public Projection PASS/CLOSED.
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
