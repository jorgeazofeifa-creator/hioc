#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

INSTALL_DIR="${HIOC_INSTALL_DIR:-/home/jazofv1/hioc}"
BACKUP_DIR="${1:-}"

if [ -z "$BACKUP_DIR" ] && [ -f "$INSTALL_DIR/backups/last-upgrade-backup" ]; then
  BACKUP_DIR="$(cat "$INSTALL_DIR/backups/last-upgrade-backup")"
fi

if [ -z "$BACKUP_DIR" ] || [ ! -d "$BACKUP_DIR/current" ]; then
  echo "Usage: $0 /path/to/release-upgrade-backup" >&2
  echo "No valid rollback backup found." >&2
  exit 1
fi

rsync -a "$BACKUP_DIR/current/" "$INSTALL_DIR/"
"$INSTALL_DIR/pi4/install_pi4.sh"

echo "HIOC rollback completed from $BACKUP_DIR"

