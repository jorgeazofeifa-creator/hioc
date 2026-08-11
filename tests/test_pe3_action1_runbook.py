import hashlib
import os
import pathlib
import re
import shutil
import subprocess
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
RUNBOOK = ROOT / "docs" / "PE3_MANUFACTURER_PRODUCTION_RUNBOOK.md"
SCRIPT = ROOT / "tools" / "hioc-pe3-action1.ps1"
GITATTRIBUTES = ROOT / ".gitattributes"


class PE3Action1RepositoryScriptGovernanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        text = RUNBOOK.read_text(encoding="utf-8")
        cls.action = text.split("## Action 1", 1)[1].split("## Action 2", 1)[0]
        cls.script = SCRIPT.read_text(encoding="utf-8")

    def test_explicit_parameter_contract(self):
        script = self.script
        for name in ("Repo", "ExternalWorkspace", "GovernanceCommit"):
            self.assertIn(f"[string]${name}", script)
        self.assertIn("[ValidatePattern('^[0-9a-f]{40}$')]", script)
        self.assertNotIn("C:\\Users\\", script)

    def test_script_has_no_delivery_corruption_signatures(self):
        script = self.script
        self.assertNotIn(r"\_", script)
        self.assertNotIn(r"$env\:", script)
        self.assertNotIn("sys.version\\_", script)
        self.assertIn("$env:HIOC_HOME = $Repo", script)
        self.assertIn("sys.version_info", script)

    def test_python_resolver_order(self):
        script = self.script
        self.assertLess(script.index("Name = 'py'"), script.index("Name = 'python3'"))
        self.assertLess(script.index("Name = 'python3'"), script.index("Name = 'python'"))
        self.assertIn("Prefix = @('-3')", script)
        self.assertIn("ERROR_CODE=PYTHON3_NOT_FOUND", script)

    def test_expected_and_unexpected_failures_preserve_host(self):
        script = self.script
        self.assertNotRegex(script, r"(?m)^\s*exit(?:\s|$)")
        self.assertIn("ERROR_CODE=VALIDATED_BUILD_PAIR_NOT_FOUND", script)
        self.assertIn("ERROR_CODE=MANUFACTURER_VALIDATION_FAILED", script)
        self.assertIn("ERROR_CODE=ACTION1_UNEXPECTED_ERROR", script)
        self.assertIn('Write-Output "FAILURE_STAGE=$Stage"', script)
        for stage in ("INITIALIZATION", "REPOSITORY_CHECK", "SCRIPT_IDENTITY",
                      "PYTHON_RESOLUTION", "BUILD_PAIR_DISCOVERY",
                      "BUILD_PAIR_CONTAINMENT", "MANUFACTURER_VALIDATION",
                      "FINAL_REPORT"):
            self.assertIn(f"$Stage = '{stage}'", script)
        self.assertNotIn("$_.Exception", script)
        self.assertNotIn("ScriptStackTrace", script)

    def test_frozen_artifact_identity_and_pair_validation(self):
        script = self.script
        self.assertIn("81f147cc57768c5797c4ad73a8c0369001bbdcbfe1548e71d3702c8c7f81e0e1", script)
        self.assertIn("10c8097c0a4ec6e8cc4cd3dc61afc7f368057f4ef4b6534df9f6dd31634a4ac4", script)
        self.assertIn("$ExpectedDatabaseBytes = 8652642", script)
        self.assertIn("$ExpectedManifestBytes = 1338", script)
        self.assertIn("Join-Path $CandidateDatabase.DirectoryName 'manufacturer-db.manifest.json'", script)
        self.assertIn("$DatabaseHash -eq $ExpectedDatabaseSha256 -and $ManifestHash -eq $ExpectedManifestSha256", script)
        selection = script.index("$SelectedPair = $MatchingPairs | Sort-Object")
        verification = script.index("$DatabaseHash -eq $ExpectedDatabaseSha256")
        self.assertGreater(selection, verification)

    def test_external_workspace_containment_remains_enforced(self):
        script = self.script
        self.assertIn("Get-ChildItem -LiteralPath $ExternalWorkspace", script)
        self.assertIn("$SelectedDirectory.StartsWith($WorkspacePrefix", script)
        self.assertIn("ERROR_CODE=SELECTED_PAIR_OUTSIDE_WORKSPACE", script)
        self.assertIn("[IO.Path]::DirectorySeparatorChar", script)

    def test_script_self_identity_and_ancestry_are_required(self):
        script = self.script
        self.assertIn("tools/hioc-pe3-action1.ps1", script)
        self.assertIn("hash-object --path=tools/hioc-pe3-action1.ps1", script)
        self.assertIn("diff --quiet $GovernanceCommit -- tools/hioc-pe3-action1.ps1", script)
        self.assertIn("ERROR_CODE=ACTION1_SCRIPT_IDENTITY_MISMATCH", script)
        self.assertIn("merge-base --is-ancestor $ImplementationCommit $GovernanceCommit", script)
        self.assertIn("$Head -ne $GovernanceCommit -or $Origin -ne $GovernanceCommit", script)

    def test_validator_is_read_only_and_no_production_or_transfer_logic_exists(self):
        script = self.script.lower()
        self.assertIn("hioc-validate-manufacturer.py", script)
        for forbidden in ("ssh ", "scp ", "rsync ", "invoke-webrequest", "curl ",
                          "wget ", "set-content", "add-content", "remove-item",
                          "copy-item", "move-item", "new-item", "192.168.100.252",
                          "release/upgrade", "manufacturer.json", "action 2"):
            self.assertNotIn(forbidden, script)
        self.assertNotIn("organization", script)
        self.assertNotIn("matched_prefix", script)

    def test_runbook_invokes_script_without_embedding_implementation(self):
        action = self.action
        self.assertIn("tools/hioc-pe3-action1.ps1", action)
        self.assertIn("-Repo $Repo -ExternalWorkspace $ExternalWorkspace -GovernanceCommit $GovernanceCommit", action)
        self.assertNotIn("function Invoke-PE3ManufacturerAction1", action)
        self.assertNotIn("$ExpectedDatabaseSha256", action)

    def test_documented_script_identities_match_actual_file(self):
        self.assertIn(
            "tools/hioc-pe3-action1.ps1 text eol=lf",
            GITATTRIBUTES.read_text(encoding="utf-8").splitlines(),
        )
        raw = SCRIPT.read_bytes()
        sha256 = hashlib.sha256(raw).hexdigest()
        documented_sha = re.search(r"ACTION1_SCRIPT_SHA256=([0-9a-f]{64})", self.action).group(1)
        self.assertEqual(sha256, documented_sha)
        git = shutil.which("git")
        if not git:
            self.skipTest("git unavailable")
        result = subprocess.run(
            [git, "-C", str(ROOT), "hash-object", "--path=tools/hioc-pe3-action1.ps1", "--", str(SCRIPT)],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        documented_blob = re.search(r"ACTION1_SCRIPT_GIT_BLOB=([0-9a-f]{40})", self.action).group(1)
        self.assertEqual(result.stdout.strip(), documented_blob)

    def test_script_parses_in_windows_powershell_51(self):
        shell = shutil.which("powershell.exe") or shutil.which("powershell")
        if not shell:
            self.skipTest("Windows PowerShell unavailable")
        command = (
            "$text=Get-Content -Raw -LiteralPath $env:HIOC_TEST_ACTION1_SCRIPT;"
            "$tokens=$null;$errors=$null;"
            "[System.Management.Automation.Language.Parser]::ParseInput($text,[ref]$tokens,[ref]$errors)|Out-Null;"
            "if($errors.Count){$errors.Message;exit 1}"
        )
        env = dict(os.environ)
        env["HIOC_TEST_ACTION1_SCRIPT"] = str(SCRIPT)
        result = subprocess.run([shell, "-NoProfile", "-Command", command], env=env,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
