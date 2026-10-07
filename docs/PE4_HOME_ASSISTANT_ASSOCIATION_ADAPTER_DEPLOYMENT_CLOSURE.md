# PE-4 Home Assistant Association Adapter Deployment Closure

Deployment Execution: PASS/CLOSED. Deployed source commit:
`4912f20d8b2ff78dcdaf8b3e0f52e57d5de5e3a2`.

The [canonical closure record](../governance/pe4/pe4-ha-association-adapter-deployment-closure.json)
and [closed schema](../governance/pe4/pe4-ha-association-adapter-deployment-closure.schema.json)
bind two separate OPERATOR_SUPPLIED_PRODUCTION_EVIDENCE sets, both provenance
OPERATOR_SUPPLIED. Codex performed repository-only governance work and did not observe
PI3, execute deployment or collect live evidence. This record is repository governance;
it is not consumed by Runtime.contracts() or installed as a runtime contract.

## Deployment and separate static acceptance

The fourth governed attempt was the first to reach durable intent and COMMITTED.
Deployment RESULT PASS, ERROR_CODE COMPLETE, block return code 0. Source/dependency/runtime,
local credential, endpoint/state-directory, module/entrypoint/runtime-governance checks all PASS.
Preexisting association state ABSENT; association scheduler absent before deployment;
scheduler NOT_STARTED; adapter/network/authentication FALSE; rollback NOT_PERFORMED.

The later independent static verification was MODE READ_ONLY, RESULT PASS, FAILURE_COUNT 0.
It verified source identity, five required dependencies, nine deployed targets, durable
transaction authority, endpoint configuration, private-state/scheduler boundaries,
platform-status preservation and compatibility-state preservation. This static deployment
acceptance is distinct from the future Independent Production Acceptance of adapter behavior,
which remains NOT STARTED. The verifier executed no adapter, accessed no credential,
attempted no HA network, changed no production/scheduler and published no MQTT.

## Historical attempts

| Attempt | Source commit | Error/result | Transaction / production deployment |
| --- | --- | --- | --- |
| 1 | `2ef66a2d575c923c6939a4cd4d5bb2c8aab2f816` | RUNTIME_DRIFT / FAIL | NOT_STARTED / NOT_STARTED |
| 2 | `e4d5a19afecccb1584708e3da57ba3c0c4258523` | RUNTIME_DRIFT / FAIL | NOT_STARTED / NOT_STARTED |
| 3 | `84635cb88380c590d2adfb655c37afd2118c629f` | DEPENDENCY_DRIFT / FAIL | NOT_STARTED / NOT_STARTED |

Attempt 1 implemented no-unreviewed customization as blanket rejection; attempt 2 used
raw sys.prefix through the governed active symlink; attempt 3 misclassified the absent
compatibility module as an existing production dependency. Each failed before intent;
none partially deployed code or performed rollback. Corrections and their historical
records remain immutable. The successful fourth attempt does not change those outcomes.

## Exact deployed manifests

Five dependencies retain REQUIRED_EXISTING_EXACT_PRESERVE_ABSENT_OR_DIFFERENT_FAIL_CLOSED.
Nine additive files were created exactly. Their code-file installation never executes
compatibility refresh/update, platform-status, the adapter, MQTT or HA. The six runtime
governance contracts remain unchanged; correction/closure records are not additional targets.

| Preserved dependency | SHA-256 |
| --- | --- |
| `pi4/lib/hioc/__init__.py` | `5052b317d5f9fa47aba366a41393caac93406ea63f98f047783bbb2e70e221b2` |
| `pi4/lib/hioc/core/__init__.py` | `043f9848cddfd3c37f153244107ea4c6b5965f26887da049d07ebd6bf4b01dbc` |
| `pi4/lib/hioc/core/config.py` | `ceb59f81cb5e247b929754603f2aaeee29e12897cf45cff5c0612ba1ecd261f7` |
| `pi4/lib/hioc/core/state.py` | `ff907db9b5a8a9cfb1413c8670475a9ff5f80203f553f12d1e565be42717772d` |
| `pi4/lib/hioc/core/schemas.py` | `7db98c3cb8d6030faf81454b7bc473ba8459b3a7c9e32377bb9a0b64e3d4fe1e` |

| Newly created target | SHA-256 |
| --- | --- |
| `pi4/lib/hioc/home_assistant_association.py` | `9a9be5812f3481146de7546875320eb6adec65ca5a2b3230ff5fec378892c7c1` |
| `pi4/bin/hioc-home-assistant-association.py` | `005fae482a4e2c42b48bfb991abf14ddf1d9de60f81169a2ed1573a767958b8c` |
| `pi4/lib/hioc/core/compatibility.py` | `713c292c09282f3be524bc8a2090de43cf0fb78a81b3c71eed143b7a0d68e952` |
| `governance/pe4/pe4-home-assistant-association-state-v1.1.schema.json` | `5cd060ffd0a7a2e0a2b3e61da50ec8e5a418f4251df7305f713c10701b0e6a5d` |
| `governance/pe4/pe4-ha-runtime-credential-provisioning-closure.json` | `ae1aa575799576d7bdbd64670a516fdc1e38cb6c2b5b6fb816211e69987dde18` |
| `governance/pe4/pe4-0c-association-contract.json` | `a48ec696c7e596dde68e252366f84ea46dfa7076a9b1aaff419a993742ed9a58` |
| `governance/pe4/pe4-0c1-association-lifecycle-clarification.json` | `de53307023af7c663878aa9e6212d27cf9023c372c69224bf4b186642c11fb0e` |
| `governance/pe4/pe4-ha-association-adapter-implementation-preparation.json` | `e014ce6a7b70db26f9d643318d93b8da9e6050afedbd09fe73e86e0efbd14d0b` |
| `governance/compatibility-contracts.json` | `83493cacfef10ff85e936bcacbee215797c745e3fa6edff1954c3cc1f3c82227` |

The supplied compatibility SHA text has 63 characters. The specified Git blob
`1ba46d4ebf3819e2fa3ee9365e5b0088ba0b4a1a` and deployed source commit establish the
64-character SHA in the manifest. The closure preserves the supplied transcription
separately from verified source identity; Codex does not independently claim live bytes.

## Durable transaction and endpoint

Journal: `/home/jazofv1/hioc/backups/pe4-ha-association-deployment-v1`.
Static acceptance proved exact journal security, canonical intent bound to source commit,
nine target hashes, prior/candidate configuration hashes and a canonical COMMITTED marker
bound to the intent SHA-256. Target count 9; created-file count 9; endpoint_added true.
NOT_STARTED -> NOT_STARTED, PREPARED -> INCOMPLETE, COMMITTED -> PASS remains unchanged.
No rollback behavior was added; no additional changed production files are inferred.

Config-prior/candidate hashes matched intent; candidate equaled the governed transformation
of prior; production configuration equaled candidate. Approved endpoint:
`ws://192.168.100.251:8123/api/websocket`. No unrelated config content or secrets are stored.

## Private state, scheduler and preserved platform

The governed association directory and lock were created/validated without running the
adapter. PRE_ADAPTER_PRIVATE_STATE ABSENT: no home_assistant.json, .home_assistant.txn-*
or .home_assistant.done-* existed. Association publication and lifecycle execution
NOT_STARTED; HA association results NONE YET. No first adapter command is supplied here.

Association scheduler absent; Scheduler Deployment NOT_STARTED. Existing platform cron
remains unchanged:

```text
17 3 * * * flock -n /tmp/hioc-platform-status.lock /home/jazofv1/hioc/pi4/bin/hioc-platform-status.py
```

Platform-status SHA-256 remains the known pre-compatibility generation:
`b65464e722bf9a4da0004ecf3bb05e4105f345a87c62405ce92d97c6298b2af8`.
It was not deployed, replaced or executed by this deployment. Static acceptance observed
compatibility-state metadata unchanged: size 39536; mtime
`2026-10-06 12:25:11.049013060 -0600`. COMPATIBILITY_STATE_PRESERVATION PASS;
no compatibility-state contents are stored.

## Credential semantics and limits

Deployment CREDENTIAL_LOCAL_VALIDATION PASS used the already governed local credential
validator. Credential file access belongs to that validation; do not claim deployment
never read it. Content exposed in evidence/output false; persisted into new deployment
evidence false; placed in argv false; placed in environment false; used for HA authentication
false; HA network/authentication false; Codex credential access false. Later static acceptance
CREDENTIAL_ACCESSED_BY_THIS_CHECK false. Local validation does not prove HA authentication.

## Current lifecycle and next task

| Boundary | State |
| --- | --- |
| adapter implementation | PASS CLOSED CORRECTED BEFORE DEPLOYMENT |
| bounded manual production validation | NOT STARTED |
| deployment | PASS CLOSED |
| deployment preparation | PASS CLOSED CORRECTED AND REBOUND |
| deployment runtime probe correction | PASS CLOSED |
| independent production acceptance | NOT STARTED |
| pe4 | NOT COMPLETE |
| phase7a | ACTIVE |
| production dependency classification correction | PASS CLOSED |
| public projection | DEFERRED |
| rollback | NOT PERFORMED |
| runtime validation correction | PASS CLOSED |
| scheduler deployment | NOT STARTED |

Exact next task: **PE-4 Home Assistant Association Adapter Bounded Manual Production Validation**.
The deployed adapter has not been executed, contacted HA, attempted authentication or
published association state. No association scheduler exists. The first adapter run
requires separate authorization. This closure provides no live execution procedure and
stops before that checkpoint. [Master Plan](HIOC_MASTER_PLAN.md) owns the authoritative
current lifecycle and next task; [historical deployment preparation](PE4_HOME_ASSISTANT_ASSOCIATION_ADAPTER_DEPLOYMENT_PREPARATION.md)
preserves the source-bound block that was executed at 4912f20d.

Validation: closure 24; existing regressions 453; total 477 run, 476 passed, one existing
release skip because rsync is unavailable on Windows. Syntax with bytecode disabled,
import safety, canonical closed schemas, links, immutable deployed source identities,
privacy/prohibited-operation checks and diff checks are repository-only.
