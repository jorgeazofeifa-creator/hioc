"""Finite operator entry for existing PE-7.3 trust and disabled HA delivery.

No import-time I/O, automatic recovery, activation or PI3 runtime replacement.
Every production entry requires an immutable toolkit manifest and sealed venv.
"""
from __future__ import annotations
import argparse,base64,contextlib,datetime,getpass,hashlib,importlib.util,json,os
from pathlib import Path
import re,secrets,shlex,shutil,stat,subprocess,sys,uuid

ROOT=Path(__file__).resolve().parents[1]
LIMIT=1048576
MANIFEST='tools/pe73-completion-package.json'
PI3_ENV=Path('/home/jazofv1/.hioc-pe73-provision-environment')
PI5_ENV=Path('/root/.hioc-pe73-provision-environment')
CA_ENV=Path('/root/.hioc-pe73-ca-signing-environment')
SCHEDULER='3f56b904fc1dd40ccbfa3fdd61cb910c4d215e9ac28a9bf2dcdf3721c73b62a9'
AMENDMENT='PE73_FULL_INVENTORY_ASSET_AUTHORIZATION_V1'
ACCEPTANCE='ACCEPTED_20f7f4c64fd32865f006ecfb2135ae6bbcada16c'

class Stop(ValueError):pass
def require(value,code):
    if not value:raise Stop(code)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode()
def module(name):
    path=ROOT/'tools'/(name+'.py')
    spec=importlib.util.spec_from_file_location('pe73_completion_'+name,path)
    value=importlib.util.module_from_spec(spec);spec.loader.exec_module(value);return value

def toolkit(expected,root=None):
    root=ROOT if root is None else root
    raw=(root/MANIFEST).read_bytes();require(sha(raw)==expected,'TOOLKIT_MANIFEST_IDENTITY')
    value=json.loads(raw)
    require(set(value)=={'version','payload_release','files'} and value['version']==1 and
        value['payload_release']=='20f7f4c64fd32865f006ecfb2135ae6bbcada16c','TOOLKIT_SCOPE')
    for name,row in value['files'].items():
        require(re.fullmatch(r'(?:tools|governance/pe7|payloads)/[A-Za-z0-9_./-]+',name) and
            '..' not in Path(name).parts,'TOOLKIT_PATH')
        path=root/name;info=path.lstat();raw=path.read_bytes()
        require(stat.S_ISREG(info.st_mode) and info.st_nlink==1 and info.st_uid==os.getuid()
            and not stat.S_IMODE(info.st_mode)&0o022 and len(raw)<=LIMIT and sha(raw)==row['sha256']
            and hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==row['git_blob'],'TOOLKIT_FILE_IDENTITY')
    return value

def environment(role):
    """Verify accepted environments in place; never install or alter dependencies."""
    require(role in {'pi3','pi5','ca'},'TARGET_ROLE')
    root={'pi3':PI3_ENV,'pi5':PI5_ENV,'ca':CA_ENV}[role]
    uid=1000 if role=='pi3' else 0
    require(sys.platform=='linux' and os.getuid()==os.geteuid()==os.getgid()==os.getegid()==uid
        and Path(sys.prefix)==root/'venv','ISOLATED_TARGET_IDENTITY')
    q=module('pe73_ha_provision');binding=q.native()
    files=binding.PrivateFiles(str(root),(uid,uid))
    try:raw=files.read(str(root/'ready.json'))
    except FileNotFoundError:raise Stop('ENVIRONMENT_READY_MISSING') from None
    try:seal=json.loads(raw)
    except (ValueError,TypeError):raise Stop('ENVIRONMENT_SEAL_SHAPE') from None
    require(type(seal)is dict and set(seal)=={'schema','source_python','python_version','files','versions'}
        and seal['schema']==1 and type(seal['files'])is dict,'ENVIRONMENT_SEAL_SHAPE')
    # The installers are immutable package code, NOT members of the original
    # PI3/PI5 environment seals. Never import or copy a missing environment tool.
    engine=module('pe73_provision_environment')
    profile=module('pe73_pi3_provision_environment')
    require(sha((ROOT/'tools/pe73_provision_environment.py').read_bytes())==
        profile.ENGINE_SOURCE['sha256'],'ENVIRONMENT_VERIFIER_IDENTITY')
    if role=='pi3':
        profile.target();engine=profile.profile(engine)
    elif role=='ca':
        module('pe73_ca_custody').target();engine.ROOT=root;engine.WHEELS=profile.WHEELS
    else:engine.target()
    engine.owned_directory(root,0o700)
    verify_environment(seal,engine,root,role)
    if role=='pi3':binding.sibling('pe73_maintenance_window').NativeOps().target_boot()
    if role=='ca':module('pe73_ca_custody').target()
    q.crypto()
    return q,binding

def verify_environment(seal,engine,root,role):
    """Read-only original seal comparison using the accepted fingerprint algorithm."""
    require(seal['source_python']==sha(Path('/usr/bin/python3').resolve().read_bytes()),'ENVIRONMENT_PYTHON_EXECUTABLE_DRIFT')
    require(seal['python_version']==list(sys.version_info[:3]),'ENVIRONMENT_PYTHON_VERSION_DRIFT')
    require(seal['versions']==engine.VERSIONS,'ENVIRONMENT_DEPENDENCY_VERSION_DRIFT')
    # The original installer explicitly selected these historical source objects.
    # ready.json alone cannot approve arbitrary replacement provisioning sources.
    expected={item['name']:item['sha256'] for item in engine.TOOLKIT}
    if role=='ca':
        custody=module('pe73_ca_custody')
        expected.update({custody.PROFILE_SOURCE['name']:custody.PROFILE_SOURCE['sha256'],
            'pe73_provision_environment.py':module('pe73_pi3_provision_environment').ENGINE_SOURCE['sha256']})
    require({name.removeprefix('tools/') for name in seal['files'] if name.startswith('tools/')}==set(expected),
        'ENVIRONMENT_SEALED_TOOL_INVENTORY')
    for name,identity in expected.items():
        require(seal['files'].get('tools/'+name,{}).get('sha256')==identity,'ENVIRONMENT_SEALED_SOURCE_IDENTITY')
    for name in seal['files']:
        require(type(name)is str and not Path(name).is_absolute() and '..' not in Path(name).parts,'ENVIRONMENT_SEAL_PATH')
        require(os.path.lexists(root/name),'ENVIRONMENT_SEALED_FILE_MISSING')
    try:observed=engine.fingerprint(root)
    except FileNotFoundError:raise Stop('ENVIRONMENT_SEALED_FILE_MISSING') from None
    require(observed==seal['files'],'ENVIRONMENT_FINGERPRINT_MISMATCH')

FAILED_MANIFEST='b2a05139dd686273959310a749a29b13a7332b0aa26ae693b713eba693eaf81b'

def assess_backend(q,binding):
    """No key generation/writes. Refuse any retained context or trust candidate.

    Combined with the proven pre-mutation failure path, this establishes whether
    a fresh operation can be considered; it never retries prepare-backend.
    """
    profile=module('pe73_pi3_provision_environment')
    home=PI3_ENV.parent;runtime=home/'hioc'
    old=home/('.hioc-pe73-completion-'+FAILED_MANIFEST[:16])
    profile.owned_directory(old,0o700)
    toolkit(FAILED_MANIFEST,old)
    for parent in (home,runtime):
        admitted=profile.owned_directory(parent)
        fd=os.open(parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC)
        try:
            before=os.fstat(fd)
            require(binding.identity(admitted)==binding.identity(before),'PREPARATION_INVENTORY_DRIFT')
            names=os.listdir(fd)
            require(len(names)<=4096,'PREPARATION_INVENTORY_LIMIT')
            require(not any(name.startswith('hioc_pe73_') for name in names),'EXISTING_PRIVATE_STATE_REQUIRES_REVIEW')
            for name in names:
                if name.startswith('.hioc-pe73-completion-'):
                    candidate=parent/name;profile.owned_directory(candidate,0o700)
                    require(not os.path.lexists(candidate/'session'),'EXISTING_SESSION_NO_RETRY')
            after=os.fstat(fd);named=parent.lstat()
            require(binding.identity(before)==binding.identity(after)==binding.identity(named),'PREPARATION_INVENTORY_DRIFT')
        finally:os.close(fd)
    return result('PASS_READ_ONLY_PE73_PREPARATION_COMPATIBILITY',
        failed_toolkit_verified=True,environment_fingerprint='PASS',retained_preparation_candidates=0,
        trust_material_created=False,production_runtime_modified=False,
        preparation_executed=False,next_action_requires_separate_authorization=True)


def session(binding,create=False):
    """One private context in the new toolkit, not a production authority record."""
    parent=ROOT/'session'
    if create:
        os.mkdir(parent,0o700)
        fd=os.open(parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC)
        try:os.fsync(fd)
        finally:os.close(fd)
        fd=os.open(ROOT,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC)
        try:os.fsync(fd)
        finally:os.close(fd)
    value=binding.PrivateFiles(str(parent),(os.getuid(),os.getgid()))
    with value.directory():pass
    return value

def context(binding,create=None):
    files=session(binding,create=create is not None)
    name=files.parent+'/context.json'
    if create is not None:files.provision(name,canonical(create))
    raw=files.read(name);value=json.loads(raw)
    require(canonical(value)==raw and set(value)=={'plan_sha256','parent','reference','ssh_port'} and
        re.fullmatch('[0-9a-f]{64}',value['plan_sha256']) and
        re.fullmatch('[A-Za-z0-9_-]{8,96}',value['reference']),'SESSION_CONTEXT')
    return value,files

def ha_namespace(binding,reference):
    require(re.fullmatch('PE73_COMPLETION_[0-9a-f]{32}',reference),'HA_TRANSACTION_REFERENCE')
    expected='backups/pe73-ha-attempt-'+reference[-32:]
    if binding.d.TX=='backups/pe73-ha-delivery-v1':binding.d.configure_transaction(reference[-32:])
    require(binding.d.TX==expected,'HA_TRANSACTION_CONTEXT')


def private(q,binding,role):
    value,_=context(binding)
    if role=='pi3':
        require(re.fullmatch('/home/jazofv1/hioc/hioc_pe73_[0-9a-f]{16}',value['parent']),'PI3_PRIVATE_SCOPE')
        files=binding.PrivateFiles(value['parent'],(1000,1000));fs=None
    else:
        ha_namespace(binding,value['reference'])
        fs=binding.d.native_filesystem()
        require(re.fullmatch(re.escape(fs._root)+'/hioc_pe73_[0-9a-f]{16}',value['parent']),'PI5_PRIVATE_SCOPE')
        files=binding.PrivateFiles(value['parent'],fs._core)
    plan=q.read_plan(files)
    require(sha(canonical(plan))==value['plan_sha256'] and plan['reference']==value['reference']
        and plan['helper_sha256']==sha((ROOT/'tools/pe73_ha_provision.py').read_bytes()),'PRIVATE_PLAN_DRIFT')
    return files,plan,value,fs

def plan(q):
    """Local policy values only; no repeated architecture choice or approvals."""
    ask=q.policy_input
    actor=getpass.getpass('Approved human HA operator ID (hidden): ').strip()
    operations=[x.strip() for x in getpass.getpass('Explicit permitted operations (get,create,update,result,availability_status; hidden): ').split(',')]
    require(bool(operations) and len(set(operations))==len(operations) and set(operations)<=set(q.POPULATION_SCOPES),'EXPLICIT_ACTOR_OPERATIONS')
    issuer=uuid.uuid4().hex;name='hioc_pe73_'+secrets.token_hex(8)
    actors={actor:{op:{'scope':q.POPULATION_SCOPES[op],'amendment':AMENDMENT,'acceptance_reference':ACCEPTANCE} for op in operations}}
    value=dict(backend_address='192.168.100.252',ha_address='192.168.100.251',
        backend_port=int(ask('Reserved disabled product port')),guard_port=int(ask('Temporary observer port')),
        private_name=name,ha_parent='/config/'+name,backend_parent='/home/jazofv1/hioc/'+name,
        ca_name=ask('Approved offline CA subject label'),server_name=ask('Approved server subject label'),
        client_name=ask('Approved HA client subject label'),valid_days=int(ask('Approved certificate validity days')),
        issuer=issuer,key_id='pe73_'+secrets.token_hex(8),actors=actors,
        frontend_origin=ask('Existing approved HTTPS HA frontend origin'),reference='PE73_COMPLETION_'+uuid.uuid4().hex,
        toolkit='/home/jazofv1/'+ROOT.name+'/tools',helper_sha256=sha((ROOT/'tools/pe73_ha_provision.py').read_bytes()))
    return q.validate_plan(value)

def transfer(operation,expected,port,payload=b''):
    require(operation in {'plan','request','bundle'} and type(port)is int and 1<=port<=65535,'TRANSFER_SCOPE')
    require(len(payload)<=LIMIT,'TRANSFER_SIZE')
    runner=ROOT/'tools/pe73_completion.py';runner_sha=sha(runner.read_bytes())
    remote='/home/jazofv1/'+ROOT.name+'/tools/pe73_completion.py'
    wrapper="import hashlib,sys; p=sys.argv[1]; r=open(p,'rb').read(1048577); assert len(r)<=1048576 and hashlib.sha256(r).hexdigest()==sys.argv[2]; sys.argv=[p,*sys.argv[3:]]; exec(compile(r,p,'exec'),{'__name__':'__main__','__file__':p})"
    command=shlex.join([str(PI3_ENV/'venv/bin/python3'),'-I','-B','-c',wrapper,remote,runner_sha,'pipe-'+operation,'--manifest-sha',expected])
    binary=shutil.which('ssh');require(binary,'EXISTING_AUTHENTICATED_SSH_REQUIRED')
    result=subprocess.run([binary,'-T','-o','StrictHostKeyChecking=yes','-o','BatchMode=yes','-o','ClearAllForwardings=yes',
        '-o','RequestTTY=no','-o','LogLevel=ERROR','-o','ConnectTimeout=10','-p',str(port),'jazofv1@192.168.100.252',command],
        input=payload,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=45)
    require(result.returncode==0 and len(result.stdout)<=LIMIT,'PRIVATE_TRANSFER_UNCERTAIN')
    return result.stdout

def prepare_backend(q,binding):
    assess_backend(q,binding)  # Fresh admission, not a retry inferred from session absence.
    require(not (ROOT/'session').exists(),'EXISTING_SESSION_NO_RETRY')
    value=plan(q);c=module('pe73_ca_custody');values=c.runtime_material(q,value)
    context(binding,create=dict(parent=value['backend_parent'],plan_sha256=sha(canonical(value)),reference=value['reference'],ssh_port=None))
    files,_=q.create_parent(binding,'backend',value['private_name']);c.write_new(files,values)
    return result('PASS_PI3_TRUST_REQUEST_PREPARATION')

def ha_request(q,binding,expected):
    require(not (ROOT/'session').exists(),'EXISTING_SESSION_NO_RETRY')
    text=q.policy_input('Existing PI3 SSH port');require(text.isdecimal(),'SSH_PORT_REQUIRED');port=int(text)
    raw=transfer('plan',expected,port);value=json.loads(raw)
    require(canonical(value)==raw,'TRANSFER_PLAN_CANONICAL');q.validate_plan(value)
    require(value['helper_sha256']==sha((ROOT/'tools/pe73_ha_provision.py').read_bytes()) and
        value['toolkit']=='/home/jazofv1/'+ROOT.name+'/tools','PEER_TOOLKIT_IDENTITY')
    key,csr=q.create_request(value)
    ha_namespace(binding,value['reference'])
    fs=binding.d.native_filesystem();parent=fs._root+'/'+value['private_name']
    context(binding,create=dict(parent=parent,plan_sha256=sha(raw),reference=value['reference'],ssh_port=port))
    files,_=q.create_parent(binding,'ha',value['private_name'])
    require(files.parent==parent,'PRIVATE_PARENT_CHANGED')
    q.stage(files,{'plan.json':raw,'client.key':key,'client.csr':csr});key=None
    response=json.loads(transfer('request',expected,port,csr))
    require(response.get('RESULT')=='PASS_PUBLIC_CSR_IMPORTED','CSR_TRANSFER_UNCERTAIN')
    return result('PASS_PI5_LOCAL_CLIENT_KEY_REQUEST')

def signer(q,binding,action):
    """Root reads public plan/CSRs only; emits only public issuance response."""
    c=module('pe73_ca_custody')
    user_root=Path('/home/jazofv1')/ROOT.name
    index=binding.PrivateFiles(str(user_root/'session'),(1000,1000))
    value=json.loads(index.read(index.parent+'/context.json'))
    require(re.fullmatch('/home/jazofv1/hioc/hioc_pe73_[0-9a-f]{16}',value['parent']),'PUBLIC_REQUEST_PARENT')
    files=binding.PrivateFiles(value['parent'],(1000,1000));value_plan=q.read_plan(files)
    require(sha(canonical(value_plan))==value['plan_sha256'] and value_plan['helper_sha256']==sha((ROOT/'tools/pe73_ha_provision.py').read_bytes()) and value_plan['toolkit']==str(user_root/'tools'),'PUBLIC_PLAN_BINDING')
    vault=c.vault_files(q)
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter('error',getpass.GetPassWarning)
        password=getpass.getpass('Offline CA passphrase (not stored or echoed): ').encode()
    if action=='sign-server':
        require(len(password)>=16,'CA_PASSPHRASE_MINIMUM')
        c.initialize_ca(q,vault,value_plan,password)
    role='server' if action=='sign-server' else 'client'
    raw=files.read(files.parent+'/'+role+'.csr')
    return c.sign_request(q,vault,value_plan,password,role,raw)

def delivery(q,binding,expected,verify=False):
    files,value,ctx,fs=private(q,binding,'pi5')
    trust=binding.TrustSide('ha',files,binding.native_packet(files,files.parent+'/packet.json'),core_root=fs._root)
    proof=fs._proof
    host=binding.digest({k:proof[k] for k in ('boot_id','terminal','core_container','core','root')})
    capabilities=fs._probe.public_capabilities(proof['core_container'])
    approved={k:v['sha256'] for k,v in capabilities.items() if type(v)is dict and 'sha256' in v}
    require('components/frontend/__init__.py' in approved,'LIVE_FRONTEND_SOURCE_REQUIRED')
    state=binding.NativeHAState(fs,files,files.parent+'/pe73-delivery-lease.json',value['reference'],host,approved,risk_acknowledgement=binding.RISKS)
    if verify:
        saved=json.loads(files.read(files.parent+'/ha-delivery-completion.json'))
        require(saved['manifest_sha256']==expected,'VERIFICATION_TOOLKIT_DRIFT')
        # Reuse the same proven host; no fresh lease or mutation in independent verification.
        require(host==saved['host_identity'] and binding.digest(capabilities)==saved['capability_identity'],'VERIFICATION_HOST_DRIFT')
        with trust.context():pass
        require(trust.first==saved['trust_identity'],'VERIFICATION_TRUST_DRIFT')
        with binding.authenticated_proxy() as proxy:
            api=binding.DeliveryAPI(proxy,fs,read_only=True)
            j=fs.load();require(binding.digest(j)==saved['journal_sha256'],'VERIFICATION_JOURNAL_DRIFT')
            require(trust.read_packet()==j['observation']['packet'],'VERIFICATION_PACKET_DRIFT')
            require(j['state']=='DELIVERED_DISABLED' and j['pending']is None,'HA_TERMINAL_REQUIRED')
            require(api.call({'type':'lovelace/config','url_path':binding.d.DASHBOARD})==j['observation']['after'],'DASHBOARD_READBACK')
            rows=api.call({'type':'lovelace/resources/list'})
            require(rows==j['observation']['resources']+[j['resource']],'RESOURCE_READBACK')
            require('hioc_operator' not in api.call({'type':'get_services'}),'NO_ACTIVATION')
            require('hioc_operator' not in api.call({'type':'get_config'})['components'],'NO_ACTIVATION')
            exports(j,fs,binding.d)
            route=binding.RouteProbe(value['frontend_origin'],value['ha_address'])
            driver=binding.d.Delivery(fs,api,lambda:None,lambda _:None,lambda *_:b'',route_probe=route)
            driver.verify(j,dict(dashboard=binding.d.DASHBOARD,resource_url='/local/hioc-asset-editor.js'))
        return result('PASS_PE73_HA_INDEPENDENT_INSTALLATION_VERIFICATION',files=4,views=6,export_backup='PASS',trust='LOCAL_CERTIFICATE_PACKET_PASS_LIVE_PAIR_ACCEPTED_AT_DELIVERY')
    require(not fs._existing,'EXISTING_HA_TRANSACTION_NO_RETRY')
    # All trust, API, route-origin and payload prerequisites are checked before first lease.
    with trust.context():pass
    route=binding.RouteProbe(value['frontend_origin'],value['ha_address'])
    route.endpoint()  # Prove TLS/peer before files, leases or API mutation.
    def read_object(release,name):
        require(release==binding.d.RELEASE,'HA_PAYLOAD_RELEASE')
        return (ROOT/'payloads'/name).read_bytes()
    with binding.authenticated_proxy() as proxy:
        api=binding.DeliveryAPI(proxy,fs)
        require('hioc_operator' not in api.call({'type':'get_services'}),'NO_ACTIVATION')
        api.call({'type':'lovelace/config','url_path':binding.d.DASHBOARD});api.call({'type':'lovelace/resources/list'})
        binding.d.artifacts(read_object)
        with binding.connect_peer(trust,value['guard_port'],value['reference']) as peer:
            packet=trust.read_packet();peer.check(packet)
            state.acquire()
            driver=binding.native_delivery(fs,proxy,trust,peer,state,route,read_object)
            approved_plan=dict(resource_url='/local/hioc-asset-editor.js',dashboard=binding.d.DASHBOARD,
                view=binding.d.VIEW,before_files={p:fs.snapshot(p,0o644) for p in binding.d.FILES.values()},
                ha_trust=packet['ha']['hioc_operator']['operator'],backend_trust=packet['backend'])
            driver.run(approved_plan,whole_process_reference=value['reference'])
            j=fs.load();exports(j,fs,binding.d)
            peer.finish(packet)
    files.provision(files.parent+'/ha-delivery-completion.json',canonical(dict(manifest_sha256=expected,
        transaction=binding.d.TX,host_identity=host,capability_identity=binding.digest(capabilities),journal_sha256=binding.digest(j),trust_identity=trust.first)))
    return result('PASS_PE73_HA_DELIVERED_DISABLED',files=4,views=6,export_backup='PASS',trust='LIVE_MTLS_HMAC_INDEPENDENT_ACL_PASS')

def exports(j,fs,d):
    require(json.loads(fs.read(d.TX+'/dashboard.before.json'))==j['observation']['config'] and
        json.loads(fs.read(d.TX+'/resources.before.json'))==j['observation']['resources'],'EXPORT_BACKUP_READBACK')
    require(j['observation']['after']==d.add_card(j['observation']['config'],d.VIEW),'ADDITIVE_DASHBOARD_ONLY')
    for i,target in enumerate(d.FILES.values()):
        before=j['observation']['before'][target]
        if before['exists']:require(sha(fs.read(d.TX+'/before-'+str(i)))==before['sha256'],'FILE_BACKUP_READBACK')

def result(code,**fields):
    return dict(RESULT=code,activation=False,automatic_retry=False,PI3_runtime_replaced=False,PE73='IN_PROGRESS',PE74='NOT_AUTHORIZED',STOP_REQUIRED=True,**fields)

def run(action,expected):
    toolkit(expected)
    role='ca' if action.startswith('sign-') else 'pi5' if action in {'ha-request','ha-complete','deliver-ha','verify-ha'} else 'pi3'
    q,binding=environment(role)
    if action=='assess-backend':return assess_backend(q,binding)
    if action=='prepare-backend':return prepare_backend(q,binding)
    if action=='ha-request':return ha_request(q,binding,expected)
    if action.startswith('sign-'):return signer(q,binding,action)
    if action in {'deliver-ha','verify-ha'}:return delivery(q,binding,expected,action=='verify-ha')
    files,value,ctx,fs=private(q,binding,'pi5' if role=='pi5' else 'pi3')
    if action.startswith('pipe-'):
        require(not sys.stdout.isatty(),'PRIVATE_PIPE_ONLY')
        if action=='pipe-request':
            raw=sys.stdin.buffer.read(16385);q.validate_request(value,raw);files.provision(files.parent+'/client.csr',raw)
            return {'RESULT':'PASS_PUBLIC_CSR_IMPORTED'}
        raw=files.read(files.parent+'/plan.json') if action=='pipe-plan' else q.export_bundle(files,binding)
        sys.stdout.buffer.write(raw);sys.stdout.buffer.flush();return None
    if action.startswith('import-'):
        require(not sys.stdin.isatty(),'PUBLIC_SIGNER_PIPE_REQUIRED')
        module('pe73_ca_custody').accept_public(q,binding,files,value,action[7:],sys.stdin.buffer.read(LIMIT+1).rstrip(b'\n'))
        return result('PASS_PUBLIC_CERTIFICATE_IMPORTED')
    if action=='complete-backend':return module('pe73_ca_custody').finish_runtime(q,binding,files,value)
    if action=='ha-complete':return q.finish_ha(files,transfer('bundle',expected,ctx['ssh_port']),binding,fs._root)
    require(action=='guard-backend','ACTION_SCOPE')
    trust=binding.TrustSide('backend',files,binding.native_packet(files,files.parent+'/packet.json'))
    state=binding.NativeBackendState(files,files.parent+'/pe73-delivery-lease.json',value['reference'],SCHEDULER,risk_acknowledgement=binding.RISKS)
    # Read-only native prerequisites are established before creating the observer lease.
    binding.current_runtime()
    with trust.context():pass
    state.acquire();print('PE73_GUARD=WAITING_FOR_ONE_AUTHENTICATED_PI5_SESSION',file=sys.stderr,flush=True)
    binding.serve_guard(trust,state,value['guard_port'])
    return result('PASS_FINITE_PE73_TRUST_GUARD')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=('assess-backend','prepare-backend','ha-request','sign-server','import-server','sign-client','import-client','complete-backend','ha-complete','guard-backend','deliver-ha','verify-ha','pipe-plan','pipe-request','pipe-bundle'))
    parser.add_argument('--manifest-sha',required=True);args=parser.parse_args()
    try:
        value=run(args.action,args.manifest_sha)
        if value is not None:print(canonical(value).decode())
        return 0
    except BaseException as error:
        code=str(error) if type(error).__name__ in {'Stop','Blocked','QualificationError','Failure'} and re.fullmatch('[A-Z][A-Z0-9_]{0,127}',str(error)) else 'INPUT_IDENTITY_CAPABILITY_OR_UNCERTAIN_OPERATION'
        print(canonical(result('FAIL_STOP_PE73_COMPLETION',action=args.action,failure_code=code,retained_state='PRESERVED_NO_AUTOMATIC_RECOVERY')).decode())
        return 1

if __name__=='__main__':raise SystemExit(main())
