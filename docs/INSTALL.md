# HIOC Installation

## Pi4

```bash
git clone https://github.com/jorgeazofeifa-creator/hioc.git ~/hioc
cd ~/hioc
bash pi4/install_pi4.sh
bash pi4/validate_pi4.sh
```

The installer uses the existing Pi4 toolkit configuration at:

```text
/home/jazofv1/pi4-tools/config/toolkit.conf
```

It adds a cron entry that runs the incident engine once per minute.

## Home Assistant

From the Home Assistant terminal after cloning or copying the repository:

```bash
cd /config/hioc
bash homeassistant/install_ha.sh
ha core check
ha core restart
```

Then enable notifications:

```text
input_boolean.hioc_incident_notifications
```

## Rollback

On Pi4:

```bash
bash ~/hioc/pi4/uninstall_pi4.sh
```

On Home Assistant, remove:

```text
/config/packages/hioc_incident_center.yaml
```

Then run:

```bash
ha core check
ha core restart
```
