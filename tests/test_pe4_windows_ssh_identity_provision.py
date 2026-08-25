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
                                     acl=lambda *_: None)
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
                         cleanup_failure=False):
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
        evidence_writer = mock.Mock(side_effect=OSError("simulated evidence")) if evidence_failure else mock.Mock()
        real_cleanup = PROVISION.safe_cleanup
        cleanup = mock.Mock(side_effect=PROVISION.Failure("STAGING_CLEANUP_FAILED", "CLEANUP")) if cleanup_failure else real_cleanup
        with mock.patch.object(PROVISION, "verify_repository"), \
             mock.patch.object(PROVISION, "target_paths", return_value=(ssh, private, public)), \
             mock.patch.object(PROVISION, "governed_keygen", return_value=root / "ssh-keygen.exe"), \
             mock.patch.object(PROVISION, "evidence_root", return_value=evidence_root), \
             mock.patch.object(PROVISION, "validate_pair", side_effect=validate), \
             mock.patch.object(PROVISION, "harden"), \
             mock.patch.object(PROVISION, "safe_cleanup", side_effect=cleanup):
            lines, status = PROVISION.execute("a" * 40, runner=runner, acl=lambda *_: None,
                acl_validate=lambda *_: None, reparse=lambda _: False,
                evidence_writer=evidence_writer, replace=replace)
        return "\n".join(lines), status, calls, private.exists(), public.exists()

    def test_failure_before_publication_cleans_staging_and_preserves_primary(self):
        with tempfile.TemporaryDirectory() as temp:
            output, status, calls, private, public = self._execute_fixture(pathlib.Path(temp), generation_failure=True)
        self.assertEqual(status, 1); self.assertEqual(calls, [])
        self.assertFalse(private); self.assertFalse(public)
        self.assertIn("ERROR_CODE=GENERATION_FAILED", output)

    def test_public_only_partial_publication_is_preserved(self):
        with tempfile.TemporaryDirectory() as temp:
            output, status, calls, private, public = self._execute_fixture(pathlib.Path(temp), replace_failure=2)
        self.assertEqual(status, 1); self.assertEqual(calls[:2], ["id_ed25519.pub", "id_ed25519"])
        self.assertFalse(private); self.assertTrue(public)
        self.assertIn("PUBLIC_KEY_PUBLISHED=TRUE", output); self.assertIn("ROLLBACK_RECOMMENDED=TRUE", output)

    def test_post_private_confirmation_failure_preserves_pair(self):
        with tempfile.TemporaryDirectory() as temp:
            output, status, calls, private, public = self._execute_fixture(pathlib.Path(temp), confirmation_failure=True)
        self.assertEqual(status, 1); self.assertTrue(private); self.assertTrue(public)
        self.assertIn("PRIVATE_KEY_PUBLISHED=TRUE", output); self.assertIn("ROLLBACK_RECOMMENDED=TRUE", output)

    def test_evidence_publication_failure_is_bounded_and_preserves_pair(self):
        with tempfile.TemporaryDirectory() as temp:
            output, status, _calls, private, public = self._execute_fixture(pathlib.Path(temp), evidence_failure=True)
        self.assertEqual(status, 1); self.assertTrue(private); self.assertTrue(public)
        self.assertIn("ERROR_CODE=EVIDENCE_PUBLICATION_FAILED", output)
        self.assertIn("EVIDENCE_PUBLISHED=FALSE", output)

    def test_cleanup_secondary_failure_preserves_primary_failure(self):
        with tempfile.TemporaryDirectory() as temp:
            output, status, _calls, _private, _public = self._execute_fixture(
                pathlib.Path(temp), generation_failure=True, cleanup_failure=True)
        self.assertEqual(status, 1)
        self.assertIn("ERROR_CODE=GENERATION_FAILED", output)
        self.assertIn("STAGING_CLEANUP=FAILED", output)

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
