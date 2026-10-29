"""PE-7 signed federation protocol. Trust configuration is explicit and disabled by default."""
from __future__ import annotations
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import hmac
import threading
from .availability_contract import (
    PolicyError, asset_id, canonical, digest, error_response, hex_digest, identifier,
    keys, require, strict_json, timestamp, uuid4,
)

ROUTES = {f'/pe7/v1/policy/{name}': name for name in ('get', 'create', 'update', 'result')}
STATUS_ROUTE = '/pe7/v1/availability/status'
ROUTES[STATUS_ROUTE] = 'availability_status'
POPULATION_SCOPES = dict(get='eligible_or_existing', create='eligible_inventory',
                         update='existing_assets', result='existing_assets',
                         availability_status='existing_assets')


ASSERTION_KEYS = ('issuer', 'audience', 'key_id', 'actor_id', 'context_id', 'request_id',
                  'issued_at', 'expires_at', 'method', 'path', 'payload_sha256')


@dataclass(frozen=True, repr=False)
class IssuerTrust:
    issuer: str
    key_id: str
    key: bytes = field(repr=False)
    client_spki_sha256: str
    # Exact IDs or explicit amendment-bound population grants; never wildcards.
    actors: dict
    enabled: bool = False

    def validate(self):
        uuid4(self.issuer)
        identifier(self.key_id)
        require(len(self.key_id) <= 64 and type(self.key) is bytes and len(self.key) == 32, 'TRUST_INVALID')
        hex_digest(self.client_spki_sha256)
        require(type(self.actors) is dict and len(self.actors) <= 1024, 'TRUST_INVALID')
        for actor, operations in self.actors.items():
            identifier(actor)
            require(type(operations) is dict and set(operations) <= set(ROUTES.values()), 'TRUST_INVALID')
            for operation, allowed in operations.items():
                if type(allowed) is dict:
                    require(set(allowed) == {'scope', 'amendment', 'acceptance_reference'} and
                            allowed['scope'] == POPULATION_SCOPES[operation] and
                            allowed['amendment'] == 'PE73_FULL_INVENTORY_ASSET_AUTHORIZATION_V1', 'TRUST_INVALID')
                    reference = allowed['acceptance_reference']
                    require(reference is None or type(reference) is str and 1 <= len(reference) <= 128, 'TRUST_INVALID')
                    if reference is not None: identifier(reference)
                    if self.enabled:
                        require(reference is not None, 'FORBIDDEN')
                    continue
                require(type(allowed) in (set, frozenset) and 1 <= len(allowed) <= 4096, 'TRUST_INVALID')
                for key in allowed:
                    asset_id(key)
        return self


class Protocol:
    """Independent backend trust/ACL, bounded nonces and mutation quotas.

    TLS peer identity is supplied only by the verified TLS server socket, never a
    header or JSON field. A trust lookup is repeated under the Asset writer guard.
    """
    def __init__(self, service, trust_lookup, clock=lambda: datetime.now(timezone.utc), *, nonce_capacity=4096, status_reader=None):
        self.service, self.trust_lookup, self.clock = service, trust_lookup, clock
        self.nonce_capacity = nonce_capacity
        self.nonces = {}
        self.attempts = deque()
        self.lock = threading.Lock()
        self.last_clock = None
        self.status_reader = status_reader
        self.read_attempts = deque()

    def _trust(self, assertion, peer, operation, key, *, locked=False, verify_population=True):
        trust = self.trust_lookup(assertion['issuer'], assertion['key_id'])
        require(isinstance(trust, IssuerTrust), 'TRUST_INVALID')
        trust.validate()
        require(trust.enabled is True and hmac.compare_digest(trust.client_spki_sha256, peer), 'TRUST_INVALID')
        require(trust.issuer == assertion['issuer'] and trust.key_id == assertion['key_id'], 'TRUST_INVALID')
        allowed = trust.actors.get(assertion['actor_id'], {}).get(operation, ())
        if type(allowed) is dict:
            if verify_population:
                require(self.service.authorize_population(operation, key, allowed['scope'], locked=locked), 'FORBIDDEN')
        else:
            require(key in allowed, 'FORBIDDEN')
        return trust

    def handle(self, path, raw, peer_spki_sha256, *, method='POST', content_type='application/json',
               content_encoding=None, origin=None):
        try:
            require(path in ROUTES and method == 'POST' and content_type == 'application/json' and
                    content_encoding is None and origin is None)
            hex_digest(peer_spki_sha256)
            envelope = strict_json(raw)
            keys(envelope, ('schema_version', 'assertion', 'payload', 'signature'))
            require(envelope['schema_version'] == '1.0')
            assertion, payload = envelope['assertion'], envelope['payload']
            keys(assertion, ASSERTION_KEYS)
            audience = 'hioc.pe7.availability.read' if path == STATUS_ROUTE else 'hioc.pe7.asset'
            require(assertion['audience'] == audience and assertion['method'] == method and assertion['path'] == path)
            uuid4(assertion['issuer'])
            uuid4(assertion['request_id'])
            for name in ('key_id', 'actor_id', 'context_id'):
                identifier(assertion[name])
            require(len(assertion['key_id']) <= 64)
            hex_digest(assertion['payload_sha256'])
            hex_digest(envelope['signature'])
            require(hmac.compare_digest(assertion['payload_sha256'], digest(payload)))
            require(type(payload) is dict)
            operation = ROUTES[path]
            if operation in ('get', 'availability_status'):
                keys(payload, ('asset_id',))
            elif operation == 'result':
                keys(payload, ('operation_id', 'asset_id'))
                uuid4(payload['operation_id'])
            else:
                keys(payload, ('asset_id', 'store_epoch', 'expected_store_revision', 'expected_revision', 'operation_id', 'fields'))
            key = asset_id(payload['asset_id'])
            trust = self._trust(assertion, peer_spki_sha256, operation, key, verify_population=False)
            expected = hmac.new(trust.key, canonical(dict(assertion=assertion, payload=payload)), hashlib.sha256).hexdigest()
            require(hmac.compare_digest(expected, envelope['signature']), 'TRUST_INVALID')
            issued, expiry = timestamp(assertion['issued_at']), timestamp(assertion['expires_at'])
            now = self.clock()
            require(isinstance(now, datetime) and now.tzinfo is not None, 'ASSERTION_EXPIRED')
            require(issued <= now < expiry and 0 < (expiry-issued).total_seconds() <= 30, 'ASSERTION_EXPIRED')
            current = self._trust(assertion, peer_spki_sha256, operation, key)
            require(hmac.compare_digest(current.key, trust.key), 'FORBIDDEN')
            with self.lock:
                require(self.last_clock is None or now >= self.last_clock, 'ASSERTION_EXPIRED')
                self.last_clock = now
                self.nonces = {key: end for key, end in self.nonces.items() if now < end}
                nonce = (assertion['issuer'], assertion['request_id'])
                require(nonce not in self.nonces, 'REPLAY_CONFLICT')
                require(len(self.nonces) < self.nonce_capacity, 'BUSY')
                self.nonces[nonce] = expiry
                if operation == 'availability_status':
                    while self.read_attempts and (now-self.read_attempts[0][0]).total_seconds() >= 60:
                        self.read_attempts.popleft()
                    actor = (assertion['issuer'], assertion['actor_id'])
                    require(sum(identity == actor for _, identity in self.read_attempts) < 30 and
                            len(self.read_attempts) < 300, 'RATE_LIMITED')
                    self.read_attempts.append((now, actor))
                if operation in ('create', 'update'):
                    while self.attempts and (now-self.attempts[0][0]).total_seconds() >= 60:
                        self.attempts.popleft()
                    actor = (assertion['issuer'], assertion['actor_id'])
                    count = sum(identity == actor for _, identity in self.attempts)
                    require(count < 10 and len(self.attempts) < 100, 'RATE_LIMITED')
                    self.attempts.append((now, actor))
            def reauthorize(*, locked=False):
                current = self._trust(assertion, peer_spki_sha256, operation, key, locked=locked)
                instant = self.clock()
                return (isinstance(instant, datetime) and instant.tzinfo is not None and
                        now <= instant < expiry and hmac.compare_digest(current.key, trust.key))
            if operation == 'availability_status':
                from .availability import validate_status
                require(self.status_reader is not None, 'STORE_UNAVAILABLE')
                require(reauthorize(), 'FORBIDDEN')
                return validate_status(self.status_reader.read(key))
            if operation == 'get':
                require(reauthorize(), 'FORBIDDEN')
                return self.service.get_policy(key)
            if operation == 'result':
                require(reauthorize(), 'FORBIDDEN')
                return self.service.operation_result(key, payload['operation_id'], assertion['issuer'], assertion['actor_id'])
            return self.service.mutate_policy(operation, payload, assertion['issuer'], assertion['actor_id'], lambda: reauthorize(locked=True))
        except PolicyError as error:
            if path == STATUS_ROUTE:
                return dict(schema_version='1.0', result='error', error_code=error.code, retryable=False)
            return error_response(error)
        except Exception:
            if path == STATUS_ROUTE:
                return dict(schema_version='1.0', result='error', error_code='STORE_UNAVAILABLE', retryable=False)
            # No private paths, user IDs, parser text, secrets or field values escape.
            return error_response(PolicyError('STORE_UNAVAILABLE'))


def sign(assertion, payload, key):
    require(type(key) is bytes and len(key) == 32, 'TRUST_INVALID')
    return dict(schema_version='1.0', assertion=assertion, payload=payload,
                signature=hmac.new(key, canonical(dict(assertion=assertion, payload=payload)), hashlib.sha256).hexdigest())


def peer_public_key_sha256(certificate_der):
    """Pin the certificate public key, not its subject or caller-supplied identity.

    Cryptography is an explicit dependency. Missing support fails closed; there is
    no certificate-hash or plaintext fallback.
    """
    from cryptography import x509
    from cryptography.hazmat.primitives import serialization
    certificate = x509.load_der_x509_certificate(certificate_der)
    spki = certificate.public_key().public_bytes(serialization.Encoding.DER,
                                                 serialization.PublicFormat.SubjectPublicKeyInfo)
    return hashlib.sha256(spki).hexdigest()


@dataclass(frozen=True, repr=False)
class ObservationTrust:
    issuer: str
    key_id: str
    key: bytes = field(repr=False)
    client_spki_sha256: str
    sources: dict  # Exact Asset ID -> allowed source-ID set, independently provisioned.
    enabled: bool = False


class ObservationProtocol:
    """Separate service role; no actor impersonation or AssetService reference."""
    def __init__(self, sink, trust_lookup, profiles, attachment, clock=lambda: datetime.now(timezone.utc)):
        self.sink, self.trust_lookup, self.profiles, self.attachment, self.clock = sink, trust_lookup, profiles, attachment, clock
        self.nonces, self.lock, self.last_clock = {}, threading.Lock(), None

    def handle(self, path, raw, peer, *, method='POST', content_type='application/json', content_encoding=None, origin=None):
        from .availability import validate_observation, validate_profile
        try:
            require(path == '/pe7/v1/observations' and method == 'POST' and content_type == 'application/json' and
                    content_encoding is None and origin is None)
            envelope = strict_json(raw, limit=262144, depth=5)
            keys(envelope, ('schema_version', 'assertion', 'payload', 'signature'))
            require(envelope['schema_version'] == '1.0')
            assertion, payload = envelope['assertion'], envelope['payload']
            keys(assertion, tuple(name for name in ASSERTION_KEYS if name not in ('actor_id', 'context_id')))
            require(assertion['audience'] == 'hioc.pe7.observation' and assertion['method'] == method and assertion['path'] == path)
            uuid4(assertion['issuer']); uuid4(assertion['request_id']); identifier(assertion['key_id'])
            trust = self.trust_lookup(assertion['issuer'], assertion['key_id'])
            require(isinstance(trust, ObservationTrust) and trust.enabled is True and
                    trust.issuer == assertion['issuer'] and trust.key_id == assertion['key_id'] and
                    type(trust.key) is bytes and len(trust.key) == 32 and
                    hmac.compare_digest(trust.client_spki_sha256, hex_digest(peer)), 'TRUST_INVALID')
            hex_digest(envelope['signature']); hex_digest(assertion['payload_sha256'])
            require(hmac.compare_digest(assertion['payload_sha256'], digest(payload)))
            expected = hmac.new(trust.key, canonical(dict(assertion=assertion, payload=payload)), hashlib.sha256).hexdigest()
            require(hmac.compare_digest(expected, envelope['signature']), 'TRUST_INVALID')
            now, issued, expiry = self.clock(), timestamp(assertion['issued_at']), timestamp(assertion['expires_at'])
            require(issued <= now < expiry and 0 < (expiry-issued).total_seconds() <= 30, 'ASSERTION_EXPIRED')
            keys(payload, ('observations',))
            require(type(payload['observations']) is list and len(payload['observations']) <= 256)
            seen = set()
            for row in payload['observations']:
                validate_observation(row)
                key, source = row['asset_id'], row['source_id']
                require((key, source) not in seen); seen.add((key, source))
                require(source in trust.sources.get(key, ()), 'FORBIDDEN')
                profile = validate_profile(self.profiles(key))
                require(source in profile['enabled_sources'] and self.attachment(key) == 'strong', 'IDENTITY_UNSAFE')
                definition = profile['source_definitions'][source]
                require(row['device_id'] == key and row['source_kind'] == definition['kind'] and
                        row['authority_ref'] == digest([source, definition['mapping_revision'], definition['mapping_sha256']]))
                require(timestamp(row['observed_at']) <= timestamp(row['collected_at']) <= now)
                if row['evidence_kind'] == 'NEGATIVE':
                    require(definition['physical_device_authority'] is True and row['scope'] == 'DEVICE')
            with self.lock:
                require(self.last_clock is None or now >= self.last_clock, 'ASSERTION_EXPIRED')
                self.last_clock = now
                self.nonces = {key:end for key,end in self.nonces.items() if now < end}
                nonce = (assertion['issuer'], assertion['request_id'])
                require(nonce not in self.nonces, 'REPLAY_CONFLICT')
                require(len(self.nonces) < 4096, 'BUSY')
                self.nonces[nonce] = expiry
            self.sink.commit(payload['observations'])
            return dict(schema_version='1.0', result='observations_received', observation_count=len(payload['observations']))
        except PolicyError as error:
            return error_response(error)
        except Exception:
            return error_response(PolicyError('STORE_UNAVAILABLE'))
