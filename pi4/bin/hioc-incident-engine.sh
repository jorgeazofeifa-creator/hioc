#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HIOC_HOME="${HIOC_HOME:-$(cd "$SCRIPT_DIR/../.." && pwd)}"
source "$HIOC_HOME/pi4/lib/hioc-common.sh"

hioc_require jq mosquitto_pub >/dev/null

INCIDENT_DIR="$HIOC_STATE_DIR/incidents"
ACTIVE_FILE="$INCIDENT_DIR/active.json"
HISTORY_FILE="$INCIDENT_DIR/history.json"
SUMMARY_FILE="$INCIDENT_DIR/summary.json"
TIMELINE_FILE="$INCIDENT_DIR/timeline.json"
LAST_EVENT_FILE="$INCIDENT_DIR/latest_event.json"
LOCK_FILE="/tmp/hioc-incident-engine.lock"
LEGACY_STATE="$PI4_TOOLS_HOME/state/hioc"

exec 9>"$LOCK_FILE"
if ! flock -n 9; then
  exit 0
fi

[ -f "$HISTORY_FILE" ] || echo '[]' > "$HISTORY_FILE"
[ -f "$ACTIVE_FILE" ] || echo '{"status":"none","title":"No active incident","severity":"info","system":"HIOC","updated":"unknown"}' > "$ACTIVE_FILE"
[ -f "$TIMELINE_FILE" ] || echo '[]' > "$TIMELINE_FILE"

now="$(hioc_now_iso)"
now_epoch="$(hioc_now_epoch)"

warn_latency="${HIOC_WARN_INTERNET_LATENCY_MS:-120}"
major_latency="${HIOC_MAJOR_INTERNET_LATENCY_MS:-250}"
warn_loss="${HIOC_WARN_PACKET_LOSS_PERCENT:-1}"
major_loss="${HIOC_MAJOR_PACKET_LOSS_PERCENT:-10}"
warn_dns="${HIOC_WARN_DNS_LATENCY_MS:-100}"
major_dns="${HIOC_MAJOR_DNS_LATENCY_MS:-500}"
warn_gateway="${HIOC_WARN_GATEWAY_LATENCY_MS:-20}"
major_gateway="${HIOC_MAJOR_GATEWAY_LATENCY_MS:-100}"
warn_mqtt="${HIOC_WARN_MQTT_PUBLISH_MS:-500}"
major_mqtt="${HIOC_MAJOR_MQTT_PUBLISH_MS:-2000}"
warn_ups="${HIOC_WARN_UPS_RUNTIME_SEC:-1800}"
major_ups="${HIOC_MAJOR_UPS_RUNTIME_SEC:-900}"
warn_temp="${HIOC_WARN_PI4_TEMP_C:-65}"
major_temp="${HIOC_MAJOR_PI4_TEMP_C:-75}"

read_mqtt_topic() {
  local topic="$1"
  local fallback="${2:-unknown}"
  timeout 3 mosquitto_sub \
    -h "$MQTT_HOST" \
    -p "${MQTT_PORT:-1883}" \
    -u "${MQTT_USER:-}" \
    -P "${MQTT_PASSWORD:-}" \
    -C 1 \
    -t "$topic" 2>/dev/null || printf '%s' "$fallback"
}

metric() {
  local topic="$1"
  local fallback="${2:-0}"
  local value
  value="$(read_mqtt_topic "$topic" "$fallback")"
  hioc_num "$value" "$fallback"
}

metric_text() {
  local topic="$1"
  local fallback="${2:-unknown}"
  read_mqtt_topic "$topic" "$fallback"
}

add_timeline() {
  local severity="$1"
  local system="$2"
  local title="$3"
  local message="$4"
  local incident_id="${5:-}"
  local event
  event="$(jq -n \
    --arg timestamp "$now" \
    --arg severity "$severity" \
    --arg system "$system" \
    --arg title "$title" \
    --arg message "$message" \
    --arg incident_id "$incident_id" \
    '{timestamp:$timestamp,severity:$severity,system:$system,title:$title,message:$message,incident_id:$incident_id}')"
  jq --argjson event "$event" --argjson limit "$HIOC_HISTORY_LIMIT" '([$event] + .)[0:$limit]' "$TIMELINE_FILE" > "$TIMELINE_FILE.tmp" && mv "$TIMELINE_FILE.tmp" "$TIMELINE_FILE"
  printf '%s' "$event" > "$LAST_EVENT_FILE"
}

publish_all() {
  hioc_publish_json_file "$HIOC_BASE_TOPIC/incidents/active" "$ACTIVE_FILE" || true
  hioc_publish_json_file "$HIOC_BASE_TOPIC/incidents/history" "$HISTORY_FILE" || true
  hioc_publish_json_file "$HIOC_BASE_TOPIC/incidents/summary" "$SUMMARY_FILE" || true
  hioc_publish_json_file "$HIOC_BASE_TOPIC/timeline/history" "$TIMELINE_FILE" || true
  [ -f "$LAST_EVENT_FILE" ] && hioc_publish_json_file "$HIOC_BASE_TOPIC/timeline/latest" "$LAST_EVENT_FILE" || true
  hioc_publish "$HIOC_BASE_TOPIC/status" "online" || true
}

stable_id() {
  local key="$1"
  printf '%s' "$key" | sha1sum | awk '{print $1}'
}

severity_rank() {
  case "$1" in
    critical) echo 4 ;;
    major) echo 3 ;;
    warning) echo 2 ;;
    info) echo 1 ;;
    *) echo 0 ;;
  esac
}

make_incident() {
  local key="$1" severity="$2" system="$3" title="$4" reason="$5" impact="$6" recommendation="$7" current="$8" affected="$9"
  local id
  id="$(stable_id "$key")"
  jq -n \
    --arg id "$id" \
    --arg key "$key" \
    --arg status "active" \
    --arg severity "$severity" \
    --arg system "$system" \
    --arg title "$title" \
    --arg reason "$reason" \
    --arg impact "$impact" \
    --arg recommendation "$recommendation" \
    --arg current "$current" \
    --arg started "$now" \
    --arg updated "$now" \
    --argjson affected "$affected" \
    '{id:$id,key:$key,status:$status,severity:$severity,system:$system,title:$title,reason:$reason,impact:$impact,recommendation:$recommendation,current_value:$current,affected:$affected,started:$started,updated:$updated,worst_observed:$current,occurrences:1}'
}

# Telemetry from existing probe topics
avg_latency="$(metric "$HIOC_LEGACY_BASE_TOPIC/network/average_internet_latency_ms" 0)"
packet_loss="$(metric "$HIOC_LEGACY_BASE_TOPIC/network/average_packet_loss_percent" 0)"
dns_local="$(metric "$HIOC_LEGACY_BASE_TOPIC/network/dns_latency_local_ms" 0)"
gateway_latency="$(metric "$HIOC_LEGACY_BASE_TOPIC/network/gateway_latency_ms" 0)"
mqtt_publish_ms="$(metric "$HIOC_LEGACY_BASE_TOPIC/network/mqtt_publish_duration_ms" 0)"
internet_health="$(metric_text "$HIOC_LEGACY_BASE_TOPIC/network/internet_health" healthy)"
gateway_status="$(metric_text "$HIOC_LEGACY_BASE_TOPIC/network/gateway_status" online)"
pi5_status="$(metric_text "$HIOC_LEGACY_BASE_TOPIC/network/pi5_status" online)"
ups1_runtime="$(hioc_num "$(hioc_file_value "$PI4_TOOLS_HOME/state/UPS1.runtime" "$(metric "$HIOC_LEGACY_BASE_TOPIC/ups/ups1_runtime" 999999)")" 999999)"
ups2_runtime="$(hioc_num "$(hioc_file_value "$PI4_TOOLS_HOME/state/UPS2.runtime" "$(metric "$HIOC_LEGACY_BASE_TOPIC/ups/ups2_runtime" 999999)")" 999999)"
ups1_status="$(hioc_file_value "$PI4_TOOLS_HOME/state/UPS1.status" online)"
ups2_status="$(hioc_file_value "$PI4_TOOLS_HOME/state/UPS2.status" online)"
pi4_temp="0"
if command -v vcgencmd >/dev/null 2>&1; then
  pi4_temp="$(vcgencmd measure_temp 2>/dev/null | sed -E "s/[^0-9.]//g" || echo 0)"
fi

candidates="[]"
add_candidate() {
  local incident="$1"
  candidates="$(jq --argjson incident "$incident" '. + [$incident]' <<< "$candidates")"
}

if [ "$gateway_status" != "online" ]; then
  add_candidate "$(make_incident gateway_offline critical Gateway "Gateway unreachable" "Pi4 cannot reach gateway 192.168.100.1" "Internet, DNS, MQTT, and Home Assistant connectivity may be affected" "Check Huawei gateway, Orbi AP path, cabling, and power." "$gateway_status" '["Internet","Gateway","DNS","MQTT","Home Assistant"]')"
elif awk "BEGIN {exit !($gateway_latency >= $major_gateway)}"; then
  add_candidate "$(make_incident gateway_latency major Gateway "Gateway latency high" "Gateway latency exceeded ${major_gateway} ms" "Local network path is degraded" "Check LAN cabling, Orbi AP, Huawei gateway load, and local interference." "${gateway_latency} ms" '["Gateway","LAN","DNS"]')"
elif awk "BEGIN {exit !($gateway_latency >= $warn_gateway)}"; then
  add_candidate "$(make_incident gateway_latency warning Gateway "Gateway latency warning" "Gateway latency exceeded ${warn_gateway} ms" "Local network path may be degraded" "Watch for packet loss or client roaming problems." "${gateway_latency} ms" '["Gateway","LAN"]')"
fi

if awk "BEGIN {exit !($packet_loss >= $major_loss)}"; then
  add_candidate "$(make_incident internet_packet_loss major Internet "Internet packet loss" "Average packet loss exceeded ${major_loss}%" "Internet quality is degraded and services may feel unreliable" "Check ISP path, Huawei WAN state, and run a manual speed test." "${packet_loss}%" '["Internet","DNS","MQTT","Cloud services"]')"
elif awk "BEGIN {exit !($packet_loss >= $warn_loss)}"; then
  add_candidate "$(make_incident internet_packet_loss warning Internet "Internet packet loss warning" "Average packet loss exceeded ${warn_loss}%" "Internet quality may be degraded" "Watch if loss persists for more than two probe cycles." "${packet_loss}%" '["Internet"]')"
elif awk "BEGIN {exit !($avg_latency >= $major_latency)}"; then
  add_candidate "$(make_incident internet_latency major Internet "Internet latency high" "Average internet latency exceeded ${major_latency} ms" "Internet quality is degraded" "Compare Cloudflare vs Google latency and check ISP routing." "${avg_latency} ms" '["Internet"]')"
elif awk "BEGIN {exit !($avg_latency >= $warn_latency)}"; then
  add_candidate "$(make_incident internet_latency warning Internet "Internet latency warning" "Average internet latency exceeded ${warn_latency} ms" "Internet may feel slow" "Watch trend and compare against gateway latency." "${avg_latency} ms" '["Internet"]')"
elif [ "$internet_health" = "critical" ]; then
  add_candidate "$(make_incident internet_health critical Internet "Internet health critical" "Probe reported internet health critical" "Internet services may be unavailable" "Inspect WAN status, Huawei gateway, DNS, and packet loss." "$internet_health" '["Internet","DNS"]')"
elif [ "$internet_health" = "degraded" ]; then
  add_candidate "$(make_incident internet_health warning Internet "Internet health degraded" "Probe reported internet health degraded" "Internet quality may be reduced" "Review latency, packet loss, and jitter." "$internet_health" '["Internet"]')"
fi

if awk "BEGIN {exit !($dns_local >= $major_dns)}"; then
  add_candidate "$(make_incident dns_latency major DNS "DNS latency high" "Local DNS lookup time exceeded ${major_dns} ms" "Name resolution may be slow or timing out" "Check Pi-hole FTL, upstream DNS, and Pi4 load." "${dns_local} ms" '["DNS","Pi-hole","Internet"]')"
elif awk "BEGIN {exit !($dns_local >= $warn_dns)}"; then
  add_candidate "$(make_incident dns_latency warning DNS "DNS latency warning" "Local DNS lookup time exceeded ${warn_dns} ms" "DNS may be slower than normal" "Review Pi-hole and upstream resolver latency." "${dns_local} ms" '["DNS","Pi-hole"]')"
fi

if awk "BEGIN {exit !($mqtt_publish_ms >= $major_mqtt)}"; then
  add_candidate "$(make_incident mqtt_publish major MQTT "MQTT publish latency high" "MQTT publish duration exceeded ${major_mqtt} ms" "Telemetry publication may be delayed" "Check Mosquitto broker health and Home Assistant host load." "${mqtt_publish_ms} ms" '["MQTT","Home Assistant","Telemetry"]')"
elif awk "BEGIN {exit !($mqtt_publish_ms >= $warn_mqtt)}"; then
  add_candidate "$(make_incident mqtt_publish warning MQTT "MQTT publish latency warning" "MQTT publish duration exceeded ${warn_mqtt} ms" "Telemetry publication may be slower than normal" "Watch broker CPU and memory." "${mqtt_publish_ms} ms" '["MQTT","Telemetry"]')"
fi

if [ "$pi5_status" != "online" ]; then
  add_candidate "$(make_incident pi5_offline critical Pi5 "Home Assistant host unreachable" "Pi4 cannot reach Pi5 / Home Assistant host" "Home Assistant dashboard and automations may be unavailable" "Check Pi5 power, network, and Home Assistant host state." "$pi5_status" '["Home Assistant","Pi5"]')"
fi

lowest_ups_runtime="$ups1_runtime"
[ "$ups2_runtime" -lt "$lowest_ups_runtime" ] && lowest_ups_runtime="$ups2_runtime"
if [ "$ups1_status" != "OL" ] || [ "$ups2_status" != "OL" ]; then
  add_candidate "$(make_incident ups_on_battery critical UPS "UPS on battery" "At least one UPS is not on line power" "Power protection is active and runtime is limited" "Confirm utility power, UPS input voltage, and attached load." "UPS1=$ups1_status UPS2=$ups2_status" '["Power","UPS","Pi4","Pi5"]')"
elif [ "$lowest_ups_runtime" -le "$major_ups" ]; then
  add_candidate "$(make_incident ups_runtime major UPS "UPS runtime low" "UPS runtime is below ${major_ups} seconds" "Systems may shut down quickly during outage" "Reduce load or prepare controlled shutdown." "${lowest_ups_runtime}s" '["Power","UPS"]')"
elif [ "$lowest_ups_runtime" -le "$warn_ups" ]; then
  add_candidate "$(make_incident ups_runtime warning UPS "UPS runtime warning" "UPS runtime is below ${warn_ups} seconds" "Battery runtime is lower than desired" "Review UPS load and battery health." "${lowest_ups_runtime}s" '["Power","UPS"]')"
fi

if awk "BEGIN {exit !($pi4_temp >= $major_temp)}"; then
  add_candidate "$(make_incident pi4_temperature major Pi4 "Pi4 temperature high" "Pi4 temperature exceeded ${major_temp}C" "Pi4 performance may throttle" "Check Pi4 cooling, case airflow, and CPU load." "${pi4_temp}C" '["Pi4","Pi-hole","NUT","Probe"]')"
elif awk "BEGIN {exit !($pi4_temp >= $warn_temp)}"; then
  add_candidate "$(make_incident pi4_temperature warning Pi4 "Pi4 temperature warning" "Pi4 temperature exceeded ${warn_temp}C" "Thermal headroom is reduced" "Watch trend and inspect cooling if it continues rising." "${pi4_temp}C" '["Pi4"]')"
fi

selected="$(jq 'sort_by(.severity as $s | if $s=="critical" then 4 elif $s=="major" then 3 elif $s=="warning" then 2 else 1 end) | reverse | .[0] // empty' <<< "$candidates")"
current_active="$(cat "$ACTIVE_FILE")"
current_key="$(jq -r '.key // empty' <<< "$current_active")"
current_status="$(jq -r '.status // "none"' <<< "$current_active")"

if [ -z "$selected" ] || [ "$selected" = "null" ]; then
  if [ "$current_status" = "active" ]; then
    resolved="$(jq --arg resolved "$now" --arg status "resolved" --argjson resolved_epoch "$now_epoch" '.status=$status | .resolved=$resolved | .updated=$resolved | .resolved_epoch=$resolved_epoch | .duration_seconds=($resolved_epoch - ((.started_epoch // 0)))' <<< "$current_active")"
    jq --argjson incident "$resolved" --argjson limit "$HIOC_HISTORY_LIMIT" '([$incident] + .)[0:$limit]' "$HISTORY_FILE" > "$HISTORY_FILE.tmp" && mv "$HISTORY_FILE.tmp" "$HISTORY_FILE"
    title="$(jq -r '.title' <<< "$resolved")"
    system="$(jq -r '.system' <<< "$resolved")"
    duration="$(jq -r '.duration_seconds // 0' <<< "$resolved")"
    add_timeline info "$system" "Incident resolved" "$title recovered after ${duration}s" "$(jq -r '.id' <<< "$resolved")"
  fi
  jq -n --arg updated "$now" '{status:"none",severity:"info",system:"HIOC",title:"No active incident",summary:"All monitored systems are within thresholds",updated:$updated}' > "$ACTIVE_FILE"
else
  selected="$(jq --argjson epoch "$now_epoch" '.started_epoch=$epoch | .updated_epoch=$epoch' <<< "$selected")"
  selected_key="$(jq -r '.key' <<< "$selected")"
  if [ "$current_status" = "active" ] && [ "$current_key" = "$selected_key" ]; then
    merged="$(jq -n --argjson old "$current_active" --argjson new "$selected" '$old | .updated=$new.updated | .updated_epoch=$new.updated_epoch | .current_value=$new.current_value | .reason=$new.reason | .impact=$new.impact | .recommendation=$new.recommendation | .occurrences=(.occurrences + 1) | .worst_observed=$new.current_value')"
    printf '%s' "$merged" > "$ACTIVE_FILE"
  else
    if [ "$current_status" = "active" ]; then
      interrupted="$(jq --arg resolved "$now" --arg status "superseded" --argjson resolved_epoch "$now_epoch" '.status=$status | .resolved=$resolved | .updated=$resolved | .resolved_epoch=$resolved_epoch | .duration_seconds=($resolved_epoch - ((.started_epoch // 0)))' <<< "$current_active")"
      jq --argjson incident "$interrupted" --argjson limit "$HIOC_HISTORY_LIMIT" '([$incident] + .)[0:$limit]' "$HISTORY_FILE" > "$HISTORY_FILE.tmp" && mv "$HISTORY_FILE.tmp" "$HISTORY_FILE"
    fi
    printf '%s' "$selected" > "$ACTIVE_FILE"
    add_timeline "$(jq -r '.severity' <<< "$selected")" "$(jq -r '.system' <<< "$selected")" "$(jq -r '.title' <<< "$selected")" "$(jq -r '.reason' <<< "$selected")" "$(jq -r '.id' <<< "$selected")"
  fi
fi

history_count="$(jq 'length' "$HISTORY_FILE")"
active_title="$(jq -r '.title // "No active incident"' "$ACTIVE_FILE")"
active_severity="$(jq -r '.severity // "info"' "$ACTIVE_FILE")"
active_status="$(jq -r '.status // "none"' "$ACTIVE_FILE")"

jq -n \
  --arg updated "$now" \
  --arg active_title "$active_title" \
  --arg active_severity "$active_severity" \
  --arg active_status "$active_status" \
  --argjson history_count "$history_count" \
  --arg avg_latency "$avg_latency" \
  --arg packet_loss "$packet_loss" \
  --arg dns_local "$dns_local" \
  --arg gateway_latency "$gateway_latency" \
  --arg mqtt_publish_ms "$mqtt_publish_ms" \
  '{updated:$updated,active_status:$active_status,active_severity:$active_severity,active_title:$active_title,history_count:$history_count,telemetry:{internet_latency_ms:($avg_latency|tonumber),packet_loss_percent:($packet_loss|tonumber),dns_latency_ms:($dns_local|tonumber),gateway_latency_ms:($gateway_latency|tonumber),mqtt_publish_ms:($mqtt_publish_ms|tonumber)}}' > "$SUMMARY_FILE"

publish_all
hioc_log INFO "incident_engine status=$active_status severity=$active_severity title=$active_title"
