#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "$ROOT/release/lib.sh"

hioc_require tar awk

VERSION="$(hioc_version_value hioc_version "$ROOT")"
BUILD_DIR="$ROOT/dist/build/HIOC-$VERSION"
PACKAGE_DIR="$ROOT/dist/packages"
PACKAGE="$PACKAGE_DIR/HIOC-$VERSION.tar.gz"

if [ ! -d "$BUILD_DIR" ]; then
  "$ROOT/release/build.sh"
fi

mkdir -p "$PACKAGE_DIR"
tar -czf "$PACKAGE" -C "$ROOT/dist/build" "HIOC-$VERSION"

echo "Packaged $PACKAGE"

