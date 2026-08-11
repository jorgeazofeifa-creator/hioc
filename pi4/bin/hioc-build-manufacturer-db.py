#!/usr/bin/env python3
"""Build a deterministic manufacturer database from three local CSV files."""
import argparse, csv, hashlib, json, os, pathlib, re, shutil, sys, tempfile

HOME = pathlib.Path(os.environ.get("HIOC_HOME", "/home/jazofv1/hioc"))
sys.path.insert(0, str(HOME / "pi4" / "lib"))
from hioc.manufacturer import *
from hioc.manufacturer import _ManufacturerLock

def fsync_directory(path):
    if os.name != "posix": return
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try: os.fsync(fd)
    finally: os.close(fd)

class Parser(argparse.ArgumentParser):
    pass

def parser():
    p = Parser();
    for flag in ("ma-l", "ma-m", "ma-s", "ma-l-sha256", "ma-m-sha256", "ma-s-sha256", "dataset-id", "dataset-version", "output-directory"): p.add_argument("--" + flag, required=True)
    p.add_argument("--json", action="store_true"); return p

def source(path_text, expected, cls):
    path = pathlib.Path(path_text)
    if not path.is_absolute() or path.is_symlink() or not path.is_file(): raise ManufacturerInputError("MANUFACTURER_DATABASE_UNREADABLE", "source file is invalid")
    if not re.fullmatch(r"[0-9a-f]{64}", expected) or file_sha256(path) != expected: raise ManufacturerIntegrityError("MANUFACTURER_DATABASE_CHECKSUM_MISMATCH", "source checksum mismatch")
    if path.stat().st_size > 64 * 1024 * 1024: raise ManufacturerInputError("MANUFACTURER_DATABASE_SCHEMA_INVALID", "source file exceeds limit")
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle: rows = list(csv.reader(handle))
    except (OSError, UnicodeError, csv.Error) as exc: raise ManufacturerInputError("MANUFACTURER_DATABASE_SCHEMA_INVALID", "source CSV is invalid") from exc
    while rows and not rows[0]: rows.pop(0)
    if not rows: raise ManufacturerInputError("MANUFACTURER_DATABASE_SCHEMA_INVALID", "source CSV is empty")
    header = rows.pop(0); required = ("Registry", "Assignment", "Organization Name")
    if any(header.count(name) != 1 for name in required): raise ManufacturerInputError("MANUFACTURER_DATABASE_SCHEMA_INVALID", "source headers are invalid")
    index = {name: header.index(name) for name in required}; output = []
    for row in rows:
        if not row or all(not cell for cell in row): continue
        if len(output) >= 500000 or len(row) < len(header): raise ManufacturerInputError("MANUFACTURER_DATABASE_SCHEMA_INVALID", "source row is invalid")
        if row[index["Registry"]] != cls: raise ManufacturerInputError("MANUFACTURER_DATABASE_SCHEMA_INVALID", "source class is invalid")
        assignment = row[index["Assignment"]]
        width = {"MA-L": 6, "MA-M": 7, "MA-S": 9}[cls]
        if not re.fullmatch(rf"[0-9A-Fa-f]{{{width}}}", assignment): raise ManufacturerInputError("MANUFACTURER_DATABASE_SCHEMA_INVALID", "source assignment is invalid")
        output.append((cls, assignment.upper(), normalize_organization(row[index["Organization Name"]])))
    return output, path

def construct(groups, dataset_id, dataset_version):
    grouped, duplicates = {}, 0
    for cls, prefix, organization in sum((group[0] for group in groups), []):
        bits = {"MA-L": 24, "MA-M": 28, "MA-S": 36}[cls]; key = f"{bits}:{prefix}"
        if key not in grouped: grouped[key] = {"prefix": prefix, "prefix_length": bits, "assignment_class": cls, "organizations": set()}
        group = grouped[key]
        if group["prefix"] != prefix or group["prefix_length"] != bits or group["assignment_class"] != cls: raise ManufacturerIntegrityError("MANUFACTURER_DATASET_CONFLICT", "irreconcilable assignment conflict")
        if organization in group["organizations"]: duplicates += 1
        else: group["organizations"].add(organization)
    records, conflicts = {}, {}
    for key in sorted(grouped):
        group = grouped[key]
        if len(group["organizations"]) == 1:
            records[key] = {"prefix": group["prefix"], "prefix_length": group["prefix_length"], "assignment_class": group["assignment_class"], "organization": next(iter(group["organizations"]))}
        elif len(group["organizations"]) >= 2:
            conflicts[key] = {"prefix": group["prefix"], "prefix_length": group["prefix_length"], "assignment_class": group["assignment_class"], "variant_count": len(group["organizations"])}
        else: raise ManufacturerIntegrityError("MANUFACTURER_DATASET_CONFLICT", "empty assignment conflict group")
    counts = {cls: sum(x["assignment_class"] == cls for x in records.values()) for cls in ("MA-L", "MA-M", "MA-S")}
    db = {"schema_version": MANUFACTURER_DB_SCHEMA_VERSION, "dataset_id": dataset_id, "dataset_version": dataset_version, "parser_version": MANUFACTURER_GENERATOR_VERSION, "semantic_sha256": "", "record_count": len(records), "ma_l_count": counts["MA-L"], "ma_m_count": counts["MA-M"], "ma_s_count": counts["MA-S"], "conflict_count": len(conflicts), "records": records, "conflicts": conflicts}
    payload = {key: value for key, value in db.items() if key != "semantic_sha256"}; db["semantic_sha256"] = semantic_sha256(payload); validate_database(db); return db, duplicates

def run(argv=None):
    json_mode = "--json" in (argv if argv is not None else sys.argv[1:]); result = None
    try:
        args = parser().parse_args(argv); json_mode = args.json; out = pathlib.Path(args.output_directory)
        if not out.is_absolute() or out.exists() or not out.parent.is_dir() or out.parent.is_symlink(): raise ManufacturerInputError("MANUFACTURER_DATABASE_SCHEMA_INVALID", "output directory is invalid")
        specs = ((args.ma_l, args.ma_l_sha256, "MA-L"), (args.ma_m, args.ma_m_sha256, "MA-M"), (args.ma_s, args.ma_s_sha256, "MA-S"))
        groups = [source(*spec) for spec in specs]
        if any(out in path.parents or path == out for _, path in groups): raise ManufacturerInputError("MANUFACTURER_DATABASE_SCHEMA_INVALID", "source and output relationship is invalid")
        lock_path = pathlib.Path("/tmp/hioc-manufacturer-build.lock") if os.name == "posix" else pathlib.Path(tempfile.gettempdir()) / "hioc-manufacturer-build.lock"
        with _ManufacturerLock(lock_path):
            db1, duplicates1 = construct(groups, args.dataset_id, args.dataset_version); db2, duplicates2 = construct(groups, args.dataset_id, args.dataset_version)
            if canonical_json_bytes(db1) != canonical_json_bytes(db2) or duplicates1 != duplicates2: raise ManufacturerIntegrityError("MANUFACTURER_DETERMINISM_FAILED", "deterministic build failed")
            db_bytes = canonical_json_bytes(db1)
            sources = [{"source_class": cls, "source_filename": path.name, "source_sha256": expected, "source_size_bytes": path.stat().st_size} for (_, expected, cls), (_, path) in zip(specs, groups)]
            manifest = {"schema_version": MANUFACTURER_MANIFEST_SCHEMA_VERSION, "database_filename": "manufacturer-db.json", "database_sha256": hashlib.sha256(db_bytes).hexdigest(), "database_size_bytes": len(db_bytes), "database_semantic_sha256": db1["semantic_sha256"], "database_schema_version": MANUFACTURER_DB_SCHEMA_VERSION, "dataset_id": args.dataset_id, "dataset_version": args.dataset_version, "parser_version": MANUFACTURER_GENERATOR_VERSION, "record_count": db1["record_count"], "ma_l_count": db1["ma_l_count"], "ma_m_count": db1["ma_m_count"], "ma_s_count": db1["ma_s_count"], "duplicate_count": duplicates1, "conflict_count": db1["conflict_count"], "source_files": sources, "build": {"canonicalization_version": "1", "deterministic_build_verified": True}}
            validate_manifest(manifest); stage = pathlib.Path(tempfile.mkdtemp(prefix=f".{out.name}.manufacturer.", dir=out.parent)); os.chmod(stage, 0o700)
            try:
                for name, data in (("manufacturer-db.json", db_bytes), ("manufacturer-db.manifest.json", canonical_json_bytes(manifest))):
                    path = stage / name
                    with path.open("wb") as handle: handle.write(data); handle.flush(); os.fsync(handle.fileno())
                    os.chmod(path, 0o600)
                load_database(stage / "manufacturer-db.json", stage / "manufacturer-db.manifest.json"); fsync_directory(stage); os.replace(stage, out); fsync_directory(out.parent); stage = None
            finally:
                if stage is not None: shutil.rmtree(stage, ignore_errors=True)
        result = {"schema_version": "1.0", "result": "PASS", "record_count": db1["record_count"], "ma_l_count": db1["ma_l_count"], "ma_m_count": db1["ma_m_count"], "ma_s_count": db1["ma_s_count"], "duplicate_count": duplicates1, "conflict_count": db1["conflict_count"], "database_sha256": manifest["database_sha256"], "database_semantic_sha256": db1["semantic_sha256"], "error": None}
        print(json.dumps(result, separators=(",", ":")) if json_mode else f"manufacturer database build passed | records={db1['record_count']} | duplicate_count={duplicates1}"); return 0
    except ManufacturerError as exc:
        result = {"schema_version": "1.0", "result": "FAIL", "record_count": 0, "ma_l_count": 0, "ma_m_count": 0, "ma_s_count": 0, "duplicate_count": 0, "conflict_count": 0, "database_sha256": None, "database_semantic_sha256": None, "error": {"code": exc.code, "message": exc.safe_message}}
        print(json.dumps(result, separators=(",", ":")) if json_mode else f"manufacturer database build failed | error={exc.code}", file=sys.stdout if json_mode else sys.stderr); return exc.exit_code
    except Exception:
        exc = ManufacturerError("MANUFACTURER_INTERNAL_ERROR", "unexpected manufacturer build failure"); print(json.dumps({"schema_version":"1.0","result":"FAIL","record_count":0,"ma_l_count":0,"ma_m_count":0,"ma_s_count":0,"duplicate_count":0,"conflict_count":0,"database_sha256":None,"database_semantic_sha256":None,"error":{"code":exc.code,"message":exc.safe_message}}, separators=(",", ":")) if json_mode else f"manufacturer database build failed | error={exc.code}", file=sys.stdout if json_mode else sys.stderr); return 70
if __name__ == "__main__": raise SystemExit(run())
