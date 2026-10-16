#!/usr/bin/env python3
"""Explicit private classification; default output is sanitized aggregate counts only."""
import argparse
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"lib"))
from hioc.classification import ClassificationError, POLICY
from hioc.classification_caller import evaluate

class SafeParser(argparse.ArgumentParser):
    def error(self, message): raise ClassificationError("INVALID")

def main(argv=None, evaluator=evaluate):
    try:
        parser=SafeParser(description="Offline private metadata classification; no output file or publication.")
        parser.add_argument("--inventory", required=True)
        for kind in ("assets","known_operator_role","hostname","manufacturer","home_assistant_summary"):
            parser.add_argument("--"+kind.replace("_","-"))
        parser.add_argument("--asset-lock")
        parser.add_argument("--approved-known-sha256")
        parser.add_argument("--manufacturer-database")
        parser.add_argument("--manufacturer-manifest")
        parser.add_argument("--approved-manufacturer-manifest-sha256")
        parser.add_argument("--pe5-handoff",action="store_true")
        args=parser.parse_args(argv)
        policy=dict(POLICY);policy["approved_known_sha256"]=args.approved_known_sha256
        paths={k:getattr(args,k) for k in ("inventory","assets","known_operator_role","hostname","manufacturer","home_assistant_summary")}
        result=evaluator(paths,policy,asset_lock=args.asset_lock,use_pe5=args.pe5_handoff, manufacturer_database=args.manufacturer_database, manufacturer_manifest=args.manufacturer_manifest, approved_manufacturer_manifest_sha256=args.approved_manufacturer_manifest_sha256)
        print(json.dumps(dict(state=result["state"],summary=result["summary"]),sort_keys=True))
        return 1 if result["state"]=="UNAVAILABLE" else 0
    except ClassificationError as error:
        print(json.dumps(dict(error_code=error.code,state="UNAVAILABLE"),sort_keys=True))
        return 1
    except (OSError,ValueError,KeyError):
        print('{"error_code":"UNAVAILABLE","state":"UNAVAILABLE"}')
        return 1
if __name__=="__main__": raise SystemExit(main())
