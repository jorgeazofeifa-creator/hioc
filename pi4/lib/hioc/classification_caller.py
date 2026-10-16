"""Explicit offline PE-6 snapshot caller. No producer, persistence, publication or recovery."""
import hashlib
import os
from pathlib import Path
import stat
from datetime import datetime, timezone

from . import classification as model
from . import configured_association as pe5
from .configured_association_store import Store, PosixFS, fingerprint
from .assets import AssetLock, AssetError


class WindowsReadFS:
    """Read-only Windows fixture/runtime seam; reject links and reparse-point ancestry."""
    @staticmethod
    def fingerprint(info):
        # Windows st_ctime is deprecated and can mean creation time for path stat
        # but change time for fstat. Compare explicit birthtime consistently.
        # mtime/size, identity, attributes and the content digest/recheck still
        # detect changes; POSIX retains its stronger native ctime fingerprint.
        birth = getattr(info, "st_birthtime_ns", None)
        if type(birth) is not int or not info.st_ino:
            model.fail("INVALID")
        return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, birth,
                info.st_mode, info.st_uid, info.st_gid, info.st_nlink,
                getattr(info, "st_file_attributes", 0), getattr(info, "st_reparse_tag", 0))
    def directory(self, path):
        path = Path(path)
        if not path.is_absolute() or ".." in path.parts:
            model.fail("INVALID")
        for parent in reversed((path, *path.parents)):
            info = parent.lstat()
            if not stat.S_ISDIR(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
                model.fail("INVALID")
        return path
    def statdir(self, path): return path.lstat()
    def close_dir(self, path): pass
    def statat(self, path, name): return (path/name).lstat()
    def openat(self, path, name, flags): return os.open(path/name, flags | os.O_BINARY)
    def fstat(self, fd): return os.fstat(fd)


class Reader:
    """Descriptor-relative no-follow POSIX reads, stable parent/file rechecks, no writes."""
    def __init__(self, fs=None):
        self.fs = fs if fs is not None else PosixFS() if os.name == "posix" else WindowsReadFS()
        self.captured = {}

    def _fingerprint(self, info):
        return self.fs.fingerprint(info) if isinstance(self.fs, WindowsReadFS) else fingerprint(info)

    def _safe(self, info, private, directory=False):
        if not (stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode)):
            model.fail("INVALID")
        if getattr(info, "st_file_attributes", 0) & 0x400 or not directory and info.st_nlink != 1:
            model.fail("INVALID")
        if os.name == "posix":
            mode = stat.S_IMODE(info.st_mode)
            if info.st_uid != os.getuid() or mode & 0o022 or private and not directory and mode != 0o600:
                model.fail("INVALID")

    def read(self, path, private=True):
        path = Path(path)
        if not path.is_absolute() or ".." in path.parts:
            model.fail("INVALID")
        directory = self.fs.directory(path.parent)
        fd = None
        try:
            parent = self.fs.statdir(directory)
            self._safe(parent, private, True)
            first = self.fs.statat(directory, path.name)
            self._safe(first, private)
            if first.st_size > model.LIMIT:
                model.fail("LIMIT_EXCEEDED")
            fd = self.fs.openat(directory, path.name, os.O_RDONLY)
            opened = self.fs.fstat(fd); self._safe(opened, private)
            if self._fingerprint(first) != self._fingerprint(opened):
                model.fail("CHANGED")
            chunks, count = [], 0
            while True:
                part = os.read(fd, min(65536, model.LIMIT+1-count))
                if not part:
                    break
                chunks.append(part); count += len(part)
                if count > model.LIMIT:
                    model.fail("LIMIT_EXCEEDED")
            data = b"".join(chunks)
            if self._fingerprint(opened) != self._fingerprint(self.fs.fstat(fd)) or self._fingerprint(opened) != self._fingerprint(self.fs.statat(directory, path.name)):
                model.fail("CHANGED")
            visible = self.fs.directory(path.parent)
            try:
                if self._fingerprint(parent) != self._fingerprint(self.fs.statdir(visible)):
                    model.fail("CHANGED")
            finally:
                self.fs.close_dir(visible)
            token = (self._fingerprint(parent), self._fingerprint(opened), hashlib.sha256(data).hexdigest())
            return model.snapshot(pe5.strict_json(data, model.LIMIT), raw=data), token
        finally:
            if fd is not None:
                os.close(fd)
            self.fs.close_dir(directory)

    def capture(self, kind, path, private=True):
        if path is None:
            return model.snapshot()
        try:
            result, token = self.read(path, private)
        except FileNotFoundError:
            self.captured[kind] = (Path(path), private, None)
            return model.snapshot()
        self.captured[kind] = (Path(path), private, token)
        return result

    def recheck(self):
        for path, private, original in self.captured.values():
            try:
                unused, token = self.read(path, private)
            except FileNotFoundError:
                token = None
            if token != original:
                model.fail("CHANGED")


def _clock():
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def _pe5(store, at):
    # Each lock is released before the next is acquired. Never invoke composer/recovery.
    output = store.read_handoff(at)
    with store.lock():
        current, unused, unused_snapshot = store.confirmed("GENERATED_RELATIONSHIP_OUTPUT")
        if current != output:
            model.fail("CHANGED")
        source, error = None, None
        if output["configured"]["state"] == "VALID":
            source, unused, unused_snapshot = store.confirmed("CONFIGURED_MAPPING_SOURCE")
    return model.snapshot(dict(output=output, source=source, output_confirmation="CONFIRMED",
                               source_confirmation="CONFIRMED" if source is not None else None))


def evaluate(paths, policy=None, asset_lock=None, use_pe5=False, reader=None,
             clock=_clock, store_factory=Store, lock_factory=AssetLock,
             manufacturer_database=None, manufacturer_manifest=None, approved_manufacturer_manifest_sha256=None):
    """Explicit inputs only. Returns private data to an in-process caller, never saves it."""
    if set(paths) - set(model.KINDS[:-1]):
        model.fail("INVALID")
    reader = reader if reader is not None else Reader()
    captured = {}
    policy = dict(model.POLICY if policy is None else policy)
    if manufacturer_database is not None or manufacturer_manifest is not None:
        try:
            policy["manufacturer_dataset"] = dict(database=reader.capture("manufacturer_database", manufacturer_database), manifest=reader.capture("manufacturer_manifest", manufacturer_manifest), approved_manifest_sha256=approved_manufacturer_manifest_sha256)
        except (OSError, ValueError):
            policy["manufacturer_dataset"] = None
    for kind in model.KINDS[:-1]:
        try:
            if kind == "assets" and paths.get(kind) is not None:
                # Match the operator-established Asset writer lock; never initialize it.
                if asset_lock is None or not Path(asset_lock).is_file() or Path(asset_lock).is_symlink():
                    model.fail("UNAVAILABLE")
                with lock_factory(Path(asset_lock), shared=True):
                    captured[kind] = reader.capture(kind, paths.get(kind))
            else:
                captured[kind] = reader.capture(kind, paths.get(kind), private=kind != "inventory")
        except (OSError, ValueError, AssetError):
            captured[kind] = model.snapshot(state="UNAVAILABLE")
    at = clock()
    store = None
    if use_pe5:
        try:
            store = store_factory()
            captured["pe5_handoff"] = _pe5(store, at)
        except (OSError, ValueError, AssetError):
            captured["pe5_handoff"] = model.snapshot(state="UNAVAILABLE")
    result = model.resolve_classification(captured, at, policy)
    # Reacquire separately, then release, before any PE-5 recheck.
    if paths.get("assets") is not None and captured["assets"]["state"] == "VALID":
        try:
            with lock_factory(Path(asset_lock), shared=True):
                reader.recheck()
        except AssetError:
            model.fail("UNAVAILABLE")
    else:
        reader.recheck()
    used_at = clock()
    if store is not None and captured["pe5_handoff"]["state"] == "VALID":
        if model.canonical(_pe5(store, used_at)) != model.canonical(captured["pe5_handoff"]):
            model.fail("CHANGED")
    model.validate_classification_result(result, captured, used_at, policy)
    return result
