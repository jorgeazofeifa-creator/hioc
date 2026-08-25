import importlib.util
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))
spec = importlib.util.spec_from_file_location("identity_provision", TOOLS / "hioc-pe4-windows-ssh-identity-provision.py")
PROVISION = importlib.util.module_from_spec(spec)
spec.loader.exec_module(PROVISION)


class Result:
    def __init__(self, stdout=""):
        self.stdout = stdout


class IdentityProvisionTests(unittest.TestCase):
    def test_cli_is_governance_commit_only(self):
        commit = "a" * 40
        self.assertEqual(PROVISION.parse_cli(["--governance-commit", commit]), commit)
        for argv in ([], ["--profile", "C:/x"], ["--governance-commit", commit, "--host", "x"]):
            with self.assertRaises(PROVISION.Failure): PROVISION.parse_cli(argv)

    def test_fixed_contract_has_empty_passphrase_and_no_transport(self):
        source = (TOOLS / "hioc-pe4-windows-ssh-identity-provision.py").read_text(encoding="utf-8")
        for value in ('"-t", "ed25519"', '"-N", ""', "KEY_COMMENT", 'resolver("ssh-keygen")'):
            self.assertIn(value, source)
        for forbidden in ("ssh-agent", "known_hosts", "PI3_IPV4", "scp.exe", "ssh.exe", "Action C"):
            self.assertNotIn(forbidden, source)

    def test_non_windows_fails_closed(self):
        with mock.patch.object(PROVISION.os, "name", "posix"):
            with self.assertRaises(PROVISION.Failure) as caught: PROVISION.target_paths()
        self.assertEqual((caught.exception.code, caught.exception.stage), ("WRONG_TARGET_OS", "TARGET_OS"))

    def test_operator_and_profile_are_fixed(self):
        with tempfile.TemporaryDirectory() as temp:
            profile = pathlib.Path(temp)
            with mock.patch.object(PROVISION.os, "name", "nt"):
                with self.assertRaises(PROVISION.Failure) as caught:
                    PROVISION.target_paths(profile_resolver=lambda: profile,
                                           operator_resolver=lambda: "someone-else",
                                           reparse=lambda _: False)
        self.assertEqual(caught.exception.code, "WRONG_WINDOWS_OPERATOR")

    def test_collision_refuses_either_final_name(self):
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp); private = root / "id_ed25519"; public = root / "id_ed25519.pub"
            for target in (private, public):
                target.write_text("occupied", encoding="ascii")
                with self.assertRaises(PROVISION.Failure) as caught: PROVISION.collision_check(private, public)
                self.assertEqual(caught.exception.code, "TARGET_COLLISION")
                target.unlink()

    def test_keygen_identity_is_pinned(self):
        with tempfile.TemporaryDirectory() as temp:
            tool = pathlib.Path(temp) / "ssh-keygen.exe"; tool.write_bytes(b"wrong")
            with self.assertRaises(PROVISION.Failure) as caught:
                PROVISION.governed_keygen(resolver=lambda _: tool)
        self.assertEqual(caught.exception.code, "SSH_KEYGEN_IDENTITY_MISMATCH")

    def test_public_parser_enforces_algorithm_comment_and_bounds(self):
        encoded = "AAAAC3NzaC1lZDI1NTE5AAAAIEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        self.assertEqual(PROVISION.parse_public(f"ssh-ed25519 {encoded} {PROVISION.KEY_COMMENT}")[0], "ssh-ed25519")
        for value in ("x" * 4097, "ssh-ed25519 invalid! comment", "ssh-ed25519 two-fields"):
            with self.assertRaises(PROVISION.Failure): PROVISION.parse_public(value)

    def test_pair_validation_and_fingerprint_are_sanitized(self):
        encoded = "AAAAC3NzaC1lZDI1NTE5AAAAIEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        public_text = f"ssh-ed25519 {encoded} {PROVISION.KEY_COMMENT}\n"
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp); private = root / "id_ed25519"; public = root / "id_ed25519.pub"
            private.write_text("opaque-private", encoding="ascii"); public.write_text(public_text, encoding="ascii")
            def runner(command, stage, **_):
                if "-y" in command: return Result(f"ssh-ed25519 {encoded}\n")
                return Result("256 SHA256:AbCdEf0123456789 comment (ED25519)\n")
            value = PROVISION.validate_pair(private, public, pathlib.Path("ssh-keygen"), runner=runner,
                                            reparse=lambda _: False, acl_validate=lambda *_: None)
        self.assertEqual(value, "SHA256:AbCdEf0123456789")

    def test_mismatch_and_wrong_comment_fail_closed(self):
        encoded = "AAAAC3NzaC1lZDI1NTE5AAAAIEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp); private = root / "id_ed25519"; public = root / "id_ed25519.pub"
            private.write_text("private", encoding="ascii")
            public.write_text(f"ssh-ed25519 {encoded} wrong\n", encoding="ascii")
            with self.assertRaises(PROVISION.Failure) as caught:
                PROVISION.validate_pair(private, public, pathlib.Path("x"), runner=lambda *_a, **_k: Result(),
                                        reparse=lambda _: False, acl_validate=lambda *_: None)
        self.assertEqual(caught.exception.code, "PUBLIC_KEY_COMMENT_MISMATCH")

    def test_hardening_applies_then_independently_rereads(self):
        calls = []
        PROVISION.harden(pathlib.Path("key"), "PRIVATE_KEY",
                         acl=lambda path, directory: calls.append(("apply", path, directory)),
                         acl_validate=lambda path, directory: calls.append(("validate", path, directory)))
        self.assertEqual([call[0] for call in calls], ["apply", "validate"])

    def test_staging_reparse_and_cleanup_broad_target_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            with self.assertRaises(PROVISION.Failure):
                PROVISION.create_private_child(root, PROVISION.STAGING_PREFIX, acl=lambda *_: None,
                                               reparse=lambda _: True)
            with self.assertRaises(PROVISION.Failure):
                PROVISION.safe_cleanup(root, root, reparse=lambda _: False)

    def test_cleanup_rejects_unexpected_directory_content(self):
        with tempfile.TemporaryDirectory() as temp:
            ssh = pathlib.Path(temp); stage = ssh / (PROVISION.STAGING_PREFIX + "abcdefgh"); stage.mkdir()
            (stage / "nested").mkdir()
            with self.assertRaises(PROVISION.Failure): PROVISION.safe_cleanup(stage, ssh, reparse=lambda _: False)

    def test_evidence_is_result_last_and_contains_no_key_material(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = pathlib.Path(temp); state = PROVISION.initial_state()
            state.update({key: "PASS" for key in ("PRIVATE_KEY_ACL", "PUBLIC_KEY_ACL", "PRIVATE_KEY_PUBLIC_MATCH")})
            PROVISION.write_evidence(directory, state, "SHA256:abc", pathlib.Path("C:/x/id_ed25519"),
                                     pathlib.Path("C:/x/id_ed25519.pub"), "PASS", "NONE", "COMPLETE", False,
                                     acl=lambda *_: None, acl_validate=lambda *_: None,
                                     reparse=lambda _: False)
            payload = (directory / "result.json").read_text(encoding="utf-8")
            self.assertIn('"public_key_fingerprint":"SHA256:abc"', payload)
            self.assertNotIn("private_key_material", payload)
            self.assertFalse((directory / ".result.tmp").exists())

    def test_terminal_is_bounded_and_does_not_emit_public_blob(self):
        lines = PROVISION.terminal_lines(PROVISION.initial_state(), "FAIL", "GENERATION_FAILED",
                                         "KEY_GENERATION", False, "SHA256:abc", None)
        joined = "\n".join(lines)
        self.assertIn("RESULT=FAIL", joined); self.assertNotIn("ssh-ed25519", joined)

    def test_publication_order_is_public_then_private_and_no_chaining(self):
        source = (TOOLS / "hioc-pe4-windows-ssh-identity-provision.py").read_text(encoding="utf-8")
        self.assertLess(source.index("replace(staged_public, public)"), source.index("replace(staged_private, private)"))
        self.assertNotIn("hioc-pe4-artifact-transfer.py", source)

    def _execute_fixture(self, root, *, replace_failure=0, confirmation_failure=False,
                         generation_failure=False, evidence_failure=False,
                         cleanup_failure=False, real_evidence=False,
                         staging_acl_failure=False):
        ssh = root / ".ssh"; ssh.mkdir(); private = ssh / "id_ed25519"; public = ssh / "id_ed25519.pub"
        evidence_root = root / "evidence"; evidence_root.mkdir()
        calls, validations = [], 0
        def runner(command, stage, **_):
            if stage == "KEY_GENERATION":
                if generation_failure: raise PROVISION.Failure("COMMAND_FAILED", stage)
                pathlib.Path(command[-1]).write_text("private", encoding="ascii")
                pathlib.Path(command[-1] + ".pub").write_text("public", encoding="ascii")
            return Result()
        def validate(*_args, **_kwargs):
            nonlocal validations
            validations += 1
            if confirmation_failure and validations == 2:
                raise PROVISION.Failure("FINAL_IDENTITY_CONFIRMATION_FAILED", "FINAL_CONFIRMATION", True)
            return "SHA256:fixture"
        def replace(source, target):
            calls.append(pathlib.Path(target).name)
            if replace_failure and len(calls) == replace_failure: raise OSError("simulated")
            os.replace(source, target)
        if real_evidence: evidence_writer = PROVISION.write_evidence
        else: evidence_writer = mock.Mock(side_effect=OSError("simulated evidence")) if evidence_failure else mock.Mock()
        def acl(path, directory):
            if staging_acl_failure and directory and pathlib.Path(path).name.startswith(PROVISION.STAGING_PREFIX):
                raise PROVISION.Failure("WORKSTATION_ACL_APPLICATION_FAILED", "WORKSTATION_ACL")
        real_cleanup = PROVISION.safe_cleanup
        cleanup = mock.Mock(side_effect=PROVISION.Failure("STAGING_CLEANUP_FAILED", "CLEANUP")) if cleanup_failure else real_cleanup
        with mock.patch.object(PROVISION, "verify_repository"), \
             mock.patch.object(PROVISION, "target_paths", return_value=(ssh, private, public)), \
             mock.patch.object(PROVISION, "governed_keygen", return_value=root / "ssh-keygen.exe"), \
             mock.patch.object(PROVISION, "evidence_root", return_value=evidence_root), \
             mock.patch.object(PROVISION, "validate_pair", side_effect=validate), \
             mock.patch.object(PROVISION, "harden"), \
             mock.patch.object(PROVISION, "safe_cleanup", side_effect=cleanup):
            lines, status = PROVISION.execute("a" * 40, runner=runner, acl=acl,
                acl_validate=lambda *_: None, reparse=lambda _: False,
                evidence_writer=evidence_writer, replace=replace)
        return "\n".join(lines), status, calls, private.exists(), public.exists(), evidence_writer

    def test_failure_before_publication_cleans_staging_and_preserves_primary(self):
        with tempfile.TemporaryDirectory() as temp:
            output, status, calls, private, public, _writer = self._execute_fixture(pathlib.Path(temp), generation_failure=True)
        self.assertEqual(status, 1); self.assertEqual(calls, [])
        self.assertFalse(private); self.assertFalse(public)
        self.assertIn("ERROR_CODE=GENERATION_FAILED", output)

    def test_public_only_partial_publication_is_preserved(self):
        with tempfile.TemporaryDirectory() as temp:
            output, status, calls, private, public, _writer = self._execute_fixture(pathlib.Path(temp), replace_failure=2)
        self.assertEqual(status, 1); self.assertEqual(calls[:2], ["id_ed25519.pub", "id_ed25519"])
        self.assertFalse(private); self.assertTrue(public)
        self.assertIn("PUBLIC_KEY_PUBLISHED=TRUE", output); self.assertIn("ROLLBACK_RECOMMENDED=TRUE", output)

    def test_post_private_confirmation_failure_preserves_pair(self):
        with tempfile.TemporaryDirectory() as temp:
            output, status, calls, private, public, _writer = self._execute_fixture(pathlib.Path(temp), confirmation_failure=True)
        self.assertEqual(status, 1); self.assertTrue(private); self.assertTrue(public)
        self.assertIn("PRIVATE_KEY_PUBLISHED=TRUE", output); self.assertIn("ROLLBACK_RECOMMENDED=TRUE", output)

    def test_evidence_publication_failure_is_bounded_and_preserves_pair(self):
        with tempfile.TemporaryDirectory() as temp:
            output, status, _calls, private, public, _writer = self._execute_fixture(pathlib.Path(temp), evidence_failure=True)
        self.assertEqual(status, 1); self.assertTrue(private); self.assertTrue(public)
        self.assertIn("ERROR_CODE=EVIDENCE_PUBLICATION_FAILED", output)
        self.assertIn("EVIDENCE_PUBLISHED=FALSE", output)

    def test_cleanup_secondary_failure_preserves_primary_failure(self):
        with tempfile.TemporaryDirectory() as temp:
            output, status, _calls, _private, _public, writer = self._execute_fixture(
                pathlib.Path(temp), generation_failure=True, cleanup_failure=True)
        self.assertEqual(status, 1)
        self.assertIn("ERROR_CODE=GENERATION_FAILED", output)
        self.assertIn("STAGING_CLEANUP=FAILED", output)
        self.assertEqual(writer.call_args.args[1]["STAGING_CLEANUP"], "FAILED")

    def test_child_created_acl_failure_retains_exact_identity_for_cleanup(self):
        with tempfile.TemporaryDirectory() as temp:
            parent = pathlib.Path(temp); unrelated = parent / "unrelated"; unrelated.mkdir()
            known = []
            with self.assertRaises(RuntimeError):
                PROVISION.create_private_child(parent, PROVISION.STAGING_PREFIX,
                    acl=lambda *_: (_ for _ in ()).throw(RuntimeError("acl")),
                    reparse=lambda _: False, created=known.append)
            self.assertEqual(len(known), 1); self.assertTrue(known[0].exists())
            PROVISION.safe_cleanup(known[0], parent, PROVISION.STAGING_PREFIX, reparse=lambda _: False)
            self.assertFalse(known[0].exists()); self.assertTrue(unrelated.exists())

    def test_failure_evidence_observes_cleanup_pass_before_construction(self):
        with tempfile.TemporaryDirectory() as temp:
            output, status, _calls, _private, _public, writer = self._execute_fixture(
                pathlib.Path(temp), generation_failure=True)
        self.assertEqual(status, 1); self.assertIn("STAGING_CLEANUP=PASS", output)
        self.assertEqual(writer.call_args.args[1]["STAGING_CLEANUP"], "PASS")

    def test_staging_acl_failure_retains_primary_and_cleans_known_child_before_evidence(self):
        with tempfile.TemporaryDirectory() as temp:
            output, status, _calls, _private, _public, writer = self._execute_fixture(
                pathlib.Path(temp), staging_acl_failure=True)
        self.assertEqual(status, 1)
        self.assertIn("ERROR_CODE=WORKSTATION_ACL_APPLICATION_FAILED", output)
        self.assertIn("STAGING_CLEANUP=PASS", output)
        self.assertEqual(writer.call_args.args[1]["STAGING_CLEANUP"], "PASS")

    def _evidence_fixture(self, replace, acl_validate=lambda *_: None):
        temp = tempfile.TemporaryDirectory(); directory = pathlib.Path(temp.name)
        state = PROVISION.initial_state(); state["STAGING_CLEANUP"] = "PASS"
        try:
            PROVISION.write_evidence(directory, state, "SHA256:abc", pathlib.Path("C:/x/id_ed25519"),
                pathlib.Path("C:/x/id_ed25519.pub"), "PASS", "NONE", "COMPLETE", False,
                acl=lambda *_: None, acl_validate=acl_validate, reparse=lambda _: False,
                replace=replace)
            error = None
        except Exception as exc: error = exc
        return temp, directory, error

    def test_result_rename_success_final_confirmation_failure_is_not_accepted(self):
        calls = 0
        def validate(*_):
            nonlocal calls; calls += 1
            if calls == 2: raise RuntimeError("final acl")
        temp, directory, error = self._evidence_fixture(os.replace, validate)
        try:
            self.assertIsInstance(error, PROVISION.Failure)
            self.assertEqual(error.code, "EVIDENCE_ACL_INVALID")
            self.assertTrue((directory / "result.json").exists())
        finally: temp.cleanup()

    def test_rename_error_with_exact_final_result_reconciles_success(self):
        def replace_then_error(source, target): os.replace(source, target); raise OSError("uncertain")
        temp, directory, error = self._evidence_fixture(replace_then_error)
        try:
            self.assertIsNone(error); self.assertTrue((directory / "result.json").is_file())
        finally: temp.cleanup()

    def test_rename_error_with_wrong_final_result_fails_without_overwrite(self):
        def wrong_then_error(source, target): pathlib.Path(target).write_text("wrong", encoding="ascii"); raise OSError("uncertain")
        temp, directory, error = self._evidence_fixture(wrong_then_error)
        try:
            self.assertIsInstance(error, PROVISION.Failure)
            self.assertEqual(error.code, "EVIDENCE_RENAME_UNCERTAIN")
            self.assertEqual((directory / "result.json").read_text(encoding="ascii"), "wrong")
        finally: temp.cleanup()

    def test_pass_evidence_requires_full_confirmation_and_agrees_with_terminal(self):
        temp, directory, error = self._evidence_fixture(os.replace)
        try:
            self.assertIsNone(error)
            payload = __import__("json").loads((directory / "result.json").read_text(encoding="utf-8"))
            self.assertEqual(payload["evidence_published"], "TRUE")
            self.assertEqual(payload["staging_cleanup"], "PASS")
            state = PROVISION.initial_state(); state["EVIDENCE_PUBLISHED"] = "TRUE"; state["STAGING_CLEANUP"] = "PASS"
            terminal = "\n".join(PROVISION.terminal_lines(state, "PASS", "NONE", "COMPLETE", False, "SHA256:abc", directory))
            self.assertIn("EVIDENCE_PUBLISHED=TRUE", terminal); self.assertIn("STAGING_CLEANUP=PASS", terminal)
        finally: temp.cleanup()

    @staticmethod
    def _terminal_map(output):
        return dict(line.split("=", 1) for line in output.splitlines() if "=" in line)

    def _assert_persistent_terminal_agreement(self, output):
        terminal = self._terminal_map(output)
        payload = __import__("json").loads((pathlib.Path(terminal["EVIDENCE_DIR"]) / "result.json").read_text(encoding="utf-8"))
        for key in PROVISION.STATE_KEYS:
            self.assertEqual(payload[key.lower()], terminal[key])
        for terminal_key, payload_key in (("RESULT", "result"), ("ERROR_CODE", "error_code"),
                                           ("FAILURE_STAGE", "failure_stage")):
            self.assertEqual(payload[payload_key], terminal[terminal_key])
        self.assertEqual(payload["rollback_recommended"], terminal["ROLLBACK_RECOMMENDED"] == "TRUE")

    def test_confirmed_pass_terminal_and_persistent_evidence_agree_all_fields(self):
        with tempfile.TemporaryDirectory() as temp:
            output, status, _calls, private, public, _writer = self._execute_fixture(
                pathlib.Path(temp), real_evidence=True)
            self.assertEqual(status, 0); self.assertTrue(private); self.assertTrue(public)
            self._assert_persistent_terminal_agreement(output)

    def test_confirmed_failure_terminal_and_persistent_evidence_agree_all_fields(self):
        with tempfile.TemporaryDirectory() as temp:
            output, status, _calls, private, public, _writer = self._execute_fixture(
                pathlib.Path(temp), generation_failure=True, real_evidence=True)
            self.assertEqual(status, 1); self.assertFalse(private); self.assertFalse(public)
            self._assert_persistent_terminal_agreement(output)

    def test_bounded_runner_rejects_output_and_duration(self):
        with self.assertRaises(PROVISION.Failure) as output:
            PROVISION.run_bounded([os.sys.executable, "-c", "print('x'*5000)"], "TEST", timeout=5, max_output=100)
        self.assertEqual(output.exception.code, "COMMAND_OUTPUT_TOO_LARGE")
        with self.assertRaises(PROVISION.Failure) as duration:
            PROVISION.run_bounded([os.sys.executable, "-c", "import time;time.sleep(2)"], "TEST", timeout=1)
        self.assertEqual(duration.exception.code, "COMMAND_TIMEOUT")

    @unittest.skipUnless(os.name == "nt", "Windows ACL integration")
    def test_real_disposable_acl_python_to_child_process_boundary(self):
        with tempfile.TemporaryDirectory() as temp:
            path = pathlib.Path(temp) / "fixture"; path.write_text("public-fixture", encoding="ascii")
            PROVISION.secure_workstation_path(path, False)
            PROVISION.validate_workstation_path_acl(path, False)


if __name__ == "__main__": unittest.main()
