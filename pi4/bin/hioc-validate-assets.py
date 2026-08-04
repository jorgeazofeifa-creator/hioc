#!/usr/bin/env python3
"""Read-only PE-2.1 Asset artifact validator."""

import argparse
import json
import os
import stat
import sys
from pathlib import Path

HIOC_HOME = Path(os.environ.get("HIOC_HOME", "/home/jazofv1/hioc"))
sys.path.insert(0, str(HIOC_HOME / "pi4" / "lib"))

from hioc.assets import (AssetError, AssetStore, AssetValidationError,
                         calculate_orphans, validate_status, validate_store)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Read-only validation of PE-2.1 Asset artifacts")
    parser.add_argument("--home", type=Path, default=HIOC_HOME)
    parser.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def validate_read_only(home: Path) -> dict:
    store = AssetStore(home)
    current = store.load_store()
    status = store.load_status()
    if status["asset_count"] != current["asset_count"]:
        raise AssetValidationError("STORE_SCHEMA_INVALID", "Asset status count differs from store")
    context, orphans = store.inventory_context(current)
    if context == "available" and status["orphaned_asset_count"] != len(orphans):
        raise AssetValidationError("STORE_SCHEMA_INVALID", "Asset orphan count differs from inventory")
    if context != "available" and status["orphaned_asset_count"] is not None:
        raise AssetValidationError("STORE_SCHEMA_INVALID", "Asset orphan count must be unknown")
    if os.name == "posix":
        if stat.S_IMODE(store.state_dir.stat().st_mode) > 0o750:
            raise AssetValidationError("STORE_PERMISSION_ERROR", "Asset state directory mode is unsafe")
        if store.backup_dir.exists() and stat.S_IMODE(store.backup_dir.stat().st_mode) != 0o700:
            raise AssetValidationError("STORE_PERMISSION_ERROR", "Asset backup directory mode is unsafe")
    partials = list(store.state_dir.glob(".assets*.tmp")) if store.state_dir.exists() else []
    if partials:
        raise AssetValidationError("STORE_SCHEMA_INVALID", "Asset temporary files remain")
    return {"schema_version": "1.0", "result": "PASS", "status": status["status"],
            "asset_count": current["asset_count"],
            "orphaned_asset_count": len(orphans) if orphans is not None else None,
            "inventory_context": context, "privacy_safe": True}


def main(argv=None) -> int:
    args = parse_args(argv)
    try:
        result = validate_read_only(args.home)
    except AssetError as exc:
        payload = {"schema_version": "1.0", "result": "FAIL", "error": {"code": exc.code, "message": exc.safe_message}}
        if args.json:
            print(json.dumps(payload, separators=(",", ":")))
        else:
            print(f"asset validation failed | error={exc.code}", file=sys.stderr)
        return exc.exit_code
    except Exception:
        if args.json:
            print('{"schema_version":"1.0","result":"FAIL","error":{"code":"INTERNAL_ERROR","message":"unexpected validator failure"}}')
        else:
            print("asset validation failed | error=INTERNAL_ERROR", file=sys.stderr)
        return 70
    if args.json:
        print(json.dumps(result, separators=(",", ":")))
    else:
        print(f"asset validation passed | status={result['status']} | asset_count={result['asset_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
