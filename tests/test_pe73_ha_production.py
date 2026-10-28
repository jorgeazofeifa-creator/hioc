"""Focused Windows synthetic/native-loopback validation; never production evidence."""
import contextlib
import copy
import datetime as dt
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import socket
import ssl
import stat
import tempfile
import threading
import time
import unittest
from unittest.mock import Mock, patch

import test_pe73_ha_delivery as old
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.x509.oid import NameOID, ExtendedKeyUsageOID

spec=importlib.util.spec_from_file_location('pe73_production_test',old.ROOT/'tools/pe73_ha_production.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)


def pair(role='server', *, expired=False, address='127.0.0.1', authority=None):
    now=dt.datetime.now(dt.timezone.utc)
    if authority is None:
        ca_key=ec.generate_private_key(ec.SECP256R1())
        name=x509.Name([x509.NameAttribute(NameOID.COMMON_NAME,'Synthetic ephemeral CA')])
        ca=(x509.CertificateBuilder().subject_name(name).issuer_name(name).public_key(ca_key.public_key())
            .serial_number(x509.random_serial_number()).not_valid_before(now-dt.timedelta(days=1))
            .not_valid_after(now+dt.timedelta(days=10)).add_extension(x509.BasicConstraints(ca=True,path_length=1),True)
            .add_extension(x509.KeyUsage(False,False,False,False,False,True,True,False,False),True)
            .sign(ca_key,hashes.SHA256()))
    else: ca,ca_key=authority
    key=ec.generate_private_key(ec.SECP256R1())
    builder=(x509.CertificateBuilder().subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME,'Synthetic '+role)]))
        .issuer_name(ca.subject).public_key(key.public_key()).serial_number(x509.random_serial_number())
        .not_valid_before(now-dt.timedelta(days=2)).not_valid_after(now+dt.timedelta(days=-1 if expired else 2))
        .add_extension(x509.BasicConstraints(ca=False,path_length=None),True)
        .add_extension(x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH if role=='server' else ExtendedKeyUsageOID.CLIENT_AUTH]),False))
    if role=='server':
        import ipaddress
        builder=builder.add_extension(x509.SubjectAlternativeName([x509.IPAddress(ipaddress.ip_address(address))]),False)
    leaf=builder.sign(ca_key,hashes.SHA256())
    pem=lambda cert:cert.public_bytes(serialization.Encoding.PEM)
    return dict(cert=pem(leaf),key=key.private_bytes(serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,serialization.NoEncryption()),ca=pem(ca),
        authority=(ca,ca_key),pin=p.spki(leaf))


class CertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=pair();cls.client=pair('client',authority=cls.server['authority'])
    def test_valid_server(self):
        v=self.server;self.assertEqual(p.validate_material(v['cert'],v['key'],v['ca'],'backend','127.0.0.1'),v['pin'])
    def test_valid_client(self):
        v=self.client;self.assertEqual(p.validate_material(v['cert'],v['key'],v['ca'],'ha','127.0.0.1'),v['pin'])
    def test_expired(self):
        v=pair(expired=True)
        with self.assertRaisesRegex(p.Stop,'EXPIRED'):p.validate_material(v['cert'],v['key'],v['ca'],'backend','127.0.0.1')
    def test_key_mismatch(self):
        v=self.server
        with self.assertRaisesRegex(p.Stop,'KEY_MISMATCH'):p.validate_material(v['cert'],self.client['key'],v['ca'],'backend','127.0.0.1')
    def test_wrong_server_san(self):
        v=self.server
        with self.assertRaisesRegex(p.Stop,'IDENTITY_MISMATCH'):p.validate_material(v['cert'],v['key'],v['ca'],'backend','127.0.0.2')
    def test_wrong_eku(self):
        v=self.client
        with self.assertRaisesRegex(p.Stop,'ROLE_MISMATCH'):p.validate_material(v['cert'],v['key'],v['ca'],'backend','127.0.0.1')
    def test_malformed_certificate_sanitized(self):
        result=p.sanitized(lambda:p.validate_material(b'PRIVATE_SENTINEL',b'PRIVATE_KEY',b'CA','ha','127.0.0.1'))
        self.assertEqual(result['RESULT'],'BLOCKED_NATIVE_BINDING_CHECK')
        self.assertNotIn('PRIVATE',json.dumps(result))
    def test_bad_ca_constraints(self):
        v=self.server
        with self.assertRaisesRegex(p.Stop,'CA_CONSTRAINTS'):p.validate_material(v['cert'],v['key'],v['cert'],'backend','127.0.0.1')


class PrivateFileTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.ops=old.RootOps(self.root)
        self.private=self.root/'homeassistant/private';self.private.mkdir()
        self.setmeta(self.private,0,0,0o700)
        self.secret=self.private/'key';self.secret.write_bytes(b'x'*32)
        self.reader=p.PrivateFiles('/homeassistant/private',(0,0),_ops=self.ops)
    def setmeta(self,path,uid,gid,mode):
        v=path.stat();self.ops.attrs[(v.st_dev,v.st_ino)]=(uid,gid,mode)
    def tearDown(self):self.assertFalse(self.ops.fds)
    def test_valid_native_mode_model(self):self.assertEqual(self.reader.read('/homeassistant/private/key'),b'x'*32)
    def test_wrong_file_mode(self):
        self.setmeta(self.secret,0,0,0o644)
        with self.assertRaisesRegex(p.Stop,'FILE_SECURITY'):self.reader.read('/homeassistant/private/key')
    def test_wrong_owner(self):
        self.setmeta(self.secret,1000,1000,0o600)
        with self.assertRaisesRegex(p.Stop,'FILE_SECURITY'):self.reader.read('/homeassistant/private/key')
    def test_wrong_parent_mode(self):
        self.setmeta(self.private,0,0,0o755)
        with self.assertRaisesRegex(p.Stop,'PARENT_SECURITY'):self.reader.read('/homeassistant/private/key')
    def test_writable_ancestor(self):
        self.setmeta(self.root/'homeassistant',0,0,0o777)
        with self.assertRaisesRegex(p.Stop,'ANCESTOR_UNSAFE'):self.reader.read('/homeassistant/private/key')
    def test_parent_owner_not_role(self):
        self.setmeta(self.private,1000,1000,0o700)
        with self.assertRaisesRegex(p.Stop,'ANCESTOR_UNSAFE'):self.reader.read('/homeassistant/private/key')
    def test_file_acl(self):
        self.ops.acl['/homeassistant/private/key']='present'
        with self.assertRaisesRegex(p.Stop,'ACL_PRESENT'):self.reader.read('/homeassistant/private/key')
    def test_unknown_acl(self):
        self.ops.acl['/homeassistant/private']='unknown'
        with self.assertRaisesRegex(p.Stop,'ACL_UNKNOWN'):self.reader.read('/homeassistant/private/key')
    def test_hardlink(self):
        os.link(self.secret,self.private/'link')
        with self.assertRaisesRegex(p.Stop,'FILE_SECURITY'):self.reader.read('/homeassistant/private/key')
    def test_symlink_open_error_preserved_without_mutation(self):
        original=self.ops.open
        def deny(name,*a,**kw):
            if name=='key':raise OSError(40,'fixture only')
            return original(name,*a,**kw)
        self.ops.open=deny
        with self.assertRaises(OSError):self.reader.read('/homeassistant/private/key')
        self.assertFalse(self.ops.log)
    def test_outside_private_parent(self):
        with self.assertRaisesRegex(p.Stop,'OUTSIDE'):self.reader.read('/homeassistant/key')
    def test_exclusive_provision_and_collision_refusal(self):
        self.reader.provision('/homeassistant/private/new',b'fixture')
        with self.assertRaises(FileExistsError):self.reader.provision('/homeassistant/private/new',b'other')
        self.assertEqual(self.reader.read('/homeassistant/private/new'),b'fixture')
    def test_zero_length_and_missing_refused(self):
        self.secret.write_bytes(b'')
        with self.assertRaisesRegex(p.Stop,'FILE_SECURITY'):self.reader.read('/homeassistant/private/key')
        with self.assertRaises(FileNotFoundError):self.reader.read('/homeassistant/private/absent')
    def test_named_identity_change_during_read(self):
        read=self.ops.read;changed=False
        def drift(fd,count):
            nonlocal changed
            raw=read(fd,count)
            if not changed:
                changed=True;self.setmeta(self.secret,0,0,0o644)
            return raw
        self.ops.read=drift
        with self.assertRaisesRegex(p.Stop,'FILE_DRIFT'):self.reader.read('/homeassistant/private/key')


class MemorySecrets:
    def __init__(self,values):self.values=values
    @contextlib.contextmanager
    def opened(self,path):
        if path not in self.values:raise FileNotFoundError('synthetic absent')
        yield self.values[path],7,(1,2,0,0,0o100600,1,len(self.values[path]),1,1)


def trust_fixture(role='ha',key=b's'*32):
    server=pair();client=pair('client',authority=server['authority'])
    ha,backend=old.configs()
    ha.update(assertion_key_file='/config/private/hmac',client_certificate='/config/private/cert',
        client_key='/config/private/key',server_ca='/config/private/ca',server_url='https://127.0.0.1:12345')
    backend.update(bind_address='127.0.0.1',ha_address='127.0.0.1',server_certificate='/private/cert',server_key='/private/key',client_ca='/private/ca')
    backend['issuer_trusts'][0].update(assertion_key_file='/private/hmac',client_spki_sha256=client['pin'])
    packet=p.d.disabled_trust(ha,backend)
    material=client if role=='ha' else server
    root='/homeassistant/private' if role=='ha' else '/private'
    secrets=MemorySecrets({root+'/cert':material['cert'],root+'/key':material['key'],root+'/ca':material['ca'],root+'/hmac':key})
    trust=p.TrustSide(role,secrets,lambda:copy.deepcopy(packet),core_root='/homeassistant' if role=='ha' else None)
    return trust,packet,server,client


class TrustTests(unittest.TestCase):
    def setUp(self):self.trust,self.packet,_,_=trust_fixture()
    def test_valid_shared_32_bytes(self):
        with self.trust.material() as (_,_,key):self.assertEqual(len(key),32)
    def test_short_key(self):
        self.trust.files.values['/homeassistant/private/hmac']=b'a'*31
        with self.assertRaisesRegex(p.Stop,'32_BYTES'):
            with self.trust.material():pass
    def test_missing_key(self):
        del self.trust.files.values['/homeassistant/private/hmac']
        with self.assertRaises(FileNotFoundError):
            with self.trust.material():pass
    def test_wrong_spki(self):
        self.packet['backend']['issuer_trusts'][0]['client_spki_sha256']='b'*64
        with self.assertRaisesRegex(p.Stop,'SPKI'):
            with self.trust.material():pass
    def test_changed_key_after_first_check(self):
        with self.trust.material():pass
        self.trust.files.values['/homeassistant/private/hmac']=b'z'*32
        with self.assertRaisesRegex(p.Stop,'TRUST_MATERIAL_DRIFT'):
            with self.trust.material():pass
    def test_enabled_role_refused(self):
        self.packet['ha']['hioc_operator']['operator']['enabled']=True
        with self.assertRaisesRegex(p.Stop,'ACTIVATION'):
            with self.trust.material():pass
    def test_acl_wildcard_refused(self):
        self.packet['backend']['issuer_trusts'][0]['actors']['fixture_operator']['get']=['*']
        with self.assertRaisesRegex(p.Stop,'ACL_ASSET'):
            with self.trust.material():pass
    def test_actor_allowlist_mismatch(self):
        self.packet['backend']['issuer_trusts'][0]['actors']['other']={'get':['dev_0123456789abcdef']}
        with self.assertRaisesRegex(p.Stop,'INDEPENDENT_ACL'):
            with self.trust.material():pass
    def test_issuer_mismatch(self):
        self.packet['backend']['issuer_trusts'][0]['key_id']='other'
        with self.assertRaisesRegex(p.Stop,'ISSUER_TRUST'):
            with self.trust.material():pass
    def test_unmapped_core_secret_path_refused(self):
        with self.assertRaisesRegex(p.Stop,'CORE_PRIVATE_MAPPING'):self.trust.path('/somewhere/key')


class SyntheticTLS:
    def __init__(self,sock,certificate=None):self.sock=sock;self.certificate=certificate
    def version(self):return 'TLSv1.3'
    def getpeername(self):return ('127.0.0.1',12345)
    def getpeercert(self,binary_form=False):return self.certificate if binary_form else {'subject':'synthetic'}
    def __getattr__(self,name):return getattr(self.sock,name)


class LiveProtocolTests(unittest.TestCase):
    def session(self, *, key_mismatch=False, packet_mismatch=False, drift=False):
        client,packet,server_cert,client_cert=trust_fixture()
        server_packet=copy.deepcopy(packet)
        if packet_mismatch:server_packet['backend']['issuer_trusts'][0]['actors']['fixture_operator']['get']=['dev_1111111111111111']
        files=MemorySecrets({'/private/cert':server_cert['cert'],'/private/key':server_cert['key'],
            '/private/ca':server_cert['ca'],'/private/hmac':b'q'*32 if key_mismatch else b's'*32})
        server=p.TrustSide('backend',files,lambda:copy.deepcopy(server_packet))
        left,right=socket.socketpair();self.addCleanup(left.close);self.addCleanup(right.close)
        der=x509.load_pem_x509_certificate(client_cert['cert']).public_bytes(serialization.Encoding.DER)
        self.errors=[];self.observations=0;self.changed=False
        def observe():
            self.observations+=1
            return {'boot':'synthetic','scheduler':'changed' if self.changed or drift and self.observations>1 else 'same'}
        def run():
            try:p.GuardServer(server,observe,'WHOLE_PROCESS_FIXTURE').handle(SyntheticTLS(right,der))
            except BaseException as error:self.errors.append(error)
            finally:right.close()
        thread=threading.Thread(target=run,daemon=True);thread.start()
        self.addCleanup(lambda:thread.join(2))
        return p.Peer(SyntheticTLS(left),client,'WHOLE_PROCESS_FIXTURE'),packet
    def test_fresh_challenge_and_stable_identity(self):
        peer,packet=self.session();a=peer.check(packet);b=peer.check(packet)
        self.assertEqual(a,b);self.assertEqual(peer.count,2);self.assertEqual(self.observations,2)
    def test_mismatched_hmac_pair(self):
        peer,packet=self.session(key_mismatch=True)
        with self.assertRaisesRegex(p.Stop,'HMAC_PAIR'):peer.check(packet)
        self.assertTrue(peer.stopped)
    def test_independent_backend_acl_cannot_be_overwritten_by_ha(self):
        peer,packet=self.session(packet_mismatch=True)
        with self.assertRaises(p.Stop):peer.check(packet)
        self.assertTrue(peer.stopped)
    def test_backend_drift_refuses_second_check(self):
        peer,packet=self.session(drift=True);peer.check(packet)
        with self.assertRaises(p.Stop):peer.check(packet)
        self.assertEqual(self.observations,2)
    def test_old_saved_receipt_not_admitted(self):
        peer,packet=self.session();peer.channel.close()
        with self.assertRaises((p.Stop,OSError)):peer.check(packet)
    def test_deadline_has_no_network_or_retry(self):
        trust,packet,_,_=trust_fixture();channel=Mock();peer=p.Peer(channel,trust,'WHOLE_PROCESS_FIXTURE',clock=lambda:901);peer.start=0
        with self.assertRaisesRegex(p.Stop,'EXPIRED'):peer.check(packet)
        channel.assert_not_called()
    def test_spki_pin_applies_to_actual_peer_certificate(self):
        trust,packet,_,client=trust_fixture();wrong=pair('client')
        channel=SyntheticTLS(Mock(),x509.load_pem_x509_certificate(wrong['cert']).public_bytes(serialization.Encoding.DER))
        with self.assertRaisesRegex(p.Stop,'SPKI'):p.peer_identity(channel,packet,'backend')
    def test_malformed_response_is_not_private_output(self):
        result=p.sanitized(lambda:(_ for _ in ()).throw(RuntimeError('SECRET_TOKEN')))
        self.assertNotIn('SECRET_TOKEN',json.dumps(result))


class NativeTLSLoopbackTests(unittest.TestCase):
    """Real OpenSSL mutual TLS on Windows loopback, no native Linux claim."""
    def exercise(self, wrong_ca=False, wrong_hostname=False, no_client=False):
        server=pair();client=pair('client',authority=server['authority'])
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary)
            for label,value in [('server.crt',server['cert']),('server.key',server['key']),('client.crt',client['cert']),('client.key',client['key'])]:
                (root/label).write_bytes(value)
            s=ssl.create_default_context(ssl.Purpose.CLIENT_AUTH,cadata=server['ca'].decode())
            s.minimum_version=ssl.TLSVersion.TLSv1_2;s.verify_mode=ssl.CERT_REQUIRED
            s.load_cert_chain(root/'server.crt',root/'server.key')
            c=ssl.create_default_context(cadata=(pair()['ca'] if wrong_ca else server['ca']).decode())
            c.minimum_version=ssl.TLSVersion.TLSv1_2
            if not no_client:c.load_cert_chain(root/'client.crt',root/'client.key')
            errors=[]
            with socket.socket() as listener:
                listener.bind(('127.0.0.1',0));listener.listen(1);listener.settimeout(3)
                def accept():
                    try:
                        raw,_=listener.accept()
                        with raw:
                            raw.settimeout(3)
                            with s.wrap_socket(raw,server_side=True) as channel:
                                self.assertTrue(channel.getpeercert());channel.sendall(b'qualified')
                    except BaseException as error:errors.append(error)
                thread=threading.Thread(target=accept);thread.start()
                try:
                    with socket.create_connection(listener.getsockname(),timeout=3) as raw:
                        with c.wrap_socket(raw,server_hostname='127.0.0.2' if wrong_hostname else '127.0.0.1') as channel:
                            self.assertEqual(channel.recv(32),b'qualified')
                finally:thread.join(4)
                self.assertFalse(thread.is_alive())
                if errors:raise errors[0]
    def test_actual_mutual_tls(self):self.exercise()
    def test_untrusted_server_ca(self):
        with self.assertRaises(ssl.SSLError):self.exercise(wrong_ca=True)
    def test_hostname_verification_not_disabled(self):
        with self.assertRaises(ssl.SSLError):self.exercise(wrong_hostname=True)
    def test_missing_client_certificate(self):
        with self.assertRaises((ssl.SSLError,AssertionError)):self.exercise(no_client=True)


class RouteTests(unittest.TestCase):
    def probe(self,body=b'editor',status=200,headers=None):
        self.response=Mock();self.response.status=status;self.response.read.return_value=body
        self.response.getheader.side_effect=lambda k:(headers or {}).get(k)
        self.connection=Mock();self.connection.getresponse.return_value=self.response
        self.connection.sock.getpeername.return_value=('192.168.100.251',443)
        self.factory=Mock(return_value=self.connection)
        return p.RouteProbe('https://ha.example.test','192.168.100.251',_connection=self.factory)
    def test_real_http_adapter_reads_exact_bytes_and_closes(self):
        probe=self.probe();result=probe('/local/hioc-asset-editor.js',hashlib.sha256(b'editor').hexdigest())
        self.assertEqual(result['status'],200);self.connection.close.assert_called_once()
        self.assertTrue(self.factory.call_args.kwargs['context'].check_hostname)
    def test_http_redirect_refused(self):
        with self.assertRaisesRegex(p.Stop,'RESPONSE_INVALID'):self.probe(status=302)('/local/hioc-asset-editor.js','a'*64)
        self.connection.close.assert_called_once()
    def test_wrong_bytes_refused(self):
        with self.assertRaisesRegex(p.Stop,'BYTES_MISMATCH'):self.probe()('/local/hioc-asset-editor.js','a'*64)
    def test_compression_refused(self):
        with self.assertRaisesRegex(p.Stop,'RESPONSE_INVALID'):self.probe(headers={'Content-Encoding':'gzip'})('/local/hioc-asset-editor.js','a'*64)
    def test_http_plaintext_or_credentials_refused(self):
        for origin in ('http://ha.example','https://user:secret@ha.example','https://ha.example/path'):
            with self.subTest(origin=origin),self.assertRaises(p.Stop):p.RouteProbe(origin,'192.168.100.251')
    def test_unexpected_actual_frontend_address_refused(self):
        probe=self.probe();self.connection.sock.getpeername.return_value=('192.168.100.252',443)
        with self.assertRaisesRegex(p.Stop,'PEER_ADDRESS'):probe('/local/hioc-asset-editor.js','a'*64)
    def test_changed_tls_policy_refused_before_http(self):
        probe=self.probe();probe.context.check_hostname=False;probe.context.verify_mode=ssl.CERT_NONE
        with self.assertRaisesRegex(p.Stop,'TLS_POLICY'):probe('/local/hioc-asset-editor.js','a'*64)
        self.factory.assert_not_called()


class OrderingTests(unittest.TestCase):
    def setUp(self):
        self.fixture=old.DeliveryAcceptanceTests('test_integrated_delivery_exact_files_resource_card_trust_disabled')
        self.fixture.setUp();self.addCleanup(self.fixture.doCleanups)
        self.f=self.fixture
    def test_http_route_occurs_after_files_before_resource_and_repeated_finally(self):
        calls=[]
        def route(url,expected):
            for source,target in old.h.FILES.items():self.assertEqual(self.f.fs.read(target,0o644),old.SOURCE[source])
            calls.append([x['type'] for x in self.f.api.calls if x['type'] in old.h.MUTATIONS])
            return {'url':url,'sha256':expected,'status':200,'identity_encoding':True}
        self.f.driver.route_probe=route;self.f.run_delivery()
        self.assertEqual(calls,[[],list(old.h.MUTATIONS)])
    def test_http_failure_no_registration_explicit_recovery(self):
        self.f.driver.route_probe=Mock(side_effect=OSError('private route failure'))
        with self.assertRaises(OSError):self.f.run_delivery()
        self.assertEqual(self.f.fs.load()['state'],'LOCAL_ROUTE_BLOCKED')
        self.assertFalse([x for x in self.f.api.calls if x['type'] in old.h.MUTATIONS])
        self.f.driver.restore_files(recovery_reference='EXPLICIT_OPERATOR_RECOVERY')
        self.assertEqual(self.f.fs.load()['state'],'FILES_RESTORED')
        self.f.driver.route_probe.assert_called_once()
    def test_missing_route_binding_stops_before_any_write(self):
        self.f.driver.route_probe=None
        with self.assertRaisesRegex(old.h.Stop,'ROUTE_BINDING'):self.f.run_delivery()
        self.assertEqual(self.f.fs.begins,0)
    def test_other_dashboard_refused_before_write(self):
        self.f.plan['dashboard']='alternate'
        with self.assertRaisesRegex(old.h.Stop,'EXCLUSIVE_HIOC'):self.f.run_delivery()
        self.assertEqual(self.f.fs.begins,0)
    def test_other_view_refused_before_write(self):
        self.f.plan['view']='hioc-v2-operations'
        with self.assertRaisesRegex(old.h.Stop,'INVENTORY_VIEW'):self.f.run_delivery()
    def test_all_six_views_and_existing_sections_order_preserved(self):
        names=['executive','operations','diagnostics','inventory','network','servers']
        original={'views':[{'path':'hioc-v2-'+x,'type':'sections','sections':[
            {'type':'grid','cards':[{'type':'markdown','content':'same '+x}]}]} for x in names],'theme':'unchanged'}
        self.f.api.config=copy.deepcopy(original);self.f.run_delivery()
        after=self.f.api.config
        self.assertEqual(after['views'][:3]+after['views'][4:],original['views'][:3]+original['views'][4:])
        self.assertEqual(after['views'][3]['sections'][:-1],original['views'][3]['sections'])
        self.assertEqual(after['views'][3]['sections'][-1],{'type':'grid','cards':[old.h.CARD]})
        self.assertEqual(after['theme'],original['theme'])
    def test_route_malformed_proof_leaves_files_only(self):
        self.f.driver.route_probe=lambda *_:True
        with self.assertRaisesRegex(old.h.Stop,'LOCAL_RESOURCE_NOT_VERIFIED'):self.f.run_delivery()
        self.assertEqual(self.f.fs.load()['state'],'LOCAL_ROUTE_BLOCKED')
    def test_final_route_failure_keeps_nonterminal_no_automatic_restore(self):
        count=0
        def route(url,expected):
            nonlocal count
            count+=1
            if count==2:raise OSError('private')
            return {'url':url,'sha256':expected,'status':200,'identity_encoding':True}
        self.f.driver.route_probe=route
        with self.assertRaises(OSError):self.f.run_delivery()
        self.assertEqual(self.f.fs.load()['state'],'VERIFYING')
        with self.assertRaisesRegex(old.h.Stop,'RECOVERY_ADJUDICATION'):self.f.driver.restore_files(recovery_reference='EXPLICIT_NEW_RECOVERY')


class BindingGuardTests(unittest.TestCase):
    def setUp(self):
        self.trust,self.packet,_,_=trust_fixture()
        self.peer=Mock();self.peer.check.return_value='opaque-session'
        self.api=Mock();self.api.call.side_effect=lambda v: {'components':[]} if v['type']=='get_config' else {'resource_mode':'storage'} if v['type']=='lovelace/info' else [] if v['type']=='lovelace/resources/list' else {}
        self.local=Mock(return_value={'host_identity':'observed','capability_identity':'approved'})
        self.b=p.Bindings(Mock(),self.api,self.trust,self.peer,self.local)
    def test_only_after_all_fresh_checks_are_fields_true(self):
        self.assertTrue(self.b.guard()['exclusive_delivery']);self.peer.check.assert_called_once()
    def test_peer_failure_cannot_be_true(self):
        self.peer.check.side_effect=p.Stop('PEER_FAILED')
        with self.assertRaisesRegex(p.Stop,'PEER_FAILED'):self.b.guard()
        self.local.assert_not_called()
    def test_local_drift_refused(self):
        self.b.guard();self.local.return_value={'host_identity':'different','capability_identity':'approved'}
        with self.assertRaisesRegex(p.Stop,'HA_LIVE_DRIFT'):self.b.guard()
    def test_loaded_integration_refused_even_no_services(self):
        self.api.call.side_effect=lambda v:{'components':['hioc_operator']} if v['type']=='get_config' else {}
        with self.assertRaisesRegex(p.Stop,'ALREADY_LOADED'):self.b.guard()
    def test_services_refused(self):
        self.api.call.return_value={'hioc_operator':{}};self.api.call.side_effect=None
        with self.assertRaisesRegex(p.Stop,'SERVICES_ALREADY_ACTIVE'):self.b.guard()
    def test_native_factory_rejects_fixture_or_receipt_admission(self):
        with self.assertRaisesRegex(p.Stop,'NATIVE_BINDING_TYPES'):p.native_delivery(Mock(),Mock(),self.trust,self.peer,self.local,Mock(),Mock())
    def test_fresh_session_does_not_corrupt_persisted_host_identity(self):
        first=self.b.guard();self.peer.check.return_value='different-fresh-live-session'
        self.assertEqual(self.b.guard(),first)
        self.assertEqual(self.peer.check.call_count,2)
    def test_requirement_report_contains_no_real_values_or_keys(self):
        result=p.requirements();self.assertFalse(result['production_ready']);self.assertFalse(result['mutation_performed'])
        self.assertEqual(result['PE74'],'NOT_AUTHORIZED')


class DeliveryAPITests(unittest.TestCase):
    def setUp(self):
        self.proxy=Mock(authenticated=True,counter=0,calls=[])
        self.fs=Mock();self.api=p.DeliveryAPI(self.proxy,self.fs)
    def test_unknown_write_refused(self):
        with self.assertRaisesRegex(p.Stop,'OUTSIDE_SCOPE'):self.api.call({'type':'call_service','domain':'hioc_operator'})
        self.proxy._frame.assert_not_called()
    def test_other_dashboard_read_refused(self):
        with self.assertRaisesRegex(p.Stop,'EXCLUSIVE_HIOC'):self.api.call({'type':'lovelace/config','url_path':'other'})
    def test_no_resource_write_without_route_and_intent(self):
        self.fs.load.return_value={'dashboard':p.d.DASHBOARD,'whole_process_reference':'WHOLE_PROCESS_APPROVED','route':None}
        with self.assertRaisesRegex(p.Stop,'VERIFIED_ROUTE'):self.api.call({'type':'lovelace/resources/create','res_type':'module','url':'/local/hioc-asset-editor.js'})
        self.proxy._frame.assert_not_called()
    def test_exact_resource_intent_single_attempt_lost_ack(self):
        self.fs.load.return_value=dict(dashboard=p.d.DASHBOARD,whole_process_reference='WHOLE_PROCESS_APPROVED',
            route={'url':'/local/hioc-asset-editor.js','sha256':p.d.MANIFEST['homeassistant/www/hioc-asset-editor.js'][0],
                'status':200,'identity_encoding':True},state='REGISTERING_RESOURCE',pending='resource')
        self.proxy._receive.side_effect=OSError('private lost ack')
        command={'type':'lovelace/resources/create','res_type':'module','url':'/local/hioc-asset-editor.js'}
        with self.assertRaises(OSError):self.api.call(command)
        with self.assertRaises(p.Stop):self.api.call(command)
        self.proxy._frame.assert_called_once()
    def test_legacy_import_guard_precedes_resource_list(self):
        self.proxy._receive.side_effect=[{'id':1,'type':'result','success':True,'result':[]},
            {'id':2,'type':'result','success':True,'result':{'resources':[]}}]
        with self.assertRaises(Exception):self.api.call({'type':'lovelace/resources/list'})
        self.assertEqual(self.proxy.calls,['lovelace/dashboards/list','lovelace/config'])
    def test_safe_absent_legacy_then_resources(self):
        self.proxy._receive.side_effect=[{'id':1,'type':'result','success':True,'result':[]},
            {'id':2,'type':'result','success':False,'error':{'code':'config_not_found'}},
            {'id':3,'type':'result','success':True,'result':[{'id':str(n),'url':'/fixture-'+str(n),'type':'module'} for n in range(11)]}]
        self.assertEqual(len(self.api.call({'type':'lovelace/resources/list'})),11)
        self.assertEqual(self.proxy.calls[-1],'lovelace/resources/list')
    def test_encoded_editor_conflict_refused(self):
        rows=[{'id':str(n),'url':'/fixture-'+str(n),'type':'module'} for n in range(11)]
        rows[0]['url']='/local/%68ioc-asset-editor.js'
        self.proxy._receive.side_effect=[{'id':1,'type':'result','success':True,'result':[]},
            {'id':2,'type':'result','success':True,'result':{'views':[]}},
            {'id':3,'type':'result','success':True,'result':rows}]
        with self.assertRaisesRegex(p.Stop,'RESOURCE_CONFLICT'):self.api.call({'type':'lovelace/resources/list'})
        self.assertFalse(self.api.sent)
    def test_malformed_resource_row_refused(self):
        with self.assertRaisesRegex(p.Stop,'RESOURCE_SCHEMA'):self.api._resources([{'url':None,'type':'module'}])
    def test_only_exact_own_journaled_resource_is_allowed(self):
        own={'id':'published','url':'/local/hioc-asset-editor.js','type':'module'}
        self.api.sent.add('lovelace/resources/create');self.fs.load.return_value={'resource':own}
        self.api._resources([own])
        with self.assertRaisesRegex(p.Stop,'RESOURCE_CONFLICT'):self.api._resources([own|{'id':'other'}])


class NativeStateTests(unittest.TestCase):
    """Native state logic with explicit Windows metadata seams, not PI5 evidence."""
    def setUp(self):
        self.fs=Mock();self.fs._proof={'boot_id':'boot','terminal':{'id':'terminal'},
            'core_container':{'id':'core'},'core':{'pid':12,'uid':0,'gid':0},'root':'/homeassistant'}
        self.cap={'components/frontend/__init__.py':{'sha256':'a'*64}}
        self.fs._probe.public_capabilities.return_value=copy.deepcopy(self.cap)
        self.files=Mock();self.files.parent='/homeassistant/private';self.records={}
        self.files.provision.side_effect=lambda name,raw:self.records.__setitem__(name,raw)
        self.files.read.side_effect=lambda name:self.records[name]
        self.host=p.digest(self.fs._proof)
    def state(self):
        with patch.object(Path,'read_text',return_value='boot'):
            return p.NativeHAState(self.fs,self.files,'/homeassistant/private/pe73-delivery-lease.json',
                'WHOLE_PROCESS_APPROVED',self.host,{'components/frontend/__init__.py':'a'*64},risk_acknowledgement=p.RISKS)
    def test_requires_new_exclusive_lease(self):
        state=self.state()
        with self.assertRaisesRegex(p.Stop,'LEASE_REQUIRED'):state()
    def test_fresh_lease_and_actual_native_proof(self):
        state=self.state();state.acquire()
        with patch.object(Path,'read_text',return_value='boot'):self.assertEqual(state()['host_identity'],self.host)
        self.fs._live.assert_called_once()
    def test_no_second_acquisition(self):
        state=self.state();state.acquire()
        with self.assertRaisesRegex(p.Stop,'NO_RETRY'):state.acquire()
        self.files.provision.assert_called_once()
    def test_boot_drift_fails_no_cleanup(self):
        state=self.state();state.acquire()
        with patch.object(Path,'read_text',return_value='new-boot'),self.assertRaisesRegex(p.Stop,'BOOT_DRIFT'):state()
        self.assertEqual(len(self.records),1)
    def test_lease_mutation_fails(self):
        state=self.state();state.acquire();self.records[state.lease_path]=b'other'
        with self.assertRaisesRegex(p.Stop,'LEASE_DRIFT'):state()
    def test_mapping_implementation_drift_fails(self):
        state=self.state();state.acquire();self.fs._probe.public_capabilities.return_value={'components/frontend/__init__.py':{'sha256':'b'*64}}
        with patch.object(Path,'read_text',return_value='boot'),self.assertRaisesRegex(p.Stop,'MAPPING_IMPLEMENTATION_DRIFT'):state()
    def test_changed_core_fails(self):
        state=self.state();state.acquire();self.fs._proof['core']['pid']=13
        with patch.object(Path,'read_text',return_value='boot'),self.assertRaisesRegex(p.Stop,'HOST_OR_CORE_DRIFT'):state()
    def test_arbitrary_lease_path_cannot_create_parallel_exclusion(self):
        with patch.object(Path,'read_text',return_value='boot'),self.assertRaisesRegex(p.Stop,'FIXED_EXCLUSION_LEASE'):
            p.NativeHAState(self.fs,self.files,'/homeassistant/private/other','WHOLE_PROCESS_APPROVED',
                self.host,{'components/frontend/__init__.py':'a'*64},risk_acknowledgement=p.RISKS)
    def test_native_proof_failure_preserved(self):
        state=self.state();state.acquire();self.fs._live.side_effect=OSError('private')
        with patch.object(Path,'read_text',return_value='boot'),self.assertRaises(OSError):state()


class BackendStateTests(unittest.TestCase):
    def setUp(self):
        self.files=Mock();self.files.parent='/private';self.record={}
        self.files.provision.side_effect=lambda name,raw:self.record.__setitem__(name,raw)
        self.files.read.side_effect=lambda name:self.record[name]
        self.ops=Mock(boot_id='boot');self.ops.target_boot.return_value='boot'
        self.ops.scheduler.return_value=b'# synthetic restored cron\n'
        self.ops.processes.return_value={'inspection_complete':True,'known_active':[]}
        self.runtime=Mock()
        self.runtime.snapshot.side_effect=lambda name,mode:{'exists':False} if name=='config/pe7_availability.json' else {
            'exists':True,'sha256':next(x['sha256'] for x in old.existing.d.MANIFEST if x['path']==name)}
        self.provider=Mock();self.provider.NativeOps.return_value=self.ops
        self.controller=Mock(MANIFEST=old.existing.d.MANIFEST);self.controller.NativeFS.return_value=self.runtime
    def sibling(self,name):return self.provider if name=='pe73_maintenance_window' else self.controller
    def state(self):
        with patch.object(p,'sibling',side_effect=self.sibling):
            return p.NativeBackendState(self.files,'/private/pe73-delivery-lease.json','WHOLE_PROCESS_APPROVED',
                p.d.sha(self.ops.scheduler.return_value),risk_acknowledgement=p.RISKS)
    def call(self,state):
        with patch.object(p,'sibling',side_effect=self.sibling):return state()
    def test_actual_live_readers_and_13_identities_required(self):
        state=self.state();state.acquire();self.assertTrue(self.call(state)['disabled'])
        self.assertEqual(self.runtime.snapshot.call_count,14)
    def test_reboot_refuses(self):
        state=self.state();state.acquire();self.ops.target_boot.return_value='new-boot'
        with self.assertRaisesRegex(p.Stop,'BOOT_OR_LEASE'):self.call(state)
    def test_no_old_lease_admission(self):
        state=self.state()
        with self.assertRaisesRegex(p.Stop,'BOOT_OR_LEASE'):self.call(state)
    def test_changed_scheduler_refuses(self):
        state=self.state();state.acquire();self.ops.scheduler.return_value=b'changed\n'
        with self.assertRaisesRegex(p.Stop,'SCHEDULER_DRIFT'):self.call(state)
    def test_affected_consumer_refuses(self):
        state=self.state();state.acquire();self.ops.processes.return_value['known_active']=[{'synthetic':True}]
        with self.assertRaisesRegex(p.Stop,'NOT_DRAINED'):self.call(state)
    def test_incomplete_process_observation_refuses(self):
        state=self.state();state.acquire();self.ops.processes.return_value['inspection_complete']=False
        with self.assertRaisesRegex(p.Stop,'NOT_DRAINED'):self.call(state)
    def test_runtime_payload_change_refuses(self):
        state=self.state();state.acquire();self.runtime.snapshot.side_effect=lambda *_:{'exists':True,'sha256':'bad'}
        with self.assertRaisesRegex(p.Stop,'PAYLOAD_DRIFT'):self.call(state)
    def test_enabled_evaluator_refuses(self):
        state=self.state();state.acquire()
        snapshot=self.runtime.snapshot.side_effect
        self.runtime.snapshot.side_effect=lambda name,mode:{'exists':True} if name=='config/pe7_availability.json' else snapshot(name,mode)
        self.runtime.read.return_value=b'{"enabled":true,"notifications_enabled":false}'
        with self.assertRaisesRegex(p.Stop,'RUNTIME_ENABLED'):self.call(state)
    def test_scheduler_with_pe7_activation_refuses(self):
        self.ops.scheduler.return_value=b'* * * * * hioc-incident-engine-v2.py --pe7-cycle\n'
        state=self.state();state.acquire()
        with self.assertRaisesRegex(p.Stop,'SCHEDULER_ENABLED'):self.call(state)


class AdditionalNegativeTests(unittest.TestCase):
    def test_native_packet_refuses_synthetic_callback_reader(self):
        with self.assertRaisesRegex(p.Stop,'NATIVE_PACKET_READER'):p.native_packet(Mock(),'/private/packet')
    def test_no_app_credential_means_no_socket(self):
        with patch.dict(os.environ,{},clear=True),patch.object(p.LIVE,'Proxy') as constructor,self.assertRaisesRegex(p.Stop,'AUTHENTICATION_REQUIRED'):
            with p.authenticated_proxy():pass
        constructor.assert_not_called()
    def test_certificate_context_uses_held_descriptors(self):
        trust,_,_,_=trust_fixture();context=Mock(check_hostname=True)
        with patch.object(p.ssl,'create_default_context',return_value=context),trust.context() as (actual,_,_):
            self.assertIs(actual,context)
        context.load_cert_chain.assert_called_once_with('/proc/self/fd/7','/proc/self/fd/7')
        self.assertEqual(context.minimum_version,ssl.TLSVersion.TLSv1_2)
        self.assertEqual(context.verify_mode,ssl.CERT_REQUIRED)
    def test_backend_listener_refuses_fixture_admission_before_socket(self):
        with patch.object(p.socket,'socket') as create,self.assertRaisesRegex(p.Stop,'NATIVE_BACKEND'):
            p.serve_guard(Mock(),Mock(),1234)
        create.assert_not_called()
    def test_guard_client_refuses_fixture_admission_before_socket(self):
        with patch.object(p.socket,'create_connection') as create,self.assertRaisesRegex(p.Stop,'NATIVE_CLIENT'):
            with p.connect_peer(Mock(),1234,'WHOLE_PROCESS_APPROVED'):pass
        create.assert_not_called()
    def test_only_fixed_dashboard_is_saved_after_exact_intent(self):
        proxy=Mock(authenticated=True,counter=0,calls=[]);fs=Mock();api=p.DeliveryAPI(proxy,fs)
        fs.load.return_value={'dashboard':p.d.DASHBOARD,'whole_process_reference':'WHOLE_PROCESS_APPROVED',
            'route':{'url':'/local/hioc-asset-editor.js','sha256':p.d.MANIFEST['homeassistant/www/hioc-asset-editor.js'][0],
                'status':200,'identity_encoding':True},'state':'REGISTERING_CARD','pending':'dashboard',
            'observation':{'after':{'views':[]}}}
        with self.assertRaisesRegex(p.Stop,'DASHBOARD_INTENT'):
            api.call({'type':'lovelace/config/save','url_path':'other','config':{'views':[]}})
        proxy._frame.assert_not_called()


class IntegratedBindingsTests(unittest.TestCase):
    def setUp(self):
        self.fixture=old.DeliveryAcceptanceTests('test_integrated_delivery_exact_files_resource_card_trust_disabled')
        self.fixture.setUp();self.addCleanup(self.fixture.doCleanups)
        self.protocol=LiveProtocolTests('test_fresh_challenge_and_stable_identity')
        self.addCleanup(self.protocol.doCleanups)
        self.peer,self.packet=self.protocol.session()
        f=self.fixture
        class API:
            def call(_,value):
                return {'components':[]} if value['type']=='get_config' else f.api.call(value)
        api=API()
        bindings=p.Bindings(f.fs,api,self.peer.trust,self.peer,
            lambda:{'host_identity':'synthetic native seam','capability_identity':'approved synthetic mapping'})
        self.driver=p.d.Delivery(f.fs,api,bindings.guard,bindings.trust_preflight,
            lambda release,path:old.SOURCE[path],route_probe=f.driver.route_probe)
        f.plan['ha_trust']=self.packet['ha']['hioc_operator']['operator']
        f.plan['backend_trust']=self.packet['backend']
    def test_complete_shared_key_guard_existing_transaction_route_and_inventory(self):
        result=self.driver.run(self.fixture.plan,whole_process_reference='WHOLE_PROCESS_FIXTURE')
        self.assertEqual(result['state'],'DELIVERED_DISABLED');self.assertGreater(self.peer.count,10)
        self.assertFalse(result['activation'])
        self.fixture.fs.assert_unrelated(self)
    def test_backend_drift_after_first_file_stops_no_registration_or_retry(self):
        publish=self.fixture.fs.publish
        def drift(*args):
            result=publish(*args);self.protocol.changed=True;return result
        self.fixture.fs.publish=drift
        with self.assertRaises(p.Stop):self.driver.run(self.fixture.plan,whole_process_reference='WHOLE_PROCESS_FIXTURE')
        self.assertEqual(len(self.fixture.fs.load()['installed']),1)
        self.assertFalse([x for x in self.fixture.api.calls if x['type'] in p.d.MUTATIONS])
    def test_wrong_process_reference_is_not_fresh_backend_authority(self):
        self.peer.reference='DIFFERENT_PROCESS_REFERENCE'
        with self.assertRaises(p.Stop):self.driver.run(self.fixture.plan,whole_process_reference='WHOLE_PROCESS_FIXTURE')
        self.assertEqual(self.fixture.fs.begins,0)


if __name__=='__main__':unittest.main()
