"""PI3 profile synthetic/local API tests; never a production qualification claim."""
import ast,contextlib,errno,hashlib,importlib.util,json,os,stat,sys,tempfile,types,unittest
from pathlib import Path,PurePosixPath
from unittest.mock import Mock,patch
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('pi3_environment_test',ROOT/'tools/pe73_pi3_provision_environment.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
ENGINE=(ROOT/'tools/pe73_provision_environment.py').read_bytes()

class ProfileTests(unittest.TestCase):
    def test_exact_accepted_engine_only(self):
        self.assertEqual(p.load_engine(ENGINE).ROOT,Path('/root/.hioc-pe73-provision-environment'))
        with self.assertRaisesRegex(p.Blocked,'IDENTITY'):p.load_engine(ENGINE+b' ')
    def test_PI5_source_and_loaded_profile_unchanged(self):
        original=p.load_engine(ENGINE);other=p.load_engine(ENGINE);p.profile(other)
        self.assertEqual(original.ROOT,Path('/root/.hioc-pe73-provision-environment'))
        self.assertEqual(other.ROOT,p.ROOT)
        self.assertEqual(hashlib.sha256((ROOT/'tools/pe73_provision_environment.py').read_bytes()).hexdigest(),p.ENGINE_SOURCE['sha256'])
    def test_same_offline_installer_and_versions(self):
        engine=p.load_engine(ENGINE);methods={name:getattr(engine,name) for name in ('prepare','fetch','validate_wheel','pip_command','lock_text','invoke','clean_env')}
        p.profile(engine)
        self.assertTrue(all(getattr(engine,k)is v for k,v in methods.items()))
        self.assertEqual(engine.VERSIONS,{'cryptography':'50.0.2','cffi':'2.0.0','pycparser':'2.23'})
        args=engine.pip_command(p.ROOT)
        for x in ('--require-hashes','--no-index','--no-deps','--only-binary=:all:','--no-user'):self.assertIn(x,args)
        self.assertEqual(args[args.index('--prefix')+1],str(p.ROOT/'venv'))
    def test_cp311_CFFI_only_and_immutable_hashes(self):
        cffi=[x for x in p.WHEELS if x['name'].startswith('cffi-')]
        self.assertEqual(len(cffi),2)
        self.assertTrue(all('-cp311-cp311-' in x['name'] and len(x['sha256'])==64 for x in cffi))
        self.assertEqual(len(p.WHEELS),6)
    def test_cache_outside_runtime_and_release_source(self):
        self.assertEqual(p.ROOT.as_posix(),'/home/jazofv1/.hioc-pe73-provision-environment')
        self.assertFalse(p.ROOT.is_relative_to('/home/jazofv1/hioc'))
        self.assertFalse(p.ROOT.is_relative_to('/home/jazofv1/hioc-release-source'))
    def test_only_environment_setup_command(self):
        with patch.object(p,'prepare') as prepare:
            for action in ('backend-init','backend-issue','ha-request','activate'):
                with contextlib.redirect_stderr(__import__('io').StringIO()),self.assertRaises(SystemExit):p.main([action])
            prepare.assert_not_called()
    def test_smoke_contains_no_production_credential_calls(self):
        tree=ast.parse(p.EXTRA_SMOKE)
        attrs={x.func.attr for x in ast.walk(tree) if isinstance(x,ast.Call) and isinstance(x.func,ast.Attribute)}
        self.assertFalse(attrs & {'generate_ca','issue','backend_material','provision','stage','write_bytes','write_text','install'})
        self.assertIn('crypto',attrs);self.assertIn('native',attrs)
        self.assertIn('ca=False',p.EXTRA_SMOKE)
    def test_dependency_subprocess_receives_no_host_credentials(self):
        engine=p.profile(p.load_engine(ENGINE))
        with patch.dict(os.environ,{'SUPERVISOR_TOKEN':'PRIVATE_TOKEN','SSH_AUTH_SOCK':'PRIVATE_SOCKET','PYTHONPATH':'PRIVATE_PATH'}):env=engine.clean_env(p.ROOT)
        self.assertNotIn('PRIVATE',json.dumps(env))

class TargetTests(unittest.TestCase):
    def model(self,uid=1000,gid=1000,host='nutandpihole',version=(3,11,2),account=None):
        s=contextlib.ExitStack();self.addCleanup(s.close)
        s.enter_context(patch.object(p.sys,'platform','linux'));s.enter_context(patch.object(p.sys,'version_info',version))
        for name,value in [('getuid',uid),('geteuid',uid),('getgid',gid),('getegid',gid)]:s.enter_context(patch.object(p.os,name,return_value=value,create=True))
        s.enter_context(patch.object(p.platform,'python_implementation',return_value='CPython'))
        s.enter_context(patch.object(p.platform,'machine',return_value='aarch64'));s.enter_context(patch.object(p.platform,'node',return_value=host))
        account=account or types.SimpleNamespace(pw_name='jazofv1',pw_gid=1000,pw_dir='/home/jazofv1')
        s.enter_context(patch.dict(sys.modules,{'pwd':types.SimpleNamespace(getpwuid=lambda uid:account)}))
    def test_actual_role_profile_allowed(self):self.model();p.target()
    def test_root_rejected(self):
        self.model(uid=0,gid=0)
        with self.assertRaisesRegex(p.Blocked,'NO_ROOT'):p.target()
    def test_wrong_group_rejected(self):
        self.model(gid=0)
        with self.assertRaises(p.Blocked):p.target()
    def test_wrong_user_rejected(self):
        self.model(uid=1001)
        with self.assertRaises(p.Blocked):p.target()
    def test_wrong_host_rejected(self):
        self.model(host='PI5')
        with self.assertRaisesRegex(p.Blocked,'HOST'):p.target()
    def test_wrong_python_rejected(self):
        self.model(version=(3,14,8))
        with self.assertRaisesRegex(p.Blocked,'ABI'):p.target()
    def test_wrong_home_rejected(self):
        self.model(account=types.SimpleNamespace(pw_name='jazofv1',pw_gid=1000,pw_dir='/tmp'))
        with self.assertRaisesRegex(p.Blocked,'HOME'):p.target()

class AncestryTests(unittest.TestCase):
    def model(self,unsafe=None,acl=None,drift=False):
        stack=contextlib.ExitStack();self.addCleanup(stack.close)
        infos={i:types.SimpleNamespace(st_dev=1,st_ino=i,st_mode=stat.S_IFDIR|0o755,st_uid=0 if i<3 else 1000,st_gid=42 if i<3 else 1000) for i in (1,2,3)}
        if unsafe:infos[unsafe].st_mode=stat.S_IFDIR|0o777
        opening=Mock(side_effect=[1,2,3]);close=Mock()
        fake=types.SimpleNamespace(**{flag:getattr(os,flag,0) for flag in ('O_RDONLY','O_DIRECTORY','O_NOFOLLOW','O_CLOEXEC')},
            open=opening,close=close,fstat=lambda fd:infos[fd],
            stat=lambda name,dir_fd,follow_symlinks:types.SimpleNamespace(st_dev=1,st_ino=dir_fd+1+(10 if drift else 0)),
            getxattr=Mock(side_effect=OSError(errno.ENODATA,'fixture') if acl is None else acl))
        stack.enter_context(patch.object(p,'os',fake))
        return opening,close
    def test_root_owned_ancestors_and_uid1000_home(self):
        opening,close=self.model();p.owned_directory(PurePosixPath('/home/jazofv1'))
        self.assertEqual(opening.call_count,3);self.assertEqual(close.call_count,3)
    def test_world_writable_ancestor_refused(self):
        opening,close=self.model(unsafe=2)
        with self.assertRaisesRegex(p.Blocked,'ANCESTRY'):p.owned_directory(PurePosixPath('/home/jazofv1'))
        self.assertEqual(close.call_count,2)
    def test_acl_present_refused(self):
        opening,close=self.model(acl=lambda *a:b'ACL')
        with self.assertRaisesRegex(p.Blocked,'ACL_PRESENT'):p.owned_directory(PurePosixPath('/home/jazofv1'))
        self.assertEqual(close.call_count,1)
    def test_acl_unknown_refused(self):
        self.model(acl=OSError(errno.EACCES,'fixture'))
        with self.assertRaisesRegex(p.Blocked,'ACL_UNKNOWN'):p.owned_directory(PurePosixPath('/home/jazofv1'))
    def test_named_identity_drift_refused(self):
        opening,close=self.model(drift=True)
        with self.assertRaisesRegex(p.Blocked,'DRIFT'):p.owned_directory(PurePosixPath('/home/jazofv1'))
        self.assertEqual(close.call_count,3)

class FingerprintTests(unittest.TestCase):
    def model(self,uid=1000,mode=stat.S_IFREG|0o600,relative='venv/module.py',link='lib',nlink=1):
        root=Mock();path=Mock();root.rglob.return_value=[path];root.__truediv__=Mock(return_value=object())
        path.relative_to.return_value=relative;path.read_bytes.return_value=b'fixture'
        path.lstat.return_value=types.SimpleNamespace(st_mode=mode,st_uid=uid,st_gid=1000,st_nlink=nlink)
        with patch.object(p.os,'readlink',return_value=link,create=True):return p.fingerprint(root)
    def test_uid1000_regular_module(self):self.assertEqual(self.model()['venv/module.py']['mode'],0o600)
    def test_root_owned_file_refused(self):
        with self.assertRaisesRegex(p.Blocked,'OWNER'):self.model(uid=0)
    def test_group_writable_file_refused(self):
        with self.assertRaisesRegex(p.Blocked,'MODE'):self.model(mode=stat.S_IFREG|0o666)
    def test_expected_lib64_alias_only(self):
        self.assertEqual(self.model(mode=stat.S_IFLNK|0o777,relative='venv/lib64'),{'venv/lib64':{'link':'lib'}})
        with self.assertRaisesRegex(p.Blocked,'SYMLINK'):self.model(mode=stat.S_IFLNK|0o777,relative='venv/foreign',link='/home/jazofv1/hioc')
    def test_hardlinked_file_refused(self):
        with self.assertRaisesRegex(p.Blocked,'HARDLINK'):self.model(nlink=2)


class PrepareTests(unittest.TestCase):
    def model(self,temp):
        stack=contextlib.ExitStack();self.addCleanup(stack.close)
        root=Path(temp)/'new-private-cache';stack.enter_context(patch.object(p,'ROOT',root))
        stack.enter_context(patch.object(p,'target'));stack.enter_context(patch.object(p,'owned_directory'))
        stack.enter_context(patch.object(p,'fingerprint',return_value={}))
        def writing(path,raw):
            with path.open('xb') as stream:stream.write(raw)
        stack.enter_context(patch.object(p,'new_file',side_effect=writing))
        engine=p.load_engine(ENGINE);engine.TOOLKIT=[]
        stack.enter_context(patch.object(p,'load_engine',return_value=engine))
        engine.fetch=Mock(return_value=b'fixture');engine.validate_wheel=Mock();engine.sync_directory=Mock()
        engine.invoke=Mock(side_effect=[b'',b'',json.dumps({'RESULT':'PASS_ISOLATED_CRYPTOGRAPHY_SMOKE','versions':engine.VERSIONS,'private_material_output':False}).encode()])
        import venv
        stack.enter_context(patch.object(venv,'EnvBuilder'))
        return root,engine
    def test_private_environment_setup_only(self):
        with tempfile.TemporaryDirectory() as temp:
            root,engine=self.model(temp);result=p.prepare()
            self.assertEqual(result['RESULT'],'PASS_PI3_ISOLATED_PROVISIONING_ENVIRONMENT')
            self.assertEqual((result['uid'],result['gid']),(1000,1000))
            self.assertFalse(result['production_CA_created']);self.assertFalse(result['HMAC_material_provisioned'])
            self.assertFalse(result['HIOC_modified']);self.assertFalse(result['PI5_modified'])
            self.assertEqual(engine.invoke.call_count,3);self.assertTrue((root/'ready.json').exists())
    def test_old_system_crypto_not_imported_for_setup(self):
        with tempfile.TemporaryDirectory() as temp:
            root,engine=self.model(temp)
            with patch.dict(sys.modules,{'cryptography':None}):self.assertEqual(p.prepare()['native_smoke'],'PASS')
    def test_existing_cache_refused(self):
        with tempfile.TemporaryDirectory() as temp:
            root,engine=self.model(temp);root.mkdir()
            with self.assertRaisesRegex(p.Blocked,'EXISTING'):p.prepare()
            engine.fetch.assert_not_called();engine.invoke.assert_not_called()
    def test_dependency_integrity_failure_before_cache_creation(self):
        with tempfile.TemporaryDirectory() as temp:
            root,engine=self.model(temp);engine.fetch.side_effect=engine.Blocked('DEPENDENCY_IDENTITY_MISMATCH')
            with self.assertRaises(ValueError):p.prepare()
            self.assertFalse(root.exists());engine.invoke.assert_not_called()
    def test_unsupported_tags_stop_before_install(self):
        with tempfile.TemporaryDirectory() as temp:
            root,engine=self.model(temp);engine.invoke.side_effect=engine.Blocked('PINNED_WHEEL_TAG_OR_OFFLINE_RESOLUTION_UNSUPPORTED')
            with self.assertRaises(ValueError):p.prepare()
            self.assertEqual(engine.invoke.call_count,1);self.assertFalse((root/'ready.json').exists())
    def test_interrupted_install_retains_no_ready(self):
        with tempfile.TemporaryDirectory() as temp:
            root,engine=self.model(temp);engine.invoke.side_effect=[b'',KeyboardInterrupt()]
            with self.assertRaises(KeyboardInterrupt):p.prepare()
            self.assertTrue(root.exists());self.assertFalse((root/'ready.json').exists());self.assertEqual(engine.invoke.call_count,2)
    def test_incomplete_smoke_cannot_mark_ready(self):
        with tempfile.TemporaryDirectory() as temp:
            root,engine=self.model(temp);engine.invoke.side_effect=[b'',b'',b'{}']
            with self.assertRaises(ValueError):p.prepare()
            self.assertFalse((root/'ready.json').exists())

class ActualAPIWindowsTests(unittest.TestCase):
    def test_actual_provisioning_crypto_APIs_ephemeral_non_CA_only(self):
        from cryptography import x509
        from cryptography.hazmat.primitives import hashes,serialization
        from cryptography.hazmat.primitives.asymmetric import ec
        from cryptography.x509.oid import NameOID
        key=ec.generate_private_key(ec.SECP256R1())
        csr=x509.CertificateSigningRequestBuilder().subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME,'PE73 ephemeral dependency smoke')])).sign(key,hashes.SHA256())
        namespace=dict(root=ROOT,key=key,csr=csr,hashlib=hashlib,x509=x509,hashes=hashes,serialization=serialization)
        exec(compile(p.EXTRA_SMOKE,'ephemeral-Windows-API-check','exec'),namespace)
        self.assertFalse(namespace['leaf'].extensions.get_extension_for_class(x509.BasicConstraints).value.ca)

if __name__=='__main__':unittest.main()
