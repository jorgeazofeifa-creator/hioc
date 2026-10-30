#!/usr/bin/env python3
"""One anchored controlled restoration. Public CLI performs read-only admission only.

No new restoration algorithm: the sealed successor-configured controller performs
rollback. Native execution requires a separately authorized, pinned operator entry.
An existing intent (including a partial one) is never adopted or retried.
"""
from __future__ import annotations
import contextlib
import copy
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
PREPARED_SHA = '144a3a86acc85f3385b395b83ce33a91422868064a62efd954499e84902a7412'
SOURCE_ANCESTOR = '8e7b668e055226c55d3bc4d9a473431bd9b3e6b6'
JOURNAL_SHA = 'ddd309c9db6e2773e619971773da834aedf42458b860bade941d91e97be57a11'
CLAIM_SHA = '23476ae2f940b5730f129e1a854234179d8618f9a82571e7caae02b062200129'
TX = 'backups/pe73-full-inventory-delivery-v1'
CLAIM = TX + '/prepared-recovery-claim.json'
INTENT = TX + '/controlled-restoration-intent.json'
ACTIONS = ('ATTACH', 'DRAIN', 'ROLLBACK', 'AUTHORIZE_RELEASE', 'RESTORE_SCHEDULER', 'RELEASE')
AUTHORITY = 'HIOC PE-7.3: Implement and Qualify Controlled Restoration'
ORIGINAL_CRON_SHA = '3f56b904fc1dd40ccbfa3fdd61cb910c4d215e9ac28a9bf2dcdf3721c73b62a9'
REDUCED_CRON_SHA = '443485cfb47920db8d6263e5266eb9f68811e81c06390a983a7006aac581b930'


def require(value, code):
    if not value:
        raise ValueError(code)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _dependencies():
    path = ROOT / 'tools/pe73_successor_prepared_recovery.py'
    require(not path.is_symlink() and path.is_file(), 'RESTORATION_DEPENDENCY_TYPE')
    raw = path.read_bytes()
    require(sha(raw) == PREPARED_SHA, 'RESTORATION_DEPENDENCY_IDENTITY')
    p = types.ModuleType('pe73_restoration_sealed_prepared')
    p.__file__ = str(path)
    exec(compile(raw, str(path), 'exec'), p.__dict__)
    return p, p._adapter()


def _source(p):
    result = p._source()  # Fixed root, main, origin, clean tree and accepted ancestry.
    check = subprocess.run(['/usr/bin/git', '--no-optional-locks', '--no-replace-objects',
        'merge-base', '--is-ancestor', SOURCE_ANCESTOR, result['commit']], cwd=ROOT,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20,
        env={'PATH': '/usr/bin:/bin', 'HOME': '/home/jazofv1', 'LANG': 'C.UTF-8',
             'LC_ALL': 'C.UTF-8', 'GIT_OPTIONAL_LOCKS': '0'})
    require(check.returncode == 0, 'RESTORATION_SOURCE_ANCESTRY')
    return result


def _names():
    return {'journal.json', 'prepared-recovery-claim.json', 'window-crontab-original'} | {
        prefix + str(i) for prefix in ('backup-', 'stage-') for i in range(13)}


def _claim(fs, d, p):
    before = fs.snapshot(CLAIM, 0o600)
    raw = fs.read(CLAIM)
    require(sha(raw) == CLAIM_SHA, 'RESTORATION_CLAIM_ANCHOR')
    v = d.parsed(raw)
    require(set(v) == {'version', 'authority', 'journal_anchor', 'pid', 'boot_id',
        'session', 'nonce', 'actions', 'admission_reference', 'authorization_sha256'},
        'RESTORATION_CLAIM_SCHEMA')
    require(type(v['version']) is int and v['version'] == 1 and
        v['authority'] == p.AUTHORITY and v['journal_anchor'] == p.JOURNAL_SHA and
        v['actions'] == list(p.CONTINUATION) and type(v['pid']) is int and v['pid'] > 0 and
        type(v['boot_id']) is str and d.AUTH.fullmatch(v['boot_id']) and
        all(type(v[k]) is str and re.fullmatch('[0-9a-f]{32}', v[k]) for k in ('session', 'nonce')) and
        type(v['authorization_sha256']) is str and d.DIGEST.fullmatch(v['authorization_sha256']) and
        v['admission_reference'] == 'PE73_' + v['authorization_sha256'], 'RESTORATION_CLAIM_SCHEMA')
    require(fs.snapshot(CLAIM, 0o600) == before, 'RESTORATION_CLAIM_DRIFT')
    return before


# Shared implementation of the original restoration recorder; exact dependencies verified.
_Recorder = _dependencies()[1]._Recorder


def _history(adapter, h, source, fs):
    # Historical journal validity is distinct from its obsolete live inode set.
    snap = fs.snapshot(adapter.HISTORICAL_TX + '/journal.json', 0o600)
    require(snap['exists'], 'RESTORATION_HISTORY_MISSING')
    value = h.WindowController(fs, source, h.d.NativeConsumers())._journal()
    require(value['state'] == 'COMMITTED' and value['pending'] is None and
            value.get('window', {}).get('phase') == 'RELEASED', 'RESTORATION_HISTORY_PHASE')
    require(fs.snapshot(adapter.HISTORICAL_TX + '/journal.json', 0o600) == snap,
            'RESTORATION_HISTORY_DRIFT')
    return snap


def _binding():
    p, adapter = _dependencies()
    source = _source(p)
    h, _ = adapter.load(successor=False)
    h.NativeOps()  # Original native host/Linux/real and effective UID/GID checks.
    fs = h.d.NativeFS()
    history = _history(adapter, h, h.d.source_gate(), fs)
    w, manifest = adapter.load()
    original = fs.read(TX + '/window-crontab-original')
    inventory = {line: 'EXCLUDE' if line in w.d.CRON else 'PRESERVE'
        for line in original.decode('utf-8', 'strict').splitlines()
        if line.strip() and not line.lstrip().startswith('#')}
    require(len(inventory) == 12 and list(inventory.values()).count('EXCLUDE') == 3,
            'RESTORATION_SCHEDULER_INVENTORY')
    c = w.MaintenanceCoordinator.native(original, inventory)
    require(type(c.provider.ops) is w.NativeOps, 'RESTORATION_NATIVE_OPS_REQUIRED')
    c.controller.fs = adapter.GuardedFS(c.controller.fs, w, manifest, history)
    recorder = _Recorder(c.provider.ops)
    recorder.install(w, c)
    return w, manifest, c, p, source, recorder


def _buffers(w, c):
    d, fs = w.d, c.controller.fs
    require(set(d.PRIOR) == set(d.ORDER) and len(d.PRIOR) == 13 and
            d.TX == TX and d.RELEASE == '20f7f4c64fd32865f006ecfb2135ae6bbcada16c',
            'RESTORATION_SUCCESSOR_CONFIGURATION_REQUIRED')
    d.check_sources(c.source_reader())
    v = c.controller._journal()
    for i, target in enumerate(d.ORDER):
        require(fs.read(TX + '/stage-' + str(i)) == c.controller.source[target], 'RESTORATION_STAGE_DRIFT')
        require(sha(fs.read(TX + '/backup-' + str(i))) ==
                v['baseline'][target]['sha256'] == d.PRIOR[target][0], 'RESTORATION_BACKUP_DRIFT')
    return v


def _temporaries(w, fs):
    for target in w.d.ORDER:
        path = str(Path(target).parent / ('.pe73-delivery-' + Path(target).name)).replace('\\', '/')
        require(not fs.snapshot(path)['exists'], 'RESTORATION_PENDING_PUBLICATION_TEMPORARY')


def _admit(w, c, p):
    d, fs = w.d, c.controller.fs
    names, identity = p._entries(fs, d)
    require(names == _names(), 'RESTORATION_UNEXPECTED_ARTIFACT_OR_PRIOR_ATTEMPT')
    require(fs.snapshot('backups/.pe73-delivery.lock', 0o600)['exists'], 'RESTORATION_MUTEX_MISSING')
    claim = _claim(fs, d, p)
    raw = fs.read(TX + '/journal.json')
    require(sha(raw) == JOURNAL_SHA, 'RESTORATION_JOURNAL_ANCHOR')
    value = _buffers(w, c)
    require(value['state'] == 'COMMITTING' and value['pending'] is None and
            set(value['installed']) == set(d.ORDER[:5]) and not value['restored'] and
            value['rollback_authorization'] is None and
            value['window']['phase'] == 'INSTALLATION_UNCERTAIN' and
            value['window']['operator'] == 'UID1000_jazofv1', 'RESTORATION_INITIAL_PHASE')
    require(sha(c.provider.original) == ORIGINAL_CRON_SHA and
            sha(c.provider.reduced) == REDUCED_CRON_SHA, 'RESTORATION_SCHEDULER_BINDING')
    c.provider._cron()
    context = c.context('ATTACH')
    p._record_guard(w, c, 'restoration._admit', lambda: require(
        context['process_observation']['inspection_complete'] and
        not context['process_observation']['known_active'], 'KNOWN_CONSUMERS_NOT_DRAINED'))
    require(c.controller.inspect()['live_state_established'], 'RESTORATION_RUNTIME_DRIFT')
    _temporaries(w, fs)
    fs.guard()
    require(fs.read(TX + '/journal.json') == raw and fs.snapshot(CLAIM, 0o600) == claim and
            p._entries(fs, d) == (names, identity), 'RESTORATION_ADMISSION_DRIFT')
    buffers = {TX + '/' + prefix + str(i): fs.snapshot(TX + '/' + prefix + str(i), 0o600)
               for prefix in ('backup-', 'stage-') for i in range(13)}
    buffers[TX + '/window-crontab-original'] = fs.snapshot(TX + '/window-crontab-original', 0o600)
    buffers['backups/.pe73-delivery.lock'] = fs.snapshot('backups/.pe73-delivery.lock', 0o600)
    return {'claim': claim, 'transaction': identity, 'journal_sha256': sha(raw),
            'context': context, 'buffers': buffers}


def inspect_restoration():
    """No mutex, admission, intent creation, scheduler mutation or runtime write."""
    w, manifest, c, p, source, recorder = _binding()
    proof = _admit(w, c, p)
    require(_source(p) == source, 'RESTORATION_SOURCE_DRIFT')
    return {'RESULT': 'PASS_READ_ONLY_CONTROLLED_RESTORATION_READINESS', 'source': source,
        'journal_sha256': proof['journal_sha256'], 'claim_sha256': CLAIM_SHA,
        'state': 'COMMITTING', 'pending': None, 'window': 'INSTALLATION_UNCERTAIN',
        'installed': 5, 'restored': 0, 'backups_verified': 13, 'stages_verified': 13,
        'runtime_snapshots_verified': 13, 'transaction_entries': 29,
        'sequence': list(ACTIONS), 'native_execution_authorized': False,
        'manual_launch_control': 'PROCEDURAL_ONLY', 'universal_exclusion': False,
        'production_mutated': False, 'PE73_STATUS': 'IN_PROGRESS',
        'PE74_STATUS': 'NOT_AUTHORIZED', 'STOP_REQUIRED': True}


class _AttemptFS:
    """One immutable intent, created inside the original admitted ATTACH mutex."""
    def __init__(self, base, w, c, p, source, proof, material):
        self.base, self.w, self.c, self.p = base, w, c, p
        self.source, self.proof, self.material = source, proof, material
        self.intent = None
        self.intent_raw = None

    def __getattr__(self, name):
        return getattr(self.base, name)

    def guard(self):
        self.base.guard()
        names, identity = self.p._entries(self.base, self.w.d)
        require(identity == self.proof['transaction'], 'RESTORATION_TRANSACTION_DRIFT')
        require(names == _names() | ({'controlled-restoration-intent.json'} if self.intent else set()),
                'RESTORATION_UNEXPECTED_ARTIFACT_OR_PRIOR_ATTEMPT')
        require(self.base.snapshot(CLAIM, 0o600) == self.proof['claim'] and
                sha(self.base.read(CLAIM)) == CLAIM_SHA, 'RESTORATION_CLAIM_DRIFT')
        for path, snapshot in self.proof['buffers'].items():
            require(self.base.snapshot(path, 0o600) == snapshot, 'RESTORATION_BUFFER_IDENTITY_DRIFT')
        if self.intent is not None:
            require(self.base.snapshot(INTENT, 0o600) == self.intent and
                    self.base.read(INTENT) == self.intent_raw, 'RESTORATION_INTENT_DRIFT')
        require(_source(self.p) == self.source, 'RESTORATION_SOURCE_DRIFT')
        _temporaries(self.w, self.base)

    @contextlib.contextmanager
    def mutex(self):
        with self.base.mutex():
            self.guard()
            if self.intent is None:
                ops = self.c.provider.ops
                ops.live_gate()
                a = getattr(ops, '_admission', None)
                require(type(a) is self.w._NativeAdmission and a.ops is ops and
                    a.coordinator is self.c and a.action == 'ATTACH' and a.pid == os.getpid(),
                    'RESTORATION_ATTACH_ADMISSION_REQUIRED')
                proof = _admit(self.w, self.c, self.p)
                require(proof['claim'] == self.proof['claim'] and
                        proof['transaction'] == self.proof['transaction'] and
                        proof['buffers'] == self.proof['buffers'], 'RESTORATION_ADMISSION_DRIFT')
                self.intent_raw = self.w.d.canonical(dict(self.material,
                    admission_reference=a.reference, authorization_sha256=a.authorization_sha256))
                self.base.write_new(INTENT, self.intent_raw)
                self.intent = self.base.snapshot(INTENT, 0o600)
            self.guard()
            yield
            self.guard()

    def _mutation(self):
        require(self.intent is not None, 'RESTORATION_INTENT_REQUIRED')
        self.c.provider.ops.live_gate()
        self.guard()
        _buffers(self.w, self.c)

    def journal(self, value):
        self._mutation()
        self.base.journal(value)

    def publish(self, *args):
        self._mutation()
        return self.base.publish(*args)

    def write_new(self, *args, **kwargs):
        raise ValueError('RESTORATION_EXTRA_PRIVATE_WRITE_FORBIDDEN')

    def remove_installed(self, *args):
        raise ValueError('RESTORATION_REMOVAL_FORBIDDEN')


def _restored(w, c):
    value = _buffers(w, c)
    d, fs = w.d, c.controller.fs
    require(value['state'] == 'ROLLED_BACK' and value['pending'] is None and
            set(value['installed']) == set(value['restored']) == set(d.ORDER[:5]),
            'RESTORATION_NOT_TERMINAL')
    for target in d.ORDER:
        now = fs.snapshot(target, d.MODES[target])
        expected = value['restored'].get(target, value['baseline'][target])
        require(now == expected and now['sha256'] == d.PRIOR[target][0], 'RESTORATION_BASELINE_NOT_VERIFIED')
        if target != d.ORDER[4]:
            require(now == value['baseline'][target], 'RESTORATION_PRESERVED_IDENTITY_DRIFT')
    require(c.controller.inspect()['live_state_established'], 'RESTORATION_RUNTIME_DRIFT')
    fs.guard()
    return value


class _Sequence:
    """Fixed recovery orchestration; all mutation algorithms and grants are sealed."""
    def __init__(self, w, c, p, source, recorder):
        self.w, self.c, self.p, self.source, self.recorder = w, c, p, source, recorder
        proof = _admit(w, c, p)
        ops = c.provider.ops
        require(getattr(ops, '_admission', None) is None, 'RESTORATION_ADMISSION_ALREADY_ACTIVE')
        self.pid, self.boot, self.session = os.getpid(), ops.boot_id, c.provider.session
        self.expires, self.deadline = ops.now() + 3600, time.monotonic() + 3600
        self.index, self.stopped, self.expected = 0, False, JOURNAL_SHA
        self.material = {'version': 1, 'authority': AUTHORITY, 'journal_anchor': JOURNAL_SHA,
            'claim_sha256': CLAIM_SHA, 'claim_snapshot': proof['claim'], 'source': source,
            'actions': list(ACTIONS), 'session': self.session, 'boot_id': self.boot,
            'pid': self.pid, 'nonce': uuid.uuid4().hex}
        self.scope = {k: proof['context'][k] for k in ('release', 'manifest_sha256',
            'controller_sha256', 'original_sha256', 'reduced_sha256', 'inventory_sha256', 'approved_jobs')}
        c.controller.fs = _AttemptFS(c.controller.fs, w, c, p, source, proof, self.material)

    def perform_next(self):
        require(not self.stopped and self.index < len(ACTIONS), 'RESTORATION_SEQUENCE_STOPPED')
        action = ACTIONS[self.index]
        self.recorder.action = action
        w, c, d, ops = self.w, self.c, self.w.d, self.c.provider.ops
        try:
            require(os.getpid() == self.pid and self.boot == ops.boot_id and self.session == c.provider.session
                and ops.now() < self.expires and time.monotonic() < self.deadline,
                'RESTORATION_FRESH_SESSION_REQUIRED')
            c.controller.fs.guard()
            require(sha(c.controller.fs.read(TX + '/journal.json')) == self.expected,
                    'RESTORATION_JOURNAL_DRIFT')
            value = _buffers(w, c)
            require(c.controller.inspect()['live_state_established'], 'RESTORATION_RUNTIME_DRIFT')
            if self.index >= 3:
                _restored(w, c)  # Before any release authority or scheduler mutation.
            c.provider._cron(original=action == 'RELEASE')
            context = c.context(action)
            require({k: context[k] for k in self.scope} == self.scope, 'RESTORATION_SCOPE_DRIFT')
            authorization = {'action': action, 'context_sha256': d.sha(d.canonical(context)),
                'reference': 'RESTORE_' + sha(d.canonical({'intent': self.material, 'action': action,
                    'ordinal': self.index, 'nonce': uuid.uuid4().hex})),
                'operator': 'UID1000_jazofv1', 'expires_at': min(self.expires, ops.now() + 300),
                'exclusive_responsibility': True, 'risks_acknowledged': list(w.RISKS)}
            require(getattr(ops, '_admission', None) is None, 'RESTORATION_ADMISSION_ALREADY_ACTIVE')
            admission = w._NativeAdmission(ops, c, action, authorization)
            admission.monotonic_deadline = min(admission.monotonic_deadline, self.deadline)
            ops._admission = admission
            try:
                result = c.execute(action, authorization)
            finally:
                ops._admission = None  # Authority only; never recovery, cron restoration or release.
            value = c.controller._journal()
            expected = [('COMMITTING', 'INSTALLATION_UNCERTAIN'), ('COMMITTING', 'INSTALLATION_UNCERTAIN'),
                ('ROLLED_BACK', 'RESTORATION_VERIFIED'), ('ROLLED_BACK', 'RELEASE_AUTHORIZED'),
                ('ROLLED_BACK', 'SCHEDULER_RESTORED'), ('ROLLED_BACK', 'RELEASED')][self.index]
            require((value['state'], value['window']['phase']) == expected and value['pending'] is None,
                    'RESTORATION_OPERATION_UNCERTAIN')
            if action == 'ROLLBACK':
                require(result == {'state': 'ROLLED_BACK', 'restored_replacements': 5,
                    'removed_new_files': 0, 'original_inode_or_ctime_restored': False}, 'RESTORATION_ROLLBACK_RESULT')
            else:
                require(result['journal_sha256'] == sha(d.canonical(value)), 'RESTORATION_RESULT_JOURNAL')
            if self.index >= 2:
                _restored(w, c)
            c.provider._cron(original=self.index >= 4)
            c.controller.fs.guard()
            self.expected = sha(c.controller.fs.read(TX + '/journal.json'))
            self.index += 1
            return action
        except BaseException:
            self.stopped = True
            raise


def _safe(error):
    code = getattr(error, 'code', None)
    if code is None and type(error) is ValueError:
        code = str(error)
    return code if type(code) is str and re.fullmatch('[A-Z][A-Z0-9_]{0,127}', code) else 'RESTORATION_STOPPED_OR_UNCERTAIN'


def _failure(c, w, recorder, error, action, attempted):
    journal, secondary, scheduler = None, None, {'state': 'UNKNOWN', 'sha256': None}
    if c is not None:
        try:
            value = c.controller._journal()
            journal = {'state': value['state'], 'pending': value['pending'],
                'window': value.get('window', {}).get('phase'), 'restored_entries': len(value['restored'])}
        except BaseException as fault:
            secondary = _safe(fault)
        try:
            raw = c.provider.ops.scheduler()
            scheduler = {'state': 'ORIGINAL' if raw == c.provider.original else
                'REDUCED' if raw == c.provider.reduced else 'UNEXPECTED', 'sha256': sha(raw)}
        except BaseException:
            pass
    return {'RESULT': 'FAIL_STOP_CONTROLLED_RESTORATION', 'failed_action': action,
        'primary_failure': _safe(error), 'inspection': journal, 'inspection_failure': secondary,
        'scheduler_observation_after_failure': scheduler, 'mutation_attempted': attempted,
        'process_guard': getattr(error, 'process_guard', None) or (recorder.receipt(w) if recorder else None),
        'claim_and_intent_must_be_retained': True, 'automatic_retry': False,
        'automatic_rollback': False, 'automatic_scheduler_restoration': False,
        'automatic_release': False, 'manual_caller_restriction': 'MAINTAIN_UNTIL_EXPLICIT_VERIFIED_RELEASE',
        'PE73_STATUS': 'IN_PROGRESS', 'PE74_STATUS': 'NOT_AUTHORIZED', 'STOP_REQUIRED': True}


def run_controlled_restoration():
    """Future separately authorized zero-argument entry. Not exposed by the CLI."""
    c = w = recorder = None
    action, attempted = 'READ_ONLY_ADMISSION', False
    try:
        w, manifest, c, p, source, recorder = _binding()
        sequence = _Sequence(w, c, p, source, recorder)
        for action in ACTIONS:
            attempted = True  # Uncertain intent creation is a mutation attempt too.
            require(sequence.perform_next() == action, 'RESTORATION_ORDER')
        action = 'FINAL_READ_ONLY_VERIFICATION'
        value = _restored(w, c)
        require(value['window']['phase'] == 'RELEASED' and
            c.provider.ops.scheduler() == c.provider.original, 'RESTORATION_FINAL_RELEASE')
        return {'RESULT': 'PASS_CONTROLLED_RESTORATION', 'source': source, 'state': 'ROLLED_BACK',
            'pending': None, 'window': 'RELEASED', 'baseline_payloads_verified': 13,
            'preserved_runtime_identities': 12, 'original_inode_or_ctime_restored': False,
            'claim_retained': True, 'intent_retained': True, 'universal_exclusion': False,
            'manual_launch_control': 'PROCEDURAL_ONLY', 'automatic_recovery': False,
            'PE73_STATUS': 'IN_PROGRESS', 'PE74_STATUS': 'NOT_AUTHORIZED', 'STOP_REQUIRED': True}
    except BaseException as error:
        return _failure(c, w, recorder, error, action, attempted)


if __name__ == '__main__':
    import sys
    try:
        require(sys.argv[1:] == ['inspect-restoration'], 'READ_ONLY_RESTORATION_INSPECTION_ONLY')
        receipt = inspect_restoration()
        status = 0
    except BaseException as error:
        receipt = {'RESULT': 'FAIL_STOP_READ_ONLY_RESTORATION_READINESS', 'failure_code': _safe(error),
            'process_guard': getattr(error, 'process_guard', None),
            'production_mutated': False, 'native_execution_authorized': False, 'STOP_REQUIRED': True}
        status = 1
    print(json.dumps(receipt, sort_keys=True), flush=True)
    raise SystemExit(status)
