#!/bin/bash

BASE="${HIOC_PI4_TOOLS_BASE:-/home/jazofv1/pi4-tools}"
CONFIG="$BASE/config/toolkit.conf"
LOG="$BASE/logs/hioc-network-probe.log"
EVENT_LOG="$BASE/logs/hioc-events.log"
STATE_DIR="$BASE/state/hioc"

configuration_error() {
  local message="$1"
  local timestamp
  timestamp="$(date '+%F %T')"
  printf '%s ERROR %s\n' "$timestamp" "$message" >&2
  if [ -d "$BASE/logs" ]; then
    printf '%s ERROR %s\n' "$timestamp" "$message" >> "$LOG"
  fi
  exit 2
}

[ -f "$CONFIG" ] || configuration_error "required configuration file is missing: $CONFIG"
# shellcheck disable=SC1090
source "$CONFIG"

for required_name in HOME_ASSISTANT_IP MQTT_HOST MQTT_PORT MQTT_USER MQTT_PASSWORD; do
  [ -n "${!required_name:-}" ] || configuration_error "required configuration value is missing: $required_name"
done

mkdir -p "$STATE_DIR"

BASE_TOPIC="${MQTT_BASE_TOPIC:-home/infrastructure/pi4}"
PROBE_TOPIC="$BASE_TOPIC/network"
EVENT_TOPIC="$BASE_TOPIC/events"
INVENTORY_TOPIC="$BASE_TOPIC/inventory"

publish_failures_file="$STATE_DIR/mqtt_publish_failures"
outage_count_file="$STATE_DIR/internet_outage_count"
last_health_file="$STATE_DIR/last_internet_health"
last_public_ip_file="$STATE_DIR/last_public_ip"

touch "$publish_failures_file" "$outage_count_file" "$last_health_file" "$last_public_ip_file"

publish_raw() {
  local topic="$1"
  local value="$2"

  mosquitto_pub \
    -h "$MQTT_HOST" \
    -p "$MQTT_PORT" \
    -u "$MQTT_USER" \
    -P "$MQTT_PASSWORD" \
    -t "$topic" \
    -m "$value" \
    -r
}

publish() {
  local topic="$1"
  local value="$2"
  local start_ms end_ms duration_ms

  start_ms=$(date +%s%3N)

  if publish_raw "$topic" "$value"; then
    end_ms=$(date +%s%3N)
    duration_ms=$((end_ms - start_ms))
    echo "$duration_ms" > "$STATE_DIR/last_publish_duration_ms"
    date '+%F %T' > "$STATE_DIR/last_publish_success"
  else
    current_failures="$(cat "$publish_failures_file" 2>/dev/null || echo 0)"
    echo $((current_failures + 1)) > "$publish_failures_file"
    echo "$(date '+%F %T') MQTT publish failed topic=$topic" >> "$LOG"
  fi
}

event() {
  local severity="$1"
  local message="$2"
  local ts
  ts="$(date '+%F %T')"

  echo "$ts [$severity] $message" >> "$EVENT_LOG"

  payload="$(jq -n \
    --arg timestamp "$ts" \
    --arg severity "$severity" \
    --arg message "$message" \
    '{timestamp:$timestamp,severity:$severity,message:$message}')"

  publish_raw "$EVENT_TOPIC/latest" "$payload"
}

ping_metrics() {
  local host="$1"
  ping -c 8 -W 2 "$host" 2>/dev/null
}

latency_avg() {
  awk -F'/' '/rtt|round-trip/ {print $5}'
}

latency_min() {
  awk -F'/' '/rtt|round-trip/ {print $4}'
}

latency_max() {
  awk -F'/' '/rtt|round-trip/ {print $6}'
}

latency_jitter() {
  awk -F'/' '/rtt|round-trip/ {print $7}'
}

packet_loss_from_ping() {
  awk -F',' '/packet loss/ {gsub(/% packet loss| /,"",$3); print $3}'
}

dns_time_ms() {
  local server="$1"
  local domain="${2:-google.com}"

  dig @"$server" "$domain" +tries=1 +time=2 +stats 2>/dev/null \
    | awk '/Query time:/ {print $4}'
}

is_reachable() {
  local host="$1"
  ping -c 1 -W 2 "$host" >/dev/null 2>&1 && echo "online" || echo "offline"
}

safe_num() {
  local value="$1"
  local fallback="${2:-0}"

  if echo "$value" | grep -Eq '^-?[0-9]+([.][0-9]+)?$'; then
    echo "$value"
  else
    echo "$fallback"
  fi
}

now="$(date '+%F %T')"

gateway_ip="192.168.100.1"
pi5_ip="$HOME_ASSISTANT_IP"
pi4_ip="192.168.100.252"
cloudflare_ip="1.1.1.1"
google_ip="8.8.8.8"

gateway_ping="$(ping_metrics "$gateway_ip")"
pi5_ping="$(ping_metrics "$pi5_ip")"
cloudflare_ping="$(ping_metrics "$cloudflare_ip")"
google_ping="$(ping_metrics "$google_ip")"

gateway_status="$(is_reachable "$gateway_ip")"
pi5_status="$(is_reachable "$pi5_ip")"
cloudflare_status="$(is_reachable "$cloudflare_ip")"
google_status="$(is_reachable "$google_ip")"

gateway_avg="$(echo "$gateway_ping" | latency_avg)"
gateway_min="$(echo "$gateway_ping" | latency_min)"
gateway_max="$(echo "$gateway_ping" | latency_max)"
gateway_jitter="$(echo "$gateway_ping" | latency_jitter)"
gateway_loss="$(echo "$gateway_ping" | packet_loss_from_ping)"

pi5_avg="$(echo "$pi5_ping" | latency_avg)"
pi5_loss="$(echo "$pi5_ping" | packet_loss_from_ping)"

cloudflare_avg="$(echo "$cloudflare_ping" | latency_avg)"
cloudflare_min="$(echo "$cloudflare_ping" | latency_min)"
cloudflare_max="$(echo "$cloudflare_ping" | latency_max)"
cloudflare_jitter="$(echo "$cloudflare_ping" | latency_jitter)"
cloudflare_loss="$(echo "$cloudflare_ping" | packet_loss_from_ping)"

google_avg="$(echo "$google_ping" | latency_avg)"
google_min="$(echo "$google_ping" | latency_min)"
google_max="$(echo "$google_ping" | latency_max)"
google_jitter="$(echo "$google_ping" | latency_jitter)"
google_loss="$(echo "$google_ping" | packet_loss_from_ping)"

dns_latency_local="$(dns_time_ms "127.0.0.1" "google.com")"
dns_latency_pihole="$(dns_time_ms "$pi4_ip" "google.com")"
dns_latency_cloudflare="$(dns_time_ms "$cloudflare_ip" "google.com")"

avg_latency="0"
if [ -n "$cloudflare_avg" ] && [ -n "$google_avg" ]; then
  avg_latency="$(awk "BEGIN {printf \"%.1f\", ($cloudflare_avg + $google_avg) / 2}")"
elif [ -n "$cloudflare_avg" ]; then
  avg_latency="$cloudflare_avg"
elif [ -n "$google_avg" ]; then
  avg_latency="$google_avg"
fi

avg_packet_loss="100"
if [ -n "$cloudflare_loss" ] && [ -n "$google_loss" ]; then
  avg_packet_loss="$(awk "BEGIN {printf \"%.1f\", ($cloudflare_loss + $google_loss) / 2}")"
elif [ -n "$cloudflare_loss" ]; then
  avg_packet_loss="$cloudflare_loss"
elif [ -n "$google_loss" ]; then
  avg_packet_loss="$google_loss"
fi

true_jitter="0"
if [ -n "$cloudflare_jitter" ] && [ -n "$google_jitter" ]; then
  true_jitter="$(awk "BEGIN {printf \"%.1f\", ($cloudflare_jitter + $google_jitter) / 2}")"
elif [ -n "$cloudflare_jitter" ]; then
  true_jitter="$cloudflare_jitter"
elif [ -n "$google_jitter" ]; then
  true_jitter="$google_jitter"
fi

internet_health="healthy"
if awk "BEGIN {exit !($avg_packet_loss > 5)}"; then
  internet_health="critical"
elif awk "BEGIN {exit !($avg_packet_loss > 0 || $avg_latency > 120 || $true_jitter > 80)}"; then
  internet_health="degraded"
fi

last_health="$(cat "$last_health_file" 2>/dev/null)"
if [ "$last_health" != "$internet_health" ]; then
  if [ "$internet_health" = "critical" ]; then
    current_outages="$(cat "$outage_count_file" 2>/dev/null || echo 0)"
    echo $((current_outages + 1)) > "$outage_count_file"
    event "critical" "Internet health changed to critical"
  elif [ "$last_health" = "critical" ] && [ "$internet_health" != "critical" ]; then
    event "info" "Internet recovered to $internet_health"
  elif [ -n "$last_health" ]; then
    event "warning" "Internet health changed from $last_health to $internet_health"
  fi
  echo "$internet_health" > "$last_health_file"
fi

public_ip="$(dig +short myip.opendns.com @resolver1.opendns.com 2>/dev/null | tail -1)"
last_public_ip="$(cat "$last_public_ip_file" 2>/dev/null)"

if [ -n "$public_ip" ] && [ "$public_ip" != "$last_public_ip" ]; then
  if [ -n "$last_public_ip" ]; then
    event "info" "Public IP changed from $last_public_ip to $public_ip"
  fi
  echo "$public_ip" > "$last_public_ip_file"
fi

mqtt_failures="$(cat "$publish_failures_file" 2>/dev/null || echo 0)"
outage_count="$(cat "$outage_count_file" 2>/dev/null || echo 0)"
last_publish_success="$(cat "$STATE_DIR/last_publish_success" 2>/dev/null)"
last_publish_duration="$(cat "$STATE_DIR/last_publish_duration_ms" 2>/dev/null || echo 0)"

# Individual topics, kept for backward compatibility
publish "$PROBE_TOPIC/last_update" "$now"
publish "$PROBE_TOPIC/gateway_status" "$gateway_status"
publish "$PROBE_TOPIC/pi5_status" "$pi5_status"
publish "$PROBE_TOPIC/cloudflare_status" "$cloudflare_status"
publish "$PROBE_TOPIC/google_status" "$google_status"
publish "$PROBE_TOPIC/internet_health" "$internet_health"

publish "$PROBE_TOPIC/gateway_latency_ms" "$(safe_num "$gateway_avg")"
publish "$PROBE_TOPIC/gateway_latency_min_ms" "$(safe_num "$gateway_min")"
publish "$PROBE_TOPIC/gateway_latency_max_ms" "$(safe_num "$gateway_max")"
publish "$PROBE_TOPIC/gateway_jitter_ms" "$(safe_num "$gateway_jitter")"

publish "$PROBE_TOPIC/pi5_latency_ms" "$(safe_num "$pi5_avg")"

publish "$PROBE_TOPIC/cloudflare_latency_ms" "$(safe_num "$cloudflare_avg")"
publish "$PROBE_TOPIC/cloudflare_latency_min_ms" "$(safe_num "$cloudflare_min")"
publish "$PROBE_TOPIC/cloudflare_latency_max_ms" "$(safe_num "$cloudflare_max")"
publish "$PROBE_TOPIC/cloudflare_jitter_ms" "$(safe_num "$cloudflare_jitter")"
publish "$PROBE_TOPIC/cloudflare_packet_loss_percent" "$(safe_num "$cloudflare_loss" 100)"

publish "$PROBE_TOPIC/google_latency_ms" "$(safe_num "$google_avg")"
publish "$PROBE_TOPIC/google_latency_min_ms" "$(safe_num "$google_min")"
publish "$PROBE_TOPIC/google_latency_max_ms" "$(safe_num "$google_max")"
publish "$PROBE_TOPIC/google_jitter_ms" "$(safe_num "$google_jitter")"
publish "$PROBE_TOPIC/google_packet_loss_percent" "$(safe_num "$google_loss" 100)"

publish "$PROBE_TOPIC/average_internet_latency_ms" "$(safe_num "$avg_latency")"
publish "$PROBE_TOPIC/average_packet_loss_percent" "$(safe_num "$avg_packet_loss" 100)"
publish "$PROBE_TOPIC/jitter_ms" "$(safe_num "$true_jitter")"

publish "$PROBE_TOPIC/dns_latency_local_ms" "$(safe_num "$dns_latency_local")"
publish "$PROBE_TOPIC/dns_latency_pihole_ms" "$(safe_num "$dns_latency_pihole")"
publish "$PROBE_TOPIC/dns_latency_cloudflare_ms" "$(safe_num "$dns_latency_cloudflare")"

publish "$PROBE_TOPIC/public_ip" "${public_ip:-unknown}"
publish "$PROBE_TOPIC/outage_count" "$outage_count"
publish "$PROBE_TOPIC/mqtt_publish_failures" "$mqtt_failures"
publish "$PROBE_TOPIC/mqtt_last_publish_success" "${last_publish_success:-unknown}"
publish "$PROBE_TOPIC/mqtt_last_publish_duration_ms" "$last_publish_duration"

snapshot="$(jq -n \
  --arg timestamp "$now" \
  --arg internet_health "$internet_health" \
  --arg gateway_status "$gateway_status" \
  --arg pi5_status "$pi5_status" \
  --arg public_ip "${public_ip:-unknown}" \
  --argjson gateway_latency "$(safe_num "$gateway_avg")" \
  --argjson pi5_latency "$(safe_num "$pi5_avg")" \
  --argjson cloudflare_latency "$(safe_num "$cloudflare_avg")" \
  --argjson google_latency "$(safe_num "$google_avg")" \
  --argjson average_latency "$(safe_num "$avg_latency")" \
  --argjson packet_loss "$(safe_num "$avg_packet_loss" 100)" \
  --argjson jitter "$(safe_num "$true_jitter")" \
  --argjson dns_local "$(safe_num "$dns_latency_local")" \
  --argjson dns_pihole "$(safe_num "$dns_latency_pihole")" \
  --argjson dns_cloudflare "$(safe_num "$dns_latency_cloudflare")" \
  --argjson outage_count "$outage_count" \
  --argjson mqtt_publish_failures "$mqtt_failures" \
  '{
    timestamp: $timestamp,
    internet: {
      health: $internet_health,
      public_ip: $public_ip,
      average_latency_ms: $average_latency,
      packet_loss_percent: $packet_loss,
      jitter_ms: $jitter,
      outage_count: $outage_count
    },
    gateway: {
      status: $gateway_status,
      latency_ms: $gateway_latency
    },
    pi5: {
      status: $pi5_status,
      latency_ms: $pi5_latency
    },
    targets: {
      cloudflare_latency_ms: $cloudflare_latency,
      google_latency_ms: $google_latency
    },
    dns: {
      local_ms: $dns_local,
      pihole_ms: $dns_pihole,
      cloudflare_ms: $dns_cloudflare
    },
    mqtt: {
      publish_failures: $mqtt_publish_failures
    }
  }')"

publish "$PROBE_TOPIC/state" "$snapshot"

inventory="$(jq -n \
  --arg timestamp "$now" \
  --arg gateway_status "$gateway_status" \
  --arg pi5_status "$pi5_status" \
  --arg pi5_ip "$pi5_ip" \
  --arg internet_health "$internet_health" \
  '{
    timestamp: $timestamp,
    devices: [
      {name:"Huawei Gateway", ip:"192.168.100.1", role:"Gateway", status:$gateway_status},
      {name:"Pi4 Infrastructure", ip:"192.168.100.252", role:"Pi-hole, DHCP, NUT, Probe", status:"online"},
      {name:"Pi5 Home Assistant", ip:$pi5_ip, role:"Home Assistant, MQTT, Z-Wave, Matter", status:$pi5_status},
      {name:"UPS1", role:"Power protection", status:"monitored"},
      {name:"UPS2", role:"Power protection", status:"monitored"},
      {name:"Orbi Router", role:"Mesh router/AP", status:"pending telemetry"},
      {name:"Orbi Satellite 1", role:"Mesh satellite", status:"pending telemetry"},
      {name:"Orbi Satellite 2", role:"Mesh satellite", status:"pending telemetry"},
      {name:"Cameras", role:"Security cameras", status:"pending RTSP stabilization"}
    ],
    overall_network_health: $internet_health
  }')"

publish "$INVENTORY_TOPIC/state" "$inventory"

echo "$now gateway=$gateway_status pi5=$pi5_status internet=$internet_health avg=${avg_latency}ms loss=${avg_packet_loss}% jitter=${true_jitter}ms dns=${dns_latency_pihole:-0}ms" >> "$LOG"
