#!/usr/bin/env python3
import argparse
import json
import os
import sys
from pathlib import Path

HIOC_HOME = Path(os.environ.get("HIOC_HOME", Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(HIOC_HOME / "pi4" / "lib"))

from hioc.lifecycle import ACTIVE, ARCHIVED, LifecycleError, LifecycleStore


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description="HIOC inventory lifecycle administration")
    command.add_argument("--state-dir", type=Path, default=HIOC_HOME / "state" / "inventory")
    sub = command.add_subparsers(dest="command", required=True)
    sub.add_parser("validate")
    sub.add_parser("audit-status")
    sub.add_parser("repair-audit")
    sub.add_parser("rebuild-event-index")
    sub.add_parser("repair-projections")
    sub.add_parser("list-generations")
    for name in ("archive", "restore"):
        item = sub.add_parser(name)
        item.add_argument("device_id")
        item.add_argument("--reason", required=True)
    rollback = sub.add_parser("rollback")
    rollback.add_argument("generation_id")
    prune = sub.add_parser("prune-generation")
    prune.add_argument("generation_id")
    prune.add_argument("--dry-run", action="store_true", required=True)
    return command


def main() -> int:
    args = parser().parse_args()
    store = LifecycleStore(args.state_dir)
    try:
        if args.command in {"validate", "audit-status", "list-generations"}:
            before = store.current_generation_id()
            generation = store.open_existing_read_only()
            if args.command == "validate":
                result = {
                    "status": "valid", "generation_id": generation["id"],
                    "projection_repairs_required": generation["projection_issues"],
                }
            elif args.command == "audit-status":
                result = store.audit_status()
            else:
                result = store.list_generations()
            if store.current_generation_id() != before:
                raise LifecycleError("CURRENT changed during read-only validation; retry")
            print(json.dumps(result, indent=2, sort_keys=True))
            return 0
        with store.lock():
            if args.command in {"repair-audit", "rebuild-event-index", "repair-projections", "prune-generation"}:
                store.open_existing_read_only()
            else:
                store.initialize_or_migrate()
            if args.command in ("repair-audit", "rebuild-event-index"):
                if args.command == "repair-audit":
                    index = store.repair_audit()
                else:
                    index = store.rebuild_event_index()
                result = {"status": "valid", "event_generations": index.get("receipt_count", 0)}
            elif args.command == "repair-projections":
                store.repair_after_commit()
                result = {"status": "repaired", "generation_id": store.current_generation_id()}
            elif args.command == "list-generations":
                result = store.list_generations()
            elif args.command == "archive":
                result = {"generation_id": store.transition(args.device_id, ARCHIVED, args.reason, os.environ.get("USER", "operator"))["id"]}
            elif args.command == "restore":
                result = {"generation_id": store.transition(args.device_id, ACTIVE, args.reason, os.environ.get("USER", "operator"))["id"]}
            elif args.command == "rollback":
                result = {"generation_id": store.rollback(args.generation_id)["id"]}
            elif args.command == "prune-generation":
                result = store.validate_prune(args.generation_id)
            else:
                raise LifecycleError("unsupported command")
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except LifecycleError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"ERROR: lifecycle state unavailable: {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
