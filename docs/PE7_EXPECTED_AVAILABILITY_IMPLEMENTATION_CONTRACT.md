# PE-7 Expected Availability and Permanent IoT Monitoring Implementation Contract

Status: PE70_STATUS=PREPARED_PENDING_INDEPENDENT_ACCEPTANCE.
PE-7.0 is NOT COMPLETE/PASS. PE71_STARTED=FALSE; implementation and production
remain unauthorized. Baseline: main at 77fab0723cf8fa02ca3536e71e1a98dc63b019a1.
All technical selections below are prepared design decisions awaiting independent
acceptance, not claims about installed capabilities. No Git publication is authorized.

## 1. Authority and boundaries

The original PE-7 foundation requirements, PE-7.0 authorization and subsequent
write-interface decision are cumulative. The operator selected a dedicated HA
operator-service integration with a narrowly scoped authenticated HIOC AssetService
adapter. Architecture approval grants no implementation, service, credential,
Dashboard, migration, deployment or production permission.

Authorities: [Master Plan](HIOC_MASTER_PLAN.md),
[three-layer architecture](PASSIVE_ENRICHMENT_ARCHITECTURE.md),
[Asset specification](PE2_ASSET_FOUNDATION_SPEC.md),
[Asset implementation](PE2_ASSET_IMPLEMENTATION_DESIGN.md),
[Dashboard architecture](DASHBOARD_ARCHITECTURE.md),
[incident model](INCIDENT_MODEL.md),
[HA association contract](PE4_HOME_ASSISTANT_ASSOCIATION_CONTRACT.md),
[PE-6 design](PE6_CLASSIFICATION_CONTRACT_DESIGN.md), and
[acceptance workflow](PE6_INDEPENDENT_ACCEPTANCE_WORKFLOW.md).
PE-6/PE-6.5 remain COMPLETE/PASS. The second PE-6.4 receipt remains unchanged
INSUFFICIENT_EVIDENCE; third-execution acceptance remains distinct. Original records,
schemas, receipts and requirements are not rewritten. Current Master Plan lifecycle
overrides explicitly historical snapshots.

PE-7 covers permanent wall/smart switches, plugs, Sonoff, lighting controls, routers
and other operator-selected Assets; qualified network/HA correlation; failure to
reconnect; actionable incidents, notifications and recovery guidance. Intent never
rewrites observation, identity, canonical IP, public roles, inventory health or
classifier inference. Unrelated monitoring remains intact. Existing confirmed
function references may inform guidance, but full automation impact is PE-8,
technical dependency/topology PE-9 and usable capability/service assurance PE-10.
No retention/archive, DHCP capacity, canonical-address hardening, Active Discovery,
surveillance implementation or global notification-severity redesign is included.

## 2. Mandatory controls and exact fields

EXPECTED_AVAILABILITY_DASHBOARD_TOGGLE=MANDATORY
INFRASTRUCTURE_DEVICE_DASHBOARD_TOGGLE=MANDATORY
INFRASTRUCTURE_TYPE_SELECTOR=MANDATORY_WHEN_ENABLED
TOGGLE_INDEPENDENCE=REQUIRED
OPERATOR_OWNED_PERSISTENCE=REQUIRED

| Field | Exact type/default | Effective meaning |
| --- | --- | --- |
| expected_availability | boolean or null; null | Only true enables PE-7; false explicit OFF; null unconfigured/effective OFF. |
| infrastructure_device | boolean or null; null | Only true activates operator-confirmed infrastructure designation. |
| infrastructure_type | null or identifier below; null | Unassigned / Unknown when null; inactive unless infrastructure_device=true. |

Exact taxonomy: router_gateway, raspberry_pi_server, network_switch,
wireless_access_point_mesh_node, smart_home_hub_bridge, other_infrastructure.
Display labels respectively: Router / Gateway; Raspberry Pi / Server; Network
Switch; Wireless Access Point / Mesh Node; Smart Home Hub / Bridge; Other
Infrastructure. Retain manufacturer/model/product separately. Unknown identifiers
fail validation; future additions require versioned capability/schema approval,
not destructive remapping or silent conversion to Other.

All four ON/OFF combinations work. Neither toggle writes the other. Type changes
write neither toggle. Booleans exclude strings/integers. Infrastructure ON implies
no criticality, severity, dependency, service guarantee or expected-online policy.
Discovery, hostname, manufacturer, online history, HA membership and classification
never set/overwrite these values. Type retained while infrastructure OFF is inactive;
re-enable restores it visibly without touching Expected Availability.

## 3. Asset successor schema and transactions

Select schema_version string 2.0 in the SAME authoritative assets.json. This is an
explicit successor, not a reinterpretation of frozen 1.0. Strict version dispatch
preserves legacy 1.0 validation/canonical behavior; unsupported versions, extra or
duplicate JSON keys, nonfinite numbers, invalid UTF-8 and malformed data fail closed.
No reads/startup/installer silently initialize, migrate, repair or downgrade.

Exact top-level keys: schema_version, updated_at, asset_count, assets, store_epoch,
store_revision, policy_requests. First four retain existing meaning. store_epoch is
UUID4 lowercase hex32; store_revision integer >=1 excluding bool. policy_requests
is a bounded receipt list (section 6), initially empty. Exact record keys: the nine
existing stable_device_id, friendly_name, physical_location, purpose, notes,
created_at, updated_at, update_source, revision PLUS the three section 2 fields.
ID equals dictionary key and matches ^dev_[0-9a-f]{16}$. Existing field normalization,
lengths, timestamp grammar remain. update_source is operator_cli or operator_ha;
record revision integer >=1. Creation revision 1; content mutation increments once.

A record with explicit true OR false policy, or retained non-null type, is meaningful
even with all four descriptive fields null. Clearing descriptive fields must not
remove it. No implicit deletion of 2.0 Assets. Removal is a separate governed local
operation; adapter cannot delete, restore, migrate, edit arbitrary fields or paths.

AssetService remains sole Asset writer; extend its versioned APIs, not direct file
mutation or a competing policy store. Existing lock/backup/temp/fsync/replace/status
sequence and private modes remain. AssetService writers hold only the Asset lock
and Asset-local backup/status operations; no inventory/PE-4/PE-5 lock acquisition.
Normal evaluation snapshots policy then releases that lock before incident work.
The sole new notification-authorization/claim exception is section 10's ordered
shared Asset read guard -> exclusive incident lock, held only for validation and
durable outbox authorization/claim, never network I/O. No code may acquire Asset while holding
incident. This prospective PE-7 ordering does not rewrite the historical PE-2 law.

2.0 serialization: UTF-8, two spaces, one LF, keys in stated order, Asset IDs lexical,
existing NFC text rules. Store/status 0600 and expected owner; backup directory 0700,
files 0600, existing parent safety checks. Status retains its exact existing key set,
values and meanings with schema_version=2.0. New read/write code handles paired
store/status explicitly; neither a status failure nor missing inventory deletes data.

Migration is an explicit local AssetService command, not Dashboard/adapter startup.
Preflight exact source bytes/hash, valid 1.0 schema, path/owner/mode/lock and no old
writer using the store. Under exclusive lock: validated exact-byte pre-mutation
backup; construct 2.0; validate; same-directory unique temp; flush/fsync/chmod;
reread; replace; parent fsync; status; verify. IDs, four descriptive values,
created_at/updated_at, record revisions and original update_source survive unchanged
as logical values. New fields null; new epoch; store_revision=1; receipts empty.
Orphans remain. Missing store needs explicit local initialization, not a GET.

Preserve post-replace failure law: return COMMIT_UNKNOWN on uncertain fsync/status;
never guess success, auto-restore or retry mutation. Explicit read-only reconciliation
establishes actual store/receipt state; repairs need separate operator authority.
Rollback stops new writers/evaluation, backs up current 2.0 and validates old backup.
After new policy edits, rollback requires explicit disposition retaining their exact
private evidence; never silently lose intent. Restore rotates store_epoch to prevent
ABA replay, even if record revisions recur. Old writers cannot resume against 2.0.

### Correction A: version-aware PE-6 Asset consumption

Select ONE version-aware PE-6 consumer extension, not a schema 1.0 projection.
At the Asset-source boundary, dispatch on the ORIGINAL store schema_version:
1.0 -> exact preserved legacy validator; 2.0 -> a separate strict 2.0 validator
covering the complete section 3 schema, including receipt metadata. Validation
precedes use of any field. The legacy validator still rejects operator_ha, unknown
keys, empty descriptive records and unsupported versions as originally required;
it is never relaxed or used on a relabelled 2.0 object. No projection rewrites
update_source to operator_cli or hides otherwise valid descriptive records.

The version-aware PE-6 Asset branch replaces only its single-version validation
call during separately authorized PE-7.1. PE-6's raw/value/digest capture, secure
Reader, Asset lock/recheck and unchanged result schema remain. Pass original 2.0
raw bytes, their actual SHA-256 and exactly parsed 2.0 value through its existing
source wrapper. The closed source wrapper is not extended or populated with
invented provenance. Original Asset update_source remains operator_ha/operator_cli
in the authoritative value, unchanged in storage and input proof. Output source
hash binds that original store, not an invented 1.0 encoding. No extra transform
identity is needed because no format transform occurs.

After successful version-specific validation, the existing Asset-documentation
calculation reads only friendly_name, physical_location and purpose from each
matched record; notes remain private. New policy/infrastructure fields confer no
role, criticality, identity, availability, health or physical classification within
PE-6. Policy-only 2.0 records are valid Assets with incomplete descriptive metadata,
not invalid source data and not deleted/omitted. Existing descriptive records have
the same classification semantics; a new source revision naturally has a new raw
digest. Do not claim byte-identical provenance after actual source bytes change.

Malformed/unsupported/future Asset versions follow the existing Asset-source
rejection path: source INVALID (or UNAVAILABLE for read/permission failure), with
no usable value and no descriptive inference; other valid independent sources
continue under existing PE-6 rules. No fallback to legacy parsing, stripping keys,
auto-migration, partial acceptance or pretending malformed data is ABSENT. Existing
historical PE-6 records/schemas/tests retain their original accepted Git authority;
new compatibility fixtures protect the explicitly versioned extension separately.
Existing PE-6 source byte/device/revision safety limits still apply to both versions;
resource-limit rejection remains explicit LIMIT_EXCEEDED, not a provenance rewrite
or a claim that a valid Asset is malformed. Version/provenance compatibility covers
all permitted record shapes within those unchanged supported consumer limits.

| Example | Declared validation and PE-6 behavior | Provenance/migration outcome |
| --- | --- | --- |
| A01: 1.0 CLI record | Exact legacy validator; original PE-6 descriptive behavior. | operator_cli and original raw digest preserved. |
| A02: 2.0 CLI record | Full 2.0 validation; same descriptive-field calculation. | operator_cli retained; no 1.0 projection. |
| A03: 2.0 HA-edited record with descriptions | Full 2.0 validation accepts operator_ha; descriptions remain usable. | operator_ha retained verbatim; original 2.0 bytes/digest used. |
| A04: 2.0 HA policy-only record | Full 2.0 validation; descriptive quality incomplete; policy not imported into PE-6 conclusions. | Record remains present; operator_ha and source digest retained. |
| A05: migrated store with earlier CLI records and later HA records | All records have full 2.0 shape; different permitted update_source values coexist. | Migration supplies null policy fields for old records, preserves metadata/provenance. |
| A06: mixed 1.0-shaped and 2.0-shaped records in one store | Invalid: one top-level version owns one complete closed record shape. | Atomic migration exposes complete old OR complete new store, never a partial mixed schema. |
| A07: malformed or future version | Existing source rejection semantics, no weaker fallback; no metadata inferred. | Original private evidence retained; no repair or rewrite. |
| A08: rollback to pre-migration backup | Stop 2.0 writers/evaluation, retain later edits privately under explicit rollback disposition, validate/restore exact old 1.0 backup and paired status. | Old 1.0 validator/consumer works again; historical operator_cli provenance unchanged. |

Before explicit migration, install the version-aware reader while 1.0 still works;
then migrate atomically. Both versions remain readable, but no per-record migration
is allowed. Rollback to 1.0 never adds a 2.0 epoch field to old bytes; adapter refuses
2.0 edits against 1.0. A later migration creates a new 2.0 epoch, so old requests
cannot regain authority. Rollback does not silently lose post-migration intent.

PE-7.1 must test A01..A08, every permitted update_source across descriptive and
policy-only records, malformed/extra/unsupported fields, mixed-shape rejection,
byte/digest/value equality, source-change recheck, no policy-derived classification,
legacy-case equivalence and truthful original provenance. Include exact historical
PE-6 replay and migration/rollback readers; modify no historical acceptance evidence.
C04's retained compatibility/provenance criterion is fulfilled by these version-aware
positive cases plus a negative test forbidding false schema 1.0 provenance projection;
its other schema/metadata requirements and the 24-row matrix remain unchanged.
Section 13's retained bounded projection scope concerns operational incident/HA
presentation; it does not reintroduce a legacy-format Asset provenance projection.

Schema closure rules: 2.0 store/record and receipt keys above are all required;
all dictionaries reject unknown keys. policy_requests array length <=1024; no
negative/bool revisions; embedded receipt IDs follow existing Asset/UUID grammar,
digests hex64, expires_at existing UTC grammar, committed revisions positive integers,
outcome exact enum. asset_count equals dictionary length. New booleans may be null;
record revision/epoch never null. Retained type while infrastructure OFF/null is
valid but inactive. Ordinary users cannot inject update_source/revisions/timestamps.
Malformed receipt metadata makes store invalid, never a reason to discard replay
protection and continue writing. Existing Asset file size/encoding/safe-path limits
remain enforced; overload returns unavailable, not partial destructive migration.

## 4. Identity and explicit Asset creation

Rendering discovered devices creates no Asset. New Create Asset and Save requires
explicit operator action, authorized actor, valid fresh inventory context, unique
normalized MAC-to-device ownership, strong-ID rederivation agreement and no conflict.
Use stable ID, never current IP, hostname, row position or HA entity ID. Valid ID
syntax alone is insufficient. Weak/ambiguous identity disables creation with reason.

Existing Assets survive disappearance; orphan records remain locally editable.
Dashboard OFF and infrastructure edits may update an existing authorized orphan,
but ON requires proved current strong attachment. Explicit orphan creation remains
local CLI-only, never an adapter flag; it confers no identity/observation authority.
Evaluator preserves intent but returns UNKNOWN_IDENTITY for unsafe attachment.
IP changes with unchanged ID preserve intent. Rotated MAC/new ID remains distinct;
no heuristic metadata copy, physical-Asset merge or alias migration. Those need
separate future authority. Rediscovery attaches only to the same proved identity.

## 5. Authentication, authorization and protected transport

Selected flow: authenticated HA browser -> hioc_operator service integration ->
mutually authenticated HTTPS HIOC adapter -> AssetService. No direct browser adapter
access, generic remote shell, unrestricted MQTT write topic or PE-4 credential reuse.

Supported implementation evidence reviewed 2026-10-21:
[HA authentication](https://developers.home-assistant.io/docs/auth_api/),
[actions](https://developers.home-assistant.io/docs/dev_101_services/), and source
provenance tag 2026.8.1:
[call_service](https://github.com/home-assistant/core/blob/2026.8.1/homeassistant/components/websocket_api/commands.py),
[connection context](https://github.com/home-assistant/core/blob/2026.8.1/homeassistant/components/websocket_api/connection.py),
[admin helper](https://github.com/home-assistant/core/blob/2026.8.1/homeassistant/helpers/service.py),
[user model](https://github.com/home-assistant/core/blob/2026.8.1/homeassistant/auth/models.py),
and [auth manager](https://github.com/home-assistant/core/blob/2026.8.1/homeassistant/auth/__init__.py).
Tag is source provenance, not observed PI5 version or a permanent exact-version gate.
Delivered HA must capability-test these contracts; unsupported interface fails closed.

HA authenticated WebSocket call_service creates ServiceCall.context from the actual
connection user. On EVERY read/edit, integration resolves context.user_id using
hass.auth.async_get_user; require non-null existing active non-system-generated
administrator AND explicit operator allowlist. Reject actor/admin/authentication
fields from service_data. async_register_admin_service alone is insufficient: the
reviewed helper allows null-user calls. Explicitly deny null/system/automation
contexts; do not forward scripts as authentication. Require direct authenticated
WebSocket current_connection from the reviewed connection module, matching
connection.user.id and call.context.user_id, a normal non-system HA login refresh
token resolved using hass.auth.async_get_refresh_token(connection.refresh_token_id),
matching token.user.id, unexpired token and context.parent_id=null. Recheck active
user, token existence/expiry and provider validation before signing; do not forward
token contents. A missing/closed authenticated connection denies the request. Unsupported connection/token APIs
fail closed. This deliberately excludes REST/script/automation-mediated edits;
not a claim that a user context alone proves an interactive Dashboard origin.
User deactivation/removal denies
new assertions. Trusted HA core/integrations can create contexts: context is not
proof of physical human presence or defense against a compromised HA instance.

Integration services: hioc_operator.get_policy, create_asset_policy,
update_asset_policy, get_operation_result. Strict schemas, authenticated restricted
reads, response-capable service calls, no selectable user in payload. UI hidden state
is not authorization. HA implementation must use supported service-response handling;
safe exceptions for user-facing failure, no raw backend exception disclosure.

Transport: TLS >=1.2 with verified server CA+hostname and pinned allowed client public
key for this integration; no redirects, verify=False, credentials in URL, plaintext,
public wildcard listener or browser CORS. Bind to later approved private interface;
firewall only observed HA source. Actual address/port/certificates remain unobserved,
not deployment assumptions. TLS client certificate authenticates SERVICE, not person.

Integration signs each bounded request with a separate 256-bit HMAC-SHA256 assertion
key. Backend maps client certificate+key_id to one approved issuer/HA instance;
independent HIOC ACL authorizes issuer+actor+operation+Asset scope. Actor comes only
from freshly checked HA context, never browser claims. HA token never leaves HA.
Shared key/certificate alone does not authorize a write: valid short-lived signed
actor assertion AND backend actor ACL are required. This is federation attested by
trusted HA integration, NOT per-user private-key authentication at HIOC. Compromise
of that trusted integration permits forged assertions; acknowledge that trust limit.

HA owns private client/assertion keys; HIOC owns server key and independent ACL/trust.
No keys in browser, cards, Git, MQTT, logs or source. File-backed secrets require
observed owner, 0600 files/0700 private parents; actual supported HA secret placement
must be established before delivery. Rotation uses explicit new key_id/certificate
and bounded overlap; revoke either binding at HIOC to immediately deny new requests.
Backend actor ACL removal is immediate; HA-only revocation can leave an issued
assertion valid for <=30 seconds. Do not claim instantaneous cross-host revocation.
No key issuance/rotation/service creation occurs here or automatically on restart.

Browser uses existing authenticated same-origin HA WebSocket/session. No new cookie
write route; no adapter cookie auth or CORS write access. Prove HA Origin and
unauthenticated/cross-origin rejection in acceptance; CSRF-equivalent protection
cannot be assumed from card placement. Integration restart reloads backend state,
never queues edits. Backend unavailable means unavailable/save disabled, not OFF.

## 6. Closed editing protocol and replay-safe mutation

Only POST /pe7/v1/policy/get, /create, /update, /result. Max 8192 UTF-8 bytes, depth 4,
application/json, no duplicate/extra keys, compression, query parameters, batches or
redirects. One Asset per request. UTC timestamps use six fractional digits+Z;
UUID4 values lowercase hex32, SHA/HMAC lowercase hex64; bool is not integer.
Canonical signing JSON: sorted keys, compact separators, ensure_ascii=true,
allow_nan=false, ASCII bytes with no trailing LF.

Exact outer keys: schema_version='1.0', assertion, payload, signature.
assertion exact keys: issuer (provisioned HA instance UUID), audience='hioc.pe7.asset',
key_id, actor_id, context_id, request_id, issued_at, expires_at, method='POST', path,
payload_sha256. key_id 1..64 and actor/context IDs 1..128 ASCII alphanumeric/_/-;
request_id UUID4. path must match actual one allowed route; payload_sha256 hashes
canonical payload. signature is constant-time-verified HMAC of canonical
{assertion,payload}. now>=issued_at, now<expires_at, lifetime<=30 seconds; invalid,
future, reversed or uncertain clock denies mutation, no skew-based expiry extension.
This editing assertion lifetime is NOT a device-monitoring or source TTL.

Get payload exact keys: asset_id. Result payload: operation_id, asset_id.
Create/update payload exact keys: asset_id, store_epoch, expected_store_revision,
expected_revision, operation_id, fields. Store epoch/revision come from authoritative
read; missing store cannot be remotely initialized. expected_revision=null is
create-only; update requires exact positive record revision. operation_id UUID4
identifies one logical user action; transport request_id is distinct. fields is a
nonempty subset of exactly expected_availability, infrastructure_device,
infrastructure_type with section 2 types. No descriptions, identity, paths, profiles,
severity, credentials, orphan flag, schedules, deletion, backup, restore or migration.

On every mutation: verify bounded schema, TLS/service trust, signature, fresh actor
assertion, independent ACL and quota before AssetService. Under exclusive Asset
lock recheck trust/ACL, epoch/store revision, record revision, identity and fields.
Create cannot overwrite existing Asset. Conservative store-wide revision prevents
lost updates across Assets as well as per-record conflicts; conflict requires user
reload/reapply, never silent last-writer-wins or automatic new intent.

Durable idempotency is part of SAME 2.0 Asset store: policy_requests entries exact
keys issuer_digest, actor_digest, operation_id, request_sha256, expires_at, asset_id,
committed_revision, committed_store_revision, outcome. Digests hash canonical issuer/
actor strings; request hash covers canonical logical mutation payload excluding
transport assertion/request_id. outcome changed/no_change. Retain 120 seconds from
initial request; expires_at is receipt retention, not assertion validity. Max 1024
entries; never evict live entries; capacity full -> BUSY before mutation. Expired
receipts may be pruned only during an explicit transaction, no cleanup daemon.

Same authorized actor+issuer+operation with identical payload returns original
receipt, never reapplies mutation or claims old values are still current. Same
operation with different payload -> REPLAY_CONFLICT. Check existing matching receipt
BEFORE applying normal stale-revision rejection; otherwise safe retry of a committed
operation could never resolve. Receipt and resulting store revision/Asset content
commit in one atomic replacement. No separate nonce file can authorize a duplicate.
Transport nonce cache lasts through assertion expiry; persistent receipt and epoch/
revision checks prevent reapplication after restart. Expired assertion always denied;
fresh assertion with expired receipt/stale revision still cannot apply again.

Integration may issue a fresh authenticated assertion for SAME operation_id+identical
logical payload only to reconcile an uncertain save after rechecking that actor.
No automatic mutation retry, changed-revision replay or background edit queue. UI
shows Read saved result on timeout. Result read restricted to that issuer+actor.
If result not found, do not infer no mutation from a missing receipt after retention;
read current policy/revision and retain uncertainty if necessary.

Remote no-op preserves record revision/timestamps, increments store_revision once
to commit its receipt: explicit new protocol semantics. Existing CLI no-op remains
unchanged. Legacy content writes increment store_revision; restores rotate epoch.
Fresh store-wide revision comparisons and epoch protect ABA and replay after restore.
Mutation quota: 10 attempts/actor/minute and 100 aggregate/minute; bounded limiter,
fail closed if unavailable. Denied writes produce no Asset content change. Durable
replay tests include crash before/after replacement and status failure.

Success response exact keys: schema_version='1.0', operation_id (null for get),
result (read/created/updated/no_change/replayed), commit_state='CONFIRMED', policy,
receipt (null for get, otherwise original operation receipt). policy exact keys:
asset_id, attachment (strong/orphan/weak/conflicted/absent), store_epoch,
store_revision, revision (null if absent), expected_availability,
infrastructure_device, infrastructure_type, effective_expected_availability,
effective_infrastructure_type, applied_policy_revision (null until evaluated).
Effective expected is true only for explicit true; effective type null unless
infrastructure=true. Absent Asset returns null fields, actual initialized epoch/
store revision and revision=null; no write. Replayed response includes ORIGINAL
receipt and CURRENT policy, explicitly not a claim old revision remains current.

Result response exact keys: schema_version='1.0', operation_id, result (found/not_found),
receipt (entry or null), policy (as above), commit_state (CONFIRMED/UNKNOWN).
Errors exact keys: schema_version='1.0', operation_id (null if untrusted), result='error',
error_code, commit_state (NOT_APPLIED/UNKNOWN), retryable (boolean). Codes:
AUTH_REQUIRED, FORBIDDEN, TRUST_INVALID, ASSERTION_EXPIRED, REPLAY_CONFLICT,
REVISION_CONFLICT, IDENTITY_UNSAFE, VALIDATION_FAILED, STORE_UNAVAILABLE,
UNSUPPORTED_SCHEMA, RATE_LIMITED, BUSY, COMMIT_UNKNOWN. HTTP mapping: 401 authentication,
403 authorization/trust, 409 conflict, 422 data/identity, 429 quota, 503 unavailable/
uncertain, 200 read/update, 201 creation. Safe HA exceptions map these codes; no raw
exception, credential, path, entity, name or private field content in errors.

Post-replace fsync/status uncertainty returns COMMIT_UNKNOWN, never saved. Durable
receipt can establish content application while status/durability remains unknown;
authorized read-only reconciliation must verify actual store/status and report
what is proven. Cannot manufacture CONFIRMED from receipt alone after uncertain
physical durability. No auto-restore. Audit operation/actor/Asset digests, revisions,
outcome and time only. No raw user IDs, household metadata, credentials or keys.

## 7. Dashboard editing and supported delivery

Extend HA/Lovelace; no new frontend framework. One bounded local custom device-details
editor calls the four authenticated services, using service response support. It
shows Expected Availability and Infrastructure Device separately, conditional type,
technical identity context and operator provenance; no unrelated private Asset fields.
Do not store per-user private responses in shared HA entities. Helpers/input_boolean/
input_select are not the authoritative policy. No frontend-only successful toggle.

Loading/unavailable/unauthorized blocks saves. Null shows Not configured (effective
OFF), distinct from explicit OFF. Reset to unconfigured is an explicit action, not
an automatic toggle consequence. Saved state changes only after backend ACK; draft,
saving, failed and revision-conflict states are visible. On failure retain confirmed
value and unsaved draft; conflict requires reload/reapply. One outstanding save per
Asset; rapid unsent draft edits may coalesce, sent writes never reorder. Application
revision is separate from persistence ACK; show pending next valid evaluation until
applied revision matches. Reload/navigation never writes. Type is hidden/inactive
when infrastructure OFF and restored visibly on re-enable. New eligible Asset
requires explicit Create Asset and Save. UI controls may be changed any time through
that workflow, not conditioned on a healthy monitoring cycle.

Preserve accepted operator layout/theme/navigation. Repository YAML copying alone
is not live storage-managed Dashboard delivery. PE-7.3 uses supported HA resource/
Dashboard editor management for guarded card/view addition with export/backup;
no .storage editing or prerequisite Dashboard mode migration. Exact current layout,
resource support and permissions are later observed facts, not assumptions.

## 8. Availability observation and evaluation

Pure evaluator inputs: validated Asset policy/epoch/revision, strong attachment,
approved profile, immutable source snapshots and prior per-Asset machine state.
No evaluator Asset writes, implicit enabling or public inventory-health replacement.
Machine evaluation state may persist with existing incident engine, not as another
operator-policy store. No classification or PE-5 producer execution side effect.

Closed normalized observation keys: schema_version='1.0', source_id, source_kind
(network/ha), asset_id, device_id, source_epoch, sample_id, observed_at, collected_at,
collection_status (SUCCESS/FAILED/UNAVAILABLE), completeness (COMPLETE/INCOMPLETE),
evidence_kind (POSITIVE/NEGATIVE/UNKNOWN), scope (DEVICE/ENTITY), authority_ref,
valid_until, reason_code, source_sha256. Private identifiers stay local; evidence
uses opaque digests. Only approved source/mapping definitions may normalize samples.
Unknown fields, identity/epoch/mapping mismatch or invalid times disqualify evidence.

Observation source_id/authority_ref/reason_code and profile IDs use 1..128 ASCII
alphanumeric/_/- identifiers; asset_id/device_id obey Asset grammar; source_epoch
UUID4 hex32; sample_id lowercase SHA-256 of canonical source epoch/report identity;
source_sha256 hex64. Times use the UTC grammar. All definitions/maps are closed;
enabled_sources is a sorted unique list of defined IDs, <=16; source_definitions
contains exactly those definitions, no executable expressions. Mapping revision
positive integer, mapping hash hex64, physical_device_authority exact bool;
positive_meanings/negative_meanings are disjoint bounded lists (<=16 values, each
1..128 noncontrol characters) reviewed for that source. No contradictory positive/
negative meaning or empty enabled set may be treated as operational availability.

Profile exact keys: schema_version='1.0', profile_id, revision, enabled_sources,
source_definitions, evaluation_interval_seconds, negative_confirmations,
recovery_confirmations, grace_seconds, reminder_interval_seconds. Per-source exact
keys: source_id, kind, expected_report_seconds, allowed_jitter_seconds,
max_age_seconds, positive_meanings, negative_meanings, physical_device_authority,
mapping_revision, mapping_sha256. Timing integer seconds, positive except jitter
may be zero; confirmation counts integers >=2; reminder_interval_seconds=null
(initial release has no repeated reminders). IDs/meanings reference the versioned
allowlisted source contract, not arbitrary executable expressions.

No production defaults silently enable profiles or schedules. max_age covers the
source's documented report cadence+jitter; grace >= largest enabled expected report
period+jitter. Concrete timings/counts must be explicitly accepted with source
semantics/cadence evidence before PE-7.4. No copying inventory 900/3600 or PE-6 2100
as outage thresholds. Missing profile -> UNKNOWN. Algorithm is implementable with
approved profile parameters and synthetic fixtures; no production threshold is
invented here. Profile revision/change is local governed configuration, not editable
through the Dashboard policy adapter.

A positive network observation must establish the unique current identity. DHCP
assignment/expiry, configured presence, stale neighbor cache, retained inventory or
health summary cannot establish a new positive or qualified negative. A complete
passive sweep's absence is NOT physical unavailability. No new pings/scans/Active
Discovery. Network negative authority only through an existing separately authorized
DEVICE-scope source with approved negative meaning; none is assumed configured.

Qualified samples require successful COMPLETE collection, approved authority,
identity/mapping, nonfuture/nonreversed time, fresh observed_at and valid_until.
collected_at does not refresh source time. Independent confirmations require actual
distinct advancing producer report sample_id+source_epoch+observed_at; repeated
reads/evaluations of one snapshot count once. Out-of-order/duplicate samples ignored;
source restart resets baseline. Expected-policy/profile/identity changes reset
counters; descriptive infrastructure/type edits do not reset availability evidence.
Output binds all input digests, revisions, evaluated_at and exclusive valid_until.

Order: explicit OFF/null -> NOT_MONITORED; unsafe identity -> UNKNOWN; failed/missing/
invalid source -> UNKNOWN; only aged usable observations -> STALE; contradictory
fresh physical evidence -> UNKNOWN/SOURCE_CONFLICT; qualified impairment -> DEGRADED;
qualified positive -> AVAILABLE or RECOVERING; qualified physical negative with no
contradicting fresh physical positive, distinct negative_confirmations AND elapsed
grace -> OFFLINE. Pending qualified negative is DEGRADED/pending, no outage push.
Loss of an irrelevant optional unselected source cannot invalidate an independent
approved authoritative source; all selected sources must have explicit quality.

NOT_MONITORED is policy; UNKNOWN is inadequate evidence; STALE is observation age;
DEGRADED is qualified impairment; OFFLINE is qualified physical outage; RECOVERING
requires positive-evidence confirmation for an open case. AVAILABLE is availability
within source scope, not proof all applications/automations work. These private
PE-7 states do not replace accepted inventory health enums. Unknown/stale freezes
outage/recovery progression, not erase the last confirmed case or invent recovery.

## 9. Minimal read-only HA availability contract

Use observation role in new integration, distinct from operator edits and PE-4
registry access. Read only explicit local allowlisted entity IDs via hass.states.get;
no get-all-states, history, event firehose, services, automations or HA writes.
Emit normalized evidence, not raw states/attributes/names/entity IDs publicly.
Separate observation key/certificate/audience and scope from operator editing;
observation credential can NEVER call Asset endpoints or impersonate a user.

Dedicated POST /pe7/v1/observations accepts at most 256 normalized samples/256 KiB,
strict schema, signed service envelope issuer, audience='hioc.pe7.observation',
request_id, issued_at/expires_at<=30 seconds, payload hash and signature using
separate key, same TLS/nonce checks. This role is service-authenticated, not falsely
labelled an operator. Writes only private observation machine state on HIOC under
later execution authority. This is not a second Asset policy owner.

Require current confirmed PE-4 strong-MAC association, entity membership in that
HA device, no historical/current binding conflict and reviewed semantic mapping.
Registry presence is not live evidence. HA switch off is not device offline.
unknown, unavailable, missing/removed entity and collector failure default UNKNOWN.
DEVICE-scope negative only if a reviewed physical connectivity source's integration
contract actually supports that conclusion; default physical_device_authority=false.
Many correlated entities do not supply independent votes for a physical outage.

Use actual source-report timestamp (State.last_reported when capability-supported
and semantic profile establishes report meaning); do not use last_changed or read
time as proof of fresh physical observation. last_reported alone does not prove
hardware polling. Unsupported reporting semantics -> UNKNOWN. Sample identity binds
HA/collector epoch, mapping, report timestamp/digest. Re-reading same State counts
once. COMPLETE means each allowlisted member has explicit observation status;
missing remains UNKNOWN, not negative. Restart/transport loss/denied access/staleness
retains history but cannot produce new availability conclusions. Conflicting fresh
qualified network/HA evidence remains explicit, not unconditional OR/AND precedence.
[HA State contract](https://developers.home-assistant.io/docs/dev_101_states/) is
source documentation, not an observed PI5 capability. No live API/credential claim.

## 10. Existing incident engine integration and notifications

Existing incident engine v2 remains sole lifecycle writer. Add a versioned per-Asset
PE-7 case map inside its state/transition transaction, not another incident daemon
or lifecycle system. Case key SHA-256 of canonical ['pe7_expected_availability',asset_id];
episode increments only for a new qualified outage after actual prior resolution.
Incident id binds case key+episode, never IP/name. Persist policy/profile/mapping
revisions, processed sample identities, counters, evidence deadline, lifecycle,
suppression reason, original detection/recovery times and event dedup IDs.

All Asset cases progress independently. Existing single-active display becomes a
derived selection without losing other cases: process legacy incident path unchanged;
retain all PE-7 cases; never supersede/discard an unrelated active legacy incident
merely to display PE-7. If legacy active exists it retains existing active slot;
otherwise select unsuppressed PE-7 by severity, detection UTC, stable ID. Separate
bounded PE-7 summary lists all cases with explicit count/completeness. Existing
active/history MQTT contracts remain compatible; new PE-7 summaries/transitions use
explicit versioned, allowlisted fields, no raw Asset metadata. No all-clear while
undisplayed unsuppressed cases remain. Notifications are driven by each episode's
transition, not whether it wins the single displayed slot.

Legacy HA start-notification automation must exclude a displayed incident whose
id is explicitly identified in the current validated PE-7 summary; PE-7 episode
consumer owns those pushes. This narrow origin check changes no legacy severity or
recipient. Missing/invalid PE-7 summary cannot suppress an unrelated legacy incident;
PE-7 presentation/notifications then report unavailable and do not guess ownership.
Versioned PE-7 summary exact keys: schema_version='1.0', evaluated_at, valid_until,
status (VALID/UNAVAILABLE), total_case_count, omitted_case_count, cases. No truncation
may imply all-clear. Each case projection exact keys: incident_id, asset_id_digest,
episode, lifecycle, availability_state, suppression_reason, severity, policy_revision,
profile_revision, detected_at, updated_at. Fields are normalized types from this
contract, no names, locations, entity IDs, raw observations or secrets. New transition
message exact keys: schema_version='1.0', event_id, incident_id, event_kind
(OUTAGE_STARTED/OUTAGE_RECOVERED), severity, occurred_at, policy_revision,
asset_id_digest. Canonical event_id binds case key+episode+kind. These bounded
operational projections require PE-7.1 compatibility/privacy tests and explicit
later MQTT/HA publication authority; nothing publishes in this preparation.

Preserve detected -> confirmed -> active -> recovering -> resolved meanings. A
qualified negative may create an internal detected case, but outage activation and
push require both distinct sample count AND grace. Real qualified positive samples
advance recovery count. Missing/stale/invalid evidence freezes progression and shows
that uncertainty alongside retained case. PE-7 MUST NOT use legacy no-candidate
recovery when evidence disappears. Suppression is orthogonal to lifecycle, not a
new synonym for resolved. Existing legacy recovery behavior stays unchanged.

Expected ON->OFF preserves episode/history and freezes lifecycle, sets suppression
OPERATOR_DISABLED and records PolicyMonitoringDisabled. It cancels proposed/pending
PE-7 pushes without an already committed dispatch authorization; section 10's bounded
pre-OFF authorization/in-flight exception is explicit, not a recovery or new permit.
No IncidentResolved/reconnected claim. Re-enable resets evidence baseline/counters
and resumes same unresolved episode; no duplicate incident/start push solely from
enabling. Actual recovery resolves after qualified positives; subsequent new
qualified outage after that resolution creates next episode. Type/infrastructure
edits change neither case/severity nor counters; rebind policy revision without
reset if expected_availability semantics are unchanged.

Initial confirmed PE-7 outage severity warning; no automatic major/critical from
infrastructure or type. Qualified impairment is warning diagnostic without outage
push until confirmation. Existing unrelated severity/UPS/internet policy unchanged.
Later escalation needs explicit impact-backed accepted policy, not inferred here.
Use existing HA notification transport/operator enable gate and configured recipient;
no discovery/reprovisioning of recipients. One start and one actual recovery event
per episode, stable key case+episode+event_kind, persistent HA consumer dedup and
stable notification tag. OFF is not a recovery push. No recurring reminder initially.
Exactly-once external delivery is not promised across crash-after-delivery-before-ack;
record that limitation and use receiver dedup where supported.

New case state plus notification outbox commit atomically via engine-owned validated
state with one existing incident-engine lock; no partial-write recovery based on
empty fallback dictionaries. Restart restores episode/sample/outbox identity;
downtime is not a negative sample. PE-7.1 must implement safe new transaction boundary
without redesigning unrelated incidents/history retention. Normal evaluation releases
Asset before incident work; dispatch authorization alone uses the ordered guard
below. Queueing or an unguarded policy recheck never constitutes dispatch authority.
A message describes evidence/policy at authorization time, not guaranteed current
monitoring at delivery time.

### Correction B: notification authorization linearization and delivery

Keep notification proposals/outbox/authorization receipts in the EXISTING incident
engine's versioned state, with its sole writer; no second Asset policy store, new
scheduler or extra credentials. Define these distinct states:

- PROPOSED: qualifying event exists, not yet queued/authorized.
- PENDING_AUTHORIZATION: durable queued event, no permission to submit externally.
- AUTHORIZED: one durable bounded permission committed under the guard below;
  no external transport attempt has yet been claimed.
- IN_FLIGHT: one attempt durably claimed for that authorization; actual transport
  submission may be about to start (transport_started_at records when it does).
- TRANSPORT_ACCEPTED or DELIVERED: provider acceptance or separately evidenced
  delivery respectively; never claim delivered from an HTTP/MQTT acceptance alone.
- FAILED_NOT_SUBMITTED: submission demonstrably did not occur; no automatic retry.
- DELIVERY_UNKNOWN: transport may have accepted it; do not resend automatically.
- CANCELLED or EXPIRED: terminal non-send disposition with retained history.

AssetService exposes an INTERNAL validated shared policy read guard to the existing
incident engine, not an adapter/Dashboard mutation endpoint. Engine first releases
any incident batch lock, acquires that shared Asset guard, then its exclusive
incident lock. All dual-lock acquisitions use Asset -> incident, release reverse;
never incident -> Asset. No nested/reentrant acquisition, unbounded lock wait or
network call while either is held. Asset writers/CLI/adapter take exclusive Asset
lock and never incident; they serialize OFF against the shared read guard. This
narrow prospective ordering exception is necessary to close the identified race;
it changes neither authoritative Asset ownership nor historical validator rules.

Under both guards, revalidate strict current store/epoch, exact record and expected-
policy revision, expected_availability=true, safe identity, approved activation,
qualifying unexpired case/event evidence, episode state, dedup and absence of a
previous grant/attempt. Missing revision, failed/uncertain read, unsupported store,
conflict or OFF denies authorization; no UNKNOWN-to-ON assumption. Persist a grant
in the same atomic, fsynced incident outbox transaction. Its durable completion,
WHILE the shared Asset guard is held, is the dispatch-authorization LINEARIZATION
POINT. Only afterward release incident then Asset. A failed/uncertain outbox commit
grants no permission to the current sender; no automatic reconciliation send.

Grant fields: authorization_id, event_id, asset_id, store_epoch, policy_revision,
case_key, episode, event_kind, evidence_sha256, authorized_at, not_after, process_epoch,
state, claimed_at, transport_started_at, completed_at, outcome. IDs/digests obey
existing grammars; optional times/outcome null until established. not_after is the
EARLIER of authorized_at+5 seconds and qualifying evidence's exclusive valid_until.
This is a proposed dispatch safety bound, not a device outage/freshness threshold.
Evidence already expired cannot obtain a grant. No extension by re-reading/retrying.

OFF's linearization point is its successful Asset content transaction commit while
holding exclusive Asset lock (uncertain commit stays fail-closed, never assumed ON).
If OFF commits first, the authorizer subsequently sees OFF/new revision and cannot
issue a grant. All ungranted old-policy proposals/pending events are immediately
ineffective for sending; the incident engine marks them CANCELLED/OPERATOR_DISABLED
when it next processes the outbox. Delayed bookkeeping cannot confer authority.
If grant commits first, it is an ALREADY AUTHORIZED operation, permitted for one
bounded attempt even if OFF commits before actual transport submission. This narrow
exception must be visible, not described as a post-OFF new notification authorization.
No new grant may linearize after OFF while monitoring remains disabled.

Before transport submission, existing engine acquires the SAME ordered shared
Asset guard -> incident lock, validates current store_epoch against the grant, and
atomically changes AUTHORIZED -> IN_FLIGHT. It verifies grant process_epoch, event
uniqueness and unexpired deadline, then releases both locks. This epoch check rejects
restore-invalidated grants; current OFF does not retroactively revoke the bounded
pre-OFF grant. Failed/uncertain store read denies claim. Only that claimant may attempt once;
no other worker retries or claims it. At the submission boundary recheck deadline;
if expired, mark EXPIRED without submitting. Use a deadline-aware transport with
remaining total timeout <=5 seconds, no library/HTTP/MQTT application-level retries
and no offline publication queue that can submit later on reconnection. If the
existing transport cannot enforce these bounds, do not send or claim acceptance.
No hard-real-time process scheduling or remote delivery deadline is claimed.

OFF while AUTHORIZED or IN_FLIGHT does not revoke the already granted single attempt;
it may cancel before submission opportunistically, but cannot be promised to recall
external delivery. Once the deadline passes, no fresh submission/claim is allowed.
Transport already initiated may be accepted/delivered later despite timeout or OFF;
record that possibility as DELIVERY_UNKNOWN until independently established.
Queued-unsent does NOT mean already-authorized/in-flight. This explicit distinction
qualifies section 11 T06's concise 'cancel unsent' wording: proposed/pending sends
are cancelled; bounded pre-OFF grants retain only their original one-attempt scope.

Evidence binds grant ID, event ID, original epoch/policy revision, authorization time,
OFF committed revision/time (if any), claim/submission/completion times and provider
acceptance/delivery outcome. Log 'authorized before disable; transport accepted after'
when that order is established; timestamps alone cannot invent an unobserved outcome.
Dashboard/history shows monitoring OFF and preserved suppressed incident, plus any
already-authorized in-flight result; never device recovered/reconnected. Type-only
edits cannot generate a new event or alter an existing grant.

Restart invalidates all unclaimed prior-process grants; pending events require fresh
policy/evidence authorization, not replay. Previously IN_FLIGHT/uncertain sends remain
DELIVERY_UNKNOWN and are not automatically resent. Expired/cancelled old-policy events
are not resurrected by re-enable. The same episode/dedup rules remain; new qualified
transitions may create only their legitimate event, not replay a cancelled send.
Restore/epoch changes invalidate unclaimed grants. Provider stable tag/event ID
continues receiver dedup, without promising exactly-once delivery. No grants for
unrelated legacy notifications pass through this PE-7 path.

| Race fixture | Required outcome |
| --- | --- |
| B01: OFF commits before authorization | Deny grant, cancel pending event, no submission. |
| B02: Authorization commits before OFF | Retain one pre-OFF grant within deadline; no new authorization after OFF. |
| B03: OFF and authorization contend | Asset guard serializes to B01 or B02; never an unguarded third outcome. |
| B04: OFF while delivery in flight | No recall guarantee; retain OFF/suppression and actual accepted/unknown result. |
| B05: OFF between authorization and submission | Only already committed grant can send once before its deadline; expired grant cannot submit. |
| B06: Old queued event retried after OFF | Ungranted/cancelled event cannot authorize or submit; no new operation from stale queue. |
| B07: Re-enable after cancellation | Old event remains cancelled; fresh evidence/episode rules, no duplicate start or artificial recovery. |
| B08: Duplicate delivery attempts | One atomic claim/event ID; other claimant denied; provider uncertainty not automatically retried. |
| B09: Missing policy revision | Fail closed, no grant, no submission. |
| B10: Failed or uncertain policy read | Fail closed and retain diagnostic; no grant from cached ON. |
| B11: Restart during pending authorization | No pre-crash permission inferred; old grants unusable, current OFF/evidence checked before any new grant. |
| B12: Incident/history and unrelated notifications | Preserve suppressed case/history, no recovery claim, legacy notification behavior unchanged. |

PE-7.1 must exercise B01..B12 with deterministic barriers around OFF commit, guarded
authorization fsync, claim and actual transport boundary, plus grant-expiry and
uncertain-write outcomes. C18/C10/C12/C17 retain their existing acceptance scope;
these fixtures specify the previously missing ordering evidence, not new criteria
or a new review stage. Production evidence later records actual ordering and scope.

## 11. Exact operator transitions

P = persisted policy/revision; E = evaluation; I = incident; N = notification.
Each row includes saved-state UI and applicable evidence; all writes require section 5/6.

| ID | Transition | Persistent/effective state | Incident/notification effect | Evidence and Dashboard response |
| --- | --- | --- | --- | --- |
| T01 | Unconfigured -> Expected ON | true, revision+1; new E baseline | No instant outage/N | Strong attachment/profile and new samples; show ON, pending evaluation. |
| T02 | Unconfigured -> explicit OFF | false, revision+1; NOT_MONITORED | No new case/N | Authorized save; show saved OFF distinct from unset. |
| T03 | OFF -> ON with fresh positive | true; AVAILABLE if no open case | Open case RECOVERING until required positives; no instant resolved | Qualified positive; show evidence scope and application revision. |
| T04 | OFF -> ON stale/missing | true; STALE/UNKNOWN | No new outage/recovery/N | Show ON and specific missing/stale evidence reason. |
| T05 | ON -> OFF healthy | false; NOT_MONITORED | Policy event only, N none | Show OFF, never device recovered. |
| T06 | ON -> OFF open case | false; freeze I, OPERATOR_DISABLED | Keep episode/history; cancel unsent PE-7 N | Show OFF plus retained suspended case, not reconnected. |
| T07 | OFF -> ON suspended case | true; reset qualification baseline | Resume same episode; no duplicate start/reopen | New samples required; show resumed/pending. |
| T08 | Infrastructure OFF/null -> ON | true, retained type/null; expected unchanged | No case/severity/N change | Show selector and explicit Unassigned if null. |
| T09 | Infrastructure ON -> OFF | false, type retained inactive; expected unchanged | No case/N change | Hide selector, no effective infrastructure designation. |
| T10 | Type changed while ON | enum/null, toggles unchanged | No case/severity/N change | Backend-confirmed saved type, operator provenance. |
| T11 | Infrastructure re-enabled | true, retained type restored | No expected-policy/case/N change | Show restored type visibly. |
| T12 | IP changes, same ID | Policy unchanged; refresh address evidence | Same key/history, no duplicate | Strong binding recheck; settings unchanged. |
| T13 | Identity ambiguous/rotated | Preserve old Asset; UNKNOWN_IDENTITY | Freeze qualification; no recovery/new outage/N | Block unsafe ON/create; allow existing OFF; no migration. |
| T14 | Two sessions conflict | First matching revision commits; second 409 | Committed policy applied once | Conflict + last confirmed value; reload/reapply explicitly. |

## 12. Closed acceptance-readiness matrix

Every row mandatory. R = PE-7.1 native fixtures, full native regression and concise
independent code acceptance. P = PE-7.4 separately authorized bounded operator
validation plus independent evidence review. A = PE-7.5 activation/natural evidence.
No actual tests or production runs are performed in this contract preparation.

| ID | Criterion / validation method | Owner |
| --- | --- | --- |
| C01 | Four toggle combinations; exact labels; null vs explicit OFF; discovery/classification cannot set intent. Schema/evaluator/UI fixtures and actual UI saves. | R + P |
| C02 | Six type identifiers+null, conditional selector, invalid enum, inactive retention/restoration, manufacturer separate. | R + P |
| C03 | Strong creation, weak/duplicate/ambiguous/orphan, explicit create, no rendering writes/merges; IP/rediscovery persistence. | R + P |
| C04 | Exact 1.0/2.0 dispatch, policy-only records, text metadata preservation, PE-6 compatibility projection/provenance, unsupported-version refusal. | R + P |
| C05 | Migration/backup/hash/modes/owner, pre/post-replace interruption, fsync/status uncertainty, explicit rollback after edits and epoch ABA replay. | R + P |
| C06 | Reload/backend/integration restart; no queued writes, initialization or migration; unavailable/loading never saved OFF. | R + P |
| C07 | HA context identity+active/admin+allowlist, null/system/deactivated/forged user rejected; real connection-context behavior on installed HA. | R + P |
| C08 | Wrong/revoked TLS cert/key/audience/issuer/signature/actor ACL rejected; no fallback or token leakage. | R + P |
| C09 | Closed bodies/responses, duplicate/extra fields, size/depth/type limits, forbidden shell/path/profile/private-field operations. | R + P |
| C10 | Revision conflicts, idempotent same request, changed-payload replay, expiry, quota/capacity, restart and COMMIT_UNKNOWN reconciliation; one application. | R + P |
| C11 | Origin/CSRF-equivalent and unauthorized/cross-origin denial; no direct browser write/CORS or shared-service-credential-as-person. | R + P |
| C12 | T01..T14 verify persisted fields, E state, incident/N effects, source gates and truthful UI. | R + P |
| C13 | Strict observations/profiles; freshness and grace boundary; future/backward clocks; duplicates/same snapshot/out-of-order/source epoch reset. | R + P + A |
| C14 | Source failure/incomplete/missing/stale, lease expiry and passive absence never create physical outage; conflict explicit. | R + P |
| C15 | Strong HA mapping/entity membership, state scope, missing/denied/stale HA, minimal capture and no private state leakage. | R + P |
| C16 | Qualified negative count AND grace; distinct positives for recovery; stale/no-candidate freeze; intentionally intermittent OFF. | R + P + A |
| C17 | Multiple concurrent Assets, stable episode/dedup, flapping, suppression/re-enable not recovery, legacy incidents/history preserved. | R + P |
| C18 | Warning mapping/no infrastructure escalation; start/recovery gating, durable event IDs/receiver dedup, OFF race and actual recipient delivery. | R + P + A |
| C19 | Backend ACK vs draft/conflict/error, applied revision separate; no unrelated private fields in shared HA state; layout/theme/resource and storage-mode delivery. | R + P |
| C20 | Asset/inventory/PE-4/PE-5/PE-6/cross-phase/privacy/schema/incident/notification/Dashboard/release regression plus full established native suite for source implementation. | R |
| C21 | Complete eight-category captures, same-observation owner/group/mode/type/device/inode/link/size/time and required ancestors; no omissions/truncation. | P + A |
| C22 | Exact source/job/lock/schedule identities; overlap, missed cycle, expiry/restart; >=3 consecutive natural cycles and output/notification identities. | R + A |
| C23 | Old records/receipts immutable; no public inventory/MQTT drift, unauthorized producer/port/service/projection/write. | R + P + A |
| C24 | Original receipt byte hash, release/tool/dependency identity, authorization, primary/protected outcomes and exact allowed differences; independent ACCEPT before closure. | P + A + PE-7.6 |

Evidence-complete receipt captures execution ID, approved policy/profile/mapping
revisions and timings, actual source quality/time/digests, bounded invocation count,
process exit, independent primary/protected failure outcomes, module origins where
applicable, before/after intervals/capture hashes, all eight protected categories,
actual same-capture security/ancestor metadata, complete differences/counts/canonical
public evidence hash, omissions/truncation and exact permitted writes. Original JSON
bytes/digest retained; private capture preimages need not be reconstructed. Sanitized
review record references source bytes honestly; no private production data in Git.

Explicitly authorize each migration/policy/evaluation/incident/outbox write and
bound its before/after revisions. No blanket producer permission. Existing scheduled
PE-5 activity requires exact evidence review if it changes protected state; do not
disable it or execute producers as a hidden prerequisite. Known primary failure
FAIL; incomplete mandatory evidence INSUFFICIENT_EVIDENCE; two independent failures
retained separately. No universal transient-absence claim or authentication from
public hashes. Production observations remain OPERATOR_SUPPLIED unless separately
established under the governing evidence classes.

Synthetic faults first. Controlled reversible production failures only through a
separately authorized safe scope/recovery procedure. No unsolicited power loss,
shared-infrastructure disablement or active probing. If a mandatory production claim
cannot safely be demonstrated, preserve its limit and stop dependent acceptance.

## 13. Bounded checkpoint sequence and implementation scope

Each successor requires separate authority. Same checkpoint includes necessary
implementation/validation/independent acceptance/Git gates, not extra review loops.

| Checkpoint | Objective / dependency / allowed scope | Evidence and stop boundary | Next |
| --- | --- | --- | --- |
| PE-7.0 | Current Windows contract after accepted PE-6.5; one contract+minimal Master Plan. | Focused consistency then explicit independent acceptance; no COMPLETE/PASS before acceptance. No code/tests/production/publication. | PE-7.1 |
| PE-7.1 | Accepted contract implementation: AssetService/migration, authenticated adapter, HA services/observation, editor, evaluator, existing incidents/outbox and explicit bounded projection. | R matrix/full native suite, protected manifest and concise independent code acceptance, exact authorized release publication. No production/schedules. Stop failed validation or contract conflict. | PE-7.2 |
| PE-7.2 | Operator-only exact release-source synchronization. | Ancestor/tree/main/upstream/clean source evidence; no runtime installation/migration/execution. | PE-7.3 |
| PE-7.3 | Separate guarded artifact/integration/UI/trust delivery with backups/rollback. | Exact paths/hashes/modes/owners/ancestors, observed HA API/resource capability; adapter/editing/evaluator disabled except separately specified preflight. No recurring job or automatic migration. | PE-7.4 |
| PE-7.4 | Separate bounded migration/operator edits/evaluation on approved Assets and numeric profiles. | Complete P matrix, exact allowed writes, actual UI and independent acceptance; no recurring activation. | PE-7.5 |
| PE-7.5 | Separate exact schedule/notification activation after accepted P evidence. | Complete A matrix incl >=3 consecutive natural cycles, overlap/missed cycle/recovery/delivery and protected judgment. No unrelated jobs/producer change. | PE-7.6 |
| PE-7.6 | Final repository-only PE-7 closure after accepted evidence. | Current Master Plan/evidence/limitations, authorized commit/push/remote/clean verification; no repeated production run. | PE-8 |

PE-7.1 intended areas: existing assets.py/CLI/validator version dispatch and reader
compatibility; narrowly named new adapter/evaluator/observation contract modules;
existing core/correlation.py and incident-engine-v2 transaction/presentation path;
one homeassistant/custom_components/hioc_operator integration and one local device
editor resource plus minimal existing Dashboard/package changes; associated native,
HA integration/frontend and directly affected current binding tests. Exact finite
path/protected blob+mode manifest is established before implementation mutation.

No PE-4 access expansion by modifying its adapter; no PE-6 design/implementation
record rewrite. Current successor bindings may follow newly accepted artifacts;
immutable historical validators replay exact accepted Git objects, never refreshed
identities or relaxed tests. Genuine existing binding conflicts must be reported
before implementation publication, not bypassed under this documentation scope.

## 14. Selected design versus remaining production facts

Selected proposals awaiting independent acceptance: schema 2.0 migration; null-safe
independent controls and inactive type retention; strong explicit creation; HA
federated actor assertion+mTLS+independent ACL; bounded replay-safe AssetService
protocol; evidence-qualified source/profile algorithm; per-Asset cases inside
existing incident engine; suppression distinct from recovery; warning-only initial
PE-7 notification policy; supported guarded Dashboard delivery. No remaining
undecided architectural transport direction or silently selected production values.

Production facts UNKNOWN: actual PI3/PI5/HA runtime versions and required APIs;
operator IDs/ACL; address/port/firewall/certificates/key storage; live Dashboard
resource/layout; actual eligible Assets and HA mapping/source semantics; source
report cadence/jitter and accepted concrete profiles; active schedules/locks;
owner/group/mode/backups, recipients and delivery. PE-7.3 observes deployment facts,
PE-7.4 source/profile/bounded behavior, PE-7.5 recurring operation. Missing facts
block dependent production action, not parameterized synthetic repository work.
No production credential, approval ID, safety value or artifact identity is invented.

## 15. Preparation disposition

PE70_CONTRACT_PREPARED=PASS denotes prepared design, not independent acceptance,
implementation or production authority. This single contract and minimal Master
Plan are the only prepared changes. No new governance record/schema/checklist,
code/test implementation, service, credential, Dashboard change, schedule,
migration, monitoring run, commit or push. Next action: independent acceptance of
THIS consolidated PE-7.0 contract. Stop; do not start PE-7.1.
