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

Status: Accepted for PE-3.0 architecture; implementation gated

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

Status: Accepted; executable implementation not started

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
