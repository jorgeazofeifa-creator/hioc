"""Narrow private mTLS Asset adapter. Constructing configuration never binds a socket."""
from __future__ import annotations
from http.server import BaseHTTPRequestHandler, HTTPServer
import ipaddress
import json
import os
import ssl
import stat
from pathlib import Path
from .availability_contract import PolicyError, error_response, require
from .availability_protocol import peer_public_key_sha256


def private_file(path, *, secret=False):
    path = Path(path)
    require(path.is_absolute(), 'TRUST_INVALID')
    info = path.lstat()
    require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, 'TRUST_INVALID')
    if os.name == 'posix':
        require(info.st_uid == os.getuid() and stat.S_IMODE(info.st_mode) == 0o600, 'TRUST_INVALID')
        parent = path.parent.lstat()
        require(stat.S_ISDIR(parent.st_mode) and parent.st_uid == os.getuid() and
                stat.S_IMODE(parent.st_mode) == 0o700, 'TRUST_INVALID')
    # Explicitly reject symlink ancestors, including keys inside redirected roots.
    for parent in path.parents:
        require(not parent.is_symlink(), 'TRUST_INVALID')
    return str(path)


def server_context(certificate, key, client_ca):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations(cafile=private_file(client_ca))
    context.load_cert_chain(private_file(certificate), private_file(key, secret=True))
    return context


def handler(protocol, observation_protocol=None):
    class PolicyHandler(BaseHTTPRequestHandler):
        protocol_version = 'HTTP/1.1'
        # No request URLs, user identifiers or exception text in the HTTP log.
        def log_message(self, *_):
            pass

        def setup(self):
            super().setup()
            self.connection.settimeout(5)

        def do_POST(self):
            try:
                require(isinstance(self.connection, ssl.SSLSocket), 'TRUST_INVALID')
                require(self.connection.context.verify_mode == ssl.CERT_REQUIRED, 'TRUST_INVALID')
                certificate = self.connection.getpeercert(binary_form=True)
                require(bool(certificate), 'TRUST_INVALID')
                lengths = self.headers.get_all('Content-Length', [])
                require(len(lengths) == 1 and lengths[0].isascii() and lengths[0].isdecimal())
                length = int(lengths[0])
                limit = 262144 if self.path == '/pe7/v1/observations' else 8192
                require(0 < length <= limit and not self.headers.get('Transfer-Encoding'))
                require(not self.headers.get('Expect'))
                raw = self.rfile.read(length)
                require(len(raw) == length)
                selected = observation_protocol if self.path == '/pe7/v1/observations' else protocol
                require(selected is not None, 'FORBIDDEN')
                result = selected.handle(self.path, raw, peer_public_key_sha256(certificate),
                    content_type=self.headers.get('Content-Type'),
                    content_encoding=self.headers.get('Content-Encoding'), origin=self.headers.get('Origin'))
            except PolicyError as error:
                result = error_response(error)
            except Exception:
                result = error_response(PolicyError('TRUST_INVALID'))
            code = result.get('error_code')
            status = {'AUTH_REQUIRED': 401, 'FORBIDDEN': 403, 'TRUST_INVALID': 403,
                      'ASSERTION_EXPIRED': 401, 'REPLAY_CONFLICT': 409, 'REVISION_CONFLICT': 409,
                      'IDENTITY_UNSAFE': 422, 'VALIDATION_FAILED': 422, 'RATE_LIMITED': 429,
                      'BUSY': 503, 'STORE_UNAVAILABLE': 503, 'COMMIT_UNKNOWN': 503,
                      'UNSUPPORTED_SCHEMA': 503}.get(code, 201 if result.get('result') == 'created' else 200)
            if self.path == '/pe7/v1/availability/status':
                if result.get('result') == 'error':
                    result = dict(schema_version='1.0', result='error', error_code=code, retryable=False)
                status = {'AUTH_REQUIRED':401, 'FORBIDDEN':403, 'TRUST_INVALID':403,
                    'ASSERTION_EXPIRED':403, 'REPLAY_CONFLICT':403, 'VALIDATION_FAILED':422,
                    'UNSUPPORTED_SCHEMA':422, 'RATE_LIMITED':429, 'BUSY':503, 'STORE_UNAVAILABLE':503}.get(code,200)
            raw = json.dumps(result, separators=(',', ':'), allow_nan=False).encode('utf-8')
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(raw)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Connection', 'close')
            self.end_headers()
            self.wfile.write(raw)
            self.close_connection = True
    return PolicyHandler


def create_server(address, port, context, protocol, *, enabled=False, allowed_ha_address=None, observation_protocol=None):
    require(enabled is True, 'FORBIDDEN')
    parsed = ipaddress.ip_address(address)
    require(parsed.version == 4 and parsed.is_private and not parsed.is_unspecified and
            not parsed.is_multicast, 'TRUST_INVALID')
    require(type(port) is int and 1 <= port <= 65535, 'TRUST_INVALID')
    peer = ipaddress.ip_address(allowed_ha_address)
    require(peer.version == 4 and peer.is_private and not peer.is_unspecified, 'TRUST_INVALID')
    require(context.verify_mode == ssl.CERT_REQUIRED and
            context.minimum_version >= ssl.TLSVersion.TLSv1_2, 'TRUST_INVALID')
    class PrivateServer(HTTPServer):
        def verify_request(self, request, client_address):
            return client_address[0] == str(peer)
    server = PrivateServer((address, port), handler(protocol, observation_protocol), bind_and_activate=False)
    try:
        server.socket = context.wrap_socket(server.socket, server_side=True)
        server.server_bind()
        server.server_activate()
    except BaseException:
        server.server_close()
        raise
    return server
