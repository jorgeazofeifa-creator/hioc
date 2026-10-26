#!/usr/bin/env python3
"""PE-7.3 bounded PI3 delivery candidate; native publication is fail-closed.

No production consumer-coverage proof exists yet. Native commit/rollback refuse
before live mutation. The transaction core is exercised only with explicit
synthetic external consumer fencing. No evidence JSON or boolean can unlock it.
"""
from __future__ import annotations
import argparse
import contextlib
import errno
import ctypes
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import socket
import stat
import sys
import subprocess

RELEASE = "51398bab4e2293b578b2cdac2d0740c3738cab2f"
# Repository ancestry is source integrity only, never tooling or mutation approval.
SOURCE = Path("/home/jazofv1/hioc-release-source")
HOME = Path("/home/jazofv1/hioc")
TX = "backups/pe73-pi3-delivery-v1"
LIMIT = 2 * 1024 * 1024
MANIFEST = [
    {
        "path": "pi4/bin/hioc-assets.py",
        "sha256": "43d84f837243606ee58fb64f3febbc28f7766d05378045b42213c7adf48127ab",
        "git_blob": "0b4d8bfdbf432dbed6ef62add9da73c74764c574"
    },
    {
        "path": "pi4/bin/hioc-availability-adapter.py",
        "sha256": "d53114faf5d3cddf6666716871f3f5b51a3876ea7db68b6ce0ab1379b0334ed7",
        "git_blob": "d81c5c7add4a682664897c99574ad2fa05d04bfa"
    },
    {
        "path": "pi4/bin/hioc-incident-engine-v2.py",
        "sha256": "6e9ec9d591ae2e48d19825c095aceb54542405329c842e271a367094475ffffe",
        "git_blob": "f1a2423919edd609a79e8bbf4dfd574c98fee30e"
    },
    {
        "path": "pi4/lib/hioc/asset_policy.py",
        "sha256": "565e2314c8947a17e31e327b21960db4338e37f514ab7c3df31738006d178a2f",
        "git_blob": "917f23cc41487da7a68c2427b3af605e885616e2"
    },
    {
        "path": "pi4/lib/hioc/assets.py",
        "sha256": "5a06d401c7496871c878337a32ec85a37dae53ba7e74fe97e30446f4d720f3ac",
        "git_blob": "132c572d875d8b87ae0d89b72eec2c69ddd1b57b"
    },
    {
        "path": "pi4/lib/hioc/availability.py",
        "sha256": "8b10bf0ced9e280a0d634fe4ec0082d6f267c1a5fd8c8abcae34e5660b2ba54d",
        "git_blob": "c56a2c29fa712609adc9121d48c1639b69b818ba"
    },
    {
        "path": "pi4/lib/hioc/availability_contract.py",
        "sha256": "b27f422e6badd13aefff5f75c1dfd03859f60b927be02721c95e56f18b4eaef3",
        "git_blob": "1479d5c553608b6ceafc14e9553c7aa8f8839de1"
    },
    {
        "path": "pi4/lib/hioc/availability_incidents.py",
        "sha256": "f3d700b10b1de607dd32a36603bd6399a956450fa0a0eb75def4491567a39f5f",
        "git_blob": "d765e77eb9b8442db97c0435f72a0ffe00142584"
    },
    {
        "path": "pi4/lib/hioc/availability_observation.py",
        "sha256": "16722847de9d0a44097d82fffa1056a94efefb9b3eeac3e955336574db324ac0",
        "git_blob": "6fe80ab1ea94a458db723c7ceabd4355fe07b8f0"
    },
    {
        "path": "pi4/lib/hioc/availability_protocol.py",
        "sha256": "3245db6e1e05cd247095031d516d376298dbab8c33e6668548b5e0321350472b",
        "git_blob": "b0398c151bec35671b76cc4f9cd343e59efe9557"
    },
    {
        "path": "pi4/lib/hioc/availability_server.py",
        "sha256": "406cb71e787eafee6c1c780f70167449a9196eacdfe8222fa1cce66312952ab2",
        "git_blob": "efe0aa0da94f8fbce9b62395b28673dbde1dada4"
    },
    {
        "path": "pi4/lib/hioc/classification.py",
        "sha256": "003ccb0eaead3476b85b8e2458d39199a84b439006f165f3fec8341c41a6eaa1",
        "git_blob": "c69c533e46a352dd498813c50fa680cfb57db84f"
    },
    {
        "path": "pi4/lib/hioc/mqtt.py",
        "sha256": "126cfcc6c6780be79e8ed6c1ce7b27f4088edfde7221794ced62bf31e24095d4",
        "git_blob": "369a0efbbebea9d24ed571fe9210562feaddb464"
    }
]
PRIOR = {
    "pi4/bin/hioc-incident-engine-v2.py": ("79f07e0eda4b31242512b7d8a6713a86f62afb4bb08ebd438adbacc9c07cb140", 0o755),
    "pi4/bin/hioc-assets.py": ("8fbe4c6f58ffb431bb51cbfd47245f60266b3ccb29d93e68177223ed6d3c722d", 0o700),
    "pi4/lib/hioc/assets.py": ("9079c976e633d6d1f1c11bf051fc24ea5746500267f0fdfaf9ae1c5c8aea35c9", 0o600),
    "pi4/lib/hioc/classification.py": ("feda2fc41c374d84728e1601b616875cda8289f489fbd903c107409a8fa5a2f6", 0o600),
    "pi4/lib/hioc/mqtt.py": ("d55a174bec05cf009038bbd15ac911dd18039bddc56da1c9847b67bc81c65ff5", 0o644),
}
# Private Python modules follow PE-6 disabled installation (0600); the explicit
# operator entry follows the observed private Asset CLI policy (0700), not Git.
MODES = {x["path"]: PRIOR[x["path"]][1] if x["path"] in PRIOR else
         0o700 if x["path"].startswith("pi4/bin/") else 0o600 for x in MANIFEST}
# Dependencies first, Asset compatibility before classification/CLI, engine LAST.
ORDER = [
    "pi4/lib/hioc/availability_contract.py", "pi4/lib/hioc/availability.py",
    "pi4/lib/hioc/availability_incidents.py", "pi4/lib/hioc/availability_observation.py",
    "pi4/lib/hioc/availability_protocol.py", "pi4/lib/hioc/availability_server.py",
    "pi4/lib/hioc/asset_policy.py", "pi4/lib/hioc/assets.py", "pi4/lib/hioc/mqtt.py",
    "pi4/lib/hioc/classification.py", "pi4/bin/hioc-assets.py",
    "pi4/bin/hioc-availability-adapter.py", "pi4/bin/hioc-incident-engine-v2.py",
]
CRON = (
    "*/1 * * * * flock -n /tmp/hioc-incident-engine.lock /home/jazofv1/hioc/pi4/bin/hioc-incident-engine-v2.py",
    "*/30 * * * * flock -n /tmp/hioc-inventory-engine.lock /home/jazofv1/hioc/pi4/bin/hioc-inventory-engine.py",
    "17 3 * * * flock -n /tmp/hioc-platform-status.lock /home/jazofv1/hioc/pi4/bin/hioc-platform-status.py",
)
AUTH = re.compile(r"[A-Za-z0-9_-]{8,96}\Z")
DIGEST = re.compile(r"[0-9a-f]{64}\Z")

class Failure(ValueError):
    def __init__(self, code):
        self.code = code
        super().__init__(code)

def require(value, code):
    if not value:
        raise Failure(code)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode("ascii")

def parsed(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "JOURNAL_INVALID")
            result[key] = value
        return result
    try:
        require(raw is not None and len(raw) <= LIMIT, "JOURNAL_INVALID")
        value = json.loads(raw, object_pairs_hook=pairs)
        require(type(value) is dict and canonical(value) == raw, "JOURNAL_INVALID")
        return value
    except (UnicodeError, TypeError, json.JSONDecodeError):
        raise Failure("JOURNAL_INVALID") from None

def anchored(info):
    kind = "DIRECTORY" if stat.S_ISDIR(info.st_mode) else "REGULAR" if stat.S_ISREG(info.st_mode) else "UNSAFE"
    return {k: getattr(info, k) for k in ("st_dev", "st_ino", "st_uid", "st_gid")} | {"mode": stat.S_IMODE(info.st_mode), "type": kind}

def identity(info):
    return anchored(info) | {k: getattr(info, k) for k in ("st_nlink", "st_size", "st_mtime_ns", "st_ctime_ns")}

def source_gate(root=SOURCE):
    def git(*args, error="SOURCE_INVALID"):
        result = subprocess.run(["/usr/bin/git", "--no-optional-locks", "--no-replace-objects", *args],
            cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20,
            env={"PATH": "/usr/bin:/bin", "HOME": "/home/jazofv1", "LANG": "C.UTF-8",
                 "LC_ALL": "C.UTF-8", "GIT_OPTIONAL_LOCKS": "0"})
        require(result.returncode == 0, error)
        return result.stdout
    head = git("rev-parse", "--verify", "HEAD^{commit}").strip()
    require(re.fullmatch(rb"[0-9a-f]{40}", head) is not None, "SOURCE_COMMIT_INVALID")
    require(git("rev-parse", "--show-toplevel").strip().decode() == str(root), "SOURCE_ROOT_MISMATCH")
    require(git("remote", "get-url", "origin").strip() ==
        b"https://github.com/jorgeazofeifa-creator/hioc.git", "SOURCE_REMOTE_MISMATCH")
    require(not git("status", "--porcelain=v1", "--untracked-files=all").strip(), "SOURCE_DIRTY")
    require(git("rev-parse", "--verify", RELEASE + "^{commit}").strip() == RELEASE.encode(),
            "SOURCE_IDENTITY_MISMATCH")
    # A later qualification publication needs no predicted HEAD. This proves only
    # payload lineage; accepted tooling and native mutation authority are separate.
    git("merge-base", "--is-ancestor", RELEASE, "HEAD", error="SOURCE_HISTORY_MISMATCH")
    result = {}
    for item in MANIFEST:
        path = item["path"]
        raw = git("show", RELEASE + ":" + path)
        require(sha(raw) == item["sha256"] and
                git("rev-parse", RELEASE + ":" + path).strip().decode() == item["git_blob"], "SOURCE_IDENTITY_MISMATCH")
        # Delivery bytes come from immutable Git objects, never checkout EOLs.
        result[path] = raw
    return result

class NativeFS:
    """POSIX no-follow pinned ancestors, bounded regular reads and durable writes."""
    def __init__(self, root=HOME):
        require(os.name == "posix", "NATIVE_POSIX_REQUIRED")
        self.root = Path(root)

    def security(self, info, directory=False, mode=None, fd=None):
        require(stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode), "UNSAFE_TYPE")
        require(info.st_uid in (0, 1000) and not stat.S_IMODE(info.st_mode) & 0o7022, "UNSAFE_OWNERSHIP_OR_MODE")
        if not directory:
            require(info.st_nlink == 1, "UNSAFE_HARDLINK")
            require(info.st_uid == info.st_gid == 1000, "UNSAFE_OWNERSHIP_OR_MODE")
        if mode is not None:
            require(stat.S_IMODE(info.st_mode) == mode, "UNSAFE_OWNERSHIP_OR_MODE")
        if fd is not None:
            for name in ("system.posix_acl_access", "system.posix_acl_default"):
                try:
                    os.getxattr(fd, name)
                except OSError as error:
                    require(error.errno == errno.ENODATA, "ACL_NOT_ESTABLISHED")
                else:
                    raise Failure("UNSAFE_ACL")


    @contextlib.contextmanager
    def directory(self, relative="", capture=None):
        path = PurePosixPath(relative)
        require(not path.is_absolute() and ".." not in path.parts, "UNSAFE_PATH")
        fd = os.open("/", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
        chain = []
        owned = [fd]
        try:
            self.security(os.fstat(fd), True, fd=fd)
            for part in (*self.root.parts[1:], *path.parts):
                child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=fd)
                owned.append(child)  # Ownership starts before validation can fail.
                chain.append((fd, part, child))
                self.security(os.fstat(child), True, fd=child)
                fd = child
            if capture is not None:
                capture["/"] = anchored(os.fstat(chain[0][0] if chain else fd))
                name = ""
                for _, part, child in chain:
                    name += "/" + part
                    capture[name] = anchored(os.fstat(child))
            yield fd
            for parent, name, child in chain:
                named = os.stat(name, dir_fd=parent, follow_symlinks=False)
                require(anchored(named) == anchored(os.fstat(child)), "ANCESTOR_DRIFT")
                self.security(named, True, fd=child)
        finally:
            primary = sys.exc_info()[1]
            cleanup_error = None
            for owned_fd in reversed(owned):
                try:
                    os.close(owned_fd)
                except OSError as error:
                    # Do not retry close: the descriptor may already be released.
                    cleanup_error = cleanup_error or error
            if cleanup_error is not None:
                if primary is None:
                    raise cleanup_error
                primary.cleanup_failed = True
                if hasattr(primary, "add_note"):
                    primary.add_note("Directory descriptor cleanup also failed.")

    def ancestors(self, path):
        result = {}
        with self.directory(str(PurePosixPath(path).parent), capture=result):
            pass
        return result

    def transaction_present(self):
        with self.directory("backups") as fd:
            try:
                info = os.stat(TX.split("/")[-1], dir_fd=fd, follow_symlinks=False)
            except FileNotFoundError:
                return False
            self.security(info, True, 0o700)
            require(info.st_uid == info.st_gid == 1000, "UNSAFE_TRANSACTION")
            return True

    def snapshot(self, relative, mode=None):
        p = PurePosixPath(relative)
        parents = self.ancestors(relative)
        with self.directory(str(p.parent)) as parent:
            try:
                fd = os.open(p.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC, dir_fd=parent)
            except FileNotFoundError:
                return {"exists": False, "parents": parents}
            try:
                before = os.fstat(fd)
                self.security(before, mode=mode, fd=fd)
                raw = bytearray()
                while len(raw) <= LIMIT:
                    chunk = os.read(fd, min(65536, LIMIT + 1 - len(raw)))
                    if not chunk:
                        break
                    raw.extend(chunk)
                require(len(raw) <= LIMIT, "SIZE_LIMIT")
                after = os.fstat(fd)
                named = os.stat(p.name, dir_fd=parent, follow_symlinks=False)
                require(identity(before) == identity(after) == identity(named), "FILE_DRIFT")
                return {"exists": True, "parents": parents, "identity": identity(after), "sha256": sha(raw)}
            finally:
                os.close(fd)

    def read(self, path, mode=0o600):
        before = self.snapshot(path, mode)
        require(before["exists"], "FILE_MISSING")
        with self.directory(str(PurePosixPath(path).parent)) as parent:
            fd = os.open(PurePosixPath(path).name, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=parent)
            try:
                require(identity(os.fstat(fd)) == before["identity"], "FILE_DRIFT")
                with os.fdopen(os.dup(fd), "rb") as stream:
                    raw = stream.read(LIMIT + 1)
            finally:
                os.close(fd)
        require(sha(raw) == before["sha256"] and self.snapshot(path, mode) == before, "FILE_DRIFT")
        return raw

    def mkdir_tx(self):
        with self.directory("backups") as fd:
            os.mkdir(TX.split("/")[-1], 0o700, dir_fd=fd)
            os.fsync(fd)
        with self.directory(TX) as fd:
            info = os.fstat(fd)
            require(info.st_uid == info.st_gid == 1000 and stat.S_IMODE(info.st_mode) == 0o700, "UNSAFE_TRANSACTION")

    def write_new(self, relative, raw, mode=0o600):
        p = PurePosixPath(relative)
        with self.directory(str(p.parent)) as parent:
            fd = os.open(p.name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC, mode, dir_fd=parent)
            try:
                os.fchmod(fd, mode)
                self.security(os.fstat(fd), mode=mode, fd=fd)
                with os.fdopen(os.dup(fd), "wb") as stream:
                    stream.write(raw); stream.flush(); os.fsync(stream.fileno())
                os.fsync(fd)
            finally:
                os.close(fd)
            os.fsync(parent)
        require(self.read(relative, mode) == raw, "WRITE_NOT_VERIFIED")

    def journal(self, value):
        raw = canonical(value)
        self.write_new(TX + "/journal-next", raw)
        with self.directory(TX) as parent:
            os.replace("journal-next", "journal.json", src_dir_fd=parent, dst_dir_fd=parent)
            os.fsync(parent)
        require(self.read(TX + "/journal.json") == raw, "JOURNAL_NOT_VERIFIED")

    def publish(self, path, raw, before, mode):
        require(self.snapshot(path, mode if before["exists"] else None) == before, "DESTINATION_DRIFT")
        p = PurePosixPath(path)
        temporary = ".pe73-delivery-" + p.name
        with self.directory(str(p.parent)) as parent:
            relative = str(p.parent / temporary)
            self.write_new(relative, raw, mode)
            require(self.snapshot(path, mode if before["exists"] else None) == before, "DESTINATION_DRIFT")
            if before["exists"]:
                os.replace(temporary, p.name, src_dir_fd=parent, dst_dir_fd=parent)
            else:
                libc = ctypes.CDLL(None, use_errno=True)
                rename = libc.renameat2
                rename.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
                rename.restype = ctypes.c_int
                require(rename(parent, os.fsencode(temporary), parent, os.fsencode(p.name), 1) == 0, "PUBLICATION_FAILED")
            os.fsync(parent)
        after = self.snapshot(path, mode)
        require(after["sha256"] == sha(raw), "INSTALL_NOT_VERIFIED")
        return after

    def remove_installed(self, path, expected, mode):
        require(self.snapshot(path, mode) == expected, "INSTALLED_DRIFT")
        p = PurePosixPath(path)
        with self.directory(str(p.parent)) as parent:
            require(identity(os.stat(p.name, dir_fd=parent, follow_symlinks=False)) == expected["identity"], "INSTALLED_DRIFT")
            os.unlink(p.name, dir_fd=parent)
            os.fsync(parent)
        require(not self.snapshot(path)["exists"], "REMOVAL_NOT_VERIFIED")

    @contextlib.contextmanager
    def mutex(self):
        import fcntl
        with self.directory("backups") as parent:
            fd = os.open(".pe73-delivery.lock", os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW | os.O_CLOEXEC, 0o600, dir_fd=parent)
            try:
                self.security(os.fstat(fd), mode=0o600, fd=fd)
                try:
                    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except BlockingIOError:
                    raise Failure("DEPLOYMENT_BUSY") from None
                named = os.stat(".pe73-delivery.lock", dir_fd=parent, follow_symlinks=False)
                require(identity(named) == identity(os.fstat(fd)), "LOCK_DRIFT")
                yield
            finally:
                os.close(fd)

class NativeConsumers:
    """Actual supplied cron evidence, explicitly NOT exhaustive caller coverage."""
    def observe(self):
        result = subprocess.run(["/usr/bin/crontab", "-l"], stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, timeout=10)
        require(result.returncode == 0 and len(result.stdout) <= 65536, "CRON_UNAVAILABLE")
        lines = result.stdout.decode("utf-8").splitlines()
        require(all(lines.count(line) == 1 for line in CRON), "CRON_MISMATCH")
        return {"cron_sha256": sha(result.stdout), "known_cron_commands": list(CRON),
                "unlocked_asset_or_classification_callers": "NOT_EXCLUDED",
                "coverage": "NOT_ESTABLISHED", "partial_failure_exclusion": "NOT_ESTABLISHED"}

    @contextlib.contextmanager
    def hold(self, observation):
        # A preflight hash, caller declaration, or matching three cron locks
        # is not proof that uncoordinated callers are excluded. No escape flag.
        raise Failure("CONSUMER_COORDINATION_NOT_ESTABLISHED")
        yield  # pragma: no cover

    def assert_active(self):
        raise Failure("CONSUMER_COORDINATION_NOT_ESTABLISHED")

# Conditional maintenance is subordinate to the existing transaction journal.
# No native privileged implementation or production qualification is supplied.
FENCE_PATH = "/home/jazofv1/hioc/pi4/lib/hioc"
MAINTENANCE_PHASES = {
    "PRESERVATION_UNCERTAIN", "SCHEDULER_PRESERVED", "EXCLUSION_UNCERTAIN",
    "LAUNCHES_EXCLUDED", "FENCE_UNCERTAIN", "FENCE_ESTABLISHED", "DRAIN_UNCERTAIN",
    "CONSUMERS_DRAINED", "ESTABLISHED", "REDRAIN_UNCERTAIN", "INSTALLATION_UNCERTAIN", "INSTALLATION_VERIFIED",
    "ROLLBACK_UNCERTAIN", "RESTORATION_VERIFIED", "RELEASE_AUTHORIZED",
    "SCHEDULER_RESTORE_UNCERTAIN", "SCHEDULER_RESTORED_FENCED",
    "ACCESS_RELEASE_UNCERTAIN", "ACCESS_RESTORED_VERIFIED"}
BOUNDARY_FIELDS = {"readers_drained", "cached_modules_drained", "open_descriptors_drained",
    "identities_enumerated", "privileged_callers_excluded", "permission_editors_excluded",
    "alternate_launchers_excluded", "persistent_fence_qualified"}


def maintenance_cron(raw, approved, inventory):
    require(type(raw) is bytes and 0 < len(raw) <= 65536 and raw.endswith(b"\n") and
        b"\r" not in raw and b"\0" not in raw, "MAINTENANCE_CRON_INVALID")
    try:
        lines = raw.decode("utf-8", "strict").splitlines(keepends=True)
    except UnicodeError:
        raise Failure("MAINTENANCE_CRON_INVALID") from None
    active = [line[:-1] for line in lines if line.strip() and not line.lstrip().startswith("#")]
    require(type(approved) is list and 3 <= len(approved) <= 128 and
        all(type(x) is str and 0 < len(x) <= 4096 and "\n" not in x for x in approved) and
        len(set(approved)) == len(approved) and set(CRON) <= set(approved), "MAINTENANCE_JOB_SCOPE")
    require(len(active) == len(set(active)) and type(inventory) is dict and set(inventory) == set(active) and
        all(x in {"EXCLUDE", "PRESERVE"} for x in inventory.values()) and
        {line for line, action in inventory.items() if action == "EXCLUDE"} == set(approved),
        "MAINTENANCE_JOB_INVENTORY")
    return "".join(line for line in lines if line[:-1] not in approved).encode("utf-8")


def fence_identity(value):
    require(type(value) is dict and set(value) ==
        {"st_dev", "st_ino", "st_uid", "st_gid", "mode", "type", "acl"} and
        all(type(value[k]) is int and value[k] >= 0 for k in
            ("st_dev", "st_ino", "st_uid", "st_gid", "mode")) and
        value["type"] == "DIRECTORY" and value["st_uid"] == value["st_gid"] == 1000 and
        value["mode"] <= 0o7777 and not value["mode"] & 0o7022 and value["acl"] == "ABSENT",
        "MAINTENANCE_FENCE_IDENTITY")
    return value


class NativeFenceInterface:
    """Fixed resource contract only. Never sudo, chmod, chown or run commands."""
    target = FENCE_PATH

    def restrict(self, reference, binding):
        authorization(reference, binding)
        raise Failure("NATIVE_FENCE_NOT_QUALIFIED")

    def restore(self, reference, binding):
        authorization(reference, binding)
        raise Failure("NATIVE_FENCE_NOT_QUALIFIED")


def validate_maintenance(fs, value):
    m = value["maintenance"]
    require(type(m) is dict and set(m) == {"version", "kind", "phase", "pending",
        "original_cron_sha256", "maintenance_cron_sha256", "approved_jobs", "inventory",
        "scheduler_identity", "original_fence", "boundary", "authorizations", "release_runtime_sha256", "resume_phase"},
        "MAINTENANCE_JOURNAL_INVALID")
    require(type(m["version"]) is int and m["version"] == 1 and m["kind"] == "SYNTHETIC_ONLY" and
        type(m["phase"]) is str and m["phase"] in MAINTENANCE_PHASES, "MAINTENANCE_JOURNAL_INVALID")
    pending = {"PRESERVATION_UNCERTAIN": "PRESERVE", "EXCLUSION_UNCERTAIN": "EXCLUDE",
        "FENCE_UNCERTAIN": "RESTRICT", "DRAIN_UNCERTAIN": "DRAIN",
        "SCHEDULER_RESTORE_UNCERTAIN": "RESTORE_SCHEDULER", "ACCESS_RELEASE_UNCERTAIN": "RELEASE_ACCESS",
        "REDRAIN_UNCERTAIN": "REDRAIN"}
    require(m["pending"] == pending.get(m["phase"]), "MAINTENANCE_JOURNAL_INVALID")
    require(all(type(m[k]) is str and DIGEST.fullmatch(m[k]) for k in
        ("original_cron_sha256", "maintenance_cron_sha256")), "MAINTENANCE_JOURNAL_INVALID")
    fence_identity(m["original_fence"])
    require(m["original_fence"]["mode"] & 0o500 == 0o500, "MAINTENANCE_JOURNAL_INVALID")
    require(type(m["scheduler_identity"]) is dict and set(m["scheduler_identity"]) ==
        {"uid", "gid", "metadata"} and type(m["scheduler_identity"]["uid"]) is int and
        type(m["scheduler_identity"]["gid"]) is int and
        m["scheduler_identity"]["uid"] == m["scheduler_identity"]["gid"] == 1000 and
        type(m["scheduler_identity"]["metadata"]) is dict and
        len(canonical(m["scheduler_identity"]["metadata"])) <= 4096, "MAINTENANCE_JOURNAL_INVALID")
    require(type(m["authorizations"]) is list and 1 <= len(m["authorizations"]) <= 64,
        "MAINTENANCE_JOURNAL_INVALID")
    refs = []
    for entry in m["authorizations"]:
        require(type(entry) is dict and set(entry) == {"action", "reference"} and
            entry["action"] in {"PRESERVE", "EXCLUDE", "RESTRICT", "DRAIN", "ESTABLISH", "REDRAIN", "ATTACH",
                "AUTHORIZE_RELEASE", "RESTORE_SCHEDULER", "RELEASE_ACCESS"} and
            type(entry["reference"]) is str and AUTH.fullmatch(entry["reference"]), "MAINTENANCE_JOURNAL_INVALID")
        refs.append(entry["reference"])
    require(len(set(refs)) == len(refs), "MAINTENANCE_JOURNAL_INVALID")
    # Recovery attachment is a recorded read/requalification operation, never
    # evidence that an exclusion or release effect occurred.
    actions = [entry["action"] for entry in m["authorizations"]]
    sequence = ["PRESERVE", "EXCLUDE", "RESTRICT", "DRAIN", "ESTABLISH",
        "AUTHORIZE_RELEASE", "RESTORE_SCHEDULER", "RELEASE_ACCESS"]
    progress = 0
    for action in actions:
        if action == "ATTACH":
            require(1 <= progress < 8 or progress == 8 and m["phase"] == "ACCESS_RELEASE_UNCERTAIN",
                "MAINTENANCE_JOURNAL_INVALID")
        elif action == "REDRAIN":
            require(progress in (4, 5, 6, 7), "MAINTENANCE_JOURNAL_INVALID")
        else:
            require(progress < len(sequence) and action == sequence[progress], "MAINTENANCE_JOURNAL_INVALID")
            progress += 1
    phase = m["resume_phase"] if m["phase"] == "REDRAIN_UNCERTAIN" else m["phase"]
    counts = {"PRESERVATION_UNCERTAIN": 1, "SCHEDULER_PRESERVED": 1,
        "EXCLUSION_UNCERTAIN": 2, "LAUNCHES_EXCLUDED": 2,
        "FENCE_UNCERTAIN": 3, "FENCE_ESTABLISHED": 3,
        "DRAIN_UNCERTAIN": 4, "CONSUMERS_DRAINED": 4, "ESTABLISHED": 5,
        "INSTALLATION_UNCERTAIN": 5, "INSTALLATION_VERIFIED": 5,
        "ROLLBACK_UNCERTAIN": 5, "RESTORATION_VERIFIED": 5,
        "RELEASE_AUTHORIZED": 6, "SCHEDULER_RESTORE_UNCERTAIN": 7,
        "SCHEDULER_RESTORED_FENCED": 7, "ACCESS_RELEASE_UNCERTAIN": 8,
        "ACCESS_RESTORED_VERIFIED": 8}
    require(type(phase) is str and progress == counts.get(phase), "MAINTENANCE_JOURNAL_INVALID")
    if m["phase"] == "REDRAIN_UNCERTAIN":
        require([a for a in actions if a != "ATTACH"][-1] == "REDRAIN", "MAINTENANCE_JOURNAL_INVALID")
    if m["phase"] != "PRESERVATION_UNCERTAIN":
        raw = fs.read(TX + "/crontab-original")
        require(sha(raw) == m["original_cron_sha256"] and
            sha(maintenance_cron(raw, m["approved_jobs"], m["inventory"])) == m["maintenance_cron_sha256"],
            "MAINTENANCE_JOURNAL_INVALID")
    if m["boundary"] is not None:
        b = m["boundary"]
        require(type(b) is dict and set(b) == BOUNDARY_FIELDS | {"kind", "session", "scope_sha256"} and
            b["kind"] == "SYNTHETIC_ONLY" and type(b["session"]) is str and AUTH.fullmatch(b["session"]) and
            type(b["scope_sha256"]) is str and DIGEST.fullmatch(b["scope_sha256"]) and
            all(b[k] is True for k in BOUNDARY_FIELDS), "MAINTENANCE_JOURNAL_INVALID")
    early = {"PRESERVATION_UNCERTAIN", "SCHEDULER_PRESERVED", "EXCLUSION_UNCERTAIN", "LAUNCHES_EXCLUDED",
        "FENCE_UNCERTAIN", "FENCE_ESTABLISHED", "DRAIN_UNCERTAIN", "CONSUMERS_DRAINED", "ESTABLISHED"}
    require(m["resume_phase"] in {"CONSUMERS_DRAINED", "ESTABLISHED", "INSTALLATION_UNCERTAIN", "INSTALLATION_VERIFIED",
        "ROLLBACK_UNCERTAIN", "RESTORATION_VERIFIED", "RELEASE_AUTHORIZED", "SCHEDULER_RESTORED_FENCED"}
        if m["phase"] == "REDRAIN_UNCERTAIN" else
        m["resume_phase"] is None, "MAINTENANCE_JOURNAL_INVALID")
    if phase in early:
        require(value["state"] == "PREPARED", "MAINTENANCE_JOURNAL_INVALID")
    if phase == "INSTALLATION_UNCERTAIN":
        require(value["state"] == "COMMITTING", "MAINTENANCE_JOURNAL_INVALID")
    if phase == "ROLLBACK_UNCERTAIN":
        require(value["state"] == "ROLLING_BACK", "MAINTENANCE_JOURNAL_INVALID")
    if phase == "INSTALLATION_VERIFIED":
        require(value["state"] == "COMMITTED", "MAINTENANCE_JOURNAL_INVALID")
    if phase == "RESTORATION_VERIFIED":
        require(value["state"] == "ROLLED_BACK", "MAINTENANCE_JOURNAL_INVALID")
    release = {"RELEASE_AUTHORIZED", "SCHEDULER_RESTORE_UNCERTAIN", "SCHEDULER_RESTORED_FENCED",
        "ACCESS_RELEASE_UNCERTAIN", "ACCESS_RESTORED_VERIFIED"}
    require(m["release_runtime_sha256"] is None if phase not in release else
        type(m["release_runtime_sha256"]) is str and DIGEST.fullmatch(m["release_runtime_sha256"]),
        "MAINTENANCE_JOURNAL_INVALID")
    if phase in release:
        require(value["state"] in {"COMMITTED", "ROLLED_BACK"} and value["pending"] is None and
            any(x["action"] == "AUTHORIZE_RELEASE" for x in m["authorizations"]), "MAINTENANCE_JOURNAL_INVALID")
    if m["phase"] != "REDRAIN_UNCERTAIN" and phase in {"CONSUMERS_DRAINED", "ESTABLISHED", "INSTALLATION_UNCERTAIN", "INSTALLATION_VERIFIED",
            "ROLLBACK_UNCERTAIN", "RESTORATION_VERIFIED"} | release:
        require(m["boundary"] is not None, "MAINTENANCE_JOURNAL_INVALID")


class MaintenanceConsumers:
    """Windows synthetic integration seam; not a production permission provider."""
    def __init__(self, ops, approved_jobs, inventory):
        require(os.name == "nt", "NATIVE_MAINTENANCE_NOT_QUALIFIED")
        self.ops, self.approved_jobs, self.inventory = ops, approved_jobs, inventory
        self.controller = None
        raw, _ = ops.scheduler()
        maintenance_cron(raw, approved_jobs, inventory)
        self.observation = self.original_binding(raw)
        self.recovery_needs_drain = False
        self.attachment_reference = None
        self.initial_context_bound = False

    def attachment_matches(self, maintenance):
        latest = next((item["reference"] for item in reversed(maintenance["authorizations"])
            if item["action"] == "ATTACH"), None)
        return self.attachment_reference == latest

    @staticmethod
    def original_binding(raw):
        return {"cron_sha256": sha(raw), "known_cron_commands": list(CRON),
            "coverage": "SYNTHETIC_ONLY_NATIVE_UNQUALIFIED", "partial_failure_exclusion": "CONDITIONAL_SYNTHETIC",
            "unlocked_asset_or_classification_callers": "REQUIRES_VERIFIED_DRAIN_AND_FENCE"}

    @classmethod
    def attach(cls, fs, source, ops, reference, binding):
        """Attach fresh objects to validated persisted maintenance; no external effects.

        The only write is a fresh ATTACH authorization in the existing private
        journal. Scheduler, fence, runtime progress and pending uncertainty are
        never repaired or adopted here. Native attachment remains unavailable.
        """
        require(os.name == "nt" and cls is MaintenanceConsumers, "NATIVE_MAINTENANCE_NOT_QUALIFIED")
        authorization(reference, binding)
        check_sources(source)
        with fs.mutex():
            require(fs.transaction_present(), "RECOVERY_TRANSACTION_MISSING")
            probe = Controller(fs, source, NativeConsumers())
            value = probe._journal()
            require(sha(canonical(value)) == binding, "MAINTENANCE_STALE_AUTHORIZATION")
            m = value.get("maintenance")
            require(m is not None, "RECOVERY_UNRELATED_TRANSACTION")
            require(m["phase"] != "ACCESS_RESTORED_VERIFIED", "RECOVERY_ALREADY_COMPLETED")
            used = [value[k] for k in ("prepare_authorization", "commit_authorization", "rollback_authorization")]
            used += [entry["reference"] for entry in m["authorizations"]]
            require(reference not in used, "MAINTENANCE_AUTHORIZATION_REUSED")
            original = fs.read(TX + "/crontab-original")
            require(sha(original) == m["original_cron_sha256"], "RECOVERY_BACKUP_MISMATCH")
            excluded = maintenance_cron(original, m["approved_jobs"], m["inventory"])
            require(sha(excluded) == m["maintenance_cron_sha256"] and
                value["consumers"] == cls.original_binding(original), "RECOVERY_ORIGINAL_BINDING_MISMATCH")
            raw, metadata = ops.scheduler()
            phase = m["resume_phase"] if m["phase"] == "REDRAIN_UNCERTAIN" else m["phase"]
            before_exclusion = {"PRESERVATION_UNCERTAIN", "SCHEDULER_PRESERVED"}
            after_restore = {"SCHEDULER_RESTORED_FENCED", "ACCESS_RELEASE_UNCERTAIN"}
            allowed_cron = (original,) if phase in before_exclusion | after_restore else (excluded,)
            if phase in {"EXCLUSION_UNCERTAIN", "SCHEDULER_RESTORE_UNCERTAIN"}:
                allowed_cron = (original, excluded)
            require(metadata == m["scheduler_identity"] and raw in allowed_cron, "RECOVERY_SCHEDULER_MISMATCH")
            current = fence_identity(ops.fence())
            fenced = dict(m["original_fence"], mode=0)
            before_fence = before_exclusion | {"EXCLUSION_UNCERTAIN", "LAUNCHES_EXCLUDED"}
            allowed_fence = (m["original_fence"],) if phase in before_fence else (fenced,)
            if phase in {"FENCE_UNCERTAIN", "ACCESS_RELEASE_UNCERTAIN"}:
                allowed_fence = (m["original_fence"], fenced)
            require(current in allowed_fence, "RECOVERY_FENCE_MISMATCH")
            approved_source = {x["path"]: x["sha256"] for x in MANIFEST}
            for path in ORDER:
                expected = value["restored"].get(path,
                    value["installed"].get(path, value["baseline"][path]))
                actual = fs.snapshot(path, MODES[path] if expected["exists"] or path == value["pending"] else None)
                if actual == expected:
                    continue
                # A pending operation can have either its exact before-state or
                # its approved after-content. Keep the pending marker untouched;
                # observing either possibility is not permission to resume.
                require(path == value["pending"] and value["state"] in {"COMMITTING", "ROLLING_BACK"},
                    "RECOVERY_RUNTIME_DRIFT")
                after_exists = value["state"] == "COMMITTING" or path in PRIOR
                require(actual.get("exists") is after_exists and
                    actual.get("parents") == value["baseline"][path]["parents"], "RECOVERY_RUNTIME_DRIFT")
                if after_exists:
                    identity = actual.get("identity", {})
                    digest = approved_source[path] if value["state"] == "COMMITTING" else PRIOR[path][0]
                    require(actual.get("sha256") == digest and identity.get("type") == "REGULAR" and
                        identity.get("st_uid") == identity.get("st_gid") == 1000 and
                        identity.get("mode") == MODES[path] and identity.get("st_nlink") == 1,
                        "RECOVERY_RUNTIME_DRIFT")
            provider = cls.__new__(cls)  # Only after original and live evidence validation.
            provider.ops = ops
            provider.approved_jobs, provider.inventory = m["approved_jobs"], m["inventory"]
            provider.observation = cls.original_binding(original)
            provider.recovery_needs_drain = True  # Never trust a previous process proof, even with the same token.
            provider.attachment_reference = reference
            provider.initial_context_bound = True
            controller = Controller(fs, source, provider)
            provider.controller = controller
            m["authorizations"].append({"action": "ATTACH", "reference": reference})
            controller._save(value, "MAINTENANCE:RECOVERY_ATTACHED")
            return controller

    def observe(self):
        # Original scheduler binding; actual maintenance is reobserved in hold.
        return dict(self.observation)

    @contextlib.contextmanager
    def hold(self, observation):
        require(observation == self.observation, "CONSUMER_DRIFT")
        self.assert_active()
        yield  # No automatic release on success, error, termination or rollback.

    def assert_active(self):
        require(self.controller is not None, "MAINTENANCE_NOT_ESTABLISHED")
        value = self.controller._journal()
        m = value.get("maintenance")
        require(m is not None and m["phase"] in {"ESTABLISHED", "INSTALLATION_UNCERTAIN",
            "INSTALLATION_VERIFIED", "ROLLBACK_UNCERTAIN", "RESTORATION_VERIFIED"}, "MAINTENANCE_NOT_ESTABLISHED")
        Maintenance(self.controller)._held(m)


class Maintenance:
    """Bounded effects and evidence stored only in the existing delivery journal."""
    def __init__(self, controller):
        self.c = controller
        require(os.name == "nt" and type(controller.consumers) is MaintenanceConsumers,
            "NATIVE_MAINTENANCE_NOT_QUALIFIED")
        self.provider = controller.consumers
        if not self.provider.initial_context_bound:
            require(not controller.fs.transaction_present(), "RECOVERY_ATTACHMENT_REQUIRED")
            self.provider.initial_context_bound = True
        self.provider.controller = controller
        self.ops = self.provider.ops

    def _load(self, reference, binding, action, phases):
        authorization(reference, binding)
        value = self.c._journal()
        require(sha(canonical(value)) == binding, "MAINTENANCE_STALE_AUTHORIZATION")
        m = value.get("maintenance")
        require((m is None and phases is None) or m is not None and phases is not None and m["phase"] in phases,
            "MAINTENANCE_TRANSITION_REFUSED")
        used = [value[k] for k in ("prepare_authorization", "commit_authorization", "rollback_authorization")]
        if m is not None:
            used += [x["reference"] for x in m["authorizations"]]
        require(reference not in used, "MAINTENANCE_AUTHORIZATION_REUSED")
        require(m is None or self.provider.attachment_matches(m), "MAINTENANCE_ATTACHMENT_SUPERSEDED")
        return value, m

    def _record(self, value, reference, action, phase, pending=None):
        m = value["maintenance"]
        m["authorizations"].append({"action": action, "reference": reference})
        m.update(phase=phase, pending=pending)
        self.c._save(value, "MAINTENANCE:" + phase)

    def _finish(self, value, phase):
        value["maintenance"].update(phase=phase, pending=None)
        self.c._save(value, "MAINTENANCE:" + phase)
        return self.inspect()

    def _original(self, m):
        raw = self.c.fs.read(TX + "/crontab-original")
        require(sha(raw) == m["original_cron_sha256"], "MAINTENANCE_BACKUP_DRIFT")
        return raw

    def _scheduler(self, m, original=False):
        raw, identity = self.ops.scheduler()
        require(identity == m["scheduler_identity"] and sha(raw) ==
            m["original_cron_sha256" if original else "maintenance_cron_sha256"], "MAINTENANCE_SCHEDULER_DRIFT")
        return raw

    def _fenced(self, m):
        actual = fence_identity(self.ops.fence())
        require(actual == dict(m["original_fence"], mode=0), "MAINTENANCE_FENCE_NOT_ESTABLISHED")

    def _scope(self, m):
        return sha(canonical({k: m[k] for k in ("original_cron_sha256", "maintenance_cron_sha256",
            "original_fence", "approved_jobs", "inventory")}))

    def _held(self, m):
        require(self.provider.attachment_matches(m), "MAINTENANCE_ATTACHMENT_SUPERSEDED")
        require(not self.provider.recovery_needs_drain, "MAINTENANCE_DRAIN_NOT_CURRENT")
        self._scheduler(m); self._fenced(m)
        proof = self.ops.boundary(self._scope(m))
        require(proof == m["boundary"], "MAINTENANCE_DRAIN_NOT_CURRENT")
        require(all(proof[k] is True for k in BOUNDARY_FIELDS), "MAINTENANCE_DRAIN_FAILED")

    def inspect(self):
        value = self.c._journal(); m = value.get("maintenance")
        if m is None:
            return {"phase": "NOT_ESTABLISHED", "production_qualified": False}
        # Observe actual effects separately; journal labels never prove enforcement.
        raw, identity = self.ops.scheduler(); current = self.ops.fence()
        return {"phase": m["phase"], "pending": m["pending"], "journal_sha256": sha(canonical(value)),
            "scheduler_sha256": sha(raw), "scheduler_identity_matches": identity == m["scheduler_identity"],
            "fence_identity_matches": current == dict(m["original_fence"], mode=0),
            "access_metadata_restored": current == m["original_fence"],
            "production_qualified": False, "evidence_kind": "SYNTHETIC_ONLY",
            "process_requalification_required": self.provider.recovery_needs_drain or
                not self.provider.attachment_matches(m)}

    def preserve(self, reference, binding):
        with self.c.fs.mutex():
            value, _ = self._load(reference, binding, "PRESERVE", None)
            require(value["state"] == "PREPARED", "MAINTENANCE_TRANSITION_REFUSED")
            raw, identity = self.ops.scheduler()
            require(sha(raw) == self.provider.observation["cron_sha256"], "MAINTENANCE_SCHEDULER_DRIFT")
            excluded = maintenance_cron(raw, self.provider.approved_jobs, self.provider.inventory)
            original = fence_identity(self.ops.fence())
            require(original["mode"] & 0o500 == 0o500, "MAINTENANCE_FENCE_IDENTITY")
            value["maintenance"] = {"version": 1, "kind": "SYNTHETIC_ONLY", "phase": "PRESERVATION_UNCERTAIN",
                "pending": "PRESERVE", "original_cron_sha256": sha(raw), "maintenance_cron_sha256": sha(excluded),
                "approved_jobs": self.provider.approved_jobs, "inventory": self.provider.inventory,
                "scheduler_identity": identity, "original_fence": original, "boundary": None,
                "authorizations": [], "release_runtime_sha256": None, "resume_phase": None}
            self._record(value, reference, "PRESERVE", "PRESERVATION_UNCERTAIN", "PRESERVE")
            self.c.fs.write_new(TX + "/crontab-original", raw)
            require(self.c.fs.read(TX + "/crontab-original") == raw, "MAINTENANCE_BACKUP_DRIFT")
            self._scheduler(value["maintenance"], original=True)
            return self._finish(value, "SCHEDULER_PRESERVED")

    def exclude(self, reference, binding):
        with self.c.fs.mutex():
            value, m = self._load(reference, binding, "EXCLUDE", {"SCHEDULER_PRESERVED"})
            raw = self._original(m); self._scheduler(m, original=True)
            candidate = maintenance_cron(raw, m["approved_jobs"], m["inventory"])
            self._record(value, reference, "EXCLUDE", "EXCLUSION_UNCERTAIN", "EXCLUDE")
            self.ops.install_scheduler(candidate, m["original_cron_sha256"])  # Fixture-only expected-byte check.
            self._scheduler(m)
            return self._finish(value, "LAUNCHES_EXCLUDED")

    def restrict(self, reference, binding):
        with self.c.fs.mutex():
            value, m = self._load(reference, binding, "RESTRICT", {"LAUNCHES_EXCLUDED"})
            self._scheduler(m)
            require(self.ops.fence() == m["original_fence"], "MAINTENANCE_FENCE_DRIFT")
            self._record(value, reference, "RESTRICT", "FENCE_UNCERTAIN", "RESTRICT")
            self.ops.restrict(reference, binding)
            self._fenced(m)
            return self._finish(value, "FENCE_ESTABLISHED")

    def drain(self, reference, binding):
        with self.c.fs.mutex():
            value, m = self._load(reference, binding, "DRAIN", {"FENCE_ESTABLISHED"})
            self._scheduler(m); self._fenced(m)
            self._record(value, reference, "DRAIN", "DRAIN_UNCERTAIN", "DRAIN")
            proof = self.ops.drain(self._scope(m))
            require(type(proof) is dict and all(proof.get(k) is True for k in BOUNDARY_FIELDS),
                "MAINTENANCE_DRAIN_FAILED")
            m["boundary"] = proof
            result = self._finish(value, "CONSUMERS_DRAINED")
            self.provider.recovery_needs_drain = False
            return result

    def establish(self, reference, binding):
        with self.c.fs.mutex():
            value, m = self._load(reference, binding, "ESTABLISH", {"CONSUMERS_DRAINED"})
            self._held(m)
            self._record(value, reference, "ESTABLISH", "ESTABLISHED")
            return self.inspect()

    def redrain(self, reference, binding):
        with self.c.fs.mutex():
            value, m = self._load(reference, binding, "REDRAIN", {"CONSUMERS_DRAINED", "ESTABLISHED", "INSTALLATION_UNCERTAIN",
                "INSTALLATION_VERIFIED", "ROLLBACK_UNCERTAIN", "RESTORATION_VERIFIED", "REDRAIN_UNCERTAIN",
                "RELEASE_AUTHORIZED", "SCHEDULER_RESTORED_FENCED"})
            observed_phase = m["resume_phase"] if m["phase"] == "REDRAIN_UNCERTAIN" else m["phase"]
            self._scheduler(m, original=observed_phase == "SCHEDULER_RESTORED_FENCED"); self._fenced(m)
            # Invalidate the previous process proof durably before a new observation.
            phase = m["resume_phase"] if m["phase"] == "REDRAIN_UNCERTAIN" else m["phase"]
            m["boundary"] = None
            m["resume_phase"] = phase
            self._record(value, reference, "REDRAIN", "REDRAIN_UNCERTAIN", "REDRAIN")
            proof = self.ops.drain(self._scope(m))
            require(type(proof) is dict and all(proof.get(k) is True for k in BOUNDARY_FIELDS),
                "MAINTENANCE_DRAIN_FAILED")
            m["boundary"] = proof
            m["resume_phase"] = None
            result = self._finish(value, phase)
            self.provider.recovery_needs_drain = False
            return result

    def _runtime(self, value):
        require(value["state"] in {"COMMITTED", "ROLLED_BACK"} and value["pending"] is None,
            "MAINTENANCE_RUNTIME_UNCERTAIN")
        check_sources(self.c.source)
        report = self.c.inspect()
        require(report["live_state_established"], "MAINTENANCE_RUNTIME_DRIFT")
        return sha(canonical({k: value[k] for k in ("state", "baseline", "installed", "restored", "manifest_sha256")}))

    def authorize_release(self, reference, binding):
        with self.c.fs.mutex():
            value, m = self._load(reference, binding, "AUTHORIZE_RELEASE", {"INSTALLATION_VERIFIED", "RESTORATION_VERIFIED"})
            self._held(m)
            m["release_runtime_sha256"] = self._runtime(value)
            self._record(value, reference, "AUTHORIZE_RELEASE", "RELEASE_AUTHORIZED")
            return self.inspect()

    def restore_scheduler(self, reference, binding):
        with self.c.fs.mutex():
            value, m = self._load(reference, binding, "RESTORE_SCHEDULER", {"RELEASE_AUTHORIZED"})
            self._held(m)
            require(self._runtime(value) == m["release_runtime_sha256"], "MAINTENANCE_RUNTIME_DRIFT")
            raw = self._original(m)
            self._record(value, reference, "RESTORE_SCHEDULER", "SCHEDULER_RESTORE_UNCERTAIN", "RESTORE_SCHEDULER")
            self.ops.install_scheduler(raw, m["maintenance_cron_sha256"])
            self._scheduler(m, original=True); self._fenced(m)
            return self._finish(value, "SCHEDULER_RESTORED_FENCED")

    def release_access(self, reference, binding):
        with self.c.fs.mutex():
            value, m = self._load(reference, binding, "RELEASE_ACCESS", {"SCHEDULER_RESTORED_FENCED"})
            require(not self.provider.recovery_needs_drain, "MAINTENANCE_DRAIN_NOT_CURRENT")
            self._scheduler(m, original=True); self._fenced(m)
            require(self.ops.boundary(self._scope(m)) == m["boundary"], "MAINTENANCE_DRAIN_NOT_CURRENT")
            require(self._runtime(value) == m["release_runtime_sha256"], "MAINTENANCE_RUNTIME_DRIFT")
            self._record(value, reference, "RELEASE_ACCESS", "ACCESS_RELEASE_UNCERTAIN", "RELEASE_ACCESS")
            self.ops.restore(reference, binding)
            require(self.ops.fence() == m["original_fence"], "MAINTENANCE_RESTORATION_UNCERTAIN")
            self._scheduler(m, original=True)
            return self._finish(value, "ACCESS_RESTORED_VERIFIED")


def check_sources(source):
    require(set(source) == set(ORDER) and len(MANIFEST) == len(ORDER) == 13, "SOURCE_MANIFEST")
    require(set(PRIOR) <= set(ORDER), "SOURCE_MANIFEST")
    for item in MANIFEST:
        raw = source[item["path"]]
        require(sha(raw) == item["sha256"], "SOURCE_IDENTITY_MISMATCH")
        require(hashlib.sha1(("blob " + str(len(raw)) + "\0").encode() + raw).hexdigest() == item["git_blob"], "SOURCE_IDENTITY_MISMATCH")

def preflight(fs, source, consumers):
    check_sources(source)
    baseline = {}
    for path in ORDER:
        before = fs.snapshot(path, MODES[path] if path in PRIOR else None)
        if path in PRIOR:
            require(before["exists"] and before["sha256"] == PRIOR[path][0], "BASELINE_MISMATCH")
        else:
            require(not before["exists"], "UNEXPECTED_TARGET")
        baseline[path] = before
    return {"version": 1, "release": RELEASE, "manifest_sha256": sha(canonical({"files": MANIFEST})),
            "baseline": baseline, "consumers": consumers.observe()}

def authorization(reference, bound_sha):
    require(type(reference) is str and AUTH.fullmatch(reference), "AUTHORIZATION_REQUIRED")
    require(type(bound_sha) is str and DIGEST.fullmatch(bound_sha), "EVIDENCE_BINDING_REQUIRED")

class Controller:
    def __init__(self, fs, source, consumers, fault=lambda _: None):
        self.fs, self.source, self.consumers, self.fault = fs, source, consumers, fault

    def inspect(self):
        if not self.fs.transaction_present():
            return {"state": "NOT_STARTED", "live_state_established": False}
        snap = self.fs.snapshot(TX + "/journal.json", 0o600)
        if not snap["exists"]:
            return {"state": "INCOMPLETE", "mutation": "UNKNOWN", "live_state_established": False}
        value = self._journal()
        # Inspection reports journal authority and separate current target matches.
        expected = {path: value["restored"].get(path,
                    value["installed"].get(path, value["baseline"][path])) for path in ORDER}
        matches = {path: self.fs.snapshot(path, MODES[path] if item["exists"] else None) == item
                   for path, item in expected.items()}
        return {"state": value["state"], "journal_sha256": sha(canonical(value)),
                "pending": value["pending"], "installed_matches": matches,
                "live_state_established": all(matches.values()) and value["pending"] is None}

    def _journal(self):
        # A state label is not recovery evidence. Validate the complete recorded
        # prefix/restoration relationship before inspect can trust any entry.
        try:
            value = parsed(self.fs.read(TX + "/journal.json"))
            keys = {"version", "release", "manifest_sha256", "baseline", "consumers",
                "state", "prepare_authorization", "commit_authorization", "rollback_authorization",
                "installed", "restored", "pending"}
            require(set(value) in (keys, keys | {"maintenance"}), "JOURNAL_INVALID")
            require(type(value["version"]) is int and value["version"] == 1 and
                value["release"] == RELEASE and
                value["manifest_sha256"] == sha(canonical({"files": MANIFEST})), "JOURNAL_INVALID")
            for key in ("baseline", "installed", "restored", "consumers"):
                require(type(value[key]) is dict, "JOURNAL_INVALID")
            require(set(value["baseline"]) == set(ORDER) and set(value["installed"]) <= set(ORDER) and
                set(value["restored"]) <= set(value["installed"]), "JOURNAL_INVALID")
            state = value["state"]
            require(type(state) is str and state in {"PREPARING", "PREPARED", "COMMITTING", "COMMITTED",
                "ROLLING_BACK", "ROLLED_BACK"}, "JOURNAL_INVALID")
            pending = value["pending"]
            require(pending is None or type(pending) is str and pending in ORDER, "JOURNAL_INVALID")
            for key, needed in (("prepare_authorization", True),
                    ("commit_authorization", state not in ("PREPARING", "PREPARED")),
                    ("rollback_authorization", state in ("ROLLING_BACK", "ROLLED_BACK"))):
                reference = value[key]
                require(type(reference) is str and AUTH.fullmatch(reference) if needed else reference is None,
                    "JOURNAL_INVALID")
            consumers = value["consumers"]
            require(set(consumers) == {"cron_sha256", "known_cron_commands", "coverage",
                "partial_failure_exclusion", "unlocked_asset_or_classification_callers"}, "JOURNAL_INVALID")
            require(type(consumers["cron_sha256"]) is str and DIGEST.fullmatch(consumers["cron_sha256"]) and
                type(consumers["known_cron_commands"]) is list and consumers["known_cron_commands"] == list(CRON),
                "JOURNAL_INVALID")
            for key in ("coverage", "partial_failure_exclusion", "unlocked_asset_or_classification_callers"):
                require(type(consumers[key]) is str and 0 < len(consumers[key]) <= 96, "JOURNAL_INVALID")

            def snapshot(item, path, exists, digest=None):
                require(type(item) is dict and set(item) ==
                    ({"exists", "parents", "identity", "sha256"} if exists else {"exists", "parents"}) and
                    type(item["exists"]) is bool and item["exists"] is exists, "JOURNAL_INVALID")
                parents = item["parents"]
                require(type(parents) is dict and 0 < len(parents) <= 128, "JOURNAL_INVALID")
                for name, parent in parents.items():
                    require(type(name) is str and 0 < len(name) <= 4096 and
                        ".." not in PurePosixPath(name).parts and type(parent) is dict and
                        set(parent) == {"st_dev", "st_ino", "st_uid", "st_gid", "mode", "type"}, "JOURNAL_INVALID")
                    require(all(type(parent[k]) is int and parent[k] >= 0 for k in
                        ("st_dev", "st_ino", "st_uid", "st_gid", "mode")) and parent["type"] == "DIRECTORY" and
                        parent["st_uid"] in (0, 1000) and parent["mode"] <= 0o7777 and
                        not parent["mode"] & 0o7022, "JOURNAL_INVALID")
                if exists:
                    identity = item["identity"]
                    require(type(identity) is dict and set(identity) == {"st_dev", "st_ino", "st_uid", "st_gid",
                        "mode", "type", "st_nlink", "st_size", "st_mtime_ns", "st_ctime_ns"}, "JOURNAL_INVALID")
                    require(all(type(identity[k]) is int and identity[k] >= 0 for k in identity if k != "type") and
                        identity["type"] == "REGULAR" and identity["st_uid"] == identity["st_gid"] == 1000 and
                        identity["st_nlink"] == 1 and identity["mode"] == MODES[path] and
                        identity["st_size"] <= LIMIT and item["sha256"] == digest, "JOURNAL_INVALID")

            source = {item["path"]: item["sha256"] for item in MANIFEST}
            for path, item in value["baseline"].items():
                snapshot(item, path, path in PRIOR, PRIOR[path][0] if path in PRIOR else None)
            installed = [path for path in ORDER if path in value["installed"]]
            require(installed == ORDER[:len(installed)], "JOURNAL_INVALID")
            for path in installed:
                item = value["installed"][path]
                snapshot(item, path, True, source[path])
                require(item["parents"] == value["baseline"][path]["parents"], "JOURNAL_INVALID")
            restored = [path for path in reversed(installed) if path in value["restored"]]
            require(restored == list(reversed(installed))[:len(restored)], "JOURNAL_INVALID")
            for path in restored:
                item = value["restored"][path]
                snapshot(item, path, path in PRIOR, PRIOR[path][0] if path in PRIOR else None)
                require(item["parents"] == value["baseline"][path]["parents"], "JOURNAL_INVALID")
                if path in PRIOR:
                    backup = self.fs.read(TX + "/backup-" + str(ORDER.index(path)))
                    require(sha(backup) == item["sha256"], "JOURNAL_INVALID")
            if state in ("PREPARING", "PREPARED"):
                require(not installed and not restored and pending is None, "JOURNAL_INVALID")
            elif state == "COMMITTING":
                require(not restored and (pending is None or len(installed) < 13 and
                    pending == ORDER[len(installed)]), "JOURNAL_INVALID")
            elif state == "COMMITTED":
                require(len(installed) == 13 and not restored and pending is None, "JOURNAL_INVALID")
            elif state == "ROLLING_BACK":
                remaining = list(reversed(installed))[len(restored):]
                require(pending is None or remaining and pending == remaining[0], "JOURNAL_INVALID")
            else:  # ROLLED_BACK: every recorded installation has proven restoration.
                require(set(value["restored"]) == set(value["installed"]) and pending is None, "JOURNAL_INVALID")
            if "maintenance" in value:
                validate_maintenance(self.fs, value)
            return value
        except (KeyError, TypeError, AttributeError, IndexError, OverflowError):
            raise Failure("JOURNAL_INVALID") from None

    def _save(self, value, point):
        if "maintenance" in value and point in {"COMMITTING", "COMMITTED", "ROLLING_BACK", "ROLLED_BACK"}:
            value["maintenance"]["phase"] = {"COMMITTING": "INSTALLATION_UNCERTAIN",
                "COMMITTED": "INSTALLATION_VERIFIED", "ROLLING_BACK": "ROLLBACK_UNCERTAIN",
                "ROLLED_BACK": "RESTORATION_VERIFIED"}[point]
        if "maintenance" in value:
            validate_maintenance(self.fs, value)
        self.fs.journal(value)
        self.fault(point)

    def prepare(self, reference, expected_preflight_sha):
        authorization(reference, expected_preflight_sha)
        with self.fs.mutex():
            current = preflight(self.fs, self.source, self.consumers)
            require(sha(canonical(current)) == expected_preflight_sha, "PREFLIGHT_DRIFT")
            require(not self.fs.transaction_present(), "TRANSACTION_EXISTS")
            self.fs.mkdir_tx()  # Existing transactions stop; no adoption/resume/cleanup.
            value = dict(current, state="PREPARING", prepare_authorization=reference,
                commit_authorization=None, rollback_authorization=None,
                installed={}, restored={}, pending=None)
            self._save(value, "PREPARING")
            for index, path in enumerate(ORDER):
                if path in PRIOR:
                    before = value["baseline"][path]
                    raw = self.fs.read(path, MODES[path])
                    require(sha(raw) == before["sha256"] and self.fs.snapshot(path, MODES[path]) == before, "BACKUP_SOURCE_DRIFT")
                    self.fs.write_new(TX + "/backup-" + str(index), raw)
                    self.fault("BACKUP:" + path)
                self.fs.write_new(TX + "/stage-" + str(index), self.source[path])
                self.fault("STAGE:" + path)
            require(preflight(self.fs, self.source, self.consumers) == current, "PREPARE_DRIFT")
            value["state"] = "PREPARED"
            self._save(value, "PREPARED")
            return self.inspect()

    def commit(self, reference, expected_journal_sha):
        authorization(reference, expected_journal_sha)
        # Must be held independently across a partial failure. Native implementation
        # deliberately refuses because that property is not established on PI3.
        with self.consumers.hold(self.consumers.observe()):
            with self.fs.mutex():
                self.consumers.assert_active()
                value = self._journal()
                require(sha(canonical(value)) == expected_journal_sha and value["state"] == "PREPARED", "TRANSACTION_NOT_PREPARED")
                require(value["pending"] is None and not value["installed"], "TRANSACTION_UNCERTAIN")
                fresh = preflight(self.fs, self.source, self.consumers)
                require(all(value[k] == fresh[k] for k in fresh), "PREFLIGHT_DRIFT")
                # Verify ALL backups/stages before the first live replacement.
                for index, path in enumerate(ORDER):
                    require(self.fs.read(TX + "/stage-" + str(index)) == self.source[path], "STAGING_DRIFT")
                    if path in PRIOR:
                        require(sha(self.fs.read(TX + "/backup-" + str(index))) == value["baseline"][path]["sha256"], "BACKUP_DRIFT")
                value.update(state="COMMITTING", commit_authorization=reference)
                self._save(value, "COMMITTING")
                for index, path in enumerate(ORDER):
                    self.consumers.assert_active()
                    value["pending"] = path
                    self._save(value, "INTENT:" + path)
                    raw = self.fs.read(TX + "/stage-" + str(index))
                    require(raw == self.source[path], "STAGING_DRIFT")
                    after = self.fs.publish(path, raw, value["baseline"][path], MODES[path])
                    self.fault("AFTER_PUBLICATION:" + path)
                    value["installed"][path] = after
                    value["pending"] = None
                    self._save(value, "INSTALLED:" + path)
                self.verify(value)
                value["state"] = "COMMITTED"
                self._save(value, "COMMITTED")
                return self.inspect()

    def verify(self, value=None):
        check_sources(self.source)
        value = value or self._journal()
        require(value["pending"] is None and set(value["installed"]) == set(ORDER), "TRANSACTION_UNCERTAIN")
        for item in MANIFEST:
            path = item["path"]
            require(self.fs.snapshot(path, MODES[path]) == value["installed"][path], "INSTALLED_DRIFT")
            require(value["installed"][path]["sha256"] == item["sha256"], "INSTALLED_DRIFT")
        return {"state": value["state"], "installed_count": 13, "static_verification": "PASS",
                "execution_performed": False}

    def rollback(self, reference, expected_journal_sha):
        authorization(reference, expected_journal_sha)
        with self.consumers.hold(self.consumers.observe()):
            with self.fs.mutex():
                self.consumers.assert_active()
                value = self._journal()
                require(sha(canonical(value)) == expected_journal_sha, "JOURNAL_DRIFT")
                require(value["state"] in {"COMMITTED", "COMMITTING"} and value["pending"] is None and
                    not value["restored"], "ROLLBACK_STATE_REFUSED")
                # Every installed identity and every not-yet-installed baseline must
                # match before ANY rollback mutation. Never infer missing provenance.
                for index, path in enumerate(ORDER):
                    expected = value["installed"].get(path, value["baseline"][path])
                    require(self.fs.snapshot(path, MODES[path] if expected["exists"] else None) == expected, "ROLLBACK_DRIFT")
                    if path in value["installed"] and path in PRIOR:
                        require(sha(self.fs.read(TX + "/backup-" + str(index))) == value["baseline"][path]["sha256"], "BACKUP_DRIFT")
                value.update(state="ROLLING_BACK", rollback_authorization=reference)
                self._save(value, "ROLLING_BACK")
                for path in reversed(ORDER):
                    if path not in value["installed"]:
                        continue
                    self.consumers.assert_active()
                    value["pending"] = path
                    self._save(value, "ROLLBACK_INTENT:" + path)
                    if path in PRIOR:
                        raw = self.fs.read(TX + "/backup-" + str(ORDER.index(path)))
                        restored = self.fs.publish(path, raw, value["installed"][path], MODES[path])
                        require(restored["sha256"] == value["baseline"][path]["sha256"], "ROLLBACK_NOT_VERIFIED")
                    else:
                        self.fs.remove_installed(path, value["installed"][path], MODES[path])
                        restored = self.fs.snapshot(path)
                    value["restored"][path] = restored
                    value["pending"] = None
                    self._save(value, "RESTORED:" + path)
                for path in ORDER:
                    now = self.fs.snapshot(path, MODES[path] if path in PRIOR else None)
                    if path in PRIOR:
                        require(now["sha256"] == value["baseline"][path]["sha256"] and
                            now["identity"]["mode"] == MODES[path], "ROLLBACK_NOT_VERIFIED")
                    else:
                        require(not now["exists"], "ROLLBACK_NOT_VERIFIED")
                value["state"] = "ROLLED_BACK"
                self._save(value, "ROLLED_BACK")
                return {"state": "ROLLED_BACK", "restored_replacements": len(set(PRIOR) & set(value["installed"])),
                        "removed_new_files": len(set(value["installed"]) - set(PRIOR)),
                        "original_inode_or_ctime_restored": False}

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("preflight", "inspect", "prepare", "commit", "verify", "rollback"))
    parser.add_argument("--authorization")
    parser.add_argument("--evidence-sha256")
    args = parser.parse_args(argv)
    receipt = {"result": "FAIL_STOP", "live_mutation_state": "NOT_ATTEMPTED",
        "pe7_executed": False, "cron_mutated": False, "configuration_mutated": False}
    controller = None
    try:
        require(os.name == "posix" and socket.gethostname() == "nutandpihole" and
            os.getuid() == os.geteuid() == os.getgid() == os.getegid() == 1000, "TARGET_IDENTITY")
        fs = NativeFS()
        source = source_gate()
        consumers = NativeConsumers()
        controller = Controller(fs, source, consumers)
        if args.action == "preflight":
            result = preflight(fs, source, consumers)
            receipt.update(result="PREFLIGHT_ONLY", preflight=result, preflight_sha256=sha(canonical(result)))
        elif args.action in ("prepare", "commit", "rollback"):
            # Authorization is independently bound on every invocation.
            if args.action in ("commit", "rollback"):
                receipt["live_mutation_state"] = "UNKNOWN_UNTIL_JOURNAL_REVIEW"
            result = getattr(controller, args.action)(args.authorization, args.evidence_sha256)
            receipt.update(result="PASS", transaction=result)
        else:
            result = getattr(controller, args.action)()
            receipt.update(result="PASS", transaction=result)
    except Failure as error:
        receipt["error_code"] = error.code
    except BaseException as error:
        receipt["error_code"] = "INTERRUPTED" if isinstance(error, KeyboardInterrupt) else "IO_OR_CONTRACT_FAILURE"
    receipt["controller_sha256"] = sha(Path(__file__).read_bytes())
    receipt["native_consumer_coordination"] = "NOT_ESTABLISHED"
    receipt["stop_required"] = True
    print(json.dumps(receipt, sort_keys=True, separators=(",", ":")))
    return 0 if receipt["result"] in ("PASS", "PREFLIGHT_ONLY") else 1

if __name__ == "__main__":
    raise SystemExit(main())
