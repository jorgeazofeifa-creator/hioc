#!/usr/bin/env bash
set -euo pipefail

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HA_CONFIG="${HA_CONFIG:-/config}"
PACKAGE_DIR="$HA_CONFIG/packages"
DASHBOARD_DIR="$HA_CONFIG/dashboards"
BACKUP_DIR="$HA_CONFIG/backups/hioc-$(date +%Y%m%d-%H%M%S)"

mkdir -p "$PACKAGE_DIR" "$DASHBOARD_DIR" "$BACKUP_DIR"

for package in "$SRC_DIR"/packages/*.yaml; do
  name="$(basename "$package")"
  if [ -f "$PACKAGE_DIR/$name" ]; then
    cp "$PACKAGE_DIR/$name" "$BACKUP_DIR/$name.before"
  fi
  cp "$package" "$PACKAGE_DIR/$name"
  echo "Installed $PACKAGE_DIR/$name"
done

for dashboard in "$SRC_DIR"/dashboards/*.yaml; do
  name="$(basename "$dashboard")"
  if [ -f "$DASHBOARD_DIR/$name" ]; then
    cp "$DASHBOARD_DIR/$name" "$BACKUP_DIR/$name.before"
  fi
  cp "$dashboard" "$DASHBOARD_DIR/$name"
  echo "Installed $DASHBOARD_DIR/$name"
done

echo "Backup directory: $BACKUP_DIR"
echo "Run: bash homeassistant/validate_ha.sh"
echo "Run: ha core check"
echo "Then: ha core restart"
