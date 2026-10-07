"""Repository-only preparation contracts and interruption tests; no Linux target I/O."""
import ast
import contextlib
from functools import lru_cache
import copy
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import sys
import stat
import subprocess
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "tools/hioc-pe4-ha-association-deploy.py"
spec = importlib.util.spec_from_file_location("pe4_deployment", HELPER)
D = importlib.util.module_from_spec(spec); spec.loader.exec_module(D)
R = json.loads((ROOT / D.RECORD).read_bytes())
COMMIT = "a" * 40

@lru_cache(maxsize=None)
def source_bytes(path):
    if path in ('tools/hioc-pe4-ha-association-deploy.py','pi4/lib/hioc/home_assistant_association.py'):return (ROOT/path).read_bytes()
    return subprocess.check_output(['git','show',D.BASELINE+':'+path],cwd=ROOT)


class SyntheticFS:
    uid = gid = 1000
    def __init__(self):
        self.files = {}; self.dirs = {}; self.modes = {}; self.unsafe = set(); self.mutations = []
        for p in ("pi4", "pi4/lib", "pi4/lib/hioc", "pi4/lib/hioc/core", "pi4/bin", "config", "state", "state/inventory", "backups", "governance", "governance/pe4"):
            self.dirs[p] = 0o755
        self.files[D.CONFIG] = b'# unchanged\nHIOC_HOME="/home/jazofv1/hioc"\nOTHER="keep"\n'
        self.modes[D.CONFIG] = 0o640
        self.files["config/toolkit.conf"] = b"";self.modes["config/toolkit.conf"] = 0o644
        for item in R["production_dependencies"]:
            self.files[item["path"]] = source_bytes(item["path"]); self.modes[item["path"]] = 0o644
    def read(self, p, mode=None):
        D.require(p not in self.unsafe, "UNSAFE_OBJECT")
        if p in self.files and mode is not None: D.require(self.modes[p] == mode, "UNSAFE_OBJECT")
        return self.files.get(p)
    def info(self, p):
        if p in self.dirs: return SimpleNamespace(st_uid=1000,st_gid=1000,st_mode=stat.S_IFDIR | self.dirs[p],st_dev=1)
        if p in self.files: return SimpleNamespace(st_uid=1000,st_gid=1000,st_mode=stat.S_IFREG | self.modes[p],st_dev=1)
        return None
    def check_directory(self,p,mode=None):
        D.require(p not in self.unsafe and p not in self.files, "UNSAFE_OBJECT")
        if p not in self.dirs:return False
        if mode is not None:D.require(self.dirs[p]==mode,"UNSAFE_OBJECT")
        return True
    def names(self,p):
        prefix=p+"/"
        return [n[len(prefix):] for n in self.files.keys() | self.dirs.keys() if n.startswith(prefix) and "/" not in n[len(prefix):]]
    def parents(self,p):
        result=[]; parent=PurePosixPath(p).parent
        while str(parent)!=".":result.append(str(parent));parent=parent.parent
        return list(reversed(result))
    def preflight_install(self,p): return None
    def mkdir(self,p,mode):
        if p in self.dirs:D.require(self.dirs[p]==mode,"UNSAFE_OBJECT");return
        D.require(str(PurePosixPath(p).parent) in self.dirs,"UNSAFE_OBJECT")
        self.dirs[p]=mode;self.mutations.append("mkdir:"+p)
    def add(self,p,raw,mode):
        D.require(str(PurePosixPath(p).parent) in self.dirs,"UNSAFE_OBJECT")
        if p in self.files:D.require(self.files[p]==raw and self.modes[p]==mode,"DESTINATION_CONFLICT");return
        self.files[p]=raw;self.modes[p]=mode;self.mutations.append("add:"+p)
    def replace_config(self,prior,candidate,mode):
        D.require(self.files[D.CONFIG]==prior,"CONFIG_CONFLICT")
        self.files[D.CONFIG]=candidate;self.modes[D.CONFIG]=mode;self.mutations.append("replace:config")
    @contextlib.contextmanager
    def lock(self):yield

def manifest():
    return {"dependencies":copy.deepcopy(R["production_dependencies"]),
            "deploy":[dict(i,bytes=source_bytes(i["path"])) for i in R["deployment_files"]]}

class DeploymentPreparationTests(unittest.TestCase):
    def setUp(self):self.fs=SyntheticFS();self.m=manifest()
    def expect_failure(self,code,call):
        with self.assertRaises(D.Failure) as e:call()
        self.assertEqual(e.exception.code,code)
    def test_module_exact_identity(self):
        self.assertEqual(R["deployment_files"][0]["git_blob"],"e71e4c45e21e9f1a25298471b48387cb19f53e1f")
        self.assertEqual(R["deployment_files"][0]["sha256"],"9a9be5812f3481146de7546875320eb6adec65ca5a2b3230ff5fec378892c7c1")
    def test_entrypoint_exact_identity(self):
        self.assertEqual(R["deployment_files"][1]["git_blob"],"2864361fac7cd48e947dac1e4e40aeeeb525adef")
        self.assertEqual(R["deployment_files"][1]["sha256"],"005fae482a4e2c42b48bfb991abf14ddf1d9de60f81169a2ed1573a767958b8c")
    def test_all_current_source_bindings(self):
        for i in R["source_bindings"]:
            raw=source_bytes(i["path"])
            self.assertEqual((ROOT/i['path']).read_bytes().replace(b'\r\n',b'\n'),raw)
            self.assertEqual(D.sha(raw),i["sha256"],i["path"])
            self.assertEqual(hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest(),i["git_blob"])
    def test_complete_dependency_manifest(self):
        self.assertEqual({i["path"] for i in R["production_dependencies"]},{"pi4/lib/hioc/__init__.py","pi4/lib/hioc/core/__init__.py","pi4/lib/hioc/core/config.py","pi4/lib/hioc/core/compatibility.py","pi4/lib/hioc/core/state.py","pi4/lib/hioc/core/schemas.py"})
        tree=ast.parse((ROOT/'pi4/lib/hioc/home_assistant_association.py').read_text())
        local={n.module for n in ast.walk(tree) if isinstance(n,ast.ImportFrom) and n.level}
        self.assertEqual(local,{'core.config','core.compatibility','core.state'})
        self.assertIn('from .schemas import Schema',(ROOT/'pi4/lib/hioc/core/state.py').read_text())
    def test_complete_governance_manifest_from_contract_source(self):
        source=(ROOT/'pi4/lib/hioc/home_assistant_association.py').read_text()
        tree=ast.parse(source)
        strings={n.value for n in ast.walk(tree) if isinstance(n,ast.Constant) and isinstance(n.value,str)}
        paths={v for v in strings if v.startswith('governance/') and v.endswith('.json')}
        self.assertEqual({i['path'] for i in R['runtime_governance']},paths)
        for i in R['runtime_governance']:self.assertIn(i['sha256'],strings)
    def test_source_production_separation(self):
        for i in R['deployment_files']+R['production_dependencies']:
            self.assertEqual(i['source'],D.SOURCE.as_posix()+'/'+i['path']);self.assertEqual(i['production'],D.HOME.as_posix()+'/'+i['path'])
        self.assertNotEqual(D.HOME,D.SOURCE)
    def test_effective_config_precedence_and_home(self):
        candidate=D.endpoint_config(b'HIOC_HOME="/home/jazofv1/hioc"\n')
        D.effective_configuration(b'HIOC_HOME="wrong"\nHIOC_HA_ENDPOINT="wrong"\n',candidate)
        self.expect_failure('CONFIG_CONFLICT',lambda:D.effective_configuration(b'HIOC_HOME="wrong"\n',D.endpoint_config(b'')))
    def test_endpoint_absent_append(self):
        raw=self.fs.read(D.CONFIG);new=D.endpoint_config(raw)
        self.assertTrue(new.startswith(raw));self.assertEqual(new[len(raw):],('HIOC_HA_ENDPOINT="'+D.ENDPOINT+'"\n').encode())
    def test_endpoint_exact_idempotent(self):
        raw=D.endpoint_config(self.fs.read(D.CONFIG));self.assertEqual(D.endpoint_config(raw),raw)
    def test_duplicate_endpoint_fails(self):
        raw=D.endpoint_config(b'');self.expect_failure('CONFIG_CONFLICT',lambda:D.endpoint_config(raw+raw))
    def test_different_endpoint_fails(self):
        self.expect_failure('CONFIG_CONFLICT',lambda:D.endpoint_config(b'HIOC_HA_ENDPOINT="invalid"\n'))
    def test_unrelated_config_bytes_preserved(self):
        for raw in (b'# comment\r\nOTHER="x"\r\n',b'OTHER=last',b'OTHER=\n',b''):
            self.assertTrue(D.endpoint_config(raw).startswith(raw))
    def test_export_endpoint_ambiguity_fails(self):
        self.expect_failure('CONFIG_CONFLICT',lambda:D.endpoint_config(b'export HIOC_HA_ENDPOINT="invalid"\n'))
    def test_dependency_mismatch_fails_without_mutation(self):
        self.fs.files[self.m['dependencies'][0]['path']]=b'drift';self.expect_failure('DEPENDENCY_DRIFT',lambda:D.deploy(self.fs,self.m,COMMIT));self.assertFalse(self.fs.mutations)
    def test_missing_dependency_fails_without_mutation(self):
        del self.fs.files[self.m['dependencies'][0]['path']];self.expect_failure('DEPENDENCY_DRIFT',lambda:D.deploy(self.fs,self.m,COMMIT));self.assertFalse(self.fs.mutations)
    def test_adapter_destination_absent(self):D.preflight(self.fs,self.m);self.assertFalse(self.fs.mutations)
    def test_adapter_destination_exact(self):
        for i in self.m['deploy']:self.fs.files[i['path']]=i['bytes'];self.fs.modes[i['path']]=int(i['mode'],8)
        D.deploy(self.fs,self.m,COMMIT)
        self.assertFalse(any('add:'+i['path'] in self.fs.mutations for i in self.m['deploy']))
    def test_adapter_destination_different_fails(self):
        p=self.m['deploy'][0]['path'];self.fs.files[p]=b'drift';self.fs.modes[p]=0o644
        self.expect_failure('DESTINATION_CONFLICT',lambda:D.deploy(self.fs,self.m,COMMIT));self.assertFalse(self.fs.mutations)
    def test_association_directory_absent_create(self):
        D.deploy(self.fs,self.m,COMMIT);self.assertEqual(self.fs.dirs[D.ASSOCIATIONS],0o700)
    def test_valid_association_directory_preserved(self):
        self.fs.dirs[D.ASSOCIATIONS]=0o700;D.deploy(self.fs,self.m,COMMIT);self.assertNotIn('mkdir:'+D.ASSOCIATIONS,self.fs.mutations)
    def test_insecure_association_directory_fails(self):
        for mode in (0o755,0o770,0o777):
            self.fs.dirs[D.ASSOCIATIONS]=mode;self.expect_failure('UNSAFE_OBJECT',lambda:D.preflight(self.fs,self.m))
    def test_unsafe_symlink_special_owner_acl_binding_fail(self):
        for p in (D.ASSOCIATIONS,D.LOCK,self.m['deploy'][0]['path']):
            self.fs.unsafe={p};self.expect_failure('UNSAFE_OBJECT',lambda:D.preflight(self.fs,self.m))
    def test_unexpected_state_stops(self):self.private_state('home_assistant.json')
    def test_unexpected_transaction_stops(self):self.private_state('.home_assistant.txn-known')
    def test_unexpected_done_stops(self):self.private_state('.home_assistant.done-known')
    def private_state(self,name):
        self.fs.dirs[D.ASSOCIATIONS]=0o700;p=D.ASSOCIATIONS+'/'+name;self.fs.files[p]=b'private';self.fs.modes[p]=0o600
        self.expect_failure('UNEXPECTED_PREEXISTING_ASSOCIATION_STATE',lambda:D.deploy(self.fs,self.m,COMMIT));self.assertEqual(self.fs.files[p],b'private');self.assertFalse(self.fs.mutations)
    def test_valid_lock_preserved_absent_created(self):
        for existing in (False,True):
            fs=SyntheticFS();fs.dirs[D.ASSOCIATIONS]=0o700
            if existing:fs.files[D.LOCK]=b'0';fs.modes[D.LOCK]=0o600
            D.deploy(fs,self.m,COMMIT);self.assertEqual(fs.files[D.LOCK],b'0' if existing else b'')
    def test_invalid_lock_mode_fails(self):
        self.fs.dirs[D.ASSOCIATIONS]=0o700;self.fs.files[D.LOCK]=b'';self.fs.modes[D.LOCK]=0o644
        self.expect_failure('UNSAFE_OBJECT',lambda:D.deploy(self.fs,self.m,COMMIT))
    def test_unauthorized_scheduler_stops(self):
        for raw in (b'5,35 * * * * /x/hioc-home-assistant-association.py',b'5,35 * * * * command # HIOC_PE4_HA_ASSOCIATION'):
            self.expect_failure('SCHEDULER_PRESENT',lambda:D.no_scheduler(raw))
        D.no_scheduler(b'# /x/hioc-home-assistant-association.py\n0 * * * * unrelated\n')
    def expected_runtime(self):
        return dict(implementation='cpython',python='3.11.2',architecture='aarch64',soabi='cpython-311-aarch64-linux-gnu',websockets='16.1.1',prefix=str(D.ENVIRONMENT),executable=str(D.INTERPRETER),isolated=True,bytecode_disabled=True,origins_valid=True,distributions_valid=True)
    def test_accepted_runtime_identity(self):D.runtime_identity(self.expected_runtime())
    def test_runtime_drift_stops(self):
        for key in self.expected_runtime():
            v=self.expected_runtime();v[key]='drift';self.expect_failure('RUNTIME_DRIFT',lambda:D.runtime_identity(v))
    def test_credential_validation_local_only(self):
        self.assertEqual(R['credential_validator']['git_blob'],'1bbe5826927b6b474db73fd2ace8a304b56dac66')
        source=HELPER.read_text();self.assertIn('"--runtime-operator"',source)
        self.assertNotIn('read_bytes()',source[source.index('def prerequisites'):source.index('EVIDENCE =')])
        self.assertFalse(R['credential']['backup']);self.assertFalse(R['credential']['authentication'])
    def test_no_adapter_network_scheduler_execution(self):
        tree=ast.parse(HELPER.read_text());imports={n.name for node in ast.walk(tree) if isinstance(node,(ast.Import,ast.ImportFrom)) for n in node.names}
        self.assertFalse(imports & {'socket','websockets','requests','run_cycle','main'})
        source=HELPER.read_text();self.assertNotIn('run_cycle(',source);self.assertNotIn('mosquitto',source)
        calls=[n for n in ast.walk(tree) if isinstance(n,ast.Call)]
        for n in calls:
            if isinstance(n.func,ast.Attribute):self.assertNotEqual(n.func.attr,'unlink')
        self.assertFalse(R['scheduler']['installation'])
    def test_rollback_preserves_after_execution(self):
        for word in ('PRIVATE_STATE','HISTORY','RECOVERY','CREDENTIAL','RUNTIME','INVENTORY','COMPATIBILITY'):
            self.assertIn(word,R['rollback']['after_execution'])
        self.assertFalse(R['rollback']['wildcard_delete']);self.assertFalse(R['transaction']['rollback_command'])
    def test_evidence_allowlist_private_data_absent(self):
        for code in D.CODES:
            e=D.evidence(COMMIT,code);self.assertEqual(set(e),set(R['evidence']['fields']))
            raw=json.dumps(e);self.assertNotIn(D.ENDPOINT,raw);self.assertNotIn('home_assistant.token',raw)
        self.assertEqual(D.evidence('secret-content')['SOURCE_COMMIT'],'INVALID')
    def test_config_metadata_preserved(self):
        D.deploy(self.fs,self.m,COMMIT);self.assertEqual(self.fs.modes[D.CONFIG],0o640)
    def test_prepared_resume_every_published_boundary(self):
        points=['PREPARED']+['FILE:'+i['path'] for i in self.m['deploy']]+['LOCK_CREATED','CONFIG_REPLACED','COMMITTED']
        for point in points:
            fs=SyntheticFS();before=fs.read(D.CONFIG)
            def fault(actual):
                if actual==point:raise RuntimeError('synthetic interruption')
            with self.assertRaises(RuntimeError):D.deploy(fs,self.m,COMMIT,fault)
            D.deploy(fs,self.m,COMMIT)
            self.assertEqual(fs.read(D.CONFIG),D.endpoint_config(before));self.assertIsNotNone(fs.read(D.TX+'/committed.json'))
            self.assertEqual(fs.read(D.TX+'/config-prior'),before)
    def test_idempotent_rerun_no_mutations(self):
        D.deploy(self.fs,self.m,COMMIT);self.fs.mutations=[];D.deploy(self.fs,self.m,COMMIT);self.assertFalse(self.fs.mutations)
    def test_preintent_interruption_stops_without_target_mutation(self):
        def fault(point):
            if point=='NAMESPACE_CREATED':raise RuntimeError('interrupted')
        with self.assertRaises(RuntimeError):D.deploy(self.fs,self.m,COMMIT,fault)
        self.expect_failure('TRANSACTION_CONFLICT',lambda:D.deploy(self.fs,self.m,COMMIT));self.assertFalse(any(i['path'] in self.fs.files for i in self.m['deploy']))
    def test_resume_source_conflict_stops(self):
        D.deploy(self.fs,self.m,COMMIT);self.expect_failure('TRANSACTION_CONFLICT',lambda:D.deploy(self.fs,self.m,'b'*40))
    def test_resume_config_drift_stops_preserving_bytes(self):
        D.deploy(self.fs,self.m,COMMIT);self.fs.files[D.CONFIG]=b'other'
        self.expect_failure('CONFIG_CONFLICT',lambda:D.deploy(self.fs,self.m,COMMIT));self.assertEqual(self.fs.files[D.CONFIG],b'other')
    def test_unknown_transaction_object_stops(self):
        D.deploy(self.fs,self.m,COMMIT);self.fs.files[D.TX+'/unknown']=b'keep';self.fs.modes[D.TX+'/unknown']=0o600
        self.expect_failure('TRANSACTION_CONFLICT',lambda:D.deploy(self.fs,self.m,COMMIT));self.assertEqual(self.fs.files[D.TX+'/unknown'],b'keep')
    def test_main_synthetic_no_adapter_invocation(self):
        with patch.object(D,'local_prerequisites',return_value=(1000,1000)),patch.object(D,'source_binding',return_value=self.m),patch.object(D,'prerequisites') as check,patch.object(D,'NativeFS',return_value=self.fs),patch('builtins.print'):
            self.assertEqual(D.main(['--expected-commit',COMMIT]),0);self.assertEqual(check.call_count,3)
    def test_import_no_io(self):
        with patch('os.open',side_effect=AssertionError('I/O')),patch('subprocess.run',side_effect=AssertionError('execution')):
            spec.loader.exec_module(D)
    def test_native_security_primitives_and_no_destructive_api(self):
        source=HELPER.read_text()
        for term in ('os.O_NOFOLLOW','os.O_DIRECTORY','os.O_EXCL','os.fsync','renameat2','os.replace','os.getxattr','st_nlink == 1','follow_symlinks=False'):
            self.assertIn(term,source)
        for term in ('shutil.rmtree','os.remove(','os.unlink(','crontab", "-r','crontab", "-i','pip install'):
            self.assertNotIn(term,source)
    def test_native_acl_absence_required(self):
        fs=D.NativeFS('/unused',1000,1000)
        info=SimpleNamespace(st_mode=stat.S_IFREG|0o600,st_uid=1000,st_gid=1000,st_nlink=1)
        with patch.object(D.os,'fstat',return_value=info),patch.object(D.os,'getxattr',create=True,return_value=b'ACL'):
            self.expect_failure('UNSAFE_OBJECT',lambda:fs.security(9,mode=0o600))
    def test_native_acl_unverifiable_fails(self):
        fs=D.NativeFS('/unused',1000,1000)
        info=SimpleNamespace(st_mode=stat.S_IFREG|0o600,st_uid=1000,st_gid=1000,st_nlink=1)
        with patch.object(D.os,'fstat',return_value=info),patch.object(D.os,'getxattr',create=True,side_effect=OSError(13,'denied')):
            self.expect_failure('UNSAFE_OBJECT',lambda:fs.security(9,mode=0o600))
    def test_native_owner_mode_link_type_failures(self):
        fs=D.NativeFS('/unused',1000,1000)
        for change in ({'st_uid':2000},{'st_gid':2000},{'st_mode':stat.S_IFREG|0o644},{'st_mode':stat.S_IFLNK|0o600},{'st_mode':stat.S_IFIFO|0o600},{'st_nlink':2}):
            info=dict(st_mode=stat.S_IFREG|0o600,st_uid=1000,st_gid=1000,st_nlink=1);info.update(change)
            with patch.object(D.os,'fstat',return_value=SimpleNamespace(**info)):
                self.expect_failure('UNSAFE_OBJECT',lambda:fs.security(9,mode=0o600))
    def test_preflight_main_failure_no_mutation(self):
        self.fs.files[self.m['dependencies'][0]['path']]=b'drift'
        with patch.object(D,'local_prerequisites',return_value=(1000,1000)),patch.object(D,'source_binding',return_value=self.m),patch.object(D,'prerequisites'),patch.object(D,'NativeFS',return_value=self.fs),patch('builtins.print'):
            self.assertEqual(D.main(['--expected-commit',COMMIT]),1)
        self.assertFalse(self.fs.mutations)
    def test_closed_schema(self):
        schema=json.loads((ROOT/D.RECORD.replace('.json','.schema.json')).read_bytes())
        def validate(value,node):
            if 'const' in node:
                self.assertEqual(type(value),type(node['const']));self.assertEqual(value,node['const']);return
            if node['type']=='object':
                self.assertIs(type(value),dict);self.assertFalse(node['additionalProperties'])
                self.assertEqual(set(value),set(node['required']));self.assertEqual(set(value),set(node['properties']))
                for key,child in node['properties'].items():validate(value[key],child)
            else:
                self.assertIs(type(value),list);self.assertFalse(node['items'])
                self.assertEqual(len(value),node['minItems']);self.assertEqual(len(value),node['maxItems'])
                self.assertEqual(len(value),len(node['prefixItems']))
                for x,child in zip(value,node['prefixItems']):validate(x,child)
        validate(R,schema)
        changed=copy.deepcopy(R);changed['unexpected']=True
        with self.assertRaises(AssertionError):validate(changed,schema)
        self.assertEqual((ROOT/D.RECORD).read_bytes(),D.canonical(R))
    def test_lifecycle_and_next(self):
        self.assertEqual(R['lifecycle']['deployment_preparation'],'PASS_CLOSED');self.assertEqual(R['lifecycle']['deployment'],'NOT_STARTED')
        self.assertEqual(R['next_checkpoint'],'PE-4 Home Assistant Association Adapter Deployment Execution')
        self.assertTrue(all(v is False for v in R['negative_evidence'].values()))

class DeploymentEvidenceCorrectionTests(unittest.TestCase):
    setUp = DeploymentPreparationTests.setUp
    expect_failure = DeploymentPreparationTests.expect_failure

    def run_main(self, *, source_error=None, prerequisite_errors=None, deploy_fault=None, post_config_error=False):
        output = []
        original_deploy = D.deploy
        original_config = D.effective_configuration
        calls = [0]
        def execute(fs, m, commit):
            return original_deploy(fs, m, commit, deploy_fault or (lambda point: None))
        def config(toolkit, candidate):
            calls[0] += 1
            if post_config_error and calls[0] == 2: raise D.Failure('CONFIG_CONFLICT')
            return original_config(toolkit, candidate)
        with patch.object(D,'local_prerequisites',return_value=(1000,1000)),patch.object(D,'source_binding',side_effect=source_error,return_value=self.m),patch.object(D,'prerequisites',side_effect=prerequisite_errors),patch.object(D,'NativeFS',return_value=self.fs),patch.object(D,'deploy',side_effect=execute),patch.object(D,'effective_configuration',side_effect=config),patch('builtins.print',side_effect=output.append):
            rc = D.main(['--expected-commit',COMMIT])
        return rc, dict(line.split('=',1) for line in output)

    def check_report(self, result, state, deployment, overall='FAIL'):
        rc, report = result
        self.assertEqual(rc,0 if overall=='PASS' else 1)
        self.assertEqual(report['RESULT'],overall)
        self.assertEqual(report['DEPLOYMENT_TRANSACTION'],state)
        self.assertEqual(report['PRODUCTION_DEPLOYMENT'],deployment)
        self.assertEqual(set(report),set(R['evidence']['fields']))
        for key in ('ADAPTER_EXECUTED','HA_NETWORK_ATTEMPTED','HA_AUTHENTICATION_ATTEMPTED'):
            self.assertEqual(report[key],'FALSE')
        self.assertEqual(report['SCHEDULER_DEPLOYMENT'],'NOT_STARTED')
        self.assertEqual(report['ROLLBACK'],'NOT_PERFORMED')
        return report

    def test_required_existing_dependency_policy_distinct(self):
        for item in self.m['dependencies']:
            self.assertEqual(item['classification'],'B_EXISTING_EXACT_DEPENDENCY')
            self.assertEqual(item['policy'],'REQUIRED_EXISTING_EXACT_PRESERVE_ABSENT_OR_DIFFERENT_FAIL_CLOSED')
            self.assertNotEqual(item['policy'],D.ADDITIVE_POLICY)
        self.assertEqual(len(self.m['deploy']),8)
        self.assertFalse(D.DEPENDENCIES.intersection(i['path'] for i in self.m['deploy']))
        for item in self.m['deploy']:self.assertEqual(item['policy'],D.ADDITIVE_POLICY)

    def test_no_dependency_path_can_enter_deploy(self):
        for item in self.m['dependencies']:
            changed=copy.deepcopy(self.m);changed['deploy'][0]=dict(item,bytes=source_bytes(item['path']))
            self.expect_failure('SOURCE_BINDING',lambda:D.deploy(self.fs,changed,COMMIT))
        self.assertFalse(self.fs.mutations)

    def test_exact_dependencies_preserved_without_mutation(self):
        before={i['path']:(self.fs.files[i['path']],self.fs.modes[i['path']]) for i in self.m['dependencies']}
        self.check_report(self.run_main(),'COMMITTED','PASS','PASS')
        for p,pair in before.items():
            self.assertEqual((self.fs.files[p],self.fs.modes[p]),pair)
            self.assertNotIn('add:'+p,self.fs.mutations)

    def test_source_binding_failure_not_started(self):
        self.check_report(self.run_main(source_error=D.Failure('SOURCE_BINDING')),'NOT_STARTED','NOT_STARTED')
        self.assertFalse(self.fs.mutations)

    def test_missing_dependency_not_started(self):
        del self.fs.files[self.m['dependencies'][0]['path']]
        report=self.check_report(self.run_main(),'NOT_STARTED','NOT_STARTED')
        self.assertEqual(report['ERROR_CODE'],'DEPENDENCY_DRIFT');self.assertFalse(self.fs.mutations)

    def test_different_dependency_not_started(self):
        self.fs.files[self.m['dependencies'][0]['path']]=b'drift'
        report=self.check_report(self.run_main(),'NOT_STARTED','NOT_STARTED')
        self.assertEqual(report['ERROR_CODE'],'DEPENDENCY_DRIFT');self.assertFalse(self.fs.mutations)

    def test_endpoint_conflict_not_started(self):
        self.fs.files[D.CONFIG]=b'HIOC_HA_ENDPOINT="wrong"\n'
        report=self.check_report(self.run_main(),'NOT_STARTED','NOT_STARTED')
        self.assertEqual(report['ERROR_CODE'],'CONFIG_CONFLICT');self.assertFalse(self.fs.mutations)

    def test_private_state_not_started(self):
        self.fs.dirs[D.ASSOCIATIONS]=0o700;self.fs.files[D.ASSOCIATIONS+'/home_assistant.json']=b'private'
        report=self.check_report(self.run_main(),'NOT_STARTED','NOT_STARTED')
        self.assertEqual(report['ERROR_CODE'],'UNEXPECTED_PREEXISTING_ASSOCIATION_STATE');self.assertFalse(self.fs.mutations)

    def test_scheduler_runtime_credential_failures_not_started(self):
        for code in ('SCHEDULER_PRESENT','RUNTIME_DRIFT','CREDENTIAL_INVALID'):
            self.fs=SyntheticFS()
            report=self.check_report(self.run_main(prerequisite_errors=D.Failure(code)),'NOT_STARTED','NOT_STARTED')
            self.assertEqual(report['ERROR_CODE'],code);self.assertFalse(self.fs.mutations)

    def test_preintent_namespace_interruption_and_rerun(self):
        def fault(point):
            if point=='NAMESPACE_CREATED':raise RuntimeError('private exception text')
        self.check_report(self.run_main(deploy_fault=fault),'NOT_STARTED','NOT_STARTED')
        self.assertEqual(D.transaction_state(self.fs,self.m,COMMIT),'NOT_STARTED')
        self.assertFalse(any(i['path'] in self.fs.files for i in self.m['deploy']))
        before=copy.deepcopy(self.fs.files)
        report=self.check_report(self.run_main(),'NOT_STARTED','NOT_STARTED')
        self.assertEqual(report['ERROR_CODE'],'TRANSACTION_CONFLICT');self.assertEqual(self.fs.files,before)

    def test_preintent_config_staging_remains_not_started(self):
        for name in ('config-prior','config-candidate'):
            self.fs=SyntheticFS();self.fs.dirs[D.TX]=0o700;self.fs.files[D.TX+'/'+name]=b'stage';self.fs.modes[D.TX+'/'+name]=0o600
            report=self.check_report(self.run_main(),'NOT_STARTED','NOT_STARTED')
            self.assertEqual(report['ERROR_CODE'],'TRANSACTION_CONFLICT')

    def test_prepared_and_every_additive_lock_config_boundary(self):
        for point in ['PREPARED']+['FILE:'+i['path'] for i in self.m['deploy']]+['LOCK_CREATED','CONFIG_REPLACED']:
            with self.subTest(point=point):
                self.fs=SyntheticFS()
                def fault(actual):
                    if actual==point:raise RuntimeError('private exception text')
                report=self.check_report(self.run_main(deploy_fault=fault),'PREPARED','INCOMPLETE')
                self.assertEqual(D.transaction_state(self.fs,self.m,COMMIT),'PREPARED')
                self.assertNotIn('private exception text',str(report))

    def test_precommit_validation_failure_is_prepared(self):
        def fault(point):
            if point=='CONFIG_REPLACED':self.fs.files[self.m['dependencies'][0]['path']]=b'drift'
        report=self.check_report(self.run_main(deploy_fault=fault),'PREPARED','INCOMPLETE')
        self.assertEqual(report['ERROR_CODE'],'DEPENDENCY_DRIFT')

    def test_committed_marker_then_interruption_is_committed(self):
        def fault(point):
            if point=='COMMITTED':raise RuntimeError('interrupted after fsync')
        self.check_report(self.run_main(deploy_fault=fault),'COMMITTED','PASS')

    def test_postcommit_config_check_failure_is_committed(self):
        report=self.check_report(self.run_main(post_config_error=True),'COMMITTED','PASS')
        self.assertEqual(report['ERROR_CODE'],'CONFIG_CONFLICT')

    def test_postcommit_runtime_credential_scheduler_failure_is_committed(self):
        for code in ('RUNTIME_DRIFT','CREDENTIAL_INVALID','SCHEDULER_PRESENT'):
            self.fs=SyntheticFS()
            report=self.check_report(self.run_main(prerequisite_errors=[None,None,D.Failure(code)]),'COMMITTED','PASS')
            self.assertEqual(report['ERROR_CODE'],code)

    def test_committed_rerun_preflight_drift_not_downgraded(self):
        self.check_report(self.run_main(),'COMMITTED','PASS','PASS')
        self.fs.files[self.m['dependencies'][0]['path']]=b'drift'
        self.check_report(self.run_main(),'COMMITTED','PASS')

    def test_success_and_idempotent_committed_rerun(self):
        self.check_report(self.run_main(),'COMMITTED','PASS','PASS')
        self.fs.mutations=[];before=copy.deepcopy(self.fs.files)
        self.check_report(self.run_main(),'COMMITTED','PASS','PASS')
        self.assertFalse(self.fs.mutations);self.assertEqual(self.fs.files,before)

    def test_classifier_is_read_only_and_marker_bound(self):
        D.deploy(self.fs,self.m,COMMIT);self.fs.mutations=[]
        self.assertEqual(D.transaction_state(self.fs,self.m,COMMIT),'COMMITTED');self.assertFalse(self.fs.mutations)
        self.fs.files[D.TX+'/committed.json']=D.canonical({'status':'COMMITTED','source_commit':'b'*40,'intent_sha256':'0'*64})
        self.assertEqual(D.transaction_state(self.fs,self.m,COMMIT),'PREPARED')
        self.fs.files[D.TX+'/intent.json']=b'{}\n'
        self.assertEqual(D.transaction_state(self.fs,self.m,COMMIT),'NOT_STARTED')

    def test_verified_commit_not_downgraded_by_later_journal_verification(self):
        original = D.transaction_state
        count = [0]
        def observe(fs,m,commit):
            count[0] += 1
            if count[0] == 3: return 'NOT_STARTED'
            return original(fs,m,commit)
        with patch.object(D,'transaction_state',side_effect=observe):
            report=self.check_report(self.run_main(),'COMMITTED','PASS')
        self.assertEqual(report['ERROR_CODE'],'TRANSACTION_CONFLICT')

    def test_correction_record_schema_and_historical_binding(self):
        path=ROOT/'governance/pe4/pe4-ha-association-adapter-deployment-preparation-correction.json'
        correction=json.loads(path.read_bytes())
        self.assertEqual(path.read_bytes(),D.canonical(correction))
        self.assertEqual(correction['historical_preparation_commit'],'0040bdc79e66c10db4f180f952d04f97b1070065')
        self.assertEqual(correction['production_deployment_mapping'],D.TRANSACTIONS)
        self.assertEqual(correction['evidence_fields'],R['evidence']['fields'])
        self.assertEqual(correction['required_existing_dependency_policy'],D.REQUIRED_POLICY)
        for key in ('corrected_helper','corrected_preparation_record','corrected_preparation_schema'):
            item=correction[key];raw=subprocess.check_output(['git','show','2ef66a2d575c923c6939a4cd4d5bb2c8aab2f816:'+item['path']],cwd=ROOT)
            self.assertEqual(D.sha(raw),item['sha256'])
        for key in ('historical_preparation_record','historical_preparation_schema'):
            item=correction[key];raw=subprocess.check_output(['git','show','0040bdc79e66c10db4f180f952d04f97b1070065:'+item['path']],cwd=ROOT)
            self.assertEqual(D.sha(raw),item['sha256'])
        schema=json.loads(path.with_suffix('.schema.json').read_bytes())
        def validate(value,node):
            if 'const' in node:
                self.assertIs(type(value),type(node['const']));self.assertEqual(value,node['const']);return
            if node['type']=='object':
                self.assertIs(type(value),dict);self.assertFalse(node['additionalProperties'])
                self.assertEqual(set(value),set(node['required']));self.assertEqual(set(value),set(node['properties']))
                for key,child in node['properties'].items():validate(value[key],child)
            else:
                self.assertIs(type(value),list);self.assertFalse(node['items'])
                self.assertEqual(len(value),node['minItems']);self.assertEqual(len(value),node['maxItems'])
                for item,child in zip(value,node['prefixItems']):validate(item,child)
        validate(correction,schema)
        changed=copy.deepcopy(correction);changed['transaction_states'].append('AMBIGUOUS')
        with self.assertRaises(AssertionError):validate(changed,schema)

    def test_evidence_only_three_durable_states(self):
        self.assertEqual(D.TRANSACTIONS,{'NOT_STARTED':'NOT_STARTED','PREPARED':'INCOMPLETE','COMMITTED':'PASS'})
        for state,deployment in D.TRANSACTIONS.items():
            for code in ('COMPLETE','IO_FAILED'):
                e=D.evidence(COMMIT,code,state);self.assertEqual(e['PRODUCTION_DEPLOYMENT'],deployment)
        self.expect_failure('INVALID',lambda:D.evidence(COMMIT,'IO_FAILED','ambiguous'))
        self.assertNotIn('PREPARED_OR_INTERRUPTED',HELPER.read_text(encoding='utf-8'))



class RuntimeCustomizationDeploymentTests(unittest.TestCase):
    def test_reviewed_components_accepted(self):
        from tests.pe4_runtime_customization_fixtures import observation
        site=D.ENVIRONMENT/'lib/python3.11/site-packages'
        with patch.object(D,'SOURCE',ROOT):D.validate_customization(observation(site),site)
    def test_every_mismatch_rejected_before_intent(self):
        from tests.pe4_runtime_customization_fixtures import failures
        site=D.ENVIRONMENT/'lib/python3.11/site-packages'
        fs=SyntheticFS();m=manifest()
        for name,bad in failures(site):
            with self.subTest(name=name),patch.object(D,'SOURCE',ROOT):
                with self.assertRaises(D.Failure) as caught:D.validate_customization(bad,site)
                self.assertEqual(caught.exception.code,'RUNTIME_DRIFT')
                with patch.object(D,'local_prerequisites',return_value=(1000,1000)),patch.object(D,'source_binding',return_value=m),patch.object(D,'NativeFS',return_value=fs),patch.object(D,'prerequisites',side_effect=caught.exception),patch('builtins.print') as output:
                    self.assertEqual(D.main(['--expected-commit',COMMIT]),1)
                lines='\n'.join(str(call.args[0]) for call in output.call_args_list)
                self.assertIn('DEPLOYMENT_TRANSACTION=NOT_STARTED',lines);self.assertIn('PRODUCTION_DEPLOYMENT=NOT_STARTED',lines);self.assertEqual(fs.mutations,[])


class ResolvedPrefixProbeTests(unittest.TestCase):
    """Execute the generated child body with injected Linux paths/modules, never a runtime."""
    ACTIVE='/home/jazofv1/hioc/runtime/pe4/active'
    ACCEPTED='/home/jazofv1/hioc/runtime/pe4/environments/cpython311-websockets16.1.1-lock-v1'
    def model(self,resolved=None):
        active=self.ACTIVE;resolved=resolved or self.ACCEPTED
        class LinuxPath(PurePosixPath):
            def resolve(inner):
                value=str(inner)
                return LinuxPath(resolved+value[len(active):]) if value==active or value.startswith(active+'/') else inner
            def absolute(inner):return inner
            def is_symlink(inner):return str(inner)==active
            def exists(inner):return True
        return LinuxPath
    def identity(self):
        return dict(implementation='cpython',python='3.11.2',architecture='aarch64',soabi='cpython-311-aarch64-linux-gnu',websockets='16.1.1',prefix=self.ACCEPTED,executable=self.ACTIVE+'/bin/python',isolated=True,bytecode_disabled=True,origins_valid=True,distributions_valid=True)
    @contextlib.contextmanager
    def host(self,active_target=None):
        from tests.pe4_runtime_customization_fixtures import observation
        path=self.model(active_target);site=path(self.ACCEPTED)/'lib/python3.11/site-packages'
        with patch.object(D,'SOURCE',ROOT):namespace=D.runtime_policy_namespace()
        namespace['runtime_customization_observation']=lambda _:observation(site)
        with patch.object(D,'SOURCE',ROOT),patch.object(D,'HOME',path('/home/jazofv1/hioc')),patch.object(D,'ENVIRONMENT',path(self.ACCEPTED)),patch.object(D,'INTERPRETER',path(self.ACTIVE+'/bin/python')),patch.object(D,'runtime_policy_namespace',return_value=namespace),patch.object(D.subprocess,'run',return_value=SimpleNamespace(returncode=0,stdout=b'',stderr=b'')):
            yield path
    def generated_probe(self):
        captured=[]
        def command(args,code):
            if '-c' in args:captured.append(args[-1]);return json.dumps(self.identity()).encode()
            return b'RESULT=PASS\nCREDENTIAL_READABLE_BY_RUNTIME_OPERATOR=TRUE\nNETWORK_CONNECTION_ATTEMPTED=FALSE\nHA_AUTHENTICATION_ATTEMPTED=FALSE\n'
        with self.host(),patch.object(D,'command',side_effect=command):D.prerequisites()
        self.assertEqual(len(captured),1);return captured[0]
    def execute_child(self,probe,*,resolved=None,change=None):
        from tests.pe4_runtime_customization_fixtures import observation
        with patch.object(D,'SOURCE',ROOT):validator=D.runtime_policy_namespace()['validate_runtime_customization']
        path=self.model(resolved);site=path(resolved or self.ACCEPTED)/'lib/python3.11/site-packages';seen=[];printed=[]
        def observe(actual):
            seen.append(actual)
            if str(actual).startswith(self.ACTIVE+'/'):raise NotADirectoryError('synthetic active symlink')
            self.assertEqual(actual,site)
            value=observation(site)
            if change=='pth':value['pth_names'].append('unreviewed.pth')
            if change=='sitecustomize':value['site_module']='/other/sitecustomize.py'
            if change=='usercustomize':value['user_loaded']=True
            return value
        distributions=[SimpleNamespace(metadata={'Name':name},version=version) for name,version in [('websockets','wrong' if change=='websockets' else '16.1.1'),('pip','23.0.1'),('setuptools','66.1.1')]]
        if change=='distribution':distributions.append(SimpleNamespace(metadata={'Name':'extra'},version='1'))
        fake_sys=SimpleNamespace(prefix=self.ACTIVE,executable=self.ACTIVE+'/bin/python',implementation=SimpleNamespace(name='cpython'),version_info=(3,11,2),flags=SimpleNamespace(isolated=1,dont_write_bytecode=1),path=['/usr/lib/python311.zip','/usr/lib/python3.11','/usr/lib/python3.11/lib-dynload',str(site)]+(['/usr/lib/python3/dist-packages'] if change=='path' else []),modules={})
        namespace=dict(Path=path,sys=fake_sys,platform=SimpleNamespace(machine=lambda:'aarch64'),sysconfig=SimpleNamespace(get_config_var=lambda _:'cpython-311-aarch64-linux-gnu'),json=json,importlib=SimpleNamespace(util=SimpleNamespace(find_spec=lambda _:SimpleNamespace(origin=str(site/'websockets/__init__.py'))),metadata=SimpleNamespace(distributions=lambda **_:distributions)),validate_runtime_customization=validator,runtime_customization_observation=observe,print=lambda value:printed.append(value))
        # Keep the generated executable probe logic; replace only imports and the
        # separately source-verified native observation definitions with injected APIs.
        tree=ast.parse(probe);tree.body=[n for n in tree.body if not isinstance(n,(ast.Import,ast.ImportFrom,ast.FunctionDef)) and not (isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CUSTOMIZATION_POLICY' for t in n.targets))]
        module=SimpleNamespace(__version__='wrong' if change=='websockets' else '16.1.1',__file__=str(site/'websockets/__init__.py'))
        with patch.dict(sys.modules,{'websockets':module}):exec(compile(tree,'synthetic generated child probe','exec'),namespace)
        return json.loads(printed[0]),seen
    def test_raw_active_prefix_uses_resolved_site_for_observation(self):
        probe=self.generated_probe();value,seen=self.execute_child(probe)
        self.assertEqual([str(p) for p in seen],[self.ACCEPTED+'/lib/python3.11/site-packages'])
        with self.host():D.runtime_identity(value)
    def test_original_unresolved_construction_reproduces_safe_failure(self):
        probe=self.generated_probe().replace("site=resolved_prefix/", "site=raw_prefix/")
        with self.assertRaises(NotADirectoryError):self.execute_child(probe)
    def test_different_resolved_prefix_remains_runtime_drift(self):
        value,_=self.execute_child(self.generated_probe(),resolved='/unreviewed/environment')
        with self.host(),self.assertRaises(D.Failure) as caught:D.runtime_identity(value)
        self.assertEqual(caught.exception.code,'RUNTIME_DRIFT')
    def test_active_target_drift_precedes_child_and_credential(self):
        with self.host('/unreviewed/environment'),patch.object(D,'command') as command,self.assertRaises(D.Failure) as caught:D.prerequisites()
        self.assertEqual(caught.exception.code,'RUNTIME_DRIFT');command.assert_not_called()
    def test_generated_child_retains_exact_customization_failures(self):
        for change in ('pth','sitecustomize','usercustomize'):
            with self.subTest(change=change),self.assertRaises(ValueError):self.execute_child(self.generated_probe(),change=change)
    def test_generated_child_retains_package_and_path_failures(self):
        probe=self.generated_probe()
        for change in ('distribution','websockets','path'):
            with self.subTest(change=change):
                value,_=self.execute_child(probe,change=change)
                with self.host(),self.assertRaises(D.Failure) as caught:D.runtime_identity(value)
                self.assertEqual(caught.exception.code,'RUNTIME_DRIFT')
    def test_actual_runtime_prerequisite_failures_never_reach_intent(self):
        probe=self.generated_probe()
        for change in ('pth','sitecustomize','usercustomize','distribution','websockets','path','prefix','active'):
            fs=SyntheticFS();m=manifest();called=[]
            def command(args,code):
                called.append(args)
                self.assertIn('-c',args,'Credential command must not be reached')
                try:value,_=self.execute_child(args[-1],resolved='/unreviewed/environment' if change=='prefix' else None,change=change)
                except (ValueError,NotADirectoryError):raise D.Failure('RUNTIME_DRIFT') from None
                return json.dumps(value).encode()
            with self.subTest(change=change),self.host('/unreviewed/environment' if change=='active' else None),patch.object(D,'command',side_effect=command),patch.object(D,'local_prerequisites',return_value=(1000,1000)),patch.object(D,'source_binding',return_value=m),patch.object(D,'NativeFS',return_value=fs),patch('builtins.print') as output:
                self.assertEqual(D.main(['--expected-commit',COMMIT]),1)
            lines='\n'.join(str(call.args[0]) for call in output.call_args_list)
            for text in ('ERROR_CODE=RUNTIME_DRIFT','DEPLOYMENT_TRANSACTION=NOT_STARTED','PRODUCTION_DEPLOYMENT=NOT_STARTED','ADAPTER_EXECUTED=FALSE','HA_NETWORK_ATTEMPTED=FALSE','HA_AUTHENTICATION_ATTEMPTED=FALSE'):self.assertIn(text,lines)
            self.assertEqual(fs.mutations,[])
    def test_policy_and_adapter_source_bytes_remain_exact(self):
        raw=(ROOT/'pi4/lib/hioc/home_assistant_association.py').read_bytes()
        self.assertEqual(D.sha(raw),'9a9be5812f3481146de7546875320eb6adec65ca5a2b3230ff5fec378892c7c1');self.assertEqual(D.RUNTIME_POLICY_MODULE_SHA,D.sha(raw))
        self.assertEqual(raw,subprocess.check_output(['git','show','e4d5a19afecccb1584708e3da57ba3c0c4258523:pi4/lib/hioc/home_assistant_association.py'],cwd=ROOT))

    def test_probe_correction_closed_governance_and_source_binding(self):
        base=ROOT/'governance/pe4/pe4-ha-association-deployment-runtime-probe-correction'
        record=json.loads(base.with_suffix('.json').read_bytes());schema=json.loads(base.with_suffix('.schema.json').read_bytes())
        def validate(value,node):
            if 'const' in node:self.assertIs(type(value),type(node['const']));self.assertEqual(value,node['const']);return
            if node['type']=='object':
                self.assertFalse(node['additionalProperties']);self.assertEqual(set(value),set(node['required']));self.assertEqual(set(value),set(node['properties']))
                for key,child in node['properties'].items():validate(value[key],child)
            else:
                self.assertFalse(node['items']);self.assertEqual(len(value),node['minItems']);self.assertEqual(len(value),node['maxItems'])
                for item,child in zip(value,node['prefixItems']):validate(item,child)
        validate(record,schema)
        bad=copy.deepcopy(record);bad['operator_evidence']['provenance']='CODEX_OBSERVED'
        with self.assertRaises(AssertionError):validate(bad,schema)
        bad=copy.deepcopy(record);bad['runtime_trust_policy_changed']=True
        with self.assertRaises(AssertionError):validate(bad,schema)
        bad=copy.deepcopy(record);bad['extra']=True
        with self.assertRaises(AssertionError):validate(bad,schema)
        for suffix in ('.json','.schema.json'):
            raw=base.with_suffix(suffix).read_bytes();self.assertEqual(raw,D.canonical(json.loads(raw)))
        for item in record['sources'].values():
            raw=(ROOT/item['path']).read_bytes();self.assertEqual(D.sha(raw),item['sha256']);self.assertEqual(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),item['git_blob'])
        self.assertEqual(record['starting_commit'],D.BASELINE);self.assertEqual(D.BASELINE,'e4d5a19afecccb1584708e3da57ba3c0c4258523')
        self.assertEqual(R['source_binding']['parent'],D.BASELINE);self.assertEqual(R['source_binding']['subject'],'PE-4: fix deployment runtime prefix validation')
        self.assertEqual(R['helper'],record['sources']['deployment_helper']);self.assertFalse(record['runtime_contract_consumption']);self.assertFalse(record['production_installation'])

if __name__ == '__main__':unittest.main()
