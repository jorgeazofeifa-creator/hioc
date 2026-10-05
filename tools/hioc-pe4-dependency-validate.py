#!/usr/bin/env python3
"""PE-4 Action E: controlled, construction-read-only dependency validation."""
import argparse
import contextlib
import importlib.abc
import importlib.machinery
import importlib.util
import inspect
import json
import os
import pathlib
import re
import stat
import sys
import sysconfig

from hioc_pe4_runtime_common import *
from hioc_pe4_handoff_compatibility import (
    validate_commit_id, verify_current_consumer_source, verify_handoff_compatibility,
)

# Derived read-only from the frozen, SHA-256-verified 188095-byte wheel.
WHEEL_MEMBERS = {'websockets/__init__.py': '002d87abddae49cfd63a8f7fc6f213a46b2127b0f2d0c7799b6ff2c2c752b7f6',
 'websockets/__main__.py': 'c2ee4ddb093c9af060cafaf68219907f8a6b7b301ed3f8bea75db7555adec987',
 'websockets/auth.py': '53f2709a7e7d65143a11e7293af322cd0086fd96c0be051fd6293b85a6510b77',
 'websockets/cli.py': '4ed8d5f6d25a2383df73a4106a1c51de0c9a624dd6b3d16375dc5563a7e1ce9b',
 'websockets/client.py': '7e58c8e64e6843e49f9b9dcc0a8c9396bda316d38e22e3b5dc7f5b6eda413deb',
 'websockets/connection.py': '38b88c56435ddb9ffceac07c43b0ab0b00685f2f6703438281d80b440f16511f',
 'websockets/datastructures.py': 'c2f2026458e78df3512e1077fec107458b359bf62058a518eb132eba0e281362',
 'websockets/exceptions.py': '6e068c76a406199a2c00450b782077d175b6627c289966b773c60eac47de3a86',
 'websockets/frames.py': 'd1bb830c1861fdfebc412e9da880c4f078d6815848966fb5e567168b15fbb16c',
 'websockets/headers.py': 'c909cf963559c15d7f57ea4e49128d2c6feef36ef0142d61ef671c8a88dc43c3',
 'websockets/http.py': '4f5b4d2e66e41429de5d0eaa7a9066b155435f23fd8b9d34215cd3253781311e',
 'websockets/http11.py': 'dd9471fcb2d223ed7291077a2cd214fa6ad68a55bcbfff8e686e4b2c0bfb9bcf',
 'websockets/imports.py': '4ff07d4d4987a1c78a310f8f36985d410007d97771031c1240d790120a882e41',
 'websockets/protocol.py': 'bd3aa33c88361e63be6d2c6c733b849963313d3c4f5d4d61995523aa76a1578e',
 'websockets/proxy.py': 'a05adb118b5ab185aff960dc9e239b0fd9c1479439aa41e9c8254b9e0c7b58c4',
 'websockets/py.typed': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
 'websockets/server.py': '138496040f166519803a9b149bea02a9a701199adef5ed220e60c8adfa55db54',
 'websockets/speedups.c': 'bbf767711e0cdfc117e877bf7f36f54d8e83dc791eebb669a072cb85967486f4',
 'websockets/speedups.cpython-311-aarch64-linux-gnu.so': 'b786db296f7d0677ddeceb7efbe963bc316a094f36e12388caa1333763ca4c1b',
 'websockets/speedups.pyi': 'ba78ef04d83eb96e1cef3fbd396e16892cd993f407d9b2c472360032ea128012',
 'websockets/streams.py': 'a57aa06bbb6d8ee17a94285662258b49f525b77142690a445f569efe3bdc09e4',
 'websockets/typing.py': '03ac61e26eb9a51cca01bb8eb34905b8684be03588224a3ea694b8c2f2557344',
 'websockets/uri.py': 'd9f14cc3e01b289e47547342bb0d51c7532790290d591a688315a184cdf4114e',
 'websockets/utils.py': 'e7828a7fa8b79c7b391c6f8ebb950b5d26b67b1435d3d76cfb8bf75e7d2a955f',
 'websockets/version.py': '47be64ba8c0e0fd4cd3560252a22004093dfe6d5991c9ca9ad3bf719fa98446c',
 'websockets/asyncio/__init__.py': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
 'websockets/asyncio/async_timeout.py': '37ee8cb9bca26a887ae8f0171af0b3860c4233eed5d978919c7df65e2e89e931',
 'websockets/asyncio/client.py': '64333f1e162e25cc22f67bc5be02084decf3bd4ae50bddf6425c9fdd08f65a5a',
 'websockets/asyncio/compatibility.py': '8247a70c387335b9bafe25d5e4476f6efa7ab8765876b4ef18d8edf0ffc9b724',
 'websockets/asyncio/connection.py': 'de1dc9e77e8f15be28374e8eabae18a1f488d2ae0a2f508d6a054e5bb269d461',
 'websockets/asyncio/messages.py': 'bb633958a63dc4fcb0f06de72a85df74ee4ae3586b4e77f831d8b3547ce074ce',
 'websockets/asyncio/router.py': '4beebdbecccaf92a9409c65b5d73ce9eec7e787d9f4c7602d89361eed3ad9a60',
 'websockets/asyncio/server.py': 'c10f6805cd1604e2336d7283609f148574537a85eb49f2eee82582ad497ebdc9',
 'websockets/extensions/__init__.py': '42466cc5a255965552a75ba1743e6e3c689b75bc7fd3dd46ad555f4b92d7729c',
 'websockets/extensions/base.py': '24d7f2939e370bb56e3c7d103a86e2a8aa06af38c920b8deeaccf920bbce3e5e',
 'websockets/extensions/permessage_deflate.py': 'f3f5f972d1bf371f51e32cd81cddef0a8ed23f1a435ce6f927f1cc2a34933f47',
 'websockets/legacy/__init__.py': 'c10e7344810d1944bfe5e28d017f42444ef1d53c0a6a92a29ab40515637d4b1b',
 'websockets/legacy/auth.py': '0dc41c09279578ff7725c1fcbc5584d072092fe5fe7f6dcb6740ec2696afd52a',
 'websockets/legacy/client.py': 'fd57f11f3baf272b21168f188902d338388513a32f21f474b43accc19a20f9a5',
 'websockets/legacy/exceptions.py': '562123a684f4f5fcf1fd9a9fd1a3460d5b510cd8d768ec3481d0ad6b72e48c57',
 'websockets/legacy/framing.py': 'afd3f5c225efff55ee015430f1238f92e13d778799d2bfc9a30024cfdf96578c',
 'websockets/legacy/handshake.py': 'd8dcebe40376c6f0c2e4474d3fe901de539cac069436562e8fffa1aff8efee93',
 'websockets/legacy/http.py': '70e0909835a120a4269bc5161973d6ec20d9834df08e8802b1bd0b3fda1eb4d4',
 'websockets/legacy/protocol.py': '6a3b555c36fe9449bd04dd0d17788469323f6f5ab97c108a4c1f70bd4a063b16',
 'websockets/legacy/server.py': 'ee6c18fb20f4963345f77a0f62e993583ece2156c25ad6843b0d451490612003',
 'websockets/sync/__init__.py': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
 'websockets/sync/client.py': 'ff612bcadc357f77fd3bfbb68cbb52d68355e07b07522fe1de51af4fd6446834',
 'websockets/sync/connection.py': 'c155486ab837d3d79489d54ea6d2dfaf5ec9a2a923a6860cc6cbdf35e838f8b9',
 'websockets/sync/messages.py': 'c99575ce1634ed90f4bd11796f5c836bbba0d2b6c0e540ce082090996c0071db',
 'websockets/sync/router.py': '06a29200a35962d45688ec6897da987b27e0c9746b30d27a16b4d364b35c5cc8',
 'websockets/sync/server.py': 'b34ec734aff6b3590b37ad94a9cefbbaf343d33ec2d184d719e3ec0a206d5da1',
 'websockets/sync/utils.py': '4ed5be9dc605bc99a2496da03bcea7804d8156c9e705d2fee07f3c91634361b8'}
REVIEWED_MODULES = (
    "websockets", "websockets.imports", "websockets.version", "websockets.exceptions",
    "websockets.asyncio", "websockets.asyncio.client", "websockets.asyncio.compatibility",
    "websockets.asyncio.connection", "websockets.asyncio.messages", "websockets.client",
    "websockets.datastructures", "websockets.extensions", "websockets.extensions.base",
    "websockets.extensions.permessage_deflate", "websockets.frames", "websockets.headers",
    "websockets.http11", "websockets.protocol", "websockets.proxy", "websockets.streams",
    "websockets.typing", "websockets.uri", "websockets.utils", "websockets.speedups",
)
BASE_EXECUTABLE = pathlib.Path("/usr/bin/python3")
BASE_PATHS = ("/usr/lib/python311.zip", "/usr/lib/python3.11",
              "/usr/lib/python3.11/lib-dynload")
NATIVE_MEMBER = "websockets/speedups.cpython-311-aarch64-linux-gnu.so"


def reject(code="CONTROLLED_RUNTIME_INVALID", stage="CONTROLLED_STARTUP"):
    raise Failure(code, stage)


def token(info):
    # Deliberately exclude atime. Include nanosecond mtime/ctime and identity.
    return (info.st_dev, info.st_ino, info.st_uid, info.st_gid, info.st_mode,
            info.st_nlink, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def read_regular(path):
    before = os.lstat(path)
    if not stat.S_ISREG(before.st_mode):
        reject("CONTROLLED_FILE_INVALID")
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
                 | getattr(os, "O_BINARY", 0))
    try:
        opened = token(os.fstat(fd))
        # Windows path stat adds extension-based execute bits and creation ctime.
        expected = token(before)
        if os.name == "nt":
            same = (opened[:4] + (stat.S_IFMT(opened[4]),) + opened[5:-1]
                    == expected[:4] + (stat.S_IFMT(expected[4]),) + expected[5:-1])
        else:
            same = opened == expected
        if not same:
            reject("CONTROLLED_FILE_CHANGED")
        chunks = []
        while True:
            part = os.read(fd, 1024 * 1024)
            if not part:
                break
            chunks.append(part)
        if token(os.fstat(fd)) != opened:
            reject("CONTROLLED_FILE_CHANGED")
    finally:
        os.close(fd)
    if token(os.lstat(path)) != token(before):
        reject("CONTROLLED_FILE_CHANGED")
    return b"".join(chunks)


def snapshot_tree(path):
    result = {}
    def visit(current, relative):
        before = os.lstat(current)
        identity = token(before)
        if stat.S_ISDIR(before.st_mode):
            names = sorted(os.listdir(current))
            result[relative] = (identity, "directory")
            for name in names:
                visit(current / name, relative + "/" + name)
            if names != sorted(os.listdir(current)):
                reject("CONSTRUCTION_CHANGED", "CONSTRUCTION_IMMUTABILITY")
        elif stat.S_ISREG(before.st_mode):
            result[relative] = (identity, hashlib.sha256(read_regular(current)).hexdigest())
        elif stat.S_ISLNK(before.st_mode):
            result[relative] = (identity, os.readlink(current))
        else:
            reject("CONTROLLED_FILE_INVALID")
        if token(os.lstat(current)) != identity:
            reject("CONSTRUCTION_CHANGED", "CONSTRUCTION_IMMUTABILITY")
    visit(pathlib.Path(path), ".")
    return result


def assert_unchanged(path, baseline):
    if snapshot_tree(path) != baseline:
        reject("CONSTRUCTION_CHANGED", "CONSTRUCTION_IMMUTABILITY")


def check_owned_chain(root, path):
    root, path = pathlib.Path(root), pathlib.Path(path)
    relative = path.relative_to(root)
    expected = os.lstat(root)
    current = root
    for part in relative.parts:
        current = current / part
        info = os.lstat(current)
        if stat.S_ISLNK(info.st_mode) or not (stat.S_ISREG(info.st_mode) or stat.S_ISDIR(info.st_mode)):
            reject("CONTROLLED_FILE_INVALID")
        if os.name == "posix" and (info.st_uid != expected.st_uid or info.st_gid != expected.st_gid
                                   or stat.S_IMODE(info.st_mode) & 0o022):
            reject("CONTROLLED_FILE_INVALID")


def reject_startup_overrides(executables, libraries):
    for executable in executables:
        executable = pathlib.Path(executable)
        candidates = [pathlib.Path(str(executable) + "._pth"),
                      executable.parent / "pybuilddir.txt",
                      executable.parent / "Modules/Setup.local",
                      executable.parent / "Lib/os.py",
                      executable.parent / "Lib/os.pyc"]
        if executable.suffix.lower() == ".exe":
            candidates.append(executable.with_suffix("._pth"))
        for candidate in candidates:
            if os.path.lexists(candidate):
                reject("STARTUP_OVERRIDE_REJECTED")
    for library in libraries:
        library = pathlib.Path(library)
        candidates = [pathlib.Path(str(library) + "._pth")]
        if library.suffix.lower() == ".dll":
            candidates.append(library.with_suffix("._pth"))
        for candidate in candidates:
            if os.path.lexists(candidate):
                reject("STARTUP_OVERRIDE_REJECTED")


def parse_venv_configuration(raw, base_executable):
    try:
        text = raw.decode("utf-8")
    except UnicodeError:
        reject("VENV_PROVENANCE_INVALID")
    if len(raw) > 65536 or "\x00" in text:
        reject("VENV_PROVENANCE_INVALID")
    values = {}
    allowed = {"home", "include-system-site-packages", "version", "executable", "command", "prompt"}
    for line in text.splitlines():
        if not line.strip():
            continue
        key, separator, value = line.partition("=")
        key, value = key.strip().lower(), value.strip()
        if not separator or key not in allowed or key in values or not value or len(value) > 4096:
            reject("VENV_PROVENANCE_INVALID")
        values[key] = value
    if (not {"home", "include-system-site-packages", "version", "executable", "command"} <= values.keys()
            or values["home"] != "/usr/bin"
            or values["include-system-site-packages"].lower() != "false"
            or values["version"] != "3.11.2"
            or os.path.realpath(values["executable"]) != os.path.realpath(base_executable)):
        reject("VENV_PROVENANCE_INVALID")
    return values


def member_bytes(site, member):
    path = pathlib.Path(site) / member
    check_owned_chain(site, path)
    raw = read_regular(path)
    if hashlib.sha256(raw).hexdigest() != WHEEL_MEMBERS[member]:
        reject("GOVERNED_PACKAGE_CHANGED", "PACKAGE_PROVENANCE")
    return raw


def validate_members(site):
    package = pathlib.Path(site) / "websockets"
    actual = set()
    for directory, dirs, files in os.walk(package, followlinks=False):
        for name in dirs + files:
            path = pathlib.Path(directory) / name
            check_owned_chain(site, path)
        for name in files:
            path = pathlib.Path(directory) / name
            member = path.relative_to(site).as_posix()
            # Cache bytes never become authoritative or enter the loader.
            if "__pycache__" in path.relative_to(package).parts and name.endswith(".pyc"):
                continue
            actual.add(member)
    if actual != set(WHEEL_MEMBERS):
        reject("GOVERNED_PACKAGE_MEMBERS_INVALID", "PACKAGE_PROVENANCE")
    for member in WHEEL_MEMBERS:
        member_bytes(site, member)


def validate_runtime_inputs(root):
    construction = pathlib.Path(root.path)
    interpreter = construction / "bin/python"
    site = construction / "lib/python3.11/site-packages"
    cfg = construction / "pyvenv.cfg"
    base = BASE_EXECUTABLE
    validate_venv_symlinks(root)
    for path in (interpreter, site, cfg):
        check_owned_chain(construction, path)
    if not stat.S_ISDIR(os.lstat(site).st_mode):
        reject("VENV_PROVENANCE_INVALID")
    if os.path.lexists(construction / "bin/pyvenv.cfg"):
        reject("STARTUP_OVERRIDE_REJECTED")
    parse_venv_configuration(read_regular(cfg), base)
    binaries = [construction / "bin" / name for name in ("python", "python3", "python3.11")]
    binaries += [base, pathlib.Path(os.path.realpath(base))]
    libraries = []
    for directory in ("/usr/lib", "/usr/lib/aarch64-linux-gnu", "/lib/aarch64-linux-gnu"):
        libraries.extend(pathlib.Path(directory).glob("libpython3.11*"))
    reject_startup_overrides(binaries, libraries)
    if read_regular(interpreter) != read_regular(pathlib.Path(os.path.realpath(base))):
        reject("VENV_PROVENANCE_INVALID")
    validate_members(site)
    info = os.stat(interpreter)
    return {"paths": list(BASE_PATHS), "prefix": "/usr", "version": [3, 11, 2],
            "soabi": "cpython-311-aarch64-linux-gnu", "interpreter": str(interpreter),
            "interpreter_identity": [info.st_dev, info.st_ino],
            "base": os.path.realpath(base), "site": str(site)}


def validate_startup(policy):
    if (list(sys.path) != policy["paths"] or not sys.flags.isolated or not sys.flags.no_site
            or not sys.flags.no_user_site or not sys.dont_write_bytecode
            or not sys.flags.ignore_environment or not sys.flags.safe_path
            or "site" in sys.modules):
        reject("CONTROLLED_STARTUP_INVALID")
    if (sys.implementation.name != "cpython" or list(sys.version_info[:3]) != policy["version"]
            or sys.prefix != policy["prefix"] or sys.base_prefix != policy["prefix"]
            or sys.exec_prefix != policy["prefix"] or sys.base_exec_prefix != policy["prefix"]):
        reject("VENV_PROVENANCE_INVALID")
    expected_site = pathlib.Path(policy["interpreter"]).parent.parent / "lib/python3.11/site-packages"
    if os.path.normpath(policy["site"]) != os.path.normpath(str(expected_site)):
        reject("VENV_PROVENANCE_INVALID")
    info = os.stat(sys.executable)
    selected = os.stat(policy["interpreter"])
    if ([selected.st_dev, selected.st_ino] != policy["interpreter_identity"]):
        reject("VENV_PROVENANCE_INVALID")
    if ([info.st_dev, info.st_ino] != policy["interpreter_identity"]
            or os.path.realpath(sys._base_executable) != policy["base"]
            or sysconfig.get_config_var("SOABI") != policy["soabi"]):
        reject("VENV_PROVENANCE_INVALID")
    if sys.meta_path != [importlib.machinery.BuiltinImporter,
                         importlib.machinery.FrozenImporter, importlib.machinery.PathFinder]:
        reject("CONTROLLED_FINDER_INVALID")
    for name, module in tuple(sys.modules.items()):
        origin = getattr(module, "__file__", None)
        if origin and not any(origin.startswith(root.rstrip(os.sep) + os.sep) for root in policy["paths"]):
            reject("CONTROLLED_IMPORT_INVALID")
    for path in policy["paths"]:
        if not os.path.isabs(path) or "site-packages" in path or "dist-packages" in path:
            reject("CONTROLLED_PATH_INVALID")
        current = pathlib.Path(path)
        while current != current.parent:
            if os.path.lexists(current):
                info = os.lstat(current)
                if stat.S_ISLNK(info.st_mode) or (os.name == "posix" and
                    (info.st_uid != 0 or stat.S_IMODE(info.st_mode) & 0o022)):
                    reject("CONTROLLED_PATH_INVALID")
            current = current.parent


def validate_distributions(lines):
    allowed = {"pip", "setuptools", "websockets"}
    pairs = [line.split("==", 1) for line in lines if line.count("==") == 1]
    parsed = [pair[0] for pair in pairs]
    if (len(pairs) != len(lines) or "websockets==16.1.1" not in lines
            or set(parsed) - allowed or parsed.count("websockets") != 1
            or parsed.count("pip") != 1 or parsed.count("setuptools") > 1
            or len(parsed) != len(set(parsed))
            or any(not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9.!+_-]{0,63}", version)
                   for _, version in pairs)):
        reject("INSTALLED_DISTRIBUTION_SET_INVALID", "DEPENDENCY_IDENTITY")
    return dict(pairs)


class VerifiedSourceLoader(importlib.abc.Loader):
    def __init__(self, site, member, package):
        self.site, self.member, self.package = site, member, package

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        path = pathlib.Path(self.site) / self.member
        raw = member_bytes(self.site, self.member)
        module.__file__ = str(path)
        module.__cached__ = None
        if self.package:
            module.__path__ = [str(path.parent)]
        exec(compile(raw, str(path), "exec", dont_inherit=True), module.__dict__)


class VerifiedNativeLoader(importlib.machinery.ExtensionFileLoader):
    def __init__(self, name, site):
        self.site = site
        super().__init__(name, str(pathlib.Path(site) / NATIVE_MEMBER))

    def create_module(self, spec):
        member_bytes(self.site, NATIVE_MEMBER)
        return super().create_module(spec)

    def exec_module(self, module):
        member_bytes(self.site, NATIVE_MEMBER)
        super().exec_module(module)


class RestrictedFinder(importlib.abc.MetaPathFinder):
    def __init__(self, policy):
        self.policy = policy

    def find_spec(self, fullname, path=None, target=None):
        top = fullname.partition(".")[0]
        if top == "websockets":
            if fullname not in REVIEWED_MODULES:
                raise ModuleNotFoundError("unreviewed package module", name=fullname)
            if fullname == "websockets.speedups":
                loader = VerifiedNativeLoader(fullname, self.policy["site"])
                return importlib.util.spec_from_file_location(fullname, loader.path, loader=loader)
            prefix = fullname.replace(".", "/")
            package = prefix + "/__init__.py" in WHEEL_MEMBERS
            member = prefix + ("/__init__.py" if package else ".py")
            loader = VerifiedSourceLoader(self.policy["site"], member, package)
            return importlib.util.spec_from_loader(fullname, loader, is_package=package)
        if top not in sys.stdlib_module_names:
            raise ModuleNotFoundError("unrelated package blocked", name=fullname)
        # Resolve only through unchanged standard machinery and trusted roots.
        for finder in (importlib.machinery.BuiltinImporter, importlib.machinery.FrozenImporter):
            spec = finder.find_spec(fullname, path)
            if spec is not None:
                return spec
        spec = importlib.machinery.PathFinder.find_spec(fullname, self.policy["paths"] if path is None else path)
        if spec is None:
            raise ModuleNotFoundError("unavailable standard-library module", name=fullname)
        origin = spec.origin
        if not origin or not any(origin.startswith(root.rstrip(os.sep) + os.sep)
                                 for root in self.policy["paths"]):
            reject("CONTROLLED_IMPORT_INVALID")
        return spec


def capability_probe(policy):
    validate_members(policy["site"])
    sys.path.append(policy["site"])
    finder = RestrictedFinder(policy)
    sys.meta_path.insert(0, finder)
    import websockets
    from websockets.asyncio.client import connect
    from websockets.exceptions import InvalidStatus, PayloadTooBig
    from websockets.datastructures import Headers
    from websockets.http11 import Response
    if (websockets.__version__ != "16.1.1" or connect.__module__ != "websockets.asyncio.client"
            or websockets.connect is not connect):
        reject("CAPABILITY_INVALID", "CAPABILITY_VALIDATION")
    parameters = inspect.signature(connect).parameters
    if (not {"max_size", "proxy", "open_timeout", "close_timeout"} <= set(parameters)
            or not any(p.kind is inspect.Parameter.VAR_KEYWORD for p in parameters.values())
            or not issubclass(InvalidStatus, Exception) or not issubclass(PayloadTooBig, Exception)):
        reject("CAPABILITY_INVALID", "CAPABILITY_VALIDATION")
    response = Response(302, "Found", Headers({"Location": "ws://192.168.100.251:8123/api/websocket"}))
    obj = object.__new__(connect)
    obj.uri = "ws://192.168.100.251:8123/api/websocket"
    obj.connection_kwargs = {"sock": object()}
    refusal = obj.process_redirect(InvalidStatus(response))
    if not isinstance(refusal, ValueError) or "preexisting socket" not in str(refusal):
        reject("CAPABILITY_INVALID", "CAPABILITY_VALIDATION")
    if sys.path != policy["paths"] + [policy["site"]] or sys.meta_path != [finder,
            importlib.machinery.BuiltinImporter, importlib.machinery.FrozenImporter,
            importlib.machinery.PathFinder]:
        reject("CONTROLLED_PATH_INVALID")
    for name, module in tuple(sys.modules.items()):
        if name.startswith("websockets"):
            if name not in REVIEWED_MODULES or not getattr(module, "__file__", "").startswith(
                    policy["site"] + os.sep + "websockets" + os.sep):
                reject("CONTROLLED_IMPORT_INVALID")
    print("CAPABILITY_VALIDATION=PASS")


def child_script(policy, capability=False):
    # Check flags/path before importing any file-backed probe dependency.
    prelude = "import sys\nPOLICY=" + repr(policy) + "\n"
    prelude += ("if sys.path != POLICY['paths'] or not sys.flags.isolated or not sys.flags.no_site "
                "or not sys.flags.no_user_site or not sys.dont_write_bytecode or 'site' in sys.modules: "
                "raise RuntimeError('CONTROLLED_STARTUP_INVALID')\n")
    prelude += ("import os,pathlib,stat,hashlib,json,re,sysconfig,inspect\n"
                "import importlib.abc,importlib.machinery,importlib.util\n"
                "class Failure(RuntimeError):\n"
                " def __init__(self,code,stage): super().__init__(code)\n")
    prelude += "WHEEL_MEMBERS=" + repr(WHEEL_MEMBERS) + "\n"
    prelude += "REVIEWED_MODULES=" + repr(REVIEWED_MODULES) + "\nNATIVE_MEMBER=" + repr(NATIVE_MEMBER) + "\n"
    definitions = (reject, token, read_regular, check_owned_chain, member_bytes,
                   validate_members, validate_startup, VerifiedSourceLoader,
                   VerifiedNativeLoader, RestrictedFinder, capability_probe)
    prelude += "\n".join(inspect.getsource(item) for item in definitions)
    prelude += "\nvalidate_startup(POLICY)\n"
    if capability:
        return prelude + "capability_probe(POLICY)\n"
    return prelude + ("import importlib.metadata as metadata\n"
        "print('\\n'.join(sorted(d.metadata['Name'].lower()+'=='+d.version "
        "for d in metadata.distributions(path=[POLICY['site']]))))\n"
        "if sys.path != POLICY['paths']: raise RuntimeError('CONTROLLED_PATH_INVALID')\n")



def run(command, stage, *, cwd=None, pass_fds=(), env=None):
    """E-only child runner: finite time and at most 64 KiB per output stream."""
    process = None
    threads = []
    output = [bytearray(), bytearray()]
    failed = threading.Event()
    try:
        process = subprocess.Popen(command, stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd,
            pass_fds=pass_fds, env=env)
        def consume(stream, index):
            try:
                while True:
                    block = stream.read(8192)
                    if not block:
                        break
                    if len(output[index]) + len(block) > 65536:
                        failed.set()
                        process.kill()
                        break
                    output[index].extend(block)
            except OSError:
                failed.set()
        for index, stream in enumerate((process.stdout, process.stderr)):
            thread = threading.Thread(target=consume, args=(stream, index), daemon=True)
            thread.start()
            threads.append(thread)
        process.wait(timeout=60)
        for thread in threads:
            thread.join(timeout=5)
        if failed.is_set() or any(thread.is_alive() for thread in threads):
            reject("COMMAND_OUTPUT_LIMIT", stage)
        if process.returncode != 0:
            reject("COMMAND_FAILED", stage)
        return subprocess.CompletedProcess(command, process.returncode,
            output[0].decode("utf-8", "strict").replace("\r\n", "\n"),
            output[1].decode("utf-8", "strict").replace("\r\n", "\n"))
    except (OSError, subprocess.SubprocessError, UnicodeError):
        reject("COMMAND_INVOCATION_FAILED", stage)
    finally:
        if process is not None:
            if process.poll() is None:
                process.kill()
                process.wait()
            for thread in threads:
                thread.join(timeout=5)
            process.stdout.close()
            process.stderr.close()


def controlled_distributions(root, environment, policy):
    result = run(["./bin/python", "-I", "-B", "-S", "-c", child_script(policy)],
                 "DEPENDENCY_IDENTITY", cwd=f"/proc/self/fd/{root.fd}",
                 pass_fds=(root.fd,), env=environment)
    if len(result.stdout) > 65536:
        reject("INSTALLED_DISTRIBUTION_SET_INVALID", "DEPENDENCY_IDENTITY")
    return validate_distributions(result.stdout.splitlines())


def controlled_capabilities(root, environment, policy):
    result = run(["./bin/python", "-I", "-B", "-S", "-c", child_script(policy, True)],
                 "CAPABILITY_VALIDATION", cwd=f"/proc/self/fd/{root.fd}",
                 pass_fds=(root.fd,), env=environment)
    if result.stdout != "CAPABILITY_VALIDATION=PASS\n":
        reject("CAPABILITY_INVALID", "CAPABILITY_VALIDATION")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--governance-commit",required=True)
    parser.add_argument("--action-d-governance-commit",required=True)
    parser.add_argument("--construction-directory",required=True)
    a = parser.parse_args()
    validate_commit_id(a.governance_commit, "SOURCE_IDENTITY")
    validate_commit_id(a.action_d_governance_commit, "HANDOFF_COMPATIBILITY")
    verify_pi3()
    verify_current_consumer_source(SOURCE, a.governance_commit)
    verify_handoff_compatibility(SOURCE, a.action_d_governance_commit, a.governance_commit)
    path = validate_construction(a.construction_directory)
    with contextlib.ExitStack() as stack:
        def retain(directory):
            stack.callback(directory.close)
            return directory
        parent = retain(open_trusted_owned_parent(RUNTIME_ROOT.parent, "ACTION_D_ELIGIBILITY"))
        runtime = retain(open_owned_directory(RUNTIME_ROOT, 0o750, "ACTION_D_ELIGIBILITY", parent=parent))
        environments = retain(open_owned_directory(ENVIRONMENT_ROOT, 0o750, "ACTION_D_ELIGIBILITY", parent=runtime))
        root = retain(open_owned_directory(path, 0o750, "ACTION_D_ELIGIBILITY", parent=environments))
        marker = validate_action_d_eligibility(root,a.action_d_governance_commit)
        # The common exact_distribution_set is deliberately not used by E.
        # Both E-local probes enforce controlled startup after producer eligibility.
        d_evidence = pathlib.Path(marker["evidence_directory"])
        baseline, d_baseline = snapshot_tree(path), snapshot_tree(d_evidence)
        try:
            policy = validate_runtime_inputs(root)
            environment = action_d_subprocess_environment()
            controlled_distributions(root, environment, policy)
            controlled_capabilities(root, environment, policy)
            assert_unchanged(path, baseline)
            assert_unchanged(d_evidence, d_baseline)
            evidence = evidence_directory("hioc-pe4-dependency-validate-")
            write_evidence(evidence, "PE-4.0B.2a-E", {
                "ACTION": "DEPENDENCY_VALIDATION", "ENVIRONMENT_IDENTITY": VERSIONED_NAME,
                "INSTALLED_VERSION": "16.1.1", "CAPABILITY_VALIDATION": "PASS"}, "PASS")
        finally:
            revalidate_owned_directory(root, "CONSTRUCTION_IMMUTABILITY")
            assert_unchanged(path, baseline)
            assert_unchanged(d_evidence, d_baseline)
    terminal("PASS", "NONE", "COMPLETE", False, evidence)
    print(f"CONSTRUCTION_DIRECTORY={path}")


if __name__ == "__main__":
    try:
        main()
    except Failure as exc:
        terminal("FAIL", exc.code, exc.stage, False)
        raise SystemExit(1)
    except Exception:
        terminal("FAIL", "UNEXPECTED_ERROR", "UNEXPECTED", False)
        raise SystemExit(1)
