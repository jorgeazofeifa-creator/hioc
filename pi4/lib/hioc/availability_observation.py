"""Bounded read-only HA normalization; no registry expansion, state firehose or probes."""
from __future__ import annotations
from datetime import timedelta
import json
import os
from pathlib import Path
import stat
import tempfile
from .availability import validate_observation, validate_profile
from .availability_contract import (
    PolicyError, asset_id, digest, identifier, integer, keys, require, time_text, timestamp, uuid4,
)

MAPPING_KEYS = ('source_id', 'asset_id', 'ha_device_id', 'entity_id', 'mapping_revision',
                'scope', 'report_semantics_verified')


def collect(states_get, mappings, profile, association, association_schema, attachment,
            epoch, now, *, association_deadline):
    """Normalize only reviewed explicit members. No attributes or entity names escape.

    association_deadline is an explicitly approved upstream association-snapshot
    boundary, never an invented default or an observation of current production.
    states_get must be the installed HA's hass.states.get, not get-all-states.
    """
    from .home_assistant_association import validate_state as validate_association
    validate_profile(profile)
    validate_association(association, association_schema)
    uuid4(epoch)
    instant = timestamp(now)
    require(instant < timestamp(association_deadline), 'IDENTITY_UNSAFE')
    require(type(mappings) is list and len(mappings) <= 256)
    observations, seen = [], set()
    for mapping in mappings:
        keys(mapping, MAPPING_KEYS)
        source, key = identifier(mapping['source_id']), asset_id(mapping['asset_id'])
        require((source, key) not in seen)
        seen.add((source, key))
        require(source in profile['enabled_sources'])
        definition = profile['source_definitions'][source]
        require(definition['kind'] == 'ha' and definition['mapping_revision'] == integer(mapping['mapping_revision']))
        require(definition['mapping_sha256'] == digest(mapping))
        require(mapping['scope'] in ('DEVICE', 'ENTITY') and type(mapping['report_semantics_verified']) is bool)
        require(type(mapping['entity_id']) is str and 1 <= len(mapping['entity_id']) <= 255)
        matches = [row for row in association['associations'] if row['hioc_device_id'] == key]
        valid = (len(matches) == 1 and attachment(key) == 'strong' and
                 matches[0]['status'] == 'ASSOCIATED_STRONG_MAC' and matches[0]['association_basis'] == 'unique_mac' and
                 matches[0]['ha_device_id'] == mapping['ha_device_id'] and
                 mapping['entity_id'] in {member['entity_id'] for member in matches[0].get('entities', [])})
        state, status, kind, reason = None, 'SUCCESS', 'UNKNOWN', 'UNSUPPORTED_REPORT_SEMANTICS'
        observed = instant
        source_sha = digest(['missing', epoch, source, key])
        if valid:
            try:
                state = states_get(mapping['entity_id'])
            except Exception:
                status, reason = 'FAILED', 'COLLECTION_FAILED'
        else:
            status, reason = 'UNAVAILABLE', 'ASSOCIATION_UNSAFE'
        if state is not None and mapping['report_semantics_verified'] is True:
            try:
                # last_changed and collection time are deliberately not fallbacks.
                observed = state.last_reported
                require(observed.tzinfo is not None and observed <= instant)
                meaning = state.state
                require(type(meaning) is str and len(meaning) <= 128)
                source_sha = digest([epoch, source, key, mapping['mapping_revision'], time_text(observed), meaning])
                if meaning not in ('unknown', 'unavailable'):
                    if meaning in definition['positive_meanings']:
                        kind, reason = 'POSITIVE', 'REVIEWED_POSITIVE'
                    elif meaning in definition['negative_meanings'] and definition['physical_device_authority'] is True and mapping['scope'] == 'DEVICE':
                        kind, reason = 'NEGATIVE', 'REVIEWED_PHYSICAL_NEGATIVE'
                    else:
                        reason = 'ENTITY_STATE_NOT_PHYSICAL_OUTAGE'
                else:
                    reason = 'HA_STATE_UNKNOWN'
            except Exception:
                observed, status, kind, reason = instant, 'UNAVAILABLE', 'UNKNOWN', 'REPORT_TIME_UNAVAILABLE'
        elif state is None and status == 'SUCCESS':
            reason = 'ENTITY_MISSING'
        deadline = min(timestamp(association_deadline), observed + timedelta(seconds=definition['max_age_seconds']))
        # Invalid/unknown observations still explicitly describe collection quality;
        # they can never count as positive/negative evidence in the evaluator.
        row = dict(schema_version='1.0', source_id=source, source_kind='ha', asset_id=key, device_id=key,
                   source_epoch=epoch, sample_id=digest([epoch, source, time_text(observed), source_sha]),
                   observed_at=time_text(observed), collected_at=now, collection_status=status, completeness='COMPLETE',
                   evidence_kind=kind, scope=mapping['scope'],
                   authority_ref=digest([source, definition['mapping_revision'], definition['mapping_sha256']]),
                   valid_until=time_text(deadline), reason_code=reason, source_sha256=source_sha)
        observations.append(validate_observation(row))
    return observations


class ObservationStore:
    """One private normalized snapshot, never Asset policy or incident lifecycle."""
    def __init__(self, home, lock_path):
        self.path = Path(home)/'state/incidents/pe7/observations.json'
        self.lock_path = Path(lock_path)
        from .asset_policy import PolicyStore
        self.reader = PolicyStore(Path(home))

    def commit(self, observations):
        from .assets import AssetLock
        from .availability_contract import strict_json
        with AssetLock(self.lock_path, shared=False):
            require(self.path.parent.is_dir() and all(not p.is_symlink() for p in self.path.parents), 'STORE_UNAVAILABLE')
            if os.name == 'posix':
                parent = self.path.parent.lstat()
                require(parent.st_uid == os.getuid() and stat.S_IMODE(parent.st_mode) == 0o700, 'STORE_UNAVAILABLE')
            current = {}
            if self.path.exists():
                info = self.path.lstat()
                require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, 'STORE_UNAVAILABLE')
                if os.name == 'posix':
                    require(info.st_uid == os.getuid() and stat.S_IMODE(info.st_mode) == 0o600, 'STORE_UNAVAILABLE')
                old = strict_json(self.reader.read_bytes(self.path), limit=262144, depth=6)
                keys(old, ('schema_version', 'observations')); require(old['schema_version'] == '1.0')
                for row in old['observations']:
                    validate_observation(row)
                    current[(row['asset_id'], row['source_id'])] = row
            for row in observations:
                validate_observation(row)
                current[(row['asset_id'], row['source_id'])] = row
            require(len(current) <= 256, 'BUSY')
            value = dict(schema_version='1.0', observations=[current[key] for key in sorted(current)])
            raw = (json.dumps(value, sort_keys=True, indent=2, allow_nan=False)+'\n').encode('utf-8')
            require(len(raw) <= 262144, 'BUSY')
            temporary, replaced = None, False
            try:
                fd, name = tempfile.mkstemp(prefix='.observation-', dir=self.path.parent); temporary = Path(name)
                with os.fdopen(fd, 'wb') as stream:
                    stream.write(raw); stream.flush(); os.fsync(stream.fileno())
                os.chmod(temporary, 0o600)
                require(temporary.read_bytes() == raw, 'STORE_UNAVAILABLE')
                os.replace(temporary, self.path); temporary, replaced = None, True
                if os.name == 'posix':
                    fd = os.open(self.path.parent, os.O_RDONLY | os.O_DIRECTORY)
                    try: os.fsync(fd)
                    finally: os.close(fd)
            except Exception:
                raise PolicyError('COMMIT_UNKNOWN' if replaced else 'STORE_UNAVAILABLE', uncertain=replaced) from None
            finally:
                if temporary is not None: temporary.unlink(missing_ok=True)
