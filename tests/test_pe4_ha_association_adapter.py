"""Synthetic adapter tests: temporary byte flow, injected POSIX metadata, no network."""
import asyncio
import contextlib
import copy
import errno
import io
import json
import os
from pathlib import Path
import stat
import struct
import sys
import tempfile
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"pi4/lib"))
from hioc import home_assistant_association as a
from hioc.core import compatibility as c
from tests.test_pe4_0c1_association_lifecycle import reference_cycle
from tests.test_pe4_ha_runtime_credential_provisioning import FixtureFS,GID
SCHEMA=json.loads((ROOT/a.SCHEMA_PATH).read_bytes())
REGISTRY=c.load_registry(ROOT/"governance/compatibility-contracts.json")
A,B="dev_0123456789abcdef","dev_1111111111111111"
MAC,OTHER="02:00:00:00:00:01","02:00:00:00:00:02"
T0,T1,T2="2026-10-06T12:00:00Z","2026-10-06T13:00:00Z","2026-10-06T14:00:00Z"
def device(name="old",mac=MAC):return dict(id=name,connections=[["mac",mac]] if mac is not None else [])
def inventory(ds=None,updated=T0):return a.encoded(dict(schema_version="1.0",updated=updated,devices=[dict(id=A,mac=MAC)] if ds is None else ds,services=[],topology={},dependencies={},summary={}))
def cycle(prior=None,ds=None,es=None,areas=None,entries=None,inv=None,ts=T0):
 return a.reconcile(prior,[[device()] if ds is None else ds,es or [],areas or [],entries or []],a.validate_inventory(inventory(inv,ts),a.instant(ts)),ts,"2026.9.4",SCHEMA)
class TemporaryFS:
 """Real Windows files/hardlinks/rename; injected POSIX ownership/ACL/flock/fsync."""
 def __init__(self,root):self.root=self.parent=Path(root);self.events=[];self.at=None;self.persistent=False;self.fault=None;self.locked=False;self.renamed={}
 def hit(self,kind):
  i=len(self.events);self.events.append(kind)
  if (self.at is not None and i>=self.at and (self.persistent or i==self.at)) or self.fault==kind:
   if not self.persistent:self.fault=None
   raise OSError(errno.EIO,"SYNTHETIC_FAULT")
 def resolved(self,path):
  path=Path(path)
  while path in self.renamed:path=self.renamed[path]
  return path
 def start(self):self.hit("start")
 def finish(self):self.hit("finish")
 def guard(self):self.hit("guard")
 def security(self,fd,directory=False,mode=0o600,links=1,owner=None):self.hit("security");return self.fstat(fd)
 def acl(self,fd,directory=False):self.hit("acl")
 def fstat(self,fd):return self.resolved(fd).stat()
 def lstat(self,parent,name):self.hit("lstat");return (self.resolved(parent)/name).lstat()
 def open_dir(self,parent,name):
  self.hit("open_dir");p=self.resolved(parent)/name;a.require(p.is_dir() and not p.is_symlink(),"STATE_PUBLICATION");return p
 def close(self,fd):pass
 def names(self,parent):self.hit("names");return [p.name for p in self.resolved(parent).iterdir()]
 def file(self,parent,name,limit=a.LIMIT,links=1,private=True):
  self.hit("read");p=self.resolved(parent)/name;s=self.lstat(parent,name)
  a.require(stat.S_ISREG(s.st_mode) and s.st_nlink==links and s.st_size<=limit,"STATE_PUBLICATION")
  raw=p.read_bytes();a.require(len(raw)==s.st_size,"STATE_PUBLICATION");return raw,s
 def write(self,parent,name,data):
  self.hit("write");p=self.resolved(parent)/name
  with p.open("xb") as f:f.write(data);f.flush();self.hit("file_sync");os.fsync(f.fileno())
  self.hit("reread");a.require(p.read_bytes()==data,"STATE_PUBLICATION")
 def mkdir(self,parent,name):self.hit("mkdir");(self.resolved(parent)/name).mkdir()
 def link(self,src,name,dst,target):self.hit("link");os.link(self.resolved(src)/name,self.resolved(dst)/target)
 def replace(self,src,name,dst,target):
  self.hit("replace");source=self.resolved(src)/name;destination=self.resolved(dst)/target;directory=source.is_dir();os.replace(source,destination)
  if directory:self.renamed[source]=destination
 def sync(self,fd):self.hit("directory_sync")
 def unlink(self,parent,name,expected):
  self.hit("unlink");actual=self.lstat(parent,name);a.require((actual.st_dev,actual.st_ino)==(expected.st_dev,expected.st_ino),"STATE_PUBLICATION");(self.resolved(parent)/name).unlink()
 def rmdir(self,parent,name,fd):self.hit("rmdir");a.require(self.resolved(parent)/name==self.resolved(fd),"STATE_PUBLICATION");self.resolved(fd).rmdir()
 @contextlib.contextmanager
 def lock(self):
  self.hit("lock")
  if self.locked:raise a.Failure("LOCK_ACQUISITION")
  (self.root/".home_assistant.lock").touch(exist_ok=True);self.locked=True
  try:yield
  finally:self.locked=False
class SyntheticRuntime:
 def __init__(self,fs):self.fs=fs;self.raw=inventory(updated=T1);self.registries=[[device()],[],[],[]];self.calls=[];self.failure=None;self.reporting=False;self.changed=False;self.reads=0
 def now(self):return a.instant(T1)
 def invoke(self,stage):
  self.calls.append(stage)
  if stage==self.failure:raise a.Failure(stage)
 def target(self):self.invoke("TARGET_VALIDATION")
 def runtime(self):self.invoke("RUNTIME_VALIDATION")
 def filesystem(self):return self.fs
 def contracts(self,fs):self.invoke("CONTRACT_VALIDATION");return SCHEMA
 def inventory(self,fs):
  self.invoke("CANONICAL_INVENTORY_INPUT");self.reads+=1;raw=self.raw+(b" " if self.changed and self.reads>1 else b"");return raw,a.validate_inventory(raw,self.now())
 def credential(self):self.invoke("CREDENTIAL_ACQUISITION");return a.credential_value(b"SYNTHETIC_INVALID_HA_CREDENTIAL\n")
 def observe(self,token,observation):
  self.invoke("HA_CONNECTION");observation.update(available=True,observed_version="2026.9.4",capabilities=dict.fromkeys(a.CAPABILITIES,True));return self.registries,"2026.9.4"
 def assessment(self,observation,ts):self.invoke("COMPATIBILITY");return c.assess(next(d for d in REGISTRY["dependencies"] if d["dependency_id"]=="ha_core"),observation,{},ts)["status"]
 def report(self,observation,ts):
  self.calls.append("report");a.require(set(observation["capabilities"])==set(a.CAPABILITIES),"COMPATIBILITY")
  if self.reporting:raise ValueError("SYNTHETIC_PRIVATE_EXCEPTION")
class Closed(Exception):rcvd=sent=SimpleNamespace(code=1000)
class FakeWS:
 def __init__(self,messages):self.messages=list(messages);self.sent=[];self.aborted=False
 @property
 def transport(self):return self
 def abort(self):self.aborted=True
 async def recv(self):
  if not self.messages:raise Closed()
  item=self.messages.pop(0)
  if isinstance(item,BaseException):raise item
  return item if type(item) in (str,bytes) else json.dumps(item)
 async def send(self,message):self.sent.append(json.loads(message))
 async def close(self):pass
def messages(regs=None):return [dict(type="auth_required",ha_version="2026.9.4"),dict(type="auth_ok",ha_version="2026.9.4")]+[dict(id=i,type="result",success=True,result=r) for i,r in enumerate(regs or [[device()],[],[],[]],1)]
def exchange(ws):
 obs={"capabilities":dict.fromkeys(a.CAPABILITIES)};result=asyncio.run(a.exchange(ws,"SYNTHETIC_INVALID_HA_CREDENTIAL",obs,time.monotonic()+90));return result,obs
class IdentityTests(unittest.TestCase):
 def test_normalization_dedup_and_supporting_namespace(self):
  d=device();d["connections"] += [["mac"," 02-00-00-00-00-01 "],["bluetooth",OTHER]]
  self.assertEqual(cycle(ds=[d])["summary"]["associated_devices"],1)
  for ns in ("bluetooth","upnp","identifier","random"):
   self.assertEqual(cycle(ds=[dict(id="old",connections=[[ns,MAC]],identifiers=[["mac",MAC]])])["summary"]["associated_devices"],0)
 def test_all_mac_outcomes(self):
  cases=[([device()],None,"ASSOCIATED_STRONG_MAC"),([device(mac=None)],None,"REVIEW_ONLY_NO_MAC"),([dict(id="old",connections=[["mac",MAC],["mac",OTHER]])],None,"REVIEW_ONLY_MULTIPLE_MAC"),([device(mac="bad")],None,"REJECT_INVALID_MAC"),([device(),device("other")],None,"REJECT_HA_MAC_COLLISION"),([device()],[dict(id=A,mac=MAC),dict(id=B,mac=MAC)],"REJECT_HIOC_MAC_AMBIGUITY"),([device()],[],"UNMATCHED_STRONG_EVIDENCE")]
  for ds,inv,reason in cases:
   with self.subTest(reason=reason):self.assertIn(reason,{d["reason"] for d in cycle(ds=ds,inv=inv)["diagnostics"]})
 def test_global_index_includes_invalid_multiple_order_independent(self):
  for connections in ([["mac",MAC],["mac","bad"]],[["mac",MAC],["mac",OTHER]]):
   ds=[device(),dict(id="other",connections=connections)]
   for order in (ds,ds[::-1]):
    r=cycle(ds=order);self.assertEqual(r["summary"]["associated_devices"],0);self.assertIn("REJECT_HA_MAC_COLLISION",{d["reason"] for d in r["diagnostics"]})
 def test_lifecycle_matches_independent_reference(self):
  prior=cycle()
  for ds in ([device()],[],[device(mac=None)],[device(mac="bad")],[dict(id="old",connections=[["mac",MAC],["mac",OTHER]])],[device(),device("other")],[device("new")]):
   actual=cycle(prior,ds,ts=T1);expected,status=reference_cycle(prior,ds,[dict(id=A,mac=MAC)],timestamp=T1)
   self.assertEqual(status,"PASS");self.assertEqual(actual["associations"],expected["associations"]);self.assertEqual(actual["binding_history"],expected["binding_history"])
 def test_every_hioc_retirement(self):
  for inv,reason in (([],"HIOC_DEVICE_ABSENT"),([dict(id=A,mac=MAC),dict(id=B,mac=MAC)],"HIOC_MAC_AMBIGUITY"),([dict(id=A,mac=OTHER)],"HIOC_CANONICAL_MAC_NO_LONGER_MATCHES")):
   self.assertEqual(cycle(cycle(),inv=inv,ts=T1)["binding_history"][0]["retirement_reason"],reason)
 def test_reactivation_episodes_earliest_and_idempotence(self):
  retired=cycle(cycle(),[],ts=T1);active=cycle(retired,ts=T2)
  self.assertEqual(active["associations"][0]["first_associated_at"],T0);self.assertEqual(active["binding_history"],retired["binding_history"])
  again=cycle(active,[],ts="2026-10-06T15:00:00Z");self.assertEqual(len(again["binding_history"]),2)
  self.assertEqual(cycle(again,[],ts="2026-10-06T16:00:00Z")["binding_history"],again["binding_history"])
 def test_recreation_conflicts_and_tied_history(self):
  prior=cycle();new=cycle(prior,[device("new")],ts=T1)
  self.assertEqual(new["associations"][0]["first_associated_at"],T1);self.assertEqual(new["binding_history"][0]["retirement_reason"],"HA_DEVICE_RECREATED")
  self.assertEqual(cycle(prior,[device(mac=None),device("new")],ts=T1)["summary"]["associated_devices"],0)
  self.assertEqual(cycle(prior,inv=[dict(id=B,mac=MAC)],ts=T1)["summary"]["rejected"],1)
  retired=cycle(prior,[],ts=T1);second=copy.deepcopy(retired["binding_history"][0]);second["ha_device_id"]="second";retired["binding_history"].append(second);retired["summary"]["historical_bindings"]=2
  self.assertEqual(cycle(retired,[device("new")],ts=T2)["summary"]["rejected"],1)
 def test_history_capacity_no_eviction(self):
  prior=cycle();prior["binding_history"]=[dict(hioc_device_id=A,ha_device_id="historical-"+str(i),first_associated_at="2026-10-06T10:00:00Z",last_confirmed_at="2026-10-06T10:00:00Z",retired_at="2026-10-06T11:00:00Z",retirement_reason="HA_DEVICE_ABSENT") for i in range(4096)];prior["summary"]["historical_bindings"]=4096
  self.assertEqual(len(cycle(prior,ts=T1)["binding_history"]),4096);before=a.encoded(prior)
  with self.assertRaises(a.Failure) as caught:cycle(prior,[],ts=T1)
  self.assertEqual(caught.exception.stage,"BINDING_HISTORY_CAPACITY");self.assertEqual(a.encoded(prior),before)
 def test_time_cardinality_and_first_invariants(self):
  prior=cycle()
  for change in (lambda s:s["associations"].append(copy.deepcopy(s["associations"][0])),lambda s:s["summary"].update(associated_devices=0),lambda s:s["associations"][0].update(last_confirmed_at=T1)):
   bad=copy.deepcopy(prior);change(bad)
   with self.assertRaises(a.Failure):a.validate_state(bad,SCHEMA)
  with self.assertRaises(a.Failure):cycle(prior,ts=T0)

class RelationshipTests(unittest.TestCase):
 def test_complete_projection_no_raw_copy(self):
  d=device();d.update(area_id="area",config_entries=["entry","entry"],via_device_id="other",manufacturer="Synthetic Vendor",unique_id="NEVER_COPY",options={"raw":"NEVER_COPY"})
  e=dict(id="registry",entity_id="sensor.synthetic",platform="test",device_id="old",area_id="area",config_entry_id="entry",unique_id="NEVER_COPY")
  r=cycle(ds=[d,device("other",OTHER)],es=[e],areas=[dict(area_id="area",name="Synthetic room")],entries=[dict(entry_id="entry",domain="test",state="loaded",options={"raw":"NEVER_COPY"})]);assoc=r["associations"][0]
  self.assertEqual(assoc["relationship_status"],"COMPLETE");self.assertEqual(len(assoc["config_entries"]),1);self.assertEqual(r["summary"]["entity_memberships"],1)
  for value in ("NEVER_COPY",MAC):self.assertNotIn(value,a.encoded(r).decode())
 def test_dangling_optional_unsafe_keeps_strong(self):
  for extra in (dict(area_id="missing"),dict(via_device_id="missing"),dict(config_entries=["missing"]),dict(name="x"*257),dict(model="http://unsafe.invalid")):
   d=device();d.update(extra);assoc=cycle(ds=[d])["associations"][0];self.assertEqual(assoc["relationship_status"],"INCOMPLETE");self.assertEqual(assoc["hioc_device_id"],A)
 def test_unsafe_member_and_orphans(self):
  e=dict(id="x"*257,entity_id="sensor.test",platform="test",device_id="old");r=cycle(es=[e])
  self.assertEqual(r["summary"]["entity_memberships"],0);self.assertEqual(r["associations"][0]["relationship_status"],"INCOMPLETE")
  es=[dict(id=str(i),entity_id="sensor."+str(i),platform="test",device_id=v) for i,v in enumerate((None,"missing"))];r=cycle(ds=[],es=es)
  self.assertEqual(r["summary"]["associated_devices"],0);self.assertEqual(r["diagnostics"],[dict(reason="ENTITY_WITHOUT_DEVICE_IDENTITY",count=2)])
 def test_entity_area_not_promoted(self):
  e=dict(id="e",entity_id="sensor.e",platform="test",device_id="old",area_id="area")
  self.assertNotIn("area_candidate",cycle(es=[e],areas=[dict(area_id="area",name="room")])["associations"][0])
class InputTests(unittest.TestCase):
 def test_exact_final_lf_lengths(self):
  for raw in (b"A\n",b"A"*4096+b"\n"):self.assertEqual(a.credential_value(raw),raw[:-1].decode())
  for raw in (b"",b"A",b"A\n\n",b"A\r\n",b"A\nB\n",b" A\n",b"A \n",b"A\x00\n",b"\xff\n",b"A"*4097+b"\n",b"\n"):
   with self.subTest(length=len(raw)):
    with self.assertRaises(a.Failure):a.credential_value(raw)
 def test_real_temp_credential_bytes_and_metadata(self):
  with tempfile.TemporaryDirectory() as root:
   fs=FixtureFS(root);(fs.root/"etc/hioc").mkdir();(fs.root/"etc/hioc/credentials").mkdir()
   for p in (fs.root/"etc/hioc",fs.root/"etc/hioc/credentials"):fs.setmeta(p,mode=0o750,gid=GID)
   target=fs.root/"etc/hioc/credentials/home_assistant.token";target.write_bytes(b"SYNTHETIC_INVALID_HA_CREDENTIAL\n");fs.setmeta(target,mode=0o640,gid=GID)
   fds=a.open_hierarchy(fs,GID)
   try:self.assertEqual(a.read_credential(fs,fds[-1],GID),"SYNTHETIC_INVALID_HA_CREDENTIAL")
   finally:
    for fd in reversed(fds):fs.close(fd)
 def test_inventory_freshness_and_no_health_gates(self):
  now=a.instant(T1)
  for updated in (T0,T1,"2026-10-06T13:01:00Z"):self.assertIn(A,a.validate_inventory(inventory([dict(id=A,mac=MAC,last_seen="old",health_status="offline")],updated),now)[0])
  for updated in ("2026-10-06T11:29:59Z","2026-10-06T13:01:01Z","2026-10-06T13:00:00"):
   with self.assertRaises(a.Failure):a.validate_inventory(inventory(updated=updated),now)
 def test_inventory_missing_bad_ids_macs_duplicates(self):
  for ds in ([dict(id="bad",mac=MAC)],[dict(id=A,mac="bad")],[dict(id=A),dict(id=A)],[dict(id=A,mac=3)]):
   with self.assertRaises(a.Failure):a.validate_inventory(inventory(ds),a.instant(T0))
  v=json.loads(inventory());del v["services"]
  with self.assertRaises(a.Failure):a.validate_inventory(a.encoded(v),a.instant(T0))
  self.assertEqual(a.validate_inventory(inventory([]),a.instant(T0)),({},{}))
 def test_json_duplicate_nan_depth_string_fields_and_size(self):
  for raw in ('{"x":1,"x":2}','{"x":NaN}','['*34+'0'+']'*34,json.dumps("x"*1025),json.dumps({str(i):i for i in range(129)})):
   with self.assertRaises(a.Failure):a.strict_json(raw,"REGISTRY_SCHEMA",True)
  with self.assertRaises(a.Failure):a.strict_json(b" "*(a.LIMIT+1),"REGISTRY_SCHEMA",True)
 def test_schema_keyword_coverage_and_privacy(self):
  bad=copy.deepcopy(SCHEMA);bad["properties"]["associations"]["items"]["anyOf"]=[{"unknownKeyword":True}]
  with self.assertRaises(a.Failure):a.check_schema_contract(bad)
  for key,value in (("raw",MAC),("schema_version","1.0")):
   bad=cycle();bad[key]=value
   with self.assertRaises(a.Failure):a.validate_state(bad,SCHEMA)
  bad=cycle();bad["associations"][0]["ha_metadata"]={"name":MAC}
  with self.assertRaises(a.Failure):a.validate_state(bad,SCHEMA)
 def test_acl_base_extended_unverifiable_absence(self):
  fs=a.NativeFS();info=SimpleNamespace(st_mode=stat.S_IFREG|0o640)
  base=struct.pack("<I",2)+b"".join(struct.pack("<HHI",tag,perm,0xffffffff) for tag,perm in ((1,6),(4,4),(32,0)))
  with patch.object(fs,"fstat",return_value=info),patch.object(os,"getxattr",return_value=base,create=True):fs.acl(1)
  for response in (b"bad",OSError(errno.EPERM,"SYNTHETIC")):
   with patch.object(os,"getxattr",side_effect=response if isinstance(response,OSError) else None,return_value=response,create=True):
    with self.assertRaises(a.Failure):fs.acl(1)
  with patch.object(os,"getxattr",side_effect=OSError(errno.ENODATA,"SYNTHETIC"),create=True):fs.acl(1)
class ProtocolTests(unittest.TestCase):
 def test_four_commands_full_capabilities(self):
  ws=FakeWS(messages());(_,version),obs=exchange(ws)
  self.assertEqual(version,"2026.9.4");self.assertEqual(obs["capabilities"],dict.fromkeys(a.CAPABILITIES,True))
  self.assertEqual(ws.sent[1:],[dict(id=i,type=cmd) for i,cmd in enumerate(a.COMMANDS,1)]);self.assertEqual(len(ws.sent),5);self.assertTrue(ws.aborted)
 def test_all_commands_errors_id_bool_and_replay(self):
  for cmd in range(4):
   for change in (dict(success=False),dict(id=True),dict(id=99),dict(type="event"),dict(success=1)):
    ms=messages();ms[cmd+2].update(change)
    with self.subTest(command=cmd,change=change):
     with self.assertRaises(a.Failure):exchange(FakeWS(ms))
  with self.assertRaises(a.Failure):exchange(FakeWS(messages()+[dict(id=4,type="result",success=True,result=[])]))
 def test_authentication_version_consistency(self):
  for index,change in ((0,dict(type="auth_ok")),(0,dict(ha_version="unsafe")),(1,dict(type="auth_invalid")),(1,dict(ha_version="2026.8.1"))):
   ms=messages();ms[index].update(change)
   with self.assertRaises(a.Failure):exchange(FakeWS(ms))
 def test_registry_core_duplicates_and_additive(self):
  valid=[[device()],[dict(id="e",entity_id="sensor.e",platform="test",device_id=None)],[dict(area_id="a",name="room")],[dict(entry_id="c",domain="test")]]
  for i in range(4):
   bad=copy.deepcopy(valid);bad[i].append(copy.deepcopy(bad[i][0]))
   with self.assertRaises(a.Failure):a.registry_cores(bad)
  bad=copy.deepcopy(valid);bad[1].append(dict(id="other",entity_id="sensor.e",platform="test",device_id=None))
  with self.assertRaises(a.Failure):a.registry_cores(bad)
  for ds in ([dict(id="d",connections=[["mac"]])],[dict(id="d",connections=None)]):
   with self.assertRaises(a.Failure):a.registry_cores([ds,[],[],[]])
  valid[0][0]["additive"]={"safe":[True,None,1]};a.registry_cores(valid)
 def test_timeout_aborts_and_reaps_no_retry(self):
  async def check():
   events=[]
   async def stalled():await asyncio.sleep(10)
   with self.assertRaises(a.Failure):await a.bounded(stalled,time.monotonic()+.01,15,"HA_CONNECTION",lambda:events.append("abort"))
   self.assertEqual(events,["abort"])
  asyncio.run(check())

class TransactionTests(unittest.TestCase):
 def prepare(self,root,present=True):
  fs=TemporaryFS(root);old=cycle() if present else None
  if old:(fs.root/"home_assistant.json").write_bytes(a.encoded(old))
  raw,info=fs.file(fs.parent,"home_assistant.json") if old else (None,None)
  return fs,a.Publication(fs,SCHEMA),raw,info,cycle(old,ts=T1)
 def test_first_and_replacement_single_link_bytes(self):
  for present in (False,True):
   with tempfile.TemporaryDirectory() as root:
    fs,w,raw,info,candidate=self.prepare(root,present);self.assertIsNone(w.publish(candidate,raw,info,lambda:None))
    actual,meta=fs.file(fs.parent,"home_assistant.json");self.assertEqual(actual,a.encoded(candidate));self.assertEqual(meta.st_nlink,1);self.assertEqual(fs.names(fs.parent),["home_assistant.json"])
 def test_every_operation_fault_exact_lkg_or_committed_warning(self):
  for present in (False,True):
   with tempfile.TemporaryDirectory() as root:
    fs,w,raw,info,candidate=self.prepare(root,present);start=len(fs.events);w.publish(candidate,raw,info,lambda:None);length=len(fs.events)-start
   for offset in range(length):
    with self.subTest(prior=present,event=offset),tempfile.TemporaryDirectory() as root:
     fs,w,raw,info,candidate=self.prepare(root,present);fs.at=len(fs.events)+offset
     try:warning=w.publish(candidate,raw,info,lambda:None)
     except a.Failure as error:
      if error.preserved=="TRUE":
       if present:
        actual,meta=fs.file(fs.parent,"home_assistant.json");self.assertEqual(actual,raw);self.assertEqual(meta.st_ino,info.st_ino);self.assertEqual(meta.st_nlink,1)
       else:self.assertFalse((fs.root/"home_assistant.json").exists())
      else:self.assertEqual(error.preserved,"UNKNOWN")
     else:self.assertIn(warning,(None,"TRANSACTION_CLEANUP_FAILED"));self.assertEqual((fs.root/"home_assistant.json").read_bytes(),a.encoded(candidate))
 def test_inventory_change_restores_exact_inode(self):
  with tempfile.TemporaryDirectory() as root:
   fs,w,raw,info,candidate=self.prepare(root)
   def changed():raise a.Failure("CANONICAL_INVENTORY_INPUT")
   with self.assertRaises(a.Failure) as caught:w.publish(candidate,raw,info,changed)
   self.assertEqual(caught.exception.stage,"CANONICAL_INVENTORY_INPUT");actual,meta=fs.file(fs.parent,"home_assistant.json");self.assertEqual(actual,raw);self.assertEqual(meta.st_ino,info.st_ino)
 def journal(self,root,prior,replaced,committed,done=False):
  fs,w,raw,info,candidate=self.prepare(root,prior);tid="a"*32;name=".home_assistant.txn-"+tid;fs.mkdir(fs.parent,name);fd=fs.open_dir(fs.parent,name);data=a.encoded(candidate);fs.write(fd,"candidate.json",data)
  if raw is not None:fs.link(fs.parent,"home_assistant.json",fd,"prior.json")
  intent=dict(transaction_id=tid,final_basename="home_assistant.json",prior_present=raw is not None,prior_length=len(raw) if raw else 0,candidate_length=len(data),prior_sha256=a.digest(raw) if raw else None,candidate_sha256=a.digest(data));fs.write(fd,"intent.json",a.encoded(intent))
  if replaced:fs.replace(fd,"candidate.json",fs.parent,"home_assistant.json")
  if committed:fs.write(fd,"committed.json",a.encoded(dict(transaction_id=tid,intent_sha256=a.digest(a.encoded(intent)),candidate_sha256=a.digest(data))))
  if done:fs.replace(fs.parent,name,fs.parent,name.replace(".txn-",".done-"))
  return fs,w,raw,info,candidate
 def test_recovery_all_valid_boundaries(self):
  for prior in (False,True):
   for replaced,committed in ((False,False),(True,False),(True,True)):
    with tempfile.TemporaryDirectory() as root:
     fs,w,raw,info,candidate=self.journal(root,prior,replaced,committed);w.recovery()
     if committed:self.assertEqual((fs.root/"home_assistant.json").read_bytes(),a.encoded(candidate))
     elif prior:
      actual,meta=fs.file(fs.parent,"home_assistant.json");self.assertEqual(actual,raw);self.assertEqual(meta.st_ino,info.st_ino)
     else:self.assertFalse((fs.root/"home_assistant.json").exists())
     self.assertFalse(any(".txn-" in n or ".done-" in n for n in fs.names(fs.parent)))
 def test_done_partial_cleanup_never_rollback(self):
  for child in (None,"committed.json","intent.json","prior.json"):
   with tempfile.TemporaryDirectory() as root:
    fs,w,raw,info,candidate=self.journal(root,True,True,True,True);done=next(p for p in fs.root.iterdir() if ".done-" in p.name)
    if child:(done/child).unlink()
    w.recovery();self.assertEqual((fs.root/"home_assistant.json").read_bytes(),a.encoded(candidate))
 def test_multiple_malformed_unexpected_recovery_fail_closed(self):
  for change in ("multiple","marker","unexpected","intent","name"):
   with tempfile.TemporaryDirectory() as root:
    fs,w,raw,info,candidate=self.journal(root,True,True,False);txn=next(p for p in fs.root.iterdir() if ".txn-" in p.name)
    if change=="multiple":(fs.root/(".home_assistant.txn-"+"b"*32)).mkdir()
    elif change=="marker":(txn/"committed.json").write_bytes(b"{}")
    elif change=="unexpected":(txn/"unexpected").write_bytes(b"SYNTHETIC")
    elif change=="intent":(txn/"intent.json").write_bytes(b"{}")
    else:txn.rename(fs.root/".home_assistant.txn-invalid")
    before=(fs.root/"home_assistant.json").read_bytes()
    with self.assertRaises(a.Failure) as caught:w.recovery()
    self.assertEqual(caught.exception.preserved,"UNKNOWN");self.assertEqual((fs.root/"home_assistant.json").read_bytes(),before)
 def test_unproved_restore_retains_recovery_material(self):
  with tempfile.TemporaryDirectory() as root:
   fs,w,raw,info,candidate=self.journal(root,True,True,False);fs.fault="directory_sync";fs.persistent=True
   with self.assertRaises(a.Failure) as caught:w.recovery()
   self.assertEqual(caught.exception.preserved,"UNKNOWN");self.assertTrue(any(".txn-" in p.name for p in fs.root.iterdir()))
 def test_prior_enoent_only_no_migration(self):
  with tempfile.TemporaryDirectory() as root:
   fs=TemporaryFS(root);self.assertEqual(a.read_prior(fs,SCHEMA),(None,None,None))
   for raw in (b"{",a.encoded(dict(schema_version="1.0")),a.encoded({})):
    (fs.root/"home_assistant.json").write_bytes(raw)
    with self.assertRaises(a.Failure) as caught:a.read_prior(fs,SCHEMA)
    self.assertEqual(caught.exception.stage,"PRIOR_STATE_VALIDATION")
 def test_production_short_write_loop_zero_write(self):
  fs=a.PosixFS(101,101);data=b"SYNTHETIC_BYTES";buffer=bytearray()
  def short(fd,chunk):buffer.extend(chunk[:2]);return min(2,len(chunk))
  info=SimpleNamespace(st_dev=1,st_ino=1,st_mode=stat.S_IFREG|0o600,st_uid=101,st_gid=101,st_nlink=1,st_size=len(data),st_mtime_ns=0,st_ctime_ns=0)
  with patch.object(fs,"guard"),patch.object(fs,"security"),patch.object(fs,"fstat",return_value=info),patch.object(fs,"lstat",return_value=info),patch.object(a.os,"open",return_value=1),patch.object(a.os,"write",side_effect=short),patch.object(a.os,"fsync"),patch.object(a.os,"lseek"),patch.object(a.os,"read",side_effect=lambda *_:bytes(buffer)),patch.object(a.os,"close"),patch.object(a.os,"O_NOFOLLOW",0,create=True),patch.object(a.os,"O_CLOEXEC",0,create=True):
   fs.write(2,"candidate.json",data);self.assertEqual(bytes(buffer),data)
   with patch.object(a.os,"write",return_value=0):
    with self.assertRaises(a.Failure):fs.write(2,"candidate.json",data)
class InvocationTests(unittest.TestCase):
 def test_success_and_compatibility_reporting_warning(self):
  for reporting in (False,True):
   with tempfile.TemporaryDirectory() as root:
    fs=TemporaryFS(root);rt=SyntheticRuntime(fs);rt.reporting=reporting;result=a.run_cycle(rt)
    self.assertIn("RESULT="+("PASS_WITH_WARNING" if reporting else "PASS")+"\n",result);self.assertIn("STATE_PUBLISHED=TRUE",result);self.assertTrue((fs.root/".home_assistant.lock").exists())
 def test_local_failures_no_secret_or_ha(self):
  for stage in ("TARGET_VALIDATION","RUNTIME_VALIDATION","CONTRACT_VALIDATION","CANONICAL_INVENTORY_INPUT","CREDENTIAL_ACQUISITION"):
   with tempfile.TemporaryDirectory() as root:
    fs=TemporaryFS(root);rt=SyntheticRuntime(fs);rt.failure=stage;result=a.run_cycle(rt)
    self.assertIn("RESULT=FAIL",result);self.assertNotIn("HA_CONNECTION",rt.calls);self.assertNotIn("report",rt.calls);self.assertFalse((fs.root/"home_assistant.json").exists())
 def test_lock_contention_permanent_inode_presecret(self):
  with tempfile.TemporaryDirectory() as root:
   fs=TemporaryFS(root);rt=SyntheticRuntime(fs)
   with fs.lock():
    inode=(fs.root/".home_assistant.lock").stat().st_ino;result=a.run_cycle(rt);self.assertIn("LOCK_ACQUISITION_FAILED",result);self.assertNotIn("CREDENTIAL_ACQUISITION",rt.calls)
   self.assertEqual((fs.root/".home_assistant.lock").stat().st_ino,inode)
 def test_failed_cycles_and_inventory_change_exact_lkg(self):
  for failure in ("CREDENTIAL_ACQUISITION","HA_CONNECTION","COMPATIBILITY","changed"):
   with tempfile.TemporaryDirectory() as root:
    fs=TemporaryFS(root);raw=a.encoded(cycle());(fs.root/"home_assistant.json").write_bytes(raw);rt=SyntheticRuntime(fs);rt.failure=failure;rt.changed=failure=="changed";result=a.run_cycle(rt)
    self.assertIn("RESULT=FAIL",result);self.assertIn("LAST_KNOWN_GOOD_PRESERVED=TRUE",result);self.assertEqual((fs.root/"home_assistant.json").read_bytes(),raw)
 def test_compatibility_all_full_maps(self):
  dep=next(d for d in REGISTRY["dependencies"] if d["dependency_id"]=="ha_core")
  cases=[(True,dict.fromkeys(a.CAPABILITIES,True),"2026.8.1","COMPATIBLE"),(True,dict.fromkeys(a.CAPABILITIES,True),"2026.9.4","COMPATIBLE_UPDATED"),(False,dict.fromkeys(a.CAPABILITIES),None,"DEPENDENCY_UNAVAILABLE"),(True,dict.fromkeys(a.CAPABILITIES),None,"COMPATIBILITY_UNKNOWN"),(True,{**dict.fromkeys(a.CAPABILITIES,True),"authentication":False},"2026.9.4","INCOMPATIBLE")]
  for available,caps,version,status in cases:self.assertEqual(c.assess(dep,dict(available=available,observed_version=version,capabilities=caps),{},T1)["status"],status)
 def test_results_bounded_allowlisted_redacted(self):
  text=a.result_fields(observation={"observed_version":MAC,"raw":"SYNTHETIC_PRIVATE_EXCEPTION"},error=a.Failure("HA_AUTHENTICATION"))
  self.assertEqual([l.split("=")[0] for l in text.splitlines()],list(a.RESULT_FIELDS));self.assertLessEqual(len(text),4096);self.assertLessEqual(len(text.splitlines()),16)
  for value in (MAC,A,"SYNTHETIC_PRIVATE_EXCEPTION","192.168.100.251"):self.assertNotIn(value,text)
 def test_arguments_fail_nonzero(self):
  output=io.StringIO()
  with patch.object(a.sys,"stdout",output):self.assertEqual(a.main(["--endpoint","SYNTHETIC"]),1)
  self.assertIn("TARGET_VALIDATION_FAILED",output.getvalue())

class BoundaryTests(unittest.TestCase):
 def test_numeric_transport_options_no_dns_proxy_redirect(self):
  async def check():
   events=[];ws=FakeWS(messages())
   class Sock:
    def setblocking(self,value):events.append(("blocking",value))
    def close(self):events.append(("socket_close",))
   sock=Sock()
   def factory(family,kind):events.append(("socket",family,kind));return sock
   class Connector:
    def __init__(self,uri,**kwargs):
     self.uri=uri;self.kwargs=kwargs;events.append(("connector",uri,kwargs));self.assertions()
    def assertions(self):
     assert self.kwargs["sock"] is sock and self.kwargs["proxy"] is None and self.kwargs["compression"] is None and self.kwargs["ping_interval"] is None
     assert self.kwargs["max_queue"]==1 and self.kwargs["max_size"]==a.LIMIT
    def __await__(self):
     async def connected():return ws
     return connected().__await__()
   async def connected(s,address):events.append(("connect",address));self.assertIs(s,sock)
   obs={"capabilities":dict.fromkeys(a.CAPABILITIES)}
   with patch.object(asyncio.get_running_loop(),"sock_connect",new=connected),patch.object(a.socket,"getaddrinfo",side_effect=AssertionError("DNS_PROHIBITED")):
    await a.network("SYNTHETIC_INVALID_HA_CREDENTIAL",obs,Connector,factory)
   self.assertIn(("connect",("192.168.100.251",8123)),events);self.assertEqual(events[0],("socket",a.socket.AF_INET,a.socket.SOCK_STREAM))
  asyncio.run(check())
 def test_record_namespace_field_limits(self):
  for regs in ([[device(str(i),OTHER) for i in range(4097)],[],[],[]],[[],[],[dict(area_id=str(i),name="room") for i in range(2049)],[]],[[],[],[],[dict(entry_id=str(i),domain="test") for i in range(4097)]]):
   with self.assertRaises(a.Failure):a.registry_cores(regs)
  d=device();d["connections"]=[[str(i),"safe"] for i in range(129)]
  with self.assertRaises(a.Failure):a.registry_cores([[d],[],[],[]])
  regs=[[dict(id=str(i),connections=[],**{str(i)+"field"+str(j):None for j in range(100)}) for i in range(3)],[],[],[]]
  with self.assertRaises(a.Failure):a.registry_cores(regs)
 def test_private_metadata_security_and_coherent_read(self):
  fs=a.PosixFS(101,101);raw=b"SYNTHETIC"
  attrs=dict(st_dev=1,st_ino=1,st_mode=stat.S_IFREG|0o600,st_uid=101,st_gid=101,st_nlink=1,st_size=len(raw),st_mtime_ns=0,st_ctime_ns=0)
  for change in ({},{"st_uid":0},{"st_gid":0},{"st_mode":stat.S_IFREG|0o644},{"st_nlink":2},{"st_mode":stat.S_IFIFO|0o600}):
   info=SimpleNamespace(**{**attrs,**change})
   with patch.object(fs,"fstat",return_value=info),patch.object(fs,"lstat",return_value=info),patch.object(fs,"open_file",return_value=11),patch.object(fs,"read",return_value=raw),patch.object(fs,"close"),patch.object(fs,"acl"):
    if change:
     with self.assertRaises(a.Failure):fs.file(10,"home_assistant.json")
    else:self.assertEqual(fs.file(10,"home_assistant.json")[0],raw)
  info=SimpleNamespace(**attrs);changed=SimpleNamespace(**{**attrs,"st_ino":2})
  with patch.object(fs,"fstat",return_value=info),patch.object(fs,"lstat",side_effect=[info,changed]),patch.object(fs,"open_file",return_value=11),patch.object(fs,"read",return_value=raw),patch.object(fs,"close"),patch.object(fs,"acl"):
   with self.assertRaises(a.Failure):fs.file(10,"inventory.json",private=False)
 def test_credential_metadata_short_read_acl_and_missing(self):
  for change in ({"uid":1},{"gid":1},{"mode":0o644},{"nlink":2},{"kind":stat.S_IFLNK},{"kind":stat.S_IFIFO},{"short":True}):
   with tempfile.TemporaryDirectory() as root:
    fs=FixtureFS(root);(fs.root/"etc/hioc").mkdir();(fs.root/"etc/hioc/credentials").mkdir()
    for p in (fs.root/"etc/hioc",fs.root/"etc/hioc/credentials"):fs.setmeta(p,mode=0o750,gid=GID)
    target=fs.root/"etc/hioc/credentials/home_assistant.token";target.write_bytes(b"SYNTHETIC_INVALID_HA_CREDENTIAL\n");fs.setmeta(target,mode=0o640,gid=GID)
    if "short" in change:fs.short_read=True
    else:fs.setmeta(target,**change)
    fds=a.open_hierarchy(fs,GID)
    try:
     with self.assertRaises((a.Failure,OSError)):a.read_credential(fs,fds[-1],GID)
    finally:
     for fd in reversed(fds):fs.close(fd)
 def test_nss_primary_and_supplementary_reader_scope(self):
  root=SimpleNamespace(pw_name="root",pw_uid=0,pw_gid=0);user=SimpleNamespace(pw_name="jazofv1",pw_uid=101,pw_gid=123)
  group=SimpleNamespace(gr_name="jazofv1",gr_gid=123,gr_mem=[])
  self.assertEqual(a.effective_readers([root,user],[group],user,group),123)
  other=SimpleNamespace(pw_name="other",pw_uid=102,pw_gid=123)
  with self.assertRaises(a.Failure):a.effective_readers([root,user,other],[group],user,group)
  group.gr_mem=["other"];other.pw_gid=0
  with self.assertRaises(a.Failure):a.effective_readers([root,user,other],[group],user,group)
 def test_recovery_failure_blocks_new_secret_network(self):
  with tempfile.TemporaryDirectory() as root:
   fs=TemporaryFS(root);(fs.root/(".home_assistant.txn-"+"a"*32)).mkdir();rt=SyntheticRuntime(fs);result=a.run_cycle(rt)
   self.assertIn("STATE_PUBLICATION_FAILED",result);self.assertIn("LAST_KNOWN_GOOD_PRESERVED=UNKNOWN",result);self.assertNotIn("CREDENTIAL_ACQUISITION",rt.calls);self.assertNotIn("HA_CONNECTION",rt.calls)
 def test_transaction_collision_no_deletion(self):
  with tempfile.TemporaryDirectory() as root:
   fs=TemporaryFS(root);existing=fs.root/(".home_assistant.txn-"+"a"*32);existing.mkdir();(existing/"sentinel").write_bytes(b"SYNTHETIC_SENTINEL")
   with patch.object(a.os,"urandom",return_value=bytes.fromhex("a"*32)):
    with self.assertRaises(a.Failure):a.Publication(fs,SCHEMA).publish(cycle(),None,None,lambda:None)
   self.assertEqual((existing/"sentinel").read_bytes(),b"SYNTHETIC_SENTINEL")
 def test_unsafe_config_domain_omits_member_reference(self):
  e=dict(id="e",entity_id="sensor.e",platform="test",device_id="old",config_entry_id="c")
  assoc=cycle(es=[e],entries=[dict(entry_id="c",domain="invalid domain")])["associations"][0]
  self.assertEqual(assoc["relationship_status"],"INCOMPLETE");self.assertNotIn("config_entry_id",assoc["entities"][0]);self.assertNotIn("config_entries",assoc)
 def test_compatibility_other_dependencies_preserved_existing_writer(self):
  from hioc.core.state import StateStore
  with tempfile.TemporaryDirectory() as root:
   store=StateStore(Path(root));caps=dict.fromkeys(a.CAPABILITIES,True)
   before=c.update_status(store,REGISTRY,{"ha_core":dict(available=True,observed_version="2026.9.4",capabilities=caps),"mqtt_transport":dict(available=True,capabilities={"connack":True,"publish":True})},T0)
   after=c.update_status(store,REGISTRY,{"ha_core":dict(available=True,observed_version="2026.9.4",capabilities={**caps,"authentication":False})},T1)
   old=next(d for d in before["dependencies"] if d["dependency_id"]=="mqtt_transport");new=next(d for d in after["dependencies"] if d["dependency_id"]=="mqtt_transport")
   self.assertEqual(old["capabilities"],new["capabilities"]);self.assertEqual(old["status"],new["status"])
class ImplementationGovernanceTests(unittest.TestCase):
 def test_closed_record_sources_and_authority_hashes(self):
  record=json.loads((ROOT/"governance/pe4/pe4-ha-association-adapter-implementation.json").read_bytes());schema=json.loads((ROOT/"governance/pe4/pe4-ha-association-adapter-implementation.schema.json").read_bytes())
  a.check_schema_contract(schema);a.validate_schema(record,schema)
  for binding in record["sources"].values():self.assertEqual(a.digest((ROOT/binding["path"]).read_bytes()),binding["sha256"])
  for path,binding in record["authorities"].items():
   if path!="docs/HIOC_MASTER_PLAN.md":self.assertEqual(a.digest((ROOT/path).read_bytes()),binding["sha256"])
  bad=copy.deepcopy(record);bad["production_execution"]=True
  with self.assertRaises(a.Failure):a.validate_schema(bad,schema)
  bad=copy.deepcopy(record);bad["raw_token"]="SYNTHETIC_INVALID_HA_CREDENTIAL"
  with self.assertRaises(a.Failure):a.validate_schema(bad,schema)
 def test_canonical_json_and_document_links(self):
  for name in ("pe4-ha-association-adapter-implementation.json","pe4-ha-association-adapter-implementation.schema.json"):
   raw=(ROOT/"governance/pe4"/name).read_bytes();self.assertEqual(raw,a.encoded(json.loads(raw)))
  doc=ROOT/"docs/PE4_HOME_ASSISTANT_ASSOCIATION_ADAPTER_IMPLEMENTATION.md"
  for link in a.re.findall(r"\]\(([^)]+)\)",doc.read_text(encoding="utf-8")):
   if "://" not in link:self.assertTrue((doc.parent/link.split("#")[0]).resolve().exists())
 def test_import_safety_no_tools_or_stubs(self):
  import ast
  source=(ROOT/"pi4/lib/hioc/home_assistant_association.py").read_text(encoding="utf-8");tree=ast.parse(source)
  for node in ast.walk(tree):
   if isinstance(node,ast.ImportFrom):self.assertFalse((node.module or "").startswith(("tools","tests")))
   if isinstance(node,ast.Import):self.assertFalse(any(n.name.startswith(("tools","tests","jsonschema")) for n in node.names))
  self.assertNotIn("NotImplementedError",source);self.assertNotIn("TODO",source)
  self.assertNotIn("integration_inventory",source);self.assertNotIn("mqtt",source.lower())

class PreflightTests(unittest.TestCase):
 def test_exact_target_endpoint_environment_host_operator(self):
  import subprocess
  from hioc.core.config import ConfigService
  pwd=SimpleNamespace(getpwnam=lambda _:SimpleNamespace(pw_uid=101))
  for change in ({},{"endpoint":"bad"},{"endpoint":None},{"host":"other"},{"uid":0},{"env":{"hTtP_pRoXy":""}},{"env":{"HIOC_HOME":str(a.HOME)}}):
   with patch.dict(sys.modules,{"pwd":pwd}),patch.object(a.sys,"platform","linux"),patch.object(a.os,"name","posix"),patch.object(a.socket,"gethostname",return_value=change.get("host","nutandpihole")),patch.object(a.os,"getuid",return_value=change.get("uid",101),create=True),patch.object(a.os,"geteuid",return_value=change.get("uid",101),create=True),patch.dict(a.os.environ,change.get("env",{}),clear=True),patch.object(ConfigService,"load",return_value={"HIOC_HOME":str(a.HOME),"HIOC_HA_ENDPOINT":change.get("endpoint",a.ENDPOINT)}),patch.object(subprocess,"run",return_value=SimpleNamespace(returncode=0,stdout=b" inet 192.168.100.252/24 ")):
    if change:
     with self.assertRaises(a.Failure):a.Runtime().target()
    else:a.Runtime().target()
 def test_exact_runtime_and_unreviewed_pth_rejection(self):
  import platform,sysconfig,importlib.util,importlib.metadata
  with tempfile.TemporaryDirectory() as root:
   home=Path(root).resolve();env=home/"runtime/pe4/environments/cpython311-websockets16.1.1-lock-v1";site=env/"lib/python3.11/site-packages";site.mkdir(parents=True);interpreter=home/"runtime/pe4/active/bin/python"
   module=SimpleNamespace(__version__="16.1.1",__file__=str(site/"websockets/__init__.py"));distribution=SimpleNamespace(metadata={"Name":"websockets"},version="16.1.1")
   for change in ({},{"version":(3,11,3)},{"machine":"x86_64"},{"soabi":"wrong"},{"isolated":0},{"bytecode":0},{"pth":True},{"websockets":"wrong"}):
    pth=site/"unreviewed.pth"
    if change.get("pth"):pth.write_text("SYNTHETIC_UNREVIEWED")
    elif pth.exists():pth.unlink()
    module.__version__=change.get("websockets","16.1.1")
    flags=SimpleNamespace(isolated=change.get("isolated",1),dont_write_bytecode=change.get("bytecode",1))
    with patch.object(a,"HOME",home),patch.object(a,"ENVIRONMENT",env),patch.object(a,"INTERPRETER",interpreter),patch.object(a.sys,"prefix",str(env)),patch.object(a.sys,"executable",str(interpreter)),patch.object(a.sys,"version_info",change.get("version",(3,11,2))),patch.object(a.sys,"flags",flags),patch.object(a.sys,"path",[str(site),str(home/"pi4/lib")]),patch.object(platform,"machine",return_value=change.get("machine","aarch64")),patch.object(sysconfig,"get_config_var",return_value=change.get("soabi","cpython-311-aarch64-linux-gnu")),patch.object(importlib.util,"find_spec",return_value=SimpleNamespace(origin=str(site/"websockets/__init__.py"))),patch.object(importlib.metadata,"distributions",return_value=[distribution]),patch.dict(sys.modules,{"websockets":module}),patch.object(a,"identities",return_value=123):
     if change:
      with self.assertRaises(a.Failure):a.Runtime().runtime()
     else:a.Runtime().runtime()

class FinalBoundaryTests(unittest.TestCase):
 def test_unsafe_optional_area_name_omitted_only(self):
  d=device();d["area_id"]="area";assoc=cycle(ds=[d],areas=[dict(area_id="area",name="x"*257)])["associations"][0]
  self.assertEqual(assoc["area_candidate"],{"area_id":"area"});self.assertEqual(assoc["relationship_status"],"INCOMPLETE")
 def test_prior_member_duplicate_key_rejected(self):
  e=dict(id="e",entity_id="sensor.e",platform="test",device_id="old");state=cycle(es=[e]);duplicate=dict(state["associations"][0]["entities"][0]);duplicate["platform"]="other";state["associations"][0]["entities"].append(duplicate);state["summary"]["entity_memberships"]=2
  with self.assertRaises(a.Failure):a.validate_state(state,SCHEMA)
 def test_invalid_schema_number_identity_not_bool(self):
  a.validate_schema(1,{"type":"integer"})
  with self.assertRaises(a.Failure):a.validate_schema(True,{"type":"integer"})

class PriorRaceTests(unittest.TestCase):
 def test_disappearance_after_initial_probe_is_not_empty_baseline(self):
  with tempfile.TemporaryDirectory() as root:
   fs=TemporaryFS(root);(fs.root/"home_assistant.json").write_bytes(a.encoded(cycle()))
   with patch.object(fs,"file",side_effect=FileNotFoundError()):
    with self.assertRaises(a.Failure) as caught:a.read_prior(fs,SCHEMA)
   self.assertEqual(caught.exception.stage,"PRIOR_STATE_VALIDATION")

class LockBindingTests(unittest.TestCase):
 def test_guard_revalidates_permanent_lock_inode_binding(self):
  fs=a.PosixFS(101,101);fs.parent=10;fs.lock_fd=11
  attrs=dict(st_dev=1,st_ino=1,st_mode=stat.S_IFREG|0o600,st_uid=101,st_gid=101,st_nlink=1,st_size=0,st_mtime_ns=0,st_ctime_ns=0)
  before=SimpleNamespace(**attrs);swapped=SimpleNamespace(**{**attrs,"st_ino":2})
  with patch.object(fs,"security"),patch.object(fs,"fstat",return_value=before),patch.object(fs,"lstat",return_value=swapped):
   with self.assertRaises(a.Failure):fs.guard()
