"""Windows-only synthetic integration; no production safety or execution claim."""
import ast
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import socket
import stat
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

from hioc import classification as model, classification_caller as caller, enrichment
from test_pe5_local_service_association import snapshot, OWNER, MAC

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('pe6_hostname_acceptance',ROOT/'tools/pe6_hostname_acceptance.py')
p=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(p)
HELPER=ROOT/'tools/pe6_protected_state_evidence.py'
HELPER_RAW=HELPER.read_bytes()
HELPER_SHA=hashlib.sha256(HELPER_RAW).hexdigest()
PRIVATE='/home/jazofv1/hioc/state/PRIVATE-host-192.0.2.1-aa:bb:cc:dd:ee:ff'
CODE='/home/jazofv1/hioc/pi4/lib/hioc/classification.py'
PRODUCER='/home/jazofv1/hioc/state/inventory/inventory.json'


def fingerprint(size=10):
    return [1,20,stat.S_IFREG|0o600,1000,1000,1,size,1000000,1000001]


def observation():
    directory='/home/jazofv1/hioc/state/enrichment/service_associations'
    producer={directory:[1,50,stat.S_IFDIR|0o700,1000,1000,2,4096,1,2],
        directory+'/current.json':fingerprint(4916),
        directory+'/current.durability.json':fingerprint(269),
        '/home/jazofv1/hioc/state':[1,4,stat.S_IFDIR|0o700,1000,1000,2,4096,1,2],
        '/home/jazofv1/hioc/state/enrichment':[1,5,stat.S_IFDIR|0o700,1000,1000,2,4096,1,2]}
    return dict(code={CODE:[fingerprint(),'a'*64]},configuration={},producer_state=producer,
        historical_journals={},runtime_root=[1,3,stat.S_IFDIR|0o755,1000,1000,1,4096,1,2],
        locks={},schedule={},user_crontab=[0,'b'*64,'c'*64])


class IntegratedAcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name).resolve()
        oldpath=list(sys.path);oldcache=sys.pycache_prefix
        oldmods={k:v for k,v in sys.modules.items() if k=='hioc' or k.startswith('hioc.')}
        def restore():
            sys.path[:]=oldpath;sys.pycache_prefix=oldcache
            for k in tuple(sys.modules):
                if k=='hioc' or k.startswith('hioc.') or k=='_pe6_verified_protected_evidence':sys.modules.pop(k,None)
            sys.modules.update(oldmods)
        self.addCleanup(restore)

    def case(self,*,primary=None,after=None,before=None,lazy=None,authorized=True,
             positive=True,review=False,truncated=False,helper_bad=False,output=False,expired_after=False,missing_report=False,source_swap=False):
        inv=snapshot();inv['updated']=caller._clock()
        host=enrichment.build_hostname_envelope(inv['devices'],
            enrichment.collect_hostname_candidates({OWNER:[dict(hostname='PRIVATE-camera' if positive else 'PRIVATE-neutral',source='integration:fixture')]},inv['updated']),None,inv['updated'])
        if primary=='input': inv['updated']='2000-01-01T00:00:00Z'
        if primary=='pair':host['generated_at']='2000-01-01T00:00:00Z'
        paths={}
        for k,v in [('inventory',inv),('hostname',host)]:
            f=self.root/(k+'.json');f.write_text(json.dumps(v),encoding='utf8');paths[k]=f
        originals={k:f.read_bytes() for k,f in paths.items()}
        a=observation();b=copy.deepcopy(a)
        pe5='/home/jazofv1/hioc/state/enrichment/service_associations'
        if before=='pe5_missing':a['producer_state'].pop(pe5)
        if before=='pe5_unsafe':a['producer_state'][pe5][2]=stat.S_IFDIR|0o755
        if after=='pe5_unsafe':b['producer_state'][pe5][4]=0
        if after=='pe5_substituted':b['producer_state'][pe5][1]+=1
        if after=='pe5_publication':
            b['producer_state'][pe5][7]+=1;b['producer_state'][pe5][8]+=1
            for suffix in ('/current.json','/current.durability.json'):
                b['producer_state'][pe5+suffix][1]+=100
                b['producer_state'][pe5+suffix][7]+=1;b['producer_state'][pe5+suffix][8]+=1
        if after in ('producer','permitted'):
            a['producer_state'][PRODUCER]=fingerprint()
            b['producer_state'][PRODUCER]=fingerprint(11)
        if after=='opaque': b['producer_state'][PRIVATE]=fingerprint()
        if after=='code':b['code'][CODE][1]='d'*64
        if after=='many':
            for i in range(70):b['producer_state'][PRIVATE+str(i)]=fingerprint(i)
        runtime_root=ROOT
        if source_swap:
            runtime_root=self.root/'runtime'
            for relative in p.MODULES:
                path=runtime_root/'pi4/lib'/relative;path.parent.mkdir(parents=True,exist_ok=True)
                path.write_bytes((ROOT/'pi4/lib'/relative).read_bytes())
        trace=[];side_effects=[];real_load=p.load_helper;active_caller=None;real_evaluate=None
        approved=sys.modules.get('hioc.core.compatibility')
        if lazy=='approved':sys.modules.pop('hioc.core.compatibility',None)
        def observe(pins):
            trace.append('protected')
            if trace.count('protected')==1:
                if before=='missing':return {}
                if before=='incomplete':raise p.Uncertain('PRIVATE observation')
                if before=='gate':raise p.Fail('PRIVATE protected')
                return a
            if source_swap:
                p.code_identity(runtime_root/'pi4/lib/hioc/classification.py',pins['pi4/lib/hioc/classification.py'],return_raw=True)
            if after=='fail':raise p.Fail('PRIVATE inspection')
            if after=='incomplete':raise p.Uncertain('PRIVATE inspection')
            return b
        def verify(pins,runtime):trace.append('origins');real_origins(pins,runtime)
        real_origins=p.verify_origins
        def evaluate(*args,**kwargs):
            trace.append('evaluate')
            self.assertEqual(set(args[0]),{'inventory','hostname'})
            self.assertEqual(set(kwargs),{'reader'})
            self.assertIsInstance(kwargs['reader'],active_caller.Reader)
            result=real_evaluate(*args,**kwargs)
            if primary=='evaluation':raise ValueError('PRIVATE_EXCEPTION '+OWNER)
            if primary=='functional':result['devices'][0]['role_suggestion'][0]['evidence_ids']=['0'*64]
            if primary=='aggregate':result['summary']['suggestion_count']+=1
            if primary=='confirmation':result['devices'][0]['operator_role']='camera'
            if primary=='changed':
                # Deliberate fixture fault, not a write by the instrument.
                with contextlib.ExitStack() as allow:
                    allow.enter_context(patch.object(os,'open',real_open))
                    with real_io_open(paths['hostname'],'ab') as stream:stream.write(b' ')
            if output:print('PRIVATE_OUTPUT')
            if lazy=='approved':
                import importlib
                importlib.import_module('hioc.core.compatibility')
            elif lazy:
                name='hioc.unexpected' if lazy=='unexpected' else 'hioc.enrichment'
                mod=types.ModuleType(name);mod.__file__=str(ROOT/'pi4/lib/hioc/enrichment.py')
                mod.__spec__=types.SimpleNamespace(name=name,origin=mod.__file__)
                if lazy=='outside':mod.__spec__.origin=str(self.root/'PRIVATE.py')
                sys.modules[name]=mod
            return result
        def identity(path,expected,**kwargs):
            trace.append('helper_identity')
            if path.name==HELPER.name:
                if expected!=HELPER_SHA:raise p.Fail('PRIVATE helper identity')
                return HELPER_RAW
            trace.pop()  # Runtime admission is distinct from helper identity.
            raw=path.read_bytes()
            if hashlib.sha256(raw).hexdigest()!=expected:raise p.Fail()
            return raw
        permits=[]
        if review:
            from dataclasses import asdict
            with patch.object(p,'code_identity',return_value=HELPER_RAW): h=real_load(HELPER_SHA)
            x=h.capture_protected(lambda:a);y=h.capture_protected(lambda:b)
            diff=json.loads(h.build_report(x,y,primary_outcome=dict(status='PASS'),protected_inspection_outcome=dict(status='PASS')))['object_differences'][0]
            permits=[asdict(h.ReviewedPermission(x.digest,y.digest,diff['artifact_id'],diff['difference_sha256'],'INVENTORY_ENGINE','SYNTHETIC_AUTHORIZATION','SYNTHETIC_ACCEPTANCE'))]
        def load(expected):
            h=real_load(expected);build=h.build_report
            def report(x,y,**kwargs):
                if missing_report:raise h.EvidenceError()
                if truncated:kwargs['max_differences']=1
                return build(x,y,**kwargs)
            h.build_report=report
            return h
        real_open=os.open;real_io_open=io.open;real_clock=caller._clock
        real_exec=p.VerifiedLoader.exec_module
        def exec_module(loader,module):
            nonlocal active_caller,real_evaluate
            if source_swap and module.__name__=='hioc.classification':
                # Fixture-only replacement after admission, before startup import.
                with real_io_open(runtime_root/'pi4/lib/hioc/classification.py','wb') as stream:
                    stream.write(b"raise RuntimeError('PRIVATE_REPLACEMENT_EXECUTED')\n")
            real_exec(loader,module)
            if module.__name__=='hioc.classification_caller':
                active_caller=module;real_evaluate=module.evaluate
                module.evaluate=evaluate;module._clock=clock
                module.Store.__init__=prohibited;module.AssetLock.__enter__=prohibited
        fixture_pins={path:hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
            for path in ['pi4/bin/hioc-classify-metadata.py',*['pi4/lib/'+x for x in p.MODULES]]}
        old_hioc={k:v for k,v in sys.modules.items() if k=='hioc' or k.startswith('hioc.')}
        for k in old_hioc:sys.modules.pop(k)
        self.addCleanup(lambda:sys.modules.update(old_hioc))
        def clock():
            if expired_after and trace.count('protected')==2: return '2100-01-01T00:00:00Z'
            return real_clock()
        def readonly(path,flags,*args,**kwargs):
            if flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND):
                side_effects.append('WRITE_OPEN');raise AssertionError('WRITE')
            return real_open(path,flags,*args,**kwargs)
        def io_readonly(file,mode='r',*args,**kwargs):
            if any(c in mode for c in 'wax+'):
                side_effects.append('WRITE_STREAM');raise AssertionError('WRITE')
            return real_io_open(file,mode,*args,**kwargs)
        def prohibited(*args,**kwargs):side_effects.append('SIDE_EFFECT');raise AssertionError('SIDE_EFFECT')
        facade=types.SimpleNamespace(**dict(vars(os),getuid=lambda:1000,getgid=lambda:1000,
            stat=lambda *args,**kwargs:types.SimpleNamespace(st_mode=stat.S_IFCHR)))
        out=io.StringIO();err=io.StringIO()
        with contextlib.ExitStack() as stack:
            for obj,key,value in [(p,'runtime_preflight',lambda:fixture_pins),
                (p,'R',runtime_root),(p,'PATHS',paths),(p,'protected',observe),(p,'verify_origins',verify),
                (p,'code_identity',identity),(p,'load_helper',load),(p.VerifiedLoader,'exec_module',exec_module)]:
                stack.enter_context(patch.object(obj,key,value))
            stack.enter_context(patch.object(os,'open',side_effect=readonly))
            stack.enter_context(patch.object(io,'open',side_effect=io_readonly))
            for obj,key in [(os,'write'),(os,'mkdir'),(os,'rename'),(os,'replace'),(os,'unlink'),(os,'chmod'),
                (socket,'socket'),(subprocess,'run'),(caller.Store,'__init__'),(caller.AssetLock,'__enter__')]:
                stack.enter_context(patch.object(obj,key,side_effect=prohibited))
            stack.enter_context(contextlib.redirect_stdout(out));stack.enter_context(contextlib.redirect_stderr(err))
            raw=p.run('SYNTHETIC_NEW_APPROVAL' if authorized else None,'SYNTHETIC_EXPIRY_ADOPTION',
                      '0'*64 if helper_bad else HELPER_SHA,reviewed_permissions=permits)
        r=json.loads(raw)
        self.assertEqual(side_effects,[]);self.assertEqual(out.getvalue()+err.getvalue(),'')
        self.assertLessEqual(len(raw),65536);self.assertLessEqual(trace.count('evaluate'),1)
        self.assertEqual(r['classification_invocations'],trace.count('evaluate'))
        self.assertEqual(len(list(self.root.iterdir())),3 if source_swap else 2)
        if primary!='changed':self.assertEqual(originals,{k:f.read_bytes() for k,f in paths.items()})
        for secret in ('PRIVATE',OWNER,MAC,'192.0.2.1','aa:bb:cc',str(self.root),'/home/jazofv1/hioc/state/'):
            self.assertNotIn(secret.encode(),raw)
        return r,trace

    def test_second_execution_references_cannot_authorize_another_run(self):
        for authorization,expiry in [('PE64_20261019_SECOND_ACCEPTANCE','SYNTHETIC_EXPIRY_ADOPTION'),
                ('SYNTHETIC_NEW_APPROVAL','PE64_20261019_FROZEN_PE1_DISPOSITION')]:
            with patch.object(p,'runtime_preflight',side_effect=AssertionError('must not run')) as preflight:
                result=json.loads(p.run(authorization,expiry,HELPER_SHA))
            self.assertEqual(result['RESULT'],'FAIL');self.assertEqual(result['classification_invocations'],0)
            preflight.assert_not_called()

    def test_required_pe5_security_evidence_emitted_with_one_call(self):
        r,t=self.case()
        e=r['protected_evidence']['pe5_endpoint_evidence']
        self.assertEqual(r['RESULT'],'PASS');self.assertEqual(t.count('evaluate'),1)
        for label in ('before','after'):
            endpoint=e['endpoints'][label];directory=endpoint['artifacts'][0]
            self.assertEqual(directory['mode'],'0700')
            self.assertEqual(directory['fingerprint']['st_uid'],'1000')
            self.assertEqual(directory['fingerprint']['st_gid'],'1000')
            self.assertEqual(endpoint['security_status'],'PASS')

    def test_missing_pe5_baseline_prevents_classification(self):
        r,t=self.case(before='pe5_missing')
        self.assertEqual(r['RESULT'],'INSUFFICIENT_EVIDENCE');self.assertNotIn('evaluate',t)
        self.assertEqual(r['classification_invocations'],0)

    def test_unsafe_pe5_baseline_prevents_classification(self):
        r,t=self.case(before='pe5_unsafe')
        self.assertEqual(r['RESULT'],'FAIL');self.assertNotIn('evaluate',t)
        self.assertEqual(r['protected_evidence']['pe5_endpoint_evidence']['endpoints']['before']['artifacts'][0]['mode'],'0755')

    def test_after_security_failure_preserves_functional_success(self):
        r,t=self.case(after='pe5_unsafe')
        self.assertEqual(r['RESULT'],'FAIL');self.assertEqual(t.count('evaluate'),1)
        self.assertEqual(r['primary_outcome']['status'],'PASS')
        self.assertEqual(r['protected_inspection_outcome']['status'],'FAIL')

    def test_directory_substitution_synchronizes_independent_outcomes(self):
        r,t=self.case(after='pe5_substituted')
        self.assertEqual(r['RESULT'],'FAIL');self.assertEqual(t.count('evaluate'),1)
        self.assertEqual(r['primary_outcome']['status'],'PASS')
        self.assertEqual(r['protected_inspection_outcome'],r['protected_evidence']['protected_inspection_outcome'])
        self.assertEqual(r['protected_inspection_outcome']['status'],'FAIL')

    def test_pe5_publication_retains_endpoints_without_self_permission(self):
        r,t=self.case(after='pe5_publication')
        self.assertEqual(r['RESULT'],'INSUFFICIENT_EVIDENCE');self.assertEqual(t.count('evaluate'),1)
        e=r['protected_evidence'];self.assertEqual(e['changed_object_count'],3)
        self.assertTrue(all(d['adjudication']=='UNATTRIBUTED' for d in e['object_differences']))
        self.assertEqual(len(e['pe5_endpoint_evidence']['endpoints']['after']['artifacts']),3)

    def test_unchanged_success(self):
        r,t=self.case();self.assertEqual(r['RESULT'],'PASS');self.assertEqual(t.count('protected'),2)
    def test_specific_independently_reviewed_producer_activity(self):
        r,t=self.case(after='permitted',review=True);self.assertEqual(r['RESULT'],'PASS')
        self.assertEqual(r['protected_evidence']['object_differences'][0]['adjudication'],'PERMITTED_CONFIRMED')
    def test_unattributed_producer_delta(self):
        r,t=self.case(after='producer');self.assertEqual(r['RESULT'],'INSUFFICIENT_EVIDENCE')
    def test_prohibited_code_drift(self):
        r,t=self.case(after='code');self.assertEqual(r['RESULT'],'FAIL')
    def test_incomplete_before_prevents_call(self):
        r,t=self.case(before='incomplete');self.assertEqual(r['RESULT'],'INSUFFICIENT_EVIDENCE');self.assertEqual(t.count('evaluate'),0);self.assertEqual(t.count('protected'),1)
    def test_known_before_gate_prevents_call_and_fails(self):
        r,t=self.case(before='gate');self.assertEqual(r['RESULT'],'FAIL');self.assertEqual(t.count('evaluate'),0)
    def test_primary_failure_after_success(self):
        r,t=self.case(primary='evaluation');self.assertEqual(r['RESULT'],'FAIL');self.assertEqual(r['primary_outcome']['stage'],'SINGLE_EVALUATION');self.assertEqual(r['protected_inspection_outcome']['status'],'PASS')
    def test_primary_and_protected_failure_retained(self):
        r,t=self.case(primary='evaluation',after='fail');self.assertEqual(r['RESULT'],'FAIL');self.assertEqual(r['primary_outcome']['stage'],'SINGLE_EVALUATION');self.assertEqual(r['protected_inspection_outcome']['status'],'FAIL')
    def test_primary_failure_and_after_incomplete(self):
        r,t=self.case(primary='evaluation',after='incomplete');self.assertEqual(r['RESULT'],'FAIL');self.assertEqual(r['protected_inspection_outcome']['status'],'INCOMPLETE')
    def test_primary_success_after_incomplete(self):
        r,t=self.case(after='incomplete');self.assertEqual(r['RESULT'],'INSUFFICIENT_EVIDENCE');self.assertEqual(r['primary_outcome']['status'],'PASS')
    def test_truncated_diff_cannot_pass(self):
        r,t=self.case(after='many',truncated=True);self.assertEqual(r['RESULT'],'INSUFFICIENT_EVIDENCE');self.assertEqual(r['protected_evidence']['omitted_object_count'],69)
    def test_opaque_private_path(self):
        r,t=self.case(after='opaque');self.assertTrue(r['protected_evidence']['object_differences'][0]['artifact_id'].startswith('OBJECT_'))
    def test_wrong_helper_identity_prevents_capture_or_call(self):
        r,t=self.case(helper_bad=True);self.assertEqual(r['RESULT'],'FAIL');self.assertEqual(t,['helper_identity'])
    def test_unexpected_lazy_module(self):
        r,t=self.case(lazy='unexpected');self.assertEqual(r['RESULT'],'FAIL');self.assertEqual(r['primary_outcome']['stage'],'POST_EVALUATION_MODULE_ORIGINS')
    def test_wrong_lazy_origin(self):
        r,t=self.case(lazy='outside');self.assertEqual(r['RESULT'],'FAIL')
    def test_approved_lazy_module(self):
        r,t=self.case(lazy='approved');self.assertEqual(r['RESULT'],'PASS');self.assertEqual(t.count('origins'),2)
    def test_invalid_selected_input(self):
        r,t=self.case(primary='input');self.assertEqual(r['RESULT'],'FAIL');self.assertEqual(t.count('evaluate'),0);self.assertEqual(t.count('protected'),2)
    def test_exact_generation_pair_required(self):
        r,t=self.case(primary='pair');self.assertEqual(r['RESULT'],'FAIL');self.assertEqual(t.count('evaluate'),0)
    def test_input_changed_during_evaluation(self):
        r,t=self.case(primary='changed');self.assertEqual(r['RESULT'],'FAIL');self.assertEqual(t.count('evaluate'),1)
    def test_optional_sources_not_selected(self):
        r,t=self.case();f=r['functional'];self.assertEqual(f['summary']['unavailable_source_count'],5)
        omitted=[s for s in f['sources'] if s['selection']=='NOT_SELECTED'];self.assertEqual(len(omitted),5)
        self.assertTrue(all(s['state']=='ABSENT' and s['sha256'] is None for s in omitted))
    def test_zero_suggestions_distinct_from_failed_classification(self):
        r,t=self.case(positive=False);self.assertEqual(r['RESULT'],'INSUFFICIENT_EVIDENCE');self.assertEqual(r['primary_outcome']['status'],'PASS');self.assertEqual(r['functional']['summary']['suggestion_count'],0)
    def test_valid_role_provenance_and_counts(self):
        r,t=self.case();f=r['functional'];self.assertEqual(f['summary']['device_count'],1);self.assertEqual(f['summary']['suggestion_count'],1);self.assertEqual(sum(f['suggestions_by_rule'].values()),1)
    def test_wrong_evidence_rejected(self):
        r,t=self.case(primary='functional');self.assertEqual(r['RESULT'],'FAIL');self.assertEqual(r['functional'],{})
    def test_wrong_aggregate_rejected(self):
        r,t=self.case(primary='aggregate');self.assertEqual(r['RESULT'],'FAIL')
    def test_operator_confirmation_rejected(self):
        r,t=self.case(primary='confirmation');self.assertEqual(r['RESULT'],'FAIL')
    def test_exactly_once_no_retry(self):
        r,t=self.case(primary='evaluation');self.assertEqual(t.count('evaluate'),1);self.assertEqual(t.count('protected'),2)
    def test_no_persistence_locks_network_or_service_calls(self):
        r,t=self.case();self.assertEqual(r['RESULT'],'PASS');self.assertFalse(r['private_output_persisted']);self.assertFalse(r['recurring_activation_performed'])
    def test_authorization_gate(self):
        r,t=self.case(authorized=False);self.assertEqual(r['RESULT'],'FAIL');self.assertEqual(t,[])
    def test_historical_authorizations_not_reusable(self):
        for ref in ('CHAT_20261019_PE64_SINGLE_RUN','ARCH_20261019_FROZEN_PE1_SCHEMA'):
            with patch.object(p,'runtime_preflight',side_effect=AssertionError('must not reach')) as gate:
                r=json.loads(p.run(ref,'SYNTHETIC_EXPIRY_ADOPTION',HELPER_SHA));self.assertEqual(r['RESULT'],'FAIL');gate.assert_not_called()
    def test_private_stdout_becomes_sanitized_failure(self):
        r,t=self.case(output=True);self.assertEqual(r['RESULT'],'FAIL')
    def test_bounded_private_failure_receipt(self):
        r,t=self.case(primary='evaluation',after='fail');self.assertLessEqual(len(p.encode(r)+b'\n'),65536)
    def test_preflight_failure_no_capture(self):
        with patch.object(p,'runtime_preflight',side_effect=ValueError('PRIVATE'*100000)):
            r=p.run('SYNTHETIC_NEW_APPROVAL','SYNTHETIC_EXPIRY_ADOPTION',HELPER_SHA)
        self.assertLess(len(r),4096);self.assertNotIn(b'PRIVATE',r);self.assertEqual(json.loads(r)['classification_invocations'],0)
    def test_helper_loader_uses_verified_same_bytes(self):
        with patch.object(p,'code_identity',return_value=HELPER_RAW) as identity:
            h=p.load_helper(HELPER_SHA)
        identity.assert_called_once_with(HELPER,HELPER_SHA,return_raw=True)
        self.assertTrue(callable(h.capture_protected));self.assertTrue(callable(h.build_report))
    def test_protected_observer_shapes_are_helper_compatible(self):
        with patch.object(p,'code_identity',return_value=HELPER_RAW):h=p.load_helper(HELPER_SHA)
        proc=self.root/'proc';proc.mkdir()
        import pathlib
        original_iter=pathlib.Path.iterdir
        def iterdir(path):return iter(()) if path.as_posix()=='/proc' else original_iter(path)
        facade=types.SimpleNamespace(**dict(vars(os),getpid=lambda:0))
        with patch.object(p,'R',Path('/home/jazofv1/hioc')),patch.object(p,'os',facade),patch.object(pathlib.Path,'iterdir',iterdir),patch.object(pathlib.Path,'glob',return_value=iter(())),patch.object(pathlib.Path,'lstat',return_value=types.SimpleNamespace(**dict(zip(h.FIELDS,observation()['runtime_root'])))),patch.object(p,'command',return_value=(0,b'',b'')),patch.object(p,'metadata',side_effect=lambda path,*args:{str(path):fingerprint()}),patch.object(p,'code_identity',return_value=[fingerprint(),'a'*64]):
            cap=h.capture_protected(lambda:p.protected({'pi4/lib/hioc/classification.py':'a'*64}))
        self.assertEqual(cap.completeness,'COMPLETE')
        self.assertIn(('code',str(Path(CODE))),cap._objects);self.assertIn(('schedule',str(Path('/etc/crontab'))),cap._objects)
    def test_expiry_during_protected_after_scan_cannot_pass(self):
        r,t=self.case(expired_after=True);self.assertEqual(r['RESULT'],'FAIL');self.assertEqual(r['primary_outcome']['stage'],'FINAL_TIME_CHECK');self.assertEqual(r['protected_inspection_outcome']['status'],'PASS')
    def test_substituted_helper_bytes_rejected_before_execution(self):
        with patch.object(p,'code_identity',return_value=b"raise Exception('PRIVATE substituted helper')"):
            with self.assertRaises(p.Fail):p.load_helper(HELPER_SHA)
    def test_missing_before_category_blocks_classification(self):
        r,t=self.case(before='missing');self.assertEqual(r['RESULT'],'INSUFFICIENT_EVIDENCE');self.assertEqual(r['classification_invocations'],0)
    def test_missing_diff_report_cannot_pass(self):
        r,t=self.case(missing_report=True);self.assertEqual(r['RESULT'],'FAIL');self.assertEqual(r['protected_inspection_outcome']['status'],'PASS')
    def test_report_failure_cannot_replace_original_primary_failure(self):
        r,t=self.case(primary='evaluation',after='fail',missing_report=True);self.assertEqual(r['primary_outcome']['stage'],'SINGLE_EVALUATION');self.assertEqual(r['protected_inspection_outcome']['status'],'FAIL')
    def test_runtime_preflight_pins_exact_committed_sources_and_inventory_variant(self):
        observed=[]
        def command(argv):
            self.assertEqual([v.replace(chr(92),'/') for v in argv[:3]],['/usr/bin/git','--git-dir=/home/jazofv1/hioc-release-source/.git','cat-file'])
            self.assertEqual(argv[3],'blob');observed.append(argv[-1])
            return 0,subprocess.check_output(['git','cat-file','blob',argv[-1]],cwd=ROOT),b''
        facade=types.SimpleNamespace(**dict(vars(os),getuid=lambda:1000,getgid=lambda:1000,
            stat=lambda *args,**kwargs:types.SimpleNamespace(st_mode=stat.S_IFCHR)))
        with patch.object(p,'os',facade),patch.object(p.socket,'gethostname',return_value='nutandpihole'),patch.object(p.sys,'flags',types.SimpleNamespace(isolated=True,no_site=True)),patch.object(p.sys,'dont_write_bytecode',True),patch.object(p,'command',side_effect=command):
            pins=p.runtime_preflight()
        self.assertEqual(len(pins),22);self.assertEqual(len(observed),22)
        self.assertEqual(pins['pi4/lib/hioc/inventory.py'],'df1dc4e2de7d8d77b54acdcb3f340281ead6cc03d74a73ad59b2864b03564503')
        self.assertEqual(pins['pi4/lib/hioc/classification.py'],'feda2fc41c374d84728e1601b616875cda8289f489fbd903c107409a8fa5a2f6')
    def test_actual_run_executes_admitted_source_and_detects_disk_replacement(self):
        r,t=self.case(source_swap=True)
        self.assertEqual(r['primary_outcome']['status'],'PASS')
        self.assertEqual(r['protected_inspection_outcome']['status'],'FAIL')
        self.assertEqual(r['RESULT'],'FAIL');self.assertEqual(r['classification_invocations'],1)
    def test_python311_syntax_and_single_evaluate_callsite(self):
        tree=ast.parse((ROOT/'tools/pe6_hostname_acceptance.py').read_text(encoding='utf8'),feature_version=(3,11))
        self.assertEqual(sum(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='evaluate' for n in ast.walk(tree)),1)


class VerifiedRuntimeTests(unittest.TestCase):
    """Native Windows source fixtures; POSIX ownership gates are NOT claimed tested."""
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name).resolve();self.pins={}
        self.old={n:m for n,m in sys.modules.items() if n=='hioc' or n.startswith('hioc.')}
        for n in self.old:sys.modules.pop(n)
        self.addCleanup(self.restore)
        self.patchroot=patch.object(p,'R',self.root);self.patchroot.start();self.addCleanup(self.patchroot.stop)
        for relative in p.MODULES:
            raw=b"VALUE = 'ADMITTED'\n"
            if relative=='hioc/__init__.py':raw=b"from .core import capabilities\nPACKAGE_READY = True\n"
            if relative=='hioc/core/__init__.py':raw=b"from . import logging\n"
            if relative=='hioc/classification.py':
                raw=b"from . import classification_contract\nVALUE = classification_contract.VALUE\ndef lazy():\n    from .core import monitoring\n    return monitoring.VALUE\n"
            path=self.root/'pi4/lib'/relative;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
            self.pins['pi4/lib/'+relative]=hashlib.sha256(raw).hexdigest()
        self.pins['pi4/bin/hioc-classify-metadata.py']='a'*64
        def read(path,expected,**kwargs):
            raw=path.read_bytes();p.need(hashlib.sha256(raw).hexdigest()==expected);return raw
        self.identity=patch.object(p,'code_identity',side_effect=read)
        self.identity.start();self.addCleanup(self.identity.stop)
        self.registry=None

    def restore(self):
        if self.registry:self.registry.close()
        for n in tuple(sys.modules):
            if n=='hioc' or n.startswith('hioc.'):sys.modules.pop(n,None)
        sys.modules.update(self.old)

    def admitted(self):
        self.registry=p.VerifiedRuntime(self.pins);self.registry.__enter__();return self.registry

    def load(self,name):return importlib.import_module(name)

    def test_approved_relative_import_and_package_initialization(self):
        r=self.admitted();module=self.load('hioc.classification')
        self.assertEqual(module.VALUE,'ADMITTED');self.assertTrue(sys.modules['hioc'].PACKAGE_READY)
        p.verify_origins(self.pins,r)
        self.assertEqual(set(r.sources),{'hioc' if x=='hioc/__init__.py' else 'hioc.core' if x=='hioc/core/__init__.py' else x[:-3].replace('/','.') for x in p.MODULES})

    def test_startup_source_replacement_never_executes(self):
        r=self.admitted();path=self.root/'pi4/lib/hioc/classification.py'
        path.write_bytes(b"raise RuntimeError('PRIVATE_REPLACEMENT')\n")
        module=self.load('hioc.classification');self.assertEqual(module.VALUE,'ADMITTED')
        p.verify_origins(self.pins,r)
        with self.assertRaises(p.Fail):p.code_identity(path,self.pins['pi4/lib/hioc/classification.py'],return_raw=True)

    def test_lazy_source_replacement_never_executes(self):
        self.admitted();module=self.load('hioc.classification')
        self.assertNotIn('hioc.core.monitoring',sys.modules)
        path=self.root/'pi4/lib/hioc/core/monitoring.py'
        path.write_bytes(b"raise RuntimeError('PRIVATE_LAZY_REPLACEMENT')\n")
        self.assertEqual(module.lazy(),'ADMITTED')
        self.assertIsInstance(sys.modules['hioc.core.monitoring'].__loader__,p.VerifiedLoader)

    def test_ordinary_source_loader_not_consulted_or_cache_written(self):
        import importlib.machinery
        self.admitted();before={str(x.relative_to(self.root)):x.read_bytes() for x in self.root.rglob('*') if x.is_file()}
        with patch.object(importlib.machinery.SourceFileLoader,'get_data',side_effect=AssertionError('UNVERIFIED_READ')),patch.object(importlib.machinery.SourceFileLoader,'get_code',side_effect=AssertionError('PYC_READ')),patch.object(importlib.machinery.SourceFileLoader,'set_data',side_effect=AssertionError('PYC_WRITE')):
            module=self.load('hioc.classification');self.assertEqual(module.lazy(),'ADMITTED')
        self.assertEqual(before,{str(x.relative_to(self.root)):x.read_bytes() for x in self.root.rglob('*') if x.is_file()})

    def test_unexpected_module_fails_without_fallback(self):
        self.admitted();self.load('hioc')
        with self.assertRaises(p.Fail):self.load('hioc.unapproved')

    def test_alternate_package_path_rejected_before_lazy_import(self):
        self.admitted();module=self.load('hioc.classification')
        sys.modules['hioc.core'].__path__.append(str(self.root/'PRIVATE_OTHER'))
        with self.assertRaises(p.Fail):module.lazy()

    def test_changed_module_origin_rejected(self):
        r=self.admitted();module=self.load('hioc.classification')
        module.__spec__.origin=str(self.root/'PRIVATE_OTHER.py')
        with self.assertRaises(p.Fail):p.verify_origins(self.pins,r)

    def test_preloaded_module_blocks_registry_before_admission(self):
        sys.modules['hioc']=types.ModuleType('hioc')
        with patch.object(p,'code_identity',side_effect=AssertionError('MUST_NOT_ADMIT')):
            with self.assertRaises(p.Fail):p.VerifiedRuntime(self.pins)

    def test_inserted_cached_module_cannot_pass_provenance(self):
        r=self.admitted();self.load('hioc')
        fake=types.ModuleType('hioc.classification')
        fake.__file__=str(self.root/'pi4/lib/hioc/classification.py')
        fake.__spec__=types.SimpleNamespace(name=fake.__name__,origin=fake.__file__)
        sys.modules[fake.__name__]=fake
        with self.assertRaises(p.Fail):p.verify_origins(self.pins,r)

    def test_wrong_digest_stops_before_any_hioc_execution(self):
        self.pins['pi4/lib/hioc/classification.py']='0'*64
        with self.assertRaises(p.Fail):self.admitted()
        self.assertFalse(any(n=='hioc' or n.startswith('hioc.') for n in sys.modules))

    def test_reload_or_duplicate_execution_rejected(self):
        self.admitted();module=self.load('hioc.classification')
        with self.assertRaises(p.Fail):importlib.reload(module)
        with self.assertRaises(p.Fail):module.__loader__.exec_module(module)

    def test_context_removal_discards_admitted_module_cache(self):
        r=self.admitted();self.load('hioc.classification');r.close()
        self.assertNotIn(r,sys.meta_path)
        self.assertFalse(any(n=='hioc' or n.startswith('hioc.') for n in sys.modules))

    def test_extension_or_namespace_module_cannot_enter_registry(self):
        self.admitted();self.load('hioc')
        for name in ('hioc.unapproved_extension','hioc.unapproved_namespace'):
            with self.subTest(name=name):
                with self.assertRaises(p.Fail):self.load(name)

    def test_registry_bytes_are_immutable_and_allowlist_not_extended(self):
        r=self.admitted();self.assertEqual(len(r.sources),21)
        with self.assertRaises(TypeError):r.sources['hioc.unapproved']=('PRIVATE',b'',False)


if __name__=='__main__':unittest.main()
