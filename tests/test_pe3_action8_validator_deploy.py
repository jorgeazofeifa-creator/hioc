import hashlib
import os
import pathlib
import re
import shutil
import subprocess
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"tools"/"hioc-pe3-action8-validator-deploy.sh"
VALIDATOR=ROOT/"pi4"/"bin"/"hioc-validate-manufacturer.py"

class PE3Action8ValidatorDeployTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.text=SCRIPT.read_text(encoding="utf-8")
    def test_frozen_validator_identity(self):
        self.assertIn("VALIDATOR_BLOB=656f64c8c556ef62e149ef036c767cd7fc3736a0",self.text)
        self.assertIn("VALIDATOR_SHA256=03f5e4658379fcf6d3093fa36cb8b9fb8a806f27b81777a0a751c647643ff5a2",self.text)
        self.assertEqual(hashlib.sha256(VALIDATOR.read_bytes()).hexdigest(),"03f5e4658379fcf6d3093fa36cb8b9fb8a806f27b81777a0a751c647643ff5a2")
    def test_exact_target_and_operator(self):
        for value in ("nutandpihole","192.168.100.252","jazofv1","/home/jazofv1/hioc-release-source","/home/jazofv1/hioc"):
            self.assertIn(value,self.text)
    def test_governance_and_source_gates(self):
        for value in ("INVALID_ARGUMENTS","INVALID_GOVERNANCE_COMMIT","SOURCE_REPOSITORY_MISSING","WRONG_BRANCH","SOURCE_REPOSITORY_DIRTY","ACTIVE_GIT_OPERATION","GOVERNANCE_HEAD_MISMATCH","ORIGIN_MAIN_MISMATCH","SOURCE_GIT_IDENTITY_MISMATCH","SOURCE_WORKTREE_IDENTITY_MISMATCH","SOURCE_VALIDATOR_IDENTITY_MISMATCH"):
            self.assertIn(value,self.text)
        self.assertIn("'^[0-9a-f]{40}$'",self.text)
        self.assertIn('rev-parse "$GOVERNANCE_COMMIT:$rel"',self.text)
    def test_runtime_prestate_is_fail_closed(self):
        for value in ("RUNTIME_ROOT_UNSAFE","RUNTIME_VALIDATOR_MISSING","RUNTIME_VALIDATOR_UNSAFE","RUNTIME_VALIDATOR_UNHASHABLE"):
            self.assertIn(value,self.text)
        self.assertIn('owned_file "$TARGET" 700',self.text)
        self.assertIn('safe_owned_directory "$RUNTIME/backups"',self.text)
    def test_noop_and_replacement_dispositions(self):
        self.assertIn("DEPLOYMENT_DISPOSITION=NOOP_IDENTICAL",self.text)
        self.assertIn("DEPLOYMENT_DISPOSITION=REPLACED",self.text)
        self.assertIn("BACKUP=NOT_REQUIRED",self.text)
        self.assertIn("VALIDATOR_PUBLICATION=NOT_REQUIRED",self.text)
    def test_backup_is_private_bounded_and_durable(self):
        self.assertIn("pe3-action8-validator-deploy-XXXXXXXX",self.text)
        self.assertIn('install -o jazofv1 -g jazofv1 -m 0700 -- "$TARGET" "$BACKUP_PATH"',self.text)
        self.assertIn('sync -f "$BACKUP_PATH"',self.text)
        self.assertIn("BACKUP_IDENTITY_FAILED",self.text)
    def test_publication_is_same_filesystem_atomic_and_durable(self):
        self.assertIn('$RUNTIME/pi4/bin/.hioc-validate-manufacturer.py.pe3.XXXXXXXX',self.text)
        self.assertIn('install -o jazofv1 -g jazofv1 -m 0700 -- "$SOURCE/$VALIDATOR_REL" "$TEMP_TARGET"',self.text)
        self.assertIn('mv -fT -- "$TEMP_TARGET" "$TARGET"',self.text)
        self.assertIn('sync -f "$TARGET" && sync -f "$RUNTIME/pi4/bin"',self.text)
        for code in ("PUBLICATION_TEMP_CREATE_FAILED","PUBLICATION_TEMP_COPY_FAILED","PUBLICATION_TEMP_IDENTITY_FAILED","PUBLICATION_TEMP_FSYNC_FAILED","ATOMIC_PUBLICATION_FAILED","PUBLICATION_FSYNC_FAILED","FINAL_RUNTIME_VALIDATOR_IDENTITY_FAILED","PUBLICATION_TEMP_CLEANUP_FAILED"):
            self.assertIn(code,self.text)
    def test_protected_state_is_content_and_metadata_identity(self):
        for value in ("manufacturer.json","manufacturer_status.json","inventory.json","hioc.conf","manufacturer-db.json","manufacturer-db.manifest.json","protected-pre.json","protected-post.json","PROTECTED_STATE_CHANGED"):
            self.assertIn(value,self.text)
        self.assertIn("hashlib.sha256(path.read_bytes()).hexdigest()",self.text)
        self.assertIn('cmp -s "$EVIDENCE_DIR/protected-pre.json" "$EVIDENCE_DIR/protected-post.json"',self.text)
    def test_embedded_protected_snapshot_python_compiles(self):
        program=self.text.split("<<'PY'\n",1)[1].split("\nPY\n",1)[0]
        compile(program,"action8-validator-protected-snapshot","exec")
    def test_no_broad_deployment_or_runtime_actions(self):
        for forbidden in ("release/upgrade.sh","pi4/install_pi4.sh","systemctl","crontab","hioc-generate-manufacturer.py","hioc-pe3-action8-generate.sh","ACTION9","hioc-pe3-dataset-transfer"):
            self.assertNotIn(forbidden,self.text)
    def test_bounded_output_and_rollback_contract(self):
        for value in ("RESULT=%s","ERROR_CODE=%s","FAILURE_STAGE=%s","ROLLBACK_RECOMMENDED=%s","EVIDENCE_DIR=%s","BACKUP_PATH=%s"):
            self.assertIn(value,self.text)
        self.assertIn("PROTECTED_STATE_CHANGED PROTECTED_POST_STATE TRUE",self.text)
        self.assertIn("FINAL_RUNTIME_VALIDATOR_IDENTITY_FAILED RUNTIME_VALIDATOR_IDENTITY TRUE",self.text)
        self.assertIn("BACKUP_CREATE_FAILED BACKUP FALSE",self.text)
    def test_evidence_is_private_and_result_last(self):
        self.assertIn("/tmp/hioc-pe3-action8-validator-deploy-XXXXXXXX",self.text)
        self.assertIn('chmod 0700 "$EVIDENCE_DIR"',self.text)
        self.assertIn('chmod 0600 "$result_temp"',self.text)
        self.assertLess(self.text.index('mv -fT -- "$result_temp"'),self.text.index("EVIDENCE_REPORT=PASS"))
    def test_parent_shell_survives_invalid_input(self):
        shell=os.environ.get("HIOC_TEST_SHELL") or shutil.which("bash")
        if not shell: self.skipTest("Bash is required")
        result=subprocess.run([shell,"-c",f"source '{SCRIPT.as_posix()}'; printf 'PARENT_SHELL_ALIVE=TRUE\\n'"],text=True,capture_output=True)
        self.assertIn("ERROR_CODE=INVALID_ARGUMENTS",result.stdout)
        self.assertIn("PARENT_SHELL_ALIVE=TRUE",result.stdout)
    def test_no_global_strict_mode_or_exit(self):
        self.assertNotRegex(self.text,r"(?m)^\s*set\s+-[^\n]*e")
        self.assertNotRegex(self.text,r"(?m)^\s*exit(?:\s|$)")
    def test_governance_documents_own_the_new_boundary(self):
        for rel in ("DECISIONS.md","docs/CHANGELOG.md","docs/DEPLOYMENT.md","docs/HIOC_MASTER_PLAN.md","docs/OPERATIONS.md","docs/PE3_MANUFACTURER_EXECUTABLE_CONTRACT.md","docs/PE3_MANUFACTURER_PRODUCTION_RUNBOOK.md","docs/RELEASE.md"):
            self.assertIn("validator",(ROOT/rel).read_text(encoding="utf-8").lower(),rel)
        runbook=(ROOT/"docs/PE3_MANUFACTURER_PRODUCTION_RUNBOOK.md").read_text(encoding="utf-8")
        self.assertIn("NOOP_IDENTICAL",runbook)
        self.assertIn("REPLACED",runbook)
        self.assertIn("Action 9 remains **NOT STARTED**"," ".join(runbook.split()))

if __name__=="__main__": unittest.main()
