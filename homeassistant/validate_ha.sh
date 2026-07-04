#!/usr/bin/env bash
set -euo pipefail

HA_CONFIG="${HA_CONFIG:-/config}"
PACKAGE_DIR="$HA_CONFIG/packages"
DASHBOARD_DIR="$HA_CONFIG/dashboards"

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

check "Incident package installed" test -f "$PACKAGE_DIR/hioc_incident_center.yaml"
check "Predictive analytics package installed" test -f "$PACKAGE_DIR/hioc_predictive_analytics.yaml"
check "Living Inventory package installed" test -f "$PACKAGE_DIR/hioc_living_inventory.yaml"
check "Platform package installed" test -f "$PACKAGE_DIR/hioc_platform.yaml"
check "Living Inventory dashboard installed" test -f "$DASHBOARD_DIR/living_inventory.yaml"
check "Dashboard v2 installed" test -f "$DASHBOARD_DIR/hioc_dashboard_v2.yaml"

if command -v python3 >/dev/null 2>&1; then
  python3 - "$PACKAGE_DIR" "$DASHBOARD_DIR" <<'PY'
import pathlib
import sys
try:
    import yaml
except ImportError:
    sys.exit(0)
for root in sys.argv[1:]:
    for path in pathlib.Path(root).glob("hioc*.yaml"):
        yaml.safe_load(path.read_text())
    for path in pathlib.Path(root).glob("living_inventory.yaml"):
        yaml.safe_load(path.read_text())
PY
  echo "OK   YAML parse check"
else
  echo "SKIP YAML parse check; python3 not installed"
fi

if command -v ha >/dev/null 2>&1; then
  check "Home Assistant core config check" ha core check
else
  echo "SKIP Home Assistant core config check; ha command not installed"
fi

if [ "$failures" -eq 0 ]; then
  echo "HIOC Home Assistant validation passed."
else
  echo "HIOC Home Assistant validation failed with $failures issue(s)."
  exit 1
fi
