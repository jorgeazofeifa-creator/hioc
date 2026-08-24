#!/usr/bin/env python3
"""Restore only a previously retained approved PE-4 active environment pointer."""
import argparse, os, pathlib, re
from hioc_pe4_runtime_common import *
def main():
    verify_pi3()
    p=argparse.ArgumentParser();p.add_argument("--governance-commit",required=True);a=p.parse_args()
    verify_repository(SOURCE,a.governance_commit,("tools/hioc-pe4-runtime-rollback.py","tools/hioc_pe4_runtime_common.py"))
    require_regular(PREVIOUS_POINTER,0o600);require_owned(PREVIOUS_POINTER)
    previous=PREVIOUS_POINTER.read_text(encoding="ascii").strip()
    if not re.fullmatch(r"cpython311-websockets[0-9.]+-lock-v[0-9]+",previous):raise Failure("ROLLBACK_TARGET_INVALID","ROLLBACK_ELIGIBILITY")
    target=ENVIRONMENT_ROOT/previous;require_directory(target,0o750);require_owned(target)
    require_regular(target/"bin/python");exact_distribution_set(target/"bin/python")
    run([str(target/"bin/python"),"-I","-c",CAPABILITY_PROBE],"ROLLBACK_ELIGIBILITY")
    require_regular(CLIENT_TARGET,0o700)
    if sha256(CLIENT_TARGET)!=CLIENT_SHA256:raise Failure("CLIENT_IDENTITY_MISMATCH","ROLLBACK_ELIGIBILITY")
    link=RUNTIME_ROOT/".active.pe4.rollback.tmp"
    if link.exists() or link.is_symlink():raise Failure("ROLLBACK_TEMP_EXISTS","ROLLBACK_PUBLICATION")
    current=validated_active_target().name
    os.symlink(str(pathlib.Path("environments")/target.name),link);os.replace(link,ACTIVE_POINTER)
    atomic_private_text(PREVIOUS_POINTER,current)
    evidence=evidence_directory("hioc-pe4-runtime-rollback-");write_evidence(evidence,"PE-4.0B.2a-ROLLBACK",{"ACTION":"RUNTIME_ROLLBACK","ACTIVE_TARGET":target.name},"PASS");terminal("PASS","NONE","COMPLETE",False,evidence)
if __name__=="__main__":
    try:main()
    except Failure as exc:terminal("FAIL",exc.code,exc.stage,exc.rollback);raise SystemExit(1)
    except Exception:terminal("FAIL","UNEXPECTED_ERROR","UNEXPECTED",False);raise SystemExit(1)
