import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "pi4" / "lib"))

from hioc.core.version import read_version_manifest


class VersionManifestTests(unittest.TestCase):
    def test_repository_version_manifest_loads(self):
        manifest = read_version_manifest(ROOT / "VERSION.yaml")
        self.assertEqual(manifest["hioc_version"], "1.0.0")
        self.assertEqual(manifest["dashboard"], "2.0.0")

    def test_missing_required_key_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "VERSION.yaml"
            path.write_text("hioc_version: 1.0.0\n")
            with self.assertRaises(ValueError):
                read_version_manifest(path)


if __name__ == "__main__":
    unittest.main()

