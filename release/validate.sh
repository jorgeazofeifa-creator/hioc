#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "$ROOT/release/lib.sh"

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

check "VERSION.yaml exists" test -f "$ROOT/VERSION.yaml"
for key in hioc_version core incident_engine correlation_engine forecast_engine inventory_engine dashboard schema mqtt_api installer build; do
  check "VERSION has $key" bash -c "[ -n \"$(hioc_version_value "$key" "$ROOT")\" ]"
done

check "Pi4 installer exists" test -f "$ROOT/pi4/install_pi4.sh"
check "Pi4 validator exists" test -f "$ROOT/pi4/validate_pi4.sh"
check "HA installer exists" test -f "$ROOT/homeassistant/install_ha.sh"
check "HA validator exists" test -f "$ROOT/homeassistant/validate_ha.sh"
check "Dashboard v2 exists" test -f "$ROOT/homeassistant/dashboards/hioc_dashboard_v2.yaml"
check "Platform status executable exists" test -f "$ROOT/pi4/bin/hioc-platform-status.py"

if command -v python3 >/dev/null 2>&1; then
  check "Python files compile" python3 -m compileall -q "$ROOT/pi4/bin" "$ROOT/pi4/lib" "$ROOT/tests"
else
  echo "SKIP Python compile; python3 not installed"
fi

if command -v bash >/dev/null 2>&1; then
  while IFS= read -r script; do
    check "Shell syntax $script" bash -n "$script"
  done < <(find "$ROOT" -path "$ROOT/dist" -prune -o -name "*.sh" -type f -print)
fi

if [ "$failures" -eq 0 ]; then
  echo "HIOC release validation passed."
else
  echo "HIOC release validation failed with $failures issue(s)."
  exit 1
fi
