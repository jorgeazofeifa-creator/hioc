#!/usr/bin/env bash
set -euo pipefail

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INSTALL_DIR="${HIOC_INSTALL_DIR:-/home/jazofv1/hioc}"
PI4_TOOLS_DIR="${PI4_TOOLS_DIR:-/home/jazofv1/pi4-tools}"
BACKUP_DIR="$INSTALL_DIR/backups/install-$(date +%Y%m%d-%H%M%S)"
CRON_LINE="*/1 * * * * flock -n /tmp/hioc-incident-engine.lock $INSTALL_DIR/pi4/bin/hioc-incident-engine.sh"

require() {
  command -v "$1" >/dev/null 2>&1 || { echo "Missing required command: $1" >&2; exit 1; }
}

require jq
require mosquitto_pub
require mosquitto_sub
require flock

if [ ! -f "$PI4_TOOLS_DIR/config/toolkit.conf" ]; then
  echo "Cannot find $PI4_TOOLS_DIR/config/toolkit.conf"
  echo "HIOC v1.0.0-core expects your existing Pi4 toolkit and MQTT config."
  exit 1
fi

mkdir -p "$INSTALL_DIR" "$BACKUP_DIR"

if [ "$SRC_DIR" != "$INSTALL_DIR" ]; then
  rsync -a --exclude .git "$SRC_DIR/" "$INSTALL_DIR/"
fi

mkdir -p "$INSTALL_DIR/config" "$INSTALL_DIR/state/incidents" "$INSTALL_DIR/logs"

if [ ! -f "$INSTALL_DIR/config/hioc.conf" ]; then
  cp "$INSTALL_DIR/pi4/config/hioc.conf.example" "$INSTALL_DIR/config/hioc.conf"
fi

chmod +x "$INSTALL_DIR/pi4/bin/hioc-incident-engine.sh"
chmod +x "$INSTALL_DIR/pi4/validate_pi4.sh"
chmod +x "$INSTALL_DIR/pi4/uninstall_pi4.sh"

crontab -l > "$BACKUP_DIR/crontab.before" 2>/dev/null || true
if ! crontab -l 2>/dev/null | grep -Fq "$INSTALL_DIR/pi4/bin/hioc-incident-engine.sh"; then
  (crontab -l 2>/dev/null; echo "$CRON_LINE") | crontab -
fi

"$INSTALL_DIR/pi4/bin/hioc-incident-engine.sh"

echo "HIOC v1.0.0-core installed on Pi4."
echo "Install directory: $INSTALL_DIR"
echo "Backup directory: $BACKUP_DIR"
echo "Next: run $INSTALL_DIR/pi4/validate_pi4.sh"
