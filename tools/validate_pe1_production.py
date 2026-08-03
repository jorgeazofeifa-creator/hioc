#!/usr/bin/env python3
"""Validate PE-1 production artifacts without duplicating schema enums."""

import argparse
from datetime import datetime
import json
from pathlib import Path, PurePath
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "pi4" / "lib"))

from hioc.enrichment import (  # noqa: E402
    AUTHORITIES,
    CONFIDENCES,
    SOURCE_TYPES,
    validate_enrichment_status,
    validate_hostname_envelope,
)


def validate_production_artifacts(artifact, status, lower_epoch=None, upper_epoch=None):
    validate_hostname_envelope(artifact)
    validate_enrichment_status(status)
    if status["status"] != "online" or status["error_code"] is not None:
        raise ValueError("PE-1 status is not online")
    for field in ("record_count", "candidate_count", "conflict_count"):
        if status[field] != artifact[field]:
            raise ValueError(f"status {field} does not match artifact")

    generated_epoch = datetime.fromisoformat(
        artifact["generated_at"].replace("Z", "+00:00")
    ).timestamp()
    if lower_epoch is not None and generated_epoch < lower_epoch:
        raise ValueError("artifact generation predates the validation window")
    if upper_epoch is not None and generated_epoch > upper_epoch:
        raise ValueError("artifact generation exceeds the validation window")

    source_types = set()
    selected_count = 0
    historical_max = 0
    for record in artifact["records"].values():
        hostname = record["hostname"]
        selected_count += int(hostname["selected_candidate_id"] is not None)
        historical_count = sum(
            candidate["state"] == "historical"
            for candidate in hostname["candidates"]
        )
        historical_max = max(historical_max, historical_count)
        if historical_count > 1:
            raise ValueError("historical candidate bound exceeded")
        for candidate in hostname["candidates"]:
            if candidate["source_type"] not in SOURCE_TYPES:
                raise ValueError("candidate source type is invalid")
            if candidate["authority"] not in AUTHORITIES:
                raise ValueError("candidate authority is invalid")
            if candidate["confidence"] not in CONFIDENCES:
                raise ValueError("candidate confidence is invalid")
            if PurePath(candidate["source_id"]).is_absolute():
                raise ValueError("candidate source identifier exposes an absolute path")
            if candidate["source_type"] != "historical":
                source_types.add(candidate["source_type"])

    return {
        "schema_version": artifact["schema_version"],
        "health_mapping": "online",
        "record_count": artifact["record_count"],
        "candidate_count": artifact["candidate_count"],
        "selected_count": selected_count,
        "conflict_count": artifact["conflict_count"],
        "historical_max_per_record": historical_max,
        "approved_source_types_observed": sorted(source_types),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact")
    parser.add_argument("status")
    parser.add_argument("--lower-epoch", type=int)
    parser.add_argument("--upper-epoch", type=int)
    parser.add_argument("--summary")
    args = parser.parse_args()
    try:
        artifact = json.loads(Path(args.artifact).read_text(encoding="utf-8"))
        status = json.loads(Path(args.status).read_text(encoding="utf-8"))
        summary = validate_production_artifacts(
            artifact, status, args.lower_epoch, args.upper_epoch
        )
        if args.summary:
            Path(args.summary).write_text(
                json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
            )
        print("PE1_PRODUCTION_VALIDATION=PASS")
        print(f"RECORD_COUNT={summary['record_count']}")
        print(f"CANDIDATE_COUNT={summary['candidate_count']}")
        print(f"SELECTED_COUNT={summary['selected_count']}")
        print(f"CONFLICT_COUNT={summary['conflict_count']}")
        print("SOURCE_TYPES_OBSERVED=" + ",".join(summary["approved_source_types_observed"]))
        return 0
    except Exception as exc:
        print(f"PE1_PRODUCTION_VALIDATION=FAIL code={type(exc).__name__}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
