"""Isolated evidence-only handoff machinery; never executes construction code."""
from __future__ import annotations
import argparse, ast, contextlib, ctypes, errno, hashlib, json, os, re, secrets, socket, stat, subprocess
from pathlib import Path
REPOSITORY=Path(__file__).resolve().parents[1]
SOURCE=Path('/home/jazofv1/hioc-release-source')
HIOC=Path('/home/jazofv1/hioc'); PE4=HIOC/'runtime/pe4'; ENVIRONMENTS=PE4/'environments'
VERSION='cpython311-websockets16.1.1-lock-v1'
CONSTRUCTION=ENVIRONMENTS/('.construct-'+VERSION+'-mwJVPNqh')
CAPTURES=PE4/'captures'; HANDOFFS=PE4/'handoffs'
E_COMMIT='1c1698f009457baa1c3b548db31916559fcc2fc8';D_COMMIT='6c431494c88688fef9a2fec7c7e81de0f503bdc2'
E_DIR=Path('/tmp/hioc-pe4-dependency-validate-9ys_lrah');D_DIR=Path('/tmp/hioc-pe4-runtime-construct-LW9Dvay6')
E_SHA='8d5ff1f602861d88ea8d363665a67091da2739686d10ab4aa9ac27f22389d834';D_SHA='a31f1e841f437dece13d327f14a99a93d5f96a8e258b9786cc6e49358821350d'
D_SOURCE_SHA='e979cc6049f8912c23e880f121fd2988d0354623c4f2a7d27eafb310e4b0c213'
NATIVE='websockets/speedups.cpython-311-aarch64-linux-gnu.so';NATIVE_SHA='b786db296f7d0677ddeceb7efbe963bc316a094f36e12388caa1333763ca4c1b'
MARKER='.hioc-action-d-eligibility.json';LIMITATION='NO_PERSISTED_E_TIME_RECURSIVE_BASELINE';CONTINUITY='GOVERNANCE_ATTESTED_E_TO_CAPTURE'
SMALL_LIMIT=65536;TREE_LIMIT=64*1024*1024;ENTRY_LIMIT=100000
SCHEMAS=tuple('action-e-'+n for n in ('handoff','construction-tree','continuity-attestation','capture-report','capture-manifest','durable-bundle','historical'))
PROTECTED=('tools/hioc-pe4-runtime-construct.py','tools/hioc_pe4_runtime_common.py','requirements-pe4.lock')
E_PROTECTED=(*PROTECTED,'tools/hioc-pe4-dependency-validate.py','tools/hioc_pe4_handoff_compatibility.py','tools/hioc-pe4-runtime-publish.py','tools/hioc-pe4-runtime-preflight.py','tools/hioc-pe4-runtime-rollback.py','tools/hioc-pe4-ha-auth-capability.py')
OWN_SOURCE=('tools/hioc_pe4_action_e_handoff.py','tools/hioc-pe4-action-e-handoff-capture.py','tools/hioc-pe4-action-e-handoff-preserve.py',*('governance/pe4/'+n+'.schema.json' for n in SCHEMAS))
STAGES=frozenset(('TARGET','SOURCE','HISTORY','E_EVIDENCE','D_EVIDENCE','RETAINED_IDENTITY','CONSTRUCTION_HIERARCHY','GOVERNED_MEMBER','TREE_CAPTURE','STAGING_ALLOCATION','STAGING_WRITE','STAGING_FSYNC','POSTVALIDATION','STAGED_INPUT','AUTHORIZATION','BUNDLE_ALLOCATION','BUNDLE_WRITE','BUNDLE_FSYNC','BUNDLE_PUBLICATION','FINAL_VALIDATION','ARGUMENTS','UNEXPECTED'))
CODES=frozenset(('INVALID','MISMATCH','UNAVAILABLE','CONFLICT','IO_FAILED','LIMIT_EXCEEDED','UNSTABLE','UNEXPECTED_ERROR'))
class Failure(Exception):
    def __init__(self,code,stage):
        if code not in CODES or stage not in STAGES:raise ValueError('invalid finite failure')
        self.code,self.stage=code,stage;super().__init__(code)
def fail(stage,code='INVALID'):raise Failure(code,stage)
def digest(raw):return hashlib.sha256(raw).hexdigest()
def canonical(document,maximum=SMALL_LIMIT):
    def types(v):
        if isinstance(v,float) or not isinstance(v,(dict,list,str,int,bool,type(None))):fail('STAGED_INPUT')
        if isinstance(v,dict):
            if any(not isinstance(k,str) for k in v):fail('STAGED_INPUT')
            for x in v.values():types(x)
        elif isinstance(v,list):
            for x in v:types(x)
    types(document)
    raw=(json.dumps(document,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False)+'\n').encode()
    if len(raw)>maximum:fail('STAGED_INPUT','LIMIT_EXCEEDED')
    return raw
def parse(raw,stage,maximum=SMALL_LIMIT,canonical_required=False):
    if len(raw)>maximum:fail(stage,'LIMIT_EXCEEDED')
    def pairs(items):
        result={}
        for k,v in items:
            if k in result:fail(stage)
            result[k]=v
        return result
    try:
        result=json.loads(raw.decode('utf-8'),object_pairs_hook=pairs,parse_float=lambda _:fail(stage),parse_constant=lambda _:fail(stage))
        if canonical_required and canonical(result,maximum)!=raw:fail(stage)
        return result
    except (ValueError,UnicodeError,RecursionError):fail(stage)
def validate(value,s,stage='STAGED_INPUT'):
    """Execute the bounded JSON Schema subset used by committed contracts."""
    if 'oneOf' in s:
        count=0
        for b in s['oneOf']:
            try:validate(value,b,stage);count+=1
            except Failure:pass
        if count!=1:fail(stage)
        return
    if 'const' in s and (type(value)!=type(s['const']) or value!=s['const']):fail(stage)
    if 'enum' in s and not any(type(value)==type(v) and value==v for v in s['enum']):fail(stage)
    t=s.get('type')
    if t=='object':
        if type(value)!=dict or set(value)!=set(s['required']) or set(value)-set(s['properties']):fail(stage)
        for k,v in value.items():validate(v,s['properties'][k],stage)
    elif t=='array':
        if type(value)!=list or not s.get('minItems',0)<=len(value)<=s.get('maxItems',ENTRY_LIMIT):fail(stage)
        for v in value:validate(v,s['items'],stage)
    elif t=='string':
        if type(value)!=str or not s.get('minLength',0)<=len(value)<=s.get('maxLength',4096):fail(stage)
        if 'pattern' in s and re.search(s['pattern'],value) is None:fail(stage)
    elif t=='integer':
        if type(value)!=int or not -(2**63)<=value<2**64 or ('minimum' in s and value<s['minimum']):fail(stage)
    elif t is not None:fail(stage)
def schema(name):return parse((REPOSITORY/'governance/pe4'/('action-e-'+name+'.schema.json')).read_bytes(),'SOURCE')
def record(name,document):
    validate(document,schema(name))
    if name in ('capture-report','handoff'):
        obs=document['revalidated_observables']
        if len({v['observable'] for v in obs})!=len(obs):fail('STAGED_INPUT')
    return document
def history():
    def constants(s):
        if 'const' in s:return s['const']
        return {k:constants(v) for k,v in s['properties'].items()}
    return constants(schema('historical'))
def token(i):return (i.st_dev,i.st_ino,i.st_uid,i.st_gid,i.st_mode,i.st_nlink,i.st_size,i.st_mtime_ns,i.st_ctime_ns)
def identity(i):return dict(dev=i.st_dev,ino=i.st_ino,uid=i.st_uid,gid=i.st_gid,mode=f'{stat.S_IMODE(i.st_mode):04o}')
class Directory:
    def __init__(self,fd,path,parent=None):self.fd,self.path,self.parent=fd,Path(path),parent;self.identity=identity(os.fstat(fd))
    def check(self,stage):
        if identity(os.fstat(self.fd))!=self.identity:fail(stage,'UNSTABLE')
        if self.parent:
            self.parent.check(stage);i=os.stat(self.path.name,dir_fd=self.parent.fd,follow_symlinks=False)
            if identity(i)!=self.identity or not stat.S_ISDIR(i.st_mode):fail(stage,'UNSTABLE')
    def close(self):os.close(self.fd)
def trusted_ancestor(path, info):
    # Original evidence lives below the conventional root-owned sticky /tmp.
    # The exception applies only to that ancestor, never to evidence children.
    if Path(path).as_posix() == '/tmp':
        return stat.S_ISDIR(info.st_mode) and info.st_uid == 0 and info.st_gid == 0 and stat.S_IMODE(info.st_mode) == 0o1777
    return stat.S_ISDIR(info.st_mode) and info.st_uid in (0, os.getuid()) and not stat.S_IMODE(info.st_mode) & 0o022

class Filesystem:
    def __init__(self):self.stack=contextlib.ExitStack();self.directories={};self.evidence_pins={}
    def close(self):self.stack.close()
    def retain(self,fd,path,parent=None):
        d=Directory(fd,path,parent);self.stack.callback(d.close);self.directories[str(path)]=d;return d
    def open(self,path,stage,mode=None):
        path=Path(path)
        if not path.is_absolute() or '..' in path.parts:fail(stage)
        parent=self.directories.get('/')
        if parent is None:parent=self.retain(os.open('/',os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW),'/')
        for part in path.parts[1:]:
            full=parent.path/part
            if str(full) in self.directories:parent=self.directories[str(full)];parent.check(stage);continue
            before=os.stat(part,dir_fd=parent.fd,follow_symlinks=False)
            if not trusted_ancestor(full, before):fail(stage)
            fd=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=parent.fd)
            try:
                after=os.fstat(fd)
                if token(before)!=token(after):fail(stage,'UNSTABLE')
                if parent.path in (HIOC/'runtime',PE4,ENVIRONMENTS,CAPTURES,HANDOFFS) and after.st_dev!=os.fstat(parent.fd).st_dev:fail(stage)
                entry_now=os.stat(part,dir_fd=parent.fd,follow_symlinks=False)
                if token(entry_now)!=token(after):fail(stage,'UNSTABLE')
                child=self.retain(fd,full,parent);fd=-1
            finally:
                if fd>=0:os.close(fd)
            parent=child
        parent.check(stage)
        if mode is not None and (parent.identity['mode']!=f'{mode:04o}' or parent.identity['uid']!=os.getuid() or parent.identity['gid']!=os.getgid()):fail(stage)
        return parent
    def child(self,parent,name,mode,stage):
        parent.check(stage)
        try:os.mkdir(name,mode,dir_fd=parent.fd)
        except FileExistsError:fail(stage,'CONFLICT')
        fd=os.open(name,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=parent.fd)
        try:
            os.fchmod(fd,mode)
            d=self.retain(fd,parent.path/name,parent);fd=-1
        finally:
            if fd>=0:os.close(fd)
        d=self.directories[str(parent.path/name)];d.check(stage)
        if d.identity['uid']!=os.getuid() or d.identity['gid']!=os.getgid() or d.identity['dev']!=parent.identity['dev']:fail(stage)
        return d
    def parent(self,path,stage):
        d=self.open(path.parent,stage,0o750)
        try:os.stat(path.name,dir_fd=d.fd,follow_symlinks=False)
        except FileNotFoundError:
            result=self.child(d,path.name,0o700,stage);os.fsync(result.fd);os.fsync(d.fd);return result
        return self.open(path,stage,0o700)
def read_file(directory,name,stage,mode=0o600,maximum=SMALL_LIMIT):
    directory.check(stage);before=os.stat(name,dir_fd=directory.fd,follow_symlinks=False)
    if not stat.S_ISREG(before.st_mode) or before.st_uid!=os.getuid() or before.st_gid!=os.getgid() or stat.S_IMODE(before.st_mode)!=mode:fail(stage)
    fd=os.open(name,os.O_RDONLY|os.O_NOFOLLOW,dir_fd=directory.fd)
    try:
        if token(before)!=token(os.fstat(fd)):fail(stage,'UNSTABLE')
        parts=[];total=0
        while True:
            b=os.read(fd,min(65536,maximum+1-total))
            if not b:break
            parts.append(b);total+=len(b)
            if total>maximum:fail(stage,'LIMIT_EXCEEDED')
        if token(before)!=token(os.fstat(fd)):fail(stage,'UNSTABLE')
    finally:os.close(fd)
    if token(before)!=token(os.stat(name,dir_fd=directory.fd,follow_symlinks=False)):fail(stage,'UNSTABLE')
    directory.check(stage);return b''.join(parts)
def absent(directory,name,stage):
    directory.check(stage)
    try:os.stat(name,dir_fd=directory.fd,follow_symlinks=False)
    except FileNotFoundError:return
    fail(stage,'CONFLICT')
def publication_guard(fs):
    root=fs.open(PE4,'CONSTRUCTION_HIERARCHY',0o750);env=fs.open(ENVIRONMENTS,'CONSTRUCTION_HIERARCHY',0o750)
    for name in ('active','previous-active','transactions','.active.pe4.tmp','.active.pe4.rollback.tmp'):absent(root,name,'CONSTRUCTION_HIERARCHY')
    absent(env,VERSION,'CONSTRUCTION_HIERARCHY')
    try:os.stat(HANDOFFS.name,dir_fd=root.fd,follow_symlinks=False)
    except FileNotFoundError:return
    hand=fs.open(HANDOFFS,'CONSTRUCTION_HIERARCHY',0o700)
    absent(hand,'action-e-'+E_COMMIT,'CONSTRUCTION_HIERARCHY')
def evidence(fs,path,expected,stage):
    if path!=(E_DIR if stage=='E_EVIDENCE' else D_DIR):fail(stage)
    d=fs.open(path,stage,0o700)
    if sorted(os.listdir(d.fd))!=['result.json']:fail(stage)
    if type(getattr(fs,'evidence_pins',None))==dict:pin_original_evidence(fs,d,stage)
    raw=read_file(d,'result.json',stage)
    if type(getattr(fs,'evidence_pins',None))==dict:pin_original_evidence(fs,d,stage)
    if digest(raw)!=expected:fail(stage,'MISMATCH')
    doc=parse(raw,stage,canonical_required=True)
    if stage=='E_EVIDENCE':validate(doc,schema('handoff')['properties']['e_semantics'],stage)
    else:
        expect={'schema_version':'1.0','action':'PE-4.0B.2a-D','governance_commit':D_COMMIT,'result':'PASS','error_code':'NONE','failure_stage':'COMPLETE','rollback_recommended':False,'construction_directory':CONSTRUCTION.as_posix(),'environment_identity':VERSION,'wheel_sha256':'86d7f0f8bdb25d2c632b72527325e4776430fd5bc61b9118de4e2b8ddb5f5b01','lock_sha256':'19433d53e3015157207d1af4ef07930db6f0e0d525597485384b3b7d42628e96','input_snapshot_retained':False,'eligibility_state':'AWAITING_CONFIRMATION'}
        if type(doc)!=dict or set(doc)!=set(expect)|{'installed_distributions'}:fail(stage)
        for k,v in expect.items():
            if type(doc[k])!=type(v) or doc[k]!=v:fail(stage)
        ds=doc['installed_distributions']
        if type(ds)!=dict or set(ds)-{'pip','setuptools','websockets'} or not {'pip','websockets'}<=set(ds) or ds['websockets']!='16.1.1':fail(stage)
        if any(type(v)!=str or re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9.!+_-]{0,63}',v) is None for v in ds.values()):fail(stage)
    return raw
def git(arguments,stage='SOURCE'):
    environment={'PATH':'/usr/bin:/bin','HOME':'/nonexistent','LANG':'C.UTF-8','LC_ALL':'C.UTF-8','GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':'/dev/null','GIT_NO_REPLACE_OBJECTS':'1'}
    try:
        p=subprocess.run(['git','--no-replace-objects','-C',str(SOURCE),*arguments],env=environment,stdin=subprocess.DEVNULL,capture_output=True,timeout=60,check=False)
        if p.returncode or len(p.stdout)>TREE_LIMIT or len(p.stderr)>SMALL_LIMIT:fail(stage)
        return p.stdout
    except (OSError,subprocess.SubprocessError):fail(stage,'IO_FAILED')
def source_guard(commit,capture_commit=None):
    if SOURCE!=REPOSITORY:fail('SOURCE')
    commits=[D_COMMIT,E_COMMIT,commit]+([capture_commit] if capture_commit else [])
    for c in commits:
        if not isinstance(c,str) or re.fullmatch('[0-9a-f]{40}',c) is None:fail('SOURCE')
        if git(['cat-file','-t',c]).strip()!=b'commit':fail('SOURCE')
    if git(['rev-parse','--is-shallow-repository']).strip()!=b'false':fail('HISTORY')
    for a,b in [(D_COMMIT,E_COMMIT),(E_COMMIT,commit)]+([(capture_commit,commit)] if capture_commit else []):git(['merge-base','--is-ancestor',a,b],'HISTORY')
    for args,wanted in ((['branch','--show-current'],b'main'),(['rev-parse','HEAD'],commit.encode()),(['rev-parse','refs/remotes/origin/main'],commit.encode())):
        if git(args).strip()!=wanted:fail('SOURCE','MISMATCH')
    if git(['status','--porcelain','--untracked-files=all']).strip() or git(['rev-list','--left-right','--count','HEAD...origin/main']).split()!=[b'0',b'0']:fail('SOURCE')
    for name in ('MERGE_HEAD','CHERRY_PICK_HEAD','REVERT_HEAD','REBASE_HEAD','rebase-merge','rebase-apply','sequencer','BISECT_START'):
        p=Path(git(['rev-parse','--git-path',name]).decode().strip());p=p if p.is_absolute() else SOURCE/p
        if os.path.lexists(p):fail('SOURCE')
    for path in E_PROTECTED:
        old=git(['rev-parse',E_COMMIT+':'+path]).strip();now=git(['rev-parse',commit+':'+path]).strip()
        if old!=now or git(['cat-file','-t',now.decode()]).strip()!=b'blob':fail('HISTORY','MISMATCH')
    for path in PROTECTED:
        if git(['rev-parse',D_COMMIT+':'+path]).strip()!=git(['rev-parse',E_COMMIT+':'+path]).strip():fail('HISTORY','MISMATCH')
    if digest(git(['show',D_COMMIT+':tools/hioc-pe4-runtime-construct.py']))!=D_SOURCE_SHA:fail('HISTORY','MISMATCH')
    # Raw bytes avoid invoking potentially configured clean filters.
    for path in (*OWN_SOURCE,*E_PROTECTED):
        if git(['show',commit+':'+path])!=(SOURCE/path).read_bytes():fail('SOURCE','MISMATCH')
    module=ast.parse(git(['show',E_COMMIT+':tools/hioc-pe4-dependency-validate.py']).decode('utf-8'));members=None
    for node in module.body:
        if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='WHEEL_MEMBERS' for t in node.targets):members=ast.literal_eval(node.value)
    if type(members)!=dict or len(members)!=52 or members.get(NATIVE)!=NATIVE_SHA:fail('GOVERNED_MEMBER')
    return members
def target_guard():
    if os.name!='posix' or not all(hasattr(os,n) for n in ('O_DIRECTORY','O_NOFOLLOW')):fail('TARGET','UNAVAILABLE')
    import pwd,grp
    if socket.gethostname().split('.')[0]!='nutandpihole' or os.getuid()!=1000 or os.getgid()!=1000 or pwd.getpwuid(os.getuid()).pw_name!='jazofv1' or grp.getgrgid(os.getgid()).gr_name!='jazofv1':fail('TARGET')
    try:p=subprocess.run(['/usr/sbin/ip','-o','-4','addr','show','scope','global'],capture_output=True,timeout=10,check=False)
    except (OSError,subprocess.SubprocessError):fail('TARGET','IO_FAILED')
    if p.returncode or len(p.stdout)>SMALL_LIMIT or re.search(rb'\binet\s+192\.168\.100\.252/',p.stdout) is None:fail('TARGET')
def component(hexname):
    try:b=bytes.fromhex(hexname)
    except ValueError:fail('TREE_CAPTURE')
    if not b or len(b)>255 or b in (b'.',b'..') or b'/' in b or b'\0' in b or b.hex()!=hexname:fail('TREE_CAPTURE')
    return b
def entry(i,path,kind,**extra):
    return dict(path=path,type=kind,dev=i.st_dev,ino=i.st_ino,uid=i.st_uid,gid=i.st_gid,mode=f'{stat.S_IMODE(i.st_mode):04o}',nlink=i.st_nlink,size=i.st_size,mtime_ns=i.st_mtime_ns,ctime_ns=i.st_ctime_ns,**extra)
def tree_entries(directory):
    entries=[]
    def visit(fd,relative):
        if len(relative)>128:fail('TREE_CAPTURE','LIMIT_EXCEEDED')
        before=os.fstat(fd);names=sorted(os.fsencode(n) for n in os.listdir(fd))
        if before.st_dev!=directory.identity['dev']:fail('TREE_CAPTURE')
        entries.append(entry(before,relative,'DIRECTORY',children=[n.hex() for n in names]))
        if len(entries)>ENTRY_LIMIT:fail('TREE_CAPTURE','LIMIT_EXCEEDED')
        for name in names:
            component(name.hex());path=relative+[name.hex()]
            if sum(len(component(p))+1 for p in path)>4096:fail('TREE_CAPTURE','LIMIT_EXCEEDED')
            i=os.stat(name,dir_fd=fd,follow_symlinks=False)
            if i.st_dev!=directory.identity['dev']:fail('TREE_CAPTURE')
            if stat.S_ISDIR(i.st_mode):
                child=os.open(name,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd)
                try:
                    if token(i)!=token(os.fstat(child)):fail('TREE_CAPTURE','UNSTABLE')
                    visit(child,path)
                finally:os.close(child)
            elif stat.S_ISREG(i.st_mode):
                child=os.open(name,os.O_RDONLY|os.O_NOFOLLOW,dir_fd=fd)
                try:
                    if token(i)!=token(os.fstat(child)):fail('TREE_CAPTURE','UNSTABLE')
                    h=hashlib.sha256()
                    while True:
                        block=os.read(child,65536)
                        if not block:break
                        h.update(block)
                    if token(i)!=token(os.fstat(child)):fail('TREE_CAPTURE','UNSTABLE')
                finally:os.close(child)
                entries.append(entry(i,path,'REGULAR_FILE',sha256=h.hexdigest()))
            elif stat.S_ISLNK(i.st_mode):
                if path!=[b'lib64'.hex()] or os.readlink(name,dir_fd=fd)!=b'lib':fail('TREE_CAPTURE')
                entries.append(entry(i,path,'SYMLINK',target_hex=os.readlink(name,dir_fd=fd).hex()))
            else:fail('TREE_CAPTURE')
            if token(i)!=token(os.stat(name,dir_fd=fd,follow_symlinks=False)):fail('TREE_CAPTURE','UNSTABLE')
            if len(entries)>ENTRY_LIMIT:fail('TREE_CAPTURE','LIMIT_EXCEEDED')
        if names!=sorted(os.fsencode(n) for n in os.listdir(fd)) or token(before)!=token(os.fstat(fd)):fail('TREE_CAPTURE','UNSTABLE')
    directory.check('TREE_CAPTURE');visit(directory.fd,[]);directory.check('TREE_CAPTURE')
    return sorted(entries,key=lambda e:tuple(component(p) for p in e['path']))
def validate_tree(doc):
    record('construction-tree',doc);entries=doc['entries'];by={}
    for e in entries:
        key=tuple(component(p) for p in e['path'])
        if key in by or sum(len(p)+1 for p in key)>4096:fail('TREE_CAPTURE')
        by[key]=e
        if e['type']=='DIRECTORY':
            names=[component(n) for n in e['children']]
            if names!=sorted(set(names)):fail('TREE_CAPTURE')
    if entries!=sorted(entries,key=lambda e:tuple(component(p) for p in e['path'])) or () not in by or by[()]['type']!='DIRECTORY':fail('TREE_CAPTURE')
    for key,e in by.items():
        if key and (key[:-1] not in by or by[key[:-1]]['type']!='DIRECTORY'):fail('TREE_CAPTURE')
        if e['type']=='DIRECTORY' and [component(n) for n in e['children']]!=sorted(k[-1] for k in by if k and k[:-1]==key):fail('TREE_CAPTURE')
    return doc
def observables():
    names=schema('capture-report')['properties']['revalidated_observables']['items']['properties']['observable']['enum']
    return [dict(observable=n,source_class='COMMITTED_POLICY' if n in ('GOVERNED_MEMBERS','GIT_LINEAGE','PUBLICATION_ABSENT','D_ELIGIBILITY') else 'RETAINED_MACHINE_OBSERVATION',source_reference='docs/PE4_ISOLATED_RUNTIME_LIFECYCLE.md@95a26c687f3cb3b1cc1cf6ee121e0ed01ad0c2e9; governed historical evidence',comparison_basis='COMMITTED_POLICY' if n in ('GOVERNED_MEMBERS','GIT_LINEAGE','PUBLICATION_ABSENT','D_ELIGIBILITY') else 'RETAINED_VALUE',result='PASS') for n in names]
def construction(fs,members):
    d=fs.open(CONSTRUCTION,'CONSTRUCTION_HIERARCHY',0o750)
    if d.identity!=history()['root']:fail('RETAINED_IDENTITY','MISMATCH')
    marker=read_file(d,MARKER,'D_EVIDENCE',0o400);doc=parse(marker,'D_EVIDENCE',canonical_required=True)
    expected={'schema_version':'1.0','action':'PE-4.0B.2a-D','governance_commit':D_COMMIT,'construction_directory':CONSTRUCTION.as_posix(),'environment_identity':VERSION,'wheel_sha256':'86d7f0f8bdb25d2c632b72527325e4776430fd5bc61b9118de4e2b8ddb5f5b01','lock_sha256':'19433d53e3015157207d1af4ef07930db6f0e0d525597485384b3b7d42628e96','evidence_directory':D_DIR.as_posix(),'evidence_sha256':D_SHA,'result':'PASS'}
    if doc!=expected or any(type(doc[k])!=type(v) for k,v in expected.items()):fail('D_EVIDENCE','MISMATCH')
    entries=tree_entries(d)
    for captured in entries:
        if captured['uid']!=1000 or captured['gid']!=1000 or (captured['type']!='SYMLINK' and int(captured['mode'],8)&0o022):fail('RETAINED_IDENTITY')
    by={tuple(component(p) for p in e['path']):e for e in entries}
    interpreter=by.get((b'bin',b'python'))
    if not interpreter or interpreter['type']!='REGULAR_FILE' or (interpreter['dev'],interpreter['ino'])!=(45826,823209):fail('RETAINED_IDENTITY','MISMATCH')
    cfg=by.get((b'pyvenv.cfg',))
    if not cfg or cfg['type']!='REGULAR_FILE':fail('RETAINED_IDENTITY')
    site=(b'lib',b'python3.11',b'site-packages')
    actual={b'/'.join(k[len(site):]).decode('ascii') for k,e in by.items() if k[:len(site)]==site and k[len(site):len(site)+1]==(b'websockets',) and e['type']!='DIRECTORY' and not (b'__pycache__' in k and k[-1].endswith(b'.pyc'))}
    if actual!=set(members):fail('GOVERNED_MEMBER','MISMATCH')
    for name,sha in members.items():
        e=by.get(site+tuple(os.fsencode(p) for p in name.split('/')))
        if not e or e['type']!='REGULAR_FILE' or e['sha256']!=sha:fail('GOVERNED_MEMBER','MISMATCH')
    cfgraw=read_file(d,'pyvenv.cfg','RETAINED_IDENTITY',int(cfg['mode'],8))
    try:config=dict(line.split(' = ',1) for line in cfgraw.decode().splitlines() if line)
    except (ValueError,UnicodeError):fail('RETAINED_IDENTITY')
    if config.get('version')!='3.11.2' or config.get('include-system-site-packages')!='false' or config.get('home')!='/usr/bin':fail('RETAINED_IDENTITY')
    chain=[];cur=d
    while cur:chain.append(dict(path=cur.path.as_posix(),identity=cur.identity));cur=cur.parent
    document=dict(schema_version='1.0',record_type='CONSTRUCTION_TREE',root_path=CONSTRUCTION.as_posix(),atime_excluded=True,hierarchy=list(reversed(chain)),entries=entries,bindings=dict(d_marker_sha256=digest(marker),d_evidence_sha256=D_SHA,interpreter_identity={k:interpreter[k] for k in ('dev','ino','uid','gid','mode')},configuration_sha256=cfg['sha256'],native_sha256=NATIVE_SHA,member_policy_sha256=digest(canonical(members)),fact_class='MACHINE_VERIFIED_CAPTURE_FORWARD'))
    validate_tree(document);return d,document
def verify_construction(directory,document):
    """Compare staged baseline without refreshing it or emitting a new capture."""
    validate_tree(document)
    if tree_entries(directory)!=document['entries']:fail('POSTVALIDATION','MISMATCH')
    for binding in document['hierarchy']:
        cur=directory
        while cur and cur.path.as_posix()!=binding['path']:cur=cur.parent
        if cur is None or cur.identity!=binding['identity']:fail('POSTVALIDATION','MISMATCH')
    directory.check('POSTVALIDATION')
def write_file(directory,name,raw,mode,stage):
    directory.check(stage);fd=os.open(name,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,mode,dir_fd=directory.fd)
    try:
        view=memoryview(raw)
        while view:
            n=os.write(fd,view)
            if n<=0:fail(stage,'IO_FAILED')
            view=view[n:]
        os.fchmod(fd,mode)
        try:os.fsync(fd)
        except OSError:fail('STAGING_FSYNC' if stage=='STAGING_WRITE' else 'BUNDLE_FSYNC','IO_FAILED')
    finally:os.close(fd)
def inventory(payloads,mode):return [dict(name=name,size=len(raw),mode=f'{mode:04o}',sha256=digest(raw)) for name,raw in sorted(payloads.items())]
def check_files(directory,payloads,mode,stage):
    if sorted(os.listdir(directory.fd))!=sorted(payloads):fail(stage,'MISMATCH')
    for name,raw in payloads.items():
        if read_file(directory,name,stage,mode,TREE_LIMIT if name=='construction-tree.json' else SMALL_LIMIT)!=raw:fail(stage,'MISMATCH')
def sync(directory,parent,stage):
    try:os.fsync(directory.fd);os.fsync(parent.fd)
    except OSError:fail(stage,'IO_FAILED')
def noreplace(parent,source,destination):
    parent.check('BUNDLE_PUBLICATION')
    for name in (source,destination):
        if '/' in name or name in ('','.','..'):fail('BUNDLE_PUBLICATION')
    libc=ctypes.CDLL(None,use_errno=True);fn=getattr(libc,'renameat2',None)
    if fn is None:fail('BUNDLE_PUBLICATION','UNAVAILABLE')
    fn.argtypes=(ctypes.c_int,ctypes.c_char_p,ctypes.c_int,ctypes.c_char_p,ctypes.c_uint);fn.restype=ctypes.c_int
    if fn(parent.fd,os.fsencode(source),parent.fd,os.fsencode(destination),1):
        e=ctypes.get_errno();fail('BUNDLE_PUBLICATION','CONFLICT' if e==errno.EEXIST else 'UNAVAILABLE' if e in (errno.ENOSYS,errno.EINVAL,errno.EOPNOTSUPP,errno.EXDEV) else 'IO_FAILED')
def capture(commit,authorization,state):
    target_guard();members=source_guard(commit);fs=Filesystem()
    try:
        publication_guard(fs);eraw=evidence(fs,E_DIR,E_SHA,'E_EVIDENCE');draw=evidence(fs,D_DIR,D_SHA,'D_EVIDENCE')
        d,baseline=construction(fs,members);parent=fs.parent(CAPTURES,'STAGING_ALLOCATION');cid=secrets.token_hex(16)
        state['path']=str(CAPTURES/('e-'+cid));stage=fs.child(parent,'e-'+cid,0o700,'STAGING_ALLOCATION')
        report=record('capture-report',dict(schema_version='1.0',record_type='CAPTURE_REPORT',capture_id=cid,capture_source_commit=commit,authorization_reference=authorization,historical=history(),revalidated_observables=observables(),capture_time_facts=dict(construction_tree_sha256=digest(canonical(baseline,TREE_LIMIT)),d_marker_sha256=baseline['bindings']['d_marker_sha256'],fact_class='MACHINE_VERIFIED_CAPTURE_FORWARD'),continuity_class=CONTINUITY,historical_recursive_snapshot_persisted=False,historical_recursive_continuity_machine_proven=False,limitation=LIMITATION,approval_state='PROPOSED',validation_result='PASS',error_code='NONE',failure_stage='COMPLETE'))
        payloads={'action-e-result.json':eraw,'action-d-result.json':draw,'construction-tree.json':canonical(baseline,TREE_LIMIT),'capture-report.json':canonical(report)}
        manifest=record('capture-manifest',dict(schema_version='1.0',record_type='CAPTURE_MANIFEST',capture_id=cid,capture_source_commit=commit,approval_state='PROPOSED',inventory=inventory(payloads,0o600)))
        payloads['capture-manifest.json']=canonical(manifest)
        for name,raw in payloads.items():write_file(stage,name,raw,0o600,'STAGING_WRITE')
        sync(stage,parent,'STAGING_FSYNC');check_files(stage,payloads,0o600,'POSTVALIDATION');verify_construction(d,baseline)
        if evidence(fs,E_DIR,E_SHA,'E_EVIDENCE')!=eraw or evidence(fs,D_DIR,D_SHA,'D_EVIDENCE')!=draw:fail('POSTVALIDATION','MISMATCH')
        publication_guard(fs);source_guard(commit)
        state['digest']=digest(payloads['capture-manifest.json']);state['evidence']='CONFIRMED'
    finally:fs.close()
def staged(fs,path,expected,capture_commit):
    if path.parent!=CAPTURES or re.fullmatch('e-[0-9a-f]{32}',path.name) is None:fail('STAGED_INPUT')
    d=fs.open(path,'STAGED_INPUT',0o700);raw=read_file(d,'capture-manifest.json','STAGED_INPUT')
    if digest(raw)!=expected:fail('STAGED_INPUT','MISMATCH')
    m=parse(raw,'STAGED_INPUT',canonical_required=True);record('capture-manifest',m)
    if m['capture_id']!=path.name[2:] or m['capture_source_commit']!=capture_commit:fail('STAGED_INPUT')
    names=['action-d-result.json','action-e-result.json','capture-report.json','construction-tree.json']
    if [v['name'] for v in m['inventory']]!=names or any(v['mode']!='0600' for v in m['inventory']):fail('STAGED_INPUT')
    payloads={'capture-manifest.json':raw}
    for item in m['inventory']:
        name=item['name'];r=read_file(d,name,'STAGED_INPUT',maximum=TREE_LIMIT if name=='construction-tree.json' else SMALL_LIMIT)
        if digest(r)!=item['sha256'] or len(r)!=item['size']:fail('STAGED_INPUT','MISMATCH')
        payloads[name]=r
    check_files(d,payloads,0o600,'STAGED_INPUT')
    tree=parse(payloads['construction-tree.json'],'STAGED_INPUT',TREE_LIMIT,True);validate_tree(tree)
    report=parse(payloads['capture-report.json'],'STAGED_INPUT',canonical_required=True);record('capture-report',report)
    if report['capture_id']!=m['capture_id'] or report['capture_source_commit']!=capture_commit or report['capture_time_facts']['construction_tree_sha256']!=digest(payloads['construction-tree.json']) or report['capture_time_facts']['d_marker_sha256']!=tree['bindings']['d_marker_sha256']:fail('STAGED_INPUT')
    if digest(payloads['action-e-result.json'])!=E_SHA or digest(payloads['action-d-result.json'])!=D_SHA:fail('STAGED_INPUT')
    return d,payloads,tree,report
def preserve(commit,path,expected,capture_commit,authorization,state):
    target_guard();source_guard(commit,capture_commit);fs=Filesystem()
    try:
        publication_guard(fs);stage,payloads,tree,report=staged(fs,path,expected,capture_commit)
        eraw=evidence(fs,E_DIR,E_SHA,'E_EVIDENCE');draw=evidence(fs,D_DIR,D_SHA,'D_EVIDENCE')
        if eraw!=payloads['action-e-result.json'] or draw!=payloads['action-d-result.json']:fail('STAGED_INPUT')
        d=fs.open(CONSTRUCTION,'CONSTRUCTION_HIERARCHY',0o750)
        if d.identity!=history()['root']:fail('RETAINED_IDENTITY','MISMATCH')
        verify_construction(d,tree);parent=fs.parent(HANDOFFS,'BUNDLE_ALLOCATION');final='action-e-'+E_COMMIT
        absent(parent,final,'BUNDLE_ALLOCATION')
        if any(n.startswith('.action-e-') for n in os.listdir(parent.fd)):fail('BUNDLE_ALLOCATION','CONFLICT')
        name='.action-e-'+secrets.token_hex(16);state['path']=str(parent.path/name);bundle=fs.child(parent,name,0o700,'BUNDLE_ALLOCATION')
        att=record('continuity-attestation',dict(schema_version='1.0',record_type='CONTINUITY_ATTESTATION',attestation_class='GOVERNANCE_DERIVED_ATTESTATION',evidence_class=CONTINUITY,historical=history(),capture_id=report['capture_id'],capture_source_commit=capture_commit,preservation_source_commit=commit,construction_tree_sha256=digest(payloads['construction-tree.json']),capture_report_sha256=digest(payloads['capture-report.json']),capture_manifest_sha256=expected,fact_sources=report['revalidated_observables'],historical_recursive_snapshot_persisted=False,historical_recursive_continuity_machine_proven=False,limitation=LIMITATION,governed_chronology=['E_EXECUTED_ONCE_PASS','WINDOWS_E_CLOSURE','WINDOWS_F_PREPARATION','WINDOWS_F_CORRECTIVE_DESIGN','WINDOWS_CONTINUITY_DESIGN','NO_AUTHORIZED_POST_E_HIOC_MUTATION_RECORDED'],approval_state='APPROVED_FOR_PRESERVATION',authorization_reference=authorization))
        out={k:payloads[k] for k in ('action-e-result.json','action-d-result.json','construction-tree.json')};out['continuity-attestation.json']=canonical(att)
        m=record('durable-bundle',dict(schema_version='1.0',record_type='DURABLE_HANDOFF_MANIFEST',capture_id=report['capture_id'],capture_source_commit=capture_commit,preservation_source_commit=commit,historical=history(),continuity_class=CONTINUITY,approval_state='APPROVED_FOR_PRESERVATION',inventory=inventory(out,0o400)))
        out['manifest.json']=canonical(m)
        for filename,raw in out.items():write_file(bundle,filename,raw,0o400,'BUNDLE_WRITE')
        check_files(bundle,out,0o400,'FINAL_VALIDATION');os.fchmod(bundle.fd,0o500);bundle.identity=identity(os.fstat(bundle.fd));sync(bundle,parent,'BUNDLE_FSYNC')
        verify_construction(d,tree);check_files(stage,payloads,0o600,'POSTVALIDATION')
        if evidence(fs,E_DIR,E_SHA,'E_EVIDENCE')!=eraw or evidence(fs,D_DIR,D_SHA,'D_EVIDENCE')!=draw:fail('POSTVALIDATION')
        source_guard(commit,capture_commit)
        bundle.check('BUNDLE_PUBLICATION');noreplace(parent,name,final)
        state['path']=str(parent.path/final);bundle.path=parent.path/final;sync(bundle,parent,'BUNDLE_FSYNC')
        reopened=fs.open(parent.path/final,'FINAL_VALIDATION',0o500)
        if reopened.identity!=bundle.identity:fail('FINAL_VALIDATION','MISMATCH')
        check_files(reopened,out,0o400,'FINAL_VALIDATION');verify_construction(d,tree);check_files(stage,payloads,0o600,'POSTVALIDATION')
        if evidence(fs,E_DIR,E_SHA,'E_EVIDENCE')!=eraw or evidence(fs,D_DIR,D_SHA,'D_EVIDENCE')!=draw:fail('POSTVALIDATION')
        source_guard(commit,capture_commit);state['digest']=digest(out['manifest.json']);state['evidence']='CONFIRMED'
    finally:fs.close()
class Parser(argparse.ArgumentParser):
    def error(self,message):fail('ARGUMENTS')
def terminal(result,code,stage,state,approval):
    for k,v in [('RESULT',result),('ERROR_CODE',code),('FAILURE_STAGE',stage),('ROLLBACK_RECOMMENDED','FALSE'),('EVIDENCE_STATE',state['evidence']),('EVIDENCE_DIR',state['path']),('MANIFEST_SHA256',state['digest']),('APPROVAL_STATE',approval),('CONTINUITY_ACCEPTED','FALSE'),('STOP_REQUIRED','TRUE')]:print(k+'='+v)
def cli(action,arguments):
    state={'path':'NONE','digest':'NONE','evidence':'UNCONFIRMED'};approval='PROPOSED'
    try:
        p=Parser(description=__doc__);p.add_argument('--governance-commit',required=True);p.add_argument('--authorization-reference',required=True)
        if action=='preserve':
            p.add_argument('--capture-directory',required=True);p.add_argument('--capture-manifest-sha256',required=True);p.add_argument('--capture-source-commit',required=True);p.add_argument('--approval-state',required=True,choices=['APPROVED_FOR_PRESERVATION'])
        a=p.parse_args(arguments)
        if re.fullmatch('[0-9a-f]{40}',a.governance_commit) is None or re.fullmatch('[A-Za-z0-9][A-Za-z0-9._:/#@ -]{0,511}',a.authorization_reference) is None:fail('ARGUMENTS')
        if action=='capture':capture(a.governance_commit,a.authorization_reference,state)
        elif action=='preserve':
            if re.fullmatch('[0-9a-f]{64}',a.capture_manifest_sha256) is None or re.fullmatch('[0-9a-f]{40}',a.capture_source_commit) is None:fail('ARGUMENTS')
            approval='APPROVED_FOR_PRESERVATION';preserve(a.governance_commit,Path(a.capture_directory),a.capture_manifest_sha256,a.capture_source_commit,a.authorization_reference,state)
        else:fail('ARGUMENTS')
        terminal('PASS','NONE','COMPLETE',state,approval);return 0
    except Failure as e:terminal('FAIL',e.code,e.stage,state,approval);return 2 if e.stage=='ARGUMENTS' else 1
    except Exception:terminal('FAIL','UNEXPECTED_ERROR','UNEXPECTED',state,approval);return 1


def bounded_io(function, stage_index=None, fixed_stage=None):
    """Map operational OS errors to the owning finite stage; never retry."""
    def invoke(*args, **kwargs):
        stage = fixed_stage or args[stage_index]
        try:
            return function(*args, **kwargs)
        except FileExistsError:
            fail(stage, 'CONFLICT')
        except (OSError, NotImplementedError):
            fail(stage, 'IO_FAILED')
    return invoke

Filesystem.open = bounded_io(Filesystem.open, stage_index=2)
Filesystem.child = bounded_io(Filesystem.child, stage_index=4)
Filesystem.parent = bounded_io(Filesystem.parent, stage_index=2)
read_file = bounded_io(read_file, stage_index=2)
write_file = bounded_io(write_file, stage_index=4)
check_files = bounded_io(check_files, stage_index=3)
tree_entries = bounded_io(tree_entries, fixed_stage='TREE_CAPTURE')
noreplace = bounded_io(noreplace, fixed_stage='BUNDLE_PUBLICATION')


def pin_original_evidence(fs, directory, stage):
    observed=(token(os.fstat(directory.fd)), token(os.stat('result.json', dir_fd=directory.fd, follow_symlinks=False)))
    key=directory.path.as_posix()
    if key in fs.evidence_pins and fs.evidence_pins[key]!=observed:
        fail(stage, 'UNSTABLE')
    fs.evidence_pins[key]=observed
