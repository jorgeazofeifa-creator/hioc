#!/usr/bin/env python3
"""Separately authorized read-only source validation; never installs or publishes.
Launch with python3 -I -B and an exact --source-commit. All native inputs are fixed.
Injected contexts are exclusively a unit-test API, not command-line options.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import types

SOURCE = Path('/home/jazofv1/hioc-release-source')
PRODUCTION = Path('/home/jazofv1/hioc')
RECORD = 'governance/pe4/pe4-ha-association-public-projection-implementation.json'
HELPER = 'pi4/lib/hioc/home_assistant_public_projection.py'
CHECKS = ['SOURCE_IMPLEMENTATION_IDENTITY','PRIVATE_ADAPTER_IDENTITY','PRIVATE_SCHEMA_IDENTITY',
          'POSIX_PATH_SECURITY','ASSOCIATION_LOCK_SECURITY','SHARED_LOCK_ACQUISITION',
          'TRANSACTION_NAMESPACE','PRIVATE_STATE_COPY','PRIVATE_STATE_SCHEMA',
          'PRIVATE_STATE_SEMANTICS','PUBLIC_CONTRACT','PUBLIC_CANDIDATE_DERIVATION',
          'CURRENT_INVENTORY_INTERSECTION']
ERRORS = frozenset(['NONE','SOURCE_COMMIT_MISMATCH','SOURCE_INVALID','TARGET_INVALID',
                   'OPERATOR_INVALID','IDENTITY_MISMATCH','ASSOCIATION_BUSY',
                   'UNEXPECTED_EXISTING_PUBLIC_PROJECTION','OMITTED_UNAVAILABLE',
                   'OMITTED_UNSAFE','OMITTED_INVALID','OMITTED_INCOHERENT','OMITTED_INTERNAL'])


class ValidationError(Exception):
    def __init__(self,code):self.code=code;super().__init__(code)


def check(condition,code):
    if not condition:raise ValidationError(code)


def constant_contract(value,node):
    if 'const' in node:
        check(type(value) is type(node['const']) and value==node['const'],'SOURCE_INVALID')
    elif node.get('type')=='object':
        check(type(value) is dict and node.get('additionalProperties') is False and set(value)==set(node['required'])==set(node['properties']),'SOURCE_INVALID')
        for k,v in value.items():constant_contract(v,node['properties'][k])
    else:
        check(type(value) is list and node.get('items') is False and len(value)==node['minItems']==node['maxItems']==len(node['prefixItems']),'SOURCE_INVALID')
        for v,s in zip(value,node['prefixItems']):constant_contract(v,s)


class NativeContext:
    def git(self,*args):
        env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
        return subprocess.check_output(['git','-c','core.fsmonitor=false',*args],cwd=SOURCE,env=env,stderr=subprocess.DEVNULL)

    def target(self):
        check(sys.platform=='linux' and os.uname().nodename=='nutandpihole','TARGET_INVALID')
        import pwd
        user=pwd.getpwnam('jazofv1')
        check(os.getuid()==os.geteuid()==user.pw_uid,'OPERATOR_INVALID')
        check(Path(__file__).resolve().parents[1]==SOURCE,'SOURCE_INVALID')

    def source(self,commit):
        check(self.git('rev-parse','HEAD').decode().strip()==commit,'SOURCE_COMMIT_MISMATCH')
        check(self.git('branch','--show-current').strip()==b'main','SOURCE_INVALID')
        check(self.git('rev-parse','origin/main').decode().strip()==commit,'SOURCE_INVALID')
        check(not self.git('status','--porcelain','--untracked-files=all').strip(),'SOURCE_INVALID')
        for op in ['MERGE_HEAD','CHERRY_PICK_HEAD','REVERT_HEAD','BISECT_START','rebase-merge','rebase-apply','sequencer','index.lock']:
            path=Path(self.git('rev-parse','--git-path',op).decode().strip())
            check(not (path if path.is_absolute() else SOURCE/path).exists(),'SOURCE_INVALID')
        record=json.loads(self.git('show',commit+':'+RECORD))
        schema=json.loads(self.git('show',commit+':'+RECORD.replace('.json','.schema.json')))
        constant_contract(record,schema)
        for item in record['implementation_artifacts']:
            raw=self.git('show',commit+':'+item['path'])
            check(hashlib.sha256(raw).hexdigest()==item['sha256'],'IDENTITY_MISMATCH')
            check(self.git('rev-parse',commit+':'+item['path']).decode().strip()==item['git_blob'],'IDENTITY_MISMATCH')
        helper_raw=self.git('show',commit+':'+HELPER)
        module=types.ModuleType('hioc.home_assistant_public_projection')
        module.__file__=str(SOURCE/HELPER);module.__package__='hioc'
        exec(compile(helper_raw,module.__file__,'exec'),module.__dict__)
        return module

    def contracts(self,helper):
        uid,gid=helper.native_identity()
        with helper.SecureReader(SOURCE,uid,gid) as reader:
            validators=helper.load_contracts(reader.relative_file)
        with helper.SecureReader(PRODUCTION,uid,gid) as reader:
            for path,sha in [(helper.MODULE_PATH,helper.MODULE_SHA),(helper.PRIVATE_SCHEMA_PATH,helper.PRIVATE_SCHEMA_SHA)]:
                check(hashlib.sha256(reader.relative_file(path)).hexdigest()==sha,'IDENTITY_MISMATCH')
        return validators

    def snapshot(self,helper):
        uid,gid=helper.native_identity()
        with helper.SecureReader(PRODUCTION/'state/inventory/associations',uid,gid) as reader:
            return reader.snapshot()

    def inventory(self,helper,private):
        uid,gid=helper.native_identity()
        with helper.SecureReader(PRODUCTION,uid,gid) as reader:
            raw=reader.relative_file('state/inventory/inventory.json')
        return private.strict_json(raw,'CANDIDATE_STATE_VALIDATION')


def validate_source(commit,context=None):
    result={k:'NOT_STARTED' for k in CHECKS}
    result.update(TARGET='PI3 NUT&PIHOLE',SOURCE_COMMIT='UNVERIFIED',MODE='READ_ONLY_SOURCE_VALIDATION',
                  PRIOR_PUBLIC_PROJECTION_PRESENT='UNKNOWN',PUBLIC_PROJECTION_ALREADY_PRESENT='UNKNOWN',
                  PUBLIC_OUTPUT_WRITTEN=False,MQTT_PUBLISHED=False,HA_NETWORK_ATTEMPTED=False,
                  CREDENTIAL_ACCESSED=False,ADAPTER_EXECUTED=False,CRONTAB_MUTATED=False,
                  PRODUCTION_MUTATED=False,RESULT='FAIL',ERROR_CODE='OMITTED_INTERNAL',STOP_REQUIRED=True)
    context=context or NativeContext()
    try:
        check(type(commit) is str and re.fullmatch('[0-9a-f]{40}',commit) is not None,'SOURCE_COMMIT_MISMATCH')
        context.target();helper=context.source(commit)
        result['SOURCE_COMMIT']=commit;result['SOURCE_IMPLEMENTATION_IDENTITY']='PASS'
        private,schema,public=context.contracts(helper)
        result['PRIVATE_ADAPTER_IDENTITY']=result['PRIVATE_SCHEMA_IDENTITY']=result['PUBLIC_CONTRACT']='PASS'
        raw=context.snapshot(helper)
        for key in ['POSIX_PATH_SECURITY','ASSOCIATION_LOCK_SECURITY','SHARED_LOCK_ACQUISITION','PRIVATE_STATE_COPY']:result[key]='PASS'
        result['TRANSACTION_NAMESPACE']='CLEAN'
        state=private.strict_json(raw,'CANDIDATE_STATE_VALIDATION')
        private.validate_state(state,schema)
        result['PRIVATE_STATE_SCHEMA']=result['PRIVATE_STATE_SEMANTICS']='PASS'
        inventory=context.inventory(helper,private)
        check(type(inventory) is dict and inventory.get('schema_version')=='1.0' and type(inventory.get('devices')) is list and all(type(d) is dict for d in inventory['devices']),'OMITTED_INVALID')
        present=any('home_assistant' in d for d in inventory['devices'])
        result['PRIOR_PUBLIC_PROJECTION_PRESENT']=result['PUBLIC_PROJECTION_ALREADY_PRESENT']=present
        check(not present,'UNEXPECTED_EXISTING_PUBLIC_PROJECTION')
        helper.derive_projection(inventory['devices'],state,private,schema,public)
        result['PUBLIC_CANDIDATE_DERIVATION']=result['CURRENT_INVENTORY_INTERSECTION']='PASS'
        context.source(commit)  # Source authority stays exact through the read-only run.
        result['RESULT']='PASS';result['ERROR_CODE']='NONE'
    except Exception as error:
        try:code=getattr(error,'code','OMITTED_INTERNAL')
        except Exception:code='OMITTED_INTERNAL'
        if type(code) is not str:code='OMITTED_INTERNAL'
        if code=='OMITTED_BUSY':
            result['RESULT']='INCOMPLETE';result['SHARED_LOCK_ACQUISITION']='BUSY';code='ASSOCIATION_BUSY'
        result['ERROR_CODE']=code if code in ERRORS else 'OMITTED_INTERNAL'
    return result


def main(argv=None):
    sys.dont_write_bytecode=True
    args=list(sys.argv[1:] if argv is None else argv)
    commit=args[1] if len(args)==2 and args[0]=='--source-commit' else None
    result=validate_source(commit)
    text='\n'.join(k+'='+('TRUE' if v is True else 'FALSE' if v is False else str(v)) for k,v in result.items())+'\n'
    if len(text.encode())>8192:text='RESULT=FAIL\nERROR_CODE=OMITTED_INTERNAL\nSTOP_REQUIRED=TRUE\n'
    print(text,end='')
    return 0 if result['RESULT']=='PASS' else 2 if result['RESULT']=='INCOMPLETE' else 1


if __name__=='__main__':raise SystemExit(main())
