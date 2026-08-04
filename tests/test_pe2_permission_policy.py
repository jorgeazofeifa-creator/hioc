import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("pe2_artifacts", ROOT / "tools" / "validate_pe2_artifacts.py")
MODULE = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(MODULE)


class Pe2PermissionPolicyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.root = Path(self.temp.name)

    def tearDown(self): self.temp.cleanup()

    def case(self, git_mode, runtime_mode, actual_mode=None, content=b"approved\n", runtime_content=None,
             owner="jazofv1", group="jazofv1"):
        path = self.root / "artifact"; path.write_bytes(runtime_content if runtime_content is not None else content)
        os.chmod(path, int(actual_mode or runtime_mode, 8))
        import hashlib
        contract = {"schema_version": "1.0", "owner": "jazofv1", "group": "jazofv1",
                    "artifacts": [{"path": "artifact", "runtime_mode": runtime_mode,
                                   "executable": bool(int(runtime_mode, 8) & 0o100), "privacy": "test"}]}
        git_manifest = {"artifacts": [{"path": "artifact", "mode": git_mode, "git_blob": "abc",
                                       "sha256": hashlib.sha256(content).hexdigest()}]}
        return MODULE.validate(contract, git_manifest, self.root,
                               owner_lookup=lambda uid: owner, group_lookup=lambda gid: group,
                               mode_lookup=lambda info: int(actual_mode or runtime_mode, 8))

    def test_git_100644_runtime_0600_passes(self):
        result = self.case("100644", "0600")
        self.assertEqual(result["artifact_identity"], "PASS")
        self.assertEqual(result["runtime_permissions"], "PASS")
        self.assertEqual(result["artifacts"][0]["git_mode"], "100644")
        self.assertEqual(result["artifacts"][0]["runtime_mode"], "0600")

    def test_git_100755_runtime_0700_passes(self):
        self.assertEqual(self.case("100755", "0700")["runtime_permissions"], "PASS")

    def test_correct_bytes_wrong_mode_is_permission_mismatch(self):
        with self.assertRaises(MODULE.ValidationFailure) as caught:
            self.case("100644", "0600", actual_mode="0644")
        self.assertEqual(caught.exception.code, "RUNTIME_PERMISSION_MISMATCH")

    def test_wrong_bytes_correct_mode_is_artifact_mismatch(self):
        with self.assertRaises(MODULE.ValidationFailure) as caught:
            self.case("100644", "0600", runtime_content=b"wrong\n")
        self.assertEqual(caught.exception.code, "RUNTIME_ARTIFACT_MISMATCH")

    def test_owner_and_group_mismatch(self):
        with self.assertRaises(MODULE.ValidationFailure) as caught:
            self.case("100644", "0600", owner="other")
        self.assertEqual(caught.exception.code, "RUNTIME_OWNERSHIP_MISMATCH")

    def test_manifest_is_authoritative_for_installer_and_validator(self):
        installer = (ROOT / "pi4" / "install_pi4.sh").read_text(encoding="utf-8")
        validator = (ROOT / "tools" / "hioc-pe2-production-validate.sh").read_text(encoding="utf-8")
        self.assertIn("pe2_artifacts.json", installer)
        self.assertIn("pe2_artifacts.json", validator)
        self.assertNotIn('endswith("assets.py")', validator)
        self.assertNotIn('.mode=="644"', validator)
        self.assertNotIn('.mode=="755"', validator)


if __name__ == "__main__": unittest.main()
