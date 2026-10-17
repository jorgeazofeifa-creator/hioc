"""PE-6.1 synthetic private classifier, provenance, admission, privacy and caller contracts."""
import ast
import contextlib
import copy
import importlib.util
import io
import json
import os
from pathlib import Path
import socket
import subprocess
import tempfile
import stat
from types import SimpleNamespace
import unittest
from datetime import timedelta
from unittest.mock import patch

from hioc import classification as m, classification_caller as caller, enrichment
from hioc import configured_association as pe5
from hioc.inventory import stable_device_id
from hioc.assets import serialize_store, AssetLockTimeout
from test_pe5_local_service_association import snapshot as inventory, device, NOW, OWNER, MAC
from test_assets_schema import record as asset_record, store as asset_store
ROOT=Path(__file__).resolve().parents[1]


def inputs(inv=None):
    return {"inventory":m.snapshot(inventory() if inv is None else inv)}


def host(names=("camera",), inv=None):
    inv=inventory() if inv is None else inv
    bound={OWNER:[dict(hostname=name,source="integration:synthetic"+str(i)) for i,name in enumerate(names)]}
    return enrichment.build_hostname_envelope(inv["devices"],enrichment.collect_hostname_candidates(bound,NOW),None,NOW)


def with_host(names=("camera",)):
    value=inputs();value["hostname"]=m.snapshot(host(names));return value


def asset():
    row=asset_record(friendly_name="PRIVATE_NAME",physical_location="PRIVATE_LOCATION",
                     purpose="PRIVATE_PURPOSE",notes="PRIVATE_NOTES")
    row["stable_device_id"]=OWNER
    return asset_store({OWNER:row})


def policy(known=None):
    p=dict(m.POLICY)
    p["approved_known_sha256"]=None if known is None else known["sha256"]
    return p


def proof(inv=None, source=None):
    inv=inventory() if inv is None else inv
    return dict(output=pe5.compose(inv,source,NOW),source=source,
                output_confirmation="CONFIRMED",source_confirmation=None if source is None else "CONFIRMED")


def one(value=None, p=None):
    return m.resolve_classification(with_host() if value is None else value,NOW,p)["devices"][0]


class ClassificationTests(unittest.TestCase):
    def test_adopted_schema_and_rules_are_exact_immutable_pe60(self):
        import hioc.classification_contract as contract
        raw=subprocess.check_output(["git","show","ea4a93fba1615af1d6641c7f0683b8e912c03d72:governance/pe6/pe6-classification-contract-design.json"],cwd=ROOT)
        accepted=json.loads(raw)
        self.assertEqual(contract.SCHEMA,accepted["proposed_output_schema"])
        self.assertEqual(contract.RULES,accepted["role_suggestion_contract"]["rules"])
        self.assertEqual(contract.DIMENSIONS,accepted["metadata_quality_contract"]["dimensions"])

    def test_each_rule_exact_tokens_case_and_boundaries(self):
        for rule in m.RULES[:-1]:
            for token in rule["tokens"]:
                with self.subTest(token=token):
                    self.assertIn(rule["role"],[x["role"] for x in one(with_host((token.upper()+"-fixture",)))["role_suggestion"]])
                    self.assertNotIn(rule["role"],[x["role"] for x in one(with_host(("prefix"+token+"suffix",)))["role_suggestion"]])

    def test_multiple_roles_never_choose_winner(self):
        row=one(with_host(("camera-server",)))
        self.assertEqual(row["classification_status"],"AMBIGUOUS")
        self.assertIsNone(row["operator_role"])
        self.assertEqual({x["role"] for x in row["role_suggestion"]},{"IoT","Server"})
        self.assertEqual({x["confidence"] for x in row["role_suggestion"]},{"low"})

    def test_unicode_and_punycode_never_create_token_authority(self):
        for name in ("cámara", "xn--camera-example", "télévision"):
            self.assertEqual(one(with_host((name,)))["role_suggestion"],[])

    def test_hostname_conflict_excluded_and_quality_conflicted(self):
        row=one(with_host(("camera","server")))
        self.assertEqual(row["role_suggestion"],[])
        self.assertEqual(row["metadata_quality"],"conflicted")

    def test_historical_hostname_never_used(self):
        inv=inventory()
        previous=host()
        value=inputs(inv)
        value["hostname"]=m.snapshot(enrichment.build_hostname_envelope(inv["devices"],{},previous,NOW))
        self.assertEqual(one(value)["role_suggestion"],[])

    def test_unpaired_hostname_and_unknown_schema_are_rejected(self):
        for key,value in (("generated_at","2026-10-12T11:59:59Z"),("schema_version","2.0"),("secret","PRIVATE_SECRET")):
            data=host();data[key]=value;current=inputs();current["hostname"]=m.snapshot(data)
            r=m.resolve_classification(current,NOW)
            self.assertEqual(r["state"],"PARTIAL")
            self.assertEqual(r["devices"][0]["role_suggestion"],[])
            self.assertEqual(next(x for x in r["inputs"] if x["kind"]=="hostname")["state"],"INVALID")

    def test_repeated_hostname_views_do_not_boost_confidence(self):
        row=one(with_host(("camera","camera","camera")))
        self.assertEqual(len(row["role_suggestion"]),1)
        candidate=row["role_suggestion"][0]
        self.assertEqual(candidate["confidence"],"low")
        self.assertEqual(len(candidate["evidence_ids"]),3)
        self.assertEqual(len(candidate["correlation_groups"]),1)

    def test_operator_source_proof_and_explicit_unknown(self):
        for role in ("Server","Unknown"):
            current=with_host()
            current["known_operator_role"]=m.snapshot({"devices":[{"mac":MAC,"role":role}]})
            row=one(current,policy(current["known_operator_role"]))
            self.assertEqual(row["operator_role"],role)
            self.assertEqual(row["classification_status"],"EXPLICIT_UNKNOWN" if role=="Unknown" else "OPERATOR_DECLARED")
            self.assertRegex(row["operator_role_evidence"],"^[0-9a-f]{64}$")
            self.assertEqual(row["role_suggestion"][0]["role"],"IoT")

    def test_unapproved_config_and_public_role_are_not_confirmation(self):
        current=inputs();inv=current["inventory"]["value"];inv["devices"][0]["role"]="Server"
        inv["devices"][0]["sources"]=["known_infrastructure"];current["inventory"]=m.snapshot(inv)
        current["known_operator_role"]=m.snapshot({"devices":[{"mac":MAC,"role":"Server"}]})
        self.assertIsNone(one(current)["operator_role"])
        self.assertIsNone(one(inputs(inv))["operator_role"])

    def test_conflicting_explicit_declarations_preserved_as_conflict(self):
        current=inputs()
        current["known_operator_role"]=m.snapshot({"devices":[{"mac":MAC,"role":r} for r in ("IoT","Server")]})
        row=one(current,policy(current["known_operator_role"]))
        self.assertIsNone(row["operator_role"]);self.assertIsNone(row["operator_role_evidence"])
        self.assertEqual(row["metadata_quality"],"conflicted")

    def test_source_removal_and_disabled_declaration_retracts_confirmation(self):
        current=inputs();known=m.snapshot({"devices":[{"mac":MAC,"role":"Server","enabled":False}]})
        current["known_operator_role"]=known
        self.assertIsNone(one(current,policy(known))["operator_role"])
        self.assertIsNone(one(inputs())["operator_role"])

    def test_configuration_approval_binds_exact_original_bytes(self):
        current=inputs();value={"devices":[{"mac":MAC,"role":"Server"}]}
        raw=json.dumps(value,indent=2).encode()+b"\n"
        current["known_operator_role"]=m.snapshot(value,raw=raw)
        self.assertEqual(one(current,policy(current["known_operator_role"]))["operator_role"],"Server")
        altered=m.snapshot(value)
        self.assertIsNone(one(dict(current,known_operator_role=altered),policy(current["known_operator_role"]))["operator_role"])

    def test_asset_completeness_and_values_preserved(self):
        for field in (None,"friendly_name","physical_location","purpose"):
            current=inputs();data=asset()
            if field:data["assets"][OWNER][field]=None
            current["assets"]=m.snapshot(data);before=copy.deepcopy(current)
            row=one(current)
            self.assertEqual(row["metadata_quality"],"incomplete" if field else "documented")
            self.assertEqual(current,before)
            self.assertNotIn("PRIVATE_",m.canonical(row).decode())

    def test_optional_notes_not_required_and_asset_not_physical_class(self):
        current=inputs();value=asset();value["assets"][OWNER]["notes"]=None;current["assets"]=m.snapshot(value)
        row=one(current)
        self.assertEqual(row["metadata_quality"],"documented")
        self.assertEqual(next(x for x in row["quality_details"] if x["name"]=="physical_asset_classification")["state"],"not_supported_current_schema")

    def test_missing_invalid_asset_and_orphan_are_distinct(self):
        self.assertEqual(one(inputs())["metadata_quality"],"incomplete")
        for value in ({},dict(asset(),schema_version="2.0")):
            current=inputs();current["assets"]=m.snapshot(value)
            self.assertEqual(one(current)["metadata_quality"],"unknown")
        current=inputs();data=asset();orphan="dev_1111111111111111";row=data["assets"].pop(OWNER);row["stable_device_id"]=orphan;data["assets"][orphan]=row;current["assets"]=m.snapshot(data)
        self.assertEqual(one(current)["metadata_quality"],"incomplete")

    def test_weak_duplicate_mac_and_owner_mismatch(self):
        for devices in ([dict(device(),mac="")],[device(),dict(device(),id="dev_1111111111111111")],[dict(device(),id="dev_1111111111111111")]):
            current=inputs(inventory(devices=devices))
            result=m.resolve_classification(current,NOW)
            self.assertTrue(all(d["identity_status"]!="strong" and not d["role_suggestion"] and d["metadata_quality"]=="unknown" for d in result["devices"]))

    def test_empty_inventory_valid_context_and_duplicates_invalid(self):
        r=m.resolve_classification(inputs(inventory(devices=[],services=[])),NOW)
        self.assertNotEqual(r["state"],"UNAVAILABLE");self.assertEqual(r["summary"]["device_count"],0)
        r=m.resolve_classification(inputs(inventory(devices=[device(),device()])),NOW)
        self.assertEqual(r["state"],"UNAVAILABLE");self.assertIsNone(r["valid_until"])

    def test_missing_required_inventory_never_valid_empty(self):
        for value in ({},{"inventory":m.snapshot()},{"inventory":m.snapshot({})}):
            r=m.resolve_classification(value,NOW)
            self.assertEqual(r["state"],"UNAVAILABLE");self.assertEqual(r["devices"],[])

    def test_future_inventory_exact_deadline_and_backwards_use(self):
        for at in ("2026-10-12T11:59:59Z","2026-10-12T12:35:00Z"):
            self.assertEqual(m.resolve_classification(inputs(),at)["state"],"UNAVAILABLE")
        r=m.resolve_classification(inputs(),NOW)
        for at in ("2026-10-12T11:59:59Z","2026-10-12T12:35:00Z"):
            with self.assertRaises(m.ClassificationError):m.validate_classification_result(r,inputs(),at)

    def test_result_is_revalidated_not_self_authenticating(self):
        current=with_host();r=m.resolve_classification(current,NOW)
        m.validate_classification_result(r,current,"2026-10-12T12:00:01Z")
        for change in ("summary","confidence","operator","reason","dimension"):
            bad=copy.deepcopy(r)
            if change=="summary":bad["summary"]["suggestion_count"]=0
            if change=="confidence":bad["devices"][0]["role_suggestion"][0]["confidence"]="high"
            if change=="operator":bad["devices"][0]["operator_role"]="Server"
            if change=="reason":bad["devices"][0]["reason_codes"]=[]
            if change=="dimension":bad["devices"][0]["quality_details"][0]["state"]="strong"
            with self.subTest(change=change),self.assertRaises(m.ClassificationError):
                m.validate_classification_result(bad,current,NOW)

    def test_source_fingerprint_change_and_retraction(self):
        current=with_host();r=m.resolve_classification(current,NOW)
        changed=with_host(("tv",))
        with self.assertRaises(m.ClassificationError):m.validate_classification_result(r,changed,NOW)
        bad=copy.deepcopy(current);bad["hostname"]["value"]["secret"]="PRIVATE"
        row=one(bad);self.assertEqual(row["role_suggestion"],[])

    def test_semantic_ids_stable_across_time_and_digest_changes(self):
        a=one(with_host(("camera",)))["role_suggestion"][0]
        b=m.resolve_classification(with_host(("camera-fixture",)),"2026-10-12T12:00:01Z")["devices"][0]["role_suggestion"][0]
        self.assertEqual(a["suggestion_id"],b["suggestion_id"]);self.assertNotEqual(a["evidence_ids"],b["evidence_ids"])
        self.assertEqual(a["suggestion_id"],"rsug_"+m.digest(["pe6-role-v1",OWNER,"IoT"]))

    def test_no_network_subprocess_files_clock_or_input_mutation(self):
        current=with_host();before=copy.deepcopy(current)
        with patch("socket.socket",side_effect=AssertionError("network")),patch("subprocess.Popen",side_effect=AssertionError("process")),patch("builtins.open",side_effect=AssertionError("file")),patch("os.getenv",side_effect=AssertionError("environment")):
            result=m.resolve_classification(current,NOW)
        self.assertEqual(current,before);self.assertEqual(result["devices"][0]["role_suggestion"][0]["role"],"IoT")

    def test_ha_allowlist_relationship_only_never_role(self):
        current=inputs()
        current["home_assistant_summary"]=m.snapshot({OWNER:dict(associated=True,association_basis="strong_mac",entity_count=1,integration_domains=["camera"],has_area_candidate=True)})
        row=one(current);self.assertEqual(row["role_suggestion"],[])
        current["home_assistant_summary"]["value"][OWNER]["private_name"]="PRIVATE"
        self.assertEqual(one(current)["role_suggestion"],[])

    def test_pe5_confirmed_local_relationship_only_and_deadline(self):
        current=inputs();current["pe5_handoff"]=m.snapshot(proof())
        r=m.resolve_classification(current,NOW)
        self.assertEqual(r["devices"][0]["role_suggestion"][0]["role"],"Core Infrastructure")
        self.assertEqual(r["valid_until"],"2026-10-12T12:20:00.000000Z")
        with self.assertRaises(m.ClassificationError):m.validate_classification_result(r,current,"2026-10-12T12:20:00Z")

    def test_pending_wrong_revision_changed_inventory_rejected(self):
        for field in ("output_confirmation","source_confirmation","inventory","schema_version"):
            current=inputs();data=proof()
            if field=="output_confirmation":data[field]="PENDING"
            elif field=="source_confirmation":
                from test_pe5_configured_association_implementation import source
                data=proof(source=source());data[field]="PENDING"
            elif field=="inventory":data["output"]["inventory"]["sha256"]="0"*64
            else:data["output"]["schema_version"]="9.0"
            current["pe5_handoff"]=m.snapshot(data)
            self.assertEqual(one(current)["role_suggestion"],[])

    def test_opaque_configured_mqtt_alone_never_classifies(self):
        from test_pe5_configured_association_implementation import source
        inv=inventory(services=[]);current=inputs(inv);current["pe5_handoff"]=m.snapshot(proof(inv,source()))
        self.assertEqual(one(current)["role_suggestion"],[])

    def test_admission_limits_never_truncate(self):
        current=inputs(inventory(devices=[device()]*4097))
        r=m.resolve_classification(current,NOW)
        self.assertEqual(r["state"],"UNAVAILABLE")
        self.assertEqual(next(x for x in r["inputs"] if x["kind"]=="inventory")["reason_code"],"LIMIT_EXCEEDED")
        current=inputs();v=inventory();v["padding"]="x"*(m.LIMIT+1);current["inventory"]=m.snapshot(v)
        r=m.resolve_classification(current,NOW)
        self.assertEqual(r["state"],"UNAVAILABLE")

    def test_closed_snapshots_invalid_json_and_safe_errors(self):
        for raw in (b'{"a":1,"a":2}',b'{"a":NaN}',b'{',b'\xff'):
            with self.assertRaises(ValueError):pe5.strict_json(raw,m.LIMIT)
        with self.assertRaises(m.ClassificationError) as caught:m.resolve_classification(inputs(),"PRIVATE_CLOCK_SECRET")
        self.assertEqual(str(caught.exception),"CLOCK_INVALID")
        with self.assertRaises(m.ClassificationError):m.resolve_classification(inputs(),NOW,dict(m.POLICY,inventory_age_seconds=True))


    def test_candidate_admission_overflow_is_explicit_not_truncated(self):
        current=with_host(tuple("camera" for unused in range(65)))
        result=m.resolve_classification(current,NOW)
        self.assertEqual(result["devices"][0]["role_suggestion"],[])
        self.assertEqual(next(x for x in result["inputs"] if x["kind"]=="hostname")["reason_code"],"LIMIT_EXCEEDED")

    def test_manufacturer_pinned_database_recomputed_and_not_role_evidence(self):
        from test_manufacturer_schema import write_pair, STAMP
        from hioc import manufacturer
        with tempfile.TemporaryDirectory() as name:
            root=Path(name);write_pair(root)
            for p in root.iterdir():p.chmod(0o600)
            db=manufacturer.load_database(root/"manufacturer-db.json",root/"manufacturer-db.manifest.json")
            dbraw=(root/"manufacturer-db.json").read_bytes();mfraw=(root/"manufacturer-db.manifest.json").read_bytes()
            pin=dict(database=m.snapshot(json.loads(dbraw),raw=dbraw),manifest=m.snapshot(json.loads(mfraw),raw=mfraw),approved_manifest_sha256=__import__("hashlib").sha256(mfraw).hexdigest())
            for mac,disposition in (("a0:b1:c2:d3:e0:02","matched"),(MAC,"excluded"),("01:00:00:00:00:01","excluded"),("00:00:00:00:00:01","unknown")):
                inv=inventory(devices=[device(mac=mac)])
                side,unused=manufacturer.build_manufacturer_sidecar(inv,db,generated_at=STAMP)
                current=inputs(inv);current["manufacturer"]=m.snapshot(side)
                p=dict(m.POLICY,manufacturer_dataset=pin);row=one(current,p)
                self.assertEqual(next(x for x in row["quality_details"] if x["name"]=="manufacturer_attribution")["state"],disposition)
                self.assertEqual(row["role_suggestion"],[])
            inv=inventory(devices=[device(mac="a0:b1:c2:d3:e0:02")])
            side,unused=manufacturer.build_manufacturer_sidecar(inv,db,generated_at=STAMP)
            side["records"][inv["devices"][0]["id"]]["manufacturer"]="FORGED_PRIVATE_ORGANIZATION"
            current=inputs(inv);current["manufacturer"]=m.snapshot(side)
            row=one(current,p)
            self.assertEqual(next(x for x in row["quality_details"] if x["name"]=="manufacturer_attribution")["state"],"unverified")

    def test_restart_is_recomputation_no_last_known_good(self):
        first=m.resolve_classification(with_host(),NOW)
        second=m.resolve_classification(inputs(),NOW)
        self.assertTrue(first["devices"][0]["role_suggestion"])
        self.assertEqual(second["devices"][0]["role_suggestion"],[])
        with self.assertRaises(m.ClassificationError):m.validate_classification_result(first,inputs(),NOW)

    def test_private_sources_do_not_escape_envelope(self):
        current=with_host();current["assets"]=m.snapshot(asset())
        data=m.canonical(m.resolve_classification(current,NOW)).decode()
        for private in ("PRIVATE_NAME","PRIVATE_LOCATION","PRIVATE_PURPOSE","PRIVATE_NOTES",MAC,"192.0.2.1","integration:synthetic"):
            self.assertNotIn(private,data)

    def test_output_and_dimension_order_is_deterministic(self):
        current=with_host(("camera-server",))
        first=m.resolve_classification(current,NOW)
        second=m.resolve_classification(dict(reversed(list(current.items()))),NOW)
        self.assertEqual(first,second)
        row=first["devices"][0]
        self.assertEqual([x["name"] for x in row["quality_details"]],sorted(x["name"] for x in row["quality_details"]))


    def test_asset_schema_uses_exact_parsed_source_order(self):
        value=inputs()
        value["assets"]=m.snapshot(asset(),raw=m.canonical(asset()))
        self.assertEqual(one(value)["metadata_quality"],"unknown")
        value["assets"]=m.snapshot(asset(),raw=serialize_store(asset()))
        self.assertEqual(one(value)["metadata_quality"],"documented")
        # Equality of decoded dictionaries cannot establish the ordered Asset protocol.
        self.assertEqual(json.loads(m.canonical(asset())),json.loads(serialize_store(asset())))


class CallerTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.inv=self.root/"inventory.json"
        self.inv.write_bytes(m.canonical(inventory()));self.inv.chmod(0o600)

    def test_native_windows_safe_reader_and_default_no_store(self):
        before=self.inv.read_bytes()
        r=caller.evaluate({"inventory":self.inv},clock=lambda:NOW,store_factory=lambda:(_ for _ in ()).throw(AssertionError("store")))
        self.assertEqual(r["state"],"PARTIAL");self.assertEqual(self.inv.read_bytes(),before)
        self.assertEqual(sorted(p.name for p in self.root.iterdir()),["inventory.json"])

    def test_no_implicit_asset_initialization_or_lock_creation(self):
        r=caller.evaluate({"inventory":self.inv,"assets":self.root/"missing.json"},clock=lambda:NOW)
        self.assertEqual(r["devices"][0]["metadata_quality"],"unknown")
        self.assertFalse((self.root/"missing.json").exists())

    def test_changed_file_recheck_is_fixed_failure(self):
        reader=caller.Reader();reader.capture("inventory",self.inv,False)
        self.inv.write_bytes(m.canonical(inventory(services=[])))
        with self.assertRaises(m.ClassificationError) as caught:reader.recheck()
        self.assertEqual(str(caught.exception),"CHANGED")

    def test_absent_file_appearance_is_not_silently_adopted(self):
        reader=caller.Reader();path=self.root/"absent.json";reader.capture("hostname",path)
        path.write_bytes(b"{}");path.chmod(0o600)
        with self.assertRaises(m.ClassificationError):reader.recheck()

    def test_hardlink_is_rejected_without_mutation(self):
        link=self.root/"linked.json";os.link(self.inv,link)
        with self.assertRaises(m.ClassificationError):caller.Reader().read(link)
        self.assertEqual(link.read_bytes(),self.inv.read_bytes())

    def test_asset_and_pe5_locks_never_nest(self):
        asset_path=self.root/"assets.json";asset_path.write_bytes(serialize_store(asset()));asset_path.chmod(0o600)
        lock=self.root/"asset.lock";lock.write_bytes(b"");events=[];held=[]
        @contextlib.contextmanager
        def lock_factory(path,shared):
            self.assertEqual(held,[]);self.assertTrue(shared);held.append("asset");events.append("asset")
            try:yield
            finally:held.pop()
        test=self
        class Store:
            @contextlib.contextmanager
            def lock(self):
                test.assertEqual(held,[]);held.append("pe5");events.append("pe5")
                try:yield
                finally:held.pop()
            def read_handoff(self,at):
                with self.lock():return proof()["output"]
            def confirmed(self,domain):
                test.assertEqual(held,["pe5"]);return proof()["output"],None,None
        result=caller.evaluate({"inventory":self.inv,"assets":asset_path},asset_lock=lock,
                              use_pe5=True,clock=lambda:NOW,store_factory=Store,lock_factory=lock_factory)
        self.assertEqual(result["devices"][0]["metadata_quality"],"documented")
        self.assertEqual(events.count("asset"),2);self.assertEqual(events.count("pe5"),4)
        self.assertEqual(held,[])

    def test_cli_summary_never_prints_private_result_or_paths(self):
        spec=importlib.util.spec_from_file_location("pe6_cli",ROOT/"pi4/bin/hioc-classify-metadata.py")
        cli=importlib.util.module_from_spec(spec);spec.loader.exec_module(cli)
        result=m.resolve_classification(with_host(),NOW)
        stream=io.StringIO()
        with contextlib.redirect_stdout(stream):
            self.assertEqual(cli.main(["--inventory","PRIVATE_PATH"],evaluator=lambda *a,**k:result),0)
        output=json.loads(stream.getvalue());self.assertEqual(set(output),{"state","summary"})
        for raw in ("PRIVATE_PATH",OWNER,MAC,"camera","rsug_","role_suggestion"):
            self.assertNotIn(raw,stream.getvalue())

    def test_cli_unknown_arguments_fixed_code_without_echo(self):
        spec=importlib.util.spec_from_file_location("pe6_cli_invalid",ROOT/"pi4/bin/hioc-classify-metadata.py")
        cli=importlib.util.module_from_spec(spec);spec.loader.exec_module(cli)
        stream=io.StringIO()
        with contextlib.redirect_stdout(stream):self.assertEqual(cli.main(["--PRIVATE_SECRET"]),1)
        self.assertNotIn("PRIVATE_SECRET",stream.getvalue())


    def test_asset_pe5_and_recheck_failure_paths_release_every_lock(self):
        asset_path=self.root/"assets.json";asset_path.write_bytes(serialize_store(asset()));asset_path.chmod(0o600)
        lock=self.root/"asset.lock";lock.write_bytes(b"")
        for failure in ("asset_capture","pe5_capture","asset_recheck"):
            with self.subTest(failure=failure):
                held=[];events=[];test=self
                @contextlib.contextmanager
                def asset_lock(path,shared):
                    test.assertEqual(held,[])
                    if failure=="asset_capture":
                        raise AssetLockTimeout("LOCK_TIMEOUT","synthetic")
                    held.append("asset");events.append("asset")
                    try:yield
                    finally:held.pop()
                class Store:
                    @contextlib.contextmanager
                    def lock(self):
                        test.assertEqual(held,[])
                        held.append("pe5");events.append("pe5")
                        try:
                            if failure=="pe5_capture":raise pe5.AssociationError("WRITE_FAILED")
                            yield
                        finally:held.pop()
                    def read_handoff(self,at):
                        with self.lock():return proof()["output"]
                    def confirmed(self,domain):
                        test.assertEqual(held,["pe5"])
                        return proof()["output"],None,None
                class Reader(caller.Reader):
                    def recheck(self):
                        if failure=="asset_recheck":m.fail("CHANGED")
                        return super().recheck()
                def evaluate():
                    return caller.evaluate({"inventory":self.inv,"assets":asset_path},
                        asset_lock=lock,use_pe5=True,clock=lambda:NOW,store_factory=Store,
                        lock_factory=asset_lock,reader=Reader())
                if failure=="asset_recheck":
                    with self.assertRaises(m.ClassificationError):evaluate()
                else:
                    result=evaluate()
                    self.assertEqual(result["devices"][0]["metadata_quality"],
                                     "unknown" if failure=="asset_capture" else "documented")
                self.assertEqual(held,[])
                if failure=="pe5_capture":self.assertEqual(events,["asset","pe5","asset"])




class ReaderFingerprintTests(unittest.TestCase):
    def info(self, **changes):
        values=dict(st_dev=1,st_ino=2,st_size=517,st_mtime_ns=200,
                    st_birthtime_ns=100,st_ctime_ns=100,st_mode=stat.S_IFREG|0o600,
                    st_uid=0,st_gid=0,st_nlink=1,st_file_attributes=32,st_reparse_tag=0)
        values.update(changes)
        return SimpleNamespace(**values)

    def test_windows_creation_and_write_times_use_consistent_meanings(self):
        path=self.info();descriptor=self.info(st_ctime_ns=200)
        self.assertEqual(caller.WindowsReadFS.fingerprint(path),caller.WindowsReadFS.fingerprint(descriptor))
        self.assertNotEqual(caller.fingerprint(path),caller.fingerprint(descriptor))

    def test_windows_identity_and_protected_metadata_are_retained(self):
        original=self.info();expected=caller.WindowsReadFS.fingerprint(original)
        for field in ('st_dev','st_ino','st_size','st_mtime_ns','st_birthtime_ns',
                      'st_mode','st_uid','st_gid','st_nlink','st_file_attributes','st_reparse_tag'):
            with self.subTest(field=field):
                self.assertNotEqual(expected,caller.WindowsReadFS.fingerprint(self.info(**{field:getattr(original,field)+1})))
        for values in ({'st_birthtime_ns':None},{'st_ino':0}):
            with self.assertRaisesRegex(m.ClassificationError,'INVALID'):
                caller.WindowsReadFS.fingerprint(self.info(**values))

    def test_posix_fingerprint_semantics_are_unchanged(self):
        reader=caller.Reader(fs=object())
        self.assertEqual(reader._fingerprint(self.info()),caller.fingerprint(self.info()))
        self.assertNotEqual(reader._fingerprint(self.info()),reader._fingerprint(self.info(st_ctime_ns=201)))


@unittest.skipUnless(os.name=='nt','Real Windows stat/fstat birthtime and reparse fixture; POSIX fingerprint remains separately tested')
class WindowsReaderTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)

    def source(self,name,data):
        path=self.root/name;path.write_bytes(data);path.chmod(0o600)
        info=path.stat()
        # Explicitly distinct timestamps, not a scheduling/timer-dependent fixture.
        os.utime(path,ns=(info.st_atime_ns,info.st_birthtime_ns-5_000_000_000))
        self.assertNotEqual(path.stat().st_birthtime_ns,path.stat().st_mtime_ns)
        return path

    def test_distinct_creation_write_times_inventory_and_documented_asset(self):
        inv=self.source('inventory.json',m.canonical(inventory()))
        ap=self.source('assets.json',serialize_store(asset()))
        lock=self.root/'asset.lock';lock.write_bytes(b'');held=[]
        @contextlib.contextmanager
        def acquire(path,shared):
            self.assertFalse(held);self.assertTrue(shared);held.append(True)
            try:yield
            finally:held.pop()
        before={p:p.read_bytes() for p in (inv,ap)}
        result=caller.evaluate({'inventory':inv,'assets':ap},asset_lock=lock,lock_factory=acquire,clock=lambda:NOW)
        self.assertEqual(result['devices'][0]['identity_status'],'strong')
        self.assertEqual(result['devices'][0]['metadata_quality'],'documented')
        self.assertFalse(held)
        for path,data in before.items():self.assertEqual(path.read_bytes(),data)

    def test_content_change_with_restored_metadata_is_rejected_by_digest(self):
        path=self.source('inventory.json',m.canonical(inventory()))
        reader=caller.Reader();reader.capture('inventory',path,False)
        before=path.stat();old=reader.captured['inventory'][2]
        data=path.read_bytes();changed=data.replace(b'"devices"',b'"devicez"',1)
        self.assertNotEqual(data,changed);self.assertEqual(len(data),len(changed))
        path.write_bytes(changed);os.utime(path,ns=(before.st_atime_ns,before.st_mtime_ns))
        unused,current=reader.read(path,False)
        self.assertEqual(old[:2],current[:2]);self.assertNotEqual(old[2],current[2])
        with self.assertRaisesRegex(m.ClassificationError,'CHANGED'):reader.recheck()

    def test_replacement_and_during_read_modification_are_rejected(self):
        path=self.source('inventory.json',m.canonical(inventory()))
        reader=caller.Reader();reader.capture('inventory',path,False)
        original_id=path.stat().st_ino
        replacement=self.source('replacement.json',path.read_bytes())
        os.replace(replacement,path)
        self.assertNotEqual(original_id,path.stat().st_ino)
        with self.assertRaisesRegex(m.ClassificationError,'CHANGED'):reader.recheck()
        fs=caller.WindowsReadFS();original=fs.fstat;calls=[]
        def changed(fd):
            calls.append(fd)
            if len(calls)==2:
                info=path.stat();os.utime(path,ns=(info.st_atime_ns,info.st_mtime_ns+1_000_000_000))
            return original(fd)
        with patch.object(fs,'fstat',changed),self.assertRaisesRegex(m.ClassificationError,'CHANGED'):
            caller.Reader(fs=fs).read(path,False)

    def test_descriptor_protected_metadata_and_reparse_ancestry_rejected(self):
        path=self.source('inventory.json',m.canonical(inventory()))
        fs=caller.WindowsReadFS();original=fs.fstat
        fields=('st_dev','st_ino','st_size','st_mtime_ns','st_birthtime_ns','st_mode',
                'st_uid','st_gid','st_nlink','st_file_attributes','st_reparse_tag')
        for field in fields:
            def altered(fd,field=field):
                real=original(fd);values={k:getattr(real,k) for k in fields}
                values[field]+=1
                return SimpleNamespace(**values)
            with self.subTest(field=field),patch.object(fs,'fstat',altered),self.assertRaises(m.ClassificationError):
                caller.Reader(fs=fs).read(path,False)
        lstat=Path.lstat
        def reparse(p):
            info=lstat(p)
            if p==self.root:
                return SimpleNamespace(st_mode=info.st_mode,st_file_attributes=0x400)
            return info
        with patch.object(Path,'lstat',reparse),self.assertRaisesRegex(m.ClassificationError,'INVALID'):
            caller.Reader().read(path,False)

    def test_invalid_asset_digest_never_becomes_documented(self):
        current=inputs();current['assets']=m.snapshot(asset(),raw=serialize_store(asset()))
        self.assertEqual(one(current)['metadata_quality'],'documented')
        current['assets']['sha256']='0'*64
        self.assertEqual(one(current)['metadata_quality'],'unknown')


class TimestampCompatibilityTests(unittest.TestCase):
    UTC = "2026-10-17T17:00:02Z"
    NEGATIVE = "2026-10-17T11:00:02-06:00"
    POSITIVE = "2026-10-17T22:30:02+05:30"

    def current(self, stamp):
        inv=inventory();inv["updated"]=stamp
        return inputs(inv)

    def test_equivalent_aware_instants_normalize_to_utc(self):
        from datetime import timezone
        for stamp in [self.UTC,self.NEGATIVE,self.POSITIVE,"2026-10-17T17:00:02+00:00"]:
            with self.subTest(stamp=stamp):
                self.assertEqual(m.timestamp(stamp),m.timestamp(self.UTC))
                self.assertIs(m.timestamp(stamp).tzinfo,timezone.utc)

    def test_fresh_offset_inventory_preserves_raw_identity_and_devices(self):
        for stamp in [self.UTC,self.NEGATIVE,self.POSITIVE]:
            current=self.current(stamp);before=copy.deepcopy(current)
            result=m.resolve_classification(current,self.UTC)
            self.assertEqual(result["state"],"PARTIAL")
            self.assertEqual(len(result["devices"]),len(current["inventory"]["value"]["devices"]))
            proof=next(x for x in result["inputs"] if x["kind"]=="inventory")
            self.assertEqual(proof["state"],"VALID")
            self.assertEqual(proof["sha256"],current["inventory"]["sha256"])
            self.assertEqual(m.timestamp(proof["generated_at"]),m.timestamp(stamp))
            self.assertTrue(proof["generated_at"].endswith("Z"))
            self.assertEqual(current,before)
            pe5.shape(result,m.SCHEMA,"RESULT_INVALID")
            m.validate_classification_result(result,current,self.UTC)

    def test_offset_evaluation_generates_only_schema_utc_times(self):
        current=self.current(self.NEGATIVE)
        result=m.resolve_classification(current,self.POSITIVE)
        for value in [result["evaluated_at"],result["valid_until"]]:
            self.assertTrue(value.endswith("Z"));self.assertNotIn("+",value)
        self.assertEqual(result["evaluated_at"],"2026-10-17T17:00:02.000000Z")
        pe5.shape(result,m.SCHEMA,"RESULT_INVALID")
        m.validate_classification_result(result,current,self.NEGATIVE)

    def test_offset_freshness_deadline_is_exclusive(self):
        current=self.current(self.NEGATIVE)
        self.assertNotEqual(m.resolve_classification(current,"2026-10-17T17:35:01.999999Z")["state"],"UNAVAILABLE")
        result=m.resolve_classification(current,self.UTC)
        for at in ["2026-10-17T17:35:02Z","2026-10-17T11:35:02-06:00"]:
            with self.subTest(at=at):
                rejected=m.resolve_classification(current,at)
                self.assertEqual(rejected["state"],"UNAVAILABLE");self.assertEqual(rejected["devices"],[])
                with self.assertRaises(m.ClassificationError):m.validate_classification_result(result,current,at)

    def test_offset_future_and_backward_clock_rejected(self):
        current=self.current(self.NEGATIVE)
        at="2026-10-17T17:00:01.999999Z"
        self.assertEqual(m.resolve_classification(current,at)["state"],"UNAVAILABLE")
        result=m.resolve_classification(current,self.UTC)
        with self.assertRaises(m.ClassificationError):m.validate_classification_result(result,current,at)

    def test_naive_malformed_offsets_calendar_and_times_fail_closed(self):
        invalid=["2026-10-17T17:00:02","2026-10-17T17:00:02z","2026-10-17 17:00:02Z",
                 "2026-10-17T17:00:02-0600","2026-10-17T17:00:02+06","2026-10-17T17:00:02+24:00",
                 "2026-10-17T17:00:02+01:60","2026-10-17T17:00:02-06:99",
                 "2026-10-17T17:00:02+01:00:00","2026-02-29T17:00:02Z",
                 "2026-13-17T17:00:02Z","2026-10-17T24:00:02Z","2026-10-17T17:00:60Z",
                 "2026-10-17T17:00:02.1234567Z",None,123]
        for stamp in invalid:
            with self.subTest(stamp=stamp):
                with self.assertRaises(m.ClassificationError) as error:m.timestamp(stamp)
                self.assertEqual(str(error.exception),"CLOCK_INVALID")
                result=m.resolve_classification(self.current(stamp),self.UTC)
                self.assertEqual(result["state"],"UNAVAILABLE");self.assertEqual(result["devices"],[])

    def test_equivalent_timestamp_reencoding_changes_source_identity(self):
        current=self.current(self.NEGATIVE);result=m.resolve_classification(current,self.UTC)
        changed=self.current(self.POSITIVE)
        self.assertNotEqual(current["inventory"]["sha256"],changed["inventory"]["sha256"])
        with self.assertRaises(m.ClassificationError):m.validate_classification_result(result,changed,self.UTC)
        forged=copy.deepcopy(current);forged["inventory"]["value"]["updated"]=self.POSITIVE
        self.assertEqual(m.resolve_classification(forged,self.UTC)["state"],"UNAVAILABLE")

    def test_offset_inventory_hostname_pairing_is_exact_not_time_only(self):
        inv=self.current(self.NEGATIVE)["inventory"]["value"]
        value=enrichment.build_hostname_envelope(inv["devices"],
            enrichment.collect_hostname_candidates({OWNER:[dict(hostname="camera",source="integration:synthetic")]},self.NEGATIVE),None,self.NEGATIVE)
        current=inputs(inv);current["hostname"]=m.snapshot(value)
        # Existing hostname validator and source pairing remain authoritative;
        # changing only the paired representation must not bypass exact identity.
        result=m.resolve_classification(current,self.UTC)
        proof=next(x for x in result["inputs"] if x["kind"]=="hostname")
        self.assertEqual(proof["state"],"VALID")
        self.assertTrue(proof["generated_at"].endswith("Z"))
        value["generated_at"]=self.UTC;current["hostname"]=m.snapshot(value)
        result=m.resolve_classification(current,self.UTC)
        self.assertEqual(next(x for x in result["inputs"] if x["kind"]=="hostname")["state"],"INVALID")

    def test_offset_pe5_handoff_keeps_original_inventory_digest(self):
        inv=self.current(self.NEGATIVE)["inventory"]["value"]
        current=inputs(inv)
        current["pe5_handoff"]=m.snapshot(dict(output=pe5.compose(inv,None,self.UTC),source=None,
            output_confirmation="CONFIRMED",source_confirmation=None))
        result=m.resolve_classification(current,self.UTC)
        self.assertEqual(next(x for x in result["inputs"] if x["kind"]=="pe5_handoff")["state"],"VALID")
        self.assertEqual(result["valid_until"],"2026-10-17T17:20:02.000000Z")
        m.validate_classification_result(result,current,self.UTC)


if __name__=="__main__":unittest.main()
