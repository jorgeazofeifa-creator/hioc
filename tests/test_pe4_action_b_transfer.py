import importlib.util
import base64
import hashlib
import os
import pathlib
import shlex
import subprocess
import sys
import io
import tempfile
import unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))
spec = importlib.util.spec_from_file_location("pe4_action_b", TOOLS / "hioc-pe4-artifact-transfer.py")
ACTION_B = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ACTION_B)
provision_spec = importlib.util.spec_from_file_location(
    "identity_provision_contract", TOOLS / "hioc-pe4-windows-ssh-identity-provision.py")
PROVISION = importlib.util.module_from_spec(provision_spec)
provision_spec.loader.exec_module(PROVISION)

def fake_transport():
    return pathlib.Path("ssh.exe"), pathlib.Path("known_hosts"), pathlib.Path("id_ed25519")

STAGING_ID=("/tmp/hioc-pe4-artifact-transfer-Ab12Cd34",11,22,1000,0o700)

class Runner:
    def __init__(self, fail_stage=None, outputs=None):
        self.calls = []
        self.fail_stages = {fail_stage} if isinstance(fail_stage, str) else set(fail_stage or ())
        self.outputs = outputs or {}

    def __call__(self, command, stage, **kwargs):
        self.calls.append((command, stage, kwargs))
        if stage in self.fail_stages:
            raise ACTION_B.Failure("SIMULATED_FAILURE", stage)
        output = self.outputs.get(stage, "CONFIRMED\n" if stage == "EVIDENCE_CONFIRMATION" else
                                  "|".join(map(str,STAGING_ID))+"\n" if stage == "REMOTE_STAGING" else "")
        return subprocess.CompletedProcess(command, 0, output, "")


class PE4ActionBTransferTests(unittest.TestCase):
    def test_all_embedded_remote_programs_compile(self):
        for name in ("REMOTE_CREATE_STAGING","REMOTE_NO_REPLACE","REMOTE_EXCLUSIVE_WRITE",
                     "REMOTE_EXCLUSIVE_INGRESS","REMOTE_EVIDENCE_PROBE",
                     "REMOTE_ARTIFACT_VALIDATE","REMOTE_ARTIFACT_CONFIRM"):
            compile(getattr(ACTION_B,name),name,"exec")

    def transport_fixture(self, root, *, operator=None, ssh_digest=None, fingerprint=None,
                          derived=None, known_record=None):
        profile = pathlib.Path(root); ssh_dir = profile / ".ssh"; ssh_dir.mkdir()
        public_fields = ["ssh-ed25519", "AQID", ACTION_B.EXPECTED_PUBLIC_COMMENT]
        (ssh_dir / "id_ed25519.pub").write_text(" ".join(public_fields)+"\n", encoding="ascii")
        (ssh_dir / "id_ed25519").write_text("opaque-private\n", encoding="ascii")
        (ssh_dir / "known_hosts").write_text("opaque-known-host\n", encoding="ascii")
        host_fingerprint = "SHA256:"+base64.b64encode(hashlib.sha256(b"\x01\x02\x03").digest()).decode().rstrip("=")
        outputs = {
            "-lf": fingerprint or f"256 {ACTION_B.EXPECTED_PUBLIC_FINGERPRINT} comment (ED25519)\n",
            "-y": derived or "ssh-ed25519 AQID\n",
            "-F": known_record or "192.168.100.252 ssh-ed25519 AQID\n",
        }
        def runner(command, stage, **kwargs):
            key = next(flag for flag in ("-lf", "-y", "-F") if flag in command)
            return subprocess.CompletedProcess(command, 0, outputs[key], "")
        def resolver(name): return profile / (name+".exe")
        def hasher(path):
            if path.name == "ssh.exe": return ssh_digest or ACTION_B.SSH_CLIENT_SHA256
            return ACTION_B.SSH_KEYGEN_SHA256
        patches = (mock.patch.object(ACTION_B.os,"name","nt"),
                   mock.patch.object(ACTION_B,"EXPECTED_WINDOWS_PROFILE",pathlib.PureWindowsPath(profile)),
                   mock.patch.object(ACTION_B,"EXPECTED_HOST_FINGERPRINT",host_fingerprint),
                   mock.patch.object(ACTION_B,"windows_reparse_point",return_value=False))
        return profile, runner, resolver, hasher, patches, operator or ACTION_B.EXPECTED_WINDOWS_OPERATOR

    def test_cli_is_exact_and_bounded(self):
        commit = "a" * 40
        self.assertEqual(ACTION_B.parse_cli(["--governance-commit", commit]), commit)
        for args in ([], ["--help"], ["--governance-commit", commit, "extra"], ["--wheel", "x"]):
            with self.assertRaises(ACTION_B.Failure):
                ACTION_B.parse_cli(args)

    @mock.patch.object(ACTION_B, "local_inputs", return_value=(pathlib.Path("C:/cache/wheel.whl"), pathlib.Path("C:/repo/requirements-pe4.lock")))
    def test_exact_host_options_separate_transfers_and_stop_after_evidence(self, _inputs):
        runner = Runner()
        states, remote = ACTION_B.execute("a" * 40, runner=runner, transport_validator=fake_transport)
        self.assertTrue(all(states[key] for key in ACTION_B.STATE_KEYS))
        self.assertEqual(states["EVIDENCE_STATE"], "CONFIRMED")
        self.assertEqual(remote, "/tmp/hioc-pe4-artifact-transfer-Ab12Cd34")
        flattened = [item for call, _, _ in runner.calls for item in call]
        for option in ACTION_B.SSH_STATIC_OPTIONS:
            self.assertIn(option, flattened)
        self.assertNotIn("ssh", flattened)
        self.assertNotIn("scp", flattened)
        self.assertTrue(all("192.168.100.251" not in item for item in flattened))
        stages = [stage for _, stage, _ in runner.calls]
        self.assertEqual(stages, ["REMOTE_STAGING", "WHEEL_TRANSFER",
                                  "REMOTE_ARTIFACT_PARTIAL", "REMOTE_ARTIFACT_PUBLICATION",
                                  "REMOTE_ARTIFACT_CONFIRMATION", "LOCK_TRANSFER",
                                  "REMOTE_LOCK_PARTIAL",
                                  "REMOTE_LOCK_PUBLICATION", "REMOTE_LOCK_CONFIRMATION",
                                  "EVIDENCE_PREPARATION", "EVIDENCE_RENAME",
                                  "EVIDENCE_CONFIRMATION"])
        self.assertNotIn("pip", " ".join(flattened))
        self.assertNotIn("venv", " ".join(flattened))

    @mock.patch.object(ACTION_B, "local_inputs", return_value=(pathlib.Path("C:/cache/wheel.whl"), pathlib.Path("C:/repo/requirements-pe4.lock")))
    def test_partial_transfer_failure_publishes_sanitized_state_and_preserves_directory(self, _inputs):
        runner = Runner("LOCK_TRANSFER")
        with self.assertRaises(ACTION_B.Failure) as caught:
            ACTION_B.execute("a" * 40, runner=runner, transport_validator=fake_transport)
        exc = caught.exception
        self.assertTrue(exc.states["REMOTE_STAGING_CREATED"])
        self.assertTrue(exc.states["WHEEL_TRANSFERRED"])
        self.assertFalse(exc.states["LOCK_TRANSFERRED"])
        self.assertEqual(exc.remote, "/tmp/hioc-pe4-artifact-transfer-Ab12Cd34")
        self.assertEqual([stage for _,stage,_ in runner.calls][-3:],
                         ["EVIDENCE_PREPARATION","EVIDENCE_RENAME","EVIDENCE_CONFIRMATION"])
        evidence = runner.calls[-3][0][-1]
        payload = base64.b64decode(shlex.split(evidence)[-1], validate=True).decode("utf-8")
        self.assertIn('"wheel_transferred":true', payload)
        self.assertIn('"lock_transferred":false', payload)
        self.assertNotIn("SIMULATED_FAILURE\n", payload)
        self.assertNotIn("rm ", evidence)

    def test_evidence_is_result_last_and_contains_only_bounded_state(self):
        states = {key: False for key in ACTION_B.STATE_KEYS}
        payload = ACTION_B.evidence_payload(states, "FAIL", "TRANSFER_FAILED", "WHEEL_TRANSFER")
        self.assertIn('"evidence_state":"AWAITING_CONFIRMATION"',payload)
        prepare = ACTION_B.evidence_prepare_command(STAGING_ID,
                                                    payload, ".failure-result.tmp")
        publish = ACTION_B.evidence_publish_command(STAGING_ID,
                                                    ".failure-result.tmp")
        self.assertNotIn("mv --", prepare)
        self.assertNotIn("mv --", publish)
        self.assertIn("O_EXCL", prepare)
        self.assertIn("O_NOFOLLOW", prepare)
        self.assertIn("follow_symlinks=False", prepare)
        self.assertIn("renameat2", publish)
        self.assertIn("destination),1", publish)
        command = prepare + publish
        for forbidden in ("token", "credential", "Authorization", "manufacturer", "inventory"):
            self.assertNotIn(forbidden, command)

    def test_transport_identity_validates_operator_tools_pair_fingerprint_and_host(self):
        with tempfile.TemporaryDirectory() as temp:
            profile,runner,resolver,hasher,patches,operator=self.transport_fixture(temp)
            with patches[0],patches[1],patches[2],patches[3]:
                ssh,known,private=ACTION_B.validate_local_transport(
                    resolver=resolver,runner=runner,operator_resolver=lambda:operator,
                    profile_resolver=lambda:profile,hasher=hasher,acl_validator=lambda *_:None)
            self.assertEqual((ssh.name,known.name,private.name),("ssh.exe","known_hosts","id_ed25519"))

    def test_transport_identity_rejects_wrong_operator_and_ssh_digest(self):
        for defect in ("operator","ssh"):
            with self.subTest(defect=defect), tempfile.TemporaryDirectory() as temp:
                profile,runner,resolver,hasher,patches,operator=self.transport_fixture(
                    temp,operator="intruder" if defect=="operator" else None,
                    ssh_digest="0"*64 if defect=="ssh" else None)
                with patches[0],patches[1],patches[2],patches[3], self.assertRaises(ACTION_B.Failure):
                    ACTION_B.validate_local_transport(resolver=resolver,runner=runner,
                        operator_resolver=lambda:operator,profile_resolver=lambda:profile,hasher=hasher,acl_validator=lambda *_:None)

    def test_transport_identity_rejects_wrong_pair_fingerprint_and_known_host(self):
        variants=(
            {"derived":"ssh-ed25519 BAUG\n"},
            {"fingerprint":"256 SHA256:wrong comment (ED25519)\n"},
            {"known_record":"192.168.100.252 ssh-rsa AQID\n"},
        )
        for variant in variants:
            with self.subTest(variant=variant), tempfile.TemporaryDirectory() as temp:
                profile,runner,resolver,hasher,patches,operator=self.transport_fixture(temp,**variant)
                with patches[0],patches[1],patches[2],patches[3], self.assertRaises(ACTION_B.Failure):
                    ACTION_B.validate_local_transport(resolver=resolver,runner=runner,
                        operator_resolver=lambda:operator,profile_resolver=lambda:profile,hasher=hasher,acl_validator=lambda *_:None)

    def test_numeric_known_host_requires_exactly_one_record(self):
        valid="192.168.100.252 ssh-ed25519 AQID\n"
        for value in (valid+valid, valid+"192.168.100.252 ssh-ed25519 BAUG\n",
                      valid+"192.168.100.252 ssh-rsa AQID\n", "# no numeric match\n"):
            with self.subTest(value=value), tempfile.TemporaryDirectory() as temp:
                profile,runner,resolver,hasher,patches,operator=self.transport_fixture(temp,known_record=value)
                with patches[0],patches[1],patches[2],patches[3], self.assertRaises(ACTION_B.Failure):
                    ACTION_B.validate_local_transport(resolver=resolver,runner=runner,
                        operator_resolver=lambda:operator,profile_resolver=lambda:profile,
                        hasher=hasher,acl_validator=lambda *_:None)

    def test_transport_acl_is_required_for_directory_and_all_three_files(self):
        with tempfile.TemporaryDirectory() as temp:
            profile,runner,resolver,hasher,patches,operator=self.transport_fixture(temp)
            calls=[]
            with patches[0],patches[1],patches[2],patches[3]:
                ACTION_B.validate_local_transport(resolver=resolver,runner=runner,
                    operator_resolver=lambda:operator,profile_resolver=lambda:profile,hasher=hasher,
                    acl_validator=lambda path,is_dir:calls.append((path.name,is_dir)))
            self.assertEqual(calls,[(".ssh",True),("known_hosts",False),("id_ed25519",False),("id_ed25519.pub",False)])
        for failed_name in (".ssh","known_hosts","id_ed25519","id_ed25519.pub"):
            with self.subTest(failed_name=failed_name), tempfile.TemporaryDirectory() as temp:
                profile,runner,resolver,hasher,patches,operator=self.transport_fixture(temp)
                def reject(path,_is_dir):
                    if path.name==failed_name: raise ACTION_B.Failure("WORKSTATION_ACL_UNSAFE","WORKSTATION_ACL")
                with patches[0],patches[1],patches[2],patches[3], self.assertRaises(ACTION_B.Failure):
                    ACTION_B.validate_local_transport(resolver=resolver,runner=runner,
                        operator_resolver=lambda:operator,profile_resolver=lambda:profile,
                        hasher=hasher,acl_validator=reject)

    def test_shared_acl_contract_covers_read_protection_principal_rights_and_inheritance(self):
        captured={}
        def fake_run(_command,_stage,**kwargs): captured.update(kwargs)
        with mock.patch.dict(ACTION_B.validate_workstation_path_acl.__globals__,{"run":fake_run}):
            ACTION_B.validate_workstation_path_acl(pathlib.Path("C:/fixture/.ssh"),True)
        self.assertEqual(captured["failure_codes"],{
            21:"WORKSTATION_ACL_VALIDATION_READ_FAILED",22:"WORKSTATION_ACL_NOT_PROTECTED",
            23:"WORKSTATION_ACL_RULE_COUNT_INVALID",24:"WORKSTATION_ACL_INHERITED_RULE_REMAINS",
            25:"WORKSTATION_ACL_IDENTITY_INVALID",26:"WORKSTATION_ACL_RULE_TYPE_INVALID",
            27:"WORKSTATION_ACL_RIGHTS_INVALID",28:"WORKSTATION_ACL_INHERITANCE_INVALID",
            29:"WORKSTATION_ACL_PROPAGATION_INVALID"})

    def test_ingress_uses_exclusive_nofollow_directory_fd_and_streamed_input(self):
        command=ACTION_B.ingress_command(STAGING_ID,
                                         ".wheel.part",3,hashlib.sha256(b"abc").hexdigest())
        for required in ("O_EXCL","O_NOFOLLOW","dir_fd=directory_fd","sys.stdin.buffer",
                         "actual!=expected","hashlib.sha256"):
            self.assertIn(required,command)
        self.assertNotIn("scp",command)

    @unittest.skipUnless(os.name=="posix" and hasattr(os,"O_DIRECTORY") and hasattr(os,"O_NOFOLLOW"),
                         "Linux exclusive-ingress primitive requires POSIX O_DIRECTORY/O_NOFOLLOW")
    def test_linux_ingress_primitive_real_success_and_all_collision_types(self):
        data=b"governed-bytes"; digest=hashlib.sha256(data).hexdigest()
        for kind in ("regular","directory","symlink","dangling"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as temp:
                root=pathlib.Path(temp); os.chmod(root,0o700); target=root/".wheel.part"
                if kind=="regular": target.write_bytes(b"foreign")
                elif kind=="directory": target.mkdir()
                elif kind=="symlink": target.symlink_to(root/"outside")
                else: target.symlink_to(root/"missing")
                result=subprocess.run([sys.executable,"-c",ACTION_B.REMOTE_EXCLUSIVE_INGRESS,
                    str(root),str(root.stat().st_dev),str(root.stat().st_ino),str(root.stat().st_uid),str(0o700),target.name,str(len(data)),digest],input=data,capture_output=True)
                self.assertNotEqual(result.returncode,0)
        with tempfile.TemporaryDirectory() as temp:
            root=pathlib.Path(temp); os.chmod(root,0o700)
            result=subprocess.run([sys.executable,"-c",ACTION_B.REMOTE_EXCLUSIVE_INGRESS,
                str(root),str(root.stat().st_dev),str(root.stat().st_ino),str(root.stat().st_uid),str(0o700),".wheel.part",str(len(data)),digest],input=data,capture_output=True)
            self.assertEqual(result.returncode,0)
            self.assertEqual((root/".wheel.part").read_bytes(),data)

    @unittest.skipUnless(os.name=="posix" and hasattr(os,"O_DIRECTORY") and hasattr(os,"O_NOFOLLOW"),
                         "Linux directory-substitution integration requires POSIX directory identity")
    def test_linux_whole_directory_replacement_rejects_same_mode_owner_and_content(self):
        data=b"governed-bytes"; digest=hashlib.sha256(data).hexdigest()
        with tempfile.TemporaryDirectory() as temp:
            parent=pathlib.Path(temp); original=parent/"transaction"; original.mkdir(); os.chmod(original,0o700)
            info=original.stat(); moved=parent/"moved"; original.rename(moved)
            original.mkdir(); os.chmod(original,0o700); (original/".wheel.part").write_bytes(data)
            result=subprocess.run([sys.executable,"-c",ACTION_B.REMOTE_EXCLUSIVE_INGRESS,
                str(original),str(info.st_dev),str(info.st_ino),str(info.st_uid),str(0o700),
                ".lock.part",str(len(data)),digest],input=data,capture_output=True)
            self.assertNotEqual(result.returncode,0)
            self.assertFalse((original/".lock.part").exists())
            self.assertEqual((original/".wheel.part").read_bytes(),data)

    def test_every_remote_primitive_enforces_creation_token_before_child_access(self):
        for primitive in (ACTION_B.REMOTE_EXCLUSIVE_INGRESS,ACTION_B.REMOTE_EXCLUSIVE_WRITE,
                          ACTION_B.REMOTE_NO_REPLACE,ACTION_B.REMOTE_ARTIFACT_VALIDATE,
                          ACTION_B.REMOTE_ARTIFACT_CONFIRM,ACTION_B.REMOTE_EVIDENCE_PROBE):
            self.assertIn("actual!=expected",primitive)
            self.assertIn("os.O_DIRECTORY|os.O_NOFOLLOW",primitive)
            self.assertLess(primitive.index("actual!=expected"),primitive.index("dir_fd=directory_fd"))

    @unittest.skipUnless(os.name=="posix", "Linux renameat2 integration fixture")
    def test_linux_renameat2_real_no_replace_and_source_consumption(self):
        with tempfile.TemporaryDirectory() as temp:
            root=pathlib.Path(temp); os.chmod(root,0o700); source=root/".wheel.part"; final=root/ACTION_B.WHEEL_NAME
            source.write_bytes(b"owned")
            info=root.stat()
            result=subprocess.run([sys.executable,"-c",ACTION_B.REMOTE_NO_REPLACE,
                                   str(root),str(info.st_dev),str(info.st_ino),str(info.st_uid),str(0o700),source.name,final.name],capture_output=True)
            self.assertEqual(result.returncode,0)
            self.assertFalse(source.exists()); self.assertEqual(final.read_bytes(),b"owned")
        with tempfile.TemporaryDirectory() as temp:
            root=pathlib.Path(temp); os.chmod(root,0o700); source=root/".wheel.part"; final=root/ACTION_B.WHEEL_NAME
            source.write_bytes(b"owned"); final.write_bytes(b"foreign")
            info=root.stat()
            result=subprocess.run([sys.executable,"-c",ACTION_B.REMOTE_NO_REPLACE,
                                   str(root),str(info.st_dev),str(info.st_ino),str(info.st_uid),str(0o700),source.name,final.name],capture_output=True)
            self.assertNotEqual(result.returncode,0)
            self.assertEqual(source.read_bytes(),b"owned"); self.assertEqual(final.read_bytes(),b"foreign")

    def test_evidence_terminal_states_are_confirmed_not_published_or_uncertain(self):
        base={key:False for key in ACTION_B.STATE_KEYS}; base["EVIDENCE_STATE"]="NOT_PUBLISHED"
        for marker,raises in (("CONFIRMED\n",False),("NOT_PUBLISHED\n",True),("UNCERTAIN\n",True)):
            states=dict(base); runner=Runner(outputs={"EVIDENCE_CONFIRMATION":marker})
            if raises:
                with self.assertRaises(ACTION_B.Failure):
                    ACTION_B.publish_evidence(runner,["ssh"],STAGING_ID,
                                              states,"PASS","NONE","COMPLETE",".result.tmp")
            else:
                ACTION_B.publish_evidence(runner,["ssh"],STAGING_ID,
                                          states,"PASS","NONE","COMPLETE",".result.tmp")
            self.assertEqual(states["EVIDENCE_STATE"],marker.strip())

    def test_hostile_ssh_configuration_cannot_change_transport(self):
        options = ACTION_B.transport_options(pathlib.Path("C:/.ssh/known_hosts"),
                                             pathlib.Path("C:/.ssh/id_ed25519"))
        joined = "\n".join(options)
        for required in ("-F\nnone", "-oHostname=192.168.100.252", "-oPort=22",
                         "-oProxyCommand=none", "-oProxyJump=none",
                         "-oCanonicalizeHostname=no", "-oGlobalKnownHostsFile=none",
                         "-oUserKnownHostsFile=C:\\.ssh\\known_hosts",
                         "-oIdentityFile=C:\\.ssh\\id_ed25519", "-oIdentityAgent=none"):
            self.assertIn(required, joined)
        hostile = "Host 192.168.100.252\n Hostname attacker.invalid\n ProxyJump attacker\n IdentityFile stolen"
        self.assertTrue(all(line.strip() not in joined for line in hostile.splitlines()))

    def test_only_fixed_non_reparse_profile_material_is_accepted(self):
        with tempfile.TemporaryDirectory() as temp:
            profile = pathlib.Path(temp)
            ssh = profile / ".ssh"; ssh.mkdir()
            known = ssh / "known_hosts"; known.write_text("host-key-record\n", encoding="ascii")
            identity = ssh / "id_ed25519"; identity.write_text("opaque-private-material\n", encoding="ascii")
            with mock.patch.dict(ACTION_B.windows_openssh_material.__globals__,
                                 {"windows_profile_root": lambda: profile}):
                self.assertEqual(ACTION_B.windows_openssh_material(), (known, identity))
                identity.write_bytes(b"")
                with self.assertRaises(ACTION_B.Failure):
                    ACTION_B.windows_openssh_material()

    def test_action_b_and_provisioning_share_the_dedicated_identity_contract(self):
        self.assertEqual(ACTION_B.SSH_IDENTITY_NAME, "id_ed25519")
        self.assertEqual(PROVISION.SSH_IDENTITY_NAME, ACTION_B.SSH_IDENTITY_NAME)
        with tempfile.TemporaryDirectory() as temp:
            profile = pathlib.Path(temp); (profile / ".ssh").mkdir()
            with mock.patch.object(PROVISION.os, "name", "nt"), \
                 mock.patch.object(PROVISION, "EXPECTED_PROFILE", pathlib.PureWindowsPath(str(profile))):
                _ssh, private, public = PROVISION.target_paths(
                    profile_resolver=lambda: profile,
                    operator_resolver=lambda: PROVISION.EXPECTED_OPERATOR,
                    reparse=lambda _: False)
        self.assertEqual(private.name, ACTION_B.SSH_IDENTITY_NAME)
        self.assertEqual(public.name, ACTION_B.SSH_IDENTITY_NAME + ".pub")

    @mock.patch.object(ACTION_B, "local_inputs", return_value=(pathlib.Path("C:/cache/wheel.whl"), pathlib.Path("C:/repo/requirements-pe4.lock")))
    def test_post_rename_failure_is_reconciled_by_exact_confirmation(self, _inputs):
        runner = Runner("EVIDENCE_RENAME")
        states, _ = ACTION_B.execute("a" * 40, runner=runner, transport_validator=fake_transport)
        self.assertEqual(states["EVIDENCE_STATE"], "CONFIRMED")
        self.assertEqual([stage for _,stage,_ in runner.calls][-2:],
                         ["EVIDENCE_RENAME","EVIDENCE_CONFIRMATION"])
        self.assertIn("follow_symlinks=False", runner.calls[-1][0][-1])

    @mock.patch.object(ACTION_B, "local_inputs", return_value=(pathlib.Path("C:/cache/wheel.whl"), pathlib.Path("C:/repo/requirements-pe4.lock")))
    def test_artifact_rename_failure_requires_final_identity_and_consumed_source(self, _inputs):
        runner = Runner("REMOTE_ARTIFACT_PUBLICATION")
        states, _ = ACTION_B.execute("a" * 40, runner=runner, transport_validator=fake_transport)
        self.assertTrue(states["REMOTE_ARTIFACT_VERIFIED"])
        command = next(call[-1] for call,stage,_ in runner.calls
                       if stage == "REMOTE_ARTIFACT_CONFIRMATION")
        for required in (ACTION_B.WHEEL_NAME, ACTION_B.WHEEL_SHA256, "info.st_size",
                         "info.st_uid", "stat.S_IMODE", "follow_symlinks=False"):
            self.assertIn(str(required), command)

    @mock.patch.object(ACTION_B, "local_inputs", return_value=(pathlib.Path("C:/cache/wheel.whl"), pathlib.Path("C:/repo/requirements-pe4.lock")))
    def test_retained_artifact_partial_or_bad_final_fails_closed(self, _inputs):
        runner = Runner(("REMOTE_ARTIFACT_PUBLICATION", "REMOTE_ARTIFACT_CONFIRMATION"))
        with self.assertRaises(ACTION_B.Failure) as caught:
            ACTION_B.execute("a" * 40, runner=runner, transport_validator=fake_transport)
        self.assertFalse(caught.exception.states["REMOTE_ARTIFACT_VERIFIED"])

    def test_all_publications_use_atomic_no_replace_and_never_delete_collisions(self):
        source = (TOOLS / "hioc-pe4-artifact-transfer.py").read_text(encoding="utf-8")
        for destination in ("WHEEL_NAME", "requirements-pe4.lock", "result.json"):
            self.assertIn(destination, source)
        for forbidden in ("mv --", "mv -n", "unlink(", "os.remove", "rm -", "shutil.rmtree"):
            self.assertNotIn(forbidden, source)
        self.assertIn("renameat2", ACTION_B.REMOTE_NO_REPLACE)
        self.assertIn("os.stat(destination", ACTION_B.REMOTE_NO_REPLACE)
        self.assertIn("else: os.close(directory_fd); raise SystemExit(94)", ACTION_B.REMOTE_NO_REPLACE)
        self.assertIn("errno.EEXIST", ACTION_B.REMOTE_NO_REPLACE)

    def test_every_existing_destination_object_is_a_collision(self):
        # lstat observes regular files, directories, symlinks, dangling symlinks,
        # and other directory entries without following them; every success exits 94.
        contract = ACTION_B.REMOTE_NO_REPLACE
        for hostile_kind in ("regular", "directory", "symlink", "dangling-symlink", "other"):
            with self.subTest(hostile_kind=hostile_kind):
                self.assertLess(contract.index("os.stat(destination"),
                                contract.index("else: os.close(directory_fd); raise SystemExit(94)"))

    def test_destination_raced_in_after_absence_check_is_rejected_atomically(self):
        contract = ACTION_B.REMOTE_NO_REPLACE
        self.assertLess(contract.index("os.stat(destination"), contract.index("renameat2("))
        self.assertIn("renameat2(directory_fd,os.fsencode(source),directory_fd,os.fsencode(destination),1)", contract)
        self.assertIn("errno.EEXIST", contract)
        self.assertNotIn("replace(", contract)

    def test_wheel_lock_and_result_publication_commands_are_no_replace(self):
        commands = (
            ACTION_B.no_replace_publish_command(STAGING_ID, ".wheel.part", ACTION_B.WHEEL_NAME),
            ACTION_B.no_replace_publish_command(STAGING_ID, ".lock.part", "requirements-pe4.lock"),
            ACTION_B.evidence_publish_command(STAGING_ID, ".result.tmp"),
        )
        for command in commands:
            self.assertIn("renameat2", command)
            self.assertIn("os.stat(destination", command)
            self.assertNotIn("mv ", command)

    def test_evidence_confirmation_requires_exact_final_and_consumed_temporary(self):
        command = ACTION_B.evidence_confirm_command(
            STAGING_ID, "f" * 64, ".result.tmp")
        for required in ("result.json", "hashlib.sha256", "stat.S_ISREG",
                         "stat.S_IMODE", "os.fsync", ".result.tmp", "follow_symlinks=False"):
            self.assertIn(required, command)

    def test_wrong_final_digest_or_unsafe_metadata_cannot_confirm(self):
        artifact = ACTION_B.artifact_confirm_command(
            STAGING_ID, ".wheel.part", ACTION_B.WHEEL_NAME, 123, "a" * 64)
        evidence = ACTION_B.evidence_confirm_command(
            STAGING_ID, "b" * 64, ".result.tmp")
        for command in (artifact,evidence):
            for required in ("stat.S_ISREG", "stat.S_IMODE", "hashlib.sha256", "os.O_NOFOLLOW"):
                self.assertIn(required, command)

    def test_unrelated_remote_content_is_never_removed_or_enumerated(self):
        source = (TOOLS / "hioc-pe4-artifact-transfer.py").read_text(encoding="utf-8")
        for forbidden in ("rm --", "rm -rf", "unlink", "rmdir", "find \"$d\" -delete"):
            self.assertNotIn(forbidden, source)

    @mock.patch.object(ACTION_B, "local_inputs", return_value=(pathlib.Path("C:/cache/wheel.whl"), pathlib.Path("C:/repo/requirements-pe4.lock")))
    def test_identical_independent_final_with_retained_evidence_temp_fails_closed(self, _inputs):
        runner = Runner(("EVIDENCE_RENAME", "EVIDENCE_CONFIRMATION"))
        with self.assertRaises(ACTION_B.Failure) as caught:
            ACTION_B.execute("a" * 40, runner=runner, transport_validator=fake_transport)
        self.assertEqual(caught.exception.states["EVIDENCE_STATE"], "UNCERTAIN")
        stages = [stage for _,stage,_ in runner.calls]
        self.assertEqual(stages.count("EVIDENCE_PREPARATION"), 1)
        self.assertEqual(stages.count("EVIDENCE_RENAME"), 1)

    @mock.patch.object(ACTION_B, "local_inputs", return_value=(pathlib.Path("C:/cache/wheel.whl"), pathlib.Path("C:/repo/requirements-pe4.lock")))
    def test_failed_pass_evidence_does_not_publish_contradictory_failure_result(self, _inputs):
        runner = Runner("EVIDENCE_CONFIRMATION")
        with self.assertRaises(ACTION_B.Failure):
            ACTION_B.execute("a" * 40, runner=runner, transport_validator=fake_transport)
        evidence_stages = [stage for _,stage,_ in runner.calls if stage.startswith("EVIDENCE_")]
        self.assertEqual(evidence_stages,
                         ["EVIDENCE_PREPARATION", "EVIDENCE_RENAME", "EVIDENCE_CONFIRMATION"])
        prepare_command=next(call[-1] for call,stage,_ in runner.calls if stage=="EVIDENCE_PREPARATION")
        self.assertIn(".result.tmp result.json",prepare_command)

    @mock.patch.object(ACTION_B, "local_inputs", return_value=(pathlib.Path("C:/cache/wheel.whl"), pathlib.Path("C:/repo/requirements-pe4.lock")))
    def test_unconfirmed_evidence_never_sets_terminal_publication_state(self, _inputs):
        runner = Runner("EVIDENCE_CONFIRMATION")
        with self.assertRaises(ACTION_B.Failure) as caught:
            ACTION_B.execute("a" * 40, runner=runner, transport_validator=fake_transport)
        self.assertEqual(caught.exception.states["EVIDENCE_STATE"], "UNCERTAIN")
        confirm = next(call[-1] for call,stage,_ in runner.calls if stage == "EVIDENCE_CONFIRMATION")
        for required in ("hashlib.sha256", "stat.S_ISREG", "stat.S_IMODE", "os.fsync"):
            self.assertIn(required, confirm)

    def test_source_has_no_path_selected_artifact_or_lifecycle_chaining(self):
        source = (TOOLS / "hioc-pe4-artifact-transfer.py").read_text(encoding="utf-8")
        self.assertIn('("HIOC","artifacts","pe4","cache")', source)
        self.assertNotIn("--wheel", source)
        self.assertNotIn("workstation_cache_root(); wheel=cache/WHEEL_NAME", source)
        for forbidden in ("release/upgrade.sh", "systemctl", "pip install", "ACTION_C"):
            self.assertNotIn(forbidden, source)

    def test_real_subprocess_boundary_fails_closed_on_output_overflow(self):
        with self.assertRaises(ACTION_B.Failure) as caught:
            ACTION_B.run_bounded([sys.executable, "-c", "import sys;sys.stdout.write('x'*9000)"],
                                 "TEST_BOUNDARY", timeout=5, max_output=1024)
        self.assertEqual((caught.exception.code, caught.exception.stage),
                         ("COMMAND_OUTPUT_TOO_LARGE", "TEST_BOUNDARY"))

    def test_bounded_runner_streams_exact_file_stdin_and_times_out_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            source=pathlib.Path(temp)/"source.bin"; source.write_bytes(b"streamed")
            result=ACTION_B.run_bounded([sys.executable,"-c",
                "import sys;sys.stdout.buffer.write(sys.stdin.buffer.read())"],
                "STREAM",timeout=5,max_output=32,stdin_path=source)
            self.assertEqual(result.stdout,"streamed")
        with self.assertRaises(ACTION_B.Failure) as caught:
            ACTION_B.run_bounded([sys.executable,"-c","import time;time.sleep(2)"],
                                 "TIMEOUT",timeout=1,max_output=32)
        self.assertEqual((caught.exception.code,caught.exception.stage),("COMMAND_TIMEOUT","TIMEOUT"))

    @mock.patch.object(ACTION_B, "local_inputs", return_value=(pathlib.Path("C:/cache/wheel.whl"), pathlib.Path("C:/repo/requirements-pe4.lock")))
    def test_transfer_failure_never_marks_unconfirmed_ingress_complete(self, _inputs):
        runner=Runner("WHEEL_TRANSFER")
        with self.assertRaises(ACTION_B.Failure) as caught:
            ACTION_B.execute("a"*40,runner=runner,transport_validator=fake_transport)
        self.assertFalse(caught.exception.states["WHEEL_TRANSFERRED"])
        transfer=next((call,kwargs) for call,stage,kwargs in runner.calls if stage=="WHEEL_TRANSFER")
        self.assertEqual(transfer[1]["stdin_path"],pathlib.Path("C:/cache/wheel.whl"))

    def test_terminal_order_is_bounded_and_includes_partial_directory(self):
        states = {key: False for key in ACTION_B.STATE_KEYS}
        states["EVIDENCE_STATE"] = "NOT_PUBLISHED"
        states["REMOTE_STAGING_CREATED"] = True
        output = io.StringIO()
        with mock.patch("sys.stdout", output):
            ACTION_B.emit(states, "FAIL", "TRANSFER_FAILED", "WHEEL_TRANSFER",
                          "/tmp/hioc-pe4-artifact-transfer-Ab12Cd34")
        lines = output.getvalue().splitlines()
        self.assertEqual(lines[-5:], ["RESULT=FAIL", "ERROR_CODE=TRANSFER_FAILED",
                                      "FAILURE_STAGE=WHEEL_TRANSFER",
                                      "ROLLBACK_RECOMMENDED=FALSE",
                                      "TRANSFER_DIRECTORY=/tmp/hioc-pe4-artifact-transfer-Ab12Cd34"])


if __name__ == "__main__":
    unittest.main()
