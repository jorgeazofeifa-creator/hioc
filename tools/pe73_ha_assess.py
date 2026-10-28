"""Bounded HA OS read-only native identity qualification, no arguments/prompts.

Default execution uses fixed local Docker metadata reads and kernel/descriptor
metadata. No HA import/API, container exec, credentials or .storage contents.
The earlier assess(config, package) source-only fixture remains available for its
historical tests; it is not the operator entry or a native admission mechanism.
"""
import ast
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import errno
import re
import socket
import subprocess
import ctypes
import io
import tarfile


def metadata(path):
    """No following symlinks, no implicit ownership correction."""
    for parent in (path, *path.parents):
        info = parent.lstat()
        if stat.S_ISLNK(info.st_mode):
            raise ValueError('SYMLINK_PATH')
    info = path.lstat()
    return {'device':info.st_dev, 'inode':info.st_ino, 'uid':info.st_uid, 'gid':info.st_gid,
            'mode':format(stat.S_IMODE(info.st_mode), '04o'), 'links':info.st_nlink,
            'type':'DIRECTORY' if stat.S_ISDIR(info.st_mode) else 'REGULAR' if stat.S_ISREG(info.st_mode) else 'OTHER',
            'mtime_ns':info.st_mtime_ns, 'ctime_ns':info.st_ctime_ns}


def assess(config, package):
    if not config.is_absolute() or not package.is_absolute() or '..' in config.parts or '..' in package.parts:
        raise ValueError('ABSOLUTE_OBSERVED_ROOTS_REQUIRED')
    result = {'RESULT':'READ_ONLY_ASSESSMENT', 'authority':'OPERATOR_SUPPLIED_WHEN_RETURNED',
              'uid':os.getuid() if hasattr(os,'getuid') else None,
              'gid':os.getgid() if hasattr(os,'getgid') else None,
              'host':__import__('socket').gethostname(), 'roots':{}, 'objects':{}, 'source_capabilities':{},
              'live_api_capabilities':'NOT_ESTABLISHED_BY_STATIC_SOURCE',
              'production_authorized':False, 'files_modified':False, 'STOP_REQUIRED':True}
    result['roots'] = {'config':metadata(config), 'package':metadata(package)}
    allowed = ('configuration.yaml','custom_components','custom_components/hioc_operator',
               'custom_components/hioc_operator/__init__.py','custom_components/hioc_operator/manifest.json',
               'custom_components/hioc_operator/services.yaml','www','www/hioc-asset-editor.js','backups',
               '.storage/lovelace',' .storage/lovelace_resources')
    for relative in allowed:
        relative = relative.strip()
        try:
            result['objects'][relative] = metadata(config/relative)
        except FileNotFoundError:
            result['objects'][relative] = {'exists':False}
    # Public installed source only; compile/AST inspection does not execute HA.
    for relative in ('components/lovelace/websocket.py','components/lovelace/resources.py',
                     'components/lovelace/__init__.py','components/frontend/__init__.py',
                     'components/websocket_api/connection.py','core.py'):
        target = package/relative
        info = metadata(target)
        if info['type'] != 'REGULAR' or info['links'] != 1:
            raise ValueError('UNSAFE_SOURCE_TYPE')
        with target.open('rb') as stream:
            raw = stream.read(2097153)
        if len(raw) > 2097152 or metadata(target) != info:
            raise ValueError('SOURCE_DRIFT_OR_LIMIT')
        tree = ast.parse(raw)
        names = {n.name for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
        constants = {n.value for n in ast.walk(tree) if isinstance(n,ast.Constant) and isinstance(n.value,str)}
        result['source_capabilities'][relative] = {'sha256':hashlib.sha256(raw).hexdigest(), 'metadata':info,
            'commands':[x for x in ('lovelace/config','lovelace/config/save','lovelace/info','lovelace/resources') if x in constants],
            'symbols':[x for x in ('current_connection','SupportsResponse','ResourceStorageCollection',
                'ResourceStorageCollectionWebsocket','websocket_lovelace_save_config') if x in names],
            'resource_load_may_import_legacy_configuration':relative.endswith('resources.py') and 'CONF_RESOURCES' in raw.decode()}
    return result


class QualificationError(ValueError):
    pass


def require(value, code):
    if not value:
        raise QualificationError(code)


def anchor(info):
    return {'device':info.st_dev, 'inode':info.st_ino, 'uid':info.st_uid,
            'gid':info.st_gid, 'mode':stat.S_IMODE(info.st_mode)}


def directory_chain(root, core_uid, core_gid, *, core_access=True):
    """Read-only descriptor proof; no pathname fallback or mutation experiment."""
    result = {}
    fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
    held = [fd]
    links = []
    try:
        parts = [('/', None)] + [(part, part) for part in Path(root).parts[1:]]
        absolute = ''
        for label, part in parts:
            if part is not None:
                child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=fd)
                links.append((fd, part, child));held.append(child);fd=child
                absolute += '/' + part
            info = os.fstat(fd)
            require(stat.S_ISDIR(info.st_mode) and info.st_uid in (0,core_uid)
                    and not stat.S_IMODE(info.st_mode) & 0o7022, 'UNSAFE_DIRECTORY')
            # Do not assume that root or capabilities bypass an unreadable parent.
            shift = 6 if info.st_uid == core_uid else 3 if info.st_gid == core_gid else 0
            require(not core_access or (stat.S_IMODE(info.st_mode) >> shift) & 1, 'CORE_TRAVERSAL_NOT_ESTABLISHED')
            for name in ('system.posix_acl_access','system.posix_acl_default'):
                try:
                    os.getxattr(fd,name)
                except OSError as error:
                    require(error.errno == errno.ENODATA, 'ACL_STATUS_UNKNOWN')
                else:
                    raise QualificationError('ACL_PRESENT')
            result[absolute or '/'] = anchor(info)
        for parent,name,child in links:
            require(anchor(os.stat(name,dir_fd=parent,follow_symlinks=False)) == anchor(os.fstat(child)), 'ANCESTOR_DRIFT')
        return result
    finally:
        for descriptor in reversed(held):
            os.close(descriptor)


def bind_mounts(terminal, core, root_metadata):
    """Exact same bind source and identity mapping, never string-prefix trust."""
    require(terminal['id'] != core['id'], 'DISTINCT_CONTAINERS_REQUIRED')
    for value in (terminal,core):
        require(value['running'] is True and value['userns'] in ('','host'), 'USER_NAMESPACE_UNSUPPORTED')
        require(type(value['mounts']) is list, 'MOUNTS_INVALID')
    mounts = [m for m in core['mounts'] if m.get('Destination') == '/config']
    require(len(mounts) == 1, 'CORE_CONFIG_MOUNT_NOT_UNIQUE')
    selected = mounts[0]
    require(selected.get('Type') == 'bind' and selected.get('RW') is True
            and type(selected.get('Source')) is str and selected['Source'].startswith('/')
            and '..' not in Path(selected['Source']).parts, 'CORE_CONFIG_BIND_REQUIRED')
    require(not any(m.get('Destination','').startswith('/config/') for m in core['mounts']), 'NESTED_CORE_CONFIG_MOUNT')
    roots = []
    for mount in terminal['mounts']:
        dest = mount.get('Destination')
        if dest in ('/config','/homeassistant') and mount.get('Source') == selected['Source']:
            require(mount.get('Type') == 'bind' and mount.get('RW') is True
                    and 'idmap' not in str(mount.get('Mode','')).lower(), 'TERMINAL_BIND_UNSUPPORTED')
            require(not any(m.get('Destination','').startswith(dest+'/') for m in terminal['mounts']), 'NESTED_TERMINAL_CONFIG_MOUNT')
            roots.append(dest)
    require(bool(roots), 'TERMINAL_CORE_CONFIG_BINDING_UNAVAILABLE')
    identities = [root_metadata(root) for root in roots]
    require(all((x['device'],x['inode']) == (identities[0]['device'],identities[0]['inode']) for x in identities), 'CONFIG_ALIAS_IDENTITY_CONFLICT')
    # Prefer the explicit HA configuration mount; never accept an arbitrary root.
    return '/homeassistant' if '/homeassistant' in roots else '/config'


def core_identity(top):
    """Only PID/UID/GID/comm, no command arguments, environment or credentials."""
    rows = top.strip().splitlines()
    require(bool(rows) and rows[0].split() == ['PID','UID','GID','COMMAND'], 'CORE_PROCESS_FORMAT_UNKNOWN')
    found=[]
    for row in rows[1:]:
        cols=row.split()
        require(len(cols)==4, 'CORE_PROCESS_FORMAT_UNKNOWN')
        if re.fullmatch(r'python(?:3(?:\.\d+)?)?',cols[3]):
            require(all(x.isdecimal() for x in cols[:3]), 'CORE_IDENTITY_NOT_NUMERIC')
            found.append([int(x) for x in cols[:3]])
    require(len(found)==1, 'CORE_PYTHON_PROCESS_NOT_UNIQUE')
    return {'pid':found[0][0], 'uid':found[0][1], 'gid':found[0][2]}


class NativeProbe:
    """Fixed local Docker reads and kernel metadata. Never exec, HA API or secrets."""
    def docker(self,*args):
        completed=subprocess.run(['/usr/local/bin/docker','--config','/proc/pe73-no-client-config',
            '--host','unix:///var/run/docker.sock',*args],stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,timeout=20,
            env={'PATH':'/usr/local/bin:/usr/bin:/bin','LANG':'C','LC_ALL':'C'})
        require(completed.returncode==0 and len(completed.stdout)<=1048576, 'DOCKER_METADATA_UNAVAILABLE')
        return completed.stdout.decode('utf-8')

    def container(self,identity):
        require(re.fullmatch('[0-9a-f]{12,64}',identity), 'CONTAINER_ID_INVALID')
        template='{"id":{{json .Id}},"image":{{json .Image}},"running":{{json .State.Running}},"pid":{{json .State.Pid}},"userns":{{json .HostConfig.UsernsMode}},"pidmode":{{json .HostConfig.PidMode}},"workdir":{{json .Config.WorkingDir}},"mounts":{{json .Mounts}}}'
        value=json.loads(self.docker('container','inspect','--format',template,identity))
        value['mounts']=[m for m in value['mounts'] if any(m.get('Destination')==p or m.get('Destination','').startswith(p+'/') for p in ('/config','/homeassistant'))]
        return value

    def process_birth(self, identity, core_id):
        require(type(core_id) is str and re.fullmatch('[0-9a-f]{64}',core_id), 'CORE_CONTAINER_ID_REQUIRED')
        base=Path('/proc')/str(identity['pid'])
        try:
            raw=(base/'stat').read_text()
            ticks=int(raw.rsplit(')',1)[1].split()[19])
            fields={line.split(':',1)[0]:line.split(':',1)[1].split() for line in (base/'status').read_text().splitlines() if line.startswith(('Uid:','Gid:'))}
            groups=set(re.findall(r'(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])',(base/'cgroup').read_text()))
            namespace=os.readlink(base/'ns/user')
            own_namespace=os.readlink('/proc/self/ns/user')
        except OSError:
            raise QualificationError('CORE_PROCESS_FILESYSTEM_IDENTITY_NOT_OBSERVABLE') from None
        require(groups=={core_id}, 'CORE_PROCESS_CONTAINER_BINDING_NOT_ESTABLISHED')
        require(list(map(int,fields['Uid']))==[identity['uid']]*4 and list(map(int,fields['Gid']))==[identity['gid']]*4, 'CORE_PROCESS_CREDENTIAL_DRIFT')
        require(namespace==own_namespace, 'CORE_USER_NAMESPACE_NOT_IDENTICAL')
        return {'pid':identity['pid'],'start_ticks':ticks,'user_namespace':namespace,'container_id':core_id}

    def core_filesystem(self,terminal,identity,root,directories,core_id=None):
        """Source strings alone are insufficient. Compare actual Core descriptor nodes.

        Uses existing observable proc objects, never assumes host PID configuration.
        Numeric PID is bound to the exact Core container cgroup, credentials, user
        namespace and process birth. No metadata-only fallback, exec, setns or
        container reconfiguration. Inaccessible or hidden identity proof stops.
        """
        pid=identity['pid'];base=Path('/proc')/str(pid)
        def birth():return self.process_birth(identity,core_id)
        before=birth();held=[]
        try:
            fd=os.open(base/'root',os.O_RDONLY|os.O_DIRECTORY|os.O_CLOEXEC);held.append(fd)
            config=os.open('config',os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC,dir_fd=fd);held.append(config)
            anchors={}
            for relative in ('','custom_components','custom_components/hioc_operator','www','backups'):
                current=config
                expected=directories.get(str(Path(root)/relative))
                try:
                    for part in Path(relative).parts:
                        current=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC,dir_fd=current);held.append(current)
                except FileNotFoundError:
                    require(expected is None and relative in ('custom_components/hioc_operator','backups'), 'CORE_VISIBLE_DIRECTORY_IDENTITY_CONFLICT')
                    anchors[relative]=None
                    continue
                value=anchor(os.fstat(current))
                require(value==expected, 'CORE_VISIBLE_DIRECTORY_IDENTITY_CONFLICT')
                anchors[relative]=value
            require(before==birth(), 'CORE_PROCESS_REPLACED_DURING_QUALIFICATION')
            return {'process_birth':before,'anchors':anchors}
        finally:
            for fd in reversed(held):os.close(fd)

    def public_capabilities(self, core):
        """Public installed source only, memory tar stream, no extract or HA import."""
        base=core['workdir']
        require(type(base) is str and Path(base).is_absolute() and '..' not in Path(base).parts, 'CORE_PUBLIC_SOURCE_UNAVAILABLE')
        result={}
        for relative in ('components/lovelace/websocket.py','components/lovelace/resources.py',
                         'components/lovelace/const.py','components/websocket_api/connection.py',
                         'components/websocket_api/commands.py','components/frontend/__init__.py','core.py'):
            try:
                completed=subprocess.run(['/usr/local/bin/docker','--config','/proc/pe73-no-client-config',
                    '--host','unix:///var/run/docker.sock','container','cp',
                    core['id']+':'+str(Path(base)/'homeassistant'/relative),'-'],
                    stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,timeout=20,
                    env={'PATH':'/usr/local/bin:/usr/bin:/bin','LANG':'C','LC_ALL':'C'})
                require(completed.returncode==0 and len(completed.stdout)<=4194304, 'PUBLIC_SOURCE_LIMIT')
                with tarfile.open(fileobj=io.BytesIO(completed.stdout),mode='r:') as archive:
                    members=archive.getmembers();files=[x for x in members if x.isfile()]
                    require(len(files)==1 and files[0].size<=2097152 and
                            Path(files[0].name).name==Path(relative).name and
                            not any(x.issym() or x.islnk() for x in members), 'PUBLIC_SOURCE_ARCHIVE_INVALID')
                    raw=archive.extractfile(files[0]).read(2097153)
                tree=ast.parse(raw);names={n.id for n in ast.walk(tree) if isinstance(n,ast.Name)}
                names.update(n.name for n in ast.walk(tree) if isinstance(n,(ast.ClassDef,ast.FunctionDef,ast.AsyncFunctionDef)))
                literals={n.value for n in ast.walk(tree) if isinstance(n,ast.Constant) and type(n.value) is str}
                result[relative]={'sha256':hashlib.sha256(raw).hexdigest(),
                    'symbols':sorted(names.intersection({'SupportsResponse','current_connection','ResourceStorageCollection','websocket_lovelace_save_config'})),
                    'commands':sorted(literals.intersection({'lovelace/config','lovelace/config/save','lovelace/info','lovelace/resources','lovelace/resources/list'})),
                    'source_support_only':True}
            except Exception:
                result[relative]={'state':'PUBLIC_SOURCE_NOT_ESTABLISHED'}
        return result

    def collect(self):
        self.observations={'paths':{},'production_mutation':False}
        require(sys.platform=='linux' and os.getuid()==os.geteuid()==os.getgid()==os.getegid()==0, 'QUALIFIED_TERMINAL_ROOT_IDENTITY_REQUIRED')
        require(socket.gethostname().lower().split('.')[0]!='nutandpihole', 'PI3_TARGET_REFUSED')
        require(all(hasattr(os,x) for x in ('O_DIRECTORY','O_NOFOLLOW','O_CLOEXEC','getxattr','fchown','fchmod','fsync'))
                and all(x in os.supports_dir_fd for x in (os.open,os.stat,os.mkdir,os.unlink,os.rename))
                and hasattr(ctypes.CDLL(None),'renameat2'), 'NATIVE_FILESYSTEM_PRIMITIVES_UNAVAILABLE')
        for root in ('/config','/homeassistant'):
            for relative in ('','custom_components','custom_components/hioc_operator','www','backups',
                             'backups/pe73-ha-delivery-v1','.storage/lovelace','.storage/lovelace_resources','.storage/lovelace_dashboards'):
                name=str(Path(root)/relative)
                try:self.observations['paths'][name]=metadata(Path(name))
                except OSError as error:self.observations['paths'][name]={'state':'ABSENT' if error.errno==errno.ENOENT else 'UNAVAILABLE','errno':error.errno}
                except ValueError:self.observations['paths'][name]={'state':'UNSAFE_PATH'}
        for name in ('uid_map','gid_map'):
            rows=[list(map(int,line.split())) for line in Path('/proc/self/'+name).read_text().splitlines()]
            require(rows==[[0,0,4294967295]], 'IDENTITY_USER_NAMESPACE_REQUIRED')
        options=json.loads(self.docker('system','info','--format','{{json .SecurityOptions}}'))
        require(type(options) is list and not any('userns' in x.lower() or 'rootless' in x.lower() for x in options), 'DOCKER_USER_MAPPING_UNSUPPORTED')
        core_ids=self.docker('container','ls','--filter','label=io.hass.type=homeassistant','--format','{{.ID}}').split()
        if not core_ids:
            core_ids=self.docker('container','ls','--filter','name=^/homeassistant$','--format','{{.ID}}').split()
        require(len(core_ids)==1, 'CORE_CONTAINER_NOT_UNIQUE')
        core=self.container(core_ids[0])
        self._observed_core=core
        identity=core_identity(self.docker('container','top',core['id'],'-eo','pid,uid,gid,comm'))
        self.observations['core']={'container_id':core['id'],'image':core['image'],'process':identity}
        ids=set(re.findall(r'(?:docker[-/]|containers/)([0-9a-f]{64})(?:[/.]|$)',Path('/proc/self/cgroup').read_text()))
        for line in Path('/proc/self/mountinfo').read_text().splitlines():
            cols=line.split()
            if len(cols)>5 and cols[4] in ('/etc/hostname','/etc/hosts','/etc/resolv.conf'):
                ids.update(re.findall(r'/containers/([0-9a-f]{64})/',cols[3]))
        require(len(ids)==1, 'TERMINAL_CONTAINER_IDENTITY_UNAVAILABLE')
        terminal=self.container(next(iter(ids)))
        def root_meta(root):
            return directory_chain(root,identity['uid'],identity['gid'])[root]
        root=bind_mounts(terminal,core,root_meta)
        self.observations['selected_root']=root
        directories={}
        failures=[]
        for relative in ('','custom_components','custom_components/hioc_operator','www','backups'):
            try:directories.update(directory_chain(str(Path(root)/relative),identity['uid'],identity['gid'],core_access=relative!='backups'))
            except FileNotFoundError:
                if relative not in ('custom_components/hioc_operator','backups'):
                    failures.append({'relative':relative,'code':'REQUIRED_PARENT_ABSENT'})
            except (OSError,QualificationError) as error:failures.append({'relative':relative,'code':str(error) if type(error) is QualificationError else 'DIRECTORY_NOT_ESTABLISHED'})
        self.observations['directory_failures']=failures
        require(not failures, 'DESTINATION_SECURITY_OR_PREREQUISITE_NOT_ESTABLISHED')
        visible=self.core_filesystem(terminal,identity,root,directories,core['id'])
        # Same boot/container/image/process/mount and root anchors must survive every mutation.
        require(self.container(terminal['id'])==terminal and self.container(core['id'])==core, 'CONTAINER_CONTEXT_DRIFT')
        return {'schema_version':'1.0','root':root,'publisher_uid':0,'publisher_gid':0,
            'core':identity,'terminal':terminal,'core_container':core,
            'boot_id':Path('/proc/sys/kernel/random/boot_id').read_text().strip(),
            'directories':directories,'core_filesystem':visible}


def preflight(probe=None):
    """Machine evidence only, never permission or an install flag."""
    probe=NativeProbe() if probe is None else probe
    try:
        value=probe.collect()
        result={'RESULT':'PASS_READ_ONLY_FILESYSTEM_IDENTITY_QUALIFICATION','filesystem_binding':value,
            'native_delivery_ready':False,
            'remaining':['LIVE_HA_CONNECTION_AND_DISABLED_GUARD','DASHBOARD_VIEW_RESOURCE_EXPORT',
                         'ACTUAL_TRUST_IDENTITIES_AND_PRIVATE_FILE_VALIDATION','NATIVE_MUTATION_BEHAVIOR'],
            'mutation_performed':False,'HA_imported':False,'container_exec_performed':False,
            'PE73':'IN_PROGRESS','PE74':'NOT_AUTHORIZED','STOP_REQUIRED':True}
    except BaseException as error:
        result={'RESULT':'BLOCKED_READ_ONLY_QUALIFICATION','failure_code':str(error) if type(error) is QualificationError else 'FILESYSTEM_OR_METADATA_NOT_ESTABLISHED',
            'failure_type':type(error).__name__,'mutation_performed':False,'HA_imported':False,
            'PE73':'IN_PROGRESS','PE74':'NOT_AUTHORIZED',
            'native_delivery_ready':False,'STOP_REQUIRED':True}
    if isinstance(probe,NativeProbe):
        result['observations']=getattr(probe,'observations',{})
        if hasattr(probe,'_observed_core'):
            try:result['public_capabilities']=probe.public_capabilities(probe._observed_core)
            except Exception:result['public_capabilities']={'state':'NOT_ESTABLISHED'}
        result['not_observed']=['LIVE_DASHBOARD_EXPORT_AND_RESOURCE_CONFLICTS','LIVE_DISABLED_ROLE_GUARD',
            'PRODUCTION_TRUST_MATERIAL_AND_ACL','FILESYSTEM_MUTATION_BEHAVIOR']
    return result


if __name__ == '__main__':
    result=preflight()
    print(json.dumps(result,sort_keys=True,separators=(',',':')))
    raise SystemExit(0 if result['RESULT'].startswith('PASS_') else 1)
