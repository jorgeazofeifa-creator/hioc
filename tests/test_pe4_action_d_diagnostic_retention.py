import importlib.util
import json
import pathlib
import sys
import unittest
from contextlib import redirect_stdout
from io import StringIO
from types import SimpleNamespace
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
SPEC = importlib.util.spec_from_file_location(
    "pe4_action_d_diagnostics", ROOT / "tools" / "hioc-pe4-runtime-construct.py")
ACTION = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ACTION)


class ActionDDiagnosticRetentionTests(unittest.TestCase):
    def state(self):
        return {"CONSTRUCTION_CREATED": "FALSE", "CONSTRUCTION_CONFIRMED": "FALSE",
                "CONSTRUCTION_RETAINED": "FALSE", "INPUT_SNAPSHOT_CREATED": "TRUE",
                "INPUT_SNAPSHOT_RETAINED": "FALSE", "CLEANUP_STATE": "COMPLETE"}

    def test_os_error_is_bounded_and_retains_errno_without_message(self):
        secret = "token=/private/path\ntraceback command --password=secret"
        document = ACTION._failure_document("a" * 40, self.state(), "SEALED_LOCK",
            "SEALED_LOCK", OSError(5, secret), "UNEXPECTED_ERROR", "UNEXPECTED")
        payload = json.dumps(document, sort_keys=True)
        self.assertEqual(document["exception_class"], "OS_ERROR")
        self.assertEqual(document["errno"], "5")
        self.assertNotIn(secret, payload)
        self.assertLessEqual(len(payload.encode()), 4096)

    def test_specific_os_error_subclasses_precede_generic_os_error(self):
        self.assertEqual(ACTION._diagnostic_exception(PermissionError(13))[0], "PERMISSION_ERROR")
        self.assertEqual(ACTION._diagnostic_exception(FileNotFoundError(2))[0], "FILE_NOT_FOUND")
        self.assertEqual(ACTION._diagnostic_exception(FileExistsError(17))[0], "FILE_EXISTS")

    def test_complete_exception_normalization_matrix_is_bounded(self):
        cases = ((ACTION.Failure("X", "Y"), "GOVERNED_FAILURE"), (OSError(5), "OS_ERROR"),
                 (PermissionError(13), "PERMISSION_ERROR"), (FileNotFoundError(2), "FILE_NOT_FOUND"),
                 (FileExistsError(17), "FILE_EXISTS"), (NotADirectoryError(20), "NOT_A_DIRECTORY"),
                 (IsADirectoryError(21), "IS_A_DIRECTORY"), (TimeoutError(), "TIMEOUT"),
                 (ValueError("x"), "VALUE_ERROR"), (RuntimeError("x"), "RUNTIME_ERROR"),
                 (Exception("x"), "OTHER"))
        for exc, expected in cases:
            with self.subTest(expected=expected):
                actual, errno = ACTION._diagnostic_exception(exc)
                self.assertEqual(actual, expected)
                self.assertTrue(errno == "NONE" or errno.isdecimal())

    def test_hostile_message_never_enters_any_diagnostic_field(self):
        hostile = "/tmp/private/secret/path\r\nBearer SUPER_SECRET_TOKEN password=DO_NOT_LEAK " \
                  "-----BEGIN OPENSSH PRIVATE KEY----- fake traceback " + ("X" * 10000)
        document = ACTION._failure_document("b" * 40, self.state(), "CONSTRUCTION_ALLOCATION",
            "CREATE_CONSTRUCTION", RuntimeError(hostile), "UNEXPECTED_ERROR", "UNEXPECTED")
        serialized = json.dumps(document, sort_keys=True)
        for value in ("SUPER_SECRET_TOKEN", "DO_NOT_LEAK", "OPENSSH PRIVATE KEY", "traceback", "/tmp/private"):
            self.assertNotIn(value, serialized)
        self.assertEqual(document["exception_class"], "RUNTIME_ERROR")
        self.assertEqual(document["errno"], "NONE")

    def test_context_and_failure_path_are_finite(self):
        self.assertIn("CONSTRUCTION_ALLOCATION", ACTION.DIAGNOSTIC_STAGES)
        self.assertIn("CREATE_CONSTRUCTION", ACTION.DIAGNOSTIC_OPERATIONS)
        self.assertTrue(ACTION.FAILURE_EVIDENCE_RE.fullmatch(
            "/tmp/hioc-pe4-runtime-construct-failure-Abc123Z9"))
        with self.assertRaises(ACTION.Failure):
            ACTION._failure_document("a" * 40, self.state(), "UNBOUNDED", "INTERNAL",
                                     RuntimeError("ignored"), "UNEXPECTED_ERROR", "UNEXPECTED")


class _Directory:
    """Disposable, descriptor-free stand-in for Action D's owned directories."""

    _next_fd = 40

    def __init__(self, name, parent=None):
        self.path = pathlib.PurePosixPath("/tmp/hioc-test") / name
        self.parent = parent if parent is not None else self
        self.fd = _Directory._next_fd
        _Directory._next_fd += 1
        self.closed = False

    def close(self):
        self.closed = True


class _Parser:
    def add_argument(self, *_args, **_kwargs):
        pass

    def parse_args(self):
        return SimpleNamespace(governance_commit="a" * 40,
                               transfer_directory="/tmp/hioc-pe4-artifact-transfer-test")


class ActionDMainDiagnosticHarnessTests(unittest.TestCase):
    """Exercise main() with disposable fakes; no PI3 or production path is touched."""

    def _run(self, injected_stage=None, exception=None, cleanup_exception=None,
             failure_publication_fails=False):
        exception = exception or RuntimeError("hostile secret must never be emitted")
        snapshot_parent = _Directory("snapshot-parent")
        snapshot = _Directory("snapshot", snapshot_parent)
        roots = []
        publications = []
        calls = {"open_owned": 0}

        def fail(stage):
            if injected_stage == stage:
                raise exception

        def create_child(parent, prefix, _mode, stage):
            if prefix.startswith("hioc-pe4-runtime-construct-failure-"):
                fail("FAILURE_EVIDENCE_PUBLICATION")
                return _Directory("hioc-pe4-runtime-construct-failure-Abc123Z9", parent)
            if prefix.startswith(".construct-"):
                fail("CONSTRUCTION_ALLOCATION")
                return _Directory("construction", parent)
            if prefix.startswith("hioc-pe4-runtime-construct-"):
                fail("EVIDENCE_PUBLICATION")
                return _Directory("evidence", parent)
            raise AssertionError(prefix)

        def open_owned(*_args, **_kwargs):
            calls["open_owned"] += 1
            stage = ("RUNTIME_ROOT_VALIDATION" if calls["open_owned"] == 1
                     else "ENVIRONMENTS_ROOT_VALIDATION")
            fail(stage)
            return _Directory("owned-%d" % calls["open_owned"])

        def cleanup(directory, stage):
            if cleanup_exception is not None and stage == "INPUT_SNAPSHOT_CLEANUP":
                raise cleanup_exception
            fail("INPUT_SNAPSHOT_CLEANUP" if stage == "INPUT_SNAPSHOT_CLEANUP"
                 else "CONSTRUCTION_CLEANUP")
            directory.close()

        def run(_argv, stage, **_kwargs):
            fail({"VENV_CREATION": "VENV_CREATION", "PIP_CAPABILITY": "PIP_CAPABILITY",
                  "OFFLINE_INSTALL": "OFFLINE_INSTALL"}.get(stage, "__NO_STAGE__"))
            return SimpleNamespace(stdout="--isolated --no-index --require-hashes --only-binary")

        def publish(directory, name, document, stage, **_kwargs):
            if failure_publication_fails and name == "failure-result.json":
                raise OSError(5, "do not disclose")
            fail("ELIGIBILITY_PUBLICATION" if name == ACTION.ACTION_D_ELIGIBILITY
                 else "EVIDENCE_PUBLICATION" if name == "result.json" else "__NO_STAGE__")
            publications.append((str(directory.path), name, document, stage))
            return "d" * 64

        def tmp_root(stage):
            fail("EVIDENCE_PUBLICATION" if stage == "EVIDENCE_ROOT"
                 else "FAILURE_EVIDENCE_PUBLICATION" if stage == "FAILURE_EVIDENCE_PUBLICATION"
                 else "__NO_STAGE__")
            root = _Directory("root-%d" % len(roots)); roots.append(root); return root

        patches = {
            "verify_pi3": mock.Mock(), "verify_repository": mock.Mock(side_effect=lambda *_: fail("REPOSITORY")),
            "create_action_d_input_snapshot": mock.Mock(side_effect=lambda *_: (fail("INPUT_SNAPSHOT"), snapshot)[1]),
            "sealed_snapshot_file": mock.Mock(side_effect=lambda *_: (fail("SEALED_LOCK"), 99)[1]),
            "open_trusted_owned_parent": mock.Mock(side_effect=lambda *_: (fail("RUNTIME_PARENT_VALIDATION"), _Directory("runtime-parent"))[1]),
            "open_owned_directory": mock.Mock(side_effect=open_owned), "create_owned_child": mock.Mock(side_effect=create_child),
            "action_d_subprocess_environment": mock.Mock(return_value={}), "run": mock.Mock(side_effect=run),
            "revalidate_owned_directory": mock.Mock(side_effect=lambda _d, stage: fail("VENV_FILESYSTEM" if stage == "VENV_FILESYSTEM" else "CONSTRUCTION_CONFIRMATION")),
            "validate_venv_symlinks": mock.Mock(), "_runtime_probe": mock.Mock(side_effect=lambda *_: fail("RUNTIME_IDENTITY")),
            "exact_distribution_set": mock.Mock(side_effect=lambda *_args, **_kwargs: (fail("DISTRIBUTION_VALIDATION"), {})[1]),
            "cleanup_owned_directory": mock.Mock(side_effect=cleanup), "open_tmp_root": mock.Mock(side_effect=tmp_root),
            "publish_owned_json": mock.Mock(side_effect=publish),
        }
        output = StringIO()
        with mock.patch.object(ACTION.argparse, "ArgumentParser", return_value=_Parser()), \
             mock.patch.object(ACTION.os, "umask", return_value=0), \
             mock.patch.object(ACTION.os, "close"), \
             mock.patch.object(ACTION.os, "fchmod", create=True), \
             mock.patch.object(ACTION.os, "stat", side_effect=lambda *_args, **_kwargs: (
                 fail("LOCK_STAT"), SimpleNamespace(st_size=123))[1]), \
             mock.patch.multiple(ACTION, **patches), redirect_stdout(output):
            result = ACTION.main()
        return result, output.getvalue(), publications

    def test_main_retains_sanitized_failure_record_at_every_primary_operation_boundary(self):
        # One injection at each primary operation proves main(), not merely helpers,
        # supplies bounded context and retains a failure document.
        stages = ("REPOSITORY", "INPUT_SNAPSHOT", "LOCK_STAT", "SEALED_LOCK", "RUNTIME_PARENT_VALIDATION",
                  "RUNTIME_ROOT_VALIDATION", "ENVIRONMENTS_ROOT_VALIDATION", "CONSTRUCTION_ALLOCATION",
                  "VENV_CREATION", "VENV_FILESYSTEM", "RUNTIME_IDENTITY", "PIP_CAPABILITY",
                  "OFFLINE_INSTALL", "DISTRIBUTION_VALIDATION", "CONSTRUCTION_CONFIRMATION",
                  "INPUT_SNAPSHOT_CLEANUP", "EVIDENCE_PUBLICATION", "ELIGIBILITY_PUBLICATION")
        for stage in stages:
            with self.subTest(stage=stage):
                result, output, publications = self._run(stage, OSError(13, "token=never-print"))
                self.assertEqual(result, 1)
                self.assertIn("RESULT=FAIL", output)
                expected_stage = "INPUT_VALIDATION" if stage == "REPOSITORY" else (
                    "INPUT_SNAPSHOT" if stage == "LOCK_STAT" else stage)
                self.assertIn("DIAGNOSTIC_STAGE=" + expected_stage, output)
                self.assertIn("EXCEPTION_CLASS=PERMISSION_ERROR", output)
                self.assertNotIn("never-print", output)
                failure = [item for item in publications if item[1] == "failure-result.json"]
                self.assertEqual(len(failure), 1)
                self.assertEqual(failure[0][2]["diagnostic_stage"], expected_stage)
                self.assertNotIn("never-print", json.dumps(failure[0][2], sort_keys=True))

    def test_main_retains_primary_failure_when_cleanup_also_fails(self):
        result, output, publications = self._run("SEALED_LOCK", PermissionError(13, "private"),
                                                 cleanup_exception=OSError(5, "cleanup-private"))
        self.assertEqual(result, 1)
        self.assertIn("CLEANUP_STATE=FAILED", output)
        self.assertIn("CLEANUP_EXCEPTION_CLASS=OS_ERROR", output)
        failure = [item for item in publications if item[1] == "failure-result.json"]
        self.assertEqual(failure[0][2]["exception_class"], "PERMISSION_ERROR")
        self.assertEqual(failure[0][2]["cleanup_state"], "FAILED")

    def test_main_fails_closed_when_failure_evidence_publication_fails(self):
        result, output, publications = self._run("SEALED_LOCK", RuntimeError("private"),
                                                 failure_publication_fails=True)
        self.assertEqual(result, 1)
        self.assertIn("FAILURE_EVIDENCE_STATE=UNCONFIRMED", output)
        self.assertIn("FAILURE_EVIDENCE_PUBLICATION=FAILED", output)
        self.assertFalse(any(item[1] == "failure-result.json" for item in publications))

    def test_main_success_control_preserves_success_publication_semantics(self):
        result, output, publications = self._run()
        self.assertEqual(result, 0)
        self.assertIn("RESULT=PASS", output)
        self.assertIn("ERROR_CODE=NONE", output)
        self.assertIn("FAILURE_STAGE=COMPLETE", output)
        self.assertIn("CONSTRUCTION_CREATED=TRUE", output)
        self.assertIn("CONSTRUCTION_CONFIRMED=TRUE", output)
        self.assertIn("CONSTRUCTION_RETAINED=TRUE", output)
        self.assertIn("INPUT_SNAPSHOT_CREATED=TRUE", output)
        self.assertIn("INPUT_SNAPSHOT_RETAINED=FALSE", output)
        self.assertIn("EVIDENCE_STATE=CONFIRMED", output)
        self.assertIn("ACTION_D_ELIGIBILITY=CONFIRMED", output)
        self.assertNotIn("FAILURE_EVIDENCE_STATE=CONFIRMED", output)
        self.assertEqual([item[1] for item in publications], ["result.json", ACTION.ACTION_D_ELIGIBILITY])


if __name__ == "__main__":
    unittest.main()
