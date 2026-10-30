"""Completion runner, current-baseline admission and post-install readback tests."""
import copy,hashlib,importlib.util,json,os
from pathlib import Path
import tempfile,unittest
from unittest.mock import Mock,patch
import test_pe73_ha_production as prior
ROOT=prior.old.ROOT
spec=importlib.util.spec_from_file_location('pe73_completion_tests',ROOT/'tools/pe73_completion.py')
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
p=prior.p

class CompletionTests(unittest.TestCase):
    def test_policy_preserves_accepted_population_scopes_and_explicit_actor_grants(self):
        q=c.module('pe73_ha_provision')
        answers=iter(['12345','12346','Offline fixture','Server fixture','Client fixture','30','https://ha.example.test'])
        with patch.object(q,'policy_input',side_effect=lambda _:next(answers)),patch.object(c.getpass,'getpass',side_effect=['human_fixture','get,create,update,result,availability_status']):
            value=c.plan(q)
        self.assertEqual(set(value['actors']),{'human_fixture'})
        for op,grant in value['actors']['human_fixture'].items():
            self.assertEqual(grant,dict(scope=q.POPULATION_SCOPES[op],amendment=c.AMENDMENT,acceptance_reference=c.ACCEPTANCE))
        self.assertNotIn('exact',str(value['actors']))
        self.assertFalse(q.packet(value,'a'*64,q.native())['backend']['enabled'])
    def test_blank_or_duplicate_operations_never_authorize(self):
        q=c.module('pe73_ha_provision')
        for operations in ('','get,get','destroy'):
            with patch.object(c.getpass,'getpass',side_effect=['fixture',operations]),self.assertRaisesRegex(c.Stop,'EXPLICIT_ACTOR'):
                c.plan(q)
    def test_environment_refuses_wrong_interpreter_before_private_reads(self):
        with patch.object(c.sys,'platform','linux'),patch.object(c.os,'getuid',return_value=1000,create=True),patch.object(c.os,'geteuid',return_value=1000,create=True),patch.object(c.os,'getgid',return_value=1000,create=True),patch.object(c.os,'getegid',return_value=1000,create=True),patch.object(c,'module') as load:
            with self.assertRaisesRegex(c.Stop,'ISOLATED_TARGET'):c.environment('pi3')
            load.assert_not_called()
    def test_invalid_transfer_has_no_subprocess(self):
        with patch.object(c.subprocess,'run') as run:
            with self.assertRaises(c.Stop):c.transfer('private-client-key','a'*64,22)
            with self.assertRaises(c.Stop):c.transfer('plan','a'*64,0)
            run.assert_not_called()
    def test_sanitized_failure_never_discloses_private_error(self):
        with patch.object(c.sys,'argv',['runner','prepare-backend','--manifest-sha','a'*64]),patch.object(c,'run',side_effect=RuntimeError('SECRET_ACTOR_TOKEN_PATH')),patch('builtins.print') as output:
            self.assertEqual(c.main(),1)
        text=str(output.call_args);self.assertNotIn('SECRET',text);self.assertIn('FAIL_STOP_PE73_COMPLETION',text)
    def test_toolkit_rejects_wrong_manifest_before_file_access(self):
        with tempfile.TemporaryDirectory() as name,patch.object(c,'ROOT',Path(name)):
            path=Path(name)/c.MANIFEST;path.parent.mkdir();path.write_bytes(b'{}')
            with self.assertRaisesRegex(c.Stop,'TOOLKIT_MANIFEST'):c.toolkit('0'*64)
    def test_export_integrity_preserves_exact_before_configs_and_backups(self):
        d=c.module('pe73_ha_delivery');config={'views':[{'path':d.VIEW,'cards':[]}],'private_fixture':'retained'}
        before={t:{'exists':False} for t in d.FILES.values()}
        j={'observation':{'config':config,'resources':[],'before':before,'after':d.add_card(config,d.VIEW)}}
        fs=Mock();fs.read.side_effect=lambda name:c.canonical(config if 'dashboard' in name else [])
        c.exports(j,fs,d)
        j['observation']['after']['private_fixture']='changed'
        with self.assertRaisesRegex(c.Stop,'ADDITIVE'):c.exports(j,fs,d)
    def test_export_corruption_is_not_accepted(self):
        d=c.module('pe73_ha_delivery');fs=Mock();fs.read.return_value=b'{}'
        with self.assertRaisesRegex(c.Stop,'EXPORT_BACKUP'):c.exports({'observation':{'config':{'views':[]},'resources':[]}},fs,d)
    def test_independent_transaction_id_never_reuses_historical_namespace(self):
        d=c.module('pe73_ha_delivery');old=d.TX
        d.configure_transaction('a'*32)
        self.assertNotEqual(d.TX,old);self.assertEqual(d.TX,'backups/pe73-ha-attempt-'+'a'*32)
        self.assertIn('a'*32,d.BOOTSTRAP)
        with self.assertRaisesRegex(d.Stop,'ALREADY_CONFIGURED'):d.configure_transaction('b'*32)
        unsafe=c.module('pe73_ha_delivery')
        with self.assertRaisesRegex(unsafe.Stop,'ID_INVALID'):unsafe.configure_transaction('../unsafe')
    def test_native_runner_never_uses_old_colocated_CA_or_activates_features(self):
        text=(ROOT/'tools/pe73_completion.py').read_text(encoding='utf8')
        self.assertNotIn('backend_material(',text);self.assertNotIn("'backend-init'",text)
        self.assertNotIn('call_service',text);self.assertNotIn('pip install',text)
        self.assertNotIn('systemctl',text);self.assertNotIn('crontab',text)
        self.assertIn("c.sign_request(q,vault",text);self.assertIn("c.runtime_material(q",text)

class PackageTests(unittest.TestCase):
    def commands(self):return c.module('pe73_completion_commands')
    def test_archive_is_exact_current_toolkit_without_credentials(self):
        import io,zipfile
        g=self.commands();raw=(ROOT/g.ARCHIVE).read_bytes()
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            mraw=z.read(g.MANIFEST);m=json.loads(mraw)
            self.assertEqual(set(z.namelist()),set(m['files'])|{g.MANIFEST})
            for name,row in m['files'].items():
                data=z.read(name);self.assertEqual(c.sha(data),row['sha256'])
                source=name.removeprefix('payloads/')
                self.assertEqual(data,(ROOT/source).read_bytes().replace(b'\r\n',b'\n'))
    def test_complete_bootstrap_python_and_pipeline_are_well_formed(self):
        import ast
        g=self.commands();commands=g.commands();self.assertEqual(len(commands),9)
        for target,action,command in commands:
            self.assertNotIn('set -e',command);self.assertNotIn('latest',command)
            if "<<'PE73'" in command:
                code=command.split('\n',1)[1].rsplit('\nPE73',1)[0];ast.parse(code)
                self.assertTrue(command.endswith('\nPE73'))
            if action=='sign-server':self.assertIn(' | ',command.splitlines()[0])
    def test_every_command_binds_current_exact_manifest(self):
        g=self.commands();identity=c.sha((ROOT/g.MANIFEST).read_bytes())
        for _,action,command in g.commands():
            self.assertIn(identity,command)
            self.assertIn('PE73_EXIT_STATUS' if not action.startswith('sign-') else 'PE73_SIGNER_EXIT',g.status(command,action.startswith('sign-')))


class CurrentRuntimeTests(unittest.TestCase):
    def fake(self,active=None,release=None):
        m=json.loads((ROOT/'governance/pe7/pe73-successor-delivery.json').read_bytes())
        current=Mock();w=Mock();current.adapter.return_value.load.return_value=(w,m)
        current.read_control.return_value={'active':active,'baseline':{'payload_release':release or m['release'],'id':'observed_fixture'}}
        return current,w,m
    def test_actual_current_baseline_replaces_historical_manifest(self):
        current,w,m=self.fake()
        with patch.object(p,'sibling',return_value=current):core,manifest,baseline=p.current_runtime()
        self.assertIs(core,w.d);self.assertEqual(manifest,m)
        current.read_control.assert_called_once_with(w,w.d.NativeFS.return_value,m)
    def test_active_transaction_refuses(self):
        current,_,_=self.fake(active={'id':'fixture'})
        with patch.object(p,'sibling',return_value=current),self.assertRaisesRegex(p.Stop,'CURRENT_PI3_BASELINE'):p.current_runtime()
    def test_nonpromoted_payload_refuses(self):
        current,_,m=self.fake();current.read_control.return_value['baseline']['payload_release']=m['prior_release']
        with patch.object(p,'sibling',return_value=current),self.assertRaisesRegex(p.Stop,'CURRENT_PI3_BASELINE'):p.current_runtime()

class FrontendEndpointTests(unittest.TestCase):
    def test_tls_peer_preflight_sends_no_http_request(self):
        probe=p.RouteProbe('https://ha.example.test','192.168.100.251')
        connection=Mock();connection.sock.getpeername.return_value=('192.168.100.251',443)
        probe.connection=Mock(return_value=connection);probe.endpoint()
        connection.connect.assert_called_once();connection.request.assert_not_called();connection.close.assert_called_once()
    def test_wrong_peer_refuses_before_any_resource_request(self):
        probe=p.RouteProbe('https://ha.example.test','192.168.100.251')
        connection=Mock();connection.sock.getpeername.return_value=('192.168.100.9',443)
        probe.connection=Mock(return_value=connection)
        with self.assertRaisesRegex(p.Stop,'PEER_ADDRESS'):probe.endpoint()
        connection.request.assert_not_called();connection.close.assert_called_once()


class ReadOnlyTerminalTests(unittest.TestCase):
    def api(self,state='DELIVERED_DISABLED'):
        self.fs=Mock();self.row={'id':'fixture','url':'/local/hioc-asset-editor.js','type':'module'}
        self.fs.load.return_value={'state':state,'pending':None,'dashboard':p.d.DASHBOARD,'resource':self.row}
        return p.DeliveryAPI(Mock(authenticated=True,counter=0,calls=[]),self.fs,read_only=True)
    def test_verification_accepts_exact_owned_resource_without_mutation(self):
        api=self.api();api._resources([self.row]);self.assertTrue(api.read_only)
    def test_verification_rejects_lookalike_or_duplicate_resource(self):
        api=self.api()
        with self.assertRaisesRegex(p.Stop,'RESOURCE_CONFLICT'):api._resources([dict(self.row,id='other')])
    def test_nonterminal_never_admitted_as_read_only_acceptance(self):
        with self.assertRaisesRegex(p.Stop,'TERMINAL_REQUIRED'):self.api('INSTALLING')
    def test_verification_cannot_write(self):
        api=self.api()
        with patch.object(api,'_request') as request,self.assertRaisesRegex(p.Stop,'MUTATION_OUTSIDE'):
            api.call({'type':'lovelace/config/save','url_path':p.d.DASHBOARD,'config':{}})
        request.assert_not_called()

class CompletionProtocolTests(unittest.TestCase):
    session=prior.LiveProtocolTests.session
    # Only these additional methods are selected by the focused harness.
    def test_authenticated_finish_has_no_server_error_or_consumer_release(self):
        peer,packet=self.session();peer.check(packet);peer.finish(packet)
        self.assertEqual(peer.channel.recv(1),b'')
        self.assertEqual(self.errors,[])
        self.assertTrue(peer.stopped)
        with self.assertRaises(p.Stop):peer.check(packet)
    def test_finish_before_check_is_not_authorized(self):
        peer,packet=self.session()
        with self.assertRaisesRegex(p.Stop,'GUARD_OPERATION'):peer.finish(packet)

if __name__=='__main__':unittest.main()
