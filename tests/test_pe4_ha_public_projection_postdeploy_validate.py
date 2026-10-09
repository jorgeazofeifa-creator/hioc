"""Injected read-only review checks; no native host access."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import unittest
from test_pe4_ha_public_projection_deploy import D,CRON,COMMIT
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("projection_postreview",ROOT/"tools/hioc-pe4-ha-public-projection-postdeploy-validate.py")
V=importlib.util.module_from_spec(spec);spec.loader.exec_module(V)

class ReviewFixture:
    def __init__(self,fault=None):self.commit=COMMIT;self.events=[];self.fault=fault;self.expected_cron_sha=D.sha(CRON)
    def hit(self,key):
        self.events.append(key)
        if key==self.fault:raise D.Failure("BASELINE_MISMATCH")
    def source(self,*_):self.hit("source")
    def target(self):self.hit("target")
    def observe_baseline(self):self.hit("baseline");return {"synthetic":True}
    def cron_read(self):self.hit("cron");return CRON if self.fault!="wrong_cron" else b"unknown\n"
    def installed_review(self,*_):self.hit("installed")
    def __getattr__(self,name):raise AssertionError("unexpected operation "+name)

class ReviewTests(unittest.TestCase):
    def test_baseline_reads_only_and_returns_receipt(self):
        ops=ReviewFixture();self.assertEqual(V.review(ops,D,"BASELINE"),{"synthetic":True})
        self.assertEqual(ops.events,["source","target","baseline","cron"])
    def test_installed_reads_only(self):
        ops=ReviewFixture();self.assertIsNone(V.review(ops,D,"INSTALLED",{}))
        self.assertEqual(ops.events,["source","target","installed"])
    def test_each_read_gate_fails_closed(self):
        for gate in ("source","target","baseline","cron","wrong_cron"):
            with self.subTest(gate=gate),self.assertRaises(D.Failure):V.review(ReviewFixture(gate),D,"BASELINE")
    def test_installed_failure_propagates_without_mutation(self):
        with self.assertRaises(D.Failure):V.review(ReviewFixture("installed"),D,"INSTALLED",{})
    def test_invalid_cli_is_canonical_and_private(self):
        with contextlib.redirect_stdout(io.StringIO()) as stream:self.assertEqual(V.main(["secret-canary"]),1)
        out=json.loads(stream.getvalue());self.assertNotIn("secret-canary",stream.getvalue());self.assertTrue(out["STOP_REQUIRED"])
        self.assertTrue(all(v is False for k,v in out.items() if k.endswith(("MUTATED","EXECUTED","PUBLISHED","ATTEMPTED","ACCESSED","ACQUIRED"))))
    def test_baseline_cli_needs_no_receipt_hash(self):
        self.assertEqual(V.parse_args(["--preparation-commit",COMMIT,"--mode","baseline"]),(COMMIT,"BASELINE",None))
    def test_installed_cli_requires_explicit_reviewed_receipt_hash(self):
        args=["--preparation-commit",COMMIT,"--mode","installed"]
        with self.assertRaises(ValueError):V.parse_args(args)
        self.assertEqual(V.parse_args(args+["--baseline-sha256","b"*64]),(COMMIT,"INSTALLED","b"*64))
    def test_unknown_mode_duplicate_and_malformed_hash_are_rejected(self):
        args=["--preparation-commit",COMMIT,"--mode","installed"]
        for tail in (["--baseline-sha256","secret-canary"],["--baseline-sha256","b"*64,"extra"],["--other","b"*64]):
            with self.subTest(tail=tail),self.assertRaises(ValueError):V.parse_args(args+tail)
        with self.assertRaises(ValueError):V.parse_args(["--preparation-commit",COMMIT,"--mode","unknown"])
    def test_deployment_and_review_have_no_network_or_runtime_imports(self):
        import ast
        for path in (ROOT/D.TOOL,ROOT/"tools/hioc-pe4-ha-public-projection-postdeploy-validate.py"):
            tree=ast.parse(path.read_text(encoding="utf8"))
            modules={name.name.split(".")[0] for node in ast.walk(tree) if isinstance(node,ast.Import) for name in node.names}
            self.assertFalse(modules&{"websockets","paho","hioc","requests","urllib"})
            text=path.read_text(encoding="utf8");self.assertNotIn("/etc/hioc/credentials",text);self.assertNotIn("8123",text)

if __name__=="__main__":unittest.main()
