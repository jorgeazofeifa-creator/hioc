from dataclasses import dataclass
from typing import Any


class SchemaError(ValueError):
    pass


@dataclass(frozen=True)
class Field:
    name: str
    types: tuple[type, ...]
    required: bool = True


class Schema:
    def __init__(self, name: str, fields: list[Field]):
        self.name = name
        self.fields = fields

    def validate(self, payload: dict[str, Any]) -> None:
        if not isinstance(payload, dict):
            raise SchemaError(f"{self.name} must be an object")
        for field in self.fields:
            if field.name not in payload:
                if field.required:
                    raise SchemaError(f"{self.name}.{field.name} is required")
                continue
            value = payload[field.name]
            if not isinstance(value, field.types):
                expected = ", ".join(t.__name__ for t in field.types)
                raise SchemaError(f"{self.name}.{field.name} must be {expected}")


EVENT_SCHEMA = Schema(
    "event",
    [
        Field("id", (str,)),
        Field("type", (str,)),
        Field("timestamp", (str,)),
        Field("source", (str,)),
        Field("payload", (dict,)),
    ],
)

INVENTORY_SCHEMA = Schema(
    "inventory",
    [
        Field("schema_version", (str,)),
        Field("updated", (str,)),
        Field("devices", (list,)),
        Field("services", (list,)),
        Field("topology", (dict,)),
        Field("dependencies", (dict,)),
        Field("summary", (dict,)),
    ],
)

INVENTORY_SUMMARY_SCHEMA = Schema(
    "inventory_summary",
    [
        Field("updated", (str,)),
        Field("device_count", (int,)),
        Field("healthy_count", (int,)),
        Field("watch_count", (int,)),
        Field("degraded_count", (int,)),
        Field("offline_count", (int,)),
        Field("service_count", (int,)),
        Field("topology_edges", (int,)),
        Field("dependency_edges", (int,)),
        Field("lowest_health_score", (int, float)),
    ],
)

LIFECYCLE_CATALOG_SCHEMA = Schema(
    "lifecycle_catalog",
    [
        Field("schema_version", (str,)),
        Field("migration_version", (int,)),
        Field("generation_id", (str,)),
        Field("devices", (list,)),
        Field("services", (list,)),
        Field("topology", (dict,)),
        Field("dependencies", (dict,)),
    ],
)

LIFECYCLE_REGISTRY_SCHEMA = Schema(
    "lifecycle_registry",
    [
        Field("schema_version", (str,)),
        Field("migration_version", (int,)),
        Field("generation_id", (str,)),
        Field("records", (dict,)),
    ],
)

LIFECYCLE_MANIFEST_SCHEMA = Schema(
    "lifecycle_manifest",
    [
        Field("schema_version", (str,)),
        Field("migration_version", (int,)),
        Field("generation_id", (str,)),
        Field("transaction_id", (str,)),
        Field("operation_receipt", (dict,)),
        Field("transition_receipts", (list,)),
    ],
)
