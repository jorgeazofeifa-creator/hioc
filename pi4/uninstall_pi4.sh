#!/usr/bin/env bash
set -euo pipefail

INSTALL_DIR="${HIOC_INSTALL_DIR:-/home/jazofv1/hioc}"
TARGET="$INSTALL_DIR/pi4/bin/hioc-incident-engine.sh"
TARGET_V2="$INSTALL_DIR/pi4/bin/hioc-incident-engine-v2.py"
TARGET_HISTORY="$INSTALL_DIR/pi4/bin/hioc-history-engine.py"
TARGET_INVENTORY="$INSTALL_DIR/pi4/bin/hioc-inventory-engine.py"
TARGET_PLATFORM="$INSTALL_DIR/pi4/bin/hioc-platform-status.py"
BACKUP_DIR="$INSTALL_DIR/backups/uninstall-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"

crontab -l > "$BACKUP_DIR/crontab.before" 2>/dev/null || true
crontab -l 2>/dev/null \
  | grep -Fv "$TARGET" \
  | grep -Fv "$TARGET_V2" \
  | grep -Fv "$TARGET_HISTORY" \
  | grep -Fv "$TARGET_INVENTORY" \
  | grep -Fv "$TARGET_PLATFORM" \
  | crontab - || true

echo "HIOC Pi4 cron entries removed."
echo "State files were not deleted."
echo "Backup directory: $BACKUP_DIR"
