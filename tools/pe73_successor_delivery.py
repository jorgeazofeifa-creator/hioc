#!/usr/bin/env python3
"""Pinned PE-7.3 successor configuration of the accepted transaction/provider.

CLI is read-only. Native sequence execution is NOT authorized by this module.
No historical controller/provider bytes or transaction algorithms are rewritten.
"""
from __future__ import annotations
import contextlib
import copy
import functools
import re
import hashlib
import json
from pathlib import Path
import types

MANIFEST_SHA256 = '80b9a9984e6ebb035c4b6c039c52b8612e0c820e11205286db4ef89bf3c536bf'
RELEASE = '20f7f4c64fd32865f006ecfb2135ae6bbcada16c'
HISTORICAL_TX = 'backups/pe73-pi3-delivery-v1'
ROOT = Path(__file__).resolve().parents[1]


def require(value, code):
    if not value:
        raise ValueError(code)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()



class _Recorder:
    """Shared restoration recorder: delegate once; freeze the first rejecting sample.

    Instrumentation is evidence only. Original methods, exceptions, clock calls,
    predicates, native admission and transaction effects remain authoritative.
    """
    def __init__(self, ops):
        self.ops, self.delegate = ops, ops.processes
        self.last = self.failure = self.frozen = self.evaluated_at = None
        self.calls = 0
        self.action = 'READ_ONLY_ADMISSION'

    def __call__(self):
        self.calls += 1
        self.last = self.failure = self.evaluated_at = None
        try:
            result = self.delegate()
            # Snapshot diagnostic fields before another reader could mutate them.
            try:
                self.last = copy.deepcopy(result)
            except BaseException:
                self.failure = 'PROCESS_EVIDENCE_INVALID'
            self.evaluated_at = None  # Discard the scan's own timestamp call.
            return result  # Exact delegate object, never the diagnostic copy.
        except BaseException:
            self.failure = 'PROCESS_INSPECTION_FAILED'
            raise

    def _projection(self, w):
        if self.last is None:
            return None
        v = w.process_evidence(self.last)
        codes = []
        for code in v['limitations']:
            if re.fullmatch(r'(?:UNCLASSIFIED|VANISHED|INCOMPLETE_PROCESS_CLASSIFICATION|PROCESS_IDENTITY_OR_ARGUMENT_DRIFT)_PID_[0-9]{1,10}', code) or code in {
                'CACHED_MODULES_AND_RETAINED_DESCRIPTORS_NOT_UNIVERSALLY_OBSERVABLE',
                'CACHED_MODULES_UNKNOWN'}:
                codes.append(code)
            else:
                codes.append('REDACTED_LIMITATION')
        return {'boot_id_sha256': sha(v['boot_id'].encode()),
            'observed_at': v['observed_at'], 'inspection_complete': v['inspection_complete'],
            'known_active': copy.deepcopy(v['known_active']),
            'limitations': codes, 'universal_exclusion': False}

    def freeze(self, w, stage, mode, expected_boot):
        if self.frozen is not None:
            return
        try:
            v = self._projection(w)
            predicates = {}
            if v is not None:
                if mode in {'PROCESSES', 'CONTEXT'}:
                    predicates['boot_identity'] = self.last['boot_id'] == expected_boot
                if mode != 'CONTEXT':
                    predicates['inspection_completeness'] = v['inspection_complete']
                    predicates['known_consumers_absent'] = not v['known_active']
                if mode in {'PROCESSES', 'CONTEXT'}:
                    predicates['observation_freshness'] = (0 <= self.evaluated_at - v['observed_at'] <= 30
                        if type(self.evaluated_at) is int else None)
            first = next((k for k, value in predicates.items() if value is False), 'UNESTABLISHED')
            self.frozen = {'action': self.action, 'failure_stage': stage,
                'failed_predicate': first, 'predicate_values': predicates,
                'delegations': self.calls, 'actual_guard_observation': v,
                'evaluated_at': self.evaluated_at if mode in {'PROCESSES','CONTEXT'} else None,
                'observation_age_seconds': (self.evaluated_at - v['observed_at']
                    if mode in {'PROCESSES','CONTEXT'} and v is not None and type(self.evaluated_at) is int else None),
                'expected_boot_id_sha256': sha(expected_boot.encode()),
                'inspection_failure': self.failure}
        except BaseException:
            self.frozen = {'action': self.action, 'failure_stage': stage,
                'failed_predicate': 'UNESTABLISHED', 'actual_guard_observation': None,
                'inspection_failure': 'PROCESS_EVIDENCE_INVALID'}

    def guard(self, w, stage, mode, call):
        boot = self.ops.boot_id
        try:
            return call()
        except BaseException as error:
            code = getattr(error, 'code', None)
            if code is None and type(error) is ValueError:
                code = str(error)
            if code in {'KNOWN_CONSUMERS_NOT_DRAINED','PROCESS_EVIDENCE_STALE',
                        'PROCESS_INSPECTION_INCOMPLETE','KNOWN_CONSUMERS_ACTIVE'}:
                self.freeze(w, stage, mode, boot)
            if self.frozen is not None:
                try:
                    error.process_guard = self.receipt(w)
                except BaseException:
                    pass
            raise  # Same exception, no retry, scan, mutation or recovery.

    def install(self, w, coordinator):
        ops = self.ops
        existing = getattr(ops, '_pe73_guard_recorder', None)
        if existing is not None:
            return existing
        ops._pe73_guard_recorder = self
        ops.processes = self
        now = ops.now
        def clock():
            value = now()
            self.evaluated_at = value
            return value  # Record an existing call; never call the clock again.
        ops.now = clock
        def wrap(original, stage, mode):
            @functools.wraps(original)
            def observed(*args, **kwargs):
                if stage in {'MaintenanceCoordinator.execute', 'MaintenanceCoordinator.context'} and args and args[0] in w.ACTIONS | {'PREPARE'}:
                    self.action = args[0]
                return self.guard(w, stage, mode, lambda: original(*args, **kwargs))
            return observed
        provider = coordinator.provider
        provider._processes = wrap(provider._processes, 'WindowConsumers._processes', 'PROCESSES')
        coordinator.context = wrap(coordinator.context, 'MaintenanceCoordinator.context', 'CONTEXT')
        coordinator.execute = wrap(coordinator.execute, 'MaintenanceCoordinator.execute', 'ADMISSION')
        return self

    def receipt(self, w):
        if self.frozen is not None:
            return copy.deepcopy(self.frozen)
        try:
            return {'action': self.action, 'delegations': self.calls,
                'actual_guard_observation': self._projection(w), 'inspection_failure': self.failure,
                'failure_stage': None, 'failed_predicate': None}
        except BaseException:
            return {'action': self.action, 'delegations': self.calls,
                'actual_guard_observation': None, 'inspection_failure': 'PROCESS_EVIDENCE_INVALID',
                'failure_stage': None, 'failed_predicate': None}


def record_guard(w, coordinator, stage, call):
    """Observe an existing admission predicate; absence of a recorder changes nothing."""
    recorder = getattr(coordinator.provider.ops, '_pe73_guard_recorder', None)
    return recorder.guard(w, stage, 'ADMISSION', call) if recorder else call()


def load(root=ROOT, *, successor=True):
    """Load two exact accepted sources, once, into private isolated namespaces.

    The provider's fixed file-loading bootstrap is replaced by the already verified
    core object. All imports, functions and classes after that bootstrap are exact
    original source. This is not an import hook or a configurable source loader.
    """
    raw = (root / 'governance/pe7/pe73-successor-delivery.json').read_bytes()
    require(sha(raw) == MANIFEST_SHA256, 'SUCCESSOR_MANIFEST_IDENTITY')
    m = json.loads(raw)
    require(m['release'] == RELEASE and len(m['artifacts']) == 13 and
            len(m['changed_paths']) == 3, 'SUCCESSOR_SCOPE')
    sources = {}
    for name, key in [('hioc-pe73-pi3-delivery.py', 'controller_sha256'),
                      ('pe73_maintenance_window.py', 'provider_sha256')]:
        path = root / 'tools' / name
        require(not path.is_symlink() and path.is_file(), 'TOOL_SOURCE_TYPE')
        value = path.read_bytes()
        require(sha(value) == m[key], 'TOOL_SOURCE_IDENTITY')
        sources[name] = (path, value)
    path, value = sources['hioc-pe73-pi3-delivery.py']
    d = types.ModuleType('pe73_successor_private_core')
    d.__file__ = str(path)
    exec(compile(value, str(path), 'exec'), d.__dict__)
    path, value = sources['pe73_maintenance_window.py']
    start = value.index(b'PIN = ')
    end = value.index(b'require = d.require\n')
    # Exactly the pinned provider bootstrap, not any function/class, is omitted.
    bootstrap = value[start:end]
    require(b'spec.loader.exec_module(d)' in bootstrap and b'class ' not in bootstrap
            and b'def ' not in bootstrap, 'PROVIDER_BOOTSTRAP_CHANGED')
    w = types.ModuleType('pe73_successor_private_window')
    w.__file__ = str(path)
    w.d = d
    w.PIN = m['controller_sha256']
    exec(compile(value[:start] + b'\n' * bootstrap.count(b'\n') + value[end:], str(path), 'exec'), w.__dict__)
    if successor:
        require([x['path'] for x in m['artifacts']] == [x['path'] for x in d.MANIFEST],
                'SUCCESSOR_MANIFEST_PATHS')
        require(m['prior_release'] == d.RELEASE, 'SUCCESSOR_PRIOR_RELEASE')
        require({x['path']: x['prior_sha256'] for x in m['artifacts']} ==
                {x['path']: x['sha256'] for x in d.MANIFEST}, 'SUCCESSOR_PRIOR_PAYLOAD')
        d.RELEASE = RELEASE
        d.TX = m['transaction']
        d.MANIFEST = [{k: item[k] for k in ('path', 'sha256', 'git_blob')}
                      for item in m['artifacts']]
        d.PRIOR = {x['path']: (x['prior_sha256'], d.MODES[x['path']])
                   for x in m['artifacts']}
        w.BACKUP = d.TX + '/window-crontab-original'
    return w, m


def predecessor(fs, historical):
    """Read-only validation using original strict core AND window validators."""
    d = historical.d
    require(d.TX == HISTORICAL_TX, 'HISTORICAL_NAMESPACE')
    before = fs.snapshot(HISTORICAL_TX + '/journal.json', 0o600)
    require(before['exists'], 'PREDECESSOR_JOURNAL_MISSING')
    source = d.source_gate()
    c = historical.WindowController(fs, source, d.NativeConsumers())
    value = c._journal()
    require(value['state'] == 'COMMITTED' and value['pending'] is None and
            value.get('window', {}).get('phase') == 'RELEASED',
            'PREDECESSOR_NOT_COMMITTED_RELEASED')
    require(c.inspect()['live_state_established'], 'PREDECESSOR_RUNTIME_DRIFT')
    require(fs.snapshot(HISTORICAL_TX + '/journal.json', 0o600) == before,
            'PREDECESSOR_JOURNAL_DRIFT')
    return before


class GuardedFS:
    """Reuse all native descriptor/security/durability methods; only skip no-ops.

    Immutable predecessor journal identity is rechecked at every transaction lock,
    journal write, stage/backup write and live publication. No historical adoption.
    """
    def __init__(self, base, window, manifest, historical_snapshot):
        self.base, self.w, self.m = base, window, manifest
        self.history = historical_snapshot
        self.unchanged = {x['path']: x['sha256'] for x in manifest['artifacts']
                          if x['path'] not in manifest['changed_paths']}

    def __getattr__(self, key):
        return getattr(self.base, key)

    def guard(self):
        require(self.base.snapshot(HISTORICAL_TX + '/journal.json', 0o600) == self.history,
                'PREDECESSOR_JOURNAL_DRIFT')

    @contextlib.contextmanager
    def mutex(self):
        with self.base.mutex():
            self.guard()
            yield
            self.guard()

    def mkdir_tx(self):
        self.guard()
        self.base.mkdir_tx()

    def write_new(self, path, raw, mode=0o600):
        require(path.startswith(self.w.d.TX + '/') and '..' not in Path(path).parts,
                'SUCCESSOR_PRIVATE_WRITE_SCOPE')
        self.guard()
        self.base.write_new(path, raw, mode)

    def journal(self, value):
        self.guard()
        self.base.journal(value)

    def publish(self, path, raw, before, mode):
        self.guard()
        require(path in self.w.d.ORDER and mode == self.w.d.MODES[path],
                'SUCCESSOR_PUBLICATION_SCOPE')
        if path in self.unchanged:
            require(sha(raw) == self.unchanged[path] and
                    self.base.snapshot(path, mode) == before and
                    self.base.read(path, mode) == raw and
                    self.base.snapshot(path, mode) == before, 'UNCHANGED_ARTIFACT_DRIFT')
            return before  # No write/rename/chmod: original inode and times retained.
        require(path in self.m['changed_paths'], 'SUCCESSOR_PUBLICATION_SCOPE')
        return self.base.publish(path, raw, before, mode)

    def remove_installed(self, *args):
        raise ValueError('SUCCESSOR_REMOVAL_FORBIDDEN')  # All thirteen existed before.


def historical_native_coordinator():
    """Fresh read-only binding for a separately authorized normal sequence.

    Never call the historical EXCLUDED-resume shortcut for this new namespace.
    Construction grants no native admission and performs no transaction mutation.
    """
    historical, _ = load(successor=False)
    fs = historical.d.NativeFS()
    historical.NativeOps()  # Existing exact host/Linux/effective UID/GID check.
    history = predecessor(fs, historical)
    w, m = load()
    original = w.NativeOps().scheduler()
    lines = original.decode('utf-8', 'strict').splitlines()
    inventory = {line: 'EXCLUDE' if line in w.d.CRON else 'PRESERVE'
                 for line in lines if line.strip() and not line.lstrip().startswith('#')}
    coordinator = w.MaintenanceCoordinator.native(original, inventory)
    coordinator.controller.fs = GuardedFS(coordinator.controller.fs, w, m, history)
    require(not coordinator.controller.fs.transaction_present(),
            'SUCCESSOR_TRANSACTION_REQUIRES_SEPARATE_RECOVERY')
    _Recorder(coordinator.provider.ops).install(w, coordinator)
    context = coordinator.context('PREPARE')
    processes = w.process_evidence(coordinator.provider.ops.processes())
    record_guard(w, coordinator, 'native_coordinator', lambda: (
        require(processes['inspection_complete'], 'PROCESS_INSPECTION_INCOMPLETE'),
        require(not processes['known_active'], 'KNOWN_CONSUMERS_ACTIVE')))
    coordinator.controller.fs.guard()
    return w, m, coordinator, context


def native_coordinator():
    """Current-baseline admission; historical native entry remains audit-only."""
    import importlib.util
    import subprocess
    path=ROOT/'tools/pe73_verified_baseline.py'
    result=subprocess.run(['/usr/bin/git','--no-optional-locks','--no-replace-objects','show',
        'HEAD:tools/pe73_verified_baseline.py'],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=20,
        env={'PATH':'/usr/bin:/bin','HOME':'/home/jazofv1','LANG':'C.UTF-8'})
    require(result.returncode==0 and not path.is_symlink() and path.read_bytes()==result.stdout,'CURRENT_TOOLING_IDENTITY')
    spec=importlib.util.spec_from_file_location('pe73_current_baseline_operations',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module.native_coordinator()


def native_assessment():
    """Only inspection: no mutex/create, scheduler write, admission or execution."""
    w, m, coordinator, context = native_coordinator()
    return {'RESULT': 'PASS_READ_ONLY_SUCCESSOR_DELIVERY_ASSESSMENT',
            'release': RELEASE, 'manifest_sha256': MANIFEST_SHA256,
            'context_sha256': sha(w.d.canonical(context)),
            'baseline_sha256': context['baseline_sha256'],
            'transaction_id': context['transaction_id'], 'payload_count': 13,
            'live_replacement_count': 3, 'unchanged_identity_count': 10,
            'manual_launch_control': 'PROCEDURAL_ONLY', 'universal_exclusion': False,
            'native_execution_authorized': False, 'production_mutated': False,
            'PE73_STATUS': 'IN_PROGRESS', 'PE74_STATUS': 'NOT_AUTHORIZED',
            'STOP_REQUIRED': True}


if __name__ == '__main__':
    import sys
    code = 1
    try:
        require(sys.argv[1:] == ['inspect'], 'READ_ONLY_INSPECT_ONLY')
        print(json.dumps(native_assessment(), sort_keys=True))
        code = 0
    except Exception as error:
        print(json.dumps({'RESULT': 'FAIL_STOP',
                          'failure_code': error.code if hasattr(error, 'code') else
                          str(error) if type(error) is ValueError else 'READ_ONLY_ASSESSMENT_FAILED',
                          'process_guard': getattr(error, 'process_guard', None),
                          'production_mutated': False, 'STOP_REQUIRED': True}, sort_keys=True))
    raise SystemExit(code)
