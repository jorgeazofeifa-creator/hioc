# PE-4 Home Assistant Association Adapter Bounded Manual Production Validation Preparation

FOR REVIEW ONLY - DO NOT RUN WITHOUT SEPARATE AUTHORIZATION

This repository-only preparation follows deployment PASS/CLOSED at closure commit
`560a7810ed1e57c861b38a3fe9d75397cba59eea`. Deployed source remains
`4912f20d8b2ff78dcdaf8b3e0f52e57d5de5e3a2`. The deployed adapter has never run.
The separate read-only static deployment acceptance is not adapter behavior acceptance.

[Canonical preparation](../governance/pe4/pe4-ha-association-bounded-manual-validation-preparation.json)
and its [closed schema](../governance/pe4/pe4-ha-association-bounded-manual-validation-preparation.schema.json)
bind the deployment closure, exact source identities, five dependencies and nine targets.
The [source-only wrapper](../tools/hioc-pe4-ha-association-manual-validate.py) is not deployed
or runtime-consumed. Importing it does not execute the adapter. Frozen adapter, entrypoint,
compatibility module, deployment helper and prior governance bytes remain unchanged.

## Authorization and operator sequence

1. Separately authorize **PI3 source synchronization to the approved preparation commit**.
2. Synchronize only `/home/jazofv1/hioc-release-source`, verify main/local origin/remote identity,
   clean tracked/untracked state and no Git operation, then STOP. No adapter execution in this action.
3. Independently review the sanitized source-sync evidence.
4. Separately authorize the first manual production validation using the exact preparation commit.
5. Invoke the reviewed wrapper once, return to the interactive shell, preserve sanitized evidence and STOP.
6. Independently review the run before any further action. A rerun requires separate review/authorization.

The wrapper has no source synchronization, fetch, pull, deployment, remediation, recovery,
rollback, scheduler installation or retry operation. The approved commit is an explicit wrapper
argument, never inferred as authority from current HEAD. Its immediate parent must be the closure
commit. The earlier sync review proves remote equality; execution rechecks local HEAD/origin/clean
source and does not repeat Git network access.

## Live side effects and network disclosure

BEFORE the future command, acknowledge that the adapter will access the governed local credential,
contact Home Assistant, authenticate, read four registries, potentially update sanitized compatibility
state and create private association state. This is a live network step after separate authorization.

The adapter does not mutate HA or its registries, canonical HIOC device/MAC/IP identity, liveness,
incidents, or Asset operator fields. It does not install a scheduler, publish MQTT/Public Projection,
run platform-status or active network discovery. The wrapper does not inspect the credential.

Exactly one IPv4 connection lifecycle to `192.168.100.251:8123`, WebSocket `/api/websocket`,
without DNS, proxy, redirect, retry, REST fallback, subscription or separate authentication probe.
Commands, sequential correlated IDs 1–4:

- `config/device_registry/list`
- `config/entity_registry/list`
- `config/area_registry/list`
- `config_entries/get`

There is no fifth registry command. A replayed/fifth envelope fails normal-close review.
The frozen shared network deadline is 90 seconds, connection/open caps 5 seconds, send/receive caps
15 seconds, normal close cap 2 seconds, bounded cancellation cleanup 2 seconds, and adapter alarm
180 seconds. The wrapper allows 195 seconds for the single child and kills an over-bound child
without retry or private-state cleanup. It drains at most 4096 stdout bytes in RAM; stderr is discarded.
No ping/curl/wget/nc/telnet/connectivity/authentication probe is added.

## Exact command and environment

The actual adapter invocation is exactly:

```sh
/home/jazofv1/hioc/runtime/pe4/active/bin/python -I -B \
  /home/jazofv1/hioc/pi4/bin/hioc-home-assistant-association.py
```

The entrypoint receives no arguments: no endpoint/path/credential/recovery/debug/dry-run/force flags.
The bootstrap wrapper receives only the approved preparation commit. Both bootstrap and adapter use
an explicit empty-derived environment with exactly PATH=/usr/sbin:/usr/bin:/bin,
HOME=/home/jazofv1, LANG=C.UTF-8 and LC_ALL=C.UTF-8. No token on argv or in environment.
HIOC_HOME, HIOC_HA_ENDPOINT, HTTP_PROXY, HTTPS_PROXY, ALL_PROXY and NO_PROXY are rejected
case-insensitively by the adapter. No shell tracing or raw exception output.

## Read-only preconditions

Require Linux target `nutandpihole`, real/effective user and group `jazofv1`, local LAN address
`192.168.100.252`, approved source commit/parent/subject, clean source, 0/0 local HEAD/origin,
no merge/rebase/cherry-pick/revert/bisect/sequencer operation and exact closure/record/source bytes.

Require deployment journal COMMITTED, exact durable intent source `4912f20d...`, nine target hashes,
nine created files, endpoint-added TRUE, secured prior/candidate config and committed marker bound
by intent SHA. Recheck all five existing dependencies and all nine deployed targets, target modes,
owners/groups, no-follow traversal, no ACL, single-link regular files and secured directories.
Configuration must equal the governed candidate with the approved endpoint. No redeployment.

Require accepted active interpreter resolving to
`/home/jazofv1/hioc/runtime/pe4/environments/cpython311-websockets16.1.1-lock-v1`, CPython 3.11.2,
aarch64, SOABI cpython-311-aarch64-linux-gnu, websockets 16.1.1, isolated/bytecode-disabled flags,
exact origins/distributions and reviewed customization policy. The wrapper reuses only the frozen
pure runtime policy/probe; it never calls deployment prerequisites or the credential validator.

Require associations directory jazofv1:jazofv1 0700, permanent `.home_assistant.lock` regular,
single-link, jazofv1:jazofv1 0600, no symlink/ACL. `home_assistant.json`, `.home_assistant.txn-*`
and `.home_assistant.done-*` must be ABSENT. Any unexpected private state stops before invocation;
do not delete, recover or rerun deployment. Review transaction contention separately.

Require platform-status known SHA and exact existing cron below, association scheduler absent
in user crontab and reviewed system cron/systemd surfaces. Inaccessible or over-bound surfaces fail
closed. The filesystem comparison covers the bounded production tree including runtime symlink
identities, file contents/security and directory security. Bounds: 50,000 objects, 512 MiB aggregate
regular-file bytes and 16 MiB per file. Unprovable/over-bound inputs stop before invocation.
This deliberate finite scope may require separate review on a larger installation; do not bypass it.

Canonical inventory must exist and be securely readable; its contents are not parsed for operator
evidence. The adapter remains authoritative for canonical inventory validation and its exact byte
recheck immediately before publication. Config/inventory bytes and all private comparison hashes
are RAM-only and reduced to equality booleans. No household-derived hash is printed or retained.

Any failed precondition results in ADAPTER_EXECUTION_COUNT=0 and no child invocation.

## Result surface and sanitized evidence

The exact adapter field allowlist, in output order:

- `RESULT`
- `ERROR_CODE`
- `FAILURE_STAGE`
- `COMPATIBILITY_STATUS`
- `OBSERVED_HA_VERSION`
- `ASSOCIATED_COUNT`
- `REVIEW_ONLY_COUNT`
- `REJECTED_COUNT`
- `UNMATCHED_COUNT`
- `HISTORICAL_BINDING_COUNT`
- `STATE_PUBLISHED`
- `LAST_KNOWN_GOOD_PRESERVED`

Values are frozen result/error/stage/status enums, numeric safe HA versions, counts bounded to
65536 (history 4096), TRUE/FALSE/UNKNOWN. Exactly 12 lines, ASCII, trailing newline and at most
4096 bytes. Extra/reordered/duplicate/malformed fields are discarded from RAM without result.txt;
OUTPUT_VALIDATION=FAIL and post-run independent invariant checks still proceed when possible.
No raw stdout/stderr/registry/private exception is persisted. Valid adapter output is retained exactly.

Evidence directory `/tmp/hioc-pe4-ha-association-manual-<secure-random-suffix>` is created with
0700 permissions by restrictive umask, random non-household suffix, never reused. Files are 0600,
exclusive no-follow creation, at most 16 KiB each:

- result.txt: exact validated sanitized adapter output; omitted on malformed/no output.
- validation.json: canonical closed report field set; its schema is embedded in the preparation record, with additional safe-version/count/return-code semantic bounds enforced by validate_report; no raw private objects or hashes.
- report.txt: HIOC Evidence Report containing deployment authority, intended execution result,
  invariant checks, warnings/review requirement and final OVERALL_VALIDATION.

The report allowlist is the following exact set. UNKNOWN is permitted only for unobserved checks;
unknown never becomes PASS. Commit identities, fixed target/closure labels, finite outcomes, counts
and safe observed version are the only variable evidence values. The wrapper status distinguishes
PRECONDITION_FAILED, EXECUTION_INCOMPLETE, POST_RUN_REVIEW_REQUIRED and COMPLETE.

- `TARGET`
- `SOURCE_GOVERNANCE_COMMIT`
- `DEPLOYED_SOURCE_COMMIT`
- `DEPLOYMENT_CLOSURE`
- `ADAPTER_EXECUTION_COUNT`
- `ADAPTER_RETURN_CODE`
- `PRE_RUN_PRIVATE_STATE`
- `POST_RUN_PRIVATE_STATE`
- `STATE_SCHEMA_VALIDATION`
- `TRANSACTION_NAMESPACE_CLEAN`
- `CONFIG_UNCHANGED`
- `CANONICAL_INVENTORY_UNCHANGED`
- `PLATFORM_STATUS_UNCHANGED`
- `PLATFORM_CRON_UNCHANGED`
- `ASSOCIATION_SCHEDULER_PRESENT`
- `COMPATIBILITY_STATE_VALIDATION`
- `CREDENTIAL_EXPOSED`
- `RAW_HA_DATA_PERSISTED`
- `PRIVATE_ASSOCIATION_CONTENT_EXPOSED`
- `PRODUCTION_FILES_UNCHANGED`
- `OUTPUT_VALIDATION`
- `WRAPPER_STATUS`
- `OVERALL_VALIDATION`
- `MANUAL_REVIEW_REQUIRED`
- `RESULT`
- `ERROR_CODE`
- `FAILURE_STAGE`
- `COMPATIBILITY_STATUS`
- `OBSERVED_HA_VERSION`
- `ASSOCIATED_COUNT`
- `REVIEW_ONLY_COUNT`
- `REJECTED_COUNT`
- `UNMATCHED_COUNT`
- `HISTORICAL_BINDING_COUNT`
- `STATE_PUBLISHED`
- `LAST_KNOWN_GOOD_PRESERVED`

No token/prefix/suffix/length/hash, raw registry, household identifier, association body/binding
history, raw inventory/compatibility/config, private Asset metadata or household-derived hash enters
the evidence directory. The credential remains root-managed canonical storage and is accessed only
by the adapter through its frozen governed path. No token copied for independent inspection.

## Acceptance matrix

| Outcome | Required evidence and handling |
| --- | --- |
| FULL PASS | RESULT=PASS; ERROR_CODE=NONE; FAILURE_STAGE=NONE; rc=0; compatibility in COMPATIBLE/COMPATIBLE_UPDATED/COMPATIBILITY_DEGRADED; STATE_PUBLISHED=TRUE; LAST_KNOWN_GOOD_PRESERVED=FALSE; valid state/counts; clean transaction namespaces; all preservation/security checks PASS; compatibility post-check PASS; no scheduler. Positive associations needed to avoid separate zero-count review. This run does not itself close Independent Production Acceptance. |
| PASS_WITH_WARNING / TRANSACTION_CLEANUP_FAILED | rc=0, published state may already be committed; preserve transaction/private state; no rerun, deletion, automatic rollback or recovery. Separate governed cleanup/recovery evidence review. OVERALL_VALIDATION=MANUAL_REVIEW_REQUIRED unless another invariant fails. |
| PASS_WITH_WARNING / COMPATIBILITY_REPORTING_FAILED | rc=0, publication may be valid; preserve published state; reporting may remain unchanged or incomplete. Investigate compatibility reporting separately. No retry. Never final production acceptance. |
| FAIL | Nonzero rc and exact stage-derived error (history stage uses BINDING_HISTORY_CAPACITY_EXCEEDED); preserve evidence/private state and exact LKG report; no automatic rerun/remediation/rollback/cleanup. |
| Malformed output, unexpected rc, mismatched state/compatibility or any failed invariant | OVERALL_VALIDATION=FAIL; keep safe evidence and private state; stop for separate review. No second invocation. |
| ASSOCIATED_COUNT=0 with otherwise valid PASS | MANUAL_REVIEW_REQUIRED, not invented implementation failure. Frozen contracts allow an empty strongly associated set. |

Nonzero REVIEW_ONLY/REJECTED/UNMATCHED counts can be correct when strong evidence is absent,
ambiguous or conflicting. No arbitrary count thresholds or expected household counts. Preserve
unique canonical-MAC-only identity. Structural summary counts must match associations/history/list
lengths and diagnostic totals under validate_state. First absent prior yields empty history (0);
there are no older associations to retire. No generic integration inventory is generated.

## LKG and publication semantics

The first absent baseline is a valid prior, not an existing known-good file. Source run_cycle sets
preserved TRUE after read_prior accepts absence. Before that point it is UNKNOWN. Before publication,
TRUE means that absence remains proved; failed coherence/finish checks can make it UNKNOWN.
Successful first publication sets FALSE because the absent baseline is replaced by new state.
Publication failures report TRUE only after adapter restoration proves baseline absence; otherwise
UNKNOWN. STATE_PUBLICATION can also occur during pre-HA recovery; stage alone does not prove contact.
The wrapper preserves the exact reported value rather than guessing progress.

Normal PASS requires no `.home_assistant.txn-*`/`.home_assistant.done-*`. Publication uses durable
intent, candidate validation, last inventory recheck, atomic replacement, committed marker and
cleanup-only done namespace. A leftover namespace requires separate review; no manual deletion.
The deployment journal remains COMMITTED independently of adapter publication transaction state.

## Private post-run validation

If state is present, securely read at most 16 MiB; require regular no-symlink single-link file,
jazofv1:jazofv1 0600/no ACL, strict duplicate-safe/nonfinite-safe JSON, accepted closed schema 1.1,
and the frozen pure validate_state (identities, uniqueness, timestamps, privacy, exact diagnostic
and count relations). Require first-run empty binding_history and counts equal adapter output.
STATE_PUBLISHED must agree with presence. Association directory and permanent lock security remain
exact. Reduce immediately to STATE_SCHEMA_VALIDATION/count/invariant results. Never print the body.
Config/inventory and the production tree comparison prove no generic integration inventory or
Asset file mutation by this procedure; the association document contains only frozen schema fields.

## Compatibility post-run validation

Compatibility.json is an expected permitted mutation, so deployment closure's old size/mtime are
not post-run invariants. Read strictly and validate the closed compatibility-status schema, registry
set/unique dependency identities/count, aggregate summary, HA status/version agreement, required
capabilities and first failed-capability semantics. Re-assess the HA entry using the frozen pure
framework and prior entry to check previous-known version, last-known-compatible history and dates.
Reproduce unrelated entries through the pure sanitizer/staleness algorithm: fresh observations may
remain, stale entries can become UNKNOWN while history is preserved. Do not require byte equality
of unrelated entries when framework semantics require refresh. No framework writer is executed.
An unchanged file after FAIL or COMPATIBILITY_REPORTING_FAILED is NOT_UPDATED_REVIEW_REQUIRED;
never treat it as successful reporting. On any other disagreement preserve state and stop.

Permitted production mutations are only the association state/transaction namespace and sanitized
compatibility state plus its governed lock. All other file content/security and directory security
must remain unchanged. Directory mtimes are intentionally excluded because publication changes them.
Normal post-run snapshots are independent even if output/state validation fails; unknown/failed
checks never pass. The wrapper itself does not mutate production.

Platform-status preserved SHA:
`b65464e722bf9a4da0004ecf3bb05e4105f345a87c62405ce92d97c6298b2af8`.
Exact existing platform cron:

```text
17 3 * * * flock -n /tmp/hioc-platform-status.lock /home/jazofv1/hioc/pi4/bin/hioc-platform-status.py
```

Report only CONFIG_UNCHANGED and CANONICAL_INVENTORY_UNCHANGED equality booleans, platform/cron
preservation and association-scheduler absence; no private config/inventory hashes retained.

## Failure-stage handling

For every stage: preserve evidence/state, no blind rerun and no manual private-state mutation.

| Failure stage | Operator handling principle |
| --- | --- |
| ASSOCIATION_EVALUATION | HA data obtained; strong-MAC reconciliation failed; do not alter identities to increase counts |
| BINDING_HISTORY_CAPACITY | Capacity failure; never evict history or truncate private state |
| CANDIDATE_STATE_VALIDATION | Candidate invalid; do not edit candidate or private state manually |
| CANONICAL_INVENTORY_INPUT | May occur before HA or at publication recheck after HA; preserve inventory authority; never override concurrent change |
| COMPATIBILITY | HA contacted; required capabilities/assessment rejected; do not weaken capability policy |
| CONTRACT_VALIDATION | NO_HA_CONTACT; review exact frozen authority bytes; no contract substitution |
| CREDENTIAL_ACQUISITION | NO_HA_CONTACT; review credential provisioning/security without exposing token |
| HA_AUTHENTICATION | HA contacted; greeting/version/authentication failed; preserve sanitized outcome, no alternate credential |
| HA_CONNECTION | Connection attempted; no successful authentication proved; no auxiliary connectivity probe or retry |
| LOCK_ACQUISITION | NO_HA_CONTACT; review lock ownership/contention/security; do not remove lock |
| PRIOR_STATE_VALIDATION | NO_HA_CONTACT; unexpected prior state invalidates first-run assumption; preserve state |
| REGISTRY_SCHEMA | HA contacted; registry structural validation failed; preserve sanitized outcome, no raw response evidence |
| REQUIRED_REGISTRY_COMMAND | HA contacted; command/correlation/envelope/normal-close failed; no fifth command or fallback |
| RUNTIME_VALIDATION | NO_HA_CONTACT; review exact interpreter/runtime/customization; no runtime mutation |
| STATE_PUBLICATION | May be pre-HA recovery or post-HA publication; TRUE means absent baseline restored, UNKNOWN means unproved; preserve all namespaces |
| TARGET_VALIDATION | NO_HA_CONTACT; review host/operator/LAN/config/environment; preserve evidence; no rerun |
| UNEXPECTED_INTERNAL | Contact/publication progress unknown; retain finite report and state; investigate before separate review |

## Complete future execution block

FOR REVIEW ONLY - DO NOT RUN WITHOUT SEPARATE AUTHORIZATION

This is the SECOND future operator action. The prior source-only synchronization must have been
independently accepted. Replace the placeholder with the exact approved preparation commit emitted
in the repository completion report; never substitute a dynamic git rev-parse value. Separately
review this concrete identity before authorization. This block will cause the live effects disclosed
above. It performs no source synchronization. It uses a bootstrap with site disabled; the sole
adapter child still uses the exact accepted interpreter with -I -B and no application arguments.

```sh
(
  /usr/bin/env -i PATH=/usr/sbin:/usr/bin:/bin HOME=/home/jazofv1 LANG=C.UTF-8 LC_ALL=C.UTF-8 \
    /usr/bin/python3 -I -B -S \
    /home/jazofv1/hioc-release-source/tools/hioc-pe4-ha-association-manual-validate.py \
    --approved-preparation-commit 'REPLACE_WITH_APPROVED_PREPARATION_COMMIT'
  validation_wrapper_return_code=$?
  printf 'VALIDATION_WRAPPER_RETURN_CODE=%s\n' "$validation_wrapper_return_code"
)
```

Subshell return restores interactive control without changing shell options. No shell set -e,
set -u, pipefail, tracing, exit, exec or logout. Exactly one adapter child or zero on precondition
failure. No automatic retry. The bootstrap's wrapper commit argument is not passed to the adapter.

## Current lifecycle and next action

Preparation PASS/CLOSED; Bounded Manual Production Validation PREPARED FOR SEPARATE AUTHORIZATION,
actual manual adapter execution NOT_PERFORMED. Deployment PASS/CLOSED. Independent Production
Acceptance and Scheduler Deployment NOT STARTED; Public Projection DEFERRED; PE-4 NOT COMPLETE;
Phase 7A ACTIVE; rollback NOT PERFORMED. Codex accessed no PI3/PI5/SSH/HA/real credential and ran
no adapter/platform-status, deployment, production mutation, scheduler, MQTT or Public Projection.

Exact next operator action: **PI3 source synchronization to the approved preparation commit**.
Stop after repository preparation. No execution authorization is supplied by this document.

Repository validation: 45 focused preparation tests; 477 regressions; 522 run, 521 passed, one existing Windows rsync skip. Syntax, import safety, canonical JSON/closed schemas, document links, frozen source/prior governance, privacy and diff checks passed.
