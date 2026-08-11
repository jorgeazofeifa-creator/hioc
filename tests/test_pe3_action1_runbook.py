import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
RUNBOOK = ROOT / "docs" / "PE3_MANUFACTURER_PRODUCTION_RUNBOOK.md"


class PE3Action1RunbookGovernanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        text = RUNBOOK.read_text(encoding="utf-8")
        cls.action = text.split("## Action 1", 1)[1].split("## Action 2", 1)[0]

    def test_python3_resolver_order_and_invocation_model(self):
        action = self.action
        self.assertLess(action.index("Name = 'py'"), action.index("Name = 'python3'"))
        self.assertLess(action.index("Name = 'python3'"), action.index("Name = 'python'"))
        self.assertIn("Prefix = @('-3')", action)
        self.assertIn("sys.version_info.major == 3", action)
        self.assertIn("print(sys.executable)", action)
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
        self.assertIn("selected pair escaped external workspace", action)

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


if __name__ == "__main__":
    unittest.main()
