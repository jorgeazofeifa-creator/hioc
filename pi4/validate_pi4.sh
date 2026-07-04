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
check "Active incident JSON exists" test -f "$INSTALL_DIR/state/incidents/active.json"
check "Incident history JSON exists" test -f "$INSTALL_DIR/state/incidents/history.json"
check "Incident summary JSON exists" test -f "$INSTALL_DIR/state/incidents/summary.json"
check "Incident engine cron installed" bash -c "crontab -l 2>/dev/null | grep -Fq '$INSTALL_DIR/pi4/bin/hioc-incident-engine-v2.py'"
check "History engine cron installed" bash -c "crontab -l 2>/dev/null | grep -Fq '$INSTALL_DIR/pi4/bin/hioc-history-engine.py'"

if [ -f "$INSTALL_DIR/state/incidents/active.json" ]; then
  check "Active incident JSON valid" jq empty "$INSTALL_DIR/state/incidents/active.json"
fi
if [ -f "$INSTALL_DIR/state/incidents/history.json" ]; then
  check "Incident history JSON valid" jq empty "$INSTALL_DIR/state/incidents/history.json"
fi
if [ -f "$INSTALL_DIR/state/incidents/summary.json" ]; then
  check "Incident summary JSON valid" jq empty "$INSTALL_DIR/state/incidents/summary.json"
fi

if [ "$failures" -eq 0 ]; then
  echo "HIOC Pi4 validation passed."
else
  echo "HIOC Pi4 validation failed with $failures issue(s)."
  exit 1
fi
