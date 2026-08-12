import copy
import hashlib
import importlib.util
import pathlib
import subprocess
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
HELPER = ROOT / "tools" / "hioc_manufacturer_protection.py"
ACTION5 = (ROOT / "tools" / "hioc-pe3-action5-deploy.sh").read_text(encoding="utf-8")
ACTION5C = (ROOT / "tools" / "hioc-pe3-action5c-revalidate.sh").read_text(encoding="utf-8")
spec = importlib.util.spec_from_file_location("manufacturer_protection", HELPER)
protection = importlib.util.module_from_spec(spec)
spec.loader.exec_module(protection)


ABSENT = {"type": "absent"}
PRIVATE_DIR = {"type": "directory", "mode": 0o700, "owner": "jazofv1", "group": "jazofv1"}


def state(*, root=ABSENT, versions=ABSENT, entries=None, payload=None,
          sidecar=ABSENT, status=ABSENT, configuration=None):
    return {
        "schema_version": 1,
        "manufacturer_root": copy.deepcopy(root),
        "manufacturer_root_entries": [] if entries is None else entries,
        "versions_root": copy.deepcopy(versions),
        "payload": [] if payload is None else payload,
        "sidecar": copy.deepcopy(sidecar),
        "status": copy.deepcopy(status),
        "configuration": configuration or {
            "type": "regular", "mode": 0o600, "owner": "jazofv1",
            "group": "jazofv1", "bytes": 10, "sha256": "a" * 64,
        },
    }


class Action5ManufacturerProtectionTests(unittest.TestCase):
    def setUp(self):
        self.before_absent = state()
        self.after_empty = state(
            root=PRIVATE_DIR, versions=PRIVATE_DIR, entries=["versions"]
        )

    def assert_rejected(self, after):
        passed, _ = protection.compare(self.after_empty, after)
        self.assertFalse(passed)

    def test_absent_to_private_empty_scaffolding_is_allowed(self):
        self.assertEqual(protection.compare(self.before_absent, self.after_empty), (True, "PASS"))

    def test_directory_mode_normalization_is_allowed(self):
        before = state(
            root={**PRIVATE_DIR, "mode": 0o750},
            versions={**PRIVATE_DIR, "mode": 0o755}, entries=["versions"],
        )
        self.assertEqual(protection.compare(before, self.after_empty), (True, "PASS"))

    def test_version_directory_creation_is_rejected(self):
        after = copy.deepcopy(self.after_empty)
        after["payload"] = [{"path": "version-a", **PRIVATE_DIR}]
        self.assert_rejected(after)

    def test_database_manifest_and_hash_changes_are_rejected(self):
        for name in ("manufacturer-db.json", "manufacturer-db.manifest.json"):
            after = copy.deepcopy(self.after_empty)
            after["payload"] = [{
                "path": f"version-a/{name}", "type": "regular", "mode": 0o600,
                "owner": "jazofv1", "group": "jazofv1", "bytes": 1,
                "sha256": "b" * 64,
            }]
            self.assert_rejected(after)
        before = copy.deepcopy(self.after_empty)
        before["payload"] = [{"path": "version-a/file", "type": "regular", "sha256": "a" * 64}]
        after = copy.deepcopy(before)
        after["payload"][0]["sha256"] = "b" * 64
        self.assertFalse(protection.compare(before, after)[0])

    def test_symlink_and_unexpected_root_entry_are_rejected(self):
        after = copy.deepcopy(self.after_empty)
        after["versions_root"] = {"type": "symlink", "target": "/tmp/value"}
        self.assert_rejected(after)
        after = copy.deepcopy(self.after_empty)
        after["manufacturer_root_entries"] = ["unexpected", "versions"]
        self.assert_rejected(after)

    def test_wrong_scaffolding_owner_or_group_is_rejected(self):
        for field in ("owner", "group"):
            after = copy.deepcopy(self.after_empty)
            after["versions_root"][field] = "unexpected"
            self.assert_rejected(after)

    def test_sidecar_status_and_configuration_changes_are_rejected(self):
        for field in ("sidecar", "status"):
            after = copy.deepcopy(self.after_empty)
            after[field] = {"type": "regular", "sha256": "c" * 64}
            self.assert_rejected(after)
        after = copy.deepcopy(self.after_empty)
        after["configuration"]["sha256"] = "d" * 64
        self.assertEqual(protection.compare(self.after_empty, after), (False, "CONFIGURATION_CHANGED"))

    def test_current_empty_scaffolding_closure_is_exact(self):
        self.assertEqual(protection.validate_empty_current(self.after_empty), (True, "PASS"))
        changed = copy.deepcopy(self.after_empty)
        changed["payload"] = [{"path": "version-a", **PRIVATE_DIR}]
        self.assertFalse(protection.validate_empty_current(changed)[0])

    def test_rollback_semantics_distinguish_scaffolding_and_payload(self):
        self.assertIn("MANUFACTURER_PAYLOAD_UNTOUCHED=PASS", ACTION5)
        self.assertIn("MANUFACTURER_SCAFFOLDING_STATE=PASS", ACTION5)
        self.assertIn("MANUFACTURER_PAYLOAD_CHANGED MANUFACTURER_PROTECTION TRUE", ACTION5)
        self.assertIn("ROLLBACK_RECOMMENDED=FALSE", ACTION5C)
        self.assertNotIn('bash "$SOURCE/release/upgrade.sh"', ACTION5C)
        self.assertNotIn('bash "$SOURCE/release/rollback.sh"', ACTION5C)

    def test_action5c_is_read_only_and_stops_before_action6(self):
        for forbidden in ("rsync ", "install ", "chmod 0700 --", "ACTION6", "manufacturer-db.json"):
            self.assertNotIn(forbidden, ACTION5C)
        for required in (
            "RUNTIME_VALIDATION=PASS", "RUNTIME_ARTIFACT_IDENTITY=PASS",
            "MANUFACTURER_PAYLOAD_UNTOUCHED=PASS", "MANUFACTURER_SCAFFOLDING_STATE=PASS",
            "CONFIGURATION_UNTOUCHED=PASS", "ACTION5=COMPLETE",
        ):
            self.assertIn(required, ACTION5C)

    def test_action5c_documented_identity_matches(self):
        path = ROOT / "tools" / "hioc-pe3-action5c-revalidate.sh"
        self.assertEqual(
            hashlib.sha256(path.read_bytes()).hexdigest(),
            "f58346ac943c56e74fd5235fae7f02a1519337cb3eca1be90ca1d6312093e55a",
        )
        result = subprocess.run(
            ["git", "hash-object", "--path=tools/hioc-pe3-action5c-revalidate.sh", str(path)],
            cwd=ROOT, check=True, capture_output=True, text=True,
        )
        self.assertEqual(result.stdout.strip(), "da47aa4a3d0346432332fc42f4111a956fd8e1bd")


if __name__ == "__main__":
    unittest.main()
