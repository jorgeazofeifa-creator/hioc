# PE-4 Home Assistant Association Public Projection Deployment Preparation

This checkpoint prepares repository source only. Preparation PASS/CLOSED is subject
to the recorded regression checks and does not authorize deployment. Public
Projection Deployment NOT STARTED / PREPARED FOR SEPARATE AUTHORIZATION;
Production Execution NOT STARTED. PE-4 NOT COMPLETE; Phase 7A ACTIVE;
PE-5 NOT STARTED; rollback NOT PERFORMED.

The parent is 6bfb689fc9e49de5d7ae17267f2b389e13f0bc1e, subject
`PE-4: close public projection POSIX validation`, whose parent is implementation
c762745b428b28518cf4415f7399ff2cacb70c66. POSIX validation PASS/CLOSED remains
OPERATOR_SUPPLIED. Codex did not observe or repeat that execution.

## Baseline authority and separate gates

PRE-DEPLOYMENT PI3 BASELINE VALIDATION NOT STARTED / REQUIRED BEFORE DEPLOYMENT.
Repository evidence establishes additive modules and schemas as 0644 owned by
jazofv1:jazofv1 in the accepted association deployment. It does not establish the
current production engine bytes, numeric IDs, inode or mode. The reviewed old
engine candidate is the engine at eda070d4b06ccd7f562a74e1cb6b42cb5c630d67,
SHA-256 06fa6d326ec75df92f0902da4360065b7767ee2a9848d7877c00c145d9d00f42.
This is not a claim that production currently matches. The read-only baseline
mode requires this exact candidate, absence of the helper/schema and public
namespace, accepted private bytes/modes, exact cron hash and security properties.
An unexpected engine, owner, mode, runtime pointer, lock or namespace stops for
manual governance review. Unknown objects are never adopted automatically.

The baseline receipt records observed engine mode/numeric owner/group/device/inode,
private file identities, runtime active link/environment/interpreter metadata,
association directory/lock and inventory lock metadata. Deployment rechecks the
receipt, accepts only operator-owned executable regular engine bytes with one link,
no special or group/world-write bits, and preserves its observed mode. Runtime
metadata inspection does not re-accept or execute the association environment.
The active environment remains cpython311-websockets16.1.1-lock-v1; no runtime
files or lock contract are changed. Public inventory is inspected for absence only;
its device identifiers and raw bytes are never placed in receipts or output.
Natural cycles may update inventory between baseline review and deployment, so its
hash/inode are not frozen; namespace absence is checked again under the drain lock.

A. PI3 SOURCE SYNCHRONIZATION TO DEPLOYMENT PREPARATION COMMIT ONLY, then STOP and
independent source review. The source-sync block in the final report validates the
exact predecessor, direct parent/subject, complete changed-file set and hashes,
and fast-forwards source only. No production path is touched.

B. Independent source-review contract: Linux host nutandpihole, user jazofv1,
exact source /home/jazofv1/hioc-release-source, main, final HEAD=origin/main,
0/0, clean, no active operation; exact parent and subject; all record/schema,
artifact and immutable implementation/private bindings verified; review scope
source-only. No cron mutation, process-lock acquisition, inventory, adapter,
projection, HA, credentials or MQTT operation. STOP after independent review.

C. FOR FUTURE SEPARATE BASELINE VALIDATION AUTHORIZATION ONLY:

```sh
env -i PATH=/usr/bin:/bin HOME=/home/jazofv1 LANG=C LC_ALL=C /usr/bin/python3 -I -S -B /home/jazofv1/hioc-release-source/tools/hioc-pe4-ha-public-projection-postdeploy-validate.py --preparation-commit PREPARATION_COMMIT --mode baseline
```

The tool writes one canonical JSON result to stdout, never creates a receipt.
The separately authorized operator must independently review a PASS receipt and
store its exact bytes at /home/jazofv1/pe4-public-projection-baseline.json, mode
0600, owned by jazofv1:jazofv1, and calculate its SHA-256. Neither source sync nor
baseline inspection authorizes deployment. Non-PASS output must not be used.

D. FOR FUTURE SEPARATE DEPLOYMENT AUTHORIZATION ONLY â€” NOT AUTHORIZED YET:

```sh
env -i PATH=/usr/bin:/bin HOME=/home/jazofv1 LANG=C LC_ALL=C /usr/bin/python3 -I -S -B /home/jazofv1/hioc-release-source/tools/hioc-pe4-ha-public-projection-deploy.py --preparation-commit PREPARATION_COMMIT --baseline-report /home/jazofv1/pe4-public-projection-baseline.json --baseline-sha256 REVIEWED_RECEIPT_SHA256 --deploy-authorized
```

A/B/C/D are separate gates. The receipt SHA is explicit operator review authority;
there is no environment-only authorization or automatic baseline adoption. No
shell-exiting constructs are needed. Deployment runs under system stdlib Python,
not under the association runtime. Native code requires Linux isolated/no-site/
no-bytecode flags and exact named user/group IDs. Production CLI has no path,
rollback, recovery or already-installed mutation override.

## Maintenance and mutation order

Before production mutation, the tool proves exact source commit/origin/main,
clean main, no Git operation, preparation parent/subject, frozen implementation,
private artifacts, closed preparation record/schema and every preparation artifact.
Source synchronization is separate; there is no fetch, pull or merge inside the
deployment tool. Source bytes are compared with exact Git objects. The accepted
association deployment tool contributes only its hash-verified no-follow reader
methods, extracted by AST; its credential, network, runtime probe and deployment
methods are never imported or called. The new pinned directory implementation
closes every opened descriptor even when a child security check fails.

The native transaction changes only the original inventory cron line and these
three runtime files in this exact order:

1. governance/pe4/pe4-home-assistant-public-projection.schema.json
2. pi4/lib/hioc/home_assistant_public_projection.py
3. pi4/bin/hioc-inventory-engine.py LAST

Target root is /home/jazofv1/hioc. Additive targets must be absent. Existing engine
must equal the reviewed baseline. Generic release/install/upgrade/rollback and
pi4/install_pi4.sh remain prohibited and unchanged. No broad rsync, directory
copy, docs, tests, preparation records, private producer, credential or runtime
installation is allowed. The inventory scheduler/interpreter contract stays intact.

The complete original crontab is read once as baseline, bounded to 65536 bytes,
strict UTF-8, LF-terminated, no CR/NUL. Comments, ordering, blank lines and unrelated
jobs are preserved exactly. The exact inventory, association, association marker
and platform lines must each occur once. Alternate/duplicate HIOC jobs and a
projection scheduler are rejected. The supplied current hash is
8f900f4679aa861b02e781a61927683db5900ddfe159d78c3831a1595ae7fe71.
Only the exact inventory line is removed; candidate install occurs once and exact
reread is mandatory. Association and platform remain present throughout.

```cron
# HIOC_PE4_HA_ASSOCIATION
5,35 * * * * /home/jazofv1/hioc/runtime/pe4/active/bin/python -I -B /home/jazofv1/hioc/pi4/bin/hioc-home-assistant-association.py >/dev/null 2>&1
*/30 * * * * flock -n /tmp/hioc-inventory-engine.lock /home/jazofv1/hioc/pi4/bin/hioc-inventory-engine.py
17 3 * * * flock -n /tmp/hioc-platform-status.lock /home/jazofv1/hioc/pi4/bin/hioc-platform-status.py
```

During separately authorized maintenance the operator must prohibit all other cron
editors, deployments and non-lock-respecting manual inventory invocations. Crontab
has no compare-and-swap interface; byte checks do not eliminate an external edit
between check and publication. The engine lock excludes only cooperating callers.
No tool attempts process killing, waiting, retrying or overriding this limitation.

After verified quiescence, open the EXISTING /tmp/hioc-inventory-engine.lock with
no-follow/read-only/nonblocking flags. /tmp must be root-owned sticky 1777; lock
must be regular, single-link, jazofv1-owned, no unsafe mode/ACL and inode-bound.
Acquire EXCLUSIVE NONBLOCKING flock once. BUSY restores the exact original cron
once, verifies it and stops. Successful acquisition remains held across all
staging, installation, installed-set checks, pre-execution rollback, cron
restoration and final verification. No inventory engine executes under that lock.

Create a dedicated exclusive 0700 transaction directory
backups/pe4-ha-public-projection-deployment-v1 BEFORE cron mutation. It retains a
0600 durable intent journal, exact old engine and exact original cron. Stage names
are .pe4-ha-public-projection-v1- plus a bounded random suffix in the target parent,
so each rename stays on the same filesystem. All parents are pinned/no-follow,
safe owner/mode/ACL; files are exclusive, regular, single-link, exact owner/group/
mode, written completely, fsynced, reread and hash-verified. Schema/helper use Linux
renameat2 NOREPLACE. Engine uses atomic replacement after exact old bytes and
identity checks. Parent directories are fsynced and installed bytes/security/
inodes rechecked. Installed coherent set is verified before original cron is
restored once and exact bytes/hash reread. The inventory lock remains held.

## Failure, interruption and rollback

Output is one concise canonical JSON object, with closed errors/stages, install
attempt count, cron hashes, historical gate observations, verified install flags,
rollback result, honest mutation state, manual-review flag and STOP_REQUIRED=true.
Unknown cron state clears the scheduler verification flags. Any attempted runtime
rollback clears installed verification flags, including when rollback remains
uncertain; false means not verified and does not assert absence. The accepted
baseline receipt SHA-256 is included in deployment output.
Exception strings, raw crontab, inventory, registries and credentials are never
printed. Attempt flags do not assert a natural inventory run. All execution,
MQTT, HA, credential and adapter fields stay false for this tool's own activity.

Source/baseline/cron gates fail before scheduler mutation. Failed maintenance
install or reread leaves UNKNOWN_AFTER_ATTEMPT and retained intent, requiring
manual review; no retry or guessed restoration. When cron is verified maintenance
and the lock is held, a normal runtime transaction failure permits one bounded
rollback only for known provenance: exact old engine bytes/mode, removal of only
newly created schema/helper with verified inode/hash, unchanged private files,
original cron restoration and verified cleanup. A stage with uncertain provenance,
failed rollback verification or uncertain cron produces manual review and never a
clean rollback claim. There is no automatic rollback after cron restoration has
been attempted, even if the installed-state final check fails. Once execution can
no longer be excluded, rollback requires a separate governed operator decision.
No retained MQTT cleanup, public-output rewrite or unrelated rollback is attempted.

Power loss/interruption before or after every mutation may retain the dedicated
transaction directory or stage names. A new invocation seeing either stops for
manual review before cron mutation; it never resumes or heuristically cleans.
The tool is one-shot; an already-installed set fails the baseline gate and belongs
to read-only installed review. No unknown file is deleted. On verified success or
verified in-process rollback, only this invocation's exact known names are removed,
fsynced and absence rechecked. No active journal, backup or staging debris remains.
A separate installed review confirms hashes/modes, private/runtime/lock metadata,
exact original cron and no transaction debris; it does not prove projection output
or production execution, and never acquires the inventory process lock. Installed
review additionally requires the independently accepted baseline receipt SHA-256,
matching the value reported by the separately authorized deployment. It does not
silently adopt an edited receipt.

FOR FUTURE SEPARATE READ-ONLY INSTALLED REVIEW AUTHORIZATION ONLY:

```sh
env -i PATH=/usr/bin:/bin HOME=/home/jazofv1 LANG=C LC_ALL=C /usr/bin/python3 -I -S -B /home/jazofv1/hioc-release-source/tools/hioc-pe4-ha-public-projection-postdeploy-validate.py --preparation-commit PREPARATION_COMMIT --mode installed --baseline-sha256 REVIEWED_RECEIPT_SHA256
```

## First natural inventory cycle

FIRST NATURAL CYCLE IS A SEPARATE FUTURE ACCEPTANCE GATE. No forced inventory run
is authorized. A later natural 0/30 cycle must have independent operator evidence:
base schema_version remains 1.0; associated devices carry exactly the five reviewed
public fields and no private identifiers; non-associated devices omit the namespace;
services/topology/dependencies/summary/status/assets/liveness/incidents remain under
existing authority; local inventory/devices output is updated; inventory/devices
MQTT publication succeeds on the existing topics with existing retained behavior,
no new topics; association remains independently healthy; no new errors or debris.
Local files or metadata alone cannot prove MQTT publication. No wait/sleep/run,
network or adapter action is part of preparation, deployment or installed review.
Post-natural-cycle rollback remains separately authorized and governed.

Validation uses synthetic temporary files, injected cron/lock/fault operations and
native primitive mocks under the established Windows regression harness. No test
instantiates native production operations. Historical preparation, implementation,
POSIX and association scheduler records remain byte-identical; current lifecycle
tests advance their current bindings while continuing to verify historical Git
objects. Source/private runtime bytes remain identical to c762745.
