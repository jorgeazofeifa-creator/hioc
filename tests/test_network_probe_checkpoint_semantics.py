import os
import pathlib
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
OBSERVER = ROOT / "tools" / "network_probe_incident_observer.py"
OPERATOR = ROOT / "pi4-tools" / "operator-deploy-network-probe.sh"
PYTHON = os.sys.executable


class CheckpointSemanticTests(unittest.TestCase):
    def observe(self, mode):
        with tempfile.TemporaryDirectory() as td:
            fixture = pathlib.Path(td) / "incident"
            bodies = {
                "clear": '{"status":"none","evidence":[]}\n',
                "active": '{"key":"home_assistant_host_unreachable","evidence":["PI5 / Home Assistant host is unreachable from Pi4"]}\n',
                "empty": "",
                "malformed": "not-json\n",
            }
            fixture.write_text(bodies[mode], encoding="utf-8")
            env = os.environ.copy()
            env["MQTT_PASSWORD"] = "never-print-this-secret"
            result = subprocess.run(
                [PYTHON, str(OBSERVER), "--host", "test", "--port", "1883",
                 "--user", "test", "--topic", "test", "--duration", "0",
                 "--interval", "0", "--fixture", str(fixture)],
                env=env, capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotIn(env["MQTT_PASSWORD"], result.stdout + result.stderr)
            return result.stdout

    def test_cleared_incident_reports_pass(self):
        self.assertIn("PHASE_B_RESULT=PASS", self.observe("clear"))

    def test_active_incident_requires_follow_up_not_failure(self):
        output = self.observe("active")
        self.assertIn("PHASE_B_RESULT=FOLLOW-UP REQUIRED", output)
        self.assertNotIn("FAIL", output)

    def test_unreadable_incident_is_inconclusive(self):
        output = self.observe("empty")
        self.assertIn("PHASE_B_RESULT=INCONCLUSIVE", output)
        self.assertIn("could not be read reliably", output)

    def test_malformed_incident_is_inconclusive(self):
        output = self.observe("malformed")
        self.assertIn("PHASE_B_RESULT=INCONCLUSIVE", output)
        self.assertIn("payload was malformed", output)

    def test_operator_keeps_phase_a_failures_fatal_and_phase_b_nonfatal(self):
        source = OPERATOR.read_text(encoding="utf-8")
        self.assertIn("PHASE A: FAIL", source)
        self.assertIn('exit "$status"', source)
        self.assertIn('cmp -s -- "$BLOB_TEMP" "$TARGET"', source)
        self.assertIn('Overall checkpoint production validation: FAIL', source)
        self.assertNotRegex(source, r'incident_cleared.*exit 1')
        phase_b = source[source.index('OBSERVATION="$('):]
        self.assertNotIn("exit 1", phase_b)

    def test_summary_distinguishes_domains_and_never_invokes_rollback(self):
        source = OPERATOR.read_text(encoding="utf-8")
        self.assertIn("PI3 governed deployment: PASS", source)
        self.assertIn("Incident recovery observation:", source)
        self.assertIn("Overall checkpoint production validation:", source)
        self.assertIn("Do not roll back based only on this observation.", source)
        self.assertNotIn('install -o jazofv1 -g jazofv1 -m 0755 -- "$BACKUP_PATH" "$TARGET"', source)


if __name__ == "__main__":
    unittest.main()
