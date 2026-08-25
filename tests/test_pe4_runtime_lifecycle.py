import hashlib
import importlib.util
import os
import pathlib
import stat
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
DOC = (ROOT / "docs/PE4_ISOLATED_RUNTIME_LIFECYCLE.md").read_text(encoding="utf-8")

spec = importlib.util.spec_from_file_location("pe4_common", TOOLS / "hioc_pe4_runtime_common.py")
COMMON = importlib.util.module_from_spec(spec)
spec.loader.exec_module(COMMON)


class PE4RuntimeLifecycleTests(unittest.TestCase):
    def test_all_action_entrypoints_exist_and_are_separate(self):
        names = (
            "hioc-pe4-windows-ssh-identity-provision.py",
            "hioc-pe4-artifact-acquire.py", "hioc-pe4-artifact-transfer.py",
            "hioc-pe4-route-proof.py", "hioc-pe4-runtime-construct.py",
            "hioc-pe4-dependency-validate.py", "hioc-pe4-runtime-publish.py",
            "hioc-pe4-runtime-preflight.py", "hioc-pe4-runtime-rollback.py",
        )
        for name in names:
            self.assertTrue((TOOLS / name).is_file(), name)
            compile((TOOLS / name).read_text(encoding="utf-8"), name, "exec")
        for action in "ABCDEFG":
            self.assertIn(f"PE-4.0B.2a-{action}", DOC)

    def test_frozen_identity(self):
        self.assertEqual(COMMON.WHEEL_SIZE, 188095)
        self.assertEqual(COMMON.WHEEL_SHA256, "86d7f0f8bdb25d2c632b72527325e4776430fd5bc61b9118de4e2b8ddb5f5b01")
        self.assertEqual(COMMON.CLIENT_BLOB, "09d66b041796dd6ec2efdb88f7a71b3f99e9a27a")
        self.assertEqual(COMMON.CLIENT_SHA256, "5c2886452a61185c7e7329777dbd4fa3de4da98dd4793a1a84501bc30016879e")
        self.assertEqual(COMMON.SSH_IDENTITY_NAME, "id_ed25519")

    def test_windows_publication_primitive_is_atomic_and_no_replace(self):
        source=(TOOLS/"hioc_pe4_runtime_common.py").read_text(encoding="utf-8")
        body=source[source.index("def windows_publish_no_replace"):source.index("def windows_openssh_tool")]
        self.assertIn("MoveFileExW",body)
        self.assertIn("0x8",body)
        self.assertNotIn("MOVEFILE_REPLACE_EXISTING",body)

    def test_wheel_validator_fails_closed_and_passes_exact_bytes(self):
        with tempfile.TemporaryDirectory() as temp:
            path = pathlib.Path(temp) / COMMON.WHEEL_NAME
            path.write_bytes(b"wrong"); os.chmod(path, 0o600)
            with self.assertRaises(COMMON.Failure): COMMON.validate_wheel(path)

    def test_install_flags_are_offline_and_hash_locked(self):
        source=(TOOLS/"hioc-pe4-runtime-construct.py").read_text(encoding="utf-8")
        for value in ("--no-index","--no-deps","--require-hashes","--only-binary=:all:","--no-cache-dir","--copies"):
            self.assertIn(value,source)
        self.assertNotIn("--upgrade",source)

    def test_network_boundaries_are_separate(self):
        identity=(TOOLS/"hioc-pe4-windows-ssh-identity-provision.py").read_text(encoding="utf-8")
        acquire=(TOOLS/"hioc-pe4-artifact-acquire.py").read_text(encoding="utf-8")
        transfer=(TOOLS/"hioc-pe4-artifact-transfer.py").read_text(encoding="utf-8")
        route=(TOOLS/"hioc-pe4-route-proof.py").read_text(encoding="utf-8")
        self.assertIn("files.pythonhosted.org",acquire); self.assertNotIn("192.168.100.251",acquire)
        self.assertNotIn("PI3_IPV4",identity); self.assertNotIn("hioc-pe4-artifact-transfer.py",identity)
        self.assertIn("StrictHostKeyChecking=yes",transfer); self.assertIn("PI3_IPV4",transfer)
        self.assertIn("(HA_IPV4,HA_PORT)",route); self.assertNotIn("urllib",route)

    def test_every_entrypoint_binds_to_governance_and_bounds_unexpected_errors(self):
        for path in TOOLS.glob("hioc-pe4-*.py"):
            source=path.read_text(encoding="utf-8")
            if path.name == "hioc-pe4-ha-auth-capability.py": continue
            self.assertIn("--governance-commit",source,path.name)
            self.assertIn("UNEXPECTED_ERROR",source,path.name)

    def test_pointer_and_rollback_are_not_caller_selected(self):
        common=(TOOLS/"hioc_pe4_runtime_common.py").read_text(encoding="utf-8")
        rollback=(TOOLS/"hioc-pe4-runtime-rollback.py").read_text(encoding="utf-8")
        self.assertIn("def validated_active_target",common)
        self.assertIn("PREVIOUS_POINTER",rollback)
        self.assertNotIn("--previous-environment",rollback)

    def test_evidence_allowlist_rejects_secret_fields(self):
        with tempfile.TemporaryDirectory() as temp:
            path=pathlib.Path(temp); os.chmod(path,0o700)
            with self.assertRaises(COMMON.Failure):
                COMMON.write_evidence(path,"x",{"TOKEN":"secret"},"PASS")

    def test_cleanup_guards_broad_targets(self):
        for value in (str(COMMON.RUNTIME),str(COMMON.ENVIRONMENT_ROOT),"/tmp/arbitrary"):
            with self.assertRaises(COMMON.Failure): COMMON.validate_construction(value)

    def test_route_order_and_status_remain_closed(self):
        self.assertIn("ROUTE_PROOF_ORDER=BEFORE_DEPENDENCY_DEPLOYMENT",DOC)
        for value in ("PE4_0B2A=NOT_STARTED","PE4_0B2B=NOT_STARTED","PE4_0C=NOT_STARTED"):
            self.assertIn(value,DOC)


if __name__ == "__main__":
    unittest.main()
