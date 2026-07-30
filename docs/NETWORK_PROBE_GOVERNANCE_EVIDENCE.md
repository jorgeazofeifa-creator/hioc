# Evidence Report: Phase 7A Network Probe Source Governance and MQTT Health Hardening

Date: 2026-07-29

## Production trigger

PI5 changed from `192.168.100.152` to `192.168.100.251`. Runtime configuration was corrected, but the unmanaged network probe retained the old address for PI5 probing and inventory publication.

## Source intake

- Archive: `hioc-network-probe-source-intake-20260729-220644.tar.gz`
- Archive SHA-256: `74e7e251bd0848a0b87d2f314fd2d0958bd5c9730a8b6ff37fff449c1052bf6d`
- Captured script SHA-256: `edf6ad456292a0fb9441f09e7eb59fa02831cee46aa7071dcaa7b8d3eadc39a1`
- Captured host: `nutandpihole`
- Captured source: `/home/jazofv1/pi4-tools/scripts/hioc-network-probe.sh`
- Repository source: `pi4-tools/scripts/hioc-network-probe.sh`
- Production deployment path: `/home/jazofv1/pi4-tools/scripts/hioc-network-probe.sh`

The archive contained exactly the expected two regular files, had no unsafe paths or links, and was extracted outside the repository. Evidence confirmed no enclosing Git repository, the five-minute cron invocation, expected hashes, and both old hardcoded PI5 references. The captured script passed `bash -n`.

## Intended behavior and invariants

Existing probes, retained topics, counters, events, thresholds, payload schemas, names, roles, and logs are preserved. PI5 probing and inventory derive from required `HOME_ASSISTANT_IP`; neither production PI5 address is embedded in executable source; jq receives the address through `--arg`; credentials are never logged. Deployment excludes configuration, logs, and state.

Dashboard operational health uses a parseable last-success timestamp with a 12-minute threshold and two-minute future tolerance. Invalid, unavailable, unknown, empty, stale, and implausibly future timestamps are not Healthy. Historical failures remain visible evidence but do not determine current health.

## Repository validation

Status: **PASS**. Both shell sources passed Bash syntax validation. Six new focused tests passed. The full regression suite passed 197 tests with 7 environment-dependent skips. Git diff checks, endpoint/source searches, secret review, and documentation-link checks passed. Home Assistant YAML tests were included but skipped because PyYAML is unavailable in the bundled Windows runtime; operator-side Home Assistant validation remains required.

## Production validation

Status: **PENDING**. Codex did not access PI3 or PI5. Controlled deployment, hash comparison, MQTT/inventory evidence, Dashboard V2 deployment, and runtime UI validation remain operator tasks.

## Warnings

- Only `hioc-network-probe.sh` was captured. Remaining `pi4-tools` content is not governed here.
- The cumulative MQTT failure count must not be erased merely to make a dashboard green.
- Dashboard V2 deployment and runtime validation remain operator tasks.
- Repository source existence alone does not validate production.

Final repository result: **PASS**. Overall checkpoint: **OPEN, PRODUCTION PENDING**.
