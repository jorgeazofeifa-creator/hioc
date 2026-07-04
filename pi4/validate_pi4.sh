#!/usr/bin/env bash
set -euo pipefail

INSTALL_DIR="${HIOC_INSTALL_DIR:-/home/jazofv1/hioc}"
PI4_TOOLS_DIR="${PI4_TOOLS_DIR:-/home/jazofv1/pi4-tools}"
source "$INSTALL_DIR/pi4/lib/hioc-common.sh"

failures=0
check() {
  local name="$1"
  shift
  if "$@" >/dev/null 2>&1; then
    echo "OK   $name"
  else
    echo "FAIL $name"
    failures=$((failures + 1))
  fi
}

check "jq installed" command -v jq
check "python3 installed" command -v python3
check "mosquitto_pub installed" command -v mosquitto_pub
check "mosquitto_sub installed" command -v mosquitto_sub
check "Pi4 toolkit config exists" test -f "$PI4_TOOLS_DIR/config/toolkit.conf"
check "HIOC config exists" test -f "$INSTALL_DIR/config/hioc.conf"
check "Incident engine v2 executable" test -x "$INSTALL_DIR/pi4/bin/hioc-incident-engine-v2.py"
check "History engine executable" test -x "$INSTALL_DIR/pi4/bin/hioc-history-engine.py"
check "Inventory engine executable" test -x "$INSTALL_DIR/pi4/bin/hioc-inventory-engine.py"
check "Platform status executable" test -x "$INSTALL_DIR/pi4/bin/hioc-platform-status.py"
check "Version manifest exists" test -f "$INSTALL_DIR/VERSION.yaml"
check "Active incident JSON exists" test -f "$INSTALL_DIR/state/incidents/active.json"
check "Incident history JSON exists" test -f "$INSTALL_DIR/state/incidents/history.json"
check "Incident summary JSON exists" test -f "$INSTALL_DIR/state/incidents/summary.json"
check "Inventory JSON exists" test -f "$INSTALL_DIR/state/inventory/inventory.json"
check "Inventory devices JSON exists" test -f "$INSTALL_DIR/state/inventory/devices.json"
check "Inventory summary JSON exists" test -f "$INSTALL_DIR/state/inventory/summary.json"
check "Inventory capabilities JSON exists" test -f "$INSTALL_DIR/state/inventory/capabilities.json"
check "Internal event log exists" test -f "$INSTALL_DIR/state/events/events.json"
check "Platform version JSON exists" test -f "$INSTALL_DIR/state/platform/version.json"
check "Platform status JSON exists" test -f "$INSTALL_DIR/state/platform/status.json"
check "Incident engine cron installed" bash -c "crontab -l 2>/dev/null | grep -Fq '$INSTALL_DIR/pi4/bin/hioc-incident-engine-v2.py'"
check "History engine cron installed" bash -c "crontab -l 2>/dev/null | grep -Fq '$INSTALL_DIR/pi4/bin/hioc-history-engine.py'"
check "Inventory engine cron installed" bash -c "crontab -l 2>/dev/null | grep -Fq '$INSTALL_DIR/pi4/bin/hioc-inventory-engine.py'"
check "Platform status cron installed" bash -c "crontab -l 2>/dev/null | grep -Fq '$INSTALL_DIR/pi4/bin/hioc-platform-status.py'"

if [ -f "$INSTALL_DIR/state/incidents/active.json" ]; then
  check "Active incident JSON valid" jq empty "$INSTALL_DIR/state/incidents/active.json"
fi
if [ -f "$INSTALL_DIR/state/incidents/history.json" ]; then
  check "Incident history JSON valid" jq empty "$INSTALL_DIR/state/incidents/history.json"
fi
if [ -f "$INSTALL_DIR/state/incidents/summary.json" ]; then
  check "Incident summary JSON valid" jq empty "$INSTALL_DIR/state/incidents/summary.json"
fi
if [ -f "$INSTALL_DIR/state/inventory/inventory.json" ]; then
  check "Inventory JSON valid" jq empty "$INSTALL_DIR/state/inventory/inventory.json"
fi
if [ -f "$INSTALL_DIR/state/inventory/devices.json" ]; then
  check "Inventory devices JSON valid" jq empty "$INSTALL_DIR/state/inventory/devices.json"
fi
if [ -f "$INSTALL_DIR/state/inventory/summary.json" ]; then
  check "Inventory summary JSON valid" jq empty "$INSTALL_DIR/state/inventory/summary.json"
fi
if [ -f "$INSTALL_DIR/state/inventory/capabilities.json" ]; then
  check "Inventory capabilities JSON valid" jq empty "$INSTALL_DIR/state/inventory/capabilities.json"
fi
if [ -f "$INSTALL_DIR/state/events/events.json" ]; then
  check "Internal event log JSON valid" jq empty "$INSTALL_DIR/state/events/events.json"
fi
if [ -f "$INSTALL_DIR/state/platform/version.json" ]; then
  check "Platform version JSON valid" jq empty "$INSTALL_DIR/state/platform/version.json"
fi
if [ -f "$INSTALL_DIR/state/platform/status.json" ]; then
  check "Platform status JSON valid" jq empty "$INSTALL_DIR/state/platform/status.json"
fi

if [ "$failures" -eq 0 ]; then
  echo "HIOC Pi4 validation passed."
else
  echo "HIOC Pi4 validation failed with $failures issue(s)."
  exit 1
fi
