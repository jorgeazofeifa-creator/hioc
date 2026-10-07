"""Source-only READ_ONLY acceptance sequence; separately authorized execution only."""
import importlib.util,json,os,re,socket,subprocess,sys
from pathlib import Path
SOURCE=Path('/home/jazofv1/hioc-release-source')
BASE='27377b95658010bf35c2b1fab8009de3d6f24bb6'
SUBJECT='PE-4: harden independent acceptance operator path'
RECORD='governance/pe4/pe4-ha-association-independent-production-acceptance-operator-path.json'
ENV={'PATH':'/usr/sbin:/usr/bin:/bin','HOME':'/home/jazofv1','LANG':'C.UTF-8','LC_ALL':'C.UTF-8'}
PASS_RC=0
FAIL_RC=2
GATES=('DEPLOYMENT','RUNTIME','PRIVATE_STATE','COMPATIBILITY','INVENTORY','CRON_SCHEDULER','PROTECTED_SURFACES_UNCHANGED','CHECKPOINT_COUNTS_AGREE')
def canonical(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False)+'\n').encode('ascii')
def require(v):
 if not v:raise ValueError('bounded acceptance failure')
def git(*args):
 p=subprocess.run(['/usr/bin/git',*args],cwd=SOURCE,env=ENV,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,timeout=15);require(p.returncode==0 and len(p.stdout)<=16777216);return p.stdout
def source_gate(commit):
 require(re.fullmatch('[0-9a-f]{40}',commit) is not None)
 require(git('rev-parse','HEAD').strip().decode()==git('rev-parse','origin/main').strip().decode()==commit)
 require(git('branch','--show-current').strip()==b'main' and git('rev-parse','HEAD^').strip().decode()==BASE)
 require(git('show','-s','--format=%s','HEAD').strip().decode()==SUBJECT and not git('status','--porcelain'))
 for n in ('MERGE_HEAD','REBASE_HEAD','CHERRY_PICK_HEAD','REVERT_HEAD','sequencer','rebase-merge','rebase-apply','BISECT_LOG','BISECT_START'):
  p=Path(git('rev-parse','--git-path',n).strip().decode());require(not (p if p.is_absolute() else SOURCE/p).exists())
 record=json.loads(git('show',commit+':'+RECORD));require((SOURCE/RECORD).read_bytes()==git('show',commit+':'+RECORD))
 import hashlib
 for item in record['implementation_bindings']+record['read_only_bindings']:
  raw=(SOURCE/item['path']).read_bytes();require(hashlib.sha256(raw).hexdigest()==item['sha256'] and git('show',commit+':'+item['path'])==raw)
 return record
def module(relative,name):
 spec=importlib.util.spec_from_file_location(name,SOURCE/relative);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def existing_checks(report):
 import pwd,grp
 m=module('tools/hioc-pe4-ha-association-manual-validate.py','acceptance_manual_definitions')
 d=module('tools/hioc-pe4-ha-association-deploy.py','acceptance_deployment_definitions')
 n=module('tools/hioc-pe4-ha-association-manual-reconcile.py','acceptance_state_definitions')
 a=module('pi4/lib/hioc/home_assistant_association.py','acceptance_adapter_definitions')
 c=module('pi4/lib/hioc/core/compatibility.py','acceptance_compatibility_definitions')
 closure=m.strict((SOURCE/m.CLOSURE).read_bytes());history=m.strict((SOURCE/n.RECORD).read_bytes())['historical_evidence']['report']
 d.LIMIT=m.LIMIT;uid=pwd.getpwnam('jazofv1').pw_uid;gid=grp.getgrnam('jazofv1').gr_gid
 require(uid>0 and os.getuid()==os.geteuid()==uid and os.getgid()==os.getegid()==gid)
 fs=d.NativeFS(m.HOME,uid,gid)
 report['FAILURE_STAGE']='DEPLOYMENT_RUNTIME';before=m.protected_snapshot(fs,closure,d,include_inventory=False)
 for k in ('DEPLOYMENT','RUNTIME','CRON_SCHEDULER'):report[k]='PASS'
 report['FAILURE_STAGE']='PRIVATE_STATE';private=fs.read(a.STATE,0o600);n.private_state(fs,d,m,a,history)
 report['PRIVATE_STATE']=report['CHECKPOINT_COUNTS_AGREE']='PASS'
 report['FAILURE_STAGE']='COMPATIBILITY';compatibility=fs.read('state/platform/compatibility.json',0o600);n.compatibility_state(fs,m,c,history);report['COMPATIBILITY']='PASS'
 report['FAILURE_STAGE']='INVENTORY'
 from datetime import datetime,timezone
 a.validate_inventory(fs.read('state/inventory/inventory.json'),datetime.now(timezone.utc));report['INVENTORY']='PASS'
 report['FAILURE_STAGE']='FINAL_RECHECK';n.private_state(fs,d,m,a,history);n.compatibility_state(fs,m,c,history)
 require(private==fs.read(a.STATE,0o600) and compatibility==fs.read('state/platform/compatibility.json',0o600))
 require(before==m.protected_snapshot(fs,closure,d,include_inventory=False));report['PROTECTED_SURFACES_UNCHANGED']='PASS'
def produce(commit,checks=existing_checks,gate=source_gate,target=True):
 report={k:'UNKNOWN' for k in GATES};report.update(TARGET='PI3 NUT&PIHOLE',SOURCE_COMMIT=commit,MODE='READ_ONLY',ORIGINAL_EPHEMERAL_EVIDENCE_REVALIDATION='UNAVAILABLE',ORIGINAL_EPHEMERAL_EVIDENCE_LIMITATION='RECORDED',ADAPTER_EXECUTED=False,HA_NETWORK_ATTEMPTED=False,CREDENTIAL_ACCESSED=False,PRODUCTION_MUTATED=False,RESULT='FAIL',FAILURE_STAGE='SOURCE')
 try:
  require(re.fullmatch('[0-9a-f]{40}',commit) is not None and target)
  gate(commit);checks(report);gate(commit);require(all(report[k]=='PASS' for k in GATES));report.update(RESULT='PASS',FAILURE_STAGE='NONE')
 except BaseException:report['RESULT']='FAIL'
 return canonical(report),PASS_RC if report['RESULT']=='PASS' else FAIL_RC

def main(argv=None):
 args=sys.argv[1:] if argv is None else argv
 # Invalid arguments never begin inspection or generate private diagnostics.
 if len(args)!=2 or args[0]!='--source-commit' or re.fullmatch('[0-9a-f]{40}',args[1]) is None:return FAIL_RC
 raw,rc=produce(args[1],target=sys.platform=='linux' and socket.gethostname()=='nutandpihole' and dict(os.environ)==ENV)
 sys.stdout.buffer.write(raw);return rc
if __name__=='__main__':raise SystemExit(main())
