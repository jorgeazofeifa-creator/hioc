# PE-2.1 Asset Foundation Evidence

Status: **COMPLETE - PRODUCTION VALIDATED**

## Repository baseline

Implementation began on clean `main` at approved implementation-design commit
`b2b69e50e0583fe00415016b58c1fd5ad1bf8235`, equal to `origin/main`, with no
merge, rebase, cherry-pick, revert, or bisect active. Work remained inside the
authoritative Windows repository. Production was not accessed or changed.

## Implementation summary

PE-2.1 implements the approved private, stable-ID-keyed Asset foundation. The
subsystem is local and operator-invoked only. It provides a strict store/status,
governed CLI, read-only validator, dedicated bounded lock, optimistic revisions,
validated pre-mutation backups, atomic restore, orphan context, sanitized output
and failure isolation. It adds no daemon, schedule, publication or consumer.

New implementation files:

- `pi4/lib/hioc/assets.py`
- `pi4/bin/hioc-assets.py`
- `pi4/bin/hioc-validate-assets.py`
- `tests/test_assets_schema.py`
- `tests/test_assets_store.py`
- `tests/test_assets_cli.py`
- `tests/test_assets_orphans.py`
- `tests/test_assets_release.py`

Bounded integration changes are limited to `pi4/install_pi4.sh` and
`pi4/validate_pi4.sh`. The installer creates restrictive directories and makes
the two commands executable without initializing state. Runtime validation is
conditional on either Asset artifact existing and never repairs or writes.
Existing release upgrade/rollback exclusions already preserve `state/` and
`backups/`, so release scripts required no modification.

## Schema and normalization evidence

The implementation owns closed version `1.0` schemas for `assets.json` and
`assets_status.json`. Tests prove empty/one/multiple records, fixed key order,
lexical Asset order, key/embedded-ID agreement, unknown-field and unsupported-
version rejection, RFC 3339 UTC timestamps, count consistency, revisions and
deterministic UTF-8 serialization.

Normalization tests prove NFC, outer whitespace, empty-to-null, single-line
controls, 128/128/256 limits, notes CRLF normalization, internal blank lines,
trailing whitespace handling, eight-line/1,024-code-point limits and tab/control
rejection. Duplicate friendly names remain permitted by schema.

## CLI contract evidence

The CLI implements only `initialize`, `list`, `show`, `set`, `clear-field`,
`remove`, `validate`, `backup`, and `restore`. Tests prove deterministic JSON,
default value/raw-ID redaction, usage/not-found/revision/privacy exit codes,
idempotent initialization, create/update/no-op, clear-last-field removal and
interactive sensitive-display gating. Unexpected exceptions are sanitized as
`INTERNAL_ERROR`/70 without stack traces.

## Lock and transaction evidence

Production locking uses shared/exclusive `fcntl.flock` on
`/tmp/hioc-assets.lock`, a five-second bounded wait, kernel crash release,
non-reentrancy, no stale-file deletion and no inventory lock. Windows test
portability retains the same service boundary without pretending to test Linux
kernel contention.

Transactions validate before write, use a unique same-directory temporary file,
flush/fsync, mode `0600`, revalidate, atomically replace and fsync the directory.
Tests prove replacement success/failure, prior-byte preservation and temporary
cleanup. A committed store is not silently rolled back when status writing fails.

## Backup and restore evidence

Backups use the approved UTC microsecond/SHA-256 filename, exact prior bytes,
`0700` directory, `0600` file, fsync and post-write digest/schema validation.
Tests prove mutation/no-op behavior, explicit backup, exact bytes, digest
rejection, basename/traversal/absolute-path rejection, valid restore and
pre-restore backup. There is no pruning or retention implementation.

## Orphan and failure-isolation evidence

Asset reads only `state/inventory/inventory.json` for orphan context. Missing or
invalid inventory yields degraded/unknown without fabricated counts. Existing
orphaned records remain editable; creation requires inventory proof or explicit
`--allow-orphan`. Tests prove current/orphan counts, malformed/missing context,
continued editing and byte-identical inventory before/after Asset mutation.

No Asset import was added to inventory or enrichment. Malformed Asset state
fails closed in the Asset subsystem and is not repaired. Status and routine
outputs contain no Asset values. No Asset condition creates health, liveness,
observation or incident semantics.

## Release preservation

Source-contract tests prove installation exposes the CLI/validator and creates
restrictive paths without cron. Upgrade continues to exclude both `state` and
`backups` from replacement/backup copying and uses no deletion. Rollback uses no
deletion and cannot remove the preserved Asset store or Asset backup directory.
The runtime validator invokes only the read-only Asset validator when artifacts
exist.

## Protected invariants

Repository diff and focused/full regression prove no changes to:

- `inventory.py`, stable identity, canonical-address selection or serialization;
- PE-1 enrichment behavior or sidecars;
- MQTT modules or payload contracts;
- Home Assistant packages/entities or dashboards;
- incidents, health, liveness or observation status;
- topology or service ownership;
- public inventory schema or values;
- cron, services, timers or daemon behavior.

## Validation results

- New PE-2.1 suites: **27 passed**.
- Focused PE-1, inventory, identity, canonical and release suites:
  **197 passed, 1 platform-dependent skip**.
- Full repository regression: **304 passed, 7 expected platform skips** after
  setting the governed Git Bash test path.
- Python compilation: **PASS**. Shell syntax and `release/validate.sh`: **PASS**
  (the release wrapper's own Git Bash environment reported its expected Python
  skip; compilation had already passed with the bundled repository runtime).
- Documentation links, whitespace, secrets and complete diff review: **PASS**.

## Performance

Repository-host synthetic microbenchmarks measured: initialization/empty
validation 63.474 ms, mutation 50.786 ms, list 5.711 ms, show 7.504 ms, backup
32.159 ms, restore 53.144 ms and orphan calculation 0.040 ms. Windows cannot
measure production `flock` contention; the five-second bound is source- and
contract-tested. These values are informational rather than PI3 proof. No
inventory call path, unbounded recursion, network scan or automatic Asset scan
was introduced. Final measured values are recorded in the commit handoff.

Approved PI3-class targets remain: read <=1 second, mutation <=3 seconds,
backup/validation <=2 seconds and lock wait <=5 seconds. Production measurement
is pending the separately authorized deployment/validation checkpoint.

## Warnings

- Repository-host Windows cannot exercise Linux kernel `flock`, POSIX ownership,
  directory fsync or production hardware timing; Linux behavior is source- and
  mock-tested, with production proof pending.
- Local backups do not provide off-host disaster recovery. Retention and
  off-device transport remain explicitly deferred.

## Repository decision

**PASS** for PE-2.1 executable repository implementation, subject to the final
full validation recorded with the local commit. Production deployment and
production validation remain pending. No production Asset values or state exist.

## Governed production operator

Production deployment/validation is prepared as the repository-controlled
`tools/hioc-pe2-production-validate.sh`. A versioned script is required because
the governed procedure includes repository synchronization, Git-object artifact
identity, protected pre/post evidence, supported deployment, synthetic revision/
backup/restore/rejection/lock transactions, privacy scans, invariant comparison,
performance thresholds, exact cleanup, reporting and non-automatic rollback.
Tests enforce its target, Git, artifact, privacy, command and rollback boundaries.
At preparation time the operator script had not been executed; the following
section records the later first production attempt.

## First production attempt and validator correction

The first governed PI3 attempt synchronized operator-governance commit
`d138aa931b6cadc3fdf943e9f35947dc342e1b63` and completed the supported upgrade.
Release backup `/home/jazofv1/hioc/backups/release-upgrade-20260803-205823` and
installer backup `/home/jazofv1/hioc/backups/install-20260803-205823` were
created. The deployed PE-2.1 implementation remains in place.

The run stopped before synthetic transactions because the validator conflated
Git tree modes with runtime permission policy. Forensic evidence proved all five
approved deployed artifacts matched their Git-derived SHA-256 byte-for-byte.
Git modes `100644`/`100755` express repository executable classification; they
do not require public runtime modes `0644`/`0755`. The installer deliberately
applied private modes `0600` to the library/non-runtime installer and `0700` to
the CLI/validators. Those modes satisfy the approved privacy contract.

The failure-report writer separately interpolated lowercase JSON `true`/`false`
into Python source, causing `NameError` and preventing the sanitized report.
These are **VALIDATOR CONTRACT DEFECTS**, not deployment, implementation,
installer, schema, privacy, or artifact failures. No rollback was performed; the
generic rollback recommendation is withdrawn.

Correction introduces one authoritative `pi4/config/pe2_artifacts.json` runtime
permission contract used by installer and validator, separates content identity
from permission/ownership errors, renders reports through validated JSON stdin,
and adds `--revalidate-existing-deployment`. Revalidation creates new evidence,
does not call `release/upgrade.sh`, and does not deploy. PE-2.1 remains open
pending corrected production revalidation; PE-3 is not started. Historical
failed evidence remains `/tmp/hioc-pe2-production-validation-j9ZehSdD`.

## Incident-invariant validator correction

Corrected revalidation completed artifact, permission, Asset transaction,
backup/restore, cleanup, final semantic-equality, and public checks before it
failed because live `active.json` was required to retain an identical digest.
Evidence `/tmp/hioc-pe2-production-validation-pqOq652B` showed unchanged history
and summary digests; sanitized forensic comparison found zero changed
nonvolatile fields. No raw incident content is recorded here.

This is a **VALIDATOR CONTRACT DEFECT**. Active lifecycle, severity, status,
title, summary, and telemetry can move through normal scheduled Incident Engine
activity; history and aggregates can also advance. Digest inequality alone does
not establish PE-2 causation. The rollback recommendation is withdrawn: cleanup
and final Asset equality preceded incident comparison, and no causal regression
was demonstrated.

The governed comparator now validates JSON and protected shape, prohibits Asset
fields and synthetic values, and structurally proves Asset-to-incident isolation.
Git history proves implementation commit `dd6f40b113fe8a395babc8bfb2325262879b8454`
did not modify incident engines. Valid live differences are operational drift;
uncertainty has rollback false. Only a demonstrated protected regression is
rollback-eligible. PE-2.1 remains deployed and repository validated but open
pending a new validation-only Evidence Report. PE-3 is not started.

The prior run reached synthetic removal and final current-state semantic equality,
but stopped before its later validation-created backup cleanup loop. Synthetic
backup residue therefore cannot be disproved from repository evidence. The next
revalidation checks both current Asset state and every readable Asset backup
before mutation. Any reserved-ID residue stops validation without deleting or
overwriting it; the sanitized result reports counts only.

## Synthetic validation backup residue cleanup

The corrected revalidation stopped safely at its residue precondition. Read-only
production evidence proves the current Asset store is valid schema `1.0`, empty,
private mode `0600`, correctly owned, and lacks the reserved synthetic ID. Asset
status is private and correctly owned. The mode-`0700` backup directory contains
six identified synthetic-only backups from prior validation. Each has one record,
none contains real Asset state, and no malformed backup was found. Classification
is **BACKUP_RESIDUE_ONLY**; rollback remains false.

This is a **VALIDATION CLEANUP ORDERING DEFECT**. Created backup basenames were
tracked, but cleanup followed public, incident, privacy, and performance checks.
The incident failure therefore occurred after current-state restoration but
before backup cleanup.

One-time cleanup uses the committed exact-basename/SHA-256 manifest and
`tools/hioc-pe2-clean-synthetic-backups.py`. Committing bounded forensic names
avoids transcription and dynamic-discovery risk; the manifest contains no Asset
values and is not retention policy. The tool validates the complete set before
deleting anything and never uses wildcard discovery.

Future validation classifies explicitly tracked current-run backups immediately
after synthetic removal and final Asset equality, records sanitized evidence,
and removes only validated synthetic-only current-run backups before unrelated
invariants. PE-2.1 remains deployed and open pending one-time cleanup followed
by separate final revalidation. PE-3 is not started.

## Final production validation and checkpoint closure

PE-2.1 was deployed through the supported release upgrade from implementation
commit `dd6f40b113fe8a395babc8bfb2325262879b8454`. Release backup
`/home/jazofv1/hioc/backups/release-upgrade-20260803-205823` and installer
backup `/home/jazofv1/hioc/backups/install-20260803-205823` were created. All
deployed implementation artifacts matched approved Git objects byte-for-byte,
and runtime permissions matched the restrictive deployment policy.

The governed one-time cleanup validated and removed six synthetic-only backups
without changing current Asset state or status and without touching a real Asset
record. Final validation-only revalidation used validator-governance commit
`6bb9e158f9d51d9e43b042950620e0c4aba03eb5` and produced sanitized evidence at
`/tmp/hioc-pe2-production-validation-CtZ4WHUN`.

Asset store/status validation; synthetic creation, update, no-op, stale-revision
rejection, backup, restore, removal, cleanup; final semantic equality; privacy;
performance; and all protected invariants passed. All current-run synthetic
backups were removed. Public inventory, identity, canonical address, health,
liveness, observation status, MQTT, Home Assistant, dashboards, incident
history, and incident summary remained protected. Active incident movement was
`INCIDENT_OPERATIONAL_DRIFT`; no PE-2 causal regression was demonstrated. No
Asset metadata entered incidents, MQTT, public inventory, logs, or evidence.
Rollback was neither performed nor required.

The production-validation history contained four governance defects: Git modes
were mistaken for runtime permission requirements; lowercase JSON booleans were
interpolated into generated Python; live active incident state was treated as
immutable; and synthetic backup cleanup followed unrelated invariants. All were
validator-governance defects, not Asset implementation defects. Deployed Asset
implementation files remained unchanged throughout correction, defect-based
rollback recommendations were withdrawn, and the final corrected validator
passed.

Decision: **PE-2.1 - COMPLETE - PRODUCTION VALIDATED**. Phase 7A remains in
progress. PE-3 remains not started.
