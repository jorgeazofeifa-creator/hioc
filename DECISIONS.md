# HIOC Architecture Decisions

## Document Ownership

This file is the Architecture Decision Record log.

The Master Plan says what HIOC is doing and where it is going. This file explains why long-term technical decisions were made.

Each decision should contain:

- Decision
- Status
- Context
- Alternatives
- Reason
- Consequences

Do not duplicate roadmap, current phase, or implementation status. Those belong in [docs/HIOC_MASTER_PLAN.md](docs/HIOC_MASTER_PLAN.md).

## ADR-0001: Keep Pi4 Toolkit Compatibility

Decision: HIOC reads existing Pi4 telemetry and does not replace the Pi4 toolkit.

Status: Accepted.

Context: Existing installations already depend on Pi4 toolkit telemetry and scripts.

Alternatives: Replace the Pi4 toolkit or require a migration before HIOC can run.

Reason: Existing installations remain stable while HIOC adds higher-level incident, forecast, and inventory behavior.

Consequences: HIOC must preserve compatibility with legacy telemetry sources and avoid breaking existing Pi4 toolkit workflows.

## ADR-0002: Use Retained MQTT as the Home Assistant Contract

Decision: HIOC publishes retained JSON payloads under `home/infrastructure/hioc`.

Status: Accepted.

Context: Home Assistant dashboards and sensors need current operational state after restarts.

Alternatives: Poll local files directly from Home Assistant or use non-retained MQTT.

Reason: Home Assistant restarts should recover the latest operational state without waiting for a fresh engine run.

Consequences: Payload compatibility matters. New fields should be additive whenever possible, and public topic names should remain stable.

## ADR-0003: Store Local JSON Before MQTT Publication

Decision: Engines persist state under `state/` before publishing MQTT.

Status: Accepted.

Context: MQTT or Home Assistant may be unavailable during an infrastructure incident.

Alternatives: Publish only to MQTT or move persistence immediately into a database.

Reason: Local files preserve diagnosis data when MQTT or Home Assistant is degraded.

Consequences: JSON state files are part of the operational recovery story and must remain inspectable and valid.

## ADR-0004: Living Inventory Uses Real Discovery Sources

Decision: Inventory discovery uses real local and passive infrastructure sources before any active discovery.

Status: Accepted.

Context: Inventory must represent observed infrastructure, not demo data.

Alternatives: Static inventory files, mock data, hardcoded devices, or active discovery as the primary source.

Reason: Production inventory must reflect trustworthy observed infrastructure while avoiding disruption.

Consequences: Inventory richness depends on available passive sources such as local host facts, routes, neighbor tables, DHCP leases, integrations, systemd, and sockets.

## ADR-0005: Modular Python Runtime for New Subsystems

Decision: New Python subsystem code lives in reusable modules under `pi4/lib/hioc`.

Status: Accepted.

Context: HIOC has multiple engines that need configuration, logging, JSON state, MQTT, validation, and data modeling.

Alternatives: Keep helpers embedded in each executable or use only shell scripts.

Reason: Configuration, logging, JSON state, MQTT, and data modeling should be shared as HIOC grows.

Consequences: New engines should prefer shared runtime modules instead of duplicating local helpers.

## ADR-0006: Keep JSON And Cron While Adding Core Contracts

Decision: HIOC Core v1.0 keeps JSON state files and cron scheduling, but centralizes state writes, config loading, logging, schemas, events, drivers, and capabilities.

Status: Accepted.

Context: Current deployment scale is a home infrastructure environment with a small number of hosts and devices.

Alternatives: Move immediately to SQLite, replace cron with an internal scheduler, or leave every engine fully independent.

Reason: Current deployment scale does not require a database or scheduler replacement. Shared contracts provide most of the maintainability gain without adding premature operational complexity.

Consequences: Cron and JSON remain operationally simple, while future refactors can build on shared contracts.

## ADR-0007: Internal Events Are Local State

Decision: Internal semantic events are written to local JSON state and do not replace public MQTT topics.

Status: Accepted.

Context: Engines need semantic context without breaking Home Assistant or external MQTT consumers.

Alternatives: Publish all internal events as public MQTT contracts, remove events, or require engines to poll each other.

Reason: MQTT remains the Home Assistant and external integration contract. Local events reduce internal coupling while preserving compatibility.

Consequences: Internal events can evolve faster than public MQTT, but they must remain bounded and valid local state.

## ADR-0008: HIOC Dashboards Are Operations Surfaces

Decision: HIOC dashboard v2 uses a defined design system and operations hierarchy rather than ad hoc Lovelace cards.

Status: Accepted.

Context: HIOC is intended to guide an operator, not merely display sensor values.

Alternatives: Continue adding cards organically or keep one broad dashboard where every card has similar visual weight.

Reason: Commercial operations consoles need prioritization, consistent terminology, and repeatable card patterns. Executive, Operations, Diagnostics, Inventory, Network, and Servers each answer different operator questions.

Consequences: Dashboard changes should preserve the design system and reduce cognitive load.

## ADR-0009: Releases Use Versioned Packages

Decision: HIOC has a formal release process with a version manifest, build/package scripts, install/upgrade/rollback wrappers, and runtime version reporting.

Status: Accepted.

Context: HIOC should be installable, upgradeable, and recoverable as production software.

Alternatives: Continue copying files manually or rely only on Git checkout.

Reason: HIOC should behave like installable software rather than a collection of copied files. Versioned artifacts and rollback metadata improve operator confidence and support long-term maintenance.

Consequences: Release scripts, validation, and version manifest changes should be handled deliberately.

## ADR-0010: Correlation v2 Preserves the Public Incident Contract

Decision: Correlation Engine v2 consumes Core events and inventory context internally, but continues to publish incidents through the existing retained MQTT topics and Home Assistant incident sensors.

Status: Accepted.

Context: Root-cause analysis and incident lifecycle detail need to evolve without breaking dashboards and automations.

Alternatives: Rename incident topics, replace existing sensors, or keep only the legacy incident model.

Reason: Root-cause analysis and lifecycle detail can evolve without forcing dashboard, automation, or user migration work. New fields live inside the existing incident JSON payloads while `status`, `severity`, `system`, and timeline compatibility remain intact.

Consequences: Incident payload additions must remain backward compatible unless a migration is explicitly approved.

## ADR-0011: Passive Observation Is Separate from Operational Monitoring

Decision: HIOC Core owns a single operational-monitoring predicate used by inventory health and incident correlation. Ordinary clients supported only by ARP and/or DHCP evidence remain visible as passive inventory but do not become availability incidents from observation age alone. Infrastructure, known-infrastructure, local-host, gateway, authoritative integration, and explicitly monitored records remain monitored. Unknown future sources default to monitored until their semantics are deliberately reviewed at this boundary.

Status: Accepted.

Context: Neighbor-cache absence proves that recent positive evidence is unavailable; it does not prove that an ordinary client has failed. Treating every retained passive identity as an availability target produced non-actionable incidents.

Alternatives: Continue incident generation for every discovered identity, suppress only correlation while leaving false degraded health, or scatter source exceptions across inventory and incident code.

Reason: Living Inventory documents what exists while incidents must remain operationally actionable. One conservative policy boundary prevents false client incidents without weakening infrastructure monitoring or silently suppressing future discovery sources.

Consequences: New discovery and Active Discovery sources must explicitly review this predicate. Passive-client observation timestamps remain authoritative and visible. Passive-client archival or expiration is not decided here and remains a separate future configurable checkpoint.

## ADR-0012: Evolve Living Inventory Toward an Asset-Centric Digital Twin

Decision: HIOC will evolve from device-centric discovery toward an asset-centric living digital twin. Discovered technical truth remains separate from operator-provided asset knowledge, and stable identity links the two across address changes and rediscovery. Availability and future incident interpretation will use explicit asset expectations rather than one universal rule for every device. Important assets will not be archived solely because their observation age is stale.

Status: Accepted.

Context: A discovered MAC address, IP address, hostname, or service is useful technical evidence but does not explain what the equipment means to the household. Mobile devices, core servers, safety sensors, guest clients, and retired equipment have different purposes, availability expectations, and retention needs.

Alternatives: Treat every discovered device as an equivalent availability target; store operator meaning directly as replaceable discovery facts; archive all identities after a single age threshold; or keep Living Inventory permanently limited to technical device records.

Reason: Operators need stable knowledge that survives DHCP changes and temporary absence. Separating discovered truth from operator knowledge preserves evidence integrity while allowing future criticality, expected availability, lifecycle, maintenance, retention, and incident policies to reflect the meaning of each asset.

Consequences: Stable identity and passive discovery remain foundational. Future asset metadata must not fabricate observations or be erased by rediscovery. Asset classification is required before aggressive archival, and important or explicitly monitored assets cannot be silently archived from stale age alone. Future incidents may consider asset criticality and expected availability only after those concepts are explicitly modeled and approved. The detailed roadmap remains owned by [docs/HIOC_MASTER_PLAN.md](docs/HIOC_MASTER_PLAN.md), and the conceptual model is described in [docs/ASSET_MODEL.md](docs/ASSET_MODEL.md).

## ADR-0013: Development Checkout and Production Runtime Have Separate Roles

Decision: HIOC formally distinguishes development, shared history, PI3 release execution, and the deployed runtime. Deliberate source changes are developed and validated in an authorized development checkout, then committed and pushed to GitHub as the shared project history. After an approved commit is pulled, `/home/jazofv1/hioc-release-source` is the authoritative clean source checkout for release execution on PI3, while `/home/jazofv1/hioc` is the deployed production runtime. Production updates use the supported release process or validated release packages. The production runtime is not the normal development working copy, and direct `git pull` operations inside it are not the standard upgrade method.

Status: Accepted.

Context: HIOC originally used `/home/jazofv1/hioc` as both a Git working copy and the production installation. As the project matured, that directory accumulated valid persistent configuration, runtime state, history, logs, backups, generated artifacts, and installer-managed file permissions. A separate clean checkout was introduced organically during deployment work after operational experience demonstrated the mismatch. The safer workflow became the de facto operating model and is now formally documented.

Alternatives: Continue using the production runtime as both the development checkout and deployed installation; erase or normalize legitimate runtime changes before every Git operation; rely exclusively on manually copied files; or maintain a separate clean source checkout and deploy through the release system.

Reason: A clean authoritative source checkout provides predictable Git state, reproducible releases, safer upgrades, clearer rollback boundaries, protection of persistent runtime data, and a clear separation between authored source and operational state.

Consequences: GitHub carries the approved shared history between development and PI3. `/home/jazofv1/hioc-release-source` is the authoritative source checkout for release execution on PI3, while `/home/jazofv1/hioc` is the deployed runtime. Runtime state must not be treated automatically as unexplained source drift, and source/runtime differences must be classified before cleanup. Direct `git pull` inside the production runtime is not the standard upgrade path. `release/upgrade.sh` or a validated release package is the supported deployment path. This ADR does not require removal of the production runtime's existing `.git` directory; its future disposition remains a separate evidence-driven governance decision. Repository and deployment hygiene work must preserve proven runtime state.

## ADR-0014: Use Core MQTT for Incident Publication

Date: 2026-07-22

Status: Accepted.

Context: Incident Review intentionally embeds operator-facing post-recovery analysis in bounded local incident history and exposes review data through the established retained MQTT contract. The incident engine still publishes each complete document by passing it as one `mosquitto_pub -m` process argument. Established production evidence shows that the current history payload exceeds the per-argument capacity and causes the supported upgrade to fail with `E2BIG`. Core already provides persistent socket-based MQTT publication, and the archived architecture review identifies the incident engine's separate subprocess publisher as technical debt, but repository evidence does not establish which architectural layer should change.

Established facts: Authoritative local incident state is written before MQTT publication; completed history contains embedded reviews; review-derived fields are externally visible; established retained topics and incident fields are compatibility contracts; the subprocess invocation is an internal mechanism; and no byte-size rationale exists for the 50-record configuration default or the Python engine's 100-record fallback.

Decision: Select Candidate C, the repository-native form of Candidate A. Preserve the current local incident storage model, embedded Incident Review model, retained MQTT topic names and semantics, and externally visible payload schema. Replace only the Incident Engine's local `mosquitto_pub -m` publication path with the existing Core `MqttClient`. Implementation must use that shared abstraction unless focused repository tests expose a blocking incompatibility; such a finding stops implementation and reopens this decision rather than authorizing an improvised transport.

Rationale: Candidate C removes the established payload from the process argument that causes `E2BIG`, preserves the documented history and operator-review model, preserves retained topics and fields, completes the Incident Engine's partial alignment with shared Core architecture, and addresses duplicated-publisher technical debt with the smallest consumer and migration surface. It requires no Home Assistant or dashboard contract change and introduces no new protocol. It solves the current process-argument failure and improves architectural consistency; it does not prove unlimited broker, consumer, or future payload capacity.

Contracts preserved: `history.json` and other authoritative incident files remain unchanged; Incident Review remains embedded; topic names, retained semantics, established fields, payload structures, history ordering, and Home Assistant visibility remain unchanged. Payload schema may change only if focused tests expose an undocumented inconsistency and a separate approved documentation update defines it. Local state remains authoritative and is written before MQTT publication. Historical data must not be silently discarded.

Internal implementation allowed to change: Only Incident Engine publication transport, its explicit connection lifecycle, redacted error propagation, and truthful process status are authorized. One Core connection is used per engine run and reused for the existing ordered publication cycle. Required publication failure stops the cycle, reports partial progress, and returns nonzero; no infinite or in-run retry is added.

Candidates considered: Candidate A is the transport-only architecture and Candidate C is its concrete repository implementation. Candidate B is deferred because normalization changes persistence and review semantics unnecessarily. Candidate D is rejected as the primary correction because record count is not a byte bound and reducing it loses visible history without fixing transport. Candidate E is deferred because a smaller projection changes the external payload and may affect consumers. Candidate F is deferred because segmentation or pagination creates a new public protocol. Deferred candidates are not permanently rejected.

Implementation constraints and compatibility: Do not change review content, retention defaults, topics, retained flags, JSON fields, Home Assistant entities, dashboards, or broker configuration. Publish original file strings without semantic transformation. Do not retain a parallel local Incident Engine publisher. Do not alter other legacy publishers. Core large-payload tests, exact topic/payload/retain tests, failure tests, full regression tests, and static checks are mandatory.

Validation and rollback: Repository validation must prove at least 200 KB packet support, unchanged payload semantics, explicit failure status, state preservation, and no Incident Engine `mosquitto_pub` path. Production validation must prove supported upgrade success, retained history availability, absence of `E2BIG`, unchanged consumers, and no data loss. Rollback uses the supported prior release or deliberate Git revert while preserving current incident state; reverting restores the known large-history `E2BIG` limitation and is not a permanent correction.

Unresolved future questions: An explicit MQTT byte-size policy, broker and consumer capacity, count versus byte retention, review immutability, summary duplication, historical occurrence semantics, alternate projections, chunking, other legacy publisher migrations, and broader Core resilience remain separate decisions.

The investigation and candidate comparison are recorded in [docs/INCIDENT_HISTORY_MQTT_ARCHITECTURE_DECISION_PREPARATION.md](docs/INCIDENT_HISTORY_MQTT_ARCHITECTURE_DECISION_PREPARATION.md). The binding implementation plan is [docs/INCIDENT_HISTORY_MQTT_TRANSPORT_IMPLEMENTATION_SPEC.md](docs/INCIDENT_HISTORY_MQTT_TRANSPORT_IMPLEMENTATION_SPEC.md). The authoritative checkpoint remains in [docs/HIOC_MASTER_PLAN.md](docs/HIOC_MASTER_PLAN.md). Implementation is authorized as the next checkpoint but has not occurred; production remains unresolved pending deployment validation.
