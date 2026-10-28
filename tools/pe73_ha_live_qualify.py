"""Bounded PE-7.3 API qualification; no filesystem discovery or mutation API.

Uses only an already-present app credential and HA's documented Supervisor proxy.
Credentials travel only in its normal internal authentication handshake, never in
arguments, files, reports, source-download requests, exceptions or HIOC requests.
No token creation, app-permission changes, HA import, .storage access or services.
"""
import base64
import hashlib
import json
import os
import re
import socket
import struct
import time
from urllib.parse import unquote, urlsplit

READS=frozenset(('auth/current_user','get_config','get_services','get_panels',
    'lovelace/info','lovelace/dashboards/list','lovelace/config','lovelace/resources/list'))
MAX_MESSAGE=2097152
MAX_DASHBOARDS=16
MAX_RESOURCES=256
MAX_VIEWS=256  # Local bounded discovery budget, not an HA schema constraint.
EDITOR='/local/hioc-asset-editor.js'
LOGIN_WORKFLOW='USE_EXISTING_HA_BROWSER_LOGIN_AS_ADMIN_NO_TOKEN_EXPORT_OR_NEW_CREDENTIAL'


class Stop(ValueError):
    pass


def require(condition,code):
    if not condition:raise Stop(code)


def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def public_text(value):
    require(type(value) is str and len(value)<=128 and all(ord(c)>=32 and ord(c)!=127 for c in value),'UNSUPPORTED_SELECTION_LABEL')
    return value


def label(value):
    return value if type(value) is str and len(value)<=128 and all(32<=ord(c)!=127 for c in value) else None


def json_type(value):
    return {dict:'object',list:'array',str:'string',int:'number',float:'number',bool:'boolean',type(None):'null'}.get(type(value),'unsupported')


def shape(value):
    """Fixed field names and counts only; never arbitrary keys or payload values."""
    result={'response_type':json_type(value)}
    if type(value) is dict:
        result.update(key_count=len(value),views_present='views' in value,
            views_type=json_type(value['views']) if 'views' in value else 'absent',
            view_count=len(value['views']) if type(value.get('views')) is list else None,
            strategy_present='strategy' in value,
            strategy_type=json_type(value['strategy']) if 'strategy' in value else 'absent',
            legacy_resources_present='resources' in value)
    elif type(value) in (list,str):result['item_count' if type(value) is list else 'character_count']=len(value)
    return result


def decode(raw):
    def pairs(items):
        result={}
        for key,value in items:
            require(key not in result,'DUPLICATE_JSON_KEY');result[key]=value
        return result
    def invalid(value):raise Stop('NONFINITE_JSON')
    require(len(raw)<=MAX_MESSAGE,'MESSAGE_LIMIT')
    value=json.loads(raw,object_pairs_hook=pairs,parse_constant=invalid)
    def depth(node,level=0):
        require(level<=32,'JSON_DEPTH_LIMIT')
        if isinstance(node,dict):
            for child in node.values():depth(child,level+1)
        elif isinstance(node,list):
            for child in node:depth(child,level+1)
    depth(value);return value


class Proxy:
    """Single stdlib WebSocket to fixed internal Supervisor endpoint; no retries."""
    def __init__(self):
        self.sock=None;self.counter=0;self.deadline=time.monotonic()+90
        self.authenticated=False;self.calls=[]

    def _exact(self,size):
        value=bytearray()
        while len(value)<size:
            require(time.monotonic()<self.deadline,'TOTAL_DEADLINE')
            self.sock.settimeout(min(10,max(0.01,self.deadline-time.monotonic())))
            piece=self.sock.recv(size-len(value));require(bool(piece),'CONNECTION_CLOSED');value.extend(piece)
        return bytes(value)

    def _frame(self,opcode,data):
        require(len(data)<=MAX_MESSAGE,'MESSAGE_LIMIT')
        mask=os.urandom(4);size=len(data)
        header=bytes((0x80|opcode,0x80|min(size,126)))
        if size>=126:
            header=bytes((0x80|opcode,0x80|126))+struct.pack('!H',size) if size<=65535 else bytes((0x80|opcode,0x80|127))+struct.pack('!Q',size)
        self.sock.sendall(header+mask+bytes(v^mask[i%4] for i,v in enumerate(data)))

    def _receive(self):
        chunks=bytearray();started=False
        for _ in range(64):
            first,second=self._exact(2);fin=bool(first&128);opcode=first&15
            require(not first&0x70 and not second&128,'UNSUPPORTED_WS_FRAME')
            size=second&127
            if size==126:size=struct.unpack('!H',self._exact(2))[0]
            elif size==127:size=struct.unpack('!Q',self._exact(8))[0]
            require(size<=MAX_MESSAGE and len(chunks)+size<=MAX_MESSAGE,'MESSAGE_LIMIT')
            raw=self._exact(size)
            if opcode in (8,9,10):
                require(fin and size<=125,'INVALID_CONTROL_FRAME')
                if opcode==8:raise Stop('CONNECTION_CLOSED')
                if opcode==9:self._frame(10,raw)
                continue
            require(opcode==(0 if started else 1),'UNSUPPORTED_WS_FRAME')
            started=True;chunks.extend(raw)
            if fin:return decode(bytes(chunks))
        raise Stop('FRAME_LIMIT')

    def connect(self,token):
        require(type(token) is str and 1<=len(token)<=4096 and '\r' not in token and '\n' not in token,'EXISTING_AUTHENTICATION_UNAVAILABLE')
        try:
            self.sock=socket.create_connection(('supervisor',80),timeout=10)
            require(self.sock.getpeername()[0]=='172.30.32.2','SUPERVISOR_ENDPOINT_NOT_ESTABLISHED')
            key=base64.b64encode(os.urandom(16)).decode()
            request=('GET /core/websocket HTTP/1.1\r\nHost: supervisor\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: '+key+'\r\nSec-WebSocket-Version: 13\r\n\r\n').encode()
            self.sock.sendall(request);header=bytearray()
            while not header.endswith(b'\r\n\r\n'):
                require(len(header)<8192,'HANDSHAKE_LIMIT');header.extend(self._exact(1))
            lines=header.decode('ascii').split('\r\n');require(lines[0].startswith('HTTP/1.1 101 '),'PROXY_PERMISSION_OR_PROTOCOL_UNAVAILABLE')
            headers={}
            for line in lines[1:]:
                if ':' in line:
                    k,v=line.split(':',1);require(k.lower() not in headers,'HANDSHAKE_DUPLICATE');headers[k.lower()]=v.strip()
            expected=base64.b64encode(hashlib.sha1((key+'258EAFA5-E914-47DA-95CA-C5AB0DC85B11').encode()).digest()).decode()
            require(headers.get('sec-websocket-accept')==expected and headers.get('upgrade','').lower()=='websocket'
                and 'upgrade' in headers.get('connection','').lower() and 'sec-websocket-extensions' not in headers,'HANDSHAKE_INVALID')
            hello=self._receive();require(type(hello) is dict and hello.get('type')=='auth_required','AUTH_PROTOCOL_UNAVAILABLE')
            self._frame(1,canonical({'type':'auth','access_token':token}))
            result=self._receive();require(type(result) is dict and result.get('type')=='auth_ok','EXISTING_AUTHENTICATION_DENIED')
            self.authenticated=True
        except BaseException:
            self.close();raise

    def call(self,kind,**fields):
        require(self.authenticated and kind in READS,'NON_READ_OPERATION_REFUSED')
        if kind=='lovelace/config':
            require(set(fields)=={'url_path'} and (fields['url_path'] is None or type(fields['url_path']) is str
                and bool(fields['url_path']) and label(fields['url_path']) is not None
                and all(c.isalnum() or c in '_-' for c in fields['url_path'])),'UNSAFE_DASHBOARD_SELECTOR')
        else:require(not fields,'UNEXPECTED_READ_ARGUMENTS')
        require(self.counter<64 and time.monotonic()<self.deadline,'READ_BUDGET')
        self.counter+=1;self.calls.append(kind)
        self._frame(1,canonical({'id':self.counter,'type':kind,**fields}))
        result=self._receive()
        require(type(result) is dict and result.get('id')==self.counter and result.get('type')=='result','RESPONSE_CONTEXT_MISMATCH')
        if result.get('success') is not True:
            error=result.get('error',{});code=error.get('code') if type(error) is dict else None
            raise Stop('CONFIG_NOT_FOUND' if code=='config_not_found' else 'READ_UNAUTHORIZED_OR_UNSUPPORTED')
        return result.get('result')

    def close(self):
        if self.sock is not None:
            held,self.sock=self.sock,None
            held.close()
        self.authenticated=False


def views(config):
    result={'response_shape':shape(config),'views':[], 'existing_editor_conflict':None,
        'discovery_status':'UNSUPPORTED_CONFIG_SHAPE','views_omitted':0}
    if type(config) is not dict:return result
    existing='custom:hioc-asset-editor' in canonical(config).decode()
    result['existing_editor_conflict']=existing
    if 'strategy' in config:
        result['discovery_status']='STRATEGY_DECLARED_NOT_STATIC';return result
    if type(config.get('views')) is not list:
        result['discovery_status']='VIEWS_NOT_EXPOSED_AS_LIST';return result
    if len(config['views'])>MAX_VIEWS:
        result.update(discovery_status='LOCAL_VIEW_BUDGET_EXCEEDED',views_omitted=len(config['views']));return result
    # The unchanged publisher iterates .get on every row. An unsupported row
    # prevents this dashboard being offered as a target, but not other dashboards.
    all_objects=all(type(v) is dict for v in config['views'])
    result['discovery_status']='STATIC_VIEWS_OBSERVED' if all_objects else 'UNSUPPORTED_VIEW_ROWS'
    for index,view in enumerate(config['views']):
        if type(view) is not dict:
            result['views'].append({'index':index,'response_type':json_type(view),
                'suitable_for_existing_additive_delivery':False,'reason':'VIEW_NOT_OBJECT'});continue
        path=view.get('path');kind=view.get('type','masonry')
        suitable=(all_objects and label(path) is not None and bool(path) and kind in ('masonry','sections')
            and not view.get('panel') and 'strategy' not in view
            and type(view.get('cards' if kind=='masonry' else 'sections')) is list and not existing
            and sum(v.get('path')==path for v in config['views'] if type(v) is dict)==1)
        result['views'].append({'index':index,'path':label(path),'path_type':json_type(path) if 'path' in view else 'absent',
            'title':label(view.get('title','')),'layout':kind if kind in ('masonry','sections','panel') else 'UNSUPPORTED',
            'strategy_present':'strategy' in view,'cards_type':json_type(view['cards']) if 'cards' in view else 'absent',
            'sections_type':json_type(view['sections']) if 'sections' in view else 'absent',
            'suitable_for_existing_additive_delivery':suitable})
    return result


def dashboard_config(api,item,url):
    """Keep a config-not-found observation; transport/authorization failures stop."""
    try:raw=api.call('lovelace/config',url_path=url)
    except Stop as error:
        if str(error)!='CONFIG_NOT_FOUND':raise
        item.update(discovery_status='CONFIG_NOT_FOUND_NO_STATIC_EXPORT',views=[],
            response_shape={'response_type':'not_observed','error_code':'CONFIG_NOT_FOUND'});return None,True
    item.update(views(raw));item['config_sha256']=digest(raw)
    return raw,False


def choices(report):
    report['preferred_existing_hioc']=[x['url_path'] for x in report['dashboards'] if x.get('existing_hioc')]
    report['compatible_choices']=[{'dashboard':d['url_path'],'view':v['path']} for d in report['dashboards']
        for v in d.get('views',[]) if v['suitable_for_existing_additive_delivery']]
    report['dashboard_summary']={'observed':len(report['dashboards']),
        'static_views_observed':sum(d.get('discovery_status')=='STATIC_VIEWS_OBSERVED' for d in report['dashboards']),
        'non_static_or_unqualified':sum(d.get('discovery_status')!='STATIC_VIEWS_OBSERVED' for d in report['dashboards']),
        'compatible_choices':len(report['compatible_choices'])}


def qualify(api):
    report={'RESULT':'BLOCKED_READ_ONLY_HA_QUALIFICATION','STOP_REQUIRED':True,
        'PE73':'IN_PROGRESS','PE74':'NOT_AUTHORIZED','mutation_requests':0,'native_delivery_ready':False,
        'filesystem_qualification':'ACCEPTED_OPERATOR_SUPPLIED_NOT_REPEATED',
        'authentication':{'mechanism':'EXISTING_APP_TOKEN_SUPPORTED_SUPERVISOR_CORE_PROXY',
            'human_operator_editing_authority':'NOT_ESTABLISHED_BY_PROXY_ADMIN'},
        'trust':'REQUIRED_BEFORE_EXISTING_DELIVERY_PREPARE_NOT_PROVISIONED_HERE',
        'target_selection':'OPERATOR_DECISION_REQUIRED_NO_TARGET_SELECTED',
        'backup':{'created':False,'method':'PRIVATE_FULL_API_CONFIG_AND_RESOURCES_EXPORT_BEFORE_DELIVERY_MUTATION'},
        'live_guard':{'disabled':False,'exclusive_delivery':False,'resources_loaded':False,
            'local_mapping':False,'storage_dashboard':False},
        'remaining_guard':['FRESH_CROSS_HOST_DISABLED_AND_EXCLUSIVE_DELIVERY','LIVE_LOCAL_ROUTE_MAPPING','ACTUAL_TRUST_BINDINGS']}
    try:
        user=api.call('auth/current_user')
        require(type(user) is dict and type(user.get('id')) is str and bool(user['id']) and user.get('is_admin') is True,'AUTHENTICATED_ADMIN_REQUIRED')
        report['authentication'].update(authenticated=True,is_admin=True,principal_sha256=digest(user['id']),
            active_user_check='SERVER_WS_REQUIRE_USER',scope='READ_ONLY_DELIVERY_DISCOVERY_NOT_PE7_OPERATOR_ACTOR')
        config=api.call('get_config');services=api.call('get_services')
        require(type(config) is dict and type(config.get('components')) is list and type(services) is dict,'CORE_API_SCHEMA')
        require(config.get('safe_mode') is False and config.get('recovery_mode') is False,'CORE_NORMAL_RESOURCE_VIEW_NOT_ESTABLISHED')
        absent='hioc_operator' not in config['components'] and 'hioc_operator' not in services
        report['ha_roles']={'integration':'ABSENT_INACTIVE' if absent else 'PRESENT_REQUIRES_DISABLED_ROLE_EVIDENCE',
            'editing_services_absent':'hioc_operator' not in services,
            'cross_host_evaluator_scheduler_migration_notifications':'NOT_ESTABLISHED_BY_HA_API'}
        require(absent,'HIOC_ACTIVE_OR_CONFIGURED_ROLE_REQUIRES_EVIDENCE')
        panels=api.call('get_panels');info=api.call('lovelace/info');catalog=api.call('lovelace/dashboards/list')
        report['api_shapes']={'panels':shape(panels),'lovelace_info':shape(info),'dashboard_catalog':shape(catalog)}
        require(type(panels) is dict and type(info) is dict and type(catalog) is list,'LOVELACE_SCHEMA_OR_LIMIT')
        report['resource_mode']=info.get('resource_mode') if info.get('resource_mode') in ('yaml','storage') else 'UNKNOWN'
        require(info.get('resource_mode') in ('yaml','storage'),'RESOURCE_MODE_UNKNOWN')
        report['dashboards']=[]
        report['catalog_count']=len(catalog);report['catalog_omitted']=max(0,len(catalog)-MAX_DASHBOARDS)
        complete=len(catalog)<=MAX_DASHBOARDS
        seen=set()
        for index,row in enumerate(catalog[:MAX_DASHBOARDS]):
            item={'catalog_index':index,'views':[],'response_shape':shape(row)}
            report['dashboards'].append(item)
            if type(row) is not dict or type(row.get('url_path')) is not str or row.get('mode') not in ('yaml','storage'):
                item['discovery_status']='UNSUPPORTED_CATALOG_ROW';complete=False;continue
            url=label(row['url_path']);title=label(row.get('title',''))
            if not url or not all(c.isalnum() or c in '_-' for c in url) or url in seen:
                item['discovery_status']='UNREPORTABLE_OR_DUPLICATE_SELECTOR';complete=False;continue
            seen.add(url)
            item.update(url_path=url,title=title,mode=row['mode'],existing_hioc='hioc' in (url+' '+(title or '')).lower())
            if row['mode']=='storage':
                dashboard_config(api,item,url)
            else:item['views_not_read']='YAML_PRESERVED_NO_MODE_MIGRATION_OR_DUPLICATE_DASHBOARD'
            choices(report)
        choices(report)
        report['catalog_complete']=complete
        require(info['resource_mode']=='storage','RESOURCE_STORAGE_MODE_REQUIRED_NO_MODE_CHANGE')
        # resources/list can save legacy imported resources. Never call it unless
        # the exact default storage source is addressable and has no legacy key.
        require(complete,'CATALOG_INCOMPLETE_RESOURCE_SAFETY_NOT_ESTABLISHED')
        if any(row['url_path']=='lovelace' for row in catalog):
            report['resource_read_guard']='DEFAULT_STORAGE_SOURCE_SHADOWED_BY_NAMED_LOVELACE'
            raise Stop('RESOURCE_LAZY_IMPORT_SAFETY_NOT_ESTABLISHED')
        default_panel=panels.get('lovelace',{})
        panel_config=default_panel.get('config') if type(default_panel) is dict else None
        report['default_panel_shape']=shape(default_panel)
        require(type(default_panel) is dict and default_panel.get('component_name')=='lovelace'
            and type(panel_config) is dict and panel_config.get('mode') in (None,'storage'),'DEFAULT_STORAGE_SOURCE_NOT_ESTABLISHED')
        item={'url_path':None,'title':'Default Dashboard','mode':'storage','existing_hioc':False,'views':[]}
        report['dashboards'].append(item)
        default,missing=dashboard_config(api,item,None)
        if type(default) is dict:
            item['title']=label(default.get('title','Default Dashboard'))
            item['existing_hioc']='hioc' in (item['title'] or '').lower()
        choices(report)
        # A successful null is NOT a config_not_found response or proof of absence.
        require(missing or type(default) is dict and 'resources' not in default,'RESOURCE_LAZY_IMPORT_SAFETY_NOT_ESTABLISHED')
        report['resource_read_guard']='EXACT_DEFAULT_HAS_NO_LEGACY_RESOURCE_IMPORT'
        resources=api.call('lovelace/resources/list')
        report['resource_response_shape']=shape(resources)
        require(type(resources) is list and len(resources)<=MAX_RESOURCES,'RESOURCE_SCHEMA_OR_LIMIT')
        items=[];conflicts=0
        for item in resources:
            require(type(item) is dict and type(item.get('url')) is str and type(item.get('type')) is str,'RESOURCE_SCHEMA')
            parsed=urlsplit(item['url']);path=unquote(parsed.path)
            conflict=(path==EDITOR or path.lower().endswith('/hioc-asset-editor.js'))
            conflicts+=int(conflict)
            items.append({'identity_sha256':digest(item),'type':item['type'] if item['type'] in ('js','module','css') else 'OTHER','hioc_editor_conflict':conflict})
        report['resources']={'count':len(items),'items':items,'sha256':digest(resources),'hioc_conflicts':conflicts}
        report['live_guard']['resources_loaded']=True
        require(not conflicts,'EXISTING_HIOC_RESOURCE_CONFLICT')
        report['local_mapping']={'source_capability':'ACCEPTED_WWW_TO_LOCAL_IMPLEMENTATION',
            'actual_route':'NOT_PROVEN_BY_ABSENT_EDITOR_OR_404','required_resource_url':EDITOR}
        require(bool(report['compatible_choices']),'NO_COMPATIBLE_STORAGE_VIEW')
        report['live_guard']['storage_dashboard']=True
        report['RESULT']='PASS_READ_ONLY_API_DASHBOARD_DISCOVERY'
    except BaseException as error:
        report['failure_code']=str(error) if type(error) is Stop else 'READ_OR_SCHEMA_FAILURE'
    report['read_commands']=list(api.calls)
    return report


def run():
    token=os.environ.get('SUPERVISOR_TOKEN')
    if not token:
        return {'RESULT':'BLOCKED_EXISTING_AUTHENTICATION_UNAVAILABLE','operator_workflow':LOGIN_WORKFLOW,
            'credential_creation_or_extraction':False,'filesystem_rechecked':False,'mutation_requests':0,
            'PE73':'IN_PROGRESS','PE74':'NOT_AUTHORIZED','STOP_REQUIRED':True}
    api=Proxy()
    try:
        api.connect(token);token=None
        result=qualify(api)
    except BaseException as error:
        result={'RESULT':'BLOCKED_AUTHENTICATION_OR_PROXY_PERMISSION','failure_code':str(error) if type(error) is Stop else 'PROXY_UNAVAILABLE',
            'operator_workflow':LOGIN_WORKFLOW,'mutation_requests':0,'PE73':'IN_PROGRESS','PE74':'NOT_AUTHORIZED','STOP_REQUIRED':True}
    finally:
        token=None
        try:api.close()
        except BaseException:
            result['primary_result_before_close']=result['RESULT']
            result['RESULT']='BLOCKED_CONNECTION_CLEANUP'
            result['cleanup_failure']='CONNECTION_CLOSE_UNCERTAIN'
    return result


if __name__=='__main__':
    result=run()
    print(json.dumps(result,sort_keys=True,separators=(',',':')))
    raise SystemExit(0 if result['RESULT'].startswith('PASS_') else 1)
