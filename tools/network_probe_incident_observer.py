#!/usr/bin/env python3
"""Bounded, non-failing observation of downstream PI5 incident recovery."""

import argparse
import json
import os
import subprocess
import time

FALSE_KEY = "home_assistant_host_unreachable"
FALSE_EVIDENCE = "PI5 / Home Assistant host is unreachable from Pi4"


def read_incident(args):
    if args.fixture is not None:
        try:
            value = open(args.fixture, encoding="utf-8").read().strip()
        except OSError:
            return None
        return value or None
    command = [
        args.mosquitto_sub,
        "-h", args.host,
        "-p", args.port,
        "-u", args.user,
        "-P", os.environ["MQTT_PASSWORD"],
        "-W", str(args.read_timeout),
        "-C", "1",
        "-t", args.topic,
    ]
    result = subprocess.run(command, capture_output=True, text=True, timeout=args.read_timeout + 2)
    if result.returncode or not result.stdout.strip():
        return None
    return result.stdout.strip()


def observe(args):
    started = time.monotonic()
    deadline = started + args.duration
    successes = failures = malformed = 0
    last_key = "unreadable"
    last_false_evidence = "unknown"
    cleared = False
    first = True
    while first or time.monotonic() < deadline:
        first = False
        try:
            raw = read_incident(args)
        except (OSError, subprocess.TimeoutExpired):
            raw = None
        if raw is None:
            failures += 1
        else:
            successes += 1
            try:
                payload = json.loads(raw)
                if not isinstance(payload, dict):
                    raise ValueError("payload is not an object")
                key = payload.get("key", "")
                evidence = payload.get("evidence", [])
                if not isinstance(evidence, list):
                    raise ValueError("evidence is not a list")
                last_key = str(key or "")
                last_false_evidence = "true" if FALSE_EVIDENCE in evidence else "false"
                if key != FALSE_KEY and FALSE_EVIDENCE not in evidence:
                    cleared = True
                    break
            except (TypeError, ValueError, json.JSONDecodeError):
                malformed += 1
                last_key = "malformed"
                last_false_evidence = "unknown"
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            break
        time.sleep(min(args.interval, remaining))

    elapsed = int(round(time.monotonic() - started))
    if cleared:
        result = "PASS"
        detail = "A successful incident read confirmed that the false PI5 incident is absent."
    elif successes == 0:
        result = "INCONCLUSIVE"
        detail = "Follow-up required: incident topic could not be read reliably."
    elif malformed:
        result = "INCONCLUSIVE"
        detail = "Follow-up required: active incident payload was malformed."
    else:
        result = "FOLLOW-UP REQUIRED"
        detail = "The false PI5 incident remained active beyond the bounded observation window."

    print(f"Incident reads successful: {successes}")
    print(f"Incident read failures/timeouts: {failures}")
    print(f"Malformed incident payloads: {malformed}")
    print(f"Last successfully read incident key: {last_key}")
    print(f"False PI5 evidence in last successful state: {last_false_evidence}")
    print(f"Elapsed observation duration: {elapsed} seconds")
    print(f"PHASE_B_RESULT={result}")
    print(detail)
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", required=True)
    parser.add_argument("--user", required=True)
    parser.add_argument("--topic", required=True)
    parser.add_argument("--duration", type=float, default=190)
    parser.add_argument("--interval", type=float, default=10)
    parser.add_argument("--read-timeout", type=int, default=5)
    parser.add_argument("--mosquitto-sub", default="mosquitto_sub")
    parser.add_argument("--fixture", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if "MQTT_PASSWORD" not in os.environ:
        parser.error("MQTT_PASSWORD must be present in the environment")
    return observe(args)


if __name__ == "__main__":
    raise SystemExit(main())
