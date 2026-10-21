"""Offline PE-6.4 acceptance evidence; never imported by the runtime.

Capture the existing protected(pins) callback, not classification. Capture objects
contain PRIVATE path keys and must never be serialized. Only build_report() bytes
are public. No filesystem traversal, classification, locks, network, or writes here.
ReviewedPermission is an EXTERNAL independent-review attestation, not a process
trace or an authorization created by this helper. References must name already
accepted evidence; matching a filename or declaring a producer never suffices.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import json
import re
import stat
from types import MappingProxyType

CATEGORIES = ('code', 'configuration', 'producer_state', 'historical_journals',
              'runtime_root', 'locks', 'schedule', 'user_crontab')
FIELDS = ('st_dev', 'st_ino', 'st_mode', 'st_uid', 'st_gid', 'st_nlink',
          'st_size', 'st_mtime_ns', 'st_ctime_ns')
ROOT = '/home/jazofv1/hioc'
MAX_OBJECTS = 30000
MAX_DIFFERENCES = 64
MAX_REPORT_BYTES = 65536
_HEX = re.compile(r'[0-9a-f]{64}\Z')
_REF = re.compile(r'[A-Z][A-Z0-9_]{7,95}\Z')
_TIME = re.compile(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d{1,6})?Z\Z')
STAGES = frozenset(('NONE', 'AUTHORIZATION', 'PREFLIGHT', 'INPUT_PREFLIGHT',
    'PRE_EVALUATION_MODULE_ORIGINS', 'SINGLE_EVALUATION',
    'POST_EVALUATION_MODULE_ORIGINS', 'FUNCTIONAL_VERIFICATION',
    'AFTER_STATE', 'FINAL_TIME_CHECK'))

class EvidenceError(ValueError):
    def __init__(self): super().__init__('INVALID_EVIDENCE')
class ProtectedInvariantFailure(Exception):
    """Translate a known existing protected-state gate failure without its text."""
class ObservationUnstable(Exception):
    """An integration adapter may translate its existing Uncertain exception."""
def _need(value):
    if not value: raise EvidenceError()
def _json(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=True, allow_nan=False).encode('ascii')
def _sha(value): return hashlib.sha256(value).hexdigest()
def _now(): return datetime.now(timezone.utc).isoformat(timespec='microseconds').replace('+00:00', 'Z')
def _time(value):
    _need(type(value) is str and _TIME.fullmatch(value))
    return datetime.fromisoformat(value.replace('Z', '+00:00'))
def _digest(value):
    _need(type(value) is str and _HEX.fullmatch(value))
    return value

@dataclass(frozen=True)
class _Object:
    fp: tuple | None = None
    sha256: str | None = None
    control: tuple | None = None

@dataclass(frozen=True)
class Capture:
    started_at: str | None
    ended_at: str | None
    completeness: str
    error: str | None
    digest: str | None
    _objects: object = field(repr=False)  # PRIVATE map; never serialize
    protected_failure: bool = False

@dataclass(frozen=True)
class ReviewedPermission:
    before_capture_sha256: str
    after_capture_sha256: str
    artifact_id: str
    difference_sha256: str
    writer_id: str
    authorization_reference: str
    acceptance_reference: str
    pe5_publication: dict | None = None


def _fingerprint(value):
    _need(type(value) in (list, tuple) and len(value) == 9)
    _need(all(type(v) is int and -(2**63) <= v < 2**64 for v in value))
    _need(all(value[i] >= 0 for i in range(7)))
    return tuple(value)

def _flatten(observations):
    _need(type(observations) is dict and set(observations) == set(CATEGORIES))
    out = {}
    def add(category, path, value):
        _need(len(out) < MAX_OBJECTS)
        _need(type(path) is str and 0 < len(path) <= 4096)
        key = (category, path); _need(key not in out)
        if value is None: item = _Object()
        elif type(value) in (tuple, list) and len(value) == 2:
            item = _Object(_fingerprint(value[0]), _digest(value[1]))
        else: item = _Object(_fingerprint(value))
        out[key] = item
    for category in CATEGORIES:
        value = observations[category]
        if category == 'runtime_root': add(category, '@runtime_root', value)
        elif category == 'user_crontab':
            _need(type(value) in (tuple, list) and len(value) == 3)
            _need(type(value[0]) is int and value[0] in (0, 1))
            out[(category, '@user_crontab')] = _Object(control=(value[0], _digest(value[1]), _digest(value[2])))
        else:
            _need(type(value) is dict)
            maps = value.values() if category == 'locks' else (value,)
            for mapping in maps:
                _need(type(mapping) is dict)
                for path, record in mapping.items(): add(category, path, record)
    return MappingProxyType(out)


def capture_protected(observe, *, clock=_now):
    """Call observe ONCE; preserve timestamps/completeness, suppress exception text.

    Supply the existing protected(pins) function through a zero-argument adapter.
    Translate known existing Fail gates to ProtectedInvariantFailure and existing
    Uncertain errors to ObservationUnstable. Preserve their independent outcomes.
    An exception means no complete snapshot, never an empty-success observation.
    This cannot make a non-atomic traversal atomic or recover callback partial data.
    """
    started = ended = None; objects = MappingProxyType({}); digest = None
    completeness = 'INCOMPLETE'; error = 'OBSERVATION_ERROR'; protected_failure = False
    try:
        started = clock(); _time(started)
        observations = observe()
        objects = _flatten(observations); digest = _sha(_json(observations))
        completeness, error = 'COMPLETE', None
    except ProtectedInvariantFailure:
        completeness, error = 'INCOMPLETE', 'PROTECTED_CHECK_FAILED'; protected_failure = True
    except ObservationUnstable: completeness, error = 'UNSTABLE', 'OBSERVATION_UNSTABLE'
    except Exception: pass
    try:
        ended = clock(); _time(ended)
        if started is None or _time(ended) < _time(started):
            completeness, error = 'UNSTABLE', 'CLOCK_INVALID'
    except Exception:
        ended = None; completeness, error = 'INCOMPLETE', 'CLOCK_INVALID'
    # Never return an invalid clock string, including private exception payloads.
    try: _time(started)
    except Exception: started = None
    return Capture(started, ended, completeness, error, digest, objects, protected_failure)


# Exact source-owned artifacts; no blanket 'state is mutable' rule.
# Bases: inventory engine lines51-141; core/events.py:15; compatibility.py:182;
# assets.py:308; manufacturer generator:25; configured_association_store.py:13.
_ARTIFACTS = {}
def _register(relative, identifier, writer, basis):
    _ARTIFACTS[ROOT + '/' + relative] = (identifier, 'INDEPENDENTLY_MUTABLE', writer, basis)
for _name in ('inventory', 'devices', 'services', 'capabilities', 'topology',
              'dependencies', 'summary', 'status', 'enrichment', 'enrichment_status'):
    _register('state/inventory/' + _name + '.json', 'INVENTORY_' + _name.upper(),
              'INVENTORY_ENGINE', 'INVENTORY_ENGINE_STATESTORE')
for _name in ('events', 'latest_event'):
    _register('state/events/' + _name + '.json', 'EVENT_' + _name.upper(),
              'EVENT_BUS', 'CORE_EVENTBUS_WRITES')
_register('state/platform/compatibility.json', 'PLATFORM_COMPATIBILITY',
          'COMPATIBILITY_WRITER', 'COMPATIBILITY_STATUS_WRITER')
for _name in ('assets', 'assets_status'):
    _register('state/inventory/' + _name + '.json', _name.upper(), 'ASSET_STORE', 'ASSET_STORE_WRITES')
for _name in ('manufacturer', 'manufacturer_status'):
    _register('state/inventory/' + _name + '.json', _name.upper(), 'MANUFACTURER_GENERATOR', 'PE3_MANUAL_GENERATOR')
for _name in ('current.json', 'current.durability.json'):
    _register('state/enrichment/service_associations/' + _name,
              'PE5_' + _name.replace('.', '_').upper(), 'PE5_COMPOSER', 'PE5_CONFIRMED_OUTPUT_CONTRACT')
PE5_DIRECTORY = ROOT + '/state/enrichment/service_associations'
_PARENTS = {ROOT: 'RUNTIME_ROOT', ROOT + '/state': 'STATE_ROOT',
    ROOT + '/state/inventory': 'STATE_INVENTORY_DIRECTORY',
    ROOT + '/state/events': 'STATE_EVENTS_DIRECTORY',
    ROOT + '/state/platform': 'STATE_PLATFORM_DIRECTORY',
    ROOT + '/state/enrichment/service_associations': 'PE5_OUTPUT_DIRECTORY'}


_CODE_IDS = {ROOT + '/pi4/lib/hioc/' + name:
             'RUNTIME_' + name.replace('/', '_').replace('.', '_').upper()
             for name in ('__init__.py', 'classification.py', 'classification_caller.py',
                 'classification_contract.py', 'assets.py', 'enrichment.py', 'manufacturer.py',
                 'inventory.py', 'service_association.py', 'configured_association.py',
                 'configured_association_store.py', 'configured_association_schemas.py',
                 'runtime.py', 'core/__init__.py', 'core/logging.py', 'core/schemas.py',
                 'core/state.py', 'core/compatibility.py', 'core/capabilities.py',
                 'core/drivers.py', 'core/monitoring.py')}
_CODE_IDS[ROOT + '/pi4/bin/hioc-classify-metadata.py'] = 'RUNTIME_CLASSIFICATION_CLI'
_PARENTS.update({ROOT + '/config': 'CONFIG_ROOT', ROOT + '/backups': 'BACKUPS_ROOT',
                 ROOT + '/state/enrichment': 'STATE_ENRICHMENT_DIRECTORY'})

_AUTHORITY_REFERENCES = {
    'PE6_VERIFIED_RUNTIME_SET': 'docs/PE6_CLASSIFICATION_IMPLEMENTATION.md:339,456',
    'INVENTORY_ENGINE_STATESTORE': 'pi4/bin/hioc-inventory-engine.py:51;pi4/lib/hioc/core/state.py:25',
    'CORE_EVENTBUS_WRITES': 'pi4/lib/hioc/core/events.py:15',
    'COMPATIBILITY_STATUS_WRITER': 'pi4/lib/hioc/core/compatibility.py:182,276',
    'ASSET_STORE_WRITES': 'pi4/lib/hioc/assets.py:308,382',
    'PE3_MANUAL_GENERATOR': 'docs/PE3_MANUFACTURER_IMPLEMENTATION_DESIGN.md:20;pi4/bin/hioc-generate-manufacturer.py:25',
    'PE5_CONFIRMED_OUTPUT_CONTRACT': 'pi4/lib/hioc/configured_association_store.py:13,336;docs/PE5_LOCAL_SERVICE_ASSOCIATION_IMPLEMENTATION.md:374',
    'RUNTIME_DIRECTORY_BOUNDARY': 'docs/PE6_CLASSIFICATION_IMPLEMENTATION.md:339',
    'PE6_NO_SCHEDULER_MUTATION': 'docs/PE6_CLASSIFICATION_CONTRACT_DESIGN.md:1059',
}

def _authority(key, opaque):
    category, path = key
    if category == 'runtime_root': return 'RUNTIME_ROOT', 'UNRESOLVED', None, 'RUNTIME_DIRECTORY_BOUNDARY'
    if category == 'user_crontab': return 'USER_CRONTAB', 'UNRESOLVED', None, 'PE6_NO_SCHEDULER_MUTATION'
    if category == 'code': return _CODE_IDS.get(path, opaque), 'IMMUTABLE', None, 'PE6_VERIFIED_RUNTIME_SET'
    if category == 'producer_state' and path in _ARTIFACTS: return _ARTIFACTS[path]
    # A known .tmp mechanism is not sufficient proof of a writer or authorization.
    return _PARENTS.get(path, opaque), 'UNRESOLVED', None, 'AUTHORITY_NOT_ESTABLISHED'

def _kind(obj, complete):
    if obj is None: return ('NOT_ENUMERATED' if complete else 'UNKNOWN'), ('ABSENT' if complete else 'UNKNOWN')
    if obj.control is not None: return 'PRESENT', 'CONTROL'
    if obj.fp is None: return 'ABSENT_AT_PROBE', 'ABSENT'
    mode = obj.fp[2]
    kind = 'REGULAR_FILE' if stat.S_ISREG(mode) else 'DIRECTORY' if stat.S_ISDIR(mode) else 'SYMLINK' if stat.S_ISLNK(mode) else 'OTHER'
    return 'PRESENT', kind

def _outcome(value):
    _need(type(value) is dict and set(value) <= {'status', 'stage', 'category'})
    _need(value.get('status') in ('PASS', 'FAIL', 'INCOMPLETE', 'NOT_RUN'))
    stage = value.get('stage', 'NONE'); _need(type(stage) is str)
    result = dict(status=value['status'], stage=stage if stage in STAGES else 'UNKNOWN')
    if 'category' in value:
        result['category'] = value['category'] if value['category'] in ('REQUIRED_CHECK_FAILED', 'PROTECTED_CHECK_FAILED', 'PROTECTED_OBSERVATION_INCOMPLETE') else 'UNSPECIFIED'
    return result


def _validate_capture(capture):
    _need(type(capture) is Capture and type(capture._objects) is MappingProxyType)
    _need(type(capture.protected_failure) is bool)
    _need(capture.completeness in ('COMPLETE', 'INCOMPLETE', 'UNSTABLE'))
    _need(capture.error in (None, 'OBSERVATION_ERROR', 'OBSERVATION_UNSTABLE', 'CLOCK_INVALID', 'PROTECTED_CHECK_FAILED'))
    for value in (capture.started_at, capture.ended_at):
        if value is not None: _time(value)
    if capture.digest is not None: _digest(capture.digest)
    if capture.completeness == 'COMPLETE':
        _need(capture.error is None and capture.digest is not None)
        _need(capture.started_at is not None and capture.ended_at is not None)
        _need(_time(capture.ended_at) >= _time(capture.started_at))
    _need(len(capture._objects) <= MAX_OBJECTS)
    for key, obj in capture._objects.items():
        _need(type(key) is tuple and len(key) == 2 and key[0] in CATEGORIES)
        _need(type(key[1]) is str and 0 < len(key[1]) <= 4096 and type(obj) is _Object)
        if obj.fp is not None: _fingerprint(obj.fp)
        if obj.sha256 is not None: _digest(obj.sha256)
        _need(obj.sha256 is None or obj.fp is not None)
        if obj.control is not None:
            _need(key[0] == 'user_crontab' and obj.fp is None and len(obj.control) == 3)
            _need(type(obj.control[0]) is int and obj.control[0] in (0, 1))
            _digest(obj.control[1]); _digest(obj.control[2])


def _validate_pe5_publication(before, after, permissions):
    """Validate an EXTERNALLY reviewed native-contract attestation, not production.

    The external reviewer must already have established writer authorization and
    schema/canonical/domain/descriptor/revision/stable-pair validation using PE-5
    read_domain()/descriptor() semantics. This helper neither authenticates those
    assertions nor infers a writer from cron, names, timestamps or CONFIRMED alone.
    Retain the external evidence separately; only its digest enters the receipt.
    No historical content digest is manufactured or added to captured observations.
    """
    ids = ('PE5_OUTPUT_DIRECTORY', 'PE5_CURRENT_JSON', 'PE5_CURRENT_DURABILITY_JSON')
    paths = (PE5_DIRECTORY, PE5_DIRECTORY+'/current.json',
             PE5_DIRECTORY+'/current.durability.json')
    keys = {('producer_state', path) for path in paths}
    _need(set(permissions) == set(ids))
    _need(before.completeness == after.completeness == 'COMPLETE')
    changed = {k for k in set(before._objects) | set(after._objects)
               if before._objects.get(k) != after._objects.get(k)}
    _need(changed == keys)  # No hidden extra creation, deletion or other-category delta.
    directory = permissions[ids[0]]
    for identifier in ids:
        item = permissions[identifier]
        _need(item.writer_id == 'PE5_COMPOSER')
        _need(item.authorization_reference == directory.authorization_reference)
        _need(item.acceptance_reference == directory.acceptance_reference)
    evidence = directory.pe5_publication
    fields = {'schema_version', 'validation', 'domain', 'durability_state', 'candidate',
        'transaction_id', 'evaluated_at', 'output_sha256', 'durability_sha256',
        'confirmed_sha256', 'output_source_revision', 'confirmed_source_revision',
        'output_after_fingerprint', 'durability_after_fingerprint'}
    _need(type(evidence) is dict and set(evidence) == fields)
    _need(evidence['schema_version'] == '1.0')
    _need(evidence['validation'] == 'PASS_SCHEMA_CANONICAL_DOMAIN_DESCRIPTOR_DIGEST_REVISION_STABLE_PAIR')
    _need(evidence['domain'] == 'GENERATED_RELATIONSHIP_OUTPUT')
    _need(evidence['durability_state'] == 'CONFIRMED' and evidence['candidate'] is None)
    _need(type(evidence['transaction_id']) is str and
          re.fullmatch(r'dur_[0-9a-f]{32}', evidence['transaction_id']))
    _need(_time(evidence['evaluated_at']) <= _time(after.ended_at))
    _need(_digest(evidence['confirmed_sha256']) == _digest(evidence['output_sha256']))
    revision = evidence['output_source_revision']
    _need(revision is None or type(revision) is int and 1 <= revision <= 9007199254740991)
    _need(type(evidence['confirmed_source_revision']) is type(revision) and
          evidence['confirmed_source_revision'] == revision)
    for i, path in enumerate(paths):
        a, b = before._objects.get(('producer_state', path)), after._objects.get(('producer_state', path))
        _need(a is not None and b is not None and a.fp is not None and b.fp is not None)
        # Stable path/type/security/device; only the documented atomic effects qualify.
        _need(a.fp[0] == b.fp[0] and a.fp[3:6] == b.fp[3:6])
        _need(a.fp[3] == a.fp[4] == 1000)
        if i == 0:
            _need(a.fp[:7] == b.fp[:7] and stat.S_ISDIR(a.fp[2]))
            _need(stat.S_IMODE(a.fp[2]) == 0o700 and a.sha256 is b.sha256 is None)
        else:
            _need(a.fp[1] != b.fp[1])  # This narrow grant covers the observed replacement pattern.
            _need(stat.S_ISREG(a.fp[2]) and a.fp[2] == b.fp[2] and
                  stat.S_IMODE(a.fp[2]) == 0o600 and a.fp[5] == 1)
            maximum = 16777216 if i == 1 else 8192
            _need(0 < a.fp[6] <= maximum and 0 < b.fp[6] <= maximum)
            kind = 'output' if i == 1 else 'durability'
            _need(_fingerprint(evidence[kind+'_after_fingerprint']) == b.fp)
            sha = _digest(evidence[kind+'_sha256'])
            if b.sha256 is not None: _need(b.sha256 == sha)
            _need(permissions[ids[i]].pe5_publication is None)
    return _sha(_json(evidence))


def build_report(before, after, *, primary_outcome, protected_inspection_outcome,
                 reviewed_permissions=(), max_differences=MAX_DIFFERENCES,
                 max_report_bytes=MAX_REPORT_BYTES):
    """Return ONLY bounded public ASCII JSON bytes; never print or persist data.

    Permissions are externally accepted, exact-change review attestations. This
    function checks their bindings and declared writer, NOT production provenance.
    Never supply them from filenames, ordinary service existence, or unreviewed logs.
    Code drift and security-field changes cannot be waived by this interface.
    """
    _validate_capture(before); _validate_capture(after)
    _need(type(max_differences) is int and 1 <= max_differences <= MAX_DIFFERENCES)
    _need(type(max_report_bytes) is int and 2048 <= max_report_bytes <= MAX_REPORT_BYTES)
    primary, inspection = _outcome(primary_outcome), _outcome(protected_inspection_outcome)
    if after.protected_failure:
        inspection = dict(status='FAIL', stage='AFTER_STATE', category='PROTECTED_CHECK_FAILED')
    elif after.completeness != 'COMPLETE' and inspection['status'] != 'FAIL':
        inspection = dict(status='INCOMPLETE', stage='AFTER_STATE', category='PROTECTED_OBSERVATION_INCOMPLETE')
    permissions = {}
    for item in reviewed_permissions:
        _need(type(item) is ReviewedPermission)
        _need(item.before_capture_sha256 == before.digest and item.after_capture_sha256 == after.digest)
        _digest(item.before_capture_sha256); _digest(item.after_capture_sha256); _digest(item.difference_sha256)
        _need(type(item.authorization_reference) is str and _REF.fullmatch(item.authorization_reference))
        _need(type(item.acceptance_reference) is str and _REF.fullmatch(item.acceptance_reference))
        _need(type(item.writer_id) is str and _REF.fullmatch(item.writer_id))
        _need(item.artifact_id not in permissions)
        permissions[item.artifact_id] = item
    publication_sha256 = None
    if 'PE5_OUTPUT_DIRECTORY' in permissions:
        publication_sha256 = _validate_pe5_publication(before, after, permissions)
    else:
        _need(all(item.pe5_publication is None for item in permissions.values()))
    differences = []; prohibited = False; unresolved = False; used = set()
    keys = sorted(set(before._objects) | set(after._objects))
    for ordinal, key in enumerate(keys):
        a, b = before._objects.get(key), after._objects.get(key)
        if a == b: continue
        identifier, mutable, writer, basis = _authority(key, 'OBJECT_%05d' % ordinal)
        pa, ka = _kind(a, before.completeness == 'COMPLETE')
        pb, kb = _kind(b, after.completeness == 'COMPLETE')
        fields = {}
        for i, field in enumerate(FIELDS):
            av = a.fp[i] if a and a.fp else None; bv = b.fp[i] if b and b.fp else None
            if av != bv: fields[field] = dict(before=str(av) if av is not None else None, after=str(bv) if bv is not None else None)
        changes = []
        if pa in ('NOT_ENUMERATED', 'ABSENT_AT_PROBE') and pb == 'PRESENT': changes.append('APPEARED')
        if pa == 'PRESENT' and pb in ('NOT_ENUMERATED', 'ABSENT_AT_PROBE'): changes.append('DISAPPEARED')
        if pa == pb == 'PRESENT' and ka != kb: changes.append('TYPE_CHANGED')
        if a and b and a.fp and b.fp and any(f in fields for f in ('st_dev', 'st_ino')): changes.append('IDENTITY_CHANGED')
        if fields: changes.append('METADATA_CHANGED')
        ah, bh = a.sha256 if a else None, b.sha256 if b else None
        if ah and bh and ah != bh: changes.append('CONTENT_HASH_CHANGED')
        control = {}
        if (a and a.control is not None) or (b and b.control is not None):
            for i, field in enumerate(('return_code', 'stdout_sha256', 'stderr_sha256')):
                av = a.control[i] if a and a.control else None; bv = b.control[i] if b and b.control else None
                if av != bv: control[field] = dict(before=str(av) if av is not None else None, after=str(bv) if bv is not None else None)
            if control: changes.append('CONTROL_CHANGED')
        record = dict(category=key[0], artifact_id=identifier,
            safe_parent_id=_PARENTS.get(key[1].rsplit('/', 1)[0]),
            object_type_before=ka, object_type_after=kb, observation_before=pa, observation_after=pb,
            object_identity_before=dict(device=str(a.fp[0]), inode=str(a.fp[1])) if a and a.fp else None,
            object_identity_after=dict(device=str(b.fp[0]), inode=str(b.fp[1])) if b and b.fp else None,
            change_types=changes, field_differences=fields, control_differences=control,
            content_hash_evidence=dict(before=ah, after=bh, basis='BOUND_READ' if ah or bh else 'NOT_APPLICABLE' if ka in ('DIRECTORY', 'CONTROL', 'ABSENT') and kb in ('DIRECTORY', 'CONTROL', 'ABSENT') else 'NOT_CAPTURED'),
            mutability=mutable, contract_basis=dict(id=basis, source=_AUTHORITY_REFERENCES.get(basis)))
        record['difference_sha256'] = _sha(_json(dict(before_capture=before.digest, after_capture=after.digest, difference=record)))
        decision, decision_basis = ('PROHIBITED', 'IMMUTABLE_RUNTIME_CHANGED') if mutable == 'IMMUTABLE' and 'UNKNOWN' not in (pa, pb) else ('UNATTRIBUTED', 'INCOMPLETE_COMPARISON' if 'UNKNOWN' in (pa, pb) else 'SPECIFIC_WRITER_EVIDENCE_MISSING')
        if identifier in permissions:
            item = permissions[identifier]; used.add(identifier)
            pe5_directory = (key == ('producer_state', PE5_DIRECTORY) and
                             identifier == 'PE5_OUTPUT_DIRECTORY' and publication_sha256 is not None)
            _need(pe5_directory or mutable == 'INDEPENDENTLY_MUTABLE' and item.writer_id == writer)
            _need(item.difference_sha256 == record['difference_sha256'])
            _need(not set(fields) & {'st_mode', 'st_uid', 'st_gid', 'st_nlink'})
            _need(before.completeness == after.completeness == 'COMPLETE')
            decision, decision_basis = 'PERMITTED_CONFIRMED', ('EXTERNAL_PE5_ATOMIC_PUBLICATION_REVIEW'
                if pe5_directory else 'EXTERNAL_INDEPENDENT_REVIEW_ATTESTATION')
            record['review_references'] = dict(authorization=item.authorization_reference, acceptance=item.acceptance_reference)
            if publication_sha256 is not None:
                record['review_references']['pe5_publication_sha256'] = publication_sha256
        record.update(adjudication=decision, adjudication_basis=decision_basis)
        prohibited |= decision == 'PROHIBITED'; unresolved |= decision == 'UNATTRIBUTED'
        differences.append(record)
    _need(used == set(permissions))
    failed = prohibited or primary['status'] == 'FAIL' or inspection['status'] == 'FAIL' or before.protected_failure
    incomplete = before.completeness != 'COMPLETE' or after.completeness != 'COMPLETE'
    incomplete |= bool(before.ended_at and after.started_at and _time(after.started_at) < _time(before.ended_at))
    insufficient = incomplete or unresolved or primary['status'] != 'PASS' or inspection['status'] != 'PASS'
    result = 'FAIL' if failed else 'INSUFFICIENT_EVIDENCE' if insufficient else 'PASS'
    report = dict(schema_version='1.0', result=result, categories=list(CATEGORIES),
        primary_outcome=primary, protected_inspection_outcome=inspection,
        capture_intervals={k:dict(start=c.started_at, end=c.ended_at, completeness=c.completeness, error=c.error, protected_gate_failed=c.protected_failure, sha256=c.digest)
                           for k, c in (('before', before), ('after', after))},
        difference_count_complete=not incomplete,
        observation_intervals_ordered=not bool(before.ended_at and after.started_at and _time(after.started_at) < _time(before.ended_at)),
        changed_object_count=len(differences), reported_object_count=min(len(differences), max_differences),
        omitted_object_count=0, differences_truncated=False,
        object_differences=differences[:max_differences],
        limitations=['ENDPOINT_OBSERVATIONS_NOT_EVENT_HISTORY', 'NO_ACTOR_INFERENCE_FROM_FILENAME',
                     'PERMISSIONS_ARE_EXTERNAL_REVIEW_ATTESTATIONS'])
    while True:
        n = len(report['object_differences']); omitted = len(differences) - n
        report.update(reported_object_count=n, omitted_object_count=omitted, differences_truncated=bool(omitted))
        if omitted and report['result'] != 'FAIL': report['result'] = 'INSUFFICIENT_EVIDENCE'
        raw = _json(report) + b'\n'
        if len(raw) <= max_report_bytes: return raw
        _need(bool(report['object_differences']))
        report['object_differences'].pop()
