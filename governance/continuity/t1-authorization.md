# HIOC | Engineering Transition T1
## Durable Project Continuity Foundation

**Authorization:** Implement the first stage of the operator-approved engineering transition documented in [GitHub Issue #6](https://github.com/jorgeazofeifa-creator/hioc/issues/6).

**Accepted baseline:** `94f014cea1d5216a1deeef9fd1d0a025f1c7083e`

**Product state:** Phase 7A ACTIVE; PE-6.1 COMPLETE/PASS; PE-6.2 NOT STARTED.

**Objective:** Make HIOC recoverable across fresh ChatGPT and Codex sessions using a small, deterministic, verified repository-based continuity system.

Complete the entire authorized T1 repository task, including implementation, validation, documentation, commit, push, independent GitHub verification, and clean-working-tree verification.

Do not start T2, T3, T4, T5, or PE-6.2.

### 1. Permanent governing requirements

NO ASSUMPTIONS. EVER.

Follow:

`UNKNOWN -> VERIFY -> ESTABLISH EVIDENCE -> DECIDE -> ACT`

Preserve all original user instructions exactly. Do not silently replace, weaken, reinterpret, or omit any original requirement.

`docs/HIOC_MASTER_PLAN.md` remains the authoritative product plan.

GitHub Issue #6 is the approved engineering-transition tracking record, not a competing project authority.

Historical evidence must remain immutable.

Distinguish:

- Immutable repository facts.
- Current observed Windows repository facts.
- OPERATOR_SUPPLIED production observations.
- Direct production observations.
- UNKNOWN information.

Do not infer one from another.

### 2. Access boundaries

Operate exclusively in the Windows HIOC development repository.

Codex has no authenticated PI3 access.

Do not attempt to SSH into PI3 or PI5.

Do not access Home Assistant, MQTT, credentials, or production.

Do not synchronize or deploy anything.

Do not initiate PE-6.2.

Do not modify existing PE-6 implementation or accepted product behavior.

### 3. Establish the exact baseline

Before modifications:

1. Verify HEAD, branch, origin/main and working-tree state.
2. Verify accepted commit `94f014cea1d5216a1deeef9fd1d0a025f1c7083e`.
3. Read the authoritative Master Plan.
4. Read the current PE-6.1 implementation evidence.
5. Inspect existing project entry points and documentation ownership.
6. Inspect existing governance schemas and validation conventions.
7. Read GitHub Issue #6.
8. Determine whether an existing continuity or transfer mechanism can be reused.

Do not duplicate functionality without evidence.

If the baseline has unexpectedly changed or the working tree contains unexplained modifications, stop before overwriting anything.

### 4. Design the continuity architecture

Establish a single concise entry point.

Proposed path:

`docs/HIOC_PROJECT_CONTEXT.md`

This document must be understandable to an unfamiliar assistant with no previous conversation history.

It should identify:

- HIOC mission and intended operator value.
- Current major subsystems.
- Windows development repository and PI3 source/production separation.
- Responsibilities of operator, architect and Codex.
- Permanent no-assumptions policy.
- Immutable historical versus current authority.
- Development and deployment boundaries.
- Current accepted product baseline.
- Current phase and next checkpoint.
- Known pending work.
- Documentation ownership map.
- Where to retrieve authoritative technical evidence.
- How to recover from a stale or contradictory context file.
- The expected workflow for diagnosis, implementation, testing and acceptance.

Keep this document concise, preferably approximately 150 to 250 lines.

Do not copy the entire Master Plan into it.

Do not create another independent roadmap.

### 5. Machine-readable continuity state

Design a strictly validated handoff record and schema.

A suitable location can be selected through evidence-based review of existing repository conventions.

The record should identify:

- Schema version.
- Project/repository identity.
- Authority references.
- Accepted product checkpoint.
- Accepted baseline commit.
- Current engineering transition activity.
- Last verified state and evidence source.
- Current blockers and UNKNOWNs.
- Pending work and exact authorization boundary.
- Candidate state and recoverability.
- Immediate next action.
- Production access limitations.

The handoff must distinguish stable repository facts from live working-tree observations.

Never claim that a previously clean checkout remains clean merely because a committed file says so.

Never claim current production health from repository documentation.

Avoid self-referential commit-hash requirements in which committing a handoff makes the handoff immediately invalid.

Implement a consistent, explainable freshness model.

### 6. Deterministic continuity validation

Provide a small, reusable validation mechanism consistent with existing repository tooling.

It must detect:

- Missing required fields.
- Invalid schema versions.
- Contradictory product status.
- Incorrect repository or commit identity.
- Stale or superseded context.
- Incorrect document ownership references.
- Unauthorized assumptions about production.
- Unknown values presented as established facts.
- Invalid candidate-state transitions.
- Unauthorized advancement to PE-6.2.
- Sensitive information accidentally included in handoff artifacts.

Do not make historical snapshot validation depend incorrectly on current working-tree paths.

Avoid persistent current-candidate validation caches that bypass freshness checks.

Preserve immutable historical evidence and previously accepted governance.

### 7. Fresh-session recovery test

Simulate a fresh assistant or Codex session that receives no prior conversation history.

Using only the intended entry point, manifest, linked authoritative documents, and verifiable repository facts, the simulated session must correctly establish:

1. HIOC's mission.
2. Phase 7A as the current product phase.
3. PE-6.1 as the last accepted repository checkpoint.
4. PE-6.2 as the next planned product checkpoint.
5. PE-6.2's separate authorization requirement.
6. The absence of PE-6 production deployment at the accepted closure.
7. The Windows-only Codex boundary.
8. The operator-only PI3 execution boundary.
9. The engineering-transition sequence in Issue #6.
10. The immediate next authorized action.
11. Which current-state facts require new verification.

Test negative scenarios involving stale commits, contradictory handoffs, missing files, and unsupported production claims.

A fresh-session recovery test must not depend on a memorized chat summary.

### 8. Simplify the human workflow

Document a short standard startup procedure.

For future ChatGPT or Codex sessions, it should be possible to begin with:

"Continue HIOC. Read the project continuity entry point and verify the current state."

The documentation should then lead to the relevant technical contract without requiring the user to paste previous conversations.

State explicitly that external assistants without repository access must be given the necessary files or a verified export.

Do not claim automatic access or memory persistence when unavailable.

Provide a clear recovery procedure when the repository cannot be accessed or when a local candidate has never been committed.

### 9. Preserve existing architecture and governance

Do not redesign the existing HIOC product.

Do not rewrite the Master Plan's historical chronology.

Do not change:

- Identity reconciliation.
- Canonical IP.
- Inventory authority.
- Health or liveness.
- Asset schema.
- PE-5 associations.
- PE-6 classification implementation.
- Public projections.
- MQTT.
- Runtime schedulers.
- Production deployment logic.

Changes must be limited to the new continuity mechanism and directly necessary documentation, governance and tests.

### 10. Test and acceptance

Implement appropriate positive and negative tests.

Verify:

- Valid continuity artifacts pass.
- Stale or contradictory state fails clearly.
- Immutable history remains intact.
- Current working-tree verification cannot be bypassed.
- No source or production status is fabricated.
- No secrets are included.
- Existing PE-4, PE-5 and PE-6 compatibility remains valid.
- Original protected artifacts remain protected.

Run the focused continuity tests and all materially affected cross-phase regressions.

Determine whether the complete native suite is required under existing authoritative test policy and execute it if required.

If a failure occurs, investigate its architectural cause before making another correction.

Do not enter an unbounded assertion-by-assertion repair cycle.

Stop for a genuine unresolved material blocker.

### 11. Documentation and permanent continuity

Update the Master Plan only where needed to record the approved engineering transition and its completed T1 status.

Keep the product roadmap intact.

Link to GitHub Issue #6 and the new continuity entry point.

Preserve explicit separation between the engineering transition and PE-6.2.

Document who or what maintains the continuity artifacts, when they are refreshed, and how their freshness is verified.

Do not add a large new historical narrative for routine diagnostic details.

### 12. Repository completion

If all required acceptance conditions pass:

1. Verify final change scope.
2. Verify protected historical artifacts.
3. Update the appropriate documentation and status.
4. Commit code, tests and documentation together.
5. Push to main.
6. Independently retrieve the published GitHub commit.
7. Verify changed artifact identities.
8. Verify clean working tree and staging.
9. Verify HEAD equals origin/main.
10. Preserve stash state.
11. Stop before the next transition stage.

Do not initiate PI3 synchronization, production deployment, T2, or PE-6.2.

### 13. Required Evidence Report

Return:

`RESULT`  
`TRANSITION_STAGE=T1`  
`BASELINE_COMMIT`  
`PROJECT_CONTEXT_PATH`  
`HANDOFF_SCHEMA_PATH`  
`HANDOFF_STATE_PATH`  
`VALIDATOR_PATH`  
`CURRENT_AUTHORITY_VERIFIED`  
`FRESH_SESSION_RECOVERY`  
`STALE_STATE_REJECTION`  
`CONTRADICTORY_STATE_REJECTION`  
`PRIVACY_VALIDATION`  
`HISTORICAL_EVIDENCE_PRESERVED`  
`FOCUSED_TESTS`  
`AFFECTED_REGRESSIONS`  
`FULL_NATIVE_SUITE_DISPOSITION`  
`TEST_FAILURES`  
`TEST_ERRORS`  
`PROTECTED_INVARIANTS`  
`DOCUMENTATION_SYNCHRONIZED`  
`FILES_CHANGED`  
`COMMIT`  
`PUSH`  
`INDEPENDENT_GITHUB_VERIFICATION`  
`WORKTREE`  
`HEAD_EQUALS_ORIGIN_MAIN`  
`PE6_1_STATUS`  
`PE6_2_STARTED`  
`PRODUCTION_ACCESS`  
`PRODUCTION_MUTATION`  
`NEXT_TRANSITION_STAGE`  
`STOP_REQUIRED`

### Completion principle

The goal is not to produce another elaborate governance mechanism.

The goal is to make a fresh conversation capable of understanding the project's actual state correctly, quickly, and without reliance on prior chat memory.

Favor the simplest solution that demonstrably satisfies that requirement.

Complete T1 as one coherent authorized repository task. Stop after accepted T1 closure or a genuine blocker.