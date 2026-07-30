#!/bin/bash
set -euo pipefail

SOURCE_ROOT="${HIOC_SOURCE_ROOT:-/home/jazofv1/hioc-release-source}"
SOURCE="$SOURCE_ROOT/pi4-tools/scripts/hioc-network-probe.sh"
TARGET="/home/jazofv1/pi4-tools/scripts/hioc-network-probe.sh"
TARGET_DIR="$(dirname "$TARGET")"

[ -f "$SOURCE" ] || { echo "ERROR: governed source missing: $SOURCE" >&2; exit 2; }
[ -d "$TARGET_DIR" ] || { echo "ERROR: target directory missing: $TARGET_DIR" >&2; exit 2; }
bash -n "$SOURCE"

timestamp="$(date '+%Y%m%dT%H%M%S')"
backup="$TARGET.$timestamp.backup"
temporary="$TARGET_DIR/.hioc-network-probe.$timestamp.$$"

cleanup() {
  [ ! -e "$temporary" ] || rm -f -- "$temporary"
}
trap cleanup EXIT

if [ -e "$TARGET" ]; then
  cp -p -- "$TARGET" "$backup"
  echo "Backup: $backup"
fi

install -o jazofv1 -g jazofv1 -m 0755 -- "$SOURCE" "$temporary"
bash -n "$temporary"
mv -f -- "$temporary" "$TARGET"
trap - EXIT

source_sha="$(sha256sum "$SOURCE" | awk '{print $1}')"
target_sha="$(sha256sum "$TARGET" | awk '{print $1}')"
printf 'Source SHA-256:   %s\nDeployed SHA-256: %s\n' "$source_sha" "$target_sha"
[ "$source_sha" = "$target_sha" ] || { echo "ERROR: deployed checksum mismatch" >&2; exit 3; }
echo "Network probe deployment: PASS"
