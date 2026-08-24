#!/usr/bin/env python3
"""PE-4.0B.2a-D: private venv construction and exact offline installation."""
import argparse, os, pathlib, tempfile
from hioc_pe4_runtime_common import *

def main():
    verify_pi3()
    p=argparse.ArgumentParser(); p.add_argument("--governance-commit",required=True);p.add_argument("--transfer-directory",required=True); a=p.parse_args()
    verify_repository(SOURCE,a.governance_commit,("tools/hioc-pe4-runtime-construct.py","tools/hioc_pe4_runtime_common.py","requirements-pe4.lock"))
    transfer=validate_transfer_directory(a.transfer_directory); require_directory(ENVIRONMENT_ROOT,0o750)
    construction=pathlib.Path(tempfile.mkdtemp(prefix=f".construct-{VERSIONED_NAME}-",dir=ENVIRONMENT_ROOT)); os.chmod(construction,0o750)
    construction.rmdir()
    try:
        run(["/usr/bin/python3","-m","venv","--copies",str(construction)],"VENV_CREATION",timeout=120)
        python=construction/"bin/python"
        probe="import platform,sys,sysconfig;assert platform.python_implementation()=='CPython';assert platform.python_version()=='3.11.2';assert sys.prefix!=sys.base_prefix;assert sysconfig.get_config_var('SOABI')=='cpython-311-aarch64-linux-gnu'"
        run([str(python),"-I","-c",probe],"RUNTIME_IDENTITY")
        run([str(python),"-m","pip","install","--no-index","--no-deps","--require-hashes","--only-binary=:all:","--no-cache-dir","--find-links",str(transfer),"-r",str(transfer/"requirements-pe4.lock")],"OFFLINE_INSTALL",timeout=120)
        exact_distribution_set(python)
    except Failure:
        safe_cleanup_construction(construction); raise
    evidence=evidence_directory("hioc-pe4-runtime-construct-")
    write_evidence(evidence,"PE-4.0B.2a-D",{"ACTION":"RUNTIME_CONSTRUCTION","CONSTRUCTION_DIRECTORY":str(construction),"ARTIFACT_FILENAME":WHEEL_NAME,"ACTUAL_SHA256":WHEEL_SHA256,"ENVIRONMENT_IDENTITY":VERSIONED_NAME},"PASS")
    terminal("PASS","NONE","COMPLETE",False,evidence); print(f"CONSTRUCTION_DIRECTORY={construction}")

if __name__ == "__main__":
    try: main()
    except Failure as exc: terminal("FAIL",exc.code,exc.stage,exc.rollback); raise SystemExit(1)
    except Exception: terminal("FAIL","UNEXPECTED_ERROR","UNEXPECTED",False); raise SystemExit(1)
