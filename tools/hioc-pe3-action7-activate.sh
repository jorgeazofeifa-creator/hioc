#!/usr/bin/env bash

# Governed PE-3 Production Action 7: manufacturer configuration activation.

SOURCE=/home/jazofv1/hioc-release-source
RUNTIME=/home/jazofv1/hioc
SCRIPT_PATH=tools/hioc-pe3-action7-activate.sh
VALIDATOR_REL=pi4/bin/hioc-validate-manufacturer.py
GENERATOR_REL=pi4/bin/hioc-generate-manufacturer.py
CONFIG="$RUNTIME/config/hioc.conf"
CONFIG_DIR="$RUNTIME/config"
BACKUP_DIR="$RUNTIME/backups/config"
FINAL_DIR="$RUNTIME/data/manufacturer/versions/local-ieee-ra--2026-08-11-r1"
FINAL_DB="$FINAL_DIR/manufacturer-db.json"
FINAL_MF="$FINAL_DIR/manufacturer-db.manifest.json"
DB_BYTES=8652642
MF_BYTES=1338
DB_SHA256=81f147cc57768c5797c4ad73a8c0369001bbdcbfe1548e71d3702c8c7f81e0e1
MF_SHA256=10c8097c0a4ec6e8cc4cd3dc61afc7f368057f4ef4b6534df9f6dd31634a4ac4
EXPECTED_RECORD_COUNT=53581
CONFIG_TEMP=
CONFIG_BACKUP=
CONFIG_PUBLISHED=FALSE

cleanup_temp() {
  [ -n "$CONFIG_TEMP" ] || return 0
  case "$CONFIG_TEMP" in "$CONFIG_DIR"/.hioc.conf.action7.*) ;; *) return 1 ;; esac
  [ -e "$CONFIG_TEMP" ] || [ -L "$CONFIG_TEMP" ] || { CONFIG_TEMP=; return 0; }
  [ -f "$CONFIG_TEMP" ] && [ ! -L "$CONFIG_TEMP" ] || return 1
  rm -- "$CONFIG_TEMP" >/dev/null 2>&1 || return 1
  CONFIG_TEMP=
}

fail_action7() {
  FAILURE_REPORTED=1
  result=$1
  code=$2
  stage=$3
  rollback=$4
  if ! cleanup_temp; then
    printf 'RESULT=VALIDATION_FAIL\nERROR_CODE=CONFIGURATION_TEMP_CLEANUP_FAILED\nFAILURE_STAGE=CONFIGURATION_CLEANUP\nROLLBACK_RECOMMENDED=%s\n' "$rollback"
    return 1
  fi
  printf 'RESULT=%s\nERROR_CODE=%s\nFAILURE_STAGE=%s\nROLLBACK_RECOMMENDED=%s\n' "$result" "$code" "$stage" "$rollback"
  [ -z "$CONFIG_BACKUP" ] || printf 'CONFIGURATION_BACKUP_PATH=%s\n' "$CONFIG_BACKUP"
  return 1
}

active_git_operation() {
  for marker in MERGE_HEAD REBASE_HEAD CHERRY_PICK_HEAD REVERT_HEAD BISECT_LOG; do
    [ ! -e "$SOURCE/.git/$marker" ] || return 0
  done
  [ ! -d "$SOURCE/.git/rebase-merge" ] && [ ! -d "$SOURCE/.git/rebase-apply" ] || return 0
  return 1
}

real_owned_directory() {
  [ -d "$1" ] && [ ! -L "$1" ] &&
    [ "$(stat -c %U:%G "$1" 2>/dev/null)" = jazofv1:jazofv1 ] &&
    [ "$(stat -c %a "$1" 2>/dev/null)" = 700 ]
}

real_owned_file() {
  [ -f "$1" ] && [ ! -L "$1" ] &&
    [ "$(stat -c %U:%G "$1" 2>/dev/null)" = jazofv1:jazofv1 ] &&
    [ "$(stat -c %a "$1" 2>/dev/null)" = 600 ]
}

safe_owned_directory() {
  [ -d "$1" ] && [ ! -L "$1" ] &&
    [ "$(stat -c %U:%G "$1" 2>/dev/null)" = jazofv1:jazofv1 ] || return 1
  mode="$(stat -c %a "$1" 2>/dev/null)" || return 1
  [ $((8#$mode & 0022)) -eq 0 ]
}

safe_owned_config() {
  [ -f "$CONFIG" ] && [ ! -L "$CONFIG" ] &&
    [ "$(stat -c %U:%G "$CONFIG" 2>/dev/null)" = jazofv1:jazofv1 ] || return 1
  mode="$(stat -c %a "$CONFIG" 2>/dev/null)" || return 1
  [ $((8#$mode & 0022)) -eq 0 ]
}

validate_dataset() {
  output="$(HIOC_HOME="$RUNTIME" python3 "$RUNTIME/$VALIDATOR_REL" database --database "$FINAL_DB" --manifest "$FINAL_MF" --json 2>/dev/null)"
  status=$?
  [ "$status" -eq 0 ] || return 1
  python3 -c 'import json,sys; d=json.loads(sys.argv[1]); raise SystemExit(0 if d.get("result")=="PASS" and d.get("privacy_safe") is True and d.get("record_count")==int(sys.argv[2]) else 1)' "$output" "$EXPECTED_RECORD_COUNT" >/dev/null 2>&1
}

configuration_value() {
  python3 - "$CONFIG" <<'PY'
import pathlib, sys
p = pathlib.Path(sys.argv[1])
try:
    lines = p.read_text(encoding="utf-8").splitlines()
except (OSError, UnicodeError):
    raise SystemExit(3)
values = []
for line in lines:
    if line.startswith("MANUFACTURER_DB_PATH="):
        raw = line.split("=", 1)[1].strip()
        if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'":
            raw = raw[1:-1]
        values.append(raw)
if len(values) > 1:
    raise SystemExit(2)
print(values[0] if values else "")
PY
}

verify_source_runtime() {
  [ "$(hostname -s 2>/dev/null)" = nutandpihole ] || { fail_action7 INPUT_OR_PRECONDITION_ERROR WRONG_TARGET TARGET_IDENTITY FALSE; return 1; }
  ip -o -4 addr show scope global 2>/dev/null | awk '{print $4}' | cut -d/ -f1 | grep -Fxq 192.168.100.252 || { fail_action7 INPUT_OR_PRECONDITION_ERROR WRONG_TARGET TARGET_IDENTITY FALSE; return 1; }
  printf 'TARGET_IDENTITY=PASS\n'
  [ -d "$SOURCE/.git" ] || { fail_action7 INPUT_OR_PRECONDITION_ERROR SOURCE_REPOSITORY_MISSING SOURCE_IDENTITY FALSE; return 1; }
  [ "$(git -C "$SOURCE" branch --show-current 2>/dev/null)" = main ] || { fail_action7 INPUT_OR_PRECONDITION_ERROR SOURCE_IDENTITY_MISMATCH SOURCE_IDENTITY FALSE; return 1; }
  [ "$(git -C "$SOURCE" rev-parse HEAD 2>/dev/null)" = "$GOVERNANCE_COMMIT" ] &&
    [ "$(git -C "$SOURCE" rev-parse origin/main 2>/dev/null)" = "$GOVERNANCE_COMMIT" ] || { fail_action7 INPUT_OR_PRECONDITION_ERROR SOURCE_IDENTITY_MISMATCH SOURCE_IDENTITY FALSE; return 1; }
  [ -z "$(git -C "$SOURCE" status --porcelain 2>/dev/null)" ] || { fail_action7 INPUT_OR_PRECONDITION_ERROR SOURCE_IDENTITY_MISMATCH SOURCE_IDENTITY FALSE; return 1; }
  active_git_operation && { fail_action7 INPUT_OR_PRECONDITION_ERROR ACTIVE_GIT_OPERATION SOURCE_IDENTITY FALSE; return 1; }
  for rel in "$SCRIPT_PATH" "$VALIDATOR_REL" "$GENERATOR_REL"; do
    [ -f "$SOURCE/$rel" ] && [ ! -L "$SOURCE/$rel" ] || { fail_action7 INPUT_OR_PRECONDITION_ERROR GOVERNED_ARTIFACT_IDENTITY_MISMATCH SOURCE_IDENTITY FALSE; return 1; }
    expected="$(git -C "$SOURCE" rev-parse "$GOVERNANCE_COMMIT:$rel" 2>/dev/null)" || { fail_action7 INPUT_OR_PRECONDITION_ERROR GOVERNED_ARTIFACT_IDENTITY_MISMATCH SOURCE_IDENTITY FALSE; return 1; }
    actual="$(git -C "$SOURCE" hash-object --path="$rel" "$SOURCE/$rel" 2>/dev/null)" || { fail_action7 INPUT_OR_PRECONDITION_ERROR GOVERNED_ARTIFACT_IDENTITY_MISMATCH SOURCE_IDENTITY FALSE; return 1; }
    [ "$actual" = "$expected" ] && git -C "$SOURCE" diff --quiet -- "$rel" || { fail_action7 INPUT_OR_PRECONDITION_ERROR GOVERNED_ARTIFACT_IDENTITY_MISMATCH SOURCE_IDENTITY FALSE; return 1; }
  done
  printf 'SOURCE_IDENTITY=PASS\n'
  [ -d "$RUNTIME" ] && [ ! -L "$RUNTIME" ] && safe_owned_directory "$CONFIG_DIR" || { fail_action7 INPUT_OR_PRECONDITION_ERROR RUNTIME_ROOT_INVALID RUNTIME_IDENTITY FALSE; return 1; }
  for rel in "$VALIDATOR_REL" "$GENERATOR_REL"; do
    [ -f "$RUNTIME/$rel" ] && [ ! -L "$RUNTIME/$rel" ] &&
      [ "$(sha256sum "$RUNTIME/$rel" 2>/dev/null | awk '{print $1}')" = "$(sha256sum "$SOURCE/$rel" 2>/dev/null | awk '{print $1}')" ] || { fail_action7 INPUT_OR_PRECONDITION_ERROR RUNTIME_ARTIFACT_IDENTITY_MISMATCH RUNTIME_IDENTITY FALSE; return 1; }
  done
  printf 'RUNTIME_IDENTITY=PASS\n'
}

verify_dataset() {
  real_owned_directory "$FINAL_DIR" || { fail_action7 INPUT_OR_PRECONDITION_ERROR DATASET_DIRECTORY_INVALID DATASET_IDENTITY FALSE; return 1; }
  [ "$(find "$FINAL_DIR" -mindepth 1 -maxdepth 1 -printf '%f\n' 2>/dev/null | sort | paste -sd, -)" = manufacturer-db.json,manufacturer-db.manifest.json ] || { fail_action7 INPUT_OR_PRECONDITION_ERROR DATASET_CONTENTS_INVALID DATASET_IDENTITY FALSE; return 1; }
  real_owned_file "$FINAL_DB" && real_owned_file "$FINAL_MF" || { fail_action7 INPUT_OR_PRECONDITION_ERROR DATASET_FILE_IDENTITY_INVALID DATASET_IDENTITY FALSE; return 1; }
  [ "$(stat -c %s "$FINAL_DB" 2>/dev/null)" = "$DB_BYTES" ] && [ "$(stat -c %s "$FINAL_MF" 2>/dev/null)" = "$MF_BYTES" ] || { fail_action7 INPUT_OR_PRECONDITION_ERROR DATASET_SIZE_MISMATCH DATASET_IDENTITY FALSE; return 1; }
  [ "$(sha256sum "$FINAL_DB" 2>/dev/null | awk '{print $1}')" = "$DB_SHA256" ] && [ "$(sha256sum "$FINAL_MF" 2>/dev/null | awk '{print $1}')" = "$MF_SHA256" ] || { fail_action7 INPUT_OR_PRECONDITION_ERROR DATASET_HASH_MISMATCH DATASET_IDENTITY FALSE; return 1; }
  printf 'DATASET_IDENTITY=PASS\n'
  validate_dataset || { fail_action7 VALIDATION_FAIL DATASET_VALIDATOR_FAILED DATASET_VALIDATION FALSE; return 1; }
  printf 'DATASET_VALIDATION=PASS\n'
}

verify_configuration_precondition() {
  safe_owned_config || { fail_action7 INPUT_OR_PRECONDITION_ERROR CONFIGURATION_IDENTITY_INVALID CONFIGURATION_PRECONDITION FALSE; return 1; }
  CONFIG_SHA256_BEFORE="$(sha256sum "$CONFIG" 2>/dev/null | awk '{print $1}')"
  [ -n "$CONFIG_SHA256_BEFORE" ] || { fail_action7 INPUT_OR_PRECONDITION_ERROR CONFIGURATION_IDENTITY_INVALID CONFIGURATION_PRECONDITION FALSE; return 1; }
  bash -n "$CONFIG" >/dev/null 2>&1 || { fail_action7 INPUT_OR_PRECONDITION_ERROR CONFIGURATION_SYNTAX_INVALID CONFIGURATION_PRECONDITION FALSE; return 1; }
  CURRENT_VALUE="$(configuration_value 2>/dev/null)"
  parse_status=$?
  [ "$parse_status" -ne 2 ] || { fail_action7 INPUT_OR_PRECONDITION_ERROR CONFIGURATION_DUPLICATE_KEY CONFIGURATION_PRECONDITION FALSE; return 1; }
  [ "$parse_status" -eq 0 ] || { fail_action7 INPUT_OR_PRECONDITION_ERROR CONFIGURATION_PARSE_FAILED CONFIGURATION_PRECONDITION FALSE; return 1; }
  [ -z "$CURRENT_VALUE" ] || [ "$CURRENT_VALUE" = "$FINAL_DB" ] || { fail_action7 INPUT_OR_PRECONDITION_ERROR CONFIGURATION_DIFFERENT_VALUE CONFIGURATION_PRECONDITION FALSE; return 1; }
  NEEDS_MUTATION=TRUE
  [ "$CURRENT_VALUE" = "$FINAL_DB" ] && [ "$(stat -c %a "$CONFIG" 2>/dev/null)" = 600 ] && NEEDS_MUTATION=FALSE
  printf 'CONFIGURATION_PRECONDITION=PASS\n'
}

create_backup() {
  if [ "$NEEDS_MUTATION" = FALSE ]; then
    printf 'CONFIGURATION_BACKUP=PASS_NOT_REQUIRED\n'
    return 0
  fi
  if [ ! -e "$BACKUP_DIR" ]; then
    install -d -o jazofv1 -g jazofv1 -m 0700 -- "$BACKUP_DIR" || { fail_action7 VALIDATION_FAIL CONFIGURATION_BACKUP_DIRECTORY_FAILED CONFIGURATION_BACKUP FALSE; return 1; }
  fi
  real_owned_directory "$BACKUP_DIR" || { fail_action7 INPUT_OR_PRECONDITION_ERROR CONFIGURATION_BACKUP_DIRECTORY_INVALID CONFIGURATION_BACKUP FALSE; return 1; }
  CONFIG_BACKUP="$(mktemp "$BACKUP_DIR/hioc.conf.pre-pe3-action7.XXXXXXXX" 2>/dev/null)" || { fail_action7 VALIDATION_FAIL CONFIGURATION_BACKUP_CREATE_FAILED CONFIGURATION_BACKUP FALSE; return 1; }
  install -o jazofv1 -g jazofv1 -m 0600 -- "$CONFIG" "$CONFIG_BACKUP" || { fail_action7 VALIDATION_FAIL CONFIGURATION_BACKUP_COPY_FAILED CONFIGURATION_BACKUP FALSE; return 1; }
  [ "$(sha256sum "$CONFIG_BACKUP" 2>/dev/null | awk '{print $1}')" = "$CONFIG_SHA256_BEFORE" ] || { fail_action7 VALIDATION_FAIL CONFIGURATION_BACKUP_IDENTITY_FAILED CONFIGURATION_BACKUP FALSE; return 1; }
  sync -f "$CONFIG_BACKUP" && sync -f "$BACKUP_DIR" || { fail_action7 VALIDATION_FAIL CONFIGURATION_BACKUP_FSYNC_FAILED CONFIGURATION_BACKUP FALSE; return 1; }
  printf 'CONFIGURATION_BACKUP=PASS_CREATED\nCONFIGURATION_BACKUP_PATH=%s\n' "$CONFIG_BACKUP"
}

publish_configuration() {
  if [ "$NEEDS_MUTATION" = FALSE ]; then
    printf 'CONFIGURATION_ACTIVATION=PASS_ALREADY_ACTIVE\n'
    return 0
  fi
  CONFIG_TEMP="$(mktemp "$CONFIG_DIR/.hioc.conf.action7.XXXXXXXX" 2>/dev/null)" || { fail_action7 VALIDATION_FAIL CONFIGURATION_TEMP_CREATE_FAILED CONFIGURATION_ACTIVATION FALSE; return 1; }
  python3 - "$CONFIG" "$CONFIG_TEMP" "$FINAL_DB" <<'PY'
import os, pathlib, sys
source, target, value = map(pathlib.Path, sys.argv[1:])
lines = source.read_text(encoding="utf-8").splitlines()
out, found = [], False
for line in lines:
    if line.startswith("MANUFACTURER_DB_PATH="):
        if found:
            raise SystemExit(2)
        out.append(f'MANUFACTURER_DB_PATH="{value}"')
        found = True
    else:
        out.append(line)
if not found:
    out.append(f'MANUFACTURER_DB_PATH="{value}"')
data = ("\n".join(out) + "\n").encode("utf-8")
with target.open("wb") as handle:
    handle.write(data)
    handle.flush()
    os.fsync(handle.fileno())
PY
  build_status=$?
  [ "$build_status" -eq 0 ] || { fail_action7 VALIDATION_FAIL CONFIGURATION_BUILD_FAILED CONFIGURATION_ACTIVATION FALSE; return 1; }
  chown jazofv1:jazofv1 "$CONFIG_TEMP" && chmod 0600 "$CONFIG_TEMP" || { fail_action7 VALIDATION_FAIL CONFIGURATION_TEMP_PERMISSION_FAILED CONFIGURATION_ACTIVATION FALSE; return 1; }
  real_owned_file "$CONFIG_TEMP" && bash -n "$CONFIG_TEMP" >/dev/null 2>&1 || { fail_action7 VALIDATION_FAIL CONFIGURATION_TEMP_VALIDATION_FAILED CONFIGURATION_ACTIVATION FALSE; return 1; }
  sync -f "$CONFIG_TEMP" || { fail_action7 VALIDATION_FAIL CONFIGURATION_TEMP_FSYNC_FAILED CONFIGURATION_ACTIVATION FALSE; return 1; }
  mv -fT -- "$CONFIG_TEMP" "$CONFIG" || { fail_action7 VALIDATION_FAIL CONFIGURATION_ATOMIC_REPLACE_FAILED CONFIGURATION_ACTIVATION FALSE; return 1; }
  CONFIG_TEMP=
  CONFIG_PUBLISHED=TRUE
  sync -f "$CONFIG" && sync -f "$CONFIG_DIR" || { fail_action7 VALIDATION_FAIL CONFIGURATION_FSYNC_FAILED CONFIGURATION_ACTIVATION TRUE; return 1; }
  if [ -z "$CURRENT_VALUE" ]; then
    printf 'CONFIGURATION_ACTIVATION=PASS_NEW\n'
  else
    printf 'CONFIGURATION_ACTIVATION=PASS_NORMALIZED\n'
  fi
}

post_validate() {
  real_owned_file "$CONFIG" || { fail_action7 VALIDATION_FAIL CONFIGURATION_POST_IDENTITY_FAILED CONFIGURATION_VALIDATION "$CONFIG_PUBLISHED"; return 1; }
  bash -n "$CONFIG" >/dev/null 2>&1 || { fail_action7 VALIDATION_FAIL CONFIGURATION_POST_SYNTAX_INVALID CONFIGURATION_VALIDATION "$CONFIG_PUBLISHED"; return 1; }
  value="$(configuration_value 2>/dev/null)"
  status=$?
  [ "$status" -eq 0 ] && [ "$value" = "$FINAL_DB" ] || { fail_action7 VALIDATION_FAIL CONFIGURATION_POST_VALUE_FAILED CONFIGURATION_VALIDATION "$CONFIG_PUBLISHED"; return 1; }
  [ "$(grep -c '^MANUFACTURER_DB_PATH=' "$CONFIG" 2>/dev/null)" = 1 ] || { fail_action7 VALIDATION_FAIL CONFIGURATION_POST_DUPLICATE_KEY CONFIGURATION_VALIDATION "$CONFIG_PUBLISHED"; return 1; }
  [ "$(sha256sum "$FINAL_DB" 2>/dev/null | awk '{print $1}')" = "$DB_SHA256" ] && [ "$(sha256sum "$FINAL_MF" 2>/dev/null | awk '{print $1}')" = "$MF_SHA256" ] || { fail_action7 VALIDATION_FAIL DATASET_CHANGED_AFTER_ACTIVATION POST_ACTIVATION_VALIDATION "$CONFIG_PUBLISHED"; return 1; }
  validate_dataset || { fail_action7 VALIDATION_FAIL DATASET_VALIDATOR_FAILED POST_ACTIVATION_VALIDATION "$CONFIG_PUBLISHED"; return 1; }
  printf 'CONFIGURATION_VALIDATION=PASS\nRUNTIME_DATASET_SELECTION=PASS\nPOST_ACTIVATION_VALIDATION=PASS\nACTION7=COMPLETE\nRESULT=PASS\n'
}

main() {
  FAILURE_REPORTED=0
  GOVERNANCE_COMMIT=
  CONFIG_SHA256_BEFORE=
  CURRENT_VALUE=
  NEEDS_MUTATION=TRUE
  [ "$#" -eq 2 ] && [ "$1" = --governance-commit ] || { fail_action7 INPUT_OR_PRECONDITION_ERROR INVALID_ARGUMENTS INPUT_VALIDATION FALSE; return 1; }
  GOVERNANCE_COMMIT=$2
  printf '%s' "$GOVERNANCE_COMMIT" | grep -Eq '^[0-9a-f]{40}$' || { fail_action7 INPUT_OR_PRECONDITION_ERROR INVALID_GOVERNANCE_COMMIT INPUT_VALIDATION FALSE; return 1; }
  verify_source_runtime || return 1
  verify_dataset || return 1
  verify_configuration_precondition || return 1
  create_backup || return 1
  publish_configuration || return 1
  post_validate || return 1
}

action7_entry() {
  main "$@"
  action7_status=$?
  if [ "$action7_status" -ne 0 ] && [ "${FAILURE_REPORTED:-0}" -ne 1 ]; then
    fail_action7 VALIDATION_FAIL ACTION7_UNEXPECTED_ERROR ACTION7_UNEXPECTED "$CONFIG_PUBLISHED"
    action7_status=$?
  fi
  return "$action7_status"
}

action7_entry "$@"
