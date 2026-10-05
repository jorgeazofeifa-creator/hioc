"""Local synthetic Git histories and descriptor fixtures; no lifecycle execution."""
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import os
import pathlib
import stat
import subprocess
import sys
import tempfile
import types
import unittest
from unittest import mock

TOOLS = pathlib.Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))
try:
    import hioc_pe4_handoff_compatibility as HANDOFF
    import hioc_pe4_runtime_common as COMMON
    spec = importlib.util.spec_from_file_location("pe4_e_test", TOOLS / "hioc-pe4-dependency-validate.py")
    E = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = E
    spec.loader.exec_module(E)
finally:
    sys.path.pop(0)


class GitCompatibilityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="hioc-handoff-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name)
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Synthetic Test")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "core.autocrlf", "false")
        self.git("config", "commit.gpgsign", "false")
        for relative in HANDOFF.CURRENT_CONSUMER_PATHS:
            self.write(relative, "initial\n")
        self.producer = self.commit()
        self.consumer = self.producer

    def git(self, *arguments, input=None):
        return subprocess.run(["git", "-C", str(self.root), *arguments],
            input=input, text=True, capture_output=True, check=True).stdout.strip()

    def write(self, relative, value):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value, encoding="utf-8", newline="\n")

    def commit(self):
        self.git("add", "-A")
        self.git("commit", "--allow-empty", "-m", "synthetic checkpoint")
        oid = self.git("rev-parse", "HEAD")
        self.git("update-ref", "refs/remotes/origin/main", oid)
        return oid

    def compatible(self):
        HANDOFF.verify_handoff_compatibility(self.root, self.producer, self.consumer)

    def source(self):
        HANDOFF.verify_current_consumer_source(self.root, self.consumer)

    def rejected(self, callable, code=None, stage="HANDOFF_COMPATIBILITY"):
        with self.assertRaises(COMMON.Failure) as caught:
            callable()
        self.assertEqual(caught.exception.stage, stage)
        self.assertFalse(caught.exception.rollback)
        if code:
            self.assertEqual(caught.exception.code, code)
        self.assertNotIn(str(self.root), str(caught.exception))

    def test_equal_commit_and_current_source_pass(self):
        self.source()
        self.compatible()

    def test_documentation_only_descendant_passes(self):
        self.write("docs/status.md", "documentation only\n")
        self.consumer = self.commit()
        self.source()
        self.compatible()

    def test_unrelated_source_and_current_e_helper_changes_pass(self):
        for relative in ("tools/unrelated.py", *HANDOFF.CURRENT_CONSUMER_PATHS[:2]):
            self.write(relative, "new consumer source\n")
        self.consumer = self.commit()
        self.source()
        self.compatible()

    def test_each_critical_blob_change_rejected(self):
        for relative in HANDOFF.CRITICAL_PRODUCER_PATHS:
            with self.subTest(relative=relative):
                self.git("reset", "--hard", self.producer)
                self.write(relative, "changed\n")
                self.consumer = self.commit()
                self.rejected(self.compatible, "HANDOFF_CRITICAL_BLOB_MISMATCH")

    def test_malformed_abbreviated_and_alias_commits_rejected(self):
        for value in ("main", self.producer[:12], self.producer.upper(), "g" * 40, "", None):
            for producer in (True, False):
                with self.subTest(value=value, producer=producer):
                    args = (value, self.consumer) if producer else (self.producer, value)
                    self.rejected(lambda: HANDOFF.verify_handoff_compatibility(self.root, *args),
                                  "INVALID_GOVERNANCE_COMMIT")

    def test_noncommit_blob_tree_and_tag_objects_rejected(self):
        self.git("tag", "-a", "synthetic-tag", "-m", "tag")
        objects = (self.git("rev-parse", "HEAD:requirements-pe4.lock"),
                   self.git("rev-parse", "HEAD^{tree}"), self.git("rev-parse", "synthetic-tag"))
        for oid in objects:
            for args in ((oid, self.consumer), (self.producer, oid)):
                with self.subTest(args=args):
                    self.rejected(lambda: HANDOFF.verify_handoff_compatibility(self.root, *args),
                                  "HANDOFF_COMMIT_OBJECT_INVALID")

    def test_missing_producer_and_consumer_objects_rejected(self):
        for args in (("0" * 40, self.consumer), (self.producer, "0" * 40)):
            self.rejected(lambda: HANDOFF.verify_handoff_compatibility(self.root, *args),
                          "HANDOFF_GIT_FAILED")

    def test_divergent_producer_rejected(self):
        self.git("checkout", "-b", "divergent")
        self.write("divergent", "producer\n")
        self.producer = self.commit()
        self.git("checkout", "main")
        self.write("consumer", "consumer\n")
        self.consumer = self.commit()
        self.rejected(self.compatible, "HANDOFF_GIT_FAILED")

    def test_descendant_producer_rejected(self):
        self.write("later", "later\n")
        self.producer = self.commit()
        self.rejected(self.compatible, "HANDOFF_GIT_FAILED")

    def test_unrelated_history_rejected(self):
        self.git("checkout", "--orphan", "unrelated")
        self.write("unrelated-root", "distinct orphan tree\n")
        self.producer = self.commit()
        self.rejected(self.compatible, "HANDOFF_GIT_FAILED")

    def test_replacement_cannot_disguise_incompatible_commit(self):
        self.git("commit", "--allow-empty", "-m", "compatible descendant")
        replacement = self.git("rev-parse", "HEAD")
        self.git("reset", "--hard", self.producer)
        self.write("requirements-pe4.lock", "incompatible\n")
        self.consumer = self.commit()
        self.git("replace", self.consumer, replacement)
        # Ordinary Git now presents matching blobs; the guard reads real objects.
        self.assertEqual(self.git("rev-parse", self.consumer + ":requirements-pe4.lock"),
                         self.git("rev-parse", self.producer + ":requirements-pe4.lock"))
        self.rejected(self.compatible, "HANDOFF_CRITICAL_BLOB_MISMATCH")

    def test_missing_critical_path_rejected(self):
        (self.root / "requirements-pe4.lock").unlink()
        self.consumer = self.commit()
        self.rejected(self.compatible, "HANDOFF_GIT_FAILED")

    def test_nonblob_critical_path_rejected(self):
        (self.root / "requirements-pe4.lock").unlink()
        self.write("requirements-pe4.lock/entry", "tree\n")
        self.consumer = self.commit()
        self.rejected(self.compatible, "HANDOFF_BLOB_OBJECT_INVALID")

    def test_shallow_history_rejected(self):
        shallow = pathlib.Path(self.git("rev-parse", "--absolute-git-dir")) / "shallow"
        shallow.write_text(self.producer + "\n", encoding="ascii")
        self.rejected(self.compatible, "HANDOFF_HISTORY_INCOMPLETE")

    def test_ancestry_command_error_is_bounded(self):
        actual = HANDOFF.subprocess.run
        def fail(command, **kwargs):
            if "merge-base" in command:
                return subprocess.CompletedProcess(command, 128, "", "uncontrolled diagnostic")
            return actual(command, **kwargs)
        with mock.patch.object(HANDOFF.subprocess, "run", side_effect=fail):
            self.rejected(self.compatible, "HANDOFF_GIT_FAILED")

    def test_missing_ancestor_object_rejected(self):
        self.write("later", "later\n")
        self.consumer = self.commit()
        gitdir = pathlib.Path(self.git("rev-parse", "--absolute-git-dir"))
        missing = gitdir / "objects" / self.producer[:2] / self.producer[2:]
        missing.chmod(0o600)
        missing.unlink()
        self.rejected(self.compatible, "HANDOFF_GIT_FAILED")

    def test_git_timeout_os_and_decode_errors_are_bounded(self):
        for error in (OSError("noise"), subprocess.TimeoutExpired("git", 60), UnicodeError("noise")):
            with mock.patch.object(HANDOFF.subprocess, "run", side_effect=error):
                self.rejected(self.compatible, "HANDOFF_GIT_FAILED")

    def test_dirty_tracked_and_untracked_rejected(self):
        for relative in ("requirements-pe4.lock", "untracked"):
            with self.subTest(relative=relative):
                self.write(relative, "dirty\n")
                self.rejected(self.source, "SOURCE_REPOSITORY_DIRTY", "SOURCE_IDENTITY")
                self.git("reset", "--hard", self.producer)
                self.git("clean", "-fd")

    def test_wrong_branch_rejected(self):
        self.git("checkout", "-b", "wrong")
        self.rejected(self.source, "SOURCE_IDENTITY_MISMATCH", "SOURCE_IDENTITY")

    def test_head_consumer_mismatch_rejected(self):
        self.write("later", "later\n")
        self.commit()
        self.rejected(self.source, "SOURCE_IDENTITY_MISMATCH", "SOURCE_IDENTITY")

    def test_origin_mismatch_and_divergence_rejected(self):
        self.git("checkout", "-b", "divergent")
        self.write("other", "other\n")
        origin = self.commit()
        self.git("checkout", "main")
        self.git("update-ref", "refs/remotes/origin/main", origin)
        self.rejected(self.source, "SOURCE_IDENTITY_MISMATCH", "SOURCE_IDENTITY")

    def test_active_operations_rejected(self):
        for name in HANDOFF.ACTIVE_OPERATIONS:
            path = pathlib.Path(self.git("rev-parse", "--absolute-git-dir")) / name
            with self.subTest(name=name):
                path.write_text(self.producer + "\n", encoding="ascii")
                self.rejected(self.source, "SOURCE_GIT_OPERATION_ACTIVE", "SOURCE_IDENTITY")
                path.unlink()

    def test_every_current_path_changed_even_hidden_from_status_rejected(self):
        for relative in HANDOFF.CURRENT_CONSUMER_PATHS:
            with self.subTest(relative=relative):
                self.git("update-index", "--assume-unchanged", relative)
                self.write(relative, "hidden worktree modification\n")
                self.assertEqual(self.git("status", "--porcelain"), "")
                self.rejected(self.source, "SOURCE_WORKTREE_IDENTITY_MISMATCH", "SOURCE_IDENTITY")
                self.git("update-index", "--no-assume-unchanged", relative)
                self.git("checkout", "--", relative)

    def test_normalized_crlf_worktree_matches_committed_lf(self):
        self.git("config", "core.autocrlf", "true")
        for relative in HANDOFF.CURRENT_CONSUMER_PATHS:
            (self.root / relative).write_bytes(b"initial\r\n")
        # Refresh the index conversion metadata after switching autocrlf.
        self.git("add", "--renormalize", ".")
        self.consumer = self.commit()
        self.source()

    def test_ahead_behind_gate_rejects_inconsistent_git_result(self):
        actual = HANDOFF._git
        def inconsistent(root, args, stage):
            if args[0] == "rev-list":
                return "1\t1"
            return actual(root, args, stage)
        with mock.patch.object(HANDOFF, "_git", side_effect=inconsistent):
            self.rejected(self.source, "SOURCE_IDENTITY_MISMATCH", "SOURCE_IDENTITY")


class ProducerEligibilityTests(unittest.TestCase):
    def setUp(self):
        self.producer, self.consumer = "a" * 40, "b" * 40
        self.root = types.SimpleNamespace(path=pathlib.Path("/synthetic/construction"), fd=10)
        self.evidence = mock.Mock()
        self.document = dict(schema_version="1.0", action="PE-4.0B.2a-D", result="PASS",
            governance_commit=self.producer, construction_directory=str(self.root.path),
            eligibility_state="AWAITING_CONFIRMATION")
        self.marker = dict(schema_version="1.0", action="PE-4.0B.2a-D", result="PASS",
            governance_commit=self.producer, construction_directory=str(self.root.path),
            environment_identity=COMMON.VERSIONED_NAME, wheel_sha256=COMMON.WHEEL_SHA256,
            lock_sha256=COMMON.LOCK_SHA256, evidence_directory="/tmp/hioc-pe4-runtime-construct-Abcd1234")

    def validate(self, digest=None, payload=None, commit=None):
        raw = json.dumps(self.document, sort_keys=True).encode() if payload is None else payload
        self.marker["evidence_sha256"] = hashlib.sha256(raw).hexdigest() if digest is None else digest
        before = copy.deepcopy((self.marker, self.document))
        with mock.patch.object(COMMON, "_read_owned_json_fd", side_effect=[(self.marker, b"marker"), (self.document, raw)]), mock.patch.object(COMMON, "open_owned_directory", return_value=self.evidence):
            try:
                return COMMON.validate_action_d_eligibility(self.root, commit or self.producer)
            finally:
                self.assertEqual((self.marker, self.document), before)

    def test_valid_distinct_producer_binding_leaves_d_objects_unchanged(self):
        self.assertIs(self.validate(), self.marker)
        self.evidence.close.assert_called_once()

    def test_marker_wrong_commit_and_no_consumer_fallback(self):
        self.marker["governance_commit"] = self.consumer
        with self.assertRaises(COMMON.Failure): self.validate()
        self.marker["governance_commit"] = self.producer
        with self.assertRaises(COMMON.Failure): self.validate(commit=self.consumer)

    def test_evidence_wrong_commit_even_with_matching_digest_rejected(self):
        self.document["governance_commit"] = self.consumer
        with self.assertRaises(COMMON.Failure) as caught: self.validate()
        self.assertEqual(caught.exception.code, "ACTION_D_EVIDENCE_MISMATCH")

    def test_wrong_marker_contract_fields_and_tampering_rejected(self):
        for key in ("construction_directory", "environment_identity", "wheel_sha256", "lock_sha256",
                    "result", "action", "schema_version", "evidence_directory"):
            original = self.marker[key]
            with self.subTest(key=key):
                self.marker[key] = "tampered"
                with self.assertRaises(COMMON.Failure): self.validate()
                self.marker[key] = original
        self.marker["extra"] = "tampered"
        with self.assertRaises(COMMON.Failure): self.validate()

    def test_tampered_evidence_and_wrong_digest_rejected(self):
        with self.assertRaises(COMMON.Failure): self.validate(digest="0" * 64)
        raw = json.dumps(self.document, sort_keys=True).encode()
        with self.assertRaises(COMMON.Failure): self.validate(digest=hashlib.sha256(raw).hexdigest(), payload=raw + b" ")
        for key in ("result", "action", "construction_directory", "eligibility_state"):
            original = self.document[key]
            with self.subTest(key=key):
                self.document[key] = "tampered"
                with self.assertRaises(COMMON.Failure): self.validate()
                self.document[key] = original

    def test_real_json_reader_ownership_mode_type_stability_and_parse_rejections(self):
        for changes in ({"st_uid": 101}, {"st_gid": 101}, {"st_mode": stat.S_IFREG | 0o600},
                        {"st_mode": stat.S_IFDIR | 0o400}, {"st_ino": 2}, {"invalid_json": True}):
            base = dict(st_uid=100, st_gid=100, st_mode=stat.S_IFREG | 0o400,
                        st_dev=1, st_ino=1, st_size=2, st_mtime_ns=1, st_ctime_ns=1)
            after = base.copy()
            if "st_ino" in changes:
                after.update(changes)
            else:
                base.update({k:v for k,v in changes.items() if k != "invalid_json"})
                after = base.copy()
            with self.subTest(changes=changes), contextlib.ExitStack() as stack:
                for name, value in (("getuid", 100), ("getgid", 100), ("open", 20)):
                    stack.enter_context(mock.patch.object(COMMON.os, name, return_value=value, create=True))
                stack.enter_context(mock.patch.object(COMMON.os, "O_NOFOLLOW", 0x20000, create=True))
                stack.enter_context(mock.patch.object(COMMON.os, "fstat", side_effect=[types.SimpleNamespace(**base),types.SimpleNamespace(**after)]))
                stack.enter_context(mock.patch.object(COMMON.os, "read", side_effect=[b"x!" if changes.get("invalid_json") else b"{}", b""]))
                close = stack.enter_context(mock.patch.object(COMMON.os, "close"))
                with self.assertRaises(COMMON.Failure):
                    COMMON._read_owned_json_fd(self.root, COMMON.ACTION_D_ELIGIBILITY, 0o400, "ACTION_D_ELIGIBILITY")
                close.assert_called_once_with(20)


class ActionEMainTests(unittest.TestCase):
    def setUp(self):
        self.producer, self.consumer = "a" * 40, "b" * 40
        self.argv = ["action-e-test", "--governance-commit", self.consumer,
                     "--action-d-governance-commit", self.producer,
                     "--construction-directory", "/synthetic/construction"]

    def harness(self, stack):
        calls = []
        mocks = {}
        names = ("verify_pi3", "verify_current_consumer_source", "verify_handoff_compatibility",
                 "validate_construction", "open_trusted_owned_parent", "open_owned_directory",
                 "action_d_subprocess_environment", "validate_action_d_eligibility",
                 "validate_runtime_inputs", "snapshot_tree", "assert_unchanged", "revalidate_owned_directory",
                 "controlled_distributions", "controlled_capabilities", "evidence_directory", "write_evidence", "terminal")
        for name in names:
            def record(*args, _name=name, **kwargs):
                calls.append((_name, args, kwargs))
                if _name.startswith("open_"): return mock.Mock(fd=42)
                if _name == "validate_construction": return pathlib.Path(args[0])
                if _name == "action_d_subprocess_environment": return {"PIP_NO_INDEX":"1"}
                if _name == "validate_action_d_eligibility": return {"evidence_directory":"synthetic-d-evidence"}
                if _name == "validate_runtime_inputs": return {"policy":"controlled"}
                if _name == "evidence_directory": return pathlib.Path("synthetic-evidence")
            mocks[name] = stack.enter_context(mock.patch.object(E, name, side_effect=record))
        stack.enter_context(mock.patch.object(sys, "argv", self.argv))
        stack.enter_context(contextlib.redirect_stdout(io.StringIO()))
        return calls, mocks

    def test_missing_producer_fails_cli_before_host_or_lifecycle(self):
        self.argv = self.argv[:3] + self.argv[5:]
        with contextlib.ExitStack() as stack:
            calls, mocks = self.harness(stack)
            stack.enter_context(contextlib.redirect_stderr(io.StringIO()))
            with self.assertRaises(SystemExit) as caught: E.main()
            self.assertEqual(caught.exception.code, 2)
            self.assertEqual(calls, [])

    def test_malformed_either_commit_fails_before_host(self):
        for index in (2, 4):
            for bad in ("main", "a" * 12):
                original = self.argv[index]
                self.argv[index] = bad
                with contextlib.ExitStack() as stack:
                    calls, mocks = self.harness(stack)
                    with self.assertRaises(COMMON.Failure): E.main()
                    self.assertEqual(calls, [])
                self.argv[index] = original

    def test_real_main_distinct_commits_exact_order_and_unchanged_evidence(self):
        with contextlib.ExitStack() as stack:
            calls, mocks = self.harness(stack)
            E.main()
            names = [name for name, args, kwargs in calls]
            self.assertLess(names.index("verify_pi3"), names.index("verify_current_consumer_source"))
            self.assertLess(names.index("verify_current_consumer_source"), names.index("verify_handoff_compatibility"))
            self.assertLess(names.index("verify_handoff_compatibility"), names.index("validate_construction"))
            self.assertLess(names.index("validate_action_d_eligibility"), names.index("controlled_distributions"))
            self.assertLess(names.index("controlled_distributions"), names.index("controlled_capabilities"))
            self.assertLess(names.index("controlled_capabilities"), names.index("evidence_directory"))
            mocks["verify_current_consumer_source"].assert_called_once_with(E.SOURCE, self.consumer)
            mocks["verify_handoff_compatibility"].assert_called_once_with(E.SOURCE, self.producer, self.consumer)
            root = mocks["validate_action_d_eligibility"].call_args.args[0]
            mocks["validate_action_d_eligibility"].assert_called_once_with(root, self.producer)
            root.close.assert_called_once()
            mocks["controlled_distributions"].assert_called_once_with(root, {"PIP_NO_INDEX":"1"}, {"policy":"controlled"})
            mocks["controlled_capabilities"].assert_called_once_with(root, {"PIP_NO_INDEX":"1"}, {"policy":"controlled"})
            mocks["write_evidence"].assert_called_once_with(pathlib.Path("synthetic-evidence"), "PE-4.0B.2a-E",
                {"ACTION":"DEPENDENCY_VALIDATION", "ENVIRONMENT_IDENTITY":COMMON.VERSIONED_NAME,
                 "INSTALLED_VERSION":"16.1.1", "CAPABILITY_VALIDATION":"PASS"}, "PASS")
            mocks["terminal"].assert_called_once_with("PASS", "NONE", "COMPLETE", False, pathlib.Path("synthetic-evidence"))
            # Exactly the controlled distribution/capability gates; no D/F/G launch.
            self.assertEqual(names.count("controlled_capabilities"), 1)

    def test_repository_compatibility_and_eligibility_reject_before_runtime_and_evidence(self):
        for gate, stage in (("verify_current_consumer_source", "SOURCE_IDENTITY"),
                            ("verify_handoff_compatibility", "HANDOFF_COMPATIBILITY"),
                            ("validate_action_d_eligibility", "ACTION_D_ELIGIBILITY")):
            with self.subTest(gate=gate), contextlib.ExitStack() as stack:
                calls, mocks = self.harness(stack)
                mocks[gate].side_effect = COMMON.Failure("BOUNDED_REJECTION", stage)
                with self.assertRaises(COMMON.Failure): E.main()
                for name in ("validate_runtime_inputs", "snapshot_tree", "assert_unchanged", "revalidate_owned_directory",
                 "controlled_distributions", "controlled_capabilities", "evidence_directory", "write_evidence", "terminal"):
                    mocks[name].assert_not_called()
                if gate != "validate_action_d_eligibility":
                    mocks["open_owned_directory"].assert_not_called()

    def test_existing_success_json_schema_is_unchanged(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = pathlib.Path(temp)
            real_open, real_close, real_fsync = os.open, os.close, os.fsync
            sentinel = 987654
            def opened(path, *args, **kwargs):
                return sentinel if pathlib.Path(path) == directory else real_open(path, *args, **kwargs)
            with mock.patch.object(COMMON, "require_directory"), mock.patch.object(COMMON, "require_owned"), mock.patch.object(COMMON.os, "open", side_effect=opened), mock.patch.object(COMMON.os, "close", side_effect=lambda fd: None if fd == sentinel else real_close(fd)), mock.patch.object(COMMON.os, "fsync", side_effect=lambda fd: None if fd == sentinel else real_fsync(fd)):
                COMMON.write_evidence(directory, "PE-4.0B.2a-E", {"ACTION":"DEPENDENCY_VALIDATION",
                    "ENVIRONMENT_IDENTITY":COMMON.VERSIONED_NAME, "INSTALLED_VERSION":"16.1.1",
                    "CAPABILITY_VALIDATION":"PASS"}, "PASS")
            self.assertEqual(json.loads((directory / "result.json").read_bytes()), {
                "schema_version":"1.0", "action":"PE-4.0B.2a-E", "ACTION":"DEPENDENCY_VALIDATION",
                "ENVIRONMENT_IDENTITY":COMMON.VERSIONED_NAME, "INSTALLED_VERSION":"16.1.1",
                "CAPABILITY_VALIDATION":"PASS", "result":"PASS", "error_code":"NONE",
                "failure_stage":"COMPLETE", "rollback_recommended":False})


if __name__ == "__main__":
    unittest.main()
