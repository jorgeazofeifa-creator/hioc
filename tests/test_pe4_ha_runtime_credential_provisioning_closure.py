"""Repository-only governance of operator-supplied credential evidence."""
import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import unittest
from tests.test_pe4_0c_association_contract import validate_schema

ROOT=Path(__file__).resolve().parents[1]
BASE="d089be8e76a37084470336f1d999f1567f60d19f"
PATH=ROOT/"governance/pe4/pe4-ha-runtime-credential-provisioning-closure.json"
SCHEMA=PATH.with_suffix(".schema.json")
RECORD=json.loads(PATH.read_bytes())
NEXT="PE-4 Home Assistant Association Adapter Implementation"


def git(*args):return subprocess.check_output(["git",*args],cwd=ROOT)


class CredentialClosureTests(unittest.TestCase):
    def test_canonical_closed_schema(self):
        schema=json.loads(SCHEMA.read_bytes())
        for path in (PATH,SCHEMA):
            raw=path.read_bytes()
            self.assertEqual(raw,(json.dumps(json.loads(raw),sort_keys=True,separators=(",",":"))+"\n").encode())
        validate_schema(RECORD,schema)
        for changes in ({"status":"NOT_COMPLETE"},{"authentication_attempted":True},{"codex_pi3_access":True},{"token":"TEST_ONLY_FORBIDDEN_FIELD"},{"runtime_readability":False}):
            invalid=copy.deepcopy(RECORD);invalid.update(changes)
            with self.assertRaises(ValueError):validate_schema(invalid,schema)
        for key in RECORD:
            invalid=copy.deepcopy(RECORD);del invalid[key]
            with self.assertRaises(ValueError):validate_schema(invalid,schema)

    def test_history_and_tool_bindings(self):
        self.assertEqual(RECORD["baseline_commit"],BASE)
        self.assertEqual(RECORD["correction_commit"],BASE)
        self.assertEqual(RECORD["preparation_commit"],"afa484620d24a1d6dec2a98e7c06e613f633bfb7")
        self.assertTrue(RECORD["correction_before_operator_execution"])
        for name,binding in RECORD["tools"].items():
            raw=git("show",BASE+":"+binding["path"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(),binding["sha256"])
            self.assertEqual(git("rev-parse",BASE+":"+binding["path"]).decode().strip(),binding["git_blob"])
            self.assertEqual((ROOT/binding["path"]).read_bytes().replace(b"\r\n",b"\n"),raw)
        self.assertEqual(RECORD["tools"]["provision"]["git_blob"],"1eaa8ae508c26f5546bb80ca68393e318b481412")
        self.assertEqual(RECORD["tools"]["validate"]["git_blob"],"1bbe5826927b6b474db73fd2ace8a304b56dac66")
        for name in ("preparation_record","preparation_schema"):
            binding=RECORD[name];raw=git("show",BASE+":"+binding["path"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(),binding["sha256"])
            self.assertEqual((ROOT/binding["path"]).read_bytes().replace(b"\r\n",b"\n"),raw)

    def test_operator_provenance_and_local_only_scope(self):
        self.assertEqual(RECORD["pi3_evidence_provenance"],"OPERATOR_SUPPLIED")
        self.assertEqual(RECORD["evidence"]["provenance"],"OPERATOR_SUPPLIED")
        self.assertFalse(RECORD["evidence"]["codex_independent_pi3_inspection"])
        for key in ("codex_pi3_access","pi5_access","home_assistant_access","deployment","adapter_implementation","production_mutation_by_codex","mqtt","authentication_attempted","network_attempted","credential_value_exposed","credential_hash_recorded","rotation_performed"):
            self.assertIs(RECORD[key],False,key)
        self.assertEqual(RECORD["authentication_validation"],"DEFERRED_TO_ADAPTER_VALIDATION")
        self.assertIn("HOME_ASSISTANT_CREDENTIAL_VALIDITY",RECORD["not_proven"])
        self.assertIn("REVOCATION_STATE",RECORD["not_proven"])
        self.assertIn("ASSOCIATION_ADAPTER_SUCCESS",RECORD["not_proven"])

    def test_evidence_sequence_is_preserved(self):
        evidence=RECORD["evidence"]
        sync=evidence["source_synchronization"]
        self.assertEqual(sync["head_before"],"d7aa423e2ead6e9c1266a884ab3e25e4331ebec1")
        for key in ("origin_after_fetch","head_after","origin_after"):self.assertEqual(sync[key],BASE)
        self.assertFalse(sync["credential_provisioned"])
        self.assertEqual((sync["ahead"],sync["behind"]),(0,0))
        for stage in ("installation","root_validation","runtime_operator_validation"):
            self.assertEqual(evidence[stage]["source_binding"],"PASS")
            self.assertEqual(evidence[stage]["approved_commit"],BASE)
            result=evidence[stage]["result"]
            self.assertEqual(result["RESULT"],"PASS")
            for key in ("CREDENTIAL_VALUE_EXPOSED","NETWORK_CONNECTION_ATTEMPTED","HA_AUTHENTICATION_ATTEMPTED"):self.assertEqual(result[key],"FALSE")
        self.assertEqual(evidence["installation"]["result"]["OPERATION"],"INSTALL")
        self.assertEqual(evidence["installation"]["result"]["INDEPENDENT_VALIDATION"],"NOT_STARTED")
        self.assertEqual(evidence["root_validation"]["result"]["CREDENTIAL_READABLE_BY_RUNTIME_OPERATOR"],"NOT_TESTED")
        self.assertEqual(evidence["root_validation"]["result"]["RUNTIME_OPERATOR_VALIDATION"],"NOT_STARTED")
        self.assertEqual(evidence["runtime_operator_validation"]["executed_as"],"jazofv1")
        self.assertEqual(evidence["runtime_operator_validation"]["result"]["CREDENTIAL_READABLE_BY_RUNTIME_OPERATOR"],"TRUE")

    def test_storage_boundary_and_accepted_results(self):
        self.assertEqual(RECORD["credential_path"],"/etc/hioc/credentials/home_assistant.token")
        self.assertEqual(RECORD["directory_policy"],{"owner":"root","group":"jazofv1","mode":"0750"})
        self.assertEqual(RECORD["file_policy"],{"owner":"root","group":"jazofv1","mode":"0640","regular_file":True,"single_link":True})
        self.assertEqual(RECORD["stored_representation"],"TOKEN_PLUS_EXACTLY_ONE_FINAL_LF")
        self.assertEqual(RECORD["read_normalization"],"REQUIRE_AND_REMOVE_EXACTLY_ONE_FINAL_LF_NO_TRIM")
        for key in ("installation_result","acl_validation","group_reader_validation","canonical_content_validation","atomic_replacement","root_validation","runtime_operator_validation"):self.assertEqual(RECORD[key],"PASS")
        self.assertIs(RECORD["runtime_readability"],True)

    def test_no_secret_or_secret_derived_evidence(self):
        forbidden={"token","token_value","credential_value","token_hash","credential_hash","token_length","credential_length","token_prefix","token_suffix","prefix","suffix","entropy","inode","timestamp","raw_exception"}
        def inspect(value):
            if isinstance(value,dict):
                self.assertFalse(forbidden & set(value))
                for child in value.values():inspect(child)
            elif isinstance(value,list):
                for child in value:inspect(child)
            elif isinstance(value,str):
                self.assertNotIn("TEST_ONLY",value)
        inspect(RECORD)
        # Every recorded SHA is identity of repository source, never a credential.
        identities=[RECORD["preparation_record"]["sha256"],RECORD["preparation_schema"]["sha256"]]+[b["sha256"] for b in RECORD["tools"].values()]
        self.assertEqual(sorted(re.findall(r'"sha256":"([0-9a-f]{64})"',PATH.read_text())),sorted(identities))

    def test_authoritative_lifecycle_and_exact_next(self):
        life=RECORD["lifecycle"]
        for key in ("preparation","operator_installation","independent_validation","governance_closure","parent"):self.assertEqual(life[key],"PASS_CLOSED")
        self.assertEqual(RECORD["parent_checkpoint_status"],"PASS_CLOSED")
        self.assertEqual((life["adapter_implementation"],life["pe4"],life["phase7a"],life["rollback"]),("NOT_STARTED","NOT_COMPLETE","ACTIVE","NOT_PERFORMED"))
        self.assertEqual(RECORD["next_checkpoint"],NEXT)
        text=(ROOT/"docs/HIOC_MASTER_PLAN.md").read_text(encoding="utf-8")
        current=text.split("# Implementation Status",1)[1].split("# Historical Operator Preparation Chronology",1)[0]
        for name in ("PE-4 Home Assistant Runtime Credential Provisioning Preparation","PE-4 Home Assistant Runtime Credential Provisioning","Operator Credential Installation","Independent Credential Validation","Credential Provisioning Governance Closure"):
            self.assertIn("| "+name+" | PASS/CLOSED |",current)
        self.assertIn("| PE-4 Home Assistant Association Adapter Implementation | PASS/CLOSED, corrected before deployment |",current)
        self.assertTrue(current.split("## Next Planned Task",1)[1].strip().startswith("### PE-4 Home Assistant Association Adapter Durable Post-Run Reconciliation"))
        self.assertIn("**PE-4 Home Assistant Association Adapter Durable Post-Run Reconciliation",current.split("## Current Objective",1)[1])

    def test_other_roadmap_and_history_unchanged(self):
        before=git("show",BASE+":docs/HIOC_MASTER_PLAN.md").decode("utf-8")
        after=(ROOT/"docs/HIOC_MASTER_PLAN.md").read_text(encoding="utf-8")
        for start,end in (("### Future Compatibility Diagnostics UX Checkpoint","# Historical Operator Preparation Chronology"),("# Historical Operator Preparation Chronology",None),("## Future Enhancements","# Repository Rules")):
            a=before.split(start,1)[1];b=after.split(start,1)[1]
            if end:a=a.split(end,1)[0];b=b.split(end,1)[0]
            if start=="## Future Enhancements":
                a=a.replace("Runtime Credential Provisioning PREPARED / NOT COMPLETE; Operator Installation and Independent Validation NOT STARTED; adapter implementation NOT STARTED; PE-4 NOT COMPLETE.","Runtime Credential Provisioning PASS/CLOSED; Operator Installation, Independent Validation and Governance Closure PASS/CLOSED based on operator-supplied PI3 evidence; adapter implementation NOT STARTED; PE-4 NOT COMPLETE.",1)
            if start=="## Future Enhancements": a=a.replace("adapter implementation NOT STARTED; PE-4 NOT COMPLETE.","adapter implementation PASS/CLOSED (repository/synthetic only); deployment and scheduler NOT STARTED; PE-4 NOT COMPLETE.",1)
            self.assertEqual(a,b,start)

    def test_protected_sources_no_adapter_and_document_links(self):
        for path in git("ls-tree","-r","--name-only",BASE).decode().splitlines():
            if path.startswith(("pi4/","release/","homeassistant/","governance/pe4/")) or path=="docs/DATA_MODEL.md":
                self.assertEqual(git("show",BASE+":"+path),(ROOT/path).read_bytes().replace(b"\r\n",b"\n"),path)
        for path in ("pi4/lib/hioc/home_assistant_association.py","pi4/bin/hioc-home-assistant-association.py"):
            self.assertEqual(git("ls-tree","-r","--name-only",BASE,"--",path),b"")
            implementation=json.loads((ROOT/"governance/pe4/pe4-ha-association-runtime-validation-correction.json").read_bytes())
            binding=next(v for v in implementation["sources"].values() if v["path"]==path)
            self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),binding["sha256"])
        doc=ROOT/"docs/PE4_HOME_ASSISTANT_RUNTIME_CREDENTIAL_PROVISIONING.md"
        for target in re.findall(r"\]\(([^)]+)\)",doc.read_text(encoding="utf-8")):
            if "://" not in target and not target.startswith("#"):self.assertTrue((doc.parent/target.split("#")[0]).resolve().exists(),target)


if __name__=="__main__":unittest.main()
