from .core.config import ConfigService


DEFAULTS = {
    "HIOC_HOME": "/home/jazofv1/hioc",
    "PI4_TOOLS_HOME": "/home/jazofv1/pi4-tools",
    "HIOC_BASE_TOPIC": "home/infrastructure/hioc",
    "HIOC_LEGACY_BASE_TOPIC": "home/infrastructure/pi4",
    "HIOC_INVENTORY_SCAN_SUBNET": "",
    "HIOC_INVENTORY_ACTIVE_DISCOVERY": "off",
    "HIOC_INVENTORY_PING_COUNT": "1",
    "HIOC_INVENTORY_PING_TIMEOUT_SEC": "1",
    "HIOC_INVENTORY_STALE_AFTER_SEC": "900",
    "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "3600",
    "HIOC_INVENTORY_SNMP_COMMUNITY": "",
    "HIOC_INVENTORY_INTEGRATION_DIR": "",
    "HIOC_INVENTORY_KNOWN_INFRASTRUCTURE_FILE": "config/inventory/known_infrastructure.json",
}


def load_config() -> dict:
    return ConfigService(DEFAULTS).load()
