import json
import logging
from pathlib import Path


class EngineLogger:
    def __init__(self, log_dir: Path, name: str, level: str = "INFO"):
        log_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper(), logging.INFO))
        if not self.logger.handlers:
            handler = logging.FileHandler(log_dir / f"{name}.log")
            handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
            self.logger.addHandler(handler)

    def info(self, message: str, **fields) -> None:
        self.logger.info(self._format(message, fields))

    def warning(self, message: str, **fields) -> None:
        self.logger.warning(self._format(message, fields))

    def error(self, message: str, **fields) -> None:
        self.logger.error(self._format(message, fields))

    def exception(self, message: str, **fields) -> None:
        self.logger.exception(self._format(message, fields))

    @staticmethod
    def _format(message: str, fields: dict) -> str:
        if not fields:
            return message
        return f"{message} {json.dumps(fields, sort_keys=True)}"

