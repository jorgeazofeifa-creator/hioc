"""Current PE-7 candidate binding, separate from immutable historical validators."""
import hashlib,json,subprocess,unittest
from functools import lru_cache
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASELINE='ad9ddc5ced903f8c922a12c08f843fba6fce907b'
RECORD='governance/pe7/pe7-implementation-candidate.json'
CONTRACT='docs/PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION_CONTRACT.md'
CONTRACT_SHA='db8e25ba10e7038ee56a66aa12481d11c18b731a22ee4dfdc4de761031a9e14d'
AUTHORIZED=sorted([
'pi4/lib/hioc/assets.py','pi4/lib/hioc/asset_policy.py','pi4/lib/hioc/availability_contract.py',
'pi4/lib/hioc/availability.py','pi4/lib/hioc/availability_protocol.py','pi4/lib/hioc/availability_incidents.py',
'pi4/lib/hioc/availability_observation.py','pi4/lib/hioc/availability_server.py','pi4/lib/hioc/classification.py',
'pi4/bin/hioc-assets.py','pi4/bin/hioc-incident-engine-v2.py','pi4/bin/hioc-availability-adapter.py',
'homeassistant/custom_components/hioc_operator/__init__.py','homeassistant/custom_components/hioc_operator/manifest.json',
'homeassistant/custom_components/hioc_operator/services.yaml','homeassistant/www/hioc-asset-editor.js',
'homeassistant/dashboards/hioc_dashboard_v2.yaml','homeassistant/packages/hioc_incident_center.yaml',
'tests/test_pe7_contract.py','tests/test_pe7_assets.py','tests/test_pe7_security.py','tests/test_pe7_evaluation.py',
'tests/test_pe7_ha.py','tests/test_pe7_dispatch.py','tests/test_pe7_dashboard.py','tests/test_pe7_binding.py',
'tests/test_pe6_classification_implementation.py','docs/HIOC_MASTER_PLAN.md',
'docs/PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md',RECORD,'pi4/lib/hioc/mqtt.py',CONTRACT,
 'tests/test_pe4_ha_association_independent_production_acceptance_preparation.py',
 'tests/test_pe4_ha_association_public_projection_deployment_closure.py',
 'tests/test_pe5_local_service_association.py','tests/test_pe5_service_association_caller.py',
 'tests/test_pe6_classification_contract_design.py','tests/test_pe4_ha_association_public_projection_test_binding_correction.py',
 'tests/test_pe4_ha_association_public_projection_preparation.py',
 'tests/test_pe4_ha_runtime_credential_provisioning_closure.py'])


SCOPE_EXTENSIONS = [
 {'path':'pi4/lib/hioc/mqtt.py','reason':'Accepted section 10 requires bounded single-attempt dispatch; legacy MQTT bodies remain unchanged.'},
 {'path':CONTRACT,'reason':'Explicitly authorized section 6.1 T03/T04 read-interface correction.'},
 *[{'path':p,'reason':'Contract-required immutable historical replay/current successor separation; preserve original historical assertions, validators and records.'} for p in sorted([
 'tests/test_pe4_ha_association_independent_production_acceptance_preparation.py',
 'tests/test_pe4_ha_association_public_projection_deployment_closure.py',
 'tests/test_pe5_local_service_association.py','tests/test_pe5_service_association_caller.py',
 'tests/test_pe6_classification_contract_design.py','tests/test_pe4_ha_association_public_projection_test_binding_correction.py',
 'tests/test_pe4_ha_association_public_projection_preparation.py',
 'tests/test_pe4_ha_runtime_credential_provisioning_closure.py'])]]

def require(value,message):
    if not value: raise ValueError(message)
def sha(raw): return hashlib.sha256(raw).hexdigest()
def blob(raw):return hashlib.sha1(('blob '+str(len(raw))+'\0').encode()+raw).hexdigest()
def raw(path):return (ROOT/path).read_bytes().replace(b'\r\n',b'\n')
def git(*args):return subprocess.check_output(['git','--no-optional-locks',*args],cwd=ROOT,stderr=subprocess.PIPE)
def canonical(value):return (json.dumps(value,sort_keys=True,indent=2,ensure_ascii=True)+'\n').encode()

@lru_cache(maxsize=None)
def immutable_bytes(identity):
    return git('--no-replace-objects','cat-file','blob',identity)

def current_candidate(*,read=raw,git_runner=git):
    record=json.loads(read(RECORD))
    require(set(record)=={'schema_version','checkpoint','baseline','status','authorized_paths','artifacts','protected',
        'production_authorized','independent_acceptance','historical_fingerprint_limitation','scope_extensions'},'closed candidate record')
    require(read(RECORD)==canonical(record),'canonical candidate record')
    require(record['schema_version']=='1.0' and record['checkpoint']=='PE-7.1' and record['baseline']==BASELINE,
        'candidate baseline')
    require(record['status']=='IMPLEMENTATION_CANDIDATE' and record['independent_acceptance']=='NOT_PERFORMED' and
        record['production_authorized'] is False,'candidate authority')
    require(record['authorized_paths']==AUTHORIZED,'authorized implementation paths')
    require(record['scope_extensions']==SCOPE_EXTENSIONS,'exact contract-required scope extensions')
    require(git_runner('branch','--show-current').strip()==b'main','current branch')
    require(git_runner('rev-parse','origin/main').strip()==BASELINE.encode(),'current publication provenance')
    require(git_runner('rev-parse','HEAD').strip()==BASELINE.encode(),'current checkpoint parent')
    changes=set(git_runner('diff','--name-only',BASELINE).decode().splitlines())
    untracked=set(git_runner('ls-files','--others','--exclude-standard').decode().splitlines())
    require(changes|untracked==set(AUTHORIZED),'unexpected implementation path')
    require(not git_runner('diff','--cached','--name-only').strip(),'candidate staging must remain empty')
    tree={}
    for row in git_runner('ls-tree','-r',BASELINE).decode().splitlines():
        meta,path=row.split('\t',1); mode,kind,identity=meta.split();tree[path]=(mode,identity)
    require([x['path'] for x in record['artifacts']]==sorted(set(AUTHORIZED)-{RECORD}),'complete current artifact map')
    for item in record['artifacts']:
        require(set(item)=={'path','mode','sha256','file_sha256','git_blob'},'closed current artifact')
        value=read(item['path'])
        require((sha(value),blob(value))==(item['sha256'],item['git_blob']),'current implementation artifact identity')
        require(item['mode']==tree.get(item['path'],('100644',None))[0],'current artifact mode')
        # Raw file bytes are checked in the repository-native entry. Injected
        # historical readers retain their canonical-byte interface.
        if read is raw: require(sha((ROOT/item['path']).read_bytes())==item['file_sha256'],'current raw file identity')
    require([x['path'] for x in record['protected']]==sorted(set(tree)-set(AUTHORIZED)),'complete protected baseline map')
    for item in record['protected']:
        require(set(item)=={'path','mode','sha256','file_sha256','git_blob'},'closed protected artifact')
        value=read(item['path'])
        require((item['mode'],item['git_blob'])==tree[item['path']] and
            (blob(value) == item['git_blob'] or value == immutable_bytes(item['git_blob']).replace(b'\r\n',b'\n')) and
            sha(value)==item['sha256'],'protected baseline artifact')
        if read is raw: require(sha((ROOT/item['path']).read_bytes())==item['file_sha256'],'protected raw baseline artifact')
    require(sha(read(CONTRACT))==CONTRACT_SHA,'corrected contract identity')
    return record

def assert_candidate_sequence(text,*,read=raw,git_runner=git):
    current_candidate(read=read,git_runner=git_runner)
    full=read('docs/HIOC_MASTER_PLAN.md').decode()
    status=full.split('# Implementation Status',1)[1].split('# Historical Operator Preparation Chronology',1)[0]
    require(text in (full,status),'current lifecycle text substitution')
    require('PE71_COMPLETE=FALSE' in status and 'PE71_INDEPENDENT_ACCEPTANCE=NOT_PERFORMED' in status and
        'PE71_IMPLEMENTATION_AUTHORIZED=TRUE' in status,'current candidate lifecycle')
    return True

class BindingTests(unittest.TestCase):
    def test_current_candidate_and_protected_baseline(self):
        record=current_candidate(); self.assertEqual(len(record['authorized_paths']),40)
        self.assertEqual(len(record['protected']),449)
    def test_modified_current_artifact_rejected(self):
        def changed(path):return raw(path)+b' ' if path=='pi4/lib/hioc/availability.py' else raw(path)
        with self.assertRaisesRegex(ValueError,'current implementation artifact'):current_candidate(read=changed)
    def test_historical_artifact_cannot_be_rebound(self):
        def changed(path):return raw(path)+b' ' if path=='governance/pe6/pe6-classification-contract-design.json' else raw(path)
        with self.assertRaisesRegex(ValueError,'protected baseline artifact'):current_candidate(read=changed)
    def test_foreign_paths_and_false_publication_rejected(self):
        for command,answer in [(('ls-files','--others','--exclude-standard'),b'foreign.txt\n'),
            (('branch','--show-current'),b'other\n'),(('rev-parse','origin/main'),b'0'*40+b'\n')]:
            def changed(*a):return answer if a==command else git(*a)
            with self.subTest(command=command),self.assertRaises(ValueError):current_candidate(git_runner=changed)
    def test_lifecycle_substitution_cannot_claim_acceptance(self):
        full=raw('docs/HIOC_MASTER_PLAN.md').decode(); assert_candidate_sequence(full)
        with self.assertRaises(ValueError):assert_candidate_sequence(full.replace('PE71_COMPLETE=FALSE','PE71_COMPLETE=TRUE'))
if __name__=='__main__':unittest.main()


# Reuse the already-established immutable PE-6 replay fixture. This helper changes
# no validator body or expected identity and does not exempt current source bytes.
def replay_historical_check(function, namespace):
    import test_pe6_classification_implementation as historical
    if getattr(historical,'_PE7_HISTORICAL_REPLAY',False):return function()
    outcome=[]
    def capture():
        try:outcome.append((True,function()))
        except BaseException as error:outcome.append((False,error,error.__traceback__))
    suite=historical.load_tests(unittest.TestLoader(),unittest.TestSuite([unittest.FunctionTestCase(capture)]),
        None,namespaces=(namespace,))
    result=unittest.TestResult();suite.run(result)
    require(len(outcome)==1 and not result.errors and not result.failures,'historical fixture failed')
    if not outcome[0][0]:raise outcome[0][1].with_traceback(outcome[0][2])
    return outcome[0][1]


def select_historical_checks(loader, tests, pattern, namespace, names):
    import test_pe6_classification_implementation as historical
    if not (ROOT/RECORD).exists():return tests
    current_successor()
    def select(suite):
        result=[]
        for test in suite:
            if isinstance(test,unittest.TestSuite):result.append(select(test))
            elif test._testMethodName in names:
                result.append(historical.load_tests(loader,unittest.TestSuite([test]),pattern,namespaces=(namespace,)))
            else:result.append(test)
        return unittest.TestSuite(result)
    return select(tests)


class PreservationTests(unittest.TestCase):
    def test_original_mqtt_implementations_not_rewritten(self):
        import ast
        previous=ast.parse(git('show',BASELINE+':pi4/lib/hioc/mqtt.py'))
        current=ast.parse(raw('pi4/lib/hioc/mqtt.py'))
        nodes=lambda tree:{n.name:ast.dump(n,include_attributes=False) for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
        old,new=nodes(previous),nodes(current)
        for key,value in old.items():self.assertEqual(new[key],value,key)

    def test_historical_assertions_and_original_validator_bodies_preserved(self):
        import ast
        paths=[x['path'] for x in SCOPE_EXTENSIONS if x['path'].startswith('tests/')]+['tests/test_pe6_classification_implementation.py']
        count=0
        for path in paths:
            old=ast.parse(git('show',BASELINE+':'+path));current=ast.parse(raw(path))
            methods=lambda tree:{c.name+'.'+n.name:ast.dump(n,include_attributes=False) for c in tree.body if isinstance(c,ast.ClassDef) for n in c.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
            before,after=methods(old),methods(current)
            for key,value in before.items():self.assertEqual(after[key],value,path+':'+key);count+=1
            names={'validate_closure_successor','closure_artifact_bindings','assert_historical_runtime_tree','validate_design'}
            for node in old.body:
                if isinstance(node,ast.FunctionDef) and node.name in names:
                    self.assertTrue(any(isinstance(candidate,ast.FunctionDef) and ast.dump(candidate,include_attributes=False)==ast.dump(node,include_attributes=False) for candidate in current.body),path+':'+node.name)
        self.assertGreater(count,52)

# Current successor validation is deliberately separate from current_candidate(),
# whose original PE-7.1 law above remains unchanged.
CURRENT_PARENT = '3f54723f3ece7c7b2b3bb3921776c9f2698967c1'
ACCEPTED_PE71 = '51398bab4e2293b578b2cdac2d0740c3738cab2f'
CURRENT_SCOPE = tuple(sorted([
    'docs/HIOC_MASTER_PLAN.md', 'docs/PE7_EXPECTED_AVAILABILITY_IMPLEMENTATION.md',
    RECORD, 'pi4/bin/hioc-availability-adapter.py', 'pi4/lib/hioc/asset_policy.py',
    'pi4/lib/hioc/availability_protocol.py', 'tests/test_pe73_ca_custody.py',
    'tests/test_pe73_provision_environment.py', 'tools/pe73_ha_delivery.py',
    'tools/pe73_ha_provision.py', 'docs/PE7_FULL_INVENTORY_AUTHORIZATION_AMENDMENT.md',
    'tests/test_pe73_full_inventory_authorization.py', 'tests/test_pe7_binding.py',
    'tests/test_pe6_classification_implementation.py', 'tools/pe73_pi3_provision_environment.py']))


@lru_cache(maxsize=None)
def immutable_tree(commit):
    require(commit in (BASELINE, CURRENT_PARENT, ACCEPTED_PE71), 'immutable tree authority')
    return {path: tuple(meta.split()[::2]) for meta, path in
            (row.split('\t', 1) for row in git('ls-tree', '-r', commit).decode().splitlines())}


@lru_cache(maxsize=None)
def accepted_pe71_record():
    return json.loads(git('show', ACCEPTED_PE71 + ':' + RECORD))


def successor_profile():
    """An external frozen test input, not a governance acceptance or deployment grant."""
    import os
    path = Path(os.environ.get('HIOC_SUCCESSOR_PROFILE', ''))
    require(path.is_absolute() and ROOT.resolve() not in path.resolve().parents,
            'external current profile required')
    value = path.read_bytes()
    require(sha(value) == os.environ.get('HIOC_SUCCESSOR_PROFILE_SHA256'),
            'external current profile identity')
    profile = json.loads(value)
    require(value == canonical(profile), 'canonical current profile')
    return profile


def current_successor(*, read=raw, git_runner=git, profile=None, byte_reader=None):
    """Validate this exact uncommitted successor; never infer edit permission from a diff."""
    profile = successor_profile() if profile is None else profile
    require(set(profile) == {'schema_version', 'checkpoint', 'parent', 'authorized_paths', 'files'},
            'closed current profile')
    require(profile['schema_version'] == '1.0' and profile['checkpoint'] == 'PE-7.3' and
            profile['parent'] == CURRENT_PARENT and profile['authorized_paths'] == list(CURRENT_SCOPE),
            'current profile authority')
    require(git_runner('branch', '--show-current').strip() == b'main', 'current branch')
    require(git_runner('rev-parse', 'HEAD').strip() == CURRENT_PARENT.encode(), 'current checkpoint parent')
    require(git_runner('rev-parse', 'origin/main').strip() == CURRENT_PARENT.encode(), 'current publication provenance')
    require(git_runner('rev-list', '--left-right', '--count', 'HEAD...origin/main').split() == [b'0', b'0'],
            'current divergence')
    require(Path(git_runner('rev-parse', '--show-toplevel').decode().strip()).resolve() == ROOT.resolve(),
            'current repository root')
    require(git_runner('remote', 'get-url', 'origin').strip() ==
            b'https://github.com/jorgeazofeifa-creator/hioc.git', 'current repository origin')
    require(not git_runner('diff', '--cached', '--name-only').strip(), 'candidate staging must remain empty')
    require(not git_runner('ls-files', '--unmerged').strip(), 'unresolved current conflict')
    changes = set(git_runner('diff', '--name-only', CURRENT_PARENT).decode().splitlines())
    untracked = set(git_runner('ls-files', '--others', '--exclude-standard').decode().splitlines())
    require(changes | untracked == set(CURRENT_SCOPE), 'unexpected current candidate path')
    tree = immutable_tree(CURRENT_PARENT)
    require(set(profile['files']) == set(tree) | set(CURRENT_SCOPE), 'complete current manifest')
    physical = byte_reader or (lambda path: (ROOT / path).read_bytes())
    observed = {}  # Per-invocation verified bytes only; never shared between calls.
    for path, item in profile['files'].items():
        require(set(item) == {'file_sha256', 'sha256', 'git_blob', 'mode'}, 'closed current manifest artifact')
        value = read(path)
        observed[path] = (value, sha(physical(path)))
        require((sha(value), blob(value), observed[path][1]) ==
                (item['sha256'], item['git_blob'], item['file_sha256']), 'current successor artifact identity: ' + path)
        require(item['mode'] == tree.get(path, ('100644', None))[0], 'current successor artifact mode')
        if path not in CURRENT_SCOPE:
            original = immutable_bytes(tree[path][1])
            require(value == original.replace(b'\r\n', b'\n'), 'unauthorized current baseline mutation')
    record = json.loads(observed[RECORD][0])
    original = accepted_pe71_record()
    require(observed[RECORD][0] == canonical(record), 'canonical successor record')
    require({k: v for k, v in record.items() if k != 'artifacts'} ==
            {k: v for k, v in original.items() if k != 'artifacts'}, 'historical record authority')
    require([x['path'] for x in record['artifacts']] == [x['path'] for x in original['artifacts']],
            'complete current artifact map')
    for item in record['artifacts']:
        require(set(item) == {'path', 'mode', 'sha256', 'file_sha256', 'git_blob'}, 'closed successor artifact')
        require({k: v for k, v in item.items() if k != 'path'} == profile['files'][item['path']],
                'current artifact record identity')
    baseline = immutable_tree(BASELINE)
    for item in record['protected']:
        value, file_sha256 = observed[item['path']]
        require((item['mode'], item['git_blob']) == baseline[item['path']] and
                sha(value) == item['sha256'] and file_sha256 == item['file_sha256'] and
                value == immutable_bytes(item['git_blob']).replace(b'\r\n', b'\n'), 'protected baseline artifact')
    require(sha(read(CONTRACT)) == CONTRACT_SHA, 'corrected contract identity')
    full = read('docs/HIOC_MASTER_PLAN.md').decode()
    status = full.split('# Implementation Status', 1)[1].split('# Historical Operator Preparation Chronology', 1)[0]
    next_task = full.split('## Next Planned Task', 1)[1].split('### Historical', 1)[0]
    for section in (status, next_task):
        require(all(s in section for s in ('PE73_STATUS=IN_PROGRESS', 'PE74_STATUS=NOT_AUTHORIZED',
                                           'PE73_COMPLETE=FALSE')), 'current successor lifecycle')
    amendment = read('docs/PE7_FULL_INVENTORY_AUTHORIZATION_AMENDMENT.md').decode()
    require('Status: ACCEPTED — OWNER-DIRECTED SUCCESSOR AUTHORIZATION.' in amendment and
            'Owner acceptance: HIOC PE-7.3: Finalize and Publish the Qualified Release Candidate.' in amendment and
            'availability_status=existing_assets as a deliberate successor change to section 6.1.' in amendment,
            'accepted successor amendment authority')
    return record


def assert_successor_sequence(text, *, read=raw, git_runner=git):
    current_successor(read=read, git_runner=git_runner)
    full = read('docs/HIOC_MASTER_PLAN.md').decode()
    status = full.split('# Implementation Status', 1)[1].split('# Historical Operator Preparation Chronology', 1)[0]
    require(text in (full, status), 'current lifecycle text substitution')
    return True


class OriginalCandidateReplaySuite(unittest.TestSuite):
    """Exact accepted PE-7.1 bytes with an explicitly synthetic original candidate view."""
    def run(self, result, debug=False):
        import io, tempfile, zipfile
        from contextlib import ExitStack
        from unittest.mock import patch
        repository_root = ROOT
        def repository_git(*args):
            return subprocess.check_output(['git', '--no-optional-locks', *args],
                                           cwd=repository_root, stderr=subprocess.PIPE)
        with tempfile.TemporaryDirectory(prefix='hioc-pe71-original-candidate-') as folder:
            snapshot = Path(folder)
            archive = zipfile.ZipFile(io.BytesIO(repository_git('archive', '--format=zip', ACCEPTED_PE71)))
            for member in archive.infolist():
                part = __import__('pathlib').PurePosixPath(member.filename)
                require(not part.is_absolute() and '..' not in part.parts and
                        (member.external_attr >> 16) & 0o170000 != 0o120000, 'historical archive path')
            archive.extractall(snapshot)
            original = json.loads((snapshot / RECORD).read_bytes())
            for item in original['artifacts'] + original['protected']:
                path = snapshot / item['path']; value = path.read_bytes()
                variants = (value, value.replace(b'\r\n', b'\n'),
                            value.replace(b'\r\n', b'\n').replace(b'\n', b'\r\n'))
                matched = next((v for v in variants if sha(v) == item['file_sha256']), None)
                if matched is None:
                    # Retained mixed-encoding bytes are evidence only when BOTH
                    # the historical raw digest and immutable normalized object agree.
                    retained = (repository_root / item['path']).read_bytes()
                    if sha(retained) == item['file_sha256'] and retained.replace(b'\r\n', b'\n') == value.replace(b'\r\n', b'\n'):
                        matched = retained
                require(matched is not None, 'unavailable original raw historical bytes: ' + item['path'])
                path.write_bytes(matched)
            def snapshot_read(path): return (snapshot / path).read_bytes().replace(b'\r\n', b'\n')
            def historical_git(*args):
                if args == ('branch', '--show-current'): return b'main\n'
                if args in [('rev-parse', 'HEAD'), ('rev-parse', 'origin/main')]: return (BASELINE + '\n').encode()
                if args in [('ls-files', '--others', '--exclude-standard'), ('diff', '--cached', '--name-only')]: return b''
                if args == ('diff', '--name-only', BASELINE): return repository_git('diff', '--name-only', BASELINE, ACCEPTED_PE71)
                return repository_git(*args)
            defaults = [(function, function.__kwdefaults__) for function in (historical_candidate_validator, assert_candidate_sequence)]
            try:
                with ExitStack() as stack:
                    stack.enter_context(patch.dict(globals(), ROOT=snapshot, raw=snapshot_read, git=historical_git,
                                                       current_candidate=historical_candidate_validator))
                    for function, previous in defaults:
                        function.__kwdefaults__ = dict(previous, read=snapshot_read, git_runner=historical_git)
                    return super().run(result, debug)
            finally:
                for function, previous in defaults: function.__kwdefaults__ = previous


def bind_regression_suite(loader, suite, pattern=None):
    """Only named PE-4 and sealed-toolkit historical assertions replay; current APIs stay current."""
    import sys
    import test_pe6_classification_implementation as historical
    historical.install_immutable_git_reads()
    target = ('test_pe4_ha_association_deployment_closure.DeploymentClosureTests.'
              'test_master_authoritative_lifecycle_objective_and_next_agree')
    sealed = {
        'test_pe73_ca_custody.BoundaryTests.test_exact_profile_identity',
        'test_pe73_ca_custody.BoundaryTests.test_same_engine_cp311_offline_pins',
        'test_pe73_ca_custody.BoundaryTests.test_accepted_sources_unchanged',
        'test_pe73_ca_custody.NativeIdentityTests.test_no_network_fetch_during_manual_signing_engine_load',
    }
    def select(node):
        if isinstance(node, unittest.TestSuite):
            node._tests = [select(child) for child in node if child is not None]
            return node
        if node.id().removeprefix('tests.') in sealed:
            return historical.load_tests(loader, unittest.TestSuite([node]), pattern,
                namespaces=(vars(sys.modules[node.__class__.__module__]),), revision=CURRENT_PARENT)
        if node.id() == target:
            return historical.load_tests(loader, unittest.TestSuite([node]), pattern,
                                         namespaces=(vars(sys.modules[node.__class__.__module__]),))
        return node
    return select(suite)


def load_tests(loader, tests, pattern):
    current_successor()
    def select(node):
        if isinstance(node, unittest.TestSuite): return unittest.TestSuite([select(child) for child in node])
        if isinstance(node, BindingTests): return OriginalCandidateReplaySuite([node])
        return node
    return select(tests)


class CurrentSuccessorTests(unittest.TestCase):
    def test_exact_current_scope_and_manifest(self):
        record = current_successor()
        self.assertEqual(len(record['artifacts']), 39)
        self.assertEqual(len(record['protected']), 449)
        self.assertEqual(len(CURRENT_SCOPE), 15)

    def test_current_smoke_and_sealed_installer_have_separate_exact_authorities(self):
        import importlib.util
        path = ROOT / 'tools/pe73_pi3_provision_environment.py'
        spec = importlib.util.spec_from_file_location('pe73_current_profile_binding', path)
        profile = importlib.util.module_from_spec(spec); spec.loader.exec_module(profile)
        original = __import__('types').ModuleType('pe73_original_profile_binding')
        exec(compile(git('show', CURRENT_PARENT + ':tools/pe73_pi3_provision_environment.py'),
                     'immutable-original-profile', 'exec'), original.__dict__)
        historical_sha = '2594d985f76d51b02365ca2ef98f02ac4372e566559be893762a41e6ccb39d89'
        current_sha = '1840149979827c76f58e2c933ff70e7f1dfed90788ac97abf004b6218f0e56e8'
        self.assertEqual(sha((ROOT / 'tools/pe73_ha_provision.py').read_bytes()), current_sha)
        self.assertEqual(profile.EXTRA_SMOKE, original.EXTRA_SMOKE.replace(historical_sha, current_sha))
        self.assertEqual(profile.HISTORICAL_EXTRA_SMOKE, original.EXTRA_SMOKE)
        engine_bytes = (ROOT / 'tools/pe73_provision_environment.py').read_bytes()
        engine = profile.profile(profile.load_engine(engine_bytes))
        old_engine = original.profile(original.load_engine(engine_bytes))
        self.assertEqual(engine.SMOKE, old_engine.SMOKE)
        self.assertEqual(engine.TOOLKIT, old_engine.TOOLKIT)
        for raw in (b'arbitrary', (ROOT / 'tools/pe73_ha_provision.py').read_bytes() + b' '):
            class Source:
                def __truediv__(self, name): return self
                def read_bytes(self): return raw
            with self.assertRaises(AssertionError):
                exec(compile(profile.EXTRA_SMOKE, 'current-smoke-negative-source', 'exec'),
                     dict(root=Source(), hashlib=__import__('hashlib')))
        with self.assertRaisesRegex(ValueError, 'unsupported historical replay authority'):
            __import__('test_pe6_classification_implementation').load_tests(
                unittest.TestLoader(), unittest.TestSuite(), None, revision='0' * 40)

    def test_sealed_replay_restores_exact_raw_objects_and_caller_root(self):
        import types
        import test_pe6_classification_implementation as historical
        namespace = {'R': ROOT}
        before = namespace['R']
        def check():
            self.assertNotEqual(namespace['R'], before)
            for path, identity in {
                'tools/pe73_pi3_provision_environment.py': 'f55543e7207dc7bd9b23e7262f1b17c17fcc568afdf64d8aad6335321f6f93f1',
                'tools/pe73_provision_environment.py': '0e5d41b05729907ad1e629c8d77bf57a25890f600f7e2fcf29071c106fa0b3d7',
            }.items():
                self.assertEqual(sha((namespace['R'] / path).read_bytes()), identity)
                self.assertEqual((namespace['R'] / path).read_bytes(), git('show', CURRENT_PARENT + ':' + path))
        result = unittest.TestResult()
        historical.load_tests(unittest.TestLoader(), unittest.TestSuite([unittest.FunctionTestCase(check)]),
            None, namespaces=(namespace,), revision=CURRENT_PARENT).run(result)
        self.assertEqual(result.errors, []); self.assertEqual(result.failures, [])
        self.assertEqual(namespace['R'], before)

    def test_wrong_current_git_authority_is_rejected(self):
        pairs = [(('branch', '--show-current'), b'foreign\n'),
                 (('rev-parse', 'HEAD'), b'0'*40),
                 (('rev-parse', 'origin/main'), BASELINE.encode()),
                 (('rev-list', '--left-right', '--count', 'HEAD...origin/main'), b'1\t0'),
                 (('rev-parse', '--show-toplevel'), str(ROOT.parent).encode()),
                 (('remote', 'get-url', 'origin'), b'https://invalid.example/repo'),
                 (('diff', '--cached', '--name-only'), b'staged.txt'),
                 (('ls-files', '--unmerged'), b'conflict'),
                 (('ls-files', '--others', '--exclude-standard'), b'foreign.txt'),
                 (('diff', '--name-only', CURRENT_PARENT), b'')]
        for command, answer in pairs:
            with self.subTest(command=command), self.assertRaises(ValueError):
                current_successor(git_runner=lambda *args: answer if args == command else git(*args))

    def test_missing_manifest_wrong_parent_scope_or_identity_rejected(self):
        import copy
        original = successor_profile()
        variants = []
        changed = copy.deepcopy(original); changed['parent'] = BASELINE; variants.append(changed)
        changed = copy.deepcopy(original); changed['authorized_paths'].pop(); variants.append(changed)
        changed = copy.deepcopy(original); changed['files'].pop(RECORD); variants.append(changed)
        changed = copy.deepcopy(original); changed['files'][RECORD]['sha256'] = '0'*64; variants.append(changed)
        for changed in variants:
            with self.subTest(profile=variants.index(changed)), self.assertRaises(ValueError): current_successor(profile=changed)

    def test_current_candidate_and_protected_changes_rejected(self):
        for path in ('pi4/lib/hioc/asset_policy.py', 'tools/pe73_ha_provision.py',
                     'tests/test_pe73_full_inventory_authorization.py', RECORD,
                     'docs/PE7_FULL_INVENTORY_AUTHORIZATION_AMENDMENT.md', 'pi4/lib/hioc/inventory.py'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                current_successor(read=lambda p: raw(p) + b' ' if p == path else raw(p))

    def test_raw_encoding_mode_and_lifecycle_substitution_rejected(self):
        import copy
        profile = successor_profile(); changed = copy.deepcopy(profile)
        changed['files']['tools/pe73_ha_provision.py']['mode'] = '100755'
        with self.assertRaises(ValueError): current_successor(profile=changed)
        with self.assertRaises(ValueError):
            current_successor(byte_reader=lambda p: (ROOT/p).read_bytes() + b' ' if p == RECORD else (ROOT/p).read_bytes())
        full = raw('docs/HIOC_MASTER_PLAN.md').decode()
        with self.assertRaises(ValueError): assert_successor_sequence(full.replace('PE73_COMPLETE=FALSE', 'PE73_COMPLETE=TRUE'))

    def test_historical_dispatch_is_exact_and_preserves_other_tests(self):
        class CurrentFailure(unittest.TestCase):
            def runTest(self): self.fail('CURRENT_FAILURE_MUST_SURVIVE')
        result = unittest.TestResult()
        bind_regression_suite(unittest.TestLoader(), unittest.TestSuite([CurrentFailure()])).run(result)
        self.assertEqual(len(result.failures), 1)
        self.assertIn('CURRENT_FAILURE_MUST_SURVIVE', result.failures[0][1])


    def test_legacy_current_entry_and_original_authority_remain_distinct(self):
        self.assertIs(current_candidate, current_successor)
        self.assertIsNot(historical_candidate_validator, current_candidate)
        with self.assertRaisesRegex(ValueError, 'current publication provenance'):
            historical_candidate_validator()


    def test_historical_dependency_head_and_bytes_share_one_view(self):
        import test_pe4_documentation_consistency_correction_closure as dependency
        import test_pe6_classification_implementation as historical
        previous_root, previous_git = dependency.ROOT, dependency.git
        def check():
            self.assertEqual(dependency.git('rev-parse', 'HEAD').strip(),
                             b'9d6ce274a80a578d488d7245ebfa5bca1d5f5a83')
            self.assertEqual(dependency.git('show', 'HEAD:.gitattributes').replace(b'\r\n', b'\n'),
                             (dependency.ROOT / '.gitattributes').read_bytes().replace(b'\r\n', b'\n'))
            self.assertEqual(dependency.current_bytes('.gitattributes'),
                             (dependency.ROOT / '.gitattributes').read_bytes().replace(b'\r\n', b'\n'))
        result = unittest.TestResult()
        historical.load_tests(unittest.TestLoader(), unittest.TestSuite([unittest.FunctionTestCase(check)]),
                              None).run(result)
        self.assertEqual(result.errors, [])
        self.assertEqual(result.failures, [])
        self.assertEqual(dependency.ROOT, previous_root)
        self.assertIs(dependency.git, previous_git)


    def test_immutable_cache_never_accepts_live_git_queries(self):
        import test_pe6_classification_implementation as historical
        for args in [('rev-parse', 'HEAD'), ('rev-parse', 'origin/main'),
                     ('diff', '--name-only', CURRENT_PARENT), ('diff', '--name-only', CURRENT_PARENT, 'HEAD'),
                     ('show', ':docs/HIOC_MASTER_PLAN.md'), ('ls-files', '--stage'),
                     ('status', '--porcelain'), ('branch', '--show-current')]:
            with self.subTest(args=args): self.assertFalse(historical.immutable_git_read(args))
        for args in [('show', CURRENT_PARENT + ':.gitattributes'), ('cat-file', 'blob', 'a'*40),
                     ('ls-tree', '-r', CURRENT_PARENT), ('diff', '--name-only', BASELINE, ACCEPTED_PE71)]:
            with self.subTest(args=args): self.assertTrue(historical.immutable_git_read(args))
        calls = []
        namespace = {'ROOT': ROOT}
        reader = historical.immutable_git_reader(namespace, lambda *a: calls.append(a) or b'fresh', ROOT)
        for _ in range(2): self.assertEqual(reader('rev-parse', 'HEAD'), b'fresh')
        self.assertEqual(len(calls), 2)
        namespace['ROOT'] = ROOT.parent
        reader('show', CURRENT_PARENT + ':.gitattributes')
        self.assertEqual(len(calls), 3)

    def test_immutable_cache_returns_exact_objects_and_restores_namespaced_dependencies(self):
        import test_pe6_classification_implementation as historical
        import tests.test_pe4_0c_association_contract as dependency
        namespace = {'ROOT': ROOT}
        reader = historical.immutable_git_reader(namespace, git, ROOT)
        query = ('show', CURRENT_PARENT + ':.gitattributes')
        expected = git(*query)
        self.assertEqual(reader(*query), expected)
        hits = historical._immutable_replay_command.cache_info().hits
        self.assertEqual(reader(*query), expected)
        self.assertGreater(historical._immutable_replay_command.cache_info().hits, hits)
        previous = dependency.ROOT
        def check(): self.assertNotEqual(dependency.ROOT, previous)
        result = unittest.TestResult()
        historical.load_tests(unittest.TestLoader(), unittest.TestSuite([unittest.FunctionTestCase(check)]), None).run(result)
        self.assertEqual(result.errors, [])
        self.assertEqual(result.failures, [])
        self.assertEqual(dependency.ROOT, previous)


# Existing cross-phase wrappers import this public CURRENT entry directly.
# Preserve the original function object/law for the explicit historical fixture.
historical_candidate_validator = current_candidate
current_candidate = current_successor
