import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "pi4" / "bin" / "hioc-validate-mqtt.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("hioc_validate_mqtt", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def completed(payload, returncode=0, stderr=b""):
    return subprocess.CompletedProcess([], returncode, stdout=payload + b"\n", stderr=stderr)


class MqttRuntimeValidationTests(unittest.TestCase):
    def setUp(self):
        self.module = load_validator()
        self.config = {
            "MQTT_HOST": "mqtt.example.test",
            "MQTT_PORT": "2883",
            "HIOC_BASE_TOPIC": "custom/hioc",
        }

    def payload_for_topic(self, topic):
        if topic.endswith("/status"):
            return b"online"
        if topic.endswith("/incidents/history"):
            return json.dumps(
                [{"id": "incident_1", "review": {"summary": "complete"}}]
            ).encode()
        return b"{}"

    def successful_run(self, command, **kwargs):
        topic = command[command.index("-t") + 1]
        return completed(self.payload_for_topic(topic))

    def test_loads_existing_configuration_precedence(self):
        from hioc.config import load_config

        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "hioc"
            tools = Path(tmp) / "tools"
            (home / "config").mkdir(parents=True)
            (tools / "config").mkdir(parents=True)
            (tools / "config" / "toolkit.conf").write_text(
                'MQTT_HOST="toolkit-broker"\nMQTT_PORT="1883"\n'
                'MQTT_USER="toolkit-user"\nMQTT_PASSWORD="toolkit-secret"\n',
                encoding="utf-8",
            )
            (home / "config" / "hioc.conf").write_text(
                'MQTT_PORT="2883"\nHIOC_BASE_TOPIC="configured/hioc"\n',
                encoding="utf-8",
            )
            environment = {
                "HIOC_HOME": str(home),
                "PI4_TOOLS_HOME": str(tools),
                "MQTT_USER": "environment-user",
            }
            with patch.dict(os.environ, environment, clear=True):
                config = load_config()

        self.assertEqual(config["MQTT_HOST"], "toolkit-broker")
        self.assertEqual(config["MQTT_PORT"], "2883")
        self.assertEqual(config["MQTT_USER"], "environment-user")
        self.assertEqual(config["MQTT_PASSWORD"], "toolkit-secret")
        self.assertEqual(config["HIOC_BASE_TOPIC"], "configured/hioc")

    def test_requires_configured_host_without_localhost_assumption(self):
        with self.assertRaisesRegex(ValueError, "MQTT_HOST is not configured"):
            self.module.resolve_settings(
                {"MQTT_PORT": "1883", "HIOC_BASE_TOPIC": "hioc"}
            )
        self.assertNotIn("localhost", SCRIPT.read_text(encoding="utf-8"))

    def test_authentication_arguments_are_used_but_secret_is_not_printed(self):
        config = dict(
            self.config,
            MQTT_USER="operator",
            MQTT_PASSWORD="super-secret",
        )
        seen = []

        def fail(command, **kwargs):
            seen.append(command)
            return completed(
                b"",
                returncode=1,
                stderr=b"authentication failed for super-secret operator",
            )

        output = io.StringIO()
        with patch.object(self.module, "load_config", return_value=config), \
                patch.object(self.module.subprocess, "run", side_effect=fail), \
                contextlib.redirect_stdout(output):
            exit_code = self.module.main([])

        self.assertEqual(exit_code, 1)
        self.assertIn("-u", seen[0])
        self.assertIn("operator", seen[0])
        self.assertIn("-P", seen[0])
        self.assertIn("super-secret", seen[0])
        self.assertNotIn("super-secret", output.getvalue())
        self.assertNotIn("operator", output.getvalue())

    def test_successfully_validates_all_retained_topics(self):
        with patch.object(
            self.module.subprocess, "run", side_effect=self.successful_run
        ) as run:
            settings, results = self.module.validate(self.config, 3)

        self.assertEqual(settings["host"], "mqtt.example.test")
        self.assertEqual(len(results), 7)
        self.assertTrue(all(result.status == "PASS" for result in results))
        self.assertEqual(
            [result.topic for result in results],
            [f"custom/hioc/{suffix}" for suffix in self.module.TOPIC_SUFFIXES],
        )
        self.assertTrue(all(call.kwargs["timeout"] == 3 for call in run.call_args_list))
        history = next(
            result
            for result in results
            if result.topic.endswith("/incidents/history")
        )
        self.assertIn("records=1", history.detail)
        self.assertIn("embedded_review=yes", history.detail)

    def test_large_history_reports_exact_payload_bytes(self):
        large_review = "x" * 200_000
        history = json.dumps(
            [{"id": "incident_1", "review": {"analysis": large_review}}]
        ).encode()

        def run(command, **kwargs):
            topic = command[command.index("-t") + 1]
            payload = (
                history
                if topic.endswith("/incidents/history")
                else self.payload_for_topic(topic)
            )
            return completed(payload)

        with patch.object(self.module.subprocess, "run", side_effect=run):
            _, results = self.module.validate(self.config, 2)

        result = next(
            item for item in results if item.topic.endswith("/incidents/history")
        )
        self.assertGreaterEqual(len(history), 193 * 1024)
        self.assertIn(f"bytes={len(history)}", result.detail)
        self.assertIn("records=1", result.detail)
        self.assertIn("embedded_review=yes", result.detail)

    def test_missing_topic_is_incomplete_and_nonzero(self):
        def run(command, **kwargs):
            topic = command[command.index("-t") + 1]
            if topic.endswith("/timeline/latest"):
                raise subprocess.TimeoutExpired(command, kwargs["timeout"])
            return completed(self.payload_for_topic(topic))

        with patch.object(self.module, "load_config", return_value=self.config), \
                patch.object(self.module.subprocess, "run", side_effect=run), \
                contextlib.redirect_stdout(io.StringIO()) as output:
            exit_code = self.module.main(["--timeout", "0.25"])

        self.assertEqual(exit_code, 2)
        self.assertIn("INCOMPLETE", output.getvalue())
        self.assertIn("within 0.25s", output.getvalue())

    def test_broker_connection_failure_is_fail(self):
        with patch.object(
            self.module.subprocess,
            "run",
            return_value=completed(
                b"", returncode=1, stderr=b"Connection refused"
            ),
        ):
            _, results = self.module.validate(self.config, 1)

        self.assertTrue(all(result.status == "FAIL" for result in results))
        self.assertEqual(self.module.overall_status(results), ("FAIL", 1))

    def test_invalid_json_is_fail(self):
        def run(command, **kwargs):
            topic = command[command.index("-t") + 1]
            payload = (
                b"{invalid"
                if topic.endswith("/incidents/summary")
                else self.payload_for_topic(topic)
            )
            return completed(payload)

        with patch.object(self.module.subprocess, "run", side_effect=run):
            _, results = self.module.validate(self.config, 1)

        result = next(
            item for item in results if item.topic.endswith("/incidents/summary")
        )
        self.assertEqual(result.status, "FAIL")
        self.assertIn("json=invalid", result.detail)

    def test_history_without_review_is_warning_not_failure(self):
        status, detail = self.module.summarize_payload(
            "custom/hioc/incidents/history",
            json.dumps([{"id": "legacy_incident"}]).encode(),
        )
        self.assertEqual(status, "WARNING")
        self.assertIn("records=1", detail)
        self.assertIn("embedded_review=no", detail)

    def test_validator_is_statically_read_only(self):
        source = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("mosquitto_sub", source)
        self.assertNotIn("mosquitto_pub", source)
        self.assertNotIn("MqttClient", source)
        self.assertNotIn(".publish(", source)
        self.assertNotIn("write_text(", source)
        self.assertNotIn("write_bytes(", source)


if __name__ == "__main__":
    unittest.main()
