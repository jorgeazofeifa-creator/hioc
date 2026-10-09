"""No Assumptions law: material production facts require evidence and live recheck."""
import unittest
from test_pe4_ha_public_projection_deploy import D,BaselineNativeGateTests
class NoAssumptionsTests(unittest.TestCase):
    def test_unknown_and_expected_production_facts_rejected(self):
        for fact in ({},{'sha256':D.OLD_ENGINE},{'sha256':D.OLD_ENGINE,'provenance':'EXPECTED'}, {'sha256':D.OLD_ENGINE,'provenance':'UNKNOWN'}, {'sha256':D.OLD_ENGINE,'provenance':'IMMUTABLE_REPOSITORY_FACT'}):
            with self.subTest(fact=fact),self.assertRaises(D.Failure):D.evidence_gate(fact,production=True)
    def test_source_identity_only_qualifies_as_repository_fact(self):
        fact={'sha256':D.OLD_ENGINE,'provenance':'IMMUTABLE_REPOSITORY_FACT'}
        self.assertEqual(D.evidence_gate(fact),D.OLD_ENGINE)
        with self.assertRaises(D.Failure):D.evidence_gate(fact,production=True)
    def test_operator_label_retained_and_no_codex_observation_inferred(self):
        for label in ('DIRECT_OBSERVATION','CRYPTOGRAPHICALLY_BOUND_OBSERVATION','OPERATOR_SUPPLIED'):
            fact={'sha256':D.OLD_ENGINE,'provenance':label}
            self.assertEqual(D.evidence_gate(fact,production=True),D.OLD_ENGINE)
            self.assertEqual(fact['provenance'],label)
    def test_absence_of_evidence_cannot_prove_absence(self):
        for value in ({'provenance':'DIRECT_OBSERVATION'}, {'provenance':'OPERATOR_SUPPLIED','sha256':None}):
            with self.assertRaises(D.Failure):D.evidence_gate(value,production=True)
    def test_observed_conflict_overrides_receipt_plan_no_auto_adoption(self):
        fixture=BaselineNativeGateTests();ops,files,_=fixture.fixture();receipt=ops.observe_baseline()
        saved=__import__('copy').deepcopy(receipt)
        files[D.SET[2][0]]=b'new production value'
        with self.assertRaises(D.Failure):ops.baseline(receipt)
        self.assertEqual(receipt,saved)
    def test_law_is_closed_true_semantic_contract(self):
        from pathlib import Path
        import json
        from test_pe4_ha_public_projection_deploy import ROOT
        record=json.loads((ROOT/D.RECORD).read_bytes());schema=json.loads((ROOT/D.SCHEMA).read_bytes())
        self.assertEqual(record['law'],D.NO_ASSUMPTIONS_LAW)
        for key in D.NO_ASSUMPTIONS_LAW:
            changed=__import__('copy').deepcopy(record);changed['law'][key]=False
            with self.subTest(rule=key),self.assertRaises(D.Failure):D.check_closed(changed,schema)
class NoAssumptionsDocumentTests(unittest.TestCase):
    def test_master_authority_and_focused_governance_share_law(self):
        from test_pe4_ha_public_projection_deploy import ROOT
        texts=[(ROOT/p).read_text(encoding='utf8') for p in ('docs/HIOC_MASTER_PLAN.md','docs/PE4_HOME_ASSISTANT_ASSOCIATION_PUBLIC_PROJECTION_DEPLOYMENT_BASELINE_CORRECTION.md')]
        for text in texts:
            for phrase in ('NO ASSUMPTIONS','Any unverified material fact is UNKNOWN','Repository state cannot prove production state','Unknown prerequisites block dependent mutation','Evidence conflicts override plans','Assumptions discovered in governance are defects'):
                self.assertIn(phrase,text)
if __name__=='__main__':unittest.main()
