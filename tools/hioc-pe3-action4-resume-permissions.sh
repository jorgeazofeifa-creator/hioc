#!/usr/bin/env bash

# Governed PE-3 Production Action 4 resume checkpoint. This script performs
# only bounded staging permission normalization and read-only validation.

SOURCE=/home/jazofv1/hioc-release-source
PI3_STAGE=/tmp/hioc-pe3-dataset-transfer-PJ5qPbRS
DB="$PI3_STAGE/manufacturer-db.json"
MF="$PI3_STAGE/manufacturer-db.manifest.json"
IMPLEMENTATION_COMMIT=157ae644dcedcbec7c69cb0d8b054e104335e024
SCRIPT_PATH=tools/hioc-pe3-action4-resume-permissions.sh
DB_BYTES=8652642
MF_BYTES=1338
DB_SHA256=81f147cc57768c5797c4ad73a8c0369001bbdcbfe1548e71d3702c8c7f81e0e1
MF_SHA256=10c8097c0a4ec6e8cc4cd3dc61afc7f368057f4ef4b6534df9f6dd31634a4ac4
EXPECTED_RECORD_COUNT=53581

result_fail() {
  printf 'RESULT=%s\nERROR_CODE=%s\nFAILURE_STAGE=%s\n' "$1" "$2" "$3"
  return 1
}

source_fail() { result_fail INPUT_OR_PRECONDITION_ERROR SOURCE_IDENTITY_DRIFT SOURCE_IDENTITY_RECHECK; }
stage_fail() { result_fail INPUT_OR_PRECONDITION_ERROR "$1" STAGING_IDENTITY_RECHECK; }
post_fail() { result_fail VALIDATION_FAIL "$1" POST_NORMALIZATION_IDENTITY; }

exact_stage_entries() {
  [ "$(find "$PI3_STAGE" -mindepth 1 -maxdepth 1 -printf '%f\n' 2>/dev/null | sort | paste -sd, -)" = \
    'manufacturer-db.json,manufacturer-db.manifest.json' ]
}

regular_owned_file() {
  [ -f "$1" ] && [ ! -L "$1" ] &&
    [ "$(stat -c %U:%G "$1" 2>/dev/null)" = jazofv1:jazofv1 ]
}

stage_directory_valid() {
  [ -d "$PI3_STAGE" ] && [ ! -L "$PI3_STAGE" ] &&
    [ "$(stat -c %U:%G "$PI3_STAGE" 2>/dev/null)" = jazofv1:jazofv1 ] &&
    [ "$(stat -c %a "$PI3_STAGE" 2>/dev/null)" = 700 ]
}

verify_source_identity() {
  [ "$(hostname -s 2>/dev/null)" = nutandpihole ] || { result_fail INPUT_OR_PRECONDITION_ERROR WRONG_TARGET SOURCE_IDENTITY_RECHECK; return 1; }
  ip -o -4 addr show scope global 2>/dev/null | awk '{print $4}' | cut -d/ -f1 | grep -Fxq 192.168.100.252 || { result_fail INPUT_OR_PRECONDITION_ERROR WRONG_TARGET SOURCE_IDENTITY_RECHECK; return 1; }
  [ -d "$SOURCE/.git" ] || { source_fail; return 1; }
  [ "$(git -C "$SOURCE" branch --show-current 2>/dev/null)" = main ] || { source_fail; return 1; }
  [ "$(git -C "$SOURCE" rev-parse HEAD 2>/dev/null)" = "$GOVERNANCE_COMMIT" ] || { source_fail; return 1; }
  [ "$(git -C "$SOURCE" rev-parse origin/main 2>/dev/null)" = "$GOVERNANCE_COMMIT" ] || { source_fail; return 1; }
  [ -z "$(git -C "$SOURCE" status --porcelain 2>/dev/null)" ] || { source_fail; return 1; }
  for marker in MERGE_HEAD REBASE_HEAD CHERRY_PICK_HEAD REVERT_HEAD BISECT_LOG; do
    [ ! -e "$SOURCE/.git/$marker" ] || { source_fail; return 1; }
  done
  [ ! -d "$SOURCE/.git/rebase-merge" ] && [ ! -d "$SOURCE/.git/rebase-apply" ] || { source_fail; return 1; }
  git -C "$SOURCE" cat-file -e "$IMPLEMENTATION_COMMIT^{commit}" 2>/dev/null || { source_fail; return 1; }
  git -C "$SOURCE" merge-base --is-ancestor "$IMPLEMENTATION_COMMIT" HEAD >/dev/null 2>&1 || { source_fail; return 1; }
  git -C "$SOURCE" diff --quiet "$IMPLEMENTATION_COMMIT" -- pi4/lib/hioc/manufacturer.py pi4/bin/hioc-validate-manufacturer.py || { source_fail; return 1; }
  expected_blob="$(git -C "$SOURCE" rev-parse "$GOVERNANCE_COMMIT:$SCRIPT_PATH" 2>/dev/null)" || { source_fail; return 1; }
  actual_blob="$(git -C "$SOURCE" hash-object --path="$SCRIPT_PATH" "$SOURCE/$SCRIPT_PATH" 2>/dev/null)" || { source_fail; return 1; }
  [ "$actual_blob" = "$expected_blob" ] || { result_fail INPUT_OR_PRECONDITION_ERROR ACTION4_SCRIPT_IDENTITY_MISMATCH SOURCE_IDENTITY_RECHECK; return 1; }
  git -C "$SOURCE" diff --quiet -- "$SCRIPT_PATH" || { result_fail INPUT_OR_PRECONDITION_ERROR ACTION4_SCRIPT_IDENTITY_MISMATCH SOURCE_IDENTITY_RECHECK; return 1; }
  printf 'SOURCE_IDENTITY_RECHECK=PASS\n'
}

verify_stage_before_normalization() {
  stage_directory_valid || { stage_fail STAGING_IDENTITY_DRIFT; return 1; }
  exact_stage_entries || { stage_fail STAGING_EXTRA_OR_MISSING_ENTRY; return 1; }
  regular_owned_file "$DB" && regular_owned_file "$MF" || { stage_fail STAGING_OWNER_OR_TYPE_DRIFT; return 1; }
  [ "$(stat -c %s "$DB" 2>/dev/null)" = "$DB_BYTES" ] &&
    [ "$(stat -c %s "$MF" 2>/dev/null)" = "$MF_BYTES" ] || { stage_fail STAGING_SIZE_DRIFT; return 1; }
  db_hash="$(sha256sum "$DB" 2>/dev/null | awk '{print $1}')"
  mf_hash="$(sha256sum "$MF" 2>/dev/null | awk '{print $1}')"
  [ "$db_hash" = "$DB_SHA256" ] && [ "$mf_hash" = "$MF_SHA256" ] || { stage_fail STAGING_HASH_DRIFT; return 1; }
  for path in "$DB" "$MF"; do
    mode="$(stat -c %a "$path" 2>/dev/null)"
    [ "$mode" = 600 ] || [ "$mode" = 644 ] || { result_fail INPUT_OR_PRECONDITION_ERROR UNSUPPORTED_PRE_NORMALIZATION_MODE STAGING_PERMISSION_NORMALIZATION; return 1; }
  done
  printf 'STAGING_IDENTITY_RECHECK=PASS\n'
}

normalize_permissions() {
  if [ "$(stat -c %a "$DB" 2>/dev/null)" = 644 ]; then
    chmod 0600 -- "$DB" || { result_fail VALIDATION_FAIL STAGING_CHMOD_FAILED STAGING_PERMISSION_NORMALIZATION; return 1; }
  fi
  if [ "$(stat -c %a "$MF" 2>/dev/null)" = 644 ]; then
    chmod 0600 -- "$MF" || { result_fail VALIDATION_FAIL STAGING_CHMOD_FAILED STAGING_PERMISSION_NORMALIZATION; return 1; }
  fi
  printf 'STAGING_PERMISSION_NORMALIZATION=PASS\n'
}

verify_stage_after_normalization() {
  stage_directory_valid || { post_fail POST_NORMALIZATION_DIRECTORY_DRIFT; return 1; }
  exact_stage_entries || { post_fail POST_NORMALIZATION_CONTENTS_DRIFT; return 1; }
  regular_owned_file "$DB" && regular_owned_file "$MF" || { post_fail POST_NORMALIZATION_OWNER_OR_TYPE_DRIFT; return 1; }
  [ "$(stat -c %a "$DB" 2>/dev/null)" = 600 ] &&
    [ "$(stat -c %a "$MF" 2>/dev/null)" = 600 ] || { post_fail POST_NORMALIZATION_MODE_DRIFT; return 1; }
  [ "$(stat -c %s "$DB" 2>/dev/null)" = "$DB_BYTES" ] &&
    [ "$(stat -c %s "$MF" 2>/dev/null)" = "$MF_BYTES" ] || { post_fail POST_NORMALIZATION_SIZE_DRIFT; return 1; }
  [ "$(sha256sum "$DB" 2>/dev/null | awk '{print $1}')" = "$DB_SHA256" ] &&
    [ "$(sha256sum "$MF" 2>/dev/null | awk '{print $1}')" = "$MF_SHA256" ] || { post_fail POST_NORMALIZATION_HASH_DRIFT; return 1; }
  printf 'POST_NORMALIZATION_IDENTITY=PASS\n'
}

validate_manufacturer() {
  validator_output="$(HIOC_HOME="$SOURCE" python3 "$SOURCE/pi4/bin/hioc-validate-manufacturer.py" database --database "$DB" --manifest "$MF" --json 2>/dev/null)"
  validator_status=$?
  [ "$validator_status" -eq 0 ] || { result_fail VALIDATION_FAIL MANUFACTURER_VALIDATOR_FAILED MANUFACTURER_VALIDATION; return 1; }
  python3 -c 'import json,sys; d=json.loads(sys.argv[1]); raise SystemExit(0 if d.get("result")=="PASS" else 1)' "$validator_output" >/dev/null 2>&1 || { result_fail VALIDATION_FAIL MANUFACTURER_VALIDATOR_RESULT_INVALID MANUFACTURER_VALIDATION; return 1; }
  python3 -c 'import json,sys; d=json.loads(sys.argv[1]); raise SystemExit(0 if d.get("privacy_safe") is True else 1)' "$validator_output" >/dev/null 2>&1 || { result_fail VALIDATION_FAIL MANUFACTURER_PRIVACY_CHECK_FAILED MANUFACTURER_VALIDATION; return 1; }
  python3 -c 'import json,sys; d=json.loads(sys.argv[1]); raise SystemExit(0 if d.get("record_count")==int(sys.argv[2]) else 1)' "$validator_output" "$EXPECTED_RECORD_COUNT" >/dev/null 2>&1 || { result_fail VALIDATION_FAIL MANUFACTURER_RECORD_COUNT_MISMATCH MANUFACTURER_VALIDATION; return 1; }
  printf '%s\n' "$validator_output"
  printf 'MANUFACTURER_VALIDATION=PASS\n'
}

main() {
  GOVERNANCE_COMMIT=
  [ "$#" -eq 2 ] && [ "$1" = --governance-commit ] || { result_fail INPUT_OR_PRECONDITION_ERROR INVALID_ARGUMENTS INPUT_VALIDATION; return 1; }
  GOVERNANCE_COMMIT=$2
  printf '%s' "$GOVERNANCE_COMMIT" | grep -Eq '^[0-9a-f]{40}$' || { result_fail INPUT_OR_PRECONDITION_ERROR INVALID_GOVERNANCE_COMMIT INPUT_VALIDATION; return 1; }
  verify_source_identity || return 1
  verify_stage_before_normalization || return 1
  normalize_permissions || return 1
  verify_stage_after_normalization || return 1
  validate_manufacturer || return 1
  printf 'ACTION4=COMPLETE\nRESULT=PASS\n'
}

main "$@"
