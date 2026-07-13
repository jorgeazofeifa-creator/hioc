PASSIVE_CLIENT_SOURCES = {"arp_table", "dhcp_leases"}
AUTHORITATIVE_SOURCES = {"known_infrastructure", "gateway", "local_host"}


def record_sources(record: dict) -> set[str]:
    sources = {str(item).strip() for item in record.get("sources", []) if str(item).strip()}
    sources.update(item.strip() for item in str(record.get("source", "")).split(",") if item.strip())
    return sources


def is_dhcp_assignment_only(record: dict) -> bool:
    return record_sources(record) == {"dhcp_leases"}


def is_operationally_monitored(record: dict) -> bool:
    """Return the authoritative availability-monitoring policy for a device."""
    explicit = record.get("operationally_monitored")
    if explicit is True or str(explicit).strip().lower() in ("1", "true", "yes", "on", "enabled"):
        return True

    roles = {str(role).strip().lower() for role in record.get("roles", []) if str(role).strip()}
    device_type = str(record.get("type", "")).strip().lower()
    if record.get("inventory_class") == "infrastructure":
        return True
    if roles & {"collector", "gateway"} or device_type in {"collector", "gateway", "local_host"}:
        return True

    sources = record_sources(record)
    if sources & AUTHORITATIVE_SOURCES:
        return True
    if any(source.startswith("integration:") for source in sources):
        return True

    # Unknown and future sources remain monitored until their semantics are
    # deliberately added to this policy boundary. Only ordinary passive
    # client evidence is excluded from availability monitoring.
    return not (
        record.get("inventory_class") == "client"
        and bool(sources)
        and sources <= PASSIVE_CLIENT_SOURCES
    )
