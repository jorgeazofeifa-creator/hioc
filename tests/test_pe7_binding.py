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
    current_candidate()
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
