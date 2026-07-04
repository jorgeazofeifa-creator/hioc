# HIOC Design System

HIOC is an operations platform rendered through Home Assistant. It is not a general-purpose Home Assistant dashboard collection.

The interface must help an operator understand:

- What is happening?
- Why is it happening?
- What is affected?
- What should I do?

## Design Principles

1. Critical information always outranks interesting information.
2. Executive pages do not show raw diagnostics.
3. Graphs appear only when trends matter to the decision being made.
4. Every page has one primary purpose.
5. Cards use a small, consistent vocabulary.
6. Color communicates state, not decoration.
7. Terminology is stable across every page.
8. Mobile views must show the operational answer before supporting data.

## Page Roles

### Executive

Question: Do I need to get out of my chair?

Executive has exactly seven visual elements:

1. Mission Status
2. Current Incident
3. Affected Systems
4. Domain Health
5. Top Risks
6. Latest Events
7. Data Freshness

Executive contains:

- zero graphs
- zero entity tables
- zero raw diagnostics
- zero inventory tables
- zero decorative metric grids

### Operations

Question: What is happening right now?

Operations is the wallboard page. It shows live operational state across domains.

It contains domain tiles only:

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

Operations contains:

- no graphs
- no raw entity tables
- no long text blocks
- no drill-down detail unless tapped

### Diagnostics / Mission Control

Question: What exactly is happening, why, and what evidence proves it?

Diagnostics is incident-centered. It should begin with the active incident and then show evidence, dependency path, timeline, and live telemetry.

Diagnostics contains:

- incident detail
- evidence list
- dependency graph
- timeline
- live telemetry
- domain-specific raw data
- drill-down diagnostic panels

### Inventory

Question: What exists, what changed, what is unhealthy, and what depends on it?

Inventory contains:

- inventory summary
- new devices
- offline devices
- stale devices
- infrastructure devices
- device health table
- service and capability table
- topology/dependency drill-down

### Network

Question: Is the network path healthy, and where is degradation located?

Network contains:

- internet health
- WAN/gateway health
- DNS health
- MQTT path health
- probe freshness
- key network trends
- network diagnostic drill-downs

### Servers

Question: Are the infrastructure hosts healthy?

Servers contains:

- Pi4 operations
- Pi5 operations
- Home Assistant core/supervisor health
- host resource trends
- storage/recorder health when available
- host detail drill-downs

## Card Archetypes

HIOC uses exactly eight primary card archetypes.

### 1. Status Banner

Purpose: express the page's highest-level state.

Used on:

- Executive
- Operations
- Diagnostics
- Inventory
- Network
- Servers

Rules:

- one per page
- always at the top
- state word must be explicit
- color must match severity
- no detailed diagnostics

### 2. Incident Card

Purpose: summarize the current incident.

Content:

- severity
- title
- root cause
- confidence
- started time
- duration
- recommendation

Rules:

- appears on Executive and Diagnostics
- compact on Executive
- expanded on Diagnostics

### 3. Health Card

Purpose: show one domain or subsystem state.

Content:

- domain name
- state
- one reason
- one most relevant metric
- optional icon

Rules:

- one domain per card
- no long history
- no raw entity list

### 4. Trend Card

Purpose: show recent movement when trend changes operator action.

Rules:

- not allowed on Executive
- allowed on Network, Servers, Diagnostics
- max four primary trend cards per domain page
- detail trends move to drill-down pages

### 5. Detail Table

Purpose: show raw or semi-raw detail.

Rules:

- not allowed on Executive
- not allowed on Operations
- allowed on Inventory and Diagnostics
- should be grouped by state or domain

### 6. Action Card

Purpose: tell the operator what to do next.

Content:

- recommended action
- reason
- affected system
- optional link target

Rules:

- Executive shows only one primary action
- Diagnostics may show multiple supporting actions

### 7. Risk Card

Purpose: show likely future or developing issues.

Content:

- risk title
- severity
- affected domain
- forecast or evidence

Rules:

- Executive shows top three only
- detailed risk explanation belongs on Diagnostics or domain pages

### 8. Timeline Card

Purpose: show ordered operational events.

Content:

- time
- event
- severity/source

Rules:

- Executive shows latest three to five events
- Diagnostics shows incident-scoped timeline

## Color Semantics

Color is reserved for state.

### Green

Meaning: healthy, confirmed operational.

Use for:

- healthy domain
- recovered service
- no active incident

Do not use for decoration.

### Amber

Meaning: watch, degraded, early warning.

Use for:

- stale data
- warning thresholds
- forecasted risk
- degraded but functioning service

### Red

Meaning: critical, outage, active incident requiring attention.

Use for:

- active critical incident
- offline required service
- failed infrastructure dependency

### Blue

Meaning: informational, neutral operational data.

Use for:

- selected page
- informational state
- neutral trend

### Gray

Meaning: inactive, unavailable, unknown, or not configured.

Use for:

- missing telemetry
- disabled subsystem
- not applicable capability

## Typography

### Page Title

Use short nouns:

- Executive
- Operations
- Diagnostics
- Inventory
- Network
- Servers

### Section Title

Use 1-3 words:

- Current Incident
- Domain Health
- Top Risks
- Latest Events
- Data Freshness

### Status Text

Use exact state words:

- Operational
- Watch
- Degraded
- Critical
- Offline
- Unknown

Do not mix alternatives like Healthy, Good, OK, Fine, Normal, Excellent, or Intelligence for the same concept.

## Terminology

Use one term everywhere:

- Domain Health, not score/intelligence/quality interchangeably.
- Incident, not alert/problem/event for the same object.
- Recommendation, not hint/tip/advice/action in different places.
- Data Freshness, not last update/probe freshness/age inconsistently.
- Inventory, not devices/assets/equipment interchangeably.
- Capability, not feature/service/role when describing what a device provides.

## Icon Vocabulary

Use stable icons for repeated concepts.

- Mission Status: `mdi:monitor-dashboard`
- Incident: `mdi:alert-decagram`
- Internet: `mdi:web-check`
- DNS: `mdi:dns`
- MQTT: `mdi:message-processing`
- Power: `mdi:power-plug-battery`
- Pi4: `mdi:raspberry-pi`
- Pi5 / Home Assistant: `mdi:home-assistant`
- Inventory: `mdi:devices`
- Forecast: `mdi:chart-timeline-variant`
- Backup: `mdi:backup-restore`
- Automation: `mdi:robot`
- Diagnostics: `mdi:stethoscope`
- Timeline: `mdi:timeline-clock`
- Data Freshness: `mdi:clock-check`

Do not change icons between pages for the same concept.

## Spacing And Density

Use three density levels:

### Command Density

Used on Executive.

- very few cards
- high contrast hierarchy
- no tables
- no graph grids

### Wallboard Density

Used on Operations.

- uniform domain tiles
- compact but readable
- optimized for glanceability

### Diagnostic Density

Used on Diagnostics and drill-down pages.

- entity tables allowed
- graph grids allowed
- raw values allowed
- grouped by troubleshooting path

## Responsive Rules

### Mobile

First screen must show:

1. mission status
2. current incident
3. recommended action

No graph should appear before the action.

### Tablet

Optimize for wallboard mode:

- status banner
- incident card
- domain health grid
- top risks
- latest events

### Desktop

Use three intentional columns on Executive:

- left: incident and action
- center: affected systems and domain health
- right: risks, events, freshness

## Anti-Patterns

Avoid:

- equal-weight cards for unequal information
- large decorative markdown panels
- graphs on Executive
- raw entity tables on Executive or Operations
- repeated status cards across pages
- multiple names for the same concept
- environment-specific entities on portable dashboards
- spacer cards
- one-off card styles
- color used only for decoration

