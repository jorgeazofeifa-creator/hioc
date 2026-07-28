#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "$ROOT/release/lib.sh"

VERSION="$(hioc_version_value hioc_version "$ROOT")"
BUILD_DIR="$ROOT/dist/build/HIOC-$VERSION"

hioc_require awk git

rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

git -C "$ROOT" ls-files --cached -z -- | while IFS= read -r -d '' rel; do
  file="$ROOT/$rel"
  mkdir -p "$BUILD_DIR/$(dirname "$rel")"
  cp "$file" "$BUILD_DIR/$rel"
done

cat > "$BUILD_DIR/RELEASE_MANIFEST.txt" <<EOF
artifact=HIOC-$VERSION
hioc_version=$VERSION
build=$(hioc_version_value build "$ROOT")
source_commit=$(git -C "$ROOT" rev-parse HEAD)
EOF

echo "Built $BUILD_DIR"
