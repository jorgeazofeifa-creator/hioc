import json
import pathlib
import re
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
POLICY = ROOT / "docs" / "PYTHON_RUNTIME_COMPATIBILITY.md"
SUPPORT = ROOT / "governance" / "python-runtime-support.json"
ACTION1 = ROOT / "tools" / "hioc-pe3-action1.ps1"
MASTER = ROOT / "docs" / "HIOC_MASTER_PLAN.md"
DECISIONS = ROOT / "DECISIONS.md"


class PythonRuntimeCompatibilityGovernanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy = POLICY.read_text(encoding="utf-8")
        cls.support = json.loads(SUPPORT.read_text(encoding="utf-8"))
        cls.action1 = ACTION1.read_text(encoding="utf-8")
        cls.master = MASTER.read_text(encoding="utf-8")
        cls.decisions = DECISIONS.read_text(encoding="utf-8")

    def test_language_floor_matches_repository_source_evidence(self):
        production = list((ROOT / "pi4").rglob("*.py")) + list((ROOT / "tools").glob("*.py"))
        union_without_future = []
        for path in production:
            text = path.read_text(encoding="utf-8-sig")
            if re.search(r"\b[A-Za-z_][A-Za-z0-9_.\[\], ]*\s*\|\s*None\b", text):
                if "from __future__ import annotations" not in text:
                    union_without_future.append(path)
        self.assertTrue(union_without_future)
        self.assertIn("language floor is **CPython 3.10**", self.policy)
        self.assertEqual(self.support["language_floor"], "3.10")

    def test_cpython_only_and_statuses_are_exact(self):
        self.assertEqual(self.support["implementation"], "CPython")
        for implementation in ("PyPy", "GraalPy", "IronPython", "Jython"):
            self.assertIn(implementation, self.policy)
        required = (
            "LANGUAGE-COMPATIBLE FLOOR; NOT CLAIMED TESTED/SUPPORTED",
            "NOT YET REPOSITORY-VALIDATED AS A GOVERNED LINE",
            "TESTED — FULL SUITE PASS",
            "SUPPORTED WINDOWS OPERATOR LINE — VALIDATED 3.13.15",
            "PRESENT FROM OPERATOR-DIAGNOSTIC SIDE EFFECT; NOT HIOC-SUPPORTED",
            "EXACT VERSION UNVERIFIED",
        )
        for status in required:
            self.assertIn(status, self.policy)

    def test_patch_and_platform_contracts_are_separate(self):
        self.assertIn("Patch releases may float", self.policy)
        self.assertEqual(self.support["production"]["runtime_source"], "distribution_managed")
        self.assertEqual(self.support["production"]["status"], "exact_version_unverified")
        self.assertRegex(self.policy, r"Do not replace the\s+system interpreter")

    def test_windows_313_is_supported_with_validated_patch(self):
        windows = self.support["windows_operator"]
        self.assertEqual(windows["major_minor"], "3.13")
        self.assertEqual(windows["status"], "supported")
        self.assertEqual(windows["validated_patch"], "3.13.15")
        self.assertIn("SUPPORTED WINDOWS OPERATOR LINE — VALIDATED 3.13.15", self.policy.split("## Current status", 1)[1].split("## Windows", 1)[0])

    def test_action1_rejects_every_other_minor(self):
        self.assertIn("$ExpectedPythonMajorMinor = '3.13'", self.action1)
        self.assertIn('$ProbeLine -cne "$ExpectedPythonImplementation $ExpectedPythonMajorMinor"', self.action1)
        self.assertIn("ERROR_CODE=PYTHON_VERSION_UNSUPPORTED", self.action1)
        for version in ("3.10", "3.11", "3.12", "3.14"):
            self.assertNotIn(f"$ExpectedPythonMajorMinor = '{version}'", self.action1)

    def test_action1_uses_exact_managed_interpreter_not_aliases(self):
        self.assertIn("list --one --format=exe --only-managed $ExpectedPythonMajorMinor", self.action1)
        self.assertIn('$ProbeLine -cne "$ExpectedPythonImplementation $ExpectedPythonMajorMinor"', self.action1)
        self.assertIn("ERROR_CODE=PYTHON313_MANAGED_RUNTIME_NOT_FOUND", self.action1)
        self.assertNotIn("Get-Command -Name 'py'", self.action1)
        self.assertNotIn("9009", self.action1)

    def test_action1_requires_repository_support_promotion(self):
        self.assertIn("$PythonSupport.windows_operator.status -cne 'supported'", self.action1)
        self.assertIn("ERROR_CODE=PYTHON_RUNTIME_SUPPORT_PENDING", self.action1)
        self.assertLess(
            self.action1.index("$Stage = 'PYTHON_SUPPORT_STATE'"),
            self.action1.index("$Stage = 'PYTHON_RESOLUTION'"),
        )

    def test_operator_prerequisite_and_delivery_chronology_is_governed(self):
        for marker in (
            "ACTION 1 DELIVERY PATH",
            "FAILURE_STAGE=PYTHON_RESOLUTION",
            "WindowsApps",
            "9009",
            "ACTION1_PREREQUISITE_MISSING — PYTHON3",
            "A command merely resolving by name does not satisfy a prerequisite",
            "PYTHON_OPERATOR_DIAGNOSTIC_SIDE_EFFECT",
            "UNINTENDED_DEFAULT_RUNTIME_INSTALL",
            "CPython 3.14.7",
            "CPython 3.13.15",
            "pymanager",
            "NativeCommandError",
            "Diagnostic commands must themselves be assessed for side effects",
            "RUNTIME INVOCATION PATH",
            "stopped at `PYTHON_PROBE`",
            "WINDOWS PYTHON CHECKPOINT\nPROCESSSTARTINFO EXECUTION DEFECT",
            "may already be installed",
            "CROSS-PLATFORM TEST PREREQUISITE CONTRACT DEFECT",
            "MISSING BASH REPORTED AS ERROR",
            "ran 504 tests",
            "Bash is required",
        ):
            self.assertIn(marker, self.policy)

    def test_master_plan_status_and_next_checkpoint_are_consistent(self):
        for status in (
            "PHASE 7A IN PROGRESS",
            "PE-1 COMPLETE - PRODUCTION VALIDATED",
            "PE-2 COMPLETE - PRODUCTION VALIDATED",
            "PE-3.0 COMPLETE",
            "PE-3.1 IMPLEMENTED - REPOSITORY VALIDATED",
            "PE-3.2 COMPLETE - EXTERNAL DATASET VALIDATED",
            "PE-3.3 COMPLETE - DESIGN APPROVED / REPOSITORY SYNCHRONIZED",
            "PE-3 COMPLETE",
            "PE-3 ACTIONS 1-10 COMPLETE",
            "ACTION 10 COMPLETE - NOOP_ALREADY_ABSENT",
            "PYTHON INSTALL MANAGER PRESENT",
            "CPYTHON 3.14.7 PRESENT - NOT HIOC-SUPPORTED",
            "WINDOWS CPYTHON 3.13.X SUPPORTED - VALIDATED PATCH 3.13.15",
            "PRODUCTION DEPLOYMENT COMPLETE",
            "PI3 VALIDATION COMPLETE",
            "PE-4 NOT STARTED",
            "STAGING_PERMISSION_NORMALIZATION",
        ):
            self.assertIn(status, self.master)

    def test_decision_keeps_delivery_and_prerequisite_findings_distinct(self):
        adr = self.decisions.split("## ADR-0024", 1)[1]
        self.assertIn("delivery-path defects", adr)
        self.assertIn("ACTION1_PREREQUISITE_MISSING", adr)
        self.assertIn("not production infrastructure", adr)


if __name__ == "__main__":
    unittest.main()
