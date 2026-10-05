#!/usr/bin/env python3
"""Governed evidence-only Action E handoff preserve; no lifecycle execution."""
# Delegated interface: --governance-commit; bounded UNEXPECTED_ERROR terminal.
import sys
from hioc_pe4_action_e_handoff import cli

if __name__ == "__main__":
    raise SystemExit(cli("preserve", sys.argv[1:]))
