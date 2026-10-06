"""Credential-free Action G; accepted F is read-only input, never executed."""
from __future__ import annotations
import argparse, ast, copy, importlib.abc, importlib.machinery, importlib.util
import inspect, json, os, re, secrets, stat, subprocess, sys, threading
from pathlib import Path
try:
    from . import hioc_pe4_action_e_handoff as H
    from . import hioc_pe4_action_f as F
except ImportError:
    import hioc_pe4_action_e_handoff as H
    import hioc_pe4_action_f as F

F_CONSUMER='2a5e6299a0806c3f3d7c3bc11c84fddc8492333c'
F_ID='17fc3e0580ff007cdcd619ed2e2d3b34'
F_RESULT='d647c7b2241d7800a3c819cf86459e2be95c3ef58581d5ffef2dbf5bd1190941'
F_COMMITTED='24bb64cc8d885297e5696ddd733ec0dfab4b28a24e18a6996b667c186f2016e9'
TRANSACTION=H.PE4/'transactions'/('f-'+F_ID)
FINAL=H.ENVIRONMENTS/H.VERSION
CLIENT=F.C.CLIENT_TARGET
SCHEMA='governance/pe4/action-g-result.schema.json'
OWN=('tools/hioc-pe4-runtime-preflight.py','tools/hioc_pe4_action_g.py',SCHEMA)
PROTECTED=tuple(p for p in (*F.PROTECTED,*F.OWN) if p!='tools/hioc-pe4-runtime-preflight.py')
LIMIT=65536
ENV={'PATH':'/usr/bin:/bin','HOME':'/nonexistent','LANG':'C.UTF-8','LC_ALL':'C.UTF-8'}
STAGES=('ARGUMENTS','TARGET','SOURCE','HANDOFF','PUBLICATION','STARTUP','PROBE','POSTVALIDATION','EVIDENCE','COMPLETE','UNEXPECTED')
CODES=('NONE','INVALID','MISMATCH','CONFLICT','UNAVAILABLE','IO_FAILED','TIMEOUT','OUTPUT_LIMIT','PROBE_FAILED','NETWORK_FORBIDDEN','CREDENTIAL_FORBIDDEN','UNEXPECTED_ERROR')
class Failure(Exception):
    def __init__(self,code,stage):
        if code not in CODES or stage not in STAGES:raise ValueError('finite contract')
        self.code,self.stage=code,stage;super().__init__(code)
def require(value,code='MISMATCH',stage='HANDOFF'):
    if not value:raise Failure(code,stage)

def bounded(command,stage,*,env=None,cwd=None,pass_fds=(),timeout=60,limit=LIMIT):
    """Hard combined output bound while reading; children never inherit stdin."""
    process=None;threads=[];output=[bytearray(),bytearray()];lock=threading.Lock();overflow=threading.Event()
    try:
        process=subprocess.Popen(command,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,env=dict(ENV if env is None else env),cwd=cwd,pass_fds=pass_fds)
        def consume(stream,index):
            while True:
                block=stream.read(4096)
                if not block:break
                with lock:
                    remaining=limit-sum(map(len,output))
                    output[index].extend(block[:max(0,remaining)])
                    if len(block)>remaining:
                        overflow.set();process.kill();break
        for i,stream in enumerate((process.stdout,process.stderr)):
            t=threading.Thread(target=consume,args=(stream,i),daemon=True);t.start();threads.append(t)
        try:process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:raise Failure('TIMEOUT',stage)
        for t in threads:t.join(timeout=5)
        require(not overflow.is_set(),'OUTPUT_LIMIT',stage)
        require(not any(t.is_alive() for t in threads),'IO_FAILED',stage)
        require(process.returncode==0,'PROBE_FAILED' if stage=='PROBE' else 'INVALID',stage)
        return bytes(output[0])
    except Failure:
        raise
    except OSError:raise Failure('IO_FAILED',stage)
    finally:
        if process is not None:
            if process.poll() is None:process.kill();process.wait()
            for t in threads:t.join(timeout=5)
            process.stdout.close();process.stderr.close()

def git(args):
    env={**ENV,'GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':'/dev/null',
         'GIT_NO_REPLACE_OBJECTS':'1','GIT_OPTIONAL_LOCKS':'0'}
    return bounded(['/usr/bin/git','--no-replace-objects','-c','core.fsmonitor=false',
        '-c','core.untrackedCache=false','-c','core.hooksPath=/dev/null',
        '-c','submodule.recurse=false','-c','core.pager=cat','-C',str(H.SOURCE),*args],
        'SOURCE',env=env,limit=H.TREE_LIMIT)
def source_guard(commit):
    require(H.SOURCE==H.REPOSITORY,'INVALID','SOURCE')
    require(isinstance(commit,str) and re.fullmatch('[0-9a-f]{40}',commit),'INVALID','SOURCE')
    for args,wanted in ((['branch','--show-current'],b'main'),(['rev-parse','HEAD'],commit.encode()),
        (['rev-parse','refs/remotes/origin/main'],commit.encode()),(['rev-parse','--is-shallow-repository'],b'false')):
        require(git(args).strip()==wanted,stage='SOURCE')
    require(not git(['status','--porcelain','--untracked-files=all']).strip(),'CONFLICT','SOURCE')
    require(git(['rev-list','--left-right','--count','HEAD...origin/main']).split()==[b'0',b'0'],stage='SOURCE')
    for op in ('MERGE_HEAD','CHERRY_PICK_HEAD','REVERT_HEAD','REBASE_HEAD','rebase-merge','rebase-apply','sequencer','BISECT_START'):
        p=Path(os.fsdecode(git(['rev-parse','--git-path',op]).strip()))
        require(not os.path.lexists(p if p.is_absolute() else H.SOURCE/p),'CONFLICT','SOURCE')
    git(['merge-base','--is-ancestor',F_CONSUMER,commit])
    for p in PROTECTED:
        require(git(['rev-parse',F_CONSUMER+':'+p])==git(['rev-parse',commit+':'+p]),stage='SOURCE')
    # Raw byte comparison never invokes Git clean/smudge filters.
    for p in (*PROTECTED,*OWN,F.ACCEPTED):
        raw=(H.SOURCE/p).read_bytes()
        require(raw==git(['show',commit+':'+p]),stage='SOURCE')
    require(H.digest((H.SOURCE/F.ACCEPTED).read_bytes())==F.ACCEPTED_SHA,stage='SOURCE')

def validate_f(files,result_sha=F_RESULT,committed_sha=F_COMMITTED):
    require(set(files)=={'result.json',*(f'{i:04}.json' for i in range(14))})
    docs=[];previous='NONE'
    for i in range(14):
        raw=files[f'{i:04}.json'];d=H.parse(raw,'STAGED_INPUT',canonical_required=True);F.record(d)
        require(d['transaction_id']==F_ID and d['sequence']==i and d['previous_record_sha256']==previous)
        require(d['bindings']['current_consumer']==F_CONSUMER and not d['rollback_recommended'])
        docs.append(d);previous=H.digest(raw)
    result=H.parse(files['result.json'],'STAGED_INPUT',canonical_required=True);F.record(result)
    require(H.digest(files['result.json'])==result_sha and H.digest(files['0013.json'])==committed_sha)
    order=['PREPARED','CLIENT_INTENT','CLIENT_CONFIRMED','ENVIRONMENT_INTENT','ENVIRONMENT_CONFIRMED',
        'PREVIOUS_INTENT','PREVIOUS_CONFIRMED','ACTIVE_STAGE_INTENT','ACTIVE_STAGE_CONFIRMED',
        'ACTIVE_SWITCH_INTENT','ACTIVE_SWITCH_CONFIRMED','POST_VERIFIED','RESULT_REFERENCE','COMMITTED']
    require([d['event'] for d in docs]==order)
    # F records intent and confirmation while recovery remains required.
    # Only the durable COMMITTED record establishes terminal acceptance.
    publications=('NONE','NONE','CLIENT_ONLY','CLIENT_ONLY',
        'ENVIRONMENT_PUBLISHED','ENVIRONMENT_PUBLISHED','ENVIRONMENT_PUBLISHED',
        'ENVIRONMENT_PUBLISHED','ENVIRONMENT_PUBLISHED','ENVIRONMENT_PUBLISHED',
        'ACTIVE_SWITCHED','ACTIVE_SWITCHED','ACTIVE_SWITCHED','COMPLETE')
    for i,d in enumerate(docs):
        committed=i==13
        require(d['publication_state']==publications[i]
            and d['evidence_state']==('CONFIRMED' if i>=12 else 'NOT_CREATED')
            and d['recovery_required'] is (not committed)
            and d['result']==('PASS' if committed else 'IN_PROGRESS')
            and d['error_code']=='NONE'
            and d['failure_stage']==('COMPLETE' if committed else 'JOURNAL')
            and d['result_sha256']==(result_sha if i>=12 else 'NONE'))
    ref,tail=docs[-2:]
    require(result['event']=='RESULT' and result['transaction_id']==F_ID and result['result']=='PASS')
    require(ref['result_sha256']==result_sha==tail['result_sha256'] and
        ref['sequence']==result['sequence'] and ref['previous_record_sha256']==result['previous_record_sha256'])
    require(result['publication_state']=='ACTIVE_SWITCHED' and result['evidence_state']=='UNCONFIRMED'
        and result['recovery_required'] is True and result['result_sha256']=='NONE')
    for d in (result,tail):
        require(d['result']=='PASS'
            and not d['rollback_recommended']
            and d['error_code']=='NONE' and d['failure_stage']=='COMPLETE')
    require(tail['publication_state']=='COMPLETE' and tail['evidence_state']=='CONFIRMED'
        and tail['recovery_required'] is False)
    require(ref['publication_state']=='ACTIVE_SWITCHED' and ref['evidence_state']=='CONFIRMED')
    require(result['bindings']==ref['bindings']==tail['bindings'])
    b=tail['bindings'];a=F.accepted_manifest()
    require(b['current_consumer']==F_CONSUMER and b['accepted_manifest_sha256']==F.ACCEPTED_SHA
        and b['historical']==a['historical'] and b['tree_sha256']==a['capture']['tree_sha256']
        and b['attestation_sha256']==a['continuity']['attestation_sha256']
        and b['durable_bundle_sha256']==a['durable_bundle']['manifest_sha256'])
    require(b['final_environment_path']==str(FINAL) and b['client_path']==str(CLIENT)
        and b['client_sha256']==F.C.CLIENT_SHA256 and b['final_active']=='environments/'+H.VERSION
        and b['final_previous']=='NONE' and b['client_disposition']=='PUBLISHED')
    for key in ('final_environment_identity','final_active_identity','final_previous_identity','client_identity','final_root_ctime_ns'):
        require(b[key]!='NONE')
    return b

def published_tree(tree,b):
    expected=copy.deepcopy(tree['entries'])
    require(expected and expected[0]['path']==[] and expected[0]['ctime_ns']==b['original_root_ctime_ns'])
    expected[0]['ctime_ns']=b['final_root_ctime_ns']
    return expected

def result_record(commit,b,checks):
    return dict(schema_version='2.0',record_type='ACTION_G_RESULT',action='PE-4.0B.2a-G',
        current_consumer=commit,f_consumer=F_CONSUMER,f_transaction_id=F_ID,f_transaction_path=str(TRANSACTION),
        f_result_sha256=F_RESULT,f_committed_sha256=F_COMMITTED,
        accepted_manifest_sha256=b['accepted_manifest_sha256'],tree_sha256=b['tree_sha256'],
        attestation_sha256=b['attestation_sha256'],final_environment_path=b['final_environment_path'],
        final_environment_identity=b['final_environment_identity'],active_target=b['final_active'],
        active_identity=b['final_active_identity'],previous_content=b['final_previous'],
        previous_identity=b['final_previous_identity'],client_sha256=b['client_sha256'],
        client_identity=b['client_identity'],checks=checks,credential_use=False,network_connection_attempted=False,
        result='PASS',error_code='NONE',failure_stage='COMPLETE',rollback_recommended=False)
def encode_result(document):
    schema=H.parse((H.REPOSITORY/SCHEMA).read_bytes(),'SOURCE')
    H.validate(document,schema)
    return H.canonical(document,LIMIT)

class Posix:
    def __init__(self):self.fs=H.Filesystem();self.locked=False;self.evidence=None
    def close(self):
        if self.locked:F.fcntl.flock(self.root.fd,F.fcntl.LOCK_UN);self.locked=False
        self.fs.close()
    def preflight(self,commit):
        F.verify_launcher();H.target_guard();source_guard(commit)
        self.root=self.fs.open(H.PE4,'CONSTRUCTION_HIERARCHY',0o750)
        require(F.fcntl is not None,'UNAVAILABLE','PUBLICATION')
        try:F.fcntl.flock(self.root.fd,F.fcntl.LOCK_EX|F.fcntl.LOCK_NB)
        except BlockingIOError:raise Failure('CONFLICT','PUBLICATION')
        self.locked=True
        self.transactions=self.fs.open(TRANSACTION.parent,'CONSTRUCTION_HIERARCHY',0o700)
        require(sorted(os.listdir(self.transactions.fd))==['f-'+F_ID],'CONFLICT','HANDOFF')
        self.tx=self.fs.open(TRANSACTION,'CONSTRUCTION_HIERARCHY',0o700)
        self.files,self.file_tokens=self.read_transaction()
        self.bindings=validate_f(self.files)
        self.final=self.fs.open(FINAL,'CONSTRUCTION_HIERARCHY',0o750)
        self.tools=self.fs.open(CLIENT.parent,'CONSTRUCTION_HIERARCHY')
        a=F.accepted_manifest()
        self.bundle=self.fs.open(Path(a['durable_bundle']['directory']),'CONSTRUCTION_HIERARCHY',0o500)
        # Only the digest-bound canonical captured tree is needed; no E/F executor.
        self.tree_raw=H.read_file(self.bundle,'construction-tree.json','STAGED_INPUT',0o400,H.TREE_LIMIT)
        require(H.digest(self.tree_raw)==self.bindings['tree_sha256'])
        self.d_raw=H.read_file(self.bundle,'action-d-result.json','STAGED_INPUT',0o400)
        require(H.digest(self.d_raw)==self.bindings['historical']['d_evidence_sha256'])
        self.distributions=H.parse(self.d_raw,'STAGED_INPUT',canonical_required=True)['installed_distributions']
        self.tree=H.parse(self.tree_raw,'STAGED_INPUT',H.TREE_LIMIT,canonical_required=True)
        H.validate_tree(self.tree)
        self.expected=published_tree(self.tree,self.bindings)
        self.revalidate(commit)
        return copy.deepcopy(self.bindings)
    def read_transaction(self):
        names=sorted(os.listdir(self.tx.fd))
        require(names==sorted(['result.json',*(f'{i:04}.json' for i in range(14))]))
        files={};tokens={}
        for name in names:
            before=H.token(os.stat(name,dir_fd=self.tx.fd,follow_symlinks=False))
            files[name]=H.read_file(self.tx,name,'STAGED_INPUT')
            tokens[name]=H.token(os.stat(name,dir_fd=self.tx.fd,follow_symlinks=False))
            require(before==tokens[name])
        return files,tokens
    def link(self):
        before=os.stat('active',dir_fd=self.root.fd,follow_symlinks=False)
        require(stat.S_ISLNK(before.st_mode) and H.identity(before)==self.bindings['final_active_identity'],stage='PUBLICATION')
        require(os.readlink('active',dir_fd=self.root.fd)==self.bindings['final_active'],stage='PUBLICATION')
        require(H.token(before)==H.token(os.stat('active',dir_fd=self.root.fd,follow_symlinks=False)),stage='PUBLICATION')
        return H.token(before)
    def revalidate(self,commit):
        source_guard(commit)
        require(sorted(os.listdir(self.transactions.fd))==['f-'+F_ID],'CONFLICT','POSTVALIDATION')
        require(self.read_transaction()==(self.files,self.file_tokens),stage='POSTVALIDATION')
        require(H.read_file(self.bundle,'construction-tree.json','STAGED_INPUT',0o400,H.TREE_LIMIT)==self.tree_raw,stage='POSTVALIDATION')
        require(self.final.identity==self.bindings['final_environment_identity'],stage='PUBLICATION')
        require(H.tree_entries(self.final)==self.expected,stage='POSTVALIDATION')
        link=self.link()
        if hasattr(self,'active_token'):require(link==self.active_token,stage='POSTVALIDATION')
        self.active_token=link
        previous=H.read_file(self.root,'previous-active','POSTVALIDATION')
        info=os.stat('previous-active',dir_fd=self.root.fd,follow_symlinks=False)
        require(previous==b'NONE\n' and H.identity(info)==self.bindings['final_previous_identity'],stage='PUBLICATION')
        if hasattr(self,'previous_token'):require(H.token(info)==self.previous_token,stage='POSTVALIDATION')
        self.previous_token=H.token(info)
        raw=H.read_file(self.tools,CLIENT.name,'POSTVALIDATION',0o700)
        info=os.stat(CLIENT.name,dir_fd=self.tools.fd,follow_symlinks=False)
        require(H.digest(raw)==self.bindings['client_sha256']
            and dict(identity=H.identity(info),token=list(H.token(info)))==self.bindings['client_identity'],stage='PUBLICATION')
        self.client_raw=raw
        for name in (Path(self.bindings['original_construction_path']).name,):
            H.absent(self.final.parent,name,'POSTVALIDATION')
        for name in ('.active.pe4.tmp','.active.pe4.rollback.tmp'):
            H.absent(self.root,name,'POSTVALIDATION')
        self.root.check('POSTVALIDATION');self.tools.check('POSTVALIDATION')
    def probe(self):
        policy=loader_policy(self.final,self.expected,self.client_raw,self.distributions)
        raw=bounded(['./bin/python','-I','-B','-S','-c',child_script(policy)],'PROBE',
            env=ENV,cwd='/proc/self/fd/'+str(self.final.fd),pass_fds=(self.final.fd,))
        checks=H.parse(raw,'STAGED_INPUT',canonical_required=True)
        require(checks==CHECKS,stage='PROBE')
        return checks
    def publish(self,raw,state):
        parent=self.fs.open(Path('/tmp'),'STAGING_ALLOCATION')
        name='hioc-pe4-runtime-preflight-'+secrets.token_hex(16)
        state['evidence']='UNCONFIRMED';state['directory']='/tmp/'+name
        self.evidence=self.fs.child(parent,name,0o700,'STAGING_ALLOCATION')
        H.sync(self.evidence,parent,'STAGING_FSYNC')
        F.write_owned(self.evidence,'result.json',raw,0o600)
        H.sync(self.evidence,parent,'STAGING_FSYNC')
        require(os.listdir(self.evidence.fd)==['result.json'],stage='EVIDENCE')
        require(H.read_file(self.evidence,'result.json','STAGED_INPUT')==raw,stage='EVIDENCE')
        self.evidence_token=H.token(os.stat('result.json',dir_fd=self.evidence.fd,follow_symlinks=False))
        state['evidence']='CONFIRMED'
    def evidence_check(self,raw):
        require(os.listdir(self.evidence.fd)==['result.json'],stage='EVIDENCE')
        require(H.read_file(self.evidence,'result.json','STAGED_INPUT')==raw and
            H.token(os.stat('result.json',dir_fd=self.evidence.fd,follow_symlinks=False))==self.evidence_token,stage='EVIDENCE')

CHECKS={k:'PASS' for k in ('interpreter','dependency','websocket','client_detection','proxy_policy','runtime_unchanged')}
def execute(commit,state,backend_factory=Posix):
    backend=backend_factory()
    try:
        b=backend.preflight(commit);checks=backend.probe();backend.revalidate(commit)
        require(checks==CHECKS,stage='PROBE')
        raw=encode_result(result_record(commit,b,checks))
        backend.publish(raw,state);backend.revalidate(commit);backend.evidence_check(raw)
    finally:backend.close()
class Parser(argparse.ArgumentParser):
    def error(self,message):raise Failure('INVALID','ARGUMENTS')
def terminal(result,code,stage,state):
    for key,value in (('RESULT',result),('ERROR_CODE',code),('FAILURE_STAGE',stage),
        ('ROLLBACK_RECOMMENDED','FALSE'),('EVIDENCE_STATE',state['evidence']),
        ('EVIDENCE_DIR',state['directory']),('CREDENTIAL_USE','FALSE'),('NETWORK_CONNECTION_ATTEMPTED','FALSE')):
        print(key+'='+value)
def cli(arguments=None,backend_factory=Posix):
    state={'evidence':'NOT_CREATED','directory':'NONE'}
    try:
        p=Parser(add_help=False,allow_abbrev=False);p.add_argument('--governance-commit',required=True)
        args=p.parse_args(arguments)
        require(re.fullmatch('[0-9a-f]{40}',args.governance_commit),'INVALID','ARGUMENTS')
        execute(args.governance_commit,state,backend_factory);terminal('PASS','NONE','COMPLETE',state);return 0
    except Failure as e:terminal('FAIL',e.code,e.stage,state);return 2 if e.stage=='ARGUMENTS' else 1
    except H.Failure:terminal('FAIL','INVALID','HANDOFF',state);return 1
    except (OSError,F.Failure):terminal('FAIL','IO_FAILED','EVIDENCE',state);return 1
    except Exception:terminal('FAIL','UNEXPECTED_ERROR','UNEXPECTED',state);return 1

REVIEWED_MODULES=('websockets','websockets.imports','websockets.version','websockets.exceptions',
 'websockets.asyncio','websockets.asyncio.client','websockets.asyncio.compatibility',
 'websockets.asyncio.connection','websockets.asyncio.messages','websockets.client',
 'websockets.datastructures','websockets.extensions','websockets.extensions.base',
 'websockets.extensions.permessage_deflate','websockets.frames','websockets.headers',
 'websockets.http11','websockets.protocol','websockets.proxy','websockets.streams',
 'websockets.typing','websockets.uri','websockets.utils','websockets.speedups')
BASE_PATHS=('/usr/lib/python311.zip','/usr/lib/python3.11','/usr/lib/python3.11/lib-dynload')
def loader_policy(directory,entries,client_raw,distributions):
    members={}
    for e in entries:
        name='/'.join(os.fsdecode(bytes.fromhex(p)) for p in e['path'])
        if e['type']=='REGULAR_FILE' and name.startswith('lib/python3.11/site-packages/websockets/'):
            members[name.removeprefix('lib/python3.11/site-packages/')]=e
    interpreter=next(e for e in entries if e['path']==[b'bin'.hex(),b'python'.hex()])
    return dict(root=str(directory.path),fd=directory.fd,identity=directory.identity,
        interpreter=interpreter,members=members,client=client_raw.decode('utf-8'),
        client_sha256=F.C.CLIENT_SHA256,distributions=distributions,
        paths=list(BASE_PATHS),version=[3,11,2],soabi='cpython-311-aarch64-linux-gnu')

def child_require(value):
    if not value:raise RuntimeError('CONTROLLED_RUNTIME_INVALID')
def child_token(i):
    return (i.st_dev,i.st_ino,i.st_uid,i.st_gid,i.st_mode,i.st_nlink,i.st_size,i.st_mtime_ns,i.st_ctime_ns)
def child_expected(e):
    return (e['dev'],e['ino'],e['uid'],e['gid'],stat.S_IFREG|int(e['mode'],8),
            e['nlink'],e['size'],e['mtime_ns'],e['ctime_ns'])
def verified_open(relative,entry,policy):
    fd=os.dup(policy['fd'])
    try:
        parts=relative.split('/')
        child_require(all(p not in ('','.','..') for p in parts))
        for p in parts[:-1]:
            nextfd=os.open(p,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd)
            os.close(fd);fd=nextfd
        filefd=os.open(parts[-1],os.O_RDONLY|os.O_NOFOLLOW,dir_fd=fd)
    finally:os.close(fd)
    try:
        child_require(child_token(os.fstat(filefd))==child_expected(entry))
        raw=bytearray()
        while True:
            block=os.read(filefd,65536)
            if not block:break
            raw.extend(block);child_require(len(raw)<=64*1024*1024)
        child_require(hashlib.sha256(raw).hexdigest()==entry['sha256'])
        child_require(child_token(os.fstat(filefd))==child_expected(entry))
        os.lseek(filefd,0,os.SEEK_SET)
        return filefd,bytes(raw)
    except BaseException:os.close(filefd);raise
class SourceLoader(importlib.abc.Loader):
    def __init__(self,name,member,package,policy):
        self.name,self.member,self.package,self.policy=name,member,package,policy
    def create_module(self,spec):return None
    def exec_module(self,module):
        fd,raw=verified_open('lib/python3.11/site-packages/'+self.member,self.policy['members'][self.member],self.policy)
        try:
            filename=self.policy['root']+'/lib/python3.11/site-packages/'+self.member
            module.__file__=filename;module.__cached__=None
            if self.package:module.__path__=[os.path.dirname(filename)]
            exec(compile(raw,filename,'exec',dont_inherit=True),module.__dict__)
        finally:os.close(fd)
class NativeLoader(importlib.machinery.ExtensionFileLoader):
    def __init__(self,name,policy):
        member='websockets/speedups.cpython-311-aarch64-linux-gnu.so'
        self.fd,raw=verified_open('lib/python3.11/site-packages/'+member,policy['members'][member],policy)
        self.entry=policy['members'][member]
        super().__init__(name,'/proc/self/fd/'+str(self.fd))
    def create_module(self,spec):
        child_require(child_token(os.fstat(self.fd))==child_expected(self.entry))
        return super().create_module(spec)
    def exec_module(self,module):
        try:
            child_require(child_token(os.fstat(self.fd))==child_expected(self.entry))
            super().exec_module(module)
            child_require(child_token(os.fstat(self.fd))==child_expected(self.entry))
        finally:os.close(self.fd)
class Finder(importlib.abc.MetaPathFinder):
    def __init__(self,policy):self.policy=policy
    def find_spec(self,fullname,path=None,target=None):
        if fullname.partition('.')[0]=='websockets':
            child_require(fullname in REVIEWED_MODULES)
            if fullname=='websockets.speedups':
                loader=NativeLoader(fullname,self.policy)
                return importlib.util.spec_from_file_location(fullname,loader.path,loader=loader)
            prefix=fullname.replace('.','/')
            package=prefix+'/__init__.py' in self.policy['members']
            member=prefix+('/__init__.py' if package else '.py')
            child_require(member in self.policy['members'])
            return importlib.util.spec_from_loader(fullname,SourceLoader(fullname,member,package,self.policy),is_package=package)
        child_require(fullname.partition('.')[0] in sys.stdlib_module_names)
        for f in (importlib.machinery.BuiltinImporter,importlib.machinery.FrozenImporter):
            spec=f.find_spec(fullname,path)
            if spec is not None:return spec
        spec=importlib.machinery.PathFinder.find_spec(fullname,self.policy['paths'] if path is None else path)
        child_require(spec is not None and spec.origin is not None and
            any(spec.origin.startswith(p.rstrip('/')+'/') for p in self.policy['paths']))
        return spec

def deny_network(*args,**kwargs):raise RuntimeError('NETWORK_FORBIDDEN')
def deny_credentials(*args,**kwargs):raise RuntimeError('CREDENTIAL_FORBIDDEN')
def install_prohibitions():
    import socket, getpass
    def audit(event,args):
        if event in ('socket.connect','socket.getaddrinfo','socket.gethostbyname','socket.sendto','socket.sendmsg'):
            deny_network()
    sys.addaudithook(audit)
    socket.create_connection=deny_network;socket.getaddrinfo=deny_network
    for name in ('connect','connect_ex','sendto','sendmsg'):
        if hasattr(socket.socket,name):setattr(socket.socket,name,deny_network)
    getpass.getpass=deny_credentials

def check_capabilities(module,connect,InvalidStatus,PayloadTooBig,Response,Headers):
    child_require(module.__version__=='16.1.1' and module.connect is connect
        and connect.__module__=='websockets.asyncio.client')
    parameters=inspect.signature(connect).parameters
    child_require({'max_size','proxy','open_timeout','close_timeout'}<=set(parameters)
        and any(p.kind is inspect.Parameter.VAR_KEYWORD for p in parameters.values())
        and issubclass(InvalidStatus,Exception) and issubclass(PayloadTooBig,Exception))
    response=Response(302,'Found',Headers({'Location':'ws://192.168.100.251:8123/api/websocket'}))
    obj=object.__new__(connect);obj.uri='ws://192.168.100.251:8123/api/websocket';obj.connection_kwargs={'sock':object()}
    refusal=obj.process_redirect(InvalidStatus(response))
    child_require(isinstance(refusal,ValueError) and 'preexisting socket' in str(refusal))

def client_detection(raw,expected,environment):
    import types
    child_require(hashlib.sha256(raw).hexdigest()==expected)
    client=types.ModuleType('hioc_g_verified_client');client.__file__='<verified-frozen-client>'
    sys.modules[client.__name__]=client
    exec(compile(raw,client.__file__,'exec',dont_inherit=True),client.__dict__)
    for name in ('run','acquire_token','rest_check','websockets_check'):
        child_require(hasattr(client,name));setattr(client,name,deny_credentials if name=='acquire_token' else deny_network)
    child_require(client.detect_websocket_client()=='PYTHON_WEBSOCKETS')
    child_require(dict(os.environ)==environment and client.proxy_influence_present(dict(os.environ)) is False)
    child_require(client.proxy_influence_present({'HTTPS_PROXY':'forbidden'}) is True)

def child_probe(policy):
    import sysconfig, importlib.metadata as metadata
    child_require(list(sys.path)==policy['paths'] and 'site' not in sys.modules)
    child_require(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.ignore_environment)
    child_require(list(sys.version_info[:3])==policy['version'] and sys.implementation.name=='cpython'
        and sys.prefix==sys.base_prefix=='/usr' and sysconfig.get_config_var('SOABI')==policy['soabi'])
    for p in policy['paths']:
        current=Path(p)
        while current!=current.parent:
            if os.path.lexists(current):
                i=os.lstat(current);child_require(not stat.S_ISLNK(i.st_mode) and i.st_uid==0 and not stat.S_IMODE(i.st_mode)&0o022)
            current=current.parent
    i=os.fstat(policy['fd'])
    child_require(dict(dev=i.st_dev,ino=i.st_ino,uid=i.st_uid,gid=i.st_gid,mode=f'{stat.S_IMODE(i.st_mode):04o}')==policy['identity'])
    fd,raw=verified_open('bin/python',policy['interpreter'],policy)
    try:child_require(child_token(os.stat(sys.executable))==child_expected(policy['interpreter']))
    finally:os.close(fd)
    child_require(dict(os.environ)==ENV and not any(k.lower().endswith('_proxy') for k in os.environ))
    install_prohibitions()
    finder=Finder(policy);sys.meta_path=[finder,importlib.machinery.BuiltinImporter,importlib.machinery.FrozenImporter]
    site=policy['root']+'/lib/python3.11/site-packages'
    distributions=list(metadata.distributions(path=[site]))
    pairs=[(d.metadata['Name'].lower(),d.version) for d in distributions]
    child_require(len(pairs)==len(dict(pairs)) and dict(pairs)==policy['distributions'])
    import websockets
    from websockets.asyncio.client import connect
    from websockets.exceptions import InvalidStatus,PayloadTooBig
    from websockets.http11 import Response
    from websockets.datastructures import Headers
    import websockets.speedups
    check_capabilities(websockets,connect,InvalidStatus,PayloadTooBig,Response,Headers)
    client_detection(policy['client'].encode(),policy['client_sha256'],ENV)
    child_require(sys.path==policy['paths'] and sys.meta_path==[finder,importlib.machinery.BuiltinImporter,importlib.machinery.FrozenImporter])
    print(json.dumps(CHECKS,sort_keys=True,separators=(',',':')))

def child_script(policy):
    prelude="import sys\n"
    prelude+="if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode) or 'site' in sys.modules: raise RuntimeError('CONTROLLED_STARTUP_INVALID')\n"
    prelude+="import os,stat,hashlib,json,inspect,importlib.abc,importlib.machinery,importlib.util\nfrom pathlib import Path\n"
    prelude+="POLICY="+repr(policy)+"\nENV="+repr(ENV)+"\nCHECKS="+repr(CHECKS)+"\nREVIEWED_MODULES="+repr(REVIEWED_MODULES)+"\n"
    definitions=(child_require,child_token,child_expected,verified_open,SourceLoader,NativeLoader,Finder,
        deny_network,deny_credentials,install_prohibitions,check_capabilities,client_detection,child_probe)
    return prelude+'\n'.join(inspect.getsource(x) for x in definitions)+'\nchild_probe(POLICY)\n'
