"""Synthetic PE-4.0B.2b tests; no HA connection or credential acquisition."""
import asyncio
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import stat
import tempfile
import types
import unittest
from unittest.mock import patch
import warnings

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('discovery', ROOT / 'tools/hioc-pe4-ha-registry-discovery.py')
m = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(m)
PRIVATE = ['device-bedroom-secret', 'sensor.private_kitchen', 'area-private', 'entry-private',
           'AA:BB:CC:DD:EE:01', '192.168.50.10', 'my-private-host', 'token-SYNTHETIC',
           'https://private.invalid/secret', 'Private Room']


def rows():
    return [
        [{'id': PRIVATE[0], 'config_entry_id': PRIVATE[3], 'area_id': PRIVATE[2],
          'via_device_id': None, 'disabled_by': None, 'connections': [['mac', PRIVATE[4]]],
          'identifiers': [['mqtt', 'private-unique-id']], 'name': PRIVATE[9],
          'configuration_url': PRIVATE[8], 'labels': [], 'config_entries': [PRIVATE[3]],
          'config_entries_subentries': {PRIVATE[3]: [None]}}],
        [{'entity_id': PRIVATE[1], 'device_id': PRIVATE[0], 'area_id': PRIVATE[2],
          'config_entry_id': PRIVATE[3], 'disabled_by': None, 'platform': 'mqtt',
          'options': {'hostname': PRIVATE[6], 'ip': PRIVATE[5]}}],
        [{'area_id': PRIVATE[2], 'name': PRIVATE[9], 'aliases': [], 'floor_id': None}],
        [{'entry_id': PRIVATE[3], 'domain': 'mqtt', 'title': PRIVATE[9],
          'state': 'loaded', 'supported_subentry_types': {},
          'error_reason_translation_placeholders': None}],
    ]


def report(data=None):
    reducer = m.Reducer()
    for registry, records in zip(m.REGISTRIES, data if data is not None else rows()):
        reducer.consume(registry, records)
    return reducer.finish()


def result(id_, records):
    return json.dumps({'id': id_, 'type': 'result', 'success': True, 'result': records})


class Closed(Exception):
    rcvd = types.SimpleNamespace(code=1000)
    sent = types.SimpleNamespace(code=1000)


class WS:
    def __init__(self, messages=None):
        self.messages = messages if messages is not None else [
            json.dumps({'type': 'auth_required', 'ha_version': m.CORE_TAG}),
            json.dumps({'type': 'auth_ok', 'ha_version': m.CORE_TAG}),
            *[result(i, r) for i, r in enumerate(rows(), 1)]]
        self.sent = []
        self.closed = 0
        self.aborted = 0
        self.transport = self
    async def recv(self):
        if self.messages:
            return self.messages.pop(0)
        raise Closed()
    async def send(self, value):
        self.sent.append(json.loads(value))
    async def close(self):
        self.closed += 1
    def abort(self):
        self.aborted += 1


class MemoryPOSIX:
    O_WRONLY = 1
    O_CREAT = 2
    O_EXCL = 4
    O_NOFOLLOW = 8
    def __init__(self, fixture):
        self.fixture = Path(fixture)
        self.files = {}
        self.fds = {}
        self.events = []
        self.next_fd = 10
        self.fail_event = None
        self.interrupt = False
    def event(self, op, name):
        self.events.append((op, name))
        if self.fail_event == (op, name):
            raise KeyboardInterrupt() if self.interrupt else OSError('synthetic-private-error')
    def open(self, name, flags, mode, dir_fd):
        self.event('open', name)
        if name in self.files:
            raise FileExistsError()
        self.files[name] = bytearray()
        fd = self.next_fd
        self.next_fd += 1
        self.fds[fd] = name
        return fd
    def fchmod(self, fd, mode):
        self.event('chmod', mode)
    def fstat(self, fd):
        return types.SimpleNamespace(st_mode=(stat.S_IFDIR | 0o700) if fd == 1 else (stat.S_IFREG | 0o600), st_uid=12, st_gid=12)
    def geteuid(self):
        return 12
    def getegid(self):
        return 12
    def write(self, fd, view):
        self.event('write', self.fds[fd])
        self.files[self.fds[fd]].extend(view)
        return len(view)
    def fsync(self, fd):
        self.event('fsync', self.fds.get(fd, 'directory'))
    def close(self, fd):
        self.event('close', self.fds[fd])
        del self.fds[fd]
    def link(self, source, target, **kwargs):
        self.event('link', target)
        if target in self.files:
            raise FileExistsError()
        self.files[target] = self.files[source]
        (self.fixture / target).write_bytes(self.files[target])
    def unlink(self, name, dir_fd):
        self.event('unlink', name)
        del self.files[name]
        if (self.fixture/name).exists(): (self.fixture/name).unlink()


class SyntheticSchemaTests(unittest.TestCase):
    def assertPrivateAbsent(self, payload):
        for value in PRIVATE + ['private-unique-id']:
            self.assertNotIn(value, payload)
    def test_multiple_relations_and_mac_no_leak(self):
        data = rows()
        other = copy.deepcopy(data[0][0])
        other.update(id='device-two', via_device_id=PRIVATE[0], disabled_by='user')
        other['connections'] = [['mac', 'aa-bb-cc-dd-ee-01'], ['mac', 'aabb.ccdd.ee01']]
        data[0].append(other)
        entity = copy.deepcopy(data[1][0])
        entity.update(entity_id='scene.secret_scene', device_id=None, platform='template', disabled_by='integration')
        data[1].append(entity)
        r = report(data)
        d, e = r['registries']['device']['counts'], r['registries']['entity']['counts']
        self.assertEqual((d['records'], d['disabled'], d['via_device']), (2, 1, 1))
        self.assertEqual((d['mac_collision_values'], d['mac_conflicting_devices'], d['mac_duplicate_entries']), (1, 2, 1))
        self.assertEqual((e['with_device'], e['without_device'], e['with_area'], e['with_config_entry']), (1, 1, 2, 2))
        self.assertEqual((e['template_platform'], e['scene_domain']), (1, 1))
        self.assertPrivateAbsent(m.validate_report(r).decode())
    def test_zero_registries(self):
        r = report([[], [], [], []])
        self.assertTrue(all(o['counts']['records'] == 0 for o in r['registries'].values()))
    def test_unknown_fields_are_counts_only(self):
        data = rows()
        data[0][0][PRIVATE[6]] = {'token': PRIVATE[7]}
        r = report(data)
        self.assertEqual(r['registries']['device']['counts']['unknown_object'], 1)
        self.assertIn('UNKNOWN_FIELDS', r['warnings'])
        self.assertPrivateAbsent(m.canonical(r).decode())
    def test_unknown_namespace_not_published(self):
        data = rows()
        data[0][0]['identifiers'].append([PRIVATE[6], PRIVATE[5]])
        r = report(data)
        self.assertEqual(r['registries']['device']['counts']['unpublished_namespaces'], 1)
        self.assertPrivateAbsent(m.canonical(r).decode())
    def test_namespace_types_and_zero_one_multiple_connections(self):
        data = rows()
        for index, connections in enumerate([[], [['zigbee', 'private']], [['mac', PRIVATE[4]], ['upnp', 'private']]]):
            d = copy.deepcopy(data[0][0]); d.update(id=f'private-device-{index}', connections=connections)
            data[0].append(d)
        r = report(data)['registries']['device']
        self.assertEqual([r['counts']['connections_' + n] for n in ['zero', 'one', 'multiple']], [1, 2, 1])
        self.assertEqual(r['namespaces']['connection'], ['mac', 'upnp', 'zigbee'])
    def test_structure_fingerprint_excludes_values_counts_and_namespaces(self):
        data = rows(); original = report(data)
        data[0][0]['connections'] = [['upnp', 'different-private-value']]
        data[0].append(dict(data[0][0], id='other-private-device'))
        self.assertEqual(original['structure_fingerprint'], report(data)['structure_fingerprint'])
    def test_optional_fields_inventory(self):
        data = rows(); data[0].append(dict(data[0][0], id='two'))
        del data[0][1]['name']
        self.assertEqual(report(data)['registries']['device']['fields']['name'], {'types': ['string'], 'optional': True})
    def test_malformed_cores_types_pairs_and_duplicate_ids(self):
        variants = []
        for key, value in [('connections', 'bad'), ('identifiers', [[1, 2]]), ('id', None), ('area_id', 3), ('disabled_by', True)]:
            d = rows(); d[0][0][key] = value; variants.append(d)
        d = rows(); del d[1][0]['device_id']; variants.append(d)
        d = rows(); d[0].append(copy.deepcopy(d[0][0])); variants.append(d)
        for data in variants:
            with self.subTest(data_index=variants.index(data)), self.assertRaises(m.Failure): report(data)
    def test_record_limits_exact_and_over(self):
        for registry in m.REGISTRIES:
            with self.subTest(registry=registry), patch.dict(m.MAX_RECORDS, {registry: 2}):
                reducer = m.Reducer(); row = rows()[m.REGISTRIES.index(registry)][0]
                valid = [dict(row, **{m.ID_FIELD[registry]: str(i)}) for i in range(2)]
                reducer.consume(registry, valid)
                with self.assertRaises(m.Failure): m.Reducer().consume(registry, valid + [row])
    def test_field_and_namespace_bounds(self):
        with patch.object(m, 'MAX_FIELDS', 3), self.assertRaises(m.Failure): report()
        data = rows(); data[0][0]['connections'] = [['one', 'a'], ['two', 'b']]
        with patch.object(m, 'MAX_NAMESPACES', 1), self.assertRaises(m.Failure): report(data)
        with patch.object(m, 'MAX_FIELD_NAMES', 1), self.assertRaises(m.Failure): report()
    def test_dangling_relationships_count_only(self):
        data = rows(); data[1][0]['device_id'] = 'missing-private'
        r = report(data)
        self.assertEqual(r['registries']['entity']['counts']['dangling_relationships'], 1)
        self.assertNotIn('missing-private', m.canonical(r).decode())
    def test_mac_formats(self):
        for value in ['aa:bb:cc:dd:ee:01', 'AA-BB-CC-DD-EE-01', 'aabb.ccdd.ee01', 'aabbccddee01']:
            self.assertEqual(m.normalize_mac(value), 'aabbccddee01')
        for value in ['aa:::bbccddeeff', 'wrong-private', '192.168.50.10']:
            self.assertIsNone(m.normalize_mac(value))
    def test_no_mac_hash(self):
        source = (ROOT / 'tools/hioc-pe4-ha-registry-discovery.py').read_text()
        self.assertNotIn('hashlib.sha256(value', source)
        self.assertNotIn('hashlib.sha256(norm', source)
    def test_json_duplicate_nested_nonfinite_deep_binary(self):
        for raw in ['{"type":"result","type":"event"}', '{"a":{"x":1,"x":2}}',
                    '{"x":NaN}', '{"x":Infinity}', '{"x":' + '[' * 40 + '0' + ']' * 40 + '}', b'{}', '[]']:
            with self.subTest(raw_type=type(raw)), self.assertRaises(m.Failure): m.strict_message(raw)
    def test_json_exact_byte_and_depth_limits(self):
        raw = '{"x":"abc"}'
        with patch.object(m, 'MAX_MESSAGE', len(raw.encode())): self.assertEqual(m.strict_message(raw)['x'], 'abc')
        with patch.object(m, 'MAX_MESSAGE', len(raw.encode()) - 1), self.assertRaises(m.Failure): m.strict_message(raw)
        with patch.object(m, 'MAX_DEPTH', 2): self.assertEqual(m.strict_message('{"x":[0]}')['x'], [0])
        with patch.object(m, 'MAX_DEPTH', 1), self.assertRaises(m.Failure): m.strict_message('{"x":[0]}')
    def test_decoder_resource_errors_normalized(self):
        for error in (RecursionError, MemoryError, OverflowError):
            with patch.object(m.json, 'loads', side_effect=error), self.assertRaises(m.Failure): m.strict_message('{}')
    def test_final_validator_rejects_raw_values_keys_and_types(self):
        good = report()
        mutations = [dict(good, token=PRIVATE[7]), dict(good, INSTANCE_REFERENCE=PRIVATE[6]),
                     dict(good, warnings=[PRIVATE[8]]), dict(good, structure_fingerprint=PRIVATE[4])]
        r = copy.deepcopy(good); r['registries']['device']['fields'][PRIVATE[1]] = {'types':['string'], 'optional':False}; mutations.append(r)
        r = copy.deepcopy(good); r['registries']['device']['counts']['records'] = True; mutations.append(r)
        r = copy.deepcopy(good); r['registries']['device']['namespaces']['connection'] = [PRIVATE[4]]; mutations.append(r)
        for r in mutations:
            with self.assertRaises(m.Failure): m.validate_report(r)
    def test_evidence_size_warning_limits(self):
        r = report(); size = len(m.validate_report(r))
        with patch.object(m, 'MAX_EVIDENCE', size): m.validate_report(r)
        with patch.object(m, 'MAX_EVIDENCE', size-1), self.assertRaises(m.Failure): m.validate_report(r)
        r['warnings'] = ['UNKNOWN_FIELDS'] * (m.MAX_WARNINGS + 1)
        with self.assertRaises(m.Failure): m.validate_report(r)
    def test_failure_report_is_minimal(self):
        r = m.base_report('AUTHENTICATION_FAILED', 'AUTHENTICATION')
        self.assertEqual(r['registries'], {})
        m.validate_report(r)


class NetworkTests(unittest.IsolatedAsyncioTestCase):
    async def test_exact_four_order_ids_and_no_other_commands(self):
        ws = WS(); r = await m.exchange(ws, PRIVATE[7], m.time.monotonic()+10)
        self.assertEqual([x['type'] for x in ws.sent], ['auth', *m.COMMANDS])
        self.assertEqual([x['id'] for x in ws.sent[1:]], [1,2,3,4])
        self.assertEqual(ws.closed, 1)
        self.assertNotIn(PRIVATE[7], m.canonical(r).decode())
    async def test_response_correlation_envelope_events_replay(self):
        for replacement in [result(2, []), result(True, []), '{"type":"event","id":1}',
                            '{"id":1,"type":"result","success":1,"result":[]}',
                            '{"id":1,"type":"result","success":true,"result":[],"error":{}}']:
            ws = WS(); ws.messages[2] = replacement
            with self.assertRaises(m.Failure): await m.exchange(ws, 'synthetic', m.time.monotonic()+10)
            self.assertEqual(len(ws.sent), 2)
    async def test_error_classification(self):
        for code, expected in [('unauthorized','INSUFFICIENT_READ_SCOPE'), ('unknown_command','UNSUPPORTED_INTERFACE'), ('unknown_error','UNEXPECTED_SCHEMA')]:
            ws = WS(); ws.messages[2] = json.dumps({'id':1,'type':'result','success':False,'error':{'code':code,'message':PRIVATE[9]}})
            with self.assertRaises(m.Failure) as got: await m.exchange(ws, 'synthetic', m.time.monotonic()+10)
            self.assertEqual(got.exception.code, expected)
            self.assertNotIn(PRIVATE[9], str(got.exception))
    async def test_auth_failure_and_version_pin(self):
        ws = WS(); ws.messages[1] = json.dumps({'type':'auth_invalid','message':PRIVATE[9]})
        with self.assertRaises(m.Failure) as got: await m.exchange(ws,'synthetic', m.time.monotonic()+10)
        self.assertEqual(got.exception.code, 'AUTHENTICATION_FAILED')
        self.assertEqual(len(ws.sent),1)
        ws = WS(); ws.messages[0] = json.dumps({'type':'auth_required','ha_version':'2026.8.2'})
        with self.assertRaises(m.Failure) as got: await m.exchange(ws,'synthetic',m.time.monotonic()+10)
        self.assertEqual(got.exception.code,'UNSUPPORTED_HA_DEPLOYMENT')
        self.assertEqual(ws.sent, [])
    async def test_extra_response_rejected_after_fourth(self):
        ws = WS(); ws.messages.append(result(4, []))
        with self.assertRaises(m.Failure): await m.exchange(ws,'synthetic',m.time.monotonic()+10)
        self.assertEqual(len(ws.sent),5)
    async def test_stalled_send_receive_close_no_orphan(self):
        async def stall(*args): await asyncio.Future()
        for operation in ['send','recv','close']:
            ws = WS(); setattr(ws, operation, stall)
            with patch.object(m,'RECEIVE_TIMEOUT',0.01), patch.object(m,'CLOSE_TIMEOUT',0.01), self.assertRaises(m.Failure):
                await m.exchange(ws,'synthetic',m.time.monotonic()+1)
            self.assertGreater(ws.aborted,0)
            self.assertEqual([t for t in asyncio.all_tasks() if t is not asyncio.current_task() and not t.done()], [])
    async def test_absolute_deadline_no_reset_no_coroutine_before_expiry(self):
        called = []
        async def operation(): called.append(1)
        with self.assertRaises(m.Failure): await m.bounded(operation,m.time.monotonic()-1,15,'INTERFACE_DISCOVERY')
        self.assertEqual(called,[])
        ws = WS(); original = ws.recv
        async def slow():
            await asyncio.sleep(.015)
            return await original()
        ws.recv = slow
        with self.assertRaises(m.Failure): await m.exchange(ws,'synthetic',m.time.monotonic()+.045)
        self.assertLess(len(ws.sent),5)
    async def test_interrupt_cleanup(self):
        ws = WS()
        async def interrupted(*args): raise asyncio.CancelledError()
        ws.send=interrupted
        with self.assertRaises(asyncio.CancelledError): await m.exchange(ws,'synthetic',m.time.monotonic()+10)
        self.assertGreater(ws.aborted,0)


class PublicationTests(unittest.TestCase):
    def test_atomic_result_last_no_raw_files_and_collision(self):
        with tempfile.TemporaryDirectory() as fixture:
            ops = MemoryPOSIX(fixture); r = report()
            m.publish_files(1,r,ops)
            self.assertEqual(set(ops.files), {'discovery-report.json','discovery-result.txt'})
            for data in ops.files.values():
                for private in PRIVATE: self.assertNotIn(private.encode(),data)
            links = [name for op,name in ops.events if op=='link']
            self.assertEqual(links, ['discovery-report.json','discovery-result.txt'])
            first_result = ops.events.index(('link','discovery-result.txt'))
            self.assertIn(('fsync','directory'), ops.events[:first_result])
            saved = bytes(ops.files['discovery-report.json'])
            with self.assertRaises(FileExistsError): m.publish_files(1,r,ops)
            self.assertEqual(bytes(ops.files['discovery-report.json']),saved)
            self.assertFalse(ops.fds)
            self.assertFalse(any(name.startswith('.publish-') for name in ops.files))
    def test_result_collision_not_overwritten(self):
        with tempfile.TemporaryDirectory() as fixture:
            ops = MemoryPOSIX(fixture); ops.files['discovery-result.txt']=bytearray(b'original')
            with self.assertRaises(FileExistsError): m.publish_files(1,report(),ops)
            self.assertEqual(ops.files['discovery-result.txt'],b'original')
    def test_interruption_cleanup_no_result(self):
        with tempfile.TemporaryDirectory() as fixture:
            ops = MemoryPOSIX(fixture); ops.fail_event=('link','discovery-report.json'); ops.interrupt=True
            with self.assertRaises(KeyboardInterrupt): m.publish_files(1,report(),ops)
            self.assertEqual(ops.files,{})
            self.assertFalse(ops.fds)
    def test_unsafe_evidence_rejected_before_open(self):
        with tempfile.TemporaryDirectory() as fixture:
            ops=MemoryPOSIX(fixture)
            with self.assertRaises(m.Failure): m.publish_files(1,{'token':PRIVATE[7]},ops)
            self.assertEqual(ops.events,[])
    def test_secure_prompt_warning_fatal_no_fallback(self):
        def prompt(_): warnings.warn('synthetic', m.getpass.GetPassWarning); return PRIVATE[7]
        with self.assertRaises(m.Failure): m.acquire_token(prompt)
    def test_no_argv_env_file_credential(self):
        for value in ['', 'x\ny', None]:
            with self.assertRaises(m.Failure): m.acquire_token(lambda _:value)
    def test_preflight_failure_no_prompt_network_evidence(self):
        out=[]
        with patch.object(m,'preflight',side_effect=m.Failure('WRONG_TARGET','TARGET_IDENTITY')), patch.object(m,'acquire_token') as prompt, patch.object(m,'discover') as net, patch.object(m,'publish') as publication:
            self.assertEqual(m.run([],out.append),1)
            prompt.assert_not_called(); net.assert_not_called(); publication.assert_not_called()
    def test_success_main_sanitized_publication(self):
        with patch.object(m,'preflight'), patch.object(m,'acquire_token',return_value=PRIVATE[7]), patch.object(m,'discover',return_value=report()), patch.object(m,'publish') as publication:
            out=[]; self.assertEqual(m.run([],out.append),0)
            publication.assert_called_once()
            self.assertNotIn(PRIVATE[7], ''.join(out))
    def test_failed_network_sanitized_failure_publication(self):
        with patch.object(m,'preflight'), patch.object(m,'acquire_token',return_value=PRIVATE[7]), patch.object(m,'discover',side_effect=m.Failure('AUTHENTICATION_FAILED','AUTHENTICATION')), patch.object(m,'publish') as publication:
            out=[]; self.assertEqual(m.run([],out.append),1)
            self.assertEqual(publication.call_args.args[0]['result'],'FAIL')
            self.assertNotIn(PRIVATE[7], ''.join(out))
    def test_publication_failure_no_retry_no_pass(self):
        with patch.object(m,'preflight'), patch.object(m,'acquire_token',return_value=PRIVATE[7]), patch.object(m,'discover',return_value=report()), patch.object(m,'publish',side_effect=m.Failure('EVIDENCE_PUBLICATION_FAILED','EVIDENCE_PUBLICATION')) as publication:
            out=[]; self.assertEqual(m.run([],out.append),1)
            publication.assert_called_once(); self.assertNotIn('RESULT=PASS',''.join(out))





def validate_schema(value, schema, root=None):
    """Independent executor for every JSON Schema keyword in this one fixture.

    Kept test-only: the standalone client uses its own stricter final validator.
    Unknown keywords fail the test rather than silently weakening validation.
    """
    root = root or schema
    allowed = {'$schema','$id','$defs','$ref','title','type','const','enum','properties',
               'additionalProperties','required','items','minItems','maxItems','uniqueItems',
               'minimum','maximum','minLength','maxLength','pattern','anyOf','allOf','if','then','else'}
    if set(schema)-allowed: raise AssertionError('unhandled schema keyword')
    if '$ref' in schema:
        target=root
        for part in schema['$ref'].removeprefix('#/').split('/'): target=target[part]
        validate_schema(value,target,root)
    if 'const' in schema and (type(value) is not type(schema['const']) or value != schema['const']): raise ValueError()
    if 'enum' in schema and not any(type(value) is type(x) and value==x for x in schema['enum']): raise ValueError()
    if 'anyOf' in schema:
        for branch in schema['anyOf']:
            try: validate_schema(value,branch,root); break
            except ValueError: pass
        else: raise ValueError()
    for branch in schema.get('allOf',[]): validate_schema(value,branch,root)
    if 'if' in schema:
        try: validate_schema(value,schema['if'],root); branch='then'
        except ValueError: branch='else'
        if branch in schema: validate_schema(value,schema[branch],root)
    types={'object':dict,'array':list,'string':str,'boolean':bool,'integer':int,'null':type(None)}
    if 'type' in schema and type(value) is not types[schema['type']]: raise ValueError()
    if type(value) is dict:
        props=schema.get('properties',{})
        if not set(schema.get('required',[])).issubset(value): raise ValueError()
        if schema.get('additionalProperties') is False and set(value)-set(props): raise ValueError()
        for key,item in value.items():
            if key in props: validate_schema(item,props[key],root)
    if type(value) is list:
        if len(value)<schema.get('minItems',0) or len(value)>schema.get('maxItems',10**9): raise ValueError()
        if schema.get('uniqueItems') and len({json.dumps(x,sort_keys=True) for x in value})!=len(value): raise ValueError()
        if 'items' in schema:
            for item in value: validate_schema(item,schema['items'],root)
    if type(value) is int:
        if value<schema.get('minimum',-10**30) or value>schema.get('maximum',10**30): raise ValueError()
    if type(value) is str:
        if len(value)<schema.get('minLength',0) or len(value)>schema.get('maxLength',10**9): raise ValueError()
        if 'pattern' in schema and not m.re.search(schema['pattern'],value): raise ValueError()


class SourceAndSchemaTests(unittest.TestCase):
    def test_pinned_compact_source_contract(self):
        facts=json.loads((ROOT/'governance/pe4/pe4-0b2b-core-source-contract.json').read_text())
        self.assertEqual(facts['core_tag'],'2026.8.1')
        self.assertEqual([x['command'] for x in facts['commands']],list(m.COMMANDS))
        for item,registry in zip(facts['commands'],m.REGISTRIES):
            self.assertTrue(item['read_only']); self.assertFalse(item['admin_required'])
            self.assertEqual(item['result_shape'],'ARRAY_OF_OBJECTS')
            self.assertEqual(item['mandatory_core'],sorted(m.CORE[registry]))
            self.assertEqual(item['recognized_fields'],{k:sorted(v) for k,v in m.FIELDS[registry].items()})
        self.assertEqual(len(facts['sources']),10)
        for source in facts['sources']:
            self.assertTrue(source['url'].startswith('https://raw.githubusercontent.com/home-assistant/core/2026.8.1/'))
    def test_versioned_schema_accepts_reports_rejects_unsafe(self):
        schema=json.loads((ROOT/'governance/pe4/pe4-0b2b-discovery-report.schema.json').read_text())
        validate_schema(report(),schema)
        for code in m.ERROR_CODES: validate_schema(m.base_report(code,'SCHEMA_DISCOVERY'),schema)
        for r in [dict(report(),raw=PRIVATE[7]),dict(report(),INSTANCE_REFERENCE=PRIVATE[9]),
                  dict(report(),result='FAIL'),dict(report(),ERROR_CODE='UNEXPECTED_ERROR')]:
            with self.assertRaises(ValueError): validate_schema(r,schema)
    def test_closed_2a_identity_and_no_dependencies_on_2a_fg_runtime(self):
        raw=(ROOT/'tools/hioc-pe4-ha-auth-capability.py').read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(),'aa0e58ed6c7bb4586625836cc71ad0cab9270e6b11a6a5db66497115b001decf')
        source=(ROOT/'tools/hioc-pe4-ha-registry-discovery.py').read_text()
        for excluded in ['hioc-pe4-ha-auth-capability.py','hioc_pe4_action_f','hioc_pe4_action_g','hioc_pe4_runtime_common']:
            self.assertNotIn(excluded,source)
    def test_no_mutation_subscription_followups(self):
        for command in m.COMMANDS:
            self.assertNotRegex(command,r'update|delete|create|disable|reload|subscribe|flow|service|state|event|supported_features|get_single|linked')
        self.assertEqual(len(m.COMMANDS),4)
    def test_actual_record_limits_exact_and_one_over(self):
        # Real frozen limits, not only reduced fixture limits.
        for registry in m.REGISTRIES:
            row=rows()[m.REGISTRIES.index(registry)][0]
            records=[dict(row,**{m.ID_FIELD[registry]:f'private-{i}'}) for i in range(m.MAX_RECORDS[registry])]
            reducer=m.Reducer(); reducer.consume(registry,records)
            self.assertEqual(reducer.observations[registry]['counts']['records'],m.MAX_RECORDS[registry])
            with self.assertRaises(m.Failure): m.Reducer().consume(registry,records+[row])
    def test_actual_message_limit_exact_and_one_over(self):
        raw='{"x":"'+'a'*(m.MAX_MESSAGE-8)+'"}'
        self.assertEqual(len(raw.encode()),m.MAX_MESSAGE)
        m.strict_message(raw)
        with self.assertRaises(m.Failure): m.strict_message(raw+' ')


class ConnectionPolicyTests(unittest.IsolatedAsyncioTestCase):
    async def test_preconnected_numeric_socket_no_proxy_redirect_or_retry(self):
        ws=WS(); calls=[]
        class Connector:
            def __init__(self,uri,**kwargs): calls.append((uri,kwargs))
            def process_redirect(self,exc): return 'UNSAFE_DEFAULT'
            def __await__(self):
                async def get(): return ws
                return get().__await__()
        module=types.SimpleNamespace(__version__='16.1.1',connect=Connector)
        sock=types.SimpleNamespace(setblocking=lambda _:None,close=lambda:None)
        loop=asyncio.get_running_loop()
        with patch.object(m,'socket',types.SimpleNamespace(AF_INET=2,SOCK_STREAM=1,socket=lambda *args:sock)), patch.object(loop,'sock_connect',new_callable=__import__('unittest.mock',fromlist=['AsyncMock']).AsyncMock) as connect:
            r=await m.discover('synthetic',module)
        connect.assert_awaited_once_with(sock,('192.168.100.251',8123))
        self.assertEqual(len(calls),1)
        kwargs=calls[0][1]
        self.assertIsNone(kwargs['proxy']); self.assertIsNone(kwargs['ping_interval']); self.assertIsNone(kwargs['compression'])
        self.assertEqual(kwargs['max_size'],m.MAX_MESSAGE)
        self.assertIs(kwargs['sock'],sock)
        self.assertEqual(r['result'],'PASS')
        # Subclass intercepts every redirect and returns the original exception.
        self.assertNotIn('getaddrinfo',(ROOT/'tools/hioc-pe4-ha-registry-discovery.py').read_text().replace('no getaddrinfo/DNS',''))
    async def test_connect_stall_bounded_no_retry(self):
        class Connector:
            def process_redirect(self,exc): return exc
        module=types.SimpleNamespace(__version__='16.1.1',connect=Connector)
        sock=types.SimpleNamespace(setblocking=lambda _:None,close=lambda:None)
        async def stalled(*args): await asyncio.Future()
        with patch.object(m,'socket',types.SimpleNamespace(AF_INET=2,SOCK_STREAM=1,socket=lambda *args:sock)), patch.object(asyncio.get_running_loop(),'sock_connect',side_effect=stalled) as connect, patch.object(m,'CONNECT_TIMEOUT',.01):
            with self.assertRaises(m.Failure): await m.discover('synthetic',module)
        self.assertEqual(connect.call_count,1)
    async def test_incompatible_dependency_rejected_before_socket(self):
        with patch.object(m.socket,'socket') as create:
            with self.assertRaises(m.Failure): await m.discover('synthetic',types.SimpleNamespace(__version__='wrong'))
            create.assert_not_called()


class PublicationFaultTests(unittest.TestCase):
    def test_report_and_result_link_failures_cleanup(self):
        for target in ['discovery-report.json','discovery-result.txt']:
            with self.subTest(target=target), tempfile.TemporaryDirectory() as fixture:
                ops=MemoryPOSIX(fixture); ops.fail_event=('link',target)
                with self.assertRaises(OSError): m.publish_files(1,report(),ops)
                self.assertNotIn('discovery-result.txt',ops.files)
                self.assertFalse(ops.fds)
                self.assertFalse(any(x.startswith('.publish-') for x in ops.files))
    def test_result_durability_failure_withdraws_marker(self):
        with tempfile.TemporaryDirectory() as fixture:
            ops=MemoryPOSIX(fixture)
            old_sync=ops.fsync; number=0
            def sync(fd):
                nonlocal number
                if fd==1:
                    number+=1
                    if number==2: raise OSError('synthetic')
                old_sync(fd)
            ops.fsync=sync
            with self.assertRaises(OSError): m.publish_files(1,report(),ops)
            self.assertNotIn('discovery-result.txt',ops.files)
            self.assertIn('discovery-report.json',ops.files)
    def test_partial_writes_and_zero_write(self):
        with tempfile.TemporaryDirectory() as fixture:
            ops=MemoryPOSIX(fixture); orig=ops.write
            ops.write=lambda fd,view:orig(fd,view[:7])
            m.publish_files(1,report(),ops)
            self.assertEqual(bytes(ops.files['discovery-report.json']),m.validate_report(report()))
        with tempfile.TemporaryDirectory() as fixture:
            ops=MemoryPOSIX(fixture); ops.write=lambda fd,view:0
            with self.assertRaises(OSError): m.publish_files(1,report(),ops)
            self.assertEqual(ops.files,{})
    def test_wrong_directory_or_file_metadata(self):
        for directory in [True,False]:
            with tempfile.TemporaryDirectory() as fixture:
                ops=MemoryPOSIX(fixture); original=ops.fstat
                def wrong(fd):
                    info=original(fd)
                    if (fd==1)==directory: info.st_uid=99
                    return info
                ops.fstat=wrong
                with self.assertRaises(m.Failure): m.publish_files(1,report(),ops)
                self.assertEqual(ops.files,{})





class DirectoryPOSIX(MemoryPOSIX):
    O_RDONLY=16
    O_DIRECTORY=32
    def __init__(self,fixture):
        super().__init__(fixture)
        self.directory=None
        self.bad_parent=False
        self.bad_binding=False
    def open(self,name,flags,mode=None,dir_fd=None):
        if name=='/tmp':
            self.event('parent_open',(name,flags)); return 2
        if name==self.directory:
            self.event('directory_open',(name,flags,dir_fd)); return 1
        return super().open(name,flags,mode,dir_fd)
    def mkdir(self,name,mode,dir_fd):
        self.event('mkdir',(name,mode,dir_fd)); self.directory=name
    def fstat(self,fd):
        if fd==2:
            return types.SimpleNamespace(st_mode=stat.S_IFDIR|0o1777,st_uid=99 if self.bad_parent else 0,st_gid=0,st_dev=4,st_ino=2)
        if fd==1:
            return types.SimpleNamespace(st_mode=stat.S_IFDIR|0o700,st_uid=12,st_gid=12,st_dev=4,st_ino=1)
        return super().fstat(fd)
    def stat(self,name,**kwargs):
        info=self.fstat(2 if name=='/tmp' else 1)
        if name!='/tmp' and name==self.directory and self.bad_binding: info.st_ino=99
        return info
    def close(self,fd):
        if fd in {1,2}: self.event('directory_close',fd)
        else: super().close(fd)


class DirectoryAndGateTests(unittest.TestCase):
    def test_real_publish_orchestration_under_controlled_fixture(self):
        with tempfile.TemporaryDirectory() as fixture:
            ops=DirectoryPOSIX(fixture)
            # inject adapter into production directory flow and publication core
            original=m.publish_files
            with patch.object(m,'os',ops), patch.object(m,'publish_files',side_effect=lambda fd,r,guard:original(fd,r,ops,guard)):
                m.publish(report())
            self.assertRegex(ops.directory,r'^hioc-pe4-ha-discovery-[0-9a-f]{8}$')
            self.assertIn(('mkdir',(ops.directory,0o700,2)),ops.events)
            self.assertIn(('directory_open',(ops.directory,ops.O_RDONLY|ops.O_DIRECTORY|ops.O_NOFOLLOW,2)),ops.events)
            self.assertEqual(set(p.name for p in Path(fixture).iterdir()),{'discovery-report.json','discovery-result.txt'})
    def test_untrusted_tmp_and_directory_substitution_fail_closed(self):
        for bad in ['bad_parent','bad_binding']:
            with tempfile.TemporaryDirectory() as fixture:
                ops=DirectoryPOSIX(fixture); setattr(ops,bad,True)
                with patch.object(m,'os',ops), self.assertRaises(m.Failure) as got:
                    m.publish(report())
                self.assertEqual(got.exception.code,'EVIDENCE_PUBLICATION_FAILED')
                self.assertEqual(ops.files,{})
    def test_directory_guard_failure_withdraws_result(self):
        with tempfile.TemporaryDirectory() as fixture:
            ops=MemoryPOSIX(fixture); checks=0
            def guard():
                nonlocal checks
                checks+=1
                if checks==6: raise m.Failure('EVIDENCE_PUBLICATION_FAILED','EVIDENCE_PUBLICATION')
            with self.assertRaises(m.Failure): m.publish_files(1,report(),ops,guard)
            self.assertNotIn('discovery-result.txt',ops.files)
            self.assertFalse(ops.fds)
    def test_terminal_gates_before_getpass(self):
        # Reproduce approved host/runtime without OS queries or a real credential.
        env='/home/jazofv1/hioc/runtime/pe4/environments/cpython311-websockets16.1.1-lock-v1'
        operator=types.SimpleNamespace(getpwuid=lambda _:types.SimpleNamespace(pw_name='jazofv1'))
        os_stub=types.SimpleNamespace(name='posix',path=m.os.path,geteuid=lambda:12,environ={})
        sys_stub=types.SimpleNamespace(version_info=(3,11,2),prefix=env,
            flags=types.SimpleNamespace(isolated=1,dont_write_bytecode=1),
            stdin=types.SimpleNamespace(isatty=lambda:True),stderr=types.SimpleNamespace(isatty=lambda:True))
        module=types.SimpleNamespace(__version__='16.1.1',__file__=env+'/lib/python3.11/site-packages/websockets/__init__.py')
        # Host's Windows realpath has Windows separators; emulate POSIX realpath.
        os_stub.path=types.SimpleNamespace(realpath=lambda p:p)
        with patch.object(m,'os',os_stub), patch.object(m,'sys',sys_stub), patch.object(m,'socket',types.SimpleNamespace(gethostname=lambda:'nutandpihole')), patch.dict(__import__('sys').modules,{'pwd':operator}), patch.object(m.subprocess,'run',return_value=types.SimpleNamespace(stdout='inet 192.168.100.252/24')), patch.object(m.importlib,'import_module',return_value=module):
            m.preflight([])
            for component in ['stdin','stderr']:
                original=getattr(sys_stub,component)
                setattr(sys_stub,component,types.SimpleNamespace(isatty=lambda:False))
                with self.assertRaises(m.Failure) as got: m.preflight([])
                self.assertEqual(got.exception.code,'AUTHENTICATION_UNAVAILABLE')
                setattr(sys_stub,component,original)
            for name in ['HTTP_PROXY','http_proxy','ALL_PROXY','NO_PROXY']:
                os_stub.environ={name:'synthetic'}
                with self.assertRaises(m.Failure):m.preflight([])
            os_stub.environ={}
            with self.assertRaises(m.Failure):m.preflight(['--token=synthetic'])
            sys_stub.flags.isolated=0
            with self.assertRaises(m.Failure):m.preflight([])





class AdditionalBoundaryTests(unittest.TestCase):
    def test_actual_field_and_namespace_limits(self):
        data=rows(); row=data[0][0]
        row.update({f'unknown_{i}':None for i in range(m.MAX_FIELDS-len(row))})
        report(data)
        row['one_extra_field']=None
        with self.assertRaises(m.Failure): report(data)
        data=rows()
        data[0][0]['connections']=[[f'namespace_{i}','private-value'] for i in range(m.MAX_NAMESPACES)]
        data[0][0]['identifiers']=[]
        report(data)
        data[0][0]['identifiers']=[['one_more_namespace','private-value']]
        with self.assertRaises(m.Failure):report(data)
    def test_actual_global_field_name_limit(self):
        registry='device'; row=rows()[0][0]; originals=set(row)
        reducer=m.Reducer()
        records=[]
        for i in range(3):
            r=dict(row,id=f'private-{i}')
            extras={f'unknown_{j}':None for j in range(i*(m.MAX_FIELDS-len(row)),(i+1)*(m.MAX_FIELDS-len(row)))}
            r.update(extras);records.append(r)
        # Select exactly 256 unique names across rows, then add the 257th.
        names=set().union(*(set(r) for r in records))
        remove=sorted(names-originals)[m.MAX_FIELD_NAMES-len(originals):]
        for r in records:
            for name in remove:r.pop(name,None)
        reducer.consume(registry,records)
        self.assertEqual(len(reducer.field_union),m.MAX_FIELD_NAMES)
        records[-1]['one_more_field']=None
        with self.assertRaises(m.Failure):m.Reducer().consume(registry,records)
    def test_finite_numbers_and_invalid_unicode(self):
        for raw in ['{"x":{"private":1e999}}','{"x":"\ud800"}']:
            with self.assertRaises(m.Failure):m.strict_message(raw)
    def test_mac_invalid_and_connection_identifier_collisions(self):
        data=rows(); row=copy.deepcopy(data[0][0]);row['id']='second-private-device'
        data[0].append(row)
        r=report(data)['registries']['device']['counts']
        self.assertEqual(r['connection_collision_values'],1)
        self.assertEqual(r['identifier_collision_values'],1)
        data[0][0]['connections']=[['mac','invalid-private-mac']]
        self.assertEqual(report(data)['registries']['device']['counts']['mac_invalid'],1)
    def test_warning_duplicates_and_bound_rejected(self):
        r=report();r['warnings']=['UNKNOWN_FIELDS','UNKNOWN_FIELDS']
        with self.assertRaises(m.Failure): m.validate_report(r)
        r['warnings']=['UNKNOWN_FIELDS']*(m.MAX_WARNINGS+1)
        with self.assertRaises(m.Failure): m.validate_report(r)
    def test_standalone_client_governance_boundary(self):
        source=(ROOT/'tools/hioc-pe4-ha-registry-discovery.py').read_text()
        self.assertNotIn('--governance-commit',source)
        record=json.loads((ROOT/'governance/pe4/pe4-0b2b-discovery-preparation.json').read_text())
        self.assertIn('SEPARATE_2B_EXECUTION_AUTHORIZATION',record['future_pre_token_gates'])
        with self.assertRaises(m.Failure): m.preflight(['--governance-commit='+'0'*40])
    def test_publication_permissions_and_flags(self):
        with tempfile.TemporaryDirectory() as fixture:
            ops=MemoryPOSIX(fixture); seen=[]; old=ops.open
            def opened(name,flags,mode,dir_fd):
                seen.append((flags,mode,dir_fd));return old(name,flags,mode,dir_fd)
            ops.open=opened;m.publish_files(1,report(),ops)
            self.assertEqual(seen,[(ops.O_WRONLY|ops.O_CREAT|ops.O_EXCL|ops.O_NOFOLLOW,0o600,1)]*2)
    def test_preparation_record_bindings(self):
        path=ROOT/'governance/pe4/pe4-0b2b-discovery-preparation.json'
        record=json.loads(path.read_text())
        raw=(ROOT/record['source']['repository_path']).read_bytes()
        self.assertEqual(record['source']['sha256'],hashlib.sha256(raw).hexdigest())
        # Git's clean filter preserves LF canonical tool source.
        header=f'blob {len(raw)}\0'.encode();self.assertEqual(record['source']['git_blob'],hashlib.sha1(header+raw).hexdigest())
        self.assertEqual(record['core_tag'],m.CORE_TAG)
        self.assertEqual(record['commands'],list(m.COMMANDS))
        self.assertEqual(record['lifecycle']['pe4_0b2a'],'PASS_CLOSED')
        self.assertEqual(record['lifecycle']['pe4_0b2b'],'NOT_STARTED')
        self.assertFalse(record['discovery_executed'])
        self.assertEqual(record['bounds']['max_records'],m.MAX_RECORDS)
        self.assertEqual(record['prerequisite']['commit'],'09814b8ab19553f21ff68c3a617a5164c47ef59f')


if __name__ == '__main__': unittest.main()
