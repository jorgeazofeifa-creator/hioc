import importlib.util
import logging
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "pi4" / "bin" / "hioc-platform-status.py"


def load_platform_status_module():
    spec = importlib.util.spec_from_file_location("hioc_platform_status", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SuccessfulMqttClient:
    def __init__(self, *_args, **_kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def publish(self, *_args):
        pass


class FailingMqttClient(SuccessfulMqttClient):
    def __enter__(self):
        raise RuntimeError("MQTT unavailable")


class PlatformStatusTests(unittest.TestCase):
    def test_successful_run_logs_with_standard_logger(self):
        module = load_platform_status_module()
        version = {
            "hioc_version": "1.0.0",
            "core": "1.0.0",
            "correlation_engine": "2.0.0",
            "dashboard": "2.0.0",
            "schema": "1.0.0",
            "mqtt_api": "1.0.0",
            "build": 1,
        }
        logger = logging.getLogger("test-platform-status")

        with tempfile.TemporaryDirectory() as tmp, \
                patch.object(module, "load_config", return_value={"HIOC_HOME": tmp}), \
                patch.object(module, "read_version_manifest", return_value=version), \
                patch.object(module, "MqttClient", SuccessfulMqttClient), \
                patch.object(module, "setup_logger", return_value=logger):
            self.assertEqual(module.main(), 0)

    def test_mqtt_failure_logs_with_standard_logger(self):
        module = load_platform_status_module()
        logger = logging.getLogger("test-platform-status-mqtt-failure")

        with tempfile.TemporaryDirectory() as tmp, \
                patch.object(module, "load_config", return_value={"HIOC_HOME": tmp}), \
                patch.object(module, "read_version_manifest", wraps=module.read_version_manifest), \
                patch.object(module, "MqttClient", FailingMqttClient), \
                patch.object(module, "setup_logger", return_value=logger):
            Path(tmp, "VERSION.yaml").write_text((ROOT / "VERSION.yaml").read_text(encoding="utf-8"), encoding="utf-8")
            self.assertEqual(module.main(), 0)


if __name__ == "__main__":
    unittest.main()
