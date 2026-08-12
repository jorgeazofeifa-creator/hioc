#!/usr/bin/env bash

# Governed PE-3 Production Action 5: supported code deployment and identity.

SOURCE=/home/jazofv1/hioc-release-source
RUNTIME=/home/jazofv1/hioc
SCRIPT_PATH=tools/hioc-pe3-action5-deploy.sh
IMPLEMENTATION_COMMIT=157ae644dcedcbec7c69cb0d8b054e104335e024
PROTECTION_TOOL=tools/hioc_manufacturer_protection.py
ARTIFACTS='pi4/lib/hioc/manufacturer.py pi4/bin/hioc-build-manufacturer-db.py pi4/bin/hioc-validate-manufacturer.py pi4/bin/hioc-generate-manufacturer.py pi4/install_pi4.sh pi4/validate_pi4.sh pi4/config/hioc.conf.example release/upgrade.sh release/rollback.sh tools/hioc_manufacturer_protection.py'

fail_action5() {
  FAILURE_REPORTED=1
  printf 'RESULT=%s\nERROR_CODE=%s\nFAILURE_STAGE=%s\nROLLBACK_RECOMMENDED=%s\n' "$1" "$2" "$3" "$4"
  return 1
}

source_fail() { fail_action5 INPUT_OR_PRECONDITION_ERROR "$1" SOURCE_IDENTITY FALSE; }

active_git_operation() {
  for marker in MERGE_HEAD REBASE_HEAD CHERRY_PICK_HEAD REVERT_HEAD BISECT_LOG; do
    [ ! -e "$SOURCE/.git/$marker" ] || return 0
  done
  [ ! -d "$SOURCE/.git/rebase-merge" ] && [ ! -d "$SOURCE/.git/rebase-apply" ] || return 0
  return 1
}

verify_target_and_source() {
  [ "$(hostname -s 2>/dev/null)" = nutandpihole ] || { fail_action5 INPUT_OR_PRECONDITION_ERROR WRONG_TARGET TARGET_IDENTITY FALSE; return 1; }
  ip -o -4 addr show scope global 2>/dev/null | awk '{print $4}' | cut -d/ -f1 | grep -Fxq 192.168.100.252 || { fail_action5 INPUT_OR_PRECONDITION_ERROR WRONG_TARGET TARGET_IDENTITY FALSE; return 1; }
  printf 'TARGET_IDENTITY=PASS\n'
  [ -d "$SOURCE/.git" ] || { source_fail SOURCE_REPOSITORY_MISSING; return 1; }
  [ "$(git -C "$SOURCE" branch --show-current 2>/dev/null)" = main ] || { source_fail WRONG_BRANCH; return 1; }
  [ "$(git -C "$SOURCE" rev-parse HEAD 2>/dev/null)" = "$GOVERNANCE_COMMIT" ] || { source_fail GOVERNANCE_COMMIT_MISMATCH; return 1; }
  [ "$(git -C "$SOURCE" rev-parse origin/main 2>/dev/null)" = "$GOVERNANCE_COMMIT" ] || { source_fail GOVERNANCE_COMMIT_MISMATCH; return 1; }
  [ -z "$(git -C "$SOURCE" status --porcelain 2>/dev/null)" ] || { source_fail SOURCE_REPOSITORY_DIRTY; return 1; }
  active_git_operation && { source_fail ACTIVE_GIT_OPERATION; return 1; }
  [ -f "$SOURCE/$SCRIPT_PATH" ] && [ ! -L "$SOURCE/$SCRIPT_PATH" ] || { source_fail ACTION5_SCRIPT_IDENTITY_MISMATCH; return 1; }
  expected_script_blob="$(git -C "$SOURCE" rev-parse "$GOVERNANCE_COMMIT:$SCRIPT_PATH" 2>/dev/null)" || { source_fail ACTION5_SCRIPT_IDENTITY_MISMATCH; return 1; }
  actual_script_blob="$(git -C "$SOURCE" hash-object --path="$SCRIPT_PATH" "$SOURCE/$SCRIPT_PATH" 2>/dev/null)" || { source_fail ACTION5_SCRIPT_IDENTITY_MISMATCH; return 1; }
  [ "$actual_script_blob" = "$expected_script_blob" ] && git -C "$SOURCE" diff --quiet -- "$SCRIPT_PATH" || { source_fail ACTION5_SCRIPT_IDENTITY_MISMATCH; return 1; }
  git -C "$SOURCE" cat-file -e "$IMPLEMENTATION_COMMIT^{commit}" 2>/dev/null || { source_fail IMPLEMENTATION_COMMIT_MISSING; return 1; }
  git -C "$SOURCE" merge-base --is-ancestor "$IMPLEMENTATION_COMMIT" "$GOVERNANCE_COMMIT" >/dev/null 2>&1 || { source_fail IMPLEMENTATION_ANCESTRY_FAILED; return 1; }
  printf 'SOURCE_IDENTITY=PASS\n'
}

prepare_evidence_and_manifest() {
  EVIDENCE_DIR="$(mktemp -d /tmp/hioc-pe3-action5-XXXXXXXX 2>/dev/null)" || { fail_action5 INPUT_OR_PRECONDITION_ERROR EVIDENCE_PATH_FAILED EVIDENCE_PREPARATION FALSE; return 1; }
  chmod 0700 "$EVIDENCE_DIR" || { fail_action5 INPUT_OR_PRECONDITION_ERROR EVIDENCE_PATH_FAILED EVIDENCE_PREPARATION FALSE; return 1; }
  # shellcheck disable=SC2086
  python3 "$SOURCE/tools/git_artifact_manifest.py" "$GOVERNANCE_COMMIT" $ARTIFACTS --repo "$SOURCE" --compare-worktree > "$EVIDENCE_DIR/git-artifacts.json" 2>/dev/null || { fail_action5 INPUT_OR_PRECONDITION_ERROR SOURCE_ARTIFACT_IDENTITY_FAILED SOURCE_IDENTITY FALSE; return 1; }
  jq -e --arg c "$GOVERNANCE_COMMIT" '.commit==$c and .generated_from_git_objects and all(.artifacts[];.working_tree_equal==true)' "$EVIDENCE_DIR/git-artifacts.json" >/dev/null 2>&1 || { fail_action5 INPUT_OR_PRECONDITION_ERROR SOURCE_ARTIFACT_IDENTITY_FAILED SOURCE_IDENTITY FALSE; return 1; }
}

snapshot_manufacturer_state() {
  python3 "$SOURCE/$PROTECTION_TOOL" snapshot --runtime "$RUNTIME" > "$1" 2>/dev/null || { fail_action5 INPUT_OR_PRECONDITION_ERROR MANUFACTURER_SNAPSHOT_FAILED MANUFACTURER_PROTECTION FALSE; return 1; }
}

validate_release() {
  bash "$SOURCE/release/validate.sh" > "$EVIDENCE_DIR/release-validation.sanitized.txt" 2>&1 || { fail_action5 VALIDATION_FAIL RELEASE_VALIDATION_FAILED RELEASE_VALIDATION FALSE; return 1; }
  grep -Fxq 'HIOC release validation passed.' "$EVIDENCE_DIR/release-validation.sanitized.txt" || { fail_action5 VALIDATION_FAIL RELEASE_VALIDATION_FAILED RELEASE_VALIDATION FALSE; return 1; }
  printf 'RELEASE_VALIDATION=PASS\n'
}

validate_backup_path() {
  [ -n "$RELEASE_BACKUP" ] && [ -d "$RELEASE_BACKUP" ] && [ ! -L "$RELEASE_BACKUP" ] || return 1
  [ -d "$RELEASE_BACKUP/current" ] && [ ! -L "$RELEASE_BACKUP/current" ] || return 1
  [ -f "$RELEASE_BACKUP/current/release/rollback.sh" ] && [ ! -L "$RELEASE_BACKUP/current/release/rollback.sh" ] || return 1
  [ -f "$RELEASE_BACKUP/current/pi4/install_pi4.sh" ] && [ ! -L "$RELEASE_BACKUP/current/pi4/install_pi4.sh" ] || return 1
  backup_real="$(realpath "$RELEASE_BACKUP" 2>/dev/null)" || return 1
  backup_root_real="$(realpath "$RUNTIME/backups" 2>/dev/null)" || return 1
  case "$backup_real" in "$backup_root_real"/release-upgrade-*) ;; *) return 1 ;; esac
  return 0
}

deploy_supported_release() {
  [ -d "$RUNTIME" ] && [ ! -L "$RUNTIME" ] || { fail_action5 INPUT_OR_PRECONDITION_ERROR BACKUP_PRECONDITION_FAILED RELEASE_BACKUP FALSE; return 1; }
  [ -d "$RUNTIME/backups" ] && [ ! -L "$RUNTIME/backups" ] && [ -w "$RUNTIME/backups" ] || { fail_action5 INPUT_OR_PRECONDITION_ERROR BACKUP_PRECONDITION_FAILED RELEASE_BACKUP FALSE; return 1; }
  find "$RUNTIME/backups" -mindepth 1 -maxdepth 1 -type d -name 'release-upgrade-*' -printf '%p\n' > "$EVIDENCE_DIR/backups-before.unsorted.txt" 2>/dev/null || { fail_action5 INPUT_OR_PRECONDITION_ERROR BACKUP_PRECONDITION_FAILED RELEASE_BACKUP FALSE; return 1; }
  sort "$EVIDENCE_DIR/backups-before.unsorted.txt" > "$EVIDENCE_DIR/backups-before.txt" || { fail_action5 INPUT_OR_PRECONDITION_ERROR EVIDENCE_PATH_FAILED EVIDENCE_PREPARATION FALSE; return 1; }
  snapshot_manufacturer_state "$EVIDENCE_DIR/manufacturer-before.json" || return 1
  python3 "$SOURCE/$PROTECTION_TOOL" validate-predeploy --snapshot "$EVIDENCE_DIR/manufacturer-before.json" >/dev/null 2>&1 || { fail_action5 INPUT_OR_PRECONDITION_ERROR MANUFACTURER_PREDEPLOY_STATE_INVALID MANUFACTURER_PROTECTION FALSE; return 1; }
  HIOC_INSTALL_DIR="$RUNTIME" bash "$SOURCE/release/upgrade.sh" > "$EVIDENCE_DIR/release-upgrade.sanitized.txt" 2>&1
  upgrade_status=$?
  find "$RUNTIME/backups" -mindepth 1 -maxdepth 1 -type d -name 'release-upgrade-*' -printf '%p\n' > "$EVIDENCE_DIR/backups-after.unsorted.txt" 2>/dev/null || { fail_action5 VALIDATION_FAIL EVIDENCE_PATH_FAILED EVIDENCE_REPORT TRUE; return 1; }
  sort "$EVIDENCE_DIR/backups-after.unsorted.txt" > "$EVIDENCE_DIR/backups-after.txt" || { fail_action5 VALIDATION_FAIL EVIDENCE_PATH_FAILED EVIDENCE_REPORT TRUE; return 1; }
  new_backups="$(comm -13 "$EVIDENCE_DIR/backups-before.txt" "$EVIDENCE_DIR/backups-after.txt" 2>/dev/null)" || { fail_action5 VALIDATION_FAIL EVIDENCE_PATH_FAILED EVIDENCE_REPORT TRUE; return 1; }
  if [ "$upgrade_status" -ne 0 ]; then
    if [ -n "$new_backups" ]; then
      fail_action5 VALIDATION_FAIL CODE_DEPLOYMENT_FAILED CODE_DEPLOYMENT TRUE
    else
      fail_action5 VALIDATION_FAIL RELEASE_BACKUP_CREATION_FAILED RELEASE_BACKUP FALSE
    fi
    return 1
  fi
  [ -f "$RUNTIME/backups/last-upgrade-backup" ] && [ ! -L "$RUNTIME/backups/last-upgrade-backup" ] || { fail_action5 VALIDATION_FAIL RELEASE_BACKUP_CREATION_FAILED RELEASE_BACKUP TRUE; return 1; }
  RELEASE_BACKUP="$(cat "$RUNTIME/backups/last-upgrade-backup" 2>/dev/null)"
  validate_backup_path || { fail_action5 VALIDATION_FAIL RELEASE_BACKUP_INVALID RELEASE_BACKUP TRUE; return 1; }
  grep -Fxq "$RELEASE_BACKUP" "$EVIDENCE_DIR/backups-before.txt" && { fail_action5 VALIDATION_FAIL RELEASE_BACKUP_NOT_NEW RELEASE_BACKUP TRUE; return 1; }
  printf '%s\n' "$RELEASE_BACKUP" > "$EVIDENCE_DIR/release-backup-path.txt" || { fail_action5 VALIDATION_FAIL EVIDENCE_PATH_FAILED EVIDENCE_REPORT TRUE; return 1; }
  printf 'RELEASE_BACKUP=PASS\nCODE_DEPLOYMENT=PASS\n'
}

validate_runtime_and_artifacts() {
  HIOC_INSTALL_DIR="$RUNTIME" bash "$RUNTIME/pi4/validate_pi4.sh" > "$EVIDENCE_DIR/runtime-validation.sanitized.txt" 2>&1 || { fail_action5 VALIDATION_FAIL RUNTIME_VALIDATION_FAILED RUNTIME_VALIDATION TRUE; return 1; }
  grep -Fxq 'HIOC Pi4 validation passed.' "$EVIDENCE_DIR/runtime-validation.sanitized.txt" || { fail_action5 VALIDATION_FAIL RUNTIME_VALIDATION_FAILED RUNTIME_VALIDATION TRUE; return 1; }
  printf 'RUNTIME_VALIDATION=PASS\n'
  for rel in $ARTIFACTS; do
    expected="$(jq -r --arg p "$rel" '.artifacts[]|select(.path==$p)|.sha256' "$EVIDENCE_DIR/git-artifacts.json" 2>/dev/null)"
    [ -n "$expected" ] && [ -f "$RUNTIME/$rel" ] && [ ! -L "$RUNTIME/$rel" ] && [ "$(sha256sum "$RUNTIME/$rel" 2>/dev/null | awk '{print $1}')" = "$expected" ] || { fail_action5 VALIDATION_FAIL RUNTIME_ARTIFACT_IDENTITY_MISMATCH RUNTIME_ARTIFACT_IDENTITY TRUE; return 1; }
  done
  python3 "$SOURCE/$PROTECTION_TOOL" snapshot --runtime "$RUNTIME" > "$EVIDENCE_DIR/manufacturer-after.json" 2>/dev/null || { fail_action5 VALIDATION_FAIL MANUFACTURER_SNAPSHOT_FAILED MANUFACTURER_PROTECTION TRUE; return 1; }
  protection_result="$(python3 "$SOURCE/$PROTECTION_TOOL" compare --before "$EVIDENCE_DIR/manufacturer-before.json" --after "$EVIDENCE_DIR/manufacturer-after.json" 2>/dev/null)"
  protection_status=$?
  if [ "$protection_status" -ne 0 ]; then
    protection_code="$(printf '%s' "$protection_result" | jq -r '.code // "MANUFACTURER_PROTECTION_FAILED"' 2>/dev/null)"
    case "$protection_code" in
      CONFIGURATION_CHANGED) fail_action5 VALIDATION_FAIL CONFIGURATION_CHANGED MANUFACTURER_PROTECTION TRUE ;;
      *) fail_action5 VALIDATION_FAIL MANUFACTURER_PAYLOAD_CHANGED MANUFACTURER_PROTECTION TRUE ;;
    esac
    return 1
  fi
  printf 'MANUFACTURER_PAYLOAD_UNTOUCHED=PASS\nMANUFACTURER_SCAFFOLDING_STATE=PASS\nCONFIGURATION_UNTOUCHED=PASS\n'
  printf 'RUNTIME_ARTIFACT_IDENTITY=PASS\n'
}

write_evidence_report() {
  jq -n --arg commit "$GOVERNANCE_COMMIT" --arg script_blob "$expected_script_blob" --arg backup "$RELEASE_BACKUP" '{schema_version:1,result:"PASS",target:"nutandpihole",source_commit:$commit,action5_script_blob:$script_blob,release_validation:"PASS",release_backup:$backup,code_deployment:"PASS",runtime_validation:"PASS",runtime_artifact_identity:"PASS",manufacturer_payload_untouched:true,manufacturer_scaffolding_state:"PRIVATE_EMPTY_OR_PAYLOAD_PRESERVED",configuration_untouched:true,rollback_recommended:false}' > "$EVIDENCE_DIR/action5-evidence.json" 2>/dev/null || { fail_action5 VALIDATION_FAIL EVIDENCE_PATH_FAILED EVIDENCE_REPORT TRUE; return 1; }
  printf 'EVIDENCE_REPORT=PASS\nEVIDENCE_DIR=%s\nRELEASE_BACKUP_PATH=%s\n' "$EVIDENCE_DIR" "$RELEASE_BACKUP"
}

main() {
  FAILURE_REPORTED=0
  GOVERNANCE_COMMIT=
  EVIDENCE_DIR=
  RELEASE_BACKUP=
  [ "$#" -eq 2 ] && [ "$1" = --governance-commit ] || { fail_action5 INPUT_OR_PRECONDITION_ERROR INVALID_ARGUMENTS INPUT_VALIDATION FALSE; return 1; }
  GOVERNANCE_COMMIT=$2
  printf '%s' "$GOVERNANCE_COMMIT" | grep -Eq '^[0-9a-f]{40}$' || { fail_action5 INPUT_OR_PRECONDITION_ERROR INVALID_GOVERNANCE_COMMIT INPUT_VALIDATION FALSE; return 1; }
  verify_target_and_source || return 1
  prepare_evidence_and_manifest || return 1
  validate_release || return 1
  deploy_supported_release || return 1
  validate_runtime_and_artifacts || return 1
  write_evidence_report || return 1
  printf 'ACTION5=COMPLETE\nRESULT=PASS\nROLLBACK_RECOMMENDED=FALSE\n'
}

action5_entry() {
  main "$@"
  action5_status=$?
  if [ "$action5_status" -ne 0 ] && [ "${FAILURE_REPORTED:-0}" -ne 1 ]; then
    fail_action5 VALIDATION_FAIL ACTION5_UNEXPECTED_ERROR ACTION5_UNEXPECTED FALSE
    action5_status=$?
  fi
  return "$action5_status"
}

action5_entry "$@"
