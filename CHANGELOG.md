# HIOC Changelog

## Unreleased

- Phase 7A Collector Canonical Ownership (implementation, production validation pending): select collector IP and MAC atomically from a deterministic complete interface record with default-route preference, and preserve supported known-infrastructure metadata across observed IP or hostname changes when the normalized MAC matches exactly. Observed runtime identity remains authoritative and weaker matches with conflicting MAC evidence remain rejected. No public schema, MQTT, Home Assistant, dashboard, health, incident, or discovery-policy contract changed.
