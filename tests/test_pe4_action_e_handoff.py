"""Synthetic behavior/fault tests; no production paths are opened."""
import copy, contextlib, io, json, pathlib, stat, types, unittest
from unittest import mock
from tools import hioc_pe4_action_e_handoff as H

def info(**changes):
    values=dict(st_dev=45826,st_ino=823199,st_uid=1000,st_gid=1000,st_mode=stat.S_IFDIR|0o750,st_nlink=2,st_size=4096,st_mtime_ns=10,st_ctime_ns=20,st_atime_ns=30)
    values.update(changes);return types.SimpleNamespace(**values)
def tree():
    return dict(schema_version='1.0',record_type='CONSTRUCTION_TREE',root_path=H.CONSTRUCTION.as_posix(),atime_excluded=True,hierarchy=[dict(path=H.CONSTRUCTION.as_posix(),identity=H.history()['root'])],entries=[H.entry(info(),[],'DIRECTORY',children=[])],bindings=dict(d_marker_sha256='1'*64,d_evidence_sha256=H.D_SHA,interpreter_identity=dict(dev=45826,ino=823209,uid=1000,gid=1000,mode='0755'),configuration_sha256='2'*64,native_sha256=H.NATIVE_SHA,member_policy_sha256='3'*64,fact_class='MACHINE_VERIFIED_CAPTURE_FORWARD'))
def report(t=None):
    t=t or tree()
    return dict(schema_version='1.0',record_type='CAPTURE_REPORT',capture_id='a'*32,capture_source_commit='b'*40,authorization_reference='test-only',historical=H.history(),revalidated_observables=H.observables(),capture_time_facts=dict(construction_tree_sha256=H.digest(H.canonical(t,H.TREE_LIMIT)),d_marker_sha256=t['bindings']['d_marker_sha256'],fact_class='MACHINE_VERIFIED_CAPTURE_FORWARD'),continuity_class=H.CONTINUITY,historical_recursive_snapshot_persisted=False,historical_recursive_continuity_machine_proven=False,limitation=H.LIMITATION,approval_state='PROPOSED',validation_result='PASS',error_code='NONE',failure_stage='COMPLETE')
def directory(path=H.CONSTRUCTION,fd=10):
    return types.SimpleNamespace(path=path,fd=fd,identity=H.history()['root'].copy(),parent=None,check=mock.Mock())

class CanonicalTests(unittest.TestCase):
    def test_canonical_bytes_order_escape_and_lf(self):
        self.assertEqual(H.canonical({'z':'\u00e9','a':1}),b'{"a":1,"z":"\\u00e9"}\n')
        self.assertEqual(H.canonical({'z':1,'a':2}),H.canonical({'a':2,'z':1}))
    def test_parse_rejections(self):
        for raw in (b'{"a":1,"a":2}',b'{"a":NaN}',b'{"a":1.0}',b'\xff',b'{'):
            with self.subTest(raw=raw),self.assertRaises(H.Failure):H.parse(raw,'E_EVIDENCE')
    def test_size_and_canonical_input_limits(self):
        for function in (lambda:H.canonical({'a':'abc'},3),lambda:H.parse(b'12345','STAGED_INPUT',4),lambda:H.parse(b'{ "a":1}\n','STAGED_INPUT',canonical_required=True)):
            with self.assertRaises(H.Failure):function()
    def test_schema_exact_types_keys_and_constants(self):
        valid=report();H.record('capture-report',valid)
        for change in ({'extra':1},{'capture_source_commit':'A'*40},{'capture_source_commit':'abc'},{'historical_recursive_snapshot_persisted':True},{'historical_recursive_continuity_machine_proven':True},{'approval_state':'ACCEPTED'},{'continuity_class':'MACHINE_VERIFIED_CAPTURE_FORWARD'}):
            v=copy.deepcopy(valid);v.update(change)
            with self.subTest(change=change),self.assertRaises(H.Failure):H.record('capture-report',v)
        v=copy.deepcopy(valid);del v['historical']
        with self.assertRaises(H.Failure):H.record('capture-report',v)
    def test_integer_boolean_is_not_integer(self):
        for v in (True,False,1.0,'1'):
            with self.assertRaises(H.Failure):H.validate(v,{'type':'integer'})
    def test_all_schema_keywords_are_supported(self):
        allowed={'$schema','$id','type','properties','required','additionalProperties','const','enum','oneOf','minLength','maxLength','pattern','minimum','items','minItems','maxItems'}
        def walk(s):
            self.assertFalse(set(s)-allowed)
            if 'properties' in s:
                self.assertEqual(set(s['required']),set(s['properties']));self.assertIs(s['additionalProperties'],False)
                for v in s['properties'].values():walk(v)
            if 'items' in s:walk(s['items'])
            for v in s.get('oneOf',[]):walk(v)
        for name in H.SCHEMAS:walk(H.schema(name.removeprefix('action-e-')))
    def test_tree_duplicate_traversal_and_membership(self):
        H.validate_tree(tree())
        for mutation in ('duplicate','dotdot','membership','bool','atime'):
            v=tree()
            if mutation=='duplicate':v['entries'].append(copy.deepcopy(v['entries'][0]))
            elif mutation=='dotdot':v['entries'][0]['path']=['2e2e']
            elif mutation=='membership':v['entries'][0]['children']=['61']
            elif mutation=='bool':v['entries'][0]['ino']=True
            else:v['entries'][0]['atime_ns']=0
            with self.subTest(mutation=mutation),self.assertRaises(H.Failure):H.validate_tree(v)
    def test_component_byte_encoding(self):
        self.assertEqual(H.component('ff61'),b'\xffa')
        for name in ('','2e','2e2e','2f','00','FF','a','61'*256):
            with self.assertRaises(H.Failure):H.component(name)
    def test_atime_is_excluded_and_all_other_identity_fields_count(self):
        self.assertEqual(H.token(info()),H.token(info(st_atime_ns=999)))
        for k in ('st_dev','st_ino','st_uid','st_gid','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns'):
            self.assertNotEqual(H.token(info()),H.token(info(**{k:getattr(info(),k)+1})))
    def test_entry_limit_schema(self):
        with mock.patch.object(H,'ENTRY_LIMIT',1):
            with self.assertRaises(H.Failure):H.validate([1,2],{'type':'array','items':{'type':'integer'}})
    def test_no_self_digest_inventory(self):
        inv=H.inventory({'x.json':b'abc'},0o600)
        self.assertEqual(inv,[dict(name='x.json',size=3,mode='0600',sha256=H.digest(b'abc'))])

class HistoricalEvidenceTests(unittest.TestCase):
    def e_doc(self):
        return {k:v['const'] for k,v in H.schema('handoff')['properties']['e_semantics']['properties'].items()}
    def evidence_call(self,raw,expected=None,stage='E_EVIDENCE',names=None):
        fs=mock.Mock();fs.open.return_value=directory(H.E_DIR)
        with mock.patch.object(H,'read_file',return_value=raw),mock.patch.object(H.os,'listdir',return_value=names or ['result.json']):return H.evidence(fs,H.E_DIR,expected or H.digest(raw),stage)
    def test_exact_e_record_matches_historical_digest(self):
        raw=H.canonical(self.e_doc());self.assertEqual(H.digest(raw),H.E_SHA);self.assertEqual(self.evidence_call(raw),raw)
    def test_e_bad_semantics_keys_digest_and_final_set(self):
        base=self.e_doc()
        for key,value in [('extra',1),('result','FAIL'),('rollback_recommended',0),('schema_version','2.0')]:
            v=copy.deepcopy(base);v[key]=value
            with self.assertRaises(H.Failure):self.evidence_call(H.canonical(v))
        v=copy.deepcopy(base);del v['action']
        with self.assertRaises(H.Failure):self.evidence_call(H.canonical(v))
        with self.assertRaises(H.Failure):self.evidence_call(H.canonical(base),'0'*64)
        with self.assertRaises(H.Failure):self.evidence_call(H.canonical(base),names=['result.json','.result.tmp'])
    def test_original_read_owner_mode_type_and_stability(self):
        d=directory();regular=info(st_mode=stat.S_IFREG|0o600)
        for change in ({'st_uid':999},{'st_gid':999},{'st_mode':stat.S_IFREG|0o644},{'st_mode':stat.S_IFLNK|0o600}):
            with mock.patch.object(H.os,'getuid',return_value=1000,create=True),mock.patch.object(H.os,'getgid',return_value=1000,create=True),mock.patch.object(H.os,'stat',return_value=info(**(vars(regular)|change))),self.assertRaises(H.Failure):H.read_file(d,'result.json','E_EVIDENCE')
    def test_root_rejection_precedes_tree(self):
        for k in ('dev','ino','uid','gid','mode'):
            fs=mock.Mock();d=directory();d.identity[k]='0700' if k=='mode' else 9;fs.open.return_value=d
            with mock.patch.object(H,'tree_entries') as walk,self.assertRaises(H.Failure):H.construction(fs,{})
            walk.assert_not_called()
    def test_wrong_marker_binding(self):
        fs=mock.Mock();fs.open.return_value=directory()
        with mock.patch.object(H,'read_file',return_value=b'{}\n'),mock.patch.object(H,'tree_entries') as walk,self.assertRaises(H.Failure):H.construction(fs,{})
        walk.assert_not_called()
    def test_bad_staging_path_precedes_open(self):
        for path in (H.CAPTURES/'e-abc', pathlib.Path('/tmp/e-'+'a'*32)):
            fs=mock.Mock()
            with self.assertRaises(H.Failure):H.staged(fs,path,'a'*64,'b'*40)
            fs.open.assert_not_called()
    def test_source_guard_separates_historical_commits(self):
        with self.assertRaises(H.Failure):H.source_guard('b'*40)
        with mock.patch.object(H,'SOURCE',H.REPOSITORY),mock.patch.object(H,'git',return_value=b'blob') as g,self.assertRaises(H.Failure):H.source_guard('b'*40)
        self.assertEqual(g.call_args[0][0],['cat-file','-t',H.D_COMMIT])
    def test_git_replacements_disabled_and_environment_bounded(self):
        done=types.SimpleNamespace(returncode=0,stdout=b'ok',stderr=b'')
        with mock.patch.object(H.subprocess,'run',return_value=done) as run:self.assertEqual(H.git(['status']),b'ok')
        args,kwargs=run.call_args;self.assertIn('--no-replace-objects',args[0]);self.assertEqual(kwargs['env']['GIT_NO_REPLACE_OBJECTS'],'1');self.assertNotIn('PYTHONPATH',kwargs['env'])

class TraversalTests(unittest.TestCase):
    def walk(self,names=None,kind=stat.S_IFREG,change=False):
        d=directory();root=info();leaf=info(st_ino=7,st_mode=kind|0o600,st_size=3)
        with contextlib.ExitStack() as s:
            s.enter_context(mock.patch.object(H.os,'O_NOFOLLOW',getattr(H.os,'O_NOFOLLOW',0x100),create=True));s.enter_context(mock.patch.object(H.os,'O_DIRECTORY',getattr(H.os,'O_DIRECTORY',0x200),create=True))
            s.enter_context(mock.patch.object(H.os,'listdir',side_effect=[names or [b'\xffa'],([] if change else names or [b'\xffa'])]))
            s.enter_context(mock.patch.object(H.os,'fstat',side_effect=[root,leaf,leaf,root]))
            s.enter_context(mock.patch.object(H.os,'stat',return_value=leaf));op=s.enter_context(mock.patch.object(H.os,'open',return_value=20));s.enter_context(mock.patch.object(H.os,'close'));s.enter_context(mock.patch.object(H.os,'read',side_effect=[b'abc',b'']))
            result=H.tree_entries(d)
            return result,op.call_args
    def test_actual_traversal_byte_filename_hash_no_follow(self):
        result,call=self.walk();self.assertEqual(result[1]['path'],['ff61']);self.assertEqual(result[1]['sha256'],H.digest(b'abc'));self.assertTrue(call[0][1]&getattr(H.os,'O_NOFOLLOW',0x100))
    def test_namespace_change_is_rejected(self):
        with self.assertRaises(H.Failure):self.walk(change=True)
    def test_special_file_rejected(self):
        with self.assertRaises(H.Failure):self.walk(kind=stat.S_IFIFO)
    def test_capture_forward_change_rejected(self):
        d=directory();t=tree()
        for field in ('ino','uid','gid','mode','mtime_ns','ctime_ns','size'):
            changed=copy.deepcopy(t['entries']);changed[0][field]='0700' if field=='mode' else 99
            with mock.patch.object(H,'tree_entries',return_value=changed),self.assertRaises(H.Failure):H.verify_construction(d,t)
    @unittest.skipUnless(H.os.name=='posix','real POSIX descriptor semantics require native validation')
    def test_real_posix_read_only_walk(self):
        import tempfile
        with tempfile.TemporaryDirectory() as t:
            p=pathlib.Path(t);(p/'file').write_bytes(b'abc');fd=H.os.open(p,H.os.O_RDONLY|H.os.O_DIRECTORY)
            try:
                d=H.Directory(fd,p);a=H.tree_entries(d);b=H.tree_entries(d);self.assertEqual(a,b)
            finally:H.os.close(fd)

if __name__=='__main__':unittest.main()

class AdditionalHistoricalTests(unittest.TestCase):
    def d_doc(self):
        return dict(schema_version='1.0',action='PE-4.0B.2a-D',governance_commit=H.D_COMMIT,result='PASS',error_code='NONE',failure_stage='COMPLETE',rollback_recommended=False,construction_directory=H.CONSTRUCTION.as_posix(),environment_identity=H.VERSION,wheel_sha256='86d7f0f8bdb25d2c632b72527325e4776430fd5bc61b9118de4e2b8ddb5f5b01',lock_sha256='19433d53e3015157207d1af4ef07930db6f0e0d525597485384b3b7d42628e96',installed_distributions={'pip':'23.0.1','setuptools':'66.1.1','websockets':'16.1.1'},input_snapshot_retained=False,eligibility_state='AWAITING_CONFIRMATION')
    def call_d(self,document):
        raw=H.canonical(document);fs=mock.Mock();fs.open.return_value=directory(H.D_DIR)
        with mock.patch.object(H,'read_file',return_value=raw),mock.patch.object(H.os,'listdir',return_value=['result.json']):return H.evidence(fs,H.D_DIR,H.digest(raw),'D_EVIDENCE')
    def test_d_exact_schema_and_values(self):
        self.assertEqual(self.call_d(self.d_doc()),H.canonical(self.d_doc()))
        for key in self.d_doc():
            v=self.d_doc();del v[key]
            with self.subTest(key=key),self.assertRaises(H.Failure):self.call_d(v)
    def test_d_wrong_lineage_result_and_distribution(self):
        for key,value in [('governance_commit',H.E_COMMIT),('construction_directory','/tmp/wrong'),('eligibility_state','CONFIRMED'),('rollback_recommended',0),('installed_distributions',{'pip':'1','websockets':'16.1.1','extra':'1'}),('installed_distributions',{'pip':True,'websockets':'16.1.1'}),('extra','x')]:
            v=self.d_doc();v[key]=value
            with self.subTest(key=key),self.assertRaises(H.Failure):self.call_d(v)
    def test_original_path_rejection(self):
        fs=mock.Mock()
        with self.assertRaises(H.Failure):H.evidence(fs,pathlib.Path('/tmp/alternate'),H.E_SHA,'E_EVIDENCE')
        fs.open.assert_not_called()
    def test_no_replace_success_checks_flag_and_fds(self):
        fn=mock.Mock(return_value=0)
        with mock.patch.object(H.ctypes,'CDLL',return_value=types.SimpleNamespace(renameat2=fn)):H.noreplace(directory(),'.stage','final')
        self.assertEqual(fn.call_args[0],(10,b'.stage',10,b'final',1))
    def test_schema_preservation_never_accepts(self):
        s=H.schema('continuity-attestation')
        self.assertEqual(s['properties']['approval_state'],{'const':'APPROVED_FOR_PRESERVATION'})
        self.assertEqual(s['properties']['historical_recursive_continuity_machine_proven'],{'const':False})
        self.assertEqual(H.schema('capture-report')['properties']['approval_state'],{'const':'PROPOSED'})
    def test_snapshot_symlink_target_records_are_exact(self):
        i=info(st_mode=stat.S_IFLNK|0o777)
        a=H.entry(i,['6c69623634'],'SYMLINK',target_hex='6c6962')
        b=H.entry(i,['6c69623634'],'SYMLINK',target_hex='616c74')
        self.assertNotEqual(H.canonical(a),H.canonical(b))
    def test_staged_manifest_digest_rejection_precedes_tree(self):
        fs=mock.Mock();fs.open.return_value=directory(H.CAPTURES/('e-'+'a'*32))
        with mock.patch.object(H,'read_file',return_value=b'{}\n'),self.assertRaises(H.Failure):H.staged(fs,H.CAPTURES/('e-'+'a'*32),'f'*64,'b'*40)
    def test_postwrite_mismatch_is_rejected(self):
        with mock.patch.object(H.os,'listdir',return_value=['x.json']),mock.patch.object(H,'read_file',return_value=b'changed'),self.assertRaises(H.Failure):H.check_files(directory(),{'x.json':b'original'},0o600,'POSTVALIDATION')
    def test_integer_overflow_is_rejected(self):
        with self.assertRaises(H.Failure):H.validate(2**100,{'type':'integer'})
    def test_low_level_io_failure_has_finite_stage(self):
        with mock.patch.object(H.os,'stat',side_effect=OSError('private text')),self.assertRaises(H.Failure) as exc:H.read_file(directory(),'x','D_EVIDENCE')
        self.assertEqual((exc.exception.code,exc.exception.stage),('IO_FAILED','D_EVIDENCE'));self.assertNotIn('private',str(exc.exception))

class OriginalPinTests(unittest.TestCase):
    def test_original_inode_replacement_rejected_even_with_same_bytes(self):
        fs=types.SimpleNamespace(evidence_pins={});d=directory(H.E_DIR)
        with mock.patch.object(H.os,'fstat',return_value=info()),mock.patch.object(H.os,'stat',side_effect=[info(st_mode=stat.S_IFREG|0o600),info(st_ino=99,st_mode=stat.S_IFREG|0o600)]):
            H.pin_original_evidence(fs,d,'E_EVIDENCE')
            with self.assertRaises(H.Failure):H.pin_original_evidence(fs,d,'E_EVIDENCE')
    def test_original_atime_difference_ignored(self):
        fs=types.SimpleNamespace(evidence_pins={});d=directory(H.E_DIR)
        with mock.patch.object(H.os,'fstat',return_value=info()),mock.patch.object(H.os,'stat',side_effect=[info(st_mode=stat.S_IFREG|0o600),info(st_atime_ns=900,st_mode=stat.S_IFREG|0o600)]):
            H.pin_original_evidence(fs,d,'E_EVIDENCE');H.pin_original_evidence(fs,d,'E_EVIDENCE')

class StaticConstructionTests(unittest.TestCase):
    def fixture(self):
        members={H.NATIVE:H.NATIVE_SHA,'websockets/__init__.py':'a'*64}
        cfg=b'home = /usr/bin\ninclude-system-site-packages = false\nversion = 3.11.2\n'
        marker=dict(schema_version='1.0',action='PE-4.0B.2a-D',governance_commit=H.D_COMMIT,construction_directory=H.CONSTRUCTION.as_posix(),environment_identity=H.VERSION,wheel_sha256='86d7f0f8bdb25d2c632b72527325e4776430fd5bc61b9118de4e2b8ddb5f5b01',lock_sha256='19433d53e3015157207d1af4ef07930db6f0e0d525597485384b3b7d42628e96',evidence_directory=H.D_DIR.as_posix(),evidence_sha256=H.D_SHA,result='PASS')
        files={(b'bin',b'python'):('b'*64,823209),(b'pyvenv.cfg',):(H.digest(cfg),9)}
        for name,sha in members.items():files[(b'lib',b'python3.11',b'site-packages')+tuple(p.encode() for p in name.split('/'))]=(sha,8)
        dirs={()}
        for key in files:
            for n in range(1,len(key)):dirs.add(key[:n])
        entries=[]
        for key in dirs:
            children=sorted({k[len(key)] for k in set(files)|dirs if len(k)>len(key) and k[:len(key)]==key and len(k)==len(key)+1})
            entries.append(H.entry(info(),[p.hex() for p in key],'DIRECTORY',children=[p.hex() for p in children]))
        for key,(sha,ino) in files.items():entries.append(H.entry(info(st_ino=ino,st_mode=stat.S_IFREG|0o640),[p.hex() for p in key],'REGULAR_FILE',sha256=sha))
        entries.sort(key=lambda e:tuple(bytes.fromhex(p) for p in e['path']))
        return members,cfg,marker,entries
    def call(self,mutation=None):
        members,cfg,marker,entries=self.fixture();fs=mock.Mock();fs.open.return_value=directory()
        if mutation:mutation(cfg,marker,entries)
        with mock.patch.object(H,'read_file',side_effect=[H.canonical(marker),cfg]) as reader,mock.patch.object(H,'tree_entries',return_value=entries):
            out=H.construction(fs,members);self.assertEqual(reader.call_args_list[-1].args[3],0o640);return out
    def test_static_members_and_safe_cfg_0640_pass_without_python(self):
        with mock.patch.object(H.subprocess,'run') as run:d,t=self.call()
        run.assert_not_called();self.assertEqual(t['bindings']['native_sha256'],H.NATIVE_SHA)
    def test_interpreter_native_and_member_mismatch_stop(self):
        for which in ('interpreter','native','member','owner','mode'):
            def mutate(cfg,marker,entries):
                for e in entries:
                    path=b'/'.join(bytes.fromhex(p) for p in e['path'])
                    if which=='interpreter' and path==b'bin/python':e['ino']=0
                    if which=='native' and path.endswith(H.NATIVE.encode()):e['sha256']='0'*64
                    if which=='member' and path.endswith(b'websockets/__init__.py'):e['sha256']='0'*64
                    if which=='owner':e['uid']=0
                    if which=='mode' and e['type']=='REGULAR_FILE':e['mode']='0666'
            with self.subTest(which=which),self.assertRaises(H.Failure):self.call(mutate)


class EvidenceAncestorTests(unittest.TestCase):
    def test_exact_root_owned_sticky_tmp_allowed(self):
        with mock.patch.object(H.os, 'getuid', return_value=1000, create=True):
            self.assertTrue(H.trusted_ancestor('/tmp', info(st_uid=0, st_gid=0, st_mode=stat.S_IFDIR | 0o1777)))
            for path, uid, gid, mode in [('/tmp', 1000, 0, 0o1777), ('/tmp', 0, 1000, 0o1777), ('/tmp', 0, 0, 0o777), ('/tmp/child', 0, 0, 0o1777), ('/other', 0, 0, 0o1777)]:
                with self.subTest(path=path, uid=uid, gid=gid, mode=mode):
                    self.assertFalse(H.trusted_ancestor(path, info(st_uid=uid, st_gid=gid, st_mode=stat.S_IFDIR | mode)))
