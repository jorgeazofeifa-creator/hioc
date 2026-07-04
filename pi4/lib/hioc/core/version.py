from pathlib import Path


REQUIRED_VERSION_KEYS = [
    "hioc_version",
    "core",
    "incident_engine",
    "forecast_engine",
    "inventory_engine",
    "dashboard",
    "schema",
    "mqtt_api",
    "installer",
    "build",
]


def read_version_manifest(path: Path) -> dict:
    values = {}
    if not path.exists():
        raise FileNotFoundError(f"Version manifest not found: {path}")
    for raw in path.read_text(errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    missing = [key for key in REQUIRED_VERSION_KEYS if key not in values]
    if missing:
        raise ValueError(f"Version manifest missing required keys: {', '.join(missing)}")
    return values

