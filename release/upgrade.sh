#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "$ROOT/release/lib.sh"

INSTALL_DIR="${HIOC_INSTALL_DIR:-/home/jazofv1/hioc}"
BACKUP_DIR="$INSTALL_DIR/backups/release-upgrade-$(hioc_timestamp)"

hioc_require rsync

if [ ! -d "$INSTALL_DIR" ]; then
  echo "Install directory does not exist: $INSTALL_DIR" >&2
  echo "Run release/install.sh first." >&2
  exit 1
fi

mkdir -p "$BACKUP_DIR"
rsync -a \
  --exclude state \
  --exclude history \
  --exclude logs \
  --exclude backups \
  "$INSTALL_DIR/" "$BACKUP_DIR/current/"

rsync -a \
  --exclude .git \
  --exclude dist \
  --exclude state \
  --exclude history \
  --exclude logs \
  --exclude backups \
  "$ROOT/" "$INSTALL_DIR/"

"$INSTALL_DIR/pi4/install_pi4.sh"

echo "$BACKUP_DIR" > "$INSTALL_DIR/backups/last-upgrade-backup"
echo "HIOC upgrade completed."
echo "Backup directory: $BACKUP_DIR"

