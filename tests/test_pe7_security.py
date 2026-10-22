"""Signed service/actor/ACL fixtures. Keys are synthetic ephemeral test bytes."""
import copy
from datetime import timedelta
import json
import unittest
import uuid
from unittest.mock import Mock
from hioc.availability_contract import canonical, digest, timestamp, time_text
from hioc.availability_protocol import IssuerTrust, Protocol, sign
import test_pe7_evaluation as fixture


class SecurityTests(unittest.TestCase):
    def setUp(self):
        self.issuer = uuid.uuid4().hex
        self.secret = bytes(range(32))
        self.peer = 'b'*64
        self.trust = IssuerTrust(self.issuer, 'synthetic_test_only', self.secret, self.peer,
            {'synthetic_operator': {name: frozenset([fixture.ID]) for name in ('get', 'create', 'update', 'result')}}, True)
        self.service = Mock()
        self.service.get_policy.return_value = {'fixture': 'authorized_read'}
        self.service.mutate_policy.return_value = {'fixture': 'authorized_mutation'}
        self.now = timestamp(fixture.TS)
        self.protocol = Protocol(self.service, lambda issuer, key: self.trust, lambda: self.now)

    def request(self, operation='get', payload=None):
        payload = payload or dict(asset_id=fixture.ID)
        path = '/pe7/v1/policy/'+operation
        assertion = dict(issuer=self.issuer, audience='hioc.pe7.asset', key_id='synthetic_test_only',
            actor_id='synthetic_operator', context_id='synthetic_context', request_id=uuid.uuid4().hex,
            issued_at=time_text(self.now), expires_at=time_text(self.now+timedelta(seconds=30)),
            method='POST', path=path, payload_sha256=digest(payload))
        return path, sign(assertion, payload, self.secret)

    def send(self, request, **kwargs):
        path, envelope = request
        return self.protocol.handle(path, canonical(envelope), self.peer, **kwargs)

    def test_authorized_read_preserves_service_actor_separation(self):
        self.assertEqual(self.send(self.request()), {'fixture': 'authorized_read'})
        self.service.get_policy.assert_called_once_with(fixture.ID)
        self.service.mutate_policy.assert_not_called()

    def test_certificate_or_key_does_not_replace_actor_acl(self):
        request = self.request()
        self.trust.actors.clear()
        self.assertEqual(self.send(request)['error_code'], 'FORBIDDEN')
        self.service.get_policy.assert_not_called()

    def test_wrong_revoked_certificate_key_issuer_audience_actor(self):
        for field, value in (('issuer', uuid.uuid4().hex), ('audience', 'hioc.pe7.observation'),
                             ('key_id', 'unknown_key'), ('actor_id', 'forged_actor')):
            request = self.request(); request[1]['assertion'][field] = value
            result = self.send(request)
            self.assertEqual(result['result'], 'error')
        path, value = self.request()
        self.assertEqual(self.protocol.handle(path, canonical(value), 'c'*64)['error_code'], 'TRUST_INVALID')
        self.trust = IssuerTrust(self.issuer, 'synthetic_test_only', self.secret, self.peer, self.trust.actors, False)
        self.assertEqual(self.send(self.request())['error_code'], 'TRUST_INVALID')
        self.service.get_policy.assert_not_called()

    def test_signature_payload_path_and_method_are_bound(self):
        path, envelope = self.request()
        envelope['signature'] = '0'*64
        self.assertEqual(self.send((path, envelope))['error_code'], 'TRUST_INVALID')
        path, envelope = self.request(); envelope['payload']['asset_id'] = 'dev_1111111111111111'
        self.assertEqual(self.send((path, envelope))['result'], 'error')
        path, envelope = self.request()
        self.assertEqual(self.protocol.handle(path+'/extra', canonical(envelope), self.peer)['result'], 'error')
        self.assertEqual(self.send(self.request(), method='GET')['result'], 'error')
        self.service.get_policy.assert_not_called()

    def test_nonce_replay_and_expiry_boundaries(self):
        request = self.request()
        self.send(request)
        self.assertEqual(self.send(request)['error_code'], 'REPLAY_CONFLICT')
        request = self.request(); self.now += timedelta(seconds=30)
        self.assertEqual(self.send(request)['error_code'], 'ASSERTION_EXPIRED')
        request = self.request(); self.now -= timedelta(seconds=1)
        self.assertEqual(self.send(request)['error_code'], 'ASSERTION_EXPIRED')

    def test_size_depth_duplicates_extra_fields_and_cors_fail_closed(self):
        path, envelope = self.request()
        raw = canonical(envelope)
        variants = [raw+b' '*8192, raw.replace(b'"schema_version":"1.0"', b'"schema_version":"1.0","schema_version":"1.0"')]
        for data in variants:
            self.assertEqual(self.protocol.handle(path, data, self.peer)['result'], 'error')
        for kwargs in ({'origin':'https://untrusted.invalid'}, {'content_encoding':'gzip'}, {'content_type':'text/plain'}):
            self.assertEqual(self.send(self.request(), **kwargs)['result'], 'error')
        for payload in ({'asset_id':fixture.ID, 'notes':'private'}, {'asset_id':fixture.ID, 'actor_id':'admin'},
                        {'asset_id':fixture.ID, 'shell':'whoami'}):
            self.assertEqual(self.send(self.request(payload=payload))['result'], 'error')
        self.service.get_policy.assert_not_called()

    def test_under_lock_reauthorization_rechecks_revocation(self):
        payload = dict(asset_id=fixture.ID, store_epoch=uuid.uuid4().hex, expected_store_revision=1,
                       expected_revision=1, operation_id=uuid.uuid4().hex, fields={'expected_availability':False})
        self.send(self.request('update', payload))
        reauthorize = self.service.mutate_policy.call_args.args[-1]
        self.assertIs(reauthorize(), True)
        self.trust.actors.clear()
        from hioc.availability_contract import PolicyError
        with self.assertRaises(PolicyError): reauthorize()

    def test_quota_and_capacity_are_bounded(self):
        for count in range(11):
            payload = dict(asset_id=fixture.ID, store_epoch=uuid.uuid4().hex, expected_store_revision=1,
                expected_revision=1, operation_id=uuid.uuid4().hex, fields={'expected_availability':False})
            result = self.send(self.request('update', payload))
        self.assertEqual(result['error_code'], 'RATE_LIMITED')
        self.protocol.nonce_capacity = len(self.protocol.nonces)
        self.assertEqual(self.send(self.request())['error_code'], 'BUSY')

    def test_sanitized_failure_has_no_exception_or_private_payload(self):
        self.service.get_policy.side_effect = OSError('secret private hostname credential')
        result = self.send(self.request())
        self.assertEqual(set(result), {'schema_version', 'operation_id', 'result', 'error_code', 'commit_state', 'retryable'})
        self.assertNotIn('secret', json.dumps(result))
        self.assertNotIn(fixture.ID, json.dumps(result))


if __name__ == '__main__': unittest.main()


class NativeTLSTests(unittest.TestCase):
    def test_real_mtls_requires_client_certificate_and_independent_pin(self):
        import datetime,ipaddress,ssl,tempfile,threading,http.client
        from pathlib import Path
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes,serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        from hioc.availability_server import server_context,create_server
        from hioc.availability_protocol import peer_public_key_sha256
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);root.chmod(0o700)
            key=rsa.generate_private_key(public_exponent=65537,key_size=2048)
            name=x509.Name([x509.NameAttribute(NameOID.COMMON_NAME,'HIOC synthetic native fixture')])
            now=datetime.datetime.now(datetime.timezone.utc)
            ca=x509.CertificateBuilder().subject_name(name).issuer_name(name).public_key(key.public_key()).serial_number(x509.random_serial_number()).not_valid_before(now-datetime.timedelta(minutes=1)).not_valid_after(now+datetime.timedelta(days=1)).add_extension(x509.BasicConstraints(ca=True,path_length=0),critical=True).sign(key,hashes.SHA256())
            def put(name,raw):
                path=root/name;path.write_bytes(raw);path.chmod(0o600);return str(path)
            ca_path=put('ca.pem',ca.public_bytes(serialization.Encoding.PEM))
            def leaf(label,server=False):
                private=rsa.generate_private_key(public_exponent=65537,key_size=2048)
                builder=x509.CertificateBuilder().subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME,label)])).issuer_name(name).public_key(private.public_key()).serial_number(x509.random_serial_number()).not_valid_before(now-datetime.timedelta(minutes=1)).not_valid_after(now+datetime.timedelta(days=1))
                if server:builder=builder.add_extension(x509.SubjectAlternativeName([x509.IPAddress(ipaddress.ip_address('127.0.0.1'))]),critical=False)
                cert=builder.sign(key,hashes.SHA256())
                return cert,put(label+'.pem',cert.public_bytes(serialization.Encoding.PEM)),put(label+'.key',private.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,serialization.NoEncryption()))
            _,server_cert,server_key=leaf('server',True)
            client,client_cert,client_key=leaf('client')
            peer=peer_public_key_sha256(client.public_bytes(serialization.Encoding.DER))
            issuer=uuid.uuid4().hex;secret=b't'*32
            trust=IssuerTrust(issuer,'synthetic',secret,peer,{'actor':{'get':frozenset([fixture.ID])}},True)
            service=Mock();service.get_policy.return_value={'fixture':'native_authenticated'}
            protocol=Protocol(service,lambda *_:trust,lambda:timestamp(fixture.TS))
            context=server_context(server_cert,server_key,ca_path)
            # Port zero is not an accepted configured endpoint. Reserve an ephemeral
            # loopback port only for this isolated native test, then pass its exact value.
            import socket
            with socket.socket() as reservation:reservation.bind(('127.0.0.1',0));port=reservation.getsockname()[1]
            server=create_server('127.0.0.1',port,context,protocol,enabled=True,allowed_ha_address='127.0.0.1')
            server.timeout=2
            def request(with_certificate):
                transport=ssl.create_default_context(cafile=ca_path)
                if with_certificate:transport.load_cert_chain(client_cert,client_key)
                payload={'asset_id':fixture.ID};path='/pe7/v1/policy/get'
                assertion=dict(issuer=issuer,key_id='synthetic',actor_id='actor',context_id='context',request_id=uuid.uuid4().hex,
                    audience='hioc.pe7.asset',method='POST',path=path,issued_at=fixture.TS,expires_at=fixture.at(30),payload_sha256=digest(payload))
                worker=threading.Thread(target=server.handle_request);worker.start()
                connection=http.client.HTTPSConnection('127.0.0.1',port,context=transport,timeout=3)
                try:
                    connection.request('POST',path,canonical(sign(assertion,payload,secret)),{'Content-Type':'application/json'})
                    answer=connection.getresponse();return answer.status,json.loads(answer.read())
                finally:connection.close();worker.join(4);self.assertFalse(worker.is_alive())
            try:
                with self.assertRaises((ssl.SSLError,ConnectionError,OSError)):request(False)
                self.assertEqual(request(True),(200,{'fixture':'native_authenticated'}))
                trust.actors.clear()
                self.assertEqual(request(True)[0],403)
                self.assertEqual(service.get_policy.call_count,1)
            finally:server.server_close()
