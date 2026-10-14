"""Private POSIX store for PE-5 configured relationships; no network or collectors."""
import contextlib
import hashlib
import os
import stat
import uuid
from pathlib import Path

from . import configured_association as model
from .configured_association_schemas import schemas

PRODUCTION_ROOT = Path("/home/jazofv1/hioc")
DOMAINS = {
    "CONFIGURED_MAPPING_SOURCE": ("config/enrichment/mqtt_mappings.json", "config/enrichment/mqtt_mappings.durability.json"),
    "GENERATED_RELATIONSHIP_OUTPUT": ("state/enrichment/service_associations/current.json", "state/enrichment/service_associations/current.durability.json"),
}
SOURCE = "CONFIGURED_MAPPING_SOURCE"
OUTPUT = "GENERATED_RELATIONSHIP_OUTPUT"
INVENTORY = "state/inventory/inventory.json"
LOCK = "state/enrichment/service_associations/.lock"


class PosixFS:
    """Small syscall seam. Production requires real POSIX no-follow and flock."""
    def __init__(self):
        if os.name != "posix" or not hasattr(os, "O_NOFOLLOW") or not hasattr(os, "O_DIRECTORY"):
            raise model.AssociationError("WRITE_FAILED", "POSIX_CAPABILITY_UNAVAILABLE")
        if not {os.open, os.stat, os.rename, os.unlink, os.mkdir} <= os.supports_dir_fd:
            raise model.AssociationError("WRITE_FAILED", "POSIX_CAPABILITY_UNAVAILABLE")
        try:
            import fcntl
            if not callable(fcntl.flock) or not all(hasattr(fcntl, x) for x in ("LOCK_EX", "LOCK_NB", "LOCK_UN")):
                raise ImportError()
        except (ImportError, AttributeError):
            raise model.AssociationError("WRITE_FAILED", "POSIX_CAPABILITY_UNAVAILABLE") from None

    def directory(self, path):
        path = Path(path)
        if not path.is_absolute() or ".." in path.parts:
            raise model.AssociationError("SOURCE_METADATA_INVALID")
        fd = os.open("/", os.O_RDONLY | os.O_DIRECTORY)
        try:
            for part in path.parts[1:]:
                child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
                os.close(fd); fd = child
            return fd
        except BaseException:
            os.close(fd)
            raise

    def child_directory(self, fd, name):
        return os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)

    def mkdir(self, fd, name):
        os.mkdir(name, 0o700, dir_fd=fd)

    def statdir(self, fd):
        return os.fstat(fd)

    def close_dir(self, fd):
        os.close(fd)

    def statat(self, fd, name):
        return os.stat(name, dir_fd=fd, follow_symlinks=False)

    def openat(self, fd, name, flags, mode=0o600):
        return os.open(name, flags | os.O_NOFOLLOW | os.O_NONBLOCK, mode, dir_fd=fd)

    def fstat(self, fd):
        return os.fstat(fd)

    def chmod(self, fd):
        os.fchmod(fd, 0o600)

    def sync(self, fd, phase):
        os.fsync(fd)

    def syncdir(self, fd, phase):
        os.fsync(fd)

    def replace(self, fd, before, after, phase):
        os.replace(before, after, src_dir_fd=fd, dst_dir_fd=fd)

    def unlink(self, fd, name):
        os.unlink(name, dir_fd=fd)

    def flock(self, fd, unlock=False):
        import fcntl
        fcntl.flock(fd, fcntl.LOCK_UN if unlock else fcntl.LOCK_EX | fcntl.LOCK_NB)


def fingerprint(s):
    return (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns,
            s.st_mode, s.st_uid, s.st_gid, s.st_nlink)


class Snapshot:
    def __init__(self, path, data, info):
        self.path, self.data, self.info = path, data, fingerprint(info)
        self.sha256 = hashlib.sha256(data).hexdigest()


class Store:
    """Root injection exists for repository fixtures, never CLI/env configuration."""
    def __init__(self, root=PRODUCTION_ROOT, owner_uid=None, fs=None):
        self.root = Path(root)
        self.fs = fs if fs is not None else PosixFS()
        if owner_uid is None:
            import pwd
            owner_uid = pwd.getpwnam("jazofv1").pw_uid
            if os.geteuid() != owner_uid:
                raise model.AssociationError("SOURCE_METADATA_INVALID")
        self.uid = owner_uid

    def path(self, relative):
        path = self.root / relative
        if not self.root.is_absolute() or ".." in path.parts:
            raise model.AssociationError("SOURCE_METADATA_INVALID")
        return path

    @contextlib.contextmanager
    def parent(self, path, private=True):
        fd = self.fs.directory(Path(path).parent)
        try:
            s = self.fs.statdir(fd)
            if not stat.S_ISDIR(s.st_mode):
                raise model.AssociationError("SOURCE_METADATA_INVALID")
            if private and (s.st_uid != self.uid or stat.S_IMODE(s.st_mode) != 0o700):
                raise model.AssociationError("SOURCE_METADATA_INVALID")
            yield fd
        finally:
            self.fs.close_dir(fd)

    @contextlib.contextmanager
    def initialize_directories(self):
        """Only approved initial source installation enters this fixed bootstrap.
        Existing directories are never chmod/chown repaired. No primary rollback.
        Hold anchors until source publication finishes; race checks also precede
        mkdir and primary publication. Failed attempts may leave safe empty dirs.
        """
        anchors = []
        def check():
            for path, fd, identity, private in anchors:
                info = self.fs.statdir(fd)
                self.bootstrap_directory(info, private)
                if (info.st_dev, info.st_ino) != identity:
                    raise model.AssociationError("SOURCE_CHANGED")
                current = self.fs.directory(path)
                try:
                    visible = self.fs.statdir(current)
                    self.bootstrap_directory(visible, private)
                    if (visible.st_dev, visible.st_ino) != identity:
                        raise model.AssociationError("SOURCE_CHANGED")
                finally:
                    self.fs.close_dir(current)
        def attach(path, fd, private):
            anchors.append((path, fd, None, private))
            info = self.fs.statdir(fd)
            self.bootstrap_directory(info, private)
            anchors[-1] = (path, fd, (info.st_dev, info.st_ino), private)
        def child(path, parent_fd, private, create=False):
            check()
            try:
                fd = self.fs.child_directory(parent_fd, path.name)
            except FileNotFoundError:
                if not create:
                    raise
                try:
                    self.fs.mkdir(parent_fd, path.name)
                except FileExistsError:
                    # Another approved initializer may win mkdir, never adopt
                    # an unsafe replacement or normalize its permissions.
                    pass
                fd = self.fs.child_directory(parent_fd, path.name)
            attach(path, fd, private)
            check()
            if create:
                # Certify surviving safe directory entries after partial/restart
                # bootstrap as well as newly created entries.
                self.fs.syncdir(fd, "BOOTSTRAP_CHILD")
                self.fs.syncdir(parent_fd, "BOOTSTRAP_PARENT")
        try:
            attach(self.root, self.fs.directory(self.root), False)
            root_fd = anchors[-1][1]
            child(self.root / "config", root_fd, False)
            config_fd = anchors[-1][1]
            child(self.root / "config/enrichment", config_fd, True, True)
            child(self.root / "state", root_fd, False)
            state_fd = anchors[-1][1]
            child(self.root / "state/enrichment", state_fd, True, True)
            enrichment_fd = anchors[-1][1]
            child(self.root / "state/enrichment/service_associations", enrichment_fd, True, True)
            check()
            yield check
        except model.AssociationError:
            raise
        except OSError:
            raise model.AssociationError("WRITE_FAILED", "INITIALIZATION_INFRASTRUCTURE_FAILED") from None
        finally:
            for unused, fd, unused_identity, unused_private in reversed(anchors):
                self.fs.close_dir(fd)

    def bootstrap_directory(self, info, private):
        mode = stat.S_IMODE(info.st_mode)
        if (not stat.S_ISDIR(info.st_mode) or info.st_uid != self.uid
                or (mode != 0o700 if private else bool(mode & 0o022) or mode & 0o700 != 0o700)):
            raise model.AssociationError("SOURCE_METADATA_INVALID")

    def safe_file(self, s, private=True):
        if not stat.S_ISREG(s.st_mode) or s.st_nlink != 1:
            raise model.AssociationError("SOURCE_METADATA_INVALID")
        if private and (s.st_uid != self.uid or stat.S_IMODE(s.st_mode) != 0o600):
            raise model.AssociationError("SOURCE_METADATA_INVALID")

    def read(self, path, maximum, private=True, absent=False):
        try:
            with self.parent(path, private) as d:
                try:
                    first = self.fs.statat(d, path.name)
                except FileNotFoundError:
                    if absent:
                        return None
                    raise
                self.safe_file(first, private)
                if first.st_size > maximum:
                    raise model.AssociationError("SOURCE_SCHEMA_INVALID")
                fd = self.fs.openat(d, path.name, os.O_RDONLY)
                try:
                    opened = self.fs.fstat(fd); self.safe_file(opened, private)
                    if fingerprint(first) != fingerprint(opened):
                        raise model.AssociationError("SOURCE_CHANGED")
                    chunks, total = [], 0
                    while True:
                        part = os.read(fd, min(65536, maximum + 1 - total))
                        if not part:
                            break
                        chunks.append(part); total += len(part)
                        if total > maximum:
                            raise model.AssociationError("SOURCE_SCHEMA_INVALID")
                    after = self.fs.fstat(fd)
                    if fingerprint(after) != fingerprint(opened) or fingerprint(self.fs.statat(d, path.name)) != fingerprint(after):
                        raise model.AssociationError("SOURCE_CHANGED")
                    return Snapshot(path, b"".join(chunks), after)
                finally:
                    os.close(fd)
        except model.AssociationError:
            raise
        except (OSError, ValueError):
            raise model.AssociationError("SOURCE_UNREADABLE") from None

    def unchanged(self, snapshot, code):
        try:
            if snapshot is None:
                return
            maximum = model.SOURCE_LIMIT if snapshot.path == self.path(DOMAINS[SOURCE][0]) else model.OUTPUT_LIMIT
            fresh = self.read(snapshot.path, maximum, private=snapshot.path != self.path(INVENTORY))
            if fresh.info != snapshot.info or fresh.data != snapshot.data:
                raise model.AssociationError(code)
        except model.AssociationError:
            raise model.AssociationError(code) from None

    @contextlib.contextmanager
    def lock(self):
        path = self.path(LOCK)
        fd = None
        try:
            with self.parent(path) as d:
                try:
                    fd = self.fs.openat(d, path.name, os.O_RDWR | os.O_CREAT | os.O_EXCL)
                    self.fs.chmod(fd)
                except FileExistsError:
                    fd = self.fs.openat(d, path.name, os.O_RDWR)
                self.safe_file(self.fs.fstat(fd))
                self.fs.flock(fd)
                try:
                    yield
                finally:
                    self.fs.flock(fd, unlock=True)
        except BlockingIOError:
            raise model.AssociationError("OVERLAP_SKIPPED") from None
        except model.AssociationError:
            raise
        except OSError:
            raise model.AssociationError("WRITE_FAILED", "LOCK_UNAVAILABLE") from None
        finally:
            if fd is not None:
                os.close(fd)

    def descriptor(self, domain, value):
        return dict(sha256=model.digest(value),
                    source_revision=value["revision"] if domain == SOURCE else value["configured"]["revision"])

    def validate_primary(self, domain, value):
        if domain == SOURCE:
            model.validate_source(value)
        else:
            model.validate_envelope(value)
        return value

    def read_domain(self, domain):
        primary, metadata = [self.path(p) for p in DOMAINS[domain]]
        limit = model.SOURCE_LIMIT if domain == SOURCE else model.OUTPUT_LIMIT
        a = self.read(primary, limit, absent=True)
        b = self.read(metadata, 8192, absent=True)
        value = self.validate_primary(domain, model.strict_json(a.data, limit, "PRIOR_STATE_INVALID" if domain == OUTPUT else "SOURCE_SCHEMA_INVALID")) if a else None
        meta = model.strict_json(b.data, 8192, "WRITE_FAILED") if b else None
        if meta is not None:
            model.shape(meta, schemas()["metadata_schema"], "WRITE_FAILED")
            if meta["domain"] != domain or b.data != model.canonical(meta):
                raise model.AssociationError("WRITE_FAILED", "DURABILITY_BINDING_INVALID")
        if a and a.data != model.canonical(value):
            raise model.AssociationError("PRIOR_STATE_INVALID" if domain == OUTPUT else "SOURCE_SCHEMA_INVALID")
        return value, meta, a, b

    def confirmed(self, domain, allow_initial=False, resync=False):
        value, meta, primary, witness = self.read_domain(domain)
        if value is None and meta is None and allow_initial:
            return None, None, None
        if value is None or meta is None or meta["state"] != "CONFIRMED" or meta["confirmed"] != self.descriptor(domain, value):
            raise model.AssociationError("WRITE_FAILED", "RECOVERY_REQUIRED")
        if resync:
            self.resync(primary.path, domain + "_ANCHOR")
            self.resync(witness.path, domain + "_METADATA_ANCHOR")
        return value, meta["confirmed"], primary

    def resync(self, path, phase):
        with self.parent(path) as d:
            fd = self.fs.openat(d, path.name, os.O_RDWR)
            try:
                self.safe_file(self.fs.fstat(fd))
                self.fs.sync(fd, phase + "_FILE")
                self.fs.syncdir(d, phase + "_PARENT")
            finally:
                os.close(fd)

    def atomic(self, path, data, phase, before_replace=None):
        """One replacement; caller determines authority. Never rolls primary back."""
        with self.parent(path) as d:
            try:
                self.safe_file(self.fs.statat(d, path.name))
            except FileNotFoundError:
                pass
            name = ".hioc-" + uuid.uuid4().hex + ".tmp"
            fd, owned = None, None
            try:
                fd = self.fs.openat(d, name, os.O_WRONLY | os.O_CREAT | os.O_EXCL)
                self.fs.chmod(fd); owned = self.fs.fstat(fd); self.safe_file(owned)
                view = memoryview(data)
                while view:
                    size = os.write(fd, view)
                    if size <= 0:
                        raise OSError("short write")
                    view = view[size:]
                self.fs.sync(fd, phase + "_FILE")
                os.close(fd); fd = None
                if before_replace:
                    before_replace()
                # Directory path must still resolve to this anchored parent.
                check = self.fs.directory(path.parent)
                try:
                    current = self.fs.statdir(check); anchored = self.fs.statdir(d)
                    if (current.st_dev, current.st_ino) != (anchored.st_dev, anchored.st_ino):
                        raise model.AssociationError("SOURCE_CHANGED")
                finally:
                    self.fs.close_dir(check)
                try:
                    self.safe_file(self.fs.statat(d, path.name))
                except FileNotFoundError:
                    pass
                self.fs.replace(d, name, path.name, phase + "_REPLACE")
                try:
                    self.fs.syncdir(d, phase + "_PARENT")
                except OSError:
                    raise model.AssociationError("WRITE_FAILED", phase + "_PARENT") from None
            finally:
                if fd is not None:
                    os.close(fd)
                if owned is not None:
                    try:
                        s = self.fs.statat(d, name)
                        if (s.st_dev, s.st_ino, s.st_uid) == (owned.st_dev, owned.st_ino, owned.st_uid):
                            self.safe_file(s); self.fs.unlink(d, name)
                    except FileNotFoundError:
                        pass

    def metadata(self, domain, state, confirmed, candidate, transaction_id):
        meta = dict(schema_version="1.0", domain=domain, state=state, transaction_id=transaction_id,
                    confirmed=confirmed, candidate=candidate)
        model.shape(meta, schemas()["metadata_schema"], "WRITE_FAILED")
        return meta

    def publish(self, domain, value, before_replace=None, recovery=False, initial=False):
        self.validate_primary(domain, value)
        primary, metadata = [self.path(p) for p in DOMAINS[domain]]
        if recovery:
            # Preserve only validated identity descriptors, never guess from visible bytes.
            try:
                meta_snapshot = self.read(metadata, 8192, absent=True)
                meta = model.strict_json(meta_snapshot.data, 8192, "WRITE_FAILED") if meta_snapshot else None
                if meta:
                    model.shape(meta, schemas()["metadata_schema"], "WRITE_FAILED")
                    if meta["domain"] != domain or meta_snapshot.data != model.canonical(meta):
                        raise model.AssociationError("WRITE_FAILED")
                old = meta["confirmed"] if meta else None
            except model.AssociationError as error:
                if error.code in ("SOURCE_METADATA_INVALID", "SOURCE_UNREADABLE", "SOURCE_CHANGED"):
                    raise
                # Malformed metadata has no usable anchor; only explicitly approved
                # bootstrap permits a new lineage, without anti-rollback claims.
                if not initial:
                    raise
                old = None
                meta = None
            if domain == SOURCE and meta:
                for anchor in (meta["confirmed"], meta["candidate"]):
                    if anchor and self.descriptor(domain, value) != anchor and value["revision"] <= anchor["source_revision"]:
                        raise model.AssociationError("SOURCE_REVISION_ROLLBACK")
        else:
            unused, old, unused_snapshot = self.confirmed(domain, allow_initial=initial, resync=True)
        candidate = self.descriptor(domain, value)
        transaction_id = "dur_" + uuid.uuid4().hex
        phase = "PRE_REPLACEMENT_FAILURE"
        try:
            pending = self.metadata(domain, "PENDING", old, candidate, transaction_id)
            self.atomic(metadata, model.canonical(pending), "PENDING")
            try:
                def guarded_replace():
                    if not recovery:
                        if unused_snapshot is not None:
                            self.unchanged(unused_snapshot, "SOURCE_CHANGED" if domain == SOURCE else "PRIOR_STATE_INVALID")
                        elif self.read(primary, model.SOURCE_LIMIT if domain == SOURCE else model.OUTPUT_LIMIT, absent=True) is not None:
                            raise model.AssociationError("SOURCE_CHANGED")
                    if before_replace:
                        before_replace()
                self.atomic(primary, model.canonical(value), "PRIMARY", guarded_replace)
            except model.AssociationError as error:
                if error.phase == "PRIMARY_PARENT":
                    raise model.AssociationError("WRITE_FAILED", "INDETERMINATE_DURABILITY") from None
                raise
            phase = "CONFIRMATION_METADATA_UNCONFIRMED"
            written = self.read(primary, model.SOURCE_LIMIT if domain == SOURCE else model.OUTPUT_LIMIT)
            if written.data != model.canonical(value):
                raise model.AssociationError("WRITE_FAILED")
            confirmed = self.metadata(domain, "CONFIRMED", candidate, None, transaction_id)
            self.atomic(metadata, model.canonical(confirmed), "CONFIRMATION")
            return "CONFIRMED_DURABLE_CURRENT"
        except model.AssociationError as error:
            if error.phase == "INDETERMINATE_DURABILITY":
                raise
            raise model.AssociationError(error.code, phase) from None
        except OSError:
            raise model.AssociationError("WRITE_FAILED", phase) from None

    def recover(self, domain, approved, validate_current):
        if approved is not True:
            raise model.AssociationError("WRITE_FAILED", "OPERATOR_APPROVAL_REQUIRED")
        value, meta, primary, unused = self.read_domain(domain)
        if value is None or meta is None or self.descriptor(domain, value) not in (meta["confirmed"], meta["candidate"]):
            raise model.AssociationError("WRITE_FAILED", "RECOVERY_REQUIRED")
        validate_current(value)
        # Persistence recertification only: no primary replace and no timestamp refresh.
        try:
            self.resync(primary.path, "RECOVERY_PRIMARY")
        except OSError:
            raise model.AssociationError("WRITE_FAILED", "RECOVERY_REQUIRED") from None
        candidate = self.descriptor(domain, value)
        confirmed = self.metadata(domain, "CONFIRMED", candidate, None, meta["transaction_id"])
        try:
            self.atomic(self.path(DOMAINS[domain][1]), model.canonical(confirmed), "RECOVERY_CONFIRMATION")
        except (OSError, model.AssociationError):
            raise model.AssociationError("WRITE_FAILED", "CONFIRMATION_METADATA_UNCONFIRMED") from None
        return "CONFIRMED_DURABLE_CURRENT"

    def input_inventory(self):
        snapshot = self.read(self.path(INVENTORY), model.OUTPUT_LIMIT, private=False)
        return model.strict_json(snapshot.data, model.OUTPUT_LIMIT, "INVENTORY_INVALID"), snapshot

    def file_token(self, relative):
        path = self.path(relative)
        try:
            with self.parent(path, private=False) as d:
                try:
                    return fingerprint(self.fs.statat(d, path.name))
                except FileNotFoundError:
                    return None
        except (OSError, model.AssociationError):
            return "UNREADABLE"

    def source_token(self):
        # Metadata-only token also tracks malformed/unavailable source changes.
        tokens = []
        for relative in DOMAINS[SOURCE]:
            path = self.path(relative)
            try:
                with self.parent(path, private=False) as d:
                    parent = self.fs.statdir(d)
                    try:
                        value = fingerprint(self.fs.statat(d, path.name))
                    except FileNotFoundError:
                        value = None
                    tokens.append((fingerprint(parent), value))
            except (OSError, model.AssociationError):
                tokens.append("UNREADABLE")
        return tuple(tokens)

    def source_state(self):
        try:
            value, anchor, snapshot = self.confirmed(SOURCE, allow_initial=True)
            return value, snapshot, None if value is not None else "SOURCE_ABSENT"
        except model.AssociationError as error:
            try:
                raw_snapshot = self.read(self.path(DOMAINS[SOURCE][0]), model.SOURCE_LIMIT, absent=True)
            except model.AssociationError:
                raw_snapshot = None
            return None, raw_snapshot, error.code

    def composer(self, evaluated_at, recovery=False, approved=False):
        if recovery and approved is not True:
            raise model.AssociationError("WRITE_FAILED", "OPERATOR_APPROVAL_REQUIRED")
        with self.lock():
            inventory_snapshot = None
            try:
                inventory_snapshot = self.read(self.path(INVENTORY), model.OUTPUT_LIMIT, private=False)
                inventory = model.strict_json(inventory_snapshot.data, model.OUTPUT_LIMIT, "INVENTORY_INVALID")
            except model.AssociationError:
                inventory = None
            inventory_token = self.file_token(INVENTORY)
            source, source_snapshot, source_error = self.source_state()
            source_token = self.source_token()
            if recovery:
                prior = None
            else:
                try:
                    prior, anchor, unused = self.confirmed(OUTPUT, allow_initial=True, resync=True)
                except model.AssociationError:
                    raise model.AssociationError("PRIOR_STATE_INVALID", "RECOVERY_REQUIRED") from None
            result = model.compose(inventory, source, evaluated_at, prior, source_error)
            def unchanged():
                if self.file_token(INVENTORY) != inventory_token:
                    raise model.AssociationError("INVENTORY_INVALID")
                if inventory_snapshot:
                    self.unchanged(inventory_snapshot, "INVENTORY_INVALID")
                else:
                    # Invalid/absent inventory remains unavailable; a new appearance aborts.
                    try:
                        self.input_inventory()
                    except model.AssociationError:
                        pass
                    else:
                        raise model.AssociationError("INVENTORY_INVALID")
                if self.source_token() != source_token:
                    raise model.AssociationError("SOURCE_CHANGED")
                if source_snapshot:
                    self.unchanged(source_snapshot, "SOURCE_CHANGED")
                again, unused_snapshot, again_error = self.source_state()
                if again != source or again_error != source_error:
                    raise model.AssociationError("SOURCE_CHANGED")
            self.publish(OUTPUT, result, unchanged, recovery=recovery, initial=True)
            return result

    def recovery_revision_floor(self, source, confirmed_anchors):
        candidate = self.descriptor(SOURCE, source)
        known_source_identities = list(confirmed_anchors)
        floors = []
        for domain in (SOURCE, OUTPUT):
            try:
                data = self.read(self.path(DOMAINS[domain][1]), 8192, absent=True)
                if data is None:
                    continue
                meta = model.strict_json(data.data, 8192, "WRITE_FAILED")
                model.shape(meta, schemas()["metadata_schema"], "WRITE_FAILED")
                if meta["domain"] != domain or data.data != model.canonical(meta):
                    continue
                for item in (meta["confirmed"], meta["candidate"]):
                    if item is not None and item["source_revision"] is not None:
                        floors.append(item["source_revision"])
                        if domain == SOURCE:
                            known_source_identities.append(item)
            except model.AssociationError:
                # Invalid metadata is not invented evidence. The source-domain
                # publisher separately refuses unsafe metadata and requires
                # explicit initialization for malformed lineage.
                continue
        if floors:
            floor = max(floors)
            if source["revision"] < floor:
                raise model.AssociationError("SOURCE_REVISION_ROLLBACK")
            if source["revision"] == floor and candidate not in known_source_identities:
                raise model.AssociationError("SOURCE_REVISION_ROLLBACK")

    def install_source(self, source, approved=False, initialize=False, recovery=False):
        if approved is not True:
            raise model.AssociationError("WRITE_FAILED", "OPERATOR_APPROVAL_REQUIRED")
        model.validate_source(source)
        # Recovery retains its existing authority; --initialize combined with
        # recovery never grants missing-directory creation.
        bootstrap = self.initialize_directories() if initialize is True and not recovery else contextlib.nullcontext(None)
        with bootstrap as infrastructure_check, self.lock():
            if infrastructure_check:
                infrastructure_check()
            anchors = []
            if not recovery:
                current, anchor, unused = self.confirmed(SOURCE, allow_initial=initialize, resync=True)
                anchors.append(anchor)
            # Recovery is not permission to erase a separately available confirmed
            # source identity in a valid output. Pending/invalid visible output
            # is never promoted into an anchor.
            try:
                prior, output_anchor, unused = self.confirmed(OUTPUT, allow_initial=True)
                if prior is not None:
                    anchors.append(dict(sha256=prior["configured"]["source_sha256"],
                                        source_revision=prior["configured"]["revision"]))
            except model.AssociationError:
                # An unusable output remains blocked in its own domain.
                pass
            model.check_revision(source, anchors)
            if recovery:
                self.recovery_revision_floor(source, anchors)
            return self.publish(SOURCE, source, before_replace=infrastructure_check, recovery=recovery, initial=initialize)

    def read_handoff(self, evaluated_at):
        with self.lock():
            value, unused_anchor, output_snapshot = self.confirmed(OUTPUT)
            inventory, inventory_snapshot = self.input_inventory()
            source, source_snapshot, error = self.source_state()
            token = self.source_token()
            if value["configured"]["state"] == "VALID" and error:
                raise model.AssociationError(error)
            model.validate_handoff(value, inventory, source, evaluated_at)
            self.unchanged(inventory_snapshot, "INVENTORY_INVALID")
            self.unchanged(output_snapshot, "PRIOR_STATE_INVALID")
            if source_snapshot:
                self.unchanged(source_snapshot, "SOURCE_CHANGED")
            if token != self.source_token():
                raise model.AssociationError("SOURCE_CHANGED")
            current, unused_anchor, unused = self.confirmed(OUTPUT)
            if current != value:
                raise model.AssociationError("PRIOR_STATE_INVALID")
            return value

    def recertify(self, domain, evaluated_at, approved=False):
        with self.lock():
            def valid(value):
                if domain == OUTPUT:
                    inventory, unused = self.input_inventory()
                    source, unused, error = self.source_state()
                    if value["configured"]["state"] == "VALID" and error:
                        raise model.AssociationError(error)
                    model.validate_handoff(value, inventory, source, evaluated_at)
                else:
                    model.validate_source(value)
            return self.recover(domain, approved, valid)
