# HIOC Project Continuity

Derived recovery entry point; not an independent roadmap or production authority.
Start here in a fresh assistant session, then verify the linked sources.

## Start a session

"Continue HIOC. Read the project continuity entry point and verify the current state."

1. Work in the authorized Windows development repository only.
2. Read this file and [the machine-readable handoff](../governance/continuity/project-handoff.json).
3. Run the read-only validator below from the repository root.
4. Read the current Master Plan sections; historical narratives do not supersede them.
5. Report what was verified, what remains UNKNOWN, and the exact authorized scope.
6. If any source disagrees, stop dependent work and resolve evidence first.

```powershell
& "C:\Users\JorgeAzofeifaCastill\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -B tools/hioc-project-context.py
```

This interpreter path was verified for T1; another machine must verify its interpreter.
The tool reads local Git/files only, writes no files, and performs no network request.
A nonzero result is UNKNOWN_STOP; preserve work and inspect the conflicting evidence.
Do not treat a committed handoff as proof that today's working tree is clean.

## Mission and operator value

HIOC is the Home Infrastructure Operations Center.
It helps the operator understand what is happening, why, what is affected,
what action is appropriate, and what happened while the operator was away.
Monitoring supports this operational understanding; it is not the complete objective.
The existing [project overview](PROJECT.md), path `docs/PROJECT.md`, owns subsystem orientation.
[README](../README.md) remains the repository front door and documentation map.

Major subsystems include passive Living Inventory, incidents and correlation,
history and forecasts, retained MQTT telemetry, the Home Assistant operator console,
Asset Foundation, passive service associations, and private classification/metadata quality.
Read the focused owners below rather than duplicating their technical contracts here.

## Product state anchored in immutable evidence

Accepted product baseline: `94f014cea1d5216a1deeef9fd1d0a025f1c7083e`.
This is PE-6.1's accepted repository closure, not the future T1 commit's own hash.
Phase 7A is ACTIVE; PE-4 and Public Projection are PASS/CLOSED.
PE-5 is COMPLETE; PE-6.0 and PE-6.1 are COMPLETE/PASS.
PE-6 remains in progress with repository implementation and no PE-6 deployment at closure.
PE-6.2 - PI3 Release-Source Synchronization is the next planned product checkpoint.
PE-6.2 is NOT STARTED and requires separate authorization.
Product status comes from the Master Plan and accepted Git evidence, not Issue #6.

PE-6.1 implements a private, stateless classifier and explicit offline caller.
It adds no persistent result store, scheduler, inventory hook or public projection.
Suggestions do not become operator declarations or alter operational health.
Identity, canonical IP, public inventory, liveness and MQTT contracts remain unchanged.
See [accepted PE-6.1 evidence](PE6_CLASSIFICATION_IMPLEMENTATION.md).
See [the adopted PE-6 design](PE6_CLASSIFICATION_CONTRACT_DESIGN.md).
Accepted PE-4/PE-5 production observations remain OPERATOR_SUPPLIED.
No repository fact establishes today's production health, freshness or configuration.

## Engineering transition is separate

[Issue #6](https://github.com/jorgeazofeifa-creator/hioc/issues/6) tracks the approved transition.
Its exact retrieved text is preserved in [the source snapshot](../governance/continuity/engineering-transition-issue-6.md).
The original T1 authorization is preserved [verbatim](../governance/continuity/t1-authorization.md).
The issue snapshot records approval and sequence, not live issue status.
The Master Plan remains the sole product direction and sequencing authority.

- T1: durable continuity foundation (this repository implementation).
- T2: historical/current binding audit and equivalent centralized invariant coverage.
- T3: deterministic Windows/Linux-target test environments and safe CI evaluation.
- T4: one bounded capability pilot with workflow and operator-value measurements.
- T5: evidence-based consolidation after the pilot.

T1 completion does not authorize T2, T3, T4, T5 or PE-6.2.
Immediate action during an unpublished T1 candidate: verify and finish only authorized T1 acceptance.
Immediate action after accepted T1 publication: STOP; wait for separate authorization.
T2 is the next transition stage, not an instruction to begin it.
Phase 7B Active Discovery and later roadmap capabilities remain postponed as planned.
Surveillance implementation is not authorized by this transition.

## Responsibilities and access boundaries

The operator owns priorities, authorizations, production execution and supplied observations.
The architect/assistant analyzes authority, identifies UNKNOWNs and proposes bounded contracts.
Codex implements and validates authorized repository changes and reports precise evidence.
No role may silently replace an original instruction or infer operational authority.

Windows development repository:
`C:\Users\JorgeAzofeifaCastill\Documents\HA\hioc`
PI3 source checkout: `/home/jazofv1/hioc-release-source` (operator-managed Git source).
PI3 production runtime: `/home/jazofv1/hioc` (non-Git deployment target).
These three locations have distinct authority; source synchronization is not deployment.
Codex has no authenticated PI3 access and must not attempt SSH to PI3 or PI5.
No Home Assistant, MQTT, credential or production access is authorized.
No production mutation, synchronization, deployment, scheduler or service operation is authorized.
Operator execution on PI3 requires its own explicit bounded authorization.
A repository script or documented command never grants permission to execute it in production.

## Permanent evidence rules

NO ASSUMPTIONS. EVER.
UNKNOWN -> VERIFY -> ESTABLISH EVIDENCE -> DECIDE -> ACT
Preserve all original user instructions exactly; no silent omission or weakening.

- IMMUTABLE_REPOSITORY_FACT: accepted Git object identity and repository content only.
- DIRECT_OBSERVATION with WINDOWS_REPOSITORY scope: a fresh local command/observation.
- OPERATOR_SUPPLIED: production observations supplied by the operator; retain this label.
- DIRECT_OBSERVATION with production scope: only actually authorized/performed; none in T1.
- CRYPTOGRAPHICALLY_BOUND_OBSERVATION: exact evidence binding, never an inferred production fact.
- UNKNOWN: missing, inaccessible, contradictory or unverified information.

This T1 task produces no direct production observation.
Historical accepted snapshots stay bound to historical Git objects.
Current bindings validate the present candidate freshly; successful earlier checks are not a cache.
A historical clean state, pushed commit or source checkout cannot prove live production state.
Never promote an expected value, plan, source hash or UNKNOWN into an observed fact.

## Documentation ownership and retrieval

| Subject | Authoritative document |
|---|---|
| Product principles, phase, objective, next task | [Master Plan](HIOC_MASTER_PLAN.md) |
| High-level project/subsystems | [Project overview](PROJECT.md) |
| System reference | [System reference](SYSTEM_REFERENCE.md) |
| Runtime and operations | [Operations](OPERATIONS.md) |
| Source/deployment boundary | [Deployment](DEPLOYMENT.md) |
| Architecture | [Architecture](ARCHITECTURE.md) |
| Data contracts | [Data model](DATA_MODEL.md) |
| MQTT | [MQTT](MQTT.md) |
| Home Assistant | [Home Assistant](HOME_ASSISTANT.md) |
| PE-6 accepted design | [Design contract](PE6_CLASSIFICATION_CONTRACT_DESIGN.md) |
| PE-6.1 repository implementation/evidence | [Implementation evidence](PE6_CLASSIFICATION_IMPLEMENTATION.md) |
| Transition tracking only | [Issue #6](https://github.com/jorgeazofeifa-creator/hioc/issues/6) |
| Continuity mechanics only | This file and `tools/hioc_project_continuity.py` |

The handoff's ownership map must match these established document responsibilities.
Use accepted commit/blob bytes for historical verification; do not substitute today's file.

## Freshness and recovery model

The handoff is a derived, strictly typed snapshot with a fixed accepted product baseline.
It records the historical clean Windows observation at T1 start with its limitation.
It does not store a claim that the T1 commit has already been pushed or independently verified.
Git observations establish publication, HEAD, origin/main, candidate state and cleanliness afresh.
Artifact identities cover the finite T1 scope except the handoff/schema themselves.
Their canonical bytes, exact typed schema and stable semantic rules are validated directly.
This avoids a record hash depending recursively on itself or on its future commit hash.

Current mode checks the repository identity, baseline ancestry, exact scope,
working bytes, index identities, all protected baseline files, owners and product boundaries.
A staged T1 candidate at the baseline and a clean committed T1 state are distinct legal states.
An unexpected path, unmerged index, changed source, stale context or contradictory record fails.
A later product or transition change requires an explicitly authorized continuity refresh.
Do not automatically adopt a later HEAD just because it is newer.

For explicit historical verification only:
`python -B tools/hioc-project-context.py --commit <full-40-character-commit>`
This reads the requested immutable tree; it says LIVE_STATE=NOT_OBSERVED.
It must not depend on the current checkout containing that snapshot's files.
Historical success is not current-session acceptance.

If the context is stale or contradictory, stop mutation and compare authoritative Git objects,
the current Master Plan sections, the handoff and newly observed local state.
Identify the exact conflict; obtain evidence or authorization rather than guessing.
Do not reset, clean, restore, restage, overwrite or delete an unexplained candidate.

If a candidate was never committed, the committed handoff cannot recover its missing bytes.
Preserve the actual checkout/index; capture its diff, exact candidate blobs and a sanitized
manifest through an explicitly authorized export/backup procedure before changing machines.
Absent those bytes, candidate recoverability is UNKNOWN; never reconstruct it from chat memory.
If the repository cannot be accessed, request the necessary files or a verified export.
An external assistant has no automatic repository access or persistent conversation memory.
A verified export must bind exact files to a commit, or separately identify unpublished bytes.
An inaccessible authority or incomplete export means UNKNOWN_STOP, not permission to continue.

## Standard engineering workflow and maintenance

Read authority -> verify state -> diagnose -> implement within scope -> validate -> accept.
Then commit -> verify commit -> push -> independently verify GitHub -> verify clean repository.
A scoped authorization covers routine work; genuine evidence/contract blockers require a stop.
Investigate a failed validation's cause before correction; avoid assertion-by-assertion patching.
Use the established native Windows stdin unittest harness from the repository root,
with shell-free PATH, HIOC_TEST_SHELL cleared, and sys.path[:0]=['tests','pi4/lib'].
Run focused and materially affected regressions; apply the authoritative full-suite policy.
T1 adds repository tooling, so its acceptance includes the complete native suite.
Platform/dependency skips remain skips, with explicit reasons, never passes.

The contributor completing an authorized checkpoint maintains continuity in the same change.
Refresh the handoff/context when baseline, current authority, ownership, transition or scope changes.
Recalculate artifact identities only after final bytes stabilize; validate before publication.
Maintain exact historical snapshots separately; never rewrite accepted evidence for convenience.
Record observed validation totals in the completion report and commit message.
Publication and live cleanliness are independently checked rather than asserted by this file.
Stop after T1; the next transition stage and product checkpoint require separate authorization.

The two directly affected current binding helpers recognize only manifest-verified T1 changes.
Accepted PE-6.1 validator/test bodies replay immutable 94f014c objects; T1 freshness tests
exercise current files separately. The shared historical runtime guard permits only the two
new, baseline-absent read-only continuity tools. Existing runtime artifacts remain immutable.

Completed T1 acceptance and environment disposition: [Master Plan T1 closure](HIOC_MASTER_PLAN.md#engineering-transition-t1---durable-project-continuity).
Publication identity comes from verified Git objects, never a stored live-clean claim.
