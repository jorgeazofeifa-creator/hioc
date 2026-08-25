# PE-4.0B.2a Isolated Runtime Lifecycle

## Authority and status

This document governs repository-controlled execution of the already-selected
PE-4 runtime. It does not authorize execution. PI3 remains the execution host,
PI5 HA remains the remote API source, CPython 3.11.2 remains accepted, and
`websockets==16.1.1` remains frozen by
`PE4_ISOLATED_RUNTIME_DEPENDENCY_CONTRACT.md` and `requirements-pe4.lock`.

```text
ROUTE_PROOF_ORDER=BEFORE_DEPENDENCY_DEPLOYMENT
PE4_0B2A=NOT_STARTED
PE4_0B2B=NOT_STARTED
PE4_0C=NOT_STARTED
ACTION_A=COMPLETE
ACTION_B=BLOCKED_PENDING_GOVERNANCE_CORRECTION
```

Every action is separately authorized, emits a bounded terminal result, and
stops. PASS never chains the next action.

## Action boundaries and tools

| Action | Repository entrypoint | Network boundary | Mutation boundary |
| --- | --- | --- | --- |
| PE-4.0B.2a-A | `tools/hioc-pe4-artifact-acquire.py` | Exact governed HTTPS `files.pythonhosted.org` wheel URL only | Private workstation staging and durable off-device cache only |
| PE-4.0B.2a-B | `tools/hioc-pe4-artifact-transfer.py` | SSH/SCP only to `jazofv1@192.168.100.252`, strict known-host checking | One private `/tmp/hioc-pe4-artifact-transfer-XXXXXXXX` directory only |
| PE-4.0B.2a-C | `tools/hioc-pe4-route-proof.py` | One TCP connection to `192.168.100.251:8123`; no HTTP, WebSocket, credentials, proxy, DNS, redirect, or retry | None |
| PE-4.0B.2a-D | `tools/hioc-pe4-runtime-construct.py` | None | One private construction directory and offline venv installation |
| PE-4.0B.2a-E | `tools/hioc-pe4-dependency-validate.py` | None | None; isolation, distribution, and API behavior validation only |
| PE-4.0B.2a-F | `tools/hioc-pe4-runtime-publish.py` | None | Exact client, versioned environment, and active pointer only |
| PE-4.0B.2a-G | `tools/hioc-pe4-runtime-preflight.py` | None | None; complete credential-free runtime preflight only |
| Rollback | `tools/hioc-pe4-runtime-rollback.py` | None | Atomic active-pointer restoration to a retained eligible environment only |

The tools share `tools/hioc_pe4_runtime_common.py`. The shared module freezes
paths, identities, modes, evidence fields, cleanup boundaries, exact installed
distribution policy, and source/client verification; it is not an entrypoint.

## Artifact acquisition, cache, and transfer

Action A creates a unique private directory below the workstation's local HIOC
artifact root, refuses symlinked or unsafe paths, downloads only the exact
official URL with bounded size and time, and verifies filename, 188095-byte
size, and SHA-256 before same-root durable-cache publication. The cache is
off-device recovery input and is never Git content. Failure removes only the
invocation directory after proving its parent and type.

The exact Windows layout is the Known Folder `LocalApplicationData` followed by
`HIOC/artifacts/pe4/{cache,staging,evidence}`. The Known Folder is the trusted
boundary; every existing child component is rejected if it is a file, symlink,
junction, mount point, or other reparse point. Each governed directory and file
uses a protected DACL with inheritance removed and exactly the current user SID
allowed Full Control. Windows security is proved by DACL, never POSIX mode.

ACL persistence does not use `Get-Acl` or `Set-Acl`. A child-only environment
passes the already validated path to Windows PowerShell; the helper loads the
existing `DirectorySecurity` or `FileSecurity` access descriptor through
`DirectoryInfo`/`FileInfo`, disables inheritance without retaining inherited
rules, removes every remaining explicit Allow or Deny rule, adds exactly one
current-user SID FullControl rule, persists the descriptor, and rereads it.
Validation requires a protected DACL, exactly one non-inherited Allow ACE, the
exact SID and FullControl rights, directory `ContainerInherit|ObjectInherit` or
file `None`, and `PropagationFlags=None`. Read, protection, rule-update,
application, reread, and each validation failure have bounded error codes.

The first production attempt created only the expected `HIOC` directory and
stopped at ACL application before acquisition. A retry after separate
publication and authorization must reject it if it is a file or reparse point;
otherwise it hardens that existing directory before creating or using any
descendant. No operator deletion or manual ACL change is required or allowed.

Action A uses a direct HTTPS connection to the single frozen
`files.pythonhosted.org` host/path, with no proxy, redirect, retry, alternate
endpoint, or URL resolution. A monotonic 20-second total deadline is propagated
as the maximum remaining timeout for connection, response, and every bounded
read. At most 188096 bytes are read. Result-last evidence is an invocation-owned
child under the governed evidence root: a same-directory temporary file is
flushed, atomically replaced as `result.json`, and ACL-validated. Windows does
not claim POSIX directory-fsync durability.

Terminal and evidence state explicitly report `ARTIFACT_ACQUIRED`,
`ARTIFACT_VERIFIED`, `DURABLE_CACHE_PUBLISHED`, `CACHE_REUSED`, and
`EVIDENCE_PUBLISHED`. Evidence failure after durable publication therefore
cannot be mistaken for non-publication. Invalid CLI input emits only bounded
failure markers. Action A PASS stops before Action B.

Action A production evidence records fresh acquisition, exact verification,
durable publication, result-last evidence, and PASS. Action B consumes only the
exact wheel at the fixed `LocalApplicationData/HIOC/artifacts/pe4/cache` path
and the repository lock; it accepts no caller-selected path and does not consume
Action A evidence. It validates cache components as non-reparse directories
with governed protected DACLs and independently verifies filename, size,
SHA-256, lock identity, governance commit, and source identities.

Action B resolves only Windows system OpenSSH executables, never `PATH`. It uses
strict known-host verification, numeric PI3 addressing, bounded attempts/time/
output, public-key-only batch authentication, and no password fallback. Wheel
and lock transfer separately into one private, owner/mode-validated PI3 staging
directory and are independently verified before atomic rename. Result-last
sanitized evidence records partial state. The directory is reported and
preserved on PASS or any post-creation failure; there is no automatic cleanup.
Action B remains blocked until this correction is published and separately
prepared and authorized.

## Construction and validation

Action D requires the exact transferred directory, owner, `0700` mode, wheel,
and lock. `/usr/bin/python3 -m venv --copies` creates one non-existing private
sibling under the governed environment root. `--copies` prevents internal venv
symlinks under the contract that permits only the managed active pointer.
System-site packages are not enabled. The exact CPython 3.11.2, Linux AArch64
SOABI, and isolated prefix are proved before pip runs.

Installation uses the isolated interpreter and exactly:

```text
--no-index --no-deps --require-hashes --only-binary=:all: --no-cache-dir
```

The transferred private directory is the sole `--find-links` source. Pip isn't
upgraded. Failure deletes only the proven invocation-owned construction tree;
symlinks, an active target, unexpected owner, parent, name, or mode stop cleanup.

Action E independently proves the installed distribution set is limited to
venv bootstrap components plus exactly `websockets==16.1.1`. It proves canonical
asyncio `connect`, `max_size`, `proxy`, `open_timeout`, `close_timeout`, `**kwargs`
preconnected-socket support, redirect refusal with that socket, `PayloadTooBig`,
and `InvalidStatus`. Install success alone is never acceptance.

## Publication, backup, and rollback

Action F revalidates source commit, clean `main`, `origin/main`, client Git blob
and SHA-256, dependency capabilities, construction ownership, and non-symlinked
paths. It creates the exact immutable versioned environment, installs the client
at `/home/jazofv1/hioc/tools/hioc-pe4-ha-auth-capability.py` with mode `0700`,
and atomically replaces the active pointer only after validation. Existing
unexpected destinations fail closed. The prior active target is recorded and
retained; environments are never modified in place.

General release backup, deployment, and rollback flows treat `runtime/pe4` as
release-managed externalized content: they neither overwrite nor restore it.
Recovery inputs are the Git lock and tools, exact frozen artifact identity, the
durable off-device wheel cache, and retained prior approved environment. State,
history, logs, backups, configuration, manufacturer data, and credentials keep
their existing protected classifications.

PE-4 rollback is separate from general release rollback. It accepts only a
basename matching the governed environment form, proves it is a non-symlinked
direct child with safe ownership/mode and an acceptable distribution set, and
reads that basename only from the tool-published private `previous-active`
record rather than caller input, then atomically restores only the active
pointer. It never contacts an index and
never deletes the failed or restored environment automatically.

## Evidence, failure, and cleanup

Persistent evidence uses a tool-created private `/tmp` directory (`0700`) and
atomic result-last `result.json` (`0600`) with fsync. Allowed content is limited
to action/target classification, governed artifact filename/size/digests,
environment identity, client blob/digest, owner/mode result, installed version,
capability/preflight result, prior/current active target, bounded error/stage,
result, and rollback recommendation.

Credentials, tokens, authorization headers, HA bodies, secrets, environment
dumps, raw command output, arbitrary package metadata, and unrelated system or
household information are prohibited. Every failure stops. Cleanup may target
only a validated invocation path; neither `/home/jazofv1/hioc` nor
`/home/jazofv1/hioc/runtime/pe4/environments` may be recursively removed.
