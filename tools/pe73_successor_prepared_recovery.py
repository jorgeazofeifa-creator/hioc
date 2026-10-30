#!/usr/bin/env python3
"""One anchored successor PREPARED/no-window recovery; CLI assessment is read-only."""
from __future__ import annotations
import contextlib
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time
import types
import uuid

ROOT = Path(__file__).resolve().parents[1]
ADAPTER_SHA = 'cb6d84c2c4b2181fc1af6e03fee3685a0d364146f528466483b6b20751dcc394'
ADAPTER_COMMIT = 'cb7eef345fba9abd271b5265950c4a7132513a69'
JOURNAL_SHA = 'd79f96f0838f2e4f10db611d2ac27cef09991c40175985bb879c184228ae84b3'
TX = 'backups/pe73-full-inventory-delivery-v1'
CLAIM = TX + '/prepared-recovery-claim.json'
CONTINUATION = ('PRESERVE', 'EXCLUDE', 'DRAIN', 'ESTABLISH', 'COMMIT',
                'AUTHORIZE_RELEASE', 'RESTORE_SCHEDULER', 'RELEASE')
AUTHORITY = 'HIOC PE-7.3: Recover the interrupted successor delivery from PREPARED'


def require(value, code):
    if not value:
        raise ValueError(code)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _adapter():
    path = ROOT / 'tools/pe73_successor_delivery.py'
    require(not path.is_symlink() and path.is_file(), 'ADAPTER_SOURCE_TYPE')
    raw = path.read_bytes()
    require(sha(raw) == ADAPTER_SHA, 'ADAPTER_SOURCE_IDENTITY')
    module = types.ModuleType('pe73_prepared_recovery_adapter')
    module.__file__ = str(path)
    exec(compile(raw, str(path), 'exec'), module.__dict__)
    return module


def _source():
    def git(*args):
        result = subprocess.run(['/usr/bin/git', '--no-optional-locks', '--no-replace-objects', *args],
            cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20,
            env={'PATH': '/usr/bin:/bin', 'HOME': '/home/jazofv1', 'LANG': 'C.UTF-8',
                 'LC_ALL': 'C.UTF-8', 'GIT_OPTIONAL_LOCKS': '0'})
        require(result.returncode == 0, 'RECOVERY_SOURCE_CHECK_FAILED')
        return result.stdout.strip()
    require(str(ROOT) == '/home/jazofv1/hioc-release-source' and ROOT.resolve() == ROOT,
            'RECOVERY_SOURCE_ROOT')
    require(git('rev-parse', '--show-toplevel').decode() == str(ROOT), 'RECOVERY_SOURCE_ROOT')
    require(git('branch', '--show-current') == b'main' and
            git('remote', 'get-url', 'origin') == b'https://github.com/jorgeazofeifa-creator/hioc.git',
            'RECOVERY_SOURCE_PROVENANCE')
    require(not git('status', '--porcelain=v1', '--untracked-files=all') and
            not git('ls-files', '--unmerged'), 'RECOVERY_SOURCE_DIRTY_OR_CONFLICTED')
    git('merge-base', '--is-ancestor', ADAPTER_COMMIT, 'HEAD')
    return {'commit': git('rev-parse', '--verify', 'HEAD^{commit}').decode(),
            'tree': git('rev-parse', 'HEAD^{tree}').decode()}


def _entries(fs, d):
    """Descriptor-bound enumeration; no lock/create/chmod or pathname following."""
    require(fs.transaction_present(), 'RECOVERY_TRANSACTION_MISSING')
    with fs.directory(TX) as fd:
        info = os.fstat(fd)
        fs.security(info, True, 0o700, fd=fd)
        require(info.st_uid == info.st_gid == 1000, 'RECOVERY_TRANSACTION_OWNER')
        return set(os.listdir(fd)), d.anchored(info)


def _base_entries():
    return {'journal.json'} | {'backup-' + str(i) for i in range(13)} | {
        'stage-' + str(i) for i in range(13)}


def _validate(w, coordinator, owned_claim=None):
    """No mutation; all predicates must hold again during execution admission."""
    d, c, p = w.d, coordinator.controller, coordinator.provider
    require(d.TX == TX and d.RELEASE == '20f7f4c64fd32865f006ecfb2135ae6bbcada16c',
            'RECOVERY_SCOPE_MISMATCH')
    require(c.fs.snapshot('backups/.pe73-delivery.lock', 0o600)['exists'],
            'RECOVERY_EXISTING_MUTEX_MISSING')
    names, identity = _entries(c.fs, d)
    allowed = _base_entries() | ({'prepared-recovery-claim.json'} if owned_claim is not None else set())
    require(names == allowed, 'RECOVERY_UNEXPECTED_ARTIFACTS_OR_PRIOR_ATTEMPT')
    if owned_claim is not None:
        require(c.fs.snapshot(CLAIM, 0o600) == owned_claim, 'RECOVERY_CLAIM_DRIFT')
    raw = c.fs.read(TX + '/journal.json')
    require(sha(raw) == JOURNAL_SHA, 'RECOVERY_JOURNAL_ANCHOR_MISMATCH')
    value = c._journal()  # Original strict core/window validation, not a state-label parser.
    require(value['state'] == 'PREPARED' and value['pending'] is None and
            value.get('window') is None and 'maintenance' not in value and
            not value['installed'] and not value['restored'] and
            value['commit_authorization'] is None and value['rollback_authorization'] is None and
            len(value['baseline']) == 13, 'RECOVERY_PHASE_OR_AUTHORITY_MISMATCH')
    p._cron(original=True)
    context = coordinator.context('PRESERVE')
    processes = context['process_observation']
    require(processes['inspection_complete'] and not processes['known_active'],
            'KNOWN_CONSUMERS_NOT_DRAINED')
    require(c.inspect()['live_state_established'], 'RECOVERY_RUNTIME_DRIFT')
    fresh = d.preflight(c.fs, c.source, p)
    require(all(value[k] == fresh[k] for k in fresh), 'RECOVERY_PREFLIGHT_DRIFT')
    for index, target in enumerate(d.ORDER):
        require(c.fs.read(TX + '/stage-' + str(index)) == c.source[target], 'RECOVERY_STAGE_DRIFT')
        backup = c.fs.read(TX + '/backup-' + str(index))
        require(d.sha(backup) == value['baseline'][target]['sha256'] == d.PRIOR[target][0],
                'RECOVERY_BACKUP_DRIFT')
        require(c.fs.snapshot(target, d.MODES[target]) == value['baseline'][target],
                'RECOVERY_RUNTIME_DRIFT')
    c.fs.guard()  # Historical COMMITTED/RELEASED journal identity remains bound.
    require(c.fs.read(TX + '/journal.json') == raw, 'RECOVERY_JOURNAL_DRIFT')
    require(_entries(c.fs, d) == (names, identity), 'RECOVERY_TRANSACTION_DIRECTORY_DRIFT')
    return {'journal_sha256': JOURNAL_SHA, 'transaction_identity': identity,
            'context': context, 'entry_count': len(names)}


def _native_binding():
    source = _source()
    adapter = _adapter()
    historical, _ = adapter.load(successor=False)
    historical.NativeOps()  # Exact native machine/real+effective UID/GID/boot checks.
    history = adapter.predecessor(historical.d.NativeFS(), historical)
    w, m = adapter.load()
    require(adapter.MANIFEST_SHA256 ==
            'e8b37aba46c2bbb56616366420fb4041353fb009ae17d158cf5937aa064ae7a7',
            'RECOVERY_MANIFEST_IDENTITY')
    original = w.NativeOps().scheduler()
    inventory = {line: 'EXCLUDE' if line in w.d.CRON else 'PRESERVE'
                 for line in original.decode('utf-8', 'strict').splitlines()
                 if line.strip() and not line.lstrip().startswith('#')}
    coordinator = w.MaintenanceCoordinator.native(original, inventory)
    require(type(coordinator.provider.ops) is w.NativeOps, 'RECOVERY_NATIVE_OPS_REQUIRED')
    coordinator.controller.fs = adapter.GuardedFS(coordinator.controller.fs, w, m, history)
    proof = _validate(w, coordinator)
    return w, m, coordinator, proof, source


def inspect_prepared_recovery():
    w, m, c, proof, source = _native_binding()
    return {'RESULT': 'PASS_READ_ONLY_ANCHORED_PREPARED_RECOVERY_ASSESSMENT',
            'source': source, 'payload_release': w.d.RELEASE, 'transaction': TX,
            'journal_sha256': JOURNAL_SHA, 'state': 'PREPARED', 'pending': None,
            'window': None, 'backups_verified': 13, 'stages_verified': 13,
            'runtime_baselines_verified': 13, 'transaction_entries': proof['entry_count'],
            'fresh_context_sha256': sha(w.d.canonical(proof['context'])),
            'continuation': list(CONTINUATION), 'manual_launch_control': 'PROCEDURAL_ONLY',
            'universal_exclusion': False, 'native_execution_authorized': False,
            'production_mutated': False, 'PE73_STATUS': 'IN_PROGRESS',
            'PE74_STATUS': 'NOT_AUTHORIZED', 'STOP_REQUIRED': True}


class _RecoveryFS:
    """Create the one-attempt claim only inside admitted PRESERVE's mutex."""
    def __init__(self, base, w, coordinator, material):
        self.base, self.w, self.coordinator = base, w, coordinator
        self.material, self.claim = material, None
    def __getattr__(self, name):
        return getattr(self.base, name)
    def guard(self):
        self.base.guard()
        names, _ = _entries(self.base, self.w.d)
        if self.claim is None:
            require(names == _base_entries(), 'RECOVERY_UNEXPECTED_ARTIFACTS_OR_PRIOR_ATTEMPT')
        else:
            require(self.base.snapshot(CLAIM, 0o600) == self.claim, 'RECOVERY_CLAIM_DRIFT')
            require(_base_entries() | {'prepared-recovery-claim.json'} <= names and
                    names <= _base_entries() | {'prepared-recovery-claim.json', 'window-crontab-original'},
                    'RECOVERY_UNEXPECTED_ARTIFACTS')
    @contextlib.contextmanager
    def mutex(self):
        with self.base.mutex():
            self.guard()
            if self.claim is None:
                p, w = self.coordinator.provider, self.w
                p.ops.live_gate()
                admission = getattr(p.ops, '_admission', None)
                require(type(admission) is w._NativeAdmission and admission.ops is p.ops and
                        admission.coordinator is self.coordinator and admission.action == 'PRESERVE' and
                        admission.pid == os.getpid(), 'RECOVERY_PRESERVE_ADMISSION_REQUIRED')
                _validate(w, self.coordinator)
                material = dict(self.material, admission_reference=admission.reference,
                                authorization_sha256=admission.authorization_sha256)
                self.base.write_new(CLAIM, w.d.canonical(material))
                self.claim = self.base.snapshot(CLAIM, 0o600)
                _validate(w, self.coordinator, owned_claim=self.claim)
            self.guard()
            yield
            self.guard()
    def _mutation_guard(self):
        require(self.claim is not None, 'RECOVERY_CLAIM_REQUIRED')
        self.coordinator.provider.ops.live_gate()
        self.guard()
    def journal(self, value):
        self._mutation_guard()
        self.base.journal(value)
    def write_new(self, path, raw, mode=0o600):
        self._mutation_guard()
        require(path != CLAIM, 'RECOVERY_CLAIM_OVERWRITE_FORBIDDEN')
        self.base.write_new(path, raw, mode)
    def publish(self, *args):
        self._mutation_guard()
        return self.base.publish(*args)


def _begin(w, coordinator):
    """Read-only planning; the original first-operation admission gates every write.

    A distinct anchored entry initializes the original per-operation engine.
    Normal __init__ and the historical EXCLUDED resume remain unchanged.
    """
    c, p, d = coordinator.controller, coordinator.provider, w.d
    _validate(w, coordinator)
    material = {'version': 1, 'authority': AUTHORITY, 'journal_anchor': JOURNAL_SHA,
                'pid': os.getpid(), 'boot_id': p.ops.boot_id, 'session': p.session,
                'nonce': uuid.uuid4().hex, 'actions': list(CONTINUATION)}
    c.fs = _RecoveryFS(c.fs, w, coordinator, material)
    w.DEPLOYMENT_SEQUENCE = CONTINUATION  # Private fixed entry, never operator input.
    engine = object.__new__(w._ApprovedSequence)
    engine.coordinator, engine.resume = coordinator, False
    engine.actions = CONTINUATION
    engine.index, engine.stopped, engine.pid = 0, False, os.getpid()
    engine.boot_id, engine.session = p.ops.boot_id, p.session
    engine.expires_at = p.ops.now() + 3600
    engine.monotonic_deadline = time.monotonic() + 3600
    engine.expected_journal = JOURNAL_SHA
    initial = coordinator.context('PRESERVE')
    engine.scope = {k: initial[k] for k in ('release', 'manifest_sha256', 'controller_sha256',
        'original_sha256', 'reduced_sha256', 'inventory_sha256', 'approved_jobs')}
    engine.reference = d.sha(d.canonical({'authority': AUTHORITY, 'entry': 'EXACT_PREPARED_NO_WINDOW',
        'planned_claim_sha256': d.sha(d.canonical(material)), 'initial_context': initial,
        'scope': engine.scope, 'journal_anchor': JOURNAL_SHA, 'actions': list(CONTINUATION)}))
    return engine


def _safe_code(error):
    value = getattr(error, 'code', None)
    if value is None and type(error) is ValueError:
        value = str(error)
    return value if isinstance(value, str) and re.fullmatch(r'[A-Z][A-Z0-9_]{0,127}', value) else 'RECOVERY_STOPPED_OR_UNCERTAIN'


def run_prepared_recovery():
    """Only for a separately authorized operator execution; no automatic resume."""
    coordinator = None
    attempted, action = False, None
    try:
        w, m, coordinator, proof, source = _native_binding()
        attempted = True  # Even an uncertain private claim write is an attempt.
        engine = _begin(w, coordinator)
        for action in CONTINUATION:
            observed_action, result = engine.perform_next()
            require(observed_action == action, 'RECOVERY_OPERATION_ORDER')
            print(json.dumps({'result': 'PASS_RECOVERY_OPERATION', 'action': action,
                              'journal_sha256': result['journal_sha256']}, sort_keys=True), flush=True)
        c = coordinator.controller
        value = c._journal()
        require(value['state'] == 'COMMITTED' and value['pending'] is None and
                value['window']['phase'] == 'RELEASED', 'RECOVERY_FINAL_PHASE')
        c.verify(value)
        require(coordinator.provider.ops.scheduler() == coordinator.provider.original,
                'RECOVERY_FINAL_SCHEDULER')
        for item in m['artifacts']:
            if item['path'] not in m['changed_paths']:
                require(c.fs.snapshot(item['path'], w.d.MODES[item['path']]) ==
                        value['baseline'][item['path']], 'RECOVERY_PRESERVED_ARTIFACT_DRIFT')
        c.fs.guard()
        return {'RESULT': 'PASS_ANCHORED_PREPARED_SUCCESSOR_RECOVERY', 'source': source,
                'state': 'COMMITTED', 'pending': None, 'window': 'RELEASED',
                'payloads_verified': 13, 'replacement_scope': 3, 'preserved_identities': 10,
                'claim_retained': True, 'manual_launch_control': 'PROCEDURAL_ONLY',
                'universal_exclusion': False, 'automatic_recovery': False,
                'PE73_STATUS': 'IN_PROGRESS', 'PE74_STATUS': 'NOT_AUTHORIZED', 'STOP_REQUIRED': True}
    except BaseException as primary:
        inspection, secondary = None, None
        if coordinator is not None:
            try:
                value = coordinator.controller._journal()
                inspection = {'state': value['state'], 'pending': value['pending'],
                              'window': value.get('window', {}).get('phase')}
            except BaseException as error:
                secondary = _safe_code(error)
        return {'RESULT': 'FAIL_STOP_ANCHORED_PREPARED_SUCCESSOR_RECOVERY',
                'failed_action': action, 'primary_failure': _safe_code(primary),
                'mutation_attempted': attempted, 'inspection': inspection,
                'inspection_failure': secondary, 'claim_must_not_be_removed': True,
                'automatic_retry': False, 'automatic_rollback': False,
                'automatic_scheduler_restoration': False, 'automatic_release': False,
                'manual_caller_restriction': 'MAINTAIN_UNTIL_EXPLICIT_VERIFIED_RELEASE',
                'PE73_STATUS': 'IN_PROGRESS', 'PE74_STATUS': 'NOT_AUTHORIZED', 'STOP_REQUIRED': True}


if __name__ == '__main__':
    import sys
    try:
        require(sys.argv[1:] == ['inspect-prepared-recovery'], 'READ_ONLY_RECOVERY_INSPECTION_ONLY')
        print(json.dumps(inspect_prepared_recovery(), sort_keys=True), flush=True)
        status = 0
    except BaseException as error:
        print(json.dumps({'RESULT': 'FAIL_STOP_READ_ONLY_PREPARED_RECOVERY_ASSESSMENT',
                          'failure_code': _safe_code(error), 'production_mutated': False,
                          'STOP_REQUIRED': True}, sort_keys=True), flush=True)
        status = 1
    raise SystemExit(status)
