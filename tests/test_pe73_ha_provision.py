"""Ephemeral repository fixtures only; no Pi, credentials or production access."""
import base64
import contextlib
import copy
import importlib.util
import json
from pathlib import Path
import ssl
import tempfile
import unittest
from unittest.mock import Mock, patch

import test_pe73_ha_production as prior

spec=importlib.util.spec_from_file_location('pe73_provision_test',prior.old.ROOT/'tools/pe73_ha_provision.py')
q=importlib.util.module_from_spec(spec);spec.loader.exec_module(q)
p=prior.p

def plan():
    return dict(backend_address='192.168.100.252',ha_address='192.168.100.251',backend_port=18443,
        guard_port=18444,private_name='synthetic',ha_parent='/config/synthetic',
        backend_parent='/home/jazofv1/hioc/synthetic',ca_name='Ephemeral fixture CA',
        server_name='Fixture backend',client_name='Fixture HA',valid_days=2,
        issuer='123456781234423482341234567890ab',key_id='fixture_key',
        actors={'synthetic_operator':{'get':['dev_0123456789abcdef']}},
        frontend_origin='https://ha.invalid',reference='PE73_FIXTURE_AUTHORIZATION',
        toolkit='/home/jazofv1/fixture',helper_sha256='a'*64)

class Files(prior.MemorySecrets):
    def __init__(self,parent,values=None):
        self.parent=parent;self.writes=[];self.fail=None
        super().__init__({parent+'/'+k:v for k,v in (values or {}).items()})
    def read(self,path):
        if path not in self.values:raise FileNotFoundError(path)
        return self.values[path]
    def provision(self,path,raw):
        if path in self.values:raise FileExistsError(path)
        if path==self.fail:raise OSError('PRIVATE_SYNTHETIC_FAILURE')
        self.values[path]=raw;self.writes.append(path)

class IssuanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan=plan();cls.password=b'fixture password not a production secret'
        cls.material=q.backend_material(cls.plan,cls.password)
        cls.key,cls.csr=q.create_request(cls.plan)
        cls.chain,_=q.issue(cls.plan,cls.material['ca.pem'],cls.material['ca-offline.key'],cls.password,csr_raw=cls.csr)
    def test_real_ca_and_both_chains(self):
        ca=p.certificates(self.material['ca.pem'])[0]
        ca.verify_directly_issued_by(ca)
        for raw in (self.material['server-chain.pem'],self.chain):
            certs=p.certificates(raw);self.assertEqual(len(certs),2)
            certs[0].verify_directly_issued_by(certs[1])
    def test_server_pair_san_and_eku(self):
        m=self.material
        p.validate_material(m['server-chain.pem'],m['server.key'],m['ca.pem'],'backend',self.plan['backend_address'])
    def test_client_pair_eku_and_spki(self):
        self.assertEqual(p.validate_material(self.chain,self.key,self.material['ca.pem'],'ha',self.plan['backend_address']),p.spki(p.certificates(self.chain)[0]))
    def test_ca_is_encrypted(self):
        _,_,s,*_=q.crypto()
        with self.assertRaises(TypeError):s.load_pem_private_key(self.material['ca-offline.key'],None)
        with self.assertRaises(ValueError):s.load_pem_private_key(self.material['ca-offline.key'],b'wrong password')
    def test_client_private_key_never_issued_on_backend(self):
        _,private=q.issue(self.plan,self.material['ca.pem'],self.material['ca-offline.key'],self.password,csr_raw=self.csr)
        self.assertIsNone(private)
    def test_fresh_randomness(self):
        other=q.backend_material(self.plan,self.password)
        for name in ('assertion.key','server.key','ca-offline.key'):
            self.assertNotEqual(other[name],self.material[name])
        self.assertEqual(len(other['assertion.key']),32)
    def test_wrong_key(self):
        with self.assertRaisesRegex(p.Stop,'KEY_MISMATCH'):
            p.validate_material(self.chain,self.material['server.key'],self.material['ca.pem'],'ha',self.plan['backend_address'])
    def test_expired_time(self):
        import datetime
        with self.assertRaisesRegex(p.Stop,'EXPIRED'):
            p.validate_material(self.chain,self.key,self.material['ca.pem'],'ha',self.plan['backend_address'],now=datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(days=10))
    def test_wrong_server_identity(self):
        m=self.material
        with self.assertRaisesRegex(p.Stop,'IDENTITY'):
            p.validate_material(m['server-chain.pem'],m['server.key'],m['ca.pem'],'backend','192.168.100.1')
    def test_wrong_csr_subject_refused_before_import(self):
        other=copy.deepcopy(self.plan);other['client_name']='Other HA'
        with self.assertRaisesRegex(q.Blocked,'SUBJECT'):q.validate_request(other,self.csr)
    def test_wrong_csr_san(self):
        x,h,s,ec,_,oid=q.crypto();key=ec.generate_private_key(ec.SECP256R1())
        import ipaddress
        raw=(x.CertificateSigningRequestBuilder().subject_name(x.Name([x.NameAttribute(oid.COMMON_NAME,self.plan['client_name'])]))
             .add_extension(x.SubjectAlternativeName([x.IPAddress(ipaddress.ip_address('192.168.100.1'))]),False)
             .sign(key,h.SHA256()).public_bytes(s.Encoding.PEM))
        with self.assertRaisesRegex(q.Blocked,'SAN'):q.validate_request(self.plan,raw)
    def test_bad_spki(self):
        with self.assertRaises(p.Stop):q.packet(self.plan,'not a pin',p)
    def test_short_ca_password(self):
        with self.assertRaises(q.Blocked):q.generate_ca(self.plan,b'short')
    def test_existing_binding_consumes_generated_material(self):
        value=q.packet(self.plan,p.spki(p.certificates(self.chain)[0]),p)
        root='/homeassistant/synthetic'
        files=Files(root,{'client-chain.pem':self.chain,'client.key':self.key,'ca.pem':self.material['ca.pem'],'assertion.key':self.material['assertion.key']})
        with p.TrustSide('ha',files,lambda:value,core_root='/homeassistant').material() as (actual,_,key):
            self.assertEqual(actual,value);self.assertEqual(key,self.material['assertion.key'])
        self.assertFalse(value['ha']['hioc_operator']['operator']['enabled'])
        self.assertFalse(value['ha']['hioc_operator']['observations']['enabled'])
        self.assertFalse(value['ha']['hioc_operator']['notifications']['enabled'])
        self.assertFalse(value['backend']['enabled'])
        self.assertFalse(value['backend']['issuer_trusts'][0]['enabled'])

class PolicyTests(unittest.TestCase):
    def bad(self,key,value):
        v=plan();v[key]=value
        with self.assertRaises((ValueError,TypeError)):q.validate_plan(v)
    def test_invalid_issuer(self):self.bad('issuer','not an issuer')
    def test_missing_issuer(self):
        v=plan();del v['issuer']
        with self.assertRaises(q.Blocked):q.validate_plan(v)
    def test_no_wildcard_asset(self):self.bad('actors',{'actor':{'get':['*']}})
    def test_no_unapproved_operation(self):self.bad('actors',{'actor':{'delete':['dev_0123456789abcdef']}})
    def test_no_empty_actor_scope(self):self.bad('actors',{})
    def test_no_application_guard_port_alias(self):self.bad('guard_port',18443)
    def test_no_privileged_port(self):self.bad('guard_port',443)
    def test_no_remote_endpoint_substitution(self):self.bad('backend_address','192.168.100.1')
    def test_no_external_frontend_credentials(self):self.bad('frontend_origin','https://secret@ha.invalid')
    def test_no_http_frontend(self):self.bad('frontend_origin','http://ha.invalid')
    def test_no_private_parent_escape(self):self.bad('backend_parent','/etc/ssl')
    def test_exact_fields(self):
        v=plan();v['enable']=True
        with self.assertRaises(q.Blocked):q.validate_plan(v)

class DurableBoundaryTests(unittest.TestCase):
    def test_completion_packet_last(self):
        f=Files('/fixture');q.stage(f,{'plan.json':b'{}','ca.pem':b'public'},packet_value={'enabled':False})
        self.assertEqual(f.writes,['/fixture/plan.json','/fixture/ca.pem','/fixture/packet.json'])
    def test_preexisting_destination_refuses_before_any_write(self):
        f=Files('/fixture',{'ca.pem':b'keep'})
        with self.assertRaises(q.Blocked):q.stage(f,{'plan.json':b'{}','ca.pem':b'other'})
        self.assertEqual(f.writes,[]);self.assertEqual(f.read('/fixture/ca.pem'),b'keep')
    def test_partial_write_retained_and_no_completion(self):
        f=Files('/fixture');f.fail='/fixture/ca.pem'
        with self.assertRaises(OSError):q.stage(f,{'plan.json':b'{}','ca.pem':b'public'},packet_value={})
        self.assertEqual(f.writes,['/fixture/plan.json']);self.assertNotIn('/fixture/packet.json',f.values)
        with self.assertRaises(q.Blocked):q.stage(f,{'plan.json':b'{}','ca.pem':b'public'})
    def test_path_escape_rejected(self):
        f=Files('/fixture')
        with self.assertRaises(q.Blocked):q.stage(f,{'../other':b'not written'})
        self.assertEqual(f.writes,[])
    def test_existing_native_factory_still_rejects_fixture_reader(self):
        with self.assertRaises(p.Stop):p.native_packet(Files('/fixture'),'/fixture/packet.json')

class TransferTests(unittest.TestCase):
    def test_existing_host_key_and_no_auth_prompt_or_forwarding(self):
        with patch.object(q.shutil,'which',return_value='/usr/bin/ssh'),patch.object(q.subprocess,'run',return_value=Mock(returncode=0,stdout=b'{}')) as run:
            self.assertEqual(q.ssh(p,'/home/jazofv1/fixture','a'*64,plan()['backend_parent'],22,'plan'),b'{}')
        argv=run.call_args.args[0]
        for expected in ('StrictHostKeyChecking=yes','BatchMode=yes','ClearAllForwardings=yes','RequestTTY=no','jazofv1@192.168.100.252'):
            self.assertIn(expected,argv)
        self.assertEqual(run.call_count,1);self.assertEqual(run.call_args.kwargs['input'],b'')
    def test_transfer_failure_does_not_disclose_private_output(self):
        with patch.object(q.shutil,'which',return_value='ssh'),patch.object(q.subprocess,'run',return_value=Mock(returncode=1,stdout=b'PRIVATE_KEY',stderr=b'PRIVATE_ACL')) as run:
            with self.assertRaisesRegex(q.Blocked,'AUTHENTICATED_PRIVATE_TRANSFER_BLOCKED') as caught:
                q.ssh(p,'/fixture','a'*64,plan()['backend_parent'],22,'bundle')
        self.assertNotIn('PRIVATE_KEY',str(caught.exception));self.assertEqual(run.call_count,1)
    def test_missing_crypto_stops_before_native_or_mutation(self):
        with patch.object(q,'crypto',side_effect=q.Blocked('missing')),patch.object(q,'native') as native:
            with self.assertRaises(q.Blocked):q.main(['backend-init'])
            native.assert_not_called()
    def test_inadequate_crypto_api_fails_closed(self):
        x,*_=q.crypto()
        with patch.object(x,'load_pem_x509_certificates',create=True,new=None):
            with self.assertRaises(q.Blocked):q.crypto()

class ProbeTests(unittest.TestCase):
    def test_probe_has_no_native_private_reads(self):
        with contextlib.ExitStack() as stack:
            stack.enter_context(patch.object(q.sys,'platform','linux'))
            for name in ('getuid','geteuid','getgid','getegid'):stack.enter_context(patch.object(q.os,name,return_value=0,create=True))
            stack.enter_context(patch.object(q.shutil,'which',return_value=None))
            stack.enter_context(patch.object(q.Path,'is_file',return_value=False))
            native=stack.enter_context(patch.object(q,'native'))
            result=q.probe_pi5();native.assert_not_called()
        self.assertEqual(result['RESULT'],'PASS_READ_ONLY_PROVISIONING_RUNTIME_ASSESSMENT')
        self.assertFalse(result['mutations_performed']);self.assertFalse(result['credentials_read']);self.assertFalse(result['production_ready'])


class HandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy=plan();cls.password=b'ephemeral synthetic password'
        cls.material=q.backend_material(cls.policy,cls.password)
        cls.key,cls.request=q.create_request(cls.policy)
    def setUp(self):
        self.backend=Files(self.policy['backend_parent'],{'plan.json':q.canonical(self.policy),**self.material,'client.csr':self.request})
        self.ha=Files('/homeassistant/synthetic',{'plan.json':q.canonical(self.policy),'client.key':self.key,'client.csr':self.request})
        # Fixture adapters do not weaken the actual NativePacket factory. The
        # unchanged factory explicitly rejects fixtures in a separate test.
        self.addCleanup(patch.stopall)
        patch.object(p,'native_packet',side_effect=lambda files,path:lambda:json.loads(files.read(path))).start()
        @contextlib.contextmanager
        def context(trust):
            with trust.material() as material:yield material
        patch.object(p.TrustSide,'context',context).start()
    def issued(self):
        result=q.finish_backend(self.backend,self.password,p)
        self.assertEqual(result['RESULT'],'PASS_BACKEND_OFFLINE_ISSUANCE')
        return q.export_bundle(self.backend,p)
    def test_full_two_host_transfer_and_existing_trust_compatibility(self):
        raw=self.issued();result=q.finish_ha(self.ha,raw,p,'/homeassistant')
        self.assertEqual(result['RESULT'],'PASS_HA_DISABLED_TRUST_PROVISIONING')
        self.assertEqual(result['cross_host_live_validation'],'REQUIRED')
        self.assertEqual(self.ha.read(self.ha.parent+'/client.key'),self.key)
        self.assertEqual(self.ha.read(self.ha.parent+'/assertion.key'),self.backend.read(self.backend.parent+'/assertion.key'))
        self.assertTrue(self.backend.writes[-1].endswith('/packet.json'))
        self.assertTrue(self.ha.writes[-1].endswith('/packet.json'))
    def test_no_private_ca_or_server_or_ha_key_export(self):
        raw=self.issued();value=json.loads(raw)
        self.assertEqual(set(value),{'plan','packet','ca','client_chain','assertion'})
        for key in ('ca-offline.key','server.key'):self.assertNotIn(self.material[key],raw)
        self.assertNotIn(self.key,raw)
    def test_backend_key_drift_refuses_stale_transfer(self):
        self.issued();self.backend.values[self.backend.parent+'/assertion.key']=b'x'*32
        with self.assertRaisesRegex(q.Blocked,'CURRENT_BACKEND_HMAC_MISMATCH'):q.export_bundle(self.backend,p)
    def test_short_transfer_key_before_writes(self):
        value=json.loads(self.issued());value['assertion']=base64.b64encode(b'x'*31).decode()
        with self.assertRaisesRegex(q.Blocked,'HMAC_LENGTH'):q.finish_ha(self.ha,q.canonical(value),p,'/homeassistant')
        self.assertEqual(self.ha.writes,[])
    def test_wrong_pin_before_writes(self):
        value=json.loads(self.issued());value['packet']['backend']['issuer_trusts'][0]['client_spki_sha256']='b'*64
        with self.assertRaisesRegex(q.Blocked,'SPKI'):q.finish_ha(self.ha,q.canonical(value),p,'/homeassistant')
        self.assertEqual(self.ha.writes,[])
    def test_independent_acl_plan_cannot_be_replaced(self):
        value=json.loads(self.issued());value['plan']['actors']={'other':{'get':['dev_0123456789abcdef']}}
        with self.assertRaisesRegex(q.Blocked,'INDEPENDENT_PLAN'):q.finish_ha(self.ha,q.canonical(value),p,'/homeassistant')
        self.assertEqual(self.ha.writes,[])
    def test_existing_complete_state_refuses_second_issuance(self):
        self.issued();before=copy.deepcopy(self.backend.values)
        with self.assertRaisesRegex(q.Blocked,'COMPLETION'):q.finish_backend(self.backend,self.password,p)
        self.assertEqual(before,self.backend.values)
    def test_partial_ha_state_kept_without_completion(self):
        raw=self.issued();self.ha.fail=self.ha.parent+'/client-chain.pem'
        with self.assertRaises(OSError):q.finish_ha(self.ha,raw,p,'/homeassistant')
        self.assertIn(self.ha.parent+'/ca.pem',self.ha.values)
        self.assertNotIn(self.ha.parent+'/packet.json',self.ha.values)
        with self.assertRaises(q.Blocked):q.finish_ha(self.ha,raw,p,'/homeassistant')
    def test_receipts_exclude_private_scope_and_material(self):
        result=q.finish_backend(self.backend,self.password,p);raw=q.canonical(result)
        for value in (self.password,self.material['assertion.key'],self.key,b'synthetic_operator',b'dev_0123456789abcdef'):
            self.assertNotIn(value,raw)
    def test_owner_and_symlink_security_delegated_to_existing_reader(self):
        # This is a deliberate unsafe-reader rejection, not native fixture proof.
        raw=self.issued()
        with patch.object(self.ha,'read',side_effect=p.Stop('PRIVATE_FILE_SECURITY')):
            with self.assertRaises(p.Stop):q.finish_ha(self.ha,raw,p,'/homeassistant')
    def test_source_pins_match_published_native_dependencies(self):
        for name,digest in q.PINS.items():
            self.assertEqual(q.sha((prior.old.ROOT/'tools'/(name+'.py')).read_bytes()),digest)


class GeneratedNativeTLSLoopbackTests(unittest.TestCase):
    def test_issued_material_completes_actual_openssl_mutual_tls(self):
        import socket,threading
        policy=plan();password=b'ephemeral test CA password'
        materials=q.backend_material(policy,password);key,csr=q.create_request(policy)
        chain,_=q.issue(policy,materials['ca.pem'],materials['ca-offline.key'],password,csr_raw=csr)
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary)
            for name,raw in {'s.crt':materials['server-chain.pem'],'s.key':materials['server.key'],'c.crt':chain,'c.key':key}.items():
                (root/name).write_bytes(raw)
            server=ssl.create_default_context(ssl.Purpose.CLIENT_AUTH,cadata=materials['ca.pem'].decode())
            server.minimum_version=ssl.TLSVersion.TLSv1_2;server.verify_mode=ssl.CERT_REQUIRED
            server.load_cert_chain(root/'s.crt',root/'s.key')
            client=ssl.create_default_context(cadata=materials['ca.pem'].decode())
            client.minimum_version=ssl.TLSVersion.TLSv1_2;client.load_cert_chain(root/'c.crt',root/'c.key')
            with socket.socket() as listener:
                listener.bind(('127.0.0.1',0));listener.listen(1);listener.settimeout(5)
                outcomes=[]
                def receive():
                    try:
                        raw,_=listener.accept();raw.settimeout(5)
                        with server.wrap_socket(raw,server_side=True) as channel:
                            x,*_=q.crypto()
                            outcomes.append(p.spki(x.load_der_x509_certificate(channel.getpeercert(binary_form=True))))
                            channel.sendall(b'fixture')
                    except BaseException as error:outcomes.append(type(error).__name__)
                thread=threading.Thread(target=receive,daemon=True);thread.start()
                with socket.create_connection(listener.getsockname(),timeout=5) as raw:
                    with client.wrap_socket(raw,server_hostname=policy['backend_address']) as channel:
                        self.assertEqual(channel.recv(7),b'fixture')
                thread.join(5);self.assertFalse(thread.is_alive())
                self.assertEqual(outcomes,[p.spki(p.certificates(chain)[0])])

if __name__=='__main__':unittest.main()
