#!/usr/bin/env python3
"""PE-4.0B.2a-E: validate isolation and the exact websockets behavioral API."""
import argparse
from hioc_pe4_runtime_common import *

def main():
    verify_pi3()
    p=argparse.ArgumentParser();p.add_argument("--governance-commit",required=True);p.add_argument("--construction-directory",required=True);a=p.parse_args()
    verify_repository(SOURCE,a.governance_commit,("tools/hioc-pe4-dependency-validate.py","tools/hioc_pe4_runtime_common.py"))
    root=validate_construction(a.construction_directory); python=root/"bin/python"; exact_distribution_set(python)
    run([str(python),"-I","-c",CAPABILITY_PROBE],"CAPABILITY_VALIDATION")
    evidence=evidence_directory("hioc-pe4-dependency-validate-")
    write_evidence(evidence,"PE-4.0B.2a-E",{"ACTION":"DEPENDENCY_VALIDATION","ENVIRONMENT_IDENTITY":VERSIONED_NAME,"INSTALLED_VERSION":"16.1.1","CAPABILITY_VALIDATION":"PASS"},"PASS")
    terminal("PASS","NONE","COMPLETE",False,evidence);print(f"CONSTRUCTION_DIRECTORY={root}")
if __name__ == "__main__":
    try:main()
    except Failure as exc:terminal("FAIL",exc.code,exc.stage,False);raise SystemExit(1)
    except Exception:terminal("FAIL","UNEXPECTED_ERROR","UNEXPECTED",False);raise SystemExit(1)
