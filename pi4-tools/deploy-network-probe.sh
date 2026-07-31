#!/bin/bash
set -euo pipefail

SOURCE_ROOT="${HIOC_SOURCE_ROOT:-/home/jazofv1/hioc-release-source}"
EXPECTED_COMMIT="${1:-}"
RELATIVE_PATH="${2:-pi4-tools/scripts/hioc-network-probe.sh}"
TARGET="${HIOC_NETWORK_PROBE_TARGET:-/home/jazofv1/pi4-tools/scripts/hioc-network-probe.sh}"
INSTALL_OWNER="${HIOC_INSTALL_OWNER-jazofv1}"
INSTALL_GROUP="${HIOC_INSTALL_GROUP-jazofv1}"
SOURCE="$SOURCE_ROOT/$RELATIVE_PATH"
TARGET_DIR="$(dirname "$TARGET")"

[ -n "$EXPECTED_COMMIT" ] || { echo "Usage: $0 EXPECTED_COMMIT [REPOSITORY_RELATIVE_PATH]" >&2; exit 2; }
[ "$RELATIVE_PATH" = "pi4-tools/scripts/hioc-network-probe.sh" ] || { echo "ERROR: unexpected network-probe source path" >&2; exit 2; }
[ -d "$SOURCE_ROOT/.git" ] || { echo "ERROR: source root is not a Git checkout" >&2; exit 2; }
resolved_commit="$(git -C "$SOURCE_ROOT" rev-parse --verify "$EXPECTED_COMMIT^{commit}")" ||
  { echo "ERROR: expected commit does not exist" >&2; exit 2; }
[ "$EXPECTED_COMMIT" = "$resolved_commit" ] || { echo "ERROR: expected commit must be a full, exact commit SHA" >&2; exit 2; }
head_commit="$(git -C "$SOURCE_ROOT" rev-parse HEAD)"
[ "$head_commit" = "$EXPECTED_COMMIT" ] || { echo "ERROR: HEAD does not equal approved commit" >&2; exit 2; }
[ -z "$(git -C "$SOURCE_ROOT" status --porcelain --untracked-files=all)" ] ||
  { echo "ERROR: source repository is dirty" >&2; exit 2; }

tree_entry="$(git -C "$SOURCE_ROOT" ls-tree "$EXPECTED_COMMIT" -- "$RELATIVE_PATH")"
mode="$(printf '%s\n' "$tree_entry" | awk '{print $1}')"
type="$(printf '%s\n' "$tree_entry" | awk '{print $2}')"
blob="$(printf '%s\n' "$tree_entry" | awk '{print $3}')"
[ "$type" = "blob" ] && [ -n "$blob" ] || { echo "ERROR: source is not a tracked Git blob" >&2; exit 2; }
[ "$mode" = "100755" ] || { echo "ERROR: governed source Git mode must be 100755" >&2; exit 2; }
[ -f "$SOURCE" ] || { echo "ERROR: governed source missing: $SOURCE" >&2; exit 2; }
[ -d "$TARGET_DIR" ] || { echo "ERROR: target directory missing: $TARGET_DIR" >&2; exit 2; }

blob_temporary="$(mktemp)"
cleanup() {
  [ ! -e "${temporary:-}" ] || rm -f -- "$temporary"
  rm -f -- "$blob_temporary"
}
trap cleanup EXIT
git -C "$SOURCE_ROOT" cat-file blob "$blob" >"$blob_temporary"
cmp -s -- "$blob_temporary" "$SOURCE" || { echo "ERROR: working-tree source differs byte-for-byte from approved Git blob" >&2; exit 2; }
bash -n "$SOURCE"

timestamp="$(date '+%Y%m%dT%H%M%S')"
backup="$TARGET.$timestamp.backup"
temporary="$TARGET_DIR/.hioc-network-probe.$timestamp.$$"

if [ -e "$TARGET" ]; then
  cp -p -- "$TARGET" "$backup" || { echo "ERROR: backup failed" >&2; exit 3; }
  echo "Backup: $backup"
fi

install_args=(-m 0755)
[ -z "$INSTALL_OWNER" ] || install_args+=(-o "$INSTALL_OWNER")
[ -z "$INSTALL_GROUP" ] || install_args+=(-g "$INSTALL_GROUP")
install "${install_args[@]}" -- "$blob_temporary" "$temporary"
bash -n "$temporary"
mv -f -- "$temporary" "$TARGET"

blob_sha="$(sha256sum "$blob_temporary" | awk '{print $1}')"
source_sha="$(sha256sum "$SOURCE" | awk '{print $1}')"
target_sha="$(sha256sum "$TARGET" | awk '{print $1}')"
cmp -s -- "$blob_temporary" "$TARGET" || { echo "ERROR: deployed file differs from approved Git blob" >&2; exit 3; }
[ "$(stat -c '%a' "$TARGET")" = "755" ] || { echo "ERROR: deployed mode is not 0755" >&2; exit 3; }
if [ -n "$INSTALL_OWNER" ]; then [ "$(stat -c '%U' "$TARGET")" = "$INSTALL_OWNER" ] || { echo "ERROR: deployed owner mismatch" >&2; exit 3; }; fi
if [ -n "$INSTALL_GROUP" ]; then [ "$(stat -c '%G' "$TARGET")" = "$INSTALL_GROUP" ] || { echo "ERROR: deployed group mismatch" >&2; exit 3; }; fi
printf 'Commit: %s\nPath: %s\nGit blob: %s\nGit blob SHA-256: %s\nWorking-tree SHA-256: %s\nDeployed SHA-256: %s\nBackup: %s\n' \
  "$EXPECTED_COMMIT" "$RELATIVE_PATH" "$blob" "$blob_sha" "$source_sha" "$target_sha" "${backup:-none}"
echo "Network probe deployment: PASS"
