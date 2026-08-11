import hashlib
import pathlib
import re
import shutil
import subprocess
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
RUNBOOK = ROOT / "docs" / "PE3_MANUFACTURER_PRODUCTION_RUNBOOK.md"


class PE3Action1RunbookGovernanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        text = RUNBOOK.read_text(encoding="utf-8")
        cls.action = text.split("## Action 1", 1)[1].split("## Action 2", 1)[0]
        cls.code = re.search(r"```powershell\s*(.*?)\s*```", cls.action, re.S).group(1)

    def test_python3_resolver_order_and_invocation_model(self):
        action = self.action
        self.assertLess(action.index("Name = 'py'"), action.index("Name = 'python3'"))
        self.assertLess(action.index("Name = 'python3'"), action.index("Name = 'python'"))
        self.assertIn("Prefix = @('-3')", action)
        self.assertIn("sys.version_info.major == 3", action)
        self.assertIn("print(sys.executable)", action)
        self.assertIn("$PythonProbeCode", action)
        self.assertIn("& $PythonExecutable @PythonPrefix", action)
        self.assertNotIn("$Python = 'python'", action)

    def test_missing_python3_has_exact_precondition_error(self):
        self.assertIn("RESULT=INPUT_OR_PRECONDITION_ERROR", self.action)
        self.assertIn("ERROR_CODE=PYTHON3_NOT_FOUND", self.action)

    def test_pair_discovery_requires_adjacent_manifest_and_both_hashes(self):
        action = self.action
        self.assertIn("Get-ChildItem -LiteralPath $ExternalWorkspace", action)
        self.assertIn("Join-Path $CandidateDatabase.DirectoryName 'manufacturer-db.manifest.json'", action)
        self.assertIn("$DatabaseHash -eq $ExpectedDatabaseSha256 -and $ManifestHash -eq $ExpectedManifestSha256", action)
        self.assertIn("$CandidateDatabase.Length -ne $ExpectedDatabaseBytes", action)
        self.assertIn("$CandidateManifest.Length -ne $ExpectedManifestBytes", action)
        self.assertNotIn("LastWriteTime", action)
        self.assertNotIn("CreationTime", action)

    def test_zero_and_multiple_match_contract(self):
        action = self.action
        self.assertIn("if ($MatchingPairs.Count -eq 0)", action)
        self.assertIn("ERROR_CODE=VALIDATED_BUILD_PAIR_NOT_FOUND", action)
        selection = action.index("$SelectedPair = $MatchingPairs | Sort-Object")
        verification = action.index("$DatabaseHash -eq $ExpectedDatabaseSha256")
        self.assertGreater(selection, verification)
        self.assertIn("matching_pair_count=$MatchingPairs.Count", action)
        self.assertNotIn("GetRelativePath", action)
        self.assertIn("ERROR_CODE=SELECTED_PAIR_OUTSIDE_WORKSPACE", action)
        self.assertIn("[IO.Path]::DirectorySeparatorChar", action)
        self.assertNotIn("TrimEnd('\\')", action)
        self.assertNotIn("Replace('\\', '/')", action)

    def test_expected_failures_return_without_terminating_host(self):
        code = self.code
        self.assertIn("function Invoke-PE3ManufacturerAction1", code)
        self.assertRegex(code, r"ERROR_CODE=PYTHON3_NOT_FOUND'\s+return")
        self.assertRegex(code, r"ERROR_CODE=VALIDATED_BUILD_PAIR_NOT_FOUND'\s+return")
        self.assertRegex(code, r"ERROR_CODE=MANUFACTURER_VALIDATION_FAILED'; return")
        self.assertNotRegex(code, r"(?m)^\s*exit(?:\s|$)")

    def test_unexpected_error_is_sanitized_and_returns(self):
        code = self.code
        self.assertRegex(code, r"catch\s*\{\s*Write-Output 'RESULT=VALIDATION_FAIL'\s*Write-Output 'ERROR_CODE=ACTION1_UNEXPECTED_ERROR'\s*Write-Output \"FAILURE_STAGE=\$Stage\"\s*return")
        self.assertNotIn("$_.Exception", code)
        self.assertNotIn("ScriptStackTrace", code)
        self.assertIn('Write-Output "FAILURE_STAGE=$Stage"', code)
        for stage in ("INITIALIZATION", "REPOSITORY_CHECK", "PYTHON_RESOLUTION",
                      "BUILD_PAIR_DISCOVERY", "BUILD_PAIR_CONTAINMENT",
                      "MANUFACTURER_VALIDATION", "FINAL_REPORT"):
            self.assertIn(f"$Stage = '{stage}'", code)

    def test_pass_returns_normally_to_operator_prompt(self):
        code = self.code
        pass_result = code.index("[ordered]@{ result='PASS'")
        normal_return = code.index("return", pass_result)
        catch_block = code.index("catch", normal_return)
        invocation = code.index("Invoke-PE3ManufacturerAction1", catch_block)
        self.assertLess(pass_result, normal_return)
        self.assertLess(normal_return, catch_block)
        self.assertLess(catch_block, invocation)

    def test_action_remains_read_only_private_and_windows_only(self):
        action = self.action.lower()
        for forbidden in ("ssh ", "scp ", "invoke-webrequest", "curl ", "wget ",
                          "set-content", "add-content", "remove-item", "copy-item",
                          "move-item", "new-item"):
            self.assertNotIn(forbidden, action)
        self.assertNotIn("192.168.100.252", action)
        self.assertIn("selected_build_directory", action)
        self.assertNotIn("organization", action)
        self.assertNotIn("matched_prefix", action)

    def test_extracted_block_has_no_delivery_corruption_signatures(self):
        code = self.code
        self.assertNotIn(r"\_", code)
        self.assertNotIn(r"$env\:", code)
        self.assertNotIn("sys.version\\_", code)
        self.assertIn("$env:HIOC_HOME = $Repo", code)
        self.assertIn("sys.version_info", code)

    def test_block_integrity_failure_is_visible_and_returns(self):
        code = self.code
        self.assertIn("ERROR_CODE=ACTION1_BLOCK_INTEGRITY_FAILED", code)
        self.assertIn("$ExpectedDatabaseSha256 -cnotmatch '^[0-9a-f]{64}$'", code)
        self.assertIn("$ImplementationCommit -cnotmatch '^[0-9a-f]{40}$'", code)
        self.assertRegex(code, r"ERROR_CODE=ACTION1_BLOCK_INTEGRITY_FAILED'\s+return")

    def test_canonical_extracted_block_hash_matches_documented_digest(self):
        normalized = self.code.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n") + "\n"
        digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
        documented = re.search(r"ACTION1_BLOCK_SHA256=([0-9a-f]{64})", self.action).group(1)
        self.assertEqual(digest, documented)

    def test_canonical_block_prompts_without_operator_specific_reconstruction(self):
        code = self.code
        self.assertIn("$Repo = Read-Host 'Enter the authoritative HIOC repository path'", code)
        self.assertIn("$ExternalWorkspace = Read-Host 'Enter the retained PE-3 external workspace path'", code)
        self.assertIn("$OperatorGovernanceCommit = Read-Host 'Enter the approved full 40-hex post-push governance commit'", code)
        self.assertNotIn("C:\\path\\to", code)
        self.assertNotIn("<approved-full-40-hex-post-push-commit>", code)

    def test_extracted_block_parses_in_windows_powershell(self):
        shell = shutil.which("powershell.exe") or shutil.which("powershell")
        if not shell:
            self.skipTest("Windows PowerShell unavailable")
        command = (
            "$t=Get-Content -Raw -LiteralPath $env:HIOC_TEST_RUNBOOK;"
            "$a=($t -split '## Action 1',2)[1] -split '## Action 2',2|Select-Object -First 1;"
            "$b=([regex]::Match($a,'(?s)```powershell\\s*(.*?)\\s*```')).Groups[1].Value;"
            "$tokens=$null;$errors=$null;"
            "[System.Management.Automation.Language.Parser]::ParseInput($b,[ref]$tokens,[ref]$errors)|Out-Null;"
            "if($errors.Count){$errors.Message;exit 1}"
        )
        env = dict(__import__("os").environ)
        env["HIOC_TEST_RUNBOOK"] = str(RUNBOOK)
        result = subprocess.run([shell, "-NoProfile", "-Command", command], env=env,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
