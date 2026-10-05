"""Windows-native synthetic proof; never invokes a production lifecycle action."""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import pathlib
import shutil
import struct
import subprocess
import sys
import tempfile
import types
import unittest
import venv
import zipfile
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
spec = importlib.util.spec_from_file_location("action_e_immutable", ROOT / "tools/hioc-pe4-dependency-validate.py")
E = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = E
spec.loader.exec_module(E)
WHEEL = pathlib.Path(os.environ["LOCALAPPDATA"]) / "HIOC/artifacts/pe4/cache" / E.WHEEL_NAME


class ControlledRuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # The AArch64 member is inspected, never installed or certified on Windows.
        cls.archive = WHEEL.read_bytes()
        assert len(cls.archive) == E.WHEEL_SIZE
        assert hashlib.sha256(cls.archive).hexdigest() == E.WHEEL_SHA256
        cls.seed_temp = tempfile.TemporaryDirectory()
        cls.seed = pathlib.Path(cls.seed_temp.name).resolve() / "seed"
        venv.EnvBuilder(with_pip=False, symlinks=False).create(cls.seed)
        cls.executable_relative = pathlib.Path("Scripts/python.exe") if os.name == "nt" else pathlib.Path("bin/python")

    @classmethod
    def tearDownClass(cls):
        cls.seed_temp.cleanup()

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name).resolve() / "construction"
        # Fixture setup only; copying an accepted production construction is prohibited.
        shutil.copytree(self.seed, self.root)
        self.python = self.root / self.executable_relative
        self.site = self.root / "lib/python3.11/site-packages"
        self.site.mkdir(parents=True)
        with zipfile.ZipFile(io.BytesIO(self.archive)) as archive:
            for member in archive.namelist():
                if member.endswith("/"):
                    continue
                if member.startswith("websockets/") or member.endswith(".dist-info/METADATA") or member.endswith("entry_points.txt"):
                    target = self.site / member
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(archive.read(member))
        self.metadata("pip", "23.0.1")
        self.metadata("setuptools", "66.1.1")
        self.marker = self.root / ".hioc-action-d-eligibility.json"
        self.marker.write_text('{"synthetic":"marker"}')
        self.d_evidence = pathlib.Path(self.temp.name) / "d-evidence"
        self.d_evidence.mkdir(); (self.d_evidence / "result.json").write_text('{"synthetic":"evidence"}')
        self.sentinel = self.root / "MUST_NOT_EXIST"
        self.env = E.action_d_subprocess_environment()
        if os.name == "nt":
            self.env["SYSTEMROOT"] = os.environ["SYSTEMROOT"]
        # Platform-equivalent fixture policy is not exposed by production CLI.
        state = subprocess.run([str(self.python), "-I", "-B", "-S", "-c",
            "import json,sys,sysconfig,os;print(json.dumps({'paths':sys.path,'prefix':sys.base_prefix,'version':list(sys.version_info[:3]),'soabi':sysconfig.get_config_var('SOABI'),'base':os.path.realpath(sys._base_executable)}))"],
            capture_output=True, text=True, check=True, env=self.env)
        self.policy = json.loads(state.stdout)
        info = self.python.stat()
        self.policy.update(site=str(self.site), interpreter=str(self.python), interpreter_identity=[info.st_dev, info.st_ino])

    def metadata(self, name, version, directory=None):
        path = self.site / (directory or (name + "-" + version + ".dist-info"))
        path.mkdir(exist_ok=True)
        (path / "METADATA").write_text("Metadata-Version: 2.1\nName: " + name + "\nVersion: " + version + "\n")

    def child(self, capability=False, prefix="", suffix="", policy=None, success=True):
        baseline = E.snapshot_tree(self.root)
        evidence = E.snapshot_tree(self.d_evidence)
        script = E.child_script(policy or self.policy, capability)
        # Test instrumentation runs after startup validation and before probe execution.
        if prefix:
            script = script.replace("\nvalidate_startup(POLICY)\n", "\nvalidate_startup(POLICY)\n" + prefix + "\n")
        result = subprocess.run([str(self.python), "-I", "-B", "-S", "-c", script + suffix],
            cwd=self.root, env=self.env, capture_output=True, text=True, timeout=60)
        self.assertEqual(E.snapshot_tree(self.root), baseline)
        self.assertEqual(E.snapshot_tree(self.d_evidence), evidence)
        self.assertFalse(self.sentinel.exists())
        if success:
            self.assertEqual(result.returncode, 0, result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0)
        return result

    def attack_source(self):
        return "from pathlib import Path;Path(" + repr(str(self.sentinel)) + ").write_text('EXECUTED')\n"

    def test_exact_wheel_and_all_52_members(self):
        with zipfile.ZipFile(io.BytesIO(self.archive)) as archive:
            expected = {name:hashlib.sha256(archive.read(name)).hexdigest() for name in archive.namelist()
                        if name.startswith("websockets/") and not name.endswith("/")}
        self.assertEqual(E.WHEEL_MEMBERS, expected)
        self.assertEqual(len(expected), 52)
        self.assertEqual(expected[E.NATIVE_MEMBER], "b786db296f7d0677ddeceb7efbe963bc316a094f36e12388caa1333763ca4c1b")
        E.validate_members(self.site)

    def test_cache_free_capability_and_distribution_success(self):
        self.assertFalse(list(self.site.rglob("*.pyc")))
        result = self.child()
        self.assertEqual(E.validate_distributions(result.stdout.splitlines()),
                         {"pip":"23.0.1", "setuptools":"66.1.1", "websockets":"16.1.1"})
        self.assertEqual(self.child(True).stdout, "CAPABILITY_VALIDATION=PASS\n")
        self.assertFalse(list(self.site.rglob("__pycache__")))

    def test_executable_pth_is_inert(self):
        (self.site / "distutils-precedence.pth").write_text("import pathlib;pathlib.Path(" + repr(str(self.sentinel)) + ").write_text('EXECUTED')\n")
        self.child(); self.child(True)

    def test_sitecustomize_is_inert(self):
        (self.site / "sitecustomize.py").write_text(self.attack_source())
        self.child(); self.child(True)

    def test_usercustomize_and_pythonpath_are_inert(self):
        (self.site / "usercustomize.py").write_text(self.attack_source())
        (self.root / "sitecustomize.py").write_text(self.attack_source())
        self.env["PYTHONPATH"] = str(self.site)
        self.env["PYTHONDONTWRITEBYTECODE"] = "0"
        self.child(); self.child(True)

    def test_metadata_does_not_execute_packages_or_entry_points(self):
        for name in ("pip", "setuptools"):
            package = self.site / name; package.mkdir(); (package / "__init__.py").write_text(self.attack_source())
        (self.site / "pip-23.0.1.dist-info/entry_points.txt").write_text("[console_scripts]\nattack = pip:attack\n")
        self.child(suffix="\nassert not any(n in sys.modules for n in ('pip','setuptools','websockets'))\n")

    def test_optional_python_socks_is_blocked(self):
        package = self.site / "python_socks"; package.mkdir(); (package / "__init__.py").write_text(self.attack_source())
        self.child(True)

    def test_unrelated_import_blocked_and_stdlib_permitted(self):
        (self.site / "unrelated.py").write_text(self.attack_source())
        self.child(True, suffix="\nimport fractions\ntry:\n import unrelated\nexcept ModuleNotFoundError:\n pass\nelse:\n raise AssertionError('unrelated import accepted')\n")

    def test_missing_stdlib_name_cannot_fall_through_to_site(self):
        (self.site / "_unavailable_fixture.py").write_text(self.attack_source())
        self.child(True,suffix="\nsys.stdlib_module_names=frozenset(set(sys.stdlib_module_names)|{'_unavailable_fixture'})\ntry:\n import _unavailable_fixture\nexcept ModuleNotFoundError:\n pass\nelse:\n raise AssertionError('stdlib fallback escaped')\n")

    def test_unreviewed_websockets_module_blocked(self):
        self.child(True, suffix="\ntry:\n import websockets.cli\nexcept ModuleNotFoundError:\n pass\nelse:\n raise AssertionError('unreviewed import accepted')\n")

    def test_no_network_resolution_connection_proxy_or_url_open(self):
        guards = """import socket,asyncio,urllib.request

def forbidden(*args,**kwargs): raise AssertionError('NETWORK_ATTEMPT')
socket.socket.connect = forbidden
socket.socket.connect_ex = forbidden
socket.create_connection = forbidden
socket.getaddrinfo = forbidden
socket.gethostbyname = forbidden
socket.gethostbyname_ex = forbidden
socket.gethostbyaddr = forbidden
asyncio.BaseEventLoop.create_connection = forbidden
asyncio.BaseEventLoop.create_unix_connection = forbidden
urllib.request.urlopen = forbidden
urllib.request.getproxies = forbidden
"""
        self.child(True, prefix=guards)

    def test_stale_and_malicious_pyc_are_ignored(self):
        import py_compile
        cache = self.site / "websockets/__pycache__"; cache.mkdir()
        source = pathlib.Path(self.temp.name) / "evil.py"; source.write_text(self.attack_source())
        dest = cache / ("version." + sys.implementation.cache_tag + ".pyc")
        py_compile.compile(str(source), cfile=str(dest), doraise=True)
        installed=(self.site/"websockets/version.py").stat()
        cache_bytes=dest.read_bytes()
        dest.write_bytes(cache_bytes[:8]+struct.pack("<II",int(installed.st_mtime),installed.st_size)+cache_bytes[16:])
        # Even a valid-looking timestamp cache never reaches the source loader.
        self.child(True,suffix="\nassert sys.modules['websockets.version'].__cached__ is None\n")
        (cache / "missing.cpython-311.pyc").write_bytes(b"stale")
        self.child(True)

    def test_changed_missing_unexpected_and_native_members_rejected(self):
        cases = [("websockets/version.py", "change"), ("websockets/imports.py", "missing"),
                 ("websockets/extra.py", "extra"), (E.NATIVE_MEMBER, "change")]
        for member, operation in cases:
            path = self.site / member
            original = path.read_bytes() if path.exists() else None
            try:
                if operation == "missing": path.unlink()
                else: path.write_bytes(b"changed")
                with self.assertRaises(E.Failure): E.validate_members(self.site)
                self.child(True, success=False)
            finally:
                if original is None: path.unlink()
                else: path.write_bytes(original)

    def test_failure_after_real_package_imports_preserves_tree(self):
        self.child(True, suffix="\nassert 'websockets.asyncio.client' in sys.modules\nraise RuntimeError('ordinary failure after imports')\n", success=False)

    def test_missing_signature_failure_after_imports_preserves_tree(self):
        self.child(True, prefix="inspect.signature=lambda obj: type('S',(),{'parameters':{}})()", success=False)

    def test_unexpected_path_and_finder_state_fail_closed(self):
        self.child(prefix="sys.path.append(POLICY['site']);validate_startup(POLICY)", success=False)
        self.child(prefix="sys.meta_path.append(object());validate_startup(POLICY)", success=False)
        self.child(policy=dict(self.policy, paths=self.policy['paths'] + [str(self.root)]), success=False)

    def test_wrong_interpreter_version_base_or_site_rejected(self):
        for field, value in (("interpreter_identity",[-1,-1]), ("version",[3,11,2]),
                             ("base","/not/the/base"), ("prefix","/wrong-prefix"), ("soabi","wrong-soabi"),
                             ("site",str(self.root / "wrong-site"))):
            if field == "version" and self.policy[field] == value: value=[3,10,0]
            self.child(True, policy=dict(self.policy, **{field:value}), success=False)

    def test_distribution_rejection_preserves_construction(self):
        scenarios = [("extra", "1.0", None), ("pip", "23.0.1", "duplicate.dist-info"),
                     ("websockets", "0", "wrong.dist-info"), ("setuptools", "bad version", "bad.dist-info")]
        for name, version, directory in scenarios:
            path = self.site / (directory or name + "-" + version + ".dist-info")
            self.metadata(name, version, directory)
            try:
                result = self.child()
                with self.assertRaises(E.Failure) as caught: E.validate_distributions(result.stdout.splitlines())
                self.assertEqual((caught.exception.code,caught.exception.stage),
                                 ("INSTALLED_DISTRIBUTION_SET_INVALID","DEPENDENCY_IDENTITY"))
            finally:
                shutil.rmtree(path)

    def test_distribution_policy_matches_existing_common(self):
        cases = ["pip==23.0.1\nwebsockets==16.1.1", "pip==23.0.1\nsetuptools==66.1.1\nwebsockets==16.1.1",
                 "pip==23.0.1\nwebsockets==16.1.1\nextra==1", "websockets==16.1.1", "pip==bad version\nwebsockets==16.1.1",
                 "pip==1\npip==1\nwebsockets==16.1.1", "pip==1\nwebsockets==0", "broken"]
        import hioc_pe4_runtime_common as common
        for output in cases:
            with mock.patch.object(common, "run", return_value=types.SimpleNamespace(stdout=output)):
                try: expected = common.exact_distribution_set(pathlib.Path("synthetic"))
                except common.Failure as expected_error:
                    with self.assertRaises(E.Failure) as actual: E.validate_distributions(output.splitlines())
                    self.assertEqual((actual.exception.code,actual.exception.stage),(expected_error.code,expected_error.stage))
                else: self.assertEqual(E.validate_distributions(output.splitlines()), expected)

    def test_venv_configuration_valid_and_invalid(self):
        valid = b"home = /usr/bin\ninclude-system-site-packages = false\nversion = 3.11.2\nexecutable = /usr/bin/python3\ncommand = /usr/bin/python3 -m venv --copies .\n"
        self.assertEqual(E.parse_venv_configuration(valid,"/usr/bin/python3")["version"],"3.11.2")
        bad = [valid.replace(b"/usr/bin\n",b"/wrong\n"),valid.replace(b"false",b"true"),
               valid.replace(b"version = 3.11.2\n",b""),valid+b"home = /wrong\n",valid+b"malformed\n",
               valid.replace(b"executable = /usr/bin/python3",b"executable = /wrong"),b"\xff",valid+b"unexpected = value\n"]
        for raw in bad:
            with self.assertRaises(E.Failure): E.parse_venv_configuration(raw,"/usr/bin/python3")

    def test_executable_library_overrides_and_build_markers(self):
        exe=self.root / "fixture-python";library=self.root / "libpython3.11.so"
        candidates=[pathlib.Path(str(exe)+"._pth"),pathlib.Path(str(library)+"._pth"),self.root / "pybuilddir.txt",self.root / "Modules/Setup.local"]
        for path in candidates:
            path.parent.mkdir(exist_ok=True)
            path.write_text("import site\n")
            try:
                with self.assertRaises(E.Failure) as caught:E.reject_startup_overrides([exe],[library])
                self.assertEqual(caught.exception.code,"STARTUP_OVERRIDE_REJECTED")
            finally:path.unlink()

    def test_both_runtime_requests_flags_fd_environment_and_output(self):
        root=types.SimpleNamespace(fd=123)
        with mock.patch.object(E,"run",return_value=types.SimpleNamespace(stdout="pip==1\nwebsockets==16.1.1\n")) as run:
            E.controlled_distributions(root,self.env,self.policy)
            args,kwargs=run.call_args
            self.assertEqual(args[0][:5],["./bin/python","-I","-B","-S","-c"])
            self.assertEqual(kwargs,dict(cwd="/proc/self/fd/123",pass_fds=(123,),env=self.env))
        with mock.patch.object(E,"run",return_value=types.SimpleNamespace(stdout="CAPABILITY_VALIDATION=PASS\n")) as run:
            E.controlled_capabilities(root,self.env,self.policy)
            self.assertEqual(run.call_args.args[0][:5],["./bin/python","-I","-B","-S","-c"])
        expected={"PATH":"/usr/bin:/bin","LANG":"C.UTF-8","LC_ALL":"C.UTF-8","HOME":"/nonexistent",
                  "PYTHONNOUSERSITE":"1","PYTHONDONTWRITEBYTECODE":"1","PIP_CONFIG_FILE":os.devnull,
                  "PIP_DISABLE_PIP_VERSION_CHECK":"1","PIP_NO_INPUT":"1","PIP_NO_INDEX":"1",
                  "PIP_ROOT_USER_ACTION":"ignore","PIP_KEYRING_PROVIDER":"disabled"}
        self.assertEqual(E.action_d_subprocess_environment(),expected)

    def test_outer_provenance_rejects_before_child_launch(self):
        (self.root / "bin").mkdir(exist_ok=True)
        interpreter=self.root / "bin/python"
        shutil.copyfile(sys.executable,interpreter)
        root=types.SimpleNamespace(path=self.root,fd=123)
        base=pathlib.Path(self.temp.name)/"base-python3"
        shutil.copyfile(sys.executable,base)
        with mock.patch.object(E,"BASE_EXECUTABLE",base), \
             mock.patch.object(E,"validate_venv_symlinks"), \
             mock.patch.object(E,"parse_venv_configuration",return_value={}), \
             mock.patch.object(E,"run") as launched:
            self.assertEqual(E.validate_runtime_inputs(root)["site"],str(self.site))
            for override in (self.root/"bin/python._pth",self.root/"bin/pyvenv.cfg",self.root/"bin/pybuilddir.txt"):
                override.write_text("import site\n")
                try:
                    with self.assertRaises(E.Failure):E.validate_runtime_inputs(root)
                    launched.assert_not_called()
                finally:override.unlink()
            interpreter.write_bytes(b"wrong interpreter")
            with self.assertRaises(E.Failure):E.validate_runtime_inputs(root)
            launched.assert_not_called()

    def test_native_loader_verifies_before_native_execution(self):
        loader=E.VerifiedNativeLoader("websockets.speedups",str(self.site))
        path=self.site/E.NATIVE_MEMBER;path.write_bytes(b"changed native")
        with mock.patch.object(E.importlib.machinery.ExtensionFileLoader,"create_module") as native:
            with self.assertRaises(E.Failure):loader.create_module(types.SimpleNamespace())
            native.assert_not_called()

    def test_bounded_runner_success_failure_output_and_decode(self):
        base=[sys.executable,"-I","-B","-S","-c"]
        self.assertEqual(E.run(base+["print('ok')"],"TEST").stdout,"ok\n")
        for code,expected in (("raise RuntimeError('private diagnostic')","COMMAND_FAILED"),
                              ("print('x'*70000)","COMMAND_OUTPUT_LIMIT"),
                              ("import sys;sys.stdout.buffer.write(bytes([255]))","COMMAND_INVOCATION_FAILED")):
            with self.assertRaises(E.Failure) as caught:E.run(base+[code],"TEST")
            self.assertEqual(caught.exception.code,expected)
            self.assertNotIn("private diagnostic",str(caught.exception))

    def test_real_main_success_failures_and_evidence_boundary(self):
        for fail_gate in (None,"validate_runtime_inputs","controlled_distributions","controlled_capabilities","write_evidence"):
            before=E.snapshot_tree(self.root);d_before=E.snapshot_tree(self.d_evidence)
            evidence=pathlib.Path(self.temp.name)/"evidence"
            directory=types.SimpleNamespace(path=self.root,fd=123,close=mock.Mock())
            def distribution(root,env,policy):
                output=self.child().stdout
                return E.validate_distributions(output.splitlines())
            def capability(root,env,policy):self.child(True)
            def write(path,action,fields,result):
                path.mkdir(exist_ok=True)
                document={"schema_version":"1.0","action":action,**fields,"result":result,"error_code":"NONE","failure_stage":"COMPLETE","rollback_recommended":False}
                (path/"result.json").write_text(json.dumps(document))
            with contextlib.ExitStack() as stack:
                stack.enter_context(mock.patch.object(sys,"argv",["E","--governance-commit","a"*40,"--action-d-governance-commit","b"*40,"--construction-directory",str(self.root)]))
                for name in ("verify_pi3","verify_current_consumer_source","verify_handoff_compatibility","revalidate_owned_directory"):
                    stack.enter_context(mock.patch.object(E,name))
                stack.enter_context(mock.patch.object(E,"validate_construction",return_value=self.root))
                stack.enter_context(mock.patch.object(E,"open_trusted_owned_parent",return_value=directory))
                stack.enter_context(mock.patch.object(E,"open_owned_directory",return_value=directory))
                stack.enter_context(mock.patch.object(E,"validate_action_d_eligibility",return_value={"evidence_directory":str(self.d_evidence)}))
                gates={"validate_runtime_inputs":stack.enter_context(mock.patch.object(E,"validate_runtime_inputs",return_value=self.policy)),
                       "controlled_distributions":stack.enter_context(mock.patch.object(E,"controlled_distributions",side_effect=distribution)),
                       "controlled_capabilities":stack.enter_context(mock.patch.object(E,"controlled_capabilities",side_effect=capability)),
                       "write_evidence":stack.enter_context(mock.patch.object(E,"write_evidence",side_effect=write))}
                publication=stack.enter_context(mock.patch.object(E,"evidence_directory",return_value=evidence))
                if fail_gate:gates[fail_gate].side_effect=E.Failure("BOUNDED_FAILURE","TEST")
                output=io.StringIO();stack.enter_context(contextlib.redirect_stdout(output))
                if fail_gate:
                    with self.assertRaises(E.Failure):E.main()
                    self.assertNotIn("RESULT=PASS",output.getvalue())
                    if fail_gate != "write_evidence":publication.assert_not_called()
                else:
                    E.main()
                    self.assertEqual(output.getvalue().splitlines(),["RESULT=PASS","ERROR_CODE=NONE","FAILURE_STAGE=COMPLETE","ROLLBACK_RECOMMENDED=FALSE","EVIDENCE_DIR="+str(evidence),"CONSTRUCTION_DIRECTORY="+str(self.root)])
                    self.assertEqual(json.loads((evidence/"result.json").read_text()),{
                        "schema_version":"1.0","action":"PE-4.0B.2a-E","ACTION":"DEPENDENCY_VALIDATION",
                        "ENVIRONMENT_IDENTITY":E.VERSIONED_NAME,"INSTALLED_VERSION":"16.1.1","CAPABILITY_VALIDATION":"PASS",
                        "result":"PASS","error_code":"NONE","failure_stage":"COMPLETE","rollback_recommended":False})
                self.assertEqual(E.snapshot_tree(self.root),before);self.assertEqual(E.snapshot_tree(self.d_evidence),d_before)
                if fail_gate=="validate_runtime_inputs":
                    gates["controlled_distributions"].assert_not_called();gates["controlled_capabilities"].assert_not_called()


if __name__ == "__main__":
    unittest.main()
