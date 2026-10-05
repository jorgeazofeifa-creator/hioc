#!/usr/bin/env python3
"""PE-4.0B.2a-E: validate isolation and the exact websockets behavioral API."""
import argparse, pathlib
from hioc_pe4_runtime_common import *
from hioc_pe4_handoff_compatibility import (validate_commit_id,
    verify_current_consumer_source, verify_handoff_compatibility)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--governance-commit",required=True)
    p.add_argument("--action-d-governance-commit",required=True)
    p.add_argument("--construction-directory",required=True);a=p.parse_args()
    validate_commit_id(a.governance_commit,"SOURCE_IDENTITY")
    validate_commit_id(a.action_d_governance_commit,"HANDOFF_COMPATIBILITY")
    verify_pi3()
    verify_current_consumer_source(SOURCE,a.governance_commit)
    verify_handoff_compatibility(SOURCE,a.action_d_governance_commit,a.governance_commit)
    path=validate_construction(a.construction_directory)
    runtime_parent=open_trusted_owned_parent(RUNTIME_ROOT.parent,"ACTION_D_ELIGIBILITY")
    runtime_root=open_owned_directory(RUNTIME_ROOT,0o750,"ACTION_D_ELIGIBILITY",parent=runtime_parent)
    environment_root=open_owned_directory(ENVIRONMENT_ROOT,0o750,"ACTION_D_ELIGIBILITY",parent=runtime_root)
    root=open_owned_directory(path,0o750,"ACTION_D_ELIGIBILITY",parent=environment_root)
    environment=action_d_subprocess_environment();work=f"/proc/self/fd/{root.fd}"
    try:
        validate_action_d_eligibility(root,a.action_d_governance_commit)
        exact_distribution_set(pathlib.Path("./bin/python"),cwd=work,pass_fds=(root.fd,),env=environment)
        run(["./bin/python","-I","-c",CAPABILITY_PROBE],"CAPABILITY_VALIDATION",cwd=work,pass_fds=(root.fd,),env=environment)
    finally:
        root.close();environment_root.close();runtime_root.close();runtime_parent.close()
    evidence=evidence_directory("hioc-pe4-dependency-validate-")
    write_evidence(evidence,"PE-4.0B.2a-E",{"ACTION":"DEPENDENCY_VALIDATION","ENVIRONMENT_IDENTITY":VERSIONED_NAME,"INSTALLED_VERSION":"16.1.1","CAPABILITY_VALIDATION":"PASS"},"PASS")
    terminal("PASS","NONE","COMPLETE",False,evidence);print(f"CONSTRUCTION_DIRECTORY={path}")
if __name__ == "__main__":
    try:main()
    except Failure as exc:terminal("FAIL",exc.code,exc.stage,False);raise SystemExit(1)
    except Exception:terminal("FAIL","UNEXPECTED_ERROR","UNEXPECTED",False);raise SystemExit(1)
