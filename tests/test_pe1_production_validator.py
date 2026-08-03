import json
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "pi4" / "lib"))
sys.path.insert(0, str(ROOT / "tools"))

from hioc.enrichment import build_enrichment_status, build_hostname_envelope, collect_hostname_candidates
from validate_pe1_production import validate_production_artifacts


NOW = "2026-08-03T13:49:00-06:00"
DEVICE_ID = "dev_0123456789abcdef"


class Pe1ProductionValidatorTests(unittest.TestCase):
    def test_uses_emitted_source_type_contract(self):
        evidence = {
            DEVICE_ID: [
                {"hostname": "known-host", "source": "known_infrastructure", "_observed": False},
                {"hostname": "integration-host", "source": "integration:controller"},
                {"hostname": "local-host", "source": "local_host"},
                {
                    "hostname": "lease-host",
                    "source": "dhcp_leases",
                    "dhcp_lease_source": "/etc/pihole/dhcp.leases",
                },
            ]
        }
        candidates = collect_hostname_candidates(evidence, NOW)
        artifact = build_hostname_envelope([{"id": DEVICE_ID}], candidates, None, NOW)
        status = build_enrichment_status("online", NOW, artifact)
        summary = validate_production_artifacts(artifact, status)
        self.assertEqual(
            summary["approved_source_types_observed"],
            [
                "assignment_observation",
                "configured_infrastructure",
                "direct_observation",
                "trusted_integration",
            ],
        )

    def test_rejects_non_online_status(self):
        artifact = build_hostname_envelope([{"id": DEVICE_ID}], {}, None, NOW)
        status = build_enrichment_status("degraded", NOW, artifact, "prior_artifact_invalid")
        with self.assertRaisesRegex(ValueError, "not online"):
            validate_production_artifacts(artifact, status)

    def test_cli_writes_redacted_aggregate_summary(self):
        artifact = build_hostname_envelope([{"id": DEVICE_ID}], {}, None, NOW)
        status = build_enrichment_status("online", NOW, artifact)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            artifact_path = root / "enrichment.json"
            status_path = root / "status.json"
            summary_path = root / "summary.json"
            artifact_path.write_text(json.dumps(artifact), encoding="utf-8")
            status_path.write_text(json.dumps(status), encoding="utf-8")
            from validate_pe1_production import main
            original = sys.argv
            try:
                sys.argv = [
                    "validate_pe1_production.py",
                    str(artifact_path),
                    str(status_path),
                    "--summary",
                    str(summary_path),
                ]
                self.assertEqual(main(), 0)
            finally:
                sys.argv = original
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            self.assertNotIn("records", summary)


if __name__ == "__main__":
    unittest.main()
