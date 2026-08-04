import json
import sys
import tempfile
import unicodedata
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "pi4" / "lib"))
from hioc.assets import (AssetValidationError, normalize_field, serialize_store,
                         validate_status, validate_store)

TS = "2026-08-03T12:34:56.123456Z"
ID = "dev_0123456789abcdef"


def record(**values):
    fields = {"friendly_name": "Synthetic Asset", "physical_location": None,
              "purpose": None, "notes": None}
    fields.update(values)
    return {"stable_device_id": ID, **fields, "created_at": TS, "updated_at": TS,
            "update_source": "operator_cli", "revision": 1}


def store(records=None):
    records = records or {}
    return {"schema_version": "1.0", "updated_at": TS,
            "asset_count": len(records), "assets": records}


class AssetSchemaTests(unittest.TestCase):
    def test_empty_one_and_sorted_store(self):
        self.assertEqual(validate_store(store())["asset_count"], 0)
        value = store({ID: record()})
        self.assertEqual(validate_store(value), value)
        self.assertEqual(json.loads(serialize_store(value))["asset_count"], 1)

    def test_stable_id_and_closed_schema(self):
        bad = store({ID: record()}); bad["extra"] = True
        with self.assertRaises(AssetValidationError): validate_store(bad)
        bad = store({ID: record()}); bad["assets"][ID]["stable_device_id"] = "dev_ffffffffffffffff"
        with self.assertRaises(AssetValidationError): validate_store(bad)

    def test_unsupported_version_and_unknown_record_field(self):
        bad = store(); bad["schema_version"] = "2.0"
        with self.assertRaises(AssetValidationError) as caught: validate_store(bad)
        self.assertEqual(caught.exception.code, "STORE_UNSUPPORTED_VERSION")
        bad = store({ID: record()}); bad["assets"][ID]["extra"] = 1
        with self.assertRaises(AssetValidationError): validate_store(bad)

    def test_normalization_contract(self):
        self.assertEqual(normalize_field("friendly_name", "  Café  "), "Café")
        self.assertEqual(normalize_field("friendly_name", "e\u0301"), unicodedata.normalize("NFC", "e\u0301"))
        self.assertIsNone(normalize_field("purpose", "  "))
        self.assertEqual(normalize_field("notes", "\r\n alpha  \r\n\r\n beta\t  \r\n"), "alpha\n\n beta")

    def test_limits_controls_lines_and_tabs(self):
        for field, length in (("friendly_name", 129), ("physical_location", 129), ("purpose", 257)):
            with self.assertRaises(AssetValidationError): normalize_field(field, "x" * length)
        for value in ("a\nb", "a\tb", "a\x00b"):
            with self.assertRaises(AssetValidationError): normalize_field("friendly_name", value)
        with self.assertRaises(AssetValidationError): normalize_field("notes", "\n".join("x" for _ in range(9)))
        with self.assertRaises(AssetValidationError): normalize_field("notes", "x" * 1025)

    def test_null_only_record_and_bad_revision_rejected(self):
        bad_record = record(friendly_name=None)
        with self.assertRaises(AssetValidationError): validate_store(store({ID: bad_record}))
        bad_record = record(); bad_record["revision"] = 0
        with self.assertRaises(AssetValidationError): validate_store(store({ID: bad_record}))

    def test_status_is_closed_and_private(self):
        status = {"schema_version": "1.0", "updated": TS, "status": "online",
                  "asset_count": 0, "orphaned_asset_count": 0,
                  "invalid_record_count": 0, "generator": "hioc-assets",
                  "error_code": None, "error_message": None}
        self.assertEqual(validate_status(status), status)
        self.assertNotIn("friendly_name", json.dumps(status))


if __name__ == "__main__": unittest.main()
