# HIOC Dashboard Review

Review scope:

- `homeassistant/dashboards/home_infrastructure_hioc_incident_center_v12.yaml`
- `homeassistant/dashboards/living_inventory.yaml`
- `homeassistant/dashboards/incident_command_card.yaml`

No dashboard YAML was modified.

## Executive Summary

The dashboards show strong operational intent: HIOC is trying to be a command center, not a pile of sensors. The best existing patterns are the Incident Center, the “what/why/affected/action” framing in Living Inventory, and the diagnostics pages that acknowledge telemetry gaps.

The current implementation is not yet a commercial NOC console. It is dense, repetitive, visually inconsistent, and over-dependent on environment-specific entities. The main dashboard tries to be executive overview, live wallboard, diagnostics, topology, service inventory, trend console, and telemetry gap tracker at the same time. That creates a long scroll, weak prioritization, and too many cards competing for attention.

The redesign should separate:

- Executive command view: current status, active incident, blast radius, recommended action, top risks.
- Domain pages: Network, Servers, Inventory, Services, Power, Cameras.
- Diagnostics: deep troubleshooting and raw telemetry.
- Drill-downs/popups: entity-heavy details and historical graphs.

## Evaluation

### Information Architecture

Current quality: mixed.

The main dashboard has sensible view names: Executive, Servers, Network, Diagnostics. But the Executive view contains too many operational details, repeated score cards, live trend strips, quick metrics, service status, topology, and event timeline content. Diagnostics also duplicates many domain sections.

The Living Inventory dashboard is conceptually clean: summary, counts, graph coverage, device health, services. It is a better pattern for future pages.

Key issue: views are organized partly by audience and partly by system domain. A commercial NOC needs both, but with stricter boundaries.

### Visual Hierarchy

Current quality: medium-low.

The dashboards use strong status colors and large markdown panels, but the hierarchy is inconsistent. Some sections use large decorative markdown cards; others use Mushroom cards; others use entity tables and mini graphs. Critical operational state does not always dominate the viewport because many equal-weight cards compete.

The Executive page should have one unmistakable primary state: operational, degraded, incident, or critical. Everything else should support that.

### Operator Workflow

Current quality: medium.

The incident card answers useful questions: what happened, root cause, confidence, impact, evidence, and recommendation. That is exactly the right NOC workflow.

The weakness is navigation after the recommendation. The operator should be able to jump from an incident to affected systems, dependency graph, and relevant diagnostics. Today the operator scrolls through many sections and must infer where to go.

### Color Usage

Current quality: medium.

Green/amber/red semantics are used consistently in places, but the UI overuses colored cards, gradients, and status icons. Large dark/blue gradient cards make the dashboard feel custom and atmospheric rather than cleanly operational.

Commercial NOC color should be sparse:

- Green only for confirmed healthy rollups.
- Amber for degraded/watch.
- Red for active outage or critical incident.
- Neutral surfaces for normal detail.
- Avoid decorative gradients except possibly a small status header.

### Card Consistency

Current quality: low-medium.

The dashboard mixes:

- markdown cards
- Mushroom title cards
- Mushroom template cards
- entity cards
- mini-graph cards
- nested grid cards
- card_mod-heavy style blocks

The result feels handcrafted rather than systematized. A NOC console should use a small set of repeated card archetypes:

- status banner
- incident command card
- KPI tile
- domain health row
- trend sparkline
- entity detail table
- diagnostic drill-down

### Responsiveness

Current quality: medium.

The `sections` layout helps, and many cards use `grid_options`. However, some markdown cards are tall, text-heavy, and use fixed row counts. The Executive page in particular risks turning into a long scroll on tablets and mobile.

The Living Inventory page is more responsive because it has fewer cards and clearer sections.

### Performance

Current quality: medium-low.

The main dashboard contains many mini-graph-card instances and many templated markdown cards. This can become heavy on tablets, wall displays, and mobile browsers. Some cards reference large JSON attributes, especially inventory device/service lists.

High-cost cards should move to drill-down pages or popups:

- long historical mini graphs
- entity-heavy diagnostic lists
- raw device inventory markdown loops
- service add-on tables

### Duplicate Information

Current quality: low.

There is significant duplication:

- incident status appears in multiple forms
- internet/DNS/MQTT/UPS scores appear in Executive, Network, Diagnostics, and Quick Metrics
- Pi4/Pi5 metrics appear in Executive trends, Servers, and Diagnostics
- MQTT publish latency appears in Executive, Network/Diagnostics, and MQTT Diagnostics
- Huawei WAN appears in quick metrics, Network, and Diagnostics
- UPS appears in quick metrics, diagnostics, and score breakdown

Duplication is useful only when information changes granularity. Current duplication often repeats the same fact with a different card style.

### Missing Information

Important missing NOC information:

- active incident age and current phase in a compact top bar
- affected devices/services list tied to the active incident
- “next best action” as a first-class element
- engine health: incident/history/inventory last run, duration, failures
- MQTT broker health from HIOC’s perspective
- data freshness by subsystem
- dependency graph summary on Executive
- inventory changes since last run
- maintenance mode / muted alerts / notification status
- top degraded devices
- top noisy sensors or repeated incidents
- capability summary: DNS, DHCP, MQTT, UPS, gateway, recorder, camera, Z-Wave, Matter

### Card Density

Current quality: high density, uneven.

Executive is too dense for an executive/NOC first page. Diagnostics is expected to be dense, but should be grouped by domain and use drill-downs.

Inventory is closer to the right density but needs tables or auto-entities instead of long markdown loops for many devices.

### Navigation

Current quality: medium.

There are useful top-level views, but hierarchy is not explicit enough. A commercial NOC should have predictable routes:

- Executive
- Incidents
- Inventory
- Network
- Servers
- Services
- Power
- Cameras
- Diagnostics

For this repository’s current scope, five primary pages are enough:

- Executive
- Inventory
- Network
- Servers
- Diagnostics

Everything else can be a section or drill-down.

### Accessibility

Current quality: medium-low.

Issues:

- color is often the primary state indicator
- dense markdown text may be hard to scan
- emoji/status dots can be unclear to screen readers
- long secondary strings in Mushroom cards may truncate
- gradients and dark cards may reduce contrast depending on theme

Use text labels plus color. Keep status names explicit: Healthy, Watch, Degraded, Critical.

### Mobile Usability

Current quality: low-medium.

The Executive dashboard is likely too long and graph-heavy on mobile. Important incident/action content should be first, compact, and followed by small domain rollups. Detailed graphs and entity tables should move to drill-down pages.

The Living Inventory dashboard is more mobile-friendly but the device markdown list will become unwieldy with many devices.

### Tablet Usability

Current quality: medium.

Tablet is likely the sweet spot for the current design. However, the main dashboard still has too many equal-weight sections. A tablet wallboard should prioritize:

- status
- incident
- domain health
- top degraded services
- freshness

### Desktop Usability

Current quality: medium.

Desktop can absorb the density, but the dashboard still lacks a strong NOC hierarchy. Wide desktop should use columns intentionally:

- left: current incident/action
- center: domain health and topology/impact
- right: freshness, recent events, top risks

## Commercial NOC Dashboard Hierarchy

Recommended primary navigation:

1. Executive
2. Inventory
3. Network
4. Servers
5. Diagnostics

Optional later pages:

- Incidents
- Services
- Power
- Cameras
- Topology
- Reports

## Executive Page

Purpose: answer “Are we okay? If not, what do I do now?”

Keep:

- Mission status / global status, but redesign as a compact top status banner.
- Incident command card.
- Domain health summary for Internet, DNS, Power, Services, Inventory.
- Latest timeline event.
- Top degraded/offline devices.
- Data freshness / engine health.

Move away from Executive:

- Live Trend Strip with many graphs.
- Detailed Pi4/Pi5 host graphs.
- Detailed MQTT broker/add-on diagnostics.
- Huawei WAN detail.
- UPS detail.
- Camera service detail.
- Confirmed telemetry gaps.
- Long score breakdown markdown.

Executive recommended layout:

1. Top status banner: `Operational / Degraded / Critical`, active incident count, infrastructure score, inventory count, last update.
2. Incident Command: title, severity, root cause, confidence, impact, recommendation.
3. Affected Systems: list from incident/inventory/dependency graph.
4. Domain Health Row: Network, DNS, MQTT, Power, Servers, Inventory.
5. Top Risks: degraded devices, stale telemetry, forecast warnings.
6. Latest Events: last 5 timeline/internal events.

## Inventory Page

Purpose: answer “What exists, what changed, what is unhealthy, and what depends on it?”

Keep:

- Living Inventory summary.
- Inventory counts.
- Graph coverage.
- Device health.
- Services.

Improve:

- Convert long markdown device list into a table-like card or auto-entities style grouping by health.
- Add sections for New Devices, Offline Devices, Stale Devices, Infrastructure Devices, and Capabilities.
- Show topology/dependency summary as a graph or compact relation table.

Move to popups:

- full firmware blob
- raw MAC/IP details
- per-device health reasons
- service ports

Inventory recommended layout:

1. Inventory status banner.
2. Counts: total, healthy, watch, degraded, offline, services, capabilities.
3. Changes: newly discovered, disappeared, stale.
4. Infrastructure devices: gateway, switches, APs/satellites, Pi4, Pi5.
5. Device health table.
6. Services/capabilities table.
7. Dependency graph drill-down.

## Network Page

Purpose: answer “Is the network path healthy, and where is degradation located?”

Keep:

- Internet operations.
- Gateway/internal path.
- DNS operations.
- WAN/traffic.
- Probe diagnostics.

Move from Executive:

- Internet latency graph.
- Packet loss graph.
- DNS latency graph.
- Gateway latency graph.
- WAN download/upload graphs.

Merge:

- Internet score, internet intelligence, internet quality, packet loss, latency, jitter into one Network Health panel.
- DNS score, DNS quality, Pi-hole latency, Cloudflare latency, query pressure into one DNS Health panel.
- Gateway WAN status and Huawei detail into one Gateway/WAN panel.

Move to popups:

- full Huawei WAN entity table
- raw probe publish details
- long historical graphs

Network recommended layout:

1. Network status banner.
2. Path diagnosis: gateway, WAN, DNS, internet, MQTT publish.
3. Four core trends: latency, loss, DNS, gateway.
4. WAN throughput.
5. Probe freshness.
6. Drill-downs for Huawei, DNS/Pi-hole, MQTT path.

## Servers Page

Purpose: answer “Are the infrastructure hosts healthy?”

Keep:

- Pi4 Probe Appliance.
- Pi5 Home Assistant Host.
- Host comparison trends.

Move from Diagnostics:

- Pi4 detail.
- Pi5 detail.
- recorder/storage pending telemetry once implemented.

Merge:

- Pi4 health and probe freshness into one Pi4 Host card.
- Pi5 host and HA core/supervisor resource use into one Pi5 Host card.

Move to popups:

- full entity lists
- CPU/memory/storage graphs beyond the first three
- package/toolkit versions

Servers recommended layout:

1. Host status row: Pi4, Pi5, MQTT broker host if separate.
2. Pi4 card: temp, memory, disk, probe freshness, services.
3. Pi5 card: CPU, memory, disk, temperature, HA core/supervisor health.
4. Trends: CPU, memory, temperature, disk.
5. Host details drill-down.

## Diagnostics Page

Purpose: answer “What raw facts help me troubleshoot a known problem?”

Keep:

- deep troubleshooting panels
- entity tables
- telemetry gap tracking
- MQTT diagnostics
- UPS diagnostics
- Huawei diagnostics
- camera diagnostics

Move into Diagnostics:

- most Executive mini graphs
- raw service add-on entity lists
- pending telemetry cards
- long detailed entity cards

Diagnostics should be domain-grouped:

1. Incident Diagnostics
2. Network Diagnostics
3. DNS/Pi-hole Diagnostics
4. MQTT Diagnostics
5. Power/UPS Diagnostics
6. Host Diagnostics
7. Camera/Video Diagnostics
8. Telemetry Gaps

## Cards That Should Move

- Live Trend Strip: move from Executive to Network and Diagnostics.
- Quick Metrics: split into domain pages; remove as a standalone Executive section.
- Score Breakdown: replace with compact Domain Health Row on Executive.
- Pi4/Pi5 detailed host sections: move to Servers.
- MQTT & Service Bus Diagnostics: move to Diagnostics or a future Services page.
- UPS Diagnostics: move to Diagnostics or future Power page.
- Huawei Gateway Diagnostics: move to Network/Diagnostics.
- Cameras & Video Services: move to Diagnostics or future Cameras page.
- Diagnostics Telemetry Gaps: keep only on Diagnostics.

## Cards That Should Disappear

- Empty spacer markdown cards such as `<br>`.
- Repeated score breakdown markdown if domain health cards exist.
- Duplicate WAN IP cards when WAN/Gateway panel exists.
- Duplicate MQTT publish duration cards when MQTT diagnostics panel exists.
- Any Executive card that only repeats a metric already shown in a domain health row.

## Cards That Should Merge

- Incident Center template card + incident markdown detail should become one consistent Incident Command card.
- Mission Status + Infrastructure Score graph should become a compact top banner plus optional score trend popup.
- Internet Score + Internet Intelligence + Internet Quality should become one Network Health card.
- DNS Score + DNS Intelligence + DNS Quality should become one DNS Health card.
- Pi4 Health + Probe Freshness should become one Pi4 Operations card.
- MQTT Broker + Probe Publish should become one MQTT Service Bus card.
- UPS Protection + UPS detail summary should become one Power Protection card.

## Cards That Should Become Popups

- Full Pi4 entity detail.
- Full Pi5 entity detail.
- Full MQTT detail.
- Connected add-ons list.
- Huawei WAN detail.
- UPS detail.
- Camera service detail.
- Raw inventory device firmware details.
- Long trend graphs beyond the primary 24h signal.
- Telemetry gap explanations from Executive.

## Cards That Should Become Drill-Down Pages

- Incident history and timeline.
- Full inventory device list.
- Topology/dependency graph.
- Network diagnostics.
- DNS/Pi-hole diagnostics.
- MQTT diagnostics.
- Host resource history.
- UPS/power history.
- Camera/video platform health.

## Recommended Card System

Use a small commercial-style card vocabulary:

- `Status Banner`: one per page.
- `Incident Command`: primary operational incident card.
- `Domain Health Card`: one row/card per domain.
- `KPI Tile`: compact metric, not paragraph text.
- `Trend Card`: only for high-value graphs.
- `Detail Table`: entity lists and diagnostics.
- `Action Card`: recommended operator action.
- `Gap Card`: missing telemetry, only in Diagnostics.

Avoid one-off styled markdown cards unless the content is genuinely narrative.

## Accessibility Recommendations

- Use explicit words alongside colors: Healthy, Watch, Degraded, Critical.
- Reduce emoji usage in status-critical text.
- Avoid relying on green/amber/red alone.
- Use consistent card titles.
- Keep secondary text short enough for mobile.
- Prefer entity tables or structured rows over long markdown paragraphs.
- Reduce gradient backgrounds and ensure contrast works in light/dark themes.

## Performance Recommendations

- Reduce graph count on Executive to zero or one.
- Put dense mini-graph grids on drill-down pages.
- Avoid rendering full inventory device lists on first page load.
- Avoid large JSON attributes in frequently visible cards when possible.
- Use summary sensors for Executive.
- Keep raw entity tables off Executive.

## Mobile Recommendations

Mobile Executive should show only:

1. status banner
2. active incident/action
3. affected systems
4. domain health row
5. latest event

Everything else should be a tap-through.

## Tablet Recommendations

Tablet layout should support wallboard mode:

- top banner
- incident card
- domain health grid
- top risks
- latest events

Avoid long scrolls on tablet wall views.

## Desktop Recommendations

Desktop Executive should use three purposeful columns:

- Left: active incident and action.
- Center: domain health and affected systems.
- Right: freshness, top risks, latest events.

Diagnostics can use more columns because it is operator-driven, not wallboard-first.

## Proposed Commercial NOC Hierarchy

### Executive

Only:

- Global status banner.
- Incident Command.
- Recommended action.
- Affected systems.
- Domain health summary.
- Top risks.
- Latest events.
- Engine/data freshness.

### Inventory

Only:

- Inventory status.
- Counts and health distribution.
- New/offline/stale devices.
- Infrastructure devices.
- Device health table.
- Service/capability table.
- Topology/dependency drill-down entry.

### Network

Only:

- Network status.
- Internet/WAN health.
- Gateway path.
- DNS/Pi-hole health.
- MQTT path health.
- Key network trends.
- Probe freshness.

### Servers

Only:

- Pi4 operations.
- Pi5 operations.
- HA core/supervisor.
- Host resource trends.
- Storage/recorder once available.
- Host detail drill-down.

### Diagnostics

Only:

- Deep raw details.
- Graph grids.
- Entity tables.
- Telemetry gaps.
- Vendor-specific panels.
- Troubleshooting drill-down content.

## Final Recommendation

The next dashboard milestone should not be more cards. It should be a hierarchy refactor.

Recommended first redesign pass:

1. Rebuild Executive as a true NOC command page with fewer than 10 cards.
2. Move raw graphs and entity tables to Diagnostics.
3. Make Inventory the model for focused domain pages.
4. Standardize card archetypes and color semantics.
5. Separate repo-owned portable dashboards from local environment-specific dashboards.

The design direction is strong. The current dashboard needs editorial discipline: less repetition, fewer equal-weight cards, clearer drill-down paths, and a stricter separation between command, domain, and diagnostic views.

