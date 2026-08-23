# HIOC Deployment

Action 9 production validation is now **PASS / COMPLETE**. It was read only and
created only its private Evidence Report at
`/tmp/hioc-pe3-action9-Bb6vGrmm`; no runtime deployment, production mutation, or
rollback occurred. Actions 1–9 are complete. Action 10 remains not started/not
prepared pending commit/push of the completion checkpoint and separate
operator-safety/governance review.

The historical Action 9 performance correction was repository governance, not
deployment. The first attempt changed no production state and created no Action 9 evidence
directory. Current Action 9 records valid performance as an observation with an
unvalidated baseline; it does not deploy code, invoke generation, or enforce the
historical four-second/incremental-RSS targets as current production limits.
Any changed Action 9 tool requires a new post-push source-governance refresh,
but no runtime deployment: Action 9 executes from release-source and continues
to verify the already-deployed validator/library identity read only.

Action 9 is not deployment. Its repository-controlled tool reads the clean
exact-commit release source, deployed validator/library, current manufacturer
artifacts, immutable dataset selection, inventory, and reviewed Action 8 PASS
evidence. Runtime content is not published or changed. The sole permitted
mutation is a private invocation-owned Action 9 Evidence Report directory under
`/tmp`. No release upgrade, installer, generator, service action, staging,
retransmission, rollback, or later action belongs to this boundary.

The bounded corrected-manufacturer-validator checkpoint is owned only by
`tools/hioc-pe3-action8-validator-deploy.sh`. It is not a release upgrade. It
requires release-source already synchronized to the approved full commit, then
proves source Git/worktree identity and the independently frozen validator blob.
An exact runtime match is `NOOP_IDENTICAL`; otherwise a safe existing validator
is backed up privately and replaced atomically at owner/group
`jazofv1:jazofv1`, mode `0700`, with file and directory durability checks.
Source synchronization and validator deployment are separate review/STOP
boundaries. Neither boundary authorizes Action 8.

The Action 8 permission correction changes the governed validator source, not
the generated production artifacts or their exact `0600` requirement.
Production runtime must not be edited ad hoc. Source synchronization, supported
runtime deployment/identity proof, and any later Action 8 attempt require their
own reviewed authorizations. The Action 8 wrapper is unchanged, so its bootstrap
script-blob trust anchor does not change.

The active PE-3 Action 8 bootstrap trust gate freezes the independently reviewed
diagnostic-retention wrapper blob
`482f83584a62be2f02b2a73af4e78b0f4ebf447a`. The prior stale identity blocked
preparation before execution. Correcting the repository contract does not
prepare or execute synchronization, deploy runtime code, require transport
staging, or authorize Action 8 or Action 9.

Action 8 no longer depends on the undeclared host utility `/usr/bin/time`.
Performance instrumentation is owned by the already-required governed Python
runtime, so no host package installation is part of deployment. The changed
wrapper requires a new source-only bootstrap identity gate after publication;
it does not require runtime deployment or transport staging.

For PE-3 Production Action 5, the authoritative runbook invokes the checked-in
`tools/hioc-pe3-action5-deploy.sh`; do not reconstruct its deployment logic in
an interactive shell. The action changes only supported runtime code and release
backup state, reports bounded sanitized evidence, and stops before dataset or
configuration actions.
Before that invocation, separately authorized Action 5A must synchronize the
clean PI3 release-source checkout to the exact approved commit and prove the
script's Git/worktree identity. Action 5A stops without deployment; Action 5B
owns the supported upgrade.

Manufacturer protection across that upgrade is semantic: empty, private,
correctly owned installer scaffolding may be created or mode-normalized, but
payload, sidecar/status, symlink, unexpected-entry, and configuration changes
are prohibited. The initial Action 5B deployment passed runtime validation but
hit the former scaffolding false positive. It remains deployed; rollback is not
recommended. A separately bootstrapped read-only Action 5C validates and closes
the existing deployment without repeating it. Its bootstrap boundary is Action
5C-A: clean exact target synchronization plus Action 5C script identity, then a
mandatory stop. Action 5C-B is prepared only after reviewed Action 5C-A PASS and
separate authorization.

Action 6 uses a separately bootstrapped repository-controlled installer. Action
6-A synchronizes and proves `tools/hioc-pe3-action6-install.sh`, then stops.
Action 6-B alone may create the immutable dataset version through a private
same-filesystem staging directory and no-replace atomic publication. It does
not activate configuration, clean transport staging, or invoke Action 7.

Action 7 uses the same split trust boundary. Action 7-A performs only clean
release-source synchronization and exact identity proof for
`tools/hioc-pe3-action7-activate.sh`, then stops. Action 7-B is separately
authorized and changes only the runtime `MANUFACTURER_DB_PATH` setting after
proving the exact Action 6 immutable dataset. It preserves unrelated
configuration, creates a private durable backup when mutation is needed,
publishes atomically, and does not deploy code, reload services, touch transport
staging, modify the immutable dataset, generate sidecars/status, or invoke
Action 8.

Action 8 is not a release deployment. Its repository-controlled wrapper invokes
the already deployed manual manufacturer generator only after source/runtime,
configuration, installed dataset, inventory, output, protected-state, and
evidence gates pass. Because PI3 currently predates the wrapper, a separate
source-synchronization/script-identity bootstrap must pass before the mutating
action can be considered. The bootstrap only fast-forwards the clean release
source to the explicitly supplied and validated operator-approved full 40-hex
post-push commit, proves exact script identity, and stops. Action 8
does not use `release/upgrade.sh`, alter deployed code, or chain Action 9.
It creates its own private temporary evidence directory only after deployment,
source, runtime, configuration, installed dataset, inventory, and output
preconditions pass; no Action 5/5C evidence directory is an input.
Transport staging is transient pre-install state and is not consumed or required
after Action 6 immutable publication and Action 7 activation. Its absence does
not authorize recreation or retransmission and does not weaken installed-dataset
identity validation.

Action 8 generator failures now retain a private, structured failure artifact
without deploying code or exposing raw generator streams. The wrapper publishes
performance first and `generation-failure.json` last, records bounded root-cause
and output-mutation evidence, removes raw captures, and stops. This repository
change does not authorize synchronization, deployment, generation, or Action 9;
the changed wrapper requires a separate post-push bootstrap identity gate.

## Document Ownership

This document owns the repository-to-production workflow, source and runtime boundaries, operator responsibilities, synchronization expectations, and production acceptance boundary. Detailed commands remain in [INSTALL.md](INSTALL.md) and packaging mechanics remain in [RELEASE.md](RELEASE.md).

## Deployment Boundaries

| Boundary | Role |
| --- | --- |
| Windows development repository | Authoritative development workspace; changes are validated, committed, and pushed here. |
| GitHub `main` | Shared authoritative Git history. |
| `/home/jazofv1/hioc-release-source` | PI3 Git checkout used for release validation and supported deployment execution. |
| `/home/jazofv1/hioc` | Non-Git production runtime containing deployed files and persistent runtime data. |

The supported flow is:

```text
Windows repository -> GitHub main -> PI3 release source -> validated upgrade -> non-Git runtime
```

Codex operates only in the Windows repository. The operator performs PI3 synchronization, deployment, rollback, and production evidence capture. Direct Git operations inside `/home/jazofv1/hioc` are unsupported.

## Supported Workflow

1. Validate repository changes.
2. Update the Master Plan and affected focused documentation.
3. Commit related code and documentation together.
4. Push `main` and verify a clean Windows working tree.
5. Operator verifies a clean, non-divergent PI3 release-source checkout and fast-forwards it to `origin/main`.
   When a governed production script may be absent or older on the target, this
   synchronization and script-identity proof is a separate authorization gate.
6. Operator runs `release/validate.sh` and the supported `release/upgrade.sh` when runtime files changed.
7. Operator runs `/home/jazofv1/hioc/pi4/validate_pi4.sh` and any checkpoint-specific validation.
8. Operator captures production evidence and commits required closeout documentation.

Documentation-only source changes are excluded from the deployed runtime by `pi4/install_pi4.sh`. Whether to run a production upgrade for such a commit must follow the operator handoff and the established release workflow; do not copy documentation ad hoc into the non-Git runtime.

## Preservation and Recovery

Upgrade preserves `config`, `state`, `history`, `logs`, and `backups`. Supported rollback uses `release/rollback.sh` and excludes `.git`. Source recovery comes from GitHub, the release-source checkout, or an approved release package. Runtime recovery comes from release backups and preserved persistent data. See [RECOVERY_BASELINE.md](RECOVERY_BASELINE.md).

## Production Validation Expectations

Production acceptance uses the deployed validator, cron inspection, fresh state, logs, generated artifacts, and checkpoint-specific evidence. A successful repository test does not prove production behavior. A production observation does not prove an internal implementation invariant unless the artifact exposes it.

## Operations Acceptance Standard

A release is not complete until repository documentation answers what exists, why it exists, how it runs, how it is validated, and how it is recovered without requiring SSH discovery. The actionable checklist is authoritative in [HIOC_MASTER_PLAN.md](HIOC_MASTER_PLAN.md#operations-acceptance-standard). Any required production verification must be captured in an Evidence Report and committed back to the repository.
