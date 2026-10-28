"""Synthetic API/transport qualification, never a production execution."""
import ast
import base64
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import unittest
from unittest.mock import patch

SOURCE=Path(__file__).resolve().parents[1]/'tools/pe73_ha_live_qualify.py'
spec=importlib.util.spec_from_file_location('live_qualifier',SOURCE)
q=importlib.util.module_from_spec(spec)
spec.loader.exec_module(q)
SECRET='synthetic-test-secret-never-production'


def config():
    return {'title':'HIOC Dashboard v2','views':[{'title':p,'path':'hioc-v2-'+p,'cards':[]} for p in ('executive','operations','diagnostics','inventory','network','servers')]}


class API:
    def __init__(self):
        self.calls=[];self.fail={};self.selectors=[]
        self.data={'auth/current_user':{'id':'synthetic-admin','name':SECRET,'is_admin':True,'credentials':[SECRET]},
            'get_config':{'components':['lovelace'],'version':'2026.10.4','private':SECRET,'safe_mode':False,'recovery_mode':False},
            'get_services':{},'get_panels':{'lovelace':{'component_name':'lovelace','config':{'mode':'storage'}}},
            'lovelace/info':{'resource_mode':'storage'},
            'lovelace/dashboards/list':[{'url_path':q.TARGET,'title':'HIOC Dashboard v2','mode':'storage'}],
            'lovelace/resources/list':[],('lovelace/config',q.TARGET):config(),
            ('lovelace/config',None):{'views':[]}}

    def call(self,kind,**fields):
        self.calls.append(kind)
        if kind=='lovelace/config':self.selectors.append(fields.get('url_path'))
        if kind not in q.READS:raise AssertionError('mutation')
        if kind in self.fail:raise self.fail[kind]
        key=(kind,fields.get('url_path')) if kind=='lovelace/config' else kind
        return copy.deepcopy(self.data[key])


class QualificationTests(unittest.TestCase):
    def setUp(self):self.api=API()
    def run_api(self):return q.qualify(self.api)
    def blocked(self,code):
        r=self.run_api();self.assertTrue(r['RESULT'].startswith('BLOCKED'))
        self.assertEqual(r['failure_code'],code);self.assertEqual(r['mutation_requests'],0)
        return r
    def target(self):return self.api.data[('lovelace/config',q.TARGET)]
    def test_exclusive_existing_hioc_target_passes(self):
        r=self.run_api();self.assertTrue(r['RESULT'].startswith('PASS'))
        self.assertEqual(r['target_dashboard'],'hioc-dashboard-v2')
        self.assertEqual(r['target_policy'],'EXCLUSIVE_EXISTING_HIOC_INTERFACE_NO_ALTERNATIVE_DASHBOARD')
        self.assertEqual(len(r['preserved_view_paths']),6)
        self.assertNotIn('compatible_choices',r);self.assertNotIn('preferred_existing_hioc',r)
        self.assertFalse(r['native_delivery_ready'])
    def test_six_registered_dashboards_only_hioc_config_read(self):
        for i in range(5):self.api.data['lovelace/dashboards/list'].append({'url_path':'other-'+str(i),'title':SECRET,'mode':'yaml' if i%2 else 'storage'})
        r=self.run_api();self.assertTrue(r['RESULT'].startswith('PASS'))
        self.assertEqual(r['catalog_count'],6)
        self.assertEqual(self.api.selectors,[q.TARGET,None])
        self.assertNotIn(SECRET,json.dumps(r));self.assertEqual(r['unrelated_dashboard_configs_read'],0)
    def test_compatibility_panel_without_config_is_not_resource_source(self):
        self.api.data['get_panels']={'lovelace':{'component_name':'lovelace','config':None}}
        r=self.run_api();self.assertTrue(r['RESULT'].startswith('PASS'))
        self.assertNotIn('get_panels',self.api.calls)
    def test_missing_panel_does_not_defeat_actual_source_proof(self):
        self.api.data['get_panels']={}
        self.assertTrue(self.run_api()['RESULT'].startswith('PASS'))
    def test_panel_permission_not_queried(self):
        self.api.fail['get_panels']=RuntimeError(SECRET)
        self.assertTrue(self.run_api()['RESULT'].startswith('PASS'))
    def test_no_private_payload_in_receipt(self):
        self.target()['views'][0]['cards']=[{'type':'markdown','content':SECRET,'entity':'sensor.private'}]
        r=self.run_api();raw=json.dumps(r)
        for text in (SECRET,'synthetic-admin','credentials','markdown','sensor.private'):self.assertNotIn(text,raw)
    def test_missing_admin(self):
        self.api.data['auth/current_user']['is_admin']=False
        self.blocked('AUTHENTICATED_ADMIN_REQUIRED');self.assertEqual(len(self.api.calls),1)
    def test_truthy_admin_not_true(self):
        self.api.data['auth/current_user']['is_admin']=1;self.blocked('AUTHENTICATED_ADMIN_REQUIRED')
    def test_missing_principal(self):
        self.api.data['auth/current_user']['id']='';self.blocked('AUTHENTICATED_ADMIN_REQUIRED')
    def test_safe_mode_no_false_loaded_claim(self):
        self.api.data['get_config']['safe_mode']=True
        self.blocked('CORE_NORMAL_RESOURCE_VIEW_NOT_ESTABLISHED');self.assertNotIn('lovelace/resources/list',self.api.calls)
    def test_recovery_mode_blocks(self):
        self.api.data['get_config']['recovery_mode']=True;self.blocked('CORE_NORMAL_RESOURCE_VIEW_NOT_ESTABLISHED')
    def test_absent_integration_is_inactive(self):
        self.assertEqual(self.run_api()['ha_roles']['integration'],'ABSENT_INACTIVE')
    def test_present_component_blocks(self):
        self.api.data['get_config']['components'].append('hioc_operator');self.blocked('HIOC_ACTIVE_OR_CONFIGURED_ROLE_REQUIRES_EVIDENCE')
    def test_present_services_block(self):
        self.api.data['get_services']['hioc_operator']={};self.blocked('HIOC_ACTIVE_OR_CONFIGURED_ROLE_REQUIRES_EVIDENCE')
    def test_cross_host_and_trust_guards_not_fabricated(self):
        r=self.run_api()
        for key in ('disabled','exclusive_delivery','local_mapping'):self.assertFalse(r['live_guard'][key])
        self.assertTrue(r['live_guard']['resources_loaded']);self.assertTrue(r['live_guard']['storage_dashboard'])
        self.assertEqual(r['trust'],'REQUIRED_BEFORE_EXISTING_DELIVERY_PREPARE_NOT_PROVISIONED_HERE')
        self.assertFalse(r['backup']['created'])
    def test_missing_fixed_target_no_fallback(self):
        self.api.data['lovelace/dashboards/list']=[{'url_path':'alternative-hioc','title':'HIOC Dashboard v2','mode':'storage'}]
        self.blocked('EXCLUSIVE_HIOC_DASHBOARD_NOT_UNIQUELY_ESTABLISHED')
        self.assertEqual(self.api.selectors,[])
    def test_duplicate_target_refused(self):
        self.api.data['lovelace/dashboards/list']*=2
        self.blocked('EXCLUSIVE_HIOC_DASHBOARD_NOT_UNIQUELY_ESTABLISHED')
    def test_target_yaml_no_mode_migration(self):
        self.api.data['lovelace/dashboards/list'][0]['mode']='yaml'
        self.blocked('EXCLUSIVE_HIOC_DASHBOARD_NOT_STORAGE_NO_MIGRATION');self.assertEqual(self.api.selectors,[])
    def test_resource_yaml_no_mutation(self):
        self.api.data['lovelace/info']['resource_mode']='yaml'
        self.blocked('RESOURCE_STORAGE_MODE_REQUIRED_NO_MODE_CHANGE');self.assertNotIn('lovelace/resources/list',self.api.calls)
    def test_target_title_not_identity(self):
        self.api.data['lovelace/dashboards/list'][0]['title']=SECRET
        r=self.run_api();self.assertTrue(r['RESULT'].startswith('PASS'));self.assertNotIn(SECRET,json.dumps(r))
    def test_unknown_catalog_rows_block_resources(self):
        self.api.data['lovelace/dashboards/list'].append(SECRET)
        r=self.blocked('CATALOG_INCOMPLETE_RESOURCE_SAFETY_NOT_ESTABLISHED')
        self.assertEqual(len(r['preserved_view_paths']),6);self.assertNotIn(SECRET,json.dumps(r))
        self.assertNotIn('lovelace/resources/list',self.api.calls)
    def test_excessive_catalog_bound_remains(self):
        self.api.data['lovelace/dashboards/list']*=17
        self.blocked('CATALOG_INCOMPLETE_RESOURCE_SAFETY_NOT_ESTABLISHED')
    def test_shadowed_legacy_source_stays_blocked_even_storage(self):
        for mode in ('yaml','storage'):
            self.api=API();self.api.data['lovelace/dashboards/list'].append({'url_path':'lovelace','title':SECRET,'mode':mode})
            self.blocked('RESOURCE_LAZY_IMPORT_SAFETY_NOT_ESTABLISHED')
            self.assertEqual(self.api.selectors,[q.TARGET]);self.assertNotIn('lovelace/resources/list',self.api.calls)
    def test_legacy_resources_key_never_imported(self):
        for value in ([],None,[{'url':SECRET,'type':'module'}]):
            self.api=API();self.api.data[('lovelace/config',None)]={'resources':value}
            r=self.blocked('RESOURCE_LAZY_IMPORT_SAFETY_NOT_ESTABLISHED')
            self.assertTrue(r['legacy_import_probe']['legacy_resources_present'])
            self.assertNotIn('lovelace/resources/list',self.api.calls);self.assertNotIn(SECRET,json.dumps(r))
    def test_actual_default_config_without_views_is_not_UI_target(self):
        self.api.data[('lovelace/config',None)]={'strategy':{'private':SECRET}}
        r=self.run_api();self.assertTrue(r['RESULT'].startswith('PASS'))
        self.assertTrue(r['legacy_import_probe']['strategy_present']);self.assertNotIn(SECRET,json.dumps(r))
        self.assertEqual(r['target_dashboard'],q.TARGET);self.assertNotIn('dashboards',r)
    def test_successful_null_default_not_absence(self):
        self.api.data[('lovelace/config',None)]=None
        r=self.blocked('RESOURCE_LAZY_IMPORT_SAFETY_NOT_ESTABLISHED')
        self.assertEqual(r['legacy_import_probe']['response_type'],'null');self.assertNotIn('lovelace/resources/list',self.api.calls)
    def test_default_unexpected_types_block(self):
        for value in (SECRET,[],True,3):
            self.api=API();self.api.data[('lovelace/config',None)]=value
            r=self.blocked('RESOURCE_LAZY_IMPORT_SAFETY_NOT_ESTABLISHED');self.assertNotIn(SECRET,json.dumps(r))
    def test_default_config_not_found_safe_no_legacy_import(self):
        original=self.api.call
        def call(kind,**fields):
            if kind=='lovelace/config' and fields.get('url_path') is None:
                self.api.calls.append(kind);self.api.selectors.append(None);raise q.Stop('CONFIG_NOT_FOUND')
            return original(kind,**fields)
        self.api.call=call;r=self.run_api();self.assertTrue(r['RESULT'].startswith('PASS'))
        self.assertEqual(r['legacy_import_probe']['error_code'],'CONFIG_NOT_FOUND')
    def test_resource_conflict_no_query_disclosure(self):
        self.api.data['lovelace/resources/list']=[{'url':'/local/hioc-asset-editor.js?token='+SECRET,'type':'module'}]
        r=self.blocked('EXISTING_HIOC_RESOURCE_CONFLICT');self.assertNotIn(SECRET,json.dumps(r))
    def test_encoded_editor_conflict(self):
        self.api.data['lovelace/resources/list']=[{'url':'/local/%68ioc-asset-editor.js','type':'module'}]
        self.blocked('EXISTING_HIOC_RESOURCE_CONFLICT')
    def test_unrelated_resource_preserved_redacted(self):
        self.api.data['lovelace/resources/list']=[{'url':'https://example.invalid/card.js?key='+SECRET,'type':'module'}]
        r=self.run_api();self.assertEqual(r['resources']['count'],1);self.assertNotIn(SECRET,json.dumps(r))
        self.assertEqual(r['resources']['items'],[]);self.assertEqual(r['resources']['reported_scope'],'HIOC_EDITOR_CONFLICTS_ONLY')
    def test_resource_schema_and_limit_remain(self):
        for value in ({SECRET:SECRET},[{}]*257,[{}]):
            self.api=API();self.api.data['lovelace/resources/list']=value
            r=self.run_api();self.assertTrue(r['RESULT'].startswith('BLOCKED'));self.assertNotIn(SECRET,json.dumps(r))
    def test_existing_editor_card_blocks_not_duplicated(self):
        self.target()['views'][0]['cards']=[{'type':'custom:hioc-asset-editor'}]
        self.blocked('EXISTING_HIOC_EDITOR_CARD_CONFLICT');self.assertNotIn('lovelace/resources/list',self.api.calls)
    def test_six_views_preserved_no_target_view_selected(self):
        before=copy.deepcopy(self.target());r=self.run_api()
        self.assertEqual(before,self.target());self.assertEqual(r['preserved_view_paths'],[v['path'] for v in before['views']])
        self.assertEqual(r['view_placement'],'NO_VIEW_SELECTED_OR_LAYOUT_CHANGE_AUTHORIZED')
    def test_view_count_drift_no_rebuild(self):
        self.target()['views'].append({'path':'extra','cards':[]})
        self.blocked('EXISTING_SIX_HIOC_VIEWS_NOT_ESTABLISHED')
    def test_duplicate_or_missing_paths_refused(self):
        self.target()['views'][1]['path']=self.target()['views'][0]['path']
        self.blocked('EXISTING_HIOC_VIEW_PATHS_NOT_ESTABLISHED')
    def test_sections_and_masonry_supported(self):
        self.target()['views'][0].update(type='sections',sections=[])
        self.assertTrue(self.run_api()['RESULT'].startswith('PASS'))
    def test_no_additive_view_keeps_six_but_does_not_modify(self):
        for v in self.target()['views']:v['panel']=True
        self.blocked('NO_COMPATIBLE_HIOC_STATIC_VIEW')
    def test_generated_views_do_not_become_static(self):
        for v in self.target()['views']:v['strategy']={'type':'original-states'}
        self.blocked('NO_COMPATIBLE_HIOC_STATIC_VIEW')
    def test_optional_cards_not_filled(self):
        for v in self.target()['views']:del v['cards']
        self.blocked('NO_COMPATIBLE_HIOC_STATIC_VIEW')
    def test_strategy_target_diagnosed_no_fallback(self):
        self.api.data[('lovelace/config',q.TARGET)]={'strategy':{'private':SECRET}}
        r=self.blocked('EXCLUSIVE_HIOC_STATIC_VIEWS_NOT_ESTABLISHED');self.assertNotIn(SECRET,json.dumps(r))
        self.assertEqual(r['hioc_dashboard']['discovery_status'],'STRATEGY_DECLARED_NOT_STATIC')
    def test_missing_nonlist_and_unexpected_target_shapes(self):
        for value in ({},{'views':None},{'views':SECRET},None,[],SECRET):
            self.api=API();self.api.data[('lovelace/config',q.TARGET)]=value
            r=self.blocked('EXCLUSIVE_HIOC_STATIC_VIEWS_NOT_ESTABLISHED')
            self.assertIn('response_shape',r['hioc_dashboard']);self.assertNotIn(SECRET,json.dumps(r))
    def test_oversized_target_not_assumed_malformed(self):
        self.target()['views']*=q.MAX_VIEWS+1
        r=self.blocked('EXCLUSIVE_HIOC_STATIC_VIEWS_NOT_ESTABLISHED')
        self.assertEqual(r['hioc_dashboard']['discovery_status'],'LOCAL_VIEW_BUDGET_EXCEEDED')
    def test_shape_parser_still_supports33_without_global_schema_error(self):
        raw={'views':[{'path':'v'+str(i),'cards':[]} for i in range(33)]}
        r=q.views(raw);self.assertEqual(r['discovery_status'],'STATIC_VIEWS_OBSERVED');self.assertEqual(len(r['views']),33)
    def test_unreportable_label_does_not_leak(self):
        self.target()['views'][0]['title']={'private':SECRET}
        r=self.run_api();self.assertIsNone(r['hioc_dashboard']['views'][0]['title']);self.assertNotIn(SECRET,json.dumps(r))
    def test_unknown_resource_mode_not_echoed(self):
        self.api.data['lovelace/info']['resource_mode']={SECRET:SECRET}
        r=self.blocked('RESOURCE_MODE_UNKNOWN');self.assertNotIn(SECRET,json.dumps(r))
    def test_each_used_read_failure_stops_sanitized(self):
        for command in q.READS-{'get_panels'}:
            self.api=API();self.api.fail[command]=OSError(SECRET)
            r=self.blocked('READ_OR_SCHEMA_FAILURE');self.assertNotIn(SECRET,json.dumps(r))
    def test_no_mutation_commands_sent(self):
        before=copy.deepcopy(self.api.data);self.run_api();self.assertEqual(before,self.api.data)
        self.assertLessEqual(set(self.api.calls),q.READS)
        self.assertEqual(self.api.selectors,[q.TARGET,None])


class RunTests(unittest.TestCase):
    def test_no_existing_token_no_socket_or_credential_search(self):
        with patch.dict(q.os.environ,{},clear=True),patch.object(q,'Proxy') as proxy:
            r=q.run();proxy.assert_not_called()
        self.assertEqual(r['RESULT'],'BLOCKED_EXISTING_AUTHENTICATION_UNAVAILABLE')
        self.assertEqual(r['operator_workflow'],q.LOGIN_WORKFLOW)
    def test_existing_token_only_passed_to_normal_authentication(self):
        api=API();api.connect=lambda token:self.assertEqual(token,SECRET);api.close=lambda:None
        with patch.dict(q.os.environ,{'SUPERVISOR_TOKEN':SECRET},clear=True),patch.object(q,'Proxy',return_value=api):r=q.run()
        self.assertTrue(r['RESULT'].startswith('PASS'));self.assertNotIn(SECRET,json.dumps(r))
    def test_denied_proxy_never_uses_fallback_credentials(self):
        api=API();api.connect=lambda token:(_ for _ in ()).throw(q.Stop('EXISTING_AUTHENTICATION_DENIED'));api.close=lambda:None
        with patch.dict(q.os.environ,{'SUPERVISOR_TOKEN':SECRET},clear=True),patch.object(q,'Proxy',return_value=api):r=q.run()
        self.assertEqual(r['failure_code'],'EXISTING_AUTHENTICATION_DENIED')
        self.assertEqual(api.calls,[])
    def test_private_transport_error_sanitized(self):
        api=API();api.connect=lambda token:(_ for _ in ()).throw(OSError(SECRET));api.close=lambda:None
        with patch.dict(q.os.environ,{'SUPERVISOR_TOKEN':SECRET},clear=True),patch.object(q,'Proxy',return_value=api):r=q.run()
        self.assertNotIn(SECRET,json.dumps(r))
    def test_close_uncertainty_cannot_pass(self):
        api=API();api.connect=lambda token:None;api.close=lambda:(_ for _ in ()).throw(OSError(SECRET))
        with patch.dict(q.os.environ,{'SUPERVISOR_TOKEN':SECRET},clear=True),patch.object(q,'Proxy',return_value=api):r=q.run()
        self.assertEqual(r['RESULT'],'BLOCKED_CONNECTION_CLEANUP')
        self.assertEqual(r['primary_result_before_close'],'PASS_READ_ONLY_API_DASHBOARD_DISCOVERY')
        self.assertNotIn(SECRET,json.dumps(r))


def frame(value,opcode=1,fin=True):
    raw=value if isinstance(value,bytes) else q.canonical(value)
    n=len(raw);header=bytes(((128 if fin else 0)|opcode,n if n<126 else 126))
    if n>=126:header+=struct.pack('!H',n)
    return header+raw


class Sock:
    def __init__(self,raw=b'',peer='172.30.32.2'):
        self.raw=raw;self.sent=[];self.closed=0;self.peer=peer
    def recv(self,size):result,self.raw=self.raw[:size],self.raw[size:];return result
    def settimeout(self,value):pass
    def getpeername(self):return self.peer,80
    def sendall(self,raw):self.sent.append(raw)
    def close(self):self.closed+=1


class TransportTests(unittest.TestCase):
    def proxy(self,raw=b''):
        p=q.Proxy();p.sock=Sock(raw);p.authenticated=True;return p
    def test_approved_reads_only(self):
        p=self.proxy(frame({'id':1,'type':'result','success':True,'result':{}}))
        self.assertEqual(p.call('get_config'),{})
        with self.assertRaises(q.Stop):p.call('call_service',domain='hioc_operator')
        self.assertEqual(p.counter,1)
    def test_mutations_refused_before_send(self):
        p=self.proxy()
        for op in ('lovelace/config/save','lovelace/resources/create','lovelace/dashboards/create','call_service'):
            with self.assertRaises(q.Stop):p.call(op)
        self.assertEqual(p.sock.sent,[])
    def test_arguments_cannot_smuggle_action(self):
        p=self.proxy()
        for kind,fields in [('get_config',{'action':'write'}),('lovelace/config',{'url_path':'../../secrets'}),('lovelace/config',{})]:
            with self.assertRaises(q.Stop):p.call(kind,**fields)
        self.assertEqual(p.sock.sent,[])
    def test_response_id_bound(self):
        p=self.proxy(frame({'id':2,'type':'result','success':True,'result':{}}))
        with self.assertRaisesRegex(q.Stop,'RESPONSE_CONTEXT_MISMATCH'):p.call('get_config')
    def test_error_message_never_returned(self):
        p=self.proxy(frame({'id':1,'type':'result','success':False,'error':{'code':'unauthorized','message':SECRET}}))
        with self.assertRaisesRegex(q.Stop,'READ_UNAUTHORIZED_OR_UNSUPPORTED'):p.call('get_config')
    def test_fragmented_json_supported(self):
        p=self.proxy(frame(b'{"a":',fin=False)+frame(b'1}',opcode=0))
        self.assertEqual(p._receive(),{'a':1})
    def test_ping_only_protocol_pong(self):
        p=self.proxy(frame(b'ping',opcode=9)+frame({'a':1}))
        self.assertEqual(p._receive(),{'a':1});self.assertEqual(p.sock.sent[0][0],0x8a)
    def test_binary_frame_refused(self):
        with self.assertRaises(q.Stop):self.proxy(frame(b'data',opcode=2))._receive()
    def test_server_mask_refused(self):
        with self.assertRaises(q.Stop):self.proxy(b'\x81\x80')._receive()
    def test_oversized_frame_refused_before_payload(self):
        with self.assertRaisesRegex(q.Stop,'MESSAGE_LIMIT'):self.proxy(b'\x81\x7f'+struct.pack('!Q',q.MAX_MESSAGE+1))._receive()
    def test_read_budget(self):
        p=self.proxy();p.counter=64
        with self.assertRaisesRegex(q.Stop,'READ_BUDGET'):p.call('get_config')
    def test_deadline(self):
        p=self.proxy();p.deadline=0
        with self.assertRaisesRegex(q.Stop,'READ_BUDGET'):p.call('get_config')
    def test_duplicate_json_keys(self):
        with self.assertRaisesRegex(q.Stop,'DUPLICATE_JSON_KEY'):q.decode(b'{"a":1,"a":2}')
    def test_nonfinite_json(self):
        with self.assertRaisesRegex(q.Stop,'NONFINITE_JSON'):q.decode(b'{"a":NaN}')
    def test_json_depth(self):
        with self.assertRaisesRegex(q.Stop,'JSON_DEPTH_LIMIT'):q.decode(b'['*34+b'0'+b']'*34)
    def test_masked_client_frame(self):
        p=self.proxy();p._frame(1,b'abc');raw=p.sock.sent[0]
        self.assertEqual(raw[1],0x83);mask=raw[2:6]
        self.assertEqual(bytes(v^mask[i%4] for i,v in enumerate(raw[6:])),b'abc')
    def test_normal_supported_proxy_authentication(self):
        key=base64.b64encode(b'x'*16).decode()
        accept=base64.b64encode(hashlib.sha1((key+'258EAFA5-E914-47DA-95CA-C5AB0DC85B11').encode()).digest()).decode()
        raw=('HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: '+accept+'\r\n\r\n').encode()
        s=Sock(raw+frame({'type':'auth_required'})+frame({'type':'auth_ok'}))
        p=q.Proxy()
        with patch.object(q.socket,'create_connection',return_value=s) as connect,patch.object(q.os,'urandom',side_effect=lambda n:b'x'*n):p.connect(SECRET)
        connect.assert_called_once_with(('supervisor',80),timeout=10)
        self.assertTrue(p.authenticated);self.assertNotIn(SECRET.encode(),s.sent[0])
        raw=s.sent[1];mask=raw[2:6];message=bytes(v^mask[i%4] for i,v in enumerate(raw[6:]))
        self.assertEqual(json.loads(message),{'type':'auth','access_token':SECRET})
        p.close();self.assertEqual(s.closed,1)
    def test_wrong_proxy_peer_refused_before_credentials(self):
        s=Sock(peer='192.0.2.1');p=q.Proxy()
        with patch.object(q.socket,'create_connection',return_value=s):
            with self.assertRaisesRegex(q.Stop,'SUPERVISOR_ENDPOINT_NOT_ESTABLISHED'):p.connect(SECRET)
        self.assertEqual(s.sent,[]);self.assertEqual(s.closed,1)
    def test_http_denial_no_credential_frame(self):
        s=Sock(b'HTTP/1.1 403 Forbidden\r\n\r\n');p=q.Proxy()
        with patch.object(q.socket,'create_connection',return_value=s):
            with self.assertRaisesRegex(q.Stop,'PROXY_PERMISSION_OR_PROTOCOL_UNAVAILABLE'):p.connect(SECRET)
        self.assertEqual(len(s.sent),1);self.assertNotIn(SECRET.encode(),s.sent[0])
    def test_no_files_or_HA_imports_and_no_mutation_capability(self):
        tree=ast.parse(SOURCE.read_bytes());imports=set();calls=set()
        for n in ast.walk(tree):
            if isinstance(n,ast.Import):imports.update(x.name for x in n.names)
            if isinstance(n,ast.ImportFrom):imports.add(n.module)
            if isinstance(n,ast.Call):calls.add(n.func.attr if isinstance(n.func,ast.Attribute) else n.func.id if isinstance(n.func,ast.Name) else '')
        self.assertFalse(imports & {'subprocess','pathlib','hioc','homeassistant','requests'})
        self.assertFalse(calls & {'open','write','mkdir','chmod','chown','replace','unlink','system','exec','eval'})
        self.assertEqual(q.READS,{'auth/current_user','get_config','get_services','get_panels','lovelace/info','lovelace/dashboards/list','lovelace/config','lovelace/resources/list'})


if __name__=='__main__':unittest.main()
