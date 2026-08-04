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

    def test_git_governance_for_revalidation(self):
        for marker in ("status --porcelain=v1 --untracked-files=all", "fetch origin", "ORIGIN_MAIN_MISMATCH", "merge --ff-only origin/main"):
            self.assertIn(marker, self.text)
        for forbidden in ("reset --hard", "git stash", "git clean", "checkout --"):
            self.assertNotIn(forbidden, self.text)

    def test_revalidation_mode_is_explicit_and_skips_deployment_branch(self):
        self.assertIn('--revalidate-existing-deployment', self.text)
        self.assertIn('DEPLOYMENT_STATUS="DEPLOYED_EXISTING_REVALIDATION"', self.text)
        self.assertIn('REVALIDATION_MODE=TRUE', self.text)
        self.assertNotIn('release/upgrade.sh', self.text)

    def test_manifest_derived_from_git_objects(self):
        self.assertIn("tools/git_artifact_manifest.py", self.text)
        self.assertIn('OPERATOR_ARTIFACTS=(tools/hioc-pe2-production-validate.sh', self.text)
        for path in ("pi4/lib/hioc/assets.py", "pi4/bin/hioc-assets.py", "pi4/bin/hioc-validate-assets.py", "pi4/install_pi4.sh", "pi4/validate_pi4.sh"):
            self.assertIn(path, (ROOT / "pi4" / "config" / "pe2_artifacts.json").read_text(encoding="utf-8"))

    def test_privacy_and_no_sensitive_display(self):
        self.assertNotIn("--show-sensitive", self.text)
        self.assertIn("PRIVACY_LEAK", self.text)
        self.assertIn("redact_id", self.text)

    def test_no_automatic_rollback_or_broad_backup_delete(self):
        self.assertNotIn("bash release/rollback.sh)", self.text)
        self.assertNotIn("rm -rf", self.text)
        self.assertIn('ROLLBACK_RECOMMENDED="TRUE"', self.text)
        self.assertIn('release-upgrade-20260803-205823', self.text)

    def test_symlink_rejection_and_exact_cleanup(self):
        self.assertIn("SYMLINK_REJECTION_FAILED", self.text)
        self.assertNotIn("rm -- $RUNTIME/backups/assets/*", self.text)
        self.assertIn('rm -- "$path"', self.text)
        self.assertIn("SYNTHETIC_RESIDUE_PRESENT", self.text)
        self.assertIn("CLEAN_BEFORE_MUTATION", self.text)

    def test_authoritative_cli_and_validator_used(self):
        self.assertIn('pi4/bin/hioc-assets.py', self.text)
        self.assertIn('pi4/bin/hioc-validate-assets.py', self.text)
        for command in ("initialize", "set --device-id", "clear-field", "list", "show --device-id", "backup", "restore --backup", "remove --device-id", "validate"):
            self.assertIn(command, self.text)

    def test_report_writer_does_not_interpolate_python_booleans(self):
        self.assertNotIn("bool($DEPLOYMENT_STARTED)", self.text)
        self.assertIn("render_pe2_evidence.py", self.text)

    def test_validation_failure_never_uses_fail_helper(self):
        self.assertIn('die_validation "VALIDATOR_INTERNAL_ERROR"', self.text)
        self.assertIn('ROLLBACK_RECOMMENDED="FALSE"', self.text)

    def test_incident_contract_is_positive_and_validation_only(self):
        self.assertIn("validate_pe2_incident_contract.py", self.text)
        self.assertIn("INCIDENT_OPERATIONAL_DRIFT", self.text)
        self.assertIn("INCIDENT_VALIDATION_INCONCLUSIVE", self.text)
        self.assertNotIn('cmp -s "$digest" "$EVIDENCE/post/incidents/$name"', self.text)
        self.assertNotIn("release/upgrade.sh", self.text)


if __name__ == "__main__":
    unittest.main()
