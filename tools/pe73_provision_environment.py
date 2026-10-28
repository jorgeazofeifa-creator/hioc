"""Pinned, finite PI5 Terminal-only provisioning dependencies. Never executes Core.

Uses stdlib venv and official pip; no wheel extractor, source build, host package
install, trust publisher, deployment journal, service or automatic recovery.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path, PurePosixPath
import platform
import stat
import subprocess
import sys
import sysconfig
import urllib.request
import zipfile

ROOT=Path('/root/.hioc-pe73-provision-environment')
VERSIONS={'cryptography':'50.0.2','cffi':'2.0.0','pycparser':'2.23'}
WHEELS=[{'name': 'cryptography-50.0.2-cp311-abi3-manylinux2014_aarch64.manylinux_2_17_aarch64.whl', 'size': 4731146, 'sha256': '79def8d059362e7831389ed3be0ecdf58a89386e1271e35dd9f5af84e81bffd0', 'url': 'https://files.pythonhosted.org/packages/d9/69/c9bd862c3bf43d6399c433caf002df16e2dffd4be49bdf515cda38038711/cryptography-50.0.2-cp311-abi3-manylinux2014_aarch64.manylinux_2_17_aarch64.whl'}, {'name': 'cryptography-50.0.2-cp311-abi3-musllinux_1_2_aarch64.whl', 'size': 4870819, 'sha256': '25784ce8b9621c90c643efb9e1e2162ab3b0224cae446ad5e70e7fcb1ce18b51', 'url': 'https://files.pythonhosted.org/packages/6c/5d/906970b83bbfc1f5bbfb677a143c181f2801f23b6a7204a3b47c42c97e65/cryptography-50.0.2-cp311-abi3-musllinux_1_2_aarch64.whl'}, {'name': 'cffi-2.0.0-cp314-cp314-manylinux2014_aarch64.manylinux_2_17_aarch64.whl', 'size': 220049, 'sha256': '24b6f81f1983e6df8db3adc38562c83f7d4a0c36162885ec7f7b77c7dcbec97b', 'url': 'https://files.pythonhosted.org/packages/d6/43/0e822876f87ea8a4ef95442c3d766a06a51fc5298823f884ef87aaad168c/cffi-2.0.0-cp314-cp314-manylinux2014_aarch64.manylinux_2_17_aarch64.whl'}, {'name': 'cffi-2.0.0-cp314-cp314-musllinux_1_2_aarch64.whl', 'size': 222828, 'sha256': '737fe7d37e1a1bffe70bd5754ea763a62a066dc5913ca57e957824b72a85e205', 'url': 'https://files.pythonhosted.org/packages/2b/0f/1f177e3683aead2bb00f7679a16451d302c436b5cbf2505f0ea8146ef59e/cffi-2.0.0-cp314-cp314-musllinux_1_2_aarch64.whl'}, {'name': 'pycparser-2.23-py3-none-any.whl', 'size': 118140, 'sha256': 'e5c6e8d3fbad53479cab09ac03729e0a9faf2bee3db8208a550daf5af81a5934', 'url': 'https://files.pythonhosted.org/packages/a0/e3/59cd50310fc9b59512193629e1984c1f95e5c8ae6e5d8c69532ccc65a7fe/pycparser-2.23-py3-none-any.whl'}, {'name': 'pip-25.3-py3-none-any.whl', 'size': 1778622, 'sha256': '9655943313a94722b7774661c21049070f6bbb0a1516bf02f7c8d5d9201514cd', 'url': 'https://files.pythonhosted.org/packages/44/3c/d717024885424591d5376220b5e836c2d5293ce2011523c9de23ff7bf068/pip-25.3-py3-none-any.whl'}]
TOOLKIT=[{'name': 'pe73_ha_provision.py', 'size': 30478, 'sha256': '2594d985f76d51b02365ca2ef98f02ac4372e566559be893762a41e6ccb39d89', 'url': 'https://raw.githubusercontent.com/jorgeazofeifa-creator/hioc/b5a020982484e35126daa70b256860a23af8e88f/tools/pe73_ha_provision.py'}, {'name': 'pe73_ha_production.py', 'size': 43208, 'sha256': '86e4333ef2df1bf67b4621ccd6a3314f1322af00dafb42e9d3c5f0724e7bd23c', 'url': 'https://raw.githubusercontent.com/jorgeazofeifa-creator/hioc/686be8841f461eacd57a9076948acf632bbf7bea/tools/pe73_ha_production.py'}, {'name': 'pe73_ha_delivery.py', 'size': 47825, 'sha256': '25ab8ca4140b9ddc73b60f8e921b426a234901ab6634d2239f865469505558ca', 'url': 'https://raw.githubusercontent.com/jorgeazofeifa-creator/hioc/686be8841f461eacd57a9076948acf632bbf7bea/tools/pe73_ha_delivery.py'}, {'name': 'pe73_ha_assess.py', 'size': 27164, 'sha256': 'da4c97ef7e5acaf5840b9cbca03ee0cd888183e784a3f55bb8671b45b8372443', 'url': 'https://raw.githubusercontent.com/jorgeazofeifa-creator/hioc/686be8841f461eacd57a9076948acf632bbf7bea/tools/pe73_ha_assess.py'}, {'name': 'pe73_ha_live_qualify.py', 'size': 19844, 'sha256': 'ce4bbd30fdb268ec28637f990b85e9640d174a120eba971ed730f7ba94dfb845', 'url': 'https://raw.githubusercontent.com/jorgeazofeifa-creator/hioc/686be8841f461eacd57a9076948acf632bbf7bea/tools/pe73_ha_live_qualify.py'}, {'name': 'pe73_maintenance_window.py', 'size': 54151, 'sha256': '756eb3ad2c43047a60a43398afb4c34d165dad8729803099dc367da90f1bd741', 'url': 'https://raw.githubusercontent.com/jorgeazofeifa-creator/hioc/686be8841f461eacd57a9076948acf632bbf7bea/tools/pe73_maintenance_window.py'}, {'name': 'hioc-pe73-pi3-delivery.py', 'size': 67571, 'sha256': '76b422edc73ed87baba94fef6fcfa8e197a564d4d8f57c95dba6b8a1624907d2', 'url': 'https://raw.githubusercontent.com/jorgeazofeifa-creator/hioc/686be8841f461eacd57a9076948acf632bbf7bea/tools/hioc-pe73-pi3-delivery.py'}]
MAX_FILE=16777216

class Blocked(ValueError):pass
def require(value,code):
    if not value:raise Blocked(code)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()

def target():
    require(sys.platform=='linux' and platform.python_implementation()=='CPython'
        and sys.version_info[:2]==(3,14) and platform.machine()=='aarch64'
        and not sysconfig.get_config_var('Py_GIL_DISABLED'),'SUPPORTED_TERMINAL_ABI_REQUIRED')
    require(os.getuid()==os.geteuid()==os.getgid()==os.getegid()==0,'TERMINAL_IDENTITY_REQUIRED')
    # No guessing of musl/glibc version. Official pip wheel tags decide below.
    require(Path(sys.executable).resolve().is_file(),'TERMINAL_INTERPRETER_REQUIRED')

def clean_env(root):
    # Do not pass Supervisor/application tokens, SSH agents, proxy passwords,
    # pip credentials/configuration or any other inherited secrets to subprocesses.
    return {'PATH':'/usr/bin:/bin','HOME':str(root/'home'),'TMPDIR':str(root/'tmp'),
        'LANG':'C.UTF-8','PIP_CONFIG_FILE':os.devnull,'PYTHONDONTWRITEBYTECODE':'1'}

def checked(raw,item):
    require(type(raw)is bytes and len(raw)==item['size'] and len(raw)<=MAX_FILE
        and sha(raw)==item['sha256'],'DEPENDENCY_IDENTITY_MISMATCH')
    return raw

def fetch(item):
    url=item['url']
    require(url.startswith('https://files.pythonhosted.org/packages/') or
        url.startswith('https://raw.githubusercontent.com/jorgeazofeifa-creator/hioc/'), 'APPROVED_SOURCE_REQUIRED')
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(url,timeout=30) as response:
        require(response.geturl()==url,'DEPENDENCY_REDIRECT_REFUSED')
        raw=response.read(min(MAX_FILE,item['size'])+1)
    return checked(raw,item)

def validate_wheel(raw,name):
    require(name.endswith('.whl'),'BINARY_WHEEL_REQUIRED')
    with zipfile.ZipFile(io.BytesIO(raw)) as wheel:
        entries=wheel.infolist();names=[x.filename for x in entries]
        require(len(names)==len(set(names)) and len(names)<=4096
            and sum(x.file_size for x in entries)<=67108864,'WHEEL_ARCHIVE_LIMIT')
        for item in entries:
            path=PurePosixPath(item.filename)
            require(not path.is_absolute() and '..' not in path.parts and '\\' not in item.filename
                and not stat.S_ISLNK(item.external_attr>>16),'UNSAFE_WHEEL_MEMBER')
        require(any(x.endswith('.dist-info/WHEEL') for x in names)
            and any(x.endswith('.dist-info/RECORD') for x in names),'WHEEL_METADATA_REQUIRED')

def lock_text():
    return ''.join(name+'=='+version+''.join(' --hash=sha256:'+x['sha256']
        for x in WHEELS if x['name'].startswith(name+'-'))+'\n' for name,version in VERSIONS.items()).encode()

def owned_directory(path,mode=None):
    info=path.lstat()
    require(stat.S_ISDIR(info.st_mode) and info.st_uid==info.st_gid==0
        and not stat.S_IMODE(info.st_mode)&0o022,'ENVIRONMENT_DIRECTORY_SECURITY')
    if mode is not None:require(stat.S_IMODE(info.st_mode)==mode,'ENVIRONMENT_PRIVATE_MODE')
    fd=os.open(path,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC)
    try:
        require((info.st_dev,info.st_ino)==(os.fstat(fd).st_dev,os.fstat(fd).st_ino),'ENVIRONMENT_DIRECTORY_DRIFT')
        for name in ('system.posix_acl_access','system.posix_acl_default'):
            try:os.getxattr(fd,name)
            except OSError as error:
                import errno
                require(error.errno==errno.ENODATA,'ENVIRONMENT_ACL_UNKNOWN')
            else:raise Blocked('ENVIRONMENT_ACL_PRESENT')
    finally:os.close(fd)
    return info

def new_file(path,raw):
    # Every caller uses only a new private tree, no existing credential path.
    fd=os.open(path,os.O_RDWR|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW|os.O_CLOEXEC,0o600)
    try:
        info=os.fstat(fd)
        require(stat.S_ISREG(info.st_mode) and info.st_uid==info.st_gid==0 and info.st_nlink==1
            and stat.S_IMODE(info.st_mode)==0o600,'NEW_ENVIRONMENT_FILE_SECURITY')
        with os.fdopen(os.dup(fd),'wb') as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())
        os.lseek(fd,0,os.SEEK_SET)
        require(os.read(fd,len(raw)+1)==raw,'ENVIRONMENT_FILE_READBACK')
        require((info.st_dev,info.st_ino)==(path.lstat().st_dev,path.lstat().st_ino),'ENVIRONMENT_FILE_DRIFT')
    finally:os.close(fd)

def invoke(argv,root,code="ISOLATED_DEPENDENCY_COMMAND_FAILED"):
    result=subprocess.run(argv,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,timeout=120,env=clean_env(root),cwd=root)
    require(result.returncode==0 and len(result.stdout)<=1048576 and len(result.stderr)<=1048576,
        code)
    # No raw installer/native exception output in user-visible receipts.
    return result.stdout

def pip_command(root,*,dry_run=False):
    pip=next(x['name'] for x in WHEELS if x['name'].startswith('pip-'))
    wrapper="import runpy,sys; sys.path.insert(0,sys.argv.pop(1)); runpy.run_module('pip',run_name='__main__')"
    args=[str(root/'venv/bin/python3'),'-I','-B','-c',wrapper,str(root/'wheels'/pip),
        '--isolated','--disable-pip-version-check','install','--no-index','--no-deps',
        '--only-binary=:all:','--require-hashes','--no-cache-dir','--no-compile','--no-user',
        '--prefix',str(root/'venv'),'--find-links',str(root/'wheels'),'-r',str(root/'requirements.lock')]
    if dry_run:args+=['--dry-run']
    return args

SMOKE=r'''
import hashlib,importlib.metadata,json,pathlib,site,sys
root=pathlib.Path(sys.argv[1]);venv=root/'venv'
assert sys.prefix!=sys.base_prefix and pathlib.Path(sys.prefix).resolve()==venv.resolve()
assert site.ENABLE_USER_SITE is False
import cryptography,cffi,pycparser,_cffi_backend
expected={'cryptography':'50.0.2','cffi':'2.0.0','pycparser':'2.23'}
for name,version in expected.items():assert importlib.metadata.version(name)==version
for module in (cryptography,cffi,pycparser,_cffi_backend):
    assert pathlib.Path(module.__file__).resolve().is_relative_to(venv.resolve())
from cryptography import x509
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.x509.oid import NameOID
# Ephemeral in-memory dependency test, not a production client credential.
key=ec.generate_private_key(ec.SECP256R1())
csr=x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
    x509.NameAttribute(NameOID.COMMON_NAME,'PE73 ephemeral dependency smoke')])).sign(key,hashes.SHA256())
assert csr.is_signature_valid
assert callable(x509.load_pem_x509_certificates) and hasattr(x509.Certificate,'not_valid_after_utc')
assert hasattr(x509.Certificate,'verify_directly_issued_by')
print(json.dumps({'RESULT':'PASS_ISOLATED_CRYPTOGRAPHY_SMOKE','versions':expected,'private_material_output':False},sort_keys=True))
'''

def fingerprint(root):
    """Dependency receipt only; no trust/deployment state or secret identities."""
    result={}
    for path in sorted(root.rglob('*')):
        if path==root/'ready.json':continue
        info=path.lstat();relative=str(path.relative_to(root))
        require(info.st_uid==info.st_gid==0,'ENVIRONMENT_OWNER_OR_MODE')
        if not stat.S_ISLNK(info.st_mode):
            require(not stat.S_IMODE(info.st_mode)&0o022,'ENVIRONMENT_OWNER_OR_MODE')
        if stat.S_ISLNK(info.st_mode):
            # stdlib venv's lib64 -> lib is the only allowed directory alias.
            require(relative=='venv/lib64' and os.readlink(path)=='lib','UNEXPECTED_ENVIRONMENT_SYMLINK')
            result[relative]={'link':'lib'}
        elif stat.S_ISREG(info.st_mode):
            require(info.st_nlink==1,'ENVIRONMENT_HARDLINK')
            result[relative]={'sha256':sha(path.read_bytes()),'mode':stat.S_IMODE(info.st_mode)}
        else:require(stat.S_ISDIR(info.st_mode),'ENVIRONMENT_OBJECT_TYPE')
    return result

def sync_directory(path):
    fd=os.open(path,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try:os.fsync(fd)
    finally:os.close(fd)


def prepare():
    target()
    try:import venv
    except ImportError:raise Blocked("STDLIB_VENV_UNAVAILABLE") from None
    require(not os.path.lexists(ROOT),'EXISTING_ENVIRONMENT_REFUSED')
    owned_directory(ROOT.parent)
    # Verify ALL immutable downloads before creating the new environment.
    payloads={item['name']:fetch(item) for item in [*WHEELS,*TOOLKIT]}
    for item in WHEELS:validate_wheel(payloads[item['name']],item['name'])
    os.mkdir(ROOT,0o700)
    owned_directory(ROOT,0o700)
    for child in ('wheels','tools','home','tmp'):(ROOT/child).mkdir(mode=0o700)
    for item in [*WHEELS,*TOOLKIT]:
        new_file(ROOT/('wheels' if item in WHEELS else 'tools')/item['name'],payloads[item['name']])
    new_file(ROOT/'requirements.lock',lock_text())
    # No ensurepip, global/user packages, package upgrades or Core invocation.
    venv.EnvBuilder(system_site_packages=False,clear=False,symlinks=False,
        with_pip=False,upgrade=False).create(ROOT/'venv')
    invoke(pip_command(ROOT,dry_run=True),ROOT,'PINNED_WHEEL_TAG_OR_OFFLINE_RESOLUTION_UNSUPPORTED')  # Reject unsupported libc/wheel tags before install.
    invoke(pip_command(ROOT),ROOT)  # One offline binary-only installation, no retry.
    report=json.loads(invoke([str(ROOT/'venv/bin/python3'),'-I','-B','-c',SMOKE,str(ROOT)],ROOT))
    require(report=={'RESULT':'PASS_ISOLATED_CRYPTOGRAPHY_SMOKE','versions':VERSIONS,'private_material_output':False},'ISOLATED_SMOKE_NOT_ESTABLISHED')
    seal={'schema':1,'source_python':sha(Path(sys.executable).resolve().read_bytes()),
        'python_version':list(sys.version_info[:3]),'files':fingerprint(ROOT),'versions':VERSIONS}
    new_file(ROOT/'ready.json',canonical(seal))
    sync_directory(ROOT)
    return {'RESULT':'PASS_PI5_ISOLATED_PROVISIONING_ENVIRONMENT','target':'PI5_HA_TERMINAL',
        'versions':VERSIONS,'environment':str(ROOT),'native_smoke':'PASS',
        'Core_modified':False,'global_packages_modified':False,'production_credentials_created':False,
        'private_client_key_transferred':False,'production_runtime_modified':False,
        'PE73':'IN_PROGRESS','PE74':'NOT_AUTHORIZED','STOP_REQUIRED':True}

def launch(action):
    target();require(action in ('ha-request','ha-complete'),'HA_PROVISIONING_ACTION_ONLY')
    owned_directory(ROOT,0o700)
    ready=ROOT/'ready.json';info=ready.lstat()
    require(stat.S_ISREG(info.st_mode) and info.st_uid==info.st_gid==0 and info.st_nlink==1
        and stat.S_IMODE(info.st_mode)==0o600,'READY_RECEIPT_SECURITY')
    value=json.loads(ready.read_bytes())
    require(value=={'schema':1,'source_python':sha(Path(sys.executable).resolve().read_bytes()),
        'python_version':list(sys.version_info[:3]),'files':fingerprint(ROOT),'versions':VERSIONS},'ISOLATED_ENVIRONMENT_DRIFT')
    # No exec/replacement shell. Inherit the operator terminal ONLY for the existing
    # masked local policy inputs. No per-operation approval or custom trust layer.
    result=subprocess.run([str(ROOT/'venv/bin/python3'),'-I','-B',
        str(ROOT/'tools/pe73_ha_provision.py'),action],check=False,env={**clean_env(ROOT),'HOME':'/root',**({'SSH_AUTH_SOCK':os.environ['SSH_AUTH_SOCK']} if 'SSH_AUTH_SOCK' in os.environ else {})})
    require(result.returncode==0,'PROVISIONING_ACTION_BLOCKED_NO_RETRY')
    return {'RESULT':'PASS_ISOLATED_PROVISIONING_ACTION','action':action,'STOP_REQUIRED':True}

def main(argv=None):
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=('prepare','ha-request','ha-complete'))
    args=parser.parse_args(argv)
    return prepare() if args.action=='prepare' else launch(args.action)

if __name__=='__main__':
    try:receipt=main()
    except BaseException as error:
        # Never recursively remove a partial venv or unknown/replaced object.
        # Absence of ready.json prevents all credential operations. Preserve it
        # for explicit recovery; no automatic deletion/retry or secret handling.
        receipt={'RESULT':'BLOCKED_PI5_ISOLATED_ENVIRONMENT','cleanup':'RETAINED_NO_AUTOMATIC_DELETE_OR_RETRY',
            'Core_modified':False,'failure_code':str(error) if type(error)is Blocked else 'ISOLATED_RUNTIME_OR_IO_NOT_ESTABLISHED','STOP_REQUIRED':True}
    print(json.dumps(receipt,sort_keys=True,separators=(',',':')))
    raise SystemExit(0 if receipt['RESULT'].startswith('PASS_') else 1)
