"""Windows byte-preserving one-shot operator transport; no acceptance logic."""
import importlib.util,os,re,selectors,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TARGET='jazofv1@192.168.100.252'
WRAPPER='/home/jazofv1/hioc-release-source/tools/hioc-pe4-ha-association-independent-acceptance.py'
TIMEOUT=180
LIMIT=4096
def helper():
 spec=importlib.util.spec_from_file_location('governed_capture',ROOT/'tools/hioc-pe4-ha-association-acceptance-capture.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def transport(command):
 # Binary stdout, stderr discarded, bounded deadline; never retry.
 p=subprocess.Popen(command,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
 import threading,queue
 chunks=queue.Queue(maxsize=2)
 def read():
  try:
   while True:
    raw=p.stdout.read1(4097);chunks.put(raw)
    if not raw:break
  except BaseException:chunks.put(None)
 worker=threading.Thread(target=read,daemon=True);worker.start();raw=bytearray();deadline=time.monotonic()+TIMEOUT
 try:
  while True:
   chunk=chunks.get(timeout=max(.01,deadline-time.monotonic()))
   if chunk is None:raise ValueError('transport')
   if not chunk:break
   raw.extend(chunk)
   if len(raw)>LIMIT or time.monotonic()>deadline:raise ValueError('transport')
  rc=p.wait(timeout=max(.01,deadline-time.monotonic()));return bytes(raw),rc
 except BaseException:
  p.kill();p.wait(timeout=5);raise
 finally:p.stdout.close()
def prepare_parent(base,commit,m):
 m.require(re.fullmatch('[0-9a-f]{40}',commit) is not None)
 m.secure_directory(base);parent=base/commit
 if not parent.exists():
  parent.mkdir();m.protect_new_directory(parent);m.secure_directory(parent);m.durable_directory(parent);m.durable_directory(base)
 else:m.secure_directory(parent)
 return parent
def execute(commit,run_id,receive,publish,validate):
 raw,rc=receive();original=validate(raw,commit,rc);publish(original,commit,rc,run_id)
 return 0 if rc==0 else 2  # Valid FAIL evidence is not acceptance PASS.
def main(argv=None):
 import argparse,json,hashlib
 try:
  m=helper();m.require(os.name=='nt' and sys.version_info[:2]>=(3,12))
  parser=argparse.ArgumentParser(add_help=False,exit_on_error=False);parser.add_argument('--source-commit',required=True);parser.add_argument('--new-run-id',required=True);args=parser.parse_args(argv)
  m.require(re.fullmatch(r'[0-9]{8}T[0-9]{6}-[0-9a-f]{12}',args.new_run_id) is not None);m.source_binding(ROOT,args.source_commit)
  record=json.loads((ROOT/'governance/pe4/pe4-ha-association-independent-production-acceptance-operator-path.json').read_bytes())
  for item in record['implementation_bindings']+record['read_only_bindings']:
   raw=(ROOT/item['path']).read_bytes().replace(b'\r\n',b'\n');m.require(hashlib.sha256(raw).hexdigest()==item['sha256'])
  local=Path(os.environ['LOCALAPPDATA']);m.require(local==Path.home()/'AppData/Local')
  base=local/'HIOC/evidence/pe4/independent-acceptance'
  for path in [local,local/'HIOC',local/'HIOC/evidence',local/'HIOC/evidence/pe4',base]:m.require(path.is_dir() and not path.is_symlink() and not path.is_junction())
  parent=prepare_parent(base,args.source_commit,m);m.require(not (parent/args.new_run_id).exists())
  ssh=str(Path(os.environ['SystemRoot'])/'System32/OpenSSH/ssh.exe')
  m.require(hashlib.sha256(Path(ssh).read_bytes()).hexdigest()=='786ff14be7cd652b2b9770a57e9b1aa5e03a052ce3a3d641fb4760c0ff3fde05')
  profile=Path.home();key=profile/'.ssh/id_ed25519';known=profile/'.ssh/known_hosts'
  for path in [profile/'.ssh',key,known]:m.require(path.exists() and not path.is_symlink() and not path.is_junction())
  # Strict existing host key, no password prompt, no agent forwarding; fixed target only.
  remote='env -i PATH=/usr/sbin:/usr/bin:/bin HOME=/home/jazofv1 LANG=C.UTF-8 LC_ALL=C.UTF-8 /usr/bin/python3 -I -S -B '+WRAPPER+' --source-commit '+args.source_commit
  command=[ssh,'-F','none','-T','-p','22','-i',str(key),'-o','UserKnownHostsFile='+str(known),'-o','GlobalKnownHostsFile=none','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o','ForwardAgent=no','-o','IdentityAgent=none','-o','IdentitiesOnly=yes','-o','PreferredAuthentications=publickey','-o','PasswordAuthentication=no','-o','KbdInteractiveAuthentication=no','-o','ProxyCommand=none','-o','ProxyJump=none','-o','CanonicalizeHostname=no','-o','ConnectTimeout=15',TARGET,remote]
  rc=execute(args.source_commit,args.new_run_id,lambda:transport(command),lambda raw,c,r,n:m.publish_original(raw,c,r,parent/n),m.validate_received)
  print('OPERATOR_RESULT='+('PASS' if rc==0 else 'FAIL')+'\nSTOP_REQUIRED=TRUE');return rc
 except BaseException:
  print('OPERATOR_RESULT=FAIL\nERROR_CODE=TRANSPORT_OR_CAPTURE_FAILED\nSTOP_REQUIRED=TRUE');return 3
if __name__=='__main__':raise SystemExit(main())
