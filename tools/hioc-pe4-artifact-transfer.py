#!/usr/bin/env python3
"""PE-4.0B.2a-B: transfer one cached wheel and lock to PI3, verify, then STOP."""
import argparse, pathlib, re
from hioc_pe4_runtime_common import *

def main():
    parser=argparse.ArgumentParser();parser.add_argument("--governance-commit",required=True);args=parser.parse_args()
    verify_repository(REPOSITORY_ROOT,args.governance_commit,("tools/hioc-pe4-artifact-transfer.py","tools/hioc_pe4_runtime_common.py","requirements-pe4.lock"))
    cache=workstation_cache_root(); wheel=cache/WHEEL_NAME
    if wheel.stat().st_size != WHEEL_SIZE or sha256(wheel)!=WHEEL_SHA256:raise Failure("ARTIFACT_IDENTITY_MISMATCH","ARTIFACT_IDENTITY")
    require_regular(LOCAL_LOCK)
    if sha256(LOCAL_LOCK)!=LOCK_SHA256:raise Failure("LOCK_IDENTITY_MISMATCH","ARTIFACT_IDENTITY")
    ssh=["ssh","-oBatchMode=yes","-oStrictHostKeyChecking=yes","-oConnectTimeout=5",f"{OWNER}@{PI3_IPV4}"]
    remote=run(ssh+["umask 077; mktemp -d /tmp/hioc-pe4-artifact-transfer-XXXXXXXX"],"REMOTE_STAGING",timeout=15).stdout.strip()
    if not TRANSFER_RE.fullmatch(remote): raise Failure("REMOTE_STAGING_INVALID","REMOTE_STAGING")
    opts=["-oBatchMode=yes","-oStrictHostKeyChecking=yes","-oConnectTimeout=5"]
    run(["scp",*opts,str(wheel),str(LOCAL_LOCK),f"{OWNER}@{PI3_IPV4}:{remote}/"],"TRANSFER",timeout=60)
    verify=f"chmod 600 {remote}/{WHEEL_NAME} {remote}/requirements-pe4.lock && test $(stat -c %s {remote}/{WHEEL_NAME}) -eq {WHEEL_SIZE} && test $(sha256sum {remote}/{WHEEL_NAME} | cut -d' ' -f1) = {WHEEL_SHA256} && test $(sha256sum {remote}/requirements-pe4.lock | cut -d' ' -f1) = {LOCK_SHA256} && printf '%s\\n' '{{\"action\":\"PE-4.0B.2a-B\",\"result\":\"PASS\",\"error_code\":\"NONE\",\"failure_stage\":\"COMPLETE\",\"rollback_recommended\":false}}' > {remote}/.result.tmp && chmod 600 {remote}/.result.tmp && sync -f {remote}/.result.tmp && mv {remote}/.result.tmp {remote}/result.json && sync -f {remote}/result.json && sync -f {remote}"
    run(ssh+[verify],"REMOTE_IDENTITY",timeout=20)
    terminal("PASS","NONE","COMPLETE",False); print(f"TRANSFER_DIRECTORY={remote}")

if __name__ == "__main__":
    try: main()
    except Failure as exc: terminal("FAIL",exc.code,exc.stage,exc.rollback); raise SystemExit(1)
    except Exception: terminal("FAIL","UNEXPECTED_ERROR","UNEXPECTED",False); raise SystemExit(1)
