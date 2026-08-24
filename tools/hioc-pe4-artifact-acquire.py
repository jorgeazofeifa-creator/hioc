#!/usr/bin/env python3
"""PE-4.0B.2a-A: exact official wheel acquisition and durable cache publication."""
import argparse, os, pathlib, shutil, tempfile, urllib.request
from hioc_pe4_runtime_common import *

def main():
    parser=argparse.ArgumentParser();parser.add_argument("--governance-commit",required=True);args=parser.parse_args()
    verify_repository(REPOSITORY_ROOT,args.governance_commit,("tools/hioc-pe4-artifact-acquire.py","tools/hioc_pe4_runtime_common.py","requirements-pe4.lock"))
    base = workstation_cache_root(); base.mkdir(parents=True, exist_ok=True); secure_workstation_directory(base)
    stage = pathlib.Path(tempfile.mkdtemp(prefix="acquire-", dir=base)); secure_workstation_directory(stage)
    target = stage / WHEEL_NAME
    try:
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, req, fp, code, msg, headers, newurl):
                raise Failure("ARTIFACT_REDIRECT_REFUSED", "ACQUISITION")
        request = urllib.request.Request(WHEEL_URL, headers={"User-Agent": "HIOC-PE4-artifact/1"})
        with urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect).open(request, timeout=20) as response:
            if response.geturl() != WHEEL_URL or response.headers.get("Content-Length") != str(WHEEL_SIZE):
                raise Failure("ARTIFACT_RESPONSE_INVALID", "ACQUISITION")
            data = response.read(WHEEL_SIZE + 1)
        if len(data) != WHEEL_SIZE: raise Failure("ARTIFACT_SIZE_MISMATCH", "ACQUISITION")
        fd=os.open(target,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        with os.fdopen(fd,"wb") as handle: handle.write(data); handle.flush(); os.fsync(handle.fileno())
        if target.name != WHEEL_NAME or target.stat().st_size != WHEEL_SIZE or sha256(target) != WHEEL_SHA256:
            raise Failure("ARTIFACT_IDENTITY_MISMATCH", "ARTIFACT_IDENTITY")
        durable = base / WHEEL_NAME
        if durable.exists():
            if durable.stat().st_size != WHEEL_SIZE or sha256(durable) != WHEEL_SHA256:
                raise Failure("DURABLE_CACHE_CONFLICT", "CACHE_PUBLICATION")
            target.unlink()
        else: os.replace(target,durable)
    except Exception:
        if stage.parent == base and stage.is_dir() and not stage.is_symlink(): shutil.rmtree(stage)
        raise
    stage.rmdir()
    evidence=evidence_directory("hioc-pe4-artifact-acquire-")
    write_evidence(evidence,"PE-4.0B.2a-A",{"ACTION":"ARTIFACT_ACQUISITION","ARTIFACT_FILENAME":WHEEL_NAME,"ARTIFACT_SIZE":WHEEL_SIZE,"APPROVED_SHA256":WHEEL_SHA256,"ACTUAL_SHA256":sha256(durable)},"PASS")
    terminal("PASS","NONE","COMPLETE",False,evidence)

if __name__ == "__main__":
    try: main()
    except Failure as exc: terminal("FAIL",exc.code,exc.stage,exc.rollback); raise SystemExit(1)
    except Exception: terminal("FAIL","UNEXPECTED_ERROR","UNEXPECTED",False); raise SystemExit(1)
