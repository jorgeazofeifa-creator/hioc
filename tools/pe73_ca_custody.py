"""Manual PI3 CA custody successor. No daemon, runtime activation or user-venv sudo.

CA encrypted key: root-only vault. Runtime server key/HMAC: UID1000 only.
Existing validated environments and historical provisioning code are never edited.
The old co-located backend-init/backend-issue workflow is not authorized for use.
"""
from __future__ import annotations
import argparse
import base64
import datetime as dt
import getpass
import hashlib
import importlib.util
import ipaddress
import json
import os
from pathlib import Path
import platform
import secrets
import stat
import sys
import types
import urllib.request

ROOT=Path('/root/.hioc-pe73-ca-signing-environment')
VAULT=Path('/root/.hioc-pe73-ca-custody')
PROFILE_SOURCE={
 'url':'https://raw.githubusercontent.com/jorgeazofeifa-creator/hioc/7027ca033fb0b8f2839ba1f3f65893d0c25d001f/tools/pe73_pi3_provision_environment.py',
 'sha256':'f55543e7207dc7bd9b23e7262f1b17c17fcc568afdf64d8aad6335321f6f93f1',
 'name':'pe73_pi3_provision_environment.py','size':11457}
HELPER_SHA='2594d985f76d51b02365ca2ef98f02ac4372e566559be893762a41e6ccb39d89'
LIMIT=1048576

class Blocked(ValueError):pass

def require(value,code):
    if not value:raise Blocked(code)

def sha(raw):return hashlib.sha256(raw).hexdigest()
def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode()

def load_profile(raw=None):
    if raw is None:
        opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with opener.open(PROFILE_SOURCE['url'],timeout=30) as response:
            require(response.geturl()==PROFILE_SOURCE['url'],'PROFILE_REDIRECT_REFUSED')
            raw=response.read(LIMIT+1)
    require(type(raw)is bytes and len(raw)<=LIMIT and sha(raw)==PROFILE_SOURCE['sha256'],'PROFILE_IDENTITY_MISMATCH')
    profile=types.ModuleType('pe73_custody_dependency_profile')
    exec(compile(raw,PROFILE_SOURCE['url'],'exec'),profile.__dict__)
    return profile

def target():
    require(sys.platform=='linux' and platform.node()=='nutandpihole'
        and platform.machine()=='aarch64' and platform.python_implementation()=='CPython'
        and sys.version_info[:2]==(3,11),'PI3_HOST_OR_ABI_MISMATCH')
    require(os.getuid()==os.geteuid()==os.getgid()==os.getegid()==0,'ROOT_MANUAL_CUSTODY_REQUIRED')
    # A root process must never execute the validated UID1000-owned environment.
    executable=Path(sys.executable).resolve()
    allowed=(Path('/usr/bin/python3.11'),ROOT/'venv/bin/python3')
    require(executable in allowed,'ROOT_CONTROLLED_INTERPRETER_REQUIRED')
    for path in [executable,*executable.parents]:
        info=path.lstat()
        require(info.st_uid==0 and not stat.S_IMODE(info.st_mode)&0o022,'PRIVILEGED_INTERPRETER_ANCESTRY_UNSAFE')
    require(executable.is_file(),'PRIVILEGED_INTERPRETER_NOT_REGULAR')

def engine_for(profile,*,offline=False):
    if offline:
        raw=(ROOT/'tools/pe73_provision_environment.py').read_bytes()
        engine=profile.load_engine(raw)
    else:engine=profile.load_engine()
    # Reuse the exact accepted finite installer and CP311 wheel pins; no files in
    # either accepted PI3/PI5 environment are touched or executed with privilege.
    engine.ROOT=ROOT;engine.WHEELS=profile.WHEELS;engine.target=target
    engine.TOOLKIT=[*engine.TOOLKIT,PROFILE_SOURCE,
        {**profile.ENGINE_SOURCE,'name':'pe73_provision_environment.py'}]
    return engine

def helper(root=ROOT):
    path=root/'tools/pe73_ha_provision.py'
    raw=path.read_bytes();require(sha(raw)==HELPER_SHA,'ROOT_TOOLKIT_IDENTITY_MISMATCH')
    spec=importlib.util.spec_from_file_location('pe73_root_custody_original',path)
    q=importlib.util.module_from_spec(spec);spec.loader.exec_module(q)
    return q

def verify_ready(engine):
    engine.owned_directory(ROOT,0o700)
    ready=ROOT/'ready.json';info=ready.lstat()
    require(stat.S_ISREG(info.st_mode) and info.st_uid==info.st_gid==0
        and info.st_nlink==1 and stat.S_IMODE(info.st_mode)==0o600,'ROOT_READY_SECURITY')
    expected={'schema':1,'source_python':sha(Path('/usr/bin/python3').resolve().read_bytes()),
        'python_version':list(sys.version_info[:3]),'files':engine.fingerprint(ROOT),'versions':engine.VERSIONS}
    require(json.loads(ready.read_bytes())==expected,'ROOT_SIGNING_ENVIRONMENT_DRIFT')
    require(Path(sys.prefix)==ROOT/'venv','ROOT_SIGNING_VENV_REQUIRED')

def vault_files(q):
    binding=q.native();files=binding.PrivateFiles(str(VAULT),(0,0))
    with files.directory():pass
    return files

def create_vault(q):
    # Existing descriptor-secure publisher, one new direct child only. No chown,
    # chmod, adoption, cleanup or reuse of a pre-existing custody directory.
    parent=q.native().PrivateFiles('/root',(0,0))
    with parent.directory() as fd:
        os.mkdir(VAULT.name,0o700,dir_fd=fd);os.fsync(fd)
    return vault_files(q)

def prepare():
    target()
    require(not os.path.lexists(ROOT) and not os.path.lexists(VAULT),'EXISTING_CUSTODY_STATE_REFUSED')
    profile=load_profile();engine=engine_for(profile)
    result=engine.prepare()
    require(result['native_smoke']=='PASS','ROOT_SIGNER_DEPENDENCIES_NOT_ESTABLISHED')
    # Native toolkit imports, but never key generation/signing, during setup.
    raw=engine.invoke([str(ROOT/'venv/bin/python3'),'-I','-B','-c',
        "import importlib.util,sys; from pathlib import Path; p=Path(sys.argv[1]); s=importlib.util.spec_from_file_location('q',p); q=importlib.util.module_from_spec(s); s.loader.exec_module(q); q.crypto(); q.native()",
        str(ROOT/'tools/pe73_ha_provision.py')],ROOT)
    require(raw==b'','UNEXPECTED_SIGNER_SETUP_OUTPUT')
    q=helper();create_vault(q)
    return {'RESULT':'PASS_PI3_SEPARATE_CA_CUSTODY_PREPARATION','environment':str(ROOT),'vault':str(VAULT),
        'owner_uid':0,'owner_gid':0,'directory_mode':'0700','CA_created':False,
        'certificate_issued':False,'HMAC_created':False,'runtime_credentials_read':False,
        'accepted_PI3_PI5_environments_modified':False,'production_services_modified':False,
        'PE73':'IN_PROGRESS','PE74':'NOT_AUTHORIZED','STOP_REQUIRED':True}

def absent(files,names):
    for name in names:
        try:files.read(files.parent+'/'+name)
        except FileNotFoundError:continue
        raise Blocked('EXISTING_CUSTODY_DESTINATION_REFUSED')

def write_new(files,values):
    absent(files,values)
    for name,raw in values.items():files.provision(files.parent+'/'+name,raw)

def initialize_ca(q,files,plan,password):
    q.validate_plan(plan)
    require(files.parent==str(VAULT),'ROOT_VAULT_ONLY')
    absent(files,('plan.sha256','ca.pem','ca-offline.key'))
    ca,encrypted=q.generate_ca(plan,password)
    # No actor/ACL contents, runtime server key or assertion material in custody.
    write_new(files,{'plan.sha256':sha(q.canonical(plan)).encode(),'ca.pem':ca,'ca-offline.key':encrypted})
    return {'RESULT':'PASS_MANUAL_ROOT_CA_INITIALIZATION','STOP_REQUIRED':True}

def request(q,plan,role):
    q.validate_plan(plan);require(role in ('server','client'),'CSR_ROLE_INVALID')
    if role=='client':return q.create_request(plan)
    x,h,s,ec,_,oid=q.crypto();key=ec.generate_private_key(ec.SECP256R1())
    csr=(x.CertificateSigningRequestBuilder()
        .subject_name(x.Name([x.NameAttribute(oid.COMMON_NAME,plan['server_name'])]))
        .add_extension(x.SubjectAlternativeName([x.IPAddress(ipaddress.ip_address(plan['backend_address']))]),False)
        .sign(key,h.SHA256()))
    return key.private_bytes(s.Encoding.PEM,s.PrivateFormat.PKCS8,s.NoEncryption()),csr.public_bytes(s.Encoding.PEM)

def issue_server_request(q,plan,ca_raw,encrypted,password,raw):
    # Same accepted P256/SHA256/extension/validity contract as q.issue; unlike its
    # historical server branch, the server private key is generated by UID1000.
    x,h,s,ec,eku,oid=q.crypto();now=dt.datetime.now(dt.timezone.utc)
    require(type(raw)is bytes and len(raw)<=16384,'CSR_SIZE_INVALID')
    csr=x.load_pem_x509_csr(raw);public=csr.public_key()
    require(csr.is_signature_valid and csr.subject==x.Name([x.NameAttribute(oid.COMMON_NAME,plan['server_name'])]),'SERVER_REQUEST_SIGNATURE_OR_SUBJECT')
    require(isinstance(public,ec.EllipticCurvePublicKey) and public.curve.name=='secp256r1','SERVER_REQUEST_KEY_TYPE')
    require(len(csr.extensions)==1 and list(csr.extensions.get_extension_for_class(x.SubjectAlternativeName).value)==[x.IPAddress(ipaddress.ip_address(plan['backend_address']))],'SERVER_REQUEST_SAN_INVALID')
    ca=x.load_pem_x509_certificate(ca_raw);key=s.load_pem_private_key(encrypted,password)
    require(key.public_key().public_numbers()==ca.public_key().public_numbers(),'CA_KEY_MISMATCH')
    require(ca.subject==x.Name([x.NameAttribute(oid.COMMON_NAME,plan['ca_name'])]),'CA_IDENTITY_MISMATCH')
    ca.verify_directly_issued_by(ca)
    require(ca.not_valid_before_utc<=now<ca.not_valid_after_utc and ca.extensions.get_extension_for_class(x.BasicConstraints).value.ca,'CA_EXPIRED_OR_INVALID')
    cert=(x.CertificateBuilder().subject_name(csr.subject).issuer_name(ca.subject).public_key(public)
        .serial_number(x.random_serial_number()).not_valid_before(now-dt.timedelta(minutes=1))
        .not_valid_after(min(now+dt.timedelta(days=plan['valid_days']),ca.not_valid_after_utc))
        .add_extension(x.BasicConstraints(ca=False,path_length=None),True)
        .add_extension(x.KeyUsage(True,False,False,False,False,False,False,False,False),True)
        .add_extension(x.SubjectKeyIdentifier.from_public_key(public),False)
        .add_extension(x.AuthorityKeyIdentifier.from_issuer_public_key(ca.public_key()),False)
        .add_extension(x.SubjectAlternativeName([x.IPAddress(ipaddress.ip_address(plan['backend_address']))]),False)
        .add_extension(x.ExtendedKeyUsage([eku.SERVER_AUTH]),False).sign(key,h.SHA256()))
    cert.verify_directly_issued_by(ca)
    return cert.public_bytes(s.Encoding.PEM)+ca_raw

def sign_request(q,files,plan,password,role,csr):
    q.validate_plan(plan);require(files.parent==str(VAULT),'ROOT_VAULT_ONLY')
    require(role in ('server','client'),'CSR_ROLE_INVALID')
    require(files.read(files.parent+'/plan.sha256')==sha(q.canonical(plan)).encode(),'APPROVED_PLAN_DRIFT')
    name=role+'-issuance.json';absent(files,(name,))
    ca=files.read(files.parent+'/ca.pem');encrypted=files.read(files.parent+'/ca-offline.key')
    if role=='server':chain=issue_server_request(q,plan,ca,encrypted,password,csr)
    else:chain,_=q.issue(plan,ca,encrypted,password,csr_raw=csr)
    public={'schema':1,'role':role,'plan_sha256':sha(q.canonical(plan)),
        'csr_sha256':sha(csr),'ca':base64.b64encode(ca).decode(),'chain':base64.b64encode(chain).decode()}
    # One issuance per role, no renewal/retry after an uncertain write.
    write_new(files,{name:canonical(public)})
    return public

def runtime_material(q,plan):
    # Invoked only by the UID1000 runtime-side wrapper, never by root CLI.
    key,csr=request(q,plan,'server')
    return {'plan.json':q.canonical(plan),'server.key':key,'server.csr':csr,'assertion.key':secrets.token_bytes(32)}

def accept_public(q,binding,files,plan,role,raw):
    require(role in ('server','client'),'CSR_ROLE_INVALID')
    require(files.parent==plan['backend_parent'],'RUNTIME_PARENT_MISMATCH')
    require(type(raw)is bytes and len(raw)<=LIMIT,'PUBLIC_RESPONSE_SIZE')
    value=json.loads(raw)
    require(type(value)is dict and set(value)=={'schema','role','plan_sha256','csr_sha256','ca','chain'}
        and canonical(value)==raw and value['schema']==1 and value['role']==role,'PUBLIC_RESPONSE_SHAPE')
    csr=files.read(files.parent+'/'+('server.csr' if role=='server' else 'client.csr'))
    require(value['plan_sha256']==sha(q.canonical(plan)) and value['csr_sha256']==sha(csr),'PUBLIC_RESPONSE_BINDING')
    ca=base64.b64decode(value['ca'],validate=True);chain=base64.b64decode(value['chain'],validate=True)
    if role=='server':binding.validate_material(chain,files.read(files.parent+'/server.key'),ca,'backend',plan['backend_address'])
    else:
        # Client key stays on PI5. Validate CSR/SPKI/chain locally, then the
        # accepted finish_ha verifies its own private-key pairing before use.
        certificate=binding.certificates(chain)[0];request_value=q.validate_request(plan,csr)
        require(certificate.public_key().public_numbers()==request_value.public_key().public_numbers(),'CLIENT_CSR_KEY_MISMATCH')
        certificate.verify_directly_issued_by(binding.certificates(ca)[0])
        x,*_=q.crypto()
        from cryptography.x509.oid import ExtendedKeyUsageOID
        require(list(certificate.extensions.get_extension_for_class(x.ExtendedKeyUsage).value)==[ExtendedKeyUsageOID.CLIENT_AUTH]
            and certificate.subject==request_value.subject
            and certificate.extensions.get_extension_for_class(x.SubjectAlternativeName).value==request_value.extensions.get_extension_for_class(x.SubjectAlternativeName).value,'CLIENT_LEAF_IDENTITY')
    try:existing=files.read(files.parent+'/ca.pem')
    except FileNotFoundError:existing=None
    require(existing is None or existing==ca,'CA_EXPORT_MISMATCH')
    values={'server-chain.pem' if role=='server' else 'client-chain.pem':chain}
    if existing is None:values={'ca.pem':ca,**values}
    write_new(files,values)

def finish_runtime(q,binding,files,plan):
    absent(files,('packet.json','ha-transfer.json'))
    ca=files.read(files.parent+'/ca.pem');chain=files.read(files.parent+'/client-chain.pem')
    assertion=files.read(files.parent+'/assertion.key');require(len(assertion)==32,'HMAC_LENGTH_INVALID')
    value=q.packet(plan,binding.spki(binding.certificates(chain)[0]),binding)
    bundle={'plan':plan,'packet':value,'ca':base64.b64encode(ca).decode(),
        'client_chain':base64.b64encode(chain).decode(),'assertion':base64.b64encode(assertion).decode()}
    q.stage(files,{'ha-transfer.json':q.canonical(bundle)},packet_value=value)
    with binding.TrustSide('backend',files,binding.native_packet(files,files.parent+'/packet.json')).context():pass
    return {'RESULT':'PASS_RUNTIME_DISABLED_TRUST_COMPLETION','activation':False,'STOP_REQUIRED':True}

def runtime_action(args):
    # No sudo of this user-controlled environment. Existing seal must still match.
    profile=load_profile();profile.target()
    require(Path(sys.prefix)==profile.ROOT/'venv','ACCEPTED_UID1000_VENV_REQUIRED')
    engine=profile.profile(profile.load_engine());engine.owned_directory(profile.ROOT,0o700)
    ready=profile.ROOT/'ready.json';info=ready.lstat()
    require(stat.S_ISREG(info.st_mode) and info.st_uid==info.st_gid==1000
        and info.st_nlink==1 and stat.S_IMODE(info.st_mode)==0o600,'USER_READY_SECURITY')
    require(json.loads(ready.read_bytes())=={'schema':1,'source_python':sha(Path('/usr/bin/python3').resolve().read_bytes()),
        'python_version':list(sys.version_info[:3]),'files':engine.fingerprint(profile.ROOT),'versions':engine.VERSIONS},'ACCEPTED_USER_ENVIRONMENT_DRIFT')
    q=helper(profile.ROOT);binding=q.native()
    if args.action=='runtime-prepare':
        require(args.runtime_parent is None,'RUNTIME_WIZARD_ONLY')
        plan=q.plan_wizard(profile.ROOT/'tools');values=runtime_material(q,plan)
        files,_=q.create_parent(binding,'backend',plan['private_name'])
        write_new(files,values)
        return {'RESULT':'PASS_RUNTIME_KEY_AND_CSR_PREPARATION','activation':False,'STOP_REQUIRED':True}
    files=binding.PrivateFiles(args.runtime_parent,(1000,1000));plan=q.read_plan(files)
    require(files.parent==plan['backend_parent'],'RUNTIME_PLAN_PARENT_MISMATCH')
    if args.action=='runtime-complete':return finish_runtime(q,binding,files,plan)
    require(not sys.stdin.isatty(),'CAPTURED_PUBLIC_SIGNER_PIPE_REQUIRED')
    role='server' if args.action=='import-server' else 'client'
    accept_public(q,binding,files,plan,role,sys.stdin.buffer.read(LIMIT+1).rstrip(b'\n'))
    return {'RESULT':'PASS_PUBLIC_CERTIFICATE_IMPORTED','role':role,'activation':False,'STOP_REQUIRED':True}

def main(argv=None):
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=('prepare','initialize-ca','issue-server','issue-client','runtime-prepare','import-server','import-client','runtime-complete'))
    parser.add_argument('--runtime-parent');args=parser.parse_args(argv)
    if args.action.startswith('runtime-') or args.action.startswith('import-'):
        return runtime_action(args)
    target()
    if args.action=='prepare':
        require(args.runtime_parent is None,'PREPARATION_HAS_NO_RUNTIME_INPUT');return prepare()
    profile=load_profile((ROOT/'tools/pe73_pi3_provision_environment.py').read_bytes())
    engine=engine_for(profile,offline=True);verify_ready(engine);q=helper();files=vault_files(q)
    require(type(args.runtime_parent)is str and args.runtime_parent.startswith('/home/jazofv1/hioc/'),'APPROVED_RUNTIME_PARENT_REQUIRED')
    # Read public plan/CSR only through existing UID1000 no-follow/owner/mode
    # checks; never read HMAC or server/client private material in the signer.
    runtime=q.native().PrivateFiles(args.runtime_parent,(1000,1000));plan=q.read_plan(runtime)
    require(runtime.parent==plan['backend_parent'],'RUNTIME_PLAN_PARENT_MISMATCH')
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter('error',getpass.GetPassWarning)
        password=getpass.getpass('Offline CA passphrase (not stored): ').encode()
    if args.action=='initialize-ca':return initialize_ca(q,files,plan,password)
    role='server' if args.action=='issue-server' else 'client'
    raw=runtime.read(runtime.parent+'/'+('server.csr' if role=='server' else 'client.csr'))
    # Public certificate response only, intended for a captured local pipe; no
    # CA key, runtime key, HMAC, plan/ACL contents or private errors in stdout.
    return sign_request(q,files,plan,password,role,raw)

if __name__=='__main__':
    try:
        receipt=main();status=0
    except BaseException as error:
        code=str(error) if type(error)is Blocked else 'CUSTODY_OR_IO_NOT_ESTABLISHED'
        receipt={'RESULT':'BLOCKED_SEPARATE_CA_CUSTODY','failure_code':code,
            'cleanup':'RETAINED_NO_AUTOMATIC_RETRY_OR_DELETE','STOP_REQUIRED':True};status=1
    print(json.dumps(receipt,sort_keys=True,separators=(',',':')))
    raise SystemExit(status)
