"""Finite PE-7.3 HA delivery preparation; no import-time I/O or activation.

Reuses the accepted PI3 NativeFS primitives, never the PI3 transaction. Endpoints
and an authenticated HA callWS connection must be supplied by a qualified operator
binding. This module does not SSH, invent mount points, provision trust, reload HA,
or turn a saved capability report into native permission. No native CLI is exposed.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import re
import time
import uuid
import contextlib
import errno
import os
import stat
from urllib.parse import urlsplit

RELEASE = '51398bab4e2293b578b2cdac2d0740c3738cab2f'
MANIFEST = {
    'homeassistant/custom_components/hioc_operator/__init__.py': ('ebf4d61bdc2bdd1d5757d420c0fd520c08101ff665976d8128c105eb8ad2547d', 'aba3acac0b0674fbb6421026ab6832b67ce60ca8'),
    'homeassistant/custom_components/hioc_operator/manifest.json': ('ab5b8cc72802cd1330c07162569eb83072081f9043666b8e065e73be734c5bb0', '1575e986a22fede52eb2a88de05706a0b8c7227a'),
    'homeassistant/custom_components/hioc_operator/services.yaml': ('22e558f73800f4250ece8e136a745ddac2700c13007b6a3689d70876d11b91e1', 'eef7d43cc0f03824e83e2a8b3a922afaff3d0c02'),
    'homeassistant/www/hioc-asset-editor.js': ('f8ff3c590a111545f9dac452c8c93eb9b1abc97694d1b90a77e92f9fd039f52c', '472b5fa4345f296cee27980a5a9266ae84553a85'),
    'homeassistant/dashboards/hioc_dashboard_v2.yaml': ('aa675cd1fdd0164064f6f28c909dd06dde4a29f3c89fae14a014a5b11dddcb34', '3eca99a1010b912534626821482e74a6a11822ca'),
    'homeassistant/packages/hioc_incident_center.yaml': ('910668e283dcd158664e720eed591a98b2e44ac79303a752c1f8f16a31fa722b', '031d3583b6c1fdc14eb431d7b5b1818dd37d8c3e'),
}
FILES = {
    source: source.removeprefix('homeassistant/')
    for source in MANIFEST if '/custom_components/' in source or '/www/' in source
}
TX = 'backups/pe73-ha-delivery-v1'
TRUST_BUNDLE = TX + '/trust.disabled.json'
BOOTSTRAP = '.pe73-ha-directory-intent.json'
CARD = {'type': 'custom:hioc-asset-editor', 'inventory_entity': 'sensor.hioc_inventory_devices'}
READS = ('auth/current_user', 'get_config', 'get_services', 'lovelace/info',
         'lovelace/resources/list', 'lovelace/config')
MUTATIONS = ('lovelace/resources/create', 'lovelace/config/save')
API_SOURCE = 'https://github.com/home-assistant/core/blob/2026.8.1/homeassistant/components/lovelace/'


class Stop(ValueError):
    """Only a public code, never private exception text."""


def require(value, code):
    if not value:
        raise Stop(code)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False).encode()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def digest(value):
    return sha(canonical(value))


def path(value):
    require(type(value) is str and bool(value) and '\\' not in value and '\x00' not in value,
            'PATH_INVALID')
    p = PurePosixPath(value)
    require(not p.is_absolute() and all(x not in ('', '.', '..') for x in value.split('/'))
            and '.storage' not in p.parts, 'PATH_INVALID')
    return value


def artifacts(read_object):
    """Reader must return immutable Git blob bytes, not checkout-normalized files."""
    result = {}
    for name, (expected, identity) in MANIFEST.items():
        raw = read_object(RELEASE, name)
        require(type(raw) is bytes and sha(raw) == expected and
                hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == identity,
                'ARTIFACT_IDENTITY_MISMATCH')
        result[name] = raw
    return result


def disabled_trust(ha, backend):
    """Validate existing configuration shape without loading or generating secrets.

    Actual certificate/key validity and on-host private_file checks remain required
    by the qualified endpoint's trust_preflight. No HA or backend enable is written.
    """
    ha, backend = copy.deepcopy(ha), copy.deepcopy(backend)
    require(set(ha) == {'enabled', 'issuer', 'key_id', 'assertion_key_file', 'client_certificate',
        'client_key', 'server_ca', 'server_url', 'operator_allowlist', 'request_timeout_seconds'}, 'HA_TRUST_SHAPE')
    require(set(backend) == {'enabled', 'bind_address', 'port', 'ha_address', 'server_certificate',
        'server_key', 'client_ca', 'issuer_trusts'}, 'BACKEND_TRUST_SHAPE')
    require(ha['enabled'] is False and backend['enabled'] is False, 'ACTIVATION_FORBIDDEN')
    require(type(ha['issuer']) is str and uuid.UUID(hex=ha['issuer']).version == 4
        and uuid.UUID(hex=ha['issuer']).hex == ha['issuer'], 'ISSUER_INVALID')
    require(type(ha['key_id']) is str and re.fullmatch(r'[A-Za-z0-9_-]{1,64}', ha['key_id']), 'KEY_ID_INVALID')
    url = urlsplit(ha['server_url'])
    require(url.scheme == 'https' and url.hostname and url.port and url.path in ('', '/')
        and not url.username and not url.password and not url.query and not url.fragment, 'TRUST_URL_INVALID')
    import ipaddress
    for key in ('bind_address', 'ha_address'):
        addr = ipaddress.ip_address(backend[key])
        require(addr.version == 4 and addr.is_private and not addr.is_unspecified and not addr.is_multicast,
                'TRUST_ADDRESS_INVALID')
    require(type(backend['port']) is int and 1 <= backend['port'] <= 65535
            and backend['port'] == url.port and url.hostname == backend['bind_address'], 'TRUST_ENDPOINT_MISMATCH')
    require(type(ha['request_timeout_seconds']) is int and 1 <= ha['request_timeout_seconds'] <= 30,
            'TRUST_TIMEOUT_INVALID')
    for config, fields in ((ha, ('assertion_key_file','client_certificate','client_key','server_ca')),
                           (backend, ('server_certificate','server_key','client_ca'))):
        for key in fields:
            require(type(config[key]) is str and PurePosixPath(config[key]).is_absolute()
                    and '..' not in PurePosixPath(config[key]).parts, 'PRIVATE_PATH_INVALID')
    allow = ha['operator_allowlist']
    require(type(allow) is list and bool(allow) and len(set(allow)) == len(allow) and
        all(type(x) is str and re.fullmatch(r'[A-Za-z0-9_-]{1,128}', x) for x in allow), 'OPERATOR_ALLOWLIST_INVALID')
    require(type(backend['issuer_trusts']) is list and len(backend['issuer_trusts']) == 1, 'ISSUER_TRUST_INVALID')
    entry = backend['issuer_trusts'][0]
    require(set(entry) == {'enabled','issuer','key_id','assertion_key_file','client_spki_sha256','actors'}
        and entry['enabled'] is False and entry['issuer'] == ha['issuer'] and entry['key_id'] == ha['key_id']
        and type(entry['assertion_key_file']) is str and PurePosixPath(entry['assertion_key_file']).is_absolute()
        and '..' not in PurePosixPath(entry['assertion_key_file']).parts
        and re.fullmatch('[0-9a-f]{64}', entry['client_spki_sha256']), 'ISSUER_TRUST_INVALID')
    require(type(entry['actors']) is dict and set(entry['actors']) == set(allow), 'INDEPENDENT_ACL_REQUIRED')
    for operations in entry['actors'].values():
        require(type(operations) is dict and bool(operations) and set(operations) <=
            {'get','create','update','result','availability_status'}, 'ACL_OPERATION_INVALID')
        for ids in operations.values():
            require(type(ids) is list and bool(ids) and len(set(ids)) == len(ids) and
                all(type(x) is str and re.fullmatch('dev_[0-9a-f]{16}', x) for x in ids), 'ACL_ASSET_INVALID')
    # Inactive packet only. Never inserted into active configuration.yaml or adapter config.
    return {'ha': {'hioc_operator': {'operator': ha, 'observations': {'enabled': False},
                                    'notifications': {'enabled': False}}}, 'backend': backend}


def add_card(config, view_path):
    """Narrow additive edit of an observed regular-cards view; unknown layouts stop."""
    config = copy.deepcopy(config)
    require(type(config) is dict and type(config.get('views')) is list, 'DASHBOARD_INVALID')
    views = [v for v in config['views'] if v.get('path') == view_path]
    require(len(views) == 1, 'VIEW_NOT_UNIQUE')
    view = views[0]
    require(view.get('type', 'masonry') in ('masonry', 'sections') and not view.get('panel'), 'LAYOUT_UNSUPPORTED')
    require('custom:hioc-asset-editor' not in canonical(config).decode(), 'EXISTING_EDITOR_CONFLICT')
    if view.get('type') == 'sections':
        require(type(view.get('sections')) is list, 'LAYOUT_UNSUPPORTED')
        view['sections'].append({'type':'grid', 'cards':[copy.deepcopy(CARD)]})
    else:
        require(type(view.get('cards')) is list, 'LAYOUT_UNSUPPORTED')
        view['cards'].append(copy.deepcopy(CARD))
    return config


class Delivery:
    """Fixed PREPARE -> files -> resource -> card -> independent readback.

    fs exposes the accepted NativeFS snapshot/read/write_new/publish primitives and
    HA-specific begin/save/load ledger bindings. api.call is the existing authenticated
    HA WebSocket request interface (not a credential in JSON). guard observes actual
    host/disabled/caller state; trust_preflight examines existing private trust safely.
    These native bindings are NOT established by synthetic fixtures or saved reports.
    """
    def __init__(self, fs, api, guard, trust_preflight, read_object, *, clock=time.monotonic):
        self.fs, self.api, self.guard, self.trust_preflight = fs, api, guard, trust_preflight
        self.read_object, self.clock = read_object, clock
        self.stopped = False
        self.last = None

    def observe(self, plan):
        require(set(plan) == {'resource_url','dashboard','view','before_files','ha_trust','backend_trust'}, 'PLAN_SHAPE')
        url = urlsplit(plan['resource_url'])
        require(url.scheme == url.netloc == url.query == url.fragment == '' and
            url.path == '/local/hioc-asset-editor.js', 'RESOURCE_URL_UNSUPPORTED')
        # /local is the source-supported HA mapping for www; capability must verify it.
        require(plan['dashboard'] is None or type(plan['dashboard']) is str and bool(plan['dashboard']), 'DASHBOARD_ID_REQUIRED')
        require(type(plan['view']) is str and bool(plan['view']), 'VIEW_REQUIRED')
        state = self.guard()
        require(set(state) == {'host_identity','disabled','exclusive_delivery','resources_loaded','local_mapping',
                              'storage_dashboard','capability_identity'}, 'LIVE_GUARD_SHAPE')
        require(all(state[k] is True for k in ('disabled','exclusive_delivery','resources_loaded',
                    'local_mapping','storage_dashboard')), 'LIVE_CAPABILITY_OR_DISABLED_GATE')
        require(bool(state['host_identity']) and bool(state['capability_identity']), 'LIVE_IDENTITY_REQUIRED')
        require(self.api.call({'type':'auth/current_user'})['is_admin'] is True, 'HA_ADMIN_REQUIRED')
        require('hioc_operator' not in self.api.call({'type':'get_services'}), 'HA_SERVICES_ALREADY_ACTIVE')
        info = self.api.call({'type':'lovelace/info'})
        require(info.get('resource_mode') == 'storage', 'RESOURCE_MODE_UNSUPPORTED')
        resources = self.api.call({'type':'lovelace/resources/list'})
        require(type(resources) is list and all(type(v) is dict for v in resources), 'RESOURCES_INVALID')
        require(not any(urlsplit(v.get('url','')).path == url.path for v in resources), 'RESOURCE_CONFLICT')
        config = self.api.call({'type':'lovelace/config', 'url_path':plan['dashboard']})
        after = add_card(config, plan['view'])
        before = {target:self.fs.snapshot(target, 0o644) for target in FILES.values()}
        require(set(self.fs.children('custom_components/hioc_operator')) <=
                {'__init__.py','manifest.json','services.yaml'}, 'FOREIGN_INTEGRATION_CONTENT')
        require(before == plan['before_files'], 'FILE_BASELINE_DRIFT')
        packet = disabled_trust(plan['ha_trust'], plan['backend_trust'])
        trust = self.trust_preflight(copy.deepcopy(packet))
        require(set(trust) == {'identity','ha_private_files','backend_private_files','certificate_pair',
            'assertion_pair','spki_pin','independent_acl'} and bool(trust['identity']) and
            all(trust[k] is True for k in trust if k != 'identity'), 'TRUST_NOT_ESTABLISHED')
        return dict(state=state, resources=resources, config=config, after=after, before=before,
                    trust=trust, packet=packet, plan_sha256=digest(plan))

    def prepare(self, plan):
        require(not self.stopped and self.last is None, 'NO_RETRY_OR_SECOND_TRANSACTION')
        sources = artifacts(self.read_object)
        observed = self.observe(plan)
        # All facts checked BEFORE creating transaction, staging files or API mutations.
        self.fs.begin(TX)
        journal = dict(schema_version='1.0', state='PREPARING', pending=None, installed=[], dashboard=plan['dashboard'],
                       resource=None, api_after=None, observation=observed, source_release=RELEASE)
        self.last = copy.deepcopy(journal)
        self.fs.save(journal)
        if hasattr(self.fs, 'provision_directories'):
            self.fs.provision_directories(journal)
        for index, (source, target) in enumerate(FILES.items()):
            if observed['before'][target]['exists']:
                raw = self.fs.read(target, 0o644)
                require(sha(raw) == observed['before'][target]['sha256'], 'BACKUP_SOURCE_DRIFT')
                self.fs.write_new(TX + '/before-' + str(index), raw)
            self.fs.write_new(TX + '/stage-' + str(index), sources[source])
        self.fs.write_new(TX + '/dashboard.before.json', canonical(observed['config']))
        self.fs.write_new(TX + '/resources.before.json', canonical(observed['resources']))
        self.fs.write_new(TRUST_BUNDLE, canonical(observed['packet']))
        # Full repository YAML/package retained for reference, NEVER installed/reloaded.
        for name in ('homeassistant/dashboards/hioc_dashboard_v2.yaml',
                     'homeassistant/packages/hioc_incident_center.yaml'):
            self.fs.write_new(TX + '/' + PurePosixPath(name).name + '.reference', sources[name])
        journal['state'] = 'PREPARED'
        self.fs.save(journal)
        self.last = copy.deepcopy(journal)
        return digest(journal)

    def _save(self, journal, state, pending):
        journal['state'], journal['pending'] = state, pending
        self.fs.save(journal)
        self.last = copy.deepcopy(journal)

    def install(self, plan, approved_preparation, *, whole_process_reference):
        """One explicit process approval; technical evidence rechecked, no prompts."""
        require(type(whole_process_reference) is str and re.fullmatch('[A-Za-z0-9_-]{8,96}',
                whole_process_reference), 'WHOLE_PROCESS_AUTHORIZATION_REQUIRED')
        require(not self.stopped and self.last is not None, 'NO_RETRY_OR_AUTOMATIC_RECOVERY')
        journal = self.fs.load()
        require(journal == self.last and digest(journal) == approved_preparation and
                journal['state'] == 'PREPARED', 'PREPARATION_DRIFT')
        deadline = self.clock() + 900
        try:
            sources = artifacts(self.read_object)
            require(self.observe(plan) == journal['observation'], 'FRESH_CONTEXT_DRIFT')
            journal['whole_process_reference'] = whole_process_reference
            self._save(journal, 'PREPARED', None)
            for index, (source, target) in enumerate(FILES.items()):
                self._fresh(journal, deadline)
                require(self.fs.read(TX + '/stage-' + str(index)) == sources[source], 'STAGE_DRIFT')
                self._save(journal, 'INSTALLING', target)
                snapshot = self.fs.publish(target, sources[source], journal['observation']['before'][target], 0o644)
                require(snapshot['sha256'] == MANIFEST[source][0], 'INSTALLATION_NOT_VERIFIED')
                journal['installed'].append({'path':target, 'snapshot':snapshot})
                self._save(journal, 'INSTALLING', None)
            self._fresh(journal, deadline)
            self._save(journal, 'REGISTERING_RESOURCE', 'resource')
            resource = self.api.call({'type':'lovelace/resources/create', 'res_type':'module', 'url':plan['resource_url']})
            require(type(resource) is dict and set(resource) == {'id','url','type'} and
                resource['type'] == 'module' and resource['url'] == plan['resource_url'] and bool(resource['id']), 'RESOURCE_ACK_INVALID')
            journal['resource'] = resource
            self._save(journal, 'REGISTERING_RESOURCE', None)
            self._fresh(journal, deadline)
            self._save(journal, 'REGISTERING_CARD', 'dashboard')
            self.api.call({'type':'lovelace/config/save','url_path':plan['dashboard'],
                           'config':journal['observation']['after']})
            journal['api_after'] = journal['observation']['after']
            self._save(journal, 'VERIFYING', None)
            self._fresh(journal, deadline)
            self.verify(journal, plan)
            self._save(journal, 'DELIVERED_DISABLED', None)
            return {'RESULT':'PASS_SYNTHETIC_OR_QUALIFIED_ENDPOINT_DELIVERY', 'state':journal['state'],
                    'files':len(FILES), 'activation':False, 'automatic_recovery':False}
        except BaseException:
            # Last durable pending intent is retained. Never retry/adopt a lost ACK.
            self.stopped = True
            raise

    def _fresh(self, journal, deadline):
        require(self.clock() < deadline and self.fs.load() == self.last, 'DEADLINE_OR_JOURNAL_DRIFT')
        require(self.guard() == journal['observation']['state'], 'LIVE_CONTEXT_DRIFT')
        require(self.trust_preflight(copy.deepcopy(journal['observation']['packet'])) == journal['observation']['trust'], 'TRUST_DRIFT')
        require('hioc_operator' not in self.api.call({'type':'get_services'}), 'HA_ACTIVATION_DRIFT')
        installed = {entry['path']:entry['snapshot'] for entry in journal['installed']}
        for target in FILES.values():
            require(self.fs.snapshot(target, 0o644) == installed.get(target, journal['observation']['before'][target]), 'RUNTIME_DRIFT')
        resources = self.api.call({'type':'lovelace/resources/list'})
        expected = journal['observation']['resources'] + ([journal['resource']] if journal['resource'] else [])
        require(resources == expected, 'RESOURCE_DRIFT')
        config = self.api.call({'type':'lovelace/config','url_path':journal['dashboard'] if 'dashboard' in journal else self._dashboard})
        require(config == (journal['api_after'] or journal['observation']['config']), 'DASHBOARD_DRIFT')

    def run(self, plan, *, whole_process_reference):
        """Bounded integrated sequence, exactly once; no automatic recovery path."""
        require(type(whole_process_reference) is str and re.fullmatch('[A-Za-z0-9_-]{8,96}',
                whole_process_reference), 'WHOLE_PROCESS_AUTHORIZATION_REQUIRED')
        self._dashboard = plan['dashboard']
        try:
            if hasattr(self.fs, 'authorize_process'):
                self.fs.authorize_process(whole_process_reference, digest(plan))
            prepared = self.prepare(plan)
            return self.install(plan, prepared, whole_process_reference=whole_process_reference)
        except BaseException:
            self.stopped = True
            raise

    def verify(self, journal, plan):
        require(len(journal['installed']) == len(FILES), 'INCOMPLETE_INSTALLATION')
        for source, target in FILES.items():
            require(sha(self.fs.read(target, 0o644)) == MANIFEST[source][0], 'INDEPENDENT_READBACK_FAILED')
        require(self.api.call({'type':'lovelace/config','url_path':plan['dashboard']}) == journal['observation']['after'], 'DASHBOARD_NOT_VERIFIED')
        require(self.fs.read(TRUST_BUNDLE) == canonical(journal['observation']['packet']), 'TRUST_PACKET_DRIFT')

    def restore_files(self, *, recovery_reference):
        """Explicit recovery ONLY after operator adjudicates API/uncertainty externally.

        No API rollback is automatic. A nonterminal/pending transaction is refused.
        Even explicit file recovery refuses while the added live card/resource exists.
        """
        require(type(recovery_reference) is str and re.fullmatch('[A-Za-z0-9_-]{8,96}', recovery_reference), 'RECOVERY_AUTHORIZATION_REQUIRED')
        journal = self.fs.load()
        require(journal['state'] == 'DELIVERED_DISABLED' and journal['pending'] is None, 'RECOVERY_ADJUDICATION_REQUIRED')
        require(self.guard() == journal['observation']['state'], 'RECOVERY_CONTEXT_DRIFT')
        require(self.api.call({'type':'lovelace/resources/list'}) == journal['observation']['resources'] and
                self.api.call({'type':'lovelace/config','url_path':journal['dashboard']}) == journal['observation']['config'], 'API_RESTORATION_NOT_ESTABLISHED')
        try:
            if hasattr(self.fs, 'authorize_recovery'):
                self.fs.authorize_recovery(recovery_reference)
            journal['recovery_reference']=recovery_reference
            for index in reversed(range(len(FILES))):
                target = list(FILES.values())[index]
                installed = journal['installed'][index]['snapshot']
                require(self.fs.snapshot(target, 0o644) == installed, 'RESTORE_TARGET_DRIFT')
                baseline = journal['observation']['before'][target]
                if baseline['exists']:
                    raw = self.fs.read(TX + '/before-' + str(index))
                    require(sha(raw) == baseline['sha256'], 'BACKUP_DRIFT')
                    self._save(journal, 'RESTORING', target)
                    self.fs.publish(target, raw, installed, 0o644)
                    require(sha(self.fs.read(target, 0o644)) == baseline['sha256'], 'RESTORE_NOT_VERIFIED')
                else:
                    self._save(journal, 'RESTORING', target)
                    self.fs.remove_installed(target, installed, 0o644)
                self._save(journal, 'RESTORING', None)
            if hasattr(self.fs, 'restore_created_directory'):
                self.fs.restore_created_directory(journal)
            self._save(journal, 'FILES_RESTORED', None)
        except BaseException:
            self.stopped = True
            raise


def _anchor(info):
    return {'device':info.st_dev,'inode':info.st_ino,'uid':info.st_uid,
            'gid':info.st_gid,'mode':stat.S_IMODE(info.st_mode)}


def _file_identity(info):
    return _anchor(info) | {'size':info.st_size,'mtime_ns':info.st_mtime_ns,
                            'ctime_ns':info.st_ctime_ns,'links':info.st_nlink}


_PRIVATE_NAMES = frozenset(['journal.json','journal-next','dashboard.before.json',
    'resources.before.json','trust.disabled.json','hioc_dashboard_v2.yaml.reference',
    'hioc_incident_center.yaml.reference'] +
    [prefix+str(i) for prefix in ('before-','stage-') for i in range(4)])


class _ScopedHAFileSystem:
    """One-shot, exact-root/file publisher, not a generic privileged filesystem.

    Production factory supplies os and a LIVE read-only NativeProbe. The private
    ops seam exists for Windows descriptor/ownership fixtures only. No root path,
    numeric owner or serialized permission flag can be supplied to the factory.
    """
    def __init__(self, probe, *, _ops=os):
        self._ops,self._probe=_ops,probe
        require(_ops.name=='posix', 'NATIVE_POSIX_REQUIRED')
        self._proof=probe.collect()
        require(self._proof['root'] in ('/config','/homeassistant') and
            self._proof['publisher_uid']==self._proof['publisher_gid']==0,
            'QUALIFIED_SCOPE_REQUIRED')
        self._root=self._proof['root'];self._dirs=copy.deepcopy(self._proof['directories'])
        self._core=(self._proof['core']['uid'],self._proof['core']['gid'])
        require(all(type(x) is int and x>=0 for x in self._core), 'CORE_OWNER_UNKNOWN')
        self._armed=False;self._begun=False;self._recovery=False;self._publishing=None
        self._plan_sha=None;self._reference=None
        self._journal_raw=None;self._bootstrapping=False;self._created=[]
        # Missing required directory proof rejects BEFORE mkdir, open(O_CREAT), chmod or chown.
        for relative in ('','custom_components','www'):
            require(str(PurePosixPath(self._root)/relative) in self._dirs, 'DESTINATION_PREREQUISITE_MISSING')
            require(self._proof.get('core_filesystem',{}).get('anchors',{}).get(relative)==
                    self._dirs[str(PurePosixPath(self._root)/relative)], 'CORE_VISIBLE_IDENTITY_REQUIRED')
        for relative in ('custom_components/hioc_operator','backups'):
            require(relative in self._proof.get('core_filesystem',{}).get('anchors',{}) and
                self._proof['core_filesystem']['anchors'][relative]==self._dirs.get(str(PurePosixPath(self._root)/relative)), 'CORE_VISIBLE_IDENTITY_REQUIRED')
        self._existing=False
        if str(PurePosixPath(self._root)/'backups') not in self._dirs:
            return
        with self._directory('backups') as fd:
            try:info=self._ops.stat('pe73-ha-delivery-v1',dir_fd=fd,follow_symlinks=False)
            except FileNotFoundError:pass
            else:
                require(stat.S_ISDIR(info.st_mode) and info.st_uid==info.st_gid==0 and
                        stat.S_IMODE(info.st_mode)==0o700, 'EXISTING_TRANSACTION_SECURITY')
                self._dirs[str(PurePosixPath(self._root)/TX)]=_anchor(info)
                self._existing=True
        if self._existing:
            with self._directory(TX):pass

    def _live(self):
        require(self._probe.collect()==self._proof, 'CORE_OR_ROOT_CONTEXT_DRIFT')
        require(self._ops.getuid()==self._ops.geteuid()==self._ops.getgid()==self._ops.getegid()==0,
                'PUBLISHER_IDENTITY_DRIFT')

    def authorize_process(self, reference, plan_sha):
        require(not self._existing and not self.snapshot(BOOTSTRAP)['exists'], 'EXISTING_TRANSACTION_REQUIRES_EXPLICIT_DISPOSITION')
        require(not self._armed and not self._begun and re.fullmatch('[A-Za-z0-9_-]{8,96}',reference)
                and re.fullmatch('[0-9a-f]{64}',plan_sha), 'PROCESS_SCOPE_INVALID')
        self._live();self._armed=True;self._reference=reference;self._plan_sha=plan_sha

    def _classify(self, relative):
        path(relative)
        if relative==BOOTSTRAP:return 'private'
        if relative in FILES.values():return 'public'
        if relative.startswith(TX+'/') and relative[len(TX)+1:] in _PRIVATE_NAMES:return 'private'
        temporaries={str(PurePosixPath(x).parent/('.pe73-ha-'+PurePosixPath(x).name)):x for x in FILES.values()}
        require(relative in temporaries and temporaries[relative]==self._publishing, 'PATH_OUTSIDE_CLOSED_SCOPE')
        return 'temporary'

    def _security(self, fd, relative, mode):
        info=self._ops.fstat(fd)
        require(stat.S_ISREG(info.st_mode) and info.st_nlink==1, 'UNSAFE_REGULAR_FILE')
        owner=self._core if self._classify(relative) in ('public','temporary') else (0,0)
        require((info.st_uid,info.st_gid)==owner and stat.S_IMODE(info.st_mode)==mode,
                'EXACT_OWNER_OR_MODE_MISMATCH')
        self._acl(fd)
        return info

    def _acl(self, fd):
        for name in ('system.posix_acl_access','system.posix_acl_default'):
            try:self._ops.getxattr(fd,name)
            except OSError as error:require(error.errno==errno.ENODATA, 'ACL_STATUS_UNKNOWN')
            else:raise Stop('ACL_PRESENT')

    @contextlib.contextmanager
    def _directory(self, relative):
        allowed={'','custom_components','custom_components/hioc_operator','www','backups',TX}
        if relative=='.':relative=''
        require(relative in allowed, 'DIRECTORY_OUTSIDE_SCOPE')
        fd=self._ops.open('/',self._ops.O_RDONLY|self._ops.O_DIRECTORY|self._ops.O_NOFOLLOW|self._ops.O_CLOEXEC)
        held=[fd];links=[];names=['/'];absolute=''
        try:
            for part in [None,*PurePosixPath(self._root).parts[1:],*PurePosixPath(relative).parts]:
                if part is not None:
                    child=self._ops.open(part,self._ops.O_RDONLY|self._ops.O_DIRECTORY|self._ops.O_NOFOLLOW|self._ops.O_CLOEXEC,dir_fd=fd)
                    held.append(child);links.append((fd,part,child));fd=child;absolute+='/'+part;names.append(absolute)
                info=self._ops.fstat(fd)
                require(stat.S_ISDIR(info.st_mode) and self._dirs.get(absolute or '/')==_anchor(info), 'DIRECTORY_IDENTITY_DRIFT')
                require(not stat.S_IMODE(info.st_mode)&0o7022, 'UNSAFE_DIRECTORY_MODE')
                self._acl(fd)
            yield fd
            for parent,name,child in links:
                require(_anchor(self._ops.stat(name,dir_fd=parent,follow_symlinks=False))==_anchor(self._ops.fstat(child)), 'ANCESTOR_SUBSTITUTION')
            for descriptor,name in zip(held,names):
                info=self._ops.fstat(descriptor)
                require(stat.S_ISDIR(info.st_mode) and self._dirs[name]==_anchor(info), 'DIRECTORY_SECURITY_DRIFT')
                self._acl(descriptor)
        finally:
            # Close exactly once. A cleanup error never retries a filesystem mutation.
            primary=__import__('sys').exc_info()[1];failure=None
            for descriptor in reversed(held):
                try:self._ops.close(descriptor)
                except OSError as error:failure=failure or error
            if failure is not None:
                if primary is None:raise failure
                if hasattr(primary,'add_note'):primary.add_note('Descriptor cleanup also failed.')

    def _absent_integration(self):
        if str(PurePosixPath(self._root)/'custom_components/hioc_operator') in self._dirs:
            return False
        with self._directory('custom_components') as fd:
            try:self._ops.stat('hioc_operator',dir_fd=fd,follow_symlinks=False)
            except FileNotFoundError:return True
            raise Stop('UNEXPECTED_INTEGRATION_DIRECTORY')

    def children(self, relative):
        require(relative=='custom_components/hioc_operator', 'DIRECTORY_OUTSIDE_SCOPE')
        if self._absent_integration():return []
        with self._directory(relative) as fd:return sorted(self._ops.listdir(fd))

    def snapshot(self, relative, mode=None):
        kind=self._classify(relative);expected=0o644 if kind in ('public','temporary') else 0o600
        require(mode in (None,expected), 'MODE_OUTSIDE_SCOPE')
        p=PurePosixPath(relative)
        if kind=='public' and str(p.parent)=='custom_components/hioc_operator' and self._absent_integration():
            return {'exists':False,'parents':self._parent_binding(relative)}
        with self._directory(str(p.parent)) as parent:
            try:fd=self._ops.open(p.name,self._ops.O_RDONLY|self._ops.O_NOFOLLOW|self._ops.O_NONBLOCK|self._ops.O_CLOEXEC,dir_fd=parent)
            except FileNotFoundError:return {'exists':False,'parents':self._parent_binding(relative)}
            try:
                info=self._security(fd,relative,expected);identity=_file_identity(info)
                raw=self._read_fd(fd)
                require(identity==_file_identity(self._ops.fstat(fd))==_file_identity(self._ops.stat(p.name,dir_fd=parent,follow_symlinks=False)), 'FILE_IDENTITY_DRIFT')
                return {'exists':True,'parents':self._parent_binding(relative),'identity':identity,'sha256':sha(raw)}
            finally:self._ops.close(fd)

    def _parent_binding(self, relative):
        full=str(PurePosixPath(self._root)/PurePosixPath(relative).parent)
        return {p:copy.deepcopy(v) for p,v in self._dirs.items() if p!=str(PurePosixPath(self._root)/'custom_components/hioc_operator') and (p=='/' or full==p or full.startswith(p+'/'))}

    def _read_fd(self, fd):
        chunks=bytearray()
        while len(chunks)<=1048576:
            value=self._ops.read(fd,min(65536,1048577-len(chunks)))
            if not value:break
            chunks.extend(value)
        require(len(chunks)<=1048576, 'READ_LIMIT')
        return bytes(chunks)

    def read(self, relative, mode=0o600):
        before=self.snapshot(relative,mode);require(before['exists'], 'FILE_MISSING')
        p=PurePosixPath(relative)
        with self._directory(str(p.parent)) as parent:
            fd=self._ops.open(p.name,self._ops.O_RDONLY|self._ops.O_NOFOLLOW|self._ops.O_CLOEXEC,dir_fd=parent)
            try:
                require(_file_identity(self._security(fd,relative,mode))==before['identity'], 'FILE_IDENTITY_DRIFT')
                raw=self._read_fd(fd)
            finally:self._ops.close(fd)
        require(sha(raw)==before['sha256'] and self.snapshot(relative,mode)==before, 'FILE_IDENTITY_DRIFT')
        return raw

    def begin(self, tx):
        require(self._armed and not self._begun and tx==TX, 'PROCESS_NOT_AUTHORIZED')
        self._live()
        if str(PurePosixPath(self._root)/'backups') not in self._dirs:
            # A fixed private bootstrap intent precedes the missing backup parent.
            # Existing bootstrap evidence is never overwritten or auto-adopted.
            self._bootstrapping=True
            try:self.write_new(BOOTSTRAP,canonical({'state':'DIRECTORY_CREATE_INTENT','path':'backups',
                'plan_sha256':self._plan_sha,'reference':self._reference,'context_sha256':digest(self._proof)}))
            finally:self._bootstrapping=False
            self._create_directory('backups',0o700)
        with self._directory('backups') as fd:
            self._ops.mkdir('pe73-ha-delivery-v1',0o700,dir_fd=fd)
            self._ops.fsync(fd)
            value=self._ops.stat('pe73-ha-delivery-v1',dir_fd=fd,follow_symlinks=False)
            require(stat.S_ISDIR(value.st_mode) and value.st_uid==value.st_gid==0
                    and stat.S_IMODE(value.st_mode)==0o700, 'PRIVATE_DIRECTORY_SECURITY')
            self._dirs[str(PurePosixPath(self._root)/TX)]=_anchor(value)
        self._begun=True

    def _create_directory(self, relative, mode):
        require(relative in ('backups','custom_components/hioc_operator') and
            mode==(0o700 if relative=='backups' else 0o755), 'DIRECTORY_CREATION_OUTSIDE_SCOPE')
        require(self._armed, 'DIRECTORY_PROCESS_NOT_AUTHORIZED')
        self._live();p=PurePosixPath(relative)
        if relative=='backups':
            require(not self._begun and self.read(BOOTSTRAP)==canonical({'state':'DIRECTORY_CREATE_INTENT','path':'backups',
                'plan_sha256':self._plan_sha,'reference':self._reference,'context_sha256':digest(self._proof)}), 'BOOTSTRAP_INTENT_REQUIRED')
        else:
            require(self._begun, 'DIRECTORY_PROCESS_NOT_AUTHORIZED')
            journal=self.load()
            require(journal['state']=='PREPARING' and journal['pending']==relative and journal['observation']['plan_sha256']==self._plan_sha, 'DURABLE_DIRECTORY_INTENT_REQUIRED')
        require(str(PurePosixPath(self._root)/relative) not in self._dirs, 'DIRECTORY_ALREADY_PRESENT')
        with self._directory(str(p.parent)) as parent:
            self._ops.mkdir(p.name,mode,dir_fd=parent)
            info=self._ops.stat(p.name,dir_fd=parent,follow_symlinks=False)
            fd=self._ops.open(p.name,self._ops.O_RDONLY|self._ops.O_DIRECTORY|self._ops.O_NOFOLLOW|self._ops.O_CLOEXEC,dir_fd=parent)
            try:
                require(_anchor(self._ops.fstat(fd))==_anchor(info) and stat.S_ISDIR(info.st_mode) and info.st_uid==info.st_gid==0, 'CREATED_DIRECTORY_IDENTITY')
                self._ops.fchmod(fd,mode);self._acl(fd);self._ops.fsync(fd)
                created=_anchor(self._ops.fstat(fd))
                require(created==_anchor(self._ops.stat(p.name,dir_fd=parent,follow_symlinks=False)) and created['mode']==mode, 'CREATED_DIRECTORY_DRIFT')
            finally:self._ops.close(fd)
            self._ops.fsync(parent)
        expected=copy.deepcopy(self._proof)
        expected['directories'][str(PurePosixPath(self._root)/relative)]=created
        expected['core_filesystem']['anchors'][relative]=created
        require(self._probe.collect()==expected, 'CREATED_DIRECTORY_CORE_PROOF_FAILED')
        self._proof=expected;self._dirs.update(copy.deepcopy(expected['directories']))
        self._created.append({'path':relative,'identity':created})

    def provision_directories(self, journal):
        require(self._armed and self._begun and journal['state']=='PREPARING' and journal['pending'] is None, 'DIRECTORY_INTENT_SCOPE')
        journal['created_directories']=copy.deepcopy(self._created)
        if self._absent_integration():
            journal['pending']='custom_components/hioc_operator';self.save(journal)
            self._create_directory('custom_components/hioc_operator',0o755)
            journal['created_directories']=copy.deepcopy(self._created);journal['pending']=None
        self.save(journal)

    def write_new(self, relative, raw, mode=0o600):
        kind=self._classify(relative)
        require(self._armed and (self._begun or self._bootstrapping and relative==BOOTSTRAP) and type(raw) is bytes and len(raw)<=1048576, 'WRITE_NOT_AUTHORIZED')
        require(kind!='public' and mode==(0o644 if kind=='temporary' else 0o600), 'WRITE_OUTSIDE_SCOPE')
        self._live();p=PurePosixPath(relative)
        with self._directory(str(p.parent)) as parent:
            fd=self._ops.open(p.name,self._ops.O_WRONLY|self._ops.O_CREAT|self._ops.O_EXCL|self._ops.O_NOFOLLOW|self._ops.O_CLOEXEC,mode,dir_fd=parent)
            try:
                info=self._ops.fstat(fd)
                require(stat.S_ISREG(info.st_mode) and info.st_nlink==1 and info.st_uid==info.st_gid==0, 'NEW_DESCRIPTOR_IDENTITY')
                owner=self._core if kind=='temporary' else (0,0)
                if owner!=(0,0):self._ops.fchown(fd,*owner)
                # Only the just-created, exclusive, scope-checked descriptor is changed.
                self._ops.fchmod(fd,mode);self._security(fd,relative,mode)
                offset=0
                while offset<len(raw):
                    written=self._ops.write(fd,raw[offset:]);require(written>0, 'SHORT_WRITE');offset+=written
                self._ops.fsync(fd)
            finally:self._ops.close(fd)
            self._ops.fsync(parent)
        require(self.read(relative,mode)==raw, 'NEW_FILE_READBACK_FAILED')

    def save(self, value):
        require(value['observation']['plan_sha256']==self._plan_sha, 'JOURNAL_PROCESS_SCOPE_DRIFT')
        if self._journal_raw is None:
            require(not self.snapshot(TX+'/journal.json')['exists'], 'EXISTING_JOURNAL_REFUSED')
        else:
            require(self.read(TX+'/journal.json')==self._journal_raw, 'JOURNAL_EXTERNAL_DRIFT')
        self.write_new(TX+'/journal-next',canonical(value))
        with self._directory(TX) as fd:
            self._ops.replace('journal-next','journal.json',src_dir_fd=fd,dst_dir_fd=fd);self._ops.fsync(fd)
        require(self.load()==value, 'JOURNAL_NOT_VERIFIED')
        self._journal_raw=canonical(value)

    def load(self):
        raw=self.read(TX+'/journal.json');value=json.loads(raw)
        require(canonical(value)==raw, 'JOURNAL_INVALID')
        return value

    def _payload(self, target, raw):
        source=next(p for p,t in FILES.items() if t==target)
        if not self._recovery:
            require(sha(raw)==MANIFEST[source][0], 'PUBLIC_PAYLOAD_NOT_PINNED')
        else:
            journal=self.load();index=list(FILES.values()).index(target)
            expected=journal['observation']['before'][target]
            require(expected['exists'] and sha(raw)==expected['sha256']
                    and raw==self.read(TX+'/before-'+str(index)), 'RECOVERY_PAYLOAD_MISMATCH')

    def publish(self, relative, raw, before, mode):
        require(relative in FILES.values() and mode==0o644 and self._armed and self._begun, 'PUBLICATION_OUTSIDE_SCOPE')
        self._live();self._payload(relative,raw)
        journal=self.load()
        require(journal['pending']==relative and journal['state']==('RESTORING' if self._recovery else 'INSTALLING'), 'DURABLE_INTENT_REQUIRED')
        require(self.snapshot(relative,mode)==before, 'DESTINATION_DRIFT')
        p=PurePosixPath(relative);temp='.pe73-ha-'+p.name;self._publishing=relative
        try:
            self.write_new(str(p.parent/temp),raw,mode)
            temporary_snapshot=self.snapshot(str(p.parent/temp),mode)
            with self._directory(str(p.parent)) as fd:
                require(self.snapshot(relative,mode)==before, 'DESTINATION_DRIFT')
                require(self.snapshot(str(p.parent/temp),mode)==temporary_snapshot, 'TEMPORARY_IDENTITY_DRIFT')
                if before['exists']:self._ops.replace(temp,p.name,src_dir_fd=fd,dst_dir_fd=fd)
                else:self._rename_new(fd,temp,p.name)
                self._ops.fsync(fd)
            result=self.snapshot(relative,mode)
            require(result['sha256']==sha(raw), 'PUBLICATION_READBACK_FAILED')
            return result
        finally:self._publishing=None

    def _rename_new(self, fd, source, target):
        if self._ops is not os:
            return self._ops.rename_new(fd,source,target)
        import ctypes
        library=ctypes.CDLL(None,use_errno=True);rename=library.renameat2
        rename.argtypes=[ctypes.c_int,ctypes.c_char_p,ctypes.c_int,ctypes.c_char_p,ctypes.c_uint]
        rename.restype=ctypes.c_int
        require(rename(fd,os.fsencode(source),fd,os.fsencode(target),1)==0, 'NOREPLACE_PUBLICATION_FAILED')

    def authorize_recovery(self, reference):
        require((self._begun or self._existing) and not self._recovery and re.fullmatch('[A-Za-z0-9_-]{8,96}',reference), 'RECOVERY_NOT_AUTHORIZED')
        self._live();journal=self.load()
        require(journal['state']=='DELIVERED_DISABLED' and journal['pending'] is None and
            journal['source_release']==RELEASE and [x['path'] for x in journal['installed']]==list(FILES.values()) and
            set(journal['observation']['before'])==set(FILES.values()), 'UNCERTAIN_RECOVERY_REFUSED')
        for index,(source,target) in enumerate(FILES.items()):
            require(self.snapshot(target,0o644)==journal['installed'][index]['snapshot'] and
                    sha(self.read(target,0o644))==MANIFEST[source][0], 'RECOVERY_INSTALLATION_DRIFT')
            before=journal['observation']['before'][target]
            if before['exists']:
                require(sha(self.read(TX+'/before-'+str(index)))==before['sha256'], 'RECOVERY_BACKUP_DRIFT')
        self._plan_sha=journal['observation']['plan_sha256']
        require(re.fullmatch('[0-9a-f]{64}',self._plan_sha), 'RECOVERY_PROCESS_SCOPE_INVALID')
        self._journal_raw=canonical(journal);self._armed=True;self._begun=True
        self._recovery=True

    def restore_created_directory(self, journal):
        created=next((x for x in journal.get('created_directories',[]) if x['path']=='custom_components/hioc_operator'),None)
        if created is None:return
        require(self._recovery and journal['state']=='RESTORING' and journal['pending'] is None, 'DIRECTORY_RECOVERY_SCOPE')
        relative=created['path'];absolute=str(PurePosixPath(self._root)/relative)
        require(self._dirs.get(absolute)==created['identity'], 'DIRECTORY_RECOVERY_IDENTITY_DRIFT')
        with self._directory(relative) as fd:
            require(not self._ops.listdir(fd), 'CREATED_DIRECTORY_NOT_EMPTY')
        journal['pending']=relative;self.save(journal);self._live()
        with self._directory('custom_components') as fd:
            require(_anchor(self._ops.stat('hioc_operator',dir_fd=fd,follow_symlinks=False))==created['identity'], 'DIRECTORY_RECOVERY_IDENTITY_DRIFT')
            self._ops.rmdir('hioc_operator',dir_fd=fd);self._ops.fsync(fd)
        expected=copy.deepcopy(self._proof);del expected['directories'][absolute]
        expected['core_filesystem']['anchors'][relative]=None
        require(self._probe.collect()==expected, 'REMOVED_DIRECTORY_CORE_PROOF_FAILED')
        self._proof=expected;self._dirs.pop(absolute);self._dirs.update(copy.deepcopy(expected['directories']))
        journal['removed_created_directory']=created;journal['pending']=None;self.save(journal)

    def remove_installed(self, relative, expected, mode):
        require(self._recovery and relative in FILES.values() and mode==0o644, 'REMOVAL_NOT_AUTHORIZED')
        self._live();journal=self.load()
        require(journal['pending']==relative and journal['state']=='RESTORING' and
            not journal['observation']['before'][relative]['exists'], 'REMOVAL_SCOPE_INVALID')
        require(expected==next(x['snapshot'] for x in journal['installed'] if x['path']==relative)
                and self.snapshot(relative,mode)==expected, 'INSTALLED_IDENTITY_DRIFT')
        p=PurePosixPath(relative)
        with self._directory(str(p.parent)) as fd:
            require(_file_identity(self._ops.stat(p.name,dir_fd=fd,follow_symlinks=False))==expected['identity'], 'INSTALLED_IDENTITY_DRIFT')
            self._ops.unlink(p.name,dir_fd=fd);self._ops.fsync(fd)
        require(not self.snapshot(relative,mode)['exists'], 'REMOVAL_NOT_VERIFIED')


def native_filesystem():
    """No arbitrary root/owner inputs or saved-report admission. Qualification first."""
    require(os.name=='posix', 'NATIVE_POSIX_REQUIRED')
    spec=importlib.util.spec_from_file_location('pe73_live_ha_probe',Path(__file__).with_name('pe73_ha_assess.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return _ScopedHAFileSystem(module.NativeProbe())


def receipt(driver, plan, *, whole_process_reference):
    """No private exceptions, paths, actors, trust configuration or HA payloads."""
    try:
        result = driver.run(plan, whole_process_reference=whole_process_reference)
        return result | {'STOP_REQUIRED':True, 'PE73':'IN_PROGRESS', 'PE74':'NOT_AUTHORIZED'}
    except BaseException as error:
        driver.stopped = True
        return {'RESULT':'FAIL_STOP', 'failure_code':str(error) if type(error) is Stop else 'DELIVERY_OR_READBACK_UNCERTAIN',
                'automatic_recovery':False, 'activation':False, 'STOP_REQUIRED':True}
