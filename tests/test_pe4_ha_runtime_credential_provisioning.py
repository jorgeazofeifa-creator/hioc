"""Synthetic-only filesystem/security tests. Never open /etc or request credentials."""
import ast
import contextlib
import copy
import errno
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import stat
import struct
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from tests.test_pe4_0c_association_contract import validate_schema

ROOT = Path(__file__).resolve().parents[1]
BASE = "d8e888023882770e2f158dc1fffebd5b354fb616"
NEXT = "PE-4 Home Assistant Runtime Credential Provisioning — Operator Installation"
RECORD_PATH = ROOT / "governance/pe4/pe4-ha-runtime-credential-provisioning-preparation.json"
SCHEMA_PATH = RECORD_PATH.with_suffix(".schema.json")


def load(name):
    path = ROOT / ("tools/hioc-pe4-ha-runtime-credential-" + name + ".py")
    spec = importlib.util.spec_from_file_location("credential_" + name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


P = load("provision")
V = load("validate")
GID = 12345
# Deliberately obvious local-test data, not HA token-shaped or usable credentials.
OLD = b"TEST_ONLY_OLD_INVALID_HA_CREDENTIAL\n"
NEW = "TEST_ONLY_NEW_INVALID_HA_CREDENTIAL"


def shared_open(path, flags, mode=0o600):
    """Windows fixture handles permit Linux-like unlink/rename while pinned.

    Keep real descriptors open: FILE_SHARE_DELETE models POSIX rename semantics,
    rather than closing the pinned descriptor to make a test pass.
    """
    if os.name != "nt": return os.open(path, flags, mode)
    import ctypes
    from ctypes import wintypes
    import msvcrt
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    create = kernel.CreateFileW
    create.argtypes = [wintypes.LPCWSTR,wintypes.DWORD,wintypes.DWORD,wintypes.LPVOID,wintypes.DWORD,wintypes.DWORD,wintypes.HANDLE]
    create.restype = wintypes.HANDLE
    access = 0x80000000 | 0x10000 | (0x40000000 if flags & os.O_RDWR else 0)
    handle = create(str(path), access, 7, None, 1 if flags & os.O_EXCL else 3, 0x80, None)
    if handle == ctypes.c_void_p(-1).value:
        error = ctypes.get_last_error()
        if error in (80,183): raise FileExistsError(errno.EEXIST,"test-only collision")
        raise ctypes.WinError(error)
    return msvcrt.open_osfhandle(handle, flags & (os.O_RDWR | getattr(os,"O_BINARY",0)))


class FixtureFS:
    """Real temporary byte flow/rename/link operations, injected POSIX metadata.

    Windows has no root/chown/POSIX ACL/dir_fd/flock. Their policy results are
    modeled explicitly; Linux syscall deployment remains a later operator proof.
    """
    def __init__(self, root):
        self.root = Path(root)
        self.handles = {}
        self.metadata = {}
        self.events = []
        self.counter = 100000
        self.fault = None
        self.short_write = None
        self.zero_write = False
        self.short_read = False
        self.collision = False
        self.changed = False
        self.acl_error = None
        self.root.mkdir(exist_ok=True)
        (self.root / "etc").mkdir()
        for path in (self.root, self.root / "etc"):
            self.setmeta(path, mode=0o755, gid=0)

    def event(self, name):
        self.events.append(name)
        if self.fault == name:
            if name == "interrupt": raise KeyboardInterrupt()
            raise OSError("TEST_ONLY_NEW_INVALID_HA_CREDENTIAL")

    def key(self, path):
        s = os.lstat(path)
        return (s.st_dev, s.st_ino)

    def setmeta(self, path, mode=None, uid=0, gid=GID, kind=None, nlink=None):
        data = self.metadata.setdefault(self.key(path), {})
        data.update(uid=uid, gid=gid)
        if mode is not None: data["mode"] = mode
        if kind is not None: data["kind"] = kind
        if nlink is not None: data["nlink"] = nlink

    def info(self, path):
        s = os.lstat(path)
        m = self.metadata.get((s.st_dev, s.st_ino), {})
        return SimpleNamespace(st_dev=s.st_dev, st_ino=s.st_ino,
            st_mode=m.get("kind", stat.S_IFMT(s.st_mode)) | m.get("mode", stat.S_IMODE(s.st_mode)),
            st_uid=m.get("uid", 0), st_gid=m.get("gid", GID), st_nlink=m.get("nlink", s.st_nlink),
            st_size=s.st_size, st_mtime_ns=s.st_mtime_ns, st_ctime_ns=s.st_ctime_ns)

    def handle(self, path, real=None):
        self.counter += 1
        self.handles[self.counter] = [Path(path), real]
        return self.counter

    def open_root(self): return self.handle(self.root)

    def open_dir(self, parent, name):
        path = self.handles[parent][0] / name
        info = self.info(path)
        if not stat.S_ISDIR(info.st_mode): raise OSError("unsafe directory")
        return self.handle(path)

    def open_file(self, parent, name):
        path = self.handles[parent][0] / name
        if not stat.S_ISREG(self.info(path).st_mode): raise OSError("unsafe file")
        return self.handle(path, shared_open(path, os.O_RDONLY | getattr(os, "O_BINARY", 0)))

    def fstat(self, fd): return self.info(self.handles[fd][0])
    def lstat(self, parent, name): return self.info(self.handles[parent][0] / name)

    def read(self, fd, size):
        self.event("read")
        data = os.read(self.handles[fd][1], size)
        return data[:1] if self.short_read else data

    def seek(self, fd): os.lseek(self.handles[fd][1], 0, os.SEEK_SET)

    def close(self, fd):
        path, real = self.handles.pop(fd)
        if real is not None: os.close(real)

    def acl(self, fd, directory=False):
        self.event("acl")
        if self.acl_error: raise P.BoundaryError(self.acl_error)

    def mkdir(self, parent, name):
        self.event("mkdir")
        path = self.handles[parent][0] / name
        path.mkdir()
        self.setmeta(path, mode=0o700, gid=0)

    def ownership(self, fd, gid):
        self.event("ownership")
        path = self.handles[fd][0]
        self.metadata[self.key(path)].update(uid=0, gid=gid)

    def mode(self, fd, mode):
        self.event("mode")
        self.metadata[self.key(self.handles[fd][0])]["mode"] = mode

    def sync(self, fd):
        path, real = self.handles[fd]
        stage = path.name.startswith(".hioc-ha-credential-")
        self.event("fsync_stage" if stage else "fsync_directory")
        if real is not None: os.fsync(real)

    def lock(self, fd): self.event("lock")
    def stage_name(self): return ".hioc-ha-credential-test-only-staging"

    def create_stage(self, parent, name):
        self.event("create_stage")
        path = self.handles[parent][0] / name
        if self.collision:
            path.write_bytes(b"TEST_ONLY_COLLISION_OBJECT")
        fd = shared_open(path, os.O_RDWR | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0), 0o600)
        self.setmeta(path, mode=0o600, gid=0)
        return self.handle(path, fd)

    def write(self, fd, data):
        self.event("write")
        if self.zero_write: return 0
        return os.write(self.handles[fd][1], data[:self.short_write] if self.short_write else data)

    def replace(self, parent, name):
        self.event("interrupt")
        self.event("replace")
        directory = self.handles[parent][0]
        oldpath, newpath = directory / name, directory / P.FINAL_NAME
        if os.name == "nt":
            # NTFS POSIX rename flags keep the old open reader valid, like Linux.
            import ctypes
            from ctypes import wintypes
            import msvcrt
            name = str(newpath)
            class RenameInfo(ctypes.Structure):
                _fields_ = [("Flags",wintypes.DWORD),("RootDirectory",wintypes.HANDLE),("FileNameLength",wintypes.DWORD),("FileName",wintypes.WCHAR*(len(name)+1))]
            info = RenameInfo(3,None,len(name.encode("utf-16-le")),name)
            kernel = ctypes.WinDLL("kernel32",use_last_error=True)
            rename = kernel.SetFileInformationByHandle
            rename.argtypes = [wintypes.HANDLE,ctypes.c_int,wintypes.LPVOID,wintypes.DWORD]
            rename.restype = wintypes.BOOL
            stage = next(h[1] for h in self.handles.values() if h[0] == oldpath and h[1] is not None)
            if not rename(msvcrt.get_osfhandle(stage),22,ctypes.byref(info),ctypes.sizeof(info)):
                raise ctypes.WinError(ctypes.get_last_error())
        else:
            os.replace(oldpath, newpath)
        for handle in self.handles.values():
            if handle[0] == oldpath: handle[0] = newpath
        if self.fault == "final_verify": self.acl_error = "ACL_UNVERIFIABLE"
        if self.fault == "post_replace_fsync": self.fault = "fsync_directory"

    def unlink_stage(self, parent, name):
        self.event("cleanup")
        (self.handles[parent][0] / name).unlink()

    def hierarchy(self):
        for path in (self.root / "etc/hioc", self.root / "etc/hioc/credentials"):
            path.mkdir(exist_ok=True)
            self.setmeta(path, mode=0o750)
        return self.root / "etc/hioc/credentials"

    def credential(self, data=OLD):
        path = self.hierarchy() / P.FINAL_NAME
        path.write_bytes(data)
        self.setmeta(path, mode=0o640)
        return path


class FixtureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="hioc-synthetic-credential-")
        self.fs = FixtureFS(self.temp.name)

    def tearDown(self):
        self.assertEqual(self.fs.handles, {}, "all pinned descriptors must be closed")
        self.temp.cleanup()
        self.assertFalse(Path(self.temp.name).exists())

    def install(self): return P.install(self.fs, GID, lambda: NEW)
    def validate(self): return V.validate(self.fs, GID)

    def test_first_install_and_independent_read(self):
        self.assertEqual(self.install(), "INSTALL")
        final = self.fs.root / "etc/hioc/credentials" / P.FINAL_NAME
        self.assertEqual(final.read_bytes(), NEW.encode() + b"\n")
        self.assertEqual(self.fs.info(final).st_mode, stat.S_IFREG | 0o640)
        self.validate()
        self.assertIn("lock", self.fs.events)
        self.assertGreaterEqual(self.fs.events.count("fsync_stage"), 2)
        self.assertEqual(list(final.parent.iterdir()), [final])

    def test_rotation_no_backup_old_pinned_reader_survives(self):
        final = self.fs.credential()
        old_fd = shared_open(final, os.O_RDONLY | getattr(os, "O_BINARY", 0))
        try:
            self.assertEqual(self.install(), "ROTATE")
            self.assertEqual(final.read_bytes(), NEW.encode() + b"\n")
            if old_fd is not None: self.assertEqual(os.read(old_fd, 4098), OLD)
        finally:
            if old_fd is not None: os.close(old_fd)
        self.assertEqual(list(final.parent.iterdir()), [final])
        self.assertNotIn(OLD, [path.read_bytes() for path in final.parent.iterdir()])

    def test_safe_existing_directories(self):
        self.fs.hierarchy()
        self.assertEqual(self.install(), "INSTALL")
        self.assertNotIn("mkdir", self.fs.events)

    def test_bad_directory_drift_rejected_before_prompt(self):
        for change in ({"uid": 123}, {"gid": 456}, {"mode": 0o770}, {"mode": 0o777}, {"mode": 0o700}, {"kind": stat.S_IFLNK}, {"kind": stat.S_IFREG}):
            with self.subTest(change=change):
                directory = self.fs.hierarchy()
                self.fs.setmeta(directory, mode=0o750, **{k:v for k,v in change.items() if k != "mode"})
                if "mode" in change: self.fs.setmeta(directory, mode=change["mode"])
                with self.assertRaises((P.BoundaryError, OSError)):
                    P.install(self.fs, GID, lambda: self.fail("prompt before failed preflight"))
                self.fs.setmeta(directory, mode=0o750, kind=stat.S_IFDIR)

    def test_ancestor_symlink_and_unsafe_root(self):
        etc = self.fs.root / "etc"
        self.fs.setmeta(etc, mode=0o755, gid=0, kind=stat.S_IFLNK)
        with self.assertRaises(OSError): self.install()
        self.fs.setmeta(etc, mode=0o777, gid=0, kind=stat.S_IFDIR)
        with self.assertRaises(P.BoundaryError): self.install()

    def test_existing_final_object_security_fail_closed(self):
        for change in ({"uid": 123}, {"gid": 456}, {"mode": 0o644}, {"mode": 0o660}, {"mode": 0o600}, {"kind": stat.S_IFLNK}, {"kind": stat.S_IFIFO}, {"kind": stat.S_IFDIR}, {"nlink": 2}):
            with self.subTest(change=change):
                final = self.fs.credential()
                self.fs.setmeta(final, mode=0o640, kind=stat.S_IFREG, nlink=1)
                meta = self.fs.metadata[self.fs.key(final)]; meta.update(change)
                with self.assertRaises(P.BoundaryError) as caught:
                    P.install(self.fs, GID, lambda: self.fail("unsafe existing object prompted"))
                self.assertEqual(caught.exception.code, "EXISTING_CREDENTIAL_INVALID")
                self.assertEqual(final.read_bytes(), OLD)

    def test_real_hardlink_rejected(self):
        final = self.fs.credential()
        os.link(final, final.parent / "test-only-second-link")
        with self.assertRaises(P.BoundaryError): self.install()
        with self.assertRaises(V.BoundaryError): self.validate()

    def test_real_directory_at_final(self):
        directory = self.fs.hierarchy()
        (directory / P.FINAL_NAME).mkdir()
        with self.assertRaises(P.BoundaryError): self.install()
        with self.assertRaises(V.BoundaryError): self.validate()

    def test_bad_existing_content_no_overwrite(self):
        for data in (b"", b"\n", b"TEST ONLY", b"TEST\nONLY\n", b"TEST\r\n", b"TEST\t", b"TEST\x00", b"TEST\xff", b"X" * 4097, b"X" * 4098):
            with self.subTest(data_description=len(data)):
                final = self.fs.credential(data)
                with self.assertRaises(P.BoundaryError): self.install()
                self.assertEqual(final.read_bytes(), data)

    def test_one_read_accepts_required_single_lf(self):
        for data in (b"TEST_ONLY\n", b"X" * 4096 + b"\n"):
            self.fs.credential(data)
            before = self.fs.events.count("read")
            self.validate()
            self.assertEqual(self.fs.events.count("read") - before, 1)

    def test_noncanonical_persisted_content_rejected(self):
        for data in (b"",b"\n",b"TEST_ONLY",b"X"*4096,b"TEST_ONLY\n\n",b"TEST_ONLY\r\n",b"TEST\nONLY\n",b"TEST\rONLY\n",b"TEST ONLY\n",b"TEST\tONLY\n",b"TEST\x00ONLY\n",b"TEST\xffONLY\n",b"X"*4097+b"\n"):
            with self.subTest(description=len(data)):
                self.fs.credential(data)
                with self.assertRaises(V.BoundaryError): self.validate()
                with self.assertRaises(P.BoundaryError): P.content_policy(data)

    def test_missing_final_lf_existing_file_rejected_before_acquisition(self):
        for data in (b"TEST_ONLY",b"X"*4096):
            with self.subTest(description=len(data)):
                final=self.fs.credential(data)
                self.fs.events.clear()
                with self.assertRaises(P.BoundaryError) as caught:
                    P.install(self.fs,GID,lambda:self.fail("invalid existing credential must not prompt"))
                self.assertEqual(caught.exception.code,"EXISTING_CREDENTIAL_INVALID")
                self.assertEqual(final.read_bytes(),data)
                self.assertNotIn("create_stage",self.fs.events)
                self.assertNotIn("replace",self.fs.events)
                self.assertEqual(list(final.parent.iterdir()),[final])

    def test_both_validator_cli_modes_reject_missing_final_lf_readonly(self):
        final=self.fs.credential(b"TEST_ONLY")
        for mode in ("--root","--runtime-operator"):
            output,error=io.StringIO(),io.StringIO()
            self.fs.events.clear()
            with patch.object(V,"identities",return_value=GID),patch.object(V,"NativeFS",return_value=self.fs),contextlib.redirect_stdout(output),contextlib.redirect_stderr(error):
                self.assertEqual(V.main([mode]),1)
            self.assertIn("ERROR_CODE=CONTENT_INVALID",output.getvalue())
            self.assertNotIn("TEST_ONLY",output.getvalue()+error.getvalue())
            self.assertEqual(final.read_bytes(),b"TEST_ONLY")
            self.assertFalse(set(self.fs.events)&{"write","mkdir","replace","cleanup","mode","ownership"})

    def test_short_read_rejected(self):
        self.fs.credential(); self.fs.short_read = True
        with self.assertRaises(V.BoundaryError): self.validate()

    def test_acl_unknown_and_extra_access_fail_before_prompt(self):
        for code in ("ACL_UNVERIFIABLE", "ACL_UNEXPECTED"):
            self.fs.acl_error = code
            with self.assertRaises(P.BoundaryError):
                P.install(self.fs, GID, lambda: self.fail("ACL preflight must precede prompt"))

    def test_complete_short_writes(self):
        self.fs.short_write = 2
        self.assertEqual(self.install(), "INSTALL")
        self.assertGreater(self.fs.events.count("write"), 5)

    def test_zero_write_keeps_old_and_cleans_stage(self):
        final = self.fs.credential(); self.fs.zero_write = True
        with self.assertRaises(P.BoundaryError): self.install()
        self.assertEqual(final.read_bytes(), OLD)
        self.assertEqual(list(final.parent.iterdir()), [final])

    def test_stage_collision_never_deletes_foreign_object(self):
        final = self.fs.credential(); self.fs.collision = True
        with self.assertRaises(FileExistsError): self.install()
        self.assertEqual(final.read_bytes(), OLD)
        collision = final.parent / self.fs.stage_name()
        self.assertEqual(collision.read_bytes(), b"TEST_ONLY_COLLISION_OBJECT")

    def test_pre_replace_faults_preserve_old_cleanup(self):
        for fault in ("create_stage", "write", "fsync_stage", "ownership", "mode", "replace", "interrupt"):
            with self.subTest(fault=fault):
                final = self.fs.credential(); self.fs.fault = fault
                with self.assertRaises((P.BoundaryError,OSError,KeyboardInterrupt)): self.install()
                self.assertEqual(final.read_bytes(), OLD)
                self.assertEqual(list(final.parent.iterdir()), [final])
                self.fs.fault = None

    def test_post_replace_errors_new_authoritative_never_delete_final(self):
        for fault in ("final_verify", "post_replace_fsync"):
            with self.subTest(fault=fault):
                final = self.fs.credential(); self.fs.fault = fault
                with self.assertRaises(P.BoundaryError) as caught: self.install()
                self.assertIn("NEW_AUTHORITATIVE", caught.exception.code)
                self.assertEqual(final.read_bytes(), NEW.encode() + b"\n")
                self.assertEqual(list(final.parent.iterdir()), [final])
                self.fs.fault = self.fs.acl_error = None

    def test_cleanup_failure_bounded_and_never_final_deletion(self):
        final = self.fs.credential(); self.fs.zero_write = True; self.fs.fault = "cleanup"
        with self.assertRaises(P.BoundaryError) as caught: self.install()
        self.assertEqual(str(caught.exception), "STAGING_CLEANUP_UNPROVED")
        self.assertEqual(final.read_bytes(), OLD)
        self.assertTrue((final.parent / self.fs.stage_name()).exists())

    def test_synthetic_deletion_absence_fails_without_mutation(self):
        final = self.fs.credential(); final.unlink()
        with self.assertRaises(FileNotFoundError): self.validate()
        self.assertEqual(list(final.parent.iterdir()), [])


    def test_existing_changes_during_prompt_abort_without_overwrite(self):
        final = self.fs.credential()
        replacement = b"TEST_ONLY_SEPARATE_OPERATOR_CHANGE\n"
        def acquire():
            final.write_bytes(replacement)
            return NEW
        with self.assertRaises(P.BoundaryError) as caught:
            P.install(self.fs,GID,acquire)
        self.assertEqual(caught.exception.code,"EXISTING_CREDENTIAL_CHANGED")
        self.assertEqual(final.read_bytes(),replacement)
        self.assertNotIn("replace",self.fs.events)
        self.assertEqual(list(final.parent.iterdir()),[final])

    def test_name_rebind_and_metadata_change_during_bounded_read(self):
        final = self.fs.credential()
        original_read = self.fs.read
        def read_then_change(fd,size):
            data = original_read(fd,size)
            self.fs.metadata[self.fs.key(final)]["mode"] = 0o644
            return data
        with patch.object(self.fs,"read",side_effect=read_then_change):
            with self.assertRaises(V.BoundaryError) as caught: self.validate()
        self.assertEqual(caught.exception.code,"FILE_CHANGED")
        self.fs.setmeta(final,mode=0o640)
        original_lstat = self.fs.lstat
        calls = 0
        def rebound(parent,name):
            nonlocal calls
            info = original_lstat(parent,name)
            if name == P.FINAL_NAME:
                calls += 1
                if calls > 1: info.st_ino += 1
            return info
        with patch.object(self.fs,"lstat",side_effect=rebound):
            with self.assertRaises(V.BoundaryError) as caught: self.validate()
        self.assertEqual(caught.exception.code,"NAME_BINDING_CHANGED")

    def test_lock_failure_and_initial_directory_fsync_fail_before_prompt(self):
        for fault in ("lock","fsync_directory"):
            self.fs.fault = fault
            with self.assertRaises(OSError):
                P.install(self.fs,GID,lambda:self.fail("failed credential-free preflight prompted"))
            self.assertFalse((self.fs.root/"etc/hioc/credentials"/P.FINAL_NAME).exists())
            self.fs.fault = None

    def test_stage_metadata_and_cleanup_binding_failure_do_not_delete_other_object(self):
        final = self.fs.credential()
        original_write = self.fs.write
        def alter_stage(fd,data):
            original_write(fd,data)
            self.fs.metadata[self.fs.key(self.fs.handles[fd][0])]["uid"] = 123
            return len(data)
        with patch.object(self.fs,"write",side_effect=alter_stage):
            with self.assertRaises(P.BoundaryError) as caught: self.install()
        self.assertEqual(caught.exception.code,"STAGING_CLEANUP_UNPROVED")
        self.assertEqual(final.read_bytes(),OLD)
        self.assertTrue((final.parent/self.fs.stage_name()).exists())

    def test_bad_input_after_preflight_keeps_old_no_staging(self):
        final = self.fs.credential()
        with self.assertRaises(P.BoundaryError):
            P.install(self.fs,GID,lambda:"TEST ONLY INVALID INPUT")
        self.assertEqual(final.read_bytes(),OLD)
        self.assertNotIn("create_stage",self.fs.events)

    def test_exceptions_and_all_fixture_output_contain_no_secret(self):
        output,error=io.StringIO(),io.StringIO()
        with contextlib.redirect_stdout(output),contextlib.redirect_stderr(error):
            self.assertEqual(self.install(),"INSTALL")
            self.validate()
        self.assertEqual(output.getvalue()+error.getvalue(),"")
        for invalid in ("TEST ONLY INVALID INPUT",NEW+"\n"):
            with self.assertRaises(P.BoundaryError) as caught: P.encode_input(invalid)
            self.assertNotIn(invalid,str(caught.exception))


class PolicyTests(unittest.TestCase):
    def test_input_policy_and_maximum(self):
        self.assertEqual(P.encode_input("X" * 4096), b"X" * 4096 + b"\n")
        for value in ("", "X" * 4097, "TEST ONLY", "TEST\tONLY", "TEST\r", "TEST\n", "TEST\x00", "TESTé"):
            with self.subTest(description=len(value)):
                with self.assertRaises(P.BoundaryError): P.encode_input(value)
        for data in (b"TEST_ONLY\n\n", b"TEST_ONLY ", b" TEST_ONLY", b"TEST_ONLY\r\n"):
            with self.assertRaises(P.BoundaryError): P.content_policy(data)

    def accounts(self, primary=True, supplemental=()):
        root = SimpleNamespace(pw_name="root", pw_uid=0, pw_gid=0)
        user = SimpleNamespace(pw_name="jazofv1", pw_uid=1000, pw_gid=GID if primary else 1000)
        group = SimpleNamespace(gr_name="jazofv1", gr_gid=GID, gr_mem=list(supplemental))
        return [root, user], [group], user, group

    def test_primary_supplemental_and_root_readers(self):
        for primary, supplementary in ((True, ()), (False, ("jazofv1",)), (True, ("root",))):
            self.assertEqual(P.effective_readers(*self.accounts(primary, supplementary)), GID)

    def test_unexpected_primary_and_supplemental_readers(self):
        for primary in (True, False):
            users, groups, user, group = self.accounts()
            users.append(SimpleNamespace(pw_name="test-only-other", pw_uid=2000, pw_gid=GID if primary else 2000))
            if not primary: group.gr_mem.append("test-only-other")
            with self.assertRaises(P.BoundaryError): P.effective_readers(users, groups, user, group)

    def test_duplicate_missing_and_inconsistent_accounts(self):
        for change in ("duplicate_user", "duplicate_uid", "duplicate_group", "duplicate_gid", "missing_member", "duplicate_member", "nonmember", "missing_user"):
            users, groups, user, group = self.accounts()
            if change == "duplicate_user": users.append(user)
            if change == "duplicate_uid": users.append(SimpleNamespace(pw_name="alias", pw_uid=1000, pw_gid=0))
            if change == "duplicate_group": groups.append(group)
            if change == "duplicate_gid": groups.append(SimpleNamespace(gr_name="alias", gr_gid=GID, gr_mem=[]))
            if change == "missing_member": group.gr_mem.append("missing")
            if change == "duplicate_member": group.gr_mem.extend(["jazofv1", "jazofv1"])
            if change == "nonmember": user.pw_gid = 1000
            if change == "missing_user": users.remove(user)
            with self.subTest(change=change):
                with self.assertRaises(P.BoundaryError): P.effective_readers(users, groups, user, group)

    def test_linux_and_privilege_gate_without_host_access(self):
        with patch.object(P.sys, "platform", "win32"):
            with self.assertRaises(P.BoundaryError) as caught: P.identities("root")
            self.assertEqual(caught.exception.code, "LINUX_REQUIRED")
        users, groups, user, group = self.accounts()
        pwd = SimpleNamespace(getpwnam=lambda n: user if n == "jazofv1" else users[0], getpwuid=lambda n: users[0] if n == 0 else user, getpwall=lambda: users)
        grp = SimpleNamespace(getgrnam=lambda n: group, getgrall=lambda: groups, getgrgid=lambda n: group)
        with patch.dict("sys.modules", {"pwd":pwd, "grp":grp}), patch.object(P.sys,"platform","linux"), patch.object(P.os,"uname",create=True,return_value=SimpleNamespace(nodename=P.HOST)), patch.object(P.os,"geteuid",create=True,return_value=1000), patch.object(P.os,"getuid",create=True,return_value=1000), patch.object(P.os,"getegid",create=True,return_value=GID), patch.object(P.os,"getgroups",create=True,return_value=[GID]):
            with self.assertRaises(P.BoundaryError) as caught: P.identities("root")
            self.assertEqual(caught.exception.code, "ROOT_REQUIRED")
            self.assertEqual(P.identities("operator"), GID)
            with patch.object(P.os,"geteuid",return_value=0), patch.object(P.os,"getuid",return_value=0):
                self.assertEqual(P.identities("root"), GID)
            with patch.object(pwd,"getpwnam",side_effect=KeyError("test-only-error")):
                with self.assertRaises(P.BoundaryError): P.identities("root")

    def test_exact_linux_open_flags_and_exclusive_staging(self):
        constants={"O_DIRECTORY":0x10000,"O_NOFOLLOW":0x20000,"O_CLOEXEC":0x40000,"O_NONBLOCK":0x80000}
        with patch.multiple(P.os,create=True,**constants),patch.object(P.os,"open",return_value=999) as opened:
            P.NativeFS().open_dir(123,"credentials")
            self.assertEqual(opened.call_args.kwargs,{"dir_fd":123})
            self.assertEqual(opened.call_args.args[1] & (constants["O_NOFOLLOW"]|constants["O_DIRECTORY"]),constants["O_NOFOLLOW"]|constants["O_DIRECTORY"])
            P.NativeFS().open_file(123,P.FINAL_NAME)
            self.assertTrue(opened.call_args.args[1] & constants["O_NONBLOCK"])
            self.assertTrue(opened.call_args.args[1] & constants["O_NOFOLLOW"])
            P.ProvisionFS().create_stage(123,".hioc-ha-credential-test-only")
            flags=opened.call_args.args[1]
            self.assertEqual(flags & (os.O_CREAT|os.O_EXCL|constants["O_NOFOLLOW"]),os.O_CREAT|os.O_EXCL|constants["O_NOFOLLOW"])
            self.assertEqual(opened.call_args.args[2],0o600)

    def test_root_validator_does_not_claim_actual_operator_read(self):
        output=io.StringIO()
        with patch.object(V,"identities",return_value=GID),patch.object(V,"validate"),contextlib.redirect_stdout(output):
            self.assertEqual(V.main(["--root"]),0)
        self.assertIn("CREDENTIAL_READABLE_BY_RUNTIME_OPERATOR=NOT_TESTED",output.getvalue())
        self.assertNotIn("CREDENTIAL_READABLE_BY_RUNTIME_OPERATOR=TRUE",output.getvalue())

    def test_kernel_acl_absent_base_extended_unknown_and_default(self):
        native = P.NativeFS()
        base = struct.pack("<I",2) + b"".join(struct.pack("<HHI",tag,perm,0xffffffff) for tag,perm in ((1,6),(4,4),(32,0)))
        with patch.object(P.os,"getxattr",create=True,side_effect=OSError(errno.ENODATA,"test-only")):
            native.acl(999,True)
        with patch.object(native,"fstat",return_value=SimpleNamespace(st_mode=stat.S_IFREG|0o640)), patch.object(P.os,"getxattr",create=True,return_value=base):
            native.acl(999)
            with self.assertRaises(P.BoundaryError): native.acl(999,True)
        for raw in (base + struct.pack("<HHI",2,4,2000), b"malformed", base.replace(struct.pack("<HHI",4,4,0xffffffff),struct.pack("<HHI",4,6,0xffffffff))):
            with patch.object(native,"fstat",return_value=SimpleNamespace(st_mode=stat.S_IFREG|0o640)), patch.object(P.os,"getxattr",create=True,return_value=raw):
                with self.assertRaises(P.BoundaryError): native.acl(999)
        for error in (errno.EOPNOTSUPP, errno.EACCES, errno.EIO):
            with patch.object(P.os,"getxattr",create=True,side_effect=OSError(error,"test-only")):
                with self.assertRaises(P.BoundaryError) as caught: native.acl(999)
                self.assertEqual(caught.exception.code,"ACL_UNVERIFIABLE")

    def test_cli_rejects_any_secret_path_delete_arguments_without_echo(self):
        for module, args in ((P,["--token",NEW]), (P,["delete"]), (P,["--path","test-only"]), (V,["--token",NEW]), (V,["--path","test-only"]), (V,[])):
            output, error = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
                self.assertEqual(module.main(args),1)
            self.assertNotIn(NEW,output.getvalue()+error.getvalue())
            self.assertNotIn("Traceback",output.getvalue()+error.getvalue())
            self.assertIn("ERROR_CODE=ARGUMENTS_INVALID",output.getvalue())

    def test_cli_success_and_raw_failure_are_redacted(self):
        for module, args, function, result in ((P,[],"install","INSTALL"),(V,["--runtime-operator"],"validate",None)):
            for fail in (False,True):
                output, error = io.StringIO(),io.StringIO()
                with patch.object(module,"identities",return_value=GID), patch.object(module,function,side_effect=RuntimeError(NEW) if fail else None,return_value=result), contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
                    self.assertEqual(module.main(args),int(fail))
                text=output.getvalue()+error.getvalue()
                self.assertNotIn(NEW,text); self.assertNotIn("HASH",text)
                self.assertNotIn("Traceback",text)
                self.assertIn("CREDENTIAL_VALUE_EXPOSED=FALSE",text)
                self.assertIn("NETWORK_CONNECTION_ATTEMPTED=FALSE",text)

    @patch.object(P.os,"O_NOCTTY",0,create=True)
    @patch.object(P.os,"O_CLOEXEC",0,create=True)
    def test_hidden_prompt_once_no_fallback(self):
        fake_stream = io.StringIO()
        with patch.object(P.os,"open",return_value=999), patch.object(P.os,"dup",return_value=1000), patch.object(P.os,"close"), patch.object(P.os,"isatty",return_value=True), patch.object(P.os,"fdopen",return_value=fake_stream), patch.object(P.sys.stdin,"isatty",return_value=True), patch.object(P.sys.stderr,"isatty",return_value=True), patch("getpass.getpass",return_value=NEW) as prompt:
            self.assertEqual(P.hidden_input(),NEW)
            prompt.assert_called_once()
            self.assertEqual(prompt.call_args.args[0],"Home Assistant runtime access token:")
        import getpass
        fake_stream = io.StringIO()
        with patch.object(P.os,"open",return_value=999), patch.object(P.os,"dup",return_value=1000), patch.object(P.os,"close"), patch.object(P.os,"isatty",return_value=True), patch.object(P.os,"fdopen",return_value=fake_stream), patch.object(P.sys.stdin,"isatty",return_value=True), patch.object(P.sys.stderr,"isatty",return_value=True), patch("getpass.getpass",side_effect=getpass.GetPassWarning("test-only")):
            with self.assertRaises(getpass.GetPassWarning): P.hidden_input()
        with patch.object(P.os,"open",return_value=999), patch.object(P.os,"close"), patch.object(P.os,"isatty",return_value=False), patch("getpass.getpass") as prompt:
            with self.assertRaises(P.BoundaryError): P.hidden_input()
            prompt.assert_not_called()


class GovernanceTests(unittest.TestCase):
    def record(self): return json.loads(RECORD_PATH.read_text(encoding="utf-8"))

    def test_closed_canonical_record(self):
        record=self.record(); schema=json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        for path in (RECORD_PATH,SCHEMA_PATH):
            text=path.read_text(encoding="utf-8")
            self.assertEqual(text,json.dumps(json.loads(text),sort_keys=True,separators=(",",":"))+"\n")
        validate_schema(record,schema)
        for change in ({"credential_provisioned":True},{"token":NEW},{"parent_checkpoint_status":"PASS_CLOSED"}):
            value=copy.deepcopy(record); value.update(change)
            with self.assertRaises(ValueError): validate_schema(value,schema)
        for key in record:
            value=copy.deepcopy(record); del value[key]
            with self.assertRaises(ValueError): validate_schema(value,schema)
        self.assertEqual(record["baseline_commit"],BASE)
        self.assertEqual(record["pre_execution_correction"]["starting_commit"],"afa484620d24a1d6dec2a98e7c06e613f633bfb7")
        self.assertTrue(record["pre_execution_correction"]["before_operator_execution"])
        self.assertEqual(record["content_policy"]["read_normalization"],"REQUIRE_AND_REMOVE_EXACTLY_ONE_FINAL_LF_NO_TRIM")
        self.assertEqual(record["independent_validation"]["normalization"],"REQUIRE_EXACTLY_ONE_FINAL_LF_NO_GENERIC_TRIM")
        self.assertEqual(record["next_checkpoint"],NEXT)
        self.assertEqual(record["credential_path"],P.CREDENTIAL_PATH)
        self.assertEqual((record["credential_owner"],record["credential_group"],record["credential_mode"],record["directory_mode"]),("root","jazofv1","0640","0750"))

    def test_bound_tool_sources(self):
        for binding in self.record()["tools"].values():
            path=ROOT/binding["path"]
            source=path.read_bytes()
            self.assertEqual(hashlib.sha256(source).hexdigest(),binding["sha256"])
            blob=subprocess.check_output(["git","hash-object","--path="+binding["path"],binding["path"]],cwd=ROOT).decode().strip()
            self.assertEqual(blob,binding["git_blob"])
            compile(source,str(path),"exec")

    def test_static_privacy_readonly_validator_and_no_network(self):
        prohibited={"requests","websockets","socket","urllib","http","subprocess","hashlib","logging","hioc"}
        for name in ("provision","validate"):
            source=(ROOT/f"tools/hioc-pe4-ha-runtime-credential-{name}.py").read_text(encoding="utf-8")
            tree=ast.parse(source)
            imports={alias.name.split(".")[0] for node in ast.walk(tree) if isinstance(node,(ast.Import,ast.ImportFrom)) for alias in (node.names if isinstance(node,ast.Import) else [SimpleNamespace(name=node.module or "")])}
            self.assertFalse(imports & prohibited)
            for value in ("--token","os.environ","getenv(","curl","mqtt","state/",".bak","sha256","delete"):
                self.assertNotIn(value,source)
            for node in ast.walk(tree):
                if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=="print":
                    printed={n.id for n in ast.walk(node) if isinstance(n,ast.Name)}
                    self.assertFalse(printed & {"value","data","encoded","exc"})
            if name=="validate":
                for value in ("os.write(","os.mkdir(","os.replace(","os.unlink(","os.fchmod(","os.fchown(","O_CREAT","getpass"):
                    self.assertNotIn(value,source)
        # Shared security code is intentionally identical, with independent entrypoints.
        a=(ROOT/"tools/hioc-pe4-ha-runtime-credential-provision.py").read_text().split("class ProvisionFS",1)[0]
        b=(ROOT/"tools/hioc-pe4-ha-runtime-credential-validate.py").read_text().split("def validate(fs",1)[0]
        self.assertEqual(a.strip(),b.strip())

    def test_release_ownership_and_protected_baseline(self):
        protected=["release/install.sh","release/upgrade.sh","release/rollback.sh","release/build.sh","pi4/install_pi4.sh","pi4/uninstall_pi4.sh","homeassistant/install_ha.sh","docs/DATA_MODEL.md","tools/hioc-pe4-ha-auth-capability.py","tools/hioc-pe4-ha-registry-discovery.py","pi4/lib/hioc/inventory.py","pi4/bin/hioc-inventory-engine.py","pi4/lib/hioc/core/state.py","pi4/lib/hioc/core/compatibility.py","governance/pe4/pe4-ha-association-adapter-implementation-preparation.json","docs/PE4_HOME_ASSISTANT_ASSOCIATION_ADAPTER_IMPLEMENTATION_PREPARATION.md"]
        for path in protected:
            before=subprocess.check_output(["git","show",BASE+":"+path],cwd=ROOT)
            after=(ROOT/path).read_text(encoding="utf-8").encode()
            if path in {"docs/DATA_MODEL.md","pi4/bin/hioc-inventory-engine.py"}:
                implementation=json.loads((ROOT/"governance/pe4/pe4-ha-association-public-projection-implementation.json").read_bytes())
                self.assertEqual(before,subprocess.check_output(["git","show",implementation['starting_commit']+":"+path],cwd=ROOT),path)
                bound=next(i for i in implementation['implementation_artifacts'] if i['path']==path)
                self.assertEqual(hashlib.sha256(after).hexdigest(),bound['sha256'],path)
            else:self.assertEqual(before,after,path)
            if path.endswith(".sh"):
                self.assertNotIn(b"/etc/hioc",after)
                self.assertNotIn(b"home_assistant.token",after)
        self.assertIn('INSTALL_DIR="${HIOC_INSTALL_DIR:-/home/jazofv1/hioc}"',(ROOT/"release/upgrade.sh").read_text())
        self.assertIn('"$INSTALL_DIR/" "$BACKUP_DIR/current/"',(ROOT/"release/upgrade.sh").read_text())
        for path in ("pi4/lib/hioc/home_assistant_association.py","pi4/bin/hioc-home-assistant-association.py"):
            self.assertEqual(subprocess.check_output(["git","ls-tree","-r","--name-only",BASE,"--",path],cwd=ROOT),b"")
            implementation=json.loads((ROOT/"governance/pe4/pe4-ha-association-runtime-validation-correction.json").read_bytes())
            binding=next(v for v in implementation["sources"].values() if v["path"]==path)
            self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),binding["sha256"])

    def test_lifecycle_links_and_unrelated_roadmap_preserved(self):
        text=subprocess.check_output(['git','show','c762745b428b28518cf4415f7399ff2cacb70c66:docs/HIOC_MASTER_PLAN.md'],cwd=ROOT).decode('utf8')
        current=text.split("# Implementation Status",1)[1].split("# Historical Operator Preparation Chronology",1)[0]
        for row in ("| PE-4 Home Assistant Runtime Credential Provisioning Preparation | PASS/CLOSED |","| PE-4 Home Assistant Runtime Credential Provisioning | PASS/CLOSED |","| Operator Credential Installation | PASS/CLOSED |","| Independent Credential Validation | PASS/CLOSED |","| Credential Provisioning Governance Closure | PASS/CLOSED |","| PE-4 Home Assistant Association Adapter Implementation | PASS/CLOSED, corrected before deployment |","| PE-4 | NOT COMPLETE |","| Phase 7A | ACTIVE |","| Rollback | NOT PERFORMED |"):
            self.assertIn(row,current)
        self.assertTrue(current.split("## Next Planned Task",1)[1].strip().startswith("### PE-4 Home Assistant Association Public Projection"))
        before=subprocess.check_output(["git","show",BASE+":docs/HIOC_MASTER_PLAN.md"],cwd=ROOT).decode("utf-8")
        for start,end in (("## Future Enhancements","# Repository Rules"),("### Future Compatibility Diagnostics UX Checkpoint","# Historical Operator Preparation Chronology"),("# Historical Operator Preparation Chronology",None)):
            previous=before.split(start,1)[1]; now=text.split(start,1)[1]
            if end: previous=previous.split(end,1)[0]; now=now.split(end,1)[0]
            if start == "## Future Enhancements":
                previous = previous.replace("Runtime Credential Provisioning NOT STARTED; adapter implementation NOT STARTED; PE-4 NOT COMPLETE.", "Runtime Credential Provisioning Preparation PASS/CLOSED; Runtime Credential Provisioning PASS/CLOSED; Operator Installation, Independent Validation and Governance Closure PASS/CLOSED based on operator-supplied PI3 evidence; adapter implementation NOT STARTED; PE-4 NOT COMPLETE.", 1)
            if start=="## Future Enhancements": previous=previous.replace("adapter implementation NOT STARTED; PE-4 NOT COMPLETE.","adapter implementation PASS/CLOSED (repository/synthetic only); deployment and scheduler NOT STARTED; PE-4 NOT COMPLETE.",1)
            self.assertEqual(previous,now)
        import re
        doc=ROOT/"docs/PE4_HOME_ASSISTANT_RUNTIME_CREDENTIAL_PROVISIONING.md"
        for target in re.findall(r"\]\(([^)]+)\)",doc.read_text(encoding="utf-8")):
            if "://" not in target and not target.startswith("#"):
                self.assertTrue((doc.parent/target.split("#")[0]).resolve().exists(),target)


if __name__ == "__main__":
    unittest.main()
