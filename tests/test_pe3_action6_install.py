import os
import pathlib
import re
import shutil
import subprocess
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "hioc-pe3-action6-install.sh"
RUNBOOK = ROOT / "docs" / "PE3_MANUFACTURER_PRODUCTION_RUNBOOK.md"


class PE3Action6InstallContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = SCRIPT.read_text(encoding="utf-8")
        cls.runbook = RUNBOOK.read_text(encoding="utf-8")
        cls.action6 = cls.runbook.split("## Action 6", 1)[1].split("## Action 7", 1)[0]
        cls.action6a = cls.action6.split("### Action 6-A", 1)[1].split("### Action 6-B", 1)[0]
        cls.bootstrap = re.search(r"```bash\n(.*?)```", cls.action6a, re.DOTALL).group(1)
        cls.action6b = cls.action6.split("### Action 6-B", 1)[1]

    def test_no_unresolved_transport_placeholder(self):
        self.assertNotIn("/tmp/hioc-pe3-dataset-transfer-XXXXXXXX", self.action6)
        self.assertIn("/tmp/hioc-pe3-dataset-transfer-PJ5qPbRS", self.script)

    def test_bootstrap_stops_before_installation(self):
        self.assertIn("hioc_pe3_action6_a_sync()", self.bootstrap)
        self.assertIn("tools/hioc-pe3-action6-install.sh", self.bootstrap)
        self.assertNotIn("bash \"$SCRIPT\"", self.bootstrap)
        for forbidden in ("PI3_STAGE", "/home/jazofv1/hioc\n", "install ", "ACTION6=COMPLETE", "Action 7"):
            self.assertNotIn(forbidden, self.bootstrap)
        for marker in (
            "TARGET_IDENTITY=PASS", "REPOSITORY_PRECONDITION=PASS",
            "REPOSITORY_SYNCHRONIZATION=PASS", "SYNCHRONIZED_HEAD_IDENTITY=PASS",
            "ACTION6_SCRIPT_AVAILABILITY=PASS", "ACTION6_SCRIPT_IDENTITY=PASS",
            "ACTION6_A=COMPLETE", "RESULT=PASS",
        ):
            self.assertEqual(self.bootstrap.count(marker), 1)

    def test_bootstrap_parent_shell_survives(self):
        shell = os.environ.get("HIOC_TEST_SHELL") or shutil.which("bash")
        if not shell:
            self.skipTest("Bash is required")
        result = subprocess.run(
            [shell, "-c", self.bootstrap + "\nprintf 'PARENT_SHELL_ALIVE=TRUE\\n'"],
            text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("RESULT=INPUT_OR_PRECONDITION_ERROR", result.stdout)
        self.assertIn("PARENT_SHELL_ALIVE=TRUE", result.stdout)
        self.assertNotRegex(self.bootstrap, r"(?m)^\s*(?:set\s+-[^\n]*e|exit(?:\s|$))")

    def test_short_invocation_only(self):
        blocks = re.findall(r"```bash\n(.*?)```", self.action6b, re.DOTALL)
        self.assertEqual(len(blocks), 1)
        self.assertIn("bash /home/jazofv1/hioc-release-source/tools/hioc-pe3-action6-install.sh", blocks[0])
        self.assertIn("--governance-commit", blocks[0])
        self.assertNotIn("install ", blocks[0])

    def test_precondition_failures_are_complete(self):
        for code in (
            "INVALID_ARGUMENTS", "INVALID_GOVERNANCE_COMMIT", "WRONG_TARGET",
            "SOURCE_REPOSITORY_MISSING", "SOURCE_IDENTITY_MISMATCH",
            "ACTIVE_GIT_OPERATION", "ACTION6_SCRIPT_IDENTITY_MISMATCH",
            "VALIDATOR_IDENTITY_MISMATCH", "RUNTIME_ROOT_INVALID",
            "STAGING_PATH_MISMATCH", "STAGING_DIRECTORY_MISSING",
            "STAGING_TYPE_OR_SYMLINK_INVALID", "STAGING_OWNER_OR_MODE_INVALID",
            "STAGING_EXTRA_OR_MISSING_ENTRY", "STAGED_FILE_TYPE_INVALID",
            "STAGED_FILE_OWNER_OR_MODE_INVALID", "STAGED_SIZE_MISMATCH",
            "STAGED_HASH_MISMATCH", "STAGED_VALIDATOR_FAILED",
        ):
            self.assertIn(code, self.script)

    def test_install_and_postpublication_failures_are_complete(self):
        for code in (
            "IMMUTABLE_VERSION_CONFLICT", "INSTALLATION_STAGING_CREATE_FAILED",
            "INSTALLATION_COPY_FAILED", "INSTALLATION_PERMISSION_FAILED",
            "POST_COPY_IDENTITY_FAILED", "FSYNC_FAILED",
            "ATOMIC_PUBLICATION_FAILED", "POST_PUBLICATION_IDENTITY_FAILED",
            "FINAL_VALIDATOR_FAILED", "CONFIGURATION_CHANGED",
            "ACTION6_UNEXPECTED_ERROR", "INSTALLATION_STAGING_CLEANUP_FAILED",
        ):
            self.assertIn(code, self.script)

    def test_staging_and_final_invariants_are_frozen(self):
        for value in (
            "8652642", "1338",
            "81f147cc57768c5797c4ad73a8c0369001bbdcbfe1548e71d3702c8c7f81e0e1",
            "10c8097c0a4ec6e8cc4cd3dc61afc7f368057f4ef4b6534df9f6dd31634a4ac4",
            "53581", "jazofv1:jazofv1", "DB_NAME=manufacturer-db.json",
            "MF_NAME=manufacturer-db.manifest.json",
        ):
            self.assertIn(value, self.script)
        self.assertIn('d.get("privacy_safe") is True', self.script)
        self.assertIn("no_csv", self.script)

    def test_atomic_publication_and_fsync_are_governed(self):
        self.assertIn(".action6-install-XXXXXXXX", self.script)
        self.assertIn('renameat2(-100', self.script)
        self.assertIn("RENAME_NOREPLACE", self.action6)
        self.assertIn('sync -f "$INSTALL_STAGE/$DB_NAME"', self.script)
        self.assertIn('sync -f "$VERSIONS"', self.script)
        self.assertNotIn('mv -- "$INSTALL_STAGE"', self.script)

    def test_existing_version_is_idempotent_or_fail_closed(self):
        self.assertIn("IMMUTABLE_INSTALLATION=PASS_ALREADY_IDENTICAL", self.script)
        self.assertIn("IMMUTABLE_INSTALLATION=PASS_NEW", self.script)
        conflict = self.script.index("IMMUTABLE_VERSION_CONFLICT")
        create = self.script.index('mktemp -d "$DATA_ROOT/.action6-install-XXXXXXXX"')
        self.assertLess(conflict, create)
        self.assertNotRegex(self.script, r"rm\s+-r[fF]?.*FINAL_DIR")

    def test_cleanup_is_bounded_to_invocation_owned_stage(self):
        cleanup = self.script.split("cleanup_install_stage()", 1)[1].split("fail_action6()", 1)[0]
        self.assertIn('"$DATA_ROOT"/.action6-install-*', cleanup)
        self.assertIn('rm -r -- "$INSTALL_STAGE"', cleanup)
        self.assertNotIn("PI3_STAGE", cleanup)
        self.assertNotIn("FINAL_DIR", cleanup)
        self.assertNotIn("rm -rf", self.script)

    def test_configuration_is_fingerprinted_and_never_modified(self):
        self.assertIn("CONFIG_SHA256_BEFORE", self.script)
        self.assertIn("configuration_unchanged", self.script)
        self.assertNotIn("MANUFACTURER_DB_PATH=", self.script)
        self.assertNotRegex(self.script, r"(?:install|cp|mv|sed).*\$CONFIG")

    def test_pass_contract_and_action7_barrier(self):
        for marker in (
            "TARGET_IDENTITY=PASS", "SOURCE_IDENTITY=PASS", "STAGING_IDENTITY=PASS",
            "STAGING_VALIDATION=PASS", "IMMUTABLE_INSTALLATION=PASS_NEW",
            "IMMUTABLE_INSTALLATION=PASS_ALREADY_IDENTICAL", "FINAL_DATASET_IDENTITY=PASS",
            "FINAL_DATASET_VALIDATION=PASS", "CONFIGURATION_UNTOUCHED=PASS",
            "ACTION6=COMPLETE", "RESULT=PASS",
        ):
            self.assertIn(marker, self.script)
        self.assertNotIn("ACTION7", self.script)
        self.assertIn("Action 7 unauthorized", self.action6)

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


if __name__ == "__main__":
    unittest.main()
