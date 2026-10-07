# PE-4 Reconciliation Evidence Authority Correction

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

All production facts here are OPERATOR_SUPPLIED_PRODUCTION_EVIDENCE, not Codex observations.
The frozen predecessor is d767ad429ae0573ffb1411ccb787795063ef647c. Historical commits,
predecessor scope correction record/schema, deployed adapter, entrypoint, compatibility
module and deployment helper remain immutable.

## Chronology and three authorities

1. First adapter invocation completed once: PASS, return code 0, counts 25/170/26/8/history0,
   HA COMPATIBLE / 2026.9.4. Historical wrapper FAIL / return code 1 / review required.
2. Production-scope correction completed, followed by operator source synchronization PASS.
3. First reconciler attempt failed at HISTORICAL_EVIDENCE before durable protected checks.
4. The subgate diagnostic failed with FileNotFoundError. Presence diagnostic then established
   /tmp/hioc-pe4-ha-association-manual-3ciclqi7 absent, zero matching directories.
5. No artifacts were recreated and no second adapter invocation is authorized.
6. Committed historical report validation replaces the unavailable artifact prerequisite.
   Durable current production reconciliation remains a separately authorized future action.

| Evidence class | Authority and availability |
| --- | --- |
| A: live execution report | Immutable predecessor historical_evidence.report; AVAILABLE / CANONICAL OPERATOR_SUPPLIED_REPORT |
| B: original ephemeral artifacts | result.txt, validation.json, report.txt; UNAVAILABLE_FOR_REVALIDATION |
| C: durable current production | Future read-only protected-state checks; NOT YET RECONCILED UNDER CORRECTED AUTHORITY |

The [new canonical record](../governance/pe4/pe4-ha-association-reconciliation-evidence-authority-correction.json)
and [closed schema](../governance/pe4/pe4-ha-association-reconciliation-evidence-authority-correction.schema.json)
bind the [immutable predecessor](../governance/pe4/pe4-ha-association-bounded-manual-validation-correction.json)
and its schema by Git blob and SHA-256. The corrected source-only reconciler accepts only
--approved-evidence-authority-commit with the exact independently approved successor SHA.
It validates main/HEAD/origin/parent/subject/clean source authority and exact tracked identities.
It accepts no evidence-directory or arbitrary report argument and performs no /tmp evidence reads.

## Mandatory limitation and future durable checks

Use RECONCILIATION=PASS with ORIGINAL_EPHEMERAL_EVIDENCE_PRESENT=FALSE,
ORIGINAL_EPHEMERAL_EVIDENCE_REVALIDATION=UNAVAILABLE and
ORIGINAL_EPHEMERAL_EVIDENCE_LIMITATION=RECORDED. Known loss fields remain explicit on failure.
PASS requires all report and durable gates, independent review, and a later repository closure
retaining this limitation. It neither changes historical adapter PASS nor historical wrapper FAIL.
Original metadata, bytes, validation.json canonical bytes, result.txt/report.txt identity and
cross-file equality cannot be rechecked. No original artifact hashes are claimed. No disappearance
cause is known. Eventual closure must not claim FULL_ORIGINAL_ARTIFACT_REVALIDATION or ZERO_EVIDENCE_GAPS.

Read-only checks retain deployment closure, exact five dependencies and nine deployed targets,
COMMITTED journal/config candidate, accepted runtime identity/security, exact platform-status and
cron, absent association scheduler, secured directory/lock, current protected-surface stability.
private home_assistant.json must be present, regular, no symlink, single link, correct owner/group/
mode and no ACL, strict governed schema 1.1, empty binding_history, HA 2026.9.4, counts
25/170/26/8/history0, clean transaction/done namespace. Compatibility must be strict governed JSON,
HA COMPATIBLE / 2026.9.4, required capabilities TRUE, failed_capability null and framework summary
consistent. Private values stay in memory and are never printed. protected_snapshot uses
include_inventory=False; execution-time config/inventory TRUE remain historical operator evidence.
No retrospective inventory equality or whole-production-tree walk is introduced.
No adapter, credential, HA network, compatibility update, cleanup, evidence writer, scheduler
mutation, deployment or platform-status execution occurs. Output is finite sanitized stdout.

## Permanent evidence durability rule

Closure-critical evidence must not rely solely on ephemeral /tmp storage. During the same governed checkpoint, before depending on later file-level revalidation, retain a sanitized copy in a durable governed evidence directory, persist canonical sanitized repository governance, or record required evidence-file SHA-256 identities and metadata in durable governance before loss. Preserve privacy: never persist raw private HA, inventory or credential data for durability. Hashes and metadata cannot recover lost bytes; record retention and revalidation limits. This rule covers future HIOC production validation checkpoints, without expanding into backup or disaster recovery work.

## Second future operator action — review only

FOR REVIEW ONLY - DO NOT RUN WITHOUT SEPARATE AUTHORIZATION.
First synchronize source only, STOP and independently review the exact successor identity.
The block below is a repository review template; replace the quoted placeholder with the exact
approved successor SHA supplied in the final report. Do not infer approval from a moving HEAD.
The reconciler independently requires the direct d767ad4 successor with the exact correction subject.
No synchronization is included. This subshell returns control to the interactive shell.

```sh
(
  /usr/bin/env -i PATH=/usr/sbin:/usr/bin:/bin HOME=/home/jazofv1 LANG=C.UTF-8 LC_ALL=C.UTF-8 \
    /usr/bin/python3 -I -B -S \
    /home/jazofv1/hioc-release-source/tools/hioc-pe4-ha-association-manual-reconcile.py \
    --approved-evidence-authority-commit 'REPLACE_WITH_APPROVED_EVIDENCE_AUTHORITY_COMMIT'
  reconciliation_return_code=$?
  printf 'RECONCILIATION_RETURN_CODE=%s\n' "$reconciliation_return_code"
)
```

Repository validation: 41 successor authority/durable reconciliation tests, 23 preserved historical
synthetic reconciler tests and 28 scope-correction tests. The required full regression totals are
614 run, 613 passed and one existing Windows rsync skip. Syntax and definition-only import safety,
canonical new record/closed schema, all existing PE-4 record/schema pairs, changed-document links,
frozen source/predecessor governance identities, prohibited-operation review and diff checks pass.
