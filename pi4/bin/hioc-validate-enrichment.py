#!/usr/bin/env python3
import json
import sys
from pathlib import Path


HIOC_HOME = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(HIOC_HOME / "pi4" / "lib"))

from hioc.enrichment import validate_enrichment_status, validate_hostname_envelope


def main() -> int:
    if len(sys.argv) != 3:
        print("hostname enrichment validation failed: invalid arguments", file=sys.stderr)
        return 2
    try:
        enrichment = json.loads(Path(sys.argv[1]).read_text())
        status = json.loads(Path(sys.argv[2]).read_text())
        validate_hostname_envelope(enrichment)
        validate_enrichment_status(status)
    except Exception:
        print("hostname enrichment validation failed: invalid artifact", file=sys.stderr)
        return 1
    print("hostname enrichment validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
