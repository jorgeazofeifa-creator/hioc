"""Read-only source-only post-run reconciliation; no credential, HA or adapter execution.
FOR REVIEW ONLY - DO NOT RUN WITHOUT SEPARATE AUTHORIZATION.
Produces sanitized stdout only; never writes existing evidence or production.
"""
import errno
import importlib.util
import json
import os
from pathlib import Path
import re
import socket
import stat
import subprocess
import sys

SOURCE = Path('/home/jazofv1/hioc-release-source')
BASE = 'abae01b6eb60aecb12396d8078dee719d75801b7'
RECORD = 'governance/pe4/pe4-ha-association-bounded-manual-validation-correction.json'
EVIDENCE = '/tmp/hioc-pe4-ha-association-manual-3ciclqi7'
ENV = {'PATH':'/usr/sbin:/usr/bin:/bin','HOME':'/home/jazofv1','LANG':'C.UTF-8','LC_ALL':'C.UTF-8'}
FILES = ('result.txt','validation.json','report.txt')
REPORT_FIELDS = ('TARGET','SOURCE_CORRECTION_COMMIT','HISTORICAL_EVIDENCE_VALIDATION','HISTORICAL_ADAPTER_RESULT','HISTORICAL_WRAPPER_OVERALL_VALIDATION','HISTORICAL_PRODUCTION_FILES_UNCHANGED','HISTORICAL_ADAPTER_EXECUTION_COUNT','HISTORICAL_EXECUTION_TIME_CONFIG_PRESERVED','HISTORICAL_EXECUTION_TIME_INVENTORY_PRESERVED','PROTECTED_PRODUCTION_SURFACES_UNCHANGED','CURRENT_DEPLOYMENT_RUNTIME_SECURITY','CURRENT_PRIVATE_STATE_VALIDATION','CURRENT_STATE_COUNTS_AGREE','CURRENT_TRANSACTION_NAMESPACE_CLEAN','CURRENT_COMPATIBILITY_STATE_VALIDATION','CURRENT_PLATFORM_CRON_PRESERVED','CURRENT_ASSOCIATION_SCHEDULER_ABSENT','EXECUTION_TIME_COMPARISON_RECREATED','ADAPTER_EXECUTED_BY_RECONCILIATION','CREDENTIAL_ACCESSED_BY_RECONCILIATION','HA_NETWORK_ATTEMPTED_BY_RECONCILIATION','PRODUCTION_MUTATED_BY_RECONCILIATION','EXISTING_EVIDENCE_REWRITTEN','RAW_PRIVATE_DATA_EXPOSED','FAILURE_STAGE','RECONCILIATION')
STAGES = ('TARGET','SOURCE_AUTHORITY','HISTORICAL_EVIDENCE','PROTECTED_SURFACES','PRIVATE_STATE','COMPATIBILITY_STATE','FINAL_READ_ONLY_RECHECK','NONE')
class Stop(Exception): pass

def require(value):
    if not value:raise Stop()

def command(args):
    p=subprocess.run(args,cwd=SOURCE,env=ENV,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,timeout=15)
    require(p.returncode==0 and len(p.stdout)<=16*1024*1024);return p.stdout

def source_gate(commit):
    require(re.fullmatch('[0-9a-f]{40}',commit) is not None)
    def g(*a):return command(['/usr/bin/git',*a]).decode('ascii').strip()
    require(g('branch','--show-current')=='main' and g('rev-parse','HEAD')==g('rev-parse','origin/main')==commit)
    require(g('rev-parse','HEAD^')==BASE and g('rev-list','--left-right','--count','HEAD...origin/main')=='0\t0')
    require(g('show','-s','--format=%s','HEAD')=='PE-4: correct bounded validation production scope')
    require(not g('status','--porcelain','--untracked-files=all'))
    for n in ('MERGE_HEAD','CHERRY_PICK_HEAD','REVERT_HEAD','BISECT_LOG','BISECT_START','sequencer','rebase-apply','rebase-merge'):
        p=Path(g('rev-parse','--git-path',n));require(not (p if p.is_absolute() else SOURCE/p).exists())
    for path in (RECORD,RECORD.replace('.json','.schema.json'),'tools/hioc-pe4-ha-association-manual-validate.py','tools/hioc-pe4-ha-association-manual-reconcile.py'):
        require(command(['/usr/bin/git','show',commit+':'+path])==(SOURCE/path).read_bytes())

def module(path,name):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def acl_absent(fd):
    for name in ('system.posix_acl_access','system.posix_acl_default'):
        try:os.getxattr(fd,name)
        except OSError as error:require(error.errno==errno.ENODATA)
        else:raise Stop()

def object_security(info,uid,directory=False):
    require((stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode)) and info.st_uid==uid and stat.S_IMODE(info.st_mode)==(0o700 if directory else 0o600))
    if not directory:require(info.st_nlink==1 and info.st_size<=16384)

def stable_metadata(info):
    return tuple(getattr(info,k) for k in ('st_dev','st_ino','st_mode','st_uid','st_gid','st_nlink','st_size','st_mtime_ns','st_ctime_ns'))

def evidence_input(path,uid):
    """Pinned no-follow /tmp directory/files, bounded exact allowlist, no writes."""
    require(path==EVIDENCE and re.fullmatch(r'/tmp/hioc-pe4-ha-association-manual-[a-z0-9_-]+',path) is not None)
    parent=os.open('/tmp',os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC)
    fd=None
    try:
        parent_info=os.fstat(parent);require(stat.S_ISDIR(parent_info.st_mode) and parent_info.st_uid==0 and stat.S_IMODE(parent_info.st_mode)==0o1777)
        name=Path(path).name;fd=os.open(name,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC,dir_fd=parent)
        held=os.fstat(fd);object_security(held,uid,True);acl_absent(fd)
        require(set(os.listdir(fd))==set(FILES))
        result={}
        for filename in FILES:
            child=os.open(filename,os.O_RDONLY|os.O_NONBLOCK|os.O_NOFOLLOW|os.O_CLOEXEC,dir_fd=fd)
            try:
                before=os.fstat(child);object_security(before,uid);acl_absent(child)
                raw=bytearray()
                while len(raw)<=16384:
                    part=os.read(child,16385-len(raw))
                    if not part:break
                    raw.extend(part)
                after=os.fstat(child);named=os.stat(filename,dir_fd=fd,follow_symlinks=False)
                require(len(raw)<=16384 and len(raw)==before.st_size and stable_metadata(before)==stable_metadata(after) and stable_metadata(named)==stable_metadata(after))
                result[filename]=bytes(raw)
            finally:os.close(child)
        named=os.stat(name,dir_fd=parent,follow_symlinks=False)
        require((named.st_dev,named.st_ino)==(held.st_dev,held.st_ino) and stable_metadata(held)==stable_metadata(os.fstat(fd)) and set(os.listdir(fd))==set(FILES))
        return result
    finally:
        if fd is not None:os.close(fd)
        os.close(parent)

def validate_historical(files,m,correction,preparation,compat):
    require(set(files)==set(FILES))
    report=m.strict(files['validation.json'])
    require(m.canonical(report)==files['validation.json'])
    m.schema_validate(report,preparation['evidence_report_schema'])
    # Validate the historical allowlist through corrected pure sanitizer after a temporary rename.
    translated=dict(report);translated['PROTECTED_PRODUCTION_SURFACES_UNCHANGED']=translated.pop('PRODUCTION_FILES_UNCHANGED')
    m.validate_report(translated)
    require(report==correction['historical_evidence']['report'])
    fields=m.parse_result(files['result.txt'],compat)
    require(fields=={key:report[key] for key in m.FIELDS})
    old_extra=tuple('PRODUCTION_FILES_UNCHANGED' if k=='PROTECTED_PRODUCTION_SURFACES_UNCHANGED' else k for k in m.EXTRA)
    expected=('\n'.join(k+'='+report[k] for k in old_extra+m.FIELDS)+'\n').encode('ascii')
    require(files['report.txt']==expected)
    return report

def private_state(fs,d,m,adapter,historical):
    require(m.namespace(fs,d)==(True,True))
    value=adapter.strict_json(fs.read(adapter.STATE,0o600),'CANDIDATE_STATE_VALIDATION')
    schema=adapter.strict_json(fs.read(adapter.SCHEMA_PATH),'CONTRACT_VALIDATION');adapter.check_schema_contract(schema);adapter.validate_state(value,schema)
    require(value['binding_history']==[] and value['observed_ha_version']==historical['OBSERVED_HA_VERSION'])
    for field,key in zip(m.FIELDS[5:10],('associated_devices','review_only','rejected','unmatched','historical_bindings')):
        require(str(value['summary'][key])==historical[field])
    return True

def compatibility_state(fs,m,compat,historical):
    value=m.strict(fs.read('state/platform/compatibility.json',0o600))
    schema=m.strict((SOURCE/'governance/compatibility-status.schema.json').read_bytes());m.schema_validate(value,schema)
    registry=m.strict(fs.read('governance/compatibility-contracts.json'))
    entries=value['dependencies'];by_id={e['dependency_id']:e for e in entries}
    require(len(by_id)==len(entries)==value['dependency_count']==len(registry['dependencies']))
    require(set(by_id)=={d['dependency_id'] for d in registry['dependencies']})
    entry=by_id['ha_core'];require(entry['status']==historical['COMPATIBILITY_STATUS'] and entry['observed_version']==historical['OBSERVED_HA_VERSION'])
    dep=next(d for d in registry['dependencies'] if d['dependency_id']=='ha_core')
    require(all(entry['capabilities'].get(k) is True for k in dep['required_capabilities']) and entry['failed_capability'] is None)
    # Current semantic proof only: no historical private compatibility file is available.
    prior={'last_known_compatible_version':entry['previous_known_compatible_version']}
    expected=compat.assess(dep,{'observed_version':entry['observed_version'],'capabilities':entry['capabilities']},prior,entry['updated'])
    require(entry==expected and compat.summarize(entries,value['updated'])==value)
    return True

def reconcile_checks(m,d,fs,closure,historical,adapter,compat):
    before=m.protected_snapshot(fs,closure,d,include_inventory=False)
    private_state(fs,d,m,adapter,historical)
    compatibility_state(fs,m,compat,historical)
    after=m.protected_snapshot(fs,closure,d,include_inventory=False)
    require(before==after)
    return True

def report_text(report):
    require(set(report)==set(REPORT_FIELDS))
    for key,value in report.items():
        require(type(value) is str)
        if key=='TARGET':require(value=='PI3 NUT&PIHOLE')
        elif key=='SOURCE_CORRECTION_COMMIT':require(value=='UNKNOWN' or re.fullmatch('[0-9a-f]{40}',value) is not None)
        elif key=='FAILURE_STAGE':require(value in STAGES)
        else:require(value in ('PASS','FAIL','TRUE','FALSE','UNKNOWN','1'))
    return '\n'.join(k+'='+report[k] for k in REPORT_FIELDS)+'\n'

def main(argv=None):
    args=sys.argv[1:] if argv is None else argv
    report={k:'UNKNOWN' for k in REPORT_FIELDS};report.update(TARGET='PI3 NUT&PIHOLE',RECONCILIATION='FAIL',FAILURE_STAGE='TARGET',EXECUTION_TIME_COMPARISON_RECREATED='FALSE',ADAPTER_EXECUTED_BY_RECONCILIATION='FALSE',CREDENTIAL_ACCESSED_BY_RECONCILIATION='FALSE',HA_NETWORK_ATTEMPTED_BY_RECONCILIATION='FALSE',PRODUCTION_MUTATED_BY_RECONCILIATION='FALSE',EXISTING_EVIDENCE_REWRITTEN='FALSE',RAW_PRIVATE_DATA_EXPOSED='FALSE')
    try:
        require(len(args)==4 and args[0]=='--approved-correction-commit' and args[2]=='--evidence-directory')
        commit=args[1];require(re.fullmatch('[0-9a-f]{40}',commit) is not None);report['SOURCE_CORRECTION_COMMIT']=commit
        require(sys.platform=='linux' and socket.gethostname()=='nutandpihole' and os.environ==ENV)
        import pwd,grp
        uid=pwd.getpwnam('jazofv1').pw_uid;gid=grp.getgrnam('jazofv1').gr_gid
        require(uid>0 and os.getuid()==os.geteuid()==uid and os.getgid()==os.getegid()==gid)
        report['FAILURE_STAGE']='SOURCE_AUTHORITY';source_gate(commit)
        m=module(SOURCE/'tools/hioc-pe4-ha-association-manual-validate.py','reviewed_manual_definitions')
        closure,correction=m.source_binding(commit)
        require(correction['second_adapter_execution_authorized'] is False and correction['post_run_reconciliation']=='NOT_PERFORMED')
        preparation=m.strict((SOURCE/m.RECORD).read_bytes())
        compat=module(SOURCE/'pi4/lib/hioc/core/compatibility.py','reviewed_compatibility_definitions')
        report['FAILURE_STAGE']='HISTORICAL_EVIDENCE';files=evidence_input(args[3],uid)
        historical=validate_historical(files,m,correction,preparation,compat)
        report.update(HISTORICAL_EVIDENCE_VALIDATION='PASS',HISTORICAL_ADAPTER_RESULT=historical['RESULT'],HISTORICAL_WRAPPER_OVERALL_VALIDATION=historical['OVERALL_VALIDATION'],HISTORICAL_PRODUCTION_FILES_UNCHANGED=historical['PRODUCTION_FILES_UNCHANGED'],HISTORICAL_ADAPTER_EXECUTION_COUNT='1',HISTORICAL_EXECUTION_TIME_CONFIG_PRESERVED=historical['CONFIG_UNCHANGED'],HISTORICAL_EXECUTION_TIME_INVENTORY_PRESERVED=historical['CANONICAL_INVENTORY_UNCHANGED'])
        report['FAILURE_STAGE']='PROTECTED_SURFACES'
        d=module(SOURCE/'tools/hioc-pe4-ha-association-deploy.py','reviewed_deployment_definitions');d.LIMIT=m.LIMIT
        fs=d.NativeFS(m.HOME,uid,gid);before=m.protected_snapshot(fs,closure,d,include_inventory=False)
        report.update(CURRENT_DEPLOYMENT_RUNTIME_SECURITY='PASS',CURRENT_PLATFORM_CRON_PRESERVED='TRUE',CURRENT_ASSOCIATION_SCHEDULER_ABSENT='TRUE')
        report['FAILURE_STAGE']='PRIVATE_STATE';adapter=module(SOURCE/'pi4/lib/hioc/home_assistant_association.py','reviewed_state_definitions')
        private_state(fs,d,m,adapter,historical)
        report.update(CURRENT_PRIVATE_STATE_VALIDATION='PASS',CURRENT_STATE_COUNTS_AGREE='TRUE',CURRENT_TRANSACTION_NAMESPACE_CLEAN='TRUE')
        report['FAILURE_STAGE']='COMPATIBILITY_STATE';compatibility_state(fs,m,compat,historical);report['CURRENT_COMPATIBILITY_STATE_VALIDATION']='PASS'
        report['FAILURE_STAGE']='FINAL_READ_ONLY_RECHECK';source_gate(commit)
        require(m.protected_snapshot(fs,closure,d,include_inventory=False)==before and evidence_input(args[3],uid)==files)
        private_state(fs,d,m,adapter,historical);compatibility_state(fs,m,compat,historical)
        report.update(PROTECTED_PRODUCTION_SURFACES_UNCHANGED='TRUE',RECONCILIATION='PASS',FAILURE_STAGE='NONE')
    except BaseException:
        # No exception text, household paths/values or private objects enter stdout.
        report['RECONCILIATION']='FAIL'
    print(report_text(report),end='')
    return 0 if report['RECONCILIATION']=='PASS' else 1

if __name__=='__main__':raise SystemExit(main())
