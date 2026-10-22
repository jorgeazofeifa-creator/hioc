"""Native temporary-store PE-7 transactions; no production filesystem access."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import uuid
from unittest.mock import patch

from hioc import assets
from hioc.asset_policy import PolicyStore, PolicyService, validate_store, validate_versioned
from hioc.availability_contract import PolicyError, POLICY_FIELDS
from test_assets_schema import store, record, ID, TS


class PolicyAssetsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.storage = PolicyStore(self.home, lock_path=self.home / 'asset.lock')
        self.storage.timestamp = lambda: TS
        self.storage.inventory_context = lambda _: ('available', set())
        self.service = PolicyService(self.storage, lambda _: 'strong')
        self.storage.ensure_directories()
        self.prior = store({ID: record()})
        self.raw = assets.serialize_store(self.prior)
        self.storage.store_path.write_bytes(self.raw)
        self.sha = hashlib.sha256(self.raw).hexdigest()

    def migrate(self):
        return self.service.migrate(self.sha, writers_stopped=True)

    def payload(self, current, fields, *, key=ID):
        return dict(asset_id=key, store_epoch=current['store_epoch'],
                    expected_store_revision=current['store_revision'],
                    expected_revision=current['assets'][key]['revision'] if key in current['assets'] else None,
                    operation_id=uuid.uuid4().hex, fields=fields)

    def test_explicit_migration_preserves_all_historical_values_and_backup(self):
        migrated = self.migrate()
        self.assertEqual(migrated['store_revision'], 1)
        self.assertEqual({k: migrated['assets'][ID][k] for k in assets.RECORD_KEYS}, self.prior['assets'][ID])
        self.assertTrue(all(migrated['assets'][ID][k] is None for k in POLICY_FIELDS))
        self.assertIn(self.raw, [p.read_bytes() for p in self.storage.backup_dir.iterdir()])
        with self.assertRaises(assets.AssetValidationError):
            assets.validate_store(migrated)
        self.assertEqual(validate_versioned(migrated), migrated)

    def test_no_read_migration_or_missing_store_initialization(self):
        with self.assertRaises(PolicyError):
            self.service.get_policy(ID)
        self.assertEqual(self.storage.store_path.read_bytes(), self.raw)
        self.storage.store_path.unlink()
        with self.assertRaises(PolicyError):
            self.service.get_policy(ID)
        self.assertFalse(self.storage.store_path.exists())

    def test_requires_stopped_writers_and_exact_preflight_hash(self):
        for digest, stopped in ((self.sha, False), ('0' * 64, True)):
            with self.assertRaises(PolicyError):
                self.service.migrate(digest, writers_stopped=stopped)
        self.assertEqual(self.storage.store_path.read_bytes(), self.raw)

    def test_independent_policies_and_inactive_type_retention(self):
        current = self.migrate()
        for expected in (True, False, None):
            for infrastructure in (True, False, None):
                payload = self.payload(current, dict(expected_availability=expected,
                    infrastructure_device=infrastructure, infrastructure_type='network_switch'))
                response = self.service.mutate_policy('update', payload, 'issuer', 'actor', lambda: True)
                self.assertIs(response['policy']['expected_availability'], expected)
                self.assertIs(response['policy']['infrastructure_device'], infrastructure)
                self.assertEqual(response['policy']['infrastructure_type'], 'network_switch')
                self.assertEqual(response['policy']['effective_infrastructure_type'],
                                 'network_switch' if infrastructure is True else None)
                current = self.storage.load_store()

    def test_replay_precedes_stale_revision_and_preserves_record_noop(self):
        current = self.migrate()
        payload = self.payload(current, {'expected_availability': False})
        first = self.service.mutate_policy('update', payload, 'issuer', 'actor', lambda: True)
        replay = self.service.mutate_policy('update', payload, 'issuer', 'actor', lambda: True)
        self.assertEqual(replay['result'], 'replayed')
        self.assertEqual(replay['receipt'], first['receipt'])
        modified = copy.deepcopy(payload)
        modified['fields']['expected_availability'] = True
        with self.assertRaises(PolicyError) as caught:
            self.service.mutate_policy('update', modified, 'issuer', 'actor', lambda: True)
        self.assertEqual(caught.exception.code, 'REPLAY_CONFLICT')
        current = self.storage.load_store()
        before = copy.deepcopy(current['assets'][ID])
        self.service.mutate_policy('update', self.payload(current, {'expected_availability': False}),
                                   'issuer', 'actor', lambda: True)
        after = self.storage.load_store()
        self.assertEqual(after['assets'][ID], before)
        self.assertEqual(after['store_revision'], current['store_revision'] + 1)

    def test_stale_concurrent_revision_denied(self):
        current = self.migrate()
        first = self.payload(current, {'expected_availability': False})
        second = self.payload(current, {'infrastructure_device': True})
        self.service.mutate_policy('update', first, 'issuer', 'actor', lambda: True)
        with self.assertRaises(PolicyError) as caught:
            self.service.mutate_policy('update', second, 'issuer', 'actor', lambda: True)
        self.assertEqual(caught.exception.code, 'REVISION_CONFLICT')

    def test_existing_orphan_off_allowed_on_denied(self):
        current = self.migrate()
        self.service.attachment = lambda _: 'orphan'
        self.service.mutate_policy('update', self.payload(current, {'expected_availability': False}),
                                   'issuer', 'actor', lambda: True)
        current = self.storage.load_store()
        with self.assertRaises(PolicyError) as caught:
            self.service.mutate_policy('update', self.payload(current, {'expected_availability': True}),
                                       'issuer', 'actor', lambda: True)
        self.assertEqual(caught.exception.code, 'IDENTITY_UNSAFE')

    def test_policy_only_create_preserves_real_ha_provenance(self):
        current = self.migrate()
        new_id = 'dev_1111111111111111'
        response = self.service.mutate_policy('create', self.payload(current,
            {'expected_availability': False}, key=new_id), 'issuer', 'actor', lambda: True)
        self.assertEqual(response['result'], 'created')
        current = self.storage.load_store()
        self.assertEqual(current['assets'][new_id]['update_source'], 'operator_ha')
        self.assertTrue(all(current['assets'][new_id][k] is None for k in assets.OPERATOR_FIELDS))
        validate_store(current)

    def test_post_replace_status_failure_is_unknown_not_success(self):
        current = self.migrate()
        payload = self.payload(current, {'expected_availability': False})
        with patch.object(self.service, '_write_status', side_effect=OSError('private detail')):
            with self.assertRaises(PolicyError) as caught:
                self.service.mutate_policy('update', payload, 'issuer', 'actor', lambda: True)
        self.assertEqual(caught.exception.code, 'COMMIT_UNKNOWN')
        self.assertTrue(caught.exception.uncertain)
        self.assertIs(self.storage.load_store()['assets'][ID]['expected_availability'], False)

    def test_rollback_exact_legacy_bytes_and_remigration_rotates_epoch(self):
        first = self.migrate()
        backup = next(p.name for p in self.storage.backup_dir.iterdir() if p.read_bytes() == self.raw)
        with self.assertRaises(PolicyError):
            self.service.restore_exact(backup, writers_stopped=True)
        self.service.restore_exact(backup, writers_stopped=True, retain_later_edits=True)
        self.assertEqual(self.storage.store_path.read_bytes(), self.raw)
        second = self.migrate()
        self.assertNotEqual(first['store_epoch'], second['store_epoch'])

    def test_closed_schema_types_and_receipts(self):
        current = self.migrate()
        for name, value in (('expected_availability', 1), ('infrastructure_device', 'true'),
                            ('infrastructure_type', 'router')):
            bad = copy.deepcopy(current)
            bad['assets'][ID][name] = value
            with self.assertRaises(PolicyError):
                validate_store(bad)
        for update in ({'schema_version': '3.0'}, {'policy_requests': [{}]}, {'extra': 1}):
            bad = copy.deepcopy(current)
            bad.update(update)
            with self.assertRaises(PolicyError):
                validate_versioned(bad)


if __name__ == '__main__':
    unittest.main()
