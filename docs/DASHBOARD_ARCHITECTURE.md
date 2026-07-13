# HIOC Dashboard Architecture

## Document Ownership

This document owns the architectural boundary between HIOC operational truth and dashboard presentation. It defines:

- which layers may produce operational conclusions
- which dashboard text may remain static
- how unknown and unavailable values must be presented
- when narrowly duplicated visual logic is acceptable
- how the operator-approved Dashboard v2 layout is preserved
- how the current storage-managed dashboard relates to repository YAML
- the safe direction for a future YAML-managed dashboard deployment

It does not own project direction, visual language, page intent, engine behavior, MQTT contracts, entity schemas, or the implementation roadmap. Those remain with the focused documents linked in [Related Documents](#related-documents).

## 1. Purpose

Dashboard v2 is the HIOC presentation layer. It organizes and explains operational state; it does not create that state.

HIOC engines and Home Assistant package templates own operational truth. Dashboard cards consume their entities and attributes, apply presentation-only formatting, and provide navigation or explanatory context.

Missing truth must remain visibly missing. In particular, `unknown` or `unavailable` must never be converted into healthy, zero, none, no action required, or any other all-clear conclusion.

## 2. Authoritative Source Hierarchy

Operational conclusions flow down this hierarchy:

1. **Inventory Engine** owns discovered identity, provenance, observation state, operational-monitoring eligibility, health, counts, topology, and inventory recommendations.
2. **Correlation and Incident Engines** own incident status, severity, phase, affected systems, root cause, confidence, evidence, and incident recommendations.
3. **History Engine** owns historical samples, incident history, timelines, durations, and historical summaries.
4. **Platform Core** owns platform version, component readiness, service state, and platform health.
5. **Predictive Analytics** owns forecast state, trend conclusions, and forecast recommendations.
6. **Home Assistant packages** translate retained MQTT payloads and their attributes into stable, defensive entities. Package templates may combine authoritative fields when the package is the declared owner of the resulting conclusion.
7. **Dashboard templates** render those entities. They may select labels, colors, visibility, and explanatory wording, but must not become an independent source of operational truth.

Representative authoritative entities include:

- `sensor.hioc_inventory_operations_summary`
- `sensor.hioc_inventory_recommended_action`
- inventory count entities and inventory payload attributes
- `sensor.hioc_incident_status`
- `sensor.hioc_incident_severity`
- `sensor.hioc_incident_recommendation`
- incident summary, evidence, affected-system, root-cause, confidence, phase, and timeline entities or attributes
- platform status and component entities from `hioc_platform.yaml`
- forecast entities from `hioc_predictive_analytics.yaml`

When an entity already owns a conclusion, the dashboard must render that entity instead of recreating its policy.

## 3. Allowed Static Interface Copy

Static dashboard text is allowed when it does not assert current operational truth. Valid uses include:

- card and section titles
- field labels such as `Root cause` or `Recommended action`
- navigation instructions such as `Click: Diagnostics`
- explanatory descriptions of what a card or metric means
- wording inside a branch whose condition is derived from authoritative entity state
- fixed visual vocabulary such as severity labels and their approved colors, provided the selected branch is driven by authoritative status and severity

Examples:

```jinja
Click: Diagnostics for evidence and timeline.
```

```jinja
{% if severity == 'major' %}
  Major incidents require prompt investigation.
{% endif %}
```

The second example is valid only when `severity` was normalized from the authoritative incident-severity entity and the incident is authoritatively active.

## 4. Prohibited Hardcoded Operational Truth

The dashboard must not hardcode, infer independently, or unconditionally duplicate current:

- health, service, platform, forecast, incident, or recovery state
- incident severity
- degraded, offline, watch, affected-system, or other operational counts
- root cause, confidence, evidence, or affected systems
- active recommendations or whether operator action is required
- device-specific names, addresses, identifiers, counts, or statuses

Unacceptable:

```jinja
{% if states('sensor.hioc_incident_status') == 'active' %}Critical{% endif %}
```

Active status alone does not imply Critical severity.

Unacceptable:

```jinja
Recommended action: No action required.
```

This asserts an all-clear result without evaluating authoritative state.

Acceptable:

```jinja
Recommended action: {{ states('sensor.hioc_inventory_recommended_action') }}
```

Acceptable visual branch:

```jinja
{% set status = states('sensor.hioc_incident_status') | lower %}
{% set severity = states('sensor.hioc_incident_severity') | lower %}
{% if status == 'active' and severity == 'critical' %}
  red
{% elif status == 'active' and severity == 'major' %}
  deep orange
{% elif status == 'active' and severity == 'warning' %}
  amber
{% else %}
  gray
{% endif %}
```

This is acceptable only as a styling decision and must remain aligned with the authoritative package semantics through focused tests.

## 5. Unknown and Unavailable Semantics

`unknown`, `unavailable`, missing, empty, malformed, or unrecognized values mean that HIOC cannot currently establish the conclusion.

They must render as an explicit neutral unknown state or an unavailable explanation. They must not silently become:

- `0`
- Healthy
- Operational
- None or No active incident
- No action required
- Offline
- Stopped

Unknown is not evidence of failure, but it is also not evidence of health. Templates must normalize case, protect missing attributes, handle `None`, and provide complete labels and valid CSS for every branch.

Where a package entity provides a defensive unknown result, the dashboard should display it directly. Where visual branching is necessary, unknown and unrecognized values use the neutral gray presentation and an explicit `Unknown` label.

## 6. Duplication Policy

Operational policy belongs in engines and package entities. Dashboard duplication is permitted only when Home Assistant card behavior requires narrowly visual branching, such as:

- severity color or border selection
- conditional visibility
- icon selection
- compact display labels

Any permitted duplication must:

1. read the same authoritative raw entities or attributes
2. reproduce only the minimum presentation decision
3. default safely for missing and future values
4. have focused regression coverage proving alignment with the authoritative behavior

Line-count reduction is not a reason to create helper entities, restructure cards, or introduce a new abstraction. Conversely, standalone Lovelace and `card_mod` templates may repeat small defensive branches when Home Assistant cannot share local template state. Such repetition is acceptable when tests enforce identical behavior.

## 7. Operator Layout Baseline

The operator-supplied Dashboard v2 YAML is the authoritative visual and layout baseline. Functional corrections must be reconciled onto that baseline without resetting manually refined presentation choices.

The protected baseline includes:

- view titles, order, paths, icons, and theme
- sections and their order
- card order and titles
- vertical-stack and grid nesting
- `max_columns`
- `column_span`
- `grid_options.columns`
- `grid_options.rows`
- minimum heights and card dimensions
- navigation paths
- `card_mod` styling
- spacing and visual hierarchy

The repository file `homeassistant/dashboards/hioc_dashboard_v2.yaml` is the version-controlled baseline after approved layout and functional changes are reconciled. Operational corrections may change template behavior, but they must not casually rewrite layout or formatting.

## 8. Layout Regression Protection

`tests/test_dashboard_layout.py` structurally validates Dashboard v2 instead of relying on broad text presence. Its protected contract includes:

- ordered view titles, paths, and icons
- per-view `max_columns`
- section count and order
- recursive card types, titles, and order
- grid columns and rows
- column spans
- navigation paths
- vertical-stack and grid structure
- a structural fingerprint of the reconciled operator baseline

Functional tests separately protect inventory presentation, dynamic-truth rules, and incident-severity behavior. A layout fingerprint change requires deliberate review against the operator baseline; it must not be updated merely to make a test pass.

## 9. Current Deployment Architecture

The current live Dashboard v2 is a **storage-managed Lovelace dashboard**. Its content is stored by Home Assistant and is independent of `/config/dashboards/hioc_dashboard_v2.yaml`.

`homeassistant/install_ha.sh` currently:

1. copies repository package YAML into `/config/packages`
2. copies repository dashboard YAML into `/config/dashboards`
3. backs up overwritten copied files

The repository does not currently register `hioc_dashboard_v2.yaml` under a Lovelace YAML dashboard configuration. Therefore Home Assistant does not consume the copied dashboard file for the live storage-managed dashboard. Copying the repository file updates a deployment artifact, not the live Lovelace storage record.

That is why the operator currently must paste YAML through the Home Assistant dashboard editor. Edits made in storage mode can also diverge from the repository file and may need manual layout reconciliation.

No Home Assistant dashboard mode is changed by this documentation checkpoint.

## 10. Planned YAML-Mode Migration

A future, separately approved checkpoint should evaluate registering Dashboard v2 as a YAML-mode dashboard while preserving the current storage dashboard as a rollback surface.

The safest migration direction is:

1. retain the current storage-managed dashboard unchanged during validation
2. register the repository-installed file as a separate YAML-mode dashboard
3. preserve the HIOC Operations theme, operator layout, and practical URL behavior
4. validate navigation paths and approve any path updates before switching operator traffic
5. compare the YAML dashboard visually on desktop, tablet, and mobile
6. keep an export of the storage dashboard and a repository revision for rollback
7. switch or retire the old entry only after explicit operator approval

Home Assistant `.storage` files must never be edited directly as a deployment mechanism. A storage-mode import tool could be evaluated as an alternative, but it would need backups, deterministic structural validation, and an officially supported write path. Until that exists, the repository file is the reviewed source baseline but not the automatically rendered live dashboard.

This migration is planned architecture, not current implementation.

## 11. Dashboard Change Workflow

Every Dashboard v2 change should follow this sequence:

1. Identify the authoritative engine, payload attribute, or Home Assistant entity for every operational conclusion affected.
2. Confirm whether the change is functional, visual, structural, or deployment-related.
3. Start from the repository copy of the approved operator layout baseline.
4. Prefer an existing authoritative entity over dashboard-local policy.
5. Keep unavoidable dashboard branching narrowly visual and default-safe.
6. Preserve entity IDs, view paths, navigation, card structure, dimensions, theme, and layout unless the approved task explicitly changes them.
7. Add focused tests that locate the exact card or template deterministically and exercise every relevant state branch.
8. Run dynamic-truth, layout, severity, inventory-presentation, YAML, UTF-8, Home Assistant, link, and whitespace validation as applicable.
9. Review the full diff for unrelated formatting churn and operational literals.
10. Obtain operator approval before committing, pushing, or changing dashboard deployment mode when the checkpoint requires it.

## 12. Related Documents

- [HIOC Master Plan](HIOC_MASTER_PLAN.md) owns project direction, phases, objectives, and working agreements.
- [HIOC Design System](DESIGN_SYSTEM.md) owns visual language, terminology, card archetypes, colors, spacing, and operator UX rules.
- [Dashboard v2 Plan](DASHBOARD_V2_PLAN.md) owns page purposes, information architecture, navigation intent, and dashboard implementation decisions. This document adds the operational-truth and baseline-preservation boundary.
- [Home Assistant Integration](HOME_ASSISTANT.md) owns packages, entities, installation, and Home Assistant integration points.
- [HIOC Architecture Decisions](../DECISIONS.md) records why long-lived technical decisions were made.
- [MQTT Contract](MQTT.md) owns retained topics and payload transport contracts.
- [HIOC Data Model](DATA_MODEL.md) owns payload field meanings and schemas.

If these documents appear to conflict, use the ownership boundaries above: engines and their contracts own data truth; Home Assistant packages own entity translation and declared composite conclusions; this document owns dashboard truth consumption and layout preservation; the Master Plan owns project direction.
