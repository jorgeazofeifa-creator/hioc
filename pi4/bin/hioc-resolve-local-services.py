#!/usr/bin/env python3
"""Explicit offline caller for finalized inventory; private stdout, no state writer."""
import argparse
import json
import os
import re
import stat
import sys
from pathlib import Path

HIOC_HOME = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(HIOC_HOME / "pi4" / "lib"))
from hioc.service_association import (
    MAX_SNAPSHOT_BYTES, ServiceAssociationError,
    resolve_service_associations, validate_service_association_envelope,
)


class CallerError(ValueError):
    """Fixed safe codes only; never echo filenames or input data."""


class SafeParser(argparse.ArgumentParser):
    def error(self, message):
        raise CallerError("CALLER_ARGUMENT_INVALID")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise CallerError("SNAPSHOT_JSON_INVALID")
        result[key] = value
    return result


def evaluate_file(inventory_file, evaluated_at, max_snapshot_age_seconds):
    """Read one bounded regular-file snapshot and return a validated private envelope.

    Caller parameters are explicit. No config, clock, collector, prior private state,
    publication, write, recovery, scheduler or production activation is performed.
    A producer's atomic replacement yields one opened version; no multi-file read.
    """
    # Validate caller policy/time before reading any source file.
    from hioc.service_association import _policy, _time
    _policy(max_snapshot_age_seconds)
    _time(evaluated_at, "INVALID_EVALUATION_TIME")
    try:
        path = Path(inventory_file)
        observed = path.lstat()
        if not stat.S_ISREG(observed.st_mode):
            raise CallerError("SNAPSHOT_FILE_UNSAFE")
        flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_NOFOLLOW", 0)
        fd = os.open(path, flags)
        with os.fdopen(fd, "rb") as source:
            opened = os.fstat(source.fileno())
            if not stat.S_ISREG(opened.st_mode) or (opened.st_dev, opened.st_ino) != (observed.st_dev, observed.st_ino):
                raise CallerError("SNAPSHOT_FILE_UNSAFE")
            raw = source.read(MAX_SNAPSHOT_BYTES + 1)
            after = os.fstat(source.fileno())
            if (opened.st_size, opened.st_mtime_ns, opened.st_ctime_ns) != (after.st_size, after.st_mtime_ns, after.st_ctime_ns):
                raise CallerError("SNAPSHOT_FILE_CHANGED")
    except CallerError:
        raise
    except (OSError, TypeError, ValueError):
        raise CallerError("SNAPSHOT_READ_FAILED") from None
    if len(raw) > MAX_SNAPSHOT_BYTES:
        raise CallerError("SNAPSHOT_FILE_LIMIT_EXCEEDED")
    try:
        snapshot = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object)
    except CallerError:
        raise
    except (UnicodeError, ValueError, RecursionError):
        raise CallerError("SNAPSHOT_JSON_INVALID") from None
    envelope = resolve_service_associations(snapshot, evaluated_at, max_snapshot_age_seconds)
    validate_service_association_envelope(envelope)
    return envelope


def main(argv=None):
    parser = SafeParser(description="Evaluate a privately captured finalized inventory offline.")
    parser.add_argument("--inventory-file", required=True)
    parser.add_argument("--evaluated-at", required=True)
    parser.add_argument("--max-snapshot-age-seconds", required=True)
    try:
        args = parser.parse_args(argv)
        if not re.fullmatch(r"(?:0|[1-9][0-9]{0,15})", args.max_snapshot_age_seconds):
            raise CallerError("INVALID_MAX_SNAPSHOT_AGE")
        result = evaluate_file(args.inventory_file, args.evaluated_at,
                               int(args.max_snapshot_age_seconds))
        # Fully resolve, validate and serialize before any output. No public publisher.
        encoded = json.dumps(result, sort_keys=True, separators=(",", ":"),
                             ensure_ascii=True, allow_nan=False) + "\n"
        sys.stdout.write(encoded)
        return 0
    except (CallerError, ServiceAssociationError) as error:
        print(str(error), file=sys.stderr)
        return 1
    except Exception:
        print("CALLER_INTERNAL", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
