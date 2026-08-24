#!/usr/bin/env python3
"""PE-4.0B.2a-F: deploy client, publish immutable environment, switch pointer."""
import argparse, os, pathlib, shutil
from hioc_pe4_runtime_common import *

def main():
    verify_pi3()
    p=argparse.ArgumentParser();p.add_argument("--construction-directory",required=True);p.add_argument("--governance-commit",required=True);a=p.parse_args()
    root=validate_construction(a.construction_directory);verify_client_source(a.governance_commit,"tools/hioc-pe4-runtime-publish.py")
    require_directory(RUNTIME_ROOT,0o750);require_owned(RUNTIME_ROOT);require_directory(ENVIRONMENT_ROOT,0o750);require_owned(ENVIRONMENT_ROOT)
    exact_distribution_set(root/"bin/python");run([str(root/"bin/python"),"-I","-c",CAPABILITY_PROBE],"CAPABILITY_VALIDATION")
    if VERSIONED_ENVIRONMENT.exists() or VERSIONED_ENVIRONMENT.is_symlink():raise Failure("VERSIONED_ENVIRONMENT_EXISTS","PUBLICATION")
    require_directory(CLIENT_TARGET.parent);require_owned(CLIENT_TARGET.parent)
    if CLIENT_TARGET.exists() or CLIENT_TARGET.is_symlink():
        require_regular(CLIENT_TARGET,0o700);require_owned(CLIENT_TARGET)
        if sha256(CLIENT_TARGET)!=CLIENT_SHA256:raise Failure("EXISTING_CLIENT_IDENTITY_MISMATCH","CLIENT_PUBLICATION")
    else:
        temp=CLIENT_TARGET.parent/("."+CLIENT_TARGET.name+".pe4.tmp")
        if temp.exists() or temp.is_symlink():raise Failure("CLIENT_TEMP_EXISTS","CLIENT_PUBLICATION")
        shutil.copyfile(CLIENT_SOURCE,temp);os.chmod(temp,0o700)
        if sha256(temp)!=CLIENT_SHA256:raise Failure("CLIENT_IDENTITY_MISMATCH","CLIENT_PUBLICATION")
        os.replace(temp,CLIENT_TARGET)
    os.replace(root,VERSIONED_ENVIRONMENT);os.chmod(VERSIONED_ENVIRONMENT,0o750)
    previous="NONE"
    if ACTIVE_POINTER.exists() or ACTIVE_POINTER.is_symlink():
        previous=validated_active_target().name
    atomic_private_text(PREVIOUS_POINTER,previous)
    link=RUNTIME_ROOT/".active.pe4.tmp"
    if link.exists() or link.is_symlink():raise Failure("ACTIVE_TEMP_EXISTS","ACTIVE_POINTER",True)
    os.symlink(str(pathlib.Path("environments")/VERSIONED_NAME),link)
    os.replace(link,ACTIVE_POINTER)
    evidence=evidence_directory("hioc-pe4-runtime-publish-")
    write_evidence(evidence,"PE-4.0B.2a-F",{"ACTION":"RUNTIME_PUBLICATION","ENVIRONMENT_IDENTITY":VERSIONED_NAME,"CLIENT_BLOB":CLIENT_BLOB,"CLIENT_SHA256":CLIENT_SHA256,"PREVIOUS_ACTIVE_TARGET":previous,"ACTIVE_TARGET":VERSIONED_NAME,"OWNER_GROUP":"jazofv1:jazofv1","MODE_VALIDATION":"PASS"},"PASS")
    terminal("PASS","NONE","COMPLETE",False,evidence)
if __name__=="__main__":
    try:main()
    except Failure as exc:terminal("FAIL",exc.code,exc.stage,exc.rollback);raise SystemExit(1)
    except Exception:terminal("FAIL","UNEXPECTED_ERROR","UNEXPECTED",False);raise SystemExit(1)
