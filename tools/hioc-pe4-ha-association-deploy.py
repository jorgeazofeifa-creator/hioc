"""Repository-bound additive deployment only; never invokes the association adapter.

Production CLI has no path override or rollback/delete option. Injectable filesystem
and fault hook are synthetic test interfaces only. All failures have finite output.
"""
import argparse
import contextlib
import errno
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys

SOURCE = Path("/home/jazofv1/hioc-release-source")
HOME = Path("/home/jazofv1/hioc")
BASELINE = "5e9d1ff3d74bb22c6cc0c4f726517c1d0b86d7f2"
RECORD = "governance/pe4/pe4-ha-association-adapter-deployment-preparation.json"
ENDPOINT = "ws://192.168.100.251:8123/api/websocket"
CONFIG = "config/hioc.conf"
ASSOCIATIONS = "state/inventory/associations"
LOCK = ASSOCIATIONS + "/.home_assistant.lock"
TX = "backups/pe4-ha-association-deployment-v1"
INTERPRETER = HOME / "runtime/pe4/active/bin/python"
ENVIRONMENT = HOME / "runtime/pe4/environments/cpython311-websockets16.1.1-lock-v1"
LIMIT = 2 * 1024 * 1024
CODES = {"INVALID", "SOURCE_BINDING", "DEPENDENCY_DRIFT", "DESTINATION_CONFLICT",
         "CONFIG_CONFLICT", "UNSAFE_OBJECT", "UNEXPECTED_PREEXISTING_ASSOCIATION_STATE",
         "SCHEDULER_PRESENT", "RUNTIME_DRIFT", "CREDENTIAL_INVALID", "TRANSACTION_CONFLICT",
         "IO_FAILED", "COMPLETE"}

class Failure(Exception):
    def __init__(self, code):
        self.code = code if code in CODES else "INVALID"
        super().__init__(self.code)

def require(condition, code="INVALID"):
    if not condition: raise Failure(code)

def sha(raw): return hashlib.sha256(raw).hexdigest()
def canonical(value): return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()

def endpoint_config(raw):
    """Mirror ConfigService key/value semantics, preserving unrelated bytes exactly."""
    require(type(raw) is bytes and len(raw) <= LIMIT, "CONFIG_CONFLICT")
    try: text = raw.decode("utf-8", "strict")
    except UnicodeError: raise Failure("CONFIG_CONFLICT") from None
    found = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line: continue
        key, value = line.split("=", 1)
        if key.strip() == "HIOC_HA_ENDPOINT":
            found.append(value.strip().strip('"').strip("'"))
        # Export-like assignments are not consumed by ConfigService; disallow ambiguity.
        require(not re.match(r"(?:export\s+)?HIOC_HA_ENDPOINT\b", key.strip()) or key.strip() == "HIOC_HA_ENDPOINT", "CONFIG_CONFLICT")
    require(len(found) <= 1 and (not found or found[0] == ENDPOINT), "CONFIG_CONFLICT")
    if found: return raw
    return raw + (b"\n" if raw and not raw.endswith(b"\n") else b"") + ('HIOC_HA_ENDPOINT="' + ENDPOINT + '"\n').encode()

def shell_values(raw):
    try: text = raw.decode("utf-8", "strict")
    except UnicodeError: raise Failure("CONFIG_CONFLICT") from None
    values = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip('"').strip("'")
    return values

def effective_configuration(toolkit, config):
    values = {"HIOC_HOME": HOME.as_posix()}
    values.update(shell_values(toolkit)); values.update(shell_values(config))
    require(values.get("HIOC_HOME") == HOME.as_posix() and values.get("HIOC_HA_ENDPOINT") == ENDPOINT, "CONFIG_CONFLICT")

def no_scheduler(raw):
    require(len(raw) <= LIMIT, "SCHEDULER_PRESENT")
    for line in raw.decode("utf-8", "strict").splitlines():
        if line.strip() and not line.lstrip().startswith("#"):
            require("hioc-home-assistant-association.py" not in line and "HIOC_PE4_HA_ASSOCIATION" not in line, "SCHEDULER_PRESENT")

def no_private_state(names):
    require(not any(n == "home_assistant.json" or n.startswith((".home_assistant.txn-", ".home_assistant.done-")) for n in names), "UNEXPECTED_PREEXISTING_ASSOCIATION_STATE")

def runtime_identity(value):
    expected = {"implementation": "cpython", "python": "3.11.2", "architecture": "aarch64",
                "soabi": "cpython-311-aarch64-linux-gnu", "websockets": "16.1.1",
                "prefix": str(ENVIRONMENT), "executable": str(INTERPRETER), "isolated": True,
                "bytecode_disabled": True, "origins_valid": True, "distributions_valid": True}
    require(value == expected, "RUNTIME_DRIFT")

def destination(raw, expected, required=False):
    require(raw is not None or not required, "DEPENDENCY_DRIFT")
    if raw is not None: require(sha(raw) == expected, "DEPENDENCY_DRIFT" if required else "DESTINATION_CONFLICT")
    return "EXACT" if raw is not None else "ABSENT"

class NativeFS:
    """Pinned no-follow directory traversal and exclusive additive publication."""
    def __init__(self, root, uid, gid):
        self.root, self.uid, self.gid = Path(root), uid, gid

    def security(self, fd, directory=False, mode=None):
        info = os.fstat(fd)
        require(stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode), "UNSAFE_OBJECT")
        require(info.st_uid in (0, self.uid) and not stat.S_IMODE(info.st_mode) & 0o7022, "UNSAFE_OBJECT")
        if not directory: require(info.st_nlink == 1, "UNSAFE_OBJECT")
        if mode is not None:
            require(info.st_uid == self.uid and info.st_gid == self.gid and stat.S_IMODE(info.st_mode) == mode, "UNSAFE_OBJECT")
        for name in ("system.posix_acl_access", "system.posix_acl_default"):
            try: os.getxattr(fd, name)
            except OSError as exc: require(exc.errno == errno.ENODATA, "UNSAFE_OBJECT")
            else: raise Failure("UNSAFE_OBJECT")
        return info

    @contextlib.contextmanager
    def directory(self, relative=""):
        require(not relative.startswith("/") and ".." not in relative.split("/"), "UNSAFE_OBJECT")
        fd = os.open("/", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
        chain = []
        try:
            self.security(fd, True)
            for part in (*self.root.parts[1:], *([p for p in relative.split("/") if p])):
                child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=fd)
                chain.append((fd, part, child)); self.security(child, True); fd = child
            yield fd
            for parent, name, child in chain:
                current = os.stat(name, dir_fd=parent, follow_symlinks=False)
                held = os.fstat(child)
                require((current.st_dev, current.st_ino) == (held.st_dev, held.st_ino), "UNSAFE_OBJECT")
                self.security(child, True)
        finally:
            for parent, _, _ in reversed(chain): os.close(parent)
            os.close(fd)

    def read(self, relative, mode=None):
        path = Path(relative)
        try:
            with self.directory(str(path.parent) if str(path.parent) != "." else "") as parent:
                try: fd = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC, dir_fd=parent)
                except FileNotFoundError: return None
                try:
                    before = self.security(fd, mode=mode)
                    raw = bytearray()
                    while len(raw) <= LIMIT:
                        chunk = os.read(fd, min(65536, LIMIT + 1 - len(raw)))
                        if not chunk: break
                        raw.extend(chunk)
                    require(len(raw) <= LIMIT, "UNSAFE_OBJECT")
                    after = self.security(fd, mode=mode)
                    name = os.stat(path.name, dir_fd=parent, follow_symlinks=False)
                    require(before == after and (name.st_dev, name.st_ino) == (after.st_dev, after.st_ino), "UNSAFE_OBJECT")
                    return bytes(raw)
                finally: os.close(fd)
        except FileNotFoundError: return None

    def info(self, relative):
        p = Path(relative)
        try:
            with self.directory(str(p.parent) if str(p.parent) != "." else "") as fd:
                return os.stat(p.name, dir_fd=fd, follow_symlinks=False)
        except FileNotFoundError: return None

    def check_directory(self, relative, mode=None):
        if self.info(relative) is None: return False
        with self.directory(relative) as fd: self.security(fd, True, mode)
        return True

    def names(self, relative):
        if self.info(relative) is None: return []
        with self.directory(relative) as fd:
            names = os.listdir(fd)
            require(len(names) <= 4096, "UNSAFE_OBJECT")
            return names

    def preflight_install(self, relative):
        import ctypes
        require(hasattr(ctypes.CDLL(None), "renameat2"), "UNSAFE_OBJECT")
        for parent in reversed(self.parents(relative)):
            if self.info(parent) is not None:
                with self.directory(parent) as fd:
                    info = self.security(fd, True)
                    require(info.st_uid == self.uid and info.st_gid == self.gid and info.st_mode & stat.S_IWUSR and info.st_dev == self.info("backups").st_dev, "UNSAFE_OBJECT")
                return
        raise Failure("UNSAFE_OBJECT")

    def mkdir(self, relative, mode):
        p = Path(relative)
        with self.directory(str(p.parent)) as fd:
            created = False
            try: os.mkdir(p.name, mode, dir_fd=fd); created = True
            except FileExistsError: pass
            with self.directory(relative) as child:
                if created: os.fchmod(child, mode)
                os.fsync(child); self.security(child, True, mode)
            os.fsync(fd)

    def parents(self, relative):
        p = Path(relative).parent
        result = []
        while str(p) != ".": result.append(str(p)); p = p.parent
        return list(reversed(result))

    def add(self, relative, raw, mode):
        """Linux renameat2 NOREPLACE: atomic publication without overwriting a name."""
        import ctypes
        existing = self.read(relative, mode)
        if existing is not None:
            require(existing == raw, "DESTINATION_CONFLICT")
            return
        p = Path(relative); stage = TX + "/stage-" + sha(relative.encode())[:16]
        with self.directory(TX) as txfd, self.directory(str(p.parent)) as parent:
            s = Path(stage).name
            try: fd = os.open(s, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, mode, dir_fd=txfd)
            except FileExistsError:
                fd = os.open(s, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=txfd)
                self.security(fd, mode=mode)
                require(os.read(fd, LIMIT + 1) == raw, "TRANSACTION_CONFLICT")
            else:
                os.fchmod(fd, mode)
                with os.fdopen(os.dup(fd), "wb") as stream: stream.write(raw); stream.flush(); os.fsync(stream.fileno())
            try:
                os.fsync(fd); os.fsync(txfd)
                named = os.stat(s, dir_fd=txfd, follow_symlinks=False); held = os.fstat(fd)
                require((named.st_dev, named.st_ino) == (held.st_dev, held.st_ino), "TRANSACTION_CONFLICT")
                libc = ctypes.CDLL(None, use_errno=True)
                rename = libc.renameat2
                rename.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
                rename.restype = ctypes.c_int
                rc = rename(txfd, os.fsencode(s), parent, os.fsencode(p.name), 1)
                require(rc == 0, "DESTINATION_CONFLICT")
                os.fsync(parent); os.fsync(txfd)
            finally: os.close(fd)
        require(self.read(relative, mode) == raw, "DESTINATION_CONFLICT")

    def replace_config(self, prior, candidate, mode):
        require(self.read(CONFIG) == prior, "CONFIG_CONFLICT")
        self.add(TX + "/config-next", candidate, mode)
        with self.directory("config") as parent, self.directory(TX) as txfd:
            require(self.read(CONFIG) == prior, "CONFIG_CONFLICT")
            before = self.info(CONFIG); staged = self.info(TX + "/config-next")
            require((before.st_uid, before.st_gid, stat.S_IMODE(before.st_mode)) == (staged.st_uid, staged.st_gid, stat.S_IMODE(staged.st_mode)), "CONFIG_CONFLICT")
            os.replace("config-next", "hioc.conf", src_dir_fd=txfd, dst_dir_fd=parent)
            os.fsync(parent); os.fsync(txfd)
        require(self.read(CONFIG) == candidate, "CONFIG_CONFLICT")

    @contextlib.contextmanager
    def lock(self):
        import fcntl
        # Production backups directory must already exist and be operator-owned.
        with self.directory("backups") as parent:
            fd = os.open(".pe4-ha-association-deployment.lock", os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600, dir_fd=parent)
            try:
                self.security(fd, mode=0o600)
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                held = self.security(fd, mode=0o600)
                named = os.stat(".pe4-ha-association-deployment.lock", dir_fd=parent, follow_symlinks=False)
                require((held.st_dev, held.st_ino) == (named.st_dev, named.st_ino), "UNSAFE_OBJECT")
                os.fsync(fd); os.fsync(parent)
                yield
            finally: os.close(fd)

def preflight(fs, manifest, resume=False):
    for item in manifest["dependencies"]:
        destination(fs.read(item["path"]), item["sha256"], True)
    for item in manifest["deploy"]:
        destination(fs.read(item["path"]), item["sha256"])
        info = fs.info(item["path"])
        if info is not None:
            require(info.st_uid == fs.uid and info.st_gid == fs.gid and stat.S_IMODE(info.st_mode) == int(item["mode"], 8), "UNSAFE_OBJECT")
        for parent in fs.parents(item["path"]): fs.check_directory(parent)
        fs.preflight_install(item["path"])
    require(fs.check_directory("state/inventory"), "UNSAFE_OBJECT")
    fs.check_directory(ASSOCIATIONS, 0o700)
    no_private_state(fs.names(ASSOCIATIONS))
    fs.read(LOCK, 0o600)
    raw = fs.read(CONFIG)
    require(raw is not None, "CONFIG_CONFLICT")
    info = fs.info(CONFIG)
    require(info.st_uid == fs.uid and info.st_gid == fs.gid, "CONFIG_CONFLICT")
    require(fs.check_directory("backups"), "UNSAFE_OBJECT")
    fs.preflight_install(CONFIG); fs.preflight_install(LOCK); fs.preflight_install(TX + "/intent.json")
    return raw, endpoint_config(raw)

def deploy(fs, manifest, source_commit, fault=lambda point: None):
    intent_path = TX + "/intent.json"
    expected_names = {"config-prior", "config-candidate", "config-next", "intent.json", "committed.json"}
    staged_paths = [i["path"] for i in manifest["deploy"]] + [LOCK, intent_path, TX + "/config-prior", TX + "/config-candidate", TX + "/config-next", TX + "/committed.json"]
    expected_names.update("stage-" + sha(p.encode())[:16] for p in staged_paths)
    require(set(fs.names(TX)) <= expected_names, "TRANSACTION_CONFLICT")
    intent_raw = fs.read(intent_path, 0o600)
    if intent_raw is None:
        require(fs.info(TX) is None, "TRANSACTION_CONFLICT")
        prior, candidate = preflight(fs, manifest)
        created = [i["path"] for i in manifest["deploy"] if fs.read(i["path"]) is None]
        dirs = {ASSOCIATIONS} if fs.info(ASSOCIATIONS) is None else set()
        for i in manifest["deploy"]:
            dirs.update(p for p in fs.parents(i["path"]) if fs.info(p) is None)
        intent = {"version": 1, "source_commit": source_commit, "created_files": created,
                  "created_directories": sorted(dirs, key=lambda p: (p.count("/"), p)),
                  "lock_created": fs.info(LOCK) is None, "endpoint_added": prior != candidate,
                  "config_mode": format(stat.S_IMODE(fs.info(CONFIG).st_mode), "04o"),
                  "prior_sha256": sha(prior), "candidate_sha256": sha(candidate),
                  "targets": {i["path"]: i["sha256"] for i in manifest["deploy"]}}
        fs.mkdir(TX, 0o700)
        fault("NAMESPACE_CREATED")
        # Prepare config backup and immutable intent before target/config mutation.
        fs.add(TX + "/config-prior", prior, 0o600)
        fs.add(TX + "/config-candidate", candidate, 0o600)
        fs.add(intent_path, canonical(intent), 0o600)
        fault("PREPARED")
    else:
        fs.check_directory(TX, 0o700)
        intent = json.loads(intent_raw)
        require(intent_raw == canonical(intent) and intent["source_commit"] == source_commit and
                intent["targets"] == {i["path"]: i["sha256"] for i in manifest["deploy"]}, "TRANSACTION_CONFLICT")
        require(set(intent) == {"version", "source_commit", "created_files", "created_directories", "lock_created", "endpoint_added", "config_mode", "prior_sha256", "candidate_sha256", "targets"} and intent["version"] == 1, "TRANSACTION_CONFLICT")
        require(set(intent["created_files"]) <= set(intent["targets"]) and
                set(intent["created_directories"]) <= {p for i in manifest["deploy"] for p in fs.parents(i["path"])} | {ASSOCIATIONS}, "TRANSACTION_CONFLICT")
        prior = fs.read(TX + "/config-prior", 0o600); candidate = fs.read(TX + "/config-candidate", 0o600)
        require(prior is not None and candidate is not None and sha(prior) == intent["prior_sha256"] and
                sha(candidate) == intent["candidate_sha256"] and endpoint_config(prior) == candidate, "TRANSACTION_CONFLICT")
        require(fs.read(CONFIG) in (prior, candidate) and format(stat.S_IMODE(fs.info(CONFIG).st_mode), "04o") == intent["config_mode"], "CONFIG_CONFLICT")
        preflight(fs, manifest, True)
    for directory in intent["created_directories"]:
        fs.mkdir(directory, 0o700 if directory == ASSOCIATIONS else 0o755)
    for item in manifest["deploy"]:
        if fs.read(item["path"]) is None:
            require(item["path"] in intent["created_files"], "TRANSACTION_CONFLICT")
            fs.add(item["path"], item["bytes"], int(item["mode"], 8))
        fault("FILE:" + item["path"])
    if fs.read(LOCK) is None:
        require(intent["lock_created"], "TRANSACTION_CONFLICT")
        fs.add(LOCK, b"", 0o600)
    fault("LOCK_CREATED")
    if fs.read(CONFIG) != candidate:
        require(intent["endpoint_added"], "CONFIG_CONFLICT")
        fs.replace_config(prior, candidate, int(intent["config_mode"], 8))
    fault("CONFIG_REPLACED")
    preflight(fs, manifest)
    require(fs.read(CONFIG) == candidate, "CONFIG_CONFLICT")
    committed = canonical({"status": "COMMITTED", "source_commit": source_commit, "intent_sha256": sha(canonical(intent))})
    current = fs.read(TX + "/committed.json", 0o600)
    if current is None: fs.add(TX + "/committed.json", committed, 0o600)
    else: require(current == committed, "TRANSACTION_CONFLICT")
    fault("COMMITTED")

ENV = {"PATH": "/usr/sbin:/usr/bin:/bin", "HOME": "/home/jazofv1", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
def command(args, code, cwd=None):
    result = subprocess.run(args, cwd=cwd, env=ENV, stdin=subprocess.DEVNULL, capture_output=True, timeout=15)
    require(result.returncode == 0 and len(result.stdout) + len(result.stderr) <= LIMIT, code)
    return result.stdout

def source_binding(expected):
    require(re.fullmatch(r"[0-9a-f]{40}", expected) is not None, "SOURCE_BINDING")
    require(Path(__file__).resolve() == SOURCE / "tools/hioc-pe4-ha-association-deploy.py", "SOURCE_BINDING")
    def git(*args): return command(["/usr/bin/git", "-C", str(SOURCE), *args], "SOURCE_BINDING").decode().strip()
    require(git("rev-parse", "--show-toplevel") == str(SOURCE) and git("branch", "--show-current") == "main", "SOURCE_BINDING")
    require(git("rev-parse", "HEAD") == git("rev-parse", "origin/main") == expected and
            git("rev-parse", "HEAD^") == BASELINE and git("log", "-1", "--format=%s") == "PE-4: prepare Home Assistant association adapter deployment", "SOURCE_BINDING")
    require(git("rev-list", "--left-right", "--count", "HEAD...origin/main") == "0\t0" and
            git("status", "--porcelain=v1", "--untracked-files=all") == "", "SOURCE_BINDING")
    for op in ("MERGE_HEAD", "REBASE_HEAD", "CHERRY_PICK_HEAD", "REVERT_HEAD", "BISECT_LOG", "rebase-apply", "rebase-merge", "sequencer"):
        path = Path(git("rev-parse", "--git-path", op))
        require(not (path if path.is_absolute() else SOURCE / path).exists(), "SOURCE_BINDING")
    remote = git("remote", "get-url", "origin")
    require(remote == "https://github.com/jorgeazofeifa-creator/hioc.git", "SOURCE_BINDING")
    # Offline production deployment: independently approved exact commit supplies remote provenance.
    record_raw = (SOURCE / RECORD).read_bytes()
    require(record_raw == command(["/usr/bin/git", "-C", str(SOURCE), "show", expected + ":" + RECORD], "SOURCE_BINDING"), "SOURCE_BINDING")
    record = json.loads(record_raw)
    for item in record["source_bindings"]:
        raw = (SOURCE / item["path"]).read_bytes()
        require(sha(raw) == item["sha256"] and git("rev-parse", expected + ":" + item["path"]) == item["git_blob"], "SOURCE_BINDING")
    # Bind helper and record to the independently approved commit without circular hashes.
    require(Path(__file__).read_bytes() == command(["/usr/bin/git", "-C", str(SOURCE), "show", expected + ":tools/hioc-pe4-ha-association-deploy.py"], "SOURCE_BINDING"), "SOURCE_BINDING")
    manifest = {"dependencies": record["production_dependencies"], "deploy": record["deployment_files"]}
    manifest["deploy"] = [dict(i, bytes=(SOURCE / i["path"]).read_bytes()) for i in manifest["deploy"]]
    return manifest

def local_prerequisites():
    import pwd, grp
    require(sys.platform == "linux" and os.uname().nodename == "nutandpihole", "INVALID")
    user, group = pwd.getpwnam("jazofv1"), grp.getgrnam("jazofv1")
    require(os.getuid() == os.geteuid() == user.pw_uid and user.pw_uid > 0 and os.getegid() == group.gr_gid, "INVALID")
    require(not any(k.startswith(("HIOC_", "MQTT_")) or k.lower() in {"pi4_tools_home", "http_proxy", "https_proxy", "all_proxy", "no_proxy"} for k in os.environ), "INVALID")
    return user.pw_uid, group.gr_gid

def prerequisites():
    # Read-only crontab inspection, never install/remove a job.
    result = subprocess.run(["/usr/bin/crontab", "-l"], env=ENV, stdin=subprocess.DEVNULL, capture_output=True, timeout=5)
    require(len(result.stdout) + len(result.stderr) <= LIMIT and (result.returncode == 0 or
            result.returncode == 1 and result.stdout == b"" and result.stderr.strip() == b"no crontab for jazofv1"), "SCHEDULER_PRESENT")
    no_scheduler(result.stdout)
    site = ENVIRONMENT / "lib/python3.11/site-packages"
    require((HOME / "runtime/pe4/active").is_symlink() and (HOME / "runtime/pe4/active").resolve() == ENVIRONMENT and
            not list(site.glob("*.pth")) and not (site / "sitecustomize.py").exists() and not (site / "usercustomize.py").exists(), "RUNTIME_DRIFT")
    probe = """import sys,platform,sysconfig,json,importlib.util,importlib.metadata
from pathlib import Path
site=Path(sys.prefix)/'lib/python3.11/site-packages'
spec=importlib.util.find_spec('websockets')
d={x.metadata['Name'].lower().replace('_','-'):x.version for x in importlib.metadata.distributions(path=[str(site)])}
valid=spec is not None and spec.origin is not None and Path(spec.origin).resolve()==site/'websockets/__init__.py'
paths={Path('/usr/lib/python311.zip'),Path('/usr/lib/python3.11'),Path('/usr/lib/python3.11/lib-dynload'),site}
if valid:
 import websockets
 valid=websockets.__version__=='16.1.1' and Path(websockets.__file__).resolve()==site/'websockets/__init__.py'
valid=valid and all(Path(p).resolve() in paths for p in sys.path) and 'sitecustomize' not in sys.modules and 'usercustomize' not in sys.modules
print(json.dumps(dict(implementation=sys.implementation.name,python='.'.join(map(str,sys.version_info[:3])),architecture=platform.machine(),soabi=sysconfig.get_config_var('SOABI'),websockets=d.get('websockets'),prefix=str(Path(sys.prefix).resolve()),executable=str(Path(sys.executable).absolute()),isolated=bool(sys.flags.isolated),bytecode_disabled=bool(sys.flags.dont_write_bytecode),origins_valid=valid,distributions_valid=set(d)<= {'websockets','pip','setuptools'})))
"""
    runtime_identity(json.loads(command([str(INTERPRETER), "-I", "-B", "-c", probe], "RUNTIME_DRIFT")))
    output = command([str(INTERPRETER), "-I", "-B", str(SOURCE / "tools/hioc-pe4-ha-runtime-credential-validate.py"), "--runtime-operator"], "CREDENTIAL_INVALID")
    require(b"RESULT=PASS\n" in output and b"CREDENTIAL_READABLE_BY_RUNTIME_OPERATOR=TRUE\n" in output and
            b"NETWORK_CONNECTION_ATTEMPTED=FALSE\n" in output and b"HA_AUTHENTICATION_ATTEMPTED=FALSE\n" in output, "CREDENTIAL_INVALID")

EVIDENCE = {"TARGET": "PI3 NUT&PIHOLE", "SOURCE_BINDING": "PASS", "PRODUCTION_DEPENDENCIES": "PASS",
    "RUNTIME_VALIDATION": "PASS", "CREDENTIAL_LOCAL_VALIDATION": "PASS", "ENDPOINT_CONFIGURATION": "PASS",
    "STATE_DIRECTORY_VALIDATION": "PASS", "PREEXISTING_ASSOCIATION_STATE": "ABSENT",
    "MODULE_DEPLOYMENT": "PASS", "ENTRYPOINT_DEPLOYMENT": "PASS", "RUNTIME_GOVERNANCE_DEPLOYMENT": "PASS",
    "SCHEDULER_PRESENT_BEFORE": "FALSE", "SCHEDULER_DEPLOYMENT": "NOT_STARTED", "ADAPTER_EXECUTED": "FALSE",
    "HA_NETWORK_ATTEMPTED": "FALSE", "HA_AUTHENTICATION_ATTEMPTED": "FALSE", "PRODUCTION_DEPLOYMENT": "PASS",
    "ROLLBACK": "NOT_PERFORMED", "RESULT": "PASS"}

def evidence(commit, code="COMPLETE", transaction="NOT_STARTED"):
    commit = commit if re.fullmatch(r"[0-9a-f]{40}", commit) else "INVALID"
    result = dict(EVIDENCE, SOURCE_COMMIT=commit, ERROR_CODE=code, DEPLOYMENT_TRANSACTION=transaction)
    if code != "COMPLETE":
        for key, value in result.items():
            if value == "PASS": result[key] = "NOT_PROVEN"
        result.update(RESULT="FAIL", PRODUCTION_DEPLOYMENT="INCOMPLETE", PREEXISTING_ASSOCIATION_STATE="NOT_PROVEN", SCHEDULER_PRESENT_BEFORE="NOT_PROVEN")
    return result

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-commit", required=True)
    args = parser.parse_args(argv)
    transaction = "NOT_STARTED"
    try:
        uid, gid = local_prerequisites()
        manifest = source_binding(args.expected_commit)
        prerequisites()
        fs = NativeFS(HOME, uid, gid)
        # All source, dependencies, destinations, config and private state checked before mutation.
        prior, candidate = preflight(fs, manifest)
        toolkit_fs = NativeFS(Path("/home/jazofv1/pi4-tools"), uid, gid)
        toolkit = toolkit_fs.read("config/toolkit.conf")
        require(toolkit is not None, "CONFIG_CONFLICT")
        effective_configuration(toolkit, candidate)
        with fs.lock():
            prerequisites()
            transaction = "PREPARED_OR_INTERRUPTED"
            require(toolkit_fs.read("config/toolkit.conf") == toolkit, "CONFIG_CONFLICT")
            deploy(fs, manifest, args.expected_commit)
            transaction = "COMMITTED"
            effective_configuration(toolkit, fs.read(CONFIG))
            require(toolkit_fs.read("config/toolkit.conf") == toolkit, "CONFIG_CONFLICT")
            prerequisites()
            transaction = "COMMITTED"
        result = evidence(args.expected_commit, transaction=transaction)
        rc = 0
    except Failure as exc: result = evidence(args.expected_commit, exc.code, transaction); rc = 1
    except BaseException: result = evidence(args.expected_commit, "IO_FAILED", transaction); rc = 1
    for key, value in result.items(): print(key + "=" + value)
    return rc

if __name__ == "__main__": sys.exit(main())
