from test_pe4_ha_association_public_projection_test_binding_correction import current_artifact_bindings, verify_source_binding
"""Actual implementation tests; all Windows inputs synthetic, no production I/O."""
import ast
import copy
import errno
import importlib.util
import json
import os
from pathlib import Path
import stat
import tempfile
import types
import unittest
from unittest.mock import patch,Mock
from hioc import home_assistant_public_projection as h
from test_pe4_ha_association_public_projection_preparation import association,state,devices,canonical,PUBLIC_REJECTS,PRIVATE_REJECTS
from test_hostname_enrichment import load_engine_module,public_inventory
ROOT=Path(__file__).resolve().parents[1]
V,S,P=h.load_contracts(lambda p:(ROOT/p).read_bytes())


def inventory(count=3):return dict(devices=devices(count),summary={'untouched':True},schema_version='1.0')
def project(value,private_state):return h.attach_projection(value,h.derive_projection(value['devices'],private_state,V,S,P),V,P)


class PureTests(unittest.TestCase):
    def test_exact_allowlist_mapping_and_nonassociation_omission(self):
        out=project(inventory(),state([association()]))
        self.assertEqual(set(out['devices'][0]['home_assistant']),set(P['required']))
        self.assertTrue(out['devices'][0]['home_assistant']['associated'])
        self.assertEqual(out['devices'][0]['home_assistant']['association_basis'],'strong_mac')
        self.assertNotIn('home_assistant',out['devices'][1])

    def test_config_entry_source_only_sorted_unique_and_private_values_absent(self):
        a=association();a['entities']=[dict(entity_id='sensor.private_fixture',registry_id='registry_private',platform='platform_no_fallback')]
        a['config_entries']=[dict(entry_id='entry_'+str(i),domain=d) for i,d in enumerate(['zha','mqtt','zha'])]
        a['area_candidate']={'area_id':'private_area','name':'private name'}
        out=project(inventory(),state([a]))['devices'][0]['home_assistant']
        self.assertEqual(out['integration_domains'],['mqtt','zha']);self.assertEqual(out['entity_count'],1)
        self.assertTrue(out['has_area_candidate'])
        for secret in ['private','platform_no_fallback','2030','unique_mac','COMPLETE','synthetic-version']:self.assertNotIn(secret,canonical(out).decode())

    def test_incomplete_retained_members_and_optional_defaults(self):
        out=project(inventory(),state([association(complete=False)]))['devices'][0]['home_assistant']
        self.assertEqual(out,dict(associated=True,association_basis='strong_mac',entity_count=0,integration_domains=[],has_area_candidate=False))

    def test_history_current_id_ignored_and_missing_active_device_not_created(self):
        old={k:v for k,v in association().items() if k in ['hioc_device_id','ha_device_id','first_associated_at','last_confirmed_at']}
        old.update(first_associated_at='2029-01-01T00:00:00Z',last_confirmed_at='2029-01-02T00:00:00Z',retired_at='2029-01-03T00:00:00Z',retirement_reason='HA_DEVICE_ABSENT')
        self.assertEqual(project(inventory(),state([], [old])),inventory())
        self.assertEqual(project(inventory(),state([association(8)])),inventory())

    def test_authority_values_order_and_input_immutability(self):
        value=inventory();before=copy.deepcopy(value)
        out=project(value,state([association(2)]))
        self.assertEqual(h.strip_inventory(out),before);self.assertEqual(value,before)
        self.assertEqual([d['id'] for d in out['devices']],[d['id'] for d in before['devices']])

    def test_recomputation_strips_stale_and_injected_namespaces(self):
        value=inventory();value['devices'][0]['home_assistant']={'unsafe':True}
        self.assertEqual(project(value,state()),inventory())
        self.assertEqual(h.strip_inventory(value),inventory())
        self.assertIn('home_assistant',value['devices'][0])

    def test_duplicate_current_or_private_ids_rejected(self):
        with self.assertRaises(h.ProjectionError):project(dict(devices=[devices()[0],devices()[0]]),state([association()]))
        a=association(2);a['hioc_device_id']=association()['hioc_device_id']
        with self.assertRaises(Exception):project(inventory(),state([association(),a]))

    def test_atomic_attachment_all_objects_validated_before_any_changes(self):
        value=inventory();before=copy.deepcopy(value)
        with self.assertRaises(Exception):h.attach_projection(value,{devices()[0]['id']:{'private':'bad'}},V,P)
        self.assertEqual(value,before)
        a=association(2);a['config_entries']=[dict(entry_id='fixture',domain='deadbeefcafe')]
        with self.assertRaises(h.ProjectionError):project(value,state([association(),a]))
        self.assertEqual(value,before)

    def test_varied_counts_canonical_determinism(self):
        for count in [0,1,2,4,7]:
            a=[association(i) for i in range(1,count+1)]
            self.assertEqual(canonical(project(inventory(count),state(a))),canonical(project(inventory(count),state(list(reversed(a))))))

    def test_public_bounds(self):
        obj=dict(associated=True,association_basis='strong_mac',entity_count=65536,integration_domains=['a'+'b'*63],has_area_candidate=False)
        h.validate_public(obj,V,P)
        for key,value in [('entity_count',65537),('entity_count',-1),('entity_count',True),('integration_domains',['a'+'b'*64]),('integration_domains',['mqtt']*4097)]:
            bad=dict(obj);bad[key]=value
            with self.assertRaises(Exception):h.validate_public(bad,V,P)

    def test_module_schema_identities_before_private_code_execution(self):
        for changed in [h.MODULE_PATH,h.PRIVATE_SCHEMA_PATH,h.PUBLIC_SCHEMA_PATH]:
            def read(p):return b'untrusted code must never execute' if p==changed else (ROOT/p).read_bytes()
            with patch('builtins.compile',side_effect=AssertionError('private code executed')):
                with self.assertRaises(h.ProjectionError):h.load_contracts(read)

    def test_strict_snapshot_utf8_duplicates_nonfinite_and_oversize(self):
        for raw in [b'\xff',b'{"a":1,"a":1}',b'{"x":NaN}',b'{"x":Infinity}',b'x'*(h.LIMIT+1)]:
            with self.assertRaises(Exception):V.strict_json(raw,'CANDIDATE_STATE_VALIDATION')

    def test_import_ast_no_network_or_mutating_dependencies(self):
        tree=ast.parse((ROOT/'pi4/lib/hioc/home_assistant_public_projection.py').read_text())
        imports={n.module for n in ast.walk(tree) if isinstance(n,ast.ImportFrom)}|{a.name for n in ast.walk(tree) if isinstance(n,ast.Import) for a in n.names}
        self.assertFalse(imports&{'websockets','requests','jsonschema','socket','subprocess'})
        self.assertNotIn('fcntl',{a.name for n in tree.body if isinstance(n,ast.Import) for a in n.names})
        self.assertNotIn('integrations',(ROOT/'pi4/lib/hioc/home_assistant_public_projection.py').read_text())


def public_case(field,value):
    def test(self):
        obj=dict(associated=True,association_basis='strong_mac',entity_count=0,integration_domains=[],has_area_candidate=False);obj[field]=value
        with self.assertRaises(Exception):h.validate_public(obj,V,P)
    return test
for name,(field,value) in PUBLIC_REJECTS.items():setattr(PureTests,'test_public_reject_'+name,public_case(field,value))
def private_case(path,value):
    def test(self):
        candidate=state([association()]);node=candidate
        for k in path[:-1]:node=node[k]
        node[path[-1]]=value
        with self.assertRaises(Exception):project(inventory(),candidate)
    return test
for name,(path,value) in PRIVATE_REJECTS.items():setattr(PureTests,'test_private_reject_'+name,private_case(path,value))


class Entries:
    def __init__(self,names):self.names=names;self.count=0;self.closed=False
    def __enter__(self):return self
    def __exit__(self,*a):self.closed=True
    def __iter__(self):
        for name in self.names:self.count+=1;yield types.SimpleNamespace(name=name)


class FakeFS:
    def __init__(self):
        self.opened=set();self.closed=[];self.nextfd=0;self.fd={};self.fdinfo={};self.acquired=False;self.releases=0;self.locks=0
        def info(mode,ino,size=0):return types.SimpleNamespace(st_mode=mode,st_dev=1,st_ino=ino,st_uid=100,st_gid=200,st_nlink=1,st_size=size,st_mtime_ns=1,st_ctime_ns=1)
        self.raw=canonical(state([association()]))
        self.nodes={'root':info(stat.S_IFDIR|0o700,1),'associations':info(stat.S_IFDIR|0o700,2),'.home_assistant.lock':info(stat.S_IFREG|0o600,3),'home_assistant.json':info(stat.S_IFREG|0o600,4,len(self.raw))}
        self.names=[];self.entries_calls=0;self.iterators=[];self.busy=False;self.acl_bad=False;self.read_hook=None
    def allocate(self,name):
        self.nextfd+=1;self.fd[self.nextfd]=name;self.fdinfo[self.nextfd]=self.nodes[name];self.opened.add(self.nextfd);return self.nextfd
    def open_root(self,p):return self.allocate('root')
    def open_dir(self,p,n):return self.allocate(n)
    def open_file(self,p,n):
        if n not in self.nodes:raise FileNotFoundError()
        return self.allocate(n)
    def fstat(self,fd):return copy.copy(self.fdinfo[fd])
    def lstat(self,p,n):
        if n not in self.nodes:raise FileNotFoundError()
        return copy.copy(self.nodes[n])
    def acl(self,fd,directory=False):
        if self.acl_bad:raise h.ProjectionError('OMITTED_UNSAFE')
    def close(self,fd):self.opened.remove(fd);self.closed.append(fd)
    def read(self,fd,size):
        raw=self.raw
        if self.read_hook:self.read_hook(self)
        return raw[:size]
    def entries(self,fd):
        self.entries_calls+=1
        entries=Entries(self.names if not callable(self.names) else self.names(self.entries_calls));self.iterators.append(entries);return entries
    def flock(self,fd,acquire):
        if acquire:
            self.locks+=1
            if self.busy:raise BlockingIOError(errno.EAGAIN,'private secret')
            self.acquired=True
        else:self.acquired=False;self.releases+=1


class ReaderTests(unittest.TestCase):
    def read(self,fs,clock=None):
        with h.SecureReader('/associations',100,200,fs,**({'clock':clock} if clock else {})) as reader:return reader.snapshot()
    def test_success_releases_before_validation_and_closes_all(self):
        fs=FakeFS();raw=self.read(fs);self.assertEqual(raw,fs.raw);self.assertFalse(fs.opened);self.assertFalse(fs.acquired);self.assertEqual(fs.releases,1);self.assertEqual(fs.locks,1)
        V.validate_state(V.strict_json(raw,'CANDIDATE_STATE_VALIDATION'),S)
        self.assertTrue(all(i.closed for i in fs.iterators))
    def test_busy_no_wait_retry_or_unlock_unacquired(self):
        fs=FakeFS();fs.busy=True
        with self.assertRaises(h.ProjectionError) as e:self.read(fs)
        self.assertEqual(e.exception.code,'OMITTED_BUSY');self.assertEqual(fs.locks,1);self.assertEqual(fs.releases,0);self.assertFalse(fs.opened)
    def test_missing_state_and_lock_no_creation(self):
        for name in ['home_assistant.json','.home_assistant.lock']:
            fs=FakeFS();del fs.nodes[name]
            with self.assertRaises(FileNotFoundError):self.read(fs)
            self.assertFalse(fs.opened);self.assertFalse(fs.acquired)
    def test_acl_failure_fails_closed(self):
        fs=FakeFS();fs.acl_bad=True
        with self.assertRaises(h.ProjectionError):self.read(fs)
        self.assertFalse(fs.opened)
    def test_namespace_bounded_no_transaction_content_opened(self):
        fs=FakeFS();fs.names=['ordinary']*10000
        with self.assertRaises(h.ProjectionError):self.read(fs)
        self.assertEqual(fs.iterators[0].count,4097);self.assertTrue(fs.iterators[0].closed);self.assertFalse(fs.opened)
    def test_namespace_before_after_rejects_even_malformed_prefixes(self):
        for prefix in ['.home_assistant.txn-','.home_assistant.done-']:
            for when in [1,2]:
                fs=FakeFS();fs.names=lambda call:[prefix+'malformed'] if call==when else []
                with self.assertRaises(h.ProjectionError):self.read(fs)
                self.assertFalse(fs.opened);self.assertFalse(fs.acquired);self.assertEqual(fs.releases,1)
    def test_replacement_and_partial_copy_rejected(self):
        for change in ['st_ino','st_mtime_ns','st_ctime_ns','st_nlink','st_size']:
            fs=FakeFS();fs.read_hook=lambda fs:setattr(fs.nodes['home_assistant.json'],change,getattr(fs.nodes['home_assistant.json'],change)+1)
            with self.assertRaises(h.ProjectionError):self.read(fs)
            self.assertFalse(fs.opened);self.assertFalse(fs.acquired)
        fs=FakeFS();fs.raw=fs.raw[:-1]
        with self.assertRaises(h.ProjectionError):self.read(fs)
        self.assertFalse(fs.opened)
    def test_replaced_lock_and_parent_binding_are_rejected(self):
        for name in ['.home_assistant.lock','associations']:
            fs=FakeFS()
            def replace(fs):
                replacement=copy.copy(fs.nodes[name]);replacement.st_ino+=10;fs.nodes[name]=replacement
            fs.read_hook=replace
            with self.assertRaises(h.ProjectionError):self.read(fs)
            self.assertFalse(fs.opened);self.assertFalse(fs.acquired)
    def test_io_and_unlock_failures_attempt_all_cleanup(self):
        fs=FakeFS()
        def fail_read(*a):raise OSError('private text')
        fs.read=fail_read
        with self.assertRaises(OSError):self.read(fs)
        self.assertFalse(fs.opened);self.assertFalse(fs.acquired)
        fs=FakeFS();flock=fs.flock
        def fail_unlock(fd,acquire):
            flock(fd,acquire)
            if not acquire:raise OSError('private text')
        fs.flock=fail_unlock
        with self.assertRaises(OSError):self.read(fs)
        self.assertFalse(fs.opened);self.assertFalse(fs.acquired)
    def test_finite_deadline_always_releases_resources(self):
        fs=FakeFS();tick=[0]
        def clock():tick[0]+=1;return tick[0]
        with self.assertRaises(h.ProjectionError):self.read(fs,clock)
        self.assertFalse(fs.opened);self.assertFalse(fs.acquired)
    def test_no_follow_nonblock_readonly_native_flags(self):
        with patch.object(h.os,'O_NOFOLLOW',0x100000,create=True),patch.object(h.os,'O_CLOEXEC',0x200000,create=True),patch.object(h.os,'O_NONBLOCK',0x400000,create=True),patch.object(h.os,'open',return_value=1) as opened:
            h.NativeReadFS().open_file(3,'fixture')
            flags=opened.call_args.args[1]
            self.assertTrue(flags&0x100000);self.assertTrue(flags&0x400000);self.assertFalse(flags&os.O_CREAT);self.assertFalse(flags&os.O_WRONLY)
    def test_native_acl_exact_minimal_and_fail_closed_errors(self):
        import struct
        info=types.SimpleNamespace(st_mode=stat.S_IFREG|0o600)
        minimal=struct.pack('<I',2)+b''.join(struct.pack('<HHI',tag,perm,0xffffffff) for tag,perm in [(1,6),(4,0),(32,0)])
        with patch.object(h.os,'fstat',return_value=info),patch.object(h.os,'getxattr',return_value=minimal,create=True):h.NativeReadFS().acl(1)
        for raw in [b'invalid',minimal+b'extra',minimal[:4]+minimal[12:20]+minimal[4:12]+minimal[20:]]:
            with patch.object(h.os,'fstat',return_value=info),patch.object(h.os,'getxattr',return_value=raw,create=True):
                with self.assertRaises(h.ProjectionError):h.NativeReadFS().acl(1)
        for code in [errno.EPERM,errno.ENOTSUP]:
            with patch.object(h.os,'getxattr',side_effect=OSError(code,'private'),create=True):
                with self.assertRaises(h.ProjectionError):h.NativeReadFS().acl(1)
        with patch.object(h.os,'getxattr',side_effect=OSError(errno.ENODATA,'absent'),create=True):h.NativeReadFS().acl(1,True)
        with patch.object(h.os,'fstat',return_value=info),patch.object(h.os,'getxattr',return_value=minimal,create=True):
            with self.assertRaises(h.ProjectionError):h.NativeReadFS().acl(1,True)
    def test_critical_section_does_not_parse_or_validate(self):
        fs=FakeFS()
        with patch.object(h,'load_contracts',side_effect=AssertionError('validation under lock')):self.read(fs)
    def test_file_open_mismatch_is_rejected(self):
        fs=FakeFS();original=fs.open_file
        def opened(p,n):
            fd=original(p,n)
            if n=='home_assistant.json':fs.nodes[n].st_ino+=1
            return fd
        fs.open_file=opened
        with self.assertRaises(h.ProjectionError):self.read(fs)
        self.assertFalse(fs.opened);self.assertFalse(fs.acquired)


def reader_case(node,key,value):
    def test(self):
        fs=FakeFS();setattr(fs.nodes[node],key,value)
        with self.assertRaises(h.ProjectionError):self.read(fs)
        self.assertFalse(fs.opened);self.assertFalse(fs.acquired)
    return test
for node in ['associations','.home_assistant.lock','home_assistant.json']:
    mutations={'owner':('st_uid',900),'group':('st_gid',900),'mode':('st_mode',(stat.S_IFDIR|0o755) if node=='associations' else stat.S_IFREG|0o640),'writable':('st_mode',(stat.S_IFDIR|0o777) if node=='associations' else stat.S_IFREG|0o666)}
    if node!='associations':mutations.update(symlink=('st_mode',stat.S_IFLNK|0o600),fifo=('st_mode',stat.S_IFIFO|0o600),device=('st_mode',stat.S_IFCHR|0o600),directory=('st_mode',stat.S_IFDIR|0o600),links=('st_nlink',2))
    for name,(key,value) in mutations.items():setattr(ReaderTests,'test_reject_'+node.replace('.','').replace('-','_')+'_'+name,reader_case(node,key,value))
setattr(ReaderTests,'test_oversize_state',reader_case('home_assistant.json','st_size',h.LIMIT+1))


@unittest.skipUnless(sys_platform_linux := (__import__('sys').platform=='linux'),'Actual Linux/POSIX gate pending on PI3')
class PosixReaderTests(unittest.TestCase):
    def fixture(self):
        temp=tempfile.TemporaryDirectory();root=Path(temp.name);root.chmod(0o700)
        for name,data in [('home_assistant.json',canonical(state([association()]))),('.home_assistant.lock',b'')]:
            p=root/name;p.write_bytes(data);p.chmod(0o600)
        return temp,root
    def test_real_reader_complete_copy_and_shared_vs_exclusive_lock(self):
        import fcntl
        temp,root=self.fixture()
        with temp:
            with h.SecureReader(root,os.getuid(),os.getgid(),anchor=root) as reader:self.assertEqual(reader.snapshot(),(root/'home_assistant.json').read_bytes())
            with (root/'.home_assistant.lock').open('rb') as lock:
                fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
                with h.SecureReader(root,os.getuid(),os.getgid(),anchor=root) as reader:
                    with self.assertRaises(h.ProjectionError) as e:reader.snapshot()
                    self.assertEqual(e.exception.code,'OMITTED_BUSY')
                fcntl.flock(lock,fcntl.LOCK_UN)
    def test_real_symlink_hardlink_dirty_namespace_and_permissions(self):
        for kind in ['symlink','hardlink','dirty','permissions']:
            temp,root=self.fixture()
            with temp:
                if kind=='symlink':(root/'home_assistant.json').rename(root/'target');(root/'home_assistant.json').symlink_to(root/'target')
                elif kind=='hardlink':os.link(root/'home_assistant.json',root/'other')
                elif kind=='dirty':(root/'.home_assistant.txn-malformed').mkdir()
                else:(root/'home_assistant.json').chmod(0o644)
                with h.SecureReader(root,os.getuid(),os.getgid(),anchor=root) as reader:
                    with self.assertRaises(h.ProjectionError):reader.snapshot()


class EngineIntegrationTests(unittest.TestCase):
    def run_engine(self,mode):
        module=load_engine_module();value=public_inventory();value['devices'][0]['id']=association()['hioc_device_id'];value['_hostname_evidence']=None
        previous=copy.deepcopy(value);previous['devices'][0]['home_assistant']={'stale_secret':True}
        current=copy.deepcopy(value);current['devices'][0]['home_assistant']={'injected_secret':True}
        snapshots=[];topics=[];connections=[];events=[];compat=[];log=Mock()
        def discover(config,prior,**kwargs):
            self.assertNotIn('home_assistant',prior['devices'][0]);snapshots.append('discovery');return copy.deepcopy(current)
        def optional(base):
            self.assertEqual(snapshots,['discovery']);self.assertNotIn('home_assistant',base['devices'][0])
            if mode=='internal':raise RuntimeError('private exception must not leak')
            if mode=='read_failure':raise h.ProjectionError('OMITTED_UNAVAILABLE')
            if mode=='public_failure':
                a=association();a['config_entries']=[dict(entry_id='fixture',domain='deadbeefcafe')]
                return project(base,state([a]))
            return project(base,state([association()])) if mode in ['valid','mqtt_failure'] else project(base,state())
        class Mqtt:
            def __init__(self,*a):connections.append(1)
            def __enter__(self):
                self_outer.assertTrue((home/'state/inventory/inventory.json').exists());return self
            def __exit__(self,*a):pass
            def publish(self,topic,payload):
                if mode=='mqtt_failure':raise RuntimeError('synthetic transport')
                topics.append((topic,copy.deepcopy(payload)))
        self_outer=self
        with tempfile.TemporaryDirectory() as temp:
            home=Path(temp)
            class Bus:
                def __init__(self,*a):pass
                def publish(self,*a):events.append(a)
            def refresh(*a):compat.append(1);return None
            with patch.object(module,'load_config',return_value={'HIOC_HOME':temp,'HIOC_BASE_TOPIC':'fixture'}),patch.object(module,'setup_logger',return_value=log),patch.object(module,'load_json',return_value=previous),patch.object(module,'discover_inventory',side_effect=discover),patch.object(module,'MqttClient',Mqtt),patch.object(module,'EventBus',Bus),patch.object(module,'refresh_status',side_effect=refresh),patch.object(module,'now_iso',return_value=value['updated']),patch.object(h,'project_inventory',side_effect=optional):
                if mode=='import_failure':
                    import builtins
                    original=builtins.__import__
                    def imports(name,*a,**kw):
                        if name=='hioc.home_assistant_public_projection':raise ImportError('private exception must not leak')
                        return original(name,*a,**kw)
                    with patch('builtins.__import__',side_effect=imports):code=module.main()
                else:code=module.main()
            files={n:json.loads((home/'state/inventory'/n).read_bytes()) for n in ['inventory.json','devices.json','services.json','topology.json','dependencies.json','summary.json','status.json']}
        self.assertEqual(code,0);self.assertEqual(len(connections),1)
        self.assertEqual(events,[]);self.assertGreaterEqual(len(compat),2)
        self.assertNotIn('private exception',str(log.method_calls))
        for key in ['services','topology','dependencies','summary']:self.assertEqual(files[key+'.json'],value[key])
        self.assertEqual(files['devices.json'],files['inventory.json']['devices'])
        self.assertEqual(files['inventory.json']['schema_version'],'1.0')
        if mode!='mqtt_failure':self.assertEqual({t for t,_ in topics},{'fixture/inventory'+suffix for suffix in ['', '/devices','/services','/topology','/dependencies','/summary','/status']})
        self.assertNotIn('stale_secret',json.dumps(files));self.assertNotIn('injected_secret',json.dumps(files))
        present=mode in ['valid','mqtt_failure']
        self.assertEqual('home_assistant' in files['devices.json'][0],present)
        if topics:
            for topic,payload in topics:
                if topic not in ['fixture/inventory','fixture/inventory/devices']:self.assertNotIn('home_assistant',json.dumps(payload))
        self.assertEqual(files['status.json']['status'],'degraded' if mode=='mqtt_failure' else 'online')
    def test_valid(self):self.run_engine('valid')
    def test_omitted(self):self.run_engine('omitted')
    def test_import_failure(self):self.run_engine('import_failure')
    def test_private_read_failure(self):self.run_engine('read_failure')
    def test_public_validation_failure(self):self.run_engine('public_failure')
    def test_internal_exception(self):self.run_engine('internal')
    def test_mqtt_failure_unchanged(self):self.run_engine('mqtt_failure')


class ImplementationGovernanceTests(unittest.TestCase):
    def test_closed_canonical_record_and_schema(self):
        from test_pe4_ha_association_deployment_closure import validate
        path=ROOT/'governance/pe4/pe4-ha-association-public-projection-implementation.json'
        record=json.loads(path.read_bytes());schema=json.loads(path.with_suffix('.schema.json').read_bytes())
        validate(record,schema);self.assertEqual(path.read_bytes(),canonical(record));self.assertEqual(path.with_suffix('.schema.json').read_bytes(),canonical(schema))
        bad=copy.deepcopy(record);bad['PI3_POSIX_SOURCE_VALIDATION']='PASS'
        with self.assertRaises(ValueError):validate(bad,schema)
    def test_all_current_artifact_identities_and_base_bindings(self):
        import hashlib,subprocess
        record=json.loads((ROOT/'governance/pe4/pe4-ha-association-public-projection-implementation.json').read_bytes())
        for item in record['implementation_artifacts']:
            # Immutable implementation bindings remain checked against their exact commit.
            closure=json.loads((ROOT/'governance/pe4/pe4-ha-association-public-projection-posix-source-validation-closure.json').read_bytes())
            raw=subprocess.check_output(['git','show',closure['closure_predecessor']+':'+item['path']],cwd=ROOT)
            self.assertEqual(hashlib.sha256(raw).hexdigest(),item['sha256'])
            self.assertEqual(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),item['git_blob'])
            current=(ROOT/item['path']).read_bytes().replace(b'\r\n',b'\n')
            changed={i['path']:i for i in closure['closure_artifacts']}
            prep=json.loads((ROOT/'governance/pe4/pe4-ha-association-public-projection-deployment-baseline-correction.json').read_bytes());changed.update({i['path']:i for i in prep['artifacts']});changed.update(current_artifact_bindings())
            if item['path'] in changed:
                self.assertEqual(hashlib.sha256(current).hexdigest(),changed[item['path']]['sha256'])
            else:self.assertEqual(current,raw)
        for item in record['sources']:
            raw=subprocess.check_output(['git','show',record['starting_commit']+':'+item['path']],cwd=ROOT)
            self.assertEqual(hashlib.sha256(raw).hexdigest(),item['sha256'])
            self.assertEqual(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),item['git_blob'])
            verify_source_binding(item,raw,'governance/pe4/pe4-ha-association-public-projection-implementation.json',record['starting_commit'])
    def test_private_producer_preparation_and_scheduler_unchanged(self):
        import hashlib
        pairs=[(h.MODULE_PATH,h.MODULE_SHA),(h.PRIVATE_SCHEMA_PATH,h.PRIVATE_SCHEMA_SHA),
               ('governance/pe4/pe4-ha-association-public-projection-preparation.json','fa69557234e78e2ae63736c97ed1f18f4e6bec11d4d070f8663aaa19ef963122'),
               ('governance/pe4/pe4-ha-association-public-projection-preparation.schema.json','89d23127227bd0f37edc717808478d34452a1e1ce606eeb631db95e9a04b0721'),
               ('docs/PE4_HOME_ASSISTANT_ASSOCIATION_PUBLIC_PROJECTION_PREPARATION.md','f64b8ae325866f0cf6dbcea83147ad748b3461e94e7c60a237b5cc4df564dace')]
        for path,sha in pairs:self.assertEqual(hashlib.sha256((ROOT/path).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),sha)
    def test_private_pure_call_surface_only(self):
        tree=ast.parse((ROOT/'pi4/lib/hioc/home_assistant_public_projection.py').read_text(encoding='utf8'))
        calls={n.func.attr for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=='private'}
        self.assertTrue(calls<={'strict_json','check_schema_contract','validate_state','validate_privacy'})
    def test_lifecycle_still_gated_and_mqtt_contract_exact(self):
        record=json.loads((ROOT/'governance/pe4/pe4-ha-association-public-projection-implementation.json').read_bytes())
        self.assertEqual(record['source_implementation'],'IMPLEMENTED');self.assertEqual(record['windows_synthetic_validation'],'PASS')
        for key in ['pi3_posix_source_validation','production_deployment','production_public_projection']:self.assertEqual(record[key],'NOT_STARTED')
        self.assertEqual(record['public_fields'],P['required']);self.assertFalse(any(record['codex_activity'].values()))
        text=(ROOT/'docs/HIOC_MASTER_PLAN.md').read_text(encoding='utf8')
        for phrase in ['WINDOWS SYNTHETIC VALIDATION PASS','PI3 POSIX Source Validation','POSIX validation closure commit ONLY','PE-4 NOT COMPLETE']:self.assertIn(phrase,text)


if __name__=='__main__':unittest.main()
