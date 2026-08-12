# PE-3.3 Manufacturer Production Deployment and Validation Runbook

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
ACTION1_SCRIPT_SHA256=cd4aa7afe845fbf8a76e6736d956dc1d4818ef87084eeacc0220b980cf5e567c
ACTION1_SCRIPT_GIT_BLOB=02a89b37eb5458b15a6b037941e023c0911df0b3
```

The governance commit supplied by the operator must contain that exact blob.
The script first verifies branch, HEAD/origin identity, repository cleanliness,
its own repository path and Git blob, a clean script diff, and implementation
ancestry. Script-identity failure returns
`RESULT=INPUT_OR_PRECONDITION_ERROR` and
`ERROR_CODE=ACTION1_SCRIPT_IDENTITY_MISMATCH` without closing PowerShell.

Action 1 also reads the approved commit's explicit
`governance/python-runtime-support.json`. The current Windows CPython 3.13 line
is `validation_pending`, so Action 1 returns
`ERROR_CODE=PYTHON_RUNTIME_SUPPORT_PENDING` before interpreter discovery. It may
proceed only after a separate support-promotion commit records the exact passing
3.13 patch and changes the state to `supported`. See
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

Expected output after support promotion: validator PASS plus the final sanitized
PASS object. The selected interpreter is reported only as `py -3.13`,
`python3`, or `python`, with major/minor `3.13`;
the selected build is relative to the supplied workspace, and no Windows user
path or registry content is printed. Multiple exact matching pairs are accepted
only after both hashes and sizes match; lexical absolute-path ordering then makes
the choice deterministic. Expected failures emit sanitized `RESULT` and
`ERROR_CODE` lines and return control to the interactive prompt. Unexpected
failures additionally report only the approved bounded `FAILURE_STAGE`, never
exception text, command text, stack traces, absolute paths, or registry content.

`py -3.13` has priority. `python3` and `python` are accepted only when execution
proves CPython 3.13. A usable other runtime returns
`PYTHON_VERSION_UNSUPPORTED`; no usable runtime returns `PYTHON3_NOT_FOUND`.
WindowsApps aliases that fail execution are not runtimes. Automatic Python
Install Manager installation is disabled during probes. Action 1 never installs
Python.

The prerequisite checkpoint uses `pymanager` for management and `py -3.13`
only for execution after explicit 3.13 installation. The operator workstation's
unintended CPython 3.14.7 does not satisfy Action 1 and does not change its
resolver or support-state gate. Action 1 remains blocked until the separate
3.13 validation passes and a later commit promotes support.

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

Stop on any non-PASS result. Run Action 1 only; return output; do not proceed.


## Action 2 — Manual transfer to unique PI3 staging

Targets: PI3 console to create staging, then Windows to transfer. Mutation:
temporary staging only. Rollback relevance: none; failed staging is removable
after classification.

On PI3, after the operator independently confirms the target terminal:

```bash
set -euo pipefail
umask 077
PI3_STAGE="$(mktemp -d /tmp/hioc-pe3-dataset-transfer-XXXXXXXX)"
chmod 0700 "$PI3_STAGE"
chown jazofv1:jazofv1 "$PI3_STAGE"
printf 'PI3_STAGE=%s\n' "$PI3_STAGE"
```

On Windows, use the exact returned path and the two explicit Action 1 variables:

```powershell
$Pi3Stage = '/tmp/hioc-pe3-dataset-transfer-XXXXXXXX' # replace with exact returned value
scp -- $Database $Manifest "jazofv1@192.168.100.252:${Pi3Stage}/"
if ($LASTEXITCODE -ne 0) { throw 'transfer failed' }
Write-Output 'TRANSFER_RESULT=PASS'
```

No wildcard, recursive copy, source CSV, evidence directory, or repository path
is allowed. Stop if the stage path is not the exact returned path. Run Action 2
only; return output; do not proceed.

## Action 3 — PI3 staging verification

Target: PI3. Mutation: none. Rollback relevance: none.

```bash
set -euo pipefail
set +x
EXPECTED_HOST=nutandpihole
EXPECTED_IP=192.168.100.252
IMPLEMENTATION_COMMIT=157ae644dcedcbec7c69cb0d8b054e104335e024
SOURCE=/home/jazofv1/hioc-release-source
PI3_STAGE='/tmp/hioc-pe3-dataset-transfer-XXXXXXXX' # exact Action 2 value
DB="$PI3_STAGE/manufacturer-db.json"
MF="$PI3_STAGE/manufacturer-db.manifest.json"
[ "$(hostname -s)" = "$EXPECTED_HOST" ]
ip -o -4 addr show scope global | awk '{print $4}' | cut -d/ -f1 | grep -Fxq "$EXPECTED_IP"
read -r -p 'Type nutandpihole to confirm the production target: ' CONFIRM_TARGET
[ "$CONFIRM_TARGET" = nutandpihole ]
printf 'CONFIRM_TARGET=nutandpihole@192.168.100.252\n'
[ -d "$PI3_STAGE" ] && [ ! -L "$PI3_STAGE" ] && [ "$(stat -c %U:%G "$PI3_STAGE")" = jazofv1:jazofv1 ] && [ "$(stat -c %a "$PI3_STAGE")" = 700 ]
[ "$(find "$PI3_STAGE" -mindepth 1 -maxdepth 1 -printf '%f\n' | sort | paste -sd, -)" = 'manufacturer-db.json,manufacturer-db.manifest.json' ]
for p in "$DB" "$MF"; do [ -f "$p" ] && [ ! -L "$p" ]; done
[ "$(stat -c %s "$DB")" = 8652642 ] && [ "$(stat -c %s "$MF")" = 1338 ]
[ "$(sha256sum "$DB" | awk '{print $1}')" = 81f147cc57768c5797c4ad73a8c0369001bbdcbfe1548e71d3702c8c7f81e0e1 ]
[ "$(sha256sum "$MF" | awk '{print $1}')" = 10c8097c0a4ec6e8cc4cd3dc61afc7f368057f4ef4b6534df9f6dd31634a4ac4 ]
git -C "$SOURCE" cat-file -e "$IMPLEMENTATION_COMMIT^{commit}"
git -C "$SOURCE" merge-base --is-ancestor "$IMPLEMENTATION_COMMIT" HEAD
[ "$(git -C "$SOURCE" branch --show-current)" = main ]
[ -z "$(git -C "$SOURCE" status --porcelain)" ]
git -C "$SOURCE" diff --quiet "$IMPLEMENTATION_COMMIT" -- pi4/lib/hioc/manufacturer.py pi4/bin/hioc-validate-manufacturer.py
HIOC_HOME="$SOURCE" python3 "$SOURCE/pi4/bin/hioc-validate-manufacturer.py" database --database "$DB" --manifest "$MF" --json
printf 'STAGING_VERIFICATION=PASS\n'
```

The validator is permitted only after the local source proves approved
implementation ancestry. Stop on wrong target, unexpected file, checksum, size,
symlink, source identity, or validator failure. Run Action 3 only; return output.

## Action 4 — PI3 release-source synchronization

Target: PI3 release-source repository. Mutation: Git fast-forward only. Rollback
relevance: source synchronization is not runtime rollback.

```bash
set -euo pipefail
SOURCE=/home/jazofv1/hioc-release-source
IMPLEMENTATION_COMMIT=157ae644dcedcbec7c69cb0d8b054e104335e024
OPERATOR_GOVERNANCE_COMMIT='<approved-full-40-hex-post-push-commit>'
[ "$(hostname -s)" = nutandpihole ]
ip -o -4 addr show scope global | awk '{print $4}' | cut -d/ -f1 | grep -Fxq 192.168.100.252
[ "$(git -C "$SOURCE" branch --show-current)" = main ]
[ -z "$(git -C "$SOURCE" status --porcelain)" ]
for marker in MERGE_HEAD REBASE_HEAD CHERRY_PICK_HEAD REVERT_HEAD BISECT_LOG; do [ ! -e "$SOURCE/.git/$marker" ]; done
[ ! -d "$SOURCE/.git/rebase-merge" ] && [ ! -d "$SOURCE/.git/rebase-apply" ]
git -C "$SOURCE" fetch origin
[ "$(git -C "$SOURCE" rev-parse origin/main)" = "$OPERATOR_GOVERNANCE_COMMIT" ]
git -C "$SOURCE" merge-base --is-ancestor "$IMPLEMENTATION_COMMIT" "$OPERATOR_GOVERNANCE_COMMIT"
git -C "$SOURCE" merge --ff-only origin/main
[ "$(git -C "$SOURCE" rev-parse HEAD)" = "$OPERATOR_GOVERNANCE_COMMIT" ]
[ -z "$(git -C "$SOURCE" status --porcelain)" ]
printf 'REPOSITORY_SYNCHRONIZATION=PASS\n'
```

Stop on any divergence, dirty state, active operation, ancestry failure, or
non-fast-forward. Run Action 4 only; return output.

## Action 5 — Supported code deployment and artifact identity

Target: PI3 runtime through the supported release workflow. Mutation: runtime
code and timestamped release backup. Rollback relevance: code domain.

```bash
set -euo pipefail
SOURCE=/home/jazofv1/hioc-release-source
RUNTIME=/home/jazofv1/hioc
IMPLEMENTATION_COMMIT=157ae644dcedcbec7c69cb0d8b054e104335e024
OPERATOR_GOVERNANCE_COMMIT='<approved-full-40-hex-post-push-commit>'
EVIDENCE_DIR="$(mktemp -d /tmp/hioc-pe3-production-validation-XXXXXXXX)"
chmod 0700 "$EVIDENCE_DIR"
ARTIFACTS=(pi4/lib/hioc/manufacturer.py pi4/bin/hioc-build-manufacturer-db.py pi4/bin/hioc-validate-manufacturer.py pi4/bin/hioc-generate-manufacturer.py pi4/install_pi4.sh pi4/validate_pi4.sh pi4/config/hioc.conf.example release/upgrade.sh release/rollback.sh)
python3 "$SOURCE/tools/git_artifact_manifest.py" "$OPERATOR_GOVERNANCE_COMMIT" "${ARTIFACTS[@]}" --repo "$SOURCE" --compare-worktree > "$EVIDENCE_DIR/git-artifacts.json"
jq -e --arg c "$OPERATOR_GOVERNANCE_COMMIT" '.commit==$c and .generated_from_git_objects and all(.artifacts[];.working_tree_equal==true)' "$EVIDENCE_DIR/git-artifacts.json" >/dev/null
git -C "$SOURCE" merge-base --is-ancestor "$IMPLEMENTATION_COMMIT" "$OPERATOR_GOVERNANCE_COMMIT"
bash "$SOURCE/release/validate.sh"
HIOC_INSTALL_DIR="$RUNTIME" bash "$SOURCE/release/upgrade.sh" | tee "$EVIDENCE_DIR/release-upgrade.sanitized.txt"
RELEASE_BACKUP="$(cat "$RUNTIME/backups/last-upgrade-backup")"
[ -d "$RELEASE_BACKUP/current" ]
printf '%s\n' "$RELEASE_BACKUP" > "$EVIDENCE_DIR/release-backup-path.txt"
printf 'NONE\n' > "$EVIDENCE_DIR/installer-backup-path.txt"
bash "$RUNTIME/pi4/validate_pi4.sh"
for rel in pi4/lib/hioc/manufacturer.py pi4/bin/hioc-build-manufacturer-db.py pi4/bin/hioc-validate-manufacturer.py pi4/bin/hioc-generate-manufacturer.py pi4/install_pi4.sh pi4/validate_pi4.sh pi4/config/hioc.conf.example release/upgrade.sh release/rollback.sh; do
  expected="$(jq -r --arg p "$rel" '.artifacts[]|select(.path==$p)|.sha256' "$EVIDENCE_DIR/git-artifacts.json")"
  [ -n "$expected" ] && [ "$(sha256sum "$RUNTIME/$rel" | awk '{print $1}')" = "$expected" ]
done
printf 'EVIDENCE_DIR=%s\nRELEASE_BACKUP=%s\nCODE_DEPLOYMENT=PASS\n' "$EVIDENCE_DIR" "$RELEASE_BACKUP"
```

The upgrade must report its timestamped backup; installer backup paths, if any,
are recorded from actual output rather than invented. Dataset state is excluded
from release replacement. Stop on artifact, release, backup, or PI4 validation
failure. Run Action 5 only; return sanitized output.

## Action 6 — Immutable dataset installation

Target: PI3 runtime data root. Mutation: one immutable version-directory
creation. Rollback relevance: dataset domain; no existing dataset is deleted.

Order is frozen as sync, supported code deployment, runtime validation, staged
dataset validation, immutable installation, configuration, final validation,
generation, and sidecar validation. This guarantees an unvalidated dataset is
never active and rollback-capable code exists before activation.

```bash
set -euo pipefail
umask 077
RUNTIME=/home/jazofv1/hioc
PI3_STAGE='/tmp/hioc-pe3-dataset-transfer-XXXXXXXX'
DATA_ROOT="$RUNTIME/data/manufacturer"
VERSIONS="$DATA_ROOT/versions"
FINAL_DIR="$VERSIONS/local-ieee-ra--2026-08-11-r1"
FINAL_DB="$FINAL_DIR/manufacturer-db.json"
FINAL_MF="$FINAL_DIR/manufacturer-db.manifest.json"
install -d -o jazofv1 -g jazofv1 -m 0700 "$DATA_ROOT" "$VERSIONS"
if [ -e "$FINAL_DIR" ]; then
  [ -d "$FINAL_DIR" ] && [ ! -L "$FINAL_DIR" ]
  [ "$(sha256sum "$FINAL_DB" | awk '{print $1}')" = 81f147cc57768c5797c4ad73a8c0369001bbdcbfe1548e71d3702c8c7f81e0e1 ]
  [ "$(sha256sum "$FINAL_MF" | awk '{print $1}')" = 10c8097c0a4ec6e8cc4cd3dc61afc7f368057f4ef4b6534df9f6dd31634a4ac4 ]
  HIOC_HOME="$RUNTIME" python3 "$RUNTIME/pi4/bin/hioc-validate-manufacturer.py" database --database "$FINAL_DB" --manifest "$FINAL_MF" --json
  printf 'DATASET_INSTALL=PASS_ALREADY_IDENTICAL\n'
  exit 0
fi
INSTALL_STAGE="$(mktemp -d "$DATA_ROOT/.staging-XXXXXXXX")"
trap 'test -z "${INSTALL_STAGE:-}" || test ! -d "$INSTALL_STAGE" || rm -r -- "$INSTALL_STAGE"' EXIT
chmod 0700 "$INSTALL_STAGE" && chown jazofv1:jazofv1 "$INSTALL_STAGE"
install -o jazofv1 -g jazofv1 -m 0600 "$PI3_STAGE/manufacturer-db.json" "$INSTALL_STAGE/manufacturer-db.json"
install -o jazofv1 -g jazofv1 -m 0600 "$PI3_STAGE/manufacturer-db.manifest.json" "$INSTALL_STAGE/manufacturer-db.manifest.json"
[ "$(find "$INSTALL_STAGE" -mindepth 1 -maxdepth 1 -printf '%f\n' | sort | paste -sd, -)" = 'manufacturer-db.json,manufacturer-db.manifest.json' ]
[ "$(sha256sum "$INSTALL_STAGE/manufacturer-db.json" | awk '{print $1}')" = 81f147cc57768c5797c4ad73a8c0369001bbdcbfe1548e71d3702c8c7f81e0e1 ]
[ "$(sha256sum "$INSTALL_STAGE/manufacturer-db.manifest.json" | awk '{print $1}')" = 10c8097c0a4ec6e8cc4cd3dc61afc7f368057f4ef4b6534df9f6dd31634a4ac4 ]
HIOC_HOME="$RUNTIME" python3 "$RUNTIME/pi4/bin/hioc-validate-manufacturer.py" database --database "$INSTALL_STAGE/manufacturer-db.json" --manifest "$INSTALL_STAGE/manufacturer-db.manifest.json" --json
sync -f "$INSTALL_STAGE/manufacturer-db.json"; sync -f "$INSTALL_STAGE/manufacturer-db.manifest.json"; sync -f "$INSTALL_STAGE"; sync -f "$DATA_ROOT"
mv -- "$INSTALL_STAGE" "$FINAL_DIR"
INSTALL_STAGE=''
sync -f "$VERSIONS"
[ "$(stat -c %a "$FINAL_DIR")" = 700 ] && [ "$(stat -c %U:%G "$FINAL_DIR")" = jazofv1:jazofv1 ]
for p in "$FINAL_DB" "$FINAL_MF"; do [ -f "$p" ] && [ ! -L "$p" ] && [ "$(stat -c %a "$p")" = 600 ] && [ "$(stat -c %U:%G "$p")" = jazofv1:jazofv1 ]; done
! find "$FINAL_DIR" -type f -iname '*.csv' | grep -q .
printf 'DATASET_INSTALL=PASS_NEW_IMMUTABLE_VERSION\n'
```

`/tmp` is not assumed to share a filesystem with `/home`; explicit files are
copied into a same-filesystem hidden staging directory and atomically renamed.
An identical existing final directory is accepted without replacement; any
difference stops. Run Action 6 only; return output.

## Action 7 — Configuration activation

Target: PI3 runtime configuration. Mutation: conditional atomic configuration
update plus exact backup. Rollback relevance: configuration domain.

```bash
set -euo pipefail
umask 077
RUNTIME=/home/jazofv1/hioc
EVIDENCE_DIR='/tmp/hioc-pe3-production-validation-XXXXXXXX'
CONFIG="$RUNTIME/config/hioc.conf"
FINAL_DB="$RUNTIME/data/manufacturer/versions/local-ieee-ra--2026-08-11-r1/manufacturer-db.json"
CONFIG_BACKUP_DIR="$RUNTIME/backups/config"
install -d -o jazofv1 -g jazofv1 -m 0700 "$CONFIG_BACKUP_DIR"
CURRENT="$(python3 - "$CONFIG" <<'PY'
import pathlib,sys
lines=pathlib.Path(sys.argv[1]).read_text(encoding='utf-8').splitlines()
values=[x.split('=',1)[1].strip().strip("\"'") for x in lines if x.startswith('MANUFACTURER_DB_PATH=')]
if len(values)>1: raise SystemExit(2)
print(values[0] if values else '')
PY
)"
if [ -n "$CURRENT" ] && [ "$CURRENT" != "$FINAL_DB" ]; then printf 'CONFIG_RESULT=INPUT_OR_PRECONDITION_ERROR_DIFFERENT_VALUE\n' >&2; exit 20; fi
if [ "$CURRENT" = "$FINAL_DB" ]; then printf 'NONE\n' > "$EVIDENCE_DIR/config-backup-path.txt"; printf 'CONFIG_RESULT=PASS_ALREADY_ACTIVE\n'; exit 0; fi
CONFIG_BACKUP="$CONFIG_BACKUP_DIR/hioc.conf.$(date -u +%Y%m%dT%H%M%SZ).pre-pe3"
install -o jazofv1 -g jazofv1 -m 0600 "$CONFIG" "$CONFIG_BACKUP"
printf '%s\n' "$CONFIG_BACKUP" > "$EVIDENCE_DIR/config-backup-path.txt"
python3 - "$CONFIG" "$FINAL_DB" <<'PY'
import os,pathlib,sys,tempfile
p=pathlib.Path(sys.argv[1]); value=sys.argv[2]; lines=p.read_text(encoding='utf-8').splitlines(); found=False; out=[]
for line in lines:
 if line.startswith('MANUFACTURER_DB_PATH='):
  if found: raise SystemExit('duplicate MANUFACTURER_DB_PATH')
  out.append(f'MANUFACTURER_DB_PATH="{value}"'); found=True
 else: out.append(line)
if not found: out.append(f'MANUFACTURER_DB_PATH="{value}"')
fd,name=tempfile.mkstemp(prefix='.hioc.conf.',dir=p.parent); os.close(fd)
q=pathlib.Path(name); q.write_text('\n'.join(out)+'\n',encoding='utf-8'); os.chmod(q,0o600); os.replace(q,p)
PY
chown jazofv1:jazofv1 "$CONFIG" && chmod 0600 "$CONFIG"
grep -Fxq "MANUFACTURER_DB_PATH=\"$FINAL_DB\"" "$CONFIG"
HIOC_HOME="$RUNTIME" python3 "$RUNTIME/pi4/bin/hioc-validate-manufacturer.py" database --database "$FINAL_DB" --manifest "${FINAL_DB%/*}/manufacturer-db.manifest.json" --json
printf 'CONFIG_BACKUP=%s\nCONFIG_RESULT=PASS_ACTIVATED\n' "$CONFIG_BACKUP"
```

Absent and empty values activate after backup; the same value is a no-op; a
different nonempty value is an input/precondition error and is never overwritten.
Run Action 7 only; return output.

## Action 8 — Protected pre-state and manufacturer generation

Target: PI3 runtime state. Mutation: evidence directory, manufacturer sidecar,
and manufacturer status only. Rollback relevance: sidecar/config domains.

Use the exact `EVIDENCE_DIR` returned by Action 5:

```bash
set -euo pipefail
set +x
RUNTIME=/home/jazofv1/hioc
SOURCE=/home/jazofv1/hioc-release-source
EVIDENCE_DIR='/tmp/hioc-pe3-production-validation-XXXXXXXX'
mkdir -p "$EVIDENCE_DIR/pre" "$EVIDENCE_DIR/post"
chmod 0700 "$EVIDENCE_DIR" "$EVIDENCE_DIR/pre" "$EVIDENCE_DIR/post"
python3 - "$RUNTIME" "$EVIDENCE_DIR/pre/protected.json" <<'PY'
import hashlib,json,pathlib,sys
root=pathlib.Path(sys.argv[1]); target=pathlib.Path(sys.argv[2])
stable=['state/inventory/inventory.json','state/inventory/devices.json','state/inventory/services.json','state/inventory/topology.json','state/inventory/dependencies.json','state/inventory/summary.json','state/inventory/status.json','state/inventory/enrichment.json','state/inventory/enrichment_status.json','state/inventory/assets.json','state/inventory/assets_status.json','state/platform/status.json']
live=['state/incidents/active.json','state/incidents/history.json','state/incidents/summary.json','state/incident_engine_status.json']
def clean(v):
 if isinstance(v,dict): return {k:clean(x) for k,x in sorted(v.items()) if k not in {'updated','updated_at','generated_at','timestamp','last_seen','last_changed'}}
 if isinstance(v,list): return [clean(x) for x in v]
 return v
def item(rel,kind):
 p=root/rel
 if not p.is_file() or p.is_symlink(): return {'path':rel,'class':kind,'present':False}
 value=json.loads(p.read_text(encoding='utf-8')); raw=json.dumps(clean(value),sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
 count=len(value) if isinstance(value,(dict,list)) else None
 return {'path':rel,'class':kind,'present':True,'semantic_sha256':hashlib.sha256(raw).hexdigest(),'top_level_count':count}
target.write_text(json.dumps({'stable':[item(x,'stable') for x in stable],'operational_drift':[item(x,'live') for x in live]},indent=2,sort_keys=True)+'\n',encoding='utf-8')
PY
/usr/bin/time -f 'manufacturer_generation_elapsed_seconds=%e manufacturer_generation_max_rss_kib=%M' -o "$EVIDENCE_DIR/generation-performance.txt" python3 "$RUNTIME/pi4/bin/hioc-generate-manufacturer.py" --home "$RUNTIME" --json | tee "$EVIDENCE_DIR/generation-result.json"
jq -e '.result=="PASS" and .status=="online" and (.record_count|type)=="number" and (.matched_count|type)=="number" and (.unknown_count|type)=="number" and (.excluded_count|type)=="number" and (.invalid_count|type)=="number" and .error==null' "$EVIDENCE_DIR/generation-result.json" >/dev/null
printf 'MANUFACTURER_GENERATION=PASS\n'
```

The generated output is aggregate only. Match percentage is not an acceptance
criterion. Stop on lock, database, inventory, write, or aggregate failure. Do not
manually edit sidecars. Run Action 8 only; return output.

## Action 9 — Production validation and Evidence Report

Target: PI3 runtime and evidence directory. Mutation: evidence files; repeated
generator calls for governed timing use no-op sidecar semantics. Rollback
relevance depends on demonstrated causal failure.

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

## Action 10 — Temporary transfer cleanup

Target: PI3 temporary staging only. Mutation: deletion of two verified staging
files and their exact staging directory. Rollback relevance: none.

```bash
set -euo pipefail
PI3_STAGE='/tmp/hioc-pe3-dataset-transfer-XXXXXXXX'
EVIDENCE_DIR='/tmp/hioc-pe3-production-validation-XXXXXXXX'
[ "$PI3_STAGE" != /tmp ] && [[ "$PI3_STAGE" == /tmp/hioc-pe3-dataset-transfer-* ]]
[ -d "$PI3_STAGE" ] && [ ! -L "$PI3_STAGE" ]
[ "$(find "$PI3_STAGE" -mindepth 1 -maxdepth 1 -printf '%f\n' | sort | paste -sd, -)" = 'manufacturer-db.json,manufacturer-db.manifest.json' ]
rm -- "$PI3_STAGE/manufacturer-db.json"
rm -- "$PI3_STAGE/manufacturer-db.manifest.json"
rmdir -- "$PI3_STAGE"
jq '.cleanup="PASS"' "$EVIDENCE_DIR/PE3_MANUFACTURER_PRODUCTION_EVIDENCE.json" > "$EVIDENCE_DIR/.evidence.tmp"
chmod 0600 "$EVIDENCE_DIR/.evidence.tmp"
mv -- "$EVIDENCE_DIR/.evidence.tmp" "$EVIDENCE_DIR/PE3_MANUFACTURER_PRODUCTION_EVIDENCE.json"
(cd "$EVIDENCE_DIR" && find . -type f ! -name EVIDENCE_CHECKSUMS.sha256 -print0 | sort -z | xargs -0 sha256sum > EVIDENCE_CHECKSUMS.sha256)
printf 'TRANSFER_CLEANUP=PASS\n'
```

Do not remove the final version, Windows sources/build, release backup,
configuration backup, or validation evidence. Run Action 10 only; return output.

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
| 3 | PI3 | staging verification PASS | No | Host/file/hash/validator error | None |
| 4 | PI3 source | synchronization PASS | Git fast-forward | Dirty/diverged/wrong commit | Source only |
| 5 | PI3 runtime | code deployment PASS and backup path | Runtime code/backup | Release/artifact/PI4 failure | Code |
| 6 | PI3 runtime | new or identical immutable dataset PASS | New version only | Existing difference/install failure | Dataset |
| 7 | PI3 runtime | config active/no-op PASS and backup if changed | Config/backup | Different value/config failure | Config |
| 8 | PI3 runtime | aggregate generation PASS | Sidecar/status/evidence | Generator failure | Sidecar/config |
| 9 | PI3 runtime | validation/evidence PASS | Evidence; no-op timing writes | Invariant/privacy/required threshold failure | Classified |
| 10 | PI3 `/tmp` | transfer cleanup PASS | Exact temporary deletion | Unexpected staging contents | None |

At every boundary: run only the named action, return its output, and wait for
explicit authorization. Never continue automatically.
