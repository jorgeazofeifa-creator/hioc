"""Launch only with the accepted active interpreter and explicit -I -B.

PASS and governed PASS_WITH_WARNING return zero; FAIL returns nonzero.
No credential, endpoint, path, recovery or destructive options are exposed.
"""
import sys

# Isolated mode deliberately excludes the script directory and PYTHONPATH.
sys.path.insert(0, "/home/jazofv1/hioc/pi4/lib")
from hioc.home_assistant_association import main

if __name__ == "__main__":
    raise SystemExit(main())
