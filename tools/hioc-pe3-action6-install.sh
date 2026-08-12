#!/usr/bin/env bash

# Governed PE-3 Production Action 6: immutable manufacturer dataset install.

SOURCE=/home/jazofv1/hioc-release-source
RUNTIME=/home/jazofv1/hioc
SCRIPT_PATH=tools/hioc-pe3-action6-install.sh
VALIDATOR_REL=pi4/bin/hioc-validate-manufacturer.py
PI3_STAGE=/tmp/hioc-pe3-dataset-transfer-PJ5qPbRS
DB_NAME=manufacturer-db.json
MF_NAME=manufacturer-db.manifest.json
DB_BYTES=8652642
MF_BYTES=1338
DB_SHA256=81f147cc57768c5797c4ad73a8c0369001bbdcbfe1548e71d3702c8c7f81e0e1
MF_SHA256=10c8097c0a4ec6e8cc4cd3dc61afc7f368057f4ef4b6534df9f6dd31634a4ac4
EXPECTED_RECORD_COUNT=53581
DATA_ROOT="$RUNTIME/data/manufacturer"
VERSIONS="$DATA_ROOT/versions"
FINAL_DIR="$VERSIONS/local-ieee-ra--2026-08-11-r1"
CONFIG="$RUNTIME/config/hioc.conf"
INSTALL_STAGE=

cleanup_install_stage() {
  [ -n "$INSTALL_STAGE" ] || return 0
  case "$INSTALL_STAGE" in "$DATA_ROOT"/.action6-install-*) ;; *) return 1 ;; esac
  [ -e "$INSTALL_STAGE" ] || [ -L "$INSTALL_STAGE" ] || { INSTALL_STAGE=; return 0; }
  [ -d "$INSTALL_STAGE" ] && [ ! -L "$INSTALL_STAGE" ] || return 1
  rm -r -- "$INSTALL_STAGE" >/dev/null 2>&1 || return 1
  INSTALL_STAGE=
  return 0
}

fail_action6() {
  FAILURE_REPORTED=1
  result=$1
  code=$2
  stage=$3
  if ! cleanup_install_stage; then
    printf 'RESULT=VALIDATION_FAIL\nERROR_CODE=INSTALLATION_STAGING_CLEANUP_FAILED\nFAILURE_STAGE=INSTALLATION_CLEANUP\nROLLBACK_RECOMMENDED=FALSE\n'
    return 1
  fi
  printf 'RESULT=%s\nERROR_CODE=%s\nFAILURE_STAGE=%s\nROLLBACK_RECOMMENDED=FALSE\n' "$result" "$code" "$stage"
  return 1
}

active_git_operation() {
  for marker in MERGE_HEAD REBASE_HEAD CHERRY_PICK_HEAD REVERT_HEAD BISECT_LOG; do
    [ ! -e "$SOURCE/.git/$marker" ] || return 0
  done
  [ ! -d "$SOURCE/.git/rebase-merge" ] && [ ! -d "$SOURCE/.git/rebase-apply" ] || return 0
  return 1
}

exact_entries() {
  [ "$(find "$1" -mindepth 1 -maxdepth 1 -printf '%f\n' 2>/dev/null | sort | paste -sd, -)" = "$DB_NAME,$MF_NAME" ]
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

pair_sizes_match() {
  [ "$(stat -c %s "$1/$DB_NAME" 2>/dev/null)" = "$DB_BYTES" ] &&
    [ "$(stat -c %s "$1/$MF_NAME" 2>/dev/null)" = "$MF_BYTES" ]
}

pair_hashes_match() {
  [ "$(sha256sum "$1/$DB_NAME" 2>/dev/null | awk '{print $1}')" = "$DB_SHA256" ] &&
    [ "$(sha256sum "$1/$MF_NAME" 2>/dev/null | awk '{print $1}')" = "$MF_SHA256" ]
}

pair_types_permissions_match() {
  real_owned_file "$1/$DB_NAME" && real_owned_file "$1/$MF_NAME"
}

no_csv() {
  ! find "$1" -type f -iname '*.csv' -print -quit 2>/dev/null | grep -q .
}

validate_pair() {
  validator_output="$(HIOC_HOME="$RUNTIME" python3 "$RUNTIME/$VALIDATOR_REL" database --database "$1/$DB_NAME" --manifest "$1/$MF_NAME" --json 2>/dev/null)"
  validator_status=$?
  [ "$validator_status" -eq 0 ] || return 1
  python3 -c 'import json,sys; d=json.loads(sys.argv[1]); raise SystemExit(0 if d.get("result")=="PASS" and d.get("privacy_safe") is True and d.get("record_count")==int(sys.argv[2]) else 1)' "$validator_output" "$EXPECTED_RECORD_COUNT" >/dev/null 2>&1
}

verify_target_source_runtime() {
  [ "$(hostname -s 2>/dev/null)" = nutandpihole ] || { fail_action6 INPUT_OR_PRECONDITION_ERROR WRONG_TARGET TARGET_IDENTITY; return 1; }
  ip -o -4 addr show scope global 2>/dev/null | awk '{print $4}' | cut -d/ -f1 | grep -Fxq 192.168.100.252 || { fail_action6 INPUT_OR_PRECONDITION_ERROR WRONG_TARGET TARGET_IDENTITY; return 1; }
  printf 'TARGET_IDENTITY=PASS\n'
  [ -d "$SOURCE/.git" ] || { fail_action6 INPUT_OR_PRECONDITION_ERROR SOURCE_REPOSITORY_MISSING SOURCE_IDENTITY; return 1; }
  [ "$(git -C "$SOURCE" branch --show-current 2>/dev/null)" = main ] || { fail_action6 INPUT_OR_PRECONDITION_ERROR SOURCE_IDENTITY_MISMATCH SOURCE_IDENTITY; return 1; }
  [ "$(git -C "$SOURCE" rev-parse HEAD 2>/dev/null)" = "$GOVERNANCE_COMMIT" ] &&
    [ "$(git -C "$SOURCE" rev-parse origin/main 2>/dev/null)" = "$GOVERNANCE_COMMIT" ] || { fail_action6 INPUT_OR_PRECONDITION_ERROR SOURCE_IDENTITY_MISMATCH SOURCE_IDENTITY; return 1; }
  [ -z "$(git -C "$SOURCE" status --porcelain 2>/dev/null)" ] || { fail_action6 INPUT_OR_PRECONDITION_ERROR SOURCE_IDENTITY_MISMATCH SOURCE_IDENTITY; return 1; }
  active_git_operation && { fail_action6 INPUT_OR_PRECONDITION_ERROR ACTIVE_GIT_OPERATION SOURCE_IDENTITY; return 1; }
  [ -f "$SOURCE/$SCRIPT_PATH" ] && [ ! -L "$SOURCE/$SCRIPT_PATH" ] || { fail_action6 INPUT_OR_PRECONDITION_ERROR ACTION6_SCRIPT_IDENTITY_MISMATCH SOURCE_IDENTITY; return 1; }
  expected_script_blob="$(git -C "$SOURCE" rev-parse "$GOVERNANCE_COMMIT:$SCRIPT_PATH" 2>/dev/null)" || { fail_action6 INPUT_OR_PRECONDITION_ERROR ACTION6_SCRIPT_IDENTITY_MISMATCH SOURCE_IDENTITY; return 1; }
  actual_script_blob="$(git -C "$SOURCE" hash-object --path="$SCRIPT_PATH" "$SOURCE/$SCRIPT_PATH" 2>/dev/null)" || { fail_action6 INPUT_OR_PRECONDITION_ERROR ACTION6_SCRIPT_IDENTITY_MISMATCH SOURCE_IDENTITY; return 1; }
  [ "$actual_script_blob" = "$expected_script_blob" ] && git -C "$SOURCE" diff --quiet -- "$SCRIPT_PATH" || { fail_action6 INPUT_OR_PRECONDITION_ERROR ACTION6_SCRIPT_IDENTITY_MISMATCH SOURCE_IDENTITY; return 1; }
  [ -f "$SOURCE/$VALIDATOR_REL" ] && [ ! -L "$SOURCE/$VALIDATOR_REL" ] || { fail_action6 INPUT_OR_PRECONDITION_ERROR VALIDATOR_IDENTITY_MISMATCH SOURCE_IDENTITY; return 1; }
  expected_validator_blob="$(git -C "$SOURCE" rev-parse "$GOVERNANCE_COMMIT:$VALIDATOR_REL" 2>/dev/null)" || { fail_action6 INPUT_OR_PRECONDITION_ERROR VALIDATOR_IDENTITY_MISMATCH SOURCE_IDENTITY; return 1; }
  [ "$(git -C "$SOURCE" hash-object --path="$VALIDATOR_REL" "$SOURCE/$VALIDATOR_REL" 2>/dev/null)" = "$expected_validator_blob" ] && git -C "$SOURCE" diff --quiet -- "$VALIDATOR_REL" || { fail_action6 INPUT_OR_PRECONDITION_ERROR VALIDATOR_IDENTITY_MISMATCH SOURCE_IDENTITY; return 1; }
  [ -d "$RUNTIME" ] && [ ! -L "$RUNTIME" ] || { fail_action6 INPUT_OR_PRECONDITION_ERROR RUNTIME_ROOT_INVALID RUNTIME_IDENTITY; return 1; }
  [ -f "$RUNTIME/$VALIDATOR_REL" ] && [ ! -L "$RUNTIME/$VALIDATOR_REL" ] &&
    [ "$(sha256sum "$RUNTIME/$VALIDATOR_REL" 2>/dev/null | awk '{print $1}')" = "$(sha256sum "$SOURCE/$VALIDATOR_REL" 2>/dev/null | awk '{print $1}')" ] || { fail_action6 INPUT_OR_PRECONDITION_ERROR VALIDATOR_IDENTITY_MISMATCH RUNTIME_IDENTITY; return 1; }
  real_owned_directory "$DATA_ROOT" && real_owned_directory "$VERSIONS" || { fail_action6 INPUT_OR_PRECONDITION_ERROR RUNTIME_ROOT_INVALID RUNTIME_IDENTITY; return 1; }
  [ -f "$CONFIG" ] && [ ! -L "$CONFIG" ] || { fail_action6 INPUT_OR_PRECONDITION_ERROR CONFIGURATION_IDENTITY_INVALID CONFIGURATION_PRECONDITION; return 1; }
  CONFIG_SHA256_BEFORE="$(sha256sum "$CONFIG" 2>/dev/null | awk '{print $1}')"
  [ -n "$CONFIG_SHA256_BEFORE" ] || { fail_action6 INPUT_OR_PRECONDITION_ERROR CONFIGURATION_IDENTITY_INVALID CONFIGURATION_PRECONDITION; return 1; }
  printf 'SOURCE_IDENTITY=PASS\n'
}

verify_transport_stage() {
  [ "$PI3_STAGE" = /tmp/hioc-pe3-dataset-transfer-PJ5qPbRS ] || { fail_action6 INPUT_OR_PRECONDITION_ERROR STAGING_PATH_MISMATCH STAGING_IDENTITY; return 1; }
  [ -e "$PI3_STAGE" ] || { fail_action6 INPUT_OR_PRECONDITION_ERROR STAGING_DIRECTORY_MISSING STAGING_IDENTITY; return 1; }
  [ -d "$PI3_STAGE" ] && [ ! -L "$PI3_STAGE" ] || { fail_action6 INPUT_OR_PRECONDITION_ERROR STAGING_TYPE_OR_SYMLINK_INVALID STAGING_IDENTITY; return 1; }
  real_owned_directory "$PI3_STAGE" || { fail_action6 INPUT_OR_PRECONDITION_ERROR STAGING_OWNER_OR_MODE_INVALID STAGING_IDENTITY; return 1; }
  exact_entries "$PI3_STAGE" || { fail_action6 INPUT_OR_PRECONDITION_ERROR STAGING_EXTRA_OR_MISSING_ENTRY STAGING_IDENTITY; return 1; }
  [ -f "$PI3_STAGE/$DB_NAME" ] && [ ! -L "$PI3_STAGE/$DB_NAME" ] && [ -f "$PI3_STAGE/$MF_NAME" ] && [ ! -L "$PI3_STAGE/$MF_NAME" ] || { fail_action6 INPUT_OR_PRECONDITION_ERROR STAGED_FILE_TYPE_INVALID STAGING_IDENTITY; return 1; }
  pair_types_permissions_match "$PI3_STAGE" || { fail_action6 INPUT_OR_PRECONDITION_ERROR STAGED_FILE_OWNER_OR_MODE_INVALID STAGING_IDENTITY; return 1; }
  pair_sizes_match "$PI3_STAGE" || { fail_action6 INPUT_OR_PRECONDITION_ERROR STAGED_SIZE_MISMATCH STAGING_IDENTITY; return 1; }
  pair_hashes_match "$PI3_STAGE" || { fail_action6 INPUT_OR_PRECONDITION_ERROR STAGED_HASH_MISMATCH STAGING_IDENTITY; return 1; }
  no_csv "$PI3_STAGE" || { fail_action6 INPUT_OR_PRECONDITION_ERROR STAGING_EXTRA_OR_MISSING_ENTRY STAGING_IDENTITY; return 1; }
  printf 'STAGING_IDENTITY=PASS\n'
  validate_pair "$PI3_STAGE" || { fail_action6 VALIDATION_FAIL STAGED_VALIDATOR_FAILED STAGING_VALIDATION; return 1; }
  printf 'STAGING_VALIDATION=PASS\n'
}

verify_final_identity() {
  [ -d "$FINAL_DIR" ] && [ ! -L "$FINAL_DIR" ] || return 1
  real_owned_directory "$FINAL_DIR" || return 1
  exact_entries "$FINAL_DIR" || return 1
  pair_types_permissions_match "$FINAL_DIR" || return 1
  pair_sizes_match "$FINAL_DIR" || return 1
  pair_hashes_match "$FINAL_DIR" || return 1
  no_csv "$FINAL_DIR" || return 1
  return 0
}

configuration_unchanged() {
  [ -f "$CONFIG" ] && [ ! -L "$CONFIG" ] &&
    [ "$(sha256sum "$CONFIG" 2>/dev/null | awk '{print $1}')" = "$CONFIG_SHA256_BEFORE" ]
}

accept_existing_or_prepare() {
  if [ -e "$FINAL_DIR" ] || [ -L "$FINAL_DIR" ]; then
    verify_final_identity || { fail_action6 INPUT_OR_PRECONDITION_ERROR IMMUTABLE_VERSION_CONFLICT FINAL_VERSION_PRECONDITION; return 1; }
    validate_pair "$FINAL_DIR" || { fail_action6 VALIDATION_FAIL FINAL_VALIDATOR_FAILED FINAL_DATASET_VALIDATION; return 1; }
    printf 'IMMUTABLE_INSTALLATION=PASS_ALREADY_IDENTICAL\nFINAL_DATASET_IDENTITY=PASS\nFINAL_DATASET_VALIDATION=PASS\n'
    configuration_unchanged || { fail_action6 VALIDATION_FAIL CONFIGURATION_CHANGED CONFIGURATION_PROTECTION; return 1; }
    printf 'CONFIGURATION_UNTOUCHED=PASS\nACTION6=COMPLETE\nRESULT=PASS\n'
    return 0
  fi
  INSTALL_STAGE="$(mktemp -d "$DATA_ROOT/.action6-install-XXXXXXXX" 2>/dev/null)" || { fail_action6 VALIDATION_FAIL INSTALLATION_STAGING_CREATE_FAILED INSTALLATION_PREPARATION; return 1; }
  [ -d "$INSTALL_STAGE" ] && [ ! -L "$INSTALL_STAGE" ] || { fail_action6 VALIDATION_FAIL INSTALLATION_STAGING_CREATE_FAILED INSTALLATION_PREPARATION; return 1; }
  chmod 0700 "$INSTALL_STAGE" && chown jazofv1:jazofv1 "$INSTALL_STAGE" || { fail_action6 VALIDATION_FAIL INSTALLATION_PERMISSION_FAILED INSTALLATION_PREPARATION; return 1; }
}

copy_validate_publish() {
  install -o jazofv1 -g jazofv1 -m 0600 -- "$PI3_STAGE/$DB_NAME" "$INSTALL_STAGE/$DB_NAME" || { fail_action6 VALIDATION_FAIL INSTALLATION_COPY_FAILED INSTALLATION_COPY; return 1; }
  install -o jazofv1 -g jazofv1 -m 0600 -- "$PI3_STAGE/$MF_NAME" "$INSTALL_STAGE/$MF_NAME" || { fail_action6 VALIDATION_FAIL INSTALLATION_COPY_FAILED INSTALLATION_COPY; return 1; }
  real_owned_directory "$INSTALL_STAGE" && exact_entries "$INSTALL_STAGE" && pair_types_permissions_match "$INSTALL_STAGE" && pair_sizes_match "$INSTALL_STAGE" && pair_hashes_match "$INSTALL_STAGE" && no_csv "$INSTALL_STAGE" || { fail_action6 VALIDATION_FAIL POST_COPY_IDENTITY_FAILED POST_COPY_IDENTITY; return 1; }
  validate_pair "$INSTALL_STAGE" || { fail_action6 VALIDATION_FAIL STAGED_VALIDATOR_FAILED POST_COPY_VALIDATION; return 1; }
  sync -f "$INSTALL_STAGE/$DB_NAME" && sync -f "$INSTALL_STAGE/$MF_NAME" && sync -f "$INSTALL_STAGE" && sync -f "$DATA_ROOT" && sync -f "$VERSIONS" || { fail_action6 VALIDATION_FAIL FSYNC_FAILED DURABLE_PUBLICATION; return 1; }
  python3 - "$INSTALL_STAGE" "$FINAL_DIR" <<'PY'
import ctypes, errno, os, sys
libc = ctypes.CDLL(None, use_errno=True)
renameat2 = getattr(libc, "renameat2", None)
if renameat2 is None:
    raise SystemExit(2)
renameat2.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
rc = renameat2(-100, os.fsencode(sys.argv[1]), -100, os.fsencode(sys.argv[2]), 1)
if rc != 0:
    value = ctypes.get_errno()
    raise SystemExit(17 if value == errno.EEXIST else 3)
PY
  publish_status=$?
  if [ "$publish_status" -eq 17 ]; then
    fail_action6 INPUT_OR_PRECONDITION_ERROR IMMUTABLE_VERSION_CONFLICT ATOMIC_PUBLICATION
    return 1
  fi
  [ "$publish_status" -eq 0 ] || { fail_action6 VALIDATION_FAIL ATOMIC_PUBLICATION_FAILED ATOMIC_PUBLICATION; return 1; }
  INSTALL_STAGE=
  sync -f "$VERSIONS" && sync -f "$DATA_ROOT" || { fail_action6 VALIDATION_FAIL FSYNC_FAILED DURABLE_PUBLICATION; return 1; }
  verify_final_identity || { fail_action6 VALIDATION_FAIL POST_PUBLICATION_IDENTITY_FAILED FINAL_DATASET_IDENTITY; return 1; }
  printf 'IMMUTABLE_INSTALLATION=PASS_NEW\nFINAL_DATASET_IDENTITY=PASS\n'
  validate_pair "$FINAL_DIR" || { fail_action6 VALIDATION_FAIL FINAL_VALIDATOR_FAILED FINAL_DATASET_VALIDATION; return 1; }
  printf 'FINAL_DATASET_VALIDATION=PASS\n'
  configuration_unchanged || { fail_action6 VALIDATION_FAIL CONFIGURATION_CHANGED CONFIGURATION_PROTECTION; return 1; }
  printf 'CONFIGURATION_UNTOUCHED=PASS\nACTION6=COMPLETE\nRESULT=PASS\n'
}

main() {
  FAILURE_REPORTED=0
  GOVERNANCE_COMMIT=
  CONFIG_SHA256_BEFORE=
  [ "$#" -eq 2 ] && [ "$1" = --governance-commit ] || { fail_action6 INPUT_OR_PRECONDITION_ERROR INVALID_ARGUMENTS INPUT_VALIDATION; return 1; }
  GOVERNANCE_COMMIT=$2
  printf '%s' "$GOVERNANCE_COMMIT" | grep -Eq '^[0-9a-f]{40}$' || { fail_action6 INPUT_OR_PRECONDITION_ERROR INVALID_GOVERNANCE_COMMIT INPUT_VALIDATION; return 1; }
  verify_target_source_runtime || return 1
  verify_transport_stage || return 1
  accept_existing_or_prepare || return 1
  [ -n "$INSTALL_STAGE" ] || return 0
  copy_validate_publish || return 1
}

action6_entry() {
  main "$@"
  action6_status=$?
  if [ "$action6_status" -ne 0 ] && [ "${FAILURE_REPORTED:-0}" -ne 1 ]; then
    fail_action6 VALIDATION_FAIL ACTION6_UNEXPECTED_ERROR ACTION6_UNEXPECTED
    action6_status=$?
  fi
  return "$action6_status"
}

action6_entry "$@"
