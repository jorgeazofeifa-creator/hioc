# PE-4 Independent Production Acceptance Preparation

Preparation PASS/CLOSED. Independent Production Acceptance execution NOT STARTED /
PREPARED FOR SEPARATE AUTHORIZATION. Repository-only preparation under
369134ff77d062ba0aeebc3db98e04662f2f6fed; its parent is
96150db5e28b065a587ae09ce0522ef6bd66f3be and subject is
`PE-4: close durable post-run reconciliation`. Master Plan remains authoritative.

## Derived architecture and sufficiency

Existing identity-bound read-only definition functions are sufficient. No new tool is required
or implemented. This is a governed function invocation sequence, not permission to run any
existing CLI main. The reconciler CLI's source gate applies to its historical predecessor;
its main must not be rerun. Deployment main mutates production, deployment prerequisites read
a credential, and platform-status main writes state and publishes MQTT. All are excluded.
The source-only manual wrapper's protected_snapshot/deployment_integrity/runtime_probe/scheduler,
the reconciler's private_state/compatibility_state, deployment NativeFS read-only methods,
and adapter pure schema/privacy/inventory validators cover the required current-state proof.
Compatibility assess/summarize are pure; refresh_status is prohibited.

No HA network or credential content/metadata access is needed: this accepts installation,
security and the existing published snapshot, using the already accepted one live execution.
It does not prove present HA reachability, current HA registry freshness, future successful
scheduled cycles, token validity today or current live service health. Operational readiness
means the existing subsystem satisfies prerequisites for separately preparing a scheduler;
it does not authorize enabling one or mark PE-4 complete.

## Exact future invocation sequence (separate authorization required)

1. Require Linux nutandpihole, real/effective jazofv1 user/group, fixed sanitized environment,
   source root /home/jazofv1/hioc-release-source and production root /home/jazofv1/hioc.
   Require the exact independently reviewed preparation commit, direct parent 369134ff,
   subject `PE-4: prepare independent production acceptance`, clean main/origin equality,
   0/0 and no Git operation. No fetch/pull during acceptance. Verify preparation canonical
   record/schema and every source binding BEFORE importing definition modules. The Master
   Plan binding is the immutable predecessor document, not the newly updated current bytes.
2. Use system Python -I -S -B; verify and load only the bound definition modules by absolute
   source path. Never call their main methods. Validate source bytes also against Git blob
   identities in the reviewed preparation commit. No PYTHONPATH or ambient import fallback.
3. Set deployment.LIMIT=manual.LIMIT (16 MiB) and create deployment.NativeFS(manual.HOME,
   reviewed jazofv1 uid/gid). Invoke only read/info/check_directory/names/security; never
   mkdir/add/replace_config/lock/deploy/preflight/prerequisites. The source closure record
   supplies the manifest and immutable committed historical report supplies expectations.
4. Run before=manual.protected_snapshot(fs,deployment_closure,deployment,include_inventory=False).
   This calls deployment_integrity, runtime_probe and scheduler: five existing dependencies,
   nine targets (three code/six governance), COMMITTED intent/commit/config journal, exact
   candidate config and unique frozen endpoint, directory/lock security, active runtime,
   accepted CPython/websockets/customization and platform cron/scheduler absence. The accepted
   interpreter's local -I -B identity probe is permitted; the adapter is never started.
5. Call reconciler.private_state(fs,deployment,manual,adapter,historical_report) and
   reconciler.compatibility_state(fs,manual,compatibility,historical_report). Do not call
   reconciler.main/source_gate/source_authority/reconcile_checks. Private state schema 1.1
   and semantic validation prove unique active keys, timestamps, cardinality, relationships,
   privacy, diagnostic/count agreement, empty history and clean txn/done namespace.
   Compatibility validates the recorded map/capabilities/version and pure assessment/summary;
   no new HA compatibility probe or compatibility publication occurs.
6. Securely read state/inventory/inventory.json through fs.read; require present, bounded,
   regular single-link/no-symlink/no-ACL governed filesystem security. Call
   adapter.validate_inventory(raw,current_UTC). This validates current schema 1.0, unique
   dev_ IDs, valid MAC values and freshness without gating on liveness/health. Keep raw data
   and indexes in memory only. Current canonical inventory can evolve independently; do not
   reconstruct execution-time equality, recompute HA matching or assert every historical
   association is still present in current inventory. Frozen code preserves HIOC authority.
7. Repeat private-state and compatibility validation and protected_snapshot; require the
   protected snapshot equals before. Recheck private/compatibility raw bytes and security
   against the first acceptance read for a coherent acceptance interval. Recheck source
   authority and all imported identities. Concurrent protected/private/compatibility drift
   fails closed; no retry, lock acquisition, cleanup or automatic remediation. Inventory
   freshness/semantics are a current observation, not a whole-tree stability claim.
8. Emit only the finite canonical sanitized report below, with no exception text/stderr.
   PASS requires every gate PASS, FAILURE_STAGE=NONE, counts agree, protected stability,
   all activity false and mandatory historical limitation intact. UNKNOWN is not success.
   Nonzero return on any failure; stage is finite. STOP for independent evidence review.

## Exact surfaces, security and snapshot counts

Use deployment closure's exact dependencies/deployed_targets, and journal
backups/pe4-ha-association-deployment-v1/{intent.json,committed.json,config-prior,config-candidate}.
Config is config/hioc.conf. Private directory state/inventory/associations is jazofv1:jazofv1
0700; .home_assistant.lock and home_assistant.json are 0600, regular single-link, no symlink
or ACL. Exact manifest owner/group/modes apply; dependency policy allows root/operator owners,
no special/group/world write. Descriptor-bound no-follow reads reject inode/name/security drift.
Only the exact accepted runtime active pointer is a permitted symlink. Ordinary read atime is
outside the content/namespace/mode/owner/group/mtime comparison; no atime restoration is attempted.

The fixed accepted runtime is runtime/pe4/environments/cpython311-websockets16.1.1-lock-v1;
active must resolve exactly there. Runtime/customization validation uses the already corrected
pure local probe, never deployment prerequisites or credential validation. Platform-status
artifact must match its governed SHA; no platform-status execution occurs. Preserve exactly
`17 3 * * * flock -n /tmp/hioc-platform-status.lock /home/jazofv1/hioc/pi4/bin/hioc-platform-status.py`.
Inspect existing user cron, /etc/crontab, /etc/cron.d, /etc/systemd/system and
/home/jazofv1/.config/systemd/user for association schedules using bound scheduler logic.

25 associated / 170 review-only / 26 rejected / 8 unmatched / 0 history and recorded HA 2026.9.4
are exact expectations for acceptance of this existing first published state only. They are
historical snapshot values, never permanent architectural constants. Internal agreement is
also required. A different otherwise valid snapshot fails this checkpoint for separate review;
no adapter rerun is authorized to refresh it. No private IDs, counts-derived private mappings
or private file digests enter retained evidence.

## Durable sanitized evidence contract

Before separately authorizing execution, the operator must prepare and independently review
secure WORKSTATION capture at
`C:\Users\JorgeAzofeifaCastill\AppData\Local\HIOC\evidence\pe4\independent-acceptance\<authorized-commit>\<unique-run-id>`.
This is outside production. Owner AzureAD\JorgeAzofeifaCastill; protected Windows DACL permits
only operator, SYSTEM and Administrators full control; no other readers or reparse points.
No production evidence file is created, touched, chmodded or moved. No /tmp-only evidence.

Capture bounded stdout directly to a new exclusive run directory, discard stderr, and reject
oversize/malformed/noncanonical/private output. validation.json is UTF-8, ASCII escapes, sorted
keys, compact separators, no NaN and one trailing LF, maximum 4096 bytes. The preparation record
embeds its closed report_schema and exact allowed_fields: target/source/mode, finite gate results,
counts-agreement/stability, limitation, activity false, result and failure stage only. No free text.
PASS semantics additionally require all gates PASS and stage NONE; schema alone is insufficient.

manifest.json maximum 4096 bytes is a closed canonical object with exactly schema_version='1.0',
source_commit (40 lower hex), validation_sha256 (64 lower hex) and validation_bytes (integer 1..4096).
Publish manifest LAST only after validation; flush durable files/directory using the approved
Windows capture mechanism, reopen and verify length/hash/canonical schema and security. No overwrite,
append, fallback or automatic retry. Incomplete capture cannot support acceptance. Capture security,
publication/durability or return-code failure is FAIL even when inspection gates passed.
Retain both files through independent review, repository evidence closure and later revalidation;
no automatic deletion. After separate review, persist canonical sanitized successor repository
governance evidence with exact capture identities. Hashes do not recover lost bytes.

Exclude tokens, raw registries, device/entity/config-entry IDs, household/area names, MACs,
private association/inventory content or their digests, credentials and raw exception/stderr text.
Credential provisioning closure is bound as historical security authority without opening its
production credential hierarchy. No claim of renewed credential readability/authentication.

## Immutable history and lifecycle

OPERATOR_SUPPLIED_PRODUCTION_EVIDENCE: the supplied source synchronization to 369134ff passed;
Codex did not observe it. Exact sanitized report is preserved in the preparation record.
Historical adapter count=1 and PASS, wrapper FAIL / MANUAL REVIEW REQUIRED and
PRODUCTION_FILES_UNCHANGED=FALSE remain unchanged. ORIGINAL_EPHEMERAL_EVIDENCE_PRESENT=FALSE,
REVALIDATION=UNAVAILABLE, LIMITATION=RECORDED, disappearance cause UNKNOWN;
EXECUTION_TIME_COMPARISON_RECREATED=FALSE and HISTORICAL_EVIDENCE_RECREATED=FALSE.
No FULL_ORIGINAL_ARTIFACT_REVALIDATION or ZERO_EVIDENCE_GAPS claim is made.

Preparation PASS/CLOSED; acceptance NOT STARTED / PREPARED FOR SEPARATE AUTHORIZATION;
second adapter execution NOT AUTHORIZED; scheduler NOT STARTED; projection DEFERRED;
PE-4 NOT COMPLETE; Phase 7A ACTIVE; rollback NOT PERFORMED. Next: PI3 source synchronization
to preparation commit ONLY, STOP, independent source review, then separate acceptance authorization.
Codex performed no PI3/PI5/HA/credential access or production execution/mutation.
