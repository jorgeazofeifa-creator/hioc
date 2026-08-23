#!/usr/bin/env bash

# Governed PE-3 Production Action 8: protected pre-state and manufacturer generation.

SOURCE=/home/jazofv1/hioc-release-source
RUNTIME=/home/jazofv1/hioc
SCRIPT_REL=tools/hioc-pe3-action8-generate.sh
GENERATOR_REL=pi4/bin/hioc-generate-manufacturer.py
VALIDATOR_REL=pi4/bin/hioc-validate-manufacturer.py
LIBRARY_REL=pi4/lib/hioc/manufacturer.py
CONFIG="$RUNTIME/config/hioc.conf"
INVENTORY="$RUNTIME/state/inventory/inventory.json"
STATE_DIR="$RUNTIME/state/inventory"
SIDE="$STATE_DIR/manufacturer.json"
STATUS="$STATE_DIR/manufacturer_status.json"
FINAL_DIR="$RUNTIME/data/manufacturer/versions/local-ieee-ra--2026-08-11-r1"
DB="$FINAL_DIR/manufacturer-db.json"
MF="$FINAL_DIR/manufacturer-db.manifest.json"
TRANSPORT_STAGE=/tmp/hioc-pe3-dataset-transfer-PJ5qPbRS
DB_BYTES=8652642
MF_BYTES=1338
DB_SHA256=81f147cc57768c5797c4ad73a8c0369001bbdcbfe1548e71d3702c8c7f81e0e1
MF_SHA256=10c8097c0a4ec6e8cc4cd3dc61afc7f368057f4ef4b6534df9f6dd31634a4ac4
EXPECTED_DATABASE_RECORD_COUNT=53581
TEMP_RESULT=
TEMP_PERFORMANCE=
GENERATOR_SUCCEEDED=FALSE
EVIDENCE_DIR_CREATED=FALSE

cleanup_evidence_temps() {
  for candidate in "$TEMP_RESULT" "$TEMP_PERFORMANCE"; do
    [ -n "$candidate" ] || continue
    case "$candidate" in "$EVIDENCE_DIR"/.action8-*) ;; *) return 1 ;; esac
    [ -e "$candidate" ] || [ -L "$candidate" ] || continue
    [ -f "$candidate" ] && [ ! -L "$candidate" ] || return 1
    rm -- "$candidate" >/dev/null 2>&1 || return 1
  done
  TEMP_RESULT=
  TEMP_PERFORMANCE=
}

fail_action8() {
  FAILURE_REPORTED=1
  result=$1
  code=$2
  stage=$3
  rollback=$4
  if ! cleanup_evidence_temps; then
    printf 'RESULT=VALIDATION_FAIL\nERROR_CODE=EVIDENCE_TEMP_CLEANUP_FAILED\nFAILURE_STAGE=EVIDENCE_CLEANUP\nROLLBACK_RECOMMENDED=%s\n' "$rollback"
    [ "${EVIDENCE_DIR_CREATED:-FALSE}" != TRUE ] || printf 'EVIDENCE_DIR=%s\n' "$EVIDENCE_DIR"
    return 1
  fi
  printf 'RESULT=%s\nERROR_CODE=%s\nFAILURE_STAGE=%s\nROLLBACK_RECOMMENDED=%s\n' "$result" "$code" "$stage" "$rollback"
  [ "${EVIDENCE_DIR_CREATED:-FALSE}" != TRUE ] || printf 'EVIDENCE_DIR=%s\n' "$EVIDENCE_DIR"
  return 1
}

active_git_operation() {
  for marker in MERGE_HEAD REBASE_HEAD CHERRY_PICK_HEAD REVERT_HEAD BISECT_LOG; do
    [ ! -e "$SOURCE/.git/$marker" ] || return 0
  done
  [ ! -d "$SOURCE/.git/rebase-merge" ] && [ ! -d "$SOURCE/.git/rebase-apply" ] || return 0
  return 1
}

owned_mode_directory() {
  [ -d "$1" ] && [ ! -L "$1" ] &&
    [ "$(stat -c %U:%G "$1" 2>/dev/null)" = jazofv1:jazofv1 ] &&
    [ "$(stat -c %a "$1" 2>/dev/null)" = "$2" ]
}

owned_mode_file() {
  [ -f "$1" ] && [ ! -L "$1" ] &&
    [ "$(stat -c %U:%G "$1" 2>/dev/null)" = jazofv1:jazofv1 ] &&
    [ "$(stat -c %a "$1" 2>/dev/null)" = "$2" ]
}

safe_owned_file() {
  [ -f "$1" ] && [ ! -L "$1" ] &&
    [ "$(stat -c %U:%G "$1" 2>/dev/null)" = jazofv1:jazofv1 ] || return 1
  file_mode="$(stat -c %a "$1" 2>/dev/null)" || return 1
  [ $((8#$file_mode & 0022)) -eq 0 ]
}

validate_database() {
  output="$(HIOC_HOME="$RUNTIME" python3 "$RUNTIME/$VALIDATOR_REL" database --database "$DB" --manifest "$MF" --json 2>/dev/null)"
  rc=$?
  [ "$rc" -eq 0 ] || return 1
  python3 -c 'import json,sys; d=json.loads(sys.argv[1]); raise SystemExit(0 if d.get("result")=="PASS" and d.get("privacy_safe") is True and d.get("record_count")==int(sys.argv[2]) else 1)' "$output" "$EXPECTED_DATABASE_RECORD_COUNT" >/dev/null 2>&1
}

validate_sidecar() {
  output="$(HIOC_HOME="$RUNTIME" python3 "$RUNTIME/$VALIDATOR_REL" sidecar --sidecar "$SIDE" --status "$STATUS" --inventory "$INVENTORY" --database "$DB" --manifest "$MF" --json 2>/dev/null)"
  rc=$?
  [ "$rc" -eq 0 ] || return 1
  python3 -c 'import json,sys; d=json.loads(sys.argv[1]); raise SystemExit(0 if d.get("result")=="PASS" and d.get("privacy_safe") is True and d.get("status")=="online" and isinstance(d.get("record_count"),int) else 1)' "$output" >/dev/null 2>&1
}

configuration_value() {
  python3 - "$CONFIG" <<'PY'
import pathlib, sys
lines = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()
values = []
for line in lines:
    if line.startswith("MANUFACTURER_DB_PATH="):
        raw = line.split("=", 1)[1].strip()
        if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'": raw = raw[1:-1]
        values.append(raw)
if len(values) != 1: raise SystemExit(2)
print(values[0])
PY
}

verify_target_source_runtime() {
  [ "$(hostname -s 2>/dev/null)" = nutandpihole ] || { fail_action8 INPUT_OR_PRECONDITION_ERROR WRONG_TARGET TARGET_IDENTITY FALSE; return 1; }
  ip -o -4 addr show scope global 2>/dev/null | awk '{print $4}' | cut -d/ -f1 | grep -Fxq 192.168.100.252 || { fail_action8 INPUT_OR_PRECONDITION_ERROR WRONG_TARGET TARGET_IDENTITY FALSE; return 1; }
  [ "$(id -un 2>/dev/null)" = jazofv1 ] && [ "$(id -gn 2>/dev/null)" = jazofv1 ] || { fail_action8 INPUT_OR_PRECONDITION_ERROR WRONG_OPERATOR TARGET_IDENTITY FALSE; return 1; }
  printf 'TARGET_IDENTITY=PASS\n'
  [ -d "$SOURCE/.git" ] || { fail_action8 INPUT_OR_PRECONDITION_ERROR SOURCE_REPOSITORY_MISSING SOURCE_IDENTITY FALSE; return 1; }
  [ "$(git -C "$SOURCE" branch --show-current 2>/dev/null)" = main ] || { fail_action8 INPUT_OR_PRECONDITION_ERROR SOURCE_IDENTITY_MISMATCH SOURCE_IDENTITY FALSE; return 1; }
  [ "$(git -C "$SOURCE" rev-parse HEAD 2>/dev/null)" = "$GOVERNANCE_COMMIT" ] && [ "$(git -C "$SOURCE" rev-parse origin/main 2>/dev/null)" = "$GOVERNANCE_COMMIT" ] || { fail_action8 INPUT_OR_PRECONDITION_ERROR SOURCE_IDENTITY_MISMATCH SOURCE_IDENTITY FALSE; return 1; }
  [ -z "$(git -C "$SOURCE" status --porcelain 2>/dev/null)" ] || { fail_action8 INPUT_OR_PRECONDITION_ERROR SOURCE_IDENTITY_MISMATCH SOURCE_IDENTITY FALSE; return 1; }
  active_git_operation && { fail_action8 INPUT_OR_PRECONDITION_ERROR ACTIVE_GIT_OPERATION SOURCE_IDENTITY FALSE; return 1; }
  for rel in "$SCRIPT_REL" "$GENERATOR_REL" "$VALIDATOR_REL" "$LIBRARY_REL"; do
    [ -f "$SOURCE/$rel" ] && [ ! -L "$SOURCE/$rel" ] || { fail_action8 INPUT_OR_PRECONDITION_ERROR GOVERNED_ARTIFACT_IDENTITY_MISMATCH SOURCE_IDENTITY FALSE; return 1; }
    expected="$(git -C "$SOURCE" rev-parse "$GOVERNANCE_COMMIT:$rel" 2>/dev/null)" || { fail_action8 INPUT_OR_PRECONDITION_ERROR GOVERNED_ARTIFACT_IDENTITY_MISMATCH SOURCE_IDENTITY FALSE; return 1; }
    actual="$(git -C "$SOURCE" hash-object --path="$rel" "$SOURCE/$rel" 2>/dev/null)" || { fail_action8 INPUT_OR_PRECONDITION_ERROR GOVERNED_ARTIFACT_IDENTITY_MISMATCH SOURCE_IDENTITY FALSE; return 1; }
    [ "$actual" = "$expected" ] && git -C "$SOURCE" diff --quiet -- "$rel" || { fail_action8 INPUT_OR_PRECONDITION_ERROR GOVERNED_ARTIFACT_IDENTITY_MISMATCH SOURCE_IDENTITY FALSE; return 1; }
  done
  printf 'SOURCE_IDENTITY=PASS\n'
  [ -d "$RUNTIME" ] && [ ! -L "$RUNTIME" ] || { fail_action8 INPUT_OR_PRECONDITION_ERROR RUNTIME_ROOT_INVALID RUNTIME_IDENTITY FALSE; return 1; }
  for rel in "$GENERATOR_REL" "$VALIDATOR_REL" "$LIBRARY_REL"; do
    [ -f "$RUNTIME/$rel" ] && [ ! -L "$RUNTIME/$rel" ] && [ "$(sha256sum "$RUNTIME/$rel" 2>/dev/null | awk '{print $1}')" = "$(sha256sum "$SOURCE/$rel" 2>/dev/null | awk '{print $1}')" ] || { fail_action8 INPUT_OR_PRECONDITION_ERROR RUNTIME_ARTIFACT_IDENTITY_MISMATCH RUNTIME_IDENTITY FALSE; return 1; }
  done
  printf 'RUNTIME_IDENTITY=PASS\n'
}

prepare_evidence_directory() {
  EVIDENCE_DIR="$(mktemp -d /tmp/hioc-pe3-action8-XXXXXXXX 2>/dev/null)" || { fail_action8 VALIDATION_FAIL EVIDENCE_DIRECTORY_CREATE_FAILED EVIDENCE_PREPARATION FALSE; return 1; }
  case "$EVIDENCE_DIR" in /tmp/hioc-pe3-action8-*) ;; *) fail_action8 VALIDATION_FAIL EVIDENCE_DIRECTORY_INVALID EVIDENCE_PREPARATION FALSE; return 1 ;; esac
  [ "$(dirname -- "$EVIDENCE_DIR")" = /tmp ] || { fail_action8 VALIDATION_FAIL EVIDENCE_DIRECTORY_INVALID EVIDENCE_PREPARATION FALSE; return 1; }
  chmod 0700 "$EVIDENCE_DIR" >/dev/null 2>&1 && owned_mode_directory "$EVIDENCE_DIR" 700 || { fail_action8 VALIDATION_FAIL EVIDENCE_DIRECTORY_INVALID EVIDENCE_PREPARATION FALSE; return 1; }
  EVIDENCE_DIR_CREATED=TRUE
  install -d -m 0700 -- "$EVIDENCE_DIR/pre" >/dev/null 2>&1 && owned_mode_directory "$EVIDENCE_DIR/pre" 700 || { fail_action8 VALIDATION_FAIL EVIDENCE_PRE_DIRECTORY_CREATE_FAILED EVIDENCE_PREPARATION FALSE; return 1; }
  printf 'EVIDENCE_PRECONDITION=PASS\n'
}

verify_configuration_dataset_inventory() {
  owned_mode_file "$CONFIG" 600 && bash -n "$CONFIG" >/dev/null 2>&1 || { fail_action8 INPUT_OR_PRECONDITION_ERROR CONFIGURATION_IDENTITY_INVALID CONFIGURATION_IDENTITY FALSE; return 1; }
  selected="$(configuration_value 2>/dev/null)"; rc=$?
  [ "$rc" -eq 0 ] && [ "$selected" = "$DB" ] || { fail_action8 INPUT_OR_PRECONDITION_ERROR CONFIGURATION_SELECTION_MISMATCH CONFIGURATION_IDENTITY FALSE; return 1; }
  CONFIG_SHA_BEFORE="$(sha256sum "$CONFIG" | awk '{print $1}')"
  printf 'CONFIGURATION_IDENTITY=PASS\n'
  owned_mode_directory "$FINAL_DIR" 700 && owned_mode_file "$DB" 600 && owned_mode_file "$MF" 600 || { fail_action8 INPUT_OR_PRECONDITION_ERROR DATASET_IDENTITY_INVALID DATASET_IDENTITY FALSE; return 1; }
  [ "$(find "$FINAL_DIR" -mindepth 1 -maxdepth 1 -printf '%f\n' 2>/dev/null | sort | paste -sd, -)" = manufacturer-db.json,manufacturer-db.manifest.json ] || { fail_action8 INPUT_OR_PRECONDITION_ERROR DATASET_CONTENTS_INVALID DATASET_IDENTITY FALSE; return 1; }
  [ "$(stat -c %s "$DB")" = "$DB_BYTES" ] && [ "$(stat -c %s "$MF")" = "$MF_BYTES" ] && [ "$(sha256sum "$DB" | awk '{print $1}')" = "$DB_SHA256" ] && [ "$(sha256sum "$MF" | awk '{print $1}')" = "$MF_SHA256" ] || { fail_action8 INPUT_OR_PRECONDITION_ERROR DATASET_IDENTITY_MISMATCH DATASET_IDENTITY FALSE; return 1; }
  printf 'DATASET_IDENTITY=PASS\n'
  validate_database || { fail_action8 VALIDATION_FAIL DATASET_VALIDATOR_FAILED DATASET_VALIDATION FALSE; return 1; }
  printf 'DATASET_VALIDATION=PASS\n'
  safe_owned_file "$INVENTORY" || { fail_action8 INPUT_OR_PRECONDITION_ERROR INVENTORY_IDENTITY_INVALID INVENTORY_IDENTITY FALSE; return 1; }
  python3 -c 'import json,sys; d=json.load(open(sys.argv[1],encoding="utf-8")); raise SystemExit(0 if isinstance(d,dict) and isinstance(d.get("devices"),list) else 1)' "$INVENTORY" >/dev/null 2>&1 || { fail_action8 INPUT_OR_PRECONDITION_ERROR INVENTORY_INVALID INVENTORY_IDENTITY FALSE; return 1; }
  printf 'INVENTORY_IDENTITY=PASS\n'
}

verify_transport_and_output_prestate() {
  owned_mode_directory "$TRANSPORT_STAGE" 700 || { fail_action8 INPUT_OR_PRECONDITION_ERROR TRANSPORT_STAGING_INVALID PROTECTED_PRE_STATE FALSE; return 1; }
  [ "$(find "$TRANSPORT_STAGE" -mindepth 1 -maxdepth 1 -printf '%f\n' 2>/dev/null | sort | paste -sd, -)" = manufacturer-db.json,manufacturer-db.manifest.json ] || { fail_action8 INPUT_OR_PRECONDITION_ERROR TRANSPORT_STAGING_INVALID PROTECTED_PRE_STATE FALSE; return 1; }
  TRANSPORT_SHA_BEFORE="$(sha256sum "$TRANSPORT_STAGE/manufacturer-db.json" "$TRANSPORT_STAGE/manufacturer-db.manifest.json" 2>/dev/null | sha256sum | awk '{print $1}')"
  side_exists=FALSE
  if [ -e "$SIDE" ] || [ -L "$SIDE" ] || [ -e "$STATUS" ] || [ -L "$STATUS" ]; then
    owned_mode_file "$SIDE" 600 && owned_mode_file "$STATUS" 600 || { fail_action8 INPUT_OR_PRECONDITION_ERROR MANUFACTURER_OUTPUT_PRECONDITION_INVALID OUTPUT_PRECONDITION FALSE; return 1; }
    validate_sidecar || { fail_action8 INPUT_OR_PRECONDITION_ERROR EXISTING_MANUFACTURER_OUTPUT_INVALID OUTPUT_PRECONDITION FALSE; return 1; }
    side_exists=TRUE
  fi
  printf 'OUTPUT_PRECONDITION=PASS\n'
}

write_protected_snapshot() {
  snapshot="$EVIDENCE_DIR/pre/protected.json"
  [ ! -e "$snapshot" ] && [ ! -L "$snapshot" ] || { fail_action8 INPUT_OR_PRECONDITION_ERROR ACTION8_EVIDENCE_ALREADY_EXISTS PROTECTED_PRE_STATE FALSE; return 1; }
  python3 - "$RUNTIME" "$snapshot" <<'PY'
import hashlib, json, os, pathlib, sys
root, target = map(pathlib.Path, sys.argv[1:])
stable = ['state/inventory/inventory.json','state/inventory/devices.json','state/inventory/services.json','state/inventory/topology.json','state/inventory/dependencies.json','state/inventory/summary.json','state/inventory/status.json','state/inventory/enrichment.json','state/inventory/enrichment_status.json','state/inventory/assets.json','state/inventory/assets_status.json','state/platform/status.json']
live = ['state/incidents/active.json','state/incidents/history.json','state/incidents/summary.json','state/incident_engine_status.json']
def clean(v):
    if isinstance(v,dict): return {k:clean(x) for k,x in sorted(v.items()) if k not in {'updated','updated_at','generated_at','timestamp','last_seen','last_changed'}}
    if isinstance(v,list): return [clean(x) for x in v]
    return v
def item(rel, kind):
    p=root/rel
    if not p.exists(): return {'path':rel,'class':kind,'present':False}
    if p.is_symlink() or not p.is_file(): raise SystemExit(4)
    value=json.loads(p.read_text(encoding='utf-8')); raw=json.dumps(clean(value),sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
    return {'path':rel,'class':kind,'present':True,'semantic_sha256':hashlib.sha256(raw).hexdigest(),'top_level_count':len(value) if isinstance(value,(dict,list)) else None}
doc={'stable':[item(x,'stable') for x in stable],'operational_drift':[item(x,'live') for x in live]}
data=(json.dumps(doc,indent=2,sort_keys=True)+'\n').encode(); fd=os.open(target,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
with os.fdopen(fd,'wb') as handle: handle.write(data); handle.flush(); os.fsync(handle.fileno())
PY
  rc=$?
  [ "$rc" -eq 0 ] && owned_mode_file "$snapshot" 600 || { fail_action8 VALIDATION_FAIL PROTECTED_SNAPSHOT_FAILED PROTECTED_PRE_STATE FALSE; return 1; }
  sync -f "$snapshot" && sync -f "$EVIDENCE_DIR/pre" || { fail_action8 VALIDATION_FAIL PROTECTED_SNAPSHOT_FSYNC_FAILED PROTECTED_PRE_STATE FALSE; return 1; }
  printf 'PROTECTED_PRE_STATE=PASS\n'
}

run_generation() {
  TEMP_RESULT="$(mktemp "$EVIDENCE_DIR/.action8-result.XXXXXXXX" 2>/dev/null)" || { fail_action8 VALIDATION_FAIL EVIDENCE_TEMP_CREATE_FAILED MANUFACTURER_GENERATION FALSE; return 1; }
  TEMP_PERFORMANCE="$(mktemp "$EVIDENCE_DIR/.action8-performance.XXXXXXXX" 2>/dev/null)" || { fail_action8 VALIDATION_FAIL EVIDENCE_TEMP_CREATE_FAILED MANUFACTURER_GENERATION FALSE; return 1; }
  chmod 0600 "$TEMP_RESULT" "$TEMP_PERFORMANCE" || { fail_action8 VALIDATION_FAIL EVIDENCE_TEMP_PERMISSION_FAILED MANUFACTURER_GENERATION FALSE; return 1; }
  /usr/bin/time -f 'manufacturer_generation_elapsed_seconds=%e manufacturer_generation_max_rss_kib=%M' -o "$TEMP_PERFORMANCE" python3 "$RUNTIME/$GENERATOR_REL" --home "$RUNTIME" --json > "$TEMP_RESULT" 2>/dev/null
  generation_rc=$?
  [ "$generation_rc" -eq 0 ] || { fail_action8 VALIDATION_FAIL MANUFACTURER_GENERATOR_FAILED MANUFACTURER_GENERATION FALSE; return 1; }
  GENERATOR_SUCCEEDED=TRUE
  python3 - "$TEMP_RESULT" <<'PY'
import json, pathlib, sys
d=json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))
counts=[d.get(k) for k in ('record_count','matched_count','unknown_count','excluded_count','invalid_count')]
ok=d.get('result')=='PASS' and d.get('status')=='online' and all(type(x) is int and x>=0 for x in counts) and sum(counts[1:])==counts[0] and d.get('error') is None
raise SystemExit(0 if ok else 1)
PY
  [ "$?" -eq 0 ] || { fail_action8 VALIDATION_FAIL GENERATION_RESULT_INVALID MANUFACTURER_GENERATION TRUE; return 1; }
  printf 'MANUFACTURER_GENERATION=PASS\n'
}

validate_and_publish_evidence() {
  owned_mode_file "$SIDE" 600 && owned_mode_file "$STATUS" 600 || { fail_action8 VALIDATION_FAIL MANUFACTURER_OUTPUT_IDENTITY_INVALID MANUFACTURER_ARTIFACT_IDENTITY TRUE; return 1; }
  [ -z "$(find "$STATE_DIR" -maxdepth 1 -type f \( -name '.manufacturer*.tmp' -o -name '.manufacturer_status*.tmp' \) -print -quit 2>/dev/null)" ] || { fail_action8 VALIDATION_FAIL MANUFACTURER_TEMP_ARTIFACT_PRESENT MANUFACTURER_ARTIFACT_IDENTITY TRUE; return 1; }
  printf 'MANUFACTURER_ARTIFACT_IDENTITY=PASS\n'
  validate_sidecar || { fail_action8 VALIDATION_FAIL MANUFACTURER_ARTIFACT_VALIDATION_FAILED MANUFACTURER_ARTIFACT_VALIDATION TRUE; return 1; }
  printf 'MANUFACTURER_ARTIFACT_VALIDATION=PASS\n'
  [ "$(sha256sum "$CONFIG" | awk '{print $1}')" = "$CONFIG_SHA_BEFORE" ] || { fail_action8 VALIDATION_FAIL CONFIGURATION_CHANGED PROTECTED_POST_GENERATION TRUE; return 1; }
  [ "$(sha256sum "$DB" | awk '{print $1}')" = "$DB_SHA256" ] && [ "$(sha256sum "$MF" | awk '{print $1}')" = "$MF_SHA256" ] || { fail_action8 VALIDATION_FAIL DATASET_CHANGED PROTECTED_POST_GENERATION TRUE; return 1; }
  [ "$(sha256sum "$TRANSPORT_STAGE/manufacturer-db.json" "$TRANSPORT_STAGE/manufacturer-db.manifest.json" 2>/dev/null | sha256sum | awk '{print $1}')" = "$TRANSPORT_SHA_BEFORE" ] || { fail_action8 VALIDATION_FAIL TRANSPORT_STAGING_CHANGED PROTECTED_POST_GENERATION TRUE; return 1; }
  printf 'PROTECTED_POST_GENERATION=PASS\n'
  sync -f "$TEMP_RESULT" && sync -f "$TEMP_PERFORMANCE" || { fail_action8 VALIDATION_FAIL EVIDENCE_FSYNC_FAILED EVIDENCE_PUBLICATION TRUE; return 1; }
  mv -fT -- "$TEMP_PERFORMANCE" "$EVIDENCE_DIR/generation-performance.txt" || { fail_action8 VALIDATION_FAIL EVIDENCE_PUBLICATION_FAILED EVIDENCE_PUBLICATION TRUE; return 1; }
  TEMP_PERFORMANCE=
  mv -fT -- "$TEMP_RESULT" "$EVIDENCE_DIR/generation-result.json" || { fail_action8 VALIDATION_FAIL EVIDENCE_PUBLICATION_FAILED EVIDENCE_PUBLICATION TRUE; return 1; }
  TEMP_RESULT=
  sync -f "$EVIDENCE_DIR/generation-result.json" && sync -f "$EVIDENCE_DIR/generation-performance.txt" && sync -f "$EVIDENCE_DIR" || { fail_action8 VALIDATION_FAIL EVIDENCE_FSYNC_FAILED EVIDENCE_PUBLICATION TRUE; return 1; }
  printf 'EVIDENCE_PUBLICATION=PASS\nEVIDENCE_REPORT=PASS\nEVIDENCE_DIR=%s\nACTION8=COMPLETE\nRESULT=PASS\nROLLBACK_RECOMMENDED=FALSE\n' "$EVIDENCE_DIR"
}

main() {
  FAILURE_REPORTED=0
  GOVERNANCE_COMMIT=
  EVIDENCE_DIR=
  EVIDENCE_DIR_CREATED=FALSE
  [ "$#" -eq 2 ] && [ "$1" = --governance-commit ] || { fail_action8 INPUT_OR_PRECONDITION_ERROR INVALID_ARGUMENTS INPUT_VALIDATION FALSE; return 1; }
  GOVERNANCE_COMMIT=$2
  printf '%s' "$GOVERNANCE_COMMIT" | grep -Eq '^[0-9a-f]{40}$' || { fail_action8 INPUT_OR_PRECONDITION_ERROR INVALID_GOVERNANCE_COMMIT INPUT_VALIDATION FALSE; return 1; }
  verify_target_source_runtime || return 1
  verify_configuration_dataset_inventory || return 1
  verify_transport_and_output_prestate || return 1
  prepare_evidence_directory || return 1
  write_protected_snapshot || return 1
  run_generation || return 1
  validate_and_publish_evidence || return 1
}

action8_entry() {
  main "$@"
  action8_rc=$?
  if [ "$action8_rc" -ne 0 ] && [ "${FAILURE_REPORTED:-0}" -ne 1 ]; then
    fail_action8 VALIDATION_FAIL ACTION8_UNEXPECTED_ERROR ACTION8_UNEXPECTED "$GENERATOR_SUCCEEDED"
    action8_rc=$?
  fi
  return "$action8_rc"
}

action8_entry "$@"
