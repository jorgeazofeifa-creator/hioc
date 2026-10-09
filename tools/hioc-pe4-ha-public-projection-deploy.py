"""PE-4 one-shot deployment; native entrypoint requires explicit authorization.

No runtime, network, credential or private-state code is executed by this tool.
The transaction controller accepts injected operations for synthetic testing.
"""
import contextlib
import hashlib
import json
import re

SOURCE = "/home/jazofv1/hioc-release-source"
TARGET = "/home/jazofv1/hioc"
PARENT = "6bfb689fc9e49de5d7ae17267f2b389e13f0bc1e"
IMPLEMENTATION = "c762745b428b28518cf4415f7399ff2cacb70c66"
SUBJECT = "PE-4: prepare public projection deployment"
RECORD = "governance/pe4/pe4-ha-association-public-projection-deployment-preparation.json"
SCHEMA = RECORD.replace(".json", ".schema.json")
TOOL = "tools/hioc-pe4-ha-public-projection-deploy.py"
TX = "backups/pe4-ha-public-projection-deployment-v1"
PREFIX = ".pe4-ha-public-projection-v1-"
LOCK = "/tmp/hioc-inventory-engine.lock"
CRON_SHA = "8f900f4679aa861b02e781a61927683db5900ddfe159d78c3831a1595ae7fe71"
INVENTORY = "*/30 * * * * flock -n /tmp/hioc-inventory-engine.lock /home/jazofv1/hioc/pi4/bin/hioc-inventory-engine.py"
ASSOCIATION = "5,35 * * * * /home/jazofv1/hioc/runtime/pe4/active/bin/python -I -B /home/jazofv1/hioc/pi4/bin/hioc-home-assistant-association.py >/dev/null 2>&1"
PLATFORM = "17 3 * * * flock -n /tmp/hioc-platform-status.lock /home/jazofv1/hioc/pi4/bin/hioc-platform-status.py"
MARKER = "# HIOC_PE4_HA_ASSOCIATION"
SET = (
 ("governance/pe4/pe4-home-assistant-public-projection.schema.json", "50369a904e83ace1c9d5c760ddc9c3e90a70c059725b4f238eaae4f0347185b3"),
 ("pi4/lib/hioc/home_assistant_public_projection.py", "2a1ec243048182327d40918f69a064e1be65233d75bb0dfcf3dd3b1d9ba7fe37"),
 ("pi4/bin/hioc-inventory-engine.py", "e956d635637cc30c4335321345480b6fb53c6264e6411b73f2aa7b8a2ef4a60d"),
)
PRIVATE = {
 "pi4/lib/hioc/home_assistant_association.py": "9a9be5812f3481146de7546875320eb6adec65ca5a2b3230ff5fec378892c7c1",
 "governance/pe4/pe4-home-assistant-association-state-v1.1.schema.json": "5cd060ffd0a7a2e0a2b3e61da50ec8e5a418f4251df7305f713c10701b0e6a5d",
 "pi4/bin/hioc-home-assistant-association.py": "005fae482a4e2c42b48bfb991abf14ddf1d9de60f81169a2ed1573a767958b8c",
}
# This is a reviewed Git candidate, never a claim about the current production host.
OLD_ENGINE = "06fa6d326ec75df92f0902da4360065b7767ee2a9848d7877c00c145d9d00f42"
LIMIT = 16 * 1024 * 1024
CRON_LIMIT = 65536
STAGES = frozenset(("NONE", "SOURCE_GATE", "TARGET_GATE", "BASELINE_GATE", "CRONTAB_BASELINE", "INVENTORY_QUIESCE", "INVENTORY_DRAIN", "STAGING", "SCHEMA_INSTALL", "HELPER_INSTALL", "ENGINE_INSTALL", "INSTALLED_SET_VERIFY", "CRONTAB_RESTORE", "FINAL_VERIFY"))
CODES = frozenset(("NONE", "AUTHORIZATION_REQUIRED", "INVALID_ARGUMENT", "SOURCE_BINDING", "UNSAFE_OBJECT", "BASELINE_REQUIRED", "BASELINE_MISMATCH", "CRONTAB_MISMATCH", "CRONTAB_FAILED", "BUSY", "TRANSACTION_CONFLICT", "IO_FAILED", "INTERRUPTED", "INSTALLED_MISMATCH", "ROLLBACK_FAILED"))
FALSE_FIELDS = ("ADAPTER_EXECUTED", "PUBLIC_PROJECTION_EXECUTED", "INVENTORY_ENGINE_EXECUTED", "MQTT_PUBLISHED", "HA_NETWORK_ATTEMPTED", "CREDENTIAL_ACCESSED")

class Failure(Exception):
    def __init__(self, code):
        self.code = code if code in CODES else "IO_FAILED"
        super().__init__(self.code)

def require(value, code="UNSAFE_OBJECT"):
    if not value: raise Failure(code)

def sha(raw): return hashlib.sha256(raw).hexdigest()
def canonical(value): return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode()

def strict_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "BASELINE_MISMATCH"); result[key] = value
        return result
    try:
        require(type(raw) is bytes and len(raw) <= LIMIT, "BASELINE_MISMATCH")
        return json.loads(raw.decode("utf8"), object_pairs_hook=pairs, parse_constant=lambda _: (_ for _ in ()).throw(Failure("BASELINE_MISMATCH")))
    except (ValueError, UnicodeError): raise Failure("BASELINE_MISMATCH") from None

def closed_schema(value):
    if type(value) is dict:
        return {"type":"object","additionalProperties":False,"required":sorted(value),"properties":{k:closed_schema(v) for k,v in value.items()}}
    if type(value) is list:
        return {"type":"array","items":False,"minItems":len(value),"maxItems":len(value),"prefixItems":[closed_schema(v) for v in value]}
    return {"const":value}

def check_closed(value,node):
    if "const" in node:
        require(type(value) is type(node["const"]) and value==node["const"],"SOURCE_BINDING"); return
    if node.get("type")=="object":
        require(type(value) is dict and node["additionalProperties"] is False and set(value)==set(node["required"])==set(node["properties"]),"SOURCE_BINDING")
        for key,child in node["properties"].items():check_closed(value[key],child)
    else:
        require(type(value) is list and node["items"] is False and len(value)==node["minItems"]==node["maxItems"]==len(node["prefixItems"]),"SOURCE_BINDING")
        for child,contract in zip(value,node["prefixItems"]):check_closed(child,contract)


def source_authority(value, commit):
    expected = {"host":"nutandpihole", "operator":"jazofv1", "source":SOURCE,
                "branch":"main", "head":commit, "origin":commit, "ahead":0,
                "behind":0, "clean":True, "active_operation":False,
                "subject":SUBJECT, "parent":PARENT, "implementation":IMPLEMENTATION,
                "tool":SOURCE + "/" + TOOL}
    require(type(commit) is str and re.fullmatch("[0-9a-f]{40}", commit), "SOURCE_BINDING")
    require(value == expected, "SOURCE_BINDING")

def cron_candidate(raw, expected_sha=CRON_SHA):
    require(type(raw) is bytes and 0 < len(raw) <= CRON_LIMIT and raw.endswith(b"\n") and b"\r" not in raw and b"\0" not in raw, "CRONTAB_MISMATCH")
    try: lines = raw.decode("utf8", "strict").splitlines(keepends=True)
    except UnicodeError: raise Failure("CRONTAB_MISMATCH") from None
    require(sha(raw) == expected_sha, "CRONTAB_MISMATCH")
    for text in (INVENTORY, ASSOCIATION, PLATFORM, MARKER):
        require(lines.count(text + "\n") == 1, "CRONTAB_MISMATCH")
    for line in lines:
        if not line.strip() or line.lstrip().startswith("#"): continue
        for needle, exact in (("hioc-inventory", INVENTORY), ("hioc-home-assistant-association", ASSOCIATION), ("hioc-platform-status", PLATFORM)):
            if needle in line: require(line == exact + "\n", "CRONTAB_MISMATCH")
        require("public-projection" not in line and "public_projection" not in line, "CRONTAB_MISMATCH")
    return "".join(line for line in lines if line != INVENTORY + "\n").encode("utf8")

def evidence(commit):
    result = {"RESULT":"FAIL", "ERROR_CODE":"NONE", "FAILURE_STAGE":"NONE",
      "SOURCE_COMMIT":commit, "DEPLOYMENT_PREPARATION_COMMIT":commit, "BASELINE_REPORT_SHA256":None,
      "INSTALL_ATTEMPTS":0, "INVENTORY_CRON_BASELINE_SHA256":None,
      "INVENTORY_CRON_MAINTENANCE_SHA256":None, "INVENTORY_CRON_FINAL_SHA256":None,
      "ROLLBACK_PERFORMED":False, "ROLLBACK_RESULT":"NOT_PERFORMED",
      "MUTATION_STATE":"NOT_ATTEMPTED", "MANUAL_REVIEW_REQUIRED":False, "STOP_REQUIRED":True}
    for key in (*FALSE_FIELDS, "INVENTORY_SCHEDULER_QUIESCED", "INVENTORY_LOCK_ACQUIRED", "PUBLIC_SCHEMA_INSTALLED", "PUBLIC_HELPER_INSTALLED", "INVENTORY_ENGINE_INSTALLED", "DEPLOYED_SET_VERIFIED", "CRONTAB_RESTORED", "ASSOCIATION_CRON_UNCHANGED", "PLATFORM_CRON_UNCHANGED"):
        result[key] = False
    return result

def execute(ops, commit, baseline, authorized=False):
    """Finite transaction. Operations own pinned descriptors and durable intent.

    No retry. Uncertain cron publication forbids automatic code rollback. An
    interruption retains the journal, even when no runtime file was installed.
    """
    out = evidence(commit); stage = "SOURCE_GATE"
    if not authorized:
        out.update(ERROR_CODE="AUTHORIZATION_REQUIRED", FAILURE_STAGE=stage); return out
    original = maintenance = old = None
    attempted = []; completed = []; restore_started = False; lock_held = False
    intent = False
    def restore():
        nonlocal restore_started, stage
        stage = "CRONTAB_RESTORE"; restore_started = True
        require(ops.cron_read() == maintenance, "CRONTAB_MISMATCH")
        ops.intent(stage)
        out["MUTATION_STATE"] = "UNKNOWN_AFTER_ATTEMPT"
        ops.cron_install(original)
        final = ops.cron_read(); require(final == original, "CRONTAB_MISMATCH")
        out.update(MUTATION_STATE="VERIFIED_RESTORED", CRONTAB_RESTORED=True,
                   INVENTORY_CRON_FINAL_SHA256=sha(final), INVENTORY_SCHEDULER_QUIESCED=False)
    try:
        ops.source(commit)
        stage = "TARGET_GATE"; ops.target()
        stage = "BASELINE_GATE"; require(baseline is not None, "BASELINE_REQUIRED")
        old = ops.baseline(baseline)
        stage = "CRONTAB_BASELINE"; original = ops.cron_read()
        maintenance = cron_candidate(original, ops.expected_cron_sha)
        require(baseline["crontab_sha256"] == sha(original), "BASELINE_MISMATCH")
        out.update(INVENTORY_CRON_BASELINE_SHA256=sha(original), INVENTORY_CRON_MAINTENANCE_SHA256=sha(maintenance), ASSOCIATION_CRON_UNCHANGED=True, PLATFORM_CRON_UNCHANGED=True)
        intent = True; ops.begin(commit, baseline, original, old)
        stage = "INVENTORY_QUIESCE"; ops.intent(stage)
        out["MUTATION_STATE"] = "UNKNOWN_AFTER_ATTEMPT"
        ops.cron_install(maintenance)
        require(ops.cron_read() == maintenance, "CRONTAB_MISMATCH")
        out.update(MUTATION_STATE="VERIFIED_MAINTENANCE", INVENTORY_SCHEDULER_QUIESCED=True)
        stage = "INVENTORY_DRAIN"; ops.intent(stage)
        with ops.inventory_lock():
            lock_held = True; out["INVENTORY_LOCK_ACQUIRED"] = True
            try:
                ops.recheck(baseline, old)
                for index, (path, digest) in enumerate(SET):
                    stage = "STAGING"; ops.intent(stage)
                    raw = ops.source_bytes(path); require(sha(raw) == digest, "SOURCE_BINDING")
                    ops.stage(path, raw, baseline)
                    stage = ("SCHEMA_INSTALL", "HELPER_INSTALL", "ENGINE_INSTALL")[index]
                    ops.intent(stage); attempted.append(path); out["INSTALL_ATTEMPTS"] += 1
                    ops.install(path, raw, baseline)
                    ops.verify(path, raw, baseline); completed.append(path)
                    out[("PUBLIC_SCHEMA_INSTALLED", "PUBLIC_HELPER_INSTALLED", "INVENTORY_ENGINE_INSTALLED")[index]] = True
                stage = "INSTALLED_SET_VERIFY"; ops.intent(stage); ops.installed(baseline)
                require(ops.cron_read() == maintenance, "CRONTAB_MISMATCH")
                out["DEPLOYED_SET_VERIFIED"] = True
                restore()
                stage = "FINAL_VERIFY"; ops.intent(stage)
                ops.installed(baseline)
                require(ops.cron_read() == original, "CRONTAB_MISMATCH")
                ops.finish(); intent = False
                out.update(RESULT="PASS", MUTATION_STATE="VERIFIED_DEPLOYED", FAILURE_STAGE="NONE")
            except BaseException as exc:
                failed_stage = stage
                # Never undo code after restoration was attempted: scheduler state
                # could permit execution once our lock is released.
                if not restore_started and not isinstance(exc, (KeyboardInterrupt, SystemExit)):
                    try:
                        require(ops.cron_read() == maintenance, "CRONTAB_MISMATCH")
                        ops.intent("ROLLBACK_BEFORE_RESTORE")
                        out["ROLLBACK_PERFORMED"] = bool(attempted)
                        ops.rollback(attempted, old, baseline)
                        ops.verify_baseline(baseline, old)
                        if attempted: out["ROLLBACK_RESULT"] = "VERIFIED"
                        restore(); ops.finish(); intent = False
                        out["MUTATION_STATE"] = "VERIFIED_RESTORED"
                    except BaseException:
                        out.update(ROLLBACK_RESULT="FAILED_OR_UNKNOWN", MANUAL_REVIEW_REQUIRED=True, MUTATION_STATE="UNKNOWN_AFTER_ATTEMPT")
                stage = failed_stage
                raise
            finally: lock_held = False
    except Failure as exc:
        out.update(ERROR_CODE=exc.code, FAILURE_STAGE=stage)
        failed_stage = stage
        if exc.code == "BUSY" and out["MUTATION_STATE"] == "VERIFIED_MAINTENANCE" and not attempted:
            try:
                restore(); ops.finish(); intent = False
            except BaseException:
                out.update(MANUAL_REVIEW_REQUIRED=True, MUTATION_STATE="UNKNOWN_AFTER_ATTEMPT")
            out["FAILURE_STAGE"] = failed_stage
    except (KeyboardInterrupt, SystemExit):
        out.update(ERROR_CODE="INTERRUPTED", FAILURE_STAGE=stage, MANUAL_REVIEW_REQUIRED=True)
    except BaseException:
        out.update(ERROR_CODE="IO_FAILED", FAILURE_STAGE=stage)
    if intent or out["MUTATION_STATE"] == "UNKNOWN_AFTER_ATTEMPT": out["MANUAL_REVIEW_REQUIRED"] = True
    # False means not verified; it does not assert absence after uncertain rollback.
    if out["MUTATION_STATE"] == "UNKNOWN_AFTER_ATTEMPT":
        out["ASSOCIATION_CRON_UNCHANGED"] = out["PLATFORM_CRON_UNCHANGED"] = False
    if out["ROLLBACK_PERFORMED"]:
        for key in ("PUBLIC_SCHEMA_INSTALLED", "PUBLIC_HELPER_INSTALLED", "INVENTORY_ENGINE_INSTALLED", "DEPLOYED_SET_VERIFIED"): out[key] = False
    return out

# Native methods are reached only after CLI authorization and Linux identity gates.
ENV = {"PATH":"/usr/bin:/bin", "HOME":"/home/jazofv1", "LANG":"C", "LC_ALL":"C", "GIT_OPTIONAL_LOCKS":"0"}
SECURITY_DEPENDENCY = "tools/hioc-pe4-ha-association-deploy.py"
SECURITY_SHA = "9f1903c99206348722584a976c57ac9e1bcbf53178e0c8d472719687259a48da"


def command(args, data=None, limit=LIMIT):
    """Linux bounded pipes; finite deadline; kill only our own failed child."""
    import os, selectors, subprocess, time
    require(data is None or len(data) <= CRON_LIMIT, "IO_FAILED")
    process = subprocess.Popen(args, stdin=subprocess.PIPE if data is not None else subprocess.DEVNULL,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=ENV, close_fds=True)
    outputs = {"out":bytearray(), "err":bytearray()}; selector = selectors.DefaultSelector()
    try:
        for stream, name in ((process.stdout,"out"),(process.stderr,"err")):
            os.set_blocking(stream.fileno(),False); selector.register(stream,selectors.EVENT_READ,name)
        offset = 0
        if data is not None:
            os.set_blocking(process.stdin.fileno(),False); selector.register(process.stdin,selectors.EVENT_WRITE,"in")
        deadline = time.monotonic() + 15
        while selector.get_map():
            require(time.monotonic() < deadline, "IO_FAILED")
            for key, _ in selector.select(min(.1,max(0,deadline-time.monotonic()))):
                stream, name = key.fileobj, key.data
                if name == "in":
                    if offset < len(data): offset += os.write(stream.fileno(),data[offset:offset+4096])
                    if offset == len(data): selector.unregister(stream); stream.close()
                else:
                    chunk = os.read(stream.fileno(),min(65536,limit+1-len(outputs[name])))
                    if not chunk: selector.unregister(stream); stream.close()
                    else:
                        outputs[name].extend(chunk); require(len(outputs[name]) <= limit, "IO_FAILED")
        rc = process.wait(timeout=max(.01,deadline-time.monotonic()))
        require(rc == 0, "IO_FAILED")
        return bytes(outputs["out"])
    finally:
        selector.close()
        for stream in (process.stdin,process.stdout,process.stderr):
            if stream is not None: stream.close()
        if process.poll() is None: process.kill()
        process.wait()


def native_fs_class(source_raw):
    """Use only the exact accepted no-follow reader definitions, no legacy main."""
    import ast, contextlib, errno, os, stat
    from pathlib import Path
    require(sha(source_raw) == SECURITY_SHA, "SOURCE_BINDING")
    tree = ast.parse(source_raw)
    cls = next(node for node in tree.body if isinstance(node,ast.ClassDef) and node.name == "NativeFS")
    allowed = {"__init__","security","directory","read","info","names"}
    cls.body = [node for node in cls.body if isinstance(node,ast.FunctionDef) and node.name in allowed]
    require({node.name for node in cls.body} == allowed, "SOURCE_BINDING")
    module = ast.Module(body=[cls],type_ignores=[])
    namespace = dict(contextlib=contextlib,errno=errno,os=os,stat=stat,Path=Path,require=require,Failure=Failure,LIMIT=LIMIT)
    exec(compile(ast.fix_missing_locations(module),"accepted-native-fs","exec"),namespace)
    class PinnedFS(namespace["NativeFS"]):
        @contextlib.contextmanager
        def directory(self,relative=""):
            require(not relative.startswith("/") and ".." not in relative.split("/"),"UNSAFE_OBJECT")
            descriptors = []; chain = []
            try:
                fd = os.open("/",os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC)
                descriptors.append(fd); self.security(fd,True)
                for part in (*self.root.parts[1:],*filter(None,relative.split("/"))):
                    child = os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC,dir_fd=fd)
                    descriptors.append(child); chain.append((fd,part,child))
                    self.security(child,True); fd = child
                yield fd
                for parent,name,child in chain:
                    named = os.stat(name,dir_fd=parent,follow_symlinks=False)
                    held = self.security(child,True)
                    require((named.st_dev,named.st_ino)==(held.st_dev,held.st_ino),"UNSAFE_OBJECT")
            finally:
                for fd in reversed(descriptors): os.close(fd)
    return PinnedFS


def file_identity(info):
    import stat
    return {"uid":info.st_uid,"gid":info.st_gid,"mode":stat.S_IMODE(info.st_mode),
            "device":info.st_dev,"inode":info.st_ino,"links":info.st_nlink}


class NativeOps:
    expected_cron_sha = CRON_SHA
    def __init__(self, commit):
        import os, pwd, grp, socket, sys
        from pathlib import Path
        require(sys.platform == "linux" and os.name == "posix", "SOURCE_BINDING")
        self.commit = commit
        require(socket.gethostname() == "nutandpihole", "SOURCE_BINDING")
        user = pwd.getpwnam("jazofv1"); group = grp.getgrnam("jazofv1")
        require(os.getuid() == os.geteuid() == user.pw_uid and os.getgid() == os.getegid() == group.gr_gid and user.pw_uid > 0, "SOURCE_BINDING")
        require(pwd.getpwuid(user.pw_uid).pw_name == "jazofv1" and grp.getgrgid(group.gr_gid).gr_name == "jazofv1", "SOURCE_BINDING")
        require(Path(SOURCE).resolve() == Path(SOURCE) and Path(__file__).resolve() == Path(SOURCE)/TOOL, "SOURCE_BINDING")
        require(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode, "SOURCE_BINDING")
        self.uid, self.gid = user.pw_uid, group.gr_gid
        # Git-bound dependency is verified before defining any accepted FS method.
        raw = self.git("show",commit+":"+SECURITY_DEPENDENCY,raw=True)
        cls = native_fs_class(raw)
        self.source_fs = cls(SOURCE,self.uid,self.gid); self.fs = cls(TARGET,self.uid,self.gid)
        require(self.source_fs.read(SECURITY_DEPENDENCY) == raw, "SOURCE_BINDING")
        self.stages = {}; self.provenance = {}; self.tx_owned = False; self.tx_files = {}
        self.lock_fd = None; self.saved_baseline = None; self.record = None

    def git(self, *args, raw=False):
        value = command(["/usr/bin/git","-c","core.fsmonitor=false","-C",SOURCE,*args])
        return value if raw else value.decode("utf8","strict").strip()

    def source(self, commit):
        import os, socket
        from pathlib import Path
        require(commit == self.commit, "SOURCE_BINDING")
        gitdir = Path(self.git("rev-parse","--absolute-git-dir"))
        operations = ("MERGE_HEAD","CHERRY_PICK_HEAD","REVERT_HEAD","BISECT_START","rebase-merge","rebase-apply","sequencer","index.lock")
        require(gitdir == Path(SOURCE)/".git", "SOURCE_BINDING")
        count = self.git("rev-list","--left-right","--count","HEAD...origin/main").split()
        value = {"host":socket.gethostname(),"operator":"jazofv1","source":str(Path(SOURCE).resolve()),
                 "branch":self.git("branch","--show-current"),"head":self.git("rev-parse","HEAD"),
                 "origin":self.git("rev-parse","origin/main"),"ahead":int(count[0]),"behind":int(count[1]),
                 "clean":not self.git("status","--porcelain=v1","--untracked-files=all"),
                 "active_operation":any(os.path.lexists(gitdir/name) for name in operations),
                 "subject":self.git("show","-s","--format=%s",commit),
                 "parent":self.git("show","-s","--format=%P",commit),
                 "implementation":self.git("rev-parse",PARENT+"^"),"tool":str(Path(__file__).resolve())}
        source_authority(value,commit)
        for path, digest in (*SET,*PRIVATE.items()):
            raw = self.source_bytes(path); require(sha(raw) == digest, "SOURCE_BINDING")
            require(self.git("show",IMPLEMENTATION+":"+path,raw=True) == raw, "SOURCE_BINDING")
        record_raw = self.source_bytes(RECORD); schema_raw = self.source_bytes(SCHEMA)
        self.record = strict_json(record_raw); schema = strict_json(schema_raw)
        expected_schema = {"$schema":"https://json-schema.org/draft/2020-12/schema", "title":"PE-4 public projection deployment preparation", **closed_schema(self.record)}
        require(canonical(schema)==canonical(expected_schema),"SOURCE_BINDING"); check_closed(self.record,schema)
        require(self.record["status"] == "PASS/CLOSED" and self.record["starting_head"] == PARENT and self.record["implementation_commit"] == IMPLEMENTATION, "SOURCE_BINDING")
        for binding in self.record["artifacts"]:
            raw = self.source_bytes(binding["path"])
            require(sha(raw) == binding["sha256"] and self.git("rev-parse",commit+":"+binding["path"]) == binding["git_blob"], "SOURCE_BINDING")
        for binding in self.record["historical_authority"]:
            require(sha(self.git("show",binding["commit"]+":"+binding["path"],raw=True)) == binding["sha256"], "SOURCE_BINDING")

    def source_bytes(self,path):
        raw = self.git("show",self.commit+":"+path,raw=True)
        require(self.source_fs.read(path) == raw, "SOURCE_BINDING")
        return raw

    def target(self):
        import ctypes
        from pathlib import Path
        require(Path(TARGET).resolve() == Path(TARGET), "BASELINE_MISMATCH")
        with self.fs.directory(): pass
        require(self.fs.info(TX) is None, "TRANSACTION_CONFLICT")
        for path, _ in SET:
            parent = str(Path(path).parent)
            with self.fs.directory(parent) as fd:
                info = self.fs.security(fd,True)
                require(info.st_uid == self.uid and info.st_gid == self.gid and info.st_mode & 0o200, "UNSAFE_OBJECT")
            require(not any(name.startswith(PREFIX) for name in self.fs.names(parent)), "TRANSACTION_CONFLICT")
        with self.fs.directory("backups") as fd:
            info = self.fs.security(fd,True)
            require(info.st_uid == self.uid and info.st_gid == self.gid and info.st_mode & 0o200, "UNSAFE_OBJECT")
        require(hasattr(ctypes.CDLL(None),"renameat2"), "UNSAFE_OBJECT")

    def private(self):
        result = {}
        for path, digest in PRIVATE.items():
            raw = self.fs.read(path); require(raw is not None and sha(raw) == digest, "BASELINE_MISMATCH")
            mode = 0o755 if path.endswith("/hioc-home-assistant-association.py") else 0o644
            require(self.fs.read(path,mode) == raw, "BASELINE_MISMATCH")
            result[path] = file_identity(self.fs.info(path))
        return result

    def runtime(self):
        """Read-only metadata binding, never launches either interpreter."""
        import os, stat
        from pathlib import Path
        environment = "runtime/pe4/environments/cpython311-websockets16.1.1-lock-v1"
        with self.fs.directory("runtime/pe4") as fd:
            info = os.stat("active",dir_fd=fd,follow_symlinks=False)
            require(stat.S_ISLNK(info.st_mode) and info.st_uid == self.uid and info.st_gid == self.gid, "BASELINE_MISMATCH")
            require(info.st_nlink == 1,"BASELINE_MISMATCH")
            link = os.readlink("active",dir_fd=fd)
            require((Path(TARGET)/"runtime/pe4"/link).resolve() == Path(TARGET)/environment, "BASELINE_MISMATCH")
            require(os.stat("active",dir_fd=fd,follow_symlinks=False) == info,"BASELINE_MISMATCH")
        values = {"active":{"target":link,**file_identity(info)}}
        with self.fs.directory(environment) as fd:
            values["environment"] = file_identity(self.fs.security(fd,True))
        with self.fs.directory(environment+"/bin") as fd:
            executable = os.stat("python",dir_fd=fd,follow_symlinks=False)
            require(executable.st_uid in (0,self.uid) and executable.st_nlink == 1,"BASELINE_MISMATCH")
            if stat.S_ISLNK(executable.st_mode):
                target = os.readlink("python",dir_fd=fd)
                require((Path(TARGET)/environment/"bin"/target).resolve() == Path("/usr/bin/python3.11"),"BASELINE_MISMATCH")
                values["interpreter"] = {"target":target,**file_identity(executable)}
            else:
                require(stat.S_ISREG(executable.st_mode) and not stat.S_IMODE(executable.st_mode)&0o7022,"BASELINE_MISMATCH")
                values["interpreter"] = {"sha256":sha(self.fs.read(environment+"/bin/python")),**file_identity(executable)}
        with self.fs.directory("state/inventory/associations") as fd:
            values["association_directory"] = file_identity(self.fs.security(fd,True,0o700))
        lock = "state/inventory/associations/.home_assistant.lock"
        self.fs.read(lock,0o600); require(self.fs.info(lock) is not None, "BASELINE_MISMATCH")
        values["association_lock"] = file_identity(self.fs.info(lock))
        return values

    @contextlib.contextmanager
    def inventory_file(self):
        import os, stat
        fd = parent = None
        try:
            parent = os.open("/tmp",os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC)
            info = os.fstat(parent)
            require(stat.S_ISDIR(info.st_mode) and info.st_uid == 0 and stat.S_IMODE(info.st_mode) == 0o1777, "UNSAFE_OBJECT")
            fd = os.open("hioc-inventory-engine.lock",os.O_RDONLY|os.O_NONBLOCK|os.O_NOFOLLOW|os.O_CLOEXEC,dir_fd=parent)
            held = self.fs.security(fd)
            require(held.st_uid == self.uid and held.st_gid == self.gid, "UNSAFE_OBJECT")
            named = os.stat("hioc-inventory-engine.lock",dir_fd=parent,follow_symlinks=False)
            require(file_identity(held) == file_identity(named), "UNSAFE_OBJECT")
            yield fd
            require(file_identity(self.fs.security(fd)) == file_identity(os.stat("hioc-inventory-engine.lock",dir_fd=parent,follow_symlinks=False)), "UNSAFE_OBJECT")
        finally:
            if fd is not None: os.close(fd)
            if parent is not None: os.close(parent)

    def lock_identity(self):
        import os
        with self.inventory_file() as fd: return file_identity(os.fstat(fd))

    @contextlib.contextmanager
    def inventory_lock(self):
        import fcntl, os
        with self.inventory_file() as fd:
            try: fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
            except BlockingIOError: raise Failure("BUSY") from None
            self.lock_fd = fd
            try: yield
            finally:
                self.lock_fd = None; fcntl.flock(fd,fcntl.LOCK_UN)

    def observe_baseline(self):
        import stat
        self.target()
        for path, _ in SET[:2]: require(self.fs.info(path) is None, "BASELINE_MISMATCH")
        engine = SET[2][0]; old = self.fs.read(engine)
        require(old is not None and sha(old) == OLD_ENGINE, "BASELINE_MISMATCH")
        info = self.fs.info(engine)
        require(info.st_uid == self.uid and info.st_gid == self.gid and stat.S_IMODE(info.st_mode) & 0o100 and not stat.S_IMODE(info.st_mode) & 0o7022, "UNSAFE_OBJECT")
        inventory = self.fs.read("state/inventory/inventory.json")
        require(inventory is not None, "BASELINE_MISMATCH")
        value = strict_json(inventory)
        require(type(value) is dict and type(value.get("devices")) is list and all(type(d) is dict and "home_assistant" not in d for d in value["devices"]) and "home_assistant" not in value, "BASELINE_MISMATCH")
        return {"version":"1.0", "preparation_commit":self.commit, "production_root":TARGET,
                "engine_sha256":sha(old), "engine":file_identity(info), "private":self.private(),
                "runtime":self.runtime(), "inventory_lock":self.lock_identity(), "crontab_sha256":CRON_SHA}

    def baseline(self,value):
        require(type(value) is dict and self.observe_baseline() == value, "BASELINE_MISMATCH")
        self.saved_baseline = value
        return self.fs.read(SET[2][0])

    def recheck(self,value,old):
        # Transaction namespace is now ours, so do not call target()/observe_baseline().
        require(self.lock_fd is not None, "BUSY")
        self.verify_baseline(value,old)
        require(self.lock_identity() == value["inventory_lock"], "BASELINE_MISMATCH")
        for path,_ in SET[:2]: require(self.fs.info(path) is None, "BASELINE_MISMATCH")
        inventory = strict_json(self.fs.read("state/inventory/inventory.json"))
        require(type(inventory.get("devices")) is list and all(type(d) is dict and "home_assistant" not in d for d in inventory["devices"]) and "home_assistant" not in inventory, "BASELINE_MISMATCH")

    def verify_baseline(self,value,old):
        require(self.fs.read(SET[2][0],value["engine"]["mode"]) == old and sha(old) == OLD_ENGINE, "BASELINE_MISMATCH")
        for path,_ in SET[:2]: require(self.fs.info(path) is None, "BASELINE_MISMATCH")
        require(self.private() == value["private"] and self.runtime() == value["runtime"], "BASELINE_MISMATCH")

    def installed_review(self,baseline):
        require(baseline["preparation_commit"] == self.commit,"BASELINE_MISMATCH")
        for path,digest in SET:
            raw = self.fs.read(path,self.mode(path,baseline))
            require(raw is not None and sha(raw)==digest,"INSTALLED_MISMATCH")
        require(self.private()==baseline["private"] and self.runtime()==baseline["runtime"] and self.lock_identity()==baseline["inventory_lock"],"BASELINE_MISMATCH")
        cron_candidate(self.cron_read())
        self.target()
        for path,digest in SET:
            require(sha(self.fs.read(path,self.mode(path,baseline)))==digest,"INSTALLED_MISMATCH")

    def cron_read(self):
        try: return command(["/usr/bin/crontab","-l"],limit=CRON_LIMIT)
        except Failure: raise Failure("CRONTAB_FAILED") from None

    def cron_install(self,raw):
        try: command(["/usr/bin/crontab","-"],data=raw,limit=CRON_LIMIT)
        except Failure: raise Failure("CRONTAB_FAILED") from None

    def write_new(self,path,raw,mode):
        import os
        from pathlib import Path
        p = Path(path)
        with self.fs.directory(str(p.parent)) as parent:
            fd = os.open(p.name,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW|os.O_CLOEXEC,mode,dir_fd=parent)
            try:
                os.fchmod(fd,mode); self.fs.security(fd,mode=mode)
                view = memoryview(raw)
                while view:
                    size = os.write(fd,view); require(size > 0,"IO_FAILED"); view = view[size:]
                os.fsync(fd)
            finally: os.close(fd)
            os.fsync(parent)
        require(self.fs.read(path,mode) == raw, "INSTALLED_MISMATCH")
        if path.startswith(TX+"/"):self.tx_files[path] = {"identity":file_identity(self.fs.info(path)),"sha256":sha(raw)}

    def begin(self,commit,baseline,cron,old):
        import os
        with self.fs.directory("backups") as fd:
            os.mkdir(TX.split("/")[-1],0o700,dir_fd=fd); self.tx_owned = True; os.fsync(fd)
        self.intent("PREPARED")
        self.write_new(TX+"/crontab-original",cron,0o600)
        self.write_new(TX+"/engine-original",old,0o600)

    def intent(self,stage):
        import os
        require(self.tx_owned,"TRANSACTION_CONFLICT")
        raw = canonical({"version":"1.0","commit":self.commit,"stage":stage,"stages":self.stages,"provenance":self.provenance})
        self.write_new(TX+"/intent-next",raw,0o600)
        with self.fs.directory(TX) as fd:
            existing = self.fs.info(TX+"/intent")
            if existing is not None:
                require(TX+"/intent" in self.tx_files and file_identity(existing)==self.tx_files[TX+"/intent"]["identity"],"TRANSACTION_CONFLICT")
            os.replace("intent-next","intent",src_dir_fd=fd,dst_dir_fd=fd); os.fsync(fd)
            self.tx_files[TX+"/intent"] = self.tx_files.pop(TX+"/intent-next")

    def mode(self,path,baseline): return baseline["engine"]["mode"] if path == SET[2][0] else 0o644

    def stage(self,path,raw,baseline):
        import secrets
        from pathlib import Path
        require(self.lock_fd is not None,"BUSY")
        name = str(Path(path).parent/PREFIX) + secrets.token_hex(8)
        require(path not in self.stages,"TRANSACTION_CONFLICT")
        self.stages[path] = name; self.intent("STAGING")
        self.write_new(name,raw,self.mode(path,baseline))
        self.provenance[path] = file_identity(self.fs.info(name)); self.intent("STAGED")

    def install(self,path,raw,baseline):
        import ctypes, os
        from pathlib import Path
        require(self.lock_fd is not None,"BUSY")
        p = Path(path); staged = Path(self.stages[path])
        require(self.fs.read(str(staged),self.mode(path,baseline)) == raw and file_identity(self.fs.info(str(staged))) == self.provenance[path], "INSTALLED_MISMATCH")
        with self.fs.directory(str(p.parent)) as fd:
            if path == SET[2][0]:
                require(self.fs.read(path) == self.fs.read(TX+"/engine-original",0o600) and file_identity(self.fs.info(path)) == baseline["engine"], "BASELINE_MISMATCH")
                os.replace(staged.name,p.name,src_dir_fd=fd,dst_dir_fd=fd)
            else:
                require(self.fs.info(path) is None,"BASELINE_MISMATCH")
                rename = ctypes.CDLL(None,use_errno=True).renameat2
                rename.argtypes = [ctypes.c_int,ctypes.c_char_p,ctypes.c_int,ctypes.c_char_p,ctypes.c_uint]; rename.restype = ctypes.c_int
                require(rename(fd,os.fsencode(staged.name),fd,os.fsencode(p.name),1) == 0,"INSTALLED_MISMATCH")
            os.fsync(fd)
        self.verify(path,raw,baseline)

    def verify(self,path,raw,baseline):
        require(self.fs.read(path,self.mode(path,baseline)) == raw and file_identity(self.fs.info(path)) == self.provenance[path],"INSTALLED_MISMATCH")

    def installed(self,baseline):
        require(self.lock_fd is not None,"BUSY")
        for path,digest in SET:
            raw = self.fs.read(path,self.mode(path,baseline)); require(raw is not None and sha(raw) == digest,"INSTALLED_MISMATCH")
            if self.provenance: require(file_identity(self.fs.info(path)) == self.provenance[path],"INSTALLED_MISMATCH")
        require(self.private() == baseline["private"] and self.runtime() == baseline["runtime"] and self.lock_identity() == baseline["inventory_lock"],"BASELINE_MISMATCH")

    def unlink_known(self,path,identity):
        import os
        from pathlib import Path
        p = Path(path)
        with self.fs.directory(str(p.parent)) as fd:
            require(file_identity(self.fs.info(path)) == identity,"TRANSACTION_CONFLICT")
            os.unlink(p.name,dir_fd=fd); os.fsync(fd)

    def rollback(self,attempted,old,baseline):
        import os, secrets
        from pathlib import Path
        require(self.lock_fd is not None,"BUSY")
        for path in reversed(attempted):
            info = self.fs.info(path)
            if path == SET[2][0]:
                raw = self.fs.read(path)
                if raw == old:
                    require(file_identity(info) == baseline["engine"],"TRANSACTION_CONFLICT"); continue
                require(path in self.provenance and file_identity(info) == self.provenance[path] and sha(raw) == dict(SET)[path],"TRANSACTION_CONFLICT")
                staged = str(Path(path).parent/PREFIX)+secrets.token_hex(8)
                self.stages["rollback-engine"] = staged; self.intent("ROLLBACK_ENGINE")
                self.write_new(staged,old,baseline["engine"]["mode"])
                p = Path(path)
                with self.fs.directory(str(p.parent)) as fd:
                    require(file_identity(self.fs.info(path)) == self.provenance[path],"TRANSACTION_CONFLICT")
                    os.replace(Path(staged).name,p.name,src_dir_fd=fd,dst_dir_fd=fd); os.fsync(fd)
                require(self.fs.read(path,baseline["engine"]["mode"]) == old,"INSTALLED_MISMATCH")
            elif info is not None:
                require(path in self.provenance and sha(self.fs.read(path)) == dict(SET)[path],"TRANSACTION_CONFLICT")
                self.unlink_known(path,self.provenance[path])
        self.verify_baseline(baseline,old)

    def finish(self):
        import os
        from pathlib import Path
        require(self.tx_owned,"TRANSACTION_CONFLICT")
        # Only this invocation's exact bounded names are eligible for cleanup.
        for path,name in self.stages.items():
            info = self.fs.info(name)
            if info is not None:
                require(path in self.provenance,"TRANSACTION_CONFLICT")
                self.unlink_known(name,self.provenance[path])
        expected = {"intent","crontab-original","engine-original"}
        require(set(self.fs.names(TX)) == expected,"TRANSACTION_CONFLICT")
        with self.fs.directory(TX) as fd:
            for name in sorted(expected):
                path = TX+"/"+name
                require(path in self.tx_files and file_identity(self.fs.info(path))==self.tx_files[path]["identity"] and sha(self.fs.read(path,0o600))==self.tx_files[path]["sha256"],"TRANSACTION_CONFLICT")
                os.unlink(name,dir_fd=fd)
            os.fsync(fd)
        with self.fs.directory("backups") as fd:
            os.rmdir(Path(TX).name,dir_fd=fd); os.fsync(fd)
        self.tx_owned = False
        for path,_ in SET:
            require(not any(n.startswith(PREFIX) for n in self.fs.names(str(Path(path).parent))),"TRANSACTION_CONFLICT")


def parse_args(args):
    # Closed grammar avoids argparse echoing arbitrary arguments or paths.
    require(len(args) == 7 and args[0] == "--preparation-commit" and args[2] == "--baseline-report" and args[4] == "--baseline-sha256" and args[6] == "--deploy-authorized","INVALID_ARGUMENT")
    require(re.fullmatch("[0-9a-f]{40}",args[1]) and re.fullmatch("[0-9a-f]{64}",args[5]),"INVALID_ARGUMENT")
    require(args[3] == "/home/jazofv1/pe4-public-projection-baseline.json","INVALID_ARGUMENT")
    return args[1],args[3],args[5]


def main(args=None):
    import sys
    args = list(sys.argv[1:] if args is None else args)
    commit = None; out = evidence(None); stage = "SOURCE_GATE"
    if "--deploy-authorized" not in args:
        out.update(ERROR_CODE="AUTHORIZATION_REQUIRED",FAILURE_STAGE="SOURCE_GATE")
    else:
        try:
            commit,path,digest = parse_args(args)
            ops = NativeOps(commit); ops.source(commit); stage = "BASELINE_GATE"
            # Baseline receipt is outside source and production, descriptor-read only.
            receipt_fs = type(ops.fs)("/home/jazofv1",ops.uid,ops.gid)
            raw = receipt_fs.read("pe4-public-projection-baseline.json",0o600)
            require(raw is not None and sha(raw) == digest,"BASELINE_REQUIRED")
            receipt = strict_json(raw)
            require(receipt["RESULT"] == "PASS" and receipt["MODE"] == "BASELINE" and receipt["STOP_REQUIRED"] is True,"BASELINE_REQUIRED")
            baseline = receipt["BASELINE"]
            out = execute(ops,commit,baseline,authorized=True)
            out["BASELINE_REPORT_SHA256"] = digest
        except Failure as exc:
            out = evidence(commit); out.update(ERROR_CODE=exc.code,FAILURE_STAGE=stage)
        except BaseException:
            out = evidence(commit); out.update(ERROR_CODE="IO_FAILED",FAILURE_STAGE=stage)
    sys.stdout.write(canonical(out).decode("utf8")); return 0 if out["RESULT"] == "PASS" else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
