"""End-to-end workflow orchestration with deterministic syscall fault injection."""
import contextlib, copy, ctypes, errno, io, pathlib, types, unittest
from unittest import mock
from tools import hioc_pe4_action_e_handoff as H
from tests.test_pe4_action_e_handoff import directory, tree, report

class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.stack=contextlib.ExitStack();self.addCleanup(self.stack.close);self.files={};self.calls=[]
        self.d=directory();self.parent=directory(H.CAPTURES,11);self.stage=directory(H.CAPTURES/('e-'+'a'*32),12);self.bundle=directory(H.HANDOFFS/'.action-e-test',13)
        self.fs=mock.Mock();self.fs.parent.side_effect=lambda path,stage:self.parent
        self.fs.child.side_effect=self.child
        self.fs.open.side_effect=lambda path,*args:self.bundle if pathlib.Path(path).parent==H.HANDOFFS else self.d
        self.patch('Filesystem',return_value=self.fs);self.patch('target_guard');self.patch('source_guard',return_value={});self.patch('publication_guard');self.patch('absent');self.patch('construction',return_value=(self.d,tree()))
        self.patch('evidence',side_effect=lambda fs,path,*args:b'E' if path==H.E_DIR else b'D')
        self.patch('write_file',side_effect=self.write);self.patch('sync',side_effect=lambda *args:self.calls.append(('sync',args[2])));self.patch('check_files',side_effect=self.check)
        self.patch('verify_construction');self.patch('noreplace',side_effect=lambda *args:self.calls.append(('rename',args)))
        self.stack.enter_context(mock.patch.object(H.secrets,'token_hex',return_value='a'*32))
        self.stack.enter_context(mock.patch.object(H.os,'listdir',return_value=[]));self.stack.enter_context(mock.patch.object(H.os,'fchmod',create=True))
        self.stack.enter_context(mock.patch.object(H.os,'fstat',return_value=types.SimpleNamespace(st_dev=45826,st_ino=823199,st_uid=1000,st_gid=1000,st_mode=0o40500)))
    def patch(self,name,**kwargs):return self.stack.enter_context(mock.patch.object(H,name,**kwargs))
    def child(self,parent,name,mode,stage):
        self.calls.append(('child',stage));d=self.stage if stage=='STAGING_ALLOCATION' else self.bundle;d.path=parent.path/name;return d
    def write(self,d,name,raw,mode,stage):self.calls.append(('write',name,mode));self.files[name]=raw
    def check(self,d,payloads,mode,stage):
        for k,v in payloads.items():
            if self.files.get(k)!=v:H.fail(stage,'MISMATCH')
    def state(self):return dict(path='NONE',digest='NONE',evidence='UNCONFIRMED')
    def preserve_fixture(self):
        t=tree();r=report(t);payloads={'action-e-result.json':b'E','action-d-result.json':b'D','construction-tree.json':H.canonical(t,H.TREE_LIMIT),'capture-report.json':H.canonical(r),'capture-manifest.json':b'M'}
        self.files.update(payloads);self.patch('staged',return_value=(self.stage,payloads,t,r));return t,payloads,r
    def test_capture_full_workflow_keeps_proposed_and_original_bytes(self):
        state=self.state();H.capture('b'*40,'test-authorization',state)
        self.assertEqual(state['evidence'],'CONFIRMED');self.assertEqual(self.files['action-e-result.json'],b'E')
        m=H.parse(self.files['capture-manifest.json'],'STAGED_INPUT');self.assertEqual(m['approval_state'],'PROPOSED');self.assertNotIn('capture-manifest.json',[x['name'] for x in m['inventory']])
        r=H.parse(self.files['capture-report.json'],'STAGED_INPUT');self.assertFalse(r['historical_recursive_continuity_machine_proven']);self.assertEqual(r['approval_state'],'PROPOSED')
        self.assertEqual(len([x for x in self.calls if x[0]=='child']),1);H.noreplace.assert_not_called()
    def test_capture_each_failure_retains_locator_and_closes(self):
        for name,stage in [('write_file','STAGING_WRITE'),('sync','STAGING_FSYNC'),('check_files','POSTVALIDATION'),('verify_construction','POSTVALIDATION')]:
            with self.subTest(name=name),mock.patch.object(H,name,side_effect=H.Failure('IO_FAILED',stage)):
                state=self.state()
                with self.assertRaises(H.Failure):H.capture('b'*40,'test',state)
                self.assertIn('/captures/e-',state['path'].replace('\\','/'));self.assertEqual(state['evidence'],'UNCONFIRMED')
        self.assertGreaterEqual(self.fs.close.call_count,4)
    def test_capture_allocation_collision_no_retry(self):
        self.fs.child.side_effect=H.Failure('CONFLICT','STAGING_ALLOCATION');state=self.state()
        with self.assertRaises(H.Failure):H.capture('b'*40,'test',state)
        self.fs.child.assert_called_once();self.assertIn('/captures/e-',state['path'].replace('\\','/'))
    def test_capture_post_original_evidence_change(self):
        H.evidence.side_effect=[b'E',b'D',b'changed']
        with self.assertRaises(H.Failure):H.capture('b'*40,'test',self.state())
    def test_preservation_full_workflow_no_new_baseline_or_acceptance(self):
        self.preserve_fixture();self.parent.path=H.HANDOFFS;state=self.state()
        H.preserve('c'*40,self.stage.path,'f'*64,'b'*40,'test',state)
        H.construction.assert_not_called();self.assertEqual(state['evidence'],'CONFIRMED');H.noreplace.assert_called_once()
        final={x[1] for x in self.calls if x[0]=='write'}
        self.assertEqual(final,{'action-e-result.json','action-d-result.json','construction-tree.json','continuity-attestation.json','manifest.json'})
        att=H.parse(self.files['continuity-attestation.json'],'STAGED_INPUT');self.assertEqual(att['approval_state'],'APPROVED_FOR_PRESERVATION');self.assertFalse(att['historical_recursive_snapshot_persisted']);self.assertFalse(att['historical_recursive_continuity_machine_proven'])
        self.assertIn('NO_AUTHORIZED_POST_E_HIOC_MUTATION_RECORDED',att['governed_chronology']);self.assertNotIn('ACCEPTED',self.files['manifest.json'].decode())
    def test_preservation_failure_boundaries_never_retry(self):
        self.preserve_fixture();self.parent.path=H.HANDOFFS
        for name,stage in [('staged','STAGED_INPUT'),('evidence','E_EVIDENCE'),('verify_construction','POSTVALIDATION'),('write_file','BUNDLE_WRITE'),('sync','BUNDLE_FSYNC'),('noreplace','BUNDLE_PUBLICATION'),('check_files','FINAL_VALIDATION')]:
            with self.subTest(name=name),mock.patch.object(H,name,side_effect=H.Failure('IO_FAILED',stage)):
                state=self.state()
                with self.assertRaises(H.Failure):H.preserve('c'*40,self.stage.path,'f'*64,'b'*40,'test',state)
                self.assertEqual(state['evidence'],'UNCONFIRMED')
    def test_existing_preservation_staging_is_not_adopted(self):
        self.preserve_fixture();self.parent.path=H.HANDOFFS
        with mock.patch.object(H.os,'listdir',return_value=['.action-e-stale']),self.assertRaises(H.Failure):H.preserve('c'*40,self.stage.path,'f'*64,'b'*40,'test',self.state())
        self.fs.child.assert_not_called()
    def test_cli_dispatch_once_and_fixed_terminal(self):
        for action in ('capture','preserve'):
            args=['--governance-commit','b'*40,'--authorization-reference','test']
            if action=='preserve':args+=['--capture-directory',str(self.stage.path),'--capture-manifest-sha256','f'*64,'--capture-source-commit','b'*40,'--approval-state','APPROVED_FOR_PRESERVATION']
            with mock.patch.object(H,action) as launch,contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(H.cli(action,args),0);launch.assert_called_once()
            self.assertIn('CONTINUITY_ACCEPTED=FALSE',output.getvalue());self.assertTrue(output.getvalue().endswith('STOP_REQUIRED=TRUE\n'))
    def test_cli_bad_arguments_finite_failure(self):
        for args in ([],['--governance-commit','short','--authorization-reference','x'],['--governance-commit','b'*40,'--authorization-reference','bad\nref']):
            with contextlib.redirect_stdout(io.StringIO()) as out:self.assertEqual(H.cli('capture',args),2)
            self.assertIn('FAILURE_STAGE=ARGUMENTS',out.getvalue())
    def test_cli_failure_and_unexpected_are_sanitized(self):
        for error,code in ((H.Failure('MISMATCH','POSTVALIDATION'),'MISMATCH'),(RuntimeError('secret'),'UNEXPECTED_ERROR')):
            with mock.patch.object(H,'capture',side_effect=error),contextlib.redirect_stdout(io.StringIO()) as out:self.assertEqual(H.cli('capture',['--governance-commit','b'*40,'--authorization-reference','x']),1)
            self.assertIn('ERROR_CODE='+code,out.getvalue());self.assertNotIn('secret',out.getvalue())

class PrimitiveTests(unittest.TestCase):
    def test_no_replace_errno_matrix_and_no_fallback(self):
        for error,code in [(errno.EEXIST,'CONFLICT'),(errno.ENOSYS,'UNAVAILABLE'),(errno.EINVAL,'UNAVAILABLE'),(errno.EOPNOTSUPP,'UNAVAILABLE'),(errno.EXDEV,'UNAVAILABLE'),(errno.EIO,'IO_FAILED')]:
            fn=mock.Mock(return_value=-1)
            with mock.patch.object(H.ctypes,'CDLL',return_value=types.SimpleNamespace(renameat2=fn)),mock.patch.object(H.ctypes,'get_errno',return_value=error),mock.patch.object(H.os,'replace') as replace,self.assertRaises(H.Failure) as exc:H.noreplace(directory(),'.staged','final')
            self.assertEqual(exc.exception.code,code);replace.assert_not_called();self.assertEqual(fn.call_args[0][-1],1)
    def test_no_replace_unavailable(self):
        with mock.patch.object(H.ctypes,'CDLL',return_value=types.SimpleNamespace()),self.assertRaises(H.Failure):H.noreplace(directory(),'.staged','final')
    def test_exclusive_partial_write_and_file_fsync(self):
        d=directory()
        with mock.patch.object(H.os,'O_NOFOLLOW',getattr(H.os,'O_NOFOLLOW',0x100),create=True),mock.patch.object(H.os,'open',return_value=7) as op,mock.patch.object(H.os,'write',side_effect=[2,1]) as write,mock.patch.object(H.os,'fchmod',create=True),mock.patch.object(H.os,'fsync') as sync,mock.patch.object(H.os,'close'):
            H.write_file(d,'x.json',b'abc',0o600,'STAGING_WRITE');self.assertEqual(write.call_count,2);sync.assert_called_once_with(7);self.assertTrue(op.call_args[0][1]&H.os.O_EXCL)
    def test_file_fsync_failure_retains_file_and_closes(self):
        with mock.patch.object(H.os,'O_NOFOLLOW',0x100,create=True),mock.patch.object(H.os,'open',return_value=7),mock.patch.object(H.os,'write',return_value=3),mock.patch.object(H.os,'fchmod',create=True),mock.patch.object(H.os,'fsync',side_effect=OSError()),mock.patch.object(H.os,'close') as close,mock.patch.object(H.os,'unlink') as unlink,self.assertRaises(H.Failure):H.write_file(directory(),'x.json',b'abc',0o600,'STAGING_WRITE')
        close.assert_called_once_with(7);unlink.assert_not_called()
    def test_directory_and_parent_fsync_failures(self):
        for sequence in ([OSError()],[None,OSError()]):
            with mock.patch.object(H.os,'fsync',side_effect=sequence),self.assertRaises(H.Failure):H.sync(directory(),directory(fd=11),'STAGING_FSYNC')
    def test_unexpected_final_file_set_rejected(self):
        with mock.patch.object(H.os,'listdir',return_value=['unexpected']),self.assertRaises(H.Failure):H.check_files(directory(),{'result.json':b'a'},0o600,'POSTVALIDATION')
    def test_lifecycle_forbidden_writes_are_absent(self):
        source=(H.REPOSITORY/'tools/hioc_pe4_action_e_handoff.py').read_text(encoding='utf-8')
        for value in ('os.unlink(', 'os.rmdir(', 'shutil.', 'os.replace(', 'import websockets', 'cleanup_owned_directory(', 'controlled_capabilities('):self.assertNotIn(value,source)
        self.assertFalse((H.REPOSITORY/'governance/pe4/accepted-action-e.json').exists())

if __name__=='__main__':unittest.main()
