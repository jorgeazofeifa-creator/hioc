from dataclasses import dataclass
from pathlib import Path
import os
from typing import Optional


@dataclass(frozen=True)
class ConfigOption:
    name: str
    default: str
    description: str


CORE_OPTIONS = [
    ConfigOption("HIOC_HOME", "/home/jazofv1/hioc", "HIOC installation directory"),
    ConfigOption("PI4_TOOLS_HOME", "/home/jazofv1/pi4-tools", "Existing Pi4 toolkit directory"),
    ConfigOption("HIOC_BASE_TOPIC", "home/infrastructure/hioc", "HIOC MQTT base topic"),
    ConfigOption("HIOC_EVENT_RETENTION", "500", "Maximum retained internal events"),
    ConfigOption("HIOC_LOG_LEVEL", "INFO", "Minimum engine log level"),
]


def read_shell_config(path: Path) -> dict[str, str]:
    values = {}
    if not path.exists():
        return values
    for raw in path.read_text(errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


class ConfigService:
    def __init__(self, defaults: Optional[dict[str, str]] = None):
        self.defaults = {option.name: option.default for option in CORE_OPTIONS}
        if defaults:
            self.defaults.update(defaults)

    def load(self) -> dict[str, str]:
        home = Path(os.environ.get("HIOC_HOME", self.defaults["HIOC_HOME"]))
        tools = Path(os.environ.get("PI4_TOOLS_HOME", self.defaults["PI4_TOOLS_HOME"]))
        values = dict(self.defaults)
        values.update(read_shell_config(tools / "config" / "toolkit.conf"))
        values.update(read_shell_config(home / "config" / "hioc.conf"))
        values.update({key: value for key, value in os.environ.items() if key.startswith("HIOC_") or key.startswith("MQTT_")})
        values["HIOC_HOME"] = os.environ.get("HIOC_HOME", values.get("HIOC_HOME", self.defaults["HIOC_HOME"]))
        values["PI4_TOOLS_HOME"] = os.environ.get("PI4_TOOLS_HOME", values.get("PI4_TOOLS_HOME", self.defaults["PI4_TOOLS_HOME"]))
        return values

    @staticmethod
    def as_bool(config: dict[str, str], key: str, default: bool = False) -> bool:
        value = str(config.get(key, "on" if default else "off")).lower()
        return value in ("1", "true", "yes", "on", "enabled")

    @staticmethod
    def as_int(config: dict[str, str], key: str, default: int) -> int:
        try:
            return int(str(config.get(key, default)).strip())
        except ValueError:
            return default
