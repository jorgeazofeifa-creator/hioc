# PE-4 Bounded Manual Validation Production-Scope Correction

Successor authority: [PE4_HOME_ASSISTANT_ASSOCIATION_RECONCILIATION_EVIDENCE_AUTHORITY_CORRECTION.md](PE4_HOME_ASSISTANT_ASSOCIATION_RECONCILIATION_EVIDENCE_AUTHORITY_CORRECTION.md). The original review block below is historical and superseded: its missing /tmp argument is not a successor prerequisite. Historical facts and predecessor record remain frozen.

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


FOR REVIEW ONLY - DO NOT RUN WITHOUT SEPARATE AUTHORIZATION

This repository-only correction follows the first and only authorized live adapter invocation.
Starting preparation commit: `abae01b6eb60aecb12396d8078dee719d75801b7`.
Deployed source remains `4912f20d8b2ff78dcdaf8b3e0f52e57d5de5e3a2`.

[Canonical correction](../governance/pe4/pe4-ha-association-bounded-manual-validation-correction.json)
and [closed schema](../governance/pe4/pe4-ha-association-bounded-manual-validation-correction.schema.json)
preserve the exact supplied first-run report and diagnostic provenance. The
[corrected wrapper](../tools/hioc-pe4-ha-association-manual-validate.py) and
[read-only reconciler](../tools/hioc-pe4-ha-association-manual-reconcile.py) are source-only,
not deployed or consumed by runtime. Historical preparation/closure records and deployed code
remain immutable. No adapter defect is established by this evidence.

## Historical operator evidence and chronology

All production results and diagnostics in this section are
OPERATOR_SUPPLIED_PRODUCTION_EVIDENCE, provenance OPERATOR_SUPPLIED; Codex did not collect them.

1. Repository preparation PASS/CLOSED and PI3 source synchronization PASS preceded the run.
2. The first live wrapper ran once from approved preparation commit `abae01b6...`.
3. Adapter RESULT=PASS, return code 0, ERROR_CODE=NONE, FAILURE_STAGE=NONE.
4. HA compatibility COMPATIBLE, observed version 2026.9.4.
5. Private state published; ABSENT -> PRESENT, schema PASS, transaction namespace clean.
6. Counts: associated 25, review-only 170, rejected 26, unmatched 8, historical bindings 0.
7. First-publication LAST_KNOWN_GOOD_PRESERVED=FALSE is the frozen successful-first-run meaning.
8. Config, canonical inventory, platform-status and cron preservation TRUE; scheduler absent;
   compatibility validation PASS; credential/raw-HA/private-content exposure FALSE; output PASS.
9. Historical PRODUCTION_FILES_UNCHANGED=FALSE, WRAPPER_STATUS=POST_RUN_REVIEW_REQUIRED,
   OVERALL_VALIDATION=FAIL, MANUAL_REVIEW_REQUIRED=TRUE and outer wrapper return code 1 remain exact.
10. Read-only diagnostics later showed independently mutating HIOC runtime files and a failure
    of the exact global snapshot routine at SNAPSHOT_A even without adapter execution.
11. Scope is corrected to protected adapter-specific surfaces. Adapter is not rerun.
12. Read-only reconciliation must be separately executed and independently reviewed before closure.

Original evidence directory: `/tmp/hioc-pe4-ha-association-manual-3ciclqi7`.
The existing result.txt, validation.json and report.txt are read-only inputs; never rewrite them.
The raw historical wrapper FAIL is not relabeled PASS. Adapter PASS and successful specific
invariants remain separate facts.

The original-window diagnostic found zero surviving non-exempt changed candidates and was
INCONCLUSIVE. Its window was 2026-10-07T03:55:14.521612Z through 03:59:17.661723Z;
publication mtime 03:58:29.521612Z and report mtime 03:59:14.661723Z.
One non-association directory, state/platform, had mtime/ctime 03:58:29.845613Z, consistent with
compatibility publication. Directory mtime/ctime are excluded from original snapshot equality,
so those timestamps are not a demonstrated cause of the mismatch.

Later diagnostics found 22 current runtime files, with examples in history, logs, events,
forecast, incidents and statistics. Some mtimes were about 04:00:03Z, 04:00:10Z, 04:00:11Z and
04:04:10Z, after the original report. They establish normal independent churn, not the original
differing file. Redacted inventory paths remain redacted. The later exact production_snapshot
failed with DIAGNOSTIC_INTERNAL_FAILURE:Failure at SNAPSHOT_A; no adapter, HA or credential access.
The original mismatch file remains unidentified; no precise cause is fabricated.

## Source defect and corrected contract

The old production_snapshot walked almost all of the production tree and read every non-exempt
regular file by content/security. Independent subsystem writers could either differ between
snapshots or fail a strict stability read. HIOC is not required to be globally quiescent during
an association cycle. This is a wrapper invariant defect, not evidence of an adapter writer to
those unrelated paths. No brittle growing list of runtime-file exclusions is introduced.

The new field is PROTECTED_PRODUCTION_SURFACES_UNCHANGED. Historical
PRODUCTION_FILES_UNCHANGED retains its original whole-tree meaning and FALSE value.
The corrected policy is explicit and closed:

| Protected surface | Proof |
| --- | --- |
| Deployed adapter, entrypoint, compatibility module | Exact frozen hashes plus ownership/mode/no-follow/single-link/no-ACL security |
| Five existing dependencies | Exact closure manifest and secure read |
| Six deployed runtime-governance files | Exact closure manifest and deployed ownership/modes |
| config/hioc.conf | Exact committed governed candidate; execution-time pre/post bytes remain explicit |
| Canonical inventory | Own exact-byte execution-time comparison and adapter publication recheck; historical TRUE retained |
| platform-status executable | Exact preserved SHA; never execute or deploy |
| Platform cron / association scheduler | Exact platform entry, scheduler absent |
| Deployment journal | COMMITTED source, targets, intent, prior/candidate config and bound marker; secured exact objects |
| Accepted runtime | Exact identity/origins/distributions/customization/security and active pointer |
| Association directory / permanent lock | Governed 0700/0600 ownership, no symlink/ACL, regular single-link lock |

Exact deployed protected manifest (three code targets, five dependencies and six governance targets):

- `pi4/lib/hioc/home_assistant_association.py`
- `pi4/bin/hioc-home-assistant-association.py`
- `pi4/lib/hioc/core/compatibility.py`
- `governance/pe4/pe4-home-assistant-association-state-v1.1.schema.json`
- `governance/pe4/pe4-ha-runtime-credential-provisioning-closure.json`
- `governance/pe4/pe4-0c-association-contract.json`
- `governance/pe4/pe4-0c1-association-lifecycle-clarification.json`
- `governance/pe4/pe4-ha-association-adapter-implementation-preparation.json`
- `governance/compatibility-contracts.json`
- `pi4/lib/hioc/__init__.py`
- `pi4/lib/hioc/core/__init__.py`
- `pi4/lib/hioc/core/config.py`
- `pi4/lib/hioc/core/state.py`
- `pi4/lib/hioc/core/schemas.py`

Additional exact protected file paths: config/hioc.conf, execution-time
state/inventory/inventory.json, pi4/bin/hioc-platform-status.py,
state/inventory/associations/.home_assistant.lock and deployment journal intent.json,
committed.json, config-prior and config-candidate beneath
backups/pe4-ha-association-deployment-v1. No production-tree walk is used.
Snapshot hashes and private bytes stay in RAM; reports contain only finite outcomes.

Expected mutation surfaces are the association state/transaction namespace and compatibility.json
with its lock/temp mechanics. All other runtime tree paths are outside this adapter-specific
immutability assertion and retain their own subsystem governance.

## Immutable adapter write-scope analysis

The source-only call review is bound to the exact adapter/compatibility/StateStore identities in
correction governance:

- Runtime.filesystem constructs PosixFS. Its pinned chain terminates in state/inventory/associations.
  PosixFS.start/lock may create only that directory/permanent lock. Publication recovery/publish
  writes candidate/intent/committed files and links/replaces/unlinks within its pinned transaction,
  done and final home_assistant.json namespace.
- Runtime.contracts constructs StateStore(HOME / state/platform). Runtime.report invokes update_status
  with ha_core observation. The compatibility lock is .compatibility.lock; _update_status writes only
  compatibility.json, whose StateStore mechanics use compatibility.json.tmp and replace/chmod/cleanup.
  StateStore root/parent mkdir calls are also confined to state/platform.
- ConfigService.load and Runtime.inventory are readers; the credential hierarchy is read-only.
  Reconciliation uses pure validators, never constructs StateStore or calls its writers.
- Sanitized stdout and the in-process alarm are other effects. No adapter file writer targets history,
  incidents, events, forecast, statistics, inventory-engine logs, generic inventory state, config,
  platform-status or cron. No additional adapter write target was found.

The adapter, entrypoint, compatibility module and deployment helper are unchanged.
A newly discovered additional adapter write target would require stopping rather than expanding scope.

## Corrected wrapper boundary

Future separately authorized execution mechanics retain at most one invocation, no retry, minimal
environment, accepted -I -B interpreter/no application arguments, frozen four registry commands,
all target/runtime/deployment/state/security checks and sanitized output. Corrected authority explicitly
has second_adapter_execution_authorized=false, so this correction's wrapper cannot invoke a second
adapter. Its first-run absence requirements also remain. The existence of corrected code is not
execution authorization. No corrected live-run block is provided as the next action.

## Read-only reconciliation rules

The reconciler is bound to the exact correction commit, immediate parent preparation commit,
expected subject, main/local origin equality, clean source and no active Git operation. It does no
fetch/pull; remote identity is established by the earlier independently reviewed source-only sync.
Before loading shared definition-only modules it verifies source bytes against the approved commit.
Frozen preparation and closure identities are checked separately from corrected wrapper identities.

Existing evidence path must match the exact fixed directory and required /tmp naming pattern.
No-follow pinned directory traversal: directory owned by jazofv1 mode 0700, no symlink/ACL;
exact three-file allowlist, regular single-link owner jazofv1 mode 0600, no symlink/ACL, max 16 KiB.
Strict duplicate-safe/nonfinite-safe JSON must be canonical and validate under the frozen preparation
report schema plus finite sanitizer. Report fields must equal the supplied historical report exactly;
result.txt must agree with the 12 adapter fields and report.txt must agree with frozen field ordering.
Reading may change filesystem access times; those are not content/security coherence failures.

Current checks reverify deployment/source/config/runtime/platform/cron/scheduler/journal/directory/lock
protected boundaries. Private state must be present, secure, strict-JSON valid under closed schema 1.1
and frozen pure state validator, with reported summary 25/170/26/8/history 0 and no transaction/done
namespace. No state body/identity/hash is printed. Compatibility state must be structurally valid,
registry IDs/count and aggregate summary coherent, ha_core COMPATIBLE/2026.9.4 with required
capabilities true/no failed capability and frozen assess/history semantics. No compatibility writer
or reporting rerun is called. Historical COMPATIBILITY_STATE_VALIDATION=PASS supplies execution-time
framework preservation evidence; current checking does not invent the lost pre-run private payload.

Current protected checks and existing evidence are read again before success. A difference, failed
security check, malformed evidence, mismatch or unproved invariant gives RECONCILIATION=FAIL and a
finite stage only. No exception text, credential, private state, household identifiers or raw HA data.
The reconciler writes nothing; it emits a finite sanitized report on stdout and return code 0/1.
It cannot close repository governance or authorize another adapter invocation.

A later reconciliation proves current durable coherence; it cannot recreate all original execution-time
comparisons. It does not compare current inventory to a nonexistent historical inventory snapshot.
Historical CONFIG_UNCHANGED, CANONICAL_INVENTORY_UNCHANGED, PLATFORM_STATUS_UNCHANGED,
PLATFORM_CRON_UNCHANGED and scheduler absence remain explicitly OPERATOR_SUPPLIED execution-time evidence.
No unrelated runtime immutability is claimed or required.

## Separate operator actions and review-only block

1. Separately approve PI3 source synchronization to the correction commit. Source sync only, then STOP.
2. Independently review source synchronization.
3. Separately authorize read-only post-run reconciliation of the existing first run.
4. Run the following reviewed block once, capture sanitized stdout and return to the interactive shell.
5. STOP for independent reconciliation review. If accepted, next checkpoint is separate repository
   governance closure of Bounded Manual Production Validation. Independent Production Acceptance
   remains a later checkpoint. No adapter rerun, cleanup, rollback, deployment or scheduler action.

FOR REVIEW ONLY - DO NOT RUN WITHOUT SEPARATE AUTHORIZATION

This block is the second future operator action. Replace the quoted placeholder with the exact
correction commit in the completion report; do not infer authorization from dynamic HEAD.
It reads source, the existing sanitized evidence and governed production state; it does not acquire
credential, contact HA, execute adapter/platform-status, mutate production, rewrite evidence, clean
transaction files, rerun compatibility reporting or change scheduler.

```sh
(
  /usr/bin/env -i PATH=/usr/sbin:/usr/bin:/bin HOME=/home/jazofv1 LANG=C.UTF-8 LC_ALL=C.UTF-8 \
    /usr/bin/python3 -I -B -S \
    /home/jazofv1/hioc-release-source/tools/hioc-pe4-ha-association-manual-reconcile.py \
    --approved-correction-commit 'REPLACE_WITH_APPROVED_CORRECTION_COMMIT' \
    --evidence-directory /tmp/hioc-pe4-ha-association-manual-3ciclqi7
  reconciliation_return_code=$?
  printf 'RECONCILIATION_RETURN_CODE=%s\n' "$reconciliation_return_code"
)
```

No shell set -e/-u/pipefail/tracing/exit/exec/logout; the subshell returns interactive control.
No source synchronization or adapter execution is combined into this block.

## Current lifecycle

Deployment and historical preparation PASS/CLOSED; Bounded Manual Production Validation
ATTEMPTED / REVIEW REQUIRED; scope correction PASS/CLOSED; Post-Run Reconciliation PREPARED FOR
SEPARATE AUTHORIZATION, NOT_PERFORMED. Independent Production Acceptance and Scheduler Deployment
NOT STARTED; Public Projection DEFERRED; PE-4 NOT COMPLETE; Phase 7A ACTIVE; rollback NOT PERFORMED.
Current objective: PE-4 Home Assistant Association Adapter Post-Run Reconciliation.
Next operator action: **PI3 source synchronization to the correction commit**.
Codex has not accessed PI3/PI5/SSH/HA/real credentials, executed adapter/platform-status/reconciliation,
deployed or mutated production/scheduler, published MQTT or begun Public Projection.

Repository validation: 28 correction tests and 23 reconciliation tests passed; 522 regressions run, 521 passed, one existing Windows rsync skip. Total 573 run, 572 passed, one skipped. Syntax/import safety, canonical closed schemas, links, source identities, privacy/prohibited-operation checks and diff checks passed. All 53 prior governance artifacts and frozen deployed sources remain unchanged.
