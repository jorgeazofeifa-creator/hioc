#!/usr/bin/env bash
set -euo pipefail

hioc_release_dir() {
  cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd
}

hioc_version_value() {
  local key="$1"
  local root="${2:-$(hioc_release_dir)}"
  awk -F: -v key="$key" '$1 == key {gsub(/^[ \t]+|[ \t]+$/, "", $2); print $2}' "$root/VERSION.yaml"
}

hioc_require() {
  local missing=0
  for cmd in "$@"; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
      echo "Missing required command: $cmd" >&2
      missing=1
    fi
  done
  [ "$missing" -eq 0 ]
}

hioc_timestamp() {
  date +%Y%m%d-%H%M%S
}

