## Production compatibility dependency classification correction — 2026-10-06

Production Dependency Classification Correction PASS/CLOSED. The production observations
below are **OPERATOR_SUPPLIED_PRODUCTION_EVIDENCE**, provenance OPERATOR_SUPPLIED;
Codex did not access PI3, collect production evidence or execute the adapter/platform-status.

1. First deployment attempt failed RUNTIME_DRIFT / NOT_STARTED at 2ef66a2.
2. Exact accepted-runtime customization validation was corrected at e4d5a19.
3. Second attempt failed RUNTIME_DRIFT / NOT_STARTED at e4d5a19.
4. The raw-prefix child-probe construction was corrected at 84635cb.
5. Third attempt at `84635cb88380c590d2adfb655c37afd2118c629f` failed safely with
   DEPENDENCY_DRIFT / NOT_STARTED. No durable intent, production mutation, adapter
   execution, HA network/authentication, scheduler installation or rollback occurred.
6. Read-only evidence showed five category-B objects present/exact and compatibility.py absent.
7. Production platform-status is the known PRE_COMPATIBILITY_KNOWN_VERSION, SHA-256
   `b65464e722bf9a4da0004ecf3bb05e4105f345a87c62405ce92d97c6298b2af8`,
   jazofv1:jazofv1 mode 0755. Its existing cron is preserved. Current repository
   platform-status SHA-256 is `55f75b7945b02f5d23759cf277b0e008a407d9d71e51a9c12b40a3cd1855c733`.
8. The recent production compatibility state does not prove module deployment:
   tools/hioc-pe4-ha-registry-discovery.py record_compatibility() inserts its source-root
   pi4/lib into sys.path on POSIX, imports compatibility from the release-source tree,
   and calls refresh_status with StateStore under /home/jazofv1/hioc/state/platform.
   The PE-4.0B.2b source-tree writer can therefore produce sanitized central state
   without installing compatibility.py in production. No private state contents are recorded.
9. compatibility.py was introduced at `8187114c7233be82b188f0fc03b93a022787e7bb`,
   “HIOC: add compatibility resilience and drift diagnostics”. Its classification as
   an already existing production dependency was a preparation defect, not byte drift.
10. It is now A_NEW_FILE_TO_DEPLOY, using the ordinary additive transaction path.
11. No platform-status upgrade or general compatibility-framework deployment is bundled.

Current manifest: **five required existing dependencies, nine additive targets**.
Only compatibility.py moved category; its source bytes are unchanged. Remaining B files
retain REQUIRED_EXISTING_EXACT_PRESERVE_ABSENT_OR_DIFFERENT_FAIL_CLOSED. compatibility.py
is installed only when absent, preserved when exact, and rejected when different/unsafe;
source blob `1ba46d4ebf3819e2fa3ee9365e5b0088ba0b4a1a`, SHA-256
`713c292c09282f3be524bc8a2090de43cf0fb78a81b3c71eed143b7a0d68e952`,
owner/group jazofv1:jazofv1, mode 0644. The supplied request's SHA text had 63 characters;
the specified immutable Git blob and existing manifest establish this 64-character SHA.
The record preserves that transcription separately from the verified source identity.

Adapter direct local imports remain core.config, core.compatibility and core.state;
StateStore requires core.schemas. compatibility module-load imports are standard-library
only. The consumed safe_version/load_registry/assess/update_status call closure adds no
local dependency and does not reach mqtt_observation(), whose conditional ..mqtt import
is therefore outside the adapter path. No additional mandatory dependency was found.
Adapter, entrypoint, compatibility module and all runtime-policy source bytes are unchanged.

Compatibility installation is code-file publication only: durable intent records its
exact target/hash and created-file status; generic staged renameat2 NOREPLACE publication,
post-verification, resume and committed idempotence protections apply. Deployment never
imports compatibility.py, runs refresh_status/update_status/mqtt_observation/platform-status,
rewrites compatibility state or inventory, publishes MQTT or executes the adapter.
The accepted runtime, launch flags, customization policy and resolved-prefix correction
remain unchanged. Transaction evidence remains NOT_STARTED -> NOT_STARTED,
PREPARED -> INCOMPLETE, COMMITTED -> PASS. All three previous attempts remained NOT_STARTED.

The [production dependency correction record](../governance/pe4/pe4-ha-association-production-dependency-correction.json)
and [closed schema](../governance/pe4/pe4-ha-association-production-dependency-correction.schema.json)
bind the source/classification and operator provenance. All correction records are
repository-only governance, not additional production contracts. Runtime.contracts()
still reads six governance files. Prior correction records and commits remain immutable.
Older six-B/eight-additive statements below describe historical preparation and are
superseded by the five-B/nine-additive current manifest. Current helper source binding
requires the exact successor subject `PE-4: correct production compatibility dependency`,
immediate parent 84635cb, main/origin equality, clean tree, 0/0 and no Git operation.

Validation: deployment focused 83, runtime customization 8, adapter 73, production
dependency correction 14, other regressions 275; total 453 run, 452 passed, one existing
rsync-unavailable release skip on Windows. Tests cover absent/exact/different/unsafe,
intent, interruption immediately before/after compatibility publication, resume,
idempotence, all five required dependencies, state/platform/cron preservation and import
closure. No accepted interpreter, actual adapter/platform-status, live host or credential
is exercised. Syntax/import safety, canonical closed schemas, links, source identities,
privacy/prohibited-operation checks and diff checks are repository-only.

Adapter Implementation PASS/CLOSED, corrected before deployment; Runtime Validation
Correction PASS/CLOSED; Deployment Runtime Probe Correction PASS/CLOSED; Production
Dependency Classification Correction PASS/CLOSED; Deployment Preparation PASS/CLOSED,
corrected and rebound. Deployment, Bounded Manual Production Validation, Independent
Production Acceptance and Scheduler Deployment NOT STARTED; Public Projection DEFERRED;
PE-4 NOT COMPLETE; Phase 7A ACTIVE; Rollback NOT PERFORMED. Next unchanged:
**PE-4 Home Assistant Association Adapter Deployment Execution**. Complete operator block
is FOR REVIEW ONLY and was not run. Stop after repository correction.

## Deployment runtime probe resolved-prefix correction — 2026-10-06

Deployment Runtime Probe Correction PASS/CLOSED. The following chronology is
**OPERATOR_SUPPLIED_PRODUCTION_EVIDENCE**, provenance OPERATOR_SUPPLIED; Codex did not
access PI3 or collect the production observations:

1. First Deployment Execution attempt at 2ef66a2 failed RUNTIME_DRIFT, with durable
   transaction and production deployment NOT_STARTED.
2. Accepted-runtime customization correction at
   `e4d5a19afecccb1584708e3da57ba3c0c4258523` closed the exact reviewed customization policy.
3. Second Deployment Execution attempt at e4d5a19 again failed RUNTIME_DRIFT, with
   durable transaction and production deployment NOT_STARTED; no production mutation,
   adapter execution, HA connection/authentication, scheduling or rollback occurred.
4. Read-only diagnostic passed bootstrap policy extraction and exact customization
   observation, then isolated child NotADirectoryError at active: raw sys.prefix retained
   the governed `/home/jazofv1/hioc/runtime/pe4/active` symlink.
5. The operator's resolved-prefix diagnostic passed customization_validation, RESULT
   and RESOLVED_PREFIX_VALIDATION using the accepted environment's real site-packages.
   It accessed no credential, attempted no HA network and performed no production mutation.
6. The production adapter is unaffected: Runtime.runtime() already derives site from
   the fixed accepted ENVIRONMENT. Its module/entrypoint source bytes remain unchanged.
7. The deployment helper now resolves sys.prefix before site-packages observation;
   runtime_identity() still requires the exact accepted environment. The separately
   governed active link must resolve there before the child starts. No trust policy,
   O_NOFOLLOW traversal, filesystem observation helper or launch flag was weakened.

The child now uses:

```python
raw_prefix = Path(sys.prefix)
resolved_prefix = raw_prefix.resolve()
site = resolved_prefix / "lib/python3.11/site-packages"
```

Its reported prefix is `str(resolved_prefix)`, verified by the unchanged exact runtime
identity contract. Accepted resolved environment remains
`/home/jazofv1/hioc/runtime/pe4/environments/cpython311-websockets16.1.1-lock-v1`;
accepted adapter/runtime child launch remains `/home/jazofv1/hioc/runtime/pe4/active/bin/python -I -B`.
The existing stdlib deployment bootstrap uses -S independently of that accepted launch.
CUSTOMIZATION_POLICY, validate_runtime_customization, runtime_directory,
runtime_file_observation and runtime_customization_observation are unchanged because the
entire approved adapter module remains byte-for-byte identical. .pth, sitecustomize,
usercustomize, package, origin and sys.path gates retain the exact prior trust policy.

The [probe correction record](../governance/pe4/pe4-ha-association-deployment-runtime-probe-correction.json)
and [closed schema](../governance/pe4/pe4-ha-association-deployment-runtime-probe-correction.schema.json)
bind the new helper and unchanged adapter/entrypoint. Prior runtime correction records
and their helper identities remain immutable historical e4d5a19 evidence. Current deployment
preparation is rebound to the successor with immediate parent e4d5a19 and exact subject
`PE-4: fix deployment runtime prefix validation`; all main/origin/clean/0/0/no-operation
guards remain. This correction record is governance-only, not read by Runtime.contracts()
or installed in production. Eight additive targets, six runtime governance contracts and
six category-B dependencies remain unchanged. B policy remains
REQUIRED_EXISTING_EXACT_PRESERVE_ABSENT_OR_DIFFERENT_FAIL_CLOSED.

Validation: deployment focused 83 (including nine resolved-prefix/correction tests),
runtime customization 8, adapter 73, other regressions 275; total 439 run, 438 passed,
one existing release skip because rsync is unavailable on Windows. Behavioral tests execute
the generated child body with injected Linux paths/modules; the old construction reproduces
the safe failure, the resolved construction passes, and every tested runtime prerequisite
failure remains before credential validation, durable intent or production target mutation.
No accepted interpreter, actual adapter, credential, host or network is exercised by tests.

Adapter Implementation PASS/CLOSED, corrected before deployment; Runtime Validation
Correction PASS/CLOSED; Deployment Runtime Probe Correction PASS/CLOSED; Deployment
Preparation PASS/CLOSED, corrected and rebound. Deployment, Bounded Manual Production
Validation, Independent Production Acceptance and Scheduler Deployment NOT STARTED;
Public Projection DEFERRED; PE-4 NOT COMPLETE; Phase 7A ACTIVE; Rollback NOT PERFORMED.
Both failed attempts remain pre-intent failures. Next unchanged:
**PE-4 Home Assistant Association Adapter Deployment Execution**. The regenerated complete
operator block is FOR REVIEW ONLY and was not run. Stop after repository correction.

## Accepted runtime validation correction — 2026-10-06

Runtime Validation Correction PASS/CLOSED. **OPERATOR_SUPPLIED_PRODUCTION_EVIDENCE**:
the first Deployment Execution block was attempted once at
`2ef66a2d575c923c6939a4cd4d5bb2c8aab2f816` and failed safely with RUNTIME_DRIFT.
Deployment transaction and production deployment both remained NOT_STARTED. No production
adapter files, endpoint configuration, association state directory, credential/network
access, scheduler or rollback resulted. Codex did not collect the live evidence or access
PI3. The operator evidence established reviewed startup customization in the unchanged
accepted runtime. Blanket rejection implemented the frozen “no unreviewed customization”
policy too strictly; the correction permits only the exact reviewed identities below.

The [runtime correction record](../governance/pe4/pe4-ha-association-runtime-validation-correction.json)
and [closed schema](../governance/pe4/pe4-ha-association-runtime-validation-correction.schema.json)
bind current source identities and operator provenance. All prior commits and closed
historical records remain immutable. The accepted environment, active symlink, CPython
3.11.2/aarch64/SOABI, websockets 16.1.1 and its origin, sys.path bounds, package bounds and
launch **-I -B** remain unchanged. No runtime mutation occurred.

Exactly one site-packages .pth is required: distutils-precedence.pth, regular/no symlink,
jazofv1:jazofv1, 0640, one link, 151 bytes, SHA-256
`2638ce9e2500e572a5e0de7faed6661eb569d1b696fcba07b0dd223da5f5d224`.
Exact content includes the trailing space before LF. Setuptools 66.1.1 must record the
same basename, location, size and sha256 distribution hash
`JjjOniUA5XKl4N5_rtZmHrVp0baW_LoHsN0iPaX10iQ`. No other .pth is allowed.

sitecustomize must be loaded from `/usr/lib/python3.11/sitecustomize.py`, an exact root:root
symlink to `/etc/python3.11/sitecustomize.py`. The target must be regular root:root,
0644, one link, 155 bytes, exact reviewed content and SHA-256
`43d81125d92376b1a69d53a71126a041cc9a18d8080e92dea0a2ae23be138b1e`.
Debian package/version and successful dpkg verification are operator provenance only;
exact filesystem/module identities are the trust anchors. usercustomize remains prohibited,
loaded or present. Neither customization file is deleted or rewritten.

The adapter and deployment helper use the same literal policy and pure validator. The
helper checks the adapter source SHA-256 and extracts only the literal policy plus four
validation/observation definitions through AST; it does not import the adapter, execute
Runtime/run_cycle/main or invoke network operations. This avoids an extra runtime module
or deployment target. Native bounded no-follow reads pin directory and file bindings,
recheck metadata and symlink destination, and feed the pure validator. Deployment verifies
filesystem properties in its stdlib bootstrap before the accepted -I -B child probe,
which independently verifies the actually loaded module. The bootstrap's existing -S is
not an adapter launch change. Any mismatch fails adapter RUNTIME_VALIDATION_FAILED at
RUNTIME_VALIDATION before credential/network/publication; deployment RUNTIME_DRIFT before
intent or production mutation, with NOT_STARTED transaction/deployment evidence.

The correction record is governance-only: Runtime.contracts() still consumes exactly six
existing governance files. Eight additive A/C targets and six preserved B dependencies
remain unchanged in number. B policy remains
REQUIRED_EXISTING_EXACT_PRESERVE_ABSENT_OR_DIFFERENT_FAIL_CLOSED.

Validation: adapter 73; deployment preparation 74; correction 8; other regressions 275.
Total 430 run, 429 passed, one existing release skip because rsync is unavailable on Windows.
Important runtime logic uses deterministic fixtures and injected Linux metadata, with no
Windows skip. Syntax, import safety, canonical closed schemas, links, source identities,
privacy/prohibited-operation review and diff checks are repository-only.

Adapter Implementation PASS/CLOSED, corrected before deployment; Runtime Validation
Correction PASS/CLOSED; Deployment Preparation PASS/CLOSED, corrected before execution
and rebound to current source. Deployment, Bounded Manual Production Validation,
Independent Production Acceptance and Scheduler Deployment NOT STARTED; Public Projection
DEFERRED; PE-4 NOT COMPLETE; Phase 7A ACTIVE; Rollback NOT PERFORMED.
Next: **PE-4 Home Assistant Association Adapter Deployment Execution**. Stop after
repository correction; the regenerated deployment block remains FOR REVIEW ONLY.

### Current corrected executable identities

| Source | Git blob | SHA-256 |
| --- | --- | --- |
| `tools/hioc-pe4-ha-association-deploy.py` | `f18f49aafff9071b850bb4203a6017f49a1566d5` | `9f1903c99206348722584a976c57ac9e1bcbf53178e0c8d472719687259a48da` |
| `pi4/bin/hioc-home-assistant-association.py` | `2864361fac7cd48e947dac1e4e40aeeeb525adef` | `005fae482a4e2c42b48bfb991abf14ddf1d9de60f81169a2ed1573a767958b8c` |
| `pi4/lib/hioc/home_assistant_association.py` | `e71e4c45e21e9f1a25298471b48387cb19f53e1f` | `9a9be5812f3481146de7546875320eb6adec65ca5a2b3230ff5fec378892c7c1` |

Historical adapter identity at 5e9d1ff3: blob `0c049b7ee19b6b20c3fef53717455ba341d4a149`, SHA-256 `cf04d05f6215b9654539df69797de49a831044795ba8f7f5b3432d9d35a086b9`. Superseded for current execution; retained as historical evidence.

## Current deployment preparation pointer

Deployment Preparation PASS/CLOSED; the current next checkpoint is
**PE-4 Home Assistant Association Adapter Deployment Execution**.
[Deployment preparation](PE4_HOME_ASSISTANT_ASSOCIATION_ADAPTER_DEPLOYMENT_PREPARATION.md)
owns the FOR REVIEW ONLY operator block. Deployment remains NOT STARTED. The earlier
checkpoint closure narratives below preserve their historical sequencing and validation;
historical records remain unchanged; the runtime correction below supersedes executable identities.

# PE-4 Home Assistant Association Adapter Implementation

## Historical pre-deployment correction — 2026-10-06

Adapter Implementation PASS/CLOSED, corrected before deployment. Original implementation
commit `0bdb9340157daba4a6948251922d762cc4fc97ff` passed repository tests but received
an independent pre-deployment review identifying incomplete canonical-envelope type
validation and shared filesystem helpers capable of misclassifying state failures.
No deployment or production adapter execution/authentication occurred before correction.
The [current correction record](../governance/pe4/pe4-ha-association-adapter-predeployment-correction.json)
and [closed schema](../governance/pe4/pe4-ha-association-adapter-predeployment-correction.schema.json)
bind the historical 5e9d1ff3 executable identities. The original implementation record/schema
and original commit remain unchanged historical evidence; their source bindings are
historical, not current executable identities.

Canonical input now requires an exact dict root, schema_version 1.0, timezone-aware
updated string, devices/services lists, and topology/dependencies/summary dicts.
Malformed shape fails CANONICAL_INVENTORY_INPUT before credentials/HA. Only devices[].mac
remains association authority; the other root types establish envelope integrity.

NativeFS credential ACL checks retain CREDENTIAL_ACQUISITION. PosixFS explicitly owns
STATE_PUBLICATION security checks; shared name binding dispatches through the filesystem's
security context. Lock, contract, prior and inventory call boundaries retain their respective
LOCK_ACQUISITION, CONTRACT_VALIDATION, PRIOR_STATE_VALIDATION and CANONICAL_INVENTORY_INPUT
stages. Recovery/publication security never originates credential acquisition errors.
No owner, mode, ACL, no-follow, inode/name or durability check was removed.

Namespace conclusion B: the limit is the combined distinct namespace union across
connections and optional identifiers. Frozen preparation transport.max_namespaces is
128; its source_review binding pins the historical 2b reducer to Git blob
`9e77993c3f6a533b3d394017d4d97e2366959797`, SHA-256
`b074608e98e887767be964120e8bfad8b5f7fba5fa17d671b0a1a1704f35c1b8`.
That reducer's consume() loops over connections and identifiers and inserts both
into one namespace_union before enforcing MAX_NAMESPACES. The 0C contract's
Identifier namespaces section denies them HIOC identity authority. Optional identifiers
therefore require reviewed exact two-string pairs, bounded/nonempty strings, and
share the 128-name transport counter. They are never MAC-indexed, matched or persisted.
Connection MAC decision semantics and all other frozen identity/lifecycle rules are unchanged.

Historical focused validation: 70 tests passed, including 10 new correction tests with
separate envelope cases, real production ACL/name helpers, native lock validation,
recovery/publication stage assertions, exact LKG/absence and namespace boundaries.
Regressions: 275 run, 274 passed, one existing rsync-unavailable release skip.
Total: 345 run, 344 passed, one skipped. Syntax/import safety, canonical schema/JSON,
links, source identities, privacy/prohibited-path and diff checks passed.

Deployment and Scheduler Deployment NOT STARTED; Public Projection DEFERRED;
PE-4 NOT COMPLETE; Phase 7A ACTIVE; Rollback NOT PERFORMED. No real credential,
PI3/PI5/HA access, adapter network execution, production mutation, deployment,
scheduler activation, MQTT, public projection or rollback occurred.
Next remains **PE-4 Home Assistant Association Adapter Deployment Preparation**;
that checkpoint has not begun.

## Historical original implementation closure

Repository implementation and Windows synthetic validation: PASS/CLOSED.
Starting commit: `8923a074ac304a5cfe46367330819291caed6550`.
[Historical implementation record](../governance/pe4/pe4-ha-association-adapter-implementation.json)
and [closed schema](../governance/pe4/pe4-ha-association-adapter-implementation.schema.json)
bind source blobs and SHA-256 identities without a circular implementation-commit binding.

The [0C contract](PE4_HOME_ASSISTANT_ASSOCIATION_CONTRACT.md),
[0C.1 lifecycle](PE4_HOME_ASSISTANT_ASSOCIATION_LIFECYCLE_CLARIFICATION.md),
[frozen preparation](PE4_HOME_ASSISTANT_ASSOCIATION_ADAPTER_IMPLEMENTATION_PREPARATION.md),
and [current credential closure](PE4_HOME_ASSISTANT_RUNTIME_CREDENTIAL_PROVISIONING.md)
remain authoritative. Historical preparation's optional-LF wording is superseded
by TOKEN_PLUS_EXACTLY_ONE_FINAL_LF and
REQUIRE_AND_REMOVE_EXACTLY_ONE_FINAL_LF_NO_TRIM. Historical artifacts are unchanged.

## Runtime and input gates

The runtime-owned module is `pi4/lib/hioc/home_assistant_association.py`;
`pi4/bin/hioc-home-assistant-association.py` is a thin entrypoint without options.
Future governed launch uses `/home/jazofv1/hioc/runtime/pe4/active/bin/python`
with explicit `-I -B`, installed `/home/jazofv1/hioc/pi4/lib`, and accepted environment
`/home/jazofv1/hioc/runtime/pe4/environments/cpython311-websockets16.1.1-lock-v1`.
CPython 3.11.2, aarch64, cpython-311-aarch64-linux-gnu, websockets 16.1.1,
exact module origin, isolation, no bytecode and no unreviewed site paths are gates.
Only stdlib and accepted websockets are used; tools proof clients are not imported.
Linux/POSIX, actual jazofv1 on nutandpihole, HIOC_HOME `/home/jazofv1/hioc`, and
local IPv4 `192.168.100.252` are required before secrets/network.

Nonsecret `HIOC_HA_ENDPOINT` must be explicitly configured in `config/hioc.conf`
as `ws://192.168.100.251:8123/api/websocket`. Missing/drift fails; no default.
HIOC_HOME/HIOC_HA_ENDPOINT and case-insensitive proxy environment influence fail.
No production configuration or config example was changed.

The permanent 0600 jazofv1:jazofv1 lock is
`/home/jazofv1/hioc/state/inventory/associations/.home_assistant.lock` in owned 0700
associations. Nonblocking exclusive flock has zero acquisition timeout, spans HA
work, releases in finally and is never unlinked. Lock order is association, then
contracts/recovery/prior/inventory, credential, HA without other locks, candidate
and inventory recheck, association commit, existing compatibility lock, unlock.

Only ENOENT initializes an in-memory first baseline. Invalid prior/security/schema
1.0/history fails closed. Canonical inventory is fixed `state/inventory/inventory.json`,
read-only, schema 1.0, <=16 MiB/depth 32/65536 devices, unique dev_ IDs, canonical
MAC set index, aware updated <=5400 seconds old and <=60 seconds future.
Liveness/health never gate association. Before replacement the exact inventory bytes
are reopened, revalidated and compared; no retry or inventory lock.

Credential `/etc/hioc/credentials/home_assistant.token` uses root:jazofv1 0640,
root:jazofv1 0750 directories, single regular link, no-follow descriptor traversal,
NSS reader/ACL checks and before/after/name validation. One 2..4097-byte read requires
exactly one final LF; remaining 1..4096 bytes are printable ASCII 0x21..0x7E.
No trim, prompt, fallback, argv/environment/config token or credential digest.
References are released on network exit; no zeroization guarantee is claimed.

## HA protocol and association

One numeric AF_INET preconnected socket targets 192.168.100.251:8123; no DNS,
proxy, redirect, compression, ping, subscription, retry or alternate endpoint.
Connect 5 seconds; each send/receive 15; close 2; total network 90; invocation 180;
reaping grace 2; messages <=16 MiB, max_queue=1. A silent logger exposes no frames.
Strict JSON rejects duplicates/nonfinite values, depth >32, strings >1024,
record fields >128, distinct fields >256 and namespaces >128. Required bounded
structural cores and registry IDs/entity IDs are validated without last-wins.

After auth_required/auth_ok with consistent sanitized version, commands are exactly:

1. ID 1: `config/device_registry/list`
2. ID 2: `config/entity_registry/list`
3. ID 3: `config/area_registry/list`
4. ID 4: `config_entries/get`

Exact integer correlation, success=true and result shape are mandatory. All reads
must succeed; replay/unexpected responses fail. No fifth command or fallback.
Global HA indexing includes valid evidence on invalid/multiple-MAC devices.
Only one valid distinct noncolliding connection namespace mac mapping to one
canonical HIOC ID is strong. Supporting identifiers and IP/name/hostname/vendor
never create identity; generic HA integration ingestion is prohibited.

0C.1 reconfirms current strong pairs, preserves earliest exact-pair first time,
retires unconfirmed prior active episodes by frozen precedence, retains old episodes
unchanged, enforces historical HA ownership and current one-to-one cardinality.
Safe recreation requires all frozen conditions, absent prior-active/latest-history
source, no tie/competition/conflict; never-bound new pairs get new first time.
Same-pair reactivation preserves earliest first. History limit 4096 has no eviction;
4097 fails with entire LKG unchanged. Failed cycles never retire or advance timestamps.

Entity membership follows entity.device_id through a strong HA pair. Config entries
are deduplicated from reviewed device/member refs and resolve entry_id/domain.
Only direct device area yields area_candidate; via_device_id is private reviewed
metadata. Optional dangling/unsafe/unrepresentable fields/members are omitted with
INCOMPLETE while preserving strong identity. COMPLETE requires all present reviewed
supporting refs safe. Raw unique_id/connections/options/URLs/MAC/IP are never copied.
Closed internal schema validation covers every actual frozen keyword, plus
cross-record chronology, ownership, history preservation, summaries and privacy.

## Durable private publication and compatibility

Private schema 1.1 state is
`/home/jazofv1/hioc/state/inventory/associations/home_assistant.json`, owned 0600.
A random owned 0700 `.home_assistant.txn-<32_lower_hex>` stages 0600 candidate,
exact-prior-inode hardlink when present, closed <=4096-byte intent, and commit marker.
Complete writes, file rereads/fsyncs, directory fsyncs, input/prior/name checks,
atomic replacement and final schema/byte/security verification precede the verified
durable committed marker. Precommit failures durably invalidate an uncommitted marker,
restore the exact prior inode/bytes or absence, fsync and verify. Unproved restoration
returns preservation UNKNOWN and retains material, blocking secrets/network at recovery.
Recovery rejects malformed/multiple pending namespaces; committed state is verified.
Atomic rename to `.home_assistant.done-<32_lower_hex>` and parent fsync precede pinned
child cleanup. Done recovery is cleanup-only and never restores prior state.

ha_core receives a full version_metadata/authentication/device_registry/entity_registry/
area_registry/config_entries bool-or-None map. Existing assess runs before commit using
known compatible history; existing update_status runs after commit or observed HA
failure. Local pre-HA failures do not replace evidence. Version drift alone continues
as COMPATIBLE_UPDATED. No generic compatibility writer or new dependency row exists.
Postcommit reporting or cleanup failure is PASS_WITH_WARNING, preserving committed state.

Output is <=4096 bytes/16 allowlisted lines with factual TRUE/FALSE/UNKNOWN and
validated counts or UNKNOWN, no exception text, token, household IDs or raw response.
PASS and PASS_WITH_WARNING exit zero; FAIL exits nonzero. Retry is next invocation.

## Validation and checkpoint boundary

Focused implementation tests exercise temporary byte flow with synthetic POSIX
ownership/ACL/flock/directory-fsync metadata, memory HA messages and injected syscall
faults, plus the actual complete-write loop. Native Linux deployment syscall proof
remains a separately authorized production checkpoint; no fixture is a production override.
60 focused tests passed. Requested regressions ran 275 tests: 274 passed and one
existing POSIX-rsync-dependent release test was skipped on Windows. Total: 335 run,
334 passed, one skipped. Syntax/import safety, canonical closed JSON, source identities,
protected baseline bytes, documentation links and diff checks also passed.

Existing 0C/0C.1/preparation/credential/closure/2b/Master/inventory/compatibility/release
regressions preserve historical authority and now bind current implementation sources.

| Checkpoint | State |
|---|---|
| Adapter Implementation | PASS/CLOSED |
| Deployment | NOT STARTED |
| Scheduler Deployment | NOT STARTED |
| PE-4 | NOT COMPLETE |
| Phase 7A | ACTIVE |
| Rollback | NOT PERFORMED |

No real credential, PI3/PI5/HA access, network validation, production state mutation,
deployment, scheduler activation, MQTT association publication, public projection or
rollback occurred. Future user cron HIOC_PE4_HA_ASSOCIATION at `5,35 * * * *` remains
uninstalled/inactive. Public projection and PE-5 remain separately governed.
Next: **PE-4 Home Assistant Association Adapter Deployment Preparation**.
No PI3 deployment command is authorized or supplied here.
