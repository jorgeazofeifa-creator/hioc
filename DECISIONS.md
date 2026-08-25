# HIOC Architecture Decisions

## Decision: Execute PE-4 Home Assistant consumption on PI3

HIOC is the consumer of Home Assistant data, so the PE-4 authenticated client
belongs to PI3 NUT&PIHOLE. PI5 HA remains only the remote API source at exact
`192.168.100.251:8123`. Execution-host identity (`nutandpihole`, `jazofv1`,
`192.168.100.252`) is independent from endpoint identity (`PI5_HA`,
`192.168.100.251:8123`). Previous PI5-local root/add-on assumptions are
superseded; their dependency-unavailable precheck remains historical evidence.

PI3 runtime/dependency preflight is credential-free, local, network-free, and
fail-closed. Route proof is separately authorized and limited to one no-payload
TCP connection to the exact endpoint. Dependencies must honor the existing
release-source/non-Git-runtime contract and should be isolated when proved
supportable. This decision authorizes no execution, installation, deployment,
credentials, or PE-4.0B.2a run.

## Decision: Enforce zero WebSocket redirects with a target-bound socket

The approved `websockets` dependency follows handshake redirects by default and
does not expose a per-call redirect-count argument. PE-4.0B.2a therefore opens
one bounded TCP socket to the exact governed target and supplies it through the
supported `sock` connection path. The dependency rejects every redirect when a
pre-existing socket is present, before following `Location`; this adds no
request and implements no WebSocket framing. Missing redirect-rejection API
capability fails before credential acquisition. This corrects the
**PE-4.0B.2A WEBSOCKETS REDIRECT-SUPPRESSION ENFORCEMENT DEFECT — CLIENT ACCEPTS
A DEPENDENCY API THAT MAY FOLLOW HANDSHAKE REDIRECTS WITHOUT AN EXPLICIT
ZERO-REDIRECT CONTROL** without authorizing runtime preparation or execution.

## Decision: Require dependency-enforced PE-4.0B.2a message bounds

The websocket-client path is removed because its complete-message `recv()`
could materialize more than 65,536 bytes before the client checked length.
PE-4.0B.2a now accepts only a compatible `websockets` implementation whose
connection receives `max_size=65536` together with explicit proxy and timeout
controls. Dependency absence or incompatible signatures stop before credential
acquisition; no unsafe fallback or custom RFC6455 implementation is permitted.

## Decision: Implement PE-4.0B.2a as a bounded repository client

The frozen proof is implemented by `tools/hioc-pe4-ha-auth-capability.py`.
Callers supply only the exact governed non-secret target tuple; endpoints,
sequence, bounds, and commands are internal constants. The client accepts only
a compatible `websockets` API with pre-materialization message bounding and
explicit proxy suppression. Dependency absence or incompatibility stops
before credential acquisition; package installation and a custom protocol
stack remain rejected. This implementation decision does not authorize PI5
access, deployment, credentials, execution, 2b, or association work.

## Decision: Freeze PE-4.0B.2a to REST then WebSocket authentication

Official Home Assistant documentation supports a fixed-message authenticated
`GET /api/` and the `/api/websocket` authentication handshake. PE-4.0B.2a will
perform exactly those two credential-bearing interactions and no WebSocket
command. It uses terminal-only sanitized output, `PI5_HA` logical provenance,
and a repository-controlled client. A custom WebSocket stack, dependency
installation, registries, states, redirects, retries, and fallback are rejected.
The public REST API exposes no required registries; source-level config/frontend
WebSocket registry commands remain a separately reviewed 2b concern.

## Decision: Split authenticated PE-4 discovery after preflight PASS

PE-4.0B.1 is COMPLETE / PASS. The governed target is PI5 in an
`HA_TERMINAL_ADDON` context on HA OS, using the exact proven endpoint
`http://192.168.100.251:8123`. The historical first attempt remains a failed
HA CLI parser-contract chronology; only the corrected operator procedure
produced PASS, and active repository code never contained that defect.

PE-4.0B.2 will use separate authorization and STOP boundaries: 2a proves
authentication and supported API capability; 2b may later perform sanitized
registry/schema discovery. A standalone repository-controlled Python process
with terminal `getpass` is the credential-injection choice. No dedicated
WebSocket client was detected, so preparation must prove an existing Python
library or technically review a standard-library implementation without
installing packages. REST registry sufficiency and registry commands are not
assumed. Neither 2a nor 2b is implemented or authorized by this decision.

## Decision: Govern PE-4 Home Assistant access before live discovery

PE-4.0A establishes a supported-interface-first, read-only, least-privilege
contract before any PI5 or live Home Assistant access. Supported authenticated
REST/WebSocket registry access is candidate-only pending deployed-interface
classification; `.storage`, databases, shell/add-on access, state collection,
and service or registry mutation are prohibited fallbacks. Sanitized discovery
is count/category/schema evidence, not household inventory. HIOC identity and
operator Asset authority remain protected. PE-4.0B and implementation remain
not started and require separate authorization.

## Decision: Record Action 10 and PE-3 completion

Action 10 is complete through administrative repository-only closure with
disposition `NOOP_ALREADY_ABSENT`; Actions 1–10 and PE-3 are complete. No PI3 or
PI5 action, staging recreation or deletion, production mutation, rollback, or
Action 10 Evidence Report was required. Action 9 PASS and its private Evidence
Report remain the final PE-3 production validation and evidence. Transport
staging remains absent and retransmission remains unnecessary. Phase 7A remains
active, and all future-roadmap checkpoints remain separate and preserved.

## Historical decision: Action 10 is an administrative no-op closure

Repository history proves PE-3 Action 10 originally existed only to delete the
two-file transport directory after final validation and to rewrite the former
combined production-evidence report. That design is superseded. Action 6
validated and durably published the immutable database/manifest, Action 7 made
the installed database authoritative through configuration, Action 8 removed
the post-install staging dependency, and production later confirmed transport
staging absent. Action 9 completed read-only validation and published its own
private result-last Evidence Report.

Action 10 is therefore **CASE C — ACTION 10 ADMINISTRATIVE NO-OP CLOSURE**. It
requires no PI3 access, read-only verification, deletion, reconstruction,
retransmission, new evidence directory, or consumption of Action 8/9 evidence.
Its disposition is `NOOP_ALREADY_ABSENT`; rollback has no meaning and remains
FALSE. The governance correction retires the stale deletion-required ledger,
Action 9 timing-write language, and required-threshold language while preserving
them in Git history. Action 10 remains **NOT COMPLETE** until this correction is
validated, committed, pushed to `main`, and followed by clean-tree verification.
Only then may a separate repository-only status checkpoint record Actions 1–10
and PE-3 complete. All future-roadmap work remains separate.

## Decision: Record governed PE-3 Action 9 production completion

The corrected governed Action 9 production validation completed with
`RESULT=PASS`, `ACTION9=COMPLETE`, and `ROLLBACK_RECOMMENDED=FALSE`. Its private
Evidence Report at `/tmp/hioc-pe3-action9-Bb6vGrmm` is preserved unchanged,
alongside the successful Action 8 evidence at
`/tmp/hioc-pe3-action8-eZxNGrKa`. Production validation was read only; no
production mutation or rollback occurred.

The valid observations remain `12.467231` seconds and `146744` KiB total peak
child RSS, with `MEASURED`, `UNVALIDATED`, and `INSUFFICIENT_BASELINE`
semantics. Both historical targets were exceeded but are not production
enforced, so the performance assessment passed without creating replacement
thresholds. Actions 1–9 are complete. Action 10 remains not started/not
prepared pending this completion checkpoint's commit and push followed by a
separate operator-safety/governance review. The future performance-baseline
checkpoint and every future-roadmap commitment remain preserved.

## Historical decision: Action 9 performance correction before completion

The first governed Action 9 attempt passed target, source, runtime, and Action 8
evidence identity, then failed in the combined Action 8 evidence-validation
stage. Read-only forensics proved the Action 8 result and protected-snapshot
schemas passed; only performance failed, with elapsed `12.467231` seconds and
maximum child RSS `146744` KiB. No Action 9 evidence directory or production
mutation occurred, and rollback remains FALSE.

This is **CASE D — BOTH CONTRACT AND MEASUREMENT DEFECTS**: unvalidated design
targets of four seconds and 48 MiB were promoted to a single-run hard production
gate, while total peak child RSS was compared with an incremental-RSS target.
Action 9 now validates result, performance syntax, performance assessment, and
protected snapshot independently. Valid measured performance is recorded as
`INSUFFICIENT_BASELINE`; historical target exceedance is contextual and cannot
control production acceptance. Future hard limits require a separate governed,
versioned, workload-specific benchmark. Action 9 remains attempted but not
complete, and Action 10 remains not started/not prepared.

## Decision: Action 9 is read-only validation with invocation-owned evidence

The historical Action 9 inline procedure is rejected for stale evidence
provenance, interactive strict mode, unavailable timing dependency, repeated
generation, and incomplete failure/evidence semantics. The corrected boundary
uses `tools/hioc-pe3-action9-validate.sh`, consumes the exact reviewed Action 8
PASS evidence only after strict path/type/ownership/mode/content validation, and
reuses its governed Python performance record rather than rerunning generation.

Action 9 independently validates current production artifacts and protected
state without modifying them. Only private invocation-owned Action 9 evidence is
written, with a bounded machine-readable Evidence Report and result-last marker.
Rollback is always advisory FALSE because no production mutation occurs. The
tool stops without Action 10, cleanup, deployment, staging, or retransmission.

## Decision: Record governed PE-3 Action 8 production completion before Action 9

The governed PI3 Action 8 execution at commit
`fa344828161e892523faa3da5d4cdf07d2e8e792` returned `ACTION8=COMPLETE`,
`RESULT=PASS`, and `ROLLBACK_RECOMMENDED=FALSE`. Its prerequisite source refresh
and corrected-validator deployment are current PASS checkpoints. Evidence at
`/tmp/hioc-pe3-action8-eZxNGrKa` is preserved without reuse or cleanup; no
rollback, transport-staging recreation, or dataset retransmission occurred.

Action 8 is complete and Action 9 remains not started. The permanent completion
rule requires this status and production evidence to be committed and pushed
before a separately governed Action 9 review or preparation begins. All future
roadmap commitments remain unchanged.

## Action 8 corrected-validator deployment boundary

Decision: `tools/hioc-pe3-action8-validator-deploy.sh` exclusively owns the
corrective publication of `pi4/bin/hioc-validate-manufacturer.py` from a clean,
exact-commit PI3 release-source checkout into the non-Git runtime. The reviewed
validator blob is an independent executable trust anchor in addition to the
operator-supplied governance commit. An intentional validator change therefore
requires explicit anchor review; unrelated commits do not silently redefine the
runtime executable.

An exact identical owner/group/mode/content target is a no-op without backup.
A differing but otherwise safe target receives one invocation-owned private
backup, then same-directory private temporary publication, exact `0700`
ownership/mode, identity validation, atomic replacement, and file/directory
fsync. Rollback is advisory and never automatic. Stable manufacturer outputs,
inventory, active configuration, and selected immutable database/manifest are
hashed with relevant metadata before and after and must remain identical.

Context: the broad supported release upgrade copies unrelated artifacts, invokes
the installer, manages schedules and permissions, and runs engines. It cannot
satisfy the bounded corrective checkpoint. The new tool cannot invoke that
upgrade, the installer, any engine, Action 8, Action 9, services, or schedules.

## Action 8 validator permission classes

Decision: manufacturer sidecar and status outputs remain private regular
non-symlink files at exact mode `0600`. Inventory supplied for semantic
comparison is a distinct input class: it may be readable by group/world but may
not be writable by either. Immutable manufacturer database files retain their
existing private contract.

Context: the third governed Action 8 attempt proved generation and artifact
identity, then the validator reported a generic permission error. Its reader had
accepted both generated artifacts and subsequently rejected inventory by
applying the private-artifact bitmask to it.

Consequences: validation remains read-only and fail-closed, exact manufacturer
privacy is not relaxed, and unsafe broader writes and symlinks remain rejected.
Production semantic PASS is unresolved; the rollback advisory is preserved and
no rollback was performed.

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

Decision: HIOC formally distinguishes development, shared history, PI3 release execution, and the deployed runtime. Deliberate source changes are developed and validated in an authorized development checkout, then committed and pushed to GitHub as the shared project history. After an approved commit is pulled, `/home/jazofv1/hioc-release-source` is the authoritative clean source checkout for release execution on PI3, while `/home/jazofv1/hioc` is a non-Git deployed production runtime. Production updates use the supported release process or validated release packages. Direct runtime Git workflows are unsupported by design.

Status: Accepted.

Context: HIOC originally used `/home/jazofv1/hioc` as both a Git working copy and the production installation. As the project matured, that directory accumulated valid persistent configuration, runtime state, history, logs, backups, generated artifacts, and installer-managed file permissions. A separate clean checkout was introduced organically during deployment work after operational experience demonstrated the mismatch. The safer workflow became the de facto operating model and is now formally documented.

Alternatives: Continue using the production runtime as both the development checkout and deployed installation; erase or normalize legitimate runtime changes before every Git operation; rely exclusively on manually copied files; or maintain a separate clean source checkout and deploy through the release system.

Reason: A clean authoritative source checkout provides predictable Git state, reproducible releases, safer upgrades, clearer rollback boundaries, protection of persistent runtime data, and a clear separation between authored source and operational state.

Consequences: GitHub carries approved shared history between development and PI3. `/home/jazofv1/hioc-release-source` owns Git-based release execution, while `/home/jazofv1/hioc` contains deployed application files and preserved operational data. Installation, deployment, upgrade backups, and rollback restoration must exclude runtime Git metadata. Runtime version identity comes from `VERSION.yaml` and release metadata. `release/upgrade.sh`, `release/rollback.sh`, or a validated release package provide supported deployment and recovery without using runtime Git history. Configuration, state, history, logs, backups, credentials, and other operational data remain protected.

Resolution, 2026-07-28: The Repository and Deployment Hygiene investigation confirmed that runtime `.git` was residue from the original clone-in-place installation model. No runtime engine, installation, validation, versioning, upgrade, rollback, or disaster-recovery capability depends on it. The production runtime is formally a non-Git deployment target. All Git operations belong to the authoritative Windows repository, GitHub, or `/home/jazofv1/hioc-release-source`. The earlier open disposition is resolved: runtime Git metadata must be retired during the current hygiene phase, and direct Git operations in `/home/jazofv1/hioc` are unsupported. This decision is final within the current architecture unless replaced by a future formally approved ADR.

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

The investigation and candidate comparison are recorded in [docs/INCIDENT_HISTORY_MQTT_ARCHITECTURE_DECISION_PREPARATION.md](docs/INCIDENT_HISTORY_MQTT_ARCHITECTURE_DECISION_PREPARATION.md). The binding implementation plan is [docs/INCIDENT_HISTORY_MQTT_TRANSPORT_IMPLEMENTATION_SPEC.md](docs/INCIDENT_HISTORY_MQTT_TRANSPORT_IMPLEMENTATION_SPEC.md). The authoritative checkpoint remains in [docs/HIOC_MASTER_PLAN.md](docs/HIOC_MASTER_PLAN.md). Repository implementation and production validation are complete. The supported upgrade and runtime validator passed with all seven required retained topics valid, a 230660-byte incident-history payload containing 27 records, and embedded review data present. This result closes only the approved transport correction; TLS, payload policy, other legacy publishers, broker resilience, and broader MQTT modernization remain unresolved future work.

## ADR-0015: Keep Pi-hole DHCP Within the Existing Passive Driver Contract

Date: 2026-07-28

Status: Accepted for the next bounded implementation checkpoint. Implementation has not started.

Context: Pi-hole DHCP lease ingestion already acquires and parses lease files in source-specific functions, returns source-tagged device mappings through `PassiveNetworkDriver` and `DriverResult`, and relies on centralized `merge_records()` logic for stable identity, source authority, weak-to-strong reconciliation, observation timestamps, health, and retained inventory. `DriverRegistry` validates the common result shape and supplies default provenance for driver records. Known infrastructure separately contributes operator metadata. HIOC has no family of independent identity providers and no asset-provider framework.

Decision: Select **Pi-hole-specific integration** through the existing passive-driver and device-record convention. Keep Pi-hole/dnsmasq acquisition, parsing, source status, and lease metadata in bounded DHCP adapter functions. Feed valid records into the existing `DriverResult.devices` and central reconciliation path with `source: dhcp_leases`, `_positive_observation: false`, source-file attribution, and lease metadata. Do not create an `IdentitySource` protocol, abstract base class, registration system, plugin framework, generalized provider API, or new canonical observation schema.

Rationale: The repository already has the smallest generic boundary it needs: a driver `discover(config)` call returning validated source-tagged device mappings. A second identity-source contract would duplicate collection and provenance responsibilities, introduce overlapping registration concepts, and encourage speculative providers before a second justified implementation exists. Keeping the source adapter Pi-hole-specific does not couple Pi-hole parsing to canonical reconciliation because the parser emits the established record convention and merge behavior remains centralized. Parser functions and immutable snapshots remain independently testable without network access.

Rejected alternative: A minimal generic `IdentitySource` boundary is rejected for this checkpoint. A protocol, base class, or new callable convention would add terminology and structure without replacing any missing architectural seam. Future evidence sources can first use the existing driver and record convention. If a later concrete source cannot fit it without source checks spreading through reconciliation, that checkpoint must return to architecture review with repository evidence rather than prebuilding a framework now.

Identity ownership: A valid normalized DHCP MAC may create or confirm a MAC-backed technical identity and may upgrade one unambiguous IP-only weak identity through existing reconciliation. It never replaces a conflicting MAC. DHCP IP and hostname are assignment and technical identity evidence with lower authority than stronger current local-host, gateway, ARP, or integration evidence. DHCP contributes neither operator `name` or future `friendly_name` nor vendor, so those operator-managed fields remain separate. The supported Pi-hole row has no lease-start value, so none is fabricated. Expiry and client ID remain lease metadata. DHCP presence or active assignment is not positive observation, reachability, health, degradation, or online/offline state, and never updates `last_seen`. Deterministic precedence rules are sufficient; no confidence score is added.

Conflict rules: Matching MAC records merge under central field authority. Weak IP-only promotion occurs only for one unambiguous weak and strong identity with no conflicting MAC. Strong passive hostname or IP values outrank DHCP values, while DHCP may fill a missing technical field. Operator naming is never supplied by DHCP. Multiple leases for one MAC use established deterministic ordering; different MACs sharing an IP remain separate. Malformed rows and rows without a usable MAC create no identity. Blank hostnames are accepted without fabrication. Expired leases never prove offline. Source unavailability creates no evidence and preserves prior inventory; successful empty collection reports empty rather than failure. Archived-asset behavior remains undefined until the retention and asset policies exist.

Provenance: Preserve the current record-level model: `source: dhcp_leases`, canonical `sources`, `dhcp_lease_source`, lease metadata, and discovery-source status. Field-level lineage, confidence scoring, and a general provenance subsystem are not required for this checkpoint.

Implementation boundary: The next checkpoint may change Pi-hole lease reading and parsing, conversion into the existing record convention, central reconciliation only where required to enforce the approved deterministic rules, focused parser and merge tests, applicable documentation, and production validation. It must preserve stable MAC-backed identity, ambiguity protection, assignment-only semantics, source attribution, current public JSON and MQTT contracts unless a proven incompatibility stops the checkpoint, and all unrelated behavior.

Non-goals: Home Assistant, mDNS, SSDP, MQTT, or other identity providers; Active Discovery; dynamic plugins; dependency injection; asynchronous source events; generalized asset management; retention or archive implementation; incident-history validation; dependency graphs; topology; backup and disaster recovery; unrelated collectors; and dashboard work are outside this decision.

Validation required: Focused tests must cover source parsing, malformed and empty inputs, multiple leases, deterministic ordering, matching strong identity, unambiguous weak promotion, conflicting MAC and IP reuse, hostname and operator-name precedence, blank hostname, source unavailability, expiry without liveness, no `last_seen` refresh, and source attribution. Full regression, release validation, supported deployment, production inventory validation, and documentation closeout remain required before the DHCP checkpoint can complete.


## ADR-0016: Govern the HIOC Network Probe in the Authoritative Repository

Date: 2026-07-29

Status: Accepted and production validated.

Decision: The checksum-verified production baseline for `hioc-network-probe.sh` is imported at `pi4-tools/scripts/hioc-network-probe.sh`. This repository path is authoritative for future changes, while the deployed path remains `/home/jazofv1/pi4-tools/scripts/hioc-network-probe.sh`. The runtime `toolkit.conf` remains untracked configuration and must never be committed with credentials.

Context: The production script had no enclosing Git repository. A first correction stopped rather than reconstruct undisclosed behavior from fragments. The operator then captured the complete script in `hioc-network-probe-source-intake-20260729-220644.tar.gz`; the archive and script hashes were verified before review.

Consequences: The repository copy becomes the approved source after review, commit, and push, but production remains unvalidated until controlled deployment and checksum comparison. Future changes must pass through Git and the deterministic deployment helper. Emergency production edits must be reconciled immediately through documented source intake. Only this script was captured; other `pi4-tools` components remain external or unmanaged pending complete checksum-verified intake. Direct unrecorded production editing is not an accepted workflow.

Validation closure: Approved commit
`e06539d9bece040d721b9912213559cc54f1610d` passed governed PI3 deployment,
artifact identity, controlled publication, inventory, and incident-recovery
validation. The earlier pending condition is satisfied; no rollback was needed.

## ADR-0017: Git Objects Own Deployment Artifact Identity

Date: 2026-07-30

Status: Accepted, implemented, and production validated.

Decision: For every Git-governed deployment artifact, authoritative bytes are
the raw blob stored at the exact approved commit and path. Artifact evidence
always binds full commit SHA, repository-relative path, Git blob ID, and
Git-derived SHA-256. Checksums from worktrees, editor buffers, temporary files,
pre-commit versions, or normalized text streams are non-authoritative.
Deployment procedures derive identity locally from Git objects and never trust
a manually supplied checksum.

Context: The Phase 7A report hashed a CRLF Windows checkout and published that
value for an LF Git blob. Git clean conversion made the checkout appear clean
and gave `git hash-object` the committed blob ID, but its raw bytes had a
different SHA-256. PI3 safely rejected the false value before deployment.

Alternatives: Store a checksum manifest in the same commit it identifies,
manually transcribe a post-commit hash, or trust a clean worktree. The first is
self-referential; the others permit stale or platform-specific bytes.

Consequences: `tools/git_artifact_manifest.py` dynamically derives deterministic
identity from an operator-specified exact commit, avoiding a tracked
self-reference. Deployment helpers must prove clean exact-commit checkout,
blob/source/target byte equality, syntax, tree mode, backup, ownership, and
deployed mode. Post-push evidence must be regenerated from exact `origin/main`
before repository PASS. Production remains pending until operator validation.

Production closure: operator evidence confirmed matching Git blob, worktree,
and deployed bytes; Phase A and Phase B passed; and overall production
validation passed. The historical pending condition above is satisfied.

Refinement: Deployment correctness and downstream incident recovery are
separate validation domains. Deterministic deployment failure is **FAIL** and
exits nonzero. Validated deployment with delayed or inconclusive bounded
incident convergence is **PARTIAL PASS** and exits successfully for separate
follow-up; it must not trigger rollback by itself. **PASS** requires evidence
from both domains. Git-object authority and the Endpoint Migration Audit
conclusion remain unchanged.

## ADR-0018: Select Canonical IPv4 by Explicit Operational Evidence

Date: 2026-07-30

Status: Accepted, implemented, and production validated.

Decision: For observations already reconciled to one MAC-backed identity,
select the representative canonical IPv4 through one deterministic evidence
comparator. The evidence order is local collector, gateway, explicitly
configured integration, `REACHABLE`, `PERMANENT`, active DHCP, `DELAY`,
`PROBE`, unknown fallback ARP, `STALE`, generic driver, expired DHCP, and other
weak evidence. Normal neighbor collection rejects `FAILED`, `INCOMPLETE`, and
other unusable observations; they have no preferred operational authority if
presented directly. Invalid, IPv6, unspecified, loopback, link-local,
multicast, reserved, and limited-broadcast values are ineligible.

Equal evidence uses infinite-lease preference, later finite expiry, later
available observation epoch, then numerically lowest IPv4. Missing timestamps
are zero. Selection is independent of input, dictionary, and set order.

Rationale: The former generic field-authority selector ranked all ARP evidence
above DHCP and broke equal ARP ties lexically. It could therefore choose a stale
old address over the active lease for the same MAC. The explicit comparator
corrects that defect while allowing stronger current neighbor or configured
evidence to outrank DHCP and preserving static devices.

Boundaries: Canonical address is one representative address, not complete
address history, liveness, health, retention, or archive state. DHCP assignment
does not refresh `last_seen` or force online status. MAC normalization,
identity grouping, ambiguity protection, source aggregation, public schemas,
incident severity, dashboards, and the separate atomic collector-interface
selector remain unchanged. The existing model has aggregate provenance but no
field-level candidate-address history; this decision does not create one.

Validation: Focused tests must prove DHCP-over-STALE behavior, order
independence, strong/static neighbor support, unusable and invalid candidate
handling, deterministic ties, identity and provenance preservation, and
liveness independence. Full regression and governed PI3 production validation
remain required before checkpoint closure.

Production-validation refinement: A direct ADR-0018 production candidate must
be active DHCP IPv4 versus a different same-MAC `STALE` neighbor IPv4 and must
have no higher-ranked local, gateway, configured integration, `REACHABLE`, or
`PERMANENT` evidence. `PASS` proves the qualifying DHCP address wins.
`NO_QUALIFYING_CANDIDATE` means no current direct reproduction exists and does
not recommend rollback. `FAIL` is reserved for a qualifying stale IPv4 that
still wins or an independent deployment/invariant failure. The first governed
run's IPv6 link-local candidate with higher-authority integration evidence was
a validator-selection defect, not a reason to change this decision.

Invariant input refinement: Production validation accepts exactly six required
Boolean invariants: artifact identity, unique MAC identity, inventory-count
consistency, health/liveness field presence, stable identity fields, and
bounded unrelated canonical changes. Each must be present and have JSON Boolean
type. Required `false` values fail; missing or non-Boolean required values and
unexpected non-underscore keys are input errors and also fail validation.
Underscore-prefixed keys are diagnostic metadata and never enter Boolean
evaluation. A diagnostic count of zero therefore preserves
`NO_QUALIFYING_CANDIDATE` and cannot recommend rollback.

Production closure: Corrected strict validation at source commit
`b3621c3765e56b9741565ac58be6a5fad4d0f302` retained the unchanged comparator
from `839e924b2249bec736ff74d9a2ac593c7fee6bb8`. Source and runtime matched
Git-derived SHA-256
`35f36916399331a6e1129f7a49ba86933960eca8e94d6b30c80e9be3d7cd75b8`.
All six required Boolean invariants passed; diagnostic counts were preserved;
inventory remained 151; one unrelated canonical-address change stayed within
the approved bound; and the final result was
`NO_QUALIFYING_CANDIDATE` with no rollback. The earlier unconditional-DHCP and
generic-truthiness failures were validator defects. The `.152` lease residue
and DHCP service-health work remain outside this completed decision.

## ADR-0019: Separate Observation, Enrichment, and Asset Information Layers

Date: 2026-08-03

Status: Accepted; PE-1 production validated; PE-2.0 design approved.

Decision: Permanently separate Observation (what a passive source saw),
Enrichment (what HIOC learned, normalized, correlated, or inferred), and Asset
(what the operator intentionally knows and manages). The layers reference one
another without destructive transformation and remain tied through stable
identity. Begin with a parallel local artifact containing observed hostname
evidence and enrichment candidates, selection, conflicts, categorical
authority, confidence, and provenance. Do not create Asset-friendly names or
project that first artifact into public inventory, MQTT, Home Assistant,
dashboards, or incidents.

Context: Current inventory preserves aggregate sources and deterministic
selected values but not the candidate, conflict, or provenance for each field.
`name` also combines operator intent with display fallback. Home Assistant and
MQTT are consumers/transport today, and no repository OUI enrichment exists.

Alternatives: Add nested provenance directly to every public device; create a
database before proving the model; allow every integration dictionary equal
authority; or start with operator and external-reference data simultaneously.

Reason: A local hostname-only envelope exercises real conflicting passive
sources with the smallest payload, privacy, identity, and consumer risk. It
creates the reusable contract needed for later operator-friendly names,
physical location, manufacturer, Home Assistant association, and explainable
classification.

Consequences: Identity, canonical address, liveness, health, monitoring,
incidents, and retention remain owned by their existing contracts. Operator
Asset metadata cannot be silently overwritten. Descriptive authority defaults
to Asset metadata, configured infrastructure facts, trusted Enrichment, strong
Observation, weak Observation, then historical fallback. This ordering never
bypasses identity, canonical-address, liveness, health, or incident algorithms.
Authority is field-specific;
confidence is categorical and never acts as identity or health evidence.
Public projection, OUI data, Home Assistant access, expected availability,
permanent-IoT monitoring, automation impact, and retention each require later
review. The full proposed contract is in
`docs/PASSIVE_ENRICHMENT_ARCHITECTURE.md`.

Cross-layer invariants: Observation is never rewritten to match interpretation;
Enrichment never claims to be direct evidence; Asset corrections persist;
expected availability is Asset intent; current availability begins with
Observation; staleness applies to evidence rather than Asset existence; and
missing enrichment or Asset metadata cannot independently create an incident
or health conclusion. Asset data is the most privacy-sensitive layer and is
deny-by-default for publication.

PE-1 approved contract: only existing explicit technical hostnames from known
infrastructure, configured integrations, the local collector, and active DHCP
leases are eligible. Configured/integration `name`, retained public hostname,
ARP, service names, reverse DNS, MQTT, Home Assistant, and legacy toolkit names
are excluded. Case, Unicode/IDNA equivalent, and trailing-dot forms agree;
`.lan`, `.local`, short names, and FQDNs are not collapsed. Invalid and
placeholder evidence may be retained but is nonselectable. Selection is
deterministic in descriptive order: configured fact, trusted integration,
local observation, DHCP observation, then one-generation historical fallback.

Storage and lifecycle: PE-1 uses closed version `1.0` local sidecars at
`state/inventory/enrichment.json` and `enrichment_status.json`, keyed by stable
device ID. It retains current candidates plus at most the immediately previous
selected candidate for one successful generation while the device remains in
resolved inventory. The existing inventory schedule and identity path remain
authoritative; enrichment is fail-open, never rereads sources, never becomes a
public payload, and cannot block valid inventory output. The full approved
implementation contract is
`docs/PE1_HOSTNAME_ENRICHMENT_SPEC.md`.

Repository implementation: PE-1 uses an isolated enrichment library and the
existing Inventory Engine schedule. Current-cycle records are bound only by
central resolved stable identity, passed privately, removed before public
serialization/events/MQTT, then normalized and written to validated local
sidecars. Enrichment failure is fail-open for authoritative inventory and
publication. Focused and full regressions prove the approved source,
normalization, selection, lifecycle, privacy, determinism, and protected
invariant contracts.

Production decision: PE-1 deployed from approved implementation commit
`29737ee97899bf06be09df661725c8186a7c339f`; Git-derived identity, supported
deployment/backups, authoritative schema validation, and corrected production
validation passed. The first aggregate validator duplicated the wrong
acquisition-oriented `source_type` allowlist. Validator-governance commit
`55186db4ad73131d47271b43dffe20fd53be4a09` corrected it by importing
`SOURCE_TYPES`, `AUTHORITIES`, and `CONFIDENCES` from the authoritative module.
The defect was not an implementation or production-invariant failure.
Production reported `online`, 153 records, 83 candidates, 82 selections, and
zero conflicts; missing optional source types, history, and conflicts were
acceptable. No rollback was recommended or performed. PE-1 is **COMPLETE -
PRODUCTION VALIDATED**. See
`docs/PE1_HOSTNAME_ENRICHMENT_EVIDENCE.md`.

PE-2.0 Asset decision: PE-2.1 will add a separate closed version `1.0` local
store at `state/inventory/assets.json`, with subsystem status at
`assets_status.json`. Records are keyed only by current-format stable HIOC
device ID and contain nullable operator-managed `friendly_name`,
`physical_location`, `purpose`, and private `notes`, plus system timestamps,
fixed update source, and revision. Owner is deferred because its human meaning
and privacy boundary are unresolved. Current public `name`, `display_name`,
`location`, `area`, `notes`, role, identity, canonical address, health,
liveness, topology, services, and consumers are not reinterpreted or changed.

A governed local CLI is the only PE-2.1 write path. It uses a dedicated bounded
lock, strict validation, optimistic revision checks, a validated backup before
every mutation, restrictive atomic replacement, redacted output, and explicit
restore. Orphans remain valid and editable without deletion, health, or incident
meaning. Asset metadata is local-only and deny-by-default for all publication.
Identity supersession creates an orphan; automatic Asset merge/split/migration
is prohibited until a later alias contract exists. Expected availability,
lifecycle, public presentation, HA/UI/API editing, and retention remain later
decisions. Full contract: `docs/PE2_ASSET_FOUNDATION_SPEC.md`. PE-2.0 is
**COMPLETE - DESIGN APPROVED**. The PE-2.1 implementation-design review is
**COMPLETE - IMPLEMENTATION DESIGN APPROVED** in
`docs/PE2_ASSET_IMPLEMENTATION_DESIGN.md`; PE-2.1 executable implementation is
**IMPLEMENTED - REPOSITORY VALIDATED**, with deployment and production validation
pending. The approved design selects isolated CLI/service/store modules,
no inventory import or schedule, strict Asset-local transactions, bounded flock,
closed schemas/errors, deny-by-default output, and release preservation.

PE-2.1 production-validator correction: the first supported deployment completed
and all approved runtime bytes matched Git. Its validator incorrectly conflated
Git tree modes with restrictive runtime permissions, then failed report writing
by interpolating lowercase JSON booleans into Python. Runtime modes are now owned
once by `pi4/config/pe2_artifacts.json` and consumed by installer/validator;
content identity and runtime permission/ownership failures are distinct. Report
serialization consumes JSON, and revalidation performs no deployment. The prior
generic rollback recommendation is withdrawn; corrected production revalidation
remains required before PE-2.1 closure.

## ADR-0018: Validate PE-2 incident isolation by positive contract

Status: Accepted

PE-2.1 validation does not treat live incident snapshots as immutable. It
validates JSON and protected shape, prohibits Asset fields and synthetic values,
proves the absence of an Asset incident write path, and classifies unrelated
lifecycle changes as operational drift. History and summary may advance normally.
Comparator uncertainty is non-rollback; rollback requires a deterministic,
causally demonstrated protected incident regression. The deployed Asset
implementation and existing incident engine behavior remain unchanged.

## ADR-0019: Exact cleanup for PE-2 synthetic validation backups

Status: Accepted

Synthetic validation backups are validation hygiene, not operator retention.
One-time cleanup requires a closed manifest of exact basenames and SHA-256 values
and complete validation of containment, type, ownership/mode, digest, JSON,
authoritative Asset schema, and synthetic-only content before deletion.
Wildcards, discovery deletion, timestamp ranges, and deletion of mixed or
unlisted backups are prohibited. Future validators clean only explicitly tracked
current-run synthetic-only backups immediately after final Asset equality and
before unrelated invariants. This corrects validator ordering without weakening
the Asset backup implementation or policy.

## PE-2.1 production-validation closure

PE-2.1 is **COMPLETE - PRODUCTION VALIDATED**. Implementation commit
`dd6f40b113fe8a395babc8bfb2325262879b8454` was deployed through the supported
release path and matched approved Git objects with restrictive permissions.
Final validation at governance commit
`6bb9e158f9d51d9e43b042950620e0c4aba03eb5` passed Asset transactions, cleanup,
final equality, privacy, performance, and all protected invariants. Incident
movement was operational drift with no PE-2 causal regression.

The Git-mode/runtime-mode mismatch, generated-Python Boolean serialization,
immutable-active-incident assumption, and late synthetic-backup cleanup were all
validator-governance defects. They did not establish an Asset implementation
defect; deployed Asset files remained unchanged during correction. Associated
rollback recommendations were withdrawn, and no rollback was executed. Phase 7A
remains in progress; PE-3 is not started.

## ADR-0020: Use pinned IEEE assignments for manufacturer reference enrichment

Status: Accepted; PE-3.0 architecture complete and PE-3.1 repository implemented

PE-3 manufacturer information is private descriptive Enrichment, never identity,
Asset intent, device classification or operational evidence. The future
authoritative upstream is a pinned checksum-verified snapshot of the IEEE
Registration Authority public MA-L, MA-M and MA-S/OUI-36 listings. IEEE is the
assignment authority; Wireshark is a GPL composite with its own collision
precedence, and Nmap data carries NPSL redistribution constraints.

Before any IEEE data is committed, packaged or deployed, PE-3.1 requires a
recorded redistribution-terms review and approval. Runtime network lookup and
automatic updates are prohibited. Lookup is longest-prefix, offline,
deterministic and fail-open for inventory; local-admin, multicast, private,
invalid and unknown addresses never receive fabricated manufacturers. Future
operator correction belongs to Asset and future classification remains separate.
The complete binding architecture is
`docs/PE3_MANUFACTURER_ENRICHMENT_SPEC.md`.

## ADR-0021: Freeze PE-3.1 as an injected normalized dataset and separate sidecar

Status: Superseded by ADR-0022 for executable details

Because IEEE redistribution permission is not established, raw and transformed
assignment data are prohibited from repository/release distribution by default.
The future offline builder consumes explicitly supplied, checksum-pinned files;
runtime consumes only a deterministic normalized database. If redistribution is
not approved, an authorized local build injects the identical artifact without
changing runtime logic.

The runtime artifact has a closed versioned schema, a canonical-records digest
distinct from the complete-file artifact checksum, and only normalized prefix,
length, assignment type, and organization fields. Lookup validates immutable
36-, 28-, and 24-bit maps in longest-prefix order. Local-admin/randomized and
multicast addresses cannot produce manufacturer claims, and explicit EUI-64 is
never converted by removing `FF:FE`.

Manufacturer output uses separate private `manufacturer.json` and status
sidecars rather than changing the production-validated hostname enrichment
schema. This isolates dataset licensing, refresh, failure and rollback from
PE-1 and PE-2. Reference evidence remains immutable provenance; a future
operator correction is separate Asset metadata. Missing or invalid reference
data fails open and cannot affect protected operational contracts.

ADR-0022 and `docs/PE3_MANUFACTURER_EXECUTABLE_CONTRACT.md` resolve the exact
schemas, paths, execution model, and test mapping. ADR-0021 remains historical
context for separation and offline injection, not an executable authority.

## ADR-0022: Freeze the PE-3.1 executable contract around a separate generator

Status: Accepted; executable implementation repository validated

PE-3.1 uses a separate manually invoked generator that reads completed inventory
and writes only private manufacturer sidecars. It never hooks the inventory
engine and has no schedule. This isolates dataset and generation failure from
identity, canonical address, PE-1, PE-2, and every public consumer.

Local acquisition and local transformation are the approved dataset model.
Source and normalized registry content cannot enter Git or releases. The offline
builder produces an immutable version directory containing the closed database
and manifest as one atomic transaction; configuration selects the local database.

The sidecar is a deterministic mapping keyed by stable device ID. EUI-48 uses
36/28/24 longest-prefix lookup; EUI-64 is validated/classified but makes no
manufacturer claim. Exact APIs, CLI flags, exit/error codes, schemas, paths,
locks, failure behavior, preservation, testing, production validation, and
rollback are binding in `docs/PE3_MANUFACTURER_EXECUTABLE_CONTRACT.md`. This
decision creates no executable, dataset, deployment, or production change.

Lock-order clarification: the dedicated manufacturer lock protects the complete
generation transaction. Database, adjacent manifest, and completed inventory
content are opened and validated only after lock acquisition; generation and
sidecar/status writes remain under that lock. This removes the validation-to-
generation time-of-check/time-of-use gap and serializes manufacturer generators
without acquiring the inventory, PE-1 enrichment, Asset, or another HIOC state
lock. The manufacturer lock does not prevent `inventory.json` replacement; the
generator uses the validated in-memory snapshot loaded under its lock. Any prior
implementation instruction requiring content validation before lock acquisition
is superseded only on this point. The executable contract contains the sole
normative order, and all other PE-3.1 decisions remain unchanged.

Error-mapping clarification: the frozen `(code, message)` exception interface
now accepts four explicit first-class causes: dataset conflict at exit 10,
deterministic-build mismatch at exit 11, sidecar validation at exit 15, and
status validation at exit 16. Builder owns the first two; validator and generator
own the latter two. Each prevents creating, accepting, or publishing its invalid
manufacturer artifact. These bounded manufacturer-subsystem failures leave
inventory and all protected systems unaffected and do not independently imply
production rollback. The executable contract remains the sole normative mapping;
all existing codes and exits, including unused 1 and 13, remain unchanged.

Validator-lock clarification: the standalone manufacturer validator is a
strictly read-only observer and acquires no lock. Published database safety comes
from complete atomic directory promotion and immutable version directories, not
reader/writer locking. Sidecar validation uses independently loaded file values
and reports any cross-generation mismatch without mutation, automatic retry, or
rollback inference. The builder-only exclusive build lock and generator-only
exclusive generation lock are the complete PE-3.1 manufacturer lock inventory;
there is no validator, shared, reader/writer, third, or version-directory lock.
This supersedes only the earlier shared-database-lock instruction. Generator
order, error mappings, and all other frozen contracts remain unchanged.

Repository implementation: PE-3.1 now implements the frozen library, offline
builder, lock-free validator, separate generator, schemas, corrected locks and
errors, installer/release preservation, exclusion governance, synthetic tests,
and evidence report. No IEEE data, production database, deployment, schedule,
public projection, or protected subsystem change occurred. Repository validation
does not complete PE-3; local production dataset creation, deployment, and
production validation remain separate pending gates, and PE-4 is not started.

Real-source compatibility amendment: organization normalization removes only
U+200B ZERO WIDTH SPACE and U+200E LEFT-TO-RIGHT MARK, converts U+0009 TAB to
collapsible whitespace, and continues to reject every other prohibited control
or format character. Official assignment keys with multiple distinct normalized
organizations do not select a winner. The database retains one closed conflict
entry containing only prefix metadata and variant count, never organization
variants. Conflict lookup is a first-class non-claim that blocks shorter-prefix
fallback and returns null manufacturer with unknown confidence. Exit 10 remains
reserved for structurally irreconcilable conflict metadata or nondeterministic
grouping, not representable official organization variation.

## ADR-0023: Gate PE-3 production deployment as ten reviewed operator actions

Status: Accepted design; not executed

PE-3 production deployment transfers only the validated normalized database and
manifest; raw IEEE CSVs remain on the operator workstation. PI3 first deploys
approved code through the supported release upgrade, then validates and
atomically promotes a same-filesystem private dataset staging directory to
`data/manufacturer/versions/local-ieee-ra--2026-08-11-r1`. Configuration is
backed up and activated only when absent/empty or already identical; a different
nonempty value stops without overwrite.

Windows verification, transfer, staging validation, repository synchronization,
code deployment, dataset installation, configuration, generation, production
validation, and transfer cleanup are separate actions with an evidence return
between each. Git-object content plus release policy governs deployed code;
implementation commit and operator-governance commit are separate identities.
Protected evidence uses semantic summaries and treats live incident movement as
operational drift requiring causal review. Evidence is aggregate-only. Code,
dataset, configuration, and sidecar rollback domains remain separate. The
authoritative commands and classifications are frozen in
`docs/PE3_MANUFACTURER_PRODUCTION_RUNBOOK.md`. This decision performs no
production action and does not start PE-4.

Historical Action 1 operator-discovery amendment, superseded by ADR-0024:
Windows verification resolved Python 3
without a user-specific path, in the strict order `py -3`, `python3`, then
`python`, and stops with `PYTHON3_NOT_FOUND` if no candidate executes as Python
3. The operator supplies only the external PE-3 workspace root; the procedure
accepts an adjacent database/manifest pair only when both frozen hashes and
sizes match. Multiple identical matches are selected deterministically only
after verification; zero matches stop with `VALIDATED_BUILD_PAIR_NOT_FOUND`.
Outputs remain sanitized and the action remains read-only and Windows-only.

Interactive-host amendment: Action 1 uses a single function-scoped PowerShell
execution path. Expected precondition and validation outcomes print sanitized `RESULT`
and `ERROR_CODE` values and return from the function; no branch invokes `exit`.
Unexpected exceptions are caught and rendered only as `VALIDATION_FAIL` /
`ACTION1_UNEXPECTED_ERROR`, without paths, stack traces, or data values. This
preserves the operator prompt for evidence capture and changes no artifact,
validation, transfer, or production contract.

Repository-executable amendment: two corrupted operator transcripts establish
an Action 1 delivery-path defect and are not Python, manufacturer-validator,
dataset, repository, or production evidence. Action 1 source is no longer
distributed through chat. Its sole canonical executable implementation is
`tools/hioc-pe3-action1.ps1`; the runbook freezes its SHA-256 and Git blob and
provides only a direct parameterized invocation from the synchronized
repository. The script verifies its own approved Git identity and clean state,
preserves the interactive host on every expected failure, and bounds unexpected
errors to `ACTION1_UNEXPECTED_ERROR` plus `FAILURE_STAGE`. No attempt reached PI3
or changed production.

## ADR-0024: Separate Python language floor, tested evidence, and operational support

Status: Accepted governance; Windows CPython 3.13.x support validated and promoted

HIOC adopts Model D. CPython 3.10 is the repository language floor because
production source uses PEP 604 union syntax. This is not a blanket support claim.
CPython 3.12.13 has complete-suite evidence. CPython 3.13.x is the supported
Windows operator line, with patch releases allowed to float; the governed
checkpoint passed on 3.13.15 and this approved repository change promotes
`governance/python-runtime-support.json`. Production continues
using distribution-managed CPython `python3`; its exact version is unverified
and must be independently validated. Other Python implementations are not
supported.

The operator workstation is controlled operational environment for prerequisite
identity and reproducibility, although it is not production infrastructure. A
resolved command or WindowsApps alias is not runtime evidence; actual execution,
implementation, and version probes are mandatory. Prerequisite failures remain
distinct from product failures.

The original chat-delivered Action 1 attempts remain delivery-path defects.
After repository-controlled execution eliminated that variable, the governed
script genuinely failed at `PYTHON_RESOLUTION`: `py` was absent, `python3` and
`python` were nonfunctional WindowsApps aliases returning 9009, and bounded
search found no real installation. This is `ACTION1_PREREQUISITE_MISSING —
PYTHON3`. Action 1 now selects only CPython 3.13, disables automatic Python
installation while probing, and cannot proceed until repository support state
is explicitly promoted. The next checkpoint is Windows Python 3.13 Installation
& Compatibility Validation, not PE-3 Action 1 or Action 2.

Validation-critical or production-capable multi-line operator programs remain
versioned in Git whenever practical; chat guidance invokes them rather than
reproducing their source. This decision installs nothing and performs no PI or
production action.

Windows checkpoint delivery amendment: the Python 3.13 installation and
compatibility procedure is substantial and therefore lives only in
`tools/hioc-python313-validate.ps1`. The script verifies its approved repository
identity and `validation_pending` support state, uses the official WinGet Python
Install Manager package, installs the governed 3.13 line explicitly, validates
CPython and exact major/minor by execution, runs the full/focused/manufacturer
and compilation checks, and reports sanitized evidence. It cannot promote the
support manifest, execute Action 1, or perform production work. Chat supplies
only the short invocation after the tooling commit is pushed.

Forensic checkpoint amendment: the first governed run stopped at
`PYTHON_INSTALLATION` because Windows PowerShell 5.1 promoted informational
manager stderr to `NativeCommandError` / `RemoteException` before the script
could evaluate the native exit code. All WinGet and Python-manager calls now use
one process helper that captures both streams and treats exit zero as success;
nonzero exit remains failure. Scripted management uses the unambiguous
`pymanager`; `py -3.13` is reserved for executing the explicitly installed
governed runtime. Automatic runtime installation is disabled before any
launcher invocation.

An informal `py --help` diagnostic installed default CPython 3.14.7 when no
managed runtime existed. This is `PYTHON_OPERATOR_DIAGNOSTIC_SIDE_EFFECT —
UNINTENDED_DEFAULT_RUNTIME_INSTALL`, not HIOC support promotion, 3.13
validation, PE-3 failure, or production failure. It remains present pending a
separate cleanup decision and neither satisfies nor blocks the 3.13 contract.
A documented manager dry run observed CPython 3.13.15, but patch policy remains
floating 3.13.x. Diagnostic commands must be assessed for side effects and use
documented non-mutating list, inspect, version, or dry-run forms.

Runtime-path forensic amendment: the corrected checkpoint passed explicit
installation and then stopped at `PYTHON_PROBE`. The probe, test runner, and
compilation still used direct native invocation, so the same PowerShell 5.1
stderr-promotion defect remained beyond manager calls. This is **PYTHON
CHECKPOINT NATIVE STDERR HANDLING DEFECT — RUNTIME INVOCATION PATH**, not
CPython incompatibility, HIOC/manufacturer test failure, version rejection, or
PE-3/production failure.

All checkpoint-native programs now use one governed process wrapper with
deterministic Windows argument quoting, bounded stream capture, and actual exit
status. The manager's filtered `--one` inventory is authoritative: an existing
3.13 is reused, absence permits one explicit install, and malformed or
non-authoritative multiple output fails closed. A 3.13 runtime may now exist,
but exact patch and compatibility are established only by a successful wrapped
probe and validation matrix. Support remains `validation_pending`; the script
does not promote itself.

Cross-platform full-regression amendment: the next governed run reached
`FULL_REGRESSION`, and a verbose CPython 3.13 execution ran 504 tests with only
three errors. Each error came from a Bash-dependent network-probe governance
test invoking an unresolved shell fallback on Windows and raising
`FileNotFoundError` / `WinError 2`. This is **CROSS-PLATFORM TEST PREREQUISITE
CONTRACT DEFECT — MISSING BASH REPORTED AS ERROR**, not Python incompatibility,
HIOC/manufacturer failure, or PE-3/production failure.

The accepted contract follows existing repository practice: only the three
Bash-executing tests skip explicitly with `Bash is required` when the tool is
unavailable; platform-neutral checks remain active. Where Bash is available,
all original assertions execute unchanged. The full suite continues to fail on
real errors and reports actual test/skip counts without pinning a skip total.

Checkpoint-result amendment: after the Bash prerequisite correction, another
governed execution reported `FULL_REGRESSION_FAILED`, but the immediate direct
governed CPython 3.13 run passed 506 tests with 13 skips and native exit code 0.
This is **CHECKPOINT FULL-REGRESSION RESULT-CLASSIFICATION DEFECT —
NON-AUTHORITATIVE SUMMARY PARSE USED AS ACCEPTANCE GATE**, not Python, test,
manufacturer, PE-3, or production failure. The wrapper had captured the correct
exit code, but stage logic also required a parsed `Ran` count; head-only bounded
capture could discard the trailing unittest summary and leave that count zero.

Test-stage acceptance is now determined exclusively by the authoritative native
exit code. Capture retains the tail for result-summary reporting, and parsed
test/skip counts are informational only. No count is pinned, and genuine
nonzero exits remain failures. Support stays `validation_pending` with no
validated patch until the corrected governed checkpoint passes and a separate
support-promotion commit is approved.

Further forensic amendment: the governed checkpoint still reported
`FULL_REGRESSION_FAILED` after the summary-gate correction. Direct CPython 3.13
then passed 508 tests with 13 skips and exit code 0, both normally and with the
checkpoint's temporary `PYTHONPYCACHEPREFIX`. This rules out runtime
compatibility, the underlying suite, expected-count logic, Bash handling,
legitimate PyYAML skips, pycache placement, and chat delivery. The remaining
meaningful difference is the Windows `ProcessStartInfo` wrapper path.

The exact same-launcher mechanism cannot be established in Codex because its
process cannot resolve the operator's `py` launcher. Governance therefore
requires one checked-in diagnostic execution after commit and push; no
speculative checkpoint alteration is authorized before that evidence. The
diagnostic compares direct and wrapper execution using the same executable,
arguments, environment, working directory, and regression workload, while
reporting only sanitized process metadata.

Durable rule: validation wrappers require production-grade tests. A wrapper
that disagrees with the native process is defective and cannot establish
product incompatibility. Diagnostic equivalence must cover executable, argv,
environment, working directory, and execution wrapper before attribution.

The governed operator diagnostic then established the exact launch-layer
divergence: direct `py -3.13` full regression exited 0 and produced a valid
516-test, 13-skip summary; `ProcessStartInfo` launched the resolved `py` App
Execution Alias, completed both redirected stream tasks, exited 1, and produced
no unittest summary. This is **WINDOWS APP EXECUTION ALIAS / PROCESSSTARTINFO
RUNTIME-LAUNCH DIVERGENCE**, not Python incompatibility or test failure. Raw
stderr remains undisclosed, and no signature enum is invented without evidence.

Model C is adopted. The manager's non-installing, machine-oriented
`pymanager list --one --format=exe --only-managed 3.13` output resolves the exact
governed interpreter, which the native wrapper invokes directly. Model A retains
the disproven alias; Model B retains a manager execution layer and its automatic-
install surface. Model C has fewer layers, excludes 3.14/default selection, and
preserves authoritative child exit status. Diagnostic execution and diagnosed
equivalence are separate result dimensions.

Final runtime-execution amendment: resolving the exact managed interpreter did
not make `ProcessStartInfo` reliable. The exact path validated, direct execution
passed, and direct execution with the checkpoint's pycache prefix passed 518
tests with 13 skips and exit code 0. Only `ProcessStartInfo` execution failed.
This is **WINDOWS PYTHON CHECKPOINT PROCESSSTARTINFO EXECUTION DEFECT**.

Model C selection remains, but all Python stages now invoke the exact interpreter
through PowerShell's native operator with narrowly scoped `Continue` error
handling, immediate `$LASTEXITCODE` capture, OS-temporary stream files, bounded
tail reads, restoration, and cleanup. `ProcessStartInfo` remains acceptable for
the separately validated Git, WinGet, and manager paths only. A wrapper that
repeatedly disagrees with the exact governed runtime must be removed rather than
continually patched.

Support-closure amendment: the corrected governed checkpoint passed on exact
CPython 3.13.15 at commit `6b622280a6f414d14ca3060da349423d92d664cb`:
full suite 520 with 13 skips, Python policy 10, Action 1 governance 13,
manufacturer 119, compilation PASS, and clean repository. Windows CPython
3.13.x is supported; 3.13.15 is validation evidence, not a permanent patch pin.

Action 1 now uses the same exact managed-interpreter contract and remains
read-only. The checkpoint is a one-time promotion validator and intentionally
refuses once support is `supported`; no revalidation mode is implied. CPython
3.14.7 remains an unsupported diagnostic side effect. A future independent
checkpoint must decide retain-versus-remove without affecting PE-3 deployment.

PE-3 production-sequencing amendment: Action 3 verifies only the transferred
PI3 staging pair. A clean but stale source checkout cannot prove an
implementation commit before the action assigned to fetch it. Action 4 therefore
owns the clean fast-forward and, after synchronization, the implementation and
validator identity checks, point-of-use staged hash/size revalidation, and
read-only database validation. Action 5 remains the first deployment action.

The original Action 3 stopped after all target and staging checks passed because
the implementation commit was absent locally. This is a sequencing precondition,
not artifact or repository corruption. Interactive production verification must
not enable unbounded shell-level `errexit`; function-scoped checks emit bounded
failure evidence and return control. Accepted staging evidence is retained unless
the staging state changes.

PE-3 staged-permission amendment: Model C is adopted. Action 4 owns bounded
pre-validator permission normalization because synchronized implementation
identity and staged artifact identity are both available there. Action 2 remains
transport-only and Action 3 remains read-only staging evidence. Database,
manifest, sidecar, and status files require `0600`; version directories require
`0700`.

Transport success and checksum identity do not imply permission safety. Type,
symlink status, ownership, size, digest, and mode are independent invariants.
Only exact authorized staging files with proven owner, size, and digest and no
unexpected siblings may be normalized, only from `0600` or the observed `0644`
to `0600`, followed by mode and digest revalidation. The stopped Action 4 may
resume at permission normalization after exact synchronized source state is
re-established; Action 5 remains the first deployment action.

PE-3 Action 4 resume completion amendment: the original resume block was
insufficient because its post-`chmod` barrier covered only mode and digest and
its validator acceptance relied on process success without independently
requiring PASS, privacy safety, and the frozen record count. The exact operation
is therefore moved to `tools/hioc-pe3-action4-resume-permissions.sh`. It owns
complete pre/post staging identity, changes only proven `0644` target files,
treats `0600` as an idempotent no-op, and emits separate sanitized barriers.
Substantial production operator logic must be repository controlled; chat may
deliver only the short invocation. Action 4 remains stopped and Action 5 is not
started.

PE-3 Action 4 target-availability amendment: repository-controlled operator
scripts cannot be invoked merely because the governance repository contains
them. The target release-source checkout must first be clean, free of active Git
operations, fast-forwardable, synchronized to the exact governance commit, and
must prove the script's commit blob and worktree identity. PI3 remained at
`653f887a643c877a8f611145c8b8e9f92a65b6cd`, so the first resume invocation
made no production mutation but could not find the later script. A small inline
synchronization prerequisite is necessary because a wrapper stored only in the
newer target commit would have the same bootstrap problem.

PE-3 Action 4 execution-boundary amendment: repository synchronization, script
availability proof, and mutating script execution are distinct trust boundaries.
Action 4A is the bootstrap-safe synchronization and identity proof and must stop
after PASS. Action 4B is the separately authorized repository-controlled
permission-normalization and validator resume. No command may auto-chain 4A to
4B. Final `ACTION4=COMPLETE` is emitted only by 4B after reviewed 4A PASS;
Action 5 remains the first deployment action.

## Decision: PE-3 Action 5 is a repository-controlled deployment transaction

**Date:** 2026-08-12
**Status:** Accepted before Action 5 execution

The former Action 5 runbook block was rejected before production use because it
enabled interactive `set -euo pipefail`, piped deployment through `tee`, relied
on bare assertions, retained an unresolved governance-commit placeholder, and
lacked bounded evidence. This is classified as **PE-3 ACTION 5 OPERATOR-SAFETY
CONTRACT DEFECT — INTERACTIVE ERREXIT / PIPEFAIL AND INCOMPLETE EVIDENCE**, not a
deployment failure.

Action 5 is now implemented by `tools/hioc-pe3-action5-deploy.sh`. The exact
approved post-push commit is an operator input and gates source and script
identity. Release validation must pass before mutation; deployment uses only
`release/upgrade.sh`; backup, runtime validation, deployed Git-derived artifact
identity, and unchanged dataset/configuration fingerprints are explicit
barriers. Pre-mutation failures recommend no rollback. Failures during or after
runtime mutation recommend rollback when a usable new backup exists; rollback
is reported, never automatic. Action 6 remains separately authorized.

## Decision: PE-3 Action 5 synchronization and execution are separate gates

**Date:** 2026-08-12
**Status:** Accepted before Action 5 execution

PI3 was last governed at the Action 4 commit, before the Action 5 deployment
script existed. Invoking that unavailable script would repeat the previously
observed bootstrap defect. This is classified as **PE-3 ACTION 5 BOOTSTRAP
PREREQUISITE DEFECT — TARGET RELEASE-SOURCE MAY PREDATE DEPLOYMENT SCRIPT**.

Action 5A is an inline, bootstrap-safe, non-deployment procedure that proves the
PI3 target, clean fast-forward ancestry, exact approved synchronized commit, and
the Action 5 script's regular/non-symlink Git and worktree identity. It then
stops. Action 5B requires reviewed Action 5A PASS and separate authorization;
only Action 5B may deploy or emit `ACTION5=COMPLETE`. This pattern is mandatory
whenever a target may predate a repository-controlled production script.

## Decision: Action 5 protects payload semantics, not empty scaffolding identity

**Date:** 2026-08-12
**Status:** Accepted after Action 5B forensic review

The first Action 5B deployment passed release backup, code deployment, and
runtime validation, then the raw recursive fingerprint reported
`MANUFACTURER_DATASET_CHANGED`. Read-only evidence proved only installer-managed
empty, owned, private manufacturer directories existed. No payload or
configuration activation occurred. The authoritative classification is
**ACTION 5 PROTECTION SNAPSHOT FALSE POSITIVE — RELEASE-MANAGED EMPTY
MANUFACTURER SCAFFOLDING**. Rollback is not recommended because it reruns the
same installer logic.

Action 5 permits only creation or `0700` normalization of real, correctly owned
empty scaffold directories. It continues to fail closed on any version,
database, manifest, sidecar, status, symlink, unexpected entry, payload identity,
or configuration change. A separately bootstrapped, read-only Action 5C closes
the deployed runtime; deployment is not repeated and Action 6 remains a
separate authorization.

Action 5C bootstrap amendment: the new revalidation script may not yet exist on
the target. This is classified as **PE-3 ACTION 5C BOOTSTRAP CONTRACT MISSING —
TARGET MAY PREDATE REVALIDATION SCRIPT**, a governance/runbook deficiency and
not a production failure. Action 5C-A is the inline, bootstrap-safe target
synchronization and exact script Git/worktree identity gate and must stop after
PASS. Action 5C-B is the separately authorized read-only revalidation and
closure. No command may auto-chain them. Every newly introduced repository-
controlled operator script requires this synchronization/identity boundary when
the target may predate it, including scripts whose eventual operation is
read-only.

Action 6 operator-safety amendment: the historical inline immutable-install
block is rejected as **PE-3 ACTION 6 OPERATOR-SAFETY AND EVIDENCE CONTRACT
DEFECT — IMMUTABLE DATASET INSTALLATION PROCEDURE NOT PRODUCTION-SAFE**. Action
6 had not executed, so this is not a production failure. Substantial mutating
installation logic now belongs to `tools/hioc-pe3-action6-install.sh`. Action
6-A separately synchronizes the target and proves script identity; reviewed
PASS and separate authorization are mandatory before Action 6-B. Publication
uses an invocation-owned hidden same-filesystem directory, complete revalidation
and fsync, and no-replace atomic rename. Identical existing content is accepted;
any differing invariant fails closed. Configuration activation remains Action
7, which cannot be prepared or executed without reviewed full Action 6 PASS.

## ADR-0025: Separate infrastructure availability from application and service assurance

**Date:** 2026-08-22
**Status:** Accepted roadmap architecture; PE-10 planned / not started

HIOC adopts a separate future **PE-10 - Application, Integration & Service
Assurance** phase after PE-8 functional-impact correlation and PE-9 technical
dependency intelligence. A reachable host, available Home Assistant entity, or
successful recovery API call is not sufficient evidence that an operator-visible
function is usable or recovered.

PE-10 will correlate layered device, network, cloud/vendor, integration, entity,
freshness, corroboration, automation, protocol/service, and functional evidence.
It will use the existing Asset, dependency, topology, incident-propagation, and
impact models rather than replace them. PE-7 remains the owner of expected-online
intent; PE-10 owns capability/service usability across a dependency chain.

Any future automated remediation must be evidence-based, bounded, backoff-
controlled, loop-safe, recorded, operator-policy controlled, and followed by
functional validation. Risky actions may require manual approval. Synthetic
service checks, including Google Cast checks, must be harmless and non-disruptive.

Infrastructure backup/DR/hardware migration and PI3 + PI5 Abrupt Power-Loss /
Cold-Boot Recovery Validation remain separate checkpoints: the former protects
restoration and migration, the latter proves uncontrolled-interruption recovery,
and neither establishes steady-state application/service assurance.

## Decision: PE-3 Action 7 is a separately bootstrapped configuration transaction

**Date:** 2026-08-22
**Status:** Accepted before Action 7 execution; Action 7 not started

The historical inline Action 7 procedure is rejected as **PE-3 ACTION 7
OPERATOR-SAFETY AND EVIDENCE CONTRACT DEFECT — CONFIGURATION ACTIVATION
PROCEDURE NOT PRODUCTION-SAFE**. It used interactive `set -euo pipefail` and
shell-level exits, depended on an unresolved evidence-directory placeholder,
embedded meaningful mutation inline, and lacked closed source, runtime,
immutable-dataset, backup, post-publication, and rollback evidence. No Action 7
or production mutation occurred.

Action 7-A is a bootstrap-safe clean synchronization and exact script-identity
gate and must stop after PASS. Separately authorized Action 7-B is owned by
`tools/hioc-pe3-action7-activate.sh`. It may change only
`MANUFACTURER_DB_PATH`, from absent/empty to the exact installed immutable
`local-ieee-ra--2026-08-11-r1` database. The intended value at mode `0600` is
idempotent; a safe owner-matched selected file at a broader read-only mode is
backed up and normalized. Duplicates and different nonempty values fail closed.
A required change receives
a private durable exact backup and same-directory atomic publication. The
immutable dataset, transport staging, sidecar/status, services, schedules, and
all unrelated configuration remain untouched. Rollback is reported, never
automatic, and is recommended only after publication if durability or
post-publication validation fails. Action 8 remains separately authorized.

## Decision: PE-3 Action 8 is a governed protected-generation transaction

**Date:** 2026-08-22
**Status:** Accepted before Action 8 execution; Action 8 not started

The historical Action 8 inline procedure is rejected as **PE-3 ACTION 8
OPERATOR-SAFETY AND EVIDENCE CONTRACT DEFECT — MANUFACTURER GENERATION
PROCEDURE NOT PRODUCTION-SAFE**. Interactive strict mode, a `tee` pipeline under
pipefail, an unresolved evidence path, bare assertions, and incomplete identity,
protected-state, publication, failure, and rollback evidence made it unsuitable
for production. No Action 8 mutation occurred.

Action 8 is owned by `tools/hioc-pe3-action8-generate.sh`, which coordinates the
existing manual generator without changing its lock, atomic-write, no-op, or
failure contracts. The wrapper proves target/source/runtime, activated
configuration, exact installed dataset, inventory, output preconditions, and
evidence state; validates the resulting private sidecar/status and
protected domains; and publishes aggregate private evidence. It cannot deploy,
reload, reschedule, clean staging, or chain Action 9. Since PI3 predates the new
wrapper, a future separately authorized bootstrap synchronization/identity gate
is mandatory after commit/push and is intentionally not invented here.

## Decision: PE-3 Action 8 bootstrap is a separate source-only trust boundary

**Date:** 2026-08-22
**Status:** Prepared; not executed

The missing bootstrap contract is classified as **PE-3 ACTION 8 BOOTSTRAP
CONTRACT MISSING — TARGET RELEASE SOURCE PREDATES GOVERNED GENERATION SCRIPT**.
The correction freezes a parent-shell-safe inline gate that verifies PI3,
requires a clean `main` release-source checkout without an active Git operation,
fetches and fast-forwards only to governance commit
`8d65af39c6f41a7dcd003371378ace41fab270cd`, and proves the Action 8 script's
committed and worktree Git blob
`91360c1f83c890dd340a9a6390bf462cb0f95731`. It then stops. Runtime,
configuration, dataset, inventory, manufacturer artifacts, Action 8 evidence,
transport staging, services, and Action 9 are outside this bootstrap boundary.

## Decision: Action 8 bootstrap governance identity is supplied after publication

**Date:** 2026-08-22
**Status:** Corrected before bootstrap execution

The first Action 8 bootstrap correction froze its parent commit before the
governance correction itself could exist. This is classified as **PE-3 ACTION 8
BOOTSTRAP GOVERNANCE-COMMIT SELF-STALE CONTRACT DEFECT**, a repository defect
and not a production failure. A literal replacement would become stale again.

The bootstrap therefore accepts one explicit operator-approved lowercase full
40-hex governance commit after commit/push. Format validation precedes target,
fetch, and merge work; the value is never inferred from a branch, tag, symbolic
ref, or remote. Exact `origin/main`, ancestry, fast-forward-only synchronization,
post-sync HEAD, cleanliness, and the frozen Action 8 script Git/worktree blob
remain mandatory. The bootstrap still stops without runtime, staging, evidence,
generation, rollback, or Action 9 work.

## Decision: Action 8 owns its temporary evidence directory

**Date:** 2026-08-22
**Status:** Corrected before Action 8 execution

The operator-supplied `/tmp/hioc-pe3-production-validation-*` input is rejected
as **PE-3 ACTION 8 EVIDENCE-DIRECTORY PROVENANCE AND DURABILITY CONTRACT DEFECT
— EPHEMERAL PATH IS NOT DURABLY IDENTIFIABLE**. Neither Action 5B nor Action 5C
creates that prefix, and Action 8 consumes none of their evidence. Name, owner,
mode, and absent output files could not establish historical provenance.

Action 8 now accepts only the exact governance commit. After every read-only
identity and output precondition passes, it creates one unique private
invocation-owned `/tmp/hioc-pe3-action8-XXXXXXXX` directory, writes only
sanitized protected-state, aggregate result, and performance evidence, publishes
the result last, and reports the exact path. The path is temporary operator
evidence for reviewed Action 8 and later separate validation; loss blocks later
authorization and never permits reconstruction or substitution. The script blob
change requires a new post-push bootstrap identity gate before Action 8.

## Decision: Action 8 does not depend on post-install transport staging

**Date:** 2026-08-22
**Status:** Corrected after pre-generation staging-loss stop; Action 8 incomplete

The stopped Action 8 attempt proved target, source, runtime, configuration,
installed immutable dataset, dataset validation, and inventory, then reported
`TRANSPORT_STAGING_INVALID` before generation because the historical `/tmp`
transfer directory was absent. This is classified as **PE-3 ACTION 8
TRANSPORT-STAGING LIFETIME CONTRACT DEFECT — EPHEMERAL TRANSFER STATE
INCORRECTLY REQUIRED AFTER IMMUTABLE INSTALLATION**. It is not dataset loss, an
Action 6 or Action 7 failure, or a manufacturer-generation failure.

Action 6 consumes, validates, and atomically publishes the transferred pair.
Action 7 selects that installed immutable database. Action 8 reads only the
installed pair through the active configuration and already freezes its type,
owner, mode, size, hashes, validation result, privacy result, and record count.
The former staging fingerprint added no provenance, security, privacy, or
rollback authority. Action 8 now accepts staging absence and neither reads,
recreates, retransmits, nor cleans it. Cleanup belongs after reviewed Action 6
publication as a separate authorization; an already absent directory needs no
cleanup action. The stopped attempt caused no generation mutation and recommends
no rollback. The changed wrapper requires a new post-push bootstrap identity gate
before any separately authorized Action 8 retry.

## Decision: Action 8 retains sanitized generator-failure evidence

**Date:** 2026-08-22
**Status:** Corrected after failed-generation forensics; Action 8 incomplete

The Action 8 attempt at governance commit
`e59b74a2a5c8b8cad05589198609fd616044a434` reached protected pre-state and then
returned `MANUFACTURER_GENERATOR_FAILED`. The wrapper captured the generator's
bounded JSON stdout privately but deleted it during failure cleanup, discarded
stderr, and did not publish performance. The generator produced no status file.
Forensics found only the valid protected pre-state snapshot, so the underlying
production root cause cannot be recovered. This is **PE-3 ACTION 8 GENERATOR
FAILURE DIAGNOSTIC RETENTION DEFECT — WRAPPER COLLAPSES GENERATOR FAILURE
WITHOUT DURABLE SANITIZED ROOT-CAUSE EVIDENCE**.

Action 8 now privately captures stdout/stderr, parses only the allowlisted JSON
failure code, records numeric exit status and stderr presence without raw
content, compares strict pre/post sidecar and status identities, and publishes
performance before result-last `generation-failure.json`. Raw captures are
removed. Status-only safe failure publication does not recommend rollback;
sidecar mutation, unsafe output state, leftover temporaries, or evidence/cleanup
uncertainty does. Rollback remains manual. No production action, rerun, Action 9
preparation, staging reconstruction, or rollback is authorized by this decision.
The wrapper blob change requires a new post-push bootstrap gate.

## Decision: Action 8 bootstrap retains an independent frozen wrapper identity

**Date:** 2026-08-22
**Status:** Corrected before replacement-bootstrap preparation or execution

Replacement-bootstrap preparation stopped because the active runbook still
froze the superseded Action 8 wrapper blob. This is **PE-3 ACTION 8 BOOTSTRAP
SCRIPT-IDENTITY GOVERNANCE DEFECT — GOVERNED TRUST GATE REFERENCES SUPERSEDED
WRAPPER BLOB**. Historical records of earlier wrapper identities remain valid
historical evidence and are not rewritten.

The governance commit remains an operator-supplied full lowercase 40-hex value
because a tracked procedure cannot know its own future commit. The wrapper blob
remains a separate frozen literal because it is the independently reviewed
executable trust anchor, not merely whatever object happens to exist at the
approved commit. The active gate now freezes blob
`482f83584a62be2f02b2a73af4e78b0f4ebf447a`. No bootstrap, generation,
production, transport-staging, rollback, or Action 9 action occurred.

## Decision: Action 8 performance evidence uses governed Python

**Date:** 2026-08-22
**Status:** Corrected after retained exit-127 production evidence

The second Action 8 attempt retained private sanitized evidence proving no
manufacturer output mutation and exit `127`, while PI3 lacked the wrapper's
hard-coded `/usr/bin/time`. The generator was not proven to have started. This
is **PE-3 ACTION 8 PERFORMANCE-INSTRUMENTATION PORTABILITY DEFECT — OPTIONAL
/usr/bin/time DEPENDENCY BLOCKS GOVERNED MANUFACTURER GENERATION**.

Performance evidence remains mandatory, but the already-required governed
Python runtime now owns child creation, monotonic elapsed time, and child maximum
RSS. A private marker records only confirmed child creation; failure evidence
uses bounded `CONFIRMED` or `UNCONFIRMED` launch status and never raw diagnostics.
The changed wrapper invalidates the current bootstrap identity and requires a
new post-push trust gate. No rollback, staging, retransmission, or Action 9 work
is authorized.
# Decision: Use a hash-locked isolated PI3 runtime for PE-4.0B.2a

PE-4.0B.2a adopts CASE A: a release-managed, versioned virtual environment
under `/home/jazofv1/hioc/runtime/pe4`, activated through a strictly managed
atomic pointer. PI3's distribution CPython 3.11.2 satisfies the existing HIOC
CPython 3.10 language-floor policy and is not replaced. The sole dependency is
the exact official CPython 3.11 AArch64 `websockets==16.1.1` wheel frozen in
`requirements-pe4.lock`; installation is offline, hash-required, binary-only,
and has no transitive dependencies. The client and isolated environment are one
compatibility unit. This decision is governance only and authorizes no host,
credential, installation, deployment, or client access.

# Decision: Separate the PE-4 isolated-runtime lifecycle into A-G tools

Artifact acquisition, transfer, credential-free route proof, private
construction, dependency validation, publication, and final preflight remain
separate authorization and STOP boundaries. Shared safety primitives are
repository-controlled, while each action has its own executable. `runtime/pe4`
is externalized from general release backup/rollback and recovered from the
frozen artifact cache plus retained immutable environments. Dedicated rollback
changes only the validated active pointer. Implementation alone authorizes no
network or production action.

# Decision: Make Action A evidence and acquisition native to Windows

Action A uses the Windows Local Application Data Known Folder as its trusted
boundary, rejects reparse traversal below it, and protects cache, staging, and
evidence with a current-user-only protected DACL. It uses a direct exact-host
HTTPS connection with a monotonic total deadline and bounded reads. Result-last
publication flushes and atomically replaces the evidence file without claiming
POSIX directory-fsync semantics. Explicit acquisition, verification, durable
cache, reuse, and evidence states prevent ambiguous partial success.

Production ACL correction: Action A must not depend on
`Microsoft.PowerShell.Security` cmdlet autoloading or pass path values as
trailing `powershell.exe -Command` tokens. The Windows ACL authority is the
existing `DirectorySecurity`/`FileSecurity` descriptor obtained through
`DirectoryInfo`/`FileInfo`. The implementation disables inheritance without
preserving inherited ACEs, removes every remaining explicit Allow or Deny ACE,
adds one current-user SID FullControl rule with exact file/directory flags,
persists the modified descriptor, and rereads it for fail-closed validation.
An existing non-reparse `HIOC` directory left by the failed attempt is hardened
in place; manual deletion or ACL repair is prohibited.

# Decision: Make Action B transfer input and partial state deterministic

Action B derives the frozen wheel only from the governed durable Windows cache;
it accepts no path and does not rely on Action A evidence. It uses only Windows
system OpenSSH, numeric PI3 identity, strict public-key-only batch authentication,
and bounded output. Wheel and lock are separately transferred and verified in
one private PI3 directory. Sanitized result-last evidence records partial state,
and the directory is preserved and reported rather than automatically cleaned.

# Decision: Isolate Action B from ambient OpenSSH configuration

Action B treats ambient user/system SSH configuration and agent identities as
untrusted. It reads no SSH config, pins numeric PI3 and port 22, disables
hostname canonicalization, proxies, jump hosts, forwarding, and local commands,
and explicitly uses only the current Windows Known Folder profile's real,
non-reparse `.ssh/known_hosts` and `.ssh/id_ed25519`. Evidence publication is a
three-step prepare, atomic rename, and exact digest/durability confirmation; a
rename error is reconciled only by successful confirmation of the exact file.

# Decision: Govern the dedicated Action B Windows identity lifecycle

Read-only discovery found no existing private key suitable for Action B. The
fixed `.ssh/id_ed25519` pair is therefore created only through a separate
repository-controlled Windows prerequisite, never an ad hoc command. The tool
pins system `ssh-keygen.exe`, Ed25519, an empty passphrase required by Action B's
agent-free batch contract, and comment `hioc-pe4-action-b-windows`. It rejects
collisions and reparse traversal, generates under protected invocation staging,
validates DACL and pair identity, publishes the public key first and private key
last, and records only a sanitized fingerprint in result-last evidence. It
never installs the public key on PI3 or chains Action B. Partial publication is
preserved for separately authorized reconciliation, never automatically erased.

# Decision: Confirm SSH identity evidence only after final cleanup state

The first published provisioning lifecycle could write failure evidence before
staging cleanup, could leave a renamed result semantically stronger than its
confirmed ACL/readback state, and could lose a newly created child path when
initial ACL hardening failed. Invocation ownership is now recorded immediately
after directory creation. Failure cleanup reaches its final bounded state before
the payload is constructed. Evidence is prepared with its final state, flushed,
ACL-validated, atomically renamed once, and accepted only after exact bytes,
digest, file type, reparse, and DACL reread confirmation. Rename uncertainty is
reconciled by that same confirmation; wrong or ambiguous results remain
unaccepted and are never overwritten by a contradictory result.

# Decision: Treat every Windows path entry as a collision and retain id_ed25519

Execution preparation found that `Path.exists()` plus `Path.is_symlink()` did
not prove true absence of a dangling junction or another non-symlink reparse
entry. Provisioning now uses non-following `lstat` semantics: only a
`FileNotFoundError` is absence, every observed or indeterminate entry is a
collision. Key and evidence publication use Windows `MoveFileExW` with
write-through and without replacement, so the publication operation itself
cannot overwrite an entry raced into place after inspection.

History also confirms that `.ssh/id_ed25519` and `.ssh/id_ed25519.pub` were
explicitly frozen as the dedicated PE-4 Action B identity when ambient OpenSSH
configuration was isolated. The provisioning tool intentionally consumes that
same shared repository constant; the later `hioc_pe4_pi3_ed25519` description
was preparation-report drift, not an implementation decision. The generic name
does not authorize personal-key reuse: discovery proved both paths absent, the
pair may be created only by this PE-4 prerequisite, and Action B accepts exactly
that governed output. Provisioning and Action B remain blocked and unexecuted.

# Decision: Require evidence-source consumption before rename reconciliation

The first no-replace evidence correction could accept a raced exact
`result.json` after publication failed because it confirmed only the final file,
not whether its own `.result.tmp` was consumed. Evidence reconciliation now
requires both complete final content/type/reparse/DACL confirmation and true
non-following absence of the prepared temporary source. A retained file,
dangling link, junction, reparse entry, or indeterminate temporary path fails
closed. Normal publication applies the same source-consumption invariant. No
collision result is overwritten and no second result is attempted. Provisioning
and Action B remain blocked and unexecuted pending publication and fresh review.

# Decision: Accept the native Windows OpenSSH public-record terminator

The first authorized identity-provisioning attempt generated and ACL-hardened
the staged pair but failed before publication because Windows OpenSSH terminated
the public record with CRLF and the parser rejected every carriage return. The
record contract now accepts one optional LF or CRLF terminator and nothing
else: embedded line endings, a bare CR, multiple records, malformed fields, and
oversized input still fail closed. Derived-public validation parses the pinned
generator's actual three-field record and governed comment rather than adding a
synthetic field. The failed attempt published no key, requires no rollback, and
does not authorize a retry until this correction is published and freshly
prepared.
