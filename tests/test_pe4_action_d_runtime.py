import importlib.util
import pathlib
import os
import subprocess
import tempfile
import unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
spec = importlib.util.spec_from_file_location("pe4_action_d_common", TOOLS / "hioc_pe4_runtime_common.py")
COMMON = importlib.util.module_from_spec(spec)
spec.loader.exec_module(COMMON)
CONSTRUCT = (TOOLS / "hioc-pe4-runtime-construct.py").read_text(encoding="utf-8")
VALIDATE = (TOOLS / "hioc-pe4-dependency-validate.py").read_text(encoding="utf-8")


class ActionDIsolationTests(unittest.TestCase):
    def test_subprocess_environment_is_explicit_and_excludes_hostile_inputs(self):
        hostile = ("PYTHONPATH", "PYTHONHOME", "PIP_FIND_LINKS", "PIP_INDEX_URL",
                   "PIP_EXTRA_INDEX_URL", "PIP_TRUSTED_HOST", "PIP_PROXY",
                   "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY")
        with mock.patch.dict(COMMON.os.environ, {name: "hostile" for name in hostile}):
            environment = COMMON.action_d_subprocess_environment()
        for name in hostile:
            self.assertNotEqual(environment.get(name), "hostile")
        self.assertEqual(environment["PIP_CONFIG_FILE"], COMMON.os.devnull)
        self.assertEqual(environment["PIP_NO_INDEX"], "1")
        self.assertEqual(environment["PYTHONNOUSERSITE"], "1")

    def test_distribution_set_accepts_only_governed_bootstrap_and_websockets(self):
        result = subprocess.CompletedProcess([], 0,
            "pip==23.0.1\nsetuptools==66.1.1\nwebsockets==16.1.1\n", "")
        with mock.patch.object(COMMON, "run", return_value=result):
            parsed = COMMON.exact_distribution_set(pathlib.Path("python"))
        self.assertEqual(parsed["websockets"], "16.1.1")

    def test_distribution_set_rejects_unexpected_or_duplicate_packages(self):
        for output in ("pip==23\nwebsockets==16.1.1\nrequests==2\n",
                       "pip==23\nwebsockets==16.1.1\nwebsockets==16.1.1\n",
                       "pip==23\nwebsockets==15.0\n"):
            with self.subTest(output=output), mock.patch.object(
                    COMMON, "run", return_value=subprocess.CompletedProcess([], 0, output, "")):
                with self.assertRaises(COMMON.Failure):
                    COMMON.exact_distribution_set(pathlib.Path("python"))

    def test_construction_is_retained_and_descriptor_anchored(self):
        self.assertIn("create_owned_child(environment_root", CONSTRUCT)
        self.assertIn('cwd=f"/proc/self/fd/{construction.fd}"', CONSTRUCT)
        self.assertNotIn("construction.rmdir()", CONSTRUCT)
        self.assertNotIn("tempfile.mkdtemp", CONSTRUCT)

    def test_install_is_offline_hash_locked_binary_only_and_snapshot_bound(self):
        for value in ("--isolated", "--no-index", "--no-deps", "--require-hashes",
                      "--only-binary=:all:", "--no-cache-dir",
                      "--disable-pip-version-check", 'f"/proc/self/fd/{lock_fd}"'):
            self.assertIn(value, CONSTRUCT)
        self.assertNotIn("str(transfer)", CONSTRUCT)

    def test_lock_is_sealed_before_pip_consumes_its_descriptor(self):
        source = (TOOLS / "hioc_pe4_runtime_common.py").read_text(encoding="utf-8")
        for value in ("os.memfd_create", "fcntl.F_ADD_SEALS", "fcntl.F_SEAL_WRITE",
                      "fcntl.F_GET_SEALS"):
            self.assertIn(value, source)
        self.assertIn("sealed_snapshot_file(snapshot", CONSTRUCT)

    def test_action_e_requires_confirmed_action_d_handoff(self):
        gate = "validate_action_d_eligibility(root,a.governance_commit)"
        self.assertIn(gate, VALIDATE)
        self.assertLess(VALIDATE.index(gate), VALIDATE.index("exact_distribution_set"))

    def test_venv_policy_allows_only_bounded_standard_lib64_link(self):
        source = (TOOLS / "hioc_pe4_runtime_common.py").read_text(encoding="utf-8")
        self.assertIn('relative != "lib64" or os.readlink(path) != "lib"', source)
        self.assertIn('Failure("UNEXPECTED_VENV_SYMLINK"', source)

    def test_result_last_and_no_replace_eligibility_are_explicit(self):
        self.assertIn('publish_owned_json(evidence, "result.json"', CONSTRUCT)
        self.assertIn("publish_owned_json(construction, ACTION_D_ELIGIBILITY", CONSTRUCT)
        self.assertIn("os.link(temporary, name", (TOOLS / "hioc_pe4_runtime_common.py").read_text())

    def test_failure_output_keeps_primary_and_cleanup_states_separate(self):
        self.assertIn('state["CLEANUP_STATE"]', CONSTRUCT)
        self.assertIn("terminal(\"FAIL\", exc.code, exc.stage, exc.rollback", CONSTRUCT)


@unittest.skipUnless(os.name == "posix", "descriptor-relative Action D filesystem semantics are PI3/POSIX-only")
class ActionDPosixFilesystemTests(unittest.TestCase):
    def setUp(self):
        self.temporary = pathlib.Path(tempfile.mkdtemp(prefix="hioc-action-d-test-", dir="/tmp"))
        os.chmod(self.temporary, 0o700)
        self.parent = COMMON.open_owned_directory(self.temporary, 0o700, "TEST")

    def tearDown(self):
        if self.parent.fd >= 0:
            for name in os.listdir(self.parent.fd):
                path = self.temporary / name
                if path.is_dir() and not path.is_symlink():
                    child = COMMON.open_owned_directory(path, 0o700, "TEST", parent=self.parent)
                    COMMON.cleanup_owned_directory(child, "TEST")
                else:
                    os.unlink(name, dir_fd=self.parent.fd)
            self.parent.close()
        self.temporary.rmdir()

    def test_exclusive_child_retains_parent_and_inode_identity(self):
        child = COMMON.create_owned_child(self.parent, "child-", 0o700, "TEST")
        before = (child.dev, child.ino)
        COMMON.revalidate_owned_directory(child, "TEST")
        self.assertEqual(before, (os.fstat(child.fd).st_dev, os.fstat(child.fd).st_ino))
        COMMON.cleanup_owned_directory(child, "TEST")

    def test_json_publication_is_confirmed_and_no_replace(self):
        digest = COMMON.publish_owned_json(self.parent, "result.json", {"result": "PASS"}, "TEST")
        self.assertEqual(len(digest), 64)
        with self.assertRaises(COMMON.Failure):
            COMMON.publish_owned_json(self.parent, "result.json", {"result": "PASS"}, "TEST")

    def test_unexpected_venv_symlink_is_rejected_but_lib64_is_allowed(self):
        child = COMMON.create_owned_child(self.parent, "venv-", 0o700, "TEST")
        os.mkdir("lib", dir_fd=child.fd)
        os.symlink("lib", "lib64", dir_fd=child.fd)
        COMMON.validate_venv_symlinks(child)
        os.symlink("/tmp", "escape", dir_fd=child.fd)
        with self.assertRaises(COMMON.Failure):
            COMMON.validate_venv_symlinks(child)
        COMMON.cleanup_owned_directory(child, "TEST")

    def test_descriptor_cleanup_unlinks_links_without_following_targets(self):
        child = COMMON.create_owned_child(self.parent, "clean-", 0o700, "TEST")
        outside = self.temporary / "outside"
        outside.write_text("preserve", encoding="ascii")
        os.symlink(str(outside), "link", dir_fd=child.fd)
        COMMON.cleanup_owned_directory(child, "TEST")
        self.assertEqual(outside.read_text(encoding="ascii"), "preserve")


if __name__ == "__main__":
    unittest.main()
