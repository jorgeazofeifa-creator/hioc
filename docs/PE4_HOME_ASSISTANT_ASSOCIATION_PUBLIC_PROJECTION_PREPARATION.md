# PE-4 Home Assistant Association Public Projection Preparation

Status: **PASS/CLOSED**. Public Projection: **NOT STARTED / PREPARED FOR SEPARATE IMPLEMENTATION**.
This repository-only checkpoint freezes architecture, governance and synthetic
specifications. It adds no runtime helper, inventory integration, adapter change,
HA package/dashboard change, deployment tool or scheduler change. Synthetic model
execution is not public-projection runtime execution or production validation.

## Repository authority and evidence

Starting main and origin/main: `debe1ae485cf6b88839f9f8f2fbb071835deda05`, subject
`PE-4: close association scheduler deployment`, direct parent
`8579bb9707a1b8fd9b525b66a5156f5e96bc2429`. Origin was fetched; branch,
exact identities, 0/0, clean worktree and absence of active Git operations were
verified before modification. The record binds 103 material source identities
at this exact predecessor, with Git blob and SHA-256. Only the Master Plan and
current lifecycle expectation tests are marked historical-only; all runtime,
HA, deployment, scheduler and historical governance bytes remain unchanged.

The frozen 0C record authorizes exactly five public facts. Its contract document
explicitly maps private `unique_mac` to public `strong_mac` (Public projection
boundary). The 0C.1 lifecycle clarification gives binding history no public,
identity or liveness authority. Schema 1.1 admits technical config-entry domains
separately from entity platforms. No immutable authority requires false-valued
association objects or an entity-platform fallback. The narrow decisions below
therefore resolve these questions without broadening the frozen allowlist.

Operator-supplied prior review places PI3 source at this predecessor, main equal
to origin/main, clean 0/0 with no Git operation. The independently supplied current
crontab SHA-256 is
`8f900f4679aa861b02e781a61927683db5900ddfe159d78c3831a1595ae7fe71`.
This is historical supplied evidence, not a Codex production observation.
Counts and HA version in predecessor closure evidence remain snapshot-only;
no current production counts or version become projection expectations.

## Single writer and cycle integration

`pi4/bin/hioc-inventory-engine.py` remains the sole public inventory writer.
It owns inventory.json, devices.json, services.json, topology.json,
dependencies.json, summary.json and status.json; current capabilities output
and compatibility behavior are also preserved. The association adapter writes
only its private association state. Its scheduler cannot mutate public inventory
or publish MQTT. Generic `state/inventory/integrations` ingestion is prohibited:
it precedes identity reconciliation and can acquire discovery/liveness authority.

Future cycle order:

1. Remove `home_assistant` from copies of prior public device dictionaries before
   passing prior inventory into discovery. The current retained-device branch
   uses `record = dict(old)`, which would otherwise preserve arbitrary fields.
2. Generate base inventory through unchanged discovery, canonical identity,
   reconciliation, observation, health and enrichment logic.
3. Strip `home_assistant` from every resulting device again. This also excludes
   incoming source fields; no prior or upstream public object becomes authority.
4. Copy and validate the optional private snapshot, derive all candidate public
   objects and validate the whole candidate before attaching any of them.
5. Attach only to the intersection of current generated stable device IDs and
   validated active association stable IDs, after private-field removal and
   before the first authoritative public file write. Preserve base device order.
6. Write existing local files before existing MQTT publication as today.

A missing current device is skipped; no new device, observation, identity record,
MAC/IP/hostname or history-derived member can be created. An optional sanitized
local unmatched count may aid diagnosis, but no public aggregate is authorized.
An ambiguous duplicate current stable ID invalidates the optional projection.

## Exact public object

Only actively associated current devices receive `home_assistant`. All five
keys are required within each admitted object; devices without a current active
association omit the entire object. Absence is not an HA negative observation.

| Public field | Frozen derivation |
| --- | --- |
| associated | Exactly boolean true, valid active association intersecting current inventory |
| association_basis | Exactly strong_mac, from private unique_mac only |
| entity_count | Length of validated current entities, default empty; integer 0 through 65536 |
| integration_domains | Config entries' domain only, unique lexicographically sorted; default empty |
| has_area_candidate | Boolean presence of a validated non-null area_candidate object |

Domains have at most 4096 members, each 1-64 characters matching exactly
`^[a-z][a-z0-9_]{0,63}$`, inherited from private schema 1.1. Apply existing
`validate_privacy` and additionally reject a full 12-hex compact MAC string.
Colon/hyphen MACs, IPs, dotted hostnames, URLs, controls and objects fail the
closed domain contract. Technical config-entry namespace origin is mandatory:
a regex cannot establish that arbitrary free text is an integration domain.
Never accept unknown namespace values, titles or entity platforms as substitutes.
No arbitrary identifiers or free text may enter the object. Existing private
validation is applied first; unsafe private metadata invalidates the snapshot,
even when that metadata would not itself be projected.

COMPLETE and INCOMPLETE supporting relationships do not weaken a valid strong
association. Associated stays true; count only safely retained current members,
use only retained approved domains, reflect only valid area presence. Missing
metadata yields zero/empty/false and is never invented. Relationship status,
area IDs/names and all relationship identifiers remain private.

The separate closed public-object schema is embedded as a preparation fixture
in the record, alongside stricter sorting/value privacy semantics. The current
Core inventory schema checks only shallow top-level types; it does not enforce
this nested privacy boundary. Future code must validate the closed object
before attaching it. Inventory schema_version remains **1.0** for this optional
additive device field; private association schema remains **1.1**. Any future
schema interpretation change requires a separate governed checkpoint.

## Private validation reuse and failure isolation

Reuse the side-effect-free import of `hioc.home_assistant_association` and call
only `strict_json`, `check_schema_contract`, `validate_state(state, schema)` and
`validate_privacy`. No private validator copy or divergence is authorized.
Import currently uses only standard-library modules; websockets is imported
lazily inside `network`. A future implementation must prove compatibility under
the inventory's actual interpreter and verify the bound module and schema
identities, with secure no-follow owner/mode/ACL verification and the bound
module byte hash checked before import. It must not switch inventory to the association runtime or load a
websockets client. If extraction/refactoring later becomes necessary, it is a
separate adapter-affecting change with new governance/acceptance/quiescence.

Private schema SHA-256:
`5cd060ffd0a7a2e0a2b3e61da50ec8e5a418f4251df7305f713c10701b0e6a5d`.
Use strict UTF-8 JSON, duplicate-key and nonfinite rejection, bounded depth/size,
closed schema 1.1, stable ID syntax, current strong status/basis, active ID and
entity uniqueness, config-entry uniqueness, timestamp ordering, historical owner
and episode separation, exact summary/diagnostic consistency and privacy checks.
The reader validates a current snapshot without a prior argument. Cross-cycle
history preservation/transition validation remains the producer's responsibility.

Every optional import/read/parse/validation/derivation error is contained before
the inventory engine's global handler, which otherwise could log exception text.
Missing, unreadable, unsafe, malformed, duplicate, inconsistent, oversized,
identity-mismatched or incoherent input causes **all HA projection to be omitted
for that cycle**, while unchanged base inventory remains available. Build the
entire projection candidate before any attachment; no partial success leaks.

Strip prior public objects on every failure. Private LKG authority is not current
public projection availability: private bytes are untouched, while public objects
can disappear until a later safely validated snapshot is available. This means
neither retirement, failed association, offline, unhealthy nor unavailable.
Diagnostics are fixed local enums only: OMITTED_UNAVAILABLE, OMITTED_BUSY,
OMITTED_UNSAFE, OMITTED_INVALID, OMITTED_INCOHERENT or OMITTED_INTERNAL.
Do not log exception text, content, private IDs, paths with private identifiers or
relationship values. No private rewrite, recovery, cleanup, LKG erasure, HA retry,
credential read, adapter refresh or public status/summary aggregate is permitted.

## Concurrent snapshot and lock model

Selected model: a **short nonblocking shared lock on the existing association
lock**, then a secure bounded byte copy, release, and pure validation in memory.
An atomic pathname read alone is insufficient: the adapter creates a prior
hardlink, atomically replaces the final name, verifies it, writes a commit marker
and cleans transaction names. A failure before commitment can restore the old
state. A reader could otherwise consume a transient replacement or prior file
with link count two. Adapter exclusive locking covers recovery/publication.

The future reader must:

- Pin the existing directory chain from root through home/jazofv1/hioc/state/
  inventory/associations; never create missing paths. Require root or jazofv1
  ownership, no group/world writes and no unsafe extended/default ACLs. Require
  the association directory's existing owner/group and mode 0700.
- Open the existing `.home_assistant.lock` read-only, no-follow, regular-file,
  correct jazofv1 owner and accepted group, mode 0600, link count one, no unsafe
  ACL. Validate descriptor/name binding before and after acquisition. Use
  `LOCK_SH | LOCK_NB`; missing/busy/unsafe lock means omit, no create/wait/retry.
- Under the shared lock, reject any `.home_assistant.txn-` or
  `.home_assistant.done-` prefix, including malformed names, before and after
  copying. Never inspect/recover/delete transactional private content.
- Bound namespace inspection to 4096 entries and enforce a future finite copy
  deadline. Abort on excess. Open only the expected state regular file via the
  pinned parent, with no-follow/nonblocking flags, owner/group/mode 0600, link
  count one and ACL validation. Reject symlink/FIFO/device/directory.
- Require lstat/open/fstat fingerprint equality, size at most 16 MiB, complete
  bounded read, unchanged fstat/lstat afterward and rechecked parent/lock binding.
  Close/release on every path. Validate only the copied bytes after release.

No discovery, parsing/schema traversal, MQTT, HA, credentials or another lock
acquisition occurs while holding this shared lock. Existing inventory outer
flock `/tmp/hioc-inventory-engine.lock` stays unchanged; the adapter does not
acquire that lock, so this ordering introduces no lock cycle. No lock is held
through publication. Filesystem I/O cannot guarantee a hard wall-clock duration;
the future deadline and bounded work limit exposure and fail by omission.

The producer retains existing exclusive nonblocking behavior. A busy reader
omits this cycle's projection. A producer encountering the brief shared copy
can skip publication and preserve LKG until its next natural slot. No forced
retry, manual invocation, cascade or new scheduling is authorized. Once copied
under the lock, either complete previous or complete newly committed bytes are
valid input; later replacement does not invalidate that immutable memory copy.
The preparation tests model these predicates only; actual POSIX race/security
and lock-release behavior must be tested during separate implementation.

## Timing and MQTT/consumer behavior

Inventory remains at 0/30 (`*/30`); association remains at 5/35. Under normal
timely completed cycles, the next inventory slot is **25 minutes** after the
association slot. The 30-minute cadence therefore consumes a previously
completed private snapshot. Association duration shifts completion-to-slot lag;
process delays, contention, failed/skipped cycles or missed publication remove
any hard maximum wall-clock guarantee. Metadata lag implies no liveness,
health, stale observation or failure conclusion. No new scheduler, cascade,
immediate inventory trigger or adapter public write is authorized.

The five fields flow only through existing `<HIOC_BASE_TOPIC>/inventory` and
`/inventory/devices`. Existing `/inventory/services`, `/topology`, `/dependencies`,
`/summary`, `/status` and capabilities payloads do not gain association fields.
Preserve retained QoS 0, one MQTT connection per inventory run, local files
before MQTT and existing transport failure behavior. Sequential local-file and
retained-topic writes are not a new multi-topic atomicity guarantee.

The HIOC Inventory Devices sensor uses inventory/devices for count and
inventory as json_attributes_topic, transporting nested devices transparently.
No HA package change is required. No dashboard change, cards, notifications,
automations, entity-availability monitoring, Compatibility Diagnostics UX or
HA service/write authority follows. Home Assistant and dashboard source files
remain byte-identical to the bound predecessor.

## Future deployment ordering; no deployment now

Repository release upgrade/rollback copies a tree with rsync; install_pi4 rewrites
cron and immediately runs inventory. It cannot safely serve this narrowly scoped
future deployment without separately governed correction. Mixed engine/helper/
contract files and a running inventory process must be excluded explicitly.

A later authorized inventory-side deployment must pause only inventory scheduling
in an exclusive maintenance window, drain all inventory processes (including
manual runs), stage/hash/synthetically validate a coherent set, install helper
and public contract first, engine last, verify identities and restore the exact
inventory schedule after the separate gate. No forced inventory execution.
Association scheduling may remain active **only** when the adapter module,
private schema, association runtime and lock/security contract stay untouched.
The selected pure-function reuse meets that scope; future proof is still required.
Any shared adapter validator refactor requires new adapter acceptance governance
and association quiescence during its separately authorized deployment.
No quiescence, crontab mutation, runtime switch, installation or rollback occurs now.

## Authority and lifecycle

All canonical ID/MAC/IP, membership, hostname/manufacturer, Asset intent,
observation/liveness, health, incidents, topology, network parents, service
ownership, availability, MQTT health and HA state remain governed by their
existing owners. Projection is association metadata only. Binding history has
zero public authority and cannot resurrect devices or change these fields.

Scheduler Preparation and Deployment PASS/CLOSED; recurring operation ACTIVE /
AUTHORIZED; first natural invocation OBSERVED and first natural state publication
PASS. Independent Production Acceptance PASS/CLOSED. Manual Second Adapter
Execution NOT AUTHORIZED / NOT PERFORMED. Public Projection Preparation PASS/CLOSED;
Public Projection NOT STARTED / PREPARED FOR SEPARATE IMPLEMENTATION; PE-4 NOT COMPLETE;
Phase 7A ACTIVE; PE-5 NOT STARTED; rollback NOT PERFORMED. No unresolved architecture
questions remain; implementation/runtime/deployment verification is future work.

## Validation

Test-local specification models freeze private validator reuse, the closed
public object, active/history separation, varying counts, current-ID intersection,
stripping/recomputation, field authority preservation, privacy/error isolation,
determinism and coherent-read predicates. They do not implement or prove a
production filesystem reader. Runtime source identities and existing behavior
remain bound; existing inventory/MQTT tests provide regression coverage.

Native Windows command uses the bundled CPython 3.12.14 executable:
`C:\Users\JorgeAzofeifaCastill\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -B -`.
The Python stdin harness sets PATH to Windows System32, Windows,
System32/WindowsPowerShell/v1.0, Program Files/Git/cmd and the interpreter directory;
removes HIOC_TEST_SHELL; asserts Git present and bash/sh absent; prepends tests and
pi4/lib to sys.path. It loads named focused/targeted suites, then discovers
`test_pe4*.py` and `test*.py` in tests. Shell-dependent tests skip under the
established native method. Exact command and final totals are in the final report.

Initial focused draft run: 87 total, 85 passed, 1 failure, 1 error, 0 skipped.
Both were new test reference errors: strong_mac belongs to the bound contract
document, not its JSON record; entrypoint is run_cycle, not run. Corrected only
new test/governance references. No runtime change or suppressed failure.
Corrected focused run: 87/87 passed; targeted run: 310 total, 309 passed,
1 skipped, no failure/error. First complete PE-4 run: 1538 total, 1522 passed,
16 skipped, no failure/error. First full run: 2263 total, 2215 passed, 47 skipped,
1 failure, 0 errors. The failure was the unchanged compatibility Master Plan
current-next-task test still expecting scheduler deployment. Corrected that one
current expectation only; bound its predecessor bytes as historical-only. No
historical record changed. Strengthened the existing history fixture to reference
a current inventory ID, ensuring omission is due to history exclusion rather
than missing membership. No runtime behavior or timing threshold changed.
Final native Windows reruns:

| Suite | Total | Passed | Skipped | Failures | Errors |
| --- | ---: | ---: | ---: | ---: | ---: |
| Public Projection preparation | 87 | 87 | 0 | 0 | 0 |
| Targeted including compatibility lifecycle | 315 | 314 | 1 | 0 | 0 |
| Relevant PE-4 | 1538 | 1522 | 16 | 0 | 0 |
| Full repository | 2263 | 2216 | 47 | 0 | 0 |

Final PE-4 run took 241.273 seconds; full run took 263.026 seconds.
No timing-sensitive flake occurred and no timing threshold changed. Skips follow
the established native Windows method. After recording these results, focused
preparation tests were rerun to validate final canonical metadata/schema; all 87
passed. Git unstaged/staged diff whitespace checks passed before the one commit.
The full suite includes synthetic PE-1 fixture outputs, not new production evidence.

## Operator handoff

Immediate next action: **PI3 source synchronization to this preparation commit
ONLY**, then **STOP AND INDEPENDENT SOURCE REVIEW**. Future implementation needs
separate authorization. The final report supplies the exact host/user/predecessor/
subject/parent/changeset/artifact-hash guarded fast-forward-only source block.
Do not synchronize PI3 now or touch /home/jazofv1/hioc. Do not run adapter,
acceptance, reconciler, projection, MQTT or HA/credential/broker access; do not
alter scheduler or start PE-5. Independent natural 5/35 cycles may continue;
they are not execution by source synchronization.
