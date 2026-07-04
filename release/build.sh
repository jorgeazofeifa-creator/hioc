#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "$ROOT/release/lib.sh"

VERSION="$(hioc_version_value hioc_version "$ROOT")"
BUILD_DIR="$ROOT/dist/build/HIOC-$VERSION"

hioc_require awk find

rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

find "$ROOT" \
  -path "$ROOT/.git" -prune -o \
  -path "$ROOT/dist" -prune -o \
  -path "$ROOT/state" -prune -o \
  -path "$ROOT/backups" -prune -o \
  -path "$ROOT/logs" -prune -o \
  -path "*/__pycache__" -prune -o \
  -type f -print | while IFS= read -r file; do
    rel="${file#$ROOT/}"
    mkdir -p "$BUILD_DIR/$(dirname "$rel")"
    cp "$file" "$BUILD_DIR/$rel"
  done

cat > "$BUILD_DIR/RELEASE_MANIFEST.txt" <<EOF
artifact=HIOC-$VERSION
hioc_version=$VERSION
build=$(hioc_version_value build "$ROOT")
created=$(date -Iseconds)
source_root=$ROOT
EOF

echo "Built $BUILD_DIR"

