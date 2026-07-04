#!/usr/bin/env bash
set -euo pipefail

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HA_CONFIG="${HA_CONFIG:-/config}"
PACKAGE_DIR="$HA_CONFIG/packages"
BACKUP_DIR="$HA_CONFIG/backups/hioc-$(date +%Y%m%d-%H%M%S)"

mkdir -p "$PACKAGE_DIR" "$BACKUP_DIR"

if [ -f "$PACKAGE_DIR/hioc_incident_center.yaml" ]; then
  cp "$PACKAGE_DIR/hioc_incident_center.yaml" "$BACKUP_DIR/hioc_incident_center.yaml.before"
fi

cp "$SRC_DIR/packages/hioc_incident_center.yaml" "$PACKAGE_DIR/hioc_incident_center.yaml"

echo "Installed Home Assistant HIOC package to $PACKAGE_DIR/hioc_incident_center.yaml"
echo "Backup directory: $BACKUP_DIR"
echo "Run: ha core check"
echo "Then: ha core restart"
