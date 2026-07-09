# HIOC Dashboard v2 Plan

Dashboard v2 is a full information architecture redesign. It preserves existing capabilities, avoids adding new features, and reorganizes the interface into an operations platform.

No existing functionality should be removed. Detailed information should move to the correct page, popup, or drill-down.

Implemented dashboard file:

```text
homeassistant/dashboards/hioc_dashboard_v2.yaml
```

## Goals

- Reduce Executive to a true command page.
- Add Operations as the wallboard/live-state page.
- Turn Diagnostics into Mission Control for active troubleshooting.
- Restore the darker HIOC/NOC visual language while preserving the v2 information architecture.
- Make the dashboard guide operators with meaning, risk, recommended action, and investigation paths.
- Preserve all current dashboard capabilities.
- Eliminate duplicate information.
- Standardize terminology and visual hierarchy.
- Use the HIOC Design System card archetypes.
- Keep repo-owned dashboards portable and separate from local environment-specific views.

## Proposed Navigation

1. Executive
2. Operations
3. Diagnostics
4. Inventory
5. Network
6. Servers

Optional future pages:

- Services
- Power
- Cameras
- Reports
- Topology

## Executive Page

Purpose: Do I need to get out of my chair?

Executive has exactly seven visual elements:

1. Mission Status
2. Current Incident
3. Affected Systems
4. Domain Health
5. Top Risks
6. Latest Events
7. Data Freshness

Rules:

- no graphs
- no entity tables
- no diagnostics
- no inventory lists
- no raw telemetry
- no spacer cards
- every warning explains meaning and next step
- every domain item has a click path

Recommended layout:

- Status Banner across top.
- Incident Card and Action Card as primary left/center content.
- Affected Systems below incident.
- Domain Health as a compact vertical drill-down list.
- Top Risks, Latest Events, and Data Freshness in right column on desktop.

## Operations Page

Purpose: What is happening right now?

Operations is the wall monitor page. It shows live state only.

Domains:

- Internet
- DNS
- MQTT
- Power
- Pi4
- Pi5
- Inventory
- Forecasts
- Backups
- Automations

Rules:

- no graphs
- no raw entity tables
- no long text
- each domain gets one Health Card
- all cards use identical structure
- domain cards link to drill-down page or popup
- status colors must be visible at a glance

Recommended layout:

- Status Banner.
- 2x5 or 3x4 domain health grid depending on viewport.
- Latest event strip.
- Data freshness footer.

## Diagnostics / Mission Control

Purpose: What exactly is happening, why, and what evidence proves it?

Diagnostics should be incident-first.

Top structure when an incident is active:

1. Incident summary
2. Root cause and confidence
3. Evidence
4. Affected dependency path
5. Incident timeline
6. Live telemetry
7. Domain-specific drill-downs

Example content order:

```text
Incident: Internet degradation
Confidence: 96%
Root Cause: ISP
Started: 11:42
Duration: 4m 17s

Evidence:
- Gateway normal
- Pi-hole normal
- Packet loss 7%
- Cloudflare latency 321ms
- Google latency 340ms

Dependency Path:
Internet -> Gateway -> Pi-hole -> MQTT -> Home Assistant -> Automations

Timeline:
11:42 Packet loss increased
11:43 Latency exceeded threshold
11:44 Incident declared
11:45 Recovery detected

Live Telemetry:
graphs and raw values
```

When no incident is active, Diagnostics should show readiness and telemetry health, not a wall of raw data.

Diagnostics v2 must include a Recommended Action card. When no incident is active, it should still explain current watch items such as DNS trend rising or Pi4 memory rising using existing HIOC forecast entities.

## Inventory Page

Purpose: What exists, what changed, what is unhealthy, and what depends on it?

Keep:

- inventory status
- counts
- new/offline/stale devices
- infrastructure devices
- device health
- services
- capabilities
- topology/dependency entry point

Change:

- replace long markdown loops with table/card rows
- group by state first, device type second
- move raw firmware/MAC/IP blobs to popups
- do not use markdown pipe tables because Home Assistant may render them as raw text

## Network Page

Purpose: Is the network path healthy, and where is degradation located?

Keep:

- Internet
- WAN/gateway
- DNS/Pi-hole
- MQTT path
- probe freshness
- key trends

Change:

- merge Internet Score, Internet Health, Internet Intelligence, and Internet Quality into one term: Network Health or Domain Health.
- move raw Huawei details to popup/drill-down.
- show only the most important four trend cards by default.

## Servers Page

Purpose: Are infrastructure hosts healthy?

Keep:

- Pi4
- Pi5
- Home Assistant core/supervisor
- host resources
- storage/recorder when available

Change:

- merge Pi4 health and probe freshness.
- merge Pi5 system monitor and HA core/supervisor resources.
- move raw entities to popups.

## Card Moves

Move from Executive to Operations:

- domain status cards
- high-level service status
- live operational tiles

Move from Executive to Diagnostics:

- Live Trend Strip
- raw metric graphs
- telemetry gap cards
- service add-on detail
- MQTT detail
- UPS detail
- camera detail

Move from Executive to Network:

- Internet latency
- packet loss
- DNS latency
- gateway latency
- WAN download/upload

Move from Executive to Servers:

- Pi4 graphs
- Pi5 graphs
- host resource detail

Move from Executive to Inventory:

- protected device counts
- inventory/device health detail
- topology/dependency detail

## Cards To Remove

Remove as standalone cards:

- spacer markdown cards
- duplicate score breakdown cards
- duplicate WAN IP cards
- duplicate MQTT latency cards
- duplicate health cards that repeat another domain summary

Removing means deleting the duplicate presentation, not losing the underlying information.

## Cards To Merge

- Mission Status + Infrastructure Score -> Mission Status Banner.
- Incident template + incident markdown -> Incident Card.
- Internet Score + Internet Intelligence + Internet Quality -> Network Health Card.
- DNS Score + DNS Intelligence + DNS Quality -> DNS Health Card.
- Pi4 Health + Probe Freshness -> Pi4 Health Card.
- MQTT Broker + Probe Publish -> MQTT Health Card.
- UPS Protection + UPS Detail summary -> Power Health Card.

## Popups

Use popups for:

- full entity lists
- firmware details
- MAC/IP/serial detail
- service ports
- detailed UPS data
- detailed Huawei data
- camera service raw data
- long host metrics

## Drill-Down Pages

Use drill-down pages for:

- incident history
- timeline
- topology graph
- full inventory
- network diagnostics
- DNS/Pi-hole diagnostics
- MQTT diagnostics
- server diagnostics
- power diagnostics
- camera diagnostics

## Terminology Standardization

Replace inconsistent terms:

- Internet Score
- Internet Intelligence
- Internet Quality
- Internet Health

With:

- Internet Health

Use the same pattern:

- DNS Health
- MQTT Health
- Power Health
- Inventory Health
- Server Health

Use:

- Recommendation, not advice/hint/tip.
- Data Freshness, not probe freshness/last update/update age.
- Domain Health, not score breakdown.
- Capability, not feature/role/service when referring to what a device provides.

## Commercial NOC First View

The first viewport of Executive should contain:

- Mission Status
- Current Incident
- Recommendation
- Affected Systems

If there is an active critical incident, nothing visually interesting should outrank it.

## Migration Approach

1. Freeze existing dashboards as v1 reference.
2. Build new v2 dashboard files separately.
3. Start with Executive and Operations only.
4. Build Diagnostics / Mission Control second.
5. Rebuild Inventory, Network, and Servers using the same card vocabulary.
6. Validate mobile/tablet/desktop manually.
7. Keep the old dashboard available until v2 is verified.

## Acceptance Criteria

Dashboard v2 is complete when:

- Executive has exactly seven visual elements.
- Operations has only live domain health cards.
- Diagnostics is incident-centered.
- No Executive page card contains a graph or entity table.
- Terminology is consistent across all pages.
- Every repeated concept uses the same icon.
- Raw detail exists only on Diagnostics, drill-down pages, or popups.
- Existing HIOC capabilities remain reachable.
- Public Home Assistant entities do not need to change.
