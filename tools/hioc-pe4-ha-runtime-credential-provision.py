#!/usr/bin/env python3
"""Fixed-path PE-4 credential boundary. No network, authentication or evidence bytes.

Internal functions accept an injected filesystem for synthetic tests only.
Production has no fixture/path override. Linux POSIX ACL xattrs are inspected on FDs.
"""
import errno
import os
import stat
import struct
import sys

CREDENTIAL_PATH = "/etc/hioc/credentials/home_assistant.token"
FINAL_NAME = "home_assistant.token"
HOST = "nutandpihole"
OPERATOR = "jazofv1"
MAX_TOKEN = 4096
MAX_FILE = 4097


class BoundaryError(Exception):
    """Only fixed codes are exposed by the CLI; never exception arguments."""
    def __init__(self, code):
        self.code = code
        super().__init__(code)


def require(condition, code):
    if not condition:
        raise BoundaryError(code)


def content_policy(data):
    require(isinstance(data, bytes) and len(data) <= MAX_FILE, "CONTENT_INVALID")
    value = data[:-1] if data.endswith(b"\n") else data
    try:
        require(0 < len(value) <= MAX_TOKEN and all(0x21 <= b <= 0x7e for b in value), "CONTENT_INVALID")
    finally:
        value = None


def encode_input(value):
    try:
        encoded = value.encode("ascii", errors="strict")
    except (UnicodeError, AttributeError):
        raise BoundaryError("INPUT_INVALID") from None
    require(0 < len(encoded) <= MAX_TOKEN and all(0x21 <= b <= 0x7e for b in encoded), "INPUT_INVALID")
    return encoded + b"\n"


def effective_readers(users, groups, user, group):
    """NSS enumeration plus lookups; primary membership is not in gr_mem."""
    require(len({u.pw_name for u in users}) == len(users), "ACCOUNT_LOOKUP_INVALID")
    require(len({u.pw_uid for u in users}) == len(users), "ACCOUNT_LOOKUP_INVALID")
    require(len({g.gr_name for g in groups}) == len(groups), "ACCOUNT_LOOKUP_INVALID")
    require(sum(g.gr_gid == group.gr_gid for g in groups) == 1, "ACCOUNT_LOOKUP_INVALID")
    require(sum(u == user for u in users) == 1 and sum(g == group for g in groups) == 1, "ACCOUNT_LOOKUP_INVALID")
    require(user.pw_name == OPERATOR and user.pw_uid > 0 and group.gr_name == OPERATOR and group.gr_gid > 0, "ACCOUNT_LOOKUP_INVALID")
    require(len(group.gr_mem) == len(set(group.gr_mem)), "ACCOUNT_LOOKUP_INVALID")
    by_name = {u.pw_name: u for u in users}
    require(all(name in by_name for name in group.gr_mem), "ACCOUNT_LOOKUP_INVALID")
    readers = {u.pw_name for u in users if u.pw_gid == group.gr_gid}
    readers.update(group.gr_mem)
    require(OPERATOR in readers, "GROUP_READER_INVALID")
    require(all(name == OPERATOR or by_name[name].pw_uid == 0 for name in readers), "GROUP_READER_INVALID")
    return group.gr_gid


def identities(mode):
    require(sys.platform == "linux", "LINUX_REQUIRED")
    require(os.uname().nodename == HOST, "HOST_INVALID")
    import pwd
    import grp
    try:
        user = pwd.getpwnam(OPERATOR)
        group = grp.getgrnam(OPERATOR)
        users, groups = pwd.getpwall(), grp.getgrall()
        root = pwd.getpwuid(0)
        require(root.pw_name == "root" and root.pw_uid == 0 and sum(u == root for u in users) == 1, "ACCOUNT_LOOKUP_INVALID")
        gid = effective_readers(users, groups, user, group)
        members = set(group.gr_mem) | {u.pw_name for u in users if u.pw_gid == gid}
        for member in members:
            looked_up = pwd.getpwnam(member)
            require(looked_up.pw_name == member and sum(u == looked_up for u in users) == 1, "ACCOUNT_LOOKUP_INVALID")
        require(pwd.getpwuid(user.pw_uid) == user and grp.getgrgid(gid) == group, "ACCOUNT_LOOKUP_INVALID")
    except (KeyError, OSError):
        raise BoundaryError("ACCOUNT_LOOKUP_INVALID") from None
    if mode == "root":
        require(os.geteuid() == 0 and os.getuid() == 0, "ROOT_REQUIRED")
    else:
        require(os.geteuid() == user.pw_uid and os.getuid() == user.pw_uid, "OPERATOR_REQUIRED")
        require(gid in {os.getegid(), *os.getgroups()}, "OPERATOR_GROUP_INVALID")
    return gid


def fingerprint(info):
    return (info.st_dev, info.st_ino, info.st_mode, info.st_uid, info.st_gid,
            info.st_nlink, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


class NativeFS:
    """Descriptor-relative Linux operations; imports alone perform no I/O."""
    def open_root(self):
        return os.open("/", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)

    def open_dir(self, parent, name):
        return os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=parent)

    def open_file(self, parent, name):
        return os.open(name, os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=parent)

    def fstat(self, fd):
        return os.fstat(fd)

    def lstat(self, parent, name):
        return os.stat(name, dir_fd=parent, follow_symlinks=False)

    def read(self, fd, size):
        return os.read(fd, size)

    def close(self, fd):
        os.close(fd)

    def acl(self, fd, directory=False):
        for attr in (["system.posix_acl_access", "system.posix_acl_default"] if directory else ["system.posix_acl_access"]):
            try:
                raw = os.getxattr(fd, attr)
            except OSError as exc:
                # ENODATA is an authoritative absent ACL; ENOTSUP/EPERM etc fail.
                require(exc.errno == errno.ENODATA, "ACL_UNVERIFIABLE")
                continue
            require(attr.endswith("access"), "ACL_UNEXPECTED")
            require(len(raw) == 28 and struct.unpack("<I", raw[:4])[0] == 2, "ACL_UNEXPECTED")
            entries = [struct.unpack("<HHI", raw[i:i+8]) for i in range(4, 28, 8)]
            mode = stat.S_IMODE(self.fstat(fd).st_mode)
            expected = [(1, (mode >> 6) & 7, 0xffffffff), (4, (mode >> 3) & 7, 0xffffffff), (32, mode & 7, 0xffffffff)]
            require(entries == expected, "ACL_UNEXPECTED")


def check_directory(fs, fd, gid=None):
    info = fs.fstat(fd)
    mode = stat.S_IMODE(info.st_mode)
    require(stat.S_ISDIR(info.st_mode) and info.st_uid == 0 and not (mode & 0o7022), "DIRECTORY_INVALID")
    if gid is not None:
        require(info.st_gid == gid and mode == 0o750, "DIRECTORY_INVALID")
    fs.acl(fd, True)
    return info


def bound_name(fs, parent, name, fd):
    require(fingerprint(fs.lstat(parent, name)) == fingerprint(fs.fstat(fd)), "NAME_BINDING_CHANGED")


def open_hierarchy(fs, gid):
    fds = []
    try:
        fd = fs.open_root(); fds.append(fd); check_directory(fs, fd)
        for name in ("etc", "hioc", "credentials"):
            parent = fd
            fd = fs.open_dir(parent, name); fds.append(fd)
            check_directory(fs, fd, gid if name != "etc" else None)
            bound_name(fs, parent, name, fd)
        return fds
    except BaseException:
        for fd in reversed(fds): fs.close(fd)
        raise


def recheck_hierarchy(fs, fds, gid):
    for index, fd in enumerate(fds):
        check_directory(fs, fd, gid if index >= 2 else None)
        if index:
            bound_name(fs, fds[index-1], ("etc", "hioc", "credentials")[index-1], fd)


def read_credential(fs, parent, gid, name=FINAL_NAME, expected=None):
    # lstat before open rejects FIFO/device/directory without opening it.
    initial = fs.lstat(parent, name)
    require(stat.S_ISREG(initial.st_mode) and initial.st_nlink == 1, "FILE_INVALID")
    fd = fs.open_file(parent, name)
    data = None
    try:
        before = fs.fstat(fd)
        require(fingerprint(initial) == fingerprint(before), "NAME_BINDING_CHANGED")
        require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "FILE_INVALID")
        require(before.st_uid == 0 and before.st_gid == gid and stat.S_IMODE(before.st_mode) == 0o640, "FILE_SECURITY_INVALID")
        require(0 < before.st_size <= MAX_FILE, "CONTENT_INVALID")
        fs.acl(fd)
        data = fs.read(fd, MAX_FILE + 1)  # one bounded logical read; short reads fail.
        require(len(data) == before.st_size, "READ_INCOMPLETE")
        require(fingerprint(before) == fingerprint(fs.fstat(fd)), "FILE_CHANGED")
        bound_name(fs, parent, name, fd)
        content_policy(data)
        require(expected is None or data == expected, "CONTENT_CHANGED")
        return fingerprint(before)
    finally:
        data = None
        fs.close(fd)


def sanitized_failure(code):
    # Never interpolate exception text, paths supplied by callers, or secret data.
    print("RESULT=FAIL")
    print("ERROR_CODE=" + code)
    print("CREDENTIAL_VALUE_EXPOSED=FALSE")
    print("NETWORK_CONNECTION_ATTEMPTED=FALSE")
    print("HA_AUTHENTICATION_ATTEMPTED=FALSE")


class ProvisionFS(NativeFS):
    def mkdir(self, parent, name):
        os.mkdir(name, 0o700, dir_fd=parent)

    def ownership(self, fd, gid):
        os.fchown(fd, 0, gid)

    def mode(self, fd, mode):
        os.fchmod(fd, mode)

    def sync(self, fd):
        os.fsync(fd)

    def lock(self, fd):
        import fcntl
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)

    def stage_name(self):
        import secrets
        return ".hioc-ha-credential-" + secrets.token_hex(24)

    def create_stage(self, parent, name):
        return os.open(name, os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC, 0o600, dir_fd=parent)

    def write(self, fd, data):
        return os.write(fd, data)

    def replace(self, parent, name):
        os.replace(name, FINAL_NAME, src_dir_fd=parent, dst_dir_fd=parent)

    def unlink_stage(self, parent, name):
        os.unlink(name, dir_fd=parent)


def prepare_hierarchy(fs, gid):
    fds = []
    try:
        fd = fs.open_root(); fds.append(fd); check_directory(fs, fd)
        for name in ("etc", "hioc", "credentials"):
            parent = fd
            try:
                fd = fs.open_dir(parent, name)
            except FileNotFoundError:
                require(name != "etc", "ANCESTOR_MISSING")
                fs.mkdir(parent, name)
                fd = fs.open_dir(parent, name)
                fds.append(fd)
                fresh = fs.fstat(fd)
                require(stat.S_ISDIR(fresh.st_mode) and fresh.st_uid == 0 and stat.S_IMODE(fresh.st_mode) == 0o700, "DIRECTORY_CREATION_INVALID")
                fs.acl(fd, True)
                bound_name(fs, parent, name, fd)
                fs.ownership(fd, gid); fs.mode(fd, 0o750)
                fs.sync(fd); fs.sync(parent)
            else:
                fds.append(fd)
            check_directory(fs, fd, gid if name != "etc" else None)
            bound_name(fs, parent, name, fd)
        fs.lock(fds[-1])  # pinned directory flock; no lock-file or token backup.
        recheck_hierarchy(fs, fds, gid)
        fs.sync(fds[-1])  # prove directory fsync works before the hidden prompt.
        return fds
    except BaseException:
        for fd in reversed(fds): fs.close(fd)
        raise


def existing_credential(fs, parent, gid):
    try:
        fs.lstat(parent, FINAL_NAME)
    except FileNotFoundError:
        return None
    try:
        return read_credential(fs, parent, gid)
    except Exception:
        raise BoundaryError("EXISTING_CREDENTIAL_INVALID") from None


def hidden_input():
    import getpass
    import warnings
    # Open the controlling terminal explicitly. Never fall back to stdin or echo.
    fd = os.open("/dev/tty", os.O_RDWR | os.O_NOCTTY | os.O_CLOEXEC)
    try:
        require(os.isatty(fd) and sys.stdin.isatty() and sys.stderr.isatty(), "CONTROLLING_TTY_REQUIRED")
        with os.fdopen(os.dup(fd), "w", encoding="ascii", closefd=True) as stream:
            with warnings.catch_warnings():
                warnings.simplefilter("error", getpass.GetPassWarning)
                return getpass.getpass("Home Assistant runtime access token:", stream=stream)
    finally:
        os.close(fd)


def install(fs, gid, acquire):
    """Injected acquisition is internal only. Production supplies hidden_input."""
    fds = prepare_hierarchy(fs, gid)
    stage_fd = None
    stage_name = None
    replaced = False
    value = data = None
    try:
        parent = fds[-1]
        previous = existing_credential(fs, parent, gid)
        # All credential-free boundary checks above precede the one hidden prompt.
        value = acquire()
        try:
            data = encode_input(value)
        finally:
            value = None
        recheck_hierarchy(fs, fds, gid)
        candidate_name = fs.stage_name()
        require(candidate_name.startswith(".hioc-ha-credential-") and "/" not in candidate_name and candidate_name != FINAL_NAME, "STAGING_NAME_INVALID")
        stage_fd = fs.create_stage(parent, candidate_name)
        stage_name = candidate_name  # only our successful O_EXCL creation can be cleaned.
        initial = fs.fstat(stage_fd)
        require(stat.S_ISREG(initial.st_mode) and initial.st_uid == 0 and initial.st_nlink == 1 and stat.S_IMODE(initial.st_mode) == 0o600, "STAGING_INVALID")
        fs.acl(stage_fd)
        bound_name(fs, parent, stage_name, stage_fd)
        offset = 0
        while offset < len(data):
            written = fs.write(stage_fd, data[offset:])
            require(isinstance(written, int) and 0 < written <= len(data) - offset, "WRITE_INCOMPLETE")
            offset += written
        fs.sync(stage_fd)
        private = fs.fstat(stage_fd)
        require(stat.S_ISREG(private.st_mode) and private.st_uid == 0 and private.st_nlink == 1 and stat.S_IMODE(private.st_mode) == 0o600, "STAGING_INVALID")
        fs.acl(stage_fd)
        bound_name(fs, parent, stage_name, stage_fd)
        fs.ownership(stage_fd, gid); fs.mode(stage_fd, 0o640)
        fs.sync(stage_fd)  # durability includes ownership/mode, not only content.
        read_credential(fs, parent, gid, stage_name, expected=data)
        require(fs.fstat(stage_fd).st_dev == fs.fstat(parent).st_dev, "STAGING_FILESYSTEM_INVALID")
        bound_name(fs, parent, stage_name, stage_fd)
        recheck_hierarchy(fs, fds, gid)
        current = existing_credential(fs, parent, gid)
        require(previous == current, "EXISTING_CREDENTIAL_CHANGED")
        operation = "INSTALL" if current is None else "ROTATE"
        fs.replace(parent, stage_name)
        replaced = True
        fs.sync(parent)
        final = read_credential(fs, parent, gid, expected=data)
        pinned = fs.fstat(stage_fd)
        require(final[:2] == (pinned.st_dev, pinned.st_ino), "FINAL_BINDING_INVALID")
        recheck_hierarchy(fs, fds, gid)
        return operation
    except BaseException:
        if replaced:
            # New credential is authoritative; never claim rollback/preservation.
            raise BoundaryError("POST_REPLACE_VALIDATION_FAILED_NEW_AUTHORITATIVE") from None
        raise
    finally:
        value = data = None
        try:
            if stage_fd is not None and stage_name is not None and not replaced:
                # Cleanup only the object still bound to our private pinned descriptor.
                # If replace changed the name but raised, absence is safe; final untouched.
                try:
                    named = fs.lstat(fds[-1], stage_name)
                except FileNotFoundError:
                    named = None
                if named is not None:
                    pinned = fs.fstat(stage_fd)
                    require((named.st_dev, named.st_ino) == (pinned.st_dev, pinned.st_ino) and stat.S_ISREG(named.st_mode) and named.st_uid == 0 and named.st_nlink == 1, "STAGING_CLEANUP_UNPROVED")
                    recheck_hierarchy(fs, fds, gid)
                    fs.unlink_stage(fds[-1], stage_name)
                    fs.sync(fds[-1])
        except BaseException:
            raise BoundaryError("STAGING_CLEANUP_UNPROVED") from None
        finally:
            if stage_fd is not None: fs.close(stage_fd)
            for fd in reversed(fds): fs.close(fd)


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    try:
        require(args == [], "ARGUMENTS_INVALID")
        gid = identities("root")
        operation = install(ProvisionFS(), gid, hidden_input)
        print("RESULT=PASS")
        print("OPERATION=" + operation)
        print("TARGET_HOST=" + HOST)
        print("APPROVED_OPERATOR=" + OPERATOR)
        print("CREDENTIAL_PATH=" + CREDENTIAL_PATH)
        print("DIRECTORY_OWNER_GROUP_MODE=root:jazofv1:0750")
        print("FILE_OWNER_GROUP_MODE=root:jazofv1:0640")
        for field in ("DIRECTORY_VALIDATION", "FILE_VALIDATION", "ACL_VALIDATION", "GROUP_READER_VALIDATION", "CREDENTIAL_CONTENT_VALIDATION", "ATOMIC_REPLACEMENT"):
            print(field + "=PASS")
        print("CREDENTIAL_VALUE_EXPOSED=FALSE")
        print("NETWORK_CONNECTION_ATTEMPTED=FALSE")
        print("HA_AUTHENTICATION_ATTEMPTED=FALSE")
        print("INDEPENDENT_VALIDATION=NOT_STARTED")
        return 0
    except BoundaryError as exc:
        sanitized_failure(exc.code)
    except BaseException:
        sanitized_failure("PROVISIONING_FAILED_REPLACEMENT_STATUS_UNPROVED")
    return 1


if __name__ == "__main__":
    sys.exit(main())
