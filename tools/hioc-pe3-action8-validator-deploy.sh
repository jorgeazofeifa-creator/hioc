#!/usr/bin/env bash

# Governed PE-3 Action 8 corrective validator-only runtime deployment.

SOURCE=/home/jazofv1/hioc-release-source
RUNTIME=/home/jazofv1/hioc
TOOL_REL=tools/hioc-pe3-action8-validator-deploy.sh
VALIDATOR_REL=pi4/bin/hioc-validate-manufacturer.py
VALIDATOR_BLOB=656f64c8c556ef62e149ef036c767cd7fc3736a0
VALIDATOR_SHA256=03f5e4658379fcf6d3093fa36cb8b9fb8a806f27b81777a0a751c647643ff5a2
TARGET="$RUNTIME/$VALIDATOR_REL"
EVIDENCE_DIR=
BACKUP_DIR=
BACKUP_PATH=
TEMP_TARGET=
TARGET_MUTATED=FALSE
FAILURE_REPORTED=0

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

safe_owned_directory() {
  [ -d "$1" ] && [ ! -L "$1" ] &&
    [ "$(stat -c %U:%G "$1" 2>/dev/null)" = jazofv1:jazofv1 ] || return 1
  directory_mode="$(stat -c %a "$1" 2>/dev/null)" || return 1
  [ $((8#$directory_mode & 0022)) -eq 0 ]
}

cleanup_temp() {
  [ -n "$TEMP_TARGET" ] || return 0
  case "$TEMP_TARGET" in "$RUNTIME/pi4/bin/.hioc-validate-manufacturer.py.pe3."*) ;; *) return 1 ;; esac
  [ -e "$TEMP_TARGET" ] || [ -L "$TEMP_TARGET" ] || { TEMP_TARGET=; return 0; }
  [ -f "$TEMP_TARGET" ] && [ ! -L "$TEMP_TARGET" ] || return 1
  rm -- "$TEMP_TARGET" >/dev/null 2>&1 || return 1
  TEMP_TARGET=
}

write_result() {
  [ -n "$EVIDENCE_DIR" ] && owned_directory "$EVIDENCE_DIR" 700 || return 1
  result_temp="$(mktemp "$EVIDENCE_DIR/.deployment-result.XXXXXXXX" 2>/dev/null)" || return 1
  chmod 0600 "$result_temp" || { rm -- "$result_temp" >/dev/null 2>&1; return 1; }
  {
    printf 'RESULT=%s\nERROR_CODE=%s\nFAILURE_STAGE=%s\nROLLBACK_RECOMMENDED=%s\n' "$1" "$2" "$3" "$4"
    [ -z "${DEPLOYMENT_DISPOSITION:-}" ] || printf 'DEPLOYMENT_DISPOSITION=%s\n' "$DEPLOYMENT_DISPOSITION"
    printf 'EVIDENCE_DIR=%s\n' "$EVIDENCE_DIR"
    [ -z "$BACKUP_PATH" ] || printf 'BACKUP_PATH=%s\n' "$BACKUP_PATH"
  } > "$result_temp" || { rm -- "$result_temp" >/dev/null 2>&1; return 1; }
  sync -f "$result_temp" || { rm -- "$result_temp" >/dev/null 2>&1; return 1; }
  mv -fT -- "$result_temp" "$EVIDENCE_DIR/deployment-result.txt" || return 1
  sync -f "$EVIDENCE_DIR/deployment-result.txt" && sync -f "$EVIDENCE_DIR"
}

fail_deployment() {
  FAILURE_REPORTED=1
  result=$1 code=$2 stage=$3 rollback=$4
  if ! cleanup_temp; then
    result=VALIDATION_FAIL code=PUBLICATION_TEMP_CLEANUP_FAILED stage=PUBLICATION_CLEANUP rollback=TRUE
  fi
  write_result "$result" "$code" "$stage" "$rollback" >/dev/null 2>&1 || true
  printf 'RESULT=%s\nERROR_CODE=%s\nFAILURE_STAGE=%s\nROLLBACK_RECOMMENDED=%s\n' "$result" "$code" "$stage" "$rollback"
  [ -z "$EVIDENCE_DIR" ] || printf 'EVIDENCE_DIR=%s\n' "$EVIDENCE_DIR"
  [ -z "$BACKUP_PATH" ] || printf 'BACKUP_PATH=%s\n' "$BACKUP_PATH"
  return 1
}

verify_target_source() {
  [ "$(hostname -s 2>/dev/null)" = nutandpihole ] || { fail_deployment INPUT_OR_PRECONDITION_ERROR WRONG_TARGET TARGET_IDENTITY FALSE; return 1; }
  ip -o -4 addr show scope global 2>/dev/null | awk '{print $4}' | cut -d/ -f1 | grep -Fxq 192.168.100.252 || { fail_deployment INPUT_OR_PRECONDITION_ERROR WRONG_TARGET TARGET_IDENTITY FALSE; return 1; }
  [ "$(id -un 2>/dev/null)" = jazofv1 ] && [ "$(id -gn 2>/dev/null)" = jazofv1 ] || { fail_deployment INPUT_OR_PRECONDITION_ERROR WRONG_OPERATOR TARGET_IDENTITY FALSE; return 1; }
  printf 'TARGET_IDENTITY=PASS\n'
  [ -d "$SOURCE/.git" ] || { fail_deployment INPUT_OR_PRECONDITION_ERROR SOURCE_REPOSITORY_MISSING SOURCE_IDENTITY FALSE; return 1; }
  [ "$(git -C "$SOURCE" branch --show-current 2>/dev/null)" = main ] || { fail_deployment INPUT_OR_PRECONDITION_ERROR WRONG_BRANCH SOURCE_IDENTITY FALSE; return 1; }
  [ -z "$(git -C "$SOURCE" status --porcelain 2>/dev/null)" ] || { fail_deployment INPUT_OR_PRECONDITION_ERROR SOURCE_REPOSITORY_DIRTY SOURCE_IDENTITY FALSE; return 1; }
  active_git_operation && { fail_deployment INPUT_OR_PRECONDITION_ERROR ACTIVE_GIT_OPERATION SOURCE_IDENTITY FALSE; return 1; }
  [ "$(git -C "$SOURCE" rev-parse HEAD 2>/dev/null)" = "$GOVERNANCE_COMMIT" ] || { fail_deployment INPUT_OR_PRECONDITION_ERROR GOVERNANCE_HEAD_MISMATCH SOURCE_IDENTITY FALSE; return 1; }
  [ "$(git -C "$SOURCE" rev-parse origin/main 2>/dev/null)" = "$GOVERNANCE_COMMIT" ] || { fail_deployment INPUT_OR_PRECONDITION_ERROR ORIGIN_MAIN_MISMATCH SOURCE_IDENTITY FALSE; return 1; }
  for rel in "$TOOL_REL" "$VALIDATOR_REL"; do
    [ -f "$SOURCE/$rel" ] && [ ! -L "$SOURCE/$rel" ] || { fail_deployment INPUT_OR_PRECONDITION_ERROR SOURCE_ARTIFACT_UNSAFE SOURCE_IDENTITY FALSE; return 1; }
    expected="$(git -C "$SOURCE" rev-parse "$GOVERNANCE_COMMIT:$rel" 2>/dev/null)" || { fail_deployment INPUT_OR_PRECONDITION_ERROR SOURCE_GIT_IDENTITY_MISMATCH SOURCE_IDENTITY FALSE; return 1; }
    actual="$(git -C "$SOURCE" hash-object --path="$rel" "$SOURCE/$rel" 2>/dev/null)" || { fail_deployment INPUT_OR_PRECONDITION_ERROR SOURCE_WORKTREE_IDENTITY_MISMATCH SOURCE_IDENTITY FALSE; return 1; }
    [ "$actual" = "$expected" ] && git -C "$SOURCE" diff --quiet -- "$rel" || { fail_deployment INPUT_OR_PRECONDITION_ERROR SOURCE_WORKTREE_IDENTITY_MISMATCH SOURCE_IDENTITY FALSE; return 1; }
  done
  printf 'SOURCE_IDENTITY=PASS\n'
  [ "$expected" = "$VALIDATOR_BLOB" ] && [ "$(sha256sum "$SOURCE/$VALIDATOR_REL" 2>/dev/null | awk '{print $1}')" = "$VALIDATOR_SHA256" ] || { fail_deployment INPUT_OR_PRECONDITION_ERROR SOURCE_VALIDATOR_IDENTITY_MISMATCH SOURCE_VALIDATOR_IDENTITY FALSE; return 1; }
  python3 -c 'import pathlib,sys; compile(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"),sys.argv[1],"exec")' "$SOURCE/$VALIDATOR_REL" >/dev/null 2>&1 || { fail_deployment INPUT_OR_PRECONDITION_ERROR SOURCE_VALIDATOR_INVALID SOURCE_VALIDATOR_IDENTITY FALSE; return 1; }
  printf 'SOURCE_VALIDATOR_IDENTITY=PASS\n'
}

prepare_evidence() {
  EVIDENCE_DIR="$(mktemp -d /tmp/hioc-pe3-action8-validator-deploy-XXXXXXXX 2>/dev/null)" || { fail_deployment INPUT_OR_PRECONDITION_ERROR EVIDENCE_CREATE_FAILED EVIDENCE_PREPARATION FALSE; return 1; }
  chmod 0700 "$EVIDENCE_DIR" && owned_directory "$EVIDENCE_DIR" 700 || { fail_deployment INPUT_OR_PRECONDITION_ERROR EVIDENCE_PERMISSION_FAILED EVIDENCE_PREPARATION FALSE; return 1; }
  printf 'EVIDENCE_PREPARATION=PASS\n'
}

snapshot_protected() {
  python3 - "$RUNTIME" "$1" <<'PY'
import grp, hashlib, json, os, pathlib, pwd, stat, sys
root, target = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
config = root / "config/hioc.conf"
values=[]
for line in config.read_text(encoding="utf-8").splitlines():
    if line.startswith("MANUFACTURER_DB_PATH="):
        value=line.split("=",1)[1].strip()
        if len(value)>=2 and value[0]==value[-1] and value[0] in "\"'": value=value[1:-1]
        values.append(value)
if len(values)!=1: raise SystemExit(2)
db=pathlib.Path(values[0]); expected=root/"data/manufacturer/versions/local-ieee-ra--2026-08-11-r1/manufacturer-db.json"
if db != expected: raise SystemExit(3)
paths=[config,root/"state/inventory/inventory.json",root/"state/inventory/manufacturer.json",root/"state/inventory/manufacturer_status.json",db,db.parent/"manufacturer-db.manifest.json"]
records=[]
for path in paths:
    info=path.lstat()
    if path.is_symlink() or not stat.S_ISREG(info.st_mode): raise SystemExit(4)
    mode=stat.S_IMODE(info.st_mode); rel=str(path.relative_to(root))
    if pwd.getpwuid(info.st_uid).pw_name!="jazofv1" or grp.getgrgid(info.st_gid).gr_name!="jazofv1": raise SystemExit(5)
    if rel=="state/inventory/inventory.json":
        if mode & 0o022: raise SystemExit(6)
    elif mode != 0o600: raise SystemExit(7)
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    records.append({"path":rel,"type":"regular","owner":"jazofv1","group":"jazofv1","mode":format(mode,"04o"),"size":info.st_size,"sha256":digest})
data=(json.dumps({"schema_version":"1.0","protected":records},sort_keys=True,separators=(",",":"))+"\n").encode()
fd=os.open(target,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
with os.fdopen(fd,"wb") as handle: handle.write(data); handle.flush(); os.fsync(handle.fileno())
PY
}

verify_runtime_prestate() {
  [ -d "$RUNTIME" ] && [ ! -L "$RUNTIME" ] && safe_owned_directory "$RUNTIME" && safe_owned_directory "$RUNTIME/pi4/bin" && safe_owned_directory "$RUNTIME/backups" || { fail_deployment INPUT_OR_PRECONDITION_ERROR RUNTIME_ROOT_UNSAFE RUNTIME_PRECONDITION FALSE; return 1; }
  [ -e "$TARGET" ] || [ -L "$TARGET" ] || { fail_deployment INPUT_OR_PRECONDITION_ERROR RUNTIME_VALIDATOR_MISSING RUNTIME_PRECONDITION FALSE; return 1; }
  owned_file "$TARGET" 700 || { fail_deployment INPUT_OR_PRECONDITION_ERROR RUNTIME_VALIDATOR_UNSAFE RUNTIME_PRECONDITION FALSE; return 1; }
  RUNTIME_SHA_BEFORE="$(sha256sum "$TARGET" 2>/dev/null | awk '{print $1}')"
  [ -n "$RUNTIME_SHA_BEFORE" ] || { fail_deployment INPUT_OR_PRECONDITION_ERROR RUNTIME_VALIDATOR_UNHASHABLE RUNTIME_PRECONDITION FALSE; return 1; }
  printf 'RUNTIME_PRECONDITION=PASS\n'
  snapshot_protected "$EVIDENCE_DIR/protected-pre.json" && owned_file "$EVIDENCE_DIR/protected-pre.json" 600 && sync -f "$EVIDENCE_DIR" || { fail_deployment INPUT_OR_PRECONDITION_ERROR PROTECTED_PRE_STATE_INVALID PROTECTED_PRE_STATE FALSE; return 1; }
  printf 'PROTECTED_PRE_STATE=PASS\n'
}

create_backup() {
  BACKUP_DIR="$(mktemp -d "$RUNTIME/backups/pe3-action8-validator-deploy-XXXXXXXX" 2>/dev/null)" || { fail_deployment VALIDATION_FAIL BACKUP_CREATE_FAILED BACKUP FALSE; return 1; }
  chmod 0700 "$BACKUP_DIR" && owned_directory "$BACKUP_DIR" 700 || { fail_deployment VALIDATION_FAIL BACKUP_PERMISSION_FAILED BACKUP FALSE; return 1; }
  BACKUP_PATH="$BACKUP_DIR/hioc-validate-manufacturer.py"
  install -o jazofv1 -g jazofv1 -m 0700 -- "$TARGET" "$BACKUP_PATH" || { fail_deployment VALIDATION_FAIL BACKUP_COPY_FAILED BACKUP FALSE; return 1; }
  owned_file "$BACKUP_PATH" 700 && [ "$(sha256sum "$BACKUP_PATH" | awk '{print $1}')" = "$RUNTIME_SHA_BEFORE" ] || { fail_deployment VALIDATION_FAIL BACKUP_IDENTITY_FAILED BACKUP FALSE; return 1; }
  sync -f "$BACKUP_PATH" && sync -f "$BACKUP_DIR" && sync -f "$RUNTIME/backups" || { fail_deployment VALIDATION_FAIL BACKUP_FSYNC_FAILED BACKUP FALSE; return 1; }
  printf 'BACKUP=PASS\nBACKUP_PATH=%s\n' "$BACKUP_PATH"
}

publish_validator() {
  TEMP_TARGET="$(mktemp "$RUNTIME/pi4/bin/.hioc-validate-manufacturer.py.pe3.XXXXXXXX" 2>/dev/null)" || { fail_deployment VALIDATION_FAIL PUBLICATION_TEMP_CREATE_FAILED VALIDATOR_PUBLICATION FALSE; return 1; }
  install -o jazofv1 -g jazofv1 -m 0700 -- "$SOURCE/$VALIDATOR_REL" "$TEMP_TARGET" || { fail_deployment VALIDATION_FAIL PUBLICATION_TEMP_COPY_FAILED VALIDATOR_PUBLICATION FALSE; return 1; }
  owned_file "$TEMP_TARGET" 700 && [ "$(sha256sum "$TEMP_TARGET" | awk '{print $1}')" = "$VALIDATOR_SHA256" ] || { fail_deployment VALIDATION_FAIL PUBLICATION_TEMP_IDENTITY_FAILED VALIDATOR_PUBLICATION FALSE; return 1; }
  sync -f "$TEMP_TARGET" || { fail_deployment VALIDATION_FAIL PUBLICATION_TEMP_FSYNC_FAILED VALIDATOR_PUBLICATION FALSE; return 1; }
  mv -fT -- "$TEMP_TARGET" "$TARGET" || { fail_deployment VALIDATION_FAIL ATOMIC_PUBLICATION_FAILED VALIDATOR_PUBLICATION FALSE; return 1; }
  TEMP_TARGET=
  TARGET_MUTATED=TRUE
  sync -f "$TARGET" && sync -f "$RUNTIME/pi4/bin" || { fail_deployment VALIDATION_FAIL PUBLICATION_FSYNC_FAILED VALIDATOR_PUBLICATION TRUE; return 1; }
  printf 'VALIDATOR_PUBLICATION=PASS\n'
}

verify_final() {
  owned_file "$TARGET" 700 && [ "$(sha256sum "$TARGET" 2>/dev/null | awk '{print $1}')" = "$VALIDATOR_SHA256" ] && cmp -s "$SOURCE/$VALIDATOR_REL" "$TARGET" || { fail_deployment VALIDATION_FAIL FINAL_RUNTIME_VALIDATOR_IDENTITY_FAILED RUNTIME_VALIDATOR_IDENTITY TRUE; return 1; }
  printf 'RUNTIME_VALIDATOR_IDENTITY=PASS\nSOURCE_RUNTIME_EQUALITY=PASS\n'
  snapshot_protected "$EVIDENCE_DIR/protected-post.json" && owned_file "$EVIDENCE_DIR/protected-post.json" 600 || { fail_deployment VALIDATION_FAIL PROTECTED_POST_STATE_INVALID PROTECTED_POST_STATE TRUE; return 1; }
  cmp -s "$EVIDENCE_DIR/protected-pre.json" "$EVIDENCE_DIR/protected-post.json" || { fail_deployment VALIDATION_FAIL PROTECTED_STATE_CHANGED PROTECTED_POST_STATE TRUE; return 1; }
  sync -f "$EVIDENCE_DIR/protected-post.json" && sync -f "$EVIDENCE_DIR" || { fail_deployment VALIDATION_FAIL EVIDENCE_FSYNC_FAILED PROTECTED_POST_STATE TRUE; return 1; }
  printf 'PROTECTED_POST_STATE=PASS\n'
}

main() {
  [ "$#" -eq 2 ] && [ "$1" = --governance-commit ] || { fail_deployment INPUT_OR_PRECONDITION_ERROR INVALID_ARGUMENTS INPUT_VALIDATION FALSE; return 1; }
  GOVERNANCE_COMMIT=$2
  printf '%s' "$GOVERNANCE_COMMIT" | grep -Eq '^[0-9a-f]{40}$' || { fail_deployment INPUT_OR_PRECONDITION_ERROR INVALID_GOVERNANCE_COMMIT INPUT_VALIDATION FALSE; return 1; }
  verify_target_source || return 1
  prepare_evidence || return 1
  verify_runtime_prestate || return 1
  if [ "$RUNTIME_SHA_BEFORE" = "$VALIDATOR_SHA256" ] && cmp -s "$SOURCE/$VALIDATOR_REL" "$TARGET"; then
    printf 'BACKUP=NOT_REQUIRED\nVALIDATOR_PUBLICATION=NOT_REQUIRED\n'
    DEPLOYMENT_DISPOSITION=NOOP_IDENTICAL
  else
    create_backup || return 1
    publish_validator || return 1
    DEPLOYMENT_DISPOSITION=REPLACED
  fi
  verify_final || return 1
  write_result PASS NONE COMPLETE FALSE || { fail_deployment VALIDATION_FAIL EVIDENCE_RESULT_PUBLICATION_FAILED EVIDENCE_REPORT "$TARGET_MUTATED"; return 1; }
  printf 'DEPLOYMENT_DISPOSITION=%s\nEVIDENCE_REPORT=PASS\nEVIDENCE_DIR=%s\nRESULT=PASS\nROLLBACK_RECOMMENDED=FALSE\n' "$DEPLOYMENT_DISPOSITION" "$EVIDENCE_DIR"
}

deployment_entry() {
  main "$@"
  status=$?
  if [ "$status" -ne 0 ] && [ "$FAILURE_REPORTED" -ne 1 ]; then
    fail_deployment VALIDATION_FAIL VALIDATOR_DEPLOYMENT_UNEXPECTED VALIDATOR_DEPLOYMENT "$TARGET_MUTATED"
    status=$?
  fi
  return "$status"
}

deployment_entry "$@"
