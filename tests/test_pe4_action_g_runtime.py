import contextlib
import io
import unittest
from unittest import mock

from tools import hioc_pe4_action_g as G


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
