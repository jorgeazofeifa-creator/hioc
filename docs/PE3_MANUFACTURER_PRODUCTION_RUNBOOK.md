# PE-3.3 Manufacturer Production Deployment and Validation Runbook

## Current Action 8 completion checkpoint

The governed Action 8 execution at governance commit
`fa344828161e892523faa3da5d4cdf07d2e8e792` completed with `ACTION8=COMPLETE`,
`RESULT=PASS`, and `ROLLBACK_RECOMMENDED=FALSE`. Its private invocation evidence
is preserved at `/tmp/hioc-pe3-action8-eZxNGrKa` and must not be modified,
deleted, reused, or cleaned. The prerequisite source-governance refresh and
corrected-validator runtime deployment are **PASS / COMPLETE / CURRENT**. No
rollback was performed, transport staging remains absent and unnecessary, and
dataset retransmission is not required.

Action 8 is **PASS / COMPLETE**. Action 9 remains **NOT STARTED**. The existing
Action 9 operator block has not been prepared for execution at this checkpoint;
it requires a separate governance review after this completion record is
validated, committed, pushed to `main`, and the repository is verified clean.

## Corrected-validator synchronization and deployment prerequisites

The previous Action 8 bootstrap PASS is historical for an earlier governance
commit. Although the Action 8 wrapper blob remains unchanged, release-source
must first pass the existing synchronization/bootstrap gate at the newly
approved commit and STOP for review. A second, separately authorized boundary
may then invoke `tools/hioc-pe3-action8-validator-deploy.sh` with that same full
commit and must STOP after evidence review. No executable operator invocation is
authorized or prepared by this implementation checkpoint.

Validator deployment emits `TARGET_IDENTITY`, `SOURCE_IDENTITY`,
`SOURCE_VALIDATOR_IDENTITY`, `RUNTIME_PRECONDITION`, `PROTECTED_PRE_STATE`,
`BACKUP`, `VALIDATOR_PUBLICATION`, `RUNTIME_VALIDATOR_IDENTITY`,
`SOURCE_RUNTIME_EQUALITY`, `PROTECTED_POST_STATE`, `DEPLOYMENT_DISPOSITION`,
`EVIDENCE_REPORT`, `RESULT`, and `ROLLBACK_RECOMMENDED`. Disposition is
`NOOP_IDENTICAL` or `REPLACED`. Every failure emits bounded `RESULT`,
`ERROR_CODE`, `FAILURE_STAGE`, and rollback advice, plus private evidence/backup
paths only when created. It cannot modify the generated manufacturer pair,
inventory, configuration, immutable dataset, staging, services, or schedules.
At that prerequisite checkpoint, Action 8 remained **ATTEMPTED BUT NOT
COMPLETE** and Action 9 remained **NOT STARTED**.

## Current Action 8 permission-contract stop

At governance commit `6828ee0d0f9b47d9c8c86b5e660c14a09894c2ad`, the
third governed attempt reached `MANUFACTURER_GENERATION=PASS` and
`MANUFACTURER_ARTIFACT_IDENTITY=PASS`, then stopped at
`MANUFACTURER_ARTIFACT_VALIDATION` with `MANUFACTURER_PERMISSION_ERROR`.
Both generated artifacts were owner/group `jazofv1:jazofv1`, exact mode `0600`,
and no manufacturer temporary artifacts existed. The validator accepted those
two files, then incorrectly applied their private permission ceiling to
`inventory.json`. The correction preserves exact `0600` for both manufacturer
artifacts and the established non-group/world-writable inventory input modes.

At that historical permission-contract stop, the existing artifacts appeared
permission-safe from supplied metadata, but semantic validation had not
completed. The rollback advisory was fail-closed `TRUE`; no rollback was
performed. Action 8 was **ATTEMPTED BUT NOT COMPLETE** and Action 9 was **NOT
STARTED**. Governed runtime validator synchronization and a separately reviewed
next authorization were required.

Status: **DESIGN FROZEN; NOT EXECUTED**

This is the authoritative operator procedure for deploying and validating PE-3
on PI3 NUT&PIHOLE. Codex does not execute these commands. The operator runs one
action, returns its sanitized output for review, and does not proceed until the
next action is explicitly authorized.

## Frozen identities and boundaries

```text
IMPLEMENTATION_COMMIT=157ae644dcedcbec7c69cb0d8b054e104335e024
OPERATOR_GOVERNANCE_COMMIT=<full 40-hex commit created by this checkpoint and pushed to origin/main>
DATASET_ID=local-ieee-ra
DATASET_VERSION=2026-08-11-r1
DATABASE_SHA256=81f147cc57768c5797c4ad73a8c0369001bbdcbfe1548e71d3702c8c7f81e0e1
DATABASE_SEMANTIC_SHA256=2dbda82441416feea8d2f60c4ebe043c033c1de80ed50460e55a5367dcc1083c
MANIFEST_SHA256=10c8097c0a4ec6e8cc4cd3dc61afc7f368057f4ef4b6534df9f6dd31634a4ac4
DATABASE_BYTES=8652642
MANIFEST_BYTES=1338
SELECTABLE_RECORDS=53581
CONFLICT_KEYS=2
NORMALIZED_UNIQUE_KEYS=53583
MA_L_SELECTABLE=39916
MA_M_SELECTABLE=6538
MA_S_SELECTABLE=7127
EXACT_DUPLICATES=0
```

Only the validated normalized database and adjacent manifest cross the Windows
to PI3 boundary. Raw IEEE CSV files, registry rows, external workspace evidence,
and source organization variants remain on the operator workstation. No runtime
download or automated update exists.

Target identity is hostname `nutandpihole`, IPv4 `192.168.100.252`, operator and
runtime owner `jazofv1:jazofv1`, release source
`/home/jazofv1/hioc-release-source`, and runtime `/home/jazofv1/hioc`.

The final immutable dataset directory is exactly:

```text
/home/jazofv1/hioc/data/manufacturer/versions/local-ieee-ra--2026-08-11-r1
```

The parent and version directory modes are `0700`; database, manifest, sidecar,
and status modes are `0600`. Symlinks and group/world write are prohibited.
Versions are never overwritten, merged, pruned, or replaced by release actions.

## Action 1 — Windows local artifact verification

Target: Windows operator workstation. Mutation: none. Rollback relevance: none.

The canonical executable implementation is the checked-in script
`tools/hioc-pe3-action1.ps1`. Never reproduce or reconstruct that script
through chat. The approved script identities are:

```text
ACTION1_SCRIPT_SHA256=f2788c6517bae6aa0fc8394f523576e6f702371cba8d8751d6c76e0d4bd8b5bb
ACTION1_SCRIPT_GIT_BLOB=da9a0f8acaa86f4bfeb5c30490a8d3212e0c2b0e
```

The governance commit supplied by the operator must contain that exact blob.
The script first verifies branch, HEAD/origin identity, repository cleanliness,
its own repository path and Git blob, a clean script diff, and implementation
ancestry. Script-identity failure returns
`RESULT=INPUT_OR_PRECONDITION_ERROR` and
`ERROR_CODE=ACTION1_SCRIPT_IDENTITY_MISMATCH` without closing PowerShell.

Action 1 also reads the approved commit's explicit
`governance/python-runtime-support.json`. Windows CPython 3.13.x is `supported`
with validated patch evidence 3.13.15, so the support gate permits interpreter
discovery. It still returns `PYTHON_RUNTIME_SUPPORT_PENDING` for any repository
state that is not supported. See
[PYTHON_RUNTIME_COMPATIBILITY.md](PYTHON_RUNTIME_COMPATIBILITY.md).

Use this invocation block only; enter the two Windows paths and the approved
full post-push governance commit when prompted:

```powershell
$Repo = Read-Host 'Enter the authoritative HIOC repository path'
$ExternalWorkspace = Read-Host 'Enter the retained PE-3 external workspace path'
$GovernanceCommit = Read-Host 'Enter the approved full 40-hex post-push governance commit'
$Action1Script = Join-Path $Repo 'tools/hioc-pe3-action1.ps1'
& $Action1Script -Repo $Repo -ExternalWorkspace $ExternalWorkspace -GovernanceCommit $GovernanceCommit
```

Expected output: validator PASS plus the final sanitized PASS object. The
resolver is reported only as
`pymanager list --one --format=exe --only-managed 3.13`, with major/minor `3.13`;
the selected build is relative to the supplied workspace, and no Windows user
path or registry content is printed. Multiple exact matching pairs are accepted
only after both hashes and sizes match; lexical absolute-path ordering then makes
the choice deterministic. Expected failures emit sanitized `RESULT` and
`ERROR_CODE` lines and return control to the interactive prompt. Unexpected
failures additionally report only the approved bounded `FAILURE_STAGE`, never
exception text, command text, stack traces, absolute paths, or registry content.

Action 1 resolves only the exact managed 3.13 interpreter through `pymanager`
machine-oriented output, requires an absolute regular file, and probes CPython
3.13. It does not use `py`, `python3`, `python`, or `pymanager exec`. Automatic
installation is disabled and Action 1 never installs Python.

The prerequisite checkpoint used `pymanager` for management and ultimately
resolved the exact manager-owned interpreter for execution after explicit 3.13
installation. The operator workstation's
unintended CPython 3.14.7 does not satisfy Action 1 and does not change its
resolver or support-state gate. The following paragraphs preserve the historical
blocked stages that preceded the successful validation and support promotion.

The prerequisite checkpoint's post-install `PYTHON_PROBE` failure is classified
as native runtime-invocation handling, not Python compatibility or PE-3
evidence. A 3.13 runtime may exist but remains unvalidated. Action 1 stays
blocked until the hardened checkpoint reuses or installs 3.13, completes all
wrapped validation stages, and a separate commit promotes support.

The later `FULL_REGRESSION_FAILED` result was isolated to three Bash-dependent
network-probe governance tests raising Windows `WinError 2` because no shell was
resolvable. This is a cross-platform test-prerequisite defect, not CPython 3.13
or PE-3 evidence. The tests now skip explicitly only when Bash is absent and
retain full semantics when it is present. Action 1 remains blocked pending a
fresh governed checkpoint PASS and separate support promotion.

The following governed retry also reported `FULL_REGRESSION_FAILED`, but an
immediate direct `py -3.13` full regression in the same repository passed 506
tests with 13 skips and exit code 0. Forensics established a checkpoint result-
classification defect: an optionally parsed test count was incorrectly used as
an acceptance gate, and head-only bounded capture could omit the trailing
unittest summary. The corrected checkpoint uses native exit code exclusively
for pass/fail and reports parsed counts without treating them as criteria.
This is not Python, manufacturer, PE-3, or production failure. Action 1 remains
blocked until a corrected governed checkpoint PASS and separate support-state
promotion.

The governed checkpoint still returned `FULL_REGRESSION_FAILED` after that
correction. Direct CPython 3.13 runs then passed 508 tests with 13 skips and exit
code 0 both normally and with the checkpoint's `PYTHONPYCACHEPREFIX`. The exact
Windows `ProcessStartInfo` mismatch is pending one separately governed,
repository-controlled diagnostic execution. Do not interpret this as PE-3
evidence, rerun Action 1, or prepare Action 2.

The diagnostic proved the resolved `py` App Execution Alias diverges when
launched through `ProcessStartInfo`: direct regression exited 0, while the
wrapper exited 1 after completed stream reads and produced no unittest summary.
The Python checkpoint now resolves and directly invokes the exact managed
CPython 3.13 interpreter. Action 1 remains blocked pending a trustworthy
checkpoint PASS and separate support promotion.

Final isolation proved even the exact managed interpreter failed only when the
checkpoint executed Python through `ProcessStartInfo`; direct execution passed
with the same pycache environment. The corrected checkpoint retains exact 3.13
selection and invokes every Python stage through scoped PowerShell-native
execution. Action 1 remains blocked until that checkpoint returns PASS and
support is promoted separately.

Closure: the corrected governed checkpoint passed on CPython 3.13.15 at commit
`6b622280a6f414d14ca3060da349423d92d664cb`, including full regression 520/13
skips, policy 10, Action 1 governance 13, manufacturer 119, compilation, and a
clean repository. Support is promoted and Action 1 is ready to resume, but was
not executed by the promotion checkpoint.

Stop on any non-PASS result. Run Action 1 only; return output; do not proceed.


## Action 2 — Manual transfer to unique PI3 staging

Targets: PI3 console to create staging, then Windows to transfer. Mutation:
temporary staging only. Rollback relevance: none; failed staging is removable
after classification.

On PI3, after the operator independently confirms the target terminal:

```bash
set -euo pipefail
umask 077
PI3_STAGE="$(mktemp -d /tmp/hioc-pe3-dataset-transfer-XXXXXXXXXX)"
chmod 0700 "$PI3_STAGE"
chown jazofv1:jazofv1 "$PI3_STAGE"
printf 'PI3_STAGE=%s\n' "$PI3_STAGE"
```

On Windows, use the exact returned path and the two explicit Action 1 variables:

```powershell
$Pi3Stage = '/tmp/hioc-pe3-dataset-transfer-PJ5qPbRS'
scp -- $Database $Manifest "jazofv1@192.168.100.252:${Pi3Stage}/"
if ($LASTEXITCODE -ne 0) { throw 'transfer failed' }
Write-Output 'TRANSFER_RESULT=PASS'
```

No wildcard, recursive copy, source CSV, evidence directory, or repository path
is allowed. Stop if the stage path is not the exact returned path. Run Action 2
only; return output; do not proceed.

## Action 3 — PI3 staging verification

Target: PI3. Mutation: none. Rollback relevance: none. This action verifies only
the target and transferred staging artifacts. Repository synchronization,
implementation identity, and validator execution belong to Action 4 because a
stale clean source checkout may not yet contain the implementation commit.

The original Action 3 incorrectly required that commit before Action 4 fetched
it and used `set -euo pipefail` with bare assertions in an interactive shell.
The failed history check terminated the operator session. Read-only recovery
proved that staging remained intact and established the following accepted
Action 3 evidence for `/tmp/hioc-pe3-dataset-transfer-PJ5qPbRS`: target identity
PASS; owner/mode PASS; exact two-file contents PASS; regular/non-symlink checks
PASS; byte sizes PASS; and both frozen SHA-256 identities PASS. Action 3 is
**STOPPED — REPOSITORY-SEQUENCING PRECONDITION**, with its staging-only scope
complete. Do not repeat it for this deployment unless staging changes.

For any required future staging revalidation, use the function-scoped block
below. It does not enable shell-level `errexit`; every failure emits a sanitized
result, code, and stage, returns from the function, and leaves the prompt alive.

```bash
set +x
hioc_pe3_action3() {
  PI3_STAGE='/tmp/hioc-pe3-dataset-transfer-PJ5qPbRS'
  DB="$PI3_STAGE/manufacturer-db.json"
  MF="$PI3_STAGE/manufacturer-db.manifest.json"
  fail() { printf 'RESULT=INPUT_OR_PRECONDITION_ERROR\nERROR_CODE=%s\nFAILURE_STAGE=%s\n' "$1" "$2"; return 1; }
  [ "$(hostname -s 2>/dev/null)" = nutandpihole ] || { fail WRONG_TARGET TARGET_IDENTITY; return; }
  ip -o -4 addr show scope global 2>/dev/null | awk '{print $4}' | cut -d/ -f1 | grep -Fxq 192.168.100.252 || { fail WRONG_TARGET TARGET_IDENTITY; return; }
  read -r -p 'Type nutandpihole to confirm the production target: ' CONFIRM_TARGET
  [ "$CONFIRM_TARGET" = nutandpihole ] || { fail TARGET_CONFIRMATION_FAILED TARGET_IDENTITY; return; }
  [ -d "$PI3_STAGE" ] && [ ! -L "$PI3_STAGE" ] || { fail STAGING_DIRECTORY_INVALID STAGING_IDENTITY; return; }
  [ "$(stat -c %U:%G "$PI3_STAGE" 2>/dev/null)" = jazofv1:jazofv1 ] && [ "$(stat -c %a "$PI3_STAGE" 2>/dev/null)" = 700 ] || { fail STAGING_PERMISSIONS_INVALID STAGING_IDENTITY; return; }
  [ "$(find "$PI3_STAGE" -mindepth 1 -maxdepth 1 -printf '%f\n' 2>/dev/null | sort | paste -sd, -)" = 'manufacturer-db.json,manufacturer-db.manifest.json' ] || { fail STAGING_CONTENTS_INVALID STAGING_CONTENTS; return; }
  for p in "$DB" "$MF"; do [ -f "$p" ] && [ ! -L "$p" ] || { fail STAGING_FILE_INVALID STAGING_CONTENTS; return; }; done
  [ "$(stat -c %s "$DB" 2>/dev/null)" = 8652642 ] && [ "$(stat -c %s "$MF" 2>/dev/null)" = 1338 ] || { fail ARTIFACT_SIZE_MISMATCH ARTIFACT_IDENTITY; return; }
  [ "$(sha256sum "$DB" 2>/dev/null | awk '{print $1}')" = 81f147cc57768c5797c4ad73a8c0369001bbdcbfe1548e71d3702c8c7f81e0e1 ] || { fail DATABASE_HASH_MISMATCH ARTIFACT_IDENTITY; return; }
  [ "$(sha256sum "$MF" 2>/dev/null | awk '{print $1}')" = 10c8097c0a4ec6e8cc4cd3dc61afc7f368057f4ef4b6534df9f6dd31634a4ac4 ] || { fail MANIFEST_HASH_MISMATCH ARTIFACT_IDENTITY; return; }
  printf 'RESULT=PASS\nSTAGING_VERIFICATION=PASS\n'
}
hioc_pe3_action3
```

Stop on any non-PASS result. Run Action 3 only; return output; do not proceed.

## Action 4 — PI3 release-source synchronization and implementation validation

Target: PI3 release-source repository and transferred staging pair. Mutation:
Git fast-forward only; all post-sync implementation and dataset validation is
read-only. Rollback relevance: source synchronization is not runtime rollback.

Action 4 first synchronizes the clean source checkout. Only after HEAD equals
the approved governance commit does it prove implementation ancestry, protected
implementation/validator identity, recheck the staged artifact identity at the
point of validator use, normalize only the two identity-proven staged files to
the frozen `0600` mode, recheck mode and content identity, and run the read-only
validator. This is the required barrier before Action 5 can deploy code.

```bash
set +x
hioc_pe3_action4() {
  SOURCE=/home/jazofv1/hioc-release-source
  PI3_STAGE='/tmp/hioc-pe3-dataset-transfer-PJ5qPbRS'
  DB="$PI3_STAGE/manufacturer-db.json"
  MF="$PI3_STAGE/manufacturer-db.manifest.json"
  IMPLEMENTATION_COMMIT=157ae644dcedcbec7c69cb0d8b054e104335e024
  OPERATOR_GOVERNANCE_COMMIT='<approved-full-40-hex-post-push-commit>'
  fail() { printf 'RESULT=INPUT_OR_PRECONDITION_ERROR\nERROR_CODE=%s\nFAILURE_STAGE=%s\n' "$1" "$2"; return 1; }
  validation_fail() { printf 'RESULT=VALIDATION_FAIL\nERROR_CODE=%s\nFAILURE_STAGE=%s\n' "$1" "$2"; return 1; }
  [ "$(hostname -s 2>/dev/null)" = nutandpihole ] || { fail WRONG_TARGET TARGET_IDENTITY; return; }
  ip -o -4 addr show scope global 2>/dev/null | awk '{print $4}' | cut -d/ -f1 | grep -Fxq 192.168.100.252 || { fail WRONG_TARGET TARGET_IDENTITY; return; }
  [ -d "$SOURCE/.git" ] || { fail SOURCE_REPOSITORY_MISSING REPOSITORY_PRECONDITION; return; }
  [ "$(git -C "$SOURCE" branch --show-current 2>/dev/null)" = main ] || { fail WRONG_BRANCH REPOSITORY_PRECONDITION; return; }
  [ -z "$(git -C "$SOURCE" status --porcelain 2>/dev/null)" ] || { fail SOURCE_REPOSITORY_DIRTY REPOSITORY_PRECONDITION; return; }
  for marker in MERGE_HEAD REBASE_HEAD CHERRY_PICK_HEAD REVERT_HEAD BISECT_LOG; do [ ! -e "$SOURCE/.git/$marker" ] || { fail ACTIVE_GIT_OPERATION REPOSITORY_PRECONDITION; return; }; done
  [ ! -d "$SOURCE/.git/rebase-merge" ] && [ ! -d "$SOURCE/.git/rebase-apply" ] || { fail ACTIVE_GIT_OPERATION REPOSITORY_PRECONDITION; return; }
  git -C "$SOURCE" fetch origin >/dev/null 2>&1 || { fail GIT_FETCH_FAILED REPOSITORY_SYNCHRONIZATION; return; }
  [ "$(git -C "$SOURCE" rev-parse origin/main 2>/dev/null)" = "$OPERATOR_GOVERNANCE_COMMIT" ] || { fail GOVERNANCE_COMMIT_MISMATCH REPOSITORY_SYNCHRONIZATION; return; }
  git -C "$SOURCE" merge-base --is-ancestor HEAD origin/main >/dev/null 2>&1 || { fail NON_FAST_FORWARD_SOURCE REPOSITORY_SYNCHRONIZATION; return; }
  git -C "$SOURCE" merge --ff-only origin/main >/dev/null 2>&1 || { fail FAST_FORWARD_FAILED REPOSITORY_SYNCHRONIZATION; return; }
  [ "$(git -C "$SOURCE" rev-parse HEAD 2>/dev/null)" = "$OPERATOR_GOVERNANCE_COMMIT" ] && [ -z "$(git -C "$SOURCE" status --porcelain 2>/dev/null)" ] || { fail POST_SYNC_IDENTITY_FAILED REPOSITORY_SYNCHRONIZATION; return; }
  git -C "$SOURCE" cat-file -e "$IMPLEMENTATION_COMMIT^{commit}" 2>/dev/null || { fail IMPLEMENTATION_COMMIT_MISSING IMPLEMENTATION_IDENTITY; return; }
  git -C "$SOURCE" merge-base --is-ancestor "$IMPLEMENTATION_COMMIT" HEAD >/dev/null 2>&1 || { fail IMPLEMENTATION_ANCESTRY_FAILED IMPLEMENTATION_IDENTITY; return; }
  git -C "$SOURCE" diff --quiet "$IMPLEMENTATION_COMMIT" -- pi4/lib/hioc/manufacturer.py pi4/bin/hioc-validate-manufacturer.py || { fail MANUFACTURER_IMPLEMENTATION_IDENTITY_FAILED IMPLEMENTATION_IDENTITY; return; }
  [ -d "$PI3_STAGE" ] && [ ! -L "$PI3_STAGE" ] && [ "$(stat -c %U:%G "$PI3_STAGE" 2>/dev/null)" = jazofv1:jazofv1 ] && [ "$(stat -c %a "$PI3_STAGE" 2>/dev/null)" = 700 ] || { fail STAGING_IDENTITY_CHANGED STAGING_REVALIDATION; return; }
  [ "$(find "$PI3_STAGE" -mindepth 1 -maxdepth 1 -printf '%f\n' 2>/dev/null | sort | paste -sd, -)" = 'manufacturer-db.json,manufacturer-db.manifest.json' ] || { fail STAGING_CONTENTS_CHANGED STAGING_REVALIDATION; return; }
  for p in "$DB" "$MF"; do [ -f "$p" ] && [ ! -L "$p" ] && [ "$(stat -c %U:%G "$p" 2>/dev/null)" = jazofv1:jazofv1 ] || { fail STAGING_FILE_IDENTITY_CHANGED STAGING_REVALIDATION; return; }; done
  [ "$(stat -c %s "$DB" 2>/dev/null)" = 8652642 ] && [ "$(stat -c %s "$MF" 2>/dev/null)" = 1338 ] || { fail ARTIFACT_SIZE_MISMATCH STAGING_REVALIDATION; return; }
  [ "$(sha256sum "$DB" 2>/dev/null | awk '{print $1}')" = 81f147cc57768c5797c4ad73a8c0369001bbdcbfe1548e71d3702c8c7f81e0e1 ] && [ "$(sha256sum "$MF" 2>/dev/null | awk '{print $1}')" = 10c8097c0a4ec6e8cc4cd3dc61afc7f368057f4ef4b6534df9f6dd31634a4ac4 ] || { fail ARTIFACT_HASH_MISMATCH STAGING_REVALIDATION; return; }
  DB_HASH_BEFORE="$(sha256sum "$DB" | awk '{print $1}')"; MF_HASH_BEFORE="$(sha256sum "$MF" | awk '{print $1}')"
  for p in "$DB" "$MF"; do mode="$(stat -c %a "$p" 2>/dev/null)"; [ "$mode" = 600 ] || [ "$mode" = 644 ] || { fail STAGING_MODE_NOT_NORMALIZABLE STAGING_PERMISSION_NORMALIZATION; return; }; done
  chmod 0600 -- "$DB" "$MF" || { fail STAGING_CHMOD_FAILED STAGING_PERMISSION_NORMALIZATION; return; }
  [ "$(stat -c %a "$DB")" = 600 ] && [ "$(stat -c %a "$MF")" = 600 ] || { fail STAGING_MODE_NORMALIZATION_FAILED STAGING_PERMISSION_NORMALIZATION; return; }
  [ "$(sha256sum "$DB" | awk '{print $1}')" = "$DB_HASH_BEFORE" ] && [ "$(sha256sum "$MF" | awk '{print $1}')" = "$MF_HASH_BEFORE" ] || { fail CONTENT_CHANGED_DURING_CHMOD STAGING_PERMISSION_NORMALIZATION; return; }
  HIOC_HOME="$SOURCE" python3 "$SOURCE/pi4/bin/hioc-validate-manufacturer.py" database --database "$DB" --manifest "$MF" --json || { validation_fail MANUFACTURER_VALIDATION_FAILED MANUFACTURER_VALIDATION; return; }
  printf 'RESULT=PASS\nREPOSITORY_SYNCHRONIZATION=PASS\nIMPLEMENTATION_VALIDATION=PASS\nSTAGING_REVALIDATION=PASS\nSTAGING_PERMISSION_NORMALIZATION=PASS\n'
}
hioc_pe3_action4
```

Stop on any non-PASS result. The Git fast-forward may remain after a later
validation stop; it does not change production runtime. Do not deploy or proceed
to Action 5 without all five final PASS lines and the validator PASS object.
Run Action 4 only; return output.

### Action 4A — target synchronization and resume-script identity

The synchronized Action 4 run reached the approved validator and stopped safely
with `MANUFACTURER_PERMISSION_ERROR`: both correct, owner-matched staged files
were mode `0644`. Transport success and digest identity did not establish
permission safety. Source synchronization passed at commit
`653f887a643c877a8f611145c8b8e9f92a65b6cd`, but later governance corrections
introduced the resume script. Its first invocation failed before execution
because PI3 release source was still at that older commit. No staging or
production mutation occurred. Action 4A synchronizes the target source to the
exact approved commit, proves script identity, and then stops for evidence
review. It is inline because the stale target cannot contain a new bootstrap
tool.

The authoritative implementation is the repository-controlled
`tools/hioc-pe3-action4-resume-permissions.sh`. Chat must provide only the short
invocation below, never reproduce the script source. The script first verifies
its own Git object from the approved governance commit, exact synchronized
source identity, implementation ancestry/identity, and the complete staging
identity. Only mode `0600` or the observed transport-created `0644` is eligible.
Files already at `0600` are an idempotent no-op; `chmod 0600` receives only the
exact database and/or manifest still at `0644`.

After normalization, the script rechecks the directory type, owner, and mode;
the exact two-entry set; both files' regular/non-symlink type, owner/group,
`0600` mode, frozen byte size, and frozen SHA-256. It then runs only the approved
read-only validator and accepts only JSON with `result:"PASS"`,
`privacy_safe:true`, and `record_count:53581`.

Target: **PI3 NUT&PIHOLE**, interactive Bash. Replace the placeholder only with
the approved full 40-hex commit containing this prerequisite and the script.
The bounded prerequisite permits only a clean fast-forward and verifies script
availability and Git identity. It performs no reset, force, stash, local-change
discard, merge commit, staging reference or mutation, validator execution,
deployment, or Action 5 work. It returns PASS and stops.

```bash
set +x
hioc_pe3_action4a_sync() {
  SOURCE=/home/jazofv1/hioc-release-source
  SCRIPT_REL=tools/hioc-pe3-action4-resume-permissions.sh
  SCRIPT="$SOURCE/$SCRIPT_REL"
  GOVERNANCE_COMMIT='<approved-full-40-hex-action4-resume-sync-commit>'
  SCRIPT_BLOB=0602d9f460bf127bac4be953686fad1c0700c14e
  fail() { printf 'RESULT=INPUT_OR_PRECONDITION_ERROR\nERROR_CODE=%s\nFAILURE_STAGE=%s\n' "$1" "$2"; return 1; }
  [ "$(hostname -s 2>/dev/null)" = nutandpihole ] || { fail WRONG_TARGET TARGET_SYNCHRONIZATION; return; }
  ip -o -4 addr show scope global 2>/dev/null | awk '{print $4}' | cut -d/ -f1 | grep -Fxq 192.168.100.252 || { fail WRONG_TARGET TARGET_SYNCHRONIZATION; return; }
  printf 'TARGET_IDENTITY=PASS\n'
  [ -d "$SOURCE/.git" ] || { fail SOURCE_REPOSITORY_MISSING TARGET_SYNCHRONIZATION; return; }
  [ "$(git -C "$SOURCE" branch --show-current 2>/dev/null)" = main ] || { fail WRONG_BRANCH TARGET_SYNCHRONIZATION; return; }
  [ -z "$(git -C "$SOURCE" status --porcelain 2>/dev/null)" ] || { fail SOURCE_REPOSITORY_DIRTY TARGET_SYNCHRONIZATION; return; }
  for marker in MERGE_HEAD REBASE_HEAD CHERRY_PICK_HEAD REVERT_HEAD BISECT_LOG; do [ ! -e "$SOURCE/.git/$marker" ] || { fail ACTIVE_GIT_OPERATION TARGET_SYNCHRONIZATION; return; }; done
  [ ! -d "$SOURCE/.git/rebase-merge" ] && [ ! -d "$SOURCE/.git/rebase-apply" ] || { fail ACTIVE_GIT_OPERATION TARGET_SYNCHRONIZATION; return; }
  printf 'REPOSITORY_PRECONDITION=PASS\n'
  git -C "$SOURCE" fetch origin >/dev/null 2>&1 || { fail GIT_FETCH_FAILED TARGET_SYNCHRONIZATION; return; }
  [ "$(git -C "$SOURCE" rev-parse origin/main 2>/dev/null)" = "$GOVERNANCE_COMMIT" ] || { fail GOVERNANCE_COMMIT_MISMATCH TARGET_SYNCHRONIZATION; return; }
  git -C "$SOURCE" merge-base --is-ancestor HEAD origin/main >/dev/null 2>&1 || { fail NON_FAST_FORWARD_SOURCE TARGET_SYNCHRONIZATION; return; }
  git -C "$SOURCE" merge --ff-only origin/main >/dev/null 2>&1 || { fail FAST_FORWARD_FAILED TARGET_SYNCHRONIZATION; return; }
  printf 'REPOSITORY_SYNCHRONIZATION=PASS\n'
  [ "$(git -C "$SOURCE" rev-parse HEAD 2>/dev/null)" = "$GOVERNANCE_COMMIT" ] || { fail POST_SYNC_HEAD_MISMATCH TARGET_SYNCHRONIZATION; return; }
  [ -z "$(git -C "$SOURCE" status --porcelain 2>/dev/null)" ] || { fail POST_SYNC_REPOSITORY_DIRTY TARGET_SYNCHRONIZATION; return; }
  printf 'SYNCHRONIZED_HEAD_IDENTITY=PASS\n'
  [ -f "$SCRIPT" ] && [ ! -L "$SCRIPT" ] || { fail ACTION4_RESUME_SCRIPT_MISSING SCRIPT_AVAILABILITY; return; }
  printf 'ACTION4_RESUME_SCRIPT_AVAILABILITY=PASS\n'
  [ "$(git -C "$SOURCE" rev-parse "$GOVERNANCE_COMMIT:$SCRIPT_REL" 2>/dev/null)" = "$SCRIPT_BLOB" ] || { fail ACTION4_SCRIPT_GIT_IDENTITY_MISMATCH SCRIPT_AVAILABILITY; return; }
  [ "$(git -C "$SOURCE" hash-object --path="$SCRIPT_REL" "$SCRIPT" 2>/dev/null)" = "$SCRIPT_BLOB" ] && git -C "$SOURCE" diff --quiet -- "$SCRIPT_REL" || { fail ACTION4_SCRIPT_WORKTREE_IDENTITY_MISMATCH SCRIPT_AVAILABILITY; return; }
  printf 'ACTION4_RESUME_SCRIPT_IDENTITY=PASS\nACTION4A=COMPLETE\nRESULT=PASS\n'
}
hioc_pe3_action4a_sync
```

Action 4A must stop after its eight exact PASS lines. Return the output for
review. No shell block or script may chain Action 4A into Action 4B.

### Action 4B — staging permission normalization and manufacturer validation

Action 4B requires separate authorization after reviewed Action 4A PASS. It is
the unchanged repository-controlled resume script:

```bash
set +x
bash /home/jazofv1/hioc-release-source/tools/hioc-pe3-action4-resume-permissions.sh \
  --governance-commit '<approved-full-40-hex-action4a-sync-commit>'
```

Canonical script identity (UTF-8, LF): SHA-256
`31561b166d9d272c18767789e56dc126a107f7ce42b21ac93f81d37737e003a6`; Git blob
`0602d9f460bf127bac4be953686fad1c0700c14e`. Success evidence is exactly the
validator's privacy-safe JSON plus these separate barriers: `SOURCE_IDENTITY_RECHECK=PASS`,
`STAGING_IDENTITY_RECHECK=PASS`, `STAGING_PERMISSION_NORMALIZATION=PASS`,
`POST_NORMALIZATION_IDENTITY=PASS`, `MANUFACTURER_VALIDATION=PASS`,
`ACTION4=COMPLETE`, and final `RESULT=PASS`.

Every failure emits exact `RESULT`, `ERROR_CODE`, and `FAILURE_STAGE` fields and
returns from the governed script process. Source drift, staging drift,
unsupported initial mode, chmod failure, post-normalization directory/content/
owner/type/mode/size/hash drift, validator failure, privacy failure, and record
count mismatch each stop before later stages. The script contains no shell-level
`set -e`, no interactive-shell `exit`, and cannot terminate its parent Bash.
Return its sanitized output and stop. Do not proceed to Action 5 automatically.
If Action 4A fails, Action 4B is never invoked and the preserved staging path is
never referenced or changed. Action 4B owns the existing script PASS contract.
Its final `ACTION4=COMPLETE` means both reviewed Action 4A PASS and separately
authorized Action 4B PASS. Action 4B must stop before Action 5.

## Action 5 — Supported code deployment and artifact identity

### Action 5A — target repository synchronization and Action 5 script identity

PI3 release source was last governed at
`3ae13bf35db7cf133540a50d481a8de2e26b222d`, before the Action 5 deployment
script existed. Action 5A is therefore a separate bootstrap-safe,
non-deployment trust boundary. It synchronizes only a clean, fast-forwardable
`main` checkout to the exact approved commit, proves the Action 5 script's Git
and worktree identity, emits sanitized evidence, and stops. It never references
staging, creates backup state, validates or changes runtime, invokes Action 5B,
or prepares Action 6.

Target: **PI3 NUT&PIHOLE**, interactive Bash. Replace the placeholder only with
the approved full 40-hex commit containing this prerequisite and the Action 5
script.

```bash
set +x
hioc_pe3_action5a_sync() {
  SOURCE=/home/jazofv1/hioc-release-source
  SCRIPT_REL=tools/hioc-pe3-action5-deploy.sh
  SCRIPT="$SOURCE/$SCRIPT_REL"
  GOVERNANCE_COMMIT='<approved-full-40-hex-action5-bootstrap-commit>'
  SCRIPT_BLOB=b493be45d42c7732f353519beec23fa62d45a942
  fail() { printf 'RESULT=INPUT_OR_PRECONDITION_ERROR\nERROR_CODE=%s\nFAILURE_STAGE=%s\n' "$1" "$2"; return 1; }
  [ "$(hostname -s 2>/dev/null)" = nutandpihole ] || { fail WRONG_TARGET TARGET_SYNCHRONIZATION; return; }
  ip -o -4 addr show scope global 2>/dev/null | awk '{print $4}' | cut -d/ -f1 | grep -Fxq 192.168.100.252 || { fail WRONG_TARGET TARGET_SYNCHRONIZATION; return; }
  printf 'TARGET_IDENTITY=PASS\n'
  [ -d "$SOURCE/.git" ] || { fail SOURCE_REPOSITORY_MISSING TARGET_SYNCHRONIZATION; return; }
  [ "$(git -C "$SOURCE" branch --show-current 2>/dev/null)" = main ] || { fail WRONG_BRANCH TARGET_SYNCHRONIZATION; return; }
  [ -z "$(git -C "$SOURCE" status --porcelain 2>/dev/null)" ] || { fail SOURCE_REPOSITORY_DIRTY TARGET_SYNCHRONIZATION; return; }
  for marker in MERGE_HEAD REBASE_HEAD CHERRY_PICK_HEAD REVERT_HEAD BISECT_LOG; do [ ! -e "$SOURCE/.git/$marker" ] || { fail ACTIVE_GIT_OPERATION TARGET_SYNCHRONIZATION; return; }; done
  [ ! -d "$SOURCE/.git/rebase-merge" ] && [ ! -d "$SOURCE/.git/rebase-apply" ] || { fail ACTIVE_GIT_OPERATION TARGET_SYNCHRONIZATION; return; }
  printf 'REPOSITORY_PRECONDITION=PASS\n'
  git -C "$SOURCE" fetch origin >/dev/null 2>&1 || { fail GIT_FETCH_FAILED TARGET_SYNCHRONIZATION; return; }
  [ "$(git -C "$SOURCE" rev-parse origin/main 2>/dev/null)" = "$GOVERNANCE_COMMIT" ] || { fail GOVERNANCE_COMMIT_MISMATCH TARGET_SYNCHRONIZATION; return; }
  git -C "$SOURCE" merge-base --is-ancestor HEAD origin/main >/dev/null 2>&1 || { fail NON_FAST_FORWARD_SOURCE TARGET_SYNCHRONIZATION; return; }
  git -C "$SOURCE" merge --ff-only origin/main >/dev/null 2>&1 || { fail FAST_FORWARD_FAILED TARGET_SYNCHRONIZATION; return; }
  printf 'REPOSITORY_SYNCHRONIZATION=PASS\n'
  [ "$(git -C "$SOURCE" rev-parse HEAD 2>/dev/null)" = "$GOVERNANCE_COMMIT" ] || { fail POST_SYNC_HEAD_MISMATCH TARGET_SYNCHRONIZATION; return; }
  [ -z "$(git -C "$SOURCE" status --porcelain 2>/dev/null)" ] || { fail POST_SYNC_REPOSITORY_DIRTY TARGET_SYNCHRONIZATION; return; }
  printf 'SYNCHRONIZED_HEAD_IDENTITY=PASS\n'
  [ -e "$SCRIPT" ] || { fail ACTION5_SCRIPT_MISSING SCRIPT_AVAILABILITY; return; }
  [ -f "$SCRIPT" ] && [ ! -L "$SCRIPT" ] || { fail ACTION5_SCRIPT_NOT_REGULAR SCRIPT_AVAILABILITY; return; }
  printf 'ACTION5_SCRIPT_AVAILABILITY=PASS\n'
  [ "$(git -C "$SOURCE" rev-parse "$GOVERNANCE_COMMIT:$SCRIPT_REL" 2>/dev/null)" = "$SCRIPT_BLOB" ] || { fail ACTION5_SCRIPT_GIT_IDENTITY_MISMATCH SCRIPT_IDENTITY; return; }
  [ "$(git -C "$SOURCE" hash-object --path="$SCRIPT_REL" "$SCRIPT" 2>/dev/null)" = "$SCRIPT_BLOB" ] && git -C "$SOURCE" diff --quiet -- "$SCRIPT_REL" || { fail ACTION5_SCRIPT_WORKTREE_IDENTITY_MISMATCH SCRIPT_IDENTITY; return; }
  printf 'ACTION5_SCRIPT_IDENTITY=PASS\nACTION5A=COMPLETE\nRESULT=PASS\n'
}
hioc_pe3_action5a_sync
```

Action 5A must stop after its eight exact PASS lines. Any failure emits exact
`RESULT`, `ERROR_CODE`, and `FAILURE_STAGE`, suppresses later checks, and returns
control to the parent shell. Action 5A PASS must be reviewed and separately
authorized before Action 5B. No procedure may auto-chain them.

### Action 5B — supported code deployment

Target: PI3 runtime through the supported release workflow. Mutation: runtime
code and timestamped release backup. Rollback relevance: code domain.

```bash
bash /home/jazofv1/hioc-release-source/tools/hioc-pe3-action5-deploy.sh \
  --governance-commit '<approved-full-40-hex-action5-bootstrap-commit>'
```

The checked-in script is the sole executable Action 5B implementation. Before
mutation it proves target identity, exact source/governance identity, its own
Git-object/worktree identity, implementation ancestry, source artifact identity,
and release validation. It then uses only `release/upgrade.sh`, proves the new
timestamped rollback backup, validates the deployed runtime, verifies the ten
governed runtime artifacts against Git-derived SHA-256 values, and applies a
semantic manufacturer-protection comparison. It protects installed versions,
database, manifest, sidecar, status, and configuration state while allowing
only installer-managed creation or `0700` normalization of empty scaffolding.

Canonical Action 5 script identity for this correction:

- SHA-256: `7cc9e0b7a0c3b06055b329cafdf71fe55ae362a8c1e67b870d8c04655771c690`
- Git blob: `b493be45d42c7732f353519beec23fa62d45a942`

PASS requires, exactly once, `TARGET_IDENTITY=PASS`, `SOURCE_IDENTITY=PASS`,
`RELEASE_VALIDATION=PASS`, `RELEASE_BACKUP=PASS`, `CODE_DEPLOYMENT=PASS`,
`RUNTIME_VALIDATION=PASS`, `MANUFACTURER_PAYLOAD_UNTOUCHED=PASS`,
`MANUFACTURER_SCAFFOLDING_STATE=PASS`, `CONFIGURATION_UNTOUCHED=PASS`,
`RUNTIME_ARTIFACT_IDENTITY=PASS`,
`EVIDENCE_REPORT=PASS`, `ACTION5=COMPLETE`, `RESULT=PASS`, and
`ROLLBACK_RECOMMENDED=FALSE`, plus the private `EVIDENCE_DIR` and validated
`RELEASE_BACKUP_PATH`. Any failure emits bounded `RESULT`, `ERROR_CODE`,
`FAILURE_STAGE`, and `ROLLBACK_RECOMMENDED` and stops later stages while leaving
the parent shell alive. Failures before runtime mutation report rollback false;
a failed upgrade with a newly created backup, an invalid new backup after a
successful upgrade, or any post-deployment validation/identity failure reports
rollback true. Rollback is never automatic. Do not authorize Action 6 without
reviewing all PASS evidence. Dataset installation and configuration activation
remain later actions.

The first Action 5B execution reached successful code deployment and runtime
validation but the former raw recursive fingerprint treated installer-created,
empty private scaffolding as `MANUFACTURER_DATASET_CHANGED`. Read-only forensics
proved the manufacturer root contained only an empty `versions` directory;
both directories were real, owned by `jazofv1:jazofv1`, and mode `0700`. No
version, database, manifest, sidecar, status artifact, or configuration
activation existed. This is **ACTION 5 PROTECTION SNAPSHOT FALSE POSITIVE —
RELEASE-MANAGED EMPTY MANUFACTURER SCAFFOLDING**. Rollback is not recommended:
it would rerun the same installer scaffolding logic. Genuine payload or
configuration mutation remains a post-deployment failure with
rollback/investigation recommended.

### Action 5C — read-only post-deployment protection revalidation and closure

Action 5C is the smallest safe closure for that already-deployed runtime and
does not repeat deployment. It rechecks source/script identity, implementation
ancestry, the preserved release-backup pointer, release/runtime validation,
runtime artifact identities, exact empty/private manufacturer scaffolding,
absence of payload/sidecar/status artifacts, and inactive configuration.

Canonical Action 5C script identity:

- path: `tools/hioc-pe3-action5c-revalidate.sh`
- SHA-256: `f58346ac943c56e74fd5235fae7f02a1519337cb3eca1be90ca1d6312093e55a`
- Git blob: `da47aa4a3d0346432332fc42f4111a956fd8e1bd`

Because this script is new, the target may predate it. This is **PE-3 ACTION 5C
BOOTSTRAP CONTRACT MISSING — TARGET MAY PREDATE REVALIDATION SCRIPT**, a
governance/runbook deficiency rather than a production failure. Action 5C is
therefore split into two separately authorized boundaries.

#### Action 5C-A — Target Repository Synchronization & Action 5C Script Identity

Action 5C-A is an inline, bootstrap-safe, non-deployment procedure because the
stale target cannot be assumed to contain a new repository-controlled script.
It owns only target identity, clean fast-forward synchronization of the
release-source `main` checkout to the exact approved governance commit, and the
Action 5C script's availability plus Git/worktree identity. It does not inspect
or change the runtime, manufacturer payload, staging, configuration, backups,
or sidecars; it does not invoke Action 5C-B, rollback, deployment, or Action 6.

Target: **PI3 NUT&PIHOLE**, interactive Bash. Replace the governance placeholder
only with the approved full 40-hex commit containing this gate and the canonical
Action 5C script.

```bash
set +x
hioc_pe3_action5c_a_sync() {
  SOURCE=/home/jazofv1/hioc-release-source
  SCRIPT_REL=tools/hioc-pe3-action5c-revalidate.sh
  SCRIPT="$SOURCE/$SCRIPT_REL"
  GOVERNANCE_COMMIT='<approved-full-40-hex-action5c-bootstrap-commit>'
  SCRIPT_BLOB=da47aa4a3d0346432332fc42f4111a956fd8e1bd
  fail() { printf 'RESULT=INPUT_OR_PRECONDITION_ERROR\nERROR_CODE=%s\nFAILURE_STAGE=%s\n' "$1" "$2"; return 1; }
  [ "$(hostname -s 2>/dev/null)" = nutandpihole ] || { fail WRONG_TARGET TARGET_SYNCHRONIZATION; return; }
  ip -o -4 addr show scope global 2>/dev/null | awk '{print $4}' | cut -d/ -f1 | grep -Fxq 192.168.100.252 || { fail WRONG_TARGET TARGET_SYNCHRONIZATION; return; }
  printf 'TARGET_IDENTITY=PASS\n'
  [ -d "$SOURCE/.git" ] || { fail SOURCE_REPOSITORY_MISSING TARGET_SYNCHRONIZATION; return; }
  [ "$(git -C "$SOURCE" branch --show-current 2>/dev/null)" = main ] || { fail WRONG_BRANCH TARGET_SYNCHRONIZATION; return; }
  [ -z "$(git -C "$SOURCE" status --porcelain 2>/dev/null)" ] || { fail SOURCE_REPOSITORY_DIRTY TARGET_SYNCHRONIZATION; return; }
  for marker in MERGE_HEAD REBASE_HEAD CHERRY_PICK_HEAD REVERT_HEAD BISECT_LOG; do [ ! -e "$SOURCE/.git/$marker" ] || { fail ACTIVE_GIT_OPERATION TARGET_SYNCHRONIZATION; return; }; done
  [ ! -d "$SOURCE/.git/rebase-merge" ] && [ ! -d "$SOURCE/.git/rebase-apply" ] || { fail ACTIVE_GIT_OPERATION TARGET_SYNCHRONIZATION; return; }
  printf 'REPOSITORY_PRECONDITION=PASS\n'
  git -C "$SOURCE" fetch origin >/dev/null 2>&1 || { fail GIT_FETCH_FAILED TARGET_SYNCHRONIZATION; return; }
  [ "$(git -C "$SOURCE" rev-parse origin/main 2>/dev/null)" = "$GOVERNANCE_COMMIT" ] || { fail GOVERNANCE_COMMIT_MISMATCH TARGET_SYNCHRONIZATION; return; }
  git -C "$SOURCE" merge-base --is-ancestor HEAD origin/main >/dev/null 2>&1 || { fail NON_FAST_FORWARD_SOURCE TARGET_SYNCHRONIZATION; return; }
  git -C "$SOURCE" merge --ff-only origin/main >/dev/null 2>&1 || { fail FAST_FORWARD_FAILED TARGET_SYNCHRONIZATION; return; }
  printf 'REPOSITORY_SYNCHRONIZATION=PASS\n'
  [ "$(git -C "$SOURCE" rev-parse HEAD 2>/dev/null)" = "$GOVERNANCE_COMMIT" ] || { fail POST_SYNC_HEAD_MISMATCH TARGET_SYNCHRONIZATION; return; }
  [ -z "$(git -C "$SOURCE" status --porcelain 2>/dev/null)" ] || { fail POST_SYNC_REPOSITORY_DIRTY TARGET_SYNCHRONIZATION; return; }
  printf 'SYNCHRONIZED_HEAD_IDENTITY=PASS\n'
  [ -e "$SCRIPT" ] || { fail ACTION5C_SCRIPT_MISSING SCRIPT_AVAILABILITY; return; }
  [ -f "$SCRIPT" ] && [ ! -L "$SCRIPT" ] || { fail ACTION5C_SCRIPT_NOT_REGULAR SCRIPT_AVAILABILITY; return; }
  printf 'ACTION5C_SCRIPT_AVAILABILITY=PASS\n'
  [ "$(git -C "$SOURCE" rev-parse "$GOVERNANCE_COMMIT:$SCRIPT_REL" 2>/dev/null)" = "$SCRIPT_BLOB" ] || { fail ACTION5C_SCRIPT_GIT_IDENTITY_MISMATCH SCRIPT_IDENTITY; return; }
  [ "$(git -C "$SOURCE" hash-object --path="$SCRIPT_REL" "$SCRIPT" 2>/dev/null)" = "$SCRIPT_BLOB" ] && git -C "$SOURCE" diff --quiet -- "$SCRIPT_REL" || { fail ACTION5C_SCRIPT_WORKTREE_IDENTITY_MISMATCH SCRIPT_IDENTITY; return; }
  printf 'ACTION5C_SCRIPT_IDENTITY=PASS\nACTION5C_A=COMPLETE\nRESULT=PASS\n'
}
hioc_pe3_action5c_a_sync
```

Action 5C-A stops after its eight exact PASS lines. Any failure emits exact
`RESULT`, `ERROR_CODE`, and `FAILURE_STAGE`, suppresses later checks, returns
control to the parent shell, and leaves Action 5 incomplete. No command may
auto-chain Action 5C-A into Action 5C-B.

#### Action 5C-B — Read-only Action 5 Revalidation & Closure

Only after reviewed Action 5C-A PASS and separate authorization may Action 5C-B
be prepared and invoked. It requires `--governance-commit <full-40-hex>` and
`--release-backup </home/jazofv1/hioc/backups/release-upgrade-*>`. The preserved
Action 5B backup for that later authorization is exactly
`/home/jazofv1/hioc/backups/release-upgrade-20260812-133550`; no other path may
be inferred or substituted. No Action 5C-B invocation is prepared by this
checkpoint.

Action 5C-B PASS requires `TARGET_IDENTITY=PASS`,
`SOURCE_IDENTITY=PASS`, `RELEASE_BACKUP_IDENTITY=PASS`,
`RELEASE_VALIDATION=PASS`, `RUNTIME_VALIDATION=PASS`,
`RUNTIME_ARTIFACT_IDENTITY=PASS`, `MANUFACTURER_PAYLOAD_UNTOUCHED=PASS`,
`MANUFACTURER_SCAFFOLDING_STATE=PASS`, `CONFIGURATION_UNTOUCHED=PASS`,
`ACTION5B_DEPLOYMENT_EVIDENCE=PRESERVED`, `EVIDENCE_REPORT=PASS`,
`ACTION5=COMPLETE`, `RESULT=PASS`, and `ROLLBACK_RECOMMENDED=FALSE`.
Any failure leaves Action 5 incomplete and Action 6 unauthorized.

## Action 6 — Immutable dataset installation

Target: PI3 runtime data root. Mutation: one immutable version-directory
creation. Rollback relevance: dataset domain; no existing dataset is deleted.

Order is frozen as sync, supported code deployment, runtime validation, staged
dataset validation, immutable installation, configuration, final validation,
generation, and sidecar validation. This guarantees an unvalidated dataset is
never active and rollback-capable code exists before activation.

The former inline Action 6 block is retired as **PE-3 ACTION 6 OPERATOR-SAFETY
AND EVIDENCE CONTRACT DEFECT — IMMUTABLE DATASET INSTALLATION PROCEDURE NOT
PRODUCTION-SAFE**. It contained an unresolved staging placeholder, enabled
interactive `set -euo pipefail`, used `exit 0`, relied on bare assertions, and
lacked bounded failure and complete PASS evidence. Action 6 was not executed;
this is a governance/runbook defect, not a production failure.

The exact preserved transport staging path is
`/tmp/hioc-pe3-dataset-transfer-PJ5qPbRS`. Action 6 is now split into two
separately authorized boundaries because PI3 may predate the new governed
installer.

### Action 6-A — target synchronization and Action 6 script identity

Action 6-A is bootstrap-safe and inline. It owns only clean fast-forward
synchronization to the approved governance commit and exact Action 6 script
Git/worktree identity, then stops. It never references transport staging or the
runtime and never invokes Action 6-B or Action 7.

```bash
set +x
hioc_pe3_action6_a_sync() {
  SOURCE=/home/jazofv1/hioc-release-source
  SCRIPT_REL=tools/hioc-pe3-action6-install.sh
  SCRIPT="$SOURCE/$SCRIPT_REL"
  GOVERNANCE_COMMIT='<approved-full-40-hex-action6-bootstrap-commit>'
  SCRIPT_BLOB=c8bd1e00a9113a67bf12c96b1e402f8380c7ede9
  fail() { printf 'RESULT=INPUT_OR_PRECONDITION_ERROR\nERROR_CODE=%s\nFAILURE_STAGE=%s\n' "$1" "$2"; return 1; }
  [ "$(hostname -s 2>/dev/null)" = nutandpihole ] || { fail WRONG_TARGET TARGET_SYNCHRONIZATION; return; }
  ip -o -4 addr show scope global 2>/dev/null | awk '{print $4}' | cut -d/ -f1 | grep -Fxq 192.168.100.252 || { fail WRONG_TARGET TARGET_SYNCHRONIZATION; return; }
  printf 'TARGET_IDENTITY=PASS\n'
  [ -d "$SOURCE/.git" ] || { fail SOURCE_REPOSITORY_MISSING TARGET_SYNCHRONIZATION; return; }
  [ "$(git -C "$SOURCE" branch --show-current 2>/dev/null)" = main ] || { fail WRONG_BRANCH TARGET_SYNCHRONIZATION; return; }
  [ -z "$(git -C "$SOURCE" status --porcelain 2>/dev/null)" ] || { fail SOURCE_REPOSITORY_DIRTY TARGET_SYNCHRONIZATION; return; }
  for marker in MERGE_HEAD REBASE_HEAD CHERRY_PICK_HEAD REVERT_HEAD BISECT_LOG; do [ ! -e "$SOURCE/.git/$marker" ] || { fail ACTIVE_GIT_OPERATION TARGET_SYNCHRONIZATION; return; }; done
  [ ! -d "$SOURCE/.git/rebase-merge" ] && [ ! -d "$SOURCE/.git/rebase-apply" ] || { fail ACTIVE_GIT_OPERATION TARGET_SYNCHRONIZATION; return; }
  printf 'REPOSITORY_PRECONDITION=PASS\n'
  git -C "$SOURCE" fetch origin >/dev/null 2>&1 || { fail GIT_FETCH_FAILED TARGET_SYNCHRONIZATION; return; }
  [ "$(git -C "$SOURCE" rev-parse origin/main 2>/dev/null)" = "$GOVERNANCE_COMMIT" ] || { fail GOVERNANCE_COMMIT_MISMATCH TARGET_SYNCHRONIZATION; return; }
  git -C "$SOURCE" merge-base --is-ancestor HEAD origin/main >/dev/null 2>&1 || { fail NON_FAST_FORWARD_SOURCE TARGET_SYNCHRONIZATION; return; }
  git -C "$SOURCE" merge --ff-only origin/main >/dev/null 2>&1 || { fail FAST_FORWARD_FAILED TARGET_SYNCHRONIZATION; return; }
  printf 'REPOSITORY_SYNCHRONIZATION=PASS\n'
  [ "$(git -C "$SOURCE" rev-parse HEAD 2>/dev/null)" = "$GOVERNANCE_COMMIT" ] || { fail POST_SYNC_HEAD_MISMATCH TARGET_SYNCHRONIZATION; return; }
  [ -z "$(git -C "$SOURCE" status --porcelain 2>/dev/null)" ] || { fail POST_SYNC_REPOSITORY_DIRTY TARGET_SYNCHRONIZATION; return; }
  printf 'SYNCHRONIZED_HEAD_IDENTITY=PASS\n'
  [ -e "$SCRIPT" ] || { fail ACTION6_SCRIPT_MISSING SCRIPT_AVAILABILITY; return; }
  [ -f "$SCRIPT" ] && [ ! -L "$SCRIPT" ] || { fail ACTION6_SCRIPT_NOT_REGULAR SCRIPT_AVAILABILITY; return; }
  printf 'ACTION6_SCRIPT_AVAILABILITY=PASS\n'
  [ "$(git -C "$SOURCE" rev-parse "$GOVERNANCE_COMMIT:$SCRIPT_REL" 2>/dev/null)" = "$SCRIPT_BLOB" ] || { fail ACTION6_SCRIPT_GIT_IDENTITY_MISMATCH SCRIPT_IDENTITY; return; }
  [ "$(git -C "$SOURCE" hash-object --path="$SCRIPT_REL" "$SCRIPT" 2>/dev/null)" = "$SCRIPT_BLOB" ] && git -C "$SOURCE" diff --quiet -- "$SCRIPT_REL" || { fail ACTION6_SCRIPT_WORKTREE_IDENTITY_MISMATCH SCRIPT_IDENTITY; return; }
  printf 'ACTION6_SCRIPT_IDENTITY=PASS\nACTION6_A=COMPLETE\nRESULT=PASS\n'
}
hioc_pe3_action6_a_sync
```

Action 6-A must stop after its eight exact PASS lines. Any failure emits bounded
`RESULT`, `ERROR_CODE`, and `FAILURE_STAGE`, returns control to the parent shell,
and leaves Action 6 not started. Action 6-B requires reviewed Action 6-A PASS
and separate authorization; no command may auto-chain them.

### Action 6-B — governed immutable dataset installation

The sole implementation is
`tools/hioc-pe3-action6-install.sh` (SHA-256
`ceb5e2e6f116b3726d4ea73886a4fe035a29931955408e5938f14bf642407895`,
Git blob `c8bd1e00a9113a67bf12c96b1e402f8380c7ede9`). After reviewed Action 6-A
PASS and separate authorization, the operator uses only:

```bash
bash /home/jazofv1/hioc-release-source/tools/hioc-pe3-action6-install.sh \
  --governance-commit '<approved-full-40-hex-action6-bootstrap-commit>'
```

Before mutation the script proves target, source, script, validator, runtime,
configuration, and exact transport-staging identity, including exact two-file
contents, owner/mode, byte sizes, hashes, absence of CSV, and privacy-safe
validator result `PASS` with 53,581 records. It creates only a unique hidden
`.action6-install-*` directory under the runtime manufacturer data root, copies
the two files at `0600`, revalidates them, fsyncs both files and relevant
directories, and uses Linux `renameat2(..., RENAME_NOREPLACE)` for atomic
publication. A
byte-for-byte and invariant-identical existing final version is accepted
without replacement; any difference is `IMMUTABLE_VERSION_CONFLICT` and leaves
it untouched. Cleanup is limited to the exact invocation-owned hidden staging
directory; transport staging and installed versions are never removed.

New-install PASS requires, in order, `TARGET_IDENTITY=PASS`,
`SOURCE_IDENTITY=PASS`, `STAGING_IDENTITY=PASS`, `STAGING_VALIDATION=PASS`,
`IMMUTABLE_INSTALLATION=PASS_NEW`, `FINAL_DATASET_IDENTITY=PASS`,
`FINAL_DATASET_VALIDATION=PASS`, `CONFIGURATION_UNTOUCHED=PASS`,
`ACTION6=COMPLETE`, and `RESULT=PASS`. Idempotent PASS substitutes only
`IMMUTABLE_INSTALLATION=PASS_ALREADY_IDENTICAL`. Any failure emits bounded
`RESULT`, `ERROR_CODE`, `FAILURE_STAGE`, and `ROLLBACK_RECOMMENDED=FALSE`,
returns control to the parent prompt, leaves Action 6 incomplete, and keeps
Action 7 unauthorized. Action 6 never changes `MANUFACTURER_DB_PATH`, generates
sidecars/status, cleans transport staging, or invokes Action 7.

## Action 7 — Configuration activation

Target: PI3 runtime configuration. Mutation: conditional atomic configuration
update plus exact backup. Rollback relevance: configuration domain.

### Pre-execution governance correction

The historical inline Action 7 block below this heading was rejected before
execution as **PE-3 ACTION 7 OPERATOR-SAFETY AND EVIDENCE CONTRACT DEFECT —
CONFIGURATION ACTIVATION PROCEDURE NOT PRODUCTION-SAFE**. It enabled interactive
`set -euo pipefail`, used shell-level `exit`, depended on an unresolved evidence
directory, embedded substantial mutation in chat-sized shell, and lacked closed
source, runtime, immutable-dataset, backup, post-publication, and rollback
evidence. Action 7 remains **NOT STARTED** and the installed immutable dataset,
runtime configuration, sidecars/status, and transport staging remain untouched.

Action 7 is split into two separately authorized boundaries because PI3 does
not yet contain the new governed activation script.

### Action 7-A — target synchronization and Action 7 script identity

Action 7-A is bootstrap-safe. It owns only clean fast-forward synchronization
to the approved governance commit and exact Action 7 script Git/worktree
identity, then stops. The governance commit and script blob must be frozen from
the reviewed post-push repository before this block is authorized; the block is
not executable while either marked value remains unresolved.

```bash
set +x
hioc_pe3_action7_a_sync() {
  SOURCE=/home/jazofv1/hioc-release-source
  SCRIPT_REL=tools/hioc-pe3-action7-activate.sh
  SCRIPT="$SOURCE/$SCRIPT_REL"
  GOVERNANCE_COMMIT='<approved-full-40-hex-action7-bootstrap-commit>'
  SCRIPT_BLOB='<approved-action7-script-git-blob>'
  fail() { printf 'RESULT=INPUT_OR_PRECONDITION_ERROR\nERROR_CODE=%s\nFAILURE_STAGE=%s\nROLLBACK_RECOMMENDED=FALSE\n' "$1" "$2"; return 1; }
  [ "$(hostname -s 2>/dev/null)" = nutandpihole ] || { fail WRONG_TARGET TARGET_SYNCHRONIZATION; return; }
  ip -o -4 addr show scope global 2>/dev/null | awk '{print $4}' | cut -d/ -f1 | grep -Fxq 192.168.100.252 || { fail WRONG_TARGET TARGET_SYNCHRONIZATION; return; }
  printf 'TARGET_IDENTITY=PASS\n'
  [ -d "$SOURCE/.git" ] || { fail SOURCE_REPOSITORY_MISSING TARGET_SYNCHRONIZATION; return; }
  [ "$(git -C "$SOURCE" branch --show-current 2>/dev/null)" = main ] || { fail WRONG_BRANCH TARGET_SYNCHRONIZATION; return; }
  [ -z "$(git -C "$SOURCE" status --porcelain 2>/dev/null)" ] || { fail SOURCE_REPOSITORY_DIRTY TARGET_SYNCHRONIZATION; return; }
  for marker in MERGE_HEAD REBASE_HEAD CHERRY_PICK_HEAD REVERT_HEAD BISECT_LOG; do [ ! -e "$SOURCE/.git/$marker" ] || { fail ACTIVE_GIT_OPERATION TARGET_SYNCHRONIZATION; return; }; done
  [ ! -d "$SOURCE/.git/rebase-merge" ] && [ ! -d "$SOURCE/.git/rebase-apply" ] || { fail ACTIVE_GIT_OPERATION TARGET_SYNCHRONIZATION; return; }
  printf 'REPOSITORY_PRECONDITION=PASS\n'
  git -C "$SOURCE" fetch origin >/dev/null 2>&1 || { fail GIT_FETCH_FAILED TARGET_SYNCHRONIZATION; return; }
  [ "$(git -C "$SOURCE" rev-parse origin/main 2>/dev/null)" = "$GOVERNANCE_COMMIT" ] || { fail GOVERNANCE_COMMIT_MISMATCH TARGET_SYNCHRONIZATION; return; }
  git -C "$SOURCE" merge-base --is-ancestor HEAD origin/main >/dev/null 2>&1 || { fail NON_FAST_FORWARD_SOURCE TARGET_SYNCHRONIZATION; return; }
  git -C "$SOURCE" merge --ff-only origin/main >/dev/null 2>&1 || { fail FAST_FORWARD_FAILED TARGET_SYNCHRONIZATION; return; }
  printf 'REPOSITORY_SYNCHRONIZATION=PASS\n'
  [ "$(git -C "$SOURCE" rev-parse HEAD 2>/dev/null)" = "$GOVERNANCE_COMMIT" ] || { fail POST_SYNC_HEAD_MISMATCH TARGET_SYNCHRONIZATION; return; }
  [ -z "$(git -C "$SOURCE" status --porcelain 2>/dev/null)" ] || { fail POST_SYNC_REPOSITORY_DIRTY TARGET_SYNCHRONIZATION; return; }
  printf 'SYNCHRONIZED_HEAD_IDENTITY=PASS\n'
  [ -f "$SCRIPT" ] && [ ! -L "$SCRIPT" ] || { fail ACTION7_SCRIPT_MISSING SCRIPT_AVAILABILITY; return; }
  printf 'ACTION7_SCRIPT_AVAILABILITY=PASS\n'
  [ "$(git -C "$SOURCE" rev-parse "$GOVERNANCE_COMMIT:$SCRIPT_REL" 2>/dev/null)" = "$SCRIPT_BLOB" ] || { fail ACTION7_SCRIPT_GIT_IDENTITY_MISMATCH SCRIPT_IDENTITY; return; }
  [ "$(git -C "$SOURCE" hash-object --path="$SCRIPT_REL" "$SCRIPT" 2>/dev/null)" = "$SCRIPT_BLOB" ] && git -C "$SOURCE" diff --quiet -- "$SCRIPT_REL" || { fail ACTION7_SCRIPT_WORKTREE_IDENTITY_MISMATCH SCRIPT_IDENTITY; return; }
  printf 'ACTION7_SCRIPT_IDENTITY=PASS\nACTION7_A=COMPLETE\nRESULT=PASS\n'
}
hioc_pe3_action7_a_sync
```

Action 7-A must stop after its eight exact PASS lines. It never reads or changes
runtime configuration, the immutable dataset, sidecars/status, or transport
staging and cannot invoke Action 7-B or Action 8. Any failure returns bounded
evidence to the surviving parent shell. Action 7-B requires reviewed Action 7-A
PASS and separate authorization.

### Action 7-B — governed configuration activation

The sole implementation is `tools/hioc-pe3-action7-activate.sh`. After reviewed
Action 7-A PASS and separate authorization, the operator uses only:

```bash
bash /home/jazofv1/hioc-release-source/tools/hioc-pe3-action7-activate.sh \
  --governance-commit '<approved-full-40-hex-action7-bootstrap-commit>'
```

Action 7-B proves target, source, script, validator, generator, runtime, exact
immutable version, file ownership/modes/sizes/hashes, privacy-safe database PASS,
and the configuration precondition before mutation. The only permitted setting
is `MANUFACTURER_DB_PATH`, selecting
`/home/jazofv1/hioc/data/manufacturer/versions/local-ieee-ra--2026-08-11-r1/manufacturer-db.json`.
Absent or empty values activate after a private durable exact backup. The exact
intended value at private mode `0600` is an idempotent no-op without another
backup; the intended value at a safe owner-matched but broader read-only mode is
backed up and atomically normalized to `0600`. Duplicate keys, group/world-
writable configuration, or any different nonempty value fail closed and are
never overwritten.

Publication changes only that key, preserves all other lines, uses one private
same-directory temporary file and atomic replacement, and fsyncs the file and
configuration directory. Action 7 does not generate or modify manufacturer
sidecar/status artifacts, restart or reload a service, change systemd, cron,
timers, environment configuration, dataset permissions/ownership/content, or
transport staging. The manual generator first consumes the activated setting in
separately authorized Action 8.

PASS requires `TARGET_IDENTITY`, `SOURCE_IDENTITY`, `RUNTIME_IDENTITY`,
`DATASET_IDENTITY`, `DATASET_VALIDATION`, `CONFIGURATION_PRECONDITION`, one
`CONFIGURATION_BACKUP` disposition, one `CONFIGURATION_ACTIVATION` disposition,
`CONFIGURATION_VALIDATION`, `RUNTIME_DATASET_SELECTION`,
`POST_ACTIVATION_VALIDATION`, `ACTION7=COMPLETE`, and `RESULT=PASS`. Failure
reports `RESULT`, `ERROR_CODE`, `FAILURE_STAGE`, and `ROLLBACK_RECOMMENDED`.
Rollback is never automatic. It is `FALSE` before atomic publication and `TRUE`
only if the new configuration was published but durable or post-publication
validation failed; the exact backup path is retained in failure evidence.

#### Action 7 state and partial-failure matrix

- **Never run / key absent or empty:** require exact Action 6 dataset PASS,
  preserve a private `0600` byte-identical backup, activate the one intended
  value atomically at mode `0600`, and validate again.
- **Already active and correct at mode `0600`:** idempotent PASS; no mutation and
  no new backup.
- **Already selected at a safe broader read-only mode:** preserve a backup and
  atomically normalize the activated configuration to `0600`.
- **Duplicate keys, a different nonempty value, unsafe ownership/mode, invalid
  shell syntax, missing dataset, or differing dataset identity:** fail before
  configuration publication with rollback not recommended.
- **Publication succeeds but fsync or post-validation fails:** retain the exact
  backup path, report rollback recommended, and stop. Restoration is a separate
  operator-reviewed atomic configuration action and is never automatic.
- **Rerun after interruption:** atomic replacement means the configuration is
  either the prior complete file or the new complete file. The rerun follows the
  corresponding precondition/no-op path; it never guesses from a partial file.
- **Power loss:** the durable pre-mutation backup and same-directory atomic
  replacement bound the state to the complete prior or intended file. Abrupt
  power-loss testing remains exclusively in the separate future PI3 + PI5
  Abrupt Power-Loss / Cold-Boot Recovery Validation checkpoint.

Before Action 7, Action 6 must be complete and the exact immutable version must
exist while configuration remains unactivated or already exactly selected.
After PASS, `config/hioc.conf` contains exactly one intended
`MANUFACTURER_DB_PATH` at mode `0600`; all other configuration content, the
immutable pair, transport staging, sidecars/status, services, and schedules are
unchanged. The backup, when created, remains private durable rollback material.
No reload is applicable. Reviewed full Action 7 PASS is the sole authorization
prerequisite for preparing the separate Action 8 generation action.

Run Action 7 only and return all output. Do not begin Action 8 without reviewed
full Action 7 PASS.

## Action 8 — Protected pre-state and manufacturer generation

Target: PI3 runtime state. Mutation: evidence directory, manufacturer sidecar,
and manufacturer status only. Rollback relevance: sidecar/config domains.

### Pre-execution governance correction

The historical inline block is rejected before execution as **PE-3 ACTION 8
OPERATOR-SAFETY AND EVIDENCE CONTRACT DEFECT — MANUFACTURER GENERATION
PROCEDURE NOT PRODUCTION-SAFE**. It enabled interactive `set -euo pipefail`,
used a `tee` pipeline under pipefail, retained an unresolved evidence-directory
placeholder, used bare assertions, and lacked complete target, source, runtime,
configuration, dataset, inventory, output-precondition, post-publication,
failure-stage, and rollback evidence. At that historical checkpoint, Action 8
remained **NOT STARTED**. No manufacturer sidecar/status generation, evidence
mutation, staging cleanup, or later action occurred.

Substantial Action 8 logic is now owned by
`tools/hioc-pe3-action8-generate.sh`. The script accepts the exact governance
commit as its only operator input. It proves target and source identity; its
own, generator, validator, and
manufacturer-library Git/worktree identity; deployed runtime identity; Action 7
configuration selection; exact immutable database identity and privacy-safe
validator PASS; inventory validity; output preconditions; transport-staging
preservation; and protected state before creating its own private evidence
directory and beginning generation.

The published PI3 release source at
`46f06bc3b1e7676ec23ac310d7a9a8585c05f632` predates this new script. A future
bootstrap synchronization/script-identity gate is therefore mandatory after the
correction is reviewed, committed, and pushed.

### Action 8 bootstrap — target synchronization and script identity

The bootstrap is a separate, non-production authorization boundary. It owns
only clean fast-forward synchronization of the PI3 release-source checkout to
the exact published governance commit and proof of the Action 8 script's Git and
worktree identity, then stops. It never reads runtime configuration, the
immutable dataset, inventory, manufacturer outputs, Action 8 evidence, or
transport staging and cannot invoke Action 8 or Action 9.

Target: PI3 **NUT&PIHOLE**, interactive Bash. Mutation: Git metadata and tracked
release-source files through fast-forward only. Runtime/production mutation:
none. Rollback: not applicable and not recommended.

```bash
set +x
hioc_pe3_action8_bootstrap_sync() {
  SOURCE=/home/jazofv1/hioc-release-source
  SCRIPT_REL=tools/hioc-pe3-action8-generate.sh
  SCRIPT="$SOURCE/$SCRIPT_REL"
  GOVERNANCE_COMMIT=${1:-}
  SCRIPT_BLOB=b8c38607325acaf6ab3a02878c834e05e54bea56
  fail() { printf 'RESULT=INPUT_OR_PRECONDITION_ERROR\nERROR_CODE=%s\nFAILURE_STAGE=%s\nROLLBACK_RECOMMENDED=FALSE\n' "$1" "$2"; return 1; }
  [ "$#" -eq 1 ] || { fail INVALID_GOVERNANCE_COMMIT INPUT_VALIDATION; return; }
  printf '%s' "$GOVERNANCE_COMMIT" | grep -Eq '^[0-9a-f]{40}$' || { fail INVALID_GOVERNANCE_COMMIT INPUT_VALIDATION; return; }
  [ "$(hostname -s 2>/dev/null)" = nutandpihole ] || { fail WRONG_TARGET TARGET_SYNCHRONIZATION; return; }
  ip -o -4 addr show scope global 2>/dev/null | awk '{print $4}' | cut -d/ -f1 | grep -Fxq 192.168.100.252 || { fail WRONG_TARGET TARGET_SYNCHRONIZATION; return; }
  printf 'TARGET_IDENTITY=PASS\n'
  [ -d "$SOURCE/.git" ] || { fail SOURCE_REPOSITORY_MISSING REPOSITORY_PRECONDITION; return; }
  [ "$(git -C "$SOURCE" branch --show-current 2>/dev/null)" = main ] || { fail WRONG_BRANCH REPOSITORY_PRECONDITION; return; }
  [ -z "$(git -C "$SOURCE" status --porcelain 2>/dev/null)" ] || { fail SOURCE_REPOSITORY_DIRTY REPOSITORY_PRECONDITION; return; }
  for marker in MERGE_HEAD REBASE_HEAD CHERRY_PICK_HEAD REVERT_HEAD BISECT_LOG; do [ ! -e "$SOURCE/.git/$marker" ] || { fail ACTIVE_GIT_OPERATION REPOSITORY_PRECONDITION; return; }; done
  [ ! -d "$SOURCE/.git/rebase-merge" ] && [ ! -d "$SOURCE/.git/rebase-apply" ] || { fail ACTIVE_GIT_OPERATION REPOSITORY_PRECONDITION; return; }
  printf 'REPOSITORY_PRECONDITION=PASS\n'
  git -C "$SOURCE" fetch origin >/dev/null 2>&1 || { fail GIT_FETCH_FAILED REPOSITORY_SYNCHRONIZATION; return; }
  [ "$(git -C "$SOURCE" rev-parse origin/main 2>/dev/null)" = "$GOVERNANCE_COMMIT" ] || { fail GOVERNANCE_COMMIT_MISMATCH REPOSITORY_SYNCHRONIZATION; return; }
  git -C "$SOURCE" merge-base --is-ancestor HEAD "$GOVERNANCE_COMMIT" >/dev/null 2>&1 || { fail NON_FAST_FORWARD_SOURCE REPOSITORY_SYNCHRONIZATION; return; }
  git -C "$SOURCE" merge --ff-only origin/main >/dev/null 2>&1 || { fail FAST_FORWARD_FAILED REPOSITORY_SYNCHRONIZATION; return; }
  printf 'REPOSITORY_SYNCHRONIZATION=PASS\n'
  [ "$(git -C "$SOURCE" rev-parse HEAD 2>/dev/null)" = "$GOVERNANCE_COMMIT" ] || { fail POST_SYNC_HEAD_MISMATCH SYNCHRONIZED_HEAD_IDENTITY; return; }
  [ -z "$(git -C "$SOURCE" status --porcelain 2>/dev/null)" ] || { fail POST_SYNC_REPOSITORY_DIRTY SYNCHRONIZED_HEAD_IDENTITY; return; }
  printf 'SYNCHRONIZED_HEAD_IDENTITY=PASS\n'
  [ ! -L "$SCRIPT" ] || { fail ACTION8_SCRIPT_NOT_REGULAR SCRIPT_AVAILABILITY; return; }
  [ -e "$SCRIPT" ] || { fail ACTION8_SCRIPT_MISSING SCRIPT_AVAILABILITY; return; }
  [ -f "$SCRIPT" ] || { fail ACTION8_SCRIPT_NOT_REGULAR SCRIPT_AVAILABILITY; return; }
  printf 'ACTION8_SCRIPT_AVAILABILITY=PASS\n'
  [ "$(git -C "$SOURCE" rev-parse "$GOVERNANCE_COMMIT:$SCRIPT_REL" 2>/dev/null)" = "$SCRIPT_BLOB" ] || { fail ACTION8_SCRIPT_GIT_IDENTITY_MISMATCH SCRIPT_IDENTITY; return; }
  [ "$(git -C "$SOURCE" hash-object --path="$SCRIPT_REL" "$SCRIPT" 2>/dev/null)" = "$SCRIPT_BLOB" ] && git -C "$SOURCE" diff --quiet -- "$SCRIPT_REL" || { fail ACTION8_SCRIPT_WORKTREE_IDENTITY_MISMATCH SCRIPT_IDENTITY; return; }
  printf 'ACTION8_SCRIPT_IDENTITY=PASS\nACTION8_BOOTSTRAP=COMPLETE\nRESULT=PASS\n'
}
hioc_pe3_action8_bootstrap_sync '<operator-approved-full-40-hex-governance-commit>'
```

The invocation value is supplied only after the final governance correction is
committed, pushed, and explicitly approved. It must be a literal lowercase full
40-hex commit ID; an empty value, abbreviation, symbolic ref, branch, or tag
fails as `INVALID_GOVERNANCE_COMMIT` at `INPUT_VALIDATION` before target checks,
fetch, or merge. The procedure never infers the value from a ref.

Canonical PASS is exactly, in order: `TARGET_IDENTITY`,
`REPOSITORY_PRECONDITION`, `REPOSITORY_SYNCHRONIZATION`,
`SYNCHRONIZED_HEAD_IDENTITY`, `ACTION8_SCRIPT_AVAILABILITY`,
`ACTION8_SCRIPT_IDENTITY`, `ACTION8_BOOTSTRAP=COMPLETE`, and `RESULT=PASS`.
Every failure emits bounded `RESULT`, `ERROR_CODE`, `FAILURE_STAGE`, and
`ROLLBACK_RECOMMENDED=FALSE`, suppresses later stages, and returns control to the
parent prompt. Stop after bootstrap PASS and return all output for review. The
exact prior evidence-directory path is not an input to this bootstrap. At that
pre-execution checkpoint, Action 8 remained **ATTEMPTED BUT NOT COMPLETE**.
Another attempt required separate authorization only after the source refresh
and corrected-validator deployment checkpoints passed and were reviewed. The
later governed execution is recorded above as **PASS / COMPLETE**; Action 9
remains **NOT STARTED**.

The generator remains the established manual
`pi4/bin/hioc-generate-manufacturer.py`; no collector, service, timer, cron job,
systemd unit, reload, or restart is introduced. It consumes the single
`MANUFACTURER_DB_PATH` activated by Action 7 and reads the adjacent immutable
manifest plus current `inventory.json` under its existing exclusive manufacturer
lock. It may atomically create or replace only private mode-`0600`
`manufacturer.json` and `manufacturer_status.json` according to the executable
contract. The wrapper creates one invocation-owned
`/tmp/hioc-pe3-action8-XXXXXXXX` directory only after all read-only identity and
output preconditions pass. The real non-symlink directory and its `pre`
subdirectory are owned by `jazofv1:jazofv1` at mode `0700`; no operator path is
accepted and no prior directory is reused. It may contain only Action 8 private
evidence: `pre/protected.json`, `generation-performance.txt`, and
result-last `generation-result.json` on PASS. A generator failure instead retains
`generation-performance.txt` followed by result-last `generation-failure.json`.
Invocation-owned raw stdout/stderr and diagnostic temporary files exist only
while running and are removed before control returns when cleanup succeeds.

Action 8 must not alter configuration, the immutable database/manifest,
inventory or other protected runtime state, services,
schedules, environment configuration, or deployment state. It cannot clean
staging or chain Action 9. The sidecar generator's frozen two-artifact failure
semantics remain authoritative: prior valid state is preserved where specified;
a generator-domain failure does not by itself recommend rollback. A successful
generation followed by invalid output, protected-state drift, or failed durable
evidence publication stops with rollback review recommended; rollback is never
automatic.

Canonical PASS requires, in order: `TARGET_IDENTITY`, `SOURCE_IDENTITY`,
`RUNTIME_IDENTITY`, `CONFIGURATION_IDENTITY`, `DATASET_IDENTITY`,
`DATASET_VALIDATION`, `INVENTORY_IDENTITY`, `OUTPUT_PRECONDITION`,
`EVIDENCE_PRECONDITION`, `PROTECTED_PRE_STATE`, `MANUFACTURER_GENERATION`,
`MANUFACTURER_ARTIFACT_IDENTITY`, `MANUFACTURER_ARTIFACT_VALIDATION`,
`PROTECTED_POST_GENERATION`, `EVIDENCE_PUBLICATION`, `EVIDENCE_REPORT=PASS`,
the exact `EVIDENCE_DIR`, `ACTION8=COMPLETE`, `RESULT=PASS`, and
`ROLLBACK_RECOMMENDED=FALSE`. Performance evidence is published before the
generation result, which is the result-last marker. Every failure emits
`RESULT`, `ERROR_CODE`, `FAILURE_STAGE`, and `ROLLBACK_RECOMMENDED`; after safe
directory creation it also emits the exact `EVIDENCE_DIR`. Failures return
control to the parent prompt, suppress later stages, and never perform automatic
rollback or later-action chaining.

The production attempt at governance commit
`e59b74a2a5c8b8cad05589198609fd616044a434` reached
`PROTECTED_PRE_STATE=PASS`, then stopped with `MANUFACTURER_GENERATOR_FAILED`.
Read-only forensics proved the private evidence layout contained only
`pre/protected.json`; no result, performance, temporary capture, or status
diagnostic survived. The underlying generator error is unrecoverable. This is
classified as **PE-3 ACTION 8 GENERATOR FAILURE DIAGNOSTIC RETENTION DEFECT —
WRAPPER COLLAPSES GENERATOR FAILURE WITHOUT DURABLE SANITIZED ROOT-CAUSE
EVIDENCE**.

The corrected wrapper privately captures generator stdout and stderr, never
prints either raw stream, and accepts only a bounded JSON `FAIL` envelope with an
allowlisted manufacturer error code. It publishes performance evidence first
and a private mode-`0600` `generation-failure.json` last. The failure document
contains only schema/result/stage, wrapper and allowlisted generator codes,
numeric exit status, structured-result and stderr-presence booleans, safe
sidecar/status presence/change/type summaries, temporary-artifact presence,
output-mutation class, and rollback recommendation. It contains no raw output,
message, inventory, MAC, prefix, manufacturer, database, configuration, secret,
or environment value. Raw captures are removed before final publication.

`MANUFACTURER_GENERATOR_FAILED` recommends rollback only when a sidecar change,
unsafe/missing prior output, or leftover generator temporary artifact proves a
potentially partial or unsafe output transaction. A safe status-only failure
update remains non-rollback. Failure-evidence publication or cleanup uncertainty
fails closed with rollback review recommended. Rollback is never automatic.
At that historical generator-failure checkpoint, Action 8 remained **NOT
COMPLETE** and the changed wrapper required a new post-push bootstrap before any
future separately authorized attempt. Action 9 remained **NOT STARTED**.

The next governed attempt reached the generation boundary but the hard-coded
optional `/usr/bin/time` launcher was absent on PI3. Sanitized failure evidence
was retained with exit `127`, no output mutation, and rollback not recommended;
the governed Python generator was not proven to have started. This is **PE-3
ACTION 8 PERFORMANCE-INSTRUMENTATION PORTABILITY DEFECT — OPTIONAL
/usr/bin/time DEPENDENCY BLOCKS GOVERNED MANUFACTURER GENERATION**. Action 8 now
uses an embedded governed-Python launcher with `perf_counter`, child
`getrusage`, and an invocation-private launch marker. Performance remains
mandatory private evidence, but no external timing package is required.
`generator_launch_status=CONFIRMED` means `Popen` returned successfully;
otherwise it is `UNCONFIRMED` and the wrapper reports
`GENERATOR_INVOCATION_FAILED` at `MANUFACTURER_INVOCATION`. The corrected
wrapper required another post-push bootstrap and Action 8 remained incomplete
at that historical portability-defect checkpoint.

The original Action 8 staging barrier is retired as **PE-3 ACTION 8
TRANSPORT-STAGING LIFETIME CONTRACT DEFECT — EPHEMERAL TRANSFER STATE
INCORRECTLY REQUIRED AFTER IMMUTABLE INSTALLATION**. Action 6 already consumed,
validated, and atomically published the transferred pair; Action 7 selected the
installed immutable database. Action 8 consumes no staging bytes and derives no
security, provenance, privacy, or rollback evidence from the transfer copy. It
accepts staging absence and does not read, fingerprint, recreate, retransmit, or
clean staging. Exact installed dataset and active configuration identity remain
mandatory before generation and are rechecked afterward.

The earlier dependency on an operator-supplied
`/tmp/hioc-pe3-production-validation-*` path is rejected as **PE-3 ACTION 8
EVIDENCE-DIRECTORY PROVENANCE AND DURABILITY CONTRACT DEFECT — EPHEMERAL PATH IS
NOT DURABLY IDENTIFIABLE**. Action 8 consumes no Action 5 or Action 5C evidence.
Its fresh directory is temporary operator evidence whose exact returned path
must remain intact through reviewed Action 8 evidence and separately authorized
Action 9. If it is lost, Action 9 remains blocked; no reconstruction or arbitrary
directory substitution is allowed. Persistent archival, if required by the
final Evidence Report contract, remains a later governed boundary.

After the evidence-directory correction changes the Action 8 script blob, the
previous bootstrap PASS at governance commit
`932a05efe7bf44cee91d1b85e0f90e68552c288a` remains historical evidence only.
A new synchronization/script-identity bootstrap must be reviewed and pass after
this correction is committed and pushed. It is not prepared here.

After that future replacement bootstrap PASS and separate Action 8 authorization,
the wrapper interface is only:

```text
bash /home/jazofv1/hioc-release-source/tools/hioc-pe3-action8-generate.sh \
  --governance-commit '<approved-full-40-hex-post-push-commit>'
```

No evidence-directory argument is accepted. This interface is documented but
not authorized for execution by this correction checkpoint.

Reviewed full Action 8 PASS and the private aggregate evidence are required
before Action 9 may be prepared. Match percentage is not an acceptance
criterion. Do not manually edit sidecars or status.

## Action 9 — Production validation and Evidence Report

The historical inline procedure below is obsolete and must not be executed. It
is rejected as **PE-3 ACTION 9 OPERATOR-SAFETY AND EVIDENCE-CONTRACT DEFECT —
STALE EVIDENCE INPUT, INTERACTIVE STRICT MODE, UNDECLARED TIMING DEPENDENCY, AND
UNBOUNDED FAILURE SEMANTICS**.

Current Action 9 is owned only by
`tools/hioc-pe3-action9-validate.sh`. It is a read-only production validation
transaction whose only mutation is a private invocation-owned
`/tmp/hioc-pe3-action9-XXXXXXXX` evidence directory. It accepts exactly
`--governance-commit <full-lowercase-40-hex>` and
`--action8-evidence-dir </tmp/hioc-pe3-action8-*>`. The operator supplies the
exact preserved directory returned by the reviewed Action 8 PASS; the tool does
not infer or hard-code a suffix and rejects arbitrary names or contents.

The tool proves PI3, operator, clean exact-commit source, its own Git/worktree
identity, the Action 8 wrapper, validator, manufacturer library, and deployed
validator/library equality. It requires Action 8 evidence to contain exactly
private `generation-result.json`, `generation-performance.txt`, and
`pre/protected.json`, rejects failure or unexpected evidence, validates the
bounded PASS/count/performance schemas, and never invokes the generator.
Performance acceptance reuses governed Action 8 timing and RSS evidence; there
is no `/usr/bin/time` dependency.

It independently validates configuration selection, immutable dataset hashes,
inventory permission class, exact-private manufacturer artifacts, absence of
temporary outputs, privacy-safe database and sidecar results, and byte-identical
protected state before/after. It publishes bounded `evidence-report.json`, then
result-last `action9-result.txt`, both mode `0600` under a mode-`0700` directory.
No inventory, configuration, dataset, manufacturer output, service, schedule,
Action 8 evidence, transport staging, or production code is modified.

Canonical PASS is exactly, in order: `TARGET_IDENTITY`, `SOURCE_IDENTITY`,
`RUNTIME_IDENTITY`, `ACTION8_EVIDENCE_IDENTITY`,
`ACTION8_EVIDENCE_VALIDATION`, `PERFORMANCE_EVIDENCE_VALIDATION`,
`EVIDENCE_PREPARATION`, `CONFIGURATION_IDENTITY`, `DATASET_IDENTITY`,
`INVENTORY_IDENTITY`, `MANUFACTURER_ARTIFACT_IDENTITY`,
`MANUFACTURER_ARTIFACT_VALIDATION`, `PROTECTED_STATE`, `EVIDENCE_REPORT`,
`EVIDENCE_DIR`, `ACTION9=COMPLETE`, `RESULT=PASS`, and
`ROLLBACK_RECOMMENDED=FALSE`. Every failure emits bounded `RESULT`, `ERROR_CODE`,
`FAILURE_STAGE`, and `ROLLBACK_RECOMMENDED=FALSE`, plus `EVIDENCE_DIR` only when
created. It returns to the parent prompt and stops. Action 10 remains **NOT
STARTED / NOT PREPARED**.

Interface, documented but not authorized for execution by this repository
checkpoint:

```text
bash /home/jazofv1/hioc-release-source/tools/hioc-pe3-action9-validate.sh \
  --governance-commit '<approved-full-40-hex-post-push-commit>' \
  --action8-evidence-dir '<exact-reviewed-action8-evidence-directory>'
```

### Obsolete Action 9 inline procedure — do not execute

The following block is retained solely as historical defect evidence. Its path,
strict mode, timing utility, repeated generator calls, and output behavior are
not part of the active Action 9 contract.

```bash
set -euo pipefail
set +x
RUNTIME=/home/jazofv1/hioc
SOURCE=/home/jazofv1/hioc-release-source
EVIDENCE_DIR='/tmp/hioc-pe3-production-validation-XXXXXXXX'
IMPLEMENTATION_COMMIT=157ae644dcedcbec7c69cb0d8b054e104335e024
OPERATOR_GOVERNANCE_COMMIT='<approved-full-40-hex-post-push-commit>'
FINAL_DIR="$RUNTIME/data/manufacturer/versions/local-ieee-ra--2026-08-11-r1"
DB="$FINAL_DIR/manufacturer-db.json"; MF="$FINAL_DIR/manufacturer-db.manifest.json"
SIDE="$RUNTIME/state/inventory/manufacturer.json"; STATUS="$RUNTIME/state/inventory/manufacturer_status.json"; INVENTORY="$RUNTIME/state/inventory/inventory.json"
python3 "$RUNTIME/pi4/bin/hioc-validate-manufacturer.py" sidecar --sidecar "$SIDE" --status "$STATUS" --inventory "$INVENTORY" --database "$DB" --manifest "$MF" --json | tee "$EVIDENCE_DIR/sidecar-validation.json"
jq -e '.result=="PASS" and .privacy_safe==true' "$EVIDENCE_DIR/sidecar-validation.json" >/dev/null
for p in "$SIDE" "$STATUS" "$DB" "$MF"; do [ -f "$p" ] && [ ! -L "$p" ] && [ "$(stat -c %a "$p")" = 600 ] && [ "$(stat -c %U:%G "$p")" = jazofv1:jazofv1 ]; done
! find "$RUNTIME/state/inventory" -maxdepth 1 -type f \( -name '.manufacturer*.tmp' -o -name '.manufacturer_status*.tmp' \) | grep -q .
python3 - "$RUNTIME" "$EVIDENCE_DIR/post/protected.json" "$EVIDENCE_DIR/pre/protected.json" <<'PY'
import hashlib,json,pathlib,sys
root=pathlib.Path(sys.argv[1]); target=pathlib.Path(sys.argv[2]); before=json.loads(pathlib.Path(sys.argv[3]).read_text(encoding='utf-8'))
def clean(v):
 if isinstance(v,dict): return {k:clean(x) for k,x in sorted(v.items()) if k not in {'updated','updated_at','generated_at','timestamp','last_seen','last_changed'}}
 if isinstance(v,list): return [clean(x) for x in v]
 return v
def now(entry):
 p=root/entry['path']
 if not p.is_file() or p.is_symlink(): return {'path':entry['path'],'class':entry['class'],'present':False}
 v=json.loads(p.read_text(encoding='utf-8')); raw=json.dumps(clean(v),sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
 return {'path':entry['path'],'class':entry['class'],'present':True,'semantic_sha256':hashlib.sha256(raw).hexdigest(),'top_level_count':len(v) if isinstance(v,(dict,list)) else None}
after={'stable':[now(x) for x in before['stable']],'operational_drift':[now(x) for x in before['operational_drift']]}
stable_pass=after['stable']==before['stable']; incident_changed=after['operational_drift']!=before['operational_drift']
after['stable_invariants_pass']=stable_pass; after['incident_operational_drift']='OBSERVED_REQUIRES_CAUSAL_REVIEW' if incident_changed else 'NONE_OBSERVED'
target.write_text(json.dumps(after,indent=2,sort_keys=True)+'\n',encoding='utf-8')
if not stable_pass: raise SystemExit(30)
PY
GENERATION_TIMES="$EVIDENCE_DIR/generation-warm-seconds.txt"; VALIDATION_TIMES="$EVIDENCE_DIR/sidecar-validation-seconds.txt"
: > "$GENERATION_TIMES"; : > "$VALIDATION_TIMES"
for run in 1 2 3 4 5; do
  /usr/bin/time -f %e -o "$EVIDENCE_DIR/time.tmp" python3 "$RUNTIME/pi4/bin/hioc-generate-manufacturer.py" --home "$RUNTIME" --json > "$EVIDENCE_DIR/generation-warm-$run.json"
  jq -e '.result=="PASS"' "$EVIDENCE_DIR/generation-warm-$run.json" >/dev/null
  cat "$EVIDENCE_DIR/time.tmp" >> "$GENERATION_TIMES"
  /usr/bin/time -f %e -o "$EVIDENCE_DIR/time.tmp" python3 "$RUNTIME/pi4/bin/hioc-validate-manufacturer.py" sidecar --sidecar "$SIDE" --status "$STATUS" --inventory "$INVENTORY" --database "$DB" --manifest "$MF" --json > "$EVIDENCE_DIR/sidecar-validation-$run.json"
  jq -e '.result=="PASS" and .privacy_safe==true' "$EVIDENCE_DIR/sidecar-validation-$run.json" >/dev/null
  cat "$EVIDENCE_DIR/time.tmp" >> "$VALIDATION_TIMES"
done
rm -- "$EVIDENCE_DIR/time.tmp"
python3 - "$DB" "$MF" "$GENERATION_TIMES" "$VALIDATION_TIMES" "$EVIDENCE_DIR/generation-performance.txt" "$EVIDENCE_DIR/performance.json" <<'PY'
import json,pathlib,resource,statistics,sys,time
sys.path.insert(0,'/home/jazofv1/hioc/pi4/lib'); from hioc.manufacturer import load_database,lookup_manufacturer_eui48,validate_database,validate_manifest
dbp=pathlib.Path(sys.argv[1]); mfp=pathlib.Path(sys.argv[2]); raw=json.loads(dbp.read_text()); mf=json.loads(mfp.read_text()); loads=[]; validations=[]; rss_before=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
for _ in range(20): t=time.perf_counter(); db=load_database(dbp,mfp); loads.append((time.perf_counter()-t)*1000)
for _ in range(20): t=time.perf_counter(); validate_database(raw); validate_manifest(mf); validations.append((time.perf_counter()-t)*1000)
rss_after=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss; incremental_rss=max(0,(rss_after-rss_before)*1024); lookups=[]
for _ in range(200): t=time.perf_counter(); lookup_manufacturer_eui48(db,'A2:00:00:00:00:02'); lookups.append((time.perf_counter()-t)*1000)
def p95(x): return sorted(x)[max(0,int(len(x)*.95)-1)]
generation=[float(x) for x in pathlib.Path(sys.argv[3]).read_text().split()]; sidecar_validation=[float(x) for x in pathlib.Path(sys.argv[4]).read_text().split()]
cold=float(dict(x.split('=',1) for x in pathlib.Path(sys.argv[5]).read_text().split())['manufacturer_generation_elapsed_seconds'])
out={'load_validation_index_p95_ms':p95(loads),'complete_validation_p95_ms':p95(validations),'lookup_p95_ms':p95(lookups),'lookup_median_ms':statistics.median(lookups),'manufacturer_generation_cold_seconds':cold,'manufacturer_generation_warm_p95_seconds':p95(generation),'sidecar_validation_p95_seconds':p95(sidecar_validation),'total_pe3_cold_seconds':cold+p95(sidecar_validation),'incremental_rss_bytes':incremental_rss,'thresholds':{'load_p95_ms':750,'lookup_p95_ms':5,'lookup_median_ms':1,'generation_warm_p95_seconds':2,'generation_cold_seconds':4,'incremental_rss_bytes':50331648}}
out['threshold_pass']=out['load_validation_index_p95_ms']<=750 and out['lookup_p95_ms']<=5 and out['lookup_median_ms']<=1 and out['manufacturer_generation_warm_p95_seconds']<=2 and cold<=4 and incremental_rss<=50331648
pathlib.Path(sys.argv[6]).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
PY
jq -e '.threshold_pass==true' "$EVIDENCE_DIR/performance.json" >/dev/null
jq -n --arg result PASS --arg host nutandpihole --arg ip 192.168.100.252 --arg source_commit "$OPERATOR_GOVERNANCE_COMMIT" --arg implementation_commit "$IMPLEMENTATION_COMMIT" --arg dataset_id local-ieee-ra --arg dataset_version 2026-08-11-r1 --arg db_sha 81f147cc57768c5797c4ad73a8c0369001bbdcbfe1548e71d3702c8c7f81e0e1 --arg semantic_sha 2dbda82441416feea8d2f60c4ebe043c033c1de80ed50460e55a5367dcc1083c --arg manifest_sha 10c8097c0a4ec6e8cc4cd3dc61afc7f368057f4ef4b6534df9f6dd31634a4ac4 --rawfile release_backup "$EVIDENCE_DIR/release-backup-path.txt" --rawfile installer_backup "$EVIDENCE_DIR/installer-backup-path.txt" --rawfile config_backup "$EVIDENCE_DIR/config-backup-path.txt" --slurpfile artifacts "$EVIDENCE_DIR/git-artifacts.json" --slurpfile generation "$EVIDENCE_DIR/generation-result.json" --slurpfile invariants "$EVIDENCE_DIR/post/protected.json" --slurpfile performance "$EVIDENCE_DIR/performance.json" '{result:$result,target:{hostname:$host,ipv4:$ip},source_repository_commit:$source_commit,implementation_commit:$implementation_commit,runtime_artifact_identity:$artifacts[0],release_backup_path:($release_backup|rtrimstr("\n")),installer_backup_path:(if ($installer_backup|rtrimstr("\n"))=="NONE" then null else ($installer_backup|rtrimstr("\n")) end),configuration_backup_path:(if ($config_backup|rtrimstr("\n"))=="NONE" then null else ($config_backup|rtrimstr("\n")) end),dataset:{id:$dataset_id,version:$dataset_version,database_sha256:$db_sha,semantic_sha256:$semantic_sha,manifest_sha256:$manifest_sha,record_count:53581,ma_l_count:39916,ma_m_count:6538,ma_s_count:7127,conflict_count:2},sidecar_aggregate:$generation[0],validation_result:"PASS",protected_invariants:$invariants[0],privacy:"PASS",performance:$performance[0],incident_operational_drift:$invariants[0].incident_operational_drift,cleanup:"PENDING_ACTION_10",rollback_recommended:false,rollback_command:null,pe4_status:"NOT_STARTED"}' > "$EVIDENCE_DIR/PE3_MANUFACTURER_PRODUCTION_EVIDENCE.json"
! grep -Eiq '([0-9A-F]{2}:){5}[0-9A-F]{2}|dev_[0-9a-f]{16}|matched_prefix|manufacturer[^_a-z]*:' "$EVIDENCE_DIR/PE3_MANUFACTURER_PRODUCTION_EVIDENCE.json"
(cd "$EVIDENCE_DIR" && find . -type f ! -name EVIDENCE_CHECKSUMS.sha256 -print0 | sort -z | xargs -0 sha256sum > EVIDENCE_CHECKSUMS.sha256)
printf 'PRODUCTION_VALIDATION=PASS\nEVIDENCE_REPORT=%s\n' "$EVIDENCE_DIR/PE3_MANUFACTURER_PRODUCTION_EVIDENCE.json"
```

MQTT and other live telemetry use existing platform validation evidence; no PE-3
publisher is introduced. Incident changes are operational drift requiring causal
review, not automatic invariant failure. A single performance miss is
`VALIDATION_FAIL` pending a repeated governed measurement; rollback requires two
stable-input runs above 150% of a hard bound with demonstrated PE-3 causality.
Run Action 9 only; return the sanitized report and checksums.

## Action 10 — Historical temporary transfer cleanup boundary

Transport staging is transient Action 6 input and ceases to be authoritative
after reviewed immutable publication. If it still exists, cleanup requires a
separate future authorization and a current governed procedure. If it is already
absent, as confirmed at the Action 8 pre-generation stop, no cleanup action is
required or permitted. Action 8 and Action 9 do not depend on this boundary.

The earlier inline deletion block is not an active operator instruction. Do not
recreate staging to satisfy cleanup and do not remove the installed immutable
version, Windows sources/build, release backup, configuration backup, or Action 8
evidence.

## Result taxonomy and rollback domains

- `PASS`: repository, deployment, dataset, configuration, validation, generation,
  invariants, privacy, performance, evidence, and cleanup all pass.
- `PARTIAL_PASS`: only an explicitly optional measurement/evidence source is
  unavailable; every required functional and invariant check passes.
- `INPUT_OR_PRECONDITION_ERROR`: wrong host/IP/commit/branch, dirty checkout,
  missing or unexpected artifacts, existing different dataset/configuration, or
  another unmet input condition.
- `VALIDATION_FAIL`: evidence or validator uncertainty without demonstrated
  protected regression. No automatic rollback.
- `FAIL`: deterministic artifact corruption, protected-contract regression,
  privacy leak, code-caused state failure, local-data loss, or repeated causal
  performance failure.

Code rollback, only when justified, is:

```bash
HIOC_INSTALL_DIR=/home/jazofv1/hioc bash /home/jazofv1/hioc-release-source/release/rollback.sh "$RELEASE_BACKUP"
```

Configuration rollback restores the exact `CONFIG_BACKUP` with owner
`jazofv1:jazofv1` and mode `0600`, then revalidates. Dataset failure restores the
previous configured path if one existed and preserves both prior and new
immutable versions pending classification. Sidecars are never edited manually;
the generator's last-valid semantics govern. Conflicts, unknowns, randomized
addresses, low match percentage, unattractive labels, and one optional missing
measurement are never rollback reasons by themselves.

## Operator action ledger

| Action | Target | Expected terminal result | Mutation | Stop condition | Rollback relevance |
| --- | --- | --- | --- | --- | --- |
| 1 | Windows | local validator and artifact PASS | No | Any identity/hash/validation error | None |
| 2 | PI3 + Windows | transfer PASS and exact stage path | Temporary files | Any transfer/path error | None |
| 3 | PI3 | staging verification PASS | No | Host/file/hash/symlink error | None |
| 4 | PI3 source + staging | synchronization, implementation, staged identity, and validator PASS | Git fast-forward only | Dirty/diverged/wrong commit/identity/validator error | Source only |
| 5 | PI3 runtime | code deployment PASS and backup path | Runtime code/backup | Release/artifact/PI4 failure | Code |
| 6 | PI3 runtime | new or identical immutable dataset PASS | New version only | Existing difference/install failure | Dataset |
| 7 | PI3 runtime | config active/no-op PASS and backup if changed | Config/backup | Different value/config failure | Config |
| 8 | PI3 runtime | aggregate generation PASS | Sidecar/status/evidence | Generator failure | Sidecar/config |
| 9 | PI3 runtime | validation/evidence PASS | Evidence; no-op timing writes | Invariant/privacy/required threshold failure | Classified |
| 10 | PI3 `/tmp` | transfer cleanup PASS | Exact temporary deletion | Unexpected staging contents | None |

At every boundary: run only the named action, return its output, and wait for
explicit authorization. Never continue automatically.
