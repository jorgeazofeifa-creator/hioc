"""HA federated operator services. Disabled unless explicitly configured.

Tokens stay inside HA. Service identity is not human identity: each assertion
requires fresh connection/user/provider checks and independent backend authorization.
"""
from __future__ import annotations
import hashlib
import asyncio
import hmac
import http.client
import json
import os
from pathlib import Path
import re
import ssl
import stat
import time
import uuid
from datetime import datetime, timedelta, timezone
from urllib.parse import urlsplit

DOMAIN = 'hioc_operator'
SERVICE_ROUTES = dict(get_policy='get', create_asset_policy='create',
                      update_asset_policy='update', get_operation_result='result',
                      get_availability_status='availability_status')
POLICY_FIELDS = {'expected_availability', 'infrastructure_device', 'infrastructure_type'}


class BridgeError(Exception):
    pass


def require(ok):
    if not ok:
        raise BridgeError('HIOC request unavailable or unauthorized')


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True,
                      allow_nan=False).encode('ascii')


def sha(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def secret_path(value):
    path = Path(value)
    require(path.is_absolute())
    info = path.lstat()
    require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1)
    require(all(not ancestor.is_symlink() for ancestor in path.parents))
    if os.name == 'posix':
        parent = path.parent.lstat()
        require(info.st_uid == os.getuid() and stat.S_IMODE(info.st_mode) == 0o600 and
                parent.st_uid == os.getuid() and stat.S_IMODE(parent.st_mode) == 0o700)
    return path


async def verified_actor(hass, call, allowlist, connection_context, *, now=None):
    """Capability-tested against HA 2026.8.1 source; no mock actor claims in payload."""
    require(call.context is not None and call.context.user_id is not None and call.context.parent_id is None)
    connection = connection_context.get()
    require(connection is not None and connection.user.id == call.context.user_id)
    # HA close replaces this callback even in already-created async service tasks.
    require(getattr(connection.send_message, '__func__', None) !=
            getattr(connection._connect_closed_error, '__func__', None))
    user = await hass.auth.async_get_user(call.context.user_id)
    require(user is not None and user.id == connection.user.id and user.is_active is True and
            user.system_generated is False and user.is_admin is True and user.id in allowlist)
    token = hass.auth.async_get_refresh_token(connection.refresh_token_id)
    require(token is not None and token.user.id == user.id and token.token_type == 'normal')
    instant = time.time() if now is None else now
    require(token.expire_at is None or type(token.expire_at) in (int, float) and token.expire_at > instant)
    # Provider validation is a synchronous HA callback, despite its async_ prefix.
    hass.auth.async_validate_refresh_token(token, connection.remote)
    require(connection_context.get() is connection and user.is_active is True)
    return user.id, call.context.id


def validate_payload(operation, payload):
    require(operation in SERVICE_ROUTES.values())
    require(type(payload) is dict)
    expected = {'asset_id'} if operation in ('get','availability_status') else {'asset_id', 'operation_id'} if operation == 'result' else {
        'asset_id', 'store_epoch', 'expected_store_revision', 'expected_revision', 'operation_id', 'fields'}
    require(set(payload) == expected and type(payload['asset_id']) is str and
            re.fullmatch('dev_[0-9a-f]{16}', payload['asset_id']) is not None)
    if operation in ('create', 'update'):
        fields = payload['fields']
        require(type(fields) is dict and bool(fields) and set(fields) <= POLICY_FIELDS)
        for name, value in fields.items():
            if name != 'infrastructure_type':
                require(value is None or type(value) is bool)
            else:
                require(value is None or type(value) is str and value in {
                    'router_gateway','raspberry_pi_server','network_switch','wireless_access_point_mesh_node',
                    'smart_home_hub_bridge','other_infrastructure'})
        for name in ('store_epoch','operation_id'):
            parsed = uuid.UUID(hex=payload[name])
            require(parsed.version == 4 and parsed.hex == payload[name])
        require(type(payload['expected_store_revision']) is int and 1 <= payload['expected_store_revision'] <= 2**53-1)
        require(payload['expected_revision'] is None if operation == 'create' else
            type(payload['expected_revision']) is int and 1 <= payload['expected_revision'] <= 2**53-1)
    elif operation == 'result':
        parsed = uuid.UUID(hex=payload['operation_id'])
        require(parsed.version == 4 and parsed.hex == payload['operation_id'])
    require(len(canonical(payload)) <= 4096)
    return payload


class Client:
    def __init__(self, config, *, observation=False):
        required = {'enabled', 'issuer', 'key_id', 'assertion_key_file', 'client_certificate',
                    'client_key', 'server_ca', 'server_url', 'operator_allowlist', 'request_timeout_seconds'}
        if observation: required.remove('operator_allowlist')
        require(type(config) is dict and set(config) == required and config['enabled'] is True)
        self.config = config
        issuer = uuid.UUID(hex=config['issuer'])
        require(issuer.version == 4 and issuer.hex == config['issuer'])
        if not observation:
            require(type(config['operator_allowlist']) is list and bool(config['operator_allowlist']))
            require(all(type(x) is str and re.fullmatch('[A-Za-z0-9_-]{1,128}', x) for x in config['operator_allowlist']))
        require(type(config['key_id']) is str and re.fullmatch('[A-Za-z0-9_-]{1,64}', config['key_id']))
        require(type(config['request_timeout_seconds']) is int and 1 <= config['request_timeout_seconds'] <= 30)
        url = urlsplit(config['server_url'])
        require(url.scheme == 'https' and url.hostname and url.port and url.path in ('', '/') and
                not url.username and not url.password and not url.query and not url.fragment)
        self.host, self.port = url.hostname, url.port
        self.context = ssl.create_default_context(cafile=str(secret_path(config['server_ca'])))
        self.context.minimum_version = ssl.TLSVersion.TLSv1_2
        self.context.load_cert_chain(str(secret_path(config['client_certificate'])), str(secret_path(config['client_key'])))
        self.key_path = secret_path(config['assertion_key_file'])

    def request(self, operation, payload, actor, context_id, verified_at):
        validate_payload(operation, payload)
        # Queueing or key-file I/O cannot renew a previously verified actor.
        # Logical assertion issuance precedes verification and offloading; the
        # backend also enforces this same exclusive 30-second deadline.
        instant = utc(verified_at)
        require(instant <= datetime.now(timezone.utc) < instant+timedelta(seconds=30))
        key = secret_path(self.key_path).read_bytes()
        require(len(key) == 32)
        require(instant <= datetime.now(timezone.utc) < instant+timedelta(seconds=30))
        path = '/pe7/v1/availability/status' if operation == 'availability_status' else '/pe7/v1/policy/' + operation
        audience = 'hioc.pe7.availability.read' if operation == 'availability_status' else 'hioc.pe7.asset'
        assertion = dict(issuer=self.config['issuer'], audience=audience, key_id=self.config['key_id'],
                         actor_id=actor, context_id=context_id, request_id=uuid.uuid4().hex,
                         issued_at=instant.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                         expires_at=(instant+timedelta(seconds=30)).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                         method='POST', path=path, payload_sha256=sha(payload))
        envelope = dict(schema_version='1.0', assertion=assertion, payload=payload,
                        signature=hmac.new(key, canonical(dict(assertion=assertion, payload=payload)), hashlib.sha256).hexdigest())
        raw = canonical(envelope)
        require(len(raw) <= 8192)
        return self.exchange(path, raw, lambda value:validate_response(value, operation, payload), limit=16384 if operation=='availability_status' else 65536)

    def exchange(self, path, raw, validator, *, limit):
        connection = http.client.HTTPSConnection(self.host, self.port, context=self.context,
                                                timeout=self.config['request_timeout_seconds'])
        try:
            # Exactly one transport attempt. No redirects, retry, offline queue or HA token.
            connection.request('POST', path, raw, {'Content-Type': 'application/json'})
            response = connection.getresponse()
            require(response.status in (200, 201, 401, 403, 409, 422, 429, 503))
            require(response.getheader('Content-Type') == 'application/json')
            body = response.read(limit+1)
            require(len(body) <= limit)
            def pairs(items):
                result = {}
                for name, value in items:
                    require(name not in result)
                    result[name] = value
                return result
            result = json.loads(body.decode('utf-8'), object_pairs_hook=pairs,
                parse_constant=lambda _:require(False))
            return validator(result)
        finally:
            connection.close()


def validate_response(value, operation, payload):
    require(type(value) is dict and value.get('schema_version') == '1.0')
    if operation == 'availability_status':
        return validate_availability_response(value, payload)
    if value.get('result') == 'error':
        require(set(value) == {'schema_version', 'operation_id', 'result', 'error_code', 'commit_state', 'retryable'})
        require(value['error_code'] in {'AUTH_REQUIRED', 'FORBIDDEN', 'TRUST_INVALID', 'ASSERTION_EXPIRED',
            'REPLAY_CONFLICT', 'REVISION_CONFLICT', 'IDENTITY_UNSAFE', 'VALIDATION_FAILED', 'STORE_UNAVAILABLE',
            'UNSUPPORTED_SCHEMA', 'RATE_LIMITED', 'BUSY', 'COMMIT_UNKNOWN'})
        require(value['commit_state'] in ('NOT_APPLIED', 'UNKNOWN') and type(value['retryable']) is bool)
        return value
    require(set(value) == {'schema_version', 'operation_id', 'result', 'commit_state', 'policy', 'receipt'})
    require(value['result'] in (('found', 'not_found') if operation == 'result' else ('read',) if operation == 'get'
                               else ('created', 'updated', 'no_change', 'replayed')))
    require(value['commit_state'] in ('CONFIRMED', 'UNKNOWN') if operation == 'result' else value['commit_state'] == 'CONFIRMED')
    policy = value['policy']
    require(type(policy) is dict and set(policy) == {'asset_id', 'attachment', 'store_epoch', 'store_revision',
        'revision', 'expected_availability', 'infrastructure_device', 'infrastructure_type',
        'effective_expected_availability', 'effective_infrastructure_type', 'applied_policy_revision'})
    require(policy['asset_id'] == payload['asset_id'])
    require(value['operation_id'] == payload.get('operation_id'))
    for name in ('expected_availability', 'infrastructure_device'):
        require(policy[name] is None or type(policy[name]) is bool)
    require(type(policy['effective_expected_availability']) is bool)
    require(policy['attachment'] in ('strong', 'orphan', 'weak', 'conflicted', 'absent'))
    epoch = uuid.UUID(hex=policy['store_epoch'])
    require(epoch.version==4 and epoch.hex==policy['store_epoch'])
    require(type(policy['store_revision']) is int and 1<=policy['store_revision']<=2**53-1)
    for name in ('revision','applied_policy_revision'):
        require(policy[name] is None or type(policy[name]) is int and 1<=policy[name]<=2**53-1)
    allowed_types={'router_gateway','raspberry_pi_server','network_switch','wireless_access_point_mesh_node',
        'smart_home_hub_bridge','other_infrastructure'}
    require(policy['infrastructure_type'] is None or policy['infrastructure_type'] in allowed_types)
    require(policy['effective_expected_availability'] is (policy['expected_availability'] is True))
    require(policy['effective_infrastructure_type']==(policy['infrastructure_type'] if policy['infrastructure_device'] is True else None))
    receipt=value['receipt']
    if receipt is not None:
        require(type(receipt) is dict and set(receipt)=={'issuer_digest','actor_digest','operation_id','request_sha256',
            'expires_at','asset_id','committed_revision','committed_store_revision','outcome'})
        require(receipt['asset_id']==payload['asset_id'] and receipt['operation_id']==payload['operation_id'])
        for name in ('issuer_digest','actor_digest','request_sha256'):
            require(type(receipt[name]) is str and re.fullmatch('[0-9a-f]{64}',receipt[name]))
        require(receipt['outcome'] in ('changed','no_change')); utc(receipt['expires_at'])
        for name in ('committed_revision','committed_store_revision'):
            require(type(receipt[name]) is int and 1<=receipt[name]<=2**53-1)
    require(receipt is None if operation=='get' or value['result']=='not_found' else receipt is not None)
    return value


async def async_setup(hass, config):
    settings = config.get(DOMAIN)
    if type(settings) is dict and set(settings) <= {'operator', 'notifications', 'observations'}:
        operator, observation = settings.get('operator'), settings.get('observations')
        if operator and operator.get('enabled') is True and observation and observation.get('enabled') is True:
            await hass.async_add_executor_job(distinct_observation_credentials, operator, observation['transport'])
        await async_setup_notifications(hass, settings.get('notifications'))
        await async_setup_observations(hass, settings.get('observations'))
        settings = settings.get('operator')
    if settings is None or settings.get('enabled') is not True:
        return True
    import voluptuous as vol
    from homeassistant.components.websocket_api.connection import current_connection
    from homeassistant.core import SupportsResponse
    from homeassistant.exceptions import HomeAssistantError
    try:
        client = await hass.async_add_executor_job(Client, settings)
    except Exception:
        raise HomeAssistantError('HIOC trust configuration unavailable') from None
    for service, operation in SERVICE_ROUTES.items():
        async def handle(call, operation=operation):
            try:
                payload = validate_payload(operation, dict(call.data))
                verified_at = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                actor, context = await verified_actor(hass, call, settings['operator_allowlist'], current_connection)
                return await hass.async_add_executor_job(client.request, operation, payload, actor, context, verified_at)
            except Exception:
                raise HomeAssistantError('HIOC request unavailable or unauthorized') from None
        # Per-operation closed validation is inside the handler before authentication/signing.
        hass.services.async_register(DOMAIN, service, handle,
            schema=vol.Schema(dict, extra=vol.PREVENT_EXTRA), supports_response=SupportsResponse.ONLY)
    return True


EVENT_KEYS = {'schema_version', 'event_id', 'incident_id', 'event_kind', 'severity',
              'occurred_at', 'policy_revision', 'asset_id_digest'}
CASE_KEYS = {'incident_id', 'asset_id_digest', 'episode', 'lifecycle', 'availability_state',
             'suppression_reason', 'severity', 'policy_revision', 'profile_revision', 'detected_at', 'updated_at'}


def closed_json(raw, limit):
    require(type(raw) is str and len(raw.encode('utf-8')) <= limit)
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result)
            result[key] = value
        return result
    def invalid(_):
        raise BridgeError('Invalid public projection')
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=invalid)


def utc(value):
    require(type(value) is str and re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{6}Z', value))
    return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)


def validate_projection(value, now):
    require(type(value) is dict and set(value) == {'schema_version', 'evaluated_at', 'valid_until',
        'status', 'total_case_count', 'omitted_case_count', 'cases'})
    require(value['schema_version'] == '1.0' and value['status'] == 'VALID' and
            utc(value['evaluated_at']) <= now < utc(value['valid_until']))
    require(type(value['cases']) is list and type(value['total_case_count']) is int and
            value['total_case_count'] == len(value['cases']) <= 4096 and
            type(value['omitted_case_count']) is int and value['omitted_case_count'] == 0)
    seen = set()
    for case in value['cases']:
        require(type(case) is dict and set(case) == CASE_KEYS)
        for key in ('incident_id', 'asset_id_digest'):
            require(type(case[key]) is str and re.fullmatch('[0-9a-f]{64}', case[key]))
        require(case['incident_id'] not in seen); seen.add(case['incident_id'])
        require(case['severity'] == 'warning' and case['suppression_reason'] in (None, 'OPERATOR_DISABLED'))
        require(case['lifecycle'] in ('detected', 'confirmed', 'active', 'recovering', 'resolved'))
        require(case['availability_state'] in ('NOT_MONITORED', 'AVAILABLE', 'UNKNOWN', 'STALE', 'DEGRADED', 'OFFLINE', 'RECOVERING'))
        for key in ('episode', 'policy_revision', 'profile_revision'):
            require(type(case[key]) is int and 1 <= case[key] <= 2**53-1)
        require(utc(case['detected_at']) <= utc(case['updated_at']) <= now)
    return value


def validate_event(value):
    require(type(value) is dict and set(value) == EVENT_KEYS and value['schema_version'] == '1.0')
    for key in ('event_id', 'incident_id', 'asset_id_digest'):
        require(type(value[key]) is str and re.fullmatch('[0-9a-f]{64}', value[key]))
    require(value['event_kind'] in ('OUTAGE_STARTED', 'OUTAGE_RECOVERED') and value['severity'] == 'warning')
    require(type(value['policy_revision']) is int and value['policy_revision'] >= 1)
    utc(value['occurred_at'])
    return value


class NotificationReceiver:
    """Durable receiver dedup BEFORE external delivery; uncertainty is never retried."""
    def __init__(self, storage, notify, enabled, clock=lambda: datetime.now(timezone.utc)):
        self.storage, self.notify, self.enabled, self.clock = storage, notify, enabled, clock
        self.lock = asyncio.Lock()
        self.projection = None

    async def accept(self, value):
        validate_event(value)
        require(self.projection is not None)
        projection = validate_projection(self.projection, self.clock())
        require(any(case['incident_id'] == value['incident_id'] for case in projection['cases']))
        require(self.enabled() is True)
        async with self.lock:
            ledger = await self.storage.async_load()
            if ledger is None:
                ledger = {'schema_version':'1.0', 'events':{}}
            require(type(ledger) is dict and set(ledger) == {'schema_version', 'events'} and
                    ledger['schema_version'] == '1.0' and type(ledger['events']) is dict)
            events = ledger['events']
            if value['event_id'] in events:
                require(events[value['event_id']]['sha256'] == sha(value))
                return 'DUPLICATE'
            require(len(events) < 8192)
            events[value['event_id']] = {'sha256':sha(value), 'state':'IN_FLIGHT'}
            await self.storage.async_save(ledger)
            # Crash after this durable write remains uncertain; no automatic resend.
        try:
            await self.notify(value)
            outcome = 'TRANSPORT_ACCEPTED'
        except Exception:
            outcome = 'DELIVERY_UNKNOWN'
        async with self.lock:
            ledger = await self.storage.async_load()
            require(type(ledger) is dict and value['event_id'] in ledger.get('events', {}))
            ledger['events'][value['event_id']]['state'] = outcome
            await self.storage.async_save(ledger)
        return outcome


async def async_setup_notifications(hass, settings):
    if settings is None or settings.get('enabled') is not True:
        return
    require(type(settings) is dict and set(settings) == {'enabled', 'summary_topic', 'event_topic'})
    require(settings['summary_topic'] == 'home/infrastructure/hioc/incidents/pe7/summary' and
            settings['event_topic'] == 'home/infrastructure/hioc/incidents/pe7/transitions')
    from homeassistant.components import mqtt
    from homeassistant.helpers.storage import Store
    async def notify(event):
        await hass.services.async_call('notify', 'mobile_app_pixel_9_pro_xl', {
            'title': 'HIOC Warning: Expected availability',
            'message': 'Qualified outage started' if event['event_kind'] == 'OUTAGE_STARTED' else 'Qualified recovery confirmed',
            'data': {'tag':'hioc_pe7_'+event['incident_id'], 'channel':'HIOC', 'importance':'high'}}, blocking=True)
    receiver = NotificationReceiver(Store(hass, 1, 'hioc_operator.pe7_notification_receipts'), notify,
        lambda: (state := hass.states.get('input_boolean.hioc_incident_notifications')) is not None and state.state == 'on')
    async def receive_summary(message):
        try:
            value = validate_projection(closed_json(message.payload, 16777216), datetime.now(timezone.utc))
            receiver.projection = value
            hass.states.async_set('sensor.hioc_pe7_incident_summary', 'VALID', value)
        except Exception:
            receiver.projection = None
            hass.states.async_set('sensor.hioc_pe7_incident_summary', 'UNAVAILABLE', {})
    async def receive_event(message):
        try:
            await receiver.accept(closed_json(message.payload, 4096))
        except Exception:
            # Invalid/uncertain input causes no notification or private exception output.
            return
    await mqtt.async_subscribe(hass, settings['summary_topic'], receive_summary, qos=1)
    await mqtt.async_subscribe(hass, settings['event_topic'], receive_event, qos=1)


STATUS_RESPONSE_KEYS = {'schema_version','result','asset_id','read_at','status_reason','expected_availability',
    'policy_status','current_policy_revision','applied_policy_revision','policy_binding','evaluation','observations'}
STATUS_REASONS = {'QUALIFIED_POSITIVE','QUALIFIED_NEGATIVE','RECOVERY_PENDING','NEGATIVE_PENDING','ENTITY_SCOPE_ONLY',
    'SOURCE_STALE','SOURCE_MISSING','SOURCE_MISSING_OR_DUPLICATE','COLLECTION_FAILED','COLLECTION_INCOMPLETE',
    'COLLECTION_UNAVAILABLE','SOURCE_CONFLICT','SOURCE_UNKNOWN','INVALID_SOURCE','MISSING_PROFILE','INVALID_PROFILE',
    'UNKNOWN_IDENTITY','OPERATOR_DISABLED','CLOCK_REVERSED','RETIRED_SOURCE_EPOCH','SOURCE_OUT_OF_ORDER'}


def validate_availability_response(value, payload):
    require(type(value) is dict and value.get('schema_version')=='1.0' and len(canonical(value))<=16384)
    if value.get('result')=='error':
        require(set(value)=={'schema_version','result','error_code','retryable'} and value['retryable'] is False and
            value['error_code'] in {'AUTH_REQUIRED','FORBIDDEN','TRUST_INVALID','ASSERTION_EXPIRED','REPLAY_CONFLICT',
                'VALIDATION_FAILED','UNSUPPORTED_SCHEMA','RATE_LIMITED','BUSY','STORE_UNAVAILABLE'})
        return value
    require(set(value)==STATUS_RESPONSE_KEYS and value['asset_id']==payload['asset_id'])
    read=utc(value['read_at'])
    require(value['result'] in ('READ','NOT_EVALUATED','UNAVAILABLE') and
        value['policy_status'] in ('PRESENT','ABSENT','UNAVAILABLE') and value['policy_binding'] in ('CURRENT','PENDING','UNKNOWN'))
    require(value['expected_availability'] is None or type(value['expected_availability']) is bool)
    positive=lambda v:type(v) is int and 1<=v<=2**53-1
    if value['policy_status']=='PRESENT': require(positive(value['current_policy_revision']))
    else: require(value['current_policy_revision'] is None and value['expected_availability'] is None)
    if value['result']!='READ':
        require(value['evaluation'] is None and value['observations'] is None and
            value['applied_policy_revision'] is None and value['policy_binding']=='UNKNOWN')
        if value['result']=='NOT_EVALUATED':
            require(value['status_reason']=='NOT_EVALUATED' and value['policy_status']!='UNAVAILABLE')
        else: require(value['status_reason'] in ('EVALUATION_STORAGE_UNAVAILABLE','POLICY_STORAGE_UNAVAILABLE','POLICY_CHANGED_DURING_READ'))
        return value
    require(value['status_reason']=='SNAPSHOT_READ' and value['policy_status']!='UNAVAILABLE' and positive(value['applied_policy_revision']))
    if value['policy_binding']=='CURRENT': require(value['current_policy_revision']==value['applied_policy_revision'])
    e=value['evaluation']
    require(type(e) is dict and set(e)=={'availability_state','reason_code','evidence_scope','evaluated_at','valid_until','freshness'})
    require(e['availability_state'] in ('NOT_MONITORED','AVAILABLE','UNKNOWN','STALE','DEGRADED','OFFLINE','RECOVERING') and
        e['reason_code'] in STATUS_REASONS and e['evidence_scope'] in ('DEVICE','ENTITY','MIXED','NONE','UNKNOWN') and
        e['freshness'] in ('FRESH','EXPIRED','UNKNOWN'))
    evaluated=utc(e['evaluated_at']); deadline=None if e['valid_until'] is None else utc(e['valid_until'])
    if e['freshness']=='FRESH': require(deadline is not None and evaluated<=read<deadline)
    if e['freshness']=='EXPIRED': require(deadline is not None and read>=deadline)
    rows=value['observations']
    if rows is not None:
        require(type(rows) is list and len(rows)<=16); refs=[]
        for row in rows:
            require(type(row) is dict and set(row)=={'source_ref','scope','collection_status','completeness','freshness','observed_at','valid_until'})
            require(type(row['source_ref']) is str and re.fullmatch('[0-9a-f]{64}',row['source_ref']))
            refs.append(row['source_ref'])
            require(row['scope'] in ('DEVICE','ENTITY','NONE','UNKNOWN') and
                row['collection_status'] in ('SUCCESS','FAILED','UNAVAILABLE','ABSENT','UNKNOWN') and
                row['completeness'] in ('COMPLETE','INCOMPLETE','UNKNOWN') and row['freshness'] in ('FRESH','STALE','ABSENT','UNKNOWN'))
            for k in ('observed_at','valid_until'):
                if row[k] is not None: utc(row[k])
            if row['collection_status']=='ABSENT': require(row['scope']=='NONE' and row['freshness']=='ABSENT' and
                row['completeness']=='UNKNOWN' and row['observed_at'] is None and row['valid_until'] is None)
            if row['freshness'] in ('FRESH','STALE'):
                require(row['collection_status']=='SUCCESS' and row['completeness']=='COMPLETE' and utc(row['observed_at'])<=read)
                require(read<utc(row['valid_until']) if row['freshness']=='FRESH' else read>=utc(row['valid_until']))
        require(refs==sorted(set(refs)))
    return value


class ObservationClient(Client):
    """Distinct service assertion, never an operator actor or Asset mutation."""
    def __init__(self, config):
        super().__init__(config, observation=True)

    def submit(self, observations):
        require(type(observations) is list and len(observations)<=256)
        payload={'observations':observations}; now=datetime.now(timezone.utc)
        key=secret_path(self.key_path).read_bytes(); require(len(key)==32)
        assertion=dict(issuer=self.config['issuer'], audience='hioc.pe7.observation', key_id=self.config['key_id'],
            request_id=uuid.uuid4().hex, issued_at=now.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            expires_at=(now+timedelta(seconds=30)).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            method='POST', path='/pe7/v1/observations', payload_sha256=sha(payload))
        envelope=dict(schema_version='1.0',assertion=assertion,payload=payload,
            signature=hmac.new(key,canonical(dict(assertion=assertion,payload=payload)),hashlib.sha256).hexdigest())
        raw=canonical(envelope); require(len(raw)<=262144)
        def validate(value):
            require(type(value) is dict and set(value)=={'schema_version','result','observation_count'} and
                value['schema_version']=='1.0' and value['result']=='observations_received' and
                type(value['observation_count']) is int and value['observation_count']==len(observations))
            return value
        return self.exchange('/pe7/v1/observations',raw,validate,limit=8192)


def collect_selected_observations(states_get, settings, now):
    """Only explicit members and actual report times; no history, attrs, service or probe."""
    require(set(settings)=={'enabled','transport','source_epoch','profiles','mappings','association','association_sha256','association_deadline'})
    require(settings['enabled'] is True and utc(now)<utc(settings['association_deadline']))
    epoch=uuid.UUID(hex=settings['source_epoch']); require(epoch.version==4 and epoch.hex==settings['source_epoch'])
    association=settings['association']; require(sha(association)==settings['association_sha256'])
    require(type(settings['mappings']) is list and len(settings['mappings'])<=256)
    result=[];seen=set()
    for mapping in settings['mappings']:
        require(type(mapping) is dict and set(mapping)=={'source_id','asset_id','ha_device_id','entity_id','mapping_revision','scope','report_semantics_verified'})
        key,source=mapping['asset_id'],mapping['source_id']
        require(type(key) is str and re.fullmatch('dev_[0-9a-f]{16}',key) and (key,source) not in seen);seen.add((key,source))
        profile=settings['profiles'][key]; definition=profile['source_definitions'][source]
        require(source in profile['enabled_sources'] and definition['kind']=='ha' and
            definition['mapping_revision']==mapping['mapping_revision'] and definition['mapping_sha256']==sha(mapping))
        require(type(definition['max_age_seconds']) is int and definition['max_age_seconds']>0 and
            mapping['scope'] in ('DEVICE','ENTITY') and type(mapping['report_semantics_verified']) is bool)
        matches=[row for row in association['associations'] if row['hioc_device_id']==key]
        safe=(len(matches)==1 and matches[0]['status']=='ASSOCIATED_STRONG_MAC' and matches[0]['association_basis']=='unique_mac' and
            matches[0]['ha_device_id']==mapping['ha_device_id'] and
            mapping['entity_id'] in {member['entity_id'] for member in matches[0].get('entities',[])})
        status,kind,reason='UNAVAILABLE','UNKNOWN','ASSOCIATION_UNSAFE'
        observed=utc(now); source_sha=sha(['missing',epoch.hex,source,key])
        if safe:
            try:
                state=states_get(mapping['entity_id']);status='SUCCESS';reason='ENTITY_MISSING'
                if state is not None:
                    require(mapping['report_semantics_verified'] is True)
                    observed=state.last_reported
                    require(observed.tzinfo is not None and observed<=utc(now))
                    meaning=state.state;require(type(meaning) is str and len(meaning)<=128)
                    source_sha=sha([epoch.hex,source,key,mapping['mapping_revision'],observed.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),meaning])
                    if meaning in ('unknown','unavailable'):
                        reason='ENTITY_STATE_NOT_PHYSICAL_OUTAGE'
                    elif meaning in definition['positive_meanings']:
                        kind,reason='POSITIVE','REVIEWED_POSITIVE'
                    elif meaning in definition['negative_meanings'] and definition['physical_device_authority'] is True and mapping['scope']=='DEVICE':
                        kind,reason='NEGATIVE','REVIEWED_PHYSICAL_NEGATIVE'
                    else: reason='ENTITY_STATE_NOT_PHYSICAL_OUTAGE'
            except BridgeError:
                observed,status,kind,reason=utc(now),'UNAVAILABLE','UNKNOWN','REPORT_TIME_UNAVAILABLE'
            except Exception:
                observed,status,kind,reason=utc(now),'FAILED','UNKNOWN','COLLECTION_FAILED'
        deadline=min(utc(settings['association_deadline']),observed+timedelta(seconds=definition['max_age_seconds']))
        observed_text=observed.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        result.append(dict(schema_version='1.0',source_id=source,source_kind='ha',asset_id=key,device_id=key,
            source_epoch=epoch.hex,sample_id=sha([epoch.hex,source,observed_text,source_sha]),observed_at=observed_text,
            collected_at=now,collection_status=status,completeness='COMPLETE',evidence_kind=kind,scope=mapping['scope'],
            authority_ref=sha([source,definition['mapping_revision'],definition['mapping_sha256']]),
            valid_until=deadline.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),reason_code=reason,source_sha256=source_sha))
    return result


async def async_setup_observations(hass, settings):
    if settings is None or settings.get('enabled') is not True: return
    client=await hass.async_add_executor_job(ObservationClient,settings['transport'])
    async def collect_once():
        # Retained callable only; no timer, subscription, automatic first run or actor impersonation.
        now=datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        rows=collect_selected_observations(hass.states.get,settings,now)
        return await hass.async_add_executor_job(client.submit,rows)
    hass.data.setdefault(DOMAIN,{})['collect_observations_once']=collect_once


def distinct_observation_credentials(operator, observation):
    from cryptography import x509
    from cryptography.hazmat.primitives import serialization
    def public(config):
        cert=x509.load_pem_x509_certificate(secret_path(config['client_certificate']).read_bytes())
        return cert.public_key().public_bytes(serialization.Encoding.DER,serialization.PublicFormat.SubjectPublicKeyInfo)
    require(public(operator) != public(observation))
    require(secret_path(operator['assertion_key_file']).read_bytes() != secret_path(observation['assertion_key_file']).read_bytes())
