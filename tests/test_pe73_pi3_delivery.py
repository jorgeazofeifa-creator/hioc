"""Synthetic PE-7.3 delivery fixtures. No production deployment is executed.

Real Windows temporary files, fsync/replace and AssetLock are used. POSIX
ownership/mode and ancestor/security behavior are explicit fixture metadata, not
a claim about Linux execution. External fencing is SYNTHETIC ONLY.
"""
import ast
import contextlib
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from hioc.assets import AssetLock, AssetLockTimeout

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("pe73_delivery_fixture", ROOT/"tools/hioc-pe73-pi3-delivery.py")
d = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(d)

def git(*args):
    return subprocess.check_output(["git", "--no-optional-locks", *args], cwd=ROOT)

SOURCE = {item["path"]: git("show", d.RELEASE+":"+item["path"]) for item in d.MANIFEST}
BASE = {}
for path, (digest, _) in d.PRIOR.items():
    if path.endswith("/mqtt.py"):
        # Exact historically supplied production representation, not refreshed
        # from the different immediate pre-PE7 repository version.
        BASE[path] = git("cat-file", "blob", "d185aee1c3a30de72f060c824878224022236c3c")
    else:
        BASE[path] = git("show", "ad9ddc5ced903f8c922a12c08f843fba6fce907b:"+path)
    assert d.sha(BASE[path]) == digest

class FixtureFS:
    """Isolated native files plus explicit POSIX metadata injection."""
    def __init__(self, root):
        self.root = root
        self.modes = {}
        self.uids = {}
        self.gids = {}
        self.fail = None
        self.publications = []
        for parent in ("pi4/bin", "pi4/lib/hioc", "backups", "config", "state"):
            (root/parent).mkdir(parents=True, exist_ok=True)
        for path, raw in BASE.items():
            (root/path).write_bytes(raw)
            self.modes[path] = d.MODES[path]
        for path, raw in {"config/hioc.conf": b"synthetic-config",
                "state/unchanged.json": b"synthetic-state",
                "backups/historical-pe4-journal": b"COMMITTED preserved",
                "unrelated.txt": b"do not change"}.items():
            (root/path).write_bytes(raw)
        self.unchanged = {p.relative_to(root).as_posix(): p.read_bytes()
                          for p in root.rglob("*") if p.is_file() and p.relative_to(root).as_posix() not in BASE}

    def path(self, relative):
        p = Path(relative)
        d.require(not p.is_absolute() and ".." not in p.parts, "UNSAFE_PATH")
        result = self.root/p
        for ancestor in [result, *result.parents]:
            if ancestor == self.root.parent:
                break
            d.require(not ancestor.is_symlink(), "UNSAFE_TYPE")
        return result

    def ancestors(self, relative):
        result = {}
        parent = self.path(relative).parent
        while parent != self.root.parent:
            info = parent.stat()
            result[str(parent.relative_to(self.root))] = {
                "st_dev": info.st_dev, "st_ino": info.st_ino, "st_uid": 1000,
                "st_gid": 1000, "mode": 0o755, "type": "DIRECTORY"}
            parent = parent.parent
        return result

    def snapshot(self, relative, mode=None):
        path = self.path(relative)
        parents = self.ancestors(relative)
        if not path.exists():
            return {"exists": False, "parents": parents}
        info = path.lstat()
        d.require(path.is_file(), "UNSAFE_TYPE")
        d.require(info.st_nlink == 1, "UNSAFE_HARDLINK")
        uid, gid = self.uids.get(relative, 1000), self.gids.get(relative, 1000)
        actual_mode = self.modes.get(relative, 0o600)
        d.require(uid == gid == 1000 and not actual_mode & 0o7022, "UNSAFE_OWNERSHIP_OR_MODE")
        if mode is not None:
            d.require(actual_mode == mode, "UNSAFE_OWNERSHIP_OR_MODE")
        identity = d.identity(info)
        identity.update(st_uid=uid, st_gid=gid, mode=actual_mode)
        return {"exists": True, "parents": parents, "identity": identity, "sha256": d.sha(path.read_bytes())}

    def read(self, relative, mode=0o600):
        snap = self.snapshot(relative, mode)
        d.require(snap["exists"], "FILE_MISSING")
        return self.path(relative).read_bytes()

    def transaction_present(self):
        return (self.root/d.TX).is_dir()

    def mkdir_tx(self):
        self.path(d.TX).mkdir(mode=0o700)

    def write_new(self, relative, raw, mode=0o600):
        if self.fail and self.fail(relative):
            raise OSError("synthetic private exception must not leak")
        with self.path(relative).open("xb") as stream:
            stream.write(raw); stream.flush(); os.fsync(stream.fileno())
        self.modes[relative] = mode
        d.require(self.read(relative, mode) == raw, "WRITE_NOT_VERIFIED")

    def journal(self, value):
        raw = d.canonical(value)
        self.write_new(d.TX+"/journal-next", raw)
        os.replace(self.path(d.TX+"/journal-next"), self.path(d.TX+"/journal.json"))
        self.modes[d.TX+"/journal.json"] = 0o600

    def publish(self, relative, raw, before, mode):
        d.require(self.snapshot(relative, mode if before["exists"] else None) == before, "DESTINATION_DRIFT")
        temporary = relative+".synthetic-next"
        self.write_new(temporary, raw, mode)
        if self.fail and self.fail("PUBLISH:"+relative):
            raise OSError("synthetic publication failure")
        os.replace(self.path(temporary), self.path(relative))
        self.modes[relative] = mode
        self.publications.append(relative)
        return self.snapshot(relative, mode)

    def remove_installed(self, relative, expected, mode):
        d.require(self.snapshot(relative, mode) == expected, "INSTALLED_DRIFT")
        self.path(relative).unlink()

    @contextlib.contextmanager
    def mutex(self):
        with AssetLock(self.root/"backups"/".synthetic-deployment.lock", False, timeout=0):
            yield

    def assert_unrelated(self, test):
        for path, raw in self.unchanged.items():
            test.assertEqual((self.root/path).read_bytes(), raw, path)

class SyntheticExternalFence:
    """Test-only externally owned fence persists across controller exceptions."""
    def __init__(self, root):
        self.root, self.active, self.busy = root, False, False
        self.observation = {"cron_sha256": d.sha(d.canonical({"cron": list(d.CRON)})),
            "known_cron_commands": list(d.CRON), "coverage": "SYNTHETIC_COMPLETE",
            "partial_failure_exclusion": "SYNTHETIC_EXTERNALLY_HELD",
            "unlocked_asset_or_classification_callers": "SYNTHETIC_EXCLUDED"}
        self.guard = None

    def observe(self):
        return copy.deepcopy(self.observation)

    def start(self):
        self.guard = AssetLock(self.root/".synthetic-consumer.lock", False, timeout=0)
        self.guard.__enter__()
        self.active = True

    def close(self):
        if self.guard:
            self.guard.__exit__(None, None, None)
        self.guard, self.active = None, False

    @contextlib.contextmanager
    def hold(self, observation):
        d.require(not self.busy, "CONSUMER_BUSY")
        self.assert_active()
        d.require(observation == self.observation, "CONSUMER_DRIFT")
        yield  # Does not release the externally owned fixture fence.

    def assert_active(self):
        d.require(self.active, "CONSUMER_COORDINATION_NOT_ESTABLISHED")

class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.fs = FixtureFS(self.root)
        self.fence = SyntheticExternalFence(self.root)
        self.fence.start()
        self.c = d.Controller(self.fs, SOURCE, self.fence)

    def tearDown(self):
        self.fs.assert_unrelated(self)
        self.fence.close()
        self.temp.cleanup()

    def prepare(self):
        before = d.preflight(self.fs, SOURCE, self.fence)
        return self.c.prepare("PREPARE_SYNTHETIC", d.sha(d.canonical(before)))

    def commit(self):
        report = self.prepare()
        return self.c.commit("COMMIT_SYNTHETIC", report["journal_sha256"])

    def test_exact_13_manifest_git_blobs_order_and_modes(self):
        d.check_sources(SOURCE)
        self.assertEqual(len(SOURCE), 13)
        self.assertEqual(len(d.PRIOR), 5)
        self.assertEqual(d.ORDER[-1], "pi4/bin/hioc-incident-engine-v2.py")
        self.assertEqual(d.MODES[d.ORDER[-1]], 0o755)
        self.assertEqual(d.MODES["pi4/bin/hioc-assets.py"], 0o700)
        self.assertTrue(all(d.MODES[p] == 0o600 for p in SOURCE if p not in d.PRIOR and "/lib/" in p))

    def test_readonly_preflight_and_inspection_do_not_write(self):
        before = sorted(p.relative_to(self.root).as_posix() for p in self.root.rglob("*"))
        result = d.preflight(self.fs, SOURCE, self.fence)
        self.assertEqual(self.c.inspect()["state"], "NOT_STARTED")
        self.assertEqual(result["release"], d.RELEASE)
        self.assertEqual(before, sorted(p.relative_to(self.root).as_posix() for p in self.root.rglob("*")))

    def test_every_replacement_hash_or_absence_mismatch(self):
        for path in d.PRIOR:
            with self.subTest(path=path):
                original = self.fs.path(path).read_bytes()
                self.fs.path(path).write_bytes(b"wrong baseline")
                with self.assertRaisesRegex(d.Failure, "BASELINE_MISMATCH"):
                    d.preflight(self.fs, SOURCE, self.fence)
                self.fs.path(path).write_bytes(original)
        for path in set(SOURCE)-set(d.PRIOR):
            with self.subTest(path=path):
                self.fs.path(path).write_bytes(b"unexpected")
                with self.assertRaisesRegex(d.Failure, "UNEXPECTED_TARGET"):
                    d.preflight(self.fs, SOURCE, self.fence)
                self.fs.path(path).unlink()

    def test_wrong_source_bytes_and_commit_rejected(self):
        wrong = dict(SOURCE); wrong[d.ORDER[0]] += b"tampered"
        with self.assertRaisesRegex(d.Failure, "SOURCE_IDENTITY"):
            d.preflight(self.fs, wrong, self.fence)
        answer = subprocess.CompletedProcess([], 0, stdout=b"invalid-commit\n", stderr=b"")
        with patch.object(d.subprocess, "run", return_value=answer):
            with self.assertRaisesRegex(d.Failure, "SOURCE_COMMIT_INVALID"):
                d.source_gate(ROOT)

    def test_source_gate_checks_clean_release_root_remote_and_all_git_objects(self):
        calls = []
        def command(argv, **kwargs):
            calls.append((argv, kwargs))
            args = argv[3:]
            if args == ["rev-parse", "--verify", "HEAD^{commit}"]: raw = (d.RELEASE+"\n").encode()
            elif args == ["rev-parse", "--verify", d.RELEASE+"^{commit}"]: raw = (d.RELEASE+"\n").encode()
            elif args == ["merge-base", "--is-ancestor", d.RELEASE, "HEAD"]: raw = b""
            elif args == ["rev-parse", "--show-toplevel"]: raw = (str(ROOT)+"\n").encode()
            elif args == ["remote", "get-url", "origin"]: raw = b"https://github.com/jorgeazofeifa-creator/hioc.git\n"
            elif args == ["status", "--porcelain=v1", "--untracked-files=all"]: raw = b""
            elif args[0] == "show": raw = SOURCE[args[1].split(":",1)[1]]
            elif args[0] == "rev-parse":
                path = args[1].split(":",1)[1]
                raw = (next(x["git_blob"] for x in d.MANIFEST if x["path"] == path)+"\n").encode()
            else: raise AssertionError(args)
            return subprocess.CompletedProcess(argv, 0, raw, b"")
        with patch.object(d.subprocess, "run", side_effect=command):
            self.assertEqual(d.source_gate(ROOT), SOURCE)
        self.assertTrue(all(argv[0] == "/usr/bin/git" for argv, _ in calls))
        self.assertTrue(all("GIT_DIR" not in kwargs["env"] for _, kwargs in calls))
        def wrong_remote(argv, **kwargs):
            if argv[3:] == ["remote", "get-url", "origin"]:
                return subprocess.CompletedProcess(argv, 0, b"https://wrong.invalid/repo", b"")
            return command(argv, **kwargs)
        with patch.object(d.subprocess, "run", side_effect=wrong_remote):
            with self.assertRaisesRegex(d.Failure, "SOURCE_REMOTE_MISMATCH"):
                d.source_gate(ROOT)

    def test_ownership_group_and_mode_rejected(self):
        path = next(iter(d.PRIOR))
        for field, value in ((self.fs.uids, 0), (self.fs.gids, 0), (self.fs.modes, 0o666)):
            old = field.get(path)
            field[path] = value
            with self.assertRaisesRegex(d.Failure, "UNSAFE_OWNERSHIP_OR_MODE"):
                d.preflight(self.fs, SOURCE, self.fence)
            if old is None: del field[path]
            else: field[path] = old

    def test_hardlink_attack_rejected(self):
        path = next(iter(d.PRIOR))
        os.link(self.fs.path(path), self.root/"hardlink")
        try:
            with self.assertRaisesRegex(d.Failure, "UNSAFE_HARDLINK"):
                d.preflight(self.fs, SOURCE, self.fence)
        finally:
            (self.root/"hardlink").unlink()

    def test_symlink_and_path_escape_fail_closed(self):
        with self.assertRaisesRegex(d.Failure, "UNSAFE_PATH"):
            self.fs.snapshot("../escape")
        path = next(iter(d.PRIOR))
        # Deterministic synthetic symlink indication; Windows privileges do not
        # become an unreported missing test of the rejection branch.
        original = Path.is_symlink
        with patch.object(Path, "is_symlink", lambda p: True if p == self.fs.root/path else original(p)):
            with self.assertRaisesRegex(d.Failure, "UNSAFE_TYPE"):
                d.preflight(self.fs, SOURCE, self.fence)

    def test_authorization_and_stale_preflight_cannot_prepare(self):
        before = d.preflight(self.fs, SOURCE, self.fence)
        for reference, binding in ((None, "a"*64), ("OK_SYNTHETIC", None), ("OK_SYNTHETIC", "a"*64)):
            with self.subTest(reference=reference, binding=binding), self.assertRaises(d.Failure):
                self.c.prepare(reference, binding)
        self.assertFalse(self.fs.transaction_present())

    def test_prepare_exact_backups_and_stages_no_live_writes(self):
        result = self.prepare()
        self.assertEqual(result["state"], "PREPARED")
        self.assertEqual(self.fs.publications, [])
        for index, path in enumerate(d.ORDER):
            self.assertEqual(self.fs.read(d.TX+"/stage-"+str(index)), SOURCE[path])
            if path in d.PRIOR:
                self.assertEqual(self.fs.read(d.TX+"/backup-"+str(index)), BASE[path])
                self.assertEqual(self.fs.path(path).read_bytes(), BASE[path])

    def test_backup_failure_retains_incomplete_without_install(self):
        self.fs.fail = lambda p: "/backup-" in p
        with self.assertRaises(OSError):
            self.prepare()
        self.assertEqual(self.c.inspect()["state"], "PREPARING")
        self.assertFalse(self.fs.publications)

    def test_staging_failure_retains_incomplete_without_install(self):
        self.fs.fail = lambda p: "/stage-" in p
        with self.assertRaises(OSError):
            self.prepare()
        self.assertEqual(self.c.inspect()["state"], "PREPARING")
        self.assertFalse(self.fs.publications)

    def test_prepared_transaction_cannot_be_reprepared_or_automatically_retried(self):
        self.prepare()
        current = d.preflight(self.fs, SOURCE, self.fence)
        with self.assertRaisesRegex(d.Failure, "TRANSACTION_EXISTS"):
            self.c.prepare("PREPARE_AGAIN", d.sha(d.canonical(current)))

    def test_all_staging_verified_before_first_publication(self):
        report = self.prepare()
        self.fs.path(d.TX+"/stage-12").write_bytes(b"corrupt")
        with self.assertRaisesRegex(d.Failure, "STAGING_DRIFT"):
            self.c.commit("COMMIT_SYNTHETIC", report["journal_sha256"])
        self.assertFalse(self.fs.publications)

    def test_atomic_publication_failure_no_false_success(self):
        report = self.prepare()
        self.fs.fail = lambda p: p == "PUBLISH:"+d.ORDER[0]
        with self.assertRaises(OSError):
            self.c.commit("COMMIT_SYNTHETIC", report["journal_sha256"])
        inspection = self.c.inspect()
        self.assertEqual(inspection["state"], "COMMITTING")
        self.assertEqual(inspection["pending"], d.ORDER[0])
        self.assertTrue(self.fence.active)
        with self.assertRaisesRegex(d.Failure, "ROLLBACK_STATE_REFUSED"):
            self.c.rollback("ROLLBACK_SYNTHETIC", inspection["journal_sha256"])

    def test_interruption_after_recorded_partial_install_retains_external_fence(self):
        report = self.prepare()
        def interrupt(point):
            if point == "INSTALLED:"+d.ORDER[0]: raise KeyboardInterrupt()
        self.c.fault = interrupt
        with self.assertRaises(KeyboardInterrupt):
            self.c.commit("COMMIT_SYNTHETIC", report["journal_sha256"])
        self.assertTrue(self.fence.active)
        info = self.c.inspect()
        self.assertEqual(info["state"], "COMMITTING")
        self.assertEqual(sum(path in self.c._journal()["installed"] for path in d.ORDER), 1)
        self.assertTrue(all(info["installed_matches"].values()))
        self.c.fault = lambda _: None
        rolled = self.c.rollback("ROLLBACK_SEPARATE", info["journal_sha256"])
        self.assertEqual(rolled["state"], "ROLLED_BACK")

    def test_unjournaled_publication_is_uncertain_and_not_adopted(self):
        report = self.prepare()
        def interrupt(point):
            if point == "AFTER_PUBLICATION:"+d.ORDER[0]: raise KeyboardInterrupt()
        self.c.fault = interrupt
        with self.assertRaises(KeyboardInterrupt):
            self.c.commit("COMMIT_SYNTHETIC", report["journal_sha256"])
        info = self.c.inspect()
        self.assertIsNotNone(info["pending"])
        self.assertFalse(info["live_state_established"])
        with self.assertRaisesRegex(d.Failure, "ROLLBACK_STATE_REFUSED"):
            self.c.rollback("ROLLBACK_SYNTHETIC", info["journal_sha256"])

    def test_full_commit_static_verify_and_idempotent_inspection(self):
        info = self.commit()
        self.assertEqual(info["state"], "COMMITTED")
        self.assertEqual(self.fs.publications, d.ORDER)
        self.assertEqual(self.c.verify()["installed_count"], 13)
        self.assertEqual(self.c.inspect(), self.c.inspect())
        with self.assertRaisesRegex(d.Failure, "TRANSACTION_NOT_PREPARED"):
            self.c.commit("COMMIT_AGAIN", info["journal_sha256"])

    def test_separately_authorized_rollback_restores_five_removes_eight(self):
        info = self.commit()
        with self.assertRaisesRegex(d.Failure, "AUTHORIZATION_REQUIRED"):
            self.c.rollback(None, info["journal_sha256"])
        result = self.c.rollback("ROLLBACK_SEPARATE", info["journal_sha256"])
        self.assertEqual(result["restored_replacements"], 5)
        self.assertEqual(result["removed_new_files"], 8)
        self.assertTrue(self.c.inspect()["live_state_established"])
        for path in SOURCE:
            self.assertEqual(self.fs.path(path).read_bytes(), BASE[path]) if path in BASE else self.assertFalse(self.fs.path(path).exists())

    def test_rollback_refuses_any_installed_drift_before_mutation(self):
        info = self.commit()
        self.fs.path(d.ORDER[-1]).write_bytes(b"changed by someone else")
        before = len(self.fs.publications)
        with self.assertRaisesRegex(d.Failure, "ROLLBACK_DRIFT"):
            self.c.rollback("ROLLBACK_SEPARATE", info["journal_sha256"])
        self.assertEqual(len(self.fs.publications), before)

    def test_consumer_contention_or_missing_external_fence_stops_before_mutation(self):
        report = self.prepare()
        self.fence.busy = True
        with self.assertRaisesRegex(d.Failure, "CONSUMER_BUSY"):
            self.c.commit("COMMIT_SYNTHETIC", report["journal_sha256"])
        self.fence.busy = False; self.fence.active = False
        with self.assertRaisesRegex(d.Failure, "CONSUMER_COORDINATION_NOT_ESTABLISHED"):
            self.c.commit("COMMIT_SYNTHETIC", report["journal_sha256"])
        self.assertFalse(self.fs.publications)
        self.fence.active = True

    def test_actual_native_windows_deployment_mutex_contention(self):
        report = self.prepare()
        with self.fs.mutex():
            with self.assertRaises(AssetLockTimeout):
                self.c.commit("COMMIT_SYNTHETIC", report["journal_sha256"])
        self.assertFalse(self.fs.publications)

    def test_native_three_cron_locks_never_claim_complete_coordination(self):
        raw = ("\n".join(d.CRON)+"\n").encode()
        native = d.NativeConsumers()
        with patch.object(d.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, raw, b"")):
            observed = native.observe()
        self.assertEqual(observed["unlocked_asset_or_classification_callers"], "NOT_EXCLUDED")
        for action in ("commit", "rollback"):
            controller = d.Controller(self.fs, SOURCE, native)
            with patch.object(native, "observe", return_value=observed):
                with self.assertRaisesRegex(d.Failure, "CONSUMER_COORDINATION_NOT_ESTABLISHED"):
                    getattr(controller, action)("EXPLICIT_AUTHORIZATION", "a"*64)
        self.assertFalse(self.fs.transaction_present())
        self.assertFalse(self.fs.publications)

    def test_missing_or_duplicate_actual_cron_is_rejected(self):
        for lines in (d.CRON[1:], (*d.CRON, d.CRON[0])):
            raw = ("\n".join(lines)+"\n").encode()
            with self.subTest(lines=lines), patch.object(d.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, raw, b"")):
                with self.assertRaisesRegex(d.Failure, "CRON_MISMATCH"):
                    d.NativeConsumers().observe()

    def test_each_atomic_publication_failure_retains_evidence_without_automatic_rollback(self):
        for path in d.ORDER:
            with self.subTest(path=path), tempfile.TemporaryDirectory() as directory:
                fs = FixtureFS(Path(directory))
                fence = SyntheticExternalFence(Path(directory))
                fence.start()
                try:
                    controller = d.Controller(fs, SOURCE, fence)
                    report = d.preflight(fs, SOURCE, fence)
                    prepared = controller.prepare("PREPARE_SYNTHETIC", d.sha(d.canonical(report)))
                    fs.fail = lambda name, path=path: name == "PUBLISH:"+path
                    with self.assertRaises(OSError):
                        controller.commit("COMMIT_SYNTHETIC", prepared["journal_sha256"])
                    inspection = controller.inspect()
                    self.assertEqual(inspection["pending"], path)
                    self.assertEqual(inspection["state"], "COMMITTING")
                    self.assertTrue(fence.active)
                    self.assertEqual(fs.publications, d.ORDER[:d.ORDER.index(path)])
                    fs.assert_unrelated(self)
                finally:
                    fence.close()

    def test_every_replacement_backup_is_required_before_commit(self):
        for path in d.PRIOR:
            with self.subTest(path=path), tempfile.TemporaryDirectory() as directory:
                fs = FixtureFS(Path(directory)); fence = SyntheticExternalFence(Path(directory))
                fence.start()
                try:
                    controller = d.Controller(fs, SOURCE, fence)
                    report = d.preflight(fs, SOURCE, fence)
                    prepared = controller.prepare("PREPARE_SYNTHETIC", d.sha(d.canonical(report)))
                    fs.path(d.TX+"/backup-"+str(d.ORDER.index(path))).write_bytes(b"corrupt backup")
                    with self.assertRaisesRegex(d.Failure, "BACKUP_DRIFT"):
                        controller.commit("COMMIT_SYNTHETIC", prepared["journal_sha256"])
                    self.assertFalse(fs.publications)
                    fs.assert_unrelated(self)
                finally:
                    fence.close()

    def test_destination_drift_after_prepare_is_not_authorized_by_old_receipt(self):
        report = self.prepare()
        path = next(iter(d.PRIOR))
        self.fs.path(path).write_bytes(b"changed since preparation")
        with self.assertRaisesRegex(d.Failure, "BASELINE_MISMATCH"):
            self.c.commit("COMMIT_SYNTHETIC", report["journal_sha256"])
        self.assertFalse(self.fs.publications)

    def test_journal_cannot_rebind_release_or_manifest_or_historical_baseline(self):
        self.prepare()
        original = self.fs.read(d.TX+"/journal.json")
        for field in ("release", "manifest_sha256"):
            bad = json.loads(original);bad[field] = "0"*len(bad[field])
            self.fs.journal(bad)
            with self.assertRaisesRegex(d.Failure, "JOURNAL_INVALID"):
                self.c.inspect()
        bad = json.loads(original)
        bad["baseline"][next(iter(d.PRIOR))]["sha256"] = "0"*64
        self.fs.journal(bad)
        with self.assertRaisesRegex(d.Failure, "JOURNAL_INVALID"):
            self.c.inspect()

    def test_native_security_acl_and_symlink_type_guards(self):
        import errno, stat
        from types import SimpleNamespace
        fs = d.NativeFS.__new__(d.NativeFS)
        info = SimpleNamespace(st_mode=stat.S_IFREG | 0o600, st_uid=1000,
                               st_gid=1000, st_nlink=1)
        with patch.object(d.os, "getxattr", side_effect=OSError(errno.ENODATA, "fixture"), create=True):
            fs.security(info, mode=0o600, fd=123)
        with patch.object(d.os, "getxattr", return_value=b"ACL", create=True):
            with self.assertRaisesRegex(d.Failure, "UNSAFE_ACL"):
                fs.security(info, mode=0o600, fd=123)
        with patch.object(d.os, "getxattr", side_effect=OSError(errno.EACCES, "private"), create=True):
            with self.assertRaisesRegex(d.Failure, "ACL_NOT_ESTABLISHED"):
                fs.security(info, mode=0o600, fd=123)
        info.st_mode = stat.S_IFLNK | 0o600
        with self.assertRaisesRegex(d.Failure, "UNSAFE_TYPE"):
            fs.security(info, mode=0o600)

    def test_cli_sanitizes_private_io_failure_and_performs_no_deployment(self):
        import io
        original = d.require
        def require(value, code):
            if code != "TARGET_IDENTITY":
                original(value, code)
        output = io.StringIO()
        with patch.object(d, "require", side_effect=require), patch.object(d, "NativeFS", return_value=self.fs), patch.object(d, "source_gate", return_value=SOURCE), patch.object(self.fs, "transaction_present", side_effect=OSError("private hostname credential")), contextlib.redirect_stdout(output):
            self.assertEqual(d.main(["inspect"]), 1)
        receipt = json.loads(output.getvalue())
        self.assertEqual(receipt["error_code"], "IO_OR_CONTRACT_FAILURE")
        self.assertNotIn("credential", output.getvalue())
        self.assertFalse(receipt["pe7_executed"])
        self.assertFalse(receipt["cron_mutated"])
        self.assertFalse(self.fs.publications)

    def test_controller_never_executes_jobs_network_or_configuration_writes(self):
        self.prepare()
        with patch.object(d.subprocess, "run", side_effect=AssertionError("unexpected command")), patch.object(d.socket, "socket", side_effect=AssertionError("unexpected network")):
            report = self.c.inspect()
            self.c.commit("COMMIT_SYNTHETIC", report["journal_sha256"])
            self.c.verify()
        self.fs.assert_unrelated(self)
        source = (ROOT/"tools/hioc-pe73-pi3-delivery.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        strings = [n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str)]
        self.assertFalse(any("--pe7-cycle" == s or "--pe7-initialize" == s or "--serve" == s for s in strings))
        self.assertNotIn("install_pi4.sh", source)
        self.assertNotIn("release/upgrade.sh", source)

    def test_journal_rejects_rolled_back_without_restoration(self):
        self.commit()
        value = self.c._journal()
        value.update(state="ROLLED_BACK", rollback_authorization=None)
        self.fs.journal(value)
        with self.assertRaisesRegex(d.Failure, "JOURNAL_INVALID"):
            self.c.inspect()

    def test_journal_rejects_committed_restoration_override(self):
        self.commit()
        value = self.c._journal()
        value["restored"] = copy.deepcopy(value["installed"])
        for item in value["restored"].values():
            item["sha256"] = "0"*64
        self.fs.journal(value)
        with self.assertRaisesRegex(d.Failure, "JOURNAL_INVALID"):
            self.c.inspect()

    def test_journal_closed_bounded_fields_and_types(self):
        self.prepare()
        original = self.c._journal()
        mutations = [lambda v: v.update(version=True), lambda v: v.update(extra=True),
            lambda v: v.update(installed=[]), lambda v: v.update(restored=[]),
            lambda v: v.update(prepare_authorization="bad"),
            lambda v: v.update(consumers={}), lambda v: v.update(pending=True),
            lambda v: v["baseline"][d.ORDER[0]].update(extra=1),
            lambda v: v["baseline"][d.ORDER[0]].update(parents={"x"*4097: {}})]
        for change in mutations:
            with self.subTest(change=mutations.index(change)):
                value = copy.deepcopy(original); change(value); self.fs.journal(value)
                with self.assertRaisesRegex(d.Failure, "JOURNAL_INVALID"):
                    self.c.inspect()

    def test_journal_rejects_unauthorized_or_incomplete_rollback(self):
        info = self.commit(); self.c.rollback("ROLLBACK_SYNTHETIC", info["journal_sha256"])
        original = self.c._journal()
        self.assertTrue(self.c.inspect()["live_state_established"])
        mutations = [lambda v: v.update(rollback_authorization=None),
            lambda v: v["restored"].pop(d.ORDER[-1]),
            lambda v: v["restored"].update({"unexpected": {}}),
            lambda v: v["restored"][next(iter(d.PRIOR))].update(sha256="0"*64),
            lambda v: v["restored"][next(iter(d.PRIOR))]["identity"].update(st_uid=0)]
        for change in mutations:
            value = copy.deepcopy(original); change(value); self.fs.journal(value)
            with self.subTest(change=mutations.index(change)), self.assertRaisesRegex(d.Failure, "JOURNAL_INVALID"):
                self.c.inspect()

    def test_journal_restoration_requires_verified_backup(self):
        info = self.commit(); self.c.rollback("ROLLBACK_SYNTHETIC", info["journal_sha256"])
        path = next(iter(d.PRIOR))
        self.fs.path(d.TX+"/backup-"+str(d.ORDER.index(path))).write_bytes(b"wrong backup")
        with self.assertRaisesRegex(d.Failure, "JOURNAL_INVALID"):
            self.c.inspect()

    def test_journal_duplicate_restoration_entries_rejected(self):
        info = self.commit(); self.c.rollback("ROLLBACK_SYNTHETIC", info["journal_sha256"])
        original = self.fs.read(d.TX+"/journal.json")
        key = d.ORDER[-1]
        entry = json.dumps(key)+":"+d.canonical(self.c._journal()["restored"][key]).decode().strip()
        marker = '"restored":{'
        duplicate = original.decode().replace(marker, marker+entry+",", 1).encode()
        self.fs.path(d.TX+"/journal.json").write_bytes(duplicate)
        with self.assertRaisesRegex(d.Failure, "JOURNAL_INVALID"):
            self.c.inspect()

    def test_interrupted_rollback_records_only_reverse_installed_prefix(self):
        info = self.commit()
        def interrupt(point):
            if point == "RESTORED:"+d.ORDER[-1]: raise KeyboardInterrupt()
        self.c.fault = interrupt
        with self.assertRaises(KeyboardInterrupt):
            self.c.rollback("ROLLBACK_SYNTHETIC", info["journal_sha256"])
        value = self.c._journal()
        self.assertEqual(value["state"], "ROLLING_BACK")
        self.assertEqual(set(value["restored"]), {d.ORDER[-1]})
        self.assertTrue(self.c.inspect()["live_state_established"])
        # Exact current state is established, but rollback is not complete/resumable.
        with self.assertRaisesRegex(d.Failure, "ROLLBACK_STATE_REFUSED"):
            self.c.rollback("ROLLBACK_AGAIN", self.c.inspect()["journal_sha256"])
        value["restored"][d.ORDER[0]] = copy.deepcopy(value["baseline"][d.ORDER[0]])
        self.fs.journal(value)
        with self.assertRaisesRegex(d.Failure, "JOURNAL_INVALID"):
            self.c.inspect()

    def test_interrupted_rollback_pending_remains_uncertain(self):
        info = self.commit()
        def interrupt(point):
            if point == "ROLLBACK_INTENT:"+d.ORDER[-1]: raise KeyboardInterrupt()
        self.c.fault = interrupt
        with self.assertRaises(KeyboardInterrupt):
            self.c.rollback("ROLLBACK_SYNTHETIC", info["journal_sha256"])
        self.assertEqual(self.c.inspect()["state"], "ROLLING_BACK")
        self.assertFalse(self.c.inspect()["live_state_established"])

    def test_journal_conflicting_commit_progress_rejected(self):
        self.commit(); original = self.c._journal()
        mutations = [lambda v: v.update(commit_authorization=None),
            lambda v: v.update(pending=d.ORDER[0]),
            lambda v: v["installed"].pop(d.ORDER[0]),
            lambda v: v["installed"][d.ORDER[0]]["identity"].update(st_nlink=2),
            lambda v: v["installed"][d.ORDER[0]]["parents"].clear()]
        for change in mutations:
            value=copy.deepcopy(original); change(value); self.fs.journal(value)
            with self.subTest(change=mutations.index(change)), self.assertRaisesRegex(d.Failure, "JOURNAL_INVALID"):
                self.c.inspect()


class NativeTraversalTests(unittest.TestCase):
    def traverse(self, *, root="/one/two", reject=None, open_failure=None,
                 close_failure=None, body_failure=False):
        import errno, stat
        from pathlib import PurePosixPath
        from types import SimpleNamespace
        fs=d.NativeFS.__new__(d.NativeFS); fs.root=PurePosixPath(root)
        live=set(); closed=[]; acquired=[]
        def op(name, flags, **kwargs):
            if name == open_failure: raise OSError(errno.EACCES, "synthetic open")
            fd=10+len(acquired); acquired.append(fd); live.add(fd); return fd
        def info(fd):
            return SimpleNamespace(st_dev=1, st_ino=fd, st_uid=1000,
                st_gid=1000, st_mode=stat.S_IFDIR|0o755)
        def security(value, *args, **kwargs):
            if value.st_ino == reject: raise d.Failure("UNSAFE_OWNERSHIP_OR_MODE")
        def close(fd):
            self.assertIn(fd, live, "double close")
            live.remove(fd); closed.append(fd)
            if fd == close_failure: raise OSError(errno.EIO, "synthetic close")
        error=None
        with contextlib.ExitStack() as stack:
            for name in ("O_DIRECTORY","O_NOFOLLOW","O_CLOEXEC"):
                stack.enter_context(patch.object(d.os,name,0,create=True))
            stack.enter_context(patch.object(d.os,"open",side_effect=op))
            stack.enter_context(patch.object(d.os,"close",side_effect=close))
            stack.enter_context(patch.object(d.os,"fstat",side_effect=info))
            stack.enter_context(patch.object(d.os,"stat",side_effect=lambda name,dir_fd,**kw: info(dir_fd+1)))
            stack.enter_context(patch.object(fs,"security",side_effect=security))
            try:
                with fs.directory() as fd:
                    self.assertEqual(fd, acquired[-1])
                    if body_failure: raise d.Failure("ORIGINAL_BODY_FAILURE")
            except BaseException as e: error=e
        self.assertFalse(live, "descriptor leak")
        self.assertEqual(sorted(closed), acquired)
        self.assertEqual(len(closed), len(set(closed)))
        return error, closed

    def test_child_validation_failure_preserved(self):
        error, closed=self.traverse(reject=11)
        self.assertIsInstance(error,d.Failure)
        self.assertEqual(error.code,"UNSAFE_OWNERSHIP_OR_MODE")
        self.assertEqual(closed,[11,10])

    def test_parent_validation_failure(self):
        error,closed=self.traverse(reject=10)
        self.assertIsInstance(error,d.Failure); self.assertEqual(closed,[10])

    def test_successful_multilevel_traversal_exact_once_cleanup(self):
        error,closed=self.traverse()
        self.assertIsNone(error); self.assertEqual(closed,[12,11,10])

    def test_open_failure_closes_owned_ancestors(self):
        error,closed=self.traverse(open_failure="two")
        self.assertIsInstance(error,OSError); self.assertEqual(closed,[11,10])

    def test_cleanup_failure_preserves_primary_and_attempts_all_closes(self):
        error,closed=self.traverse(reject=11,close_failure=11)
        self.assertIsInstance(error,d.Failure)
        self.assertEqual(error.code,"UNSAFE_OWNERSHIP_OR_MODE")
        self.assertTrue(error.cleanup_failed); self.assertEqual(closed,[11,10])

    def test_cleanup_failure_without_primary_is_reported(self):
        error,closed=self.traverse(close_failure=12)
        self.assertIsInstance(error,OSError); self.assertEqual(closed,[12,11,10])

    def test_body_failure_is_preserved_during_cleanup_failure(self):
        error,closed=self.traverse(body_failure=True,close_failure=12)
        self.assertIsInstance(error,d.Failure); self.assertEqual(error.code,"ORIGINAL_BODY_FAILURE")
        self.assertTrue(error.cleanup_failed)


class SyntheticMaintenanceOps:
    """Persistent fixture effects; session/process evidence is independently reset.

    No actual cron, permission, privilege, service or production operation exists.
    """
    def __init__(self):
        self.pe4="5,35 * * * * /fixture/pe4-python -I -B /fixture/hioc-home-assistant-association.py"
        self.pe5="2,17,32,47 * * * * /fixture/hioc-compose-service-associations.py"
        self.history="*/5 * * * * /fixture/hioc-history-engine.py"
        self.other="0 1 * * * /fixture/unrelated-job"
        self.raw=("# exact synthetic original\n\n"+"\n".join((*d.CRON,self.pe4,self.pe5,self.history,self.other))+"\n").encode()
        self.original=self.raw
        self.approved=[*d.CRON,self.pe4,self.pe5]
        self.inventory={line:("EXCLUDE" if line in self.approved else "PRESERVE")
            for line in self.raw.decode().splitlines() if line and not line.startswith("#")}
        self.metadata={"uid":1000,"gid":1000,"metadata":{"kind":"SYNTHETIC_ONLY","spool":"NOT_OBSERVED"}}
        self.original_fence={"st_dev":1,"st_ino":2,"st_uid":1000,"st_gid":1000,
            "mode":0o700,"type":"DIRECTORY","acl":"ABSENT"}
        self.current=copy.deepcopy(self.original_fence)
        self.flags={key:True for key in d.BOUNDARY_FIELDS}
        self.session="SYNTHETIC_SESSION_1"
        self.fail=None; self.after_effect=False; self.concurrent_edit=False; self.calls=[]

    def scheduler(self): return self.raw,copy.deepcopy(self.metadata)
    def fence(self): return copy.deepcopy(self.current)
    def install_scheduler(self, raw, expected_sha):
        self.calls.append("scheduler")
        if self.concurrent_edit:self.raw+=b"# concurrent editor\n"
        d.require(d.sha(self.raw)==expected_sha,"MAINTENANCE_SCHEDULER_DRIFT")
        if self.fail=="scheduler" and not self.after_effect: raise OSError("synthetic scheduler failure")
        self.raw=raw
        if self.fail=="scheduler":raise OSError("synthetic uncertain scheduler result")
    def restrict(self, reference, binding):
        d.authorization(reference,binding);self.calls.append("restrict")
        if self.fail=="restrict" and not self.after_effect:raise OSError("synthetic fence failure")
        self.current["mode"]=0
        if self.fail=="restrict":raise OSError("synthetic uncertain fence")
    def restore(self, reference, binding):
        d.authorization(reference,binding);self.calls.append("restore")
        if self.fail=="restore" and not self.after_effect:raise OSError("synthetic release failure")
        self.current=copy.deepcopy(self.original_fence)
        if self.fail=="restore":raise OSError("synthetic uncertain release")
    def boundary(self, scope):
        return dict(self.flags,kind="SYNTHETIC_ONLY",session=self.session,scope_sha256=scope)
    def drain(self, scope):self.calls.append("drain");return self.boundary(scope)


class MaintenanceTests(unittest.TestCase):
    def setUp(self):self._start()
    def _start(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.fs=FixtureFS(self.root);self.ops=SyntheticMaintenanceOps()
        self.provider=d.MaintenanceConsumers(self.ops,self.ops.approved,self.ops.inventory)
        self.c=d.Controller(self.fs,SOURCE,self.provider);self.m=d.Maintenance(self.c);self.counter=0
        report=d.preflight(self.fs,SOURCE,self.provider)
        self.c.prepare("PREPARE_SYNTHETIC",d.sha(d.canonical(report)))
    def tearDown(self):self.fs.assert_unrelated(self);self.temp.cleanup()
    def step(self,name):
        self.counter+=1
        return getattr(self.m,name)("MAINTENANCE_%03d"%self.counter,d.sha(d.canonical(self.c._journal())))
    def establish(self):
        for name in ("preserve","exclude","restrict","drain","establish"):self.step(name)
    def commit(self):
        self.establish();return self.c.commit("COMMIT_SYNTHETIC",self.c.inspect()["journal_sha256"])
    def release(self):
        for name in ("authorize_release","restore_scheduler","release_access"):self.step(name)

    def test_not_established_and_exact_scheduler_preservation(self):
        self.assertEqual(self.m.inspect()["phase"],"NOT_ESTABLISHED")
        with self.assertRaisesRegex(d.Failure,"MAINTENANCE_NOT_ESTABLISHED"):
            self.c.commit("COMMIT_SYNTHETIC",self.c.inspect()["journal_sha256"])
        self.step("preserve")
        self.assertEqual(self.fs.read(d.TX+"/crontab-original"),self.ops.original)
        self.assertEqual(self.ops.raw,self.ops.original)
        self.assertEqual(self.ops.current,self.ops.original_fence)

    def test_scheduler_preservation_failure_prevents_exclusion(self):
        self.fs.fail=lambda name:name==d.TX+"/crontab-original"
        with self.assertRaises(OSError):self.step("preserve")
        self.assertEqual(self.m.inspect()["phase"],"PRESERVATION_UNCERTAIN")
        self.assertEqual(self.ops.calls,[])
        with self.assertRaises(d.Failure):self.step("exclude")
        self.assertFalse(self.fs.publications)

    def test_exact_exclusion_preserves_history_comments_and_unrelated_jobs(self):
        self.step("preserve");self.step("exclude")
        expected=d.maintenance_cron(self.ops.original,self.ops.approved,self.ops.inventory)
        self.assertEqual(self.ops.raw,expected)
        self.assertIn((self.ops.history+"\n").encode(),self.ops.raw)
        self.assertIn((self.ops.other+"\n").encode(),self.ops.raw)
        self.assertTrue(self.ops.raw.startswith(b"# exact synthetic original\n\n"))
        for job in self.ops.approved:self.assertNotIn((job+"\n").encode(),self.ops.raw)

    def test_incomplete_unknown_duplicate_or_unapproved_job_inventory_rejected(self):
        for approved,inventory in ((self.ops.approved[:-1],self.ops.inventory),
                (self.ops.approved,self.ops.inventory|{"unknown":"PRESERVE"}),
                (self.ops.approved+[self.ops.approved[0]],self.ops.inventory),
                (self.ops.approved,{k:v for k,v in self.ops.inventory.items() if k!=self.ops.history})):
            with self.assertRaises(d.Failure):d.maintenance_cron(self.ops.original,approved,inventory)

    def test_concurrent_scheduler_edit_before_or_during_exclusion(self):
        self.step("preserve")
        self.ops.raw+=b"# external change\n"
        with self.assertRaisesRegex(d.Failure,"MAINTENANCE_SCHEDULER_DRIFT"):self.step("exclude")
        self.assertIn(b"# external change",self.ops.raw)
        self.ops.raw=self.ops.original;self.ops.concurrent_edit=True
        with self.assertRaisesRegex(d.Failure,"MAINTENANCE_SCHEDULER_DRIFT"):self.step("exclude")
        self.assertIn(b"# concurrent editor",self.ops.raw)
        self.assertFalse(self.fs.publications)

    def test_failed_or_uncertain_scheduler_exclusion_cannot_publish(self):
        self.step("preserve");self.ops.fail="scheduler";self.ops.after_effect=True
        with self.assertRaises(OSError):self.step("exclude")
        self.assertEqual(self.m.inspect()["phase"],"EXCLUSION_UNCERTAIN")
        with self.assertRaises(d.Failure):self.c.commit("COMMIT_SYNTHETIC",self.c.inspect()["journal_sha256"])
        self.assertFalse(self.fs.publications)

    def test_failed_permission_restriction_does_not_establish_fence(self):
        self.step("preserve");self.step("exclude");self.ops.fail="restrict"
        with self.assertRaises(OSError):self.step("restrict")
        self.assertEqual(self.m.inspect()["phase"],"FENCE_UNCERTAIN")
        self.assertFalse(self.m.inspect()["fence_identity_matches"])
        with self.assertRaises(d.Failure):self.step("drain")

    def test_uncertain_permission_result_stays_blocked_even_if_fenced(self):
        self.step("preserve");self.step("exclude");self.ops.fail="restrict";self.ops.after_effect=True
        with self.assertRaises(OSError):self.step("restrict")
        self.assertTrue(self.m.inspect()["fence_identity_matches"])
        with self.assertRaises(d.Failure):self.step("drain")

    def test_existing_process_drain_failure_retains_fence(self):
        for name in ("preserve","exclude","restrict"):self.step(name)
        self.ops.flags["cached_modules_drained"]=False
        with self.assertRaisesRegex(d.Failure,"MAINTENANCE_DRAIN_FAILED"):self.step("drain")
        self.assertEqual(self.m.inspect()["phase"],"DRAIN_UNCERTAIN")
        self.assertTrue(self.m.inspect()["fence_identity_matches"])
        self.assertFalse(self.fs.publications)

    def test_each_independent_caller_and_persistence_limit_blocks_commit(self):
        self.establish()
        for key in d.BOUNDARY_FIELDS:
            self.ops.flags[key]=False
            with self.subTest(key=key),self.assertRaisesRegex(d.Failure,"MAINTENANCE_DRAIN_NOT_CURRENT"):
                self.c.commit("COMMIT_SYNTHETIC",self.c.inspect()["journal_sha256"])
            self.ops.flags[key]=True
        self.assertFalse(self.fs.publications)

    def test_controller_termination_at_maintenance_transitions_never_releases(self):
        for phase,method in (("EXCLUSION_UNCERTAIN","exclude"),("FENCE_UNCERTAIN","restrict"),
                ("DRAIN_UNCERTAIN","drain")):
            with self.subTest(phase=phase):
                if method=="exclude":self.step("preserve")
                elif method=="restrict":
                    # Previous exclusion stopped before the effect. Restore only this
                    # isolated fixture to a fresh transaction, never production resume.
                    self.tearDown();self._start();self.step("preserve");self.step("exclude")
                else:
                    self.tearDown();self._start()
                    for name in ("preserve","exclude","restrict"):self.step(name)
                def interrupt(point,phase=phase):
                    if point=="MAINTENANCE:"+phase:raise KeyboardInterrupt()
                self.c.fault=interrupt
                with self.assertRaises(KeyboardInterrupt):self.step(method)
                self.assertEqual(self.m.inspect()["phase"],phase)
                self.assertFalse(self.fs.publications)
                self.assertNotIn("restore",self.ops.calls)

    def test_every_recorded_partial_publication_keeps_persistent_exclusion(self):
        for index,path in enumerate(d.ORDER):
            if index:self.tearDown();self._start()
            self.establish()
            def interrupt(point,path=path):
                if point=="INSTALLED:"+path:raise KeyboardInterrupt()
            self.c.fault=interrupt
            with self.subTest(path=path),self.assertRaises(KeyboardInterrupt):
                self.c.commit("COMMIT_SYNTHETIC",self.c.inspect()["journal_sha256"])
            self.assertEqual(self.m.inspect()["phase"],"INSTALLATION_UNCERTAIN")
            self.assertTrue(self.m.inspect()["fence_identity_matches"])
            self.assertEqual(self.fs.publications,d.ORDER[:index+1])
            with self.assertRaises(d.Failure):self.step("authorize_release")
            self.assertNotIn("restore",self.ops.calls)

    def test_every_unconfirmed_publication_remains_uncertain(self):
        for index,path in enumerate(d.ORDER):
            if index:self.tearDown();self._start()
            self.establish()
            def interrupt(point,path=path):
                if point=="AFTER_PUBLICATION:"+path:raise KeyboardInterrupt()
            self.c.fault=interrupt
            with self.subTest(path=path),self.assertRaises(KeyboardInterrupt):
                self.c.commit("COMMIT_SYNTHETIC",self.c.inspect()["journal_sha256"])
            self.assertEqual(self.c.inspect()["pending"],path)
            self.assertFalse(self.c.inspect()["live_state_established"])
            self.assertTrue(self.m.inspect()["fence_identity_matches"])
            with self.assertRaises(d.Failure):self.step("authorize_release")

    def test_interrupted_rollback_keeps_access_closed(self):
        info=self.commit()
        def interrupt(point):
            if point=="RESTORED:"+d.ORDER[-1]:raise KeyboardInterrupt()
        self.c.fault=interrupt
        with self.assertRaises(KeyboardInterrupt):self.c.rollback("ROLLBACK_SYNTHETIC",info["journal_sha256"])
        self.assertEqual(self.m.inspect()["phase"],"ROLLBACK_UNCERTAIN")
        self.assertTrue(self.m.inspect()["fence_identity_matches"])
        with self.assertRaises(d.Failure):self.step("authorize_release")

    def test_restart_reconstruction_requires_new_drain_evidence(self):
        self.establish();self.ops.session="SYNTHETIC_SESSION_AFTER_REBOOT"
        self.c=d.Controller(self.fs,SOURCE,self.provider);self.m=d.Maintenance(self.c)
        self.assertTrue(self.m.inspect()["fence_identity_matches"])
        with self.assertRaisesRegex(d.Failure,"MAINTENANCE_DRAIN_NOT_CURRENT"):
            self.c.commit("COMMIT_SYNTHETIC",self.c.inspect()["journal_sha256"])
        self.step("redrain")
        self.assertEqual(self.c.commit("COMMIT_SYNTHETIC",self.c.inspect()["journal_sha256"])["state"],"COMMITTED")

    def test_interrupted_redrain_is_explicitly_uncertain_and_not_auto_resumed(self):
        self.establish();self.ops.session="SYNTHETIC_NEW_SESSION"
        def interrupt(point):
            if point=="MAINTENANCE:REDRAIN_UNCERTAIN":raise KeyboardInterrupt()
        self.c.fault=interrupt
        with self.assertRaises(KeyboardInterrupt):self.step("redrain")
        self.assertEqual(self.m.inspect()["phase"],"REDRAIN_UNCERTAIN")
        with self.assertRaises(d.Failure):self.provider.assert_active()
        self.c.fault=lambda _:None;self.step("redrain")
        self.provider.assert_active()

    def test_failed_scheduler_restoration_never_releases_fence(self):
        self.commit();self.step("authorize_release");self.ops.fail="scheduler";self.ops.after_effect=True
        with self.assertRaises(OSError):self.step("restore_scheduler")
        self.assertEqual(self.m.inspect()["phase"],"SCHEDULER_RESTORE_UNCERTAIN")
        self.assertEqual(self.ops.raw,self.ops.original)
        self.assertTrue(self.m.inspect()["fence_identity_matches"])
        with self.assertRaises(d.Failure):self.step("release_access")

    def test_unauthorized_or_premature_access_release_refused(self):
        self.establish()
        with self.assertRaises(d.Failure):self.step("release_access")
        with self.assertRaises(d.Failure):self.m.release_access(None,"a"*64)
        self.assertTrue(self.m.inspect()["fence_identity_matches"])

    def test_exact_successful_restoration_after_verified_installation(self):
        self.commit();self.release()
        self.assertEqual(self.m.inspect()["phase"],"ACCESS_RESTORED_VERIFIED")
        self.assertEqual(self.ops.raw,self.ops.original)
        self.assertEqual(self.ops.current,self.ops.original_fence)
        self.assertFalse(self.m.inspect()["production_qualified"])
        with self.assertRaises(d.Failure):self.step("release_access")
        with self.assertRaises(d.Failure):self.c.rollback("ROLLBACK_SYNTHETIC",self.c.inspect()["journal_sha256"])

    def test_exact_release_after_separately_authorized_rollback(self):
        info=self.commit();self.c.rollback("ROLLBACK_SYNTHETIC",info["journal_sha256"])
        self.assertEqual(self.m.inspect()["phase"],"RESTORATION_VERIFIED")
        self.release();self.assertEqual(self.ops.current,self.ops.original_fence)
        for path in SOURCE:
            self.assertEqual(self.fs.path(path).read_bytes(),BASE[path]) if path in BASE else self.assertFalse(self.fs.path(path).exists())

    def test_uncertain_final_access_release_does_not_claim_restored(self):
        self.commit();self.step("authorize_release");self.step("restore_scheduler")
        self.ops.fail="restore";self.ops.after_effect=True
        with self.assertRaises(OSError):self.step("release_access")
        self.assertEqual(self.m.inspect()["phase"],"ACCESS_RELEASE_UNCERTAIN")
        self.assertTrue(self.m.inspect()["access_metadata_restored"])
        self.assertEqual(self.c.inspect()["state"],"COMMITTED")
        with self.assertRaises(d.Failure):self.step("release_access")

    def test_stale_reference_duplicate_operation_and_stale_binding(self):
        binding=self.c.inspect()["journal_sha256"]
        self.m.preserve("UNIQUE_MAINTENANCE",binding)
        with self.assertRaisesRegex(d.Failure,"MAINTENANCE_STALE_AUTHORIZATION"):
            self.m.exclude("NEXT_MAINTENANCE",binding)
        fresh=self.c.inspect()["journal_sha256"]
        with self.assertRaisesRegex(d.Failure,"MAINTENANCE_AUTHORIZATION_REUSED"):
            self.m.exclude("UNIQUE_MAINTENANCE",fresh)
        with self.assertRaisesRegex(d.Failure,"MAINTENANCE_TRANSITION_REFUSED"):
            self.m.preserve("OTHER_MAINTENANCE",fresh)

    def test_privileged_interface_and_native_path_reject_without_effects(self):
        native=d.NativeFenceInterface()
        self.assertEqual(native.target,"/home/jazofv1/hioc/pi4/lib/hioc")
        for name in ("restrict","restore"):
            with self.assertRaisesRegex(d.Failure,"NATIVE_FENCE_NOT_QUALIFIED"):
                getattr(native,name)("SEPARATE_AUTHORIZATION","a"*64)
            with self.assertRaises(TypeError):getattr(native,name)("x","a"*64,path="/etc")
        with self.assertRaisesRegex(d.Failure,"NATIVE_MAINTENANCE_NOT_QUALIFIED"):
            d.Maintenance(d.Controller(self.fs,SOURCE,d.NativeConsumers()))
        with patch.object(d.os,"name","posix"):
            with self.assertRaisesRegex(d.Failure,"NATIVE_MAINTENANCE_NOT_QUALIFIED"):
                d.MaintenanceConsumers(self.ops,self.ops.approved,self.ops.inventory)
        self.assertEqual(self.ops.calls,[])

    def test_runtime_scheduler_or_fence_drift_blocks_release(self):
        self.commit()
        self.fs.path(d.ORDER[-1]).write_bytes(b"unexpected target")
        with self.assertRaisesRegex(d.Failure,"MAINTENANCE_RUNTIME_DRIFT"):self.step("authorize_release")
        self.assertTrue(self.m.inspect()["fence_identity_matches"])

    def test_maintenance_journal_tampering_cannot_establish_exclusion(self):
        self.establish();original=self.c._journal()
        for change in (lambda v:v["maintenance"].update(phase="ACCESS_RESTORED_VERIFIED"),
                lambda v:v["maintenance"].update(boundary=None),
                lambda v:v["maintenance"]["authorizations"].append(v["maintenance"]["authorizations"][0]),
                lambda v:v["maintenance"].update(approved_jobs=[])):
            value=copy.deepcopy(original);change(value);self.fs.journal(value)
            with self.assertRaises(d.Failure):self.provider.assert_active()
        self.fs.journal(original)
        self.fs.path(d.TX+"/crontab-original").write_bytes(b"changed backup")
        with self.assertRaises(d.Failure):self.provider.assert_active()

    def test_maintenance_performs_no_commands_network_or_native_permission_changes(self):
        # Existing AssetLock legitimately chmods its isolated Windows fixture.
        # Allow only that exact operation; reject package/runtime chmod calls.
        native_chmod = d.os.chmod
        def fixture_lock_chmod(path, mode, *args, **kwargs):
            self.assertEqual(Path(path), self.root/"backups"/".synthetic-deployment.lock")
            self.assertEqual(mode, 0o600)
            return native_chmod(path, mode, *args, **kwargs)
        with patch.object(d.subprocess,"run",side_effect=AssertionError("unexpected command")), \
                patch.object(d.socket,"socket",side_effect=AssertionError("unexpected network")), \
                patch.object(d.os,"chmod",side_effect=fixture_lock_chmod), \
                patch.object(d.os,"chown",side_effect=AssertionError("native chown forbidden"),create=True):
            self.commit();self.release()
        self.fs.assert_unrelated(self)


    def test_phase_requires_ordered_authorization_history(self):
        self.establish();original=self.c._journal()
        for actions in (original["maintenance"]["authorizations"][:1],
                list(reversed(original["maintenance"]["authorizations"]))):
            value=copy.deepcopy(original);value["maintenance"]["authorizations"]=actions
            self.fs.journal(value)
            with self.assertRaisesRegex(d.Failure,"MAINTENANCE_JOURNAL_INVALID"):
                self.provider.assert_active()



class RecoveryAttachmentTests(unittest.TestCase):
    setUp = MaintenanceTests.setUp
    _start = MaintenanceTests._start
    tearDown = MaintenanceTests.tearDown
    step = MaintenanceTests.step
    establish = MaintenanceTests.establish
    commit = MaintenanceTests.commit
    release = MaintenanceTests.release

    def restart(self, reference="RECOVERY_ATTACH_001", binding=None, same_session=False):
        # Retain only modeled external effects and the on-disk transaction.
        # Neither the provider, controller, proof object nor original plan survives.
        raw,metadata=self.ops.scheduler()
        effects=json.loads(json.dumps({"scheduler":raw.hex(),"metadata":metadata,
            "fence":self.ops.fence()}))
        self.c=None;self.provider=None;self.m=None;self.ops=None
        ops=SyntheticMaintenanceOps.__new__(SyntheticMaintenanceOps)
        ops.raw=bytes.fromhex(effects["scheduler"]);ops.metadata=effects["metadata"]
        ops.current=effects["fence"];ops.flags={k:True for k in d.BOUNDARY_FIELDS}
        ops.session="SYNTHETIC_SESSION_1" if same_session else "FRESH_RECOVERY_SESSION"
        ops.fail=None;ops.after_effect=False;ops.concurrent_edit=False;ops.calls=[]
        self.ops=ops
        if binding is None:binding=d.sha(self.fs.read(d.TX+"/journal.json"))
        c=d.MaintenanceConsumers.attach(self.fs,SOURCE,ops,reference,binding)
        self.c=c;self.provider=c.consumers;self.m=d.Maintenance(c)
        # Fixture restore behavior is initialized from independently validated
        # persisted originals, not the destroyed backend's in-memory originals.
        value=c._journal();ops.original=self.fs.read(d.TX+"/crontab-original")
        ops.original_fence=copy.deepcopy(value["maintenance"]["original_fence"])
        return value

    def test_fresh_initial_preparation_stays_strict(self):
        self.assertNotIn("maintenance",self.c._journal())
        self.assertEqual(self.provider.observe()["cron_sha256"],d.sha(self.ops.original))
        reduced=d.maintenance_cron(self.ops.original,self.ops.approved,self.ops.inventory)
        self.ops.raw=reduced
        with self.assertRaisesRegex(d.Failure,"MAINTENANCE_JOB_INVENTORY"):
            d.MaintenanceConsumers(self.ops,self.ops.approved,self.ops.inventory)
        with self.assertRaises(d.Failure):self.c.commit("COMMIT_SYNTHETIC",self.c.inspect()["journal_sha256"])

    def test_fresh_provider_reconstruction_against_reduced_cron(self):
        self.establish()
        original_sha=self.c._journal()["maintenance"]["original_cron_sha256"]
        value=self.restart()
        self.assertEqual(self.provider.observe()["cron_sha256"],original_sha)
        self.assertNotEqual(d.sha(self.ops.raw),original_sha)
        self.assertEqual(self.provider.approved_jobs,value["maintenance"]["approved_jobs"])
        self.assertTrue(self.m.inspect()["process_requalification_required"])
        with self.assertRaisesRegex(d.Failure,"MAINTENANCE_DRAIN_NOT_CURRENT"):
            self.c.commit("COMMIT_SYNTHETIC",self.c.inspect()["journal_sha256"])
        self.step("redrain")
        self.assertEqual(self.c.commit("COMMIT_SYNTHETIC",self.c.inspect()["journal_sha256"])["state"],"COMMITTED")

    def test_attach_before_scheduler_exclusion_preserves_original_preparation(self):
        self.step("preserve");self.restart()
        self.assertEqual(self.m.inspect()["phase"],"SCHEDULER_PRESERVED")
        for name in ("exclude","restrict","drain","establish"):self.step(name)
        self.provider.assert_active()

    def test_attach_after_exclusion_before_fence(self):
        self.step("preserve");self.step("exclude");self.restart()
        self.assertEqual(self.m.inspect()["phase"],"LAUNCHES_EXCLUDED")
        for name in ("restrict","drain","establish"):self.step(name)
        self.provider.assert_active()

    def test_attach_after_drain_requires_fresh_drain_even_with_identical_session(self):
        for name in ("preserve","exclude","restrict","drain"):self.step(name)
        self.restart(same_session=True)
        with self.assertRaisesRegex(d.Failure,"MAINTENANCE_DRAIN_NOT_CURRENT"):self.step("establish")
        self.step("redrain");self.step("establish");self.provider.assert_active()

    def test_partial_publication_attachment_preserves_prefix_and_separate_rollback(self):
        self.establish()
        def stop(point):
            if point=="INSTALLED:"+d.ORDER[2]:raise KeyboardInterrupt()
        self.c.fault=stop
        with self.assertRaises(KeyboardInterrupt):self.c.commit("COMMIT_SYNTHETIC",self.c.inspect()["journal_sha256"])
        value=self.restart();self.assertEqual(len(value["installed"]),3)
        with self.assertRaises(d.Failure):self.step("authorize_release")
        with self.assertRaisesRegex(d.Failure,"MAINTENANCE_DRAIN_NOT_CURRENT"):
            self.c.rollback("ROLLBACK_SYNTHETIC",self.c.inspect()["journal_sha256"])
        self.step("redrain")
        self.c.rollback("ROLLBACK_SYNTHETIC",self.c.inspect()["journal_sha256"])
        self.assertEqual(self.m.inspect()["phase"],"RESTORATION_VERIFIED")

    def test_unconfirmed_publication_attachment_does_not_adopt_or_resume(self):
        self.establish()
        def stop(point):
            if point=="AFTER_PUBLICATION:"+d.ORDER[0]:raise KeyboardInterrupt()
        self.c.fault=stop
        with self.assertRaises(KeyboardInterrupt):self.c.commit("COMMIT_SYNTHETIC",self.c.inspect()["journal_sha256"])
        value=self.restart();self.assertEqual(value["pending"],d.ORDER[0]);self.assertFalse(value["installed"])
        self.step("redrain")
        with self.assertRaisesRegex(d.Failure,"ROLLBACK_STATE_REFUSED"):
            self.c.rollback("ROLLBACK_SYNTHETIC",self.c.inspect()["journal_sha256"])
        with self.assertRaises(d.Failure):self.step("authorize_release")
        self.assertFalse(self.c.inspect()["live_state_established"])

    def test_interrupted_rollback_attachment_preserves_uncertainty(self):
        info=self.commit()
        def stop(point):
            if point=="RESTORED:"+d.ORDER[-1]:raise KeyboardInterrupt()
        self.c.fault=stop
        with self.assertRaises(KeyboardInterrupt):self.c.rollback("ROLLBACK_SYNTHETIC",info["journal_sha256"])
        value=self.restart();self.assertEqual(value["state"],"ROLLING_BACK")
        self.assertEqual(set(value["restored"]),{d.ORDER[-1]})
        self.step("redrain")
        with self.assertRaises(d.Failure):self.step("authorize_release")
        with self.assertRaisesRegex(d.Failure,"ROLLBACK_STATE_REFUSED"):
            self.c.rollback("ROLLBACK_AGAIN",self.c.inspect()["journal_sha256"])

    def test_committed_held_transaction_attachment_does_not_authorize_release(self):
        self.commit();self.restart(same_session=True)
        with self.assertRaises(d.Failure):self.step("restore_scheduler")
        with self.assertRaisesRegex(d.Failure,"MAINTENANCE_DRAIN_NOT_CURRENT"):self.step("authorize_release")
        self.step("redrain");self.release()
        self.assertEqual(self.m.inspect()["phase"],"ACCESS_RESTORED_VERIFIED")

    def test_attachment_after_scheduler_restoration_requires_new_drain(self):
        self.commit();self.step("authorize_release");self.step("restore_scheduler")
        self.restart(same_session=True)
        with self.assertRaisesRegex(d.Failure,"MAINTENANCE_DRAIN_NOT_CURRENT"):self.step("release_access")
        self.step("redrain");self.step("release_access")
        self.assertEqual(self.m.inspect()["phase"],"ACCESS_RESTORED_VERIFIED")

    def test_attachment_after_release_authorization_preserves_bound_runtime(self):
        self.commit();self.step("authorize_release");self.restart()
        with self.assertRaisesRegex(d.Failure,"MAINTENANCE_DRAIN_NOT_CURRENT"):self.step("restore_scheduler")
        self.step("redrain");self.step("restore_scheduler");self.step("release_access")
        self.assertEqual(self.m.inspect()["phase"],"ACCESS_RESTORED_VERIFIED")

    def test_missing_original_backup_rejected(self):
        self.establish();self.fs.path(d.TX+"/crontab-original").unlink()
        with self.assertRaises(d.Failure):self.restart()

    def test_corrupted_original_backup_rejected(self):
        self.establish();self.fs.path(d.TX+"/crontab-original").write_bytes(b"bad scheduler\n")
        with self.assertRaises(d.Failure):self.restart()

    def test_backup_journal_digest_mismatch_rejected(self):
        self.establish();value=self.c._journal();value["maintenance"]["original_cron_sha256"]="0"*64
        self.fs.journal(value)
        with self.assertRaises(d.Failure):self.restart()

    def test_wrong_approved_job_set_rejected(self):
        self.establish();value=self.c._journal();value["maintenance"]["approved_jobs"].pop()
        self.fs.journal(value)
        with self.assertRaises(d.Failure):self.restart()

    def test_unrecognized_scheduler_or_account_rejected(self):
        self.establish();self.ops.raw+=b"# unauthorized edit\n"
        with self.assertRaisesRegex(d.Failure,"RECOVERY_SCHEDULER_MISMATCH"):self.restart()

    def test_unexpected_fence_identity_rejected(self):
        self.establish();self.ops.current["st_ino"]+=1
        with self.assertRaisesRegex(d.Failure,"RECOVERY_FENCE_MISMATCH"):self.restart()

    def test_fence_symlink_type_rejected(self):
        self.establish();self.ops.current["type"]="SYMLINK"
        with self.assertRaisesRegex(d.Failure,"MAINTENANCE_FENCE_IDENTITY"):self.restart()

    def test_unexpected_artifact_drift_rejected(self):
        self.establish();self.fs.path(next(iter(d.PRIOR))).write_bytes(b"unexpected runtime bytes")
        with self.assertRaisesRegex(d.Failure,"RECOVERY_RUNTIME_DRIFT"):self.restart()

    def test_conflicting_journal_state_rejected(self):
        self.establish();value=self.c._journal();value["maintenance"]["phase"]="INSTALLATION_VERIFIED"
        self.fs.journal(value)
        with self.assertRaises(d.Failure):self.restart()

    def test_wrong_release_or_transaction_version_rejected(self):
        self.establish();original=self.c._journal()
        for key,new in (("release","0"*40),("version",2)):
            value=copy.deepcopy(original);value[key]=new;self.fs.journal(value)
            with self.assertRaises(d.Failure):
                d.MaintenanceConsumers.attach(self.fs,SOURCE,self.ops,"RECOVERY_BAD_OBJECT",d.sha(d.canonical(value)))
        self.fs.journal(original)

    def test_duplicate_journal_fields_rejected(self):
        self.establish();raw=self.fs.read(d.TX+"/journal.json")
        raw=raw.replace(b'{',b'{"version":1,',1);self.fs.path(d.TX+"/journal.json").write_bytes(raw)
        with self.assertRaisesRegex(d.Failure,"JOURNAL_INVALID"):self.restart()

    def test_completed_transaction_cannot_start_new_maintenance(self):
        self.commit();self.release()
        with self.assertRaisesRegex(d.Failure,"RECOVERY_ALREADY_COMPLETED"):self.restart()

    def test_unrelated_legacy_transaction_rejected(self):
        self.establish();value=self.c._journal();del value["maintenance"];self.fs.journal(value)
        with self.assertRaisesRegex(d.Failure,"RECOVERY_UNRELATED_TRANSACTION"):self.restart()

    def test_duplicate_attach_and_reused_authorization_refused(self):
        self.establish();old=d.sha(self.fs.read(d.TX+"/journal.json"));self.restart(reference="RECOVERY_UNIQUE")
        with self.assertRaisesRegex(d.Failure,"MAINTENANCE_STALE_AUTHORIZATION"):
            d.MaintenanceConsumers.attach(self.fs,SOURCE,self.ops,"RECOVERY_OTHER",old)
        with self.assertRaisesRegex(d.Failure,"MAINTENANCE_AUTHORIZATION_REUSED"):
            self.restart(reference="RECOVERY_UNIQUE")

    def test_uncertain_scheduler_exclusion_is_observed_without_adoption(self):
        self.step("preserve");self.ops.fail="scheduler";self.ops.after_effect=True
        with self.assertRaises(OSError):self.step("exclude")
        self.restart();self.assertEqual(self.m.inspect()["phase"],"EXCLUSION_UNCERTAIN")
        with self.assertRaises(d.Failure):self.step("restrict")
        with self.assertRaises(d.Failure):self.step("release_access")

    def test_uncertain_final_access_release_remains_uncertain(self):
        self.commit();self.step("authorize_release");self.step("restore_scheduler")
        self.ops.fail="restore";self.ops.after_effect=True
        with self.assertRaises(OSError):self.step("release_access")
        self.restart();self.assertEqual(self.m.inspect()["phase"],"ACCESS_RELEASE_UNCERTAIN")
        self.assertTrue(self.m.inspect()["access_metadata_restored"])
        with self.assertRaises(d.Failure):self.step("release_access")

    def test_native_attachment_refused_before_any_effect(self):
        with patch.object(d.os,"name","posix"):
            with self.assertRaisesRegex(d.Failure,"NATIVE_MAINTENANCE_NOT_QUALIFIED"):
                d.MaintenanceConsumers.attach(self.fs,SOURCE,self.ops,"RECOVERY_NATIVE_BLOCK","a"*64)
        self.assertNotIn("maintenance",self.c._journal())
        self.assertEqual(self.ops.calls,[])

    def test_new_attachment_durably_invalidates_older_provider_context(self):
        self.establish();old_provider=self.provider;old_maintenance=self.m
        self.restart()
        self.assertTrue(old_maintenance.inspect()["process_requalification_required"])
        with self.assertRaisesRegex(d.Failure,"MAINTENANCE_ATTACHMENT_SUPERSEDED"):
            old_provider.assert_active()
        with self.assertRaisesRegex(d.Failure,"MAINTENANCE_ATTACHMENT_SUPERSEDED"):
            old_maintenance.redrain("OBSOLETE_DRAIN_CONTEXT",self.c.inspect()["journal_sha256"])
        self.step("redrain");self.provider.assert_active()


    def test_existing_transaction_cannot_use_new_initial_context(self):
        self.commit();self.step("authorize_release");self.step("restore_scheduler")
        fresh=d.MaintenanceConsumers(self.ops,self.ops.approved,self.ops.inventory)
        controller=d.Controller(self.fs,SOURCE,fresh)
        with self.assertRaisesRegex(d.Failure,"RECOVERY_ATTACHMENT_REQUIRED"):
            d.Maintenance(controller)
        self.assertEqual(self.ops.current["mode"],0)
        self.assertNotIn("restore",self.ops.calls)



class SourceCheckoutCompatibilityTests(unittest.TestCase):
    """Source integrity is independent of checkout SHA and mutation authorization."""
    def run_gate(self, checkout, override=None, related=True):
        calls = []
        def command(argv, **kwargs):
            args = argv[3:]; calls.append(args)
            if args == ["rev-parse", "--verify", "HEAD^{commit}"]: raw = (checkout+"\n").encode()
            elif args == ["rev-parse", "--verify", d.RELEASE+"^{commit}"]: raw = (d.RELEASE+"\n").encode()
            elif args == ["merge-base", "--is-ancestor", d.RELEASE, "HEAD"]:
                if not related: return subprocess.CompletedProcess(argv, 1, b"", b"")
                raw = b""
            elif args == ["rev-parse", "--show-toplevel"]: raw = (str(ROOT)+"\n").encode()
            elif args == ["remote", "get-url", "origin"]: raw = b"https://github.com/jorgeazofeifa-creator/hioc.git\n"
            elif args == ["status", "--porcelain=v1", "--untracked-files=all"]: raw = b""
            elif args[0] == "show":
                self.assertTrue(args[1].startswith(d.RELEASE+":"))
                raw = SOURCE[args[1].split(":",1)[1]]
            elif args[0] == "rev-parse" and ":" in args[1]:
                self.assertTrue(args[1].startswith(d.RELEASE+":"))
                raw = (next(x["git_blob"] for x in d.MANIFEST if x["path"] == args[1].split(":",1)[1])+"\n").encode()
            else: raise AssertionError(args)
            if override is not None: raw = override(args, raw)
            return subprocess.CompletedProcess(argv, 0, raw, b"")
        with patch.object(d.subprocess, "run", side_effect=command):
            result = d.source_gate(ROOT)
        return result, calls

    def test_exact_approved_checkout_reads_all_thirteen_immutable_payload_objects(self):
        self.assertFalse(hasattr(d,"QUALIFICATION_CHECKOUT"))
        self.assertEqual(d.RELEASE,"51398bab4e2293b578b2cdac2d0740c3738cab2f")
        result,calls=self.run_gate("302a4e3f34f53fffb8299771d31c115e052b5400")
        self.assertEqual(result,SOURCE)
        self.assertEqual(sum(a[0]=="show" for a in calls),13)
        self.assertEqual(sum(a[0]=="rev-parse" and ":" in a[1] for a in calls),13)

    def test_original_payload_checkout_remains_accepted_for_historical_compatibility(self):
        self.assertEqual(self.run_gate(d.RELEASE)[0],SOURCE)

    def test_unrelated_history_is_rejected_independently_of_checkout_sha(self):
        for checkout in ("0"*40,"f"*40,"d64d772f82728a41d920eb64433ee2398645097f",
                         "302a4e3f34f53fffb8299771d31c115e052b5400"[:-1]+"1"):
            with self.subTest(checkout=checkout):
                with self.assertRaisesRegex(d.Failure,"SOURCE_HISTORY_MISMATCH"):
                    self.run_gate(checkout,related=False)

    def test_approved_checkout_still_rejects_dirty_tracked_and_untracked_trees(self):
        for dirty in (b" M tracked.py\n",b"?? unexpected.py\n"):
            with self.subTest(dirty=dirty):
                with self.assertRaisesRegex(d.Failure,"SOURCE_DIRTY"):
                    self.run_gate("302a4e3f34f53fffb8299771d31c115e052b5400",lambda a,b:dirty if a[0]=="status" else b)

    def test_approved_checkout_still_rejects_wrong_root_and_origin(self):
        for target,code in ((["rev-parse","--show-toplevel"],"SOURCE_ROOT_MISMATCH"),
                            (["remote","get-url","origin"],"SOURCE_REMOTE_MISMATCH")):
            with self.subTest(code=code):
                with self.assertRaisesRegex(d.Failure,code):
                    self.run_gate("302a4e3f34f53fffb8299771d31c115e052b5400",lambda a,b:b"unexpected\n" if a==target else b)

    def test_each_payload_byte_and_git_blob_mismatch_is_rejected(self):
        for item in d.MANIFEST:
            for operation in ("show","rev-parse"):
                with self.subTest(path=item["path"],operation=operation):
                    target=[operation,d.RELEASE+":"+item["path"]]
                    with self.assertRaisesRegex(d.Failure,"SOURCE_IDENTITY_MISMATCH"):
                        self.run_gate("302a4e3f34f53fffb8299771d31c115e052b5400",
                            lambda a,b:b"tampered" if a==target else b)


if __name__ == "__main__":
    unittest.main()
