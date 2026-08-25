import importlib.util
import base64
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


class Runner:
    def __init__(self, fail_stage=None):
        self.calls = []
        self.fail_stages = {fail_stage} if isinstance(fail_stage, str) else set(fail_stage or ())

    def __call__(self, command, stage, **kwargs):
        self.calls.append((command, stage, kwargs))
        if stage in self.fail_stages:
            raise ACTION_B.Failure("SIMULATED_FAILURE", stage)
        output = "/tmp/hioc-pe4-artifact-transfer-Ab12Cd34\n" if stage == "REMOTE_STAGING" else ""
        return subprocess.CompletedProcess(command, 0, output, "")


class PE4ActionBTransferTests(unittest.TestCase):
    def test_cli_is_exact_and_bounded(self):
        commit = "a" * 40
        self.assertEqual(ACTION_B.parse_cli(["--governance-commit", commit]), commit)
        for args in ([], ["--help"], ["--governance-commit", commit, "extra"], ["--wheel", "x"]):
            with self.assertRaises(ACTION_B.Failure):
                ACTION_B.parse_cli(args)

    @mock.patch.object(ACTION_B, "local_inputs", return_value=(pathlib.Path("C:/cache/wheel.whl"), pathlib.Path("C:/repo/requirements-pe4.lock")))
    def test_exact_host_options_separate_transfers_and_stop_after_evidence(self, _inputs):
        runner = Runner()
        states, remote = ACTION_B.execute("a" * 40, runner=runner,
            resolver=lambda name: pathlib.Path(f"C:/Windows/System32/OpenSSH/{name}.exe"),
            material_resolver=lambda: (pathlib.Path("C:/.ssh/known_hosts"),pathlib.Path("C:/.ssh/id_ed25519")))
        self.assertTrue(all(states.values()))
        self.assertEqual(remote, "/tmp/hioc-pe4-artifact-transfer-Ab12Cd34")
        flattened = [item for call, _, _ in runner.calls for item in call]
        for option in ACTION_B.SSH_STATIC_OPTIONS:
            self.assertIn(option, flattened)
        self.assertNotIn("ssh", flattened)
        self.assertNotIn("scp", flattened)
        self.assertTrue(all("192.168.100.251" not in item for item in flattened))
        stages = [stage for _, stage, _ in runner.calls]
        self.assertEqual(stages, ["REMOTE_STAGING", "WHEEL_TRANSFER", "LOCK_TRANSFER",
                                  "REMOTE_ARTIFACT_PARTIAL", "REMOTE_ARTIFACT_PUBLICATION",
                                  "REMOTE_ARTIFACT_CONFIRMATION", "REMOTE_LOCK_PARTIAL",
                                  "REMOTE_LOCK_PUBLICATION", "REMOTE_LOCK_CONFIRMATION",
                                  "EVIDENCE_PREPARATION", "EVIDENCE_RENAME",
                                  "EVIDENCE_CONFIRMATION"])
        self.assertNotIn("pip", " ".join(flattened))
        self.assertNotIn("venv", " ".join(flattened))

    @mock.patch.object(ACTION_B, "local_inputs", return_value=(pathlib.Path("C:/cache/wheel.whl"), pathlib.Path("C:/repo/requirements-pe4.lock")))
    def test_partial_transfer_failure_publishes_sanitized_state_and_preserves_directory(self, _inputs):
        runner = Runner("LOCK_TRANSFER")
        with self.assertRaises(ACTION_B.Failure) as caught:
            ACTION_B.execute("a" * 40, runner=runner, resolver=lambda name: pathlib.Path(name),
                material_resolver=lambda: (pathlib.Path("known_hosts"),pathlib.Path("id_ed25519")))
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
        prepare = ACTION_B.evidence_prepare_command("/tmp/hioc-pe4-artifact-transfer-Ab12Cd34",
                                                    payload, ".failure-result.tmp")
        publish = ACTION_B.evidence_publish_command("/tmp/hioc-pe4-artifact-transfer-Ab12Cd34",
                                                    ".failure-result.tmp")
        self.assertNotIn("mv --", prepare)
        self.assertNotIn("mv --", publish)
        self.assertIn("O_EXCL", prepare)
        self.assertIn("O_NOFOLLOW", prepare)
        self.assertIn("os.lstat(path)", prepare)
        self.assertIn("renameat2", publish)
        self.assertIn("destination),1", publish)
        command = prepare + publish
        for forbidden in ("token", "credential", "Authorization", "manufacturer", "inventory"):
            self.assertNotIn(forbidden, command)

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
        states, _ = ACTION_B.execute("a" * 40, runner=runner, resolver=lambda name: pathlib.Path(name),
            material_resolver=lambda: (pathlib.Path("known_hosts"),pathlib.Path("id_ed25519")))
        self.assertTrue(states["EVIDENCE_PUBLISHED"])
        self.assertEqual([stage for _,stage,_ in runner.calls][-2:],
                         ["EVIDENCE_RENAME","EVIDENCE_CONFIRMATION"])
        self.assertIn("os.lstat(sys.argv[1])", runner.calls[-1][0][-1])

    @mock.patch.object(ACTION_B, "local_inputs", return_value=(pathlib.Path("C:/cache/wheel.whl"), pathlib.Path("C:/repo/requirements-pe4.lock")))
    def test_artifact_rename_failure_requires_final_identity_and_consumed_source(self, _inputs):
        runner = Runner("REMOTE_ARTIFACT_PUBLICATION")
        states, _ = ACTION_B.execute("a" * 40, runner=runner, resolver=lambda name: pathlib.Path(name),
            material_resolver=lambda: (pathlib.Path("known_hosts"),pathlib.Path("id_ed25519")))
        self.assertTrue(states["REMOTE_ARTIFACT_VERIFIED"])
        command = next(call[-1] for call,stage,_ in runner.calls
                       if stage == "REMOTE_ARTIFACT_CONFIRMATION")
        for required in (ACTION_B.WHEEL_NAME, ACTION_B.WHEEL_SHA256, "stat -c %s",
                         "stat -c %U", "stat -c %a", "os.lstat(sys.argv[1])"):
            self.assertIn(str(required), command)

    @mock.patch.object(ACTION_B, "local_inputs", return_value=(pathlib.Path("C:/cache/wheel.whl"), pathlib.Path("C:/repo/requirements-pe4.lock")))
    def test_retained_artifact_partial_or_bad_final_fails_closed(self, _inputs):
        runner = Runner(("REMOTE_ARTIFACT_PUBLICATION", "REMOTE_ARTIFACT_CONFIRMATION"))
        with self.assertRaises(ACTION_B.Failure) as caught:
            ACTION_B.execute("a" * 40, runner=runner, resolver=lambda name: pathlib.Path(name),
                material_resolver=lambda: (pathlib.Path("known_hosts"),pathlib.Path("id_ed25519")))
        self.assertFalse(caught.exception.states["REMOTE_ARTIFACT_VERIFIED"])

    def test_all_publications_use_atomic_no_replace_and_never_delete_collisions(self):
        source = (TOOLS / "hioc-pe4-artifact-transfer.py").read_text(encoding="utf-8")
        for destination in ("WHEEL_NAME", "requirements-pe4.lock", "result.json"):
            self.assertIn(destination, source)
        for forbidden in ("mv --", "mv -n", "unlink(", "os.remove", "rm -", "shutil.rmtree"):
            self.assertNotIn(forbidden, source)
        self.assertIn("renameat2", ACTION_B.REMOTE_NO_REPLACE)
        self.assertIn("os.lstat(destination)", ACTION_B.REMOTE_NO_REPLACE)
        self.assertIn("else: raise SystemExit(94)", ACTION_B.REMOTE_NO_REPLACE)
        self.assertIn("errno.EEXIST", ACTION_B.REMOTE_NO_REPLACE)

    def test_every_existing_destination_object_is_a_collision(self):
        # lstat observes regular files, directories, symlinks, dangling symlinks,
        # and other directory entries without following them; every success exits 94.
        contract = ACTION_B.REMOTE_NO_REPLACE
        for hostile_kind in ("regular", "directory", "symlink", "dangling-symlink", "other"):
            with self.subTest(hostile_kind=hostile_kind):
                self.assertLess(contract.index("os.lstat(destination)"),
                                contract.index("else: raise SystemExit(94)"))

    def test_destination_raced_in_after_absence_check_is_rejected_atomically(self):
        contract = ACTION_B.REMOTE_NO_REPLACE
        self.assertLess(contract.index("os.lstat(destination)"), contract.index("renameat2("))
        self.assertIn("renameat2(-100,os.fsencode(source),-100,os.fsencode(destination),1)", contract)
        self.assertIn("errno.EEXIST", contract)
        self.assertNotIn("replace(", contract)

    def test_wheel_lock_and_result_publication_commands_are_no_replace(self):
        remote = "/tmp/hioc-pe4-artifact-transfer-Ab12Cd34"
        commands = (
            ACTION_B.no_replace_publish_command(remote, remote+"/.wheel.part", remote+"/"+ACTION_B.WHEEL_NAME),
            ACTION_B.no_replace_publish_command(remote, remote+"/.lock.part", remote+"/requirements-pe4.lock"),
            ACTION_B.evidence_publish_command(remote, ".result.tmp"),
        )
        for command in commands:
            self.assertIn("renameat2", command)
            self.assertIn("os.lstat(destination)", command)
            self.assertNotIn("mv ", command)

    def test_evidence_confirmation_requires_exact_final_and_consumed_temporary(self):
        command = ACTION_B.evidence_confirm_command(
            "/tmp/hioc-pe4-artifact-transfer-Ab12Cd34", "f" * 64, ".result.tmp")
        for required in ("result.json", "sha256sum", "stat -c %U", "stat -c %a",
                         "sync -f", ".result.tmp", "os.lstat(sys.argv[1])"):
            self.assertIn(required, command)

    def test_wrong_final_digest_or_unsafe_metadata_cannot_confirm(self):
        artifact = ACTION_B.artifact_confirm_command(
            "/tmp/hioc-pe4-artifact-transfer-Ab12Cd34", "/tmp/x/.wheel.part",
            "/tmp/x/final.whl", 123, "a" * 64)
        evidence = ACTION_B.evidence_confirm_command(
            "/tmp/hioc-pe4-artifact-transfer-Ab12Cd34", "b" * 64, ".result.tmp")
        for command in (artifact, evidence):
            self.assertIn("test -f", command)
            self.assertIn("test ! -L", command)
            self.assertIn("stat -c %U", command)
            self.assertIn("stat -c %a", command)
            self.assertIn("sha256sum", command)
        self.assertIn("stat -c %s", artifact)

    def test_unrelated_remote_content_is_never_removed_or_enumerated(self):
        source = (TOOLS / "hioc-pe4-artifact-transfer.py").read_text(encoding="utf-8")
        for forbidden in ("rm --", "rm -rf", "unlink", "rmdir", "find \"$d\" -delete"):
            self.assertNotIn(forbidden, source)

    @mock.patch.object(ACTION_B, "local_inputs", return_value=(pathlib.Path("C:/cache/wheel.whl"), pathlib.Path("C:/repo/requirements-pe4.lock")))
    def test_identical_independent_final_with_retained_evidence_temp_fails_closed(self, _inputs):
        runner = Runner(("EVIDENCE_RENAME", "EVIDENCE_CONFIRMATION"))
        with self.assertRaises(ACTION_B.Failure) as caught:
            ACTION_B.execute("a" * 40, runner=runner, resolver=lambda name: pathlib.Path(name),
                material_resolver=lambda: (pathlib.Path("known_hosts"),pathlib.Path("id_ed25519")))
        self.assertFalse(caught.exception.states["EVIDENCE_PUBLISHED"])
        stages = [stage for _,stage,_ in runner.calls]
        self.assertEqual(stages.count("EVIDENCE_PREPARATION"), 1)
        self.assertEqual(stages.count("EVIDENCE_RENAME"), 1)

    @mock.patch.object(ACTION_B, "local_inputs", return_value=(pathlib.Path("C:/cache/wheel.whl"), pathlib.Path("C:/repo/requirements-pe4.lock")))
    def test_failed_pass_evidence_does_not_publish_contradictory_failure_result(self, _inputs):
        runner = Runner("EVIDENCE_CONFIRMATION")
        with self.assertRaises(ACTION_B.Failure):
            ACTION_B.execute("a" * 40, runner=runner, resolver=lambda name: pathlib.Path(name),
                material_resolver=lambda: (pathlib.Path("known_hosts"),pathlib.Path("id_ed25519")))
        evidence_stages = [stage for _,stage,_ in runner.calls if stage.startswith("EVIDENCE_")]
        self.assertEqual(evidence_stages,
                         ["EVIDENCE_PREPARATION", "EVIDENCE_RENAME", "EVIDENCE_CONFIRMATION"])
        joined = "\n".join(call[-1] for call,stage,_ in runner.calls if stage.startswith("EVIDENCE_"))
        self.assertNotIn(".failure-result.tmp", joined)

    @mock.patch.object(ACTION_B, "local_inputs", return_value=(pathlib.Path("C:/cache/wheel.whl"), pathlib.Path("C:/repo/requirements-pe4.lock")))
    def test_unconfirmed_evidence_never_sets_terminal_publication_state(self, _inputs):
        runner = Runner("EVIDENCE_CONFIRMATION")
        with self.assertRaises(ACTION_B.Failure) as caught:
            ACTION_B.execute("a" * 40, runner=runner, resolver=lambda name: pathlib.Path(name),
                material_resolver=lambda: (pathlib.Path("known_hosts"),pathlib.Path("id_ed25519")))
        self.assertFalse(caught.exception.states["EVIDENCE_PUBLISHED"])
        confirm = next(call[-1] for call,stage,_ in runner.calls if stage == "EVIDENCE_CONFIRMATION")
        for required in ("sha256sum", "stat -c %U", "stat -c %a", "sync -f"):
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

    def test_terminal_order_is_bounded_and_includes_partial_directory(self):
        states = {key: False for key in ACTION_B.STATE_KEYS}
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
