#!/usr/bin/env python3
"""Validate and deterministically render a sanitized PE-2 Evidence Report."""

import json
import sys


def normalize_report(payload):
    if not isinstance(payload, dict):
        raise ValueError("report must be an object")
    if not isinstance(payload.get("rollback_recommended"), bool):
        raise ValueError("rollback_recommended must be Boolean")
    if not isinstance(payload.get("warnings"), list) or not all(isinstance(v, str) for v in payload["warnings"]):
        raise ValueError("warnings must be a string array")
    if payload.get("rollback_command") is not None and not isinstance(payload["rollback_command"], str):
        raise ValueError("rollback_command must be string or null")
    return payload


def main():
    try:
        payload = normalize_report(json.load(sys.stdin))
    except Exception:
        print('{"error":"invalid sanitized Evidence Report input"}', file=sys.stderr)
        return 2
    json.dump(payload, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
