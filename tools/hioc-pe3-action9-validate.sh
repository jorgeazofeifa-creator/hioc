#!/usr/bin/env bash

# Governed PE-3 Action 9: read-only production validation and Evidence Report.

SOURCE=/home/jazofv1/hioc-release-source
RUNTIME=/home/jazofv1/hioc
TOOL_REL=tools/hioc-pe3-action9-validate.sh
VALIDATOR_REL=pi4/bin/hioc-validate-manufacturer.py
LIBRARY_REL=pi4/lib/hioc/manufacturer.py
ACTION8_REL=tools/hioc-pe3-action8-generate.sh
CONFIG="$RUNTIME/config/hioc.conf"
INVENTORY="$RUNTIME/state/inventory/inventory.json"
SIDE="$RUNTIME/state/inventory/manufacturer.json"
STATUS="$RUNTIME/state/inventory/manufacturer_status.json"
FINAL_DIR="$RUNTIME/data/manufacturer/versions/local-ieee-ra--2026-08-11-r1"
DB="$FINAL_DIR/manufacturer-db.json"
MF="$FINAL_DIR/manufacturer-db.manifest.json"
DB_SHA256=81f147cc57768c5797c4ad73a8c0369001bbdcbfe1548e71d3702c8c7f81e0e1
MF_SHA256=10c8097c0a4ec6e8cc4cd3dc61afc7f368057f4ef4b6534df9f6dd31634a4ac4
EXPECTED_RECORD_COUNT=53581
EVIDENCE_DIR=
ACTION8_EVIDENCE_DIR=
REPORT_TEMP=
RESULT_TEMP=
FAILURE_REPORTED=0
PERFORMANCE_ELAPSED_SECONDS=
PERFORMANCE_MAX_CHILD_RSS_KIB=
HISTORICAL_ELAPSED_TARGET_EXCEEDED=
HISTORICAL_RSS_TARGET_EXCEEDED=

active_git_operation() {
  for marker in MERGE_HEAD REBASE_HEAD CHERRY_PICK_HEAD REVERT_HEAD BISECT_LOG; do
    [ ! -e "$SOURCE/.git/$marker" ] || return 0
  done
  [ ! -d "$SOURCE/.git/rebase-merge" ] && [ ! -d "$SOURCE/.git/rebase-apply" ] || return 0
  return 1
}

owned_file() {
  [ -f "$1" ] && [ ! -L "$1" ] &&
    [ "$(stat -c %U:%G "$1" 2>/dev/null)" = jazofv1:jazofv1 ] &&
    [ "$(stat -c %a "$1" 2>/dev/null)" = "$2" ]
}

owned_directory() {
  [ -d "$1" ] && [ ! -L "$1" ] &&
    [ "$(stat -c %U:%G "$1" 2>/dev/null)" = jazofv1:jazofv1 ] &&
    [ "$(stat -c %a "$1" 2>/dev/null)" = "$2" ]
}

safe_owned_file() {
  [ -f "$1" ] && [ ! -L "$1" ] &&
    [ "$(stat -c %U:%G "$1" 2>/dev/null)" = jazofv1:jazofv1 ] || return 1
  mode="$(stat -c %a "$1" 2>/dev/null)" || return 1
  [ $((8#$mode & 0022)) -eq 0 ]
}

cleanup_temps() {
  for candidate in "$REPORT_TEMP" "$RESULT_TEMP"; do
    [ -n "$candidate" ] || continue
    case "$candidate" in "$EVIDENCE_DIR"/.action9-*) ;; *) return 1 ;; esac
    [ -e "$candidate" ] || [ -L "$candidate" ] || continue
    [ -f "$candidate" ] && [ ! -L "$candidate" ] || return 1
    rm -- "$candidate" >/dev/null 2>&1 || return 1
  done
  REPORT_TEMP=
  RESULT_TEMP=
}

write_failure_result() {
  [ -n "$EVIDENCE_DIR" ] && owned_directory "$EVIDENCE_DIR" 700 || return 0
  RESULT_TEMP="$(mktemp "$EVIDENCE_DIR/.action9-result.XXXXXXXX" 2>/dev/null)" || return 1
  chmod 0600 "$RESULT_TEMP" || return 1
  printf 'RESULT=%s\nERROR_CODE=%s\nFAILURE_STAGE=%s\nROLLBACK_RECOMMENDED=FALSE\nEVIDENCE_DIR=%s\n' "$1" "$2" "$3" "$EVIDENCE_DIR" > "$RESULT_TEMP" || return 1
  sync -f "$RESULT_TEMP" || return 1
  mv -fT -- "$RESULT_TEMP" "$EVIDENCE_DIR/action9-result.txt" || return 1
  RESULT_TEMP=
  sync -f "$EVIDENCE_DIR/action9-result.txt" && sync -f "$EVIDENCE_DIR"
}

fail_action9() {
  FAILURE_REPORTED=1
  result=$1 code=$2 stage=$3
  if ! cleanup_temps; then
    result=VALIDATION_FAIL code=EVIDENCE_TEMP_CLEANUP_FAILED stage=EVIDENCE_CLEANUP
  fi
  write_failure_result "$result" "$code" "$stage" >/dev/null 2>&1 || true
  printf 'RESULT=%s\nERROR_CODE=%s\nFAILURE_STAGE=%s\nROLLBACK_RECOMMENDED=FALSE\n' "$result" "$code" "$stage"
  [ -z "$EVIDENCE_DIR" ] || printf 'EVIDENCE_DIR=%s\n' "$EVIDENCE_DIR"
  return 1
}

verify_target_source_runtime() {
  [ "$(hostname -s 2>/dev/null)" = nutandpihole ] || { fail_action9 INPUT_OR_PRECONDITION_ERROR WRONG_TARGET TARGET_IDENTITY; return 1; }
  ip -o -4 addr show scope global 2>/dev/null | awk '{print $4}' | cut -d/ -f1 | grep -Fxq 192.168.100.252 || { fail_action9 INPUT_OR_PRECONDITION_ERROR WRONG_TARGET TARGET_IDENTITY; return 1; }
  [ "$(id -un 2>/dev/null)" = jazofv1 ] && [ "$(id -gn 2>/dev/null)" = jazofv1 ] || { fail_action9 INPUT_OR_PRECONDITION_ERROR WRONG_OPERATOR TARGET_IDENTITY; return 1; }
  printf 'TARGET_IDENTITY=PASS\n'
  [ -d "$SOURCE/.git" ] || { fail_action9 INPUT_OR_PRECONDITION_ERROR SOURCE_REPOSITORY_MISSING SOURCE_IDENTITY; return 1; }
  [ "$(git -C "$SOURCE" branch --show-current 2>/dev/null)" = main ] || { fail_action9 INPUT_OR_PRECONDITION_ERROR WRONG_BRANCH SOURCE_IDENTITY; return 1; }
  [ -z "$(git -C "$SOURCE" status --porcelain 2>/dev/null)" ] || { fail_action9 INPUT_OR_PRECONDITION_ERROR SOURCE_REPOSITORY_DIRTY SOURCE_IDENTITY; return 1; }
  active_git_operation && { fail_action9 INPUT_OR_PRECONDITION_ERROR ACTIVE_GIT_OPERATION SOURCE_IDENTITY; return 1; }
  [ "$(git -C "$SOURCE" rev-parse HEAD 2>/dev/null)" = "$GOVERNANCE_COMMIT" ] && [ "$(git -C "$SOURCE" rev-parse origin/main 2>/dev/null)" = "$GOVERNANCE_COMMIT" ] || { fail_action9 INPUT_OR_PRECONDITION_ERROR GOVERNANCE_IDENTITY_MISMATCH SOURCE_IDENTITY; return 1; }
  for rel in "$TOOL_REL" "$VALIDATOR_REL" "$LIBRARY_REL" "$ACTION8_REL"; do
    [ -f "$SOURCE/$rel" ] && [ ! -L "$SOURCE/$rel" ] || { fail_action9 INPUT_OR_PRECONDITION_ERROR GOVERNED_ARTIFACT_UNSAFE SOURCE_IDENTITY; return 1; }
    expected="$(git -C "$SOURCE" rev-parse "$GOVERNANCE_COMMIT:$rel" 2>/dev/null)" || { fail_action9 INPUT_OR_PRECONDITION_ERROR GOVERNED_ARTIFACT_GIT_IDENTITY_MISMATCH SOURCE_IDENTITY; return 1; }
    actual="$(git -C "$SOURCE" hash-object --path="$rel" "$SOURCE/$rel" 2>/dev/null)" || { fail_action9 INPUT_OR_PRECONDITION_ERROR GOVERNED_ARTIFACT_WORKTREE_IDENTITY_MISMATCH SOURCE_IDENTITY; return 1; }
    [ "$actual" = "$expected" ] && git -C "$SOURCE" diff --quiet -- "$rel" || { fail_action9 INPUT_OR_PRECONDITION_ERROR GOVERNED_ARTIFACT_WORKTREE_IDENTITY_MISMATCH SOURCE_IDENTITY; return 1; }
  done
  printf 'SOURCE_IDENTITY=PASS\n'
  [ -d "$RUNTIME" ] && [ ! -L "$RUNTIME" ] || { fail_action9 INPUT_OR_PRECONDITION_ERROR RUNTIME_ROOT_INVALID RUNTIME_IDENTITY; return 1; }
  for rel in "$VALIDATOR_REL" "$LIBRARY_REL"; do
    [ -f "$RUNTIME/$rel" ] && [ ! -L "$RUNTIME/$rel" ] && cmp -s "$SOURCE/$rel" "$RUNTIME/$rel" || { fail_action9 INPUT_OR_PRECONDITION_ERROR RUNTIME_ARTIFACT_IDENTITY_MISMATCH RUNTIME_IDENTITY; return 1; }
  done
  printf 'RUNTIME_IDENTITY=PASS\n'
}

verify_action8_evidence() {
  case "$ACTION8_EVIDENCE_DIR" in /tmp/hioc-pe3-action8-*) ;; *) fail_action9 INPUT_OR_PRECONDITION_ERROR ACTION8_EVIDENCE_PATH_INVALID ACTION8_EVIDENCE_IDENTITY; return 1 ;; esac
  [ "$(dirname -- "$ACTION8_EVIDENCE_DIR")" = /tmp ] && owned_directory "$ACTION8_EVIDENCE_DIR" 700 || { fail_action9 INPUT_OR_PRECONDITION_ERROR ACTION8_EVIDENCE_DIRECTORY_UNSAFE ACTION8_EVIDENCE_IDENTITY; return 1; }
  owned_directory "$ACTION8_EVIDENCE_DIR/pre" 700 || { fail_action9 INPUT_OR_PRECONDITION_ERROR ACTION8_EVIDENCE_DIRECTORY_UNSAFE ACTION8_EVIDENCE_IDENTITY; return 1; }
  expected='generation-performance.txt,generation-result.json,pre'
  actual="$(find "$ACTION8_EVIDENCE_DIR" -mindepth 1 -maxdepth 1 -printf '%f\n' 2>/dev/null | sort | paste -sd, -)"
  [ "$actual" = "$expected" ] || { fail_action9 INPUT_OR_PRECONDITION_ERROR ACTION8_EVIDENCE_CONTENTS_INVALID ACTION8_EVIDENCE_IDENTITY; return 1; }
  [ "$(find "$ACTION8_EVIDENCE_DIR/pre" -mindepth 1 -maxdepth 1 -printf '%f\n' 2>/dev/null | sort | paste -sd, -)" = protected.json ] || { fail_action9 INPUT_OR_PRECONDITION_ERROR ACTION8_EVIDENCE_CONTENTS_INVALID ACTION8_EVIDENCE_IDENTITY; return 1; }
  for path in "$ACTION8_EVIDENCE_DIR/generation-result.json" "$ACTION8_EVIDENCE_DIR/generation-performance.txt" "$ACTION8_EVIDENCE_DIR/pre/protected.json"; do
    owned_file "$path" 600 || { fail_action9 INPUT_OR_PRECONDITION_ERROR ACTION8_EVIDENCE_FILE_UNSAFE ACTION8_EVIDENCE_IDENTITY; return 1; }
  done
  [ ! -e "$ACTION8_EVIDENCE_DIR/generation-failure.json" ] && [ ! -L "$ACTION8_EVIDENCE_DIR/generation-failure.json" ] || { fail_action9 INPUT_OR_PRECONDITION_ERROR ACTION8_FAILURE_EVIDENCE_PRESENT ACTION8_EVIDENCE_IDENTITY; return 1; }
  printf 'ACTION8_EVIDENCE_IDENTITY=PASS\n'

  python3 - "$ACTION8_EVIDENCE_DIR" <<'PY' >/dev/null 2>&1
import json, pathlib, sys
root=pathlib.Path(sys.argv[1])
try:
    result=json.loads((root/'generation-result.json').read_text(encoding='utf-8'))
except (OSError, UnicodeError, json.JSONDecodeError):
    raise SystemExit(2)
keys={'schema_version','result','status','record_count','matched_count','unknown_count','excluded_count','invalid_count','error'}
if not isinstance(result,dict) or set(result)!=keys or result.get('schema_version')!='1.0' or result.get('result')!='PASS' or result.get('status')!='online' or result.get('error') is not None: raise SystemExit(2)
counts=[result.get(k) for k in ('record_count','matched_count','unknown_count','excluded_count','invalid_count')]
if any(type(x) is not int or x < 0 for x in counts) or sum(counts[1:])!=counts[0]: raise SystemExit(3)
PY
  case "$?" in
    0) ;;
    3) fail_action9 VALIDATION_FAIL ACTION8_RESULT_COUNTS_INVALID ACTION8_RESULT_VALIDATION; return 1 ;;
    *) fail_action9 VALIDATION_FAIL ACTION8_RESULT_SCHEMA_INVALID ACTION8_RESULT_VALIDATION; return 1 ;;
  esac
  printf 'ACTION8_RESULT_VALIDATION=PASS\n'

  performance_values="$(python3 - "$ACTION8_EVIDENCE_DIR" <<'PY'
import pathlib, re, sys
root=pathlib.Path(sys.argv[1])
try:
    text=(root/'generation-performance.txt').read_text(encoding='ascii')
except (OSError, UnicodeError):
    raise SystemExit(4)
m=re.fullmatch(r'manufacturer_generation_elapsed_seconds=([^ ]+) manufacturer_generation_max_rss_kib=([^ ]+) manufacturer_generation_measurement_status=([^\n]+)\n',text)
if not m: raise SystemExit(4)
try:
    elapsed=float(m.group(1)); rss=int(m.group(2))
except ValueError:
    raise SystemExit(4)
if m.group(3)!='MEASURED': raise SystemExit(5)
if elapsed < 0 or rss < 0: raise SystemExit(4)
print(f'{elapsed:.6f}\t{rss}\t{"TRUE" if elapsed > 4 else "FALSE"}\t{"TRUE" if rss*1024 > 50331648 else "FALSE"}')
PY
)"
  case "$?" in
    0) ;;
    5) fail_action9 VALIDATION_FAIL ACTION8_PERFORMANCE_STATUS_INVALID ACTION8_PERFORMANCE_SYNTAX; return 1 ;;
    *) fail_action9 VALIDATION_FAIL ACTION8_PERFORMANCE_FORMAT_INVALID ACTION8_PERFORMANCE_SYNTAX; return 1 ;;
  esac
  IFS="$(printf '\t')" read -r PERFORMANCE_ELAPSED_SECONDS PERFORMANCE_MAX_CHILD_RSS_KIB HISTORICAL_ELAPSED_TARGET_EXCEEDED HISTORICAL_RSS_TARGET_EXCEEDED <<EOF
$performance_values
EOF
  [ -n "$PERFORMANCE_ELAPSED_SECONDS" ] && [ -n "$PERFORMANCE_MAX_CHILD_RSS_KIB" ] || { fail_action9 VALIDATION_FAIL ACTION8_PERFORMANCE_FORMAT_INVALID ACTION8_PERFORMANCE_SYNTAX; return 1; }
  printf 'ACTION8_PERFORMANCE_SYNTAX=PASS\n'
  printf 'PERFORMANCE_ELAPSED_SECONDS=%s\n' "$PERFORMANCE_ELAPSED_SECONDS"
  printf 'PERFORMANCE_MAX_CHILD_RSS_KIB=%s\n' "$PERFORMANCE_MAX_CHILD_RSS_KIB"
  printf 'PERFORMANCE_RSS_SEMANTIC=TOTAL_PEAK_CHILD_RSS\n'
  printf 'PERFORMANCE_MEASUREMENT_STATUS=MEASURED\n'
  printf 'PERFORMANCE_BASELINE_STATUS=UNVALIDATED\n'
  printf 'PERFORMANCE_OBSERVATION=INSUFFICIENT_BASELINE\n'
  printf 'HISTORICAL_ELAPSED_TARGET_EXCEEDED=%s\n' "$HISTORICAL_ELAPSED_TARGET_EXCEEDED"
  printf 'HISTORICAL_RSS_TARGET_EXCEEDED=%s\n' "$HISTORICAL_RSS_TARGET_EXCEEDED"
  printf 'HISTORICAL_TARGETS_PRODUCTION_ENFORCED=FALSE\n'
  printf 'ACTION8_PERFORMANCE_ASSESSMENT=PASS\n'

  python3 - "$ACTION8_EVIDENCE_DIR" <<'PY' >/dev/null 2>&1
import json, pathlib, sys
root=pathlib.Path(sys.argv[1])
try:
    protected=json.loads((root/'pre/protected.json').read_text(encoding='utf-8'))
except (OSError, UnicodeError, json.JSONDecodeError):
    raise SystemExit(2)
if not isinstance(protected,dict) or set(protected)!={'stable','operational_drift'} or not isinstance(protected['stable'],list) or not isinstance(protected['operational_drift'],list): raise SystemExit(2)
PY
  [ "$?" -eq 0 ] || { fail_action9 VALIDATION_FAIL ACTION8_PROTECTED_SNAPSHOT_SCHEMA_INVALID ACTION8_PROTECTED_SNAPSHOT_VALIDATION; return 1; }
  printf 'ACTION8_PROTECTED_SNAPSHOT_VALIDATION=PASS\n'
}

prepare_evidence() {
  EVIDENCE_DIR="$(mktemp -d /tmp/hioc-pe3-action9-XXXXXXXX 2>/dev/null)" || { fail_action9 VALIDATION_FAIL EVIDENCE_DIRECTORY_CREATE_FAILED EVIDENCE_PREPARATION; return 1; }
  chmod 0700 "$EVIDENCE_DIR" && owned_directory "$EVIDENCE_DIR" 700 || { fail_action9 VALIDATION_FAIL EVIDENCE_DIRECTORY_INVALID EVIDENCE_PREPARATION; return 1; }
  printf 'EVIDENCE_PREPARATION=PASS\n'
}

validate_production() {
  owned_file "$CONFIG" 600 && bash -n "$CONFIG" >/dev/null 2>&1 || { fail_action9 INPUT_OR_PRECONDITION_ERROR CONFIGURATION_IDENTITY_INVALID CONFIGURATION_IDENTITY; return 1; }
  selected="$(python3 - "$CONFIG" <<'PY'
import pathlib,sys
values=[]
for line in pathlib.Path(sys.argv[1]).read_text(encoding='utf-8').splitlines():
    if line.startswith('MANUFACTURER_DB_PATH='):
        value=line.split('=',1)[1].strip()
        if len(value)>=2 and value[0]==value[-1] and value[0] in "\"'": value=value[1:-1]
        values.append(value)
if len(values)!=1: raise SystemExit(2)
print(values[0])
PY
)" || { fail_action9 INPUT_OR_PRECONDITION_ERROR CONFIGURATION_IDENTITY_INVALID CONFIGURATION_IDENTITY; return 1; }
  [ "$selected" = "$DB" ] || { fail_action9 INPUT_OR_PRECONDITION_ERROR CONFIGURATION_SELECTION_MISMATCH CONFIGURATION_IDENTITY; return 1; }
  printf 'CONFIGURATION_IDENTITY=PASS\n'
  owned_directory "$FINAL_DIR" 700 && owned_file "$DB" 600 && owned_file "$MF" 600 || { fail_action9 INPUT_OR_PRECONDITION_ERROR DATASET_IDENTITY_INVALID DATASET_IDENTITY; return 1; }
  [ "$(sha256sum "$DB" | awk '{print $1}')" = "$DB_SHA256" ] && [ "$(sha256sum "$MF" | awk '{print $1}')" = "$MF_SHA256" ] || { fail_action9 INPUT_OR_PRECONDITION_ERROR DATASET_IDENTITY_MISMATCH DATASET_IDENTITY; return 1; }
  printf 'DATASET_IDENTITY=PASS\n'
  safe_owned_file "$INVENTORY" || { fail_action9 INPUT_OR_PRECONDITION_ERROR INVENTORY_IDENTITY_INVALID INVENTORY_IDENTITY; return 1; }
  owned_file "$SIDE" 600 && owned_file "$STATUS" 600 || { fail_action9 INPUT_OR_PRECONDITION_ERROR MANUFACTURER_ARTIFACT_IDENTITY_INVALID MANUFACTURER_ARTIFACT_IDENTITY; return 1; }
  [ -z "$(find "$RUNTIME/state/inventory" -maxdepth 1 -type f \( -name '.manufacturer*.tmp' -o -name '.manufacturer_status*.tmp' \) -print -quit 2>/dev/null)" ] || { fail_action9 VALIDATION_FAIL MANUFACTURER_TEMP_ARTIFACT_PRESENT MANUFACTURER_ARTIFACT_IDENTITY; return 1; }
  printf 'INVENTORY_IDENTITY=PASS\nMANUFACTURER_ARTIFACT_IDENTITY=PASS\n'
  REPORT_TEMP="$(mktemp "$EVIDENCE_DIR/.action9-report.XXXXXXXX" 2>/dev/null)" || { fail_action9 VALIDATION_FAIL EVIDENCE_TEMP_CREATE_FAILED PRODUCTION_VALIDATION; return 1; }
  chmod 0600 "$REPORT_TEMP" || { fail_action9 VALIDATION_FAIL EVIDENCE_TEMP_PERMISSION_FAILED PRODUCTION_VALIDATION; return 1; }
  python3 - "$RUNTIME" "$SOURCE" "$GOVERNANCE_COMMIT" "$ACTION8_EVIDENCE_DIR" "$REPORT_TEMP" "$DB_SHA256" "$MF_SHA256" "$EXPECTED_RECORD_COUNT" "$PERFORMANCE_ELAPSED_SECONDS" "$PERFORMANCE_MAX_CHILD_RSS_KIB" "$HISTORICAL_ELAPSED_TARGET_EXCEEDED" "$HISTORICAL_RSS_TARGET_EXCEEDED" <<'PY'
import hashlib,json,os,pathlib,subprocess,sys
runtime,source=map(pathlib.Path,sys.argv[1:3]); commit,action8=sys.argv[3:5]; target=pathlib.Path(sys.argv[5]); db_sha,mf_sha=sys.argv[6:8]
expected_database_records=int(sys.argv[8])
elapsed=float(sys.argv[9]); max_child_rss_kib=int(sys.argv[10]); historical_elapsed_exceeded=sys.argv[11]=='TRUE'; historical_rss_exceeded=sys.argv[12]=='TRUE'
paths=[runtime/'config/hioc.conf',runtime/'state/inventory/inventory.json',runtime/'state/inventory/manufacturer.json',runtime/'state/inventory/manufacturer_status.json',runtime/'data/manufacturer/versions/local-ieee-ra--2026-08-11-r1/manufacturer-db.json',runtime/'data/manufacturer/versions/local-ieee-ra--2026-08-11-r1/manufacturer-db.manifest.json']
def snapshot(): return {str(p.relative_to(runtime)):{'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths}
before=snapshot()
validator=runtime/'pi4/bin/hioc-validate-manufacturer.py'; side=paths[2]; status=paths[3]; inventory=paths[1]; db=paths[4]; mf=paths[5]
def run(args):
    cp=subprocess.run([sys.executable,str(validator),*args,'--json'],text=True,capture_output=True)
    if cp.returncode or cp.stderr: raise SystemExit(20)
    return json.loads(cp.stdout)
database=run(['database','--database',str(db),'--manifest',str(mf)])
artifact=run(['sidecar','--sidecar',str(side),'--status',str(status),'--inventory',str(inventory),'--database',str(db),'--manifest',str(mf)])
if database.get('result')!='PASS' or database.get('privacy_safe') is not True or database.get('record_count')!=expected_database_records: raise SystemExit(21)
if artifact.get('result')!='PASS' or artifact.get('privacy_safe') is not True or artifact.get('status')!='online' or type(artifact.get('record_count')) is not int: raise SystemExit(22)
after=snapshot()
if before!=after: raise SystemExit(23)
generation=json.loads((pathlib.Path(action8)/'generation-result.json').read_text(encoding='utf-8'))
if artifact['record_count']!=generation['record_count']: raise SystemExit(24)
report={'schema_version':'1.0','result':'PASS','action':'PE-3_ACTION9','governance_commit':commit,'target':{'hostname':'nutandpihole','ipv4':'192.168.100.252'},'action8_evidence':{'path':action8,'generation_result_sha256':hashlib.sha256((pathlib.Path(action8)/'generation-result.json').read_bytes()).hexdigest(),'generation_performance_sha256':hashlib.sha256((pathlib.Path(action8)/'generation-performance.txt').read_bytes()).hexdigest(),'validated':True},'dataset':{'id':'local-ieee-ra','version':'2026-08-11-r1','database_sha256':db_sha,'manifest_sha256':mf_sha,'record_count':expected_database_records},'manufacturer':{'status':'online','record_count':artifact['record_count'],'privacy_safe':True},'performance':{'source':'ACTION8_GOVERNED_EVIDENCE','measurement_status':'MEASURED','elapsed_seconds':elapsed,'maximum_child_rss_kib':max_child_rss_kib,'rss_semantic':'TOTAL_PEAK_CHILD_RSS','baseline_status':'UNVALIDATED','observation':'INSUFFICIENT_BASELINE','historical_elapsed_target_seconds':4,'historical_incremental_rss_target_bytes':50331648,'historical_elapsed_target_exceeded':historical_elapsed_exceeded,'historical_rss_target_exceeded':historical_rss_exceeded,'historical_targets_production_enforced':False},'protected_state':{'unchanged':True,'artifacts':before},'warnings':['PERFORMANCE_BASELINE_NOT_ESTABLISHED'],'rollback_recommended':False}
data=(json.dumps(report,sort_keys=True,separators=(',',':'))+'\n').encode()
with target.open('wb') as handle: handle.write(data); handle.flush(); os.fsync(handle.fileno())
PY
  rc=$?
  case "$rc" in
    0) ;;
    20|21|22|24) fail_action9 VALIDATION_FAIL MANUFACTURER_ARTIFACT_VALIDATION_FAILED MANUFACTURER_ARTIFACT_VALIDATION; return 1 ;;
    23) fail_action9 VALIDATION_FAIL PROTECTED_STATE_CHANGED PROTECTED_STATE; return 1 ;;
    *) fail_action9 VALIDATION_FAIL PRODUCTION_VALIDATION_UNEXPECTED PRODUCTION_VALIDATION; return 1 ;;
  esac
  printf 'MANUFACTURER_ARTIFACT_VALIDATION=PASS\nPROTECTED_STATE=PASS\n'
}

publish_report() {
  mv -fT -- "$REPORT_TEMP" "$EVIDENCE_DIR/evidence-report.json" || { fail_action9 VALIDATION_FAIL EVIDENCE_REPORT_PUBLICATION_FAILED EVIDENCE_REPORT; return 1; }
  REPORT_TEMP=
  sync -f "$EVIDENCE_DIR/evidence-report.json" || { fail_action9 VALIDATION_FAIL EVIDENCE_REPORT_FSYNC_FAILED EVIDENCE_REPORT; return 1; }
  RESULT_TEMP="$(mktemp "$EVIDENCE_DIR/.action9-result.XXXXXXXX" 2>/dev/null)" || { fail_action9 VALIDATION_FAIL EVIDENCE_RESULT_CREATE_FAILED EVIDENCE_REPORT; return 1; }
  chmod 0600 "$RESULT_TEMP" || { fail_action9 VALIDATION_FAIL EVIDENCE_RESULT_PERMISSION_FAILED EVIDENCE_REPORT; return 1; }
  printf 'RESULT=PASS\nERROR_CODE=NONE\nFAILURE_STAGE=COMPLETE\nROLLBACK_RECOMMENDED=FALSE\nEVIDENCE_DIR=%s\n' "$EVIDENCE_DIR" > "$RESULT_TEMP" || { fail_action9 VALIDATION_FAIL EVIDENCE_RESULT_WRITE_FAILED EVIDENCE_REPORT; return 1; }
  sync -f "$RESULT_TEMP" || { fail_action9 VALIDATION_FAIL EVIDENCE_RESULT_FSYNC_FAILED EVIDENCE_REPORT; return 1; }
  mv -fT -- "$RESULT_TEMP" "$EVIDENCE_DIR/action9-result.txt" || { fail_action9 VALIDATION_FAIL EVIDENCE_RESULT_PUBLICATION_FAILED EVIDENCE_REPORT; return 1; }
  RESULT_TEMP=
  sync -f "$EVIDENCE_DIR/action9-result.txt" && sync -f "$EVIDENCE_DIR" || { fail_action9 VALIDATION_FAIL EVIDENCE_DIRECTORY_FSYNC_FAILED EVIDENCE_REPORT; return 1; }
  printf 'EVIDENCE_REPORT=PASS\nEVIDENCE_DIR=%s\nACTION9=COMPLETE\nRESULT=PASS\nROLLBACK_RECOMMENDED=FALSE\n' "$EVIDENCE_DIR"
}

main() {
  [ "$#" -eq 4 ] && [ "$1" = --governance-commit ] && [ "$3" = --action8-evidence-dir ] || { fail_action9 INPUT_OR_PRECONDITION_ERROR INVALID_ARGUMENTS INPUT_VALIDATION; return 1; }
  GOVERNANCE_COMMIT=$2
  ACTION8_EVIDENCE_DIR=$4
  printf '%s' "$GOVERNANCE_COMMIT" | grep -Eq '^[0-9a-f]{40}$' || { fail_action9 INPUT_OR_PRECONDITION_ERROR INVALID_GOVERNANCE_COMMIT INPUT_VALIDATION; return 1; }
  verify_target_source_runtime || return 1
  verify_action8_evidence || return 1
  prepare_evidence || return 1
  validate_production || return 1
  publish_report || return 1
}

action9_entry() {
  main "$@"
  rc=$?
  if [ "$rc" -ne 0 ] && [ "$FAILURE_REPORTED" -ne 1 ]; then
    fail_action9 VALIDATION_FAIL ACTION9_UNEXPECTED_ERROR ACTION9_UNEXPECTED
    rc=$?
  fi
  return "$rc"
}

action9_entry "$@"
