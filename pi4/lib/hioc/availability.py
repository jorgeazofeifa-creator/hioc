"""Pure, evidence-qualified PE-7 evaluation. No probes, writes, or timing defaults."""
from __future__ import annotations
import copy
from datetime import timedelta
from .availability_contract import (
    PolicyError, asset_id, digest, hex_digest, identifier, integer, keys,
    require, time_text, timestamp, uuid4,
)

PROFILE_KEYS = ('schema_version', 'profile_id', 'revision', 'enabled_sources', 'source_definitions',
                'evaluation_interval_seconds', 'negative_confirmations', 'recovery_confirmations',
                'grace_seconds', 'reminder_interval_seconds')
SOURCE_KEYS = ('source_id', 'kind', 'expected_report_seconds', 'allowed_jitter_seconds',
               'max_age_seconds', 'positive_meanings', 'negative_meanings',
               'physical_device_authority', 'mapping_revision', 'mapping_sha256')
OBSERVATION_KEYS = ('schema_version', 'source_id', 'source_kind', 'asset_id', 'device_id',
                    'source_epoch', 'sample_id', 'observed_at', 'collected_at', 'collection_status',
                    'completeness', 'evidence_kind', 'scope', 'authority_ref', 'valid_until',
                    'reason_code', 'source_sha256')


def validate_profile(value):
    keys(value, PROFILE_KEYS)
    require(value['schema_version'] == '1.0')
    identifier(value['profile_id'])
    integer(value['revision'])
    enabled = value['enabled_sources']
    require(type(enabled) is list and 1 <= len(enabled) <= 16 and enabled == sorted(set(enabled)))
    require(type(value['source_definitions']) is dict and set(value['source_definitions']) == set(enabled))
    for name in ('evaluation_interval_seconds', 'grace_seconds'):
        integer(value[name])
    for name in ('negative_confirmations', 'recovery_confirmations'):
        integer(value[name], 2)
    require(value['reminder_interval_seconds'] is None)
    for source in enabled:
        identifier(source)
        definition = value['source_definitions'][source]
        keys(definition, SOURCE_KEYS)
        require(definition['source_id'] == source and definition['kind'] in ('network', 'ha'))
        for name in ('expected_report_seconds', 'max_age_seconds', 'mapping_revision'):
            integer(definition[name])
        integer(definition['allowed_jitter_seconds'], 0)
        cadence = definition['expected_report_seconds'] + definition['allowed_jitter_seconds']
        require(definition['max_age_seconds'] >= cadence and value['grace_seconds'] >= cadence)
        require(type(definition['physical_device_authority']) is bool)
        hex_digest(definition['mapping_sha256'])
        for name in ('positive_meanings', 'negative_meanings'):
            meanings = definition[name]
            require(type(meanings) is list and len(meanings) <= 16 and len(set(meanings)) == len(meanings))
            for meaning in meanings:
                require(type(meaning) is str and 1 <= len(meaning) <= 128 and
                        all(ord(ch) >= 32 and ord(ch) != 127 for ch in meaning))
        require(not set(definition['positive_meanings']) & set(definition['negative_meanings']))
    return value


def validate_observation(value):
    keys(value, OBSERVATION_KEYS)
    require(value['schema_version'] == '1.0' and value['source_kind'] in ('network', 'ha'))
    for name in ('source_id', 'authority_ref', 'reason_code'):
        identifier(value[name])
    for name in ('asset_id', 'device_id'):
        asset_id(value[name])
    uuid4(value['source_epoch'])
    hex_digest(value['sample_id'])
    hex_digest(value['source_sha256'])
    for name in ('observed_at', 'collected_at', 'valid_until'):
        timestamp(value[name])
    require(value['collection_status'] in ('SUCCESS', 'FAILED', 'UNAVAILABLE'))
    require(value['completeness'] in ('COMPLETE', 'INCOMPLETE'))
    require(value['evidence_kind'] in ('POSITIVE', 'NEGATIVE', 'UNKNOWN'))
    require(value['scope'] in ('DEVICE', 'ENTITY'))
    return value


MACHINE_KEYS = ('baseline', 'expected', 'sources', 'negative_count', 'positive_count', 'negative_since',
                'evaluated_at', 'applied_policy_revision', 'availability_state', 'input_sha256', 'valid_until',
                'profile_revision')


def validate_machine(value):
    keys(value, MACHINE_KEYS)
    require(value['baseline'] is None or hex_digest(value['baseline']))
    require(type(value['expected']) is bool and type(value['sources']) is dict and len(value['sources']) <= 16)
    for name in ('negative_count', 'positive_count'):
        integer(value[name], 0)
    integer(value['applied_policy_revision'])
    if value['profile_revision'] is not None: integer(value['profile_revision'])
    timestamp(value['evaluated_at']); hex_digest(value['input_sha256'])
    for name in ('negative_since', 'valid_until'):
        if value[name] is not None: timestamp(value[name])
    require(value['availability_state'] in ('NOT_MONITORED', 'AVAILABLE', 'UNKNOWN', 'STALE', 'DEGRADED', 'OFFLINE', 'RECOVERING'))
    for source, row in value['sources'].items():
        identifier(source)
        keys(row, ('source_epoch', 'sample_id', 'observed_at', 'retired_epochs'))
        uuid4(row['source_epoch']); hex_digest(row['sample_id']); timestamp(row['observed_at'])
        require(type(row['retired_epochs']) is list and len(row['retired_epochs']) <= 16 and
                len(set(row['retired_epochs'])) == len(row['retired_epochs']))
        for epoch in row['retired_epochs']: uuid4(epoch)
        require(row['source_epoch'] not in row['retired_epochs'])
    return value


def evaluate(policy, attachment, profile, observations, prior, now, *, case_open=False):
    """Return a new machine state. Distinct advancing producer reports count once.

    Infrastructure/descriptive revisions rebind the applied revision without resetting
    the Expected Availability baseline. Unknown evidence freezes counters and cases.
    """
    instant = timestamp(now)
    asset_id(policy['asset_id']); uuid4(policy['store_epoch']); integer(policy['revision'])
    require(policy['expected_availability'] is None or type(policy['expected_availability']) is bool)
    state = copy.deepcopy(validate_machine(prior)) if prior is not None else dict(
        baseline=None, expected=False, sources={}, negative_count=0, positive_count=0, negative_since=None,
        evaluated_at=now, applied_policy_revision=policy['revision'], availability_state='UNKNOWN',
        input_sha256='0'*64, valid_until=None, profile_revision=None)
    previous_time = state.get('evaluated_at')
    result = dict(state=state, availability_state='UNKNOWN', reason_code='MISSING_PROFILE',
                  evaluated_at=now, valid_until=None, policy_revision=policy.get('revision'),
                  profile_revision=(profile.get('revision') if type(profile) is dict and
                                    type(profile.get('revision')) is int and 1 <= profile['revision'] <= 2**53-1 else None),
                  input_sha256=digest([policy, attachment, profile, observations]))
    def finish(status, reason):
        state.update(evaluated_at=now, applied_policy_revision=policy.get('revision'),
                     availability_state=status, input_sha256=result['input_sha256'], valid_until=result['valid_until'],
                     profile_revision=result['profile_revision'])
        validate_machine(state)
        result.update(availability_state=status, reason_code=reason)
        return result
    if policy.get('expected_availability') is not True:
        state.update(expected=False, sources={}, negative_count=0, positive_count=0, negative_since=None)
        return finish('NOT_MONITORED', 'OPERATOR_DISABLED')
    if attachment != 'strong':
        return finish('UNKNOWN', 'UNKNOWN_IDENTITY')
    if previous_time is not None and timestamp(previous_time) > instant:
        state.update(sources={}, negative_count=0, positive_count=0, negative_since=None)
        return finish('UNKNOWN', 'CLOCK_REVERSED')
    if profile is None:
        return finish('UNKNOWN', 'MISSING_PROFILE')
    try:
        validate_profile(profile)
    except (PolicyError, TypeError, ValueError):
        return finish('UNKNOWN', 'INVALID_PROFILE')
    baseline = digest([policy.get('store_epoch'), policy.get('asset_id'), True, profile])
    if state.get('baseline') != baseline or state.get('expected') is not True:
        state.update(baseline=baseline, expected=True, sources={}, negative_count=0,
                     positive_count=0, negative_since=None)
        result['state'] = state
    require(type(observations) is list and len(observations) <= 256)
    usable, aged, fresh_samples = [], [], []
    for source in profile['enabled_sources']:
        definition = profile['source_definitions'][source]
        found = [row for row in observations if type(row) is dict and row.get('source_id') == source]
        if len(found) != 1:
            return finish('UNKNOWN', 'SOURCE_MISSING_OR_DUPLICATE')
        row = found[0]
        try:
            validate_observation(row)
            require(row['asset_id'] == policy['asset_id'] == row['device_id'])
            require(row['source_kind'] == definition['kind'])
            require(row['authority_ref'] == digest([source, definition['mapping_revision'], definition['mapping_sha256']]))
            observed, collected, deadline = (timestamp(row[name]) for name in ('observed_at', 'collected_at', 'valid_until'))
            require(observed <= collected <= instant and observed < deadline)
        except (PolicyError, TypeError, ValueError):
            return finish('UNKNOWN', 'INVALID_SOURCE')
        if row['collection_status'] != 'SUCCESS' or row['completeness'] != 'COMPLETE':
            return finish('UNKNOWN', 'SOURCE_UNAVAILABLE')
        if instant >= min(deadline, observed + timedelta(seconds=definition['max_age_seconds'])):
            aged.append(row)
            continue
        actual_deadline = min(deadline, observed + timedelta(seconds=definition['max_age_seconds']))
        result['valid_until'] = min(result['valid_until'] or time_text(actual_deadline), time_text(actual_deadline))
        physical = row['scope'] == 'DEVICE' and definition['physical_device_authority'] is True
        previous = state['sources'].get(source)
        retired = previous['retired_epochs'][:] if previous is not None else []
        if row['source_epoch'] in retired:
            return finish('UNKNOWN', 'RETIRED_SOURCE_EPOCH')
        if previous is not None and previous['source_epoch'] != row['source_epoch']:
            require(len(retired) < 16, 'BUSY')
            retired.append(previous['source_epoch'])
            state.update(negative_count=0, positive_count=0, negative_since=None)
            previous = None
        if previous is None or (row['observed_at'] > previous['observed_at'] and row['sample_id'] != previous['sample_id']):
            state['sources'][source] = dict({name: row[name] for name in ('source_epoch', 'sample_id', 'observed_at')}, retired_epochs=retired)
            fresh_samples.append((row['evidence_kind'], physical, row['observed_at']))
        elif row['observed_at'] < previous['observed_at']:
            return finish('UNKNOWN', 'SOURCE_OUT_OF_ORDER')
        usable.append((row, physical))
    if aged:
        return finish('STALE' if not usable else 'UNKNOWN', 'SOURCE_STALE')
    positives = [row for row, physical in usable if physical and row['evidence_kind'] == 'POSITIVE']
    negatives = [row for row, physical in usable if physical and row['evidence_kind'] == 'NEGATIVE']
    if positives and negatives:
        return finish('UNKNOWN', 'SOURCE_CONFLICT')
    if any(row['evidence_kind'] == 'UNKNOWN' for row, _ in usable):
        return finish('UNKNOWN', 'SOURCE_UNKNOWN')
    if positives:
        if any(kind == 'POSITIVE' and physical for kind, physical, _ in fresh_samples):
            state['positive_count'] += 1
            state.update(negative_count=0, negative_since=None)
        if case_open and state['positive_count'] < profile['recovery_confirmations']:
            return finish('RECOVERING', 'RECOVERY_PENDING')
        return finish('AVAILABLE', 'QUALIFIED_POSITIVE')
    if negatives:
        advancing = [at for kind, physical, at in fresh_samples if kind == 'NEGATIVE' and physical]
        if advancing:
            state['negative_count'] += 1
            state['positive_count'] = 0
            state['negative_since'] = state['negative_since'] or now
        elapsed = 0 if state['negative_since'] is None else (instant - timestamp(state['negative_since'])).total_seconds()
        if state['negative_count'] >= profile['negative_confirmations'] and elapsed >= profile['grace_seconds']:
            return finish('OFFLINE', 'QUALIFIED_NEGATIVE')
        return finish('DEGRADED', 'NEGATIVE_PENDING')
    # Entity evidence may establish only its scope, never a physical outage/recovery.
    return finish('DEGRADED', 'ENTITY_SCOPE_ONLY')


# Section 6.1 projections are engine-owned evidence, never policy or case authority.
STATUS_KEYS = ('schema_version', 'result', 'asset_id', 'read_at', 'status_reason',
    'expected_availability', 'policy_status', 'current_policy_revision',
    'applied_policy_revision', 'policy_binding', 'evaluation', 'observations')
EVALUATION_KEYS = ('availability_state', 'reason_code', 'evidence_scope', 'evaluated_at', 'valid_until', 'freshness')
QUALITY_KEYS = ('source_ref', 'scope', 'collection_status', 'completeness', 'freshness', 'observed_at', 'valid_until')
REASONS = frozenset(('QUALIFIED_POSITIVE', 'QUALIFIED_NEGATIVE', 'RECOVERY_PENDING', 'NEGATIVE_PENDING',
    'ENTITY_SCOPE_ONLY', 'SOURCE_STALE', 'SOURCE_MISSING', 'SOURCE_MISSING_OR_DUPLICATE',
    'COLLECTION_FAILED', 'COLLECTION_INCOMPLETE', 'COLLECTION_UNAVAILABLE', 'SOURCE_CONFLICT',
    'SOURCE_UNKNOWN', 'INVALID_SOURCE', 'MISSING_PROFILE', 'INVALID_PROFILE', 'UNKNOWN_IDENTITY',
    'OPERATOR_DISABLED', 'CLOCK_REVERSED', 'RETIRED_SOURCE_EPOCH', 'SOURCE_OUT_OF_ORDER'))


def evaluation_snapshot(policy, result, profile, observations):
    """Capture only recorded quality used by this evaluation; no reads or execution."""
    quality, scopes = None, set()
    reason = result['reason_code']
    if result['availability_state'] == 'NOT_MONITORED':
        quality = []
    elif profile is not None:
        try:
            validate_profile(profile)
            quality = []
            for source in profile['enabled_sources']:
                rows = [v for v in observations if v.get('source_id') == source]
                item = dict(source_ref=digest(source), scope='NONE' if not rows else 'UNKNOWN',
                    collection_status='ABSENT' if not rows else 'UNKNOWN', completeness='UNKNOWN',
                    freshness='ABSENT' if not rows else 'UNKNOWN', observed_at=None, valid_until=None)
                if len(rows) == 1:
                    row = rows[0]
                    try:
                        validate_observation(row)
                        definition = profile['source_definitions'][source]
                        require(row['device_id'] == row['asset_id'] == policy['asset_id'] and
                            row['source_kind'] == definition['kind'] and row['authority_ref'] ==
                            digest([source, definition['mapping_revision'], definition['mapping_sha256']]))
                        observed, collected, deadline = [timestamp(row[k]) for k in ('observed_at','collected_at','valid_until')]
                        require(observed <= collected <= timestamp(result['evaluated_at']) and observed < deadline)
                        deadline = min(deadline, observed + timedelta(seconds=definition['max_age_seconds']))
                        item.update(scope=row['scope'], collection_status=row['collection_status'],
                            completeness=row['completeness'], observed_at=row['observed_at'], valid_until=time_text(deadline))
                        scopes.add(row['scope'])
                        if row['collection_status'] == 'SUCCESS' and row['completeness'] == 'COMPLETE':
                            item['freshness'] = 'FRESH' if timestamp(result['evaluated_at']) < deadline else 'STALE'
                    except (ValueError, KeyError, TypeError):
                        pass
                quality.append(item)
            quality.sort(key=lambda x:x['source_ref'])
        except (ValueError, KeyError, TypeError):
            quality = None
    if reason == 'SOURCE_MISSING_OR_DUPLICATE' and quality is not None:
        failed = next((source for source in profile['enabled_sources'] if
            sum(row.get('source_id') == source for row in observations) != 1), None)
        if failed is not None and not any(row.get('source_id') == failed for row in observations):
            reason = 'SOURCE_MISSING'
    if reason == 'SOURCE_UNAVAILABLE':
        ordered = sorted(quality or [], key=lambda row: profile['enabled_sources'].index(next(
            source for source in profile['enabled_sources'] if digest(source) == row['source_ref'])))
        first = next((v for v in ordered if v['collection_status'] != 'SUCCESS' or v['completeness'] != 'COMPLETE'), None)
        reason = ('COLLECTION_FAILED' if first and first['collection_status']=='FAILED' else
            'COLLECTION_INCOMPLETE' if first and first['completeness']=='INCOMPLETE' else 'COLLECTION_UNAVAILABLE')
    require(reason in REASONS)
    scope = 'UNKNOWN' if quality is None or any(row['scope']=='UNKNOWN' for row in quality) else 'MIXED' if len(scopes)>1 else next(iter(scopes),'NONE')
    return dict(store_epoch=policy['store_epoch'], policy_revision=policy['revision'], machine=result['state'],
        evaluation=dict(availability_state=result['availability_state'], reason_code=reason, evidence_scope=scope,
            evaluated_at=result['evaluated_at'], valid_until=result['valid_until'], freshness='UNKNOWN'), observations=quality)


def validate_status(value):
    """Closed external status schema, also used to validate persisted projections."""
    keys(value, STATUS_KEYS); require(value['schema_version']=='1.0'); asset_id(value['asset_id'])
    instant=timestamp(value['read_at'])
    require(value['result'] in ('READ','NOT_EVALUATED','UNAVAILABLE'))
    require(value['status_reason'] in ('SNAPSHOT_READ','NOT_EVALUATED','EVALUATION_STORAGE_UNAVAILABLE',
        'POLICY_STORAGE_UNAVAILABLE','POLICY_CHANGED_DURING_READ'))
    require(value['policy_status'] in ('PRESENT','ABSENT','UNAVAILABLE'))
    require(value['expected_availability'] is None or type(value['expected_availability']) is bool)
    if value['policy_status']=='PRESENT': integer(value['current_policy_revision'])
    else: require(value['current_policy_revision'] is None and value['expected_availability'] is None)
    require(value['policy_binding'] in ('CURRENT','PENDING','UNKNOWN'))
    if value['result']!='READ':
        require(value['evaluation'] is None and value['observations'] is None and
            value['applied_policy_revision'] is None and value['policy_binding']=='UNKNOWN')
        require(value['status_reason']=='NOT_EVALUATED' if value['result']=='NOT_EVALUATED' else
            value['status_reason'] in ('EVALUATION_STORAGE_UNAVAILABLE','POLICY_STORAGE_UNAVAILABLE','POLICY_CHANGED_DURING_READ'))
        require(value['policy_status']!='UNAVAILABLE' if value['result']=='NOT_EVALUATED' else True)
    else:
        require(value['status_reason']=='SNAPSHOT_READ' and value['policy_status']!='UNAVAILABLE')
        integer(value['applied_policy_revision'])
        e=keys(value['evaluation'], EVALUATION_KEYS)
        require(e['availability_state'] in ('NOT_MONITORED','AVAILABLE','UNKNOWN','STALE','DEGRADED','OFFLINE','RECOVERING'))
        require(e['reason_code'] in REASONS and e['evidence_scope'] in ('DEVICE','ENTITY','MIXED','NONE','UNKNOWN'))
        reasons_by_state = {'NOT_MONITORED': {'OPERATOR_DISABLED'}, 'AVAILABLE': {'QUALIFIED_POSITIVE'},
            'RECOVERING': {'RECOVERY_PENDING'}, 'OFFLINE': {'QUALIFIED_NEGATIVE'},
            'DEGRADED': {'NEGATIVE_PENDING','ENTITY_SCOPE_ONLY'}, 'STALE': {'SOURCE_STALE'}}
        if e['availability_state'] in reasons_by_state:
            require(e['reason_code'] in reasons_by_state[e['availability_state']])
        evaluated=timestamp(e['evaluated_at']); deadline=None if e['valid_until'] is None else timestamp(e['valid_until'])
        require(e['freshness'] in ('FRESH','EXPIRED','UNKNOWN'))
        if e['freshness']=='FRESH': require(deadline is not None and evaluated<=instant<deadline)
        if e['freshness']=='EXPIRED': require(deadline is not None and instant>=deadline)
        if value['policy_binding']=='CURRENT': require(value['current_policy_revision']==value['applied_policy_revision'])
    rows=value['observations']
    if rows is not None:
        require(type(rows) is list and len(rows)<=16)
        refs=[]
        for row in rows:
            keys(row, QUALITY_KEYS); refs.append(hex_digest(row['source_ref']))
            require(row['scope'] in ('DEVICE','ENTITY','NONE','UNKNOWN') and
                row['collection_status'] in ('SUCCESS','FAILED','UNAVAILABLE','ABSENT','UNKNOWN') and
                row['completeness'] in ('COMPLETE','INCOMPLETE','UNKNOWN') and row['freshness'] in ('FRESH','STALE','ABSENT','UNKNOWN'))
            for k in ('observed_at','valid_until'):
                if row[k] is not None: timestamp(row[k])
            if row['collection_status']=='ABSENT':
                require(row['scope']=='NONE' and row['freshness']=='ABSENT' and row['completeness']=='UNKNOWN' and
                    row['observed_at'] is None and row['valid_until'] is None)
            if row['freshness'] in ('FRESH','STALE'):
                require(row['collection_status']=='SUCCESS' and row['completeness']=='COMPLETE' and
                    timestamp(row['observed_at'])<=instant)
                require(instant<timestamp(row['valid_until']) if row['freshness']=='FRESH' else instant>=timestamp(row['valid_until']))
        require(refs==sorted(set(refs)))
    require(len(__import__('hioc.availability_contract',fromlist=['canonical']).canonical(value))<=16384)
    return value


class AvailabilityReader:
    """One bounded policy/evidence/policy read. No initialization, evaluation or writes."""
    def __init__(self, service, engine, clock):
        self.service,self.engine,self.clock=service,engine,clock
        service.evaluation_snapshot_reader = self.snapshot

    def snapshot(self, key):
        from .availability_incidents import validate_state
        require(not self.engine.uncertain, 'STORE_UNAVAILABLE')
        state = validate_state(strict_status_json(self.service.store.read_bytes(self.engine.path)))
        return __import__('copy').deepcopy(state['evaluations'].get(key))

    def _policy(self, key):
        from .assets import AssetLock
        store=self.service.store
        with AssetLock(store.lock_path, shared=True, read_only=True):
            require(not store.uncertain, 'STORE_UNAVAILABLE')
            value=store.load_store(); require(value['schema_version']=='2.0','UNSUPPORTED_SCHEMA')
            require(store.durability_pair_confirmed(value),'STORE_UNAVAILABLE')
            record=value['assets'].get(key)
            return (value['store_epoch'], record['revision'] if record else None,
                record['expected_availability'] if record else None, 'PRESENT' if record else 'ABSENT')

    def read(self, key):
        import copy
        asset_id(key); now=self.clock(); timestamp(now)
        response=dict(schema_version='1.0',result='UNAVAILABLE',asset_id=key,read_at=now,
            status_reason='POLICY_STORAGE_UNAVAILABLE',expected_availability=None,policy_status='UNAVAILABLE',
            current_policy_revision=None,applied_policy_revision=None,policy_binding='UNKNOWN',evaluation=None,observations=None)
        try: policy=self._policy(key)
        except Exception: return validate_status(response)
        response.update(expected_availability=policy[2],policy_status=policy[3],current_policy_revision=policy[1],
            status_reason='EVALUATION_STORAGE_UNAVAILABLE')
        try:
            snapshot=self.snapshot(key)
        except Exception: return validate_status(response)
        try: after=self._policy(key)
        except Exception: after=None
        if after!=policy:
            response.update(expected_availability=None,policy_status='UNAVAILABLE',current_policy_revision=None,
                status_reason='POLICY_CHANGED_DURING_READ')
            return validate_status(response)
        if snapshot is None:
            response.update(result='NOT_EVALUATED',status_reason='NOT_EVALUATED')
        else:
            evaluation=snapshot['evaluation']; rows=snapshot['observations']
            deadline=evaluation['valid_until']; evaluated=timestamp(evaluation['evaluated_at'])
            evaluation['freshness']=('UNKNOWN' if deadline is None or timestamp(now)<evaluated else
                'FRESH' if timestamp(now)<timestamp(deadline) else 'EXPIRED')
            for row in rows or []:
                if row['freshness']=='FRESH' and timestamp(now)>=timestamp(row['valid_until']): row['freshness']='STALE'
            response.update(result='READ',status_reason='SNAPSHOT_READ',evaluation=evaluation,observations=rows,
                applied_policy_revision=snapshot['policy_revision'],policy_binding='CURRENT' if
                (snapshot['store_epoch'],snapshot['policy_revision'])==policy[:2] else 'PENDING')
        return validate_status(response)


def strict_status_json(raw):
    from .availability_contract import strict_json
    return strict_json(raw,limit=16777216,depth=24)
