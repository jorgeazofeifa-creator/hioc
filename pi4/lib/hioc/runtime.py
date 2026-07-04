import logging
import subprocess
from datetime import datetime
from pathlib import Path

from .core.logging import EngineLogger
from .core.state import StateStore


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def setup_logger(log_dir: Path, name: str) -> logging.Logger:
    return EngineLogger(log_dir, name).logger


def run_command(cmd: list[str], timeout: int = 5) -> tuple[int, str, str]:
    try:
        proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout, check=False)
        return proc.returncode, proc.stdout.strip(), proc.stderr.strip()
    except FileNotFoundError as exc:
        return 127, "", str(exc)
    except subprocess.TimeoutExpired:
        return 124, "", "command timed out"
    except Exception as exc:
        return 1, "", str(exc)


def load_json(path: Path, fallback):
    return StateStore(path.parent).read_json(path.name, fallback)


def save_json(path: Path, data) -> None:
    StateStore(path.parent).write_json(path.name, data)
