#!/usr/bin/env python3
"""PE-4.0B.2a-B: transfer the frozen wheel and lock to private PI3 staging."""
from __future__ import annotations
import base64, getpass, hashlib, json, os, pathlib, re, shlex, stat, sys
from hioc_pe4_runtime_common import *

TOOL_RELATIVE="tools/hioc-pe4-artifact-transfer.py"
SOURCE_RELATIVES=(TOOL_RELATIVE,"tools/hioc_pe4_runtime_common.py","requirements-pe4.lock")
STATE_KEYS=("REMOTE_STAGING_CREATED","WHEEL_TRANSFERRED","LOCK_TRANSFERRED","REMOTE_ARTIFACT_VERIFIED","REMOTE_LOCK_VERIFIED")
EVIDENCE_STATES=("NOT_PUBLISHED","CONFIRMED","UNCERTAIN")
EXPECTED_WINDOWS_OPERATOR="JorgeAzofeifaCastill"
EXPECTED_WINDOWS_PROFILE=pathlib.PureWindowsPath(r"C:\Users\JorgeAzofeifaCastill")
EXPECTED_PUBLIC_FINGERPRINT="SHA256:fQn8fFfCxcDSVD9ohgp2zKJoDTiGN9qJmAkHii1WJpU"
EXPECTED_PUBLIC_COMMENT="hioc-pe4-action-b-windows"
EXPECTED_HOST_FINGERPRINT="SHA256:JlBiwMynecRJ0m0tDsA1Ks1E5xo2BKcOJKd8pzWyVQQ"
SSH_STATIC_OPTIONS=("-F","none",f"-oHostname={PI3_IPV4}",f"-oPort={SSH_PORT}",
                    "-oCanonicalizeHostname=no","-oCanonicalizeFallbackLocal=no",
                    "-oProxyCommand=none","-oProxyJump=none","-oGlobalKnownHostsFile=none",
                    f"-oHostKeyAlias={PI3_IPV4}","-oCheckHostIP=yes",
                    "-oBatchMode=yes","-oStrictHostKeyChecking=yes","-oConnectTimeout=5",
                    "-oConnectionAttempts=1","-oNumberOfPasswordPrompts=0",
                    "-oPasswordAuthentication=no","-oKbdInteractiveAuthentication=no",
                    "-oPreferredAuthentications=publickey","-oPubkeyAuthentication=yes",
                    "-oHostbasedAuthentication=no","-oGSSAPIAuthentication=no",
                    "-oIdentitiesOnly=yes","-oIdentityAgent=none","-oAddKeysToAgent=no",
                    "-oForwardAgent=no","-oForwardX11=no","-oClearAllForwardings=yes",
                    "-oPermitLocalCommand=no","-oLogLevel=ERROR")

def transport_options(known_hosts,identity):
    return (*SSH_STATIC_OPTIONS,f"-oUserKnownHostsFile={known_hosts}",f"-oIdentityFile={identity}")

def parse_cli(argv):
    if len(argv)!=2 or argv[0]!="--governance-commit" or not re.fullmatch(r"[0-9a-f]{40}",argv[1]):
        raise Failure("INVALID_ARGUMENTS","INPUT_VALIDATION")
    return argv[1]

def local_inputs(commit):
    verify_repository(REPOSITORY_ROOT,commit,SOURCE_RELATIVES)
    pe4=workstation_cache_root(); trusted=pe4.parents[2]
    cache=validate_windows_hierarchy(trusted,("HIOC","artifacts","pe4","cache"))
    for directory in (trusted/"HIOC",trusted/"HIOC/artifacts",pe4,cache): validate_workstation_path_acl(directory,True)
    wheel=cache/WHEEL_NAME
    if not wheel.exists() or wheel.is_symlink() or windows_reparse_point(wheel) or not wheel.is_file():
        raise Failure("ARTIFACT_PATH_UNSAFE","ARTIFACT_IDENTITY")
    validate_workstation_path_acl(wheel,False)
    if wheel.stat().st_size!=WHEEL_SIZE: raise Failure("ARTIFACT_SIZE_MISMATCH","ARTIFACT_IDENTITY")
    if sha256(wheel)!=WHEEL_SHA256: raise Failure("ARTIFACT_SHA256_MISMATCH","ARTIFACT_IDENTITY")
    require_regular(LOCAL_LOCK)
    if sha256(LOCAL_LOCK)!=LOCK_SHA256: raise Failure("LOCK_IDENTITY_MISMATCH","ARTIFACT_IDENTITY")
    return wheel,LOCAL_LOCK

def _public_record(path):
    if path.stat().st_size>16384: raise Failure("SSH_PUBLIC_KEY_OVERSIZED","OPENSSH_IDENTITY")
    try: value=path.read_text(encoding="ascii")
    except (OSError,UnicodeError): raise Failure("SSH_PUBLIC_KEY_INVALID","OPENSSH_IDENTITY")
    if value.endswith("\r\n"): value=value[:-2]
    elif value.endswith("\n"): value=value[:-1]
    if "\r" in value or "\n" in value: raise Failure("SSH_PUBLIC_KEY_INVALID","OPENSSH_IDENTITY")
    fields=value.split(" ")
    if len(fields)!=3 or fields[0]!="ssh-ed25519" or fields[2]!=EXPECTED_PUBLIC_COMMENT:
        raise Failure("SSH_PUBLIC_KEY_IDENTITY_MISMATCH","OPENSSH_IDENTITY")
    try: base64.b64decode(fields[1],validate=True)
    except Exception: raise Failure("SSH_PUBLIC_KEY_INVALID","OPENSSH_IDENTITY")
    return fields

def _fingerprint_record(output,code):
    match=re.fullmatch(r"\d+ (SHA256:[A-Za-z0-9+/]+={0,2}) .+ \(ED25519\)\r?\n?",output)
    if not match: raise Failure(code,"OPENSSH_IDENTITY")
    return match.group(1)

def validate_local_transport(resolver=windows_openssh_tool,runner=run_bounded,
                             operator_resolver=getpass.getuser,profile_resolver=windows_profile_root,
                             hasher=sha256):
    if os.name!="nt" or operator_resolver()!=EXPECTED_WINDOWS_OPERATOR:
        raise Failure("WINDOWS_OPERATOR_MISMATCH","OPENSSH_IDENTITY")
    profile=profile_resolver()
    if pathlib.PureWindowsPath(profile)!=EXPECTED_WINDOWS_PROFILE:
        raise Failure("WINDOWS_PROFILE_MISMATCH","OPENSSH_IDENTITY")
    ssh_directory=profile/".ssh"
    paths=(ssh_directory,ssh_directory/SSH_KNOWN_HOSTS_NAME,
           ssh_directory/SSH_IDENTITY_NAME,ssh_directory/(SSH_IDENTITY_NAME+".pub"))
    for index,path in enumerate(paths):
        try: info=path.lstat()
        except OSError: raise Failure("OPENSSH_MATERIAL_MISSING","OPENSSH_IDENTITY")
        expected=stat.S_ISDIR(info.st_mode) if index==0 else stat.S_ISREG(info.st_mode)
        if not expected or path.is_symlink() or windows_reparse_point(path) or (index and info.st_size<=0):
            raise Failure("OPENSSH_MATERIAL_UNSAFE","OPENSSH_IDENTITY")
    known_hosts,identity,public=paths[1:]
    ssh,keygen=resolver("ssh"),resolver("ssh-keygen")
    if hasher(ssh)!=SSH_CLIENT_SHA256 or hasher(keygen)!=SSH_KEYGEN_SHA256:
        raise Failure("OPENSSH_EXECUTABLE_IDENTITY_MISMATCH","OPENSSH_IDENTITY")
    fields=_public_record(public)
    fingerprint=runner([str(keygen),"-lf",str(public),"-E","sha256"],
                       "OPENSSH_IDENTITY",timeout=10,max_output=4096).stdout
    if _fingerprint_record(fingerprint,"SSH_PUBLIC_FINGERPRINT_MISMATCH")!=EXPECTED_PUBLIC_FINGERPRINT:
        raise Failure("SSH_PUBLIC_FINGERPRINT_MISMATCH","OPENSSH_IDENTITY")
    derived=runner([str(keygen),"-y","-f",str(identity)],"OPENSSH_IDENTITY",
                   timeout=10,max_output=16384).stdout.strip().split()
    if len(derived) not in (2,3) or derived[:2]!=fields[:2] or (len(derived)==3 and derived[2]!=EXPECTED_PUBLIC_COMMENT):
        raise Failure("SSH_KEY_PAIR_MISMATCH","OPENSSH_IDENTITY")
    lookup=runner([str(keygen),"-F",PI3_IPV4,"-f",str(known_hosts)],"OPENSSH_IDENTITY",
                  timeout=10,max_output=65536).stdout
    fingerprints=[]
    for line in lookup.splitlines():
        if not line or line.startswith("#"): continue
        parts=line.split()
        if len(parts)<3 or parts[1]!="ssh-ed25519":
            raise Failure("KNOWN_HOSTS_IDENTITY_MISMATCH","OPENSSH_IDENTITY")
        try: raw=base64.b64decode(parts[2],validate=True)
        except Exception: raise Failure("KNOWN_HOSTS_INVALID","OPENSSH_IDENTITY")
        fingerprints.append("SHA256:"+base64.b64encode(hashlib.sha256(raw).digest()).decode().rstrip("="))
    if not fingerprints or set(fingerprints)!={EXPECTED_HOST_FINGERPRINT}:
        raise Failure("KNOWN_HOSTS_IDENTITY_MISMATCH","OPENSSH_IDENTITY")
    return ssh,known_hosts,identity

def remote_guard(remote):
    q=shlex.quote(remote)
    return f"test -d {q} || exit 41; test ! -L {q} || exit 42; test \"$(stat -c %U -- {q})\" = {OWNER} || exit 43; test \"$(stat -c %a -- {q})\" = 700 || exit 44"

REMOTE_NO_REPLACE = """import ctypes,errno,os,stat,sys
source,destination=sys.argv[1:3]
try: source_info=os.lstat(source)
except OSError: raise SystemExit(91)
if not stat.S_ISREG(source_info.st_mode): raise SystemExit(92)
try: os.lstat(destination)
except FileNotFoundError: pass
except OSError: raise SystemExit(93)
else: raise SystemExit(94)
libc=ctypes.CDLL(None,use_errno=True)
renameat2=getattr(libc,'renameat2',None)
if renameat2 is None: raise SystemExit(95)
renameat2.argtypes=(ctypes.c_int,ctypes.c_char_p,ctypes.c_int,ctypes.c_char_p,ctypes.c_uint)
renameat2.restype=ctypes.c_int
if renameat2(-100,os.fsencode(source),-100,os.fsencode(destination),1)!=0:
    error=ctypes.get_errno()
    raise SystemExit(96 if error in (errno.EEXIST,errno.ENOENT) else 97)
"""

REMOTE_EXCLUSIVE_WRITE = """import base64,os,stat,sys
directory,temporary,final,payload=sys.argv[1:5]
if temporary not in ('.result.tmp','.failure-result.tmp') or final!='result.json': raise SystemExit(101)
try: directory_fd=os.open(directory,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
except OSError: raise SystemExit(102)
directory_info=os.fstat(directory_fd)
if not stat.S_ISDIR(directory_info.st_mode) or stat.S_IMODE(directory_info.st_mode)!=0o700 or directory_info.st_uid!=os.getuid(): raise SystemExit(103)
for path in (temporary,final):
    try: os.stat(path,dir_fd=directory_fd,follow_symlinks=False)
    except FileNotFoundError: pass
    except OSError: raise SystemExit(104)
    else: raise SystemExit(105)
try: nofollow=os.O_NOFOLLOW
except AttributeError: raise SystemExit(106)
flags=os.O_WRONLY|os.O_CREAT|os.O_EXCL|nofollow
try: descriptor=os.open(temporary,flags,0o600,dir_fd=directory_fd)
except OSError: raise SystemExit(107)
try:
    data=base64.b64decode(payload,validate=True)
    view=memoryview(data)
    while view:
        written=os.write(descriptor,view)
        if written<=0: raise OSError()
        view=view[written:]
    os.fchmod(descriptor,0o600)
    os.fsync(descriptor)
finally: os.close(descriptor)
os.close(directory_fd)
"""

REMOTE_EXCLUSIVE_INGRESS = """import hashlib,os,stat,sys
directory,name,size_text,digest=sys.argv[1:5]
if name not in ('.wheel.part','.lock.part'): raise SystemExit(131)
size=int(size_text)
flags=os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW
try: directory_fd=os.open(directory,flags)
except OSError: raise SystemExit(132)
try:
    directory_info=os.fstat(directory_fd)
    if not stat.S_ISDIR(directory_info.st_mode) or stat.S_IMODE(directory_info.st_mode)!=0o700 or directory_info.st_uid!=os.getuid(): raise SystemExit(133)
    try: descriptor=os.open(name,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600,dir_fd=directory_fd)
    except OSError: raise SystemExit(134)
    total=0; calculated=hashlib.sha256()
    try:
        while True:
            block=sys.stdin.buffer.read(min(65536,size+1-total))
            if not block: break
            total+=len(block)
            if total>size: raise SystemExit(135)
            calculated.update(block)
            view=memoryview(block)
            while view:
                written=os.write(descriptor,view)
                if written<=0: raise SystemExit(136)
                view=view[written:]
        if total!=size or calculated.hexdigest()!=digest: raise SystemExit(137)
        os.fchmod(descriptor,0o600); os.fsync(descriptor)
    finally: os.close(descriptor)
finally: os.close(directory_fd)
"""

REMOTE_SOURCE_ABSENT = """import os,sys
try: os.lstat(sys.argv[1])
except FileNotFoundError: raise SystemExit(0)
except OSError: raise SystemExit(111)
raise SystemExit(112)
"""

REMOTE_EVIDENCE_PROBE = """import hashlib,os,stat,sys
directory,temporary,final,digest=sys.argv[1:5]
def entry(name,fd):
    try: return os.stat(name,dir_fd=fd,follow_symlinks=False)
    except FileNotFoundError: return None
    except OSError: return False
try: directory_fd=os.open(directory,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
except OSError: print('UNCERTAIN'); raise SystemExit(0)
try:
    temp_info=entry(temporary,directory_fd); final_info=entry(final,directory_fd)
    if temp_info is False or final_info is False:
        print('UNCERTAIN'); raise SystemExit(0)
    if temp_info is not None:
        print('NOT_PUBLISHED'); raise SystemExit(0)
    if final_info is None or not stat.S_ISREG(final_info.st_mode) or stat.S_IMODE(final_info.st_mode)!=0o600 or final_info.st_uid!=os.getuid():
        print('UNCERTAIN'); raise SystemExit(0)
    descriptor=os.open(final,os.O_RDONLY|os.O_NOFOLLOW,dir_fd=directory_fd)
    try:
        calculated=hashlib.sha256()
        while True:
            block=os.read(descriptor,65536)
            if not block: break
            calculated.update(block)
        os.fsync(descriptor)
    finally: os.close(descriptor)
    os.fsync(directory_fd)
    print('CONFIRMED' if calculated.hexdigest()==digest else 'UNCERTAIN')
finally: os.close(directory_fd)
"""

def remote_python(code,*arguments):
    return " ".join(map(shlex.quote,("/usr/bin/python3","-c",code,*arguments)))

def no_replace_publish_command(remote,source,destination):
    return remote_guard(remote)+"; "+remote_python(REMOTE_NO_REPLACE,source,destination)

def source_absent_command(path):
    return remote_python(REMOTE_SOURCE_ABSENT,path)

def ingress_command(remote,name,size,digest):
    return remote_guard(remote)+"; "+remote_python(REMOTE_EXCLUSIVE_INGRESS,remote,name,str(size),digest)

def evidence_payload(states,result,code,stage):
    doc={"schema_version":"1.0","action":"PE-4.0B.2a-B",**{k.lower():states[k] for k in STATE_KEYS},"evidence_state":"AWAITING_CONFIRMATION","result":result,"error_code":code,"failure_stage":stage,"rollback_recommended":False}
    return json.dumps(doc,sort_keys=True,separators=(",",":"))+"\n"

def evidence_prepare_command(remote,payload,temp_name):
    encoded=base64.b64encode(payload.encode("utf-8")).decode("ascii")
    return remote_guard(remote)+"; "+remote_python(REMOTE_EXCLUSIVE_WRITE,remote,temp_name,"result.json",encoded)

def evidence_publish_command(remote,temp_name):
    return no_replace_publish_command(remote,f"{remote}/{temp_name}",f"{remote}/result.json")

def evidence_confirm_command(remote,payload_sha256,temp_name):
    return remote_guard(remote)+"; "+remote_python(REMOTE_EVIDENCE_PROBE,remote,temp_name,"result.json",payload_sha256)

def artifact_confirm_command(remote,partial,final,size,digest):
    qpartial,qfinal,qdir=map(shlex.quote,(partial,final,remote))
    return remote_guard(remote)+f"; test -f {qfinal} || exit 121; test ! -L {qfinal} || exit 122; test \"$(stat -c %U -- {qfinal})\" = {OWNER} || exit 123; test \"$(stat -c %a -- {qfinal})\" = 600 || exit 124; test \"$(stat -c %s -- {qfinal})\" = {size} || exit 125; test \"$(sha256sum -- {qfinal} | cut -d' ' -f1)\" = {digest} || exit 126; sync -f {qfinal} || exit 127; sync -f {qdir} || exit 128; "+source_absent_command(partial)

def publish_and_confirm(runner,ssh,remote,partial,final,size,digest,stage):
    try:
        runner(ssh+[no_replace_publish_command(remote,partial,final)],stage+"_PUBLICATION",timeout=20,max_output=4096)
    except Failure:
        runner(ssh+[artifact_confirm_command(remote,partial,final,size,digest)],stage+"_CONFIRMATION",timeout=20,max_output=4096)
        return
    runner(ssh+[artifact_confirm_command(remote,partial,final,size,digest)],stage+"_CONFIRMATION",timeout=20,max_output=4096)

def publish_evidence(runner,ssh,remote,states,result,code,stage,temp_name):
    payload=evidence_payload(states,result,code,stage)
    digest=hashlib.sha256(payload.encode("utf-8")).hexdigest()
    runner(ssh+[evidence_prepare_command(remote,payload,temp_name)],"EVIDENCE_PREPARATION",timeout=20,max_output=4096)
    try: runner(ssh+[evidence_publish_command(remote,temp_name)],"EVIDENCE_RENAME",timeout=20,max_output=4096)
    except Failure: pass
    try:
        confirmation=runner(ssh+[evidence_confirm_command(remote,digest,temp_name)],"EVIDENCE_CONFIRMATION",timeout=20,max_output=4096).stdout.strip()
    except Failure as exc:
        states["EVIDENCE_STATE"]="UNCERTAIN"
        raise Failure("EVIDENCE_PUBLICATION_UNCERTAIN",exc.stage)
    if confirmation not in EVIDENCE_STATES: confirmation="UNCERTAIN"
    states["EVIDENCE_STATE"]=confirmation
    if confirmation!="CONFIRMED":
        raise Failure("EVIDENCE_NOT_PUBLISHED" if confirmation=="NOT_PUBLISHED" else "EVIDENCE_PUBLICATION_UNCERTAIN","EVIDENCE_CONFIRMATION")

def execute(commit,runner=run_bounded,transport_validator=validate_local_transport):
    states={k:False for k in STATE_KEYS}; states["EVIDENCE_STATE"]="NOT_PUBLISHED"; remote=""; evidence_attempted=False
    ssh_tool,known_hosts,identity=transport_validator(); options=transport_options(known_hosts,identity)
    ssh=[str(ssh_tool),*options,f"{OWNER}@{PI3_IPV4}"]
    try:
        wheel,lock=local_inputs(commit)
        create=("umask 077; d=$(mktemp -d /tmp/hioc-pe4-artifact-transfer-XXXXXXXX) || exit 31; test -d \"$d\" || exit 32; test ! -L \"$d\" || exit 33; "+f"test \"$(stat -c %U -- \"$d\")\" = {OWNER} || exit 34; "+"test \"$(stat -c %a -- \"$d\")\" = 700 || exit 35; test -z \"$(find \"$d\" -mindepth 1 -maxdepth 1 -print -quit)\" || exit 36; printf '%s\\n' \"$d\"")
        remote=runner(ssh+[create],"REMOTE_STAGING",timeout=15,max_output=4096).stdout.strip()
        if not TRANSFER_RE.fullmatch(remote): raise Failure("REMOTE_STAGING_INVALID","REMOTE_STAGING")
        states["REMOTE_STAGING_CREATED"]=True
        runner(ssh+[ingress_command(remote,".wheel.part",WHEEL_SIZE,WHEEL_SHA256)],"WHEEL_TRANSFER",timeout=60,max_output=8192,stdin_path=wheel)
        qpart=shlex.quote(f"{remote}/.wheel.part")
        check=remote_guard(remote)+f"; test -f {qpart} || exit 51; test ! -L {qpart} || exit 52; chmod 600 {qpart} || exit 53; test \"$(stat -c %U -- {qpart})\" = {OWNER} || exit 54; test \"$(stat -c %a -- {qpart})\" = 600 || exit 55; test \"$(stat -c %s -- {qpart})\" = {WHEEL_SIZE} || exit 56; test \"$(sha256sum -- {qpart} | cut -d' ' -f1)\" = {WHEEL_SHA256} || exit 57; sync -f {qpart} || exit 58"
        runner(ssh+[check],"REMOTE_ARTIFACT_PARTIAL",timeout=30,max_output=4096); states["WHEEL_TRANSFERRED"]=True
        publish_and_confirm(runner,ssh,remote,f"{remote}/.wheel.part",f"{remote}/{WHEEL_NAME}",WHEEL_SIZE,WHEEL_SHA256,"REMOTE_ARTIFACT"); states["REMOTE_ARTIFACT_VERIFIED"]=True
        runner(ssh+[ingress_command(remote,".lock.part",LOCAL_LOCK.stat().st_size,LOCK_SHA256)],"LOCK_TRANSFER",timeout=30,max_output=8192,stdin_path=lock)
        qpart=shlex.quote(f"{remote}/.lock.part")
        check=remote_guard(remote)+f"; test -f {qpart} || exit 61; test ! -L {qpart} || exit 62; chmod 600 {qpart} || exit 63; test \"$(stat -c %U -- {qpart})\" = {OWNER} || exit 64; test \"$(stat -c %a -- {qpart})\" = 600 || exit 65; test \"$(sha256sum -- {qpart} | cut -d' ' -f1)\" = {LOCK_SHA256} || exit 66; sync -f {qpart} || exit 67"
        runner(ssh+[check],"REMOTE_LOCK_PARTIAL",timeout=20,max_output=4096); states["LOCK_TRANSFERRED"]=True
        publish_and_confirm(runner,ssh,remote,f"{remote}/.lock.part",f"{remote}/requirements-pe4.lock",LOCAL_LOCK.stat().st_size,LOCK_SHA256,"REMOTE_LOCK"); states["REMOTE_LOCK_VERIFIED"]=True
        evidence_attempted=True; publish_evidence(runner,ssh,remote,states,"PASS","NONE","COMPLETE",".result.tmp")
        return states,remote
    except Failure as exc:
        if remote and states["REMOTE_STAGING_CREATED"] and not evidence_attempted:
            try:
                evidence_attempted=True; publish_evidence(runner,ssh,remote,states,"FAIL",exc.code,exc.stage,".failure-result.tmp")
            except Failure: pass
        exc.states,exc.remote=states,remote; raise

def emit(states,result,code,stage,remote=""):
    for key in STATE_KEYS: print(f"{key}={'TRUE' if states[key] else 'FALSE'}")
    print(f"EVIDENCE_STATE={states['EVIDENCE_STATE']}")
    print(f"ACTION_B={'COMPLETE' if result=='PASS' else 'NOT_COMPLETE'}"); terminal(result,code,stage,False)
    if remote: print(f"TRANSFER_DIRECTORY={remote}")

def main():
    states={k:False for k in STATE_KEYS}; states["EVIDENCE_STATE"]="NOT_PUBLISHED"
    try:
        states,remote=execute(parse_cli(sys.argv[1:])); emit(states,"PASS","NONE","COMPLETE",remote)
    except Failure as exc:
        emit(getattr(exc,"states",states),"FAIL",exc.code,exc.stage,getattr(exc,"remote","")); raise SystemExit(1)
    except Exception:
        emit(states,"FAIL","UNEXPECTED_ERROR","UNEXPECTED"); raise SystemExit(1)

if __name__=="__main__": main()
