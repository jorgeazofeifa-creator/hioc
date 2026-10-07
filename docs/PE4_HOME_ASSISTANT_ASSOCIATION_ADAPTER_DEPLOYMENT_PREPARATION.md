## Deployment Execution governance closure — 2026-10-06

**Deployment PASS/CLOSED.** The operator reported successful governed deployment at
`4912f20d8b2ff78dcdaf8b3e0f52e57d5de5e3a2` and a separate PASS read-only static acceptance.
Both are OPERATOR_SUPPLIED_PRODUCTION_EVIDENCE, provenance OPERATOR_SUPPLIED; Codex did
not collect them or access PI3. Transaction COMMITTED; five dependencies preserved;
nine targets verified, all nine newly created; endpoint added. The three earlier failures
remain historical pre-intent NOT_STARTED attempts, with no partial deployment or rollback.

Deployment-local credential validation PASS used the governed local validator; this is
not a claim that deployment never read the credential file. No credential content was
exposed/persisted in evidence, placed in argv/environment or used for HA authentication.
The separate static acceptance accessed no credential. Codex accessed no real credential.
Adapter/platform-status remained unexecuted; no adapter HA network/authentication or
association state publication occurred. Association scheduler absent; existing platform
cron unchanged; pre-compatibility platform-status and compatibility-state metadata preserved.

Current objective and exact next task: **PE-4 Home Assistant Association Adapter Bounded Manual Production Validation**.
It remains NOT STARTED and requires separate first-run authorization. Independent Production
Acceptance and Scheduler Deployment NOT STARTED; Public Projection DEFERRED; PE-4 NOT COMPLETE;
Phase 7A ACTIVE; Rollback NOT PERFORMED. Stop before first adapter execution.
[Focused deployment closure](PE4_HOME_ASSISTANT_ASSOCIATION_ADAPTER_DEPLOYMENT_CLOSURE.md)
consolidates the two evidence sets and boundaries. Earlier checkpoint narratives retain
historical states and next tasks; this closure supersedes their current-authority wording.

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

### Deployed executable identities at 4912f20d

| Source | Git blob | SHA-256 |
| --- | --- | --- |
| `tools/hioc-pe4-ha-association-deploy.py` | `f18f49aafff9071b850bb4203a6017f49a1566d5` | `9f1903c99206348722584a976c57ac9e1bcbf53178e0c8d472719687259a48da` |
| `pi4/bin/hioc-home-assistant-association.py` | `2864361fac7cd48e947dac1e4e40aeeeb525adef` | `005fae482a4e2c42b48bfb991abf14ddf1d9de60f81169a2ed1573a767958b8c` |
| `pi4/lib/hioc/home_assistant_association.py` | `e71e4c45e21e9f1a25298471b48387cb19f53e1f` | `9a9be5812f3481146de7546875320eb6adec65ca5a2b3230ff5fec378892c7c1` |

Historical adapter identity at 5e9d1ff3: blob `0c049b7ee19b6b20c3fef53717455ba341d4a149`, SHA-256 `cf04d05f6215b9654539df69797de49a831044795ba8f7f5b3432d9d35a086b9`. Superseded for current execution; retained as historical evidence.

# PE-4 Home Assistant Association Adapter Deployment Preparation


## Historical pre-execution governance and evidence correction — 2026-10-06

Deployment Preparation PASS/CLOSED, corrected before execution. Historical preparation
commit `0040bdc79e66c10db4f180f952d04f97b1070065` passed repository tests but independent
review found an incorrect additive policy on category B and ambiguous/control-flow-based
transaction evidence. No deployment, helper/adapter execution or HA authentication occurred.
The [dedicated correction record](../governance/pe4/pe4-ha-association-adapter-deployment-preparation-correction.json)
and [closed schema](../governance/pe4/pe4-ha-association-adapter-deployment-preparation-correction.schema.json)
bind the historical 2ef66a2 helper and preparation record/schema. The historical commit
and its records remain immutable Git evidence; current policy/source identities below are
corrected. The complete current proposed block remains FOR REVIEW ONLY.

All six B_EXISTING_EXACT_DEPENDENCY files use
REQUIRED_EXISTING_EXACT_PRESERVE_ABSENT_OR_DIFFERENT_FAIL_CLOSED:
ABSENT/DIFFERENT -> DEPENDENCY_DRIFT; EXACT -> PRESERVE; INSTALL/REPLACE -> PROHIBITED.
Their source identities are unchanged. The eight A/C targets retain
ABSENT_INSTALL_EXACT_PRESERVE_DIFFERENT_FAIL_CLOSED. A manifest guard enforces exactly six
reviewed B paths, eight distinct additive paths, their classifications/policies and disjoint
sets before any installation. No broad HIOC upgrade or dependency installation is authorized.

DEPLOYMENT_TRANSACTION has exactly NOT_STARTED, PREPARED, COMMITTED. A bounded read-only
classifier validates secured canonical intent, its source/target authority and config backups,
then the canonical COMMITTED marker bound to intent/source. It never executes recovery,
modifies targets or deletes artifacts. Missing/invalid intent proves no PREPARED state;
a pre-intent namespace still stops TRANSACTION_CONFLICT without guessed cleanup. Valid
intent without valid committed marker is PREPARED. Valid committed marker is COMMITTED
regardless of later target, effective config, toolkit, runtime, credential or scheduler
acceptance failure. An already verified durable commit is not concealed by later failed
journal verification; overall acceptance fails and operator review is required.

| Durable transaction | PRODUCTION_DEPLOYMENT | Overall RESULT |
| --- | --- | --- |
| NOT_STARTED | NOT_STARTED | PASS/FAIL according to operation result |
| PREPARED | INCOMPLETE | FAIL for interrupted/incomplete operation |
| COMMITTED | PASS | PASS, or FAIL if later acceptance/recheck fails |

The 22-field evidence allowlist is unchanged. Prerequisites may be NOT_PROVEN on failure;
durable transaction/deployment evidence stays factual. Adapter/network/authentication FALSE,
scheduler NOT_STARTED and rollback NOT_PERFORMED remain fixed. No automatic rollback.
72 focused tests include 22 new correction tests with the full preflight/interruption/
postcommit/idempotence matrix, immutable source identities and closed schemas. Required
regressions: adapter 70, remaining 275; total 417 run, 416 passed, one existing rsync skip.
Deployment, Bounded Manual Production Validation, Independent Production Acceptance and
Scheduler NOT STARTED; Public Projection DEFERRED; PE-4 NOT COMPLETE; Phase 7A ACTIVE;
Rollback NOT PERFORMED. Next unchanged: **PE-4 Home Assistant Association Adapter Deployment Execution**.

## Historical preparation closure and unchanged operational boundaries

Deployment Preparation PASS/CLOSED from clean synchronized main
`5e9d1ff3d74bb22c6cc0c4f726517c1d0b86d7f2`. Adapter Implementation PASS/CLOSED,
corrected before deployment. Historical implementation `0bdb9340157daba4a6948251922d762cc4fc97ff`
and all closed contracts/records remain immutable. This is repository-only preparation;
no host inspection, deployment or first adapter invocation occurred. The block below is
FOR REVIEW ONLY and requires separate deployment authorization and independent review.

The [canonical record](../governance/pe4/pe4-ha-association-adapter-deployment-preparation.json)
and [closed schema](../governance/pe4/pe4-ha-association-adapter-deployment-preparation.schema.json)
freeze the manifest and policy. [Implementation](PE4_HOME_ASSISTANT_ASSOCIATION_ADAPTER_IMPLEMENTATION.md),
[preparation](PE4_HOME_ASSISTANT_ASSOCIATION_ADAPTER_IMPLEMENTATION_PREPARATION.md),
[0C](PE4_HOME_ASSISTANT_ASSOCIATION_CONTRACT.md), [0C.1](PE4_HOME_ASSISTANT_ASSOCIATION_LIFECYCLE_CLARIFICATION.md),
[historical predeployment correction](../governance/pe4/pe4-ha-association-adapter-predeployment-correction.json)
and [credential closure](../governance/pe4/pe4-ha-runtime-credential-provisioning-closure.json)
remain authority. Current closure overrides historical optional-LF wording.

## Complete static runtime dependency audit

Entrypoint imports only hioc.home_assistant_association after inserting installed
pi4/lib. Adapter's dynamic HIOC imports are core.config.ConfigService;
core.compatibility.safe_version, STATES, GOOD, load_registry, assess and update_status;
and core.state.StateStore. Package initializers execute during these imports.
StateStore transitively imports core.schemas.Schema. Their APIs, initializers and
source bytes are covered by the five B dependencies and additive compatibility.py below; no broad existing-code replacement is allowed.
core.compatibility's conditional mqtt_observation import of hioc.mqtt is not reachable
from the adapter's consumed APIs. pi4/lib/hioc/config.py was inspected but is not imported:
the adapter consumes ConfigService directly, not load_config. These exclusions are explicit
in governance. Standard-library imports, Linux NSS/ACL/flock/fsync/renameat2, the local ip
binary and accepted websockets are category E external prerequisites.

ConfigService reads toolkit.conf, then hioc.conf, then HIOC_/MQTT_ environment values.
Toolkit is read securely but never modified. Deployment disallows those environment keys,
PI4_TOOLS_HOME and proxy overrides, mirrors reviewed parser semantics, verifies effective
HIOC_HOME and endpoint after merge and rechecks toolkit bytes. Dynamic inventory and
compatibility state are existing runtime data inputs, never deployment sources/targets.
Runtime governance is the complete six-file set read by Runtime.contracts(), including
compatibility-contracts.json. No adapter/private-state import is needed for deployment.

Identities bind committed Git bytes; Windows checkout CRLF is not a production source identity.
The future Linux source must match the exact committed bytes, without deployment normalization.

Source prefix: `/home/jazofv1/hioc-release-source/`.
Production prefix: `/home/jazofv1/hioc/`. Every relative path below maps independently
to these prefixes; synchronizing the checkout does not establish production identity.

### B: existing production Python files, exact identity required

Missing or different bytes STOP with DEPENDENCY_DRIFT. Preserve existing secure metadata:
regular single-link files; root/operator ownership; no special or group/world-write bits,
no access/default ACL, no symlink/special objects or changed name/inode binding. No update set.

| Relative path | Git blob | SHA-256 |
| --- | --- | --- |
| `pi4/lib/hioc/__init__.py` | `d706ff40b4b225296170fda501567c4fbf3d5136` | `5052b317d5f9fa47aba366a41393caac93406ea63f98f047783bbb2e70e221b2` |
| `pi4/lib/hioc/core/__init__.py` | `ea7e8b622af1a81d400e6d7f434729a663f44f70` | `043f9848cddfd3c37f153244107ea4c6b5965f26887da049d07ebd6bf4b01dbc` |
| `pi4/lib/hioc/core/config.py` | `0d6b972bf303a7bca736a881ea855bc13fffcdc8` | `ceb59f81cb5e247b929754603f2aaeee29e12897cf45cff5c0612ba1ecd261f7` |
| `pi4/lib/hioc/core/state.py` | `2be5b599f3822b859a5ca92cd046905255a2923f` | `ff907db9b5a8a9cfb1413c8670475a9ff5f80203f553f12d1e565be42717772d` |
| `pi4/lib/hioc/core/schemas.py` | `7f2bbe7264c1b02294bbebfed65c2745d559c706` | `7db98c3cb8d6030faf81454b7bc473ba8459b3a7c9e32377bb9a0b64e3d4fe1e` |

### A: primary additive code targets

Owner/group jazofv1:jazofv1. Module mode 0644; entrypoint mode 0755. Absent installs;
exact bytes and metadata preserve idempotently; different bytes or unsafe metadata STOP.
No unexplained preexisting adapter is replaced.

| Relative path | Mode | Git blob | SHA-256 |
| --- | --- | --- | --- |
| `pi4/lib/hioc/home_assistant_association.py` | `0644` | `e71e4c45e21e9f1a25298471b48387cb19f53e1f` | `9a9be5812f3481146de7546875320eb6adec65ca5a2b3230ff5fec378892c7c1` |
| `pi4/bin/hioc-home-assistant-association.py` | `0755` | `2864361fac7cd48e947dac1e4e40aeeeb525adef` | `005fae482a4e2c42b48bfb991abf14ddf1d9de60f81169a2ed1573a767958b8c` |
| `pi4/lib/hioc/core/compatibility.py` | `0644` | `1ba46d4ebf3819e2fa3ee9365e5b0088ba0b4a1a` | `713c292c09282f3be524bc8a2090de43cf0fb78a81b3c71eed143b7a0d68e952` |

### C: complete runtime governance manifest

Owner/group jazofv1:jazofv1, mode 0644. Absent installs reviewed source copy;
exact bytes/metadata preserve; different or unsafe existing objects FAIL CLOSED.
Preparation, correction and implementation records themselves are source review evidence,
not additional production contract files read by the adapter.

| Relative path | Git blob | SHA-256 |
| --- | --- | --- |
| `governance/pe4/pe4-home-assistant-association-state-v1.1.schema.json` | `38c0235b86241caaaf0bc000117bf5635f8b3eb1` | `5cd060ffd0a7a2e0a2b3e61da50ec8e5a418f4251df7305f713c10701b0e6a5d` |
| `governance/pe4/pe4-ha-runtime-credential-provisioning-closure.json` | `4a4f15c50f4726a7518c77dd42080f0aea5bf078` | `ae1aa575799576d7bdbd64670a516fdc1e38cb6c2b5b6fb816211e69987dde18` |
| `governance/pe4/pe4-0c-association-contract.json` | `744f1cf4b6b9c214720bc6e9c84656bc5efce973` | `a48ec696c7e596dde68e252366f84ea46dfa7076a9b1aaff419a993742ed9a58` |
| `governance/pe4/pe4-0c1-association-lifecycle-clarification.json` | `96b4be1185d3f61fd6e5d6914ef27f2d1dae762a` | `de53307023af7c663878aa9e6212d27cf9023c372c69224bf4b186642c11fb0e` |
| `governance/pe4/pe4-ha-association-adapter-implementation-preparation.json` | `7581ea89e40c5fb5b8eca60753b457eac2f4aa28` | `e014ce6a7b70db26f9d643318d93b8da9e6050afedbd09fe73e86e0efbd14d0b` |
| `governance/compatibility-contracts.json` | `84cb92f2cab8f51e6dbf7b1b7415d7e008eded9a` | `83493cacfef10ff85e936bcacbee215797c745e3fa6edff1954c3cc1f3c82227` |

## D: endpoint configuration

Only `/home/jazofv1/hioc/config/hioc.conf` changes, only when the effective assignment is
absent. Add exactly `HIOC_HA_ENDPOINT="ws://192.168.100.251:8123/api/websocket"` and a final LF;
add a separator LF if the existing final line lacks one. Preserve the entire unrelated
byte prefix, comments, order and semantics. Strict UTF-8 prevents ignored-byte ambiguity.
Exactly one ConfigService assignment with the required value is idempotent. Duplicate,
different or export-like ambiguous assignments STOP with CONFIG_CONFLICT. Validate the
merged effective HIOC_HOME and endpoint before mutation and after replacement.
No environment overrides, credential additions or toolkit edits.

Preserve jazofv1 owner/group and existing secure file mode. Root-owned/unwritable config
requiring privilege or unexplained metadata fails rather than introducing a new privilege
boundary. Candidate is fsynced on the same filesystem, precise prior bytes are rechecked,
then os.replace atomically publishes; both affected parent directories are fsynced.
A private 0600 exact config backup is retained in the 0700 deployment namespace; it may
contain unrelated existing configuration, so it is never printed or copied into evidence.
No credential file is copied, hashed, backed up or rewritten.

## Private prerequisites and preexisting-state gates

Associations parent exact jazofv1:jazofv1 0700; permanent .home_assistant.lock exact
jazofv1:jazofv1 0600, regular single link, no ACL/symlink/special object. Absent directory
and lock are journaled then created; valid existing ones are preserved. Lock bytes have
no identity meaning and are preserved. Wrong owner/group/mode/type/binding or unverifiable
ACL stops; no chmod/chown adoption of existing unsafe objects.

Inspect associations with pinned directory FD. Any home_assistant.json, any name beginning
.home_assistant.txn- or .home_assistant.done- stops with
UNEXPECTED_PREEXISTING_ASSOCIATION_STATE before targets/config change. Never open/read
private state content, delete, recover or assume stale. The adapter is not run. Existing
state/inventory, production code parents, config and backups must be secure; all changed
parents must be operator-owned/writable and on the staging filesystem. Missing governance
subdirectories can be created 0755 and are explicitly journaled for possible later rollback.

## E: credential and accepted runtime verification

Credential stays `/etc/hioc/credentials/home_assistant.token`, root:jazofv1 0640;
credential directories root:jazofv1 0750. Invoke the reviewed validator from source with
accepted interpreter -I -B and --runtime-operator, capturing all its output. Verify PASS,
actual operator readability and explicit no network/authentication. Exact token-plus-one-LF
policy and require/remove-one-LF-without-trim remain unchanged. This proves local storage
only, not token validity, revocation, HA permissions or authentication. No token output,
hash, length, prefix/suffix, rotation or backup.

Validator Git blob: `1bbe5826927b6b474db73fd2ace8a304b56dac66`;
SHA-256: `f9ce04a51a5bf07cb841bf0d18ea7ac531e6dc6480534a1f6438c47ec8601aaa`.

Read-only runtime verification uses `/home/jazofv1/hioc/runtime/pe4/active/bin/python`,
active resolving exactly to environments/cpython311-websockets16.1.1-lock-v1.
Require CPython 3.11.2, aarch64, SOABI cpython-311-aarch64-linux-gnu, websockets 16.1.1,
isolated/no-bytecode flags, exact sys.prefix, executable and reviewed sys.path/import origins.
Only the exact reviewed .pth and system sitecustomize identities above are permitted; usercustomize is prohibited. Only websockets/pip/setuptools distributions are allowed.
Validate installed version and package origin without calling connect. Runtime drift stops.
No runtime write, pip install, package update or D/E/F/G rerun. System Python -I -B -S
is only the stdlib bootstrap; the accepted runtime supplies its own separate read-only probe.

## Transaction, interruption and recovery

A dedicated [stdlib deployment helper](../tools/hioc-pe4-ha-association-deploy.py) is necessary
because guarded multi-file additive publication, precise config preservation and interrupted
operation require testable mechanics. It has no adapter import, HA networking, cron mutation,
MQTT, projection, rollback/reset/delete command or production path override.

Use fixed backups/.pe4-ha-association-deployment.lock (operator 0600), nonblocking flock,
and backups/pe4-ha-association-deployment-v1 (operator 0700). Require a maintenance window
without concurrent release/config writers. Do all source, dependency, destination, endpoint,
state, scheduler, runtime and credential preflights before any production mutation; repeat
under the deployment lock. Intent contains only version, exact source commit, fixed target
identities, created-file/directory list, created-lock flag, endpoint-added flag and config
identities/mode. It contains no household/private association data or credential information.

NOT_STARTED: no durable intent. First create namespace and exact private config prior/candidate
backups. PREPARED: canonical 0600 intent durably published and fsynced before any adapter,
governance, endpoint or association prerequisite installation. Stage each reviewed additive
file in that same namespace/filesystem; verify bytes/mode; atomically publish using Linux
renameat2 RENAME_NOREPLACE and fsync both parent directories. Existing exact targets are
preserved. Endpoint uses the separately governed atomic replacement above. Postvalidate
all production targets/config/state prerequisites, then durably publish COMMITTED marker
bound to the intent and source commit. Recheck runtime/credential/scheduler and effective
configuration before reporting success. A postcheck failure reports FAIL with durable
transaction state, never claims adapter execution or automatic rollback.

Interruption after PREPARED: re-run only the same reviewed source commit/block, revalidate
all preconditions and intent/backups, accept only exact prior/candidate config and exact
existing targets, resume missing intended additions and publish/verify COMMITTED. Fully
committed reruns make no target/config changes. Partial unpublished stage bytes that cannot
be verified, an unknown namespace member, source/config drift or malformed journal STOP.
Interruption before durable intent: stop for separate review; no adapter/config/state target
has changed. Preserve all artifacts; no guessed cleanup. Atomic rename prevents partial
visible target files. Journal and backups make incomplete deployment detectable.

## Rollback boundary, defined only

Before any successful or partial adapter execution, a separately reviewed rollback may
remove only exact files proved created by this intent, restore exact prior config bytes
only if endpoint_added is true and current bytes are precisely this candidate, and remove
only the created lock/empty created directories after confirming no association state or
transaction exists. Preserve all preexisting exact files and prerequisites. Validate marker,
source, hashes, metadata and identity immediately before each action. Use explicit names;
never wildcard-delete. A failed/partial rollback retains evidence and stops for review.
There is no automatic rollback and this helper exposes no deletion option.

After any successful or partial adapter execution, preserve home_assistant.json,
binding_history, txn/done/recovery material, credential, runtime, canonical inventory and
compatibility history. Disable scheduling under its separate governance before later code
rollback; older code unable to consume schema 1.1 must fail closed. Never erase private
state/history to make an older release work. Existing release installer/upgrade/rollback
are inspected but not invoked or changed; their broad rsync/cron behavior is outside this
adapter boundary. External /etc credential ownership remains outside release ownership.

## Scheduler, later execution and bounded evidence

Read only jazofv1 crontab -l. Active filename or HIOC_PE4_HA_ASSOCIATION marker stops;
comments alone do not. A missing crontab is accepted only through its exact bounded
no-crontab diagnostic; other read failures stop. No job is installed/removed. Future
cadence 5,35 * * * *, user jazofv1, remains separately governed. Other schedulers and any
non-cron recurring mechanism require operator review; this preparation does not assert
remote scheduler absence from repository evidence.

Deployment stops after production-file verification, ADAPTER_EXECUTED=FALSE,
HA_NETWORK_ATTEMPTED=FALSE, HA_AUTHENTICATION_ATTEMPTED=FALSE,
SCHEDULER_DEPLOYMENT=NOT_STARTED. First invocation belongs separately to
PE-4 Home Assistant Association Adapter Bounded Manual Production Validation, followed
by Independent Production Acceptance, then Scheduler Deployment.

Evidence fields are the exact closed allowlist in the record: TARGET, SOURCE_COMMIT,
SOURCE_BINDING, PRODUCTION_DEPENDENCIES, RUNTIME_VALIDATION, CREDENTIAL_LOCAL_VALIDATION,
ENDPOINT_CONFIGURATION, STATE_DIRECTORY_VALIDATION, PREEXISTING_ASSOCIATION_STATE,
MODULE_DEPLOYMENT, ENTRYPOINT_DEPLOYMENT, RUNTIME_GOVERNANCE_DEPLOYMENT,
SCHEDULER_PRESENT_BEFORE, SCHEDULER_DEPLOYMENT, ADAPTER_EXECUTED, HA_NETWORK_ATTEMPTED,
HA_AUTHENTICATION_ATTEMPTED, PRODUCTION_DEPLOYMENT, ROLLBACK, RESULT, ERROR_CODE,
DEPLOYMENT_TRANSACTION. Values are fixed PASS/FAIL/NOT_PROVEN, ABSENT/FALSE/NOT_STARTED,
NOT_PERFORMED, finite failure codes, transaction states and a 40-hex commit. Failure
never implies a failed prerequisite passed. No token, MAC, inventory IP, registry/entity
ID, household name or exception text. The approved fixed endpoint appears only in source
policy/docs, not runtime evidence. Git remote synchronization is repository work only;
future production deployment performs no remote/network operation.

## Validation and lifecycle

50 focused synthetic tests, including every manifest/policy gate, native security checks,
interruptions at every durable publication boundary and idempotence. Required regressions:
adapter/correction 70, 0C 14, 0C.1 13, implementation preparation 13, credential provisioning
44, credential closure 9, 2b closure 3, Master Plan 5, inventory 123, compatibility 40,
release 11 (one existing rsync-unavailable Windows skip). Total 395 run, 394 passed, one
skipped. Syntax with bytecode disabled, import safety, canonical record/closed schema,
links, source identities, privacy/prohibited operations and diff checks pass. This is
synthetic repository evidence; native Linux target/metadata/runtime proofs are future
operator preflight, not claimed already observed.

| Boundary | Status |
| --- | --- |
| Adapter Implementation | PASS/CLOSED, corrected before deployment |
| Deployment Preparation | PASS/CLOSED |
| Deployment | NOT STARTED |
| Bounded Manual Production Validation | NOT STARTED |
| Independent Production Acceptance | NOT STARTED |
| Scheduler Deployment | NOT STARTED |
| Public Projection | DEFERRED |
| PE-4 | NOT COMPLETE |
| Phase 7A | ACTIVE |
| Rollback | NOT PERFORMED |

No PI3/PI5/HA access, real credential access, adapter/network execution, production
mutation, deployment, scheduler activation, MQTT, public projection or rollback occurred.
Next exactly: **PE-4 Home Assistant Association Adapter Deployment Execution**.

## Historical deployment block — executed by operator at 4912f20d

Historical block only; do not rerun as part of closure. The operator previously bound EXPECTED to the exact single
corrective successor commit before separate authorization. The final repository report
provides the literal completed corrective commit. The block verifies helper/record/schema against
both reviewed SHA-256 and that Git commit before starting the source-bound helper. It does
not assume cwd, fetch, SSH, invoke the adapter or perform manual validation. Explicit
Python/shell return codes always return control to the existing interactive shell; no
shell set flags, exit, exec or logout.

```sh
# FOR REVIEW ONLY - DO NOT RUN WITHOUT SEPARATE DEPLOYMENT AUTHORIZATION
# TARGET=PI3 NUT&PIHOLE
/usr/bin/python3 -I -B -S - <<'PY'
import hashlib, os, subprocess, sys
from pathlib import Path
EXPECTED = "4912f20d8b2ff78dcdaf8b3e0f52e57d5de5e3a2"
ROOT = Path("/home/jazofv1/hioc-release-source")
FILES = {
    "tools/hioc-pe4-ha-association-deploy.py": "9f1903c99206348722584a976c57ac9e1bcbf53178e0c8d472719687259a48da",
    "governance/pe4/pe4-ha-association-adapter-deployment-preparation.json": "89fee5a30d0e3d5f3c1dfc395b823119769676a0e9e376a754f49b479c418b1e",
    "governance/pe4/pe4-ha-association-adapter-deployment-preparation.schema.json": "9a5adb872098762b5997c834c62ee57c4393352d60ebe90c3da565160d99bb45",
    "governance/pe4/pe4-ha-association-production-dependency-correction.json": "727a66984d1a79880fcafa18161a512b19b2da5498dda0225e0ac4ba5c7377bc",
    "governance/pe4/pe4-ha-association-production-dependency-correction.schema.json": "82129797f7a650962757026218fc726446c57002c179ffcffadaafbdf8cc9e80",
}
ENV = {"PATH": "/usr/sbin:/usr/bin:/bin", "HOME": "/home/jazofv1", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
rc = 1
try:
    if len(EXPECTED) != 40 or any(c not in "0123456789abcdef" for c in EXPECTED):
        raise ValueError("binding")
    for path, expected_sha in FILES.items():
        raw = (ROOT / path).read_bytes()
        committed = subprocess.run(["/usr/bin/git", "-C", str(ROOT), "show", EXPECTED + ":" + path], env=ENV, stdin=subprocess.DEVNULL, capture_output=True, timeout=15)
        if committed.returncode or raw != committed.stdout or hashlib.sha256(raw).hexdigest() != expected_sha:
            raise ValueError("binding")
    result = subprocess.run(["/usr/bin/python3", "-I", "-B", "-S", str(ROOT / "tools/hioc-pe4-ha-association-deploy.py"), "--expected-commit", EXPECTED], stdin=subprocess.DEVNULL, check=False)
    rc = result.returncode
except BaseException:
    report = {'TARGET': 'PI3 NUT&PIHOLE', 'SOURCE_COMMIT': 'INVALID', 'SOURCE_BINDING': 'FAIL', 'PRODUCTION_DEPENDENCIES': 'NOT_PROVEN', 'RUNTIME_VALIDATION': 'NOT_PROVEN', 'CREDENTIAL_LOCAL_VALIDATION': 'NOT_PROVEN', 'ENDPOINT_CONFIGURATION': 'NOT_PROVEN', 'STATE_DIRECTORY_VALIDATION': 'NOT_PROVEN', 'PREEXISTING_ASSOCIATION_STATE': 'NOT_PROVEN', 'MODULE_DEPLOYMENT': 'NOT_PROVEN', 'ENTRYPOINT_DEPLOYMENT': 'NOT_PROVEN', 'RUNTIME_GOVERNANCE_DEPLOYMENT': 'NOT_PROVEN', 'SCHEDULER_PRESENT_BEFORE': 'NOT_PROVEN', 'SCHEDULER_DEPLOYMENT': 'NOT_STARTED', 'ADAPTER_EXECUTED': 'FALSE', 'HA_NETWORK_ATTEMPTED': 'FALSE', 'HA_AUTHENTICATION_ATTEMPTED': 'FALSE', 'PRODUCTION_DEPLOYMENT': 'NOT_STARTED', 'ROLLBACK': 'NOT_PERFORMED', 'RESULT': 'FAIL', 'ERROR_CODE': 'SOURCE_BINDING', 'DEPLOYMENT_TRANSACTION': 'NOT_STARTED'}
    for key, value in report.items():
        print(key + "=" + value)
raise SystemExit(rc)
PY
hioc_deployment_rc=$?
printf 'DEPLOYMENT_BLOCK_RETURN_CODE=%s\n' "$hioc_deployment_rc"
unset hioc_deployment_rc
```
