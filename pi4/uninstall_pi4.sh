#!/usr/bin/env bash
set -euo pipefail

INSTALL_DIR="${HIOC_INSTALL_DIR:-/home/jazofv1/hioc}"
TARGET="$INSTALL_DIR/pi4/bin/hioc-incident-engine.sh"
BACKUP_DIR="$INSTALL_DIR/backups/uninstall-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"

crontab -l > "$BACKUP_DIR/crontab.before" 2>/dev/null || true
crontab -l 2>/dev/null | grep -Fv "$TARGET" | crontab - || true

echo "HIOC Pi4 cron entry removed."
echo "State files were not deleted."
echo "Backup directory: $BACKUP_DIR"
