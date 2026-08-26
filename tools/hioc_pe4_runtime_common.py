#!/usr/bin/env python3
"""Shared fail-closed primitives for the governed PE-4 isolated runtime."""

from __future__ import annotations

import hashlib
import json
import os
import pathlib
import re
import stat
import subprocess
import tempfile
import threading
import secrets
import string
try:
    import fcntl
except ImportError:  # Windows repository validation; Action D itself is PI3-only.
    fcntl = None
from typing import Iterable

REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parents[1]
LOCAL_LOCK = REPOSITORY_ROOT / "requirements-pe4.lock"
SOURCE = pathlib.Path("/home/jazofv1/hioc-release-source")
RUNTIME = pathlib.Path("/home/jazofv1/hioc")
RUNTIME_ROOT = RUNTIME / "runtime/pe4"
ENVIRONMENT_ROOT = RUNTIME_ROOT / "environments"
VERSIONED_NAME = "cpython311-websockets16.1.1-lock-v1"
VERSIONED_ENVIRONMENT = ENVIRONMENT_ROOT / VERSIONED_NAME
ACTIVE_POINTER = RUNTIME_ROOT / "active"
PREVIOUS_POINTER = RUNTIME_ROOT / "previous-active"
ACTIVE_INTERPRETER = ACTIVE_POINTER / "bin/python"
CLIENT_SOURCE = SOURCE / "tools/hioc-pe4-ha-auth-capability.py"
CLIENT_TARGET = RUNTIME / "tools/hioc-pe4-ha-auth-capability.py"
LOCK_SOURCE = SOURCE / "requirements-pe4.lock"
OWNER = "jazofv1"
GROUP = "jazofv1"
PI3_HOST = "nutandpihole"
PI3_IPV4 = "192.168.100.252"
SSH_PORT = 22
SSH_KNOWN_HOSTS_NAME = "known_hosts"
SSH_IDENTITY_NAME = "id_ed25519"
SSH_KEYGEN_SHA256 = "44c6809b7bbc917f1310ba92857f983e2788e9b0015aa7896fa0362eddb6338b"
SSH_CLIENT_SHA256 = "6250fd52163fe99a0dc49403ed1b4bbef9b764bdb7bada017a93d057d9376a42"
HA_IPV4 = "192.168.100.251"
HA_PORT = 8123
WHEEL_NAME = "websockets-16.1.1-cp311-cp311-manylinux2014_aarch64.manylinux_2_17_aarch64.manylinux_2_28_aarch64.whl"
WHEEL_SIZE = 188095
WHEEL_SHA256 = "86d7f0f8bdb25d2c632b72527325e4776430fd5bc61b9118de4e2b8ddb5f5b01"
LOCK_SHA256 = "19433d53e3015157207d1af4ef07930db6f0e0d525597485384b3b7d42628e96"
WHEEL_URL = "https://files.pythonhosted.org/packages/de/09/87df740f7430ce564bd52402e9c9458d4d0459cc7d2ee29e530c8204851b/" + WHEEL_NAME
CLIENT_BLOB = "09d66b041796dd6ec2efdb88f7a71b3f99e9a27a"
CLIENT_SHA256 = "5c2886452a61185c7e7329777dbd4fa3de4da98dd4793a1a84501bc30016879e"
TRANSFER_RE = re.compile(r"^/tmp/hioc-pe4-artifact-transfer-[A-Za-z0-9]{8}$")
CONSTRUCTION_RE = re.compile(r"^\.construct-" + re.escape(VERSIONED_NAME) + r"-[A-Za-z0-9]{8}$")
ACTION_D_INPUT_RE = re.compile(r"^hioc-pe4-runtime-input-[A-Za-z0-9]{8}$")
ACTION_D_ELIGIBILITY = ".hioc-action-d-eligibility.json"
CAPABILITY_PROBE = r'''import inspect,sys
import websockets
from websockets.exceptions import InvalidStatus,PayloadTooBig
from websockets.asyncio.client import connect
assert websockets.__version__ == "16.1.1"
p=inspect.signature(connect).parameters
assert {"max_size","proxy","open_timeout","close_timeout"} <= set(p)
assert any(v.kind is inspect.Parameter.VAR_KEYWORD for v in p.values())
assert sys.prefix != sys.base_prefix
class Response: status_code=302; headers={"Location":"ws://192.168.100.251:8123/api/websocket"}
obj=object.__new__(connect); obj.uri="ws://192.168.100.251:8123/api/websocket"; obj.connection_kwargs={"sock":object()}
try: obj.process_redirect(Response())
except Exception as exc: assert "preexisting socket" in str(exc)
else: raise AssertionError("redirect accepted")
'''


class Failure(RuntimeError):
    def __init__(self, code: str, stage: str, rollback: bool = False):
        self.code, self.stage, self.rollback = code, stage, rollback
        super().__init__(code)


class OwnedDirectory:
    def __init__(self, path: pathlib.Path, fd: int, dev: int, ino: int, uid: int,
                 gid: int, mode: int, parent: "OwnedDirectory | None" = None):
        self.path, self.fd, self.dev, self.ino = path, fd, dev, ino
        self.uid, self.gid, self.mode, self.parent = uid, gid, mode, parent

    def close(self) -> None:
        if self.fd >= 0:
            os.close(self.fd)
            self.fd = -1


def _directory_token(fd: int) -> tuple[int, int, int, int, int]:
    info = os.fstat(fd)
    if not stat.S_ISDIR(info.st_mode):
        raise Failure("DIRECTORY_TYPE_INVALID", "DIRECTORY_IDENTITY")
    return info.st_dev, info.st_ino, info.st_uid, info.st_gid, stat.S_IMODE(info.st_mode)


def open_owned_directory(path: pathlib.Path, mode: int, stage: str,
                         parent: OwnedDirectory | None = None,
                         expected_uid: int | None = None,
                         expected_gid: int | None = None) -> OwnedDirectory:
    if os.name != "posix" or not hasattr(os, "O_DIRECTORY") or not hasattr(os, "O_NOFOLLOW"):
        raise Failure("POSIX_DIRECTORY_PRIMITIVES_UNAVAILABLE", stage)
    try:
        fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    except OSError:
        raise Failure("DIRECTORY_OPEN_FAILED", stage)
    try:
        dev, ino, uid, gid, actual_mode = _directory_token(fd)
        wanted_uid = os.getuid() if expected_uid is None else expected_uid
        wanted_gid = os.getgid() if expected_gid is None else expected_gid
        if uid != wanted_uid or gid != wanted_gid or actual_mode != mode:
            raise Failure("DIRECTORY_IDENTITY_MISMATCH", stage)
        if parent is not None:
            revalidate_owned_directory(parent, stage)
            child = os.stat(path.name, dir_fd=parent.fd, follow_symlinks=False)
            if (child.st_dev, child.st_ino, child.st_uid, child.st_gid,
                    stat.S_IMODE(child.st_mode)) != (dev, ino, uid, gid, actual_mode):
                raise Failure("DIRECTORY_PARENT_IDENTITY_MISMATCH", stage)
            if dev != parent.dev:
                raise Failure("DIRECTORY_MOUNT_SUBSTITUTION", stage)
        return OwnedDirectory(path, fd, dev, ino, uid, gid, actual_mode, parent)
    except Exception:
        os.close(fd)
        raise


def revalidate_owned_directory(directory: OwnedDirectory, stage: str) -> None:
    if directory.fd < 0:
        raise Failure("DIRECTORY_HANDLE_CLOSED", stage)
    if _directory_token(directory.fd) != (directory.dev, directory.ino, directory.uid,
                                           directory.gid, directory.mode):
        raise Failure("DIRECTORY_IDENTITY_LOST", stage)
    if directory.parent is not None:
        parent = directory.parent
        if _directory_token(parent.fd) != (parent.dev, parent.ino, parent.uid,
                                            parent.gid, parent.mode):
            raise Failure("DIRECTORY_PARENT_IDENTITY_LOST", stage)
        try:
            info = os.stat(directory.path.name, dir_fd=parent.fd, follow_symlinks=False)
        except OSError:
            raise Failure("DIRECTORY_NAME_LOST", stage)
        if (info.st_dev, info.st_ino, info.st_uid, info.st_gid,
                stat.S_IMODE(info.st_mode)) != (directory.dev, directory.ino,
                                                directory.uid, directory.gid,
                                                directory.mode):
            raise Failure("DIRECTORY_NAME_SUBSTITUTED", stage)


def create_owned_child(parent: OwnedDirectory, prefix: str, mode: int,
                       stage: str) -> OwnedDirectory:
    alphabet = string.ascii_letters + string.digits
    for _ in range(32):
        name = prefix + "".join(secrets.choice(alphabet) for _ in range(8))
        try:
            os.mkdir(name, mode=mode, dir_fd=parent.fd)
        except FileExistsError:
            continue
        except OSError:
            raise Failure("DIRECTORY_CREATION_FAILED", stage)
        path = parent.path / name
        try:
            fd = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                         dir_fd=parent.fd)
            os.fchmod(fd, mode)
            dev, ino, uid, gid, actual_mode = _directory_token(fd)
            if (uid, gid, actual_mode, dev) != (os.getuid(), os.getgid(), mode, parent.dev):
                raise Failure("CREATED_DIRECTORY_IDENTITY_INVALID", stage)
            child = OwnedDirectory(path, fd, dev, ino, uid, gid, actual_mode, parent)
            revalidate_owned_directory(child, stage)
            os.fsync(fd); os.fsync(parent.fd)
            return child
        except Exception:
            try: os.rmdir(name, dir_fd=parent.fd)
            except OSError: pass
            raise
    raise Failure("DIRECTORY_NAME_EXHAUSTED", stage)


def open_tmp_root(stage: str) -> OwnedDirectory:
    info = os.lstat("/tmp")
    if not stat.S_ISDIR(info.st_mode) or stat.S_ISLNK(info.st_mode):
        raise Failure("TEMP_ROOT_INVALID", stage)
    return open_owned_directory(pathlib.Path("/tmp"), stat.S_IMODE(info.st_mode), stage,
                                expected_uid=info.st_uid, expected_gid=info.st_gid)


def open_trusted_owned_parent(path: pathlib.Path, stage: str) -> OwnedDirectory:
    current = pathlib.Path(path.anchor)
    for part in path.parts[1:]:
        current /= part
        info = os.lstat(current)
        if (not stat.S_ISDIR(info.st_mode) or stat.S_ISLNK(info.st_mode)
                or info.st_uid not in (0, os.getuid()) or stat.S_IMODE(info.st_mode) & 0o022):
            raise Failure("UNSAFE_PARENT_CHAIN", stage)
    info = os.lstat(path)
    if info.st_uid != os.getuid() or info.st_gid != os.getgid():
        raise Failure("PARENT_OWNERSHIP_INVALID", stage)
    return open_owned_directory(path, stat.S_IMODE(info.st_mode), stage,
                                expected_uid=info.st_uid, expected_gid=info.st_gid)


def publish_owned_json(directory: OwnedDirectory, name: str, document: dict[str, object],
                       stage: str, mode: int = 0o600) -> str:
    revalidate_owned_directory(directory, stage)
    if "/" in name or name in ("", ".", ".."):
        raise Failure("EVIDENCE_NAME_INVALID", stage)
    payload = (json.dumps(document, sort_keys=True, separators=(",", ":")) + "\n").encode()
    if len(payload) > 65536:
        raise Failure("EVIDENCE_TOO_LARGE", stage)
    temporary = "." + name + "." + "".join(secrets.choice(string.ascii_letters)
                                                for _ in range(8))
    fd = -1
    try:
        fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                     mode, dir_fd=directory.fd)
        view = memoryview(payload)
        while view:
            written = os.write(fd, view)
            if written <= 0:
                raise Failure("EVIDENCE_WRITE_FAILED", stage)
            view = view[written:]
        os.fchmod(fd, mode); os.fsync(fd); os.close(fd); fd = -1
        os.link(temporary, name, src_dir_fd=directory.fd, dst_dir_fd=directory.fd,
                follow_symlinks=False)
        os.unlink(temporary, dir_fd=directory.fd); os.fsync(directory.fd)
        check = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory.fd)
        try:
            info = os.fstat(check)
            actual = b""
            while len(actual) <= 65536:
                block = os.read(check, 65536)
                if not block: break
                actual += block
            if (not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid()
                    or info.st_gid != os.getgid() or stat.S_IMODE(info.st_mode) != mode
                    or actual != payload):
                raise Failure("EVIDENCE_CONFIRMATION_FAILED", stage)
        finally:
            os.close(check)
        revalidate_owned_directory(directory, stage)
        return hashlib.sha256(payload).hexdigest()
    except FileExistsError:
        raise Failure("EVIDENCE_NO_REPLACE_CONFLICT", stage)
    except Failure:
        raise
    except OSError:
        raise Failure("EVIDENCE_PUBLICATION_FAILED", stage)
    finally:
        if fd >= 0: os.close(fd)
        try: os.unlink(temporary, dir_fd=directory.fd)
        except OSError: pass


def sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require_regular(path: pathlib.Path, mode: int | None = None) -> None:
    info = path.lstat()
    if path.is_symlink() or not stat.S_ISREG(info.st_mode):
        raise Failure("UNSAFE_FILE", "PATH_VALIDATION")
    if mode is not None and stat.S_IMODE(info.st_mode) != mode:
        raise Failure("UNSAFE_MODE", "PERMISSION_VALIDATION")


def require_directory(path: pathlib.Path, mode: int | None = None) -> None:
    info = path.lstat()
    if path.is_symlink() or not stat.S_ISDIR(info.st_mode):
        raise Failure("UNSAFE_DIRECTORY", "PATH_VALIDATION")
    if mode is not None and stat.S_IMODE(info.st_mode) != mode:
        raise Failure("UNSAFE_MODE", "PERMISSION_VALIDATION")
    if stat.S_IMODE(info.st_mode) & 0o022:
        raise Failure("WRITABLE_BY_GROUP_OR_WORLD", "PERMISSION_VALIDATION")


def require_owned(path: pathlib.Path) -> None:
    import grp, pwd
    info = path.lstat()
    if pwd.getpwuid(info.st_uid).pw_name != OWNER or grp.getgrgid(info.st_gid).gr_name != GROUP:
        raise Failure("OWNER_GROUP_MISMATCH", "PERMISSION_VALIDATION")


def workstation_cache_root() -> pathlib.Path:
    command = ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command",
               "[Environment]::GetFolderPath('LocalApplicationData')"]
    root = run(command, "WORKSTATION_PATH", timeout=10).stdout.strip()
    if not root or not pathlib.Path(root).is_absolute():
        raise Failure("WORKSTATION_PATH_INVALID", "WORKSTATION_PATH")
    return pathlib.Path(root) / "HIOC/artifacts/pe4"


def windows_reparse_point(path: pathlib.Path) -> bool:
    info = path.lstat()
    attributes = getattr(info, "st_file_attributes", 0)
    return path.is_symlink() or bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))


def windows_path_entry_exists(path: pathlib.Path) -> bool:
    """Detect any Windows directory entry without following a reparse target."""
    try:
        os.lstat(path)
    except FileNotFoundError:
        return False
    except OSError:
        # An unreadable or otherwise indeterminate entry is not proven absent.
        raise Failure("PATH_ENTRY_INSPECTION_FAILED", "COLLISION_CHECK")
    return True


def windows_publish_no_replace(source: pathlib.Path, destination: pathlib.Path) -> None:
    """Atomically move a Windows file while refusing every existing destination."""
    if os.name != "nt":
        raise OSError("Windows no-replace publication is unavailable")
    import ctypes
    # MoveFileEx with only WRITE_THROUGH is an atomic no-replace move.
    # WRITE_THROUGH requests completion of the move before the call returns.
    if windows_path_entry_exists(destination):
        raise FileExistsError(str(destination))
    if not ctypes.windll.kernel32.MoveFileExW(str(source), str(destination), 0x8):
        raise ctypes.WinError()


def windows_openssh_tool(name: str) -> pathlib.Path:
    """Resolve the Windows system OpenSSH client without consulting PATH."""
    if name not in {"ssh", "ssh-keygen"} or os.name != "nt":
        raise Failure("OPENSSH_TOOL_INVALID", "OPENSSH_IDENTITY")
    import ctypes
    buffer = ctypes.create_unicode_buffer(32768)
    length = ctypes.windll.kernel32.GetWindowsDirectoryW(buffer, len(buffer))
    if length == 0 or length >= len(buffer):
        raise Failure("WINDOWS_DIRECTORY_UNAVAILABLE", "OPENSSH_IDENTITY")
    candidate = pathlib.Path(buffer.value) / "System32" / "OpenSSH" / f"{name}.exe"
    if not candidate.is_absolute() or not candidate.exists() or candidate.is_symlink():
        raise Failure("OPENSSH_TOOL_MISSING", "OPENSSH_IDENTITY")
    if windows_reparse_point(candidate) or not candidate.is_file():
        raise Failure("OPENSSH_TOOL_UNSAFE", "OPENSSH_IDENTITY")
    return candidate


def windows_profile_root() -> pathlib.Path:
    """Resolve the current profile through the Windows Known Folder API."""
    if os.name != "nt":
        raise Failure("WINDOWS_PROFILE_UNAVAILABLE", "OPENSSH_IDENTITY")
    import ctypes
    buffer = ctypes.create_unicode_buffer(32768)
    # CSIDL_PROFILE is the current user's profile and does not trust environment variables.
    result = ctypes.windll.shell32.SHGetFolderPathW(None, 0x0028, None, 0, buffer)
    profile = pathlib.Path(buffer.value) if result == 0 and buffer.value else pathlib.Path()
    if not profile.is_absolute() or not profile.is_dir() or profile.is_symlink():
        raise Failure("WINDOWS_PROFILE_UNAVAILABLE", "OPENSSH_IDENTITY")
    if windows_reparse_point(profile):
        raise Failure("WINDOWS_PROFILE_UNSAFE", "OPENSSH_IDENTITY")
    return profile


def windows_openssh_material() -> tuple[pathlib.Path, pathlib.Path]:
    """Return fixed known-hosts and private-identity paths without reading secrets."""
    ssh_directory = windows_profile_root() / ".ssh"
    if (not ssh_directory.is_dir() or ssh_directory.is_symlink()
            or windows_reparse_point(ssh_directory)):
        raise Failure("OPENSSH_DIRECTORY_UNSAFE", "OPENSSH_IDENTITY")
    known_hosts = ssh_directory / SSH_KNOWN_HOSTS_NAME
    identity = ssh_directory / SSH_IDENTITY_NAME
    for path, code in ((known_hosts, "KNOWN_HOSTS_UNSAFE"),
                       (identity, "SSH_IDENTITY_UNSAFE")):
        if (not path.is_file() or path.is_symlink() or windows_reparse_point(path)
                or path.stat().st_size <= 0):
            raise Failure(code, "OPENSSH_IDENTITY")
    return known_hosts, identity


def prepare_windows_hierarchy(trusted_root: pathlib.Path, relative_parts: Iterable[str],
                              *, acl=None, reparse=None) -> pathlib.Path:
    acl = secure_workstation_path if acl is None else acl
    reparse = windows_reparse_point if reparse is None else reparse
    if not trusted_root.is_absolute() or not trusted_root.is_dir():
        raise Failure("WORKSTATION_PATH_INVALID", "WORKSTATION_PATH")
    current = trusted_root
    for part in relative_parts:
        if not re.fullmatch(r"[A-Za-z0-9._-]+", part):
            raise Failure("WORKSTATION_PATH_INVALID", "WORKSTATION_PATH")
        current = current / part
        if current.exists() or current.is_symlink():
            if reparse(current):
                raise Failure("WORKSTATION_REPARSE_POINT", "WORKSTATION_PATH")
            if not current.is_dir():
                raise Failure("WORKSTATION_PATH_NOT_DIRECTORY", "WORKSTATION_PATH")
        else:
            current.mkdir()
        acl(current, True)
    return current


def validate_windows_hierarchy(trusted_root: pathlib.Path, relative_parts: Iterable[str],
                               *, reparse=None) -> pathlib.Path:
    reparse = windows_reparse_point if reparse is None else reparse
    if not trusted_root.is_absolute() or not trusted_root.is_dir():
        raise Failure("WORKSTATION_PATH_INVALID", "WORKSTATION_PATH")
    current = trusted_root
    for part in relative_parts:
        if not re.fullmatch(r"[A-Za-z0-9._-]+", part):
            raise Failure("WORKSTATION_PATH_INVALID", "WORKSTATION_PATH")
        current = current / part
        if not current.exists() or current.is_symlink():
            raise Failure("WORKSTATION_PATH_MISSING", "WORKSTATION_PATH")
        if reparse(current):
            raise Failure("WORKSTATION_REPARSE_POINT", "WORKSTATION_PATH")
        if not current.is_dir():
            raise Failure("WORKSTATION_PATH_NOT_DIRECTORY", "WORKSTATION_PATH")
    return current


def secure_workstation_path(path: pathlib.Path, is_directory: bool) -> None:
    script = r'''$p=$env:HIOC_PE4_ACL_PATH;$isDir=$env:HIOC_PE4_ACL_IS_DIRECTORY -eq '1';$sid=[Security.Principal.WindowsIdentity]::GetCurrent().User
try{$item=if($isDir){[IO.DirectoryInfo]::new($p)}else{[IO.FileInfo]::new($p)}
    $acl=$item.GetAccessControl([Security.AccessControl.AccessControlSections]::Access)}catch{exit 11}
try{$acl.SetAccessRuleProtection($true,$false)}catch{exit 12}
try{foreach($existing in @($acl.GetAccessRules($true,$true,[Security.Principal.SecurityIdentifier]))){
        [void]$acl.RemoveAccessRuleSpecific($existing)}
    $inherit=if($isDir){[Security.AccessControl.InheritanceFlags]::ContainerInherit -bor [Security.AccessControl.InheritanceFlags]::ObjectInherit}else{[Security.AccessControl.InheritanceFlags]::None}
    $rule=New-Object Security.AccessControl.FileSystemAccessRule($sid,[Security.AccessControl.FileSystemRights]::FullControl,$inherit,[Security.AccessControl.PropagationFlags]::None,[Security.AccessControl.AccessControlType]::Allow)
    $acl.AddAccessRule($rule)}catch{exit 13}
try{$item.SetAccessControl($acl)}catch{exit 14}
try{$check=$item.GetAccessControl([Security.AccessControl.AccessControlSections]::Access)
    $rules=@($check.GetAccessRules($true,$true,[Security.Principal.SecurityIdentifier]))}catch{exit 21}
if(-not $check.AreAccessRulesProtected){exit 22}
if($rules.Count -ne 1){exit 23}
$actual=$rules[0]
if($actual.IsInherited){exit 24}
if($actual.IdentityReference.Value -ne $sid.Value){exit 25}
if($actual.AccessControlType -ne [Security.AccessControl.AccessControlType]::Allow){exit 26}
if($actual.FileSystemRights -ne [Security.AccessControl.FileSystemRights]::FullControl){exit 27}
$expectedInheritance=if($isDir){[Security.AccessControl.InheritanceFlags]::ContainerInherit -bor [Security.AccessControl.InheritanceFlags]::ObjectInherit}else{[Security.AccessControl.InheritanceFlags]::None}
if($actual.InheritanceFlags -ne $expectedInheritance){exit 28}
if($actual.PropagationFlags -ne [Security.AccessControl.PropagationFlags]::None){exit 29}'''
    environment = os.environ.copy()
    environment["HIOC_PE4_ACL_PATH"] = str(path)
    environment["HIOC_PE4_ACL_IS_DIRECTORY"] = "1" if is_directory else "0"
    run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", script],
        "WORKSTATION_ACL", timeout=15, failure_codes={
            11: "WORKSTATION_ACL_READ_FAILED",
            12: "WORKSTATION_ACL_PROTECTION_FAILED",
            13: "WORKSTATION_ACL_RULE_UPDATE_FAILED",
            14: "WORKSTATION_ACL_APPLICATION_FAILED",
            21: "WORKSTATION_ACL_VALIDATION_READ_FAILED",
            22: "WORKSTATION_ACL_NOT_PROTECTED",
            23: "WORKSTATION_ACL_RULE_COUNT_INVALID",
            24: "WORKSTATION_ACL_INHERITED_RULE_REMAINS",
            25: "WORKSTATION_ACL_IDENTITY_INVALID",
            26: "WORKSTATION_ACL_RULE_TYPE_INVALID",
            27: "WORKSTATION_ACL_RIGHTS_INVALID",
            28: "WORKSTATION_ACL_INHERITANCE_INVALID",
            29: "WORKSTATION_ACL_PROPAGATION_INVALID",
        }, env=environment)


def secure_workstation_directory(path: pathlib.Path) -> None:
    secure_workstation_path(path, True)


def validate_workstation_path_acl(path: pathlib.Path, is_directory: bool) -> None:
    script = r'''$p=$env:HIOC_PE4_ACL_PATH;$isDir=$env:HIOC_PE4_ACL_IS_DIRECTORY -eq '1';$sid=[Security.Principal.WindowsIdentity]::GetCurrent().User
try{$item=if($isDir){[IO.DirectoryInfo]::new($p)}else{[IO.FileInfo]::new($p)}
    $acl=$item.GetAccessControl([Security.AccessControl.AccessControlSections]::Access)
    $rules=@($acl.GetAccessRules($true,$true,[Security.Principal.SecurityIdentifier]))}catch{exit 21}
if(-not $acl.AreAccessRulesProtected){exit 22}
if($rules.Count -ne 1){exit 23}
$actual=$rules[0]
if($actual.IsInherited){exit 24}
if($actual.IdentityReference.Value -ne $sid.Value){exit 25}
if($actual.AccessControlType -ne [Security.AccessControl.AccessControlType]::Allow){exit 26}
if($actual.FileSystemRights -ne [Security.AccessControl.FileSystemRights]::FullControl){exit 27}
$expectedInheritance=if($isDir){[Security.AccessControl.InheritanceFlags]::ContainerInherit -bor [Security.AccessControl.InheritanceFlags]::ObjectInherit}else{[Security.AccessControl.InheritanceFlags]::None}
if($actual.InheritanceFlags -ne $expectedInheritance){exit 28}
if($actual.PropagationFlags -ne [Security.AccessControl.PropagationFlags]::None){exit 29}'''
    environment = os.environ.copy()
    environment["HIOC_PE4_ACL_PATH"] = str(path)
    environment["HIOC_PE4_ACL_IS_DIRECTORY"] = "1" if is_directory else "0"
    run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", script],
        "WORKSTATION_ACL", timeout=15, failure_codes={
            21: "WORKSTATION_ACL_VALIDATION_READ_FAILED",
            22: "WORKSTATION_ACL_NOT_PROTECTED",
            23: "WORKSTATION_ACL_RULE_COUNT_INVALID",
            24: "WORKSTATION_ACL_INHERITED_RULE_REMAINS",
            25: "WORKSTATION_ACL_IDENTITY_INVALID",
            26: "WORKSTATION_ACL_RULE_TYPE_INVALID",
            27: "WORKSTATION_ACL_RIGHTS_INVALID",
            28: "WORKSTATION_ACL_INHERITANCE_INVALID",
            29: "WORKSTATION_ACL_PROPAGATION_INVALID",
        }, env=environment)


WINDOWS_SYSTEM_SID = "S-1-5-18"
WINDOWS_ADMINISTRATORS_SID = "S-1-5-32-544"
WINDOWS_FULL_CONTROL = 2032127
WINDOWS_MODIFY_SYNCHRONIZE = 1245631


def validate_windows_ssh_acl_policy(role: str, metadata: dict) -> None:
    """Validate sanitized Windows SSH ACL metadata without changing the ACL."""
    if role not in {"directory", "known_hosts", "key"} or not isinstance(metadata, dict):
        raise Failure("SSH_ACL_METADATA_INVALID", "OPENSSH_IDENTITY")
    current = metadata.get("current_sid")
    owner = metadata.get("owner_sid")
    rules = metadata.get("rules")
    if (not isinstance(current, str) or not current.startswith("S-")
            or not isinstance(owner, str) or not isinstance(rules, list)
            or not isinstance(metadata.get("protected"), bool)
            or not isinstance(metadata.get("is_directory"), bool)
            or not isinstance(metadata.get("reparse"), bool) or len(rules) > 8):
        raise Failure("SSH_ACL_METADATA_INVALID", "OPENSSH_IDENTITY")
    expected_directory = role == "directory"
    if metadata["is_directory"] != expected_directory:
        raise Failure("SSH_ACL_OBJECT_TYPE_INVALID", "OPENSSH_IDENTITY")
    if metadata["reparse"]:
        raise Failure("SSH_ACL_REPARSE_POINT", "OPENSSH_IDENTITY")
    if role == "directory":
        allowed_owners = {current, WINDOWS_ADMINISTRATORS_SID}
        expected_protected = False
        expected = {
            current: (WINDOWS_FULL_CONTROL, True, 3),
            WINDOWS_SYSTEM_SID: (WINDOWS_FULL_CONTROL, True, 3),
            WINDOWS_ADMINISTRATORS_SID: (WINDOWS_FULL_CONTROL, True, 3),
        }
    elif role == "known_hosts":
        allowed_owners = {current}
        expected_protected = True
        expected = {
            current: (WINDOWS_MODIFY_SYNCHRONIZE, False, 0),
            WINDOWS_SYSTEM_SID: (WINDOWS_FULL_CONTROL, False, 0),
            WINDOWS_ADMINISTRATORS_SID: (WINDOWS_FULL_CONTROL, False, 0),
        }
    else:
        allowed_owners = {current}
        expected_protected = True
        expected = {current: (WINDOWS_FULL_CONTROL, False, 0)}
    if owner not in allowed_owners:
        raise Failure("SSH_ACL_OWNER_INVALID", "OPENSSH_IDENTITY")
    if metadata["protected"] != expected_protected:
        raise Failure("SSH_ACL_PROTECTION_INVALID", "OPENSSH_IDENTITY")
    if len(rules) != len(expected):
        raise Failure("SSH_ACL_RULE_COUNT_INVALID", "OPENSSH_IDENTITY")
    seen = set()
    for rule in rules:
        if not isinstance(rule, dict) or set(rule) != {
                "sid", "allow", "rights", "inherited", "inheritance", "propagation"}:
            raise Failure("SSH_ACL_RULE_INVALID", "OPENSSH_IDENTITY")
        sid = rule.get("sid")
        if sid not in expected or sid in seen:
            raise Failure("SSH_ACL_PRINCIPAL_INVALID", "OPENSSH_IDENTITY")
        seen.add(sid)
        if rule.get("allow") is not True:
            raise Failure("SSH_ACL_DENY_RULE", "OPENSSH_IDENTITY")
        rights, inherited, inheritance = expected[sid]
        if rule.get("rights") != rights:
            raise Failure("SSH_ACL_RIGHTS_INVALID", "OPENSSH_IDENTITY")
        if rule.get("inherited") is not inherited:
            raise Failure("SSH_ACL_INHERITED_STATE_INVALID", "OPENSSH_IDENTITY")
        if rule.get("inheritance") != inheritance:
            raise Failure("SSH_ACL_INHERITANCE_INVALID", "OPENSSH_IDENTITY")
        if rule.get("propagation") != 0:
            raise Failure("SSH_ACL_PROPAGATION_INVALID", "OPENSSH_IDENTITY")


def validate_windows_ssh_acl(path: pathlib.Path, role: str, *, runner=None) -> None:
    """Read bounded, SID-only ACL metadata and apply the role-specific policy."""
    script = r'''$p=$env:HIOC_PE4_ACL_PATH
try {
  $attributes=[IO.File]::GetAttributes($p)
  $isDirectory=($attributes -band [IO.FileAttributes]::Directory) -ne 0
  $reparse=($attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0
  $item=if($isDirectory){[IO.DirectoryInfo]::new($p)}else{[IO.FileInfo]::new($p)}
  $section=[Security.AccessControl.AccessControlSections]::Owner -bor [Security.AccessControl.AccessControlSections]::Access
  $acl=$item.GetAccessControl($section)
  $current=[Security.Principal.WindowsIdentity]::GetCurrent().User.Value
  $owner=$acl.GetOwner([Security.Principal.SecurityIdentifier]).Value
  $rules=@($acl.GetAccessRules($true,$true,[Security.Principal.SecurityIdentifier]) | ForEach-Object {
    [ordered]@{sid=$_.IdentityReference.Value;allow=$_.AccessControlType -eq [Security.AccessControl.AccessControlType]::Allow;rights=[int]$_.FileSystemRights;inherited=[bool]$_.IsInherited;inheritance=[int]$_.InheritanceFlags;propagation=[int]$_.PropagationFlags}
  })
  [ordered]@{current_sid=$current;owner_sid=$owner;protected=[bool]$acl.AreAccessRulesProtected;is_directory=[bool]$isDirectory;reparse=[bool]$reparse;rules=$rules} | ConvertTo-Json -Compress -Depth 4
} catch { exit 31 }'''
    runner = run_bounded if runner is None else runner
    environment = os.environ.copy()
    environment["HIOC_PE4_ACL_PATH"] = str(path)
    result = runner(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", script],
                    "OPENSSH_IDENTITY", timeout=15, max_output=16384,
                    failure_codes={31: "SSH_ACL_READ_FAILED"}, env=environment)
    if len(result.stdout) > 16384:
        raise Failure("SSH_ACL_METADATA_INVALID", "OPENSSH_IDENTITY")
    try:
        metadata = json.loads(result.stdout)
    except (TypeError, json.JSONDecodeError):
        raise Failure("SSH_ACL_METADATA_INVALID", "OPENSSH_IDENTITY")
    validate_windows_ssh_acl_policy(role, metadata)


def validate_windows_ssh_directory_acl(path: pathlib.Path) -> None:
    validate_windows_ssh_acl(path, "directory")


def validate_windows_known_hosts_acl(path: pathlib.Path) -> None:
    validate_windows_ssh_acl(path, "known_hosts")


def validate_windows_ssh_key_acl(path: pathlib.Path) -> None:
    validate_windows_ssh_acl(path, "key")


def verify_pi3() -> None:
    import getpass, socket
    if socket.gethostname().split(".", 1)[0] != PI3_HOST or getpass.getuser() != OWNER:
        raise Failure("WRONG_TARGET_OR_OPERATOR", "TARGET_IDENTITY")
    addresses = run(["ip", "-o", "-4", "addr", "show", "scope", "global"], "TARGET_IDENTITY").stdout
    if not re.search(r"\binet\s+" + re.escape(PI3_IPV4) + r"/", addresses):
        raise Failure("WRONG_TARGET", "TARGET_IDENTITY")


def validate_wheel(path: pathlib.Path) -> None:
    if path.name != WHEEL_NAME:
        raise Failure("ARTIFACT_FILENAME_MISMATCH", "ARTIFACT_IDENTITY")
    require_regular(path, 0o600)
    if path.stat().st_size != WHEEL_SIZE:
        raise Failure("ARTIFACT_SIZE_MISMATCH", "ARTIFACT_IDENTITY")
    if sha256(path) != WHEEL_SHA256:
        raise Failure("ARTIFACT_SHA256_MISMATCH", "ARTIFACT_IDENTITY")


def validate_transfer_directory(value: str) -> pathlib.Path:
    if not TRANSFER_RE.fullmatch(value):
        raise Failure("TRANSFER_PATH_INVALID", "INPUT_VALIDATION")
    path = pathlib.Path(value)
    require_directory(path, 0o700)
    require_owned(path)
    validate_wheel(path / WHEEL_NAME)
    require_regular(path / "requirements-pe4.lock", 0o600)
    if sha256(path / "requirements-pe4.lock") != LOCK_SHA256:
        raise Failure("LOCK_IDENTITY_MISMATCH", "ARTIFACT_IDENTITY")
    return path


def _copy_exact_file(source_fd: int, destination_fd: int, name: str, size: int,
                     digest: str, source_mode: int = 0o600) -> None:
    try:
        src = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=source_fd)
    except OSError:
        raise Failure("TRANSFER_FILE_OPEN_FAILED", "INPUT_SNAPSHOT")
    try:
        before = os.fstat(src)
        if (not stat.S_ISREG(before.st_mode) or before.st_uid != os.getuid()
                or before.st_gid != os.getgid()
                or stat.S_IMODE(before.st_mode) != source_mode or before.st_size != size):
            raise Failure("TRANSFER_FILE_IDENTITY_INVALID", "INPUT_SNAPSHOT")
        try:
            dst = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                          0o400, dir_fd=destination_fd)
        except OSError:
            raise Failure("SNAPSHOT_FILE_CREATION_FAILED", "INPUT_SNAPSHOT")
        calculated = hashlib.sha256(); total = 0
        try:
            while True:
                block = os.read(src, 65536)
                if not block: break
                total += len(block)
                if total > size:
                    raise Failure("TRANSFER_FILE_SIZE_MISMATCH", "INPUT_SNAPSHOT")
                calculated.update(block)
                view = memoryview(block)
                while view:
                    written = os.write(dst, view)
                    if written <= 0:
                        raise Failure("SNAPSHOT_FILE_WRITE_FAILED", "INPUT_SNAPSHOT")
                    view = view[written:]
            os.fchmod(dst, 0o400); os.fsync(dst)
            after = os.fstat(src)
            if (before.st_dev, before.st_ino, before.st_uid, before.st_gid,
                    before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (
                    after.st_dev, after.st_ino, after.st_uid, after.st_gid,
                    after.st_size, after.st_mtime_ns, after.st_ctime_ns):
                raise Failure("TRANSFER_FILE_MUTATED", "INPUT_SNAPSHOT")
            if total != size or calculated.hexdigest() != digest:
                raise Failure("TRANSFER_FILE_DIGEST_MISMATCH", "INPUT_SNAPSHOT")
        finally:
            os.close(dst)
    finally:
        os.close(src)


def validate_action_b_result(directory: OwnedDirectory) -> None:
    try:
        fd = os.open("result.json", os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory.fd)
    except OSError:
        raise Failure("ACTION_B_EVIDENCE_OPEN_FAILED", "INPUT_SNAPSHOT")
    try:
        info = os.fstat(fd)
        payload = b""
        while len(payload) <= 65536:
            block = os.read(fd, 65536)
            if not block: break
            payload += block
        after = os.fstat(fd)
        if (not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid()
                or info.st_gid != os.getgid() or stat.S_IMODE(info.st_mode) != 0o600
                or len(payload) > 65536 or (info.st_dev, info.st_ino, info.st_size,
                info.st_mtime_ns, info.st_ctime_ns) != (after.st_dev, after.st_ino,
                after.st_size, after.st_mtime_ns, after.st_ctime_ns)):
            raise Failure("ACTION_B_EVIDENCE_IDENTITY_INVALID", "INPUT_SNAPSHOT")
        document = json.loads(payload)
    except (UnicodeError, ValueError, json.JSONDecodeError):
        raise Failure("ACTION_B_EVIDENCE_INVALID", "INPUT_SNAPSHOT")
    finally:
        os.close(fd)
    true_fields = ("remote_staging_created", "wheel_transferred", "lock_transferred",
                   "remote_artifact_verified", "remote_lock_verified")
    expected_fields = {"schema_version", "action", *true_fields, "evidence_state",
                       "result", "error_code", "failure_stage", "rollback_recommended"}
    if (set(document) != expected_fields or document.get("schema_version") != "1.0"
            or document.get("action") != "PE-4.0B.2a-B"
            or document.get("result") != "PASS" or document.get("error_code") != "NONE"
            or document.get("failure_stage") != "COMPLETE"
            or document.get("rollback_recommended") is not False
            or document.get("evidence_state") != "AWAITING_CONFIRMATION"
            or any(document.get(name) is not True for name in true_fields)):
        raise Failure("ACTION_B_EVIDENCE_MISMATCH", "INPUT_SNAPSHOT")


def create_action_d_input_snapshot(value: str) -> OwnedDirectory:
    if not TRANSFER_RE.fullmatch(value):
        raise Failure("TRANSFER_PATH_INVALID", "INPUT_VALIDATION")
    transfer = open_owned_directory(pathlib.Path(value), 0o700, "TRANSFER_IDENTITY")
    tmp_root = open_tmp_root("SNAPSHOT_ROOT")
    snapshot = None
    try:
        names = sorted(os.listdir(transfer.fd))
        expected = sorted((WHEEL_NAME, "requirements-pe4.lock", "result.json"))
        if names != expected:
            raise Failure("TRANSFER_CONTENT_SET_INVALID", "INPUT_SNAPSHOT")
        validate_action_b_result(transfer)
        snapshot = create_owned_child(tmp_root, "hioc-pe4-runtime-input-", 0o700,
                                      "INPUT_SNAPSHOT")
        _copy_exact_file(transfer.fd, snapshot.fd, WHEEL_NAME, WHEEL_SIZE, WHEEL_SHA256)
        lock_size = os.stat("requirements-pe4.lock", dir_fd=transfer.fd,
                            follow_symlinks=False).st_size
        _copy_exact_file(transfer.fd, snapshot.fd, "requirements-pe4.lock",
                         lock_size, LOCK_SHA256)
        os.fsync(snapshot.fd)
        revalidate_owned_directory(transfer, "INPUT_SNAPSHOT")
        revalidate_owned_directory(snapshot, "INPUT_SNAPSHOT")
        return snapshot
    except Exception:
        if snapshot is not None:
            try:
                cleanup_owned_directory(snapshot, "SNAPSHOT_CLEANUP")
                snapshot = None
            except Exception: pass
        raise
    finally:
        transfer.close()
        if snapshot is None:
            tmp_root.close()


def sealed_snapshot_file(directory: OwnedDirectory, name: str, size: int,
                         digest: str) -> int:
    if not hasattr(os, "memfd_create") or fcntl is None:
        raise Failure("SEALED_INPUT_UNAVAILABLE", "INPUT_SNAPSHOT")
    source = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory.fd)
    sealed = os.memfd_create("hioc-pe4-action-d-input", os.MFD_CLOEXEC | os.MFD_ALLOW_SEALING)
    try:
        calculated = hashlib.sha256(); total = 0
        while True:
            block = os.read(source, 65536)
            if not block: break
            total += len(block); calculated.update(block)
            view = memoryview(block)
            while view:
                written = os.write(sealed, view)
                if written <= 0: raise Failure("SEALED_INPUT_WRITE_FAILED", "INPUT_SNAPSHOT")
                view = view[written:]
        if total != size or calculated.hexdigest() != digest:
            raise Failure("SEALED_INPUT_IDENTITY_MISMATCH", "INPUT_SNAPSHOT")
        os.lseek(sealed, 0, os.SEEK_SET)
        seals = fcntl.F_SEAL_SEAL | fcntl.F_SEAL_SHRINK | fcntl.F_SEAL_GROW | fcntl.F_SEAL_WRITE
        fcntl.fcntl(sealed, fcntl.F_ADD_SEALS, seals)
        if fcntl.fcntl(sealed, fcntl.F_GET_SEALS) != seals:
            raise Failure("SEALED_INPUT_CONFIRMATION_FAILED", "INPUT_SNAPSHOT")
        return sealed
    except Exception:
        os.close(sealed)
        raise
    finally:
        os.close(source)


def validate_construction(value: str) -> pathlib.Path:
    path = pathlib.Path(value)
    if path.parent != ENVIRONMENT_ROOT or not CONSTRUCTION_RE.fullmatch(path.name):
        raise Failure("CONSTRUCTION_PATH_INVALID", "INPUT_VALIDATION")
    require_directory(path, 0o750)
    require_owned(path)
    return path


def _read_owned_json_fd(directory: OwnedDirectory, name: str, mode: int,
                        stage: str) -> tuple[dict[str, object], bytes]:
    try:
        fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory.fd)
    except OSError:
        raise Failure("GOVERNED_JSON_OPEN_FAILED", stage)
    try:
        before = os.fstat(fd); raw = b""
        while len(raw) <= 65536:
            block = os.read(fd, 65536)
            if not block: break
            raw += block
        after = os.fstat(fd)
        if (not stat.S_ISREG(before.st_mode) or before.st_uid != os.getuid()
                or before.st_gid != os.getgid() or stat.S_IMODE(before.st_mode) != mode
                or len(raw) > 65536 or (before.st_dev, before.st_ino, before.st_size,
                before.st_mtime_ns, before.st_ctime_ns) != (after.st_dev, after.st_ino,
                after.st_size, after.st_mtime_ns, after.st_ctime_ns)):
            raise Failure("GOVERNED_JSON_IDENTITY_INVALID", stage)
        document = json.loads(raw)
    except (UnicodeError, ValueError, json.JSONDecodeError):
        raise Failure("GOVERNED_JSON_INVALID", stage)
    finally:
        os.close(fd)
    return document, raw


def validate_action_d_eligibility(root: OwnedDirectory, governance_commit: str) -> dict[str, object]:
    document, _ = _read_owned_json_fd(root, ACTION_D_ELIGIBILITY, 0o400,
                                      "ACTION_D_ELIGIBILITY")
    required = {
        "schema_version", "action", "governance_commit", "construction_directory",
        "environment_identity", "wheel_sha256", "lock_sha256", "evidence_directory",
        "evidence_sha256", "result",
    }
    if (set(document) != required or document.get("schema_version") != "1.0"
            or document.get("action") != "PE-4.0B.2a-D"
            or document.get("governance_commit") != governance_commit
            or document.get("construction_directory") != str(root.path)
            or document.get("environment_identity") != VERSIONED_NAME
            or document.get("wheel_sha256") != WHEEL_SHA256
            or document.get("lock_sha256") != LOCK_SHA256
            or document.get("result") != "PASS"):
        raise Failure("ACTION_D_ELIGIBILITY_MISMATCH", "ACTION_D_ELIGIBILITY")
    evidence_value = document.get("evidence_directory")
    if not isinstance(evidence_value, str) or not re.fullmatch(
            r"/tmp/hioc-pe4-runtime-construct-[A-Za-z0-9]{8}", evidence_value):
        raise Failure("ACTION_D_EVIDENCE_PATH_INVALID", "ACTION_D_ELIGIBILITY")
    evidence = open_owned_directory(pathlib.Path(evidence_value), 0o700,
                                    "ACTION_D_ELIGIBILITY")
    try:
        evidence_doc, payload = _read_owned_json_fd(evidence, "result.json", 0o600,
                                                    "ACTION_D_ELIGIBILITY")
    finally:
        evidence.close()
    if hashlib.sha256(payload).hexdigest() != document.get("evidence_sha256"):
        raise Failure("ACTION_D_EVIDENCE_DIGEST_MISMATCH", "ACTION_D_ELIGIBILITY")
    if (evidence_doc.get("action") != "PE-4.0B.2a-D"
            or evidence_doc.get("result") != "PASS"
            or evidence_doc.get("governance_commit") != governance_commit
            or evidence_doc.get("construction_directory") != str(root.path)
            or evidence_doc.get("eligibility_state") != "AWAITING_CONFIRMATION"):
        raise Failure("ACTION_D_EVIDENCE_MISMATCH", "ACTION_D_ELIGIBILITY")
    return document


def validated_active_target() -> pathlib.Path:
    if not ACTIVE_POINTER.is_symlink():
        raise Failure("ACTIVE_POINTER_INVALID", "ACTIVE_POINTER")
    raw = pathlib.Path(os.readlink(ACTIVE_POINTER))
    if raw.is_absolute() or len(raw.parts) != 2 or raw.parts[0] != "environments":
        raise Failure("ACTIVE_POINTER_TARGET_INVALID", "ACTIVE_POINTER")
    candidate = ENVIRONMENT_ROOT / raw.parts[1]
    require_directory(candidate, 0o750); require_owned(candidate)
    return candidate


def run(command: list[str], stage: str, *, timeout: int = 60, capture: bool = True,
        failure_codes: dict[int, str] | None = None,
        env: dict[str, str] | None = None, cwd: str | None = None,
        pass_fds: tuple[int, ...] = ()) -> subprocess.CompletedProcess[str]:
    try:
        result = subprocess.run(command, text=True, capture_output=capture, timeout=timeout,
                                check=False, env=env, cwd=cwd, pass_fds=pass_fds)
    except (OSError, subprocess.TimeoutExpired):
        raise Failure("COMMAND_INVOCATION_FAILED", stage)
    if result.returncode != 0:
        raise Failure((failure_codes or {}).get(result.returncode, "COMMAND_FAILED"), stage)
    return result


def run_bounded(command: list[str], stage: str, *, timeout: int,
                max_output: int = 65536,
                failure_codes: dict[int, str] | None = None,
                stdin_path: pathlib.Path | None = None,
                env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    source = None
    try:
        source = stdin_path.open("rb") if stdin_path is not None else subprocess.DEVNULL
        process = subprocess.Popen(command, stdin=source, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, env=env)
    except OSError:
        if source not in (None, subprocess.DEVNULL): source.close()
        raise Failure("COMMAND_INVOCATION_FAILED", stage)
    chunks: list[list[bytes]] = [[], []]
    total = 0
    lock = threading.Lock()
    overflow = threading.Event()

    def collect(stream, target: list[bytes]) -> None:
        nonlocal total
        while True:
            block = stream.read(4096)
            if not block:
                return
            with lock:
                remaining = max_output - total
                if remaining > 0:
                    target.append(block[:remaining])
                total += len(block)
                if total > max_output:
                    overflow.set()
                    try:
                        process.kill()
                    except OSError:
                        pass

    readers = [threading.Thread(target=collect, args=(process.stdout, chunks[0]), daemon=True),
               threading.Thread(target=collect, args=(process.stderr, chunks[1]), daemon=True)]
    for reader in readers:
        reader.start()
    timed_out = False
    try:
        returncode = process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        process.kill()
        returncode = process.wait()
    for reader in readers:
        reader.join()
    process.stdout.close()
    process.stderr.close()
    if source not in (None, subprocess.DEVNULL): source.close()
    stdout = b"".join(chunks[0]).decode("utf-8", "replace")
    stderr = b"".join(chunks[1]).decode("utf-8", "replace")
    if timed_out:
        raise Failure("COMMAND_TIMEOUT", stage)
    if overflow.is_set():
        raise Failure("COMMAND_OUTPUT_TOO_LARGE", stage)
    if returncode != 0:
        raise Failure((failure_codes or {}).get(returncode, "COMMAND_FAILED"), stage)
    return subprocess.CompletedProcess(command, returncode, stdout, stderr)


def write_evidence(directory: pathlib.Path, action: str, fields: dict[str, object], result: str,
                   code: str = "NONE", stage: str = "COMPLETE", rollback: bool = False) -> None:
    require_directory(directory, 0o700)
    allowed = {
        "ACTION", "TARGET_IDENTITY", "ARTIFACT_FILENAME", "ARTIFACT_SIZE",
        "APPROVED_SHA256", "ACTUAL_SHA256", "ENVIRONMENT_IDENTITY", "CLIENT_BLOB",
        "CLIENT_SHA256", "OWNER_GROUP", "MODE_VALIDATION", "INSTALLED_VERSION",
        "CAPABILITY_VALIDATION", "PREVIOUS_ACTIVE_TARGET", "ACTIVE_TARGET",
        "TRANSFER_DIRECTORY", "CONSTRUCTION_DIRECTORY", "PREFLIGHT",
    }
    if not set(fields).issubset(allowed):
        raise Failure("UNSAFE_EVIDENCE_FIELD", "EVIDENCE_PUBLICATION")
    document = {"schema_version": "1.0", "action": action, **fields,
                "result": result, "error_code": code, "failure_stage": stage,
                "rollback_recommended": rollback}
    payload = (json.dumps(document, sort_keys=True, separators=(",", ":")) + "\n").encode()
    temp = directory / ".result.tmp"
    fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as handle:
        handle.write(payload); handle.flush(); os.fsync(handle.fileno())
    os.replace(temp, directory / "result.json")
    dirfd = os.open(directory, os.O_RDONLY)
    try: os.fsync(dirfd)
    finally: os.close(dirfd)


def evidence_directory(prefix: str) -> pathlib.Path:
    path = pathlib.Path(tempfile.mkdtemp(prefix=prefix, dir="/tmp"))
    os.chmod(path, 0o700)
    return path


def atomic_private_text(path: pathlib.Path, value: str) -> None:
    temp = path.parent / ("." + path.name + ".tmp")
    if temp.exists() or temp.is_symlink():
        raise Failure("PRIVATE_TEXT_TEMP_EXISTS", "PUBLICATION")
    fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="ascii", newline="\n") as handle:
        handle.write(value + "\n"); handle.flush(); os.fsync(handle.fileno())
    os.replace(temp, path)
    dirfd = os.open(path.parent, os.O_RDONLY)
    try: os.fsync(dirfd)
    finally: os.close(dirfd)


def terminal(result: str, code: str, stage: str, rollback: bool, evidence: pathlib.Path | None = None) -> None:
    print(f"RESULT={result}")
    print(f"ERROR_CODE={code}")
    print(f"FAILURE_STAGE={stage}")
    print(f"ROLLBACK_RECOMMENDED={'TRUE' if rollback else 'FALSE'}")
    if evidence is not None: print(f"EVIDENCE_DIR={evidence}")


def verify_repository(root: pathlib.Path, governance_commit: str, relatives: Iterable[str]) -> None:
    if not re.fullmatch(r"[0-9a-f]{40}", governance_commit):
        raise Failure("INVALID_GOVERNANCE_COMMIT", "SOURCE_IDENTITY")
    for expected, command in (
        (governance_commit, ["git", "-C", str(root), "rev-parse", "HEAD"]),
        (governance_commit, ["git", "-C", str(root), "rev-parse", "origin/main"]),
        ("main", ["git", "-C", str(root), "branch", "--show-current"]),
    ):
        if run(command, "SOURCE_IDENTITY").stdout.strip() != expected:
            raise Failure("SOURCE_IDENTITY_MISMATCH", "SOURCE_IDENTITY")
    if run(["git", "-C", str(root), "status", "--porcelain"], "SOURCE_IDENTITY").stdout:
        raise Failure("SOURCE_REPOSITORY_DIRTY", "SOURCE_IDENTITY")
    for relative in relatives:
        expected = run(["git", "-C", str(root), "rev-parse", f"{governance_commit}:{relative}"], "SOURCE_IDENTITY").stdout.strip()
        actual = run(["git", "-C", str(root), "hash-object", "--path", relative, str(root / relative)], "SOURCE_IDENTITY").stdout.strip()
        if expected != actual:
            raise Failure("SOURCE_WORKTREE_IDENTITY_MISMATCH", "SOURCE_IDENTITY")


def verify_client_source(governance_commit: str, tool_relative: str) -> None:
    verify_repository(SOURCE, governance_commit, (tool_relative, "tools/hioc_pe4_runtime_common.py", "tools/hioc-pe4-ha-auth-capability.py", "requirements-pe4.lock"))
    blob = run(["git", "-C", str(SOURCE), "rev-parse", f"{governance_commit}:tools/hioc-pe4-ha-auth-capability.py"], "CLIENT_IDENTITY").stdout.strip()
    if blob != CLIENT_BLOB or sha256(CLIENT_SOURCE) != CLIENT_SHA256:
        raise Failure("CLIENT_IDENTITY_MISMATCH", "CLIENT_IDENTITY")


def exact_distribution_set(python: pathlib.Path, *, cwd: str | None = None,
                           pass_fds: tuple[int, ...] = (), env: dict[str, str] | None = None) -> dict[str, str]:
    code = "import importlib.metadata as m;print('\\n'.join(sorted(d.metadata['Name'].lower()+'=='+d.version for d in m.distributions())))"
    names = run([str(python), "-I", "-c", code], "DEPENDENCY_IDENTITY",
                cwd=cwd, pass_fds=pass_fds, env=env).stdout.splitlines()
    allowed = {"pip", "setuptools", "websockets"}
    pairs = [line.split("==", 1) for line in names if line.count("==") == 1]
    parsed = [pair[0] for pair in pairs]
    if (len(pairs) != len(names) or "websockets==16.1.1" not in names
            or set(parsed) - allowed or parsed.count("websockets") != 1
            or parsed.count("pip") != 1 or parsed.count("setuptools") > 1
            or len(parsed) != len(set(parsed))
            or any(not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9.!+_-]{0,63}", version)
                   for _, version in pairs)):
        raise Failure("INSTALLED_DISTRIBUTION_SET_INVALID", "DEPENDENCY_IDENTITY")
    return dict(pairs)


def _remove_tree_fd(fd: int, root_dev: int, stage: str) -> None:
    for name in os.listdir(fd):
        info = os.stat(name, dir_fd=fd, follow_symlinks=False)
        if stat.S_ISDIR(info.st_mode):
            if info.st_dev != root_dev:
                raise Failure("CLEANUP_MOUNT_POINT", stage)
            child = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            try: _remove_tree_fd(child, root_dev, stage)
            finally: os.close(child)
            os.rmdir(name, dir_fd=fd)
        else:
            os.unlink(name, dir_fd=fd)
    os.fsync(fd)


def _refuse_active_construction(directory: OwnedDirectory, stage: str) -> None:
    if directory.parent is None or directory.parent.path != ENVIRONMENT_ROOT:
        return
    try:
        info = os.lstat(ACTIVE_POINTER)
    except FileNotFoundError:
        return
    except OSError:
        raise Failure("ACTIVE_POINTER_UNVERIFIABLE", stage)
    if not stat.S_ISLNK(info.st_mode):
        raise Failure("ACTIVE_POINTER_INVALID", stage)
    try:
        target = pathlib.Path(os.readlink(ACTIVE_POINTER))
    except OSError:
        raise Failure("ACTIVE_POINTER_UNVERIFIABLE", stage)
    if target == pathlib.Path("environments") / directory.path.name:
        raise Failure("CONSTRUCTION_IS_ACTIVE", stage)


def cleanup_owned_directory(directory: OwnedDirectory, stage: str = "CLEANUP") -> None:
    try:
        revalidate_owned_directory(directory, stage)
        _refuse_active_construction(directory, stage)
        if directory.parent is None:
            raise Failure("CLEANUP_PARENT_UNAVAILABLE", stage)
        _remove_tree_fd(directory.fd, directory.dev, stage)
        revalidate_owned_directory(directory, stage)
        _refuse_active_construction(directory, stage)
        os.rmdir(directory.path.name, dir_fd=directory.parent.fd)
        os.fsync(directory.parent.fd)
        directory.close()
    except Failure:
        raise
    except OSError:
        raise Failure("CLEANUP_FAILED", stage)


def validate_venv_symlinks(directory: OwnedDirectory) -> None:
    base = pathlib.Path(f"/proc/self/fd/{directory.fd}")
    for root, dirs, files in os.walk(base, followlinks=False):
        for name in dirs + files:
            path = pathlib.Path(root) / name
            if path.is_symlink():
                relative = path.relative_to(base).as_posix()
                if relative != "lib64" or os.readlink(path) != "lib":
                    raise Failure("UNEXPECTED_VENV_SYMLINK", "VENV_FILESYSTEM")


def action_d_subprocess_environment() -> dict[str, str]:
    return {
        "PATH": "/usr/bin:/bin",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "HOME": "/nonexistent",
        "PYTHONNOUSERSITE": "1",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PIP_CONFIG_FILE": os.devnull,
        "PIP_DISABLE_PIP_VERSION_CHECK": "1",
        "PIP_NO_INPUT": "1",
        "PIP_NO_INDEX": "1",
        "PIP_ROOT_USER_ACTION": "ignore",
        "PIP_KEYRING_PROVIDER": "disabled",
    }
