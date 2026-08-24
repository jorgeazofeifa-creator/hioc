#!/usr/bin/env python3
"""PE-4.0B.2a-C: one credential-free TCP route proof to the frozen HA endpoint."""
import argparse, socket
from hioc_pe4_runtime_common import *

def main():
    verify_pi3()
    parser=argparse.ArgumentParser();parser.add_argument("--governance-commit",required=True);args=parser.parse_args()
    verify_repository(SOURCE,args.governance_commit,("tools/hioc-pe4-route-proof.py","tools/hioc_pe4_runtime_common.py"))
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM); sock.settimeout(5)
    try: sock.connect((HA_IPV4,HA_PORT))
    except OSError: raise Failure("ROUTE_UNAVAILABLE","ROUTE_PROOF")
    finally: sock.close()
    terminal("PASS","NONE","COMPLETE",False)

if __name__ == "__main__":
    try: main()
    except Failure as exc: terminal("FAIL",exc.code,exc.stage,False); raise SystemExit(1)
    except Exception: terminal("FAIL","UNEXPECTED_ERROR","UNEXPECTED",False); raise SystemExit(1)
