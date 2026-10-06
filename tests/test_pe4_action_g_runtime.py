import contextlib
import io
import unittest
from unittest import mock
from pathlib import PurePosixPath

from tools import hioc_pe4_action_g as G


def faithful_f_transaction():
    """Serialize real F journal records; never run F's executor or preflight."""
    from tests.test_pe4_action_f_runtime import Memory, bindings
    backend=Memory()
    bound=bindings();bound['current_consumer']=G.F_CONSUMER
    state=G.F.initial_state();state['recovery']=True
    journal=G.F.Journal(backend,G.F_ID,bound,state)
    journal.append('PREPARED')
    for operation in G.F.OPERATIONS:
        journal.append(operation+'_INTENT')
        backend.confirm(operation,bound)
        if operation=='CLIENT':state['publication']='CLIENT_ONLY'
        if operation=='ENVIRONMENT':state['publication']='ENVIRONMENT_PUBLISHED'
        if operation=='ACTIVE_SWITCH':state['publication']='ACTIVE_SWITCHED'
        journal.append(operation+'_CONFIRMED')
    journal.append('POST_VERIFIED')
    state['evidence']='UNCONFIRMED'
    result=G.F.record(journal.document('RESULT'))
    backend.files['result.json']=result
    digest=G.H.digest(result)
    state['evidence']='CONFIRMED'
    journal.append('RESULT_REFERENCE',digest)
    state['publication']='COMPLETE';state['recovery']=False
    journal.append('COMMITTED',digest)
    journal.verify(result)
    return backend.files,bound


def reseal(files):
    """Reseal synthetic hashes so each negative test reaches semantic checks."""
    previous='NONE'
    for i in range(14):
        name=f'{i:04}.json';doc=G.H.parse(files[name],'STAGED_INPUT')
        doc['previous_record_sha256']=previous
        if i==12:
            result=G.H.parse(files['result.json'],'STAGED_INPUT')
            result['previous_record_sha256']=previous
            files['result.json']=G.H.canonical(result)
        if i>=12:doc['result_sha256']=G.H.digest(files['result.json'])
        files[name]=G.H.canonical(doc);previous=G.H.digest(files[name])


class FJournalRecoveryTests(unittest.TestCase):
    def validate(self,files):
        # Production paths are POSIX; preserve their spelling on Windows.
        with mock.patch.object(G,'FINAL',PurePosixPath(G.FINAL.as_posix())), mock.patch.object(G,'CLIENT',PurePosixPath(G.CLIENT.as_posix())):
            return G.validate_f(files,G.H.digest(files['result.json']),G.H.digest(files['0013.json']))

    def mutate(self,files,name,field,value):
        doc=G.H.parse(files[name],'STAGED_INPUT');doc[field]=value
        files[name]=G.H.canonical(doc);reseal(files)

    def test_successful_real_f_serialization_and_incomplete_recovery_states(self):
        files,bound=faithful_f_transaction()
        for i in range(13):
            self.assertIs(G.H.parse(files[f'{i:04}.json'],'STAGED_INPUT')['recovery_required'],True)
        self.assertIs(G.H.parse(files['result.json'],'STAGED_INPUT')['recovery_required'],True)
        self.assertIs(G.H.parse(files['0013.json'],'STAGED_INPUT')['recovery_required'],False)
        self.assertEqual(self.validate(files),bound)

    def test_committed_recovery_true_is_rejected(self):
        files,_=faithful_f_transaction();self.mutate(files,'0013.json','recovery_required',True)
        with self.assertRaises(G.Failure):self.validate(files)

    def test_every_incomplete_record_must_require_recovery(self):
        for name in [*(f'{i:04}.json' for i in range(13)),'result.json']:
            with self.subTest(name=name):
                files,_=faithful_f_transaction();self.mutate(files,name,'recovery_required',False)
                with self.assertRaises(G.Failure):self.validate(files)

    def test_publication_and_evidence_progression_are_exact(self):
        for name in [*(f'{i:04}.json' for i in range(14)),'result.json']:
            for field in ('publication_state','evidence_state'):
                with self.subTest(name=name,field=field):
                    files,_=faithful_f_transaction();old=G.H.parse(files[name],'STAGED_INPUT')[field]
                    alternatives=('NONE','COMPLETE') if field=='publication_state' else ('NOT_CREATED','CONFIRMED')
                    self.mutate(files,name,field,next(v for v in alternatives if v!=old))
                    with self.assertRaises(G.Failure):self.validate(files)

    def test_exact_result_and_committed_digests_remain_mandatory(self):
        files,_=faithful_f_transaction();r=G.H.digest(files['result.json']);c=G.H.digest(files['0013.json'])
        for rd,cd in [('0'*64,c),(r,'0'*64)]:
            with self.assertRaises(G.Failure):G.validate_f(files,rd,cd)
        with self.assertRaises(G.Failure):G.validate_f(files)  # Synthetic bytes cannot satisfy production pins.

    def test_chain_order_sequence_and_file_set_remain_mandatory(self):
        for field,value in [('previous_record_sha256','0'*64),('event','CLIENT_CONFIRMED'),('sequence',3)]:
            files,_=faithful_f_transaction();doc=G.H.parse(files['0001.json'],'STAGED_INPUT');doc[field]=value
            files['0001.json']=G.H.canonical(doc)
            if field!='previous_record_sha256':reseal(files)
            with self.assertRaises(G.Failure):self.validate(files)
        for extra in (False,True):
            files,_=faithful_f_transaction()
            if extra:files['extra.json']=b'{}\n'
            else:files.pop('0000.json')
            with self.assertRaises(G.Failure):self.validate(files)

    def test_result_reference_and_pass_contracts_remain_mandatory(self):
        for name in ('0000.json','0012.json','0013.json','result.json'):
            for field,value in [('rollback_recommended',True),('error_code','MISMATCH'),('failure_stage','HANDOFF')]:
                files,_=faithful_f_transaction();self.mutate(files,name,field,value)
                with self.assertRaises((G.Failure,G.H.Failure)):self.validate(files)
        files,_=faithful_f_transaction();doc=G.H.parse(files['0012.json'],'STAGED_INPUT')
        doc['result_sha256']='0'*64;files['0012.json']=G.H.canonical(doc)
        with self.assertRaises(G.Failure):self.validate(files)


class ActionGRuntimeTests(unittest.TestCase):
    def test_entrypoint_is_thin_and_controlled(self):
        source = open("tools/hioc-pe4-runtime-preflight.py", encoding="utf-8").read()
        self.assertIn("from hioc_pe4_action_g import cli", source)
        self.assertIn("--governance-commit", open("tools/hioc_pe4_action_g.py", encoding="utf-8").read())

    def test_invalid_arguments_fail_before_backend(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            rc = G.cli(["--governance-commit", "bad"], lambda: self.fail("backend"))
        self.assertEqual(rc, 2)
        self.assertIn("RESULT=FAIL", output.getvalue())

    def test_no_shared_probe_or_lifecycle_executor(self):
        source = open("tools/hioc_pe4_action_g.py", encoding="utf-8").read()
        self.assertNotIn("CAPABILITY_PROBE", source)
        self.assertNotIn("verify_repository(", source)
        self.assertNotIn("hioc-pe4-runtime-rollback.py", source)

    def test_network_and_credentials_are_explicitly_denied(self):
        with self.assertRaises(RuntimeError):
            G.deny_network()
        with self.assertRaises(RuntimeError):
            G.deny_credentials()

    def test_f_constants_are_pinned(self):
        self.assertEqual(G.F_ID, "17fc3e0580ff007cdcd619ed2e2d3b34")
        self.assertEqual(G.F_RESULT, "d647c7b2241d7800a3c819cf86459e2be95c3ef58581d5ffef2dbf5bd1190941")
        self.assertEqual(G.F_COMMITTED, "24bb64cc8d885297e5696ddd733ec0dfab4b28a24e18a6996b667c186f2016e9")

    def test_bounded_output_rejects_overflow(self):
        with self.assertRaises(G.Failure) as caught:
            G.bounded(["/usr/bin/python3", "-I", "-B", "-S", "-c", "print('x'*10000)"], "PROBE", limit=100)
        self.assertIn(caught.exception.code, {"OUTPUT_LIMIT", "IO_FAILED"})
