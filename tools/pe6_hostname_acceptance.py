"""Operator-only PE-6.4 acceptance instrument; no runtime integration.

Uncommitted preparation is not execution authority. Entrypoint bytes require an
external approved release checksum BEFORE execution. The helper is compiled only
from descriptor-read, hash-verified bytes; no unverified helper import/cache.
Default selected inputs, Reader, policy and clock are intentionally not CLI options.
Reviewed permissions, if supplied as closed field dictionaries by an independent
reviewer, must bind actual capture/difference hashes. CLI supplies none. No blanket producer exemption.
"""
import argparse, types
import importlib.abc
import importlib.util
import collections, contextlib, hashlib, json, os, pathlib, re, socket, stat, subprocess, sys
R=pathlib.Path('/home/jazofv1/hioc'); S=pathlib.Path('/home/jazofv1/hioc-release-source')
COMMIT='9d6ce274a80a578d488d7245ebfa5bca1d5f5a83'
MODULES=['hioc/__init__.py', 'hioc/assets.py', 'hioc/enrichment.py', 'hioc/manufacturer.py', 'hioc/core/__init__.py', 'hioc/core/logging.py', 'hioc/core/schemas.py', 'hioc/core/state.py', 'hioc/runtime.py', 'hioc/core/compatibility.py', 'hioc/core/capabilities.py', 'hioc/core/drivers.py', 'hioc/core/monitoring.py', 'hioc/inventory.py', 'hioc/service_association.py', 'hioc/configured_association_schemas.py', 'hioc/configured_association.py', 'hioc/classification_contract.py', 'hioc/classification.py', 'hioc/configured_association_store.py', 'hioc/classification_caller.py']
PATHS={'inventory':R/'state/inventory/inventory.json','hostname':R/'state/inventory/enrichment.json'}
CRON=['/etc/crontab','/etc/cron.d','/etc/cron.hourly','/etc/cron.daily',
      '/etc/cron.weekly','/etc/cron.monthly','/etc/systemd/system','/run/systemd/system']
class Fail(Exception): pass
class Uncertain(Exception): pass
def need(ok):
    if not ok: raise Fail()
def digest(b): return hashlib.sha256(b).hexdigest()
def encode(v): return json.dumps(v,sort_keys=True,separators=(',',':')).encode()
def fp(s): return [s.st_dev,s.st_ino,s.st_mode,s.st_uid,s.st_gid,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def command(argv):
    p=subprocess.run(argv,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
       timeout=20,env={'PATH':'/usr/bin:/bin','LC_ALL':'C','GIT_OPTIONAL_LOCKS':'0',
       'GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':'/dev/null','GIT_TERMINAL_PROMPT':'0','GIT_NO_REPLACE_OBJECTS':'1'})
    return p.returncode,p.stdout,p.stderr

def code_identity(path,expected, *, return_raw=False):
    fd=os.open('/',os.O_RDONLY|os.O_DIRECTORY); leaf=None
    try:
        for part in path.parent.parts[1:]:
            child=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd)
            os.close(fd); fd=child; s=os.fstat(fd)
            need(s.st_uid in (0,1000) and not s.st_mode & 0o022)
        a=os.stat(path.name,dir_fd=fd,follow_symlinks=False)
        need(stat.S_ISREG(a.st_mode) and a.st_nlink==1 and (a.st_uid==a.st_gid==1000 if expected else a.st_uid in (0,1000)) and not a.st_mode & 0o022)
        if path.name in ('hioc-classify-metadata.py','classification.py','classification_caller.py','classification_contract.py','pe6_protected_state_evidence.py'):
            need(stat.S_IMODE(a.st_mode)==0o600)
        leaf=os.open(path.name,os.O_RDONLY|os.O_NOFOLLOW,dir_fd=fd)
        need(fp(a)==fp(os.fstat(leaf))); raw=b''
        while True:
            b=os.read(leaf,65536)
            if not b: break
            raw+=b; need(len(raw)<=16777216)
        need(fp(a)==fp(os.fstat(leaf))==fp(os.stat(path.name,dir_fd=fd,follow_symlinks=False)))
        need(digest(raw)==expected) if expected else need(b'hioc-classify-metadata' not in raw and b'classification_caller' not in raw)
        return raw if return_raw else [fp(a),digest(raw)]
    finally:
        if leaf is not None: os.close(leaf)
        os.close(fd)

def metadata(path,scan=False):
    # Metadata only: no private configuration, journal or producer contents opened.
    out={}; todo=[path]
    try:
        while todo:
            p=todo.pop(); need(len(out)<30000)
            try: a=p.lstat()
            except FileNotFoundError: out[str(p)]=None; continue
            out[str(p)]=code_identity(p,None) if scan and stat.S_ISREG(a.st_mode) else fp(a)
            if stat.S_ISDIR(a.st_mode):
                todo.extend(p.iterdir())
                if fp(a)!=fp(p.lstat()): raise Uncertain()
    except OSError: raise Uncertain() from None
    return out

def protected(pins):
    for p in pathlib.Path('/proc').iterdir():
        if not p.name.isdigit() or int(p.name)==os.getpid(): continue
        try: b=(p/'cmdline').read_bytes()
        except FileNotFoundError: continue
        need(b'hioc-classify-metadata' not in b and b'hioc.classification_caller' not in b)
    rc,b,e=command(['/usr/bin/crontab','-l'])
    need(rc==0 or rc==1 and b'no crontab for jazofv1' in e.lower())
    need(b'hioc-classify-metadata' not in b and b'classification_caller' not in b)
    return {'code':{str(R/p):code_identity(R/p,h) for p,h in pins.items()},
      'configuration':metadata(R/'config'),'producer_state':metadata(R/'state'),
      'historical_journals':metadata(R/'backups'),'runtime_root':fp(R.lstat()),
      'locks':{str(p):metadata(p) for p in pathlib.Path('/tmp').glob('hioc*')},
      'schedule':{k:v for p in CRON for k,v in metadata(pathlib.Path(p),True).items()},'user_crontab':[rc,digest(b),digest(e)]}

class Quiet:
    def write(self,s):
        need(not s)
        return 0
    def flush(self): pass

def reduce_result(result,snaps,m):
    m.pe5.shape(result,m.SCHEMA,'RESULT_INVALID')
    sources={p['kind']:p for p in result['inputs']}
    need(set(sources)==set(m.KINDS) and len(result['inputs'])==len(m.KINDS) and result['state']=='PARTIAL')
    for k,p in sources.items():
        need((p['state'],p['reason_code'],p['sha256'])==
           ('VALID','VALIDATED',snaps[k]['sha256']) if k in snaps else
           (p['state'],p['reason_code'],p['sha256'])==('ABSENT','ABSENT',None))
    inv=snaps['inventory']['value']; host=snaps['hostname']['value']; owners=m.local._owners(inv['devices'])
    rows=result['devices']; ids=[d['stable_device_id'] for d in rows]
    need(len(ids)==len(set(ids)) and set(ids)=={d['id'] for d in inv['devices']})
    rules=collections.Counter(); statuses=collections.Counter(); quality=collections.Counter(); reasons=collections.Counter()
    for d in rows:
        did=d['stable_device_id']; strong=m.local._owner_reason(did,*owners) is None
        need((d['identity_status']=='strong')==strong and d['operator_role'] is None and d['operator_role_evidence'] is None)
        need(d['classification_status'] not in ('OPERATOR_DECLARED','EXPLICIT_UNKNOWN'))
        h=host['records'][did]['hostname']; support={}
        if strong and not h['conflict']:
            for c in h['candidates']:
                name=c['normalized_value']; normalized=m.enrichment.normalize_hostname_evidence(c['raw_value'])
                if c['state']!='active' or not c['selectable'] or c['authority']=='historical' or c['quality'] in ('invalid','placeholder') or not name.isascii() or any(t.startswith('xn--') for t in name.split('.')) or not normalized or normalized['normalized_value']!=name: continue
                for rule in m.RULES[:-1]:
                    if set(re.findall('[a-z0-9]+',name.lower())) & set(rule['tokens']):
                        support.setdefault(rule['id'],set()).add(m.digest([did,'hostname',snaps['hostname']['sha256'],c['candidate_id']]))
        actual=set()
        for s in d['role_suggestion']:
            selected=[r for r in m.RULES[:-1] if r['id'] in s['rule_ids']]
            need(strong and selected and all(r['role']==s['role'] and r['id'] in support for r in selected))
            need(s['evidence_ids']==sorted(set().union(*(support[r['id']] for r in selected))))
            need(s['confidence']=='low' and s['suggestion_id']=='rsug_'+m.digest(['pe6-role-v1',did,s['role']]))
            need(s['correlation_groups']==[m.digest(['pe6-group-v1',did,'hostname'])])
            actual.update(s['rule_ids']); rules.update(s['rule_ids'])
        need(actual==set(support)); statuses[d['classification_status']]+=1; quality[d['metadata_quality']]+=1
        need(d['reason_codes']==sorted({q['reason_code'] for q in d['quality_details']})); reasons.update(d['reason_codes'])
    summary=dict(device_count=len(rows),suggestion_count=sum(len(d['role_suggestion']) for d in rows),
                 conflicted_count=quality['conflicted'],unavailable_source_count=5)
    need(result['summary']==summary)
    return dict(schema_version=result['schema_version'],rule_version=result['rule_version'],
      evaluated_at=result['evaluated_at'],valid_until=result['valid_until'],state=result['state'],summary=summary,
      classification_status_counts=dict(statuses),metadata_quality_counts=dict(quality),reason_counts=dict(reasons),
      suggestions_by_rule={r['id']:rules[r['id']] for r in m.RULES[:-1]},
      sources=[dict(kind=k,state=sources[k]['state'],reason=sources[k]['reason_code'],sha256=sources[k]['sha256'],
             selection='SELECTED' if k in snaps else 'NOT_SELECTED') for k in m.KINDS])

class VerifiedLoader(importlib.abc.Loader):
    """One allowlisted HIOC module; never asks a source/bytecode loader for code."""
    def __init__(self, registry, name):
        self.registry, self.name = registry, name

    def create_module(self, spec): return None

    def exec_module(self, module):
        registry = self.registry
        need(registry.active and sys.meta_path[0] is registry)
        path, raw, package = registry.sources[self.name]
        need(module.__name__ == self.name and module.__spec__.loader is self)
        need(module.__spec__.origin == str(path) and self.name not in registry.attempted)
        registry.attempted.add(self.name)
        module.__cached__ = None
        # No path reopening, pyc lookup, namespace or extension-module fallback.
        registry.executed[self.name] = module
        try:
            exec(compile(raw, str(path), 'exec', dont_inherit=True), module.__dict__)
        except BaseException:
            registry.executed.pop(self.name, None)
            raise


class VerifiedRuntime(importlib.abc.MetaPathFinder):
    """Acceptance-scoped registry for the EXACT existing 21-module dependency set.

    Entry-tool identity and the interpreter/stdlib are trusted outside this hook.
    It is not an OS sandbox and does not authenticate operator approvals.
    """
    def __init__(self, pins):
        self.active = False
        need(not any(n == 'hioc' or n.startswith('hioc.') for n in sys.modules))
        expected = {'pi4/bin/hioc-classify-metadata.py', *('pi4/lib/'+p for p in MODULES)}
        need(set(pins) == expected)
        sources = {}
        for relative in MODULES:
            package = relative.endswith('/__init__.py')
            name = relative[:-12] if package else relative[:-3]
            name = name.replace('/', '.')
            path = R/'pi4/lib'/relative
            raw = code_identity(path, pins['pi4/lib/'+relative], return_raw=True)
            need(type(raw) is bytes and digest(raw) == pins['pi4/lib/'+relative])
            sources[name] = (path, raw, package)
        self.sources = types.MappingProxyType(sources)
        self.executed, self.attempted = {}, set()

    def __enter__(self):
        need(not self.active)
        need(not any(n == 'hioc' or n.startswith('hioc.') for n in sys.modules))
        sys.meta_path.insert(0, self); self.active = True
        return self

    def find_spec(self, fullname, path=None, target=None):
        if fullname != 'hioc' and not fullname.startswith('hioc.'): return None
        need(self.active and sys.meta_path[0] is self and target is None)
        need(fullname in self.sources)
        source, raw, package = self.sources[fullname]
        if fullname == 'hioc': need(path is None)
        else:
            parent = fullname.rsplit('.', 1)[0]
            need(parent in self.executed)
            parent_path = self.sources[parent][0].parent
            need(type(path) is list and path == [str(parent_path)])
            self.check_module(parent, sys.modules.get(parent))
        loader = VerifiedLoader(self, fullname)
        return importlib.util.spec_from_file_location(fullname, str(source), loader=loader,
            submodule_search_locations=[str(source.parent)] if package else None)

    def check_module(self, name, module):
        need(self.active and sys.meta_path[0] is self and name in self.sources)
        need(module is not None and self.executed.get(name) is module)
        spec = getattr(module, '__spec__', None)
        need(spec is not None and type(spec.loader) is VerifiedLoader)
        need(spec.loader.registry is self and spec.loader.name == name)
        need(module.__loader__ is spec.loader and spec.name == name)
        path, raw, package = self.sources[name]
        need(spec.origin == module.__file__ == str(path))
        need(bool(spec.submodule_search_locations is not None) == package)
        if package: need(module.__path__ == spec.submodule_search_locations == [str(path.parent)])

    def close(self):
        if not self.active: return
        sys.meta_path[:] = [finder for finder in sys.meta_path if finder is not self]
        # No HIOC module predated this context; prevent cached reuse after admission ends.
        for name in tuple(sys.modules):
            if name == 'hioc' or name.startswith('hioc.'): sys.modules.pop(name, None)
        self.active = False

    def __exit__(self, *unused): self.close()


def verify_origins(pins, runtime):
    for name,mod in tuple(sys.modules.items()):
        if name!='hioc' and not name.startswith('hioc.'): continue
        runtime.check_module(name, mod)
        relative='pi4/lib/'+name.replace('.','/')+('/__init__.py' if name in ('hioc','hioc.core') else '.py')
        need(relative in pins)
        expected=R/relative; spec=getattr(mod,'__spec__',None)
        need(spec is not None and spec.name==name)
        for origin in (getattr(mod,'__file__',None),spec.origin):
            need(type(origin) is str)
            actual=pathlib.Path(origin)
            need(actual.is_absolute() and actual==expected and actual.resolve(strict=True)==expected)

def load_helper(expected_sha256):
    """One fixed helper, not a general import mechanism; verify before first use."""
    need(type(expected_sha256) is str and re.fullmatch('[0-9a-f]{64}', expected_sha256))
    path=pathlib.Path(__file__).resolve().with_name('pe6_protected_state_evidence.py')
    raw=code_identity(path,expected_sha256,return_raw=True)
    need(digest(raw)==expected_sha256)
    module=types.ModuleType('_pe6_verified_protected_evidence')
    module.__file__=str(path)
    sys.modules[module.__name__]=module
    try:
        # Execute the SAME verified bytes, avoiding a second path read or pyc load.
        exec(compile(raw,str(path),'exec'),module.__dict__)
    except BaseException:
        sys.modules.pop(module.__name__,None)
        raise Fail() from None
    return module


def runtime_preflight():
    need(os.getuid()==os.getgid()==1000 and socket.gethostname()=='nutandpihole')
    need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
         and stat.S_ISCHR(os.stat('/dev/null').st_mode))
    pins={}
    for relative in ['pi4/bin/hioc-classify-metadata.py',*['pi4/lib/'+p for p in MODULES]]:
        rc,raw,unused=command(['/usr/bin/git','--git-dir='+str(S/'.git'),
                              'cat-file','blob',COMMIT+':'+relative])
        need(rc==0); pins[relative]=digest(raw)
    pins['pi4/lib/hioc/inventory.py']='df1dc4e2de7d8d77b54acdcb3f340281ead6cc03d74a73ad59b2864b03564503'
    return pins


def _outcome(status,stage,category=None):
    value=dict(status=status,stage=stage)
    if category: value['category']=category
    return value


def run(authorization_reference=None,expiry_disposition_reference=None,
        helper_sha256=None,*,reviewed_permissions=()):
    """Return bounded public bytes; never print/persist private observations/results.

    Non-default dependencies are test mocks, not operator-selectable bypass flags.
    Authorization references are documentary gates, not authenticated signatures;
    the operator must have a separate truthful approval. Historical refs rejected.
    """
    stage='AUTHORIZATION'; calls=0; helper=None; before=after=None; runtime=None
    primary=_outcome('NOT_RUN','NONE'); inspection=_outcome('NOT_RUN','AFTER_STATE')
    functional={}; origins_before=origins_after='NOT_ESTABLISHED'
    receipt=dict(RESULT='FAIL',STOP_REQUIRED=True)
    try:
        for ref in (authorization_reference,expiry_disposition_reference):
            need(type(ref) is str and re.fullmatch('[A-Z][A-Z0-9_]{7,95}',ref))
            need(ref not in ('CHAT_20261019_PE64_SINGLE_RUN','ARCH_20261019_FROZEN_PE1_SCHEMA'))
        stage='PREFLIGHT'; pins=runtime_preflight()
        sys.pycache_prefix='/dev/null/hioc-pe64-no-bytecode'
        with contextlib.redirect_stdout(Quiet()),contextlib.redirect_stderr(Quiet()):
            helper=load_helper(helper_sha256)
        def observe():
            try:
                with contextlib.redirect_stdout(Quiet()),contextlib.redirect_stderr(Quiet()):
                    return protected(pins)
            except (Uncertain,OSError): raise helper.ObservationUnstable() from None
            except BaseException: raise helper.ProtectedInvariantFailure() from None
        before=helper.capture_protected(observe)
        if before.completeness=='COMPLETE' and not before.protected_failure:
            try:
                with contextlib.redirect_stdout(Quiet()),contextlib.redirect_stderr(Quiet()):
                    runtime=VerifiedRuntime(pins)
                    runtime.__enter__()
                    from hioc import classification as m,classification_caller as caller
                    stage='PRE_EVALUATION_MODULE_ORIGINS'; verify_origins(pins, runtime); origins_before='PASS'
                    stage='INPUT_PREFLIGHT'
                    reader=caller.Reader()
                    snaps={k:reader.capture(k,p,private=k!='inventory') for k,p in PATHS.items()}
                    inv=snaps['inventory']['value']
                    m.local.resolve_service_associations(inv,caller._clock(),2100)
                    need(len({d['id'] for d in inv['devices']})==len(inv['devices']))
                    need(0<=(m.timestamp(caller._clock())-m.timestamp(inv['updated'])).total_seconds()<2100)
                    m._hostname(snaps['hostname']['value'],inv); reader.recheck()
                    stage='SINGLE_EVALUATION'; need(calls==0); calls+=1
                    result=caller.evaluate(PATHS,reader=reader)
                    stage='POST_EVALUATION_MODULE_ORIGINS'; verify_origins(pins, runtime); origins_after='PASS'
                    stage='FUNCTIONAL_VERIFICATION'; functional=reduce_result(result,snaps,m)
                    reader.recheck()
                    stage='FINAL_TIME_CHECK'; now=caller._clock()
                    need(m.timestamp(result['evaluated_at'])<=m.timestamp(now)<m.timestamp(result['valid_until']))
                    primary=_outcome('PASS','FUNCTIONAL_VERIFICATION')
            except BaseException:
                # An unsuccessful verification must not leak a partially reduced result.
                functional={}; primary=_outcome('FAIL',stage,'REQUIRED_CHECK_FAILED')
            finally:
                after=helper.capture_protected(observe)
                inspection=_outcome('FAIL' if after.protected_failure else
                    'PASS' if after.completeness=='COMPLETE' else 'INCOMPLETE','AFTER_STATE')
        if primary['status']=='PASS':
            try:
                stage='FINAL_TIME_CHECK'
                need(m.timestamp(result['evaluated_at'])<=m.timestamp(caller._clock())<m.timestamp(result['valid_until']))
            except BaseException:
                functional={}; primary=_outcome('FAIL',stage,'REQUIRED_CHECK_FAILED')
        if after is None:
            # Explicit NOT_RUN after-state; never invent a successful empty capture.
            after=helper.Capture(None,None,'INCOMPLETE','OBSERVATION_ERROR',None,types.MappingProxyType({}))
        evidence=json.loads(helper.build_report(before,after,primary_outcome=primary,
            protected_inspection_outcome=inspection,
            reviewed_permissions=tuple(helper.ReviewedPermission(**item) for item in reviewed_permissions),
            max_report_bytes=32768))
        verdict=evidence['result']
        positive=bool(functional.get('summary',{}).get('suggestion_count'))
        if verdict=='PASS' and not positive: verdict='INSUFFICIENT_EVIDENCE'
        receipt.update(RESULT=verdict,protected_evidence=evidence,functional=functional,
            functional_positive_evidence='PASS' if positive else 'INSUFFICIENT_EVIDENCE',
            authorization_reference=authorization_reference,expiry_disposition_reference=expiry_disposition_reference,
            helper_sha256=helper_sha256,runtime_identity=digest(encode(pins)),source_object=COMMIT)
    except BaseException:
        # Includes authorization, helper identity and report-generation failures.
        if primary['status']!='FAIL': primary=_outcome('FAIL',stage,'REQUIRED_CHECK_FAILED')
        receipt=dict(RESULT='FAIL',STOP_REQUIRED=True)
    finally:
        if runtime is not None: runtime.close()
    receipt.update(primary_outcome=primary,protected_inspection_outcome=inspection,
        classification_invocations=calls,module_origins_before=origins_before,
        module_origins_after=origins_after,private_output_persisted=False,
        recurring_activation_performed=False,
        limitations=['WINDOWS_TESTS_DO_NOT_ESTABLISH_PRODUCTION_SAFETY',
          'BOUNDED_ACTIVATION_OBSERVATION_NOT_UNIVERSAL_ABSENCE',
          'FROZEN_PE1_HAS_NO_CANDIDATE_EXPIRES_AT','RUNTIME_INVENTORY_VARIANT_PRESERVED',
          'AUTHORIZATION_REFERENCES_REQUIRE_SEPARATE_OPERATOR_APPROVAL'])
    raw=encode(receipt)+b'\n'
    if len(raw)>65536:
        # Losing required report evidence cannot yield PASS. Retain independent outcomes.
        verdict='FAIL' if receipt['RESULT']=='FAIL' else 'INSUFFICIENT_EVIDENCE'
        raw=encode(dict(RESULT=verdict,primary_outcome=primary,
            protected_inspection_outcome=inspection,classification_invocations=calls,
            receipt_truncated=True,STOP_REQUIRED=True))+b'\n'
    return raw


def main():
    # No approval defaults: none of the historical identifiers authorizes a rerun.
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--authorization-reference')
    parser.add_argument('--expiry-disposition-reference')
    parser.add_argument('--helper-sha256')
    args=parser.parse_args()
    raw=run(args.authorization_reference,args.expiry_disposition_reference,args.helper_sha256)
    sys.stdout.buffer.write(raw)


if __name__=='__main__': main()
