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


def windows_openssh_tool(name: str) -> pathlib.Path:
    """Resolve the Windows system OpenSSH client without consulting PATH."""
    if name not in {"ssh", "scp", "ssh-keygen"} or os.name != "nt":
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


def validate_construction(value: str) -> pathlib.Path:
    path = pathlib.Path(value)
    if path.parent != ENVIRONMENT_ROOT or not CONSTRUCTION_RE.fullmatch(path.name):
        raise Failure("CONSTRUCTION_PATH_INVALID", "INPUT_VALIDATION")
    require_directory(path, 0o750)
    require_owned(path)
    return path


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
        env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    try:
        result = subprocess.run(command, text=True, capture_output=capture, timeout=timeout,
                                check=False, env=env)
    except (OSError, subprocess.TimeoutExpired):
        raise Failure("COMMAND_INVOCATION_FAILED", stage)
    if result.returncode != 0:
        raise Failure((failure_codes or {}).get(result.returncode, "COMMAND_FAILED"), stage)
    return result


def run_bounded(command: list[str], stage: str, *, timeout: int,
                max_output: int = 65536,
                failure_codes: dict[int, str] | None = None) -> subprocess.CompletedProcess[str]:
    try:
        process = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
    except OSError:
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


def exact_distribution_set(python: pathlib.Path) -> None:
    code = "import importlib.metadata as m;print('\\n'.join(sorted(d.metadata['Name'].lower()+'=='+d.version for d in m.distributions())))"
    names = run([str(python), "-I", "-c", code], "DEPENDENCY_IDENTITY").stdout.splitlines()
    allowed = {"pip", "setuptools", "websockets"}
    parsed = {line.split("==", 1)[0] for line in names}
    if "websockets==16.1.1" not in names or not parsed.issubset(allowed):
        raise Failure("INSTALLED_DISTRIBUTION_SET_INVALID", "DEPENDENCY_IDENTITY")


def safe_cleanup_construction(path: pathlib.Path) -> None:
    validate_construction(str(path))
    if ACTIVE_POINTER.is_symlink() and validated_active_target() == path:
        raise Failure("CONSTRUCTION_IS_ACTIVE", "CLEANUP")
    for item in path.rglob("*"):
        if item.is_symlink():
            raise Failure("CONSTRUCTION_SYMLINK_FOUND", "CLEANUP")
    import shutil
    shutil.rmtree(path)
