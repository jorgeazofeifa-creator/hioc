from dataclasses import dataclass, field
from collections.abc import Mapping


@dataclass
class DriverResult:
    name: str
    devices: list[dict] = field(default_factory=list)
    services: list[dict] = field(default_factory=list)
    capabilities: list[dict] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


class DriverRegistry:
    def __init__(self):
        self._drivers = []

    def register(self, driver) -> None:
        self._drivers.append(driver)

    def run(self, config: dict) -> list[DriverResult]:
        results = []
        for driver in self._drivers:
            name = getattr(driver, "name", driver.__class__.__name__)
            try:
                result = driver.discover(config)
                results.append(self._validate_result(name, result))
            except Exception as exc:
                results.append(DriverResult(name=name, errors=[str(exc)]))
        return results

    @staticmethod
    def _validate_result(name: str, result) -> DriverResult:
        if not isinstance(result, DriverResult):
            return DriverResult(name=name, errors=["driver returned invalid result"])

        errors = list(result.errors)

        def normalized_records(records, kind: str) -> list[dict]:
            if not isinstance(records, (list, tuple)):
                errors.append(f"driver {kind} must be a list or tuple")
                return []
            normalized = []
            for index, record in enumerate(records):
                if not isinstance(record, Mapping):
                    errors.append(f"driver {kind} record {index} is not a mapping")
                    continue
                item = dict(record)
                if kind == "device" and not str(item.get("source", "")).strip() and not item.get("sources"):
                    item["source"] = f"driver:{name}"
                normalized.append(item)
            return normalized

        return DriverResult(
            name=str(result.name or name),
            devices=normalized_records(result.devices, "device"),
            services=normalized_records(result.services, "service"),
            capabilities=normalized_records(result.capabilities, "capability"),
            errors=errors,
        )
