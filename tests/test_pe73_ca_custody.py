"""Synthetic custody qualification; never production execution."""
import ast,base64,contextlib,copy,hashlib,importlib.util,json,unittest
from pathlib import Path,PurePosixPath
from unittest.mock import Mock,patch
import test_pe73_ha_provision as old
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('custody_tests',R/'tools/pe73_ca_custody.py')
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
q=old.q;p=old.p
class CustodyTests(unittest.TestCase):
 def setUp(self):
  self.plan=old.plan();self.password=b'synthetic offline CA passphrase'
  self.files=old.Files(str(c.VAULT));c.initialize_ca(q,self.files,self.plan,self.password)
  self.runtime=old.Files(self.plan['backend_parent'],c.runtime_material(q,self.plan))
 def public(self,role='server',plan=None,csr=None):
  plan=self.plan if plan is None else plan
  if csr is None:
   if role=='server':csr=self.runtime.read(self.runtime.parent+'/server.csr')
   else:
    self.client_key,csr=q.create_request(plan);self.runtime.values[self.runtime.parent+'/client.csr']=csr
  return c.sign_request(q,self.files,plan,self.password,role,csr)
 def test_vault_contains_only_CA_and_binding(self):
  self.assertEqual({Path(x).name for x in self.files.values},{'ca.pem','ca-offline.key','plan.sha256'})
 def test_runtime_key_HMAC_not_in_vault(self):
  self.assertEqual({Path(x).name for x in self.runtime.values},{'plan.json','server.key','server.csr','assertion.key'})
  self.assertEqual(len(self.runtime.read(self.runtime.parent+'/assertion.key')),32)
 def test_CA_encrypted_password_not_persisted(self):
  _,_,s,*_=q.crypto()
  with self.assertRaises(TypeError):s.load_pem_private_key(self.files.read(self.files.parent+'/ca-offline.key'),None)
  self.assertTrue(all(self.password not in raw for raw in self.files.values.values()))
 def test_CA_reinitialization_refused_before_crypto(self):
  with patch.object(q,'generate_ca') as generate:
   with self.assertRaisesRegex(c.Blocked,'EXISTING'):c.initialize_ca(q,self.files,self.plan,self.password)
   generate.assert_not_called()
 def test_runtime_parent_not_CA_vault(self):
  with self.assertRaisesRegex(c.Blocked,'ROOT_VAULT'):c.initialize_ca(q,self.runtime,self.plan,self.password)
 def test_public_response_has_no_private_material_or_ACL(self):
  value=self.public();raw=c.canonical(value)
  self.assertEqual(set(value),{'schema','role','plan_sha256','csr_sha256','ca','chain'})
  self.assertNotIn(b'PRIVATE KEY',raw);self.assertNotIn(b'synthetic_operator',raw);self.assertNotIn(self.password,raw)
 def test_server_certificate_matches_runtime_key(self):
  value=self.public();c.accept_public(q,p,self.runtime,self.plan,'server',c.canonical(value))
  p.validate_material(self.runtime.read(self.runtime.parent+'/server-chain.pem'),self.runtime.read(self.runtime.parent+'/server.key'),self.runtime.read(self.runtime.parent+'/ca.pem'),'backend',self.plan['backend_address'])
 def test_client_key_stays_on_client(self):
  value=self.public('client');c.accept_public(q,p,self.runtime,self.plan,'client',c.canonical(value))
  p.validate_material(base64.b64decode(value['chain']),self.client_key,base64.b64decode(value['ca']),'ha',self.plan['backend_address'])
  self.assertNotIn(self.client_key,self.files.values.values());self.assertNotIn(self.client_key,self.runtime.values.values())
 def test_same_accepted_server_extensions(self):
  value=self.public();original,_=q.issue(self.plan,self.files.read(self.files.parent+'/ca.pem'),self.files.read(self.files.parent+'/ca-offline.key'),self.password)
  actual=p.certificates(base64.b64decode(value['chain']))[0];expected=p.certificates(original)[0]
  self.assertEqual(actual.subject,expected.subject)
  for ext in actual.extensions:
   if ext.oid.dotted_string=='2.5.29.14':continue
   other=expected.extensions.get_extension_for_oid(ext.oid);self.assertEqual((ext.critical,ext.value),(other.critical,other.value))
 def test_client_reuses_original_issuance(self):
  with patch.object(q,'issue',wraps=q.issue) as issue:self.public('client')
  issue.assert_called_once();self.assertIn('csr_raw',issue.call_args.kwargs)
 def test_signer_does_not_generate_server_key(self):
  with patch.object(q,'issue',side_effect=AssertionError('server key must be local')):self.public()
 def test_plan_drift_refused(self):
  other=copy.deepcopy(self.plan);other['server_name']='Changed'
  with self.assertRaisesRegex(c.Blocked,'PLAN_DRIFT'):self.public(plan=other)
 def test_wrong_password_no_issuance_record(self):
  self.password=b'wrong'
  with self.assertRaises(ValueError):self.public()
  self.assertNotIn(self.files.parent+'/server-issuance.json',self.files.values)
 def test_wrong_server_subject(self):
  other=copy.deepcopy(self.plan);other['server_name']='Other';_,csr=c.request(q,other,'server')
  with self.assertRaisesRegex(c.Blocked,'SUBJECT'):self.public(csr=csr)
 def test_wrong_server_SAN(self):
  x,h,serialization,ec,_,oid=q.crypto();key=ec.generate_private_key(ec.SECP256R1())
  import ipaddress
  csr=x.CertificateSigningRequestBuilder().subject_name(x.Name([x.NameAttribute(oid.COMMON_NAME,self.plan['server_name'])])).add_extension(x.SubjectAlternativeName([x.IPAddress(ipaddress.ip_address('192.168.100.253'))]),False).sign(key,h.SHA256()).public_bytes(serialization.Encoding.PEM)
  with self.assertRaisesRegex(c.Blocked,'SAN'):self.public(csr=csr)
 def test_client_CSR_not_server(self):
  _,csr=q.create_request(self.plan)
  with self.assertRaisesRegex(c.Blocked,'SUBJECT'):self.public(csr=csr)
 def test_server_CSR_not_client(self):
  with self.assertRaisesRegex(q.Blocked,'SUBJECT'):self.public('client',csr=self.runtime.read(self.runtime.parent+'/server.csr'))
 def test_large_CSR_refused(self):
  with self.assertRaisesRegex(c.Blocked,'CSR_SIZE'):self.public(csr=b'x'*16385)
 def test_invalid_role(self):
  with self.assertRaisesRegex(c.Blocked,'CSR_ROLE'):self.public('other',csr=b'x')
 def test_duplicate_issuance_not_retried(self):
  self.public()
  with patch.object(c,'issue_server_request') as sign:
   with self.assertRaisesRegex(c.Blocked,'EXISTING'):self.public()
   sign.assert_not_called()
 def test_partial_CA_not_overwritten(self):
  files=old.Files(str(c.VAULT),{'ca.pem':b'partial'})
  with self.assertRaisesRegex(c.Blocked,'EXISTING'):c.initialize_ca(q,files,self.plan,self.password)
  self.assertEqual(len(files.values),1)
 def test_interrupted_CA_retained_refuses_retry(self):
  files=old.Files(str(c.VAULT));files.fail=files.parent+'/ca.pem'
  with self.assertRaises(OSError):c.initialize_ca(q,files,self.plan,self.password)
  files.fail=None
  with self.assertRaisesRegex(c.Blocked,'EXISTING'):c.initialize_ca(q,files,self.plan,self.password)
 def test_interrupted_issuance_not_automatically_retried(self):
  self.files.fail=self.files.parent+'/server-issuance.json'
  with patch.object(c,'issue_server_request',wraps=c.issue_server_request) as sign:
   with self.assertRaises(OSError):self.public()
   self.assertEqual(sign.call_count,1)
 def test_wrong_public_plan_binding(self):
  value=self.public();value['plan_sha256']='0'*64
  with self.assertRaisesRegex(c.Blocked,'BINDING'):c.accept_public(q,p,self.runtime,self.plan,'server',c.canonical(value))
 def test_wrong_public_CSR_binding(self):
  value=self.public();value['csr_sha256']='0'*64
  with self.assertRaisesRegex(c.Blocked,'BINDING'):c.accept_public(q,p,self.runtime,self.plan,'server',c.canonical(value))
 def test_secret_field_refused(self):
  value=self.public();value['ca-offline.key']='no'
  with self.assertRaisesRegex(c.Blocked,'SHAPE'):c.accept_public(q,p,self.runtime,self.plan,'server',c.canonical(value))
 def test_wrong_runtime_key(self):
  value=self.public();key,_=c.request(q,self.plan,'server');self.runtime.values[self.runtime.parent+'/server.key']=key
  with self.assertRaisesRegex(p.Stop,'KEY_MISMATCH'):c.accept_public(q,p,self.runtime,self.plan,'server',c.canonical(value))
 def test_conflicting_CA_export(self):
  value=self.public();self.runtime.values[self.runtime.parent+'/ca.pem']=b'conflict'
  with self.assertRaisesRegex(c.Blocked,'CA_EXPORT'):c.accept_public(q,p,self.runtime,self.plan,'server',c.canonical(value))
 def test_import_no_overwrite(self):
  value=self.public();raw=c.canonical(value);c.accept_public(q,p,self.runtime,self.plan,'server',raw)
  with self.assertRaisesRegex(c.Blocked,'EXISTING'):c.accept_public(q,p,self.runtime,self.plan,'server',raw)
 def test_complete_flow_preserves_disabled_packet(self):
  for role in ('server','client'):c.accept_public(q,p,self.runtime,self.plan,role,c.canonical(self.public(role)))
  @contextlib.contextmanager
  def context(trust):
   with trust.material() as material:yield material
  with patch.object(p,'native_packet',side_effect=lambda files,path:lambda:json.loads(files.read(path))),patch.object(p.TrustSide,'context',context):
   result=c.finish_runtime(q,p,self.runtime,self.plan);self.assertFalse(result['activation'])
   self.assertEqual(q.export_bundle(self.runtime,p),self.runtime.read(self.runtime.parent+'/ha-transfer.json'))
  packet=json.loads(self.runtime.read(self.runtime.parent+'/packet.json'))
  self.assertFalse(packet['ha']['hioc_operator']['operator']['enabled']);self.assertFalse(packet['backend']['enabled'])
 def test_completion_requires_both_roles(self):
  c.accept_public(q,p,self.runtime,self.plan,'server',c.canonical(self.public()))
  with self.assertRaises(FileNotFoundError):c.finish_runtime(q,p,self.runtime,self.plan)
  self.assertNotIn(self.runtime.parent+'/packet.json',self.runtime.values)
class BoundaryTests(unittest.TestCase):
 def test_exact_profile_identity(self):
  raw=(R/'tools/pe73_pi3_provision_environment.py').read_bytes();c.load_profile(raw)
  with self.assertRaisesRegex(c.Blocked,'IDENTITY'):c.load_profile(raw+b' ')
 def test_same_engine_cp311_offline_pins(self):
  profile=c.load_profile((R/'tools/pe73_pi3_provision_environment.py').read_bytes());engine=profile.load_engine((R/'tools/pe73_provision_environment.py').read_bytes())
  with patch.object(profile,'load_engine',return_value=engine):actual=c.engine_for(profile)
  self.assertEqual(actual.ROOT,c.ROOT);self.assertEqual(actual.WHEELS,profile.WHEELS)
  for flag in ('--no-index','--require-hashes','--only-binary=:all:','--no-user'):self.assertIn(flag,actual.pip_command(c.ROOT))
 def test_custody_outside_runtime_home(self):
  for path in (c.ROOT,c.VAULT):self.assertEqual(path.parent.as_posix(),'/root')
 def test_root_gate(self):
  with patch.object(c,'target',side_effect=c.Blocked('ROOT_MANUAL_CUSTODY_REQUIRED')):
   with self.assertRaisesRegex(c.Blocked,'ROOT_MANUAL'):c.main(['initialize-ca','--runtime-parent','/home/jazofv1/hioc/test'])
 def test_old_unsafe_actions_not_exposed(self):
  for action in ('backend-init','backend-issue','activate','recover','serve'):
   with patch('sys.stderr',__import__('io').StringIO()),self.assertRaises(SystemExit):c.main([action])
 def test_existing_state_refused_before_download(self):
  with patch.object(c,'target'),patch.object(c.os.path,'lexists',return_value=True),patch.object(c,'load_profile') as load:
   with self.assertRaisesRegex(c.Blocked,'EXISTING'):c.prepare()
   load.assert_not_called()
 def test_setup_failure_no_vault(self):
  engine=Mock();engine.prepare.side_effect=OSError('private')
  with patch.object(c,'target'),patch.object(c.os.path,'lexists',return_value=False),patch.object(c,'load_profile'),patch.object(c,'engine_for',return_value=engine),patch.object(c,'create_vault') as create:
   with self.assertRaises(OSError):c.prepare()
   create.assert_not_called()
 def test_prepare_no_CA_or_HMAC(self):
  engine=Mock();engine.prepare.return_value={'native_smoke':'PASS'};engine.invoke.return_value=b''
  with patch.object(c,'target'),patch.object(c.os.path,'lexists',return_value=False),patch.object(c,'load_profile'),patch.object(c,'engine_for',return_value=engine),patch.object(c,'helper'),patch.object(c,'create_vault'),patch.object(c,'initialize_ca') as initialize,patch.object(c,'runtime_material') as runtime:
   receipt=c.prepare();self.assertFalse(receipt['CA_created']);self.assertFalse(receipt['HMAC_created']);initialize.assert_not_called();runtime.assert_not_called()
 def test_root_CLI_reads_only_public_plan_CSR(self):
  tree=ast.parse((R/'tools/pe73_ca_custody.py').read_bytes());text=ast.unparse(next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main'))
  for secret in ('assertion.key','server.key','client.key'):self.assertNotIn(secret,text)
 def test_no_service_permission_repair_or_cleanup(self):
  tree=ast.parse((R/'tools/pe73_ca_custody.py').read_bytes());calls={n.func.attr for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute)}
  self.assertFalse(calls & {'chmod','chown','fchmod','fchown','unlink','rmdir','rmtree','serve_forever','system','Popen'})
 def test_root_interpreter_excludes_user_venv(self):
  source=(R/'tools/pe73_ca_custody.py').read_text();self.assertIn('PRIVILEGED_INTERPRETER_ANCESTRY_UNSAFE',source)
  self.assertIn("allowed=(Path('/usr/bin/python3.11'),ROOT/'venv/bin/python3')",source)
 def test_accepted_sources_unchanged(self):
  import subprocess
  # Root signer deliberately retains the historical sealed crypto toolkit;
  # population ACL deployment is separately gated, never an in-place cache edit.
  historical=subprocess.check_output(['git','--no-replace-objects','show','b5a020982484e35126daa70b256860a23af8e88f:tools/pe73_ha_provision.py'],cwd=R)
  self.assertEqual(hashlib.sha256(historical).hexdigest(),c.HELPER_SHA)
  for path,h in {'tools/pe73_provision_environment.py':'0e5d41b05729907ad1e629c8d77bf57a25890f600f7e2fcf29071c106fa0b3d7','tools/pe73_pi3_provision_environment.py':c.PROFILE_SOURCE['sha256']}.items():self.assertEqual(hashlib.sha256((R/path).read_bytes()).hexdigest(),h)

class NativeCustodyFilesystemTests(unittest.TestCase):
 def setUp(self):
  import tempfile,stat
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
  vault_patch=patch.object(c,'VAULT',PurePosixPath('/root/.hioc-pe73-ca-custody'));vault_patch.start();self.addCleanup(vault_patch.stop)
  self.ops=old.prior.old.RootOps(self.root)
  (self.root/'root').mkdir();self.private=self.root/str(c.VAULT).lstrip('/');self.private.mkdir()
  for path in (self.root/'root',self.private):
   info=path.stat();self.ops.attrs[(info.st_dev,info.st_ino)]=(0,0,0o700)
  self.binding=Mock();self.binding.PrivateFiles.side_effect=lambda parent,owner:p.PrivateFiles(parent,owner,_ops=self.ops)
  self.q=Mock();self.q.native.return_value=self.binding
 def tearDown(self):self.assertFalse(self.ops.fds)
 def meta(self,path,uid=0,gid=0,mode=0o700):
  info=path.stat();self.ops.attrs[(info.st_dev,info.st_ino)]=(uid,gid,mode)
 def test_root_vault_descriptor_security(self):
  files=c.vault_files(self.q);files.provision(str(c.VAULT)+'/ca-offline.key',b'encrypted synthetic bytes')
  self.assertEqual(files.read(str(c.VAULT)+'/ca-offline.key'),b'encrypted synthetic bytes')
 def test_same_runtime_UID_vault_refused(self):
  self.meta(self.private,1000,1000)
  with self.assertRaisesRegex(p.Stop,'UNSAFE'):c.vault_files(self.q)
 def test_world_readable_vault_refused(self):
  self.meta(self.private,mode=0o755)
  with self.assertRaisesRegex(p.Stop,'PARENT_SECURITY'):c.vault_files(self.q)
 def test_extended_ACL_refused(self):
  self.ops.acl[str(c.VAULT)]='present'
  with self.assertRaisesRegex(p.Stop,'ACL_PRESENT'):c.vault_files(self.q)
 def test_unknown_ACL_refused(self):
  self.ops.acl[str(c.VAULT)]='unknown'
  with self.assertRaisesRegex(p.Stop,'ACL_UNKNOWN'):c.vault_files(self.q)
 def test_CA_file_wrong_owner_refused(self):
  files=c.vault_files(self.q);path=self.private/'ca-offline.key';path.write_bytes(b'fixture');self.meta(path,1000,1000,0o600)
  with self.assertRaisesRegex(p.Stop,'FILE_SECURITY'):files.read(str(c.VAULT)+'/ca-offline.key')
 def test_hardlinked_CA_refused(self):
  import os
  files=c.vault_files(self.q);path=self.private/'ca-offline.key';path.write_bytes(b'fixture');os.link(path,self.private/'alias')
  with self.assertRaisesRegex(p.Stop,'FILE_SECURITY'):files.read(str(c.VAULT)+'/ca-offline.key')
 def test_vault_creation_exclusive(self):
  original=c.os.mkdir
  def mkdir(name,mode,dir_fd):return original(self.ops.actual(name,dir_fd)[1],mode)
  with patch.object(c.os,'mkdir',side_effect=mkdir),patch.object(c.os,'fsync',side_effect=self.ops.fsync):
   with self.assertRaises(FileExistsError):c.create_vault(self.q)

class NativeIdentityTests(unittest.TestCase):
 def test_wrong_host_refused_before_privilege_or_files(self):
  with patch.object(c.sys,'platform','linux'),patch.object(c.platform,'node',return_value='other'):
   with self.assertRaisesRegex(c.Blocked,'HOST_OR_ABI'):c.target()
 def test_UID1000_cannot_be_signer(self):
  with contextlib.ExitStack() as stack:
   stack.enter_context(patch.object(c.sys,'platform','linux'));stack.enter_context(patch.object(c.sys,'version_info',(3,11,2)))
   for name,value in [('node','nutandpihole'),('machine','aarch64'),('python_implementation','CPython')]:stack.enter_context(patch.object(c.platform,name,return_value=value))
   for name in ('getuid','geteuid','getgid','getegid'):stack.enter_context(patch.object(c.os,name,return_value=1000,create=True))
   with self.assertRaisesRegex(c.Blocked,'ROOT_MANUAL'):c.target()
 def test_no_network_fetch_during_manual_signing_engine_load(self):
  profile=c.load_profile((R/'tools/pe73_pi3_provision_environment.py').read_bytes())
  raw=(R/'tools/pe73_provision_environment.py').read_bytes()
  with patch.object(c.Path,'read_bytes',return_value=raw),patch.object(c.urllib.request,'build_opener',side_effect=AssertionError('NO_NETWORK')):
   engine=c.engine_for(profile,offline=True)
  self.assertEqual(engine.ROOT,c.ROOT)
 def test_root_seal_drift_refused(self):
  import tempfile,stat,sys,types
  with tempfile.TemporaryDirectory() as temporary:
   root=Path(temporary);(root/'ready.json').write_text('{}')
   engine=Mock();engine.fingerprint.return_value={};engine.VERSIONS={}
   real_python=Path(sys.executable)
   info=types.SimpleNamespace(st_mode=stat.S_IFREG|0o600,st_uid=0,st_gid=0,st_nlink=1)
   with patch.object(c,'ROOT',root),patch.object(c.Path,'lstat',return_value=info),patch.object(c.Path,'resolve',return_value=real_python):
    with self.assertRaisesRegex(c.Blocked,'DRIFT'):c.verify_ready(engine)
 def test_root_ready_owned_by_runtime_refused(self):
  import stat,types
  info=types.SimpleNamespace(st_mode=stat.S_IFREG|0o600,st_uid=1000,st_gid=1000,st_nlink=1)
  with patch.object(c.Path,'lstat',return_value=info):
   with self.assertRaisesRegex(c.Blocked,'READY_SECURITY'):c.verify_ready(Mock())
