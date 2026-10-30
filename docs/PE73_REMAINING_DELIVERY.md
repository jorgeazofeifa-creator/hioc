# PE-7.3 remaining trust and disabled Home Assistant delivery

This is the operator execution package for the already accepted PE-7 architecture.
PE73_STATUS=IN_PROGRESS; PE74_STATUS=NOT_AUTHORIZED. Run one numbered operation at a
time, return its sanitized result and exit status, and stop on any nonzero status or
unexpected result. Do not repeat a partially completed operation. Operations7 and8
are a coordinated pair: leave the finite foreground PI3 observer open while running
the PI5 publisher in its separate Terminal. This is not a service or activation.

The successful PI3 transaction050d0241fa67426c92e1ffe88a95817b and promoted baseline
a1b692bad44745feabcace25981bf69b are preserved. None of these commands reinstalls its
13 artifacts, changes cron, rewrites the baseline or accesses its historical journal.
Fresh current-baseline/runtime checks during the HA guard are continuity safeguards.

## Prerequisites and scope

- PI3: nutandpihole, jazofv1,1000:1000, accepted isolated environment at
  /home/jazofv1/.hioc-pe73-provision-environment. PI5: HA Terminal, root, accepted
  isolated environment at /root/.hioc-pe73-provision-environment. Neither environment
  is installed, upgraded or modified. Ready-file/source/fingerprint drift stops.
- Manual CA signing alone uses the accepted root-owned environment
  /root/.hioc-pe73-ca-signing-environment and vault /root/.hioc-pe73-ca-custody.
  Sudo is limited to that established root-custody boundary. It never executes a
  user-owned interpreter as root. No CA service, automatic issuance or renewal.
- Existing strict-host-key, noninteractive authenticated PI5-to-PI3 SSH must work.
  No passwords/tokens/keys are acquired or exported. Only public CSR/certificates and
  the existing design's CA/client chain/shared32-byte HMAC bundle cross that pipe;
  the PI5 client private key never leaves PI5 and the CA key never leaves root custody.
- Operation1 asks locally for the actual approved disabled product port, temporary
  guard port, certificate subjects/validity and existing HTTPS frontend origin.
  Actor ID and explicitly granted operations are entered privately. These facts
  remain unbound until entered; no values are invented or requested in chat.
  The accepted population architecture/amendment is selected automatically; no
  exact-ID-versus-population decision, hash copying or operation-ID entry is required.
- The frontend origin must already have valid system-trusted HTTPS resolving to
 192.168.100.251. No CA is added to system trust and no frontend transport is changed.
  A credential-free TLS/actual-peer preflight occurs before HA publication; the exact
  /local/hioc-asset-editor.js content is checked after publication and before API writes.
- Keep manual Asset/classification/administrative callers and other deployment or
  Dashboard editors out of this bounded window. Native scans/leases remain mandatory;
  procedural responsibility does not prove universal exclusion of cached modules,
  retained descriptors or privileged/uncooperative callers. No process termination,
  cron exclusion, scheduler restoration or automatic retry is performed here.

The code bundle is public source and six immutable HA payload/reference artifacts,
not production configuration or credentials. Each initial command verifies a fixed
Git blob, archive SHA-256, manifest and every source file before execution. It needs
no unpublished repository files on either Pi and assumes no current directory.
An incomplete/unsafe existing toolkit is retained and refused, never cleaned.
The actual production data are held in new0700 role-owned private parents with0600
single-link files and existing no-follow/ACL/ancestry/readback protections.

## Production compatibility correction: preparation stopped before trust creation

OPERATOR_SUPPLIED, failed release707ce936571f749b24d76f03cd7ba641f231c8fb:
prepare-backend returned FAIL_STOP_PE73_COMPLETION, generic
INPUT_IDENTITY_CAPABILITY_OR_UNCERTAIN_OPERATION, exit1. Toolkit and accepted
UID1000 environment existed with safe observed modes; inspected toolkit/runtime
sessions were absent. The existing schema1 ready seal passed UID/prefix/schema/
Python-version/source-Python checks, then FileNotFoundError occurred. Neither
tools/pe73_provision_environment.py nor tools/pe73_pi3_provision_environment.py
existed in that environment or its sealed inventory. No retry was performed.

IMMUTABLE_REPOSITORY_FACT: the accepted PI3 profile at
7027ca033fb0b8f2839ba1f3f65893d0c25d001f (SHA256
f55543e7207dc7bd9b23e7262f1b17c17fcc568afdf64d8aad6335321f6f93f1)
loads the engine at513d511fe255e11a875145543f62fa5dca2169a1 in memory.
The original profile implementation was introduced at
39b8b239c8b2399d984ac5c6be1436a5e49e1558. Accepted setup/source identity and
OPERATOR_SUPPLIED PASS are retained in the existing implementation history.
The installer prepare() stores only the seven TOOLKIT sources,
wheels, locked requirements and venv before fingerprinting every non-ready object.
It never stores either installer. PI5 uses the same seven-tool inventory; the root
CA custody installer deliberately adds both installer/profile objects. Therefore
the old completion environment() reaches the missing engine read before policy
input, runtime_material(), context creation or create_parent(). This reproduces
the concrete compatibility failure path; the failed process supplied no traceback,
so no claim is made that every other prerequisite was valid.

Selected Alternative A: the immutable current package already contains the exact
accepted engine (0e5d41b05729907ad1e629c8d77bf57a25890f600f7e2fcf29071c106fa0b3d7)
and the PI3 profile. Use their existing read-only fingerprint/ancestry algorithms
from that verified package, not an assumed copy inside the environment. The full
original ready seal, Python executable/version, dependency versions and every
file/link/mode identity still must match. Historical sealed toolkit source pins
are additionally checked against the original installer's TOOLKIT, with the exact
two CA-only additions. Never refresh or manufacture a ready seal. PI3 remains
1000:1000; PI5 and manual signing retain their distinct root-only targets. No
environment install, source copy, wheel installation, upgrade or mutation occurs.

Alternative B is unnecessary: no new cryptographic capability or dependency is
needed, and another venv adds installation/migration risk without resolving any
missing runtime API. Copying installer files into the existing environment is
rejected because it changes the accepted fingerprint. No alternate trust engine,
CA mechanism or permissive fallback is introduced.

Read-only environment diagnostics distinguish missing ready/sealed files, wrong
tool inventory/source identity, Python executable/version/dependency drift and
full fingerprint mismatch. Existing owner/mode/link/ACL/target/capability errors
remain fail-closed public codes. No private traceback or exception text is emitted.

The nine operations share this corrected role verification. Preparation/import/
backend completion/observer use PI3; client generation/completion/delivery/readback
use PI5; issuance alone uses root CA custody. Existing transfer source pins,
independent HA transaction namespace, disabled packets, native consumer checks,
backups and one-attempt publication remain unchanged. Unknown native prerequisites
are still evaluated on host. No operation is considered completed by these tests.

### First next step: compatibility and retained-state assessment only

Target PI3 NUT&PIHOLE, jazofv1, no sudo. Separate operator execution authorization
is required; this publication does not retry operation1. The command below installs
only a new immutable public code bundle, verifies the accepted environment, verifies
the exact failed toolkit, and performs bounded anchored home/runtime inventories.
It refuses any old/new session (including partial state), any hioc_pe73_ private
candidate, unsafe identity or changing inventory. It reads no credential contents,
generates no key, and creates no trust/session/CA material. It does not inspect or
replace the completed13 runtime payloads, scheduler or successful transaction.

Expected RESULT=PASS_READ_ONLY_PE73_PREPARATION_COMPATIBILITY and exit0; the receipt
must state preparation_executed=false, trust_material_created=false and
retained_preparation_candidates=0. It is a read-only assessment after the code-only
bootstrap, not preparation permission. Retain and review the receipt before a
separately authorized fresh prepare-backend. Any FAIL, existing/unknown state,
nonzero exit or lost acknowledgement stops; no automatic retry or cleanup. A later
assessment revalidates state; it never repeats the trust operation.

```bash
/usr/bin/python3 -I -S -B - <<'PE73'
UID=1000
HOME='/home/jazofv1'
ENV='/home/jazofv1/.hioc-pe73-provision-environment'
ACTION='assess-backend'
MSHA='752f6bb01ab45de58ef303636e8d69aae834c75f2c0ba05aba20e043cc60af8f'
BLOB='3ed00862304bd3e30efea7807f6a471b2d5ee37d'
SHA='81f8cb0013c49afce0fe40ce54bbfe80036e2110d6b777c85833200cb90ee8f0'
SIZE=159651
import base64,hashlib,io,json,os,pathlib,stat,subprocess,sys,urllib.request,zipfile
def need(ok):
    if not ok:raise ValueError("SOURCE_OR_PRIVATE_TOOLKIT_NOT_ESTABLISHED")
def sha(raw):return hashlib.sha256(raw).hexdigest()
try:
    need(sys.platform=="linux" and os.getuid()==os.geteuid()==os.getgid()==os.getegid()==UID)
    root=pathlib.Path(HOME)/(".hioc-pe73-completion-"+MSHA[:16])
    for parent in [pathlib.Path(HOME),*pathlib.Path(HOME).parents]:
        info=parent.lstat();need(stat.S_ISDIR(info.st_mode) and info.st_uid in (0,UID) and not stat.S_IMODE(info.st_mode)&0o7022);need(not ({"system.posix_acl_access","system.posix_acl_default"}&set(os.listxattr(parent,follow_symlinks=False))))
    if not os.path.lexists(root):
        url="https://api.github.com/repos/jorgeazofeifa-creator/hioc/git/blobs/"+BLOB
        request=urllib.request.Request(url,headers={"User-Agent":"HIOC-PE73-Immutable-Delivery","Accept":"application/vnd.github+json"})
        with urllib.request.build_opener(urllib.request.ProxyHandler({})).open(request,timeout=30) as response:
            need(response.geturl()==url);value=json.loads(response.read(4000001))
        need(value["sha"]==BLOB and value["encoding"]=="base64")
        raw=base64.b64decode(value["content"].replace("\n",""),validate=True)
        need(len(raw)==SIZE and sha(raw)==SHA)
        archive=zipfile.ZipFile(io.BytesIO(raw));names=archive.namelist()
        need(len(names)==len(set(names)) and sum(x.file_size for x in archive.infolist())<16000000)
        manifest=archive.read("tools/pe73-completion-package.json");need(sha(manifest)==MSHA)
        files=json.loads(manifest)["files"];need(set(names)==set(files)|{"tools/pe73-completion-package.json"})
        payloads={}
        for name in names:
            part=pathlib.PurePosixPath(name);need(not part.is_absolute() and ".." not in part.parts and "\\" not in name)
            need((archive.getinfo(name).external_attr>>16)&0o170000==0o100000)
            data=archive.read(name);need(len(data)<=1048576)
            if name in files:need(sha(data)==files[name]["sha256"])
            payloads[name]=data
        os.mkdir(root,0o700)
        for name,data in payloads.items():
            path=root/name;path.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
            fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
            try:
                with os.fdopen(fd,"wb",closefd=False) as stream:stream.write(data);stream.flush();os.fsync(fd)
            finally:os.close(fd)
        for directory in sorted([x for x in root.rglob("*") if x.is_dir()]+[root],key=lambda p:len(p.parts),reverse=True):
            fd=os.open(directory,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
            try:os.fsync(fd)
            finally:os.close(fd)
        fd=os.open(root.parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        try:os.fsync(fd)
        finally:os.close(fd)
    info=root.lstat();need(stat.S_ISDIR(info.st_mode) and info.st_uid==info.st_gid==UID and stat.S_IMODE(info.st_mode)==0o700)
    manifest=(root/"tools/pe73-completion-package.json").read_bytes();need(sha(manifest)==MSHA)
    for name,row in json.loads(manifest)["files"].items():
        path=root/name
        for parent in [path.parent,*path.parent.parents]:
            if parent==root.parent:break
            info=parent.lstat();need(stat.S_ISDIR(info.st_mode) and info.st_uid==UID and not stat.S_IMODE(info.st_mode)&0o7022);need(not ({"system.posix_acl_access","system.posix_acl_default"}&set(os.listxattr(parent,follow_symlinks=False))))
        info=path.lstat();need(stat.S_ISREG(info.st_mode) and info.st_nlink==1 and info.st_uid==info.st_gid==UID and stat.S_IMODE(info.st_mode)==0o600 and sha(path.read_bytes())==row["sha256"])
    command=[ENV+"/venv/bin/python3","-I","-B",str(root/"tools/pe73_completion.py"),ACTION,"--manifest-sha",MSHA]
    result=subprocess.run(command,check=False,close_fds=True)
    raise SystemExit(result.returncode)
except Exception:
    print(json.dumps({"RESULT":"FAIL_STOP_IMMUTABLE_TOOLKIT_OR_ENVIRONMENT","automatic_retry":False,"retained_state":"PRESERVED","STOP_REQUIRED":True}))
    raise SystemExit(1)
PE73
pe73_status=$?
printf "PE73_EXIT_STATUS=%s\n" "$pe73_status"
```

The subsequent nine commands below are prepared, not an instruction to execute
them now. Operation1 reruns the complete fresh admission check before generating
anything; session absence alone is insufficient. Each mutation is single-attempt
and non-repeatable after failure or uncertain acknowledgement. Return one receipt
and status at a time. The failed toolkit/environment remain unchanged.

| Operation | User / privilege | Persistent state / expected status / next permitted action |
| --- | --- | --- |
|1 prepare-backend|PI3 jazofv1, no sudo|New UID1000 private plan/server key/CSR/HMAC and toolkit session; PASS_PI3_TRUST_REQUEST_PREPARATION/0; only then2.|
|2 sign-server + import-server|PI3 root signing only via sudo, UID1000 importer|New encrypted root CA/server issuance, public cert imported; both statuses0, PASS_PUBLIC_CERTIFICATE_IMPORTED; then3.|
|3 ha-request|PI5 Terminal root, no sudo|Local private client key/CSR/session, public CSR transferred; PASS_PI5_LOCAL_CLIENT_KEY_REQUEST/0; then4.|
|4 sign-client + import-client|PI3 root signing only via sudo, UID1000 importer|Same existing CA, client issuance/public cert import; both statuses0, PASS_PUBLIC_CERTIFICATE_IMPORTED; then5.|
|5 complete-backend|PI3 jazofv1, no sudo|Inactive packet and matching transfer bundle; PASS_RUNTIME_DISABLED_TRUST_COMPLETION/0; then6.|
|6 ha-complete|PI5 Terminal root, no sudo|Matching inactive trust files/packet, local key retained; PASS_HA_DISABLED_TRUST_PROVISIONING/0; then7.|
|7 guard-backend|PI3 jazofv1, no sudo|Private finite observer lease; WAITING is not completion; paired8 then PASS_FINITE_PE73_TRUST_GUARD/0.|
|8 deliver-ha|PI5 Terminal root, no sudo|Exact private transaction/backups/exports, four pinned files, own resource/additive card; PASS_PE73_HA_DELIVERED_DISABLED/0; then9.|
|9 verify-ha|PI5 Terminal root, no sudo|Read-only terminal verification, no new lease; PASS_PE73_HA_INDEPENDENT_INSTALLATION_VERIFICATION/0; return evidence for governance closure.|

No mutation step is automatically repeated or recovered. Operation9 may reobserve
only an unchanged valid terminal state. No migration, activation, product service,
credential reuse, baseline replacement, cron operation or PE-7.4 authority exists.

## Operations

### 1. Prepare PI3 runtime trust requests

Target: **PI3 NUT&PIHOLE / jazofv1**.

Creates only the new private plan, runtime server key/CSR and32-byte HMAC. No CA key, certificate issuance, runtime module or scheduler change. Expected RESULT=PASS_PI3_TRUST_REQUEST_PREPARATION. New private names and references are generated internally.

```bash
/usr/bin/python3 -I -S -B - <<'PE73'
UID=1000
HOME='/home/jazofv1'
ENV='/home/jazofv1/.hioc-pe73-provision-environment'
ACTION='prepare-backend'
MSHA='752f6bb01ab45de58ef303636e8d69aae834c75f2c0ba05aba20e043cc60af8f'
BLOB='3ed00862304bd3e30efea7807f6a471b2d5ee37d'
SHA='81f8cb0013c49afce0fe40ce54bbfe80036e2110d6b777c85833200cb90ee8f0'
SIZE=159651
import base64,hashlib,io,json,os,pathlib,stat,subprocess,sys,urllib.request,zipfile
def need(ok):
    if not ok:raise ValueError("SOURCE_OR_PRIVATE_TOOLKIT_NOT_ESTABLISHED")
def sha(raw):return hashlib.sha256(raw).hexdigest()
try:
    need(sys.platform=="linux" and os.getuid()==os.geteuid()==os.getgid()==os.getegid()==UID)
    root=pathlib.Path(HOME)/(".hioc-pe73-completion-"+MSHA[:16])
    for parent in [pathlib.Path(HOME),*pathlib.Path(HOME).parents]:
        info=parent.lstat();need(stat.S_ISDIR(info.st_mode) and info.st_uid in (0,UID) and not stat.S_IMODE(info.st_mode)&0o7022);need(not ({"system.posix_acl_access","system.posix_acl_default"}&set(os.listxattr(parent,follow_symlinks=False))))
    if not os.path.lexists(root):
        url="https://api.github.com/repos/jorgeazofeifa-creator/hioc/git/blobs/"+BLOB
        request=urllib.request.Request(url,headers={"User-Agent":"HIOC-PE73-Immutable-Delivery","Accept":"application/vnd.github+json"})
        with urllib.request.build_opener(urllib.request.ProxyHandler({})).open(request,timeout=30) as response:
            need(response.geturl()==url);value=json.loads(response.read(4000001))
        need(value["sha"]==BLOB and value["encoding"]=="base64")
        raw=base64.b64decode(value["content"].replace("\n",""),validate=True)
        need(len(raw)==SIZE and sha(raw)==SHA)
        archive=zipfile.ZipFile(io.BytesIO(raw));names=archive.namelist()
        need(len(names)==len(set(names)) and sum(x.file_size for x in archive.infolist())<16000000)
        manifest=archive.read("tools/pe73-completion-package.json");need(sha(manifest)==MSHA)
        files=json.loads(manifest)["files"];need(set(names)==set(files)|{"tools/pe73-completion-package.json"})
        payloads={}
        for name in names:
            part=pathlib.PurePosixPath(name);need(not part.is_absolute() and ".." not in part.parts and "\\" not in name)
            need((archive.getinfo(name).external_attr>>16)&0o170000==0o100000)
            data=archive.read(name);need(len(data)<=1048576)
            if name in files:need(sha(data)==files[name]["sha256"])
            payloads[name]=data
        os.mkdir(root,0o700)
        for name,data in payloads.items():
            path=root/name;path.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
            fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
            try:
                with os.fdopen(fd,"wb",closefd=False) as stream:stream.write(data);stream.flush();os.fsync(fd)
            finally:os.close(fd)
        for directory in sorted([x for x in root.rglob("*") if x.is_dir()]+[root],key=lambda p:len(p.parts),reverse=True):
            fd=os.open(directory,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
            try:os.fsync(fd)
            finally:os.close(fd)
        fd=os.open(root.parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        try:os.fsync(fd)
        finally:os.close(fd)
    info=root.lstat();need(stat.S_ISDIR(info.st_mode) and info.st_uid==info.st_gid==UID and stat.S_IMODE(info.st_mode)==0o700)
    manifest=(root/"tools/pe73-completion-package.json").read_bytes();need(sha(manifest)==MSHA)
    for name,row in json.loads(manifest)["files"].items():
        path=root/name
        for parent in [path.parent,*path.parent.parents]:
            if parent==root.parent:break
            info=parent.lstat();need(stat.S_ISDIR(info.st_mode) and info.st_uid==UID and not stat.S_IMODE(info.st_mode)&0o7022);need(not ({"system.posix_acl_access","system.posix_acl_default"}&set(os.listxattr(parent,follow_symlinks=False))))
        info=path.lstat();need(stat.S_ISREG(info.st_mode) and info.st_nlink==1 and info.st_uid==info.st_gid==UID and stat.S_IMODE(info.st_mode)==0o600 and sha(path.read_bytes())==row["sha256"])
    command=[ENV+"/venv/bin/python3","-I","-B",str(root/"tools/pe73_completion.py"),ACTION,"--manifest-sha",MSHA]
    result=subprocess.run(command,check=False,close_fds=True)
    raise SystemExit(result.returncode)
except Exception:
    print(json.dumps({"RESULT":"FAIL_STOP_IMMUTABLE_TOOLKIT_OR_ENVIRONMENT","automatic_retry":False,"retained_state":"PRESERVED","STOP_REQUIRED":True}))
    raise SystemExit(1)
PE73
pe73_status=$?
printf "PE73_EXIT_STATUS=%s\n" "$pe73_status"
```

### 2. Manually initialize the offline CA and issue the server certificate

Target: **PI3 NUT&PIHOLE / manual root signing**.

Root custody must be prepared and unused for this new plan. The CA is encrypted in the root-only vault; only the public response crosses the local pipe to jazofv1. The importer independently validates plan/CSR/certificate bindings. Enter the CA passphrase only at the controlling terminal. Both pipeline statuses must be0 and the importer must report PASS_PUBLIC_CERTIFICATE_IMPORTED. Existing/partial CA state refuses; never rerun issuance.

```bash
sudo /usr/bin/python3 -I -S -B - <<'PE73' | /home/jazofv1/.hioc-pe73-provision-environment/venv/bin/python3 -I -B -c 'import hashlib,sys; p=sys.argv[1]; r=open(p,'"'"'rb'"'"').read(1048577); assert len(r)<=1048576 and hashlib.sha256(r).hexdigest()==sys.argv[2]; sys.argv=[p,*sys.argv[3:]]; exec(compile(r,p,'"'"'exec'"'"'),{'"'"'__name__'"'"':'"'"'__main__'"'"','"'"'__file__'"'"':p})' /home/jazofv1/.hioc-pe73-completion-752f6bb01ab45de5/tools/pe73_completion.py 2bcf0e5cec2d6b657a6970d39ef7d630b4c4c05c6d27469ae3b9e6c7d61e33c6 import-server --manifest-sha 752f6bb01ab45de58ef303636e8d69aae834c75f2c0ba05aba20e043cc60af8f
UID=0
HOME='/root'
ENV='/root/.hioc-pe73-ca-signing-environment'
ACTION='sign-server'
MSHA='752f6bb01ab45de58ef303636e8d69aae834c75f2c0ba05aba20e043cc60af8f'
BLOB='3ed00862304bd3e30efea7807f6a471b2d5ee37d'
SHA='81f8cb0013c49afce0fe40ce54bbfe80036e2110d6b777c85833200cb90ee8f0'
SIZE=159651
import base64,hashlib,io,json,os,pathlib,stat,subprocess,sys,urllib.request,zipfile
def need(ok):
    if not ok:raise ValueError("SOURCE_OR_PRIVATE_TOOLKIT_NOT_ESTABLISHED")
def sha(raw):return hashlib.sha256(raw).hexdigest()
try:
    need(sys.platform=="linux" and os.getuid()==os.geteuid()==os.getgid()==os.getegid()==UID)
    root=pathlib.Path(HOME)/(".hioc-pe73-completion-"+MSHA[:16])
    for parent in [pathlib.Path(HOME),*pathlib.Path(HOME).parents]:
        info=parent.lstat();need(stat.S_ISDIR(info.st_mode) and info.st_uid in (0,UID) and not stat.S_IMODE(info.st_mode)&0o7022);need(not ({"system.posix_acl_access","system.posix_acl_default"}&set(os.listxattr(parent,follow_symlinks=False))))
    if not os.path.lexists(root):
        url="https://api.github.com/repos/jorgeazofeifa-creator/hioc/git/blobs/"+BLOB
        request=urllib.request.Request(url,headers={"User-Agent":"HIOC-PE73-Immutable-Delivery","Accept":"application/vnd.github+json"})
        with urllib.request.build_opener(urllib.request.ProxyHandler({})).open(request,timeout=30) as response:
            need(response.geturl()==url);value=json.loads(response.read(4000001))
        need(value["sha"]==BLOB and value["encoding"]=="base64")
        raw=base64.b64decode(value["content"].replace("\n",""),validate=True)
        need(len(raw)==SIZE and sha(raw)==SHA)
        archive=zipfile.ZipFile(io.BytesIO(raw));names=archive.namelist()
        need(len(names)==len(set(names)) and sum(x.file_size for x in archive.infolist())<16000000)
        manifest=archive.read("tools/pe73-completion-package.json");need(sha(manifest)==MSHA)
        files=json.loads(manifest)["files"];need(set(names)==set(files)|{"tools/pe73-completion-package.json"})
        payloads={}
        for name in names:
            part=pathlib.PurePosixPath(name);need(not part.is_absolute() and ".." not in part.parts and "\\" not in name)
            need((archive.getinfo(name).external_attr>>16)&0o170000==0o100000)
            data=archive.read(name);need(len(data)<=1048576)
            if name in files:need(sha(data)==files[name]["sha256"])
            payloads[name]=data
        os.mkdir(root,0o700)
        for name,data in payloads.items():
            path=root/name;path.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
            fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
            try:
                with os.fdopen(fd,"wb",closefd=False) as stream:stream.write(data);stream.flush();os.fsync(fd)
            finally:os.close(fd)
        for directory in sorted([x for x in root.rglob("*") if x.is_dir()]+[root],key=lambda p:len(p.parts),reverse=True):
            fd=os.open(directory,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
            try:os.fsync(fd)
            finally:os.close(fd)
        fd=os.open(root.parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        try:os.fsync(fd)
        finally:os.close(fd)
    info=root.lstat();need(stat.S_ISDIR(info.st_mode) and info.st_uid==info.st_gid==UID and stat.S_IMODE(info.st_mode)==0o700)
    manifest=(root/"tools/pe73-completion-package.json").read_bytes();need(sha(manifest)==MSHA)
    for name,row in json.loads(manifest)["files"].items():
        path=root/name
        for parent in [path.parent,*path.parent.parents]:
            if parent==root.parent:break
            info=parent.lstat();need(stat.S_ISDIR(info.st_mode) and info.st_uid==UID and not stat.S_IMODE(info.st_mode)&0o7022);need(not ({"system.posix_acl_access","system.posix_acl_default"}&set(os.listxattr(parent,follow_symlinks=False))))
        info=path.lstat();need(stat.S_ISREG(info.st_mode) and info.st_nlink==1 and info.st_uid==info.st_gid==UID and stat.S_IMODE(info.st_mode)==0o600 and sha(path.read_bytes())==row["sha256"])
    command=[ENV+"/venv/bin/python3","-I","-B",str(root/"tools/pe73_completion.py"),ACTION,"--manifest-sha",MSHA]
    result=subprocess.run(command,check=False,close_fds=True)
    raise SystemExit(result.returncode)
except Exception:
    print(json.dumps({"RESULT":"FAIL_STOP_IMMUTABLE_TOOLKIT_OR_ENVIRONMENT","automatic_retry":False,"retained_state":"PRESERVED","STOP_REQUIRED":True}))
    raise SystemExit(1)
PE73
pe73_status=( "${PIPESTATUS[@]}" )
printf "PE73_SIGNER_EXIT=%s PE73_IMPORT_EXIT=%s\n" "${pe73_status[0]}" "${pe73_status[1]}"
```

### 3. Generate the PI5 client key locally and transfer only its CSR

Target: **PI5 HA / Terminal root**.

Enter only the existing PI3 SSH port locally. The authenticated pipe obtains the exact prepared plan and transfers the public CSR. Expected RESULT=PASS_PI5_LOCAL_CLIENT_KEY_REQUEST. The private client key remains on PI5.

```bash
/usr/bin/python3 -I -S -B - <<'PE73'
UID=0
HOME='/root'
ENV='/root/.hioc-pe73-provision-environment'
ACTION='ha-request'
MSHA='752f6bb01ab45de58ef303636e8d69aae834c75f2c0ba05aba20e043cc60af8f'
BLOB='3ed00862304bd3e30efea7807f6a471b2d5ee37d'
SHA='81f8cb0013c49afce0fe40ce54bbfe80036e2110d6b777c85833200cb90ee8f0'
SIZE=159651
import base64,hashlib,io,json,os,pathlib,stat,subprocess,sys,urllib.request,zipfile
def need(ok):
    if not ok:raise ValueError("SOURCE_OR_PRIVATE_TOOLKIT_NOT_ESTABLISHED")
def sha(raw):return hashlib.sha256(raw).hexdigest()
try:
    need(sys.platform=="linux" and os.getuid()==os.geteuid()==os.getgid()==os.getegid()==UID)
    root=pathlib.Path(HOME)/(".hioc-pe73-completion-"+MSHA[:16])
    for parent in [pathlib.Path(HOME),*pathlib.Path(HOME).parents]:
        info=parent.lstat();need(stat.S_ISDIR(info.st_mode) and info.st_uid in (0,UID) and not stat.S_IMODE(info.st_mode)&0o7022);need(not ({"system.posix_acl_access","system.posix_acl_default"}&set(os.listxattr(parent,follow_symlinks=False))))
    if not os.path.lexists(root):
        url="https://api.github.com/repos/jorgeazofeifa-creator/hioc/git/blobs/"+BLOB
        request=urllib.request.Request(url,headers={"User-Agent":"HIOC-PE73-Immutable-Delivery","Accept":"application/vnd.github+json"})
        with urllib.request.build_opener(urllib.request.ProxyHandler({})).open(request,timeout=30) as response:
            need(response.geturl()==url);value=json.loads(response.read(4000001))
        need(value["sha"]==BLOB and value["encoding"]=="base64")
        raw=base64.b64decode(value["content"].replace("\n",""),validate=True)
        need(len(raw)==SIZE and sha(raw)==SHA)
        archive=zipfile.ZipFile(io.BytesIO(raw));names=archive.namelist()
        need(len(names)==len(set(names)) and sum(x.file_size for x in archive.infolist())<16000000)
        manifest=archive.read("tools/pe73-completion-package.json");need(sha(manifest)==MSHA)
        files=json.loads(manifest)["files"];need(set(names)==set(files)|{"tools/pe73-completion-package.json"})
        payloads={}
        for name in names:
            part=pathlib.PurePosixPath(name);need(not part.is_absolute() and ".." not in part.parts and "\\" not in name)
            need((archive.getinfo(name).external_attr>>16)&0o170000==0o100000)
            data=archive.read(name);need(len(data)<=1048576)
            if name in files:need(sha(data)==files[name]["sha256"])
            payloads[name]=data
        os.mkdir(root,0o700)
        for name,data in payloads.items():
            path=root/name;path.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
            fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
            try:
                with os.fdopen(fd,"wb",closefd=False) as stream:stream.write(data);stream.flush();os.fsync(fd)
            finally:os.close(fd)
        for directory in sorted([x for x in root.rglob("*") if x.is_dir()]+[root],key=lambda p:len(p.parts),reverse=True):
            fd=os.open(directory,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
            try:os.fsync(fd)
            finally:os.close(fd)
        fd=os.open(root.parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        try:os.fsync(fd)
        finally:os.close(fd)
    info=root.lstat();need(stat.S_ISDIR(info.st_mode) and info.st_uid==info.st_gid==UID and stat.S_IMODE(info.st_mode)==0o700)
    manifest=(root/"tools/pe73-completion-package.json").read_bytes();need(sha(manifest)==MSHA)
    for name,row in json.loads(manifest)["files"].items():
        path=root/name
        for parent in [path.parent,*path.parent.parents]:
            if parent==root.parent:break
            info=parent.lstat();need(stat.S_ISDIR(info.st_mode) and info.st_uid==UID and not stat.S_IMODE(info.st_mode)&0o7022);need(not ({"system.posix_acl_access","system.posix_acl_default"}&set(os.listxattr(parent,follow_symlinks=False))))
        info=path.lstat();need(stat.S_ISREG(info.st_mode) and info.st_nlink==1 and info.st_uid==info.st_gid==UID and stat.S_IMODE(info.st_mode)==0o600 and sha(path.read_bytes())==row["sha256"])
    command=[ENV+"/venv/bin/python3","-I","-B",str(root/"tools/pe73_completion.py"),ACTION,"--manifest-sha",MSHA]
    result=subprocess.run(command,check=False,close_fds=True)
    raise SystemExit(result.returncode)
except Exception:
    print(json.dumps({"RESULT":"FAIL_STOP_IMMUTABLE_TOOLKIT_OR_ENVIRONMENT","automatic_retry":False,"retained_state":"PRESERVED","STOP_REQUIRED":True}))
    raise SystemExit(1)
PE73
pe73_status=$?
printf "PE73_EXIT_STATUS=%s\n" "$pe73_status"
```

### 4. Manually issue/import the client certificate

Target: **PI3 NUT&PIHOLE / manual root signing**.

Uses the same root-only CA and exact stored plan/CSR. No runtime key/HMAC is read by the signer. Both pipeline statuses must be0; importer RESULT=PASS_PUBLIC_CERTIFICATE_IMPORTED. No repeat after lost acknowledgement.

```bash
sudo /root/.hioc-pe73-ca-signing-environment/venv/bin/python3 -I -B -c 'import hashlib,sys; p=sys.argv[1]; r=open(p,'"'"'rb'"'"').read(1048577); assert len(r)<=1048576 and hashlib.sha256(r).hexdigest()==sys.argv[2]; sys.argv=[p,*sys.argv[3:]]; exec(compile(r,p,'"'"'exec'"'"'),{'"'"'__name__'"'"':'"'"'__main__'"'"','"'"'__file__'"'"':p})' /root/.hioc-pe73-completion-752f6bb01ab45de5/tools/pe73_completion.py 2bcf0e5cec2d6b657a6970d39ef7d630b4c4c05c6d27469ae3b9e6c7d61e33c6 sign-client --manifest-sha 752f6bb01ab45de58ef303636e8d69aae834c75f2c0ba05aba20e043cc60af8f | /home/jazofv1/.hioc-pe73-provision-environment/venv/bin/python3 -I -B -c 'import hashlib,sys; p=sys.argv[1]; r=open(p,'"'"'rb'"'"').read(1048577); assert len(r)<=1048576 and hashlib.sha256(r).hexdigest()==sys.argv[2]; sys.argv=[p,*sys.argv[3:]]; exec(compile(r,p,'"'"'exec'"'"'),{'"'"'__name__'"'"':'"'"'__main__'"'"','"'"'__file__'"'"':p})' /home/jazofv1/.hioc-pe73-completion-752f6bb01ab45de5/tools/pe73_completion.py 2bcf0e5cec2d6b657a6970d39ef7d630b4c4c05c6d27469ae3b9e6c7d61e33c6 import-client --manifest-sha 752f6bb01ab45de58ef303636e8d69aae834c75f2c0ba05aba20e043cc60af8f
pe73_status=( "${PIPESTATUS[@]}" )
printf "PE73_SIGNER_EXIT=%s PE73_IMPORT_EXIT=%s\n" "${pe73_status[0]}" "${pe73_status[1]}"
```

### 5. Complete inactive PI3 trust material

Target: **PI3 NUT&PIHOLE / jazofv1**.

Validates public chains/pins and writes the inactive independent backend packet and HA transfer bundle last. Expected RESULT=PASS_RUNTIME_DISABLED_TRUST_COMPLETION. No product adapter is started and no active runtime configuration is written.

```bash
/home/jazofv1/.hioc-pe73-provision-environment/venv/bin/python3 -I -B -c 'import hashlib,sys; p=sys.argv[1]; r=open(p,'"'"'rb'"'"').read(1048577); assert len(r)<=1048576 and hashlib.sha256(r).hexdigest()==sys.argv[2]; sys.argv=[p,*sys.argv[3:]]; exec(compile(r,p,'"'"'exec'"'"'),{'"'"'__name__'"'"':'"'"'__main__'"'"','"'"'__file__'"'"':p})' /home/jazofv1/.hioc-pe73-completion-752f6bb01ab45de5/tools/pe73_completion.py 2bcf0e5cec2d6b657a6970d39ef7d630b4c4c05c6d27469ae3b9e6c7d61e33c6 complete-backend --manifest-sha 752f6bb01ab45de58ef303636e8d69aae834c75f2c0ba05aba20e043cc60af8f
pe73_status=$?
printf "PE73_EXIT_STATUS=%s\n" "$pe73_status"
```

### 6. Complete inactive PI5 trust material

Target: **PI5 HA / Terminal root**.

Uses the authenticated pipe to obtain the matching chain/HMAC/independent ACL packet; validates its own local client key and writes the disabled packet last. Expected RESULT=PASS_HA_DISABLED_TRUST_PROVISIONING. No configuration.yaml change, integration reload or restart.

```bash
/root/.hioc-pe73-provision-environment/venv/bin/python3 -I -B -c 'import hashlib,sys; p=sys.argv[1]; r=open(p,'"'"'rb'"'"').read(1048577); assert len(r)<=1048576 and hashlib.sha256(r).hexdigest()==sys.argv[2]; sys.argv=[p,*sys.argv[3:]]; exec(compile(r,p,'"'"'exec'"'"'),{'"'"'__name__'"'"':'"'"'__main__'"'"','"'"'__file__'"'"':p})' /root/.hioc-pe73-completion-752f6bb01ab45de5/tools/pe73_completion.py 2bcf0e5cec2d6b657a6970d39ef7d630b4c4c05c6d27469ae3b9e6c7d61e33c6 ha-complete --manifest-sha 752f6bb01ab45de58ef303636e8d69aae834c75f2c0ba05aba20e043cc60af8f
pe73_status=$?
printf "PE73_EXIT_STATUS=%s\n" "$pe73_status"
```

### 7. Open the finite PI3 trust observer

Target: **PI3 NUT&PIHOLE / jazofv1, leave foreground session open**.

Freshly verifies current approved baseline/no active transaction, payload integrity, original scheduler, disabled PE-7 roles and native consumer conditions. It creates only its private observer lease and listens for one authenticated PI5 session. WAITING_FOR_ONE_AUTHENTICATED_PI5_SESSION is readiness, not success. Leave this terminal open, then execute operation8 on PI5. Expected terminal RESULT=PASS_FINITE_PE73_TRUST_GUARD after authenticated FINISH; no consumer release or automatic lease deletion occurs.

```bash
/home/jazofv1/.hioc-pe73-provision-environment/venv/bin/python3 -I -B -c 'import hashlib,sys; p=sys.argv[1]; r=open(p,'"'"'rb'"'"').read(1048577); assert len(r)<=1048576 and hashlib.sha256(r).hexdigest()==sys.argv[2]; sys.argv=[p,*sys.argv[3:]]; exec(compile(r,p,'"'"'exec'"'"'),{'"'"'__name__'"'"':'"'"'__main__'"'"','"'"'__file__'"'"':p})' /home/jazofv1/.hioc-pe73-completion-752f6bb01ab45de5/tools/pe73_completion.py 2bcf0e5cec2d6b657a6970d39ef7d630b4c4c05c6d27469ae3b9e6c7d61e33c6 guard-backend --manifest-sha 752f6bb01ab45de58ef303636e8d69aae834c75f2c0ba05aba20e043cc60af8f
pe73_status=$?
printf "PE73_EXIT_STATUS=%s\n" "$pe73_status"
```

### 8. Deliver HA artifacts/resource/editor, disabled

Target: **PI5 HA / Terminal root, while the finite PI3 guard waits**.

Performs live native/Core filesystem proof, frontend TLS proof, exact Dashboard/resource continuity, mTLS/HMAC/independent ACL checks and fresh guard observations. A distinct HA transaction preserves exact private Dashboard/resource exports and file backups before mutation. Publishes four pinned files and verifies the served editor before exactly one resource/create and one additive Inventory card save. Preserves all six views/layout/unrelated resources. Expected RESULT=PASS_PE73_HA_DELIVERED_DISABLED. Trust identities, exports and terminal journal binding remain private; no service activation/migration/evaluation occurs.

```bash
/root/.hioc-pe73-provision-environment/venv/bin/python3 -I -B -c 'import hashlib,sys; p=sys.argv[1]; r=open(p,'"'"'rb'"'"').read(1048577); assert len(r)<=1048576 and hashlib.sha256(r).hexdigest()==sys.argv[2]; sys.argv=[p,*sys.argv[3:]]; exec(compile(r,p,'"'"'exec'"'"'),{'"'"'__name__'"'"':'"'"'__main__'"'"','"'"'__file__'"'"':p})' /root/.hioc-pe73-completion-752f6bb01ab45de5/tools/pe73_completion.py 2bcf0e5cec2d6b657a6970d39ef7d630b4c4c05c6d27469ae3b9e6c7d61e33c6 deliver-ha --manifest-sha 752f6bb01ab45de58ef303636e8d69aae834c75f2c0ba05aba20e043cc60af8f
pe73_status=$?
printf "PE73_EXIT_STATUS=%s\n" "$pe73_status"
```

### 9. Independent read-only installation verification

Target: **PI5 HA / Terminal root**.

Starts a separate process, creates no lease and performs no publication. Verifies exact terminal journal/trust/context, actual four installed files/modes, full live additive Dashboard/resource state, private export/backups and exact HTTPS-served editor content. Checks hioc_operator remains unloaded and its services absent. Expected RESULT=PASS_PE73_HA_INDEPENDENT_INSTALLATION_VERIFICATION. It does not claim PE-7.4 UI saves or monitoring behavior has run.

```bash
/root/.hioc-pe73-provision-environment/venv/bin/python3 -I -B -c 'import hashlib,sys; p=sys.argv[1]; r=open(p,'"'"'rb'"'"').read(1048577); assert len(r)<=1048576 and hashlib.sha256(r).hexdigest()==sys.argv[2]; sys.argv=[p,*sys.argv[3:]]; exec(compile(r,p,'"'"'exec'"'"'),{'"'"'__name__'"'"':'"'"'__main__'"'"','"'"'__file__'"'"':p})' /root/.hioc-pe73-completion-752f6bb01ab45de5/tools/pe73_completion.py 2bcf0e5cec2d6b657a6970d39ef7d630b4c4c05c6d27469ae3b9e6c7d61e33c6 verify-ha --manifest-sha 752f6bb01ab45de58ef303636e8d69aae834c75f2c0ba05aba20e043cc60af8f
pe73_status=$?
printf "PE73_EXIT_STATUS=%s\n" "$pe73_status"
```

## Failure and recovery

Any failure stops this sequence; retain exact private context, trust parents,
issuance evidence, observer leases, directory intents, journal, stages and backups.
There is no automatic rollback, reconnect, retry, cron action, release or cleanup.
Do not reset the context to obtain a new attempt over an unresolved transaction.
Failure receipts expose only bounded public codes/action/status; do not paste private
plan, packet, key, ACL, Dashboard export or exception contents into chat.

The existing HA Delivery.restore_files recovery is restricted to a known terminal
DELIVERED_DISABLED or LOCAL_ROUTE_BLOCKED state with pending=null, verified installed
identities and exact original live Dashboard/resource state. LOCAL_ROUTE_BLOCKED
has no attempted API mutation; verified files/backups remain. After possible API
mutation or an uncertain acknowledgement, do not call file restore or rerun delivery.
Use the retained exact exports and supported Home Assistant Dashboard/resource editor
to restore only the transaction's own additive card/resource after current-state
adjudication; never edit .storage or replace unrelated content. If any unrelated
change occurred, preserve it and stop rather than overwrite with an old full export.
Only after API baseline restoration and fresh native guard/explicit recovery authority
may the existing file-restoration routine restore each recorded backup/remove each
verified newly installed object. Interrupted restoration retains its exact pending
state and is not replayed blindly. A concrete failure needs its actual journal,
not a speculative universal recovery command with guessed state or expired leases.

## Final closure evidence

Return sanitized results and actual exit statuses for operations1–9, especially the
disabled HA delivery, independent installation verification and finite PI3 guard.
PI3 prior delivery remains OPERATOR_SUPPLIED PASS, not rerun. All remaining production
fields remain UNKNOWN/PENDING until the operator supplies their actual results.
Final PE-7.3 closure is one concise evidence reconciliation and documentation/Git
commit/push/clean verification; no new broad implementation review, historical
predecessor check or repeated executive approval is required. PE-7.4 remains
NOT_AUTHORIZED; migration, editing, evaluation and recurring activation are later.
