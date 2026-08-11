#!/usr/bin/env python3
"""Manual bounded PE-3.1 manufacturer sidecar generator."""
import argparse,json,os,pathlib,sys,tempfile
from datetime import datetime,timezone
DEFAULT_HOME=pathlib.Path(os.environ.get("HIOC_HOME","/home/jazofv1/hioc"))
sys.path.insert(0,str(DEFAULT_HOME/"pi4"/"lib")); from hioc.manufacturer import *; from hioc.manufacturer import _ManufacturerLock
class Parser(argparse.ArgumentParser):
    pass
def parser():
    p=Parser(); p.add_argument("--home"); p.add_argument("--inventory"); p.add_argument("--database"); p.add_argument("--manifest"); p.add_argument("--output-sidecar"); p.add_argument("--output-status"); p.add_argument("--json",action="store_true"); return p
def config_database(home):
    path=home/"config"/"hioc.conf"
    if not path.exists(): return ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("MANUFACTURER_DB_PATH="): return line.split("=",1)[1].strip().strip('"\'')
    return ""
def stamp(): return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
def failure_status(now,code,message,dataset=None,existing=False):
    unavailable=code in {"MANUFACTURER_NOT_CONFIGURED","MANUFACTURER_DATABASE_MISSING","MANUFACTURER_MANIFEST_MISSING","MANUFACTURER_DATABASE_UNREADABLE","MANUFACTURER_MANIFEST_UNREADABLE","MANUFACTURER_PERMISSION_ERROR"}
    return {"schema_version":"1.0","updated":now,"status":"unavailable" if unavailable else "degraded" if existing and code in {"MANUFACTURER_LOCK_TIMEOUT","MANUFACTURER_SIDECAR_WRITE_FAILED","MANUFACTURER_STATUS_WRITE_FAILED"} else "error","dataset_available":dataset is not None,"dataset_id":dataset.document["dataset_id"] if dataset else None,"dataset_version":dataset.document["dataset_version"] if dataset else None,"dataset_semantic_sha256":dataset.document["semantic_sha256"] if dataset else None,"record_count":0,"matched_count":0,"unknown_count":0,"excluded_count":0,"invalid_count":0,"conflict_count":dataset.document["conflict_count"] if dataset else 0,"generator":MANUFACTURER_GENERATOR_VERSION,"error_code":code,"error_message":message}
def run(argv=None):
    json_mode="--json" in (argv if argv is not None else sys.argv[1:]); sidecar_path=status_path=None; database=None; status_attempted=False
    try:
        args=parser().parse_args(argv); json_mode=args.json; home=pathlib.Path(args.home) if args.home else DEFAULT_HOME
        inventory=pathlib.Path(args.inventory) if args.inventory else home/"state"/"inventory"/"inventory.json"; sidecar_path=pathlib.Path(args.output_sidecar) if args.output_sidecar else home/"state"/"inventory"/"manufacturer.json"; status_path=pathlib.Path(args.output_status) if args.output_status else home/"state"/"inventory"/"manufacturer_status.json"
        db_text=args.database if args.database else config_database(home)
        db_path=pathlib.Path(db_text) if db_text else None; manifest=pathlib.Path(args.manifest) if args.manifest else db_path.parent/"manufacturer-db.manifest.json" if db_path else None
        if any(not path.is_absolute() for path in (home,inventory,sidecar_path,status_path)) or db_path is not None and not db_path.is_absolute() or manifest is not None and not manifest.is_absolute(): raise ManufacturerInputError("MANUFACTURER_DATABASE_SCHEMA_INVALID","paths must be absolute")
        lock_path=pathlib.Path("/tmp/hioc-manufacturer.lock") if os.name=="posix" else pathlib.Path(tempfile.gettempdir())/"hioc-manufacturer.lock"
        with _ManufacturerLock(lock_path):
            try:
                if not db_text: raise ManufacturerUnavailableError("MANUFACTURER_NOT_CONFIGURED","manufacturer database is not configured")
                database=load_database(db_path,manifest)
                try: inventory_doc=json.loads(inventory.read_text(encoding="utf-8"),object_pairs_hook=dict)
                except FileNotFoundError as exc: raise ManufacturerValidationError("MANUFACTURER_INVENTORY_MISSING","inventory is missing") from exc
                except (OSError,UnicodeError,json.JSONDecodeError) as exc: raise ManufacturerValidationError("MANUFACTURER_INVENTORY_INVALID","inventory is invalid") from exc
                now=stamp(); sidecar,status=build_manufacturer_sidecar(inventory_doc,database,generated_at=now)
                old=None
                if sidecar_path.exists():
                    try: old=validate_manufacturer_sidecar(json.loads(sidecar_path.read_text(encoding="utf-8"),object_pairs_hook=dict))
                    except (OSError,UnicodeError,json.JSONDecodeError,ManufacturerError) as exc: raise ManufacturerValidationError("MANUFACTURER_SIDECAR_INVALID","existing sidecar is invalid") from exc
                if old:
                    old_sem={k:v for k,v in old.items() if k!="generated_at"}; new_sem={k:v for k,v in sidecar.items() if k!="generated_at"}
                    if old_sem==new_sem: sidecar=old; status["updated"]=old["generated_at"]
                    else: write_json_atomic(sidecar_path,sidecar,mode=0o600)
                else: write_json_atomic(sidecar_path,sidecar,mode=0o600)
                try: write_json_atomic(status_path,status,mode=0o600)
                except ManufacturerWriteError as exc: raise ManufacturerWriteError("MANUFACTURER_STATUS_WRITE_FAILED",exc.safe_message) from exc
            except ManufacturerError as locked_exc:
                status_attempted=True
                try: write_json_atomic(status_path,failure_status(stamp(),locked_exc.code,locked_exc.safe_message,database,sidecar_path.exists()),mode=0o600)
                except Exception:
                    if locked_exc.code!="MANUFACTURER_STATUS_WRITE_FAILED": locked_exc=ManufacturerWriteError("MANUFACTURER_STATUS_WRITE_FAILED","manufacturer status write failed")
                raise locked_exc
        envelope={"schema_version":"1.0","result":"PASS","status":"online","record_count":sidecar["record_count"],"matched_count":sidecar["matched_count"],"unknown_count":sidecar["unknown_count"],"excluded_count":sidecar["excluded_count"],"invalid_count":sidecar["invalid_count"],"error":None}; print(json.dumps(envelope,separators=(",", ":")) if json_mode else f"manufacturer generation passed | records={sidecar['record_count']} | matched={sidecar['matched_count']}"); return 0
    except ManufacturerError as exc:
        if status_path and exc.code!="MANUFACTURER_LOCK_TIMEOUT" and not status_attempted:
            try: write_json_atomic(status_path,failure_status(stamp(),exc.code,exc.safe_message,database,sidecar_path.exists() if sidecar_path else False),mode=0o600)
            except Exception:
                if exc.code!="MANUFACTURER_STATUS_WRITE_FAILED": exc=ManufacturerWriteError("MANUFACTURER_STATUS_WRITE_FAILED","manufacturer status write failed")
        envelope={"schema_version":"1.0","result":"FAIL","status":"error","record_count":0,"matched_count":0,"unknown_count":0,"excluded_count":0,"invalid_count":0,"error":{"code":exc.code,"message":exc.safe_message}}; print(json.dumps(envelope,separators=(",", ":")) if json_mode else f"manufacturer generation failed | error={exc.code}",file=sys.stdout if json_mode else sys.stderr); return exc.exit_code
    except Exception:
        exc=ManufacturerError("MANUFACTURER_INTERNAL_ERROR","unexpected manufacturer generation failure"); print(json.dumps({"schema_version":"1.0","result":"FAIL","status":"error","record_count":0,"matched_count":0,"unknown_count":0,"excluded_count":0,"invalid_count":0,"error":{"code":exc.code,"message":exc.safe_message}},separators=(",", ":")) if json_mode else f"manufacturer generation failed | error={exc.code}",file=sys.stdout if json_mode else sys.stderr); return 70
if __name__=="__main__": raise SystemExit(run())
