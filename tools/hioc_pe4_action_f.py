"""Publication-only Action F: one-shot, durable intent journal; no environment code."""
from __future__ import annotations
import argparse, copy, errno, json, os, re, secrets, stat, subprocess, sys
from pathlib import Path
try:
    import fcntl
except ImportError:
    fcntl = None
try:
    from . import hioc_pe4_action_e_handoff as H
    from . import hioc_pe4_runtime_common as C
except ImportError:
    import hioc_pe4_action_e_handoff as H
    import hioc_pe4_runtime_common as C

ACCEPTED = 'governance/pe4/accepted-action-e.json'
ACCEPTED_SHA = '1ac94f233bf543cafdc81b1f530177bd1c84d46ae13a7a686b33d34032d50c14'
RECORD_SCHEMA = 'governance/pe4/action-f-record.schema.json'
LIMIT = 65536
STAGES = ('ARGUMENTS','TARGET','SOURCE','HANDOFF','CONSTRUCTION','PRECONDITIONS',
          'LOCK','TRANSACTION','JOURNAL','CLIENT','ENVIRONMENT','PREVIOUS',
          'ACTIVE_STAGE','ACTIVE_SWITCH','POSTVALIDATION','RESULT','COMPLETION','COMPLETE','UNEXPECTED')
CODES = ('NONE','INVALID','MISMATCH','CONFLICT','UNAVAILABLE','IO_FAILED',
         'LIMIT_EXCEEDED','UNSTABLE','LOCK_BUSY','UNRESOLVED_TRANSACTION','UNEXPECTED_ERROR')
STATES = ('NONE','CLIENT_ONLY','ENVIRONMENT_PUBLISHED','ACTIVE_SWITCHED','COMPLETE','UNCERTAIN')
OPERATIONS = ('CLIENT','ENVIRONMENT','PREVIOUS','ACTIVE_STAGE','ACTIVE_SWITCH')
EVENTS = ('PREPARED',*(x+'_'+y for x in OPERATIONS for y in ('INTENT','CONFIRMED')),
          'POST_VERIFIED','RESULT','RESULT_REFERENCE','COMMITTED')
OWN = ('tools/hioc-pe4-runtime-publish.py','tools/hioc_pe4_action_f.py',RECORD_SCHEMA,ACCEPTED)
PROTECTED = tuple(p for p in H.E_PROTECTED if p != 'tools/hioc-pe4-runtime-publish.py') + H.OWN_SOURCE

class Failure(Exception):
    def __init__(self,code,stage):
        if code not in CODES or stage not in STAGES: raise ValueError('finite contract')
        self.code,self.stage=code,stage
        super().__init__(code)

def require(value,code='MISMATCH',stage='HANDOFF'):
    if not value: raise Failure(code,stage)

def record(document):
    schema=H.parse((H.REPOSITORY/RECORD_SCHEMA).read_bytes(),'STAGED_INPUT')
    H.validate(document,schema)
    require(document['event'] in EVENTS,'INVALID','JOURNAL')
    return H.canonical(document,LIMIT)

def same_entries(expected,actual,published=False):
    expected,actual=copy.deepcopy(expected),copy.deepcopy(actual)
    if published:
        # rename may change only the construction root ctime, not descendants.
        for entries in (expected,actual):
            require(entries and entries[0]['path']==[],'INVALID','CONSTRUCTION')
            entries[0].pop('ctime_ns',None)
    require(expected==actual,'MISMATCH','CONSTRUCTION')

def write_owned(directory,name,raw,mode):
    # Keep the created inode bound to its name through write, fsync and reread.
    require(mode in (0o600,0o700) and len(raw)<=LIMIT,'LIMIT_EXCEEDED','JOURNAL')
    directory.check('BUNDLE_WRITE')
    fd=os.open(name,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,mode,dir_fd=directory.fd)
    try:
        created=os.fstat(fd)
        require(stat.S_ISREG(created.st_mode) and created.st_nlink==1 and
                created.st_uid==os.getuid() and created.st_gid==os.getgid(),'INVALID','JOURNAL')
        view=memoryview(raw)
        while view:
            count=os.write(fd,view)
            require(count>0,'IO_FAILED','JOURNAL')
            view=view[count:]
        os.fchmod(fd,mode);os.fsync(fd)
        completed=os.fstat(fd)
        require(H.identity(created)==dict(H.identity(completed),mode=H.identity(created)['mode']),'UNSTABLE','JOURNAL')
        require(stat.S_IMODE(completed.st_mode)==mode and completed.st_nlink==1 and completed.st_size==len(raw),'MISMATCH','JOURNAL')
        require(H.token(completed)==H.token(os.stat(name,dir_fd=directory.fd,follow_symlinks=False)),'UNSTABLE','JOURNAL')
    finally:os.close(fd)
    require(H.read_file(directory,name,'POSTVALIDATION',mode)==raw,'MISMATCH','JOURNAL')
    require(H.token(completed)==H.token(os.stat(name,dir_fd=directory.fd,follow_symlinks=False)),'UNSTABLE','JOURNAL')
    directory.check('POSTVALIDATION')
    return completed

def git(args):
    env={'PATH':'/usr/bin:/bin','HOME':'/nonexistent','LANG':'C.UTF-8','LC_ALL':'C.UTF-8',
         'GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':'/dev/null',
         'GIT_NO_REPLACE_OBJECTS':'1','GIT_OPTIONAL_LOCKS':'0'}
    p=subprocess.run(['/usr/bin/git','--no-replace-objects','-c','core.fsmonitor=false',
      '-c','core.untrackedCache=false','-c','core.hooksPath=/dev/null','-c','submodule.recurse=false',
      '-C',str(H.SOURCE),*args],env=env,stdin=subprocess.DEVNULL,capture_output=True,timeout=60)
    require(p.returncode==0 and len(p.stdout)<=H.TREE_LIMIT and len(p.stderr)<=LIMIT,'INVALID','SOURCE')
    return p.stdout

def source_guard(commit,accepted):
    require(H.SOURCE==H.REPOSITORY,'INVALID','SOURCE')
    require(re.fullmatch('[0-9a-f]{40}',commit) is not None,'INVALID','SOURCE')
    for args,wanted in ((['branch','--show-current'],b'main'),(['rev-parse','HEAD'],commit.encode()),
                        (['rev-parse','refs/remotes/origin/main'],commit.encode()),
                        (['rev-parse','--is-shallow-repository'],b'false')):
        require(git(args).strip()==wanted,'MISMATCH','SOURCE')
    require(not git(['status','--porcelain','--untracked-files=all']).strip(),'CONFLICT','SOURCE')
    require(git(['rev-list','--left-right','--count','HEAD...origin/main']).split()==[b'0',b'0'],'MISMATCH','SOURCE')
    for op in ('MERGE_HEAD','CHERRY_PICK_HEAD','REVERT_HEAD','REBASE_HEAD',
               'rebase-merge','rebase-apply','sequencer','BISECT_START'):
        p=Path(os.fsdecode(git(['rev-parse','--git-path',op]).strip()))
        if not p.is_absolute(): p=H.SOURCE/p
        require(not os.path.lexists(p),'CONFLICT','SOURCE')
    hist=accepted['historical'];capture=accepted['capture']['source_commit']
    for a,b in ((hist['d_producer'],hist['e_execution_consumer']),
                (hist['e_execution_consumer'],capture),(capture,commit)):
        git(['merge-base','--is-ancestor',a,b])
    for p in PROTECTED:
        reference=capture if p in H.OWN_SOURCE else hist['e_execution_consumer']
        require(git(['rev-parse',reference+':'+p])==git(['rev-parse',commit+':'+p]),'MISMATCH','SOURCE')
    for p in (*PROTECTED,*OWN,'tools/hioc-pe4-ha-auth-capability.py'):
        require(git(['hash-object','--path='+p,str(H.SOURCE/p)]).strip()
                ==git(['rev-parse',commit+':'+p]).strip(),'MISMATCH','SOURCE')
    require(H.digest(git(['show',commit+':'+ACCEPTED]))==ACCEPTED_SHA,'MISMATCH','SOURCE')

def verify_launcher():
    require(sys.executable=='/usr/bin/python3' and sys.implementation.name=='cpython'
            and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,
            'INVALID','TARGET')

def accepted_manifest():
    raw=(H.REPOSITORY/ACCEPTED).read_bytes()
    require(H.digest(raw)==ACCEPTED_SHA,'MISMATCH','HANDOFF')
    doc=H.record('handoff',H.parse(raw,'STAGED_INPUT',canonical_required=True))
    require(doc['approval']['state']=='ACCEPTED' and
            doc['revalidated_observables']==H.observables(),'INVALID','HANDOFF')
    for field in ('authorization_reference','decisions_record','master_plan_record'):
        require(doc['approval'][field] and '\n' not in doc['approval'][field],'INVALID','HANDOFF')
    return doc

def snapshot_bindings(accepted,tree):
    hist=accepted['historical']
    by={tuple(H.component(p) for p in e['path']):e for e in tree['entries']}
    root=by.get(())
    require(root and {k:root[k] for k in hist['root']}==hist['root'],'MISMATCH','CONSTRUCTION')
    interpreter=by.get((b'bin',b'python'))
    require(interpreter and interpreter['type']=='REGULAR_FILE' and
            {k:interpreter[k] for k in hist['interpreter']}==hist['interpreter'],'MISMATCH','CONSTRUCTION')
    require(tree['bindings']['interpreter_identity']=={k:interpreter[k] for k in ('dev','ino','uid','gid','mode')},'MISMATCH','CONSTRUCTION')
    native=by.get((b'lib',b'python3.11',b'site-packages')+tuple(hist['native_member'].encode().split(b'/')))
    require(native and native['type']=='REGULAR_FILE' and native['sha256']==hist['native_sha256'],'MISMATCH','CONSTRUCTION')
    for name,binding,mode in ((H.MARKER,'d_marker_sha256','0400'),('pyvenv.cfg','configuration_sha256',None)):
        entry=by.get((os.fsencode(name),))
        require(entry and entry['type']=='REGULAR_FILE' and entry['sha256']==tree['bindings'][binding]
                and (mode is None or entry['mode']==mode),'MISMATCH','CONSTRUCTION')

def bundle(fs,accepted):
    path=Path(accepted['durable_bundle']['directory'])
    require(path.parent==H.HANDOFFS and path.name=='action-e-'+accepted['historical']['e_execution_consumer'],'INVALID','HANDOFF')
    d=fs.open(path,'STAGED_INPUT',0o500)
    raw=H.read_file(d,'manifest.json','STAGED_INPUT',0o400)
    require(H.digest(raw)==accepted['durable_bundle']['manifest_sha256'])
    manifest=H.record('durable-bundle',H.parse(raw,'STAGED_INPUT',canonical_required=True))
    require(manifest['historical']==accepted['historical'] and
            manifest['capture_id']==accepted['capture']['capture_id'] and
            manifest['capture_source_commit']==accepted['capture']['source_commit'] and
            manifest['continuity_class']==accepted['continuity']['evidence_class'])
    names=['action-d-result.json','action-e-result.json','construction-tree.json','continuity-attestation.json']
    require([i['name'] for i in manifest['inventory']]==names)
    payloads={'manifest.json':raw}
    for item in manifest['inventory']:
        require(item['mode']=='0400')
        name=item['name']
        raw=H.read_file(d,name,'STAGED_INPUT',0o400,H.TREE_LIMIT if name=='construction-tree.json' else LIMIT)
        require(len(raw)==item['size'] and H.digest(raw)==item['sha256'])
        payloads[name]=raw
    H.check_files(d,payloads,0o400,'STAGED_INPUT')
    tree=H.parse(payloads['construction-tree.json'],'STAGED_INPUT',H.TREE_LIMIT,True)
    H.validate_tree(tree)
    require(H.digest(payloads['construction-tree.json'])==accepted['capture']['tree_sha256'])
    require(tree['root_path']==accepted['historical']['construction_path'])
    att=H.record('continuity-attestation',H.parse(payloads['continuity-attestation.json'],'STAGED_INPUT',canonical_required=True))
    require(H.digest(payloads['continuity-attestation.json'])==accepted['continuity']['attestation_sha256'])
    require(att['historical']==accepted['historical'] and
            att['capture_id']==manifest['capture_id'] and
            att['capture_source_commit']==manifest['capture_source_commit'] and
            att['preservation_source_commit']==manifest['preservation_source_commit'] and
            att['capture_manifest_sha256']==accepted['capture']['manifest_sha256'] and
            att['capture_report_sha256']==accepted['capture']['report_sha256'] and
            att['construction_tree_sha256']==accepted['capture']['tree_sha256'] and
            att['fact_sources']==accepted['revalidated_observables'])
    for field in ('historical_recursive_snapshot_persisted','historical_recursive_continuity_machine_proven','limitation'):
        require(att[field]==accepted['continuity'][field])
    require(att['evidence_class']==accepted['continuity']['evidence_class'])
    hist=accepted['historical']
    for name,key in (('action-d-result.json','d_evidence_sha256'),('action-e-result.json','e_evidence_sha256')):
        require(H.digest(payloads[name])==hist[key])
    H.validate(H.parse(payloads['action-e-result.json'],'STAGED_INPUT',canonical_required=True),
               H.schema('handoff')['properties']['e_semantics'])
    for key in ('d_evidence_sha256','native_sha256'):
        require(tree['bindings'][key]==hist[key])
    return d,payloads,tree

class Posix:
    """Descriptor-bound OS adapter; tests replace only OS-facing operations."""
    def __init__(self):
        self.fs=H.Filesystem();self.locked=False;self.tx=None;self.payloads=None;self.record_pins={}
    def close(self):
        # Retained kernel lock lasts through all durable completion checks.
        self.fs.close()
    def preflight(self,commit):
        verify_launcher()
        H.target_guard()
        self.accepted=accepted_manifest()
        source_guard(commit,self.accepted)
        self.root=self.fs.open(H.PE4,'CONSTRUCTION_HIERARCHY',0o750)
        require(fcntl is not None,'UNAVAILABLE','LOCK')
        try: fcntl.flock(self.root.fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError: raise Failure('LOCK_BUSY','LOCK')
        self.locked=True
        self.env=self.fs.open(H.ENVIRONMENTS,'CONSTRUCTION_HIERARCHY',0o750)
        self.tools=self.fs.open(C.CLIENT_TARGET.parent,'CONSTRUCTION_HIERARCHY')
        require(self.tools.identity['uid']==os.getuid() and self.tools.identity['gid']==os.getgid(),'INVALID','PRECONDITIONS')
        self.durable,self.payloads,self.tree=bundle(self.fs,self.accepted)
        snapshot_bindings(self.accepted,self.tree)
        self.originals()
        self.construction=self.fs.open(Path(self.accepted['historical']['construction_path']),'CONSTRUCTION_HIERARCHY',0o750)
        require(self.construction.identity==self.accepted['historical']['root'],'MISMATCH','CONSTRUCTION')
        H.verify_construction(self.construction,self.tree)
        marker=H.read_file(self.construction,H.MARKER,'RETAINED_IDENTITY',0o400)
        require(H.digest(marker)==self.tree['bindings']['d_marker_sha256'],'MISMATCH','CONSTRUCTION')
        m=H.parse(marker,'RETAINED_IDENTITY',canonical_required=True)
        require(m['governance_commit']==self.accepted['historical']['d_producer'] and
                m['construction_directory']==self.construction.path.as_posix() and
                m['evidence_sha256']==self.accepted['historical']['d_evidence_sha256'] and
                m['result']=='PASS','MISMATCH','CONSTRUCTION')
        self.final=self.accepted['historical']['environment_identity']
        H.absent(self.env,self.final,'CONSTRUCTION_HIERARCHY')
        # This accepted first-publication handoff records PUBLICATION_ABSENT.
        for name in ('active','previous-active','.active.pe4.tmp','.active.pe4.rollback.tmp'):
            H.absent(self.root,name,'CONSTRUCTION_HIERARCHY')
        self.transactions=None
        try: os.stat('transactions',dir_fd=self.root.fd,follow_symlinks=False)
        except FileNotFoundError: pass
        else:
            self.transactions=self.fs.open(H.PE4/'transactions','CONSTRUCTION_HIERARCHY',0o700)
            require(not os.listdir(self.transactions.fd),'UNRESOLVED_TRANSACTION','PRECONDITIONS')
        self.client_raw=git(['show',commit+':tools/hioc-pe4-ha-auth-capability.py'])
        require(H.digest(self.client_raw)==C.CLIENT_SHA256,'MISMATCH','CLIENT')
        self.client_before=self.client_info()
        return dict(current_consumer=commit,accepted_manifest_sha256=ACCEPTED_SHA,
          historical=self.accepted['historical'],durable_bundle_sha256=self.accepted['durable_bundle']['manifest_sha256'],
          tree_sha256=self.accepted['capture']['tree_sha256'],attestation_sha256=self.accepted['continuity']['attestation_sha256'],
          original_construction_path=self.construction.path.as_posix(),original_construction_identity=self.construction.identity,
          final_environment_path=(H.ENVIRONMENTS/self.final).as_posix(),final_environment_identity='NONE',
          client_path=C.CLIENT_TARGET.as_posix(),client_sha256=C.CLIENT_SHA256,client_identity=self.client_before,
          original_root_ctime_ns=self.tree['entries'][0]['ctime_ns'],final_root_ctime_ns='NONE',
          final_active_identity='NONE',final_previous_identity='NONE',
          client_disposition='EXACT_PREEXISTING' if self.client_before!='NONE' else 'ABSENT',
          original_active='NONE',original_previous='NONE',final_active='NONE',final_previous='NONE')
    def originals(self):
        hist=self.accepted['historical']
        first=not hasattr(self,'original_presence')
        if first:self.original_presence={}
        for field,sha,name,stage in (('e_evidence_directory','e_evidence_sha256','action-e-result.json','E_EVIDENCE'),('d_evidence_directory','d_evidence_sha256','action-d-result.json','D_EVIDENCE')):
            path=Path(hist[field])
            try: os.lstat(path)
            except FileNotFoundError:
                if first:self.original_presence[field]=False
                else:require(not self.original_presence[field],'UNSTABLE','HANDOFF')
                continue
            if first:self.original_presence[field]=True
            else:require(self.original_presence[field],'UNSTABLE','HANDOFF')
            require(H.evidence(self.fs,path,hist[sha],stage)==self.payloads[name],'MISMATCH','HANDOFF')
    def client_info(self):
        self.tools.check('POSTVALIDATION')
        try: before=os.stat(C.CLIENT_TARGET.name,dir_fd=self.tools.fd,follow_symlinks=False)
        except FileNotFoundError: return 'NONE'
        raw=H.read_file(self.tools,C.CLIENT_TARGET.name,'POSTVALIDATION',0o700)
        require(H.digest(raw)==C.CLIENT_SHA256,'MISMATCH','CLIENT')
        require(H.token(before)==H.token(os.stat(C.CLIENT_TARGET.name,dir_fd=self.tools.fd,follow_symlinks=False)),'UNSTABLE','CLIENT')
        return dict(identity=H.identity(before),token=list(H.token(before)))
    def revalidate(self,commit):
        source_guard(commit,self.accepted)
        H.check_files(self.durable,self.payloads,0o400,'POSTVALIDATION')
        self.originals()
        H.verify_construction(self.construction,self.tree)
        require(self.client_info()==self.client_before,'UNSTABLE','CLIENT')
        H.absent(self.env,self.final,'POSTVALIDATION')
        for name in ('active','previous-active','.active.pe4.tmp','.active.pe4.rollback.tmp'):
            H.absent(self.root,name,'POSTVALIDATION')
        if self.transactions is not None: require(not os.listdir(self.transactions.fd),'UNRESOLVED_TRANSACTION','PRECONDITIONS')
    def allocate(self,tid):
        if self.transactions is None:
            self.transactions=self.fs.child(self.root,'transactions',0o700,'BUNDLE_ALLOCATION')
            H.sync(self.transactions,self.root,'BUNDLE_FSYNC')
        self.tx=self.fs.child(self.transactions,'f-'+tid,0o700,'BUNDLE_ALLOCATION')
        H.sync(self.tx,self.transactions,'BUNDLE_FSYNC')
        return self.tx.path.as_posix()
    def write(self,name,raw):
        completed=write_owned(self.tx,name,raw,0o600)
        self.record_pins[name]=H.token(completed)
        H.sync(self.tx,self.transactions,'BUNDLE_FSYNC')
        require(self.read(name)==raw,'MISMATCH','JOURNAL')
    def read(self,name):
        require(name in self.record_pins,'INVALID','JOURNAL')
        before=os.stat(name,dir_fd=self.tx.fd,follow_symlinks=False)
        require(H.token(before)==self.record_pins[name],'UNSTABLE','JOURNAL')
        raw=H.read_file(self.tx,name,'POSTVALIDATION',0o600)
        require(H.token(os.stat(name,dir_fd=self.tx.fd,follow_symlinks=False))==self.record_pins[name],'UNSTABLE','JOURNAL')
        return raw
    def names(self): self.tx.check('POSTVALIDATION');return sorted(os.listdir(self.tx.fd))
    def mutate(self,operation,tid):
        if operation=='CLIENT':
            require(self.client_info()=='NONE','CONFLICT','CLIENT')
            self.temp_client='.'+C.CLIENT_TARGET.name+'.f-'+tid
            self.client_staged=write_owned(self.tools,self.temp_client,self.client_raw,0o700)
            H.sync(self.tools,self.tools.parent,'BUNDLE_FSYNC')
            staged=H.read_file(self.tools,self.temp_client,'POSTVALIDATION',0o700)
            require(staged==self.client_raw,'MISMATCH','CLIENT')
            require(H.token(self.client_staged)==H.token(os.stat(self.temp_client,dir_fd=self.tools.fd,follow_symlinks=False)),'UNSTABLE','CLIENT')
            H.noreplace(self.tools,self.temp_client,C.CLIENT_TARGET.name)
        elif operation=='ENVIRONMENT':
            H.verify_construction(self.construction,self.tree)
            H.noreplace(self.env,self.construction.path.name,self.final)
            self.construction.path=H.ENVIRONMENTS/self.final
            self.fs.directories[str(self.construction.path)]=self.construction
        elif operation=='PREVIOUS':
            self.temp_previous='.previous-active.f-'+tid
            previous=write_owned(self.root,self.temp_previous,b'NONE\n',0o600)
            H.sync(self.root,self.root.parent,'BUNDLE_FSYNC')
            require(H.token(previous)==H.token(os.stat(self.temp_previous,dir_fd=self.root.fd,follow_symlinks=False)),'UNSTABLE','PREVIOUS')
            self.previous_staged=H.identity(previous)
            self.previous_staged_token=H.token(previous)
            H.noreplace(self.root,self.temp_previous,'previous-active')
        elif operation=='ACTIVE_STAGE':
            self.temp_active='.active.f-'+tid
            self.root.check('POSTVALIDATION')
            os.symlink('environments/'+self.final,self.temp_active,dir_fd=self.root.fd)
            self.active_staged=H.identity(os.stat(self.temp_active,dir_fd=self.root.fd,follow_symlinks=False))
        elif operation=='ACTIVE_SWITCH':
            require(self.link(self.temp_active)==self.active_staged,'UNSTABLE','ACTIVE_SWITCH')
            H.noreplace(self.root,self.temp_active,'active')
        else: raise Failure('INVALID','UNEXPECTED')
    def link(self,name):
        self.root.check('POSTVALIDATION')
        i=os.stat(name,dir_fd=self.root.fd,follow_symlinks=False)
        require(stat.S_ISLNK(i.st_mode) and i.st_uid==os.getuid() and i.st_gid==os.getgid(),'INVALID','ACTIVE_SWITCH')
        require(os.readlink(name,dir_fd=self.root.fd)=='environments/'+self.final,'MISMATCH','ACTIVE_SWITCH')
        require(H.token(i)==H.token(os.stat(name,dir_fd=self.root.fd,follow_symlinks=False)),'UNSTABLE','ACTIVE_SWITCH')
        return H.identity(i)
    def confirm(self,operation,bindings):
        if operation=='CLIENT':
            now=self.client_info()
            require(now!='NONE' and now['identity']==H.identity(self.client_staged) and
                    now['token'][:-1]==list(H.token(self.client_staged))[:-1],'MISMATCH','CLIENT')
            H.sync(self.tools,self.tools.parent,'BUNDLE_FSYNC')
            require(self.client_info()==now,'UNSTABLE','CLIENT')
            bindings['client_identity']=now;bindings['client_disposition']='PUBLISHED'
        elif operation=='ENVIRONMENT':
            self.construction.check('POSTVALIDATION')
            published=H.tree_entries(self.construction)
            same_entries(self.tree['entries'],published,True)
            H.sync(self.construction,self.env,'BUNDLE_FSYNC');os.fsync(self.env.parent.fd)
            same_entries(published,H.tree_entries(self.construction))
            self.published_entries=copy.deepcopy(published)
            bindings['final_root_ctime_ns']=published[0]['ctime_ns']
            H.absent(self.env,Path(bindings['original_construction_path']).name,'POSTVALIDATION')
            bindings['final_environment_identity']=self.construction.identity
        elif operation=='PREVIOUS':
            require(H.read_file(self.root,'previous-active','POSTVALIDATION')==b'NONE\n','MISMATCH','PREVIOUS')
            require(H.identity(os.stat('previous-active',dir_fd=self.root.fd,follow_symlinks=False))==self.previous_staged,'UNSTABLE','PREVIOUS')
            info=os.stat('previous-active',dir_fd=self.root.fd,follow_symlinks=False)
            require(H.token(info)[:-1]==self.previous_staged_token[:-1],'UNSTABLE','PREVIOUS')
            self.previous_final_token=H.token(info)
            H.sync(self.root,self.root.parent,'BUNDLE_FSYNC')
            require(H.token(os.stat('previous-active',dir_fd=self.root.fd,follow_symlinks=False))==self.previous_final_token,'UNSTABLE','PREVIOUS')
            bindings['final_previous']='NONE'
            bindings['final_previous_identity']=self.previous_staged
        elif operation in ('ACTIVE_STAGE','ACTIVE_SWITCH'):
            name=self.temp_active if operation=='ACTIVE_STAGE' else 'active'
            require(self.link(name)==self.active_staged,'UNSTABLE',operation)
            H.sync(self.root,self.root.parent,'BUNDLE_FSYNC')
            require(self.link(name)==self.active_staged,'UNSTABLE',operation)
            if operation=='ACTIVE_SWITCH':
                bindings['final_active']='environments/'+self.final
                bindings['final_active_identity']=self.active_staged
    def not_completed(self,operation):
        # Absence proofs are read-only and never authorize retry or cleanup.
        parent,name=(self.tools,C.CLIENT_TARGET.name) if operation=='CLIENT' else (self.env,self.final) if operation=='ENVIRONMENT' else (self.root,'previous-active' if operation=='PREVIOUS' else self.temp_active if operation=='ACTIVE_STAGE' else 'active')
        parent.check('POSTVALIDATION')
        try: os.stat(name,dir_fd=parent.fd,follow_symlinks=False)
        except FileNotFoundError:
            if operation=='ENVIRONMENT':
                self.construction.check('POSTVALIDATION')
                H.verify_construction(self.construction,self.tree)
            if operation=='ACTIVE_SWITCH':
                require(self.link(self.temp_active)==self.active_staged,'UNSTABLE','ACTIVE_SWITCH')
            return True
        return False
    def postverify(self,bindings,commit):
        source_guard(commit,self.accepted)
        H.check_files(self.durable,self.payloads,0o400,'POSTVALIDATION')
        self.originals()
        same_entries(self.published_entries,H.tree_entries(self.construction))
        require(self.construction.identity==bindings['original_construction_identity'],'MISMATCH','POSTVALIDATION')
        require(self.client_info()==bindings['client_identity'],'UNSTABLE','POSTVALIDATION')
        require(self.link('active')==self.active_staged,'UNSTABLE','POSTVALIDATION')
        require(H.read_file(self.root,'previous-active','POSTVALIDATION')==b'NONE\n','MISMATCH','POSTVALIDATION')
        require(H.identity(os.stat('previous-active',dir_fd=self.root.fd,follow_symlinks=False))==self.previous_staged,'UNSTABLE','POSTVALIDATION')
        require(H.token(os.stat('previous-active',dir_fd=self.root.fd,follow_symlinks=False))==self.previous_final_token,'UNSTABLE','POSTVALIDATION')
        H.absent(self.env,Path(bindings['original_construction_path']).name,'POSTVALIDATION')
        for name in (getattr(self,'temp_client',''),self.temp_previous,self.temp_active):
            if name: H.absent(self.tools if name==getattr(self,'temp_client',None) else self.root,name,'POSTVALIDATION')
        self.root.check('POSTVALIDATION');self.env.check('POSTVALIDATION')

class Journal:
    def __init__(self,backend,tid,bindings,state):
        self.backend,self.tid,self.bindings,self.state=backend,tid,bindings,state
        self.records=[];self.head='NONE'
    def document(self,event,result_digest='NONE'):
        return dict(schema_version='2.0',record_type='ACTION_F_RECORD',transaction_id=self.tid,
          sequence=len(self.records),event=event,previous_record_sha256=self.head,
          bindings=copy.deepcopy(self.bindings),publication_state=self.state['publication'],
          recovery_required=self.state['recovery'],rollback_recommended=False,evidence_state=self.state['evidence'],
          result_sha256=result_digest,result='PASS' if event in ('RESULT','COMMITTED') else 'IN_PROGRESS',
          error_code='NONE',failure_stage='COMPLETE' if event in ('RESULT','COMMITTED') else 'JOURNAL')
    def append(self,event,result_digest='NONE'):
        raw=record(self.document(event,result_digest))
        name=str(len(self.records)).zfill(4)+'.json'
        self.backend.write(name,raw)
        self.records.append((name,raw));self.head=H.digest(raw)
    def verify(self,result_raw):
        previous='NONE'
        for index,(name,raw) in enumerate(self.records):
            reread=self.backend.read(name)
            require(reread==raw,'MISMATCH','COMPLETION')
            doc=H.parse(reread,'STAGED_INPUT',canonical_required=True);record(doc)
            require(doc['transaction_id']==self.tid and doc['sequence']==index and
                    doc['previous_record_sha256']==previous,'MISMATCH','COMPLETION')
            previous=H.digest(raw)
        require(self.backend.names()==sorted([n for n,_ in self.records]+['result.json']),'MISMATCH','COMPLETION')
        require(self.backend.read('result.json')==result_raw,'MISMATCH','COMPLETION')
        result=H.parse(result_raw,'STAGED_INPUT',canonical_required=True);record(result)
        require(result['event']=='RESULT' and result['result']=='PASS','INVALID','COMPLETION')
        reference=H.parse(self.records[-2][1],'STAGED_INPUT')
        require(reference['event']=='RESULT_REFERENCE' and reference['result_sha256']==H.digest(result_raw)
                and reference['sequence']==result['sequence']
                and reference['previous_record_sha256']==result['previous_record_sha256'],'MISMATCH','COMPLETION')
        tail=H.parse(self.records[-1][1],'STAGED_INPUT')
        require(tail['event']=='COMMITTED' and tail['result_sha256']==H.digest(result_raw)
                and tail['publication_state']=='COMPLETE' and tail['evidence_state']=='CONFIRMED' and not tail['recovery_required'],'MISMATCH','COMPLETION')
        expected=['PREPARED']
        if self.bindings['client_disposition']=='PUBLISHED':expected+=['CLIENT_INTENT','CLIENT_CONFIRMED']
        expected += [op+'_'+phase for op in OPERATIONS[1:] for phase in ('INTENT','CONFIRMED')]
        expected += ['POST_VERIFIED','RESULT_REFERENCE','COMMITTED']
        require([H.parse(raw,'STAGED_INPUT')['event'] for _,raw in self.records]==expected,'INVALID','COMPLETION')

def initial_state():
    return dict(publication='NONE',recovery=False,rollback=False,transaction='NONE',evidence='NOT_CREATED')

def execute(commit,state,backend_factory=Posix):
    backend=backend_factory();stage='TARGET';pending=False;allocated=False
    try:
        bindings=backend.preflight(commit)
        stage='PRECONDITIONS';backend.revalidate(commit)
        tid=secrets.token_hex(16)
        require(re.fullmatch('[0-9a-f]{32}',tid) is not None,'INVALID','TRANSACTION')
        stage='TRANSACTION'
        # Set locator before allocation: failures never lose a partial directory.
        state['transaction']=str(H.PE4/'transactions'/('f-'+tid))
        allocated=True;state['recovery']=True
        require(backend.allocate(tid)==state['transaction'],'MISMATCH','TRANSACTION')
        journal=Journal(backend,tid,bindings,state)
        stage='JOURNAL';journal.append('PREPARED')
        operations=list(OPERATIONS)
        if bindings['client_disposition']=='EXACT_PREEXISTING': operations.remove('CLIENT')
        for operation in operations:
            stage=operation
            prior_state=state['publication']
            # Treat even a torn intent write as unresolved; never retry it.
            journal.append(operation+'_INTENT')
            pending=True
            backend.mutate(operation,tid)
            backend.confirm(operation,bindings)
            if operation=='CLIENT':state['publication']='CLIENT_ONLY'
            if operation=='ENVIRONMENT':state['publication']='ENVIRONMENT_PUBLISHED'
            if operation=='ACTIVE_SWITCH':state['publication']='ACTIVE_SWITCHED'
            pending=False
            journal.append(operation+'_CONFIRMED')
        stage='POSTVALIDATION';backend.postverify(bindings,commit)
        journal.append('POST_VERIFIED')
        stage='RESULT';state['evidence']='UNCONFIRMED'
        result_raw=record(journal.document('RESULT'))
        backend.write('result.json',result_raw)
        require(backend.read('result.json')==result_raw,'MISMATCH','RESULT')
        state['evidence']='CONFIRMED'
        stage='COMPLETION';journal.append('RESULT_REFERENCE',H.digest(result_raw))
        state['publication']='COMPLETE'
        state['recovery']=False
        journal.append('COMMITTED',H.digest(result_raw))
        journal.verify(result_raw)
        backend.postverify(bindings,commit)
        state['recovery']=False
        # Close failures must prevent terminal PASS.
        closing=backend;backend=None;closing.close()
        return
    except Exception as exc:
        if pending:
            state['publication']='UNCERTAIN'
            if hasattr(backend,'not_completed'):
                try:
                    if backend.not_completed(operation):state['publication']=prior_state
                except Exception:pass
        if allocated: state['recovery']=True
        if stage=='COMPLETION' and state['publication']=='COMPLETE':state['publication']='ACTIVE_SWITCHED'
        if isinstance(exc,Failure):raise
        if isinstance(exc,H.Failure) and stage=='TARGET':
            stage={'TARGET':'TARGET','SOURCE':'SOURCE','HISTORY':'SOURCE','STAGED_INPUT':'HANDOFF','RETAINED_IDENTITY':'CONSTRUCTION','TREE_CAPTURE':'CONSTRUCTION','CONSTRUCTION_HIERARCHY':'PRECONDITIONS'}.get(exc.stage,stage)
        code=getattr(exc,'code','IO_FAILED' if isinstance(exc,OSError) else 'UNEXPECTED_ERROR')
        raise Failure(code if code in CODES else 'UNEXPECTED_ERROR',stage) from None
    finally:
        if backend is not None:
            try:backend.close()
            except Exception:
                state['recovery']=allocated
                raise Failure('IO_FAILED',stage) from None

class Parser(argparse.ArgumentParser):
    def error(self,message):raise Failure('INVALID','ARGUMENTS')

def terminal(result,code,stage,state):
    values=dict(RESULT=result,ERROR_CODE=code,FAILURE_STAGE=stage,
      ROLLBACK_RECOMMENDED='TRUE' if state['rollback'] else 'FALSE',
      PUBLICATION_STATE=state['publication'],RECOVERY_REQUIRED='TRUE' if state['recovery'] else 'FALSE',
      TRANSACTION_DIR=state['transaction'],EVIDENCE_STATE=state['evidence'],
      EVIDENCE_DIR=state['transaction'] if state['evidence']=='CONFIRMED' else 'NONE')
    for key,value in values.items():print(key+'='+value)

def cli(arguments=None,backend_factory=Posix):
    state=initial_state()
    try:
        p=Parser(description=__doc__)
        p.add_argument('--governance-commit',required=True)
        a=p.parse_args(arguments)
        require(re.fullmatch('[0-9a-f]{40}',a.governance_commit) is not None,'INVALID','ARGUMENTS')
        execute(a.governance_commit,state,backend_factory)
        terminal('PASS','NONE','COMPLETE',state);return 0
    except Failure as exc:
        terminal('FAIL',exc.code,exc.stage,state);return 2 if exc.stage=='ARGUMENTS' else 1
    except Exception:
        terminal('FAIL','UNEXPECTED_ERROR','UNEXPECTED',state);return 1
