import os
import pathlib
import subprocess
import shutil
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "pi4-tools" / "scripts" / "hioc-network-probe.sh"
DEPLOY = ROOT / "pi4-tools" / "deploy-network-probe.sh"
SHELL = os.environ.get("HIOC_TEST_SHELL") or shutil.which("bash") or shutil.which("sh") or "bash"


class NetworkProbeGovernanceTests(unittest.TestCase):
    def test_shell_sources_parse(self):
        for source in (SCRIPT, DEPLOY):
            result = subprocess.run([SHELL, "-n", str(source)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_pi5_endpoint_has_one_configured_source(self):
        source = SCRIPT.read_text(encoding="utf-8")
        self.assertNotIn("192.168.100.152", source)
        self.assertNotIn("192.168.100.251", source)
        self.assertIn('pi5_ip="$HOME_ASSISTANT_IP"', source)
        self.assertIn('--arg pi5_ip "$pi5_ip"', source)
        self.assertIn('ip:$pi5_ip', source)

    def test_production_repository_has_no_pi5_address_literal(self):
        production_roots = (
            ROOT / "pi4",
            ROOT / "pi4-tools",
            ROOT / "homeassistant",
            ROOT / "release",
        )
        suffixes = {".py", ".sh", ".yaml", ".yml", ".json", ".conf", ".example"}
        offenders = []
        for production_root in production_roots:
            if not production_root.exists():
                continue
            for path in production_root.rglob("*"):
                if path.is_file() and path.suffix in suffixes:
                    text = path.read_text(encoding="utf-8", errors="replace")
                    if "192.168.100.152" in text or "192.168.100.251" in text:
                        offenders.append(str(path.relative_to(ROOT)))
        self.assertEqual(offenders, [], f"PI5 address literals found: {offenders}")

    def test_pi5_incident_trace_uses_probe_status_not_endpoint_literal(self):
        engine = (ROOT / "pi4" / "bin" / "hioc-incident-engine-v2.py").read_text(encoding="utf-8")
        correlation = (ROOT / "pi4" / "lib" / "hioc" / "core" / "correlation.py").read_text(encoding="utf-8")
        package = (ROOT / "homeassistant" / "packages" / "hioc_incident_center.yaml").read_text(encoding="utf-8")
        dashboard = (ROOT / "homeassistant" / "dashboards" / "hioc_dashboard_v2.yaml").read_text(encoding="utf-8")
        self.assertIn('mqtt_read(f"{legacy}/network/pi5_status", "online")', engine)
        self.assertIn("Pi5 / Home Assistant host is unreachable from Pi4", correlation)
        self.assertIn("Home Assistant host unreachable", correlation)
        self.assertIn("state_topic: home/infrastructure/hioc/incidents/active", package)
        self.assertIn("states('sensor.hioc_incident_active')", dashboard)

    def test_missing_home_assistant_ip_fails_without_exposing_credentials(self):
        with tempfile.TemporaryDirectory() as td:
            base = pathlib.Path(td)
            (base / "config").mkdir()
            (base / "logs").mkdir()
            secret = "not-a-production-secret"
            (base / "config" / "toolkit.conf").write_text(
                f'MQTT_HOST="198.51.100.10"\nMQTT_PORT="1883"\n'
                f'MQTT_USER="test"\nMQTT_PASSWORD="{secret}"\n',
                encoding="utf-8",
            )
            env = os.environ.copy()
            env["HIOC_PI4_TOOLS_BASE"] = str(base)
            result = subprocess.run([SHELL, str(SCRIPT)], env=env, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("HOME_ASSISTANT_IP", result.stderr)
            self.assertNotIn(secret, result.stdout + result.stderr)

    def test_configured_pi5_reaches_probe_and_inventory_arguments(self):
        with tempfile.TemporaryDirectory() as td:
            base = pathlib.Path(td)
            bindir = base / "bin"
            bindir.mkdir()
            (base / "config").mkdir()
            (base / "logs").mkdir()
            configured_ip = "198.51.100.77"
            (base / "config" / "toolkit.conf").write_text(
                f'HOME_ASSISTANT_IP="{configured_ip}"\nMQTT_HOST="198.51.100.10"\n'
                'MQTT_PORT="1883"\nMQTT_USER="test"\nMQTT_PASSWORD="secret"\n',
                encoding="utf-8",
            )
            calls = base / "calls"
            stubs = {
                "ping": '#!/bin/sh\necho "ping $*" >> "$HIOC_TEST_CALLS"\n'
                        'echo "8 packets transmitted, 8 received, 0% packet loss"\n'
                        'echo "rtt min/avg/max/mdev = 1/2/3/4 ms"\n',
                "dig": '#!/bin/sh\necho "2"\n',
                "mosquitto_pub": '#!/bin/sh\nexit 0\n',
                "jq": '#!/bin/sh\nprintf "jq" >> "$HIOC_TEST_CALLS"\n'
                      'for arg in "$@"; do printf " <%s>" "$arg" >> "$HIOC_TEST_CALLS"; done\n'
                      'printf "\\n" >> "$HIOC_TEST_CALLS"\necho "{}"\n',
            }
            for name, body in stubs.items():
                path = bindir / name
                path.write_text(body, encoding="utf-8")
                path.chmod(0o755)
            env = os.environ.copy()
            env.update(
                HIOC_PI4_TOOLS_BASE=str(base),
                HIOC_TEST_CALLS=str(calls),
                PATH=str(bindir) + os.pathsep + env["PATH"],
            )
            result = subprocess.run([SHELL, str(SCRIPT)], env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            observed = calls.read_text(encoding="utf-8")
            self.assertIn(f"ping -c 8 -W 2 {configured_ip}", observed)
            self.assertIn(f"ping -c 1 -W 2 {configured_ip}", observed)
            self.assertIn(f"<pi5_ip> <{configured_ip}>", observed)


if __name__ == "__main__":
    unittest.main()
