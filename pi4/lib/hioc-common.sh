#!/usr/bin/env bash
set -euo pipefail

HIOC_HOME="${HIOC_HOME:-/home/jazofv1/hioc}"
PI4_TOOLS_HOME="${PI4_TOOLS_HOME:-/home/jazofv1/pi4-tools}"
HIOC_CONFIG="$HIOC_HOME/config/hioc.conf"
PI4_TOOLKIT_CONFIG="$PI4_TOOLS_HOME/config/toolkit.conf"

[ -f "$PI4_TOOLKIT_CONFIG" ] && source "$PI4_TOOLKIT_CONFIG"
[ -f "$HIOC_CONFIG" ] && source "$HIOC_CONFIG"

HIOC_BASE_TOPIC="${HIOC_BASE_TOPIC:-home/infrastructure/hioc}"
HIOC_LEGACY_BASE_TOPIC="${HIOC_LEGACY_BASE_TOPIC:-${MQTT_BASE_TOPIC:-home/infrastructure/pi4}}"
HIOC_STATE_DIR="${HIOC_STATE_DIR:-$HIOC_HOME/state}"
HIOC_LOG_DIR="${HIOC_LOG_DIR:-$HIOC_HOME/logs}"
HIOC_BACKUP_DIR="${HIOC_BACKUP_DIR:-$HIOC_HOME/backups}"
HIOC_HISTORY_LIMIT="${HIOC_HISTORY_LIMIT:-50}"
HIOC_MAINTENANCE_MODE="${HIOC_MAINTENANCE_MODE:-off}"

mkdir -p "$HIOC_STATE_DIR" "$HIOC_LOG_DIR" "$HIOC_BACKUP_DIR" "$HIOC_STATE_DIR/incidents"

hioc_now_iso() {
  date '+%Y-%m-%dT%H:%M:%S%z'
}

hioc_now_epoch() {
  date +%s
}

hioc_log() {
  local level="$1"
  shift
  printf '%s [%s] %s\n' "$(date '+%F %T')" "$level" "$*" >> "$HIOC_LOG_DIR/hioc.log"
}

hioc_require() {
  local missing=0
  for cmd in "$@"; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
      echo "Missing required command: $cmd" >&2
      missing=1
    fi
  done
  [ "$missing" -eq 0 ]
}

hioc_num() {
  local value="${1:-}"
  local fallback="${2:-0}"
  if printf '%s' "$value" | grep -Eq '^-?[0-9]+([.][0-9]+)?$'; then
    printf '%s' "$value"
  else
    printf '%s' "$fallback"
  fi
}

hioc_file_value() {
  local file="$1"
  local fallback="${2:-unknown}"
  if [ -f "$file" ]; then
    cat "$file" 2>/dev/null || printf '%s' "$fallback"
  else
    printf '%s' "$fallback"
  fi
}

hioc_publish() {
  local topic="$1"
  local payload="$2"
  if [ -z "${MQTT_HOST:-}" ]; then
    hioc_log ERROR "MQTT_HOST is not configured"
    return 1
  fi
  mosquitto_pub \
    -h "$MQTT_HOST" \
    -p "${MQTT_PORT:-1883}" \
    -u "${MQTT_USER:-}" \
    -P "${MQTT_PASSWORD:-}" \
    -t "$topic" \
    -m "$payload" \
    -r
}

hioc_publish_json_file() {
  local topic="$1"
  local file="$2"
  if [ ! -f "$file" ]; then
    hioc_log WARN "Cannot publish missing JSON file $file"
    return 1
  fi
  hioc_publish "$topic" "$(cat "$file")"
}
