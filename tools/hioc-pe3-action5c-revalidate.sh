#!/usr/bin/env bash

# Governed read-only closure for the PE-3 Action 5 scaffolding false positive.

SOURCE=/home/jazofv1/hioc-release-source
RUNTIME=/home/jazofv1/hioc
SCRIPT_PATH=tools/hioc-pe3-action5c-revalidate.sh
PROTECTION_TOOL=tools/hioc_manufacturer_protection.py
IMPLEMENTATION_COMMIT=157ae644dcedcbec7c69cb0d8b054e104335e024
RUNTIME_ARTIFACTS='pi4/lib/hioc/manufacturer.py pi4/bin/hioc-build-manufacturer-db.py pi4/bin/hioc-validate-manufacturer.py pi4/bin/hioc-generate-manufacturer.py pi4/install_pi4.sh pi4/validate_pi4.sh pi4/config/hioc.conf.example release/upgrade.sh release/rollback.sh'

fail_action5c() {
  FAILURE_REPORTED=1
  printf 'RESULT=%s\nERROR_CODE=%s\nFAILURE_STAGE=%s\nROLLBACK_RECOMMENDED=FALSE\n' "$1" "$2" "$3"
  return 1
}

verify_source() {
  [ "$(hostname -s 2>/dev/null)" = nutandpihole ] || { fail_action5c INPUT_OR_PRECONDITION_ERROR WRONG_TARGET TARGET_IDENTITY; return 1; }
  ip -o -4 addr show scope global 2>/dev/null | awk '{print $4}' | cut -d/ -f1 | grep -Fxq 192.168.100.252 || { fail_action5c INPUT_OR_PRECONDITION_ERROR WRONG_TARGET TARGET_IDENTITY; return 1; }
  printf 'TARGET_IDENTITY=PASS\n'
  [ -d "$SOURCE/.git" ] || { fail_action5c INPUT_OR_PRECONDITION_ERROR SOURCE_REPOSITORY_MISSING SOURCE_IDENTITY; return 1; }
  [ "$(git -C "$SOURCE" branch --show-current 2>/dev/null)" = main ] || { fail_action5c INPUT_OR_PRECONDITION_ERROR WRONG_BRANCH SOURCE_IDENTITY; return 1; }
  [ "$(git -C "$SOURCE" rev-parse HEAD 2>/dev/null)" = "$GOVERNANCE_COMMIT" ] && [ "$(git -C "$SOURCE" rev-parse origin/main 2>/dev/null)" = "$GOVERNANCE_COMMIT" ] || { fail_action5c INPUT_OR_PRECONDITION_ERROR GOVERNANCE_COMMIT_MISMATCH SOURCE_IDENTITY; return 1; }
  [ -z "$(git -C "$SOURCE" status --porcelain 2>/dev/null)" ] || { fail_action5c INPUT_OR_PRECONDITION_ERROR SOURCE_REPOSITORY_DIRTY SOURCE_IDENTITY; return 1; }
  [ -f "$SOURCE/$SCRIPT_PATH" ] && [ ! -L "$SOURCE/$SCRIPT_PATH" ] || { fail_action5c INPUT_OR_PRECONDITION_ERROR ACTION5C_SCRIPT_IDENTITY_MISMATCH SOURCE_IDENTITY; return 1; }
  expected_script_blob="$(git -C "$SOURCE" rev-parse "$GOVERNANCE_COMMIT:$SCRIPT_PATH" 2>/dev/null)" || { fail_action5c INPUT_OR_PRECONDITION_ERROR ACTION5C_SCRIPT_IDENTITY_MISMATCH SOURCE_IDENTITY; return 1; }
  [ "$(git -C "$SOURCE" hash-object --path="$SCRIPT_PATH" "$SOURCE/$SCRIPT_PATH" 2>/dev/null)" = "$expected_script_blob" ] && git -C "$SOURCE" diff --quiet -- "$SCRIPT_PATH" || { fail_action5c INPUT_OR_PRECONDITION_ERROR ACTION5C_SCRIPT_IDENTITY_MISMATCH SOURCE_IDENTITY; return 1; }
  git -C "$SOURCE" merge-base --is-ancestor "$IMPLEMENTATION_COMMIT" "$GOVERNANCE_COMMIT" >/dev/null 2>&1 || { fail_action5c INPUT_OR_PRECONDITION_ERROR IMPLEMENTATION_ANCESTRY_FAILED SOURCE_IDENTITY; return 1; }
  printf 'SOURCE_IDENTITY=PASS\n'
}

validate_backup() {
  [ -f "$RUNTIME/backups/last-upgrade-backup" ] && [ ! -L "$RUNTIME/backups/last-upgrade-backup" ] || { fail_action5c INPUT_OR_PRECONDITION_ERROR RELEASE_BACKUP_MISSING RELEASE_BACKUP_IDENTITY; return 1; }
  [ "$(cat "$RUNTIME/backups/last-upgrade-backup" 2>/dev/null)" = "$RELEASE_BACKUP" ] || { fail_action5c INPUT_OR_PRECONDITION_ERROR RELEASE_BACKUP_MISMATCH RELEASE_BACKUP_IDENTITY; return 1; }
  [ -d "$RELEASE_BACKUP/current" ] && [ ! -L "$RELEASE_BACKUP" ] && [ ! -L "$RELEASE_BACKUP/current" ] || { fail_action5c INPUT_OR_PRECONDITION_ERROR RELEASE_BACKUP_INVALID RELEASE_BACKUP_IDENTITY; return 1; }
  printf 'RELEASE_BACKUP_IDENTITY=PASS\n'
}

revalidate_current() {
  EVIDENCE_DIR="$(mktemp -d /tmp/hioc-pe3-action5c-XXXXXXXX 2>/dev/null)" || { fail_action5c INPUT_OR_PRECONDITION_ERROR EVIDENCE_PATH_FAILED EVIDENCE_PREPARATION; return 1; }
  chmod 0700 "$EVIDENCE_DIR" || { fail_action5c INPUT_OR_PRECONDITION_ERROR EVIDENCE_PATH_FAILED EVIDENCE_PREPARATION; return 1; }
  bash "$SOURCE/release/validate.sh" > "$EVIDENCE_DIR/release-validation.sanitized.txt" 2>&1 || { fail_action5c VALIDATION_FAIL RELEASE_VALIDATION_FAILED RELEASE_VALIDATION; return 1; }
  grep -Fxq 'HIOC release validation passed.' "$EVIDENCE_DIR/release-validation.sanitized.txt" || { fail_action5c VALIDATION_FAIL RELEASE_VALIDATION_FAILED RELEASE_VALIDATION; return 1; }
  printf 'RELEASE_VALIDATION=PASS\n'
  HIOC_INSTALL_DIR="$RUNTIME" bash "$RUNTIME/pi4/validate_pi4.sh" > "$EVIDENCE_DIR/runtime-validation.sanitized.txt" 2>&1 || { fail_action5c VALIDATION_FAIL RUNTIME_VALIDATION_FAILED RUNTIME_VALIDATION; return 1; }
  grep -Fxq 'HIOC Pi4 validation passed.' "$EVIDENCE_DIR/runtime-validation.sanitized.txt" || { fail_action5c VALIDATION_FAIL RUNTIME_VALIDATION_FAILED RUNTIME_VALIDATION; return 1; }
  printf 'RUNTIME_VALIDATION=PASS\n'
  # shellcheck disable=SC2086
  python3 "$SOURCE/tools/git_artifact_manifest.py" "$GOVERNANCE_COMMIT" $RUNTIME_ARTIFACTS --repo "$SOURCE" --compare-worktree > "$EVIDENCE_DIR/git-artifacts.json" 2>/dev/null || { fail_action5c VALIDATION_FAIL SOURCE_ARTIFACT_IDENTITY_FAILED RUNTIME_ARTIFACT_IDENTITY; return 1; }
  for rel in $RUNTIME_ARTIFACTS; do
    expected="$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(next(x["sha256"] for x in d["artifacts"] if x["path"]==sys.argv[2]))' "$EVIDENCE_DIR/git-artifacts.json" "$rel" 2>/dev/null)"
    [ -n "$expected" ] && [ -f "$RUNTIME/$rel" ] && [ ! -L "$RUNTIME/$rel" ] && [ "$(sha256sum "$RUNTIME/$rel" 2>/dev/null | awk '{print $1}')" = "$expected" ] || { fail_action5c VALIDATION_FAIL RUNTIME_ARTIFACT_IDENTITY_MISMATCH RUNTIME_ARTIFACT_IDENTITY; return 1; }
  done
  printf 'RUNTIME_ARTIFACT_IDENTITY=PASS\n'
  python3 "$SOURCE/$PROTECTION_TOOL" snapshot --runtime "$RUNTIME" > "$EVIDENCE_DIR/manufacturer-current.json" 2>/dev/null || { fail_action5c VALIDATION_FAIL MANUFACTURER_SNAPSHOT_FAILED MANUFACTURER_PROTECTION; return 1; }
  python3 "$SOURCE/$PROTECTION_TOOL" validate-empty-current --snapshot "$EVIDENCE_DIR/manufacturer-current.json" >/dev/null 2>&1 || { fail_action5c VALIDATION_FAIL MANUFACTURER_PAYLOAD_PRESENT MANUFACTURER_PROTECTION; return 1; }
  python3 -c 'import pathlib,sys
p=pathlib.Path(sys.argv[1]); value=""
for line in p.read_text(encoding="utf-8").splitlines():
 if line.startswith("MANUFACTURER_DB_PATH="): value=line.split("=",1)[1].strip().strip("\"\x27")
raise SystemExit(0 if value=="" else 1)' "$RUNTIME/config/hioc.conf" || { fail_action5c VALIDATION_FAIL CONFIGURATION_ACTIVATED MANUFACTURER_PROTECTION; return 1; }
  printf 'MANUFACTURER_PAYLOAD_UNTOUCHED=PASS\nMANUFACTURER_SCAFFOLDING_STATE=PASS\nCONFIGURATION_UNTOUCHED=PASS\n'
  printf 'ACTION5B_DEPLOYMENT_EVIDENCE=PRESERVED\nEVIDENCE_REPORT=PASS\nEVIDENCE_DIR=%s\nRELEASE_BACKUP_PATH=%s\nACTION5=COMPLETE\nRESULT=PASS\nROLLBACK_RECOMMENDED=FALSE\n' "$EVIDENCE_DIR" "$RELEASE_BACKUP"
}

main() {
  FAILURE_REPORTED=0
  [ "$#" -eq 4 ] && [ "$1" = --governance-commit ] && [ "$3" = --release-backup ] || { fail_action5c INPUT_OR_PRECONDITION_ERROR INVALID_ARGUMENTS INPUT_VALIDATION; return 1; }
  GOVERNANCE_COMMIT=$2
  RELEASE_BACKUP=$4
  printf '%s' "$GOVERNANCE_COMMIT" | grep -Eq '^[0-9a-f]{40}$' || { fail_action5c INPUT_OR_PRECONDITION_ERROR INVALID_GOVERNANCE_COMMIT INPUT_VALIDATION; return 1; }
  case "$RELEASE_BACKUP" in "$RUNTIME"/backups/release-upgrade-*) ;; *) fail_action5c INPUT_OR_PRECONDITION_ERROR INVALID_RELEASE_BACKUP INPUT_VALIDATION; return 1 ;; esac
  verify_source || return 1
  validate_backup || return 1
  revalidate_current || return 1
}

main "$@"
