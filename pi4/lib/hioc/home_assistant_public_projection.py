"""Optional PE-4 public metadata consumer. Import performs no I/O.
Private validators execute only after exact byte identity verification. Native
reads are descriptor-relative, read-only and nonblocking; no producer API runs.
"""
import errno
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import struct
import sys
import time
import types

HOME = Path('/home/jazofv1/hioc')
MODULE_PATH = 'pi4/lib/hioc/home_assistant_association.py'
MODULE_SHA = '9a9be5812f3481146de7546875320eb6adec65ca5a2b3230ff5fec378892c7c1'
PRIVATE_SCHEMA_PATH = 'governance/pe4/pe4-home-assistant-association-state-v1.1.schema.json'
PRIVATE_SCHEMA_SHA = '5cd060ffd0a7a2e0a2b3e61da50ec8e5a418f4251df7305f713c10701b0e6a5d'
PUBLIC_SCHEMA_PATH = 'governance/pe4/pe4-home-assistant-public-projection.schema.json'
PUBLIC_SCHEMA_SHA = '50369a904e83ace1c9d5c760ddc9c3e90a70c059725b4f238eaae4f0347185b3'
LIMIT = 16 * 1024 * 1024
CODES = frozenset(['OMITTED_UNAVAILABLE','OMITTED_BUSY','OMITTED_UNSAFE',
                   'OMITTED_INVALID','OMITTED_INCOHERENT','OMITTED_INTERNAL'])


class ProjectionError(Exception):
    def __init__(self, code):
        self.code = code if type(code) is str and code in CODES else 'OMITTED_INTERNAL'
        super().__init__(self.code)


def require(condition, code='OMITTED_UNSAFE'):
    if not condition:
        raise ProjectionError(code)


def fingerprint(info):
    return (info.st_dev,info.st_ino,info.st_mode,info.st_uid,info.st_gid,
            info.st_nlink,info.st_size,info.st_mtime_ns,info.st_ctime_ns)


class NativeReadFS:
    """Linux primitives, imported/used only on a capable POSIX path."""
    def open_root(self, path):
        return os.open(path,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC)

    def open_dir(self,parent,name):
        return os.open(name,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC,dir_fd=parent)

    def open_file(self,parent,name):
        return os.open(name,os.O_RDONLY|os.O_NONBLOCK|os.O_NOFOLLOW|os.O_CLOEXEC,dir_fd=parent)

    def fstat(self,fd):return os.fstat(fd)
    def lstat(self,parent,name):return os.stat(name,dir_fd=parent,follow_symlinks=False)
    def read(self,fd,size):return os.read(fd,size)
    def close(self,fd):os.close(fd)
    def entries(self,fd):return os.scandir(fd)

    def flock(self,fd,acquire):
        import fcntl
        fcntl.flock(fd,(fcntl.LOCK_SH|fcntl.LOCK_NB) if acquire else fcntl.LOCK_UN)

    def acl(self,fd,directory=False):
        # Match the accepted producer's access/default ACL semantics exactly.
        for attr in (['system.posix_acl_access','system.posix_acl_default'] if directory else ['system.posix_acl_access']):
            try:raw=os.getxattr(fd,attr)
            except OSError as exc:
                require(exc.errno==errno.ENODATA)
                continue
            require(attr.endswith('access') and len(raw)==28 and struct.unpack('<I',raw[:4])[0]==2)
            entries=[struct.unpack('<HHI',raw[i:i+8]) for i in range(4,28,8)]
            mode=stat.S_IMODE(self.fstat(fd).st_mode)
            require(entries==[(1,(mode>>6)&7,0xffffffff),(4,(mode>>3)&7,0xffffffff),(32,mode&7,0xffffffff)])


def native_identity():
    require(sys.platform=='linux' and os.name=='posix','OMITTED_UNAVAILABLE')
    import pwd
    import grp
    user=pwd.getpwnam('jazofv1');group=grp.getgrnam('jazofv1')
    users=pwd.getpwall();groups=grp.getgrall()
    require(user.pw_uid>0 and group.gr_gid>0)
    require(len({u.pw_name for u in users})==len(users) and len({u.pw_uid for u in users})==len(users))
    require(len({g.gr_name for g in groups})==len(groups) and sum(g.gr_gid==group.gr_gid for g in groups)==1)
    require(sum(u==user for u in users)==sum(g==group for g in groups)==1)
    require(pwd.getpwuid(user.pw_uid)==user and grp.getgrgid(group.gr_gid)==group)
    require(len(group.gr_mem)==len(set(group.gr_mem)))
    by_name={u.pw_name:u for u in users}
    require(all(n in by_name for n in group.gr_mem))
    readers={u.pw_name for u in users if u.pw_gid==group.gr_gid}|set(group.gr_mem)
    require('jazofv1' in readers and all(n=='jazofv1' or by_name[n].pw_uid==0 for n in readers))
    require(os.getuid()==os.geteuid()==user.pw_uid and group.gr_gid in {os.getegid(),*os.getgroups()})
    return user.pw_uid,group.gr_gid


class SecureReader:
    """Pinned existing hierarchy; anchor injection is for controlled test trees.
    Production defaults always begin at /. This object never creates a path.
    """
    def __init__(self,root,uid,gid,fs=None,anchor=Path('/'),clock=time.monotonic,seconds=2):
        self.root=Path(root);self.anchor=Path(anchor);self.uid=uid;self.gid=gid
        self.fs=fs or NativeReadFS();self.clock=clock;self.seconds=seconds
        self.chain=[];self.lock_fd=None;self.deadline=None

    def checkpoint(self):
        require(self.deadline is None or self.clock()<=self.deadline,'OMITTED_INCOHERENT')

    def security(self,fd,directory=False,private=False):
        self.checkpoint();info=self.fs.fstat(fd);mode=stat.S_IMODE(info.st_mode)
        require(stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode))
        require(info.st_uid in (0,self.uid) and not mode&0o022)
        if private:require(info.st_uid==self.uid and info.st_gid==self.gid and mode==(0o700 if directory else 0o600))
        if not directory:require(info.st_nlink==1)
        self.fs.acl(fd,directory)
        return info

    def guard(self):
        for parent,name,fd in self.chain:
            info=self.security(fd,True)
            if parent is not None:
                named=self.fs.lstat(parent,name)
                require((info.st_dev,info.st_ino,info.st_mode,info.st_uid,info.st_gid)==(named.st_dev,named.st_ino,named.st_mode,named.st_uid,named.st_gid),'OMITTED_INCOHERENT')
        if self.lock_fd is not None:
            self.security(self.lock_fd,private=True)
            self.bound(self.chain[-1][2],'.home_assistant.lock',self.lock_fd)

    def bound(self,parent,name,fd):
        self.checkpoint()
        require(fingerprint(self.fs.fstat(fd))==fingerprint(self.fs.lstat(parent,name)),'OMITTED_INCOHERENT')

    def __enter__(self):
        try:
            names=self.root.relative_to(self.anchor).parts
            fd=self.fs.open_root(self.anchor);self.chain.append((None,None,fd))
            for name in names:
                parent=fd;fd=self.fs.open_dir(parent,name);self.chain.append((parent,name,fd))
            self.guard()
            return self
        except Exception:
            self.__exit__(None,None,None)
            raise

    def __exit__(self,*_):
        failed=False
        for _,_,fd in reversed(self.chain):
            try:self.fs.close(fd)
            except Exception:failed=True
        self.chain=[]
        if failed:raise ProjectionError('OMITTED_INTERNAL')

    def file(self,parent,name,private=False,limit=LIMIT):
        self.checkpoint();before=self.fs.lstat(parent,name)
        require(stat.S_ISREG(before.st_mode) and before.st_nlink==1)
        require(0<=before.st_size<=limit,'OMITTED_INVALID')
        fd=self.fs.open_file(parent,name)
        try:
            info=self.security(fd,private=private)
            require(fingerprint(before)==fingerprint(info),'OMITTED_INCOHERENT')
            raw=self.fs.read(fd,limit+1)
            self.checkpoint()
            require(len(raw)==info.st_size,'OMITTED_INCOHERENT')
            self.security(fd,private=private);self.bound(parent,name,fd)
            require(fingerprint(info)==fingerprint(self.fs.fstat(fd)),'OMITTED_INCOHERENT')
            return raw
        finally:self.fs.close(fd)

    def relative_file(self,path):
        """Secure source/public file read with transient pinned subdirectories."""
        parts=Path(path).parts
        require(parts and not Path(path).is_absolute() and all(p not in ('.','..') for p in parts))
        original=len(self.chain)
        try:
            parent=self.chain[-1][2]
            for name in parts[:-1]:
                fd=self.fs.open_dir(parent,name);self.chain.append((parent,name,fd));parent=fd
            self.guard();raw=self.file(parent,parts[-1]);self.guard()
            return raw
        finally:
            while len(self.chain)>original:
                fd=self.chain.pop()[2];self.fs.close(fd)

    def namespace(self,parent):
        self.checkpoint()
        with self.fs.entries(parent) as entries:
            for count,entry in enumerate(entries,1):
                self.checkpoint();require(count<=4096,'OMITTED_INCOHERENT')
                require(not entry.name.startswith(('.home_assistant.txn-','.home_assistant.done-')),'OMITTED_INCOHERENT')

    def snapshot(self):
        """Caller pins associations root. No parsing occurs in this section."""
        parent=self.chain[-1][2];fd=None;locked=False
        self.deadline=self.clock()+self.seconds
        try:
            self.security(parent,True,True)
            before=self.fs.lstat(parent,'.home_assistant.lock')
            require(stat.S_ISREG(before.st_mode) and before.st_nlink==1)
            fd=self.fs.open_file(parent,'.home_assistant.lock')
            self.security(fd,private=True)
            require(fingerprint(before)==fingerprint(self.fs.fstat(fd)),'OMITTED_INCOHERENT')
            self.bound(parent,'.home_assistant.lock',fd)
            try:self.fs.flock(fd,True)
            except OSError as exc:
                if exc.errno in (errno.EAGAIN,errno.EACCES):raise ProjectionError('OMITTED_BUSY') from None
                raise
            locked=True;self.lock_fd=fd
            self.guard();self.namespace(parent)
            raw=self.file(parent,'home_assistant.json',True)
            self.namespace(parent);self.guard();self.security(parent,True,True)
            return raw
        finally:
            self.lock_fd=None;self.deadline=None
            try:
                if locked:self.fs.flock(fd,False)
            finally:
                if fd is not None:self.fs.close(fd)


def load_contracts(read):
    """Verify BOTH private identities before executing any private module byte."""
    module=read(MODULE_PATH);schema_raw=read(PRIVATE_SCHEMA_PATH);public_raw=read(PUBLIC_SCHEMA_PATH)
    require(hashlib.sha256(module).hexdigest()==MODULE_SHA,'OMITTED_INVALID')
    require(hashlib.sha256(schema_raw).hexdigest()==PRIVATE_SCHEMA_SHA,'OMITTED_INVALID')
    require(hashlib.sha256(public_raw).hexdigest()==PUBLIC_SCHEMA_SHA,'OMITTED_INVALID')
    private=types.ModuleType('hioc.home_assistant_association')
    private.__file__=MODULE_PATH;private.__package__='hioc'
    exec(compile(module,MODULE_PATH,'exec'),private.__dict__)
    schema=private.strict_json(schema_raw,'CANDIDATE_STATE_VALIDATION')
    public=private.strict_json(public_raw,'CANDIDATE_STATE_VALIDATION')
    private.check_schema_contract(schema);private.check_schema_contract(public)
    return private,schema,public


def strip_inventory(inventory):
    result=dict(inventory)
    result['devices']=[{k:v for k,v in d.items() if k!='home_assistant'} for d in inventory.get('devices',[])]
    return result


def validate_public(obj,private,schema):
    # Independently validate the public allowlist; never fork private validation.
    fields={'associated','association_basis','entity_count','integration_domains','has_area_candidate'}
    require(type(obj) is dict and set(obj)==fields==set(schema['required']) and schema['additionalProperties'] is False,'OMITTED_INVALID')
    require(obj['associated'] is True and type(obj['association_basis']) is str and obj['association_basis']=='strong_mac','OMITTED_INVALID')
    bounds=schema['properties']['entity_count']
    require(type(obj['entity_count']) is int and bounds['minimum']<=obj['entity_count']<=bounds['maximum'],'OMITTED_INVALID')
    require(type(obj['has_area_candidate']) is bool,'OMITTED_INVALID')
    domains=obj['integration_domains'];rules=schema['properties']['integration_domains'];item=rules['items']
    require(type(domains) is list and len(domains)<=rules['maxItems'],'OMITTED_INVALID')
    require(all(type(d) is str and item['minLength']<=len(d)<=item['maxLength'] and re.fullmatch(item['pattern'],d) for d in domains),'OMITTED_INVALID')
    require(domains==sorted(set(domains)) and not any(re.fullmatch('[0-9a-f]{12}',d) for d in domains),'OMITTED_INVALID')
    private.validate_privacy(obj)


def derive_projection(devices,state,private,schema,public):
    private.validate_state(state,schema)
    ids=[d['id'] for d in devices]
    require(all(type(i) is str and re.fullmatch('dev_[0-9a-f]{16}',i) for i in ids) and len(ids)==len(set(ids)),'OMITTED_INVALID')
    current=set(ids);candidate={}
    for association in state['associations']:
        key=association['hioc_device_id']
        if key not in current:continue
        obj=dict(associated=True,association_basis='strong_mac',entity_count=len(association.get('entities',[])),integration_domains=sorted({c['domain'] for c in association.get('config_entries',[])}),has_area_candidate=isinstance(association.get('area_candidate'),dict))
        validate_public(obj,private,public);candidate[key]=obj
    return candidate


def attach_projection(inventory,candidate,private,public):
    base=strip_inventory(inventory);ids=[d['id'] for d in base['devices']]
    require(type(candidate) is dict and len(ids)==len(set(ids)) and set(candidate)<=set(ids),'OMITTED_INVALID')
    for obj in candidate.values():validate_public(obj,private,public)
    for device in base['devices']:
        if device['id'] in candidate:device['home_assistant']=candidate[device['id']]
    return base


def project_inventory(inventory,source_root=HOME,state_root=HOME):
    """Production API; raises fixed errors, never writes/logs/contacts a producer."""
    private=None
    try:
        uid,gid=native_identity()
        with SecureReader(source_root,uid,gid) as reader:
            private,schema,public=load_contracts(reader.relative_file)
        with SecureReader(Path(state_root)/'state/inventory/associations',uid,gid) as reader:
            raw=reader.snapshot()
        state=private.strict_json(raw,'CANDIDATE_STATE_VALIDATION')
        candidate=derive_projection(inventory['devices'],state,private,schema,public)
        return attach_projection(inventory,candidate,private,public)
    except ProjectionError:raise
    except FileNotFoundError:raise ProjectionError('OMITTED_UNAVAILABLE') from None
    except (OSError,PermissionError):raise ProjectionError('OMITTED_UNSAFE') from None
    except Exception as error:
        code='OMITTED_INVALID' if private is not None and isinstance(error,private.Failure) else 'OMITTED_INTERNAL'
        raise ProjectionError(code) from None
