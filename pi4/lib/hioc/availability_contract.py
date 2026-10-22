"""Closed PE-7 primitives. No runtime configuration, I/O or production defaults."""
from __future__ import annotations

import hashlib
import json
import re
import uuid
from datetime import datetime, timezone

POLICY_FIELDS = ('expected_availability', 'infrastructure_device', 'infrastructure_type')
INFRASTRUCTURE_TYPES = (
    'router_gateway', 'raspberry_pi_server', 'network_switch',
    'wireless_access_point_mesh_node', 'smart_home_hub_bridge', 'other_infrastructure',
)
HEX = re.compile(r'^[0-9a-f]{64}$')
IDENTIFIER = re.compile(r'^[A-Za-z0-9_-]{1,128}$')
ASSET_ID = re.compile(r'^dev_[0-9a-f]{16}$')
UTC = re.compile(r'^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{6}Z$')


class PolicyError(ValueError):
    """Only the fixed code crosses an external boundary; never exception text."""
    def __init__(self, code='VALIDATION_FAILED', *, uncertain=False):
        self.code = code
        self.uncertain = uncertain
        super().__init__(code)


def require(ok, code='VALIDATION_FAILED'):
    if not ok:
        raise PolicyError(code)


def keys(value, expected):
    require(type(value) is dict and set(value) == set(expected))
    return value


def integer(value, minimum=1):
    require(type(value) is int and minimum <= value <= 2**53-1)
    return value


def identifier(value):
    require(type(value) is str and IDENTIFIER.fullmatch(value) is not None)
    return value


def asset_id(value):
    require(type(value) is str and ASSET_ID.fullmatch(value) is not None)
    return value


def hex_digest(value):
    require(type(value) is str and HEX.fullmatch(value) is not None)
    return value


def uuid4(value):
    require(type(value) is str and re.fullmatch('[0-9a-f]{32}', value) is not None)
    parsed = uuid.UUID(hex=value)
    require(parsed.version == 4 and parsed.variant == uuid.RFC_4122)
    return value


def timestamp(value):
    require(type(value) is str and UTC.fullmatch(value) is not None)
    try:
        return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)
    except ValueError:
        raise PolicyError() from None


def time_text(value):
    require(isinstance(value, datetime) and value.tzinfo is not None)
    return value.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=True, allow_nan=False).encode('ascii')


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def strict_json(raw, *, limit=8192, depth=4):
    require(type(raw) is bytes and len(raw) <= limit)
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result)
            result[key] = value
        return result
    def nonfinite(_):
        raise PolicyError()
    try:
        value = json.loads(raw.decode('utf-8', errors='strict'), object_pairs_hook=pairs,
                           parse_constant=nonfinite)
    except (UnicodeError, ValueError, RecursionError):
        raise PolicyError() from None
    def walk(item, level):
        require(level <= depth)
        if type(item) is dict:
            for val in item.values():
                walk(val, level + 1)
        elif type(item) is list:
            for val in item:
                walk(val, level + 1)
    walk(value, 0)
    return value


def policy_fields(value):
    require(type(value) is dict and bool(value) and set(value) <= set(POLICY_FIELDS))
    for name, val in value.items():
        if name == 'infrastructure_type':
            require(val is None or type(val) is str and val in INFRASTRUCTURE_TYPES)
        else:
            require(val is None or type(val) is bool)
    return value


RECEIPT_KEYS = (
    'issuer_digest', 'actor_digest', 'operation_id', 'request_sha256', 'expires_at',
    'asset_id', 'committed_revision', 'committed_store_revision', 'outcome',
)


def validate_receipt(value):
    keys(value, RECEIPT_KEYS)
    for name in ('issuer_digest', 'actor_digest', 'request_sha256'):
        hex_digest(value[name])
    uuid4(value['operation_id'])
    timestamp(value['expires_at'])
    asset_id(value['asset_id'])
    integer(value['committed_revision'])
    integer(value['committed_store_revision'])
    require(value['outcome'] in ('changed', 'no_change'))
    return value


def error_response(error):
    return dict(schema_version='1.0', operation_id=None, result='error',
                error_code=error.code, commit_state='UNKNOWN' if error.uncertain else 'NOT_APPLIED',
                retryable=False)
