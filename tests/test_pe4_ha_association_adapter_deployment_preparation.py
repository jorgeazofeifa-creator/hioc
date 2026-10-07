"""Repository-only preparation contracts and interruption tests; no Linux target I/O."""
import ast
import contextlib
from functools import lru_cache
import copy
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
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
    if path=='tools/hioc-pe4-ha-association-deploy.py':return (ROOT/path).read_bytes()
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
        self.assertEqual(R["deployment_files"][0]["git_blob"],"0c049b7ee19b6b20c3fef53717455ba341d4a149")
        self.assertEqual(R["deployment_files"][0]["sha256"],"cf04d05f6215b9654539df69797de49a831044795ba8f7f5b3432d9d35a086b9")
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

if __name__ == '__main__':unittest.main()
