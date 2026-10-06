import contextlib
import io
import unittest
from unittest import mock
from pathlib import PurePosixPath
import builtins
import importlib.metadata
import importlib.machinery
import os
import sys
import sysconfig
import tempfile
import types
import json
import subprocess
from pathlib import Path

from tools import hioc_pe4_action_g as G


def faithful_f_transaction():
    """Serialize real F journal records; never run F's executor or preflight."""
    from tests.test_pe4_action_f_runtime import Memory, bindings
    backend=Memory()
    bound=bindings();bound['current_consumer']=G.F_CONSUMER
    state=G.F.initial_state();state['recovery']=True
    journal=G.F.Journal(backend,G.F_ID,bound,state)
    journal.append('PREPARED')
    for operation in G.F.OPERATIONS:
        journal.append(operation+'_INTENT')
        backend.confirm(operation,bound)
        if operation=='CLIENT':state['publication']='CLIENT_ONLY'
        if operation=='ENVIRONMENT':state['publication']='ENVIRONMENT_PUBLISHED'
        if operation=='ACTIVE_SWITCH':state['publication']='ACTIVE_SWITCHED'
        journal.append(operation+'_CONFIRMED')
    journal.append('POST_VERIFIED')
    state['evidence']='UNCONFIRMED'
    result=G.F.record(journal.document('RESULT'))
    backend.files['result.json']=result
    digest=G.H.digest(result)
    state['evidence']='CONFIRMED'
    journal.append('RESULT_REFERENCE',digest)
    state['publication']='COMPLETE';state['recovery']=False
    journal.append('COMMITTED',digest)
    journal.verify(result)
    return backend.files,bound


def reseal(files):
    """Reseal synthetic hashes so each negative test reaches semantic checks."""
    previous='NONE'
    for i in range(14):
        name=f'{i:04}.json';doc=G.H.parse(files[name],'STAGED_INPUT')
        doc['previous_record_sha256']=previous
        if i==12:
            result=G.H.parse(files['result.json'],'STAGED_INPUT')
            result['previous_record_sha256']=previous
            files['result.json']=G.H.canonical(result)
        if i>=12:doc['result_sha256']=G.H.digest(files['result.json'])
        files[name]=G.H.canonical(doc);previous=G.H.digest(files[name])


class FJournalRecoveryTests(unittest.TestCase):
    def validate(self,files):
        # Production paths are POSIX; preserve their spelling on Windows.
        with mock.patch.object(G,'FINAL',PurePosixPath(G.FINAL.as_posix())), mock.patch.object(G,'CLIENT',PurePosixPath(G.CLIENT.as_posix())):
            return G.validate_f(files,G.H.digest(files['result.json']),G.H.digest(files['0013.json']))

    def mutate(self,files,name,field,value):
        doc=G.H.parse(files[name],'STAGED_INPUT');doc[field]=value
        files[name]=G.H.canonical(doc);reseal(files)

    def test_successful_real_f_serialization_and_incomplete_recovery_states(self):
        files,bound=faithful_f_transaction()
        for i in range(13):
            self.assertIs(G.H.parse(files[f'{i:04}.json'],'STAGED_INPUT')['recovery_required'],True)
        self.assertIs(G.H.parse(files['result.json'],'STAGED_INPUT')['recovery_required'],True)
        self.assertIs(G.H.parse(files['0013.json'],'STAGED_INPUT')['recovery_required'],False)
        self.assertEqual(self.validate(files),bound)

    def test_committed_recovery_true_is_rejected(self):
        files,_=faithful_f_transaction();self.mutate(files,'0013.json','recovery_required',True)
        with self.assertRaises(G.Failure):self.validate(files)

    def test_every_incomplete_record_must_require_recovery(self):
        for name in [*(f'{i:04}.json' for i in range(13)),'result.json']:
            with self.subTest(name=name):
                files,_=faithful_f_transaction();self.mutate(files,name,'recovery_required',False)
                with self.assertRaises(G.Failure):self.validate(files)

    def test_publication_and_evidence_progression_are_exact(self):
        for name in [*(f'{i:04}.json' for i in range(14)),'result.json']:
            for field in ('publication_state','evidence_state'):
                with self.subTest(name=name,field=field):
                    files,_=faithful_f_transaction();old=G.H.parse(files[name],'STAGED_INPUT')[field]
                    alternatives=('NONE','COMPLETE') if field=='publication_state' else ('NOT_CREATED','CONFIRMED')
                    self.mutate(files,name,field,next(v for v in alternatives if v!=old))
                    with self.assertRaises(G.Failure):self.validate(files)

    def test_exact_result_and_committed_digests_remain_mandatory(self):
        files,_=faithful_f_transaction();r=G.H.digest(files['result.json']);c=G.H.digest(files['0013.json'])
        for rd,cd in [('0'*64,c),(r,'0'*64)]:
            with self.assertRaises(G.Failure):G.validate_f(files,rd,cd)
        with self.assertRaises(G.Failure):G.validate_f(files)  # Synthetic bytes cannot satisfy production pins.

    def test_chain_order_sequence_and_file_set_remain_mandatory(self):
        for field,value in [('previous_record_sha256','0'*64),('event','CLIENT_CONFIRMED'),('sequence',3)]:
            files,_=faithful_f_transaction();doc=G.H.parse(files['0001.json'],'STAGED_INPUT');doc[field]=value
            files['0001.json']=G.H.canonical(doc)
            if field!='previous_record_sha256':reseal(files)
            with self.assertRaises(G.Failure):self.validate(files)
        for extra in (False,True):
            files,_=faithful_f_transaction()
            if extra:files['extra.json']=b'{}\n'
            else:files.pop('0000.json')
            with self.assertRaises(G.Failure):self.validate(files)

    def test_result_reference_and_pass_contracts_remain_mandatory(self):
        for name in ('0000.json','0012.json','0013.json','result.json'):
            for field,value in [('rollback_recommended',True),('error_code','MISMATCH'),('failure_stage','HANDOFF')]:
                files,_=faithful_f_transaction();self.mutate(files,name,field,value)
                with self.assertRaises((G.Failure,G.H.Failure)):self.validate(files)
        files,_=faithful_f_transaction();doc=G.H.parse(files['0012.json'],'STAGED_INPUT')
        doc['result_sha256']='0'*64;files['0012.json']=G.H.canonical(doc)
        with self.assertRaises(G.Failure):self.validate(files)


class DistributionOrderingTests(unittest.TestCase):
    expected={'pip':'23.0.1','setuptools':'66.1.1','websockets':'16.1.1'}

    def seed(self,site,pairs):
        for i,(name,version) in enumerate(pairs):
            directory=site/f'{name}-{i}.dist-info';directory.mkdir(parents=True)
            (directory/'METADATA').write_text(f'Metadata-Version: 2.1\nName: {name}\nVersion: {version}\n',encoding='utf-8')

    def test_standard_distribution_discovery_disappears_without_pathfinder(self):
        with tempfile.TemporaryDirectory() as root:
            site=Path(root);self.seed(site,list(self.expected.items()))
            original=list(sys.meta_path)
            try:
                self.assertEqual({d.metadata['Name']:d.version for d in importlib.metadata.distributions(path=[str(site)])},self.expected)
                sys.meta_path=[G.Finder({'paths':list(sys.path)}),importlib.machinery.BuiltinImporter,importlib.machinery.FrozenImporter]
                self.assertEqual(list(importlib.metadata.distributions(path=[str(site)])),[])
            finally:sys.meta_path=original

    def run_probe(self,pairs,success):
        # Mock target-only startup facts; run real child_probe and real metadata
        # discovery. Stop at the first package import, before any package code.
        original_meta=list(sys.meta_path);original_path=list(sys.path)
        real_import=builtins.__import__;real_distributions=importlib.metadata.distributions
        events=[]
        class PackageBoundary(Exception):pass
        with tempfile.TemporaryDirectory() as root:
            site=Path(root)/'lib/python3.11/site-packages';site.mkdir(parents=True)
            self.seed(site,pairs)
            sentinel=Path(root)/'EXECUTED'
            (site/'websockets').mkdir()
            (site/'websockets/__init__.py').write_text(f"raise AssertionError('package executed before restriction')\n",encoding='utf-8')
            (site/'sentinel.pth').write_text(f"import pathlib;pathlib.Path({str(sentinel)!r}).touch()\n",encoding='utf-8')
            (site/'sitecustomize.py').write_text("raise AssertionError('site customization')\n",encoding='utf-8')
            interpreter=Path(root)/'interpreter';interpreter.write_bytes(b'fixture')
            fd=os.open(interpreter,os.O_RDONLY);info=os.fstat(fd)
            policy={'root':root,'paths':original_path,'version':list(sys.version_info[:3]),'soabi':sysconfig.get_config_var('SOABI'),
                'fd':fd,'identity':G.H.identity(info),'interpreter':{},'distributions':dict(self.expected)}
            flags=types.SimpleNamespace(**{n:getattr(sys.flags,n) for n in dir(sys.flags) if not n.startswith('_')})
            flags.isolated=flags.no_site=flags.ignore_environment=1
            def discover(*args,**kwargs):
                self.assertEqual(kwargs,{'path':[root+'/lib/python3.11/site-packages']})
                self.assertEqual(sys.meta_path,original_meta)
                self.assertEqual(events,['prohibitions'])
                events.append('metadata')
                return real_distributions(*args,**kwargs)
            def guarded_import(name,*args,**kwargs):
                if name=='websockets' or name.startswith('websockets.'):
                    self.assertEqual(events,['prohibitions','metadata'])
                    self.assertIsInstance(sys.meta_path[0],G.Finder)
                    self.assertEqual(sys.meta_path[1:],[importlib.machinery.BuiltinImporter,importlib.machinery.FrozenImporter])
                    self.assertNotIn(importlib.machinery.PathFinder,sys.meta_path)
                    events.append('package');raise PackageBoundary()
                return real_import(name,*args,**kwargs)
            try:
                with contextlib.ExitStack() as stack:
                    stack.enter_context(mock.patch.object(sys,'flags',flags))
                    stack.enter_context(mock.patch.object(sys,'dont_write_bytecode',True))
                    stack.enter_context(mock.patch.object(sys,'prefix','/usr'))
                    stack.enter_context(mock.patch.object(sys,'base_prefix','/usr'))
                    stack.enter_context(mock.patch.dict(sys.modules,{}))
                    sys.modules.pop('site',None)
                    stack.enter_context(mock.patch.object(G.os.path,'lexists',return_value=False))
                    stack.enter_context(mock.patch.object(G,'verified_open',side_effect=lambda *a:(os.dup(fd),b'fixture')))
                    stack.enter_context(mock.patch.object(G,'child_expected',return_value=G.child_token(os.stat(sys.executable))))
                    stack.enter_context(mock.patch.dict(os.environ,G.ENV,clear=True))
                    stack.enter_context(mock.patch.object(G,'install_prohibitions',side_effect=lambda:events.append('prohibitions')))
                    stack.enter_context(mock.patch.object(importlib.metadata,'distributions',side_effect=discover))
                    stack.enter_context(mock.patch.object(builtins,'__import__',side_effect=guarded_import))
                    with self.assertRaises(PackageBoundary if success else RuntimeError):G.child_probe(policy)
                self.assertEqual(events,['prohibitions','metadata','package'] if success else ['prohibitions','metadata'])
                self.assertFalse(sentinel.exists())
                self.assertEqual(sys.path,original_path)
            finally:
                sys.meta_path=original_meta;sys.path=original_path;os.close(fd)

    def test_exact_dictionary_accepted_before_restricted_package_phase(self):
        self.run_probe(list(self.expected.items()),True)

    def test_isolated_metadata_scan_executes_no_package_pth_or_site_hooks(self):
        with tempfile.TemporaryDirectory() as root:
            site=Path(root);self.seed(site,list(self.expected.items()))
            sentinel=site/'EXECUTED';package=site/'websockets';package.mkdir()
            payload=f"import pathlib;pathlib.Path({str(sentinel)!r}).touch()\n"
            (package/'__init__.py').write_text(payload,encoding='utf-8')
            (site/'bad.pth').write_text(payload,encoding='utf-8')
            (site/'sitecustomize.py').write_text(payload,encoding='utf-8')
            code="import sys,json,importlib.metadata as m; assert sys.flags.no_site and sys.dont_write_bytecode and 'site' not in sys.modules; print(json.dumps({d.metadata['Name']:d.version for d in m.distributions(path=[sys.argv[1]])})); assert 'websockets' not in sys.modules"
            env=dict(G.ENV)
            if os.name=='nt':env['SYSTEMROOT']=os.environ['SYSTEMROOT']
            result=subprocess.run([sys.executable,'-I','-B','-S','-c',code,str(site)],env=env,stdin=subprocess.DEVNULL,capture_output=True,timeout=10)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(json.loads(result.stdout),self.expected)
            self.assertFalse(sentinel.exists());self.assertFalse(list(site.rglob('*.pyc')))

    def test_missing_extra_duplicate_and_wrong_version_rejected_before_import(self):
        good=list(self.expected.items())
        variants=[good[:-1],good+[('unexpected','1')],good+[good[0]],[(n,'0' if n=='websockets' else v) for n,v in good]]
        for pairs in variants:
            with self.subTest(pairs=pairs):self.run_probe(pairs,False)

    def test_generated_startup_and_existing_client_loader_restrictions(self):
        script=G.child_script({})
        self.assertLess(script.index('distributions=list(metadata.distributions'),script.index('finder=Finder(policy);sys.meta_path='))
        self.assertLess(script.index('finder=Finder(policy);sys.meta_path='),script.index('\n    import websockets\n'))
        self.assertIn('sys.flags.no_site',script);self.assertIn('sys.dont_write_bytecode',script)
        self.assertNotIn('site.main(',script);self.assertNotIn('addsitedir(',script)
        self.assertIn('verified_open',script);self.assertIn('InvalidStatus(response)',script)
        self.assertIn("client.detect_websocket_client()=='PYTHON_WEBSOCKETS'",script)


class ActionGRuntimeTests(unittest.TestCase):
    def test_entrypoint_is_thin_and_controlled(self):
        source = open("tools/hioc-pe4-runtime-preflight.py", encoding="utf-8").read()
        self.assertIn("from hioc_pe4_action_g import cli", source)
        self.assertIn("--governance-commit", open("tools/hioc_pe4_action_g.py", encoding="utf-8").read())

    def test_invalid_arguments_fail_before_backend(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            rc = G.cli(["--governance-commit", "bad"], lambda: self.fail("backend"))
        self.assertEqual(rc, 2)
        self.assertIn("RESULT=FAIL", output.getvalue())

    def test_no_shared_probe_or_lifecycle_executor(self):
        source = open("tools/hioc_pe4_action_g.py", encoding="utf-8").read()
        self.assertNotIn("CAPABILITY_PROBE", source)
        self.assertNotIn("verify_repository(", source)
        self.assertNotIn("hioc-pe4-runtime-rollback.py", source)

    def test_network_and_credentials_are_explicitly_denied(self):
        with self.assertRaises(RuntimeError):
            G.deny_network()
        with self.assertRaises(RuntimeError):
            G.deny_credentials()

    def test_f_constants_are_pinned(self):
        self.assertEqual(G.F_ID, "17fc3e0580ff007cdcd619ed2e2d3b34")
        self.assertEqual(G.F_RESULT, "d647c7b2241d7800a3c819cf86459e2be95c3ef58581d5ffef2dbf5bd1190941")
        self.assertEqual(G.F_COMMITTED, "24bb64cc8d885297e5696ddd733ec0dfab4b28a24e18a6996b667c186f2016e9")

    def test_bounded_output_rejects_overflow(self):
        with self.assertRaises(G.Failure) as caught:
            G.bounded(["/usr/bin/python3", "-I", "-B", "-S", "-c", "print('x'*10000)"], "PROBE", limit=100)
        self.assertIn(caught.exception.code, {"OUTPUT_LIMIT", "IO_FAILED"})
