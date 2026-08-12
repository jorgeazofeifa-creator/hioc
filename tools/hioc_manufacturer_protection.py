#!/usr/bin/env python3
"""Semantic manufacturer-state protection for PE-3 deployment."""

import argparse
import hashlib
import json
import os
import pathlib
import stat
import sys

try:
    import grp
    import pwd
except ImportError:  # pragma: no cover - POSIX production dependency
    grp = None
    pwd = None


def _node(path):
    path = pathlib.Path(path)
    if not path.exists() and not path.is_symlink():
        return {"type": "absent"}
    info = path.lstat()
    base = {
        "mode": stat.S_IMODE(info.st_mode),
        "owner": pwd.getpwuid(info.st_uid).pw_name if pwd else str(info.st_uid),
        "group": grp.getgrgid(info.st_gid).gr_name if grp else str(info.st_gid),
    }
    if path.is_symlink():
        return {**base, "type": "symlink", "target": os.readlink(path)}
    if path.is_dir():
        return {**base, "type": "directory"}
    if path.is_file():
        return {
            **base,
            "type": "regular",
            "bytes": info.st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        }
    return {**base, "type": "other"}


def snapshot(runtime):
    runtime = pathlib.Path(runtime)
    root = runtime / "data" / "manufacturer"
    versions = root / "versions"
    payload = []
    if versions.is_dir() and not versions.is_symlink():
        for path in sorted(versions.rglob("*"), key=lambda item: item.as_posix()):
            payload.append(
                {"path": path.relative_to(versions).as_posix(), **_node(path)}
            )
    return {
        "schema_version": 1,
        "manufacturer_root": _node(root),
        "manufacturer_root_entries": (
            sorted(item.name for item in root.iterdir())
            if root.is_dir() and not root.is_symlink()
            else []
        ),
        "versions_root": _node(versions),
        "payload": payload,
        "sidecar": _node(runtime / "state" / "inventory" / "manufacturer.json"),
        "status": _node(
            runtime / "state" / "inventory" / "manufacturer_status.json"
        ),
        "configuration": _node(runtime / "config" / "hioc.conf"),
    }


def _valid_root(node, *, after):
    if node["type"] == "absent":
        return not after
    if node["type"] != "directory":
        return False
    if node.get("owner") != "jazofv1" or node.get("group") != "jazofv1":
        return False
    return not after or node.get("mode") == 0o700


def compare(before, after):
    if before.get("schema_version") != 1 or after.get("schema_version") != 1:
        return False, "SNAPSHOT_SCHEMA_INVALID"
    if not _valid_root(before["manufacturer_root"], after=False):
        return False, "PREDEPLOY_SCAFFOLD_INVALID"
    if not _valid_root(before["versions_root"], after=False):
        return False, "PREDEPLOY_SCAFFOLD_INVALID"
    if not _valid_root(after["manufacturer_root"], after=True):
        return False, "POSTDEPLOY_SCAFFOLD_INVALID"
    if not _valid_root(after["versions_root"], after=True):
        return False, "POSTDEPLOY_SCAFFOLD_INVALID"
    if before["manufacturer_root_entries"] not in ([], ["versions"]):
        return False, "PREDEPLOY_UNEXPECTED_ENTRY"
    if after["manufacturer_root_entries"] != ["versions"]:
        return False, "POSTDEPLOY_UNEXPECTED_ENTRY"
    for field in ("payload", "sidecar", "status"):
        if before[field] != after[field]:
            return False, "MANUFACTURER_PAYLOAD_CHANGED"
    if before["configuration"] != after["configuration"]:
        return False, "CONFIGURATION_CHANGED"
    return True, "PASS"


def validate_predeploy(current):
    if current.get("schema_version") != 1:
        return False, "SNAPSHOT_SCHEMA_INVALID"
    if not _valid_root(current["manufacturer_root"], after=False):
        return False, "PREDEPLOY_SCAFFOLD_INVALID"
    if not _valid_root(current["versions_root"], after=False):
        return False, "PREDEPLOY_SCAFFOLD_INVALID"
    if current["manufacturer_root_entries"] not in ([], ["versions"]):
        return False, "PREDEPLOY_UNEXPECTED_ENTRY"
    return True, "PASS"


def validate_empty_current(current):
    absent = {"type": "absent"}
    if not _valid_root(current["manufacturer_root"], after=True):
        return False, "CURRENT_SCAFFOLD_INVALID"
    if not _valid_root(current["versions_root"], after=True):
        return False, "CURRENT_SCAFFOLD_INVALID"
    if current["manufacturer_root_entries"] != ["versions"]:
        return False, "CURRENT_UNEXPECTED_ENTRY"
    if current["payload"]:
        return False, "CURRENT_MANUFACTURER_PAYLOAD_PRESENT"
    if current["sidecar"] != absent or current["status"] != absent:
        return False, "CURRENT_MANUFACTURER_SIDECAR_PRESENT"
    return True, "PASS"


def _read(path):
    return json.loads(pathlib.Path(path).read_text(encoding="utf-8"))


def main(argv=None):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    snap = subparsers.add_parser("snapshot")
    snap.add_argument("--runtime", required=True)
    compare_parser = subparsers.add_parser("compare")
    compare_parser.add_argument("--before", required=True)
    compare_parser.add_argument("--after", required=True)
    current_parser = subparsers.add_parser("validate-empty-current")
    current_parser.add_argument("--snapshot", required=True)
    pre_parser = subparsers.add_parser("validate-predeploy")
    pre_parser.add_argument("--snapshot", required=True)
    args = parser.parse_args(argv)
    if args.command == "snapshot":
        print(json.dumps(snapshot(args.runtime), sort_keys=True, separators=(",", ":")))
        return 0
    if args.command == "compare":
        passed, code = compare(_read(args.before), _read(args.after))
    elif args.command == "validate-empty-current":
        passed, code = validate_empty_current(_read(args.snapshot))
    else:
        passed, code = validate_predeploy(_read(args.snapshot))
    print(json.dumps({"result": "PASS" if passed else "FAIL", "code": code}))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
