#!/usr/bin/env bash
set -Eeuo pipefail
set +x
umask 077

APPROVED_IMPL="dd6f40b113fe8a395babc8bfb2325262879b8454"
OPERATOR_COMMIT="${HIOC_PE2_OPERATOR_COMMIT:-}"
SOURCE="/home/jazofv1/hioc-release-source"
RUNTIME="/home/jazofv1/hioc"
KNOWN_RELEASE_BACKUP="/home/jazofv1/hioc/backups/release-upgrade-20260803-205823"
EXPECTED_HOST="nutandpihole"
EXPECTED_IP="192.168.100.252"
SYNTHETIC_ID="dev_0000000000000000"
if [ "${1:-}" != "--revalidate-existing-deployment" ] || [ "$#" -ne 1 ]; then
  printf 'RESULT=INPUT_OR_PRECONDITION_ERROR\nROLLBACK_RECOMMENDED=FALSE\n'
  exit 20
fi
ARTIFACT_CONTRACT_REL="pi4/config/pe2_artifacts.json"
ARTIFACTS=()
OPERATOR_ARTIFACTS=(tools/hioc-pe2-production-validate.sh tools/validate_pe2_artifacts.py tools/validate_pe2_incident_contract.py tools/hioc-pe2-clean-synthetic-backups.py tools/render_pe2_evidence.py pi4/config/pe2_artifacts.json)
PUBLIC_FILES=(inventory.json devices.json services.json topology.json dependencies.json summary.json status.json enrichment.json enrichment_status.json)
INCIDENT_FILES=(active.json history.json summary.json)
MQTT_SUFFIXES=(inventory inventory/devices inventory/services inventory/topology inventory/dependencies inventory/summary inventory/status)

EVIDENCE=""
DEPLOYMENT_STARTED=0
DEPLOYMENT_STATUS="NOT_STARTED"
RESULT="INPUT_OR_PRECONDITION_ERROR"
ROLLBACK_RECOMMENDED="FALSE"
ROLLBACK_COMMAND="NONE"
WARNINGS=()
CREATED_BACKUPS=()
INITIAL_STATE="UNKNOWN"
FINAL_STATE="UNKNOWN"
SYNTHETIC_RESULT="NOT_RUN"
PUBLIC_INVARIANTS="NOT_RUN"
PRIVACY_RESULT="NOT_RUN"
PERFORMANCE_RESULT="NOT_RUN"
INCIDENT_CLASSIFICATION="NOT_RUN"
CAUSAL_REGRESSION="FALSE"
SYNTHETIC_CLEANUP_STATUS="NOT_CHECKED"

say() { printf '%s\n' "$*"; }
die_pre() { say "ERROR_CODE=$1" >&2; say "ERROR_MESSAGE=$2" >&2; exit 20; }
die_fail() {
  RESULT="FAIL"
  local rollback_worthy="${3:-TRUE}"
  if [ "$DEPLOYMENT_STARTED" -eq 1 ] && [ "$rollback_worthy" = TRUE ]; then ROLLBACK_RECOMMENDED="TRUE"; fi
  say "ERROR_CODE=$1" >&2; say "ERROR_MESSAGE=$2" >&2; exit 30
}
die_validation() {
  RESULT="VALIDATION_FAIL"
  ROLLBACK_RECOMMENDED="FALSE"
  say "ERROR_CODE=$1" >&2
  say "ERROR_MESSAGE=$2" >&2
  exit 40
}
require() { command -v "$1" >/dev/null 2>&1 || die_pre "MISSING_COMMAND" "required command is unavailable: $1"; }
sha() { sha256sum "$1" | awk '{print $1}'; }
mode() { stat -c '%a' "$1"; }
owner() { stat -c '%U:%G' "$1"; }
redact_id() { printf '%s' "$1" | sha256sum | cut -c1-12; }
json_get() { python3 - "$1" "$2" <<'PY'
import json,sys
v=json.load(open(sys.argv[1],encoding="utf-8"))
for part in sys.argv[2].split('.'):
    v=v[int(part)] if isinstance(v,list) else v[part]
if isinstance(v,bool): print(str(v).lower())
elif v is None: print("null")
elif isinstance(v,(dict,list)): print(json.dumps(v,separators=(",",":"),sort_keys=True))
else: print(v)
PY
}
semantic_digest() { python3 - "$1" <<'PY'
import hashlib,json,sys
p=json.load(open(sys.argv[1],encoding="utf-8")); p.pop("updated_at",None)
print(hashlib.sha256(json.dumps(p,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest())
PY
}
sanitized_asset_summary() { python3 - "$1" <<'PY'
import hashlib,json,sys
p=json.load(open(sys.argv[1],encoding="utf-8")); rows=[]
for key,r in sorted(p.get("assets",{}).items()):
 rows.append({"device_id_digest":hashlib.sha256(key.encode()).hexdigest()[:12],"revision":r["revision"],"populated_fields":[f for f in ("friendly_name","physical_location","purpose","notes") if r[f] is not None]})
print(json.dumps({"schema_version":p.get("schema_version"),"asset_count":p.get("asset_count"),"records":rows},sort_keys=True))
PY
}
canonical_json_digest() { python3 - "$1" <<'PY'
import hashlib,json,sys
p=json.load(open(sys.argv[1],encoding="utf-8"))
def clean(v):
 if isinstance(v,dict): return {k:clean(x) for k,x in sorted(v.items()) if k not in {"updated","updated_at","generated_at","timestamp","last_seen","last_changed"}}
 if isinstance(v,list): return [clean(x) for x in v]
 return v
print(hashlib.sha256(json.dumps(clean(p),sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest())
PY
}

write_report() {
  [ -n "$EVIDENCE" ] || return 0
  local warning_json repository_head origin_head artifact_state schema_state permission_state
  warning_json="$(printf '%s\n' "${WARNINGS[@]:-}" | jq -Rsc 'split("\n") | map(select(length>0))')"
  repository_head="$(git -C "$SOURCE" rev-parse HEAD 2>/dev/null || printf unavailable)"
  origin_head="$(git -C "$SOURCE" rev-parse origin/main 2>/dev/null || printf unavailable)"
  artifact_state="$(test -f "$EVIDENCE/artifact-post.ok" && printf PASS || printf NOT_PASS)"
  schema_state="$(test -f "$EVIDENCE/asset-validator-post.json" && printf PASS || printf NOT_RUN)"
  permission_state="$(test -f "$EVIDENCE/permissions.ok" && printf PASS || printf NOT_PASS)"
  jq -n \
    --arg checkpoint "Phase 7A PE-2.1 Asset Foundation production validation" \
    --arg target_host "$EXPECTED_HOST" --arg target_ip "$EXPECTED_IP" \
    --arg approved_commit "$APPROVED_IMPL" --arg source "$SOURCE" \
    --arg head "$repository_head" --arg origin_main "$origin_head" \
    --arg deployment_started "$DEPLOYMENT_STARTED" --arg deployment_status "$DEPLOYMENT_STATUS" \
    --arg artifact_identity "$artifact_state" --arg initial "$INITIAL_STATE" --arg final "$FINAL_STATE" \
    --arg schema "$schema_state" --arg permissions "$permission_state" \
    --arg synthetic "$SYNTHETIC_RESULT" --arg invariants "$PUBLIC_INVARIANTS" \
    --arg privacy "$PRIVACY_RESULT" --arg performance "$PERFORMANCE_RESULT" --arg incident "$INCIDENT_CLASSIFICATION" --arg causal "$CAUSAL_REGRESSION" --arg cleanup "$SYNTHETIC_CLEANUP_STATUS" \
    --arg result "$RESULT" --arg rollback "$ROLLBACK_RECOMMENDED" \
    --arg rollback_command "$ROLLBACK_COMMAND" --argjson warnings "$warning_json" \
    '{checkpoint:$checkpoint,target:{hostname:$target_host,infrastructure_ip:$target_ip},approved_commit:$approved_commit,repository:{source:$source,head:$head,origin_main:$origin_main},deployment:{started:($deployment_started=="1"),status:$deployment_status},artifact_identity:$artifact_identity,initial_asset_state:$initial,final_asset_state:$final,asset_schema:$schema,status_schema:$schema,permissions:$permissions,synthetic_validation:$synthetic,revision_validation:$synthetic,backup_validation:$synthetic,restore_validation:$synthetic,rejection_tests:$synthetic,lock_validation:$synthetic,orphan_validation:$synthetic,synthetic_cleanup:$cleanup,public_invariants:$invariants,mqtt_contract:$invariants,pe1_enrichment_invariant:$invariants,incident_classification:$incident,causal_regression_demonstrated:($causal=="TRUE"),privacy:$privacy,performance:$performance,warnings:$warnings,result:$result,rollback_recommended:($rollback=="TRUE"),rollback_command:(if $rollback_command=="NONE" then null else $rollback_command end)}' \
    | python3 "$SOURCE/tools/render_pe2_evidence.py" > "$EVIDENCE/EVIDENCE_REPORT.json"
  (cd "$EVIDENCE" && find . -type f ! -name EVIDENCE_CHECKSUMS.sha256 -print0 | sort -z | xargs -0 sha256sum > EVIDENCE_CHECKSUMS.sha256)
}
finish() {
  rc=$?
  if [ "$rc" -ne 0 ] && [ "$RESULT" != "FAIL" ]; then
    if [ "$DEPLOYMENT_STARTED" -eq 1 ]; then RESULT="VALIDATION_FAIL"; else RESULT="INPUT_OR_PRECONDITION_ERROR"; fi
    ROLLBACK_RECOMMENDED="FALSE"
  fi
  if [ "$RESULT" = "FAIL" ] && [ "$DEPLOYMENT_STARTED" -eq 1 ] && [ "$ROLLBACK_RECOMMENDED" = TRUE ] && [ -d "$KNOWN_RELEASE_BACKUP/current" ]; then
    ROLLBACK_COMMAND="cd $SOURCE && HIOC_INSTALL_DIR=$RUNTIME bash release/rollback.sh $KNOWN_RELEASE_BACKUP"
  fi
  write_report || true
  say "EVIDENCE_DIR=${EVIDENCE:-NOT_CREATED}"
  say "DEPLOYMENT_STATUS=$DEPLOYMENT_STATUS"
  say "IMPLEMENTATION_STATUS=REPOSITORY_VALIDATED"
  say "VALIDATOR_STATUS=$SYNTHETIC_RESULT"
  say "PROTECTED_INVARIANT_STATUS=$PUBLIC_INVARIANTS"
  say "INCIDENT_CLASSIFICATION=$INCIDENT_CLASSIFICATION"
  say "CAUSAL_REGRESSION_DEMONSTRATED=$CAUSAL_REGRESSION"
  say "PRIVACY_STATUS=$PRIVACY_RESULT"
  say "SYNTHETIC_CLEANUP_STATUS=$SYNTHETIC_CLEANUP_STATUS"
  say "RESULT=$RESULT"
  say "ROLLBACK_RECOMMENDED=$ROLLBACK_RECOMMENDED"
  say "ROLLBACK_COMMAND=$ROLLBACK_COMMAND"
  exit "$rc"
}
trap finish EXIT

for cmd in git python3 sha256sum stat find jq mktemp timeout hostname ip diff awk sed grep flock readlink; do require "$cmd"; done
[[ "$OPERATOR_COMMIT" =~ ^[0-9a-f]{40}$ ]] || die_pre "OPERATOR_COMMIT_MISSING" "approved operator governance commit was not supplied"

actual_host="$(hostname -s)"
fqdn="$(hostname -f 2>/dev/null || hostname)"
ipv4="$(ip -o -4 addr show scope global | awk '{print $4}' | cut -d/ -f1 | sort -u | paste -sd, -)"
say "TARGET_HOSTNAME=$actual_host"
say "TARGET_FQDN=$fqdn"
say "TARGET_GLOBAL_IPV4=$ipv4"
[ "$actual_host" = "$EXPECTED_HOST" ] || die_pre "WRONG_TARGET" "hostname does not match nutandpihole"
printf '%s\n' "$ipv4" | tr ',' '\n' | grep -Fxq "$EXPECTED_IP" || die_pre "WRONG_TARGET" "expected PI3 address is absent"
say "Type nutandpihole to confirm the target:"
read -r confirmed_host </dev/tty
[ "$confirmed_host" = "$EXPECTED_HOST" ] || die_pre "TARGET_NOT_CONFIRMED" "interactive target confirmation failed"

[ -d "$SOURCE/.git" ] || die_pre "SOURCE_NOT_GIT" "release-source Git repository is missing"
[ "$(git -C "$SOURCE" branch --show-current)" = main ] || die_pre "WRONG_BRANCH" "release-source branch is not main"
[ -z "$(git -C "$SOURCE" status --porcelain=v1 --untracked-files=all)" ] || die_pre "DIRTY_REPOSITORY" "release-source working tree is dirty"
gitdir="$(git -C "$SOURCE" rev-parse --git-dir)"
for marker in MERGE_HEAD CHERRY_PICK_HEAD REVERT_HEAD BISECT_START rebase-merge rebase-apply; do [ ! -e "$gitdir/$marker" ] || die_pre "ACTIVE_GIT_OPERATION" "release-source has an active Git operation"; done
git -C "$SOURCE" fetch origin
operator_commit="$(git -C "$SOURCE" rev-parse origin/main)"
[ "$operator_commit" = "$OPERATOR_COMMIT" ] || die_pre "ORIGIN_MAIN_MISMATCH" "origin/main does not equal the approved operator governance commit"
git -C "$SOURCE" merge --ff-only origin/main
[ "$(git -C "$SOURCE" rev-parse HEAD)" = "$operator_commit" ] || die_pre "SOURCE_HEAD_MISMATCH" "HEAD does not equal origin/main"
git -C "$SOURCE" merge-base --is-ancestor "$APPROVED_IMPL" HEAD || die_pre "IMPLEMENTATION_NOT_ANCESTOR" "approved implementation is not in deployed source history"
[ -z "$(git -C "$SOURCE" status --porcelain=v1 --untracked-files=all)" ] || die_pre "DIRTY_REPOSITORY" "release-source became dirty"

EVIDENCE="$(mktemp -d /tmp/hioc-pe2-production-validation-XXXXXXXX)"
chmod 0700 "$EVIDENCE"
{
  printf 'hostname=%s\nfqdn=%s\nglobal_ipv4=%s\n' "$actual_host" "$fqdn" "$ipv4"
  git -C "$SOURCE" rev-parse HEAD
  git -C "$SOURCE" rev-parse origin/main
  git -C "$SOURCE" status --porcelain=v1 --untracked-files=all
} > "$EVIDENCE/target-and-repository.txt"

mapfile -t ARTIFACTS < <(jq -r '.artifacts[].path' "$SOURCE/$ARTIFACT_CONTRACT_REL")
[ "${#ARTIFACTS[@]}" -gt 0 ] || die_pre "RUNTIME_PERMISSION_CONTRACT_INVALID" "PE-2 artifact permission contract is empty"
python3 "$SOURCE/tools/git_artifact_manifest.py" "$APPROVED_IMPL" "${ARTIFACTS[@]}" --repo "$SOURCE" > "$EVIDENCE/artifact-manifest.json"
jq -e --arg c "$APPROVED_IMPL" '.commit==$c and .generated_from_git_objects' "$EVIDENCE/artifact-manifest.json" >/dev/null || die_pre "SOURCE_ARTIFACT_MISMATCH" "Git-object identity generation failed"
python3 "$SOURCE/tools/git_artifact_manifest.py" HEAD "${OPERATOR_ARTIFACTS[@]}" --repo "$SOURCE" --compare-worktree > "$EVIDENCE/operator-artifact-manifest.json"
jq -e '.generated_from_git_objects and all(.artifacts[];.working_tree_equal==true)' "$EVIDENCE/operator-artifact-manifest.json" >/dev/null || die_pre "OPERATOR_ARTIFACT_MISMATCH" "operator-script Git identity failed"

mkdir -p "$EVIDENCE/pre/public" "$EVIDENCE/pre/mqtt" "$EVIDENCE/pre/assets" "$EVIDENCE/post/public" "$EVIDENCE/post/mqtt"
{
  for path in "$RUNTIME/state/inventory" "$RUNTIME/state/inventory/assets.json" "$RUNTIME/state/inventory/assets_status.json" "$RUNTIME/backups/assets"; do
    if [ -e "$path" ] || [ -L "$path" ]; then stat -c '%n mode=%a owner=%U:%G type=%F' "$path"; else printf '%s ABSENT\n' "$path"; fi
  done
} > "$EVIDENCE/pre/path-metadata.txt"
for artifact in "${ARTIFACTS[@]}"; do if [ -f "$RUNTIME/$artifact" ]; then printf '%s %s\n' "$(sha "$RUNTIME/$artifact")" "$artifact"; else printf 'ABSENT %s\n' "$artifact"; fi; done > "$EVIDENCE/pre/runtime-artifacts.sha256"
if [ -e "$RUNTIME/state/inventory/assets.json" ]; then
  [ ! -L "$RUNTIME/state/inventory/assets.json" ] || die_pre "ASSET_STORE_SYMLINK" "Asset store is a symlink"
  cp --preserve=mode,timestamps "$RUNTIME/state/inventory/assets.json" "$EVIDENCE/pre/assets/assets.json"
  PYTHONPATH="$SOURCE/pi4/lib" python3 - "$RUNTIME" <<'PY' > "$EVIDENCE/pre/asset-validator.json" || die_pre "MALFORMED_ASSET_STORE" "existing Asset state is not valid"
import json,sys
from pathlib import Path
from hioc.assets import validate_store,validate_status
root=Path(sys.argv[1]); store=validate_store(json.load(open(root/"state/inventory/assets.json",encoding="utf-8")))
status=validate_status(json.load(open(root/"state/inventory/assets_status.json",encoding="utf-8")))
assert store["asset_count"]==status["asset_count"]
print(json.dumps({"result":"PASS","asset_count":store["asset_count"],"status":status["status"]},sort_keys=True))
PY
  INITIAL_STATE="VALID_EXISTING"
  sha "$EVIDENCE/pre/assets/assets.json" > "$EVIDENCE/pre/asset-byte.sha256"
  semantic_digest "$EVIDENCE/pre/assets/assets.json" > "$EVIDENCE/pre/asset-semantic.sha256"
  sanitized_asset_summary "$EVIDENCE/pre/assets/assets.json" > "$EVIDENCE/pre/asset-summary.json"
  [ -e "$RUNTIME/state/inventory/assets_status.json" ] && cp --preserve=mode,timestamps "$RUNTIME/state/inventory/assets_status.json" "$EVIDENCE/pre/assets/assets_status.json"
else
  [ ! -e "$RUNTIME/state/inventory/assets_status.json" ] || die_pre "UNPAIRED_ASSET_STATUS" "Asset status exists without Asset store"
  INITIAL_STATE="UNINITIALIZED"
fi
if [ -d "$RUNTIME/backups/assets" ]; then find "$RUNTIME/backups/assets" -maxdepth 1 -type f -printf '%f\n' | sort > "$EVIDENCE/pre/backup-inventory.txt"; else : > "$EVIDENCE/pre/backup-inventory.txt"; fi
for name in "${PUBLIC_FILES[@]}"; do path="$RUNTIME/state/inventory/$name"; if [ -f "$path" ]; then cp "$path" "$EVIDENCE/pre/public/$name"; canonical_json_digest "$path" > "$EVIDENCE/pre/public/$name.semantic.sha256"; fi; done
mkdir -p "$EVIDENCE/pre/incidents" "$EVIDENCE/post/incidents"
for name in "${INCIDENT_FILES[@]}"; do path="$RUNTIME/state/incidents/$name"; if [ -f "$path" ]; then cp "$path" "$EVIDENCE/pre/incidents/$name"; canonical_json_digest "$path" > "$EVIDENCE/pre/incidents/$name.semantic.sha256"; fi; done

MQTT_AVAILABLE=0
if command -v mosquitto_sub >/dev/null 2>&1; then
  set +u
  set +x
  [ -f "$RUNTIME/config/hioc.conf" ] && source "$RUNTIME/config/hioc.conf"
  [ -f /home/jazofv1/pi4-tools/config/toolkit.conf ] && source /home/jazofv1/pi4-tools/config/toolkit.conf
  set -u
  mqtt_host="${MQTT_HOST:-}"; mqtt_port="${MQTT_PORT:-1883}"; mqtt_base="${HIOC_BASE_TOPIC:-home/infrastructure/hioc}"
  if [ -n "$mqtt_host" ]; then
    mqtt_args=(-h "$mqtt_host" -p "$mqtt_port" -C 1 -W 5)
    [ -n "${MQTT_USER:-}" ] && mqtt_args+=(-u "$MQTT_USER")
    [ -n "${MQTT_PASSWORD:-}" ] && mqtt_args+=(-P "$MQTT_PASSWORD")
    MQTT_AVAILABLE=1
    for suffix in "${MQTT_SUFFIXES[@]}"; do mosquitto_sub "${mqtt_args[@]}" -t "$mqtt_base/$suffix" > "$EVIDENCE/pre/mqtt/${suffix//\//_}.payload"; done
    if mosquitto_sub "${mqtt_args[@]}" -t "$mqtt_base/assets/#" > "$EVIDENCE/pre/mqtt/assets.payload" 2>/dev/null; then [ ! -s "$EVIDENCE/pre/mqtt/assets.payload" ] || die_pre "ASSET_MQTT_EXISTS" "an Asset MQTT topic exists before deployment"; fi
  else WARNINGS+=("MQTT configuration unavailable; MQTT invariant optional observation not captured"); fi
else WARNINGS+=("mosquitto_sub unavailable; MQTT invariant optional observation not captured"); fi

(cd "$SOURCE" && bash release/validate.sh) > "$EVIDENCE/release-validation.log" 2>&1 || die_pre "RELEASE_VALIDATION_FAILED" "repository release validation failed"
(cd "$SOURCE" && python3 -m unittest tests.test_assets_schema tests.test_assets_store tests.test_assets_cli tests.test_assets_orphans tests.test_assets_release) > "$EVIDENCE/focused-tests.log" 2>&1 || die_pre "FOCUSED_TESTS_FAILED" "PE-2 focused tests failed"

DEPLOYMENT_STARTED=1
DEPLOYMENT_STATUS="DEPLOYED_EXISTING_REVALIDATION"
say "REVALIDATION_MODE=TRUE"

set +e
python3 "$SOURCE/tools/validate_pe2_artifacts.py" --contract "$SOURCE/$ARTIFACT_CONTRACT_REL" --git-manifest "$EVIDENCE/artifact-manifest.json" --runtime-root "$RUNTIME" > "$EVIDENCE/artifact-runtime.json"
artifact_rc=$?
set -e
if [ "$artifact_rc" -ne 0 ]; then
  artifact_error="$(jq -r '.error_code // "VALIDATOR_INTERNAL_ERROR"' "$EVIDENCE/artifact-runtime.json" 2>/dev/null || printf VALIDATOR_INTERNAL_ERROR)"
  case "$artifact_error" in
    RUNTIME_ARTIFACT_MISMATCH) die_fail "RUNTIME_ARTIFACT_MISMATCH" "deployed runtime bytes differ from approved Git objects" ;;
    RUNTIME_PERMISSION_MISMATCH|RUNTIME_OWNERSHIP_MISMATCH) die_fail "$artifact_error" "deployed runtime permission policy failed" ;;
    *) die_validation "VALIDATOR_INTERNAL_ERROR" "artifact validator procedure failed" ;;
  esac
fi
touch "$EVIDENCE/artifact-post.ok"

find "$RUNTIME/backups/assets" -maxdepth 1 -type f -printf '%f\n' | sort > "$EVIDENCE/post-deploy-backup-inventory.txt"
comm -23 "$EVIDENCE/pre/backup-inventory.txt" "$EVIDENCE/post-deploy-backup-inventory.txt" | grep -q . && die_fail "ASSET_BACKUP_LOSS" "Asset backups were removed"

"$RUNTIME/pi4/validate_pi4.sh" > "$EVIDENCE/runtime-validation.log" 2>&1 || die_fail "RUNTIME_VALIDATION_FAILED" "Pi4 runtime validation failed"
[ "$(mode "$RUNTIME/state/inventory")" -le 750 ] || die_fail "STATE_MODE_INVALID" "state directory mode is too broad"
[ "$(mode "$RUNTIME/backups/assets")" = 700 ] || die_fail "BACKUP_MODE_INVALID" "Asset backup directory mode is invalid"
[ ! -L "$RUNTIME/backups/assets" ] || die_fail "BACKUP_SYMLINK" "Asset backup root is a symlink"
[ "$(owner "$RUNTIME/backups/assets")" = jazofv1:jazofv1 ] || die_fail "OWNERSHIP_INVALID" "Asset backup ownership is invalid"
find "$RUNTIME/state/inventory" -maxdepth 1 -type f -name '.assets*.tmp' | grep -q . && die_fail "PARTIAL_FILE_FOUND" "unexpected Asset temporary file exists"
touch "$EVIDENCE/permissions.ok"

CLI=(python3 "$RUNTIME/pi4/bin/hioc-assets.py" --json)
run_cli() { local label="$1"; shift; local start end rc; start="$(date +%s%N)"; if HIOC_HOME="$RUNTIME" "${CLI[@]}" "$@" > "$EVIDENCE/$label.json" 2> "$EVIDENCE/$label.err"; then rc=0; else rc=$?; fi; end="$(date +%s%N)"; printf '%s %s\n' "$label" "$(((end-start)/1000000))" >> "$EVIDENCE/performance-ms.txt"; return "$rc"; }

python3 - "$RUNTIME/state/inventory/assets.json" "$RUNTIME/backups/assets" "$SYNTHETIC_ID" <<'PY' > "$EVIDENCE/synthetic-residue-check.json" || die_validation "SYNTHETIC_RESIDUE_PRESENT" "reserved synthetic Asset remains in current state or backups; mutation stopped"
import json,sys
from pathlib import Path
store,backups,reserved=Path(sys.argv[1]),Path(sys.argv[2]),sys.argv[3]
current=False; backup_count=0; invalid_backup_count=0
if store.is_file(): current=reserved in json.load(store.open(encoding="utf-8")).get("assets",{})
if backups.is_dir():
 for path in backups.iterdir():
  if not path.is_file() or path.is_symlink(): continue
  try: present=reserved in json.load(path.open(encoding="utf-8")).get("assets",{})
  except (OSError,ValueError,TypeError): invalid_backup_count+=1; continue
  backup_count+=int(present)
print(json.dumps({"current_state_present":current,"backup_files_present":backup_count,"unreadable_backup_files":invalid_backup_count},sort_keys=True))
raise SystemExit(1 if current or backup_count or invalid_backup_count else 0)
PY
SYNTHETIC_CLEANUP_STATUS="CLEAN_BEFORE_MUTATION"

if [ "$INITIAL_STATE" = UNINITIALIZED ]; then run_cli initialize initialize || die_fail "INITIALIZE_FAILED" "Asset initialization failed"; fi
run_cli validate-initial validate || die_fail "ASSET_VALIDATE_FAILED" "initial Asset validation failed"
[ "$(mode "$RUNTIME/state/inventory/assets.json")" = 600 ] && [ "$(mode "$RUNTIME/state/inventory/assets_status.json")" = 600 ] || die_fail "ASSET_FILE_MODE_INVALID" "Asset file mode is invalid"
[ "$(owner "$RUNTIME/state/inventory/assets.json")" = jazofv1:jazofv1 ] || die_fail "OWNERSHIP_INVALID" "Asset store ownership is invalid"
cp "$RUNTIME/state/inventory/assets.json" "$EVIDENCE/pre-transaction-assets.json"
pre_semantic="$(semantic_digest "$EVIDENCE/pre-transaction-assets.json")"
pre_orphans="$(json_get "$RUNTIME/state/inventory/assets_status.json" orphaned_asset_count)"
if python3 - "$RUNTIME/state/inventory/assets.json" "$SYNTHETIC_ID" <<'PY'
import json,sys
raise SystemExit(0 if sys.argv[2] in json.load(open(sys.argv[1]))["assets"] else 1)
PY
then
  SYNTHETIC_RESULT="PARTIAL_PASS_COLLISION"; WARNINGS+=("reserved synthetic Asset ID already exists; mutation sequence skipped")
else
  run_cli create set --device-id "$SYNTHETIC_ID" --friendly-name 'HIOC PE2 Validation Asset' --physical-location 'Validation Lab' --purpose 'Governed production validation' --notes 'Synthetic temporary record for PE-2.1 validation.' --allow-orphan || die_fail "SYNTHETIC_CREATE_FAILED" "synthetic Asset creation failed"
  revision1="$(json_get "$EVIDENCE/create.json" data.revision)"; [ "$revision1" = 1 ] || die_fail "REVISION_INVALID" "creation revision is invalid"
  backup_create="$(json_get "$EVIDENCE/create.json" data.backup)"; CREATED_BACKUPS+=("$backup_create")
  run_cli update set --device-id "$SYNTHETIC_ID" --purpose 'Governed production validation updated' --expected-revision "$revision1" || die_fail "SYNTHETIC_UPDATE_FAILED" "synthetic Asset update failed"
  revision2="$(json_get "$EVIDENCE/update.json" data.revision)"; [ "$revision2" -eq $((revision1+1)) ] || die_fail "REVISION_INVALID" "update revision did not increment"
  backup_update="$(json_get "$EVIDENCE/update.json" data.backup)"; CREATED_BACKUPS+=("$backup_update")
  before_noop="$(sha "$RUNTIME/state/inventory/assets.json")"; before_backups="$(find "$RUNTIME/backups/assets" -maxdepth 1 -type f | wc -l)"
  run_cli noop set --device-id "$SYNTHETIC_ID" --purpose 'Governed production validation updated' --expected-revision "$revision2" || die_fail "NOOP_FAILED" "no-op update failed"
  [ "$(json_get "$EVIDENCE/noop.json" data.revision)" = "$revision2" ] && [ "$(sha "$RUNTIME/state/inventory/assets.json")" = "$before_noop" ] && [ "$(find "$RUNTIME/backups/assets" -maxdepth 1 -type f | wc -l)" = "$before_backups" ] || die_fail "NOOP_MUTATED" "no-op changed state or backup count"
  set +e; run_cli stale set --device-id "$SYNTHETIC_ID" --purpose invalid --expected-revision "$revision1"; stale_rc=$?; set -e
  [ "$stale_rc" -eq 5 ] && [ "$(sha "$RUNTIME/state/inventory/assets.json")" = "$before_noop" ] || die_fail "STALE_REJECTION_FAILED" "stale revision was not safely rejected"
  run_cli clear clear-field --device-id "$SYNTHETIC_ID" --field physical_location --expected-revision "$revision2" || die_fail "CLEAR_FAILED" "field clear failed"
  revision3="$(json_get "$EVIDENCE/clear.json" data.revision)"; backup_clear="$(json_get "$EVIDENCE/clear.json" data.backup)"; CREATED_BACKUPS+=("$backup_clear")
  run_cli list list || die_fail "LIST_FAILED" "redacted list failed"; run_cli show show --device-id "$SYNTHETIC_ID" || die_fail "SHOW_FAILED" "redacted show failed"
  run_cli explicit-backup backup || die_fail "EXPLICIT_BACKUP_FAILED" "explicit backup failed"; explicit_backup="$(json_get "$EVIDENCE/explicit-backup.json" data.backup)"; CREATED_BACKUPS+=("$explicit_backup")
  run_cli post-backup-update set --device-id "$SYNTHETIC_ID" --notes 'Synthetic temporary record updated for restore validation.' --expected-revision "$revision3" || die_fail "RESTORE_SETUP_FAILED" "restore setup update failed"; CREATED_BACKUPS+=("$(json_get "$EVIDENCE/post-backup-update.json" data.backup)")
  run_cli restore restore --backup "$explicit_backup" || die_fail "RESTORE_FAILED" "Asset restore failed"; CREATED_BACKUPS+=("$(json_get "$EVIDENCE/restore.json" data.pre_restore_backup)")
  [ "$(json_get "$RUNTIME/state/inventory/assets.json" assets.$SYNTHETIC_ID.revision)" = "$revision3" ] || die_fail "RESTORE_SEMANTICS_FAILED" "restore did not recover expected revision"
  set +e; run_cli traversal restore --backup '../assets.json'; traversal_rc=$?; run_cli invalid-id set --device-id invalid --friendly-name invalid --allow-orphan; invalid_id_rc=$?; run_cli invalid-field set --device-id "$SYNTHETIC_ID" --notes $'invalid\tfield' --expected-revision "$revision3"; invalid_field_rc=$?; set -e
  [ "$traversal_rc" -eq 9 ] && [ "$invalid_id_rc" -eq 3 ] && [ "$invalid_field_rc" -eq 3 ] || die_fail "REJECTION_TEST_FAILED" "one invalid operation was not rejected with the approved exit code"
  symlink_name="assets-20000101T000000000000Z-000000000000.json"
  ln -s "$EVIDENCE/pre-transaction-assets.json" "$RUNTIME/backups/assets/$symlink_name"
  set +e; run_cli symlink-rejection restore --backup "$symlink_name"; symlink_rc=$?; set -e
  rm -- "$RUNTIME/backups/assets/$symlink_name"
  [ "$symlink_rc" -eq 9 ] || die_fail "SYMLINK_REJECTION_FAILED" "restore symlink was not rejected"
  lock_ready="$EVIDENCE/lock-ready"; rm -f "$lock_ready"
  python3 - "$RUNTIME" "$lock_ready" <<'PY' &
import sys,time
from pathlib import Path
sys.path.insert(0,str(Path(sys.argv[1])/"pi4"/"lib"))
from hioc.assets import AssetLock
with AssetLock(Path("/tmp/hioc-assets.lock"),False): Path(sys.argv[2]).touch(); time.sleep(6)
PY
  lock_pid=$!; for _ in $(seq 1 50); do [ -e "$lock_ready" ] && break; sleep .1; done
  set +e; run_cli lock-timeout list; lock_rc=$?; set -e; wait "$lock_pid"
  [ "$lock_rc" -eq 6 ] || die_fail "LOCK_TIMEOUT_FAILED" "lock timeout did not return exit 6"
  run_cli remove remove --device-id "$SYNTHETIC_ID" --expected-revision "$revision3" || die_fail "SYNTHETIC_REMOVE_FAILED" "synthetic Asset removal failed"; CREATED_BACKUPS+=("$(json_get "$EVIDENCE/remove.json" data.backup)")
  run_cli validate-final validate || die_fail "FINAL_ASSET_VALIDATE_FAILED" "final Asset validation failed"
  SYNTHETIC_RESULT="PASS"
fi

final_semantic="$(semantic_digest "$RUNTIME/state/inventory/assets.json")"
[ "$final_semantic" = "$pre_semantic" ] || die_fail "FINAL_STATE_MISMATCH" "final Asset semantic state differs from pre-transaction state"
if [ "$INITIAL_STATE" = UNINITIALIZED ]; then FINAL_STATE="INITIALIZED_EMPTY_APPROVED"; else FINAL_STATE="VALID_EXISTING_RESTORED"; fi
python3 - "$RUNTIME/state/inventory/assets.json" "$SYNTHETIC_ID" <<'PY' || die_fail "SYNTHETIC_REMAINS" "synthetic Asset remains after cleanup"
import json,sys
raise SystemExit(1 if sys.argv[2] in json.load(open(sys.argv[1]))["assets"] else 0)
PY
SYNTHETIC_CLEANUP_STATUS="CLEAN_CURRENT_STATE"
post_orphans="$(json_get "$RUNTIME/state/inventory/assets_status.json" orphaned_asset_count)"; [ "$post_orphans" = "$pre_orphans" ] || die_fail "ORPHAN_COUNT_MISMATCH" "orphan count did not return to initial value"

PYTHONPATH="$SOURCE/pi4/lib" python3 - "$RUNTIME/backups/assets" "$EVIDENCE/current-run-synthetic-cleanup-manifest.json" "$EVIDENCE/current-run-backup-classification.json" "$SYNTHETIC_ID" "${CREATED_BACKUPS[@]:-}" <<'PY' || die_validation "SYNTHETIC_BACKUP_CLASSIFICATION_FAILED" "validation-created backup could not be classified safely"
import hashlib,json,sys
from pathlib import Path
from hioc.assets import validate_store
root,manifest_path,evidence_path,reserved=Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]),sys.argv[4]
entries=[]; evidence=[]
for name in filter(None,sys.argv[5:]):
 path=root/name
 try: raw=path.read_bytes(); payload=validate_store(json.loads(raw.decode("utf-8")))
 except Exception: raise SystemExit(1)
 ids=set(payload["assets"]); contains=reserved in ids; synthetic_only=ids=={reserved}
 if contains and not synthetic_only: raise SystemExit(1)
 digest=hashlib.sha256(raw).hexdigest()
 evidence.append({"basename":name,"sha256":digest,"creation_role":"pe2_validation","record_count":payload["asset_count"],"synthetic_only":synthetic_only})
 if synthetic_only: entries.append({"basename":name,"sha256":digest})
manifest={"schema_version":1,"purpose":"current-run-pe2-validation-cleanup","entries":entries}
manifest_path.write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n",encoding="utf-8")
evidence_path.write_text(json.dumps({"tracked_backup_count":len(evidence),"synthetic_only_count":len(entries),"backups":evidence},indent=2,sort_keys=True)+"\n",encoding="utf-8")
PY
cleanup_entry_count="$(json_get "$EVIDENCE/current-run-synthetic-cleanup-manifest.json" entries | jq 'length')"
if [ "$cleanup_entry_count" -gt 0 ]; then
  PYTHONPATH="$SOURCE/pi4/lib" python3 "$SOURCE/tools/hioc-pe2-clean-synthetic-backups.py" --manifest "$EVIDENCE/current-run-synthetic-cleanup-manifest.json" --backup-root "$RUNTIME/backups/assets" --delete > "$EVIDENCE/current-run-synthetic-cleanup.json" || die_validation "SYNTHETIC_BACKUP_CLEANUP_FAILED" "validation-created synthetic backup cleanup failed"
  [ "$(json_get "$EVIDENCE/current-run-synthetic-cleanup.json" cleanup_result)" = PASS ] || die_validation "SYNTHETIC_BACKUP_CLEANUP_FAILED" "validation-created synthetic backup cleanup was incomplete"
fi
SYNTHETIC_CLEANUP_STATUS="CLEAN_CURRENT_STATE_AND_VALIDATION_BACKUPS"

for name in "${PUBLIC_FILES[@]}"; do path="$RUNTIME/state/inventory/$name"; if [ -f "$path" ]; then cp "$path" "$EVIDENCE/post/public/$name"; canonical_json_digest "$path" > "$EVIDENCE/post/public/$name.semantic.sha256"; fi; done
for digest in "$EVIDENCE"/pre/public/*.semantic.sha256; do [ -e "$digest" ] || continue; name="$(basename "$digest")"; cmp -s "$digest" "$EVIDENCE/post/public/$name" || die_fail "PUBLIC_INVARIANT_FAILED" "public inventory contract changed: $name"; done
for name in "${INCIDENT_FILES[@]}"; do path="$RUNTIME/state/incidents/$name"; if [ -f "$path" ]; then cp "$path" "$EVIDENCE/post/incidents/$name"; canonical_json_digest "$path" > "$EVIDENCE/post/incidents/$name.semantic.sha256"; fi; done
set +e
python3 "$SOURCE/tools/validate_pe2_incident_contract.py" --pre "$EVIDENCE/pre/incidents" --post "$EVIDENCE/post/incidents" --repo "$SOURCE" --implementation-commit "$APPROVED_IMPL" --synthetic-value 'HIOC PE2 Validation Asset' --synthetic-value 'Validation Lab' --synthetic-value 'Governed production validation' --synthetic-value 'Synthetic temporary record for PE-2.1 validation.' > "$EVIDENCE/incident-contract.json"
incident_rc=$?
set -e
INCIDENT_CLASSIFICATION="$(json_get "$EVIDENCE/incident-contract.json" classification)"
CAUSAL_REGRESSION="$(json_get "$EVIDENCE/incident-contract.json" causal_regression_demonstrated | tr '[:lower:]' '[:upper:]')"
case "$incident_rc:$INCIDENT_CLASSIFICATION" in
  0:INCIDENT_CONTRACT_UNCHANGED|0:INCIDENT_OPERATIONAL_DRIFT) ;;
  40:INCIDENT_VALIDATION_INCONCLUSIVE) die_validation "INCIDENT_VALIDATION_INCONCLUSIVE" "incident evidence could not be classified safely" ;;
  30:INCIDENT_CONTRACT_REGRESSION) die_fail "INCIDENT_CONTRACT_REGRESSION" "protected incident contract regression demonstrated" TRUE ;;
  *) die_validation "INCIDENT_VALIDATOR_ERROR" "incident comparator returned an invalid contract" ;;
esac
if [ "$MQTT_AVAILABLE" -eq 1 ]; then
  for suffix in "${MQTT_SUFFIXES[@]}"; do mosquitto_sub "${mqtt_args[@]}" -t "$mqtt_base/$suffix" > "$EVIDENCE/post/mqtt/${suffix//\//_}.payload"; cmp -s "$EVIDENCE/pre/mqtt/${suffix//\//_}.payload" "$EVIDENCE/post/mqtt/${suffix//\//_}.payload" || die_fail "MQTT_INVARIANT_FAILED" "established MQTT projection changed"; done
  if mosquitto_sub "${mqtt_args[@]}" -t "$mqtt_base/assets/#" > "$EVIDENCE/post/mqtt/assets.payload" 2>/dev/null; then [ ! -s "$EVIDENCE/post/mqtt/assets.payload" ] || die_fail "ASSET_MQTT_PUBLISHED" "an Asset MQTT topic was published"; fi
fi
PUBLIC_INVARIANTS="PASS"

run_cli asset-validator-post validate || die_fail "FINAL_VALIDATOR_FAILED" "final Asset validation failed"
HIOC_HOME="$RUNTIME" python3 "$RUNTIME/pi4/bin/hioc-validate-assets.py" --home "$RUNTIME" --json > "$EVIDENCE/asset-validator-post.json" || die_fail "READ_ONLY_VALIDATOR_FAILED" "read-only Asset validator failed"

for secret in 'HIOC PE2 Validation Asset' 'Validation Lab' 'Governed production validation' 'Synthetic temporary record for PE-2.1 validation.'; do
  if grep -RFl --exclude='pre-transaction-assets.json' --exclude='assets.json' --exclude='*.payload' "$secret" "$EVIDENCE" "$RUNTIME/logs" "$RUNTIME/state/inventory/assets_status.json" 2>/dev/null | grep -q .; then die_fail "PRIVACY_LEAK" "synthetic Asset value entered routine evidence or logs"; fi
done
PRIVACY_RESULT="PASS"

max_ms="$(awk 'BEGIN{m=0}{if($2>m)m=$2}END{print m}' "$EVIDENCE/performance-ms.txt")"
python3 - "$EVIDENCE/performance-ms.txt" <<'PY' > "$EVIDENCE/performance-summary.json"
import json,sys
rows={};
for line in open(sys.argv[1]): k,v=line.split(); rows[k]=int(v)
limits={"list":1000,"show":1000,"create":3000,"update":3000,"noop":3000,"explicit-backup":2000,"restore":3000,"remove":3000,"validate-initial":2000,"validate-final":2000,"lock-timeout":6000}
warnings=[k for k,v in rows.items() if k in limits and v>limits[k]]
print(json.dumps({"durations_ms":rows,"maximum_ms":max(rows.values(),default=0),"warnings":warnings,"threshold_pass":not warnings},indent=2,sort_keys=True))
PY
jq -e '.threshold_pass==true' "$EVIDENCE/performance-summary.json" >/dev/null || die_fail "PERFORMANCE_THRESHOLD_FAILED" "an approved operation threshold failed"
PERFORMANCE_RESULT="PASS"

if [[ "$SYNTHETIC_RESULT" == PARTIAL_PASS* ]]; then RESULT="PARTIAL_PASS"; else RESULT="PASS"; fi
ROLLBACK_RECOMMENDED="FALSE"
DEPLOYMENT_STATUS="DEPLOYED_AND_VALIDATED"
exit 0
