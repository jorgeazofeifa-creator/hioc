#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

TARGET="${1:-all}"

case "$TARGET" in
  all)
    installed=0
    if [ -f "${PI4_TOOLS_DIR:-/home/jazofv1/pi4-tools}/config/toolkit.conf" ]; then
      "$ROOT/pi4/install_pi4.sh"
      installed=1
    fi
    if [ -d "${HA_CONFIG:-/config}" ]; then
      "$ROOT/homeassistant/install_ha.sh"
      installed=1
    fi
    if [ "$installed" -eq 0 ]; then
      echo "No supported HIOC install target detected." >&2
      echo "Use '$0 pi4' on the Pi4 collector or '$0 ha' in Home Assistant." >&2
      exit 1
    fi
    ;;
  pi4)
    "$ROOT/pi4/install_pi4.sh"
    ;;
  ha|homeassistant)
    "$ROOT/homeassistant/install_ha.sh"
    ;;
  *)
    echo "Usage: $0 [all|pi4|ha]" >&2
    exit 1
    ;;
esac

echo "HIOC install completed for target: $TARGET"
