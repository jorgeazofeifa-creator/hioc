import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "git_artifact_manifest.py"
DEPLOY = ROOT / "pi4-tools" / "deploy-network-probe.sh"
PYTHON = os.environ.get("PYTHON", os.sys.executable)
SHELL = os.environ.get("HIOC_TEST_SHELL") or shutil.which("bash")


class GitArtifactGovernanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = pathlib.Path(self.temp.name)
        subprocess.run(["git", "init", "-b", "main", str(self.repo)], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "user.email", "test@example.invalid"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "user.name", "Test"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "core.autocrlf", "false"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "core.filemode", "true"], check=True)
        path = self.repo / "pi4-tools" / "scripts"
        path.mkdir(parents=True)
        self.artifact = path / "hioc-network-probe.sh"
        self.artifact.write_bytes(b"#!/bin/bash\nprintf 'original\\n'\n")
        self.artifact.chmod(0o755)
        subprocess.run(["git", "-C", str(self.repo), "add", "."], check=True)
        subprocess.run(
            ["git", "-C", str(self.repo), "update-index", "--chmod=+x",
             "pi4-tools/scripts/hioc-network-probe.sh"],
            check=True,
        )
        subprocess.run(["git", "-C", str(self.repo), "commit", "-m", "artifact"], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "core.filemode", "false"], check=True)
        self.commit = subprocess.check_output(["git", "-C", str(self.repo), "rev-parse", "HEAD"], text=True).strip()

    def tearDown(self):
        self.temp.cleanup()

    def manifest(self, *extra):
        return subprocess.run(
            [PYTHON, str(TOOL), "--repo", str(self.repo), self.commit,
             "pi4-tools/scripts/hioc-network-probe.sh", *extra],
            capture_output=True, text=True,
        )

    def test_manifest_matches_raw_git_blob_and_rev_parse(self):
        result = self.manifest("--compare-worktree")
        self.assertEqual(result.returncode, 0, result.stderr)
        item = json.loads(result.stdout)["artifacts"][0]
        blob = subprocess.check_output(["git", "-C", str(self.repo), "cat-file", "blob", item["git_blob"]])
        expected_blob = subprocess.check_output(
            ["git", "-C", str(self.repo), "rev-parse", f"{self.commit}:pi4-tools/scripts/hioc-network-probe.sh"],
            text=True,
        ).strip()
        self.assertEqual(item["git_blob"], expected_blob)
        self.assertEqual(item["sha256"], hashlib.sha256(blob).hexdigest())
        self.assertTrue(item["working_tree_equal"])

    def test_modified_and_crlf_worktrees_are_detected(self):
        self.artifact.write_bytes(b"#!/bin/bash\r\nprintf 'modified\\n'\r\n")
        item = json.loads(self.manifest("--compare-worktree").stdout)["artifacts"][0]
        self.assertFalse(item["working_tree_equal"])
        self.artifact.write_bytes(b"#!/bin/bash\r\nprintf 'original\\n'\r\n")
        item = json.loads(self.manifest("--compare-worktree").stdout)["artifacts"][0]
        self.assertFalse(item["working_tree_equal"])

    def test_missing_path_is_rejected(self):
        result = subprocess.run(
            [PYTHON, str(TOOL), "--repo", str(self.repo), self.commit, "missing.sh"],
            capture_output=True, text=True,
        )
        self.assertNotEqual(result.returncode, 0)

    def test_stale_external_checksum_cannot_override_git_identity(self):
        stale = hashlib.sha256(self.artifact.read_bytes()).hexdigest()
        self.artifact.write_bytes(b"#!/bin/bash\nprintf 'final\\n'\n")
        subprocess.run(["git", "-C", str(self.repo), "add", "."], check=True)
        subprocess.run(["git", "-C", str(self.repo), "commit", "-m", "final artifact"], check=True, capture_output=True)
        self.commit = subprocess.check_output(["git", "-C", str(self.repo), "rev-parse", "HEAD"], text=True).strip()
        derived = json.loads(self.manifest().stdout)["artifacts"][0]["sha256"]
        self.assertNotEqual(stale, derived)

    @unittest.skipUnless(SHELL, "Bash is required")
    def test_deployer_rejects_dirty_wrong_commit_untracked_and_modified_source(self):
        target = self.repo / "target.sh"
        env = os.environ.copy()
        env.update(HIOC_SOURCE_ROOT=str(self.repo), HIOC_NETWORK_PROBE_TARGET=str(target),
                   HIOC_INSTALL_OWNER="", HIOC_INSTALL_GROUP="")
        self.artifact.write_bytes(self.artifact.read_bytes() + b"# valid change\n")
        result = subprocess.run([SHELL, str(DEPLOY), self.commit], env=env, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        subprocess.run(["git", "-C", str(self.repo), "checkout", "--", "."], check=True)
        wrong = "0" * 40
        self.assertNotEqual(subprocess.run([SHELL, str(DEPLOY), wrong], env=env, capture_output=True).returncode, 0)
        untracked = self.repo / "untracked"
        untracked.write_text("x")
        self.assertNotEqual(subprocess.run([SHELL, str(DEPLOY), self.commit], env=env, capture_output=True).returncode, 0)

    @unittest.skipUnless(SHELL, "Bash is required")
    def test_deployer_reports_matching_blob_source_target_and_backup(self):
        target = self.repo.parent / f"{self.repo.name}-target.sh"
        target.write_text("old\n")
        env = os.environ.copy()
        env.update(HIOC_SOURCE_ROOT=str(self.repo), HIOC_NETWORK_PROBE_TARGET=str(target),
                   HIOC_INSTALL_OWNER="", HIOC_INSTALL_GROUP="")
        try:
            result = subprocess.run([SHELL, str(DEPLOY), self.commit], env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            expected = hashlib.sha256(self.artifact.read_bytes()).hexdigest()
            self.assertEqual(result.stdout.count(expected), 3)
            self.assertIn("Git blob:", result.stdout)
            self.assertIn("Backup:", result.stdout)
            self.assertEqual(target.read_bytes(), self.artifact.read_bytes())
        finally:
            for path in target.parent.glob(target.name + "*"):
                path.unlink()


if __name__ == "__main__":
    unittest.main()
