import copy
import importlib.util
import json
import logging
import os
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "pi4" / "bin" / "hioc-inventory-engine.py"
VALIDATOR = ROOT / "pi4" / "bin" / "hioc-validate-enrichment.py"

import sys
sys.path.insert(0, str(ROOT / "pi4" / "lib"))

from hioc.core.state import StateStore
from hioc.enrichment import (
    EnricherRegistry,
    EnrichmentSchemaError,
    build_enrichment_status,
    build_hostname_envelope,
    collect_hostname_candidates,
    load_previous_enrichment,
    normalize_hostname_evidence,
    validate_enrichment_status,
    validate_hostname_envelope,
)
from hioc.inventory import merge_records


NOW = "2026-08-03T12:00:00-06:00"
LATER = "2026-08-03T12:30:00-06:00"
DEVICE_ID = "dev_0123456789abcdef"
MAC = "aa:bb:cc:dd:ee:ff"


def device(device_id=DEVICE_ID):
    return {"id": device_id, "ip": "192.0.2.10", "mac": MAC}


def envelope(records, previous=None, generated_at=NOW, devices=None):
    devices = devices if devices is not None else [device()]
    bindings = {devices[0]["id"]: records} if devices else {}
    candidates = collect_hostname_candidates(bindings, generated_at)
    return build_hostname_envelope(devices, candidates, previous, generated_at)


def hostname(payload, device_id=DEVICE_ID):
    return payload["records"][device_id]["hostname"]


def load_engine_module():
    spec = importlib.util.spec_from_file_location("hioc_inventory_engine_pe1", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CapturingMqttClient:
    calls = []

    def __init__(self, *_args, **_kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def publish(self, topic, payload):
        self.calls.append((topic, copy.deepcopy(payload)))


def public_inventory(evidence=None):
    summary = {
        "updated": NOW,
        "device_count": 1,
        "healthy_count": 1,
        "watch_count": 0,
        "degraded_count": 0,
        "offline_count": 0,
        "service_count": 0,
        "topology_edges": 0,
        "dependency_edges": 0,
        "lowest_health_score": 100,
    }
    result = {
        "schema_version": "1.0",
        "updated": NOW,
        "devices": [{
            **device(),
            "hostname": "public-host",
            "name": "Public Name",
            "display_name": "Public Name",
            "health_status": "healthy",
            "observation_status": "recent",
        }],
        "services": [],
        "topology": {"root_id": DEVICE_ID, "edges": []},
        "dependencies": {"edges": []},
        "summary": summary,
        "_capabilities": [],
        "_hostname_evidence": evidence if evidence is not None else {
            DEVICE_ID: [{"hostname": "lease-host", "source": "dhcp_leases", "dhcp_lease_source": "/private/leases"}]
        },
    }
    return result


class HostnameNormalizationTests(unittest.TestCase):
    def test_empty_and_wildcard_are_rejected(self):
        for value in ("", "   ", "*"):
            with self.subTest(value=value):
                self.assertIsNone(normalize_hostname_evidence(value))

    def test_case_unicode_idna_and_trailing_dot_normalize_deterministically(self):
        values = ["BÜCHER.Example.", "bücher.example", "xn--bcher-kva.example"]
        normalized = [normalize_hostname_evidence(value) for value in values]
        self.assertEqual({item["normalized_value"] for item in normalized}, {"xn--bcher-kva.example"})
        self.assertEqual(normalized[0]["display_value"], "BÜCHER.Example")

    def test_local_lan_and_short_names_are_not_collapsed(self):
        values = ["host", "host.local", "host.lan"]
        normalized = [normalize_hostname_evidence(value)["normalized_value"] for value in values]
        self.assertEqual(normalized, values)

    def test_placeholders_ip_and_mac_are_retained_nonselectable(self):
        values = ["unknown", "localhost", "localhost.localdomain", "192.0.2.1", "2001:db8::1", MAC, "device-aabbccddeeff"]
        for value in values:
            with self.subTest(value=value):
                item = normalize_hostname_evidence(value)
                self.assertEqual(item["quality"], "placeholder")
                self.assertFalse(item["selectable"])

    def test_generated_and_nonstandard_names_are_low_quality_selectable(self):
        for value in ("android-ab12", "ESP_AB12", "DESKTOP-ABC1", "device", "router", "sensor_node"):
            with self.subTest(value=value):
                item = normalize_hostname_evidence(value)
                self.assertEqual(item["quality"], "low")
                self.assertTrue(item["selectable"])

    def test_invalid_characters_separators_and_lengths_are_nonselectable(self):
        values = ["bad name", "bad..name", "-bad", "bad-", "x" * 64 + ".lan", "a." + "b" * 252]
        for value in values:
            with self.subTest(value=value):
                item = normalize_hostname_evidence(value)
                self.assertEqual(item["quality"], "invalid")
                self.assertFalse(item["selectable"])


class HostnameSourceAndSelectionTests(unittest.TestCase):
    def test_each_approved_source_is_collected_with_stable_identity(self):
        records = [
            {"hostname": "known-host", "source": "known_infrastructure", "_observed": False},
            {"hostname": "integration-host", "source": "integration:controller"},
            {"hostname": "local-host", "source": "local_host"},
            {"hostname": "lease-host", "source": "dhcp_leases", "dhcp_lease_source": "/etc/pihole/dhcp.leases"},
        ]
        candidates = collect_hostname_candidates({DEVICE_ID: records}, NOW)[DEVICE_ID]
        self.assertEqual(len(candidates), 4)
        self.assertEqual({item["source_type"] for item in candidates}, {
            "configured_infrastructure", "trusted_integration", "direct_observation", "assignment_observation",
        })
        dhcp = next(item for item in candidates if item["source_type"] == "assignment_observation")
        self.assertRegex(dhcp["source_id"], r"^dhcp_leases:[0-9a-f]{12}$")
        self.assertNotIn("/etc", json.dumps(candidates))

    def test_unapproved_name_arp_service_and_unbound_sources_are_excluded(self):
        records = [
            {"name": "Display Name", "source": "known_infrastructure", "_observed": False},
            {"hostname": "arp-host", "source": "arp_table"},
            {"hostname": "service-host", "source": "systemd"},
            {"hostname": "reverse-host", "source": "active_network"},
            {"hostname": "mqtt-host", "source": "mqtt"},
            {"hostname": "ha-host", "source": "home_assistant"},
            {"hostname": "ambiguous", "sources": ["integration:a", "arp_table"]},
        ]
        candidates = collect_hostname_candidates({DEVICE_ID: records}, NOW)[DEVICE_ID]
        self.assertEqual(candidates, [])

    def test_private_acquisition_source_prevents_integration_source_spoofing(self):
        record = {
            "hostname": "integration-host",
            "source": "local_host",
            "_enrichment_source": "integration:controller",
        }
        candidate = collect_hostname_candidates({DEVICE_ID: [record]}, NOW)[DEVICE_ID][0]
        self.assertEqual(candidate["source_id"], "integration:controller")
        self.assertEqual(candidate["authority"], "trusted_enrichment")

    def test_authority_order_is_known_integration_local_dhcp(self):
        records = [
            {"hostname": "dhcp", "source": "dhcp_leases", "dhcp_lease_source": "/leases"},
            {"hostname": "local", "source": "local_host"},
            {"hostname": "integration", "source": "integration:z"},
            {"hostname": "known", "source": "known_infrastructure", "_observed": False},
        ]
        result = envelope(records)
        selected = hostname(result)["selected_candidate_id"]
        self.assertEqual(next(item["normalized_value"] for item in hostname(result)["candidates"] if item["candidate_id"] == selected), "known")
        self.assertEqual(hostname(result)["selection_rule"], "configured_fact")

    def test_same_normalized_value_is_agreement_not_conflict(self):
        records = [
            {"hostname": "Host.LAN.", "source": "local_host"},
            {"hostname": "host.lan", "source": "integration:a"},
        ]
        result = envelope(records)
        self.assertFalse(hostname(result)["conflict"])
        self.assertEqual(hostname(result)["evidence_status"], "selected_with_agreement")
        self.assertEqual(hostname(result)["selection_rule"], "source_agreement")

    def test_fqdn_short_and_multiple_active_values_conflict(self):
        records = [
            {"hostname": "host", "source": "local_host"},
            {"hostname": "host.lan", "source": "integration:a"},
        ]
        result = envelope(records)
        self.assertTrue(hostname(result)["conflict"])
        self.assertEqual(result["conflict_count"], 1)
        self.assertEqual({item["conflict_status"] for item in hostname(result)["candidates"]}, {"active_conflict"})

    def test_placeholders_do_not_conflict_with_selectable_values(self):
        records = [
            {"hostname": "unknown", "source": "known_infrastructure", "_observed": False},
            {"hostname": "real-host", "source": "dhcp_leases", "dhcp_lease_source": "/leases"},
        ]
        result = envelope(records)
        self.assertFalse(hostname(result)["conflict"])
        selected = next(item for item in hostname(result)["candidates"] if item["selected"])
        self.assertEqual(selected["normalized_value"], "real-host")

    def test_duplicate_records_deduplicate_and_equal_authority_uses_lexical_tie(self):
        records = [
            {"hostname": "Zulu", "source": "integration:a"},
            {"hostname": "zulu", "source": "integration:a"},
            {"hostname": "alpha", "source": "integration:b"},
        ]
        result = envelope(records)
        self.assertEqual(result["candidate_count"], 2)
        selected = next(item for item in hostname(result)["candidates"] if item["selected"])
        self.assertEqual(selected["normalized_value"], "alpha")

    def test_input_permutations_and_serialization_are_deterministic(self):
        records = [
            {"hostname": "dhcp", "source": "dhcp_leases", "dhcp_lease_source": "/z"},
            {"hostname": "local", "source": "local_host"},
            {"hostname": "integration", "source": "integration:b"},
        ]
        outputs = []
        for order in (records, list(reversed(records)), [records[1], records[2], records[0]]):
            outputs.append(json.dumps(envelope(order), indent=2, sort_keys=True))
        self.assertEqual(len(set(outputs)), 1)

    def test_missing_source_timestamps_are_null_and_availability_is_explicit(self):
        result = envelope([{"hostname": "host", "source": "local_host"}])
        candidate = hostname(result)["candidates"][0]
        self.assertIsNone(candidate["observed_at"])
        self.assertEqual(candidate["first_available_at"], NOW)
        self.assertEqual(candidate["last_available_at"], NOW)


class HostnameLifecycleAndSchemaTests(unittest.TestCase):
    def test_active_to_historical_transition_lasts_one_generation(self):
        first = envelope([{"hostname": "old", "source": "local_host"}])
        second = envelope([{"hostname": "new", "source": "local_host"}], first, LATER)
        old = next(item for item in hostname(second)["candidates"] if item["normalized_value"] == "old")
        self.assertEqual(old["state"], "historical")
        self.assertEqual(old["conflict_status"], "historical_disagreement")
        self.assertFalse(hostname(second)["conflict"])
        third = envelope([{"hostname": "new", "source": "local_host"}], second, "2026-08-03T13:00:00-06:00")
        self.assertEqual({item["normalized_value"] for item in hostname(third)["candidates"]}, {"new"})

    def test_historical_fallback_is_selected_when_current_evidence_disappears(self):
        first = envelope([{"hostname": "old", "source": "local_host"}])
        second = envelope([], first, LATER)
        self.assertEqual(hostname(second)["selection_rule"], "historical_fallback")
        self.assertEqual(hostname(second)["candidates"][0]["state"], "historical")

    def test_no_candidate_empty_inventory_multiple_devices_and_disappearance(self):
        empty_name = envelope([])
        self.assertEqual(hostname(empty_name)["evidence_status"], "no_evidence")
        empty_inventory = build_hostname_envelope([], {}, None, NOW)
        self.assertEqual(empty_inventory["record_count"], 0)
        second_id = "dev_fedcba9876543210"
        multiple = build_hostname_envelope([device(second_id), device()], {}, None, NOW)
        self.assertEqual(list(multiple["records"]), sorted([DEVICE_ID, second_id]))
        disappeared = build_hostname_envelope([device(second_id)], {}, multiple, LATER)
        self.assertNotIn(DEVICE_ID, disappeared["records"])

    def test_strict_schema_rejects_unknown_fields_counts_and_candidate_tampering(self):
        valid = envelope([{"hostname": "host", "source": "local_host"}])
        mutations = []
        unknown = copy.deepcopy(valid); unknown["unexpected"] = True; mutations.append(unknown)
        count = copy.deepcopy(valid); count["candidate_count"] = 99; mutations.append(count)
        candidate = copy.deepcopy(valid); candidate["records"][DEVICE_ID]["hostname"]["candidates"][0]["normalized_value"] = "changed"; mutations.append(candidate)
        for payload in mutations:
            with self.subTest(payload=payload), self.assertRaises(EnrichmentSchemaError):
                validate_hostname_envelope(payload)

    def test_status_schema_covers_online_degraded_error_and_unavailable(self):
        artifact = envelope([])
        for value in ("online", "degraded", "error", "unavailable"):
            with self.subTest(value=value):
                error_code = None if value == "online" else "test_condition"
                status = build_enrichment_status(value, NOW, artifact if value in {"online", "degraded"} else None, error_code)
                validate_enrichment_status(status)

    def test_malformed_previous_artifact_is_not_repaired(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "enrichment.json"
            path.write_text('{"broken": true}')
            previous, invalid = load_previous_enrichment(path)
            self.assertIsNone(previous)
            self.assertTrue(invalid)
            self.assertEqual(path.read_text(), '{"broken": true}')

    def test_validator_cli_accepts_valid_and_rejects_malformed(self):
        import subprocess
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            artifact = envelope([])
            status = build_enrichment_status("online", NOW, artifact)
            artifact_path = root / "enrichment.json"; artifact_path.write_text(json.dumps(artifact))
            status_path = root / "status.json"; status_path.write_text(json.dumps(status))
            valid = subprocess.run([sys.executable, str(VALIDATOR), str(artifact_path), str(status_path)], capture_output=True)
            self.assertEqual(valid.returncode, 0)
            artifact_path.write_text("{}")
            invalid = subprocess.run([sys.executable, str(VALIDATOR), str(artifact_path), str(status_path)], capture_output=True)
            self.assertEqual(invalid.returncode, 1)

    def test_state_store_mode_and_atomic_failure_preserve_previous_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = StateStore(Path(tmp))
            store.write_json("enrichment.json", {"old": True}, mode=0o600)
            if os.name != "nt":
                self.assertEqual(os.stat(Path(tmp) / "enrichment.json").st_mode & 0o777, 0o600)
            with patch.object(Path, "replace", side_effect=OSError("replace failed")):
                with self.assertRaises(OSError):
                    store.write_json("enrichment.json", {"new": True}, mode=0o600)
            self.assertEqual(store.read_json("enrichment.json", {}), {"old": True})
            self.assertFalse((Path(tmp) / "enrichment.json.tmp").exists())

    def test_registry_is_ordered_and_prevents_duplicate_bypass(self):
        registry = EnricherRegistry()
        register = lambda name: registry.register(
            name,
            lambda context: [context["value"]],
            lambda values, _context: [value.upper() for value in values],
            "configured_fact",
            "authoritative",
            lambda values, authority, confidence, _context: {
                "values": values, "authority": authority, "confidence": confidence,
            },
        )
        register("zeta")
        register("alpha")
        result = registry.run({"value": "safe"})
        self.assertEqual(list(result), ["alpha", "zeta"])
        self.assertEqual(result["alpha"], {"values": ["SAFE"], "authority": "configured_fact", "confidence": "authoritative"})
        with self.assertRaises(ValueError):
            register("alpha")

    def test_future_enricher_context_cannot_mutate_protected_inventory(self):
        registry = EnricherRegistry()
        registry.register(
            "malicious_test",
            lambda context: context["devices"].pop(),
            lambda value, _context: value,
            "weak_observation",
            "low",
            lambda value, _authority, _confidence, context: context.update({"devices": []}) or value,
        )
        original = {"devices": [{"id": DEVICE_ID, "ip": "192.0.2.10"}]}
        registry.run(original)
        self.assertEqual(original, {"devices": [{"id": DEVICE_ID, "ip": "192.0.2.10"}]})


class ProtectedInvariantTests(unittest.TestCase):
    def test_identity_merge_public_result_is_identical_with_evidence_binding(self):
        records = [
            {"ip": "192.0.2.10", "mac": MAC, "hostname": "strong", "source": "integration:a"},
            {"ip": "192.0.2.11", "mac": MAC, "hostname": "weak", "source": "dhcp_leases", "dhcp_lease_source": "/leases", "lease_expires_epoch": 4102444800, "_positive_observation": False},
        ]
        config = {"HIOC_INVENTORY_STALE_AFTER_SEC": "900", "HIOC_INVENTORY_OFFLINE_AFTER_SEC": "3600"}
        baseline = merge_records(copy.deepcopy(records), {"devices": []}, NOW, 1000, config)
        bindings = {}
        result = merge_records(copy.deepcopy(records), {"devices": []}, NOW, 1000, config, bindings)
        self.assertEqual(result, baseline)
        self.assertEqual(set(bindings), {baseline[0]["id"]})
        protected = ("id", "ip", "hostname", "name", "display_name", "health_status", "observation_status", "source", "sources")
        self.assertEqual({key: result[0].get(key) for key in protected}, {key: baseline[0].get(key) for key in protected})

    def test_engine_writes_private_sidecars_without_public_or_mqtt_changes(self):
        module = load_engine_module()
        CapturingMqttClient.calls = []
        logger = logging.getLogger("test-pe1-engine")
        expected = public_inventory()
        with tempfile.TemporaryDirectory() as tmp, \
                patch.object(module, "load_config", return_value={"HIOC_HOME": tmp, "HIOC_BASE_TOPIC": "hioc"}), \
                patch.object(module, "discover_inventory", side_effect=lambda *_args, **_kwargs: copy.deepcopy(expected)), \
                patch.object(module, "MqttClient", CapturingMqttClient), \
                patch.object(module, "setup_logger", return_value=logger):
            self.assertEqual(module.main(), 0)
            state = Path(tmp) / "state" / "inventory"
            public = json.loads((state / "inventory.json").read_text())
            artifact = json.loads((state / "enrichment.json").read_text())
            status = json.loads((state / "enrichment_status.json").read_text())
            first_artifact_bytes = (state / "enrichment.json").read_bytes()
            CapturingMqttClient.calls = []
            self.assertEqual(module.main(), 0)
            self.assertEqual((state / "enrichment.json").read_bytes(), first_artifact_bytes)
        expected_public = copy.deepcopy(expected); expected_public.pop("_capabilities"); expected_public.pop("_hostname_evidence")
        self.assertEqual(public, expected_public)
        self.assertEqual(status["status"], "online")
        self.assertEqual(artifact["record_count"], 1)
        self.assertEqual([topic for topic, _ in CapturingMqttClient.calls], [
            "hioc/inventory", "hioc/inventory/devices", "hioc/inventory/services",
            "hioc/inventory/topology", "hioc/inventory/dependencies", "hioc/inventory/summary", "hioc/inventory/status",
        ])
        self.assertNotIn("enrichment", json.dumps(CapturingMqttClient.calls))

    def test_engine_failure_is_fail_open_and_preserves_previous_artifact(self):
        module = load_engine_module()
        CapturingMqttClient.calls = []
        logger = logging.getLogger("test-pe1-engine-failure")
        previous = envelope([{"hostname": "old", "source": "local_host"}])
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state" / "inventory"; state.mkdir(parents=True)
            artifact_path = state / "enrichment.json"; artifact_path.write_text(json.dumps(previous, sort_keys=True))
            before = artifact_path.read_bytes()
            with patch.object(module, "load_config", return_value={"HIOC_HOME": tmp, "HIOC_BASE_TOPIC": "hioc"}), \
                    patch.object(module, "discover_inventory", return_value=public_inventory()), \
                    patch.object(module, "collect_hostname_candidates", side_effect=RuntimeError("private-host-value")), \
                    patch.object(module, "MqttClient", CapturingMqttClient), \
                    patch.object(module, "setup_logger", return_value=logger), \
                    self.assertLogs(logger, level="ERROR") as logs:
                self.assertEqual(module.main(), 0)
            self.assertEqual(artifact_path.read_bytes(), before)
            status = json.loads((state / "enrichment_status.json").read_text())
            public = json.loads((state / "inventory.json").read_text())
        self.assertEqual(status["status"], "error")
        self.assertEqual(status["error_code"], "generation_failed")
        self.assertEqual(public["devices"][0]["hostname"], "public-host")
        self.assertEqual(len(CapturingMqttClient.calls), 7)
        self.assertNotIn("private-host-value", "\n".join(logs.output))

    def test_engine_malformed_prior_artifact_generates_degraded_current_artifact(self):
        module = load_engine_module()
        logger = logging.getLogger("test-pe1-degraded")
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state" / "inventory"; state.mkdir(parents=True)
            (state / "enrichment.json").write_text("{}")
            with patch.object(module, "load_config", return_value={"HIOC_HOME": tmp}), \
                    patch.object(module, "discover_inventory", return_value=public_inventory()), \
                    patch.object(module, "MqttClient", CapturingMqttClient), \
                    patch.object(module, "setup_logger", return_value=logger):
                self.assertEqual(module.main(), 0)
            status = json.loads((state / "enrichment_status.json").read_text())
            artifact = json.loads((state / "enrichment.json").read_text())
        self.assertEqual(status["status"], "degraded")
        self.assertEqual(status["error_code"], "prior_artifact_invalid")
        validate_hostname_envelope(artifact)

    def test_engine_status_write_failure_restores_previous_valid_envelope(self):
        module = load_engine_module()
        logger = logging.getLogger("test-pe1-status-write-failure")
        previous = envelope([{"hostname": "old", "source": "local_host"}])
        original_write = module.StateStore.write_json

        def fail_status_write(store, name, payload, schema=None, mode=None):
            if name == "enrichment_status.json":
                raise OSError("status write failed")
            return original_write(store, name, payload, schema, mode)

        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state" / "inventory"; state.mkdir(parents=True)
            path = state / "enrichment.json"; path.write_text(json.dumps(previous, indent=2, sort_keys=True))
            before = path.read_bytes()
            with patch.object(module, "load_config", return_value={"HIOC_HOME": tmp}), \
                    patch.object(module, "discover_inventory", return_value=public_inventory()), \
                    patch.object(module.StateStore, "write_json", new=fail_status_write), \
                    patch.object(module, "MqttClient", CapturingMqttClient), \
                    patch.object(module, "setup_logger", return_value=logger):
                self.assertEqual(module.main(), 0)
            self.assertEqual(path.read_bytes(), before)

    def test_engine_unavailable_evidence_is_not_device_health(self):
        module = load_engine_module()
        logger = logging.getLogger("test-pe1-unavailable")
        value = public_inventory(); value.pop("_hostname_evidence")
        with tempfile.TemporaryDirectory() as tmp, \
                patch.object(module, "load_config", return_value={"HIOC_HOME": tmp}), \
                patch.object(module, "discover_inventory", return_value=value), \
                patch.object(module, "MqttClient", CapturingMqttClient), \
                patch.object(module, "setup_logger", return_value=logger):
            self.assertEqual(module.main(), 0)
            status = json.loads((Path(tmp) / "state" / "inventory" / "enrichment_status.json").read_text())
            public = json.loads((Path(tmp) / "state" / "inventory" / "inventory.json").read_text())
        self.assertEqual(status["status"], "unavailable")
        self.assertEqual(public["devices"][0]["health_status"], "healthy")

    def test_performance_is_bounded_for_1000_devices(self):
        devices = []
        bindings = {}
        for index in range(1000):
            device_id = f"dev_{index:016x}"
            devices.append({"id": device_id})
            bindings[device_id] = [{"hostname": f"host-{index}.lan", "source": "integration:test"}]
        started = time.perf_counter()
        candidates = collect_hostname_candidates(bindings, NOW)
        result = build_hostname_envelope(devices, candidates, None, NOW)
        elapsed = time.perf_counter() - started
        self.assertEqual(result["record_count"], 1000)
        self.assertLess(elapsed, 2.0)


if __name__ == "__main__":
    unittest.main()
