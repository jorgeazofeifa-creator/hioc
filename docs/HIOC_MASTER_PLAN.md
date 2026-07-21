# HIOC Master Plan

**Version:** 1.0  
**Status:** Active  
**Owner:** Jorge Azofeifa  
**Project:** Home Infrastructure Operations Center (HIOC)

---

## Purpose of this Document

This document is the authoritative roadmap for the HIOC project.

It defines the project's vision, guiding principles, architecture, implementation roadmap, and working agreements. When implementation decisions conflict with conversational guidance, this document takes precedence unless it is intentionally revised.

Every contributor, human or AI, should read this document before making changes to the project.

---

## Document Ownership

This document is the constitution of the project.

It owns:

- vision
- philosophy
- principles
- roadmap
- implementation phases
- current phase
- current objective
- next task
- working agreement

It should not contain detailed architecture, MQTT documentation, Home Assistant documentation, data model details, installation instructions, release procedures, design system rules, or dashboard implementation details. Those belong in the focused documents linked from [../README.md](../README.md).

Update this document only when project direction, roadmap, phase, objective, next task, or implementation status changes.

---

# Vision

HIOC (Home Infrastructure Operations Center) is an operational platform for monitoring, understanding, documenting, and troubleshooting a home infrastructure.

Its primary purpose is **not** monitoring.

Its primary purpose is helping the operator immediately answer:

- What is happening?
- Why is it happening?
- What is affected?
- What should I do?
- What happened while I was away?

HIOC should behave like a miniature Network Operations Center (NOC), providing operator-oriented information instead of raw metrics.

---

# Design Principles

These principles override every implementation decision.

## 1. Stability Before Features

Never add features simply because they are possible.

Every feature must improve operator awareness.

---

## 2. Follow the Current Phase

Implement only the current planned phase.

Avoid introducing unrelated improvements or redesigning existing systems unless fixing a defect or explicitly approved.

When a phase is complete:

- Validate
- Commit
- Return to this document
- Continue with the next phase

---

## 3. One Problem at a Time

Each phase has one primary objective.

Complete it before beginning another.

Avoid parallel feature development.

---

## 4. Operator First

Dashboards exist for humans.

Every card should answer an operational question.

Avoid exposing implementation details whenever possible.

---

## 5. Explain, Don't Display

Do not simply expose values.

Explain:

- Meaning
- Impact
- Recommendation

The dashboard should reduce operator thinking, not increase it.

---

## 6. Passive Before Active

Always prefer information already available from the infrastructure.

Only perform active discovery when passive information cannot achieve the required objective.

---

## 7. Safe Operation

HIOC must never negatively impact the infrastructure it monitors.

Avoid unnecessary:

- Polling
- Network scans
- Broadcast traffic
- CPU usage
- Disk writes

---

## 8. Reuse Existing Components

Enhance existing systems whenever practical.

Avoid duplicate engines or overlapping functionality.

---

## 9. Incremental Evolution

Prefer extending existing architecture over replacing it.

Large redesigns require explicit approval.

---

# Architecture

Current major components include:

- Platform Core
- Inventory Engine
- Incident Engine
- Correlation Engine
- History Engine
- Dashboard v2
- MQTT Publishing Layer
- Home Assistant Integration

Additional components should integrate cleanly into this architecture.

---

# Dashboard Philosophy

Dashboard v2 is the primary operator interface.

Each page has a specific purpose.

## Operations

Current infrastructure health.

## Diagnostics

Current evidence.

## History

Past incidents.

## Inventory

Living infrastructure documentation.

## Network

Network diagnostics.

## Servers

Server diagnostics.

Future pages should have equally focused responsibilities.

---

# Incident Philosophy

Every incident should produce:

- Live status
- Supporting evidence
- Affected systems
- Dependency path
- Recommended action

When resolved, every incident should automatically produce:

- Timeline
- Summary
- Probable cause
- Duration
- Affected services
- Operator review

Historical analysis is considered a first-class feature.

---

# Inventory Philosophy

The Inventory is the living documentation of the infrastructure.

It should answer:

- What exists?
- Where is it?
- What does it do?
- What depends on it?
- Is it healthy?
- When was it last seen?
- How was it discovered?

Inventory information should become richer over time while remaining trustworthy.

---

# Development Roadmap

## Completed

- Platform Foundation
- MQTT Publishing
- Dashboard v2
- Incident Engine
- Correlation Engine
- History Engine
- Incident Review
- Dashboard usability improvements
- Initial Living Inventory

---

## Current Phase

### Phase 7A - Passive Living Inventory

Objective:

Build the richest possible infrastructure inventory without performing active network discovery.

Passive information sources include:

- Pi-hole DHCP leases
- Linux ARP / Neighbor tables
- Home Assistant Device Registry
- Home Assistant Entity Registry
- MQTT Discovery
- Existing integrations
- Known infrastructure definitions
- Routing information
- Passive operating system information

Expected outcome:

The Inventory becomes the authoritative documentation of the infrastructure without requiring active scans.

---

#### Phase 7A.8 Recovery Validation Chain

Status: **COMPLETE**

Scope: Recovery and re-validation of the approved lifecycle migration baseline after temporary validation state loss.

Completed validation sequence: R1, Post-R1, R2, Post-R2, R3, Post-R3, R4, and Post-R4. R4 received the formal decision **A. R4 APPROVED**.

- Approved generation: `gen_1784229948679_0a45eaf2f2f7`
- Approved recovery epoch: `/home/jazofv1/hioc-validation/phase7a8/epoch-20260716T173541Z`

The recovery sequence is complete, and the approved migrated baseline is the authoritative lifecycle recovery reference. The original HIOC Master Plan remains authoritative; Phase 7A Passive Living Inventory remains active; Active Discovery remains postponed. R5 is a future checkpoint and was not prepared or executed by this finalization.

This checkpoint preserves phased work, no scope creep, production validation, Evidence Reports, and return to the Master Plan after each completed sub-step.

#### Remaining Phase 7A Corrective Sequence

1. Repository and Deployment Hygiene.
2. Resume Phase 7A.9 Passive Inventory Correctness Validation.
3. Remaining inventory correctness work: validate duplicate collapse and correct any remaining defects; resolve FAILED/INCOMPLETE ARP semantics; verify dashboard severity mapping; validate collector canonical ownership; and validate Pi-hole DHCP lease ingestion.
4. Resume passive enrichment.
5. Continue toward asset-centric inventory.
6. Design and approve retention and archival policy.
7. Complete Phase 7A.
8. Begin Phase 7B Safe Active Discovery.

Phase 7A.9 is paused while the required hygiene checkpoint is completed. Remaining inventory correctness work follows Phase 7A.9, and passive enrichment resumes only after that corrective work.

---

## Planned Phase

### Phase 7B - Safe Active Discovery

Status:

Not started.

This phase is intentionally postponed until Phase 7A is complete.

Goals include:

- Manual discovery
- Scheduled low-frequency discovery
- Safe network probing
- No continuous scanning
- No aggressive port scanning

---

## Future Enhancements

Potential future work includes:

- Dependency graph visualization
- Infrastructure topology
- Automatic service relationships
- Failure propagation visualization
- Historical infrastructure trends
- Predictive recommendations
- Expanded operational analytics
- Backup and disaster recovery

These items remain intentionally out of scope until the current roadmap reaches them.

### Phase 7A Continuity and Deferred Hardening

Phase 7A remains focused on trustworthy passive discovery and enrichment. Completed corrective checkpoints, including Watch-device discoverability, remain part of that foundation. Deferred Phase 7A work remains preserved:

- Configurable passive-client retention and archival, after asset policy is designed.
- Canonical local-address hardening without production-specific identity exceptions.
- Continued Phase 7A enrichment from passive sources.

Active Discovery remains postponed. Future YAML dashboard deployment modernization also remains planned and must not be folded into unrelated inventory checkpoints.

### Asset-Centric Evolution

After reliable passive identity is established, Living Inventory should gradually evolve from unknown technical devices into identified, operator-managed assets. Planned capabilities include:

- Operator asset identity and friendly naming.
- Physical location and purpose.
- Owner or responsible person.
- Asset classification and operational criticality.
- Expected availability and explicit monitoring expectations.
- Asset lifecycle state, including active, retired, and archived concepts.
- Maintenance expectations, purchase or installation context, maintenance history, notes, and optional photo references.
- An operator workflow for physically matching discovered MAC addresses and other stable evidence to real assets.
- Gradual enrichment from an unknown device to an identified, managed asset without losing discovery provenance.
- Safe configurable retention and archival governed by asset policy rather than stale age alone.

These are future concepts. They do not add runtime fields or change current health, monitoring, incident, retention, or discovery behavior.

### Roadmap Dependencies

- Stable identity and passive discovery are foundational to operator asset enrichment.
- Asset classification must exist before aggressive archival can be safe.
- Expected availability must be defined before disappearance can be treated as failure.
- The improved dependency graph, automatic service relationships, failure propagation visualization, and infrastructure topology become more meaningful after assets and services are identified.
- Historical infrastructure trends and predictive recommendations depend on reliable identity, asset classification, relationships, and retained history.

The asset-centric vision expands the meaning of future work; it does not replace or reorder any existing phase or capability.

---

# Repository and Deployment Governance

HIOC formally separates the authoritative source checkout from the deployed production runtime:

```text
GitHub
  |
  v
/home/jazofv1/hioc-release-source
  authoritative source checkout for release execution on PI3
  |
  | release validation and the supported release process
  v
/home/jazofv1/hioc
  deployed production runtime
```

Deliberate source changes are developed and validated in an authorized development checkout, then committed and pushed to GitHub as the shared project history. After the approved changes are pulled on PI3, `/home/jazofv1/hioc-release-source` is the authoritative source checkout for release preparation and the supported release workflow. It should remain clean except for deliberate release work in progress.

`/home/jazofv1/hioc` is the deployed production runtime. It is expected to contain persistent operator configuration, runtime state, incident and inventory history, logs, backups, generated files, installer-managed permissions, and other operational artifacts. Production updates must use the supported release process from the authoritative source checkout or a validated release package, not direct Git updates inside the runtime.

The current repository workflow was not introduced through a single planned migration. It evolved organically as operational experience demonstrated the need to separate a clean development and release checkout from the production runtime. This document formalizes that proven workflow rather than introducing a new architectural model.

The existence or future removal of the production runtime's `.git` directory is a separate governance question and is not decided here. Repository and deployment cleanup must preserve persistent runtime state unless an artifact is proven obsolete and its removal is separately validated. Repository architecture changes must consider the full historical workflow and must not rely only on evidence from the most recent deployment or recovery event.

## Repository and Deployment Hygiene Checkpoint

The source/runtime architecture is settled and is not being reopened. The current checkpoint is the cleanup and reconciliation phase that follows governance reconstruction. It classifies production content before any controlled cleanup; it does not claim that cleanup is complete.

Repository and runtime artifacts use these disposition categories:

| Category | First-pass classification |
|---|---|
| AUTHORITATIVE SOURCE | GitHub `main` and the clean source checkout at `/home/jazofv1/hioc-release-source`. |
| DEPLOYED APPLICATION | `pi4/bin/`, `pi4/lib/`, required runtime configuration examples and support files, and `homeassistant/`. Preserve. |
| PERSISTENT RUNTIME DATA | `config/`, `state/`, `history/`, and `logs/`. Preserve. |
| DEPLOYMENT TOOLING | `release/`, `pi4/install_pi4.sh`, `pi4/uninstall_pi4.sh`, `pi4/validate_pi4.sh`, `homeassistant/install_ha.sh`, `homeassistant/validate_ha.sh`, and `VERSION.yaml`. Preserve pending dependency review. |
| BACKUP / ARCHIVE | `backups/`. Preserve pending backup and retention review. |
| GENERATED / TRANSIENT | `__pycache__/`, `*.pyc`, `.pytest_cache/`, and similar generated caches. Cleanup candidates only after validation. |
| SOURCE-ONLY CANDIDATE | `README.md`, `ROADMAP.md`, `DECISIONS.md`, `CHANGELOG.md`, and `docs/` inside the production runtime are provisional source-only candidates. Their presence reflects historical deployments rather than competing development history. They remain provisional until deployment behavior is changed and validated. |
| SOURCE / RELEASE VALIDATION | `tests/` is used by `release/validate.sh` in the source or release-validation context. Current evidence does not establish that it is required in the production runtime. |
| UNRESOLVED | The production runtime's `.git/` directory and any artifact whose ownership or dependency remains uncertain. Nothing classified as UNRESOLVED may be deleted. |

### Dependency Review Findings

The initial dependency review is complete for the current provisional source-only candidates. It reflects the evidence gathered against the current deployment architecture and establishes the baseline for subsequent deployment-manifest validation. No runtime, cron, systemd, installer, rollback, Home Assistant, or other operational dependency was discovered for `README.md`, `ROADMAP.md`, `DECISIONS.md`, `CHANGELOG.md`, or `docs/`. References among those files are documentation-to-documentation links rather than runtime dependencies.

`tests/` has a different role: `release/validate.sh` compiles the repository's test tree during source or release validation. This establishes a source/release-validation dependency but does not establish that `tests/` is required in the production runtime.

PI3-only recovery commit `5d0473dfd20efe7b07cf9167803d02aead10d61e` was reviewed against the authoritative `origin/main` history. Its `docs/RECOVERY_BASELINE.md` content is byte-for-byte identical to the authoritative version, and every substantive Master Plan addition is already present. The commit is therefore formally superseded and requires no merge or cherry-pick. It remains temporarily preserved on the PI3 local branch `recovery/phase-7a8-documentation-pi3` until this supersession record is committed and pushed, after which the branch may be removed as a separately validated governance action.

The current deployment process broadly copies the source tree into production. `release/upgrade.sh` excludes only `.git`, `dist`, `state`, `history`, `logs`, and `backups`; `pi4/install_pi4.sh` excludes only `.git` when source and installation paths differ. This broad synchronization explains why source-oriented documentation and tests are present in production. Nothing has been removed, and no deployment manifest or exclusion policy has been implemented.

### Next Hygiene Sub-Checkpoint

Define and validate an explicit production deployment manifest or exclusion policy. It must determine exactly which paths are:

- Deployed application.
- Deployment tooling required in production.
- Source/release validation only.
- Persistent runtime data.
- Excluded from production deployment.

Any deployment change must preserve:

- `config/`, `state/`, `history/`, `logs/`, and `backups/`.
- Rollback capability.
- Pi4 runtime executables and libraries.
- Required Pi4 validation tooling.
- Required Home Assistant deployment artifacts.
- `VERSION.yaml` and required release metadata.

Cleanup of existing production copies may occur only after the manifest or exclusion policy is implemented, release validation passes, a pre-change production backup exists, a dry-run or equivalent deployment preview is reviewed, production deployment is validated, and an Evidence Report is produced.

Production cleanup requires, in order:

1. Dependency validation.
2. A pre-change backup.
3. Controlled, explicitly scoped changes.
4. Production validation.
5. An Evidence Report.
6. A documentation update.
7. A code and documentation commit when both changed.
8. A push to `main`.
9. A clean authoritative working tree.

Phase 7A.9 remains paused until this required hygiene checkpoint is completed. No cleanup, deletion, or `.git` disposition is approved merely by this classification.

---

# Repository Rules

Every completed phase must:

- Compile successfully
- Pass unit tests
- Validate Home Assistant YAML
- Preserve backward compatibility unless explicitly approved

Every checkpoint Evidence Report must state:

- Deployment result.
- Intended behavior.
- Invariant checks.
- Warnings and deferred risks.
- Final PASS or FAIL.

Repository and deployment rules:

- Begin all deliberate source changes in an authorized development checkout.
- Keep documentation and code synchronized when behavior and operating procedures change together.
- Never copy generated runtime state back into source control.
- Do not allow the production runtime to become an alternate development branch.
- Investigate and classify unexplained source/runtime divergence before cleanup.
- Do not remove obsolete-looking files without evidence that they are unused.
- Ensure deployments are reproducible from the authoritative source checkout on the target host or a validated release package.
- Classify runtime and generated artifacts explicitly, then preserve or exclude them intentionally.
- Commit accepted recovery manifests and similar historical evidence documents to the authoritative repository history. Keep approved historical records immutable; new recovery work must create new evidence instead of modifying them or leaving them only in temporary branches or local repositories.

Unless specifically requested:

- Do not redesign unrelated code
- Do not rename MQTT topics
- Do not rename entities
- Do not introduce breaking changes

---

# Commit Rules

Every completed phase ends with:

1. Validate the intended behavior.
2. Validate applicable invariants and backward compatibility.
3. Update the Implementation Status and any relevant roadmap, governance, or decision sections in this document.
4. Commit code and documentation together when both changed.
5. Push to main.
6. Verify the development checkout has a clean working tree and the shared history contains the approved commit.
7. Record an Evidence Report containing the deployment result when applicable, intended behavior, invariant checks, warnings, and final PASS or FAIL.

`docs/HIOC_MASTER_PLAN.md` remains the authoritative project source of truth.

---

# Working Agreement

While implementing HIOC:

- Stay focused on the current phase.
- Avoid scope creep.
- Record future ideas instead of implementing them immediately.
- Return to this document whenever a phase is completed.
- Keep changes consistent with the project's architecture and philosophy.

---

# Implementation Status

This section reflects the current state of the project.

It should be updated whenever a development phase is completed.

The Phase 7A.8 Recovery Validation Chain, repository governance reconstruction, and reconciliation of the historical recovery documentation are complete. The temporary PI3 preservation branch has been retired, and GitHub history is authoritative. Development checkouts, the authoritative source checkout for PI3 release execution, and the deployed production runtime have formally documented roles. Phase 7A remains active. Repository and Deployment Hygiene is the current checkpoint and is not complete. Phase 7A.9 has not been executed and remains paused until the hygiene checkpoint completes.

## Current Branch

main

## Current Commit

Tracked by Git history. Do not update this document solely to record documentation-only commit hashes.

## Current Phase

Phase 7A - Passive Living Inventory

## Phase Progress

| Phase | Status |
|--------|--------|
| Platform Foundation | ✅ Complete |
| MQTT Publishing | ✅ Complete |
| Dashboard v2 | ✅ Complete |
| Incident Engine | ✅ Complete |
| Correlation Engine | ✅ Complete |
| History Engine | ✅ Complete |
| Incident Review | ✅ Complete |
| Dashboard Usability Improvements | ✅ Complete |
| Initial Living Inventory | ✅ Complete |
| Phase 7A - Passive Living Inventory | 🚧 In Progress |
| Phase 7B - Safe Active Discovery | ⏳ Planned |

## Current Objective

Complete the Repository and Deployment Hygiene checkpoint by validating dependencies and classifying production-runtime content before any separately approved cleanup. Preserve deployed application files, persistent runtime data, deployment tooling, backups, and every unresolved artifact.

## Next Planned Task

Complete the evidence-driven Repository and Deployment Hygiene review without deleting or changing production content.

After the hygiene checkpoint completes, resume Phase 7A.9 - Passive Inventory Correctness Validation as a read-only production-validation checkpoint with no behavioral changes. It will establish a trusted passive-inventory baseline and produce an Evidence Report.

Remaining Phase 7A corrective work and passive enrichment follow in the documented sequence.

Do not begin Active Discovery until Phase 7A has been completed.

---

# Decision Log

## 2026-07

Architectural decisions currently in effect:

- Dashboard v2 is the primary operator interface.
- Passive Living Inventory must be completed before Active Discovery.
- HIOC favors operator explanations over raw metrics.
- Historical incident review is a first-class feature.
- Incident testing will occur during real operational events rather than synthetic simulations.
- New features must not interrupt the current implementation phase.
- Scope changes require an intentional revision of this master plan.

---

# Maintaining This Document

This document should evolve deliberately.

Routine implementation work should update only:

- Current Phase
- Phase Progress
- Current Objective
- Next Planned Task

Changes to the project's philosophy, architecture, or roadmap should be made intentionally and reflected in the Decision Log.
