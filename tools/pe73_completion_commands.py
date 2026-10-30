"""Build the public, deterministic PE-7.3 operator package and exact commands."""
import base64,hashlib,io,json,pathlib,shlex,zipfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
MANIFEST='tools/pe73-completion-package.json'
ARCHIVE='release/pe73-completion-package.zip'
TOOLS=['pe73_completion','pe73_ha_provision','pe73_ha_production','pe73_ha_delivery','pe73_ha_assess',
 'pe73_ha_live_qualify','pe73_ca_custody','pe73_pi3_provision_environment','pe73_provision_environment',
 'pe73_maintenance_window','hioc-pe73-pi3-delivery','pe73_verified_baseline','pe73_successor_delivery']
GOV=['governance/pe7/pe73-successor-delivery.json','governance/pe7/pe73-verified-baseline-contract.json']
PAYLOADS=['homeassistant/custom_components/hioc_operator/'+p for p in ('__init__.py','manifest.json','services.yaml')]+['homeassistant/www/hioc-asset-editor.js','homeassistant/dashboards/hioc_dashboard_v2.yaml','homeassistant/packages/hioc_incident_center.yaml']
sha=lambda raw:hashlib.sha256(raw).hexdigest()
blob=lambda raw:hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def build():
    files={**{'tools/'+p+'.py':(ROOT/'tools'/(p+'.py')).read_bytes().replace(b'\r\n',b'\n') for p in TOOLS},
        **{p:(ROOT/p).read_bytes().replace(b'\r\n',b'\n') for p in GOV},
        **{'payloads/'+p:(ROOT/p).read_bytes().replace(b'\r\n',b'\n') for p in PAYLOADS}}
    manifest=json.dumps(dict(version=1,payload_release='20f7f4c64fd32865f006ecfb2135ae6bbcada16c',
        files={p:dict(sha256=sha(raw),git_blob=blob(raw)) for p,raw in sorted(files.items())}),sort_keys=True,indent=2).encode()+b'\n'
    (ROOT/MANIFEST).write_bytes(manifest);files[MANIFEST]=manifest
    stream=io.BytesIO()
    with zipfile.ZipFile(stream,'w',compression=zipfile.ZIP_DEFLATED) as archive:
        for name,raw in sorted(files.items()):
            info=zipfile.ZipInfo(name,(1980,1,1,0,0,0));info.external_attr=0o100600<<16
            info.compress_type=zipfile.ZIP_DEFLATED;archive.writestr(info,raw)
    (ROOT/ARCHIVE).write_bytes(stream.getvalue())

def bootstrap(role,action):
    raw=(ROOT/ARCHIVE).read_bytes();msha=sha((ROOT/MANIFEST).read_bytes())
    uid=1000 if role=='pi3' else 0
    home='/home/jazofv1' if role=='pi3' else '/root'
    env={'pi3':'/home/jazofv1/.hioc-pe73-provision-environment','pi5':'/root/.hioc-pe73-provision-environment','ca':'/root/.hioc-pe73-ca-signing-environment'}[role]
    code='''import base64,hashlib,io,json,os,pathlib,stat,subprocess,sys,urllib.request,zipfile
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
        raw=base64.b64decode(value["content"].replace("\\n",""),validate=True)
        need(len(raw)==SIZE and sha(raw)==SHA)
        archive=zipfile.ZipFile(io.BytesIO(raw));names=archive.namelist()
        need(len(names)==len(set(names)) and sum(x.file_size for x in archive.infolist())<16000000)
        manifest=archive.read("tools/pe73-completion-package.json");need(sha(manifest)==MSHA)
        files=json.loads(manifest)["files"];need(set(names)==set(files)|{"tools/pe73-completion-package.json"})
        payloads={}
        for name in names:
            part=pathlib.PurePosixPath(name);need(not part.is_absolute() and ".." not in part.parts and "\\\\" not in name)
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
'''
    config='UID='+repr(uid)+'\nHOME='+repr(home)+'\nENV='+repr(env)+'\nACTION='+repr(action)+'\nMSHA='+repr(msha)+'\nBLOB='+repr(blob(raw))+'\nSHA='+repr(sha(raw))+'\nSIZE='+repr(len(raw))+'\n'
    # Constants are plain assignments before the try block; no source from main/latest.
    code=config+code
    return ('sudo ' if role=='ca' else '')+"/usr/bin/python3 -I -S -B - <<'PE73'\n"+code+"PE73"

def installed(role,action):
    msha=sha((ROOT/MANIFEST).read_bytes());home='/home/jazofv1' if role=='pi3' else '/root'
    env={'pi3':'/home/jazofv1/.hioc-pe73-provision-environment','pi5':'/root/.hioc-pe73-provision-environment','ca':'/root/.hioc-pe73-ca-signing-environment'}[role]
    source=home+'/.hioc-pe73-completion-'+msha[:16]+'/tools/pe73_completion.py'
    wrapper="import hashlib,sys; p=sys.argv[1]; r=open(p,'rb').read(1048577); assert len(r)<=1048576 and hashlib.sha256(r).hexdigest()==sys.argv[2]; sys.argv=[p,*sys.argv[3:]]; exec(compile(r,p,'exec'),{'__name__':'__main__','__file__':p})"
    args=[env+'/venv/bin/python3','-I','-B','-c',wrapper,source,sha((ROOT/'tools/pe73_completion.py').read_bytes()),action,'--manifest-sha',msha]
    return ('sudo ' if role=='ca' else '')+shlex.join(args)

def commands():
    def pipe(block,right):
        first,rest=block.split('\n',1);return first+' | '+right+'\n'+rest
    return [
        ('PI3 NUT&PIHOLE / jazofv1','prepare-backend',bootstrap('pi3','prepare-backend')),
        ('PI3 NUT&PIHOLE / manual root signing','sign-server',pipe(bootstrap('ca','sign-server'),installed('pi3','import-server'))),
        ('PI5 HA / Terminal root','ha-request',bootstrap('pi5','ha-request')),
        ('PI3 NUT&PIHOLE / manual root signing','sign-client',installed('ca','sign-client')+' | '+installed('pi3','import-client')),
        ('PI3 NUT&PIHOLE / jazofv1','complete-backend',installed('pi3','complete-backend')),
        ('PI5 HA / Terminal root','ha-complete',installed('pi5','ha-complete')),
        ('PI3 NUT&PIHOLE / jazofv1, leave foreground session open','guard-backend',installed('pi3','guard-backend')),
        ('PI5 HA / Terminal root, while the finite PI3 guard waits','deliver-ha',installed('pi5','deliver-ha')),
        ('PI5 HA / Terminal root','verify-ha',installed('pi5','verify-ha')),
    ]

def status(command,pipeline=False):
    if pipeline:return command+'\npe73_status=( "${PIPESTATUS[@]}" )\nprintf "PE73_SIGNER_EXIT=%s PE73_IMPORT_EXIT=%s\\n" "${pe73_status[0]}" "${pe73_status[1]}"'
    return command+'\npe73_status=$?\nprintf "PE73_EXIT_STATUS=%s\\n" "$pe73_status"'

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--build',action='store_true');args=parser.parse_args()
    if args.build:build()
    else:
        for target,action,command in commands():print(target+' / '+action+'\n'+status(command,action.startswith('sign-'))+'\n')
