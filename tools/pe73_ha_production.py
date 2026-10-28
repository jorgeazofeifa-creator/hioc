"""PE-7.3 native trust/guard bindings; never imports or enables HA/HIOC roles.

The foreground guard is a finite mutually authenticated observation channel, not
the product adapter, a remote shell or a persistent service. It has no mutation
commands. Actual endpoints, certificates, independently owned ACL and whole-process
exclusion responsibility must be supplied locally; none is inferred from receipts.
Product actor assertions and the immutable runtime payload are not changed.
"""
from __future__ import annotations

import contextlib
import copy
import datetime as dt
import errno
import hashlib
import hmac
import http.client
import importlib.util
import ipaddress
import json
import os
from pathlib import Path, PurePosixPath
import re
import secrets
import socket
import ssl
import stat
import struct
import sys
import time
from urllib.parse import unquote, urlsplit


def sibling(name):
    spec = importlib.util.spec_from_file_location('pe73_binding_' + name,
        Path(__file__).with_name(name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


d = sibling('pe73_ha_delivery')
LIVE = sibling('pe73_ha_live_qualify')
require, Stop, canonical, digest = d.require, d.Stop, d.canonical, d.digest
MAX = 1048576
RISKS = 'MANUAL_CALLERS_PROCEDURALLY_PROHIBITED_NOT_UNIVERSALLY_ENFORCED'
ACCEPTED_DASHBOARD = '7502a36014253a6cce6b5bcd82277c3c59242d33a191161500d5b3f8c6660ab8'
VIEW_PATHS = ['hioc-v2-' + name for name in ('executive','operations','diagnostics','inventory','network','servers')]


def identity(info):
    return (info.st_dev, info.st_ino, info.st_uid, info.st_gid,
        info.st_mode, info.st_nlink, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


class PrivateFiles:
    """Anchored private-file access; no path-based secret reopen by TLS.

    Owners are observed role identities, never PI3's policy inherited on PI5.
    The explicit private parent is 0700; every ancestor is no-follow, no ACL,
    non-writable by group/other and owned by root or the actual role owner.
    """
    def __init__(self, parent, owner, *, _ops=os):
        self.ops, self.parent, self.owner = _ops, parent, owner
        require(_ops.name == 'posix' and type(owner) is tuple and len(owner) == 2
            and all(type(x) is int and x >= 0 for x in owner), 'PRIVATE_NATIVE_IDENTITY_REQUIRED')
        require(type(parent) is str and str(PurePosixPath(parent)) == parent
            and parent.startswith('/') and parent != '/' and '..' not in PurePosixPath(parent).parts,
            'PRIVATE_PARENT_INVALID')

    def acl(self, fd):
        for key in ('system.posix_acl_access', 'system.posix_acl_default'):
            try: self.ops.getxattr(fd, key)
            except OSError as error: require(error.errno == errno.ENODATA, 'PRIVATE_ACL_UNKNOWN')
            else: raise Stop('PRIVATE_ACL_PRESENT')

    @contextlib.contextmanager
    def directory(self):
        o = self.ops
        fd = o.open('/', o.O_RDONLY | o.O_DIRECTORY | o.O_NOFOLLOW | o.O_CLOEXEC)
        held, links = [fd], []
        try:
            for index, part in enumerate([None, *PurePosixPath(self.parent).parts[1:]]):
                if part is not None:
                    parent = fd
                    fd = o.open(part, o.O_RDONLY | o.O_DIRECTORY | o.O_NOFOLLOW | o.O_CLOEXEC, dir_fd=parent)
                    held.append(fd); links.append((parent, part, fd))
                info = o.fstat(fd)
                require(stat.S_ISDIR(info.st_mode) and info.st_uid in (0, self.owner[0])
                    and not stat.S_IMODE(info.st_mode) & 0o7022, 'PRIVATE_ANCESTOR_UNSAFE')
                self.acl(fd)
            info = o.fstat(fd)
            require((info.st_uid, info.st_gid) == self.owner
                and stat.S_IMODE(info.st_mode) == 0o700, 'PRIVATE_PARENT_SECURITY')
            anchors = [(x, d._anchor(o.fstat(x))) for x in held]
            yield fd
            for parent, name, child in links:
                require(d._anchor(o.stat(name, dir_fd=parent, follow_symlinks=False))
                    == d._anchor(o.fstat(child)), 'PRIVATE_ANCESTOR_DRIFT')
            for descriptor, anchor in anchors:
                require(d._anchor(o.fstat(descriptor)) == anchor, 'PRIVATE_ANCESTOR_DRIFT')
                self.acl(descriptor)
        finally:
            primary = sys.exc_info()[1]; failed = False
            for descriptor in reversed(held):
                try: o.close(descriptor)
                except OSError: failed = True
            if failed and primary is None: raise Stop('PRIVATE_DESCRIPTOR_CLOSE_UNCERTAIN')

    def name(self, path):
        require(type(path) is str and str(PurePosixPath(path).parent) == self.parent
            and str(PurePosixPath(path)) == path and PurePosixPath(path).name not in ('.', '..'),
            'PRIVATE_PATH_OUTSIDE_APPROVED_PARENT')
        return PurePosixPath(path).name

    @contextlib.contextmanager
    def opened(self, path):
        name = self.name(path); o = self.ops
        with self.directory() as parent:
            fd = o.open(name, o.O_RDONLY | o.O_NOFOLLOW | o.O_NONBLOCK | o.O_CLOEXEC, dir_fd=parent)
            try:
                info = o.fstat(fd)
                require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and
                    (info.st_uid, info.st_gid) == self.owner and stat.S_IMODE(info.st_mode) == 0o600
                    and 0 < info.st_size <= MAX, 'PRIVATE_FILE_SECURITY')
                self.acl(fd); before = identity(info)
                raw = bytearray()
                while len(raw) <= MAX:
                    chunk = o.read(fd, min(65536, MAX + 1 - len(raw)))
                    if not chunk: break
                    raw.extend(chunk)
                require(0 < len(raw) <= MAX, 'PRIVATE_READ_LIMIT')
                require(identity(o.fstat(fd)) == identity(o.stat(name, dir_fd=parent,
                    follow_symlinks=False)) == before, 'PRIVATE_FILE_DRIFT')
                yield bytes(raw), fd, before
                require(identity(o.fstat(fd)) == identity(o.stat(name, dir_fd=parent,
                    follow_symlinks=False)) == before, 'PRIVATE_FILE_DRIFT')
                self.acl(fd)
            finally: o.close(fd)

    def read(self, path):
        with self.opened(path) as (raw, _, _): return raw

    def provision(self, destination, raw):
        """Explicit operator call only: one new private file, never overwrite/retry.

        Caller supplies already-issued material. No key generation, active config,
        permission repair or secret output. An uncertain file is retained.
        """
        require(type(raw) is bytes and 0 < len(raw) <= MAX, 'PROVISION_SIZE')
        o = self.ops
        with self.directory() as parent:
            fd = o.open(self.name(destination), o.O_WRONLY | o.O_CREAT | o.O_EXCL |
                o.O_NOFOLLOW | o.O_CLOEXEC, 0o600, dir_fd=parent)
            try:
                info = o.fstat(fd)
                require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and
                    (info.st_uid, info.st_gid) == self.owner, 'PROVISION_OWNER')
                # Only the new exclusive descriptor, never an existing file.
                o.fchmod(fd, 0o600); self.acl(fd)
                offset = 0
                while offset < len(raw):
                    written = o.write(fd, raw[offset:]); require(written > 0, 'PROVISION_SHORT_WRITE')
                    offset += written
                o.fsync(fd)
            finally: o.close(fd)
            o.fsync(parent)
        require(self.read(destination) == raw, 'PROVISION_READBACK')


def certificates(raw):
    from cryptography import x509
    require(type(raw) is bytes and 0 < len(raw) <= MAX, 'CERTIFICATE_SIZE')
    values = x509.load_pem_x509_certificates(raw)
    require(1 <= len(values) <= 8, 'CERTIFICATE_CHAIN_LIMIT')
    return values


def spki(cert):
    from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
    return hashlib.sha256(cert.public_key().public_bytes(Encoding.DER,
        PublicFormat.SubjectPublicKeyInfo)).hexdigest()


def validate_material(certificate, key, ca, role, address, now=None):
    """Local pair/time/EKU and CA constraints; TLS validates the peer's chain.

    No handwritten replacement for OpenSSL path validation. A completed mutual
    TLS connection is required before trust_preflight can report success.
    """
    from cryptography import x509
    from cryptography.hazmat.primitives.serialization import load_pem_private_key, Encoding, PublicFormat
    from cryptography.x509.oid import ExtendedKeyUsageOID
    now = dt.datetime.now(dt.timezone.utc) if now is None else now
    chain, authorities = certificates(certificate), certificates(ca)
    for cert in [*chain, *authorities]:
        require(cert.not_valid_before_utc <= now < cert.not_valid_after_utc, 'CERTIFICATE_EXPIRED_OR_NOT_YET_VALID')
    leaf = chain[0]
    private = load_pem_private_key(key, password=None)
    require(private.public_key().public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo) ==
        leaf.public_key().public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo), 'CERTIFICATE_KEY_MISMATCH')
    usage = leaf.extensions.get_extension_for_class(x509.ExtendedKeyUsage).value
    require((ExtendedKeyUsageOID.CLIENT_AUTH if role == 'ha' else ExtendedKeyUsageOID.SERVER_AUTH)
        in usage, 'CERTIFICATE_ROLE_MISMATCH')
    require(not leaf.extensions.get_extension_for_class(x509.BasicConstraints).value.ca, 'LEAF_IS_CA')
    for issuer in authorities:
        require(issuer.extensions.get_extension_for_class(x509.BasicConstraints).value.ca
            and issuer.extensions.get_extension_for_class(x509.KeyUsage).value.key_cert_sign,
            'CA_CONSTRAINTS_INVALID')
    for child, issuer in zip(chain, chain[1:]): child.verify_directly_issued_by(issuer)
    if role == 'backend':
        names = leaf.extensions.get_extension_for_class(x509.SubjectAlternativeName).value
        require(ipaddress.ip_address(address) in names.get_values_for_type(x509.IPAddress), 'SERVER_IDENTITY_MISMATCH')
    return spki(leaf)


class TrustSide:
    """Reads only independently owned local trust; all output is sanitized.

    HA paths use /config in the runtime contract. Map to the live verified Terminal
    root only after NativeProbe proves their shared filesystem identity.
    """
    def __init__(self, role, files, read_packet, *, core_root=None):
        require(role in ('ha', 'backend'), 'TRUST_ROLE_INVALID')
        self.role, self.files, self.read_packet, self.core_root = role, files, read_packet, core_root
        self.first = None

    def path(self, name):
        if self.role == 'ha':
            require(self.core_root in ('/homeassistant', '/config') and name.startswith('/config/'), 'CORE_PRIVATE_MAPPING_REQUIRED')
            return self.core_root + name[len('/config'):]
        return name

    @contextlib.contextmanager
    def material(self):
        packet = self.read_packet()
        checked = d.disabled_trust(packet['ha']['hioc_operator']['operator'], packet['backend'])
        require(packet == checked, 'PRIVATE_PACKET_SHAPE')
        config = packet['ha']['hioc_operator']['operator'] if self.role == 'ha' else packet['backend']
        entry = packet['backend']['issuer_trusts'][0]
        names = ('client_certificate', 'client_key', 'server_ca') if self.role == 'ha' else ('server_certificate', 'server_key', 'client_ca')
        key_path = config['assertion_key_file'] if self.role == 'ha' else entry['assertion_key_file']
        with contextlib.ExitStack() as stack:
            objects = [stack.enter_context(self.files.opened(self.path(config[k]))) for k in names]
            assertion, _, key_identity = stack.enter_context(self.files.opened(self.path(key_path)))
            require(len(assertion) == 32, 'HMAC_KEY_MUST_BE_32_BYTES')
            pin = validate_material(*(x[0] for x in objects), self.role, packet['backend']['bind_address'])
            if self.role == 'ha': require(pin == entry['client_spki_sha256'], 'CLIENT_SPKI_MISMATCH')
            # Never return this identity publicly: it includes private file/ACL bindings.
            binding = digest({'packet': packet, 'files':[(d.sha(x[0]), x[2]) for x in objects],
                'assertion':(d.sha(assertion), key_identity)})
            if self.first is None: self.first = binding
            require(binding == self.first, 'TRUST_MATERIAL_DRIFT')
            yield packet, objects, assertion

    @contextlib.contextmanager
    def context(self):
        with self.material() as (packet, objects, assertion):
            purpose = ssl.Purpose.SERVER_AUTH if self.role == 'ha' else ssl.Purpose.CLIENT_AUTH
            context = ssl.create_default_context(purpose, cadata=objects[2][0].decode('ascii'))
            context.minimum_version = ssl.TLSVersion.TLSv1_2
            context.verify_mode = ssl.CERT_REQUIRED
            if self.role == 'ha': require(context.check_hostname, 'TLS_HOSTNAME_REQUIRED')
            # /proc/self/fd reopens the still-held validated inode, not an unsafe
            # secret pathname. The reader rechecks named and descriptor identities.
            context.load_cert_chain('/proc/self/fd/' + str(objects[0][1]),
                '/proc/self/fd/' + str(objects[1][1]))
            yield context, packet, assertion


def send(channel, value):
    raw = canonical(value)
    require(len(raw) <= 32768, 'GUARD_MESSAGE_LIMIT')
    channel.sendall(struct.pack('!I', len(raw)) + raw)


def receive(channel):
    def exact(count):
        raw = bytearray()
        while len(raw) < count:
            part = channel.recv(count - len(raw)); require(bool(part), 'GUARD_CONNECTION_LOST')
            raw.extend(part)
        return bytes(raw)
    size = struct.unpack('!I', exact(4))[0]
    require(0 < size <= 32768, 'GUARD_MESSAGE_LIMIT')
    raw = exact(size); value = json.loads(raw)
    require(canonical(value) == raw and type(value) is dict, 'GUARD_MESSAGE_INVALID')
    return value


def key_proof(key, request, reply):
    # Guard-only key-possession challenge, not an actor assertion, editing
    # request or substitute for the unchanged product assertion protocol.
    return hmac.new(key, b'PE73_DELIVERY_GUARD_KEY_POSSESSION\0' + canonical([request, reply]), hashlib.sha256).hexdigest()


def peer_identity(channel, packet, role):
    require(channel.version() in ('TLSv1.2', 'TLSv1.3') and channel.getpeercert(), 'MUTUAL_TLS_NOT_ESTABLISHED')
    address = packet['backend']['ha_address' if role == 'backend' else 'bind_address']
    require(channel.getpeername()[0] == address, 'GUARD_PEER_ADDRESS_MISMATCH')
    if role == 'backend':
        from cryptography import x509
        require(spki(x509.load_der_x509_certificate(channel.getpeercert(binary_form=True))) ==
            packet['backend']['issuer_trusts'][0]['client_spki_sha256'], 'CLIENT_SPKI_MISMATCH')


class GuardServer:
    """One foreground session, <=900s, <=128 read checks; no listener/autostart.

    Operator supplies an explicitly approved connected mTLS socket. No request
    names a file, command, process, role change or recovery action. No retries.
    The independent backend packet/ACL and local state are reread on EVERY check.
    """
    def __init__(self, trust, observe, reference, *, clock=time.monotonic):
        require(type(reference) is str and re.fullmatch('[A-Za-z0-9_-]{8,96}',reference), 'GUARD_PROCESS_REFERENCE_REQUIRED')
        self.trust, self.observe, self.clock = trust, observe, clock
        self.reference = reference
        self.used = False

    def handle(self, channel):
        require(not self.used, 'GUARD_SESSION_REUSE'); self.used = True
        start = self.clock(); baseline = None; session = None
        channel.settimeout(15)
        for count in range(1, 129):
            require(self.clock() < start + 900, 'GUARD_EXPIRED')
            request = receive(channel)
            require(set(request) == {'operation', 'reference', 'session', 'counter', 'nonce', 'packet_sha256'}
                and request['operation'] == 'CHECK' and request['counter'] == count
                and request['reference'] == self.reference
                and type(request['session']) is str and re.fullmatch('[0-9a-f]{64}', request['session'])
                and type(request['nonce']) is str and re.fullmatch('[0-9a-f]{64}', request['nonce']), 'GUARD_REQUEST_INVALID')
            if session is None: session = request['session']
            require(session == request['session'], 'GUARD_SESSION_DRIFT')
            with self.trust.material() as (packet, _, key):
                peer_identity(channel, packet, 'backend')
                require(request['packet_sha256'] == digest(packet), 'INDEPENDENT_BACKEND_ACL_OR_PACKET_MISMATCH')
                observed = self.observe()
                if baseline is None: baseline = observed
                require(observed == baseline, 'BACKEND_LIVE_DRIFT')
                reply = {'session':session, 'counter':count, 'nonce':request['nonce'],
                    'state_sha256':digest(observed), 'independent_trust_sha256':self.trust.first}
                send(channel, reply | {'key_proof':key_proof(key, request, reply)})
        raise Stop('GUARD_CHECK_LIMIT')


class Peer:
    """Live authenticated stream only; no JSON-receipt admission interface."""
    def __init__(self, channel, trust, reference, *, clock=time.monotonic):
        require(type(reference) is str and re.fullmatch('[A-Za-z0-9_-]{8,96}',reference), 'GUARD_PROCESS_REFERENCE_REQUIRED')
        self.channel, self.trust, self.clock = channel, trust, clock
        self.reference = reference
        self.session, self.count, self.start = secrets.token_hex(32), 0, clock()
        self.baseline = None; self.stopped = False

    def check(self, packet):
        require(not self.stopped and self.clock() < self.start + 900 and self.count < 128, 'GUARD_EXPIRED_OR_STOPPED')
        try:
            with self.trust.material() as (local, _, key):
                require(local == packet, 'LOCAL_TRUST_PACKET_DRIFT')
                peer_identity(self.channel, packet, 'ha')
                self.count += 1
                request = dict(operation='CHECK', reference=self.reference, session=self.session, counter=self.count,
                    nonce=secrets.token_hex(32), packet_sha256=digest(packet))
                self.channel.settimeout(15); send(self.channel, request); result = receive(self.channel)
                require(set(result) == {'session','counter','nonce','state_sha256','independent_trust_sha256','key_proof'}, 'GUARD_RESPONSE_INVALID')
                proof = result.pop('key_proof')
                require(type(proof) is str and hmac.compare_digest(proof, key_proof(key, request, result)), 'HMAC_PAIR_MISMATCH')
                require(all(result[k] == request[k] for k in ('session','counter','nonce')), 'GUARD_REPLAY_OR_CONTEXT_MISMATCH')
                stable = (result['state_sha256'], result['independent_trust_sha256'])
                require(all(type(x) is str and re.fullmatch('[0-9a-f]{64}', x) for x in stable), 'GUARD_RESPONSE_INVALID')
                if self.baseline is None: self.baseline = stable
                require(stable == self.baseline, 'BACKEND_LIVE_DRIFT')
                return self.session
        except BaseException:
            self.stopped = True
            raise


class RouteProbe:
    """Only the explicitly approved HA HTTPS origin, no redirects/auth export."""
    def __init__(self, origin, expected_address, *, ca_file=None, _connection=http.client.HTTPSConnection):
        url = urlsplit(origin)
        require(url.scheme == 'https' and url.hostname and not url.username and not url.password
            and url.path in ('','/') and not url.query and not url.fragment, 'HA_HTTP_ORIGIN_REQUIRED')
        self.host, self.port = url.hostname, url.port or 443
        address = ipaddress.ip_address(expected_address)
        require(address.version == 4 and address.is_private and not address.is_loopback
            and not address.is_unspecified and not address.is_multicast, 'APPROVED_PI5_FRONTEND_ADDRESS_REQUIRED')
        self.expected_address = expected_address
        self.context = ssl.create_default_context(cafile=ca_file)
        self.context.minimum_version = ssl.TLSVersion.TLSv1_2
        self.connection = _connection

    def __call__(self, url, expected):
        require(url == '/local/hioc-asset-editor.js' and re.fullmatch('[0-9a-f]{64}', expected), 'EDITOR_ROUTE_SCOPE')
        require(self.context.check_hostname and self.context.verify_mode == ssl.CERT_REQUIRED
            and self.context.minimum_version >= ssl.TLSVersion.TLSv1_2, 'EDITOR_TLS_POLICY_DRIFT')
        connection = self.connection(self.host, self.port, context=self.context, timeout=15)
        try:
            connection.connect()
            require(connection.sock.getpeername()[0] == self.expected_address, 'HA_FRONTEND_PEER_ADDRESS_MISMATCH')
            connection.request('GET', url, headers={'Accept-Encoding':'identity', 'Cache-Control':'no-cache'})
            response = connection.getresponse()
            require(response.status == 200 and response.getheader('Content-Encoding') in (None, 'identity')
                and response.getheader('Location') is None, 'EDITOR_HTTP_RESPONSE_INVALID')
            raw = response.read(MAX + 1)
            require(len(raw) <= MAX and d.sha(raw) == expected, 'EDITOR_HTTP_BYTES_MISMATCH')
            return {'url':url,'sha256':expected,'status':200,'identity_encoding':True}
        finally: connection.close()


class Bindings:
    """Adapters for the existing Delivery transaction, never a second publisher.

    ``observe_local`` is NativeHAState, ``peer`` is the live mTLS Peer; callback
    tests are synthetic only. All production constructors require native readers.
    The session identity is opaque and stable while every call rechecks fresh state.
    """
    def __init__(self, fs, api, trust, peer, observe_local):
        self.fs, self.api, self.trust, self.peer, self.observe_local = fs, api, trust, peer, observe_local
        self.baseline = None

    def trust_preflight(self, packet):
        identity = self.peer.check(packet)
        return dict(identity=identity, ha_private_files=True, backend_private_files=True,
            certificate_pair=True, assertion_pair=True, spki_pin=True, independent_acl=True)

    def guard(self):
        with self.trust.material() as (packet, _, _): session = self.peer.check(packet)
        local = self.observe_local()
        if type(self.observe_local) is NativeHAState:
            reference = self.observe_local.record['reference']
            require(reference == self.peer.reference and
                (self.fs._reference == reference or self.fs._reference is None and self.fs._existing),
                'WHOLE_PROCESS_CONTEXT_MISMATCH')
        require(type(local) is dict and set(local) == {'host_identity','capability_identity'}, 'LOCAL_NATIVE_GUARD_SHAPE')
        if self.baseline is None: self.baseline = local
        require(local == self.baseline, 'HA_LIVE_DRIFT')
        require('hioc_operator' not in self.api.call({'type':'get_services'}), 'HA_SERVICES_ALREADY_ACTIVE')
        config = self.api.call({'type':'get_config'})
        require(type(config) is dict and type(config.get('components')) is list
            and not any(x == 'hioc_operator' or x.startswith('hioc_operator.') for x in config['components']), 'HA_INTEGRATION_ALREADY_LOADED')
        require(self.api.call({'type':'lovelace/info'}).get('resource_mode') == 'storage', 'RESOURCE_MODE_UNSUPPORTED')
        resources = self.api.call({'type':'lovelace/resources/list'})
        require(type(resources) is list and all(type(x) is dict for x in resources), 'LIVE_RESOURCE_BASELINE_UNAVAILABLE')
        # Actual API baselines are separately compared by Delivery._fresh before
        # every publication; nonce/counters are intentionally not stable identity.
        # Fresh proof is checked on every call, but its nonce/session is NOT a
        # filesystem identity. Keep the persisted host identity stable so an
        # explicitly authorized new-session recovery can prove the same host.
        # Installation still binds the live session in trust_preflight and cannot
        # silently resume; the existing recovery gates remain unchanged.
        return dict(host_identity=local['host_identity'], disabled=True,
            exclusive_delivery=True, resources_loaded=True, local_mapping=True,
            storage_dashboard=True, capability_identity=local['capability_identity'])


class NativeHAState:
    """Fresh proven Core/root/mapping plus independent private delivery lease.

    Lease is a freshly created, durable private record held by the operator's
    whole-process session. It is NEVER deleted/released automatically, including
    on failure or timeout. Concurrent operators must use this fixed lease path.
    Manual callers remain procedurally prohibited, not universally excluded.
    """
    def __init__(self, fs, files, lease_path, reference, expected_host_identity, approved_capabilities, *, risk_acknowledgement):
        require(re.fullmatch('[A-Za-z0-9_-]{8,96}', reference), 'WHOLE_PROCESS_AUTHORIZATION_REQUIRED')
        require(risk_acknowledgement == RISKS, 'MANUAL_EXCLUSION_RESPONSIBILITY_REQUIRED')
        require(re.fullmatch('[0-9a-f]{64}', expected_host_identity) and type(approved_capabilities) is dict
            and bool(approved_capabilities) and all(type(k) is str and re.fullmatch('[0-9a-f]{64}',v)
                for k,v in approved_capabilities.items()), 'APPROVED_HOST_AND_SOURCE_IDENTITIES_REQUIRED')
        self.fs, self.files, self.lease_path = fs, files, lease_path
        require(lease_path == files.parent + '/pe73-delivery-lease.json', 'FIXED_EXCLUSION_LEASE_REQUIRED')
        self.expected_host_identity, self.approved_capabilities = expected_host_identity, approved_capabilities
        self.record = {'reference':reference, 'session':secrets.token_hex(32),
            'risks':RISKS, 'boot':Path('/proc/sys/kernel/random/boot_id').read_text().strip()}
        self.started = time.monotonic(); self.created = False

    def acquire(self):
        require(not self.created, 'LEASE_NO_RETRY')
        self.created = True  # Any uncertain mutation consumes this attempt.
        self.files.provision(self.lease_path, canonical(self.record))

    def __call__(self):
        require(self.created and time.monotonic() < self.started + 900, 'DELIVERY_LEASE_REQUIRED_OR_EXPIRED')
        require(self.files.read(self.lease_path) == canonical(self.record), 'DELIVERY_LEASE_DRIFT')
        require(Path('/proc/sys/kernel/random/boot_id').read_text().strip() == self.record['boot'], 'HA_BOOT_DRIFT')
        self.fs._live()  # Actual Core process, root, inode/device, owner/mode, ACLs.
        proof = self.fs._proof
        capabilities = self.fs._probe.public_capabilities(proof['core_container'])
        frontend = capabilities.get('components/frontend/__init__.py', {})
        # Source identity must be the operator's approved installed implementation;
        # NativeProbe has already established www/Core-root object identity.
        require(type(frontend.get('sha256')) is str and re.fullmatch('[0-9a-f]{64}', frontend['sha256']), 'WWW_LOCAL_IMPLEMENTATION_UNOBSERVABLE')
        require('components/frontend/__init__.py' in self.approved_capabilities and all(
            capabilities.get(k,{}).get('sha256') == v for k,v in self.approved_capabilities.items()), 'APPROVED_MAPPING_IMPLEMENTATION_DRIFT')
        host = digest({k:proof[k] for k in ('boot_id','terminal','core_container','core','root')})
        require(host == self.expected_host_identity, 'APPROVED_PI5_HOST_OR_CORE_DRIFT')
        return {'host_identity':host,
            'capability_identity':digest(capabilities)}


class NativeBackendState:
    """Read-only PI3 state, immutable payload and scheduler/disabled guards.

    Existing NativeOps supplies the accepted process parser and target identity;
    it is not replaced by PID counting or a claim of universal caller exclusion.
    No scheduler lock, cron change, consumer stop or artifact write is performed.
    """
    def __init__(self, files, lease_path, reference, expected_scheduler, *, risk_acknowledgement):
        self.files, self.lease_path = files, lease_path
        require(lease_path == files.parent + '/pe73-delivery-lease.json', 'FIXED_EXCLUSION_LEASE_REQUIRED')
        require(risk_acknowledgement == RISKS and re.fullmatch('[A-Za-z0-9_-]{8,96}',reference)
            and re.fullmatch('[0-9a-f]{64}', expected_scheduler), 'BACKEND_EXCLUSION_RESPONSIBILITY_REQUIRED')
        self.scheduler = expected_scheduler
        self.provider = sibling('pe73_maintenance_window')
        self.ops = self.provider.NativeOps()
        self.record = {'reference':reference,'session':secrets.token_hex(32),'risks':RISKS,'boot':self.ops.boot_id}
        self.started = time.monotonic(); self.created = False

    def acquire(self):
        require(not self.created, 'LEASE_NO_RETRY')
        self.created = True
        self.files.provision(self.lease_path, canonical(self.record))

    def __call__(self):
        boot = self.ops.target_boot()
        require(self.created and boot == self.record['boot'] and time.monotonic() < self.started + 900,
            'BACKEND_BOOT_OR_LEASE_EXPIRED')
        require(self.files.read(self.lease_path) == canonical(self.record), 'BACKEND_DELIVERY_LEASE_DRIFT')
        scheduler = self.ops.scheduler()
        require(d.sha(scheduler) == self.scheduler, 'BACKEND_SCHEDULER_DRIFT')
        require(not re.search(rb'--pe7-(?:cycle|initialize)|hioc-availability-adapter|availability_server', scheduler), 'PE7_SCHEDULER_ENABLED')
        process = self.ops.processes()
        require(process['inspection_complete'] is True and not process['known_active'], 'BACKEND_CONSUMERS_NOT_DRAINED')
        controller = sibling('hioc-pe73-pi3-delivery')
        runtime = controller.NativeFS()
        payload = []
        for entry in controller.MANIFEST:
            observed = runtime.snapshot(entry['path'], 0o755 if entry['path'].startswith('pi4/bin/') else 0o644)
            require(observed['exists'] and observed['sha256'] == entry['sha256'], 'PI3_PAYLOAD_DRIFT')
            payload.append(observed)
        # Runtime engine's exact fixed JSON config is optional only when absent.
        policy = runtime.snapshot('config/pe7_availability.json', 0o600)
        if policy['exists']:
            source = runtime.read('config/pe7_availability.json')
            value = json.loads(source)
            require(type(value) is dict and value.get('enabled') is False
                and value.get('notifications_enabled') is False, 'PE7_RUNTIME_ENABLED_OR_UNKNOWN')
        return {'boot':boot, 'scheduler_sha256':self.scheduler,
            'lease':digest(self.record), 'payload':digest(payload), 'policy':policy, 'disabled':True,
            'exclusion':RISKS}


class DeliveryAPI:
    """Reuse the qualified Supervisor transport; only two journal-bound writes.

    This does not widen the read-only qualifier's command allowlist. The separate
    delivery adapter admits each write once, only after exact durable intent in
    the existing transaction. No service calls, reload, restart or .storage API.
    """
    def __init__(self, proxy, fs):
        self.proxy, self.fs = proxy, fs
        self.qualifier = LIVE
        self.sent = set(); self.stopped = False
        self.dashboard_observed = False; self.resources_observed = False
        proxy.deadline = time.monotonic() + 900

    def _request(self, kind, fields):
        require(not self.stopped and self.proxy.authenticated and self.proxy.counter < 512
            and time.monotonic() < self.proxy.deadline, 'DELIVERY_API_CLOSED_OR_EXPIRED')
        self.proxy.counter += 1
        self.proxy.calls.append(kind)
        self.proxy._frame(1, canonical({'id':self.proxy.counter,'type':kind,**fields}))
        result = self.proxy._receive()
        require(type(result) is dict and result.get('type') == 'result'
            and result.get('id') == self.proxy.counter and result.get('success') is True, 'DELIVERY_API_RESPONSE_UNCERTAIN')
        return result.get('result')

    def call(self, value):
        require(type(value) is dict and type(value.get('type')) is str, 'DELIVERY_API_SHAPE')
        kind = value['type']; fields = {k:v for k,v in value.items() if k != 'type'}
        if kind in d.READS:
            if kind == 'lovelace/config': require(fields == {'url_path':d.DASHBOARD}, 'EXCLUSIVE_HIOC_DASHBOARD_REQUIRED')
            else: require(not fields, 'DELIVERY_READ_FIELDS')
            if kind == 'lovelace/resources/list':
                # Protect against the original lazy legacy import side effect;
                # this is a fresh delivery-time check, not a new qualification run.
                q = self.qualifier
                catalog = self._request('lovelace/dashboards/list', {})
                adapter = type('ReadAdapter', (), {'call':lambda _,k,**f:self._legacy(k,f)})()
                q.resource_source(adapter, {}, catalog)
            result = self._request(kind, fields)
            if kind == 'lovelace/config' and not self.dashboard_observed:
                require(digest(result) == ACCEPTED_DASHBOARD and type(result) is dict and
                    [v.get('path') for v in result.get('views',[])] == VIEW_PATHS, 'ACCEPTED_HIOC_DASHBOARD_DRIFT')
                self.dashboard_observed = True
            if kind == 'lovelace/resources/list' and not self.resources_observed:
                require(type(result) is list and len(result) == 11, 'ACCEPTED_RESOURCE_COUNT_DRIFT')
                self.resources_observed = True
            if kind == 'lovelace/resources/list': self._resources(result)
            return result
        require(kind in d.MUTATIONS and kind not in self.sent, 'DELIVERY_MUTATION_OUTSIDE_SCOPE_OR_RETRY')
        journal = self.fs.load()
        require(journal['dashboard'] == d.DASHBOARD and journal.get('whole_process_reference')
            and journal.get('route') == {'url':'/local/hioc-asset-editor.js',
                'sha256':d.MANIFEST['homeassistant/www/hioc-asset-editor.js'][0],
                'status':200,'identity_encoding':True}, 'VERIFIED_ROUTE_AND_PROCESS_AUTHORITY_REQUIRED')
        if kind == 'lovelace/resources/create':
            require(journal['state'] == 'REGISTERING_RESOURCE' and journal['pending'] == 'resource'
                and fields == {'res_type':'module','url':'/local/hioc-asset-editor.js'}, 'RESOURCE_INTENT_MISMATCH')
        else:
            require(journal['state'] == 'REGISTERING_CARD' and journal['pending'] == 'dashboard'
                and fields == {'url_path':d.DASHBOARD,'config':journal['observation']['after']}, 'DASHBOARD_INTENT_MISMATCH')
        self.sent.add(kind)
        try: return self._request(kind, fields)
        except BaseException:
            self.stopped = True
            raise

    def _resources(self, rows):
        require(type(rows) is list and len(rows) <= 256 and all(type(row) is dict
            and type(row.get('url')) is str and 0 < len(row['url']) <= 2048
            and type(row.get('type')) is str for row in rows), 'LIVE_RESOURCE_SCHEMA_INVALID')
        own = self.fs.load().get('resource') if 'lovelace/resources/create' in self.sent else None
        for row in rows:
            path = unquote(urlsplit(row['url']).path)
            conflict = path == '/local/hioc-asset-editor.js' or path.lower().endswith('/hioc-asset-editor.js')
            require(not conflict or own is not None and row == own and
                row['url'] == '/local/hioc-asset-editor.js' and row['type'] == 'module', 'LIVE_HIOC_RESOURCE_CONFLICT')

    def _legacy(self, kind, fields):
        require(kind == 'lovelace/config' and fields == {'url_path':None}, 'LEGACY_PROBE_SCOPE')
        # CONFIG_NOT_FOUND is safe only when HA explicitly reports that code.
        self.proxy.counter += 1
        require(self.proxy.counter < 512 and time.monotonic() < self.proxy.deadline, 'DELIVERY_API_CLOSED_OR_EXPIRED')
        self.proxy.calls.append(kind)
        self.proxy._frame(1, canonical({'id':self.proxy.counter,'type':kind,**fields}))
        result = self.proxy._receive()
        require(type(result) is dict and result.get('id') == self.proxy.counter and result.get('type') == 'result', 'LEGACY_PROBE_CONTEXT')
        if result.get('success') is not True:
            q = self.qualifier
            if result.get('error',{}).get('code') == 'config_not_found': raise q.Stop('CONFIG_NOT_FOUND')
            raise Stop('LEGACY_PROBE_UNAVAILABLE')
        return result.get('result')


class NativePacket:
    """Canonical packet from the role-owned descriptor reader, not a callback."""
    def __init__(self, files, path):
        require(type(files) is PrivateFiles and files.ops is os, 'NATIVE_PACKET_READER_REQUIRED')
        self.files, self.path = files, path

    def __call__(self):
        raw = self.files.read(self.path); packet = json.loads(raw)
        require(canonical(packet) == raw, 'PRIVATE_PACKET_CANONICAL_REQUIRED')
        return packet


def native_packet(files, path):
    return NativePacket(files, path)


@contextlib.contextmanager
def authenticated_proxy():
    """Existing app credential only; no credential prompt/export or new token."""
    token = os.environ.get('SUPERVISOR_TOKEN')
    require(type(token) is str and bool(token), 'EXISTING_AUTHENTICATION_REQUIRED')
    proxy = LIVE.Proxy()
    try:
        proxy.connect(token); token = None
        yield proxy
    finally:
        token = None
        proxy.close()


@contextlib.contextmanager
def connect_peer(trust, guard_port, reference):
    """Operator-approved temporary observer port; product adapter stays disabled."""
    require(type(trust) is TrustSide and trust.role == 'ha' and type(trust.files) is PrivateFiles
        and trust.files.ops is os and type(trust.read_packet) is NativePacket
        and trust.read_packet.files is trust.files,
        'NATIVE_CLIENT_TRUST_REQUIRED')
    require(type(guard_port) is int and 1 <= guard_port <= 65535, 'APPROVED_GUARD_PORT_REQUIRED')
    with trust.context() as (context, packet, _):
        host = packet['backend']['bind_address']
        require(guard_port != packet['backend']['port'], 'GUARD_MUST_NOT_OCCUPY_PRODUCT_ENDPOINT')
        with socket.create_connection((host, guard_port), timeout=15) as raw:
            with context.wrap_socket(raw, server_hostname=host) as channel:
                peer_identity(channel, packet, 'ha')
                yield Peer(channel, trust, reference)


def serve_guard(trust, state, guard_port):
    """Exactly one foreground connection; no fork/daemon/service/retry/mutation."""
    require(type(trust) is TrustSide and trust.role == 'backend' and type(trust.files) is PrivateFiles
        and trust.files.ops is os and trust.files.owner == (1000,1000)
        and type(trust.read_packet) is NativePacket and trust.read_packet.files is trust.files
        and type(state) is NativeBackendState and state.files is trust.files,
        'NATIVE_BACKEND_TRUST_AND_STATE_REQUIRED')
    state()  # Fail before opening even the bounded observer listener.
    require(type(guard_port) is int and 1 <= guard_port <= 65535, 'APPROVED_GUARD_PORT_REQUIRED')
    with trust.context() as (context, packet, _):
        require(guard_port != packet['backend']['port'], 'GUARD_MUST_NOT_OCCUPY_PRODUCT_ENDPOINT')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
            listener.settimeout(120)
            listener.bind((packet['backend']['bind_address'], guard_port)); listener.listen(1)
            raw, address = listener.accept()
            with raw:
                raw.settimeout(15)
                require(address[0] == packet['backend']['ha_address'], 'GUARD_PEER_ADDRESS_MISMATCH')
                with context.wrap_socket(raw, server_side=True) as channel:
                    GuardServer(trust, state, state.record['reference']).handle(channel)


def native_delivery(fs, proxy, trust, peer, local_state, route, read_object):
    """Construct the existing publisher only from actual native-bound components."""
    require(type(fs) is d._ScopedHAFileSystem and type(trust) is TrustSide and trust.role == 'ha'
        and type(trust.files) is PrivateFiles and type(peer) is Peer and peer.trust is trust
        and type(local_state) is NativeHAState and local_state.fs is fs
        and fs._ops is os and trust.files.ops is os and trust.files.owner == fs._core
        and local_state.files is trust.files and trust.core_root == fs._root
        and type(trust.read_packet) is NativePacket and trust.read_packet.files is trust.files
        and type(proxy) is LIVE.Proxy and proxy.authenticated is True
        and isinstance(proxy.sock, socket.socket) and proxy.sock.getpeername()[0] == '172.30.32.2'
        and isinstance(peer.channel, ssl.SSLSocket) and peer.channel.context.check_hostname
        and peer.channel.context.verify_mode == ssl.CERT_REQUIRED
        and type(route) is RouteProbe and route.connection is http.client.HTTPSConnection,
        'NATIVE_BINDING_TYPES_REQUIRED')
    api = DeliveryAPI(proxy, fs)
    bindings = Bindings(fs, api, trust, peer, local_state)
    return d.Delivery(fs, api, bindings.guard, bindings.trust_preflight, read_object, route_probe=route)


def sanitized(call):
    try:
        call()
        return {'RESULT':'PASS_NATIVE_BINDING_CHECK','activation':False,'STOP_REQUIRED':True}
    except BaseException:
        # Native exceptions and provider exceptions can contain secret paths/data.
        return {'RESULT':'BLOCKED_NATIVE_BINDING_CHECK','failure_code':'BINDING_NOT_ESTABLISHED',
            'activation':False,'automatic_recovery':False,'STOP_REQUIRED':True}


def requirements():
    """No secret read, host discovery, network or filesystem mutation."""
    try:
        import cryptography
        crypto = bool(cryptography.__version__)
    except ImportError: crypto = False
    return {'RESULT':'REQUIRED_LOCAL_INPUTS_NOT_PRODUCTION_AUTHORIZATION',
        'cryptography_available':crypto,
        'required':['approved_private_parents_and_observed_role_owners',
            'issued_client_server_chains_and_private_keys_and_CA_roots',
            'shared_32_byte_HMAC_key_with_issuer_and_key_id',
            'independently_owned_backend_exact_actor_operation_asset_ACL_and_HA_allowlist',
            'approved_backend_address_port_HA_source_and_bounded_guard_endpoint',
            'approved_verified_HTTPS_HA_frontend_origin_and_CA',
            'whole_process_reference_and_durable_exclusive_delivery_responsibility',
            'fresh_live_mTLS_peer_and_native_host_Core_root_proof'],
        'PE73':'IN_PROGRESS','PE74':'NOT_AUTHORIZED','production_ready':False,
        'mutation_performed':False,'STOP_REQUIRED':True}


if __name__ == '__main__':
    require(sys.argv[1:] == ['--requirements'], 'ONLY_READ_ONLY_REQUIREMENTS_CLI_EXPOSED')
    print(json.dumps(requirements(), sort_keys=True, separators=(',',':')))
