#!/usr/bin/env python3
"""PE-4.0B.2a-G: complete credential-free isolated-runtime preflight."""
from hioc_pe4_runtime_common import *
def main():
    verify_pi3()
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument("--governance-commit",required=True);args=parser.parse_args()
    verify_repository(SOURCE,args.governance_commit,("tools/hioc-pe4-runtime-preflight.py","tools/hioc_pe4_runtime_common.py","tools/hioc-pe4-ha-auth-capability.py"))
    if validated_active_target()!=VERSIONED_ENVIRONMENT:raise Failure("ACTIVE_POINTER_INVALID","ACTIVE_POINTER")
    require_directory(VERSIONED_ENVIRONMENT,0o750);require_regular(CLIENT_TARGET,0o700)
    if sha256(CLIENT_TARGET)!=CLIENT_SHA256:raise Failure("CLIENT_IDENTITY_MISMATCH","CLIENT_IDENTITY")
    exact_distribution_set(ACTIVE_INTERPRETER);run([str(ACTIVE_INTERPRETER),"-I","-c",CAPABILITY_PROBE],"CAPABILITY_VALIDATION")
    probe="import importlib.util,sys;p=sys.argv[1];s=importlib.util.spec_from_file_location('client',p);m=importlib.util.module_from_spec(s);sys.modules['client']=m;s.loader.exec_module(m);assert m.detect_websocket_client()=='PYTHON_WEBSOCKETS';assert m.proxy_influence_present(dict()) is False"
    run([str(ACTIVE_INTERPRETER),"-I","-c",probe,str(CLIENT_TARGET)],"RUNTIME_PREFLIGHT")
    evidence=evidence_directory("hioc-pe4-runtime-preflight-");write_evidence(evidence,"PE-4.0B.2a-G",{"ACTION":"RUNTIME_PREFLIGHT","ENVIRONMENT_IDENTITY":VERSIONED_NAME,"CLIENT_SHA256":CLIENT_SHA256,"PREFLIGHT":"PASS"},"PASS");terminal("PASS","NONE","COMPLETE",False,evidence)
if __name__=="__main__":
    try:main()
    except Failure as exc:terminal("FAIL",exc.code,exc.stage,False);raise SystemExit(1)
    except Exception:terminal("FAIL","UNEXPECTED_ERROR","UNEXPECTED",False);raise SystemExit(1)
