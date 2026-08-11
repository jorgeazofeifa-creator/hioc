#!/usr/bin/env python3
"""Strictly read-only PE-3.1 manufacturer artifact validator."""
import argparse, json, os, pathlib, stat, sys
HOME = pathlib.Path(os.environ.get("HIOC_HOME", "/home/jazofv1/hioc")); sys.path.insert(0, str(HOME / "pi4" / "lib"))
from hioc.manufacturer import *
class Parser(argparse.ArgumentParser):
    pass
def parser():
    root=Parser(); sub=root.add_subparsers(dest="target",required=True)
    db=sub.add_parser("database"); db.add_argument("--database",required=True); db.add_argument("--manifest",required=True); db.add_argument("--json",action="store_true")
    side=sub.add_parser("sidecar"); side.add_argument("--sidecar",required=True); side.add_argument("--status",required=True); side.add_argument("--inventory"); side.add_argument("--database"); side.add_argument("--manifest"); side.add_argument("--json",action="store_true"); return root
def read(path_text, code):
    path=pathlib.Path(path_text)
    if not path.is_absolute() or path.is_symlink() or not path.is_file(): raise ManufacturerValidationError(code,"validation file is invalid")
    if os.name=="posix" and stat.S_IMODE(path.stat().st_mode)&~0o600: raise ManufacturerUnavailableError("MANUFACTURER_PERMISSION_ERROR","file mode is unsafe")
    try: document=json.loads(path.read_text(encoding="utf-8"),object_pairs_hook=dict)
    except (OSError,UnicodeError,json.JSONDecodeError) as exc: raise ManufacturerValidationError(code,"validation JSON is invalid") from exc
    return document,path
def run(argv=None):
    json_mode="--json" in (argv if argv is not None else sys.argv[1:]); target="database"
    try:
        args=parser().parse_args(argv); target=args.target; json_mode=args.json; record_count=matched_count=None; status=None
        if target=="database":
            dbp=pathlib.Path(args.database); mfp=pathlib.Path(args.manifest)
            if dbp.parent!=mfp.parent: raise ManufacturerInputError("MANUFACTURER_MANIFEST_SCHEMA_INVALID","database and manifest directory differ")
            if dbp.name!="manufacturer-db.json" or mfp.name!="manufacturer-db.manifest.json": raise ManufacturerInputError("MANUFACTURER_MANIFEST_SCHEMA_INVALID","manufacturer pair basenames are invalid")
            if any(p.name.startswith(".manufacturer") and p.name.endswith(".tmp") for p in dbp.parent.iterdir()): raise ManufacturerValidationError("MANUFACTURER_MANIFEST_SCHEMA_INVALID","temporary manufacturer sibling exists")
            db=load_database(dbp,mfp); record_count=db.document["record_count"]
        else:
            if bool(args.database)!=bool(args.manifest): raise ManufacturerInputError("MANUFACTURER_MANIFEST_SCHEMA_INVALID","database and manifest must appear together")
            side,_=read(args.sidecar,"MANUFACTURER_SIDECAR_INVALID"); statdoc,_=read(args.status,"MANUFACTURER_STATUS_INVALID")
            try: side=validate_manufacturer_sidecar(side)
            except ManufacturerError as exc: raise ManufacturerValidationError("MANUFACTURER_SIDECAR_INVALID",exc.safe_message) from exc
            try: statdoc=validate_manufacturer_status(statdoc)
            except ManufacturerError as exc: raise ManufacturerValidationError("MANUFACTURER_STATUS_INVALID",exc.safe_message) from exc
            if statdoc["status"]=="online" and any(statdoc[k]!=side[k] for k in ("record_count","matched_count","unknown_count","excluded_count","invalid_count","dataset_version","dataset_semantic_sha256")): raise ManufacturerValidationError("MANUFACTURER_STATUS_INVALID","sidecar and status differ")
            if args.inventory:
                inv,_=read(args.inventory,"MANUFACTURER_INVENTORY_INVALID"); ids=[]
                if not isinstance(inv,dict) or not isinstance(inv.get("devices"),list): raise ManufacturerValidationError("MANUFACTURER_INVENTORY_INVALID","inventory is invalid")
                for item in inv["devices"]:
                    if not isinstance(item,dict) or not isinstance(item.get("id"),str): raise ManufacturerValidationError("MANUFACTURER_INVENTORY_INVALID","inventory is invalid")
                    ids.append(item["id"])
                if sorted(ids)!=list(side["records"]): raise ManufacturerValidationError("MANUFACTURER_SIDECAR_INVALID","inventory and sidecar IDs differ")
            if args.database:
                db=load_database(pathlib.Path(args.database),pathlib.Path(args.manifest))
                if side["dataset_version"]!=db.document["dataset_version"] or side["dataset_semantic_sha256"]!=db.document["semantic_sha256"]: raise ManufacturerValidationError("MANUFACTURER_SIDECAR_INVALID","sidecar dataset differs")
            record_count=side["record_count"]; matched_count=side["matched_count"]; status=statdoc["status"]
        envelope={"schema_version":"1.0","result":"PASS","target":target,"status":status,"record_count":record_count,"matched_count":matched_count,"privacy_safe":True,"error":None}; print(json.dumps(envelope,separators=(",", ":")) if json_mode else f"manufacturer validation passed | target={target}"); return 0
    except ManufacturerError as exc:
        envelope={"schema_version":"1.0","result":"FAIL","target":target,"status":None,"record_count":None,"matched_count":None,"privacy_safe":True,"error":{"code":exc.code,"message":exc.safe_message}}; print(json.dumps(envelope,separators=(",", ":")) if json_mode else f"manufacturer validation failed | target={target} | error={exc.code}",file=sys.stdout if json_mode else sys.stderr); return exc.exit_code
    except Exception:
        exc=ManufacturerError("MANUFACTURER_INTERNAL_ERROR","unexpected manufacturer validation failure"); print(json.dumps({"schema_version":"1.0","result":"FAIL","target":target,"status":None,"record_count":None,"matched_count":None,"privacy_safe":True,"error":{"code":exc.code,"message":exc.safe_message}},separators=(",", ":")) if json_mode else f"manufacturer validation failed | target={target} | error={exc.code}",file=sys.stdout if json_mode else sys.stderr); return 70
if __name__=="__main__": raise SystemExit(run())
