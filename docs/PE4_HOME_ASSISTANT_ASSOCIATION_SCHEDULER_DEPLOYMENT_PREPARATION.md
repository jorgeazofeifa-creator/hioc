# Home Assistant Association Scheduler Deployment Preparation

Repository-only preparation. Scheduler installation and production execution NOT AUTHORIZED.
Independent Production Acceptance remains PASS/CLOSED. PI3 source review at predecessor
826608b40d5248c67742a17fc95a6e7612981df1 is OPERATOR_SUPPLIED; Codex did not access PI3.

## Frozen architecture and canonical representation

Preserve JAZOFV1_USER_CRONTAB_DEDICATED_SHORT_LIVED_JOB, HIOC_PE4_HA_ASSOCIATION,
5,35 * * * *, 1800 seconds. Inventory uses installer */30 slots; five-minute offset
is ordering intent only. Existing fresh valid canonical inventory/input gates remain authoritative.
First run is FIRST_SCHEDULED_SLOT_WITH_VALID_FRESH_CANONICAL_INVENTORY_NO_FORCED_BOOT_NETWORK_RUN.
Retry NEXT_SCHEDULED_INVOCATION_ONLY; overlap INTERNAL_DEDICATED_NONBLOCKING_FLOCK_MANUAL_AND_CRON_SAME_LOCK
at state/inventory/associations/.home_assistant.lock. No extra external overlap lock.
Separate short-lived process, no PassiveNetworkDriver attachment, no inventory dependency on exit.
No systemd service/timer, forced boot run, manual test run or immediate adapter execution.

Canonical insertion is exactly UTF-8/LF:

```cron
# HIOC_PE4_HA_ASSOCIATION
5,35 * * * * /home/jazofv1/hioc/runtime/pe4/active/bin/python -I -B /home/jazofv1/hioc/pi4/bin/hioc-home-assistant-association.py >/dev/null 2>&1
```

release/install.sh delegates to pi4/install_pi4.sh; upgrade and rollback invoke that same installer.
The installer uses user crontab -l and crontab - with standalone schedule/command lines. It has
no PE-4 identity marker convention. OPERATIONS documents no redirection on existing jobs and
unverified host handling of output. Therefore choose the smallest explicit standalone job-ID
comment and /dev/null redirection for both streams, avoiding new logs or cron mail. Absolute
accepted runtime plus -I -B replaces shebang reliance; adapter owns its existing overlap lock.
The unrelated platform line remains exactly:

```cron
17 3 * * * flock -n /tmp/hioc-platform-status.lock /home/jazofv1/hioc/pi4/bin/hioc-platform-status.py
```

Generic installer is not reused as an execution path: it removes blank lines/replaces other
jobs and manually executes engines. tests/test_release.py governs release/runtime ownership,
not a scheduler compare-and-swap or transactional rollback contract. The narrow new tool reuses
crontab stdin installation but neither normalization nor immediate execution.

## Governed future tool

tools/hioc-pe4-ha-association-scheduler-deploy.py accepts only exact source commit and
--install-scheduler-authorized. Target nutandpihole/jazofv1, real/effective UID/GID; fixed source,
main/origin equality, clean tree, exact parent/subject/no active Git operation. It verifies its
own hash, predecessor bound identities, current committed bytes and acceptance PASS/CLOSED before
imports. Master Plan and acceptance-test predecessor hashes remain historical because lifecycle
assertions evolve; their current bytes must still match the exact authorized commit.
Reuse only manual_validate.deployment_integrity and runtime_probe with deployed NativeFS; never
prerequisites(), credential validator, adapter/reconciler/main or acceptance execution. Probe
runs accepted interpreter with -I -B and pure runtime inspection, not the adapter entrypoint.
Exact committed deployment/journal/config/module/entrypoint/runtime governance remain mandatory.

Read only user crontab and the previously governed /etc/crontab, /etc/cron.d, /etc/systemd/system,
and user .config/systemd/user surfaces. Bounds 65536 bytes and 15 seconds per crontab process,
4096 scheduler objects. Reject unsafe roots/objects and association indicators including job ID,
malformed entries, duplicates or unexpected service/timer. Missing platform line, empty crontab,
invalid UTF-8, NUL, CR and oversize fail before mutation; never adopt or repair existing jobs.
Unrelated UTF-8 bytes, comments, whitespace and blank lines remain an exact prefix. Append only
one LF if a prior final LF is absent, then the canonical two-line block. No environment, mail,
unrelated comments or scheduler lines are rewritten; existing adapter target/environment gates
remain authoritative and may reject unsuitable input or inherited environment.

Scheduler surface reads reuse the source-bound deployment NativeFS helper with pinned directory
handles, no-follow traversal, owner/mode/ACL checks and a 64 KiB file bound. Child symlink
targets are inspected without following them; redirected scheduler roots are rejected.
The scan stops above 4,096 objects. Synthetic filesystems exercise the actual scanner
without reading real scheduler surfaces.

## Mutation and failure contract

Keep exact prior bytes and candidate only in memory. Emit hashes, finite states and false
activity flags; never dump crontab, process stderr, private state or credentials. Immediately
before installation revalidate source/runtime/deployed identities and unchanged scheduler
surfaces, then exact crontab reread. One /usr/bin/crontab - stdin call, no shell or temp file.
Only rc0 plus exact candidate reread, one marker/job, preserved platform/unrelated bytes,
unchanged guard state and final reread is PASS. Never retry installation automatically.

A failed/ambiguous/timeout return does not prove prior preservation. Reread if possible and report
CANDIDATE_OBSERVED, PRIOR_OBSERVED, OTHER_OBSERVED or UNKNOWN, always FAIL/manual review for
nonzero or unknown return. Post-read/check failure remains FAIL/manual review; job may already
be installed and may run at a natural slot. Crash/interruption requires review, never rerun the
installer blindly. There is no durable prior-byte journal or restart/resume installation path.
No automatic rollback/removal is implemented. Any later removal requires separate authorization,
a secured exact prior crontab and proof of current mutation state; removal cannot undo a job that
already ran. This checkpoint performs no rollback.

crontab provides no compare-and-swap; rechecks cannot eliminate concurrent editor races.
Future authorization requires an exclusive operator crontab maintenance window. Preservation
is relative to the last verified preimage, not a claim of atomic isolation against other editors.
No new external adapter overlap lock is introduced to pretend to solve that race.

Installation does not invoke the adapter. Future scheduler authorization permits recurring
natural 5/35 slots subject to adapter gates, not an extra manual second invocation. Second
Adapter Execution remains NOT AUTHORIZED as a manual action. The first natural slot can occur
before installation verification completes; uncertain outcomes require immediate manual review.

## Lifecycle and handoff

Scheduler Deployment Preparation PASS/CLOSED; Scheduler Deployment NOT STARTED / PREPARED FOR
SEPARATE AUTHORIZATION. Acceptance PASS/CLOSED; Attempt 1 failed capture/history immutable;
Attempt 2 PASS. Original ephemeral revalidation UNAVAILABLE and limitation RECORDED unchanged.
Second Adapter Execution NOT AUTHORIZED; Public Projection DEFERRED; PE-4 NOT COMPLETE;
Phase 7A ACTIVE; rollback NOT PERFORMED. No PI3/PI5/HA/credential/production/scheduler access here.
Next action: PI3 source synchronization to the preparation commit ONLY, STOP and independent
review. A short future system Python -I -S -B command invokes this committed source-only tool
under its exact env-i environment. Do not run it until separately authorized.

## Local validation

CPython 3.12.14 native Windows, -B, local synthetic fixtures only. The established regression
method limits PATH to Windows system/PowerShell, Git cmd and Python, removes HIOC_TEST_SHELL,
and requires no bash/sh. Focused scheduler tests: 77 run / 77 passed / 0 skipped / 0 failures /
0 errors. Relevant PE-4 discovery: 1,400 run / 1,384 passed / 16 skipped / 0 failures / 0 errors.
Final full repository discovery: 2,125 run / 2,078 passed / 47 skipped / 0 failures / 0 errors.
No timing flake occurred. Initial full regression before scanner hardening also passed:
2,119 run / 2,072 passed / 47 skipped / 0 failures / 0 errors. Initial relevant PE-4 passed:
1,394 run / 1,378 passed / 16 skipped / 0 failures / 0 errors.

An expanded parser privacy fixture initially had 71 run / 70 passed / 1 error because
CPython 3.12 raises argparse.ArgumentError directly with exit_on_error=False. Corrected the
new fixture's failure-type expectation to recognize both supported parser failures and still
prove stderr is empty; the CLI emits finite sanitized evidence for either type. Corrected
focused run passed 71/71, followed by final scanner coverage 77/77. No failure was suppressed
and no timing threshold changed. Historical regressions/records remain immutable.

All 64 predecessor source bindings verified. Existing production, release and historical
governance files remain byte-identical; syntax and git diff --check pass. Final validation
metadata, closed schema and direct-test launcher ordering were followed by a focused rerun.
