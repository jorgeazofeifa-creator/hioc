#!/usr/bin/env python3
"""Current-baseline operations over the existing PE-7.3 controller/window.

Mutation functions are separate, owner-authorized entry points. CLI is read-only.
Historical entries are never adopted. No automatic recovery or mutation retries.
"""
from __future__ import annotations
import contextlib
import copy
import ctypes
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import uuid

ROOT = Path(__file__).resolve().parents[1]
ADAPTER_SHA = '1dc47e5c3fd6ec5fd98d9414e39bb8e3dc8b80d03ddb32b29d6625e79f5ee05b'
CONTRACT_SHA = '26ae2945cdc745732a5e40fcd0011bd6e7c21f3a8932a28f5c333f0754002bb6'
TARGET = {'hostname':'nutandpihole','runtime_root':'/home/jazofv1/hioc','uid':1000,'gid':1000}
CONTROL = 'backups/pe73-current-baseline.json'
PREFIX = 'backups/pe73-attempt-'

def require(value, code):
    if not value:
        raise ValueError(code)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def adapter():
    path=ROOT/'tools/pe73_successor_delivery.py'
    require(not path.is_symlink() and sha(path.read_bytes())==ADAPTER_SHA,'BASELINE_ADAPTER_IDENTITY')
    spec=importlib.util.spec_from_file_location('pe73_baseline_adapter',path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    return m

def contract():
    raw=(ROOT/'governance/pe7/pe73-verified-baseline-contract.json').read_bytes()
    require(sha(raw)==CONTRACT_SHA,'BASELINE_CONTRACT_IDENTITY')
    return json.loads(raw)

def read_control(w,fs,m):
    require(fs.snapshot(CONTROL,0o600)['exists'],'CURRENT_BASELINE_NOT_ESTABLISHED')
    value=w.d.parsed(fs.read(CONTROL))
    require(set(value)=={'version','baseline','active'} and value['version']==1,'CURRENT_BASELINE_INVALID')
    b=value['baseline']
    require(set(b)=={'id','status','target','payload_release','authorized_release','contract_sha256',
        'artifacts','compatibility','approval','recovery_reference'},'CURRENT_BASELINE_INVALID')
    require(re.fullmatch('[0-9a-f]{32}',b['id']) and b['status']=='APPROVED_VERIFIED' and
        b['target']==TARGET and b['authorized_release']==m['release'] and b['contract_sha256']==CONTRACT_SHA,
        'CURRENT_BASELINE_INVALID')
    require(b['payload_release'] in {m['prior_release'],m['release']},'BASELINE_RELEASE_NOT_AUTHORIZED')
    expected={x['path']:{'sha256':x['prior_sha256'] if b['payload_release']==m['prior_release'] else x['sha256'],
        'mode':w.d.MODES[x['path']],'uid':1000,'gid':1000,'type':'REGULAR'} for x in m['artifacts']}
    require(b['artifacts']==expected and b['compatibility']=={
        'scope':'PI3_RUNTIME_ARTIFACTS_ONLY','activation_authorized':False,
        'scheduler_sha256':contract()['original_scheduler_sha256']},'BASELINE_INVENTORY_OR_COMPATIBILITY')
    require(set(b['approval'])=={'reference','kind'} and b['approval']['kind']=='EXPLICIT_OWNER_OPERATION' and
        w.d.AUTH.fullmatch(b['approval']['reference']) and type(b['recovery_reference']) is dict and
        set(b['recovery_reference'])=={'kind','reference'} and
        b['recovery_reference']['kind'] in {'OPERATOR_SUPPLIED_RESTORATION','VERIFIED_TRANSACTION'} and
        type(b['recovery_reference']['reference']) is str and
        re.fullmatch('[A-Za-z0-9_/-]{8,160}',b['recovery_reference']['reference']), 'BASELINE_APPROVAL_INVALID')
    return value

class AttemptFS:
    """Existing NativeFS effects, transaction-local identities and current control only."""
    def __init__(self,operation):
        self.op=operation
    def __getattr__(self,name):
        return getattr(self.op.base,name)
    def guard(self):
        o=self.op
        v=read_control(o.w,o.base,o.manifest)
        require(v['active']==o.binding and sha(o.d.canonical(v['baseline']))==o.baseline_sha,
                'ACTIVE_TRANSACTION_OR_BASELINE_DRIFT')
        require(o.base.snapshot(CONTROL,0o600)==o.control_snapshot,'CURRENT_CONTROL_IDENTITY_DRIFT')
        if o.base.transaction_present():
            names=o.base.entries(o.d.TX)
            fixed={'attempt.json','journal.json','journal-next','terminal.json','window-crontab-original'} | {kind+str(i) for kind in ('stage-','backup-') for i in range(13)}
            require(len(names)<=256 and all(name in fixed or re.fullmatch(r'(?:recovery-[0-9a-f]{32}\.json|archived-[0-9a-f]{32})',name) for name in names),'TRANSACTION_UNEXPECTED_ENTRY')
            require(o.base.read(o.d.TX+'/attempt.json')==o.d.canonical(o.binding),'ATTEMPT_BINDING_DRIFT')
    @contextlib.contextmanager
    def mutex(self):
        o=self.op
        with o.base.mutex():
            o.ops.live_gate()
            if o.binding is None:
                o.claim()
            self.guard()
            yield
            # Finalization is a separate explicitly authorized transition.
            self.guard()
    def mkdir_tx(self):
        self.guard();self.op.base.mkdir_tx()
        self.op.base.write_new(self.op.d.TX+'/attempt.json',self.op.d.canonical(self.op.binding))
    def write_new(self,path,raw,mode=0o600):
        self.guard()
        require(path.startswith(self.op.d.TX+'/') and '..' not in Path(path).parts,'ATTEMPT_WRITE_SCOPE')
        self.op.base.write_new(path,raw,mode)
    def journal(self,value):
        self.guard();self.op.base.journal(value)
    def publish(self,path,raw,before,mode):
        self.guard();o=self.op
        require(path in o.d.ORDER and mode==o.d.MODES[path],'ATTEMPT_PUBLICATION_SCOPE')
        require(o.base.snapshot(path,mode)==before,'DESTINATION_DRIFT')
        if sha(raw)==before['sha256']:
            require(o.base.read(path,mode)==raw and o.base.snapshot(path,mode)==before,'UNCHANGED_ARTIFACT_DRIFT')
            return before
        require(path in o.manifest['changed_paths'],'ATTEMPT_PUBLICATION_SCOPE')
        return o.base.publish(path,raw,before,mode)
    def remove_installed(self,*args):
        raise ValueError('ATTEMPT_REMOVAL_FORBIDDEN')


def continuation_controller(w):
    class Controller(w.WindowController):
        """Resume an existing reverse restored prefix; first rollback uses original method."""
        def rollback(self,reference,binding):
            v=self._journal()
            if v['state']!='ROLLING_BACK':
                return super().rollback(reference,binding)
            self.consumers.consume_runtime('ROLLBACK',reference,binding)
            with self.consumers.hold(self.consumers.observe()):
                with self.fs.mutex():
                    v=self._journal()
                    require(w.d.sha(w.d.canonical(v))==binding and v['pending'] is None,'ROLLBACK_RESUME_DRIFT')
                    for i,path in enumerate(w.d.ORDER):
                        expected=v['restored'].get(path,v['installed'].get(path,v['baseline'][path]))
                        require(self.fs.snapshot(path,w.d.MODES[path])==expected,'ROLLBACK_DRIFT')
                        require(w.d.sha(self.fs.read(w.d.TX+'/backup-'+str(i)))==v['baseline'][path]['sha256'],'BACKUP_DRIFT')
                    self.fs.write_new(w.d.TX+'/recovery-'+uuid.uuid4().hex+'.json',w.d.canonical({
                        'kind':'CONTINUE_ROLLBACK','authorization':reference,'journal_sha256':binding}))
                    for path in reversed(w.d.ORDER):
                        if path not in v['installed'] or path in v['restored']:
                            continue
                        self.consumers.assert_active()
                        v['pending']=path;self._save(v,'ROLLBACK_INTENT:'+path)
                        raw=self.fs.read(w.d.TX+'/backup-'+str(w.d.ORDER.index(path)))
                        restored=self.fs.publish(path,raw,v['installed'][path],w.d.MODES[path])
                        require(restored['sha256']==v['baseline'][path]['sha256'],'ROLLBACK_NOT_VERIFIED')
                        v['restored'][path]=restored;v['pending']=None;self._save(v,'RESTORED:'+path)
                    for path in w.d.ORDER:
                        require(self.fs.snapshot(path,w.d.MODES[path])['sha256']==v['baseline'][path]['sha256'],'ROLLBACK_NOT_VERIFIED')
                    v['state']='ROLLED_BACK';self._save(v,'ROLLED_BACK')
                    return {'state':'ROLLED_BACK','restored_replacements':len(v['restored']),
                        'removed_new_files':0,'original_inode_or_ctime_restored':False}
    return Controller

class Operations:
    """One current authority record; old journals never enter routine admission."""
    def __init__(self,w,manifest,base,ops,source,source_reader,*,transaction_id=None,
                 target=None,tooling=None,establishment=False,recovery=False):
        self.w,self.d,self.manifest,self.base,self.ops=w,w.d,manifest,base,ops
        self.policy=contract()
        require(self.policy['payload_manifest_sha256']==sha((ROOT/'governance/pe7/pe73-successor-delivery.json').read_bytes()),'PAYLOAD_CONTRACT_MISMATCH')
        require((TARGET if target is None else target)==TARGET,'TARGET_IDENTITY')
        require(manifest['release']==self.policy['authorized_release'],'SOURCE_RELEASE_NOT_AUTHORIZED')
        self.source,self.source_reader=source,source_reader
        self.fresh_source()
        self.tooling=tooling
        require(type(self.tooling) is dict,'TOOLING_IDENTITY')
        require(set(self.tooling)=={'commit','tree'} and all(re.fullmatch('[0-9a-f]{40}',v) for v in self.tooling.values()),'TOOLING_IDENTITY')
        self.id=transaction_id or uuid.uuid4().hex
        require(type(self.id) is str and re.fullmatch('[0-9a-f]{32}',self.id),'TRANSACTION_ID_INVALID')
        self.d.TX=PREFIX+self.id;w.BACKUP=self.d.TX+'/window-crontab-original'
        self.binding=None;self.baseline=None;self.baseline_sha=None;self.control_snapshot=None
        self.establishment,self.recovery=establishment,recovery
        if not establishment:
            current=read_control(w,base,manifest);self.baseline=current['baseline']
            self.baseline_sha=sha(self.d.canonical(self.baseline))
            if recovery:
                a=current['active'];require(type(a) is dict and a.get('id')==self.id,'WRONG_RECOVERY_TRANSACTION')
                self.binding=a
                require(set(a)=={'id','path','baseline_sha256','release','manifest_sha256','target','tooling','pre_transaction'} and
                    a['path']==self.d.TX and a['baseline_sha256']==self.baseline_sha and a['release']==manifest['release'] and
                    a['manifest_sha256']==self.policy['payload_manifest_sha256'] and a['target']==TARGET and
                    type(a['tooling']) is dict and set(a['tooling'])=={'commit','tree'} and
                    all(re.fullmatch('[0-9a-f]{40}',x) for x in a['tooling'].values()) and
                    set(a['pre_transaction'])==set(self.d.ORDER),'ATTEMPT_BINDING_INVALID')
            else:
                require(current['active'] is None,'ACTIVE_OR_UNCERTAIN_TRANSACTION')
                require(not base.transaction_present(),'TRANSACTION_ID_ALREADY_USED')
            self.control_snapshot=base.snapshot(CONTROL,0o600)
            self.d.PRIOR={p:(v['sha256'],v['mode']) for p,v in self.baseline['artifacts'].items()}
        self.original=(base.read(w.BACKUP) if recovery and base.transaction_present() and base.snapshot(w.BACKUP,0o600)['exists'] else ops.scheduler())
        require(sha(self.original)==self.policy['original_scheduler_sha256'],'WINDOW_ORIGINAL_SCHEDULER_MISMATCH')
        inventory={line:'EXCLUDE' if line in self.d.CRON else 'PRESERVE' for line in self.original.decode('utf8').splitlines() if line.strip() and not line.lstrip().startswith('#')}
        require(len(inventory)==self.policy['scheduler_entry_count'],'WINDOW_SCHEDULER_INVENTORY_CHANGED')
        self.provider=w.WindowConsumers(ops,self.original,list(self.d.CRON),inventory)
        require(sha(self.provider.reduced)==self.policy['reduced_scheduler_sha256'],'WINDOW_REDUCED_SCHEDULER_MISMATCH')
        self.fs=AttemptFS(self)
        c=continuation_controller(w)(self.fs,source,self.provider)
        self.provider.controller=c
        self.co=w.MaintenanceCoordinator(self.provider,self.fresh_source)
        self.recorder=adapter()._Recorder(ops).install(w,self.co)
        original_context=self.co.context
        def context(action):
            value=original_context(action)
            value.update(baseline_sha256=self.baseline_sha,transaction_id=self.id,tooling_identity=self.tooling)
            if not establishment:
                if self.binding is not None:self.fs.guard()
                else:
                    control=read_control(w,base,manifest)
                    require(control['active'] is None and sha(self.d.canonical(control['baseline']))==self.baseline_sha,'CURRENT_BASELINE_DRIFT')
            return value
        self.co.context=context
        self.initial=None if recovery else self.runtime(self.expected_initial())
        self.incomplete_reservation=False
        if recovery and base.transaction_present():
            meta=self.d.TX+'/attempt.json'
            if base.snapshot(meta,0o600)['exists'] and base.read(meta)==self.d.canonical(self.binding):
                self.fs.guard()
            else:
                require(not base.snapshot(self.d.TX+'/journal.json',0o600)['exists'] and
                    base.entries(self.d.TX)<= {'attempt.json'},'RESERVATION_EVIDENCE_CONFLICT')
                self.incomplete_reservation=True

    def fresh_source(self):
        fresh=self.source_reader();self.d.check_sources(fresh)
        require(fresh==self.source,'SOURCE_IDENTITY_MISMATCH')
        return fresh
    def expected_initial(self):
        if self.baseline:return {p:v['sha256'] for p,v in self.baseline['artifacts'].items()}
        return {x['path']:x['prior_sha256'] for x in self.manifest['artifacts']}
    def runtime(self,expected):
        result={}
        for path in self.d.ORDER:
            snap=self.base.snapshot(path,self.d.MODES[path])
            require(snap['exists'] and snap['sha256']==expected[path],'CURRENT_RUNTIME_BASELINE_MISMATCH')
            result[path]=snap
        return result
    def control_write(self,value,before,*,recovery=False):
        raw=self.d.canonical(value)
        if recovery:
            temporary='backups/.pe73-delivery-pe73-current-baseline.json'
            snap=self.base.snapshot(temporary,0o600)
            if snap['exists']:
                require(self.base.read(temporary)==raw,'CONTROL_TEMPORARY_NOT_ESTABLISHED')
                self.base.archive(temporary,self.d.TX+'/archived-'+uuid.uuid4().hex,snapshot=snap,mode=0o600)
        if before['exists']:self.base.publish(CONTROL,raw,before,0o600)
        else:self.base.write_new(CONTROL,raw)
        require(self.base.read(CONTROL)==raw,'CONTROL_WRITE_NOT_VERIFIED')
        self.control_snapshot=self.base.snapshot(CONTROL,0o600)
    def approved_baseline(self,release,reference,recovery):
        return {'id':uuid.uuid4().hex,'status':'APPROVED_VERIFIED','target':dict(TARGET),
            'payload_release':release,'authorized_release':self.manifest['release'],'contract_sha256':CONTRACT_SHA,
            'artifacts':{x['path']:{'sha256':x['prior_sha256'] if release==self.manifest['prior_release'] else x['sha256'],
                'mode':self.d.MODES[x['path']],'uid':1000,'gid':1000,'type':'REGULAR'} for x in self.manifest['artifacts']},
            'compatibility':{'scope':'PI3_RUNTIME_ARTIFACTS_ONLY','activation_authorized':False,
                'scheduler_sha256':self.policy['original_scheduler_sha256']},
            'approval':{'reference':reference,'kind':'EXPLICIT_OWNER_OPERATION'},'recovery_reference':recovery}
    def establish(self):
        require(self.establishment,'BASELINE_ESTABLISHMENT_ENTRY_REQUIRED')
        def transition(reference):
            with self.base.mutex():
                require(not self.base.snapshot(CONTROL,0o600)['exists'],'BASELINE_ALREADY_ESTABLISHED')
                require(self.runtime(self.expected_initial())==self.initial and self.ops.scheduler()==self.original,'BASELINE_ESTABLISHMENT_DRIFT')
                baseline=self.approved_baseline(self.manifest['prior_release'],reference,
                    {'kind':'OPERATOR_SUPPLIED_RESTORATION','reference':'PASS_CONTROLLED_RESTORATION_AND_19_CHECKS'})
                self.control_write({'version':1,'baseline':baseline,'active':None},self.base.snapshot(CONTROL,0o600))
                return baseline
        return self.authorized('BASELINE_ESTABLISHMENT',transition,preparation=True)
    def claim(self):
        self.ops.live_gate();require(not self.establishment and not self.recovery,'NEW_ATTEMPT_ENTRY_REQUIRED')
        current=read_control(self.w,self.base,self.manifest)
        require(current['active'] is None and sha(self.d.canonical(current['baseline']))==self.baseline_sha,'ACTIVE_OR_UNCERTAIN_TRANSACTION')
        require(self.base.snapshot(CONTROL,0o600)==self.control_snapshot and not self.base.transaction_present(),'TRANSACTION_ID_ALREADY_USED')
        require(self.runtime(self.expected_initial())==self.initial,'TRANSACTION_LOCAL_RUNTIME_DRIFT')
        self.binding={'id':self.id,'path':self.d.TX,'baseline_sha256':self.baseline_sha,
            'release':self.manifest['release'],'manifest_sha256':self.policy['payload_manifest_sha256'],
            'target':dict(TARGET),'tooling':self.tooling,'pre_transaction':self.initial}
        current['active']=self.binding;self.control_write(current,self.control_snapshot)
    def authorized(self,action,call,preparation=False):
        # Direct invocation requires separate whole-process owner authorization.
        # No persisted receipt or synthetic observation is permission input.
        self.fresh_source();require(getattr(self.ops,'_admission',None) is None,'NATIVE_OPERATION_ALREADY_ACTIVE')
        def observed():
            return {'action':action,'transaction':self.id,'tooling':self.tooling,
                'control':self.base.snapshot(CONTROL,0o600),
                'runtime':{p:self.base.snapshot(p,self.d.MODES[p]) for p in self.d.ORDER},
                'scheduler_sha256':sha(self.ops.scheduler()),'boot_id':self.ops.boot_id}
        before=observed()
        reference='CURRENT_'+uuid.uuid4().hex
        a={'action':action,'reference':reference,'context_sha256':sha(self.d.canonical(before)),
            'operator':'UID1000_jazofv1','expires_at':self.ops.now()+300,
            'exclusive_responsibility':True,'risks_acknowledged':list(self.w.RISKS)}
        self.ops._admission=self.w._NativeAdmission(self.ops,self.co,action,a)
        try:
            self.ops.live_gate();require(observed()==before,'NATIVE_AUTHORIZATION_CONTEXT_DRIFT')
            self.fresh_source();self.recorder.action=action
            if not preparation:self.provider._processes()
            return call(reference)
        finally:self.ops._admission=None
    def actions(self,actions):
        # Reuse coordinator.execute and its original fresh operation grants.
        for action in actions:
            self.recorder.action=action
            context=self.co.context(action)
            a={'action':action,'reference':'CURRENT_'+uuid.uuid4().hex,
                'context_sha256':sha(self.d.canonical(context)),'operator':'UID1000_jazofv1',
                'expires_at':self.ops.now()+300,'exclusive_responsibility':True,'risks_acknowledged':list(self.w.RISKS)}
            require(getattr(self.ops,'_admission',None) is None,'NATIVE_OPERATION_ALREADY_ACTIVE')
            self.ops._admission=self.w._NativeAdmission(self.ops,self.co,action,a)
            try:self.co.execute(action,a)
            finally:self.ops._admission=None
        return self.finalize()
    def deploy(self):
        require(not self.establishment and not self.recovery,'NEW_ATTEMPT_ENTRY_REQUIRED')
        return self.actions(self.w.DEPLOYMENT_SEQUENCE)
    def buffers(self):
        self.fs.guard()
        v=self.co.controller._journal()
        for i,path in enumerate(self.d.ORDER):
            require(self.base.read(self.d.TX+'/stage-'+str(i))==self.source[path],'STAGING_DRIFT')
            require(sha(self.base.read(self.d.TX+'/backup-'+str(i)))==v['baseline'][path]['sha256'],'BACKUP_DRIFT')
        return v
    def reconcile(self):
        """Explicit recovery only: bind current expected effects, never infer writer identity."""
        def resolve(reference):
            with self.base.mutex():
                v=self.buffers();original=self.d.canonical(v)
                phase=v.get('window',{}).get('phase')
                require(phase not in {None,'PRESERVATION_UNCERTAIN','EXCLUSION_UNCERTAIN','RESTORE_UNCERTAIN'},'SCHEDULER_OR_PREPARATION_RECONCILIATION_REQUIRED')
                expected=self.original if phase in {'PRESERVED','SCHEDULER_RESTORED','RELEASED'} else self.provider.reduced
                require(self.ops.scheduler()==expected,'WINDOW_SCHEDULER_DRIFT')
                pending=v['pending']
                if pending is not None:
                    require(v['state'] in {'COMMITTING','ROLLING_BACK'},'PENDING_STATE_NOT_RECOVERABLE')
                    snap=self.base.snapshot(pending,self.d.MODES[pending])
                    previous=v['installed'].get(pending,v['baseline'][pending])
                    wanted=v['baseline'][pending]['sha256'] if v['state']=='ROLLING_BACK' else next(x['sha256'] for x in self.manifest['artifacts'] if x['path']==pending)
                    require(snap==previous or snap['sha256']==wanted,'PENDING_RUNTIME_NOT_ESTABLISHED')
                    evidence={'kind':'EXPLICIT_PENDING_RECONCILIATION','authorization':reference,
                        'journal_sha256':sha(original),'path':pending,'observed':snap,
                        'writer_attribution':'NOT_CLAIMED'}
                    self.fs.write_new(self.d.TX+'/recovery-'+uuid.uuid4().hex+'.json',self.d.canonical(evidence))
                    temporary=str(Path(pending).parent/('.pe73-delivery-'+Path(pending).name)).replace('\\','/')
                    if self.base.snapshot(temporary,self.d.MODES[pending])['exists']:
                        require(self.base.read(temporary,self.d.MODES[pending])==self.source[pending] or
                            sha(self.base.read(temporary,self.d.MODES[pending]))==v['baseline'][pending]['sha256'],'RECOVERY_TEMPORARY_DRIFT')
                        self.base.archive(temporary,self.d.TX+'/archived-'+uuid.uuid4().hex,snapshot=self.base.snapshot(temporary,self.d.MODES[pending]),mode=self.d.MODES[pending])
                    if snap!=previous or v['state']=='ROLLING_BACK' and snap['sha256']==wanted:
                        v['restored' if v['state']=='ROLLING_BACK' else 'installed'][pending]=snap
                    v['pending']=None
                nxt=self.d.TX+'/journal-next'
                if self.base.snapshot(nxt,0o600)['exists']:
                    candidate=self.d.parsed(self.base.read(nxt));self.co.controller._validate(candidate)
                    self.base.archive(nxt,self.d.TX+'/archived-'+uuid.uuid4().hex,snapshot=self.base.snapshot(nxt,0o600),mode=0o600)
                # This is a new authorized reconciliation write, not adoption of journal-next.
                if self.d.canonical(v)!=original:self.co.controller._save(v,'RECOVERY_RECONCILED')
                require(self.co.controller.inspect()['live_state_established'],'RECOVERY_RUNTIME_UNCERTAIN')
        return self.authorized('ROLLBACK',resolve)
    def recover(self,mode='ROLLBACK'):
        require(self.recovery and mode in {'ROLLBACK','RESUME_PREPARED','RELEASE'},'RECOVERY_ENTRY_REQUIRED')
        self.reconcile();v=self.buffers();phase=v['window']['phase'] if v.get('window') else None
        require(phase not in {None,'PRESERVATION_UNCERTAIN','EXCLUSION_UNCERTAIN','RESTORE_UNCERTAIN'},'SCHEDULER_OR_PREPARATION_RECONCILIATION_REQUIRED')
        require(not (v['state']=='COMMITTED' and phase in {'RELEASE_AUTHORIZED','SCHEDULER_RESTORED','RELEASED'}) or mode=='RELEASE','EXPLICIT_RELEASE_RECOVERY_REQUIRED')
        if v['state']=='PREPARED':
            require(mode=='RESUME_PREPARED','PREPARED_RESUME_REQUIRES_EXPLICIT_AUTHORIZATION')
            require(phase in {'PRESERVED','EXCLUDED','DRAINED','ESTABLISHED'},'PREPARED_PHASE_UNCERTAIN')
            todo=['ATTACH']
            if phase=='PRESERVED':todo+=['EXCLUDE']
            todo+=['DRAIN']
            if phase in {'PRESERVED','EXCLUDED','DRAINED'}:todo+=['ESTABLISH']
            todo+=['COMMIT','AUTHORIZE_RELEASE','RESTORE_SCHEDULER','RELEASE']
        elif phase=='RELEASED':return self.finalize()
        elif phase=='SCHEDULER_RESTORED':todo=['ATTACH','DRAIN','RELEASE']
        elif phase=='RELEASE_AUTHORIZED':todo=['ATTACH','DRAIN','RESTORE_SCHEDULER','RELEASE']
        else:
            todo=['ATTACH','DRAIN']
            if v['state'] in {'COMMITTING','ROLLING_BACK','COMMITTED'} and mode=='ROLLBACK':todo+=['ROLLBACK']
            else:require(v['state']=='ROLLED_BACK' or v['state']=='COMMITTED' and mode=='RELEASE','RECOVERY_MODE_OR_PHASE')
            todo+=['AUTHORIZE_RELEASE','RESTORE_SCHEDULER','RELEASE']
        return self.actions(tuple(todo))
    def reconcile_scheduler(self):
        """Separately authorized recovery; never called automatically after failure."""
        require(self.recovery,'RECOVERY_ENTRY_REQUIRED')
        def reconcile(reference):
            with self.base.mutex():
                v=self.buffers();w=v.get('window')
                require(w is not None and w['phase'] in {'EXCLUSION_UNCERTAIN','RESTORE_UNCERTAIN'},'SCHEDULER_RECONCILIATION_PHASE')
                raw=self.ops.scheduler()
                require(raw in (self.original,self.provider.reduced),'WINDOW_SCHEDULER_DRIFT')
                if w['phase']=='EXCLUSION_UNCERTAIN':
                    require(raw==self.provider.reduced,'ORIGINAL_SCHEDULER_REQUIRES_PRIVATE_ABORT')
                    w['phase']='EXCLUDED';self.co.controller._save(v,'RECOVERY_EXCLUSION_READBACK')
                else:
                    require(v['state'] in {'COMMITTED','ROLLED_BACK'} and v['pending'] is None and
                        self.co.controller.inspect()['live_state_established'],'RESTORATION_NOT_VERIFIED')
                    if raw==self.provider.reduced:
                        intent=self.d.TX+'/recovery-'+uuid.uuid4().hex+'.json'
                        body=self.d.canonical({'kind':'EXPLICIT_SCHEDULER_RESTORATION','authorization':reference,
                            'journal_sha256':sha(self.d.canonical(v)),'before_sha256':sha(raw),
                            'after_sha256':sha(self.original)})
                        self.fs.write_new(intent,body)
                        old=self.ops.scheduler_gate
                        attempted=[False]
                        def gate():
                            self.ops.live_gate();self.fs.guard();self.provider._processes()
                            require(not attempted[0] and self.ops._admission.action=='RESTORE_SCHEDULER' and
                                self.base.read(intent)==body and self.co.controller._journal()==v and
                                self.ops.scheduler()==self.provider.reduced,'RECOVERY_SCHEDULER_INTENT_DRIFT')
                            attempted[0]=True
                        self.ops.scheduler_gate=gate
                        try:self.ops.install_scheduler(self.original,sha(self.provider.reduced))
                        finally:self.ops.scheduler_gate=old
                    require(self.ops.scheduler()==self.original,'SCHEDULER_INSTALL_UNCONFIRMED')
                    w['phase']='SCHEDULER_RESTORED';self.co.controller._save(v,'RECOVERY_RESTORATION_READBACK')
                return {'phase':w['phase'],'automatic_retry':False}
        return self.authorized('RESTORE_SCHEDULER',reconcile)

    def abort_preparation(self):
        """No runtime/scheduler effects; close only a provably unchanged private attempt."""
        require(self.recovery,'RECOVERY_ENTRY_REQUIRED')
        def abort(reference):
            with self.base.mutex():
                current=read_control(self.w,self.base,self.manifest)
                require(current['active']==self.binding and self.base.snapshot(CONTROL,0o600)==self.control_snapshot,'ACTIVE_TRANSACTION_OR_BASELINE_DRIFT')
                require(self.ops.scheduler()==self.original and
                    self.runtime(self.expected_initial())==self.binding['pre_transaction'],'ABORT_EFFECTS_NOT_EXCLUDED')
                if not self.base.transaction_present():self.base.mkdir_tx()
                if self.incomplete_reservation:
                    require(self.base.entries(self.d.TX)<= {'attempt.json'},'RESERVATION_EVIDENCE_CONFLICT')
                    meta=self.d.TX+'/attempt.json'
                    if self.base.snapshot(meta,0o600)['exists']:
                        self.base.archive(meta,self.d.TX+'/archived-'+uuid.uuid4().hex,snapshot=self.base.snapshot(meta,0o600),mode=0o600)
                if not self.base.snapshot(self.d.TX+'/attempt.json',0o600)['exists']:
                    self.base.write_new(self.d.TX+'/attempt.json',self.d.canonical(self.binding))
                journal=self.d.TX+'/journal.json'
                if self.base.snapshot(journal,0o600)['exists']:
                    v=self.co.controller._journal()
                    require(v['state'] in {'PREPARING','PREPARED'} and not v['installed'] and
                        not v['restored'] and v['pending'] is None and
                        (v.get('window') is None or v['window']['phase'] in {'PRESERVATION_UNCERTAIN','PRESERVED','EXCLUSION_UNCERTAIN'}), 'ABORT_EFFECTS_NOT_EXCLUDED')
                terminal={'kind':'ABORTED_BEFORE_RUNTIME','transaction':self.id,'authorization':reference}
                path=self.d.TX+'/terminal.json'
                if self.base.snapshot(path,0o600)['exists']:
                    old=self.d.parsed(self.base.read(path))
                    require(set(old)==set(terminal) and old['kind']=='ABORTED_BEFORE_RUNTIME' and
                        old['transaction']==self.id and self.d.AUTH.fullmatch(old['authorization']),'TERMINAL_EVIDENCE_CONFLICT')
                    terminal=old
                else:self.base.write_new(path,self.d.canonical(terminal))
                control=read_control(self.w,self.base,self.manifest);control['active']=None
                self.control_write(control,self.control_snapshot,recovery=True)
                return terminal
        return self.authorized('ABORT_PREPARATION',abort,preparation=True)
    def finalize(self):
        def finish(reference):
            with self.base.mutex():
                v=self.buffers()
                require(v['state'] in {'COMMITTED','ROLLED_BACK'} and v['pending'] is None and
                    v.get('window',{}).get('phase')=='RELEASED' and self.ops.scheduler()==self.original and
                    self.co.controller.inspect()['live_state_established'],'BASELINE_PROMOTION_REFUSED')
                release=self.manifest['release'] if v['state']=='COMMITTED' else self.baseline['payload_release']
                expected={x['path']:x['sha256'] if release==self.manifest['release'] else x['prior_sha256'] for x in self.manifest['artifacts']}
                self.runtime(expected)
                control=read_control(self.w,self.base,self.manifest)
                if v['state']=='COMMITTED':
                    control['baseline']=self.approved_baseline(release,reference,{'kind':'VERIFIED_TRANSACTION','reference':self.d.TX})
                control['active']=None
                receipt={'kind':'VERIFIED_TERMINAL','transaction':self.id,'state':v['state'],
                    'journal_sha256':sha(self.d.canonical(v)),'next_control_sha256':sha(self.d.canonical(control)),
                    'authorization':reference,'next_control':control}
                terminal=self.d.TX+'/terminal.json'
                if self.base.snapshot(terminal,0o600)['exists']:
                    old=self.d.parsed(self.base.read(terminal))
                    require(set(old)==set(receipt) and old['kind']=='VERIFIED_TERMINAL' and
                        self.d.AUTH.fullmatch(old['authorization']) and old['transaction']==self.id and old['state']==v['state'] and
                        old['journal_sha256']==sha(self.d.canonical(v)) and
                        sha(self.d.canonical(old['next_control']))==old['next_control_sha256'] and
                        old['next_control']['active'] is None,'TERMINAL_EVIDENCE_CONFLICT')
                    # Complete the exact already approved transition, never regenerate it.
                    candidate=old['next_control']
                    require(set(candidate)=={'version','baseline','active'} and candidate['version']==1,'TERMINAL_EVIDENCE_CONFLICT')
                    if v['state']=='ROLLED_BACK':require(candidate['baseline']==self.baseline,'TERMINAL_EVIDENCE_CONFLICT')
                    else:
                        expected=dict(control['baseline']);actual=dict(candidate['baseline'])
                        require(re.fullmatch('[0-9a-f]{32}',actual['id']) and
                            actual['approval']=={'reference':old['authorization'],'kind':'EXPLICIT_OWNER_OPERATION'},'TERMINAL_EVIDENCE_CONFLICT')
                        for key in ('id','approval'):actual.pop(key);expected.pop(key)
                        require(actual==expected,'TERMINAL_EVIDENCE_CONFLICT')
                    control=candidate;receipt=old
                else:self.base.write_new(terminal,self.d.canonical(receipt))
                self.control_write(control,self.control_snapshot,recovery=True)
                return receipt
        return self.authorized('FINALIZE_BASELINE',finish)


def native():
    """Source-only construction; no mutation or automatic baseline establishment."""
    a=adapter();w,m=a.load();ops=w.NativeOps();base=w.d.NativeFS()
    require(base.root==Path(TARGET['runtime_root']),'TARGET_IDENTITY')
    def git(*args):
        p=subprocess.run(['/usr/bin/git','--no-optional-locks','--no-replace-objects',*args],cwd=ROOT,
            stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=20,env={'PATH':'/usr/bin:/bin','HOME':'/home/jazofv1','LANG':'C.UTF-8'})
        require(p.returncode==0,'OPERATION_SOURCE_INVALID');return p.stdout.strip()
    require(ROOT==Path('/home/jazofv1/hioc-release-source') and ROOT.resolve()==ROOT and
        git('branch','--show-current')==b'main' and git('rev-parse','--show-toplevel').decode()==str(ROOT), 'OPERATION_SOURCE_ROOT')
    source=w.d.source_gate()
    tooling={'commit':git('rev-parse','HEAD').decode(),'tree':git('rev-parse','HEAD^{tree}').decode()}
    require(git('rev-parse','origin/main').decode()==tooling['commit'],'TOOLING_RELEASE_NOT_SYNCHRONIZED')
    def fresh():
        require(git('rev-parse','HEAD').decode()==tooling['commit'] and
            git('rev-parse','origin/main').decode()==tooling['commit'] and not git('status','--porcelain=v1','--untracked-files=all') and
            git('remote','get-url','origin')==b'https://github.com/jorgeazofeifa-creator/hioc.git','OPERATION_SOURCE_DRIFT')
        return source
    # Native archival uses the same proven descriptor and renameat2 primitives.
    def archive(src,dst,*,snapshot,mode):
        require(base.snapshot(src,mode)==snapshot and not base.snapshot(dst,mode)['exists'],'RECOVERY_ARCHIVE_DRIFT')
        with base.directory(str(Path(src).parent)) as sf,base.directory(str(Path(dst).parent)) as df:
            require(os.fstat(sf).st_dev==os.fstat(df).st_dev,'RECOVERY_ARCHIVE_CROSS_DEVICE')
            rename=ctypes.CDLL(None,use_errno=True).renameat2
            rename.argtypes=[ctypes.c_int,ctypes.c_char_p,ctypes.c_int,ctypes.c_char_p,ctypes.c_uint];rename.restype=ctypes.c_int
            require(base.snapshot(src,mode)==snapshot and rename(sf,os.fsencode(Path(src).name),df,os.fsencode(Path(dst).name),1)==0,'RECOVERY_ARCHIVE_FAILED')
            os.fsync(sf);os.fsync(df)
        after=base.snapshot(dst,mode)
        require(after['sha256']==snapshot['sha256'] and all(after['identity'][k]==snapshot['identity'][k] for k in
            ('st_dev','st_ino','st_uid','st_gid','mode','st_nlink','st_size')) and
            not base.snapshot(src,mode)['exists'],'RECOVERY_ARCHIVE_NOT_VERIFIED')
    base.archive=archive
    def entries(path):
        with base.directory(path) as fd:
            base.security(os.fstat(fd),True,0o700,fd=fd)
            names=set(os.listdir(fd));require(len(names)<=256,'TRANSACTION_ENTRY_LIMIT');return names
    base.entries=entries
    return w,m,base,ops,source,fresh,tooling


def native_operation(*,transaction_id=None,establishment=False,recovery=False):
    w,m,base,ops,source,fresh,tooling=native()
    return Operations(w,m,base,ops,source,fresh,transaction_id=transaction_id,
        establishment=establishment,recovery=recovery,tooling=tooling)


def native_coordinator():
    w,m,base,ops,source,fresh,tooling=native()
    operation=Operations(w,m,base,ops,source,fresh,tooling=tooling)
    # Keep the operation alive on the coordinator; no mutation in construction.
    operation.co.verified_baseline_operation=operation
    def sequence(coordinator):
        require(coordinator is operation.co,'COORDINATOR_IDENTITY')
        return operation.deploy()
    w.run_deployment_sequence=sequence
    return w,m,operation.co,operation.co.context('PREPARE')

if __name__=='__main__':
    try:
        w,m,base,ops,source,fresh,tooling=native()
        value=read_control(w,base,m)
        print(json.dumps({'RESULT':'PASS_READ_ONLY_CURRENT_BASELINE','baseline_id':value['baseline']['id'],
            'active_transaction':value['active']['id'] if value['active'] else None,
            'deployment_authorized':False,'production_mutated':False,'STOP_REQUIRED':True},sort_keys=True))
    except Exception as error:
        code=str(error) if type(error) is ValueError and re.fullmatch('[A-Z][A-Z0-9_]{0,127}',str(error)) else 'CURRENT_BASELINE_INSPECTION_FAILED'
        print(json.dumps({'RESULT':'FAIL_STOP','failure_code':code,'process_guard':getattr(error,'process_guard',None),
            'production_mutated':False,'STOP_REQUIRED':True},sort_keys=True))
        raise SystemExit(1)
