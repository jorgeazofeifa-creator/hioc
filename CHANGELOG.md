# Changelog

## v1.0.0-core

Initial real HIOC core foundation.

### Added

- Pi4 installer and uninstaller.
- Incident engine that reads existing Pi4 probe state and publishes structured MQTT JSON.
- Persistent active incident, incident history, summary, and timeline JSON files.
- Duplicate suppression through stable incident keys.
- Recovery detection and duration calculation.
- Home Assistant MQTT sensors for active incident, severity, status, system, summary, history count, and latest timeline event.
- Home Assistant notification automation driven from structured incidents.
- Documentation for architecture, incident model, MQTT topics, and installation.

### Notes

- This release is intentionally compatible with the existing `~/pi4-tools` installation.
- It does not replace the existing `hioc-network-probe.sh`.
