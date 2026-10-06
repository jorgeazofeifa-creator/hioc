# PE-4 Home Assistant Runtime Credential Provisioning

This repository preparation is PREPARED_FOR_SEPARATE_OPERATOR_EXECUTION.
Preparation is PASS/CLOSED; the parent Runtime Credential Provisioning is
PREPARED / NOT COMPLETE. No credential has been provisioned. Operator Installation,
Independent Credential Validation and Governance Closure remain NOT STARTED.
Adapter Implementation is NOT STARTED; PE-4 NOT COMPLETE; Phase 7A ACTIVE;
rollback NOT PERFORMED. The next task is **PE-4 Home Assistant Runtime Credential
Provisioning — Operator Installation**.

The unchanged [implementation preparation](PE4_HOME_ASSISTANT_ASSOCIATION_ADAPTER_IMPLEMENTATION_PREPARATION.md)
and [frozen authority](../governance/pe4/pe4-ha-association-adapter-implementation-preparation.json)
govern unattended acquisition. This [preparation record](../governance/pe4/pe4-ha-runtime-credential-provisioning-preparation.json)
is canonical compact sorted JSON validated by its
[closed schema](../governance/pe4/pe4-ha-runtime-credential-provisioning-preparation.schema.json).
Credential preparation is separate because secure local delivery must precede
adapter implementation and bounded authentication validation. A policy-valid
revoked or incorrect credential can pass local storage validation intentionally.
There is no HA request, discovery, network import, MQTT, cron or HIOC-state write.

## Pre-execution canonical-storage correction — 2026-10-06

Original preparation commit `afa484620d24a1d6dec2a98e7c06e613f633bfb7`
remains immutable Git history; historical preparation baseline is
`d8e888023882770e2f158dc1fffebd5b354fb616`. Independent review found that both
original tools accepted missing-final-LF files despite TOKEN_PLUS_EXACTLY_ONE_FINAL_LF.
This corrective checkpoint updates the canonical record/schema and executable
source bindings before any operator execution. It does not erase or amend the
original preparation. Missing-final-LF files now fail CONTENT_INVALID; provisioning
preflight maps invalid existing files to EXISTING_CREDENTIAL_INVALID before the
hidden prompt, with no replacement. Both validator identity modes require the LF.

Preparation remains PASS/CLOSED, corrected before execution. Parent remains
PREPARED / NOT COMPLETE; Installation, Independent Validation, Governance Closure
and Adapter Implementation remain NOT STARTED. No credential was provisioned.
The previous proposed installation block is superseded; use only the corrected
commit/identities in the new FOR REVIEW ONLY block after independent review.


## Exact boundary

Logical name: `home_assistant_access_token`. Mechanism:
`DEDICATED_ROOT_PRIVATE_FILE_FOR_CRON_UNATTENDED_READ`.

| Object | Owner:group | Exact mode |
| --- | --- | --- |
| `/etc/hioc` | `root:jazofv1` | `0750` |
| `/etc/hioc/credentials` | `root:jazofv1` | `0750` |
| `/etc/hioc/credentials/home_assistant.token` | `root:jazofv1` | `0640` |

The file must be regular, single-link and not a symlink. Every ancestor is opened
relative to a pinned parent with Linux O_DIRECTORY/O_NOFOLLOW/O_CLOEXEC. `/` and
`/etc` must be root-owned, without group/world write or special mode bits; their
ordinary group and world read/execute permissions are allowed. Governed directories
require the exact group and mode. No recursive ownership or permission change is
allowed. Existing safe but differing directory modes also fail: this implementation
chooses **no normalization**. Unexpected owners, groups, ACLs and object types fail.
Directory link counts normally reflect subdirectories; Linux prohibits ordinary
hardlinks to directories. File nlink must equal one.

Only missing `/etc/hioc` and `/etc/hioc/credentials` may be created. Each starts
0700, is pinned and ACL-checked, then fchown/fchmod establish 0750 and child/parent
fsync make metadata durable. Credential-free preflight may leave empty newly
created governed directories after a failure. It never removes existing hierarchy.
Concurrent provisioning is excluded by a nonblocking flock on the pinned credential
directory, held until descriptor closure; no separate lock file is created. A busy
lock fails before prompting. Directory fsync support is checked before prompting.
Future read-only consumers need no provisioning lock.

## Effective readers and ACLs

Linux NSS enumeration and keyed lookups must agree. Membership is the union of
all users whose primary gid equals the approved group gid and `grp.gr_mem`
supplemental members. Only non-root `jazofv1` may belong; root is implicitly
privileged. Missing accounts/members, duplicated names or UIDs, multiple groups
with the target gid, inconsistent lookups or duplicate supplemental entries fail.
The operator must actually be an effective member of the approved group. PI3's
actual account configuration is unknown until the later on-host preflight.
No users or groups are created or modified. Unauthorized ordinary-reader exclusion
is proved through this effective-membership calculation and the ACL boundary,
without creating a test user or weakening host configuration.

The tools call Linux `os.getxattr(fd, ...)` on pinned descriptors for
`system.posix_acl_access` and, for directories, `system.posix_acl_default`.
Only ENODATA means an authoritative absent ACL. EOPNOTSUPP/ENOTSUP, permission
errors, unreadable, malformed or unknown ACL data fail closed. An access ACL may
also be the exact Linux version-2 three base entries (owner/group/other), whose
permissions match mode bits and whose IDs are undefined. All named entries,
mask entries and all default ACLs are rejected, even if apparently harmless.
This intentionally narrow POSIX ACL policy prevents inherited or additional access.
No `getfacl` package is required. A filesystem that exposes different ACL models
or cannot establish this boundary cannot pass; no NFSv4 ACL claim is made.
Read-only validation checks the same boundary in each identity mode.

## Hidden input and content

The [provisioning tool](../tools/hioc-pe4-ha-runtime-credential-provision.py)
requires Linux, real/effective root and hostname `nutandpihole`. It accepts no
arguments, path override, delete subcommand, token option, environment credential,
config credential or piped input. Host, accounts, group, ancestors, ACLs and any
existing credential are checked before acquiring the secret.

The root process opens `/dev/tty`, verifies a controlling TTY and interactive
stdin/stderr, and calls getpass exactly once with:
`Home Assistant runtime access token:`. GetPassWarning is fatal; no echo/stdin
fallback is permitted. Sudo privilege is obtained before this prompt; no secret
crosses sudo stdin, shell substitution, argv, environment, heredoc, Git or chat.
Input is `<entered locally through hidden terminal prompt>` only.

Strict ASCII encoding permits only nonempty bytes 0x21 through 0x7E, at most
4096 bytes. Spaces, tabs, CR, LF, NUL, controls and non-ASCII fail without trimming.
No JWT, prefix, version or HA token-shape assumption is made. Provisioning stores
exactly one final LF, for at most 4097 file bytes. Every persisted file must be 2 through 4097 bytes and end with exactly one
final LF. Reading requires and removes that LF, then checks the identical token policy.
Missing LF fails; existing noncanonical bytes are not normalized or overwritten.
A second final LF, interior LF or other whitespace fails. No length, prefix,
suffix, hash, entropy or credential-derived evidence is generated.

## Install and atomic rotation

The same local operation is INSTALL if the final file is absent, or ROTATE if a
valid final exists immediately before replacement. An unsafe or content-invalid
existing file fails `EXISTING_CREDENTIAL_INVALID` before the prompt, without
replacement. The existing snapshot is checked again immediately before commit;
changed binding/content metadata fails rather than silently adopting unknown state.

An unpredictable 192-bit staging name is created in the credential directory using
O_CREAT/O_EXCL/O_NOFOLLOW, initial 0600 and a pinned read/write descriptor. Collision
fails without deleting the colliding object. Complete write-loop progress is
required. Private staging metadata/ACL/name binding are rechecked after writing.
File fsync, fchown root:jazofv1, fchmod 0640 and a second fsync precede
bounded exact byte reread, metadata/ACL/name-binding and same-filesystem checks.
Only then os.replace atomically replaces the final name. The directory is fsynced,
then final no-follow/nonblocking reopen, exact bytes, security metadata and staging
inode identity are verified. No direct final-file write is used.

Before replacement the old credential is untouched. After replacement the new
credential is authoritative, including when directory fsync or final verification
fails. `POST_REPLACE_VALIDATION_FAILED_NEW_AUTHORITATIVE` requires separate
operator review; it never claims rollback or restoration. A process interruption
at an unobservable syscall boundary may yield an unproved replacement-status
failure: inspect through a separately authorized read-only validation action.
A future adapter already holding an old pinned descriptor/value may finish;
the next invocation reads the replacement. No old value is retained as evidence,
no backup or .bak exists, and no second real token is required to prove rotation.

Cleanup removes only the staging name proven to match this invocation's pinned
regular root-owned single-link object, after rechecking hierarchy. It never
unlinks the final name. Unproved cleanup emits `STAGING_CLEANUP_UNPROVED`; the
operator must review safely rather than recursively removing files. Ordinary
exceptions and catchable interruptions attempt cleanup. SIGKILL/power loss cannot
run finally: a root-owned 0600/0640 orphan may remain for a separately authorized
recovery action. The tool never claims cleanup after uncatchable interruption.

## Independent read-only validation

The separate [validator](../tools/hioc-pe4-ha-runtime-credential-validate.py)
accepts only `--root` or `--runtime-operator` and the fixed governed path.
It contains no create/write/chown/chmod/replace/delete operation, no provisioning
call and no network/authentication code. Root mode requires real/effective root;
runtime mode requires real/effective `jazofv1` and an active approved group.

Each opens the fixed hierarchy and regular file no-follow/nonblocking, checks
owner/group/modes/nlink/ACL/size, performs one read bounded to 4098 bytes, requires
exact size, verifies before/after fstat and current name binding, requires exactly one final LF, validates canonical content,
and rechecks ancestor bindings. Oversized, changed or short reads fail. References
are released; physical memory zeroization is not claimed. Root mode prints runtime
readability NOT_TESTED. Only a separate actual `jazofv1` read may print TRUE.
Installation's final root recheck is not independent validation or authentication.

## One operator action at a time

1. Repository Preparation: PASS/CLOSED, prepared for separate operator execution.
2. Operator Installation: NOT STARTED. Use the exact pushed commit and source hashes
   supplied in the preparation report on **PI3 NUT&PIHOLE**, host `nutandpihole`,
   operator `jazofv1`, source `/home/jazofv1/hioc-release-source`.
3. Independent Validation: NOT STARTED. After separate authorization and accepted
   installation evidence, bind the same source and run root validation, then an
   actual non-root runtime-operator read as distinct checks. Commands are supplied
   at that checkpoint, not chained into installation.
4. Governance Closure: NOT STARTED. Independently accept installation and both
   validation results before closing the parent. Parent remains NOT COMPLETE here.
5. Adapter Implementation: NOT STARTED, follows credential prerequisite closure.

The installation report's self-contained block checks branch main, exact new
commit, local origin/main, 0/0, clean index/worktree including untracked files,
all active Git-operation markers, canonical source paths, host/operator and both
tool blobs/SHA-256 before sudo. No fetching, checkout, deployment or secret occurs
in those checks. Root then independently reads bounded no-follow source bytes,
checks both exact SHA-256 identities and executes the already-verified in-memory
provisioning bytes under isolated Python with bytecode disabled. Neither tool
imports a mutable sibling; common security code is self-contained and regression
checked identical. This avoids a path-reopen race between hash and root execution.
The proposed command block stops immediately after provisioning. It is FOR REVIEW
ONLY and is not executed by Codex. The operator-shell rule prohibits set -e, set -u,
pipefail, shell exit/exec and logout; explicit return-code handling preserves the
existing interactive shell after PASS or FAIL. No working directory is assumed.

## Evidence, recovery and closure

Allowed evidence: target host/operator, fixed path, root:jazofv1 directory 0750
and file 0640, regular/single-link PASS, ACL/group/content PASS, INSTALL or ROTATE,
atomic replacement PASS, separately established runtime-readability PASS,
credential-value-exposed FALSE, network FALSE, authentication FALSE and bounded
stage/error codes. Forbidden: bytes, derived hash, length, partial value, prefix,
suffix, entropy, raw exception, traceback, backups, unnecessary inodes/timestamps.
Production output is bounded constants and codes, with no exception-text echo.
Do not paste a credential into Codex. Local failure output contains no secret.

If preflight fails, do not bypass checks or repair unexpected secret objects.
Account/ACL/hierarchy drift requires separately authorized operator review.
If input fails, the old final is untouched and this operation stops; a later
explicit invocation can retry. Post-replacement errors leave the new authoritative
file in place for separate validation. Cleanup uncertainty requires bounded review,
not automatic secret deletion. Later closure needs exact source identities,
installation evidence, root validation and non-root readability validation;
authentication remains DEFERRED_TO_ADAPTER_VALIDATION. No live rotation/deletion
is part of initial acceptance.

Deliberate credential removal/revocation is a separate explicit security action,
without a routine provisioning delete command. Frozen future adapter semantics:
missing credential fails, preserves last-known-good state and has no fallback.
Synthetic tests exercise absence; no live credential is deleted.

## Release, upgrade and rollback preservation

Reviewed unchanged [release installer](../release/install.sh),
[upgrade](../release/upgrade.sh), [rollback](../release/rollback.sh),
[builder](../release/build.sh), [collector installer](../pi4/install_pi4.sh),
[collector uninstaller](../pi4/uninstall_pi4.sh) and
[HA installer](../homeassistant/install_ha.sh) operate on managed source/install,
backup, runtime and HA-package trees, not `/etc/hioc/credentials`. Standard HIOC
install updates, upgrades and code rollback do not overwrite, delete or back up
the external operator credential. Regression tests bind those scripts unchanged,
check their actual managed-tree boundaries and absence of credential ownership.
Do not redirect configurable install roots into the credential hierarchy.
No general installer is given credential creation. Secret bytes are not Git,
release manifests, rollback evidence or repository-controlled backups. This is
not a promise about OS reinstallation, disk loss or manual deletion; future DR
work must govern those independently. DATA_MODEL is unchanged.

## Repository validation limits

Synthetic tests use real temporary file bytes, exclusive create, short writes,
atomic rename, hardlinks and cleanup with injected POSIX metadata, ACL/NSS, lock,
privilege and syscall faults on Windows. Production CLI has no fixture override.
Tests cover boundaries, first installation, rotation, required canonical LF, invalid prior
state, interruption and post-commit errors, read-only validation and redaction.
They do not prove actual PI3 ownership/ACL support, sudo TTY, directory fsync or
non-root access until later operator execution. No production/network tests ran.
