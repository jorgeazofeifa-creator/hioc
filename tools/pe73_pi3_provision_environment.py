"""PI3 UID1000 profile of the accepted isolated dependency engine, setup only.

Never invokes provisioning actions, persists test keys, or changes the PI5 engine.
No production CA/HMAC material belongs in this dependency cache or runtime tree.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import stat
import sys
import types
import urllib.request

ROOT=Path('/home/jazofv1/.hioc-pe73-provision-environment')
ENGINE_SOURCE={'size': 16959, 'sha256': '0e5d41b05729907ad1e629c8d77bf57a25890f600f7e2fcf29071c106fa0b3d7', 'url': 'https://raw.githubusercontent.com/jorgeazofeifa-creator/hioc/513d511fe255e11a875145543f62fa5dca2169a1/tools/pe73_provision_environment.py'}
WHEELS=[{'name': 'cryptography-50.0.2-cp311-abi3-manylinux2014_aarch64.manylinux_2_17_aarch64.whl', 'size': 4731146, 'sha256': '79def8d059362e7831389ed3be0ecdf58a89386e1271e35dd9f5af84e81bffd0', 'url': 'https://files.pythonhosted.org/packages/d9/69/c9bd862c3bf43d6399c433caf002df16e2dffd4be49bdf515cda38038711/cryptography-50.0.2-cp311-abi3-manylinux2014_aarch64.manylinux_2_17_aarch64.whl'}, {'name': 'cryptography-50.0.2-cp311-abi3-musllinux_1_2_aarch64.whl', 'size': 4870819, 'sha256': '25784ce8b9621c90c643efb9e1e2162ab3b0224cae446ad5e70e7fcb1ce18b51', 'url': 'https://files.pythonhosted.org/packages/6c/5d/906970b83bbfc1f5bbfb677a143c181f2801f23b6a7204a3b47c42c97e65/cryptography-50.0.2-cp311-abi3-musllinux_1_2_aarch64.whl'}, {'name': 'pycparser-2.23-py3-none-any.whl', 'size': 118140, 'sha256': 'e5c6e8d3fbad53479cab09ac03729e0a9faf2bee3db8208a550daf5af81a5934', 'url': 'https://files.pythonhosted.org/packages/a0/e3/59cd50310fc9b59512193629e1984c1f95e5c8ae6e5d8c69532ccc65a7fe/pycparser-2.23-py3-none-any.whl'}, {'name': 'pip-25.3-py3-none-any.whl', 'size': 1778622, 'sha256': '9655943313a94722b7774661c21049070f6bbb0a1516bf02f7c8d5d9201514cd', 'url': 'https://files.pythonhosted.org/packages/44/3c/d717024885424591d5376220b5e836c2d5293ce2011523c9de23ff7bf068/pip-25.3-py3-none-any.whl'}, {'name': 'cffi-2.0.0-cp311-cp311-manylinux2014_aarch64.manylinux_2_17_aarch64.whl', 'size': 216476, 'sha256': '730cacb21e1bdff3ce90babf007d0a0917cc3e6492f336c2f0134101e0944f93', 'url': 'https://files.pythonhosted.org/packages/b8/56/6033f5e86e8cc9bb629f0077ba71679508bdf54a9a5e112a3c0b91870332/cffi-2.0.0-cp311-cp311-manylinux2014_aarch64.manylinux_2_17_aarch64.whl'}, {'name': 'cffi-2.0.0-cp311-cp311-musllinux_1_2_aarch64.whl', 'size': 218971, 'sha256': 'a05d0c237b3349096d3981b727493e22147f934b20f6f125a3eba8f994bec4a9', 'url': 'https://files.pythonhosted.org/packages/44/64/58f6255b62b101093d5df22dcb752596066c7e89dd725e0afaed242a61be/cffi-2.0.0-cp311-cp311-musllinux_1_2_aarch64.whl'}]

class Blocked(ValueError):pass
def require(value,code):
    if not value:raise Blocked(code)
def sha(raw):return hashlib.sha256(raw).hexdigest()

def target():
    require(sys.platform=='linux' and platform.python_implementation()=='CPython'
        and sys.version_info[:2]==(3,11) and platform.machine()=='aarch64'
        and platform.node()=='nutandpihole','PI3_HOST_OR_ABI_MISMATCH')
    require(os.getuid()==os.geteuid()==os.getgid()==os.getegid()==1000,'PI3_UID_GID1000_REQUIRED_NO_ROOT')
    import pwd
    account=pwd.getpwuid(1000)
    require(account.pw_name=='jazofv1' and account.pw_gid==1000
        and account.pw_dir=='/home/jazofv1','PI3_ACCOUNT_HOME_MISMATCH')

def load_engine(raw=None):
    if raw is None:
        opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with opener.open(ENGINE_SOURCE['url'],timeout=30) as response:
            require(response.geturl()==ENGINE_SOURCE['url'],'ENGINE_REDIRECT_REFUSED')
            raw=response.read(1048577)
    require(type(raw)is bytes and len(raw)==ENGINE_SOURCE['size']
        and sha(raw)==ENGINE_SOURCE['sha256'],'ACCEPTED_ENGINE_IDENTITY_MISMATCH')
    engine=types.ModuleType('pe73_pi3_private_dependency_engine')
    engine.__file__=ENGINE_SOURCE['url']
    exec(compile(raw,ENGINE_SOURCE['url'],'exec'),engine.__dict__)
    return engine

def owned_directory(path,mode=None):
    """Descriptor-bound complete ancestry, root or owner ancestors, owner leaf."""
    require(path.is_absolute() and '..' not in path.parts,'UNSAFE_ENVIRONMENT_PATH')
    fds=[];chain=[]
    def validate(fd,leaf=False):
        info=os.fstat(fd)
        require(stat.S_ISDIR(info.st_mode) and info.st_uid in (0,1000)
            and not stat.S_IMODE(info.st_mode)&0o022,'ENVIRONMENT_ANCESTRY_SECURITY')
        if leaf:
            require(info.st_uid==info.st_gid==1000,'ENVIRONMENT_LEAF_OWNER')
            if mode is not None:require(stat.S_IMODE(info.st_mode)==mode,'ENVIRONMENT_PRIVATE_MODE')
        for name in ('system.posix_acl_access','system.posix_acl_default'):
            try:os.getxattr(fd,name)
            except OSError as error:
                import errno
                require(error.errno==errno.ENODATA,'ENVIRONMENT_ACL_UNKNOWN')
            else:raise Blocked('ENVIRONMENT_ACL_PRESENT')
        return info
    try:
        fd=os.open('/',os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC);fds.append(fd);validate(fd)
        for part in path.parts[1:]:
            child=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC,dir_fd=fd)
            fds.append(child);validate(child);chain.append((fd,part,child));fd=child
        result=validate(fd,True)
        for parent,name,child in chain:
            named=os.stat(name,dir_fd=parent,follow_symlinks=False);held=validate(child)
            require((named.st_dev,named.st_ino)==(held.st_dev,held.st_ino),'ENVIRONMENT_ANCESTOR_DRIFT')
        return result
    finally:
        for fd in reversed(fds):os.close(fd)

def new_file(path,raw):
    # Adapt only the role identity of the accepted cache writer; no trust writer.
    fd=os.open(path,os.O_RDWR|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW|os.O_CLOEXEC,0o600)
    try:
        info=os.fstat(fd)
        require(stat.S_ISREG(info.st_mode) and info.st_uid==info.st_gid==1000 and info.st_nlink==1
            and stat.S_IMODE(info.st_mode)==0o600,'PI3_NEW_CACHE_FILE_SECURITY')
        with os.fdopen(os.dup(fd),'wb') as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())
        os.lseek(fd,0,os.SEEK_SET)
        require(os.read(fd,len(raw)+1)==raw,'PI3_CACHE_FILE_READBACK')
        named=path.lstat()
        require((info.st_dev,info.st_ino)==(named.st_dev,named.st_ino),'PI3_CACHE_FILE_DRIFT')
    finally:os.close(fd)

def fingerprint(root):
    result={}
    for path in sorted(root.rglob('*')):
        if path==root/'ready.json':continue
        info=path.lstat();relative=str(path.relative_to(root))
        require(info.st_uid==info.st_gid==1000,'PI3_ENVIRONMENT_OWNER')
        if stat.S_ISLNK(info.st_mode):
            require(relative=='venv/lib64' and os.readlink(path)=='lib','PI3_UNEXPECTED_SYMLINK')
            result[relative]={'link':'lib'}
        else:
            require(not stat.S_IMODE(info.st_mode)&0o022,'PI3_ENVIRONMENT_MODE')
            if stat.S_ISREG(info.st_mode):
                require(info.st_nlink==1,'PI3_ENVIRONMENT_HARDLINK')
                result[relative]={'sha256':sha(path.read_bytes()),'mode':stat.S_IMODE(info.st_mode)}
            else:require(stat.S_ISDIR(info.st_mode),'PI3_ENVIRONMENT_TYPE')
    return result

EXTRA_SMOKE=r'''
# Import the exact existing provisioning glue; no CLI or production functions.
import importlib.util,datetime,secrets
helper=root/'tools/pe73_ha_provision.py'
assert hashlib.sha256(helper.read_bytes()).hexdigest()=='2594d985f76d51b02365ca2ef98f02ac4372e566559be893762a41e6ccb39d89'
spec=importlib.util.spec_from_file_location('pe73_pi3_api_smoke',helper)
q=importlib.util.module_from_spec(spec);spec.loader.exec_module(q)
q.crypto();q.native()
# Exercise required APIs with an ephemeral non-CA leaf and encrypted in-memory
# key only. Certificate APIs use a fixed PUBLIC EXPIRED NON-CA fixture;
# no certificate is signed/issued on the Pi. No production identity, CA or HMAC.
password=secrets.token_bytes(32)
encoded=key.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,
    serialization.BestAvailableEncryption(password))
restored=serialization.load_pem_private_key(encoded,password)
assert restored.public_key().public_numbers()==key.public_key().public_numbers()
leaf=x509.load_pem_x509_certificate(b'-----BEGIN CERTIFICATE-----\nMIIBYjCCAQmgAwIBAgIDCyTHMAoGCCqGSM49BAMCMDExLzAtBgNVBAMMJlBFNzMg\nUFVCTElDIEVYUElSRUQgTk9OIENBIEFQSSBGSVhUVVJFMB4XDTIwMDEwMTAwMDAw\nMFoXDTIxMDEwMTAwMDAwMFowMTEvMC0GA1UEAwwmUEU3MyBQVUJMSUMgRVhQSVJF\nRCBOT04gQ0EgQVBJIEZJWFRVUkUwWTATBgcqhkjOPQIBBggqhkjOPQMBBwNCAATj\np5xBbaJnZ6U2YwOfiyjaJPtmahJPX+UJEFg2Z4WggjKn6DLhuY41VudJqJSwCmRZ\ntfcVLhUEeXr31FHMjYlkoxAwDjAMBgNVHRMBAf8EAjAAMAoGCCqGSM49BAMCA0cA\nMEQCIHWa/HfBc9UQVtCPxxZ8d5yYHNabJc6uCxoTf7EWdrmSAiAuUz6Ix4vX+DSM\nrBmrvaOt017lRrJLjY6kgxAhbA+VYg==\n-----END CERTIFICATE-----\n')
leaf.verify_directly_issued_by(leaf)
assert leaf.not_valid_before_utc<leaf.not_valid_after_utc
assert len(x509.load_pem_x509_certificates(leaf.public_bytes(serialization.Encoding.PEM)))==1
'''

def profile(engine):
    """Private in-memory PI3 profile, never edits PI5 source or environment."""
    engine.ROOT=ROOT;engine.WHEELS=WHEELS
    engine.target=target;engine.owned_directory=owned_directory
    engine.new_file=new_file;engine.fingerprint=fingerprint
    marker="print(json.dumps({'RESULT':'PASS_ISOLATED_CRYPTOGRAPHY_SMOKE'"
    require(engine.SMOKE.count(marker)==1,'ACCEPTED_SMOKE_BINDING_MISMATCH')
    engine.SMOKE=engine.SMOKE.replace(marker,EXTRA_SMOKE+'\n'+marker)
    return engine

def prepare():
    target()  # No root, download or filesystem work on the wrong target.
    require(not os.path.lexists(ROOT),'EXISTING_PI3_ENVIRONMENT_REFUSED')
    engine=profile(load_engine())
    result=engine.prepare()  # Same finite install/refusal algorithm as accepted PI5.
    require(result['RESULT']=='PASS_PI5_ISOLATED_PROVISIONING_ENVIRONMENT'
        and result['native_smoke']=='PASS','SHARED_ENGINE_RESULT_MISMATCH')
    return {'RESULT':'PASS_PI3_ISOLATED_PROVISIONING_ENVIRONMENT',
        'target':'PI3_NUT_AND_PIHOLE','environment':str(ROOT),'uid':1000,'gid':1000,
        'versions':engine.VERSIONS,'native_smoke':'PASS','provisioning_crypto_apis':'PASS',
        'system_packages_modified':False,'production_credentials_created':False,
        'production_CA_created':False,'HMAC_material_provisioned':False,
        'HIOC_modified':False,'services_modified':False,'PI5_modified':False,
        'PE73':'IN_PROGRESS','PE74':'NOT_AUTHORIZED','STOP_REQUIRED':True}

def main(argv=None):
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=('prepare',))
    parser.parse_args(argv);return prepare()

if __name__=='__main__':
    try:receipt=main()
    except BaseException as error:
        code=str(error) if isinstance(error,ValueError) and str(error).isupper() and str(error).replace('_','').isalnum() else 'PI3_ISOLATED_RUNTIME_OR_IO_NOT_ESTABLISHED'
        receipt={'RESULT':'BLOCKED_PI3_ISOLATED_PROVISIONING_ENVIRONMENT','failure_code':code,
            'cleanup':'RETAINED_NO_AUTOMATIC_DELETE_OR_RETRY','production_credentials_created':False,
            'HIOC_modified':False,'PI5_modified':False,'STOP_REQUIRED':True}
    print(json.dumps(receipt,sort_keys=True,separators=(',',':')))
    raise SystemExit(0 if receipt['RESULT'].startswith('PASS_') else 1)
