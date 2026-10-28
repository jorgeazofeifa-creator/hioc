"""One integrated Windows synthetic acceptance set; no production endpoints.

Uses existing real-file/fsync/atomic-replacement fixtures and explicit POSIX
security metadata. Synthetic callback results never qualify native transport,
ownership, trust/certificate validity, HA API capability or consumer exclusion.
"""
import asyncio
import copy
import hashlib
import importlib.util
import json
import os
import errno
import stat
import types
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch
import test_pe73_pi3_delivery as existing

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('pe73_ha_test', ROOT/'tools/pe73_ha_delivery.py')
h = importlib.util.module_from_spec(spec); spec.loader.exec_module(h)
SOURCE = {p:existing.git('show',h.RELEASE+':'+p) for p in h.MANIFEST}


class Files(existing.FixtureFS):
    def __init__(self, root):
        super().__init__(root)
        for name in ('custom_components/hioc_operator','www'):
            (root/name).mkdir(parents=True)
        self.begins = 0

    def children(self, relative):
        return sorted(x.name for x in self.path(relative).iterdir())

    def begin(self, tx):
        self.begins += 1
        self.path(tx).mkdir(mode=0o700)

    def save(self, value):
        self.write_new(h.TX+'/journal-next', h.canonical(value))
        os.replace(self.path(h.TX+'/journal-next'),self.path(h.TX+'/journal.json'))
        self.modes[h.TX+'/journal.json'] = 0o600

    def load(self):
        return json.loads(self.read(h.TX+'/journal.json'))


class API:
    def __init__(self):
        self.config = {'title':'Existing theme/layout', 'views':[{'path':'hioc-v2-inventory','cards':[{'type':'markdown','content':'preserve'}]}]}
        self.resources = [{'id':'existing-css','url':'/observed-existing.css','type':'css'}]
        self.calls = []
        self.active = False
        self.fail = None
        self.mode = 'storage'
        self.admin = True

    def call(self, value):
        self.calls.append(copy.deepcopy(value)); kind = value['type']
        if self.fail == kind + ':before': raise OSError('private error must not be emitted')
        if kind == 'auth/current_user': result = {'is_admin':self.admin}
        elif kind == 'get_services': result = {'hioc_operator':{}} if self.active else {}
        elif kind == 'lovelace/info': result = {'resource_mode':self.mode}
        elif kind == 'lovelace/resources/list': result = self.resources
        elif kind == 'lovelace/config': result = self.config
        elif kind == 'lovelace/resources/create':
            result = {'id':'fixture-created-id','url':value['url'],'type':value['res_type']}
            self.resources.append(result)
        elif kind == 'lovelace/config/save': self.config = copy.deepcopy(value['config']);result = None
        else: raise AssertionError('UNEXPECTED_API_CALL')
        if self.fail == kind + ':after': raise OSError('private lost acknowledgement')
        return copy.deepcopy(result)


def configs():
    ha = {'enabled':False,'issuer':'12345678123442348234123456789abc','key_id':'fixture_only',
          'assertion_key_file':'/fixture/ha-private/assertion','client_certificate':'/fixture/ha-private/client.crt',
          'client_key':'/fixture/ha-private/client.key','server_ca':'/fixture/ha-private/server-ca',
          'server_url':'https://192.168.10.2:12345','operator_allowlist':['fixture_operator'], 'request_timeout_seconds':5}
    backend = {'enabled':False,'bind_address':'192.168.10.2','port':12345,'ha_address':'192.168.10.3',
               'server_certificate':'/fixture/pi3-private/server.crt','server_key':'/fixture/pi3-private/server.key',
               'client_ca':'/fixture/pi3-private/client-ca', 'issuer_trusts':[{
                   'enabled':False,'issuer':ha['issuer'],'key_id':ha['key_id'],
                   'assertion_key_file':'/fixture/pi3-private/assertion','client_spki_sha256':'a'*64,
                   'actors':{'fixture_operator':{'get':['dev_0123456789abcdef'],'availability_status':['dev_0123456789abcdef']}}}]}
    return ha,backend


class DeliveryAcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.fs = Files(Path(self.temp.name));self.api=API()
        self.guard_value = {'host_identity':'fixture-boot-host','disabled':True,'exclusive_delivery':True,
            'resources_loaded':True,'local_mapping':True,'storage_dashboard':True,'capability_identity':'observed-source-sha'}
        self.trust = {'identity':'fixture-bound-public-digests', 'ha_private_files':True,'backend_private_files':True,
            'certificate_pair':True,'assertion_pair':True,'spki_pin':True,'independent_acl':True}
        self.driver = h.Delivery(self.fs,self.api,lambda:copy.deepcopy(self.guard_value),
            lambda _:copy.deepcopy(self.trust),lambda release,p:SOURCE[p], route_probe=lambda url,expected: {'url':url,'sha256':expected,'status':200,'identity_encoding':True})
        ha,backend=configs()
        self.plan = {'resource_url':'/local/hioc-asset-editor.js','dashboard':'hioc-dashboard-v2',
            'view':'hioc-v2-inventory','before_files':{p:self.fs.snapshot(p,0o644) for p in h.FILES.values()},
            'ha_trust':ha,'backend_trust':backend}

    def run_delivery(self):
        return self.driver.run(self.plan,whole_process_reference='OWNER_APPROVED_FIXED_DELIVERY')

    def test_integrated_delivery_exact_files_resource_card_trust_disabled(self):
        before = copy.deepcopy(self.api.config);resources=copy.deepcopy(self.api.resources)
        result = self.run_delivery()
        self.assertEqual(result['state'],'DELIVERED_DISABLED')
        self.assertFalse(result['activation']);self.assertEqual(result['files'],4)
        for source,target in h.FILES.items():self.assertEqual(self.fs.read(target,0o644),SOURCE[source])
        self.assertEqual(self.api.config,h.add_card(before,'hioc-v2-inventory'))
        self.assertEqual(self.api.resources[:-1],resources)
        packet=json.loads(self.fs.read(h.TRUST_BUNDLE))
        self.assertFalse(packet['backend']['enabled'])
        self.assertFalse(packet['ha']['hioc_operator']['operator']['enabled'])
        self.assertEqual([x['type'] for x in self.api.calls if x['type'] in h.MUTATIONS],list(h.MUTATIONS))
        self.fs.assert_unrelated(self)

    def test_manifest_git_and_sha_exact(self):
        self.assertEqual(len(h.artifacts(lambda release,p:SOURCE[p])),6)
        with self.assertRaisesRegex(h.Stop,'ARTIFACT_IDENTITY'):h.artifacts(lambda release,p:SOURCE[p]+b' ')

    def test_read_object_always_immutable_release(self):
        reader=Mock(side_effect=lambda release,p:SOURCE[p]);h.artifacts(reader)
        self.assertEqual({x.args[0] for x in reader.call_args_list},{h.RELEASE})

    def test_whole_process_authority_no_prompts(self):
        with patch('builtins.input',side_effect=AssertionError('NO_PROMPTS')):self.run_delivery()

    def test_missing_process_authority_no_writes(self):
        with self.assertRaises(h.Stop):self.driver.run(self.plan,whole_process_reference='')
        self.assertEqual(self.fs.begins,0)

    def test_invalid_unknown_capabilities_no_writes(self):
        for field in ('disabled','exclusive_delivery','resources_loaded','local_mapping','storage_dashboard'):
            self.guard_value[field]=False
            with self.assertRaisesRegex(h.Stop,'LIVE_CAPABILITY'):self.driver.observe(self.plan)
            self.guard_value[field]=True
        self.assertEqual(self.fs.begins,0)

    def test_admin_and_storage_mode_required(self):
        self.api.admin=False
        with self.assertRaisesRegex(h.Stop,'HA_ADMIN'):self.driver.observe(self.plan)
        self.api.admin=True;self.api.mode='yaml'
        with self.assertRaisesRegex(h.Stop,'RESOURCE_MODE'):self.driver.observe(self.plan)

    def test_existing_resource_and_duplicate_editor_conflicts(self):
        self.api.resources.append({'id':'foreign','url':self.plan['resource_url']+'?v=old','type':'module'})
        with self.assertRaisesRegex(h.Stop,'RESOURCE_CONFLICT'):self.driver.observe(self.plan)
        self.api.resources.pop();self.api.config['views'][0]['cards'].append(h.CARD)
        with self.assertRaisesRegex(h.Stop,'EXISTING_EDITOR_CONFLICT'):self.driver.observe(self.plan)

    def test_foreign_integration_content_refused(self):
        self.fs.path('custom_components/hioc_operator/foreign.py').write_bytes(b'keep')
        with self.assertRaisesRegex(h.Stop,'FOREIGN_INTEGRATION_CONTENT'):self.driver.observe(self.plan)

    def test_unknown_resource_urls_not_invented(self):
        for url in ('https://invented/editor.js','/wrong.js','/local/hioc-asset-editor.js?v=1'):
            self.plan['resource_url']=url
            with self.assertRaises(h.Stop):self.driver.observe(self.plan)

    def test_sections_and_masonry_preserve_existing_layout(self):
        config={'theme':'old','views':[{'path':'x','type':'sections','sections':[{'type':'grid','cards':[]}]}]}
        result=h.add_card(config,'x')
        self.assertEqual(result['views'][0]['sections'][:-1],config['views'][0]['sections'])
        self.assertEqual(result['theme'],'old');self.assertEqual(len(result['views'][0]['sections']),2)

    def test_unknown_and_panel_layouts_not_rewritten(self):
        for view in ({'path':'x','type':'panel','cards':[]},{'path':'x','type':'custom:unknown'}):
            with self.assertRaises(h.Stop):h.add_card({'views':[view]},'x')

    def test_backup_and_explicit_restoration_exact(self):
        for target in h.FILES.values():self.fs.write_new(target,b'old exact accepted-before fixture',0o644)
        self.plan['before_files']={p:self.fs.snapshot(p,0o644) for p in h.FILES.values()}
        self.run_delivery();journal=self.fs.load()
        self.api.config=copy.deepcopy(journal['observation']['config']);self.api.resources=copy.deepcopy(journal['observation']['resources'])
        self.driver.restore_files(recovery_reference='SEPARATE_APPROVED_RECOVERY')
        for target in h.FILES.values():self.assertEqual(self.fs.read(target,0o644),b'old exact accepted-before fixture')
        self.assertEqual(self.fs.load()['state'],'FILES_RESTORED')
        self.assertTrue(self.fs.path(h.TX+'/before-0').exists())

    def test_new_file_restoration_removes_only_exact_installed_objects(self):
        self.run_delivery();journal=self.fs.load()
        self.api.config=copy.deepcopy(journal['observation']['config']);self.api.resources=copy.deepcopy(journal['observation']['resources'])
        self.driver.restore_files(recovery_reference='SEPARATE_APPROVED_RECOVERY')
        self.assertTrue(all(not self.fs.path(p).exists() for p in h.FILES.values()));self.fs.assert_unrelated(self)

    def test_live_card_blocks_file_recovery(self):
        self.run_delivery()
        with self.assertRaisesRegex(h.Stop,'API_RESTORATION_NOT_ESTABLISHED'):
            self.driver.restore_files(recovery_reference='SEPARATE_APPROVED_RECOVERY')

    def test_backup_tamper_refuses_recovery(self):
        for target in h.FILES.values():self.fs.write_new(target,b'old',0o644)
        self.plan['before_files']={p:self.fs.snapshot(p,0o644) for p in h.FILES.values()}
        self.run_delivery();journal=self.fs.load()
        self.api.config=copy.deepcopy(journal['observation']['config']);self.api.resources=copy.deepcopy(journal['observation']['resources'])
        self.fs.path(h.TX+'/before-3').write_bytes(b'tampered')
        with self.assertRaisesRegex(h.Stop,'BACKUP_DRIFT'):
            self.driver.restore_files(recovery_reference='ANOTHER_APPROVED_RECOVERY')

    def test_existing_transaction_never_reused_or_overwritten(self):
        self.fs.path(h.TX).mkdir()
        with self.assertRaises(FileExistsError):self.run_delivery()
        self.assertFalse(self.fs.path(h.TX+'/journal.json').exists())

    def test_stage_tamper_refused(self):
        prepared=self.driver.prepare(self.plan)
        self.fs.path(h.TX+'/stage-0').write_bytes(b'changed')
        with self.assertRaisesRegex(h.Stop,'STAGE_DRIFT'):
            self.driver.install(self.plan,prepared,whole_process_reference='OWNER_APPROVED_FIXED_DELIVERY')
        self.assertEqual(self.fs.publications,[])

    def test_file_baseline_drift_refused(self):
        self.fs.write_new(list(h.FILES.values())[0],b'concurrent file',0o644)
        with self.assertRaisesRegex(h.Stop,'FILE_BASELINE_DRIFT'):self.run_delivery()
        self.assertEqual(self.fs.begins,0)

    def test_activation_refused(self):
        self.api.active=True
        with self.assertRaisesRegex(h.Stop,'HA_SERVICES_ALREADY_ACTIVE'):self.run_delivery()
        self.assertEqual(self.fs.begins,0)

    def test_scope_change_invalidates_preparation(self):
        prepared=self.driver.prepare(self.plan);self.plan['dashboard']='different'
        with self.assertRaisesRegex(h.Stop,'EXCLUSIVE_HIOC_DASHBOARD_REQUIRED'):
            self.driver.install(self.plan,prepared,whole_process_reference='OWNER_APPROVED_FIXED_DELIVERY')

    def test_live_identity_change_invalidates_preparation(self):
        prepared=self.driver.prepare(self.plan);self.guard_value['host_identity']='new-boot'
        with self.assertRaisesRegex(h.Stop,'FRESH_CONTEXT_DRIFT'):
            self.driver.install(self.plan,prepared,whole_process_reference='OWNER_APPROVED_FIXED_DELIVERY')

    def test_interrupted_file_publication_keeps_pending_and_no_retry(self):
        self.fs.fail=lambda p:p.startswith('PUBLISH:')
        with self.assertRaises(OSError):self.run_delivery()
        self.assertEqual(self.fs.load()['pending'],list(h.FILES.values())[0])
        self.assertEqual(self.api.resources[-1]['id'],'existing-css')
        with self.assertRaises(h.Stop):self.run_delivery()

    def test_resource_lost_ack_never_retried_or_rolled_back(self):
        self.api.fail='lovelace/resources/create:after'
        with self.assertRaises(OSError):self.run_delivery()
        self.assertEqual(self.fs.load()['pending'],'resource');self.assertEqual(len(self.api.resources),2)
        self.assertEqual(sum(x['type']=='lovelace/resources/create' for x in self.api.calls),1)
        with self.assertRaises(h.Stop):self.run_delivery()

    def test_dashboard_lost_ack_keeps_uncertainty(self):
        self.api.fail='lovelace/config/save:after'
        with self.assertRaises(OSError):self.run_delivery()
        self.assertEqual(self.fs.load()['pending'],'dashboard')
        self.assertEqual(sum(x['type']=='lovelace/config/save' for x in self.api.calls),1)

    def test_no_secrets_generated_no_activation_or_unrelated_api_calls(self):
        with patch('socket.socket',side_effect=AssertionError('NO_NETWORK_IN_FIXTURE')):
            self.run_delivery()
        self.assertTrue({x['type'] for x in self.api.calls}<=set(h.READS+h.MUTATIONS))
        self.assertNotIn('configuration.yaml',[p.relative_to(self.fs.root).as_posix() for p in self.fs.root.rglob('*')])

    def test_private_exceptions_not_exposed_in_receipt(self):
        self.api.fail='lovelace/resources/create:after'
        result=h.receipt(self.driver,self.plan,whole_process_reference='OWNER_APPROVED_FIXED_DELIVERY')
        self.assertEqual(result['RESULT'],'FAIL_STOP')
        self.assertNotIn('private',json.dumps(result));self.assertFalse(result['automatic_recovery'])

    def test_unsafe_paths_rejected(self):
        for p in ('/etc/passwd','../elsewhere','a/../b','a\\b','.storage/lovelace','a//b'):
            with self.assertRaises(h.Stop):h.path(p)

    def test_deadline_expiry_before_publication(self):
        prepared=self.driver.prepare(self.plan)
        self.driver.clock=Mock(side_effect=[0,901])
        with self.assertRaisesRegex(h.Stop,'DEADLINE_OR_JOURNAL_DRIFT'):
            self.driver.install(self.plan,prepared,whole_process_reference='OWNER_APPROVED_FIXED_DELIVERY')
        self.assertEqual(self.fs.publications,[])

    def test_native_binding_refuses_windows_without_mutation(self):
        if os.name != 'nt':self.skipTest('Windows-specific native refusal')
        with self.assertRaisesRegex(ValueError,'NATIVE_POSIX_REQUIRED'):h.native_filesystem()

    def test_disabled_trust_rejects_enable_wildcard_and_missing_acl(self):
        ha,backend=configs();ha['enabled']=True
        with self.assertRaisesRegex(h.Stop,'ACTIVATION_FORBIDDEN'):h.disabled_trust(ha,backend)
        ha['enabled']=False;backend['issuer_trusts'][0]['actors']={}
        with self.assertRaisesRegex(h.Stop,'INDEPENDENT_ACL_REQUIRED'):h.disabled_trust(ha,backend)
        backend=configs()[1];backend['issuer_trusts'][0]['actors']['fixture_operator']['get']=['*']
        with self.assertRaisesRegex(h.Stop,'ACL_ASSET_INVALID'):h.disabled_trust(ha,backend)

    def test_unvalidated_live_trust_is_not_permission(self):
        self.trust['certificate_pair']=False
        with self.assertRaisesRegex(h.Stop,'TRUST_NOT_ESTABLISHED'):self.run_delivery()
        self.assertEqual(self.fs.begins,0)

    def test_permissions_and_symlinks_refused_by_existing_fixture(self):
        target=list(h.FILES.values())[0];self.fs.write_new(target,b'old',0o644)
        self.fs.modes[target]=0o666
        with self.assertRaises(existing.d.Failure):self.driver.observe(self.plan)

    def test_partial_journal_never_automatically_adopted(self):
        self.api.fail='lovelace/config/save:after'
        with self.assertRaises(OSError):self.run_delivery()
        fresh=h.Delivery(self.fs,self.api,lambda:self.guard_value,lambda _:self.trust,lambda release,p:SOURCE[p], route_probe=lambda url,expected: {'url':url,'sha256':expected,'status':200,'identity_encoding':True})
        with self.assertRaises(h.Stop):fresh.install(self.plan,'irrelevant',whole_process_reference='OWNER_APPROVED_FIXED_DELIVERY')

    def test_concurrent_unrelated_resource_edit_stops_without_overwrite(self):
        publish=self.fs.publish
        def changed(*args):
            result=publish(*args)
            self.api.resources.append({'id':'concurrent','url':'/other.js','type':'module'})
            return result
        self.fs.publish=changed
        with self.assertRaisesRegex(h.Stop,'RESOURCE_DRIFT'):self.run_delivery()
        self.assertEqual(self.api.resources[-1]['id'],'concurrent')
        self.assertEqual(sum(x['type'] in h.MUTATIONS for x in self.api.calls),0)

    def test_restoration_failure_is_not_retried(self):
        for target in h.FILES.values():self.fs.write_new(target,b'old',0o644)
        self.plan['before_files']={p:self.fs.snapshot(p,0o644) for p in h.FILES.values()}
        self.run_delivery();journal=self.fs.load()
        self.api.config=copy.deepcopy(journal['observation']['config']);self.api.resources=copy.deepcopy(journal['observation']['resources'])
        self.fs.fail=lambda p:p.startswith('PUBLISH:')
        with self.assertRaises(OSError):self.driver.restore_files(recovery_reference='SEPARATE_APPROVED_RECOVERY')
        self.assertEqual(self.fs.load()['state'],'RESTORING');self.assertIsNotNone(self.fs.load()['pending'])
        with self.assertRaisesRegex(h.Stop,'RECOVERY_ADJUDICATION_REQUIRED'):
            self.driver.restore_files(recovery_reference='SEPARATE_APPROVED_RECOVERY')

    def test_disabled_existing_integration_creates_no_services_or_listeners(self):
        spec=importlib.util.spec_from_file_location('existing_ha_disabled',ROOT/'homeassistant/custom_components/hioc_operator/__init__.py')
        bridge=importlib.util.module_from_spec(spec);spec.loader.exec_module(bridge)
        hass=Mock()
        loop=asyncio.new_event_loop()
        try:
            with patch.object(bridge,'Client',side_effect=AssertionError('NO_CLIENT')), \
                 patch.object(bridge,'ObservationClient',side_effect=AssertionError('NO_CLIENT')), \
                 patch('socket.create_connection',side_effect=AssertionError('NO_NETWORK')), \
                 patch('http.client.HTTPSConnection',side_effect=AssertionError('NO_NETWORK')):
                self.assertTrue(loop.run_until_complete(bridge.async_setup(hass,{'hioc_operator':{
                    'operator':{'enabled':False},'notifications':{'enabled':False},'observations':{'enabled':False}}})))
        finally:
            loop.close()
        self.assertEqual(hass.mock_calls,[])


class GovernanceAndAssessmentTests(unittest.TestCase):
    def test_existing39_successor449_protected_identities(self):
        record=json.loads((ROOT/'governance/pe7/pe7-implementation-candidate.json').read_bytes())
        self.assertEqual(len(record['artifacts']),39);self.assertEqual(len(record['protected']),449)
        for entry in record['artifacts']+record['protected']:
            raw=(ROOT/entry['path']).read_bytes()
            self.assertEqual(h.sha(raw),entry['file_sha256'],entry['path'])
            self.assertEqual(h.sha(raw.replace(b'\r\n',b'\n')),entry['sha256'],entry['path'])
        self.assertEqual(h.sha((ROOT/'tools/hioc-pe73-pi3-delivery.py').read_bytes()),
            '76b422edc73ed87baba94fef6fcfa8e197a564d4d8f57c95dba6b8a1624907d2')
        self.assertEqual(h.sha((ROOT/'tools/pe73_maintenance_window.py').read_bytes()),
            '756eb3ad2c43047a60a43398afb4c34d165dad8729803099dc367da90f1bd741')

    def test13_delivery_and6_ha_pins_match_immutable_objects(self):
        self.assertEqual(len(existing.d.MANIFEST),13)
        for item in existing.d.MANIFEST:self.assertEqual(h.sha(existing.SOURCE[item['path']]),item['sha256'])
        self.assertEqual(len(h.artifacts(lambda release,p:SOURCE[p])),6)

    def test_assessment_has_no_import_or_configuration_content_execution(self):
        spec=importlib.util.spec_from_file_location('pe73_assessment_test',ROOT/'tools/pe73_ha_assess.py')
        assess=importlib.util.module_from_spec(spec);spec.loader.exec_module(assess)
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);config=root/'config';package=root/'homeassistant';config.mkdir();package.mkdir()
            (config/'configuration.yaml').write_text('SECRET_CONTENT_NOT_TO_BE_READ')
            for p in ('components/lovelace/websocket.py','components/lovelace/resources.py',
                'components/lovelace/__init__.py','components/frontend/__init__.py','components/websocket_api/connection.py','core.py'):
                target=package/p;target.parent.mkdir(parents=True,exist_ok=True)
                target.write_text("raise RuntimeError('SOURCE_MUST_NOT_EXECUTE')\n")
            before={str(p):p.read_bytes() for p in root.rglob('*') if p.is_file()}
            result=assess.assess(config,package)
            self.assertEqual(result['RESULT'],'READ_ONLY_ASSESSMENT')
            self.assertNotIn('SECRET_CONTENT_NOT_TO_BE_READ',json.dumps(result))
            self.assertEqual(before,{str(p):p.read_bytes() for p in root.rglob('*') if p.is_file()})
            self.assertEqual(result['live_api_capabilities'],'NOT_ESTABLISHED_BY_STATIC_SOURCE')


class RootOps:
    """Real Windows files/descriptors plus explicit POSIX directory/owner/ACL model.

    Directory fsync, UID/GID and renameat2 semantics are modeled, not Linux proof.
    No credentials, container, host permission or production path is involved.
    """
    name='posix'
    O_RDONLY=os.O_RDONLY;O_WRONLY=os.O_WRONLY;O_CREAT=os.O_CREAT;O_EXCL=os.O_EXCL
    O_DIRECTORY=0x10000000;O_NOFOLLOW=0x20000000;O_CLOEXEC=0x40000000;O_NONBLOCK=0x08000000
    def __init__(self, root):
        self.root=root;self.fds={};self.nextfd=-1;self.attrs={};self.log=[];self.acl={};self.fail=None
        for name in ('homeassistant/custom_components/hioc_operator','homeassistant/www','homeassistant/backups'):
            (root/name).mkdir(parents=True,exist_ok=True)
    def getuid(self):return 0
    geteuid=getuid;getgid=getuid;getegid=getuid
    def actual(self,path,dir_fd=None):
        value=str(path)
        if dir_fd is not None:value=self.fds[dir_fd][0].rstrip('/')+'/'+value
        return value,self.root/value.lstrip('/')
    def info(self, info):
        key=(info.st_dev,info.st_ino)
        default=(0,0,0o755 if stat.S_ISDIR(info.st_mode) else 0o600)
        uid,gid,mode=self.attrs.get(key,default)
        return types.SimpleNamespace(st_dev=info.st_dev,st_ino=info.st_ino,st_uid=uid,st_gid=gid,
            st_mode=stat.S_IFMT(info.st_mode)|mode,st_nlink=info.st_nlink,st_size=info.st_size,
            st_mtime_ns=info.st_mtime_ns,st_ctime_ns=info.st_ctime_ns)
    def open(self,path,flags,mode=0o777,dir_fd=None):
        virtual,actual=self.actual(path,dir_fd)
        if flags&self.O_NOFOLLOW and actual.is_symlink():raise OSError(errno.ELOOP,'fixture')
        if flags&self.O_DIRECTORY:
            if not actual.is_dir():raise FileNotFoundError('fixture directory')
            fd=self.nextfd;self.nextfd-=1;self.fds[fd]=(virtual,actual);return fd
        realflags=flags&~(self.O_DIRECTORY|self.O_NOFOLLOW|self.O_CLOEXEC|self.O_NONBLOCK)
        if flags&os.O_CREAT:self.log.append(('create',virtual))
        fd=os.open(actual,realflags|os.O_BINARY if hasattr(os,'O_BINARY') else realflags,mode)
        self.fds[fd]=(virtual,actual);return fd
    def fstat(self,fd):
        value=self.info(self.fds[fd][1].lstat() if fd<0 else os.fstat(fd))
        if fd>=0:
            # Windows fstat may retain creation-time semantics for ctime while
            # pathname stat reports rename change-time. Model POSIX change-time
            # consistently, only when the same real inode is still named here.
            named=self.fds[fd][1].lstat()
            if (named.st_dev,named.st_ino)==(value.st_dev,value.st_ino):
                value.st_ctime_ns=named.st_ctime_ns
        return value
    def stat(self,path,dir_fd=None,follow_symlinks=False):return self.info(self.actual(path,dir_fd)[1].lstat())
    def getxattr(self,fd,name):
        code=self.acl.get(self.fds[fd][0])
        if code=='present':return b'fixture-acl'
        raise OSError(errno.EACCES if code=='unknown' else errno.ENODATA,'fixture')
    def close(self,fd):
        self.fds.pop(fd)
        if fd>=0:os.close(fd)
    def read(self,fd,size):return os.read(fd,size)
    def write(self,fd,raw):return os.write(fd,raw)
    def fsync(self,fd):
        if fd>=0:os.fsync(fd)
    def fchown(self,fd,uid,gid):
        info=self.fstat(fd);self.attrs[(info.st_dev,info.st_ino)]=(uid,gid,stat.S_IMODE(info.st_mode))
        self.log.append(('fchown',self.fds[fd][0],uid,gid))
    def fchmod(self,fd,mode):
        info=self.fstat(fd);self.attrs[(info.st_dev,info.st_ino)]=(info.st_uid,info.st_gid,mode)
        self.log.append(('fchmod',self.fds[fd][0],mode))
    def mkdir(self,path,mode,dir_fd):
        virtual,actual=self.actual(path,dir_fd);self.log.append(('mkdir',virtual));actual.mkdir()
        info=actual.stat();self.attrs[(info.st_dev,info.st_ino)]=(0,0,mode)
    def listdir(self,fd):return [p.name for p in self.fds[fd][1].iterdir()]
    def replace(self,src,dst,src_dir_fd,dst_dir_fd):
        if self.fail=='replace':raise OSError('fixture uncertain')
        self.log.append(('replace',self.actual(dst,dst_dir_fd)[0]))
        os.replace(self.actual(src,src_dir_fd)[1],self.actual(dst,dst_dir_fd)[1])
    def rename_new(self,fd,src,dst):
        if self.fail=='publish':raise OSError('fixture interrupted publication')
        if self.actual(dst,fd)[1].exists():raise FileExistsError('fixture')
        self.log.append(('rename_new',self.actual(dst,fd)[0]));self.replace(src,dst,fd,fd)
    def rmdir(self,path,dir_fd):
        self.log.append(('rmdir',self.actual(path,dir_fd)[0]));self.actual(path,dir_fd)[1].rmdir()
    def unlink(self,path,dir_fd):
        self.log.append(('unlink',self.actual(path,dir_fd)[0]));self.actual(path,dir_fd)[1].unlink()


class Probe:
    def __init__(self,ops,core_uid=1000,core_gid=1000):
        dirs={}
        for p in [ops.root,*[p for p in ops.root.rglob('*') if p.is_dir()]]:
            name='/'+p.relative_to(ops.root).as_posix()
            if name=='/.':name='/'
            dirs[name]=h._anchor(ops.info(p.stat()))
        self.value={'root':'/homeassistant','publisher_uid':0,'publisher_gid':0,
            'core':{'pid':42,'uid':core_uid,'gid':core_gid},'directories':dirs,
            'core_container':{'id':'core','image':'fixture-image'},'boot_id':'fixture-boot'}
        self.ops=ops;self.dynamic=False
        self.value['core_filesystem']={'anchors':{p:copy.deepcopy(dirs.get('/homeassistant'+('/'+p if p else '')))  for p in ('','custom_components','custom_components/hioc_operator','www','backups')},'process_birth':{'pid':42,'start_ticks':1}}
    def collect(self):
        value=copy.deepcopy(self.value)
        if self.dynamic:
            for relative in ('backups','custom_components/hioc_operator'):
                absolute='/homeassistant/'+relative;p=self.ops.root/absolute.lstrip('/')
                if p.exists():
                    item=h._anchor(self.ops.info(p.stat()));value['directories'][absolute]=item
                    value['core_filesystem']['anchors'][relative]=item
                else:
                    value['directories'].pop(absolute,None);value['core_filesystem']['anchors'][relative]=None
        return value


class HAOSPublisherTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.ops=RootOps(Path(self.temp.name));self.probe=Probe(self.ops)
        self.fs=h._ScopedHAFileSystem(self.probe,_ops=self.ops);self.api=API()
        self.guard={'host_identity':'qualified-fixture','disabled':True,'exclusive_delivery':True,
            'resources_loaded':True,'local_mapping':True,'storage_dashboard':True,'capability_identity':'fixture'}
        self.trust={'identity':'fixture','ha_private_files':True,'backend_private_files':True,
            'certificate_pair':True,'assertion_pair':True,'spki_pin':True,'independent_acl':True}
        self.driver=h.Delivery(self.fs,self.api,lambda:copy.deepcopy(self.guard),lambda _:self.trust,
            lambda release,p:SOURCE[p], route_probe=lambda url,expected: {'url':url,'sha256':expected,'status':200,'identity_encoding':True})
        ha,backend=configs()
        self.plan={'resource_url':'/local/hioc-asset-editor.js','dashboard':'hioc-dashboard-v2','view':'hioc-v2-inventory',
            'ha_trust':ha,'backend_trust':backend,'before_files':{p:self.fs.snapshot(p,0o644) for p in h.FILES.values()}}
    def run_delivery(self):return self.driver.run(self.plan,whole_process_reference='ONE_APPROVED_HAOS_PROCESS')
    def test_root_publisher_distinct_core_owner_and_private_records(self):
        self.assertEqual(self.run_delivery()['state'],'DELIVERED_DISABLED')
        for p in h.FILES.values():
            snap=self.fs.snapshot(p,0o644);self.assertEqual((snap['identity']['uid'],snap['identity']['gid']),(1000,1000))
        private=self.fs.snapshot(h.TX+'/journal.json',0o600)
        self.assertEqual((private['identity']['uid'],private['identity']['gid']),(0,0))
        self.assertTrue(all('.pe73-ha-' in row[1] for row in self.ops.log if row[0]=='fchown'))
        self.assertFalse(self.ops.fds)
    def test_core_root_is_not_inferred_from_publisher_but_can_be_qualified(self):
        self.probe=Probe(self.ops,core_uid=0,core_gid=0)
        self.fs=h._ScopedHAFileSystem(self.probe,_ops=self.ops)
        self.driver.fs=self.fs;self.plan['before_files']={p:self.fs.snapshot(p,0o644) for p in h.FILES.values()}
        self.run_delivery()
        self.assertEqual(self.fs.snapshot(next(iter(h.FILES.values())),0o644)['identity']['uid'],0)
        self.assertFalse(any(x[0]=='fchown' for x in self.ops.log))
    def test_no_mutation_before_explicit_process_and_live_identity(self):
        with self.assertRaises(h.Stop):self.fs.begin(h.TX)
        self.assertEqual(self.ops.log,[])
    def test_no_arbitrary_root_or_owner_factory_arguments(self):
        with self.assertRaises(TypeError):h.native_filesystem('/etc')
    def test_missing_destination_prerequisite_no_creation(self):
        del self.probe.value['directories']['/homeassistant/www']
        with self.assertRaisesRegex(h.Stop,'PREREQUISITE'):h._ScopedHAFileSystem(self.probe,_ops=self.ops)
        self.assertEqual(self.ops.log,[])
    def test_unknown_core_identity_no_creation(self):
        self.probe.value['core']['uid']='unknown'
        with self.assertRaises(h.Stop):h._ScopedHAFileSystem(self.probe,_ops=self.ops)
        self.assertEqual(self.ops.log,[])
    def test_matching_mount_strings_do_not_replace_core_descriptor_proof(self):
        del self.probe.value['core_filesystem']
        with self.assertRaisesRegex(h.Stop,'CORE_VISIBLE_IDENTITY'):h._ScopedHAFileSystem(self.probe,_ops=self.ops)
        self.assertEqual(self.ops.log,[])
    def test_process_identity_drift_before_begin_no_creation(self):
        self.ops.geteuid=lambda:1000
        with self.assertRaisesRegex(h.Stop,'PUBLISHER_IDENTITY'):self.run_delivery()
        self.assertEqual(self.ops.log,[])
    def test_core_mount_or_boot_drift_no_creation(self):
        self.probe.value['boot_id']='changed'
        with self.assertRaisesRegex(h.Stop,'CONTEXT_DRIFT'):self.run_delivery()
        self.assertEqual(self.ops.log,[])
    def test_parent_identity_drift_is_rejected(self):
        self.fs._dirs['/homeassistant/www']['inode']+=1
        with self.assertRaisesRegex(h.Stop,'DIRECTORY_IDENTITY'):self.fs.snapshot('www/hioc-asset-editor.js',0o644)
        self.assertEqual(self.ops.log,[])
    def test_unsafe_parent_permissions_refused(self):
        p=self.ops.root/'homeassistant/www';info=p.stat();self.ops.attrs[(info.st_dev,info.st_ino)]=(0,0,0o777)
        with self.assertRaises(h.Stop):self.run_delivery()
        self.assertEqual(self.ops.log,[])
    def test_parent_permission_change_during_operation_is_detected(self):
        p=self.ops.root/'homeassistant/www';info=p.stat()
        with self.assertRaisesRegex(h.Stop,'DIRECTORY_SECURITY_DRIFT'):
            with self.fs._directory('www'):
                self.ops.attrs[(info.st_dev,info.st_ino)]=(0,0,0o777)
        self.assertFalse(self.ops.fds)
    def test_parent_acl_change_during_operation_is_detected(self):
        with self.assertRaisesRegex(h.Stop,'ACL_PRESENT'):
            with self.fs._directory('www'):
                self.ops.acl['/homeassistant/www']='present'
        self.assertFalse(self.ops.fds)
    def test_acl_present_and_unknown_both_fail_before_mutation(self):
        for value in ('present','unknown'):
            self.ops.acl['/homeassistant']=value
            with self.assertRaises(h.Stop):self.driver.observe(self.plan)
        self.assertEqual(self.ops.log,[])
    def test_only_closed_paths_and_private_names_admitted(self):
        for target in ('/etc/passwd','../state/assets.json','state/assets.json','configuration.yaml',
                       '.storage/lovelace',h.TX+'/arbitrary','www/other.js'):
            with self.assertRaises(h.Stop):self.fs.write_new(target,b'x')
        self.assertEqual(self.ops.log,[])
    def test_arbitrary_public_payload_refused(self):
        self.run_delivery();target=next(iter(h.FILES.values()))
        with self.assertRaisesRegex(h.Stop,'PAYLOAD_NOT_PINNED'):self.fs.publish(target,b'new-unapproved',self.fs.snapshot(target,0o644),0o644)
    def test_private_records_cannot_become_world_readable(self):
        self.run_delivery()
        with self.assertRaises(h.Stop):self.fs.write_new(h.TX+'/stage-0',b'x',0o644)
    def test_hardlinked_destination_refused_without_chown(self):
        relative=next(iter(h.FILES.values()));p=self.ops.root/'homeassistant'/relative;p.write_bytes(b'old')
        info=p.stat();self.ops.attrs[(info.st_dev,info.st_ino)]=(1000,1000,0o644)
        os.link(p,self.ops.root/'hardlink-fixture')
        with self.assertRaisesRegex(h.Stop,'UNSAFE_REGULAR_FILE'):self.fs.snapshot(relative,0o644)
        self.assertEqual(self.ops.log,[])
    def test_wrong_public_owner_is_not_fixed_in_place(self):
        relative=next(iter(h.FILES.values()));p=self.ops.root/'homeassistant'/relative;p.write_bytes(b'old')
        info=p.stat();self.ops.attrs[(info.st_dev,info.st_ino)]=(0,0,0o644)
        with self.assertRaisesRegex(h.Stop,'OWNER_OR_MODE'):self.fs.snapshot(relative,0o644)
        self.assertEqual(self.ops.log,[])
    def test_symlink_file_type_rejected(self):
        relative=next(iter(h.FILES.values()));p=self.ops.root/'homeassistant'/relative;p.write_bytes(b'old')
        original=self.ops.fstat
        def changed(fd):
            info=original(fd)
            if fd>=0:info.st_mode=stat.S_IFLNK|0o644
            return info
        self.ops.fstat=changed
        with self.assertRaisesRegex(h.Stop,'UNSAFE_REGULAR_FILE'):self.fs.snapshot(relative,0o644)
        self.assertEqual(self.ops.log,[])
    def test_existing_backup_and_root_recovery_preserve_exact_bytes(self):
        for relative in h.FILES.values():
            p=self.ops.root/'homeassistant'/relative;p.write_bytes(b'previous approved code')
            info=p.stat();self.ops.attrs[(info.st_dev,info.st_ino)]=(1000,1000,0o644)
        self.plan['before_files']={p:self.fs.snapshot(p,0o644) for p in h.FILES.values()}
        self.run_delivery();j=self.fs.load()
        self.api.resources=copy.deepcopy(j['observation']['resources']);self.api.config=copy.deepcopy(j['observation']['config'])
        self.driver.restore_files(recovery_reference='SEPARATE_APPROVED_RECOVERY')
        for relative in h.FILES.values():self.assertEqual(self.fs.read(relative,0o644),b'previous approved code')
        self.assertEqual(self.fs.read(h.TX+'/before-0'),b'previous approved code')
    def test_no_per_operation_human_prompts(self):
        with patch('builtins.input',side_effect=AssertionError('NO_PROMPTS')):self.run_delivery()
    def test_root_private_journal_failure_leaves_evidence_no_runtime_install(self):
        self.ops.fail='replace'
        with self.assertRaises(OSError):self.run_delivery()
        self.assertTrue((self.ops.root/'homeassistant'/h.TX/'journal-next').exists())
        self.assertTrue(all(not self.fs.snapshot(p,0o644)['exists'] for p in h.FILES.values()))
        before=list(self.ops.log)
        with self.assertRaises(h.Stop):self.run_delivery()
        self.assertEqual(self.ops.log,before)
    def test_partial_publication_preserves_durable_pending_no_retry(self):
        self.ops.fail='publish'
        with self.assertRaises(OSError):self.run_delivery()
        self.assertEqual(self.fs.load()['pending'],next(iter(h.FILES.values())))
        writes=len(self.ops.log)
        with self.assertRaises(h.Stop):self.run_delivery()
        self.assertEqual(writes,len(self.ops.log))
    def test_lost_api_ack_never_retries_or_releases(self):
        self.api.fail='lovelace/resources/create:after'
        with self.assertRaises(OSError):self.run_delivery()
        self.assertEqual(self.fs.load()['pending'],'resource')
        self.assertEqual(sum(x['type']=='lovelace/resources/create' for x in self.api.calls),1)
    def test_private_journal_external_drift_cannot_be_overwritten(self):
        self.run_delivery();target=self.ops.root/'homeassistant'/h.TX/'journal.json'
        target.write_bytes(b'{}')
        with self.assertRaisesRegex(h.Stop,'JOURNAL_EXTERNAL_DRIFT'):self.fs.save(self.driver.last)
    def test_explicit_recovery_removes_only_own_verified_artifacts(self):
        self.run_delivery();j=self.fs.load()
        self.api.resources=copy.deepcopy(j['observation']['resources']);self.api.config=copy.deepcopy(j['observation']['config'])
        self.driver.restore_files(recovery_reference='SEPARATE_APPROVED_RECOVERY')
        self.assertEqual(self.fs.load()['state'],'FILES_RESTORED')
        self.assertTrue(all(not self.fs.snapshot(p,0o644)['exists'] for p in h.FILES.values()))
    def test_fresh_session_can_inspect_then_explicitly_recover_verified_terminal_state(self):
        self.run_delivery();j=self.fs.load()
        fresh=h._ScopedHAFileSystem(self.probe,_ops=self.ops)
        self.assertEqual(fresh.load(),j)
        before=list(self.ops.log)
        with self.assertRaisesRegex(h.Stop,'EXPLICIT_DISPOSITION'):
            fresh.authorize_process('ANOTHER_NORMAL_PROCESS','a'*64)
        self.assertEqual(self.ops.log,before)
        self.api.resources=copy.deepcopy(j['observation']['resources']);self.api.config=copy.deepcopy(j['observation']['config'])
        self.driver.fs=fresh
        self.driver.restore_files(recovery_reference='EXPLICIT_FRESH_RECOVERY')
        self.assertEqual(fresh.load()['state'],'FILES_RESTORED')
        self.assertEqual(fresh.load()['recovery_reference'],'EXPLICIT_FRESH_RECOVERY')
    def test_fresh_session_never_adopts_pending_or_incomplete_mutation(self):
        self.ops.fail='publish'
        with self.assertRaises(OSError):self.run_delivery()
        fresh=h._ScopedHAFileSystem(self.probe,_ops=self.ops)
        self.assertIsNotNone(fresh.load()['pending']);before=list(self.ops.log)
        with self.assertRaisesRegex(h.Stop,'UNCERTAIN_RECOVERY_REFUSED'):
            fresh.authorize_recovery('EXPLICIT_RECOVERY_CANNOT_OVERRIDE_UNCERTAINTY')
        self.assertEqual(self.ops.log,before)
    def test_long_term_runtime_and_persistent_state_independent(self):
        for relative in ('state/assets.json','state/history.json','notes.txt','configuration.yaml','.storage/other'):
            p=self.ops.root/'homeassistant'/relative;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'operator knowledge preserved')
        before={str(p):p.read_bytes() for p in (self.ops.root/'homeassistant').rglob('*') if p.is_file()}
        self.run_delivery()
        for name,value in before.items():self.assertEqual(Path(name).read_bytes(),value)
        for source in h.FILES:self.assertNotIn(b'pe73_ha_delivery',SOURCE[source]);self.assertNotIn(h.TX.encode(),SOURCE[source])
        self.assertFalse(any(x['type'] not in h.READS+h.MUTATIONS for x in self.api.calls))
    def test_no_ha_version_equality_gate(self):
        source=(ROOT/'tools/pe73_ha_delivery.py').read_text(encoding='utf-8')
        self.assertNotIn('2026.10.4',source)


    def absent_directories(self, *names):
        for relative in names:(self.ops.root/'homeassistant'/relative).rmdir()
        self.probe=Probe(self.ops);self.probe.dynamic=True
        self.fs=h._ScopedHAFileSystem(self.probe,_ops=self.ops);self.driver.fs=self.fs
        self.plan['before_files']={p:self.fs.snapshot(p,0o644) for p in h.FILES.values()}
    def test_new_integration_directory_needs_no_manual_creation(self):
        self.absent_directories('custom_components/hioc_operator')
        self.assertEqual(self.fs.children('custom_components/hioc_operator'),[])
        self.assertEqual(self.run_delivery()['state'],'DELIVERED_DISABLED')
        j=self.fs.load();self.assertEqual(j['created_directories'][0]['path'],'custom_components/hioc_operator')
        self.assertEqual(j['created_directories'][0]['identity']['mode'],0o755)
        events=self.ops.log
        first_journal=next(i for i,x in enumerate(events) if x==('replace','/homeassistant/'+h.TX+'/journal.json'))
        create=events.index(('mkdir','/homeassistant/custom_components/hioc_operator'))
        self.assertLess(first_journal,create)
    def test_missing_backup_parent_has_private_durable_bootstrap(self):
        self.absent_directories('custom_components/hioc_operator','backups')
        self.run_delivery()
        intent=json.loads(self.fs.read(h.BOOTSTRAP));self.assertEqual(intent['state'],'DIRECTORY_CREATE_INTENT')
        self.assertEqual(intent['path'],'backups')
        self.assertEqual(self.fs.snapshot(h.BOOTSTRAP)['identity']['mode'],0o600)
        self.assertEqual([x['path'] for x in self.fs.load()['created_directories']],['backups','custom_components/hioc_operator'])
        self.assertLess(self.ops.log.index(('create','/homeassistant/'+h.BOOTSTRAP)),self.ops.log.index(('mkdir','/homeassistant/backups')))
    def test_directory_creation_failure_retains_pending_and_no_retry(self):
        self.absent_directories('custom_components/hioc_operator');original=self.ops.mkdir
        def fail(name,mode,dir_fd):
            if name=='hioc_operator':raise OSError('creation uncertain')
            return original(name,mode,dir_fd)
        self.ops.mkdir=fail
        with self.assertRaises(OSError):self.run_delivery()
        self.assertEqual(self.fs.load()['pending'],'custom_components/hioc_operator')
        before=list(self.ops.log)
        with self.assertRaises(h.Stop):self.run_delivery()
        self.assertEqual(before,self.ops.log)
    def test_bootstrap_interruption_cannot_be_auto_adopted(self):
        self.absent_directories('backups');original=self.ops.mkdir
        def fail(name,mode,dir_fd):
            if name=='backups':raise OSError('creation uncertain')
            return original(name,mode,dir_fd)
        self.ops.mkdir=fail
        with self.assertRaises(OSError):self.run_delivery()
        self.assertTrue(self.fs.snapshot(h.BOOTSTRAP)['exists'])
        fresh=h._ScopedHAFileSystem(self.probe,_ops=self.ops);before=list(self.ops.log)
        with self.assertRaisesRegex(h.Stop,'EXPLICIT_DISPOSITION'):fresh.authorize_process('DO_NOT_RETRY','a'*64)
        self.assertEqual(before,self.ops.log)
    def test_substituted_absent_directory_refused_before_transaction(self):
        self.absent_directories('custom_components/hioc_operator')
        (self.ops.root/'homeassistant/custom_components/hioc_operator').mkdir()
        with self.assertRaises(h.Stop):self.run_delivery()
        self.assertEqual(self.ops.log,[])
    def test_directory_creation_cannot_target_persistent_or_arbitrary_paths(self):
        for path in ('state','configuration.yaml','www','custom_components','../other'):
            with self.assertRaises(h.Stop):self.fs._create_directory(path,0o755)
        self.assertEqual(self.ops.log,[])
    def test_exact_created_directory_removed_only_by_explicit_recovery(self):
        self.absent_directories('custom_components/hioc_operator');self.run_delivery();j=self.fs.load()
        self.api.resources=copy.deepcopy(j['observation']['resources']);self.api.config=copy.deepcopy(j['observation']['config'])
        self.driver.restore_files(recovery_reference='EXPLICIT_DIRECTORY_RECOVERY')
        self.assertFalse((self.ops.root/'homeassistant/custom_components/hioc_operator').exists())
        self.assertEqual(self.fs.load()['removed_created_directory']['path'],'custom_components/hioc_operator')
    def test_fresh_directory_recovery_uses_recorded_identity(self):
        self.absent_directories('custom_components/hioc_operator');self.run_delivery();j=self.fs.load()
        self.api.resources=copy.deepcopy(j['observation']['resources']);self.api.config=copy.deepcopy(j['observation']['config'])
        self.driver.fs=h._ScopedHAFileSystem(self.probe,_ops=self.ops)
        self.driver.restore_files(recovery_reference='FRESH_DIRECTORY_RECOVERY')
        self.assertFalse((self.ops.root/'homeassistant/custom_components/hioc_operator').exists())
    def test_existing_integration_directory_never_removed_by_recovery(self):
        self.run_delivery();j=self.fs.load()
        self.api.resources=copy.deepcopy(j['observation']['resources']);self.api.config=copy.deepcopy(j['observation']['config'])
        self.driver.restore_files(recovery_reference='PRESERVE_EXISTING_DIRECTORY')
        self.assertTrue((self.ops.root/'homeassistant/custom_components/hioc_operator').is_dir())
        self.assertFalse(any(x[0]=='rmdir' for x in self.ops.log))


class NativeBindingTests(unittest.TestCase):
    def setUp(self):
        spec=importlib.util.spec_from_file_location('assessment_binding_test',ROOT/'tools/pe73_ha_assess.py')
        self.a=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.a)
        self.core={'id':'core','running':True,'userns':'','mounts':[{'Destination':'/config','Source':'/actual/core-config','RW':True,'Type':'bind'}]}
        self.term={'id':'term','running':True,'userns':'','mounts':[{'Destination':'/homeassistant','Source':'/actual/core-config','RW':True,'Type':'bind'}]}
        self.meta=lambda root:{'device':1,'inode':2}
    def test_exact_source_root_binding(self):self.assertEqual(self.a.bind_mounts(self.term,self.core,self.meta),'/homeassistant')
    def test_addon_config_is_not_automatically_core_config(self):
        self.term['mounts'][0]['Source']='/addon-private-config'
        with self.assertRaises(self.a.QualificationError):self.a.bind_mounts(self.term,self.core,self.meta)
    def test_idmapped_or_unknown_user_namespace_rejected(self):
        self.core['userns']='remapped'
        with self.assertRaises(self.a.QualificationError):self.a.bind_mounts(self.term,self.core,self.meta)
    def test_nested_mount_cannot_redirect_delivery(self):
        self.core['mounts'].append({'Destination':'/config/www','Source':'/different'})
        with self.assertRaises(self.a.QualificationError):self.a.bind_mounts(self.term,self.core,self.meta)
    def test_distinct_aliases_conflict(self):
        self.term['mounts'].append(dict(self.term['mounts'][0],Destination='/config'))
        with self.assertRaises(self.a.QualificationError):self.a.bind_mounts(self.term,self.core,lambda p:{'device':1,'inode':1 if p=='/config' else 2})
    def test_actual_numeric_core_process_identity(self):
        self.assertEqual(self.a.core_identity('PID UID GID COMMAND\n42 123 456 python3.13\n'),{'pid':42,'uid':123,'gid':456})
    def test_multiple_python_processes_do_not_guess_owner(self):
        with self.assertRaises(self.a.QualificationError):self.a.core_identity('PID UID GID COMMAND\n42 0 0 python3\n43 1000 1000 python3\n')
    def test_preflight_failure_is_sanitized_and_read_only(self):
        probe=Mock();probe.collect.side_effect=OSError('private-sensitive-value')
        value=self.a.preflight(probe)
        self.assertEqual(value['RESULT'],'BLOCKED_READ_ONLY_QUALIFICATION');self.assertNotIn('sensitive',json.dumps(value))
        self.assertFalse(value['mutation_performed'])
    def core_report(self):
        dirs={str(Path('/homeassistant')/p):{'device':7,'inode':i+10,'uid':0,'gid':0,'mode':0o755}
            for i,p in enumerate(('','custom_components','www'))}
        anchors={p:dirs.get(str(Path('/homeassistant')/p)) for p in ('','custom_components','custom_components/hioc_operator','www','backups')}
        value={'schema':'PE73_CORE_FILESYSTEM_V1','process':{'local_pid':32,'start_ticks':123,
            'uid':0,'gid':0,'user_namespace':'user:[1]'},'anchors':anchors,
            'helper_uid':0,'helper_gid':0,'read_only':True}
        return dirs,value
    def core_call(self,value=None,*,top='731186 0 0 python3'):
        dirs,default=self.core_report();value=default if value is None else value
        probe=self.a.NativeProbe();calls=[]
        def docker(*args):
            calls.append(args)
            return json.dumps(value) if args[1]=='exec' else 'PID UID GID COMMAND\n'+top+'\n'
        probe.docker=docker
        with patch.object(self.a.os,'readlink',return_value='user:[1]'),patch.object(self.a.Path,'read_text',side_effect=FileNotFoundError(2,'isolated PID namespace')):
            result=probe.core_filesystem({'pidmode':''},{'pid':731186,'uid':0,'gid':0},'/homeassistant',dirs,'a'*64)
        return result,calls
    def test_isolated_pid_namespace_uses_only_fixed_metadata_exec(self):
        result,calls=self.core_call()
        self.assertEqual(result['process_birth']['local_pid'],32)
        self.assertEqual(result['process_birth']['host_pid'],731186)
        self.assertEqual(calls[0],('container','exec','--user','0:0','--workdir','/','a'*64,
            'python3','-I','-S','-B','-c',self.a.CORE_FS_PROBE))
        self.assertEqual(len(calls),2)
    def test_core_cannot_read_private_parent_by_assumed_root_bypass(self):
        with tempfile.TemporaryDirectory() as temp:
            ops=RootOps(Path(temp));p=ops.root/'homeassistant';info=p.stat()
            ops.attrs[(info.st_dev,info.st_ino)]=(0,0,0o700)
            with patch.object(self.a,'os',ops):
                with self.assertRaisesRegex(self.a.QualificationError,'CORE_TRAVERSAL'):
                    self.a.directory_chain('/homeassistant/www',1000,1000)
            self.assertEqual(ops.log,[])
    def test_exact_public_ancestry_readability_without_mutations(self):
        with tempfile.TemporaryDirectory() as temp:
            ops=RootOps(Path(temp))
            with patch.object(self.a,'os',ops):
                result=self.a.directory_chain('/homeassistant/www',1000,1000)
            self.assertIn('/homeassistant/www',result);self.assertEqual(ops.log,[]);self.assertFalse(ops.fds)


    def process_fixture(self, *, groups=None, uid=1000):
        pid=42;core='a'*64
        statrow='42 (python3) '+' '.join(['S']+['0']*18+['123']+['0']*20)
        values={'stat':statrow,'status':f'Uid: {uid} {uid} {uid} {uid}\nGid: 1000 1000 1000 1000\n',
            'cgroup':'0::/docker/'+(core if groups is None else groups)+'\n'}
        return core,{'pid':pid,'uid':1000,'gid':1000},lambda path:values[path.name]
    def test_private_pid_mode_is_not_a_configuration_prerequisite(self):
        result,calls=self.core_call();self.assertEqual(result['anchors']['']['device'],7)
        source=(ROOT/'tools/pe73_ha_assess.py').read_text()
        self.assertNotIn("terminal.get('pidmode')=='host'",source)
        self.assertNotIn("base=Path('/proc')/str(identity['pid'])",source)
    def test_pid_number_collision_cannot_impersonate_core_container(self):
        result,calls=self.core_call();self.assertEqual(calls[0][6],'a'*64)
        self.assertEqual(result['process_birth']['container_id'],'a'*64)
        with self.assertRaisesRegex(self.a.QualificationError,'CONTAINER_ID_REQUIRED'):
            self.a.NativeProbe().core_filesystem({}, {'pid':731186,'uid':0,'gid':0},'/homeassistant',{},'homeassistant;bad')
    def test_hidden_terminal_cgroup_never_becomes_metadata_only_admission(self):
        dirs,value=self.core_report();value['anchors']['']['inode']+=1
        with self.assertRaisesRegex(self.a.QualificationError,'IDENTITY_CONFLICT'):self.core_call(value)
    def test_core_credential_drift_is_not_hidden_by_container_match(self):
        dirs,value=self.core_report();value['process']['uid']=1000
        with self.assertRaisesRegex(self.a.QualificationError,'CREDENTIAL_DRIFT'):self.core_call(value)
    def test_device_inode_mode_and_owner_mismatch_each_refused(self):
        for field in ('device','inode','uid','gid','mode'):
            dirs,value=self.core_report();value['anchors']['www'][field]+=1
            with self.subTest(field=field),self.assertRaisesRegex(self.a.QualificationError,'IDENTITY_CONFLICT'):
                self.core_call(value)
    def test_unexpected_core_directory_cannot_replace_proven_absence(self):
        dirs,value=self.core_report();value['anchors']['custom_components/hioc_operator']=value['anchors']['www']
        with self.assertRaisesRegex(self.a.QualificationError,'IDENTITY_CONFLICT'):self.core_call(value)
    def test_core_host_process_change_during_helper_refused(self):
        with self.assertRaisesRegex(self.a.QualificationError,'HOST_PROCESS_DRIFT'):self.core_call(top='731187 0 0 python3')
    def test_failed_or_partial_helper_proof_cannot_admit(self):
        for value in ({'RESULT':'BLOCKED'},{'schema':'PE73_CORE_FILESYSTEM_V1'},None):
            if value is None:
                dirs,value=self.core_report();value['read_only']=False
            with self.subTest(value=value),self.assertRaises(self.a.QualificationError):self.core_call(value)
    def test_core_user_namespace_mismatch_refused(self):
        dirs,value=self.core_report();value['process']['user_namespace']='user:[different]'
        with self.assertRaisesRegex(self.a.QualificationError,'NAMESPACE_NOT_IDENTICAL'):self.core_call(value)
    def test_fixed_helper_has_no_write_shell_network_or_ha_operation(self):
        import ast
        tree=ast.parse(self.a.CORE_FS_PROBE)
        banned={'write','unlink','rmdir','mkdir','chmod','fchmod','chown','fchown','replace','rename','system','popen','exec','eval','input','connect'}
        for node in ast.walk(tree):
            if isinstance(node,ast.Call):
                name=node.func.attr if isinstance(node.func,ast.Attribute) else node.func.id if isinstance(node.func,ast.Name) else ''
                self.assertNotIn(name,banned)
        imports=[alias.name for node in tree.body if isinstance(node,ast.Import) for alias in node.names]
        self.assertEqual(imports,['errno','json','os','re','stat'])
        self.assertNotIn('731186',self.a.CORE_FS_PROBE)
    def helper_capture(self,ops,*,drift=False):
        import ast
        tree=ast.parse(self.a.CORE_FS_PROBE)
        defs=[n for n in tree.body if isinstance(n,ast.FunctionDef)]
        scope={'os':ops,'json':json,'stat':stat,'errno':errno,'re':__import__('re')}
        exec(compile(ast.Module(body=defs,type_ignores=[]),'fixed-helper-functions','exec'),scope)
        birth={'local_pid':32,'start_ticks':123,'uid':0,'gid':0,'user_namespace':'user:[1]'}
        scope['local_python_processes']=lambda:[dict(birth)]
        scope['process']=lambda pid:dict(birth,start_ticks=124 if drift else 123)
        original=ops.open
        def opened(path,flags,mode=0o777,dir_fd=None):
            if path=='/proc/32/root':return original('/',flags,mode,dir_fd)
            if path=='config' and dir_fd is not None and ops.fds[dir_fd][0]=='/':return original('/homeassistant',flags,mode)
            return original(path,flags,mode,dir_fd)
        original_stat=ops.stat
        def stated(path,dir_fd=None,follow_symlinks=False):
            if path=='config' and dir_fd is not None and ops.fds[dir_fd][0]=='/':
                return original_stat('/homeassistant',follow_symlinks=follow_symlinks)
            return original_stat(path,dir_fd=dir_fd,follow_symlinks=follow_symlinks)
        ops.stat=stated
        ops.open=opened;ops.readlink=lambda path:'user:[1]'
        real_open=open
        def read_only_map(path,*args,**kwargs):
            if path in ('/proc/self/uid_map','/proc/self/gid_map'):
                return __import__('io').StringIO('0 0 4294967295\n')
            return real_open(path,*args,**kwargs)
        scope['open']=read_only_map
        return scope['capture']()
    def test_core_helper_actual_descriptors_readonly_and_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            ops=RootOps(Path(temp));value=self.helper_capture(ops)
            self.assertEqual(value['anchors']['']['inode'],(ops.root/'homeassistant').stat().st_ino)
            self.assertEqual(value['process']['local_pid'],32);self.assertEqual(ops.log,[]);self.assertFalse(ops.fds)
    def test_core_helper_acl_drift_and_process_restart_fail_closed(self):
        for failure in ('acl','restart'):
            with self.subTest(failure=failure),tempfile.TemporaryDirectory() as temp:
                ops=RootOps(Path(temp))
                if failure=='acl':ops.acl['/homeassistant/www']='present'
                with self.assertRaises(ValueError):self.helper_capture(ops,drift=failure=='restart')
                self.assertEqual(ops.log,[]);self.assertFalse(ops.fds)
    def test_private_backup_directory_does_not_require_core_traversal(self):
        with tempfile.TemporaryDirectory() as temp:
            ops=RootOps(Path(temp));p=ops.root/'homeassistant/backups';info=p.stat();ops.attrs[(info.st_dev,info.st_ino)]=(0,0,0o700)
            with patch.object(self.a,'os',ops):
                result=self.a.directory_chain('/homeassistant/backups',1000,1000,core_access=False)
            self.assertEqual(result['/homeassistant/backups']['mode'],0o700);self.assertEqual(ops.log,[])


if __name__ == '__main__':
    unittest.main()
