#!/usr/bin/env python3
"""PE-4.0B.2a-F: publication-only journaled transaction.

--governance-commit binds the current F consumer; failures include UNEXPECTED_ERROR.
"""
import os, sys
# Isolated system Python excludes script directories; add this governed source only.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hioc_pe4_action_f import cli

if __name__ == "__main__":
    raise SystemExit(cli())
