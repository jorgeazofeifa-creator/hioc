"""EXPERIMENTAL Windows fixture-only filesystem broker; no CLI or privilege backend.

Accepted Controller code is loaded unchanged into a private module with synthetic
identity constants. Nothing here authenticates a native peer or bypasses Linux DAC.
"""
import contextlib
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import tempfile
import threading
import uuid

ACCEPTED_CONTROLLER_SHA256 = "76b422edc73ed87baba94fef6fcfa8e197a564d4d8f57c95dba6b8a1624907d2"
TRANSACTION = "SYNTHETIC_PE73_BROKER_V1"
LIMIT = 2 * 1024 * 1024
MUTATIONS = {"BACKUP", "STAGE", "PUBLISH", "RESTORE", "REMOVE"}
OPERATIONS = MUTATIONS | {"SNAPSHOT", "READ"}
_FIXTURE_ROOTS = {}  # External fixture ownership, never a broker transaction authority.
FIELDS = {"version", "operation", "artifact", "area", "transaction", "operation_id",
          "source_sha256", "expected", "context", "payload_hex"}

class BrokerError(Exception):
    pass

def require(ok, code):
    if not ok:
        raise BrokerError(code)

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode()

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def parsed(raw):
    def pairs(items):
        value = {}
        for key, item in items:
            require(key not in value, "DUPLICATE_FIELD")
            value[key] = item
        return value
    require(type(raw) is bytes and len(raw) <= LIMIT * 3, "REQUEST_SIZE")
    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                          parse_constant=lambda _: (_ for _ in ()).throw(BrokerError("NONFINITE")))
    except (UnicodeError, ValueError, RecursionError):
        raise BrokerError("MALFORMED_JSON") from None

def load_fixture_controller():
    path = Path(__file__).with_name("hioc-pe73-pi3-delivery.py")
    require(digest(path.read_bytes()) == ACCEPTED_CONTROLLER_SHA256, "CONTROLLER_CHANGED")
    spec = importlib.util.spec_from_file_location("pe73_private_broker_fixture", path)
    d = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(d)
    source = {p: ("synthetic-candidate:" + p + "\n").encode() for p in d.ORDER}
    base = {p: ("synthetic-baseline:" + p + "\n").encode() for p in d.PRIOR}
    d.RELEASE = "f" * 40
    d.MANIFEST = [{"path": p, "sha256": digest(source[p]),
                   "git_blob": hashlib.sha1(("blob " + str(len(source[p])) + "\0").encode() + source[p]).hexdigest()}
                  for p in sorted(source)]
    d.PRIOR = {p: (digest(raw), d.MODES[p]) for p, raw in base.items()}
    d.CRON = ("synthetic-inventory", "synthetic-platform", "synthetic-incident")
    d.check_sources(source)
    return d, source, base

class FixtureDisk:
    """Real temporary Windows bytes; POSIX owner/mode are explicit fixture metadata.

    Fresh objects reopen the persisted image. Metadata contains no transaction phase.
    Only the accepted Controller writes the transaction journal.
    """
    def __init__(self, root, d):
        require(os.name == "nt" and root in _FIXTURE_ROOTS and
                _FIXTURE_ROOTS[root] == (root.stat().st_dev, root.stat().st_ino) and
                root.parent == Path(tempfile.gettempdir()) and not root.is_symlink(), "UNOWNED_FIXTURE_ROOT")
        self.root, self.d = root, d
        self.guard = threading.RLock()
        self.metadata_path = root / ".fixture-metadata.json"
        require(not self.metadata_path.is_symlink() and (not self.metadata_path.exists() or
                self.metadata_path.is_file() and self.metadata_path.stat().st_nlink == 1), "UNSAFE_FIXTURE_METADATA")
        self.metadata = json.loads(self.metadata_path.read_text()) if self.metadata_path.exists() else {}
        self.fixed = set(d.ORDER) | {d.TX + "/journal.json", d.TX + "/journal-next"}
        self.fixed |= {d.TX + "/" + kind + "-" + str(i) for kind in ("stage", "backup") for i in range(13)}
        self.fixed |= {str(PurePosixPath(p).parent / (".fixture-next-" + str(i))) for i, p in enumerate(d.ORDER)}
        self.trace_dir = root / ".broker-fixture-evidence"
        require(not self.trace_dir.is_symlink() and not getattr(self.trace_dir, "is_junction", lambda: False)(), "UNSAFE_EVIDENCE_DIRECTORY")
        self.trace_dir.mkdir(exist_ok=True)

    def path(self, relative):
        require(type(relative) is str and relative in self.fixed, "LOCAL_PATH_NOT_ALLOWLISTED")
        result = self.root / relative
        for item in (self.root, *reversed(result.relative_to(self.root).parents), result):
            item = item if item == self.root else self.root / item
            try:
                info = item.lstat()
            except FileNotFoundError:
                continue
            require(not stat.S_ISLNK(info.st_mode) and not getattr(info, "st_file_attributes", 0) & 0x400, "UNSAFE_REPARSE")
            require(item == result or stat.S_ISDIR(info.st_mode), "ANCESTOR_TYPE")
        return result

    def save_metadata(self):
        self.metadata_path.write_bytes(canonical(self.metadata))

    def ancestors(self, relative):
        target = self.path(relative)
        out = {}
        for parent in (target.parent, *target.parent.parents):
            if parent == self.root.parent:
                break
            info = parent.lstat()
            require(stat.S_ISDIR(info.st_mode) and not getattr(info, "st_file_attributes", 0) & 0x400, "ANCESTOR_TYPE")
            out[parent.relative_to(self.root).as_posix()] = {
                "st_dev": info.st_dev, "st_ino": info.st_ino, "st_uid": 1000,
                "st_gid": 1000, "mode": 0o755, "type": "DIRECTORY"}
        return out

    def snapshot(self, relative, mode=None):
        p = self.path(relative)
        parents = self.ancestors(relative)
        if not p.exists():
            return {"exists": False, "parents": parents}
        info = p.lstat()
        require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "UNSAFE_FILE")
        uid, gid, actual_mode = self.metadata.get(relative, [1000, 1000, 0o600])
        require(uid == gid == 1000 and not actual_mode & 0o7022 and (mode is None or mode == actual_mode), "OWNERSHIP_MODE")
        require(info.st_size <= LIMIT, "FILE_SIZE")
        raw = p.read_bytes()
        require(self.d.identity(info) == self.d.identity(p.lstat()), "READ_DRIFT")
        identity = self.d.identity(info)
        identity.update(st_uid=uid, st_gid=gid, mode=actual_mode)
        return {"exists": True, "parents": parents, "identity": identity, "sha256": digest(raw)}

    def read(self, relative, mode=0o600):
        before = self.snapshot(relative, mode)
        require(before["exists"], "FILE_MISSING")
        raw = self.path(relative).read_bytes()
        require(digest(raw) == before["sha256"] and self.snapshot(relative, mode) == before, "READ_DRIFT")
        return raw

    def write_new(self, relative, raw, mode=0o600, hook=lambda _: None, point="unused"):
        require(type(raw) is bytes and len(raw) <= LIMIT, "WRITE_SIZE")
        with self.path(relative).open("xb") as stream:
            half = len(raw) // 2
            stream.write(raw[:half]); stream.flush()
            self.metadata[relative] = [1000, 1000, mode]
            self.save_metadata()
            hook(point)
            stream.write(raw[half:]); stream.flush(); os.fsync(stream.fileno())
        hook("after_mutation_before_verification")
        require(self.read(relative, mode) == raw, "WRITE_NOT_VERIFIED")

    def transaction_present(self):
        return (self.root / self.d.TX).is_dir()

    def mkdir_tx(self):
        (self.root / self.d.TX).mkdir()

    def journal(self, value):
        # Sole controller-owned journal; no broker grant or trace authorizes this.
        self.write_new(self.d.TX + "/journal-next", self.d.canonical(value))
        os.replace(self.path(self.d.TX + "/journal-next"), self.path(self.d.TX + "/journal.json"))
        self.metadata[self.d.TX + "/journal.json"] = [1000, 1000, 0o600]
        self.save_metadata()

    @contextlib.contextmanager
    def mutex(self):
        with self.guard:
            yield

    def publish(self, path, raw, before, mode, hook):
        require(self.snapshot(path, mode if before["exists"] else None) == before, "TARGET_DRIFT")
        index = self.d.ORDER.index(path)
        temporary = str(PurePosixPath(path).parent / (".fixture-next-" + str(index)))
        self.write_new(temporary, raw, mode)
        hook("during_publication")
        require(self.snapshot(path, mode if before["exists"] else None) == before, "TARGET_DRIFT")
        if before["exists"]:
            os.replace(self.path(temporary), self.path(path))
        else:
            # Windows rename refuses an existing destination. This is NOT a
            # claim of native Linux renameat2 qualification.
            os.rename(self.path(temporary), self.path(path))
        self.metadata[path] = [1000, 1000, mode]; self.save_metadata()
        hook("after_mutation_before_verification")
        after = self.snapshot(path, mode)
        require(after["sha256"] == digest(raw), "PUBLICATION_NOT_VERIFIED")
        return after

    def remove_installed(self, path, expected, mode, hook):
        require(self.snapshot(path, mode) == expected, "TARGET_DRIFT")
        hook("during_rollback")
        require(self.snapshot(path, mode) == expected, "TARGET_DRIFT")
        self.path(path).unlink()
        hook("after_mutation_before_verification")
        return self.snapshot(path)

    def traces(self):
        files = list(self.trace_dir.iterdir())
        require(len(files) <= 512 and all(p.is_file() and not p.is_symlink() for p in files), "EVIDENCE_LIMIT")
        return [parsed(p.read_bytes()) for p in files]

    def consume_attempt(self, request):
        # Negative replay evidence only. It never represents transaction progress.
        intent = {k: request[k] for k in ("transaction", "operation", "artifact", "context")}
        for previous in self.traces():
            require(previous["operation_id"] != request["operation_id"], "REPLAYED_OPERATION")
            require(previous["intent_sha256"] != digest(canonical(intent)), "INTENT_ALREADY_ATTEMPTED")
        p = self.trace_dir / (request["operation_id"] + ".json")
        with p.open("xb") as stream:
            stream.write(canonical({"operation_id": request["operation_id"],
                "request_sha256": digest(canonical(request)), "intent_sha256": digest(canonical(intent)),
                "evidence_kind": "NONAUTHORITATIVE_ATTEMPT_ONLY"}))

class FixtureConsumers:
    def __init__(self, d):
        self.active = True
        self.session = uuid.uuid4().hex
        self.d = d
    def observe(self):
        return {"cron_sha256": digest(b"synthetic-cron"), "known_cron_commands": list(self.d.CRON),
                "coverage": "SYNTHETIC_ONLY", "partial_failure_exclusion": "FIXTURE_ONLY",
                "unlocked_asset_or_classification_callers": "EXTERNAL_FIXTURE_BOUNDARY"}
    def assert_active(self):
        require(self.active, "CONSUMER_BOUNDARY_NOT_ESTABLISHED")
    @contextlib.contextmanager
    def hold(self, observation):
        require(observation == self.observe(), "CONSUMER_DRIFT")
        self.assert_active()
        yield  # No broker operation or exception releases this external fixture.

class FixtureAuthority:
    """In-process object grants, NOT native peer authentication or credentials."""
    def __init__(self, disk, d, source, base, consumers):
        self.disk, self.d, self.source, self.base, self.consumers = disk, d, source, base, consumers
        self.controller = None
        self.grants, self.replies = {}, {}
        self._validated_journal = None

    def journal(self):
        if not self.disk.transaction_present():
            return None
        # Journal and backups are outside the package fence. Reuse the exact
        # accepted validator on that local read-only view, avoiding recursive
        # broker authorization during its backup-provenance reads.
        raw = self.disk.read(self.d.TX + "/journal.json")
        key = (digest(raw), canonical(self.disk.snapshot(self.d.TX + "/journal.json", 0o600)))
        if self._validated_journal is None or self._validated_journal[0] != key:
            value = self.d.Controller(self.disk, self.source, self.consumers)._journal()
            require(self.d.canonical(value) == raw, "JOURNAL_CHANGED_DURING_VALIDATION")
            self._validated_journal = (key, copy.deepcopy(value))
        # The cache is an optimization over freshly read secured bytes/identity,
        # never a phase authority or a substitute for reopening durable evidence.
        return copy.deepcopy(self._validated_journal[1])

    def context(self, operation):
        value = self.journal()
        authorization = None
        if value is not None:
            field = "prepare_authorization" if operation in {"BACKUP", "STAGE"} else (
                "rollback_authorization" if operation in {"RESTORE", "REMOVE"} else "commit_authorization")
            authorization = value[field]
        return {"journal_sha256": digest(canonical(value)) if value is not None else None,
                "authorization": authorization, "consumer_session": self.consumers.session}

    def resource(self, request):
        index = self.d.ORDER.index(request["artifact"])
        return request["artifact"] if request["area"] == "TARGET" else (
            self.d.TX + "/" + request["area"].lower() + "-" + str(index))

    def observation_binding(self, artifact, area):
        value = self.journal()
        recorded = None
        if value is not None and area == "TARGET":
            recorded = value["restored"].get(artifact, value["installed"].get(artifact, value["baseline"][artifact]))
        return {"kind": "OBSERVE", "recorded": recorded}

    def policy(self, request, inspect_actual=False):
        operation, artifact = request["operation"], request["artifact"]
        require(request["context"] == self.context(operation), "STALE_AUTHORIZATION_CONTEXT")
        self.d.check_sources(self.source)
        mode = self.d.MODES[artifact] if request["area"] == "TARGET" else 0o600
        if operation not in MUTATIONS:
            require(canonical(request["expected"]) == canonical(self.observation_binding(artifact, request["area"])), "STALE_OBSERVATION_BINDING")
            if inspect_actual:
                self.disk.snapshot(self.resource(request), mode)
            return
        if operation in {"STAGE", "BACKUP"}:
            require(request["expected"] == {"kind": "ABSENT"}, "EXPECTED_ABSENCE_REQUIRED")
            actual = {"exists": False}
            if inspect_actual:
                require(not self.disk.snapshot(self.resource(request), mode)["exists"], "STALE_EXPECTED_STATE")
        else:
            actual = request["expected"]
            if inspect_actual:
                require(canonical(self.disk.snapshot(self.resource(request), mode)) == canonical(actual), "STALE_EXPECTED_STATE")
        self.consumers.assert_active()  # Journal labels do not prove this boundary.
        value = self.journal()
        require(value is not None and request["context"]["authorization"] is not None, "NO_CONTROLLER_AUTHORIZATION")
        index = self.d.ORDER.index(artifact)
        if operation in {"BACKUP", "STAGE"}:
            require(value["state"] == "PREPARING" and not actual["exists"], "PREPARATION_PRECONDITION")
            for previous in self.d.ORDER[:index]:
                prior_stage = self.d.TX + "/stage-" + str(self.d.ORDER.index(previous))
                require(self.disk.read(prior_stage) == self.source[previous], "STAGING_ORDER")
            if operation == "BACKUP":
                require(artifact in self.base, "BACKUP_PROVENANCE")
                if inspect_actual:
                    require(self.disk.snapshot(artifact, mode=self.d.MODES[artifact]) == value["baseline"][artifact], "BACKUP_PROVENANCE")
                require(bytes.fromhex(request["payload_hex"]) == self.base[artifact], "BACKUP_IDENTITY")
            else:
                require(bytes.fromhex(request["payload_hex"]) == self.source[artifact], "SOURCE_IDENTITY")
                if artifact in self.base:
                    require(self.disk.read(self.d.TX + "/backup-" + str(index)) == self.base[artifact], "BACKUP_IDENTITY")
        elif operation == "PUBLISH":
            require(value["state"] == "COMMITTING" and value["pending"] == artifact and
                    artifact == self.d.ORDER[len(value["installed"])], "PUBLICATION_PRECONDITION")
            require(actual == value["baseline"][artifact], "TARGET_DRIFT")
            for i, path in enumerate(self.d.ORDER):
                require(self.disk.read(self.d.TX + "/stage-" + str(i)) == self.source[path], "STAGING_IDENTITY")
                if path in self.base:
                    require(self.disk.read(self.d.TX + "/backup-" + str(i)) == self.base[path], "BACKUP_IDENTITY")
        else:
            require(value["state"] == "ROLLING_BACK" and value["pending"] == artifact and
                    actual == value["installed"][artifact], "RESTORATION_PRECONDITION")
            remaining = [p for p in reversed(self.d.ORDER) if p in value["installed"] and p not in value["restored"]]
            require(remaining and remaining[0] == artifact, "RESTORATION_ORDER")
            if operation == "RESTORE":
                require(artifact in self.base and self.disk.read(self.d.TX + "/backup-" + str(index)) == self.base[artifact], "BACKUP_IDENTITY")
            else:
                require(artifact not in self.base, "REMOVAL_NOT_AUTHORIZED")

    def issue(self, request):
        self.policy(request)
        require(len(self.grants) < 64, "FIXTURE_GRANT_LIMIT")
        token = object()
        self.grants[token] = digest(canonical(request))
        return token

    def consume(self, token, request):
        require(token in self.grants, "NO_FIXTURE_GRANT")
        require(self.grants.pop(token) == digest(canonical(request)), "GRANT_REQUEST_MISMATCH")
        self.policy(request)

    def seal(self, reply):
        require(len(self.replies) < 64, "FIXTURE_REPLY_LIMIT")
        self.replies[id(reply)] = (reply, digest(canonical(reply)))
        return reply

    def verify_reply(self, reply, request):
        sealed = self.replies.pop(id(reply), None)
        require(sealed is not None and sealed[0] is reply and sealed[1] == digest(canonical(reply)), "UNAUTHENTICATED_FIXTURE_REPLY")
        require(set(reply) == {"version", "transaction", "operation_id", "request_sha256", "result", "synthetic_only"}
                and type(reply["version"]) is int and reply["version"] == 1 and reply["synthetic_only"] is True
                and reply["transaction"] == TRANSACTION and reply["operation_id"] == request["operation_id"]
                and reply["request_sha256"] == digest(canonical(request)), "REPLY_BINDING")
        result = reply["result"]
        if request["operation"] == "READ":
            require(type(result) is dict and set(result) == {"content_hex", "sha256"} and
                    type(result["content_hex"]) is str and len(result["content_hex"]) <= LIMIT * 2 and
                    re.fullmatch("(?:[0-9a-f]{2})*", result["content_hex"]) and
                    digest(bytes.fromhex(result["content_hex"])) == result["sha256"], "READ_RESULT_SCHEMA")
        else:
            require(type(result) is dict and type(result.get("exists")) is bool and
                    set(result) == ({"exists", "parents", "identity", "sha256"} if result["exists"] else {"exists", "parents"}), "SNAPSHOT_RESULT_SCHEMA")
            relative = PurePosixPath(self.resource(request))
            allowed_parents = {str(parent) for parent in relative.parents}
            parents = result["parents"]
            require(type(parents) is dict and set(parents) == allowed_parents, "PARENT_RESULT_SCHEMA")
            for item in parents.values():
                require(type(item) is dict and set(item) == {"st_dev", "st_ino", "st_uid", "st_gid", "mode", "type"} and
                        item["type"] == "DIRECTORY" and all(type(item[k]) is int and item[k] >= 0 for k in item if k != "type") and
                        item["st_uid"] == item["st_gid"] == 1000 and item["mode"] == 0o755, "PARENT_RESULT_SCHEMA")
            if result["exists"]:
                item = result["identity"]
                require(type(item) is dict and set(item) == {"st_dev", "st_ino", "st_uid", "st_gid", "mode", "type", "st_nlink", "st_size", "st_mtime_ns", "st_ctime_ns"} and
                        item["type"] == "REGULAR" and all(type(item[k]) is int and item[k] >= 0 for k in item if k != "type") and
                        item["st_uid"] == item["st_gid"] == 1000 and item["st_nlink"] == 1 and item["st_size"] <= LIMIT and
                        item["mode"] == (self.d.MODES[request["artifact"]] if request["area"] == "TARGET" else 0o600) and
                        type(result["sha256"]) is str and re.fullmatch("[0-9a-f]{64}", result["sha256"]), "FILE_RESULT_SCHEMA")
        return result

class Broker:
    """Finite artifact operations only; no transaction writer or consumer control."""
    def __init__(self, authority, fault=lambda point, request: None):
        self.a = authority
        self.fault = fault

    def validate(self, raw):
        request = parsed(raw)
        require(type(request) is dict and set(request) == FIELDS, "CLOSED_REQUEST")
        require(canonical(request) == raw, "NONCANONICAL_REQUEST")
        require(type(request["version"]) is int and request["version"] == 1, "REQUEST_VERSION")
        require(type(request["operation"]) is str and request["operation"] in OPERATIONS, "UNKNOWN_OPERATION")
        require(type(request["artifact"]) is str and request["artifact"] in self.a.d.ORDER, "ARTIFACT_NOT_ALLOWLISTED")
        require(request["transaction"] == TRANSACTION and type(request["operation_id"]) is str and
                re.fullmatch("[0-9a-f]{32}", request["operation_id"]), "TRANSACTION_OR_OPERATION_ID")
        require(type(request["area"]) is str and request["area"] in {"TARGET", "STAGE", "BACKUP"}, "UNKNOWN_AREA")
        operation = request["operation"]
        required_area = "STAGE" if operation == "STAGE" else "BACKUP" if operation == "BACKUP" else "TARGET"
        require(operation in {"SNAPSHOT", "READ"} or request["area"] == required_area, "OPERATION_AREA")
        require(type(request["expected"]) is dict and type(request["context"]) is dict and
                set(request["context"]) == {"journal_sha256", "authorization", "consumer_session"}, "CLOSED_BINDING")
        original = operation in {"BACKUP", "RESTORE"} or request["area"] == "BACKUP"
        require(not original or request["artifact"] in self.a.base, "NOT_A_REPLACEMENT")
        expected_digest = digest(self.a.base[request["artifact"]]) if original else digest(self.a.source[request["artifact"]])
        require(request["source_sha256"] == expected_digest, "SOURCE_IDENTITY")
        payload = request["payload_hex"]
        require(type(payload) is str and len(payload) <= LIMIT * 2 and re.fullmatch("(?:[0-9a-f]{2})*", payload)
                if operation in {"BACKUP", "STAGE"} else payload is None, "PAYLOAD_SCOPE")
        return request

    def exchange(self, raw, token):
        try:
            request = self.validate(raw)
            with self.a.disk.mutex():
                self.a.consume(token, request)
                if request["operation"] in MUTATIONS:
                    self.a.disk.consume_attempt(request)
                hook = lambda point: self.fault(point, request)
                hook("before_execution")
                self.a.policy(request, inspect_actual=True)
                hook("after_validation_before_mutation")
                result = self.execute(request, hook)
                hook("after_success_before_reply")
                return self.a.seal({"version": 1, "transaction": TRANSACTION,
                    "operation_id": request["operation_id"], "request_sha256": digest(raw),
                    "result": result, "synthetic_only": True})
        except BrokerError:
            raise
        except BaseException:
            raise BrokerError("OUTCOME_UNCONFIRMED") from None

    def execute(self, request, hook):
        disk, d = self.a.disk, self.a.d
        operation, artifact = request["operation"], request["artifact"]
        path = self.a.resource(request)
        mode = d.MODES[artifact] if request["area"] == "TARGET" else 0o600
        if operation in {"SNAPSHOT", "READ"}:
            hook("during_recovery_inspection")
            if operation == "SNAPSHOT":
                return disk.snapshot(path, mode)
            raw = disk.read(path, mode)
            allowed = {digest(self.a.source[artifact])}
            if artifact in self.a.base:
                allowed.add(digest(self.a.base[artifact]))
            require(digest(raw) in allowed, "UNVERIFIED_READ_IDENTITY")
            return {"content_hex": raw.hex(), "sha256": digest(raw)}
        if operation in {"BACKUP", "STAGE"}:
            raw = bytes.fromhex(request["payload_hex"])
            disk.write_new(path, raw, mode, hook, "during_backup" if operation == "BACKUP" else "during_staging")
            return disk.snapshot(path, mode)
        if operation in {"PUBLISH", "RESTORE"}:
            if operation == "RESTORE":
                hook("during_rollback")
            raw = self.a.source[artifact] if operation == "PUBLISH" else self.a.base[artifact]
            return disk.publish(path, raw, request["expected"], mode, hook)
        return disk.remove_installed(path, request["expected"], mode, hook)

class BrokerFS:
    """Unprivileged adapter exercising the accepted Controller.fs seam."""
    def __init__(self, broker):
        self.broker, self.a, self.local = broker, broker.a, broker.a.disk
        self.last_request = None
        self.last_token = None
        self.requests = []
        self.transport = broker.exchange

    def request(self, operation, artifact, area="TARGET", payload=None, expected=None):
        require(type(operation) is str and operation in OPERATIONS and type(artifact) is str and artifact in self.a.d.ORDER, "REQUEST_SCOPE")
        require(area in {"TARGET", "STAGE", "BACKUP"}, "REQUEST_AREA")
        require(not (operation in {"BACKUP", "RESTORE"} or area == "BACKUP") or artifact in self.a.base, "NOT_A_REPLACEMENT")
        require(len(self.requests) < 2048, "FIXTURE_REQUEST_LIMIT")
        index = self.a.d.ORDER.index(artifact)
        path = artifact if area == "TARGET" else self.a.d.TX + "/" + area.lower() + "-" + str(index)
        mode = self.a.d.MODES[artifact] if area == "TARGET" else 0o600
        request = {"version": 1, "operation": operation, "artifact": artifact, "area": area,
            "transaction": TRANSACTION, "operation_id": uuid.uuid4().hex,
            "source_sha256": digest(self.a.base[artifact] if operation in {"BACKUP", "RESTORE"} or area == "BACKUP" else self.a.source[artifact]),
            "expected": (self.a.observation_binding(artifact, area) if operation in {"READ", "SNAPSHOT"}
                else {"kind": "ABSENT"}) if expected is None else expected,
            "context": self.a.context(operation), "payload_hex": payload.hex() if payload is not None else None}
        self.last_request = copy.deepcopy(request)
        # Closed validation occurs BEFORE the fixture authority can issue any grant.
        self.broker.validate(canonical(request))
        token = self.a.issue(request)
        self.last_token = token
        self.requests.append(copy.deepcopy(request))
        reply = self.transport(canonical(request), token)
        return self.a.verify_reply(reply, request)

    def locate(self, path):
        if path in self.a.d.ORDER:
            return path, "TARGET"
        for i, artifact in enumerate(self.a.d.ORDER):
            for area in ("STAGE", "BACKUP"):
                if path == self.a.d.TX + "/" + area.lower() + "-" + str(i):
                    return artifact, area
        return None

    def snapshot(self, path, mode=None):
        located = self.locate(path)
        return self.request("SNAPSHOT", *located) if located else self.local.snapshot(path, mode)

    def read(self, path, mode=0o600):
        located = self.locate(path)
        if not located:
            return self.local.read(path, mode)
        result = self.request("READ", *located)
        raw = bytes.fromhex(result["content_hex"])
        require(digest(raw) == result["sha256"], "READ_REPLY_IDENTITY")
        return raw

    def write_new(self, path, raw, mode=0o600):
        located = self.locate(path)
        require(located is not None and located[1] in {"STAGE", "BACKUP"}, "NO_GENERIC_WRITE")
        return self.request(located[1], located[0], located[1], raw)

    def publish(self, path, raw, before, mode):
        require(path in self.a.d.ORDER and mode == self.a.d.MODES[path], "PUBLISH_SCOPE")
        operation = "PUBLISH" if raw == self.a.source[path] else "RESTORE"
        require(raw == (self.a.source[path] if operation == "PUBLISH" else self.a.base.get(path)), "PUBLISH_CONTENT")
        return self.request(operation, path, expected=before)

    def remove_installed(self, path, expected, mode):
        require(path in self.a.d.ORDER and mode == self.a.d.MODES[path], "REMOVE_SCOPE")
        return self.request("REMOVE", path, expected=expected)

    def transaction_present(self):
        return self.local.transaction_present()
    def mkdir_tx(self):
        return self.local.mkdir_tx()
    def journal(self, value):
        return self.local.journal(value)
    def mutex(self):
        return self.local.mutex()

class Fixture:
    """Creates its OWN Windows temporary root; there is no caller root override."""
    def __init__(self):
        require(os.name == "nt", "WINDOWS_FIXTURE_ONLY")
        self.d, self.source, self.base = load_fixture_controller()
        self.temp = tempfile.TemporaryDirectory(prefix="hioc-pe73-broker-fixture-")
        self.root = Path(self.temp.name)
        _FIXTURE_ROOTS[self.root] = (self.root.stat().st_dev, self.root.stat().st_ino)
        for path in ("pi4/bin", "pi4/lib/hioc", "backups"):
            (self.root / path).mkdir(parents=True, exist_ok=True)
        self.disk = FixtureDisk(self.root, self.d)
        for path, raw in self.base.items():
            self.disk.write_new(path, raw, self.d.MODES[path])
        self.consumers = FixtureConsumers(self.d)
        self.reopen()

    def reopen(self):
        # Destroy ALL broker/authority/adapter/controller request memory. Reopen
        # only the external fixture bytes/metadata; consumer boundary is external.
        self.disk = FixtureDisk(self.root, self.d)
        self.authority = FixtureAuthority(self.disk, self.d, self.source, self.base, self.consumers)
        self.broker = Broker(self.authority)
        self.fs = BrokerFS(self.broker)
        self.controller = self.d.Controller(self.fs, self.source, self.consumers)
        self.authority.controller = self.controller

    def prepare(self):
        before = self.d.preflight(self.fs, self.source, self.consumers)
        return self.controller.prepare("PREPARE_SYNTHETIC_BROKER", digest(self.d.canonical(before)))

    def commit(self):
        value = self.prepare()
        return self.controller.commit("COMMIT_SYNTHETIC_BROKER", value["journal_sha256"])

    def close(self):
        _FIXTURE_ROOTS.pop(self.root, None)
        self.temp.cleanup()
