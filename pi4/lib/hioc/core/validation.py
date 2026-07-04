from dataclasses import dataclass


@dataclass
class ValidationResult:
    name: str
    ok: bool
    message: str = ""


class Validator:
    def __init__(self):
        self.results: list[ValidationResult] = []

    def check(self, name: str, condition: bool, message: str = "") -> None:
        self.results.append(ValidationResult(name, condition, message))

    def extend(self, results: list[ValidationResult]) -> None:
        self.results.extend(results)

    def ok(self) -> bool:
        return all(result.ok for result in self.results)

    def as_dict(self) -> dict:
        return {
            "ok": self.ok(),
            "results": [result.__dict__ for result in self.results],
        }

