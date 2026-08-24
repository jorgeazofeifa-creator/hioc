#!/usr/bin/env bash
set -euo pipefail

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INSTALL_DIR="${HIOC_INSTALL_DIR:-/home/jazofv1/hioc}"
PI4_TOOLS_DIR="${PI4_TOOLS_DIR:-/home/jazofv1/pi4-tools}"
BACKUP_DIR="$INSTALL_DIR/backups/install-$(date +%Y%m%d-%H%M%S)"
CRON_INCIDENT="*/1 * * * * flock -n /tmp/hioc-incident-engine.lock $INSTALL_DIR/pi4/bin/hioc-incident-engine-v2.py"
CRON_HISTORY="*/5 * * * * flock -n /tmp/hioc-history-engine.lock $INSTALL_DIR/pi4/bin/hioc-history-engine.py"
CRON_INVENTORY="*/30 * * * * flock -n /tmp/hioc-inventory-engine.lock $INSTALL_DIR/pi4/bin/hioc-inventory-engine.py"
CRON_PLATFORM="17 3 * * * flock -n /tmp/hioc-platform-status.lock $INSTALL_DIR/pi4/bin/hioc-platform-status.py"

require() {
  command -v "$1" >/dev/null 2>&1 || { echo "Missing required command: $1" >&2; exit 1; }
}

require jq
require mosquitto_pub
require mosquitto_sub
require flock
require python3

if [ ! -f "$PI4_TOOLS_DIR/config/toolkit.conf" ]; then
  echo "Cannot find $PI4_TOOLS_DIR/config/toolkit.conf"
  echo "HIOC expects your existing Pi4 toolkit and MQTT config."
  exit 1
fi

mkdir -p "$INSTALL_DIR" "$BACKUP_DIR"

if [ "$SRC_DIR" != "$INSTALL_DIR" ]; then
  rsync -a \
    --exclude .git \
    --exclude '/README.md' \
    --exclude '/ROADMAP.md' \
    --exclude '/DECISIONS.md' \
    --exclude '/CHANGELOG.md' \
    --exclude '/docs/' \
    --exclude '/tests/' \
    --exclude '/data/manufacturer/' \
    --exclude '/runtime/pe4/' \
    "$SRC_DIR/" "$INSTALL_DIR/"
fi

mkdir -p "$INSTALL_DIR/config" "$INSTALL_DIR/state/incidents" "$INSTALL_DIR/history" "$INSTALL_DIR/logs"
mkdir -p "$INSTALL_DIR/state/inventory"
mkdir -p "$INSTALL_DIR/state/platform"
mkdir -p "$INSTALL_DIR/backups/assets"
mkdir -p "$INSTALL_DIR/data/manufacturer/versions"
chmod 0750 "$INSTALL_DIR/state/inventory"
chmod 0700 "$INSTALL_DIR/backups/assets"
chmod 0700 "$INSTALL_DIR/data/manufacturer" "$INSTALL_DIR/data/manufacturer/versions"
if [ -f "$INSTALL_DIR/state/inventory/assets.json" ]; then chmod 0600 "$INSTALL_DIR/state/inventory/assets.json"; fi
if [ -f "$INSTALL_DIR/state/inventory/assets_status.json" ]; then chmod 0600 "$INSTALL_DIR/state/inventory/assets_status.json"; fi
if [ -f "$INSTALL_DIR/state/inventory/manufacturer.json" ]; then chmod 0600 "$INSTALL_DIR/state/inventory/manufacturer.json"; fi
if [ -f "$INSTALL_DIR/state/inventory/manufacturer_status.json" ]; then chmod 0600 "$INSTALL_DIR/state/inventory/manufacturer_status.json"; fi

if [ ! -f "$INSTALL_DIR/config/hioc.conf" ]; then
  cp "$INSTALL_DIR/pi4/config/hioc.conf.example" "$INSTALL_DIR/config/hioc.conf"
fi

chmod +x "$INSTALL_DIR/pi4/bin/hioc-incident-engine.sh"
chmod +x "$INSTALL_DIR/pi4/bin/hioc-incident-engine-v2.py"
chmod +x "$INSTALL_DIR/pi4/bin/hioc-history-engine.py"
chmod +x "$INSTALL_DIR/pi4/bin/hioc-inventory-engine.py"
chmod +x "$INSTALL_DIR/pi4/bin/hioc-platform-status.py"
chmod +x "$INSTALL_DIR/pi4/bin/hioc-validate-mqtt.py"
chmod +x "$INSTALL_DIR/pi4/bin/hioc-assets.py"
chmod +x "$INSTALL_DIR/pi4/bin/hioc-validate-assets.py"
chmod 0600 "$INSTALL_DIR/pi4/lib/hioc/manufacturer.py"
chmod 0700 "$INSTALL_DIR/pi4/bin/hioc-build-manufacturer-db.py"
chmod 0700 "$INSTALL_DIR/pi4/bin/hioc-validate-manufacturer.py"
chmod 0700 "$INSTALL_DIR/pi4/bin/hioc-generate-manufacturer.py"
chmod +x "$INSTALL_DIR/pi4/validate_pi4.sh"
chmod +x "$INSTALL_DIR/pi4/uninstall_pi4.sh"

# PE-2 runtime permissions are owned by one machine-readable deployment policy.
PE2_ARTIFACT_CONTRACT="$INSTALL_DIR/pi4/config/pe2_artifacts.json"
if [ -f "$PE2_ARTIFACT_CONTRACT" ]; then
  while IFS=$'\t' read -r artifact_path artifact_mode; do
    [ -n "$artifact_path" ] || continue
    chmod "$artifact_mode" "$INSTALL_DIR/$artifact_path"
  done < <(jq -r '.artifacts[] | [.path, .runtime_mode] | @tsv' "$PE2_ARTIFACT_CONTRACT")
fi

crontab -l > "$BACKUP_DIR/crontab.before" 2>/dev/null || true
current_cron="$(crontab -l 2>/dev/null || true)"
current_cron="$(printf '%s\n' "$current_cron" | grep -Fv "$INSTALL_DIR/pi4/bin/hioc-incident-engine.sh" | grep -Fv "$INSTALL_DIR/pi4/bin/hioc-incident-engine-v2.py" || true)"
(printf '%s\n' "$current_cron"; echo "$CRON_INCIDENT") | sed '/^$/d' | crontab -

current_cron="$(crontab -l 2>/dev/null || true)"
if ! printf '%s\n' "$current_cron" | grep -Fq "$INSTALL_DIR/pi4/bin/hioc-history-engine.py"; then
  (printf '%s\n' "$current_cron"; echo "$CRON_HISTORY") | sed '/^$/d' | crontab -
fi

current_cron="$(crontab -l 2>/dev/null || true)"
if ! printf '%s\n' "$current_cron" | grep -Fq "$INSTALL_DIR/pi4/bin/hioc-inventory-engine.py"; then
  (printf '%s\n' "$current_cron"; echo "$CRON_INVENTORY") | sed '/^$/d' | crontab -
fi

current_cron="$(crontab -l 2>/dev/null || true)"
if ! printf '%s\n' "$current_cron" | grep -Fq "$INSTALL_DIR/pi4/bin/hioc-platform-status.py"; then
  (printf '%s\n' "$current_cron"; echo "$CRON_PLATFORM") | sed '/^$/d' | crontab -
fi

"$INSTALL_DIR/pi4/bin/hioc-incident-engine-v2.py"
"$INSTALL_DIR/pi4/bin/hioc-history-engine.py"
"$INSTALL_DIR/pi4/bin/hioc-inventory-engine.py"
"$INSTALL_DIR/pi4/bin/hioc-platform-status.py"

echo "HIOC installed on Pi4."
echo "Install directory: $INSTALL_DIR"
echo "Backup directory: $BACKUP_DIR"
echo "Next: run $INSTALL_DIR/pi4/validate_pi4.sh"
