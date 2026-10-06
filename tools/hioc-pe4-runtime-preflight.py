#!/usr/bin/env python3
"""PE-4.0B.2a-G controlled credential-free preflight; --governance-commit required.
Finite UNEXPECTED_ERROR handling belongs to the dedicated Action G helper.
"""
import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from hioc_pe4_action_g import cli
if __name__=="__main__":
    raise SystemExit(cli())
