"""Exact historical backport proof. All runtime inputs are synthetic."""
import ast
import copy
import hashlib
from pathlib import Path
import subprocess
import sys
import types
import unittest
from unittest.mock import Mock, patch
from hioc import home_assistant_public_projection as h
from test_pe4_ha_association_public_projection_preparation import association,state
ROOT=Path(__file__).resolve().parents[1]
BASE='29737ee97899bf06be09df661725c8186a7c339f'
PUBLIC='c762745b428b28518cf4415f7399ff2cacb70c66'
ENGINE='pi4/bin/hioc-inventory-engine.py'
PAYLOAD='tools/payloads/pe4-public-projection-pe1/hioc-inventory-engine.py'
def git(ref,path):return subprocess.check_output(['git','show',ref+':'+path],cwd=ROOT)
def derive():
    base=git(BASE,ENGINE).decode(); current=git(PUBLIC,ENGINE).decode()
    funcs=[n for n in ast.parse(current).body if isinstance(n,ast.FunctionDef) and n.name in ('_strip_home_assistant','_optional_home_assistant')]
    assert len(funcs)==2
    addition='\n\n'.join(ast.get_source_segment(current,n) for n in funcs)+'\n\n'
    assert base.count('def main() -> int:')==1
    assert base.count('previous = load_json(inventory_file, {"devices": []})')==1
    assert base.count('        store.write_json("inventory.json", inventory, INVENTORY_SCHEMA)')==1
    return base.replace('def main() -> int:',addition+'def main() -> int:',1).replace('previous = load_json(inventory_file, {"devices": []})','previous = _strip_home_assistant(load_json(inventory_file, {"devices": []}))',1).replace('        store.write_json("inventory.json", inventory, INVENTORY_SCHEMA)','        inventory = _optional_home_assistant(inventory, log)\n        store.write_json("inventory.json", inventory, INVENTORY_SCHEMA)',1).encode()
class Undo(ast.NodeTransformer):
    def visit_Module(self,n):
        n.body=[x for x in n.body if not isinstance(x,ast.FunctionDef) or x.name not in ('_strip_home_assistant','_optional_home_assistant')]
        return self.generic_visit(n)
    def visit_Assign(self,n):
        if isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name):
            if n.value.func.id=='_strip_home_assistant':n.value=n.value.args[0]
            elif n.value.func.id=='_optional_home_assistant':return None
        return self.generic_visit(n)
def structural(raw):return ast.dump(ast.parse(raw),include_attributes=False)
def functions():
    tree=ast.parse((ROOT/PAYLOAD).read_bytes());tree.body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name.startswith('_')]
    namespace={};exec(compile(tree,PAYLOAD,'exec'),namespace);return namespace
class BackportTests(unittest.TestCase):
    def test_exact_pe1_identity(self):
        raw=git(BASE,ENGINE)
        self.assertEqual(hashlib.sha256(raw).hexdigest(),'c89a294c114f87e43da1ecc8c60ba0c56801c47e3470105a8b6e8a7a8b99ab69')
        self.assertEqual(subprocess.check_output(['git','rev-parse',BASE+':'+ENGINE],cwd=ROOT).decode().strip(),'7b788e37cf4acb203ed5ca5f302ae52f1a862ae6')
    def test_payload_exact_deterministic_bytes(self):self.assertEqual((ROOT/PAYLOAD).read_bytes().replace(b'\r\n',b'\n'),derive())
    def test_entire_pe1_control_flow_recovers_after_only_projection_removed(self):
        self.assertEqual(ast.dump(Undo().visit(ast.parse(derive())),include_attributes=False),structural(git(BASE,ENGINE)))
    def test_exact_same_projection_delta_recovers_canonical_parent(self):
        self.assertEqual(ast.dump(Undo().visit(ast.parse(git(PUBLIC,ENGINE))),include_attributes=False),structural(git(PUBLIC+'^',ENGINE)))
    def test_added_functions_exact_canonical_structure(self):
        for name in ('_strip_home_assistant','_optional_home_assistant'):
            nodes=[]
            for raw in (derive(),git(PUBLIC,ENGINE)):
                nodes.append(next(n for n in ast.parse(raw).body if isinstance(n,ast.FunctionDef) and n.name==name))
            self.assertEqual(ast.dump(nodes[0],include_attributes=False),ast.dump(nodes[1],include_attributes=False))
    def test_no_compatibility_activation_or_new_topics(self):
        raw=derive().decode();tree=ast.parse(raw)
        self.assertFalse(any(isinstance(n,ast.ImportFrom) and n.module=='hioc.core.compatibility' for n in ast.walk(tree)))
        for value in ('refresh_status','mqtt_observation','compatibility_observations','platform/compatibility','_compatibility'):self.assertNotIn(value,raw)
        base_topics=[n.value for n in ast.walk(ast.parse(git(BASE,ENGINE))) if isinstance(n,ast.Constant) and isinstance(n.value,str) and '/' in n.value]
        self.assertEqual([n.value for n in ast.walk(tree) if isinstance(n,ast.Constant) and isinstance(n.value,str) and '/' in n.value],base_topics)
    def test_projection_order_before_first_public_write(self):
        main=next(n for n in ast.parse(derive()).body if isinstance(n,ast.FunctionDef) and n.name=='main')
        calls=[(n.lineno,ast.unparse(n.func)) for n in ast.walk(main) if isinstance(n,ast.Call)]
        def first(name):return min(line for line,func in calls if func==name)
        self.assertLess(first('_strip_home_assistant'),first('discover_inventory'))
        self.assertLess(first('discover_inventory'),first('_optional_home_assistant'))
        self.assertLess(first('_optional_home_assistant'),first('store.write_json'))
    def test_sanitized_complete_omission_on_helper_failure(self):
        f=functions();value={'schema_version':'1.0','devices':[{'id':'dev_'+'1'*16,'home_assistant':{'unsafe':True}}]}
        for error in (ImportError('private'),h.ProjectionError('OMITTED_INVALID'),RuntimeError('secret')):
            with patch.object(h,'project_inventory',side_effect=error):
                log=Mock();out=f['_optional_home_assistant'](value,log)
                self.assertEqual(out,{'schema_version':'1.0','devices':[{'id':'dev_'+'1'*16}]})
                self.assertNotIn('secret',str(log.mock_calls));self.assertNotIn('private',str(log.mock_calls))
    def test_pe1_generated_devices_helper_contract_and_authority_preservation(self):
        # Execute the immutable PE1 module with synthetic merge inputs only.
        # Its pure monitoring dependency must retain identical historical bytes.
        self.assertEqual(git(BASE,'pi4/lib/hioc/core/monitoring.py'),git('HEAD','pi4/lib/hioc/core/monitoring.py'))
        module=types.ModuleType('hioc._pe1_projection_fixture');module.__package__='hioc'
        sys.modules[module.__name__]=module
        try:
            exec(compile(git(BASE,'pi4/lib/hioc/inventory.py'),'immutable-pe1-inventory','exec'),module.__dict__)
            records=[dict(mac='02:00:00:00:00:01',ip='192.0.2.1',name='synthetic',source='local_host',last_seen='2030-01-02T03:04:05Z')]
            devices=module.merge_records(records,{'devices':[]},'2030-01-02T03:04:05Z',1893553445,{})
            devices=[{k:v for k,v in d.items() if not k.startswith('_')} for d in devices]
            self.assertEqual(len(devices),1)
            value=dict(schema_version='1.0',updated='2030-01-02T03:04:05Z',devices=devices,services=[],topology={'edges':[]},dependencies={'edges':[]},summary={})
            before=copy.deepcopy(value);private,schema,public=h.load_contracts(lambda p:(ROOT/p).read_bytes())
            a=association();a['hioc_device_id']=devices[0]['id']
            candidate=h.derive_projection(devices,state([a]),private,schema,public)
            out=h.attach_projection(value,candidate,private,public)
            self.assertEqual(set(out['devices'][0]['home_assistant']),set(public['required']))
            self.assertEqual(h.strip_inventory(out),before);self.assertEqual(value,before)
            self.assertEqual(h.attach_projection(value,{},private,public),before)
        finally:sys.modules.pop(module.__name__,None)
if __name__=='__main__':unittest.main()
