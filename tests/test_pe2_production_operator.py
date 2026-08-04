from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "hioc-pe2-production-validate.sh"


class Pe2ProductionOperatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = SCRIPT.read_text(encoding="utf-8")

    def test_governed_shell_contract(self):
        for marker in ("set -Eeuo pipefail", "set +x", "umask 077", "read -r confirmed_host </dev/tty"):
            self.assertIn(marker, self.text)

    def test_exact_target_and_implementation(self):
        self.assertIn('EXPECTED_HOST="nutandpihole"', self.text)
        self.assertIn('EXPECTED_IP="192.168.100.252"', self.text)
        self.assertIn('APPROVED_IMPL="dd6f40b113fe8a395babc8bfb2325262879b8454"', self.text)

    def test_git_governance_and_supported_upgrade(self):
        for marker in ("status --porcelain=v1 --untracked-files=all", "fetch origin", "ORIGIN_MAIN_MISMATCH", "merge --ff-only origin/main", "release/upgrade.sh"):
            self.assertIn(marker, self.text)
        for forbidden in ("reset --hard", "git stash", "git clean", "checkout --"):
            self.assertNotIn(forbidden, self.text)

    def test_manifest_derived_from_git_objects(self):
        self.assertIn("tools/git_artifact_manifest.py", self.text)
        self.assertIn('OPERATOR_ARTIFACT="tools/hioc-pe2-production-validate.sh"', self.text)
        for path in ("pi4/lib/hioc/assets.py", "pi4/bin/hioc-assets.py", "pi4/bin/hioc-validate-assets.py", "pi4/install_pi4.sh", "pi4/validate_pi4.sh"):
            self.assertIn(path, self.text)

    def test_privacy_and_no_sensitive_display(self):
        self.assertNotIn("--show-sensitive", self.text)
        self.assertIn("PRIVACY_LEAK", self.text)
        self.assertIn("redact_id", self.text)

    def test_no_automatic_rollback_or_broad_backup_delete(self):
        self.assertNotIn("bash release/rollback.sh)", self.text)
        self.assertNotIn("rm -rf", self.text)
        self.assertIn('ROLLBACK_RECOMMENDED="TRUE"', self.text)

    def test_symlink_rejection_and_exact_cleanup(self):
        self.assertIn("SYMLINK_REJECTION_FAILED", self.text)
        self.assertNotIn("rm -- $RUNTIME/backups/assets/*", self.text)
        self.assertIn('rm -- "$path"', self.text)

    def test_authoritative_cli_and_validator_used(self):
        self.assertIn('pi4/bin/hioc-assets.py', self.text)
        self.assertIn('pi4/bin/hioc-validate-assets.py', self.text)
        for command in ("initialize", "set --device-id", "clear-field", "list", "show --device-id", "backup", "restore --backup", "remove --device-id", "validate"):
            self.assertIn(command, self.text)


if __name__ == "__main__":
    unittest.main()
