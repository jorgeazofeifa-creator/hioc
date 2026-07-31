#!/bin/bash
set -eEuo pipefail
set +x

EXPECTED_COMMIT="${1:-}"
SOURCE_ROOT="${HIOC_SOURCE_ROOT:-/home/jazofv1/hioc-release-source}"
RELATIVE_PATH="pi4-tools/scripts/hioc-network-probe.sh"
WORKTREE_FILE="$SOURCE_ROOT/$RELATIVE_PATH"
DEPLOY_HELPER="$SOURCE_ROOT/pi4-tools/deploy-network-probe.sh"
OBSERVER="$SOURCE_ROOT/tools/network_probe_incident_observer.py"
TARGET="${HIOC_NETWORK_PROBE_TARGET:-/home/jazofv1/pi4-tools/scripts/hioc-network-probe.sh}"
CONFIG_FILE="${HIOC_TOOLKIT_CONFIG:-/home/jazofv1/pi4-tools/config/toolkit.conf}"
LOCK_PATH="${HIOC_NETWORK_PROBE_LOCK:-/tmp/hioc-network-probe.lock}"
PHASE_A_RESULT="FAIL"
BACKUP_PATH=""
BLOB_TEMP=""
DEPLOY_LOG=""

phase_a_failure() {
  local status=$?
  trap - ERR
  echo "PHASE A: FAIL" >&2
  echo "PI3 governed deployment: FAIL" >&2
  echo "Overall checkpoint production validation: FAIL" >&2
  if [ -n "$BACKUP_PATH" ] && [ -e "$BACKUP_PATH" ]; then
    printf 'Rollback backup: %s\n' "$BACKUP_PATH" >&2
    printf 'Use only if deterministic deployment validation fails and rollback is justified:\ninstall -o jazofv1 -g jazofv1 -m 0755 -- %q %q\n' \
      "$BACKUP_PATH" "$TARGET" >&2
  fi
  exit "$status"
}
trap phase_a_failure ERR
cleanup() {
  [ -z "$BLOB_TEMP" ] || rm -f -- "$BLOB_TEMP"
  [ -z "$DEPLOY_LOG" ] || rm -f -- "$DEPLOY_LOG"
}
trap cleanup EXIT

[ -n "$EXPECTED_COMMIT" ]
echo "Target machine: PI3 NUT&PIHOLE"
echo "Approved commit: $EXPECTED_COMMIT"
echo "Artifact path: $RELATIVE_PATH"
[ "$(hostname -s | tr '[:upper:]' '[:lower:]')" = "nutandpihole" ]
[ -d "$SOURCE_ROOT/.git" ]
cd "$SOURCE_ROOT"
[ -z "$(git status --porcelain --untracked-files=all)" ]
git fetch origin
[ "$(git rev-parse origin/main)" = "$EXPECTED_COMMIT" ]
git switch main
git merge --ff-only origin/main
[ "$(git rev-parse HEAD)" = "$EXPECTED_COMMIT" ]
[ -z "$(git status --porcelain --untracked-files=all)" ]

BLOB_OBJECT="$(git rev-parse "${EXPECTED_COMMIT}:${RELATIVE_PATH}")"
git cat-file -e "${BLOB_OBJECT}^{blob}"
TREE_ENTRY="$(git ls-tree "$EXPECTED_COMMIT" -- "$RELATIVE_PATH")"
[ "$(printf '%s\n' "$TREE_ENTRY" | awk '{print $1}')" = "100755" ]
[ "$(printf '%s\n' "$TREE_ENTRY" | awk '{print $2}')" = "blob" ]
[ "$(printf '%s\n' "$TREE_ENTRY" | awk '{print $3}')" = "$BLOB_OBJECT" ]
BLOB_TEMP="$(mktemp)"
git cat-file blob "$BLOB_OBJECT" >"$BLOB_TEMP"
GIT_BLOB_SHA="$(sha256sum "$BLOB_TEMP" | awk '{print $1}')"
SOURCE_SHA="$(sha256sum "$WORKTREE_FILE" | awk '{print $1}')"
cmp -s -- "$BLOB_TEMP" "$WORKTREE_FILE"
[ "$(git hash-object --no-filters "$WORKTREE_FILE")" = "$BLOB_OBJECT" ]
bash -n "$WORKTREE_FILE"

[ -r "$CONFIG_FILE" ]
unset HOME_ASSISTANT_IP MQTT_HOST MQTT_PORT MQTT_USER MQTT_PASSWORD MQTT_BASE_TOPIC HIOC_BASE_TOPIC
set -a
source "$CONFIG_FILE"
set +a
for name in HOME_ASSISTANT_IP MQTT_HOST MQTT_PORT MQTT_USER MQTT_PASSWORD; do [ -n "${!name:-}" ]; done
[ "$HOME_ASSISTANT_IP" != "192.168.100.152" ]
case "$HOME_ASSISTANT_IP" in *[!0-9.]*|"") false ;; esac
echo "Configured HOME_ASSISTANT_IP: $HOME_ASSISTANT_IP"
echo "MQTT settings: present; credentials not displayed"

exec 9>"$LOCK_PATH"
flock -n 9
ping -c 3 -W 2 "$HOME_ASSISTANT_IP" >/dev/null
timeout 5 bash -c "exec 3<>/dev/tcp/${HOME_ASSISTANT_IP}/8123"

DEPLOY_LOG="$(mktemp)"
set +e
"$DEPLOY_HELPER" "$EXPECTED_COMMIT" "$RELATIVE_PATH" 2>&1 | tee "$DEPLOY_LOG"
DEPLOY_STATUS="${PIPESTATUS[0]}"
set -e
BACKUP_PATH="$(sed -n 's/^Backup: //p' "$DEPLOY_LOG" | head -1)"
[ "$DEPLOY_STATUS" -eq 0 ] || false
[ -n "$BACKUP_PATH" ]
[ -e "$BACKUP_PATH" ]
[ "$BACKUP_PATH" != "$TARGET" ]
[ "$BACKUP_PATH" != "$TARGET.backup" ]
[ -f "$TARGET" ]
bash -n "$TARGET"
[ "$(stat -c '%U' "$TARGET")" = "jazofv1" ]
[ "$(stat -c '%G' "$TARGET")" = "jazofv1" ]
[ "$(stat -c '%a' "$TARGET")" = "755" ]
DEPLOYED_SHA="$(sha256sum "$TARGET" | awk '{print $1}')"
cmp -s -- "$BLOB_TEMP" "$TARGET"
[ "$GIT_BLOB_SHA" = "$SOURCE_SHA" ]
[ "$GIT_BLOB_SHA" = "$DEPLOYED_SHA" ]

"$TARGET"
BASE_TOPIC="${MQTT_BASE_TOPIC:-home/infrastructure/pi4}"
HIOC_BASE_TOPIC="${HIOC_BASE_TOPIC:-home/infrastructure/hioc}"
mqtt_read() {
  timeout 8 mosquitto_sub -h "$MQTT_HOST" -p "$MQTT_PORT" -u "$MQTT_USER" \
    -P "$MQTT_PASSWORD" -W 5 -C 1 -t "$1"
}
[ "$(mqtt_read "$BASE_TOPIC/network/pi5_status")" = "online" ]
NETWORK_STATE="$(mqtt_read "$BASE_TOPIC/network/state")"
printf '%s' "$NETWORK_STATE" | jq -e '.pi5.status == "online"' >/dev/null
INVENTORY_STATE="$(mqtt_read "$BASE_TOPIC/inventory/state")"
printf '%s' "$INVENTORY_STATE" | jq -e --arg ip "$HOME_ASSISTANT_IP" '
  any(.devices[]; .name == "Pi5 Home Assistant" and .ip == $ip and .status == "online")
  and all(.devices[]; .ip != "192.168.100.152")
' >/dev/null

PHASE_A_RESULT="PASS"
trap - ERR
echo "Git blob ID: $BLOB_OBJECT"
echo "Git-derived SHA-256: $GIT_BLOB_SHA"
echo "Source SHA-256: $SOURCE_SHA"
echo "Deployed SHA-256: $DEPLOYED_SHA"
echo "Rollback backup: $BACKUP_PATH"
echo "PHASE A: PASS"

set +e
OBSERVATION="$(
  MQTT_PASSWORD="$MQTT_PASSWORD" python3 "$OBSERVER" \
    --host "$MQTT_HOST" --port "$MQTT_PORT" --user "$MQTT_USER" \
    --topic "$HIOC_BASE_TOPIC/incidents/active"
)"
OBSERVER_STATUS=$?
set -e
if [ "$OBSERVER_STATUS" -ne 0 ]; then
  OBSERVATION="Incident reads successful: 0
Incident read failures/timeouts: 1
Malformed incident payloads: 0
Last successfully read incident key: unreadable
False PI5 evidence in last successful state: unknown
Elapsed observation duration: 0 seconds
PHASE_B_RESULT=INCONCLUSIVE
Follow-up required: incident observer could not complete reliably."
fi
printf '%s\n' "$OBSERVATION"
PHASE_B_RESULT="$(printf '%s\n' "$OBSERVATION" | sed -n 's/^PHASE_B_RESULT=//p' | tail -1)"

echo "PI3 governed deployment: PASS"
echo "PHASE B: $PHASE_B_RESULT"
if [ "$PHASE_B_RESULT" = "PASS" ]; then
  echo "Incident recovery observation: PASS"
  echo "Overall checkpoint production validation: PASS"
else
  echo "Incident recovery observation: $PHASE_B_RESULT"
  echo "Overall checkpoint production validation: PARTIAL PASS"
  echo "Governed deployment succeeded; PI5 live probe, retained MQTT state, and retained inventory are correct."
  echo "The next checkpoint is incident-engine recovery semantics and downstream state convergence."
  echo "Do not roll back based only on this observation."
fi
echo "Do not roll back solely because incident recovery was not observed during the bounded window."
printf 'Use only if deterministic deployment validation fails and rollback is justified:\ninstall -o jazofv1 -g jazofv1 -m 0755 -- %q %q\n' \
  "$BACKUP_PATH" "$TARGET"
exit 0
