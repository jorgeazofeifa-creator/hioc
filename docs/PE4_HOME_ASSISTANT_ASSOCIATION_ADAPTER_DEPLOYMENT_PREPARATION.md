# PE-4 Home Assistant Association Adapter Deployment Preparation


## Current pre-execution governance and evidence correction — 2026-10-06

Deployment Preparation PASS/CLOSED, corrected before execution. Historical preparation
commit `0040bdc79e66c10db4f180f952d04f97b1070065` passed repository tests but independent
review found an incorrect additive policy on category B and ambiguous/control-flow-based
transaction evidence. No deployment, helper/adapter execution or HA authentication occurred.
The [dedicated correction record](../governance/pe4/pe4-ha-association-adapter-deployment-preparation-correction.json)
and [closed schema](../governance/pe4/pe4-ha-association-adapter-deployment-preparation-correction.schema.json)
bind the corrected helper and current preparation record/schema. The historical commit
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
[current correction](../governance/pe4/pe4-ha-association-adapter-predeployment-correction.json)
and [credential closure](../governance/pe4/pe4-ha-runtime-credential-provisioning-closure.json)
remain authority. Current closure overrides historical optional-LF wording.

## Complete static runtime dependency audit

Entrypoint imports only hioc.home_assistant_association after inserting installed
pi4/lib. Adapter's dynamic HIOC imports are core.config.ConfigService;
core.compatibility.safe_version, STATES, GOOD, load_registry, assess and update_status;
and core.state.StateStore. Package initializers execute during these imports.
StateStore transitively imports core.schemas.Schema. Their APIs, initializers and
source bytes are all in category B below; no broad existing-code replacement is allowed.
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
| `pi4/lib/hioc/core/compatibility.py` | `1ba46d4ebf3819e2fa3ee9365e5b0088ba0b4a1a` | `713c292c09282f3be524bc8a2090de43cf0fb78a81b3c71eed143b7a0d68e952` |
| `pi4/lib/hioc/core/state.py` | `2be5b599f3822b859a5ca92cd046905255a2923f` | `ff907db9b5a8a9cfb1413c8670475a9ff5f80203f553f12d1e565be42717772d` |
| `pi4/lib/hioc/core/schemas.py` | `7f2bbe7264c1b02294bbebfed65c2745d559c706` | `7db98c3cb8d6030faf81454b7bc473ba8459b3a7c9e32377bb9a0b64e3d4fe1e` |

### A: primary additive code targets

Owner/group jazofv1:jazofv1. Module mode 0644; entrypoint mode 0755. Absent installs;
exact bytes and metadata preserve idempotently; different bytes or unsafe metadata STOP.
No unexplained preexisting adapter is replaced.

| Relative path | Mode | Git blob | SHA-256 |
| --- | --- | --- | --- |
| `pi4/lib/hioc/home_assistant_association.py` | `0644` | `0c049b7ee19b6b20c3fef53717455ba341d4a149` | `cf04d05f6215b9654539df69797de49a831044795ba8f7f5b3432d9d35a086b9` |
| `pi4/bin/hioc-home-assistant-association.py` | `0755` | `2864361fac7cd48e947dac1e4e40aeeeb525adef` | `005fae482a4e2c42b48bfb991abf14ddf1d9de60f81169a2ed1573a767958b8c` |

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
No .pth/site/user customization; only websockets/pip/setuptools distributions allowed.
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

## Complete future operator block — FOR REVIEW ONLY

DO NOT RUN in this preparation. Independent review must bind EXPECTED to the exact single
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
EXPECTED = "REPLACE_WITH_INDEPENDENTLY_REVIEWED_PREPARATION_COMMIT"
ROOT = Path("/home/jazofv1/hioc-release-source")
FILES = {
    "governance/pe4/pe4-ha-association-adapter-deployment-preparation-correction.json": "bcf5338a7d8735a8ff16ada200985d6cc48e5a65c7f860ab083f3b5aed05f5cb",
    "governance/pe4/pe4-ha-association-adapter-deployment-preparation-correction.schema.json": "06b703a89cd021b2c9df82ba9aeb2022a37a984b9e101f4f322ac54deec6c382",
    "tools/hioc-pe4-ha-association-deploy.py": "2510f8996e80f2b779a9764bc5c685808f3f0d6ec64adc3fabbcebaf0d0e588c",
    "governance/pe4/pe4-ha-association-adapter-deployment-preparation.json": "744c67b9f638ed0d66c1bc9c4d9e6f81c7fea47a9ca11d4fc4ff4b6490d984d0",
    "governance/pe4/pe4-ha-association-adapter-deployment-preparation.schema.json": "31a5e50caadb78e79059e94547d854346458eabde92e2024f9ca497bf9cba544",
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
