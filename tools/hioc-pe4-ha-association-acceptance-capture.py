"""Windows-only offline capture of ORIGINAL sanitized stdout; no SSH or inspection.
Separately authorized Attempt 2 only. No retry or evidence reconstruction.
"""
import argparse,hashlib,json,os,re,subprocess,sys
from pathlib import Path
BASE='27377b95658010bf35c2b1fab8009de3d6f24bb6'
SUBJECT='PE-4: harden independent acceptance operator path'
LIMIT=4096
GATES=('DEPLOYMENT','RUNTIME','PRIVATE_STATE','COMPATIBILITY','INVENTORY','CRON_SCHEDULER','PROTECTED_SURFACES_UNCHANGED','CHECKPOINT_COUNTS_AGREE')
ACTIVITY=('ADAPTER_EXECUTED','HA_NETWORK_ATTEMPTED','CREDENTIAL_ACCESSED','PRODUCTION_MUTATED')
STAGES=('SOURCE','DEPLOYMENT_RUNTIME','PRIVATE_STATE','COMPATIBILITY','INVENTORY','FINAL_RECHECK','CAPTURE','NONE')
FIELDS=set(GATES+ACTIVITY+('TARGET','SOURCE_COMMIT','MODE','ORIGINAL_EPHEMERAL_EVIDENCE_REVALIDATION','ORIGINAL_EPHEMERAL_EVIDENCE_LIMITATION','RESULT','FAILURE_STAGE'))
class CaptureFailure(Exception):pass
def require(v):
 if not v:raise CaptureFailure()
def canonical(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False)+'\n').encode('ascii')
def validate_received(raw,commit,return_code):
 require(type(raw) is bytes and 1<=len(raw)<=LIMIT and raw.endswith(b'\n') and b'\r' not in raw and raw.isascii())
 require(type(return_code) is int and return_code in (0,2) and re.fullmatch('[0-9a-f]{40}',commit) is not None)
 def pairs(items):
  v={}
  for k,x in items:require(k not in v);v[k]=x
  return v
 def bad(_):raise CaptureFailure()
 try:value=json.loads(raw.decode('ascii'),object_pairs_hook=pairs,parse_constant=bad)
 except (ValueError,UnicodeError):raise CaptureFailure() from None
 require(type(value) is dict and set(value)==FIELDS)
 require(value['TARGET']=='PI3 NUT&PIHOLE' and value['SOURCE_COMMIT']==commit and value['MODE']=='READ_ONLY')
 require(value['ORIGINAL_EPHEMERAL_EVIDENCE_REVALIDATION']=='UNAVAILABLE' and value['ORIGINAL_EPHEMERAL_EVIDENCE_LIMITATION']=='RECORDED')
 require(all(type(value[k]) is str and value[k] in ('PASS','FAIL','UNKNOWN') for k in GATES))
 require(all(value[k] is False for k in ACTIVITY))
 require(value['RESULT'] in ('PASS','FAIL') and value['FAILURE_STAGE'] in STAGES)
 if value['RESULT']=='PASS':require(return_code==0 and value['FAILURE_STAGE']=='NONE' and all(value[k]=='PASS' for k in GATES))
 else:require(return_code==2 and value['FAILURE_STAGE']!='NONE')
 require(canonical(value)==raw)
 return raw  # Identity of the original bytes, never canonical(value).
def source_binding(root,commit):
 require(re.fullmatch('[0-9a-f]{40}',commit) is not None)
 def git(*a):
  p=subprocess.run(['git','-C',str(root),*a],stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,timeout=15)
  require(p.returncode==0 and len(p.stdout)<1048576);return p.stdout
 require(git('rev-parse','HEAD').strip().decode()==commit and git('rev-parse','origin/main').strip().decode()==commit)
 require(git('branch','--show-current').strip()==b'main' and git('rev-parse','HEAD^').strip().decode()==BASE)
 require(git('show','-s','--format=%s','HEAD').strip().decode()==SUBJECT and not git('status','--porcelain'))
 require(git('show',commit+':tools/'+Path(__file__).name)==Path(__file__).read_bytes().replace(b'\r\n',b'\n'))
 for name in ('MERGE_HEAD','REBASE_HEAD','CHERRY_PICK_HEAD','REVERT_HEAD','sequencer','rebase-merge','rebase-apply','BISECT_LOG','BISECT_START'):
  v=Path(git('rev-parse','--git-path',name).strip().decode());require(not (v if v.is_absolute() else root/v).exists())
 return True
def powershell_environment():
 env=os.environ.copy();env['PSModulePath']=str(Path(os.environ['SystemRoot'])/'System32/WindowsPowerShell/v1.0/Modules');return env
def secure_directory(path,file=False):
 # Validate every existing directory from the governed base down; no ACL changes.
 require(os.name=='nt' and (path.is_file() if file else path.is_dir()) and not path.is_symlink() and not path.is_junction())
 script="""$p=[Console]::In.ReadToEnd();$a=Get-Acl -LiteralPath $p -ErrorAction Stop;
$ids=@('S-1-5-18','S-1-5-32-544',[System.Security.Principal.WindowsIdentity]::GetCurrent().User.Value);
$owner=(New-Object System.Security.Principal.NTAccount($a.Owner)).Translate([System.Security.Principal.SecurityIdentifier]).Value;
$ok=$a.AreAccessRulesProtected -and ($owner -eq $ids[2]);$seen=@();
foreach($r in $a.Access){$id=$r.IdentityReference.Translate([System.Security.Principal.SecurityIdentifier]).Value;
if(($id -notin $ids) -or ($r.AccessControlType -ne 'Allow') -or ($r.IsInherited) -or ($r.FileSystemRights -ne 'FullControl')){$ok=$false};$seen+=$id};
foreach($id in $ids){if($id -notin $seen){$ok=$false}};[Console]::Write([int]$ok)"""
 p=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',script],input=str(path).encode(),stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,timeout=15,env=powershell_environment())
 require(p.returncode==0 and p.stdout==b'1')
def protect_new_directory(path,file=False):
 require(os.name=='nt' and (path.is_file() if file else path.is_dir()) and not path.is_symlink() and not path.is_junction())
 script="""$p=[Console]::In.ReadToEnd();$u=[System.Security.Principal.WindowsIdentity]::GetCurrent().User;
$a=New-Object System.Security.AccessControl.DirectorySecurity;$a.SetOwner($u);$a.SetAccessRuleProtection($true,$false);
foreach($id in @($u.Value,'S-1-5-18','S-1-5-32-544')){
$sid=New-Object System.Security.Principal.SecurityIdentifier($id);
$r=New-Object System.Security.AccessControl.FileSystemAccessRule($sid,'FullControl','ContainerInherit,ObjectInherit','None','Allow');$a.AddAccessRule($r)};
Set-Acl -LiteralPath $p -AclObject $a -ErrorAction Stop"""
 if file:script=script.replace('DirectorySecurity','FileSecurity').replace("'ContainerInherit,ObjectInherit'","'None'")
 p=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',script],input=str(path).encode(),stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=15,env=powershell_environment())
 require(p.returncode==0)
def durable_directory(path):
 import ctypes
 from ctypes import wintypes
 k=ctypes.WinDLL('kernel32',use_last_error=True)
 k.CreateFileW.argtypes=(wintypes.LPCWSTR,wintypes.DWORD,wintypes.DWORD,ctypes.c_void_p,wintypes.DWORD,wintypes.DWORD,wintypes.HANDLE);k.CreateFileW.restype=wintypes.HANDLE
 k.FlushFileBuffers.argtypes=(wintypes.HANDLE,);k.FlushFileBuffers.restype=wintypes.BOOL
 k.CloseHandle.argtypes=(wintypes.HANDLE,)
 h=k.CreateFileW(str(path),0x40000000,7,None,3,0x02000000,None)
 require(h not in (None,ctypes.c_void_p(-1).value))
 try:require(bool(k.FlushFileBuffers(h)))
 finally:k.CloseHandle(h)
def exclusive_file(path,raw):
 with path.open('xb') as f:
  protect_new_directory(path,file=True);secure_directory(path,file=True)
  f.write(raw);f.flush();os.fsync(f.fileno())
 secure_directory(path,file=True);require(path.read_bytes()==raw)
def publish_original(raw,commit,return_code,directory,security=secure_directory,sync=durable_directory,write=exclusive_file,protect=protect_new_directory):
 original=validate_received(raw,commit,return_code)
 require(re.fullmatch(r'[0-9]{8}T[0-9]{6}-[0-9a-f]{12}',directory.name) is not None)
 require(directory.parent.name==commit and commit!=BASE and not directory.exists())
 security(directory.parent)
 directory.mkdir()  # New exclusive run only; never create parents or reuse failed run.
 protect(directory)  # ACL only on the newly created workstation run, never historical paths.
 security(directory)
 write(directory/'validation.json',original)
 security(directory);sync(directory)
 manifest=canonical({'schema_version':'1.0','source_commit':commit,'validation_sha256':hashlib.sha256(original).hexdigest(),'validation_bytes':len(original)})
 require(len(manifest)<=LIMIT)
 write(directory/'manifest.json',manifest)  # Manifest LAST, never overwrite.
 security(directory);sync(directory);sync(directory.parent)
 require((directory/'validation.json').read_bytes()==original and (directory/'manifest.json').read_bytes()==manifest)
 return manifest
def main(argv=None):
 try:
  require(os.name=='nt' and sys.version_info[:2]>=(3,12))
  parser=argparse.ArgumentParser(add_help=False,exit_on_error=False)
  parser.add_argument('--source-commit',required=True);parser.add_argument('--remote-return-code',required=True,type=int);parser.add_argument('--new-run-id',required=True)
  args=parser.parse_args(argv)
  # Original raw stdout must be supplied on binary stdin by the separately reviewed capture process.
  raw=sys.stdin.buffer.read(LIMIT+1);validate_received(raw,args.source_commit,args.remote_return_code)
  root=Path(__file__).resolve().parents[1];source_binding(root,args.source_commit)
  local=Path(os.environ['LOCALAPPDATA']);require(local==Path.home()/'AppData/Local')
  require(re.fullmatch(r'[0-9]{8}T[0-9]{6}-[0-9a-f]{12}',args.new_run_id) is not None)
  base=local/'HIOC/evidence/pe4/independent-acceptance'
  for path in [local,local/'HIOC',local/'HIOC/evidence',local/'HIOC/evidence/pe4']:
   require(path.is_dir() and not path.is_symlink() and not path.is_junction())
  security_chain=[base,base/args.source_commit]
  for path in security_chain:secure_directory(path)
  directory=base/args.source_commit/args.new_run_id
  publish_original(raw,args.source_commit,args.remote_return_code,directory)
  print('CAPTURE=PASS');return 0 if args.remote_return_code==0 else 2
 except BaseException:
  print('CAPTURE=FAIL\nERROR_CODE=CAPTURE_VALIDATION_OR_DURABILITY_FAILED\nSTOP_REQUIRED=TRUE');return 3
if __name__=='__main__':raise SystemExit(main())
