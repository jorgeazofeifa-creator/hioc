#!/usr/bin/env python3
"""Read-only HIOC fresh-session continuity check."""
import sys
sys.dont_write_bytecode = True
from hioc_project_continuity import main
if __name__ == "__main__":
    raise SystemExit(main())
