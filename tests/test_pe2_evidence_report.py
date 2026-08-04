import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("pe2_report", ROOT / "tools" / "render_pe2_evidence.py")
MODULE = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(MODULE)


class Pe2EvidenceReportTests(unittest.TestCase):
    def payload(self, rollback=False, command=None, result="PASS", warnings=None):
        return {"result": result, "rollback_recommended": rollback,
                "rollback_command": command, "warnings": warnings or [], "optional": ""}

    def test_false_and_true_are_boolean(self):
        self.assertIs(MODULE.normalize_report(self.payload(False))["rollback_recommended"], False)
        self.assertIs(MODULE.normalize_report(self.payload(True, "rollback"))["rollback_recommended"], True)

    def test_null_empty_and_warnings_are_valid(self):
        result = MODULE.normalize_report(self.payload(command=None, warnings=["bounded warning"]))
        self.assertIsNone(result["rollback_command"])
        self.assertEqual(result["optional"], "")

    def test_non_boolean_is_rejected(self):
        with self.assertRaises(ValueError): MODULE.normalize_report(self.payload("false"))

    def test_result_classification_contract(self):
        for result in ("VALIDATION_FAIL", "INPUT_OR_PRECONDITION_ERROR", "PARTIAL_PASS", "PASS"):
            self.assertFalse(MODULE.normalize_report(self.payload(False, result=result))["rollback_recommended"])
        genuine = MODULE.normalize_report(self.payload(True, "exact rollback", "FAIL"))
        self.assertTrue(genuine["rollback_recommended"])


if __name__ == "__main__": unittest.main()
