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

class PE5DirectoryPublicationTests(unittest.TestCase):
    """Synthetic EXTERNAL review attestations; never production observations."""
    directory=m.PE5_DIRECTORY
    output=m.PE5_DIRECTORY+'/current.json'
    durability=m.PE5_DIRECTORY+'/current.durability.json'

    def fixtures(self, mutate=None):
        a=observation()
        a['producer_state']={self.directory:[1,50,stat.S_IFDIR|0o700,1000,1000,2,4096,10,11],
            self.output:fp(inode=60,size=4915),self.durability:fp(inode=61,size=269)}
        b=copy.deepcopy(a)
        b['producer_state'][self.directory][7:]=[12,13]
        b['producer_state'][self.output]=fp(inode=62,size=4916)
        b['producer_state'][self.output][7]+=2;b['producer_state'][self.output][8]+=2
        b['producer_state'][self.durability]=fp(inode=63,size=269)
        b['producer_state'][self.durability][7]+=2;b['producer_state'][self.durability][8]+=2
        if mutate:mutate(a,b)
        self.last_observations=(a,b)
        x=m.capture_protected(lambda:a,clock=iter(['2026-10-20T03:32:01Z','2026-10-20T03:32:01.1Z']).__next__)
        y=m.capture_protected(lambda:b,clock=iter(['2026-10-20T03:32:03Z','2026-10-20T03:32:03.1Z']).__next__)
        e=dict(schema_version='1.0',validation='PASS_SCHEMA_CANONICAL_DOMAIN_DESCRIPTOR_DIGEST_REVISION_STABLE_PAIR',
            domain='GENERATED_RELATIONSHIP_OUTPUT',durability_state='CONFIRMED',candidate=None,
            transaction_id='dur_'+'1'*32,evaluated_at='2026-10-20T03:32:02Z',
            output_sha256='e'*64,durability_sha256='f'*64,confirmed_sha256='e'*64,
            output_source_revision=1,confirmed_source_revision=1,
            output_after_fingerprint=copy.deepcopy(b['producer_state'].get(self.output)),
            durability_after_fingerprint=copy.deepcopy(b['producer_state'].get(self.durability)))
        for field in ('output_after_fingerprint','durability_after_fingerprint'):
            if e[field] is not None and len(e[field])==2:e[field]=e[field][0]
        differences=report(x,y)['object_differences'];by_id={d['artifact_id']:d for d in differences}
        grants=[m.ReviewedPermission(x.digest,y.digest,identifier,by_id[identifier]['difference_sha256'],
            'PE5_COMPOSER','SYNTHETIC_PE5_AUTHORIZATION','SYNTHETIC_PE5_ACCEPTANCE',
            e if identifier=='PE5_OUTPUT_DIRECTORY' else None)
            for identifier in ('PE5_OUTPUT_DIRECTORY','PE5_CURRENT_JSON','PE5_CURRENT_DURABILITY_JSON')
            if identifier in by_id]
        return x,y,e,grants

    def test_exact_three_object_publication_requires_external_review(self):
        x,y,e,g=self.fixtures()
        self.assertEqual(report(x,y)['result'],'INSUFFICIENT_EVIDENCE')
        result=report(x,y,reviewed_permissions=g)
        self.assertEqual(result['result'],'PASS');self.assertEqual(result['changed_object_count'],3)
        self.assertTrue(all(d['adjudication']=='PERMITTED_CONFIRMED' for d in result['object_differences']))
        hashes={d['review_references']['pe5_publication_sha256'] for d in result['object_differences']}
        self.assertEqual(len(hashes),1)
        for d in result['object_differences']:
            self.assertIsNone(d['content_hash_evidence']['before'])
            self.assertIsNone(d['content_hash_evidence']['after'])
        # Later supplied digests are referenced, never relabeled captured hashes.
        self.assertNotIn('dur_111',json.dumps(result))

    def test_published_difference_hashes_remain_unchanged(self):
        x,y,e,g=self.fixtures()
        raw=subprocess.check_output(['git','cat-file','blob',
            'f4248d7ade25058da07abcf77a7c79dd2c6bd5d9:tools/pe6_protected_state_evidence.py'],cwd=ROOT)
        old=type(sys)('pe64_published_directory_binding');sys.modules[old.__name__]=old
        self.addCleanup(lambda:sys.modules.pop(old.__name__,None))
        exec(compile(raw,'published_evidence.py','exec'),old.__dict__)
        a,b=self.last_observations
        old_report=json.loads(old.build_report(old.capture_protected(lambda:a),old.capture_protected(lambda:b),
            primary_outcome=PASS,protected_inspection_outcome=INSPECT))
        expected={d['artifact_id']:d['difference_sha256'] for d in old_report['object_differences']}
        current={d['artifact_id']:d['difference_sha256'] for d in report(x,y)['object_differences']}
        self.assertEqual(current,expected)
        self.assertEqual(report(x,y,reviewed_permissions=g)['result'],'PASS')

    def test_directory_permission_without_transaction_is_rejected(self):
        x,y,e,g=self.fixtures();g[0]=replace(g[0],pe5_publication=None)
        with self.assertRaises(m.EvidenceError):report(x,y,reviewed_permissions=g)

    def test_missing_or_incomplete_validation_rejected(self):
        for field in ('transaction_id','domain','output_after_fingerprint','validation'):
            x,y,e,g=self.fixtures();del e[field]
            with self.subTest(field=field):
                with self.assertRaises(m.EvidenceError):report(x,y,reviewed_permissions=g)
        x,y,e,g=self.fixtures();e['validation']='INCOMPLETE'
        with self.assertRaises(m.EvidenceError):report(x,y,reviewed_permissions=g)

    def test_unconfirmed_durability_or_candidate_rejected(self):
        for field,value in [('durability_state','PENDING'),('candidate',{'sha256':'e'*64})]:
            x,y,e,g=self.fixtures();e[field]=value
            with self.subTest(field=field):
                with self.assertRaises(m.EvidenceError):report(x,y,reviewed_permissions=g)

    def test_descriptor_digest_revision_domain_and_transaction_rejected(self):
        for field,value in [('confirmed_sha256','0'*64),('confirmed_source_revision',2),
                ('confirmed_source_revision',True),('output_source_revision',0),
                ('output_sha256','INVALID'),('durability_sha256','INVALID'),
                ('domain','CONFIGURED_MAPPING_SOURCE'),('transaction_id','dur_INVALID'),
                ('evaluated_at','2026-10-20T03:33:00Z')]:
            x,y,e,g=self.fixtures();e[field]=value
            with self.subTest(field=field,value=value):
                with self.assertRaises(m.EvidenceError):report(x,y,reviewed_permissions=g)

    def test_wrong_writer_or_review_references_rejected(self):
        for i in range(3):
            for field,value in [('writer_id','INVENTORY_ENGINE'),('authorization_reference','OTHER_AUTHORIZATION'),('acceptance_reference','OTHER_ACCEPTANCE')]:
                x,y,e,g=self.fixtures();g[i]=replace(g[i],**{field:value})
                with self.subTest(i=i,field=field):
                    with self.assertRaises(m.EvidenceError):report(x,y,reviewed_permissions=g)

    def test_wrong_captures_or_difference_hash_rejected(self):
        for i in range(3):
            for field in ('before_capture_sha256','after_capture_sha256','difference_sha256'):
                x,y,e,g=self.fixtures();g[i]=replace(g[i],**{field:'0'*64})
                with self.subTest(i=i,field=field):
                    with self.assertRaises(m.EvidenceError):report(x,y,reviewed_permissions=g)

    def test_wrong_after_file_fingerprints_rejected(self):
        for field in ('output_after_fingerprint','durability_after_fingerprint'):
            x,y,e,g=self.fixtures();e[field][1]+=1
            with self.subTest(field=field):
                with self.assertRaises(m.EvidenceError):report(x,y,reviewed_permissions=g)

    def test_extra_object_appearance_or_disappearance_rejected(self):
        for category in ('producer_state','configuration','code'):
            for appearing in (True,False):
                def mutate(a,b): (b if appearing else a)[category][PRIVATE]=fp()
                x,y,e,g=self.fixtures(mutate)
                with self.subTest(category=category,appearing=appearing):
                    with self.assertRaises(m.EvidenceError):report(x,y,reviewed_permissions=g)

    def test_missing_companion_files_or_permissions_rejected(self):
        for path in (self.output,self.durability):
            for side in (0,1):
                def mutate(a,b): (a if side==0 else b)['producer_state'].pop(path)
                x,y,e,g=self.fixtures(mutate)
                with self.subTest(path=path,side=side):
                    with self.assertRaises(m.EvidenceError):report(x,y,reviewed_permissions=g)
        x,y,e,g=self.fixtures()
        with self.assertRaises(m.EvidenceError):report(x,y,reviewed_permissions=g[:1])

    def test_unrelated_directory_cannot_use_publication_permission(self):
        def mutate(a,b):
            for obs in (a,b):obs['producer_state'][self.directory+'-other']=obs['producer_state'].pop(self.directory)
        x,y,e,g=self.fixtures(mutate)
        self.assertEqual(report(x,y,reviewed_permissions=g)['result'],'INSUFFICIENT_EVIDENCE')
        d=next(d for d in report(x,y)['object_differences'] if d['artifact_id'].startswith('OBJECT_'))
        g.append(m.ReviewedPermission(x.digest,y.digest,'PE5_OUTPUT_DIRECTORY',d['difference_sha256'],
            'PE5_COMPOSER','SYNTHETIC_PE5_AUTHORIZATION','SYNTHETIC_PE5_ACCEPTANCE',e))
        with self.assertRaises(m.EvidenceError):report(x,y,reviewed_permissions=g)

    def test_directory_security_identity_size_or_type_change_rejected(self):
        for field in range(7):
            def mutate(a,b): b['producer_state'][self.directory][field]+=1
            x,y,e,g=self.fixtures(mutate)
            with self.subTest(field=field):
                with self.assertRaises(m.EvidenceError):report(x,y,reviewed_permissions=g)

    def test_file_security_change_or_no_replacement_rejected(self):
        for path in (self.output,self.durability):
            for field in (0,1,2,3,4,5):
                def mutate(a,b):
                    if field==1:b['producer_state'][path][1]=a['producer_state'][path][1]
                    else:b['producer_state'][path][field]+=1
                x,y,e,g=self.fixtures(mutate)
                with self.subTest(path=path,field=field):
                    with self.assertRaises(m.EvidenceError):report(x,y,reviewed_permissions=g)

    def test_incomplete_capture_cannot_receive_permission(self):
        x,y,e,g=self.fixtures();y=replace(y,completeness='INCOMPLETE',error='OBSERVATION_ERROR')
        with self.assertRaises(m.EvidenceError):report(x,y,reviewed_permissions=g)

    def test_truncated_report_never_passes(self):
        x,y,e,g=self.fixtures()
        for kwargs in (dict(max_differences=1),dict(max_report_bytes=2048)):
            r=report(x,y,reviewed_permissions=g,**kwargs)
            self.assertEqual(r['result'],'INSUFFICIENT_EVIDENCE');self.assertTrue(r['differences_truncated'])

    def test_primary_or_protected_failure_preserved(self):
        x,y,e,g=self.fixtures()
        r=report(x,y,reviewed_permissions=g,primary_outcome=dict(status='FAIL',stage='SINGLE_EVALUATION'),protected_inspection_outcome=dict(status='FAIL',stage='AFTER_STATE'))
        self.assertEqual(r['result'],'FAIL');self.assertEqual(r['primary_outcome']['status'],'FAIL');self.assertEqual(r['protected_inspection_outcome']['status'],'FAIL')

    def test_permission_packet_not_allowed_on_unrelated_artifacts(self):
        x,y=changed(INVENTORY);d=report(x,y)['object_differences'][0]
        g=m.ReviewedPermission(x.digest,y.digest,d['artifact_id'],d['difference_sha256'],
            'INVENTORY_ENGINE','SYNTHETIC_AUTHORIZATION','SYNTHETIC_ACCEPTANCE',{})
        with self.assertRaises(m.EvidenceError):report(x,y,reviewed_permissions=[g])

    def test_file_permissions_alone_never_waive_directory(self):
        x,y,e,g=self.fixtures()
        self.assertEqual(report(x,y,reviewed_permissions=g[1:])['result'],'INSUFFICIENT_EVIDENCE')

    def test_external_digest_must_match_hash_if_after_capture_contains_one(self):
        for path in (self.output,self.durability):
            def mutate(a,b):b['producer_state'][path]=[b['producer_state'][path],'0'*64]
            x,y,e,g=self.fixtures(mutate)
            with self.subTest(path=path):
                with self.assertRaises(m.EvidenceError):report(x,y,reviewed_permissions=g)

    def test_private_fields_cannot_be_smuggled_into_transaction_packet(self):
        x,y,e,g=self.fixtures();e['PRIVATE_HOSTNAME']='PRIVATE_DATA'
        with self.assertRaises(m.EvidenceError):report(x,y,reviewed_permissions=g)


if __name__ == '__main__': unittest.main()
