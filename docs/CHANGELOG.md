# HIOC Changelog

- Recorded PE-3 completion. Action 10 completed administratively with disposition
  `NOOP_ALREADY_ABSENT`; Actions 1–10 and PE-3 are complete. No PI3 or PI5
  action, staging recreation or deletion, production mutation, rollback, or
  Action 10 Evidence Report was required. Action 9 PASS and its Evidence Report
  remain the final PE-3 production validation and evidence. Transport staging
  remains absent, retransmission remains unnecessary, and all future-roadmap
  checkpoints remain preserved.

- Corrected PE-3 Action 10 governance as **CASE C — ADMINISTRATIVE NO-OP
  CLOSURE**. Historical Action 10 only deleted the two-file transport directory
  and rewrote an obsolete combined evidence report. Transport staging is already
  absent and non-authoritative after Action 6 immutable publication and Action 7
  activation; Actions 8 and 9 do not consume it. No PI3 verification, deletion,
  reconstruction, retransmission, or Action 8/9 evidence input is required.
  `NOOP_ALREADY_ABSENT` is the administrative disposition. Action 10 remains not
  complete pending validation, commit, push, and clean-tree verification of this
  correction, followed by a separate repository-only completion record.

- Recorded the governed PE-3 Action 9 production PASS. The read-only validation
  published its private Evidence Report at
  `/tmp/hioc-pe3-action9-Bb6vGrmm`, returned `ACTION9=COMPLETE` and
  `ROLLBACK_RECOMMENDED=FALSE`, and caused no production mutation or rollback.
  Its valid `12.467231`-second and `146744`-KiB total-peak-child-RSS
  observations remain `UNVALIDATED`/`INSUFFICIENT_BASELINE`; both historical
  targets were exceeded but were not production enforced. Actions 1–9 are
  complete, Action 10 remains not started/not prepared, Action 8 evidence remains
  preserved at `/tmp/hioc-pe3-action8-eZxNGrKa`, transport staging remains
  absent, retransmission remains unnecessary, and all future checkpoints are
  preserved.

- Corrected PE-3 Action 9 performance validation after its first read-only
  production attempt isolated a performance-only failure. Result and protected
  schemas passed; measured elapsed time was `12.467231` seconds and total peak
  child RSS was `146744` KiB. The four-second and incremental-RSS 48-MiB design
  targets lack current PI3 production provenance and no longer hard-fail Action
  9. Independent result, performance-syntax, insufficient-baseline assessment,
  and protected-snapshot stages replace the collapsed diagnostic. The private
  Evidence Report records sanitized observations and historical comparisons.
  No Action 9 evidence directory or production mutation occurred; rollback is
  FALSE, Action 9 is attempted but incomplete, and Action 10 is not started.

- Replaced the unsafe historical PE-3 Action 9 inline procedure with a governed
  read-only validation tool. It strictly validates the operator-supplied Action
  8 PASS evidence, reuses its portable performance record, independently proves
  current production artifacts and protected state unchanged, and publishes a
  private result-last Evidence Report. It has no `/usr/bin/time`, generator,
  strict interactive shell, staging, rollback, or Action 10 behavior. Action 9
  remains not started pending commit, push, synchronization, and authorization.

- Recorded the governed PE-3 Action 8 production PASS at commit
  `fa344828161e892523faa3da5d4cdf07d2e8e792`, including preserved private
  evidence `/tmp/hioc-pe3-action8-eZxNGrKa`, current source-refresh and
  corrected-validator deployment prerequisites, `ROLLBACK_RECOMMENDED=FALSE`,
  no rollback, absent/unnecessary transport staging, and no retransmission.
  Action 8 is complete; Action 9 remains not started pending a separate governed
  checkpoint after this completion record is committed and pushed.

- Corrected the active Action 8 bootstrap status from the stale historical
  `NOT STARTED` state to `ATTEMPTED BUT NOT COMPLETE`. The active contract now
  preserves Action 9 as `NOT STARTED` and requires reviewed source refresh and
  corrected-validator deployment before another separately authorized attempt;
  dated historical checkpoint statements remain historical evidence.

- Added a governed validator-only Action 8 corrective deployment boundary. It
  independently freezes the reviewed validator identity, supports exact
  identical no-op, creates a private durable backup only for replacement,
  publishes atomically in the runtime target directory, and proves protected
  manufacturer/configuration/dataset/inventory state unchanged. It does not use
  the broad release upgrade or invoke engines, schedules, Action 8, or Action 9.

- Corrected the Action 8 validator permission-class mismatch exposed by the
  third governed attempt. Both generated private artifacts passed exact `0600`
  identity checks, but the validator later applied their private bitmask to the
  inventory input and returned `MANUFACTURER_PERMISSION_ERROR`. Manufacturer
  outputs remain exact `0600`; inventory retains its no-group/world-write rule.
  Action 8 remains incomplete, the rollback advisory remains true, and no
  rollback or production action occurred.

- Replaced Action 8's undeclared hard-coded `/usr/bin/time` launcher after PI3
  retained sanitized exit-127 evidence proving instrumentation blocked the
  governed generator before execution was confirmed. Governed Python now owns
  child launch, monotonic timing, child maximum-RSS measurement, and a bounded
  launch-status marker. No output changed and rollback remains unrecommended.

- Corrected the active PE-3 Action 8 bootstrap trust gate after preparation
  stopped before PI3 execution because it still froze the superseded wrapper
  blob. The independently reviewed Git-blob anchor now names the current
  diagnostic-retention wrapper; parameterized governance-commit validation and
  every source-only fail-closed boundary remain unchanged. The replacement
  bootstrap remains not prepared or executed.

- Corrected PE-3 Action 8 generator-failure diagnostic retention after production
  forensics proved the failed invocation retained only protected pre-state. The
  wrapper now publishes private sanitized performance followed by result-last
  `generation-failure.json`, records allowlisted root cause, exit status, output
  mutation, and rollback advice, and deletes raw stdout/stderr captures. Action 8
  remains incomplete, Action 9 remains not started, and the changed wrapper
  requires a new post-push bootstrap before another separately authorized run.

- Removed PE-3 Action 8's unverifiable historical evidence-directory input.
  The wrapper now creates one unique private invocation-owned
  `/tmp/hioc-pe3-action8-XXXXXXXX` directory after read-only preconditions pass,
  publishes sanitized performance then result-last aggregate evidence, and
  reports the exact path. No bootstrap, generation, production, or later action
  occurred; the changed script requires a new post-push bootstrap identity gate.

- Corrected the PE-3 Action 8 bootstrap's self-stale governance identity. The
  gate now accepts an explicitly approved literal full 40-hex post-push commit,
  validates it before target/network work, and retains exact remote, ancestry,
  fast-forward, synchronized HEAD, cleanliness, and frozen script-blob barriers.
  No bootstrap, generation, production, staging, or later action occurred.

- Governed the separate PE-3 Action 8 bootstrap as a source-only clean
  fast-forward and exact script Git/worktree identity gate. It stops before
  generation and never reads or changes runtime state, configuration, dataset,
  manufacturer artifacts, Action 8 evidence, or transport staging. The
  bootstrap is prepared but not executed; Action 8 remains not started.

- Corrected the PE-3 Action 8 transport-staging lifetime defect exposed by the
  pre-generation `TRANSPORT_STAGING_INVALID` stop. Action 8 now treats transfer
  staging as transient Action 6 input, validates the installed immutable pair and
  active configuration as authoritative, and neither reads, recreates,
  retransmits, nor cleans staging. The stopped attempt generated no manufacturer
  artifacts; rollback is not recommended and Action 9 remains not started.

- Replaced the unsafe PE-3 Action 8 inline generation block with a governed
  protected-generation wrapper. It verifies target/source/runtime, activated
  configuration, exact immutable dataset, inventory, output preconditions,
  installed dataset, protected state, generated sidecar/status, and private
  aggregate evidence; preserves the generator's existing lock and atomic-write
  contracts; and stops before Action 9. Action 7 is complete, Action 8 remains
  not started, and no production action occurred.

- Replaced the unsafe PE-3 Action 7 inline configuration block with a separately
  bootstrapped repository-controlled activation transaction. The corrected
  contract proves source/runtime and exact immutable dataset identity, validates
  privacy-safe record count, preserves unrelated configuration, creates a
  private durable backup when needed, publishes atomically, validates the
  selected runtime path, reports bounded rollback guidance, and stops before
  Action 8. Action 7 remains not started; no production action occurred.

- Added the future PE-10 Application, Integration & Service Assurance roadmap
  phase. It distinguishes infrastructure availability from functional service
  health; preserves PE-7 expected availability and the existing PE-8/PE-9 Asset,
  impact, dependency, topology, and propagation work; records Tuya/Smart Life
  stale-state and Google Cast use cases; and defines evidence-based, bounded,
  functionally validated recovery and operator-focused notification targets.
  No implementation or production behavior changed.

- Synchronized the authoritative PE-3 status after reviewed production evidence:
  Actions 1-5, 6-A, and 6-B are complete; Action 6 is complete; Action 7 is not
  started; no rollback is recommended; the deployed runtime and transport
  staging remain preserved. This checkpoint did not prepare or execute Action 7.

- Replaced the unsafe PE-3 Action 6 inline immutable-install block with a
  separately bootstrapped repository-controlled installer. The corrected
  contract freezes the exact preserved staging path, full source/staging/
  configuration barriers, privacy-safe validation, same-filesystem no-replace
  atomic publication, bounded cleanup/failures, complete PASS evidence, and an
  explicit Action 7 authorization barrier. No target or dataset action occurred.

- Added the missing PE-3 Action 5C bootstrap contract. Inline Action 5C-A now
  performs only clean target synchronization and exact Action 5C script
  identity before stopping; separately authorized Action 5C-B remains the
  read-only closure. No target access, synchronization, revalidation,
  deployment, rollback, manufacturer mutation, or Action 6 work occurred.

- Corrected PE-3 Action 5 manufacturer protection after the first Action 5B
  deployment passed code/runtime validation but a raw recursive fingerprint
  misclassified release-managed empty `0700` scaffolding as dataset mutation.
  Read-only forensics proved no manufacturer payload or configuration activation
  existed, so rollback is not recommended. Added semantic payload protection,
  explicit payload/scaffolding/configuration evidence, and a separately
  bootstrapped read-only Action 5C closure. Added the future PI3 + PI5 abrupt
  power-loss/cold-boot recovery checkpoint; Action 6 remains not started.
  Validation passed 25 focused Action 5 tests, 120 manufacturer tests, and all
  571 repository tests with 8 environment-dependent skips.

- Added an explicit PE-3 Action 5A bootstrap gate because PI3 may remain at the
  prior Action 4 commit that predates the Action 5 deployment script. Action 5A
  performs only a clean exact fast-forward and proves the deployment script's
  availability and Git/worktree identity before stopping. Action 5B requires
  separate authorization and remains the first production mutation.
  Validation passed 29 focused tests, 17 release/governance tests, 120
  manufacturer tests, and all 560 repository tests.

- Hardened PE-3 Production Action 5 before its first execution. Replaced the
  unsafe interactive strict-mode/`tee` block and unresolved governance commit
  placeholder with `tools/hioc-pe3-action5-deploy.sh`. The governed script
  verifies target/source/self/artifact identity, performs pre-deployment release
  validation, uses only the supported upgrade path, proves the new backup,
  validates runtime identities, preserves dataset/configuration state, emits
  bounded evidence and rollback guidance, and stops before Action 6.
  Validation passed 24 focused tests, 120 manufacturer tests, and all 555
  repository tests with 19 environment-dependent skips.

- Split PE-3 Action 4 into separately authorized 4A synchronization/script
  identity and 4B permission-normalization/validator boundaries. Action 4A now
  emits eight explicit PASS barriers and stops without staging access or script
  execution. Action 4B remains the unchanged repository script and alone may
  complete Action 4 after separate authorization. No production action occurred.

- Gated the PE-3 Action 4 resume on target release-source synchronization after
  PI3 was found at `653f887a643c877a8f611145c8b8e9f92a65b6cd`, before the resume
  script existed. The bounded prerequisite permits only a clean exact
  fast-forward, verifies script Git/worktree identity, and dispatches only after
  availability passes. Existing staging was untouched and Action 5 remains not
  started.

- Completed the PE-3 Action 4 resume contract after finding that the inline
  procedure rechecked only modes and hashes after normalization and did not
  explicitly enforce validator JSON privacy/count fields. The exact operation
  now lives in a repository-controlled Bash script with full pre/post identity
  barriers, bounded chmod targets, explicit sanitized evidence, failure-path
  terminal safety, and permanent dangerous-operator-pattern guidance. Action 4
  remains stopped; no PI, staging, deployment, or production action occurred.

- Corrected the PE-3 staged-artifact permission contract after synchronized
  Action 4 safely stopped on validator rejection of transport-created `0644`
  files. Action 4 now identity-gates normalization of only the exact database
  and manifest to frozen mode `0600`, then rechecks mode and hashes before the
  read-only validator. Existing staging and completed synchronization evidence
  are preserved; Action 5 and production remain untouched.

- Corrected the PE-3 Action 3/4 sequencing contradiction discovered on PI3.
  Action 3 now verifies staging only; Action 4 synchronizes the clean source,
  proves implementation/validator identity, rechecks staged identity, and runs
  the read-only validator before Action 5 can deploy. Function-scoped operator
  failures now preserve the interactive shell and emit sanitized codes. The
  already-passed staging evidence is retained; no production action occurred.

- Promoted Windows CPython 3.13.x to supported after the first trustworthy
  governed checkpoint PASS on 3.13.15: full suite 520 with 13 skips, policy 10,
  Action 1 governance 13, manufacturer 119, compilation PASS, and clean tree.
  Action 1 now resolves only the exact manager-owned 3.13 interpreter. The
  validation checkpoint is explicitly one-time and refuses after promotion.
  CPython 3.14.7 remains an unsupported diagnostic side effect pending separate
  disposition. No PE-3 or production action occurred.

- Removed `ProcessStartInfo` from all governed Python runtime execution after
  final operator isolation proved the exact managed interpreter passes directly
  both normally and with the checkpoint pycache prefix, but fails through that
  wrapper. The checkpoint now uses scoped PowerShell-native invocation with
  immediate exit-code capture, temporary redirected streams, bounded tails,
  restored error policy, and cleanup for every Python stage. Non-Python utility
  execution is unchanged; support remains pending.

- Corrected Windows CPython checkpoint execution after governed evidence proved
  direct `py -3.13` passed while `ProcessStartInfo` launching the resolved App
  Execution Alias exited 1 despite completed stream tasks. Runtime execution now
  resolves the exact managed 3.13 interpreter with `pymanager list --format=exe`
  and invokes it directly, excluding default/3.14 selection and automatic
  installation. Diagnostic output now separates successful diagnostic execution
  from failed equivalence. Support remains pending and no checkpoint or
  production action was executed.

- Added a repository-controlled Windows process-wrapper forensic diagnostic
  after the governed checkpoint continued to report `FULL_REGRESSION_FAILED`
  while direct CPython 3.13 runs passed 508 tests with 13 skips and exit code 0,
  including with the checkpoint pycache prefix. The diagnostic compares direct
  PowerShell and current `ProcessStartInfo` execution using identical launcher,
  argv, environment, working directory, and suite, emitting only sanitized
  process metadata. Portable Windows tests cover large/simultaneous streams,
  nonzero exits, argv fidelity, spaced executable paths, repetition, and
  cleanup. The checkpoint and support state are unchanged pending evidence.

- Corrected a false `FULL_REGRESSION_FAILED` classification after an immediate
  direct governed CPython 3.13 run passed 506 tests with 13 skips and exit code
  0. The checkpoint had used a parsed `Ran` count as an extra acceptance gate
  while bounded capture retained the stream head and could omit unittest's
  trailing summary. Test stages now accept only authoritative native exit zero,
  preserve stream tails for sanitized count reporting, and retain every real
  nonzero failure. Focused regression coverage reproduces summary truncation.
  Support remains pending with no validated patch; no checkpoint, PE-3, PI, or
  production action was executed.

- Corrected the network-probe governance module's cross-platform prerequisite
  contract after the Windows CPython 3.13 checkpoint reached full regression.
  Three Bash-dependent tests had attempted an unresolved fallback executable
  and raised `WinError 2`; they now skip individually and visibly only when
  Bash is unavailable, while three platform-neutral checks always run and all
  six original assertions run where Bash exists. Full-regression failure/error
  handling and actual test/skip reporting remain unchanged. No runtime,
  support-state, PI, deployment, or production mutation occurred.

- Hardened every native execution path in the Windows CPython 3.13 checkpoint
  after the corrected operator run passed installation and failed at
  `PYTHON_PROBE`. Git, WinGet, `pymanager`, the exact 3.13 probe, all test
  stages, and compilation now share one PowerShell 5.1-safe wrapper with
  deterministic argument quoting, bounded stream capture, and native-exit-code
  semantics. The checkpoint reuses an authoritative managed 3.13 selection and
  installs only when absent. No exact 3.13 patch or compatibility result is
  inferred, support remains pending, and no Python/PI/production action occurred
  in this repository correction.

- Corrected the governed Windows CPython 3.13 checkpoint after forensic review
  proved that informational Python Manager stderr could become a PowerShell 5.1
  exception before native exit-code evaluation. Scripted management now uses
  `pymanager`, automatic runtime installation is disabled before every launcher
  probe, and one native-process helper captures stdout/stderr with the actual
  exit code. The official manager is present; an informal diagnostic's
  unintended CPython 3.14.7 installation is preserved and classified as an
  operator side effect, not HIOC support or production state. A safe dry run
  observed 3.13.15, while the governed line remains floating 3.13.x and pending
  validation. No Python install/uninstall or production action occurred here.

- Added the repository-controlled Windows CPython 3.13 installation and
  compatibility-validation checkpoint. The PowerShell script self-verifies its
  approved Git identity and pending support state, uses only the official WinGet
  Python Install Manager path, executes the complete governed validation matrix
  through `py -3.13`, preserves repository cleanliness, and emits sanitized
  promotion evidence. It does not promote support, execute PE-3 Action 1, or
  perform production work. No installation was executed in this commit.

- Established the authoritative Model D Python runtime compatibility policy.
  CPython 3.10 is the language floor, CPython 3.12.13 is the sole exact
  full-suite-tested version, Windows CPython 3.13.x is proposed with validation
  pending, and the distribution-managed production version remains unverified.
  Action 1 now requires explicit repository support promotion, probes only
  CPython 3.13 in `py -3.13`, `python3`, `python` order, disables automatic
  installation, and distinguishes missing from incompatible runtimes. The
  genuine Windows prerequisite failure remains separate from the earlier chat
  delivery defects. No Python installation or production action occurred.

- Replaced chat-delivered PE-3.3 Action 1 source with the repository-controlled
  Windows PowerShell script `tools/hioc-pe3-action1.ps1`. The runbook now records
  the script SHA-256 and Git blob and exposes only a direct parameterized
  invocation. The script self-verifies repository, governance, implementation,
  and script identity before the unchanged read-only artifact validation. Both
  failed operator attempts are delivery-path defects with no valid Action 1
  evidence and no PI3 or production impact.

- Attempted a PE-3.3 Action 1 operator-copy integrity correction after a
  delivered block was corrupted by Markdown escaping and backslash loss. That
  chat-delivery approach was later superseded by the repository-controlled
  script recorded above. The failed transcript is delivery failure, not
  manufacturer validation evidence; no production action occurred.

- Corrected the PE-3.3 Action 1 interactive-session defect. Expected Python,
  build-pair, repository/Git, containment, and validator failures now print
  sanitized result/error codes and return from a single function-scoped block;
  unexpected exceptions return `ACTION1_UNEXPECTED_ERROR`. Action 1 contains no
  `exit`, preserving the PowerShell prompt and evidence. No Action 1 validation
  evidence was accepted, and no PI3/PI5 access, transfer, deployment, production
  mutation, sidecar generation, or PE-4 work occurred.

- Hardened the documentation-only PE-3.3 Action 1 operator procedure after
  pre-execution review. It now resolves an executable Python 3 in the frozen
  `py -3`, `python3`, `python` order with `PYTHON3_NOT_FOUND`, and discovers an
  adjacent database/manifest pair only after both frozen hashes and sizes match,
  with deterministic selection among identical matches and
  `VALIDATED_BUILD_PAIR_NOT_FOUND` for zero matches. No Action 1 execution,
  artifact change, transfer, PI3/PI5 access, deployment, production mutation, or
  PE-4 work occurred.

- Audited and synchronized repository-wide documentation governance against Git
  history through PE-3.3. Corrected stale PE-1, PE-2, and PE-3 implementation
  status statements; restored the explicit PE-1 through PE-9 roadmap; preserved
  deferred monitoring, retention, notification, validator, dependency, and
  disaster-recovery work; documented authority and status vocabulary; and added
  `DOCUMENTATION_GOVERNANCE_AUDIT.md`. No executable, test, schema, production
  configuration, dataset, deployment, PI3/PI5, or PE-4 action occurred.

- Defined the documentation-only PE-3.3 production deployment and validation
  runbook. It freezes ten separately authorized operator actions, transfers only
  the validated normalized database/manifest, uses Git-object artifact identity
  and supported release deployment, atomically installs an immutable version,
  guards configuration changes, validates private sidecars and protected state,
  measures PI3 thresholds, and separates rollback domains. No transfer,
  deployment, PI3/PI5 access, sidecar generation, or PE-4 work occurred.

- Corrected PE-3.1 official-source normalization and conflict preservation.
  Organization normalization removes only U+200B/U+200E, collapses TAB as
  whitespace, and leaves every other prohibited control fail-closed. Assignment
  keys with multiple normalized organizations are stored without organization
  variants as explicit non-selectable conflicts; lookup returns
  `conflicting_assignment` and blocks weaker-prefix fallback. No IEEE rows or
  generated production artifacts entered Git.

- Implemented and repository-validated the private PE-3.1 manufacturer
  foundation: closed schemas, deterministic 36/28/24 lookup, local-only builder,
  lock-free validator, separately locked manual generator, atomic immutable
  publication/state writes, exact corrected errors, release preservation, data
  exclusion governance, 96 synthetic tests, and repository-host performance
  evidence. No IEEE or production data, network client, schedule, public
  inventory/consumer change, deployment, or production action occurred.

- Corrected the documentation-only PE-3.1 validator lock semantics. The
  standalone validator now explicitly acquires no lock and performs no mutation;
  database safety derives from atomic publication of complete immutable version
  directories. Runtime sidecar validation observes independently loaded files
  and reports cross-generation mismatches without repair. The exclusive builder
  and generator locks remain unchanged and are the complete manufacturer lock
  inventory. Future acceptance tests must prove the lock-free/read-only behavior.
  No executable, test, dataset, deployment, or production change occurred.

- Corrected the documentation-only PE-3.1 manufacturer error mappings by adding
  first-class bounded codes for dataset conflict, deterministic-build mismatch,
  sidecar validation, and status validation at the already frozen exits 10, 11,
  15, and 16. The `(code, message)` interface and every existing mapping remain
  unchanged. Builder owns conflict/determinism; validator and generator own
  sidecar/status validation. These failures prevent invalid artifact creation or
  publication, leave inventory and protected subsystems unaffected, and do not
  independently imply rollback. No executable, test, dataset, deployment, or
  production change occurred.

- Corrected the documentation-only PE-3.1 manufacturer generator lock order.
  The dedicated manufacturer lock now unambiguously covers database, manifest,
  and completed-inventory snapshot loading and validation through sidecar/status
  generation and writes. This closes the validation-to-generation TOCTOU gap
  while serializing manufacturer generators only; it does not acquire an
  inventory, PE-1, Asset, or other HIOC state lock and does not block or mutate
  inventory generation. The prior validate-before-lock implementation instruction
  is superseded only in this respect. No executable, test, dataset, deployment,
  or production change occurred.

- Froze the documentation-only PE-3.1 executable contract. Resolved the sidecar
  list-versus-map conflict and specified the separate manual generator, exact
  APIs/dataclasses/exceptions, database/manifest/sidecar/status schemas, builder,
  validator and generator CLIs, shared exit/error codes, configuration/paths,
  locks, atomic transactions, failure preservation, parser rules, EUI-64
  no-claim behavior, inventory input, privacy, release preservation, 92-test
  mapping, performance, production validation, and rollback. Local acquisition
  and transformation are approved; no code, test, dataset, deployment, or
  production change occurred.

- Approved the documentation-only PE-3.1 Manufacturer Enrichment implementation
  design. Froze restrictive license and external-injection governance, the
  normalized MA-L/MA-M/MA-S database schema and digest semantics, O(1)
  longest-prefix lookup, EUI/address-class behavior, three-module boundary,
  separate private manufacturer sidecars, provenance, PI3 performance bounds,
  fail-open isolation, privacy, production validation, rollback, and a 76-test
  executable plan. No code, dataset, deployment, or production change occurred;
  executable implementation remains gated and not started.

- Defined PE-3.0 Manufacturer Reference Enrichment architecture and governance
  without code, schema, tests, dataset or runtime changes. Selected pinned IEEE
  Registration Authority listings as the future authoritative upstream subject
  to an explicit redistribution-license gate; fixed deterministic lookup,
  provenance, confidence, privacy, failure-isolation, invariant, performance,
  validation and 64-case test contracts. PE-3.1 remains not started.

- Closed PE-2.1 Asset Foundation as **COMPLETE - PRODUCTION VALIDATED**. Deployed
  Git-derived identity, restrictive permissions, synthetic transactions and
  cleanup, final Asset equality, protected contracts, privacy, performance, and
  incident operational-drift classification passed. Four validator-governance
  defects were corrected without changing deployed Asset implementation files;
  no rollback occurred. PE-3 remains not started.

- Governed one-time cleanup of six exact PE-2 synthetic-only validation backups.
  Added an exact basename/SHA manifest, two-phase schema-aware cleanup tool, and
  moved future tracked current-run backup cleanup before unrelated invariants.
  No Asset implementation, real Asset state, retention policy, deployment, or
  rollback behavior changed.

- Corrected the second PE-2.1 validator-contract defect. Live `active.json` is
  no longer digest-immutable; a sanitized positive comparator classifies valid
  operational drift, proves Asset-to-incident isolation, and reserves rollback
  for causally demonstrated protected regressions. PE-2.1 remains deployed and
  open for validation-only production closure.

- Corrected the PE-2 production validator after the first supported deployment.
  All runtime artifact bytes matched Git, while the validator incorrectly
  treated Git `100644`/`100755` modes as runtime `0644`/`0755` requirements and
  its report writer inserted lowercase JSON booleans into Python source. A
  shared runtime-permission manifest, independent content/permission checks,
  safe JSON report renderer, corrected rollback classification and no-deploy
  revalidation mode now govern closure. No rollback occurred; PE-2.1 remains
  deployed and awaits corrected production revalidation.

- Implemented and repository-validated PE-2.1 Asset Foundation: strict private
  store/status schemas, governed local CLI, read-only validator, dedicated
  bounded lock, optimistic revisions, atomic fsync transactions, validated
  backup/restore, orphan context, privacy-safe output, conditional installer
  validation, release-preservation guards and synthetic tests. No public
  inventory, consumer, schedule or production change occurred; deployment and
  production validation remain pending.

- Completed the PE-2.1 Implementation Design Review without executable or
  production change. The approved design freezes module boundaries, schemas,
  normalization, locks, revisions, atomic transactions, backups/restores,
  sanitized output, exit/error codes, privacy, failures, production validation,
  cleanup, performance, release preservation, tests and the future implementation
  prompt. PE-2.1 executable implementation remains not started.

- Completed PE-2.0 design review and approved the implementation-ready Asset
  foundation for operator-managed `friendly_name`, `physical_location`,
  `purpose`, and private `notes`. The design uses a separate stable-ID-keyed
  closed local store, governed CLI, dedicated lock, atomic writes, validated
  per-mutation backups, explicit orphan handling, and deny-by-default privacy.
  Existing public naming/location fields are not reinterpreted; owner, public
  projection, expected availability, lifecycle, identity migration, UI and
  integrations remain deferred. PE-2.1 is not started and no executable or
  production behavior changed.

- Closed PE-1 Hostname Enrichment Evidence Envelope as **COMPLETE - PRODUCTION
  VALIDATED**. Git-derived artifact identity, supported deployment and backups,
  authoritative schema validation, and corrected production validation passed.
  Production reported `online`, 153 records, 83 candidates, 82 selections, zero
  conflicts, and the three observed source types `assignment_observation`,
  `configured_infrastructure`, and `direct_observation`. Missing optional source
  types, history, and conflicts were acceptable; protected public and
  operational contracts did not regress, no rollback occurred, and PE-2 was not
  started.

- Corrected the PE-1 production aggregate validator after its duplicated
  `source_type` allowlist used acquisition/source identity names instead of the
  emitted closed-schema values. Deployment, Git/runtime artifact identity,
  controlled inventory execution, and authoritative enrichment validation had
  already passed; no rollback condition was demonstrated, and the deployed
  PE-1 implementation remains unchanged.

## Document Ownership

This document owns released and delivered work.

This is the repository's single authoritative changelog. The root [CHANGELOG.md](../CHANGELOG.md) is a discoverability pointer only. All future release and completed-checkpoint entries must be written here. Maintaining a second overlapping full changelog is prohibited unless a separately approved governance decision establishes a distinct, non-overlapping purpose.

Use these categories when applicable:

- Added
- Changed
- Removed
- Fixed
- Deprecated
- Security

Do not place roadmap items here. Future work belongs in [../ROADMAP.md](../ROADMAP.md) and detailed implementation direction belongs in [HIOC_MASTER_PLAN.md](HIOC_MASTER_PLAN.md).

## Unreleased

### Added

- Implemented the repository-validated PE-1 Hostname Enrichment Evidence
  Envelope. The Inventory Engine now produces validated, restrictive local
  `enrichment.json` and `enrichment_status.json` sidecars from the four approved
  existing hostname sources, with deterministic normalization, authority,
  conflict, confidence, bounded history, atomic writes, and fail-open isolation.
  Public inventory, MQTT, Home Assistant, dashboards, incidents, identity,
  canonical address, liveness, health, topology, service ownership, retention,
  and operator metadata remain unchanged. Production deployment and validation
  subsequently passed.

- Added a deployed, read-only MQTT runtime validator that uses existing HIOC
  configuration to perform bounded retained-topic checks and emit concise
  post-install or post-upgrade Evidence Report output without publishing state
  or exposing credentials.

### Documentation

- Completed PE-0 design review and approved the implementation-ready PE-1
  Hostname Enrichment Evidence Envelope specification. The package closes
  hostname source eligibility, normalization, authority, deterministic
  selection, conflict/confidence, local schema, bounded lifecycle,
  failure-isolation, module, test, production-evidence, rollback, and privacy
  decisions. PE-1 remains not started; no executable or production behavior
  changed.

- Refined the proposed Passive Enrichment architecture into permanent,
  non-destructive Observation, Enrichment, and Asset information layers.
  Documented their separate authority, mutability, provenance, persistence,
  privacy, stale-observation, and expected-availability meanings; clarified
  that PE-1 records hostname observations and enrichment candidates but creates
  no Asset name or public/runtime behavior. PE-0 remains in design review and
  PE-1 remains not started.

- Defined the Phase 7A Passive Enrichment Architecture and Specification for
  design review. It maps implemented and absent passive sources, audits the
  current schema, separates metadata layers, and proposes field-level
  provenance, conflicts, categorical confidence, privacy boundaries, and an
  ordered implementation sequence. The first proposed sub-checkpoint is a
  local-only hostname evidence envelope. No executable or production behavior
  changed, and implementation remains subject to explicit approval.

- Closed Canonical Address Selection Hardening as production validated. The
  unchanged comparator from `839e924` matched source and runtime at the
  approved Git-derived SHA-256; all six strict Boolean invariants passed;
  diagnostic metadata remained informational; inventory stayed at 151 devices;
  and one unrelated canonical-address change remained within the bounded
  invariant. Final result was `NO_QUALIFYING_CANDIDATE` with no rollback. Both
  earlier failures were validator defects, not comparator defects. The
  unexpired `.152` old lease remains separate future DHCP cleanup evidence.

- Established the focused documentation architecture: the Master Plan remains the authoritative roadmap; the new System Reference Manual owns current state; Operations owns the cron-driven runtime and freshness-based health model; Network Foundation owns critical addresses and dependencies; Deployment owns source-to-runtime boundaries; and Incident Model owns operational incident semantics. Added the permanent July 29 DHCP pool-exhaustion incident report, recorded HIOC deployment validation as PASS, added the Operations Acceptance Standard, and planned a future DHCP Service Health & Capacity Monitoring phase without implementing it.
- Closed Pi-hole DHCP Lease Ingestion as **PASS WITH DOCUMENTED WARNING** after supported production upgrade, PI3 validation, and successful inventory generation. All 140 active lease MAC identities were represented with DHCP provenance and expiry metadata; seven additional DHCP-backed identities were confirmed as retained expired historical records rather than duplicate active leases. One active lease MAC/IP pair differed from the selected canonical IP because the same MAC owned two simultaneous `STALE` neighbor addresses. DHCP ingestion remains passed; deterministic canonical-address precedence is deferred to a separate Phase 7A hardening checkpoint that must preserve MAC-backed identity and must not treat DHCP assignment as liveness.
- Accepted ADR-0015 for the active Pi-hole DHCP Lease Ingestion checkpoint. Pi-hole DHCP remains a source-specific adapter within the existing passive-driver and source-tagged device-record convention; central reconciliation continues owning canonical identity, authority, and observation semantics. The decision rejects a new `IdentitySource` or plugin framework, defines DHCP field ownership and deterministic conflict rules, and bounds the later implementation without marking DHCP ingestion complete.
- Completed Repository and Deployment Hygiene. Historical runtime provenance proved that HEAD `94e1997f0d9df9e43209e44f7eb62a8d808714cc` was preserved in authoritative history and that no runtime-only commits, branches, tags, or stashes existed. The approximately 2.6 MB `.git` directory was quarantined and validated, the non-Git runtime passed production validation, a supported upgrade did not recreate `.git`, rollback did not restore it, post-rollback SHA-256 comparisons matched the authoritative release source for the checked deployment artifacts, and persistent runtime data remained intact. The approved quarantine path was removed successfully, the runtime remains formally non-Git, and all checkpoint closure criteria are satisfied.
- Completed Repository Governance Reconciliation on 2026-07-28: retained `validation/phase-7a8-lifecycle` locally and remotely as the intentional reachability reference for approved recovery candidate `be7b69d`; retired three fully merged local branches and the two corresponding remote branches that still existed; and removed the untracked `hioc_known_hosts.tmp` workspace artifact after confirming that no operational tooling consumed it. At that stage the overall Repository and Deployment Hygiene checkpoint remained open for the two manual PI3 audits and final closeout; the audits and production engineering validation are recorded as complete in the later entry above.
- Reconciled changelog governance by restoring the root `CHANGELOG.md` as a pointer to this authoritative record. Repository history confirms that the documentation-governance migration established this single-authority model; a later bounded implementation entry accidentally replaced the pointer and became stale after Collector Canonical Ownership regression, production, and documentation validation completed. No historical evidence was removed from Git history.
- Closed the Phase 7A Collector Canonical Ownership checkpoint after implementation commit `054fb55a2e70901f3230145b76983c31d2b5ce61` passed release validation, supported production upgrade, Pi4 validation, and production evidence review. The canonical collector remained MAC-backed at `192.168.100.252`, all eight services were owned by `Pi3 - NUT and Pi-hole`, and the historical `.105` ownership defect was not observed; this documentation-only closeout does not change runtime or public contracts.
- Recorded successful production deployment and validation of the single-snapshot ARP semantics correction: normal discovery reported `arp_table`, discovery remained unlimited, and the checkpoint closed after PASS evidence.
- Recorded successful ADR-0014 production validation and made the repository the
  authoritative operational reference for configured, read-only MQTT runtime
  validation after installation or upgrade.
- Documented the planned asset-centric Living Inventory vision, including evidence authority, observation versus availability, operator-managed asset knowledge, lifecycle-safe retention principles, and roadmap dependencies; no runtime behavior changed.

### Fixed

- Fixed the revised canonical production validator's invariant input contract.
  It previously applied generic truthiness to diagnostic metadata and treated
  `_unrelated_canonical_change_count: 0` as failure despite all six Boolean
  invariants passing. The validator now requires the closed, typed Boolean
  schema, preserves underscore-prefixed diagnostics without evaluating them,
  and reports malformed input explicitly. At that correction stage the
  expected rerun result was `NO_QUALIFYING_CANDIDATE`; rollback was not
  performed, the comparator was unchanged, and closure remained pending the
  PI3 rerun recorded above.

- Corrected the Canonical Address Selection production-validation procedure
  after the first governed run admitted an IPv6 link-local stale neighbor and
  ignored higher-authority configured integration evidence. Repository-owned
  validation now enforces the intended stale-IPv4-versus-active-DHCP contract
  and distinguishes `PASS`, non-rollback `NO_QUALIFYING_CANDIDATE`, and genuine
  `FAIL`. The comparator was unchanged and remained deployed. Active DHCP
  evidence for retired PI5 address `.152` remained unresolved pending the
  read-only PI3 investigation, and the checkpoint remained open at that stage.

- Implemented the repository correction for deterministic canonical IPv4
  selection. Neighbor state now participates as private reconciliation
  evidence; an active DHCP assignment for a MAC cannot lose merely to a stale
  neighbor address, while stronger current/configured evidence and legitimate
  static devices remain supported. Stable MAC identity, aggregate provenance,
  liveness, health, schemas, dashboards, incidents, and retention are
  unchanged. Production validation remains pending, so the Phase 7A checkpoint
  is still open.

- Closed the network-probe checksum-governance and PI5 endpoint-migration
  correction after governed PI3 deployment at
  `e06539d9bece040d721b9912213559cc54f1610d`. Blob, worktree, and deployed
  checksums matched; Phase A and Phase B passed; retained PI5 state and
  inventory were correct; the false incident cleared; and no rollback or
  warning was required. Phase 7A remains active.

- Separated deterministic network-probe deployment validation from bounded
  downstream incident-recovery observation. Delayed or inconclusive recovery
  now produces PARTIAL PASS and follow-up without rollback. Added safe read
  accounting, malformed-payload handling, backup validation, and a tracked
  operator procedure.

- Corrected the Phase 7A network-probe checksum-governance defect. The
  previously reported `27e4dec6...` checksum remains only as incident evidence:
  it is proven to be the CRLF Windows checkout hash, not the approved Git blob
  hash. Added deterministic Git-object identity, commit-bound deployment with
  blob/source/target byte comparisons, and stale-checksum regression tests.
  PI3 deployment was pending at that implementation stage and is closed by the
  later production-validation entry above.

- Implemented bounded Pi-hole DHCP lease ingestion semantics. Inventory cycles use one fixed collection epoch; only active finite or infinite IPv4 Pi-hole/dnsmasq leases contribute assignment evidence; expired, IPv6, ISC-format, malformed, and unusable rows contribute no identity evidence. Explicit blank configuration disables acquisition, the default is limited to `/etc/pihole/dhcp.leases`, source aggregation preserves complete and incomplete states, and unavailable configured DHCP evidence reports truthful discovery limitation without weakening MAC-backed identity or observation authority. Automated regression validation passed, and the later production Evidence Report closes the checkpoint with a documented canonical-address warning.
- Implemented the repository side of runtime Git metadata retirement. Upgrade backups now exclude `.git`, rollback restoration excludes `.git` even from historical backups, and tests preserve legitimate hidden files and persistent-state protections. README and operator documentation now use the release-source installation model, ADR-0013 formally defines `/home/jazofv1/hioc` as a non-Git runtime, and runtime version identity remains owned by `VERSION.yaml`. Manual PI3 provenance capture, quarantine, upgrade, rollback, and production validation were pending at that stage and are recorded as complete in the later production Evidence Report entry, including approved quarantine removal.
- Hardened release construction so `release/build.sh` obtains its complete source set from Git-tracked files instead of traversing the workspace. Ignored, untracked, cache, and temporary artifacts—including `hioc_known_hosts.tmp`—cannot enter a release merely by existing beside the source. The generated manifest now records the source commit without checkout-path or wall-clock fields, while deployment and runtime behavior remain unchanged.
- Deployed the bounded Pi-hole DHCP Single Snapshot Acquisition correction: inventory captures lease files once into a cycle-local immutable snapshot and reuses it throughout discovery status, passive observations, and reconciliation, removing duplicate acquisition without intentionally changing functional behavior. Automated regression tests prove the single-acquisition invariant; successful production deployment confirmed `dhcp_leases_found`, 145 DHCP-backed devices, preserved `/etc/pihole/dhcp.leases` metadata, and no observable inventory regression. The broader DHCP checkpoint remains open.
- Completed the Dashboard Severity Mapping checkpoint at implementation commit `1e2dcf973d02514561b7bb8a4f5c6f495350ab09`: Living Inventory aggregate Watch wording now covers observation or availability review without incorrectly describing every Watch condition as stale, Dashboard v2 gives unavailable inventory status precedence over retained device counts when styling Inventory Summary, and production deployment and validation passed. Health, schemas, MQTT, entities, incidents, layout, and the existing blue Watch palette remain unchanged; the Watch color UX/design decision remains deferred.
- ARP discovery-source status and passive device evidence now share one authoritative neighbor-table acquisition per inventory cycle, and total primary-plus-fallback command failure is reported as unavailable rather than successful empty evidence. Unresolved-neighbor filtering, identity, retention, health, monitoring, and accepted NUD-state behavior remain unchanged.
- Incident Engine retained publication now uses one shared Core MQTT connection per run instead of placing complete payload documents in `mosquitto_pub -m` process arguments, preserving local history, embedded reviews, topics, retained semantics, and payload schemas while returning a truthful nonzero status for required publication failures.
- Living Inventory now includes a dedicated Watch Devices presentation, ordered by oldest known observation first and showing authoritative identity, observation, provenance, and health-reason details without changing inventory semantics.
- Pi-hole DHCP lease ingestion now distinguishes missing, unreadable, malformed, I/O-error, empty, partial, and usable sources; validates lease fields; preserves assignment metadata without treating a lease as liveness; and prevents DHCP data from overriding stronger current identity evidence.
- Local services now retain ownership by the canonical pre-enrichment collector identity; known-infrastructure classification can no longer erase local-host ownership, and a missing collector no longer falls back to an arbitrary inventory device. Canonical-address selection is unchanged and remains a separate future hardening checkpoint.
- Inventory Summary now renders the dedicated recommendation entity so watch-only passive clients do not imply operator attention; degraded and offline guidance is unchanged.
- Home Assistant operational presentation now preserves the operator-supplied Dashboard v2 layout, treats missing incident/inventory/forecast/platform payload values as unknown instead of all-clear or zero, and protects the reconciled layout and dynamic-truth policy with focused regression tests.

### Added

- Dashboard architecture guidance defining operational-truth ownership, unknown-state handling, operator-layout protection, and the current storage-managed deployment boundary.
- Living Inventory engine with local/network discovery, inventory database, topology, service dependency graph, firmware fields, MAC/IP tracking, health scoring, and last-seen timestamps.
- Retained MQTT inventory topics under `home/infrastructure/hioc/inventory`.
- Home Assistant Living Inventory package and dashboard.
- Pi4 installer, uninstaller, and validation integration for inventory.
- Unit tests for inventory identity, health scoring, topology, and dependencies.
- Architecture, project, MQTT, Home Assistant, data model, roadmap, and decision documentation.
- Passive-by-default inventory discovery with active discovery disabled unless explicitly configured.
- Persistent MQTT client abstraction for Living Inventory publications.
- 30-minute default inventory refresh interval.
- Topology inference for intermediate infrastructure devices and integration-provided parent hints.
- HIOC Core v1.0 shared runtime with StateStore, schema validation, event bus, driver registry, capability registry, configuration service, and structured logging.
- Living Inventory internal events and capability state without changing public MQTT or Home Assistant entities.
- Dashboard v2 with Executive, Operations, Diagnostics, Inventory, Network, and Servers views built from real HIOC-owned entities.
- Release System v1.0 with version manifest, build/package/validate/install/upgrade/rollback scripts, platform status publisher, MQTT platform topics, and Home Assistant platform entities.
- Correlation Engine v2 with Core event context, topology-aware root-cause analysis, confidence scoring, lifecycle phases, duplicate suppression, and backward-compatible incident MQTT/Home Assistant output.
- HIOC Master Plan as the authoritative project charter.
- Passive known infrastructure definitions from `/home/jazofv1/hioc/config/inventory/known_infrastructure.json` to enrich Living Inventory without active discovery.

### Fixed

- Passive ARP/DHCP-only clients now retain stale observation state without generating availability incidents, while a centralized Core policy keeps infrastructure and authoritative sources operationally monitored.
- Dashboard v2 now presents active incidents using their actual Warning, Major, or Critical severity, with an Unknown fallback for unavailable severity or status.
- Release upgrades now invoke the Pi4 installer through Bash so clean source-controlled copies do not require the executable bit before installation.
- Platform-status logging now uses standard logging arguments so successful installation and upgrade runs can complete.
- Inventory now reconciles unique current or retained IP-only identities with unique current or retained MAC-backed identities without merging conflicting MACs.
- Inventory now excludes unresolved or MAC-less neighbor-cache entries from durable devices and removes legacy MAC-less records supported only by ARP provenance.

## v1.0.0-core

Initial real HIOC core foundation.

### Added

- Pi4 installer and uninstaller.
- Incident engine that reads existing Pi4 probe state and publishes structured MQTT JSON.
- Persistent active incident, incident history, summary, and timeline JSON files.
- Duplicate suppression through stable incident keys.
- Recovery detection and duration calculation.
- Home Assistant MQTT sensors for active incident, severity, status, system, summary, history count, and latest timeline event.
- Home Assistant notification automation driven from structured incidents.
- Documentation for architecture, incident model, MQTT topics, and installation.

### Notes

- This release is intentionally compatible with the existing `~/pi4-tools` installation.
- It does not replace the existing `hioc-network-probe.sh`.

- Phase 7A repository governance now owns the checksum-verified HIOC network probe source, derives PI5 probing and inventory addressing from `HOME_ASSISTANT_IP`, provides guarded deterministic deployment, and separates Dashboard V2 MQTT operational freshness from forecast trend. This entry records the earlier pending state; the Unreleased production-validation entry closes it.
