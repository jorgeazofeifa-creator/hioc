import contextlib
import hashlib
import importlib.util
import io
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))
import hioc_pe4_runtime_common as COMMON

SPEC = importlib.util.spec_from_file_location("pe4_action_a", TOOLS / "hioc-pe4-artifact-acquire.py")
ACTION = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ACTION)


class FakeSocket:
    def __init__(self): self.timeouts = []
    def settimeout(self, value): self.timeouts.append(value)


class FakeResponse:
    def __init__(self, data=b"data", status=200, length=None):
        self.data, self.status, self.position = data, status, 0
        self.length = str(len(data) if length is None else length)
    def getheader(self, name): return self.length if name == "Content-Length" else None
    def read(self, count):
        block=self.data[self.position:self.position+count];self.position+=len(block);return block


class FakeConnection:
    response = FakeResponse()
    instances = []
    def __init__(self, host, timeout, context):
        self.host,self.timeout,self.context,self.sock=host,timeout,context,FakeSocket();self.request_data=None
        type(self).instances.append(self)
    def request(self, method, path, headers): self.request_data=(method,path,headers)
    def getresponse(self): return type(self).response
    def close(self): self.closed=True


class ActionAWindowsTests(unittest.TestCase):
    def setUp(self): FakeConnection.instances=[]

    def patched_identity(self, data=b"data"):
        return mock.patch.multiple(ACTION,WHEEL_SIZE=len(data),MAX_RESPONSE_BYTES=len(data)+1,WHEEL_SHA256=hashlib.sha256(data).hexdigest())

    def test_known_folder_is_resolved_by_windows_api(self):
        source=(TOOLS/"hioc_pe4_runtime_common.py").read_text(encoding="utf-8")
        self.assertIn("GetFolderPath('LocalApplicationData')",source)
        self.assertNotIn('os.environ["LOCALAPPDATA"]',source)

    def test_cache_and_evidence_roots_are_deterministic(self):
        with tempfile.TemporaryDirectory() as temp:
            trusted=pathlib.Path(temp); legacy=trusted/"HIOC/artifacts/pe4"
            cache,staging,evidence=ACTION.roots(cache_resolver=lambda:legacy,acl=lambda p,d:None,reparse=lambda p:False)
            self.assertEqual(cache,legacy/"cache");self.assertEqual(staging,legacy/"staging");self.assertEqual(evidence,legacy/"evidence")

    def test_missing_c_tmp_is_irrelevant(self):
        source=(TOOLS/"hioc-pe4-artifact-acquire.py").read_text(encoding="utf-8")
        self.assertNotIn('dir="/tmp"',source);self.assertIn("EVIDENCE_PARTS",source)

    def test_acl_creation_is_current_sid_only(self):
        with mock.patch.object(COMMON,"run") as runner:
            COMMON.secure_workstation_path(pathlib.Path("C:/fixture"),True)
        command=runner.call_args.args[0];script=command[4]
        self.assertIn("SetAccessRuleProtection($true,$false)",script)
        self.assertIn("$rules.Count -ne 1",script)
        self.assertIn("WindowsIdentity]::GetCurrent().User",script)
        self.assertIn("GetAccessControl",script);self.assertIn("SetAccessControl",script)
        self.assertNotIn("Get-Acl",script);self.assertNotIn("Set-Acl",script)
        self.assertEqual(command[-1],script)
        self.assertEqual(runner.call_args.kwargs["env"]["HIOC_PE4_ACL_PATH"],"C:\\fixture")

    def test_acl_distinguishes_directory_and_file(self):
        with mock.patch.object(COMMON,"run") as runner:
            COMMON.secure_workstation_path(pathlib.Path("C:/fixture"),False)
        self.assertEqual(runner.call_args.kwargs["env"]["HIOC_PE4_ACL_IS_DIRECTORY"],"0")

    def test_acl_validation_requires_protected_dacl(self):
        source=(TOOLS/"hioc_pe4_runtime_common.py").read_text(encoding="utf-8")
        self.assertIn("AreAccessRulesProtected",source)

    def test_acl_validation_rejects_additional_allow_aces(self):
        source=(TOOLS/"hioc_pe4_runtime_common.py").read_text(encoding="utf-8")
        self.assertIn("$rules.Count -ne 1",source)

    def test_acl_validation_rejects_deny_inherited_and_wrong_flags(self):
        source=(TOOLS/"hioc_pe4_runtime_common.py").read_text(encoding="utf-8")
        self.assertIn("AccessControlType]::Allow",source)
        self.assertIn("$actual.IsInherited",source)
        self.assertIn("$actual.InheritanceFlags -ne $expectedInheritance",source)
        self.assertIn("$actual.PropagationFlags",source)

    def test_acl_application_and_validation_failures_are_bounded(self):
        for returncode,expected in ((14,"WORKSTATION_ACL_APPLICATION_FAILED"),(23,"WORKSTATION_ACL_RULE_COUNT_INVALID")):
            result=subprocess.CompletedProcess([],returncode,"","")
            with self.subTest(returncode=returncode),mock.patch.object(COMMON.subprocess,"run",return_value=result):
                with self.assertRaisesRegex(COMMON.Failure,expected):
                    COMMON.secure_workstation_path(pathlib.Path("C:/fixture"),True)

    @unittest.skipUnless(os.name == "nt" and shutil.which("powershell.exe"),"Windows ACL integration requires powershell.exe")
    def test_real_windows_acl_hardens_inherited_production_shape(self):
        seed_script=r'''$p=$env:HIOC_PE4_TEST_PATH;$item=[IO.DirectoryInfo]::new($p)
$acl=$item.GetAccessControl([Security.AccessControl.AccessControlSections]::Access)
$acl.SetAccessRuleProtection($true,$false)
foreach($rule in @($acl.GetAccessRules($true,$true,[Security.Principal.SecurityIdentifier]))){[void]$acl.RemoveAccessRuleSpecific($rule)}
$inherit=[Security.AccessControl.InheritanceFlags]::ContainerInherit -bor [Security.AccessControl.InheritanceFlags]::ObjectInherit
$none=[Security.AccessControl.PropagationFlags]::None;$allow=[Security.AccessControl.AccessControlType]::Allow
$user=[Security.Principal.WindowsIdentity]::GetCurrent().User;$system=[Security.Principal.SecurityIdentifier]::new('S-1-5-18')
$acl.AddAccessRule((New-Object Security.AccessControl.FileSystemAccessRule($user,[Security.AccessControl.FileSystemRights]::FullControl,$inherit,$none,$allow)))
$acl.AddAccessRule((New-Object Security.AccessControl.FileSystemAccessRule($system,[Security.AccessControl.FileSystemRights]::ReadAndExecute,$inherit,$none,$allow)))
$acl.AddAccessRule((New-Object Security.AccessControl.FileSystemAccessRule($system,[Security.AccessControl.FileSystemRights]::ReadData,$inherit,$none,[Security.AccessControl.AccessControlType]::Deny)))
$item.SetAccessControl($acl)'''
        summary_script=r'''$p=$env:HIOC_PE4_TEST_PATH;$isDir=$env:HIOC_PE4_TEST_IS_DIRECTORY -eq '1'
$item=if($isDir){[IO.DirectoryInfo]::new($p)}else{[IO.FileInfo]::new($p)}
$acl=$item.GetAccessControl([Security.AccessControl.AccessControlSections]::Access)
$sid=[Security.Principal.WindowsIdentity]::GetCurrent().User
$rules=@($acl.GetAccessRules($true,$true,[Security.Principal.SecurityIdentifier]))
$mine=@($rules|Where-Object{$_.IdentityReference.Value -eq $sid.Value})
Write-Output ('PROTECTED='+$acl.AreAccessRulesProtected)
Write-Output ('RULES='+$rules.Count)
Write-Output ('INHERITED='+@($rules|Where-Object{$_.IsInherited}).Count)
Write-Output ('DENY='+@($rules|Where-Object{$_.AccessControlType -eq [Security.AccessControl.AccessControlType]::Deny}).Count)
Write-Output ('MINE='+$mine.Count)
Write-Output ('FULL='+@($mine|Where-Object{$_.FileSystemRights -eq [Security.AccessControl.FileSystemRights]::FullControl}).Count)
if($rules.Count -eq 1){Write-Output ('INHERITANCE='+[int]$rules[0].InheritanceFlags);Write-Output ('PROPAGATION='+[int]$rules[0].PropagationFlags)}'''
        def run_script(script,path,is_directory=True):
            environment=os.environ.copy();environment["HIOC_PE4_TEST_PATH"]=str(path)
            environment["HIOC_PE4_TEST_IS_DIRECTORY"]="1" if is_directory else "0"
            return COMMON.run(["powershell.exe","-NoProfile","-NonInteractive","-Command",script],
                              "TEST_ACL",env=environment).stdout.splitlines()
        with tempfile.TemporaryDirectory() as temp:
            parent=pathlib.Path(temp);run_script(seed_script,parent)
            hioc=parent/"HIOC";hioc.mkdir();artifact=hioc/"artifact.whl";artifact.write_bytes(b"x")
            before=run_script(summary_script,hioc)
            self.assertIn("PROTECTED=False",before);self.assertIn("RULES=3",before);self.assertIn("DENY=1",before)
            COMMON.secure_workstation_path(hioc,True)
            after=run_script(summary_script,hioc)
            for marker in ("PROTECTED=True","RULES=1","INHERITED=0","DENY=0","MINE=1","FULL=1","INHERITANCE=3","PROPAGATION=0"):
                self.assertIn(marker,after)
            COMMON.secure_workstation_path(artifact,False)
            file_after=run_script(summary_script,artifact,False)
            for marker in ("PROTECTED=True","RULES=1","INHERITED=0","DENY=0","MINE=1","FULL=1","INHERITANCE=0","PROPAGATION=0"):
                self.assertIn(marker,file_after)
            COMMON.secure_workstation_path(hioc,True)

    @unittest.skipUnless(os.name == "nt" and shutil.which("powershell.exe"),"Windows ACL integration requires powershell.exe")
    def test_existing_hioc_only_state_recovers_before_use(self):
        with tempfile.TemporaryDirectory() as temp:
            trusted=pathlib.Path(temp);(trusted/"HIOC").mkdir();legacy=trusted/"HIOC/artifacts/pe4"
            cache,staging,evidence=ACTION.roots(cache_resolver=lambda:legacy)
            self.assertTrue(cache.is_dir());self.assertTrue(staging.is_dir());self.assertTrue(evidence.is_dir())

    def test_safe_existing_hierarchy(self):
        with tempfile.TemporaryDirectory() as temp:
            root=pathlib.Path(temp);(root/"HIOC").mkdir()
            result=COMMON.prepare_windows_hierarchy(root,("HIOC",),acl=lambda p,d:None,reparse=lambda p:False)
            self.assertEqual(result,root/"HIOC")

    def test_symlink_or_reparse_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root=pathlib.Path(temp);(root/"HIOC").mkdir()
            secured=[]
            with self.assertRaises(COMMON.Failure):
                COMMON.prepare_windows_hierarchy(root,("HIOC",),acl=lambda p,d:secured.append(p),reparse=lambda p:True)
            self.assertEqual(secured,[])

    def test_unexpected_file_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root=pathlib.Path(temp);(root/"HIOC").write_text("x")
            with self.assertRaises(COMMON.Failure):
                COMMON.prepare_windows_hierarchy(root,("HIOC",),acl=lambda p,d:None,reparse=lambda p:False)

    def test_unsafe_nested_cache_child_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root=pathlib.Path(temp);(root/"HIOC").mkdir();(root/"HIOC/artifacts").mkdir()
            with self.assertRaises(COMMON.Failure):
                COMMON.prepare_windows_hierarchy(root/"HIOC",("artifacts",),acl=lambda p,d:None,reparse=lambda p:True)

    def test_exact_official_endpoint_and_no_proxy_layer(self):
        with self.patched_identity():
            FakeConnection.response=FakeResponse(b"data")
            ACTION.download(connection_factory=FakeConnection,clock=lambda:0)
        instance=FakeConnection.instances[0]
        self.assertEqual(instance.host,"files.pythonhosted.org")
        self.assertEqual(instance.request_data[0],"GET")
        self.assertNotIn("Proxy",(TOOLS/"hioc-pe4-artifact-acquire.py").read_text())

    def test_redirect_is_refused(self):
        with self.patched_identity():
            FakeConnection.response=FakeResponse(status=302,length=0)
            with self.assertRaisesRegex(COMMON.Failure,"ARTIFACT_REDIRECT_REFUSED"):
                ACTION.download(connection_factory=FakeConnection,clock=lambda:0)

    def test_content_length_mismatch(self):
        with self.patched_identity():
            FakeConnection.response=FakeResponse(b"data",length=5)
            with self.assertRaisesRegex(COMMON.Failure,"ARTIFACT_RESPONSE_INVALID"):
                ACTION.download(connection_factory=FakeConnection,clock=lambda:0)

    def test_oversized_response(self):
        with self.patched_identity(b"data"):
            FakeConnection.response=FakeResponse(b"datax",length=4)
            with self.assertRaisesRegex(COMMON.Failure,"ARTIFACT_RESPONSE_TOO_LARGE"):
                ACTION.download(connection_factory=FakeConnection,clock=lambda:0)

    def test_true_total_deadline_expiration(self):
        values=iter((0,0,0,21))
        with self.patched_identity():
            FakeConnection.response=FakeResponse(b"data")
            with self.assertRaisesRegex(COMMON.Failure,"ACQUISITION_DEADLINE_EXCEEDED"):
                ACTION.download(connection_factory=FakeConnection,clock=lambda:next(values))

    def test_normal_download_within_deadline(self):
        with self.patched_identity():
            FakeConnection.response=FakeResponse(b"data")
            self.assertEqual(ACTION.download(connection_factory=FakeConnection,clock=lambda:0),b"data")

    def test_exact_size_validation(self):
        with self.patched_identity():
            with self.assertRaisesRegex(COMMON.Failure,"ARTIFACT_SIZE_MISMATCH"):ACTION.validate_payload(b"bad")

    def test_exact_sha_validation(self):
        with self.patched_identity():
            with self.assertRaisesRegex(COMMON.Failure,"ARTIFACT_SHA256_MISMATCH"):ACTION.validate_payload(b"xxxx")

    def test_matching_cache_is_reused(self):
        with tempfile.TemporaryDirectory() as temp,self.patched_identity():
            root=pathlib.Path(temp);stage=root/"stage";cache=root/"cache";stage.mkdir();cache.mkdir();(cache/ACTION.WHEEL_NAME).write_bytes(b"data")
            self.assertTrue(ACTION.publish_cache(b"data",stage,cache,acl=lambda p,d:None))

    def test_conflicting_cache_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp,self.patched_identity():
            root=pathlib.Path(temp);stage=root/"stage";cache=root/"cache";stage.mkdir();cache.mkdir();(cache/ACTION.WHEEL_NAME).write_bytes(b"bad!")
            with self.assertRaisesRegex(COMMON.Failure,"DURABLE_CACHE_CONFLICT"):ACTION.publish_cache(b"data",stage,cache,acl=lambda p,d:None)

    def test_new_cache_is_published_atomically(self):
        with tempfile.TemporaryDirectory() as temp,self.patched_identity():
            root=pathlib.Path(temp);stage=root/"stage";cache=root/"cache";stage.mkdir();cache.mkdir()
            self.assertFalse(ACTION.publish_cache(b"data",stage,cache,acl=lambda p,d:None));self.assertEqual((cache/ACTION.WHEEL_NAME).read_bytes(),b"data")

    def test_evidence_publication_success(self):
        with tempfile.TemporaryDirectory() as temp:
            directory=pathlib.Path(temp);ACTION.write_windows_evidence(directory,ACTION.initial_state(),"PASS","NONE","COMPLETE",acl=lambda p,d:None)
            self.assertTrue((directory/"result.json").is_file());self.assertFalse((directory/".result.tmp").exists())

    def test_failure_before_cache_publication_is_explicit(self):
        state=ACTION.initial_state();lines=ACTION.terminal_lines(state,"FAIL","ARTIFACT_RESPONSE_INVALID","ACQUISITION",None)
        self.assertIn("DURABLE_CACHE_PUBLISHED=FALSE",lines)

    def test_failure_after_cache_publication_is_explicit(self):
        state=ACTION.initial_state();state["DURABLE_CACHE_PUBLISHED"]="TRUE"
        lines=ACTION.terminal_lines(state,"FAIL","EVIDENCE_PUBLICATION_FAILED","EVIDENCE_PUBLICATION",None)
        self.assertIn("DURABLE_CACHE_PUBLISHED=TRUE",lines);self.assertIn("EVIDENCE_PUBLISHED=FALSE",lines)

    def test_execute_retains_published_state_when_evidence_fails(self):
        with tempfile.TemporaryDirectory() as temp,self.patched_identity(),mock.patch.object(ACTION,"verify_repository"):
            trusted=pathlib.Path(temp);legacy=trusted/"HIOC/artifacts/pe4";FakeConnection.response=FakeResponse(b"data")
            def broken(*args,**kwargs):raise OSError("private detail")
            lines,status=ACTION.execute("a"*40,connection_factory=FakeConnection,clock=lambda:0,
                cache_resolver=lambda:legacy,acl=lambda p,d:None,reparse=lambda p:False,evidence_writer=broken)
            self.assertEqual(status,1);self.assertIn("DURABLE_CACHE_PUBLISHED=TRUE",lines)
            self.assertIn("EVIDENCE_PUBLISHED=FALSE",lines);self.assertIn("ERROR_CODE=EVIDENCE_PUBLICATION_FAILED",lines)

    def test_network_does_not_start_until_complete_hierarchy_is_secured(self):
        failure=COMMON.Failure("WORKSTATION_ACL_APPLICATION_FAILED","WORKSTATION_ACL")
        with mock.patch.object(ACTION,"verify_repository"),mock.patch.object(ACTION,"roots",side_effect=failure),mock.patch.object(ACTION,"download") as download:
            lines,status=ACTION.execute("a"*40)
        self.assertEqual(status,1);download.assert_not_called()
        self.assertIn("ERROR_CODE=WORKSTATION_ACL_APPLICATION_FAILED",lines)

    def test_success_evidence_records_published_true(self):
        with tempfile.TemporaryDirectory() as temp:
            directory=pathlib.Path(temp);state=ACTION.initial_state();state["EVIDENCE_PUBLISHED"]="TRUE"
            ACTION.write_windows_evidence(directory,state,"PASS","NONE","COMPLETE",acl=lambda p,d:None)
            self.assertEqual(json.loads((directory/"result.json").read_text())["evidence_published"],"TRUE")

    def test_partial_success_markers_are_complete(self):
        lines=ACTION.terminal_lines(ACTION.initial_state(),"FAIL","X","Y",None)
        for key in ACTION.STATE_KEYS:self.assertTrue(any(line.startswith(key+"=") for line in lines))

    def test_missing_governance_commit_is_bounded(self):
        with self.assertRaisesRegex(COMMON.Failure,"INVALID_ARGUMENTS"):ACTION.parse_cli([])

    def test_malformed_governance_commit_is_bounded(self):
        with self.assertRaisesRegex(COMMON.Failure,"INVALID_ARGUMENTS"):ACTION.parse_cli(["--governance-commit","bad"])

    def test_unexpected_argument_is_bounded(self):
        with self.assertRaisesRegex(COMMON.Failure,"INVALID_ARGUMENTS"):ACTION.parse_cli(["--other","a"*40])

    def test_duplicate_argument_is_bounded(self):
        with self.assertRaisesRegex(COMMON.Failure,"INVALID_ARGUMENTS"):ACTION.parse_cli(["--governance-commit","a"*40,"--governance-commit","a"*40])

    def test_invalid_cli_prints_no_usage_or_traceback(self):
        output=io.StringIO()
        with contextlib.redirect_stdout(output):status=ACTION.main([])
        self.assertEqual(status,1);self.assertNotIn("usage:",output.getvalue().lower());self.assertNotIn("traceback",output.getvalue().lower())

    def test_cleanup_removes_only_invocation_child(self):
        with tempfile.TemporaryDirectory() as temp:
            parent=pathlib.Path(temp);child=parent/(ACTION.STAGING_PREFIX+"abcd1234");child.mkdir()
            ACTION.safe_remove_invocation(child,parent,ACTION.STAGING_PREFIX,reparse=lambda p:False);self.assertFalse(child.exists())

    def test_cleanup_rejects_cache_root_and_unrelated_path(self):
        with tempfile.TemporaryDirectory() as temp:
            parent=pathlib.Path(temp);other=parent/"other";other.mkdir()
            with self.assertRaises(COMMON.Failure):ACTION.safe_remove_invocation(other,parent,ACTION.STAGING_PREFIX,reparse=lambda p:False)

    def test_cleanup_rejects_descendant_reparse(self):
        with tempfile.TemporaryDirectory() as temp:
            parent=pathlib.Path(temp);child=parent/(ACTION.STAGING_PREFIX+"abcd1234");child.mkdir();nested=child/"nested";nested.mkdir()
            with self.assertRaisesRegex(COMMON.Failure,"CLEANUP_REPARSE_POINT"):
                ACTION.safe_remove_invocation(child,parent,ACTION.STAGING_PREFIX,reparse=lambda p:p==nested)

    def test_reused_artifact_acl_is_revalidated(self):
        with tempfile.TemporaryDirectory() as temp,self.patched_identity():
            root=pathlib.Path(temp);stage=root/"stage";cache=root/"cache";stage.mkdir();cache.mkdir();(cache/ACTION.WHEEL_NAME).write_bytes(b"data");seen=[]
            ACTION.publish_cache(b"data",stage,cache,acl=lambda p,d:seen.append((p,d)))
            self.assertIn((cache/ACTION.WHEEL_NAME,False),seen)

    def test_terminal_includes_action_status(self):
        self.assertIn("ACTION_A=COMPLETE",ACTION.terminal_lines(ACTION.initial_state(),"PASS","NONE","COMPLETE",None))
        self.assertIn("ACTION_A=NOT_COMPLETE",ACTION.terminal_lines(ACTION.initial_state(),"FAIL","X","Y",None))

    def test_source_has_no_raw_exception_or_argparse(self):
        source=(TOOLS/"hioc-pe4-artifact-acquire.py").read_text(encoding="utf-8")
        self.assertNotIn("argparse",source);self.assertNotIn("traceback",source)


if __name__ == "__main__":
    unittest.main()
