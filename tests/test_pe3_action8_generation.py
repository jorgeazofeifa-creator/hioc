import os
import pathlib
import re
import shutil
import subprocess
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "hioc-pe3-action8-generate.sh"
RUNBOOK = ROOT / "docs" / "PE3_MANUFACTURER_PRODUCTION_RUNBOOK.md"


class PE3Action8GenerationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = SCRIPT.read_text(encoding="utf-8")
        cls.runbook = RUNBOOK.read_text(encoding="utf-8")
        cls.action8 = cls.runbook.split("## Action 8", 1)[1].split("## Action 9", 1)[0]
        cls.action8_flat = " ".join(cls.action8.split())

    def test_unsafe_inline_action8_is_retired(self):
        self.assertIn("ACTION 8 OPERATOR-SAFETY AND EVIDENCE CONTRACT DEFECT", self.action8_flat)
        self.assertNotIn("```bash\nset -euo pipefail", self.action8)
        self.assertNotIn("| tee \"$EVIDENCE_DIR", self.action8)
        self.assertNotIn("hioc-pe3-production-validation-XXXXXXXX", self.action8)

    def test_future_bootstrap_is_required_but_not_invented(self):
        self.assertIn("future bootstrap synchronization/script-identity gate", self.action8_flat)
        self.assertIn("not prepared by this checkpoint", self.action8_flat)
        self.assertNotIn("hioc_pe3_action8_a_sync()", self.action8)
        self.assertNotRegex(self.action8, r"```bash")

    def test_exact_identity_contract(self):
        self.assertIn('"$(id -un 2>/dev/null)" = jazofv1', self.script)
        self.assertIn('"$(id -gn 2>/dev/null)" = jazofv1', self.script)
        for value in (
            "local-ieee-ra--2026-08-11-r1", "8652642", "1338",
            "81f147cc57768c5797c4ad73a8c0369001bbdcbfe1548e71d3702c8c7f81e0e1",
            "10c8097c0a4ec6e8cc4cd3dc61afc7f368057f4ef4b6534df9f6dd31634a4ac4",
            "53581", "/tmp/hioc-pe3-dataset-transfer-PJ5qPbRS",
        ):
            self.assertIn(value, self.script)
        for rel in (
            "hioc-pe3-action8-generate.sh", "hioc-generate-manufacturer.py",
            "hioc-validate-manufacturer.py", "manufacturer.py",
        ):
            self.assertIn(rel, self.script)

    def test_pass_and_failure_contracts(self):
        for marker in (
            "TARGET_IDENTITY=PASS", "SOURCE_IDENTITY=PASS", "RUNTIME_IDENTITY=PASS",
            "EVIDENCE_PRECONDITION=PASS", "CONFIGURATION_IDENTITY=PASS",
            "DATASET_IDENTITY=PASS", "DATASET_VALIDATION=PASS",
            "INVENTORY_IDENTITY=PASS", "OUTPUT_PRECONDITION=PASS",
            "PROTECTED_PRE_STATE=PASS", "MANUFACTURER_GENERATION=PASS",
            "MANUFACTURER_ARTIFACT_IDENTITY=PASS",
            "MANUFACTURER_ARTIFACT_VALIDATION=PASS",
            "PROTECTED_POST_GENERATION=PASS", "EVIDENCE_PUBLICATION=PASS",
            "ACTION8=COMPLETE", "RESULT=PASS",
        ):
            self.assertIn(marker, self.script)
        for marker in ("ERROR_CODE=%s", "FAILURE_STAGE=%s", "ROLLBACK_RECOMMENDED=%s"):
            self.assertIn(marker, self.script)

    def test_mutation_and_protection_boundaries(self):
        self.assertIn('python3 "$RUNTIME/$GENERATOR_REL" --home "$RUNTIME" --json', self.script)
        self.assertIn("manufacturer.json", self.script)
        self.assertIn("manufacturer_status.json", self.script)
        self.assertIn("generation-result.json", self.script)
        self.assertIn("generation-performance.txt", self.script)
        self.assertIn("CONFIG_SHA_BEFORE", self.script)
        self.assertIn("TRANSPORT_SHA_BEFORE", self.script)
        for forbidden in ("systemctl", "crontab", "release/upgrade.sh", "ACTION9", "rm -r"):
            self.assertNotIn(forbidden, self.script)

    def test_private_atomic_evidence_and_artifact_validation(self):
        self.assertIn(".action8-result.XXXXXXXX", self.script)
        self.assertIn(".action8-performance.XXXXXXXX", self.script)
        self.assertIn('mv -fT -- "$TEMP_RESULT"', self.script)
        self.assertLess(
            self.script.index('mv -fT -- "$TEMP_PERFORMANCE"'),
            self.script.index('mv -fT -- "$TEMP_RESULT"'),
        )
        self.assertIn('[ "$(dirname -- "$EVIDENCE_DIR")" = /tmp ]', self.script)
        self.assertIn('sync -f "$EVIDENCE_DIR"', self.script)
        self.assertIn("validate_sidecar", self.script)
        self.assertIn("MANUFACTURER_TEMP_ARTIFACT_PRESENT", self.script)
        self.assertNotIn("| tee", self.script)

    def test_child_script_failure_preserves_parent_shell(self):
        shell = os.environ.get("HIOC_TEST_SHELL") or shutil.which("bash")
        if not shell:
            self.skipTest("Bash is required")
        path = str(SCRIPT).replace("\\", "/")
        if re.match(r"^[A-Za-z]:/", path):
            path = "/" + path[0].lower() + path[2:]
        result = subprocess.run(
            [shell, "-c", f". '{path}'; printf 'PARENT_SHELL_ALIVE=TRUE\\n'"],
            text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("ERROR_CODE=INVALID_ARGUMENTS", result.stdout)
        self.assertIn("PARENT_SHELL_ALIVE=TRUE", result.stdout)
        self.assertNotRegex(self.script, r"(?m)^\s*(?:set\s+-[^\n]*e|exit(?:\s|$))")


if __name__ == "__main__":
    unittest.main()
