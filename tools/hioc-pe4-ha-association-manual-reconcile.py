"""Read-only source-only post-run reconciliation; no credential, HA or adapter execution.
FOR REVIEW ONLY - DO NOT RUN WITHOUT SEPARATE AUTHORIZATION.
Produces sanitized stdout only; never writes existing evidence or production.
"""
import importlib.util
import os
from pathlib import Path
import re
import socket
import subprocess
import sys

SOURCE = Path('/home/jazofv1/hioc-release-source')
BASE = 'd767ad429ae0573ffb1411ccb787795063ef647c'
RECORD = 'governance/pe4/pe4-ha-association-bounded-manual-validation-correction.json'
AUTHORITY = 'governance/pe4/pe4-ha-association-reconciliation-evidence-authority-correction.json'
PREDECESSOR_SHA = '9534ee4846aa32aad3bff2db2d413ff56e558863634153e5bcd71d2a0fdfeede'
PREDECESSOR_SCHEMA_SHA = 'e8f9d4cf602dd183890b3cef0db0a957d31fe1584ec5bf052d71db5807f38afd'
ENV = {'PATH':'/usr/sbin:/usr/bin:/bin','HOME':'/home/jazofv1','LANG':'C.UTF-8','LC_ALL':'C.UTF-8'}
REPORT_FIELDS = ('TARGET','SOURCE_EVIDENCE_AUTHORITY_COMMIT','HISTORICAL_REPORT_AUTHORITY','HISTORICAL_REPORT_VALIDATION','HISTORICAL_ADAPTER_RESULT','HISTORICAL_WRAPPER_OVERALL_VALIDATION','HISTORICAL_PRODUCTION_FILES_UNCHANGED','HISTORICAL_ADAPTER_EXECUTION_COUNT','HISTORICAL_EXECUTION_TIME_CONFIG_PRESERVED','HISTORICAL_EXECUTION_TIME_INVENTORY_PRESERVED','ORIGINAL_EPHEMERAL_EVIDENCE_PRESENT','ORIGINAL_EPHEMERAL_EVIDENCE_REVALIDATION','ORIGINAL_EPHEMERAL_EVIDENCE_LIMITATION','PROTECTED_PRODUCTION_SURFACES_UNCHANGED','CURRENT_DEPLOYMENT_RUNTIME_SECURITY','CURRENT_PRIVATE_STATE_VALIDATION','CURRENT_STATE_COUNTS_AGREE','CURRENT_TRANSACTION_NAMESPACE_CLEAN','CURRENT_COMPATIBILITY_STATE_VALIDATION','CURRENT_PLATFORM_CRON_PRESERVED','CURRENT_ASSOCIATION_SCHEDULER_ABSENT','EXECUTION_TIME_COMPARISON_RECREATED','ADAPTER_EXECUTED_BY_RECONCILIATION','CREDENTIAL_ACCESSED_BY_RECONCILIATION','HA_NETWORK_ATTEMPTED_BY_RECONCILIATION','PRODUCTION_MUTATED_BY_RECONCILIATION','HISTORICAL_EVIDENCE_RECREATED','RAW_PRIVATE_DATA_EXPOSED','FAILURE_STAGE','RECONCILIATION')
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
    require(g('show','-s','--format=%s','HEAD')=='PE-4: correct reconciliation evidence authority')
    require(not g('status','--porcelain','--untracked-files=all'))
    for n in ('MERGE_HEAD','REBASE_HEAD','CHERRY_PICK_HEAD','REVERT_HEAD','BISECT_LOG','BISECT_START','sequencer','rebase-apply','rebase-merge'):
        p=Path(g('rev-parse','--git-path',n));require(not (p if p.is_absolute() else SOURCE/p).exists())
    for path in (AUTHORITY,AUTHORITY.replace('.json','.schema.json'),RECORD,RECORD.replace('.json','.schema.json'),'tools/hioc-pe4-ha-association-manual-validate.py','tools/hioc-pe4-ha-association-manual-reconcile.py'):
        require(command(['/usr/bin/git','show',commit+':'+path])==(SOURCE/path).read_bytes())

def module(path,name):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def frozen_input(m,path,digest,blob=None):
    raw=command(['/usr/bin/git','show',BASE+':'+path])
    require(m.sha(raw)==digest and raw==(SOURCE/path).read_bytes())
    if blob is not None:
        require(command(['/usr/bin/git','rev-parse',BASE+':'+path]).decode('ascii').strip()==blob)
    return raw

def source_authority(m,commit):
    """Exact successor and immutable predecessor authority; no historical /tmp access."""
    authority=m.strict((SOURCE/AUTHORITY).read_bytes())
    authority_schema=m.strict((SOURCE/AUTHORITY.replace('.json','.schema.json')).read_bytes())
    require(m.canonical(authority)==(SOURCE/AUTHORITY).read_bytes())
    m.schema_validate(authority,authority_schema)
    require(authority['starting_commit']==BASE and authority['second_adapter_execution_authorized'] is False)
    for key,path,digest in (('predecessor_record',RECORD,PREDECESSOR_SHA),('predecessor_schema',RECORD.replace('.json','.schema.json'),PREDECESSOR_SCHEMA_SHA)):
        item=authority[key];require(item['path']==path and item['sha256']==digest)
        frozen_input(m,path,digest,item['git_blob'])
    correction=m.strict(frozen_input(m,RECORD,PREDECESSOR_SHA))
    m.schema_validate(correction,m.strict(frozen_input(m,RECORD.replace('.json','.schema.json'),PREDECESSOR_SCHEMA_SHA)))
    for key in ('preparation','preparation_schema','deployment_closure','deployment_closure_schema','corrected_wrapper'):
        item=correction[key];frozen_input(m,item['path'],item['sha256'],item['git_blob'])
    closure=m.strict((SOURCE/m.CLOSURE).read_bytes())
    m.schema_validate(closure,m.strict((SOURCE/m.CLOSURE.replace('.json','.schema.json')).read_bytes()))
    require(closure['status']=='PASS_CLOSED' and closure['deployment_transaction']=='COMMITTED' and closure['deployed_source_commit']==m.DEPLOYED)
    for item in closure['sources'].values():
        frozen_input(m,item['path'],item['sha256'],item['git_blob'])
    preparation=m.strict((SOURCE/m.RECORD).read_bytes())
    m.schema_validate(preparation,m.strict((SOURCE/m.RECORD.replace('.json','.schema.json')).read_bytes()))
    item=preparation['compatibility_status_schema'];frozen_input(m,item['path'],item['sha256'],item['git_blob'])
    item=authority['reconciliation_tool'];require(item['path']=='tools/hioc-pe4-ha-association-manual-reconcile.py' and m.sha((SOURCE/item['path']).read_bytes())==item['sha256'])
    require(command(['/usr/bin/git','rev-parse',commit+':'+item['path']]).decode('ascii').strip()==item['git_blob'])
    return closure,correction

def validate_committed_report(m,correction):
    """COMMITTED_OPERATOR_SUPPLIED_REPORT_VALIDATION, never original artifact validation."""
    # Recheck immutable bytes even when this pure validator is called independently.
    raw=frozen_input(m,RECORD,PREDECESSOR_SHA)
    schema=m.strict(frozen_input(m,RECORD.replace('.json','.schema.json'),PREDECESSOR_SCHEMA_SHA))
    expected=m.strict(raw);m.schema_validate(correction,schema);require(correction==expected)
    report=correction['historical_evidence']['report']
    preparation=m.strict((SOURCE/m.RECORD).read_bytes())
    m.schema_validate(report,preparation['evidence_report_schema'])
    require(report['RESULT']=='PASS' and report['OVERALL_VALIDATION']=='FAIL' and report['PRODUCTION_FILES_UNCHANGED']=='FALSE' and report['ADAPTER_EXECUTION_COUNT']=='1')
    require(report['CONFIG_UNCHANGED']==report['CANONICAL_INVENTORY_UNCHANGED']=='TRUE')
    require(report['COMPATIBILITY_STATUS']=='COMPATIBLE' and report['OBSERVED_HA_VERSION']=='2026.9.4')
    old_extra=tuple('PRODUCTION_FILES_UNCHANGED' if k=='PROTECTED_PRODUCTION_SURFACES_UNCHANGED' else k for k in m.EXTRA)
    require(correction['historical_evidence']['exact_report_text']=='\n'.join(k+'='+report[k] for k in old_extra+m.FIELDS)+'\n')
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

KNOWN_LIMITATION = {
    'HISTORICAL_REPORT_AUTHORITY':'COMMITTED_OPERATOR_SUPPLIED_REPORT',
    'ORIGINAL_EPHEMERAL_EVIDENCE_PRESENT':'FALSE',
    'ORIGINAL_EPHEMERAL_EVIDENCE_REVALIDATION':'UNAVAILABLE',
    'ORIGINAL_EPHEMERAL_EVIDENCE_LIMITATION':'RECORDED',
}
NO_ACTIVITY = ('EXECUTION_TIME_COMPARISON_RECREATED','ADAPTER_EXECUTED_BY_RECONCILIATION','CREDENTIAL_ACCESSED_BY_RECONCILIATION','HA_NETWORK_ATTEMPTED_BY_RECONCILIATION','PRODUCTION_MUTATED_BY_RECONCILIATION','HISTORICAL_EVIDENCE_RECREATED','RAW_PRIVATE_DATA_EXPOSED')
SUCCESS = dict(KNOWN_LIMITATION,HISTORICAL_REPORT_VALIDATION='PASS',HISTORICAL_ADAPTER_RESULT='PASS',HISTORICAL_WRAPPER_OVERALL_VALIDATION='FAIL',HISTORICAL_PRODUCTION_FILES_UNCHANGED='FALSE',HISTORICAL_ADAPTER_EXECUTION_COUNT='1',HISTORICAL_EXECUTION_TIME_CONFIG_PRESERVED='TRUE',HISTORICAL_EXECUTION_TIME_INVENTORY_PRESERVED='TRUE',PROTECTED_PRODUCTION_SURFACES_UNCHANGED='TRUE',CURRENT_DEPLOYMENT_RUNTIME_SECURITY='PASS',CURRENT_PRIVATE_STATE_VALIDATION='PASS',CURRENT_STATE_COUNTS_AGREE='TRUE',CURRENT_TRANSACTION_NAMESPACE_CLEAN='TRUE',CURRENT_COMPATIBILITY_STATE_VALIDATION='PASS',CURRENT_PLATFORM_CRON_PRESERVED='TRUE',CURRENT_ASSOCIATION_SCHEDULER_ABSENT='TRUE',FAILURE_STAGE='NONE')

def report_text(report):
    require(set(report)==set(REPORT_FIELDS))
    require(all(report[k]==v for k,v in KNOWN_LIMITATION.items()))
    require(all(report[k]=='FALSE' for k in NO_ACTIVITY))
    for key,value in report.items():
        require(type(value) is str)
        if key=='TARGET':require(value=='PI3 NUT&PIHOLE')
        elif key=='SOURCE_EVIDENCE_AUTHORITY_COMMIT':require(value=='UNKNOWN' or re.fullmatch('[0-9a-f]{40}',value) is not None)
        elif key=='FAILURE_STAGE':require(value in STAGES)
        elif key in KNOWN_LIMITATION:continue
        elif key=='RECONCILIATION':require(value in ('PASS','FAIL'))
        else:require(value in ('PASS','FAIL','TRUE','FALSE','UNKNOWN','1'))
    if report['RECONCILIATION']=='PASS':
        require(all(report[k]==v for k,v in SUCCESS.items()) and report['SOURCE_EVIDENCE_AUTHORITY_COMMIT']!='UNKNOWN')
    return '\n'.join(k+'='+report[k] for k in REPORT_FIELDS)+'\n'

def main(argv=None):
    args=sys.argv[1:] if argv is None else argv
    report={k:'UNKNOWN' for k in REPORT_FIELDS};report.update(TARGET='PI3 NUT&PIHOLE',RECONCILIATION='FAIL',FAILURE_STAGE='TARGET',EXECUTION_TIME_COMPARISON_RECREATED='FALSE',ADAPTER_EXECUTED_BY_RECONCILIATION='FALSE',CREDENTIAL_ACCESSED_BY_RECONCILIATION='FALSE',HA_NETWORK_ATTEMPTED_BY_RECONCILIATION='FALSE',PRODUCTION_MUTATED_BY_RECONCILIATION='FALSE',HISTORICAL_EVIDENCE_RECREATED='FALSE',RAW_PRIVATE_DATA_EXPOSED='FALSE')
    report.update(KNOWN_LIMITATION)
    try:
        require(len(args)==2 and args[0]=='--approved-evidence-authority-commit')
        commit=args[1];require(re.fullmatch('[0-9a-f]{40}',commit) is not None);report['SOURCE_EVIDENCE_AUTHORITY_COMMIT']=commit
        require(sys.platform=='linux' and socket.gethostname()=='nutandpihole' and os.environ==ENV)
        import pwd,grp
        uid=pwd.getpwnam('jazofv1').pw_uid;gid=grp.getgrnam('jazofv1').gr_gid
        require(uid>0 and os.getuid()==os.geteuid()==uid and os.getgid()==os.getegid()==gid)
        report['FAILURE_STAGE']='SOURCE_AUTHORITY';source_gate(commit)
        m=module(SOURCE/'tools/hioc-pe4-ha-association-manual-validate.py','reviewed_manual_definitions')
        closure,correction=source_authority(m,commit)
        require(correction['second_adapter_execution_authorized'] is False and correction['post_run_reconciliation']=='NOT_PERFORMED')
        preparation=m.strict((SOURCE/m.RECORD).read_bytes())
        compat=module(SOURCE/'pi4/lib/hioc/core/compatibility.py','reviewed_compatibility_definitions')
        report['FAILURE_STAGE']='HISTORICAL_EVIDENCE'
        historical=validate_committed_report(m,correction)
        report.update(HISTORICAL_REPORT_VALIDATION='PASS',HISTORICAL_ADAPTER_RESULT=historical['RESULT'],HISTORICAL_WRAPPER_OVERALL_VALIDATION=historical['OVERALL_VALIDATION'],HISTORICAL_PRODUCTION_FILES_UNCHANGED=historical['PRODUCTION_FILES_UNCHANGED'],HISTORICAL_ADAPTER_EXECUTION_COUNT='1',HISTORICAL_EXECUTION_TIME_CONFIG_PRESERVED=historical['CONFIG_UNCHANGED'],HISTORICAL_EXECUTION_TIME_INVENTORY_PRESERVED=historical['CANONICAL_INVENTORY_UNCHANGED'])
        report['FAILURE_STAGE']='PROTECTED_SURFACES'
        d=module(SOURCE/'tools/hioc-pe4-ha-association-deploy.py','reviewed_deployment_definitions');d.LIMIT=m.LIMIT
        fs=d.NativeFS(m.HOME,uid,gid);before=m.protected_snapshot(fs,closure,d,include_inventory=False)
        report.update(CURRENT_DEPLOYMENT_RUNTIME_SECURITY='PASS',CURRENT_PLATFORM_CRON_PRESERVED='TRUE',CURRENT_ASSOCIATION_SCHEDULER_ABSENT='TRUE')
        report['FAILURE_STAGE']='PRIVATE_STATE';adapter=module(SOURCE/'pi4/lib/hioc/home_assistant_association.py','reviewed_state_definitions')
        private_state(fs,d,m,adapter,historical)
        report.update(CURRENT_PRIVATE_STATE_VALIDATION='PASS',CURRENT_STATE_COUNTS_AGREE='TRUE',CURRENT_TRANSACTION_NAMESPACE_CLEAN='TRUE')
        report['FAILURE_STAGE']='COMPATIBILITY_STATE';compatibility_state(fs,m,compat,historical);report['CURRENT_COMPATIBILITY_STATE_VALIDATION']='PASS'
        report['FAILURE_STAGE']='FINAL_READ_ONLY_RECHECK';source_gate(commit)
        require(source_authority(m,commit)==(closure,correction))
        require(m.protected_snapshot(fs,closure,d,include_inventory=False)==before and validate_committed_report(m,correction)==historical)
        private_state(fs,d,m,adapter,historical);compatibility_state(fs,m,compat,historical)
        report.update(PROTECTED_PRODUCTION_SURFACES_UNCHANGED='TRUE',RECONCILIATION='PASS',FAILURE_STAGE='NONE')
    except BaseException:
        # No exception text, household paths/values or private objects enter stdout.
        report['RECONCILIATION']='FAIL'
    print(report_text(report),end='')
    return 0 if report['RECONCILIATION']=='PASS' else 1

if __name__=='__main__':raise SystemExit(main())
