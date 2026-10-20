"""Synthetic/local PE-6.4 protected evidence; never production observations."""
import ast
import copy
from dataclasses import replace
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import socket
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('pe6_acceptance_evidence', ROOT/'tools/pe6_protected_state_evidence.py')
m = importlib.util.module_from_spec(SPEC); sys.modules[SPEC.name] = m; SPEC.loader.exec_module(m)
PASS = dict(status='PASS', stage='FUNCTIONAL_VERIFICATION')
INSPECT = dict(status='PASS', stage='AFTER_STATE')
PRIVATE = m.ROOT + '/state/PRIVATE-host-192.0.2.1-aa:bb:cc:dd:ee:ff'
INVENTORY = m.ROOT + '/state/inventory/inventory.json'
CODE = m.ROOT + '/pi4/lib/hioc/classification.py'

def fp(inode=10, size=20, mode=stat.S_IFREG|0o600):
    return [1, inode, mode, 1000, 1000, 1, size, 1000000000000000000, 1000000000000000001]
def observation():
    v={k:{} for k in m.CATEGORIES}
    v.update(code={CODE:[fp(), 'a'*64]}, runtime_root=fp(mode=stat.S_IFDIR|0o755), user_crontab=[0,'b'*64,'c'*64])
    return v

def captures(a, b):
    return m.capture_protected(lambda:a), m.capture_protected(lambda:b)
def report(a, b, **kw):
    return json.loads(m.build_report(a,b,primary_outcome=kw.pop('primary_outcome', PASS),
                protected_inspection_outcome=kw.pop('protected_inspection_outcome', INSPECT),**kw))
def changed(path=PRIVATE):
    a=observation(); a['producer_state'][path]=fp()
    b=copy.deepcopy(a); b['producer_state'][path][6]+=1
    return captures(a,b)

class ProtectedEvidenceTests(unittest.TestCase):
    def test_unchanged_all_categories_pass(self):
        a,b=captures(observation(),observation());r=report(a,b)
        self.assertEqual(r['result'],'PASS');self.assertEqual(r['categories'],list(m.CATEGORIES));self.assertEqual(r['changed_object_count'],0)
    def test_creation_reports_presence_and_full_width_fields(self):
        a=observation();b=copy.deepcopy(a);b['producer_state'][PRIVATE]=fp(inode=2**63+123)
        x,y=captures(a,b);d=report(x,y)['object_differences'][0]
        self.assertIn('APPEARED',d['change_types']);self.assertEqual(d['observation_before'],'NOT_ENUMERATED')
        self.assertEqual(d['field_differences']['st_ino']['after'],str(2**63+123));self.assertEqual(d['object_identity_after']['inode'],str(2**63+123))
    def test_deletion(self):
        a=observation();a['producer_state'][PRIVATE]=fp();b=copy.deepcopy(a);b['producer_state'].clear()
        d=report(*captures(a,b))['object_differences'][0];self.assertIn('DISAPPEARED',d['change_types'])
    def test_identity_replacement(self):
        a=observation();a['producer_state'][PRIVATE]=fp();b=copy.deepcopy(a);b['producer_state'][PRIVATE][1]=999
        d=report(*captures(a,b))['object_differences'][0]
        self.assertIn('IDENTITY_CHANGED',d['change_types']);self.assertEqual(set(d['field_differences']),{'st_ino'})
    def test_type_change(self):
        a=observation();a['producer_state'][PRIVATE]=fp();b=copy.deepcopy(a);b['producer_state'][PRIVATE][2]=stat.S_IFDIR|0o700
        d=report(*captures(a,b))['object_differences'][0];self.assertIn('TYPE_CHANGED',d['change_types']);self.assertEqual(d['object_type_after'],'DIRECTORY')
    def test_metadata_only_change_no_invented_hash(self):
        a=observation();a['producer_state'][PRIVATE]=fp();b=copy.deepcopy(a);b['producer_state'][PRIVATE][7]+=20
        d=report(*captures(a,b))['object_differences'][0]
        self.assertEqual(set(d['field_differences']),{'st_mtime_ns'});self.assertEqual(d['content_hash_evidence'],dict(before=None,after=None,basis='NOT_CAPTURED'))
    def test_directory_only_change(self):
        path=m.ROOT+'/state/inventory';a=observation();a['producer_state'][path]=fp(mode=stat.S_IFDIR|0o750);b=copy.deepcopy(a);b['producer_state'][path][8]+=1
        d=report(*captures(a,b))['object_differences'][0]
        self.assertEqual(d['artifact_id'],'STATE_INVENTORY_DIRECTORY');self.assertEqual(d['content_hash_evidence']['basis'],'NOT_APPLICABLE');self.assertEqual(d['adjudication'],'UNATTRIBUTED')
    def test_incomplete_directory_traversal_never_empty_success(self):
        def failed():raise OSError('PRIVATE directory')
        a=m.capture_protected(failed);b=m.capture_protected(observation);r=report(a,b)
        self.assertEqual(r['result'],'INSUFFICIENT_EVIDENCE');self.assertFalse(r['difference_count_complete'])
        self.assertEqual(r['capture_intervals']['before']['completeness'],'INCOMPLETE')
        self.assertFalse(any('APPEARED' in d['change_types'] for d in r['object_differences']))
    def test_known_protected_gate_failure_retains_fail_without_partial_objects(self):
        def failed():raise m.ProtectedInvariantFailure('PRIVATE')
        a=m.capture_protected(observation);b=m.capture_protected(failed);r=report(a,b)
        self.assertEqual(r['result'],'FAIL');self.assertEqual(r['protected_inspection_outcome']['status'],'FAIL')
        self.assertEqual(r['capture_intervals']['after']['error'],'PROTECTED_CHECK_FAILED')
        self.assertNotIn('PRIVATE',json.dumps(r))
    def test_prohibited_gate_failure_survives_clock_failure_too(self):
        def failed():raise m.ProtectedInvariantFailure('PRIVATE')
        a=m.capture_protected(observation)
        clock=iter(['2026-10-20T01:00:00Z','PRIVATE-clock']).__next__
        b=m.capture_protected(failed,clock=clock);r=report(a,b)
        self.assertEqual(r['result'],'FAIL');self.assertEqual(r['protected_inspection_outcome']['status'],'FAIL')
        self.assertTrue(r['capture_intervals']['after']['protected_gate_failed'])
        self.assertEqual(r['capture_intervals']['after']['error'],'CLOCK_INVALID')
        self.assertNotIn('PRIVATE',json.dumps(r))
    def test_unstable_capture(self):
        def failed():raise m.ObservationUnstable('PRIVATE')
        a=m.capture_protected(failed);b=m.capture_protected(observation)
        self.assertEqual(report(a,b)['capture_intervals']['before']['completeness'],'UNSTABLE')
    def test_transient_create_delete_limits_with_real_local_files(self):
        with tempfile.TemporaryDirectory() as td:
            folder=Path(td)
            def snapshot():
                v=observation();v['producer_state'][m.ROOT+'/state']=list(fp(mode=stat.S_IFDIR|0o750))
                s=folder.stat();v['producer_state'][m.ROOT+'/state'][7]=s.st_mtime_ns;v['producer_state'][m.ROOT+'/state'][8]=s.st_ctime_ns
                for p in folder.iterdir():
                    s=p.stat();v['producer_state'][m.ROOT+'/state/'+p.name]=[s.st_dev,s.st_ino,s.st_mode,s.st_uid,s.st_gid,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
                return v
            a=m.capture_protected(snapshot);f=folder/'PRIVATE-transient';f.write_bytes(b'x');f.unlink();b=m.capture_protected(snapshot)
            r=report(a,b);self.assertNotIn('PRIVATE-transient',json.dumps(r))
            self.assertTrue(all(d['object_type_before']=='DIRECTORY' for d in r['object_differences']))
            self.assertIn('ENDPOINT_OBSERVATIONS_NOT_EVENT_HISTORY',r['limitations'])
    def test_unknown_path_sanitized_and_ids_stable_per_pair(self):
        a,b=changed();raw=m.build_report(a,b,primary_outcome=PASS,protected_inspection_outcome=INSPECT)
        self.assertNotIn(b'PRIVATE',raw);self.assertNotIn(b'192.0.2.1',raw);self.assertNotIn(b'aa:bb',raw);self.assertNotIn(m.ROOT.encode(),raw)
        d=json.loads(raw)['object_differences'][0];self.assertTrue(d['artifact_id'].startswith('OBJECT_'))
        self.assertEqual(raw,m.build_report(a,b,primary_outcome=PASS,protected_inspection_outcome=INSPECT))
    def test_known_mutable_is_not_permission(self):
        a,b=changed(INVENTORY);r=report(a,b);d=r['object_differences'][0]
        self.assertIn('hioc-inventory-engine.py',d['contract_basis']['source']);self.assertEqual(d['mutability'],'INDEPENDENTLY_MUTABLE');self.assertEqual(d['adjudication'],'UNATTRIBUTED');self.assertEqual(r['result'],'INSUFFICIENT_EVIDENCE')
    def test_specific_independent_review_attestation_bound_to_exact_change(self):
        a,b=changed(INVENTORY);d=report(a,b)['object_differences'][0]
        permit=m.ReviewedPermission(a.digest,b.digest,d['artifact_id'],d['difference_sha256'],'INVENTORY_ENGINE','SYNTHETIC_AUTHORIZATION','SYNTHETIC_ACCEPTANCE')
        r=report(a,b,reviewed_permissions=[permit]);self.assertEqual(r['result'],'PASS')
        self.assertEqual(r['object_differences'][0]['adjudication_basis'],'EXTERNAL_INDEPENDENT_REVIEW_ATTESTATION')
        self.assertIn('PERMISSIONS_ARE_EXTERNAL_REVIEW_ATTESTATIONS',r['limitations'])
    def test_wrong_change_wrong_capture_or_wrong_writer_rejected(self):
        a,b=changed(INVENTORY);d=report(a,b)['object_differences'][0]
        permit=m.ReviewedPermission(a.digest,b.digest,d['artifact_id'],d['difference_sha256'],'INVENTORY_ENGINE','SYNTHETIC_AUTHORIZATION','SYNTHETIC_ACCEPTANCE')
        for bad in (replace(permit,difference_sha256='f'*64),replace(permit,after_capture_sha256='e'*64),replace(permit,writer_id='UNKNOWN_WRITER')):
            with self.subTest(bad=bad.writer_id):
                with self.assertRaises(m.EvidenceError):report(a,b,reviewed_permissions=[bad])
    def test_filename_or_true_boolean_cannot_claim_permission(self):
        a,b=changed(INVENTORY)
        with self.assertRaises(m.EvidenceError):report(a,b,reviewed_permissions=[True])
        with self.assertRaises(m.EvidenceError):report(a,b,reviewed_permissions=[dict(permitted=True)])
    def test_immutable_content_change_fails_even_same_fingerprint(self):
        a=observation();b=copy.deepcopy(a);b['code'][CODE][1]='d'*64
        r=report(*captures(a,b));self.assertEqual(r['result'],'FAIL');self.assertIn('CONTENT_HASH_CHANGED',r['object_differences'][0]['change_types']);self.assertEqual(r['object_differences'][0]['artifact_id'],'RUNTIME_CLASSIFICATION_PY')
    def test_review_cannot_waive_immutable_or_security_change(self):
        a,b=changed(INVENTORY);bad_observation=observation();bad_observation['producer_state'][INVENTORY]=fp(mode=stat.S_IFREG|0o644)
        a=m.capture_protected(lambda:dict(observation(),producer_state={INVENTORY:fp()}));b=m.capture_protected(lambda:bad_observation)
        d=report(a,b)['object_differences'][0]
        permit=m.ReviewedPermission(a.digest,b.digest,d['artifact_id'],d['difference_sha256'],'INVENTORY_ENGINE','SYNTHETIC_AUTHORIZATION','SYNTHETIC_ACCEPTANCE')
        with self.assertRaises(m.EvidenceError):report(a,b,reviewed_permissions=[permit])
        x=observation();y=copy.deepcopy(x);y['code'][CODE][1]='e'*64
        a,b=captures(x,y);d=report(a,b)['object_differences'][0]
        permit=m.ReviewedPermission(a.digest,b.digest,d['artifact_id'],d['difference_sha256'],'INVENTORY_ENGINE','SYNTHETIC_AUTHORIZATION','SYNTHETIC_ACCEPTANCE')
        with self.assertRaises(m.EvidenceError):report(a,b,reviewed_permissions=[permit])
    def test_count_bound_and_hidden_prohibited_change_still_fail(self):
        a=observation();b=copy.deepcopy(a)
        for i in range(5):b['producer_state'][PRIVATE+str(i)]=fp()
        b['code'][CODE][1]='d'*64; b['code'][CODE][0]=[v+1 for v in fp()]
        r=report(*captures(a,b),max_differences=1)
        self.assertEqual(set(r['object_differences'][0]['field_differences']),set(m.FIELDS));self.assertEqual(r['changed_object_count'],6);self.assertEqual(r['omitted_object_count'],5);self.assertTrue(r['differences_truncated']);self.assertEqual(r['result'],'FAIL')
        x,y=captures(a,b);raw=m.build_report(x,y,primary_outcome=PASS,protected_inspection_outcome=INSPECT,max_report_bytes=2048)
        r=json.loads(raw);self.assertEqual(r['reported_object_count'],0);self.assertEqual(r['result'],'FAIL')
    def test_byte_bound_never_passes_truncated_evidence(self):
        a=observation();b=copy.deepcopy(a)
        for i in range(10):b['producer_state'][PRIVATE+str(i)]=fp()
        x,y=captures(a,b);raw=m.build_report(x,y,primary_outcome=PASS,protected_inspection_outcome=INSPECT,max_report_bytes=2048)
        r=json.loads(raw);self.assertLessEqual(len(raw),2048);self.assertEqual(r['result'],'INSUFFICIENT_EVIDENCE');self.assertTrue(r['differences_truncated'])
    def test_primary_and_inspection_failures_both_retained(self):
        a,b=captures(observation(),observation());r=report(a,b,primary_outcome=dict(status='FAIL',stage='FUNCTIONAL_VERIFICATION',category='REQUIRED_CHECK_FAILED'),protected_inspection_outcome=dict(status='FAIL',stage='AFTER_STATE',category='PROTECTED_CHECK_FAILED'))
        self.assertEqual(r['result'],'FAIL');self.assertEqual(r['primary_outcome']['stage'],'FUNCTIONAL_VERIFICATION');self.assertEqual(r['protected_inspection_outcome']['category'],'PROTECTED_CHECK_FAILED')
    def test_primary_fail_plus_incomplete_after_stays_fail(self):
        a=m.capture_protected(observation)
        def fail():raise OSError('PRIVATE')
        b=m.capture_protected(fail);r=report(a,b,primary_outcome=dict(status='FAIL',stage='SINGLE_EVALUATION'),protected_inspection_outcome=dict(status='INCOMPLETE',stage='AFTER_STATE'))
        self.assertEqual(r['result'],'FAIL');self.assertEqual(r['protected_inspection_outcome']['status'],'INCOMPLETE')
    def test_capture_once_no_retry_and_no_side_effect_facilities(self):
        calls=[]
        def observe():calls.append(1);return observation()
        with patch('builtins.open',side_effect=AssertionError('write')),patch.object(socket,'socket',side_effect=AssertionError('network')),patch.object(subprocess,'run',side_effect=AssertionError('process')),patch.object(os,'open',side_effect=AssertionError('lock')),patch.object(os,'chmod',side_effect=AssertionError('chmod')):
            a=m.capture_protected(observe);b=m.capture_protected(observe);r=report(a,b)
        self.assertEqual(calls,[1,1]);self.assertEqual(r['result'],'PASS')
        tree=ast.parse((ROOT/'tools/pe6_protected_state_evidence.py').read_text(encoding='utf8'))
        self.assertFalse(any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='evaluate' for n in ast.walk(tree)))
    def test_capture_failure_not_retried_or_exception_leaked(self):
        calls=[]
        def fail():calls.append(1);raise ValueError('PRIVATE CONTENT AND PATH')
        a=m.capture_protected(fail);b=m.capture_protected(observation);raw=m.build_report(a,b,primary_outcome=PASS,protected_inspection_outcome=INSPECT)
        self.assertEqual(calls,[1]);self.assertNotIn(b'PRIVATE',raw);self.assertEqual(json.loads(raw)['result'],'INSUFFICIENT_EVIDENCE')
    def test_clock_failure_and_reversal_cannot_pass(self):
        clock=iter(['2026-10-20T01:00:02Z','2026-10-20T01:00:01Z']).__next__
        a=m.capture_protected(observation,clock=clock);b=m.capture_protected(observation)
        self.assertEqual(a.completeness,'UNSTABLE');self.assertEqual(report(a,b)['result'],'INSUFFICIENT_EVIDENCE')
        c=m.capture_protected(observation,clock=lambda:'PRIVATE-clock')
        self.assertNotIn('PRIVATE',json.dumps(report(c,b)))
    def test_overlapping_capture_intervals_are_explicit(self):
        a=m.capture_protected(observation,clock=iter(['2026-10-20T01:00:00Z','2026-10-20T01:00:02Z']).__next__)
        b=m.capture_protected(observation,clock=iter(['2026-10-20T01:00:01Z','2026-10-20T01:00:03Z']).__next__)
        r=report(a,b);self.assertFalse(r['observation_intervals_ordered']);self.assertEqual(r['result'],'INSUFFICIENT_EVIDENCE')
    def test_malformed_observation_or_missing_category_not_success(self):
        for bad in ({},dict(observation(),producer_state={PRIVATE:['PRIVATE']})):
            a=m.capture_protected(lambda:bad);b=m.capture_protected(observation)
            self.assertEqual(report(a,b)['result'],'INSUFFICIENT_EVIDENCE')
    def test_forged_capture_cannot_inject_private_receipt_fields(self):
        a,b=captures(observation(),observation())
        for forged in (replace(a,error='PRIVATE'),replace(a,started_at='PRIVATE')):
            with self.assertRaises((m.EvidenceError,ValueError)):report(forged,b)
    def test_schedule_control_and_nested_lock_categories_not_dropped(self):
        a=observation();a['locks']['/tmp/hioc-fixture']={'/tmp/hioc-fixture':fp()}
        a['schedule']['/etc/cron.d/PRIVATE']= [fp(), 'd'*64]
        b=copy.deepcopy(a);b['locks']['/tmp/hioc-fixture']['/tmp/hioc-fixture'][8]+=1;b['schedule']['/etc/cron.d/PRIVATE'][1]='e'*64;b['user_crontab'][1]='f'*64
        r=report(*captures(a,b));self.assertEqual({d['category'] for d in r['object_differences']},{'locks','schedule','user_crontab'})
        self.assertNotIn('PRIVATE',json.dumps(r));self.assertTrue(any(d['control_differences'] for d in r['object_differences']))

if __name__ == '__main__': unittest.main()
