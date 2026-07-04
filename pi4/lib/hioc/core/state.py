import json
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

    def write_json(self, name: str, payload: Any, schema: Optional[Schema] = None) -> None:
        if schema is not None:
            schema.validate(payload)
        path = self.path(name)
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(json.dumps(payload, indent=2, sort_keys=True))
        tmp.replace(path)

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
