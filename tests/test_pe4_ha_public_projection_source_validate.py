"""Future source validator tested only through injected synthetic contexts."""
import copy
import importlib.util
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch
from contextlib import redirect_stdout
from hioc import home_assistant_public_projection as h
from test_pe4_ha_association_public_projection import V,S,P,ROOT,inventory
from test_pe4_ha_association_public_projection_preparation import association,state,canonical
spec=importlib.util.spec_from_file_location('pe4_projection_source_validator',ROOT/'tools/hioc-pe4-ha-public-projection-source-validate.py')
tool=importlib.util.module_from_spec(spec);spec.loader.exec_module(tool)
COMMIT='a'*40


class Context:
    def __init__(self):self.calls=[];self.problem=None;self.public=inventory();self.raw=canonical(state([association()]))
    def target(self):
        self.calls.append('target')
        if self.problem in ['TARGET_INVALID','OPERATOR_INVALID']:raise tool.ValidationError(self.problem)
    def source(self,commit):
        self.calls.append('source')
        if commit!=COMMIT:raise tool.ValidationError('SOURCE_COMMIT_MISMATCH')
        if self.problem in ['IDENTITY_MISMATCH','SOURCE_INVALID']:raise tool.ValidationError(self.problem)
        return h
    def contracts(self,helper):
        self.calls.append('contracts')
        if self.problem=='private_identity':raise tool.ValidationError('IDENTITY_MISMATCH')
        return V,S,P
    def snapshot(self,helper):
        self.calls.append('snapshot')
        if self.problem=='busy':raise h.ProjectionError('OMITTED_BUSY')
        if self.problem in h.CODES:raise h.ProjectionError(self.problem)
        return self.raw
    def inventory(self,helper,private):self.calls.append('inventory');return copy.deepcopy(self.public)


class SourceValidatorTests(unittest.TestCase):
    def test_pass_exact_commit_closed_output_and_no_side_effects(self):
        context=Context();result=tool.validate_source(COMMIT,context)
        self.assertEqual(result['RESULT'],'PASS');self.assertEqual(result['SOURCE_COMMIT'],COMMIT);self.assertTrue(result['STOP_REQUIRED'])
        self.assertEqual(result['MODE'],'READ_ONLY_SOURCE_VALIDATION')
        self.assertEqual(context.calls,['target','source','contracts','snapshot','inventory','source'])
        for key in ['PUBLIC_OUTPUT_WRITTEN','MQTT_PUBLISHED','HA_NETWORK_ATTEMPTED','CREDENTIAL_ACCESSED','ADAPTER_EXECUTED','CRONTAB_MUTATED','PRODUCTION_MUTATED','PRIOR_PUBLIC_PROJECTION_PRESENT','PUBLIC_PROJECTION_ALREADY_PRESENT']:self.assertIs(result[key],False)
        for key in tool.CHECKS:self.assertIn(result[key],['PASS','CLEAN'])
        text=json.dumps(result)
        for secret in ['dev_','fixture_device','sensor.','mqtt','2030','unique_mac']:self.assertNotIn(secret,text)
    def test_busy_incomplete_stop_without_retry(self):
        context=Context();context.problem='busy';result=tool.validate_source(COMMIT,context)
        self.assertEqual((result['RESULT'],result['ERROR_CODE'],result['SHARED_LOCK_ACQUISITION']),('INCOMPLETE','ASSOCIATION_BUSY','BUSY'))
        self.assertEqual(context.calls.count('snapshot'),1);self.assertNotIn('inventory',context.calls)
    def test_wrong_commit_target_operator_identities_and_internal_failures(self):
        for problem in ['TARGET_INVALID','OPERATOR_INVALID','IDENTITY_MISMATCH','SOURCE_INVALID','private_identity','OMITTED_INVALID','OMITTED_UNSAFE','OMITTED_UNAVAILABLE','OMITTED_INCOHERENT','OMITTED_INTERNAL']:
            context=Context();context.problem=problem;result=tool.validate_source(COMMIT,context)
            self.assertEqual(result['RESULT'],'FAIL');self.assertIn(result['ERROR_CODE'],tool.ERRORS);self.assertTrue(result['STOP_REQUIRED'])
        self.assertEqual(tool.validate_source('b'*40,Context())['ERROR_CODE'],'SOURCE_COMMIT_MISMATCH')
        self.assertEqual(tool.validate_source('private arbitrary value',Context())['SOURCE_COMMIT'],'UNVERIFIED')
    def test_unexpected_existing_namespace_fails_no_repair(self):
        context=Context();context.public['devices'][0]['home_assistant']={'private':'never dump'}
        result=tool.validate_source(COMMIT,context)
        self.assertEqual(result['ERROR_CODE'],'UNEXPECTED_EXISTING_PUBLIC_PROJECTION');self.assertEqual(result['RESULT'],'FAIL')
        self.assertTrue(result['PUBLIC_PROJECTION_ALREADY_PRESENT']);self.assertTrue(result['STOP_REQUIRED']);self.assertIn('home_assistant',context.public['devices'][0])
        self.assertNotIn('never dump',json.dumps(result))
    def test_private_invalid_schema_semantics_and_no_content_output(self):
        for raw in [b'private secret',b'\xff',canonical(state([association(),association()]))]:
            context=Context();context.raw=raw;result=tool.validate_source(COMMIT,context)
            self.assertEqual(result['RESULT'],'FAIL');self.assertNotIn('private secret',json.dumps(result))
    def test_cli_pass_incomplete_fail_and_output_cap(self):
        for problem,expected in [(None,0),('busy',2),('OMITTED_INVALID',1)]:
            context=Context();context.problem=problem
            with patch.object(tool,'NativeContext',return_value=context),redirect_stdout(io.StringIO()) as output:
                self.assertEqual(tool.main(['--source-commit',COMMIT]),expected)
            self.assertLessEqual(len(output.getvalue().encode()),8192);self.assertIn('STOP_REQUIRED=TRUE',output.getvalue())
        with redirect_stdout(io.StringIO()) as output:self.assertEqual(tool.main(['--private-secret','do-not-echo']),1)
        self.assertNotIn('do-not-echo',output.getvalue());self.assertNotIn('--private-secret',output.getvalue())
    def test_ast_cli_no_engine_network_credential_cron_mutation(self):
        import ast
        text=(ROOT/'tools/hioc-pe4-ha-public-projection-source-validate.py').read_text(encoding='utf8');tree=ast.parse(text)
        calls={n.func.attr for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute)}
        self.assertFalse(calls&{'write_text','write_bytes','mkdir','unlink','rename','publish','run_cycle','network','credential'})
        self.assertNotIn('hioc-inventory-engine.py',text)
        for node in ast.walk(tree):
            if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and node.func.attr=='replace':self.assertEqual(ast.unparse(node.func.value),'RECORD')
    def test_native_git_readonly_source_identity_and_artifact_check(self):
        context=tool.NativeContext()
        def git(*args):
            if args[:1]==('rev-parse',):
                if args[1] in ['HEAD','origin/main']:return COMMIT.encode()
                if args[1]=='--git-path':return ('missing_'+args[2]).encode()
                return b'blob'
            if args[:1]==('branch',):return b'main'
            if args[:1]==('status',):return b''
            if args[:1]==('show',):
                if args[1].endswith(tool.RECORD):return b'{"implementation_artifacts":[]}'
                if args[1].endswith(tool.RECORD.replace('.json','.schema.json')):return b'{"type":"object","additionalProperties":false,"required":["implementation_artifacts"],"properties":{"implementation_artifacts":{"type":"array","items":false,"minItems":0,"maxItems":0,"prefixItems":[]}}}'
                return (ROOT/tool.HELPER).read_bytes()
            raise AssertionError(args)
        with patch.object(context,'git',side_effect=git):self.assertEqual(context.source(COMMIT).MODULE_SHA,h.MODULE_SHA)
        with patch.object(tool.subprocess,'check_output',return_value=b'') as command:context.git('status','--porcelain')
        self.assertEqual(command.call_args.kwargs['env']['GIT_OPTIONAL_LOCKS'],'0')
        self.assertIn('core.fsmonitor=false',command.call_args.args[0])
    def test_constant_governance_closed_rejects_extra(self):
        schema={'type':'object','additionalProperties':False,'required':['ok'],'properties':{'ok':{'const':True}}}
        tool.constant_contract({'ok':True},schema)
        for value in [{'ok':True,'private':'x'},{'ok':1},{}]:
            with self.assertRaises(tool.ValidationError):tool.constant_contract(value,schema)


if __name__=='__main__':unittest.main()
