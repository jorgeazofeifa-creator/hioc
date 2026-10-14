#!/usr/bin/env python3
"""Explicit operator-approved offline install/recovery; no broker, HA or shell."""
import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
from hioc import configured_association as model
from hioc.configured_association_store import Store, SOURCE, OUTPUT


class SafeParser(argparse.ArgumentParser):
    def error(self, message):
        raise model.AssociationError("WRITE_FAILED", "ARGUMENT_INVALID")


def main(argv=None, store_factory=Store):
    parser = SafeParser(description="Private source installation or explicitly approved durability recovery.")
    sub = parser.add_subparsers(dest="action", required=True, parser_class=SafeParser)
    install = sub.add_parser("install")
    install.add_argument("--candidate-file", required=True)
    install.add_argument("--approved", action="store_true", required=True)
    install.add_argument("--initialize", action="store_true")
    install.add_argument("--fresh-recovery", action="store_true")
    recover = sub.add_parser("recertify")
    recover.add_argument("--domain", choices=["source", "output"], required=True)
    recover.add_argument("--approved", action="store_true", required=True)
    recompute = sub.add_parser("recompute-output")
    recompute.add_argument("--approved", action="store_true", required=True)
    try:
        args = parser.parse_args(argv)
        store = store_factory()
        now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        if args.action == "install":
            snapshot = store.read(Path(args.candidate_file), model.SOURCE_LIMIT)
            value = model.strict_json(snapshot.data, model.SOURCE_LIMIT)
            store.install_source(value, approved=args.approved, initialize=args.initialize, recovery=args.fresh_recovery)
        elif args.action == "recertify":
            store.recertify(SOURCE if args.domain == "source" else OUTPUT, now, args.approved)
        else:
            result = store.composer(now, recovery=True, approved=args.approved)
            if result["state"] != "VALID" or result["configured"]["error_code"] is not None:
                raise model.AssociationError(result["configured"]["error_code"] or "INVENTORY_INVALID")
        print("RESULT=PASS_PRIVATE_PERSISTENCE\nPERSISTENCE_STATE=CONFIRMED_DURABLE_CURRENT")
        return 0
    except model.AssociationError as error:
        print("RESULT=FAIL_PRIVATE_PERSISTENCE")
        print("ERROR_CODE=" + error.code)
        print("PERSISTENCE_PHASE=" + (error.phase or "NONE"))
        return 1
    except (OSError, KeyError, ValueError):
        print("RESULT=FAIL_PRIVATE_PERSISTENCE\nERROR_CODE=WRITE_FAILED")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
