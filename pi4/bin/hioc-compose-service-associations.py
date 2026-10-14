#!/usr/bin/env python3
"""Private standalone composer; fixed paths, no configuration or environment fallback."""
import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
from hioc.configured_association import AssociationError
from hioc.configured_association_store import Store


class SafeParser(argparse.ArgumentParser):
    def error(self, message):
        raise AssociationError("WRITE_FAILED", "ARGUMENT_INVALID")


def main(argv=None, store_factory=Store):
    try:
        SafeParser(description="Compose private local configured relationships.").parse_args(argv)
        result = store_factory().composer(datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"))
        code = result["configured"]["error_code"]
        print("RESULT=" + ("PASS_PRIVATE_ASSOCIATIONS" if result["state"] == "VALID" and code is None else "FAIL_PRIVATE_ASSOCIATIONS"))
        print("ERROR_CODE=" + (code or "NONE"))
        print("ACCEPTED_COUNT=" + str(len(result["configured"]["associations"])))
        print("REJECTED_COUNT=" + str(len(result["configured"]["rejections"])))
        return 0 if result["state"] == "VALID" and code is None else 1
    except AssociationError as error:
        print("RESULT=FAIL_PRIVATE_ASSOCIATIONS")
        print("ERROR_CODE=" + error.code)
        print("PERSISTENCE_PHASE=" + (error.phase or "NONE"))
        return 1
    except (OSError, KeyError, ValueError):
        print("RESULT=FAIL_PRIVATE_ASSOCIATIONS\nERROR_CODE=WRITE_FAILED")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
