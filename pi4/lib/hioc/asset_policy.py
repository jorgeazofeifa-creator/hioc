"""Explicit schema 2.0 AssetService transactions; no migration on read/startup."""
from __future__ import annotations

import copy
import contextlib
import hashlib
import json
import os
import stat
import tempfile
import uuid
from datetime import timedelta

from . import assets as legacy
from .availability_contract import (
    POLICY_FIELDS, RECEIPT_KEYS, PolicyError, asset_id, digest, integer, keys,
    policy_fields, require, strict_json, time_text, timestamp, uuid4, validate_receipt,
)

STORE_KEYS = (*legacy.STORE_KEYS, 'store_epoch', 'store_revision', 'policy_requests')
RECORD_KEYS = (*legacy.RECORD_KEYS, *POLICY_FIELDS)
MAX_STORE_BYTES = 16777216


def validate_transaction_status(value):
    """Durability evidence only: never policy, a nonce store, or mutation authority."""
    from .availability_contract import hex_digest
    keys(value, ('schema_version', 'phase', 'store_sha256', 'status_sha256', 'store_epoch', 'store_revision'))
    require(value['schema_version'] == '1.0' and value['phase'] in ('PREPARED', 'CONFIRMED'))
    hex_digest(value['store_sha256'])
    if value['status_sha256'] is not None: hex_digest(value['status_sha256'])
    require(value['phase'] != 'CONFIRMED' or value['status_sha256'] is not None)
    if value['store_epoch'] is not None: uuid4(value['store_epoch'])
    if value['store_revision'] is not None: integer(value['store_revision'])
    require((value['store_epoch'] is None) == (value['store_revision'] is None))
    return value


def inventory_attachment(store, key):
    """Reuse accepted PE-4 inventory age/schema and PE-5 strong-owner checks.

    The 5400-second bound belongs to the existing inventory-input contract. It is
    not an availability/outage profile and supplies no positive availability sample.
    """
    from .home_assistant_association import validate_inventory
    from .service_association import _owners, _owner_reason
    try:
        raw = store.read_bytes(store.inventory_path, inventory=True)
        validate_inventory(raw, timestamp(store.timestamp()))
        value = strict_json(raw, limit=MAX_STORE_BYTES, depth=16)
    except Exception:
        return 'absent'
    try:
        # The historical validator accepts bounded clock skew; PE-7 creation does not.
        updated = value['updated']
        from datetime import datetime, timezone
        instant = datetime.fromisoformat(updated.replace('Z', '+00:00'))
        require(instant <= timestamp(store.timestamp()))
        by_id, by_mac = _owners(value['devices'])
        reason = _owner_reason(key, by_id, by_mac)
        if reason is None:
            return 'strong'
        if reason == 'MISSING_OWNER':
            return 'orphan'
        if reason in ('AMBIGUOUS_OWNER', 'OWNER_MAC_COLLISION', 'OWNER_ID_MISMATCH'):
            return 'conflicted'
        return 'weak'
    except Exception:
        return 'absent'


def validate_store(value):
    keys(value, STORE_KEYS)
    require(tuple(value) == STORE_KEYS and value['schema_version'] == '2.0')
    timestamp(value['updated_at'])
    uuid4(value['store_epoch'])
    integer(value['store_revision'])
    require(type(value['assets']) is dict)
    require(type(value['asset_count']) is int and value['asset_count'] == len(value['assets']))
    require(list(value['assets']) == sorted(value['assets']))
    for key, record in value['assets'].items():
        asset_id(key)
        keys(record, RECORD_KEYS)
        require(tuple(record) == RECORD_KEYS and record['stable_device_id'] == key)
        for field in legacy.OPERATOR_FIELDS:
            require(legacy.normalize_field(field, record[field]) == record[field])
        timestamp(record['created_at'])
        timestamp(record['updated_at'])
        require(timestamp(record['created_at']) <= timestamp(record['updated_at']))
        integer(record['revision'])
        require(record['update_source'] in ('operator_cli', 'operator_ha'))
        policy_fields({name: record[name] for name in POLICY_FIELDS})
    receipts = value['policy_requests']
    require(type(receipts) is list and len(receipts) <= 1024)
    seen = set()
    for receipt in receipts:
        validate_receipt(receipt)
        identity = tuple(receipt[k] for k in ('issuer_digest', 'actor_digest', 'operation_id'))
        require(identity not in seen and receipt['committed_store_revision'] <= value['store_revision'])
        seen.add(identity)
    return value


def validate_versioned(value):
    if type(value) is dict and value.get('schema_version') == '1.0':
        return legacy.validate_store(value)
    if type(value) is dict and value.get('schema_version') == '2.0':
        return validate_store(value)
    raise PolicyError('UNSUPPORTED_SCHEMA')


def validate_status(value):
    keys(value, legacy.STATUS_KEYS)
    require(value['schema_version'] == '2.0')
    # Validate identical status semantics using a separate value, never a source projection.
    original = dict(value)
    original['schema_version'] = '1.0'
    legacy.validate_status(original)
    return value


def serialize(value):
    validate_versioned(value)
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')


class PolicyStore(legacy.AssetStore):
    """Version-aware storage using the existing Asset path/lock/status/backup owner."""
    uncertain = False

    @property
    def transaction_status_path(self):
        return self.state_dir/'assets_transaction_status.json'

    def transaction_status(self, value):
        validate_transaction_status(value)
        raw = (json.dumps(value, indent=2, allow_nan=False)+'\n').encode('utf-8')
        self._replace_exact(self.transaction_status_path, raw, validate_transaction_status)

    def durability_pair_confirmed(self, store):
        """Read-only verification of causally ordered completed store/status fsyncs.

        The CONFIRMED witness is written only after both artifacts and their parent
        fsyncs succeed. Matching metadata/timestamps alone never establish this fact.
        A missing, PREPARED, corrupt or mismatched witness proves no completion.
        """
        try:
            marker = validate_transaction_status(strict_json(self.read_bytes(self.transaction_status_path), depth=3))
            status_raw = self.read_bytes(self.status_path)
            status = strict_json(status_raw, depth=3)
            (validate_status if store['schema_version'] == '2.0' else legacy.validate_status)(status)
            store_raw = self.read_bytes(self.store_path)
            require(validate_versioned(strict_json(store_raw, limit=MAX_STORE_BYTES, depth=8)) == store)
            return (marker['phase'] == 'CONFIRMED' and marker['store_sha256'] == hashlib.sha256(store_raw).hexdigest()
                    and marker['status_sha256'] == hashlib.sha256(status_raw).hexdigest()
                    and marker['store_epoch'] == store.get('store_epoch')
                    and marker['store_revision'] == store.get('store_revision'))
        except Exception:
            return False

    def _safe_parents(self, path):
        require(path.is_absolute() and self.home.is_absolute(), 'STORE_UNAVAILABLE')
        require(all(not parent.is_symlink() for parent in (path.parent, *path.parents)), 'STORE_UNAVAILABLE')
        if os.name == 'posix':
            current = path.parent
            while current == self.home or self.home in current.parents:
                info = current.lstat()
                require(stat.S_ISDIR(info.st_mode) and info.st_uid == os.getuid() and
                        not stat.S_IMODE(info.st_mode) & 0o022, 'STORE_UNAVAILABLE')
                if current == self.home:
                    break
                current = current.parent

    def ensure_directories(self):
        require(self.home.is_dir() and not self.home.is_symlink(), 'STORE_UNAVAILABLE')
        for directory, mode in ((self.home/'state', 0o750), (self.state_dir, 0o750),
                                (self.home/'backups', 0o700), (self.backup_dir, 0o700)):
            self._safe_parents(directory)
            if not directory.exists():
                directory.mkdir(mode=mode)
            self._safe_parents(directory/'child')
        if os.name == 'posix':
            require(stat.S_IMODE(self.backup_dir.lstat().st_mode) == 0o700, 'STORE_UNAVAILABLE')
    def read_bytes(self, path, *, inventory=False):
        """Descriptor-safe bounded read; do not follow symlinks or hard-link aliases."""
        self._safe_parents(path)
        require(not inventory or path == self.inventory_path, 'STORE_UNAVAILABLE')
        before = path.lstat()
        require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, 'STORE_UNAVAILABLE')
        if os.name == 'posix':
            require(before.st_uid == os.getuid() and stat.S_IMODE(before.st_mode) in
                    ((0o600, 0o644) if inventory else (0o600,)),
                    'STORE_UNAVAILABLE')
        fd = os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0))
        with os.fdopen(fd, 'rb') as stream:
            opened = os.fstat(stream.fileno())
            require((opened.st_dev, opened.st_ino) == (before.st_dev, before.st_ino), 'STORE_UNAVAILABLE')
            raw = stream.read(MAX_STORE_BYTES + 1)
            after = os.fstat(stream.fileno())
        final = path.lstat()
        # Windows path stat and descriptor stat expose different ctime meanings in
        # the bundled interpreter. Compare each clock with its own observation API.
        fingerprint = lambda info: (info.st_dev, info.st_ino, info.st_mode, info.st_nlink,
                                    info.st_uid, info.st_gid, info.st_size, info.st_mtime_ns)
        require(len(raw) <= MAX_STORE_BYTES and fingerprint(before) == fingerprint(after) == fingerprint(final)
                and before.st_ctime_ns == final.st_ctime_ns and opened.st_ctime_ns == after.st_ctime_ns,
                'STORE_UNAVAILABLE')
        return raw

    def load_store(self, missing_ok=False):
        try:
            raw = self.read_bytes(self.store_path)
        except FileNotFoundError:
            if missing_ok:
                return None
            raise PolicyError('STORE_UNAVAILABLE') from None
        return validate_versioned(strict_json(raw, limit=MAX_STORE_BYTES, depth=8))

    def load_status(self):
        value = strict_json(self.read_bytes(self.status_path), limit=MAX_STORE_BYTES, depth=3)
        return validate_status(value) if value.get('schema_version') == '2.0' else legacy.validate_status(value)

    def inventory_context(self, store):
        try:
            inv = strict_json(self.inventory_path.read_bytes(), limit=MAX_STORE_BYTES, depth=16)
            require(type(inv.get('devices')) is list)
            current = {asset_id(row['id']) for row in inv['devices']}
            return 'available', set(store['assets']) - current
        except Exception:
            return 'unavailable', None

    def make_status(self, store, context, orphans, **kwargs):
        value = super().make_status(store, context, orphans, **kwargs)
        value['schema_version'] = store['schema_version'] if store is not None else '1.0'
        return value

    def write_store(self, store):
        self._replace_exact(self.store_path, serialize(store), validate_versioned)

    def write_status(self, value):
        validator = validate_status if value['schema_version'] == '2.0' else legacy.validate_status
        validator(value)
        raw = (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
        self._replace_exact(self.status_path, raw, validator)

    def _replace_exact(self, path, raw, validator):
        """Track replace explicitly so a failed durability step cannot claim NOT_APPLIED."""
        validator(strict_json(raw, limit=MAX_STORE_BYTES, depth=8))
        self.ensure_directories()
        temporary = None
        replaced = False
        try:
            fd, name = tempfile.mkstemp(prefix='.assets-', dir=path.parent)
            temporary = path.parent / name
            with os.fdopen(fd, 'wb') as stream:
                stream.write(raw)
                stream.flush()
                os.fsync(stream.fileno())
            os.chmod(temporary, 0o600)
            require(self.read_bytes(temporary) == raw, 'STORE_UNAVAILABLE')
            os.replace(temporary, path)
            temporary = None
            replaced = True
            self._fsync_directory(path.parent)
        except Exception:
            if replaced:
                self.uncertain = True
            raise PolicyError('COMMIT_UNKNOWN' if replaced else 'STORE_UNAVAILABLE',
                              uncertain=replaced) from None
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)

    def create_backup(self, store, exact_bytes=None):
        raw = exact_bytes if exact_bytes is not None else serialize(store)
        require(validate_versioned(strict_json(raw, limit=MAX_STORE_BYTES, depth=8)) == store)
        self.ensure_directories()
        sha = hashlib.sha256(raw).hexdigest()
        stamp = self.timestamp().replace('-', '').replace(':', '').replace('.', '')
        name = f'assets-{stamp}-{sha[:12]}.json'
        path = self.backup_dir / name
        if path.exists():
            require(self.read_bytes(path) == raw, 'STORE_UNAVAILABLE')
        else:
            self._replace_exact(path, raw, validate_versioned)
        require(hashlib.sha256(self.read_bytes(path)).hexdigest() == sha, 'STORE_UNAVAILABLE')
        return name

    def load_backup(self, basename):
        require(type(basename) is str and legacy.BACKUP_RE.fullmatch(basename) is not None)
        path = self.backup_dir / basename
        raw = self.read_bytes(path)
        require(hashlib.sha256(raw).hexdigest()[:12] == legacy.BACKUP_RE.fullmatch(basename).group(2))
        return validate_versioned(strict_json(raw, limit=MAX_STORE_BYTES, depth=8)), raw


class PolicyService(legacy.AssetService):
    """AssetService successor. Callers never write the store or select arbitrary paths."""
    def __init__(self, store, attachment=None):
        require(isinstance(store, PolicyStore))
        super().__init__(store)
        # Attachment resolver is local validated inventory authority, never a request field.
        self.attachment = attachment or (lambda key: inventory_attachment(store, key))

    def authorize_population(self, operation, key, scope, *, locked=False):
        """Explicit owner-accepted operation scope, never arbitrary-ID authority.

        The protocol calls locked=True only from its writer-guard reauthorization.
        Create conflict/replay checks remain in mutate_policy, under that guard.
        """
        from .availability_protocol import POPULATION_SCOPES
        asset_id(key)
        require(operation in POPULATION_SCOPES and scope == POPULATION_SCOPES[operation], 'FORBIDDEN')
        context = contextlib.nullcontext() if locked else legacy.AssetLock(self.store.lock_path, shared=True)
        with context:
            require(not self.store.uncertain, 'COMMIT_UNKNOWN')
            current = self.store.load_store()
            require(current['schema_version'] == '2.0', 'UNSUPPORTED_SCHEMA')
            require(self.store.durability_pair_confirmed(current), 'COMMIT_UNKNOWN')
            exists = key in current['assets']
            if operation == 'create':
                # Existing records can reach exact durable receipt reconciliation;
                # a fresh create can never overwrite them in mutate_policy.
                return self.attachment(key) == 'strong'
            if operation == 'get':
                return exists or self.attachment(key) == 'strong'
            return exists

    def _write_status(self, store):
        marker = None
        try:
            candidate = validate_transaction_status(strict_json(self.store.read_bytes(self.store.transaction_status_path), depth=3))
            if candidate['phase'] == 'CONFIRMED' and candidate['store_sha256'] == hashlib.sha256(self.store.read_bytes(self.store.store_path)).hexdigest():
                marker = candidate
        except Exception:
            pass
        status = super()._write_status(store)
        if marker is not None:
            marker['status_sha256'] = hashlib.sha256(self.store.read_bytes(self.store.status_path)).hexdigest()
            self.store.transaction_status(marker)
        return status

    def _commit(self, prior, updated):
        if self.store.uncertain:
            raise PolicyError('COMMIT_UNKNOWN', uncertain=True)
        if prior['schema_version'] == '2.0' and not self.store.durability_pair_confirmed(prior):
            raise PolicyError('COMMIT_UNKNOWN', uncertain=True)
        validate_versioned(updated)
        self.store.create_backup(prior, self.store.read_bytes(self.store.store_path))
        marker = dict(schema_version='1.0', phase='PREPARED', store_sha256=hashlib.sha256(serialize(updated)).hexdigest(),
                      status_sha256=None, store_epoch=updated.get('store_epoch'), store_revision=updated.get('store_revision'))
        self.store.transaction_status(marker)
        self.store.write_store(updated)
        try:
            self._write_status(updated)
            marker.update(phase='CONFIRMED', status_sha256=hashlib.sha256(self.store.read_bytes(self.store.status_path)).hexdigest())
            self.store.transaction_status(marker)
        except Exception:
            self.store.uncertain = True
            raise PolicyError('COMMIT_UNKNOWN', uncertain=True) from None

    def set_fields(self, device_id, fields, allow_orphan=False, expected_revision=None):
        asset_id(device_id)
        require(type(fields) is dict and bool(fields))
        normalized = {name: legacy.normalize_field(name, value) for name, value in fields.items()}
        with legacy.AssetLock(self.store.lock_path, shared=False):
            current = self.store.load_store()
            require(current['schema_version'] == '2.0', 'UNSUPPORTED_SCHEMA')
            record = current['assets'].get(device_id)
            if record is None:
                require(expected_revision is None, 'REVISION_CONFLICT')
                require(self.attachment(device_id) == 'strong' or allow_orphan is True, 'IDENTITY_UNSAFE')
                require(any(value is not None for value in normalized.values()))
                now = self.store.timestamp()
                record = dict(stable_device_id=device_id, **{k: None for k in legacy.OPERATOR_FIELDS},
                              created_at=now, updated_at=now, update_source='operator_cli', revision=1,
                              **{k: None for k in POLICY_FIELDS})
                result = 'created'
            else:
                require(type(expected_revision) is int and record['revision'] == expected_revision, 'REVISION_CONFLICT')
                if all(record[k] == v for k, v in normalized.items()):
                    return self._result('set', 'no_change', self.store.load_status()['status'], dict(revision=record['revision'], changed_fields=[], backup=None))
                record = dict(record)
                record.update(updated_at=self.store.timestamp(), update_source='operator_cli', revision=record['revision']+1)
                result = 'updated'
            record.update(normalized)
            updated = copy.deepcopy(current)
            updated['assets'][device_id] = record
            updated['assets'] = dict(sorted(updated['assets'].items()))
            updated.update(asset_count=len(updated['assets']), updated_at=record['updated_at'],
                           store_revision=current['store_revision']+1)
            self._commit(current, updated)
            return self._result('set', result, self.store.load_status()['status'], dict(device_id_digest=legacy.redacted_id(device_id),
                revision=record['revision'], changed_fields=list(normalized)))

    def set_policy_local(self, key, fields, epoch, store_revision, expected_revision=None):
        """Local operator_cli provenance; no federation assertion or remote capability."""
        asset_id(key); policy_fields(fields); uuid4(epoch); integer(store_revision)
        with legacy.AssetLock(self.store.lock_path, shared=False):
            current = self.store.load_store()
            require(current['schema_version'] == '2.0', 'UNSUPPORTED_SCHEMA')
            require(current['store_epoch'] == epoch and current['store_revision'] == store_revision, 'REVISION_CONFLICT')
            record = current['assets'].get(key)
            require(expected_revision is None if record is None else type(expected_revision) is int and record['revision'] == expected_revision, 'REVISION_CONFLICT')
            if record is None or fields.get('expected_availability') is True:
                require(self.attachment(key) == 'strong', 'IDENTITY_UNSAFE')
            if record is not None and all(record[k] == v for k,v in fields.items()):
                return self._result('set-policy', 'no_change', self.store.load_status()['status'], dict(revision=record['revision']))
            now = self.store.timestamp()
            if record is None:
                require(any(value is not None for value in fields.values()))
                record = dict(stable_device_id=key, **{name:None for name in legacy.OPERATOR_FIELDS},
                    created_at=now, updated_at=now, update_source='operator_cli', revision=1,
                    **{name:None for name in POLICY_FIELDS})
                outcome = 'created'
            else:
                record = dict(record)
                record.update(updated_at=now, update_source='operator_cli', revision=record['revision']+1)
                outcome = 'updated'
            record.update(fields)
            updated = copy.deepcopy(current); updated['assets'][key] = record
            updated['assets'] = dict(sorted(updated['assets'].items()))
            updated.update(updated_at=now, asset_count=len(updated['assets']), store_revision=current['store_revision']+1)
            self._commit(current, updated)
            return self._result('set-policy', outcome, self.store.load_status()['status'], dict(revision=record['revision']))

    def clear_field(self, device_id, field, expected_revision):
        # No implicit schema 2.0 deletion, even when the last description is cleared.
        return self.set_fields(device_id, {field: None}, expected_revision=expected_revision)

    def _remove_locked(self, current, device_id, record, command, changed):
        updated = copy.deepcopy(current)
        del updated['assets'][device_id]
        updated.update(asset_count=len(updated['assets']), updated_at=self.store.timestamp(),
                       store_revision=current['store_revision']+1)
        self._commit(current, updated)
        return self._result(command, 'removed', 'online', dict(device_id_digest=legacy.redacted_id(device_id), revision=None))

    def restore(self, basename):
        # Inherited legacy restore lacks stopped-writer/retained-edit disposition.
        raise PolicyError('FORBIDDEN')

    def migrate(self, expected_sha256, *, writers_stopped=False):
        require(writers_stopped is True, 'FORBIDDEN')
        with legacy.AssetLock(self.store.lock_path, shared=False):
            prior = self.store.load_store()
            require(prior['schema_version'] == '1.0', 'UNSUPPORTED_SCHEMA')
            raw = self.store.read_bytes(self.store.store_path)
            require(hashlib.sha256(raw).hexdigest() == expected_sha256, 'REVISION_CONFLICT')
            migrated = copy.deepcopy(prior)
            migrated['schema_version'] = '2.0'
            for record in migrated['assets'].values():
                record.update({name: None for name in POLICY_FIELDS})
            migrated.update(store_epoch=uuid.uuid4().hex, store_revision=1, policy_requests=[])
            self._commit(prior, migrated)
            return migrated

    def restore_exact(self, basename, *, writers_stopped=False, retain_later_edits=False):
        require(writers_stopped is True and retain_later_edits is True, 'FORBIDDEN')
        with legacy.AssetLock(self.store.lock_path, shared=False):
            current = self.store.load_store()
            candidate, raw = self.store.load_backup(basename)
            preserved = self.store.create_backup(current, self.store.read_bytes(self.store.store_path))
            if candidate['schema_version'] == '2.0':
                candidate = copy.deepcopy(candidate)
                candidate['store_epoch'] = uuid.uuid4().hex
                candidate['policy_requests'] = []
                raw = serialize(candidate)
            marker = dict(schema_version='1.0', phase='PREPARED', store_sha256=hashlib.sha256(raw).hexdigest(),
                          status_sha256=None, store_epoch=candidate.get('store_epoch'), store_revision=candidate.get('store_revision'))
            self.store.transaction_status(marker)
            self.store._replace_exact(self.store.store_path, raw, validate_versioned)
            try:
                self._write_status(candidate)
                marker.update(phase='CONFIRMED', status_sha256=hashlib.sha256(self.store.read_bytes(self.store.status_path)).hexdigest())
                self.store.transaction_status(marker)
            except Exception:
                self.store.uncertain = True
                raise PolicyError('COMMIT_UNKNOWN', uncertain=True) from None
            return {'preserved_private_backup': preserved, 'schema_version': candidate['schema_version']}

    def _policy(self, store, key):
        require(store['schema_version'] == '2.0', 'UNSUPPORTED_SCHEMA')
        record = store['assets'].get(key)
        attachment = self.attachment(key)
        require(attachment in ('strong', 'orphan', 'weak', 'conflicted', 'absent'))
        fields = {name: record[name] if record else None for name in POLICY_FIELDS}
        applied = None
        snapshot_reader = getattr(self, 'evaluation_snapshot_reader', None)
        if snapshot_reader is not None:
            try:
                snapshot = snapshot_reader(key)
                if snapshot is not None and snapshot['store_epoch'] == store['store_epoch']:
                    applied = snapshot['policy_revision']
            except Exception:
                pass  # Unavailable evidence cannot establish application.
        return dict(asset_id=key, attachment=attachment, store_epoch=store['store_epoch'],
                    store_revision=store['store_revision'], revision=record['revision'] if record else None,
                    **fields, effective_expected_availability=fields['expected_availability'] is True,
                    effective_infrastructure_type=fields['infrastructure_type'] if fields['infrastructure_device'] is True else None,
                    applied_policy_revision=applied)

    def get_policy(self, key):
        asset_id(key)
        with legacy.AssetLock(self.store.lock_path, shared=True):
            if self.store.uncertain:
                raise PolicyError('COMMIT_UNKNOWN', uncertain=True)
            current = self.store.load_store()
            if current['schema_version'] == '2.0' and not self.store.durability_pair_confirmed(current):
                raise PolicyError('COMMIT_UNKNOWN', uncertain=True)
            return dict(schema_version='1.0', operation_id=None, result='read', commit_state='CONFIRMED',
                        policy=self._policy(current, key), receipt=None)

    @staticmethod
    def _receipt(store, issuer, actor, operation):
        matches = [item for item in store['policy_requests']
                   if (item['issuer_digest'], item['actor_digest'], item['operation_id']) ==
                   (digest(issuer), digest(actor), operation)]
        require(len(matches) <= 1, 'STORE_UNAVAILABLE')
        return matches[0] if matches else None

    def operation_result(self, key, operation, issuer, actor):
        asset_id(key)
        uuid4(operation)
        with legacy.AssetLock(self.store.lock_path, shared=True):
            store = self.store.load_store()
            require(store['schema_version'] == '2.0', 'UNSUPPORTED_SCHEMA')
            receipt = self._receipt(store, issuer, actor, operation)
            require(receipt is None or receipt['asset_id'] == key, 'FORBIDDEN')
            # Receipt alone cannot prove physical durability. Exact paired status is required.
            confirmed = False
            try:
                status = self.store.load_status()
                confirmed = (self.store.durability_pair_confirmed(store) and status['schema_version'] == '2.0' and
                             status['asset_count'] == store['asset_count'] and
                             status['updated'] >= store['updated_at'] and
                             status['status'] in ('online', 'degraded'))
            except Exception:
                pass
            if confirmed:
                self.store.uncertain = False  # Explicit read-only reconciliation, no file repair.
            return dict(schema_version='1.0', operation_id=operation,
                        result='found' if receipt else 'not_found', receipt=receipt,
                        policy=self._policy(store, key), commit_state='CONFIRMED' if confirmed else 'UNKNOWN')

    def mutate_policy(self, operation, payload, issuer, actor, reauthorize):
        require(operation in ('create', 'update'))
        keys(payload, ('asset_id', 'store_epoch', 'expected_store_revision', 'expected_revision', 'operation_id', 'fields'))
        key = asset_id(payload['asset_id'])
        uuid4(payload['store_epoch'])
        uuid4(payload['operation_id'])
        integer(payload['expected_store_revision'])
        policy_fields(payload['fields'])
        if operation == 'create':
            require(payload['expected_revision'] is None)
        else:
            integer(payload['expected_revision'])
        with legacy.AssetLock(self.store.lock_path, shared=False):
            if self.store.uncertain:
                raise PolicyError('COMMIT_UNKNOWN', uncertain=True)
            require(reauthorize() is True, 'FORBIDDEN')
            current = self.store.load_store()
            require(current['schema_version'] == '2.0', 'UNSUPPORTED_SCHEMA')
            now = timestamp(self.store.timestamp())
            receipt = self._receipt(current, issuer, actor, payload['operation_id'])
            if receipt is not None:
                require(receipt['request_sha256'] == digest(payload), 'REPLAY_CONFLICT')
                require(timestamp(receipt['expires_at']) > now, 'REVISION_CONFLICT')
                if not self.store.durability_pair_confirmed(current):
                    raise PolicyError('COMMIT_UNKNOWN', uncertain=True)
                return dict(schema_version='1.0', operation_id=payload['operation_id'], result='replayed',
                            commit_state='CONFIRMED', policy=self._policy(current, key), receipt=receipt)
            require(current['store_epoch'] == payload['store_epoch'] and
                    current['store_revision'] == payload['expected_store_revision'], 'REVISION_CONFLICT')
            record = current['assets'].get(key)
            require((record is None if operation == 'create' else record is not None and
                     record['revision'] == payload['expected_revision']), 'REVISION_CONFLICT')
            if record is None or payload['fields'].get('expected_availability') is True:
                require(self.attachment(key) == 'strong', 'IDENTITY_UNSAFE')
            retained = [row for row in current['policy_requests'] if timestamp(row['expires_at']) > now]
            require(len(retained) < 1024, 'BUSY')
            updated = copy.deepcopy(current)
            changed = record is None or any(record[name] != val for name, val in payload['fields'].items())
            if record is None:
                require(any(value is not None for value in payload['fields'].values()))
                record = dict(stable_device_id=key, **{name: None for name in legacy.OPERATOR_FIELDS},
                              created_at=time_text(now), updated_at=time_text(now), update_source='operator_ha', revision=1,
                              **{name: None for name in POLICY_FIELDS})
            else:
                record = dict(record)
                if changed:
                    record.update(updated_at=time_text(now), update_source='operator_ha', revision=record['revision'] + 1)
            record.update(payload['fields'])
            updated['assets'][key] = record
            updated['assets'] = dict(sorted(updated['assets'].items()))
            updated.update(asset_count=len(updated['assets']), updated_at=time_text(now),
                           store_revision=current['store_revision'] + 1)
            receipt = dict(issuer_digest=digest(issuer), actor_digest=digest(actor), operation_id=payload['operation_id'],
                           request_sha256=digest(payload), expires_at=time_text(now + timedelta(seconds=120)), asset_id=key,
                           committed_revision=record['revision'], committed_store_revision=updated['store_revision'],
                           outcome='changed' if changed else 'no_change')
            updated['policy_requests'] = retained + [receipt]
            self._commit(current, updated)
            return dict(schema_version='1.0', operation_id=payload['operation_id'],
                        result='created' if operation == 'create' else 'updated' if changed else 'no_change',
                        commit_state='CONFIRMED', policy=self._policy(updated, key), receipt=receipt)
