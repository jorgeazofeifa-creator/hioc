"""PE-7 case/outbox transactions owned exclusively by incident-engine-v2.

This module has no scheduler, MQTT client, recipient, or production configuration.
All external transport is a single explicitly supplied deadline-aware operation.
"""
from __future__ import annotations
import copy
import json
import os
import tempfile
import uuid
from contextlib import contextmanager
from datetime import timedelta
from pathlib import Path
from .assets import AssetLock
from .availability import validate_machine, evaluation_snapshot, validate_status
from .availability_contract import (
    PolicyError, asset_id, canonical, digest, integer, keys, require, strict_json,
    timestamp, time_text, uuid4,
)

OUTBOX_STATES = {'PROPOSED', 'PENDING_AUTHORIZATION', 'AUTHORIZED', 'IN_FLIGHT',
                 'TRANSPORT_ACCEPTED', 'DELIVERED', 'FAILED_NOT_SUBMITTED',
                 'DELIVERY_UNKNOWN', 'CANCELLED', 'EXPIRED'}


def empty_state():
    return dict(schema_version='1.0', cases={}, outbox={}, process_epoch=uuid.uuid4().hex, legacy_active=None, evaluations={})


def validate_state(value):
    keys(value, ('schema_version', 'cases', 'outbox', 'process_epoch', 'legacy_active', 'evaluations'))
    require(type(value['evaluations']) is dict and len(value['evaluations']) <= 4096, 'BUSY')
    for key, snapshot in value['evaluations'].items():
        asset_id(key)
        keys(snapshot, ('store_epoch', 'policy_revision', 'machine', 'evaluation', 'observations'))
        uuid4(snapshot['store_epoch']); integer(snapshot['policy_revision'])
        machine = validate_machine(snapshot['machine'])
        require(machine['applied_policy_revision'] == snapshot['policy_revision'])
        require(all(machine[name] == snapshot['evaluation'][name] for name in ('availability_state','evaluated_at','valid_until')))
        validate_status(dict(schema_version='1.0', result='READ', asset_id=key,
            read_at=machine['evaluated_at'], status_reason='SNAPSHOT_READ', expected_availability=None,
            policy_status='PRESENT', current_policy_revision=snapshot['policy_revision'],
            applied_policy_revision=snapshot['policy_revision'], policy_binding='CURRENT',
            evaluation=snapshot['evaluation'], observations=snapshot['observations']))
    require(value['legacy_active'] is None or type(value['legacy_active']) is dict)
    require(value['schema_version'] == '1.0' and type(value['cases']) is dict and type(value['outbox']) is dict)
    uuid4(value['process_epoch'])
    require(len(value['cases']) <= 4096 and len(value['outbox']) <= 8192, 'BUSY')
    for case_key, case in value['cases'].items():
        keys(case, ('asset_id', 'episode', 'incident_id', 'lifecycle', 'suppression_reason',
                    'availability_state', 'severity', 'policy_revision', 'profile_revision',
                    'detected_at', 'updated_at', 'resolved_at', 'machine', 'events'))
        require(case_key == digest(['pe7_expected_availability', asset_id(case['asset_id'])]))
        integer(case['episode'])
        require(case['incident_id'] == digest([case_key, case['episode']]))
        require(case['lifecycle'] in ('detected', 'confirmed', 'active', 'recovering', 'resolved'))
        require(case['severity'] == 'warning' and case['suppression_reason'] in (None, 'OPERATOR_DISABLED'))
        validate_machine(case['machine'])
        require(type(case['events']) is list)
        timestamp(case['detected_at'])
        timestamp(case['updated_at'])
        if case['resolved_at'] is not None:
            timestamp(case['resolved_at'])
    for event_id, event in value['outbox'].items():
        keys(event, ('event', 'asset_id', 'store_epoch', 'policy_revision', 'evidence_sha256',
                     'evidence_valid_until', 'state', 'grant', 'off_revision', 'off_at'))
        require(event_id == event['event']['event_id'] and event['state'] in OUTBOX_STATES)
        asset_id(event['asset_id'])
        uuid4(event['store_epoch'])
        integer(event['policy_revision'])
        timestamp(event['evidence_valid_until'])
        grant = event['grant']
        if grant is not None:
            keys(grant, ('grant_id', 'event_id', 'store_epoch', 'asset_revision', 'evidence_sha256',
                         'authorized_at', 'not_after', 'process_epoch', 'state', 'claimed_at',
                         'transport_started_at', 'completed_at', 'outcome'))
            require(grant['event_id'] == event_id and grant['state'] == event['state'])
            uuid4(grant['grant_id'])
            uuid4(grant['process_epoch'])
            require(timestamp(grant['authorized_at']) < timestamp(grant['not_after']))
            require((timestamp(grant['not_after'])-timestamp(grant['authorized_at'])).total_seconds() <= 5)
    return value


class EngineState:
    def __init__(self, path, incident_lock):
        self.path, self.incident_lock = Path(path), Path(incident_lock)
        self.held = False
        self.uncertain = False

    @contextmanager
    def transaction(self):
        require(not self.held, 'BUSY')
        with AssetLock(self.incident_lock, shared=False):
            self.held = True
            try:
                yield self
            finally:
                self.held = False

    def read(self):
        require(self.held, 'FORBIDDEN')
        if self.uncertain:
            raise PolicyError('COMMIT_UNKNOWN', uncertain=True)
        # No corrupt/missing state silently becomes an empty dictionary.
        require(self.path.is_file() and not self.path.is_symlink(), 'STORE_UNAVAILABLE')
        from .asset_policy import PolicyStore
        return validate_state(strict_json(PolicyStore(self.path.parent).read_bytes(self.path), limit=16777216, depth=24))

    def initialize_explicitly(self):
        require(self.held and not self.path.exists(), 'FORBIDDEN')
        self.write(empty_state())

    def write(self, value):
        require(self.held, 'FORBIDDEN')
        validate_state(value)
        require(self.path.parent.is_dir() and not self.path.parent.is_symlink(), 'STORE_UNAVAILABLE')
        from .asset_policy import PolicyStore
        secure = PolicyStore(self.path.parent)
        secure._safe_parents(self.path)
        if self.path.exists():
            secure.read_bytes(self.path)
        raw = (json.dumps(value, ensure_ascii=True, indent=2, allow_nan=False)+'\n').encode('ascii')
        require(len(raw) <= 16777216, 'BUSY')
        temporary, replaced = None, False
        try:
            fd, name = tempfile.mkstemp(prefix='.pe7-incident-', dir=self.path.parent)
            temporary = Path(name)
            with os.fdopen(fd, 'wb') as stream:
                stream.write(raw)
                stream.flush()
                os.fsync(stream.fileno())
            os.chmod(temporary, 0o600)
            require(temporary.read_bytes() == raw, 'STORE_UNAVAILABLE')
            os.replace(temporary, self.path)
            temporary, replaced = None, True
            if os.name == 'posix':
                directory = os.open(self.path.parent, os.O_RDONLY | os.O_DIRECTORY)
                try:
                    os.fsync(directory)
                finally:
                    os.close(directory)
        except Exception:
            if replaced:
                self.uncertain = True
            raise PolicyError('COMMIT_UNKNOWN' if replaced else 'STORE_UNAVAILABLE', uncertain=replaced) from None
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)


def apply_evaluation(state, policy, evaluation):
    """Pure case transition; caller commits cases and outbox together under engine lock."""
    updated = copy.deepcopy(validate_state(state))
    key = digest(['pe7_expected_availability', policy['asset_id']])
    case = updated['cases'].get(key)
    availability, now = evaluation['availability_state'], evaluation['evaluated_at']
    if case is None and availability not in ('DEGRADED', 'OFFLINE'):
        return updated
    if case is None or case['lifecycle'] == 'resolved' and availability == 'OFFLINE':
        episode = case['episode'] + 1 if case else 1
        case = dict(asset_id=policy['asset_id'], episode=episode, incident_id=digest([key, episode]),
                    lifecycle='detected', suppression_reason=None, availability_state=availability, severity='warning',
                    policy_revision=policy['revision'], profile_revision=evaluation['profile_revision'],
                    detected_at=now, updated_at=now, resolved_at=None, machine={}, events=[])
        updated['cases'][key] = case
    case.update(machine=evaluation['state'], availability_state=availability, updated_at=now,
                policy_revision=policy['revision'], profile_revision=evaluation['profile_revision'] or case['profile_revision'])
    if availability == 'NOT_MONITORED':
        case['suppression_reason'] = 'OPERATOR_DISABLED'
        for event in updated['outbox'].values():
            if event['asset_id'] == policy['asset_id']:
                event.update(off_revision=policy['revision'], off_at=now)
                if event['state'] in ('PROPOSED', 'PENDING_AUTHORIZATION'):
                    event['state'] = 'CANCELLED'
        return updated
    case['suppression_reason'] = None
    for event in updated['outbox'].values():
        expected_state = 'OFFLINE' if event['event']['event_kind'] == 'OUTAGE_STARTED' else 'AVAILABLE'
        if (event['asset_id'] == policy['asset_id'] and event['state'] == 'PENDING_AUTHORIZATION'
                and availability == expected_state):
            event.update(policy_revision=policy['revision'], store_epoch=policy['store_epoch'],
                         evidence_sha256=evaluation['input_sha256'], evidence_valid_until=evaluation['valid_until'])
            event['event']['policy_revision'] = policy['revision']
    kind = None
    if availability == 'OFFLINE' and case['lifecycle'] in ('detected', 'confirmed'):
        case['lifecycle'] = 'active'
        kind = 'OUTAGE_STARTED'
    elif availability == 'RECOVERING' and case['lifecycle'] == 'active':
        case['lifecycle'] = 'recovering'
    elif availability == 'AVAILABLE' and case['lifecycle'] in ('active', 'recovering'):
        case.update(lifecycle='resolved', resolved_at=now)
        kind = 'OUTAGE_RECOVERED'
    elif availability == 'OFFLINE' and case['lifecycle'] == 'recovering':
        case['lifecycle'] = 'active'
    if kind is not None:
        event_id = digest([key, case['episode'], kind])
        if event_id not in case['events']:
            event = dict(schema_version='1.0', event_id=event_id, incident_id=case['incident_id'], event_kind=kind,
                         severity='warning', occurred_at=now, policy_revision=policy['revision'],
                         asset_id_digest=digest(policy['asset_id']))
            case['events'].append(event_id)
            updated['outbox'][event_id] = dict(event=event, asset_id=policy['asset_id'], store_epoch=policy['store_epoch'],
                policy_revision=policy['revision'], evidence_sha256=evaluation['input_sha256'],
                evidence_valid_until=evaluation['valid_until'], state='PENDING_AUTHORIZATION', grant=None,
                off_revision=None, off_at=None)
    return validate_state(updated)


def restart(state):
    updated = copy.deepcopy(validate_state(state))
    updated['process_epoch'] = uuid.uuid4().hex
    for event in updated['outbox'].values():
        if event['state'] == 'AUTHORIZED':
            event['state'] = event['grant']['state'] = 'EXPIRED'
        elif event['state'] == 'IN_FLIGHT':
            event['state'] = event['grant']['state'] = 'DELIVERY_UNKNOWN'
            event['grant']['outcome'] = 'PROCESS_RESTART_UNKNOWN'
    return updated


class Dispatcher:
    """Guard -> incident lock only. The caller must release its batch lock first."""
    def __init__(self, service, engine, clock, process_epoch, operator_enabled, *, barrier=lambda _: None):
        self.service, self.engine, self.clock = service, engine, clock
        self.process_epoch, self.operator_enabled, self.barrier = process_epoch, operator_enabled, barrier

    @contextmanager
    def guarded(self):
        require(not self.engine.held, 'FORBIDDEN')
        with AssetLock(self.service.store.lock_path, shared=True):
            if self.service.store.uncertain:
                raise PolicyError('COMMIT_UNKNOWN', uncertain=True)
            store = self.service.store.load_store()
            require(store['schema_version'] == '2.0', 'UNSUPPORTED_SCHEMA')
            if not self.service.store.durability_pair_confirmed(store):
                raise PolicyError('COMMIT_UNKNOWN', uncertain=True)
            with self.engine.transaction():
                yield store, self.engine.read()

    def authorize(self, event_id):
        with self.guarded() as (store, state):
            event = state['outbox'][event_id]
            now = timestamp(self.clock())
            record = store['assets'].get(event['asset_id'])
            case = state['cases'].get(digest(['pe7_expected_availability', event['asset_id']]))
            required_availability = 'OFFLINE' if event['event']['event_kind'] == 'OUTAGE_STARTED' else 'AVAILABLE'
            require(event['state'] == 'PENDING_AUTHORIZATION' and record is not None and
                    record.get('expected_availability') is True and record.get('revision') == event['policy_revision'] and
                    store['store_epoch'] == event['store_epoch'] and self.operator_enabled() is True and
                    self.service.attachment(event['asset_id']) == 'strong' and case is not None and
                    case['suppression_reason'] is None and case['availability_state'] == required_availability and
                    case['policy_revision'] == event['policy_revision'], 'FORBIDDEN')
            deadline = min(now + timedelta(seconds=5), timestamp(event['evidence_valid_until']))
            require(now < deadline and state['process_epoch'] == self.process_epoch, 'FORBIDDEN')
            event['grant'] = dict(grant_id=uuid.uuid4().hex, event_id=event_id, store_epoch=store['store_epoch'],
                asset_revision=record['revision'], evidence_sha256=event['evidence_sha256'], authorized_at=time_text(now),
                not_after=time_text(deadline), process_epoch=self.process_epoch, state='AUTHORIZED', claimed_at=None,
                transport_started_at=None, completed_at=None, outcome=None)
            event['state'] = 'AUTHORIZED'
            self.barrier('before_authorization_commit')
            self.engine.write(state)  # Linearization: replacement + parent fsync under shared Asset guard.
            self.barrier('after_authorization_commit')
            return copy.deepcopy(event['grant'])

    def claim(self, event_id):
        with self.guarded() as (store, state):
            event = state['outbox'][event_id]
            grant = event['grant']
            require(event['state'] == 'AUTHORIZED' and grant is not None and
                    grant['process_epoch'] == self.process_epoch == state['process_epoch'] and
                    grant['store_epoch'] == store['store_epoch'] and
                    timestamp(self.clock()) < timestamp(grant['not_after']), 'FORBIDDEN')
            # Current OFF cannot revoke the already durable pre-OFF grant. Epoch restore can.
            event['state'] = grant['state'] = 'IN_FLIGHT'
            grant['claimed_at'] = self.clock()
            self.engine.write(state)
            return copy.deepcopy(event)

    def _outcome(self, event_id, state_name, now, outcome, started=None):
        with self.engine.transaction():
            state = self.engine.read()
            event = state['outbox'][event_id]
            require(event['state'] == 'IN_FLIGHT' and event['grant']['process_epoch'] == self.process_epoch, 'FORBIDDEN')
            event['state'] = event['grant']['state'] = state_name
            event['grant'].update(completed_at=now, outcome=outcome, transport_started_at=started)
            self.engine.write(state)

    def submit(self, claimed, transport):
        require(not self.engine.held, 'FORBIDDEN')
        event_id, grant = claimed['event']['event_id'], claimed['grant']
        require(claimed['state'] == 'IN_FLIGHT' and grant['process_epoch'] == self.process_epoch, 'FORBIDDEN')
        now = self.clock()
        remaining = (timestamp(grant['not_after']) - timestamp(now)).total_seconds()
        if remaining <= 0:
            self._outcome(event_id, 'EXPIRED', now, 'DEADLINE_EXPIRED')
            return 'EXPIRED'
        require(transport.deadline_aware is True and transport.automatic_retries is False and
                transport.offline_queue is False, 'FORBIDDEN')
        self.barrier('transport_boundary')
        # Transport must consume the absolute deadline too, not just a socket timeout.
        now = self.clock()
        if timestamp(now) >= timestamp(grant['not_after']):
            self._outcome(event_id, 'EXPIRED', now, 'DEADLINE_EXPIRED')
            return 'EXPIRED'
        # Consume this claimant's sole attempt durably BEFORE network I/O. Reusing
        # a copied claimed object cannot submit twice, even in the same process.
        with self.engine.transaction():
            current = self.engine.read()
            actual = current['outbox'][event_id]
            require(actual['state'] == 'IN_FLIGHT' and actual['grant']['grant_id'] == grant['grant_id'] and
                    actual['grant']['transport_started_at'] is None, 'FORBIDDEN')
            actual['grant']['transport_started_at'] = now
            self.engine.write(current)
        try:
            outcome = transport.send_once(claimed['event'], deadline=grant['not_after'],
                                          timeout=min(remaining, 5))
            require(outcome in ('TRANSPORT_ACCEPTED', 'DELIVERED', 'FAILED_NOT_SUBMITTED', 'DELIVERY_UNKNOWN'))
        except Exception:
            outcome = 'DELIVERY_UNKNOWN'
        self._outcome(event_id, outcome, self.clock(), outcome, now)
        return outcome


def summary(state, now, valid_until):
    validate_state(state)
    cases = [dict(incident_id=c['incident_id'], asset_id_digest=digest(c['asset_id']), episode=c['episode'],
                  lifecycle=c['lifecycle'], availability_state=c['availability_state'],
                  suppression_reason=c['suppression_reason'], severity=c['severity'], policy_revision=c['policy_revision'],
                  profile_revision=c['profile_revision'], detected_at=c['detected_at'], updated_at=c['updated_at'])
             for c in state['cases'].values()]
    cases.sort(key=lambda c: (c['severity'], c['detected_at'], c['incident_id']))
    return dict(schema_version='1.0', evaluated_at=now, valid_until=valid_until, status='VALID',
                total_case_count=len(cases), omitted_case_count=0, cases=cases)


def displayed(legacy, projection):
    if legacy.get('status') == 'active':
        return copy.deepcopy(legacy)
    cases = [c for c in projection['cases'] if c['lifecycle'] in ('active', 'recovering') and c['suppression_reason'] is None]
    if not cases:
        return copy.deepcopy(legacy)
    if projection['status'] != 'VALID':
        return dict(status='unknown', phase='unknown', severity='warning', system='HIOC',
                    title='Expected availability evidence unavailable',
                    summary='Unresolved PE-7 cases retained; no all-clear established', updated=projection['evaluated_at'])
    case = cases[0]
    return dict(id=case['incident_id'], status='active', phase=case['lifecycle'], severity='warning',
                system='HIOC', title='Expected availability incident', summary='Qualified availability evidence',
                updated=case['updated_at'])
