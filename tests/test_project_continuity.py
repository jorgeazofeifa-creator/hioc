"""Cold-start recovery and fail-closed continuity; no production or fixture mutations."""
import ast
import copy
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import hioc_project_continuity as c


class ContinuityTests(unittest.TestCase):
    def record(self): return json.loads(c.raw(c.RECORD))
    def altered(self, key, value):
        r = self.record(); r[key] = value
        with self.assertRaises(ValueError): c.check_record(r, c.schema_for(r))

    def test_valid_current_record_and_schema(self):
        self.assertEqual(c.validate_current()["product"]["accepted_commit"], c.BASE)

    def test_fresh_session_from_entry_point_without_chat(self):
        entry = c.raw(c.CONTEXT).decode()
        self.assertTrue(150 <= len(entry.splitlines()) <= 250)
        self.assertIn(c.RECORD, entry)
        result = c.recover()
        self.assertIn("operator", result["mission"])
        self.assertEqual(result["product"], c.PRODUCT)
        self.assertEqual(result["transition"]["sequence"], c.TRANSITION["sequence"])
        self.assertFalse(result["product"]["next_authorized"])
        self.assertEqual(result["boundary"]["codex"], "WINDOWS_REPOSITORY_ONLY")
        self.assertEqual(result["boundary"]["pi3_execution"], "OPERATOR_ONLY_SEPARATE_AUTHORIZATION")
        self.assertEqual(result["production_state"], "UNKNOWN")
        self.assertTrue("NO_NEXT_STAGE" in result["next_action"] or "STOP_BEFORE_T2_OR_PE62" in result["next_action"])
        self.assertIn("HISTORICAL_OBSERVATION", self.record()["last_verified"]["limitation"])

    def test_non_windows_current_observation_is_not_mislabeled(self):
        with patch.object(c.os,"name","posix"),self.assertRaisesRegex(ValueError,"WINDOWS_REPOSITORY_ONLY"):c.validate_current()

    def test_live_observations_are_new_and_snapshot_has_no_live_claim(self):
        result=c.recover();observed=result["observed_repository"]
        self.assertEqual(observed["evidence_class"],"DIRECT_OBSERVATION")
        self.assertEqual(observed["scope"],"WINDOWS_REPOSITORY")
        self.assertEqual(observed["head"],c.git("rev-parse","HEAD").decode().strip())
        self.assertEqual(observed["origin_main"],c.git("rev-parse","origin/main").decode().strip())
        self.assertEqual(observed["independent_github_verification"],"NOT_ESTABLISHED_BY_LOCAL_TOOL")
        self.assertFalse(self.record()["recovery"]["accepted_unpublished_candidate"])

    def test_boolean_observation_cannot_be_replaced_by_number(self):
        observed=self.record()["last_verified"];observed["clean"]=1
        self.altered("last_verified",observed)

    def test_all_local_entry_links_resolve_to_authority(self):
        for link in re.findall(r"\]\(([^)]+)\)", c.raw(c.CONTEXT).decode()):
            if not link.startswith("https:"):
                self.assertTrue((c.ROOT / "docs" / link.split("#")[0]).is_file(), link)
        self.assertEqual(self.record()["authorities"], c.OWNERS)

    def test_schema_versions_missing_extra_and_wrong_types_rejected(self):
        r = self.record(); s = c.schema_for(r)
        for bad in [dict(r, schema_version="2.0"), dict(r, extra=True), {k:v for k,v in r.items() if k!="product"}]:
            with self.subTest(bad=sorted(bad)), self.assertRaises(ValueError): c.check_record(bad,s)
        self.altered("schema_version", 1)

    def test_contradictory_product_and_pe62_advancement_rejected(self):
        for key,value in [("accepted_checkpoint","PE-6.2 COMPLETE/PASS"),("next_authorized",True),("phase","Phase 7B ACTIVE"),("pe6_production_deployed_at_closure",True),("accepted_commit","0"*40)]:
            product=dict(c.PRODUCT);product[key]=value
            self.altered("product",product)

    def test_wrong_repository_and_document_ownership_rejected(self):
        self.altered("repository","https://example.invalid/other")
        owners=dict(c.OWNERS);owners["product_plan"]="docs/PROJECT.md"
        self.altered("authorities",owners)

    def test_unsupported_production_and_unknown_promotion_rejected(self):
        for key,value in [("production_access",True),("production_current_state","HEALTHY"),("pi3_access",True)]:
            boundary=dict(c.BOUNDARY);boundary[key]=value
            self.altered("boundary",boundary)
        self.altered("unknowns",[])
        observed=self.record()["last_verified"];observed["evidence_class"]="DIRECT_PRODUCTION_OBSERVATION"
        self.altered("last_verified",observed)

    def test_invalid_candidate_and_transition_authority_rejected(self):
        recovery=dict(c.RECOVERY);recovery["accepted_unpublished_candidate"]=True
        self.altered("recovery",recovery)
        transition=dict(c.TRANSITION);transition["next_stage_authorized"]=True
        self.altered("transition",transition)

    def test_sensitive_material_is_rejected(self):
        examples=[b"-----BEGIN "+b"PRIVATE KEY-----",b"pass"+b"word="+b"SYNTHETIC_ONLY",b"api_"+b"key: SYNTHETIC_ONLY",b"mqtt"+b"://"+b"fixture:fixture"+b"@invalid"]
        for data in examples:
            with self.subTest(data=data), self.assertRaisesRegex(ValueError,"SENSITIVE_INFORMATION"): c.privacy(data)

    def test_new_unauthorized_path_after_success_is_rejected(self):
        c.recover();original=c.git
        def extra(*args):
            value=original(*args)
            return value+b"UNAUTHORIZED_SYNTHETIC.txt\n" if args==("ls-files","--others","--exclude-standard") else value
        with patch.object(c,"git",extra), self.assertRaisesRegex(ValueError,"UNEXPECTED_PATH"):c.recover()

    def test_current_artifact_and_protected_bytes_rechecked(self):
        c.recover();original=c.raw
        for path,code in [(c.CONTEXT,"CURRENT_ARTIFACT_IDENTITY"),("pi4/lib/hioc/inventory.py","PROTECTED_BASELINE_ARTIFACT")]:
            with self.subTest(path=path),patch.object(c,"raw",lambda p,path=path:original(p)+b"changed" if p==path else original(p)),self.assertRaisesRegex(ValueError,code):c.recover()

    def test_missing_context_or_authority_fails(self):
        original=c.raw
        def missing(path):
            if path==c.CONTEXT:raise FileNotFoundError(path)
            return original(path)
        with patch.object(c,"raw",missing),self.assertRaises(FileNotFoundError):c.recover()

    def test_stale_commit_and_repository_identity_fail(self):
        with self.assertRaises(subprocess.CalledProcessError):c.validate_snapshot(c.BASE)
        original=c.git
        def stale(*args):
            if args[:1]==("merge-base",):return b"0"*40+b"\n"
            return original(*args)
        with patch.object(c,"git",stale),self.assertRaisesRegex(ValueError,"STALE_BASELINE"):c.recover()
        with patch.object(c,"git",lambda *args:b"https://example.invalid/other" if args==("remote","get-url","origin") else original(*args)),self.assertRaisesRegex(ValueError,"REPOSITORY_IDENTITY"):c.recover()

    def test_record_schema_current_bytes_not_cached(self):
        c.recover();original=c.raw
        for path in [c.RECORD,c.SCHEMA]:
            with self.subTest(path=path),patch.object(c,"raw",lambda p,path=path:original(p)+b" " if p==path else original(p)),self.assertRaisesRegex(ValueError,"CANONICAL_HANDOFF"):c.recover()

    def test_changed_or_unmerged_index_is_rejected(self):
        original=c.git
        for stage in ["0","1"]:
            def changed(*args):
                value=original(*args)
                if args==("ls-files","--stage"):
                    rows=value.decode().splitlines()
                    rows=[row.split()[0]+" "+"0"*40+" "+stage+"\t"+c.CONTEXT if row.endswith("\t"+c.CONTEXT) else row for row in rows]
                    return ("\n".join(rows)+"\n").encode()
                return value
            with self.subTest(stage=stage),patch.object(c,"git",changed),self.assertRaisesRegex(ValueError,"STAGED_ARTIFACT_IDENTITY|UNMERGED_INDEX"):c.recover()

    def test_false_clean_unpublished_transition_rejected(self):
        original=c.git
        def false_clean(*args):
            if args==("status","--porcelain"):return b""
            if args in [("rev-parse","HEAD"),("rev-parse","origin/main")]:return c.BASE.encode()
            if args==("rev-list","--left-right","--count","HEAD...origin/main"):return b"0 0"
            return original(*args)
        with patch.object(c,"git",false_clean),self.assertRaisesRegex(ValueError,"CANDIDATE_TRANSITION"):c.recover()

    def test_snapshot_does_not_read_working_tree(self):
        commit="a"*40
        entries={}
        for row in c.git("ls-files","--stage").decode().splitlines():
            info,path=row.split("\t",1);mode,oid,stage=info.split();entries[path]=(mode,oid)
        data={p:c.raw(p) for p in entries}
        encoded=b"".join((mode+" blob "+oid+"\t"+p).encode()+b"\0" for p,(mode,oid) in sorted(entries.items()))
        original=c.git
        def snapshot(*args):
            if args==("ls-tree","-r","-z",commit):return encoded
            if args[:1]==("merge-base",):return c.BASE.encode()
            if args[:1]==("show",) and args[1].startswith(commit+":"):return data[args[1][41:]]
            return original(*args)
        with patch.object(c,"git",snapshot),patch.object(c,"raw",side_effect=AssertionError("live path forbidden")):
            result=c.recover(commit)
        self.assertEqual(result["live_state"],"NOT_OBSERVED")
        self.assertIsNone(result["observed_repository"])
        self.assertEqual(result["result"],"PASS_HISTORICAL_SNAPSHOT")

    def test_public_legacy_binding_entry_points_are_fresh(self):
        import test_pe6_classification_implementation as g
        import test_pe6_classification_contract_design as design
        import test_pe4_documentation_consistency_correction as old
        g.implementation_successor();original=c.git
        def extra(*args):
            value=original(*args)
            return value+b"UNAUTHORIZED_SYNTHETIC.txt\n" if args==("ls-files","--others","--exclude-standard") else value
        calls=[g.implementation_successor,lambda:g.implementation_binding("docs/HIOC_MASTER_PLAN.md"),lambda:design.design_binding("docs/HIOC_MASTER_PLAN.md"),old.current_artifacts]
        with patch.object(c,"git",extra):
            for call in calls:
                with self.subTest(call=call),self.assertRaisesRegex(ValueError,"UNEXPECTED_PATH"):call()

    def test_accepted_pe61_original_validator_and_classes_preserved(self):
        path="tests/test_pe6_classification_implementation.py"
        old=ast.parse(c.git("show",c.BASE+":"+path));current=ast.parse(c.raw(path))
        classes=lambda t:[ast.dump(n,include_attributes=False) for n in t.body if isinstance(n,ast.ClassDef)]
        self.assertEqual(classes(old),classes(current))
        fn=lambda t:next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name=="validate_implementation")
        self.assertEqual(ast.dump(fn(old)),ast.dump(fn(current)))
        self.assertEqual(len(c.historical_implementation_tests(unittest.defaultTestLoader)._tests),20)

    def test_shared_runtime_guard_keeps_original_checks_and_exact_additions(self):
        import test_pe5_service_association_caller as prior
        path="tests/test_pe5_service_association_caller.py"
        old,new=ast.parse(c.git("show",c.BASE+":"+path)),ast.parse(c.raw(path))
        classes=lambda tree:[ast.dump(n,include_attributes=False) for n in tree.body if isinstance(n,ast.ClassDef)]
        self.assertEqual(classes(old),classes(new))
        fn=lambda tree:next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=="assert_historical_runtime_tree")
        before=[ast.dump(n,include_attributes=False) for n in fn(old).body]
        after=[ast.dump(n,include_attributes=False) for n in fn(new).body]
        self.assertEqual(len(after),len(before)+1)
        self.assertEqual([n for n in after if n in before],before)
        prior.assert_historical_runtime_tree("c7db29f795909d7926e36c02f1166034bcebb8b0",["pi4","release","tools","requirements-pe4.lock"])

    def test_shared_runtime_guard_rejects_existing_or_unapproved_tool(self):
        import test_pe5_service_association_caller as prior
        original=prior.git
        def existing(*args):
            if args[:3]==("ls-tree","--name-only",c.BASE) and args[-1].startswith("tools/"):return (args[-1]+"\n").encode()
            return original(*args)
        with patch.object(prior,"git",existing),self.assertRaisesRegex(ValueError,"existing runtime cannot be exempted"):
            prior.assert_historical_runtime_tree("c7db29f795909d7926e36c02f1166034bcebb8b0",["tools"])
        def unapproved(*args):
            value=original(*args)
            return value+b"tools/unapproved-synthetic.py\n" if args[:2]==("diff","--name-only") else value
        with patch.object(prior,"git",unapproved),self.assertRaisesRegex(ValueError,"historical runtime modified outside exact additive successors"):
            prior.assert_historical_runtime_tree("c7db29f795909d7926e36c02f1166034bcebb8b0",["tools"])

    def test_original_authority_text_and_product_history_preserved(self):
        self.assertTrue(c.raw("docs/HIOC_MASTER_PLAN.md").startswith(c.git("show",c.BASE+":docs/HIOC_MASTER_PLAN.md")))
        issue=c.raw("governance/continuity/engineering-transition-issue-6.md").decode()
        authorization=c.raw("governance/continuity/t1-authorization.md").decode()
        self.assertIn("T5 - Formal consolidation",issue)
        self.assertIn("## 13. Required Evidence Report",authorization)
        self.assertIn("NO ASSUMPTIONS. EVER.",authorization)

if __name__=="__main__":unittest.main()
