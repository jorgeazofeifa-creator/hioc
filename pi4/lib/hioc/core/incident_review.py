from __future__ import annotations

from datetime import datetime
from statistics import mean
from typing import Any


SERVICE_TERMS = (
    "dns",
    "mqtt",
    "pi-hole",
    "home assistant",
    "telemetry",
    "cloud",
    "nut",
    "ups",
    "probe",
    "dashboard",
    "automation",
)


def parse_time(value: Any) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None


def seconds_between(started: Any, resolved: Any, fallback: Any = 0) -> int:
    try:
        if fallback not in (None, "", "unknown"):
            return max(0, int(float(fallback)))
    except (TypeError, ValueError):
        pass
    start = parse_time(started)
    end = parse_time(resolved)
    if start and end:
        return max(0, int((end - start).total_seconds()))
    return 0


def human_duration(seconds: Any) -> str:
    try:
        total = max(0, int(float(seconds)))
    except (TypeError, ValueError):
        total = 0
    if total < 60:
        return f"{total} seconds"
    minutes, secs = divmod(total, 60)
    if minutes < 60:
        return f"{minutes} minutes {secs} seconds" if secs else f"{minutes} minutes"
    hours, mins = divmod(minutes, 60)
    if hours < 24:
        return f"{hours} hours {mins} minutes" if mins else f"{hours} hours"
    days, hours = divmod(hours, 24)
    return f"{days} days {hours} hours" if hours else f"{days} days"


def as_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, tuple):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [part.strip() for part in value.split(",") if part.strip()]
    return []


def affected_services(affected: list[str], signals: list[dict[str, Any]]) -> list[str]:
    services = []
    for item in affected:
        lowered = item.lower()
        if any(term in lowered for term in SERVICE_TERMS):
            services.append(item)
    for signal in signals:
        if signal.get("source") == "telemetry":
            system = str(signal.get("system", "")).strip()
            if system and any(term in system.lower() for term in SERVICE_TERMS):
                services.append(system)
    return sorted(set(services))


def recovery_type(incident: dict[str, Any]) -> str:
    existing = str(incident.get("recovery_type", "")).strip().lower()
    if existing:
        return existing
    status = str(incident.get("status", "")).lower()
    phase = str(incident.get("phase", "")).lower()
    if status == "resolved" or phase == "resolved":
        return "automatic"
    if status == "superseded":
        return "superseded"
    if status == "interrupted":
        return "interrupted"
    return "unknown"


def timeline_for_incident(incident: dict[str, Any], timeline: list[dict[str, Any]]) -> list[dict[str, str]]:
    incident_id = incident.get("id") or incident.get("incident_id")
    events = []
    for event in timeline:
        if incident_id and event.get("incident_id") not in (incident_id, "", None):
            continue
        timestamp = str(event.get("timestamp", incident.get("updated", "")))
        message = str(event.get("message") or event.get("title") or "Incident event")
        events.append({"timestamp": timestamp, "message": message})

    if not events and incident.get("started"):
        events.append({"timestamp": str(incident["started"]), "message": str(incident.get("reason") or incident.get("title", "Incident detected"))})
    for evidence in as_list(incident.get("evidence")):
        events.append({"timestamp": str(incident.get("started", "")), "message": evidence})
    has_resolution_event = any("resolved" in event.get("message", "").lower() for event in events)
    if (incident.get("resolved") or incident.get("end_time")) and not has_resolution_event:
        events.append({"timestamp": str(incident.get("resolved") or incident.get("end_time")), "message": "Incident resolved"})

    deduped = []
    seen = set()
    for event in sorted(events, key=lambda item: item.get("timestamp", "")):
        key = (event.get("timestamp", ""), event.get("message", ""))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(event)
    return deduped


def build_incident_report(incident: dict[str, Any], timeline: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    timeline = timeline or []
    resolved = incident.get("resolved") or incident.get("end_time")
    duration_seconds = seconds_between(incident.get("started"), resolved, incident.get("duration_seconds"))
    affected = as_list(incident.get("affected"))
    signals = incident.get("signals") if isinstance(incident.get("signals"), list) else []
    rec_type = recovery_type(incident)
    recommendation = str(incident.get("recommendation") or "No action required.")
    if rec_type == "automatic" and "no action" not in recommendation.lower():
        recommendation = f"No action required. {recommendation}"

    return {
        "title": incident.get("title", "Incident"),
        "severity": incident.get("severity", "info"),
        "started": incident.get("started", "unknown"),
        "resolved": resolved or "unknown",
        "duration_seconds": duration_seconds,
        "duration": human_duration(duration_seconds),
        "root_cause": incident.get("root_cause", incident.get("system", "unknown")),
        "confidence_percent": int(incident.get("confidence_percent", 0) or 0),
        "affected_systems": affected,
        "affected_services": affected_services(affected, signals),
        "impact_summary": incident.get("impact", "Impact was not recorded."),
        "evidence": as_list(incident.get("evidence")) or as_list(incident.get("reason")),
        "timeline": timeline_for_incident(incident, timeline),
        "recovery": "Recovered automatically." if rec_type == "automatic" else f"Recovery type: {rec_type}.",
        "recommended_action": recommendation,
        "incident_id": incident.get("id", incident.get("incident_id", "")),
        "recovery_type": rec_type,
    }


def enrich_history(history: list[dict[str, Any]], timeline: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    enriched = []
    for incident in history:
        if not isinstance(incident, dict):
            continue
        item = dict(incident)
        item["review"] = build_incident_report(item, timeline)
        item["recovery_type"] = item["review"]["recovery_type"]
        item["duration_seconds"] = item["review"]["duration_seconds"]
        enriched.append(item)
    return enriched


def compact_recent_incidents(history: list[dict[str, Any]], limit: int = 5) -> list[dict[str, Any]]:
    recent = []
    for incident in history[:limit]:
        review = incident.get("review") or build_incident_report(incident)
        recent.append({
            "title": review["title"],
            "status": "Resolved" if review["recovery_type"] == "automatic" else review["recovery_type"].title(),
            "severity": review["severity"],
            "started": review["started"],
            "resolved": review["resolved"],
            "duration": review["duration"],
            "root_cause": review["root_cause"],
            "incident_id": review["incident_id"],
        })
    return recent


def recent_incident_reviews(history: list[dict[str, Any]], limit: int = 5) -> list[dict[str, Any]]:
    reviews = []
    for incident in history[:limit]:
        reviews.append(incident.get("review") or build_incident_report(incident))
    return reviews


def build_history_stats(history: list[dict[str, Any]], now: datetime | None = None) -> dict[str, Any]:
    now = now or datetime.now().astimezone()
    starts = [(incident, parse_time((incident.get("review") or incident).get("started"))) for incident in history]
    starts = [(incident, started) for incident, started in starts if started]
    durations = [seconds_between(incident.get("started"), incident.get("resolved") or incident.get("end_time"), incident.get("duration_seconds")) for incident in history]
    valid_durations = [duration for duration in durations if duration > 0]
    automatic = sum(1 for incident in history if recovery_type(incident) == "automatic")
    manual = sum(1 for incident in history if recovery_type(incident) == "manual")

    def within(days: int) -> int:
        return sum(1 for _, started in starts if (now - started).total_seconds() <= days * 86400)

    today = sum(1 for _, started in starts if started.date() == now.date())
    longest = max(valid_durations) if valid_durations else 0
    average = round(mean(valid_durations)) if valid_durations else 0
    return {
        "today": today,
        "last_7_days": within(7),
        "last_30_days": within(30),
        "automatic_recoveries": automatic,
        "manual_intervention_required": manual,
        "average_duration_seconds": average,
        "average_duration": human_duration(average),
        "longest_incident_seconds": longest,
        "longest_incident": human_duration(longest),
    }
