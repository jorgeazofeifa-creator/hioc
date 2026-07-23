import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "pi4" / "bin" / "hioc-incident-engine-v2.py"


def load_incident_module(home):
    with patch.dict(os.environ, {"HIOC_HOME": str(home), "PI4_TOOLS_HOME": str(home)}, clear=False):
        spec = importlib.util.spec_from_file_location("hioc_incident_engine_v2_test", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module


def write_payloads(module, history_payload=None):
    payloads = {
        module.ACTIVE_FILE: {"status": "none"},
        module.HISTORY_FILE: history_payload if history_payload is not None else [{"id": "incident-1", "review": {"root_cause": "DNS"}}],
        module.SUMMARY_FILE: {"history_count": 1, "latest_incident_review": {"incident_id": "incident-1"}},
        module.TIMELINE_FILE: [{"timestamp": "2026-07-22T00:00:00+00:00"}],
        module.LATEST_EVENT_FILE: {"timestamp": "2026-07-22T00:00:00+00:00"},
        module.STATUS_FILE: {"status": "online"},
    }
    for path, payload in payloads.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payloads


class CapturingMqttClient:
    instances = []
    fail_on_topic = None
    fail_on_enter = False

    def __init__(self, config, client_id):
        self.config = config
        self.client_id = client_id
        self.calls = []
        self.exited = False
        type(self).instances.append(self)

    def __enter__(self):
        if type(self).fail_on_enter:
            raise OSError("broker unavailable")
        return self

    def __exit__(self, *_args):
        self.exited = True
        return False

    def publish(self, topic, payload, retain=True):
        if topic == type(self).fail_on_topic:
            raise OSError("publish failed")
        self.calls.append((topic, payload, retain))


class IncidentMqttTests(unittest.TestCase):
    def setUp(self):
        CapturingMqttClient.instances = []
        CapturingMqttClient.fail_on_topic = None
        CapturingMqttClient.fail_on_enter = False

    def test_publish_all_preserves_topics_order_payloads_and_retain(self):
        with tempfile.TemporaryDirectory() as tmp:
            module = load_incident_module(Path(tmp))
            write_payloads(module)
            original = {path: path.read_text(encoding="utf-8") for path in (
                module.ACTIVE_FILE, module.HISTORY_FILE, module.SUMMARY_FILE,
                module.TIMELINE_FILE, module.LATEST_EVENT_FILE, module.STATUS_FILE,
            )}
            base = "home/infrastructure/hioc"
            expected_topics = [
                f"{base}/incidents/active",
                f"{base}/incidents/history",
                f"{base}/incidents/summary",
                f"{base}/timeline/history",
                f"{base}/timeline/latest",
                f"{base}/status/detail",
                f"{base}/status",
            ]

            with patch.object(module, "MqttClient", CapturingMqttClient):
                completed = module.publish_all(base, {"MQTT_HOST": "broker"})

            client = CapturingMqttClient.instances[0]
            self.assertEqual(client.client_id, "hioc-incident-engine")
            self.assertEqual(completed, expected_topics)
            self.assertEqual([call[0] for call in client.calls], expected_topics)
            self.assertTrue(all(call[2] is True for call in client.calls))
            self.assertEqual([call[1] for call in client.calls[:-1]], list(original.values()))
            self.assertEqual(client.calls[-1][1], "online")
            self.assertTrue(client.exited)

    def test_configuration_preserves_legacy_localhost_defaults(self):
        with tempfile.TemporaryDirectory() as tmp:
            module = load_incident_module(Path(tmp))
            with patch.object(module, "read_shell_config", return_value={}):
                config = module.cfg()

            self.assertEqual(config["MQTT_HOST"], "localhost")
            self.assertEqual(config["MQTT_PORT"], "1883")

    def test_large_history_uses_core_without_subprocess_publication(self):
        with tempfile.TemporaryDirectory() as tmp:
            module = load_incident_module(Path(tmp))
            write_payloads(module, [{"id": "incident-1", "review": {"evidence": "x" * 204_800}}])

            with patch.object(module, "MqttClient", CapturingMqttClient), \
                    patch.object(module.subprocess, "run") as subprocess_run:
                module.publish_all("hioc", {"MQTT_HOST": "broker"})

            history_call = next(call for call in CapturingMqttClient.instances[0].calls if call[0] == "hioc/incidents/history")
            self.assertGreater(len(history_call[1].encode()), 204_800)
            subprocess_run.assert_not_called()

    def test_missing_files_are_skipped_and_status_remains_last(self):
        with tempfile.TemporaryDirectory() as tmp:
            module = load_incident_module(Path(tmp))
            module.HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
            module.HISTORY_FILE.write_text("[]", encoding="utf-8")

            with patch.object(module, "MqttClient", CapturingMqttClient):
                completed = module.publish_all("hioc", {"MQTT_HOST": "broker"})

            self.assertEqual(completed, ["hioc/incidents/history", "hioc/status"])

    def test_malformed_json_fails_before_connection_and_changes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            module = load_incident_module(Path(tmp))
            module.HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
            module.HISTORY_FILE.write_text("{invalid", encoding="utf-8")
            before = module.HISTORY_FILE.read_bytes()

            with patch.object(module, "MqttClient", CapturingMqttClient):
                with self.assertRaisesRegex(RuntimeError, "phase=preflight"):
                    module.publish_all("hioc", {"MQTT_HOST": "broker"})

            self.assertEqual(CapturingMqttClient.instances, [])
            self.assertEqual(module.HISTORY_FILE.read_bytes(), before)

    def test_file_read_failure_stops_before_connection(self):
        with tempfile.TemporaryDirectory() as tmp:
            module = load_incident_module(Path(tmp))
            write_payloads(module)

            with patch.object(module.HISTORY_FILE.__class__, "read_text", side_effect=OSError("read failed")), \
                    patch.object(module, "MqttClient", CapturingMqttClient):
                with self.assertRaisesRegex(RuntimeError, "phase=preflight"):
                    module.publish_all("hioc", {"MQTT_HOST": "broker"})

            self.assertEqual(CapturingMqttClient.instances, [])

    def test_connection_failure_is_explicit(self):
        with tempfile.TemporaryDirectory() as tmp:
            module = load_incident_module(Path(tmp))
            write_payloads(module)
            CapturingMqttClient.fail_on_enter = True

            with patch.object(module, "MqttClient", CapturingMqttClient):
                with self.assertRaisesRegex(RuntimeError, "phase=connect topic=none completed=0"):
                    module.publish_all("hioc", {"MQTT_HOST": "broker"})

    def test_later_failure_reports_partial_progress_and_stops(self):
        with tempfile.TemporaryDirectory() as tmp:
            module = load_incident_module(Path(tmp))
            write_payloads(module)
            base = "hioc"
            CapturingMqttClient.fail_on_topic = f"{base}/incidents/summary"
            before = {path: path.read_bytes() for path in (
                module.ACTIVE_FILE, module.HISTORY_FILE, module.SUMMARY_FILE,
                module.TIMELINE_FILE, module.LATEST_EVENT_FILE, module.STATUS_FILE,
            )}

            with patch.object(module, "MqttClient", CapturingMqttClient):
                with self.assertRaisesRegex(RuntimeError, "phase=publish topic=hioc/incidents/summary completed=2"):
                    module.publish_all(base, {"MQTT_HOST": "broker"})

            client = CapturingMqttClient.instances[0]
            self.assertEqual([call[0] for call in client.calls], [
                f"{base}/incidents/active", f"{base}/incidents/history",
            ])
            self.assertNotIn(f"{base}/status", [call[0] for call in client.calls])
            self.assertTrue(client.exited)
            self.assertEqual({path: path.read_bytes() for path in before}, before)

    def test_first_publish_failure_reports_zero_completed(self):
        with tempfile.TemporaryDirectory() as tmp:
            module = load_incident_module(Path(tmp))
            write_payloads(module)
            CapturingMqttClient.fail_on_topic = "hioc/incidents/active"

            with patch.object(module, "MqttClient", CapturingMqttClient):
                with self.assertRaisesRegex(RuntimeError, "phase=publish topic=hioc/incidents/active completed=0"):
                    module.publish_all("hioc", {"MQTT_HOST": "broker"})

            self.assertEqual(CapturingMqttClient.instances[0].calls, [])
            self.assertTrue(CapturingMqttClient.instances[0].exited)

    def test_main_returns_nonzero_for_required_publication_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            module = load_incident_module(Path(tmp))
            stderr = io.StringIO()
            with patch.object(module, "read_telemetry", return_value={}), \
                    patch.object(module, "load_inventory", return_value={"devices": [], "services": [], "topology": {"edges": []}, "dependencies": {"edges": []}, "summary": {}}), \
                    patch.object(module, "load_events", return_value=[]), \
                    patch.object(module, "core_correlate", return_value=None), \
                    patch.object(module, "publish_all", side_effect=RuntimeError("phase=connect topic=none completed=0: OSError: unavailable")), \
                    contextlib.redirect_stderr(stderr):
                result = module.main()

            self.assertEqual(result, 1)
            self.assertIn("incident MQTT publication failed phase=connect", stderr.getvalue())
            self.assertTrue(module.HISTORY_FILE.exists())

    def test_source_has_no_local_mosquitto_publisher(self):
        source = SCRIPT.read_text(encoding="utf-8")
        self.assertNotIn("mosquitto_pub", source)
        self.assertNotIn("def mqtt_pub", source)
        self.assertIn("mosquitto_sub", source)


if __name__ == "__main__":
    unittest.main()
