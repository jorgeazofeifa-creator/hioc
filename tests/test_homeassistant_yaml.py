import unittest
from pathlib import Path


class HomeAssistantYamlTests(unittest.TestCase):
    def test_homeassistant_yaml_files_parse(self):
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML is not available in this Python runtime")
        root = Path(__file__).resolve().parents[1] / "homeassistant"
        files = sorted(root.rglob("*.yaml"))
        self.assertTrue(files)
        for path in files:
            with self.subTest(path=str(path)):
                yaml.safe_load(path.read_text())


if __name__ == "__main__":
    unittest.main()

