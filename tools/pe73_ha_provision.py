"""Finite PE-7.3 offline issuance/provisioning glue, never feature activation.

One immutable local plan and the existing NativePacket (written LAST) are the
provisioning boundaries. There is no second transaction journal/publisher. Partial
material is retained and any existing destination refuses a repeated attempt.
Secrets travel only through an existing strict-host-key authenticated SSH pipe,
never the public receipt. No CA service, global trust or Core package install.
"""
from __future__ import annotations
import argparse
import base64
import contextlib
import datetime as dt
import getpass
import hashlib
import importlib.util
import ipaddress
import json
import os
from pathlib import Path, PurePosixPath
import re
import secrets
import hmac
import shlex
import shutil
import socket
import ssl
import stat
import subprocess
import sys
import time
import uuid

BASE = '686be8841f461eacd57a9076948acf632bbf7bea'
PINS = {
 'pe73_ha_production':'86e4333ef2df1bf67b4621ccd6a3314f1322af00dafb42e9d3c5f0724e7bd23c',
 'pe73_ha_delivery':'3f7938ac351604ce27e70d60f3fd970964c2a8a3c0efae1449b8dbac46360be1',
 'pe73_ha_assess':'da4c97ef7e5acaf5840b9cbca03ee0cd888183e784a3f55bb8671b45b8372443',
 'pe73_ha_live_qualify':'ce4bbd30fdb268ec28637f990b85e9640d174a120eba971ed730f7ba94dfb845',
 'pe73_maintenance_window':'756eb3ad2c43047a60a43398afb4c34d165dad8729803099dc367da90f1bd741',
 'hioc-pe73-pi3-delivery':'76b422edc73ed87baba94fef6fcfa8e197a564d4d8f57c95dba6b8a1624907d2',
}
LIMIT=1048576
OPERATIONS={'get','create','update','result','availability_status'}
POPULATION_SCOPES=dict(get='eligible_or_existing',create='eligible_inventory',update='existing_assets',result='existing_assets',availability_status='existing_assets')

class Blocked(ValueError):pass
def require(value,code):
    if not value:raise Blocked(code)
def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode()
def sha(raw):return hashlib.sha256(raw).hexdigest()


def native():
    """Existing pinned local toolkit only; never download/execute an unpinned peer."""
    root=Path(__file__).parent
    for name,expected in PINS.items():
        raw=(root/(name+'.py')).read_bytes()
        require(len(raw)<=LIMIT and sha(raw)==expected,'TOOLKIT_IDENTITY_MISMATCH')
    spec=importlib.util.spec_from_file_location('pe73_provision_binding',root/'pe73_ha_production.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def crypto():
    try:
        from cryptography import x509
        from cryptography.hazmat.primitives import hashes,serialization
        from cryptography.hazmat.primitives.asymmetric import ec
        from cryptography.x509.oid import ExtendedKeyUsageOID,NameOID
    except ImportError:raise Blocked('NATIVE_CRYPTOGRAPHY_UNAVAILABLE') from None
    require(callable(getattr(x509,'load_pem_x509_certificates',None)) and hasattr(x509.Certificate,'not_valid_after_utc')
        and hasattr(x509.Certificate,'verify_directly_issued_by'),'CRYPTOGRAPHY_API_UNAVAILABLE')
    return x509,hashes,serialization,ec,ExtendedKeyUsageOID,NameOID


def probe_pi5():
    """Read-only runtime/transfer feasibility, not repeated filesystem qualification."""
    require(sys.platform=='linux' and os.getuid()==os.geteuid()==os.getgid()==os.getegid()==0,'PI5_TERMINAL_ROOT_REQUIRED')
    result={'target':'PI5_HA','terminal_python':list(sys.version_info[:3]),
        'machine':__import__('platform').machine(),'openssl_library':ssl.OPENSSL_VERSION,
        'cryptography_available':False,'cryptography_version':None,
        'ssh_available':bool(shutil.which('ssh')),'scp_available':bool(shutil.which('scp')),
        'known_PI3_host_key':False,'core_crypto_probe':'NOT_OBSERVED',
        'mutations_performed':False,'credentials_read':False,'production_ready':False,
        'PE73':'IN_PROGRESS','PE74':'NOT_AUTHORIZED','STOP_REQUIRED':True}
    try:
        import cryptography
        crypto()
        result.update(cryptography_available=True,cryptography_version=cryptography.__version__)
    except (ImportError,Blocked):pass
    keygen=shutil.which('ssh-keygen');known=Path.home()/'.ssh/known_hosts'
    if keygen and known.is_file() and not known.is_symlink():
        value=subprocess.run([keygen,'-F','192.168.100.252','-f',str(known)],stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,timeout=10)
        require(len(value.stdout)<=65536,'PUBLIC_HOST_KEY_RESULT_LIMIT')
        result['known_PI3_host_key']=value.returncode==0 and bool(value.stdout)
    docker='/usr/local/bin/docker'
    if Path(docker).is_file():
        prefix=[docker,'--config','/proc/pe73-no-client-config','--host','unix:///var/run/docker.sock']
        listing=subprocess.run(prefix+['container','ls','--filter','label=io.hass.type=core','--format','{{.ID}}'],
            stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,timeout=15)
        ids=listing.stdout.decode('ascii').split()
        if listing.returncode==0 and len(ids)==1 and re.fullmatch('[0-9a-f]{12,64}',ids[0]):
            # Existing Core interpreter, import-only fixed helper, bytecode disabled.
            # No HA import, source/config read, network, write or package install.
            code="import json,sys,os; import cryptography; print(json.dumps({'python':list(sys.version_info[:3]),'crypto':cryptography.__version__,'uid':os.getuid(),'gid':os.getgid()}))"
            value=subprocess.run(prefix+['container','exec','--workdir','/',ids[0],'/usr/local/bin/python3','-I','-B','-c',code],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,timeout=15)
            if value.returncode==0 and len(value.stdout)<=4096:
                record=json.loads(value.stdout)
                require(set(record)=={'python','crypto','uid','gid'},'CORE_CRYPTO_RESULT_INVALID')
                result['core_crypto_probe']=record
            else:result['core_crypto_probe']='UNAVAILABLE'
    result['RESULT']='PASS_READ_ONLY_PROVISIONING_RUNTIME_ASSESSMENT' if result['cryptography_available'] else 'BLOCKED_TERMINAL_CRYPTOGRAPHY_UNAVAILABLE'
    return result


def validate_plan(plan):
    fields={'backend_address','ha_address','backend_port','guard_port','private_name','ha_parent',
        'backend_parent','ca_name','server_name','client_name','valid_days','issuer','key_id',
        'actors','frontend_origin','reference','toolkit','helper_sha256'}
    require(type(plan)is dict and set(plan)==fields,'PROVISION_PLAN_SHAPE')
    require(plan['backend_address']=='192.168.100.252' and plan['ha_address']=='192.168.100.251','ESTABLISHED_LAN_IDENTITY_REQUIRED')
    for k in ('backend_address','ha_address'):
        address=ipaddress.ip_address(plan[k]);require(address.is_private and not address.is_loopback,'PRIVATE_INTERFACE_REQUIRED')
    require(all(type(plan[k])is int and 1024<=plan[k]<=65535 for k in ('backend_port','guard_port'))
        and plan['backend_port']!=plan['guard_port'],'EXPLICIT_DISTINCT_PRIVATE_PORTS_REQUIRED')
    require(type(plan['private_name'])is str and re.fullmatch('[A-Za-z][A-Za-z0-9_-]{0,63}',plan['private_name']), 'PRIVATE_BASENAME_INVALID')
    require(plan['backend_parent']=='/home/jazofv1/hioc/'+plan['private_name'] and plan['ha_parent']=='/config/'+plan['private_name'],'PRIVATE_PARENT_SCOPE')
    require(type(plan['valid_days'])is int and 1<=plan['valid_days']<=3650,'EXPLICIT_CERTIFICATE_VALIDITY_REQUIRED')
    for k in ('ca_name','server_name','client_name'):
        require(type(plan[k])is str and 1<=len(plan[k])<=64 and all(32<=ord(c)<127 for c in plan[k]),'EXPLICIT_CERTIFICATE_SUBJECT_REQUIRED')
    require(type(plan['issuer'])is str and uuid.UUID(hex=plan['issuer']).version==4 and uuid.UUID(hex=plan['issuer']).hex==plan['issuer'],'ISSUER_INVALID')
    require(type(plan['key_id'])is str and re.fullmatch('[A-Za-z0-9_-]{1,64}',plan['key_id']),'KEY_ID_INVALID')
    require(type(plan['actors'])is dict and 1<=len(plan['actors'])<=16,'INDEPENDENT_ACTOR_SCOPE_REQUIRED')
    for actor,operations in plan['actors'].items():
        require(type(actor)is str and re.fullmatch('[A-Za-z0-9_-]{1,128}',actor) and type(operations)is dict and bool(operations)
            and set(operations)<=OPERATIONS,'ACTOR_OPERATION_INVALID')
        for operation,ids in operations.items():
            if type(ids)is dict:
                require(set(ids)=={'scope','amendment','acceptance_reference'} and ids['scope']==POPULATION_SCOPES[operation] and ids['amendment']=='PE73_FULL_INVENTORY_ASSET_AUTHORIZATION_V1'
                    and (ids['acceptance_reference'] is None or type(ids['acceptance_reference'])is str
                    and re.fullmatch('[A-Za-z0-9_-]{1,128}',ids['acceptance_reference'])),'POPULATION_GRANT_INVALID')
                continue
            require(type(ids)is list and 1<=len(ids)<=256 and len(ids)==len(set(ids))
                and all(type(x)is str and re.fullmatch('dev_[0-9a-f]{16}',x) for x in ids),'EXACT_ASSET_SCOPE_REQUIRED')
    from urllib.parse import urlsplit
    url=urlsplit(plan['frontend_origin'])
    require(url.scheme=='https' and url.hostname and not url.username and not url.password
        and url.path in ('','/') and not url.query and not url.fragment,'APPROVED_EXISTING_HTTPS_FRONTEND_REQUIRED')
    require(re.fullmatch('[A-Za-z0-9_-]{8,96}',plan['reference']) and re.fullmatch('[0-9a-f]{64}',plan['helper_sha256']), 'PROVISION_REFERENCE_INVALID')
    require(type(plan['toolkit'])is str and PurePosixPath(plan['toolkit']).is_absolute() and '..' not in PurePosixPath(plan['toolkit']).parts,'TOOLKIT_PATH_INVALID')
    return plan


def generate_ca(plan,password):
    validate_plan(plan);require(type(password)is bytes and len(password)>=16,'OFFLINE_CA_PASSPHRASE_MINIMUM_16_BYTES')
    x,h,s,ec,_,oid=crypto();now=dt.datetime.now(dt.timezone.utc)
    key=ec.generate_private_key(ec.SECP256R1());name=x.Name([x.NameAttribute(oid.COMMON_NAME,plan['ca_name'])])
    ca=(x.CertificateBuilder().subject_name(name).issuer_name(name).public_key(key.public_key())
        .serial_number(x.random_serial_number()).not_valid_before(now-dt.timedelta(minutes=1))
        .not_valid_after(now+dt.timedelta(days=plan['valid_days']))
        .add_extension(x.BasicConstraints(ca=True,path_length=0),True)
        .add_extension(x.SubjectKeyIdentifier.from_public_key(key.public_key()),False)
        .add_extension(x.AuthorityKeyIdentifier.from_issuer_public_key(key.public_key()),False)
        .add_extension(x.KeyUsage(False,False,False,False,False,True,True,False,False),True).sign(key,h.SHA256()))
    return ca.public_bytes(s.Encoding.PEM),key.private_bytes(s.Encoding.PEM,s.PrivateFormat.PKCS8,s.BestAvailableEncryption(password))


def create_request(plan):
    validate_plan(plan);x,h,s,ec,_,oid=crypto()
    key=ec.generate_private_key(ec.SECP256R1())
    request=(x.CertificateSigningRequestBuilder().subject_name(x.Name([x.NameAttribute(oid.COMMON_NAME,plan['client_name'])]))
        .add_extension(x.SubjectAlternativeName([x.IPAddress(ipaddress.ip_address(plan['ha_address']))]),False).sign(key,h.SHA256()))
    return key.private_bytes(s.Encoding.PEM,s.PrivateFormat.PKCS8,s.NoEncryption()),request.public_bytes(s.Encoding.PEM)


def validate_request(plan,raw):
    validate_plan(plan);x,_,_,ec,_,oid=crypto()
    require(type(raw)is bytes and len(raw)<=16384,'CSR_SIZE_INVALID')
    csr=x.load_pem_x509_csr(raw)
    require(csr.is_signature_valid and csr.subject==x.Name([x.NameAttribute(oid.COMMON_NAME,plan['client_name'])]),'CLIENT_REQUEST_SIGNATURE_OR_SUBJECT')
    public=csr.public_key()
    require(isinstance(public,ec.EllipticCurvePublicKey) and public.curve.name=='secp256r1','CLIENT_REQUEST_KEY_TYPE')
    names=csr.extensions.get_extension_for_class(x.SubjectAlternativeName).value
    require(list(names)==[x.IPAddress(ipaddress.ip_address(plan['ha_address']))] and len(csr.extensions)==1,'CLIENT_REQUEST_SAN_INVALID')
    return csr


def issue(plan,ca_raw,ca_key_raw,password,*,csr_raw=None):
    validate_plan(plan);x,h,s,ec,eku,oid=crypto();now=dt.datetime.now(dt.timezone.utc)
    ca=x.load_pem_x509_certificate(ca_raw);ca_key=s.load_pem_private_key(ca_key_raw,password=password)
    require(ca_key.public_key().public_numbers()==ca.public_key().public_numbers(),'CA_KEY_MISMATCH')
    require(ca.subject==x.Name([x.NameAttribute(oid.COMMON_NAME,plan['ca_name'])]),'CA_IDENTITY_MISMATCH')
    ca.verify_directly_issued_by(ca)
    require(ca.not_valid_before_utc<=now<ca.not_valid_after_utc and ca.extensions.get_extension_for_class(x.BasicConstraints).value.ca,'CA_EXPIRED_OR_INVALID')
    if csr_raw is None:
        key=ec.generate_private_key(ec.SECP256R1());public=key.public_key();role='server'
        subject=x.Name([x.NameAttribute(oid.COMMON_NAME,plan['server_name'])])
    else:
        csr=validate_request(plan,csr_raw);public=csr.public_key()
        key=None;subject=csr.subject;role='client'
    cert=(x.CertificateBuilder().subject_name(subject).issuer_name(ca.subject).public_key(public)
        .serial_number(x.random_serial_number()).not_valid_before(now-dt.timedelta(minutes=1))
        .not_valid_after(min(now+dt.timedelta(days=plan['valid_days']),ca.not_valid_after_utc))
        .add_extension(x.BasicConstraints(ca=False,path_length=None),True)
        .add_extension(x.KeyUsage(True,False,False,False,False,False,False,False,False),True)
        .add_extension(x.SubjectKeyIdentifier.from_public_key(public),False)
        .add_extension(x.AuthorityKeyIdentifier.from_issuer_public_key(ca.public_key()),False)
        .add_extension(x.SubjectAlternativeName([x.IPAddress(ipaddress.ip_address(plan['backend_address' if role=='server' else 'ha_address']))]),False)
        .add_extension(x.ExtendedKeyUsage([eku.SERVER_AUTH if role=='server' else eku.CLIENT_AUTH]),False)
        .sign(ca_key,h.SHA256()))
    cert.verify_directly_issued_by(ca)
    return cert.public_bytes(s.Encoding.PEM)+ca_raw, None if key is None else key.private_bytes(s.Encoding.PEM,s.PrivateFormat.PKCS8,s.NoEncryption())


def packet(plan,pin,binding):
    validate_plan(plan);a,b=plan['ha_parent'],plan['backend_parent']
    ha=dict(enabled=False,issuer=plan['issuer'],key_id=plan['key_id'],assertion_key_file=a+'/assertion.key',
        client_certificate=a+'/client-chain.pem',client_key=a+'/client.key',server_ca=a+'/ca.pem',
        server_url='https://'+plan['backend_address']+':'+str(plan['backend_port']),
        operator_allowlist=list(plan['actors']),request_timeout_seconds=10)
    backend=dict(enabled=False,bind_address=plan['backend_address'],port=plan['backend_port'],ha_address=plan['ha_address'],
        server_certificate=b+'/server-chain.pem',server_key=b+'/server.key',client_ca=b+'/ca.pem',
        issuer_trusts=[dict(enabled=False,issuer=plan['issuer'],key_id=plan['key_id'],assertion_key_file=b+'/assertion.key',
            client_spki_sha256=pin,actors=plan['actors'])])
    return binding.d.disabled_trust(ha,backend)


def read_plan(files):
    raw=files.read(files.parent+'/plan.json');value=json.loads(raw)
    require(canonical(value)==raw,'PLAN_CANONICAL_REQUIRED');return validate_plan(value)


def backend_material(plan,password):
    """Pure generation only; no secret output, file IO or service. CA is encrypted."""
    ca,encrypted=generate_ca(plan,password)
    server,key=issue(plan,ca,encrypted,password)
    return {'ca.pem':ca,'ca-offline.key':encrypted,'server-chain.pem':server,'server.key':key,'assertion.key':secrets.token_bytes(32)}


def stage(files,values,*,packet_value=None):
    """Reuse exclusive durable provision(), retaining partial files on uncertainty."""
    allowed={'plan.json','ca.pem','ca-offline.key','server-chain.pem','server.key','assertion.key',
        'client.key','client.csr','client-chain.pem','ha-transfer.json'}
    require(type(values)is dict and bool(values) and set(values)<=allowed,'PROVISION_FILE_SCOPE')
    for name in [*values,*(['packet.json'] if packet_value is not None else [])]:
        try:files.read(files.parent+'/'+name)
        except FileNotFoundError:pass
        else:raise Blocked('EXISTING_PROVISION_DESTINATION_REFUSED')
    for name,raw in values.items():files.provision(files.parent+'/'+name,raw)
    if packet_value is not None:files.provision(files.parent+'/packet.json',canonical(packet_value))


def finish_backend(files,password,binding):
    plan=read_plan(files)
    require(files.parent==plan['backend_parent'],'BACKEND_PRIVATE_PARENT_MISMATCH')
    # No rewrite/retry: check completion BEFORE doing cryptographic work.
    try:files.read(files.parent+'/packet.json')
    except FileNotFoundError:pass
    else:raise Blocked('EXISTING_COMPLETION_REFUSED')
    chain,_=issue(plan,files.read(files.parent+'/ca.pem'),files.read(files.parent+'/ca-offline.key'),password,
        csr_raw=files.read(files.parent+'/client.csr'))
    leaf=binding.certificates(chain)[0];value=packet(plan,binding.spki(leaf),binding)
    bundle={'plan':plan,'packet':value,'ca':base64.b64encode(files.read(files.parent+'/ca.pem')).decode(),
        'client_chain':base64.b64encode(chain).decode(),'assertion':base64.b64encode(files.read(files.parent+'/assertion.key')).decode()}
    require(len(base64.b64decode(bundle['assertion']))==32,'HMAC_LENGTH_INVALID')
    stage(files,{'client-chain.pem':chain,'ha-transfer.json':canonical(bundle)},packet_value=value)
    trust=binding.TrustSide('backend',files,binding.native_packet(files,files.parent+'/packet.json'))
    with trust.context():pass
    return {'RESULT':'PASS_BACKEND_OFFLINE_ISSUANCE','activation':False,'STOP_REQUIRED':True}


def finish_ha(files,bundle_raw,binding,core_root):
    require(type(bundle_raw)is bytes and len(bundle_raw)<=LIMIT,'PRIVATE_TRANSFER_SIZE')
    bundle=json.loads(bundle_raw)
    require(type(bundle)is dict and set(bundle)=={'plan','packet','ca','client_chain','assertion'} and canonical(bundle)==bundle_raw,'PRIVATE_TRANSFER_SHAPE')
    plan=read_plan(files);require(bundle['plan']==plan,'INDEPENDENT_PLAN_MISMATCH')
    require(files.parent==core_root+plan['ha_parent'][len('/config'):],'HA_PRIVATE_PARENT_MISMATCH')
    ca=base64.b64decode(bundle['ca'],validate=True);chain=base64.b64decode(bundle['client_chain'],validate=True)
    key=base64.b64decode(bundle['assertion'],validate=True);require(len(key)==32,'HMAC_LENGTH_INVALID')
    pin=binding.validate_material(chain,files.read(files.parent+'/client.key'),ca,'ha',plan['backend_address'])
    require(bundle['packet']==packet(plan,pin,binding),'CLIENT_SPKI_OR_INDEPENDENT_ACL_MISMATCH')
    stage(files,{'ca.pem':ca,'client-chain.pem':chain,'assertion.key':key},packet_value=bundle['packet'])
    require(hmac.compare_digest(files.read(files.parent+'/assertion.key'),key),'AUTHENTICATED_TRANSFER_KEY_MISMATCH')
    trust=binding.TrustSide('ha',files,binding.native_packet(files,files.parent+'/packet.json'),core_root=core_root)
    with trust.context():pass
    return {'RESULT':'PASS_HA_DISABLED_TRUST_PROVISIONING','activation':False,'cross_host_live_validation':'REQUIRED', 'STOP_REQUIRED':True}


def export_bundle(files,binding):
    """Fresh backend read, not a stale exported key treated as current evidence."""
    plan=read_plan(files);raw=files.read(files.parent+'/ha-transfer.json');value=json.loads(raw)
    require(canonical(value)==raw and value['plan']==plan,'TRANSFER_PLAN_DRIFT')
    current=binding.native_packet(files,files.parent+'/packet.json')()
    require(value['packet']==current and base64.b64decode(value['ca'],validate=True)==files.read(files.parent+'/ca.pem')
        and base64.b64decode(value['client_chain'],validate=True)==files.read(files.parent+'/client-chain.pem'), 'TRANSFER_CERTIFICATE_OR_ACL_DRIFT')
    require(hmac.compare_digest(base64.b64decode(value['assertion'],validate=True),files.read(files.parent+'/assertion.key')),'CURRENT_BACKEND_HMAC_MISMATCH')
    trust=binding.TrustSide('backend',files,binding.native_packet(files,files.parent+'/packet.json'))
    with trust.context():pass
    return raw


def create_parent(binding,role,name):
    """One new approved direct child; existing secure descriptor code is reused."""
    require(re.fullmatch('[A-Za-z][A-Za-z0-9_-]{0,63}',name),'PRIVATE_BASENAME_INVALID')
    require(role in ('backend','ha'),'PROVISION_ROLE_INVALID')
    if role=='backend':
        provider=binding.sibling('pe73_maintenance_window');provider.NativeOps().target_boot()
        filesystem=binding.sibling('hioc-pe73-pi3-delivery').NativeFS();owner=(1000,1000)
        context=filesystem.directory();root='/home/jazofv1/hioc'
    else:
        filesystem=binding.d.native_filesystem();owner=filesystem._core
        context=filesystem._directory('');root=filesystem._root
    with context as parent:
        # mkdir EEXIST is terminal. No chmod/chown of existing objects.
        os.mkdir(name,0o700,dir_fd=parent);os.fsync(parent)
        before=os.stat(name,dir_fd=parent,follow_symlinks=False)
        fd=os.open(name,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC,dir_fd=parent)
        try:
            require((before.st_dev,before.st_ino)==(os.fstat(fd).st_dev,os.fstat(fd).st_ino),'NEW_PRIVATE_DIRECTORY_DRIFT')
            if (os.fstat(fd).st_uid,os.fstat(fd).st_gid)!=owner:os.fchown(fd,*owner)
            os.fchmod(fd,0o700);os.fsync(fd)
            require(binding.d._anchor(os.fstat(fd))==binding.d._anchor(os.stat(name,dir_fd=parent,follow_symlinks=False)),'NEW_PRIVATE_DIRECTORY_DRIFT')
        finally:os.close(fd)
        os.fsync(parent)
    files=binding.PrivateFiles(root+'/'+name,owner)
    with files.directory():pass
    return files,root


def ssh(binding,toolkit,helper_sha,parent,ssh_port,operation,payload=b''):
    """Existing OpenSSH only; strict existing host keys, no passwords/forwards/retry.

    Private stdout is captured as bytes, NEVER printed or returned in a receipt.
    The peer helper verifies its exact source bytes before execution. No service.
    """
    require(operation in ('plan','request','bundle') and type(ssh_port)is int and 1<=ssh_port<=65535,'TRANSFER_OPERATION_INVALID')
    require(re.fullmatch('[0-9a-f]{64}',helper_sha) and PurePosixPath(toolkit).is_absolute()
        and '..' not in PurePosixPath(toolkit).parts and re.fullmatch('/home/jazofv1/hioc/[A-Za-z][A-Za-z0-9_-]{0,63}',parent),'TRANSFER_SCOPE')
    binary=shutil.which('ssh');require(binary,'EXISTING_OPENSSH_CLIENT_REQUIRED')
    require(len(payload)<=LIMIT,'PRIVATE_TRANSFER_SIZE')
    wrapper="import hashlib,sys; p=sys.argv[1]; r=open(p,'rb').read(1048577); assert len(r)<=1048576 and hashlib.sha256(r).hexdigest()==sys.argv[2]; sys.argv=[p,'_pipe',*sys.argv[3:]]; exec(compile(r,p,'exec'),{'__name__':'__main__','__file__':p})"
    command=shlex.join(['/usr/bin/python3','-I','-B','-c',wrapper,toolkit+'/pe73_ha_provision.py',helper_sha,operation,parent])
    result=subprocess.run([binary,'-T','-o','StrictHostKeyChecking=yes','-o','BatchMode=yes','-o','ClearAllForwardings=yes',
        '-o','RequestTTY=no','-o','LogLevel=ERROR','-o','ConnectTimeout=10','-p',str(ssh_port),'jazofv1@192.168.100.252',command],
        input=payload,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30)
    require(result.returncode==0 and len(result.stdout)<=LIMIT,'AUTHENTICATED_PRIVATE_TRANSFER_BLOCKED')
    return result.stdout


def policy_input(label):
    with open('/dev/tty','r+',encoding='utf-8') as terminal:
        require(terminal.isatty(),'CONTROLLING_TERMINAL_REQUIRED')
        terminal.write(label+': ');terminal.flush();answer=terminal.readline(4097)
    require(bool(answer) and len(answer)<=4096 and bool(answer.strip()),'EXPLICIT_POLICY_INPUT_REQUIRED')
    return answer.strip()

def operator_values(action):
    """No hashes, operation IDs, JSON editing or approval challenges to copy."""
    name=policy_input('Previously approved private directory basename')
    require(re.fullmatch('[A-Za-z][A-Za-z0-9_-]{0,63}',name),'PRIVATE_BASENAME_INVALID')
    if action=='backend-issue':return ['/home/jazofv1/hioc/'+name]
    port=policy_input('Existing approved PI3 SSH port')
    require(port.isdecimal() and 1<=int(port)<=65535,'SSH_PORT_INVALID')
    if action=='ha-request':return ['/home/jazofv1/.hioc-pe73-provision-toolkit',sha(Path(__file__).read_bytes()),'/home/jazofv1/hioc/'+name,port]
    require(action=='ha-complete','OPERATOR_ACTION_INVALID')
    # Root discovery is read-only; identity is independently repeated by main().
    fs=native().d.native_filesystem()
    return [fs._root+'/'+name,port]


def plan_wizard(toolkit):
    """Policy inputs, not consequential-operation approval prompts. No defaults."""
    print('Create dedicated offline PE-7 CA; generate new issuer UUID/key ID; all roles stay disabled.',file=sys.stderr)
    ask=policy_input
    private=ask('New private directory basename (both hosts)')
    actors={}
    actor=getpass.getpass('Approved human HA operator ID (not printed): ').strip()
    operations=getpass.getpass('Approved comma-separated operations (get/create/update/result/availability_status): ').strip().split(',')
    mode=getpass.getpass('Authorization mode (exact/population): ').strip()
    require(mode in ('exact','population'),'EXPLICIT_AUTHORIZATION_MODE_REQUIRED')
    if mode=='exact':
        ids=getpass.getpass('Approved comma-separated exact existing dev_ Asset IDs: ').strip().split(',')
        actors[actor]={x.strip():[i.strip() for i in ids] for x in operations}
    else:
        reference=getpass.getpass('Owner acceptance reference for full-inventory amendment (blank keeps inactive/unapproved): ').strip() or None
        require(all(x.strip() in POPULATION_SCOPES for x in operations),'ACTOR_OPERATION_INVALID')
        actors[actor]={x.strip():{'scope':POPULATION_SCOPES[x.strip()],'amendment':'PE73_FULL_INVENTORY_ASSET_AUTHORIZATION_V1','acceptance_reference':reference} for x in operations}
    issuer=uuid.uuid4().hex
    plan={'backend_address':ask('Approved PI3 private bind IPv4'),'ha_address':ask('Approved HA source IPv4'),
        'backend_port':int(ask('Reserved disabled application port')),'guard_port':int(ask('Temporary observer port')),
        'private_name':private,'ha_parent':'/config/'+private,'backend_parent':'/home/jazofv1/hioc/'+private,
        'ca_name':ask('Offline CA subject label'),'server_name':ask('Server certificate subject label'),
        'client_name':ask('HA client certificate subject label'),'valid_days':int(ask('Certificate validity days')),
        'issuer':issuer,'key_id':'pe73_'+secrets.token_hex(8),'actors':actors,
        'frontend_origin':ask('Existing approved HTTPS HA frontend origin'),
        'reference':'PE73_PROVISION_'+issuer,'toolkit':str(toolkit),
        'helper_sha256':sha(Path(__file__).read_bytes())}
    return validate_plan(plan)


def main(argv=None):
    parser=argparse.ArgumentParser(description='PE-7.3 bounded disabled trust provisioning')
    parser.add_argument('action',choices=['probe-pi5','backend-init','ha-request','backend-issue','ha-complete','_pipe'])
    parser.add_argument('values',nargs='*');args=parser.parse_args(argv)
    if args.action=='probe-pi5':return probe_pi5()
    crypto()  # Before private reads, transfer or mutation on either target.
    binding=native()
    if not args.values and args.action in ('ha-request','backend-issue','ha-complete'):
        args.values=operator_values(args.action)
    if args.action=='_pipe':
        require(not sys.stdout.isatty() and len(args.values)==2,'PRIVATE_PIPE_ONLY')
        operation,parent=args.values
        require(operation in ('plan','request','bundle') and re.fullmatch('/home/jazofv1/hioc/[A-Za-z][A-Za-z0-9_-]{0,63}',parent),'PRIVATE_PIPE_SCOPE')
        binding.sibling('pe73_maintenance_window').NativeOps().target_boot()
        files=binding.PrivateFiles(parent,(1000,1000));read_plan(files)
        if operation=='request':
            raw=sys.stdin.buffer.read(16385);require(len(raw)<=16384,'CSR_SIZE_INVALID')
            validate_request(read_plan(files),raw)
            files.provision(parent+'/client.csr',raw);return {'RESULT':'PASS_PUBLIC_REQUEST_IMPORTED','STOP_REQUIRED':True}
        raw=files.read(parent+'/plan.json') if operation=='plan' else export_bundle(files,binding)
        require(len(raw)<=LIMIT,'PRIVATE_TRANSFER_SIZE');sys.stdout.buffer.write(raw);sys.stdout.buffer.flush()
        return None
    if args.action=='backend-init':
        require(not args.values,'NO_UNEXPECTED_ARGUMENTS');crypto()
        plan=plan_wizard(Path(__file__).parent)
        password=getpass.getpass('New offline CA passphrase (at least16 bytes; keep offline): ').encode()
        require(len(password)>=16,'OFFLINE_CA_PASSPHRASE_MINIMUM_16_BYTES')
        values=backend_material(plan,password);password=None
        files,_=create_parent(binding,'backend',plan['private_name'])
        stage(files,{'plan.json':canonical(plan),**values})
        return {'RESULT':'PASS_BACKEND_OFFLINE_CA_PREPARATION','private_parent':files.parent,
            'toolkit':str(Path(__file__).parent),'issuer':plan['issuer'],'key_id':plan['key_id'],'activation':False,'STOP_REQUIRED':True}
    if args.action=='ha-request':
        require(len(args.values)==4,'PEER_TOOLKIT_HASH_PARENT_SSH_PORT_REQUIRED')
        toolkit,expected,parent,port=args.values
        raw=ssh(binding,toolkit,expected,parent,int(port),'plan');plan=json.loads(raw)
        require(canonical(plan)==raw,'PLAN_CANONICAL_REQUIRED');validate_plan(plan)
        require(plan['helper_sha256']==sha(Path(__file__).read_bytes()) and plan['toolkit']==toolkit,'PEER_TOOLKIT_MISMATCH')
        key,request=create_request(plan)
        files,_=create_parent(binding,'ha',plan['private_name'])
        stage(files,{'plan.json':raw,'client.key':key,'client.csr':request})
        result=json.loads(ssh(binding,toolkit,expected,parent,int(port),'request',request))
        require(result.get('RESULT')=='PASS_PUBLIC_REQUEST_IMPORTED','CSR_TRANSFER_UNCERTAIN')
        return {'RESULT':'PASS_HA_LOCAL_KEY_AND_PUBLIC_REQUEST','private_parent':files.parent,'activation':False,'STOP_REQUIRED':True}
    require(len(args.values) in (1,2),'PRIVATE_PARENT_REQUIRED')
    parent=args.values[0]
    if args.action=='backend-issue':
        require(re.fullmatch('/home/jazofv1/hioc/[A-Za-z][A-Za-z0-9_-]{0,63}',parent),'APPROVED_BACKEND_PRIVATE_PARENT_REQUIRED')
        binding.sibling('pe73_maintenance_window').NativeOps().target_boot()
        files=binding.PrivateFiles(parent,(1000,1000))
    else:
        fs=binding.d.native_filesystem()
        require(parent.startswith(fs._root+'/') and '/' not in parent[len(fs._root)+1:],'APPROVED_HA_PRIVATE_PARENT_REQUIRED')
        files=binding.PrivateFiles(parent,fs._core)
    plan=read_plan(files)
    if args.action=='backend-issue':
        password=getpass.getpass('Unlock offline CA for this issuance (not stored): ').encode()
        return finish_backend(files,password,binding)
    if args.action=='ha-complete':
        require(len(args.values)==2,'EXPLICIT_EXISTING_SSH_PORT_REQUIRED')
        raw=ssh(binding,plan['toolkit'],plan['helper_sha256'],plan['backend_parent'],int(args.values[1]),'bundle')
        return finish_ha(files,raw,binding,fs._root)
    raise Blocked('UNSUPPORTED_PROVISIONING_ACTION')



if __name__=='__main__':
    try:
        result=main()
    except BaseException:
        result={'RESULT':'BLOCKED_PROVISIONING','failure_code':'INPUT_DEPENDENCY_SECURITY_OR_PARTIAL_STATE_NOT_ESTABLISHED',
            'partial_material':'RETAINED_IF_CREATED','automatic_retry':False,'activation':False,'STOP_REQUIRED':True}
    if result is not None:
        print(json.dumps(result,sort_keys=True,separators=(',',':')))
        raise SystemExit(0 if result['RESULT'].startswith('PASS_') else 1)
