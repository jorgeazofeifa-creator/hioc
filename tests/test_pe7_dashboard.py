"""Execute the real local card in Node with an explicit HA/DOM contract fixture."""
import json
from pathlib import Path
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = r'''
const assert = require('node:assert/strict');
const fs = require('node:fs'); const vm = require('node:vm');
class Element {
  constructor(tag='card') { this.tag=tag; this.children=[]; this.style={}; this.events={}; this.attrs={}; }
  append(...nodes) { this.children.push(...nodes); }
  replaceChildren(...nodes) { this.children=[...nodes]; }
  setAttribute(key,value) { this.attrs[key]=value; }
  addEventListener(name,callback) { this.events[name]=callback; }
  set innerHTML(_) { throw Error('HTML injection forbidden'); }
}
let fixtureNow=Date.parse('2026-10-21T00:00:00.000000Z');
const context = {Date:class extends Date {static now(){return fixtureNow;}}, HTMLElement:Element, document:{createElement:tag=>new Element(tag)},
  customElements:{define:()=>{}}, crypto:{randomUUID:require('node:crypto').randomUUID}};
vm.createContext(context);
vm.runInContext(fs.readFileSync(process.argv[1],'utf8')+'\nglobalThis.Card=HiocAssetEditor;',context);
const Card=context.Card; const id='dev_0123456789abcdef';
let policy={asset_id:id,attachment:'strong',store_epoch:'1a1416eefec8448a898fdb27a8409a43',store_revision:1,revision:1,
 expected_availability:null,infrastructure_device:null,infrastructure_type:null,effective_expected_availability:false,
 effective_infrastructure_type:null,applied_policy_revision:null};
let calls=[], failure=null, gate=null, statusOverride=null;
const clone=x=>JSON.parse(JSON.stringify(x));
const hass={states:{sensor:{attributes:{}}}, callWS:async request=>{
 calls.push(clone(request));
 assert.equal(request.type,'call_service'); assert.equal(request.domain,'hioc_operator'); assert.equal(request.return_response,true);
 const data=request.service_data;
 if(request.service==='get_policy') return {response:{schema_version:'1.0',operation_id:null,result:'read',commit_state:'CONFIRMED',policy:clone(policy),receipt:null}};
 if(request.service==='get_availability_status' && statusOverride) return {response:clone(statusOverride)};
 if(request.service==='get_availability_status') return {response:{schema_version:'1.0',asset_id:id,result:'NOT_EVALUATED',read_at:'2026-10-21T00:00:00.000000Z',status_reason:'NOT_EVALUATED',policy_status:'PRESENT',expected_availability:policy.expected_availability,current_policy_revision:policy.revision,applied_policy_revision:null,policy_binding:'UNKNOWN',evaluation:null,observations:null}};
 if(gate) await new Promise(resolve=>{gate.release=resolve;});
 if(failure) return {response:{schema_version:'1.0',operation_id:data.operation_id,result:'error',error_code:failure,
   commit_state:failure==='COMMIT_UNKNOWN'?'UNKNOWN':'NOT_APPLIED',retryable:false}};
 if(request.service==='get_operation_result') return {response:{schema_version:'1.0',operation_id:data.operation_id,result:'not_found',receipt:null,policy:clone(policy),commit_state:'UNKNOWN'}};
 assert.equal(data.expected_revision,policy.revision); assert.equal(data.expected_store_revision,policy.store_revision);
 assert.deepEqual(Object.keys(data.fields).sort(),['expected_availability','infrastructure_device','infrastructure_type']);
 policy={...policy,...clone(data.fields),revision:(policy.revision||0)+1,store_revision:policy.store_revision+1};
 return {response:{schema_version:'1.0',operation_id:data.operation_id,result:'updated',commit_state:'CONFIRMED',policy:clone(policy),receipt:{}}};
}};
const flush=()=>new Promise(resolve=>setImmediate(resolve));
const all=node=>[node,...node.children.flatMap(all)];
const button=(card,text)=>all(card).find(n=>n.tag==='button'&&n.textContent===text);
const toggle=(card,label)=>all(card).find(n=>n.tag==='input'&&n.attrs['aria-label']===label);
async function card(){const value=new Card();value.setConfig({asset_id:id});value.hass=hass;await flush();return value;}
(async()=>{
 let tested=0;
 const value=await card(); assert.equal(calls.length,2); assert.equal(calls[0].service,'get_policy'); assert.equal(calls[1].service,'get_availability_status'); tested++;
 assert.equal(toggle(value,'Expected Availability').checked,false);
 assert(all(value).some(n=>n.textContent===' Not configured (effective OFF)')); tested++;
 for(const expected of [false,true]) for(const infrastructure of [false,true]) {
   let input=toggle(value,'Expected Availability'); input.checked=expected;input.events.change();
   input=toggle(value,'Infrastructure Device'); input.checked=infrastructure;input.events.change();
   const before=clone(policy); assert.deepEqual(policy,before);
   await value.save(); assert.equal(policy.expected_availability,expected);assert.equal(policy.infrastructure_device,infrastructure);
 }
 tested++;
 let selector=all(value).find(n=>n.tag==='select'); assert(selector); assert.equal(selector.children.length,7);
 selector.value='network_switch';selector.events.change(); await value.save();
 let input=toggle(value,'Infrastructure Device');input.checked=false;input.events.change();await value.save();
 assert.equal(policy.infrastructure_type,'network_switch');assert(!all(value).some(n=>n.tag==='select'));
 input=toggle(value,'Infrastructure Device');input.checked=true;input.events.change();
 assert.equal(all(value).find(n=>n.tag==='select').value,'network_switch'); tested++;
 const confirmed=clone(value.confirmed); value.draft.expected_availability=!confirmed.expected_availability;
 gate={}; const saving=value.save();await flush();assert.equal(value.phase,'saving');assert.deepEqual(clone(value.confirmed),confirmed);
 const other=await card();const count=calls.length;await other.save();assert.equal(calls.length,count);
 gate.release();await saving;gate=null;tested++;
 failure='REVISION_CONFLICT';const old=clone(value.confirmed);value.draft.expected_availability=false;await value.save();
 assert.equal(value.phase,'conflict');assert.deepEqual(clone(value.confirmed),old);assert.equal(button(value,'Save policy').disabled,true);
 failure=null;await value.reload();tested++;
 failure='COMMIT_UNKNOWN';await value.save();assert.equal(value.phase,'uncertain');const writes=calls.filter(x=>x.service==='update_asset_policy').length;
 failure=null;await value.reconcile();assert.equal(value.phase,'uncertain');
 assert.equal(calls.filter(x=>x.service==='update_asset_policy').length,writes);tested++;
 await value.reload();button(value,'Reset to unconfigured').events.click();assert.equal(value.draft.expected_availability,null);
 assert.notEqual(policy.expected_availability,null);tested++;
 const picker=new Card();picker.setConfig({inventory_entity:'sensor.hioc_inventory_devices'});
 const before=calls.length;picker.hass={...hass,states:{'sensor.hioc_inventory_devices':{attributes:{devices:[{id,display_name:'<script>private injection</script>'}]}}}};
 assert.equal(calls.length,before);assert(all(picker).some(n=>String(n.textContent).includes('<script>')));tested++;
 policy={...policy,revision:null,attachment:'weak'};const weak=await card();assert.equal(button(weak,'Create Asset and Save').disabled,true);
 const attempt=calls.length;await weak.save();assert.equal(calls.length,attempt);tested++;
 assert(all(value).some(n=>String(n.textContent).includes('Pending next valid evaluation')));tested++;
 policy={...policy,revision:9,attachment:'strong',expected_availability:true};
 statusOverride={schema_version:'1.0',asset_id:id,result:'READ',read_at:'2026-10-21T00:00:00.000000Z',status_reason:'SNAPSHOT_READ',
   expected_availability:true,policy_status:'PRESENT',current_policy_revision:9,applied_policy_revision:9,policy_binding:'CURRENT',
   evaluation:{availability_state:'AVAILABLE',reason_code:'QUALIFIED_POSITIVE',evidence_scope:'DEVICE',evaluated_at:'2026-10-21T00:00:00.000000Z',valid_until:'2026-10-21T00:00:20.000000Z',freshness:'FRESH'},
   observations:[{source_ref:'a'.repeat(64),scope:'DEVICE',collection_status:'SUCCESS',completeness:'COMPLETE',freshness:'FRESH',observed_at:'2026-10-21T00:00:00.000000Z',valid_until:'2026-10-21T00:00:20.000000Z'}]};
 const observed=await card();
 assert(all(observed).some(n=>String(n.textContent).includes('AVAILABLE; reason: QUALIFIED_POSITIVE; scope: DEVICE')));
 assert(all(observed).some(n=>String(n.textContent).includes('last applied revision: 9')));tested++;
 fixtureNow=Date.parse('2026-10-21T00:00:20.000000Z'); observed.render();
 assert(all(observed).some(n=>String(n.textContent).includes('Last-known evaluation; not current')));tested++;
 statusOverride.evaluation={...statusOverride.evaluation,availability_state:'STALE',reason_code:'SOURCE_STALE',freshness:'EXPIRED'};
 statusOverride.read_at='2026-10-21T00:00:20.000000Z';statusOverride.observations[0].freshness='STALE';
 await observed.reload();assert.equal(toggle(observed,'Expected Availability').checked,true);
 assert(all(observed).some(n=>String(n.textContent).includes('STALE; reason: SOURCE_STALE')));tested++;
 statusOverride.evaluation={...statusOverride.evaluation,availability_state:'UNKNOWN',reason_code:'SOURCE_MISSING',evidence_scope:'NONE',valid_until:null,freshness:'UNKNOWN'};
 statusOverride.observations=[{source_ref:'a'.repeat(64),scope:'NONE',collection_status:'ABSENT',completeness:'UNKNOWN',freshness:'ABSENT',observed_at:null,valid_until:null}];
 await observed.reload();assert(all(observed).some(n=>String(n.textContent).includes('UNKNOWN; reason: SOURCE_MISSING')));tested++;
 statusOverride.policy_binding='PENDING';statusOverride.applied_policy_revision=8;
 await observed.reload();assert(all(observed).some(n=>String(n.textContent).includes('last applied revision: 8')));
 assert(all(observed).some(n=>String(n.textContent).includes('Pending next valid evaluation')));tested++;
 statusOverride={schema_version:'1.0',result:'error',error_code:'TRUST_INVALID',retryable:false};
 await observed.reload();assert.equal(observed.phase,'ready');assert.equal(observed.status,null);
 assert.equal(toggle(observed,'Expected Availability').checked,true);
 assert(all(observed).some(n=>String(n.textContent).includes('Status unavailable; no evaluated state assumed')));tested++;
 console.log(JSON.stringify({javascript_cases:tested,result:'PASS',direct_adapter_calls:0,storage_writes:0}));
})().catch(error=>{console.error(error);process.exitCode=1;});
'''


class DashboardTests(unittest.TestCase):
    def test_real_editor_interactions_and_truthful_service_ack(self):
        node = shutil.which('node')
        if node is None:
            installed = Path('C:/Program Files/nodejs/node.exe')
            node = str(installed) if installed.is_file() else None
        if node is None:
            self.skipTest('Node unavailable: actual frontend fixtures not executed')
        result = subprocess.run([node, '-e', SCRIPT, str(ROOT/'homeassistant/www/hioc-asset-editor.js')],
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        value = json.loads(result.stdout)
        self.assertEqual(value['javascript_cases'], 17)
        self.assertEqual(value['result'], 'PASS')

    def test_minimal_dashboard_delivery_and_narrow_legacy_exclusion(self):
        dashboard = (ROOT/'homeassistant/dashboards/hioc_dashboard_v2.yaml').read_text(encoding='utf-8')
        self.assertEqual(dashboard.count('type: custom:hioc-asset-editor'), 1)
        self.assertIn('title: Inventory Explorer - Devices', dashboard)
        self.assertIn('inventory_entity: sensor.hioc_inventory_devices', dashboard)
        package = (ROOT/'homeassistant/packages/hioc_incident_center.yaml').read_text(encoding='utf-8')
        self.assertIn("is_state('sensor.hioc_pe7_incident_summary', 'VALID')", package)
        self.assertIn("map(attribute='incident_id')", package)
        self.assertIn('notify.mobile_app_pixel_9_pro_xl', package)
        self.assertIn('hioc_v1_incident_timeline_logger', package)


if __name__ == '__main__': unittest.main()
