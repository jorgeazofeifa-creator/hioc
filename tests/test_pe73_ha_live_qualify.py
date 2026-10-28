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
    return {'title':'HIOC Dashboard','views':[{'title':'Operations','path':'operations','cards':[]}]}


class API:
    def __init__(self):
        self.calls=[];self.fail={}
        self.data={'auth/current_user':{'id':'synthetic-admin','name':SECRET,'is_admin':True,'credentials':[SECRET]},
            'get_config':{'components':['lovelace'],'version':'2026.10.4','private':SECRET,'safe_mode':False,'recovery_mode':False},
            'get_services':{},'get_panels':{'lovelace':{'component_name':'lovelace','config':{'mode':'storage'}}},
            'lovelace/info':{'resource_mode':'storage'},
            'lovelace/dashboards/list':[{'url_path':'hioc','title':'HIOC Dashboard','mode':'storage'}],
            'lovelace/resources/list':[],('lovelace/config','hioc'):config(),
            ('lovelace/config',None):{'views':[]}}

    def call(self,kind,**fields):
        self.calls.append(kind)
        if kind not in q.READS:raise AssertionError('mutation')
        if kind in self.fail:raise self.fail[kind]
        key=(kind,fields.get('url_path')) if kind=='lovelace/config' else kind
        return copy.deepcopy(self.data[key])


class QualificationTests(unittest.TestCase):
    def setUp(self):self.api=API()
    def run_api(self):return q.qualify(self.api)
    def blocked(self,code):
        result=self.run_api()
        self.assertTrue(result['RESULT'].startswith('BLOCKED'))
        self.assertEqual(result['failure_code'],code)
        self.assertEqual(result['mutation_requests'],0)
        return result
    def test_valid_existing_admin_supported_reads(self):
        r=self.run_api()
        self.assertEqual(r['RESULT'],'PASS_READ_ONLY_API_DASHBOARD_DISCOVERY')
        self.assertEqual(r['preferred_existing_hioc'],['hioc'])
        self.assertEqual(r['compatible_choices'],[{'dashboard':'hioc','view':'operations'}])
        self.assertFalse(r['native_delivery_ready'])
        self.assertEqual(r['target_selection'],'OPERATOR_DECISION_REQUIRED_NO_TARGET_SELECTED')
    def test_no_private_payload_in_receipt(self):
        self.api.data[('lovelace/config','hioc')]['views'][0]['cards']=[{'type':'markdown','content':SECRET}]
        raw=json.dumps(self.run_api())
        for text in (SECRET,'synthetic-admin','credentials','markdown'):self.assertNotIn(text,raw)
    def test_missing_admin(self):
        self.api.data['auth/current_user']['is_admin']=False
        self.blocked('AUTHENTICATED_ADMIN_REQUIRED');self.assertEqual(len(self.api.calls),1)
    def test_truthy_admin_is_not_true(self):
        self.api.data['auth/current_user']['is_admin']=1
        self.blocked('AUTHENTICATED_ADMIN_REQUIRED')
    def test_missing_principal(self):
        self.api.data['auth/current_user']['id']=''
        self.blocked('AUTHENTICATED_ADMIN_REQUIRED')
    def test_unsupported_read_has_no_private_exception(self):
        self.api.fail['get_services']=RuntimeError(SECRET)
        r=self.blocked('READ_OR_SCHEMA_FAILURE');self.assertNotIn(SECRET,json.dumps(r))
    def test_api_authorization_failure_isolated(self):
        self.api.fail['get_config']=q.Stop('READ_UNAUTHORIZED_OR_UNSUPPORTED')
        self.blocked('READ_UNAUTHORIZED_OR_UNSUPPORTED')
        self.assertNotIn('get_services',self.api.calls)
    def test_absent_integration_is_inactive_not_unsafe(self):
        r=self.run_api();self.assertEqual(r['ha_roles']['integration'],'ABSENT_INACTIVE')
    def test_safe_mode_empty_resources_not_claimed_loaded(self):
        self.api.data['get_config']['safe_mode']=True
        self.blocked('CORE_NORMAL_RESOURCE_VIEW_NOT_ESTABLISHED')
        self.assertNotIn('lovelace/resources/list',self.api.calls)
    def test_recovery_mode_not_resource_qualification(self):
        self.api.data['get_config']['recovery_mode']=True
        self.blocked('CORE_NORMAL_RESOURCE_VIEW_NOT_ESTABLISHED')
    def test_present_component_does_not_infer_disabled(self):
        self.api.data['get_config']['components'].append('hioc_operator')
        self.blocked('HIOC_ACTIVE_OR_CONFIGURED_ROLE_REQUIRES_EVIDENCE')
    def test_present_services_block(self):
        self.api.data['get_services']['hioc_operator']={}
        self.blocked('HIOC_ACTIVE_OR_CONFIGURED_ROLE_REQUIRES_EVIDENCE')
    def test_cross_host_guards_not_fabricated(self):
        r=self.run_api()
        for key in ('disabled','exclusive_delivery','local_mapping'):self.assertFalse(r['live_guard'][key])
        self.assertTrue(r['live_guard']['resources_loaded'])
        self.assertEqual(r['trust'],'REQUIRED_BEFORE_EXISTING_DELIVERY_PREPARE_NOT_PROVISIONED_HERE')
        self.assertFalse(r['backup']['created'])
    def test_yaml_resource_mode_preserved(self):
        self.api.data['lovelace/info']['resource_mode']='yaml'
        self.blocked('RESOURCE_STORAGE_MODE_REQUIRED_NO_MODE_CHANGE')
        self.assertNotIn('lovelace/resources/list',self.api.calls)
    def test_yaml_dashboard_not_loaded_or_migrated(self):
        self.api.data['lovelace/dashboards/list'].append({'url_path':'yaml-hioc','title':'Old HIOC','mode':'yaml'})
        r=self.run_api();self.assertIn('views_not_read',r['dashboards'][1])
        self.assertEqual(self.api.calls.count('lovelace/config'),2)
    def test_no_compatible_view(self):
        self.api.data[('lovelace/config','hioc')]['views']=[]
        self.blocked('NO_COMPATIBLE_STORAGE_VIEW')
    def test_panel_view_is_incompatible(self):
        self.api.data[('lovelace/config','hioc')]['views'][0]['panel']=True
        self.blocked('NO_COMPATIBLE_STORAGE_VIEW')
    def test_sections_view_supported(self):
        self.api.data[('lovelace/config','hioc')]['views'][0]={'path':'sections','type':'sections','sections':[]}
        self.assertEqual(self.run_api()['RESULT'],'PASS_READ_ONLY_API_DASHBOARD_DISCOVERY')
    def test_duplicate_view_paths_not_selected(self):
        self.api.data[('lovelace/config','hioc')]['views']*=2
        self.blocked('NO_COMPATIBLE_STORAGE_VIEW')
    def test_existing_editor_not_duplicated(self):
        self.api.data[('lovelace/config','hioc')]['views'][0]['cards']=[{'type':'custom:hioc-asset-editor'}]
        self.blocked('NO_COMPATIBLE_STORAGE_VIEW')
    def test_all_choices_returned_no_silent_selection(self):
        self.api.data[('lovelace/config','hioc')]['views'].append({'path':'second','cards':[]})
        self.assertEqual(len(self.run_api()['compatible_choices']),2)
    def test_default_dashboard_supported_without_creating_duplicate(self):
        self.api.data['lovelace/dashboards/list']=[]
        self.api.data[('lovelace/config',None)]=config()
        r=self.run_api();self.assertEqual(r['compatible_choices'],[{'dashboard':None,'view':'operations'}])
    def test_legacy_resources_never_lazy_imported(self):
        self.api.data[('lovelace/config',None)]['resources']=[]
        self.blocked('RESOURCE_LAZY_IMPORT_SAFETY_NOT_ESTABLISHED')
        self.assertNotIn('lovelace/resources/list',self.api.calls)
    def test_shadowed_default_source_never_assumed(self):
        self.api.data['lovelace/dashboards/list'].append({'url_path':'lovelace','title':'Default','mode':'yaml'})
        self.blocked('RESOURCE_LAZY_IMPORT_SAFETY_NOT_ESTABLISHED')
        self.assertNotIn('lovelace/resources/list',self.api.calls)
    def test_missing_default_panel_fails_before_resource_load(self):
        self.api.data['get_panels']={}
        self.blocked('DEFAULT_STORAGE_SOURCE_NOT_ESTABLISHED')
        self.assertNotIn('lovelace/resources/list',self.api.calls)
    def test_default_no_config_is_safe_empty_import(self):
        original=self.api.call
        def call(kind,**fields):
            if kind=='lovelace/config' and fields.get('url_path') is None:
                self.api.calls.append(kind);raise q.Stop('CONFIG_NOT_FOUND')
            return original(kind,**fields)
        self.api.call=call
        self.assertTrue(self.run_api()['RESULT'].startswith('PASS'))
    def test_resource_conflict_query_not_disclosed(self):
        self.api.data['lovelace/resources/list']=[{'url':'/local/hioc-asset-editor.js?token='+SECRET,'type':'module','id':SECRET}]
        r=self.blocked('EXISTING_HIOC_RESOURCE_CONFLICT');self.assertNotIn(SECRET,json.dumps(r))
    def test_encoded_resource_conflict(self):
        self.api.data['lovelace/resources/list']=[{'url':'/local/%68ioc-asset-editor.js','type':'module'}]
        self.blocked('EXISTING_HIOC_RESOURCE_CONFLICT')
    def test_unrelated_resource_preserved_and_redacted(self):
        self.api.data['lovelace/resources/list']=[{'url':'https://example.invalid/card.js?key='+SECRET,'type':'module'}]
        r=self.run_api();self.assertEqual(r['resources']['count'],1);self.assertNotIn(SECRET,json.dumps(r))
    def test_limits_dashboards(self):
        self.api.data['lovelace/dashboards/list']*=17
        r=self.blocked('CATALOG_INCOMPLETE_RESOURCE_SAFETY_NOT_ESTABLISHED')
        self.assertEqual(r['catalog_count'],17);self.assertEqual(r['catalog_omitted'],1)
        self.assertNotIn('lovelace/resources/list',self.api.calls)
    def test_limits_resources(self):
        self.api.data['lovelace/resources/list']=[{}]*257
        self.blocked('RESOURCE_SCHEMA_OR_LIMIT')
    def test_limits_views(self):
        self.api.data[('lovelace/config','hioc')]['views']*=q.MAX_VIEWS+1
        r=self.blocked('NO_COMPATIBLE_STORAGE_VIEW')
        self.assertEqual(r['dashboards'][0]['discovery_status'],'LOCAL_VIEW_BUDGET_EXCEEDED')
        self.assertEqual(r['dashboards'][0]['response_shape']['view_count'],q.MAX_VIEWS+1)
    def test_control_characters_not_printed(self):
        self.api.data['lovelace/dashboards/list'][0]['title']='bad\x1btitle'
        r=self.run_api();self.assertIsNone(r['dashboards'][0]['title'])
        self.assertNotIn('bad\x1btitle',json.dumps(r))
    def test_every_read_has_failure_isolation(self):
        for command in q.READS:
            with self.subTest(command=command):
                self.api=API();self.api.fail[command]=OSError(SECRET)
                r=self.run_api();self.assertTrue(r['RESULT'].startswith('BLOCKED'))
                self.assertNotIn(SECRET,json.dumps(r))

    def add_valid_dashboard(self):
        self.api.data['lovelace/dashboards/list'].append({'url_path':'hioc-valid','title':'HIOC Valid','mode':'storage'})
        self.api.data[('lovelace/config','hioc-valid')]=config()
    def test_strategy_dashboard_supported_response_not_malformed(self):
        self.api.data[('lovelace/config','hioc')]={'strategy':{'type':'original-states','private':SECRET}}
        self.add_valid_dashboard();r=self.run_api()
        self.assertTrue(r['RESULT'].startswith('PASS'))
        self.assertEqual(r['dashboards'][0]['discovery_status'],'STRATEGY_DECLARED_NOT_STATIC')
        self.assertEqual(r['dashboards'][0]['response_shape']['views_type'],'absent')
        self.assertEqual(r['compatible_choices'],[{'dashboard':'hioc-valid','view':'operations'}])
        self.assertNotIn(SECRET,json.dumps(r))
    def test_missing_views_preserves_later_valid_dashboard(self):
        self.api.data[('lovelace/config','hioc')]={SECRET:SECRET}
        self.add_valid_dashboard();r=self.run_api()
        self.assertEqual(r['dashboards'][0]['response_shape'],{'response_type':'object','key_count':1,
            'views_present':False,'views_type':'absent','view_count':None,'strategy_present':False,
            'strategy_type':'absent','legacy_resources_present':False})
        self.assertEqual(r['dashboards'][1]['discovery_status'],'STATIC_VIEWS_OBSERVED')
        self.assertEqual(len(r['compatible_choices']),1);self.assertNotIn(SECRET,json.dumps(r))
    def test_unexpected_config_types_diagnosed_without_unwrapping(self):
        for value in (None,True,7,[SECRET],SECRET,'{"views":[{"path":"invented","cards":[]}]}'):
            with self.subTest(response_type=q.json_type(value)):
                self.api=API();self.api.data[('lovelace/config','hioc')]=value;self.add_valid_dashboard()
                r=self.run_api();self.assertEqual(r['dashboards'][0]['discovery_status'],'UNSUPPORTED_CONFIG_SHAPE')
                self.assertEqual(r['dashboards'][0]['response_shape']['response_type'],q.json_type(value))
                self.assertEqual(r['compatible_choices'],[{'dashboard':'hioc-valid','view':'operations'}])
                self.assertNotIn(SECRET,json.dumps(r));self.assertNotIn('invented',json.dumps(r))
    def test_non_list_views_safe_type_diagnostics(self):
        for value in (None,SECRET,{},3):
            self.api=API();self.api.data[('lovelace/config','hioc')]={'views':value};self.add_valid_dashboard()
            r=self.run_api();self.assertEqual(r['dashboards'][0]['response_shape']['views_type'],q.json_type(value))
            self.assertEqual(len(r['compatible_choices']),1);self.assertNotIn(SECRET,json.dumps(r))
    def test_33_views_are_not_an_HA_schema_error(self):
        self.api.data[('lovelace/config','hioc')]['views']=[{'path':'v'+str(i),'cards':[]} for i in range(33)]
        r=self.run_api();self.assertEqual(r['dashboards'][0]['response_shape']['view_count'],33)
        self.assertEqual(len(r['compatible_choices']),33);self.assertTrue(r['RESULT'].startswith('PASS'))
    def test_excessive_views_preserve_other_valid_dashboards(self):
        self.api.data[('lovelace/config','hioc')]['views']*=q.MAX_VIEWS+1
        self.add_valid_dashboard();r=self.run_api()
        self.assertEqual(r['dashboards'][0]['views_omitted'],q.MAX_VIEWS+1)
        self.assertEqual(len(r['compatible_choices']),1)
    def test_mixed_yaml_strategy_static_are_all_preserved(self):
        self.api.data[('lovelace/config','hioc')]={'strategy':{'type':'areas'}}
        self.api.data['lovelace/dashboards/list'].append({'url_path':'yaml-preserved','title':'YAML','mode':'yaml'})
        self.add_valid_dashboard();r=self.run_api()
        self.assertEqual(len(r['dashboards']),4)
        self.assertEqual(r['dashboards'][1]['views_not_read'],'YAML_PRESERVED_NO_MODE_MIGRATION_OR_DUPLICATE_DASHBOARD')
        self.assertEqual(r['compatible_choices'],[{'dashboard':'hioc-valid','view':'operations'}])
    def test_generated_views_never_offered_for_static_addition(self):
        self.api.data[('lovelace/config','hioc')]['views'][0]['strategy']={'type':'original-states'}
        r=self.blocked('NO_COMPATIBLE_STORAGE_VIEW')
        self.assertTrue(r['dashboards'][0]['views'][0]['strategy_present'])
    def test_top_strategy_with_static_views_not_a_static_target(self):
        self.api.data[('lovelace/config','hioc')]['strategy']={'type':'areas'}
        self.blocked('NO_COMPATIBLE_STORAGE_VIEW')
    def test_optional_path_and_cards_not_invented(self):
        self.api.data[('lovelace/config','hioc')]['views']=[{'title':'Index only'},{'path':'empty'}]
        r=self.blocked('NO_COMPATIBLE_STORAGE_VIEW')
        self.assertEqual(r['dashboards'][0]['views'][0]['path_type'],'absent')
        self.assertEqual(r['dashboards'][0]['views'][1]['cards_type'],'absent')
    def test_non_object_view_does_not_qualify_publisher_incompatible_target(self):
        self.api.data[('lovelace/config','hioc')]['views'].append(SECRET)
        self.add_valid_dashboard();r=self.run_api()
        self.assertEqual(r['dashboards'][0]['discovery_status'],'UNSUPPORTED_VIEW_ROWS')
        self.assertEqual(r['dashboards'][0]['views'][1]['reason'],'VIEW_NOT_OBJECT')
        self.assertEqual(len(r['compatible_choices']),1);self.assertNotIn(SECRET,json.dumps(r))
    def test_unreportable_optional_view_labels_do_not_abort_discovery(self):
        self.api.data[('lovelace/config','hioc')]['views'].append({'path':'x'*129,'title':{'private':SECRET},'cards':[]})
        r=self.run_api();self.assertEqual(len(r['compatible_choices']),1)
        self.assertIsNone(r['dashboards'][0]['views'][1]['path']);self.assertIsNone(r['dashboards'][0]['views'][1]['title'])
        self.assertNotIn(SECRET,json.dumps(r))
    def test_default_missing_views_still_checks_legacy_key_independently(self):
        self.api.data[('lovelace/config',None)]={'strategy':{'type':'areas'},'resources':[]}
        r=self.blocked('RESOURCE_LAZY_IMPORT_SAFETY_NOT_ESTABLISHED')
        self.assertEqual(len(r['compatible_choices']),1)
        self.assertEqual(r['dashboards'][-1]['response_shape']['legacy_resources_present'],True)
        self.assertNotIn('lovelace/resources/list',self.api.calls)
    def test_default_strategy_without_legacy_key_does_not_block_other_dashboard(self):
        self.api.data[('lovelace/config',None)]={'strategy':{'type':'areas'}}
        r=self.run_api();self.assertTrue(r['RESULT'].startswith('PASS'))
        self.assertEqual(r['dashboards'][-1]['discovery_status'],'STRATEGY_DECLARED_NOT_STATIC')
    def test_successful_null_default_is_not_config_not_found(self):
        self.api.data[('lovelace/config',None)]=None
        r=self.blocked('RESOURCE_LAZY_IMPORT_SAFETY_NOT_ESTABLISHED')
        self.assertEqual(r['dashboards'][-1]['response_shape']['response_type'],'null')
        self.assertNotIn('lovelace/resources/list',self.api.calls)
    def test_wrong_default_type_keeps_valid_choices_but_blocks_resources(self):
        self.api.data[('lovelace/config',None)]=SECRET
        r=self.blocked('RESOURCE_LAZY_IMPORT_SAFETY_NOT_ESTABLISHED')
        self.assertEqual(len(r['compatible_choices']),1);self.assertNotIn(SECRET,json.dumps(r))
    def test_named_config_not_found_does_not_discard_other_dashboards(self):
        original=self.api.call
        def call(kind,**fields):
            if kind=='lovelace/config' and fields.get('url_path')=='hioc':
                self.api.calls.append(kind);raise q.Stop('CONFIG_NOT_FOUND')
            return original(kind,**fields)
        self.api.call=call;self.add_valid_dashboard();r=self.run_api()
        self.assertEqual(r['dashboards'][0]['discovery_status'],'CONFIG_NOT_FOUND_NO_STATIC_EXPORT')
        self.assertEqual(len(r['compatible_choices']),1)
    def test_catalog_unknown_rows_keep_choices_but_block_resource_guard(self):
        self.api.data['lovelace/dashboards/list'].insert(0,SECRET)
        r=self.blocked('CATALOG_INCOMPLETE_RESOURCE_SAFETY_NOT_ESTABLISHED')
        self.assertEqual(len(r['compatible_choices']),1);self.assertFalse(r['catalog_complete'])
        self.assertNotIn(SECRET,json.dumps(r));self.assertNotIn('lovelace/resources/list',self.api.calls)
    def test_partial_discovery_not_hidden_by_later_transport_failure(self):
        self.add_valid_dashboard();original=self.api.call
        def call(kind,**fields):
            if kind=='lovelace/config' and fields.get('url_path')=='hioc-valid':
                raise OSError(SECRET)
            return original(kind,**fields)
        self.api.call=call;r=self.blocked('READ_OR_SCHEMA_FAILURE')
        self.assertEqual(r['compatible_choices'],[{'dashboard':'hioc','view':'operations'}])
        self.assertNotIn('lovelace/resources/list',self.api.calls);self.assertNotIn(SECRET,json.dumps(r))
    def test_unsupported_resource_mode_does_not_disclose_payload(self):
        self.api.data['lovelace/info']['resource_mode']={'private':SECRET}
        r=self.blocked('RESOURCE_MODE_UNKNOWN');self.assertNotIn(SECRET,json.dumps(r))
    def test_null_panel_config_fails_closed_with_public_code(self):
        self.api.data['get_panels']['lovelace']['config']=None
        self.blocked('DEFAULT_STORAGE_SOURCE_NOT_ESTABLISHED')
    def test_non_list_resource_diagnostics_do_not_disclose_payload(self):
        self.api.data['lovelace/resources/list']={SECRET:SECRET}
        r=self.blocked('RESOURCE_SCHEMA_OR_LIMIT')
        self.assertEqual(r['resource_response_shape']['response_type'],'object')
        self.assertNotIn(SECRET,json.dumps(r))


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
