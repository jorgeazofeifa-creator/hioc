"""Synthetic Action F publication flow; no production object or interpreter runs."""
import copy, contextlib, io, json, stat, subprocess, types, unittest
from unittest import mock
from tools import hioc_pe4_action_f as F
from tests.test_pe4_action_e_handoff import tree, info, directory

COMMIT='b'*40
def bindings():
    a=F.accepted_manifest()
    return dict(current_consumer=COMMIT,accepted_manifest_sha256=F.ACCEPTED_SHA,
      historical=a['historical'],durable_bundle_sha256=a['durable_bundle']['manifest_sha256'],
      tree_sha256=a['capture']['tree_sha256'],attestation_sha256=a['continuity']['attestation_sha256'],
      original_construction_path=a['historical']['construction_path'],
      original_construction_identity=a['historical']['root'],final_environment_path=(F.H.ENVIRONMENTS/F.H.VERSION).as_posix(),
      final_environment_identity='NONE',client_path=F.C.CLIENT_TARGET.as_posix(),client_sha256=F.C.CLIENT_SHA256,
      client_identity='NONE',client_disposition='ABSENT',original_active='NONE',original_previous='NONE',
      final_active='NONE',final_previous='NONE',original_root_ctime_ns=20,final_root_ctime_ns='NONE',
      final_active_identity='NONE',final_previous_identity='NONE')

class Memory:
    """Small syscall adapter: real execute(), Journal, schema and terminal are used."""
    def __init__(self,fail=None,existing=False):
        self.fail=fail;self.files={};self.calls=[];self.mutations=set();self.existing=existing;self.allocated=False
    def hit(self,label):
        self.calls.append(label)
        if self.fail==label:raise OSError('private error never emitted')
    def preflight(self,commit):
        self.hit('preflight')
        if self.allocated:raise F.Failure('UNRESOLVED_TRANSACTION','PRECONDITIONS')
        b=bindings()
        if self.existing:
            b['client_disposition']='EXACT_PREEXISTING'
            b['client_identity']=dict(identity=b['original_construction_identity'],token=[1]*9)
        return b
    def revalidate(self,commit):self.hit('revalidate')
    def allocate(self,tid):
        self.allocated=True;self.hit('allocate')
        return str(F.H.PE4/'transactions'/('f-'+tid))
    def write(self,name,raw):
        event=F.H.parse(raw,'STAGED_INPUT')['event']
        self.hit('write-before:'+event)
        if name in self.files:raise F.Failure('CONFLICT','JOURNAL')
        self.files[name]=raw
        self.hit('write-after:'+event)
    def read(self,name):self.hit('read:'+name);return self.files[name]
    def names(self):self.hit('names');return sorted(self.files)
    def mutate(self,op,tid):
        self.hit('mutate-before:'+op);self.mutations.add(op);self.hit('mutate-after:'+op)
    def confirm(self,op,b):
        self.hit('confirm-before:'+op)
        if op=='CLIENT':
            b['client_disposition']='PUBLISHED'
            b['client_identity']=dict(identity=b['original_construction_identity'],token=[1]*9)
        if op=='ENVIRONMENT':
            b['final_environment_identity']=b['original_construction_identity'];b['final_root_ctime_ns']=30
        if op=='ACTIVE_SWITCH':
            b['final_active']='environments/'+F.H.VERSION;b['final_active_identity']=b['original_construction_identity']
        if op=='PREVIOUS':b['final_previous_identity']=b['original_construction_identity']
        self.hit('confirm-after:'+op)
    def not_completed(self,op):return op not in self.mutations
    def postverify(self,b,commit):self.hit('postverify')
    def close(self):self.hit('close')

def run(backend,args=None):
    out=io.StringIO()
    with contextlib.redirect_stdout(out):
        rc=F.cli(args or ['--governance-commit',COMMIT],lambda:backend)
    return rc,dict(line.split('=',1) for line in out.getvalue().splitlines())

class PublicationTests(unittest.TestCase):
    def test_absent_client_full_real_executor_and_durable_chain(self):
        backend=Memory();rc,out=run(backend)
        self.assertEqual(rc,0)
        self.assertEqual(out['RESULT'],'PASS');self.assertEqual(out['PUBLICATION_STATE'],'COMPLETE')
        self.assertEqual(out['EVIDENCE_STATE'],'CONFIRMED');self.assertEqual(out['RECOVERY_REQUIRED'],'FALSE')
        self.assertEqual(out['ROLLBACK_RECOMMENDED'],'FALSE')
        previous='NONE'
        for name in sorted(n for n in backend.files if n!='result.json'):
            doc=F.H.parse(backend.files[name],'STAGED_INPUT',canonical_required=True)
            self.assertEqual(doc['previous_record_sha256'],previous)
            previous=F.H.digest(backend.files[name])
            if doc['event'].endswith('_INTENT'):
                self.assertLess(backend.calls.index('write-after:'+doc['event']),backend.calls.index('mutate-before:'+doc['event'][:-7]))
            if doc['event'].endswith('_CONFIRMED'):
                self.assertLess(backend.calls.index('confirm-after:'+doc['event'][:-10]),backend.calls.index('write-before:'+doc['event']))
        tail=F.H.parse(backend.files[sorted(n for n in backend.files if n!='result.json')[-1]],'STAGED_INPUT')
        self.assertEqual(tail['event'],'COMMITTED')
        self.assertEqual(tail['result_sha256'],F.H.digest(backend.files['result.json']))
    def test_exact_client_is_not_republished(self):
        backend=Memory(existing=True);rc,out=run(backend)
        self.assertEqual(rc,0);self.assertNotIn('CLIENT',backend.mutations)
        self.assertNotIn('write-before:CLIENT_INTENT',backend.calls)
    def test_no_construction_python_dependency_probes_or_lifecycle_invocations(self):
        with mock.patch.object(F.H,'capture',side_effect=AssertionError()),mock.patch.object(F.H,'preserve',side_effect=AssertionError()),mock.patch.object(F.C,'exact_distribution_set',side_effect=AssertionError()),mock.patch.object(F.C,'run',side_effect=AssertionError()),mock.patch.object(F.subprocess,'run',side_effect=AssertionError()):
            self.assertEqual(run(Memory())[0],0)
    def test_arguments_rejected_without_adapter(self):
        factory=mock.Mock(side_effect=AssertionError())
        for args in ([],['--governance-commit','short'],['--construction-directory','/alternate','--governance-commit',COMMIT]):
            with self.subTest(args=args),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(F.cli(args,factory),2)
        factory.assert_not_called()
    def test_record_strict_unknown_duplicate_type_hash_and_size(self):
        state=F.initial_state();j=F.Journal(Memory(),'a'*32,bindings(),state)
        good=j.document('PREPARED');F.record(good)
        for change in ({'extra':True},{'sequence':True},{'transaction_id':'bad'},{'previous_record_sha256':'abc'},{'event':'RETRY'}):
            with self.subTest(change=change),self.assertRaises((F.Failure,F.H.Failure)):
                F.record(dict(good,**change))
        for raw in (b'{"x":1,"x":2}',b'{ "x":1}\n'):
            with self.assertRaises(F.H.Failure):F.H.parse(raw,'STAGED_INPUT',canonical_required=True)
        bad=copy.deepcopy(good);bad['bindings']['final_active']='x'*70000
        with self.assertRaises(F.H.Failure):F.record(bad)

class HandoffTests(unittest.TestCase):
    def test_actual_accepted_manifest_validates_and_is_immutable(self):
        before=(F.H.REPOSITORY/F.ACCEPTED).read_bytes()
        a=F.accepted_manifest()
        self.assertEqual(a['approval']['state'],'ACCEPTED')
        self.assertFalse(a['continuity']['historical_recursive_continuity_machine_proven'])
        self.assertEqual(F.H.digest(before),F.ACCEPTED_SHA)
    def test_changed_noncanonical_or_unaccepted_manifest_rejected(self):
        raw=(F.H.REPOSITORY/F.ACCEPTED).read_bytes()
        for altered in (raw+b' ',raw.replace(b'ACCEPTED"',b'PROPOSED"'),raw.replace(b'false',b'true',1)):
            with self.subTest(raw=altered[:10]),mock.patch.object(F.Path,'read_bytes',return_value=altered),self.assertRaises(F.Failure):
                F.accepted_manifest()
    def fixture(self):
        a=F.accepted_manifest();t=tree()
        a['capture']['tree_sha256']=F.H.digest(F.H.canonical(t,F.H.TREE_LIMIT))
        eraw=F.H.canonical(a['e_semantics']);draw=b'original synthetic D\n'
        a['historical']['e_evidence_sha256']=F.H.digest(eraw)
        a['historical']['d_evidence_sha256']=F.H.digest(draw)
        # The fixed schema requires historical production hashes: keep those values,
        # and mock only hashing for the synthetic original-copy bytes.
        a['historical']=F.H.history()
        att=dict(schema_version='1.0',record_type='CONTINUITY_ATTESTATION',attestation_class='GOVERNANCE_DERIVED_ATTESTATION',
          evidence_class=F.H.CONTINUITY,historical=a['historical'],capture_id=a['capture']['capture_id'],
          capture_source_commit=a['capture']['source_commit'],preservation_source_commit=a['capture']['source_commit'],
          construction_tree_sha256=a['capture']['tree_sha256'],capture_report_sha256=a['capture']['report_sha256'],
          capture_manifest_sha256=a['capture']['manifest_sha256'],fact_sources=a['revalidated_observables'],
          historical_recursive_snapshot_persisted=False,historical_recursive_continuity_machine_proven=False,
          limitation=F.H.LIMITATION,governed_chronology=['E_EXECUTED_ONCE_PASS','WINDOWS_E_CLOSURE','WINDOWS_F_PREPARATION','WINDOWS_F_CORRECTIVE_DESIGN','WINDOWS_CONTINUITY_DESIGN','NO_AUTHORIZED_POST_E_HIOC_MUTATION_RECORDED'],
          approval_state='APPROVED_FOR_PRESERVATION',authorization_reference='synthetic')
        payloads={'action-d-result.json':draw,'action-e-result.json':eraw,'construction-tree.json':F.H.canonical(t,F.H.TREE_LIMIT),'continuity-attestation.json':F.H.canonical(att)}
        a['continuity']['attestation_sha256']=F.H.digest(payloads['continuity-attestation.json'])
        m=dict(schema_version='1.0',record_type='DURABLE_HANDOFF_MANIFEST',capture_id=a['capture']['capture_id'],
          capture_source_commit=a['capture']['source_commit'],preservation_source_commit=a['capture']['source_commit'],
          historical=a['historical'],continuity_class=F.H.CONTINUITY,approval_state='APPROVED_FOR_PRESERVATION',
          inventory=F.H.inventory(payloads,0o400))
        for item in m['inventory']:
            if item['name']=='action-d-result.json':item['sha256']=F.H.D_SHA
            if item['name']=='action-e-result.json':item['sha256']=F.H.E_SHA
        payloads['manifest.json']=F.H.canonical(m);a['durable_bundle']['manifest_sha256']=F.H.digest(payloads['manifest.json'])
        return a,t,payloads
    def call_bundle(self,change=None):
        a,t,payloads=self.fixture()
        if change:change(a,t,payloads)
        original=F.H.digest
        def digest(raw):
            if raw==b'original synthetic D\n':return F.H.D_SHA
            if raw==F.H.canonical(a['e_semantics']):return F.H.E_SHA
            return original(raw)
        with mock.patch.object(F.H,'digest',side_effect=digest),mock.patch.object(F.H,'read_file',side_effect=lambda d,n,*args:payloads[n]),mock.patch.object(F.H,'check_files') as check:
            fs=mock.Mock();fs.open.return_value=directory()
            result=F.bundle(fs,a)
            check.assert_called_once();self.assertEqual(check.call_args.args[2],0o400)
            fs.open.assert_called_once_with(F.Path(a['durable_bundle']['directory']),'STAGED_INPUT',0o500)
            return result
    def test_real_bundle_validation_exact_inventory_modes_bindings(self):self.call_bundle()
    def test_bundle_manifest_tree_attestation_original_copy_mismatch(self):
        for name in ('manifest.json','construction-tree.json','continuity-attestation.json','action-d-result.json','action-e-result.json'):
            def change(a,t,payloads):payloads[name]+=b'changed'
            with self.subTest(name=name),self.assertRaises((F.Failure,F.H.Failure)):self.call_bundle(change)
    def test_tree_metadata_content_inode_and_root_transition(self):
        baseline=tree()['entries']
        for key in ('dev','ino','uid','gid','mode','nlink','size','mtime_ns','ctime_ns','children'):
            changed=copy.deepcopy(baseline)
            changed[0][key]='0777' if key=='mode' else ['61'] if key=='children' else changed[0][key]+1
            with self.subTest(key=key),self.assertRaises(F.Failure):F.same_entries(baseline,changed)
        renamed=copy.deepcopy(baseline);renamed[0]['ctime_ns']+=1
        F.same_entries(baseline,renamed,True)
        child=F.H.entry(info(st_mode=stat.S_IFREG|0o400),['61'],'REGULAR_FILE',sha256='a'*64)
        expected=baseline+[child]
        for key in ('sha256','ctime_ns','ino','mtime_ns','mode'):
            changed=copy.deepcopy(expected);changed[1][key]='b'*64 if key=='sha256' else '0600' if key=='mode' else changed[1][key]+1
            with self.subTest(child=key),self.assertRaises(F.Failure):F.same_entries(expected,changed,True)
        self.assertEqual(F.H.token(info()),F.H.token(info(st_atime_ns=999)))
    def test_client_absent_exact_conflicting_or_substituted(self):
        adapter=F.Posix();adapter.tools=directory(F.C.CLIENT_TARGET.parent)
        try:
            with mock.patch.object(F.os,'stat',side_effect=FileNotFoundError()):
                self.assertEqual(adapter.client_info(),'NONE')
            before=info(st_mode=stat.S_IFREG|0o700)
            with mock.patch.object(F.os,'stat',return_value=before),mock.patch.object(F.H,'read_file',return_value=b'client'),mock.patch.object(F.H,'digest',return_value=F.C.CLIENT_SHA256):
                self.assertEqual(adapter.client_info()['identity'],F.H.identity(before))
            with mock.patch.object(F.os,'stat',return_value=before),mock.patch.object(F.H,'read_file',return_value=b'conflict'),self.assertRaises(F.Failure):adapter.client_info()
            with mock.patch.object(F.os,'stat',side_effect=[before,info(st_ino=8)]),mock.patch.object(F.H,'read_file',return_value=b'client'),mock.patch.object(F.H,'digest',return_value=F.C.CLIENT_SHA256),self.assertRaises(F.Failure):adapter.client_info()
        finally:adapter.close()


class PosixAdapterTests(unittest.TestCase):
    def adapter(self):
        adapter=F.Posix()
        adapter.root=directory(F.H.PE4);adapter.root.parent=directory(F.H.HIOC/'runtime',12)
        adapter.env=directory(F.H.ENVIRONMENTS);adapter.env.parent=adapter.root
        adapter.tools=directory(F.C.CLIENT_TARGET.parent);adapter.tools.parent=directory(F.H.HIOC,13)
        adapter.construction=directory();adapter.final=F.H.VERSION
        adapter.tree=tree();adapter.client_raw=b'synthetic client';adapter.client_before='NONE'
        return adapter
    def test_real_client_staging_no_replace_and_durability_failure(self):
        for point in ('write','file-parent-sync','publish'):
            adapter=self.adapter()
            try:
                with mock.patch.object(adapter,'client_info',return_value='NONE'),mock.patch.object(F,'write_owned',return_value=info(st_mode=stat.S_IFREG|0o700)) as write,mock.patch.object(F.H,'sync') as sync,mock.patch.object(F.H,'read_file',return_value=adapter.client_raw),mock.patch.object(F.os,'stat',return_value=info(st_mode=stat.S_IFREG|0o700)),mock.patch.object(F.H,'noreplace') as rename:
                    if point=='write':write.side_effect=OSError()
                    if point=='file-parent-sync':sync.side_effect=OSError()
                    if point=='publish':rename.side_effect=F.H.Failure('CONFLICT','BUNDLE_PUBLICATION')
                    with self.assertRaises((OSError,F.H.Failure)):adapter.mutate('CLIENT','a'*32)
                    if point!='publish':rename.assert_not_called()
                    else:rename.assert_called_once()
            finally:adapter.close()
    def test_real_environment_rename_identity_and_parent_fsync_boundaries(self):
        adapter=self.adapter();b=bindings()
        try:
            with mock.patch.object(F.H,'verify_construction'),mock.patch.object(F.H,'noreplace') as rename:
                adapter.mutate('ENVIRONMENT','a'*32)
                rename.assert_called_once_with(adapter.env,F.H.CONSTRUCTION.name,F.H.VERSION)
                self.assertEqual(adapter.construction.path,F.H.ENVIRONMENTS/F.H.VERSION)
            changed=copy.deepcopy(adapter.tree['entries']);changed[0]['ctime_ns']+=5
            with mock.patch.object(F.H,'tree_entries',return_value=changed),mock.patch.object(F.H,'sync') as sync,mock.patch.object(F.os,'fsync',side_effect=OSError()),mock.patch.object(F.H,'absent'):
                with self.assertRaises(OSError):adapter.confirm('ENVIRONMENT',b)
                sync.assert_called_once_with(adapter.construction,adapter.env,'BUNDLE_FSYNC')
                self.assertEqual(b['final_environment_identity'],'NONE')
        finally:adapter.close()
    def test_previous_and_active_are_no_replace_and_verified_before_confirmation(self):
        for operation in ('PREVIOUS','ACTIVE_STAGE','ACTIVE_SWITCH'):
            adapter=self.adapter();adapter.temp_active='.active.f-'+'a'*32
            adapter.active_staged=F.H.identity(info())
            try:
                with mock.patch.object(F,'write_owned',return_value=info()) as write,mock.patch.object(F.H,'sync') as sync,mock.patch.object(F.H,'noreplace') as rename,mock.patch.object(F.os,'symlink') as link,mock.patch.object(F.os,'stat',return_value=info()),mock.patch.object(adapter,'link',return_value=adapter.active_staged):
                    adapter.mutate(operation,'a'*32)
                    if operation=='PREVIOUS':
                        self.assertEqual(write.call_args.args[2],b'NONE\n')
                        rename.assert_called_once_with(adapter.root,'.previous-active.f-'+'a'*32,'previous-active')
                    if operation=='ACTIVE_STAGE':
                        link.assert_called_once_with('environments/'+F.H.VERSION,'.active.f-'+'a'*32,dir_fd=adapter.root.fd)
                        rename.assert_not_called()
                    if operation=='ACTIVE_SWITCH':rename.assert_called_once_with(adapter.root,adapter.temp_active,'active')
                with mock.patch.object(adapter,'link',return_value=adapter.active_staged),mock.patch.object(F.H,'sync',side_effect=OSError()):
                    if operation!='PREVIOUS':
                        b=bindings()
                        with self.assertRaises(OSError):adapter.confirm(operation,b)
                        self.assertEqual(b['final_active'],'NONE')
            finally:adapter.close()
    def test_invalid_active_target_or_symlink_identity_rejected(self):
        adapter=self.adapter()
        try:
            for value in ('../outside','environments/alternate'):
                with mock.patch.object(F.os,'stat',return_value=info(st_mode=stat.S_IFLNK|0o777)),mock.patch.object(F.os,'getuid',return_value=1000,create=True),mock.patch.object(F.os,'getgid',return_value=1000,create=True),mock.patch.object(F.os,'readlink',return_value=value),self.assertRaises(F.Failure):
                    adapter.link('active')
            with mock.patch.object(F.os,'stat',return_value=info(st_mode=stat.S_IFREG|0o700)),self.assertRaises(F.Failure):adapter.link('active')
        finally:adapter.close()
    def test_not_completed_is_only_read_only_absence_proof(self):
        adapter=self.adapter();adapter.temp_active='.active.test'
        try:
            with mock.patch.object(F.os,'stat',side_effect=FileNotFoundError()),mock.patch.object(F.H,'verify_construction') as verify:
                self.assertTrue(adapter.not_completed('ENVIRONMENT'));verify.assert_called_once()
            with mock.patch.object(F.os,'stat',return_value=info()):self.assertFalse(adapter.not_completed('CLIENT'))
        finally:adapter.close()
    def test_missing_original_allowed_but_surviving_original_mismatch_rejected(self):
        adapter=self.adapter();adapter.accepted=F.accepted_manifest()
        adapter.payloads={'action-e-result.json':b'E','action-d-result.json':b'D'}
        try:
            with mock.patch.object(F.os,'lstat',side_effect=FileNotFoundError()),mock.patch.object(F.H,'evidence') as evidence:
                adapter.originals();evidence.assert_not_called()
            del adapter.original_presence
            with mock.patch.object(F.os,'lstat',return_value=info()),mock.patch.object(F.H,'evidence',return_value=b'changed'),self.assertRaises(F.Failure):
                adapter.originals()
        finally:adapter.close()


def snapshot_fixture():
    doc=tree()
    file_data={
        (b'bin',b'python'):(823209,'0755','4'*64),
        (F.H.MARKER.encode(),):(50,'0400',doc['bindings']['d_marker_sha256']),
        (b'pyvenv.cfg',):(51,'0640',doc['bindings']['configuration_sha256']),
        (b'lib',b'python3.11',b'site-packages',b'websockets',b'speedups.cpython-311-aarch64-linux-gnu.so'):(52,'0640',F.H.NATIVE_SHA),
        (b'lib',b'python3.11',b'site-packages',b'websockets',b'__init__.py'):(53,'0640','5'*64)}
    dirs={()}
    for key in file_data:
        for n in range(1,len(key)):dirs.add(key[:n])
    entries=[]
    for key in dirs:
        children=sorted({k[len(key)] for k in set(file_data)|dirs if len(k)==len(key)+1 and k[:len(key)]==key})
        entries.append(F.H.entry(info(),[p.hex() for p in key],'DIRECTORY',children=[p.hex() for p in children]))
    for key,(ino,mode,sha) in file_data.items():
        entries.append(F.H.entry(info(st_ino=ino,st_mode=stat.S_IFREG|int(mode,8)),[p.hex() for p in key],'REGULAR_FILE',sha256=sha))
    doc['entries']=sorted(entries,key=lambda e:tuple(bytes.fromhex(p) for p in e['path']))
    F.H.validate_tree(doc)
    return doc

class PreflightTests(unittest.TestCase):
    def test_explicit_snapshot_marker_native_interpreter_member_rejections(self):
        accepted=F.accepted_manifest();doc=snapshot_fixture()
        F.snapshot_bindings(accepted,doc)
        for target,field in ((b'bin/python','ino'),(F.H.MARKER.encode(),'sha256'),(b'pyvenv.cfg','sha256'),
                             (b'lib/python3.11/site-packages/websockets/speedups.cpython-311-aarch64-linux-gnu.so','sha256')):
            bad=copy.deepcopy(doc)
            for e in bad['entries']:
                if b'/'.join(bytes.fromhex(p) for p in e['path'])==target:e[field]=0 if field=='ino' else '0'*64
            with self.subTest(target=target),self.assertRaises(F.Failure):F.snapshot_bindings(accepted,bad)
        changed=copy.deepcopy(doc)
        for e in changed['entries']:
            if e['type']=='REGULAR_FILE' and e['path'][-1]==b'__init__.py'.hex():e['sha256']='0'*64
        with self.assertRaises(F.Failure):F.same_entries(doc['entries'],changed['entries'])
    def call(self,collision=None,lock_busy=False,changed_tree=False):
        adapter=F.Posix();a=F.accepted_manifest();doc=snapshot_fixture()
        marker=dict(schema_version='1.0',action='PE-4.0B.2a-D',governance_commit=a['historical']['d_producer'],
                    construction_directory=a['historical']['construction_path'],environment_identity=F.H.VERSION,
                    wheel_sha256=F.C.WHEEL_SHA256,lock_sha256=F.C.LOCK_SHA256,
                    evidence_directory=a['historical']['d_evidence_directory'],evidence_sha256=a['historical']['d_evidence_sha256'],result='PASS')
        raw=F.H.canonical(marker);doc['bindings']['d_marker_sha256']=F.H.digest(raw)
        for e in doc['entries']:
            if e['path']==[F.H.MARKER.encode().hex()]:e['sha256']=F.H.digest(raw)
        d=directory();objects={str(F.H.CONSTRUCTION):d,str(F.H.PE4):directory(F.H.PE4),
                             str(F.H.ENVIRONMENTS):directory(F.H.ENVIRONMENTS),
                             str(F.C.CLIENT_TARGET.parent):directory(F.C.CLIENT_TARGET.parent),
                             str(F.H.PE4/'transactions'):directory(F.H.PE4/'transactions')}
        adapter.fs=mock.Mock();adapter.fs.open.side_effect=lambda path,*args:objects[str(path)]
        client=subprocess.check_output(['git','--no-optional-locks','-C',str(F.H.REPOSITORY),
            'show','2a5e6299a0806c3f3d7c3bc11c84fddc8492333c:tools/hioc-pe4-ha-auth-capability.py'])
        self.assertEqual(F.C.CLIENT_SHA256,'5c2886452a61185c7e7329777dbd4fa3de4da98dd4793a1a84501bc30016879e')
        self.assertEqual(F.H.digest(client),F.C.CLIENT_SHA256)
        def status(name,**kw):
            if name==collision:return info()
            raise FileNotFoundError()
        lock=types.SimpleNamespace(LOCK_EX=2,LOCK_NB=4,flock=mock.Mock(side_effect=BlockingIOError() if lock_busy else None))
        live=copy.deepcopy(doc['entries'])
        if changed_tree:live[-1]['ctime_ns']+=1
        try:
            with mock.patch.object(F,'verify_launcher'),mock.patch.object(F.H,'target_guard'),mock.patch.object(F,'source_guard'),mock.patch.object(F,'bundle',return_value=(directory(),{},doc)),mock.patch.object(adapter,'originals'),mock.patch.object(F,'fcntl',lock),mock.patch.object(F.os,'stat',side_effect=status),mock.patch.object(F.os,'listdir',return_value=['f-incomplete']),mock.patch.object(F.os,'getuid',return_value=1000,create=True),mock.patch.object(F.os,'getgid',return_value=1000,create=True),mock.patch.object(F.H,'tree_entries',return_value=live),mock.patch.object(F.H,'read_file',return_value=raw) as read,mock.patch.object(F,'git',return_value=client):
                result=adapter.preflight(COMMIT)
                self.assertEqual(result['original_active'],'NONE')
                self.assertEqual(read.call_args.args[3],0o400)
                adapter.fs.child.assert_not_called()
                return result
        finally:adapter.close()
    def test_real_preflight_validates_before_any_directory_creation(self):self.call()
    def test_real_preflight_collision_prior_transaction_lock_and_tree_change(self):
        for collision in (F.H.VERSION,'active','previous-active','transactions'):
            with self.subTest(collision=collision),self.assertRaises((F.Failure,F.H.Failure)):self.call(collision)
        with self.assertRaises(F.Failure):self.call(lock_busy=True)
        with self.assertRaises((F.Failure,F.H.Failure)):self.call(changed_tree=True)
    def test_current_consumer_guard_and_protected_lineage(self):
        a=F.accepted_manifest();raw=(F.H.REPOSITORY/F.ACCEPTED).read_bytes()
        def command(args):
            if args==['branch','--show-current']:return b'main\n'
            if args in (['rev-parse','HEAD'],['rev-parse','refs/remotes/origin/main']):return COMMIT.encode()
            if args==['rev-parse','--is-shallow-repository']:return b'false'
            if args[0] in ('status','merge-base'):return b''
            if args[0]=='rev-list':return b'0 0'
            if args[:2]==['rev-parse','--git-path']:return b'absent'
            if args[0]=='show':return raw
            return b'a'*40
        with mock.patch.object(F.H,'SOURCE',F.H.REPOSITORY),mock.patch.object(F.os.path,'lexists',return_value=False),mock.patch.object(F,'git',side_effect=command) as git:
            F.source_guard(COMMIT,a)
            self.assertTrue(any(c.args[0]==['hash-object','--path=tools/hioc_pe4_action_f.py',str(F.H.REPOSITORY/'tools/hioc_pe4_action_f.py')] for c in git.call_args_list))
        def changed(args):
            if args[0]=='hash-object':return b'b'*40
            return command(args)
        with mock.patch.object(F.H,'SOURCE',F.H.REPOSITORY),mock.patch.object(F.os.path,'lexists',return_value=False),mock.patch.object(F,'git',side_effect=changed),self.assertRaises(F.Failure):
            F.source_guard(COMMIT,a)


class LauncherAndRetentionTests(unittest.TestCase):
    def test_construction_or_nonisolated_launcher_rejected(self):
        for executable,isolated,no_site in ((str(F.H.CONSTRUCTION/'bin/python'),1,1),('/usr/bin/python3',0,1),('/usr/bin/python3',1,0)):
            with self.subTest(executable=executable,isolated=isolated,no_site=no_site),mock.patch.object(F.sys,'executable',executable),mock.patch.object(F.sys,'flags',types.SimpleNamespace(isolated=isolated,no_site=no_site)),self.assertRaises(F.Failure):
                F.verify_launcher()
        with mock.patch.object(F.sys,'executable','/usr/bin/python3'),mock.patch.object(F.sys,'flags',types.SimpleNamespace(isolated=1,no_site=1)),mock.patch.object(F.sys,'dont_write_bytecode',True):
            F.verify_launcher()
    def test_seen_original_disappearance_rejected(self):
        adapter=F.Posix();adapter.accepted=F.accepted_manifest();adapter.payloads={'action-e-result.json':b'E','action-d-result.json':b'D'}
        try:
            with mock.patch.object(F.os,'lstat',return_value=info()),mock.patch.object(F.H,'evidence',side_effect=[b'E',b'D']):
                adapter.originals()
            with mock.patch.object(F.os,'lstat',side_effect=FileNotFoundError()),self.assertRaises(F.Failure):
                adapter.originals()
        finally:adapter.close()


class OwnedWriteTests(unittest.TestCase):
    def call(self,fail=None):
        d=directory();created=info(st_mode=stat.S_IFREG|0o600,st_nlink=1,st_size=0)
        completed=info(st_mode=stat.S_IFREG|0o600,st_nlink=1,st_size=3)
        named=info(st_mode=stat.S_IFREG|0o600,st_nlink=1,st_size=3,st_ino=99) if fail=='replacement' else completed
        if fail=='hardlink':created.st_nlink=2
        with mock.patch.object(F.os,'O_NOFOLLOW',0x100,create=True),mock.patch.object(F.os,'open',return_value=7) as opening,mock.patch.object(F.os,'fstat',side_effect=[created,completed]),mock.patch.object(F.os,'stat',return_value=named),mock.patch.object(F.os,'getuid',return_value=1000,create=True),mock.patch.object(F.os,'getgid',return_value=1000,create=True),mock.patch.object(F.os,'write',side_effect=[2,1]) as write,mock.patch.object(F.os,'fchmod',create=True),mock.patch.object(F.os,'fsync',side_effect=OSError() if fail=='fsync' else None) as sync,mock.patch.object(F.os,'close') as close,mock.patch.object(F.H,'read_file',return_value=b'abc') as read:
            try:
                result=F.write_owned(d,'record.json',b'abc',0o600)
                self.assertEqual(result,completed);self.assertEqual(write.call_count,2)
                sync.assert_called_once_with(7);read.assert_called_once_with(d,'record.json','POSTVALIDATION',0o600)
                flags=opening.call_args.args[1]
                self.assertTrue(flags&F.os.O_EXCL);self.assertTrue(flags&F.os.O_NOFOLLOW)
                self.assertEqual(opening.call_args.kwargs['dir_fd'],d.fd)
            finally:close.assert_called_once_with(7)
    def test_partial_write_fsync_and_descriptor_name_pin(self):self.call()
    def test_fsync_hardlink_and_same_bytes_inode_replacement_rejected(self):
        for fail in ('fsync','hardlink','replacement'):
            with self.subTest(fail=fail),self.assertRaises((F.Failure,OSError)):self.call(fail)
    def test_journal_reread_rejects_same_bytes_changed_inode(self):
        adapter=F.Posix();adapter.tx=directory()
        expected=info(st_mode=stat.S_IFREG|0o600,st_nlink=1)
        adapter.record_pins['0000.json']=F.H.token(expected)
        try:
            with mock.patch.object(F.os,'stat',return_value=info(st_mode=stat.S_IFREG|0o600,st_nlink=1,st_ino=999)),mock.patch.object(F.H,'read_file') as read,self.assertRaises(F.Failure):
                adapter.read('0000.json')
            read.assert_not_called()
        finally:adapter.close()

if __name__=='__main__':unittest.main()
