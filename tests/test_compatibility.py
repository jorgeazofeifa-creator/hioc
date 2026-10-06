"""Repository-only compatibility, persistence, privacy and consumer proofs."""
import copy
import importlib.util
import json
import logging
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'pi4/lib'))
from hioc.core import compatibility as c
from hioc.core.state import StateStore
REGISTRY=c.load_registry(ROOT/'governance/compatibility-contracts.json')
DEPS={d['dependency_id']:d for d in REGISTRY['dependencies']}
STAMP='2026-10-06T12:00:00+00:00'
LATER='2026-10-06T12:01:00+00:00'


def obs(identifier,version=None,passed=True,available=True):
    return {'observed_version':version,'available':available,
            'capabilities':{name:passed for name in DEPS[identifier]['required_capabilities']}}


def assess(identifier, observation, previous=None):
    return c.assess(DEPS[identifier],observation,previous or {},STAMP)


class ClassificationTests(unittest.TestCase):
    def test_same_version_passes(self):
        self.assertEqual(assess('ha_core',obs('ha_core','2026.8.1'))['status'],'COMPATIBLE')
    def test_changed_version_passes_without_incident(self):
        r=assess('ha_core',obs('ha_core','2026.10.1'))
        self.assertEqual(r['status'],'COMPATIBLE_UPDATED');self.assertFalse(r['likely_update_compatibility_break'])
    def test_changed_version_failed_requires_known_good_for_cause(self):
        known=assess('ha_core',obs('ha_core','2026.8.1'))
        r=assess('ha_core',obs('ha_core','2026.10.1',False),known)
        self.assertTrue(r['likely_update_compatibility_break']);self.assertEqual(r['last_known_compatible_version'],'2026.8.1')
        self.assertIn('changed from 2026.8.1 to 2026.10.1',r['diagnostic'])
    def test_baseline_alone_is_not_update_cause(self):
        r=assess('ha_core',obs('ha_core','2026.10.1',False))
        self.assertFalse(r['likely_update_compatibility_break'])
    def test_same_version_failure_is_not_update(self):
        known=assess('ha_core',obs('ha_core','2026.8.1'))
        r=assess('ha_core',obs('ha_core','2026.8.1',False),known)
        self.assertEqual(r['status'],'INCOMPATIBLE');self.assertFalse(r['likely_update_compatibility_break'])
    def test_unavailable_version_does_not_block_capability(self):
        self.assertEqual(assess('ha_core',obs('ha_core'))['status'],'COMPATIBLE')
        self.assertEqual(assess('ha_core',obs('ha_core',passed=False))['status'],'INCOMPATIBLE')
    def test_unavailable_dependency_is_not_incompatible(self):
        known=assess('ha_core',obs('ha_core','2026.8.1'))
        r=assess('ha_core',obs('ha_core','2026.10.1',False,False),known)
        self.assertEqual(r['status'],'DEPENDENCY_UNAVAILABLE');self.assertFalse(r['likely_update_compatibility_break'])
    def test_missing_probe_unknown(self):
        self.assertEqual(assess('ha_core',{})['status'],'COMPATIBILITY_UNKNOWN')
    def test_optional_failure_degraded(self):
        dep=copy.deepcopy(DEPS['ha_core']);dep['optional_capabilities']=['optional']
        o=obs('ha_core');o['capabilities']['optional']=False
        self.assertEqual(c.assess(dep,o,{},STAMP)['status'],'COMPATIBILITY_DEGRADED')
    def test_trust_anchor_drift_not_adopted(self):
        o=obs('openssh_trust');o['identity_matches']=False
        self.assertEqual(assess('openssh_trust',o)['status'],'TRUST_ANCHOR_CHANGED')
        o['identity_matches']=True
        self.assertEqual(assess('openssh_trust',o)['status'],'COMPATIBLE')
    def test_frozen_dependency_version_drift(self):
        o=obs('pe4_websockets','16.2.0');o['identity_matches']=True
        self.assertEqual(assess('pe4_websockets',o)['status'],'TRUST_ANCHOR_CHANGED')
    def test_supported_python_patch_floats(self):
        r=assess('windows_python',c.python_observation('3.13.16',supported_line='3.13'))
        self.assertEqual(r['status'],'COMPATIBLE_UPDATED')
        for version,implementation in [('3.14.1','CPython'),('3.13.16','PyPy')]:
            self.assertEqual(assess('windows_python',c.python_observation(version,implementation,'3.13'))['status'],'INCOMPATIBLE')
    def test_privacy_numeric_version_only(self):
        for value in ['192.168.50.10','private-host','sensor.secret','https://secret.invalid','token-SECRET','aa:bb:cc:dd:ee:ff','x'*500]:
            self.assertIsNone(c.safe_version(value));r=assess('ha_core',obs('ha_core',value));self.assertNotIn(value,json.dumps(r))
    def test_raw_keys_and_wrong_bool_are_not_evidence(self):
        o=obs('ha_core');o['capabilities']['token']='secret'
        r=assess('ha_core',o);self.assertEqual(r['status'],'COMPATIBILITY_UNKNOWN');self.assertNotIn('secret',json.dumps(r))
    def test_subsystem_isolation(self):
        rows=[assess('ha_core',obs('ha_core',passed=False)),assess('pihole_leases',obs('pihole_leases'))]
        s=c.summarize(rows,STAMP);self.assertEqual(s['affected_components'],['PE-4 Home Assistant Association'])
    def test_os_capability_change_is_named(self):
        r=assess('iproute',obs('iproute',passed=False))
        self.assertEqual(r['status'],'INCOMPATIBLE');self.assertIn('iproute2',r['diagnostic'])


class AdapterTests(unittest.TestCase):
    def test_lease_format_empty_malformed_missing_and_partial(self):
        for statuses,expected in [(['found'],'COMPATIBLE'),(['empty'],'COMPATIBILITY_UNKNOWN'),(['malformed'],'INCOMPATIBLE'),(['partial'],'INCOMPATIBLE'),(['missing'],'DEPENDENCY_UNAVAILABLE'),(['unsupported'],'INCOMPATIBLE')]:
            self.assertEqual(assess('pihole_leases',c.lease_observation(statuses))['status'],expected)
    def test_nut_output_and_unknown_tokens(self):
        self.assertEqual(assess('nut',c.nut_observation('ups.status: OL CHRG\nups.serial: private'))['status'],'COMPATIBLE')
        self.assertEqual(assess('nut',c.nut_observation('ups.status: NEW_TOKEN'))['status'],'INCOMPATIBLE')
        self.assertEqual(assess('nut',c.nut_observation('',False))['status'],'DEPENDENCY_UNAVAILABLE')
    def test_go2rtc_schema_addition_and_type_change(self):
        self.assertEqual(assess('go2rtc',c.go2rtc_observation({'private_stream':{'new_optional':1}}))['status'],'COMPATIBLE')
        self.assertEqual(assess('go2rtc',c.go2rtc_observation([]))['status'],'INCOMPATIBLE')
    def test_local_error_does_not_blame_mqtt_contract(self):
        self.assertEqual(assess('mqtt_transport',c.mqtt_observation(ValueError('private')))['status'],'COMPATIBILITY_UNKNOWN')
        from hioc.mqtt import MqttPublishError
        r=assess('mqtt_transport',c.mqtt_observation(MqttPublishError('private','connack')))
        self.assertEqual(r['status'],'INCOMPATIBLE');self.assertEqual(r['failed_capability'],'connack')
    def test_invalid_ha_version_metadata_is_a_named_contract_failure(self):
        o=c.observation_from_ha({'result':'FAIL','compatibility':{'status':'INCOMPATIBLE','failed_capability':'version_metadata'}})
        r=assess('ha_core',o);self.assertEqual(r['status'],'INCOMPATIBLE');self.assertEqual(r['failed_capability'],'version_metadata')
    def test_unknown_ha_probe_does_not_claim_failed_capability(self):
        o=c.observation_from_ha({'result':'FAIL','compatibility':{'status':'COMPATIBILITY_UNKNOWN','failed_capability':'authentication'}})
        self.assertEqual(assess('ha_core',o)['status'],'COMPATIBILITY_UNKNOWN')
    def test_mqtt_capability_vs_unavailability(self):
        self.assertEqual(assess('mqtt_transport',obs('mqtt_transport'))['status'],'COMPATIBLE')
        self.assertEqual(assess('mqtt_transport',obs('mqtt_transport',passed=False))['status'],'INCOMPATIBLE')
        self.assertEqual(assess('mqtt_transport',obs('mqtt_transport',available=False))['status'],'DEPENDENCY_UNAVAILABLE')
    def test_isolated_interpreter_cannot_start(self):
        observations=c.isolated_runtime_observations(Path('synthetic'),runner=lambda *a,**k: (_ for _ in ()).throw(FileNotFoundError()))
        r=assess('pe4_python',observations['pe4_python']);self.assertEqual(r['status'],'DEPENDENCY_UNAVAILABLE')
    def test_isolated_abi_or_import_failure_names_runtime(self):
        responses=[types.SimpleNamespace(returncode=1,stdout='')]
        o=c.isolated_runtime_observations(Path('synthetic'),runner=lambda *a,**k:responses.pop(0))
        self.assertEqual(assess('pe4_python',o['pe4_python'])['status'],'INCOMPATIBLE')
        responses=[types.SimpleNamespace(returncode=0,stdout='{"version":"3.11.2","implementation":"cpython"}'),types.SimpleNamespace(returncode=1,stdout='')]
        o=c.isolated_runtime_observations(Path('synthetic'),runner=lambda *a,**k:responses.pop(0))
        self.assertEqual(assess('pe4_websockets',o['pe4_websockets'])['status'],'INCOMPATIBLE')
    def test_no_runtime_network_or_install_probe(self):
        calls=[]
        def runner(args,**kwargs):
            calls.append(args)
            return types.SimpleNamespace(returncode=0,stdout='{"version":"3.11.2","implementation":"cpython"}' if len(calls)==1 else '{"version":"16.1.1","api":true}')
        result=c.isolated_runtime_observations(Path('synthetic'),runner)
        self.assertEqual(assess('pe4_websockets',result['pe4_websockets'])['status'],'COMPATIBLE')
        self.assertEqual(len(calls),2);self.assertTrue(all('-I' in a and '-B' in a for a in calls))


class PersistenceTests(unittest.TestCase):
    def test_restart_known_good_first_detection_and_recovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            store=StateStore(Path(tmp));c.update_status(store,REGISTRY,{'ha_core':obs('ha_core','2026.8.1')},STAMP)
            p=c.update_status(StateStore(Path(tmp)),REGISTRY,{'ha_core':obs('ha_core','2026.10.1',False)},LATER)
            row=next(e for e in p['dependencies'] if e['dependency_id']=='ha_core')
            self.assertTrue(row['likely_update_compatibility_break']);self.assertEqual(row['first_detection_time'],LATER)
            p=c.update_status(store,REGISTRY,{'ha_core':obs('ha_core','2026.10.1',False)},'2026-10-06T12:02:00+00:00')
            row=next(e for e in p['dependencies'] if e['dependency_id']=='ha_core');self.assertEqual(row['first_detection_time'],LATER)
            p=c.update_status(store,REGISTRY,{'ha_core':obs('ha_core','2026.10.1')},'2026-10-06T12:03:00+00:00')
            row=next(e for e in p['dependencies'] if e['dependency_id']=='ha_core');self.assertEqual(row['last_known_compatible_version'],'2026.10.1');self.assertIsNone(row['first_detection_time'])
    def test_stale_probe_does_not_assert_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            store=StateStore(Path(tmp));c.update_status(store,REGISTRY,{'ha_core':obs('ha_core','2026.8.1')},STAMP)
            p=c.update_status(store,REGISTRY,{},'2026-10-09T12:00:00+00:00')
            row=next(e for e in p['dependencies'] if e['dependency_id']=='ha_core');self.assertEqual(row['status'],'COMPATIBILITY_UNKNOWN');self.assertEqual(row['last_known_compatible_version'],'2026.8.1')
    def test_atomically_replaced_private_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            store=StateStore(Path(tmp));c.update_status(store,REGISTRY,{},STAMP)
            self.assertTrue((Path(tmp)/'compatibility.json').is_file());self.assertFalse((Path(tmp)/'compatibility.json.tmp').exists())
    def test_corrupt_prior_privacy(self):
        with tempfile.TemporaryDirectory() as tmp:
            store=StateStore(Path(tmp));store.write_json('compatibility.json',{'dependencies':[{'dependency_id':'ha_core','last_known_compatible_version':'private-host','raw':'token-SECRET'}]})
            p=c.update_status(store,REGISTRY,{},STAMP);self.assertNotIn('private-host',json.dumps(p));self.assertNotIn('token-SECRET',json.dumps(p))
    def test_unknown_dependency_input_not_persisted(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=c.update_status(StateStore(Path(tmp)),REGISTRY,{'private-host':{'token':'SECRET'}},STAMP)
            self.assertNotIn('SECRET',json.dumps(p));self.assertNotIn('private-host',json.dumps(p))


class ConsumerTests(unittest.TestCase):
    def load_platform(self):
        spec=importlib.util.spec_from_file_location('platform_compat',ROOT/'pi4/bin/hioc-platform-status.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
    def test_platform_retained_compatibility_publication(self):
        m=self.load_platform();published=[]
        class MQTT:
            def __init__(self,*a,**k):pass
            def __enter__(self):return self
            def __exit__(self,*a):pass
            def publish(self,topic,payload,retain=True):published.append((topic,payload,retain))
        with tempfile.TemporaryDirectory() as tmp,patch.object(m,'load_config',return_value={'HIOC_HOME':tmp}),patch.object(m,'MqttClient',MQTT),patch.object(m,'setup_logger',return_value=logging.getLogger('compat-test')):
            Path(tmp,'VERSION.yaml').write_bytes((ROOT/'VERSION.yaml').read_bytes())
            self.assertEqual(m.main(),0)
            self.assertTrue(any(topic.endswith('/platform/compatibility') and retained for topic,payload,retained in published))
            state=json.loads(Path(tmp,'state/platform/status.json').read_text());self.assertIn('compatibility',state)
    def test_mqtt_failure_keeps_local_state(self):
        m=self.load_platform()
        class MQTT:
            def __init__(self,*a,**k):pass
            def __enter__(self):raise ConnectionRefusedError('secret-host')
            def __exit__(self,*a):pass
        with tempfile.TemporaryDirectory() as tmp,patch.object(m,'load_config',return_value={'HIOC_HOME':tmp}),patch.object(m,'MqttClient',MQTT),patch.object(m,'setup_logger',return_value=logging.getLogger('compat-test')):
            Path(tmp,'VERSION.yaml').write_bytes((ROOT/'VERSION.yaml').read_bytes());self.assertEqual(m.main(),0)
            text=Path(tmp,'state/platform/compatibility.json').read_text();self.assertNotIn('secret-host',text)
            row=next(e for e in json.loads(text)['dependencies'] if e['dependency_id']=='mqtt_transport');self.assertEqual(row['status'],'DEPENDENCY_UNAVAILABLE')
    def test_framework_failure_does_not_break_platform_telemetry(self):
        m=self.load_platform()
        class MQTT:
            def __init__(self,*a,**k):pass
            def __enter__(self):raise ConnectionRefusedError('private-address')
            def __exit__(self,*a):pass
        with tempfile.TemporaryDirectory() as tmp,patch.object(m,'load_config',return_value={'HIOC_HOME':tmp}),patch.object(m,'MqttClient',MQTT),patch.object(m,'refresh_status',side_effect=ValueError('private-token')),patch.object(m,'setup_logger',return_value=logging.getLogger('compat-test')):
            Path(tmp,'VERSION.yaml').write_bytes((ROOT/'VERSION.yaml').read_bytes())
            self.assertEqual(m.main(),0)
            state=json.loads(Path(tmp,'state/platform/status.json').read_text())
            self.assertEqual(state['status'],'degraded')
            self.assertNotIn('private-token',json.dumps(state))
            self.assertTrue(Path(tmp,'state/platform/version.json').exists())
    def test_ha_package_stable_topic_and_install_copy(self):
        text=(ROOT/'homeassistant/packages/hioc_platform.yaml').read_text()
        self.assertIn('home/infrastructure/hioc/platform/compatibility',text)
        self.assertIn('COMPATIBILITY_UNKNOWN',text)
        installer=(ROOT/'pi4/install_pi4.sh').read_text();self.assertNotIn("--exclude '/governance/'",installer);self.assertNotIn("--exclude '/pi4/lib/'",installer)
    def test_registry_records_complete_and_classified(self):
        required={'dependency_id','display_name','dependency_class','owner_system','used_by_components','version_discovery_method','version_role','required_capabilities','compatibility_probe','schema_protocol_expectations','security_provenance_requirements','failure_isolation','operator_remediation','automatic_continuation_after_version_drift','changed_version_alone_can_fail','compatibility_baseline'}
        self.assertEqual(len(DEPS),42)
        for d in DEPS.values():self.assertTrue(required<=set(d));self.assertIn(d['dependency_class'],{'A','B','C','D','E'})
    def test_correction_framework_binds_canonical_source(self):
        import hashlib
        record=json.loads((ROOT/'governance/pe4/pe4-0b2b-compatibility-correction.json').read_text())
        self.assertEqual(record['framework_binding_basis'],'CANONICAL_GIT_LF_BYTES_EXACT_ON_LINUX_RELEASE_SOURCE')
        for name,digest in record['framework_bindings'].items():
            self.assertEqual(hashlib.sha256((ROOT/name).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),digest)
    def test_historical_records_unchanged(self):
        for path in ['governance/pe4/pe4-0b2b-discovery-preparation.json','governance/pe4/pe4-0b2a-execution-closure.json','tools/hioc-pe4-ha-auth-capability.py']:
            original=subprocess.check_output(['git','show','2c339bb:'+path],cwd=ROOT)
            self.assertEqual((ROOT/path).read_bytes(),original)



class MqttFramingTests(unittest.TestCase):
    def client(self, chunks):
        from hioc.mqtt import MqttClient
        from unittest.mock import Mock
        sock=Mock();sock.recv.side_effect=chunks
        return MqttClient({'MQTT_HOST':'synthetic'}),sock
    def test_fragmented_connack(self):
        client,sock=self.client([b'\x20',b'\x02\x00',b'\x00'])
        with patch('hioc.mqtt.socket.create_connection',return_value=sock):client.connect()
        self.assertEqual(sock.recv.call_count,3)
    def test_unsafe_connack_and_eof(self):
        from hioc.mqtt import MqttPublishError
        for chunks in [[b'\x20\x02\x01\x00'],[b'\x20\x02\x00\x05'],[b'\x30\x02\x00\x00']]:
            client,sock=self.client(chunks)
            with patch('hioc.mqtt.socket.create_connection',return_value=sock),self.assertRaises(MqttPublishError):client.connect()
        client,sock=self.client([b'\x20',b''])
        with patch('hioc.mqtt.socket.create_connection',return_value=sock),self.assertRaises(ConnectionError) as got:client.connect()
        self.assertEqual(assess('mqtt_transport',c.mqtt_observation(got.exception))['status'],'DEPENDENCY_UNAVAILABLE')

if __name__=='__main__':unittest.main()
