"""Source-only future operator wrapper. Import performs no production I/O.
FOR REVIEW ONLY - DO NOT RUN WITHOUT SEPARATE AUTHORIZATION.
No source synchronization, deployment, credential reader or automatic retry.
"""
import ast
import errno
import hashlib
import importlib.util
import ipaddress
import json
import os
from pathlib import Path
import re
import selectors
import socket
import stat
import subprocess
import sys
import tempfile
import time

SOURCE = Path('/home/jazofv1/hioc-release-source')
HOME = Path('/home/jazofv1/hioc')
BASE = 'abae01b6eb60aecb12396d8078dee719d75801b7'
PREPARATION_PARENT = '560a7810ed1e57c861b38a3fe9d75397cba59eea'
CORRECTION = 'governance/pe4/pe4-ha-association-bounded-manual-validation-correction.json'
DEPLOYED = '4912f20d8b2ff78dcdaf8b3e0f52e57d5de5e3a2'
RECORD = 'governance/pe4/pe4-ha-association-bounded-manual-validation-preparation.json'
CLOSURE = 'governance/pe4/pe4-ha-association-adapter-deployment-closure.json'
CLOSURE_SHA = 'ff99c3d19d19c581279d5ff09e47bbf7cfa1f260d472e047fbc487952df6ac71'
ENV = {'PATH':'/usr/sbin:/usr/bin:/bin','HOME':'/home/jazofv1','LANG':'C.UTF-8','LC_ALL':'C.UTF-8'}
ADAPTER_COMMAND = ['/home/jazofv1/hioc/runtime/pe4/active/bin/python','-I','-B','/home/jazofv1/hioc/pi4/bin/hioc-home-assistant-association.py']
FIELDS = ('RESULT','ERROR_CODE','FAILURE_STAGE','COMPATIBILITY_STATUS','OBSERVED_HA_VERSION','ASSOCIATED_COUNT','REVIEW_ONLY_COUNT','REJECTED_COUNT','UNMATCHED_COUNT','HISTORICAL_BINDING_COUNT','STATE_PUBLISHED','LAST_KNOWN_GOOD_PRESERVED')
STAGES = ('TARGET_VALIDATION','RUNTIME_VALIDATION','LOCK_ACQUISITION','CONTRACT_VALIDATION','PRIOR_STATE_VALIDATION','CANONICAL_INVENTORY_INPUT','CREDENTIAL_ACQUISITION','HA_CONNECTION','HA_AUTHENTICATION','REQUIRED_REGISTRY_COMMAND','REGISTRY_SCHEMA','COMPATIBILITY','ASSOCIATION_EVALUATION','BINDING_HISTORY_CAPACITY','CANDIDATE_STATE_VALIDATION','STATE_PUBLICATION','UNEXPECTED_INTERNAL')
WARNINGS = ('TRANSACTION_CLEANUP_FAILED','COMPATIBILITY_REPORTING_FAILED')
GOOD = ('COMPATIBLE','COMPATIBLE_UPDATED','COMPATIBILITY_DEGRADED')
STATUS = GOOD + ('COMPATIBILITY_UNKNOWN','INCOMPATIBLE','TRUST_ANCHOR_CHANGED','DEPENDENCY_UNAVAILABLE','UNKNOWN')
EXTRA = ('TARGET','SOURCE_GOVERNANCE_COMMIT','DEPLOYED_SOURCE_COMMIT','DEPLOYMENT_CLOSURE','ADAPTER_EXECUTION_COUNT','ADAPTER_RETURN_CODE','PRE_RUN_PRIVATE_STATE','POST_RUN_PRIVATE_STATE','STATE_SCHEMA_VALIDATION','TRANSACTION_NAMESPACE_CLEAN','CONFIG_UNCHANGED','CANONICAL_INVENTORY_UNCHANGED','PLATFORM_STATUS_UNCHANGED','PLATFORM_CRON_UNCHANGED','ASSOCIATION_SCHEDULER_PRESENT','COMPATIBILITY_STATE_VALIDATION','CREDENTIAL_EXPOSED','RAW_HA_DATA_PERSISTED','PRIVATE_ASSOCIATION_CONTENT_EXPOSED','PROTECTED_PRODUCTION_SURFACES_UNCHANGED','OUTPUT_VALIDATION','WRAPPER_STATUS','OVERALL_VALIDATION','MANUAL_REVIEW_REQUIRED')
LIMIT = 16 * 1024 * 1024
class Stop(Exception): pass

def require(condition):
    if not condition: raise Stop()

def canonical(value): return (json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False)+'\n').encode()
def sha(raw): return hashlib.sha256(raw).hexdigest()
def strict(raw):
    require(type(raw) is bytes and len(raw)<=LIMIT)
    def pairs(items):
        result={}
        for k,v in items:
            require(k not in result);result[k]=v
        return result
    def bad(_): raise Stop()
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=bad)

def schema_validate(v,s):
    types={'object':dict,'array':list,'string':str,'integer':int,'boolean':bool,'null':type(None)}
    if 'type' in s:
        kinds=s['type'] if isinstance(s['type'],list) else [s['type']]
        require(any(type(v) is types[t] for t in kinds))
    if 'const' in s: require(type(v) is type(s['const']) and v==s['const'])
    if 'enum' in s: require(any(type(v) is type(x) and v==x for x in s['enum']))
    if isinstance(v,dict):
        props=s.get('properties',{});require(set(s.get('required',[]))<=set(v))
        if s.get('additionalProperties') is False:require(set(v)<=set(props))
        for k,x in v.items():
            if 'propertyNames' in s:schema_validate(k,s['propertyNames'])
            if k in props:schema_validate(x,props[k])
            elif isinstance(s.get('additionalProperties'),dict):schema_validate(x,s['additionalProperties'])
    elif isinstance(v,list):
        require(s.get('minItems',0)<=len(v)<=s.get('maxItems',LIMIT))
        if 'prefixItems' in s:
            require(s['items'] is False and len(v)==len(s['prefixItems']))
            for x,n in zip(v,s['prefixItems']):schema_validate(x,n)
        elif 'items' in s:
            for x in v:schema_validate(x,s['items'])
    elif isinstance(v,str):
        require(s.get('minLength',0)<=len(v)<=s.get('maxLength',LIMIT))
        if 'pattern' in s: require(re.search(s['pattern'],v) is not None)
    elif type(v) is int:require(s.get('minimum',-LIMIT)<=v<=s.get('maximum',LIMIT))

def command(args,cwd=None):
    p=subprocess.run(args,cwd=cwd,env=ENV,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,timeout=15)
    require(p.returncode==0 and len(p.stdout)<=LIMIT);return p.stdout

def git(*args):return command(['/usr/bin/git',*args],SOURCE).decode('ascii').strip()
def load_module(path,name):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def source_binding(commit):
    require(re.fullmatch('[0-9a-f]{40}',commit) is not None)
    require(git('branch','--show-current')=='main' and git('rev-parse','HEAD')==git('rev-parse','origin/main')==commit)
    require(git('rev-parse','HEAD^')==BASE and git('rev-list','--left-right','--count','HEAD...origin/main')=='0\t0')
    require(git('show','-s','--format=%s','HEAD')=='PE-4: correct bounded validation production scope')
    require(git('status','--porcelain','--untracked-files=all')=='')
    for n in ('MERGE_HEAD','CHERRY_PICK_HEAD','REVERT_HEAD','BISECT_LOG','BISECT_START','sequencer','rebase-apply','rebase-merge'):
        p=Path(git('rev-parse','--git-path',n));require(not (p if p.is_absolute() else SOURCE/p).exists())
    # The prior source-sync review proves remote equality; this action performs no fetch/pull.
    for p in (RECORD,RECORD.replace('.json','.schema.json'),CORRECTION,CORRECTION.replace('.json','.schema.json'),CLOSURE,CLOSURE.replace('.json','.schema.json'),'tools/hioc-pe4-ha-association-manual-validate.py','tools/hioc-pe4-ha-association-manual-reconcile.py'):
        require(command(['/usr/bin/git','show',commit+':'+p],SOURCE)==(SOURCE/p).read_bytes())
    raw=(SOURCE/CLOSURE).read_bytes();require(sha(raw)==CLOSURE_SHA)
    closure=strict(raw);require(closure['status']=='PASS_CLOSED' and closure['deployment_transaction']=='COMMITTED' and closure['deployed_source_commit']==DEPLOYED)
    record=strict((SOURCE/RECORD).read_bytes());schema_validate(record,strict((SOURCE/RECORD.replace('.json','.schema.json')).read_bytes()))
    require(record['starting_commit']==PREPARATION_PARENT and record['deployed_source_commit']==DEPLOYED)
    # Preparation binds historical wrapper bytes, never the corrected wrapper.
    for key in ('source_only_wrapper','compatibility_status_schema'):
        item=record[key];require(sha(command(['/usr/bin/git','show',BASE+':'+item['path']],SOURCE))==item['sha256'])
    correction=strict((SOURCE/CORRECTION).read_bytes());schema_validate(correction,strict((SOURCE/CORRECTION.replace('.json','.schema.json')).read_bytes()))
    require(correction['starting_commit']==BASE and correction['deployed_source_commit']==DEPLOYED)
    for key in ('corrected_wrapper','reconciliation_tool'):
        item=correction[key];require(sha((SOURCE/item['path']).read_bytes())==item['sha256'])
    for item in closure['sources'].values():
        raw=(SOURCE/item['path']).read_bytes();require(sha(raw)==item['sha256'])
    return closure,correction

def validate_cron(raw):
    require(type(raw) is bytes and len(raw)<=65536)
    text=raw.decode('utf8');lines=[line.strip() for line in text.splitlines() if line.strip() and not line.lstrip().startswith('#')]
    require(not re.search(r'(?i)(?:home.assistant|ha.association|associations)',text))
    expected='17 3 * * * flock -n /tmp/hioc-platform-status.lock /home/jazofv1/hioc/pi4/bin/hioc-platform-status.py'
    require([l for l in lines if 'hioc-platform-status' in l]==[expected])
    return raw

def scheduler():
    raw=validate_cron(command(['/usr/bin/crontab','-l']))
    # Check additional scheduler surfaces; never inspect credential storage.
    for p in (Path('/etc/crontab'),Path('/etc/cron.d'),Path('/etc/systemd/system'),Path('/home/jazofv1/.config/systemd/user')):
        if not p.exists():continue
        candidates=[p] if p.is_file() else sorted(p.rglob('*'))
        require(len(candidates)<=4096)
        for f in candidates:
            if f.is_symlink():
                require(not re.search(r'(?i)(home.assistant|ha.association)',str(f)+os.readlink(f)));continue
            if not f.is_file():continue
            require(f.stat().st_size<=65536)
            require(not re.search(rb'(?i)(hioc.home.assistant|hioc.ha.association|inventory/associations)',f.read_bytes()))
    return raw

def runtime_probe(d):
    site=d.ENVIRONMENT/'lib/python3.11/site-packages'
    require((HOME/'runtime/pe4/active').is_symlink() and (HOME/'runtime/pe4/active').resolve()==d.ENVIRONMENT)
    ns=d.runtime_policy_namespace();o=ns['runtime_customization_observation'](site)
    o['site_loaded']=True;o['site_module']=ns['CUSTOMIZATION_POLICY']['site_module'];ns['validate_runtime_customization'](o,site)
    # Reuse the immutable, corrected probe body only; NEVER call prerequisites(), which reads a credential.
    tree=ast.parse((SOURCE/'tools/hioc-pe4-ha-association-deploy.py').read_bytes())
    fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='prerequisites')
    assignment=next(n for n in fn.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='probe' for t in n.targets))
    ns={'runtime_validation_source':d.runtime_validation_source}
    exec(compile(ast.Module(body=[assignment],type_ignores=[]),'immutable runtime probe','exec'),ns)
    d.runtime_identity(strict(command([ADAPTER_COMMAND[0],'-I','-B','-c',ns['probe']])))

def deployment_integrity(d,fs,c):
    manifest={'dependencies':c['dependencies'],'deploy':c['deployed_targets']};d.check_manifest(manifest)
    require(d.transaction_state(fs,manifest,DEPLOYED)=='COMMITTED')
    intent,prior,candidate=d.reviewed_intent(fs,manifest,DEPLOYED,fs.read(d.TX+'/intent.json',0o600))
    require(len(intent['targets'])==len(intent['created_files'])==9 and intent['endpoint_added'] is True)
    for item in c['dependencies']:require(sha(fs.read(item['path']))==item['sha256'])
    for item in c['deployed_targets']:require(sha(fs.read(item['path'],int(item['mode'],8)))==item['sha256'])
    require(fs.read(d.CONFIG)==candidate and d.endpoint_config(candidate)==candidate)
    require(fs.check_directory(d.ASSOCIATIONS,0o700) and fs.read(d.LOCK,0o600) is not None)
    require(sha(fs.read('pi4/bin/hioc-platform-status.py'))==c['platform_status_sha256'])

def namespace(fs,d,first=False):
    require(fs.check_directory(d.ASSOCIATIONS,0o700) and fs.read(d.LOCK,0o600) is not None)
    names=fs.names(d.ASSOCIATIONS)
    require(all(n in ('.home_assistant.lock','home_assistant.json') or re.fullmatch(r'\.home_assistant\.(txn|done)-[0-9a-f]{32}',n) for n in names))
    tx=any(n.startswith(('.home_assistant.txn-','.home_assistant.done-')) for n in names)
    present='home_assistant.json' in names
    if first:require(not present and not tx)
    return present,not tx

PROTECTED_FILE_GROUPS = ('DEPLOYED_ADAPTER_ENTRYPOINT_COMPATIBILITY','FIVE_DEPENDENCIES','SIX_RUNTIME_GOVERNANCE','EXACT_CONFIG','EXECUTION_TIME_CANONICAL_INVENTORY','PLATFORM_STATUS','COMMITTED_JOURNAL_AUTHORITY')
JOURNAL_FILES = ('intent.json','committed.json','config-prior','config-candidate')

def protected_snapshot(fs,closure,deployment,include_inventory=True):
    """Explicit adapter-specific surfaces only; never walk the production tree.

    Private comparison values stay in RAM. Inventory comparison applies only to a
    future authorized bounded execution; reconciliation never recreates that history.
    """
    deployment_integrity(deployment,fs,closure)
    runtime_probe(deployment)
    scheduler_raw=scheduler()
    paths={item['path']:int(item['mode'],8) for item in closure['deployed_targets']}
    paths.update({item['path']:None for item in closure['dependencies']})
    paths.update({deployment.CONFIG:None,'pi4/bin/hioc-platform-status.py':None,deployment.LOCK:0o600})
    paths.update({deployment.TX+'/'+name:0o600 for name in JOURNAL_FILES})
    if include_inventory:paths['state/inventory/inventory.json']=None
    require(len(closure['dependencies'])==5 and len(closure['deployed_targets'])==9)
    result={}
    for path,mode in sorted(paths.items()):
        raw=fs.read(path,mode);require(raw is not None)
        info=fs.info(path);require(stat.S_ISREG(info.st_mode) and info.st_nlink==1)
        result[path]=(info.st_mode,info.st_uid,info.st_gid,info.st_nlink,sha(raw))
    require(fs.check_directory(deployment.ASSOCIATIONS,0o700))
    info=fs.info(deployment.ASSOCIATIONS)
    result['ASSOCIATION_DIRECTORY_SECURITY']=(info.st_mode,info.st_uid,info.st_gid)
    active=HOME/'runtime/pe4/active';info=active.lstat()
    require(stat.S_ISLNK(info.st_mode) and active.resolve()==deployment.ENVIRONMENT)
    result['RUNTIME_ACTIVE_IDENTITY']=(info.st_uid,info.st_gid,os.readlink(active),str(active.resolve()))
    result['PLATFORM_CRON_AND_SCHEDULER']=sha(scheduler_raw)
    result['RUNTIME_IDENTITY_SECURITY']='EXACT_REVIEWED_POLICY_PASS'
    return result

def parse_result(raw,compat):
    require(type(raw) is bytes and len(raw)<=4096 and raw.endswith(b'\n'))
    text=raw.decode('ascii');lines=text.splitlines();require(len(lines)==len(FIELDS))
    result={}
    for key,line in zip(FIELDS,lines):
        require(line.startswith(key+'='));result[key]=line[len(key)+1:]
    require(result['RESULT'] in ('PASS','PASS_WITH_WARNING','FAIL'))
    stage=result['FAILURE_STAGE'];require(stage in STAGES+('NONE',))
    require(result['ERROR_CODE'] in ('NONE',*WARNINGS,'BINDING_HISTORY_CAPACITY_EXCEEDED',*(s+'_FAILED' for s in STAGES)))
    require(result['COMPATIBILITY_STATUS'] in STATUS)
    require(result['OBSERVED_HA_VERSION']=='UNKNOWN' or compat.safe_version(result['OBSERVED_HA_VERSION'])==result['OBSERVED_HA_VERSION'])
    for k in FIELDS[5:10]:
        v=result[k];require(v=='UNKNOWN' or re.fullmatch(r'0|[1-9][0-9]{0,4}',v) and int(v)<=(4096 if k=='HISTORICAL_BINDING_COUNT' else 65536))
    require(result['STATE_PUBLISHED'] in ('TRUE','FALSE') and result['LAST_KNOWN_GOOD_PRESERVED'] in ('TRUE','FALSE','UNKNOWN'))
    return result

def invoke_once(on_started=lambda:None):
    # Drain only bounded stdout in RAM. Discard stderr; never save malformed/raw diagnostics.
    p=subprocess.Popen(ADAPTER_COMMAND,env=ENV,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
    on_started()
    raw=bytearray();deadline=time.monotonic()+195;sel=selectors.DefaultSelector();sel.register(p.stdout,selectors.EVENT_READ)
    try:
        while sel.get_map():
            remaining=deadline-time.monotonic()
            if remaining<=0:raise Stop()
            for key,_ in sel.select(min(remaining,1)):
                chunk=os.read(key.fileobj.fileno(),4097-len(raw))
                if not chunk:sel.unregister(key.fileobj)
                else:raw.extend(chunk);require(len(raw)<=4096)
        return p.wait(timeout=max(.1,deadline-time.monotonic())),bytes(raw)
    except BaseException:
        p.kill();p.wait(timeout=5);raise Stop() from None
    finally:sel.close();p.stdout.close()

def compatibility_validation(before,after,fields,compat,schema,registry):
    schema_validate(after,schema)
    require(len({x['dependency_id'] for x in after['dependencies']})==len(after['dependencies']))
    require(after['dependency_count']==len(after['dependencies'])==len(registry['dependencies']))
    old={x['dependency_id']:x for x in before['dependencies']};new={x['dependency_id']:x for x in after['dependencies']}
    require(set(new)=={x['dependency_id'] for x in registry['dependencies']})
    if after==before:
        require(fields['RESULT']=='FAIL' or fields['ERROR_CODE']=='COMPATIBILITY_REPORTING_FAILED')
        return 'NOT_UPDATED_REVIEW_REQUIRED'
    entry=new['ha_core'];require(entry['status']==fields['COMPATIBILITY_STATUS'] and (entry['observed_version'] or 'UNKNOWN')==fields['OBSERVED_HA_VERSION'])
    dep=next(x for x in registry['dependencies'] if x['dependency_id']=='ha_core')
    caps=entry['capabilities'];failed=entry['failed_capability']
    require(set(caps)<=set(dep['required_capabilities']+dep.get('optional_capabilities',[])))
    if entry['status'] in GOOD:
        require(all(caps.get(k) is True for k in dep['required_capabilities']))
    if entry['status']=='INCOMPATIBLE':require(failed==next((k for k in dep['required_capabilities'] if caps.get(k) is False),None) and failed is not None)
    if entry['status'] in GOOD and entry['observed_version']:
        require(entry['last_known_compatible_version']==entry['observed_version'] and entry['last_known_compatible_at']==entry['updated'])
    else:
        require(entry['last_known_compatible_version']==compat.safe_version(old.get('ha_core',{}).get('last_known_compatible_version')))
    require(entry['previous_known_compatible_version']==compat.safe_version(old.get('ha_core',{}).get('last_known_compatible_version')))
    # Replay pure framework sanitization/staleness semantics, not byte equality for unrelated entries.
    class MemoryStore:
        def read_json(self,*args):return before
        def write_json(self,name,payload,mode):self.payload=payload
    store=MemoryStore();compat._update_status(store,registry,{'ha_core':{'observed_version':entry['observed_version'],'capabilities':caps,'available':False if entry['status']=='DEPENDENCY_UNAVAILABLE' else None}},after['updated'])
    expected={x['dependency_id']:x for x in store.payload['dependencies']}
    require(entry==expected['ha_core'])
    for k in new:
        if k!='ha_core':require(new[k]==expected[k])
    require(compat.summarize(after['dependencies'],after['updated'])==after)
    return 'PASS'

def classify(fields,rc,checks):
    require(all(v in ('PASS','FAIL','TRUE','FALSE','UNKNOWN','NOT_APPLICABLE','NOT_UPDATED_REVIEW_REQUIRED') for v in checks.values()))
    if fields['RESULT']=='FAIL':
        require(rc!=0 and fields['FAILURE_STAGE'] in STAGES and fields['ERROR_CODE']==('BINDING_HISTORY_CAPACITY_EXCEEDED' if fields['FAILURE_STAGE']=='BINDING_HISTORY_CAPACITY' else fields['FAILURE_STAGE']+'_FAILED'))
        return 'FAIL'
    require(rc==0 and fields['FAILURE_STAGE']=='NONE' and fields['STATE_PUBLISHED']=='TRUE' and fields['LAST_KNOWN_GOOD_PRESERVED']=='FALSE' and fields['COMPATIBILITY_STATUS'] in GOOD)
    require(all(fields[k]!='UNKNOWN' for k in FIELDS[5:10]) and fields['HISTORICAL_BINDING_COUNT']=='0')
    if fields['RESULT']=='PASS_WITH_WARNING':
        require(fields['ERROR_CODE'] in WARNINGS and checks['STATE_SCHEMA_VALIDATION']=='PASS')
        require(all(v=='TRUE' for k,v in checks.items() if k.endswith('_UNCHANGED')))
        require(checks['ASSOCIATION_SCHEDULER_PRESENT']=='FALSE')
        require(checks['TRANSACTION_NAMESPACE_CLEAN']=='TRUE' or fields['ERROR_CODE']=='TRANSACTION_CLEANUP_FAILED' and checks['TRANSACTION_NAMESPACE_CLEAN']=='FALSE')
        require(checks['COMPATIBILITY_STATE_VALIDATION']=='PASS' or fields['ERROR_CODE']=='COMPATIBILITY_REPORTING_FAILED' and checks['COMPATIBILITY_STATE_VALIDATION']=='NOT_UPDATED_REVIEW_REQUIRED')
        return 'MANUAL_REVIEW_REQUIRED'
    require(fields['ERROR_CODE']=='NONE')
    require(all(v in ('PASS','TRUE','FALSE') for v in checks.values()))
    require(all(v=='TRUE' for k,v in checks.items() if k.endswith('_UNCHANGED') or k=='TRANSACTION_NAMESPACE_CLEAN'))
    require(checks['STATE_SCHEMA_VALIDATION']=='PASS' and checks['COMPATIBILITY_STATE_VALIDATION']=='PASS' and checks['ASSOCIATION_SCHEDULER_PRESENT']=='FALSE')
    return 'MANUAL_REVIEW_REQUIRED' if fields['ASSOCIATED_COUNT']=='0' else 'PASS'

def evidence_directory():
    os.umask(0o077)
    p=Path(tempfile.mkdtemp(prefix='hioc-pe4-ha-association-manual-',dir='/tmp'));os.chmod(p,0o700);return p

def validate_report(report):
    require(set(report)==set(FIELDS+EXTRA))
    enums={
        'TARGET':('PI3 NUT&PIHOLE',), 'DEPLOYED_SOURCE_COMMIT':(DEPLOYED,),
        'DEPLOYMENT_CLOSURE':('PASS_CLOSED','UNKNOWN'), 'ADAPTER_EXECUTION_COUNT':('0','1'),
        'RESULT':('PASS','PASS_WITH_WARNING','FAIL','UNKNOWN'),
        'ERROR_CODE':('UNKNOWN','NONE',*WARNINGS,'BINDING_HISTORY_CAPACITY_EXCEEDED',*(s+'_FAILED' for s in STAGES)),
        'FAILURE_STAGE':('UNKNOWN','NONE',*STAGES), 'COMPATIBILITY_STATUS':STATUS,
        'STATE_PUBLISHED':('TRUE','FALSE','UNKNOWN'), 'LAST_KNOWN_GOOD_PRESERVED':('TRUE','FALSE','UNKNOWN'),
        'PRE_RUN_PRIVATE_STATE':('ABSENT','UNKNOWN'), 'POST_RUN_PRIVATE_STATE':('PRESENT','ABSENT','UNKNOWN'),
        'WRAPPER_STATUS':('PRECONDITION_FAILED','EXECUTION_INCOMPLETE','POST_RUN_REVIEW_REQUIRED','COMPLETE'),
        'OVERALL_VALIDATION':('PASS','FAIL','MANUAL_REVIEW_REQUIRED'), 'MANUAL_REVIEW_REQUIRED':('TRUE','FALSE'),
        'CREDENTIAL_EXPOSED':('FALSE',), 'RAW_HA_DATA_PERSISTED':('FALSE',), 'PRIVATE_ASSOCIATION_CONTENT_EXPOSED':('FALSE',)}
    for k,v in report.items():
        require(type(v) is str and len(v)<=80)
        if k in enums:require(v in enums[k])
        elif k=='SOURCE_GOVERNANCE_COMMIT':require(v=='UNKNOWN' or re.fullmatch('[0-9a-f]{40}',v) is not None)
        elif k=='ADAPTER_RETURN_CODE':require(v=='UNKNOWN' or re.fullmatch(r'-?[0-9]{1,3}',v) and -64<=int(v)<=255)
        elif k=='OBSERVED_HA_VERSION':
            if v!='UNKNOWN':
                require(re.fullmatch(r'[0-9]{1,4}(?:\.[0-9]{1,4}){0,3}(?:(?:a|b|rc|\.dev)[0-9]{1,8})?',v) is not None)
                try:ipaddress.ip_address(v)
                except ValueError:pass
                else:raise Stop()
        elif k in FIELDS[5:10]:require(v=='UNKNOWN' or re.fullmatch(r'0|[1-9][0-9]{0,4}',v) and int(v)<=(4096 if k=='HISTORICAL_BINDING_COUNT' else 65536))
        else:require(v in ('PASS','FAIL','TRUE','FALSE','UNKNOWN','NOT_APPLICABLE','NOT_UPDATED_REVIEW_REQUIRED'))

def write_evidence(path,report,result=None):
    validate_report(report)
    if result is not None:require(result==('\n'.join(k+'='+report[k] for k in FIELDS)+'\n').encode('ascii'))
    files={'validation.json':canonical(report),'report.txt':('\n'.join(k+'='+report[k] for k in EXTRA+FIELDS)+'\n').encode('ascii')}
    if result is not None:files['result.txt']=result
    for name,raw in files.items():
        require(len(raw)<=16384)
        fd=os.open(path/name,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
        with os.fdopen(fd,'wb') as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())

def main(argv=None):
    args=sys.argv[1:] if argv is None else argv
    report={k:'UNKNOWN' for k in FIELDS+EXTRA};report.update(TARGET='PI3 NUT&PIHOLE',DEPLOYED_SOURCE_COMMIT=DEPLOYED,ADAPTER_EXECUTION_COUNT='0',CREDENTIAL_EXPOSED='FALSE',RAW_HA_DATA_PERSISTED='FALSE',PRIVATE_ASSOCIATION_CONTENT_EXPOSED='FALSE',OVERALL_VALIDATION='FAIL',WRAPPER_STATUS='PRECONDITION_FAILED',MANUAL_REVIEW_REQUIRED='TRUE')
    directory=None;raw=None;parsed=None
    try:
        require(len(args)==2 and args[0]=='--approved-preparation-commit' and re.fullmatch('[0-9a-f]{40}',args[1]) is not None)
        commit=args[1];report['SOURCE_GOVERNANCE_COMMIT']=commit
        require(sys.platform=='linux' and socket.gethostname()=='nutandpihole' and os.environ==ENV)
        import pwd,grp
        uid=pwd.getpwnam('jazofv1').pw_uid;gid=grp.getgrnam('jazofv1').gr_gid
        require(uid>0 and os.getuid()==os.geteuid()==uid and os.getgid()==os.getegid()==gid)
        require(re.search(rb'\binet 192\.168\.100\.252/',command(['/usr/sbin/ip','-o','-4','addr','show'])) is not None)
        closure,record=source_binding(commit)
        # Correction authorizes reconciliation only; a second adapter execution is prohibited.
        require(record['second_adapter_execution_authorized'] is True)
        d=load_module(SOURCE/'tools/hioc-pe4-ha-association-deploy.py','reviewed_deployment')
        d.LIMIT=LIMIT
        fs=d.NativeFS(HOME,uid,gid);deployment_integrity(d,fs,closure);runtime_probe(d)
        require(namespace(fs,d,True)==(False,True));report.update(PRE_RUN_PRIVATE_STATE='ABSENT',DEPLOYMENT_CLOSURE='PASS_CLOSED')
        cron=scheduler();config=fs.read(d.CONFIG);inventory=fs.read('state/inventory/inventory.json');require(inventory is not None)
        before=strict(fs.read('state/platform/compatibility.json',0o600))
        compat_schema=strict((SOURCE/'governance/compatibility-status.schema.json').read_bytes());schema_validate(before,compat_schema)
        adapter=load_module(SOURCE/'pi4/lib/hioc/home_assistant_association.py','reviewed_state_validation')
        compat=load_module(SOURCE/'pi4/lib/hioc/core/compatibility.py','reviewed_compatibility')
        schema=adapter.strict_json(fs.read(adapter.SCHEMA_PATH),'CONTRACT_VALIDATION');adapter.check_schema_contract(schema)
        registry=strict(fs.read('governance/compatibility-contracts.json'));snapshot=protected_snapshot(fs,closure,d)
        # Final read-only gates immediately before the sole child invocation.
        source_binding(commit);deployment_integrity(d,fs,closure);namespace(fs,d,True)
        require(scheduler()==cron and fs.read(d.CONFIG)==config and fs.read('state/inventory/inventory.json')==inventory)
        directory=evidence_directory();report['WRAPPER_STATUS']='EXECUTION_INCOMPLETE'
        try:
            rc,raw=invoke_once(lambda:report.__setitem__('ADAPTER_EXECUTION_COUNT','1'));report['ADAPTER_RETURN_CODE']=str(rc)
        except BaseException:raw=None

        try:
            parsed=parse_result(raw,compat);report.update(parsed);report['OUTPUT_VALIDATION']='PASS'
        except BaseException:report['OUTPUT_VALIDATION']='FAIL'
        def check(key,call):
            try:report[key]=call()
            except BaseException:report[key]='FAIL'
        def state_check():
            present,clean=namespace(fs,d)
            report.update(POST_RUN_PRIVATE_STATE='PRESENT' if present else 'ABSENT',TRANSACTION_NAMESPACE_CLEAN='TRUE' if clean else 'FALSE')
            if present:
                state=adapter.strict_json(fs.read(adapter.STATE,0o600),'CANDIDATE_STATE_VALIDATION');adapter.validate_state(state,schema)
                require(state['binding_history']==[])
                if parsed:
                    for key,name in zip(FIELDS[5:10],('associated_devices','review_only','rejected','unmatched','historical_bindings')):require(str(state['summary'][name])==parsed[key])
            if parsed:require((parsed['STATE_PUBLISHED']=='TRUE')==present)
            return 'PASS' if present else 'NOT_APPLICABLE'
        check('STATE_SCHEMA_VALIDATION',state_check)
        check('CONFIG_UNCHANGED',lambda:'TRUE' if fs.read(d.CONFIG)==config else 'FALSE')
        check('CANONICAL_INVENTORY_UNCHANGED',lambda:'TRUE' if fs.read('state/inventory/inventory.json')==inventory else 'FALSE')
        check('PLATFORM_STATUS_UNCHANGED',lambda:'TRUE' if sha(fs.read('pi4/bin/hioc-platform-status.py'))==closure['platform_status_sha256'] else 'FALSE')
        check('PLATFORM_CRON_UNCHANGED',lambda:'TRUE' if scheduler()==cron else 'FALSE')
        report['ASSOCIATION_SCHEDULER_PRESENT']='FALSE' if report['PLATFORM_CRON_UNCHANGED'] in ('TRUE','FALSE') else 'UNKNOWN'
        check('PROTECTED_PRODUCTION_SURFACES_UNCHANGED',lambda:'TRUE' if protected_snapshot(fs,closure,d)==snapshot else 'FALSE')
        check('COMPATIBILITY_STATE_VALIDATION',lambda:compatibility_validation(before,strict(fs.read('state/platform/compatibility.json',0o600)),parsed,compat,compat_schema,registry) if parsed else 'UNKNOWN')
        require(parsed is not None and report['ADAPTER_RETURN_CODE']!='UNKNOWN')
        checks={k:report[k] for k in ('STATE_SCHEMA_VALIDATION','TRANSACTION_NAMESPACE_CLEAN','CONFIG_UNCHANGED','CANONICAL_INVENTORY_UNCHANGED','PLATFORM_STATUS_UNCHANGED','PLATFORM_CRON_UNCHANGED','ASSOCIATION_SCHEDULER_PRESENT','PROTECTED_PRODUCTION_SURFACES_UNCHANGED','COMPATIBILITY_STATE_VALIDATION')}
        report['OVERALL_VALIDATION']=classify(parsed,rc,checks);report['MANUAL_REVIEW_REQUIRED']='FALSE' if report['OVERALL_VALIDATION']=='PASS' else 'TRUE';report['WRAPPER_STATUS']='COMPLETE'
    except BaseException:
        # Deliberately suppress exception values, malformed stdout, paths and private diagnostics.
        report['OVERALL_VALIDATION']='FAIL';report['MANUAL_REVIEW_REQUIRED']='TRUE'
        if report['ADAPTER_EXECUTION_COUNT']=='1':report['WRAPPER_STATUS']='POST_RUN_REVIEW_REQUIRED'
    try:
        if directory is None:directory=evidence_directory()
        write_evidence(directory,report,raw if parsed is not None else None)
        print('EVIDENCE_DIRECTORY='+str(directory))
        print((directory/'report.txt').read_text(encoding='ascii'),end='')
    except BaseException:print('EVIDENCE_WRITE=FAIL; MANUAL_REVIEW_REQUIRED=TRUE')
    return 0 if report['OVERALL_VALIDATION']=='PASS' else 1

if __name__=='__main__':raise SystemExit(main())
