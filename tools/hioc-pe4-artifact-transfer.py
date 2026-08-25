#!/usr/bin/env python3
"""PE-4.0B.2a-B: transfer the frozen wheel and lock to private PI3 staging."""
from __future__ import annotations
import base64, hashlib, json, pathlib, re, shlex, sys
from hioc_pe4_runtime_common import *

TOOL_RELATIVE="tools/hioc-pe4-artifact-transfer.py"
SOURCE_RELATIVES=(TOOL_RELATIVE,"tools/hioc_pe4_runtime_common.py","requirements-pe4.lock")
STATE_KEYS=("REMOTE_STAGING_CREATED","WHEEL_TRANSFERRED","LOCK_TRANSFERRED","REMOTE_ARTIFACT_VERIFIED","REMOTE_LOCK_VERIFIED","EVIDENCE_PUBLISHED")
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
try: directory_info=os.lstat(directory)
except OSError: raise SystemExit(101)
if not stat.S_ISDIR(directory_info.st_mode): raise SystemExit(102)
for path in (temporary,final):
    try: os.lstat(path)
    except FileNotFoundError: pass
    except OSError: raise SystemExit(103)
    else: raise SystemExit(104)
try: nofollow=os.O_NOFOLLOW
except AttributeError: raise SystemExit(105)
flags=os.O_WRONLY|os.O_CREAT|os.O_EXCL|nofollow
try: descriptor=os.open(temporary,flags,0o600)
except OSError: raise SystemExit(106)
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
"""

REMOTE_SOURCE_ABSENT = """import os,sys
try: os.lstat(sys.argv[1])
except FileNotFoundError: raise SystemExit(0)
except OSError: raise SystemExit(111)
raise SystemExit(112)
"""

def remote_python(code,*arguments):
    return " ".join(map(shlex.quote,("/usr/bin/python3","-c",code,*arguments)))

def no_replace_publish_command(remote,source,destination):
    return remote_guard(remote)+"; "+remote_python(REMOTE_NO_REPLACE,source,destination)

def source_absent_command(path):
    return remote_python(REMOTE_SOURCE_ABSENT,path)

def evidence_payload(states,result,code,stage):
    doc={"schema_version":"1.0","action":"PE-4.0B.2a-B",**{k.lower():states[k] for k in STATE_KEYS},"result":result,"error_code":code,"failure_stage":stage,"rollback_recommended":False}
    return json.dumps(doc,sort_keys=True,separators=(",",":"))+"\n"

def evidence_prepare_command(remote,payload,temp_name):
    temporary,final=f"{remote}/{temp_name}",f"{remote}/result.json"
    encoded=base64.b64encode(payload.encode("utf-8")).decode("ascii")
    return remote_guard(remote)+"; "+remote_python(REMOTE_EXCLUSIVE_WRITE,remote,temporary,final,encoded)

def evidence_publish_command(remote,temp_name):
    return no_replace_publish_command(remote,f"{remote}/{temp_name}",f"{remote}/result.json")

def evidence_confirm_command(remote,payload_sha256,temp_name):
    qdir,qresult=map(shlex.quote,(remote,f"{remote}/result.json"))
    temporary=f"{remote}/{temp_name}"
    return remote_guard(remote)+f"; test -f {qresult} || exit 81; test ! -L {qresult} || exit 82; test \"$(stat -c %U -- {qresult})\" = {OWNER} || exit 83; test \"$(stat -c %a -- {qresult})\" = 600 || exit 84; test \"$(sha256sum -- {qresult} | cut -d' ' -f1)\" = {payload_sha256} || exit 85; sync -f {qresult} || exit 86; sync -f {qdir} || exit 87; "+source_absent_command(temporary)

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
    published={**states,"EVIDENCE_PUBLISHED":True}
    payload=evidence_payload(published,result,code,stage)
    digest=hashlib.sha256(payload.encode("utf-8")).hexdigest()
    runner(ssh+[evidence_prepare_command(remote,payload,temp_name)],"EVIDENCE_PREPARATION",timeout=20,max_output=4096)
    try:
        runner(ssh+[evidence_publish_command(remote,temp_name)],"EVIDENCE_RENAME",timeout=20,max_output=4096)
    except Failure:
        runner(ssh+[evidence_confirm_command(remote,digest,temp_name)],"EVIDENCE_CONFIRMATION",timeout=20,max_output=4096)
        return
    runner(ssh+[evidence_confirm_command(remote,digest,temp_name)],"EVIDENCE_CONFIRMATION",timeout=20,max_output=4096)

def execute(commit,runner=run_bounded,resolver=windows_openssh_tool,material_resolver=windows_openssh_material):
    states={k:False for k in STATE_KEYS}; remote=""; evidence_attempted=False
    known_hosts,identity=material_resolver(); options=transport_options(known_hosts,identity)
    ssh=[str(resolver("ssh")),*options,f"{OWNER}@{PI3_IPV4}"]; scp=[str(resolver("scp")),*options]
    try:
        wheel,lock=local_inputs(commit)
        create=("umask 077; d=$(mktemp -d /tmp/hioc-pe4-artifact-transfer-XXXXXXXX) || exit 31; test -d \"$d\" || exit 32; test ! -L \"$d\" || exit 33; "+f"test \"$(stat -c %U -- \"$d\")\" = {OWNER} || exit 34; "+"test \"$(stat -c %a -- \"$d\")\" = 700 || exit 35; test -z \"$(find \"$d\" -mindepth 1 -maxdepth 1 -print -quit)\" || exit 36; printf '%s\\n' \"$d\"")
        remote=runner(ssh+[create],"REMOTE_STAGING",timeout=15,max_output=4096).stdout.strip()
        if not TRANSFER_RE.fullmatch(remote): raise Failure("REMOTE_STAGING_INVALID","REMOTE_STAGING")
        states["REMOTE_STAGING_CREATED"]=True
        runner(scp+[str(wheel),f"{OWNER}@{PI3_IPV4}:{remote}/.wheel.part"],"WHEEL_TRANSFER",timeout=60,max_output=8192); states["WHEEL_TRANSFERRED"]=True
        runner(scp+[str(lock),f"{OWNER}@{PI3_IPV4}:{remote}/.lock.part"],"LOCK_TRANSFER",timeout=30,max_output=8192); states["LOCK_TRANSFERRED"]=True
        qpart=shlex.quote(f"{remote}/.wheel.part")
        check=remote_guard(remote)+f"; test -f {qpart} || exit 51; test ! -L {qpart} || exit 52; chmod 600 {qpart} || exit 53; test \"$(stat -c %U -- {qpart})\" = {OWNER} || exit 54; test \"$(stat -c %a -- {qpart})\" = 600 || exit 55; test \"$(stat -c %s -- {qpart})\" = {WHEEL_SIZE} || exit 56; test \"$(sha256sum -- {qpart} | cut -d' ' -f1)\" = {WHEEL_SHA256} || exit 57; sync -f {qpart} || exit 58"
        runner(ssh+[check],"REMOTE_ARTIFACT_PARTIAL",timeout=30,max_output=4096)
        publish_and_confirm(runner,ssh,remote,f"{remote}/.wheel.part",f"{remote}/{WHEEL_NAME}",WHEEL_SIZE,WHEEL_SHA256,"REMOTE_ARTIFACT"); states["REMOTE_ARTIFACT_VERIFIED"]=True
        qpart=shlex.quote(f"{remote}/.lock.part")
        check=remote_guard(remote)+f"; test -f {qpart} || exit 61; test ! -L {qpart} || exit 62; chmod 600 {qpart} || exit 63; test \"$(stat -c %U -- {qpart})\" = {OWNER} || exit 64; test \"$(stat -c %a -- {qpart})\" = 600 || exit 65; test \"$(sha256sum -- {qpart} | cut -d' ' -f1)\" = {LOCK_SHA256} || exit 66; sync -f {qpart} || exit 67"
        runner(ssh+[check],"REMOTE_LOCK_PARTIAL",timeout=20,max_output=4096)
        publish_and_confirm(runner,ssh,remote,f"{remote}/.lock.part",f"{remote}/requirements-pe4.lock",LOCAL_LOCK.stat().st_size,LOCK_SHA256,"REMOTE_LOCK"); states["REMOTE_LOCK_VERIFIED"]=True
        evidence_attempted=True; publish_evidence(runner,ssh,remote,states,"PASS","NONE","COMPLETE",".result.tmp"); states["EVIDENCE_PUBLISHED"]=True
        return states,remote
    except Failure as exc:
        if remote and states["REMOTE_STAGING_CREATED"] and not evidence_attempted:
            try:
                evidence_attempted=True; publish_evidence(runner,ssh,remote,states,"FAIL",exc.code,exc.stage,".failure-result.tmp"); states["EVIDENCE_PUBLISHED"]=True
            except Failure: pass
        exc.states,exc.remote=states,remote; raise

def emit(states,result,code,stage,remote=""):
    for key in STATE_KEYS: print(f"{key}={'TRUE' if states[key] else 'FALSE'}")
    print(f"ACTION_B={'COMPLETE' if result=='PASS' else 'NOT_COMPLETE'}"); terminal(result,code,stage,False)
    if remote: print(f"TRANSFER_DIRECTORY={remote}")

def main():
    states={k:False for k in STATE_KEYS}
    try:
        states,remote=execute(parse_cli(sys.argv[1:])); emit(states,"PASS","NONE","COMPLETE",remote)
    except Failure as exc:
        emit(getattr(exc,"states",states),"FAIL",exc.code,exc.stage,getattr(exc,"remote","")); raise SystemExit(1)
    except Exception:
        emit(states,"FAIL","UNEXPECTED_ERROR","UNEXPECTED"); raise SystemExit(1)

if __name__=="__main__": main()
