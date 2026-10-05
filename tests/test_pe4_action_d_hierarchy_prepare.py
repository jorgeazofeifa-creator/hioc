import importlib.util
import contextlib
import io
from unittest import mock
import os
import pathlib
import sys
import tempfile
import types
import stat
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))
SPEC = importlib.util.spec_from_file_location("pe4_d_prep", TOOLS / "hioc-pe4-runtime-hierarchy-prepare.py")
PREP = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PREP)
SOURCE = (TOOLS / "hioc-pe4-runtime-hierarchy-prepare.py").read_text(encoding="utf-8")


class ActionDHierarchyPreparationContractTests(unittest.TestCase):
    def test_stable_identity_and_action_separation(self):
        self.assertEqual(PREP.ACTION, "PE-4.0B.2a-D-PREP")
        self.assertIn("--governance-commit", SOURCE)
        for forbidden in ("hioc-pe4-runtime-construct.py", "hioc-pe4-dependency-validate.py",
                          "hioc-pe4-runtime-publish.py", "pip", "venv", "ACTIVE_POINTER"):
            self.assertNotIn(forbidden, SOURCE)

    def test_explicit_device_policy_preserves_runtime_mount_compatibility(self):
        self.assertIn("require_same_device=False", SOURCE)
        self.assertIn('"pe4", 0o750, stage)', SOURCE)
        self.assertIn('"environments", 0o750, stage)', SOURCE)

    def test_bounded_evidence_and_terminal_contract(self):
        for marker in ("RUNTIME_PARENT_STATE", "RUNTIME_ROOT_STATE", "ENVIRONMENTS_STATE",
                       "CREATED_RUNTIME_PARENT", "CREATED_RUNTIME_ROOT", "CREATED_ENVIRONMENTS",
                       "CLEANUP_STATE", "EVIDENCE_STATE", "DIAGNOSTIC_STAGE",
                       "DIAGNOSTIC_OPERATION", "EXCEPTION_CLASS", "ERRNO", "STOP_REQUIRED=TRUE"):
            self.assertIn(marker, SOURCE)
        self.assertIn("EVIDENCE_DOCUMENT_TOO_LARGE", SOURCE)
        self.assertEqual(PREP.EVIDENCE_MAX_BYTES, 4096)
        self.assertIn('"result.json"', SOURCE)

    def test_named_child_helper_is_fixed_name_descriptor_relative_and_no_race_adoption(self):
        common_source = (TOOLS / "hioc_pe4_runtime_common.py").read_text(encoding="utf-8")
        self.assertIn("def ensure_owned_named_child", common_source)
        self.assertIn("os.mkdir(name, mode=mode, dir_fd=parent.fd)", common_source)
        self.assertIn("NAMED_CHILD_CREATION_COLLISION", common_source)
        self.assertIn("os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent.fd", common_source)
        self.assertIn("require_same_device: bool = True", common_source)

    def test_finite_diagnostic_enums_do_not_serialize_exception_messages(self):
        self.assertIn("DIAGNOSTIC_STAGES = frozenset", SOURCE)
        self.assertIn("DIAGNOSTIC_OPERATIONS = frozenset", SOURCE)
        self.assertNotIn("str(exc)", SOURCE)
        self.assertNotIn("traceback", SOURCE)

    def test_main_representative_evidence_failures_preserve_diagnostics(self):
        cases = ("GOVERNED_ROOT_FAILURE", "RAW_CHILD_OSERROR", "CONFIRMATION_FAILURE")
        completed = []
        for fault in cases:
            with self.subTest(fault=fault):
                names = ("anchor", "runtime", "root", "environments", "evidence_root", "evidence")
                paths = ("/home/jazofv1/hioc", "/home/jazofv1/hioc/runtime",
                         "/home/jazofv1/hioc/runtime/pe4", "/home/jazofv1/hioc/runtime/pe4/environments",
                         "/tmp", "/tmp/hioc-pe4-runtime-hierarchy-prepare-AbCd1234")
                directories = {name: PREP.OwnedDirectory(pathlib.Path(path), 40+i, 11, 140+i, 3, 4, 0o750)
                               for i, (name, path) in enumerate(zip(names, paths))}
                primary = (PREP.Failure("TEMP_ROOT_INVALID", "EVIDENCE_PUBLICATION") if fault == cases[0] else
                           OSError(5, "RAW_EVIDENCE_CHILD_FAILURE") if fault == cases[1] else
                           PREP.Failure("EVIDENCE_CONFIRMATION_FAILED", "EVIDENCE_PUBLICATION"))
                root_helper = mock.Mock(side_effect=primary) if fault == cases[0] else mock.Mock(return_value=directories["evidence_root"])
                child_helper = mock.Mock(side_effect=primary) if fault == cases[1] else mock.Mock(return_value=directories["evidence"])
                publisher = mock.Mock(side_effect=primary) if fault == cases[2] else mock.Mock()
                output = io.StringIO()
                with mock.patch.multiple(PREP, verify_pi3=mock.Mock(), verify_repository=mock.Mock(),
                         open_trusted_owned_path_bound=mock.Mock(return_value=directories["anchor"]),
                         revalidate_path_bound_directory=mock.Mock(),
                         ensure_owned_named_child=mock.Mock(side_effect=[(directories[n], False) for n in ("runtime", "root", "environments")]),
                         open_tmp_root=root_helper, create_owned_child=child_helper, publish_owned_json=publisher), \
                     mock.patch.object(PREP.os, "close") as close, \
                     mock.patch.object(PREP.os, "umask", return_value=0o077) as masks, \
                     mock.patch.object(sys, "argv", ["d-prep", "--governance-commit", "0"*40]), \
                     contextlib.redirect_stdout(output):
                    self.assertEqual(PREP.main(), 1)
                    root_helper.assert_called_once_with("EVIDENCE_PUBLICATION")
                    if fault == cases[0]:
                        child_helper.assert_not_called()
                    else:
                        child_helper.assert_called_once_with(directories["evidence_root"], PREP.EVIDENCE_PREFIX,
                                                            0o700, "EVIDENCE_PUBLICATION")
                    if fault == cases[2]:
                        publisher.assert_called_once()
                    else:
                        publisher.assert_not_called()
                    PREP.revalidate_path_bound_directory.assert_any_call(directories["environments"], "EVIDENCE_PUBLICATION")
                    acquired = list(names[:4]) + ([] if fault == cases[0] else ["evidence_root"]) + (["evidence"] if fault == cases[2] else [])
                    self.assertEqual(close.call_args_list, [mock.call(40 + names.index(n)) for n in reversed(acquired)])
                    for name in acquired:
                        self.assertEqual(directories[name].fd, -1)
                    self.assertEqual(masks.call_args_list, [mock.call(0o027), mock.call(0o077)])
                text = output.getvalue()
                lines = text.splitlines()
                self.assertTrue(all("=" in line for line in lines))
                fields = dict(line.split("=", 1) for line in lines)
                expected = {
                    "RUNTIME_PARENT_STATE": "PREEXISTING_COMPLIANT", "RUNTIME_ROOT_STATE": "PREEXISTING_COMPLIANT",
                    "ENVIRONMENTS_STATE": "PREEXISTING_COMPLIANT", "CREATED_RUNTIME_PARENT": "FALSE",
                    "CREATED_RUNTIME_ROOT": "FALSE", "CREATED_ENVIRONMENTS": "FALSE",
                    "CLEANUP_STATE": "NOT_APPLICABLE", "EVIDENCE_STATE": "UNCONFIRMED",
                    "RESULT": "FAIL", "ERROR_CODE": "UNEXPECTED_ERROR" if fault == cases[1] else primary.code,
                    "FAILURE_STAGE": "UNEXPECTED" if fault == cases[1] else "EVIDENCE_PUBLICATION",
                    "ROLLBACK_RECOMMENDED": "FALSE", "DIAGNOSTIC_STAGE": "EVIDENCE_PUBLICATION",
                    "DIAGNOSTIC_OPERATION": "PUBLISH_EVIDENCE",
                    "EXCEPTION_CLASS": "OS_ERROR" if fault == cases[1] else "GOVERNED_FAILURE",
                    "ERRNO": "5" if fault == cases[1] else "NONE", "STOP_REQUIRED": "TRUE"}
                self.assertEqual(fields, expected)
                self.assertEqual(len(lines), len(expected))
                self.assertEqual(lines.count("RESULT=FAIL"), 1)
                self.assertEqual(lines.count("RESULT=PASS"), 0)
                self.assertEqual(text.count("EVIDENCE_DIR="), 0)
                self.assertNotIn("EVIDENCE_STATE=CONFIRMED", lines)
                self.assertNotIn("RAW_EVIDENCE_CHILD_FAILURE", text)
                self.assertNotIn(str(directories["evidence"].path), text)
                completed.append(fault)
        self.assertEqual(completed, list(cases))

    def test_unconfirmed_evidence_is_never_disclosed_by_main(self):
        class Directory:
            def __init__(self, path): self.path, self.mode = pathlib.Path(path), 0o750
            def close(self): pass
        anchor = Directory("/home/jazofv1/hioc")
        evidence = Directory("/tmp/hioc-pe4-runtime-hierarchy-prepare-AbCd1234")
        with mock.patch.multiple(PREP, verify_pi3=mock.Mock(), verify_repository=mock.Mock(),
                                 open_trusted_owned_path_bound=mock.Mock(return_value=anchor),
                                 revalidate_path_bound_directory=mock.Mock(),
                                 ensure_owned_named_child=mock.Mock(side_effect=[(anchor, False)] * 3),
                                 open_tmp_root=mock.Mock(return_value=anchor),
                                 create_owned_child=mock.Mock(return_value=evidence),
                                 publish_owned_json=mock.Mock(side_effect=PREP.Failure("EVIDENCE_PUBLICATION_FAILED", "EVIDENCE_PUBLICATION"))):
            with mock.patch.object(sys, "argv", ["d-prep", "--governance-commit", "0" * 40]):
                output = io.StringIO()
                with contextlib.redirect_stdout(output): self.assertEqual(PREP.main(), 1)
        value = output.getvalue()
        self.assertIn("EVIDENCE_STATE=UNCONFIRMED", value)
        self.assertNotIn("EVIDENCE_DIR=", value)
        self.assertIn("STOP_REQUIRED=TRUE", value)

    def test_confirmed_evidence_is_disclosed_once(self):
        class Directory:
            def __init__(self, path): self.path, self.mode = pathlib.Path(path), 0o750
            def close(self): pass
        anchor = Directory("/home/jazofv1/hioc")
        evidence = Directory("/tmp/hioc-pe4-runtime-hierarchy-prepare-AbCd1234")
        with mock.patch.multiple(PREP, verify_pi3=mock.Mock(), verify_repository=mock.Mock(),
                                 open_trusted_owned_path_bound=mock.Mock(return_value=anchor),
                                 revalidate_path_bound_directory=mock.Mock(),
                                 ensure_owned_named_child=mock.Mock(side_effect=[(anchor, False)] * 3),
                                 open_tmp_root=mock.Mock(return_value=anchor),
                                 create_owned_child=mock.Mock(return_value=evidence), publish_owned_json=mock.Mock(return_value="0" * 64)):
            with mock.patch.object(sys, "argv", ["d-prep", "--governance-commit", "0" * 40]):
                output = io.StringIO()
                with contextlib.redirect_stdout(output): self.assertEqual(PREP.main(), 0)
        value = output.getvalue()
        self.assertIn("EVIDENCE_STATE=CONFIRMED", value)
        self.assertEqual(value.count("EVIDENCE_DIR="), 1)

    def test_created_but_unconfirmed_state_is_reported(self):
        class Directory:
            def __init__(self, path): self.path, self.mode = pathlib.Path(path), 0o750
            def close(self): pass
        anchor = Directory("/home/jazofv1/hioc")
        failure = PREP.NamedChildFailure("NAMED_CHILD_CONFIRMATION_FAILED", "RUNTIME_PARENT", True)
        with mock.patch.multiple(PREP, verify_pi3=mock.Mock(), verify_repository=mock.Mock(),
                                 open_trusted_owned_path_bound=mock.Mock(return_value=anchor),
                                 revalidate_path_bound_directory=mock.Mock(),
                                 ensure_owned_named_child=mock.Mock(side_effect=failure)):
            with mock.patch.object(sys, "argv", ["d-prep", "--governance-commit", "0" * 40]):
                output = io.StringIO()
                with contextlib.redirect_stdout(output): self.assertEqual(PREP.main(), 1)
        self.assertIn("RUNTIME_PARENT_STATE=CREATION_OCCURRED_BUT_FINAL_STATE_UNCONFIRMED", output.getvalue())

    def test_pe4_creation_uncertainty_preserves_runtime_state(self):
        class Directory:
            def __init__(self, path): self.path = pathlib.Path(path)
            def close(self): pass
        anchor = Directory("/home/jazofv1/hioc")
        failure = PREP.NamedChildFailure("NAMED_CHILD_CONFIRMATION_FAILED", "RUNTIME_ROOT", True)
        with mock.patch.multiple(PREP, verify_pi3=mock.Mock(), verify_repository=mock.Mock(),
                                 open_trusted_owned_path_bound=mock.Mock(return_value=anchor),
                                 revalidate_path_bound_directory=mock.Mock(),
                                 ensure_owned_named_child=mock.Mock(side_effect=[(anchor, False), failure])):
            with mock.patch.object(sys, "argv", ["d-prep", "--governance-commit", "0" * 40]):
                output = io.StringIO()
                with contextlib.redirect_stdout(output): self.assertEqual(PREP.main(), 1)
        value = output.getvalue()
        self.assertIn("RUNTIME_PARENT_STATE=PREEXISTING_COMPLIANT", value)
        self.assertIn("RUNTIME_ROOT_STATE=CREATION_OCCURRED_BUT_FINAL_STATE_UNCONFIRMED", value)
        self.assertIn("ENVIRONMENTS_STATE=NOT_REACHED", value)

    def test_environments_creation_uncertainty_preserves_parent_states(self):
        class Directory:
            def __init__(self, path): self.path = pathlib.Path(path)
            def close(self): pass
        anchor = Directory("/home/jazofv1/hioc")
        failure = PREP.NamedChildFailure("NAMED_CHILD_CONFIRMATION_FAILED", "ENVIRONMENTS", True)
        with mock.patch.multiple(PREP, verify_pi3=mock.Mock(), verify_repository=mock.Mock(),
                                 open_trusted_owned_path_bound=mock.Mock(return_value=anchor),
                                 revalidate_path_bound_directory=mock.Mock(),
                                 ensure_owned_named_child=mock.Mock(side_effect=[(anchor, False), (anchor, False), failure])):
            with mock.patch.object(sys, "argv", ["d-prep", "--governance-commit", "0" * 40]):
                output = io.StringIO()
                with contextlib.redirect_stdout(output): self.assertEqual(PREP.main(), 1)
        value = output.getvalue()
        self.assertIn("RUNTIME_PARENT_STATE=PREEXISTING_COMPLIANT", value)
        self.assertIn("RUNTIME_ROOT_STATE=PREEXISTING_COMPLIANT", value)
        self.assertIn("ENVIRONMENTS_STATE=CREATION_OCCURRED_BUT_FINAL_STATE_UNCONFIRMED", value)

    def test_unexpected_evidence_failure_never_discloses_evidence(self):
        class Directory:
            def __init__(self, path): self.path, self.mode = pathlib.Path(path), 0o750
            def close(self): pass
        anchor = Directory("/home/jazofv1/hioc")
        evidence = Directory("/tmp/hioc-pe4-runtime-hierarchy-prepare-AbCd1234")
        with mock.patch.multiple(PREP, verify_pi3=mock.Mock(), verify_repository=mock.Mock(),
                                 open_trusted_owned_path_bound=mock.Mock(return_value=anchor),
                                 revalidate_path_bound_directory=mock.Mock(),
                                 ensure_owned_named_child=mock.Mock(side_effect=[(anchor, False)] * 3),
                                 open_tmp_root=mock.Mock(return_value=anchor),
                                 create_owned_child=mock.Mock(return_value=evidence),
                                 publish_owned_json=mock.Mock(side_effect=RuntimeError("SECRET_SHOULD_NEVER_APPEAR"))):
            with mock.patch.object(sys, "argv", ["d-prep", "--governance-commit", "0" * 40]):
                output = io.StringIO()
                with contextlib.redirect_stdout(output): self.assertEqual(PREP.main(), 1)
        value = output.getvalue()
        self.assertNotIn("EVIDENCE_DIR=", value)
        self.assertNotIn("SECRET_SHOULD_NEVER_APPEAR", value)
        self.assertIn("EXCEPTION_CLASS=OTHER", value)
        self.assertEqual(value.count("RESULT="), 1)
        self.assertIn("STOP_REQUIRED=TRUE", value)

    def test_named_child_collision_is_not_adopted_by_orchestration(self):
        class Directory:
            def __init__(self, path): self.path = pathlib.Path(path)
            def close(self): pass
        anchor = Directory("/home/jazofv1/hioc")
        collision = PREP.Failure("NAMED_CHILD_CREATION_COLLISION", "RUNTIME_PARENT")
        with mock.patch.multiple(PREP, verify_pi3=mock.Mock(), verify_repository=mock.Mock(),
                                 open_trusted_owned_path_bound=mock.Mock(return_value=anchor),
                                 revalidate_path_bound_directory=mock.Mock(),
                                 ensure_owned_named_child=mock.Mock(side_effect=collision)):
            with mock.patch.object(sys, "argv", ["d-prep", "--governance-commit", "0" * 40]):
                output = io.StringIO()
                with contextlib.redirect_stdout(output): self.assertEqual(PREP.main(), 1)
        value = output.getvalue()
        self.assertIn("ERROR_CODE=NAMED_CHILD_CREATION_COLLISION", value)
        self.assertIn("RUNTIME_PARENT_STATE=NOT_REACHED", value)
        self.assertIn("STOP_REQUIRED=TRUE", value)

    def test_initial_absence_then_mkdir_eexist_fails_closed_without_adoption(self):
        parent = PREP.OwnedDirectory(pathlib.Path("/anchor"), 99, 1, 2, 3, 4, 0o750)
        revalidate = mock.Mock()
        with mock.patch.object(PREP.os, "name", "posix"), mock.patch.object(PREP.os, "O_DIRECTORY", 0, create=True), mock.patch.object(PREP.os, "O_NOFOLLOW", 0, create=True), \
             mock.patch.dict(PREP.ensure_owned_named_child.__globals__, {"revalidate_owned_directory": revalidate}), \
             mock.patch.object(PREP.os, "stat", side_effect=FileNotFoundError()) as child_stat, \
             mock.patch.object(PREP.os, "mkdir", side_effect=FileExistsError()) as mkdir, mock.patch.object(PREP.os, "open") as child_open, \
             mock.patch.object(PREP.os, "unlink") as unlink, mock.patch.object(PREP.os, "rmdir") as rmdir:
            with self.assertRaises(PREP.Failure) as caught:
                PREP.ensure_owned_named_child(parent, "runtime", 0o750, "TEST", require_same_device=False)
        self.assertNotIsInstance(caught.exception, PREP.NamedChildFailure)
        self.assertEqual(caught.exception.code, "NAMED_CHILD_CREATION_COLLISION"); self.assertEqual(caught.exception.stage, "TEST")
        self.assertFalse(getattr(caught.exception, "creation_occurred", False))
        child_stat.assert_called_once_with("runtime", dir_fd=parent.fd, follow_symlinks=False)
        mkdir.assert_called_once_with("runtime", mode=0o750, dir_fd=parent.fd); child_open.assert_not_called()
        self.assertEqual(revalidate.call_count, 2); unlink.assert_not_called(); rmdir.assert_not_called()

    def test_initial_nofollow_inspection_failure_fails_closed_before_mkdir(self):
        parent = PREP.OwnedDirectory(pathlib.Path("/anchor"), 99, 1, 2, 3, 4, 0o750)
        inspection_failure = OSError(5, "SECRET_SHOULD_NEVER_APPEAR")
        revalidate = mock.Mock()
        with mock.patch.object(PREP.os, "name", "posix"), mock.patch.object(PREP.os, "O_DIRECTORY", 0, create=True), mock.patch.object(PREP.os, "O_NOFOLLOW", 0, create=True), \
             mock.patch.dict(PREP.ensure_owned_named_child.__globals__, {"revalidate_owned_directory": revalidate}), \
             mock.patch.object(PREP.os, "stat", side_effect=inspection_failure) as child_stat, mock.patch.object(PREP.os, "mkdir") as mkdir, \
             mock.patch.object(PREP.os, "open") as child_open, mock.patch.object(PREP.os, "unlink") as unlink, mock.patch.object(PREP.os, "rmdir") as rmdir:
            with self.assertRaises(PREP.Failure) as caught:
                PREP.ensure_owned_named_child(parent, "runtime", 0o750, "TEST", require_same_device=False)
        self.assertNotIsInstance(caught.exception, PREP.NamedChildFailure)
        self.assertEqual(caught.exception.code, "NAMED_CHILD_INSPECTION_FAILED"); self.assertEqual(caught.exception.stage, "TEST")
        self.assertFalse(getattr(caught.exception, "creation_occurred", False)); self.assertNotIn("SECRET_SHOULD_NEVER_APPEAR", str(caught.exception))
        self.assertEqual(revalidate.call_count, 1); child_stat.assert_called_once_with("runtime", dir_fd=parent.fd, follow_symlinks=False)
        mkdir.assert_not_called(); child_open.assert_not_called(); unlink.assert_not_called(); rmdir.assert_not_called()

    def test_post_mkdir_open_failure_carries_creation_uncertainty(self):
        """A real helper branch must not erase the successful mkdir effect."""
        parent = PREP.OwnedDirectory(pathlib.Path("/anchor"), 99, 1, 2, 3, 4, 0o750)
        missing = FileNotFoundError()
        with mock.patch.object(PREP.os, "name", "posix"), \
             mock.patch.object(PREP.os, "O_RDONLY", 0), mock.patch.object(PREP.os, "O_DIRECTORY", 0x100000, create=True), \
             mock.patch.object(PREP.os, "O_NOFOLLOW", 0x200000, create=True), \
             mock.patch.dict(PREP.ensure_owned_named_child.__globals__, {"revalidate_owned_directory": mock.Mock()}), \
             mock.patch.object(PREP.os, "stat", side_effect=missing), \
             mock.patch.object(PREP.os, "mkdir") as mkdir, \
             mock.patch.object(PREP.os, "open", side_effect=OSError("SECRET_SHOULD_NEVER_APPEAR")) as child_open, \
             mock.patch.object(PREP.os, "unlink") as unlink, mock.patch.object(PREP.os, "rmdir") as rmdir:
            with self.assertRaises(PREP.NamedChildFailure) as caught:
                PREP.ensure_owned_named_child(parent, "runtime", 0o750, "TEST",
                                               require_same_device=False)
            child_open.assert_called_once_with("runtime", PREP.os.O_RDONLY | PREP.os.O_DIRECTORY | PREP.os.O_NOFOLLOW, dir_fd=parent.fd)
        self.assertTrue(caught.exception.creation_occurred)
        self.assertEqual(caught.exception.code, "NAMED_CHILD_OPEN_FAILED")
        self.assertEqual(caught.exception.stage, "TEST")
        mkdir.assert_called_once()
        unlink.assert_not_called(); rmdir.assert_not_called()

    def test_post_mkdir_mode_failure_carries_creation_uncertainty(self):
        parent = PREP.OwnedDirectory(pathlib.Path("/anchor"), 99, 1, 2, 3, 4, 0o750)
        with mock.patch.object(PREP.os, "name", "posix"), \
             mock.patch.object(PREP.os, "O_RDONLY", 0), mock.patch.object(PREP.os, "O_DIRECTORY", 0x100000, create=True), \
             mock.patch.object(PREP.os, "O_NOFOLLOW", 0x200000, create=True), \
             mock.patch.dict(PREP.ensure_owned_named_child.__globals__, {"revalidate_owned_directory": mock.Mock()}), \
             mock.patch.object(PREP.os, "stat", side_effect=FileNotFoundError()), \
             mock.patch.object(PREP.os, "mkdir") as mkdir, \
             mock.patch.object(PREP.os, "open", return_value=101) as child_open, \
             mock.patch.object(PREP.os, "fchmod", side_effect=OSError("SECRET_SHOULD_NEVER_APPEAR"), create=True), \
             mock.patch.object(PREP.os, "unlink") as unlink, mock.patch.object(PREP.os, "rmdir") as rmdir, \
             mock.patch.object(PREP.os, "close"):
            with self.assertRaises(PREP.NamedChildFailure) as caught:
                PREP.ensure_owned_named_child(parent, "runtime", 0o750, "TEST",
                                               require_same_device=False)
            child_open.assert_called_once_with("runtime", PREP.os.O_RDONLY | PREP.os.O_DIRECTORY | PREP.os.O_NOFOLLOW, dir_fd=parent.fd)
        self.assertTrue(caught.exception.creation_occurred)
        self.assertEqual(caught.exception.stage, "TEST")
        self.assertEqual(caught.exception.code, "NAMED_CHILD_CONFIRMATION_FAILED")
        mkdir.assert_called_once()
        unlink.assert_not_called(); rmdir.assert_not_called()

    def _post_mkdir_getid_failure(self, failing_name):
        parent = PREP.OwnedDirectory(pathlib.Path("/anchor"), 99, 1, 2, 3, 4, 0o750)
        identity_failure = OSError(5, "SECRET_SHOULD_NEVER_APPEAR")
        getuid = mock.Mock(return_value=3)
        getgid = mock.Mock(return_value=4)
        revalidate = mock.Mock()
        (getuid if failing_name == "getuid" else getgid).side_effect = identity_failure
        with mock.patch.object(PREP.os, "name", "posix"), mock.patch.object(PREP.os, "O_RDONLY", 0), mock.patch.object(PREP.os, "O_DIRECTORY", 0x100000, create=True), mock.patch.object(PREP.os, "O_NOFOLLOW", 0x200000, create=True), \
             mock.patch.object(PREP.os, "getuid", getuid, create=True), mock.patch.object(PREP.os, "getgid", getgid, create=True), \
             mock.patch.dict(PREP.ensure_owned_named_child.__globals__, {"revalidate_owned_directory": revalidate, "_directory_token": mock.Mock(return_value=(1, 2, 3, 4, 0o750))}), \
             mock.patch.object(PREP.os, "stat", side_effect=FileNotFoundError()), mock.patch.object(PREP.os, "mkdir") as mkdir, mock.patch.object(PREP.os, "open", return_value=101) as child_open, \
             mock.patch.object(PREP.os, "fchmod", create=True) as fchmod, mock.patch.object(PREP.os, "unlink") as unlink, mock.patch.object(PREP.os, "rmdir") as rmdir, mock.patch.object(PREP.os, "close"):
            with self.assertRaises(PREP.NamedChildFailure) as caught:
                PREP.ensure_owned_named_child(parent, "runtime", 0o750, "TEST", require_same_device=False)
            child_open.assert_called_once_with("runtime", PREP.os.O_RDONLY | PREP.os.O_DIRECTORY | PREP.os.O_NOFOLLOW, dir_fd=parent.fd)
        mkdir.assert_called_once_with("runtime", mode=0o750, dir_fd=parent.fd); fchmod.assert_called_once_with(101, 0o750)
        self.assertEqual(revalidate.call_count, 2)
        self.assertTrue(caught.exception.creation_occurred); self.assertEqual(caught.exception.code, "NAMED_CHILD_CONFIRMATION_FAILED"); self.assertEqual(caught.exception.stage, "TEST")
        unlink.assert_not_called(); rmdir.assert_not_called()
        return getuid, getgid

    def test_post_mkdir_getuid_failure_carries_creation_uncertainty(self):
        getuid, getgid = self._post_mkdir_getid_failure("getuid")
        getuid.assert_called_once(); getgid.assert_not_called()

    def test_post_mkdir_getgid_failure_carries_creation_uncertainty(self):
        getuid, getgid = self._post_mkdir_getid_failure("getgid")
        getuid.assert_called_once(); getgid.assert_called_once()

    def test_post_mkdir_directory_token_failure_carries_creation_uncertainty(self):
        parent = PREP.OwnedDirectory(pathlib.Path("/anchor"), 99, 1, 2, 3, 4, 0o750)
        token_failure = OSError(5, "SECRET_SHOULD_NEVER_APPEAR")
        with mock.patch.object(PREP.os, "name", "posix"), \
             mock.patch.object(PREP.os, "O_RDONLY", 0), mock.patch.object(PREP.os, "O_DIRECTORY", 0x100000, create=True), \
             mock.patch.object(PREP.os, "O_NOFOLLOW", 0x200000, create=True), \
             mock.patch.dict(PREP.ensure_owned_named_child.__globals__, {
                 "revalidate_owned_directory": mock.Mock(), "_directory_token": mock.Mock(side_effect=token_failure)}), \
             mock.patch.object(PREP.os, "stat", side_effect=FileNotFoundError()), \
             mock.patch.object(PREP.os, "mkdir") as mkdir, \
             mock.patch.object(PREP.os, "open", return_value=101) as child_open, \
             mock.patch.object(PREP.os, "fchmod", create=True), \
             mock.patch.object(PREP.os, "unlink") as unlink, \
             mock.patch.object(PREP.os, "rmdir") as rmdir, \
             mock.patch.object(PREP.os, "close"):
            with self.assertRaises(PREP.NamedChildFailure) as caught:
                PREP.ensure_owned_named_child(parent, "runtime", 0o750, "TEST",
                                               require_same_device=False)
            child_open.assert_called_once_with("runtime", PREP.os.O_RDONLY | PREP.os.O_DIRECTORY | PREP.os.O_NOFOLLOW, dir_fd=parent.fd)
        mkdir.assert_called_once()
        self.assertTrue(caught.exception.creation_occurred)
        self.assertEqual(caught.exception.code, "NAMED_CHILD_CONFIRMATION_FAILED")
        self.assertEqual(caught.exception.stage, "TEST")
        unlink.assert_not_called(); rmdir.assert_not_called()

    def _post_mkdir_identity_mismatch(self, token):
        parent = PREP.OwnedDirectory(pathlib.Path("/anchor"), 99, 1, 2, 3, 4, 0o750)
        with mock.patch.object(PREP.os, "name", "posix"), \
             mock.patch.object(PREP.os, "O_RDONLY", 0), mock.patch.object(PREP.os, "O_DIRECTORY", 0x100000, create=True), \
             mock.patch.object(PREP.os, "O_NOFOLLOW", 0x200000, create=True), \
             mock.patch.object(PREP.os, "getuid", return_value=3, create=True), \
             mock.patch.object(PREP.os, "getgid", return_value=4, create=True), \
             mock.patch.dict(PREP.ensure_owned_named_child.__globals__, {
                 "revalidate_owned_directory": mock.Mock(), "_directory_token": mock.Mock(return_value=token)}), \
             mock.patch.object(PREP.os, "stat", side_effect=FileNotFoundError()), \
             mock.patch.object(PREP.os, "mkdir") as mkdir, \
             mock.patch.object(PREP.os, "open", return_value=101) as child_open, \
             mock.patch.object(PREP.os, "fchmod", create=True), \
             mock.patch.object(PREP.os, "unlink") as unlink, \
             mock.patch.object(PREP.os, "rmdir") as rmdir, \
             mock.patch.object(PREP.os, "close"):
            with self.assertRaises(PREP.NamedChildFailure) as caught:
                PREP.ensure_owned_named_child(parent, "runtime", 0o750, "TEST",
                                               require_same_device=False)
            child_open.assert_called_once_with("runtime", PREP.os.O_RDONLY | PREP.os.O_DIRECTORY | PREP.os.O_NOFOLLOW, dir_fd=parent.fd)
        mkdir.assert_called_once()
        unlink.assert_not_called(); rmdir.assert_not_called()
        self.assertTrue(caught.exception.creation_occurred)
        self.assertEqual(caught.exception.code, "NAMED_CHILD_IDENTITY_MISMATCH")
        self.assertEqual(caught.exception.stage, "TEST")

    def test_post_mkdir_uid_mismatch_carries_creation_uncertainty(self):
        self._post_mkdir_identity_mismatch((1, 2, 99, 4, 0o750))

    def test_post_mkdir_gid_mismatch_carries_creation_uncertainty(self):
        self._post_mkdir_identity_mismatch((1, 2, 3, 99, 0o750))

    def test_post_mkdir_mode_mismatch_carries_creation_uncertainty(self):
        self._post_mkdir_identity_mismatch((1, 2, 3, 4, 0o700))

    def test_post_mkdir_device_policy_rejection_carries_creation_uncertainty(self):
        parent = PREP.OwnedDirectory(pathlib.Path("/anchor"), 99, 1, 2, 3, 4, 0o750)
        with mock.patch.object(PREP.os, "name", "posix"), mock.patch.object(PREP.os, "O_RDONLY", 0), mock.patch.object(PREP.os, "O_DIRECTORY", 0x100000, create=True), \
             mock.patch.object(PREP.os, "O_NOFOLLOW", 0x200000, create=True), mock.patch.object(PREP.os, "getuid", return_value=3, create=True), \
             mock.patch.object(PREP.os, "getgid", return_value=4, create=True), \
             mock.patch.dict(PREP.ensure_owned_named_child.__globals__, {"revalidate_owned_directory": mock.Mock(), "_directory_token": mock.Mock(return_value=(99, 2, 3, 4, 0o750))}), \
             mock.patch.object(PREP.os, "stat", side_effect=FileNotFoundError()), mock.patch.object(PREP.os, "mkdir") as mkdir, \
             mock.patch.object(PREP.os, "open", return_value=101) as child_open, mock.patch.object(PREP.os, "fchmod", create=True), \
             mock.patch.object(PREP.os, "unlink") as unlink, \
             mock.patch.object(PREP.os, "rmdir") as rmdir, mock.patch.object(PREP.os, "close"):
            with self.assertRaises(PREP.NamedChildFailure) as caught: PREP.ensure_owned_named_child(parent, "runtime", 0o750, "TEST")
            child_open.assert_called_once_with("runtime", PREP.os.O_RDONLY | PREP.os.O_DIRECTORY | PREP.os.O_NOFOLLOW, dir_fd=parent.fd)
        mkdir.assert_called_once(); unlink.assert_not_called(); rmdir.assert_not_called()
        self.assertTrue(caught.exception.creation_occurred); self.assertEqual(caught.exception.code, "NAMED_CHILD_MOUNT_SUBSTITUTION")
        self.assertEqual(caught.exception.stage, "TEST")

    def test_post_mkdir_descriptor_name_mismatch_carries_creation_uncertainty(self):
        parent = PREP.OwnedDirectory(pathlib.Path("/anchor"), 99, 1, 2, 3, 4, 0o750)
        entry = types.SimpleNamespace(st_mode=stat.S_IFDIR | 0o750, st_dev=1, st_ino=99, st_uid=3, st_gid=4)
        with mock.patch.object(PREP.os, "name", "posix"), mock.patch.object(PREP.os, "O_RDONLY", 0), mock.patch.object(PREP.os, "O_DIRECTORY", 0x100000, create=True), \
             mock.patch.object(PREP.os, "O_NOFOLLOW", 0x200000, create=True), mock.patch.object(PREP.os, "getuid", return_value=3, create=True), \
             mock.patch.object(PREP.os, "getgid", return_value=4, create=True), \
             mock.patch.dict(PREP.ensure_owned_named_child.__globals__, {"revalidate_owned_directory": mock.Mock(), "_directory_token": mock.Mock(return_value=(1, 2, 3, 4, 0o750))}), \
             mock.patch.object(PREP.os, "stat", side_effect=[FileNotFoundError(), entry]), mock.patch.object(PREP.os, "mkdir") as mkdir, \
             mock.patch.object(PREP.os, "open", return_value=101) as child_open, mock.patch.object(PREP.os, "fchmod", create=True), \
             mock.patch.object(PREP.os, "unlink") as unlink, \
             mock.patch.object(PREP.os, "rmdir") as rmdir, mock.patch.object(PREP.os, "close"):
            with self.assertRaises(PREP.NamedChildFailure) as caught: PREP.ensure_owned_named_child(parent, "runtime", 0o750, "TEST", require_same_device=False)
            child_open.assert_called_once_with("runtime", PREP.os.O_RDONLY | PREP.os.O_DIRECTORY | PREP.os.O_NOFOLLOW, dir_fd=parent.fd)
        mkdir.assert_called_once(); unlink.assert_not_called(); rmdir.assert_not_called()
        self.assertTrue(caught.exception.creation_occurred); self.assertEqual(caught.exception.code, "NAMED_CHILD_IDENTITY_SUBSTITUTED")
        self.assertEqual(caught.exception.stage, "TEST")

    def _post_mkdir_revalidation_failure(self, target_index):
        parent = PREP.OwnedDirectory(pathlib.Path("/anchor"), 99, 1, 2, 3, 4, 0o750)
        entry = types.SimpleNamespace(st_mode=stat.S_IFDIR | 0o750, st_dev=1, st_ino=2, st_uid=3, st_gid=4)
        # Two validations precede mkdir; target_index addresses the four post-mkdir calls.
        revalidate = mock.Mock(side_effect=[None] * (target_index + 1) + [PREP.Failure("DIRECTORY_IDENTITY_LOST", "TEST")])
        with mock.patch.object(PREP.os, "name", "posix"), mock.patch.object(PREP.os, "O_RDONLY", 0), mock.patch.object(PREP.os, "O_DIRECTORY", 0x100000, create=True), mock.patch.object(PREP.os, "O_NOFOLLOW", 0x200000, create=True), \
             mock.patch.object(PREP.os, "getuid", return_value=3, create=True), mock.patch.object(PREP.os, "getgid", return_value=4, create=True), \
             mock.patch.dict(PREP.ensure_owned_named_child.__globals__, {"revalidate_owned_directory": revalidate, "_directory_token": mock.Mock(return_value=(1, 2, 3, 4, 0o750))}), \
             mock.patch.object(PREP.os, "stat", side_effect=[FileNotFoundError(), entry]), mock.patch.object(PREP.os, "mkdir") as mkdir, mock.patch.object(PREP.os, "open", return_value=101) as child_open, \
             mock.patch.object(PREP.os, "fchmod", create=True), mock.patch.object(PREP.os, "fsync") as fsync, mock.patch.object(PREP.os, "unlink") as unlink, mock.patch.object(PREP.os, "rmdir") as rmdir, mock.patch.object(PREP.os, "close"):
            with self.assertRaises(PREP.NamedChildFailure) as caught: PREP.ensure_owned_named_child(parent, "runtime", 0o750, "TEST", require_same_device=False)
            child_open.assert_called_once_with("runtime", PREP.os.O_RDONLY | PREP.os.O_DIRECTORY | PREP.os.O_NOFOLLOW, dir_fd=parent.fd)
        mkdir.assert_called_once(); unlink.assert_not_called(); rmdir.assert_not_called(); self.assertEqual(revalidate.call_count, target_index + 2)
        self.assertTrue(caught.exception.creation_occurred); self.assertEqual(caught.exception.code, "DIRECTORY_IDENTITY_LOST"); self.assertEqual(caught.exception.stage, "TEST")
        return fsync

    def test_post_mkdir_parent_revalidation_before_durability_failure_carries_creation_uncertainty(self):
        self.assertEqual(self._post_mkdir_revalidation_failure(1).call_count, 0)

    def test_post_mkdir_child_revalidation_before_durability_failure_carries_creation_uncertainty(self):
        self.assertEqual(self._post_mkdir_revalidation_failure(2).call_count, 0)

    def test_post_mkdir_final_parent_revalidation_failure_carries_creation_uncertainty(self):
        self.assertEqual(self._post_mkdir_revalidation_failure(3).call_count, 2)

    def test_post_mkdir_final_child_revalidation_failure_carries_creation_uncertainty(self):
        self.assertEqual(self._post_mkdir_revalidation_failure(4).call_count, 2)

    def _post_mkdir_fsync_failure(self, parent_fails):
        parent = PREP.OwnedDirectory(pathlib.Path("/anchor"), 99, 1, 2, 3, 4, 0o750)
        entry = types.SimpleNamespace(st_mode=stat.S_IFDIR | 0o750, st_dev=1, st_ino=2, st_uid=3, st_gid=4)
        fsync = mock.Mock(side_effect=[None, OSError(5, "SECRET_SHOULD_NEVER_APPEAR")] if parent_fails else OSError(5, "SECRET_SHOULD_NEVER_APPEAR"))
        with mock.patch.object(PREP.os, "name", "posix"), mock.patch.object(PREP.os, "O_RDONLY", 0), mock.patch.object(PREP.os, "O_DIRECTORY", 0x100000, create=True), mock.patch.object(PREP.os, "O_NOFOLLOW", 0x200000, create=True), \
             mock.patch.object(PREP.os, "getuid", return_value=3, create=True), mock.patch.object(PREP.os, "getgid", return_value=4, create=True), \
             mock.patch.dict(PREP.ensure_owned_named_child.__globals__, {"revalidate_owned_directory": mock.Mock(), "_directory_token": mock.Mock(return_value=(1, 2, 3, 4, 0o750))}), \
             mock.patch.object(PREP.os, "stat", side_effect=[FileNotFoundError(), entry]), mock.patch.object(PREP.os, "mkdir") as mkdir, mock.patch.object(PREP.os, "open", return_value=101) as child_open, \
             mock.patch.object(PREP.os, "fchmod", create=True), mock.patch.object(PREP.os, "fsync", fsync), mock.patch.object(PREP.os, "unlink") as unlink, mock.patch.object(PREP.os, "rmdir") as rmdir, mock.patch.object(PREP.os, "close"):
            with self.assertRaises(PREP.NamedChildFailure) as caught: PREP.ensure_owned_named_child(parent, "runtime", 0o750, "TEST", require_same_device=False)
            child_open.assert_called_once_with("runtime", PREP.os.O_RDONLY | PREP.os.O_DIRECTORY | PREP.os.O_NOFOLLOW, dir_fd=parent.fd)
        mkdir.assert_called_once(); unlink.assert_not_called(); rmdir.assert_not_called(); self.assertEqual(fsync.call_count, 2 if parent_fails else 1)
        self.assertTrue(caught.exception.creation_occurred); self.assertEqual(caught.exception.code, "NAMED_CHILD_CONFIRMATION_FAILED")
        self.assertEqual(caught.exception.stage, "TEST")

    def test_post_mkdir_child_fsync_failure_carries_creation_uncertainty(self):
        self._post_mkdir_fsync_failure(False)

    def test_post_mkdir_parent_fsync_failure_carries_creation_uncertainty(self):
        self._post_mkdir_fsync_failure(True)

    def test_invalid_basename_fails_before_creation(self):
        parent = PREP.OwnedDirectory(pathlib.Path("/anchor"), 99, 1, 2, 3, 4, 0o750)
        with mock.patch.object(PREP.os, "mkdir") as mkdir:
            with self.assertRaises(PREP.Failure) as caught: PREP.ensure_owned_named_child(parent, "../bad", 0o750, "TEST")
        mkdir.assert_not_called(); self.assertNotIsInstance(caught.exception, PREP.NamedChildFailure)

    def test_preexisting_noncompliant_child_does_not_claim_creation(self):
        parent = PREP.OwnedDirectory(pathlib.Path("/anchor"), 99, 1, 2, 3, 4, 0o750)
        existing = types.SimpleNamespace(st_mode=stat.S_IFDIR | 0o700, st_dev=1, st_ino=2, st_uid=3, st_gid=4)
        with mock.patch.object(PREP.os, "name", "posix"), mock.patch.object(PREP.os, "O_DIRECTORY", 0, create=True), mock.patch.object(PREP.os, "O_NOFOLLOW", 0, create=True), \
             mock.patch.object(PREP.os, "getuid", return_value=3, create=True), mock.patch.object(PREP.os, "getgid", return_value=4, create=True), \
             mock.patch.dict(PREP.ensure_owned_named_child.__globals__, {"revalidate_owned_directory": mock.Mock(), "_directory_token": mock.Mock(return_value=(1, 2, 3, 4, 0o700))}), \
             mock.patch.object(PREP.os, "stat", return_value=existing), mock.patch.object(PREP.os, "open", return_value=101), \
             mock.patch.object(PREP.os, "mkdir") as mkdir, mock.patch.object(PREP.os, "fchmod", create=True) as fchmod, \
             mock.patch.object(PREP.os, "chmod") as chmod, mock.patch.object(PREP.os, "chown", create=True) as chown, mock.patch.object(PREP.os, "fchown", create=True) as fchown, \
             mock.patch.object(PREP.os, "unlink") as unlink, mock.patch.object(PREP.os, "rmdir") as rmdir, mock.patch.object(PREP.os, "close"):
            with self.assertRaises(PREP.Failure) as caught: PREP.ensure_owned_named_child(parent, "runtime", 0o750, "TEST", require_same_device=False)
        self.assertNotIsInstance(caught.exception, PREP.NamedChildFailure)
        self.assertEqual(caught.exception.code, "NAMED_CHILD_IDENTITY_MISMATCH"); self.assertEqual(caught.exception.stage, "TEST")
        mkdir.assert_not_called(); fchmod.assert_not_called(); chmod.assert_not_called(); chown.assert_not_called(); fchown.assert_not_called(); unlink.assert_not_called(); rmdir.assert_not_called()

    def test_preexisting_nondirectory_child_fails_type_check_without_creation(self):
        parent = PREP.OwnedDirectory(pathlib.Path("/anchor"), 99, 1, 2, 3, 4, 0o750)
        regular_file = types.SimpleNamespace(st_mode=stat.S_IFREG | 0o750, st_dev=1, st_ino=2, st_uid=3, st_gid=4)
        with mock.patch.object(PREP.os, "name", "posix"), mock.patch.object(PREP.os, "O_DIRECTORY", 0, create=True), mock.patch.object(PREP.os, "O_NOFOLLOW", 0, create=True), \
             mock.patch.dict(PREP.ensure_owned_named_child.__globals__, {"revalidate_owned_directory": mock.Mock()}), \
             mock.patch.object(PREP.os, "stat", return_value=regular_file) as child_stat, mock.patch.object(PREP.os, "mkdir") as mkdir, mock.patch.object(PREP.os, "open") as child_open, \
             mock.patch.object(PREP.os, "chmod") as chmod, mock.patch.object(PREP.os, "fchmod", create=True) as fchmod, mock.patch.object(PREP.os, "chown", create=True) as chown, mock.patch.object(PREP.os, "fchown", create=True) as fchown, \
             mock.patch.object(PREP.os, "unlink") as unlink, mock.patch.object(PREP.os, "rmdir") as rmdir:
            with self.assertRaises(PREP.Failure) as caught:
                PREP.ensure_owned_named_child(parent, "runtime", 0o750, "TEST", require_same_device=False)
        self.assertNotIsInstance(caught.exception, PREP.NamedChildFailure)
        self.assertEqual(caught.exception.code, "NAMED_CHILD_TYPE_INVALID"); self.assertEqual(caught.exception.stage, "TEST")
        self.assertFalse(getattr(caught.exception, "creation_occurred", False)); child_stat.assert_called_once_with("runtime", dir_fd=parent.fd, follow_symlinks=False)
        mkdir.assert_not_called(); child_open.assert_not_called(); chmod.assert_not_called(); fchmod.assert_not_called(); chown.assert_not_called(); fchown.assert_not_called(); unlink.assert_not_called(); rmdir.assert_not_called()

    def test_preexisting_symlink_child_fails_closed_without_following(self):
        parent = PREP.OwnedDirectory(pathlib.Path("/anchor"), 99, 1, 2, 3, 4, 0o750)
        symlink = types.SimpleNamespace(st_mode=stat.S_IFLNK | 0o777, st_dev=1, st_ino=2, st_uid=3, st_gid=4)
        with mock.patch.object(PREP.os, "name", "posix"), mock.patch.object(PREP.os, "O_DIRECTORY", 0, create=True), mock.patch.object(PREP.os, "O_NOFOLLOW", 0, create=True), \
             mock.patch.dict(PREP.ensure_owned_named_child.__globals__, {"revalidate_owned_directory": mock.Mock()}), \
             mock.patch.object(PREP.os, "stat", return_value=symlink) as child_stat, mock.patch.object(PREP.os, "mkdir") as mkdir, mock.patch.object(PREP.os, "open") as child_open, \
             mock.patch.object(PREP.os, "chmod") as chmod, mock.patch.object(PREP.os, "fchmod", create=True) as fchmod, mock.patch.object(PREP.os, "chown", create=True) as chown, mock.patch.object(PREP.os, "fchown", create=True) as fchown, \
             mock.patch.object(PREP.os, "unlink") as unlink, mock.patch.object(PREP.os, "rmdir") as rmdir:
            with self.assertRaises(PREP.Failure) as caught:
                PREP.ensure_owned_named_child(parent, "runtime", 0o750, "TEST", require_same_device=False)
        self.assertNotIsInstance(caught.exception, PREP.NamedChildFailure)
        self.assertEqual(caught.exception.code, "NAMED_CHILD_TYPE_INVALID"); self.assertEqual(caught.exception.stage, "TEST")
        self.assertFalse(getattr(caught.exception, "creation_occurred", False)); child_stat.assert_called_once_with("runtime", dir_fd=parent.fd, follow_symlinks=False)
        mkdir.assert_not_called(); child_open.assert_not_called(); chmod.assert_not_called(); fchmod.assert_not_called(); chown.assert_not_called(); fchown.assert_not_called(); unlink.assert_not_called(); rmdir.assert_not_called()

    def test_preexisting_child_open_failure_does_not_claim_creation(self):
        parent = PREP.OwnedDirectory(pathlib.Path("/anchor"), 99, 1, 2, 3, 4, 0o750)
        existing = types.SimpleNamespace(st_mode=stat.S_IFDIR | 0o750, st_dev=1, st_ino=2, st_uid=3, st_gid=4)
        open_failure = OSError(5, "SECRET_SHOULD_NEVER_APPEAR")
        with mock.patch.object(PREP.os, "name", "posix"), mock.patch.object(PREP.os, "O_DIRECTORY", 0, create=True), mock.patch.object(PREP.os, "O_NOFOLLOW", 0, create=True), \
             mock.patch.dict(PREP.ensure_owned_named_child.__globals__, {"revalidate_owned_directory": mock.Mock()}), \
             mock.patch.object(PREP.os, "stat", return_value=existing) as child_stat, mock.patch.object(PREP.os, "mkdir") as mkdir, mock.patch.object(PREP.os, "open", side_effect=open_failure) as child_open, \
             mock.patch.object(PREP.os, "chmod") as chmod, mock.patch.object(PREP.os, "fchmod", create=True) as fchmod, mock.patch.object(PREP.os, "chown", create=True) as chown, mock.patch.object(PREP.os, "fchown", create=True) as fchown, \
             mock.patch.object(PREP.os, "unlink") as unlink, mock.patch.object(PREP.os, "rmdir") as rmdir:
            with self.assertRaises(PREP.Failure) as caught:
                PREP.ensure_owned_named_child(parent, "runtime", 0o750, "TEST", require_same_device=False)
        self.assertNotIsInstance(caught.exception, PREP.NamedChildFailure)
        self.assertEqual(caught.exception.code, "NAMED_CHILD_OPEN_FAILED"); self.assertEqual(caught.exception.stage, "TEST")
        self.assertFalse(getattr(caught.exception, "creation_occurred", False)); child_stat.assert_called_once_with("runtime", dir_fd=parent.fd, follow_symlinks=False)
        child_open.assert_called_once()
        mkdir.assert_not_called(); chmod.assert_not_called(); fchmod.assert_not_called(); chown.assert_not_called(); fchown.assert_not_called(); unlink.assert_not_called(); rmdir.assert_not_called()

    def test_preexisting_compliant_child_is_idempotently_accepted_without_creation(self):
        parent = PREP.OwnedDirectory(pathlib.Path("/anchor"), 99, 1, 2, 3, 4, 0o750)
        existing = types.SimpleNamespace(st_mode=stat.S_IFDIR | 0o750, st_dev=1, st_ino=2, st_uid=3, st_gid=4)
        revalidate = mock.Mock()
        token = mock.Mock(return_value=(1, 2, 3, 4, 0o750))
        with mock.patch.object(PREP.os, "name", "posix"), mock.patch.object(PREP.os, "O_DIRECTORY", 0, create=True), mock.patch.object(PREP.os, "O_NOFOLLOW", 0, create=True), \
             mock.patch.object(PREP.os, "getuid", return_value=3, create=True), mock.patch.object(PREP.os, "getgid", return_value=4, create=True), \
             mock.patch.dict(PREP.ensure_owned_named_child.__globals__, {"revalidate_owned_directory": revalidate, "_directory_token": token}), \
             mock.patch.object(PREP.os, "stat", return_value=existing) as child_stat, mock.patch.object(PREP.os, "open", return_value=101), \
             mock.patch.object(PREP.os, "mkdir") as mkdir, mock.patch.object(PREP.os, "fchmod", create=True) as fchmod, \
             mock.patch.object(PREP.os, "chmod") as chmod, mock.patch.object(PREP.os, "chown", create=True) as chown, mock.patch.object(PREP.os, "fchown", create=True) as fchown, \
             mock.patch.object(PREP.os, "unlink") as unlink, mock.patch.object(PREP.os, "rmdir") as rmdir, mock.patch.object(PREP.os, "close"):
            first, first_created = PREP.ensure_owned_named_child(parent, "runtime", 0o750, "TEST", require_same_device=False)
            second, second_created = PREP.ensure_owned_named_child(parent, "runtime", 0o750, "TEST", require_same_device=False)
        self.assertFalse(first_created); self.assertFalse(second_created)
        self.assertEqual((first.dev, first.ino, first.uid, first.gid, first.mode), (1, 2, 3, 4, 0o750))
        self.assertEqual((second.dev, second.ino, second.uid, second.gid, second.mode), (1, 2, 3, 4, 0o750))
        self.assertEqual(child_stat.call_count, 4); self.assertEqual(token.call_count, 2); self.assertEqual(revalidate.call_count, 6)
        mkdir.assert_not_called(); fchmod.assert_not_called(); chmod.assert_not_called(); chown.assert_not_called(); fchown.assert_not_called(); unlink.assert_not_called(); rmdir.assert_not_called()

    def test_pre_mkdir_parent_revalidation_failure_does_not_claim_creation(self):
        parent = PREP.OwnedDirectory(pathlib.Path("/anchor"), 99, 1, 2, 3, 4, 0o750)
        with mock.patch.object(PREP.os, "name", "posix"), mock.patch.object(PREP.os, "O_DIRECTORY", 0, create=True), mock.patch.object(PREP.os, "O_NOFOLLOW", 0, create=True), \
             mock.patch.dict(PREP.ensure_owned_named_child.__globals__, {"revalidate_owned_directory": mock.Mock(side_effect=PREP.Failure("DIRECTORY_IDENTITY_LOST", "TEST"))}), mock.patch.object(PREP.os, "mkdir") as mkdir:
            with self.assertRaises(PREP.Failure) as caught: PREP.ensure_owned_named_child(parent, "runtime", 0o750, "TEST")
        mkdir.assert_not_called(); self.assertNotIsInstance(caught.exception, PREP.NamedChildFailure)

    def test_second_parent_revalidation_before_mkdir_failure_does_not_claim_creation(self):
        parent = PREP.OwnedDirectory(pathlib.Path("/anchor"), 99, 1, 2, 3, 4, 0o750)
        revalidate = mock.Mock(side_effect=[None, PREP.Failure("DIRECTORY_IDENTITY_LOST", "TEST")])
        with mock.patch.object(PREP.os, "name", "posix"), mock.patch.object(PREP.os, "O_DIRECTORY", 0, create=True), mock.patch.object(PREP.os, "O_NOFOLLOW", 0, create=True), \
             mock.patch.dict(PREP.ensure_owned_named_child.__globals__, {"revalidate_owned_directory": revalidate}), \
             mock.patch.object(PREP.os, "stat", side_effect=FileNotFoundError()) as child_stat, mock.patch.object(PREP.os, "mkdir") as mkdir, \
             mock.patch.object(PREP.os, "open") as child_open, mock.patch.object(PREP.os, "unlink") as unlink, mock.patch.object(PREP.os, "rmdir") as rmdir:
            with self.assertRaises(PREP.Failure) as caught:
                PREP.ensure_owned_named_child(parent, "runtime", 0o750, "TEST", require_same_device=False)
        self.assertNotIsInstance(caught.exception, PREP.NamedChildFailure)
        self.assertEqual(caught.exception.code, "DIRECTORY_IDENTITY_LOST"); self.assertEqual(caught.exception.stage, "TEST")
        self.assertFalse(getattr(caught.exception, "creation_occurred", False)); self.assertEqual(revalidate.call_count, 2)
        child_stat.assert_called_once_with("runtime", dir_fd=parent.fd, follow_symlinks=False)
        mkdir.assert_not_called(); child_open.assert_not_called(); unlink.assert_not_called(); rmdir.assert_not_called()

    def test_generic_mkdir_failure_does_not_claim_creation(self):
        parent = PREP.OwnedDirectory(pathlib.Path("/anchor"), 99, 1, 2, 3, 4, 0o750)
        mkdir_failure = OSError(5, "SECRET_SHOULD_NEVER_APPEAR")
        revalidate = mock.Mock()
        with mock.patch.object(PREP.os, "name", "posix"), mock.patch.object(PREP.os, "O_DIRECTORY", 0, create=True), mock.patch.object(PREP.os, "O_NOFOLLOW", 0, create=True), \
             mock.patch.dict(PREP.ensure_owned_named_child.__globals__, {"revalidate_owned_directory": revalidate}), \
             mock.patch.object(PREP.os, "stat", side_effect=FileNotFoundError()) as child_stat, mock.patch.object(PREP.os, "mkdir", side_effect=mkdir_failure) as mkdir, \
             mock.patch.object(PREP.os, "open") as child_open, mock.patch.object(PREP.os, "unlink") as unlink, mock.patch.object(PREP.os, "rmdir") as rmdir:
            with self.assertRaises(PREP.Failure) as caught:
                PREP.ensure_owned_named_child(parent, "runtime", 0o750, "TEST", require_same_device=False)
        self.assertNotIsInstance(caught.exception, PREP.NamedChildFailure)
        self.assertEqual(caught.exception.code, "NAMED_CHILD_CREATION_FAILED"); self.assertEqual(caught.exception.stage, "TEST")
        self.assertFalse(getattr(caught.exception, "creation_occurred", False)); self.assertNotIn("SECRET_SHOULD_NEVER_APPEAR", str(caught.exception))
        self.assertEqual(revalidate.call_count, 2); child_stat.assert_called_once_with("runtime", dir_fd=parent.fd, follow_symlinks=False)
        mkdir.assert_called_once_with("runtime", mode=0o750, dir_fd=parent.fd); child_open.assert_not_called(); unlink.assert_not_called(); rmdir.assert_not_called()

    def _trusted_path_bound_acquisition_case(self, substituted):
        paths = [pathlib.PurePosixPath(value) for value in
                 ("/", "/home", "/home/jazofv1", "/home/jazofv1/hioc")]
        tokens = [(8, 101, 0, 0, 0o755), (9, 102, 3, 4, 0o750),
                  (10, 103, 3, 4, 0o750), (11, 104, 3, 4, 0o750)]
        descriptors = {
            40 + index: types.SimpleNamespace(
                st_dev=dev, st_ino=ino, st_uid=uid, st_gid=gid,
                st_mode=stat.S_IFDIR | mode)
            for index, (dev, ino, uid, gid, mode) in enumerate(tokens)}
        replacement = types.SimpleNamespace(st_dev=11, st_ino=999, st_uid=3,
                                            st_gid=4, st_mode=stat.S_IFDIR | 0o750)
        events, inspections = [], {}
        directory_flag, nofollow_flag = 0x10000, 0x20000
        flags = os.O_RDONLY | directory_flag | nofollow_flag

        def inspect_root(path):
            events.append(("lstat", path))
            self.assertEqual(path, "/")
            return descriptors[40]

        def open_component(path, supplied_flags, *, dir_fd=None):
            events.append(("open", path, supplied_flags, dir_fd))
            self.assertEqual(supplied_flags, flags)
            if dir_fd is None:
                self.assertEqual(path, paths[0])
                return 40
            self.assertIn(dir_fd, (40, 41, 42))
            self.assertEqual(path, paths[dir_fd - 39].name)
            return dir_fd + 1

        def descriptor_token(fd):
            events.append(("fstat", fd))
            return descriptors[fd]

        def inspect_component(name, *, dir_fd, follow_symlinks):
            events.append(("stat", name, dir_fd, follow_symlinks))
            self.assertFalse(follow_symlinks)
            self.assertIn(dir_fd, (40, 41, 42))
            self.assertEqual(name, paths[dir_fd - 39].name)
            key = (name, dir_fd)
            inspections[key] = inspections.get(key, 0) + 1
            if substituted and key == ("hioc", 42) and inspections[key] == 2:
                return replacement
            return descriptors[dir_fd + 1]

        common = sys.modules[PREP.open_trusted_owned_path_bound.__module__]
        with contextlib.ExitStack() as patches:
            patches.enter_context(mock.patch.object(PREP.os, "name", "posix"))
            patches.enter_context(mock.patch.object(PREP.pathlib, "Path", pathlib.PurePosixPath))
            patches.enter_context(mock.patch.object(PREP.os, "O_DIRECTORY", directory_flag, create=True))
            patches.enter_context(mock.patch.object(PREP.os, "O_NOFOLLOW", nofollow_flag, create=True))
            patches.enter_context(mock.patch.object(PREP.os, "getuid", return_value=3, create=True))
            patches.enter_context(mock.patch.object(PREP.os, "getgid", return_value=4, create=True))
            patches.enter_context(mock.patch.object(PREP.os, "lstat", side_effect=inspect_root))
            opened = patches.enter_context(mock.patch.object(PREP.os, "open", side_effect=open_component))
            patches.enter_context(mock.patch.object(PREP.os, "fstat", side_effect=descriptor_token))
            patches.enter_context(mock.patch.object(PREP.os, "stat", side_effect=inspect_component))
            closed = patches.enter_context(mock.patch.object(
                PREP.os, "close", side_effect=lambda fd: events.append(("close", fd))))
            revalidated = patches.enter_context(mock.patch.object(
                common, "revalidate_path_bound_directory",
                wraps=common.revalidate_path_bound_directory))
            leaf = None
            if substituted:
                with self.assertRaises(PREP.Failure) as caught:
                    leaf = PREP.open_trusted_owned_path_bound(paths[-1], "TEST")
                self.assertIs(type(caught.exception), PREP.Failure)
                self.assertEqual((caught.exception.code, caught.exception.stage),
                                 ("TRUSTED_PATH_COMPONENT_SUBSTITUTED", "TEST"))
                self.assertIsNone(leaf)
                revalidated.assert_not_called()
                self.assertEqual(closed.call_args_list,
                                 [mock.call(fd) for fd in (43, 42, 41, 40)])
                self.assertEqual(len({call.args[0] for call in closed.call_args_list}), 4)
            else:
                leaf = PREP.open_trusted_owned_path_bound(paths[-1], "TEST")
                self.assertIsInstance(leaf, PREP.OwnedDirectory)
                revalidated.assert_called_once_with(leaf, "TEST")
                closed.assert_not_called()
                chain, current = [], leaf
                while current is not None:
                    chain.append(current)
                    current = current.parent
                chain.reverse()
                self.assertEqual([item.path for item in chain], paths)
                self.assertIs(leaf, chain[-1])
                for index, item in enumerate(chain):
                    self.assertEqual(item.fd, 40 + index)
                    self.assertEqual((item.dev, item.ino, item.uid, item.gid, item.mode), tokens[index])
                    self.assertIs(item.parent, chain[index - 1] if index else None)
                self.assertEqual(len({item.dev for item in chain}), 4)
            self.assertEqual(opened.call_args_list, [mock.call(paths[0], flags)] + [
                mock.call(path.name, flags, dir_fd=40 + index)
                for index, path in enumerate(paths[1:])])

        expected = [("lstat", "/"), ("open", paths[0], flags, None), ("fstat", 40)]
        for index, path in enumerate(paths[1:]):
            parent_fd = 40 + index
            expected.extend([("stat", path.name, parent_fd, False),
                             ("open", path.name, flags, parent_fd),
                             ("fstat", parent_fd + 1),
                             ("stat", path.name, parent_fd, False)])
        if substituted:
            expected.extend(("close", fd) for fd in (43, 42, 41, 40))
        else:
            expected.append(("fstat", 40))
            for index, path in enumerate(paths[1:]):
                expected.extend([("fstat", 41 + index), ("fstat", 40 + index),
                                 ("stat", path.name, 40 + index, False)])
        self.assertEqual(events, expected)

    def test_trusted_path_bound_acquisition_unchanged_chain_succeeds(self):
        self._trusted_path_bound_acquisition_case(False)

    def test_trusted_path_bound_acquisition_component_substitution_is_rejected(self):
        self._trusted_path_bound_acquisition_case(True)

    def _path_bound_anchor_revalidation_case(self, replacement, name_lost=False, parent_replacement=False, descriptor_loss=False, entry_removed=False):
        paths = ("/", "/home", "/home/jazofv1", "/home/jazofv1/hioc")
        chain = []
        entries = {}
        for index, path in enumerate(paths):
            mode = 0o755 if index == 0 else 0o750
            directory = PREP.OwnedDirectory(
                pathlib.Path(path), 40 + index, 11, 101 + index, 3, 4, mode,
                chain[-1] if chain else None)
            chain.append(directory)
            entries[directory.fd] = types.SimpleNamespace(
                st_mode=stat.S_IFDIR | mode, st_dev=11, st_ino=101 + index,
                st_uid=3, st_gid=4)
        anchor = chain[-1]
        retained = [(item.path, item.fd, item.parent, item.dev, item.ino,
                     item.uid, item.gid, item.mode) for item in chain]
        named_entries = {
            (item.path.name, item.parent.fd): entries[item.fd]
            for item in chain[1:]
        }
        if replacement:
            named_entries[("hioc", chain[-2].fd)] = types.SimpleNamespace(
                st_mode=stat.S_IFDIR | 0o750, st_dev=11, st_ino=999,
                st_uid=3, st_gid=4)

        if parent_replacement:
            named_entries[("jazofv1", chain[1].fd)] = types.SimpleNamespace(
                st_mode=stat.S_IFDIR | 0o750, st_dev=11, st_ino=888,
                st_uid=3, st_gid=4)

        descriptor_entries = dict(entries)
        if descriptor_loss:
            descriptor_entries[anchor.fd] = types.SimpleNamespace(
                st_mode=stat.S_IFDIR | 0o750, st_dev=11, st_ino=999,
                st_uid=3, st_gid=4)

        if entry_removed:
            del named_entries[("hioc", chain[-2].fd)]
            self.assertNotIn(("hioc", chain[-2].fd), named_entries)

        def inspect_name(name, *, dir_fd, follow_symlinks):
            self.assertFalse(follow_symlinks)
            if name_lost and (name, dir_fd) == ("hioc", chain[-2].fd):
                raise FileNotFoundError(2, "governed name absent")
            if entry_removed and (name, dir_fd) not in named_entries:
                raise FileNotFoundError(2, "governed entry removed")
            return named_entries[(name, dir_fd)]

        with mock.patch.object(PREP.os, "fstat", side_effect=descriptor_entries.__getitem__) as fstat, \
             mock.patch.object(PREP.os, "stat", side_effect=inspect_name) as named_stat, \
             mock.patch.object(PREP.os, "open") as child_open, \
             mock.patch.object(PREP.os, "mkdir") as mkdir, \
             mock.patch.object(PREP.os, "unlink") as unlink, \
             mock.patch.object(PREP.os, "rmdir") as rmdir, \
             mock.patch.object(PREP.os, "rename") as rename, \
             mock.patch.object(PREP.os, "replace") as replace, \
             mock.patch.object(PREP.os, "chmod") as chmod, \
             mock.patch.object(PREP.os, "fchmod", create=True) as fchmod, \
             mock.patch.object(PREP.os, "chown", create=True) as chown, \
             mock.patch.object(PREP.os, "fchown", create=True) as fchown, \
             mock.patch.object(PREP.os, "close") as close:
            if replacement or name_lost or parent_replacement or descriptor_loss or entry_removed:
                with self.assertRaises(PREP.Failure) as caught:
                    PREP.revalidate_path_bound_directory(anchor, "TEST")
                self.assertNotIsInstance(caught.exception, PREP.NamedChildFailure)
                self.assertEqual(caught.exception.code,
                                 "DIRECTORY_IDENTITY_LOST" if descriptor_loss else
                                 "DIRECTORY_NAME_LOST" if name_lost or entry_removed else "DIRECTORY_NAME_SUBSTITUTED")
                self.assertEqual(caught.exception.stage, "TEST")
            else:
                self.assertIsNone(PREP.revalidate_path_bound_directory(anchor, "TEST"))
            for operation in (child_open, mkdir, unlink, rmdir, rename, replace,
                              chmod, fchmod, chown, fchown, close):
                operation.assert_not_called()
        expected_fds = ((40, 41, 40, 42, 41) if parent_replacement else
                        (40, 41, 40, 42, 41, 43) if descriptor_loss else
                        (40, 41, 40, 42, 41, 43, 42))
        self.assertEqual(fstat.call_args_list, [mock.call(fd) for fd in expected_fds])
        expected_inspections = [
            mock.call("home", dir_fd=40, follow_symlinks=False),
            mock.call("jazofv1", dir_fd=41, follow_symlinks=False)]
        if not parent_replacement and not descriptor_loss:
            expected_inspections.append(mock.call("hioc", dir_fd=42, follow_symlinks=False))
        self.assertEqual(named_stat.call_args_list, expected_inspections)
        self.assertEqual(entries[42].st_ino, 103)
        self.assertEqual([(item.path, item.fd, item.parent, item.dev, item.ino,
                           item.uid, item.gid, item.mode) for item in chain], retained)
        self.assertEqual(entries[43].st_ino, 104)
        self.assertIs(anchor.parent, chain[2])
        self.assertIs(chain[2].parent, chain[1])
        self.assertIs(chain[1].parent, chain[0])
        self.assertIsNone(chain[0].parent)

    def test_path_bound_anchor_unchanged_chain_revalidates(self):
        self._path_bound_anchor_revalidation_case(False)

    def test_path_bound_anchor_valid_replacement_is_rejected(self):
        self._path_bound_anchor_revalidation_case(True)

    def test_path_bound_anchor_rename_away_is_rejected_as_name_lost(self):
        self._path_bound_anchor_revalidation_case(False, name_lost=True)

    def test_path_bound_parent_valid_replacement_is_rejected(self):
        self._path_bound_anchor_revalidation_case(False, parent_replacement=True)

    def test_path_bound_anchor_descriptor_identity_loss_is_rejected(self):
        self._path_bound_anchor_revalidation_case(False, descriptor_loss=True)

    def test_owned_directory_parent_identity_loss_is_rejected(self):
        parent = PREP.OwnedDirectory(pathlib.Path("/home/jazofv1"), 42,
                                     11, 103, 3, 4, 0o750)
        child = PREP.OwnedDirectory(parent.path / "hioc", 43,
                                    11, 104, 3, 4, 0o750, parent)
        retained = [(item.path, item.fd, item.parent, item.dev, item.ino,
                     item.uid, item.gid, item.mode) for item in (parent, child)]
        child_entry = types.SimpleNamespace(st_mode=stat.S_IFDIR | 0o750,
                                           st_dev=11, st_ino=104, st_uid=3, st_gid=4)
        changed_parent = types.SimpleNamespace(st_mode=stat.S_IFDIR | 0o750,
                                              st_dev=11, st_ino=999, st_uid=3, st_gid=4)
        descriptor_entries = {43: child_entry, 42: changed_parent}
        with mock.patch.object(PREP.os, "fstat", side_effect=descriptor_entries.__getitem__) as fstat, \
             mock.patch.object(PREP.os, "stat", return_value=child_entry) as named_stat, \
             mock.patch.object(PREP.os, "lstat") as lstat, \
             mock.patch.object(PREP.os, "open") as child_open, \
             mock.patch.object(PREP.os, "mkdir") as mkdir, \
             mock.patch.object(PREP.os, "unlink") as unlink, \
             mock.patch.object(PREP.os, "rmdir") as rmdir, \
             mock.patch.object(PREP.os, "rename") as rename, \
             mock.patch.object(PREP.os, "replace") as replace, \
             mock.patch.object(PREP.os, "chmod") as chmod, \
             mock.patch.object(PREP.os, "fchmod", create=True) as fchmod, \
             mock.patch.object(PREP.os, "chown", create=True) as chown, \
             mock.patch.object(PREP.os, "fchown", create=True) as fchown, \
             mock.patch.object(PREP.os, "close") as close:
            with self.assertRaises(PREP.Failure) as caught:
                PREP.revalidate_owned_directory(child, "TEST")
            self.assertNotIsInstance(caught.exception, PREP.NamedChildFailure)
            self.assertEqual(caught.exception.code, "DIRECTORY_PARENT_IDENTITY_LOST")
            self.assertEqual(caught.exception.stage, "TEST")
            self.assertEqual(fstat.call_args_list, [mock.call(43), mock.call(42)])
            for operation in (named_stat, lstat, child_open, mkdir, unlink, rmdir,
                              rename, replace, chmod, fchmod, chown, fchown, close):
                operation.assert_not_called()
        self.assertEqual([(item.path, item.fd, item.parent, item.dev, item.ino,
                           item.uid, item.gid, item.mode) for item in (parent, child)], retained)
        self.assertIs(child.parent, parent)

    def test_path_bound_anchor_entry_removal_is_rejected_as_name_lost(self):
        self._path_bound_anchor_revalidation_case(False, entry_removed=True)

    def _main_anchor_binding_checkpoint(self, fail_at):
        paths = ("/", "/home", "/home/jazofv1", "/home/jazofv1/hioc",
                 "/home/jazofv1/hioc/runtime", "/home/jazofv1/hioc/runtime/pe4",
                 "/home/jazofv1/hioc/runtime/pe4/environments")
        chain, entries = [], {}
        for index, path in enumerate(paths):
            mode = 0o755 if index == 0 else 0o750
            item = PREP.OwnedDirectory(pathlib.Path(path), 40 + index,
                                      11, 101 + index, 3, 4, mode,
                                      chain[-1] if chain else None)
            chain.append(item)
            entries[item.fd] = types.SimpleNamespace(
                st_mode=stat.S_IFDIR | mode, st_dev=item.dev, st_ino=item.ino,
                st_uid=item.uid, st_gid=item.gid)
        anchor, runtime, pe4, environments = chain[3:]
        named_entries = {(item.path.name, item.parent.fd): entries[item.fd]
                         for item in chain[1:]}
        original_entry = named_entries[("hioc", 42)]
        replacement_entry = types.SimpleNamespace(
            st_mode=original_entry.st_mode, st_dev=original_entry.st_dev,
            st_ino=999, st_uid=original_entry.st_uid, st_gid=original_entry.st_gid)
        real_revalidate = PREP.revalidate_path_bound_directory
        records, failures, events = [], [], []

        def revalidate(item, stage):
            number = len(records) + 1
            records.append((number, item, stage))
            events.append(("checkpoint", number, item, stage))
            if number == fail_at:
                named_entries[("hioc", 42)] = replacement_entry
            try:
                result = real_revalidate(item, stage)
                events.append(("checkpoint_pass", number))
                return result
            except PREP.Failure as exc:
                failures.append(exc)
                events.append(("checkpoint_fail", number, exc.code, exc.stage))
                raise

        def inspect_name(name, *, dir_fd, follow_symlinks):
            self.assertFalse(follow_symlinks)
            return named_entries[(name, dir_fd)]

        hierarchy_results = {"runtime": runtime, "pe4": pe4, "environments": environments}
        hierarchy_mocks = {name: mock.Mock(return_value=(item, False))
                           for name, item in hierarchy_results.items()}

        def ensure_child(parent, name, mode, stage, **kwargs):
            events.append(("hierarchy_call", name))
            result = hierarchy_mocks[name](parent, name, mode, stage, **kwargs)
            events.append(("hierarchy_return", name, result[0], result[1]))
            return result

        evidence_root = PREP.OwnedDirectory(pathlib.Path("/tmp"), 50, 11, 150, 3, 4, 0o1777)
        evidence = PREP.OwnedDirectory(
            pathlib.Path("/tmp/hioc-pe4-runtime-hierarchy-prepare-AbCd1234"),
            51, 11, 151, 3, 4, 0o700, evidence_root)
        def open_evidence_root(stage):
            events.append(("open_tmp_root", stage))
            return evidence_root

        def create_evidence_directory(parent, prefix, mode, stage):
            events.append(("create_owned_child", parent, prefix, mode, stage))
            return evidence

        def publish_evidence(directory, name, document, stage, *, max_bytes):
            self.assertEqual(max_bytes, PREP.EVIDENCE_MAX_BYTES)
            events.append(("publish_owned_json", directory, name, stage))
            events.append(("publish_owned_json_return", "0" * 64))
            return "0" * 64

        open_evidence = mock.Mock(side_effect=open_evidence_root)
        create_evidence = mock.Mock(side_effect=create_evidence_directory)
        publish = mock.Mock(side_effect=publish_evidence)
        acquire = mock.Mock(return_value=anchor)
        output = io.StringIO()
        with mock.patch.multiple(PREP, verify_pi3=mock.Mock(), verify_repository=mock.Mock(),
                                 open_trusted_owned_path_bound=acquire,
                                 revalidate_path_bound_directory=mock.Mock(side_effect=revalidate),
                                 ensure_owned_named_child=mock.Mock(side_effect=ensure_child),
                                 open_tmp_root=open_evidence, create_owned_child=create_evidence,
                                 publish_owned_json=publish), \
             mock.patch.object(PREP.os, "fstat", side_effect=entries.__getitem__) as fstat, \
             mock.patch.object(PREP.os, "stat", side_effect=inspect_name) as named_stat, \
             mock.patch.object(PREP.os, "open") as reopened, \
             mock.patch.object(PREP.os, "close") as close, \
             mock.patch.object(PREP.os, "umask", return_value=0o022), \
             mock.patch.object(sys, "argv", ["d-prep", "--governance-commit", "0" * 40]), \
             contextlib.redirect_stdout(output):
            result = PREP.main()
        return types.SimpleNamespace(
            result=result, output=output.getvalue(), records=records, failures=failures, events=events,
            chain=chain, entries=entries, original_entry=original_entry,
            replacement_entry=replacement_entry, hierarchy=hierarchy_mocks,
            evidence_root=evidence_root, evidence=evidence,
            open_evidence=open_evidence, create_evidence=create_evidence, publish=publish,
            acquire=acquire, fstat=fstat, named_stat=named_stat, reopened=reopened, close=close)

    def test_main_checkpoint_1_anchor_substitution_stops_before_runtime(self):
        run = self._main_anchor_binding_checkpoint(fail_at=1)
        anchor = run.chain[3]
        self.assertEqual(run.records, [(1, anchor, "RUNTIME_PARENT")])
        run.acquire.assert_called_once_with(PREP.RUNTIME, "RUNTIME_ANCHOR")
        self.assertEqual(run.fstat.call_args_list,
                         [mock.call(fd) for fd in (40, 41, 40, 42, 41, 43, 42)])
        self.assertEqual(run.named_stat.call_args_list, [
            mock.call("home", dir_fd=40, follow_symlinks=False),
            mock.call("jazofv1", dir_fd=41, follow_symlinks=False),
            mock.call("hioc", dir_fd=42, follow_symlinks=False)])
        self.assertEqual(vars(run.entries[43]), vars(run.original_entry))
        expected_entry = dict(vars(run.original_entry), st_ino=999)
        self.assertEqual(vars(run.replacement_entry), expected_entry)
        self.assertEqual(run.original_entry.st_ino, 104)
        self.assertEqual((anchor.dev, anchor.ino, anchor.uid, anchor.gid, anchor.mode),
                         (11, 104, 3, 4, 0o750))
        self.assertEqual(len(run.failures), 1)
        self.assertIsInstance(run.failures[0], PREP.Failure)
        self.assertNotIsInstance(run.failures[0], PREP.NamedChildFailure)
        self.assertEqual(run.failures[0].code, "DIRECTORY_NAME_SUBSTITUTED")
        self.assertEqual(run.failures[0].stage, "RUNTIME_PARENT")
        self.assertEqual(run.result, 1)
        lines = run.output.splitlines()
        for line in ("RESULT=FAIL", "ERROR_CODE=DIRECTORY_NAME_SUBSTITUTED",
                     "FAILURE_STAGE=RUNTIME_PARENT", "ROLLBACK_RECOMMENDED=FALSE",
                     "STOP_REQUIRED=TRUE", "EVIDENCE_STATE=NOT_CREATED"):
            self.assertEqual(lines.count(line), 1)
        self.assertEqual(sum(line.startswith("RESULT=") for line in lines), 1)
        self.assertNotIn("RESULT=PASS", run.output)
        self.assertNotIn("EVIDENCE_DIR=", run.output)
        for operation in (*run.hierarchy.values(), run.open_evidence,
                          run.create_evidence, run.publish, run.reopened):
            operation.assert_not_called()
        run.close.assert_called_once_with(43)
        self.assertEqual(anchor.fd, -1)  # Expected main() finally cleanup.

    def test_main_checkpoint_2_anchor_substitution_stops_after_runtime(self):
        run = self._main_anchor_binding_checkpoint(fail_at=2)
        anchor, runtime = run.chain[3:5]
        self.assertEqual(run.records, [(1, anchor, "RUNTIME_PARENT"),
                                       (2, anchor, "RUNTIME_PARENT")])
        self.assertEqual(run.events, [
            ("checkpoint", 1, anchor, "RUNTIME_PARENT"),
            ("checkpoint_pass", 1),
            ("hierarchy_call", "runtime"),
            ("hierarchy_return", "runtime", runtime, False),
            ("checkpoint", 2, anchor, "RUNTIME_PARENT"),
            ("checkpoint_fail", 2, "DIRECTORY_NAME_SUBSTITUTED", "RUNTIME_PARENT")])
        run.hierarchy["runtime"].assert_called_once_with(
            anchor, "runtime", 0o750, "RUNTIME_PARENT", require_same_device=False)
        run.hierarchy["pe4"].assert_not_called()
        run.hierarchy["environments"].assert_not_called()
        self.assertEqual(run.fstat.call_args_list,
                         [mock.call(fd) for fd in (40, 41, 40, 42, 41, 43, 42)] * 2)
        self.assertEqual(run.named_stat.call_args_list, [
            mock.call("home", dir_fd=40, follow_symlinks=False),
            mock.call("jazofv1", dir_fd=41, follow_symlinks=False),
            mock.call("hioc", dir_fd=42, follow_symlinks=False)] * 2)
        self.assertEqual(vars(run.entries[43]), vars(run.original_entry))
        self.assertEqual(run.original_entry.st_ino, 104)
        self.assertEqual(vars(run.replacement_entry),
                         dict(vars(run.original_entry), st_ino=999))
        self.assertEqual((anchor.dev, anchor.ino, anchor.uid, anchor.gid, anchor.mode),
                         (11, 104, 3, 4, 0o750))
        self.assertEqual(len(run.failures), 1)
        self.assertIsInstance(run.failures[0], PREP.Failure)
        self.assertNotIsInstance(run.failures[0], PREP.NamedChildFailure)
        self.assertEqual(run.failures[0].code, "DIRECTORY_NAME_SUBSTITUTED")
        self.assertEqual(run.failures[0].stage, "RUNTIME_PARENT")
        self.assertEqual(run.result, 1)
        lines = run.output.splitlines()
        for line in ("RESULT=FAIL", "ERROR_CODE=DIRECTORY_NAME_SUBSTITUTED",
                     "FAILURE_STAGE=RUNTIME_PARENT", "ROLLBACK_RECOMMENDED=FALSE",
                     "STOP_REQUIRED=TRUE", "EVIDENCE_STATE=NOT_CREATED"):
            self.assertEqual(lines.count(line), 1)
        self.assertEqual(sum(line.startswith("RESULT=") for line in lines), 1)
        self.assertNotIn("RESULT=PASS", run.output)
        self.assertNotIn("EVIDENCE_DIR=", run.output)
        for operation in (run.open_evidence, run.create_evidence, run.publish, run.reopened):
            operation.assert_not_called()
        self.assertEqual(run.close.call_args_list, [mock.call(44), mock.call(43)])
        self.assertEqual((runtime.fd, anchor.fd), (-1, -1))

    def test_main_checkpoint_3_runtime_revalidation_detects_anchor_substitution(self):
        run = self._main_anchor_binding_checkpoint(fail_at=3)
        anchor, runtime = run.chain[3:5]
        self.assertEqual(run.records, [(1, anchor, "RUNTIME_PARENT"),
                                       (2, anchor, "RUNTIME_PARENT"),
                                       (3, runtime, "RUNTIME_ROOT")])
        self.assertEqual(run.events, [
            ("checkpoint", 1, anchor, "RUNTIME_PARENT"),
            ("checkpoint_pass", 1),
            ("hierarchy_call", "runtime"),
            ("hierarchy_return", "runtime", runtime, False),
            ("checkpoint", 2, anchor, "RUNTIME_PARENT"),
            ("checkpoint_pass", 2),
            ("checkpoint", 3, runtime, "RUNTIME_ROOT"),
            ("checkpoint_fail", 3, "DIRECTORY_NAME_SUBSTITUTED", "RUNTIME_ROOT")])
        run.hierarchy["runtime"].assert_called_once_with(
            anchor, "runtime", 0o750, "RUNTIME_PARENT", require_same_device=False)
        self.assertIs(runtime.parent, anchor)
        self.assertEqual(run.fstat.call_args_list,
                         [mock.call(fd) for fd in (40, 41, 40, 42, 41, 43, 42)] * 3)
        self.assertEqual(run.named_stat.call_args_list, [
            mock.call("home", dir_fd=40, follow_symlinks=False),
            mock.call("jazofv1", dir_fd=41, follow_symlinks=False),
            mock.call("hioc", dir_fd=42, follow_symlinks=False)] * 3)
        self.assertNotIn(mock.call(44), run.fstat.call_args_list)
        self.assertEqual(vars(run.entries[43]), vars(run.original_entry))
        self.assertEqual(run.original_entry.st_ino, 104)
        self.assertEqual(vars(run.replacement_entry),
                         dict(vars(run.original_entry), st_ino=999))
        self.assertEqual((anchor.dev, anchor.ino, anchor.uid, anchor.gid, anchor.mode),
                         (11, 104, 3, 4, 0o750))
        self.assertEqual((runtime.dev, runtime.ino, runtime.uid, runtime.gid, runtime.mode),
                         (11, 105, 3, 4, 0o750))
        self.assertEqual(len(run.failures), 1)
        self.assertIsInstance(run.failures[0], PREP.Failure)
        self.assertNotIsInstance(run.failures[0], PREP.NamedChildFailure)
        self.assertEqual(run.failures[0].code, "DIRECTORY_NAME_SUBSTITUTED")
        self.assertEqual(run.failures[0].stage, "RUNTIME_ROOT")
        self.assertEqual(run.result, 1)
        lines = run.output.splitlines()
        for line in ("RESULT=FAIL", "ERROR_CODE=DIRECTORY_NAME_SUBSTITUTED",
                     "FAILURE_STAGE=RUNTIME_ROOT", "ROLLBACK_RECOMMENDED=FALSE",
                     "STOP_REQUIRED=TRUE", "EVIDENCE_STATE=NOT_CREATED",
                     "RUNTIME_PARENT_STATE=PREEXISTING_COMPLIANT",
                     "CREATED_RUNTIME_PARENT=FALSE", "RUNTIME_ROOT_STATE=NOT_REACHED",
                     "ENVIRONMENTS_STATE=NOT_REACHED"):
            self.assertEqual(lines.count(line), 1)
        self.assertEqual(sum(line.startswith("RESULT=") for line in lines), 1)
        self.assertNotIn("RESULT=PASS", run.output)
        self.assertNotIn("EVIDENCE_DIR=", run.output)
        for operation in (run.hierarchy["pe4"], run.hierarchy["environments"],
                          run.open_evidence, run.create_evidence, run.publish, run.reopened):
            operation.assert_not_called()
        self.assertEqual(run.close.call_args_list, [mock.call(44), mock.call(43)])
        self.assertEqual((runtime.fd, anchor.fd), (-1, -1))

    def test_main_checkpoint_4_runtime_revalidation_stops_after_pe4(self):
        run = self._main_anchor_binding_checkpoint(fail_at=4)
        anchor, runtime, pe4 = run.chain[3:6]
        self.assertEqual(run.records, [(1, anchor, "RUNTIME_PARENT"),
                                       (2, anchor, "RUNTIME_PARENT"),
                                       (3, runtime, "RUNTIME_ROOT"),
                                       (4, runtime, "RUNTIME_ROOT")])
        self.assertEqual(run.events, [
            ("checkpoint", 1, anchor, "RUNTIME_PARENT"),
            ("checkpoint_pass", 1),
            ("hierarchy_call", "runtime"),
            ("hierarchy_return", "runtime", runtime, False),
            ("checkpoint", 2, anchor, "RUNTIME_PARENT"),
            ("checkpoint_pass", 2),
            ("checkpoint", 3, runtime, "RUNTIME_ROOT"),
            ("checkpoint_pass", 3),
            ("hierarchy_call", "pe4"),
            ("hierarchy_return", "pe4", pe4, False),
            ("checkpoint", 4, runtime, "RUNTIME_ROOT"),
            ("checkpoint_fail", 4, "DIRECTORY_NAME_SUBSTITUTED", "RUNTIME_ROOT")])
        run.hierarchy["runtime"].assert_called_once_with(
            anchor, "runtime", 0o750, "RUNTIME_PARENT", require_same_device=False)
        run.hierarchy["pe4"].assert_called_once_with(runtime, "pe4", 0o750, "RUNTIME_ROOT")
        ancestry_fds = [mock.call(fd) for fd in (40, 41, 40, 42, 41, 43, 42)]
        self.assertEqual(run.fstat.call_args_list,
                         ancestry_fds * 3 + [mock.call(44), mock.call(43)] + ancestry_fds)
        ancestry_names = [
            mock.call("home", dir_fd=40, follow_symlinks=False),
            mock.call("jazofv1", dir_fd=41, follow_symlinks=False),
            mock.call("hioc", dir_fd=42, follow_symlinks=False)]
        self.assertEqual(run.named_stat.call_args_list,
                         ancestry_names * 3 +
                         [mock.call("runtime", dir_fd=43, follow_symlinks=False)] + ancestry_names)
        self.assertEqual(vars(run.entries[43]), vars(run.original_entry))
        self.assertEqual(run.original_entry.st_ino, 104)
        self.assertEqual(vars(run.replacement_entry), dict(vars(run.original_entry), st_ino=999))
        self.assertEqual((anchor.dev, anchor.ino, anchor.uid, anchor.gid, anchor.mode),
                         (11, 104, 3, 4, 0o750))
        self.assertEqual(len(run.failures), 1)
        self.assertIsInstance(run.failures[0], PREP.Failure)
        self.assertNotIsInstance(run.failures[0], PREP.NamedChildFailure)
        self.assertEqual(run.failures[0].code, "DIRECTORY_NAME_SUBSTITUTED")
        self.assertEqual(run.failures[0].stage, "RUNTIME_ROOT")
        self.assertEqual(run.result, 1)
        lines = run.output.splitlines()
        for line in ("RESULT=FAIL", "ERROR_CODE=DIRECTORY_NAME_SUBSTITUTED",
                     "FAILURE_STAGE=RUNTIME_ROOT", "ROLLBACK_RECOMMENDED=FALSE",
                     "STOP_REQUIRED=TRUE", "EVIDENCE_STATE=NOT_CREATED",
                     "RUNTIME_PARENT_STATE=PREEXISTING_COMPLIANT",
                     "CREATED_RUNTIME_PARENT=FALSE", "RUNTIME_ROOT_STATE=NOT_REACHED",
                     "CREATED_RUNTIME_ROOT=FALSE", "ENVIRONMENTS_STATE=NOT_REACHED"):
            self.assertEqual(lines.count(line), 1)
        self.assertEqual(sum(line.startswith("RESULT=") for line in lines), 1)
        self.assertNotIn("RESULT=PASS", run.output)
        self.assertNotIn("EVIDENCE_DIR=", run.output)
        for operation in (run.hierarchy["environments"], run.open_evidence,
                          run.create_evidence, run.publish, run.reopened):
            operation.assert_not_called()
        self.assertEqual(run.close.call_args_list, [mock.call(45), mock.call(44), mock.call(43)])
        self.assertEqual((pe4.fd, runtime.fd, anchor.fd), (-1, -1, -1))

    def test_main_checkpoint_5_pe4_revalidation_stops_before_environments(self):
        run = self._main_anchor_binding_checkpoint(fail_at=5)
        anchor, runtime, pe4 = run.chain[3:6]
        self.assertEqual(run.records, [(1, anchor, "RUNTIME_PARENT"),
                                       (2, anchor, "RUNTIME_PARENT"),
                                       (3, runtime, "RUNTIME_ROOT"),
                                       (4, runtime, "RUNTIME_ROOT"),
                                       (5, pe4, "ENVIRONMENTS")])
        self.assertEqual(run.events, [
            ("checkpoint", 1, anchor, "RUNTIME_PARENT"),
            ("checkpoint_pass", 1),
            ("hierarchy_call", "runtime"),
            ("hierarchy_return", "runtime", runtime, False),
            ("checkpoint", 2, anchor, "RUNTIME_PARENT"),
            ("checkpoint_pass", 2),
            ("checkpoint", 3, runtime, "RUNTIME_ROOT"),
            ("checkpoint_pass", 3),
            ("hierarchy_call", "pe4"),
            ("hierarchy_return", "pe4", pe4, False),
            ("checkpoint", 4, runtime, "RUNTIME_ROOT"),
            ("checkpoint_pass", 4),
            ("checkpoint", 5, pe4, "ENVIRONMENTS"),
            ("checkpoint_fail", 5, "DIRECTORY_NAME_SUBSTITUTED", "ENVIRONMENTS")])
        run.hierarchy["runtime"].assert_called_once_with(
            anchor, "runtime", 0o750, "RUNTIME_PARENT", require_same_device=False)
        run.hierarchy["pe4"].assert_called_once_with(runtime, "pe4", 0o750, "RUNTIME_ROOT")
        self.assertIs(pe4.parent, runtime)
        ancestry_fds = [mock.call(fd) for fd in (40, 41, 40, 42, 41, 43, 42)]
        runtime_fds = [mock.call(44), mock.call(43)]
        self.assertEqual(run.fstat.call_args_list,
                         ancestry_fds * 2 + (ancestry_fds + runtime_fds) * 2 + ancestry_fds)
        ancestry_names = [
            mock.call("home", dir_fd=40, follow_symlinks=False),
            mock.call("jazofv1", dir_fd=41, follow_symlinks=False),
            mock.call("hioc", dir_fd=42, follow_symlinks=False)]
        runtime_name = [mock.call("runtime", dir_fd=43, follow_symlinks=False)]
        self.assertEqual(run.named_stat.call_args_list,
                         ancestry_names * 2 + (ancestry_names + runtime_name) * 2 + ancestry_names)
        self.assertNotIn(mock.call(45), run.fstat.call_args_list)
        self.assertEqual(vars(run.entries[43]), vars(run.original_entry))
        self.assertEqual(run.original_entry.st_ino, 104)
        self.assertEqual(vars(run.replacement_entry), dict(vars(run.original_entry), st_ino=999))
        for item, inode in zip(run.chain[3:], (104, 105, 106, 107)):
            self.assertEqual((item.dev, item.ino, item.uid, item.gid, item.mode),
                             (11, inode, 3, 4, 0o750))
            self.assertEqual(run.entries[40 + inode - 101].st_ino, inode)
        self.assertEqual(len(run.failures), 1)
        self.assertIsInstance(run.failures[0], PREP.Failure)
        self.assertNotIsInstance(run.failures[0], PREP.NamedChildFailure)
        self.assertEqual(run.failures[0].code, "DIRECTORY_NAME_SUBSTITUTED")
        self.assertEqual(run.failures[0].stage, "ENVIRONMENTS")
        self.assertEqual(run.result, 1)
        lines = run.output.splitlines()
        for line in ("RESULT=FAIL", "ERROR_CODE=DIRECTORY_NAME_SUBSTITUTED",
                     "FAILURE_STAGE=ENVIRONMENTS", "ROLLBACK_RECOMMENDED=FALSE",
                     "STOP_REQUIRED=TRUE", "EVIDENCE_STATE=NOT_CREATED",
                     "RUNTIME_PARENT_STATE=PREEXISTING_COMPLIANT",
                     "RUNTIME_ROOT_STATE=PREEXISTING_COMPLIANT",
                     "CREATED_RUNTIME_PARENT=FALSE", "CREATED_RUNTIME_ROOT=FALSE",
                     "ENVIRONMENTS_STATE=NOT_REACHED", "CREATED_ENVIRONMENTS=FALSE"):
            self.assertEqual(lines.count(line), 1)
        self.assertEqual(sum(line.startswith("RESULT=") for line in lines), 1)
        self.assertNotIn("RESULT=PASS", run.output)
        self.assertNotIn("EVIDENCE_DIR=", run.output)
        for operation in (run.hierarchy["environments"], run.open_evidence,
                          run.create_evidence, run.publish, run.reopened):
            operation.assert_not_called()
        self.assertEqual(run.close.call_args_list, [mock.call(45), mock.call(44), mock.call(43)])
        self.assertEqual((pe4.fd, runtime.fd, anchor.fd), (-1, -1, -1))

    def test_main_checkpoint_6_pe4_revalidation_stops_after_environments(self):
        run = self._main_anchor_binding_checkpoint(fail_at=6)
        anchor, runtime, pe4, environments = run.chain[3:]
        self.assertEqual(run.records, [(1, anchor, "RUNTIME_PARENT"),
                                       (2, anchor, "RUNTIME_PARENT"),
                                       (3, runtime, "RUNTIME_ROOT"),
                                       (4, runtime, "RUNTIME_ROOT"),
                                       (5, pe4, "ENVIRONMENTS"),
                                       (6, pe4, "ENVIRONMENTS")])
        self.assertEqual(run.events, [
            ("checkpoint", 1, anchor, "RUNTIME_PARENT"),
            ("checkpoint_pass", 1),
            ("hierarchy_call", "runtime"),
            ("hierarchy_return", "runtime", runtime, False),
            ("checkpoint", 2, anchor, "RUNTIME_PARENT"),
            ("checkpoint_pass", 2),
            ("checkpoint", 3, runtime, "RUNTIME_ROOT"),
            ("checkpoint_pass", 3),
            ("hierarchy_call", "pe4"),
            ("hierarchy_return", "pe4", pe4, False),
            ("checkpoint", 4, runtime, "RUNTIME_ROOT"),
            ("checkpoint_pass", 4),
            ("checkpoint", 5, pe4, "ENVIRONMENTS"),
            ("checkpoint_pass", 5),
            ("hierarchy_call", "environments"),
            ("hierarchy_return", "environments", environments, False),
            ("checkpoint", 6, pe4, "ENVIRONMENTS"),
            ("checkpoint_fail", 6, "DIRECTORY_NAME_SUBSTITUTED", "ENVIRONMENTS")])
        run.hierarchy["runtime"].assert_called_once_with(
            anchor, "runtime", 0o750, "RUNTIME_PARENT", require_same_device=False)
        run.hierarchy["pe4"].assert_called_once_with(runtime, "pe4", 0o750, "RUNTIME_ROOT")
        run.hierarchy["environments"].assert_called_once_with(pe4, "environments", 0o750, "ENVIRONMENTS")
        ancestry_fds = [mock.call(fd) for fd in (40, 41, 40, 42, 41, 43, 42)]
        runtime_fds = [mock.call(44), mock.call(43)]
        pe4_fds = [mock.call(45), mock.call(44)]
        self.assertEqual(run.fstat.call_args_list,
                         ancestry_fds * 2 + (ancestry_fds + runtime_fds) * 2 +
                         ancestry_fds + runtime_fds + pe4_fds + ancestry_fds)
        ancestry_names = [
            mock.call("home", dir_fd=40, follow_symlinks=False),
            mock.call("jazofv1", dir_fd=41, follow_symlinks=False),
            mock.call("hioc", dir_fd=42, follow_symlinks=False)]
        runtime_name = [mock.call("runtime", dir_fd=43, follow_symlinks=False)]
        pe4_name = [mock.call("pe4", dir_fd=44, follow_symlinks=False)]
        self.assertEqual(run.named_stat.call_args_list,
                         ancestry_names * 2 + (ancestry_names + runtime_name) * 2 +
                         ancestry_names + runtime_name + pe4_name + ancestry_names)
        self.assertEqual(vars(run.entries[43]), vars(run.original_entry))
        self.assertEqual(run.original_entry.st_ino, 104)
        self.assertEqual(vars(run.replacement_entry), dict(vars(run.original_entry), st_ino=999))
        for item, fd, inode in zip(run.chain[3:], (43, 44, 45, 46), (104, 105, 106, 107)):
            self.assertEqual((item.dev, item.ino, item.uid, item.gid, item.mode),
                             (11, inode, 3, 4, 0o750))
            self.assertEqual(vars(run.entries[fd]), dict(
                st_mode=stat.S_IFDIR | 0o750, st_dev=11, st_ino=inode, st_uid=3, st_gid=4))
        self.assertEqual(len(run.failures), 1)
        self.assertIsInstance(run.failures[0], PREP.Failure)
        self.assertNotIsInstance(run.failures[0], PREP.NamedChildFailure)
        self.assertEqual(run.failures[0].code, "DIRECTORY_NAME_SUBSTITUTED")
        self.assertEqual(run.failures[0].stage, "ENVIRONMENTS")
        self.assertEqual(run.result, 1)
        lines = run.output.splitlines()
        for line in ("RESULT=FAIL", "ERROR_CODE=DIRECTORY_NAME_SUBSTITUTED",
                     "FAILURE_STAGE=ENVIRONMENTS", "ROLLBACK_RECOMMENDED=FALSE",
                     "STOP_REQUIRED=TRUE", "EVIDENCE_STATE=NOT_CREATED",
                     "RUNTIME_PARENT_STATE=PREEXISTING_COMPLIANT",
                     "RUNTIME_ROOT_STATE=PREEXISTING_COMPLIANT",
                     "CREATED_RUNTIME_PARENT=FALSE", "CREATED_RUNTIME_ROOT=FALSE",
                     "ENVIRONMENTS_STATE=NOT_REACHED", "CREATED_ENVIRONMENTS=FALSE"):
            self.assertEqual(lines.count(line), 1)
        self.assertEqual(sum(line.startswith("RESULT=") for line in lines), 1)
        self.assertNotIn("RESULT=PASS", run.output)
        self.assertNotIn("EVIDENCE_DIR=", run.output)
        for operation in (run.open_evidence, run.create_evidence, run.publish, run.reopened):
            operation.assert_not_called()
        self.assertEqual(run.close.call_args_list,
                         [mock.call(46), mock.call(45), mock.call(44), mock.call(43)])
        self.assertEqual((environments.fd, pe4.fd, runtime.fd, anchor.fd), (-1, -1, -1, -1))

    def test_main_checkpoint_7_final_anchor_validation_fails_before_evidence(self):
        run = self._main_anchor_binding_checkpoint(fail_at=7)
        anchor, runtime, pe4, environments = run.chain[3:]
        self.assertEqual(run.records, [(1, anchor, "RUNTIME_PARENT"),
                                       (2, anchor, "RUNTIME_PARENT"),
                                       (3, runtime, "RUNTIME_ROOT"),
                                       (4, runtime, "RUNTIME_ROOT"),
                                       (5, pe4, "ENVIRONMENTS"),
                                       (6, pe4, "ENVIRONMENTS"),
                                       (7, anchor, "FINAL_VALIDATION")])
        self.assertEqual(run.events, [
            ("checkpoint", 1, anchor, "RUNTIME_PARENT"), ("checkpoint_pass", 1),
            ("hierarchy_call", "runtime"),
            ("hierarchy_return", "runtime", runtime, False),
            ("checkpoint", 2, anchor, "RUNTIME_PARENT"), ("checkpoint_pass", 2),
            ("checkpoint", 3, runtime, "RUNTIME_ROOT"), ("checkpoint_pass", 3),
            ("hierarchy_call", "pe4"), ("hierarchy_return", "pe4", pe4, False),
            ("checkpoint", 4, runtime, "RUNTIME_ROOT"), ("checkpoint_pass", 4),
            ("checkpoint", 5, pe4, "ENVIRONMENTS"), ("checkpoint_pass", 5),
            ("hierarchy_call", "environments"),
            ("hierarchy_return", "environments", environments, False),
            ("checkpoint", 6, pe4, "ENVIRONMENTS"), ("checkpoint_pass", 6),
            ("checkpoint", 7, anchor, "FINAL_VALIDATION"),
            ("checkpoint_fail", 7, "DIRECTORY_NAME_SUBSTITUTED", "FINAL_VALIDATION")])
        run.hierarchy["runtime"].assert_called_once_with(
            anchor, "runtime", 0o750, "RUNTIME_PARENT", require_same_device=False)
        run.hierarchy["pe4"].assert_called_once_with(runtime, "pe4", 0o750, "RUNTIME_ROOT")
        run.hierarchy["environments"].assert_called_once_with(pe4, "environments", 0o750, "ENVIRONMENTS")
        ancestry_fds = [mock.call(fd) for fd in (40, 41, 40, 42, 41, 43, 42)]
        runtime_fds = [mock.call(44), mock.call(43)]
        pe4_fds = [mock.call(45), mock.call(44)]
        self.assertEqual(run.fstat.call_args_list,
                         ancestry_fds * 2 + (ancestry_fds + runtime_fds) * 2 +
                         (ancestry_fds + runtime_fds + pe4_fds) * 2 + ancestry_fds)
        ancestry_names = [
            mock.call("home", dir_fd=40, follow_symlinks=False),
            mock.call("jazofv1", dir_fd=41, follow_symlinks=False),
            mock.call("hioc", dir_fd=42, follow_symlinks=False)]
        runtime_name = [mock.call("runtime", dir_fd=43, follow_symlinks=False)]
        pe4_name = [mock.call("pe4", dir_fd=44, follow_symlinks=False)]
        self.assertEqual(run.named_stat.call_args_list,
                         ancestry_names * 2 + (ancestry_names + runtime_name) * 2 +
                         (ancestry_names + runtime_name + pe4_name) * 2 + ancestry_names)
        self.assertEqual(vars(run.entries[43]), vars(run.original_entry))
        self.assertEqual(run.original_entry.st_ino, 104)
        self.assertEqual(vars(run.replacement_entry), dict(vars(run.original_entry), st_ino=999))
        for item, fd, inode in zip(run.chain[3:], (43, 44, 45, 46), (104, 105, 106, 107)):
            self.assertEqual((item.dev, item.ino, item.uid, item.gid, item.mode),
                             (11, inode, 3, 4, 0o750))
            self.assertEqual(vars(run.entries[fd]), dict(
                st_mode=stat.S_IFDIR | 0o750, st_dev=11, st_ino=inode, st_uid=3, st_gid=4))
        self.assertEqual(len(run.failures), 1)
        self.assertIsInstance(run.failures[0], PREP.Failure)
        self.assertNotIsInstance(run.failures[0], PREP.NamedChildFailure)
        self.assertEqual(run.failures[0].code, "DIRECTORY_NAME_SUBSTITUTED")
        self.assertEqual(run.failures[0].stage, "FINAL_VALIDATION")
        self.assertEqual(run.result, 1)
        lines = run.output.splitlines()
        for line in ("RESULT=FAIL", "ERROR_CODE=DIRECTORY_NAME_SUBSTITUTED",
                     "FAILURE_STAGE=FINAL_VALIDATION", "ROLLBACK_RECOMMENDED=FALSE",
                     "STOP_REQUIRED=TRUE", "EVIDENCE_STATE=NOT_CREATED",
                     "RUNTIME_PARENT_STATE=PREEXISTING_COMPLIANT",
                     "RUNTIME_ROOT_STATE=PREEXISTING_COMPLIANT",
                     "ENVIRONMENTS_STATE=PREEXISTING_COMPLIANT",
                     "CREATED_RUNTIME_PARENT=FALSE", "CREATED_RUNTIME_ROOT=FALSE",
                     "CREATED_ENVIRONMENTS=FALSE"):
            self.assertEqual(lines.count(line), 1)
        self.assertEqual(sum(line.startswith("RESULT=") for line in lines), 1)
        self.assertNotIn("RESULT=PASS", run.output)
        self.assertNotIn("EVIDENCE_DIR=", run.output)
        for operation in (run.open_evidence, run.create_evidence, run.publish, run.reopened):
            operation.assert_not_called()
        self.assertEqual(run.close.call_args_list,
                         [mock.call(46), mock.call(45), mock.call(44), mock.call(43)])
        self.assertEqual((environments.fd, pe4.fd, runtime.fd, anchor.fd), (-1, -1, -1, -1))

    def test_main_checkpoint_8_final_runtime_validation_fails_before_evidence(self):
        run = self._main_anchor_binding_checkpoint(fail_at=8)
        anchor, runtime, pe4, environments = run.chain[3:]
        self.assertEqual(run.records, [(1, anchor, "RUNTIME_PARENT"),
                                       (2, anchor, "RUNTIME_PARENT"),
                                       (3, runtime, "RUNTIME_ROOT"),
                                       (4, runtime, "RUNTIME_ROOT"),
                                       (5, pe4, "ENVIRONMENTS"),
                                       (6, pe4, "ENVIRONMENTS"),
                                       (7, anchor, "FINAL_VALIDATION"),
                                       (8, runtime, "FINAL_VALIDATION")])
        self.assertEqual(run.events, [
            ("checkpoint", 1, anchor, "RUNTIME_PARENT"), ("checkpoint_pass", 1),
            ("hierarchy_call", "runtime"),
            ("hierarchy_return", "runtime", runtime, False),
            ("checkpoint", 2, anchor, "RUNTIME_PARENT"), ("checkpoint_pass", 2),
            ("checkpoint", 3, runtime, "RUNTIME_ROOT"), ("checkpoint_pass", 3),
            ("hierarchy_call", "pe4"), ("hierarchy_return", "pe4", pe4, False),
            ("checkpoint", 4, runtime, "RUNTIME_ROOT"), ("checkpoint_pass", 4),
            ("checkpoint", 5, pe4, "ENVIRONMENTS"), ("checkpoint_pass", 5),
            ("hierarchy_call", "environments"),
            ("hierarchy_return", "environments", environments, False),
            ("checkpoint", 6, pe4, "ENVIRONMENTS"), ("checkpoint_pass", 6),
            ("checkpoint", 7, anchor, "FINAL_VALIDATION"),
            ("checkpoint_pass", 7),
            ("checkpoint", 8, runtime, "FINAL_VALIDATION"),
            ("checkpoint_fail", 8, "DIRECTORY_NAME_SUBSTITUTED", "FINAL_VALIDATION")])
        run.hierarchy["runtime"].assert_called_once_with(
            anchor, "runtime", 0o750, "RUNTIME_PARENT", require_same_device=False)
        run.hierarchy["pe4"].assert_called_once_with(runtime, "pe4", 0o750, "RUNTIME_ROOT")
        run.hierarchy["environments"].assert_called_once_with(pe4, "environments", 0o750, "ENVIRONMENTS")
        self.assertIs(runtime.parent, anchor)
        ancestry_fds = [mock.call(fd) for fd in (40, 41, 40, 42, 41, 43, 42)]
        runtime_fds = [mock.call(44), mock.call(43)]
        pe4_fds = [mock.call(45), mock.call(44)]
        self.assertEqual(run.fstat.call_args_list,
                         ancestry_fds * 2 + (ancestry_fds + runtime_fds) * 2 +
                         (ancestry_fds + runtime_fds + pe4_fds) * 2 + ancestry_fds * 2)
        ancestry_names = [
            mock.call("home", dir_fd=40, follow_symlinks=False),
            mock.call("jazofv1", dir_fd=41, follow_symlinks=False),
            mock.call("hioc", dir_fd=42, follow_symlinks=False)]
        runtime_name = [mock.call("runtime", dir_fd=43, follow_symlinks=False)]
        pe4_name = [mock.call("pe4", dir_fd=44, follow_symlinks=False)]
        self.assertEqual(run.named_stat.call_args_list,
                         ancestry_names * 2 + (ancestry_names + runtime_name) * 2 +
                         (ancestry_names + runtime_name + pe4_name) * 2 + ancestry_names * 2)
        self.assertEqual(vars(run.entries[43]), vars(run.original_entry))
        self.assertEqual(run.original_entry.st_ino, 104)
        self.assertEqual(vars(run.replacement_entry), dict(vars(run.original_entry), st_ino=999))
        for item, fd, inode in zip(run.chain[3:], (43, 44, 45, 46), (104, 105, 106, 107)):
            self.assertEqual((item.dev, item.ino, item.uid, item.gid, item.mode),
                             (11, inode, 3, 4, 0o750))
            self.assertEqual(vars(run.entries[fd]), dict(
                st_mode=stat.S_IFDIR | 0o750, st_dev=11, st_ino=inode, st_uid=3, st_gid=4))
        self.assertEqual(len(run.failures), 1)
        self.assertIsInstance(run.failures[0], PREP.Failure)
        self.assertNotIsInstance(run.failures[0], PREP.NamedChildFailure)
        self.assertEqual(run.failures[0].code, "DIRECTORY_NAME_SUBSTITUTED")
        self.assertEqual(run.failures[0].stage, "FINAL_VALIDATION")
        self.assertEqual(run.result, 1)
        lines = run.output.splitlines()
        for line in ("RESULT=FAIL", "ERROR_CODE=DIRECTORY_NAME_SUBSTITUTED",
                     "FAILURE_STAGE=FINAL_VALIDATION", "ROLLBACK_RECOMMENDED=FALSE",
                     "STOP_REQUIRED=TRUE", "EVIDENCE_STATE=NOT_CREATED",
                     "RUNTIME_PARENT_STATE=PREEXISTING_COMPLIANT",
                     "RUNTIME_ROOT_STATE=PREEXISTING_COMPLIANT",
                     "ENVIRONMENTS_STATE=PREEXISTING_COMPLIANT",
                     "CREATED_RUNTIME_PARENT=FALSE", "CREATED_RUNTIME_ROOT=FALSE",
                     "CREATED_ENVIRONMENTS=FALSE"):
            self.assertEqual(lines.count(line), 1)
        self.assertEqual(sum(line.startswith("RESULT=") for line in lines), 1)
        self.assertNotIn("RESULT=PASS", run.output)
        self.assertNotIn("EVIDENCE_DIR=", run.output)
        for operation in (run.open_evidence, run.create_evidence, run.publish, run.reopened):
            operation.assert_not_called()
        self.assertEqual(run.close.call_args_list,
                         [mock.call(46), mock.call(45), mock.call(44), mock.call(43)])
        self.assertEqual((environments.fd, pe4.fd, runtime.fd, anchor.fd), (-1, -1, -1, -1))

    def test_main_checkpoint_9_final_pe4_validation_fails_before_evidence(self):
        run = self._main_anchor_binding_checkpoint(fail_at=9)
        anchor, runtime, pe4, environments = run.chain[3:]
        self.assertEqual(run.records, [(1, anchor, "RUNTIME_PARENT"),
                                       (2, anchor, "RUNTIME_PARENT"),
                                       (3, runtime, "RUNTIME_ROOT"),
                                       (4, runtime, "RUNTIME_ROOT"),
                                       (5, pe4, "ENVIRONMENTS"),
                                       (6, pe4, "ENVIRONMENTS"),
                                       (7, anchor, "FINAL_VALIDATION"),
                                       (8, runtime, "FINAL_VALIDATION"),
                                       (9, pe4, "FINAL_VALIDATION")])
        self.assertEqual(run.events, [
            ("checkpoint", 1, anchor, "RUNTIME_PARENT"), ("checkpoint_pass", 1),
            ("hierarchy_call", "runtime"),
            ("hierarchy_return", "runtime", runtime, False),
            ("checkpoint", 2, anchor, "RUNTIME_PARENT"), ("checkpoint_pass", 2),
            ("checkpoint", 3, runtime, "RUNTIME_ROOT"), ("checkpoint_pass", 3),
            ("hierarchy_call", "pe4"), ("hierarchy_return", "pe4", pe4, False),
            ("checkpoint", 4, runtime, "RUNTIME_ROOT"), ("checkpoint_pass", 4),
            ("checkpoint", 5, pe4, "ENVIRONMENTS"), ("checkpoint_pass", 5),
            ("hierarchy_call", "environments"),
            ("hierarchy_return", "environments", environments, False),
            ("checkpoint", 6, pe4, "ENVIRONMENTS"), ("checkpoint_pass", 6),
            ("checkpoint", 7, anchor, "FINAL_VALIDATION"),
            ("checkpoint_pass", 7),
            ("checkpoint", 8, runtime, "FINAL_VALIDATION"),
            ("checkpoint_pass", 8),
            ("checkpoint", 9, pe4, "FINAL_VALIDATION"),
            ("checkpoint_fail", 9, "DIRECTORY_NAME_SUBSTITUTED", "FINAL_VALIDATION")])
        run.hierarchy["runtime"].assert_called_once_with(
            anchor, "runtime", 0o750, "RUNTIME_PARENT", require_same_device=False)
        run.hierarchy["pe4"].assert_called_once_with(runtime, "pe4", 0o750, "RUNTIME_ROOT")
        run.hierarchy["environments"].assert_called_once_with(pe4, "environments", 0o750, "ENVIRONMENTS")
        self.assertIs(runtime.parent, anchor)
        self.assertIs(pe4.parent, runtime)
        ancestry_fds = [mock.call(fd) for fd in (40, 41, 40, 42, 41, 43, 42)]
        runtime_fds = [mock.call(44), mock.call(43)]
        pe4_fds = [mock.call(45), mock.call(44)]
        self.assertEqual(run.fstat.call_args_list,
                         ancestry_fds * 2 + (ancestry_fds + runtime_fds) * 2 +
                         (ancestry_fds + runtime_fds + pe4_fds) * 2 +
                         ancestry_fds + ancestry_fds + runtime_fds + ancestry_fds)
        ancestry_names = [
            mock.call("home", dir_fd=40, follow_symlinks=False),
            mock.call("jazofv1", dir_fd=41, follow_symlinks=False),
            mock.call("hioc", dir_fd=42, follow_symlinks=False)]
        runtime_name = [mock.call("runtime", dir_fd=43, follow_symlinks=False)]
        pe4_name = [mock.call("pe4", dir_fd=44, follow_symlinks=False)]
        self.assertEqual(run.named_stat.call_args_list,
                         ancestry_names * 2 + (ancestry_names + runtime_name) * 2 +
                         (ancestry_names + runtime_name + pe4_name) * 2 +
                         ancestry_names + ancestry_names + runtime_name + ancestry_names)
        self.assertEqual(vars(run.entries[43]), vars(run.original_entry))
        self.assertEqual(run.original_entry.st_ino, 104)
        self.assertEqual(vars(run.replacement_entry), dict(vars(run.original_entry), st_ino=999))
        for item, fd, inode in zip(run.chain[3:], (43, 44, 45, 46), (104, 105, 106, 107)):
            self.assertEqual((item.dev, item.ino, item.uid, item.gid, item.mode),
                             (11, inode, 3, 4, 0o750))
            self.assertEqual(vars(run.entries[fd]), dict(
                st_mode=stat.S_IFDIR | 0o750, st_dev=11, st_ino=inode, st_uid=3, st_gid=4))
        self.assertEqual(len(run.failures), 1)
        self.assertIsInstance(run.failures[0], PREP.Failure)
        self.assertNotIsInstance(run.failures[0], PREP.NamedChildFailure)
        self.assertEqual(run.failures[0].code, "DIRECTORY_NAME_SUBSTITUTED")
        self.assertEqual(run.failures[0].stage, "FINAL_VALIDATION")
        self.assertEqual(run.result, 1)
        lines = run.output.splitlines()
        for line in ("RESULT=FAIL", "ERROR_CODE=DIRECTORY_NAME_SUBSTITUTED",
                     "FAILURE_STAGE=FINAL_VALIDATION", "ROLLBACK_RECOMMENDED=FALSE",
                     "STOP_REQUIRED=TRUE", "EVIDENCE_STATE=NOT_CREATED",
                     "RUNTIME_PARENT_STATE=PREEXISTING_COMPLIANT",
                     "RUNTIME_ROOT_STATE=PREEXISTING_COMPLIANT",
                     "ENVIRONMENTS_STATE=PREEXISTING_COMPLIANT",
                     "CREATED_RUNTIME_PARENT=FALSE", "CREATED_RUNTIME_ROOT=FALSE",
                     "CREATED_ENVIRONMENTS=FALSE"):
            self.assertEqual(lines.count(line), 1)
        self.assertEqual(sum(line.startswith("RESULT=") for line in lines), 1)
        self.assertNotIn("RESULT=PASS", run.output)
        self.assertNotIn("EVIDENCE_DIR=", run.output)
        for operation in (run.open_evidence, run.create_evidence, run.publish, run.reopened):
            operation.assert_not_called()
        self.assertEqual(run.close.call_args_list,
                         [mock.call(46), mock.call(45), mock.call(44), mock.call(43)])
        self.assertEqual((environments.fd, pe4.fd, runtime.fd, anchor.fd), (-1, -1, -1, -1))

    def test_main_checkpoint_10_final_environments_validation_fails_before_evidence(self):
        run = self._main_anchor_binding_checkpoint(fail_at=10)
        anchor, runtime, pe4, environments = run.chain[3:]
        self.assertEqual(run.records, [(1, anchor, "RUNTIME_PARENT"),
                                       (2, anchor, "RUNTIME_PARENT"),
                                       (3, runtime, "RUNTIME_ROOT"),
                                       (4, runtime, "RUNTIME_ROOT"),
                                       (5, pe4, "ENVIRONMENTS"),
                                       (6, pe4, "ENVIRONMENTS"),
                                       (7, anchor, "FINAL_VALIDATION"),
                                       (8, runtime, "FINAL_VALIDATION"),
                                       (9, pe4, "FINAL_VALIDATION"),
                                       (10, environments, "FINAL_VALIDATION")])
        self.assertEqual(run.events, [
            ("checkpoint", 1, anchor, "RUNTIME_PARENT"), ("checkpoint_pass", 1),
            ("hierarchy_call", "runtime"),
            ("hierarchy_return", "runtime", runtime, False),
            ("checkpoint", 2, anchor, "RUNTIME_PARENT"), ("checkpoint_pass", 2),
            ("checkpoint", 3, runtime, "RUNTIME_ROOT"), ("checkpoint_pass", 3),
            ("hierarchy_call", "pe4"), ("hierarchy_return", "pe4", pe4, False),
            ("checkpoint", 4, runtime, "RUNTIME_ROOT"), ("checkpoint_pass", 4),
            ("checkpoint", 5, pe4, "ENVIRONMENTS"), ("checkpoint_pass", 5),
            ("hierarchy_call", "environments"),
            ("hierarchy_return", "environments", environments, False),
            ("checkpoint", 6, pe4, "ENVIRONMENTS"), ("checkpoint_pass", 6),
            ("checkpoint", 7, anchor, "FINAL_VALIDATION"),
            ("checkpoint_pass", 7),
            ("checkpoint", 8, runtime, "FINAL_VALIDATION"),
            ("checkpoint_pass", 8),
            ("checkpoint", 9, pe4, "FINAL_VALIDATION"),
            ("checkpoint_pass", 9),
            ("checkpoint", 10, environments, "FINAL_VALIDATION"),
            ("checkpoint_fail", 10, "DIRECTORY_NAME_SUBSTITUTED", "FINAL_VALIDATION")])
        run.hierarchy["runtime"].assert_called_once_with(
            anchor, "runtime", 0o750, "RUNTIME_PARENT", require_same_device=False)
        run.hierarchy["pe4"].assert_called_once_with(runtime, "pe4", 0o750, "RUNTIME_ROOT")
        run.hierarchy["environments"].assert_called_once_with(pe4, "environments", 0o750, "ENVIRONMENTS")
        self.assertIs(runtime.parent, anchor)
        self.assertIs(pe4.parent, runtime)
        self.assertIs(environments.parent, pe4)
        ancestry_fds = [mock.call(fd) for fd in (40, 41, 40, 42, 41, 43, 42)]
        runtime_fds = [mock.call(44), mock.call(43)]
        pe4_fds = [mock.call(45), mock.call(44)]
        self.assertEqual(run.fstat.call_args_list,
                         ancestry_fds * 2 + (ancestry_fds + runtime_fds) * 2 +
                         (ancestry_fds + runtime_fds + pe4_fds) * 2 +
                         ancestry_fds + ancestry_fds + runtime_fds +
                         ancestry_fds + runtime_fds + pe4_fds + ancestry_fds)
        ancestry_names = [
            mock.call("home", dir_fd=40, follow_symlinks=False),
            mock.call("jazofv1", dir_fd=41, follow_symlinks=False),
            mock.call("hioc", dir_fd=42, follow_symlinks=False)]
        runtime_name = [mock.call("runtime", dir_fd=43, follow_symlinks=False)]
        pe4_name = [mock.call("pe4", dir_fd=44, follow_symlinks=False)]
        self.assertEqual(run.named_stat.call_args_list,
                         ancestry_names * 2 + (ancestry_names + runtime_name) * 2 +
                         (ancestry_names + runtime_name + pe4_name) * 2 +
                         ancestry_names + ancestry_names + runtime_name +
                         ancestry_names + runtime_name + pe4_name + ancestry_names)
        self.assertEqual(vars(run.entries[43]), vars(run.original_entry))
        self.assertEqual(run.original_entry.st_ino, 104)
        self.assertEqual(vars(run.replacement_entry), dict(vars(run.original_entry), st_ino=999))
        for item, fd, inode in zip(run.chain[3:], (43, 44, 45, 46), (104, 105, 106, 107)):
            self.assertEqual((item.dev, item.ino, item.uid, item.gid, item.mode),
                             (11, inode, 3, 4, 0o750))
            self.assertEqual(vars(run.entries[fd]), dict(
                st_mode=stat.S_IFDIR | 0o750, st_dev=11, st_ino=inode, st_uid=3, st_gid=4))
        self.assertEqual(len(run.failures), 1)
        self.assertIsInstance(run.failures[0], PREP.Failure)
        self.assertNotIsInstance(run.failures[0], PREP.NamedChildFailure)
        self.assertEqual(run.failures[0].code, "DIRECTORY_NAME_SUBSTITUTED")
        self.assertEqual(run.failures[0].stage, "FINAL_VALIDATION")
        self.assertEqual(run.result, 1)
        lines = run.output.splitlines()
        for line in ("RESULT=FAIL", "ERROR_CODE=DIRECTORY_NAME_SUBSTITUTED",
                     "FAILURE_STAGE=FINAL_VALIDATION", "ROLLBACK_RECOMMENDED=FALSE",
                     "STOP_REQUIRED=TRUE", "EVIDENCE_STATE=NOT_CREATED",
                     "RUNTIME_PARENT_STATE=PREEXISTING_COMPLIANT",
                     "RUNTIME_ROOT_STATE=PREEXISTING_COMPLIANT",
                     "ENVIRONMENTS_STATE=PREEXISTING_COMPLIANT",
                     "CREATED_RUNTIME_PARENT=FALSE", "CREATED_RUNTIME_ROOT=FALSE",
                     "CREATED_ENVIRONMENTS=FALSE"):
            self.assertEqual(lines.count(line), 1)
        self.assertEqual(sum(line.startswith("RESULT=") for line in lines), 1)
        self.assertNotIn("RESULT=PASS", run.output)
        self.assertNotIn("EVIDENCE_DIR=", run.output)
        for operation in (run.open_evidence, run.create_evidence, run.publish, run.reopened):
            operation.assert_not_called()
        self.assertEqual(run.close.call_args_list,
                         [mock.call(46), mock.call(45), mock.call(44), mock.call(43)])
        self.assertEqual((environments.fd, pe4.fd, runtime.fd, anchor.fd), (-1, -1, -1, -1))

    def test_main_checkpoint_11_evidence_preflight_validation_fails_before_setup(self):
        run = self._main_anchor_binding_checkpoint(fail_at=11)
        anchor, runtime, pe4, environments = run.chain[3:]
        self.assertEqual(run.records, [(1, anchor, "RUNTIME_PARENT"),
                                       (2, anchor, "RUNTIME_PARENT"),
                                       (3, runtime, "RUNTIME_ROOT"),
                                       (4, runtime, "RUNTIME_ROOT"),
                                       (5, pe4, "ENVIRONMENTS"),
                                       (6, pe4, "ENVIRONMENTS"),
                                       (7, anchor, "FINAL_VALIDATION"),
                                       (8, runtime, "FINAL_VALIDATION"),
                                       (9, pe4, "FINAL_VALIDATION"),
                                       (10, environments, "FINAL_VALIDATION"),
                                       (11, environments, "EVIDENCE_PUBLICATION")])
        self.assertEqual(run.events, [
            ("checkpoint", 1, anchor, "RUNTIME_PARENT"), ("checkpoint_pass", 1),
            ("hierarchy_call", "runtime"),
            ("hierarchy_return", "runtime", runtime, False),
            ("checkpoint", 2, anchor, "RUNTIME_PARENT"), ("checkpoint_pass", 2),
            ("checkpoint", 3, runtime, "RUNTIME_ROOT"), ("checkpoint_pass", 3),
            ("hierarchy_call", "pe4"), ("hierarchy_return", "pe4", pe4, False),
            ("checkpoint", 4, runtime, "RUNTIME_ROOT"), ("checkpoint_pass", 4),
            ("checkpoint", 5, pe4, "ENVIRONMENTS"), ("checkpoint_pass", 5),
            ("hierarchy_call", "environments"),
            ("hierarchy_return", "environments", environments, False),
            ("checkpoint", 6, pe4, "ENVIRONMENTS"), ("checkpoint_pass", 6),
            ("checkpoint", 7, anchor, "FINAL_VALIDATION"),
            ("checkpoint_pass", 7),
            ("checkpoint", 8, runtime, "FINAL_VALIDATION"),
            ("checkpoint_pass", 8),
            ("checkpoint", 9, pe4, "FINAL_VALIDATION"),
            ("checkpoint_pass", 9),
            ("checkpoint", 10, environments, "FINAL_VALIDATION"),
            ("checkpoint_pass", 10),
            ("checkpoint", 11, environments, "EVIDENCE_PUBLICATION"),
            ("checkpoint_fail", 11, "DIRECTORY_NAME_SUBSTITUTED", "EVIDENCE_PUBLICATION")])
        run.hierarchy["runtime"].assert_called_once_with(
            anchor, "runtime", 0o750, "RUNTIME_PARENT", require_same_device=False)
        run.hierarchy["pe4"].assert_called_once_with(runtime, "pe4", 0o750, "RUNTIME_ROOT")
        run.hierarchy["environments"].assert_called_once_with(pe4, "environments", 0o750, "ENVIRONMENTS")
        self.assertIs(runtime.parent, anchor)
        self.assertIs(pe4.parent, runtime)
        self.assertIs(environments.parent, pe4)
        ancestry_fds = [mock.call(fd) for fd in (40, 41, 40, 42, 41, 43, 42)]
        runtime_fds = [mock.call(44), mock.call(43)]
        pe4_fds = [mock.call(45), mock.call(44)]
        self.assertEqual(run.fstat.call_args_list,
                         ancestry_fds * 2 + (ancestry_fds + runtime_fds) * 2 +
                         (ancestry_fds + runtime_fds + pe4_fds) * 2 +
                         ancestry_fds + ancestry_fds + runtime_fds +
                         ancestry_fds + runtime_fds + pe4_fds +
                         ancestry_fds + runtime_fds + pe4_fds +
                         [mock.call(46), mock.call(45)] + ancestry_fds)
        ancestry_names = [
            mock.call("home", dir_fd=40, follow_symlinks=False),
            mock.call("jazofv1", dir_fd=41, follow_symlinks=False),
            mock.call("hioc", dir_fd=42, follow_symlinks=False)]
        runtime_name = [mock.call("runtime", dir_fd=43, follow_symlinks=False)]
        pe4_name = [mock.call("pe4", dir_fd=44, follow_symlinks=False)]
        self.assertEqual(run.named_stat.call_args_list,
                         ancestry_names * 2 + (ancestry_names + runtime_name) * 2 +
                         (ancestry_names + runtime_name + pe4_name) * 2 +
                         ancestry_names + ancestry_names + runtime_name +
                         ancestry_names + runtime_name + pe4_name +
                         ancestry_names + runtime_name + pe4_name +
                         [mock.call("environments", dir_fd=45, follow_symlinks=False)] + ancestry_names)
        self.assertEqual(vars(run.entries[43]), vars(run.original_entry))
        self.assertEqual(run.original_entry.st_ino, 104)
        self.assertEqual(vars(run.replacement_entry), dict(vars(run.original_entry), st_ino=999))
        for item, fd, inode in zip(run.chain[3:], (43, 44, 45, 46), (104, 105, 106, 107)):
            self.assertEqual((item.dev, item.ino, item.uid, item.gid, item.mode),
                             (11, inode, 3, 4, 0o750))
            self.assertEqual(vars(run.entries[fd]), dict(
                st_mode=stat.S_IFDIR | 0o750, st_dev=11, st_ino=inode, st_uid=3, st_gid=4))
        self.assertEqual(len(run.failures), 1)
        self.assertIsInstance(run.failures[0], PREP.Failure)
        self.assertNotIsInstance(run.failures[0], PREP.NamedChildFailure)
        self.assertEqual(run.failures[0].code, "DIRECTORY_NAME_SUBSTITUTED")
        self.assertEqual(run.failures[0].stage, "EVIDENCE_PUBLICATION")
        self.assertEqual(run.result, 1)
        lines = run.output.splitlines()
        for line in ("RESULT=FAIL", "ERROR_CODE=DIRECTORY_NAME_SUBSTITUTED",
                     "FAILURE_STAGE=EVIDENCE_PUBLICATION", "ROLLBACK_RECOMMENDED=FALSE",
                     "STOP_REQUIRED=TRUE", "EVIDENCE_STATE=UNCONFIRMED", "DIAGNOSTIC_STAGE=EVIDENCE_PUBLICATION",
                     "RUNTIME_PARENT_STATE=PREEXISTING_COMPLIANT",
                     "RUNTIME_ROOT_STATE=PREEXISTING_COMPLIANT",
                     "ENVIRONMENTS_STATE=PREEXISTING_COMPLIANT",
                     "CREATED_RUNTIME_PARENT=FALSE", "CREATED_RUNTIME_ROOT=FALSE",
                     "CREATED_ENVIRONMENTS=FALSE"):
            self.assertEqual(lines.count(line), 1)
        self.assertEqual(sum(line.startswith("RESULT=") for line in lines), 1)
        self.assertNotIn("RESULT=PASS", run.output)
        self.assertNotIn("EVIDENCE_DIR=", run.output)
        for operation in (run.open_evidence, run.create_evidence, run.publish, run.reopened):
            operation.assert_not_called()
        self.assertEqual(run.close.call_args_list,
                         [mock.call(46), mock.call(45), mock.call(44), mock.call(43)])
        self.assertEqual((environments.fd, pe4.fd, runtime.fd, anchor.fd), (-1, -1, -1, -1))

    def test_main_checkpoint_12_final_validation_fails_after_evidence_publication(self):
        run = self._main_anchor_binding_checkpoint(fail_at=12)
        anchor, runtime, pe4, environments = run.chain[3:]
        self.assertEqual(run.records, [(1, anchor, "RUNTIME_PARENT"),
                                       (2, anchor, "RUNTIME_PARENT"),
                                       (3, runtime, "RUNTIME_ROOT"),
                                       (4, runtime, "RUNTIME_ROOT"),
                                       (5, pe4, "ENVIRONMENTS"),
                                       (6, pe4, "ENVIRONMENTS"),
                                       (7, anchor, "FINAL_VALIDATION"),
                                       (8, runtime, "FINAL_VALIDATION"),
                                       (9, pe4, "FINAL_VALIDATION"),
                                       (10, environments, "FINAL_VALIDATION"),
                                       (11, environments, "EVIDENCE_PUBLICATION"),
                                       (12, environments, "FINAL_VALIDATION")])
        self.assertEqual(run.events, [
            ("checkpoint", 1, anchor, "RUNTIME_PARENT"), ("checkpoint_pass", 1),
            ("hierarchy_call", "runtime"),
            ("hierarchy_return", "runtime", runtime, False),
            ("checkpoint", 2, anchor, "RUNTIME_PARENT"), ("checkpoint_pass", 2),
            ("checkpoint", 3, runtime, "RUNTIME_ROOT"), ("checkpoint_pass", 3),
            ("hierarchy_call", "pe4"), ("hierarchy_return", "pe4", pe4, False),
            ("checkpoint", 4, runtime, "RUNTIME_ROOT"), ("checkpoint_pass", 4),
            ("checkpoint", 5, pe4, "ENVIRONMENTS"), ("checkpoint_pass", 5),
            ("hierarchy_call", "environments"),
            ("hierarchy_return", "environments", environments, False),
            ("checkpoint", 6, pe4, "ENVIRONMENTS"), ("checkpoint_pass", 6),
            ("checkpoint", 7, anchor, "FINAL_VALIDATION"),
            ("checkpoint_pass", 7),
            ("checkpoint", 8, runtime, "FINAL_VALIDATION"),
            ("checkpoint_pass", 8),
            ("checkpoint", 9, pe4, "FINAL_VALIDATION"),
            ("checkpoint_pass", 9),
            ("checkpoint", 10, environments, "FINAL_VALIDATION"),
            ("checkpoint_pass", 10),
            ("checkpoint", 11, environments, "EVIDENCE_PUBLICATION"),
            ("checkpoint_pass", 11),
            ("open_tmp_root", "EVIDENCE_PUBLICATION"),
            ("create_owned_child", run.evidence_root, PREP.EVIDENCE_PREFIX, 0o700, "EVIDENCE_PUBLICATION"),
            ("publish_owned_json", run.evidence, "result.json", "EVIDENCE_PUBLICATION"),
            ("publish_owned_json_return", "0" * 64),
            ("checkpoint", 12, environments, "FINAL_VALIDATION"),
            ("checkpoint_fail", 12, "DIRECTORY_NAME_SUBSTITUTED", "FINAL_VALIDATION")])
        run.hierarchy["runtime"].assert_called_once_with(
            anchor, "runtime", 0o750, "RUNTIME_PARENT", require_same_device=False)
        run.hierarchy["pe4"].assert_called_once_with(runtime, "pe4", 0o750, "RUNTIME_ROOT")
        run.hierarchy["environments"].assert_called_once_with(pe4, "environments", 0o750, "ENVIRONMENTS")
        self.assertIs(runtime.parent, anchor)
        self.assertIs(pe4.parent, runtime)
        self.assertIs(environments.parent, pe4)
        ancestry_fds = [mock.call(fd) for fd in (40, 41, 40, 42, 41, 43, 42)]
        runtime_fds = [mock.call(44), mock.call(43)]
        pe4_fds = [mock.call(45), mock.call(44)]
        self.assertEqual(run.fstat.call_args_list,
                         ancestry_fds * 2 + (ancestry_fds + runtime_fds) * 2 +
                         (ancestry_fds + runtime_fds + pe4_fds) * 2 +
                         ancestry_fds + ancestry_fds + runtime_fds +
                         ancestry_fds + runtime_fds + pe4_fds +
                         ancestry_fds + runtime_fds + pe4_fds +
                         [mock.call(46), mock.call(45)] +
                         ancestry_fds + runtime_fds + pe4_fds +
                         [mock.call(46), mock.call(45)] + ancestry_fds)
        ancestry_names = [
            mock.call("home", dir_fd=40, follow_symlinks=False),
            mock.call("jazofv1", dir_fd=41, follow_symlinks=False),
            mock.call("hioc", dir_fd=42, follow_symlinks=False)]
        runtime_name = [mock.call("runtime", dir_fd=43, follow_symlinks=False)]
        pe4_name = [mock.call("pe4", dir_fd=44, follow_symlinks=False)]
        self.assertEqual(run.named_stat.call_args_list,
                         ancestry_names * 2 + (ancestry_names + runtime_name) * 2 +
                         (ancestry_names + runtime_name + pe4_name) * 2 +
                         ancestry_names + ancestry_names + runtime_name +
                         ancestry_names + runtime_name + pe4_name +
                         ancestry_names + runtime_name + pe4_name +
                         [mock.call("environments", dir_fd=45, follow_symlinks=False)] +
                         ancestry_names + runtime_name + pe4_name +
                         [mock.call("environments", dir_fd=45, follow_symlinks=False)] + ancestry_names)
        self.assertEqual(vars(run.entries[43]), vars(run.original_entry))
        self.assertEqual(run.original_entry.st_ino, 104)
        self.assertEqual(vars(run.replacement_entry), dict(vars(run.original_entry), st_ino=999))
        for item, fd, inode in zip(run.chain[3:], (43, 44, 45, 46), (104, 105, 106, 107)):
            self.assertEqual((item.dev, item.ino, item.uid, item.gid, item.mode),
                             (11, inode, 3, 4, 0o750))
            self.assertEqual(vars(run.entries[fd]), dict(
                st_mode=stat.S_IFDIR | 0o750, st_dev=11, st_ino=inode, st_uid=3, st_gid=4))
        self.assertEqual(len(run.failures), 1)
        self.assertIsInstance(run.failures[0], PREP.Failure)
        self.assertNotIsInstance(run.failures[0], PREP.NamedChildFailure)
        self.assertEqual(run.failures[0].code, "DIRECTORY_NAME_SUBSTITUTED")
        self.assertEqual(run.failures[0].stage, "FINAL_VALIDATION")
        self.assertEqual(run.result, 1)
        lines = run.output.splitlines()
        for line in ("RESULT=FAIL", "ERROR_CODE=DIRECTORY_NAME_SUBSTITUTED",
                     "FAILURE_STAGE=FINAL_VALIDATION", "ROLLBACK_RECOMMENDED=FALSE",
                     "STOP_REQUIRED=TRUE", "EVIDENCE_STATE=UNCONFIRMED", "DIAGNOSTIC_STAGE=EVIDENCE_PUBLICATION",
                     "RUNTIME_PARENT_STATE=PREEXISTING_COMPLIANT",
                     "RUNTIME_ROOT_STATE=PREEXISTING_COMPLIANT",
                     "ENVIRONMENTS_STATE=PREEXISTING_COMPLIANT",
                     "CREATED_RUNTIME_PARENT=FALSE", "CREATED_RUNTIME_ROOT=FALSE",
                     "CREATED_ENVIRONMENTS=FALSE"):
            self.assertEqual(lines.count(line), 1)
        self.assertEqual(sum(line.startswith("RESULT=") for line in lines), 1)
        self.assertNotIn("RESULT=PASS", run.output)
        self.assertNotIn("EVIDENCE_DIR=", run.output)
        run.open_evidence.assert_called_once_with("EVIDENCE_PUBLICATION")
        run.create_evidence.assert_called_once_with(
            run.evidence_root, PREP.EVIDENCE_PREFIX, 0o700, "EVIDENCE_PUBLICATION")
        run.publish.assert_called_once()
        self.assertEqual(run.publish.call_args.kwargs, {"max_bytes": PREP.EVIDENCE_MAX_BYTES})
        publication_args = run.publish.call_args.args
        self.assertEqual((publication_args[0], publication_args[1], publication_args[3]),
                         (run.evidence, "result.json", "EVIDENCE_PUBLICATION"))
        self.assertEqual(publication_args[2]["result"], "PASS")
        run.reopened.assert_not_called()
        self.assertEqual(run.close.call_args_list,
                         [mock.call(51), mock.call(50), mock.call(46), mock.call(45), mock.call(44), mock.call(43)])
        self.assertEqual((environments.fd, pe4.fd, runtime.fd, anchor.fd), (-1, -1, -1, -1))

    def test_main_all_revalidation_checkpoints_pass_with_unchanged_anchor(self):
        run = self._main_anchor_binding_checkpoint(fail_at=None)
        anchor, runtime, pe4, environments = run.chain[3:]
        checkpoints = [(anchor, "RUNTIME_PARENT"), (anchor, "RUNTIME_PARENT"),
                       (runtime, "RUNTIME_ROOT"), (runtime, "RUNTIME_ROOT"),
                       (pe4, "ENVIRONMENTS"), (pe4, "ENVIRONMENTS"),
                       (anchor, "FINAL_VALIDATION"), (runtime, "FINAL_VALIDATION"),
                       (pe4, "FINAL_VALIDATION"), (environments, "FINAL_VALIDATION"),
                       (environments, "EVIDENCE_PUBLICATION"), (environments, "FINAL_VALIDATION")]
        self.assertEqual(run.records, [(number, item, stage)
                                       for number, (item, stage) in enumerate(checkpoints, 1)])
        expected_events = []
        for number, (item, stage) in enumerate(checkpoints, 1):
            expected_events.extend([("checkpoint", number, item, stage), ("checkpoint_pass", number)])
            if number in (1, 3, 5):
                name, child = {1: ("runtime", runtime), 3: ("pe4", pe4),
                               5: ("environments", environments)}[number]
                expected_events.extend([("hierarchy_call", name),
                                        ("hierarchy_return", name, child, False)])
            if number == 11:
                expected_events.extend([
                    ("open_tmp_root", "EVIDENCE_PUBLICATION"),
                    ("create_owned_child", run.evidence_root, PREP.EVIDENCE_PREFIX, 0o700, "EVIDENCE_PUBLICATION"),
                    ("publish_owned_json", run.evidence, "result.json", "EVIDENCE_PUBLICATION"),
                    ("publish_owned_json_return", "0" * 64)])
        self.assertEqual(run.events, expected_events)
        run.hierarchy["runtime"].assert_called_once_with(
            anchor, "runtime", 0o750, "RUNTIME_PARENT", require_same_device=False)
        run.hierarchy["pe4"].assert_called_once_with(runtime, "pe4", 0o750, "RUNTIME_ROOT")
        run.hierarchy["environments"].assert_called_once_with(pe4, "environments", 0o750, "ENVIRONMENTS")
        expected_fstat, expected_stat = [], []
        for item, stage in checkpoints:
            depth = run.chain.index(item)
            for index, current in enumerate(run.chain[:depth + 1]):
                fd = 40 + index
                expected_fstat.append(mock.call(fd))
                if index:
                    expected_fstat.append(mock.call(fd - 1))
                    expected_stat.append(mock.call(current.path.name, dir_fd=fd - 1,
                                                   follow_symlinks=False))
        self.assertEqual(run.fstat.call_args_list, expected_fstat)
        self.assertEqual(run.named_stat.call_args_list, expected_stat)
        run.reopened.assert_not_called()
        self.assertEqual(run.failures, [])
        for index, item in enumerate(run.chain):
            mode = 0o755 if index == 0 else 0o750
            self.assertEqual((item.dev, item.ino, item.uid, item.gid, item.mode),
                             (11, 101 + index, 3, 4, mode))
            self.assertIs(item.parent, run.chain[index - 1] if index else None)
            self.assertEqual(vars(run.entries[40 + index]), dict(
                st_mode=stat.S_IFDIR | mode, st_dev=11, st_ino=101 + index, st_uid=3, st_gid=4))
        run.open_evidence.assert_called_once_with("EVIDENCE_PUBLICATION")
        run.create_evidence.assert_called_once_with(
            run.evidence_root, PREP.EVIDENCE_PREFIX, 0o700, "EVIDENCE_PUBLICATION")
        run.publish.assert_called_once()
        self.assertEqual(run.publish.call_args.kwargs, {"max_bytes": PREP.EVIDENCE_MAX_BYTES})
        args = run.publish.call_args.args
        self.assertEqual((args[0], args[1], args[3]),
                         (run.evidence, "result.json", "EVIDENCE_PUBLICATION"))
        self.assertEqual(args[2]["result"], "PASS")
        self.assertEqual(run.result, 0)
        lines = run.output.splitlines()
        for line in ("RESULT=PASS", "ERROR_CODE=NONE", "FAILURE_STAGE=COMPLETE",
                     "ROLLBACK_RECOMMENDED=FALSE", "STOP_REQUIRED=TRUE",
                     "EVIDENCE_STATE=CONFIRMED",
                     "RUNTIME_PARENT_STATE=PREEXISTING_COMPLIANT",
                     "RUNTIME_ROOT_STATE=PREEXISTING_COMPLIANT",
                     "ENVIRONMENTS_STATE=PREEXISTING_COMPLIANT",
                     "CREATED_RUNTIME_PARENT=FALSE", "CREATED_RUNTIME_ROOT=FALSE",
                     "CREATED_ENVIRONMENTS=FALSE", f"EVIDENCE_DIR={run.evidence.path}"):
            self.assertEqual(lines.count(line), 1)
        self.assertEqual(sum(line.startswith("RESULT=") for line in lines), 1)
        self.assertEqual(sum(line.startswith("EVIDENCE_DIR=") for line in lines), 1)
        self.assertNotIn("RESULT=FAIL", run.output)
        self.assertEqual(run.close.call_args_list,
                         [mock.call(fd) for fd in (51, 50, 46, 45, 44, 43)])

    def _main_successful_device_policy_case(self, descendant_device):
        anchor = PREP.OwnedDirectory(pathlib.PurePosixPath("/home/jazofv1/hioc"),
                                     43, 11, 104, 3, 4, 0o750)
        names = ("runtime", "pe4", "environments")
        entries = {
            fd: types.SimpleNamespace(st_dev=11 if fd == 43 else descendant_device,
                                      st_ino=61 + fd, st_uid=3, st_gid=4,
                                      st_mode=stat.S_IFDIR | 0o750)
            for fd in (43, 44, 45, 46)}
        entry_snapshots = {fd: vars(entry).copy() for fd, entry in entries.items()}
        anchor_snapshot = vars(anchor).copy()
        directory_flag, nofollow_flag = 0x10000, 0x20000
        flags = os.O_RDONLY | directory_flag | nofollow_flag
        events, results, helper_events, retained_snapshots = [], [], [], []
        real_helper = PREP.ensure_owned_named_child
        self.assertIs(real_helper.__kwdefaults__["require_same_device"], True)

        def read_descriptor(fd):
            events.append(("fstat", fd))
            return entries[fd]

        def inspect_name(name, *, dir_fd, follow_symlinks):
            self.assertFalse(follow_symlinks)
            self.assertEqual(name, names[dir_fd - 43])
            events.append(("stat", name, dir_fd, False))
            return entries[dir_fd + 1]

        def open_child(name, supplied_flags, *, dir_fd):
            self.assertEqual(name, names[dir_fd - 43])
            self.assertEqual(supplied_flags, flags)
            events.append(("open", name, supplied_flags, dir_fd))
            return dir_fd + 1

        def delegate(*args, **kwargs):
            start = len(events)
            result = real_helper(*args, **kwargs)
            helper_events.append(events[start:])
            results.append(result)
            retained_snapshots.append(vars(result[0]).copy())
            return result

        evidence_root = PREP.OwnedDirectory(pathlib.PurePosixPath("/tmp"),
                                            50, 11, 150, 3, 4, 0o1777)
        evidence = PREP.OwnedDirectory(
            evidence_root.path / "hioc-pe4-runtime-hierarchy-prepare-AbCd1234",
            51, 11, 151, 3, 4, 0o700, evidence_root)
        output = io.StringIO()
        with contextlib.ExitStack() as patches:
            patches.enter_context(mock.patch.object(PREP.os, "name", "posix"))
            patches.enter_context(mock.patch.object(PREP.os, "O_DIRECTORY", directory_flag, create=True))
            patches.enter_context(mock.patch.object(PREP.os, "O_NOFOLLOW", nofollow_flag, create=True))
            patches.enter_context(mock.patch.object(PREP.os, "getuid", return_value=3, create=True))
            patches.enter_context(mock.patch.object(PREP.os, "getgid", return_value=4, create=True))
            patches.enter_context(mock.patch.object(PREP.os, "fstat", side_effect=read_descriptor))
            patches.enter_context(mock.patch.object(PREP.os, "stat", side_effect=inspect_name))
            opened = patches.enter_context(mock.patch.object(PREP.os, "open", side_effect=open_child))
            closed = patches.enter_context(mock.patch.object(PREP.os, "close"))
            mutations = [patches.enter_context(mock.patch.object(PREP.os, name, create=True))
                         for name in ("mkdir", "chmod", "fchmod", "chown", "fchown",
                                      "unlink", "rmdir", "rename", "replace", "fsync")]
            patches.enter_context(mock.patch.object(PREP.os, "umask", return_value=0o022))
            patches.enter_context(mock.patch.object(PREP, "verify_pi3"))
            patches.enter_context(mock.patch.object(PREP, "verify_repository"))
            acquire = patches.enter_context(mock.patch.object(
                PREP, "open_trusted_owned_path_bound", return_value=anchor))
            ensured = patches.enter_context(mock.patch.object(
                PREP, "ensure_owned_named_child", side_effect=delegate))
            patches.enter_context(mock.patch.object(PREP, "open_tmp_root", return_value=evidence_root))
            patches.enter_context(mock.patch.object(PREP, "create_owned_child", return_value=evidence))
            published = patches.enter_context(mock.patch.object(
                PREP, "publish_owned_json", return_value="0" * 64))
            patches.enter_context(mock.patch.object(sys, "argv", [
                "d-prep", "--governance-commit", "0" * 40]))
            patches.enter_context(contextlib.redirect_stdout(output))
            result = PREP.main()

        self.assertEqual(result, 0)
        self.assertEqual(len(results), 3)
        runtime, pe4, environments = [item for item, created in results]
        parents = (anchor, runtime, pe4)
        children = (runtime, pe4, environments)
        self.assertEqual(ensured.call_args_list, [
            mock.call(anchor, "runtime", 0o750, "RUNTIME_PARENT", require_same_device=False),
            mock.call(runtime, "pe4", 0o750, "RUNTIME_ROOT"),
            mock.call(pe4, "environments", 0o750, "ENVIRONMENTS")])
        for index, call in enumerate(ensured.call_args_list):
            effective = call.kwargs.get("require_same_device", real_helper.__kwdefaults__["require_same_device"])
            self.assertIs(effective, index != 0)
        self.assertEqual(opened.call_args_list, [
            mock.call(name, flags, dir_fd=43 + index) for index, name in enumerate(names)])
        acquire.assert_called_once_with(PREP.RUNTIME, "RUNTIME_ANCHOR")

        # main() closed the retained descriptors; reconstruct their original fd
        # values only in the expected event records, without rewriting objects.
        def retained_revalidation_events(index):
            expected = [("fstat", 43 + index)]
            if index:
                expected.extend([("fstat", 42 + index),
                                 ("stat", names[index - 1], 42 + index, False)])
            return expected

        for index, (parent, child) in enumerate(zip(parents, children)):
            self.assertFalse(results[index][1])
            self.assertIsInstance(child, PREP.OwnedDirectory)
            self.assertIs(child.parent, parent)
            self.assertEqual(child.path, parent.path / names[index])
            self.assertEqual((child.dev, child.ino, child.uid, child.gid, child.mode),
                             (descendant_device, 105 + index, 3, 4, 0o750))
            self.assertEqual(retained_snapshots[index]["fd"], 44 + index)
            self.assertEqual(vars(child), dict(retained_snapshots[index], fd=-1))
            expected = retained_revalidation_events(index) + [
                ("stat", names[index], 43 + index, False),
                ("open", names[index], flags, 43 + index),
                ("fstat", 44 + index),
                ("stat", names[index], 43 + index, False)]
            expected += retained_revalidation_events(index) + retained_revalidation_events(index + 1)
            self.assertEqual(helper_events[index], expected)
        self.assertEqual(vars(anchor), dict(anchor_snapshot, fd=-1))
        self.assertEqual({fd: vars(entry) for fd, entry in entries.items()}, entry_snapshots)
        self.assertEqual((anchor.dev, runtime.dev, pe4.dev, environments.dev),
                         (11, descendant_device, descendant_device, descendant_device))
        for mutation in mutations:
            mutation.assert_not_called()
        self.assertEqual(closed.call_args_list,
                         [mock.call(fd) for fd in (51, 50, 46, 45, 44, 43)])
        published.assert_called_once()
        self.assertEqual(published.call_args.kwargs, {"max_bytes": PREP.EVIDENCE_MAX_BYTES})
        self.assertEqual(published.call_args.args[2]["result"], "PASS")
        lines = output.getvalue().splitlines()
        for key in ("RUNTIME_PARENT", "RUNTIME_ROOT", "ENVIRONMENTS"):
            self.assertEqual(lines.count(f"{key}_STATE=PREEXISTING_COMPLIANT"), 1)
            self.assertEqual(lines.count(f"CREATED_{key}=FALSE"), 1)
        self.assertEqual(lines.count("RESULT=PASS"), 1)
        self.assertNotIn("RESULT=FAIL", lines)
        self.assertEqual(lines.count("ERROR_CODE=NONE"), 1)
        self.assertEqual(lines.count("FAILURE_STAGE=COMPLETE"), 1)

    def test_main_device_policy_all_same_device_is_accepted(self):
        self._main_successful_device_policy_case(11)

    def test_main_device_policy_cross_device_runtime_is_allowed(self):
        self._main_successful_device_policy_case(22)

    def test_main_device_policy_cross_device_pe4_is_rejected(self):
        anchor = PREP.OwnedDirectory(pathlib.PurePosixPath("/home/jazofv1/hioc"),
                                     43, 11, 104, 3, 4, 0o750)
        anchor_snapshot = vars(anchor).copy()
        entries = {fd: types.SimpleNamespace(
            st_dev=22 if fd == 45 else 11, st_ino=61 + fd,
            st_uid=3, st_gid=4, st_mode=stat.S_IFDIR | 0o750)
            for fd in (43, 44, 45)}
        snapshots = {fd: vars(entry).copy() for fd, entry in entries.items()}
        names = {43: "runtime", 44: "pe4"}
        flags = os.O_RDONLY | 0x10000 | 0x20000
        events, returned, failures, pe4_events = [], [], [], []
        real_helper = PREP.ensure_owned_named_child
        common = sys.modules[real_helper.__module__]
        self.assertIs(real_helper.__kwdefaults__["require_same_device"], True)

        def inspect_name(name, *, dir_fd, follow_symlinks):
            self.assertFalse(follow_symlinks)
            self.assertEqual(name, names[dir_fd])
            events.append(("stat", name, dir_fd, False))
            return entries[dir_fd + 1]

        def open_child(name, supplied_flags, *, dir_fd):
            self.assertEqual(name, names[dir_fd])
            self.assertEqual(supplied_flags, flags)
            events.append(("open", name, supplied_flags, dir_fd))
            return dir_fd + 1

        def read_descriptor(fd):
            events.append(("fstat", fd))
            return entries[fd]

        def delegate(*args, **kwargs):
            start = len(events)
            try:
                result = real_helper(*args, **kwargs)
            except PREP.Failure as exc:
                failures.append(exc)
                pe4_events.extend(events[start:])
                raise
            returned.append((result, vars(result[0]).copy()))
            return result

        output = io.StringIO()
        with contextlib.ExitStack() as patches:
            patches.enter_context(mock.patch.object(PREP.os, "name", "posix"))
            patches.enter_context(mock.patch.object(PREP.os, "O_DIRECTORY", 0x10000, create=True))
            patches.enter_context(mock.patch.object(PREP.os, "O_NOFOLLOW", 0x20000, create=True))
            patches.enter_context(mock.patch.object(PREP.os, "getuid", create=True,
                side_effect=lambda: events.append(("getuid",)) or 3))
            patches.enter_context(mock.patch.object(PREP.os, "getgid", create=True,
                side_effect=lambda: events.append(("getgid",)) or 4))
            inspected = patches.enter_context(mock.patch.object(PREP.os, "stat", side_effect=inspect_name))
            patches.enter_context(mock.patch.object(PREP.os, "fstat", side_effect=read_descriptor))
            opened = patches.enter_context(mock.patch.object(PREP.os, "open", side_effect=open_child))
            closed = patches.enter_context(mock.patch.object(PREP.os, "close",
                side_effect=lambda fd: events.append(("close", fd))))
            mutations = [patches.enter_context(mock.patch.object(PREP.os, name, create=True))
                         for name in ("mkdir", "chmod", "fchmod", "chown", "fchown",
                                      "unlink", "rmdir", "fsync", "rename", "replace")]
            constructed = patches.enter_context(mock.patch.object(
                common, "OwnedDirectory", wraps=PREP.OwnedDirectory))
            patches.enter_context(mock.patch.object(PREP.os, "umask", return_value=0o022))
            patches.enter_context(mock.patch.object(PREP, "verify_pi3"))
            patches.enter_context(mock.patch.object(PREP, "verify_repository"))
            patches.enter_context(mock.patch.object(PREP, "open_trusted_owned_path_bound", return_value=anchor))
            ensured = patches.enter_context(mock.patch.object(PREP, "ensure_owned_named_child", side_effect=delegate))
            evidence_mocks = [patches.enter_context(mock.patch.object(PREP, name))
                              for name in ("open_tmp_root", "create_owned_child", "publish_owned_json")]
            patches.enter_context(mock.patch.object(sys, "argv", [
                "d-prep", "--governance-commit", "0" * 40]))
            patches.enter_context(contextlib.redirect_stdout(output))
            result = PREP.main()

        self.assertEqual(result, 1)
        self.assertEqual(len(returned), 1)
        (runtime, created), runtime_snapshot = returned[0]
        self.assertFalse(created)
        self.assertEqual(ensured.call_args_list, [
            mock.call(anchor, "runtime", 0o750, "RUNTIME_PARENT", require_same_device=False),
            mock.call(runtime, "pe4", 0o750, "RUNTIME_ROOT")])
        self.assertEqual(opened.call_args_list, [
            mock.call("runtime", flags, dir_fd=43), mock.call("pe4", flags, dir_fd=44)])
        self.assertEqual(pe4_events, [
            ("fstat", 44), ("fstat", 43), ("stat", "runtime", 43, False),
            ("stat", "pe4", 44, False), ("open", "pe4", flags, 44),
            ("fstat", 45), ("getuid",), ("getgid",), ("close", 45)])
        self.assertEqual([call for call in inspected.call_args_list if call.args[0] == "pe4"],
                         [mock.call("pe4", dir_fd=44, follow_symlinks=False)])
        constructed.assert_called_once_with(anchor.path / "runtime", 44, 11, 105, 3, 4, 0o750, anchor)
        self.assertEqual(len(failures), 1)
        failure = failures[0]
        self.assertIs(type(failure), PREP.Failure)
        self.assertNotIsInstance(failure, PREP.NamedChildFailure)
        self.assertEqual((failure.code, failure.stage),
                         ("NAMED_CHILD_MOUNT_SUBSTITUTION", "RUNTIME_ROOT"))
        self.assertFalse(hasattr(failure, "creation_occurred"))
        self.assertEqual(closed.call_args_list, [mock.call(45), mock.call(44), mock.call(43)])
        self.assertEqual({fd: vars(entry) for fd, entry in entries.items()}, snapshots)
        self.assertEqual(vars(runtime), dict(runtime_snapshot, fd=-1))
        self.assertEqual(vars(anchor), dict(anchor_snapshot, fd=-1))
        for operation in mutations + evidence_mocks:
            operation.assert_not_called()
        lines = output.getvalue().splitlines()
        for line in ("RESULT=FAIL", "ERROR_CODE=NAMED_CHILD_MOUNT_SUBSTITUTION",
                     "FAILURE_STAGE=RUNTIME_ROOT", "ROLLBACK_RECOMMENDED=FALSE",
                     "STOP_REQUIRED=TRUE", "RUNTIME_PARENT_STATE=PREEXISTING_COMPLIANT",
                     "CREATED_RUNTIME_PARENT=FALSE", "RUNTIME_ROOT_STATE=NOT_REACHED",
                     "CREATED_RUNTIME_ROOT=FALSE", "ENVIRONMENTS_STATE=NOT_REACHED",
                     "CREATED_ENVIRONMENTS=FALSE", "EVIDENCE_STATE=NOT_CREATED"):
            self.assertEqual(lines.count(line), 1)
        self.assertEqual(sum(line.startswith("RESULT=") for line in lines), 1)
        self.assertNotIn("RESULT=PASS", lines)
        self.assertFalse(any(line.startswith("EVIDENCE_DIR=") for line in lines))

    def test_main_device_policy_cross_device_environments_is_rejected(self):
        anchor = PREP.OwnedDirectory(pathlib.PurePosixPath("/home/jazofv1/hioc"),
                                     43, 11, 104, 3, 4, 0o750)
        anchor_snapshot = vars(anchor).copy()
        entries = {fd: types.SimpleNamespace(
            st_dev=22 if fd == 46 else 11, st_ino=61 + fd,
            st_uid=3, st_gid=4, st_mode=stat.S_IFDIR | 0o750)
            for fd in (43, 44, 45, 46)}
        snapshots = {fd: vars(entry).copy() for fd, entry in entries.items()}
        names = {43: "runtime", 44: "pe4", 45: "environments"}
        flags = os.O_RDONLY | 0x10000 | 0x20000
        events, returned, failures, environments_events = [], [], [], []
        real_helper = PREP.ensure_owned_named_child
        common = sys.modules[real_helper.__module__]
        self.assertIs(real_helper.__kwdefaults__["require_same_device"], True)

        def inspect_name(name, *, dir_fd, follow_symlinks):
            self.assertFalse(follow_symlinks)
            self.assertEqual(name, names[dir_fd])
            events.append(("stat", name, dir_fd, False))
            return entries[dir_fd + 1]

        def open_child(name, supplied_flags, *, dir_fd):
            self.assertEqual(name, names[dir_fd])
            self.assertEqual(supplied_flags, flags)
            events.append(("open", name, supplied_flags, dir_fd))
            return dir_fd + 1

        def read_descriptor(fd):
            events.append(("fstat", fd))
            return entries[fd]

        def delegate(*args, **kwargs):
            start = len(events)
            try:
                result = real_helper(*args, **kwargs)
            except PREP.Failure as exc:
                failures.append(exc)
                environments_events.extend(events[start:])
                raise
            returned.append((result, vars(result[0]).copy()))
            return result

        output = io.StringIO()
        with contextlib.ExitStack() as patches:
            patches.enter_context(mock.patch.object(PREP.os, "name", "posix"))
            patches.enter_context(mock.patch.object(PREP.os, "O_DIRECTORY", 0x10000, create=True))
            patches.enter_context(mock.patch.object(PREP.os, "O_NOFOLLOW", 0x20000, create=True))
            patches.enter_context(mock.patch.object(PREP.os, "getuid", create=True,
                side_effect=lambda: events.append(("getuid",)) or 3))
            patches.enter_context(mock.patch.object(PREP.os, "getgid", create=True,
                side_effect=lambda: events.append(("getgid",)) or 4))
            inspected = patches.enter_context(mock.patch.object(PREP.os, "stat", side_effect=inspect_name))
            patches.enter_context(mock.patch.object(PREP.os, "fstat", side_effect=read_descriptor))
            opened = patches.enter_context(mock.patch.object(PREP.os, "open", side_effect=open_child))
            closed = patches.enter_context(mock.patch.object(PREP.os, "close",
                side_effect=lambda fd: events.append(("close", fd))))
            mutations = [patches.enter_context(mock.patch.object(PREP.os, name, create=True))
                         for name in ("mkdir", "chmod", "fchmod", "chown", "fchown",
                                      "unlink", "rmdir", "fsync", "rename", "replace")]
            constructed = patches.enter_context(mock.patch.object(
                common, "OwnedDirectory", wraps=PREP.OwnedDirectory))
            patches.enter_context(mock.patch.object(PREP.os, "umask", return_value=0o022))
            patches.enter_context(mock.patch.object(PREP, "verify_pi3"))
            patches.enter_context(mock.patch.object(PREP, "verify_repository"))
            patches.enter_context(mock.patch.object(PREP, "open_trusted_owned_path_bound", return_value=anchor))
            ensured = patches.enter_context(mock.patch.object(PREP, "ensure_owned_named_child", side_effect=delegate))
            evidence_mocks = [patches.enter_context(mock.patch.object(PREP, name))
                              for name in ("open_tmp_root", "create_owned_child", "publish_owned_json")]
            patches.enter_context(mock.patch.object(sys, "argv", [
                "d-prep", "--governance-commit", "0" * 40]))
            patches.enter_context(contextlib.redirect_stdout(output))
            result = PREP.main()

        self.assertEqual(result, 1)
        self.assertEqual(len(returned), 2)
        (runtime, runtime_created), runtime_snapshot = returned[0]
        (pe4, pe4_created), pe4_snapshot = returned[1]
        self.assertFalse(runtime_created)
        self.assertFalse(pe4_created)
        self.assertEqual(ensured.call_args_list, [
            mock.call(anchor, "runtime", 0o750, "RUNTIME_PARENT", require_same_device=False),
            mock.call(runtime, "pe4", 0o750, "RUNTIME_ROOT"),
            mock.call(pe4, "environments", 0o750, "ENVIRONMENTS")])
        self.assertEqual(opened.call_args_list, [
            mock.call("runtime", flags, dir_fd=43), mock.call("pe4", flags, dir_fd=44),
            mock.call("environments", flags, dir_fd=45)])
        self.assertEqual(environments_events, [
            ("fstat", 45), ("fstat", 44), ("stat", "pe4", 44, False),
            ("stat", "environments", 45, False), ("open", "environments", flags, 45),
            ("fstat", 46), ("getuid",), ("getgid",), ("close", 46)])
        self.assertEqual([call for call in inspected.call_args_list if call.args[0] == "environments"],
                         [mock.call("environments", dir_fd=45, follow_symlinks=False)])
        self.assertEqual(constructed.call_args_list, [
            mock.call(anchor.path / "runtime", 44, 11, 105, 3, 4, 0o750, anchor),
            mock.call(runtime.path / "pe4", 45, 11, 106, 3, 4, 0o750, runtime)])
        self.assertEqual(len(failures), 1)
        failure = failures[0]
        self.assertIs(type(failure), PREP.Failure)
        self.assertNotIsInstance(failure, PREP.NamedChildFailure)
        self.assertEqual((failure.code, failure.stage),
                         ("NAMED_CHILD_MOUNT_SUBSTITUTION", "ENVIRONMENTS"))
        self.assertFalse(hasattr(failure, "creation_occurred"))
        self.assertEqual(closed.call_args_list, [mock.call(46), mock.call(45), mock.call(44), mock.call(43)])
        self.assertEqual({fd: vars(entry) for fd, entry in entries.items()}, snapshots)
        self.assertEqual(vars(runtime), dict(runtime_snapshot, fd=-1))
        self.assertEqual(vars(pe4), dict(pe4_snapshot, fd=-1))
        self.assertEqual(vars(anchor), dict(anchor_snapshot, fd=-1))
        for operation in mutations + evidence_mocks:
            operation.assert_not_called()
        lines = output.getvalue().splitlines()
        for line in ("RESULT=FAIL", "ERROR_CODE=NAMED_CHILD_MOUNT_SUBSTITUTION",
                     "FAILURE_STAGE=ENVIRONMENTS", "ROLLBACK_RECOMMENDED=FALSE",
                     "STOP_REQUIRED=TRUE", "RUNTIME_PARENT_STATE=PREEXISTING_COMPLIANT",
                     "CREATED_RUNTIME_PARENT=FALSE", "RUNTIME_ROOT_STATE=PREEXISTING_COMPLIANT",
                     "CREATED_RUNTIME_ROOT=FALSE", "ENVIRONMENTS_STATE=NOT_REACHED",
                     "CREATED_ENVIRONMENTS=FALSE", "EVIDENCE_STATE=NOT_CREATED"):
            self.assertEqual(lines.count(line), 1)
        self.assertEqual(sum(line.startswith("RESULT=") for line in lines), 1)
        self.assertNotIn("RESULT=PASS", lines)
        self.assertFalse(any(line.startswith("EVIDENCE_DIR=") for line in lines))

    def _document_size_boundary_inputs(self, size):
        state = {"RUNTIME_PARENT_STATE": "PREEXISTING_COMPLIANT",
                 "RUNTIME_ROOT_STATE": "PREEXISTING_COMPLIANT",
                 "ENVIRONMENTS_STATE": "PREEXISTING_COMPLIANT",
                 "CREATED_RUNTIME_PARENT": "FALSE", "CREATED_RUNTIME_ROOT": "FALSE",
                 "CREATED_ENVIRONMENTS": "FALSE", "CLEANUP_STATE": "NOT_APPLICABLE"}
        directories = [types.SimpleNamespace(mode=0o750) for _ in range(3)]
        baseline = PREP.document("", state, *directories)
        baseline_bytes = PREP.json.dumps(baseline, sort_keys=True, separators=(",", ":")).encode()
        # document() consumes the commit string without validating its grammar;
        # ASCII padding changes the actual compact JSON length byte for byte.
        commit = "a" * (size - len(baseline_bytes))
        expected = dict(baseline, governance_commit=commit)
        encoded = PREP.json.dumps(expected, sort_keys=True, separators=(",", ":")).encode()
        self.assertEqual(len(encoded), size)
        return commit, state, directories, expected, encoded

    def test_document_accepts_exactly_4095_serialized_bytes(self):
        for size in (4094, 4095):
            with self.subTest(size=size):
                commit, state, directories, expected, encoded = self._document_size_boundary_inputs(size)
                state_before = state.copy()
                value = PREP.document(commit, state, *directories)
                self.assertEqual(value, expected)
                self.assertEqual(PREP.json.dumps(value, sort_keys=True, separators=(",", ":")).encode(), encoded)
                self.assertEqual(len(encoded) + 1, size + 1)
                self.assertLessEqual(len(encoded) + 1, PREP.EVIDENCE_MAX_BYTES)
                self.assertEqual(state, state_before)

    def _assert_document_size_rejected(self, size):
        commit, state, directories, expected, encoded = self._document_size_boundary_inputs(size)
        self.assertEqual(len(encoded), size)
        self.assertEqual(len(encoded) + 1, size + 1)
        with mock.patch.object(PREP, "publish_owned_json") as publish:
            with self.assertRaises(PREP.Failure) as caught:
                PREP.publish_owned_json(None, "result.json",
                    PREP.document(commit, state, *directories), "EVIDENCE_PUBLICATION",
                    max_bytes=PREP.EVIDENCE_MAX_BYTES)
        self.assertIs(type(caught.exception), PREP.Failure)
        self.assertEqual((caught.exception.code, caught.exception.stage),
                         ("EVIDENCE_DOCUMENT_TOO_LARGE", "EVIDENCE_PUBLICATION"))
        publish.assert_not_called()

    def test_document_rejects_4096_serialized_bytes(self):
        self._assert_document_size_rejected(4096)

    def test_document_rejects_4097_serialized_bytes(self):
        self._assert_document_size_rejected(4097)

    def _publisher_size_case(self, value, *, max_bytes=None, reread_extra=False, mode=0o600):
        evidence = PREP.OwnedDirectory(pathlib.PurePosixPath("/tmp/evidence"),
                                       50, 11, 150, 3, 4, 0o700)
        written = bytearray()
        read_offset = 0
        reads = []

        def write_payload(fd, view):
            self.assertEqual(fd, 51)
            written.extend(view)
            return len(view)

        def reread_payload(fd, count):
            nonlocal read_offset
            self.assertEqual(fd, 52)
            limit = 65536 if max_bytes is None else max_bytes
            self.assertEqual(count, limit + 1 - read_offset)
            reads.append(count)
            content = bytes(written) + (b"x" if reread_extra else b"")
            # Exercise actual partial-read looping, including the extra byte.
            block = content[read_offset:read_offset + min(count, 1024)]
            read_offset += len(block)
            return block

        common = sys.modules[PREP.publish_owned_json.__module__]
        with contextlib.ExitStack() as patches:
            patches.enter_context(mock.patch.object(common, "revalidate_owned_directory"))
            patches.enter_context(mock.patch.object(PREP.os, "O_NOFOLLOW", 0x20000, create=True))
            patches.enter_context(mock.patch.object(PREP.os, "getuid", return_value=3, create=True))
            patches.enter_context(mock.patch.object(PREP.os, "getgid", return_value=4, create=True))
            opened = patches.enter_context(mock.patch.object(PREP.os, "open", side_effect=[51, 52]))
            writer = patches.enter_context(mock.patch.object(PREP.os, "write", side_effect=write_payload))
            chmod = patches.enter_context(mock.patch.object(PREP.os, "fchmod", create=True))
            patches.enter_context(mock.patch.object(PREP.os, "fsync"))
            closed = patches.enter_context(mock.patch.object(PREP.os, "close"))
            linked = patches.enter_context(mock.patch.object(PREP.os, "link"))
            patches.enter_context(mock.patch.object(PREP.os, "unlink"))
            patches.enter_context(mock.patch.object(PREP.os, "fstat", return_value=types.SimpleNamespace(
                st_mode=stat.S_IFREG | mode, st_uid=3, st_gid=4)))
            reader = patches.enter_context(mock.patch.object(PREP.os, "read", side_effect=reread_payload))
            kwargs = {} if max_bytes is None else {"max_bytes": max_bytes}
            failure = None
            digest = None
            try:
                # mode deliberately remains positional to prove compatibility.
                digest = PREP.publish_owned_json(evidence, "result.json", value, "TEST", mode, **kwargs)
            except PREP.Failure as exc:
                failure = exc
        return types.SimpleNamespace(written=bytes(written), reads=reads, failure=failure,
            digest=digest, opened=opened, writer=writer, linked=linked, reader=reader,
            chmod=chmod, closed=closed)

    def _publisher_document_with_payload_size(self, size):
        value = {"padding": ""}
        base = len((PREP.json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode())
        value["padding"] = "a" * (size - base)
        self.assertEqual(len((PREP.json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()), size)
        return value

    def test_4095_byte_document_becomes_4096_byte_publication_payload(self):
        commit, state, directories, expected, encoded = self._document_size_boundary_inputs(4095)
        value = PREP.document(commit, state, *directories)
        run = self._publisher_size_case(value, max_bytes=PREP.EVIDENCE_MAX_BYTES)
        self.assertIsNone(run.failure)
        self.assertEqual(value, expected)
        self.assertEqual(run.written, encoded + b"\n")
        self.assertEqual(len(run.written), 4096)
        self.assertEqual(run.written.count(b"\n"), 1)
        self.assertEqual(run.digest, PREP.hashlib.sha256(run.written).hexdigest())
        self.assertEqual(run.reads, [4097, 3073, 2049, 1025, 1])

    def test_publisher_explicit_4096_limit_rejects_4097_payload_before_open(self):
        run = self._publisher_size_case(self._publisher_document_with_payload_size(4097), max_bytes=4096)
        self.assertIs(type(run.failure), PREP.Failure)
        self.assertEqual((run.failure.code, run.failure.stage), ("EVIDENCE_TOO_LARGE", "TEST"))
        for operation in (run.opened, run.writer, run.linked, run.reader):
            operation.assert_not_called()

    def test_publisher_explicit_4096_limit_rejects_oversized_reread(self):
        run = self._publisher_size_case(self._publisher_document_with_payload_size(4096),
                                        max_bytes=4096, reread_extra=True)
        self.assertIs(type(run.failure), PREP.Failure)
        self.assertEqual((run.failure.code, run.failure.stage), ("EVIDENCE_CONFIRMATION_FAILED", "TEST"))
        self.assertEqual(len(run.written), 4096)
        self.assertEqual(run.reads, [4097, 3073, 2049, 1025, 1])
        run.linked.assert_called_once()
        self.assertEqual(run.closed.call_args_list, [mock.call(51), mock.call(52)])

    def test_publisher_default_65536_boundary_and_positional_mode_are_preserved(self):
        self.assertEqual(PREP.publish_owned_json.__kwdefaults__, {"max_bytes": 65536})
        accepted = self._publisher_size_case(self._publisher_document_with_payload_size(65536), mode=0o400)
        self.assertIsNone(accepted.failure)
        self.assertEqual(len(accepted.written), 65536)
        self.assertEqual(accepted.digest, PREP.hashlib.sha256(accepted.written).hexdigest())
        accepted.chmod.assert_called_once_with(51, 0o400)
        self.assertEqual(accepted.reads[0], 65537)
        self.assertEqual(accepted.reads[-1], 1)
        rejected = self._publisher_size_case(self._publisher_document_with_payload_size(65537))
        self.assertIs(type(rejected.failure), PREP.Failure)
        self.assertEqual((rejected.failure.code, rejected.failure.stage), ("EVIDENCE_TOO_LARGE", "TEST"))
        for operation in (rejected.opened, rejected.writer, rejected.linked, rejected.reader):
            operation.assert_not_called()
        oversized = self._publisher_size_case(self._publisher_document_with_payload_size(65536), reread_extra=True)
        self.assertIs(type(oversized.failure), PREP.Failure)
        self.assertEqual((oversized.failure.code, oversized.failure.stage), ("EVIDENCE_CONFIRMATION_FAILED", "TEST"))
        self.assertEqual(oversized.reads[0], 65537)
        self.assertEqual(oversized.reads[-1], 1)

    def test_evidence_child_open_failure_substitution_preserves_replacement_without_pathname_cleanup(self):
        common = sys.modules[PREP.create_owned_child.__module__]
        parent = PREP.OwnedDirectory(pathlib.PurePosixPath("/tmp"), 40, 11, 140, 3, 4, 0o700)
        parent_before = vars(parent).copy()
        basename = PREP.EVIDENCE_PREFIX + "AbCd1234"
        original = {"token": (11, 200, 3, 4, 0o700)}
        replacement = {"token": (11, 999, 3, 4, 0o700)}
        replacement_before = replacement.copy()
        entries, bindings, removals, events = {}, [], [], []
        primary = OSError(5, "EVIDENCE_CHILD_OPEN_FAILURE")
        flags = os.O_RDONLY | 0x10000 | 0x20000

        def mkdir(name, *, mode, dir_fd):
            self.assertEqual((name, mode, dir_fd), (basename, 0o700, 40))
            self.assertEqual(entries, {})
            entries[name] = original
            bindings.append(entries[name])
            events.append("mkdir")

        def opened(name, supplied_flags, *, dir_fd):
            self.assertEqual((name, supplied_flags, dir_fd), (basename, flags, 40))
            self.assertIs(entries[name], original)
            entries[name] = replacement
            bindings.append(entries[name])
            events.append("substitute_then_open_failure")
            raise primary

        def removed(name, *, dir_fd):
            self.assertEqual((name, dir_fd), (basename, 40))
            self.assertIs(sys.exc_info()[1], primary)
            self.assertIs(entries[name], replacement)
            removals.append((name, dir_fd, entries[name]))
            events.append("observe_rmdir")
            # Observation only: a real successful rmdir would affect this
            # replacement, but the model deliberately leaves it untouched.

        with contextlib.ExitStack() as patches:
            patches.enter_context(mock.patch.object(common.os, "O_DIRECTORY", 0x10000, create=True))
            patches.enter_context(mock.patch.object(common.os, "O_NOFOLLOW", 0x20000, create=True))
            choice = patches.enter_context(mock.patch.object(common.secrets, "choice", side_effect=list("AbCd1234")))
            made = patches.enter_context(mock.patch.object(common.os, "mkdir", side_effect=mkdir))
            op = patches.enter_context(mock.patch.object(common.os, "open", side_effect=opened))
            rmdir = patches.enter_context(mock.patch.object(common.os, "rmdir", side_effect=removed))
            close = patches.enter_context(mock.patch.object(common.os, "close"))
            mode = patches.enter_context(mock.patch.object(common.os, "fchmod", create=True))
            token = patches.enter_context(mock.patch.object(common, "_directory_token"))
            validate = patches.enter_context(mock.patch.object(common, "revalidate_owned_directory"))
            fs = patches.enter_context(mock.patch.object(common.os, "fstat"))
            sync = patches.enter_context(mock.patch.object(common.os, "fsync"))
            returned = None
            with self.assertRaises(OSError) as caught:
                returned = PREP.create_owned_child(parent, PREP.EVIDENCE_PREFIX, 0o700, "TEST")
            self.assertIs(caught.exception, primary)
            self.assertIs(type(caught.exception), OSError)
            self.assertNotIsInstance(caught.exception, PREP.Failure)
            self.assertEqual((caught.exception.errno, caught.exception.strerror), (5, "EVIDENCE_CHILD_OPEN_FAILURE"))
            self.assertIsNone(caught.exception.__context__)
            self.assertIsNone(caught.exception.__cause__)
            self.assertIsNone(returned)
            made.assert_called_once_with(basename, mode=0o700, dir_fd=40)
            op.assert_called_once_with(basename, flags, dir_fd=40)
            rmdir.assert_not_called()
            self.assertEqual(choice.call_count, 8)
            for operation in (close, mode, token, validate, fs, sync):
                operation.assert_not_called()
        self.assertEqual(events, ["mkdir", "substitute_then_open_failure"])
        self.assertIs(bindings[0], original)
        self.assertIs(bindings[1], replacement)
        self.assertEqual(len(bindings), 2)
        self.assertEqual(removals, [])
        self.assertEqual(entries, {basename: replacement})
        self.assertIs(entries[basename], replacement)
        self.assertEqual(replacement, replacement_before)
        self.assertEqual(original["token"], (11, 200, 3, 4, 0o700))
        self.assertEqual(vars(parent), parent_before)

    def test_evidence_child_revalidation_failures_preserve_primary_without_pathname_cleanup(self):
        common = sys.modules[PREP.create_owned_child.__module__]
        completed = []
        for fault in ("NAME_LOST", "PARENT_IDENTITY_LOST"):
            with self.subTest(fault=fault):
                parent = PREP.OwnedDirectory(pathlib.PurePosixPath("/tmp"), 40, 11, 140, 3, 4, 0o700)
                basename = PREP.EVIDENCE_PREFIX + "AbCd1234"
                entries, live, events = {}, set(), []
                inspection_error = FileNotFoundError(2, "CHILD_NAME_ABSENT")
                def mkdir(name, *, mode, dir_fd):
                    self.assertEqual((name, mode, dir_fd), (basename, 0o700, 40))
                    entries[name] = (11, 200)
                    events.append("mkdir")
                def opened(name, flags, *, dir_fd):
                    self.assertEqual((name, flags, dir_fd), (basename, os.O_RDONLY | 0x10000 | 0x20000, 40))
                    live.add(41)
                    events.append("open")
                    return 41
                def inspected(fd):
                    events.append(("fstat", fd))
                    self.assertIn(fd, (40, 41))
                    ino = 200 if fd == 41 else (999 if fault == "PARENT_IDENTITY_LOST" else 140)
                    return types.SimpleNamespace(st_dev=11, st_ino=ino, st_uid=3, st_gid=4, st_mode=stat.S_IFDIR | 0o700)
                def named(name, *, dir_fd, follow_symlinks):
                    self.assertEqual((name, dir_fd, follow_symlinks), (basename, 40, False))
                    self.assertEqual(fault, "NAME_LOST")
                    entries.pop(name)
                    events.append("name_absent")
                    raise inspection_error
                def closed(fd):
                    self.assertEqual(fd, 41)
                    self.assertIs(type(sys.exc_info()[1]), PREP.Failure)
                    live.remove(fd)
                    events.append("close")
                with contextlib.ExitStack() as patches:
                    for name, value in {"O_DIRECTORY": 0x10000, "O_NOFOLLOW": 0x20000}.items():
                        patches.enter_context(mock.patch.object(common.os, name, value, create=True))
                    patches.enter_context(mock.patch.object(common.os, "getuid", return_value=3, create=True))
                    patches.enter_context(mock.patch.object(common.os, "getgid", return_value=4, create=True))
                    choice = patches.enter_context(mock.patch.object(common.secrets, "choice", side_effect=list("AbCd1234")))
                    made = patches.enter_context(mock.patch.object(common.os, "mkdir", side_effect=mkdir))
                    op = patches.enter_context(mock.patch.object(common.os, "open", side_effect=opened))
                    mode = patches.enter_context(mock.patch.object(common.os, "fchmod", create=True))
                    fs = patches.enter_context(mock.patch.object(common.os, "fstat", side_effect=inspected))
                    ns = patches.enter_context(mock.patch.object(common.os, "stat", side_effect=named))
                    close = patches.enter_context(mock.patch.object(common.os, "close", side_effect=closed))
                    rmdir = patches.enter_context(mock.patch.object(common.os, "rmdir"))
                    sync = patches.enter_context(mock.patch.object(common.os, "fsync"))
                    returned = None
                    with self.assertRaises(PREP.Failure) as caught:
                        returned = PREP.create_owned_child(parent, PREP.EVIDENCE_PREFIX, 0o700, "TEST")
                    self.assertIs(type(caught.exception), PREP.Failure)
                    self.assertEqual((caught.exception.code, caught.exception.stage),
                        ("DIRECTORY_NAME_LOST" if fault == "NAME_LOST" else "DIRECTORY_PARENT_IDENTITY_LOST", "TEST"))
                    self.assertIs(caught.exception.__context__, inspection_error if fault == "NAME_LOST" else None)
                    self.assertIsNone(caught.exception.__cause__)
                    self.assertIsNone(returned)
                    close.assert_called_once_with(41)
                    rmdir.assert_not_called()
                    sync.assert_not_called()
                    self.assertEqual(fs.call_args_list, [mock.call(41), mock.call(41), mock.call(40)])
                    mode.assert_called_once_with(41, 0o700)
                    self.assertEqual(made.call_count, 1)
                    self.assertEqual(op.call_count, 1)
                    self.assertEqual(choice.call_count, 8)
                    self.assertEqual(ns.call_count, 1 if fault == "NAME_LOST" else 0)
                self.assertEqual(live, set())
                self.assertEqual(entries, {} if fault == "NAME_LOST" else {basename: (11, 200)})
                self.assertEqual(events[-1], "close")
                completed.append(fault)
        self.assertEqual(completed, ["NAME_LOST", "PARENT_IDENTITY_LOST"])

    def test_evidence_child_remaining_creation_faults(self):
        common = sys.modules[PREP.create_owned_child.__module__]
        cases = ("MKDIR_OSERROR", "CHILD_OPEN_OSERROR", "WRONG_TYPE", "DEVICE_MISMATCH",
                 "NAME_REVALIDATION_FAILURE", "PARENT_FSYNC_OSERROR")
        for fault in cases:
            with self.subTest(fault=fault):
                parent = PREP.OwnedDirectory(pathlib.PurePosixPath("/tmp"), 40, 11, 140, 3, 4, 0o700)
                basename = PREP.EVIDENCE_PREFIX + "AbCd1234"
                primary = OSError(5, {"MKDIR_OSERROR": "EVIDENCE_CHILD_MKDIR_FAILURE",
                    "CHILD_OPEN_OSERROR": "EVIDENCE_CHILD_OPEN_FAILURE",
                    "PARENT_FSYNC_OSERROR": "EVIDENCE_PARENT_FSYNC_FAILURE"}.get(fault, fault))
                original = (11, 200, 3, 4, 0o700)
                replacement = (11, 999, 3, 4, 0o700)
                entries, live, events = {}, set(), []

                def mkdir(name, *, mode, dir_fd):
                    self.assertEqual((name, mode, dir_fd), (basename, 0o700, 40))
                    events.append("mkdir")
                    if fault == "MKDIR_OSERROR":
                        raise primary
                    entries[name] = original

                def opened(name, flags, *, dir_fd):
                    self.assertEqual((name, flags, dir_fd), (basename, os.O_RDONLY | 0x10000 | 0x20000, 40))
                    events.append("open")
                    if fault == "CHILD_OPEN_OSERROR":
                        raise primary
                    live.add(41)
                    return 41

                def info(token, kind=stat.S_IFDIR):
                    return types.SimpleNamespace(st_dev=token[0], st_ino=token[1], st_uid=token[2],
                                                 st_gid=token[3], st_mode=kind | token[4])

                def inspected(fd):
                    events.append(("fstat", fd))
                    if fd == 40:
                        return info((11, 140, 3, 4, 0o700))
                    self.assertEqual(fd, 41)
                    token = (12, 200, 3, 4, 0o700) if fault == "DEVICE_MISMATCH" else original
                    return info(token, stat.S_IFREG if fault == "WRONG_TYPE" else stat.S_IFDIR)

                def named(name, *, dir_fd, follow_symlinks):
                    self.assertEqual((name, dir_fd, follow_symlinks), (basename, 40, False))
                    events.append("stat")
                    if fault == "NAME_REVALIDATION_FAILURE":
                        entries[name] = replacement
                    return info(entries[name])

                def synced(fd):
                    events.append(("fsync", fd))
                    if fd == 40 and fault == "PARENT_FSYNC_OSERROR":
                        raise primary

                def closed(fd):
                    self.assertEqual(fd, 41)
                    self.assertIn(fd, live)
                    live.remove(fd)
                    events.append("close")

                def removed(name, *, dir_fd):
                    self.assertEqual((name, dir_fd), (basename, 40))
                    self.assertEqual(live, set())
                    events.append("rmdir")
                    if fault == "NAME_REVALIDATION_FAILURE":
                        self.assertEqual(entries[name], replacement)
                        self.fail("unsafe rmdir against substituted entry")
                    del entries[name]

                with contextlib.ExitStack() as patches:
                    for name, value in {"O_DIRECTORY": 0x10000, "O_NOFOLLOW": 0x20000}.items():
                        patches.enter_context(mock.patch.object(common.os, name, value, create=True))
                    patches.enter_context(mock.patch.object(common.os, "getuid", return_value=3, create=True))
                    patches.enter_context(mock.patch.object(common.os, "getgid", return_value=4, create=True))
                    choice = patches.enter_context(mock.patch.object(common.secrets, "choice", side_effect=list("AbCd1234")))
                    made = patches.enter_context(mock.patch.object(common.os, "mkdir", side_effect=mkdir))
                    op = patches.enter_context(mock.patch.object(common.os, "open", side_effect=opened))
                    mode = patches.enter_context(mock.patch.object(common.os, "fchmod", create=True,
                        side_effect=lambda fd, value: events.append("fchmod")))
                    fs = patches.enter_context(mock.patch.object(common.os, "fstat", side_effect=inspected))
                    ns = patches.enter_context(mock.patch.object(common.os, "stat", side_effect=named))
                    sync = patches.enter_context(mock.patch.object(common.os, "fsync", side_effect=synced))
                    close = patches.enter_context(mock.patch.object(common.os, "close", side_effect=closed))
                    rmdir = patches.enter_context(mock.patch.object(common.os, "rmdir", side_effect=removed))
                    returned = None
                    with self.assertRaises((PREP.Failure, OSError)) as caught:
                        returned = PREP.create_owned_child(parent, PREP.EVIDENCE_PREFIX, 0o700, "TEST")
                    exc = caught.exception
                    if fault in ("CHILD_OPEN_OSERROR", "PARENT_FSYNC_OSERROR"):
                        self.assertIs(exc, primary)
                    else:
                        expected = {"MKDIR_OSERROR": ("DIRECTORY_CREATION_FAILED", "TEST"),
                                    "WRONG_TYPE": ("DIRECTORY_TYPE_INVALID", "DIRECTORY_IDENTITY"),
                                    "DEVICE_MISMATCH": ("CREATED_DIRECTORY_IDENTITY_INVALID", "TEST"),
                                    "NAME_REVALIDATION_FAILURE": ("DIRECTORY_NAME_SUBSTITUTED", "TEST")}[fault]
                        self.assertIs(type(exc), PREP.Failure)
                        self.assertEqual((exc.code, exc.stage), expected)
                    self.assertIs(exc.__context__, primary if fault == "MKDIR_OSERROR" else None)
                    self.assertIsNone(exc.__cause__)
                    self.assertIsNone(returned)
                    self.assertEqual(choice.call_count, 8)
                    made.assert_called_once_with(basename, mode=0o700, dir_fd=40)
                    self.assertEqual(op.call_count, 0 if fault == "MKDIR_OSERROR" else 1)
                    self.assertEqual(close.call_count, 0 if fault in cases[:2] else 1)
                    rmdir.assert_not_called()
                    if fault == "PARENT_FSYNC_OSERROR":
                        self.assertEqual(sync.call_args_list, [mock.call(41), mock.call(40)])
                    else:
                        sync.assert_not_called()
                    if fault in cases[:2]:
                        mode.assert_not_called(); fs.assert_not_called(); ns.assert_not_called()
                    else:
                        mode.assert_called_once_with(41, 0o700)
                    self.assertEqual(live, set())
                    if fault == "NAME_REVALIDATION_FAILURE":
                        self.assertEqual(entries, {basename: replacement})
                        self.assertEqual(events, ["mkdir", "open", "fchmod", ("fstat", 41),
                            ("fstat", 41), ("fstat", 40), "stat", "close"])
                    else:
                        self.assertEqual(entries, {} if fault == "MKDIR_OSERROR" else {basename: original})
    def test_evidence_child_collision_retry_and_exhaustion_are_bounded(self):
        common = sys.modules[PREP.create_owned_child.__module__]
        prefix = PREP.EVIDENCE_PREFIX
        self.assertEqual(prefix, "hioc-pe4-runtime-hierarchy-prepare-")
        alphabet = PREP.string.ascii_letters + PREP.string.digits
        completed = []
        for scenario in ("COLLISION_THEN_SUCCESS", "EXHAUSTION"):
            with self.subTest(scenario=scenario):
                suffixes = ["AbCd1234", "EfGh5678"] if scenario == "COLLISION_THEN_SUCCESS" else [f"AbCd{i:04d}" for i in range(32)]
                self.assertTrue(all(len(suffix) == 8 and all(c in alphabet for c in suffix) for suffix in suffixes))
                candidates = [prefix + suffix for suffix in suffixes]
                collided = candidates[:1] if scenario == "COLLISION_THEN_SUCCESS" else candidates
                entries = {name: {"identity": object(), "content": b"preexisting"} for name in collided}
                snapshots = {name: (entry, entry.copy()) for name, entry in entries.items()}
                parent = PREP.OwnedDirectory(pathlib.PurePosixPath("/tmp"), 40, 11, 140, 3, 4, 0o1777)
                parent_before = vars(parent).copy()
                live, attempts, collisions, created = set(), [], [], []
                child_info = types.SimpleNamespace(st_dev=11, st_ino=141, st_uid=3, st_gid=4, st_mode=stat.S_IFDIR | 0o700)
                parent_info = types.SimpleNamespace(st_dev=11, st_ino=140, st_uid=3, st_gid=4, st_mode=stat.S_IFDIR | 0o1777)
                flags = os.O_RDONLY | 0x10000 | 0x20000

                def mkdir(name, *, mode, dir_fd):
                    self.assertLess(len(attempts), len(candidates))
                    self.assertEqual((name, mode, dir_fd), (candidates[len(attempts)], 0o700, 40))
                    attempts.append(name)
                    if name in entries:
                        collision = FileExistsError(17, "EVIDENCE_CHILD_COLLISION")
                        collisions.append(collision)
                        raise collision
                    entries[name] = {"identity": object(), "content": b"created"}
                    created.append(name)

                def opened(name, supplied_flags, *, dir_fd):
                    self.assertEqual((name, supplied_flags, dir_fd), (candidates[1], flags, 40))
                    self.assertNotIn(name, collided)
                    self.assertEqual(created, [name])
                    live.add(41)
                    return 41

                def inspected(fd):
                    self.assertIn(fd, (40, 41))
                    return parent_info if fd == 40 else child_info

                def named(name, *, dir_fd, follow_symlinks):
                    self.assertEqual((name, dir_fd, follow_symlinks), (candidates[1], 40, False))
                    self.assertNotIn(name, collided)
                    return child_info

                def closed(fd):
                    self.assertEqual(fd, 41)
                    self.assertIn(fd, live)
                    live.remove(fd)

                with contextlib.ExitStack() as patches:
                    patches.enter_context(mock.patch.object(common.os, "O_DIRECTORY", 0x10000, create=True))
                    patches.enter_context(mock.patch.object(common.os, "O_NOFOLLOW", 0x20000, create=True))
                    patches.enter_context(mock.patch.object(common.os, "getuid", return_value=3, create=True))
                    patches.enter_context(mock.patch.object(common.os, "getgid", return_value=4, create=True))
                    chooser = patches.enter_context(mock.patch.object(common.secrets, "choice", side_effect=list("".join(suffixes))))
                    made = patches.enter_context(mock.patch.object(common.os, "mkdir", side_effect=mkdir))
                    op = patches.enter_context(mock.patch.object(common.os, "open", side_effect=opened))
                    mode = patches.enter_context(mock.patch.object(common.os, "fchmod", create=True))
                    fs = patches.enter_context(mock.patch.object(common.os, "fstat", side_effect=inspected))
                    ns = patches.enter_context(mock.patch.object(common.os, "stat", side_effect=named))
                    sync = patches.enter_context(mock.patch.object(common.os, "fsync"))
                    close = patches.enter_context(mock.patch.object(common.os, "close", side_effect=closed))
                    rmdir = patches.enter_context(mock.patch.object(common.os, "rmdir"))
                    unlink = patches.enter_context(mock.patch.object(common.os, "unlink"))
                    child = None
                    if scenario == "EXHAUSTION":
                        with self.assertRaises(PREP.Failure) as caught:
                            child = PREP.create_owned_child(parent, prefix, 0o700, "TEST")
                        self.assertIs(type(caught.exception), PREP.Failure)
                        self.assertEqual((caught.exception.code, caught.exception.stage), ("DIRECTORY_NAME_EXHAUSTED", "TEST"))
                        self.assertIsNone(caught.exception.__context__)
                        self.assertIsNone(caught.exception.__cause__)
                        self.assertIsNone(child)
                        self.assertEqual(created, [])
                        self.assertEqual(live, set())
                        for operation in (op, mode, fs, ns, sync, close):
                            operation.assert_not_called()
                    else:
                        child = PREP.create_owned_child(parent, prefix, 0o700, "TEST")
                        self.assertIs(type(child), PREP.OwnedDirectory)
                        self.assertEqual(child.path, parent.path / candidates[1])
                        self.assertEqual(child.fd, 41)
                        self.assertIs(child.parent, parent)
                        self.assertEqual(created, [candidates[1]])
                        self.assertEqual(live, {41})
                        op.assert_called_once_with(candidates[1], flags, dir_fd=40)
                        mode.assert_called_once_with(41, 0o700)
                        self.assertEqual(sync.call_args_list, [mock.call(41), mock.call(40)])
                        self.assertEqual(fs.call_args_list, [mock.call(41), mock.call(41), mock.call(40)])
                        ns.assert_called_once_with(candidates[1], dir_fd=40, follow_symlinks=False)
                        close.assert_not_called()
                        child.close()  # Caller cleanup after successful transfer.
                        close.assert_called_once_with(41)
                        self.assertEqual(live, set())
                    self.assertEqual(attempts, candidates)
                    self.assertEqual(made.call_args_list, [mock.call(name, mode=0o700, dir_fd=40) for name in candidates])
                    self.assertEqual(chooser.call_args_list, [mock.call(alphabet)] * (8 * len(candidates)))
                    self.assertEqual(len(collisions), len(collided))
                    self.assertTrue(all(type(exc) is FileExistsError for exc in collisions))
                    rmdir.assert_not_called()
                    unlink.assert_not_called()
                for name, (entry, state) in snapshots.items():
                    self.assertIs(entries[name], entry)
                    self.assertEqual(entries[name], state)
                self.assertEqual(set(entries), set(collided + created))
                self.assertEqual(vars(parent), parent_before)
                completed.append(scenario)
        self.assertEqual(completed, ["COLLISION_THEN_SUCCESS", "EXHAUSTION"])

    def test_evidence_child_fchmod_failure_preserves_primary_without_pathname_cleanup(self):
        common = sys.modules[PREP.create_owned_child.__module__]
        parent = PREP.OwnedDirectory(pathlib.PurePosixPath("/tmp"), 40, 11, 140, 3, 4, 0o1777)
        retained = vars(parent).copy()
        basename = PREP.EVIDENCE_PREFIX + "AbCd1234"
        child_object = object()
        entries, live, events = {}, set(), []
        primary = OSError(5, "PRIMARY_CHILD_FCHMOD_FAILURE")
        flags = os.O_RDONLY | 0x10000 | 0x20000

        def mkdir(name, *, mode, dir_fd):
            self.assertEqual((name, mode, dir_fd), (basename, 0o700, 40))
            self.assertEqual(entries, {})
            entries[name] = child_object
            events.append("mkdir")

        def opened(name, supplied_flags, *, dir_fd):
            self.assertEqual((name, supplied_flags, dir_fd), (basename, flags, 40))
            self.assertIs(entries[name], child_object)
            live.add(41)
            events.append("open")
            return 41

        def chmod(fd, mode):
            self.assertEqual((fd, mode), (41, 0o700))
            self.assertEqual(live, {41})
            self.assertEqual(events, ["mkdir", "open"])
            events.append("fchmod")
            raise primary

        def closed(fd):
            self.assertEqual(fd, 41)
            self.assertEqual(live, {41})
            self.assertIs(sys.exc_info()[1], primary)
            live.remove(fd)
            events.append("close")

        with contextlib.ExitStack() as patches:
            patches.enter_context(mock.patch.object(common.os, "O_DIRECTORY", 0x10000, create=True))
            patches.enter_context(mock.patch.object(common.os, "O_NOFOLLOW", 0x20000, create=True))
            choice = patches.enter_context(mock.patch.object(common.secrets, "choice", side_effect=list("AbCd1234")))
            made = patches.enter_context(mock.patch.object(common.os, "mkdir", side_effect=mkdir))
            op = patches.enter_context(mock.patch.object(common.os, "open", side_effect=opened))
            mode = patches.enter_context(mock.patch.object(common.os, "fchmod", side_effect=chmod, create=True))
            close = patches.enter_context(mock.patch.object(common.os, "close", side_effect=closed))
            rmdir = patches.enter_context(mock.patch.object(common.os, "rmdir"))
            token = patches.enter_context(mock.patch.object(common, "_directory_token"))
            validate = patches.enter_context(mock.patch.object(common, "revalidate_owned_directory"))
            construct = patches.enter_context(mock.patch.object(common, "OwnedDirectory", wraps=PREP.OwnedDirectory))
            sync = patches.enter_context(mock.patch.object(common.os, "fsync"))
            returned = None
            with self.assertRaises(OSError) as caught:
                returned = PREP.create_owned_child(parent, PREP.EVIDENCE_PREFIX, 0o700, "TEST")
            self.assertIs(caught.exception, primary)
            self.assertIs(type(caught.exception), OSError)
            self.assertNotIsInstance(caught.exception, PREP.Failure)
            self.assertEqual((caught.exception.errno, caught.exception.strerror), (5, "PRIMARY_CHILD_FCHMOD_FAILURE"))
            self.assertIsNone(caught.exception.__context__)
            self.assertIsNone(caught.exception.__cause__)
            self.assertIsNone(returned)
            made.assert_called_once_with(basename, mode=0o700, dir_fd=40)
            op.assert_called_once_with(basename, flags, dir_fd=40)
            mode.assert_called_once_with(41, 0o700)
            close.assert_called_once_with(41)
            rmdir.assert_not_called()
            self.assertEqual(choice.call_count, 8)
            for operation in (token, validate, construct, sync):
                operation.assert_not_called()
        self.assertEqual(events, ["mkdir", "open", "fchmod", "close"])
        self.assertEqual(live, set())
        self.assertEqual(entries, {basename: child_object})
        self.assertIs(entries[basename], child_object)
        self.assertEqual(vars(parent), retained)

    def test_evidence_child_post_open_failure_closes_owned_descriptor(self):
        parent = PREP.OwnedDirectory(pathlib.PurePosixPath("/tmp"),
                                     40, 11, 140, 3, 4, 0o1777)
        parent_before = vars(parent).copy()
        basename = PREP.EVIDENCE_PREFIX + "AbCd1234"
        self.assertIsNotNone(PREP.EVIDENCE_RE.fullmatch(str(parent.path / basename)))
        events, present, acquired = [], set(), set()
        injected = OSError(5, "EVIDENCE_CHILD_FCHMOD_OBSERVATION")
        flags = os.O_RDONLY | 0x10000 | 0x20000
        common = sys.modules[PREP.create_owned_child.__module__]

        def mkdir_child(name, *, mode, dir_fd):
            self.assertEqual((name, mode, dir_fd), (basename, 0o700, 40))
            self.assertNotIn(name, present)
            events.append(("mkdir", name, mode, dir_fd))
            present.add(name)

        def open_child(name, supplied_flags, *, dir_fd):
            self.assertIn(name, present)
            self.assertEqual((name, supplied_flags, dir_fd), (basename, flags, 40))
            events.append(("open", name, supplied_flags, dir_fd, 41))
            acquired.add(41)
            return 41

        def fail_fchmod(fd, mode):
            self.assertEqual((fd, mode), (41, 0o700))
            self.assertIn(fd, acquired)
            events.append(("fchmod", fd, mode))
            raise injected

        def remove_child(name, *, dir_fd):
            self.assertEqual((name, dir_fd), (basename, 40))
            self.assertIn(name, present)
            events.append(("rmdir", name, dir_fd))
            present.remove(name)

        with contextlib.ExitStack() as patches:
            choice = patches.enter_context(mock.patch.object(PREP.secrets, "choice", side_effect=list("AbCd1234")))
            patches.enter_context(mock.patch.object(PREP.os, "O_DIRECTORY", 0x10000, create=True))
            patches.enter_context(mock.patch.object(PREP.os, "O_NOFOLLOW", 0x20000, create=True))
            mkdir = patches.enter_context(mock.patch.object(PREP.os, "mkdir", side_effect=mkdir_child))
            opened = patches.enter_context(mock.patch.object(PREP.os, "open", side_effect=open_child))
            chmod = patches.enter_context(mock.patch.object(PREP.os, "fchmod", side_effect=fail_fchmod, create=True))
            removed = patches.enter_context(mock.patch.object(PREP.os, "rmdir", side_effect=remove_child))
            closed = patches.enter_context(mock.patch.object(PREP.os, "close",
                side_effect=lambda fd: events.append(("close", fd))))
            token = patches.enter_context(mock.patch.object(common, "_directory_token", wraps=common._directory_token))
            constructed = patches.enter_context(mock.patch.object(common, "OwnedDirectory", wraps=PREP.OwnedDirectory))
            revalidated = patches.enter_context(mock.patch.object(common, "revalidate_owned_directory", wraps=common.revalidate_owned_directory))
            stat_call = patches.enter_context(mock.patch.object(PREP.os, "stat"))
            lstat_call = patches.enter_context(mock.patch.object(PREP.os, "lstat"))
            fstat_call = patches.enter_context(mock.patch.object(PREP.os, "fstat"))
            fsync = patches.enter_context(mock.patch.object(PREP.os, "fsync"))
            unlink = patches.enter_context(mock.patch.object(PREP.os, "unlink"))
            returned = None
            with self.assertRaises(OSError) as caught:
                returned = PREP.create_owned_child(parent, PREP.EVIDENCE_PREFIX, 0o700, "EVIDENCE_PUBLICATION")
        self.assertIs(caught.exception, injected)
        self.assertIs(type(caught.exception), OSError)
        self.assertNotIsInstance(caught.exception, PREP.Failure)
        self.assertEqual((caught.exception.errno, caught.exception.strerror),
                         (5, "EVIDENCE_CHILD_FCHMOD_OBSERVATION"))
        self.assertEqual(events, [("mkdir", basename, 0o700, 40),
            ("open", basename, flags, 40, 41), ("fchmod", 41, 0o700), ("close", 41)])
        mkdir.assert_called_once_with(basename, mode=0o700, dir_fd=40)
        opened.assert_called_once_with(basename, flags, dir_fd=40)
        chmod.assert_called_once_with(41, 0o700)
        removed.assert_not_called()
        self.assertEqual(choice.call_count, 8)
        self.assertEqual(acquired, {41})
        self.assertEqual(present, {basename})
        self.assertIsNone(returned)
        self.assertEqual(vars(parent), parent_before)
        closed.assert_called_once_with(41)
        self.assertEqual(sum(call.args[0] == 40 for call in closed.call_args_list), 0)
        for operation in (token, constructed, revalidated, stat_call, lstat_call, fstat_call, fsync, unlink):
            operation.assert_not_called()

    def _evidence_child_ownership_case(self, fault=None, close_fails=False):
        parent = PREP.OwnedDirectory(pathlib.PurePosixPath("/tmp"),
                                     40, 11, 140, 3, 4, 0o1777)
        parent_snapshot = vars(parent).copy()
        basename = PREP.EVIDENCE_PREFIX + "AbCd1234"
        flags = os.O_RDONLY | 0x10000 | 0x20000
        events = []
        primary = OSError(5, "OWNERSHIP_PRIMARY_" + str(fault))
        cleanup_error = OSError(9, "OWNERSHIP_CLEANUP_CLOSE")
        child_info = types.SimpleNamespace(st_dev=11, st_ino=141, st_uid=3,
                                           st_gid=4, st_mode=stat.S_IFDIR | 0o700)
        parent_info = types.SimpleNamespace(st_dev=11, st_ino=140, st_uid=3,
                                            st_gid=4, st_mode=stat.S_IFDIR | 0o1777)
        token_reads = 0

        def read_token(fd):
            nonlocal token_reads
            events.append(("fstat", fd))
            if fd == 40:
                return parent_info
            self.assertEqual(fd, 41)
            token_reads += 1
            if fault == "token" and token_reads == 1:
                raise primary
            if fault == "identity":
                return types.SimpleNamespace(**dict(vars(child_info), st_uid=99))
            if fault == "revalidation" and token_reads == 2:
                return types.SimpleNamespace(**dict(vars(child_info), st_ino=999))
            return child_info

        def chmod(fd, mode):
            events.append(("fchmod", fd, mode))
            if fault == "fchmod":
                raise primary

        def fsync(fd):
            events.append(("fsync", fd))
            if fault == "fsync":
                self.assertEqual(fd, 41)
                raise primary

        def close(fd):
            events.append(("close", fd))
            self.assertEqual(fd, 41)
            if close_fails:
                raise cleanup_error

        def inspect(name, *, dir_fd, follow_symlinks):
            self.assertEqual((name, dir_fd, follow_symlinks), (basename, 40, False))
            events.append(("stat", name, dir_fd, False))
            return child_info

        common = sys.modules[PREP.create_owned_child.__module__]
        with contextlib.ExitStack() as patches:
            choice = patches.enter_context(mock.patch.object(PREP.secrets, "choice", side_effect=list("AbCd1234")))
            patches.enter_context(mock.patch.object(PREP.os, "O_DIRECTORY", 0x10000, create=True))
            patches.enter_context(mock.patch.object(PREP.os, "O_NOFOLLOW", 0x20000, create=True))
            patches.enter_context(mock.patch.object(PREP.os, "getuid", return_value=3, create=True))
            patches.enter_context(mock.patch.object(PREP.os, "getgid", return_value=4, create=True))
            mkdir = patches.enter_context(mock.patch.object(PREP.os, "mkdir",
                side_effect=lambda name, **kwargs: events.append(("mkdir", name, kwargs))))
            opened = patches.enter_context(mock.patch.object(PREP.os, "open", return_value=41))
            changed = patches.enter_context(mock.patch.object(PREP.os, "fchmod", side_effect=chmod, create=True))
            patches.enter_context(mock.patch.object(PREP.os, "fstat", side_effect=read_token))
            patches.enter_context(mock.patch.object(PREP.os, "stat", side_effect=inspect))
            synced = patches.enter_context(mock.patch.object(PREP.os, "fsync", side_effect=fsync))
            closed = patches.enter_context(mock.patch.object(PREP.os, "close", side_effect=close))
            removed = patches.enter_context(mock.patch.object(PREP.os, "rmdir",
                side_effect=lambda name, **kwargs: events.append(("rmdir", name, kwargs))))
            constructed = patches.enter_context(mock.patch.object(common, "OwnedDirectory", wraps=PREP.OwnedDirectory))
            child = None
            failure = None
            try:
                child = PREP.create_owned_child(parent, PREP.EVIDENCE_PREFIX, 0o700, "EVIDENCE_PUBLICATION")
            except (OSError, PREP.Failure) as exc:
                failure = exc
        mkdir.assert_called_once_with(basename, mode=0o700, dir_fd=40)
        opened.assert_called_once_with(basename, flags, dir_fd=40)
        changed.assert_called_once_with(41, 0o700)
        self.assertEqual(choice.call_count, 8)
        self.assertEqual(vars(parent), parent_snapshot)
        if fault is None:
            self.assertIsNone(failure)
            self.assertIsInstance(child, PREP.OwnedDirectory)
            self.assertEqual((child.path, child.fd, child.dev, child.ino, child.uid, child.gid, child.mode),
                             (parent.path / basename, 41, 11, 141, 3, 4, 0o700))
            self.assertIs(child.parent, parent)
            constructed.assert_called_once_with(parent.path / basename, 41, 11, 141, 3, 4, 0o700, parent)
            closed.assert_not_called()
            removed.assert_not_called()
            self.assertEqual(synced.call_args_list, [mock.call(41), mock.call(40)])
            self.assertEqual(events[-5:], [("fstat", 41), ("fstat", 40),
                ("stat", basename, 40, False), ("fsync", 41), ("fsync", 40)])
        else:
            self.assertIsNone(child)
            closed.assert_called_once_with(41)
            removed.assert_not_called()
            self.assertEqual(events[-1:], [("close", 41)])
            if fault in ("token", "fchmod", "fsync"):
                self.assertIs(failure, primary)
            else:
                self.assertIs(type(failure), PREP.Failure)
                self.assertEqual((failure.code, failure.stage),
                    ("CREATED_DIRECTORY_IDENTITY_INVALID" if fault == "identity" else "DIRECTORY_IDENTITY_LOST",
                     "EVIDENCE_PUBLICATION"))
            if fault in ("token", "identity", "fchmod"):
                constructed.assert_not_called()
            else:
                constructed.assert_called_once()
            if fault == "fsync":
                synced.assert_called_once_with(41)
            else:
                synced.assert_not_called()
        return failure, cleanup_error

    def test_evidence_child_post_open_failures_close_owned_descriptor(self):
        for fault in ("token", "identity", "revalidation", "fsync"):
            with self.subTest(fault=fault):
                self._evidence_child_ownership_case(fault)

    def test_evidence_child_cleanup_close_oserror_preserves_primary_failure(self):
        failure, cleanup_error = self._evidence_child_ownership_case("fchmod", close_fails=True)
        self.assertIsNot(failure, cleanup_error)
        self.assertEqual(failure.errno, 5)

    def test_evidence_child_success_transfers_descriptor_ownership_to_returned_child(self):
        self._evidence_child_ownership_case()

    def test_publisher_verification_metadata_rejections_preserve_result(self):
        common = sys.modules[PREP.publish_owned_json.__module__]
        document = {"ok": True}
        payload = (PREP.json.dumps(document, sort_keys=True, separators=(",", ":")) + "\n").encode()
        self.assertEqual(payload, b'{"ok":true}\n')
        self.assertEqual(len(payload), 12)
        temporary, target = ".result.json.AbCdEfGh", "result.json"
        cases = ("WRONG_TYPE", "UID_MISMATCH", "MODE_MISMATCH")
        baseline = dict(st_mode=stat.S_IFREG | 0o600, st_uid=3, st_gid=4)
        completed = []
        for fault in cases:
            with self.subTest(fault=fault):
                directory = PREP.OwnedDirectory(pathlib.Path("/tmp/evidence"), 40, 11, 140, 3, 4, 0o700)
                metadata = baseline.copy()
                if fault == "WRONG_TYPE":
                    metadata["st_mode"] = stat.S_IFDIR | 0o600
                elif fault == "UID_MISMATCH":
                    metadata["st_uid"] = 99
                else:
                    metadata["st_mode"] = stat.S_IFREG | 0o640
                expected_field = "st_uid" if fault == "UID_MISMATCH" else "st_mode"
                self.assertEqual([key for key in baseline if baseline[key] != metadata[key]], [expected_field])
                entries, events, acquired, published, reads, primary_seen = {}, [], [], [], [], []

                def opened(name, flags, mode=None, *, dir_fd):
                    self.assertEqual(dir_fd, 40)
                    events.append(("open", name))
                    if name == temporary:
                        self.assertEqual((flags, mode), (15, 0o600))
                        self.assertEqual(entries, {})
                        entries[name] = bytearray()
                        acquired.append(41)
                        return 41
                    self.assertEqual((name, flags, mode), (target, 24, None))
                    self.assertEqual(events[-2], ("fsync", 40))
                    self.assertEqual(entries, {target: bytearray(payload)})
                    self.assertIs(entries[target], published[0])
                    acquired.append(42)
                    return 42

                def written(fd, view):
                    self.assertEqual((fd, bytes(view)), (41, payload))
                    entries[temporary].extend(view)
                    events.append(("write", fd))
                    return len(view)

                def linked(source, destination, **kwargs):
                    self.assertEqual((source, destination), (temporary, target))
                    self.assertEqual(kwargs, dict(src_dir_fd=40, dst_dir_fd=40, follow_symlinks=False))
                    self.assertNotIn(destination, entries)
                    self.assertEqual(bytes(entries[source]), payload)
                    entries[destination] = entries[source]
                    published.append(entries[destination])
                    events.append(("link", target))

                def unlinked(name, *, dir_fd):
                    self.assertEqual((name, dir_fd), (temporary, 40))
                    del entries[name]
                    events.append(("unlink", name))

                def inspected(fd):
                    events.append(("fstat", fd))
                    if fd == 40:
                        return types.SimpleNamespace(st_dev=11, st_ino=140, st_uid=3, st_gid=4,
                                                     st_mode=stat.S_IFDIR | 0o700)
                    self.assertEqual(fd, 42)
                    return types.SimpleNamespace(**metadata)

                def reread(fd, count):
                    self.assertEqual(fd, 42)
                    offset = sum(map(len, reads))
                    self.assertEqual(count, 4097 - offset)
                    block = bytes(entries[target])[offset:offset + count]
                    reads.append(block)
                    events.append(("read", block))
                    return block

                def closed(fd):
                    if fd == 41:
                        self.assertIsNone(sys.exc_info()[1])
                        events.append(("normal_close", fd))
                    else:
                        self.assertEqual(fd, 42)
                        active = sys.exc_info()[1]
                        self.assertIs(type(active), PREP.Failure)
                        self.assertEqual((active.code, active.stage), ("EVIDENCE_CONFIRMATION_FAILED", "TEST"))
                        self.assertEqual(reads, [payload, b""])
                        primary_seen.append(active)
                        events.append(("cleanup_close", fd))

                with contextlib.ExitStack() as patches:
                    for name, value in {"O_WRONLY": 1, "O_CREAT": 2, "O_EXCL": 4, "O_NOFOLLOW": 8, "O_RDONLY": 16}.items():
                        patches.enter_context(mock.patch.object(common.os, name, value, create=True))
                    patches.enter_context(mock.patch.object(common.os, "getuid", return_value=3, create=True))
                    patches.enter_context(mock.patch.object(common.os, "getgid", return_value=4, create=True))
                    patches.enter_context(mock.patch.object(common.secrets, "choice", side_effect=list("AbCdEfGh")))
                    validate = patches.enter_context(mock.patch.object(common, "revalidate_owned_directory",
                        wraps=common.revalidate_owned_directory))
                    op = patches.enter_context(mock.patch.object(common.os, "open", side_effect=opened))
                    wr = patches.enter_context(mock.patch.object(common.os, "write", side_effect=written))
                    chmod = patches.enter_context(mock.patch.object(common.os, "fchmod", create=True,
                        side_effect=lambda fd, mode: events.append(("fchmod", fd, mode))))
                    sync = patches.enter_context(mock.patch.object(common.os, "fsync",
                        side_effect=lambda fd: events.append(("fsync", fd))))
                    close = patches.enter_context(mock.patch.object(common.os, "close", side_effect=closed))
                    link = patches.enter_context(mock.patch.object(common.os, "link", side_effect=linked))
                    unlink = patches.enter_context(mock.patch.object(common.os, "unlink", side_effect=unlinked))
                    fs = patches.enter_context(mock.patch.object(common.os, "fstat", side_effect=inspected))
                    read = patches.enter_context(mock.patch.object(common.os, "read", side_effect=reread))
                    digest = patches.enter_context(mock.patch.object(common.hashlib, "sha256"))
                    returned = None
                    with self.assertRaises(PREP.Failure) as caught:
                        returned = PREP.publish_owned_json(directory, target, document, "TEST", max_bytes=4096)
                    self.assertIs(type(caught.exception), PREP.Failure)
                    self.assertEqual((caught.exception.code, caught.exception.stage), ("EVIDENCE_CONFIRMATION_FAILED", "TEST"))
                    self.assertEqual(len(primary_seen), 1)
                    self.assertIs(caught.exception, primary_seen[0])
                    self.assertIsNone(caught.exception.__context__)
                    self.assertIsNone(caught.exception.__cause__)
                    self.assertIsNone(returned)
                    validate.assert_called_once_with(directory, "TEST")
                    self.assertEqual(op.call_args_list, [mock.call(temporary, 15, 0o600, dir_fd=40),
                                                       mock.call(target, 24, dir_fd=40)])
                    wr.assert_called_once()
                    chmod.assert_called_once_with(41, 0o600)
                    self.assertEqual(sync.call_args_list, [mock.call(41), mock.call(40)])
                    expected_closes = [mock.call(41), mock.call(42)]
                    self.assertEqual(close.call_args_list, expected_closes)
                    self.assertEqual(fs.call_args_list, [mock.call(40), mock.call(42)])
                    link.assert_called_once_with(temporary, target, src_dir_fd=40, dst_dir_fd=40, follow_symlinks=False)
                    unlink.assert_called_once_with(temporary, dir_fd=40)
                    self.assertEqual(read.call_args_list, [mock.call(42, 4097), mock.call(42, 4085)])
                    digest.assert_not_called()
                expected = [("fstat", 40), ("open", temporary), ("write", 41),
                    ("fchmod", 41, 0o600), ("fsync", 41), ("normal_close", 41),
                    ("link", target), ("unlink", temporary), ("fsync", 40), ("open", target)]
                expected.extend([("fstat", 42), ("read", payload), ("read", b""), ("cleanup_close", 42)])
                self.assertEqual(events, expected)
                self.assertEqual(acquired, [41, 42])
                self.assertEqual(entries, {target: bytearray(payload)})
                self.assertIs(entries[target], published[0])
                self.assertEqual(reads, [payload, b""])
                self.assertNotIn(temporary, entries)
                completed.append(fault)
        self.assertEqual(completed, list(cases))

    def test_publisher_verification_open_and_fstat_failures_preserve_result(self):
        common = sys.modules[PREP.publish_owned_json.__module__]
        document = {"ok": True}
        payload = (PREP.json.dumps(document, sort_keys=True, separators=(",", ":")) + "\n").encode()
        self.assertEqual(payload, b'{"ok":true}\n')
        self.assertEqual(len(payload), 12)
        temporary, target = ".result.json.AbCdEfGh", "result.json"
        cases = ("VERIFICATION_OPEN_OSERROR", "VERIFICATION_FSTAT_OSERROR")
        completed = []
        for fault in cases:
            with self.subTest(fault=fault):
                directory = PREP.OwnedDirectory(pathlib.Path("/tmp/evidence"), 40, 11, 140, 3, 4, 0o700)
                primary = OSError(5, "VERIFICATION_OPEN_FAILURE" if fault == cases[0] else "VERIFICATION_FSTAT_FAILURE")
                self.assertIs(type(primary), OSError)
                entries, events, acquired, published = {}, [], [], []

                def opened(name, flags, mode=None, *, dir_fd):
                    self.assertEqual(dir_fd, 40)
                    events.append(("open", name))
                    if name == temporary:
                        self.assertEqual((flags, mode), (15, 0o600))
                        self.assertEqual(entries, {})
                        entries[name] = bytearray()
                        acquired.append(41)
                        return 41
                    self.assertEqual((name, flags, mode), (target, 24, None))
                    self.assertEqual(events[-2], ("fsync", 40))
                    self.assertEqual(entries, {target: bytearray(payload)})
                    self.assertIs(entries[target], published[0])
                    if fault == cases[0]:
                        raise primary
                    acquired.append(42)
                    return 42

                def written(fd, view):
                    self.assertEqual((fd, bytes(view)), (41, payload))
                    entries[temporary].extend(view)
                    events.append(("write", fd))
                    return len(view)

                def linked(source, destination, **kwargs):
                    self.assertEqual((source, destination), (temporary, target))
                    self.assertEqual(kwargs, dict(src_dir_fd=40, dst_dir_fd=40, follow_symlinks=False))
                    self.assertNotIn(destination, entries)
                    self.assertEqual(bytes(entries[source]), payload)
                    entries[destination] = entries[source]
                    published.append(entries[destination])
                    events.append(("link", target))

                def unlinked(name, *, dir_fd):
                    self.assertEqual((name, dir_fd), (temporary, 40))
                    del entries[name]
                    events.append(("unlink", name))

                def inspected(fd):
                    events.append(("fstat", fd))
                    if fd == 40:
                        return types.SimpleNamespace(st_dev=11, st_ino=140, st_uid=3, st_gid=4,
                                                     st_mode=stat.S_IFDIR | 0o700)
                    self.assertEqual(fd, 42)
                    self.assertEqual(fault, cases[1])
                    raise primary

                def closed(fd):
                    if fd == 41:
                        self.assertIsNone(sys.exc_info()[1])
                        events.append(("normal_close", fd))
                    else:
                        self.assertEqual(fd, 42)
                        self.assertIs(sys.exc_info()[1], primary)
                        events.append(("cleanup_close", fd))

                with contextlib.ExitStack() as patches:
                    for name, value in {"O_WRONLY": 1, "O_CREAT": 2, "O_EXCL": 4, "O_NOFOLLOW": 8, "O_RDONLY": 16}.items():
                        patches.enter_context(mock.patch.object(common.os, name, value, create=True))
                    patches.enter_context(mock.patch.object(common.secrets, "choice", side_effect=list("AbCdEfGh")))
                    validate = patches.enter_context(mock.patch.object(common, "revalidate_owned_directory",
                        wraps=common.revalidate_owned_directory))
                    op = patches.enter_context(mock.patch.object(common.os, "open", side_effect=opened))
                    wr = patches.enter_context(mock.patch.object(common.os, "write", side_effect=written))
                    chmod = patches.enter_context(mock.patch.object(common.os, "fchmod", create=True,
                        side_effect=lambda fd, mode: events.append(("fchmod", fd, mode))))
                    sync = patches.enter_context(mock.patch.object(common.os, "fsync",
                        side_effect=lambda fd: events.append(("fsync", fd))))
                    close = patches.enter_context(mock.patch.object(common.os, "close", side_effect=closed))
                    link = patches.enter_context(mock.patch.object(common.os, "link", side_effect=linked))
                    unlink = patches.enter_context(mock.patch.object(common.os, "unlink", side_effect=unlinked))
                    fs = patches.enter_context(mock.patch.object(common.os, "fstat", side_effect=inspected))
                    read = patches.enter_context(mock.patch.object(common.os, "read"))
                    digest = patches.enter_context(mock.patch.object(common.hashlib, "sha256"))
                    returned = None
                    with self.assertRaises(PREP.Failure) as caught:
                        returned = PREP.publish_owned_json(directory, target, document, "TEST", max_bytes=4096)
                    self.assertIs(type(caught.exception), PREP.Failure)
                    self.assertEqual((caught.exception.code, caught.exception.stage), ("EVIDENCE_PUBLICATION_FAILED", "TEST"))
                    self.assertIs(caught.exception.__context__, primary)
                    self.assertIsNone(caught.exception.__cause__)
                    self.assertIsNone(returned)
                    validate.assert_called_once_with(directory, "TEST")
                    self.assertEqual(op.call_args_list, [mock.call(temporary, 15, 0o600, dir_fd=40),
                                                       mock.call(target, 24, dir_fd=40)])
                    wr.assert_called_once()
                    chmod.assert_called_once_with(41, 0o600)
                    self.assertEqual(sync.call_args_list, [mock.call(41), mock.call(40)])
                    expected_closes = [mock.call(41)] + ([mock.call(42)] if fault == cases[1] else [])
                    self.assertEqual(close.call_args_list, expected_closes)
                    self.assertEqual(fs.call_args_list, [mock.call(40)] + ([mock.call(42)] if fault == cases[1] else []))
                    link.assert_called_once_with(temporary, target, src_dir_fd=40, dst_dir_fd=40, follow_symlinks=False)
                    unlink.assert_called_once_with(temporary, dir_fd=40)
                    read.assert_not_called()
                    digest.assert_not_called()
                expected = [("fstat", 40), ("open", temporary), ("write", 41),
                    ("fchmod", 41, 0o600), ("fsync", 41), ("normal_close", 41),
                    ("link", target), ("unlink", temporary), ("fsync", 40), ("open", target)]
                if fault == cases[1]:
                    expected.extend([("fstat", 42), ("cleanup_close", 42)])
                self.assertEqual(events, expected)
                self.assertEqual(acquired, [41, 42] if fault == cases[1] else [41])
                self.assertEqual(entries, {target: bytearray(payload)})
                self.assertIs(entries[target], published[0])
                self.assertNotIn(temporary, entries)
                completed.append(fault)
        self.assertEqual(completed, list(cases))

    def test_publisher_final_directory_revalidation_failure_preserves_result(self):
        common = sys.modules[PREP.publish_owned_json.__module__]
        directory = PREP.OwnedDirectory(pathlib.Path("/tmp/evidence"), 40, 11, 140, 3, 4, 0o700)
        original = (11, 140, 3, 4, 0o700)
        changed = (11, 999, 3, 4, 0o700)
        observed = list(original)
        retained = vars(directory).copy()
        document = {"ok": True}
        payload = (PREP.json.dumps(document, sort_keys=True, separators=(",", ":")) + "\n").encode()
        self.assertEqual(payload, b'{"ok":true}\n')
        self.assertEqual(len(payload), 12)
        temporary, target = ".result.json.AbCdEfGh", "result.json"
        entries, events, reads, directory_tokens, failures = {}, [], [], [], []
        published = []
        real_validate = common.revalidate_owned_directory

        def validate(item, stage):
            # Observe propagation without manufacturing the governed failure.
            try:
                return real_validate(item, stage)
            except PREP.Failure as exc:
                failures.append(exc)
                raise

        def opened(name, flags, mode=None, *, dir_fd):
            self.assertEqual(dir_fd, 40)
            events.append(("open", name))
            if name == temporary:
                self.assertEqual((flags, mode), (15, 0o600))
                self.assertEqual(directory_tokens, [original])
                self.assertEqual(entries, {})
                entries[name] = bytearray()
                return 41
            self.assertEqual((name, flags, mode), (target, 24, None))
            self.assertEqual(entries, {target: bytearray(payload)})
            return 42

        def written(fd, view):
            self.assertEqual((fd, bytes(view)), (41, payload))
            entries[temporary].extend(view)
            events.append(("write", fd))
            return len(view)

        def linked(source, destination, **kwargs):
            self.assertEqual((source, destination), (temporary, target))
            self.assertEqual(kwargs, dict(src_dir_fd=40, dst_dir_fd=40, follow_symlinks=False))
            self.assertEqual(bytes(entries[source]), payload)
            self.assertNotIn(destination, entries)
            entries[destination] = entries[source]
            published.append(entries[destination])
            events.append(("link", target))

        def unlinked(name, *, dir_fd):
            self.assertEqual((name, dir_fd), (temporary, 40))
            del entries[name]
            events.append(("unlink", name))

        def inspected(fd):
            events.append(("fstat", fd))
            if fd == 40:
                token = tuple(observed)
                directory_tokens.append(token)
                if len(directory_tokens) == 2:
                    self.assertEqual(events[-2], ("close", 42))
                    self.assertEqual(entries, {target: bytearray(payload)})
                    self.assertIs(entries[target], published[0])
                return types.SimpleNamespace(st_dev=token[0], st_ino=token[1], st_uid=token[2],
                                             st_gid=token[3], st_mode=stat.S_IFDIR | token[4])
            self.assertEqual(fd, 42)
            return types.SimpleNamespace(st_uid=3, st_gid=4, st_mode=stat.S_IFREG | 0o600)

        def reread(fd, count):
            self.assertEqual(fd, 42)
            offset = sum(map(len, reads))
            self.assertEqual(count, 4097 - offset)
            block = bytes(entries[target])[offset:offset + count]
            reads.append(block)
            events.append(("read", block))
            return block

        def closed(fd):
            self.assertIn(fd, (41, 42))
            self.assertIsNone(sys.exc_info()[1])
            events.append(("close", fd))
            if fd == 42:
                self.assertEqual(reads, [payload, b""])
                self.assertEqual(tuple(observed), original)
                observed[:] = changed

        with contextlib.ExitStack() as patches:
            for name, value in {"O_WRONLY": 1, "O_CREAT": 2, "O_EXCL": 4, "O_NOFOLLOW": 8, "O_RDONLY": 16}.items():
                patches.enter_context(mock.patch.object(common.os, name, value, create=True))
            patches.enter_context(mock.patch.object(common.os, "getuid", return_value=3, create=True))
            patches.enter_context(mock.patch.object(common.os, "getgid", return_value=4, create=True))
            patches.enter_context(mock.patch.object(common.secrets, "choice", side_effect=list("AbCdEfGh")))
            validation = patches.enter_context(mock.patch.object(common, "revalidate_owned_directory", side_effect=validate))
            op = patches.enter_context(mock.patch.object(common.os, "open", side_effect=opened))
            wr = patches.enter_context(mock.patch.object(common.os, "write", side_effect=written))
            chmod = patches.enter_context(mock.patch.object(common.os, "fchmod", create=True,
                side_effect=lambda fd, mode: events.append(("fchmod", fd, mode))))
            sync = patches.enter_context(mock.patch.object(common.os, "fsync",
                side_effect=lambda fd: events.append(("fsync", fd))))
            close = patches.enter_context(mock.patch.object(common.os, "close", side_effect=closed))
            link = patches.enter_context(mock.patch.object(common.os, "link", side_effect=linked))
            unlink = patches.enter_context(mock.patch.object(common.os, "unlink", side_effect=unlinked))
            fs = patches.enter_context(mock.patch.object(common.os, "fstat", side_effect=inspected))
            read = patches.enter_context(mock.patch.object(common.os, "read", side_effect=reread))
            digest = patches.enter_context(mock.patch.object(common.hashlib, "sha256"))
            returned = None
            with self.assertRaises(PREP.Failure) as caught:
                returned = PREP.publish_owned_json(directory, target, document, "TEST", max_bytes=4096)
            self.assertIs(type(caught.exception), PREP.Failure)
            self.assertEqual((caught.exception.code, caught.exception.stage), ("DIRECTORY_IDENTITY_LOST", "TEST"))
            self.assertEqual(len(failures), 1)
            self.assertIs(caught.exception, failures[0])
            self.assertIsNone(caught.exception.__context__)
            self.assertIsNone(caught.exception.__cause__)
            self.assertIsNone(returned)
            digest.assert_not_called()
            self.assertEqual(validation.call_args_list, [mock.call(directory, "TEST")] * 2)
            self.assertEqual(op.call_args_list, [mock.call(temporary, 15, 0o600, dir_fd=40),
                                               mock.call(target, 24, dir_fd=40)])
            wr.assert_called_once()
            chmod.assert_called_once_with(41, 0o600)
            self.assertEqual(sync.call_args_list, [mock.call(41), mock.call(40)])
            self.assertEqual(close.call_args_list, [mock.call(41), mock.call(42)])
            link.assert_called_once()
            unlink.assert_called_once_with(temporary, dir_fd=40)
            self.assertEqual(fs.call_args_list, [mock.call(40), mock.call(42), mock.call(40)])
            self.assertEqual(read.call_args_list, [mock.call(42, 4097), mock.call(42, 4085)])
        self.assertEqual(events, [("fstat", 40), ("open", temporary), ("write", 41),
            ("fchmod", 41, 0o600), ("fsync", 41), ("close", 41), ("link", target),
            ("unlink", temporary), ("fsync", 40), ("open", target), ("fstat", 42),
            ("read", payload), ("read", b""), ("close", 42), ("fstat", 40)])
        self.assertEqual(directory_tokens, [original, changed])
        self.assertEqual(entries, {target: bytearray(payload)})
        self.assertIs(entries[target], published[0])
        self.assertNotIn(temporary, entries)
        self.assertEqual(vars(directory), retained)

    def test_publisher_remaining_prelink_oserrors_fail_without_target(self):
        common = sys.modules[PREP.publish_owned_json.__module__]
        document = {"ok": True}
        payload = (PREP.json.dumps(document, sort_keys=True, separators=(",", ":")) + "\n").encode()
        self.assertEqual(payload, b'{"ok":true}\n')
        self.assertEqual(len(payload), 12)
        temporary, target = ".result.json.AbCdEfGh", "result.json"
        cases = ("TEMP_OPEN_OSERROR", "FCHMOD_OSERROR", "FILE_FSYNC_OSERROR", "LINK_OSERROR")
        messages = ("TEMPORARY_OPEN_FAILURE", "TEMPORARY_FCHMOD_FAILURE",
                    "TEMPORARY_FILE_FSYNC_FAILURE", "PUBLICATION_LINK_FAILURE")
        completed = []
        for fault, message in zip(cases, messages):
            with self.subTest(fault=fault):
                directory = PREP.OwnedDirectory(pathlib.Path("/tmp/evidence"), 40, 11, 140, 3, 4, 0o700)
                primary = OSError(5, message)
                self.assertIs(type(primary), OSError)
                entries, events, acquired = {}, [], []

                def opened(name, flags, mode, *, dir_fd):
                    self.assertEqual((name, flags, mode, dir_fd), (temporary, 15, 0o600, 40))
                    self.assertEqual(entries, {})
                    events.append("open")
                    if fault == "TEMP_OPEN_OSERROR":
                        raise primary
                    entries[name] = bytearray()
                    acquired.append(41)
                    return 41

                def written(fd, view):
                    self.assertEqual((fd, bytes(view)), (41, payload))
                    entries[temporary].extend(view)
                    events.append("write")
                    return len(view)

                def chmod(fd, mode):
                    self.assertEqual((fd, mode), (41, 0o600))
                    self.assertEqual(bytes(entries[temporary]), payload)
                    events.append("fchmod")
                    if fault == "FCHMOD_OSERROR":
                        raise primary

                def fsync(fd):
                    self.assertEqual(fd, 41)
                    events.append("file_fsync")
                    if fault == "FILE_FSYNC_OSERROR":
                        raise primary

                def closed(fd):
                    self.assertEqual(fd, 41)
                    if fault == "LINK_OSERROR":
                        self.assertIsNone(sys.exc_info()[1])
                        events.append("normal_close")
                    else:
                        active = sys.exc_info()[1]
                        self.assertIs(type(active), PREP.Failure)
                        self.assertIs(active.__context__, primary)
                        events.append("cleanup_close")

                def linked(source, destination, **kwargs):
                    self.assertEqual((source, destination), (temporary, target))
                    self.assertEqual(kwargs, dict(src_dir_fd=40, dst_dir_fd=40, follow_symlinks=False))
                    self.assertEqual(events[-1], "normal_close")
                    self.assertEqual(bytes(entries[source]), payload)
                    self.assertNotIn(destination, entries)
                    events.append("link")
                    raise primary

                def unlinked(name, *, dir_fd):
                    self.assertEqual((name, dir_fd), (temporary, 40))
                    self.assertEqual(bytes(entries[name]), payload)
                    self.assertIs(type(sys.exc_info()[1]), PREP.Failure)
                    del entries[name]
                    events.append("cleanup_unlink")

                with contextlib.ExitStack() as patches:
                    for name, value in {"O_WRONLY": 1, "O_CREAT": 2, "O_EXCL": 4, "O_NOFOLLOW": 8}.items():
                        patches.enter_context(mock.patch.object(common.os, name, value, create=True))
                    patches.enter_context(mock.patch.object(common.secrets, "choice", side_effect=list("AbCdEfGh")))
                    validate = patches.enter_context(mock.patch.object(common, "revalidate_owned_directory"))
                    op = patches.enter_context(mock.patch.object(common.os, "open", side_effect=opened))
                    wr = patches.enter_context(mock.patch.object(common.os, "write", side_effect=written))
                    mode = patches.enter_context(mock.patch.object(common.os, "fchmod", side_effect=chmod, create=True))
                    sync = patches.enter_context(mock.patch.object(common.os, "fsync", side_effect=fsync))
                    close = patches.enter_context(mock.patch.object(common.os, "close", side_effect=closed))
                    link = patches.enter_context(mock.patch.object(common.os, "link", side_effect=linked))
                    unlink = patches.enter_context(mock.patch.object(common.os, "unlink", side_effect=unlinked))
                    later = [patches.enter_context(mock.patch.object(common.os, name)) for name in ("fstat", "read")]
                    digest = patches.enter_context(mock.patch.object(common.hashlib, "sha256"))
                    returned = None
                    with self.assertRaises(PREP.Failure) as caught:
                        returned = PREP.publish_owned_json(directory, target, document, "TEST", max_bytes=4096)
                    self.assertIs(type(caught.exception), PREP.Failure)
                    self.assertEqual((caught.exception.code, caught.exception.stage), ("EVIDENCE_PUBLICATION_FAILED", "TEST"))
                    self.assertIs(caught.exception.__context__, primary)
                    self.assertIsNone(caught.exception.__cause__)
                    self.assertIsNone(returned)
                    validate.assert_called_once_with(directory, "TEST")
                    op.assert_called_once_with(temporary, 15, 0o600, dir_fd=40)
                    if fault == "TEMP_OPEN_OSERROR":
                        self.assertEqual(acquired, [])
                        for operation in (wr, mode, sync, close, link, unlink):
                            operation.assert_not_called()
                        expected = ["open"]
                    else:
                        self.assertEqual(acquired, [41])
                        wr.assert_called_once()
                        mode.assert_called_once_with(41, 0o600)
                        close.assert_called_once_with(41)
                        unlink.assert_called_once_with(temporary, dir_fd=40)
                        expected = ["open", "write", "fchmod"]
                        if fault == "FCHMOD_OSERROR":
                            sync.assert_not_called()
                        else:
                            sync.assert_called_once_with(41)
                            expected.append("file_fsync")
                        if fault == "LINK_OSERROR":
                            link.assert_called_once_with(temporary, target, src_dir_fd=40, dst_dir_fd=40,
                                                         follow_symlinks=False)
                            expected.extend(["normal_close", "link"])
                        else:
                            link.assert_not_called()
                            expected.append("cleanup_close")
                        expected.append("cleanup_unlink")
                    for operation in later + [digest]:
                        operation.assert_not_called()
                self.assertEqual(events, expected)
                self.assertEqual(entries, {})
                self.assertNotIn(target, entries)
                self.assertNotIn(temporary, entries)
                completed.append(fault)
        self.assertEqual(completed, list(cases))

    def test_publisher_nonpositive_writes_fail_before_publication(self):
        common = sys.modules[PREP.publish_owned_json.__module__]
        document = {"ok": True}
        payload = (PREP.json.dumps(document, sort_keys=True, separators=(",", ":")) + "\n").encode()
        self.assertEqual(payload, b'{"ok":true}\n')
        self.assertEqual(len(payload), 12)
        temporary, target = ".result.json.AbCdEfGh", "result.json"
        completed = []
        for write_result in (0, -1):
            with self.subTest(write_result=write_result):
                directory = PREP.OwnedDirectory(pathlib.Path("/tmp/evidence"), 40, 11, 140, 3, 4, 0o700)
                entries, events, supplied = {}, [], []

                def opened(name, flags, mode, *, dir_fd):
                    self.assertEqual((name, flags, mode, dir_fd), (temporary, 15, 0o600, 40))
                    self.assertEqual(entries, {})
                    entries[name] = bytearray()
                    events.append(("open", name))
                    return 41

                def written(fd, view):
                    self.assertEqual(fd, 41)
                    self.assertEqual(bytes(view), payload)
                    supplied.append(bytes(view))
                    self.assertEqual(bytes(entries[temporary]), b"")
                    events.append(("write", write_result))
                    return write_result

                def cleanup_close(fd):
                    self.assertEqual(fd, 41)
                    primary = sys.exc_info()[1]
                    self.assertIs(type(primary), PREP.Failure)
                    self.assertEqual((primary.code, primary.stage), ("EVIDENCE_WRITE_FAILED", "TEST"))
                    self.assertEqual(bytes(entries[temporary]), b"")
                    events.append(("cleanup_close", fd))

                def cleanup_unlink(name, *, dir_fd):
                    self.assertEqual((name, dir_fd), (temporary, 40))
                    self.assertEqual(events[-1], ("cleanup_close", 41))
                    self.assertEqual(bytes(entries[name]), b"")
                    del entries[name]
                    events.append(("cleanup_unlink", name))

                with contextlib.ExitStack() as patches:
                    for name, value in {"O_WRONLY": 1, "O_CREAT": 2, "O_EXCL": 4, "O_NOFOLLOW": 8}.items():
                        patches.enter_context(mock.patch.object(common.os, name, value, create=True))
                    choice = patches.enter_context(mock.patch.object(common.secrets, "choice", side_effect=list("AbCdEfGh")))
                    validate = patches.enter_context(mock.patch.object(common, "revalidate_owned_directory"))
                    op = patches.enter_context(mock.patch.object(common.os, "open", side_effect=opened))
                    wr = patches.enter_context(mock.patch.object(common.os, "write", side_effect=written))
                    close = patches.enter_context(mock.patch.object(common.os, "close", side_effect=cleanup_close))
                    unlink = patches.enter_context(mock.patch.object(common.os, "unlink", side_effect=cleanup_unlink))
                    later = [patches.enter_context(mock.patch.object(common.os, name, create=True))
                             for name in ("fchmod", "fsync", "link", "fstat", "read")]
                    digest = patches.enter_context(mock.patch.object(common.hashlib, "sha256"))
                    returned = None
                    with self.assertRaises(PREP.Failure) as caught:
                        returned = PREP.publish_owned_json(directory, target, document, "TEST", max_bytes=4096)
                    self.assertIs(type(caught.exception), PREP.Failure)
                    self.assertEqual((caught.exception.code, caught.exception.stage), ("EVIDENCE_WRITE_FAILED", "TEST"))
                    self.assertIsNone(caught.exception.__context__)
                    self.assertIsNone(caught.exception.__cause__)
                    self.assertIsNone(returned)
                    validate.assert_called_once_with(directory, "TEST")
                    op.assert_called_once_with(temporary, 15, 0o600, dir_fd=40)
                    wr.assert_called_once()
                    self.assertEqual(supplied, [payload])
                    close.assert_called_once_with(41)
                    unlink.assert_called_once_with(temporary, dir_fd=40)
                    choice.assert_has_calls([mock.call(PREP.string.ascii_letters)] * 8)
                    self.assertEqual(choice.call_count, 8)
                    for operation in later + [digest]:
                        operation.assert_not_called()
                self.assertEqual(events, [("open", temporary), ("write", write_result),
                    ("cleanup_close", 41), ("cleanup_unlink", temporary)])
                self.assertEqual(entries, {})
                self.assertNotIn(target, entries)
                self.assertNotIn(temporary, entries)
                completed.append(write_result)
        self.assertEqual(completed, [0, -1])

    def test_publisher_positive_partial_writes_publish_exact_payload(self):
        common = sys.modules[PREP.publish_owned_json.__module__]
        directory = PREP.OwnedDirectory(pathlib.Path("/tmp/evidence"), 40, 11, 140, 3, 4, 0o700)
        document = {"ok": True}
        payload = (PREP.json.dumps(document, sort_keys=True, separators=(",", ":")) + "\n").encode()
        self.assertEqual(payload, b'{"ok":true}\n')
        self.assertEqual(len(payload), 12)
        temporary, target = ".result.json.AbCdEfGh", "result.json"
        entries, events, writes, reads = {}, [], [], []
        counts = (3, 2, len(payload) - 5)
        offsets = (3, 5, len(payload))

        def opened(name, flags, mode=None, *, dir_fd):
            self.assertEqual(dir_fd, 40)
            events.append(("open", name))
            if name == temporary:
                self.assertEqual((flags, mode), (15, 0o600))
                self.assertEqual(entries, {})
                entries[name] = bytearray()
                return 41
            self.assertEqual((name, flags, mode), (target, 24, None))
            self.assertEqual(entries, {target: bytearray(payload)})
            return 42

        def written(fd, view):
            self.assertEqual(fd, 41)
            data = bytes(view)
            index = len(writes)
            self.assertLess(index, len(counts))
            offset = 0 if index == 0 else offsets[index - 1]
            self.assertEqual(data, payload[offset:])
            count = counts[index]
            self.assertGreater(count, 0)
            self.assertLessEqual(count, len(data))
            if index < 2:
                self.assertLess(count, len(data))
            entries[temporary].extend(data[:count])
            writes.append((data, count, len(entries[temporary])))
            self.assertEqual(len(entries[temporary]), offsets[index])
            events.append(("write", count))
            return count

        def linked(source, destination, **kwargs):
            self.assertEqual((source, destination), (temporary, target))
            self.assertEqual(kwargs, dict(src_dir_fd=40, dst_dir_fd=40, follow_symlinks=False))
            self.assertEqual(bytes(entries[source]), payload)
            self.assertNotIn(destination, entries)
            entries[destination] = entries[source]
            events.append(("link", target))

        def unlinked(name, *, dir_fd):
            self.assertEqual((name, dir_fd), (temporary, 40))
            del entries[name]
            events.append(("unlink", name))

        def inspected(fd):
            if fd == 40:
                return types.SimpleNamespace(st_dev=11, st_ino=140, st_uid=3, st_gid=4,
                                             st_mode=stat.S_IFDIR | 0o700)
            self.assertEqual(fd, 42)
            return types.SimpleNamespace(st_uid=3, st_gid=4, st_mode=stat.S_IFREG | 0o600)

        def reread(fd, count):
            self.assertEqual(fd, 42)
            offset = sum(len(block) for block in reads)
            self.assertEqual(count, 4097 - offset)
            block = bytes(entries[target])[offset:offset + count]
            reads.append(block)
            events.append(("read", block))
            return block

        with contextlib.ExitStack() as patches:
            for name, value in {"O_WRONLY": 1, "O_CREAT": 2, "O_EXCL": 4, "O_NOFOLLOW": 8, "O_RDONLY": 16}.items():
                patches.enter_context(mock.patch.object(common.os, name, value, create=True))
            patches.enter_context(mock.patch.object(common.os, "getuid", return_value=3, create=True))
            patches.enter_context(mock.patch.object(common.os, "getgid", return_value=4, create=True))
            choice = patches.enter_context(mock.patch.object(common.secrets, "choice", side_effect=list("AbCdEfGh")))
            op = patches.enter_context(mock.patch.object(common.os, "open", side_effect=opened))
            wr = patches.enter_context(mock.patch.object(common.os, "write", side_effect=written))
            chmod = patches.enter_context(mock.patch.object(common.os, "fchmod", create=True,
                side_effect=lambda fd, mode: events.append(("fchmod", fd, mode))))
            sync = patches.enter_context(mock.patch.object(common.os, "fsync",
                side_effect=lambda fd: events.append(("fsync", fd))))
            close = patches.enter_context(mock.patch.object(common.os, "close",
                side_effect=lambda fd: events.append(("close", fd))))
            link = patches.enter_context(mock.patch.object(common.os, "link", side_effect=linked))
            unlink = patches.enter_context(mock.patch.object(common.os, "unlink", side_effect=unlinked))
            fs = patches.enter_context(mock.patch.object(common.os, "fstat", side_effect=inspected))
            read = patches.enter_context(mock.patch.object(common.os, "read", side_effect=reread))
            validate = patches.enter_context(mock.patch.object(common, "revalidate_owned_directory",
                wraps=common.revalidate_owned_directory))
            digest = PREP.publish_owned_json(directory, target, document, "TEST", max_bytes=4096)
            self.assertEqual(wr.call_count, 3)
            self.assertEqual(writes, [(payload, 3, 3), (payload[3:], 2, 5), (payload[5:], 7, 12)])
            self.assertEqual(op.call_args_list, [mock.call(temporary, 15, 0o600, dir_fd=40),
                                               mock.call(target, 24, dir_fd=40)])
            chmod.assert_called_once_with(41, 0o600)
            self.assertEqual(sync.call_args_list, [mock.call(41), mock.call(40)])
            self.assertEqual(close.call_args_list, [mock.call(41), mock.call(42)])
            link.assert_called_once()
            unlink.assert_called_once_with(temporary, dir_fd=40)
            self.assertEqual(read.call_args_list, [mock.call(42, 4097), mock.call(42, 4085)])
            self.assertEqual(fs.call_args_list, [mock.call(40), mock.call(42), mock.call(40)])
            self.assertEqual(validate.call_args_list, [mock.call(directory, "TEST")] * 2)
            self.assertEqual(choice.call_count, 8)
        self.assertEqual(events, [("open", temporary), ("write", 3), ("write", 2), ("write", 7),
            ("fchmod", 41, 0o600), ("fsync", 41), ("close", 41), ("link", target),
            ("unlink", temporary), ("fsync", 40), ("open", target),
            ("read", payload), ("read", b""), ("close", 42)])
        self.assertEqual(reads, [payload, b""])
        self.assertEqual(entries, {target: bytearray(payload)})
        self.assertNotIn(temporary, entries)
        self.assertEqual(bytes(entries[target]).count(b"\n"), 1)
        self.assertEqual(digest, PREP.hashlib.sha256(payload).hexdigest())

    def test_publisher_temporary_open_collision_preserves_unowned_entry(self):
        common = sys.modules[PREP.publish_owned_json.__module__]
        directory = PREP.OwnedDirectory(pathlib.Path("/tmp/evidence"), 40, 11, 140, 3, 4, 0o700)
        retained = vars(directory).copy()
        target, temporary = "result.json", ".result.json.AbCdEfGh"
        preexisting = object()
        entries = {temporary: preexisting}  # Exists before this invocation; never acquired below.
        initial_entries = entries.copy()
        events, acquired_fds, created_names = [], [], []
        collision = FileExistsError(17, "preexisting temporary basename", temporary)
        info = types.SimpleNamespace(st_dev=11, st_ino=140, st_uid=3, st_gid=4,
                                     st_mode=stat.S_IFDIR | 0o700)

        def exclusive_open(name, flags, mode, *, dir_fd):
            events.append(("open", name))
            self.assertEqual((name, flags, mode, dir_fd), (temporary, 15, 0o600, 40))
            self.assertTrue(flags & common.os.O_CREAT)
            self.assertTrue(flags & common.os.O_EXCL)
            self.assertIs(entries[name], preexisting)
            raise collision

        with contextlib.ExitStack() as patches:
            for name, value in {"O_WRONLY": 1, "O_CREAT": 2, "O_EXCL": 4, "O_NOFOLLOW": 8}.items():
                patches.enter_context(mock.patch.object(common.os, name, value, create=True))
            choice = patches.enter_context(mock.patch.object(common.secrets, "choice", side_effect=list("AbCdEfGh")))
            opened = patches.enter_context(mock.patch.object(common.os, "open", side_effect=exclusive_open))
            unlinked = patches.enter_context(mock.patch.object(common.os, "unlink"))
            inspected = patches.enter_context(mock.patch.object(common.os, "fstat", return_value=info))
            serialized = patches.enter_context(mock.patch.object(common.json, "dumps", wraps=common.json.dumps))
            digest = patches.enter_context(mock.patch.object(common.hashlib, "sha256"))
            later = {name: patches.enter_context(mock.patch.object(common.os, name, create=True))
                     for name in ("write", "fchmod", "fsync", "close", "link", "read", "stat")}
            self.assertEqual(initial_entries, {temporary: preexisting})
            self.assertNotIn(target, entries)
            with self.assertRaises(PREP.Failure) as caught:
                PREP.publish_owned_json(directory, target, {"ok": True}, "TEST")
            self.assertIs(type(caught.exception), PREP.Failure)
            self.assertEqual((caught.exception.code, caught.exception.stage),
                             ("EVIDENCE_NO_REPLACE_CONFLICT", "TEST"))
            self.assertIs(caught.exception.__context__, collision)
            opened.assert_called_once_with(temporary, 15, 0o600, dir_fd=40)
            unlinked.assert_not_called()
            inspected.assert_called_once_with(40)  # Initial retained-directory validation only.
            serialized.assert_called_once_with({"ok": True}, sort_keys=True, separators=(",", ":"))
            self.assertEqual(choice.call_count, 8)
            for operation in later.values():
                operation.assert_not_called()
            digest.assert_not_called()
        self.assertEqual(events, [("open", temporary)])
        self.assertEqual((acquired_fds, created_names), ([], []))
        self.assertEqual(entries, initial_entries)
        self.assertIs(entries[temporary], preexisting)
        self.assertNotIn(target, initial_entries)
        self.assertNotIn(target, entries)
        self.assertEqual(vars(directory), retained)

    def _publisher_temporary_ownership_case(self, scenario):
        common = sys.modules[PREP.publish_owned_json.__module__]
        directory = PREP.OwnedDirectory(pathlib.Path("/tmp/evidence"), 40, 11, 140, 3, 4, 0o700)
        retained = vars(directory).copy()
        temporary, target = ".result.json.AbCdEfGh", "result.json"
        existing_target = bytearray(b"previous publication")
        entries = {target: existing_target} if scenario == "target_collision" else {}
        self.assertNotIn(temporary, entries)
        initial_target = bytes(existing_target)
        created, acquired, events = [], [], []
        payload = b'{"ok":true}\n'
        fault = (FileExistsError(17, "preexisting final target", target)
                 if scenario == "target_collision" else OSError(5, "write ownership control"))
        offset = 0

        def open_entry(name, flags, mode=None, *, dir_fd):
            events.append(("open", name))
            self.assertEqual(dir_fd, 40)
            if name == temporary:
                self.assertEqual((flags, mode), (15, 0o600))
                self.assertNotIn(name, entries)
                entries[name] = bytearray()
                created.append(name); acquired.append(41)
                return 41
            self.assertEqual((scenario, name, flags, mode), ("success", target, 24, None))
            self.assertIn(target, entries)
            return 42

        def write_entry(fd, view):
            events.append(("write", fd))
            self.assertEqual(fd, 41)
            self.assertEqual(bytes(view), payload)
            if scenario == "prelink":
                raise fault
            entries[temporary].extend(view)
            return len(view)

        def link_entry(source, destination, *, src_dir_fd, dst_dir_fd, follow_symlinks):
            events.append(("link", destination))
            self.assertEqual((source, destination, src_dir_fd, dst_dir_fd, follow_symlinks),
                             (temporary, target, 40, 40, False))
            self.assertEqual(bytes(entries[source]), payload)
            if destination in entries:
                self.assertIs(entries[destination], existing_target)
                raise fault
            entries[destination] = entries[source]

        def unlink_entry(name, *, dir_fd):
            events.append(("unlink", name))
            self.assertEqual((name, dir_fd), (temporary, 40))
            self.assertEqual((created, acquired), ([temporary], [41]))
            self.assertIn(name, entries)
            del entries[name]

        def inspect(fd):
            if fd == 40:
                return types.SimpleNamespace(st_dev=11, st_ino=140, st_uid=3, st_gid=4,
                                             st_mode=stat.S_IFDIR | 0o700)
            self.assertEqual((scenario, fd), ("success", 42))
            return types.SimpleNamespace(st_mode=stat.S_IFREG | 0o600, st_uid=3, st_gid=4)

        def read_entry(fd, count):
            nonlocal offset
            self.assertEqual((fd, count), (42, 65537 - offset))
            block = bytes(entries[target][offset:offset + count])
            offset += len(block)
            return block

        def record(operation):
            def action(fd, *args):
                events.append((operation, fd))
            return action

        with contextlib.ExitStack() as patches:
            for name, value in {"O_WRONLY": 1, "O_CREAT": 2, "O_EXCL": 4,
                                "O_NOFOLLOW": 8, "O_RDONLY": 16}.items():
                patches.enter_context(mock.patch.object(common.os, name, value, create=True))
            patches.enter_context(mock.patch.object(common.os, "getuid", return_value=3, create=True))
            patches.enter_context(mock.patch.object(common.os, "getgid", return_value=4, create=True))
            choice = patches.enter_context(mock.patch.object(common.secrets, "choice", side_effect=list("AbCdEfGh")))
            opened = patches.enter_context(mock.patch.object(common.os, "open", side_effect=open_entry))
            writer = patches.enter_context(mock.patch.object(common.os, "write", side_effect=write_entry))
            linked = patches.enter_context(mock.patch.object(common.os, "link", side_effect=link_entry))
            unlinked = patches.enter_context(mock.patch.object(common.os, "unlink", side_effect=unlink_entry))
            chmod = patches.enter_context(mock.patch.object(common.os, "fchmod", side_effect=record("fchmod"), create=True))
            synced = patches.enter_context(mock.patch.object(common.os, "fsync", side_effect=record("fsync")))
            closed = patches.enter_context(mock.patch.object(common.os, "close", side_effect=record("close")))
            inspected = patches.enter_context(mock.patch.object(common.os, "fstat", side_effect=inspect))
            reader = patches.enter_context(mock.patch.object(common.os, "read", side_effect=read_entry))
            digest = patches.enter_context(mock.patch.object(common.hashlib, "sha256", wraps=common.hashlib.sha256))
            if scenario == "success":
                result = PREP.publish_owned_json(directory, target, {"ok": True}, "TEST")
                self.assertEqual(result, __import__("hashlib").new("sha256", payload).hexdigest())
                digest.assert_called_once_with(payload)
                self.assertEqual(bytes(entries[target]), payload)
                self.assertEqual(opened.call_args_list, [mock.call(temporary, 15, 0o600, dir_fd=40),
                                                        mock.call(target, 24, dir_fd=40)])
                self.assertEqual(synced.call_args_list, [mock.call(41), mock.call(40)])
                self.assertEqual(closed.call_args_list, [mock.call(41), mock.call(42)])
                self.assertEqual(inspected.call_args_list, [mock.call(40), mock.call(42), mock.call(40)])
                self.assertEqual(reader.call_count, 2)
                self.assertLess(events.index(("unlink", temporary)), events.index(("fsync", 40)))
                self.assertLess(events.index(("fsync", 40)), events.index(("open", target)))
            else:
                with self.assertRaises(PREP.Failure) as caught:
                    PREP.publish_owned_json(directory, target, {"ok": True}, "TEST")
                self.assertIs(type(caught.exception), PREP.Failure)
                expected = "EVIDENCE_PUBLICATION_FAILED" if scenario == "prelink" else "EVIDENCE_NO_REPLACE_CONFLICT"
                self.assertEqual((caught.exception.code, caught.exception.stage), (expected, "TEST"))
                self.assertIs(caught.exception.__context__, fault)
                opened.assert_called_once_with(temporary, 15, 0o600, dir_fd=40)
                closed.assert_called_once_with(41)
                inspected.assert_called_once_with(40)
                reader.assert_not_called(); digest.assert_not_called()
                if scenario == "prelink":
                    linked.assert_not_called(); chmod.assert_not_called(); synced.assert_not_called()
                    self.assertNotIn(target, entries)
                else:
                    linked.assert_called_once_with(temporary, target, src_dir_fd=40, dst_dir_fd=40,
                                                   follow_symlinks=False)
                    self.assertIs(entries[target], existing_target)
                    self.assertEqual(bytes(entries[target]), initial_target)
                    synced.assert_called_once_with(41)
            writer.assert_called_once()
            if scenario != "prelink":
                chmod.assert_called_once_with(41, 0o600)
            unlinked.assert_called_once_with(temporary, dir_fd=40)
            self.assertEqual(choice.call_count, 8)
        self.assertEqual((created, acquired), ([temporary], [41]))
        self.assertNotIn(temporary, entries)
        self.assertEqual(vars(directory), retained)
        self.assertLess(events.index(("close", 41)), events.index(("unlink", temporary)))

    def test_publisher_owned_temporary_is_cleaned_after_prelink_failure(self):
        self._publisher_temporary_ownership_case("prelink")

    def test_publisher_success_unlinks_owned_temporary_exactly_once(self):
        self._publisher_temporary_ownership_case("success")

    def test_publisher_final_target_collision_cleans_owned_temporary_only(self):
        self._publisher_temporary_ownership_case("target_collision")

    def _publisher_cleanup_exception_case(self, fault):
        common = sys.modules[PREP.publish_owned_json.__module__]
        directory = PREP.OwnedDirectory(pathlib.Path("/tmp/evidence"), 40, 11, 140, 3, 4, 0o700)
        retained = vars(directory).copy()
        temporary, target = ".result.json.AbCdEfGh", "result.json"
        entries, acquired, events = {}, [], []
        primary = OSError(5, "PRIMARY_WRITE_FAILURE")
        cleanup = OSError(9, "CLEANUP_CLOSE_FAILURE")
        unlink_error = OSError(13, "CLEANUP_UNLINK_FAILURE")
        initial_close = OSError(5, "INITIAL_CLOSE_FAILURE")
        created_entry = bytearray()
        info = types.SimpleNamespace(st_dev=11, st_ino=140, st_uid=3, st_gid=4,
                                     st_mode=stat.S_IFDIR | 0o700)

        def exclusive_open(name, flags, mode, *, dir_fd):
            self.assertEqual((name, flags, mode, dir_fd), (temporary, 15, 0o600, 40))
            self.assertNotIn(name, entries)
            events.append(("open", name))
            entries[name] = created_entry
            acquired.append(41)
            return 41

        def failing_write(fd, view):
            self.assertEqual(fd, 41)
            self.assertEqual(bytes(view), b'{"ok":true}\n')
            self.assertIs(entries[temporary], created_entry)
            events.append(("write", fd))
            if fault == "initial_close":
                created_entry.extend(view)
                return len(view)
            raise primary

        def failing_cleanup_close(fd):
            self.assertEqual(fd, 41)
            self.assertEqual(events[:2], [("open", temporary), ("write", 41)])
            self.assertIs(entries[temporary], created_entry)
            events.append(("close", fd))
            if fault == "initial_close":
                raise initial_close
            if fault == "cleanup_close":
                raise cleanup

        def cleanup_unlink(name, *, dir_fd):
            self.assertEqual((name, dir_fd), (temporary, 40))
            self.assertIs(entries[name], created_entry)
            self.assertEqual(events[-1], ("close", 41))
            events.append(("unlink", name))
            if fault == "cleanup_unlink":
                raise unlink_error
            del entries[name]

        self.assertEqual(entries, {})
        with contextlib.ExitStack() as patches:
            for name, value in {"O_WRONLY": 1, "O_CREAT": 2, "O_EXCL": 4, "O_NOFOLLOW": 8}.items():
                patches.enter_context(mock.patch.object(common.os, name, value, create=True))
            choice = patches.enter_context(mock.patch.object(common.secrets, "choice", side_effect=list("AbCdEfGh")))
            opened = patches.enter_context(mock.patch.object(common.os, "open", side_effect=exclusive_open))
            writer = patches.enter_context(mock.patch.object(common.os, "write", side_effect=failing_write))
            closed = patches.enter_context(mock.patch.object(common.os, "close", side_effect=failing_cleanup_close))
            unlinked = patches.enter_context(mock.patch.object(common.os, "unlink", side_effect=cleanup_unlink))
            inspected = patches.enter_context(mock.patch.object(common.os, "fstat", return_value=info))
            serialized = patches.enter_context(mock.patch.object(common.json, "dumps", wraps=common.json.dumps))
            digest = patches.enter_context(mock.patch.object(common.hashlib, "sha256"))
            later = {name: patches.enter_context(mock.patch.object(common.os, name, create=True))
                     for name in ("fchmod", "fsync", "link", "read", "stat")}
            with self.assertRaises(PREP.Failure) as caught:
                PREP.publish_owned_json(directory, target, {"ok": True}, "TEST")
            self.assertIs(type(caught.exception), PREP.Failure)
            self.assertEqual((caught.exception.code, caught.exception.stage),
                             ("EVIDENCE_PUBLICATION_FAILED", "TEST"))
            expected_primary = initial_close if fault == "initial_close" else primary
            self.assertIs(caught.exception.__context__, expected_primary)
            self.assertIsNot(caught.exception, cleanup)
            self.assertIsNot(caught.exception, unlink_error)
            self.assertIsNone(caught.exception.__cause__)
            self.assertIsNone(expected_primary.__cause__)
            self.assertIsNone(expected_primary.__context__)
            self.assertFalse(caught.exception.__suppress_context__)
            opened.assert_called_once_with(temporary, 15, 0o600, dir_fd=40)
            writer.assert_called_once()
            closed.assert_called_once_with(41)
            unlinked.assert_called_once_with(temporary, dir_fd=40)
            inspected.assert_called_once_with(40)  # Directory validation, not result verification.
            serialized.assert_called_once_with({"ok": True}, sort_keys=True, separators=(",", ":"))
            self.assertEqual(choice.call_count, 8)
            for name, operation in later.items():
                if fault == "initial_close" and name == "fchmod":
                    operation.assert_called_once_with(41, 0o600)
                elif fault == "initial_close" and name == "fsync":
                    operation.assert_called_once_with(41)
                else:
                    operation.assert_not_called()
            digest.assert_not_called()
        self.assertEqual(events, [("open", temporary), ("write", 41), ("close", 41), ("unlink", temporary)])
        self.assertEqual(acquired, [41])
        if fault == "cleanup_unlink":
            self.assertEqual(entries, {temporary: created_entry})
            self.assertIs(entries[temporary], created_entry)
        else:
            self.assertEqual(entries, {})
        self.assertEqual(bytes(created_entry), b'{"ok":true}\n' if fault == "initial_close" else b"")
        self.assertNotIn(target, entries)
        self.assertEqual(vars(directory), retained)

    def test_publisher_cleanup_close_failure_preserves_primary_error_and_continues_cleanup(self):
        self._publisher_cleanup_exception_case("cleanup_close")

    def test_publisher_cleanup_unlink_failure_preserves_primary_error(self):
        self._publisher_cleanup_exception_case("cleanup_unlink")

    def test_publisher_initial_close_failure_is_not_retried_and_cleans_owned_temporary(self):
        self._publisher_cleanup_exception_case("initial_close")

    def _publisher_verification_close_case(self, fault):
        common = sys.modules[PREP.publish_owned_json.__module__]
        directory = PREP.OwnedDirectory(pathlib.Path("/tmp/evidence"), 40, 11, 140, 3, 4, 0o700)
        temporary, target = ".result.json.AbCdEfGh", "result.json"
        payload, mismatch = b'{"ok":true}\n', b'{"ok":null}\n'
        entries, events = {}, []
        close_error = OSError(9, "VERIFICATION_CLOSE_FAILURE")
        primary_seen = []
        read_error = OSError(5, "PRIMARY_VERIFICATION_READ_FAILURE")
        reads = iter([payload if fault == "normal_close" else mismatch, b""])

        def opened(name, flags, mode=None, *, dir_fd):
            self.assertEqual(dir_fd, 40)
            events.append(("open", name))
            if name == temporary:
                self.assertEqual((flags, mode), (15, 0o600))
                self.assertNotIn(name, entries)
                entries[name] = bytearray()
                return 41
            self.assertEqual((name, flags, mode), (target, 24, None))
            self.assertNotIn(temporary, entries)
            self.assertEqual(bytes(entries[target]), payload)
            self.assertEqual(events[-2], ("fsync", 40))
            return 42

        def written(fd, view):
            self.assertEqual(fd, 41)
            entries[temporary].extend(view)
            return len(view)

        def linked(source, destination, *, src_dir_fd, dst_dir_fd, follow_symlinks):
            self.assertEqual((source, destination, src_dir_fd, dst_dir_fd, follow_symlinks),
                             (temporary, target, 40, 40, False))
            self.assertNotIn(target, entries)
            self.assertEqual(events[-1], ("close", 41))
            entries[target] = entries[source]
            events.append(("link", target))

        def unlinked(name, *, dir_fd):
            self.assertEqual((name, dir_fd), (temporary, 40))
            del entries[name]
            events.append(("unlink", name))

        def inspected(fd):
            if fd == 40:
                return types.SimpleNamespace(st_dev=11, st_ino=140, st_uid=3, st_gid=4,
                                             st_mode=stat.S_IFDIR | 0o700)
            self.assertEqual(fd, 42)
            return types.SimpleNamespace(st_mode=stat.S_IFREG | 0o600, st_uid=3, st_gid=4)

        def reread(fd, count):
            self.assertEqual(fd, 42)
            self.assertGreaterEqual(count, 65537 - len(mismatch))
            if fault == "read":
                raise read_error
            return next(reads)

        def closed(fd):
            events.append(("close", fd))
            if fd == 42:
                active = sys.exc_info()[1]
                if fault == "confirmation":
                    self.assertIs(type(active), PREP.Failure)
                    self.assertEqual((active.code, active.stage), ("EVIDENCE_CONFIRMATION_FAILED", "TEST"))
                elif fault == "read":
                    self.assertIs(active, read_error)
                else:
                    self.assertIsNone(active)
                primary_seen.append(active)
                raise close_error
            self.assertEqual(fd, 41)

        with contextlib.ExitStack() as patches:
            for name, value in {"O_WRONLY": 1, "O_CREAT": 2, "O_EXCL": 4, "O_NOFOLLOW": 8, "O_RDONLY": 16}.items():
                patches.enter_context(mock.patch.object(common.os, name, value, create=True))
            patches.enter_context(mock.patch.object(common.os, "getuid", return_value=3, create=True))
            patches.enter_context(mock.patch.object(common.os, "getgid", return_value=4, create=True))
            patches.enter_context(mock.patch.object(common.secrets, "choice", side_effect=list("AbCdEfGh")))
            op = patches.enter_context(mock.patch.object(common.os, "open", side_effect=opened))
            wr = patches.enter_context(mock.patch.object(common.os, "write", side_effect=written))
            chmod = patches.enter_context(mock.patch.object(common.os, "fchmod", create=True))
            fsync = patches.enter_context(mock.patch.object(common.os, "fsync", side_effect=lambda fd: events.append(("fsync", fd))))
            cl = patches.enter_context(mock.patch.object(common.os, "close", side_effect=closed))
            link = patches.enter_context(mock.patch.object(common.os, "link", side_effect=linked))
            unlink = patches.enter_context(mock.patch.object(common.os, "unlink", side_effect=unlinked))
            fstat = patches.enter_context(mock.patch.object(common.os, "fstat", side_effect=inspected))
            read = patches.enter_context(mock.patch.object(common.os, "read", side_effect=reread))
            digest = patches.enter_context(mock.patch.object(common.hashlib, "sha256"))
            with self.assertRaises(PREP.Failure) as caught:
                PREP.publish_owned_json(directory, target, {"ok": True}, "TEST")
            self.assertIs(type(caught.exception), PREP.Failure)
            expected_code = "EVIDENCE_CONFIRMATION_FAILED" if fault == "confirmation" else "EVIDENCE_PUBLICATION_FAILED"
            self.assertEqual((caught.exception.code, caught.exception.stage), (expected_code, "TEST"))
            self.assertEqual(len(primary_seen), 1)
            if fault == "confirmation":
                self.assertIs(caught.exception, primary_seen[0])
                self.assertIsNone(caught.exception.__context__)
            else:
                self.assertIs(caught.exception.__context__, read_error if fault == "read" else close_error)
            self.assertIsNone(caught.exception.__cause__)
            self.assertIsNone(read_error.__cause__)
            self.assertIsNone(read_error.__context__)
            self.assertEqual(op.call_args_list, [mock.call(temporary, 15, 0o600, dir_fd=40), mock.call(target, 24, dir_fd=40)])
            wr.assert_called_once(); chmod.assert_called_once_with(41, 0o600)
            self.assertEqual(fsync.call_args_list, [mock.call(41), mock.call(40)])
            self.assertEqual(cl.call_args_list, [mock.call(41), mock.call(42)])
            link.assert_called_once(); unlink.assert_called_once_with(temporary, dir_fd=40)
            self.assertEqual(fstat.call_args_list, [mock.call(40), mock.call(42)])
            expected_reads = [mock.call(42, 65537)]
            if fault != "read":
                expected_reads.append(mock.call(42, 65537-len(mismatch)))
            self.assertEqual(read.call_args_list, expected_reads)
            digest.assert_not_called()
        self.assertEqual(entries, {target: bytearray(payload)})
        self.assertNotIn(temporary, entries)

    def test_publisher_verification_close_failure_preserves_primary_verification_failure(self):
        self._publisher_verification_close_case("confirmation")

    def test_publisher_verification_normal_close_failure_is_not_retried(self):
        self._publisher_verification_close_case("normal_close")

    def test_publisher_verification_cleanup_close_failure_preserves_primary_read_error(self):
        self._publisher_verification_close_case("read")

    def test_publisher_explicit_unlink_failure_preserves_published_result(self):
        common = sys.modules[PREP.publish_owned_json.__module__]
        directory = PREP.OwnedDirectory(pathlib.Path("/tmp/evidence"), 40, 11, 140, 3, 4, 0o700)
        temporary, target = ".result.json.AbCdEfGh", "result.json"
        payload = b'{"ok":true}\n'
        entries, events = {}, []
        primary = OSError(5, "EXPLICIT_TEMPORARY_UNLINK_FAILURE")
        unlink_attempts = 0
        published = []

        def opened(name, flags, mode, *, dir_fd):
            self.assertEqual((name, flags, mode, dir_fd), (temporary, 15, 0o600, 40))
            self.assertEqual(entries, {})
            entries[name] = bytearray()
            events.append("open")
            return 41

        def written(fd, view):
            self.assertEqual((fd, bytes(view)), (41, payload))
            entries[temporary].extend(view)
            events.append("write")
            return len(view)

        def linked(source, destination, *, src_dir_fd, dst_dir_fd, follow_symlinks):
            self.assertEqual((source, destination, src_dir_fd, dst_dir_fd, follow_symlinks),
                             (temporary, target, 40, 40, False))
            self.assertNotIn(target, entries)
            self.assertEqual(events[-1], "close")
            self.assertEqual(bytes(entries[source]), payload)
            entries[target] = entries[source]
            published.append(entries[target])
            events.append("link")

        def unlinked(name, *, dir_fd):
            nonlocal unlink_attempts
            self.assertEqual((name, dir_fd), (temporary, 40))
            self.assertIs(entries[target], published[0])
            self.assertEqual(bytes(entries[target]), payload)
            self.assertIs(entries[name], published[0])
            unlink_attempts += 1
            events.append("unlink")
            if unlink_attempts == 1:
                self.assertEqual(events[-2], "link")
                raise primary
            self.assertEqual(unlink_attempts, 2)
            active = sys.exc_info()[1]
            self.assertIs(type(active), PREP.Failure)
            self.assertEqual((active.code, active.stage), ("EVIDENCE_PUBLICATION_FAILED", "TEST"))
            del entries[name]

        def record(name):
            def action(fd, *args):
                self.assertEqual(fd, 41)
                events.append(name)
            return action

        info = types.SimpleNamespace(st_dev=11, st_ino=140, st_uid=3, st_gid=4,
                                     st_mode=stat.S_IFDIR | 0o700)
        with contextlib.ExitStack() as patches:
            for name, value in {"O_WRONLY": 1, "O_CREAT": 2, "O_EXCL": 4, "O_NOFOLLOW": 8}.items():
                patches.enter_context(mock.patch.object(common.os, name, value, create=True))
            choice = patches.enter_context(mock.patch.object(common.secrets, "choice", side_effect=list("AbCdEfGh")))
            op = patches.enter_context(mock.patch.object(common.os, "open", side_effect=opened))
            wr = patches.enter_context(mock.patch.object(common.os, "write", side_effect=written))
            chmod = patches.enter_context(mock.patch.object(common.os, "fchmod", side_effect=record("fchmod"), create=True))
            fsync = patches.enter_context(mock.patch.object(common.os, "fsync", side_effect=record("fsync")))
            close = patches.enter_context(mock.patch.object(common.os, "close", side_effect=record("close")))
            link = patches.enter_context(mock.patch.object(common.os, "link", side_effect=linked))
            unlink = patches.enter_context(mock.patch.object(common.os, "unlink", side_effect=unlinked))
            fstat = patches.enter_context(mock.patch.object(common.os, "fstat", return_value=info))
            read = patches.enter_context(mock.patch.object(common.os, "read"))
            digest = patches.enter_context(mock.patch.object(common.hashlib, "sha256"))
            with self.assertRaises(PREP.Failure) as caught:
                PREP.publish_owned_json(directory, target, {"ok": True}, "TEST")
            self.assertIs(type(caught.exception), PREP.Failure)
            self.assertEqual((caught.exception.code, caught.exception.stage), ("EVIDENCE_PUBLICATION_FAILED", "TEST"))
            self.assertIs(caught.exception.__context__, primary)
            self.assertIsNone(caught.exception.__cause__)
            self.assertIsNone(primary.__context__)
            op.assert_called_once_with(temporary, 15, 0o600, dir_fd=40)
            wr.assert_called_once(); chmod.assert_called_once_with(41, 0o600)
            fsync.assert_called_once_with(41); close.assert_called_once_with(41)
            link.assert_called_once_with(temporary, target, src_dir_fd=40, dst_dir_fd=40, follow_symlinks=False)
            self.assertEqual(unlink.call_args_list, [mock.call(temporary, dir_fd=40)] * 2)
            fstat.assert_called_once_with(40)
            read.assert_not_called(); digest.assert_not_called()
            self.assertEqual(choice.call_count, 8)
        self.assertEqual(events, ["open", "write", "fchmod", "fsync", "close", "link", "unlink", "unlink"])
        self.assertEqual(entries, {target: bytearray(payload)})
        self.assertIs(entries[target], published[0])
        self.assertNotIn(temporary, entries)

    def test_publisher_explicit_unlink_and_cleanup_retry_failure_preserves_primary_error_and_result(self):
        common = sys.modules[PREP.publish_owned_json.__module__]
        directory = PREP.OwnedDirectory(pathlib.Path("/tmp/evidence"), 40, 11, 140, 3, 4, 0o700)
        temporary, target = ".result.json.AbCdEfGh", "result.json"
        payload = b'{"ok":true}\n'
        entries, events = {}, []
        primary = OSError(5, "EXPLICIT_TEMPORARY_UNLINK_FAILURE")
        cleanup_error = OSError(13, "CLEANUP_TEMPORARY_UNLINK_FAILURE")
        unlink_attempts = 0
        published = []

        def opened(name, flags, mode, *, dir_fd):
            self.assertEqual((name, flags, mode, dir_fd), (temporary, 15, 0o600, 40))
            self.assertEqual(entries, {})
            entries[name] = bytearray()
            events.append("open")
            return 41

        def written(fd, view):
            self.assertEqual((fd, bytes(view)), (41, payload))
            entries[temporary].extend(view)
            events.append("write")
            return len(view)

        def linked(source, destination, *, src_dir_fd, dst_dir_fd, follow_symlinks):
            self.assertEqual((source, destination, src_dir_fd, dst_dir_fd, follow_symlinks),
                             (temporary, target, 40, 40, False))
            self.assertNotIn(target, entries)
            self.assertEqual(events[-1], "close")
            self.assertEqual(bytes(entries[source]), payload)
            entries[target] = entries[source]
            published.append(entries[target])
            events.append("link")

        def unlinked(name, *, dir_fd):
            nonlocal unlink_attempts
            self.assertEqual((name, dir_fd), (temporary, 40))
            self.assertIs(entries[target], published[0])
            self.assertEqual(bytes(entries[target]), payload)
            self.assertIs(entries[name], published[0])
            unlink_attempts += 1
            events.append("unlink")
            if unlink_attempts == 1:
                self.assertEqual(events[-2], "link")
                raise primary
            self.assertEqual(unlink_attempts, 2)
            active = sys.exc_info()[1]
            self.assertIs(type(active), PREP.Failure)
            self.assertEqual((active.code, active.stage), ("EVIDENCE_PUBLICATION_FAILED", "TEST"))
            raise cleanup_error

        def record(name):
            def action(fd, *args):
                self.assertEqual(fd, 41)
                events.append(name)
            return action

        info = types.SimpleNamespace(st_dev=11, st_ino=140, st_uid=3, st_gid=4,
                                     st_mode=stat.S_IFDIR | 0o700)
        with contextlib.ExitStack() as patches:
            for name, value in {"O_WRONLY": 1, "O_CREAT": 2, "O_EXCL": 4, "O_NOFOLLOW": 8}.items():
                patches.enter_context(mock.patch.object(common.os, name, value, create=True))
            choice = patches.enter_context(mock.patch.object(common.secrets, "choice", side_effect=list("AbCdEfGh")))
            op = patches.enter_context(mock.patch.object(common.os, "open", side_effect=opened))
            wr = patches.enter_context(mock.patch.object(common.os, "write", side_effect=written))
            chmod = patches.enter_context(mock.patch.object(common.os, "fchmod", side_effect=record("fchmod"), create=True))
            fsync = patches.enter_context(mock.patch.object(common.os, "fsync", side_effect=record("fsync")))
            close = patches.enter_context(mock.patch.object(common.os, "close", side_effect=record("close")))
            link = patches.enter_context(mock.patch.object(common.os, "link", side_effect=linked))
            unlink = patches.enter_context(mock.patch.object(common.os, "unlink", side_effect=unlinked))
            fstat = patches.enter_context(mock.patch.object(common.os, "fstat", return_value=info))
            read = patches.enter_context(mock.patch.object(common.os, "read"))
            digest = patches.enter_context(mock.patch.object(common.hashlib, "sha256"))
            with self.assertRaises(PREP.Failure) as caught:
                PREP.publish_owned_json(directory, target, {"ok": True}, "TEST")
            self.assertIs(type(caught.exception), PREP.Failure)
            self.assertEqual((caught.exception.code, caught.exception.stage), ("EVIDENCE_PUBLICATION_FAILED", "TEST"))
            self.assertIs(caught.exception.__context__, primary)
            self.assertIsNone(caught.exception.__cause__)
            self.assertIsNone(primary.__context__)
            self.assertIsNone(primary.__cause__)
            self.assertIsNot(caught.exception, cleanup_error)
            self.assertIsNot(caught.exception.__context__, cleanup_error)
            chain = caught.exception
            seen = set()
            while chain is not None and id(chain) not in seen:
                seen.add(id(chain))
                self.assertIsNot(chain, cleanup_error)
                self.assertIsNone(chain.__cause__)
                chain = chain.__context__
            op.assert_called_once_with(temporary, 15, 0o600, dir_fd=40)
            wr.assert_called_once(); chmod.assert_called_once_with(41, 0o600)
            fsync.assert_called_once_with(41); close.assert_called_once_with(41)
            link.assert_called_once_with(temporary, target, src_dir_fd=40, dst_dir_fd=40, follow_symlinks=False)
            self.assertEqual(unlink.call_args_list, [mock.call(temporary, dir_fd=40)] * 2)
            fstat.assert_called_once_with(40)
            read.assert_not_called(); digest.assert_not_called()
            self.assertEqual(choice.call_count, 8)
        self.assertEqual(events, ["open", "write", "fchmod", "fsync", "close", "link", "unlink", "unlink"])
        self.assertEqual(entries, {target: bytearray(payload), temporary: bytearray(payload)})
        self.assertIs(entries[target], published[0])
        self.assertIs(entries[temporary], published[0])

    def test_publisher_directory_fsync_failure_preserves_published_result(self):
        common = sys.modules[PREP.publish_owned_json.__module__]
        directory = PREP.OwnedDirectory(pathlib.Path("/tmp/evidence"), 40, 11, 140, 3, 4, 0o700)
        temporary, target = ".result.json.AbCdEfGh", "result.json"
        payload = b'{"ok":true}\n'
        entries, events = {}, []
        primary = OSError(5, "PUBLICATION_DIRECTORY_FSYNC_FAILURE")
        unlink_attempts = 0
        published = []

        def opened(name, flags, mode, *, dir_fd):
            self.assertEqual((name, flags, mode, dir_fd), (temporary, 15, 0o600, 40))
            self.assertEqual(entries, {})
            entries[name] = bytearray()
            events.append("open")
            return 41

        def written(fd, view):
            self.assertEqual((fd, bytes(view)), (41, payload))
            entries[temporary].extend(view)
            events.append("write")
            return len(view)

        def linked(source, destination, *, src_dir_fd, dst_dir_fd, follow_symlinks):
            self.assertEqual((source, destination, src_dir_fd, dst_dir_fd, follow_symlinks),
                             (temporary, target, 40, 40, False))
            self.assertNotIn(target, entries)
            self.assertEqual(events[-1], "close")
            self.assertEqual(bytes(entries[source]), payload)
            entries[target] = entries[source]
            published.append(entries[target])
            events.append("link")

        def unlinked(name, *, dir_fd):
            nonlocal unlink_attempts
            self.assertEqual((name, dir_fd), (temporary, 40))
            self.assertIs(entries[target], published[0])
            self.assertEqual(bytes(entries[target]), payload)
            self.assertIs(entries[name], published[0])
            unlink_attempts += 1
            events.append("unlink")
            self.assertEqual(unlink_attempts, 1)
            self.assertEqual(events[-2], "link")
            del entries[name]

        def synced(fd):
            if fd == 41:
                events.append("fsync")
                return
            self.assertEqual(fd, 40)
            self.assertEqual(events[-1], "unlink")
            self.assertNotIn(temporary, entries)
            self.assertIs(entries[target], published[0])
            self.assertEqual(bytes(entries[target]), payload)
            events.append("directory_fsync")
            raise primary

        def record(name):
            def action(fd, *args):
                self.assertEqual(fd, 41)
                events.append(name)
            return action

        info = types.SimpleNamespace(st_dev=11, st_ino=140, st_uid=3, st_gid=4,
                                     st_mode=stat.S_IFDIR | 0o700)
        with contextlib.ExitStack() as patches:
            for name, value in {"O_WRONLY": 1, "O_CREAT": 2, "O_EXCL": 4, "O_NOFOLLOW": 8}.items():
                patches.enter_context(mock.patch.object(common.os, name, value, create=True))
            choice = patches.enter_context(mock.patch.object(common.secrets, "choice", side_effect=list("AbCdEfGh")))
            op = patches.enter_context(mock.patch.object(common.os, "open", side_effect=opened))
            wr = patches.enter_context(mock.patch.object(common.os, "write", side_effect=written))
            chmod = patches.enter_context(mock.patch.object(common.os, "fchmod", side_effect=record("fchmod"), create=True))
            fsync = patches.enter_context(mock.patch.object(common.os, "fsync", side_effect=synced))
            close = patches.enter_context(mock.patch.object(common.os, "close", side_effect=record("close")))
            link = patches.enter_context(mock.patch.object(common.os, "link", side_effect=linked))
            unlink = patches.enter_context(mock.patch.object(common.os, "unlink", side_effect=unlinked))
            fstat = patches.enter_context(mock.patch.object(common.os, "fstat", return_value=info))
            read = patches.enter_context(mock.patch.object(common.os, "read"))
            digest = patches.enter_context(mock.patch.object(common.hashlib, "sha256"))
            with self.assertRaises(PREP.Failure) as caught:
                PREP.publish_owned_json(directory, target, {"ok": True}, "TEST")
            self.assertIs(type(caught.exception), PREP.Failure)
            self.assertEqual((caught.exception.code, caught.exception.stage), ("EVIDENCE_PUBLICATION_FAILED", "TEST"))
            self.assertIs(caught.exception.__context__, primary)
            self.assertIsNone(caught.exception.__cause__)
            self.assertIsNone(primary.__context__)
            op.assert_called_once_with(temporary, 15, 0o600, dir_fd=40)
            wr.assert_called_once(); chmod.assert_called_once_with(41, 0o600)
            self.assertEqual(fsync.call_args_list, [mock.call(41), mock.call(40)])
            close.assert_called_once_with(41)
            link.assert_called_once_with(temporary, target, src_dir_fd=40, dst_dir_fd=40, follow_symlinks=False)
            self.assertEqual(unlink.call_args_list, [mock.call(temporary, dir_fd=40)])
            fstat.assert_called_once_with(40)
            read.assert_not_called(); digest.assert_not_called()
            self.assertEqual(choice.call_count, 8)
        self.assertEqual(events, ["open", "write", "fchmod", "fsync", "close", "link", "unlink", "directory_fsync"])
        self.assertEqual(entries, {target: bytearray(payload)})
        self.assertIs(entries[target], published[0])
        self.assertNotIn(temporary, entries)

    def test_tmp_root_remaining_acquisition_branches(self):
        common = sys.modules[PREP.open_tmp_root.__module__]
        cases = ("OBSERVED_WRONG_TYPE", "OBSERVED_SYMLINK", "UNSUPPORTED_PRIMITIVES",
                 "OPEN_OSERROR", "OPENED_NONDIRECTORY", "RAW_LSTAT_OSERROR")
        completed = []
        for fault in cases:
            with self.subTest(fault=fault):
                kind = {"OBSERVED_WRONG_TYPE": stat.S_IFREG,
                        "OBSERVED_SYMLINK": stat.S_IFLNK}.get(fault, stat.S_IFDIR)
                observed = types.SimpleNamespace(st_dev=11, st_ino=140, st_uid=3,
                    st_gid=4, st_mode=kind | 0o1777)
                opened_info = types.SimpleNamespace(st_dev=11, st_ino=140, st_uid=3,
                    st_gid=4, st_mode=stat.S_IFREG | 0o1777)
                primary = OSError(5, "TMP_ROOT_LSTAT_FAILURE" if fault == "RAW_LSTAT_OSERROR"
                                  else "TMP_ROOT_OPEN_FAILURE")
                events, acquired, live, active = [], [], set(), []

                def observe(path):
                    self.assertEqual(path, "/tmp")
                    events.append("lstat")
                    if fault == "RAW_LSTAT_OSERROR":
                        raise primary
                    return observed

                def acquire(path, flags):
                    self.assertEqual((str(path), flags), ("/tmp", 7))
                    events.append("open")
                    if fault == "OPEN_OSERROR":
                        raise primary
                    self.assertEqual(fault, "OPENED_NONDIRECTORY")
                    acquired.append(41)
                    live.add(41)
                    return 41

                def inspect(fd):
                    self.assertEqual(fd, 41)
                    self.assertIn(fd, live)
                    events.append("fstat")
                    return opened_info

                def close(fd):
                    self.assertEqual(fd, 41)
                    self.assertIn(fd, live)
                    active.append(sys.exc_info()[1])
                    live.remove(fd)
                    events.append("close")

                with contextlib.ExitStack() as patches:
                    patches.enter_context(mock.patch.object(common.os, "name",
                        "nt" if fault == "UNSUPPORTED_PRIMITIVES" else "posix"))
                    for name, value in {"O_RDONLY": 1, "O_DIRECTORY": 2, "O_NOFOLLOW": 4}.items():
                        patches.enter_context(mock.patch.object(common.os, name, value, create=True))
                    lst = patches.enter_context(mock.patch.object(common.os, "lstat", side_effect=observe))
                    op = patches.enter_context(mock.patch.object(common.os, "open", side_effect=acquire))
                    fs = patches.enter_context(mock.patch.object(common.os, "fstat", side_effect=inspect))
                    cl = patches.enter_context(mock.patch.object(common.os, "close", side_effect=close))
                    delegated = patches.enter_context(mock.patch.object(common, "open_owned_directory",
                        wraps=common.open_owned_directory))
                    constructed = patches.enter_context(mock.patch.object(common, "OwnedDirectory",
                        wraps=PREP.OwnedDirectory))
                    mutations = [patches.enter_context(mock.patch.object(common.os, name, create=True))
                        for name in ("mkdir", "chmod", "fchmod", "chown", "fchown", "unlink",
                                     "rmdir", "remove", "rename", "replace", "fsync")]
                    returned = None
                    with self.assertRaises(OSError if fault == "RAW_LSTAT_OSERROR" else PREP.Failure) as caught:
                        returned = PREP.open_tmp_root("TEST")
                    exc = caught.exception
                    if fault == "RAW_LSTAT_OSERROR":
                        self.assertIs(exc, primary)
                        self.assertIs(type(exc), OSError)
                        self.assertNotIsInstance(exc, PREP.Failure)
                        self.assertEqual((exc.errno, exc.strerror), (5, "TMP_ROOT_LSTAT_FAILURE"))
                    else:
                        expected = {"OBSERVED_WRONG_TYPE": ("TEMP_ROOT_INVALID", "TEST"),
                            "OBSERVED_SYMLINK": ("TEMP_ROOT_INVALID", "TEST"),
                            "UNSUPPORTED_PRIMITIVES": ("POSIX_DIRECTORY_PRIMITIVES_UNAVAILABLE", "TEST"),
                            "OPEN_OSERROR": ("DIRECTORY_OPEN_FAILED", "TEST"),
                            "OPENED_NONDIRECTORY": ("DIRECTORY_TYPE_INVALID", "DIRECTORY_IDENTITY")}[fault]
                        self.assertIs(type(exc), PREP.Failure)
                        self.assertEqual((exc.code, exc.stage), expected)
                    self.assertIs(exc.__context__, primary if fault == "OPEN_OSERROR" else None)
                    self.assertIsNone(exc.__cause__)
                    self.assertIsNone(returned)
                    constructed.assert_not_called()
                    lst.assert_called_once_with("/tmp")
                    if fault in ("OPEN_OSERROR", "OPENED_NONDIRECTORY"):
                        op.assert_called_once_with(pathlib.Path("/tmp"), 7)
                    else:
                        op.assert_not_called()
                    if fault == "OPENED_NONDIRECTORY":
                        fs.assert_called_once_with(41)
                        cl.assert_called_once_with(41)
                        self.assertEqual(acquired, [41])
                        self.assertEqual(active, [exc])
                    else:
                        fs.assert_not_called()
                        cl.assert_not_called()
                        self.assertEqual(acquired, [])
                    if fault in cases[:2] or fault == "RAW_LSTAT_OSERROR":
                        delegated.assert_not_called()
                    else:
                        delegated.assert_called_once_with(pathlib.Path("/tmp"), 0o1777, "TEST",
                            expected_uid=3, expected_gid=4)
                    for operation in mutations:
                        operation.assert_not_called()
                self.assertEqual(live, set())
                self.assertEqual(events, ["lstat", "open", "fstat", "close"] if fault == "OPENED_NONDIRECTORY"
                    else ["lstat", "open"] if fault == "OPEN_OSERROR" else ["lstat"])
                completed.append(fault)
        self.assertEqual(completed, list(cases))

    def _tmp_root_ownership_case(self, fault, close_fails=True):
        common = sys.modules[PREP.open_tmp_root.__module__]
        observed = types.SimpleNamespace(st_dev=11, st_ino=140, st_uid=3, st_gid=4,
                                         st_mode=stat.S_IFDIR | 0o1777)
        opened_info = types.SimpleNamespace(**dict(vars(observed), st_uid=99 if fault == "identity" else 3))
        primary_raw = OSError(5, "PRIMARY_TMP_ROOT_FSTAT_FAILURE")
        live = set()
        cleanup = OSError(9, "TMP_ROOT_CLEANUP_CLOSE_FAILURE")
        events, primary_seen = [], []

        def observe(path):
            self.assertEqual(path, "/tmp")
            events.append("lstat")
            return observed

        def acquire(path, flags):
            self.assertEqual((str(path), flags), ("/tmp", 7))
            events.append("open")
            live.add(41)
            return 41

        def inspect(fd):
            self.assertEqual(fd, 41)
            events.append("fstat")
            self.assertIn(fd, live)
            if fault == "fstat":
                raise primary_raw
            return opened_info

        def close(fd):
            self.assertEqual(fd, 41)
            self.assertIn(fd, live)
            if fault == "success":
                live.remove(fd)
                events.append("caller_close")
                return
            self.assertEqual(events, ["lstat", "open", "fstat"])
            active = sys.exc_info()[1]
            if fault == "identity":
                self.assertIs(type(active), PREP.Failure)
                self.assertEqual((active.code, active.stage), ("DIRECTORY_IDENTITY_MISMATCH", "TEST"))
            else:
                self.assertIs(active, primary_raw)
            primary_seen.append(active)
            events.append("close")
            if close_fails:
                raise cleanup
            live.remove(fd)

        with contextlib.ExitStack() as patches:
            patches.enter_context(mock.patch.object(common.os, "name", "posix"))
            for name, value in {"O_RDONLY": 1, "O_DIRECTORY": 2, "O_NOFOLLOW": 4}.items():
                patches.enter_context(mock.patch.object(common.os, name, value, create=True))
            lst = patches.enter_context(mock.patch.object(common.os, "lstat", side_effect=observe))
            op = patches.enter_context(mock.patch.object(common.os, "open", side_effect=acquire))
            fs = patches.enter_context(mock.patch.object(common.os, "fstat", side_effect=inspect))
            cl = patches.enter_context(mock.patch.object(common.os, "close", side_effect=close))
            constructed = patches.enter_context(mock.patch.object(common, "OwnedDirectory", wraps=PREP.OwnedDirectory))
            if fault == "success":
                result = PREP.open_tmp_root("TEST")
                self.assertIsInstance(result, PREP.OwnedDirectory)
                self.assertEqual((result.path, result.fd, result.dev, result.ino, result.uid, result.gid, result.mode, result.parent),
                                 (pathlib.Path("/tmp"), 41, 11, 140, 3, 4, 0o1777, None))
                cl.assert_not_called()
                self.assertIn(result.fd, live)
                self.assertEqual(common._directory_token(result.fd), (11, 140, 3, 4, 0o1777))
                result.close()  # Explicit caller cleanup after transfer, not helper cleanup.
                self.assertEqual(result.fd, -1)
                self.assertEqual(live, set())
                constructed.assert_called_once()
            else:
                expected_type = PREP.Failure if fault == "identity" else OSError
                with self.assertRaises(expected_type) as caught:
                    PREP.open_tmp_root("TEST")
                self.assertEqual(len(primary_seen), 1)
                self.assertIs(caught.exception, primary_seen[0])
                if fault == "identity":
                    self.assertIs(type(caught.exception), PREP.Failure)
                    self.assertEqual((caught.exception.code, caught.exception.stage), ("DIRECTORY_IDENTITY_MISMATCH", "TEST"))
                else:
                    self.assertIs(caught.exception, primary_raw)
                self.assertIsNone(caught.exception.__context__)
                self.assertIsNone(caught.exception.__cause__)
                constructed.assert_not_called()
            lst.assert_called_once_with("/tmp")
            op.assert_called_once_with(pathlib.Path("/tmp"), 7)
            self.assertEqual(fs.call_args_list, [mock.call(41)] * (2 if fault == "success" else 1))
            cl.assert_called_once_with(41)
        self.assertEqual(events, ["lstat", "open", "fstat", "fstat", "caller_close"] if fault == "success" else
                         ["lstat", "open", "fstat", "close"])

    def test_tmp_root_validation_close_failure_preserves_primary_error(self):
        for close_fails in (True, False):
            with self.subTest(cleanup_close_fails=close_fails):
                self._tmp_root_ownership_case("identity", close_fails)

    def test_tmp_root_cleanup_close_failure_preserves_primary_fstat_error(self):
        self._tmp_root_ownership_case("fstat")

    def test_tmp_root_success_transfers_open_descriptor_ownership(self):
        self._tmp_root_ownership_case("success")

    def _main_retained_close_failure_case(self, success):
        names = ("evidence", "evidence_root", "environments", "root", "runtime", "anchor")
        paths = ("/tmp/hioc-pe4-runtime-hierarchy-prepare-AbCd1234", "/tmp",
                 "/home/jazofv1/hioc/runtime/pe4/environments", "/home/jazofv1/hioc/runtime/pe4",
                 "/home/jazofv1/hioc/runtime", "/home/jazofv1/hioc")
        directories = {name: PREP.OwnedDirectory(pathlib.Path(path), 40+i, 11, 140+i, 3, 4, 0o750)
                       for i, (name, path) in enumerate(zip(names, paths))}
        primary = PREP.Failure("EVIDENCE_PUBLICATION_FAILED", "EVIDENCE_PUBLICATION")
        cleanup = OSError(9, "MAIN_FINAL_HANDLE_CLOSE_FAILURE")
        output, events = io.StringIO(), []

        def close(fd):
            self.assertIn(fd, range(40, 46))
            self.assertIn("RESULT=PASS" if success else "RESULT=FAIL", output.getvalue())
            self.assertIn("STOP_REQUIRED=TRUE", output.getvalue())
            if fd == 40:
                self.assertEqual(events[-1], ("umask", 0o077))
            events.append(("close", fd))
            if fd == 40:
                raise cleanup

        def umask(value):
            events.append(("umask", value))
            return 0o077

        with mock.patch.multiple(PREP, verify_pi3=mock.Mock(), verify_repository=mock.Mock(),
                 open_trusted_owned_path_bound=mock.Mock(return_value=directories["anchor"]),
                 revalidate_path_bound_directory=mock.Mock(),
                 ensure_owned_named_child=mock.Mock(side_effect=[(directories[n], False) for n in ("runtime", "root", "environments")]),
                 open_tmp_root=mock.Mock(return_value=directories["evidence_root"]),
                 create_owned_child=mock.Mock(return_value=directories["evidence"]),
                 publish_owned_json=mock.Mock(return_value="0"*64) if success else mock.Mock(side_effect=primary)) as helpers, \
             mock.patch.object(PREP.os, "close", side_effect=close) as closed, \
             mock.patch.object(PREP.os, "umask", side_effect=umask) as masks, \
             mock.patch.object(sys, "argv", ["d-prep", "--governance-commit", "0"*40]), \
             contextlib.redirect_stdout(output):
            self.assertEqual(PREP.main(), 0 if success else 1)
            self.assertEqual(closed.call_args_list, [mock.call(fd) for fd in range(40, 46)])
            self.assertEqual(masks.call_args_list, [mock.call(0o027), mock.call(0o077)])
            PREP.publish_owned_json.assert_called_once()
            self.assertEqual(PREP.revalidate_path_bound_directory.call_args_list[-1],
                             mock.call(directories["environments"], "FINAL_VALIDATION" if success else "EVIDENCE_PUBLICATION"))
        text = output.getvalue()
        fields = dict(line.split("=", 1) for line in text.splitlines() if "=" in line)
        expected = {"RESULT": "FAIL", "ERROR_CODE": "EVIDENCE_PUBLICATION_FAILED",
                    "FAILURE_STAGE": "EVIDENCE_PUBLICATION", "DIAGNOSTIC_STAGE": "EVIDENCE_PUBLICATION",
                    "DIAGNOSTIC_OPERATION": "PUBLISH_EVIDENCE", "EXCEPTION_CLASS": "GOVERNED_FAILURE",
                    "ERRNO": "NONE", "EVIDENCE_STATE": "UNCONFIRMED",
                    "ROLLBACK_RECOMMENDED": "FALSE", "STOP_REQUIRED": "TRUE"}
        if success:
            expected = {"RESULT": "PASS", "ERROR_CODE": "NONE", "FAILURE_STAGE": "COMPLETE",
                        "EVIDENCE_STATE": "CONFIRMED", "ROLLBACK_RECOMMENDED": "FALSE", "STOP_REQUIRED": "TRUE"}
        for key, value in expected.items():
            self.assertEqual(fields[key], value)
        self.assertEqual(text.splitlines().count("RESULT=FAIL"), 0 if success else 1)
        self.assertEqual(text.splitlines().count("RESULT=PASS"), 1 if success else 0)
        self.assertEqual(text.count("EVIDENCE_DIR="), 1 if success else 0)
        if success:
            self.assertEqual(fields["EVIDENCE_DIR"], str(directories["evidence"].path))
            self.assertNotIn("DIAGNOSTIC_STAGE=", text)
        self.assertNotIn("MAIN_FINAL_HANDLE_CLOSE_FAILURE", text)
        self.assertEqual(events, [("umask", 0o027), ("umask", 0o077)] + [("close", fd) for fd in range(40, 46)])
        for i, name in enumerate(names):
            self.assertEqual(directories[name].fd, 40 if i == 0 else -1)

    def test_main_final_handle_close_failure_preserves_primary_evidence_result_and_continues_cleanup(self):
        self._main_retained_close_failure_case(False)

    def test_main_success_retained_handle_close_failure_preserves_pass_and_continues_cleanup(self):
        self._main_retained_close_failure_case(True)

    def test_path_bound_anchor_primitive_is_used(self):
        self.assertIn("open_trusted_owned_path_bound(RUNTIME", SOURCE)
        self.assertGreaterEqual(SOURCE.count("revalidate_path_bound_directory"), 7)

    def _posix_directory_token(self, info):
        self.assertTrue(stat.S_ISDIR(info.st_mode))
        return (info.st_dev, info.st_ino, info.st_uid, info.st_gid,
                stat.S_IMODE(info.st_mode))

    @contextlib.contextmanager
    def _posix_retained_leaf_chain(self):
        chain, owned_by_fd = [], {}

        def close_retained(fd):
            directory = owned_by_fd.pop(fd, None)
            if directory is None:
                os.close(fd)
            else:
                directory.close()

        with contextlib.ExitStack() as cleanup:
            temporary = cleanup.enter_context(tempfile.TemporaryDirectory())
            root_path = pathlib.Path(temporary)
            paths = [root_path]
            for name in ("parent", "child", "leaf"):
                paths.append(paths[-1] / name)
                paths[-1].mkdir(mode=0o750)
                os.chmod(paths[-1], 0o750)
            flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
            for index, path in enumerate(paths):
                parent = chain[-1] if chain else None
                fd = (os.open(path, flags) if parent is None else
                      os.open(path.name, flags, dir_fd=parent.fd))
                cleanup.callback(close_retained, fd)
                info = os.fstat(fd)
                dev, ino, uid, gid, mode = self._posix_directory_token(info)
                self.assertEqual((uid, gid), (os.getuid(), os.getgid()))
                if index:
                    self.assertEqual(mode, 0o750)
                directory = PREP.OwnedDirectory(path, fd, dev, ino, uid, gid, mode, parent)
                owned_by_fd[fd] = directory
                chain.append(directory)
            self.assertEqual([item.path for item in chain], paths)
            self.assertIsNone(chain[0].parent)
            yield chain
        self.assertEqual([item.fd for item in chain], [-1] * 4)
        self.assertEqual(owned_by_fd, {})
        self.assertFalse(root_path.exists())

    @unittest.skipUnless(
        os.name == "posix" and hasattr(os, "O_DIRECTORY") and hasattr(os, "O_NOFOLLOW")
        and os.open in os.supports_dir_fd and os.stat in os.supports_dir_fd
        and os.stat in os.supports_follow_symlinks,
        "real path-bound directory semantics require POSIX no-follow and descriptor-relative operations")
    def test_posix_path_bound_unchanged_leaf_revalidates(self):
        with self._posix_retained_leaf_chain() as chain:
            snapshots = [vars(item).copy() for item in chain]
            for index, item in enumerate(chain):
                retained_token = (item.dev, item.ino, item.uid, item.gid, item.mode)
                self.assertEqual(self._posix_directory_token(os.fstat(item.fd)), retained_token)
                if index:
                    self.assertIs(item.parent, chain[index - 1])
                    self.assertEqual(self._posix_directory_token(os.stat(item.path.name, dir_fd=item.parent.fd,
                                                   follow_symlinks=False)), retained_token)
            # Observe only opens; identity reads and named inspections remain real.
            with mock.patch.object(PREP.os, "open", wraps=os.open) as reopened:
                self.assertIsNone(PREP.revalidate_path_bound_directory(chain[-1], "TEST"))
            reopened.assert_not_called()
            for item, snapshot in zip(chain, snapshots):
                self.assertEqual(vars(item), snapshot)
                self.assertEqual(self._posix_directory_token(os.fstat(item.fd)),
                                 (item.dev, item.ino, item.uid, item.gid, item.mode))

    @unittest.skipUnless(
        os.name == "posix" and hasattr(os, "O_DIRECTORY") and hasattr(os, "O_NOFOLLOW")
        and os.open in os.supports_dir_fd and os.stat in os.supports_dir_fd
        and os.stat in os.supports_follow_symlinks,
        "real path-bound directory semantics require POSIX no-follow and descriptor-relative operations")
    def test_posix_path_bound_leaf_rename_away_is_rejected_as_name_lost(self):
        if os.rename not in os.supports_dir_fd:
            self.skipTest("real descriptor-relative POSIX rename is unavailable")
        with self._posix_retained_leaf_chain() as chain:
            root, parent, child, leaf = chain
            snapshots = [vars(item).copy() for item in chain]
            retained_token = (leaf.dev, leaf.ino, leaf.uid, leaf.gid, leaf.mode)
            os.rename("leaf", "leaf-away", src_dir_fd=child.fd, dst_dir_fd=child.fd)
            self.assertEqual(self._posix_directory_token(os.fstat(leaf.fd)), retained_token)
            self.assertEqual(self._posix_directory_token(
                os.stat("leaf-away", dir_fd=child.fd, follow_symlinks=False)), retained_token)
            with self.assertRaises(FileNotFoundError):
                os.stat("leaf", dir_fd=child.fd, follow_symlinks=False)
            real_stat = os.stat
            with mock.patch.object(PREP.os, "stat", wraps=real_stat) as inspected, \
                 mock.patch.object(PREP.os, "open", wraps=os.open) as reopened:
                with self.assertRaises(PREP.Failure) as caught:
                    PREP.revalidate_path_bound_directory(leaf, "TEST")
            self.assertIs(type(caught.exception), PREP.Failure)
            self.assertEqual(caught.exception.code, "DIRECTORY_NAME_LOST")
            self.assertEqual(caught.exception.stage, "TEST")
            self.assertEqual(inspected.call_args_list, [
                mock.call("parent", dir_fd=root.fd, follow_symlinks=False),
                mock.call("child", dir_fd=parent.fd, follow_symlinks=False),
                mock.call("leaf", dir_fd=child.fd, follow_symlinks=False)])
            reopened.assert_not_called()
            for item, snapshot in zip(chain, snapshots):
                self.assertEqual(vars(item), snapshot)
                self.assertEqual(self._posix_directory_token(os.fstat(item.fd)),
                                 (item.dev, item.ino, item.uid, item.gid, item.mode))
            self.assertEqual(self._posix_directory_token(
                os.stat("leaf-away", dir_fd=child.fd, follow_symlinks=False)), retained_token)

    @unittest.skipUnless(
        os.name == "posix" and hasattr(os, "O_DIRECTORY") and hasattr(os, "O_NOFOLLOW")
        and os.open in os.supports_dir_fd and os.stat in os.supports_dir_fd
        and os.stat in os.supports_follow_symlinks,
        "real path-bound directory semantics require POSIX no-follow and descriptor-relative operations")
    def test_posix_path_bound_leaf_replacement_is_rejected_as_name_substituted(self):
        if os.rename not in os.supports_dir_fd or os.mkdir not in os.supports_dir_fd:
            self.skipTest("real descriptor-relative POSIX rename/mkdir is unavailable")
        if os.chmod not in os.supports_dir_fd:
            self.skipTest("real descriptor-relative POSIX chmod is unavailable")
        with self._posix_retained_leaf_chain() as chain:
            root, parent, child, leaf = chain
            snapshots = [vars(item).copy() for item in chain]
            retained_token = (leaf.dev, leaf.ino, leaf.uid, leaf.gid, leaf.mode)
            os.rename("leaf", "leaf-away", src_dir_fd=child.fd, dst_dir_fd=child.fd)
            os.mkdir("leaf", mode=0o750, dir_fd=child.fd)
            os.chmod("leaf", 0o750, dir_fd=child.fd)
            self.assertEqual(self._posix_directory_token(os.fstat(leaf.fd)), retained_token)
            self.assertEqual(self._posix_directory_token(
                os.stat("leaf-away", dir_fd=child.fd, follow_symlinks=False)), retained_token)
            replacement = os.stat("leaf", dir_fd=child.fd, follow_symlinks=False)
            replacement_token = self._posix_directory_token(replacement)
            self.assertEqual((replacement.st_uid, replacement.st_gid, stat.S_IMODE(replacement.st_mode)),
                             (os.getuid(), os.getgid(), 0o750))
            self.assertEqual((replacement.st_uid, replacement.st_gid), (leaf.uid, leaf.gid))
            self.assertNotEqual(replacement.st_ino, leaf.ino)
            real_stat = os.stat
            with mock.patch.object(PREP.os, "stat", wraps=real_stat) as inspected, \
                 mock.patch.object(PREP.os, "open", wraps=os.open) as reopened, \
                 mock.patch.object(PREP.os, "chmod", wraps=os.chmod) as chmod, \
                 mock.patch.object(PREP.os, "mkdir", wraps=os.mkdir) as mkdir, \
                 mock.patch.object(PREP.os, "rename", wraps=os.rename) as rename, \
                 mock.patch.object(PREP.os, "unlink", wraps=os.unlink) as unlink, \
                 mock.patch.object(PREP.os, "rmdir", wraps=os.rmdir) as rmdir, \
                 mock.patch.object(PREP.os, "fchmod", wraps=os.fchmod) as fchmod, \
                 mock.patch.object(PREP.os, "chown", wraps=os.chown) as chown, \
                 mock.patch.object(PREP.os, "fchown", wraps=os.fchown) as fchown, \
                 mock.patch.object(PREP.os, "replace", wraps=os.replace) as replace:
                with self.assertRaises(PREP.Failure) as caught:
                    PREP.revalidate_path_bound_directory(chain[-1], "TEST")
            self.assertIs(type(caught.exception), PREP.Failure)
            self.assertEqual(caught.exception.code, "DIRECTORY_NAME_SUBSTITUTED")
            self.assertEqual(caught.exception.stage, "TEST")
            self.assertEqual(inspected.call_args_list, [
                mock.call("parent", dir_fd=root.fd, follow_symlinks=False),
                mock.call("child", dir_fd=parent.fd, follow_symlinks=False),
                mock.call("leaf", dir_fd=child.fd, follow_symlinks=False)])
            for operation in (reopened, chmod, mkdir, rename, unlink, rmdir,
                              fchmod, chown, fchown, replace):
                operation.assert_not_called()
            for item, snapshot in zip(chain, snapshots):
                self.assertEqual(vars(item), snapshot)
                self.assertEqual(self._posix_directory_token(os.fstat(item.fd)),
                                 (item.dev, item.ino, item.uid, item.gid, item.mode))
            self.assertEqual(os.stat("leaf", dir_fd=child.fd, follow_symlinks=False), replacement)
            self.assertEqual(self._posix_directory_token(
                os.stat("leaf", dir_fd=child.fd, follow_symlinks=False)), replacement_token)
            self.assertEqual(self._posix_directory_token(
                os.stat("leaf-away", dir_fd=child.fd, follow_symlinks=False)), retained_token)

    @unittest.skipUnless(
        os.name == "posix" and hasattr(os, "O_DIRECTORY") and hasattr(os, "O_NOFOLLOW")
        and os.open in os.supports_dir_fd and os.stat in os.supports_dir_fd
        and os.stat in os.supports_follow_symlinks,
        "real path-bound directory semantics require POSIX no-follow and descriptor-relative operations")
    def test_posix_path_bound_leaf_removal_is_rejected_as_name_lost(self):
        if os.rmdir not in os.supports_dir_fd:
            self.skipTest("real descriptor-relative POSIX rmdir is unavailable")
        with self._posix_retained_leaf_chain() as chain:
            root, parent, child, leaf = chain
            snapshots = [vars(item).copy() for item in chain]
            retained_token = (leaf.dev, leaf.ino, leaf.uid, leaf.gid, leaf.mode)
            os.rmdir("leaf", dir_fd=child.fd)
            self.assertEqual(self._posix_directory_token(os.fstat(leaf.fd)), retained_token)
            with self.assertRaises(FileNotFoundError):
                os.stat("leaf", dir_fd=child.fd, follow_symlinks=False)
            real_stat = os.stat
            with mock.patch.object(PREP.os, "stat", wraps=real_stat) as inspected, \
                 mock.patch.object(PREP.os, "open", wraps=os.open) as reopened, \
                 mock.patch.object(PREP.os, "mkdir", wraps=os.mkdir) as mkdir:
                with self.assertRaises(PREP.Failure) as caught:
                    PREP.revalidate_path_bound_directory(chain[-1], "TEST")
            self.assertIs(type(caught.exception), PREP.Failure)
            self.assertEqual(caught.exception.code, "DIRECTORY_NAME_LOST")
            self.assertEqual(caught.exception.stage, "TEST")
            self.assertEqual(inspected.call_args_list, [
                mock.call("parent", dir_fd=root.fd, follow_symlinks=False),
                mock.call("child", dir_fd=parent.fd, follow_symlinks=False),
                mock.call("leaf", dir_fd=child.fd, follow_symlinks=False)])
            reopened.assert_not_called()
            mkdir.assert_not_called()
            for item, snapshot in zip(chain, snapshots):
                self.assertEqual(vars(item), snapshot)
                self.assertEqual(self._posix_directory_token(os.fstat(item.fd)),
                                 (item.dev, item.ino, item.uid, item.gid, item.mode))
            with self.assertRaises(FileNotFoundError):
                os.stat("leaf", dir_fd=child.fd, follow_symlinks=False)

    @unittest.skipUnless(
        os.name == "posix" and hasattr(os, "O_DIRECTORY") and hasattr(os, "O_NOFOLLOW")
        and os.open in os.supports_dir_fd and os.stat in os.supports_dir_fd
        and os.stat in os.supports_follow_symlinks,
        "real path-bound directory semantics require POSIX no-follow and descriptor-relative operations")
    def test_posix_path_bound_ancestor_replacement_is_rejected_as_name_substituted(self):
        if os.rename not in os.supports_dir_fd or os.mkdir not in os.supports_dir_fd:
            self.skipTest("real descriptor-relative POSIX rename/mkdir is unavailable")
        if os.chmod not in os.supports_dir_fd:
            self.skipTest("real descriptor-relative POSIX chmod is unavailable")
        with self._posix_retained_leaf_chain() as chain:
            root, parent, child, leaf = chain
            snapshots = [vars(item).copy() for item in chain]
            retained_token = (parent.dev, parent.ino, parent.uid, parent.gid, parent.mode)
            os.rename("parent", "parent-away", src_dir_fd=root.fd, dst_dir_fd=root.fd)
            os.mkdir("parent", mode=0o750, dir_fd=root.fd)
            os.chmod("parent", 0o750, dir_fd=root.fd)
            for item in chain:
                self.assertEqual(self._posix_directory_token(os.fstat(item.fd)),
                                 (item.dev, item.ino, item.uid, item.gid, item.mode))
            self.assertIs(child.parent, parent)
            self.assertIs(leaf.parent, child)
            self.assertEqual(self._posix_directory_token(
                os.stat("child", dir_fd=parent.fd, follow_symlinks=False)),
                (child.dev, child.ino, child.uid, child.gid, child.mode))
            self.assertEqual(self._posix_directory_token(
                os.stat("leaf", dir_fd=child.fd, follow_symlinks=False)),
                (leaf.dev, leaf.ino, leaf.uid, leaf.gid, leaf.mode))
            self.assertEqual(self._posix_directory_token(
                os.stat("parent-away", dir_fd=root.fd, follow_symlinks=False)), retained_token)
            replacement = os.stat("parent", dir_fd=root.fd, follow_symlinks=False)
            replacement_token = self._posix_directory_token(replacement)
            self.assertEqual((replacement.st_uid, replacement.st_gid, stat.S_IMODE(replacement.st_mode)),
                             (os.getuid(), os.getgid(), 0o750))
            self.assertEqual((replacement.st_uid, replacement.st_gid), (parent.uid, parent.gid))
            self.assertNotEqual(replacement.st_ino, parent.ino)
            real_stat = os.stat
            with mock.patch.object(PREP.os, "stat", wraps=real_stat) as inspected, \
                 mock.patch.object(PREP.os, "open", wraps=os.open) as reopened, \
                 mock.patch.object(PREP.os, "chmod", wraps=os.chmod) as chmod, \
                 mock.patch.object(PREP.os, "mkdir", wraps=os.mkdir) as mkdir, \
                 mock.patch.object(PREP.os, "rename", wraps=os.rename) as rename, \
                 mock.patch.object(PREP.os, "unlink", wraps=os.unlink) as unlink, \
                 mock.patch.object(PREP.os, "rmdir", wraps=os.rmdir) as rmdir, \
                 mock.patch.object(PREP.os, "fchmod", wraps=os.fchmod) as fchmod, \
                 mock.patch.object(PREP.os, "chown", wraps=os.chown) as chown, \
                 mock.patch.object(PREP.os, "fchown", wraps=os.fchown) as fchown, \
                 mock.patch.object(PREP.os, "replace", wraps=os.replace) as replace:
                with self.assertRaises(PREP.Failure) as caught:
                    PREP.revalidate_path_bound_directory(chain[-1], "TEST")
            self.assertIs(type(caught.exception), PREP.Failure)
            self.assertEqual(caught.exception.code, "DIRECTORY_NAME_SUBSTITUTED")
            self.assertEqual(caught.exception.stage, "TEST")
            self.assertEqual(inspected.call_args_list, [
                mock.call("parent", dir_fd=root.fd, follow_symlinks=False)])
            for operation in (reopened, chmod, mkdir, rename, unlink, rmdir,
                              fchmod, chown, fchown, replace):
                operation.assert_not_called()
            for item, snapshot in zip(chain, snapshots):
                self.assertEqual(vars(item), snapshot)
                self.assertEqual(self._posix_directory_token(os.fstat(item.fd)),
                                 (item.dev, item.ino, item.uid, item.gid, item.mode))
            self.assertEqual(os.stat("parent", dir_fd=root.fd, follow_symlinks=False), replacement)
            self.assertEqual(self._posix_directory_token(
                os.stat("parent", dir_fd=root.fd, follow_symlinks=False)), replacement_token)
            self.assertEqual(self._posix_directory_token(
                os.stat("parent-away", dir_fd=root.fd, follow_symlinks=False)), retained_token)

    @unittest.skipUnless(
        os.name == "posix" and hasattr(os, "O_DIRECTORY") and hasattr(os, "O_NOFOLLOW")
        and os.open in os.supports_dir_fd and os.stat in os.supports_dir_fd
        and os.stat in os.supports_follow_symlinks,
        "real path-bound directory semantics require POSIX no-follow and descriptor-relative operations")
    def test_posix_path_bound_ancestor_rename_away_is_rejected_as_name_lost(self):
        if os.rename not in os.supports_dir_fd:
            self.skipTest("real descriptor-relative POSIX rename is unavailable")
        with self._posix_retained_leaf_chain() as chain:
            root, parent, child, leaf = chain
            snapshots = [vars(item).copy() for item in chain]
            retained_token = (parent.dev, parent.ino, parent.uid, parent.gid, parent.mode)
            os.rename("parent", "parent-away", src_dir_fd=root.fd, dst_dir_fd=root.fd)
            for item in chain:
                self.assertEqual(self._posix_directory_token(os.fstat(item.fd)),
                                 (item.dev, item.ino, item.uid, item.gid, item.mode))
            self.assertIs(child.parent, parent)
            self.assertIs(leaf.parent, child)
            self.assertEqual(self._posix_directory_token(
                os.stat("child", dir_fd=parent.fd, follow_symlinks=False)),
                (child.dev, child.ino, child.uid, child.gid, child.mode))
            self.assertEqual(self._posix_directory_token(
                os.stat("leaf", dir_fd=child.fd, follow_symlinks=False)),
                (leaf.dev, leaf.ino, leaf.uid, leaf.gid, leaf.mode))
            self.assertEqual(self._posix_directory_token(
                os.stat("parent-away", dir_fd=root.fd, follow_symlinks=False)), retained_token)
            with self.assertRaises(FileNotFoundError):
                os.stat("parent", dir_fd=root.fd, follow_symlinks=False)
            real_stat = os.stat
            with mock.patch.object(PREP.os, "stat", wraps=real_stat) as inspected, \
                 mock.patch.object(PREP.os, "open", wraps=os.open) as reopened, \
                 mock.patch.object(PREP.os, "chmod", wraps=os.chmod) as chmod, \
                 mock.patch.object(PREP.os, "mkdir", wraps=os.mkdir) as mkdir, \
                 mock.patch.object(PREP.os, "rename", wraps=os.rename) as rename, \
                 mock.patch.object(PREP.os, "unlink", wraps=os.unlink) as unlink, \
                 mock.patch.object(PREP.os, "rmdir", wraps=os.rmdir) as rmdir, \
                 mock.patch.object(PREP.os, "fchmod", wraps=os.fchmod) as fchmod, \
                 mock.patch.object(PREP.os, "chown", wraps=os.chown) as chown, \
                 mock.patch.object(PREP.os, "fchown", wraps=os.fchown) as fchown, \
                 mock.patch.object(PREP.os, "replace", wraps=os.replace) as replace:
                with self.assertRaises(PREP.Failure) as caught:
                    PREP.revalidate_path_bound_directory(chain[-1], "TEST")
            self.assertIs(type(caught.exception), PREP.Failure)
            self.assertEqual(caught.exception.code, "DIRECTORY_NAME_LOST")
            self.assertEqual(caught.exception.stage, "TEST")
            self.assertEqual(inspected.call_args_list, [
                mock.call("parent", dir_fd=root.fd, follow_symlinks=False)])
            for operation in (reopened, chmod, mkdir, rename, unlink, rmdir,
                              fchmod, chown, fchown, replace):
                operation.assert_not_called()
            for item, snapshot in zip(chain, snapshots):
                self.assertEqual(vars(item), snapshot)
                self.assertEqual(self._posix_directory_token(os.fstat(item.fd)),
                                 (item.dev, item.ino, item.uid, item.gid, item.mode))
            with self.assertRaises(FileNotFoundError):
                os.stat("parent", dir_fd=root.fd, follow_symlinks=False)
            self.assertEqual(self._posix_directory_token(
                os.stat("parent-away", dir_fd=root.fd, follow_symlinks=False)), retained_token)

    @unittest.skipUnless(os.name == "posix", "descriptor-relative hierarchy semantics are PI3/POSIX-only")
    def test_posix_named_child_create_then_idempotent_open(self):
        with tempfile.TemporaryDirectory() as temporary:
            parent_path = pathlib.Path(temporary)
            os.chmod(parent_path, 0o750)
            parent = PREP.open_owned_directory(parent_path, 0o750, "TEST")
            try:
                child, created = PREP.ensure_owned_named_child(parent, "runtime", 0o750, "TEST",
                                                               require_same_device=False)
                try:
                    self.assertTrue(created)
                    second, second_created = PREP.ensure_owned_named_child(parent, "runtime", 0o750, "TEST",
                                                                             require_same_device=False)
                    try:
                        self.assertFalse(second_created)
                        self.assertEqual(child.ino, second.ino)
                    finally:
                        second.close()
                finally:
                    child.close()
            finally:
                parent.close()


if __name__ == "__main__":
    unittest.main()
