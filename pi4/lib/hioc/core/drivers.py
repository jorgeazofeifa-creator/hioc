from dataclasses import dataclass, field


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
            try:
                results.append(driver.discover(config))
            except Exception as exc:
                results.append(DriverResult(name=getattr(driver, "name", driver.__class__.__name__), errors=[str(exc)]))
        return results

