"""Prepared source-only scheduler installer. Future separate authorization only.
One crontab installation attempt; no adapter/credential/network/state execution.
"""
import argparse,hashlib,importlib.util,json,os,re,socket,stat,subprocess,sys,time
from pathlib import Path
SOURCE=Path('/home/jazofv1/hioc-release-source')
HOME=Path('/home/jazofv1/hioc')
BASE='826608b40d5248c67742a17fc95a6e7612981df1'
SUBJECT='PE-4: prepare association scheduler deployment'
RECORD='governance/pe4/pe4-ha-association-scheduler-deployment-preparation.json'
ACCEPTANCE='governance/pe4/pe4-ha-association-independent-production-acceptance-closure.json'
PLATFORM=b'17 3 * * * flock -n /tmp/hioc-platform-status.lock /home/jazofv1/hioc/pi4/bin/hioc-platform-status.py'
MARKER=b'# HIOC_PE4_HA_ASSOCIATION'
LINE=b'5,35 * * * * /home/jazofv1/hioc/runtime/pe4/active/bin/python -I -B /home/jazofv1/hioc/pi4/bin/hioc-home-assistant-association.py >/dev/null 2>&1'
BLOCK=MARKER+b'\n'+LINE+b'\n'
LIMIT=65536
TIMEOUT=15
ENV={'PATH':'/usr/sbin:/usr/bin:/bin','HOME':'/home/jazofv1','LANG':'C.UTF-8','LC_ALL':'C.UTF-8'}
SUSPICIOUS=re.compile(rb'(?i)(hioc.pe4.ha.association|hioc.home.assistant|hioc.ha.association|inventory/associations|home.assistant|ha.association)')
OPERATIONS=('MERGE_HEAD','REBASE_HEAD','CHERRY_PICK_HEAD','REVERT_HEAD','sequencer','rebase-merge','rebase-apply','BISECT_LOG','BISECT_START')
class Failure(Exception):pass
class Parser(argparse.ArgumentParser):
 def error(self,message):raise Failure()

def require(v):
 if not v:raise Failure()
def sha(raw):return hashlib.sha256(raw).hexdigest()
def canonical(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False)+'\n').encode('ascii')
def crontab_bytes(raw):
 require(type(raw) is bytes and len(raw)<=LIMIT and b'\0' not in raw and b'\r' not in raw)
 try:raw.decode('utf8','strict')
 except UnicodeError:raise Failure() from None
 return raw

def prior_crontab(raw):
 crontab_bytes(raw);require(not SUSPICIOUS.search(raw))
 lines=raw.split(b'\n');require([x for x in lines if not x.lstrip().startswith(b'#') and b'hioc-platform-status' in x]==[PLATFORM])
 return raw

def candidate_crontab(raw):
 prior_crontab(raw);candidate=raw+(b'\n' if raw and not raw.endswith(b'\n') else b'')+BLOCK
 crontab_bytes(candidate);return candidate

def verify_candidate(prior,current):
 crontab_bytes(current);require(current==candidate_crontab(prior))
 require(current.split(b'\n').count(LINE)==current.split(b'\n').count(MARKER)==1)
 require([x for x in current.split(b'\n') if not x.lstrip().startswith(b'#') and b'hioc-platform-status' in x]==[PLATFORM]);return True

def check_surfaces(entries):
 require(type(entries) is list and len(entries)<=4096)
 seen=set()
 for name,raw in entries:
  require(type(name) is str and name not in seen and len(name)<=4096);seen.add(name)
  require(type(raw) is bytes and len(raw)<=LIMIT and not SUSPICIOUS.search(name.encode('utf8')+b'\n'+raw))
 return sha(canonical([[n,sha(b)] for n,b in sorted(entries)]))

def source_gate(commit,root=SOURCE,run=subprocess.run):
 require(re.fullmatch('[0-9a-f]{40}',commit) is not None and root.resolve()==Path(__file__).resolve().parents[1])
 def git(*a):
  p=run(['git','-C',str(root),*a],stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,timeout=TIMEOUT,env=ENV if os.name=='posix' else None)
  require(p.returncode==0 and len(p.stdout)<=16777216);return p.stdout
 require(git('rev-parse','HEAD').strip().decode()==git('rev-parse','origin/main').strip().decode()==commit)
 require(git('branch','--show-current').strip()==b'main' and git('rev-parse','HEAD^').strip().decode()==BASE)
 require(git('show','-s','--format=%s','HEAD').strip().decode()==SUBJECT and not git('status','--porcelain'))
 for n in OPERATIONS:
  p=Path(git('rev-parse','--git-path',n).strip().decode());require(not (p if p.is_absolute() else root/p).exists())
 record_raw=git('show',commit+':'+RECORD);record=json.loads(record_raw)
 require((root/RECORD).read_bytes().replace(b'\r\n',b'\n')==record_raw and record['status']=='PASS_CLOSED')
 for item in record['sources']:
  raw=git('show',BASE+':'+item['path']);require(sha(raw)==item['sha256'] and git('rev-parse',BASE+':'+item['path']).strip().decode()==item['git_blob'])
  current=(root/item['path']).read_bytes().replace(b'\r\n',b'\n');require(current==git('show',commit+':'+item['path']))
  if not item['historical_only']:require(current==raw)
 own=Path(__file__).read_bytes().replace(b'\r\n',b'\n');require(sha(own)==record['deployment_tool']['sha256'] and git('show',commit+':tools/'+Path(__file__).name)==own)
 acceptance=json.loads((root/ACCEPTANCE).read_bytes());require(acceptance['status']=='PASS_CLOSED' and acceptance['lifecycle']['independent_production_acceptance']=='PASS_CLOSED' and acceptance['attempt_2']['status']=='PASS')
 return record

def target_gate(host=None,user=None,uid=None,euid=None,gid=None,egid=None):
 if host is None:
  import pwd
  host=socket.gethostname();who=pwd.getpwnam('jazofv1');user=pwd.getpwuid(os.geteuid()).pw_name;uid=os.getuid();euid=os.geteuid();gid=os.getgid();egid=os.getegid()
  require(uid==who.pw_uid and gid==who.pw_gid)
 require(host=='nutandpihole' and user=='jazofv1' and type(uid) is int and uid==euid and uid>0 and type(gid) is int and gid==egid and gid>0)

def read_command(command):
 # Binary bounded pipe works in native Windows fixtures and the future Linux CLI.
 import threading,queue
 p=subprocess.Popen(command,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,env=ENV)
 chunks=queue.Queue(maxsize=2)
 def read():
  try:
   while True:
    chunk=p.stdout.read1(4096);chunks.put(chunk)
    if not chunk:break
  except BaseException:chunks.put(None)
 threading.Thread(target=read,daemon=True).start();raw=bytearray();deadline=time.monotonic()+TIMEOUT
 try:
  while True:
   remaining=deadline-time.monotonic();require(remaining>0)
   chunk=chunks.get(timeout=remaining);require(chunk is not None)
   if not chunk:break
   raw.extend(chunk);require(len(raw)<=LIMIT)
  require(p.wait(timeout=max(.01,deadline-time.monotonic()))==0);return bytes(raw)
 except BaseException:
  p.kill();p.wait(timeout=5);raise
 finally:p.stdout.close()

class NativeOps:
 def read(self):return read_command(['/usr/bin/crontab','-l'])
 def install(self,candidate):
  return subprocess.run(['/usr/bin/crontab','-'],input=candidate,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=TIMEOUT,env=ENV).returncode
 def surfaces(self,fs=None,names=None,readlink=os.readlink):
  # Reuse bound deployment filesystem security; never follow scheduler symlinks.
  if fs is None:
   d=module('tools/hioc-pe4-ha-association-deploy.py','scheduler_surface_filesystem');d.LIMIT=LIMIT
   fs=d.NativeFS(Path('/'),os.geteuid(),os.getegid())
  roots=('etc/crontab','etc/cron.d','etc/systemd/system','home/jazofv1/.config/systemd/user');entries=[];visited=0
  def children(fd):
   with os.scandir(fd) as items:
    for item in items:yield item.name
  def scan(relative,root=False):
   nonlocal visited
   visited+=1;require(visited<=4096)
   info=fs.info(relative)
   if info is None:return
   require(info.st_uid in (0,fs.uid))
   if stat.S_ISLNK(info.st_mode):
    require(not root)
    parent,name=relative.rsplit('/',1)
    with fs.directory(parent) as fd:target=readlink(name,dir_fd=fd)
    require(type(target) is str and fs.info(relative)==info);entries.append(('/'+relative,target.encode('utf8')));return
   require(not stat.S_IMODE(info.st_mode)&0o7022)
   if stat.S_ISDIR(info.st_mode):
    entries.append(('/'+relative,str((info.st_mode,info.st_uid,info.st_gid,info.st_dev,info.st_ino)).encode()))
    with fs.directory(relative) as fd:
     for name in (names or children)(fd):
      require(type(name) is str and name not in ('','.','..') and '/' not in name and len(name)<=255)
      scan(relative+'/'+name)
    require(fs.info(relative)==info);return
   require(stat.S_ISREG(info.st_mode) and info.st_nlink==1 and info.st_size<=LIMIT)
   raw=fs.read(relative);require(type(raw) is bytes and len(raw)<=LIMIT and len(raw)==info.st_size and fs.info(relative)==info)
   entries.append(('/'+relative,raw))
  for root in roots:scan(root,True)
  return check_surfaces(entries)

def module(path,name):
 spec=importlib.util.spec_from_file_location(name,SOURCE/path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def read_only_production_gate(m,d,fs,closure,surfaces):
 m.deployment_integrity(d,fs,closure);m.runtime_probe(d)
 return surfaces()

def native_guard(commit,ops):
 target_gate();source_gate(commit)
 m=module('tools/hioc-pe4-ha-association-manual-validate.py','scheduler_manual_definitions');d=module('tools/hioc-pe4-ha-association-deploy.py','scheduler_deployment_definitions')
 import pwd
 who=pwd.getpwnam('jazofv1');fs=d.NativeFS(HOME,who.pw_uid,who.pw_gid);closure=json.loads((SOURCE/m.CLOSURE).read_bytes())
 return read_only_production_gate(m,d,fs,closure,ops.surfaces) # No main or credential-reading prerequisites.

def deploy(commit,ops,guard):
 report={'RESULT':'FAIL','ERROR_CODE':'PRECHECK_FAILED','FAILURE_STAGE':'PRECHECK','SOURCE_COMMIT':commit,'INSTALL_ATTEMPTS':0,'MUTATION_STATE':'NOT_ATTEMPTED','MANUAL_REVIEW_REQUIRED':False,'STOP_REQUIRED':True,'ADAPTER_EXECUTED':False,'CREDENTIAL_ACCESSED':False,'HA_NETWORK_ATTEMPTED':False,'ASSOCIATION_STATE_MUTATED':False,'PUBLIC_PROJECTION_EXECUTED':False,'AUTOMATIC_RETRY':False,'ROLLBACK_PERFORMED':False,'PRIOR_CRONTAB_SHA256':'UNAVAILABLE','CANDIDATE_CRONTAB_SHA256':'UNAVAILABLE'}
 try:
  baseline=guard(commit);prior=prior_crontab(ops.read());candidate=candidate_crontab(prior)
  report.update(PRIOR_CRONTAB_SHA256=sha(prior),CANDIDATE_CRONTAB_SHA256=sha(candidate),FAILURE_STAGE='PRE_MUTATION',ERROR_CODE='PRE_MUTATION_DRIFT')
  require(guard(commit)==baseline and ops.read()==prior)
  report.update(INSTALL_ATTEMPTS=1,MUTATION_STATE='UNKNOWN',MANUAL_REVIEW_REQUIRED=True,FAILURE_STAGE='INSTALL',ERROR_CODE='INSTALL_OUTCOME_UNCERTAIN')
  try:rc=ops.install(candidate)
  except BaseException:rc=None
  report.update(FAILURE_STAGE='POST_INSTALL')
  try:current=crontab_bytes(ops.read())
  except BaseException:return report
  report['MUTATION_STATE']='CANDIDATE_OBSERVED' if current==candidate else ('PRIOR_OBSERVED' if current==prior else 'OTHER_OBSERVED')
  if type(rc) is not int or rc!=0:return report
  report['ERROR_CODE']='POST_INSTALL_MISMATCH';verify_candidate(prior,current)
  require(guard(commit)==baseline and ops.read()==candidate)
  report.update(RESULT='PASS',ERROR_CODE='NONE',FAILURE_STAGE='NONE',MUTATION_STATE='VERIFIED_INSTALLED',MANUAL_REVIEW_REQUIRED=False)
 except BaseException:pass
 return report

def main(argv=None):
 try:
  require(sys.platform=='linux' and os.name=='posix' and dict(os.environ)==ENV)
  parser=Parser(add_help=False,exit_on_error=False);parser.add_argument('--source-commit',required=True);parser.add_argument('--install-scheduler-authorized',action='store_true',required=True);args=parser.parse_args(argv)
  require(args.install_scheduler_authorized and re.fullmatch('[0-9a-f]{40}',args.source_commit) is not None)
  ops=NativeOps();report=deploy(args.source_commit,ops,lambda c:native_guard(c,ops));sys.stdout.buffer.write(canonical(report));return 0 if report['RESULT']=='PASS' else 2
 except BaseException:
  sys.stdout.buffer.write(canonical({'RESULT':'FAIL','ERROR_CODE':'ARGUMENT_OR_TARGET_FAILED','FAILURE_STAGE':'PRECHECK','STOP_REQUIRED':True}));return 2
if __name__=='__main__':raise SystemExit(main())
