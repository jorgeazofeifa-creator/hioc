import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from contextlib import redirect_stdout

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("pe2_incidents", ROOT / "tools/validate_pe2_incident_contract.py")
M = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(M)


class IncidentContractTests(unittest.TestCase):
    def docs(self):
        return ({"status":"active","phase":"confirmed","severity":"warning","system":"Synthetic System","title":"Synthetic Event","summary":"Synthetic summary","updated":"2000-01-01T00:00:00Z","telemetry":{"value":1}}, [], {"correlation_engine":"2.0.0","active_count":1})

    def compare(self, mutate=None, missing=None, raw=None):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(M, "prove_no_write_path", return_value=True):
            root=Path(tmp); pre=root/"pre"; post=root/"post"; pre.mkdir(); post.mkdir()
            before=list(self.docs()); after=json.loads(json.dumps(before))
            if mutate: mutate(after)
            for directory, docs in ((pre,before),(post,after)):
                for name, doc in zip(("active.json","history.json","summary.json"),docs):
                    if directory is post and name == missing: continue
                    (directory/name).write_text(raw if directory is post and name=="active.json" and raw else json.dumps(doc),encoding="utf-8")
            return M.compare(pre,post,ROOT,"deadbeef",["Synthetic Asset Secret"])

    def test_identical(self): self.assertEqual(self.compare()["classification"],M.CLASS_UNCHANGED)
    def test_updated_change_is_drift(self): self.assertEqual(self.compare(lambda d:d[0].update(updated="later"))["classification"],M.CLASS_DRIFT)
    def test_lifecycle_title_and_telemetry_changes_are_sanitized_drift(self):
        for change in (lambda d:d[0].update(severity="critical"),lambda d:d[0].update(status="none",phase="idle"),lambda d:d[0].update(title="Other"),lambda d:d[0]["telemetry"].update(value=2)):
            result=self.compare(change); self.assertEqual(result["classification"],M.CLASS_DRIFT); self.assertFalse(result["rollback_recommended"]); self.assertNotIn("Other",json.dumps(result))
    def test_history_growth_and_summary_change_are_drift(self):
        result=self.compare(lambda d:(d[1].append({"status":"resolved"}),d[2].update(active_count=2)))
        self.assertEqual(result["classification"],M.CLASS_DRIFT)
    def test_invalid_or_missing_without_causation_is_inconclusive(self):
        for result in (self.compare(raw="{"),self.compare(missing="active.json")):
            self.assertEqual(result["classification"],M.CLASS_INCONCLUSIVE); self.assertFalse(result["rollback_recommended"])
    def test_asset_field_or_value_is_regression(self):
        for change in (lambda d:d[0].update(friendly_name="x"),lambda d:d[0].update(summary="Synthetic Asset Secret")):
            self.assertEqual(self.compare(change)["classification"],M.CLASS_REGRESSION)
    def test_zero_nonvolatile_and_changed_digest_is_drift(self):
        result=self.compare(lambda d:d[0].update(updated="later")); self.assertFalse(result["causal_regression_demonstrated"])
    def test_uncertainty_never_rolls_back(self):
        argv=["--pre","x","--post","y","--repo","z","--implementation-commit","deadbeef"]
        output=io.StringIO()
        with mock.patch.object(M,"compare",side_effect=RuntimeError), redirect_stdout(output): rc=M.main(argv)
        self.assertEqual(rc,40); self.assertFalse(json.loads(output.getvalue())["rollback_recommended"])
    def test_repository_has_no_incident_write_path(self): self.assertTrue(M.prove_no_write_path(ROOT,"dd6f40b113fe8a395babc8bfb2325262879b8454"))


if __name__ == "__main__": unittest.main()
