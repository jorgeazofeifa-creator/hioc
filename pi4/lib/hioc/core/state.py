import json
import os
from pathlib import Path
from typing import Any, Optional

from .schemas import Schema


class StateStore:
    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def path(self, name: str) -> Path:
        return self.root / name

    def read_json(self, name: str, fallback: Any):
        path = self.path(name)
        try:
            if path.exists():
                return json.loads(path.read_text())
        except Exception:
            return fallback
        return fallback

    def read_json_strict(self, name: str):
        """Read authoritative JSON without converting corruption into empty state."""
        path = self.path(name)
        try:
            text = path.read_text()
        except FileNotFoundError as exc:
            raise StateMissingError(path) from exc
        except OSError as exc:
            raise StateIOError(path, exc) from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise StateMalformedError(path, exc) from exc

    def write_json(self, name: str, payload: Any, schema: Optional[Schema] = None) -> None:
        if schema is not None:
            schema.validate(payload)
        path = self.path(name)
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(json.dumps(payload, indent=2, sort_keys=True))
        tmp.replace(path)

    def write_json_durable(self, name: str, payload: Any, schema: Optional[Schema] = None) -> None:
        if schema is not None:
            schema.validate(payload)
        path = self.path(name)
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".tmp")
        with tmp.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
        fsync_directory(path.parent)

    def append_bounded_json_list(self, name: str, item: dict, limit: int, schema: Optional[Schema] = None) -> list:
        current = self.read_json(name, [])
        if not isinstance(current, list):
            current = []
        if schema is not None:
            schema.validate(item)
        updated = [item] + current
        bounded = updated[:limit]
        self.write_json(name, bounded)
        return bounded


class StateReadError(RuntimeError):
    def __init__(self, path: Path, category: str, detail: object = ""):
        self.path = path
        self.category = category
        super().__init__(f"{category} authoritative state: {path}{': ' + str(detail) if detail else ''}")


class StateMissingError(StateReadError):
    def __init__(self, path: Path):
        super().__init__(path, "missing")


class StateMalformedError(StateReadError):
    def __init__(self, path: Path, detail: object):
        super().__init__(path, "malformed JSON", detail)


class StateIOError(StateReadError):
    def __init__(self, path: Path, detail: object):
        super().__init__(path, "I/O failure", detail)


def fsync_directory(path: Path) -> None:
    if os.name == "nt":
        return
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
