#!/usr/bin/env python3
"""Two-phase deletion of explicitly approved PE-2 synthetic-only backups."""

import argparse
import hashlib
import json
import os
import pathlib
try:
    import pwd
    import grp
except ImportError:  # Production is Linux; tests inject metadata on Windows.
    pwd = grp = None
import stat
import sys

from hioc.assets import BACKUP_RE, validate_store

RESERVED_ID = "dev_0000000000000000"
EXPECTED_ROOT = pathlib.Path("/home/jazofv1/hioc/backups/assets")
MANIFEST_KEYS = {"schema_version", "purpose", "entries"}
ENTRY_KEYS = {"basename", "sha256"}


class CleanupError(Exception):
    pass


def _load_manifest(path):
    with pathlib.Path(path).open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict) or set(value) != MANIFEST_KEYS:
        raise CleanupError("manifest_schema_invalid")
    if value["schema_version"] != 1 or value["purpose"] not in {
        "one-time-pe2-production-validation-cleanup", "current-run-pe2-validation-cleanup"
    }:
        raise CleanupError("manifest_contract_invalid")
    if not isinstance(value["entries"], list) or not value["entries"]:
        raise CleanupError("manifest_entries_invalid")
    seen = set()
    for entry in value["entries"]:
        if not isinstance(entry, dict) or set(entry) != ENTRY_KEYS:
            raise CleanupError("manifest_entry_invalid")
        name, digest = entry["basename"], entry["sha256"]
        if not isinstance(name, str) or pathlib.PurePath(name).name != name or not BACKUP_RE.fullmatch(name):
            raise CleanupError("manifest_basename_invalid")
        if name in seen or not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
            raise CleanupError("manifest_digest_invalid")
        seen.add(name)
    return value


def _metadata(path):
    if pwd is None or grp is None:
        raise CleanupError("platform_metadata_unavailable")
    info = path.lstat()
    return stat.S_IMODE(info.st_mode), pwd.getpwuid(info.st_uid).pw_name, grp.getgrgid(info.st_gid).gr_name, info


def validate_candidates(manifest, backup_root, metadata=_metadata):
    root = pathlib.Path(backup_root)
    if root.is_symlink() or not root.is_dir():
        raise CleanupError("backup_root_invalid")
    validated = []
    for entry in manifest["entries"]:
        path = root / entry["basename"]
        if path.parent.resolve() != root.resolve():
            raise CleanupError("candidate_outside_backup_root")
        mode, owner, group, info = metadata(path)
        if stat.S_ISLNK(info.st_mode): raise CleanupError("candidate_symlink")
        if not stat.S_ISREG(info.st_mode): raise CleanupError("candidate_not_regular")
        if mode != 0o600 or owner != "jazofv1" or group != "jazofv1": raise CleanupError("candidate_metadata_invalid")
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != entry["sha256"]: raise CleanupError("candidate_digest_mismatch")
        try: store = validate_store(json.loads(raw.decode("utf-8")))
        except Exception as exc: raise CleanupError("candidate_asset_schema_invalid") from exc
        if store["asset_count"] != 1 or set(store["assets"]) != {RESERVED_ID}:
            raise CleanupError("candidate_not_synthetic_only")
        validated.append({"basename": entry["basename"], "sha256": entry["sha256"], "record_count": 1,
                          "creation_role": "pe2_validation", "synthetic_only": True})
    return validated


def run(manifest_path, backup_root, delete=False, metadata=_metadata):
    report = {"schema_version": 1, "cleanup_result": "VALIDATION_FAIL", "files_validated": 0,
              "files_deleted": 0, "validated_files": [], "deleted_basenames": [], "remaining_basenames": [],
              "current_store_changed": False, "current_status_changed": False,
              "real_asset_records_touched": False, "rollback_recommended": False, "error_code": None}
    try:
        manifest = _load_manifest(manifest_path)
        validated = validate_candidates(manifest, backup_root, metadata)
        report["files_validated"] = len(validated)
        report["validated_files"] = validated
        report["remaining_basenames"] = [row["basename"] for row in validated]
        if not delete:
            report["cleanup_result"] = "VALIDATED"
            return report, 0
        root = pathlib.Path(backup_root)
        for row in validated:
            try: (root / row["basename"]).unlink()
            except OSError:
                report["cleanup_result"] = "PARTIAL_DELETE_FAILURE"
                report["error_code"] = "exact_delete_failed"
                return report, 30
            report["deleted_basenames"].append(row["basename"])
            report["files_deleted"] += 1
            report["remaining_basenames"].remove(row["basename"])
        report["cleanup_result"] = "PASS"
        return report, 0
    except (CleanupError, OSError, ValueError, json.JSONDecodeError) as exc:
        report["error_code"] = str(exc).split(":", 1)[0]
        return report, 20


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--backup-root", type=pathlib.Path, default=EXPECTED_ROOT)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--validate-only", action="store_true")
    action.add_argument("--delete", action="store_true")
    args = parser.parse_args(argv)
    if args.backup_root != EXPECTED_ROOT and not os.environ.get("HIOC_PE2_CLEANUP_TESTING"):
        result, rc = ({"schema_version": 1, "cleanup_result": "VALIDATION_FAIL", "files_validated": 0,
                       "files_deleted": 0, "current_store_changed": False, "current_status_changed": False,
                       "real_asset_records_touched": False, "rollback_recommended": False,
                       "error_code": "backup_root_not_approved"}, 20)
    else:
        result, rc = run(args.manifest, args.backup_root, args.delete)
    print(json.dumps(result, indent=2, sort_keys=True))
    return rc


if __name__ == "__main__": raise SystemExit(main())
