# HIOC

Home Infrastructure Operations Center.

HIOC turns your Pi 4 into an infrastructure monitoring appliance and uses Home Assistant as the operator console.

## v1.0.0-core

This release adds the first real installable HIOC core:

- Pi4 incident engine
- structured incident JSON
- active and history incident stores
- MQTT retained incident state
- Home Assistant MQTT sensors
- phone notifications from one incident source of truth
- install, uninstall, validation, and rollback-friendly backups

## Architecture

```text
Pi4 probe telemetry
  -> HIOC Incident Engine
  -> local JSON store
  -> MQTT retained state
  -> Home Assistant entities
  -> Dashboard and phone notifications
```

The incident engine does not replace your existing network probe. It consumes the same MQTT and state data patterns you already built and adds a structured incident lifecycle on top.

## Quick install

On the Pi4:

```bash
git clone https://github.com/jorgeazofeifa-creator/hioc.git ~/hioc
cd ~/hioc
bash pi4/install_pi4.sh
```

On Home Assistant, copy:

```text
homeassistant/packages/hioc_incident_center.yaml
```

to:

```text
/config/packages/hioc_incident_center.yaml
```

Then run:

```bash
ha core check
ha core restart
```

## MQTT topics

Default base topic:

```text
home/infrastructure/hioc
```

Main topics:

```text
home/infrastructure/hioc/incidents/active
home/infrastructure/hioc/incidents/history
home/infrastructure/hioc/incidents/summary
home/infrastructure/hioc/timeline/latest
home/infrastructure/hioc/status
```

## Safety

The installer backs up existing files before changing cron. It does not delete or replace your existing `~/pi4-tools` scripts.
