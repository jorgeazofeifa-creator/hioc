"""Bounded synthetic/local Windows checks; never Pi native evidence."""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock,patch
import zipfile

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('pe73_environment_test',ROOT/'tools/pe73_provision_environment.py')
e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)

def wheel(**extra):
    stream=io.BytesIO()
    with zipfile.ZipFile(stream,'w') as z:
        for name,raw in {'fixture/__init__.py':b'', 'fixture-1.dist-info/WHEEL':b'Wheel-Version: 1.0\n',
                         'fixture-1.dist-info/RECORD':b'',**extra}.items():z.writestr(name,raw)
    return stream.getvalue()

class IntegrityTests(unittest.TestCase):
    def test_valid_exact_dependency(self):
        raw=b'fixture';item={'size':len(raw),'sha256':e.sha(raw)}
        self.assertEqual(e.checked(raw,item),raw)
    def test_bad_hash(self):
        with self.assertRaisesRegex(e.Blocked,'IDENTITY'):e.checked(b'other',{'size':5,'sha256':'0'*64})
    def test_wrong_length(self):
        with self.assertRaises(e.Blocked):e.checked(b'x',{'size':2,'sha256':e.sha(b'x')})
    def test_valid_wheel_archive(self):e.validate_wheel(wheel(),'fixture.whl')
    def test_source_distribution_refused(self):
        with self.assertRaises(e.Blocked):e.validate_wheel(wheel(),'fixture.tar.gz')
    def test_wheel_path_escape(self):
        with self.assertRaisesRegex(e.Blocked,'UNSAFE'):e.validate_wheel(wheel(**{'../escape':b'x'}),'fixture.whl')
    def test_absolute_wheel_path(self):
        with self.assertRaises(e.Blocked):e.validate_wheel(wheel(**{'/config/private':b'x'}),'fixture.whl')
    def test_unapproved_dependency_source(self):
        with patch.object(e.urllib.request,'urlopen') as request:
            with self.assertRaises(e.Blocked):e.fetch({'url':'http://untrusted.invalid/package'})
            request.assert_not_called()
    def test_redirect_refused(self):
        response=Mock();response.geturl.return_value='https://other.invalid'
        with patch.object(e.urllib.request,'build_opener',return_value=Mock(open=Mock(return_value=contextlib.nullcontext(response)))):
            with self.assertRaisesRegex(e.Blocked,'REDIRECT'):e.fetch({'url':'https://files.pythonhosted.org/packages/fixed'})
    def test_transitive_dependencies_exactly_locked(self):
        self.assertEqual(e.VERSIONS,{'cryptography':'50.0.2','cffi':'2.0.0','pycparser':'2.23'})
        text=e.lock_text().decode()
        self.assertEqual(len(text.splitlines()),3)
        for item in e.WHEELS:
            if not item['name'].startswith('pip-'):self.assertIn('--hash=sha256:'+item['sha256'],text)
        self.assertEqual(len(e.WHEELS),6)
    def test_toolkit_bytes_match_immutable_acceptance(self):
        self.assertEqual(len(e.TOOLKIT),7)
        for item in e.TOOLKIT:
            self.assertEqual(e.checked((ROOT/'tools'/item['name']).read_bytes(),item),(ROOT/'tools'/item['name']).read_bytes())

class IsolationTests(unittest.TestCase):
    def test_installer_has_no_inherited_secrets_or_credential_config(self):
        with patch.dict(os.environ,{'SUPERVISOR_TOKEN':'PRIVATE_SENTINEL','HTTPS_PROXY':'PRIVATE_PROXY','SSH_AUTH_SOCK':'PRIVATE_AGENT','PYTHONPATH':'PRIVATE_PATH','PIP_INDEX_URL':'PRIVATE_TOKEN'}):
            env=e.clean_env(Path('/private/fixture'))
        self.assertNotIn('PRIVATE',json.dumps(env));self.assertEqual(env['PIP_CONFIG_FILE'],os.devnull)
    def test_binary_only_offline_no_build_no_global_install(self):
        root=Path('/private/fixture');args=e.pip_command(root)
        for value in ('--no-index','--no-deps','--only-binary=:all:','--require-hashes','--no-cache-dir','--no-compile','--no-user','--isolated'):
            self.assertIn(value,args)
        self.assertEqual(args[args.index('--prefix')+1],str(root/'venv'))
        self.assertEqual(args[0],str(root/'venv/bin/python3'))
        self.assertNotIn('--break-system-packages',args)
    def test_failed_installer_redacts_private_errors_and_never_retries(self):
        with patch.object(e.subprocess,'run',return_value=Mock(returncode=1,stdout=b'PRIVATE_KEY',stderr=b'PRIVATE_ERROR')) as run:
            with self.assertRaisesRegex(e.Blocked,'ISOLATED_DEPENDENCY_COMMAND_FAILED') as caught:
                e.invoke(['fixture'],Path('/private'))
            self.assertNotIn('PRIVATE_KEY',str(caught.exception));self.assertEqual(run.call_count,1)
    def test_real_local_venv_excludes_system_and_user_paths(self):
        # Actual local Windows CPython venv, not proof of native Pi support.
        import venv
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)/'isolated'
            venv.EnvBuilder(with_pip=False,system_site_packages=False).create(root)
            python=root/('Scripts/python.exe' if os.name=='nt' else 'bin/python3')
            code='import json,sys,site; print(json.dumps([sys.prefix!=sys.base_prefix,site.ENABLE_USER_SITE,sys.flags.isolated]))'
            value=subprocess.check_output([str(python),'-I','-B','-c',code],env={'PATH':os.environ.get('PATH',''),'SYSTEMROOT':os.environ.get('SYSTEMROOT',''),'PYTHONPATH':temp})
            self.assertEqual(json.loads(value),[True,False,1])
    def test_no_core_or_container_operation(self):
        source=(ROOT/'tools/pe73_provision_environment.py').read_text()
        import ast
        tree=ast.parse(source)
        literals=[n.value for n in ast.walk(tree) if isinstance(n,ast.Constant) and isinstance(n.value,str)]
        self.assertFalse(any(x in ('docker','/usr/local/bin/docker','/config','/homeassistant','sudo') for x in literals))
    def test_only_existing_ha_provisioning_actions_allowed(self):
        with patch.object(e,'target'):
            for action in ('backend-init','install','activate','rollback'):
                with self.assertRaisesRegex(e.Blocked,'HA_PROVISIONING_ACTION_ONLY'):e.launch(action)
    def test_missing_ready_receipt_blocks_before_credential_operation(self):
        with tempfile.TemporaryDirectory() as temp,patch.object(e,'ROOT',Path(temp)),patch.object(e,'target'),patch.object(e,'owned_directory'),patch.object(e.subprocess,'run') as run:
            with self.assertRaises(FileNotFoundError):e.launch('ha-request')
            run.assert_not_called()
    def launch_fixture(self,temp,drift=False):
        root=Path(temp);files={'fixture':{'sha256':'a'*64}}
        ready={'schema':1,'source_python':e.sha(Path(sys.executable).resolve().read_bytes()),
            'python_version':list(sys.version_info[:3]),'files':files,'versions':e.VERSIONS}
        (root/'ready.json').write_bytes(e.canonical(ready))
        stack=contextlib.ExitStack();self.addCleanup(stack.close)
        stack.enter_context(patch.object(e,'ROOT',root));stack.enter_context(patch.object(e,'target'))
        stack.enter_context(patch.object(e,'owned_directory'));stack.enter_context(patch.object(e.stat,'S_IMODE',return_value=0o600))
        stack.enter_context(patch.object(e,'fingerprint',return_value={} if drift else files))
        return stack.enter_context(patch.object(e.subprocess,'run',return_value=Mock(returncode=0)))
    def test_qualified_environment_launch_keeps_local_key_custody(self):
        with tempfile.TemporaryDirectory() as temp:
            run=self.launch_fixture(temp)
            with patch.dict(os.environ,{'SUPERVISOR_TOKEN':'PRIVATE_SENTINEL'}):value=e.launch('ha-request')
            self.assertEqual(value['RESULT'],'PASS_ISOLATED_PROVISIONING_ACTION')
            args=run.call_args.args[0]
            self.assertEqual(args[-1],'ha-request');self.assertIn('-I',args);self.assertIn('-B',args)
            self.assertNotIn('SUPERVISOR_TOKEN',run.call_args.kwargs['env'])
            self.assertEqual(run.call_count,1)
    def test_changed_dependency_seal_refuses_before_key_operation(self):
        with tempfile.TemporaryDirectory() as temp:
            run=self.launch_fixture(temp,drift=True)
            with self.assertRaisesRegex(e.Blocked,'ISOLATED_ENVIRONMENT_DRIFT'):e.launch('ha-request')
            run.assert_not_called()
    def test_wrong_abi_fails_before_creating_environment(self):
        with patch.object(e.sys,'platform','linux'),patch.object(e.platform,'machine',return_value='x86_64'):
            with self.assertRaisesRegex(e.Blocked,'SUPPORTED_TERMINAL_ABI_REQUIRED'):e.target()
    def test_free_threaded_python_not_silently_accepted(self):
        with patch.object(e.sys,'platform','linux'),patch.object(e.sys,'version_info',(3,14,8)),patch.object(e.platform,'machine',return_value='aarch64'),patch.object(e.platform,'python_implementation',return_value='CPython'),patch.object(e.sysconfig,'get_config_var',return_value=1):
            with self.assertRaises(e.Blocked):e.target()

class SealTests(unittest.TestCase):
    def symlink(self,relative='venv/lib64',destination='lib',uid=0):
        root=Mock();path=Mock();root.rglob.return_value=[path]
        root.__truediv__=Mock(return_value=object())
        path.relative_to.return_value=relative
        import stat
        path.lstat.return_value=Mock(st_mode=stat.S_IFLNK|0o777,st_uid=uid,st_gid=0)
        with patch.object(e.os,'readlink',return_value=destination):return e.fingerprint(root)
    def test_standard_venv_lib64_alias_is_not_rejected_for_symlink_mode(self):
        self.assertEqual(self.symlink(),{'venv/lib64':{'link':'lib'}})
    def test_arbitrary_symlink_cannot_bypass_environment_seal(self):
        with self.assertRaisesRegex(e.Blocked,'SYMLINK'):self.symlink('venv/foreign','/config')
    def test_wrong_owner_symlink_refused(self):
        with self.assertRaisesRegex(e.Blocked,'OWNER'):self.symlink(uid=1000)


class PrepareTests(unittest.TestCase):
    def model(self,temp):
        stack=contextlib.ExitStack();self.addCleanup(stack.close)
        root=Path(temp)/'new-environment';stack.enter_context(patch.object(e,'ROOT',root))
        stack.enter_context(patch.object(e,'target'))
        stack.enter_context(patch.object(e,'owned_directory'))
        raw=wheel();package={'name':'pip-fixture.whl','size':len(raw),'sha256':e.sha(raw),'url':'https://files.pythonhosted.org/packages/fixture'}
        stack.enter_context(patch.object(e,'WHEELS',[package]));stack.enter_context(patch.object(e,'TOOLKIT',[]))
        fetch=stack.enter_context(patch.object(e,'fetch',return_value=raw))
        def new_file(path,value):
            with path.open('xb') as f:f.write(value)
        stack.enter_context(patch.object(e,'new_file',side_effect=new_file))
        stack.enter_context(patch.object(e,'fingerprint',return_value={'fixture':{'sha256':'a'*64}}))
        import venv
        builder=stack.enter_context(patch.object(venv,'EnvBuilder'))
        invoke=stack.enter_context(patch.object(e,'invoke',side_effect=[b'',b'',json.dumps({'RESULT':'PASS_ISOLATED_CRYPTOGRAPHY_SMOKE','versions':e.VERSIONS,'private_material_output':False}).encode()]))
        stack.enter_context(patch.object(e,'sync_directory'))
        return root,fetch,builder,invoke
    def test_supported_isolated_execution_and_no_ensurepip(self):
        with tempfile.TemporaryDirectory() as temp:
            root,fetch,builder,invoke=self.model(temp);value=e.prepare()
            self.assertEqual(value['RESULT'],'PASS_PI5_ISOLATED_PROVISIONING_ENVIRONMENT')
            self.assertFalse(value['production_credentials_created']);self.assertFalse(value['Core_modified'])
            self.assertEqual(invoke.call_count,3)
            builder.assert_called_once_with(system_site_packages=False,clear=False,symlinks=False,with_pip=False,upgrade=False)
            self.assertTrue((root/'ready.json').is_file())
    def test_missing_terminal_crypto_does_not_prevent_isolated_setup(self):
        with tempfile.TemporaryDirectory() as temp:
            root,fetch,builder,invoke=self.model(temp)
            with patch.dict(sys.modules,{'cryptography':None,'cffi':None}):result=e.prepare()
            self.assertEqual(result['RESULT'],'PASS_PI5_ISOLATED_PROVISIONING_ENVIRONMENT')
    def test_missing_stdlib_venv_stops_before_download_or_creation(self):
        import builtins
        original=builtins.__import__
        def importing(name,*args,**kwargs):
            if name=='venv':raise ImportError('fixture')
            return original(name,*args,**kwargs)
        with tempfile.TemporaryDirectory() as temp:
            root,fetch,builder,invoke=self.model(temp)
            with patch.object(builtins,'__import__',side_effect=importing):
                with self.assertRaisesRegex(e.Blocked,'STDLIB_VENV_UNAVAILABLE'):e.prepare()
            self.assertFalse(root.exists());fetch.assert_not_called()
    def test_existing_environment_refused_without_download_or_repair(self):
        with tempfile.TemporaryDirectory() as temp:
            root,fetch,builder,invoke=self.model(temp);root.mkdir()
            with self.assertRaisesRegex(e.Blocked,'EXISTING_ENVIRONMENT_REFUSED'):e.prepare()
            fetch.assert_not_called();builder.assert_not_called();invoke.assert_not_called()
    def test_dependency_failure_leaves_no_environment(self):
        with tempfile.TemporaryDirectory() as temp:
            root,fetch,builder,invoke=self.model(temp);fetch.side_effect=e.Blocked('DEPENDENCY_IDENTITY_MISMATCH')
            with self.assertRaises(e.Blocked):e.prepare()
            self.assertFalse(root.exists());builder.assert_not_called();invoke.assert_not_called()
    def test_unsupported_wheels_no_install_no_credentials_no_ready(self):
        with tempfile.TemporaryDirectory() as temp:
            root,fetch,builder,invoke=self.model(temp);invoke.side_effect=e.Blocked('PINNED_WHEEL_TAG_OR_OFFLINE_RESOLUTION_UNSUPPORTED')
            with self.assertRaises(e.Blocked):e.prepare()
            self.assertEqual(invoke.call_count,1);self.assertTrue(root.exists());self.assertFalse((root/'ready.json').exists())
    def test_interrupted_install_retains_partial_without_launch_or_cleanup(self):
        with tempfile.TemporaryDirectory() as temp:
            root,fetch,builder,invoke=self.model(temp);invoke.side_effect=[b'',KeyboardInterrupt()]
            with self.assertRaises(KeyboardInterrupt):e.prepare()
            self.assertTrue(root.exists());self.assertFalse((root/'ready.json').exists());self.assertEqual(invoke.call_count,2)
    def test_smoke_failure_cannot_mark_ready(self):
        with tempfile.TemporaryDirectory() as temp:
            root,fetch,builder,invoke=self.model(temp);invoke.side_effect=[b'',b'',b'{"RESULT":"WRONG"}']
            with self.assertRaisesRegex(e.Blocked,'SMOKE'):e.prepare()
            self.assertFalse((root/'ready.json').exists())

if __name__=='__main__':unittest.main()
