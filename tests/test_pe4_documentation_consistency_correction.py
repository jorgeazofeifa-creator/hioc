"""Exact documentation successor; historical production authority is never refreshed."""
import ast
import copy
import difflib
import hashlib
import json
import os
import subprocess
import unittest
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREDECESSOR = '017686549acb27dbf7a8ad3577d0f84cf9f3f066'
RECORD = 'governance/pe4/pe4-documentation-consistency-correction.json'
SCHEMA = RECORD.replace('.json', '.schema.json')

def git(*args):
    return subprocess.check_output(['git', '--no-optional-locks', *args], cwd=ROOT,
                                   env=dict(os.environ, GIT_OPTIONAL_LOCKS='0'))

def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False) + '\n').encode('utf8')

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def blob(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()

def closed_schema(value):
    if type(value) is dict:
        return dict(type='object', additionalProperties=False, required=sorted(value),
                    properties={k:closed_schema(v) for k,v in sorted(value.items())})
    if type(value) is list:
        return dict(type='array', minItems=len(value), maxItems=len(value),
                    prefixItems=[closed_schema(v) for v in value], items=False)
    return {'const':value}

def validate(value, schema):
    if 'const' in schema:
        if type(value) is not type(schema['const']) or value != schema['const']:
            raise ValueError('exact typed constant mismatch')
    elif schema['type'] == 'object':
        if type(value) is not dict or set(value) != set(schema['required']):
            raise ValueError('closed object mismatch')
        for key in value: validate(value[key], schema['properties'][key])
    elif schema['type'] == 'array':
        if type(value) is not list or len(value) != schema['minItems'] or len(value) != schema['maxItems']:
            raise ValueError('exact array boundary mismatch')
        for item, child in zip(value, schema['prefixItems']): validate(item, child)
    else: raise ValueError('unknown schema contract')

@lru_cache(maxsize=None)
def historical(path):
    return git('show', PREDECESSOR + ':' + path)

def stage(path):
    raw = git('show', ':' + path)
    if (ROOT/path).read_bytes().replace(b'\r\n', b'\n') != raw:
        raise ValueError('stage/worktree mismatch')
    return raw

def _history(record, path):
    if path not in record['documentation_paths']: raise ValueError('unknown document')
    old = historical(path).decode('utf8').splitlines(keepends=True)
    candidate = list(old)
    operations = record['document_operations'][path]
    ranges = record['authorized_document_ranges'][path]
    for operation in sorted(operations, key=lambda x:x['start_line'], reverse=True):
        start,end = operation['start_line'],operation['end_line']
        if [start,end] not in ranges: raise ValueError('operation outside exact audit range')
        original = ''.join(old[start-1:end]).rstrip('\n')
        if digest(original.encode('utf8')) != operation['original_sha256']:
            raise ValueError('original finding section changed')
        candidate[start-1:end] = [operation['replacement'] + '\n']
    # Reconstruct from fixed predecessor and exact finding-range operations.
    # This protects every untouched byte, without ambiguous blank-line LCS alignment.
    if ''.join(candidate).encode('utf8') != stage(path):
        raise ValueError('document edit outside exact finding operations: '+path)

def validate_candidate(record, schema):
    validate(record, schema)
    expected_schema = {'$schema':'https://json-schema.org/draft/2020-12/schema',
                       'title':'PE-4 documentation consistency correction', **closed_schema(record)}
    if schema != expected_schema: raise ValueError('schema contract drift')
    if record['predecessor_commit'] != PREDECESSOR or git('rev-parse','HEAD').decode().strip() != PREDECESSOR:
        raise ValueError('wrong predecessor')
    if record['finding_count'] != 49 or len(record['findings']) != 49:
        raise ValueError('wrong finding boundary')
    if len(record['documentation_paths']) != 17 or len(record['existing_binding_tests']) != 12 or len(record['authorized_paths']) != 33:
        raise ValueError('wrong path cardinality')
    if len(set(record['authorized_paths'])) != 33 or sorted(record['documentation_paths']+record['existing_binding_tests']+record['new_artifacts']) != record['authorized_paths']:
        raise ValueError('wrong exact path union')
    if record['lifecycle'] != dict(pe4='PASS/CLOSED',public_projection='PASS/CLOSED',phase7a='ACTIVE',pe5='NOT_STARTED'):
        raise ValueError('wrong lifecycle')
    changed = set(git('diff','HEAD','--name-only').decode().splitlines())
    changed.update(git('ls-files','--others','--exclude-standard').decode().splitlines())
    if changed != set(record['authorized_paths']): raise ValueError('unexplained candidate path')
    entries = git('ls-files','--stage').decode().splitlines()
    if any(line.split('\t',1)[0].split()[2] != '0' for line in entries): raise ValueError('nonzero index stage')
    expected = set(record['authorized_paths']) - {RECORD, SCHEMA}
    if {i['path'] for i in record['artifacts']} != expected: raise ValueError('artifact boundary mismatch')
    for item in record['artifacts']:
        raw=stage(item['path'])
        if digest(raw) != item['sha256'] or blob(raw) != item['git_blob']: raise ValueError('current artifact identity mismatch')
    for item in record['preserved_governance']:
        raw=historical(item['path'])
        if digest(raw) != item['sha256'] or blob(raw) != item['git_blob'] or stage(item['path']) != raw:
            raise ValueError('historical governance rewritten')
    if any(record['codex_activity'].values()) or record['runtime_behavior_changed'] or record['production_evidence_changed']:
        raise ValueError('unsupported authority or activity')
    for path in record['documentation_paths']: _history(record,path)
    for finding in record['findings']:
        if finding['resolution'] != 'RESOLVED' or finding['expected_text'] not in stage(finding['path']).decode('utf8'):
            raise ValueError('unresolved finding '+finding['finding_id'])
    master=stage('docs/HIOC_MASTER_PLAN.md').decode('utf8')
    current=master.split('## Current Objective',1)[1].split('### Historical',1)[0]
    for phrase in ['PE-4 Documentation Consistency Correction','PE-4 PASS/CLOSED','Public Projection PASS/CLOSED','Phase 7A ACTIVE','PE-5 NOT_STARTED','OPERATOR_SUPPLIED','017686549acb27dbf7a8ad3577d0f84cf9f3f066']:
        if phrase not in current: raise ValueError('current Master consistency missing')
    document=stage('docs/PE4_DOCUMENTATION_CONSISTENCY_CORRECTION.md').decode('utf8')
    for phrase in ['Evidence Report','PASS_CORRECTIONS_REQUIRED','74','49','17','eight','OPERATOR_SUPPLIED','no production access','stash preserved','Validation Results','PE-5 NOT_STARTED']:
        if phrase not in document: raise ValueError('missing correction evidence')
    return record

@lru_cache(maxsize=1)
def successor():
    raw=stage(RECORD);schema_raw=stage(SCHEMA)
    record=json.loads(raw);schema=json.loads(schema_raw)
    if canonical(record)!=raw or canonical(schema)!=schema_raw: raise ValueError('noncanonical successor')
    return validate_candidate(record,schema)

def current_binding(path):
    record=successor()
    item=next((x for x in record['artifacts'] if x['path']==path),None)
    if item is None: raise ValueError('path outside current artifact map')
    raw=stage(path)
    if digest(raw)!=item['sha256'] or blob(raw)!=item['git_blob']: raise ValueError('current identity mismatch')
    return item

def verify_document_history(path):
    _history(successor(),path)

class DocumentationConsistencyCorrectionTests(unittest.TestCase):
    def test_exact_closed_candidate_and_stage_identities(self): successor()
    def test_historical_governance_preserved(self):
        for item in successor()['preserved_governance']: self.assertEqual(stage(item['path']),historical(item['path']))
    def test_all_49_findings_and_exact_33_paths(self):
        record=successor();self.assertEqual(len({x['finding_id'] for x in record['findings']}),49)
        self.assertEqual(set(x['finding_id'] for x in record['findings']),{'S%02d'%i for i in range(1,50)})
    def test_all_current_document_edits_are_within_audit_ranges(self):
        for path in successor()['documentation_paths']: verify_document_history(path)
    def test_no_runtime_or_production_or_pe5_authority(self):
        self.assertFalse(any(successor()['codex_activity'].values()))
        self.assertEqual(successor()['lifecycle']['pe5'],'NOT_STARTED')
    def test_reject_extra_path_and_wrong_predecessor(self):
        record=successor();schema=json.loads(stage(SCHEMA))
        for key,value in [('predecessor_commit','0'*40),('finding_count',48),('authorized_paths',record['authorized_paths']+['pi4/unapproved.py'])]:
            bad=copy.deepcopy(record);bad[key]=value
            with self.assertRaises(ValueError): validate_candidate(bad,schema)
    def test_reject_stale_artifact_and_refreshed_history(self):
        for key in ['artifacts','preserved_governance']:
            bad=copy.deepcopy(successor());bad[key][0]['sha256']='0'*64
            with self.assertRaises(ValueError): validate_candidate(bad,json.loads(stage(SCHEMA)))
    def test_reject_open_schema_and_extra_property(self):
        record=successor();schema=json.loads(stage(SCHEMA));schema['additionalProperties']=True
        with self.assertRaises(ValueError): validate_candidate(record,schema)
        with self.assertRaises(ValueError): validate(dict(record,unreviewed=True),json.loads(stage(SCHEMA)))
    def test_original_four_path_exception_record_is_not_extended(self):
        path='governance/pe4/pe4-ha-association-public-projection-test-binding-correction.json'
        self.assertEqual(stage(path),historical(path));self.assertEqual(len(json.loads(stage(path))['binding_exception_paths']),4)
    def test_new_test_is_bytecode_free_parseable(self):
        ast.parse(stage('tests/test_pe4_documentation_consistency_correction.py').decode('utf8'))

if __name__=='__main__': unittest.main()
