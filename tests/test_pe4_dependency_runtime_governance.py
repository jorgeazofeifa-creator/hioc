import hashlib
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTRACT = (ROOT / "docs" / "PE4_ISOLATED_RUNTIME_DEPENDENCY_CONTRACT.md").read_text(encoding="utf-8")
LOCK = (ROOT / "requirements-pe4.lock").read_text(encoding="utf-8")
CLIENT = ROOT / "tools" / "hioc-pe4-ha-auth-capability.py"


class PE4DependencyRuntimeGovernanceTests(unittest.TestCase):
    def test_python_policy_and_case_are_explicit(self):
        for value in (
            "PI3_PYTHON_POLICY=SATISFIES_EXISTING_HIOC_POLICY",
            "PI3_PYTHON_RUNTIME=CPYTHON_3_11_2",
            "PYTHON_VERSION_CHANGE_REQUIRED=FALSE",
            "DEPENDENCY_ARCHITECTURE=CASE_A_ISOLATED_RUNTIME",
        ):
            self.assertIn(value, CONTRACT)

    def test_artifact_identity_and_lock_are_exact(self):
        digest = "86d7f0f8bdb25d2c632b72527325e4776430fd5bc61b9118de4e2b8ddb5f5b01"
        filename = "websockets-16.1.1-cp311-cp311-manylinux2014_aarch64.manylinux_2_17_aarch64.manylinux_2_28_aarch64.whl"
        self.assertIn(f"FILENAME={filename}", CONTRACT)
        self.assertIn("SIZE_BYTES=188095", CONTRACT)
        self.assertIn(f"SHA256={digest}", CONTRACT)
        self.assertIn("TRANSITIVE_DEPENDENCIES=NONE", CONTRACT)
        self.assertIn("websockets==16.1.1", LOCK)
        self.assertIn(f"--hash=sha256:{digest}", LOCK)

    def test_install_and_isolation_fail_closed(self):
        for flag in ("--no-index", "--no-deps", "--require-hashes", "--only-binary=:all:"):
            self.assertIn(flag, CONTRACT)
        self.assertIn("without\n`--system-site-packages`", CONTRACT)
        self.assertIn("ACTIVE_INTERPRETER=/home/jazofv1/hioc/runtime/pe4/active/bin/python", CONTRACT)
        self.assertIn("replace the pointer atomically", CONTRACT)

    def test_client_identity_remains_reviewed(self):
        self.assertEqual(
            hashlib.sha256(CLIENT.read_bytes()).hexdigest(),
            "5c2886452a61185c7e7329777dbd4fa3de4da98dd4793a1a84501bc30016879e",
        )

    def test_checkpoint_does_not_claim_execution(self):
        self.assertIn("PE-4.0B.2a remains **NOT STARTED**", CONTRACT)
        self.assertIn("does not install, deploy, or\nexecute anything", CONTRACT)


if __name__ == "__main__":
    unittest.main()
